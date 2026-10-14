/**
 * Asking about the package: everything the page and the side panel share.
 *
 * Lifted out of `chat.js` so the floating panel and the full page ask the same
 * way. They were always going to be two places asking one question, and two
 * copies of anything here is how the panel comes to give a different answer
 * from the page for the same words — which nobody would report as a bug,
 * because both answers look plausible. It holds:
 *
 *   gather()       what to send with a question, and the sources to cite
 *   starters()     three or four questions drawn from this package
 *   choose()       which provider and model, remembered once for both
 *   handThread()   the panel's conversation, handed to the full page
 *   renderAnswer() a model's Markdown as DOM, never as innerHTML
 *   sourceList()   the sources under an answer, as links into the viewer
 *
 * Nothing here talks to a model. It reads the package's own search index and
 * its contract prose, and picks what is worth paying to send.
 */

import * as auth from '/validation.js';

const el = (tag, cls, text) => {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = String(text);
  return node;
};

// ── the package's index ──────────────────────────────────────────────

let cached = null;

/** The package's search index, fetched once per page. */
export async function index() {
  if (cached) return cached;
  cached = (async () => {
    const res = await auth.apiFetch('/api/search');
    if (!res.ok) throw new Error(`could not read the package (the server answered ${res.status})`);
    return (await res.json()).entries ?? [];
  })();
  try { return await cached; } catch (error) { cached = null; throw error; }
}

/** The words worth matching on. Short ones and the obvious question words carry
 *  no signal and would match half the package. */
const STOP = new Set(['what', 'which', 'where', 'when', 'does', 'this', 'that', 'with',
  'from', 'into', 'have', 'has', 'the', 'and', 'for', 'are', 'how', 'why', 'who',
  'can', 'does', 'is', 'to', 'of', 'in', 'on', 'a', 'an', 'it', 'do', 'me', 'them',
  'they', 'their', 'there', 'between', 'about', 'show', 'tell']);

export function terms(question) {
  return [...new Set(String(question).toLowerCase().match(/[a-z0-9_.-]{3,}/g) ?? [])]
    .filter((w) => !STOP.has(w));
}

// ── the contract's own words ─────────────────────────────────────────

/**
 * The search index carries names and a line of terms, which is enough to find
 * the right operation and not enough to answer about it: "who may call it" is
 * in the contract's prose, not in its name. So for the best few hits on a
 * contract the page fetches that contract's detail (the same /api/detail the
 * viewer's reader uses) and sends the operation's or schema's own description.
 *
 * Per file and cached, and capped at three files a question, because one
 * contract's detail can run to megabytes and the point is a paragraph of it.
 */
const details = new Map();
function detailOf(file) {
  if (!details.has(file)) {
    details.set(file, auth.apiFetch(`/api/detail?file=${encodeURIComponent(file)}`)
      .then((r) => (r.ok ? r.json() : {}))
      .catch(() => ({})));
  }
  return details.get(file);
}

/** One contract node's prose, flattened and trimmed. */
function proseOf(entry, detail) {
  const key = entry.kind === 'operation' ? `op:${entry.file}#${entry.id}`
    : entry.kind === 'schema' ? `schema:${entry.file}#${entry.id}` : null;
  const node = key ? detail?.[key] : null;
  if (!node) return '';
  const bits = [];
  if (node.description) bits.push(String(node.description).trim());
  // The names a question about an operation usually turns on, said once: its
  // parameters and the shapes it answers with. Not their whole definitions.
  const params = (node.parameters ?? []).map((p) => p?.name).filter(Boolean);
  if (params.length) bits.push(`Parameters: ${params.join(', ')}`);
  const answers = Object.keys(node.responses ?? {});
  if (answers.length) bits.push(`Responses: ${answers.join(', ')}`);
  const props = Array.isArray(node.properties)
    ? node.properties.map((p) => p?.name).filter(Boolean)
    : Object.keys(node.properties ?? {});
  if (props.length) bits.push(`Properties: ${props.slice(0, 40).join(', ')}`);
  return bits.join('\n').slice(0, PROSE_CHARS);
}

// The service trims a question's context to 60,000 characters; this keeps a
// question well inside that (twelve excerpts of at most ~3,000), so what is
// trimmed there is a page that went wrong, not an ordinary question.
const PICKED = 12;
const PROSE_CHARS = 2400;
const PROSE_FILES = 3;

/**
 * What to send with a question, and what to cite under the answer.
 *
 * Scored rather than filtered: an entry matching three of the question's words
 * beats one matching one, which is the difference between the right table and
 * the first table alphabetically.
 *
 * @returns {Promise<{context: Array<{title, text}>, sources: Array<object>}>}
 *   `sources` keeps each entry's kind, id, name, file, line and hash, which is
 *   what a citation needs to link back into the viewer. These used to be
 *   dropped here, so the answer could not say where it came from.
 */
export async function gather(question) {
  const words = terms(question);
  if (!words.length) return { context: [], sources: [] };
  const entries = await index();
  const scored = [];
  for (const entry of entries) {
    const hay = `${entry.id} ${entry.name} ${entry.sub ?? ''} ${entry.terms ?? ''}`.toLowerCase();
    let score = 0;
    for (const word of words) if (hay.includes(word)) score += 1;
    // An exact id match is worth more than three loose word hits: somebody who
    // types POS-002 means that screen.
    if (words.includes(String(entry.id).toLowerCase())) score += 4;
    if (score) scored.push([score, entry]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  const picked = scored.slice(0, PICKED).map(([, e]) => e);

  const files = [...new Set(picked
    .filter((e) => (e.kind === 'operation' || e.kind === 'schema') && e.file)
    .map((e) => e.file))].slice(0, PROSE_FILES);
  const read = new Map(await Promise.all(files.map(async (f) => [f, await detailOf(f)])));

  const context = picked.map((entry) => {
    const prose = read.has(entry.file) ? proseOf(entry, read.get(entry.file)) : '';
    const lines = [
      `kind: ${entry.kind}`,
      `id: ${entry.id}`,
      entry.name && entry.name !== entry.id ? `name: ${entry.name}` : '',
      entry.sub ? `about: ${entry.sub}` : '',
      entry.file ? `file: ${entry.file}${entry.line ? `:${entry.line}` : ''}` : '',
      prose ? `\n${prose}` : '',
      entry.terms ? `\n${String(entry.terms).slice(0, 600)}` : '',
    ].filter(Boolean);
    return { title: `${entry.kind} ${entry.id}`, text: lines.join('\n') };
  });
  const sources = picked.map(({ kind, id, name, sub, file, line, hash, href }) =>
    ({ kind, id, name, sub, file, line, hash, href }));
  return { context, sources };
}

// ── where a source is drawn ──────────────────────────────────────────

/** The kinds the viewer opens from a `kind:id` hash (`openArtefactHash`). */
const HASHED = new Set(['screen', 'board', 'table', 'flow', 'machine', 'event', 'adr', 'platform']);

/**
 * A link into the viewer for one source, or to its file when the viewer has
 * no view of it. Contract nodes are keyed by file and name in the viewer, so
 * their search hash (`op:name`) is not enough and the full id is built here.
 */
export function sourceHref(s) {
  if (s.kind === 'operation' && s.file) return `/#${encodeURIComponent(`op:${s.file}#${s.id}`)}`;
  if (s.kind === 'schema' && s.file) return `/#${encodeURIComponent(`schema:${s.file}#${s.id}`)}`;
  if (s.kind === 'contract' && s.file) return `/#${encodeURIComponent(`file:${s.file}`)}`;
  const kind = String(s.hash ?? '').split(':')[0];
  if (s.hash && HASHED.has(kind)) return `/#${encodeURIComponent(s.hash)}`;
  if (s.href) return s.href;
  if (s.file) return auth.apiUrl(`/api/file?path=${encodeURIComponent(s.file)}`);
  return null;
}

const KIND_WORD = {
  operation: 'Operation', schema: 'Schema', contract: 'Contract', screen: 'Screen',
  flow: 'Journey', state: 'State model', event: 'Event', table: 'Table', adr: 'Decision',
  board: 'Board', platform: 'Platform', permission: 'Permission', sql: 'SQL', task: 'Plan item',
  page: 'Page',
};

/**
 * The sources an answer was given, as a list of links. "Sources" rather than
 * "citations": these are what the model was shown, and the answer may not use
 * every one. Saying it plainly keeps the list honest.
 */
export function sourceList(sources, { max = 8 } = {}) {
  if (!sources?.length) return null;
  const box = el('div', 'chat-sources');
  box.append(el('p', 'chat-sources-title', `Read from the package (${sources.length})`));
  const ul = el('ul', 'chat-sources-list');
  for (const s of sources.slice(0, max)) {
    const li = el('li');
    const href = sourceHref(s);
    const name = el(href ? 'a' : 'span', 'chat-source', s.id);
    if (href) name.href = href;
    li.append(el('span', 'chat-source-kind', KIND_WORD[s.kind] ?? s.kind), name);
    if (s.name && s.name !== s.id) li.append(el('span', 'chat-source-name', s.name));
    if (s.file && s.file !== s.id) li.append(el('span', 'chat-source-file', `${s.file}${s.line ? `:${s.line}` : ''}`));
    ul.append(li);
  }
  box.append(ul);
  if (sources.length > max) box.append(el('p', 'chat-sources-more', `and ${sources.length - max} more`));
  return box;
}

// ── questions to start from ──────────────────────────────────────────

/**
 * Three or four questions about *this* package, built from real names in its
 * index rather than written down: a fixed list named TICVAI's tables on every
 * project, and a question about a table another package does not have gets an
 * honest "the package does not say", which reads as the chat not working.
 *
 * Chosen to be the central things, so the question is worth asking: the table
 * with the most columns, the permission guarding the most operations, the
 * state model with the most to say, the first screen of the first platform.
 */
export async function starters() {
  const entries = await index();
  const out = [];
  const num = (s) => Number(/(\d+)/.exec(String(s ?? ''))?.[1] ?? 0);
  const most = (list, by) => list.reduce((best, e) => (by(e) > by(best) ? e : best), list[0]);

  const tables = entries.filter((e) => e.kind === 'table' && e.written !== false);
  if (tables.length) out.push(`Which operations write to ${most(tables, (e) => num(e.sub)).id}?`);

  const permissions = entries.filter((e) => e.kind === 'permission');
  if (permissions.length) {
    const p = most(permissions, (e) => num(e.sub));
    const op = String(p.terms ?? '').split(/\s+/).find(Boolean);
    out.push(op ? `Who may call ${op}, and which screens call it?` : `What does ${p.id} allow?`);
  }

  const states = entries.filter((e) => e.kind === 'state');
  if (states.length) {
    const m = most(states, (e) => String(e.terms ?? '').length);
    out.push(`What are the states of ${m.name || m.id}, and what moves it between them?`);
  }

  const screens = entries.filter((e) => e.kind === 'screen');
  if (screens.length) out.push(`What does ${screens[0].id} (${screens[0].name}) show, and what does it call?`);
  return out.slice(0, 4);
}

// ── which provider and model ─────────────────────────────────────────

/**
 * One remembered choice, for the page and the panel both. They kept it under
 * two keys (`adam-chat-pick` here, `adam-chat-model:<provider>` in the panel),
 * so choosing a model on the page left the panel asking a different one. The
 * panel's old keys are still read once, so nobody loses a choice to this.
 *
 * Per browser, not a server-side preference: two tabs on two packages may
 * reasonably want different ones.
 */
const PICK = 'adam-chat-pick';

export function remembered() {
  try { return JSON.parse(localStorage.getItem(PICK) ?? '{}') ?? {}; } catch { return {}; }
}

export function remember(provider, model) {
  try { localStorage.setItem(PICK, JSON.stringify({ provider, model })); } catch { /* fine */ }
}

/**
 * The provider and model to ask, from the providers the service lists.
 * The remembered provider while it still has a key, else the first with one.
 * The model: what was remembered for that provider, else what the service
 * suggests, else the first it lists. Never empty while a model is listed.
 */
export function choose(providers, { provider: wanted } = {}) {
  const last = remembered();
  const provider = providers.find((p) => p.id === wanted)
    ?? providers.find((p) => p.id === last.provider && p.configured)
    ?? providers.find((p) => p.configured)
    ?? providers.find((p) => p.id === last.provider)
    ?? providers[0] ?? null;
  if (!provider) return { provider: null, model: '' };
  let model = last.provider === provider.id ? last.model : '';
  if (!model) {
    try { model = localStorage.getItem(`adam-chat-model:${provider.id}`) ?? ''; } catch { /* fine */ }
  }
  return { provider, model: model || provider.suggested || provider.models?.[0] || '' };
}

// ── handing the panel's thread to the page ───────────────────────────

/**
 * "Open the full chat" carries the conversation across. Session storage,
 * because it is one tab's conversation being moved one page along, not
 * something to find again tomorrow; and taken once, so a reload of the page
 * later does not bring an old thread back.
 */
const THREAD = 'adam-chat-thread';

export function handThread(turns) {
  try { sessionStorage.setItem(THREAD, JSON.stringify(turns ?? [])); } catch { /* fine */ }
}

export function takeThread() {
  try {
    const raw = sessionStorage.getItem(THREAD);
    sessionStorage.removeItem(THREAD);
    const turns = JSON.parse(raw ?? '[]');
    return Array.isArray(turns) ? turns : [];
  } catch { return []; }
}

// ── an answer, as DOM ────────────────────────────────────────────────

/**
 * A model's Markdown, rendered without ever handing its text to innerHTML.
 *
 * The answer is somebody else's output and it quotes the package, which quotes
 * whoever wrote the package, so it is treated as text from end to end: every
 * node is made with createElement and filled with textContent. What it
 * understands is what answers use: headings, paragraphs, bulleted and numbered
 * lists, fenced code, inline code, bold, italic and links. A link goes only to
 * http(s) or to a path on this site; anything else stays as its words.
 */
export function renderAnswer(text) {
  const host = el('div', 'chat-md');
  const lines = String(text ?? '').replace(/\r\n/g, '\n').split('\n');
  let para = [];
  let list = null;

  const closePara = () => {
    if (!para.length) return;
    const p = el('p');
    inline(p, para.join(' '));
    host.append(p);
    para = [];
  };
  const closeList = () => { list = null; };

  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    if (/^\s*```/.test(raw)) {
      closePara(); closeList();
      const pre = el('pre', 'chat-code');
      const code = el('code');
      const body = [];
      i += 1;
      while (i < lines.length && !/^\s*```/.test(lines[i])) { body.push(lines[i]); i += 1; }
      code.textContent = body.join('\n');
      pre.append(code);
      host.append(pre);
      continue;
    }
    const head = /^\s{0,3}(#{1,6})\s+(.*)$/.exec(raw);
    if (head) {
      closePara(); closeList();
      // Never above h4 inside an answer: the page's own headings stay the page's.
      const h = el(`h${Math.min(head[1].length + 2, 6)}`, 'chat-md-head');
      inline(h, head[2].replace(/\s*#+\s*$/, ''));
      host.append(h);
      continue;
    }
    const bullet = /^\s*[-*+]\s+(.*)$/.exec(raw);
    const numbered = /^\s*(\d+)[.)]\s+(.*)$/.exec(raw);
    if (bullet || numbered) {
      closePara();
      const tag = numbered ? 'ol' : 'ul';
      if (!list || list.tagName.toLowerCase() !== tag) {
        list = el(tag);
        if (numbered && numbered[1] !== '1') list.start = Number(numbered[1]);
        host.append(list);
      }
      const li = el('li');
      inline(li, (bullet ? bullet[1] : numbered[2]));
      list.append(li);
      continue;
    }
    if (!raw.trim()) { closePara(); closeList(); continue; }
    // A line indented under a list item continues it.
    if (list && /^\s{2,}\S/.test(raw) && list.lastElementChild) {
      list.lastElementChild.append(' ');
      inline(list.lastElementChild, raw.trim());
      continue;
    }
    closeList();
    para.push(raw.trim());
  }
  closePara();
  return host;
}

const SAFE_HREF = /^(https?:\/\/|\/(?!\/))/i;

/** Inline Markdown into `node`, as text nodes and elements only. */
function inline(node, text) {
  // Code first, because nothing inside backticks is markup.
  const pattern = /(`[^`]+`)|(\*\*[^*]+\*\*|__[^_]+__)|(\*[^*\s][^*]*\*|_[^_\s][^_]*_)|(\[[^\]]+\]\([^)\s]+\))/g;
  let at = 0;
  for (const m of String(text).matchAll(pattern)) {
    if (m.index > at) node.append(String(text).slice(at, m.index));
    const token = m[0];
    if (m[1]) node.append(el('code', '', token.slice(1, -1)));
    else if (m[2]) { const b = el('strong'); inline(b, token.slice(2, -2)); node.append(b); }
    else if (m[3]) { const e = el('em'); inline(e, token.slice(1, -1)); node.append(e); }
    else if (m[4]) {
      const [, label, href] = /^\[([^\]]+)\]\(([^)\s]+)\)$/.exec(token);
      if (SAFE_HREF.test(href)) {
        const a = el('a', 'chat-link');
        a.href = href;
        if (/^https?:/i.test(href)) { a.target = '_blank'; a.rel = 'noopener noreferrer'; }
        inline(a, label);
        node.append(a);
      } else node.append(label);
    }
    at = m.index + token.length;
  }
  if (at < String(text).length) node.append(String(text).slice(at));
}
