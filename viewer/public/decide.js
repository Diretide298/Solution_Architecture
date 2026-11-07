/**
 * Decide: the change-request watcher's drafts, decided from a phone.
 *
 * PHONE-SPEC.md section 4. The watcher drafts on the server and never settles;
 * this page is where the lead reads a draft, asks about it, approves, changes
 * or rejects it, and then settles what he decided after seeing the dry run.
 *
 * The safety rules carried over from REVIEW.md:
 *   - a decision binds to the draft hash it was made on and to the mark it was
 *     made over (expected_mark, the request's mark_digest), and the API refuses
 *     (409) a decision whose draft moved or whose request was marked again
 *     meanwhile (on another device). This page never retries a 409 with a
 *     fresh hash or mark: the lead has to read it again and decide again;
 *   - nothing reaches a ticket before Settle, and Settle applies only the dry
 *     run the lead saw (its fingerprint), after a phone-lock check in the app
 *     or a plain confirm in a browser.
 *
 * Offline: the last list and the drafts already read are kept in
 * localStorage; a decision made offline waits in an outbox and is sent when
 * the phone is back online, still bound to the hash and the mark it was made
 * on, so a replay after a newer mark is refused and says so.
 *
 * A request with no draft (none yet, or its drafting failed) is never
 * decided here: it has no swipe, no Approve, no place in "Approve all that
 * need nobody", and it is not counted as waiting for a decision. It sits under
 * "Not drafted yet" with why, in plain words, and Draft again (the API's
 * redraft), which starts no Claude turn: the next hourly run drafts it.
 *
 * Only the System Architect decides (security.py DECIDERS, 6 November 2026).
 *
 * `?demo=1` runs against an in-page fake (realistic titles, invented drafts)
 * so the page can be seen before the API exists. `&app=1` adds a fake
 * window.AdamApp so the app-only parts can be seen too. `&scenario=failed` is
 * the server on 6 November: every request waiting, none drafted, the key
 * refused. `&scenario=stopped` is the watcher's folder kept with its job gone
 * (four undrafted requests left); `&scenario=unset` is no watcher at all (503).
 */
import { currentTheme, setTheme } from '/theme.js';
import * as auth from '/validation.js';

const params = new URLSearchParams(location.search);
const DEMO = params.get('demo') === '1';
const SCENARIO = params.get('scenario') ?? '';
const DECIDERS = ['owner'];
const POST_LIMIT = 4000;            // what ADAM takes in one resolution (CR-455)
const TICKET_URL = 'https://pms.softlabsgroup.in/work_packages/';
const UNDO_MS = 5000;
const CACHE_KEY = 'adam-decide-cache-v2';
const OUTBOX_KEY = 'adam-decide-outbox-v1';
const HINT_KEY = 'adam-decide-swiped';
const STATUSES = ['accepted', 'done', 'rejected', 'open'];

const $ = (id) => document.getElementById(id);
const wide = window.matchMedia('(min-width: 960px)');
const coarse = window.matchMedia('(pointer: coarse)');

// ── small DOM helpers ────────────────────────────────────────────────
function h(tag, props, ...kids) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(props ?? {})) {
    if (v == null || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else if (k.startsWith('on') && typeof v === 'function') n.addEventListener(k.slice(2), v);
    else n.setAttribute(k, v === true ? '' : String(v));
  }
  for (const kid of kids.flat(Infinity)) {
    if (kid == null || kid === false) continue;
    n.append(kid instanceof Node ? kid : String(kid));
  }
  return n;
}

const PATHS = {
  check: 'M5 12.5l4.2 4.2L19 7',
  x: 'M6 6l12 12M18 6L6 18',
  edit: 'M4 20h4L19 9l-4-4L4 16v4zM13.5 6.5l4 4',
  ask: 'M5 18.5V6.5A1.5 1.5 0 0 1 6.5 5h11A1.5 1.5 0 0 1 19 6.5v8a1.5 1.5 0 0 1-1.5 1.5H9l-4 2.5z',
  chevron: 'M6 9l6 6 6-6',
  open: 'M9 6l6 6-6 6',
  inbox: 'M4 13l2.5-7.5h11L20 13M4 13v5.5h16V13M4 13h4.5l1 2.5h5l1-2.5H20',
  cloud: 'M7 18h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 6 9.5 4.25 4.25 0 0 0 7 18zM4 4l16 16',
  alert: 'M12 8v5M12 16.5v.01M10.3 4.2 2.8 17.5A2 2 0 0 0 4.5 20.5h15a2 2 0 0 0 1.7-3L13.7 4.2a2 2 0 0 0-3.4 0z',
  lock: 'M7 11V8a5 5 0 0 1 10 0v3M6 11h12v9H6z',
  send: 'M5 12h13M13 6l6 6-6 6',
  clock: 'M12 7v5l3 2M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z',
  info: 'M12 11v5M12 8v.01M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z',
  redo: 'M4 12a8 8 0 1 0 2.34-5.66M4 4v4.5h4.5',
  external: 'M14 5h5v5M19 5l-8 8M18 14v5H5V6h5',
  search: 'M10.5 17a6.5 6.5 0 1 0 0-13 6.5 6.5 0 0 0 0 13zM20 20l-4.8-4.8',
};
function icon(name) {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  const p = document.createElementNS(ns, 'path');
  p.setAttribute('d', PATHS[name]);
  svg.append(p);
  return svg;
}

// Answers and drafts are plain text. Paragraphs on blank lines, `code` in
// backticks, and file:line citations as code so they read as places.
const CITE = /((?:[\w.-]+\/)*[\w.-]+\.(?:ya?ml|sql|md|py|mjs|js|ts|cs|json|csv|html)(?::\d+(?:-\d+)?)?)/g;
function rich(text) {
  const out = [];
  for (const para of String(text ?? '').trim().split(/\n\s*\n/)) {
    if (!para.trim()) continue;
    const p = h('p');
    p.style.whiteSpace = 'pre-line';
    for (const [i, part] of para.split(/`([^`]+)`/).entries()) {
      if (i % 2) { p.append(h('code', { text: part })); continue; }
      let last = 0;
      for (const m of part.matchAll(CITE)) {
        p.append(part.slice(last, m.index), h('code', { class: 'dc-cite', text: m[0] }));
        last = m.index + m[0].length;
      }
      p.append(part.slice(last));
    }
    out.push(p);
  }
  return out;
}

// ── time ─────────────────────────────────────────────────────────────
const MIN = 60_000;
const HOUR = 60 * MIN;
const DAY = 24 * HOUR;
function span(ms) {
  if (ms < MIN) return { short: 'now', long: 'just now' };
  if (ms < HOUR) { const n = Math.round(ms / MIN); return { short: `${n} min`, long: `${n} min` }; }
  if (ms < DAY) { const n = Math.round(ms / HOUR); return { short: `${n} h`, long: `${n} ${n === 1 ? 'hour' : 'hours'}` }; }
  const n = Math.round(ms / DAY);
  return { short: `${n} d`, long: `${n} ${n === 1 ? 'day' : 'days'}` };
}
const since = (iso) => (iso ? Date.now() - Date.parse(iso) : 0);
const ago = (iso) => {
  if (!iso) return 'never';
  const s = span(since(iso));
  return s.long === 'just now' ? 'just now' : `${s.long} ago`;
};
const clock = (iso) => (iso ? new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }) : '');
const usd = (n) => `$${Number(n ?? 0).toFixed(2)}`;
const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

// ── the shapes the API answers, made one shape here ──────────────────
function normMark(m) {
  if (!m) return null;
  if (typeof m === 'string') {
    const [word, ...rest] = m.split(':');
    const decision = word.trim().toLowerCase();
    if (!['approve', 'change', 'reject'].includes(decision)) return null;
    return { decision, note: rest.join(':').trim() };
  }
  return m.decision ? { ...m, decision: String(m.decision).toLowerCase() } : null;
}
function normRow(r) {
  return {
    cr: r.cr ?? r.number ?? r.id,
    title: r.title ?? '',
    verdict: r.verdict ?? '',
    klass: r.class ?? r.klass ?? '',
    blocking: r.blocking === true || r.blocking === 'yes',
    needs: String(r.needs ?? 'none').toLowerCase(),
    decision: normMark(r.decision ?? r.mark),
    ticket: r.ticket ? String(r.ticket) : '',
    developer: r.developer ?? '',
    raisedAt: r.raised_at ?? r.raisedAt ?? null,
    // The list carries each draft's hash, so a swipe binds to the draft the
    // row was read with even before the draft itself has been opened.
    hash: r.draft_hash ?? '',
    // The mark the row was read with: a decision carries it back, so one sent
    // after the request was marked again elsewhere is refused, not written over.
    markDigest: r.mark_digest ?? '',
    draftError: r.draft_error ?? '',
    // Why it has no draft, as the watcher said it (redacted by the API), and whether the watcher gave up on it.
    draftReason: r.draft_reason ?? r.draft_error ?? '',
    draftTries: Number(r.draft_tries ?? 0),
    gaveUp: Boolean(r.gave_up),
    redraftAskedAt: r.redraft_asked_at ?? '',
    draftedAt: r.drafted_at ?? '',
  };
}
/** A request with no draft to decide: no draft hash, or a drafting that failed. Never approved from here. */
const isUndrafted = (r) => Boolean(r) && (!r.hash || Boolean(r.draftError));
/** "Invalid API key" from "claude reported an error (exit 1): Invalid API key · Please run /login". */
function shortReason(why) {
  let s = String(why ?? '').replace(/^draft failed twice:[^(]*\((.*)\)$/i, '$1');
  s = s.replace(/^claude (?:reported an error|exited)[^:]*:\s*/i, '').split(' · ')[0].trim();
  return s.length > 90 ? `${s.slice(0, 88).trimEnd()}…` : s;
}
/** Why a request has no draft, in plain words, for the row and the request. */
function plainReason(r) {
  const why = String(r.draftReason || r.draftError || '');
  const w = why.toLowerCase();
  if (!why) {
    return r.redraftAskedAt ? 'You asked for it to be drafted again. The next hourly run drafts it.'
      : 'Not drafted yet. The next hourly run drafts it.';
  }
  if (/credit balance|billing/.test(w)) return 'The Anthropic account has run out of credit, so nothing could be drafted.';
  if (/api key|authentication|unauthori[sz]ed|\b401\b|\/login/.test(w)) return 'Claude refused the watcher\'s API key, so nothing could be drafted.';
  if (/not on path/.test(w)) return 'Claude Code is not installed for the watcher on the server.';
  if (/no worktree/.test(w)) return 'The watcher could not open the release it checks drafts against.';
  if (/took too long|timed? ?out|timeoutexpired/.test(w)) return 'The drafting turn took too long and was stopped.';
  if (/budget/.test(w)) return 'The drafting turn ran out of its budget before it answered.';
  if (/json block|no entry for it|not json|one object for/.test(w)) return 'The drafting turn answered without a draft the watcher could read.';
  return 'Drafting failed.';
}
function triesLine(r) {
  if (r.gaveUp) return 'Tried twice. It waits for Draft again.';
  if (r.draftError) return 'Tried once. The next hourly run tries again.';
  return '';
}
function proposedFrom(text) {
  const m = /```json\s*([\s\S]*?)```/.exec(text ?? '');
  if (!m) return null;
  try {
    const p = JSON.parse(m[1]);
    return p && (p.resolution || p.status || p.ref) ? p : null;
  } catch { return null; }
}
function normEntry(e) {
  if (e.role) {
    const lead = ['lead', 'user', 'question'].includes(e.role);
    return lead ? { question: e.text ?? '', at: e.at } : { answer: e.text ?? '', at: e.at, proposed: e.proposed ?? proposedFrom(e.text) };
  }
  const st = e.state ?? e.status;
  const failed = st === 'failed';
  const pending = st === 'asking' || st === 'pending' || st === 'running' || (!st && !e.answer && !e.error);
  return {
    id: e.id, question: e.question ?? '', answer: e.answer ?? '', at: e.at ?? e.asked_at,
    error: failed ? (e.error || 'No answer came back; ask again.') : (e.error ?? ''),
    pending: pending && !failed, proposed: e.proposal ?? e.proposed ?? proposedFrom(e.answer),
  };
}
function normDetail(d) {
  const draft = d.draft ?? {};
  let facts = d.facts ?? draft.facts ?? [];
  if (typeof facts === 'string') facts = [facts];
  // A facts line joins several facts with middle dots; one per row reads better.
  facts = facts.flatMap((f) => (typeof f === 'string' ? f.split(/\s+·\s+/) : [f])).filter(Boolean);
  const mark = normMark(d.mark) ?? normMark(d.decision);
  return {
    ...normRow(d),
    decision: mark,
    hash: d.draft_hash ?? d.draftHash ?? draft.hash ?? '',
    rec: draft.recommendation ?? '',
    resolution: draft.resolution ?? '',
    status: draft.status ?? d.status ?? '',
    ref: draft.ref ?? d.ref ?? '',
    question: draft.question ?? '',
    noDraft: !d.draft,
    // The developer's own request, as ADAM's export has it (the watcher keeps it in state.json).
    asked: {
      problem: d.request?.problem ?? '', evidence: d.request?.evidence ?? '', options: d.request?.options ?? '',
      recommendation: d.request?.recommendation ?? '', artefact: d.request?.artefact ?? '', kind: d.request?.kind ?? '',
    },
    misread: draft.misread ?? '',
    facts,
    answer: draft.answer ?? draft.full_answer ?? '',
    thread: (d.thread ?? []).map(normEntry),
  };
}

// ── the API ──────────────────────────────────────────────────────────
class ApiError extends Error {
  constructor(message, status, offline = false, reason = '') { super(message); this.status = status; this.offline = offline; this.reason = reason; }
}
async function http(path, { method = 'GET', body, keepalive = false } = {}) {
  let res;
  try {
    res = await fetch(`${auth.apiBase()}${path}`, {
      method, credentials: 'include', keepalive,
      headers: body === undefined ? { accept: 'application/json' } : { 'content-type': 'application/json', accept: 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  } catch {
    throw new ApiError('ADAM could not be reached.', 0, true);
  }
  let data = null;
  try { data = await res.json(); } catch { /* an empty body is fine */ }
  if (!res.ok) throw new ApiError(data?.detail ?? `ADAM answered ${res.status}.`, res.status, false, data?.reason ?? '');
  return data;
}
const enc = encodeURIComponent;
const realApi = {
  summary: (sinceIso) => http(`/api/watcher/summary${sinceIso ? `?since=${enc(sinceIso)}` : ''}`),
  requests: () => http('/api/watcher/requests'),
  request: (cr) => http(`/api/watcher/requests/${enc(cr)}`),
  decide: (cr, body, keepalive) => http(`/api/watcher/requests/${enc(cr)}/decision`, { method: 'POST', body, keepalive }),
  ask: (cr, question) => http(`/api/watcher/requests/${enc(cr)}/ask`, { method: 'POST', body: { question } }),
  preview: () => http('/api/watcher/settle/preview', { method: 'POST', body: {} }),
  apply: (fingerprint) => http('/api/watcher/settle/apply', { method: 'POST', body: { fingerprint } }),
  deviceToken: (device) => http('/api/watcher/device-token', { method: 'POST', body: { device } }),
  dropDeviceToken: (id) => http(`/api/watcher/device-token/${enc(id)}`, { method: 'DELETE' }),
  redraft: (cr) => http(`/api/watcher/requests/${enc(cr)}/redraft`, { method: 'POST', body: {} }),
  redraftFailed: () => http('/api/watcher/redraft', { method: 'POST', body: { all_failed: true } }),
  history: () => http('/api/watcher/history'),
  health: () => http('/api/watcher/health'),
};
const api = DEMO ? makeFake() : realApi;

// ── state ────────────────────────────────────────────────────────────
const S = {
  me: null,
  summary: null,
  rows: [],
  details: new Map(),
  view: 'inbox',
  open: null,
  changing: false,
  loading: true,
  fatal: null,          // {kind: 'setup'|'reach'|'permission', message}
  offline: !navigator.onLine,
  readAt: null,
  pending: new Map(),   // cr -> {body, timer, label}: inside the undo window
  outbox: loadJson(OUTBOX_KEY, []),
  refused: new Map(),   // cr -> why the API refused the decision
  asking: new Set(),
  watch: null,
  // the inbox's filter (all, blocking, lead, client, undrafted), developer and search
  filter: 'all',
  dev: '',
  query: '',
  history: null,        // {items, at} once read
  health: null,         // the health route's answer once read
  redrafting: new Set(),
};

function loadJson(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; }
}
function saveJson(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* full or denied: reading still works */ }
}
const saveOutbox = () => saveJson(OUTBOX_KEY, S.outbox);
function saveCache() {
  if (DEMO) return;
  saveJson(CACHE_KEY, { at: S.readAt, summary: S.summary, rows: S.rows, details: [...S.details], history: S.history, health: S.health });
}
function loadCache() {
  if (DEMO) return false;
  const c = loadJson(CACHE_KEY, null);
  if (!c?.rows) return false;
  S.rows = c.rows; S.summary = c.summary; S.readAt = c.at; S.details = new Map(c.details ?? []);
  S.history = c.history ?? null; S.health = c.health ?? null;
  return true;
}

const rowOf = (cr) => S.rows.find((r) => r.cr === cr);
const inOutbox = (cr) => S.outbox.some((o) => o.cr === cr);
const isDecided = (r) => Boolean(r.decision) || S.pending.has(r.cr) || inOutbox(r.cr);
const kindOf = (r) => (r.blocking ? 'blocking' : r.needs === 'lead' ? 'lead' : r.needs === 'client' ? 'client' : 'none');
const groupOf = (r) => (r.blocking ? 'blocking' : r.needs === 'lead' ? 'lead' : 'rest');
const byWait = (a, b) => Date.parse(a.raisedAt ?? 0) - Date.parse(b.raisedAt ?? 0);
/** The drafted requests waiting for a decision: what the inbox, its counts and every approve read. */
function inboxRows() {
  const order = { blocking: 0, lead: 1, rest: 2 };
  return S.rows.filter((r) => !isDecided(r) && !isUndrafted(r)).sort((a, b) => order[groupOf(a)] - order[groupOf(b)] || byWait(a, b));
}
/** The requests with no draft: failed ones first, blocking first, then by how long they have waited. */
function undraftedRows() {
  return S.rows.filter((r) => !isDecided(r) && isUndrafted(r))
    .sort((a, b) => Number(Boolean(b.draftError)) - Number(Boolean(a.draftError)) || Number(b.blocking) - Number(a.blocking) || byWait(a, b));
}
// The inbox's filters. Each count is taken with the search and the developer applied, so a count says what a tap shows.
const FILTERS = [
  { key: 'all', label: 'All', test: () => true },
  { key: 'blocking', label: 'Blocking', test: (r) => r.blocking },
  { key: 'lead', label: 'Needs you', test: (r) => !isUndrafted(r) && r.needs === 'lead' },
  { key: 'client', label: 'Needs the client', test: (r) => !isUndrafted(r) && r.needs === 'client' },
  { key: 'undrafted', label: 'Not drafted', test: (r) => isUndrafted(r) },
];
function searched(r) {
  if (S.dev && r.developer !== S.dev) return false;
  const q = S.query.trim().toLowerCase().replace(/^#/, '');
  if (!q) return true;
  return r.cr.toLowerCase().includes(q) || r.cr.replace(/^CR-/i, '') === q || r.title.toLowerCase().includes(q)
    || String(r.ticket).replace(/^#/, '').includes(q);
}
const filterOf = () => FILTERS.find((f) => f.key === S.filter) ?? FILTERS[0];
const shown = (r) => searched(r) && filterOf().test(r);
const narrowed = () => S.filter !== 'all' || Boolean(S.dev) || Boolean(S.query.trim());
/** The rows in the order the inbox lists them, as filtered: what j/k and the request's arrows step through. */
const navRows = () => [...inboxRows().filter(shown), ...undraftedRows().filter(shown)];
const trayRows = () => S.rows.filter(isDecided).sort(byWait);
const markOf = (r) => S.pending.get(r.cr)?.body ?? S.outbox.find((o) => o.cr === r.cr)?.body ?? r.decision;

// ── the app's plugins, used only when they are there ─────────────────
const App = () => window.AdamApp;
function haptic(kind) {
  const H = window.Capacitor?.Plugins?.Haptics;
  if (!H) return;
  try {
    if (kind === 'success') H.notification({ type: 'SUCCESS' });
    else H.impact({ style: 'LIGHT' });
  } catch { /* a missing haptic is never a reason to fail a decision */ }
}

// ── loading ──────────────────────────────────────────────────────────
async function boot() {
  if (DEMO && params.get('app') === '1') installFakeApp();
  bindChrome();
  if (!DEMO) {
    let state = null;
    try {
      state = await auth.authState();
    } catch {
      // Unreachable is not signed out: read what was kept, if anything.
      S.offline = true;
      if (loadCache()) { S.loading = false; renderAll(); return; }
      S.loading = false;
      S.fatal = { kind: 'reach' };
      renderAll();
      return;
    }
    if (!state.signedIn) {
      location.replace(`/login.html?next=${enc(location.pathname + location.search)}`);
      return;
    }
    S.me = state.account;
    if (!DECIDERS.includes(S.me?.role)) {
      S.loading = false;
      S.fatal = { kind: 'permission' };
      renderAll();
      return;
    }
  } else {
    S.me = { name: 'Chinmay Parab', role: 'owner' };
  }
  if (loadCache()) { S.loading = false; renderAll(); }
  await refresh();
  const cr = params.get('cr');
  if (cr && rowOf(cr)) openRequest(cr, { push: false });
  else openFromHash();
  window.addEventListener('hashchange', openFromHash);
  flushOutbox();
  setInterval(() => { if (document.visibilityState === 'visible') refresh({ quiet: true }); }, 60_000);
  setInterval(renderFresh, 30_000);
}

async function refresh({ quiet = false } = {}) {
  const btn = $('dc-refresh');
  btn.classList.add('is-spinning');
  btn.disabled = true;
  try {
    const [summary, list] = await Promise.all([api.summary(), api.requests()]);
    S.summary = summary;
    const rows = (Array.isArray(list) ? list : list?.items ?? list?.requests ?? []).map(normRow);
    // Arriving rows get a short entrance; the rest stay still.
    const known = new Set(S.rows.map((r) => r.cr));
    S.arrived = S.rows.length ? new Set(rows.filter((r) => !known.has(r.cr)).map((r) => r.cr)) : new Set();
    S.rows = rows;
    S.readAt = new Date().toISOString();
    S.offline = false;
    S.fatal = null;
    saveCache();
    prefetch();
    // Health and History are read beside the list, never in its way: a failure there leaves the list as it is.
    loadHealth();
    if (S.view === 'history' || S.history) loadHistory();
  } catch (e) {
    if (e.status === 401) { location.replace(`/login.html?next=${enc(location.pathname + location.search)}`); return; }
    if (e.status === 403) S.fatal = { kind: 'permission' };
    else if (e.status === 503) {
      S.fatal = { kind: 'setup', message: e.message };
      if (S.view === 'history') loadHistory();
    }
    else if (e.offline) {
      S.offline = true;
      if (!S.rows.length) S.fatal = { kind: 'reach' };
    } else if (!quiet) toast({ text: 'The list did not load.', sub: e.message, error: true, action: 'Try again', onAction: () => refresh() });
  } finally {
    S.loading = false;
    btn.classList.remove('is-spinning');
    btn.disabled = false;
    renderAll();
  }
}

// Drafts are read ahead, a few at a time, so a swipe has a hash to bind to
// and the phone has something to read when the signal goes.
let prefetching = false;
async function prefetch() {
  if (prefetching) return;
  prefetching = true;
  const todo = [...inboxRows(), ...undraftedRows()].filter((r) => !S.details.has(r.cr)).map((r) => r.cr);
  const worker = async () => {
    while (todo.length) {
      const cr = todo.shift();
      try { S.details.set(cr, normDetail(await api.request(cr))); } catch { /* read when opened */ }
    }
  };
  await Promise.all([worker(), worker(), worker()]);
  prefetching = false;
  saveCache();
}

async function loadHealth() {
  try {
    S.health = await api.health();
    saveCache();
    if (S.view === 'health') renderHealth();
    if (S.view === 'inbox') { renderBanner(); renderInbox(); }
  } catch { /* the summary still says the essentials */ }
}
async function loadHistory() {
  try {
    const got = await api.history();
    S.history = { items: got?.items ?? [], at: new Date().toISOString() };
    saveCache();
  } catch (e) {
    if (!S.history) S.history = { items: [], at: null, error: e.offline ? 'Offline, and no History is kept yet.' : e.message };
  }
  if (S.view === 'history') renderHistory();
}

/** Draft again: the request (or every failed one) is reset on the server so the next hourly run drafts it. No
 *  Claude turn starts now, and nothing is decided. */
async function redraft(crs, { all = false } = {}) {
  const list = all ? undraftedRows().filter((r) => r.draftError).map((r) => r.cr) : crs;
  if (!list.length) return;
  if (S.offline) { toast({ text: 'Drafting again needs a connection.', error: true }); return; }
  if (notRunning()) { toast({ text: 'Draft again is off.', sub: `${NOT_RUNNING}.`, error: true }); return; }
  for (const cr of list) S.redrafting.add(cr);
  renderAll();
  try {
    const got = all ? await api.redraftFailed() : await api.redraft(list[0]);
    const done = got?.redraft ?? [];
    const now = new Date().toISOString();
    for (const cr of done) {
      const r = rowOf(cr);
      if (r) Object.assign(r, { draftError: '', draftReason: '', gaveUp: false, draftTries: 0, redraftAskedAt: now });
    }
    saveCache();
    const next = S.health?.next_run_at ? ` at ${clock(S.health.next_run_at)}` : '';
    toast(done.length
      ? { text: done.length === 1 ? `${done[0]} will be drafted again` : `${plural(done.length, 'request')} will be drafted again`,
        sub: `At the next hourly run${next}. Nothing is decided until you read the draft.` }
      : { text: 'Nothing was asked to be drafted again.', sub: Object.values(got?.skipped ?? {})[0] ?? '', error: true });
  } catch (e) {
    toast({ text: 'Draft again did not go through.', sub: e.offline ? 'You are offline.' : e.message, error: true });
  } finally {
    for (const cr of list) S.redrafting.delete(cr);
    renderAll();
  }
}

async function detailOf(cr, { fresh = false } = {}) {
  if (!fresh && S.details.has(cr)) return S.details.get(cr);
  const d = normDetail(await api.request(cr));
  S.details.set(cr, d);
  const row = rowOf(cr);
  if (row && d.decision) row.decision = d.decision;
  saveCache();
  return d;
}

// ── deciding ─────────────────────────────────────────────────────────
const VERB = { approve: 'Approved', change: 'Changed', reject: 'Rejected' };

/** Marks a request, holds it for the undo window, then sends it. */
async function decide(cr, body, { quietToast = false, render = true } = {}) {
  if (isUndrafted(rowOf(cr))) {
    // A request with no draft has nothing to approve, change or reject (the API refuses it too: not-drafted).
    toast({ text: `${cr} has no draft to decide.`, sub: 'Draft it again; decide when the draft is in.', error: true });
    return false;
  }
  let hash = body.draft_hash || rowOf(cr)?.hash;
  // The mark read with the same reading as the hash: the open request's when it is open, else the row's.
  let mark = body.expected_mark ?? (S.details.get(cr)?.hash === hash ? S.details.get(cr)?.markDigest : rowOf(cr)?.markDigest);
  if (!hash || !mark) {
    try { const d = await detailOf(cr); hash = hash || d.hash; mark = d.hash === hash ? d.markDigest : ''; } catch {
      toast({ text: `${cr} needs its draft first.`, sub: 'Open it once you are online; a decision is bound to the draft it was made on.', error: true });
      return false;
    }
  }
  const full = { ...body, draft_hash: hash, expected_mark: mark ?? '' };
  const was = S.pending.get(cr);
  if (was) clearTimeout(was.timer);
  S.pending.set(cr, { body: full, timer: setTimeout(() => send(cr), UNDO_MS) });
  S.refused.delete(cr);
  haptic(full.decision === 'reject' ? 'reject' : 'approve');
  if (render) renderAll();
  if (!quietToast) {
    toast({
      text: `${VERB[full.decision]} ${cr}`,
      sub: full.decision === 'reject' ? 'It will be drafted again with your note.' : 'Settle it from Decided.',
      action: 'Undo', onAction: () => undo([cr]), clockMs: UNDO_MS,
    });
  }
  return true;
}

function undo(crs) {
  for (const cr of crs) {
    const p = S.pending.get(cr);
    if (!p) continue;
    clearTimeout(p.timer);
    S.pending.delete(cr);
    S.arrived = new Set([...(S.arrived ?? []), cr]);
  }
  hideToast();
  renderAll();
  announce(crs.length === 1 ? `${crs[0]} is back in the inbox.` : `${crs.length} requests are back in the inbox.`);
}

async function send(cr, { keepalive = false } = {}) {
  const p = S.pending.get(cr);
  if (!p) return;
  clearTimeout(p.timer);
  S.pending.delete(cr);
  if (S.offline || !navigator.onLine) {
    S.outbox = S.outbox.filter((o) => o.cr !== cr).concat({ cr, body: p.body, at: new Date().toISOString() });
    saveOutbox();
    renderAll();
    return;
  }
  try {
    const got = await api.decide(cr, p.body, keepalive);
    const row = rowOf(cr);
    if (row) row.decision = { decision: p.body.decision, note: p.body.note ?? '', resolution: p.body.resolution };
    newMark(cr, got);
    saveCache();
  } catch (e) {
    if (e.offline) {
      S.offline = true;
      S.outbox = S.outbox.concat({ cr, body: p.body, at: new Date().toISOString() });
      saveOutbox();
    } else refusedWith(cr, e);
  }
  renderAll();
}

/** The mark the API answered with becomes the one the next decision is made over. */
function newMark(cr, got) {
  if (!got?.mark_digest) return;
  const row = rowOf(cr);
  if (row) row.markDigest = got.mark_digest;
  const d = S.details.get(cr);
  if (d) d.markDigest = got.mark_digest;
}

function refusedWith(cr, e) {
  if (e.status === 409 && e.reason === 'not-drafted') {
    S.refused.set(cr, 'It has no draft any more, so there was nothing to decide. Draft it again and decide when the draft is in.');
    S.details.delete(cr);
    toast({ text: `${cr} was not kept: it has no draft.`, sub: 'Draft it again, then decide.', error: true, action: 'Open', onAction: () => openRequest(cr) });
  } else if (e.status === 409 && e.reason === 'mark-moved') {
    S.refused.set(cr, 'It was decided again somewhere else after you decided here, so this decision was not kept. Read it again and decide again.');
    S.details.delete(cr);
    toast({ text: `${cr} was not kept: it was decided again elsewhere.`, sub: 'A newer decision is there now. Read it again and decide again.', error: true, action: 'Open', onAction: () => openRequest(cr) });
  } else if (e.status === 409) {
    S.refused.set(cr, 'The draft changed after you decided, so the decision was not kept. Read the new draft and decide again.');
    S.details.delete(cr);
    toast({ text: `${cr} was not kept: its draft changed.`, sub: 'Read the new draft and decide again.', error: true, action: 'Open', onAction: () => openRequest(cr) });
  } else {
    S.refused.set(cr, `The decision was not kept: ${e.message}`);
    toast({ text: `${cr} was not kept.`, sub: e.message, error: true });
  }
}

async function flushOutbox() {
  if (!S.outbox.length || !navigator.onLine) return;
  const queue = S.outbox;
  S.outbox = [];
  saveOutbox();
  let sent = 0;
  for (const item of queue) {
    try {
      const got = await api.decide(item.cr, item.body);
      const row = rowOf(item.cr);
      if (row) row.decision = { decision: item.body.decision, note: item.body.note ?? '' };
      newMark(item.cr, got);
      sent++;
    } catch (e) {
      if (e.offline) { S.outbox.push(item); continue; }
      refusedWith(item.cr, e);
    }
  }
  saveOutbox();
  if (sent) toast({ text: `Sent ${plural(sent, 'decision')} made offline.` });
  renderAll();
}

// Leaving with decisions inside the undo window sends them now rather than
// losing them.
window.addEventListener('pagehide', () => { for (const cr of [...S.pending.keys()]) send(cr, { keepalive: true }); });
window.addEventListener('online', () => { S.offline = false; flushOutbox(); refresh({ quiet: true }); });
window.addEventListener('offline', () => { S.offline = true; renderAll(); });
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && S.readAt && since(S.readAt) > MIN) refresh({ quiet: true }); });

// ── rendering: the frame ─────────────────────────────────────────────
function renderAll() {
  renderFresh();
  renderBanner();
  renderCounts();
  if (S.view === 'inbox') renderInbox();
  if (S.view === 'tray') renderTray();
  if (S.view === 'history') renderHistory();
  if (S.view === 'health') renderHealth();
  if (S.open) renderRequest();
}
/** The watcher's drafting note, cut to what fits one banner line: what happened and the short reason. */
function bannerText(paused) {
  let m = /^Drafting failed: (.*?); (\d+) requests? waits? for a draft/.exec(paused);
  if (m) return `Drafting failed: ${shortReason(m[1])}. ${m[2]} waiting for a draft.`;
  m = /^Drafting is held: (\d+) requests? failed \d+ times \((.*)\) and waits?/.exec(paused);
  if (m) return `Drafting is held: ${m[1]} failed twice (${shortReason(m[2])}).`;
  const first = paused.split(/(?<=\.)\s/)[0];
  return first.length > 140 ? `${first.slice(0, 138).trimEnd()}…` : first;
}
/** The watcher does not run on this server: the API answers 503 (no watcher folder configured), or its folder is
 *  here and its job is not (the summary's `watching` is false). 6 November 2026: the lead stopped it; change
 *  requests are drafted on his machine. The page says so plainly, with no error and no stale pause. */
const NOT_RUNNING = 'The watcher is not running on this server';
const notRunning = () => S.fatal?.kind === 'setup' || S.summary?.watching === false;
function notRunningBlock() {
  return stateBlock({
    iconName: 'info', title: NOT_RUNNING,
    text: 'Change requests are drafted on the System Architect\'s machine, not here, so nothing new arrives on this page and nothing is drafted again. History still lists what was settled from Decide.',
    action: h('button', { class: 'dc-btn dc-btn-line', type: 'button', onclick: () => go('history') }, 'See History'),
  });
}
/** When the watcher's run now drafting started, or '' (the summary says it only while the run lock is held). */
const runningSince = () => (notRunning() ? '' : S.summary?.running_since || S.health?.running_since || '');

function renderFresh() {
  const sub = $('dc-fresh');
  sub.classList.toggle('is-off', S.offline);
  if (S.loading && !S.readAt) sub.textContent = 'Reading the watcher…';
  else if (S.offline) sub.textContent = S.readAt ? `Offline. List from ${clock(S.readAt)}` : 'Offline';
  else if (DEMO) sub.textContent = `Demo data. Updated ${ago(S.readAt)}`;
  else if (S.fatal?.kind === 'setup') sub.textContent = 'No watcher on this server';
  else sub.textContent = `Updated ${ago(S.readAt)}`;
}

function renderBanner() {
  const b = $('dc-banner');
  b.replaceChildren();
  b.classList.remove('is-info');
  if (S.offline && S.rows.length) {
    b.append(icon('cloud'), h('span', { text: S.outbox.length
      ? `Offline. ${plural(S.outbox.length, 'decision')} will send when you are back.`
      : 'Offline. You can read and decide; decisions send when you are back.' }));
  } else if (runningSince()) {
    // A run drafting now: what the last run said no longer stands.
    b.classList.add('is-info');
    b.append(icon('clock'), h('span', { text: `Drafting now (started ${clock(runningSince())}). New drafts arrive when the run ends.` }));
  } else if (S.summary?.paused && S.view !== 'health' && !notRunning()) {
    // One line here; the whole of it is on Health, a tap away.
    b.append(icon('alert'), h('span', { text: bannerText(S.summary.paused) }),
      h('button', { class: 'dc-banner-btn', type: 'button', onclick: () => go('health') }, 'Details'));
  } else if (DEMO && !S.fatal) {
    b.classList.add('is-info');
    b.append(icon('info'), h('span', { text: 'Demo: invented drafts on real titles. Nothing you do here is sent.' }));
  }
  b.hidden = !b.childNodes.length;
  // the wide layout's request pane sits under the banner, so it needs its height
  document.body.style.setProperty('--dc-banner-h', `${b.hidden ? 0 : b.offsetHeight}px`);
}

function renderCounts() {
  const ci = $('dc-count-inbox');
  const ct = $('dc-count-tray');
  const n = inboxRows().length;
  const t = trayRows().length;
  ci.hidden = !n || S.fatal;
  ci.textContent = n;
  const before = Number(ct.textContent || 0);
  ct.hidden = !t || S.fatal;
  ct.textContent = t;
  if (t > before) { ct.classList.remove('is-bump'); void ct.offsetWidth; ct.classList.add('is-bump'); }
  const tab = (go) => document.querySelector(`.dc-tab[data-go="${go}"]`);
  const u = undraftedRows().length;
  tab('inbox').setAttribute('aria-label', `Inbox, ${plural(n, 'request')} waiting for a decision${u ? `, ${u} not drafted yet` : ''}`);
  tab('tray').setAttribute('aria-label', `Decided, ${plural(t, 'request')} to settle`);
  const dot = $('dc-health-dot');
  const s = S.summary;
  const hot = s && !notRunning() && !runningSince() && (s.last_error || s.paused || (s.daily_cap_usd && s.spend_today_usd / s.daily_cap_usd >= 0.8));
  dot.hidden = !hot;
  dot.classList.toggle('is-warn', Boolean(s && !s.last_error));
  tab('health').setAttribute('aria-label', hot ? `Health, ${s.last_error ? 'the last run failed' : 'needs a look'}` : 'Health');
}

function go(view, { focus = true } = {}) {
  S.view = view;
  for (const v of document.querySelectorAll('.dc-view')) v.hidden = v.dataset.view !== view;
  for (const t of document.querySelectorAll('.dc-tab')) {
    if (t.dataset.go === view) t.setAttribute('aria-current', 'page');
    else t.removeAttribute('aria-current');
  }
  $('dc-shell').classList.toggle('is-single', view !== 'inbox');
  if (view !== 'inbox' && S.open && wide.matches) closeRequest({ pop: false, focusBack: false });
  if (view === 'history') loadHistory();
  if (view === 'health') loadHealth();
  renderAll();
  window.scrollTo({ top: 0 });
  if (focus) $('dc-main').focus({ preventScroll: true });
}

// ── rendering: states every view shares ──────────────────────────────
function stateBlock({ error = false, iconName, title, text, action }) {
  return h('div', { class: `dc-empty${error ? ' is-error' : ''}` },
    h('div', { class: 'dc-empty-icon' }, icon(iconName)),
    h('h3', { class: 'dc-empty-title', text: title }),
    text && h('p', { text }),
    action);
}
function fatalBlock() {
  const f = S.fatal;
  if (f.kind === 'permission') {
    return stateBlock({
      iconName: 'lock', title: 'This page is for the System Architect',
      text: `Only the System Architect decides change requests here.${S.me ? ` You are signed in as ${S.me.name ?? S.me.email}.` : ''} Change requests are open to you on their own page.`,
      action: h('a', { class: 'dc-btn dc-btn-line', href: '/changes.html' }, 'Go to Change requests'),
    });
  }
  if (f.kind === 'setup') return notRunningBlock();
  return stateBlock({
    error: true, iconName: 'cloud', title: 'ADAM cannot be reached',
    text: 'Nothing is kept on this phone yet, so there is nothing to read offline. Check the connection and try again.',
    action: h('button', { class: 'dc-btn dc-btn-line', type: 'button', onclick: () => refresh() }, 'Try again'),
  });
}

// ── rendering: the inbox ─────────────────────────────────────────────
function renderInbox() {
  const head = $('dc-headline');
  const line = $('dc-lede-line');
  const groups = $('dc-groups');
  if (S.loading && !S.rows.length) return;
  groups.setAttribute('aria-busy', 'false');
  if (S.fatal) {
    $('dc-tools').hidden = true;
    head.textContent = S.fatal.kind === 'permission' ? 'Decide' : S.fatal.kind === 'setup' ? 'Nothing waiting here' : 'No requests to show';
    line.textContent = '';
    groups.replaceChildren(fatalBlock());
    return;
  }
  const rows = inboxRows();
  const undrafted = undraftedRows();
  const failed = undrafted.filter((r) => r.draftError);
  renderTools(rows, undrafted);

  if (!rows.length && !undrafted.length) {
    head.textContent = 'Nothing waiting';
    line.textContent = '';
    const t = trayRows().length;
    if (notRunning() && !t) { groups.replaceChildren(notRunningBlock()); return; }
    groups.replaceChildren(stateBlock({
      iconName: 'check', title: t ? `${plural(t, 'decision')} ready to settle` : 'You are up to date',
      text: t
        ? 'Every waiting request has a decision. Settle them to post to their tickets.'
        : `The watcher last ran ${ago(S.summary?.last_run_at)} and checks every hour. New requests arrive here${App() ? ' and as a notification' : ''}.`,
      action: t ? h('button', { class: 'dc-btn dc-btn-primary', type: 'button', onclick: () => go('tray') }, 'Go to Decided') : null,
    }));
    return;
  }

  if (!rows.length) {
    // Nothing to decide yet: the headline never counts a request with no draft as waiting for a decision.
    head.replaceChildren(h('span', { text: `${undrafted.length} new` }), h('span', { class: 'is-quiet', text: ', none drafted yet' }));
    line.textContent = undraftedLine(undrafted, failed);
  } else {
    const blocking = rows.filter((r) => r.blocking).length;
    const lead = rows.filter((r) => r.needs === 'lead').length;
    const client = rows.filter((r) => r.needs === 'client').length;
    head.replaceChildren(
      blocking ? h('span', { text: `${blocking} blocking` }) : h('span', { text: `${rows.length} to decide` }),
      blocking ? h('span', { class: 'is-quiet', text: ` of ${rows.length}` }) : null,
    );
    const bits = [];
    if (lead) bits.push(`${lead} ${lead === 1 ? 'needs' : 'need'} you`);
    if (client) bits.push(`${client} ${client === 1 ? 'needs' : 'need'} the client`);
    const oldest = rows.reduce((a, r) => Math.max(a, since(r.raisedAt)), 0);
    line.textContent = [bits.join(' and '), oldest ? `The oldest has waited ${span(oldest).long}.` : '',
      undrafted.length ? `${undrafted.length} more ${undrafted.length === 1 ? 'is' : 'are'} not drafted yet.` : '',
      notRunning() ? `${NOT_RUNNING}: nothing new arrives here.` : '']
      .filter(Boolean).map((s, i) => (i === 0 && !s.endsWith('.') ? `${s}.` : s)).join(' ');
  }

  const vis = rows.filter(shown);
  const visU = undrafted.filter(shown);
  const parts = [];
  const nobody = rows.filter((r) => r.needs === 'none');
  if (nobody.length > 1 && S.filter !== 'undrafted') {
    parts.push(h('div', { class: 'dc-inline-action' },
      h('button', { class: 'dc-btn dc-btn-ghost', type: 'button', onclick: () => approveAllSheet() },
        icon('check'), `Approve the ${nobody.length} that need nobody`)));
  }
  const names = { blocking: 'Blocking', lead: 'Needs you', rest: 'The rest' };
  const notes = {
    blocking: 'A developer is held until these are decided.',
    lead: 'The draft asks you to choose.',
    rest: '',
  };
  let hinted = false;
  for (const g of ['blocking', 'lead', 'rest']) {
    const list = vis.filter((r) => groupOf(r) === g);
    if (!list.length) continue;
    const id = `dc-g-${g}`;
    const showHint = !hinted && coarse.matches && !localStorage.getItem(HINT_KEY);
    hinted = true;
    parts.push(h('section', { class: 'dc-group', 'aria-labelledby': id },
      h('div', { class: 'dc-group-head' },
        h('h3', { class: 'dc-group-title', id, text: names[g] }),
        h('span', { class: 'dc-group-count', text: plural(list.length, 'request') })),
      showHint
        ? h('p', { class: 'dc-group-note', text: 'Swipe a row right to approve it, left to open it.' })
        : notes[g] && h('p', { class: 'dc-group-note', text: notes[g] }),
      h('ul', { class: 'dc-list', role: 'list' }, list.map(rowEl))));
  }
  if (visU.length) {
    const visFailed = visU.filter((r) => r.draftError).length;
    const busyAll = failed.some((r) => S.redrafting.has(r.cr));
    parts.push(h('section', { class: 'dc-group dc-group-undrafted', 'aria-labelledby': 'dc-g-undrafted' },
      h('div', { class: 'dc-group-head' },
        h('h3', { class: 'dc-group-title', id: 'dc-g-undrafted', text: 'Not drafted yet' }),
        h('span', { class: 'dc-group-count', text: plural(visU.length, 'request') })),
      h('p', { class: 'dc-group-note', text: notRunning()
        ? `Nothing to decide until a draft is in. ${NOT_RUNNING}, so Draft again is off.`
        : visFailed
          ? 'Nothing to decide until a draft is in. Draft again asks the next hourly run to try; it starts nothing now.'
          : 'Nothing to decide until a draft is in. The next hourly run drafts these.' }),
      failed.length > 1 && h('div', { class: 'dc-inline-action' },
        h('button', { class: 'dc-btn dc-btn-ghost', type: 'button', 'data-redraft-all': '', disabled: busyAll || S.offline || notRunning() },
          icon('redo'), `Draft all ${failed.length} failed again`)),
      h('ul', { class: 'dc-list', role: 'list' }, visU.map(undraftedEl))));
  }
  if (!vis.length && !visU.length) {
    parts.push(stateBlock({
      iconName: 'inbox', title: 'Nothing matches',
      text: 'No waiting request fits this filter and search.',
      action: h('button', { class: 'dc-btn dc-btn-line', type: 'button', onclick: clearFilters }, 'Clear the filters'),
    }));
  }
  groups.replaceChildren(...parts);
  S.arrived = new Set();
}

function undraftedLine(undrafted, failed) {
  if (notRunning()) return `${NOT_RUNNING}, so nothing drafts them here.`;
  if (runningSince()) return `The watcher is drafting now (started ${clock(runningSince())}).`;
  const next = S.health?.next_run_at;
  if (failed.length) {
    const why = shortReason(failed[0].draftReason || failed[0].draftError);
    const held = failed.every((r) => r.gaveUp);
    return `Drafting failed: ${why}. ${held ? 'Fix the cause on the server, then Draft all again.' : `The next hourly run tries again${next ? ` at ${clock(next)}` : ''}.`}`;
  }
  return `The next hourly run drafts them${next ? `, at ${clock(next)}` : ''}.`;
}

function clearFilters() {
  S.filter = 'all';
  S.dev = '';
  S.query = '';
  $('dc-search').value = '';
  renderInbox();
}

/** The inbox's search, filters and developer: built once, so typing never loses its place; counts kept fresh. */
function renderTools(rows, undrafted) {
  const box = $('dc-tools');
  const all = [...rows, ...undrafted];
  box.hidden = all.length < 3 && !narrowed();
  const bar = $('dc-filters');
  if (!bar.childNodes.length) {
    bar.append(...FILTERS.map((f) => h('button', {
      class: 'dc-filter', type: 'button', 'data-filter': f.key, 'aria-pressed': 'false',
      onclick: () => { S.filter = S.filter === f.key && f.key !== 'all' ? 'all' : f.key; renderInbox(); },
    }, h('span', { text: f.label }), h('span', { class: 'dc-filter-n' }))));
  }
  for (const f of FILTERS) {
    const btn = bar.querySelector(`[data-filter="${f.key}"]`);
    const n = all.filter((r) => searched(r) && f.test(r)).length;
    btn.querySelector('.dc-filter-n').textContent = n;
    btn.setAttribute('aria-pressed', String(S.filter === f.key));
    btn.setAttribute('aria-label', `${f.label}, ${plural(n, 'request')}`);
    btn.hidden = f.key !== 'all' && !n && S.filter !== f.key;
    btn.classList.toggle('is-undrafted', f.key === 'undrafted');
  }
  const sel = $('dc-dev');
  const devs = [...new Set(all.map((r) => r.developer).filter(Boolean))].sort((a, b) => a.localeCompare(b));
  if (sel.dataset.devs !== devs.join('|')) {
    sel.replaceChildren(h('option', { value: '' }, 'Any developer'), ...devs.map((d) => h('option', { value: d }, d)));
    sel.dataset.devs = devs.join('|');
  }
  if (S.dev && !devs.includes(S.dev)) S.dev = '';
  sel.value = S.dev;
  const n = all.filter(shown).length;
  const said = $('dc-tools-line');
  said.replaceChildren(...(narrowed()
    ? [h('span', { text: `Showing ${n} of ${plural(all.length, 'request')}.` }),
      h('button', { class: 'dc-link-btn', type: 'button', onclick: clearFilters }, 'Clear')]
    : []));
  said.hidden = !narrowed();
}

function chipsFor(r) {
  const chips = [];
  if (r.blocking) chips.push(h('span', { class: 'dc-chip dc-chip-blocking', text: 'Blocking' }));
  if (r.needs === 'lead') chips.push(h('span', { class: 'dc-chip dc-chip-lead', text: 'Needs you' }));
  if (r.needs === 'client') chips.push(h('span', { class: 'dc-chip dc-chip-client', text: 'Needs the client' }));
  return chips;
}

function rowEl(r) {
  const w = since(r.raisedAt);
  const long = r.blocking ? w >= 4 * HOUR : w >= 2 * DAY;
  const li = h('li', {
    class: `dc-row${S.arrived?.has(r.cr) ? ' is-arriving' : ''}${S.open === r.cr ? ' is-open' : ''}`,
    'data-cr': r.cr, 'data-kind': kindOf(r),
  },
    h('div', { class: 'dc-row-under', 'aria-hidden': 'true' },
      h('span', { class: 'dc-under-approve' }, icon('check'), 'Approve'),
      h('span', { class: 'dc-under-open' }, 'Open', icon('open'))),
    h('div', { class: 'dc-row-face' },
      h('button', { class: 'dc-row-open', type: 'button', 'data-open': r.cr },
        h('span', { class: 'dc-row-top' },
          h('span', { class: 'dc-row-cr', text: r.cr }),
          r.raisedAt && h('span', { class: `dc-row-wait${long ? ' is-long' : ''}` },
            h('span', { class: 'dc-sr', text: 'waiting ' }), span(w).short)),
        h('span', { class: 'dc-row-title', text: r.title }),
        h('span', { class: 'dc-row-meta' },
          r.ticket && h('span', { class: 'is-ticket' }, h('span', { class: 'dc-sr', text: 'ticket ' }), `#${String(r.ticket).replace(/^#/, '')}`),
          r.developer && h('span', { text: r.developer })),
        h('span', { class: 'dc-row-chips' }, chipsFor(r))),
      h('button', { class: 'dc-row-approve', type: 'button', 'data-approve': r.cr, text: `Approve ${r.cr}` })));
  return li;
}

/** A request with no draft: why, in plain words, and Draft again. No swipe and nothing that approves. */
function undraftedEl(r) {
  const w = since(r.raisedAt);
  const busy = S.redrafting.has(r.cr);
  const sub = triesLine(r);
  return h('li', {
    class: `dc-row is-undrafted${S.open === r.cr ? ' is-open' : ''}`, 'data-cr': r.cr,
    'data-kind': r.draftError ? 'failed' : 'waiting', 'data-noswipe': '',
  },
    h('div', { class: 'dc-row-face' },
      h('button', { class: 'dc-row-open', type: 'button', 'data-open': r.cr },
        h('span', { class: 'dc-row-top' },
          h('span', { class: 'dc-row-cr', text: r.cr }),
          r.raisedAt && h('span', { class: 'dc-row-wait' }, h('span', { class: 'dc-sr', text: 'waiting ' }), span(w).short)),
        h('span', { class: 'dc-row-title', text: r.title }),
        h('span', { class: `dc-row-why${r.draftError ? ' is-failed' : ''}` }, icon(r.draftError ? 'alert' : 'clock'),
          h('span', null, plainReason(r), sub && h('span', { class: 'dc-row-why-sub', text: ` ${sub}` }))),
        h('span', { class: 'dc-row-meta' },
          r.ticket && h('span', { class: 'is-ticket' }, h('span', { class: 'dc-sr', text: 'ticket ' }), `#${String(r.ticket).replace(/^#/, '')}`),
          r.developer && h('span', { text: r.developer }),
          r.blocking && h('span', { class: 'dc-chip dc-chip-blocking', text: 'Blocking' }))),
      r.draftError && h('div', { class: 'dc-row-redraft-wrap' },
        h('button', {
          class: 'dc-btn dc-btn-line dc-row-redraft', type: 'button', 'data-redraft': r.cr, disabled: busy || S.offline || notRunning(),
          'aria-label': `Draft ${r.cr} again`, 'aria-describedby': notRunning() ? `dc-off-${r.cr}` : null,
        }, icon('redo'), busy ? 'Asking…' : 'Draft again'),
        notRunning() && h('span', { class: 'dc-row-off', id: `dc-off-${r.cr}`, text: `${NOT_RUNNING}.` }))));
}

// ── the swipe ────────────────────────────────────────────────────────
// Right approves (with an undo), left opens. Horizontal intent is decided
// after 10 px so a vertical scroll never becomes a swipe, and touches that
// start at the screen's edges are left to the system's back gesture. A row
// with no draft has no swipe at all: there is nothing to approve.
function bindSwipe(container) {
  let g = null;
  container.addEventListener('pointerdown', (e) => {
    const face = e.target.closest('.dc-row-face');
    if (!face || e.button !== 0 || S.fatal) return;
    if (e.pointerType !== 'mouse' && (e.clientX < 24 || e.clientX > innerWidth - 24)) return;
    const li = face.closest('.dc-row');
    if (li.hasAttribute('data-noswipe')) return;
    g = { li, face, id: e.pointerId, x0: e.clientX, y0: e.clientY, dx: 0, on: false, armed: false, w: li.offsetWidth };
  });
  container.addEventListener('pointermove', (e) => {
    if (!g || e.pointerId !== g.id) return;
    const dx = e.clientX - g.x0;
    const dy = e.clientY - g.y0;
    if (!g.on) {
      if (Math.abs(dy) > 10 && Math.abs(dy) > Math.abs(dx)) { g = null; return; }
      if (Math.abs(dx) < 10 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
      g.on = true;
      g.face.setPointerCapture(e.pointerId);
      g.li.classList.add('is-dragging');
    }
    const limit = g.w * 0.62;
    const eased = Math.abs(dx) > limit ? Math.sign(dx) * (limit + (Math.abs(dx) - limit) * 0.25) : dx;
    g.dx = dx;
    g.face.style.transform = `translateX(${eased}px)`;
    g.li.dataset.dir = dx > 0 ? 'right' : 'left';
    const armed = Math.abs(dx) > Math.min(120, g.w * 0.32);
    if (armed !== g.armed) { g.armed = armed; if (armed) g.li.dataset.armed = ''; else delete g.li.dataset.armed; }
  });
  const end = (e) => {
    if (!g || e.pointerId !== g.id) return;
    const { li, face, on, armed, dx } = g;
    g = null;
    if (!on) return;
    li.classList.remove('is-dragging');
    // the click that follows a drag is not a tap
    li.addEventListener('click', (ev) => { ev.stopPropagation(); ev.preventDefault(); }, { capture: true, once: true });
    setTimeout(() => { delete li.dataset.armed; }, 0);
    if (armed && dx > 0 && e.type === 'pointerup') {
      try { localStorage.setItem(HINT_KEY, '1'); } catch { /* fine */ }
      face.style.transform = `translateX(${li.offsetWidth}px)`;
      const cr = li.dataset.cr;
      setTimeout(async () => {
        li.classList.add('is-leaving');
        const ok = await decide(cr, { decision: 'approve', draft_hash: S.details.get(cr)?.hash }, { render: false });
        setTimeout(() => (ok ? renderAll() : resetFace(li, face)), 200);
      }, 140);
      return;
    }
    resetFace(li, face);
    if (armed && dx < 0 && e.type === 'pointerup') {
      try { localStorage.setItem(HINT_KEY, '1'); } catch { /* fine */ }
      openRequest(li.dataset.cr);
    }
  };
  container.addEventListener('pointerup', end);
  container.addEventListener('pointercancel', end);
}
function resetFace(li, face) {
  li.classList.remove('is-leaving');
  face.style.transform = '';
  setTimeout(() => { if (!face.style.transform) delete li.dataset.dir; }, 300);
}

// ── approve all that need nobody ─────────────────────────────────────
function approveAllSheet() {
  const list = inboxRows().filter((r) => r.needs === 'none');
  const picked = new Set(list.map((r) => r.cr));
  const btn = h('button', { class: 'dc-btn dc-btn-primary', type: 'button' });
  const say = () => { btn.textContent = picked.size ? `Approve ${picked.size}` : 'Pick at least one'; btn.disabled = !picked.size; };
  say();
  btn.addEventListener('click', async () => {
    const crs = [...picked];
    btn.classList.add('is-busy');
    // Each one binds to its own draft; a draft not read yet is read first.
    let made = 0;
    for (const cr of crs) if (await decide(cr, { decision: 'approve', draft_hash: S.details.get(cr)?.hash }, { quietToast: true, render: false })) made++;
    closeSheet();
    renderAll();
    toast({
      text: `Approved ${plural(made, 'request')}`, sub: 'Settle them from Decided.',
      action: 'Undo', onAction: () => undo(crs), clockMs: UNDO_MS,
    });
  });
  openSheet([
    h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: `Approve the ${list.length} that need nobody?` }),
    h('p', { class: 'dc-sheet-lede', text: 'Each is approved as drafted. Nothing is posted until you settle. Untick any you want to read first.' }),
    h('ul', { class: 'dc-pick' }, list.map((r) => h('li', null,
      h('label', null,
        h('input', { type: 'checkbox', checked: true, onchange: (e) => { if (e.target.checked) picked.add(r.cr); else picked.delete(r.cr); say(); } }),
        h('span', null,
          h('span', { class: 'dc-pick-title', text: r.title }),
          h('span', { class: 'dc-pick-sub', text: [r.cr, r.blocking ? 'blocking' : '', r.developer].filter(Boolean).join(', ') })))))),
    h('div', { class: 'dc-sheet-actions' },
      h('button', { class: 'dc-btn', type: 'button', onclick: () => closeSheet() }, 'Not now'),
      btn),
  ]);
}

// ── the request ──────────────────────────────────────────────────────
let returnFocus = null;

/** The request a `#CR-650` link names (the app opens /decide#CR-650 from a
 * notification), or '' when the hash names none. */
function hashCr() {
  const m = /^#(CR-[0-9]{1,7})$/i.exec(location.hash || '');
  return m ? m[1].toUpperCase() : '';
}

/** `#CR-n` becomes the page's own request view (`?cr=CR-n`). A hash that is
 * not a waiting request is left alone and opens nothing. */
function openFromHash() {
  const cr = hashCr();
  if (!cr || !rowOf(cr)) return;
  if (S.open === cr) return;
  openRequest(cr);
}

function openRequest(cr, { push = true } = {}) {
  if (!rowOf(cr)) return;
  if (S.view !== 'inbox' && wide.matches) go('inbox', { focus: false });
  const already = Boolean(S.open);
  S.open = cr;
  S.changing = false;
  if (!already) returnFocus = document.activeElement;
  if (push) {
    const u = new URL(location.href);
    u.searchParams.set('cr', cr);
    if (hashCr()) u.hash = '';          // the #CR-n that opened it is now ?cr=CR-n
    if (already) history.replaceState({ cr }, '', u);
    else history.pushState({ cr }, '', u);
  }
  const pane = $('dc-request');
  pane.hidden = false;
  document.body.classList.add('has-request');
  $('dc-shell').classList.add('has-request');
  if (!wide.matches) {
    for (const id of ['dc-main', 'dc-tabbar']) $(id).inert = true;
    requestAnimationFrame(() => pane.classList.add('is-open'));
  } else pane.classList.add('is-open');
  for (const li of document.querySelectorAll('.dc-row')) li.classList.toggle('is-open', li.dataset.cr === cr);
  renderRequest();
  $('dc-req-body').scrollTop = 0;
  $('dc-req-body').focus({ preventScroll: true });
  detailOf(cr, { fresh: !S.offline }).then(() => { if (S.open === cr) renderRequest(); }).catch((e) => {
    if (S.open !== cr) return;
    if (e.offline) { S.offline = true; renderAll(); } else renderRequest(e);
  });
}

function closeRequest({ pop = true, focusBack = true } = {}) {
  if (!S.open) return;
  const cr = S.open;
  S.open = null;
  S.changing = false;
  const pane = $('dc-request');
  pane.classList.remove('is-open');
  document.body.classList.remove('has-request');
  $('dc-shell').classList.remove('has-request');
  for (const id of ['dc-main', 'dc-tabbar']) $(id).inert = false;
  const done = () => { if (!S.open) pane.hidden = true; };
  if (wide.matches) done(); else setTimeout(done, 320);
  if (pop) {
    const u = new URL(location.href);
    u.searchParams.delete('cr');
    history.replaceState(null, '', u);
  }
  renderAll();
  if (focusBack) {
    const target = document.querySelector(`.dc-row-open[data-open="${cr}"]`) ?? returnFocus;
    (target?.isConnected ? target : $('dc-main')).focus({ preventScroll: false });
  }
}
window.addEventListener('popstate', (e) => {
  if (e.state?.cr && rowOf(e.state.cr)) openRequest(e.state.cr, { push: false });
  else if (S.open) closeRequest({ pop: false });
});

function step(dir) {
  const list = navRows();
  const i = list.findIndex((r) => r.cr === S.open);
  const next = list[i + dir] ?? (i < 0 ? list[0] : null);
  if (next) openRequest(next.cr);
}

/** After a decision in the request: a phone goes back to the list to watch
 *  the row leave; a wide screen moves straight to the next one to decide. */
function afterDecision(cr) {
  const list = inboxRows().filter(shown);
  if (wide.matches && list.length) { openRequest(list[0].cr); return; }
  if (wide.matches) { closeRequest(); return; }
  closeRequest();
  announce(`${cr} moved to Decided.`);
}

const ticketHref = (t) => `${TICKET_URL}${encodeURIComponent(String(t).replace(/^#/, ''))}`;
const longDate = (iso) => (iso ? new Date(iso).toLocaleString([], { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }) : '');
function ticketLink(t) {
  return h('a', { class: 'dc-ticket', href: ticketHref(t), target: '_blank', rel: 'noopener noreferrer' },
    `#${String(t).replace(/^#/, '')}`, icon('external'), h('span', { class: 'dc-sr', text: ' (opens OpenProject)' }));
}

function renderRequest(error) {
  const cr = S.open;
  const r = rowOf(cr);
  if (!r) { closeRequest(); return; }
  const d = S.details.get(cr);
  const body = $('dc-req-body');
  const actions = $('dc-actions');
  $('dc-req-code').textContent = cr;
  const list = navRows();
  const idx = list.findIndex((x) => x.cr === cr);
  $('dc-req-prev').disabled = idx <= 0;
  $('dc-req-next').disabled = idx < 0 ? !list.length : idx >= list.length - 1;

  const undrafted = isUndrafted(r);
  const mark = markOf(r);
  const parts = [];
  if (S.refused.has(cr)) parts.push(said('danger', 'alert', S.refused.get(cr)));
  else if (S.pending.has(cr)) parts.push(said('info', 'clock', `${VERB[mark.decision]}. Sending in a moment; Undo is in the message below.`));
  else if (inOutbox(cr)) parts.push(said('warn', 'cloud', `${VERB[mark.decision]} while offline. It sends when you are back online, bound to this draft.`));
  else if (mark) parts.push(said('info', 'check', `You ${VERB[mark.decision].toLowerCase()} this. It stays in Decided until you settle.${mark.note ? ` Your note: ${mark.note}` : ''}`));

  const w = since(r.raisedAt);
  parts.push(h('div', { class: 'dc-req-head' },
    h('div', { class: 'dc-req-chips' }, chipsFor(r), undrafted && h('span', { class: 'dc-chip dc-chip-undrafted', text: 'Not drafted' }),
      r.raisedAt && h('span', { class: 'dc-req-waited', text: `Waiting ${span(w).long}` })),
    h('h2', { class: 'dc-req-title', id: 'dc-req-title', text: r.title }),
    h('dl', { class: 'dc-req-meta' },
      r.ticket && h('div', null, h('dt', { text: 'Ticket' }), h('dd', null, ticketLink(r.ticket))),
      r.developer && h('div', null, h('dt', { text: 'Developer' }), h('dd', { text: r.developer })),
      r.raisedAt && h('div', null, h('dt', { text: 'Raised' }), h('dd', null, h('time', { datetime: r.raisedAt, text: longDate(r.raisedAt) }))),
      r.klass && r.klass !== 'none' && h('div', null, h('dt', { text: 'Class' }), h('dd', { text: r.klass })),
      r.verdict && h('div', null, h('dt', { text: 'Verdict' }), h('dd', { text: sentence(r.verdict) })))));

  if (!d) {
    parts.push(error
      ? stateBlock({ error: true, iconName: 'alert', title: 'The request did not load', text: error.message,
        action: h('button', { class: 'dc-btn dc-btn-line', type: 'button', onclick: () => openRequest(cr, { push: false }) }, 'Try again') })
      : h('div', { 'aria-busy': 'true' },
        h('span', { class: 'dc-skel', style: 'height:28px;width:90%;margin-bottom:10px' }),
        h('span', { class: 'dc-skel', style: 'height:28px;width:70%;margin-bottom:28px' }),
        h('span', { class: 'dc-skel', style: 'height:140px;width:100%' }),
        h('span', { class: 'dc-sr', text: 'Reading the draft' })));
    body.replaceChildren(...parts);
    if (undrafted) renderActions(cr, null, mark);
    else { actions.replaceChildren(); actions.hidden = true; }
    return;
  }

  if (undrafted || d.noDraft) {
    // No draft: why, what happens next, and the developer's own words. Nothing here decides.
    const why = r.draftReason || r.draftError;
    parts.push(h('section', { class: `dc-nodraft${r.draftError ? ' is-failed' : ''}`, 'aria-labelledby': 'dc-b-nodraft' },
      h('div', { class: 'dc-nodraft-icon' }, icon(r.draftError ? 'alert' : 'clock')),
      h('div', null,
        h('h3', { class: 'dc-nodraft-title', id: 'dc-b-nodraft', text: r.draftError ? 'Drafting failed' : 'Not drafted yet' }),
        h('p', { text: plainReason(r) }),
        triesLine(r) && h('p', { class: 'dc-nodraft-sub', text: triesLine(r) }),
        why && h('p', { class: 'dc-nodraft-raw' }, h('span', { class: 'dc-sr', text: 'What the watcher said: ' }), h('code', { text: why })),
        h('p', { class: 'dc-nodraft-sub', id: 'dc-nodraft-next', text: notRunning()
          ? `There is nothing to approve until a draft is in. ${NOT_RUNNING}, so Draft again is off.`
          : r.draftError
          ? 'There is nothing to approve until a draft is in. Draft again asks the next hourly run to draft it; it starts nothing now.'
          : `There is nothing to approve until a draft is in.${S.health?.next_run_at ? ` The run is due at ${clock(S.health.next_run_at)}.` : ''}` }))));
    parts.push(askedBlock(d));
    if (d.facts.length) parts.push(factsBlock(d));
    body.replaceChildren(...parts);
    renderActions(cr, d, mark);
    return;
  }

  parts.push(h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-rec' },
    h('h3', { class: 'dc-block-title', id: 'dc-b-rec', text: 'The watcher recommends' }),
    h('p', { class: 'dc-rec', text: d.rec || 'No recommendation in this draft.' }),
    d.question && h('p', { class: 'dc-rec-why', text: d.question })));

  const shownMark = mark?.decision === 'change' && mark.resolution ? mark : d;
  if (S.changing) parts.push(changeForm(d, mark));
  else {
    const text = shownMark.resolution || d.resolution || '';
    parts.push(h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-post' },
      h('h3', { class: 'dc-block-title', id: 'dc-b-post', text: shownMark === d ? 'What will be posted' : 'What will be posted, as you changed it' }),
      h('div', { class: 'dc-post-meta' },
        h('span', { class: 'dc-chip is-plain', text: `Status: ${shownMark.status || d.status || 'not set'}` }),
        (shownMark.ref || d.ref) && h('span', { class: 'dc-chip is-plain', text: `Release: ${shownMark.ref || d.ref}` })),
      h('p', { class: `dc-post${shownMark === d ? '' : ' is-changed'}`, text: text || 'Nothing is posted for this draft.' }),
      text && countLine(text)));
  }

  parts.push(askedBlock(d));
  if (d.facts.length) parts.push(factsBlock(d));
  const folds = [];
  if (d.misread) folds.push(fold('What the request misread', d.misread));
  if (d.answer) folds.push(fold('The agent\'s full answer', d.answer));
  if (folds.length) parts.push(h('section', { class: 'dc-block' }, folds));

  parts.push(askBlock(cr, d));
  body.replaceChildren(...parts);
  renderActions(cr, d, mark);
}

/** "1,284 of 4,000 characters", and a warning above ADAM's limit. */
function countLine(text, id) {
  const n = [...String(text)].length;
  const over = n > POST_LIMIT;
  const fix = id ? 'Shorten it before you save.' : 'Change it to shorten it before you settle.';
  return h('p', { class: `dc-count${over ? ' is-over' : ''}`, id, 'aria-live': id ? 'polite' : null },
    over ? icon('alert') : null,
    over ? `${n.toLocaleString()} characters: ${(n - POST_LIMIT).toLocaleString()} over the ${POST_LIMIT.toLocaleString()} ADAM takes. ${fix}`
      : `${n.toLocaleString()} of ${POST_LIMIT.toLocaleString()} characters`);
}

/** The developer's request in their own words: the problem open, the rest folded. */
function askedBlock(d) {
  const a = d.asked ?? {};
  const more = [['Evidence', a.evidence], ['Options', a.options], ['What they recommend', a.recommendation]].filter(([, v]) => v);
  if (!a.problem && !more.length) return null;
  return h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-asked' },
    h('h3', { class: 'dc-block-title', id: 'dc-b-asked', text: `What ${d.developer ? d.developer.split(' ')[0] : 'the developer'} asked` }),
    a.problem && h('blockquote', { class: 'dc-asked' }, rich(a.problem)),
    more.length > 0 && h('details', { class: 'dc-fold', style: 'margin-top:var(--ds-space-3)' },
      h('summary', null, h('span', { text: sentence(more.map(([k]) => k).join(', ').replace(/, ([^,]*)$/, ' and $1')) }), icon('chevron')),
      h('div', { class: 'dc-fold-body' }, more.map(([k, v]) => h('div', { class: 'dc-asked-part' }, h('h4', { text: k }), rich(v))))));
}

function factsBlock(d) {
  return h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-facts' },
    h('h3', { class: 'dc-block-title', id: 'dc-b-facts', text: 'Facts' }),
    h('dl', { class: 'dc-facts' }, d.facts.map((f) => {
      const text = typeof f === 'string' ? f : `${f.label}: ${f.value}`;
      const [k, ...v] = text.split(': ');
      return v.length && k.length <= 28
        ? h('div', { class: 'dc-fact' }, h('dt', { text: k }), h('dd', null, rich(v.join(': '))[0] ?? ''))
        : h('div', { class: 'dc-fact' }, h('dd', null, rich(text)[0] ?? ''));
    })));
}

const sentence = (s) => String(s).charAt(0).toUpperCase() + String(s).slice(1).toLowerCase();
function said(kind, iconName, text) {
  return h('div', { class: `dc-said${kind === 'warn' ? ' is-warn' : kind === 'danger' ? ' is-danger' : ''}`, role: kind === 'danger' ? 'alert' : null },
    icon(iconName), h('span', { text }));
}
function fold(title, text) {
  return h('details', { class: 'dc-fold' },
    h('summary', null, h('span', { text: title }), icon('chevron')),
    h('div', { class: 'dc-fold-body' }, rich(text)));
}

function renderActions(cr, d, mark) {
  const actions = $('dc-actions');
  actions.hidden = false;
  actions.classList.toggle('is-two', S.changing);
  actions.classList.remove('is-one');
  const r = rowOf(cr);
  if (isUndrafted(r)) {
    // Nothing to decide: one action, and only when the watcher has given up or failed on it.
    actions.classList.add('is-one');
    const busy = S.redrafting.has(cr);
    actions.replaceChildren(r.draftError
      ? h('button', {
        class: 'dc-act dc-act-primary', type: 'button', disabled: busy || S.offline || notRunning(), onclick: () => redraft([cr]),
        'aria-describedby': notRunning() ? 'dc-nodraft-next' : null,
      }, icon('redo'), busy ? 'Asking…' : S.offline ? 'Draft again needs a connection' : notRunning() ? 'Draft again is off here' : 'Draft again')
      : h('p', { class: 'dc-act-note', text: r.redraftAskedAt ? 'Asked. The next hourly run drafts it.' : 'The next hourly run drafts it.' }));
    return;
  }
  if (S.changing) {
    actions.replaceChildren(
      h('button', { class: 'dc-act', type: 'button', onclick: () => { S.changing = false; renderRequest(); } }, icon('x'), 'Cancel'),
      h('button', { class: 'dc-act dc-act-primary', type: 'button', onclick: () => saveChange(cr, d) }, icon('check'), 'Save the change'));
    return;
  }
  const approved = mark?.decision === 'approve';
  const noHash = !d.hash;
  actions.replaceChildren(
    h('button', { class: `dc-act is-reject${mark?.decision === 'reject' ? ' is-on' : ''}`, type: 'button', onclick: () => rejectSheet(cr, d) }, icon('x'), 'Reject'),
    h('button', { class: `dc-act${mark?.decision === 'change' ? ' is-on' : ''}`, type: 'button', disabled: noHash, onclick: () => { S.changing = true; renderRequest(); $('dc-change-text')?.focus(); } }, icon('edit'), 'Change'),
    h('button', { class: 'dc-act', type: 'button', onclick: () => { const c = $('dc-ask-text'); c?.scrollIntoView({ behavior: 'smooth', block: 'center' }); c?.focus({ preventScroll: true }); } }, icon('ask'), 'Ask'),
    h('button', {
      class: 'dc-act dc-act-primary', type: 'button', disabled: approved || noHash,
      onclick: async () => { if (await decide(cr, { decision: 'approve', draft_hash: d.hash })) afterDecision(cr); },
    }, icon('check'), approved ? 'Approved' : 'Approve'));
}

function changeForm(d, mark) {
  const draft = mark?.decision === 'change' ? mark : d;
  const area = h('textarea', { class: 'dc-textarea', id: 'dc-change-text', rows: 8, 'aria-describedby': 'dc-change-help dc-change-count' }, draft.resolution || d.resolution || '');
  let count = countLine(area.value, 'dc-change-count');
  area.addEventListener('input', () => { const next = countLine(area.value, 'dc-change-count'); count.replaceWith(next); count = next; });
  return h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-change' },
    h('h3', { class: 'dc-block-title', id: 'dc-b-change', text: 'Change what will be posted' }),
    h('div', { class: 'dc-field' },
      h('label', { class: 'dc-field-label', for: 'dc-change-text', text: 'Text to post' }),
      area,
      count,
      h('p', { class: 'dc-field-help', id: 'dc-change-help', text: 'Posted to the ticket word for word when you settle.' }),
      h('p', { class: 'dc-field-error', id: 'dc-change-error', hidden: true })),
    h('div', { class: 'dc-field-row' },
      h('div', { class: 'dc-field' },
        h('label', { class: 'dc-field-label', for: 'dc-change-status', text: 'Status' }),
        h('select', { class: 'dc-select', id: 'dc-change-status' },
          STATUSES.map((s) => h('option', { value: s, selected: (draft.status || d.status) === s }, s)))),
      h('div', { class: 'dc-field' },
        h('label', { class: 'dc-field-label', for: 'dc-change-ref', text: 'Release' }),
        h('input', { class: 'dc-input', id: 'dc-change-ref', value: draft.ref || d.ref || '', autocomplete: 'off', placeholder: 'r15' }))));
}

async function saveChange(cr, d) {
  const text = $('dc-change-text');
  const err = $('dc-change-error');
  const resolution = text.value.trim();
  const tooLong = [...resolution].length > POST_LIMIT - 100;
  if (!resolution || tooLong) {
    // The watcher keeps a resolution to 3,900 characters, under the 4,000 ADAM takes (cr-watch.py RESOLUTION_LIMIT).
    err.textContent = tooLong
      ? `Shorten it to ${(POST_LIMIT - 100).toLocaleString()} characters or fewer: the watcher keeps it under ADAM's ${POST_LIMIT.toLocaleString()}.`
      : 'Write the text to post, or press Cancel to keep the draft.';
    err.hidden = false;
    text.setAttribute('aria-invalid', 'true');
    text.setAttribute('aria-describedby', 'dc-change-help dc-change-error');
    text.focus();
    return;
  }
  const body = { decision: 'change', draft_hash: d.hash, resolution, status: $('dc-change-status').value, ref: $('dc-change-ref').value.trim() };
  if (await decide(cr, body)) { S.changing = false; afterDecision(cr); }
}

function rejectSheet(cr, d) {
  const note = h('textarea', { class: 'dc-textarea', id: 'dc-reject-note', rows: 4, 'aria-describedby': 'dc-reject-help', required: true });
  const err = h('p', { class: 'dc-field-error', id: 'dc-reject-error', hidden: true });
  const go = async () => {
    const v = note.value.trim();
    if (!v) {
      err.textContent = 'Say why, so the next draft can answer it.';
      err.hidden = false;
      note.setAttribute('aria-invalid', 'true');
      note.setAttribute('aria-describedby', 'dc-reject-help dc-reject-error');
      note.focus();
      return;
    }
    closeSheet({ restore: false });
    if (await decide(cr, { decision: 'reject', draft_hash: d.hash, note: v })) afterDecision(cr);
  };
  openSheet([
    h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: `Reject the draft for ${cr}?` }),
    h('p', { class: 'dc-sheet-lede', text: 'Nothing is settled. The next run drafts it again with your note.' }),
    h('div', { class: 'dc-field' },
      h('label', { class: 'dc-field-label', for: 'dc-reject-note', text: 'Why' }),
      note,
      h('p', { class: 'dc-field-help', id: 'dc-reject-help', text: 'For example: the grant belongs in the release migration, not a new one.' }),
      err),
    h('div', { class: 'dc-sheet-actions' },
      h('button', { class: 'dc-btn', type: 'button', onclick: () => closeSheet() }, 'Keep it'),
      h('button', { class: 'dc-btn dc-btn-danger', type: 'button', onclick: go }, 'Reject the draft')),
  ], note);
}

// ── asking ───────────────────────────────────────────────────────────
function askBlock(cr, d) {
  const entries = [];
  for (const e of d.thread) {
    if (e.question) entries.push(h('li', { class: 'dc-msg dc-msg-q' }, h('span', { class: 'dc-msg-who', text: 'You' }), rich(e.question)));
    if (e.pending) entries.push(h('li', { class: 'dc-msg dc-msg-a', 'aria-busy': 'true' }, h('span', { class: 'dc-msg-who', text: 'Claude' }), h('span', { class: 'dc-msg-wait', text: 'Reading the release to answer. This can take a few minutes.' })));
    else if (e.error) entries.push(h('li', { class: 'dc-msg dc-msg-a' }, h('span', { class: 'dc-msg-who', text: 'Claude' }), h('p', { class: 'dc-field-error', text: `No answer: ${e.error}` })));
    else if (e.answer) {
      const text = e.answer.replace(/```json[\s\S]*?```/, '').trim();
      entries.push(h('li', { class: 'dc-msg dc-msg-a' },
        h('span', { class: 'dc-msg-who', text: 'Claude' }), rich(text),
        e.proposed && h('button', {
          class: 'dc-btn dc-btn-line dc-msg-use', type: 'button',
          onclick: () => useAnswer(cr, d, e.proposed),
        }, icon('edit'), 'Use this answer')));
    }
  }
  const box = h('textarea', { class: 'dc-textarea', id: 'dc-ask-text', rows: 1, placeholder: 'Ask about this draft', 'aria-label': 'Your question' });
  box.addEventListener('input', () => { box.style.height = 'auto'; box.style.height = `${Math.min(160, box.scrollHeight)}px`; });
  const sendBtn = h('button', { class: 'dc-btn dc-btn-primary', type: 'button', 'aria-label': 'Send the question' }, icon('send'));
  sendBtn.addEventListener('click', () => ask(cr, box, sendBtn));
  return h('section', { class: 'dc-block', 'aria-labelledby': 'dc-b-ask' },
    h('h3', { class: 'dc-block-title', id: 'dc-b-ask', text: 'Ask about it' }),
    entries.length
      ? h('ol', { class: 'dc-thread', 'aria-live': 'polite' }, entries)
      : h('p', { class: 'dc-field-help', style: 'margin-bottom:12px', text: 'Claude reads the release, read-only, and answers with the files it used. Asking never changes your decision.' }),
    S.offline || notRunning()
      ? h('p', { class: 'dc-field-help', text: S.offline ? 'Asking needs a connection.' : `Asking needs the watcher. ${NOT_RUNNING}.` })
      : h('div', { class: 'dc-compose' }, box, sendBtn));
}

async function ask(cr, box, btn) {
  const q = box.value.trim();
  if (!q) { box.focus(); return; }
  btn.classList.add('is-busy');
  btn.disabled = true;
  try {
    const entry = await api.ask(cr, q);
    const d = S.details.get(cr);
    d.thread.push(entry ? normEntry({ question: q, ...entry, status: entry.status ?? 'pending' }) : { question: q, pending: true });
    renderRequest();
    $('dc-ask-text')?.scrollIntoView({ block: 'center' });
    pollThread(cr);
  } catch (e) {
    toast({ text: 'The question was not sent.', sub: e.offline ? 'You are offline.' : e.message, error: true });
    btn.classList.remove('is-busy');
    btn.disabled = false;
  }
}

function pollThread(cr) {
  if (S.asking.has(cr)) return;
  S.asking.add(cr);
  const started = Date.now();
  const tick = async () => {
    try {
      const d = await detailOf(cr, { fresh: true });
      if (!d.thread.some((e) => e.pending) || Date.now() - started > 10 * MIN) {
        S.asking.delete(cr);
        if (S.open === cr) { renderRequest(); announce('Claude answered.'); }
        return;
      }
    } catch { /* try again on the next tick */ }
    setTimeout(tick, 3000);
  };
  setTimeout(tick, 2500);
}

function useAnswer(cr, d, proposed) {
  S.changing = true;
  renderRequest();
  if (proposed.resolution) $('dc-change-text').value = proposed.resolution;
  if (proposed.status && STATUSES.includes(proposed.status)) $('dc-change-status').value = proposed.status;
  if (proposed.ref) $('dc-change-ref').value = proposed.ref;
  $('dc-change-text').focus();
  $('dc-change-text').scrollIntoView({ block: 'center' });
  announce('The answer is in the Change box. Save the change to use it.');
}

// ── the tray and Settle ──────────────────────────────────────────────
function renderTray() {
  const box = $('dc-tray');
  const line = $('dc-tray-line');
  if (S.fatal) { line.textContent = ''; box.replaceChildren(fatalBlock()); return; }
  const rows = trayRows();
  const waitingSend = rows.filter((r) => S.pending.has(r.cr) || inOutbox(r.cr)).length;
  if (!rows.length) {
    line.textContent = '';
    box.replaceChildren(stateBlock({
      iconName: 'inbox', title: 'Nothing decided yet',
      text: 'Approve, change or reject a request and it collects here. Nothing is posted until you settle.',
      action: inboxRows().length ? h('button', { class: 'dc-btn dc-btn-line', type: 'button', onclick: () => go('inbox') }, 'Go to the inbox') : null,
    }));
    return;
  }
  line.textContent = `${plural(rows.length, 'decision')} waiting to be settled.${waitingSend ? ` ${waitingSend} not sent yet.` : ''} Settling posts them to their tickets.`;
  const list = h('ul', { class: 'dc-list', role: 'list' }, rows.map((r) => {
    const m = markOf(r);
    const sending = S.pending.has(r.cr);
    const queued = inOutbox(r.cr);
    const note = m.decision === 'reject' ? m.note : m.decision === 'change' ? m.resolution : '';
    return h('li', { class: 'dc-row', 'data-kind': kindOf(r) },
      h('div', { class: 'dc-row-face' },
        h('button', { class: 'dc-row-open', type: 'button', onclick: () => { go('inbox', { focus: false }); openRequestFromTray(r.cr); } },
          h('span', { class: 'dc-row-top' },
            h('span', { class: 'dc-row-cr', text: r.cr }),
            h('span', { class: `dc-mark-label is-${m.decision}`, text: sending ? `${VERB[m.decision]}, sending` : queued ? `${VERB[m.decision]}, offline` : VERB[m.decision] })),
          h('span', { class: 'dc-row-title', text: r.title }),
          note && h('span', { class: 'dc-row-note', text: note })),
        sending && h('button', { class: 'dc-btn dc-btn-ghost', type: 'button', style: 'align-self:center;margin-right:8px', onclick: () => undo([r.cr]) }, 'Undo')));
  }));
  const settle = h('button', { class: 'dc-btn dc-btn-primary', type: 'button', onclick: startSettle },
    icon('send'), `Settle ${plural(rows.length, 'request')}…`);
  if (S.offline) { settle.disabled = true; settle.lastChild.textContent = 'Settling needs a connection'; }
  box.replaceChildren(list, h('div', { class: 'dc-settle-dock' }, settle));
}
function openRequestFromTray(cr) {
  // a decided request is still readable and can be decided again
  S.open = null;
  openRequest(cr);
}

async function startSettle() {
  for (const cr of [...S.pending.keys()]) await send(cr);
  if (S.outbox.length) await flushOutbox();
  const status = h('p', { class: 'dc-sheet-lede', text: 'Running the dry run. Nothing is posted.' });
  openSheet([h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: 'What settling will post' }), status, h('span', { class: 'dc-skel', style: 'height:120px' })]);
  let p;
  try { p = await api.preview(); } catch (e) {
    openSheet([
      h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: 'The dry run did not run' }),
      h('p', { class: 'dc-sheet-lede', text: e.offline ? 'You are offline. Settling needs ADAM.' : e.message }),
      h('div', { class: 'dc-sheet-actions' },
        h('button', { class: 'dc-btn', type: 'button', onclick: () => closeSheet() }, 'Close'),
        h('button', { class: 'dc-btn dc-btn-primary', type: 'button', onclick: startSettle }, 'Run it again')),
    ]);
    return;
  }
  const items = previewItems(p);
  const n = items.length;
  const btn = h('button', { class: 'dc-btn dc-btn-primary', type: 'button', disabled: !n }, n ? `Settle ${n}` : 'Nothing to settle');
  btn.addEventListener('click', () => applySettle(p, n, btn));
  openSheet([
    h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: n ? `Settle ${plural(n, 'request')}?` : 'Nothing to settle' }),
    h('p', { class: 'dc-sheet-lede', text: 'This is the dry run: nothing has been posted yet. Settling marks each request in ADAM and comments on its ticket. Mail stays off.' }),
    h('ul', { class: 'dc-preview' }, items.map((it) => h('li', null,
      h('span', { class: 'dc-preview-top' }, h('span', { text: it.cr }), h('span', { text: it.status })),
      it.ticket && h('span', { class: 'dc-preview-sub', text: `Tells ticket #${String(it.ticket).replace(/^#/, '')}` }),
      it.note && h('span', { class: 'dc-preview-sub', text: it.note })))),
    p.lines?.length && h('details', { class: 'dc-fold', style: 'margin-top:12px' },
      h('summary', null, h('span', { text: 'What the watcher printed' }), icon('chevron')),
      h('div', { class: 'dc-fold-body' }, h('pre', { class: 'dc-preview-raw', text: p.lines.join('\n') }))),
    h('div', { class: 'dc-sheet-actions' },
      h('button', { class: 'dc-btn', type: 'button', onclick: () => closeSheet() }, 'Not yet'),
      btn),
  ]);
}

function previewItems(p) {
  if (Array.isArray(p.items)) return p.items.map((it) => ({ cr: it.cr, status: it.status ?? '', ticket: it.ticket ?? '', note: it.note ?? '' }));
  const seen = new Map();
  for (const line of p.lines ?? []) {
    const m = /(CR-\d+)/.exec(line);
    if (!m || seen.has(m[1])) continue;
    const status = /\b(accepted|done|rejected|open)\b/.exec(line)?.[1] ?? '';
    const ticket = /#(\d{3,})/.exec(line)?.[1] ?? '';
    seen.set(m[1], { cr: m[1], status, ticket, note: '' });
  }
  return [...seen.values()];
}

async function applySettle(p, n, btn) {
  const reason = `Settle ${plural(n, 'change request')}`;
  let ok;
  if (App()?.unlock) {
    try { ok = await App().unlock(reason); } catch { ok = false; }
  } else ok = window.confirm(`${reason}? This posts to their tickets.`);
  if (!ok) return;
  btn.classList.add('is-busy');
  btn.disabled = true;
  try {
    const got = await api.apply(p.fingerprint);
    const done = Array.isArray(got?.settled) ? got.settled.length : n;
    if (got && got.applied === false) {
      // Nothing was posted: never told as a settle.
      btn.classList.remove('is-busy');
      btn.disabled = false;
      toast({ text: 'Nothing was settled.', sub: got.detail ?? 'No request was marked the way settling takes it.', error: true });
      return;
    }
    haptic('success');
    closeSheet();
    toast({ text: `Settled ${plural(done, 'request')}`, sub: 'Their tickets have been told.' });
    await refresh({ quiet: true });
    go('inbox');
  } catch (e) {
    btn.classList.remove('is-busy');
    if (e.status === 409) {
      openSheet([
        h('h2', { class: 'dc-sheet-title', id: 'dc-sheet-title', text: 'The decisions changed' }),
        h('p', { class: 'dc-sheet-lede', text: 'A decision was added or changed after this dry run, so nothing was settled. Run the dry run again to see what will be posted.' }),
        h('div', { class: 'dc-sheet-actions' },
          h('button', { class: 'dc-btn', type: 'button', onclick: () => closeSheet() }, 'Close'),
          h('button', { class: 'dc-btn dc-btn-primary', type: 'button', onclick: startSettle }, 'Run it again')),
      ]);
    } else {
      btn.disabled = false;
      toast({ text: 'Nothing was settled.', sub: e.offline ? 'You are offline.' : e.message, error: true });
    }
  }
}

// ── history ──────────────────────────────────────────────────────────
const DECIDED_AS = { approve: 'Approved', change: 'Changed', reject: 'Rejected' };
function renderHistory() {
  const box = $('dc-history');
  const line = $('dc-history-line');
  // History is ADAM's own record, so it reads whether or not the watcher runs here.
  if (S.fatal && S.fatal.kind === 'permission') { line.textContent = ''; box.replaceChildren(fatalBlock()); return; }
  if (!S.history) {
    line.textContent = 'Reading what was settled…';
    box.replaceChildren(h('ul', { class: 'dc-list', 'aria-hidden': 'true' },
      [0, 1, 2].map(() => h('li', { class: 'dc-row dc-row-skel' }, h('span'), h('span'), h('span')))));
    return;
  }
  const items = S.history.items ?? [];
  if (!items.length) {
    line.textContent = '';
    box.replaceChildren(stateBlock({
      iconName: 'inbox', title: S.history.error ? 'History did not load' : 'Nothing settled from here yet',
      text: S.history.error ?? 'Requests you settle from Decide are listed here, newest first, with what was posted and the ticket it told.',
    }));
    return;
  }
  const ok = items.filter((i) => !i.failed).length;
  line.textContent = `${plural(ok, 'request')} settled from Decide, newest first${items.length > ok ? `; ${items.length - ok} settle${items.length - ok === 1 ? '' : 's'} failed part way` : ''}.`;
  // Grouped by day, because "when" is the question History answers.
  const days = new Map();
  for (const it of items) {
    const key = it.at ? new Date(it.at).toLocaleDateString([], { weekday: 'long', day: 'numeric', month: 'long' }) : 'Undated';
    if (!days.has(key)) days.set(key, []);
    days.get(key).push(it);
  }
  const parts = [];
  for (const [day, list] of days) {
    parts.push(h('section', { class: 'dc-group' },
      h('div', { class: 'dc-group-head' }, h('h3', { class: 'dc-group-title', text: day }),
        h('span', { class: 'dc-group-count', text: plural(list.length, 'request') })),
      h('ul', { class: 'dc-list dc-history', role: 'list' }, list.map(historyEl))));
  }
  box.replaceChildren(...parts);
}
function historyEl(it) {
  const verb = it.failed ? 'Settle failed' : DECIDED_AS[it.decision] ?? 'Settled';
  const status = it.status ? sentence(it.status) : '';
  return h('li', { class: `dc-hist${it.failed ? ' is-failed' : ''}` },
    h('div', { class: 'dc-hist-top' },
      h('span', { class: 'dc-row-cr', text: it.cr }),
      h('span', { class: `dc-mark-label is-${it.failed ? 'reject' : it.decision || 'approve'}`, text: verb }),
      h('time', { class: 'dc-hist-at', datetime: it.at, text: clock(it.at) })),
    it.title && h('p', { class: 'dc-hist-title', text: it.title }),
    h('p', { class: 'dc-hist-meta' },
      status && h('span', null, it.failed ? 'Was settling as ' : 'Now ', h('b', { text: status.toLowerCase() })),
      it.ref && h('span', null, 'Release ', h('b', { text: it.ref })),
      it.ticket ? h('span', null, it.failed ? 'Ticket ' : 'Told ', ticketLink(it.ticket)) : h('span', { text: 'No ticket to tell' })),
    it.resolution && h('details', { class: 'dc-fold dc-hist-post' },
      h('summary', null, h('span', { text: 'What was posted' }), icon('chevron')),
      h('div', { class: 'dc-fold-body' }, h('p', { class: 'dc-post', text: it.resolution }))));
}

// ── health ───────────────────────────────────────────────────────────
function renderHealth() {
  const box = $('dc-health');
  const line = $('dc-health-line');
  const s = { ...(S.summary ?? {}), ...(S.health ?? {}) };
  const have = Boolean(S.summary || S.health);
  if (S.fatal && S.fatal.kind === 'permission') { line.textContent = ''; box.replaceChildren(fatalBlock()); return; }
  const cards = [];
  if (notRunning()) {
    line.textContent = `${NOT_RUNNING}.`;
    cards.push(h('div', { class: 'dc-card' },
      h('h3', { class: 'dc-card-title', text: 'The watcher' }),
      h('p', { class: 'dc-card-value', text: 'Not running here' }),
      h('p', { class: 'dc-card-note', text: 'Change requests are drafted on the System Architect\'s machine. Nothing drafts, spends or runs on this server, so there is no next run, no error and no pause to show.' }),
      have && s.last_run_at && h('p', { class: 'dc-card-note', text: `It last ran here ${ago(s.last_run_at)}, at ${longDate(s.last_run_at)}.` })));
  } else if (have) {
    const running = runningSince();
    const failed = Boolean(s.last_error);
    line.textContent = running ? `The watcher is drafting now. It started at ${clock(running)}.`
      : failed ? (/^Drafting failed/i.test(s.last_error) ? 'The watcher runs, but its drafting failed. Nothing new was drafted.' : 'The last run failed. The list may be out of date.')
        : s.paused ? 'The watcher runs, but drafting is held. The reason is below.'
          : 'The watcher is running and drafting.';
    const next = s.next_run_at;
    const pair = [];
    pair.push(h('div', { class: 'dc-card' },
      h('h3', { class: 'dc-card-title', text: running ? 'Drafting now' : 'Last run' }),
      h('p', { class: 'dc-card-value', text: running ? `Since ${clock(running)}` : ago(s.last_run_at) }),
      !running && s.last_run_at && h('p', { class: 'dc-card-note', text: `At ${clock(s.last_run_at)}.` })));
    pair.push(h('div', { class: 'dc-card' },
      h('h3', { class: 'dc-card-title', text: 'Next run' }),
      h('p', { class: 'dc-card-value', text: next ? (since(next) > -MIN ? 'Due now' : `In ${span(-since(next)).long}`) : 'Hourly' }),
      next && h('p', { class: 'dc-card-note', text: `At ${clock(next)}. Runs every hour.` })));
    cards.push(h('div', { class: 'dc-cards-pair' }, pair));
    if (s.paused && !running) {
      cards.push(h('div', { class: 'dc-card is-warn' },
        h('h3', { class: 'dc-card-title', text: 'Why drafting is held' }),
        h('p', { class: 'dc-card-text', text: s.paused })));
    }
    if (failed) {
      cards.push(h('div', { class: 'dc-card is-danger' },
        h('h3', { class: 'dc-card-title', text: 'The last error' }),
        h('p', { class: 'dc-card-text' }, h('code', { text: s.last_error })),
        s.draft_failed > 0 && h('div', { class: 'dc-card-actions' },
          h('button', { class: 'dc-btn dc-btn-line', type: 'button', disabled: S.offline, onclick: () => redraft([], { all: true }) },
            icon('redo'), `Draft the ${plural(s.draft_failed, 'failed request')} again`))));
    }
    const cap = Number(s.daily_cap_usd || 0);
    const spent = Number(s.spend_today_usd || 0);
    const held = Number(s.spend_held_usd || 0);
    const share = cap ? Math.min(1, spent / cap) : 0;
    const meter = h('div', { class: `dc-meter${share >= 1 ? ' is-danger' : share >= 0.8 ? ' is-warn' : ''}`, role: 'meter', 'aria-valuemin': 0, 'aria-valuemax': cap, 'aria-valuenow': spent, 'aria-label': 'Spend today against the daily cap' },
      h('span', { style: `transform:scaleX(${share})` }));
    const batch = Number(s.batch_usd || 10);
    cards.push(h('div', { class: 'dc-card' },
      h('h3', { class: 'dc-card-title', text: 'Spend today' }),
      h('p', { class: 'dc-card-value', text: cap ? `${usd(spent)} of ${usd(cap)}` : usd(spent) }),
      cap && meter,
      h('p', { class: 'dc-card-note', text: [
        held ? `${usd(held)} of it is held by turns still running and comes back when they end.` : '',
        cap ? `${usd(Math.max(0, cap - spent))} left today. A drafting batch needs ${usd(batch)} of room.` : '',
      ].filter(Boolean).join(' ') })));
    const runs = s.runs ?? [];
    if (runs.length) {
      cards.push(h('div', { class: 'dc-card' },
        h('h3', { class: 'dc-card-title', text: 'The last runs' }),
        h('ol', { class: 'dc-runs' }, runs.map((r) => h('li', { class: /failed|could not/.test(r.line) ? 'is-failed' : '' },
          h('time', { datetime: r.at, text: r.at ? `${new Date(r.at).toLocaleDateString([], { day: 'numeric', month: 'short' })}, ${clock(r.at)}` : '' }),
          h('span', { text: r.line }))))));
    }
  } else {
    line.textContent = S.offline ? 'Offline, and no reading of the watcher is kept yet.' : 'Reading the watcher…';
  }
  if (App()?.setWatch) cards.push(notifyCard());
  cards.push(h('div', { class: 'dc-card' },
    h('h3', { class: 'dc-card-title', id: 'dc-theme-label', text: 'Appearance' }),
    h('div', { class: 'dc-seg', role: 'group', 'aria-labelledby': 'dc-theme-label' },
      ['dark', 'light'].map((t) => h('button', {
        type: 'button', 'aria-pressed': String(currentTheme() === t),
        onclick: () => { setTheme(t); renderHealth(); },
      }, t === 'dark' ? 'Night' : 'Day')))));
  if (S.me) cards.push(h('p', { class: 'dc-card-note', style: 'padding:0 4px', text: `Signed in as ${S.me.name ?? S.me.email}${DEMO ? ' (demo)' : ''}.` }));
  box.replaceChildren(h('div', { class: 'dc-cards' }, cards));
}

function notifyCard() {
  const on = Boolean(S.watch?.on);
  const sw = h('button', { class: 'dc-switch', type: 'button', role: 'switch', 'aria-checked': String(on), 'aria-labelledby': 'dc-notify-label' });
  sw.addEventListener('click', async () => {
    sw.disabled = true;
    try {
      if (!on) {
        const device = navigator.userAgentData?.platform || 'Android phone';
        const t = await api.deviceToken(device);
        try {
          // The app's background check reads the summary from ADAM's API origin.
          await App().setWatch({ base: auth.apiBase(), token: t.token });
        } catch (e) {
          // The app did not take the token, so nothing holds it: revoke it now
          // rather than leave a live token nobody can use or turn off.
          await api.dropDeviceToken(t.id).catch(() => {});
          throw e;
        }
        try { localStorage.setItem('adam-decide-token-id', String(t.id)); } catch { /* fine */ }
        toast({ text: 'Notifications on', sub: 'Blocking requests notify at once; the rest at 19:00.' });
      } else {
        const id = localStorage.getItem('adam-decide-token-id');
        await App().setWatch({ base: auth.apiBase(), token: '' });
        if (id) await api.dropDeviceToken(id).catch(() => {});
        toast({ text: 'Notifications off' });
      }
      S.watch = await App().watchStatus();
    } catch (e) {
      toast({ text: 'Notifications did not change.', sub: e.message, error: true });
    }
    renderHealth();
  });
  return h('div', { class: 'dc-card' },
    h('div', { class: 'dc-switch-row' },
      h('div', null,
        h('h3', { class: 'dc-card-title', id: 'dc-notify-label', style: 'color:var(--ds-ink);font-size:var(--ds-text-md)', text: 'Notify me on this phone' }),
        h('p', { class: 'dc-card-note', style: 'margin:0', text: 'Checks every 15 minutes. Blocking requests notify at once; the rest come together at 19:00.' })),
      sw),
    S.watch?.lastCheck && h('p', { class: 'dc-card-note', text: `Last checked ${ago(S.watch.lastCheck)}.` }));
}

// ── the sheet ────────────────────────────────────────────────────────
let sheetReturn = null;
function openSheet(children, focusEl) {
  const sheet = $('dc-sheet');
  const scrim = $('dc-scrim');
  const wasOpen = !sheet.hidden;
  if (!wasOpen) sheetReturn = document.activeElement;
  $('dc-sheet-inner').replaceChildren(...children.filter(Boolean));
  sheet.hidden = false;
  scrim.hidden = false;
  document.body.classList.add('has-sheet');
  for (const id of ['dc-shell', 'dc-tabbar', 'dc-banner']) $(id).inert = true;
  document.querySelector('.dc-appbar').inert = true;
  requestAnimationFrame(() => { sheet.classList.add('is-open'); scrim.classList.add('is-open'); });
  const first = focusEl ?? sheet.querySelector('input, textarea, button:not([disabled])');
  setTimeout(() => first?.focus({ preventScroll: true }), wasOpen ? 0 : 60);
}
function closeSheet({ restore = true } = {}) {
  const sheet = $('dc-sheet');
  const scrim = $('dc-scrim');
  if (sheet.hidden) return;
  sheet.classList.remove('is-open');
  scrim.classList.remove('is-open');
  document.body.classList.remove('has-sheet');
  for (const id of ['dc-shell', 'dc-banner']) $(id).inert = false;
  $('dc-tabbar').inert = Boolean(S.open && !wide.matches);
  $('dc-main').inert = Boolean(S.open && !wide.matches);
  document.querySelector('.dc-appbar').inert = false;
  setTimeout(() => { if (!sheet.classList.contains('is-open')) { sheet.hidden = true; scrim.hidden = true; } }, 300);
  if (restore && sheetReturn?.isConnected) sheetReturn.focus({ preventScroll: true });
}
// The sheet keeps focus inside itself; the page behind it is inert.
$('dc-sheet').addEventListener('keydown', (e) => {
  if (e.key !== 'Tab') return;
  const f = [...$('dc-sheet').querySelectorAll('button:not([disabled]), input, textarea, select, summary, a[href]')].filter((n) => n.offsetParent);
  if (!f.length) return;
  if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f.at(-1).focus(); }
  else if (!e.shiftKey && document.activeElement === f.at(-1)) { e.preventDefault(); f[0].focus(); }
});
$('dc-scrim').addEventListener('click', () => closeSheet());
// Drag the sheet down to dismiss it.
(() => {
  let y0 = null;
  const sheet = $('dc-sheet');
  sheet.addEventListener('pointerdown', (e) => { if (e.target.closest('.dc-sheet-grip') || ($('dc-sheet-inner').scrollTop === 0 && !e.target.closest('input, textarea, button, label, select'))) y0 = e.clientY; });
  sheet.addEventListener('pointermove', (e) => { if (y0 == null || wide.matches) return; const dy = Math.max(0, e.clientY - y0); sheet.style.transform = dy ? `translateY(${dy}px)` : ''; });
  const up = (e) => { if (y0 == null) return; const dy = e.clientY - y0; y0 = null; sheet.style.transform = ''; if (dy > 110 && !wide.matches) closeSheet(); };
  sheet.addEventListener('pointerup', up);
  sheet.addEventListener('pointercancel', up);
})();

// ── the toast ────────────────────────────────────────────────────────
let toastTimer = null;
function toast({ text, sub, action, onAction, clockMs, error = false }) {
  const t = $('dc-toast');
  clearTimeout(toastTimer);
  const kids = [h('div', { class: 'dc-toast-text' }, text, sub && h('small', { text: sub }))];
  if (action) kids.push(h('button', { class: 'dc-toast-btn', type: 'button', onclick: () => { hideToast(); onAction?.(); } }, action));
  const bar = clockMs && !matchMedia('(prefers-reduced-motion: reduce)').matches ? h('span', { class: 'dc-toast-clock' }) : null;
  if (bar) kids.push(bar);
  t.replaceChildren(...kids);
  t.classList.toggle('is-error', error);
  t.hidden = false;
  requestAnimationFrame(() => {
    t.classList.add('is-open');
    if (bar) bar.animate([{ transform: 'scaleX(1)' }, { transform: 'scaleX(0)' }], { duration: clockMs, easing: 'linear', fill: 'forwards' });
  });
  toastTimer = setTimeout(hideToast, clockMs ?? (action ? 8000 : 4000));
}
function hideToast() {
  const t = $('dc-toast');
  clearTimeout(toastTimer);
  t.classList.remove('is-open');
  setTimeout(() => { if (!t.classList.contains('is-open')) t.hidden = true; }, 200);
}
// A polite word for a screen reader when something moved out of sight.
function announce(text) {
  const fresh = $('dc-fresh');
  const keep = fresh.textContent;
  fresh.textContent = text;
  setTimeout(() => { if (fresh.textContent === text) fresh.textContent = keep; renderFresh(); }, 2500);
}

// ── wiring ───────────────────────────────────────────────────────────
function bindChrome() {
  $('dc-refresh').addEventListener('click', () => refresh());
  for (const t of document.querySelectorAll('.dc-tab')) t.addEventListener('click', () => { if (S.open && !wide.matches) closeRequest({ focusBack: false }); go(t.dataset.go); });
  $('dc-req-back').addEventListener('click', () => (history.state?.cr ? history.back() : closeRequest()));
  $('dc-req-prev').addEventListener('click', () => step(-1));
  $('dc-req-next').addEventListener('click', () => step(1));
  const groups = $('dc-groups');
  groups.addEventListener('click', (e) => {
    const open = e.target.closest('[data-open]');
    if (open) { openRequest(open.dataset.open); return; }
    const again = e.target.closest('[data-redraft]');
    if (again) { redraft([again.dataset.redraft]); return; }
    if (e.target.closest('[data-redraft-all]')) { redraft([], { all: true }); return; }
    const ap = e.target.closest('[data-approve]');
    if (ap) decide(ap.dataset.approve, { decision: 'approve', draft_hash: S.details.get(ap.dataset.approve)?.hash }).then((ok) => ok && renderAll());
  });
  bindSwipe(groups);
  $('dc-search').addEventListener('input', (e) => { S.query = e.target.value; renderInbox(); });
  $('dc-dev').addEventListener('change', (e) => { S.dev = e.target.value; renderInbox(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (!$('dc-sheet').hidden) { closeSheet(); return; }
      if (S.changing) { S.changing = false; renderRequest(); return; }
      if (S.open) { closeRequest(); return; }
    }
    if (e.target.closest('input, textarea, select') || e.metaKey || e.ctrlKey || e.altKey || !$('dc-sheet').hidden) return;
    if (S.view !== 'inbox') return;
    const rows = [...document.querySelectorAll('#dc-groups .dc-row-open')];
    const at = rows.indexOf(document.activeElement);
    if (e.key === 'j' || e.key === 'k') {
      e.preventDefault();
      if (S.open && wide.matches) { step(e.key === 'j' ? 1 : -1); return; }
      const next = rows[Math.max(0, Math.min(rows.length - 1, at + (e.key === 'j' ? 1 : -1)))] ?? rows[0];
      next?.focus();
      return;
    }
    if (e.key === '/') { e.preventDefault(); $('dc-search').focus(); return; }
    if (e.key === 'a') {
      const cr = S.open ?? (at >= 0 ? rows[at].dataset.open : null);
      if (!cr) return;
      e.preventDefault();
      const d = S.details.get(cr);
      decide(cr, { decision: 'approve', draft_hash: d?.hash }).then((ok) => { if (!ok) return; if (S.open) afterDecision(cr); else { renderAll(); document.querySelectorAll('#dc-groups .dc-row-open')[Math.max(0, at)]?.focus(); } });
    }
  });
  wide.addEventListener('change', () => {
    for (const id of ['dc-main', 'dc-tabbar']) $(id).inert = Boolean(S.open && !wide.matches);
    renderAll();
  });
  if (App()?.watchStatus) App().watchStatus().then((w) => { S.watch = w; if (S.view === 'health') renderHealth(); }).catch(() => {});
}

// ── the demo: an in-page fake of section 2's API ─────────────────────
// Titles are the real ones from the 4 November review; every draft, answer
// and fact below is invented for the demo and says nothing about the tickets.
// The demo fake's device-token calls, readable by checks/decide-check.mjs (demo only).
const demoCalls = [];
if (DEMO) window.__decideDemoCalls = demoCalls;

function makeFake() {
  const now = Date.now();
  const at = (min) => new Date(now - min * MIN).toISOString();
  const D = [
    ['CR-602', 'The operations role cannot read catalogue.price_resolution_policy, so catalogue#variantPriceRecords fails in the operations host and createMerchandise (CR-559) answers 500', 'NOT FIXED', 'none', true, 'none', '30874', 'Pranay Shinde', 38,
      'Approve: grant the operations role read access to the policy table, and nothing else changes.',
      'Accepted. Build now: a forward tenant migration grants the operations role SELECT on catalogue.price_resolution_policy, guarded so a second run changes nothing. The price query keeps its rule; its declared reads add the table. Tests run as the operations role, so a missing grant fails them.'],
    ['CR-598', 'importVenueGeometry must answer 202 with a parsing job, but import_job has no outcome a parsing job can hold and nowhere to keep the parse options', 'NOT FIXED', 'Background jobs', true, 'none', '31567', 'Narayan Gaonkar', 3 * 60 + 10,
      'Approve: let a parsing job have no outcome yet, and keep the parse options on the job.',
      'Accepted. Build now: one forward migration lets a parsing import job have no outcome until the parse finishes, and adds a column for the parse options it was asked for. The worker reads them back by job id. Tests: a new import answers 202 while parsing; a finished job always has an outcome.'],
    ['CR-601', 'Marketing\'s message sender (#37203) cannot send: no email, SMS or push vendor is named, apiConfiguration has no shape, and the secret store cannot hand a credential to the sender', 'PARTLY FIXED', 'Stored forms for secrets, tokens and hashes', true, 'client', '37203', 'Hrushikant Patkar', 26 * 60,
      'Build the sender against one provider port now; the vendor adapters wait for the client to name each vendor.',
      'Accepted in part. Build now: the sender claims queued messages, tries providers in their configured order, records each attempt, and reads credentials only through the secret store. Test it with a fake adapter. The vendor adapters are a separate ticket once the client names each vendor.'],
    ['CR-603', 'createApprovalRequest: what a matched rule with no role holder answers, how a delegation enters the chain, and whether create publishes approval.requested', 'NOT FIXED', 'Undecided rules', true, 'none', '30848', 'Pranay Shinde', 5 * 60,
      'Approve: refuse when nobody can approve, write delegates beside their delegators, and publish on create.',
      'Accepted. Build now: a request whose rule leaves nobody to approve is refused with 422 and writes nothing. A delegate gets a row beside the delegator, and the two fill one place. A request raised at pending publishes approval.requested in the same transaction.'],
    ['CR-610', 'updateMerchandise cannot set isPublished though MerchandiseItem says it does, so an item saved unpublished can never go on sale; retail.merchandisePublished ignores isPublished', 'NOT FIXED', 'none', true, 'lead', '30876', 'Pranay Shinde', 90,
      'Choose: add isPublished to the update (A), or drop it from MerchandiseItem and publish another way (B). The draft recommends A.',
      'Accepted, option A. Build now: updateMerchandise takes an optional isPublished. A guest sees an item only when it is active and published; the event fires when that visibility changes. The approved screens do not change.'],
    ['CR-612', 'searchCatalogue: "on sale at the venue and channel" rests on a channel rule the owner has not confirmed, and isAvailable ("sold out") has no rule and no declared read', 'NOT FIXED', 'Read routes between modules', true, 'lead', '31004', 'Narayan Gaonkar', 7 * 60,
      'Confirm the channel rule the draft proposes, and say whether "sold out" reads live stock or the last snapshot.',
      'Accepted. Build now: a product is on sale at a venue and channel when its listing names both and its sale window is open. isAvailable reads the stock snapshot the catalogue already declares; no live read is added.'],
    ['CR-618', 'identity#sessionTimeout cannot tell when a session is idle: the package gives no idle timeout (no value, no setting), and the job reads only identity.session', 'NOT FIXED', 'none', true, 'client', '37277', 'Hrushikant Patkar', 2 * 24 * 60,
      'Ask the client for the idle timeout; until then, build the job against a setting with a placeholder of 30 minutes.',
      'Accepted. Build now: an idle-timeout setting per tenant, marked placeholder at 30 minutes until the client gives its value. The job ends sessions idle for longer than that.'],
    ['CR-634', 'addToWishlist / getWishlist: no source for the guest\'s venue or channel, an empty guest scope hides Catalogue\'s rows, and XDR-007\'s grants miss three tables the price rule reads', 'NOT FIXED', 'A public guest read of venue data names no venue', true, 'lead', '30705', 'Deep Khanvilkar', 55,
      'Choose where the guest\'s venue comes from: the request (A) or the guest\'s last booking (B). The draft recommends A.',
      'Accepted, option A. Build now: the wishlist routes take the venue and channel from the request, as the other guest reads do, and the missing grants are added in one forward migration.'],
    ['CR-637', 'SSO sign-in: SsoProtocol includes saml2, but start and callback are OAuth-shaped (code, state) and nothing says how a SAML response arrives or is verified', 'NOT FIXED', 'none', true, 'lead', '30729', 'Deep Khanvilkar', 20,
      'Choose: build SAML now with its own callback (A), or ship OIDC first and mark saml2 as later (B).',
      'Accepted, option B. Build now: OIDC sign-in as the contract describes. saml2 stays in the enum, refused with a clear problem type until a release adds its callback.'],
    ['CR-609', 'verifyGuestEmail: nothing issues the emailed link that mode confirm consumes, and confirm has no way to find its row', 'NOT FIXED', 'Stored forms for secrets, tokens and hashes', false, 'lead', '30676', 'Chinmay Patkar', 4 * 60,
      'Approve the issuing step the draft adds, or say if the link should come from the mail service instead.',
      'Accepted. Build now: mode send issues a single-use token, stores only its hash with an expiry, and emails the link. Mode confirm finds the row by the hash.'],
    ['CR-599', 'Venue map gaps: DWG/DXF/JSON uploads are not permitted, and no operation archives a map or opens a draft from a published one', 'NOT FIXED', 'none', false, 'lead', '31564', 'Narayan Gaonkar', 30 * 60,
      'Say which formats are in the first release; the draft keeps DWG out and adds DXF and JSON.',
      'Accepted. Build now: DXF and JSON uploads; DWG stays refused with a clear message. Add archiveVenueMap and openDraftFromPublished as the draft describes.'],
    ['CR-600', 'setPrices does not say whether its PUT replaces the list\'s prices or merges into them; its lineage names the wrong table; copyPriceList lists no 409', 'NOT FIXED', 'none', false, 'none', '31413', 'Narayan Gaonkar', 9 * 60,
      'Approve: PUT replaces the whole list, the lineage is corrected, and copyPriceList answers 409 on a name clash.',
      'Accepted. Build now: setPrices replaces every price on the list in one transaction. Fix the lineage to the price table. copyPriceList answers 409 when the new name is taken.'],
    ['CR-604', 'Homepage layout is keyed by templateKey, but tenant_config holds one layout and getHomepageLayout takes no key', 'NOT FIXED', 'none', false, 'none', '31046', 'Sanket Keluskar', 22 * 60,
      'Approve: one layout per tenant; templateKey records which template it came from.',
      'Accepted. Build now: a tenant has one homepage layout. templateKey is stored on it as the template it was made from, and getHomepageLayout stays without a key.'],
    ['CR-616', 'enrolMfaMethod qrCodeUri (CR-587): the account for a guest who has no email (registered by mobile only)', 'NOT FIXED', 'none', false, 'none', '30663', 'Sanket Keluskar', 3 * 24 * 60,
      'Approve: use the mobile number as the account label when there is no email.',
      'Accepted. Build now: the authenticator label is the guest\'s email, or their mobile number in international form when there is no email.'],
    ['CR-645', 'listPromoBlocks has no description: its order, which blocks it lists, and whether it pages are not said', 'NOT FIXED', 'none', false, 'none', '30941', 'Sanket Keluskar', 70,
      'Approve: newest first, live and scheduled blocks only, paged like the other lists.',
      'Accepted. Build now: listPromoBlocks lists live and scheduled blocks, newest first, with the usual page size and cursor.'],
    ['CR-646', 'Design change: WEB-014\'s deadline is a running clock beside the steps, and the lead line sits behind an info button', 'NOT FIXED', 'none', false, 'none', '31901', 'Chitrangi Mestry', 6 * 60,
      'Approve: record the design change; the wireframe and page notes follow.',
      'Accepted. Recorded as a design change. The wireframe and the page notes are updated to match what was built.'],
    ['CR-635', 'CR-521\'s identity#subjectRecords check cannot run: Marketing is in the operations host, whose role has no SELECT on pii.subject', 'NOT A PROBLEM', 'Row security fits its callers', false, 'none', '31168', 'Sanket Keluskar', 12 * 60,
      'Close as not a problem: the read goes through Identity\'s own route, which already holds the grant.',
      'Done, not a problem. Marketing reaches the subject through Identity\'s in-process route, which runs with Identity\'s grant; no new grant is needed.'],
  ];
  const rows = D.map(([cr, title, verdict, klass, blocking, needs, ticket, developer, mins]) => ({
    cr, title, verdict, class: klass, blocking, needs, decision: '', ticket, developer, raised_at: at(mins),
  }));
  // one already decided, so the tray has something in it
  rows.push({ cr: 'CR-605', title: 'No storage for the landing-page templates TICVAI provides', verdict: 'PARTLY FIXED', class: 'Contract against storage', blocking: true, needs: 'none', decision: 'approve', ticket: '31045', developer: 'Sanket Keluskar', raised_at: at(4 * 60) });
  // Requests the watcher could not draft (6 November 2026: the server's API key was refused). Invented for the demo.
  const KEY = 'claude reported an error (exit 1): Invalid API key · Please run /login';
  const FAILED = [
    ['CR-651', 'getSeatMap answers 500 when a venue map has a section with no rows: the contract says an empty section is allowed', true, '31588', 'Narayan Gaonkar', 50, 2, KEY],
    ['CR-652', 'Refund approvals: the approval matrix has no level for refunds over the venue limit, so createRefund cannot route them', true, '30851', 'Pranay Shinde', 75, 2, KEY],
    ['CR-653', 'listOrders pages by offset but the contract promises a cursor; the mobile client already sends one', false, '31420', 'Sanket Keluskar', 95, 1, 'the drafting turn took too long and was stopped'],
    ['CR-654', 'Loyalty tiers: tier_rule has no column for the qualifying period the screen shows', false, '37290', 'Hrushikant Patkar', 8, 0, ''],
  ];
  for (const [cr, title, blocking, ticket, developer, mins, tries, why] of FAILED) {
    rows.push({ cr, title, verdict: '', class: '', blocking, needs: '', decision: '', ticket, developer, raised_at: at(mins),
      undrafted: true, draft_tries: tries, draft_reason: why,
      draft_error: tries >= 2 ? `draft failed twice: draft it again from Decide or with cr-watch.py redraft, or answer by hand (${why})` : why });
  }
  if (SCENARIO === 'failed') {
    // The server on 6 November: every request waiting, none drafted, the key refused at every turn.
    for (const r of rows) {
      if (r.decision || r.undrafted) continue;
      Object.assign(r, { undrafted: true, verdict: '', class: '', needs: '', draft_tries: 2, draft_reason: KEY,
        draft_error: `draft failed twice: draft it again from Decide or with cr-watch.py redraft, or answer by hand (${KEY})` });
    }
    rows.splice(rows.findIndex((r) => r.cr === 'CR-605'), 1);
  }
  if (SCENARIO === 'stopped') {
    // The job deleted and its env file gone: only the requests it never drafted are left in its folder.
    for (let i = rows.length - 1; i >= 0; i--) if (!rows[i].undrafted) rows.splice(i, 1);
  }
  const unset = () => {
    if (SCENARIO === 'unset') throw new ApiError('The watcher is not set up on this server.', 503);
  };
  const listed = (r) => ({ ...r, draft_hash: r.undrafted ? '' : hashOf(r.cr), mark_digest: 'demo',
    gave_up: Boolean(r.undrafted && r.draft_tries >= 2) });
  const info = Object.fromEntries(D.map((d) => [d[0], d]));
  const threads = {};
  const hashes = {};
  const hashOf = (cr) => (hashes[cr] ??= (cr.replace(/\D/g, '') * 2654435761 % 0xffffffffffff).toString(16).padStart(12, '0'));
  const wait = (ms = 260 + Math.random() * 240) => new Promise((r) => setTimeout(r, ms));
  const find = (cr) => rows.find((r) => r.cr === cr);
  let fingerprint = 0;
  const detail = (cr) => {
    const r = find(cr);
    const d = info[cr];
    const rec = d?.[9] ?? 'Approve as drafted.';
    const post = d?.[10] ?? 'Accepted. Build now as the draft describes.';
    const request = {
      problem: `${r.title}. I hit this while building ticket #${r.ticket}: the contract and the storage disagree, and I cannot finish the operation without one of them changing.`,
      evidence: `The integration test fails on the first call; the log shows the read refused. Ticket #${r.ticket} has the trace.`,
      options: 'A: change the storage to match the contract. B: change the contract to match the storage.',
      recommendation: 'A, because the screens already assume the contract.',
    };
    if (r.undrafted) {
      return { ...listed(r), draft: null, request, facts: [`Ticket: #${r.ticket}, ${r.developer}`, 'Class: none matched yet'], thread: [] };
    }
    return {
      ...listed(r),
      request,
      draft: {
        recommendation: rec,
        resolution: post,
        status: r.verdict === 'NOT A PROBLEM' ? 'done' : 'accepted',
        ref: 'r15',
        misread: r.needs === 'lead' ? 'The request reads the contract\'s example as the rule. The example shows one case; the rule is in the description above it.' : '',
        facts: [
          `Ticket: #${r.ticket}, ${r.developer}`,
          `Class: ${r.class === 'none' ? 'none matched; the draft names a new one' : r.class}`,
          'Checked against: r14, the release being served',
          `Fix branch: fix/${cr.toLowerCase()} (not made yet)`,
        ],
        answer: `I read the request against r14.\n\nThe contract describes the operation in \`contracts/${cr === 'CR-602' ? 'catalogue' : 'venuemap'}.yaml\` and the storage in backend/tenant/V0129__after_r1_20261103.sql:57. The two disagree in the way the request says.\n\nThe fix is small and local: one forward migration, one contract note, and tests that fail without it. Nothing on an approved screen changes, so the design is untouched.\n\nRecommendation: ${rec}`,
      },
      thread: threads[cr] ?? [],
    };
  };
  return {
    async summary() {
      await wait();
      unset();
      const open = rows.filter((r) => !r.decision);
      if (SCENARIO === 'stopped') {
        return { waiting: open.length, blocking: open.filter((r) => r.blocking).length, needs_lead: 0, needs_client: 0, new: [],
          watching: false, last_run_at: at(5 * 60), last_error: '', paused: '', running_since: '', spend_today_usd: 0,
          daily_cap_usd: 20, decided: 0, not_drafted: open.length, draft_failed: open.filter((r) => r.draft_error).length };
      }
      const failedNow = open.filter((r) => r.undrafted && r.draft_error);
      const failedAll = SCENARIO === 'failed';
      return {
        waiting: open.length, blocking: open.filter((r) => r.blocking).length,
        needs_lead: open.filter((r) => r.needs === 'lead').length, needs_client: open.filter((r) => r.needs === 'client').length,
        new: [], last_run_at: at(12), running_since: '',
        last_error: failedAll ? `Drafting failed: ${KEY}` : '',
        paused: failedNow.length ? (failedAll
          ? `Drafting failed: ${KEY}; ${open.length} requests wait for a draft (${failedNow.length} failed 2 times and wait for Draft again on Decide (or cr-watch.py redraft --all-failed) once the cause is fixed).`
          : `Drafting is held: ${failedNow.filter((r) => r.draft_tries >= 2).length} requests failed 2 times (${KEY}) and wait for Draft again on Decide (or cr-watch.py redraft --all-failed) once the cause is fixed.`) : '',
        spend_today_usd: failedAll ? 0 : 12.4, daily_cap_usd: failedAll ? 20 : 50, decided: rows.filter((r) => r.decision).length,
        not_drafted: open.filter((r) => r.undrafted).length, draft_failed: failedNow.length,
      };
    },
    async requests() { await wait(); unset(); return { items: rows.map(listed), last_run_at: at(12) }; },
    async redraft(cr) {
      await wait(300);
      demoCalls.push(['redraft', cr]);
      const r = find(cr);
      if (!r?.undrafted) throw new ApiError(`${cr} was not asked to be drafted again: it has a draft already.`, 409);
      Object.assign(r, { draft_error: '', draft_reason: '', draft_tries: 0, redraft_asked_at: new Date().toISOString() });
      return { redraft: [cr], skipped: {} };
    },
    async redraftFailed() {
      await wait(300);
      const crs = rows.filter((r) => r.undrafted && r.draft_error).map((r) => r.cr);
      demoCalls.push(['redraft-all', crs.length]);
      for (const cr of crs) Object.assign(find(cr), { draft_error: '', draft_reason: '', draft_tries: 0, redraft_asked_at: new Date().toISOString() });
      return { redraft: crs, skipped: {} };
    },
    async history() {
      await wait();
      const H = [
        [26, 'CR-597', 'approve', 'done', 'r15', '31533', 'createTicketTier: the price band has no currency, so a tier priced in AED and one in USD compare as equal', 'Accepted. Build now: a price band carries its currency; two tiers compare only within one currency, and a mixed list answers 422.'],
        [70, 'CR-595', 'change', 'done', '', '30711', 'Guest profile merge: which record keeps the consent history when two guests are merged', 'Decided (Chinmay, 6 November 2026): the surviving record keeps both histories, newest first. Build now: merge appends the consent rows of the record merged away.'],
        [75, 'CR-594', 'approve', 'rejected', '', '31102', 'Event capacity: the request asks for a second capacity per gate, which the venue map already holds', 'Done, not a problem. Each gate\'s capacity is on the venue map\'s gate rows; read it from there.'],
        [26 * 60, 'CR-590', 'approve', 'done', 'r14', '30598', 'Wallet top-up: the receipt has no tax line though the screen shows one', 'Accepted. Build now: the receipt carries the tax line the screen shows, from the same calculation.'],
        [27 * 60, 'CR-588', 'approve', 'done', 'r14', '', 'Design change: the seat picker opens on the cheapest available section', 'Accepted. Recorded as a design change; the wireframe follows.'],
      ];
      return { items: H.map(([mins, cr, decision, status, ref, ticket, title, resolution], i) => ({
        id: 100 - i, cr, at: at(mins), who: 'chinmay.parab@softlabsgroup.com', failed: false, status, decision, ref, ticket, title, resolution,
      })).concat(SCENARIO === 'failed' ? [] : [{ id: 90, cr: 'CR-587', at: at(28 * 60), who: 'chinmay.parab@softlabsgroup.com', failed: true, status: 'done', decision: 'approve', ref: '', ticket: '30444', title: 'Coupon stacking: two percentage coupons apply in the wrong order', resolution: '' }]) };
    },
    async health() {
      await wait();
      unset();
      if (SCENARIO === 'stopped') {
        return { watching: false, last_run_at: at(5 * 60), last_error: '', paused: '', running_since: '', next_run_at: '',
          runs: [{ at: at(5 * 60), line: '0 new, 0 closed on their own, 4 waiting, 0 to draft' }], spend_held_usd: 0, batch_usd: 10 };
      }
      const next = new Date(now);
      next.setMinutes(7, 0, 0);
      if (next <= new Date(now)) next.setHours(next.getHours() + 1);
      const failedAll = SCENARIO === 'failed';
      const runs = failedAll
        ? [[12, '0 new, 0 closed on their own, 16 waiting, 0 to draft'], [72, '0 new, 0 closed on their own, 16 waiting, 8 to draft, 0 drafted, 8 failed; first failure: claude reported an error (exit 1): Invalid API key'],
          [132, '16 new, 0 closed on their own, 16 waiting, 16 to draft, 0 drafted, 16 failed; first failure: claude reported an error (exit 1): Invalid API key']]
        : [[12, '3 new, 0 closed on their own, 21 waiting, 4 to draft, 1 drafted, 3 failed; first failure: claude reported an error (exit 1): Invalid API key'],
          [72, '2 new, 0 closed on their own, 18 waiting, 2 to draft, 2 drafted'], [132, '0 new, 0 closed on their own, 16 waiting, 0 to draft'],
          [192, '5 new, 0 closed on their own, 16 waiting, 5 to draft, 5 drafted']];
      return { runs: runs.map(([mins, line]) => ({ at: at(mins), line })), next_run_at: next.toISOString(), spend_held_usd: failedAll ? 0 : 2,
        batch_usd: 10, running_since: '' };
    },
    async request(cr) { await wait(); unset(); if (!find(cr)) throw new ApiError('No such request.', 404); return detail(cr); },
    async decide(cr, body) {
      await wait(200);
      if (find(cr)?.undrafted) throw new ApiError(`${cr} has no draft yet, so there is nothing to decide; draft it again.`, 409, false, 'not-drafted');
      if (body.draft_hash !== hashOf(cr)) throw new ApiError('The draft changed.', 409);
      const r = find(cr);
      r.decision = body.decision === 'reject' ? `reject: ${body.note}` : { decision: body.decision, resolution: body.resolution, note: body.note ?? '' };
      fingerprint++;
      return { ok: true };
    },
    async ask(cr, question) {
      await wait(300);
      const entry = { id: Date.now(), question, status: 'pending', asked_at: new Date().toISOString() };
      (threads[cr] ??= []).push(entry);
      setTimeout(() => {
        entry.status = 'done';
        entry.answer = `Yes. The draft holds against r14: contracts/catalogue.yaml:1207 declares the read, and backend/tenant/V0129__after_r1_20261103.sql:57 is where the grant would sit beside the others.\n\nOne change I would make: run the integration test as the operations role rather than the owner, so a missing grant fails it.\n\n\`\`\`json\n{"resolution": "${(info[cr]?.[10] ?? 'Accepted.').replace(/"/g, '\\"')} Run the integration tests as the operations role.", "status": "accepted", "ref": "r15"}\n\`\`\``;
      }, 2600);
      return entry;
    },
    async preview() {
      await wait(700);
      const marked = rows.filter((r) => r.decision);
      const items = marked.map((r) => {
        const m = normMark(r.decision);
        return m.decision === 'reject'
          ? { cr: r.cr, status: 'stays open', ticket: '', note: 'Drafted again on the next run, with your note.' }
          : { cr: r.cr, status: m.decision === 'change' ? 'accepted, as you changed it' : r.verdict === 'NOT A PROBLEM' ? 'done' : 'accepted', ticket: r.ticket };
      });
      return {
        fingerprint: `fp-${fingerprint}`,
        items,
        lines: items.map((it) => `${it.cr}: ${it.status}${it.ticket ? `; comment on #${it.ticket}` : ''}`).concat('dry run: nothing was written'),
      };
    },
    async apply(fp) {
      await wait(900);
      if (fp !== `fp-${fingerprint}`) throw new ApiError('The decisions changed since the preview.', 409);
      for (let i = rows.length - 1; i >= 0; i--) {
        const m = normMark(rows[i].decision);
        if (!m) continue;
        if (m.decision === 'reject') rows[i].decision = '';
        else rows.splice(i, 1);
      }
      return { settled: true };
    },
    async deviceToken() { await wait(); demoCalls.push(['token', 1]); return { token: 'demo-device-token', id: 1 }; },
    async dropDeviceToken(id) { await wait(); demoCalls.push(['drop', String(id)]); return { ok: true }; },
  };
}

function installFakeApp() {
  let watch = { on: false, lastCheck: null };
  window.AdamApp = {
    unlock: async () => { await new Promise((r) => setTimeout(r, 400)); return true; },
    setWatch: async ({ token }) => { watch = { on: Boolean(token), lastCheck: token ? new Date().toISOString() : null }; },
    watchStatus: async () => watch,
  };
}

boot();
