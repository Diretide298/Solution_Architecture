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

// **The tickets are asked for before anything else on the page is** (13
// October). They are the page, and they were the last thing asked for: the
// sign-in check, then the project list, then the team file, then this, one
// round trip after another, and only then the long one. Asked here, at the top
// of the module, they travel beside the sign-in check instead of after it.
//
// Nothing is lost by asking before the sign-in check has answered. Signed out,
// this comes back 401 and is ignored, because `requireSignIn` below is already
// on its way to the sign-in page; signed in, it is exactly the request `load()`
// would have made a second later. The project is the same one the page
// settles on below, from the same promise.
const firstAnswer = auth.ensureProject().then((project) => auth.boardOverview(project));
firstAnswer.catch(() => { /* answered by load(), or the page is leaving */ });

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
  team: null,      // docs/active/team.json's people, for a person's role
  changes: null,   // ADAM's change requests, read when somebody opens a person
  // When the tickets on the page were read, and whether a newer read is
  // running or the last one failed. See `drawAsOf`.
  read: { asOf: null, ageSeconds: 0, receivedAt: 0, refreshing: false, error: null },
  ganttOpenOnly: false,
  // What every count on the page counts: 'tasks' (OpenProject type Task, the
  // unit the plan is made of) or 'tickets' (every work package: features,
  // tasks and sub-tasks together). In the address as ?count= and remembered
  // per reader. Switching redraws from the tickets already read; nothing is
  // asked of the service again.
  unit: 'tasks',
  // Finished each day: the days shown ('' = the sprint filter's or the current
  // sprint, 'sprint:<name>', 'last15'), the number picked, and what is behind
  // each number.
  fdRange: '',
  fdPick: null,
  fdCells: null,
};

/** One of the unit, and many: "task"/"tasks" or "ticket"/"tickets". */
const W1 = () => (state.unit === 'tasks' ? 'task' : 'ticket');
const Ws = () => (state.unit === 'tasks' ? 'tasks' : 'tickets');
/** A count with its unit: "46 tasks", "1 ticket". */
const nu = (n) => plural(n, W1(), Ws());
/** "Tasks" / "Tickets", for a heading. */
const WsCap = () => (state.unit === 'tasks' ? 'Tasks' : 'Tickets');
/** Whether a ticket is counted in the current unit. */
const inUnit = (t) => state.unit === 'tickets' || t.type === 'Task';
/** The type filter applies to tickets; in tasks every row is a Task already. */
const typeOk = (t) => state.unit === 'tasks' || !state.scope.type || (t.type || '') === state.scope.type;
let unitMemo = { data: null, unit: '', list: [] };
/** Every ticket in the current unit, kept until the data or the unit changes. */
function counted() {
  const data = state.data;
  if (unitMemo.data !== data?.items || unitMemo.unit !== state.unit) {
    unitMemo = { data: data?.items, unit: state.unit, list: (data?.items ?? []).filter(inUnit) };
  }
  return unitMemo.list;
}

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
  return counted().filter((t) => {
    if (skip !== 'person' && person && who(t) !== person) return false;
    if (skip !== 'sprint' && sprint && (t.version || '(no sprint)') !== sprint) return false;
    if (skip !== 'type' && type && state.unit === 'tickets' && (t.type || '') !== type) return false;
    return true;
  });
}
/** The focus sprint's tickets, under the type filter and, unless `everyone`,
 *  the person filter. The sprint filter is the focus itself. */
const inFocus = (focus, { everyone = false } = {}) => (focus
  ? counted().filter((t) => t.version === focus.name
    && (everyone || !state.scope.person || who(t) === state.scope.person)
    && typeOk(t))
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
  params.delete('who');   // the old name for `person`, read once on arrival
  for (const key of ['person', 'sprint', 'type']) {
    if (state.scope[key]) params.set(key, state.scope[key]); else params.delete(key);
  }
  params.set('count', state.unit);
  const query = params.toString();
  history.replaceState(null, '', `${location.pathname}${query ? `?${query}` : ''}${location.hash}`);
  draw();
}

/** Count in tasks or in tickets: every section redraws from what is loaded. */
function setUnit(unit) {
  if (unit === state.unit) return;
  state.unit = unit;
  try { localStorage.setItem('adam-tasks-count', unit); } catch { /* storage denied */ }
  listLimit = LIST_PAGE;
  setScope({});
}

// ── reading ─────────────────────────────────────────────────────────
//
// **The service never makes this page wait on OpenProject**, and the page's half
// of that is to ask again rather than to wait. Three answers come back:
//
//   the tickets, as read some minutes ago. Drawn at once. When `refreshing` is
//   set a newer read is under way behind it — after a Refresh, or because the
//   held one was past its five minutes — and the page says "Refreshing…" and
//   asks again every ten seconds until it is not, then draws what came.
//
//   `reading`: nobody has read this project before (or not since the service
//   was installed). The page shows its frame with one honest line about the
//   first read, and asks again every five seconds until the tickets come.
//
//   an error, said as one, as before.
//
// There is one timer, so a Refresh pressed while the page is already asking
// replaces the waiting ask rather than adding a second one.
//
// **Refresh starts a read now, and joins one already running.** The service
// keeps one read per project, so pressing it while the five-minute loop or
// somebody else's Refresh is reading attaches this page to that read rather
// than starting a second. While a read runs — whoever started it — the button
// says "Refreshing…" and is down, and the held tickets stay on the page.

let asking = 0;
const ASK_REFRESHING_MS = 10_000;
const ASK_READING_MS = 5_000;

/** The button, in step with whether a read is running. */
function refreshButton(running, label = 'Refreshing…') {
  const button = $('tk-refresh');
  button.disabled = running;
  button.textContent = running ? label : 'Refresh';
}

async function load({ refresh = false, answer = null } = {}) {
  clearTimeout(asking);
  $('tk-error').hidden = true;
  if (refresh) {
    refreshButton(true);
    state.read.refreshing = true;
    drawAsOf();
  }
  let data;
  try {
    data = await (answer ?? auth.boardOverview(state.project, { refresh }));
  } catch (error) {
    // 428 is the service saying the token or the project link is missing: the
    // panel that says which of the two and where to fix it, not a red line.
    if (error.status === 428) return needsSetup(error.message);
    if (error.status === 403) return denied();
    // 503 is a service older than `reading`: the first read of a big project,
    // still running there. It carries on without us; asking again is the fix.
    if (error.status === 503) {
      $('tk-asof').textContent = `${error.message} Checking again in a few seconds…`;
      asking = setTimeout(() => load(), ASK_REFRESHING_MS);
      return;
    }
    // A read that failed on the way: the held tickets, if any, stay, and the
    // button comes back so it can be tried again.
    refreshButton(false);
    state.read.refreshing = false;
    if (state.data) drawAsOf();
    else $('tk-asof').textContent = '';
    showError(`Could not read the tickets: ${error.message}`);
    return;
  }
  if (data?.reading) {
    firstRead(data);
    refreshButton(true, 'Reading…');
    asking = setTimeout(() => load(), ASK_READING_MS);
    return;
  }
  // Not redrawn when nothing changed: a page asking every ten seconds while a
  // read runs would otherwise rebuild every section, and lose the reader's
  // place in a long list, to show the same tickets.
  if (!state.data || data.asOf !== state.data.asOf || data.total !== state.data.total
      || !state.data.items) {
    state.data = data;
    state.closedByName = new Map((data.statuses ?? []).map((s) => [s.name, !!s.isClosed]));
    state.defaultStatus = new Set((data.statuses ?? []).filter((s) => s.isDefault).map((s) => s.name));
    buildSprints();
    buildTree();
    draw();
  } else {
    state.data = { ...data, items: state.data.items };
    drawLede();
  }
  state.read = {
    asOf: data.asOf,
    ageSeconds: data.ageSeconds ?? 0,
    receivedAt: performance.now(),
    refreshing: !!data.refreshing,
    error: data.refreshError ?? null,
  };
  drawAsOf();
  refreshButton(state.read.refreshing);
  if (data.refreshing) asking = setTimeout(() => load(), ASK_REFRESHING_MS);
}

// ── when the tickets were read ──────────────────────────────────────
//
// Always on the page, beside Refresh, because a dashboard that does not say how
// old it is invites people to act on a number from this morning. The clock
// time comes from `asOf`, the moment the service finished reading OpenProject;
// the "minutes ago" from `ageSeconds` plus the time since this page was told
// it, so a reader's own clock being wrong cannot make the read look newer or
// older than it is. It ticks once a minute without asking the service again.

/** "02:51", or "12 Oct, 23:51" when the read was not today. Local time. */
function clockOf(iso) {
  const d = asDate(iso);
  if (!d) return '—';
  const time = d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
  return +today() === +new Date(d.getFullYear(), d.getMonth(), d.getDate())
    ? time
    : `${d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}, ${time}`;
}

/** "3 minutes ago", for a read `seconds` old. */
const ago = (seconds) => (seconds < 60 ? 'under a minute ago'
  : seconds < 5400 ? `${plural(Math.round(seconds / 60), 'minute', 'minutes')} ago`
    : `${plural(Math.round(seconds / 3600), 'hour', 'hours')} ago`);

function drawAsOf() {
  const read = state.read;
  if (!read.asOf) return;
  const age = read.ageSeconds + (performance.now() - read.receivedAt) / 1000;
  const at = clockOf(read.asOf);
  const line = $('tk-asof');
  line.classList.toggle('is-failed', !read.refreshing && !!read.error);
  line.title = read.error ?? '';
  line.textContent = read.refreshing ? `Refreshing… (last read ${at})`
    : read.error ? `Could not refresh from OpenProject. Last good read at ${at}, ${ago(age)}.`
      : `Read from OpenProject at ${at}, ${ago(age)}`;
}

/**
 * The page before its first read has ever finished: the frame, and one line
 * saying what is happening and roughly how long it takes. Roughly, because the
 * service estimates from the pages it has read so far and OpenProject's speed
 * is OpenProject's. The sections stay as they are drawn empty in the HTML.
 */
function firstRead(progress) {
  const size = progress.total ? `${progress.total.toLocaleString()} tickets` : 'every ticket';
  const eta = progress.etaSeconds;
  const wait = eta == null ? '' : eta <= 15 ? ', a few seconds'
    : eta <= 45 ? ', about half a minute' : eta <= 90 ? ', about a minute'
      : `, about ${Math.round(eta / 60)} minutes`;
  $('tk-lede').textContent = `Reading ${size} from OpenProject for the first time${wait}.`;
  $('tk-asof').textContent = progress.total
    ? `${(progress.read ?? 0).toLocaleString()} of ${progress.total.toLocaleString()} read so far.`
    : 'Starting the read.';
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
  drawPerson(focus);
  drawQueue();
  drawPlan(focus);
  drawAttention(items);
  drawPeopleTable(focus);
  drawDaily();
  drawFinishedDaily();
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
    `${nu(state.unit === 'tasks' ? counted().length : (d.total ?? 0))} in `,
    op.url ? link(op.url, null, op.name || op.identifier) : el('span', null, op.name || op.identifier || 'OpenProject'),
    d.truncated ? ' — the newest of a larger project; older tickets are not counted.' : '.',
  );
  // The line beside Refresh is `drawAsOf`'s, drawn by `load` once it knows
  // whether a newer read is coming.
}

function drawScope() {
  const all = counted();
  const tally = (key) => {
    const m = new Map();
    for (const t of all) m.set(key(t), (m.get(key(t)) ?? 0) + 1);
    return m;
  };
  const people = [...tally(who).entries()].sort((a, b) =>
    (a[0] === 'Unassigned') - (b[0] === 'Unassigned') || a[0].localeCompare(b[0]));
  fillSelect($('tk-scope-person'), 'Everyone', people.map(([n, c]) => [n, `${n} (${nu(c)})`]), state.scope.person);

  const now = currentSprint()?.name;
  const sprints = [...tally((t) => t.version || '(no sprint)').keys()].sort(bySprint);
  fillSelect($('tk-scope-sprint'), 'Every sprint', sprints.map((n) => [n, n === now ? `${n} (now)` : n]),
    state.scope.sprint);

  const types = [...tally((t) => t.type || '').entries()].filter(([n]) => n).sort((a, b) => b[1] - a[1]);
  fillSelect($('tk-scope-type'), 'Every type', types.map(([n, c]) => [n, `${n} (${nu(c)})`]), state.scope.type);
  // In tasks every row is a Task, so the type filter has nothing to choose.
  $('tk-scope-type').closest('.tk-field').hidden = state.unit === 'tasks';
  for (const b of document.querySelectorAll('[data-unit]')) {
    b.setAttribute('aria-pressed', b.dataset.unit === state.unit ? 'true' : 'false');
  }

  const on = Object.values(state.scope).some(Boolean) && !(state.unit === 'tasks'
    && !state.scope.person && !state.scope.sprint);
  $('tk-scope-clear').hidden = !on;
  const parts = [];
  if (state.scope.person) parts.push(state.scope.person);
  if (state.scope.sprint) parts.push(state.scope.sprint);
  if (state.scope.type && state.unit === 'tickets') parts.push(`${state.scope.type} only`);
  $('tk-scope-says').textContent = on
    ? `Every section shows ${parts.join(', ')}: ${nu(scoped().length)}.`
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
    seg.dataset.tip = `${label ? `${label}: ` : ''}${kind.label} ${num(n)} of ${nu(c.live)} (${share(n, c.live)})`;
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
  return `${label ? `${label}: ` : ''}${nu(c.total)}${parts.length ? `, ${parts.join(', ')}` : ''}.`;
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
    title.textContent = `${num(c.finished)} of ${nu(c.live)} finished.`;
    pace.textContent = `These ${Ws()} are in no dated sprint, so there is no pace to hold them against.`;
    ledger.replaceChildren();
    saying.textContent = '';
    return;
  }

  const items = inFocus(focus);
  const { c, k, expected, behind, tone } = paceFor(focus, items);
  const range = `${fmtWeekday(focus.start)} to ${fmtWeekday(focus.end)}`;

  when.replaceChildren(el('strong', null, focus.name), ` ${range}`,
    k.phase === 'running' && k.dayNo ? el('span', 'tk-day', `day ${k.dayNo} of ${k.n}`) : '');


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
    el('span', 'tk-headline-figures', `${num(c.finished)} of ${nu(c.live)} finished`),
  );

  if (k.phase === 'ahead') {
    pace.textContent = `Starts ${fmtWeekday(focus.start)}, ${plural(k.n, 'working day', 'working days')} long.`;
  } else if (k.phase === 'over') {
    pace.textContent = c.finished >= c.live
      ? 'Ended with everything in it finished.'
      : `Ended ${fmtWeekday(focus.end)} with ${nu(c.open)} still open: those are late now.`;
  } else {
    const gone = k.dayNo
      ? `by the end of today, day ${k.dayNo} of ${k.n}`
      : `after ${k.through} of ${k.n} working days`;
    const parts = [`An even pace would have ${nu(expected)} finished ${gone}`
      + (behind ? `, so it is ${nu(behind)} short.` : '.')];
    parts.push(k.left ? `${plural(k.left, 'working day', 'working days')} left after today.` : 'Today is its last working day.');
    if (c.finished && k.through) {
      const projected = Math.min(c.live, Math.round((c.finished / k.through) * k.n));
      parts.push(`At this rate about ${nu(projected)} will be finished when it ends on ${fmtWeekday(focus.end)}.`);
    }
    pace.textContent = parts.join(' ');
  }

  // The composition, as words and figures rather than tiles: a figure only
  // where it is not zero, because a row of zeros is a row nobody reads.
  const rows = [
    [`Planned ${Ws()}`, c.live, ''],
    ['Closed', c.done, 'done'],
    ['Waiting for QA', c.qa, 'qa'],
    ['In progress', c.going, 'going'],
    ['On hold', c.stalled, 'stalled'],
    ['Not started', c.fresh, 'fresh'],
  ].filter(([label, n]) => n || label.startsWith('Planned'));
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
  if (!c.done && c.qa) said.push(`No ${W1()} has been closed yet: ${nu(c.qa)} ${c.qa === 1 ? 'is' : 'are'} waiting for QA.`);
  else if (!c.finished && k.phase !== 'ahead') said.push('Nothing in it is finished yet.');
  if (!c.going && c.fresh && k.phase === 'running') {
    said.push('Nothing is marked In progress, so the board cannot tell work under way from work not begun.');
  }
  if (c.rejected) said.push(`${plural(c.rejected, `${W1()} was`, `${Ws()} were`)} rejected and ${c.rejected === 1 ? 'is' : 'are'} not counted.`);
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
    c.live ? `${nu(c.live)} planned` : 'nothing planned yet',
    c.finished ? `, ${nu(c.finished)} already finished.` : '.');
}

/**
 * The burn-up: finished so far against an even line through the sprint's
 * working days. One measure on one axis; the even line is dashed because it
 * is a yardstick and not data. The gap at today is drawn and labelled, since
 * it is the one number the chart exists to show.
 */
function drawBurn(focus, items, c, k, where = { figure: 'tk-burn', box: 'tk-burn-plot', caption: 'tk-burn-caption' }) {
  const figure = $(where.figure);
  const box = $(where.box);
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
    'aria-label': `Burn-up for ${focus.name}: ${num(c.finished)} of ${nu(c.live)} finished; an even pace would have ${nu(Math.round(c.live * k.frac))}.` });

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
  pic.append(svg('text', { x: x(k.n) + 6, y: y(c.live) + 18, class: 'tk-burn-tick' }, nu(c.live)));

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
    // Halfway up the gap, right of it; a gap too short to hold the label
    // beside the "finished" one puts it on the left of the line instead.
    const roomy = endY - ey > 34;
    pic.append(svg('text', roomy
      ? { x: endX + 8, y: Math.min((ey + endY) / 2 + 4, endY - 26), class: 'tk-burn-label' }
      : { x: endX - 8, y: (ey + endY) / 2 + 4, class: 'tk-burn-label', 'text-anchor': 'end' },
    `${nu(expected - cum.at(-1))} short`));
  }
  pic.append(svg('circle', { cx: endX, cy: endY, r: 4.5, class: 'tk-burn-dot' }));
  pic.append(svg('text', { x: endX + 8, y: endY - 6, class: 'tk-burn-label is-strong' }, `${nu(cum.at(-1))} finished`));

  // Hover and focus: one target per day, wider than the mark.
  const tips = svg('g', { class: 'tk-burn-hits' });
  k.days.forEach((d, i) => {
    const done = i < cum.length - 1 ? cum[i + 1] : null;
    const even = Math.round((c.live * (i + 1)) / k.n);
    const hit = svg('rect', { x: x(i), y: m.t, width: x(i + 1) - x(i), height: ih, class: 'tk-burn-hit' });
    hit.dataset.tip = `${fmtWeekday(d)}, day ${i + 1} of ${k.n}: `
      + (done == null ? `not reached yet; an even pace is ${nu(even)} by its end.`
        : `${nu(done)} finished by its end; an even pace is ${nu(even)}.`);
    tips.append(hit);
  });
  pic.append(tips);

  // The table twin, for anything not looking at the picture.
  const table = el('table', 'tk-sr');
  table.append(el('caption', null, `${focus.name}: ${Ws()} finished by the end of each working day`));
  const head = el('tr');
  head.append(el('th', null, 'Day'), el('th', null, `${WsCap()} finished`), el('th', null, `Even pace, ${Ws()}`));
  table.append(head);
  k.days.forEach((d, i) => {
    if (i + 1 >= cum.length) return;
    const row = el('tr');
    row.append(el('td', null, fmtWeekday(d)), el('td', null, num(cum[i + 1])), el('td', null, num(Math.round((c.live * (i + 1)) / k.n))));
    table.append(row);
  });

  box.replaceChildren(pic, table);
  $(where.caption).textContent = `${WsCap()} finished so far, against an even pace`
    + (Object.keys(state.data.closes ?? {}).length ? '' : ` (a ${W1()} counts on the day it last changed)`);
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
  const everything = counted().filter(typeOk);
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
  $('tk-roster-head-bar').textContent = `${focus ? focus.name : 'This sprint'}, ${Ws()}`;
  const running = k?.phase === 'running';
  $('tk-team-note').textContent = focus
    ? `Each bar is one person's ${Ws()} in ${focus.name}, on one scale. `
      + (running ? 'The upright mark is where an even pace would have their finished part by the end of today. ' : '')
      + 'Open in the plan is everything still theirs across every sprint, as a number, so a big backlog does not drown the sprint. '
      + 'Select a person to open everything about them.'
    : 'No dated sprint to measure against. Select a person to open everything about them.';

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
    if (r.c.live) done.append(el('strong', null, num(r.c.finished)), el('span', null, ` of ${nu(r.c.live)}`));

    const pace = el('span', 'tk-person-pace');
    if (!r.c.live) pace.append(el('span', 'tk-quiet', ''));
    else if (!running) pace.append(el('span', 'tk-quiet', k?.phase === 'ahead' ? `starts ${fmtShort(focus.start)}` : `${nu(r.c.open)} left open`));
    else if (r.behind > 0) {
      pace.classList.add('is-behind');
      pace.append(el('span', 'tk-pace-glyph', '↓'), `${nu(r.behind)} behind`);
    } else pace.append(el('span', 'tk-pace-glyph is-ok', '✓'), r.behind < 0 ? `${nu(-r.behind)} ahead` : 'on pace');

    const open = el('span', 'tk-person-open');
    open.append(el('strong', null, num(r.open)), el('span', null, ` open ${Ws()}`));

    row.append(ident, bar, done, pace, open);
    row.setAttribute('aria-label', `${r.name}. ${focus ? `${focus.name}: ${num(r.c.finished)} of ${num(r.c.live)} finished` : ''}`
      + `${running && r.c.live ? (r.behind > 0 ? `, ${num(r.behind)} behind an even pace` : ', on pace') : ''}`
      + `. ${num(r.open)} open in the whole plan. Opens everything about ${r.name}.`);
    row.onclick = () => openPerson(r.name);
    return row;
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', `Nobody has a ${W1()} in this view.`));

  const key = legendItems($('tk-roster-key'), KINDS.filter((kind) => rows.some((r) => r.c[kind.id])));
  if (running) {
    const item = el('li', 'tk-legend-item');
    item.append(el('span', 'tk-key-tick'), el('span', 'tk-legend-label', 'Even pace by today'));
    key.append(item);
  }
}

// ── waiting for QA ──────────────────────────────────────────────────

const QA_SHOWN = 8;

/** One ticket waiting for QA: who finished it and how long it has waited. */
function qaRow(t, { right = null } = {}) {
  const row = el('div', 'tk-qa-row');
  const w = waited(t);
  const main = el('span', 'tk-main');
  main.append(el('span', 'tk-subject', t.subject || '(no subject)'));
  if (t.parentSubject) main.append(el('span', 'tk-parent', t.parentSubject));
  row.append(link(t.url, 'tk-key', `#${t.key}`), main, el('span', 'tk-who', right ?? who(t)),
    el('span', `tk-waited${w.n >= 3 ? ' is-long' : ''}`, w.text), el('span', 'tk-qa-sprint', t.version || 'no sprint'));
  row.title = `${t.subject}\n${who(t)}, ${t.status} since ${fmtWhen(t.updatedAt)}`;
  return row;
}

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
  $('tk-qa-title').textContent = list.length ? `Waiting for QA: ${nu(list.length)}` : 'Waiting for QA';
  if (!list.length) {
    note.textContent = '';
    box.replaceChildren(el('p', 'tk-empty', `No ${W1()} is waiting for QA in this view.`));
    return;
  }
  const byWho = new Map();
  for (const t of list) byWho.set(who(t), (byWho.get(who(t)) ?? 0) + 1);
  const most = [...byWho.entries()].sort((a, b) => b[1] - a[1])[0];
  const oldest = waited(list[0]);
  note.textContent = `Finished by the developer, waiting for somebody to test and close. Oldest first; `
    + `the oldest has waited ${oldest.text === 'today' ? 'since today' : oldest.text}. `
    + (most[1] > 1 && list.length > 2 ? `${most[0]} finished ${nu(most[1])} of them. ` : '')
    + `Waiting is counted from the ${W1()}’s last change, the nearest OpenProject 10 gives to when it got here.`;

  const shown = state.qaAll ? list : list.slice(0, QA_SHOWN);
  const table = el('div', 'tk-qa-list');
  for (const t of shown) table.append(qaRow(t));
  box.replaceChildren(table);
  if (list.length > QA_SHOWN) {
    const more = el('button', 'chip tk-more', state.qaAll ? 'Show the oldest eight' : `Show all ${nu(list.length)}`);
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
      el('span', 'tk-band-words', c.live ? `${num(c.finished)} of ${nu(c.live)} finished` : `no ${Ws()} in this view`));
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
      band.dataset.tip = `${b.subject}: ${num(c.finished)} of ${nu(c.live)} finished (${share(c.finished, c.live)})`
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
      bar.dataset.tip = `${name.code ? `Block ${name.code}` : b.subject} in ${s.name}: ${nu(n)}`
        + (out ? ', outside the block’s planned window' : '');
      track.append(bar);
    }
    const unsprinted = tickets.filter((t) => !t.version).length;
    row.append(label, track);
    row.setAttribute('aria-label', `${b.subject}: ${num(c.finished)} of ${nu(c.live)} finished`
      + `${from && to ? `, planned ${from.name} to ${to.name}` : ''}`
      + `${outside ? `, ${nu(outside)} in sprints outside that window` : ''}`
      + `${unsprinted ? `, ${nu(unsprinted)} in no sprint` : ''}.`);
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
    + `the solid start of it is how much is finished. The columns inside a band are how many of its ${Ws()} `
    + 'each sprint holds, and a column standing outside its band is work planned outside the block’s window. '
    + (loose ? `${plural(loose, `${W1()} has`, `${Ws()} have`)} no sprint${looseFeatures ? ` (${num(looseFeatures)} of them features, finished when their tickets are)` : ''}.` : '')
    + ` Counted in ${Ws()}.`;
}

// ── what needs somebody ─────────────────────────────────────────────

/** A held ticket, with what was last said on it as the reason. */
function heldItem(t) {
  const item = el('div', 'tk-att-item');
  const head = el('div', 'tk-att-head');
  head.append(link(t.url, 'tk-key', `#${t.key}`), el('span', 'tk-att-subject', t.subject || '(no subject)'));
  item.append(head, el('p', 'tk-att-meta',
    `${t.assignee ? t.assignee : 'Nobody’s'}, ${t.version || 'no sprint'}, ${t.status}`));
  const why = t.lastComment;
  if (why?.text) {
    // OpenProject comments are Markdown; the emphasis marks are noise here.
    const text = why.text.replace(/\*\*|__|`/g, '').trim();
    item.append(el('blockquote', 'tk-att-why', text.length > 220 ? `${text.slice(0, 220)}…` : text),
      el('p', 'tk-att-meta', `${why.author || 'Somebody'}, ${fmtDay(why.at)}`));
  } else {
    item.append(el('p', 'tk-att-meta is-quiet', 'No comment on it says why.'));
  }
  return item;
}

function drawAttention(items) {
  // On hold, with what was last said on it.
  const held = items.filter(isStalled).sort((a, b) => Number(a.key) - Number(b.key));
  $('tk-held-title').textContent = held.length ? `On hold: ${nu(held.length)}` : 'On hold';
  const heldBox = $('tk-held');
  heldBox.replaceChildren(...held.slice(0, 6).map(heldItem));
  if (held.length > 6) heldBox.append(link('#states', 'tk-att-more', `${nu(held.length - 6)} more on hold`));
  if (!held.length) heldBox.append(el('p', 'tk-empty', `No ${W1()} is on hold.`));

  // Late and due: sentences, with the list a click away.
  const late = items.filter(isLate);
  const soon = items.filter(isDueSoon);
  const ownDates = items.filter((t) => t.dueDate).length;
  const due = $('tk-due');
  const lines = [];
  if (!ownDates) lines.push(el('p', 'tk-att-text', `No ${W1()} carries a due date of its own, so each is due when its sprint ends.`));
  lines.push(el('p', 'tk-att-text', late.length
    ? `${plural(late.length, `open ${W1()} is`, `open ${Ws()} are`)} late: past ${ownDates ? 'a due date or ' : ''}the end of ${late.length === 1 ? 'its' : 'their'} sprint.`
    : 'Nothing open is late.'));
  if (soon.length) {
    const ends = [...new Set(soon.map((t) => +dueOn(t)))].sort((a, b) => a - b);
    const when = ends.length === 1 ? `by ${fmtWeekday(new Date(ends[0]))}` : 'in the next seven days';
    const sprintEnd = ends.length === 1 && soon.every((t) => !t.dueDate && t.version)
      ? `, when ${soon[0].version} ends` : '';
    lines.push(el('p', 'tk-att-text', `${plural(soon.length, `open ${W1()} is`, `open ${Ws()} are`)} due ${when}${sprintEnd}.`));
  } else {
    lines.push(el('p', 'tk-att-text', 'Nothing open is due in the next seven days.'));
  }
  if (late.length || soon.length) lines.push(link('#dates', 'tk-att-more', `See the ${Ws()}`));
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

// ── one person ──────────────────────────────────────────────────────
//
// Everything about one developer, from the same payload as the rest of the
// page: no read per person. It is the page's `person` filter given a page of
// its own, so `?person=<name>#person` is a link somebody can send, every other
// panel (All tickets, Late and due) is already narrowed to them when the rail
// is used, and "Back to the team" is clearing that filter.
//
// The person is named by their OpenProject name, because that is all the
// overview carries for an assignee: OpenProject 10's list gives the user's
// title on the link, and the page is not given user ids.

/** Who the delivery package says somebody is: their role, and whether the plan
 *  keeps them off module tests. Optional: a package without docs/active/team.json
 *  (or a reader who cannot fetch it) just shows no role. */
async function loadTeam() {
  try {
    const answer = await fetch(auth.apiUrl('/api/file?path=docs/active/team.json'), { credentials: 'include' });
    if (!answer.ok) return;
    const doc = await answer.json();
    state.team = {
      roles: (doc.people ?? []).map((p) => ({ name: p.name, role: p.role, pools: p.pools ?? [] })),
      neverTests: doc.neverTests ?? [],
    };
    if (state.data) drawPerson(focusSprint());
  } catch { /* no role is a fine answer */ }
}

/** The package's entry for an OpenProject name: the same name, or the only one
 *  whose first name matches ("Surendra" in the plan is "Surendra Loke" here). */
function teamEntry(name, list) {
  const exact = list.find((p) => norm(p.name ?? p) === norm(name));
  if (exact) return exact;
  const first = norm(name).split(' ')[0];
  const close = list.filter((p) => norm(p.name ?? p).split(' ')[0] === first);
  return close.length === 1 ? close[0] : null;
}

/** Change requests, read once when somebody opens a person and kept. One GET
 *  of ADAM's own table; nothing is asked of OpenProject. */
async function loadChanges() {
  if (state.changes) return;
  state.changes = { pending: true };
  try {
    const answer = await auth.listChanges(state.project);
    state.changes = { items: answer.items ?? [] };
  } catch (error) {
    state.changes = { error: error.message || 'could not be read' };
  }
  if (state.scope.person) drawPersonChanges(state.scope.person, mineOf(state.scope.person));
}

function openPerson(name) {
  setScope({ person: name });
  if (location.hash !== '#person') location.hash = '#person';
}

function backToTeam() {
  setScope({ person: '' });
  location.hash = '#overview';
}

/** Every ticket a person holds, under the type filter but not the sprint one:
 *  this page is about the person across the whole plan. */
const mineOf = (name) => counted().filter((t) => who(t) === name && typeOk(t));

/** The bracketed tag a subject starts with: [BE], [FE], [DB], [Test]… */
const tagOf = (t) => /^\[([^\]]{1,20})\]/.exec(t.subject || '')?.[1] ?? '';
const isModuleTest = (t) => /^\[test\]\s*module test/i.test(t.subject || '');
const ordinal = (n) => {
  const s = ['th', 'st', 'nd', 'rd'];
  const v = n % 100;
  return `${n}${s[(v - 20) % 10] || s[v] || s[0]}`;
};

/** How a set of sprint tickets stands against an even pace: the one place the
 *  sprint section and the person page both take their verdict from. */
function paceFor(focus, items) {
  const c = count(items);
  const k = clock(focus);
  const expected = Math.round(c.live * k.frac);
  let tone = 'ok';
  if (k.phase === 'ahead') tone = 'idle';
  else if (k.phase === 'over') tone = c.finished >= c.live ? 'ok' : 'over';
  else if (expected > 0) {
    const ratio = c.finished / expected;
    tone = ratio >= 0.9 ? 'ok' : ratio >= 0.6 ? 'warn' : 'bad';
  }
  return { c, k, expected, behind: Math.max(0, expected - c.finished), tone };
}

function drawPerson(focus) {
  const name = state.scope.person;
  const nav = $('tk-nav-person');
  nav.textContent = name || 'One person';
  $('tk-p-pick').hidden = !!name;
  $('tk-p-body').hidden = !name;
  if (!name) { drawPersonPicker(focus); return; }

  const mine = mineOf(name);
  const initialsBadge = $('tk-p-avatar');
  initialsBadge.textContent = initials(name);
  $('tk-p-name').textContent = name;
  const entry = state.team ? teamEntry(name, state.team.roles) : null;
  const stacks = (() => {
    const tags = new Map();
    for (const t of mine) { const g = tagOf(t); if (g) tags.set(g, (tags.get(g) ?? 0) + 1); }
    const top = [...tags.entries()].sort((a, b) => b[1] - a[1]);
    const total = top.reduce((n, [, v]) => n + v, 0);
    return top.filter(([, v]) => v / Math.max(1, total) >= 0.2).slice(0, 2).map(([g]) => g);
  })();
  $('tk-p-role').textContent = [entry?.role, stacks.length ? `mostly ${stacks.join(' and ')} tickets` : '']
    .filter(Boolean).join(', ') || (mine.length ? '' : `No ${W1()} in OpenProject is theirs.`);

  // This sprint: the verdict, their burn-up, the composition.
  const sprintItems = focus ? mine.filter((t) => t.version === focus.name) : [];
  const verdict = $('tk-p-verdict');
  const pace = $('tk-p-pace');
  const ledger = $('tk-p-ledger');
  $('tk-p-burn').hidden = true;
  if (!focus) {
    verdict.replaceChildren('No dated sprint to measure against.');
    pace.textContent = '';
    ledger.replaceChildren();
  } else if (!sprintItems.length) {
    verdict.replaceChildren(verdictPill('idle', 'Nothing this sprint'), el('span', 'tk-p-verdict-text', `${focus.name}: nothing of theirs is planned in it.`));
    pace.textContent = '';
    ledger.replaceChildren();
  } else {
    const p = paceFor(focus, sprintItems);
    const label = p.k.phase === 'over' && p.c.finished < p.c.live ? 'Ended unfinished' : undefined;
    const words = `${focus.name}: ${num(p.c.finished)} of ${nu(p.c.live)} finished`
      + (p.k.phase === 'running' ? (p.behind ? `, ${nu(p.behind)} behind an even pace` : ', on an even pace')
        : p.k.phase === 'ahead' ? `, starts ${fmtWeekday(focus.start)}` : '');
    verdict.replaceChildren(verdictPill(p.tone, label), el('span', 'tk-p-verdict-text', words));
    if (p.k.phase === 'running') {
      const gone = p.k.dayNo ? `by the end of today, day ${p.k.dayNo} of ${p.k.n}` : `after ${p.k.through} of ${p.k.n} working days`;
      const bits = [`An even pace would have ${nu(p.expected)} of theirs finished ${gone}.`];
      if (p.c.finished && p.k.through) {
        bits.push(`At their rate about ${nu(Math.min(p.c.live, Math.round((p.c.finished / p.k.through) * p.k.n)))} will be finished by ${fmtWeekday(focus.end)}.`);
      } else if (!p.c.finished) bits.push(`No ${W1()} of theirs in it is finished yet.`);
      pace.textContent = bits.join(' ');
    } else pace.textContent = '';
    ledger.replaceChildren(...[
      [`Planned ${Ws()}`, p.c.live, ''], ['Closed', p.c.done, 'done'], ['Waiting for QA', p.c.qa, 'qa'],
      ['In progress', p.c.going, 'going'], ['On hold', p.c.stalled, 'stalled'], ['Not started', p.c.fresh, 'fresh'],
    ].filter(([label, n]) => n || label.startsWith('Planned')).map(([label, n, kind]) => {
      const wrap = el('div', 'tk-ledger-item');
      const dt = el('dt');
      if (kind) dt.append(el('span', `tk-key-swatch tk-seg-${kind}`));
      dt.append(label);
      wrap.append(dt, el('dd', null, num(n)));
      return wrap;
    }));
    if (p.k.phase !== 'ahead') {
      drawBurn(focus, sprintItems, p.c, p.k, { figure: 'tk-p-burn', box: 'tk-p-burn-plot', caption: 'tk-p-burn-caption' });
    }
  }
  drawPersonRank(name, focus);
  drawPersonFeatures(name, focus, sprintItems);
  drawPersonPlan(name, focus, mine);
  drawPersonQueue(mine);
  drawPersonFinished(mine);
  drawPersonHeld(mine);
  drawPersonGate(name);
  drawPersonTests(name, mine);
  drawPersonChanges(name, mine);
  $('tk-p-all').textContent = `Search, filter and download all ${nu(mine.length)} of ${name.split(' ')[0]}'s`;
  $('tk-p-all-note').textContent = 'Opens the full list, already narrowed to them, with the search, the state filter and the CSV.';
}

/** With nobody chosen, the page is a list of everybody to choose from. */
function drawPersonPicker(focus) {
  const rows = sortPeople(people(focus)).filter((r) => r.all.length);
  $('tk-p-pick-list').replaceChildren(...rows.map((r) => {
    const b = el('button', 'tk-p-pick-item');
    b.type = 'button';
    b.append(el('span', 'tk-avatar', initials(r.name)), el('span', 'tk-person-name', r.name),
      el('span', 'tk-quiet', `${focus ? `${nu(r.c.live)} in ${focus.name}, ` : ''}${num(r.open)} open`));
    b.onclick = () => openPerson(r.name);
    return b;
  }));
}

/** Where they sit among the team: three ranks in words, no chart. */
function drawPersonRank(name, focus) {
  const rows = people(focus).filter((r) => r.name !== 'Unassigned');
  const box = $('tk-p-rank');
  const me = rows.find((r) => r.name === name);
  if (!me) { box.replaceChildren(); return; }
  const rankBy = (get) => 1 + rows.filter((r) => get(r) > get(me)).length;
  const most = (get) => {
    const n = rankBy(get);
    if (n === 1) return `the most of ${rows.length}`;
    // Last, and not tied with everybody: "11th most of 11" says it the long way.
    if (n === rows.length) return `the least of ${rows.length}`;
    return `${ordinal(n)} most of ${rows.length}`;
  };
  const sprintTotal = rows.reduce((n, r) => n + r.c.live, 0) + (people(focus).find((r) => r.name === 'Unassigned')?.c.live ?? 0);
  const openTotal = people(focus).reduce((n, r) => n + r.open, 0);
  const k = focus ? clock(focus) : null;
  const items = [];
  if (focus && me.c.live) {
    items.push([`Share of ${focus.name}`, `${share(me.c.live, sprintTotal)}`,
      `${num(me.c.live)} of ${nu(sprintTotal)}, ${most((r) => r.c.live)}`]);
  }
  if (k?.phase === 'running' && me.c.live) {
    items.push(['Behind pace', me.behind > 0 ? nu(me.behind) : 'none',
      me.behind > 0 ? (rankBy((r) => r.behind) === 1 ? `the furthest behind of ${rows.length}`
        : `${ordinal(rankBy((r) => r.behind))} furthest behind of ${rows.length}`) : 'on or ahead of an even pace']);
  }
  items.push(['Open in the plan', nu(me.open),
    `${share(me.open, openTotal)} of the team's ${num(openTotal)}, ${most((r) => r.open)}`]);
  if (me.finishedAll) {
    items.push(['Finished so far', nu(me.finishedAll), most((r) => r.finishedAll)]);
  }
  box.replaceChildren(...items.map(([label, value, words]) => {
    const wrap = el('div', 'tk-p-rank-item');
    wrap.append(el('dt', null, label), el('dd', null, value), el('dd', 'tk-p-rank-words', words));
    return wrap;
  }));
}

/** Their open sprint work as work: grouped by the feature it belongs to. */
const FEATURES_SHOWN = 12;
function drawPersonFeatures(name, focus, sprintItems) {
  const box = $('tk-p-features');
  $('tk-p-features-title').textContent = focus ? `Open in ${focus.name}, by feature` : 'Open this sprint, by feature';
  const open = sprintItems.filter((t) => !isFinished(t) && !isRejected(t));
  if (!focus || !open.length) {
    box.replaceChildren(el('p', 'tk-empty', !focus ? 'No dated sprint.'
      : sprintItems.length ? `Every ${W1()} of theirs in ${focus.name} is finished.` : `No ${W1()} of theirs is in ${focus.name}.`));
    $('tk-p-features-note').textContent = '';
    return;
  }
  const groups = new Map();
  for (const t of sprintItems) {
    const feature = tree.second.get(t.key);
    const key = feature && feature !== t ? feature.key : '';
    const g = groups.get(key) ?? { feature: key ? feature : null, open: [], finished: 0 };
    if (isFinished(t)) g.finished += 1; else if (!isRejected(t)) g.open.push(t);
    groups.set(key, g);
  }
  const list = [...groups.values()].filter((g) => g.open.length)
    .sort((a, b) => b.open.length - a.open.length || String(a.feature?.subject).localeCompare(String(b.feature?.subject)));
  $('tk-p-features-note').textContent = `${plural(open.length, `open ${W1()}`, `open ${Ws()}`)} under `
    + `${plural(list.length, 'feature', 'features')}, the biggest first. Open one to see its ${Ws()}.`;
  const render = (all) => {
    box.replaceChildren(...(all ? list : list.slice(0, FEATURES_SHOWN)).map((g) => {
      const d = el('details', 'tk-p-feature');
      const sum = el('summary');
      const top = g.feature ? tree.top.get(g.feature.key) : null;
      const code = top ? blockName(top.subject).code : '';
      sum.append(el('span', 'tk-p-feature-name', g.feature?.subject || 'Not under a feature'),
        code ? el('span', 'tk-p-chip', code) : '',
        el('span', 'tk-p-feature-n', `${nu(g.open.length)} open${g.finished ? `, ${num(g.finished)} finished` : ''}`));
      d.append(sum);
      // A sub-task is read under its task: "V0026__orders.sql, 39 sub-tasks
      // open" is one piece of work, where 39 table rows are a list.
      const nodes = new Map();
      for (const t of g.open) {
        const underTask = t.parent && g.feature && String(t.parent) !== String(g.feature.key) && tree.byKey.has(String(t.parent));
        const head = underTask ? tree.byKey.get(String(t.parent)) : t;
        const node = nodes.get(head.key) ?? { task: head, self: false, subs: [] };
        if (underTask) node.subs.push(t); else node.self = true;
        nodes.set(head.key, node);
      }
      const rows = el('div', 'tk-p-feature-rows');
      const ordered = [...nodes.values()].sort((a, b) => Number(a.task.key) - Number(b.task.key));
      for (const n of ordered.slice(0, 60)) {
        const row = el('div', 'tk-p-ticket');
        const right = n.subs.length
          ? el('span', 'tk-p-when', `${plural(n.subs.length, 'sub-task', 'sub-tasks')} open${n.self ? ', and the task' : ''}`)
          : stateBadge(n.task);
        row.append(link(n.task.url, 'tk-key', `#${n.task.key}`), el('span', 'tk-subject', n.task.subject || '(no subject)'), right);
        if (n.subs.length) row.title = n.subs.map((x) => `#${x.key} ${x.subject}`).slice(0, 30).join('\n');
        rows.append(row);
      }
      if (ordered.length > 60) rows.append(el('p', 'tk-quiet', `and ${num(ordered.length - 60)} more, in the full list`));
      d.append(rows);
      return d;
    }));
    // The biggest feature opens by itself when it is short enough to read.
    const first = box.querySelector('details');
    if (first && first.querySelectorAll('.tk-p-ticket').length <= 12) first.open = true;
    if (list.length > FEATURES_SHOWN) {
      const more = el('button', 'chip tk-more', all ? `Show the biggest ${FEATURES_SHOWN}` : `Show all ${num(list.length)} features`);
      more.type = 'button';
      more.setAttribute('aria-expanded', all ? 'true' : 'false');
      more.onclick = () => render(!all);
      box.append(more);
    }
  };
  render(false);
}

/** Everything they hold, cut three ways: by sprint, by block, by type and tag. */
function drawPersonPlan(name, focus, mine) {
  const open = mine.filter(isOpenWork);
  $('tk-p-plan-note').textContent = `${nu(open.length)} still theirs to do across the plan`
    + `${mine.length - open.length ? `, beside ${nu(mine.length - open.length)} finished or rejected` : ''}.`;

  // Per sprint: one cell per sprint, the count printed, a column for its size.
  const sprints = datedSprints().filter((s) => s.number != null);
  const bySprint = new Map();
  for (const t of open) bySprint.set(t.version || '', (bySprint.get(t.version || '') ?? 0) + 1);
  const most = Math.max(1, ...bySprint.values());
  const strip = $('tk-p-sprints');
  const cells = sprints.map((s) => [s.name, String(s.number), bySprint.get(s.name) ?? 0, focus && s.name === focus.name]);
  const loose = bySprint.get('') ?? 0;
  if (loose) cells.push(['', 'none', loose, false]);
  strip.style.setProperty('--n', String(cells.length));
  strip.replaceChildren(...cells.map(([sprint, label, n, now]) => {
    const cell = el('div', `tk-p-cell${now ? ' is-focus' : ''}${n ? '' : ' is-empty'}`);
    const bar = el('span', 'tk-p-cell-bar');
    bar.style.setProperty('--h', String(n / most));
    cell.append(el('span', 'tk-p-cell-n', n ? num(n) : '–'), bar, el('span', 'tk-p-cell-label', label));
    cell.dataset.tip = `${sprint || 'No sprint'}: ${plural(n, `open ${W1()}`, `open ${Ws()}`)}`;
    return cell;
  }));
  strip.setAttribute('aria-label', `Open ${Ws()} per sprint: ${cells.filter(([, , n]) => n)
    .map(([s, , n]) => `${s || 'no sprint'} ${n}`).join(', ') || 'none'}.`);

  // Per block, per type, per tag: short lists with a bar on one scale each.
  const tally = (key) => {
    const m = new Map();
    for (const t of open) { const k = key(t); if (k) m.set(k, (m.get(k) ?? 0) + 1); }
    return [...m.entries()];
  };
  const blockOf = (t) => {
    const top = tree.top.get(t.key);
    if (!top || top === t) return '';
    const n = blockName(top.subject);
    return n.code ? `Block ${n.code}` : top.subject;
  };
  const blocksList = tally(blockOf).sort((a, b) => a[0].localeCompare(b[0], undefined, { numeric: true }));
  const noBlock = open.filter((t) => !blockOf(t)).length;
  if (noBlock) blocksList.push(['Not under a block', noBlock]);
  miniBars($('tk-p-blocks'), blocksList);
  miniBars($('tk-p-types'), tally((t) => t.type || 'No type').sort((a, b) => b[1] - a[1]));
  const tags = tally((t) => tagOf(t) || 'No tag').sort((a, b) => b[1] - a[1]);
  miniBars($('tk-p-tags'), tags);
}

function miniBars(box, entries) {
  const most = Math.max(1, ...entries.map(([, n]) => n));
  box.replaceChildren(...entries.map(([label, n]) => {
    const row = el('div', 'tk-p-mini');
    const bar = el('span', 'tk-p-mini-bar');
    const fill = el('span', 'tk-p-mini-fill');
    fill.style.width = `${Math.max(2, (n / most) * 100)}%`;
    bar.append(fill);
    row.append(el('span', 'tk-p-mini-label', label), bar, el('span', 'tk-p-mini-n', num(n)));
    return row;
  }));
  if (!entries.length) box.append(el('p', 'tk-empty', 'Nothing open.'));
}

function drawPersonQueue(mine) {
  const list = mine.filter(isAwaiting).sort((a, b) => (asDate(a.updatedAt) ?? 0) - (asDate(b.updatedAt) ?? 0));
  $('tk-p-qa-title').textContent = list.length ? `Waiting for QA: ${nu(list.length)}` : 'Waiting for QA';
  const box = $('tk-p-qa');
  if (!list.length) { box.replaceChildren(el('p', 'tk-empty', `No ${W1()} of theirs is waiting for QA.`)); return; }
  const table = el('div', 'tk-qa-list tk-p-list');
  for (const t of list.slice(0, 10)) table.append(qaRow(t, { right: t.status }));
  box.replaceChildren(table);
  if (list.length > 10) box.append(el('p', 'tk-quiet', `and ${nu(list.length - 10)} more, in the full list`));
}

/** What they finished most recently: "search a name, show what they closed". */
function drawPersonFinished(mine) {
  const list = mine.filter(isFinished).map((t) => [t, finishedAt(t)]).sort((a, b) => (b[1] ?? 0) - (a[1] ?? 0));
  const box = $('tk-p-done');
  $('tk-p-done-title').textContent = list.length ? `Recently finished: ${nu(list.length)}` : 'Recently finished';
  if (!list.length) { box.replaceChildren(el('p', 'tk-empty', `No ${W1()} of theirs is finished yet.`)); return; }
  const fromAdam = list.filter(([t]) => state.data.closes?.[t.key]).length;
  $('tk-p-done-note').textContent = 'Newest first. Closed and waiting for QA both count. '
    + (fromAdam === list.length ? 'Every date is when ADAM closed it.'
      : `A date is when ADAM closed the ${W1()} where it went through ADAM, otherwise its last change in OpenProject.`);
  const table = el('div', 'tk-p-list');
  for (const [t, at] of list.slice(0, 12)) {
    const row = el('div', 'tk-p-ticket tk-p-done-row');
    row.append(link(t.url, 'tk-key', `#${t.key}`), el('span', 'tk-subject', t.subject || '(no subject)'), stateBadge(t),
      el('span', 'tk-p-when', at ? fmtWhen(at.toISOString()) : '—'));
    table.append(row);
  }
  box.replaceChildren(table);
  if (list.length > 12) box.append(el('p', 'tk-quiet', `and ${nu(list.length - 12)} earlier, in the full list`));
}

function drawPersonHeld(mine) {
  const held = mine.filter(isStalled);
  $('tk-p-held-title').textContent = held.length ? `On hold: ${nu(held.length)}` : 'On hold';
  $('tk-p-held').replaceChildren(...(held.length ? held.slice(0, 8).map(heldItem)
    : [el('p', 'tk-empty', `No ${W1()} of theirs is on hold.`)]));
}

function drawPersonGate(name) {
  const g = gateFor(name);
  const box = $('tk-p-gate');
  if (!g) {
    box.replaceChildren(el('p', 'tk-att-text', `${name.split(' ')[0]} has not closed a ticket through ADAM yet, `
      + `so the ${state.data.testEvery ?? 10}-ticket gate has not started for them.`));
    return;
  }
  const s = gateState(g);
  box.replaceChildren(gateMeter(g), el('p', 'tk-att-text', `${g.closed} of ${g.every} tickets closed through ADAM since `
    + `${g.lastPassedAt ? `their last batch passed on ${fmtDay(g.lastPassedAt)}` : 'they started'}: ${s.text}.`));
}

function drawPersonTests(name, mine) {
  const tests = mine.filter(isModuleTest).sort((a, b) => bySprint(a.version || '(no sprint)', b.version || '(no sprint)'));
  const box = $('tk-p-tests');
  $('tk-p-tests-title').textContent = tests.length ? `Module tests they own: ${nu(tests.length)}` : 'Module tests they own';
  const never = state.team && teamEntry(name, state.team.neverTests);
  if (!tests.length) {
    box.replaceChildren(el('p', 'tk-att-text', never
      ? 'None, by design: the plan never gives them a module test, because a module test needs a checker who is not its builder.'
      : 'None: no ticket of theirs is a "[Test] Module test".'));
    return;
  }
  const list = el('div', 'tk-p-list');
  // The plan says who never owns one; OpenProject is where it is enforced or not.
  if (never) {
    list.append(el('p', 'tk-att-text tk-p-warn', `The plan never gives ${name.split(' ')[0]} a module test (team.json, neverTests), `
      + `yet ${tests.length === 1 ? 'this one is' : `these ${tests.length} are`} theirs in OpenProject.`));
  }
  for (const t of tests.slice(0, 8)) {
    const row = el('div', 'tk-att-item');
    const head = el('div', 'tk-att-head');
    head.append(link(t.url, 'tk-key', `#${t.key}`),
      el('span', 'tk-att-subject', (t.subject || '').replace(/^\[test\]\s*module test:\s*/i, '')));
    row.append(head, el('p', 'tk-att-meta', `${t.version || 'no sprint'}, ${t.status}`));
    list.append(row);
  }
  box.replaceChildren(list);
  if (tests.length > 8) box.append(el('p', 'tk-quiet', `and ${nu(tests.length - 8)} more`));
}

function drawPersonChanges(name, mine) {
  const box = $('tk-p-crs');
  const ch = state.changes;
  if (!ch) { loadChanges(); box.replaceChildren(el('p', 'tk-quiet', 'Reading ADAM’s change requests…')); return; }
  if (ch.pending) return;
  if (ch.error) { box.replaceChildren(el('p', 'tk-att-text', `ADAM's change requests could not be read: ${ch.error}`)); return; }
  const keys = new Set(mine.map((t) => String(t.key)));
  const list = ch.items.filter((c) => keys.has(String(c.ticket || '').replace('#', ''))
    || keys.has(String(c.childTicket || '').replace('#', '')));
  $('tk-p-crs-title').textContent = list.length ? `Change requests: ${plural(list.length, 'request', 'requests')}` : 'Change requests';
  if (!list.length) {
    box.replaceChildren(el('p', 'tk-att-text', `No ADAM change request was raised on one of ${name.split(' ')[0]}'s ${Ws()} `
      + `or filed as one${ch.items.length ? ` (${plural(ch.items.length, 'request', 'requests')} in the project)` : ''}.`));
    return;
  }
  const wrap = el('div', 'tk-p-list');
  for (const c of list) {
    const row = el('div', 'tk-p-ticket');
    const which = keys.has(String(c.childTicket || '')) ? `filed as #${c.childTicket}` : `raised on #${c.ticket}`;
    row.append(link('/changes.html', 'tk-key', c.id), el('span', 'tk-subject', c.title),
      el('span', 'tk-badge tk-badge-open', c.status), el('span', 'tk-p-when', which));
    wrap.append(row);
  }
  box.replaceChildren(wrap);
}

// ── expected per day, by sprint ─────────────────────────────────────
//
// What a sprint asks of each person's working day: their tasks (or tickets)
// in it over its working days, Monday to Friday between the sprint's dates.
// Not a target set anywhere; the plan's own unit is points, said under the
// table, which is why two people's tasks a day can differ and both be right.

function drawDaily() {
  const sprints = datedSprints().filter((s) => s.number != null);
  const pool = counted().filter(typeOk);
  const per = new Map();
  const colTotal = new Map();
  let unsprinted = 0;
  for (const t of pool) {
    const s = t.version ? sprintOf(t.version) : null;
    if (!s || s.number == null || !s.start) { if (!t.version) unsprinted += 1; continue; }
    const name = who(t);
    if (!per.has(name)) per.set(name, new Map());
    per.get(name).set(s.name, (per.get(name).get(s.name) ?? 0) + 1);
    colTotal.set(s.name, (colTotal.get(s.name) ?? 0) + 1);
  }
  const cols = sprints.filter((s) => colTotal.get(s.name));
  const empty = sprints.filter((s) => !colTotal.get(s.name));
  const days = new Map(cols.map((s) => [s.name, clock(s).n]));
  const now = currentSprint()?.name;
  const names = [...per.keys()].sort((a, b) => (a === 'Unassigned') - (b === 'Unassigned') || a.localeCompare(b));
  const perDay = (n, s) => n / days.get(s.name);
  const most = Math.max(0.1, ...names.flatMap((n) => cols.map((s) => perDay(per.get(n).get(s.name) ?? 0, s))));

  $('tk-daily-lede').textContent = `${WsCap()} per working day: each person's ${Ws()} in a sprint over its working days `
    + `(${[...new Set([...days.values()])].join(' or ') || 10}, Monday to Friday between the sprint's dates). `
    + `The team row is everybody together; the last column is each person's ${Ws()} across these sprints.`
    + (state.unit === 'tasks' ? ' Features and sub-tasks are not counted; switch to Tickets to count them.' : '');
  const table = $('tk-daily');
  if (!cols.length) {
    table.replaceChildren(el('caption', null, `No ${W1()} is in a dated sprint yet.`));
  } else {
    const head = el('tr');
    const th0 = el('th', null, 'Person');
    th0.scope = 'col';
    head.append(th0);
    for (const s of cols) {
      const th = el('th', `is-num${s.name === now ? ' is-now' : ''}`);
      th.scope = 'col';
      th.append(el('span', 'tk-daily-sprint', s.name), el('span', 'tk-daily-dates', `${fmtShort(s.start)}–${fmtShort(s.end)}`));
      head.append(th);
    }
    const thT = el('th', 'is-num', `Total ${Ws()}`);
    thT.scope = 'col';
    head.append(thT);

    const cell = (n, s) => {
      const v = perDay(n, s);
      const td = el('td', `is-num${s.name === now ? ' is-now' : ''}`, n ? v.toFixed(1) : '–');
      // A single hue, light to dark with the value: the busiest cells read first.
      if (n) td.style.background = `color-mix(in srgb, var(--accent) ${Math.round((v / most) * 26)}%, transparent)`;
      td.title = `${n ? nu(n) : `No ${Ws()}`} in ${s.name} over ${plural(days.get(s.name), 'working day', 'working days')}`;
      return td;
    };
    const body = el('tbody');
    for (const name of names) {
      const tr = el('tr', state.scope.person === name ? 'is-chosen' : null);
      const th = el('th');
      th.scope = 'row';
      const pick = el('button', 'tk-link', name);
      pick.type = 'button';
      pick.onclick = () => openPerson(name);
      th.append(pick);
      tr.append(th);
      let total = 0;
      for (const s of cols) { const n = per.get(name).get(s.name) ?? 0; total += n; tr.append(cell(n, s)); }
      tr.append(el('td', 'is-num', num(total)));
      body.append(tr);
    }
    const foot = el('tfoot');
    const team = el('tr', 'tk-daily-team');
    const tht = el('th', null, 'Team');
    tht.scope = 'row';
    team.append(tht);
    let grand = 0;
    for (const s of cols) {
      const n = colTotal.get(s.name);
      grand += n;
      const td = el('td', `is-num${s.name === now ? ' is-now' : ''}`, perDay(n, s).toFixed(1));
      td.title = `${nu(n)} in ${s.name} over ${plural(days.get(s.name), 'working day', 'working days')}`;
      team.append(td);
    }
    team.append(el('td', 'is-num', num(grand)));
    foot.append(team);
    const caption = el('caption', null, `${WsCap()} per working day, by sprint${now ? `; ${now} is now` : ''}`);
    const thead = el('thead');
    thead.append(head);
    table.replaceChildren(caption, thead, body, foot);
  }

  // Sprints with nothing in them, said once as runs: "Sprints 7 to 13".
  const runs = [];
  for (const s of empty) {
    const last = runs.at(-1);
    if (last && last[1] + 1 === s.number) last[1] = s.number; else runs.push([s.number, s.number]);
  }
  const said = runs.map(([a, b]) => (a === b ? `Sprint ${a}` : `Sprints ${a} to ${b}`)).join(', ');
  $('tk-daily-empty').textContent = [
    empty.length ? `${said} ${empty.length === 1 ? 'has' : 'have'} no ${Ws()} yet, so ${empty.length === 1 ? 'it is' : 'they are'} left out.` : '',
    unsprinted ? `${plural(unsprinted, `${W1()} has`, `${Ws()} have`)} no sprint and ${unsprinted === 1 ? 'is' : 'are'} not in the table.` : '',
  ].filter(Boolean).join(' ');
  $('tk-daily-count').textContent = `${WsCap()} a day, ${plural(names.filter((n) => n !== 'Unassigned').length, 'person', 'people')}`;
}

// ── finished each day ───────────────────────────────────────────────
//
// "Each day, tasks closed": what each person finished on each working day of a
// sprint, by the page's own rule for finished (closed, or waiting for QA). A
// ticket counts on the day ADAM closed it where the close went through ADAM
// (`closes`), and otherwise on the day it last changed in OpenProject, which
// is the nearest OpenProject 10's list gives and which a later edit moves; the
// note under the table says so every time, because a release that touches
// many tickets makes its own day read high.

/** Local calendar day of a moment, as a key. */
const dayKey = (d) => `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;

/** The days the section shows: a sprint's working days, or the last fifteen. */
function finishedRange() {
  const pick = state.fdRange;
  if (pick === 'last15') {
    const list = [];
    for (let d = today(); list.length < 15; d = addDays(d, -1)) if (isWorkday(d)) list.unshift(d);
    return { label: 'the last 15 working days', days: list, sprint: null };
  }
  const named = pick.startsWith('sprint:') ? sprintOf(pick.slice(7)) : null;
  const chosen = state.scope.sprint ? sprintOf(state.scope.sprint) : null;
  const s = (named?.start && named) || (chosen?.start && chosen) || currentSprint() || focusSprint();
  if (!s) { state.fdRange = 'last15'; return finishedRange(); }
  return { label: s.name, days: clock(s).days, sprint: s };
}

function drawFinishedDaily() {
  const range = finishedRange();
  const now = today();
  // A weekend day joins the table when something was finished on it: dropping
  // it would lose those tickets, and moving them to Monday would misdate them.
  {
    const first = range.days[0];
    const end = addDays(range.days.at(-1), 1);
    const have = new Set(range.days.map(dayKey));
    const extra = new Map();
    for (const t of counted()) {
      if (!isFinished(t) || !typeOk(t)) continue;
      const at = finishedAt(t);
      if (!at || at < first || at >= end) continue;
      const d = new Date(at.getFullYear(), at.getMonth(), at.getDate());
      if (!have.has(dayKey(d))) extra.set(dayKey(d), d);
    }
    if (extra.size) range.days = [...range.days, ...extra.values()].sort((x, y) => x - y);
  }
  const keys = range.days.map(dayKey);
  const index = new Map(keys.map((k, i) => [k, i]));
  const isFuture = (d) => d > now;

  // The days a reader can pick: each sprint that has begun, and the last 15.
  const select = $('tk-fd-range');
  const started = datedSprints().filter((s) => s.number != null && s.start <= now);
  const current = currentSprint()?.name;
  const value = range.sprint ? `sprint:${range.sprint.name}` : 'last15';
  select.replaceChildren(...started.map((s) => {
    const o = el('option', null, `${s.name}${s.name === current ? ' (now)' : ''}`);
    o.value = `sprint:${s.name}`;
    return o;
  }), Object.assign(el('option', null, 'Last 15 working days'), { value: 'last15' }));
  select.value = value;

  // Every finished ticket in the unit, under the type filter, on one of the days.
  const pool = counted().filter(typeOk);
  const per = new Map();
  const cells = new Map();     // `${name}|${day}` -> tickets
  const team = new Array(keys.length).fill(0);
  for (const t of pool) {
    if (!isFinished(t)) continue;
    const at = finishedAt(t);
    if (!at) continue;
    const i = index.get(dayKey(at));
    if (i == null) continue;
    const name = who(t);
    if (!per.has(name)) per.set(name, new Array(keys.length).fill(0));
    per.get(name)[i] += 1;
    team[i] += 1;
    const cellKey = `${name}|${keys[i]}`;
    if (!cells.has(cellKey)) cells.set(cellKey, []);
    cells.get(cellKey).push([t, at]);
  }
  // Everybody with work in the unit gets a row, so a day nobody finished
  // anything still shows who that was.
  for (const t of pool) if (!per.has(who(t))) per.set(who(t), new Array(keys.length).fill(0));
  const names = [...per.keys()].sort((a, b) => (a === 'Unassigned') - (b === 'Unassigned') || a.localeCompare(b));
  state.fdCells = cells;

  // The even pace for a day: its sprint's planned count over its working days.
  const planned = new Map();
  const target = range.days.map((d) => {
    if (!isWorkday(d)) return null;
    const s = datedSprints().find((x) => x.number != null && x.start <= d && d <= x.end);
    if (!s) return null;
    if (!planned.has(s.name)) {
      const live = pool.filter((t) => t.version === s.name && !isRejected(t)).length;
      planned.set(s.name, live / clock(s).n);
    }
    return planned.get(s.name);
  });

  const total = team.reduce((n, v) => n + v, 0);
  $('tk-fd-count').textContent = `${nu(total)} finished in ${range.label}`;
  $('tk-fd-lede').textContent = `${WsCap()} finished on each day of ${range.label}, by who holds them. `
    + `Finished is closed or waiting for QA. Select a number to list those ${Ws()} below the table.`;

  drawFinishedChart(range, team, target);

  // The table.
  const table = $('tk-fd');
  const head = el('tr');
  const th0 = el('th', null, 'Person');
  th0.scope = 'col';
  head.append(th0);
  range.days.forEach((d) => {
    const th = el('th', `is-num${+d === +now ? ' is-now' : ''}${isWorkday(d) ? '' : ' is-weekend'}`);
    th.scope = 'col';
    if (!isWorkday(d)) th.title = 'A weekend day, shown because something was finished on it';
    th.append(el('span', 'tk-daily-sprint', d.toLocaleDateString(undefined, { weekday: 'short' })),
      el('span', 'tk-daily-dates', fmtShort(d)));
    head.append(th);
  });
  const thT = el('th', 'is-num', `${WsCap()} finished`);
  thT.scope = 'col';
  head.append(thT);

  const pickCell = (name, i, n) => {
    const d = range.days[i];
    const td = el('td', `is-num${+d === +now ? ' is-now' : ''}`);
    if (isFuture(d)) { td.classList.add('is-future'); return td; }      // blank, not 0
    if (!n) { td.append(el('span', 'tk-fd-zero', '0')); return td; }
    const b = el('button', 'tk-fd-n', num(n));
    b.type = 'button';
    b.setAttribute('aria-label', `${name || 'The team'}, ${fmtWeekday(d)}: ${nu(n)} finished. List them.`);
    b.onclick = () => { state.fdPick = { name, day: keys[i] }; drawFinishedDetail(range); };
    td.append(b);
    return td;
  };
  const body = el('tbody');
  for (const name of names) {
    const tr = el('tr', state.scope.person === name ? 'is-chosen' : null);
    const th = el('th');
    th.scope = 'row';
    const pick = el('button', 'tk-link', name);
    pick.type = 'button';
    pick.onclick = () => openPerson(name);
    th.append(pick);
    tr.append(th);
    const row = per.get(name);
    row.forEach((n, i) => tr.append(pickCell(name, i, n)));
    const sum = row.reduce((a, v) => a + v, 0);
    const td = el('td', 'is-num');
    if (sum) {
      const b = el('button', 'tk-fd-n', num(sum));
      b.type = 'button';
      b.setAttribute('aria-label', `${name}: ${nu(sum)} finished in ${range.label}. List them.`);
      b.onclick = () => { state.fdPick = { name, day: '' }; drawFinishedDetail(range); };
      td.append(b);
    } else td.append(el('span', 'tk-fd-zero', '0'));
    tr.append(td);
    body.append(tr);
  }
  const foot = el('tfoot');
  const tr = el('tr', 'tk-daily-team');
  const tht = el('th', null, 'Team');
  tht.scope = 'row';
  tr.append(tht);
  team.forEach((n, i) => tr.append(pickCell('', i, n)));
  tr.append(el('td', 'is-num', num(total)));
  foot.append(tr);
  const thead = el('thead');
  thead.append(head);
  table.replaceChildren(el('caption', null, `${WsCap()} finished each day, ${range.label}`), thead, body, foot);

  const fromAdam = [...cells.values()].flat().filter(([t]) => state.data.closes?.[t.key]).length;
  $('tk-fd-note').textContent = `A ${W1()} counts on the day ADAM closed it where the close went through ADAM`
    + `${fromAdam ? ` (${num(fromAdam)} here)` : ' (none here yet)'}. Every other one counts on the day it last changed `
    + 'in OpenProject, because OpenProject 10 does not say when a status was reached, and that date is an approximation: '
    + 'a later edit or comment moves it. The r4 release changed many tickets on 13 October, so that day reads high. '
    + 'Days still to come are left blank'
    + (range.days.some((d) => !isWorkday(d)) ? '; a weekend day appears only when something was finished on it.' : '.');
  drawFinishedDetail(range);
}

/** The tickets behind the selected number, under the table. */
function drawFinishedDetail(range) {
  const box = $('tk-fd-detail');
  const pick = state.fdPick;
  if (!pick) { box.replaceChildren(); return; }
  const rows = [];
  for (const [key, list] of state.fdCells ?? []) {
    const [name, day] = key.split('|');
    if (pick.name && name !== pick.name) continue;
    if (pick.day && day !== pick.day) continue;
    rows.push(...list);
  }
  rows.sort((a, b) => b[1] - a[1]);
  const when = pick.day ? fmtWeekday(range.days.find((d) => dayKey(d) === pick.day)) : range.label;
  const head = el('div', 'tk-fd-detail-head');
  head.append(el('h3', 'tk-sub', `${pick.name || 'The team'}, ${when}: ${nu(rows.length)} finished`));
  const close = el('button', 'chip', 'Close the list');
  close.type = 'button';
  close.onclick = () => { state.fdPick = null; drawFinishedDetail(range); };
  head.append(close);
  const list = el('div', 'admin-table');
  for (const [t, at] of rows) {
    const row = el('div', 'admin-row tk-row tk-fd-row');
    const main = el('span', 'tk-main');
    main.append(el('span', 'tk-subject', t.subject || '(no subject)'));
    if (t.parentSubject) main.append(el('span', 'tk-parent', t.parentSubject));
    const how = state.data.closes?.[t.key] ? 'closed through ADAM' : 'last change';
    row.append(link(t.url, 'tk-key', `#${t.key}`), main, el('span', 'tk-who', who(t)), stateBadge(t),
      el('span', 'tk-when', `${at.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}, ${how}`));
    list.append(row);
  }
  if (!rows.length) list.append(el('p', 'tk-empty', `No ${W1()} here.`));
  box.replaceChildren(head, list);
}

/**
 * The team's finished count per day as thin bars, with the even pace for each
 * day as a dashed step line: a yardstick, not data, as in the burn-up. Days
 * to come draw no bar. Hover and focus per day; a hidden table twin.
 */
function drawFinishedChart(range, team, target) {
  const box = $('tk-fd-plot');
  const now = today();
  const W = Math.max(280, Math.round(box.clientWidth || 640));
  const H = 170;
  const m = { l: 40, r: 78, t: 16, b: 28 };
  const iw = W - m.l - m.r;
  const ih = H - m.t - m.b;
  const n = range.days.length;
  const top = roundUp(Math.max(1, ...team, ...target.filter((v) => v != null)));
  const x = (i) => m.l + (i / n) * iw;
  const y = (v) => m.t + ih - (v / top) * ih;
  const bw = Math.min(26, (iw / n) * 0.55);
  const pic = svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img',
    'aria-label': `${WsCap()} finished each day by the team, ${range.label}, against an even pace.` });
  for (const v of [0, top / 2, top]) {
    pic.append(svg('line', { x1: m.l, x2: m.l + iw, y1: y(v), y2: y(v), class: v ? 'tk-burn-grid' : 'tk-burn-base' }));
    pic.append(svg('text', { x: m.l - 8, y: y(v) + 4, class: 'tk-burn-tick', 'text-anchor': 'end' }, num(Math.round(v))));
  }
  // Day labels by priority (today, the first, the last, then Mondays), each
  // kept only where it does not touch one already placed.
  const gap = Math.ceil(46 / Math.max(1, iw / n));
  const todayAt = range.days.findIndex((d) => +d === +now);
  const wanted = [todayAt, 0, n - 1, ...range.days.map((d, i) => (d.getDay() === 1 ? i : -1))].filter((i) => i >= 0);
  const labelled = [];
  for (const i of wanted) if (!labelled.some((j) => Math.abs(j - i) < gap)) labelled.push(i);
  range.days.forEach((d, i) => {
    const cx = (x(i) + x(i + 1)) / 2;
    if (+d === +now) pic.append(svg('rect', { x: x(i), y: m.t, width: x(i + 1) - x(i), height: ih, class: 'tk-burn-today' }));
    if (labelled.includes(i)) {
      pic.append(svg('text', { x: cx, y: H - 10, class: 'tk-burn-tick', 'text-anchor': 'middle' }, +d === +now ? 'today' : fmtShort(d)));
    }
    if (d > now || !team[i]) return;
    const h = Math.max(2, (team[i] / top) * ih);
    // Square at the baseline, a 4px round at the data end.
    pic.append(svg('path', { class: 'tk-fd-bar', d: `M${cx - bw / 2},${y(0)} V${y(0) - h + 4} q0,-4 4,-4 H${cx + bw / 2 - 4} q4,0 4,4 V${y(0)} Z` }));
  });
  // The even pace, a step per day, dashed.
  const steps = [];
  target.forEach((v, i) => { if (v != null) steps.push(`M${x(i)},${y(v)} H${x(i + 1)}`); });
  if (steps.length) {
    pic.append(svg('path', { d: steps.join(' '), class: 'tk-burn-even tk-fd-even' }));
    const last = target.findLastIndex((v) => v != null);
    pic.append(svg('text', { x: x(n) + 6, y: y(target[last]) + 4, class: 'tk-burn-label' }, 'even pace'));
    pic.append(svg('text', { x: x(n) + 6, y: y(target[last]) + 18, class: 'tk-burn-tick' }, `${target[last].toFixed(1)} ${Ws()}`));
  }
  const hits = svg('g', { class: 'tk-burn-hits' });
  range.days.forEach((d, i) => {
    const hit = svg('rect', { x: x(i), y: m.t, width: x(i + 1) - x(i), height: ih, class: 'tk-burn-hit' });
    hit.dataset.tip = `${fmtWeekday(d)}: ${d > now ? 'still to come' : `${nu(team[i])} finished`}`
      + (target[i] != null ? `; an even pace is ${target[i].toFixed(1)} ${Ws()} a day` : '');
    hits.append(hit);
  });
  pic.append(hits);
  const table = el('table', 'tk-sr');
  table.append(el('caption', null, `${WsCap()} finished each day, ${range.label}`));
  const head = el('tr');
  head.append(el('th', null, 'Day'), el('th', null, `${WsCap()} finished`), el('th', null, `Even pace, ${Ws()} a day`));
  table.append(head);
  range.days.forEach((d, i) => {
    const row = el('tr');
    row.append(el('td', null, fmtWeekday(d)), el('td', null, d > now ? '' : num(team[i])),
      el('td', null, target[i] == null ? '' : target[i].toFixed(1)));
    table.append(row);
  });
  box.replaceChildren(pic, table);
  $('tk-fd-caption').textContent = `The team's ${Ws()} finished each day, against an even pace for the sprint`;
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
  wrap.append(cells, el('span', 'tk-gate-n', `${g.closed}/${g.every} tickets`));
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
  $('tk-people-lede').textContent = `Every person's ${Ws()} in ${focus ? focus.name : 'no dated sprint'} and in the whole plan, `
    + 'counted by assignee. Finished is closed plus waiting for QA (an open status named QA, review or testing), '
    + 'because that is where a developer’s finished work waits. Against pace is how far their finished count is '
    + 'from an even pace through the sprint’s working days. Late is still the developer’s and past its due date '
    + `or its sprint’s end. Rejected ${Ws()} are closed too but counted apart, so they never read as work delivered. `
    + 'The test gate counts tickets in either view: it is ten tickets closed through ADAM.';
  const table = $('tk-people');
  // Every column that carries something. A column of zeros (nothing closed
  // yet, nothing on hold) is said once in the note below the table instead.
  const columns = [
    [`${sprintName}: planned ${Ws()}`, (r) => r.c.live, true],
    ['Finished', (r) => r.c.finished, true],
    ['Closed', (r) => r.c.done],
    ['Waiting for QA', (r) => r.c.qa],
    ['In progress', (r) => r.c.going],
    ['On hold', (r) => r.c.stalled],
    ['Not started', (r) => r.c.fresh],
    ...(k?.phase === 'running' ? [['Behind pace', (r) => Math.max(0, r.behind)]] : []),
    [`Whole plan: open ${Ws()}`, (r) => r.open, true],
    ['Finished in the plan', (r) => r.finishedAll],
    ['Late', (r) => r.lateAll],
  ];
  const kept = columns.filter(([, get, always]) => always || rows.some((r) => get(r)));
  const dropped = columns.filter((col) => !kept.includes(col)).map(([label]) => label.toLowerCase());
  const head = el('tr');
  for (const [label, numeric] of [['Person', false], ...kept.map(([l]) => [l, true]), ['Test gate (tickets)', false]]) {
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
    pick.onclick = () => openPerson(r.name);
    name.append(pick);
    tr.append(name);
    for (const [label, get] of kept) {
      const v = get(r);
      tr.append(el('td', `is-num${label === 'Late' && v ? ' is-late' : ''}`, num(v)));
    }
    tr.append(el('td', 'tk-gate-cell', r.gate ? `${r.gate.closed}/${r.gate.every} tickets, ${gateState(r.gate).text}` : '—'));
    body.append(tr);
  }
  $('tk-people-zero').textContent = dropped.length
    ? `Left out because every count in them is zero: ${dropped.join(', ')}.` : '';
  const caption = el('caption', null, `${WsCap()} per person, ${sprintName} and the whole plan`);
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
  if (!rows.length) box.append(el('p', 'tk-empty', `No ${Ws()} to count.`));
  $('tk-states-count').textContent = `${rows.length} in use, counted in ${Ws()}`;
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
function paged(box, rows, draw1, size, empty, unit = null) {
  let limit = size;
  const render = () => {
    box.replaceChildren(...rows.slice(0, limit).map(draw1));
    if (rows.length > limit) {
      const more = el('button', 'chip tk-more', `Show ${num(Math.min(size, rows.length - limit))} more of ${(unit ?? num)(rows.length - limit)}`);
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
  $('tk-dates-lede').textContent = `Open ${Ws()} past the day they were due, then what falls due in the next seven days. `
    + (ownDates ? `A ${W1()} with a due date of its own is due then; any other is due when its sprint ends. `
      : `No ${W1()} in this view has a due date of its own, so each is due when its sprint ends. `)
    + `${WsCap()} waiting for QA are left out: their developer has finished them.`;
  const when = (t) => (t.dueDate ? `due ${fmtDay(asDay(t.dueDate))}` : `${t.version} ends ${fmtShort(dueOn(t))}`);
  paged($('tk-overdue'), late, (t) => ticketRow(t, `${plural(days(dueOn(t), today()), 'day', 'days')} late, ${when(t)}`),
    50, `No open ${W1()} is late.`, nu);
  paged($('tk-soon'), soon, (t) => ticketRow(t, when(t)), 50, `No open ${W1()} is due in the next seven days.`, nu);
  $('tk-dates-count').textContent = `${nu(late.length)} late, ${num(soon.length)} due this week`;
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
      if (tickets.length > 12) chips.append(el('span', 'tk-quiet', `and ${nu(tickets.length - 12)} more`));
      row.append(chips, el('span', 'tk-bar-extra',
        done === tickets.length ? 'finished' : tickets.length > 1 ? `${num(done)} of ${nu(tickets.length)} finished` : ''));
      return row;
    }, 100, '');
    group.append(table);
    box.append(group);
  }
  if (!kinds.length) {
    box.append(el('p', 'tk-empty',
      `No ${W1()} in this view is linked to a part of the package yet. Claude Code links one with adam_link, `
      + 'and then a ticket and the screen or contract it builds are the same piece of work here.'));
  }
  $('tk-deliverables-count').textContent = artefacts ? plural(artefacts, 'artefact', 'artefacts') : '';
  const loose = items.length - linked;
  $('tk-unlinked').textContent = loose
    ? `${plural(loose, `${W1()} is`, `${Ws()} are`)} not linked to anything in the package, so ${loose === 1 ? 'it does' : 'they do'} not appear above.`
    : `Every ${W1()} in this view is linked to something in the package.`;
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
    ? `${plural(undated, `${W1()} has`, `${Ws()} have`)} neither a sprint nor a date in OpenProject, so `
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
    wrap.append(el('summary', 'tk-sub', `${group.name}: ${plural(rows.length, 'row', 'rows')}, ${num(done)} of ${nu(all.length)} finished`));
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
      bar.dataset.tip = `${r.name}: ${fmtDay(r.from)} to ${fmtDay(r.to)}, ${num(doneHere)} of ${nu(r.tickets.length)} finished`
        + (late ? '; something in it is late' : '');
      track.append(bar);
      row.append(label, track, el('span', 'tk-gantt-count', `${num(doneHere)}/${num(r.tickets.length)}`));
      wrap.append(row);
    }
    box.append(wrap);
  });
  if (!shown) box.append(el('p', 'tk-empty', 'Everything placed is finished.'));
  $('tk-timeline-count').textContent = `${plural(shown, 'row', 'rows')}, counted in ${Ws()}`;
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
    const extra = [`${num(done)} of ${nu(r.tickets.length)} finished`, late ? `${num(late)} late` : ''].filter(Boolean).join(', ');
    const row = barRow(r.name, r.tickets.length, biggest, done === r.tickets.length ? 'done' : late ? 'bad' : 'fresh', extra);
    row.prepend(r.key ? link(`${state.data.endpoint}/work_packages/${r.key}`, 'tk-key', `#${r.key}`)
      : el('span', 'tk-key tk-key-none', '—'));
    return row;
  }, 60, `No ${Ws()} to group.`);
  $('tk-parents-count').textContent = `${plural(rows.filter((r) => r.key).length, 'parent', 'parents')}, counted in ${Ws()}`;
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
    const more = el('button', 'chip tk-more', `Show ${num(Math.min(LIST_PAGE, rows.length - listLimit))} more of ${nu(rows.length - listLimit)}`);
    more.type = 'button';
    more.onclick = () => { listLimit += LIST_PAGE; drawList(); };
    box.append(more);
  }
  if (!rows.length) {
    box.append(el('p', 'tk-empty', counted().length
      ? 'Nothing matches these filters.'
      : (state.data.note ?? 'This project has no tickets in OpenProject yet.')));
  }
  const all = counted().length;
  $('tk-tickets-count').textContent = rows.length === all
    ? nu(rows.length)
    : `${num(rows.length)} of ${nu(all)}`;
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
  if (!$('finished').hidden) drawFinishedDaily();
  const focus = focusSprint();
  if (!focus) return;
  const k = clock(focus);
  if (k.phase === 'ahead') return;
  const items = inFocus(focus);
  const c = count(items);
  if (c.live) drawBurn(focus, items, c, k);
  if (state.scope.person) {
    const theirs = mineOf(state.scope.person).filter((t) => t.version === focus.name);
    const tc = count(theirs);
    if (tc.live) drawBurn(focus, theirs, tc, k, { figure: 'tk-p-burn', box: 'tk-p-burn-plot', caption: 'tk-p-burn-caption' });
  }
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
  state.scope = { person: params.get('person') ?? params.get('who') ?? '', sprint: params.get('sprint') ?? '', type: params.get('type') ?? '' };
  // ?count= wins, so a link says what it was counted in; then this reader's
  // last choice; then tasks.
  {
    let saved = '';
    try { saved = localStorage.getItem('adam-tasks-count') ?? ''; } catch { /* storage denied */ }
    const asked = params.get('count');
    state.unit = ['tasks', 'tickets'].includes(asked) ? asked : ['tasks', 'tickets'].includes(saved) ? saved : 'tasks';
  }
  for (const b of document.querySelectorAll('[data-unit]')) b.onclick = () => setUnit(b.dataset.unit);
  try {
    const saved = localStorage.getItem('adam-tasks-team-sort');
    if (['behind', 'planned', 'done', 'name'].includes(saved)) state.teamSort = saved;
  } catch { /* storage denied */ }
  $('tk-team-sort').value = state.teamSort;

  // The role file and the project picker, filled in as they arrive and not
  // waited for: the tickets do not depend on either, and drawing them used to
  // wait for both, one round trip after the other.
  loadTeam();
  const picker = $('tk-project');
  picker.hidden = true;
  auth.listProjects().then(({ projects }) => {
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
    // One project, or none listed: a picker with nothing to pick is a blank box.
    picker.hidden = picker.options.length < 2;
  }).catch(() => { /* the page still works for the current project */ });

  $('tk-gantt-open').onchange = (e) => {
    state.ganttOpenOnly = e.target.checked;
    drawTimeline(scoped());
  };
  $('tk-scope-person').onchange = (e) => (e.target.value ? openPerson(e.target.value) : backToTeam());
  $('tk-p-back').onclick = (e) => { e.preventDefault(); backToTeam(); };
  $('tk-p-all').onclick = () => { location.hash = '#tickets'; };
  // A link to somebody's page opens on it, whatever the rail last showed.
  if (state.scope.person && !location.hash) history.replaceState(null, '', `${location.pathname}${location.search}#person`);
  $('tk-scope-sprint').onchange = (e) => { state.fdRange = ''; state.fdPick = null; setScope({ sprint: e.target.value }); };
  $('tk-fd-range').onchange = (e) => { state.fdRange = e.target.value; state.fdPick = null; drawFinishedDaily(); };
  $('tk-scope-type').onchange = (e) => setScope({ type: e.target.value });
  $('tk-scope-clear').onclick = () => {
    setScope({ person: '', sprint: '', type: '' });
    if (location.hash === '#person') location.hash = '#overview';
  };
  $('tk-team-sort').onchange = (e) => {
    state.teamSort = e.target.value;
    try { localStorage.setItem('adam-tasks-team-sort', state.teamSort); } catch { /* storage denied */ }
    const focus = focusSprint();
    drawRoster(focus);
    drawPeopleTable(focus);
  };

  // Answered at once: the service starts the read (or joins the one running)
  // and says `refreshing`, and `load` keeps asking until the new read is in.
  // The button is `load`'s to put back up, when the read is done.
  $('tk-refresh').onclick = () => load({ refresh: true });
  setInterval(drawAsOf, 30_000);
  $('tk-search').oninput = (e) => { state.filter.text = e.target.value; listLimit = LIST_PAGE; drawList(); };
  $('tk-status').onchange = (e) => { state.filter.status = e.target.value; listLimit = LIST_PAGE; drawList(); };
  $('tk-open-only').onchange = (e) => { state.filter.openOnly = e.target.checked; listLimit = LIST_PAGE; drawList(); };
  $('tk-export').onclick = exportCsv;
  mountTip();
  let resizing = 0;
  addEventListener('resize', () => { clearTimeout(resizing); resizing = setTimeout(redrawBurn, 150); });

  loaderSays('Reading the delivery board…');
  await load({ answer: firstAnswer });
  // One section at a time, driven by the rail. Same mechanism as the settings
  // page; see panels.js.
  mountPanels({ nav: document.querySelector('#tasks .set-nav'), fallback: 'overview',
    onShow: (name) => {
      if (name === 'overview' || name === 'person') redrawBurn();
      // Drawn to its box's width, which is nothing while the section is hidden.
      if (name === 'finished' && state.data) drawFinishedDaily();
    } });
  hideLoader();
})();
