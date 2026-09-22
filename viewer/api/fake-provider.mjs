// A stand-in for whatever model provider somebody points ADAM at.
//
// It answers all three wire shapes `llm.py` knows — OpenAI-compatible,
// Anthropic and Google — from one process, which is the only way to test that
// the adapter really does speak three different languages rather than one
// language three times.
//
// Nothing inside ADAM is stubbed: the service makes a real HTTP request with a
// real Authorization header and parses a real response body. What this removes
// is the money and the network, both of which make a test nobody runs twice.
//
// It also records what it was sent, so the check can assert on the things that
// are invisible from ADAM's side: that the system prompt went in the field that
// shape puts it in, that the history arrived in order, and that a key is sent
// the way that provider expects it.
import { createServer } from 'node:http';

const PORT = Number(process.env.PORT ?? 8797);

// The one key each shape accepts. Anything else is refused the way that
// provider refuses it, so ADAM's "would not accept that key" path is exercised
// against a real 401 rather than a mocked exception.
const GOOD = 'good-key';

const seen = [];
const json = (res, code, body) => {
  res.writeHead(code, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
};
const read = (req) => new Promise((resolve) => {
  const parts = [];
  req.on('data', (c) => parts.push(c));
  req.on('end', () => { try { resolve(JSON.parse(Buffer.concat(parts).toString())); } catch { resolve({}); } });
});

createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  if (path === '/_seen') return json(res, 200, { seen });
  if (path === '/_reset') { seen.length = 0; return json(res, 200, { ok: true }); }

  // ── OpenAI-compatible ──────────────────────────────────────────────
  const bearer = (req.headers.authorization ?? '').replace(/^Bearer /, '');

  if (path === '/openai/models') {
    if (bearer !== GOOD) return json(res, 401, { error: { message: 'Incorrect API key provided.' } });
    return json(res, 200, { data: [{ id: 'fake-large' }, { id: 'fake-small' }] });
  }
  if (path === '/openai/chat/completions' && req.method === 'POST') {
    if (bearer !== GOOD) return json(res, 401, { error: { message: 'Incorrect API key provided.' } });
    const body = await read(req);
    seen.push({ shape: 'openai', auth: 'bearer', body });
    if (body.model === 'over-quota') {
      return json(res, 429, { error: { message: 'You exceeded your current quota.' } });
    }
    return json(res, 200, {
      choices: [{ message: { role: 'assistant', content: 'openai says: ' + lastUser(body.messages) } }],
      usage: { prompt_tokens: 111, completion_tokens: 22 },
    });
  }

  // ── Anthropic ──────────────────────────────────────────────────────
  const apiKey = req.headers['x-api-key'] ?? '';

  if (path === '/anthropic/v1/models') {
    if (apiKey !== GOOD) return json(res, 401, { error: { message: 'invalid x-api-key' } });
    return json(res, 200, { data: [{ id: 'fake-opus' }, { id: 'fake-haiku' }] });
  }
  if (path === '/anthropic/v1/messages' && req.method === 'POST') {
    if (apiKey !== GOOD) return json(res, 401, { error: { message: 'invalid x-api-key' } });
    const body = await read(req);
    seen.push({
      shape: 'anthropic', auth: 'x-api-key',
      version: req.headers['anthropic-version'] ?? '', body,
    });
    return json(res, 200, {
      content: [{ type: 'text', text: 'anthropic says: ' + lastUser(body.messages) }],
      usage: { input_tokens: 222, output_tokens: 33 },
    });
  }

  // ── Google ─────────────────────────────────────────────────────────
  const key = url.searchParams.get('key') ?? '';

  if (path === '/google/v1beta/models') {
    if (key !== GOOD) return json(res, 403, { error: { message: 'API key not valid.' } });
    return json(res, 200, {
      models: [
        { name: 'models/fake-pro', supportedGenerationMethods: ['generateContent'] },
        // Filtered out by the adapter: it cannot answer a question.
        { name: 'models/fake-embed', supportedGenerationMethods: ['embedContent'] },
      ],
    });
  }
  const gen = path.match(/^\/google\/v1beta\/models\/(.+):generateContent$/);
  if (gen && req.method === 'POST') {
    if (key !== GOOD) return json(res, 403, { error: { message: 'API key not valid.' } });
    const body = await read(req);
    seen.push({ shape: 'google', auth: 'query', model: gen[1], body });
    const parts = body.contents?.[body.contents.length - 1]?.parts ?? [];
    return json(res, 200, {
      candidates: [{ content: { parts: [{ text: 'google says: ' + (parts[0]?.text ?? '') }] } }],
      usageMetadata: { promptTokenCount: 333, candidatesTokenCount: 44 },
    });
  }

  return json(res, 404, { error: { message: `nothing at ${path}` } });
}).listen(PORT, '127.0.0.1', () => console.log(`fake provider on ${PORT}`));

/** The last user turn, echoed back so the check can prove the question really
 *  travelled — and, in the Anthropic and OpenAI shapes, that history arrived in
 *  order rather than reversed. */
function lastUser(messages) {
  const mine = (messages ?? []).filter((m) => m.role === 'user');
  return mine.length ? String(mine[mine.length - 1].content).slice(0, 200) : '';
}
