/**
 * What a ticket is, which sprint it is in, and how a set of them stands against
 * an even pace. Tasks and My work both read these, so the two pages cannot
 * disagree about what "finished", "late" or "behind" means.
 *
 * **Moved out of tasks.js unchanged (14 October).** My work opens on the same
 * sentence the Tasks page says about one person: "Sprint 3: 6 of your 14
 * finished, 2 behind an even pace". Two copies of the rules would agree on
 * the day they were written and drift on the first change, and then a developer
 * would read one number on their own page and another on Tasks. So the rules
 * live here, once, and the guesses they make are written down in tasks.js's
 * header, which is still where somebody looking for them goes first.
 *
 * **Two things a page has to tell it before asking anything:** the instance's
 * statuses (`learnStatuses`, which ones are closed and which one a new ticket
 * starts in) and the project's versions (`buildSprints`, the sprints' dates).
 * Both are module state rather than arguments to every call, because every
 * question below is asked hundreds of times a draw and the answers never vary
 * between two loads.
 */

// Open states that mean the work has stopped. A guess: OpenProject has no
// "blocked" flag, so the name is all there is. The service makes the same
// guess when it reads the reason (main.py `_HELD`).
export const STALLED = /hold|block|wait|pend/i;
// Closed states that mean the work was not done.
export const DROPPED = /reject|cancel|duplicate|won.?t|invalid|obsolete/i;
// Used only when the instance does not say which status is the default.
export const FRESH = /^(new|to ?do|backlog|open|not started)$/i;
// Open states that mean the developer has finished and somebody else is next,
// and the ones among them that mean it came back ("Test failed", "Reopened").
export const AWAITING = /\bqa\b|review|testing|tested|verif/i;
export const BOUNCED = /fail|reopen/i;

// ── days ────────────────────────────────────────────────────────────

export const DAY = 86_400_000;
export const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
export const asDate = (iso) => { const d = iso ? new Date(iso) : null; return d && !Number.isNaN(+d) ? d : null; };
/** A date-only field ("2026-10-05") as local midnight. `new Date()` reads it as
 *  UTC, which in India puts the first day of a sprint at 05:30 — after today's
 *  midnight, so on its first morning the sprint had not started. */
export const asDay = (iso) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso ?? '');
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
};
export const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
export const days = (from, to) => Math.round((to - from) / DAY);
export const isWorkday = (d) => d.getDay() !== 0 && d.getDay() !== 6;

// ── what a ticket is ────────────────────────────────────────────────
//
// Every question a page asks about one ticket, asked once here so the
// sections cannot disagree about what "finished" or "late" means.

let closedByName = new Map();   // status name -> isClosed, from OpenProject
let defaultStatus = new Set();  // the status(es) a new ticket starts in

/** The instance's own statuses, as the service sends them: `{name, isClosed, isDefault}`. */
export function learnStatuses(statuses) {
  closedByName = new Map((statuses ?? []).map((s) => [s.name, !!s.isClosed]));
  defaultStatus = new Set((statuses ?? []).filter((s) => s.isDefault).map((s) => s.name));
}

export const isClosed = (t) => closedByName.get(t.status) === true;
export const isRejected = (t) => isClosed(t) && DROPPED.test(t.status || '');
export const isDone = (t) => isClosed(t) && !isRejected(t);
export const isAwaiting = (t) => !isClosed(t) && AWAITING.test(t.status || '') && !BOUNCED.test(t.status || '');
export const isFinished = (t) => isDone(t) || isAwaiting(t);
/** Still the developer's to do: open, and not waiting on QA. */
export const isOpenWork = (t) => !isClosed(t) && !isAwaiting(t);
export const isStalled = (t) => isOpenWork(t) && STALLED.test(t.status || '');
export const isFresh = (t) => isOpenWork(t) && !isStalled(t)
  && (defaultStatus.size ? defaultStatus.has(t.status) : FRESH.test(t.status || ''));

/** The five kinds a bar draws, in the order it draws them. */
export const KINDS = [
  { id: 'done', label: 'Closed' },
  { id: 'qa', label: 'Waiting for QA' },
  { id: 'going', label: 'In progress' },
  { id: 'stalled', label: 'On hold' },
  { id: 'fresh', label: 'Not started' },
];
export const kindOf = (t) => (isRejected(t) ? 'rejected' : isDone(t) ? 'done' : isAwaiting(t) ? 'qa'
  : isStalled(t) ? 'stalled' : isFresh(t) ? 'fresh' : 'going');

/** When a ticket is due: its own date, or failing that its sprint's last day.
 *  TICVAI's tickets carry no dates of their own; the sprint is the deadline. */
export const dueOn = (t) => asDay(t.dueDate) ?? sprintOf(t.version)?.end ?? null;
export const isLate = (t) => { const d = dueOn(t); return isOpenWork(t) && d != null && d < today(); };
export const isDueSoon = (t) => {
  const d = dueOn(t);
  return isOpenWork(t) && d != null && d >= today() && d <= addDays(today(), 7);
};

// ── sprints ─────────────────────────────────────────────────────────
//
// A ticket names its version and nothing else. The service sends each
// version's dates where OpenProject has them; a "Sprint N" without dates falls
// back to TICVAI's calendar — two-week sprints from Monday 5 October 2026,
// Monday to the Friday of the second week.

export const SPRINT_ONE = new Date(2026, 9, 5);
let sprintTable = new Map();

/** The sprint table, from the project's versions and the tickets that name them. */
export function buildSprints(versions, items) {
  sprintTable = new Map();
  for (const v of versions ?? []) {
    sprintTable.set(v.name, { name: v.name, start: asDay(v.startDate), end: asDay(v.endDate), fromCalendar: false });
  }
  for (const t of items ?? []) {
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
export const sprintOf = (name) => (name ? sprintTable.get(name) : null);
/** The dated sprints, in calendar order: the plan's columns. */
export const datedSprints = () => [...sprintTable.values()].filter((s) => s.start && s.end).sort((a, b) => a.start - b.start);

/** The sprint today is in: the latest one that has started and not ended more
 *  than a weekend ago. */
export function currentSprint() {
  const now = today();
  return datedSprints().filter((s) => s.start <= now && +s.end + 3 * DAY >= +now).at(-1) ?? null;
}
export const nextSprint = (s) => datedSprints().find((x) => s && x.start > s.start) ?? null;

/** Where a sprint stands in its own working days. `through` counts today. */
export function clock(s) {
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

// ── counting ────────────────────────────────────────────────────────

export function count(items) {
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

/** How a set of sprint tickets stands against an even pace: the one place the
 *  sprint section and the person page both take their verdict from. */
export function paceFor(focus, items) {
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
