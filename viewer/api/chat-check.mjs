// Asking ADAM, on anybody's key and anybody's provider.
//
// Three things this file is really about:
//
//   **The adapter speaks three languages, not one three times.** The system
//   prompt is a top-level field on Anthropic, a first turn on OpenAI and
//   `systemInstruction` on Google; the key is a bearer, a header and a query
//   parameter. The stand-in records what it was actually sent, so each of those
//   is asserted rather than assumed from a 200.
//
//   **A key is verified, encrypted, and never comes back.** Not to the page,
//   not in a listing, not in an error.
//
//   **A key is one person's.** Everything here runs on the caller's own, so one
//   account's key cannot answer another account's question.
//
//   node api/fake-provider.mjs                              # port 8797
//   TICVAI_DB=/tmp/chat.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/chat.db API=http://localhost:8799 FAKE=http://127.0.0.1:8797 \
//     node api/chat-check.mjs

const API = process.env.API ?? 'http://localhost:8787';
const FAKE = process.env.FAKE ?? 'http://127.0.0.1:8797';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const jars = new Map();
async function as(who, method, path, body) {
  const cookie = jars.get(who);
  const res = await fetch(`${API}${path}`, {
    method,
    headers: { 'content-type': 'application/json', ...(cookie ? { cookie } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) jars.set(who, set.split(';')[0]);
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

const PASSWORD = 'a-long-enough-passphrase';
const seen = async () => (await (await fetch(`${FAKE}/_seen`)).json()).seen ?? [];
const reset = () => fetch(`${FAKE}/_reset`);

// Every shape points at the stand-in through the OpenAI-compatible escape
// hatch's endpoint override — which is also the feature that makes "any
// provider" true, so exercising it here is not incidental.
const ENDPOINTS = {
  openai: `${FAKE}/openai`,
  anthropic: `${FAKE}/anthropic`,
  google: `${FAKE}/google`,
};

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);

const invited = await as('boss', 'POST', '/api/invites',
  { email: 'harness.dev@softlabsgroup.com', role: 'dev' });
const token = (invited.data?.url ?? invited.data?.link ?? '').split('#')[1];
const took = await as('harness.dev', 'POST', '/api/auth/redeem',
  { token, password: PASSWORD, name: 'Harness Dev' });
check('a developer is invited', took.status === 200, `${took.status}`);

// ── who there is, before anybody has a key ───────────────────────────

const empty = await as('harness.dev', 'GET', '/api/chat/providers');
check('the providers are listed before any key exists', empty.status === 200, `${empty.status}`);
const ids = (empty.data?.providers ?? []).map((p) => p.id);
check('including the big three and the escape hatch',
  ['anthropic', 'openai', 'google', 'compatible'].every((p) => ids.includes(p)),
  ids.join(' '));
check('none of them is configured yet',
  (empty.data?.providers ?? []).every((p) => !p.configured));
check('and each still offers models to pick from, so the page is not empty',
  (empty.data?.providers ?? []).filter((p) => p.id !== 'compatible')
    .every((p) => p.models.length > 0),
  (empty.data?.providers ?? []).map((p) => `${p.id}:${p.models.length}`).join(' '));

const noKey = await as('harness.dev', 'POST', '/api/chat',
  { question: 'anything', provider: 'openai', model: 'fake-large' });
check('asking without a key is 428 and says to add one, not 500',
  noKey.status === 428 && /key/i.test(String(noKey.data?.detail)),
  `${noKey.status} ${String(noKey.data?.detail).slice(0, 60)}`);

// ── a key is checked before it is kept ───────────────────────────────

const wrong = await as('harness.dev', 'PUT', '/api/settings/llm',
  { provider: 'openai', key: 'not-the-key', endpoint: ENDPOINTS.openai });
check('a key the provider rejects is not stored', wrong.status === 401, `${wrong.status}`);
check('and the provider\'s own sentence is carried through',
  /Incorrect API key/.test(String(wrong.data?.detail)), String(wrong.data?.detail));
check('so nothing is configured after a bad key',
  !(await as('harness.dev', 'GET', '/api/chat/providers'))
    .data.providers.find((p) => p.id === 'openai').configured);

const unknown = await as('harness.dev', 'PUT', '/api/settings/llm',
  { provider: 'nonesuch', key: 'good-key' });
check('a provider nobody has heard of is refused, with the list',
  unknown.status === 400 && /openai/.test(String(unknown.data?.detail)),
  String(unknown.data?.detail).slice(0, 70));

const sneaky = await as('harness.dev', 'PUT', '/api/settings/llm',
  { provider: 'compatible', key: 'good-key', endpoint: 'https://user:pw@example.com/v1' });
check('an endpoint carrying a credential is refused — that column is plaintext',
  sneaky.status === 400 && /unencrypted/.test(String(sneaky.data?.detail)),
  String(sneaky.data?.detail).slice(0, 70));

const noBase = await as('harness.dev', 'PUT', '/api/settings/llm',
  { provider: 'compatible', key: 'good-key' });
check('and the compatible entry needs an address as well as a key',
  noBase.status === 400, `${noBase.status} ${String(noBase.data?.detail).slice(0, 50)}`);

// ── three shapes, one adapter ────────────────────────────────────────

for (const [provider, endpoint] of Object.entries(ENDPOINTS)) {
  const saved = await as('harness.dev', 'PUT', '/api/settings/llm',
    { provider, key: 'good-key', endpoint });
  check(`a ${provider} key is accepted and checked`, saved.status === 200,
    `${saved.status} ${JSON.stringify(saved.data?.detail ?? saved.data?.checked ?? '')}`);
  check(`and the check found models rather than just returning 200`,
    /model/.test(String(saved.data?.checked)), String(saved.data?.checked));
}

const stored = await as('harness.dev', 'GET', '/api/chat/providers');
const by = Object.fromEntries((stored.data?.providers ?? []).map((p) => [p.id, p]));
check('all three now read as configured',
  ['openai', 'anthropic', 'google'].every((p) => by[p].configured));
check('the models now come from the provider rather than the table',
  by.openai.models.join(',') === 'fake-large,fake-small', by.openai.models.join(','));
check('and Google\'s list drops the model that cannot answer a question',
  by.google.models.join(',') === 'fake-pro', by.google.models.join(','));

// **The key never comes back.** Not in the listing, not anywhere.
check('no listing carries a key, only the last four characters',
  !/good-key/.test(JSON.stringify(stored.data)),
  (stored.data?.providers ?? []).map((p) => p.hint).filter(Boolean).join(' '));

// ── the questions ────────────────────────────────────────────────────

await reset();

const asked = await as('harness.dev', 'POST', '/api/chat', {
  question: 'Which operations write to orders.sales_order?',
  provider: 'openai', model: 'fake-large',
  context: [{ title: 'table orders.sales_order', text: 'columns: id, total, status' }],
});
check('a question is answered', asked.status === 200,
  `${asked.status} ${JSON.stringify(asked.data?.detail ?? '')}`);
check('and the answer really came from the provider',
  /^openai says:/.test(asked.data?.answer ?? ''), (asked.data?.answer ?? '').slice(0, 40));
check('the excerpt travelled with the question',
  /orders\.sales_order/.test(asked.data?.answer ?? ''), asked.data?.answer);
check('and what it cost is reported, because it is the person\'s own money',
  asked.data?.usage?.in === 111 && asked.data?.usage?.out === 22,
  JSON.stringify(asked.data?.usage));

const sentOpenai = (await seen())[0];
check('the OpenAI shape carries the key as a bearer token',
  sentOpenai.auth === 'bearer', sentOpenai.auth);
check('and the system prompt as the first turn, which is where that shape puts it',
  sentOpenai.body.messages[0].role === 'system'
  && /answering questions about one delivery package/.test(sentOpenai.body.messages[0].content),
  sentOpenai.body.messages[0].role);

await reset();
const viaAnthropic = await as('harness.dev', 'POST', '/api/chat', {
  question: 'Same question, different provider.',
  provider: 'anthropic', model: 'fake-opus',
  context: [{ title: 'a table', text: 'columns: id' }],
});
check('the same question goes to a different provider on the same page',
  viaAnthropic.status === 200 && /^anthropic says:/.test(viaAnthropic.data?.answer ?? ''),
  (viaAnthropic.data?.answer ?? '').slice(0, 40));
const sentAnthropic = (await seen())[0];
check('that shape carries the key in x-api-key, not a bearer',
  sentAnthropic.auth === 'x-api-key', sentAnthropic.auth);
check('and pins the API version rather than tracking latest',
  /^\d{4}-\d{2}-\d{2}$/.test(sentAnthropic.version), sentAnthropic.version);
check('with the system prompt as its own field, not a turn',
  typeof sentAnthropic.body.system === 'string'
  && sentAnthropic.body.messages.every((m) => m.role !== 'system'),
  Object.keys(sentAnthropic.body).join(','));

await reset();
const viaGoogle = await as('harness.dev', 'POST', '/api/chat', {
  question: 'And again.', provider: 'google', model: 'fake-pro',
  context: [{ title: 'a table', text: 'columns: id' }],
});
check('and to Google, whose shape is different again',
  viaGoogle.status === 200 && /^google says:/.test(viaGoogle.data?.answer ?? ''),
  (viaGoogle.data?.answer ?? '').slice(0, 40));
const sentGoogle = (await seen())[0];
check('that one carries the key in the query string',
  sentGoogle.auth === 'query', sentGoogle.auth);
check('names the model in the path rather than the body',
  sentGoogle.model === 'fake-pro', sentGoogle.model);
check('and puts the system prompt in systemInstruction',
  /delivery package/.test(sentGoogle.body.systemInstruction?.parts?.[0]?.text ?? ''),
  Object.keys(sentGoogle.body).join(','));
check('with roles spelled the way that shape spells them',
  (sentGoogle.body.contents ?? []).every((c) => ['user', 'model'].includes(c.role)),
  (sentGoogle.body.contents ?? []).map((c) => c.role).join(' '));

// ── history, in order ────────────────────────────────────────────────

await reset();
await as('harness.dev', 'POST', '/api/chat', {
  question: 'the third question', provider: 'openai', model: 'fake-large',
  history: [
    { role: 'user', text: 'the first question' },
    { role: 'assistant', text: 'the first answer' },
  ],
});
const withHistory = (await seen())[0].body.messages;
check('history arrives before the new question, in order',
  withHistory.map((m) => m.role).join(' ') === 'system user assistant user',
  withHistory.map((m) => m.role).join(' '));
check('and the newest question is last, not first',
  /the third question/.test(withHistory[withHistory.length - 1].content),
  withHistory[withHistory.length - 1].content.slice(-40));

// ── the caps, which exist because it is somebody's card ──────────────

await reset();
const huge = 'x'.repeat(30_000);
const capped = await as('harness.dev', 'POST', '/api/chat', {
  question: 'a question', provider: 'openai', model: 'fake-large',
  context: [
    { title: 'one', text: huge }, { title: 'two', text: huge },
    { title: 'three', text: huge },
  ],
});
check('more context than the cap is trimmed rather than sent',
  capped.data?.excerpts === 2 && capped.data?.droppedExcerpts === 1,
  `${capped.data?.excerpts} sent, ${capped.data?.droppedExcerpts} dropped`);
check('and the page is told, so it is not a silent truncation',
  capped.data?.droppedExcerpts > 0);

// ── when the provider says no ────────────────────────────────────────

const overQuota = await as('harness.dev', 'POST', '/api/chat',
  { question: 'anything', provider: 'openai', model: 'over-quota' });
check('a quota refusal comes back as 429', overQuota.status === 429, `${overQuota.status}`);
check('carrying what the provider actually said',
  /exceeded your current quota/.test(String(overQuota.data?.detail)),
  String(overQuota.data?.detail));

// ── a key is one person's ────────────────────────────────────────────

const theirs = await as('boss', 'GET', '/api/chat/providers');
check('another account sees none of it configured',
  (theirs.data?.providers ?? []).every((p) => !p.configured));
const borrowed = await as('boss', 'POST', '/api/chat',
  { question: 'anything', provider: 'openai', model: 'fake-large' });
check('and cannot ask on somebody else\'s key', borrowed.status === 428,
  `${borrowed.status}`);

// ── and forgetting one ───────────────────────────────────────────────

const dropped = await as('harness.dev', 'DELETE', '/api/settings/llm/google');
check('a key can be forgotten', dropped.status === 200, `${dropped.status}`);
const after = await as('harness.dev', 'GET', '/api/chat/providers');
check('and is gone, while the others stay',
  !after.data.providers.find((p) => p.id === 'google').configured
  && after.data.providers.find((p) => p.id === 'openai').configured);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
