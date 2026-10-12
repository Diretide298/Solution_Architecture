/**
 * The delivery overview: every ticket in the project's OpenProject project, in
 * every state, for a reader (an admin or a project manager).
 *
 * The viewer already answers "what am I holding" — `adam_board` in Claude Code,
 * one person, open work only. This is the other question, the one asked in a
 * status meeting: where is the delivery, who is holding what, who has finished
 * what, what is late, and which parts of the package nobody has a ticket for.
 * That needs the closed and the rejected tickets too, which is why it is a
 * separate route (`/api/board/overview`) and not the board with a wider filter.
 *
 * **People first.** The page opens on the team: one bar per person, every bar
 * on the same scale, split into closed / awaiting QA / in progress / stalled /
 * not started, with how much of it is late, twelve weeks of finished work and
 * where they stand on the testing gate. Selecting a person (or a sprint, or a ticket type) filters
 * every section, from the counts at the top to the ticket list at the bottom.
 *
 * **Every state name comes from OpenProject.** ADAM keeps no list of statuses:
 * the service hands back the instance's own, each with `isClosed` and
 * `isDefault`. The page sorts every ticket into one of six kinds, and the
 * guesses it has to make are written down here, once:
 *
 *   closed       closed, and not by a status named like "rejected"
 *   awaiting QA  open, in a status named QA / review / test / verify. The
 *                developer has finished it; it is waiting on somebody else.
 *                TICVAI's developers move finished work to "Ready for QA" and
 *                QA closes it, so this is where finished work actually sits.
 *   rejected     closed by a status named reject / cancel / duplicate / won't
 *   stalled      open, in a status named hold / block / wait / pend
 *   not started  open, in the status a new ticket starts in (`isDefault`)
 *   in progress  open, anything else
 *
 * "Finished" — what "how many did Hrushi do" counts — is closed plus awaiting
 * QA. A ticket awaiting QA is never late: its developer is done with it.
 *
 * **When a ticket was finished.** OpenProject 10's list has no closing date and
 * no date a status was reached. Where a close went through ADAM, the service
 * sends the moment it recorded (`closes`); everything else uses the ticket's
 * last change (`updatedAt`), which a later comment can move. The throughput
 * chart says which.
 *
 * **Nothing here writes.** Changing a ticket goes through propose-then-apply in
 * Claude Code, as it does everywhere else; a page that can move somebody else's
 * ticket is a page that moves it by accident.
 */
// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer. Eight pages had none of it.
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
const svg = (tag, attrs = {}) => {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  return node;
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
  teamSort: 'total',
  // The timeline's own switch, kept out of `filter` because that one drives
  // the ticket list at the bottom and these are different questions.
  ganttOpenOnly: false,
};

// Open states that mean the work has stopped. A guess: OpenProject has no
// "blocked" flag, so the name is all there is.
const STALLED = /hold|block|wait|pend/i;
// Closed states that mean the work was not done. Also a guess, and the same
// kind: a closed ticket is "done" unless its status says otherwise.
const DROPPED = /reject|cancel|duplicate|won.?t|invalid|obsolete/i;
// Used only when the instance does not say which status is the default.
const FRESH = /^(new|to ?do|backlog|open|not started)$/i;
// Open states that mean the developer has finished and somebody else is next.
const AWAITING = /\bqa\b|review|test|verif/i;

const DAY = 86_400_000;
const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const asDate = (iso) => { const d = iso ? new Date(iso) : null; return d && !Number.isNaN(+d) ? d : null; };
const days = (from, to) => Math.round((to - from) / DAY);
const fmtDay = (iso) => {
  const d = iso instanceof Date ? iso : asDate(iso);
  return d ? d.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : '—';
};
const fmtShort = (d) => (d ? d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : '—');
const fmtWhen = (iso) => {
  const d = asDate(iso);
  return d ? d.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
};
const plural = (n, one, many) => `${n.toLocaleString()} ${n === 1 ? one : many}`;
const pct = (part, whole) => (whole ? Math.round((part / whole) * 100) : 0);

// ── what a ticket is ────────────────────────────────────────────────
//
// Every question the page asks about one ticket, asked once here so the
// sections cannot disagree about what "done" or "late" means.

/** Closed in OpenProject's sense: finished or rejected, either way not open. */
const isClosed = (t) => state.closedByName.get(t.status) === true;
const isRejected = (t) => isClosed(t) && DROPPED.test(t.status || '');
/** Done: closed as finished. */
const isDone = (t) => isClosed(t) && !isRejected(t);
/** Awaiting QA: open, but the developer's part is finished. */
const isAwaiting = (t) => !isClosed(t) && AWAITING.test(t.status || '');
/** Finished: closed, or handed to QA. What "how many did Hrushi do" counts. */
const isFinished = (t) => isDone(t) || isAwaiting(t);
/** Still the developer's to do: open, and not waiting on QA. */
const isOpenWork = (t) => !isClosed(t) && !isAwaiting(t);
const isStalled = (t) => isOpenWork(t) && STALLED.test(t.status || '');
const isFresh = (t) => isOpenWork(t) && !isStalled(t)
  && (state.defaultStatus.size ? state.defaultStatus.has(t.status) : FRESH.test(t.status || ''));

/** The five kinds, in the order the bars draw them. */
const KINDS = [
  { id: 'done', label: 'Closed' },
  { id: 'qa', label: 'Awaiting QA' },
  { id: 'going', label: 'In progress' },
  { id: 'stalled', label: 'Stalled' },
  { id: 'fresh', label: 'Not started' },
];
const kindOf = (t) => (isRejected(t) ? 'rejected' : isDone(t) ? 'done' : isAwaiting(t) ? 'qa'
  : isStalled(t) ? 'stalled' : isFresh(t) ? 'fresh' : 'going');

const dueOn = (t) => asDate(t.dueDate);
const isOverdue = (t) => { const d = dueOn(t); return isOpenWork(t) && d != null && d < today(); };
const isDueSoon = (t) => {
  const d = dueOn(t);
  return isOpenWork(t) && d != null && d >= today() && d <= new Date(+today() + 7 * DAY);
};
/** Late: still the developer's, and past its due date or its sprint's end. */
const isLate = (t) => {
  if (!isOpenWork(t)) return false;
  if (isOverdue(t)) return true;
  const end = sprintOf(t.version)?.end;
  return !!end && end < today();
};
/** When it was finished: ADAM's own record where a close went through ADAM,
 *  otherwise OpenProject's last change — see the header. */
const closedAt = (t) => (isDone(t) ? asDate(state.data.closes?.[t.key] ?? t.updatedAt)
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
    sprintTable.set(v.name, { name: v.name, start: asDate(v.startDate), end: asDate(v.endDate), fromCalendar: false });
  }
  for (const t of state.data.items ?? []) {
    if (t.version && !sprintTable.has(t.version)) {
      sprintTable.set(t.version, { name: t.version, start: null, end: null, fromCalendar: false });
    }
  }
  for (const s of sprintTable.values()) {
    const n = /^sprint\s+(\d+)$/i.exec(s.name)?.[1];
    if (n && !s.start && !s.end) {
      s.start = new Date(+SPRINT_ONE + (Number(n) - 1) * 14 * DAY);
      s.end = new Date(+s.start + 11 * DAY);
      s.fromCalendar = true;
    }
  }
}
const sprintOf = (name) => (name ? sprintTable.get(name) : null);

/** The sprint today is in: the latest one that has started and not ended more
 *  than a weekend ago. */
function currentSprint() {
  const now = today();
  const started = [...sprintTable.values()]
    .filter((s) => s.start && s.start <= now && (!s.end || +s.end + 3 * DAY >= +now))
    .sort((a, b) => b.start - a.start);
  return started[0] ?? null;
}

// ── the scope ───────────────────────────────────────────────────────

/** The items the page is about, filtered by every page filter except `skip`.
 *  The roster skips the person (it shows everyone, with the one chosen marked)
 *  and the sprint list skips the sprint, for the same reason. */
function scoped(skip = '') {
  const { person, sprint, type } = state.scope;
  return (state.data?.items ?? []).filter((t) => {
    if (skip !== 'person' && person && who(t) !== person) return false;
    if (skip !== 'sprint' && sprint && (t.version || '(no sprint)') !== sprint) return false;
    if (skip !== 'type' && type && (t.type || '') !== type) return false;
    return true;
  });
}

function count(items) {
  const c = { total: items.length, done: 0, qa: 0, going: 0, stalled: 0, fresh: 0, rejected: 0, late: 0 };
  for (const t of items) {
    c[kindOf(t)] += 1;
    if (isLate(t)) c.late += 1;
  }
  c.live = c.total - c.rejected;     // what a share of finished is a share of
  c.finished = c.done + c.qa;
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
    draw();
  } catch (error) {
    // 428 is the service saying the token or the project link is missing. It is
    // not an error the reader can do anything about here, so it gets the panel
    // that says which of the two and where to fix it, not a red line.
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
  // The two causes have different fixes, and the service's sentence names which.
  const projectFault = /admin page|Projects/i.test(why);
  $('unconnected-go').textContent = projectFault ? 'Go to the admin page' : 'Go to settings';
  $('unconnected-go').href = projectFault ? '/admin.html#projects' : '/settings.html#openproject';
}

function denied() {
  $('tasks').hidden = true;
  $('denied').hidden = false;
}

// ── drawing ─────────────────────────────────────────────────────────

function draw() {
  if (!state.data) return;
  const items = scoped();
  drawLede();
  drawScope();
  drawHero(items);
  drawStats(items);
  drawRoster();
  drawThroughput(items);
  drawSprints();
  drawBlocks(items);
  drawPeopleTable();
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
    op.url ? Object.assign(el('a', null, op.name || op.identifier), { href: op.url, target: '_blank', rel: 'noreferrer' })
           : el('span', null, op.name || op.identifier || 'OpenProject'),
    d.truncated ? ' — the newest of a larger project; older tickets are not counted.' : '.',
  );
  const age = d.ageSeconds ?? 0;
  $('tk-asof').textContent = d.fromCache
    ? `Read ${age < 60 ? 'under a minute' : plural(Math.round(age / 60), 'minute', 'minutes')} ago`
    : `Read just now, ${fmtWhen(d.asOf)}`;
  $('tk-asof').dataset.tone = '';
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
  fillSelect($('tk-scope-person'), 'Everyone', people.map(([n, c]) => [n, `${n} (${c})`]), state.scope.person);

  const sprints = [...tally((t) => t.version || '(no sprint)').keys()].sort(bySprint);
  fillSelect($('tk-scope-sprint'), 'Every sprint', sprints.map((n) => [n, n === currentSprint()?.name ? `${n} (current)` : n]),
    state.scope.sprint);

  const types = [...tally((t) => t.type || '').entries()].filter(([n]) => n).sort((a, b) => b[1] - a[1]);
  fillSelect($('tk-scope-type'), 'Every type', types.map(([n, c]) => [n, `${n} (${c})`]), state.scope.type);

  const on = Object.values(state.scope).some(Boolean);
  $('tk-scope-clear').hidden = !on;
  const parts = [];
  if (state.scope.person) parts.push(state.scope.person);
  if (state.scope.sprint) parts.push(state.scope.sprint);
  if (state.scope.type) parts.push(`${state.scope.type} tickets only`);
  const n = scoped().length;
  $('tk-scope-says').textContent = on
    ? `Every section shows ${parts.join(', ')}: ${plural(n, 'ticket', 'tickets')}.`
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
// One component for the hero, every person, every sprint and every block, so a
// state is the same colour and the same place in the bar wherever it appears.
// Segments in the fixed order done / in progress / stalled / not started, a
// 2px gap between them, no border. Rejected tickets are not drawn: they are
// neither work done nor work left, and the tooltip and the table count them.

function stack(c, { scale = 1, label = '' } = {}) {
  const bar = el('div', 'tk-stack');
  const fill = el('div', 'tk-stack-fill');
  fill.style.width = `${Math.max(0, Math.min(1, scale)) * 100}%`;
  for (const kind of KINDS) {
    const n = c[kind.id];
    if (!n) continue;
    const seg = el('span', `tk-seg tk-seg-${kind.id}`);
    seg.style.flexGrow = String(n);
    seg.dataset.tip = `${label ? `${label}: ` : ''}${kind.label} ${n.toLocaleString()} of ${c.live.toLocaleString()} (${pct(n, c.live)}%)`;
    fill.append(seg);
  }
  bar.append(fill);
  bar.setAttribute('role', 'img');
  bar.setAttribute('aria-label', describe(c, label));
  return bar;
}

function describe(c, label) {
  const parts = KINDS.filter((k) => c[k.id]).map((k) => `${c[k.id]} ${k.label.toLowerCase()}`);
  if (c.rejected) parts.push(`${c.rejected} rejected`);
  if (c.late) parts.push(`${c.late} late`);
  return `${label ? `${label}: ` : ''}${plural(c.total, 'ticket', 'tickets')}${parts.length ? `, ${parts.join(', ')}` : ''}.`;
}

function legend(c) {
  const list = el('ul', 'tk-legend');
  for (const kind of KINDS) {
    const item = el('li', 'tk-legend-item');
    item.append(el('span', `tk-key-swatch tk-seg-${kind.id}`), el('span', 'tk-legend-label', kind.label),
      el('span', 'tk-legend-value', `${c[kind.id].toLocaleString()}`));
    list.append(item);
  }
  if (c.rejected) {
    const item = el('li', 'tk-legend-item tk-legend-aside');
    item.append(el('span', 'tk-legend-label', 'Rejected, not drawn'), el('span', 'tk-legend-value', c.rejected.toLocaleString()));
    list.append(item);
  }
  return list;
}

// ── the headline ────────────────────────────────────────────────────

function drawHero(items) {
  const c = count(items);
  $('tk-hero-value').textContent = `${pct(c.finished, c.live)}%`;
  $('tk-hero-label').textContent = `finished, ${c.finished.toLocaleString()} of ${c.live.toLocaleString()} tickets`
    + ` (${c.done.toLocaleString()} closed, ${c.qa.toLocaleString()} awaiting QA)`;
  const bar = stack(c, { label: 'All tickets in view' });
  bar.classList.add('tk-stack-hero');
  $('tk-hero-bar').replaceChildren(bar, legend(c));
}

function tile(value, label, hint, tone) {
  const card = el('div', `tk-tile${tone ? ` is-${tone}` : ''}`);
  const top = el('div', 'tk-tile-top');
  if (tone) top.append(el('span', 'tk-flag', '!'));
  top.append(el('span', 'tk-tile-value', String(value)));
  card.append(top, el('div', 'tk-tile-label', label));
  if (hint) card.append(el('div', 'tk-tile-hint', hint));
  return card;
}

function drawStats(items) {
  const c = count(items);
  const soon = items.filter(isDueSoon);
  const weekAgo = new Date(+today() - 7 * DAY);
  const lastWeek = items.filter((t) => { const at = closedAt(t); return at && at >= weekAgo; });
  const median = medianDaysToClose(items.filter(isFinished));
  $('tk-stats').replaceChildren(
    tile(c.qa.toLocaleString(), 'Awaiting QA', 'finished, waiting on QA'),
    tile(c.going.toLocaleString(), 'In progress', 'open and moving'),
    tile(c.stalled.toLocaleString(), 'Stalled', 'on hold, blocked or waiting', c.stalled ? 'warn' : ''),
    tile(c.late.toLocaleString(), 'Late', 'open, past due date or sprint end', c.late ? 'bad' : ''),
    tile(soon.length.toLocaleString(), 'Due this week', 'open, due in the next seven days'),
    tile(lastWeek.length.toLocaleString(), 'Finished this week', 'closed or to QA, by last change'),
    tile(median == null ? '—' : median, 'Days to finish', median == null ? 'nothing finished yet' : 'median, opened to finished'),
  );
}

function medianDaysToClose(done) {
  const spans = done
    .map((t) => { const a = asDate(t.createdAt); const b = closedAt(t); return a && b ? days(a, b) : null; })
    .filter((n) => n != null && n >= 0)
    .sort((a, b) => a - b);
  if (!spans.length) return null;
  const middle = Math.floor(spans.length / 2);
  return spans.length % 2 ? spans[middle] : Math.round((spans[middle - 1] + spans[middle]) / 2);
}

// ── the team ────────────────────────────────────────────────────────

const WEEKS = 12;

/** The twelve weeks the throughput views share, oldest first, ending today. */
function weekBuckets() {
  const start = new Date(+today() - (WEEKS * 7 - 1) * DAY);
  return { start, buckets: Array.from({ length: WEEKS }, (_, i) => ({ from: new Date(+start + i * 7 * DAY), count: 0 })) };
}
function weekIndex(start, when) {
  if (!when || when < start) return -1;
  return Math.min(WEEKS - 1, Math.floor(days(start, when) / 7));
}

/** One row per person: counts, weekly closes, and their gate if ADAM knows them. */
function people(items) {
  const { start } = weekBuckets();
  const rows = new Map();
  for (const t of items) {
    const name = who(t);
    const row = rows.get(name) ?? { name, items: [], weeks: Array(WEEKS).fill(0), closed7: 0 };
    row.items.push(t);
    const i = weekIndex(start, closedAt(t));
    if (i >= 0) row.weeks[i] += 1;
    const at = closedAt(t);
    if (at && at >= new Date(+today() - 7 * DAY)) row.closed7 += 1;
    rows.set(name, row);
  }
  for (const row of rows.values()) {
    row.c = count(row.items);
    row.gate = gateFor(row.name);
  }
  return [...rows.values()];
}

function sortPeople(rows) {
  const unassignedLast = (a, b) => (a.name === 'Unassigned') - (b.name === 'Unassigned');
  const by = {
    total: (a, b) => b.c.live - a.c.live,
    done: (a, b) => b.c.finished - a.c.finished,
    late: (a, b) => b.c.late - a.c.late || b.c.live - a.c.live,
    name: () => 0,
  }[state.teamSort] ?? (() => 0);
  return rows.sort((a, b) => unassignedLast(a, b) || by(a, b) || a.name.localeCompare(b.name));
}

const initials = (name) => (name === 'Unassigned' ? '–'
  : name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join(''));

function drawRoster() {
  const rows = sortPeople(people(scoped('person')));
  const biggest = Math.max(1, ...rows.map((r) => r.c.live));
  const weekTop = Math.max(1, ...rows.flatMap((r) => r.weeks));
  const box = $('tk-roster');
  box.replaceChildren(...rows.map((r) => {
    const chosen = state.scope.person === r.name;
    const row = el('button', `tk-person${chosen ? ' is-chosen' : ''}${r.name === 'Unassigned' ? ' is-nobody' : ''}`);
    row.type = 'button';
    row.setAttribute('aria-pressed', chosen ? 'true' : 'false');
    row.setAttribute('aria-label', `${describe(r.c, r.name)} ${chosen ? 'Selected; select again to show everyone.' : 'Select to show only their work.'}`);

    const ident = el('span', 'tk-person-who');
    ident.append(el('span', 'tk-avatar', initials(r.name)), el('span', 'tk-person-name', r.name));

    const bar = el('span', 'tk-person-bar');
    bar.append(stack(r.c, { scale: r.c.live / biggest, label: r.name }));

    const done = el('span', 'tk-person-done');
    done.append(el('strong', null, r.c.finished.toLocaleString()), el('span', null, ` of ${r.c.live.toLocaleString()}`));

    const late = el('span', `tk-person-late${r.c.late ? ' has-late' : ''}`);
    if (r.c.late) late.append(el('span', 'tk-flag', '!'), el('span', null, `${r.c.late} late`));
    else late.append(el('span', 'tk-quiet', 'none late'));

    const gate = el('span', 'tk-person-gate');
    if (r.gate) gate.append(gateMeter(r.gate, true));
    else gate.append(el('span', 'tk-quiet', '—'));

    row.append(ident, bar, done, late, spark(r.weeks, weekTop, r.name), gate);
    row.onclick = () => setScope({ person: chosen ? '' : r.name });
    return row;
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'Nobody has a ticket in this view.'));
  const named = rows.filter((r) => r.name !== 'Unassigned').length;
  $('tk-team-count').textContent = plural(named, 'person', 'people');
}

/** Twelve weeks of closes as tiny columns, on the team's common scale. */
function spark(weeks, top, name) {
  const wrap = el('span', 'tk-spark');
  const width = 96;
  const height = 22;
  const step = width / WEEKS;
  const pic = svg('svg', { viewBox: `0 0 ${width} ${height}`, width, height, 'aria-hidden': 'true', focusable: 'false' });
  pic.append(svg('line', { x1: 0, x2: width, y1: height - 0.5, y2: height - 0.5, class: 'tk-spark-base' }));
  const { buckets } = weekBuckets();
  weeks.forEach((n, i) => {
    if (!n) return;
    const h = Math.max(2, (n / top) * (height - 2));
    pic.append(svg('rect', {
      x: i * step + 1, y: height - 1 - h, width: step - 2, height: h, rx: 1.5,
      class: i === WEEKS - 1 ? 'tk-spark-bar is-latest' : 'tk-spark-bar',
    }));
  });
  const total = weeks.reduce((s, n) => s + n, 0);
  wrap.append(pic, el('span', 'tk-spark-total', String(total)));
  wrap.dataset.tip = `${name}: ${plural(total, 'ticket', 'tickets')} finished in ${WEEKS} weeks. `
    + weeks.map((n, i) => `${fmtShort(buckets[i].from)}: ${n}`).filter((_, i) => weeks[i]).join(', ');
  return wrap;
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
    const s = gateState(g);
    row.append(
      el('span', 'tk-gate-name', g.name),
      gateMeter(g),
      el('span', 'tk-gate-when', g.lastPassedAt ? `last passed ${fmtDay(g.lastPassedAt)}` : 'no batch passed yet'),
    );
    if (s.tone === 'bad') row.classList.add('is-bad');
    return row;
  }));
  if (!list.length) {
    box.append(el('p', 'tk-empty', state.scope.person
      ? `${state.scope.person} has not closed a ticket through ADAM in this project, so they are not on the gate.`
      : 'Nobody has closed a ticket through ADAM in this project yet, so nobody is on the gate.'));
  }
  const full = list.filter((g) => g.full || g.submitted || g.verdict === 'failed').length;
  $('tk-gate-count').textContent = list.length
    ? `${plural(list.length, 'developer', 'developers')}${full ? `, ${full} held` : ''}` : '';
}

// ── the people table ────────────────────────────────────────────────

function drawPeopleTable() {
  const rows = sortPeople(people(scoped('person')));
  const table = $('tk-people');
  const head = el('tr');
  for (const [label, numeric] of [['Person', false], ['Tickets', true], ['Finished', true], ['% finished', true],
    ['Closed', true], ['Awaiting QA', true], ['In progress', true], ['Stalled', true], ['Not started', true],
    ['Late', true], ['Rejected', true], ['Finished, 7 days', true], [`Finished, ${WEEKS} weeks`, true],
    ['Test gate', false]]) {
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
    for (const [v, extra] of [[r.c.live], [r.c.finished], [`${pct(r.c.finished, r.c.live)}%`], [r.c.done], [r.c.qa], [r.c.going],
      [r.c.stalled], [r.c.fresh], [r.c.late, r.c.late ? ' is-late' : ''], [r.c.rejected], [r.closed7],
      [r.weeks.reduce((s, n) => s + n, 0)]]) {
      tr.append(el('td', `is-num${extra ?? ''}`, typeof v === 'number' ? v.toLocaleString() : v));
    }
    tr.append(el('td', null, r.gate ? `${r.gate.closed}/${r.gate.every}, ${gateState(r.gate).text}` : '—'));
    body.append(tr);
  }
  const caption = el('caption', null, 'Tickets per person, by state');
  const thead = el('thead');
  thead.append(head);
  table.replaceChildren(caption, thead, body);
  $('tk-people-count').textContent = plural(rows.filter((r) => r.name !== 'Unassigned').length, 'person', 'people');
}

// ── sprints and blocks ──────────────────────────────────────────────

function drawSprints() {
  const items = scoped('sprint');
  const groups = new Map();
  for (const t of items) {
    const name = t.version || '(no sprint)';
    const list = groups.get(name) ?? [];
    list.push(t);
    groups.set(name, list);
  }
  const now = currentSprint();
  const names = [...groups.keys()].sort(bySprint);
  const box = $('tk-sprints');
  let calendar = false;
  box.replaceChildren(...names.map((name) => {
    const list = groups.get(name);
    const c = count(list);
    const s = sprintOf(name);
    if (s?.fromCalendar) calendar = true;
    const isNow = now && now.name === name;
    const ended = s?.end && s.end < today();
    const chosen = state.scope.sprint === name;
    const row = el('button', `tk-sprint${isNow ? ' is-now' : ''}${chosen ? ' is-chosen' : ''}${ended ? ' is-past' : ''}`);
    row.type = 'button';
    row.setAttribute('aria-pressed', chosen ? 'true' : 'false');

    const head = el('span', 'tk-sprint-head');
    head.append(el('span', 'tk-sprint-name', name));
    if (isNow) {
      const left = Math.max(0, days(today(), s.end));
      head.append(el('span', 'tk-now', left ? `now, ${plural(left, 'day', 'days')} left` : 'now, last day'));
    }
    head.append(el('span', 'tk-sprint-dates', s?.start ? `${fmtShort(s.start)} – ${fmtShort(s.end)}` : ''));

    const points = list.filter((t) => typeof t.storyPoints === 'number');
    const ptsDone = points.filter(isFinished).reduce((n, t) => n + t.storyPoints, 0);
    const ptsAll = points.filter((t) => !isRejected(t)).reduce((n, t) => n + t.storyPoints, 0);
    const figures = el('span', 'tk-sprint-figures');
    const share = el('span');
    share.append(el('strong', null, `${c.finished.toLocaleString()}`), ` of ${c.live.toLocaleString()} finished`);
    figures.append(share);
    if (ptsAll) figures.append(el('span', 'tk-pts', `${ptsDone} of ${ptsAll} pts`));
    // An ended sprint with open work is the one thing on this card that needs
    // somebody: those tickets are late by definition.
    const leftover = ended ? c.live - c.finished : 0;
    if (leftover) {
      const warn = el('span', 'tk-sprint-left');
      warn.append(el('span', 'tk-flag', '!'), `${leftover} left over`);
      figures.append(warn);
    }
    row.append(head, stack(c, { label: name }), figures);
    row.setAttribute('aria-label', `${describe(c, name)}${isNow ? ' The current sprint.' : ''}${leftover ? ` ${leftover} still open after it ended.` : ''}`);
    row.onclick = () => setScope({ sprint: chosen ? '' : name });
    return row;
  }));
  if (!names.length) box.append(el('p', 'tk-empty', 'No ticket in this view has a sprint.'));
  $('tk-sprints-count').textContent = now ? `current: ${now.name}` : '';
  $('tk-sprints-lede').textContent = 'Finished (closed or awaiting QA) against everything in each sprint, an OpenProject version. '
    + 'Select one to show only its tickets.'
    + (calendar ? ' Sprints without dates in OpenProject are placed on the TICVAI calendar: two weeks each from 5 October 2026.' : '');
}

/** Each ticket's top-level ancestor, walking the parent chain once per ticket. */
function topOf(byKey, memo, t) {
  if (memo.has(t.key)) return memo.get(t.key);
  const seen = new Set([t.key]);
  let at = t;
  while (at.parent && byKey.has(String(at.parent)) && !seen.has(String(at.parent))) {
    seen.add(String(at.parent));
    at = byKey.get(String(at.parent));
  }
  memo.set(t.key, at);
  return at;
}

function drawBlocks(items) {
  const all = state.data.items ?? [];
  const byKey = new Map(all.map((t) => [String(t.key), t]));
  const memo = new Map();
  const groups = new Map();
  for (const t of items) {
    const top = topOf(byKey, memo, t);
    if (top === t || !/epic/i.test(top.type || '')) continue;
    const list = groups.get(top.key) ?? [];
    list.push(t);
    groups.set(top.key, list);
  }
  const box = $('tk-blocks');
  const rows = [...groups.entries()].sort((a, b) => {
    const ta = byKey.get(a[0]);
    const tb = byKey.get(b[0]);
    return String(ta.subject).localeCompare(String(tb.subject), undefined, { numeric: true });
  });
  const biggest = Math.max(1, ...rows.map(([, list]) => list.length));
  box.replaceChildren(...rows.map(([key, list]) => {
    const epic = byKey.get(key);
    const c = count(list);
    const row = el('div', 'tk-blockrow');
    const name = el('a', 'tk-blockrow-name', epic.subject || `#${key}`);
    name.href = epic.url; name.target = '_blank'; name.rel = 'noreferrer';
    const figures = el('span', 'tk-blockrow-figures');
    const share = el('span');
    share.append(el('strong', null, `${pct(c.finished, c.live)}%`), ` ${c.finished.toLocaleString()} of ${c.live.toLocaleString()}`);
    figures.append(share);
    if (c.late) {
      const late = el('span', 'tk-person-late has-late');
      late.append(el('span', 'tk-flag', '!'), `${c.late} late`);
      figures.append(late);
    }
    row.append(name, stack(c, { scale: c.live / biggest, label: epic.subject }), figures);
    return row;
  }));
  $('blocks').hidden = !rows.length;
  $('tk-blocks-count').textContent = rows.length ? plural(rows.length, 'epic', 'epics') : '';
}

/** A row of `.admin-row`, with a bar showing its share of the biggest count. */
function barRow(label, value, biggest, tone, extra) {
  const row = el('div', 'admin-row tk-bar-row');
  row.append(el('span', 'tk-bar-label', label));
  const track = el('span', 'tk-bar');
  const fill = el('span', `tk-bar-fill${tone ? ` tk-bar-${tone}` : ''}`);
  fill.style.width = `${biggest ? Math.max(2, Math.round((value / biggest) * 100)) : 0}%`;
  track.append(fill);
  row.append(track, el('span', 'tk-bar-count', value.toLocaleString()), el('span', 'tk-bar-extra', extra ?? ''));
  return row;
}

function drawStates(items) {
  const order = (state.data.statuses ?? []).map((s) => s.name);
  const counts = new Map(order.map((name) => [name, 0]));
  for (const t of items) counts.set(t.status, (counts.get(t.status) ?? 0) + 1);
  // OpenProject's order first, then any status the instance no longer lists.
  const rows = [...counts.entries()].filter(([, n]) => n > 0);
  const biggest = Math.max(1, ...rows.map(([, n]) => n));
  const box = $('tk-states');
  box.replaceChildren(...rows.map(([name, n]) => {
    const probe = { status: name };
    const kind = kindOf(probe);
    const tone = { done: 'done', qa: 'qa', rejected: 'rejected', stalled: 'stalled', fresh: 'fresh', going: 'going' }[kind];
    const words = { done: 'closed, finished', qa: 'awaiting QA, finished', rejected: 'closed, not done', stalled: 'stalled', fresh: 'not started', going: 'in progress' }[kind];
    return barRow(name, n, biggest, tone, words);
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'No tickets to count.'));
  $('tk-states-count').textContent = `${rows.length} in use`;
}

/** One ticket as a row: number, subject, who, state, date. */
function ticketRow(t, dateLabel) {
  const row = el('div', 'admin-row tk-row');
  const number = el('a', 'tk-key', `#${t.key}`);
  number.href = t.url; number.target = '_blank'; number.rel = 'noreferrer';
  const main = el('span', 'tk-main');
  main.append(el('span', 'tk-subject', t.subject || '(no subject)'));
  if (t.parentSubject) main.append(el('span', 'tk-parent', t.parentSubject));
  row.append(number, main, el('span', 'tk-who', who(t)), stateBadge(t), el('span', 'tk-when', dateLabel ?? ''));
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

function stateBadge(t) {
  return el('span', `tk-badge tk-badge-${badgeTone(t)}`, t.status || '—');
}

function drawDates(items) {
  const overdue = items.filter(isOverdue).sort((a, b) => +dueOn(a) - +dueOn(b));
  const soon = items.filter(isDueSoon).sort((a, b) => +dueOn(a) - +dueOn(b));

  const late = $('tk-overdue');
  late.replaceChildren(...overdue.map((t) => {
    const by = days(dueOn(t), today());
    return ticketRow(t, `${plural(by, 'day', 'days')} late, due ${fmtDay(t.dueDate)}`);
  }));
  if (!overdue.length) late.append(el('p', 'tk-empty', 'Nothing open is past its due date.'));

  const next = $('tk-soon');
  next.replaceChildren(...soon.map((t) => ticketRow(t, `due ${fmtDay(t.dueDate)}`)));
  if (!soon.length) next.append(el('p', 'tk-empty', 'Nothing open is due in the next seven days.'));

  const undated = items.filter((t) => isOpenWork(t) && !dueOn(t)).length;
  $('tk-dates-count').textContent = `${overdue.length} overdue, ${soon.length} this week`;
  $('tk-soon-title').textContent = undated
    ? `Due in the next seven days — ${plural(undated, 'open ticket has', 'open tickets have')} no due date`
    : 'Due in the next seven days';
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
    const group = el('div', 'tk-group');
    group.append(el('h3', 'tk-sub', `${KIND_LABEL[kind] ?? kind} (${artefactMap.size})`));
    const table = el('div', 'admin-table');
    const rows = [...artefactMap.entries()].sort((a, b) => a[0].localeCompare(b[0]));
    for (const [id, tickets] of rows) {
      const row = el('div', 'admin-row tk-deliverable');
      const done = tickets.filter(isFinished).length;
      row.append(el('span', 'tk-artefact', id));
      const chips = el('span', 'tk-chips');
      for (const t of tickets.sort((a, b) => Number(a.key) - Number(b.key))) {
        const chip = el('a', `tk-badge tk-badge-${badgeTone(t)}`, `#${t.key} ${t.status}`);
        chip.href = t.url; chip.target = '_blank'; chip.rel = 'noreferrer';
        chip.title = t.subject || '';
        chips.append(chip);
      }
      // With one ticket the chip beside it already says the state, so the only
      // thing worth adding is the count when there is more than one.
      row.append(chips, el('span', 'tk-bar-extra',
        done === tickets.length ? 'finished'
          : tickets.length > 1 ? `${done} of ${tickets.length} finished` : ''));
      table.append(row);
    }
    group.append(table);
    box.append(group);
  }
  if (!kinds.length) {
    box.append(el('p', 'tk-empty',
      'No ticket in this view is linked to a part of the package yet. Claude Code links one with adam_link, '
      + 'and then a ticket and the screen or contract it builds are the same piece of work here.'));
  }
  $('tk-deliverables-count').textContent = artefacts ? `${plural(artefacts, 'artefact', 'artefacts')}` : '';
  const loose = items.length - linked;
  $('tk-unlinked').textContent = loose
    ? `${plural(loose, 'ticket is', 'tickets are')} not linked to anything in the package, so ${loose === 1 ? 'it does' : 'they do'} not appear above.`
    : 'Every ticket in this view is linked to something in the package.';
}

// ── the timeline ────────────────────────────────────────────────────
//
// **A view over OpenProject's dates and nothing of ADAM's own.** There is no
// schedule stored here, no bar to drag, and no way to move a date from this
// page — CF-124, the same reason the board cannot reassign a ticket. Moving
// work means moving it where the plan lives.
//
// Grouped by version, because that is where the delivery plan's milestones
// land in OpenProject, then by epic. An epic's bar spans the earliest start to
// the latest date among its own tickets: a parent usually carries no dates
// itself, so taking its own would draw almost nothing.

const MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** The window a ticket occupies. A ticket with only one of the two dates is a
 *  point rather than a span — drawing it as "from the beginning of time" is the
 *  version of this that makes every chart look like one long bar. */
function span(t) {
  const from = asDate(t.startDate);
  const to = asDate(t.dueDate);
  if (from && to) return [from, to < from ? from : to];
  if (from) return [from, from];
  if (to) return [to, to];
  return null;
}

function drawTimeline(items) {
  const box = $('tk-gantt');
  box.replaceChildren();

  // Milestone -> epic -> tickets, keeping only what can be placed.
  const placed = [];
  let undated = 0;
  for (const t of items) {
    const at = span(t);
    if (!at) { undated += 1; continue; }
    placed.push([t, at]);
  }
  $('tk-undated').textContent = undated
    ? `${plural(undated, 'ticket has', 'tickets have')} no start or due date in OpenProject, so `
      + `${undated === 1 ? 'it is' : 'they are'} not on the chart.`
    : 'Every ticket in this view has a date.';

  if (!placed.length) {
    box.append(el('p', 'tk-empty',
      'No ticket in this view carries a start or a due date, so there is nothing '
      + 'to place on a timeline. Dates are set in OpenProject.'));
    $('tk-timeline-count').textContent = '';
    return;
  }

  let first = placed[0][1][0];
  let last = placed[0][1][1];
  for (const [, [from, to]] of placed) {
    if (from < first) first = from;
    if (to > last) last = to;
  }
  // Whole months, so the gridlines are dates somebody recognises rather than
  // wherever the first ticket happened to start.
  const start = new Date(first.getFullYear(), first.getMonth(), 1);
  const end = new Date(last.getFullYear(), last.getMonth() + 1, 0);
  const width = Math.max(1, end - start);
  const at = (d) => `${Math.max(0, Math.min(100, ((d - start) / width) * 100))}%`;

  const milestones = new Map();
  for (const [t, when] of placed) {
    const key = t.version || '';
    const group = milestones.get(key) ?? { name: t.version || 'No milestone', epics: new Map() };
    const epicKey = t.parent ? String(t.parent) : `loose:${t.key}`;
    const epic = group.epics.get(epicKey) ?? {
      key: t.parent ? String(t.parent) : '',
      name: t.parentSubject || (t.parent ? `#${t.parent}` : t.subject || `#${t.key}`),
      from: when[0], to: when[1], tickets: [],
    };
    if (when[0] < epic.from) epic.from = when[0];
    if (when[1] > epic.to) epic.to = when[1];
    epic.tickets.push(t);
    group.epics.set(epicKey, epic);
    milestones.set(key, group);
  }

  // The months, once, above everything.
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
  const groups = [...milestones.entries()].sort((a, b) => {
    if (!a[0] !== !b[0]) return a[0] ? -1 : 1;          // "No milestone" last
    const ea = Math.min(...[...a[1].epics.values()].map((e) => +e.from));
    const eb = Math.min(...[...b[1].epics.values()].map((e) => +e.from));
    return ea - eb;
  });
  for (const [, group] of groups) {
    const epics = [...group.epics.values()].sort((a, b) => a.from - b.from);
    const allDone = epics.every((e) => e.tickets.every(isFinished));
    if (state.ganttOpenOnly && allDone) continue;

    const wrap = el('div', 'tk-gantt-group');
    const total = epics.reduce((n, e) => n + e.tickets.length, 0);
    const done = epics.reduce((n, e) => n + e.tickets.filter(isFinished).length, 0);
    wrap.append(el('h3', 'tk-sub', `${group.name} — ${done} of ${total} finished`));

    for (const epic of epics) {
      shown += 1;
      const row = el('div', 'tk-gantt-row');
      const label = el('span', 'tk-gantt-label', epic.name);
      label.title = epic.name;
      row.append(label);

      const track = el('div', 'tk-gantt-track');
      const late = epic.tickets.some(isOverdue);
      const finished = epic.tickets.every(isFinished);
      const bar = el('div', `tk-gantt-bar${finished ? ' is-done' : late ? ' is-late' : ''}`);
      bar.style.left = at(epic.from);
      // A single-day epic would be zero wide and invisible, so it gets a floor.
      bar.style.width = `max(3px, ${((epic.to - epic.from) / width) * 100}%)`;
      const share = epic.tickets.length
        ? epic.tickets.filter(isFinished).length / epic.tickets.length : 0;
      const fill = el('div', 'tk-gantt-fill');
      fill.style.width = `${Math.round(share * 100)}%`;
      bar.append(fill);
      // Newlines as escapes, not as real line breaks: a tooltip built from a
      // template literal spanning lines carries the source indentation into
      // the tooltip.
      bar.title = [
        epic.name,
        `${fmtDay(epic.from)} – ${fmtDay(epic.to)}`,
        `${epic.tickets.filter(isFinished).length} of ${epic.tickets.length} finished`,
        late ? 'something in it is overdue' : '',
      ].filter(Boolean).join('\n');
      track.append(bar);
      row.append(track);
      row.append(el('span', 'tk-gantt-count',
        `${epic.tickets.filter(isFinished).length}/${epic.tickets.length}`));
      wrap.append(row);
    }
    box.append(wrap);
  }
  if (!shown) {
    box.append(el('p', 'tk-empty', 'Everything with a date is finished.'));
  }
  $('tk-timeline-count').textContent = plural(shown, 'epic', 'epics');
}

function drawParents(items) {
  const groups = new Map();
  for (const t of items) {
    const key = t.parent ? String(t.parent) : '';
    const group = groups.get(key) ?? { key, name: t.parentSubject || 'No epic', tickets: [] };
    group.tickets.push(t);
    groups.set(key, group);
  }
  const rows = [...groups.values()].sort((a, b) => {
    if (!a.key !== !b.key) return a.key ? -1 : 1;       // "No epic" last
    return b.tickets.length - a.tickets.length;
  });
  const biggest = Math.max(1, ...rows.map((r) => r.tickets.length));
  const box = $('tk-parents');
  box.replaceChildren(...rows.map((r) => {
    const done = r.tickets.filter(isFinished).length;
    const late = r.tickets.filter(isOverdue).length;
    const extra = [`${done} of ${r.tickets.length} finished`, late ? `${late} overdue` : ''].filter(Boolean).join(', ');
    const row = barRow(r.name, r.tickets.length, biggest, done === r.tickets.length ? 'done' : late ? 'bad' : 'going', extra);
    if (r.key) {
      const link = el('a', 'tk-key', `#${r.key}`);
      link.href = `${state.data.endpoint}/work_packages/${r.key}`;
      link.target = '_blank'; link.rel = 'noreferrer';
      row.prepend(link);
    } else {
      row.prepend(el('span', 'tk-key tk-key-none', '—'));
    }
    return row;
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'No tickets to group.'));
  $('tk-parents-count').textContent = plural(rows.filter((r) => r.key).length, 'epic', 'epics');
}

/**
 * A "nice" ceiling for the axis: 1, 2, 5 or 10 times a power of ten.
 *
 * The old chart scaled every bar against the tallest week, which makes a good
 * week and a bad week look identical whenever both are the tallest thing on
 * screen — the shape changed but the reading never did. A rounded ceiling with
 * labelled gridlines means the bars keep their meaning between refreshes.
 */
function niceMax(value) {
  // Small counts get an even ceiling so the midpoint gridline is a whole
  // ticket. Above ten the usual 1/2/5 steps, which are already even or are
  // drawn without a midpoint.
  if (value <= 10) return Math.max(2, value + (value % 2));
  const power = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 5, 10]) {
    const candidate = step * power;
    if (candidate >= value) return candidate;
  }
  return 10 * power;
}

function drawThroughput(items) {
  const { start, buckets } = weekBuckets();
  for (const b of buckets) { b.done = 0; b.qa = 0; }
  let fromAdam = 0;
  let done = 0;
  for (const t of items) {
    if (!isFinished(t)) continue;
    const i = weekIndex(start, closedAt(t));
    if (i < 0) continue;
    const kind = isDone(t) ? 'done' : 'qa';
    buckets[i][kind] += 1;
    buckets[i].count += 1;
    if (kind === 'done') done += 1;
    if (kind === 'done' && state.data.closes?.[t.key]) fromAdam += 1;
  }

  const counts = buckets.map((b) => b.count);
  const finished = counts.reduce((sum, n) => sum + n, 0);
  const top = niceMax(Math.max(1, ...counts));
  const mean = finished / WEEKS;
  const peak = Math.max(...counts);

  const box = $('tk-weeks');
  box.replaceChildren();

  // Two series, stacked: closed at the baseline, awaiting QA on top. The legend
  // names both; the total over the peak and the latest week is the one label.
  const key = el('ul', 'tk-legend tk-legend-small');
  for (const kind of KINDS.slice(0, 2)) {
    const item = el('li', 'tk-legend-item');
    item.append(el('span', `tk-key-swatch tk-seg-${kind.id}`), el('span', 'tk-legend-label', kind.label),
      el('span', 'tk-legend-value', buckets.reduce((n, b) => n + b[kind.id], 0).toLocaleString()));
    key.append(item);
  }

  // The plot: gridlines behind, bars in front, one baseline under both.
  const plot = el('div', 'tk-thr-plot');
  const grid = el('div', 'tk-thr-grid');
  // Only ever two or three lines, and the midpoint only when it lands on a
  // whole ticket, because "2.5 tickets finished" is a quantity nobody has had.
  const ticks = top % 2 === 0 ? [top, top / 2, 0] : [top, 0];
  for (const at of ticks) {
    const line = el('div', 'tk-thr-line');
    line.style.bottom = `${(at / top) * 100}%`;
    line.append(el('span', 'tk-thr-tick', String(Math.round(at * 10) / 10)));
    grid.append(line);
  }
  plot.append(grid);

  // The average, as the one annotation worth a line of its own: the question a
  // throughput chart is actually asked is "is this week normal".
  if (finished) {
    const avg = el('div', 'tk-thr-mean');
    avg.style.bottom = `${(mean / top) * 100}%`;
    avg.append(el('span', 'tk-thr-mean-label', `avg ${Math.round(mean * 10) / 10}`));
    plot.append(avg);
  }

  const bars = el('div', 'tk-thr-bars');
  buckets.forEach((b, i) => {
    const column = el('div', 'tk-thr-col');
    column.tabIndex = 0;
    const label = `Week of ${fmtDay(b.from)}: ${plural(b.count, 'ticket', 'tickets')} finished`
      + (b.count ? ` (${b.done} closed, ${b.qa} to QA)` : '');
    column.setAttribute('aria-label', label);
    column.dataset.tip = label;
    // A week where nothing finished draws nothing. A minimum-height bar on a
    // zero is a week that looks like it delivered a little.
    const bar = el('div', 'tk-thr-bar');
    bar.style.height = b.count ? `${(b.count / top) * 100}%` : '0';
    if (i === WEEKS - 1) bar.classList.add('is-latest');
    for (const kind of ['qa', 'done']) {
      if (!b[kind]) continue;
      const seg = el('span', `tk-thr-seg tk-seg-${kind}`);
      seg.style.flexGrow = String(b[kind]);
      bar.append(seg);
    }
    // Labelled selectively — the peak and the week just gone.
    if (b.count && (b.count === peak || i === WEEKS - 1)) {
      column.append(Object.assign(el('span', 'tk-thr-value', String(b.count)),
        { style: `bottom:calc(${(b.count / top) * 100}% + 4px)` }));
    }
    column.append(bar);
    bars.append(column);
  });
  plot.append(bars);

  // Every fourth week is named; the ones between read from their neighbours.
  const axis = el('div', 'tk-thr-axis');
  buckets.forEach((b, i) => {
    const cell = el('div', 'tk-thr-when');
    if (i % 4 === 0 || i === WEEKS - 1) cell.textContent = fmtShort(b.from);
    axis.append(cell);
  });

  // The table twin, for anything not looking at the picture.
  const table = el('table', 'tk-thr-table');
  const caption = el('caption', null, `Tickets finished each week for the last ${WEEKS} weeks`);
  const head = el('tr');
  head.append(el('th', null, 'Week beginning'), el('th', null, 'Closed'), el('th', null, 'Moved to QA'), el('th', null, 'Finished'));
  const thead = el('thead');
  thead.append(head);
  const body = el('tbody');
  for (const b of buckets) {
    const row = el('tr');
    row.append(el('th', null, fmtDay(b.from)), el('td', null, String(b.done)), el('td', null, String(b.qa)),
      el('td', null, String(b.count)));
    body.append(row);
  }
  table.append(caption, thead, body);
  box.append(key, plot, axis, table);

  $('tk-throughput-who').textContent = state.scope.person || 'everyone';
  const median = medianDaysToClose(items.filter(isFinished));
  const adam = fromAdam
    ? ` ${plural(fromAdam, 'close', 'closes')} went through ADAM and ${fromAdam === 1 ? 'is' : 'are'} placed by when ADAM closed ${fromAdam === 1 ? 'it' : 'them'}.`
    : '';
  $('tk-throughput-lede').textContent =
    `${plural(finished, 'ticket', 'tickets')} finished in the last ${WEEKS} weeks: ${done} closed, `
    + `${finished - done} moved to QA. A ticket counts in the week it last changed, because OpenProject `
    + 'does not say when a status was reached; a later comment can move it.' + adam
    + (median == null ? '' : ` Median ${plural(median, 'day', 'days')} from opened to finished.`);
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
    ticketRow(t, t.dueDate ? `due ${fmtDay(t.dueDate)}` : fmtWhen(t.updatedAt))));
  if (rows.length > listLimit) {
    const more = el('button', 'chip tk-more', `Show ${Math.min(LIST_PAGE, rows.length - listLimit)} more of ${(rows.length - listLimit).toLocaleString()}`);
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
    : `${rows.length.toLocaleString()} of ${all.toLocaleString()}`;
}

function exportCsv() {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const rows = shown();
  const lines = [
    ['number', 'subject', 'type', 'status', 'finished', 'assignee', 'epic', 'milestone',
      'start', 'due', 'overdue', 'percentDone', 'created', 'lastChanged', 'artefacts', 'url'].join(','),
    ...rows.map((t) => [
      t.key, t.subject, t.type, t.status, isClosed(t) ? 'yes' : 'no', who(t), t.parentSubject, t.version,
      t.startDate, t.dueDate, isOverdue(t) ? 'yes' : 'no', t.percentDone, t.createdAt, t.updatedAt,
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
// focus, at once rather than after a native `title`'s second. It never holds
// the only copy of a number: every value is also in a label, a legend or the
// People table.

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

// ── start ───────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  // A reader's page, not an administrator's: it shows the delivery and changes
  // nothing on it. A pm was refused here, which left the role with no view of
  // the thing it exists to oversee.
  if (auth.isClient(state.me)) { denied(); return hideLoader(); }  // the delivery team reads it (12 Oct)

  state.project = await auth.ensureProject();
  $('tasks').hidden = false;

  const params = new URLSearchParams(location.search);
  state.scope = { person: params.get('who') ?? '', sprint: params.get('sprint') ?? '', type: params.get('type') ?? '' };
  try { state.teamSort = localStorage.getItem('adam-tasks-team-sort') || 'total'; } catch { /* storage denied */ }
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
    drawRoster();
    drawPeopleTable();
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

  loaderSays('Reading the delivery board…');
  await load();
  // One section at a time, driven by the rail. Same mechanism as the settings
  // page; see panels.js.
  mountPanels({ nav: document.querySelector('#tasks .set-nav'), fallback: 'overview' });
  hideLoader();
})();
