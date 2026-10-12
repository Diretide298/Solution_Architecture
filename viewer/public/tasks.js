/**
 * The delivery overview: every ticket in the project's OpenProject project, in
 * every state, for the delivery team (a client is refused).
 *
 * The viewer already answers "what am I holding" — `adam_board` in Claude Code,
 * one person, open work only. This is the question asked every morning: **is
 * this sprint on track, and who is doing what?** That needs every ticket in
 * every state, which is why it is its own route (`/api/board/overview`).
 *
 * **It opens on the sprint, not the project.** A 6-month plan one week in is
 * 0.4% finished, and a page that leads with that number says nothing anybody
 * can act on. So the first thing drawn is the sprint today falls in: how much
 * of it is finished against an even pace through its working days, and a
 * burn-up that shows the gap. Then each person's share of that sprint, sorted
 * by who is furthest behind; then the queue of finished work waiting for QA;
 * then the whole plan as one strip, Sprint 1 to 13, with the blocks as bands.
 * Figures are drawn only where they carry something: a zero that matters is
 * said as a sentence ("No ticket has been closed yet: 35 are waiting for QA"),
 * and a zero that does not is left out.
 *
 * **Every state name comes from OpenProject.** ADAM keeps no list of statuses:
 * the service hands back the instance's own, each with `isClosed` and
 * `isDefault`. The page sorts every ticket into one of six kinds, and the
 * guesses it has to make are written down here, once:
 *
 *   closed           closed, and not by a status named like "rejected"
 *   waiting for QA   open, in a status named QA / review / testing / tested /
 *                    verify, and not one that says it failed or was reopened.
 *                    The developer has finished it; somebody else is next.
 *                    TICVAI's developers move finished work to "Ready for QA"
 *                    and QA closes it, so this is where finished work sits.
 *   rejected         closed by a status named reject / cancel / duplicate / won't
 *   on hold          open, in a status named hold / block / wait / pend
 *   not started      open, in the status a new ticket starts in (`isDefault`)
 *   in progress      open, anything else
 *
 * "Finished" is closed plus waiting for QA. A ticket waiting for QA is never
 * late: its developer is done with it.
 *
 * **Pace is an even line through the sprint's working days.** A sprint of ten
 * working days with 2,000 tickets is on pace when 200 are finished at the end
 * of day one. Weekends do not count. It is a yardstick, not a plan: nobody
 * finishes a sprint in a straight line, which is why the page says "behind
 * pace" and never "late" until the sprint has ended.
 *
 * **When a ticket was finished.** OpenProject 10's list has no closing date and
 * no date a status was reached. Where a close went through ADAM, the service
 * sends the moment it recorded (`closes`); everything else uses the ticket's
 * last change (`updatedAt`), which a later comment can move. The burn-up and
 * the QA queue both say so.
 *
 * **Nothing here writes.** Changing a ticket goes through propose-then-apply in
 * Claude Code, as it does everywhere else; a page that can move somebody else's
 * ticket is a page that moves it by accident.
 */
// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer.
import '/page-chrome.js';
import * as auth from '/validation.js';
import { hideLoader, loaderSays } from '/loader.js';
import { mountPanels } from '/panels.js';

const $ = (id) => document.getElementById(id);
const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};
const SVG = 'http://www.w3.org/2000/svg';
const svg = (tag, attrs = {}, text) => {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  if (text != null) node.textContent = text;
  return node;
};
const link = (href, className, text) => {
  const a = el('a', className, text);
  a.href = href;
  if (/^https?:/.test(href)) { a.target = '_blank'; a.rel = 'noreferrer'; }
  return a;
};

const state = {
  me: null,
  project: '',
  data: null,
  closedByName: new Map(),   // status name -> isClosed, from OpenProject
  defaultStatus: new Set(),  // the status(es) a new ticket starts in
  // The filter every section obeys. Kept in the address (?who=&sprint=&type=)
  // so a link to "Hrushikant's Sprint 1" is a link somebody can send.
  scope: { person: '', sprint: '', type: '' },
  // The ticket list's own filters, on top of the page's.
  filter: { text: '', status: '', openOnly: false },
  teamSort: 'behind',
  qaAll: false,
  ganttOpenOnly: false,
};

// Open states that mean the work has stopped. A guess: OpenProject has no
// "blocked" flag, so the name is all there is. The service makes the same
// guess when it reads the reason (main.py `_HELD`).
const STALLED = /hold|block|wait|pend/i;
// Closed states that mean the work was not done.
const DROPPED = /reject|cancel|duplicate|won.?t|invalid|obsolete/i;
// Used only when the instance does not say which status is the default.
const FRESH = /^(new|to ?do|backlog|open|not started)$/i;
// Open states that mean the developer has finished and somebody else is next,
// and the ones among them that mean it came back ("Test failed", "Reopened").
const AWAITING = /\bqa\b|review|testing|tested|verif/i;
const BOUNCED = /fail|reopen/i;

// ── days ────────────────────────────────────────────────────────────

const DAY = 86_400_000;
const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const asDate = (iso) => { const d = iso ? new Date(iso) : null; return d && !Number.isNaN(+d) ? d : null; };
/** A date-only field ("2026-10-05") as local midnight. `new Date()` reads it as
 *  UTC, which in India puts the first day of a sprint at 05:30 — after today's
 *  midnight, so on its first morning the sprint had not started. */
const asDay = (iso) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
};
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const days = (from, to) => Math.round((to - from) / DAY);
const isWorkday = (d) => d.getDay() !== 0 && d.getDay() !== 6;
const fmtDay = (d) => {
  const at = d instanceof Date ? d : asDate(d);
  return at ? at.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : '—';
};
const fmtShort = (d) => (d ? d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : '—');
const fmtWeekday = (d) => (d ? d.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' }) : '—');
const fmtWhen = (iso) => {
  const d = asDate(iso);
  return d ? d.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
};
const num = (n) => Number(n).toLocaleString();
const plural = (n, one, many) => `${num(n)} ${n === 1 ? one : many}`;
const pct = (part, whole) => (whole ? Math.round((part / whole) * 100) : 0);
/** A share that is small but not nothing reads as "under 1%", not as "0%". */
const share = (part, whole) => {
  if (!whole || !part) return '0%';
  const p = (part / whole) * 100;
  return p < 1 ? 'under 1%' : `${Math.round(p)}%`;
};

// ── what a ticket is ────────────────────────────────────────────────
//
// Every question the page asks about one ticket, asked once here so the
// sections cannot disagree about what "finished" or "late" means.

const isClosed = (t) => state.closedByName.get(t.status) === true;
const isRejected = (t) => isClosed(t) && DROPPED.test(t.status || '');
const isDone = (t) => isClosed(t) && !isRejected(t);
const isAwaiting = (t) => !isClosed(t) && AWAITING.test(t.status || '') && !BOUNCED.test(t.status || '');
const isFinished = (t) => isDone(t) || isAwaiting(t);
/** Still the developer's to do: open, and not waiting on QA. */
const isOpenWork = (t) => !isClosed(t) && !isAwaiting(t);
const isStalled = (t) => isOpenWork(t) && STALLED.test(t.status || '');
const isFresh = (t) => isOpenWork(t) && !isStalled(t)
  && (state.defaultStatus.size ? state.defaultStatus.has(t.status) : FRESH.test(t.status || ''));

/** The five kinds a bar draws, in the order it draws them. */
const KINDS = [
  { id: 'done', label: 'Closed' },
  { id: 'qa', label: 'Waiting for QA' },
  { id: 'going', label: 'In progress' },
  { id: 'stalled', label: 'On hold' },
  { id: 'fresh', label: 'Not started' },
];
const kindOf = (t) => (isRejected(t) ? 'rejected' : isDone(t) ? 'done' : isAwaiting(t) ? 'qa'
  : isStalled(t) ? 'stalled' : isFresh(t) ? 'fresh' : 'going');

/** When a ticket is due: its own date, or failing that its sprint's last day.
 *  TICVAI's tickets carry no dates of their own; the sprint is the deadline. */
const dueOn = (t) => asDay(t.dueDate) ?? sprintOf(t.version)?.end ?? null;
const isLate = (t) => { const d = dueOn(t); return isOpenWork(t) && d != null && d < today(); };
const isDueSoon = (t) => {
  const d = dueOn(t);
  return isOpenWork(t) && d != null && d >= today() && d <= addDays(today(), 7);
};
/** When it was finished: ADAM's own record where a close went through ADAM,
 *  otherwise OpenProject's last change — see the header. */
const finishedAt = (t) => (isDone(t) ? asDate(state.data.closes?.[t.key] ?? t.updatedAt)
  : isAwaiting(t) ? asDate(t.updatedAt) : null);
const who = (t) => t.assignee || 'Unassigned';

// ── sprints ─────────────────────────────────────────────────────────
//
// A ticket names its version and nothing else. The service sends each
// version's dates where OpenProject has them; a "Sprint N" without dates falls
// back to TICVAI's calendar — two-week sprints from Monday 5 October 2026,
// Monday to the Friday of the second week.

const SPRINT_ONE = new Date(2026, 9, 5);
let sprintTable = new Map();

function buildSprints() {
  sprintTable = new Map();
  for (const v of state.data.versions ?? []) {
    sprintTable.set(v.name, { name: v.name, start: asDay(v.startDate), end: asDay(v.endDate), fromCalendar: false });
  }
  for (const t of state.data.items ?? []) {
    if (t.version && !sprintTable.has(t.version)) {
      sprintTable.set(t.version, { name: t.version, start: null, end: null, fromCalendar: false });
    }
  }
  for (const s of sprintTable.values()) {
    const n = /^sprint\s+(\d+)$/i.exec(s.name)?.[1];
    s.number = n ? Number(n) : null;
    if (n && !s.start && !s.end) {
      s.start = addDays(SPRINT_ONE, (Number(n) - 1) * 14);
      s.end = addDays(s.start, 11);
      s.fromCalendar = true;
    }
  }
}
const sprintOf = (name) => (name ? sprintTable.get(name) : null);
/** The dated sprints, in calendar order: the plan's columns. */
const datedSprints = () => [...sprintTable.values()].filter((s) => s.start && s.end).sort((a, b) => a.start - b.start);

/** The sprint today is in: the latest one that has started and not ended more
 *  than a weekend ago. */
function currentSprint() {
  const now = today();
  return datedSprints().filter((s) => s.start <= now && +s.end + 3 * DAY >= +now).at(-1) ?? null;
}
const nextSprint = (s) => datedSprints().find((x) => s && x.start > s.start) ?? null;

/** The sprint the top of the page is about: the one chosen in the filter, or
 *  the current one, or the first that has not started. */
function focusSprint() {
  if (state.scope.sprint) { const s = sprintOf(state.scope.sprint); return s?.start ? s : null; }
  return currentSprint() ?? datedSprints().find((s) => s.start > today()) ?? datedSprints().at(-1) ?? null;
}

/** Where a sprint stands in its own working days. `through` counts today. */
function clock(s) {
  const now = today();
  const list = [];
  for (let d = new Date(s.start); d <= s.end; d = addDays(d, 1)) if (isWorkday(d)) list.push(d);
  const n = Math.max(1, list.length);
  const phase = now < s.start ? 'ahead' : now > s.end ? 'over' : 'running';
  const before = list.filter((d) => d < now).length;
  const todayAt = list.findIndex((d) => +d === +now);
  const through = phase === 'over' ? n : phase === 'ahead' ? 0 : before + (todayAt >= 0 ? 1 : 0);
  return {
    days: list, n, phase, through,
    left: list.filter((d) => d > now).length,
    dayNo: todayAt >= 0 ? todayAt + 1 : null,
    frac: through / n,
  };
}

// ── the scope ───────────────────────────────────────────────────────

/** The items the page is about, filtered by every page filter except `skip`. */
function scoped(skip = '') {
  const { person, sprint, type } = state.scope;
  return (state.data?.items ?? []).filter((t) => {
    if (skip !== 'person' && person && who(t) !== person) return false;
    if (skip !== 'sprint' && sprint && (t.version || '(no sprint)') !== sprint) return false;
    if (skip !== 'type' && type && (t.type || '') !== type) return false;
    return true;
  });
}
/** The focus sprint's tickets, under the type filter and, unless `everyone`,
 *  the person filter. The sprint filter is the focus itself. */
const inFocus = (focus, { everyone = false } = {}) => (focus
  ? (state.data?.items ?? []).filter((t) => t.version === focus.name
    && (everyone || !state.scope.person || who(t) === state.scope.person)
    && (!state.scope.type || (t.type || '') === state.scope.type))
  : []);

function count(items) {
  const c = { total: items.length, done: 0, qa: 0, going: 0, stalled: 0, fresh: 0, rejected: 0, late: 0 };
  for (const t of items) {
    c[kindOf(t)] += 1;
    if (isLate(t)) c.late += 1;
  }
  c.live = c.total - c.rejected;     // what a share of finished is a share of
  c.finished = c.done + c.qa;
  c.open = c.going + c.stalled + c.fresh;
  return c;
}

function setScope(change) {
  Object.assign(state.scope, change);
  const params = new URLSearchParams(location.search);
  for (const [key, name] of [['person', 'who'], ['sprint', 'sprint'], ['type', 'type']]) {
    if (state.scope[key]) params.set(name, state.scope[key]); else params.delete(name);
  }
  const query = params.toString();
  history.replaceState(null, '', `${location.pathname}${query ? `?${query}` : ''}${location.hash}`);
  draw();
}

// ── reading ─────────────────────────────────────────────────────────

async function load({ refresh = false } = {}) {
  $('tk-error').hidden = true;
  if (refresh) $('tk-asof').textContent = 'Reading OpenProject…';
  try {
    const data = await auth.boardOverview(state.project, { refresh });
    state.data = data;
    state.closedByName = new Map((data.statuses ?? []).map((s) => [s.name, !!s.isClosed]));
    state.defaultStatus = new Set((data.statuses ?? []).filter((s) => s.isDefault).map((s) => s.name));
    buildSprints();
    buildTree();
    draw();
  } catch (error) {
    // 428 is the service saying the token or the project link is missing: the
    // panel that says which of the two and where to fix it, not a red line.
    if (error.status === 428) return needsSetup(error.message);
    if (error.status === 403) return denied();
    // 503 is the first read of a big project still running on the server. It
    // carries on without us; asking again shortly is the whole of the fix.
    if (error.status === 503) {
      $('tk-asof').textContent = `${error.message} Checking again in 30 seconds…`;
      setTimeout(() => load(), 30_000);
      return;
    }
    $('tk-asof').textContent = '';
    showError(`Could not read the tickets: ${error.message}`);
  }
}

function showError(message) {
  const box = $('tk-error');
  box.textContent = message;
  box.hidden = false;
}

function needsSetup(why) {
  $('tasks').hidden = true;
  $('unconnected').hidden = false;
  $('unconnected-why').textContent = why;
  const projectFault = /admin page|Projects/i.test(why);
  $('unconnected-go').textContent = projectFault ? 'Go to the admin page' : 'Go to settings';
  $('unconnected-go').href = projectFault ? '/admin.html#projects' : '/settings.html#openproject';
}

function denied() {
  $('tasks').hidden = true;
  $('denied').hidden = false;
}

// ── the tree ────────────────────────────────────────────────────────
//
// Each ticket's top-level ancestor (a block, on TICVAI) and the ancestor just
// under it (a feature), walked once per load. Visit-guarded: a parent chain is
// another system's data, and a cycle must not hang the page.

const tree = { byKey: new Map(), top: new Map(), second: new Map() };

function buildTree() {
  const all = state.data.items ?? [];
  tree.byKey = new Map(all.map((t) => [String(t.key), t]));
  tree.top = new Map();
  tree.second = new Map();
  for (const t of all) {
    const chain = [t];
    const seen = new Set([t.key]);
    let at = t;
    while (at.parent && tree.byKey.has(String(at.parent)) && !seen.has(String(at.parent))) {
      at = tree.byKey.get(String(at.parent));
      seen.add(at.key);
      chain.push(at);
    }
    tree.top.set(t.key, chain.at(-1));
    tree.second.set(t.key, chain.length >= 2 ? chain.at(-2) : null);
  }
}

/** The top-level epics: TICVAI's blocks. */
function blocks() {
  return (state.data.items ?? [])
    .filter((t) => !t.parent && /epic/i.test(t.type || ''))
    .sort((a, b) => String(a.subject).localeCompare(String(b.subject), undefined, { numeric: true }));
}

/** "Block A1: the first release, first drop (Sprints 1-4)" → its parts. The
 *  window is read from the name because that is where the plan wrote it. */
function blockName(subject) {
  const s = String(subject || '');
  const window = /\(\s*sprints?\s*(\d+)\s*[-–to ]+\s*(\d+)\s*\)/i.exec(s);
  const code = /^block\s+([a-z]\d*)\b/i.exec(s)?.[1]?.toUpperCase() ?? '';
  const words = s.replace(/^block\s+[a-z]\d*\s*:?\s*/i, '').replace(/\(\s*sprints?[^)]*\)/i, '').trim();
  return { code, words, from: window ? Number(window[1]) : null, to: window ? Number(window[2]) : null };
}

// ── drawing ─────────────────────────────────────────────────────────

function draw() {
  if (!state.data) return;
  const items = scoped();
  const focus = focusSprint();
  drawLede();
  drawScope();
  drawSprint(focus);
  drawRoster(focus);
  drawQueue();
  drawPlan(focus);
  drawAttention(items);
  drawPeopleTable(focus);
  drawGate();
  drawStates(items);
  drawDates(items);
  drawTimeline(items);
  drawDeliverables(items);
  drawParents(items);
  drawFilters(items);
  drawList();
}

function drawLede() {
  const d = state.data;
  const op = d.openproject ?? {};
  $('tk-lede').replaceChildren(
    `${plural(d.total ?? 0, 'ticket', 'tickets')} in `,
    op.url ? link(op.url, null, op.name || op.identifier) : el('span', null, op.name || op.identifier || 'OpenProject'),
    d.truncated ? ' — the newest of a larger project; older tickets are not counted.' : '.',
  );
  const age = d.ageSeconds ?? 0;
  $('tk-asof').textContent = d.fromCache
    ? `Read ${age < 60 ? 'under a minute' : plural(Math.round(age / 60), 'minute', 'minutes')} ago`
    : `Read just now, ${fmtWhen(d.asOf)}`;
}

function drawScope() {
  const all = state.data.items ?? [];
  const tally = (key) => {
    const m = new Map();
    for (const t of all) m.set(key(t), (m.get(key(t)) ?? 0) + 1);
    return m;
  };
  const people = [...tally(who).entries()].sort((a, b) =>
    (a[0] === 'Unassigned') - (b[0] === 'Unassigned') || a[0].localeCompare(b[0]));
  fillSelect($('tk-scope-person'), 'Everyone', people.map(([n, c]) => [n, `${n} (${num(c)})`]), state.scope.person);

  const now = currentSprint()?.name;
  const sprints = [...tally((t) => t.version || '(no sprint)').keys()].sort(bySprint);
  fillSelect($('tk-scope-sprint'), 'Every sprint', sprints.map((n) => [n, n === now ? `${n} (now)` : n]),
    state.scope.sprint);

  const types = [...tally((t) => t.type || '').entries()].filter(([n]) => n).sort((a, b) => b[1] - a[1]);
  fillSelect($('tk-scope-type'), 'Every type', types.map(([n, c]) => [n, `${n} (${num(c)})`]), state.scope.type);

  const on = Object.values(state.scope).some(Boolean);
  $('tk-scope-clear').hidden = !on;
  const parts = [];
  if (state.scope.person) parts.push(state.scope.person);
  if (state.scope.sprint) parts.push(state.scope.sprint);
  if (state.scope.type) parts.push(`${state.scope.type} tickets only`);
  $('tk-scope-says').textContent = on
    ? `Every section shows ${parts.join(', ')}: ${plural(scoped().length, 'ticket', 'tickets')}.`
    : '';
}

/** Sprint names in calendar order; unknown dates after, by name. */
function bySprint(a, b) {
  const sa = sprintOf(a)?.start;
  const sb = sprintOf(b)?.start;
  if (sa && sb) return sa - sb;
  if (sa || sb) return sa ? -1 : 1;
  if (a === '(no sprint)' || b === '(no sprint)') return a === '(no sprint)' ? 1 : -1;
  return a.localeCompare(b, undefined, { numeric: true });
}

function fillSelect(select, allLabel, values, chosen) {
  select.replaceChildren(el('option', null, allLabel), ...values.map((v) => {
    const [value, label] = Array.isArray(v) ? v : [v, v];
    const option = el('option', null, label);
    option.value = value;
    option.selected = value === chosen;
    return option;
  }));
  select.firstChild.value = '';
}

// ── the stacked state bar ───────────────────────────────────────────
//
// One component for every person and the plan, so a state is the same colour
// and the same place in the bar wherever it appears: closed, waiting for QA,
// in progress, on hold, not started, a 2px gap between them. Rejected tickets
// are not drawn: they are neither work done nor work left.

function stack(c, { scale = 1, label = '', tick = null } = {}) {
  const bar = el('div', 'tk-stack');
  const fill = el('div', 'tk-stack-fill');
  fill.style.width = `${Math.max(0, Math.min(1, scale)) * 100}%`;
  for (const kind of KINDS) {
    const n = c[kind.id];
    if (!n) continue;
    const seg = el('span', `tk-seg tk-seg-${kind.id}`);
    seg.style.flexGrow = String(n);
    seg.dataset.tip = `${label ? `${label}: ` : ''}${kind.label} ${num(n)} of ${num(c.live)} (${share(n, c.live)})`;
    fill.append(seg);
  }
  bar.append(fill);
  // Where an even pace would have the finished part reach by now.
  if (tick != null) {
    const mark = el('span', 'tk-pace-tick');
    mark.style.left = `${Math.max(0, Math.min(1, tick)) * 100}%`;
    bar.append(mark);
  }
  bar.setAttribute('role', 'img');
  bar.setAttribute('aria-label', describe(c, label));
  return bar;
}

function describe(c, label) {
  const parts = KINDS.filter((k) => c[k.id]).map((k) => `${num(c[k.id])} ${k.label.toLowerCase()}`);
  if (c.rejected) parts.push(`${num(c.rejected)} rejected`);
  return `${label ? `${label}: ` : ''}${plural(c.total, 'ticket', 'tickets')}${parts.length ? `, ${parts.join(', ')}` : ''}.`;
}

function legendItems(list, kinds) {
  list.replaceChildren(...kinds.map((kind) => {
    const item = el('li', 'tk-legend-item');
    item.append(el('span', `tk-key-swatch tk-seg-${kind.id}`), el('span', 'tk-legend-label', kind.label));
    return item;
  }));
  return list;
}

// ── this sprint ─────────────────────────────────────────────────────

const TONES = {
  ok: { glyph: '✓', label: 'On pace' },
  warn: { glyph: '–', label: 'A little behind' },
  bad: { glyph: '↓', label: 'Behind pace' },
  idle: { glyph: '○', label: 'Not started' },
  over: { glyph: '■', label: 'Ended' },
};

function verdictPill(tone, label) {
  const pill = el('span', `tk-verdict-pill is-${tone}`);
  pill.append(el('span', 'tk-verdict-glyph', TONES[tone].glyph), el('span', null, label ?? TONES[tone].label));
  return pill;
}

function drawSprint(focus) {
  const when = $('tk-sprint-when');
  const title = $('tk-sprint-title');
  const pace = $('tk-sprint-pace');
  const ledger = $('tk-sprint-ledger');
  const saying = $('tk-sprint-saying');
  $('tk-burn').hidden = true;
  $('tk-next').replaceChildren();

  if (!focus) {
    // A sprint without dates ("(no sprint)", a version nobody dated): there is
    // no clock to hold it against, so the top says what it holds and stops.
    const c = count(scoped());
    when.textContent = state.scope.sprint || 'No sprint';
    title.textContent = `${num(c.finished)} of ${plural(c.live, 'ticket', 'tickets')} finished.`;
    pace.textContent = 'These tickets are in no dated sprint, so there is no pace to hold them against.';
    ledger.replaceChildren();
    saying.textContent = '';
    return;
  }

  const items = inFocus(focus);
  const c = count(items);
  const k = clock(focus);
  const expected = Math.round(c.live * k.frac);
  const range = `${fmtWeekday(focus.start)} to ${fmtWeekday(focus.end)}`;

  when.replaceChildren(el('strong', null, focus.name), ` ${range}`,
    k.phase === 'running' && k.dayNo ? el('span', 'tk-day', `day ${k.dayNo} of ${k.n}`) : '');

  let tone = 'ok';
  if (k.phase === 'ahead') tone = 'idle';
  else if (k.phase === 'over') tone = c.finished >= c.live ? 'ok' : 'over';
  else if (expected > 0) {
    const ratio = c.finished / expected;
    tone = ratio >= 0.9 ? 'ok' : ratio >= 0.6 ? 'warn' : 'bad';
  }
  const behind = Math.max(0, expected - c.finished);

  if (!c.live) {
    title.replaceChildren(`Nothing in ${focus.name}${state.scope.person ? ` is ${state.scope.person}'s` : ''}.`);
    pace.textContent = '';
    ledger.replaceChildren();
    saying.textContent = '';
    drawNext(focus);
    return;
  }

  title.replaceChildren(
    verdictPill(tone, k.phase === 'over' && c.finished < c.live ? 'Ended unfinished' : undefined),
    el('span', 'tk-headline-figures', `${num(c.finished)} of ${num(c.live)} finished`),
  );

  if (k.phase === 'ahead') {
    pace.textContent = `Starts ${fmtWeekday(focus.start)}, ${plural(k.n, 'working day', 'working days')} long.`;
  } else if (k.phase === 'over') {
    pace.textContent = c.finished >= c.live
      ? 'Ended with everything in it finished.'
      : `Ended ${fmtWeekday(focus.end)} with ${plural(c.open, 'ticket', 'tickets')} still open: those are late now.`;
  } else {
    const gone = k.dayNo
      ? `by the end of today, day ${k.dayNo} of ${k.n}`
      : `after ${k.through} of ${k.n} working days`;
    const parts = [`An even pace would have ${num(expected)} finished ${gone}`
      + (behind ? `, so it is ${num(behind)} short.` : '.')];
    parts.push(k.left ? `${plural(k.left, 'working day', 'working days')} left after today.` : 'Today is its last working day.');
    if (c.finished && k.through) {
      const projected = Math.min(c.live, Math.round((c.finished / k.through) * k.n));
      parts.push(`At this rate about ${num(projected)} will be finished when it ends on ${fmtWeekday(focus.end)}.`);
    }
    pace.textContent = parts.join(' ');
  }

  // The composition, as words and figures rather than tiles: a figure only
  // where it is not zero, because a row of zeros is a row nobody reads.
  const rows = [
    ['Planned', c.live, ''],
    ['Closed', c.done, 'done'],
    ['Waiting for QA', c.qa, 'qa'],
    ['In progress', c.going, 'going'],
    ['On hold', c.stalled, 'stalled'],
    ['Not started', c.fresh, 'fresh'],
  ].filter(([label, n]) => n || label === 'Planned');
  ledger.replaceChildren(...rows.flatMap(([label, n, kind]) => {
    const wrap = el('div', 'tk-ledger-item');
    const dt = el('dt');
    if (kind) dt.append(el('span', `tk-key-swatch tk-seg-${kind}`));
    dt.append(label);
    wrap.append(dt, el('dd', null, num(n)));
    return [wrap];
  }));

  // The zeros that matter, said.
  const said = [];
  if (!c.done && c.qa) said.push(`No ticket has been closed yet: ${num(c.qa)} ${c.qa === 1 ? 'is' : 'are'} waiting for QA.`);
  else if (!c.finished && k.phase !== 'ahead') said.push('Nothing in it is finished yet.');
  if (!c.going && c.fresh && k.phase === 'running') {
    said.push('Nothing is marked In progress, so the board cannot tell work under way from work not begun.');
  }
  if (c.rejected) said.push(`${plural(c.rejected, 'ticket was', 'tickets were')} rejected and ${c.rejected === 1 ? 'is' : 'are'} not counted.`);
  saying.textContent = said.join(' ');

  if (k.phase !== 'ahead') drawBurn(focus, items, c, k);
  drawNext(focus);
}

function drawNext(focus) {
  const next = nextSprint(focus);
  if (!next) return;
  const items = inFocus(next);
  const c = count(items);
  const line = $('tk-next');
  line.replaceChildren(el('span', 'tk-next-label', 'Next'), ' ',
    el('strong', null, next.name), `, ${fmtWeekday(next.start)} to ${fmtWeekday(next.end)}: `,
    c.live ? `${plural(c.live, 'ticket', 'tickets')} planned` : 'nothing planned yet',
    c.finished ? `, ${num(c.finished)} already finished.` : '.');
}

/**
 * The burn-up: finished so far against an even line through the sprint's
 * working days. One measure on one axis; the even line is dashed because it
 * is a yardstick and not data. The gap at today is drawn and labelled, since
 * it is the one number the chart exists to show.
 */
function drawBurn(focus, items, c, k) {
  const figure = $('tk-burn');
  const box = $('tk-burn-plot');
  figure.hidden = false;
  const W = Math.max(280, Math.round(box.clientWidth || 420));
  const H = 210;
  const m = { l: 46, r: 84, t: 22, b: 30 };
  const iw = W - m.l - m.r;
  const ih = H - m.t - m.b;
  const top = roundUp(Math.max(1, c.live));
  const x = (i) => m.l + (i / k.n) * iw;
  const y = (v) => m.t + ih - (v / top) * ih;

  // Cumulative finished by the end of each working day; 0 is "before it began".
  const at = items.filter(isFinished).map(finishedAt).filter(Boolean).sort((a, b) => a - b);
  const byEnd = (d) => at.filter((w) => w < addDays(d, 1)).length;
  const cum = [at.filter((w) => w < k.days[0]).length];
  for (let i = 1; i <= k.through; i += 1) cum.push(i === k.through && k.phase === 'running' ? at.length : byEnd(k.days[i - 1]));

  const pic = svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img',
    'aria-label': `Burn-up for ${focus.name}: ${num(c.finished)} of ${num(c.live)} finished; an even pace would have ${num(Math.round(c.live * k.frac))}.` });

  // Gridlines and their labels: three, recessive.
  for (const v of [0, top / 2, top]) {
    pic.append(svg('line', { x1: m.l, x2: m.l + iw, y1: y(v), y2: y(v), class: v ? 'tk-burn-grid' : 'tk-burn-base' }));
    pic.append(svg('text', { x: m.l - 8, y: y(v) + 4, class: 'tk-burn-tick', 'text-anchor': 'end' }, num(Math.round(v))));
  }
  // Today, as the column it occupies.
  if (k.phase === 'running' && k.through) {
    pic.append(svg('rect', { x: x(k.through - 1), y: m.t, width: x(k.through) - x(k.through - 1), height: ih, class: 'tk-burn-today' }));
    pic.append(svg('text', { x: (x(k.through - 1) + x(k.through)) / 2, y: m.t - 8, class: 'tk-burn-tick', 'text-anchor': 'middle' }, 'today'));
  }
  // The days along the bottom: the first, the last, and Mondays between.
  k.days.forEach((d, i) => {
    if (i !== 0 && i !== k.n - 1 && d.getDay() !== 1) return;
    pic.append(svg('text', { x: (x(i) + x(i + 1)) / 2, y: H - 10, class: 'tk-burn-tick', 'text-anchor': 'middle' }, fmtShort(d)));
  });

  // The even pace.
  pic.append(svg('line', { x1: x(0), y1: y(0), x2: x(k.n), y2: y(c.live), class: 'tk-burn-even' }));
  pic.append(svg('text', { x: x(k.n) + 6, y: y(c.live) + 4, class: 'tk-burn-label' }, 'even pace'));
  pic.append(svg('text', { x: x(k.n) + 6, y: y(c.live) + 18, class: 'tk-burn-tick' }, num(c.live)));

  // Finished so far.
  const pts = cum.map((v, i) => `${x(i)},${y(v)}`).join(' ');
  pic.append(svg('polyline', { points: pts, class: 'tk-burn-line' }));
  const endX = x(cum.length - 1);
  const endY = y(cum.at(-1));
  // The gap at today, the number the chart exists for.
  const expected = Math.round(c.live * k.frac);
  if (k.phase === 'running' && expected > cum.at(-1)) {
    const ey = y(expected);
    pic.append(svg('line', { x1: endX, x2: endX, y1: ey, y2: endY - 6, class: 'tk-burn-gap' }));
    pic.append(svg('circle', { cx: endX, cy: ey, r: 3.5, class: 'tk-burn-expected' }));
    // Halfway up the gap, but never on top of the "finished" label below it.
    const labelY = Math.min((ey + endY) / 2 + 4, endY - 26);
    pic.append(svg('text', { x: endX + 8, y: Math.max(ey + 4, labelY), class: 'tk-burn-label' }, `${num(expected - cum.at(-1))} short`));
  }
  pic.append(svg('circle', { cx: endX, cy: endY, r: 4.5, class: 'tk-burn-dot' }));
  pic.append(svg('text', { x: endX + 8, y: endY - 6, class: 'tk-burn-label is-strong' }, `${num(cum.at(-1))} finished`));

  // Hover and focus: one target per day, wider than the mark.
  const tips = svg('g', { class: 'tk-burn-hits' });
  k.days.forEach((d, i) => {
    const done = i < cum.length - 1 ? cum[i + 1] : null;
    const even = Math.round((c.live * (i + 1)) / k.n);
    const hit = svg('rect', { x: x(i), y: m.t, width: x(i + 1) - x(i), height: ih, class: 'tk-burn-hit' });
    hit.dataset.tip = `${fmtWeekday(d)}, day ${i + 1} of ${k.n}: `
      + (done == null ? `not reached yet; an even pace is ${num(even)} by its end.`
        : `${num(done)} finished by its end; an even pace is ${num(even)}.`);
    tips.append(hit);
  });
  pic.append(tips);

  // The table twin, for anything not looking at the picture.
  const table = el('table', 'tk-sr');
  table.append(el('caption', null, `${focus.name}: tickets finished by the end of each working day`));
  const head = el('tr');
  head.append(el('th', null, 'Day'), el('th', null, 'Finished'), el('th', null, 'Even pace'));
  table.append(head);
  k.days.forEach((d, i) => {
    if (i + 1 >= cum.length) return;
    const row = el('tr');
    row.append(el('td', null, fmtWeekday(d)), el('td', null, num(cum[i + 1])), el('td', null, num(Math.round((c.live * (i + 1)) / k.n))));
    table.append(row);
  });

  box.replaceChildren(pic, table);
  $('tk-burn-caption').textContent = 'Finished so far, against an even pace'
    + (Object.keys(state.data.closes ?? {}).length ? '' : ' (a ticket counts on the day it last changed)');
}

/** An axis ceiling that hugs the value: the next multiple of half its power
 *  of ten (2,209 → 2,500), so the line uses the height it is given. */
function roundUp(value) {
  if (value <= 10) return niceMax(value);
  const step = 10 ** Math.floor(Math.log10(value)) / 2;
  return Math.ceil(value / step) * step;
}

/** A "nice" ceiling for an axis: 1, 2, 5 or 10 times a power of ten. */
function niceMax(value) {
  if (value <= 10) return Math.max(2, value + (value % 2));
  const power = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 5, 10]) {
    if (step * power >= value) return step * power;
  }
  return 10 * power;
}

// ── who is doing what ───────────────────────────────────────────────

/** One row per person: their focus-sprint counts, pace, and whole-plan load. */
function people(focus) {
  const k = focus ? clock(focus) : null;
  const rows = new Map();
  const row = (name) => {
    if (!rows.has(name)) rows.set(name, { name, sprint: [], all: [] });
    return rows.get(name);
  };
  // The whole-plan load ignores the sprint filter: "open in the plan" means
  // the plan, whatever sprint the top of the page is showing.
  const everything = (state.data.items ?? []).filter((t) => !state.scope.type || (t.type || '') === state.scope.type);
  for (const t of everything) row(who(t)).all.push(t);
  for (const t of inFocus(focus, { everyone: true })) row(who(t)).sprint.push(t);
  for (const r of rows.values()) {
    r.c = count(r.sprint);
    r.open = r.all.filter(isOpenWork).length;
    r.finishedAll = r.all.filter(isFinished).length;
    r.lateAll = r.all.filter(isLate).length;
    r.expected = k ? Math.round(r.c.live * k.frac) : 0;
    r.behind = r.expected - r.c.finished;
    r.gate = gateFor(r.name);
  }
  return [...rows.values()].filter((r) => r.all.length || r.sprint.length);
}

function sortPeople(rows) {
  const unassignedLast = (a, b) => (a.name === 'Unassigned') - (b.name === 'Unassigned');
  const by = {
    behind: (a, b) => b.behind - a.behind || b.c.live - a.c.live,
    planned: (a, b) => b.c.live - a.c.live,
    done: (a, b) => b.c.finished - a.c.finished,
    name: () => 0,
  }[state.teamSort] ?? (() => 0);
  return rows.sort((a, b) => unassignedLast(a, b) || by(a, b) || a.name.localeCompare(b.name));
}

const initials = (name) => (name === 'Unassigned' ? '–'
  : name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join(''));

function drawRoster(focus) {
  const k = focus ? clock(focus) : null;
  const rows = sortPeople(people(focus));
  const biggest = Math.max(1, ...rows.map((r) => r.c.live));
  $('tk-roster-head-bar').textContent = focus ? focus.name : 'This sprint';
  const running = k?.phase === 'running';
  $('tk-team-note').textContent = focus
    ? `Each bar is one person's tickets in ${focus.name}, on one scale. `
      + (running ? 'The upright mark is where an even pace would have their finished part by the end of today. ' : '')
      + 'Open in the plan is everything still theirs across every sprint, as a number, so a big backlog does not drown the sprint. '
      + 'Select a person to show only their work on every section.'
    : 'No dated sprint to measure against. Select a person to show only their work on every section.';

  const box = $('tk-roster');
  box.replaceChildren(...rows.map((r) => {
    const chosen = state.scope.person === r.name;
    const row = el('button', `tk-person${chosen ? ' is-chosen' : ''}${r.name === 'Unassigned' ? ' is-nobody' : ''}`);
    row.type = 'button';
    row.setAttribute('aria-pressed', chosen ? 'true' : 'false');

    const ident = el('span', 'tk-person-who');
    ident.append(el('span', 'tk-avatar', initials(r.name)), el('span', 'tk-person-name', r.name));

    const bar = el('span', 'tk-person-bar');
    if (r.c.live) {
      bar.append(stack(r.c, { scale: r.c.live / biggest, label: r.name,
        tick: running ? (r.expected / biggest) : null }));
    } else {
      bar.append(el('span', 'tk-quiet', focus ? `nothing in ${focus.name}` : 'no sprint'));
    }

    const done = el('span', 'tk-person-done');
    if (r.c.live) done.append(el('strong', null, num(r.c.finished)), el('span', null, ` of ${num(r.c.live)}`));

    const pace = el('span', 'tk-person-pace');
    if (!r.c.live) pace.append(el('span', 'tk-quiet', ''));
    else if (!running) pace.append(el('span', 'tk-quiet', k?.phase === 'ahead' ? `starts ${fmtShort(focus.start)}` : `${num(r.c.open)} left open`));
    else if (r.behind > 0) {
      pace.classList.add('is-behind');
      pace.append(el('span', 'tk-pace-glyph', '↓'), `${num(r.behind)} behind`);
    } else pace.append(el('span', 'tk-pace-glyph is-ok', '✓'), r.behind < 0 ? `${num(-r.behind)} ahead` : 'on pace');

    const open = el('span', 'tk-person-open');
    open.append(el('strong', null, num(r.open)), el('span', null, ' open'));

    row.append(ident, bar, done, pace, open);
    row.setAttribute('aria-label', `${r.name}. ${focus ? `${focus.name}: ${num(r.c.finished)} of ${num(r.c.live)} finished` : ''}`
      + `${running && r.c.live ? (r.behind > 0 ? `, ${num(r.behind)} behind an even pace` : ', on pace') : ''}`
      + `. ${num(r.open)} open in the whole plan. ${chosen ? 'Selected; select again to show everyone.' : 'Select to show only their work.'}`);
    row.onclick = () => setScope({ person: chosen ? '' : r.name });
    return row;
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'Nobody has a ticket in this view.'));

  const key = legendItems($('tk-roster-key'), KINDS.filter((kind) => rows.some((r) => r.c[kind.id])));
  if (running) {
    const item = el('li', 'tk-legend-item');
    item.append(el('span', 'tk-key-tick'), el('span', 'tk-legend-label', 'Even pace by today'));
    key.append(item);
  }
}

// ── waiting for QA ──────────────────────────────────────────────────

const QA_SHOWN = 8;

function waited(t) {
  const at = asDate(t.updatedAt);
  if (!at) return { n: 0, text: '—' };
  const d = days(new Date(at.getFullYear(), at.getMonth(), at.getDate()), today());
  return { n: d, text: d <= 0 ? 'today' : d === 1 ? '1 day' : `${d} days` };
}

function drawQueue() {
  const list = scoped().filter(isAwaiting).sort((a, b) => (asDate(a.updatedAt) ?? 0) - (asDate(b.updatedAt) ?? 0));
  const box = $('tk-qa');
  const note = $('tk-qa-note');
  $('tk-qa-title').textContent = list.length ? `Waiting for QA (${num(list.length)})` : 'Waiting for QA';
  if (!list.length) {
    note.textContent = '';
    box.replaceChildren(el('p', 'tk-empty', 'Nothing is waiting for QA in this view.'));
    return;
  }
  const byWho = new Map();
  for (const t of list) byWho.set(who(t), (byWho.get(who(t)) ?? 0) + 1);
  const most = [...byWho.entries()].sort((a, b) => b[1] - a[1])[0];
  const oldest = waited(list[0]);
  note.textContent = `Finished by the developer, waiting for somebody to test and close. Oldest first; `
    + `the oldest has waited ${oldest.text === 'today' ? 'since today' : oldest.text}. `
    + (most[1] > 1 && list.length > 2 ? `${most[0]} finished ${num(most[1])} of them. ` : '')
    + 'Waiting is counted from the ticket’s last change, the nearest OpenProject 10 gives to when it got here.';

  const shown = state.qaAll ? list : list.slice(0, QA_SHOWN);
  const table = el('div', 'tk-qa-list');
  for (const t of shown) {
    const row = el('div', 'tk-qa-row');
    const w = waited(t);
    const main = el('span', 'tk-main');
    main.append(el('span', 'tk-subject', t.subject || '(no subject)'));
    if (t.parentSubject) main.append(el('span', 'tk-parent', t.parentSubject));
    row.append(link(t.url, 'tk-key', `#${t.key}`), main, el('span', 'tk-who', who(t)),
      el('span', `tk-waited${w.n >= 3 ? ' is-long' : ''}`, w.text), el('span', 'tk-qa-sprint', t.version || 'no sprint'));
    row.title = `${t.subject}\n${who(t)}, ${t.status} since ${fmtWhen(t.updatedAt)}`;
    table.append(row);
  }
  box.replaceChildren(table);
  if (list.length > QA_SHOWN) {
    const more = el('button', 'chip tk-more', state.qaAll ? 'Show the oldest eight' : `Show all ${num(list.length)}`);
    more.type = 'button';
    more.setAttribute('aria-expanded', state.qaAll ? 'true' : 'false');
    more.onclick = () => { state.qaAll = !state.qaAll; drawQueue(); };
    box.append(more);
  }
}

// ── the plan ────────────────────────────────────────────────────────
//
// The one bold thing on the page: every sprint from the first to the last as
// columns, every block as a band across the sprints its name says it spans,
// the band filled by how much of it is finished, today as a line through all
// of them. Under the fill, how many of the block's tickets each sprint holds,
// which shows at a glance where the work really sits — including the part of
// a block planned outside its own window.

function drawPlan(focus) {
  const box = $('tk-strip');
  const sprints = datedSprints().filter((s) => s.number != null);
  const list = blocks();
  if (!sprints.length || !list.length) {
    box.replaceChildren(el('p', 'tk-empty', !sprints.length
      ? 'OpenProject has no dated sprints for this project, so there is no plan to draw.'
      : 'No top-level epic in this project, so there are no blocks to draw.'));
    $('tk-plan-note').textContent = '';
    $('tk-plan-title').textContent = 'The plan';
    return;
  }
  const first = sprints[0];
  const last = sprints.at(-1);
  $('tk-plan-title').textContent = `The plan, ${first.name} to ${last.name}`;
  const span = Math.max(1, addDays(last.end, 3) - first.start);
  const at = (d) => Math.max(0, Math.min(1, (d - first.start) / span));
  const sprintLeft = (s) => at(s.start);
  const sprintRight = (s) => at(addDays(s.end, 3));
  const now = today();
  const nowAt = now >= first.start && now <= addDays(last.end, 3) ? at(now) : null;

  // Every ticket under each block, under the person and type filters (the plan
  // is the whole plan, so the sprint filter does not narrow it).
  const pool = scoped('sprint');
  const under = new Map(list.map((b) => [b.key, []]));
  for (const t of pool) {
    const top = tree.top.get(t.key);
    if (top && top !== t && under.has(top.key)) under.get(top.key).push(t);
  }
  const loads = new Map();
  let maxLoad = 1;
  for (const b of list) {
    const m = new Map();
    for (const t of under.get(b.key)) if (t.version) m.set(t.version, (m.get(t.version) ?? 0) + 1);
    loads.set(b.key, m);
    for (const n of m.values()) maxLoad = Math.max(maxLoad, n);
  }

  const strip = el('div', 'tk-strip-grid');
  strip.style.setProperty('--now', nowAt == null ? '-10' : String(nowAt));
  strip.style.setProperty('--cols', String(sprints.length));

  // The scale: sprint numbers over their columns, months under them.
  const scale = el('div', 'tk-strip-scale');
  const cols = el('div', 'tk-strip-cols');
  for (const s of sprints) {
    const col = el('span', `tk-strip-col${focus && s.name === focus.name ? ' is-focus' : ''}`);
    col.style.left = `${sprintLeft(s) * 100}%`;
    col.style.width = `${(sprintRight(s) - sprintLeft(s)) * 100}%`;
    col.append(el('span', 'tk-strip-num', String(s.number)));
    col.dataset.tip = `${s.name}: ${fmtWeekday(s.start)} to ${fmtWeekday(s.end)}`;
    cols.append(col);
  }
  if (nowAt != null) {
    // Centred on the line, except near either end, where it would hang off
    // the panel: there it leans inwards.
    const flag = el('span', `tk-strip-today${nowAt < 0.12 ? ' is-start' : nowAt > 0.88 ? ' is-end' : ''}`, `Today, ${fmtShort(now)}`);
    flag.style.left = `${nowAt * 100}%`;
    cols.append(flag);
  }
  scale.append(el('span', 'tk-strip-corner', 'Sprint'), cols);
  strip.append(scale);

  for (const b of list) {
    const name = blockName(b.subject);
    const tickets = under.get(b.key);
    const c = count(tickets);
    const load = loads.get(b.key);
    const inWindow = (s) => name.from != null && s.number >= name.from && s.number <= name.to;
    // The band: the window in the name, or failing that the sprints its
    // tickets are in.
    let from = name.from != null ? sprints.find((s) => s.number === name.from) : null;
    let to = name.to != null ? [...sprints].reverse().find((s) => s.number <= name.to) : null;
    if (!from || !to) {
      const used = sprints.filter((s) => load.get(s.name));
      from = used[0] ?? null;
      to = used.at(-1) ?? null;
    }

    const row = el('div', 'tk-band-row');
    const label = link(b.url, 'tk-band-label');
    label.append(el('span', 'tk-band-code', name.code || b.subject),
      el('span', 'tk-band-pct', c.live ? share(c.finished, c.live) : '—'),
      el('span', 'tk-band-words', c.live ? `${num(c.finished)} of ${num(c.live)} finished` : 'no tickets in this view'));
    label.title = b.subject;

    const track = el('div', 'tk-band-track');
    if (from && to) {
      const band = el('div', 'tk-band');
      const left = sprintLeft(from);
      band.style.left = `${left * 100}%`;
      band.style.width = `${(sprintRight(to) - left) * 100}%`;
      const fill = el('div', 'tk-band-fill');
      for (const kind of ['done', 'qa']) {
        if (!c[kind]) continue;
        const seg = el('span', `tk-seg-${kind}`);
        seg.style.width = `${(c[kind] / Math.max(1, c.live)) * 100}%`;
        fill.append(seg);
      }
      band.append(fill);
      band.dataset.tip = `${b.subject}: ${num(c.finished)} of ${num(c.live)} finished (${share(c.finished, c.live)})`
        + `, planned ${from.name} to ${to.name}.`;
      track.append(band);
    }
    // How many tickets each sprint holds for this block.
    let outside = 0;
    for (const s of sprints) {
      const n = load.get(s.name) ?? 0;
      if (!n) continue;
      const out = name.from != null && !inWindow(s);
      if (out) outside += n;
      const bar = el('span', `tk-load${out ? ' is-outside' : ''}`);
      bar.style.left = `${sprintLeft(s) * 100}%`;
      bar.style.width = `${(sprintRight(s) - sprintLeft(s)) * 100}%`;
      bar.style.setProperty('--h', String(Math.max(0.08, n / maxLoad)));
      bar.dataset.tip = `${name.code ? `Block ${name.code}` : b.subject} in ${s.name}: ${plural(n, 'ticket', 'tickets')}`
        + (out ? ', outside the block’s planned window' : '');
      track.append(bar);
    }
    const unsprinted = tickets.filter((t) => !t.version).length;
    row.append(label, track);
    row.setAttribute('aria-label', `${b.subject}: ${num(c.finished)} of ${num(c.live)} finished`
      + `${from && to ? `, planned ${from.name} to ${to.name}` : ''}`
      + `${outside ? `, ${num(outside)} tickets in sprints outside that window` : ''}`
      + `${unsprinted ? `, ${num(unsprinted)} in no sprint` : ''}.`);
    row.setAttribute('role', 'group');
    strip.append(row);
  }

  // The months under the columns, so a sprint number can be read as a date.
  const foot = el('div', 'tk-strip-scale');
  const months = el('div', 'tk-strip-months');
  for (let d = new Date(first.start.getFullYear(), first.start.getMonth() + 1, 1); d < addDays(last.end, 3);
    d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) {
    if (at(d) > 0.94) break;      // a label that would run off the end
    const tick = el('span', 'tk-strip-month', `${MONTH[d.getMonth()]}${d.getMonth() === 0 ? ` ${d.getFullYear()}` : ''}`);
    tick.style.left = `${at(d) * 100}%`;
    months.append(tick);
  }
  foot.append(el('span', 'tk-strip-corner', ''), months);
  strip.append(foot);

  box.replaceChildren(strip);
  const loose = pool.filter((t) => !t.version && !/epic/i.test(t.type || '')).length;
  const looseFeatures = pool.filter((t) => !t.version && /feature/i.test(t.type || '')).length;
  $('tk-plan-note').textContent = 'Each band is a block’s planned window, read from its name in OpenProject; '
    + 'the solid start of it is how much is finished. The shaded columns under a band are how many of its tickets '
    + 'each sprint holds, and a column standing outside its band is work planned outside the block’s window. '
    + (loose ? `${plural(loose, 'ticket has', 'tickets have')} no sprint${looseFeatures ? ` (${num(looseFeatures)} of them features, finished when their tickets are)` : ''}.` : '');
}

// ── what needs somebody ─────────────────────────────────────────────

function drawAttention(items) {
  // On hold, with what was last said on it.
  const held = items.filter(isStalled).sort((a, b) => Number(a.key) - Number(b.key));
  $('tk-held-title').textContent = held.length ? `On hold (${num(held.length)})` : 'On hold';
  const heldBox = $('tk-held');
  heldBox.replaceChildren(...held.slice(0, 6).map((t) => {
    const item = el('div', 'tk-att-item');
    const head = el('div', 'tk-att-head');
    head.append(link(t.url, 'tk-key', `#${t.key}`), el('span', 'tk-att-subject', t.subject || '(no subject)'));
    item.append(head, el('p', 'tk-att-meta',
      `${t.assignee ? t.assignee : 'Nobody’s'}, ${t.version || 'no sprint'}, ${t.status}`));
    const why = t.lastComment;
    if (why?.text) {
      // OpenProject comments are Markdown; the emphasis marks are noise here.
      const text = why.text.replace(/\*\*|__|`/g, '').trim();
      const quote = el('blockquote', 'tk-att-why', text.length > 220 ? `${text.slice(0, 220)}…` : text);
      item.append(quote, el('p', 'tk-att-meta', `${why.author || 'Somebody'}, ${fmtDay(why.at)}`));
    } else {
      item.append(el('p', 'tk-att-meta is-quiet', 'No comment on it says why.'));
    }
    return item;
  }));
  if (held.length > 6) heldBox.append(link('#states', 'tk-att-more', `${num(held.length - 6)} more on hold`));
  if (!held.length) heldBox.append(el('p', 'tk-empty', 'Nothing is on hold.'));

  // Late and due: sentences, with the list a click away.
  const late = items.filter(isLate);
  const soon = items.filter(isDueSoon);
  const ownDates = items.filter((t) => t.dueDate).length;
  const due = $('tk-due');
  const lines = [];
  if (!ownDates) lines.push(el('p', 'tk-att-text', 'No ticket carries a due date of its own, so each is due when its sprint ends.'));
  lines.push(el('p', 'tk-att-text', late.length
    ? `${plural(late.length, 'open ticket is', 'open tickets are')} late: past ${ownDates ? 'a due date or ' : ''}the end of ${late.length === 1 ? 'its' : 'their'} sprint.`
    : 'Nothing open is late.'));
  if (soon.length) {
    const ends = [...new Set(soon.map((t) => +dueOn(t)))].sort((a, b) => a - b);
    const when = ends.length === 1 ? `by ${fmtWeekday(new Date(ends[0]))}` : 'in the next seven days';
    const sprintEnd = ends.length === 1 && soon.every((t) => !t.dueDate && t.version)
      ? `, when ${soon[0].version} ends` : '';
    lines.push(el('p', 'tk-att-text', `${plural(soon.length, 'open ticket is', 'open tickets are')} due ${when}${sprintEnd}.`));
  } else {
    lines.push(el('p', 'tk-att-text', 'Nothing open is due in the next seven days.'));
  }
  if (late.length || soon.length) lines.push(link('#dates', 'tk-att-more', 'See the tickets'));
  due.replaceChildren(...lines);

  // The gate, compact.
  const gate = $('tk-gatebox');
  const list = (state.data.testing ?? [])
    .filter((g) => !state.scope.person || gateFor(state.scope.person) === g)
    .sort((a, b) => b.closed - a.closed || a.name.localeCompare(b.name));
  if (!list.length) {
    gate.replaceChildren(el('p', 'tk-att-text', state.scope.person
      ? `${state.scope.person} has not closed a ticket through ADAM, so is not on the gate.`
      : `Nobody has closed a ticket through ADAM in this project yet, so the ${state.data.testEvery ?? 10}-ticket gate has not started for anyone.`));
    return;
  }
  gate.replaceChildren(...list.slice(0, 6).map((g) => {
    const row = el('div', 'tk-att-gate');
    row.append(el('span', 'tk-gate-name', g.name), gateMeter(g, true));
    return row;
  }));
  if (list.length > 6) gate.append(link('#gate', 'tk-att-more', `${num(list.length - 6)} more on the gate`));
}

// ── the testing gate ────────────────────────────────────────────────

const norm = (s) => String(s ?? '').trim().toLowerCase().replace(/\s+/g, ' ');

/** ADAM's account for an OpenProject assignee: the same name, or failing that
 *  the only account whose first name matches. ADAM and OpenProject are two
 *  account systems and nothing links them but the name somebody typed. */
function gateFor(name) {
  const list = state.data.testing ?? [];
  const exact = list.find((g) => norm(g.name) === norm(name));
  if (exact) return exact;
  const first = norm(name).split(' ')[0];
  const close = list.filter((g) => norm(g.name).split(' ')[0] === first);
  return close.length === 1 ? close[0] : null;
}

function gateState(g) {
  if (g.verdict === 'failed') return { tone: 'bad', text: 'sent back', short: 'sent back' };
  if (g.submitted) return { tone: 'warn', text: 'waiting for a check', short: 'waiting' };
  if (g.full) return { tone: 'bad', text: 'full: test now', short: 'test now' };
  return { tone: '', text: `${Math.max(0, g.every - g.closed)} to go`, short: '' };
}

function gateMeter(g, compact = false) {
  const wrap = el('span', 'tk-gate-meter');
  const cells = el('span', 'tk-cells');
  const s = gateState(g);
  for (let i = 0; i < g.every; i += 1) {
    cells.append(el('span', `tk-cell${i < g.closed ? ` is-on${s.tone ? ` is-${s.tone}` : ''}` : ''}`));
  }
  wrap.append(cells, el('span', 'tk-gate-n', `${g.closed}/${g.every}`));
  if (!compact || s.tone) wrap.append(el('span', `tk-gate-say${s.tone ? ` is-${s.tone}` : ''}`, compact ? s.short : s.text));
  wrap.dataset.tip = `${g.name}: ${g.closed} of ${g.every} closed since ${g.lastPassedAt ? `the batch passed on ${fmtDay(g.lastPassedAt)}` : 'they started'}; ${s.text}.`;
  return wrap;
}

function drawGate() {
  const every = state.data.testEvery ?? 10;
  const list = [...(state.data.testing ?? [])]
    .filter((g) => !state.scope.person || gateFor(state.scope.person) === g)
    .sort((a, b) => b.closed - a.closed || a.name.localeCompare(b.name));
  $('tk-gate-lede').textContent =
    `Each developer closes ${every} tickets through ADAM, then tests them and a teammate checks the batch `
    + 'before they can close another. This is how far each one is since their last passed batch. '
    + 'Only closes made through ADAM count; a ticket closed in OpenProject itself is not on the gate.';
  const box = $('tk-gate');
  box.replaceChildren(...list.map((g) => {
    const row = el('div', 'tk-gate-row');
    row.append(
      el('span', 'tk-gate-name', g.name),
      gateMeter(g),
      el('span', 'tk-gate-when', g.lastPassedAt ? `last passed ${fmtDay(g.lastPassedAt)}` : 'no batch passed yet'),
    );
    return row;
  }));
  if (!list.length) {
    box.append(el('p', 'tk-empty', state.scope.person
      ? `${state.scope.person} has not closed a ticket through ADAM in this project, so they are not on the gate.`
      : 'Nobody has closed a ticket through ADAM in this project yet, so nobody is on the gate.'));
  }
  const held = list.filter((g) => g.full || g.submitted || g.verdict === 'failed').length;
  $('tk-gate-count').textContent = list.length
    ? `${plural(list.length, 'developer', 'developers')}${held ? `, ${held} held` : ''}` : '';
}

// ── the people table ────────────────────────────────────────────────

function drawPeopleTable(focus) {
  const k = focus ? clock(focus) : null;
  const rows = sortPeople(people(focus));
  const sprintName = focus?.name ?? 'Sprint';
  $('tk-people-lede').textContent = `Every person's tickets in ${focus ? focus.name : 'no dated sprint'} and in the whole plan, `
    + 'counted by assignee. Finished is closed plus waiting for QA (an open status named QA, review or testing), '
    + 'because that is where a developer’s finished work waits. Against pace is how far their finished count is '
    + 'from an even pace through the sprint’s working days. Late is still the developer’s and past its due date '
    + 'or its sprint’s end. Rejected tickets are closed too but counted apart, so they never read as work delivered.';
  const table = $('tk-people');
  // Every column that carries something. A column of zeros (nothing closed
  // yet, nothing on hold) is said once in the note below the table instead.
  const columns = [
    [`${sprintName}: planned`, (r) => r.c.live, true],
    ['Finished', (r) => r.c.finished, true],
    ['Closed', (r) => r.c.done],
    ['Waiting for QA', (r) => r.c.qa],
    ['In progress', (r) => r.c.going],
    ['On hold', (r) => r.c.stalled],
    ['Not started', (r) => r.c.fresh],
    ...(k?.phase === 'running' ? [['Behind pace', (r) => Math.max(0, r.behind)]] : []),
    ['Whole plan: open', (r) => r.open, true],
    ['Finished in the plan', (r) => r.finishedAll],
    ['Late', (r) => r.lateAll],
  ];
  const kept = columns.filter(([, get, always]) => always || rows.some((r) => get(r)));
  const dropped = columns.filter((col) => !kept.includes(col)).map(([label]) => label.toLowerCase());
  const head = el('tr');
  for (const [label, numeric] of [['Person', false], ...kept.map(([l]) => [l, true]), ['Test gate', false]]) {
    const th = el('th', numeric ? 'is-num' : null, label);
    th.scope = 'col';
    head.append(th);
  }
  const body = el('tbody');
  for (const r of rows) {
    const tr = el('tr', state.scope.person === r.name ? 'is-chosen' : null);
    const name = el('th', null);
    name.scope = 'row';
    const pick = el('button', 'tk-link', r.name);
    pick.type = 'button';
    pick.onclick = () => setScope({ person: state.scope.person === r.name ? '' : r.name });
    name.append(pick);
    tr.append(name);
    for (const [label, get] of kept) {
      const v = get(r);
      tr.append(el('td', `is-num${label === 'Late' && v ? ' is-late' : ''}`, num(v)));
    }
    tr.append(el('td', null, r.gate ? `${r.gate.closed}/${r.gate.every}, ${gateState(r.gate).text}` : '—'));
    body.append(tr);
  }
  $('tk-people-zero').textContent = dropped.length
    ? `Left out because every count in them is zero: ${dropped.join(', ')}.` : '';
  const caption = el('caption', null, `Tickets per person, ${sprintName} and the whole plan`);
  const thead = el('thead');
  thead.append(head);
  table.replaceChildren(caption, thead, body);
  $('tk-people-count').textContent = plural(rows.filter((r) => r.name !== 'Unassigned').length, 'person', 'people');
}

// ── rows of counted things ──────────────────────────────────────────

/** A row of `.admin-row`, with a bar showing its share of the biggest count. */
function barRow(label, value, biggest, tone, extra) {
  const row = el('div', 'admin-row tk-bar-row');
  row.append(el('span', 'tk-bar-label', label));
  const track = el('span', 'tk-bar');
  const fill = el('span', `tk-bar-fill${tone ? ` tk-bar-${tone}` : ''}`);
  fill.style.width = `${biggest ? Math.max(2, Math.round((value / biggest) * 100)) : 0}%`;
  track.append(fill);
  row.append(track, el('span', 'tk-bar-count', num(value)), el('span', 'tk-bar-extra', extra ?? ''));
  return row;
}

function drawStates(items) {
  const order = (state.data.statuses ?? []).map((s) => s.name);
  const counts = new Map(order.map((name) => [name, 0]));
  for (const t of items) counts.set(t.status, (counts.get(t.status) ?? 0) + 1);
  const rows = [...counts.entries()].filter(([, n]) => n > 0);
  const biggest = Math.max(1, ...rows.map(([, n]) => n));
  const box = $('tk-states');
  box.replaceChildren(...rows.map(([name, n]) => {
    const kind = kindOf({ status: name });
    const words = { done: 'closed, finished', qa: 'waiting for QA, finished', rejected: 'closed, not done',
      stalled: 'on hold', fresh: 'not started', going: 'in progress' }[kind];
    return barRow(name, n, biggest, kind, words);
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'No tickets to count.'));
  $('tk-states-count').textContent = `${rows.length} in use`;
}

/** One ticket as a row: number, subject, who, state, date. */
function ticketRow(t, dateLabel) {
  const row = el('div', 'admin-row tk-row');
  const main = el('span', 'tk-main');
  main.append(el('span', 'tk-subject', t.subject || '(no subject)'));
  if (t.parentSubject) main.append(el('span', 'tk-parent', t.parentSubject));
  row.append(link(t.url, 'tk-key', `#${t.key}`), main, el('span', 'tk-who', who(t)), stateBadge(t),
    el('span', 'tk-when', dateLabel ?? ''));
  return row;
}

function badgeTone(t) {
  const kind = kindOf(t);
  if (kind === 'done') return 'done';
  if (kind === 'qa') return 'qa';
  if (kind === 'rejected') return 'rejected';
  if (kind === 'stalled') return 'warn';
  return isLate(t) ? 'bad' : 'open';
}

const stateBadge = (t) => el('span', `tk-badge tk-badge-${badgeTone(t)}`, t.status || '—');

/** A long list drawn a page at a time; the rest is a button away. */
function paged(box, rows, draw1, size, empty) {
  let limit = size;
  const render = () => {
    box.replaceChildren(...rows.slice(0, limit).map(draw1));
    if (rows.length > limit) {
      const more = el('button', 'chip tk-more', `Show ${num(Math.min(size, rows.length - limit))} more of ${num(rows.length - limit)}`);
      more.type = 'button';
      more.onclick = () => { limit += size; render(); };
      box.append(more);
    }
    if (!rows.length) box.append(el('p', 'tk-empty', empty));
  };
  render();
}

function drawDates(items) {
  const late = items.filter(isLate).sort((a, b) => +dueOn(a) - +dueOn(b));
  const soon = items.filter(isDueSoon).sort((a, b) => +dueOn(a) - +dueOn(b) || Number(a.key) - Number(b.key));
  const ownDates = items.filter((t) => t.dueDate).length;
  $('tk-dates-lede').textContent = 'Open tickets past the day they were due, then what falls due in the next seven days. '
    + (ownDates ? 'A ticket with a due date of its own is due then; any other is due when its sprint ends. '
      : 'No ticket in this view has a due date of its own, so each is due when its sprint ends. ')
    + 'Tickets waiting for QA are left out: their developer has finished them.';
  const when = (t) => (t.dueDate ? `due ${fmtDay(asDay(t.dueDate))}` : `${t.version} ends ${fmtShort(dueOn(t))}`);
  paged($('tk-overdue'), late, (t) => ticketRow(t, `${plural(days(dueOn(t), today()), 'day', 'days')} late, ${when(t)}`),
    50, 'Nothing open is late.');
  paged($('tk-soon'), soon, (t) => ticketRow(t, when(t)), 50, 'Nothing open is due in the next seven days.');
  $('tk-dates-count').textContent = `${num(late.length)} late, ${num(soon.length)} due this week`;
}

// A linked artefact is `kind:id`; the ticket rows carry `touches: [{kind, id}]`.
const KIND_LABEL = {
  screen: 'Screens', flow: 'Flows', contract: 'Contracts', operation: 'Operations',
  schema: 'Schemas', table: 'Tables', module: 'Modules', service: 'Services',
  adr: 'Decisions', platform: 'Platforms',
};

function drawDeliverables(items) {
  const byKind = new Map();
  let linked = 0;
  for (const t of items) {
    if (!t.touches?.length) continue;
    linked += 1;
    for (const touch of t.touches) {
      const kind = byKind.get(touch.kind) ?? new Map();
      const list = kind.get(touch.id) ?? [];
      list.push(t);
      kind.set(touch.id, list);
      byKind.set(touch.kind, kind);
    }
  }

  const box = $('tk-deliverables');
  box.replaceChildren();
  const kinds = [...byKind.entries()].sort((a, b) => b[1].size - a[1].size);
  let artefacts = 0;
  for (const [kind, artefactMap] of kinds) {
    artefacts += artefactMap.size;
    const group = el('details', 'tk-group');
    group.open = kinds.length === 1;
    group.append(el('summary', 'tk-sub', `${KIND_LABEL[kind] ?? kind} (${num(artefactMap.size)})`));
    const table = el('div', 'admin-table');
    const rows = [...artefactMap.entries()].sort((a, b) => a[0].localeCompare(b[0]));
    paged(table, rows, ([id, tickets]) => {
      const row = el('div', 'admin-row tk-deliverable');
      const done = tickets.filter(isFinished).length;
      row.append(el('span', 'tk-artefact', id));
      const chips = el('span', 'tk-chips');
      for (const t of tickets.sort((a, b) => Number(a.key) - Number(b.key)).slice(0, 12)) {
        const chip = link(t.url, `tk-badge tk-badge-${badgeTone(t)}`, `#${t.key} ${t.status}`);
        chip.title = t.subject || '';
        chips.append(chip);
      }
      if (tickets.length > 12) chips.append(el('span', 'tk-quiet', `and ${num(tickets.length - 12)} more`));
      row.append(chips, el('span', 'tk-bar-extra',
        done === tickets.length ? 'finished' : tickets.length > 1 ? `${num(done)} of ${num(tickets.length)} finished` : ''));
      return row;
    }, 100, '');
    group.append(table);
    box.append(group);
  }
  if (!kinds.length) {
    box.append(el('p', 'tk-empty',
      'No ticket in this view is linked to a part of the package yet. Claude Code links one with adam_link, '
      + 'and then a ticket and the screen or contract it builds are the same piece of work here.'));
  }
  $('tk-deliverables-count').textContent = artefacts ? plural(artefacts, 'artefact', 'artefacts') : '';
  const loose = items.length - linked;
  $('tk-unlinked').textContent = loose
    ? `${plural(loose, 'ticket is', 'tickets are')} not linked to anything in the package, so ${loose === 1 ? 'it does' : 'they do'} not appear above.`
    : 'Every ticket in this view is linked to something in the package.';
}

// ── features by sprint ──────────────────────────────────────────────
//
// **A view over OpenProject's dates and sprints, nothing of ADAM's own.** There
// is no schedule stored here and no bar to drag (CF-124). A ticket's window is
// its own start and due date where it has them, and otherwise its sprint's;
// TICVAI's tickets carry no dates, so on the live project every bar is drawn
// from sprints. Grouped by block, a row per feature (the level under a block),
// each spanning every ticket beneath it.

const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function windowOf(t) {
  const from = asDay(t.startDate);
  const to = asDay(t.dueDate);
  if (from || to) return [from ?? to, to && from && to < from ? from : (to ?? from)];
  const s = sprintOf(t.version);
  return s?.start && s?.end ? [s.start, s.end] : null;
}

function drawTimeline(items) {
  const box = $('tk-gantt');
  box.replaceChildren();
  const placed = [];
  let undated = 0;
  for (const t of items) {
    if (/epic|feature/i.test(t.type || '') && !t.startDate && !t.dueDate) continue;   // drawn by their tickets
    const at = windowOf(t);
    if (!at) { undated += 1; continue; }
    placed.push([t, at]);
  }
  $('tk-undated').textContent = undated
    ? `${plural(undated, 'ticket has', 'tickets have')} neither a sprint nor a date in OpenProject, so `
      + `${undated === 1 ? 'it is' : 'they are'} not on the chart.`
    : 'Every ticket in this view has a sprint or a date.';
  if (!placed.length) {
    box.append(el('p', 'tk-empty', 'No ticket in this view has a sprint or a date, so there is nothing to place.'));
    $('tk-timeline-count').textContent = '';
    return;
  }

  let first = placed[0][1][0];
  let last = placed[0][1][1];
  for (const [, [from, to]] of placed) {
    if (from < first) first = from;
    if (to > last) last = to;
  }
  const start = new Date(first.getFullYear(), first.getMonth(), 1);
  const end = new Date(last.getFullYear(), last.getMonth() + 1, 0);
  const width = Math.max(1, end - start);
  const at = (d) => `${Math.max(0, Math.min(100, ((d - start) / width) * 100))}%`;

  // Block -> feature -> tickets.
  const groups = new Map();
  for (const [t, when] of placed) {
    const top = tree.top.get(t.key);
    const second = tree.second.get(t.key);
    const groupKey = top && top !== t ? top.key : '';
    const group = groups.get(groupKey) ?? { name: groupKey ? top.subject : 'Not under a block', url: groupKey ? top.url : '', rows: new Map() };
    const rowTicket = second ?? t;
    const rowKey = rowTicket.key;
    const row = group.rows.get(rowKey) ?? { name: rowTicket.subject || `#${rowKey}`, url: rowTicket.url, from: when[0], to: when[1], tickets: [] };
    if (when[0] < row.from) row.from = when[0];
    if (when[1] > row.to) row.to = when[1];
    row.tickets.push(t);
    group.rows.set(rowKey, row);
    groups.set(groupKey, group);
  }

  const scale = el('div', 'tk-gantt-scale');
  for (let d = new Date(start); d <= end; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) {
    const tick = el('div', 'tk-gantt-month', `${MONTH[d.getMonth()]} ${String(d.getFullYear()).slice(2)}`);
    tick.style.left = at(d);
    scale.append(tick);
  }
  const now = today();
  if (now >= start && now <= end) {
    const line = el('div', 'tk-gantt-now');
    line.style.left = at(now);
    line.title = 'today';
    scale.append(line);
  }
  box.append(scale);

  let shown = 0;
  const ordered = [...groups.entries()].sort((a, b) => {
    if (!a[0] !== !b[0]) return a[0] ? -1 : 1;
    return String(a[1].name).localeCompare(String(b[1].name), undefined, { numeric: true });
  });
  ordered.forEach(([, group], index) => {
    const rows = [...group.rows.values()].sort((a, b) => a.from - b.from || a.name.localeCompare(b.name));
    const all = rows.flatMap((r) => r.tickets);
    const done = all.filter(isFinished).length;
    const wrap = el('details', 'tk-gantt-group');
    wrap.open = index === 0;
    wrap.append(el('summary', 'tk-sub', `${group.name}: ${plural(rows.length, 'row', 'rows')}, ${num(done)} of ${num(all.length)} finished`));
    for (const r of rows) {
      const finished = r.tickets.every(isFinished);
      if (state.ganttOpenOnly && finished) continue;
      shown += 1;
      const row = el('div', 'tk-gantt-row');
      const label = link(r.url, 'tk-gantt-label', r.name);
      label.title = r.name;
      const track = el('div', 'tk-gantt-track');
      const late = r.tickets.some(isLate);
      const bar = el('div', `tk-gantt-bar${finished ? ' is-done' : late ? ' is-late' : ''}`);
      bar.style.left = at(r.from);
      bar.style.width = `max(3px, ${((addDays(r.to, 1) - r.from) / width) * 100}%)`;
      const doneHere = r.tickets.filter(isFinished).length;
      const fill = el('div', 'tk-gantt-fill');
      fill.style.width = `${Math.round((doneHere / r.tickets.length) * 100)}%`;
      bar.append(fill);
      bar.dataset.tip = `${r.name}: ${fmtDay(r.from)} to ${fmtDay(r.to)}, ${num(doneHere)} of ${num(r.tickets.length)} finished`
        + (late ? '; something in it is late' : '');
      track.append(bar);
      row.append(label, track, el('span', 'tk-gantt-count', `${num(doneHere)}/${num(r.tickets.length)}`));
      wrap.append(row);
    }
    box.append(wrap);
  });
  if (!shown) box.append(el('p', 'tk-empty', 'Everything placed is finished.'));
  $('tk-timeline-count').textContent = plural(shown, 'row', 'rows');
}

function drawParents(items) {
  const groups = new Map();
  for (const t of items) {
    const key = t.parent ? String(t.parent) : '';
    const group = groups.get(key) ?? { key, name: t.parentSubject || 'No parent', tickets: [] };
    group.tickets.push(t);
    groups.set(key, group);
  }
  const rows = [...groups.values()].sort((a, b) => {
    if (!a.key !== !b.key) return a.key ? -1 : 1;
    return b.tickets.length - a.tickets.length;
  });
  const biggest = Math.max(1, ...rows.map((r) => r.tickets.length));
  paged($('tk-parents'), rows, (r) => {
    const done = r.tickets.filter(isFinished).length;
    const late = r.tickets.filter(isLate).length;
    const extra = [`${num(done)} of ${num(r.tickets.length)} finished`, late ? `${num(late)} late` : ''].filter(Boolean).join(', ');
    const row = barRow(r.name, r.tickets.length, biggest, done === r.tickets.length ? 'done' : late ? 'bad' : 'fresh', extra);
    row.prepend(r.key ? link(`${state.data.endpoint}/work_packages/${r.key}`, 'tk-key', `#${r.key}`)
      : el('span', 'tk-key tk-key-none', '—'));
    return row;
  }, 60, 'No tickets to group.');
  $('tk-parents-count').textContent = plural(rows.filter((r) => r.key).length, 'parent', 'parents');
}

// ── the list, its filters, and the download ─────────────────────────

function drawFilters(items) {
  const statuses = [...new Set(items.map((t) => t.status))].filter(Boolean).sort();
  fillSelect($('tk-status'), 'Every state', statuses, state.filter.status);
}

function shown() {
  const { text, status, openOnly } = state.filter;
  const needle = text.trim().toLowerCase();
  return scoped().filter((t) => {
    if (status && t.status !== status) return false;
    if (openOnly && isClosed(t)) return false;
    if (!needle) return true;
    return [t.key, t.subject, t.assignee, t.parentSubject, t.type, t.version]
      .some((field) => String(field ?? '').toLowerCase().includes(needle));
  }).sort((a, b) => Number(b.key) - Number(a.key));
}

// A list of thousands of rows is thousands of DOM nodes nobody scrolls through;
// the first few hundred are drawn and the rest are a click away, and the CSV
// always carries every row.
const LIST_PAGE = 300;
let listLimit = LIST_PAGE;

function drawList() {
  const rows = shown();
  const box = $('tk-list');
  box.replaceChildren(...rows.slice(0, listLimit).map((t) =>
    ticketRow(t, t.dueDate ? `due ${fmtDay(asDay(t.dueDate))}` : t.version || fmtWhen(t.updatedAt))));
  if (rows.length > listLimit) {
    const more = el('button', 'chip tk-more', `Show ${num(Math.min(LIST_PAGE, rows.length - listLimit))} more of ${num(rows.length - listLimit)}`);
    more.type = 'button';
    more.onclick = () => { listLimit += LIST_PAGE; drawList(); };
    box.append(more);
  }
  if (!rows.length) {
    box.append(el('p', 'tk-empty', state.data.items?.length
      ? 'Nothing matches these filters.'
      : (state.data.note ?? 'This project has no tickets in OpenProject yet.')));
  }
  const all = (state.data.items ?? []).length;
  $('tk-tickets-count').textContent = rows.length === all
    ? plural(rows.length, 'ticket', 'tickets')
    : `${num(rows.length)} of ${num(all)}`;
}

function exportCsv() {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const rows = shown();
  const lines = [
    ['number', 'subject', 'type', 'status', 'finished', 'assignee', 'parent', 'sprint',
      'start', 'due', 'late', 'percentDone', 'created', 'lastChanged', 'artefacts', 'url'].join(','),
    ...rows.map((t) => [
      t.key, t.subject, t.type, t.status, isFinished(t) ? 'yes' : 'no', who(t), t.parentSubject, t.version,
      t.startDate, t.dueDate, isLate(t) ? 'yes' : 'no', t.percentDone, t.createdAt, t.updatedAt,
      (t.touches ?? []).map((x) => `${x.kind}:${x.id}`).join(' '), t.url,
    ].map(esc).join(',')),
  ].join('\r\n');
  // A BOM, so Excel on Windows reads the dashes and quotes as written.
  const url = URL.createObjectURL(new Blob(['﻿' + lines], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  const narrowed = Object.values(state.filter).some(Boolean) || Object.values(state.scope).some(Boolean);
  a.download = `${state.project}-tasks${narrowed ? '-filtered' : ''}-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// ── the tooltip ─────────────────────────────────────────────────────
//
// One for the page. Anything with `data-tip` shows it on hover and on keyboard
// focus. It never holds the only copy of a number: every value is also in a
// label, a sentence or the People table.

function mountTip() {
  const tip = $('tk-tip');
  let owner = null;
  const place = (x, y) => {
    const pad = 12;
    const w = tip.offsetWidth;
    const h = tip.offsetHeight;
    let left = x + pad;
    let top = y - h - pad;
    if (left + w > innerWidth - 8) left = Math.max(8, x - w - pad);
    if (top < 8) top = y + pad + 8;
    tip.style.left = `${left}px`;
    tip.style.top = `${top}px`;
  };
  const show = (target, x, y) => {
    owner = target;
    tip.textContent = target.dataset.tip;
    tip.hidden = false;
    place(x, y);
  };
  const hide = () => { owner = null; tip.hidden = true; };
  document.addEventListener('pointermove', (e) => {
    const target = e.target.closest?.('[data-tip]');
    if (!target) { if (owner && e.pointerType !== 'touch') hide(); return; }
    if (target !== owner) show(target, e.clientX, e.clientY);
    else place(e.clientX, e.clientY);
  });
  document.addEventListener('focusin', (e) => {
    const target = e.target.closest?.('[data-tip]') ?? e.target.querySelector?.(':scope [data-tip]');
    if (!target || !e.target.matches(':focus-visible')) return;
    const box = target.getBoundingClientRect();
    show(target, box.left + box.width / 2, box.top);
  });
  document.addEventListener('focusout', hide);
  document.addEventListener('scroll', hide, { passive: true });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') hide(); });
}

/** The burn-up is drawn to its box's width, so it is drawn again when that changes. */
function redrawBurn() {
  if (!state.data) return;
  const focus = focusSprint();
  if (!focus) return;
  const k = clock(focus);
  if (k.phase === 'ahead') return;
  const items = inFocus(focus);
  const c = count(items);
  if (c.live) drawBurn(focus, items, c, k);
}

// ── start ───────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  // A reader's page, not an administrator's: it shows the delivery and changes
  // nothing on it. The whole delivery team reads it; a client does not (12 Oct).
  if (auth.isClient(state.me)) { denied(); return hideLoader(); }

  state.project = await auth.ensureProject();
  $('tasks').hidden = false;

  const params = new URLSearchParams(location.search);
  state.scope = { person: params.get('who') ?? '', sprint: params.get('sprint') ?? '', type: params.get('type') ?? '' };
  try {
    const saved = localStorage.getItem('adam-tasks-team-sort');
    if (['behind', 'planned', 'done', 'name'].includes(saved)) state.teamSort = saved;
  } catch { /* storage denied */ }
  $('tk-team-sort').value = state.teamSort;

  const picker = $('tk-project');
  try {
    const { projects } = await auth.listProjects();
    const mine = projects.filter((p) => !state.me.projects?.length || state.me.projects.includes(p.id));
    picker.replaceChildren(...mine.map((p) => {
      const option = el('option', null, p.name || p.id);
      option.value = p.id;
      option.selected = p.id === state.project;
      return option;
    }));
    picker.onchange = () => {
      auth.rememberProject(picker.value);
      location.search = `?project=${encodeURIComponent(picker.value)}`;
    };
  } catch { /* the page still works for the current project */ }
  // One project, or none listed: a picker with nothing to pick is a blank box.
  picker.hidden = picker.options.length < 2;

  $('tk-gantt-open').onchange = (e) => {
    state.ganttOpenOnly = e.target.checked;
    drawTimeline(scoped());
  };
  $('tk-scope-person').onchange = (e) => setScope({ person: e.target.value });
  $('tk-scope-sprint').onchange = (e) => setScope({ sprint: e.target.value });
  $('tk-scope-type').onchange = (e) => setScope({ type: e.target.value });
  $('tk-scope-clear').onclick = () => setScope({ person: '', sprint: '', type: '' });
  $('tk-team-sort').onchange = (e) => {
    state.teamSort = e.target.value;
    try { localStorage.setItem('adam-tasks-team-sort', state.teamSort); } catch { /* storage denied */ }
    const focus = focusSprint();
    drawRoster(focus);
    drawPeopleTable(focus);
  };

  $('tk-refresh').onclick = async () => {
    $('tk-refresh').disabled = true;
    await load({ refresh: true });
    $('tk-refresh').disabled = false;
  };
  $('tk-search').oninput = (e) => { state.filter.text = e.target.value; listLimit = LIST_PAGE; drawList(); };
  $('tk-status').onchange = (e) => { state.filter.status = e.target.value; listLimit = LIST_PAGE; drawList(); };
  $('tk-open-only').onchange = (e) => { state.filter.openOnly = e.target.checked; listLimit = LIST_PAGE; drawList(); };
  $('tk-export').onclick = exportCsv;
  mountTip();
  let resizing = 0;
  addEventListener('resize', () => { clearTimeout(resizing); resizing = setTimeout(redrawBurn, 150); });

  loaderSays('Reading the delivery board…');
  await load();
  // One section at a time, driven by the rail. Same mechanism as the settings
  // page; see panels.js.
  mountPanels({ nav: document.querySelector('#tasks .set-nav'), fallback: 'overview',
    onShow: (name) => { if (name === 'overview') redrawBurn(); } });
  hideLoader();
})();
