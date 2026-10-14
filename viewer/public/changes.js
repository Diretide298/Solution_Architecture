/**
 * Change requests: where the package was found wrong.
 *
 * Raised by the team - often by a developer's Claude while building, after the
 * developer agreed - taken on by the lead whose side and platform it is, and
 * settled by that lead, a reviewer on the project or an admin.
 *
 * **Built on the sheet, the way Tasks is.** The page opens on one sentence
 * answering the question it is opened for every morning - what is waiting on
 * somebody, and who - then the figures that sentence rests on, one picture
 * (where every request is on its way from raised to done), and the next thing
 * to do. Everything else is a section on the rail, and every section obeys one
 * filter kept in the address. See sheet.js.
 *
 * **Rows, not cards.** The old page drew a collapsed card per request with every
 * action hidden inside it, newest first. A lead reading forty of them could not
 * see which mattered. Each section is now a table ordered by urgency - blocking
 * work first, then requests nobody has taken on past the two days, then the
 * oldest - and opening a row (or arriving on `?cr=CR-031`) shows the request in
 * full with one primary button: the next step its state allows.
 *
 * The list and the project names are asked for at the top, beside the sign-in
 * check rather than after it (13 October): round trips that depend on nothing
 * but the project. Signed out, they come back 401 and are ignored, because
 * `requireSignIn` is already sending the reader to the door.
 */
// The viewer's top bar on a page that is not the viewer: layer tabs, bell,
// account drawer.
import '/page-chrome.js';
import * as auth from '/validation.js';
import { hideLoader } from '/loader.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, ago, daysSince, param, setParams, personLink,
  verdict, next, mountScope, legend, badge, confirmStep,
} from '/sheet.js';
// The file this page hands out, and the labels on it. Shared with the
// service's own export of the same register rather than spelled again here:
// either file can be filled in and uploaded back, which only holds while the
// two are the same file. See change-csv.js.
import { CHANGE_KIND_LABEL, CHANGE_SIDE_LABEL, CHANGE_STATUS_LABEL, toChangeCsv } from '/change-csv.js';

const firstList = auth.ensureProject().then((project) => auth.listChanges(project));
const firstRegistry = auth.listProjects();
firstList.catch(() => { /* answered by load() */ });
firstRegistry.catch(() => { /* answered below */ });

const $ = (id) => document.getElementById(id);
const KINDS = CHANGE_KIND_LABEL;
const DAY = 86_400_000;

const state = {
  project: null,
  projectName: '',
  me: null,
  items: [],
  mayResolve: false,
  afterDays: 2,
  // CR id -> {waitingDays, shouldBe}, from /api/changes/overdue. That route is
  // an admin's or a pm's (it names who should have acted); everybody else gets
  // the waiting time worked out here and no names.
  overdue: new Map(),
  // The release being served and what was settled in it, for "this release".
  release: null,
  readAt: null,
  // The request open in its section, which is also `?cr=` in the address.
  open: '',
  section: 'decide',
  scope: null,
  // What OpenProject says about each request's ticket, asked once per request
  // and only when somebody opens it: a read is three calls to OpenProject.
  sources: new Map(),
  // Text typed into a request's fields, kept across redraws: a filter change
  // or another request settled redraws every table, and a lead halfway through
  // a decision note should not lose it to that.
  drafts: new Map(),
  // What the last action on a request did, said at the top of its detail.
  said: new Map(),
};
let showSection = () => {};

function showError(message) {
  $('cr-error').textContent = message;
  $('cr-error').hidden = !message;
}

// ── what each request is, in this page's words ──────────────────────

const mine = (name) => !!(state.me && name && [state.me.name, state.me.email].includes(name));
const ageMs = (iso) => Date.now() - (Date.parse(iso ?? '') || Date.now());

/**
 * Where a request is on its way, and what that is called.
 *
 * `stage` is the column of the flow strip; `tone` is its colour, one of the
 * sheet's state words and only ever in its sheet meaning:
 *   late     open, nobody has taken it on, and the two days are up
 *   fresh    open, nobody has taken it on, inside the two days
 *   going    somebody has it: taken on and being decided, or scheduled and
 *            being fixed
 *   stalled  accepted, and waiting for a ticket or a comment to carry it
 *   done     the package has been fixed
 * Rejected requests are off the line and drawn in no colour.
 */
function facts(c) {
  const open = c.status === 'open';
  const untaken = open && !c.pickedBy;
  // The service's own rule, measured the same way: raised more than the
  // window ago, open and untaken. Its answer wins when it was asked for.
  const late = untaken && (state.overdue.has(c.id) || ageMs(c.raisedAt) > state.afterDays * DAY);
  const stage = open ? 'raised'
    : c.status === 'accepted' ? (c.childTicket ? 'scheduled' : 'decided')
      : c.status;
  const tone = { raised: untaken ? (late ? 'late' : 'fresh') : 'going', decided: 'stalled',
    scheduled: 'going', done: 'done', rejected: 'quiet' }[stage];
  const word = { raised: untaken ? 'Open' : 'Taken on', decided: 'Accepted', scheduled: 'Scheduled',
    done: 'Done', rejected: 'Rejected' }[stage];
  // How long it has been waiting on whoever acts next.
  const since = open ? c.raisedAt : stage === 'decided' ? c.resolvedAt
    : stage === 'scheduled' ? (c.childAt ?? c.resolvedAt) : null;
  const waiting = since ? daysSince(since) : null;
  const active = open || c.status === 'accepted';
  return { open, untaken, late, stage, tone, word, waiting, active, blocking: c.blocking && active };
}

const slice = (c) => c.slice || (c.tag ? `${CHANGE_SIDE_LABEL[c.tag] ?? c.tag}${c.platform ? ` · ${c.platform}` : ''}` : '');
const days = (n) => (n === 0 ? 'under a day' : plural(n, 'day'));

/** Most urgent first: blocking work, then past the window, then the longest waiting. */
function byUrgency(a, b) {
  const x = facts(a), y = facts(b);
  return (Number(y.active) - Number(x.active))
    || (Number(y.blocking) - Number(x.blocking))
    || (Number(y.late) - Number(x.late))
    || ((y.waiting ?? -1) - (x.waiting ?? -1))
    || (b.number - a.number);
}

const NEXT_STEP = {
  raised: (c) => (c.pickedBy ? 'Decide' : 'Take it on'),
  decided: (c, info) => decidedStep(c, info),
  scheduled: () => 'Mark done when fixed',
  done: () => '',
  rejected: () => '',
};

/**
 * Accepted, not yet scheduled: what is left depends on the ticket it came out
 * of, which only OpenProject knows. Settling an open ticket already comments on
 * it, so "Schedule it" was usually wrong: the agent had the decision and all
 * that was left was marking it done. Until the ticket has been read the row
 * says the neutral thing; `nextCell` reads it and puts the answer in.
 */
function decidedStep(c, info) {
  if (!c.ticket) return 'Make a ticket';
  if (!info?.read) return 'Schedule it';
  if (info.onSettle?.accepted?.action === 'ticket') return 'Make a ticket';
  if (info.told?.includes('accepted')) return 'Mark done when fixed';
  return `Add the comment to #${c.ticket}`;
}

function nextCell(c, stage) {
  const td = el('td', 'cr-c-next', NEXT_STEP[stage](c));
  if (stage === 'decided' && c.ticket && (c.mayFileTicket || c.maySettle)) {
    source(c).then((info) => { td.textContent = NEXT_STEP.decided(c, info); });
  }
  return td;
}

// ── the filter ──────────────────────────────────────────────────────

function inScope(c, s = state.scope?.state ?? {}) {
  if (s.side === 'none' ? !!c.tag : (s.side && c.tag !== s.side)) return false;
  if (s.platform && c.platform !== s.platform) return false;
  if (s.status && c.status !== s.status) return false;
  if (s.person && c.raisedBy !== s.person && c.pickedBy !== s.person) return false;
  if (s.blocking && !c.blocking) return false;
  // A lens, never a wall: a lead reads the whole project and this narrows
  // what is on screen. The service sends every request either way.
  if (s.mine && !c.mine) return false;
  if (s.q) {
    const hay = [c.id, c.title, c.target?.kind, c.target?.id, c.ticket, c.childTicket, c.raisedBy,
      c.pickedBy, c.problem, c.resolution].join(' ').toLowerCase();
    if (!hay.includes(s.q.toLowerCase())) return false;
  }
  return true;
}
const shown = () => state.items.filter((c) => inScope(c));
const narrowed = () => {
  const s = state.scope?.state ?? {};
  return ['side', 'platform', 'status', 'person', 'q', 'blocking', 'mine'].some((k) => !!s[k]);
};

function says(s) {
  const total = state.items.length;
  // Counted from the state handed in: on the first draw the filter is still
  // being mounted and `state.scope` does not exist yet.
  const n = state.items.filter((c) => inScope(c, s)).length;
  const bits = [];
  if (s.side) bits.push(s.side === 'none' ? 'with no side yet' : `${CHANGE_SIDE_LABEL[s.side]} only`);
  if (s.platform) bits.push(`on ${s.platform}`);
  if (s.status) bits.push(`${CHANGE_STATUS_LABEL[s.status].toLowerCase()} only`);
  if (s.person) bits.push(`raised or held by ${s.person}`);
  if (s.q) bits.push(`matching "${s.q}"`);
  if (s.blocking) bits.push('blocking work');
  if (s.mine) bits.push('on your platforms');
  if (!bits.length) return `Showing all ${plural(total, 'change request')}.`;
  return `Showing ${fmt(n)} of ${plural(total, 'change request')}: ${bits.join(', ')}.`;
}

function mountFilter() {
  const people = () => [...new Set(state.items.flatMap((c) => [c.raisedBy, c.pickedBy]).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b)).map((p) => [p, p]);
  const platforms = () => [...new Set(state.items.map((c) => c.platform).filter(Boolean))]
    .sort().map((p) => [p, p]);
  const fields = [
    { key: 'side', label: 'Side', all: 'Both sides',
      options: [['frontend', 'Frontend'], ['backend', 'Backend'], ['none', 'Nobody has said']] },
    { key: 'platform', label: 'Platform', all: 'Every platform', options: platforms },
    { key: 'status', label: 'Status', all: 'Any status',
      options: Object.entries(CHANGE_STATUS_LABEL) },
    { key: 'person', label: 'Raised or held by', all: 'Anyone', options: people },
    { key: 'q', label: 'Search', kind: 'search', placeholder: 'Title or ticket' },
    { key: 'blocking', label: 'Blocking work only', kind: 'check' },
  ];
  // Offered only where it would do something. Somebody who owns no platform
  // has no "mine", and a filter that empties the page is worse than none.
  if (state.items.some((c) => c.mine)) fields.push({ key: 'mine', label: 'My platforms only', kind: 'check' });
  state.scope = mountScope({ root: $('cr-scope'), fields, says, onChange: () => draw() });
}

// ── reading ─────────────────────────────────────────────────────────

async function load(answer = null) {
  try {
    const data = await (answer ?? auth.listChanges(state.project));
    state.items = data.items ?? [];
    // The service's answer says which project it read, which is the one the
    // page is about when neither the address nor the last visit named one.
    if (data.project && !state.project) state.project = data.project;
    if (!state.projectName) state.projectName = state.project;
    state.mayResolve = Boolean(data.mayResolve);
    state.afterDays = data.afterDays ?? 2;
    state.readAt = new Date();
    showError('');
  } catch (error) {
    state.items = [];
    showError(error.status === 403
      ? 'Change requests are for the delivery team, and this account cannot see them. If that is wrong, ask an administrator.'
      : `Could not read the change requests: ${error.message}. Try Refresh; if it keeps failing, the accounts service is down.`);
  }
  // Who should have taken each one. An admin's or a pm's question; anybody
  // else is answered from the rows above, without names.
  if (auth.isReader(state.me)) {
    try {
      const late = await auth.overdueChanges(state.project);
      state.overdue = new Map((late.items ?? []).map((c) => [c.id, c]));
    } catch { state.overdue = new Map(); }
  }
  // The filter's sentence counts the rows, and its people and platforms come
  // from them, so it is redrawn with every read - and only then: redrawing it
  // while somebody types in its search box would take the caret away.
  state.scope?.redraw();
}

async function loadRelease() {
  try {
    const latest = await auth.changeReleaseNotes(state.project);
    // The release before the one served, so "in r5" is what was settled
    // between r4 and r5 rather than everything ever settled up to r5.
    const n = Number(String(latest.to?.tag ?? '').replace(/\D/g, ''));
    let inIt = latest;
    if (n > 1) {
      try { inIt = await auth.changeReleaseNotes(state.project, `r${n - 1}`, latest.to.tag); } catch { /* the first tag */ }
    }
    state.release = { to: latest.to, from: inIt.from, items: inIt.items ?? [], markdown: inIt.markdown ?? '' };
  } catch (error) {
    state.release = { error: error.status === 409
      ? 'There is no release tag yet, so nothing has been released.'
      : `The release record could not be read: ${error.message}.` };
  }
}

const releasedAt = () => Date.parse(state.release?.to?.taggedAt ?? '') || null;

// ── the opening ─────────────────────────────────────────────────────

/** A link to one request, opening it in place rather than reloading. */
function crLink(c, text = c.id, className = 'sh-key') {
  const a = el('a', className, text);
  const params = new URLSearchParams(location.search);
  params.set('cr', c.id);
  a.href = `${location.pathname}?${params}#${homeOf(c)}`;
  a.onclick = (e) => { e.preventDefault(); openCr(c.id); };
  return a;
}

function drawVerdict(rows) {
  const f = rows.map((c) => [c, facts(c)]);
  const open = f.filter(([, x]) => x.open);
  const untaken = open.filter(([, x]) => x.untaken);
  const late = untaken.filter(([, x]) => x.late);
  const decided = f.filter(([, x]) => x.stage === 'decided');
  const scheduled = f.filter(([, x]) => x.stage === 'scheduled');
  const blocking = f.filter(([, x]) => x.blocking);
  const since = releasedAt();
  const tag = state.release?.to?.tag;
  const done = f.filter(([c, x]) => x.stage === 'done' && (!since || Date.parse(c.resolvedAt) > since));
  const unrouted = open.filter(([c]) => !c.tag);

  let headline;
  if (!state.items.length) headline = 'No change requests yet.';
  else if (!rows.length) headline = 'Nothing matches this filter.';
  else if (open.length) headline = `${plural(open.length, 'change request')} need${open.length === 1 ? 's' : ''} a decision.`;
  else if (decided.length) headline = `Nothing waits for a decision; ${plural(decided.length, 'accepted request')} ${decided.length === 1 ? 'is' : 'are'} not scheduled.`;
  else headline = 'Nothing is waiting on anybody.';

  const pill = late.length ? { tone: 'bad', text: `${fmt(late.length)} waiting too long` }
    : untaken.length ? { tone: 'warn', text: `${fmt(untaken.length)} not taken on` }
      : rows.length ? { tone: 'ok', text: open.length ? 'Everything open has somebody' : 'All clear' } : null;

  // The sentence under it: what is blocked, and the one request most overdue,
  // with whose it is - the thing a lead would say out loud at the stand-up.
  const pace = [];
  if (blocking.length) pace.push(`${fmt(blocking.length)} ${blocking.length === 1 ? 'is' : 'are'} blocking work`);
  const worst = [...untaken].sort(([a], [b]) => byUrgency(a, b))[0];
  if (worst) {
    const [c, x] = worst;
    const who = state.overdue.get(c.id)?.shouldBe?.map((p) => p.name) ?? [];
    const where = slice(c) || 'no side yet';
    const line = [crLink(c), ` has waited ${days(x.waiting ?? 0)} with nobody on it (${where})`];
    if (who.length) line.push(`; ${who.join(' or ')} should take it on`);
    pace.push(line);
  }
  const paceNode = el('span');
  pace.forEach((part, i) => {
    if (i) paceNode.append('; ');
    if (Array.isArray(part)) paceNode.append(...part); else paceNode.append(part);
  });
  if (pace.length) paceNode.append('.');

  const saying = [];
  if (unrouted.length) {
    saying.push(`${plural(unrouted.length, 'open request')} ${unrouted.length === 1 ? 'has' : 'have'} no side yet, so no lead owns ${unrouted.length === 1 ? 'it' : 'them'}: ${unrouted.map(([c]) => c.id).join(', ')}.`);
  }
  const rejected = f.filter(([, x]) => x.stage === 'rejected').length;
  if (rejected) saying.push(`${plural(rejected, 'request')} ${rejected === 1 ? 'was' : 'were'} rejected: the package was right.`);

  const when = el('span');
  when.append(el('strong', '', state.projectName || state.project || ''),
    state.readAt ? ` · read at ${state.readAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : '');

  verdict($('cr-verdict'), {
    when,
    headline,
    headlineId: 'cr-headline',
    pill,
    pace: pace.length ? paceNode : '',
    ledger: rows.length ? [
      { label: 'Open', value: open.length, title: 'Waiting for a decision' },
      { label: 'Not taken on', value: untaken.length, swatch: 'fresh', bad: late.length > 0,
        title: late.length ? `${fmt(late.length)} past the ${days(state.afterDays)} with nobody on them` : 'Nobody has said they are dealing with these' },
      { label: 'Not scheduled', value: decided.length, swatch: 'stalled', title: 'Accepted, and no ticket or comment carries the fix yet' },
      { label: 'Scheduled', value: scheduled.length, swatch: 'going' },
      { label: tag && since ? `Done since ${tag}` : 'Done', value: done.length, swatch: 'done' },
    ] : [],
    saying: saying.join(' '),
  });

  // Next: the first two things somebody has to do, in the order they matter.
  const verbs = { raised: (c) => (c.pickedBy ? 'decide' : 'take on'), decided: () => 'schedule',
    scheduled: () => 'mark done, when it is fixed,' };
  const steps = f.filter(([, x]) => x.active).sort(([a], [b]) => byUrgency(a, b)).slice(0, 2);
  const nextNode = el('span');
  steps.forEach(([c, x], i) => {
    const verb = verbs[x.stage](c);
    nextNode.append(i ? `, then ${verb} ` : `${verb[0].toUpperCase()}${verb.slice(1)} `, crLink(c));
  });
  if (steps.length) nextNode.append('.');
  next($('cr-next'), steps.length ? nextNode : null);
}

/**
 * The page's one picture: every request on its way from raised to done, one
 * mark each, coloured by how it is doing. A strip rather than a chart, because
 * the question is "where is each one and which are stuck", and a count per
 * column would answer only the first half.
 */
function drawFlow(rows) {
  const box = $('cr-flow');
  box.replaceChildren();
  if (!rows.length) { box.hidden = true; return; }
  box.hidden = false;
  const since = releasedAt();
  const tag = state.release?.to?.tag;
  const f = rows.map((c) => [c, facts(c)]);
  const doneAll = f.filter(([, x]) => x.stage === 'done');
  const doneNow = doneAll.filter(([c]) => !since || Date.parse(c.resolvedAt) > since);
  const columns = [
    ['raised', 'Raised', 'open: being taken on and decided', f.filter(([, x]) => x.stage === 'raised')],
    ['decided', 'Accepted', 'waiting for a ticket or a comment', f.filter(([, x]) => x.stage === 'decided')],
    ['scheduled', 'Scheduled', 'a ticket carries the fix', f.filter(([, x]) => x.stage === 'scheduled')],
    ['done', tag && since ? `Done since ${tag}` : 'Done', 'the package is fixed', doneNow],
  ];

  box.append(el('figcaption', 'sh-figure-caption', 'Where every request is, oldest at the top of each step. Open one to act on it.'));
  const strip = el('ol', 'cr-flow-strip');
  for (const [key, label, hint, list] of columns) {
    const col = el('li', `cr-flow-col is-${key}`);
    const head = el('div', 'cr-flow-head');
    head.append(el('span', 'cr-flow-count', fmt(list.length)), el('span', 'cr-flow-label', label));
    head.title = hint;
    const marks = el('div', 'cr-flow-marks');
    const sorted = [...list].sort(([a], [b]) => Date.parse(a.raisedAt) - Date.parse(b.raisedAt));
    for (const [c, x] of sorted) {
      const mark = crLink(c, c.id.replace(/^CR-0*/, ''), `cr-mark sh-fill-${x.tone}${x.blocking ? ' is-blocking' : ''}`);
      mark.title = `${c.id}: ${c.title}. ${x.word}${x.waiting !== null ? `, waiting ${days(x.waiting)}` : ''}${x.blocking ? ', blocks work' : ''}.`;
      mark.setAttribute('aria-label', mark.title);
      marks.append(mark);
    }
    if (!list.length) marks.append(el('span', 'cr-flow-none', 'none'));
    col.append(head, marks);
    strip.append(col);
  }
  box.append(strip);

  const earlier = doneAll.length - doneNow.length;
  const rejected = f.filter(([, x]) => x.stage === 'rejected').length;
  const aside = [earlier ? `${fmt(earlier)} done before ${tag}` : '', rejected ? `${fmt(rejected)} rejected` : '']
    .filter(Boolean).join(' · ');
  if (aside) box.append(el('p', 'cr-flow-aside', `Off the strip: ${aside}.`));

  box.append(legend([
    { kind: 'late', label: `Nobody on it for over ${days(state.afterDays)}` },
    { kind: 'fresh', label: 'New, nobody on it yet' },
    { kind: 'going', label: 'Somebody has it' },
    { kind: 'stalled', label: 'Accepted, waiting to be scheduled' },
    { kind: 'done', label: 'Done' },
  ], 'cr-flow-legend'));
  const ring = el('p', 'cr-flow-ring');
  ring.append(el('span', 'cr-ring-key', ''), 'A ring means it blocks work.');
  ring.firstChild.setAttribute('aria-hidden', 'true');
  box.append(ring);

  // The strip's twin: the same marks as a table, for a screen reader and for
  // copying, out of sight.
  const twin = el('table', 'sh-sr');
  twin.append(el('caption', '', 'Every request by step'));
  const head = el('tr');
  for (const h of ['Request', 'Step', 'State', 'Waiting', 'Blocks work']) { const th = el('th', '', h); th.scope = 'col'; head.append(th); }
  const thead = el('thead'); thead.append(head);
  const tbody = el('tbody');
  for (const [, label, , list] of columns) {
    for (const [c, x] of list) {
      const tr = el('tr');
      for (const v of [`${c.id} ${c.title}`, label, x.word, x.waiting !== null ? days(x.waiting) : '', x.blocking ? 'yes' : '']) tr.append(el('td', '', v));
      tbody.append(tr);
    }
  }
  twin.append(thead, tbody);
  box.append(twin);
}

// ── the tables ──────────────────────────────────────────────────────

const SECTIONS = {
  decide: {
    rows: (c, x) => x.open,
    empty: 'Nothing is waiting for a decision. Raise one from the rail if you found the package wrong.',
    note: () => `Open requests, most urgent first: blocking work, then those nobody has taken on for more than ${days(state.afterDays)}, then the oldest. Open one to read it and act on it.`,
  },
  untaken: {
    rows: (c, x) => x.untaken,
    empty: 'Every open request has somebody on it.',
    note: () => `Open requests nobody has said they are dealing with. After ${days(state.afterDays)} each one is escalated to the admins; the team lead whose side and platform it is should take it on.`,
    holder: 'should',
  },
  unscheduled: {
    rows: (c, x) => x.stage === 'decided',
    empty: 'Every accepted request is scheduled.',
    note: () => 'Accepted, so the package is wrong, but nothing in OpenProject carries the fix yet. '
      + 'Decided 14 October: when the ticket it came out of is closed, the fix gets a new ticket under it; '
      + 'when that ticket is still open, it gets a comment instead, which the developer\'s AI agent reads on its next pull. '
      + 'Accepting does this by itself; this list is what it could not do.',
  },
  fixing: {
    rows: (c, x) => x.stage === 'scheduled',
    empty: 'Nothing is scheduled as a ticket right now.',
    note: () => 'Accepted and filed as a ticket in OpenProject. Mark each one done when the package has been fixed, and say which release or commit fixed it.',
  },
  all: {
    rows: () => true,
    empty: 'No change requests in this project yet.',
    note: () => 'Every request the filter shows, whatever its state. The CSV holds exactly these rows; an admin can fill in its decision column and upload it to settle many at once.',
  },
};

/** The section a request belongs in, so a link to it opens where it can be acted on. */
function homeOf(c) {
  const x = facts(c);
  return x.open ? 'decide' : x.stage === 'decided' ? 'unscheduled' : x.stage === 'scheduled' ? 'fixing' : 'all';
}

function ticketCell(c) {
  const box = el('span', 'cr-tickets');
  if (c.ticket) box.append(opLink(c.ticket, c.ticketUrl, `Ticket #${c.ticket} in OpenProject, which ${c.id} was raised from`));
  if (c.childTicket) {
    if (c.ticket) box.append(el('span', 'sh-quiet', 'filed as'));
    box.append(opLink(c.childTicket, c.childUrl, `Ticket #${c.childTicket} in OpenProject, filed for ${c.id}`));
  }
  if (!c.ticket && !c.childTicket) box.append(el('span', 'sh-quiet', 'none'));
  return box;
}

function opLink(key, url, title) {
  if (!url) return el('span', 'sh-key', `#${key}`);
  const a = el('a', 'sh-key', `#${key}`);
  a.href = url;
  a.target = '_blank';
  a.rel = 'noopener';
  a.title = `${title} (opens in a new tab)`;
  return a;
}

function drawTable(name) {
  const def = SECTIONS[name];
  const host = $(`cr-t-${name}`);
  if (!host) return;
  const rows = shown().filter((c) => def.rows(c, facts(c))).sort(byUrgency);
  // A request named in the address is shown in its section even when the
  // filter would hide it, and says so: a link somebody was sent has to open.
  const named = state.items.find((c) => c.id === state.open);
  if (named && !rows.includes(named) && def.rows(named, facts(named))) rows.unshift(named);
  $(`cr-${name}-note`).textContent = def.note();

  const columns = [
    ['Request', 'cr-c-req'],
    ['Side', 'cr-c-side'],
    ['Raised by', 'cr-c-raised'],
    [def.holder === 'should' ? 'Should take it on' : 'Holder', 'cr-c-holder'],
    ['Ticket', 'cr-c-ticket'],
    ['Waiting', 'cr-c-wait is-num'],
    ['State', 'cr-c-state'],
    ['Next', 'cr-c-next'],
  ];
  const wrap = el('div', 'sh-table-wrap');
  const table = el('table', 'sh-table cr-table');
  const thead = el('thead');
  const hr = el('tr');
  for (const [label, cls] of columns) { const th = el('th', cls, label); th.scope = 'col'; hr.append(th); }
  thead.append(hr);
  const tbody = el('tbody');
  table.append(thead, tbody);
  wrap.append(table);

  if (!rows.length) {
    const tr = el('tr');
    const td = el('td', 'sh-empty', state.items.length && narrowed()
      ? `${def.empty.replace(/\.$/, '')} under this filter. "Show everything" above lifts it.`
      : def.empty);
    td.colSpan = columns.length;
    tr.append(td);
    tbody.append(tr);
  }
  for (const c of rows) {
    const x = facts(c);
    // Drawn in the section on screen only: every section is in the page at
    // once, and the same request open in two would repeat its field ids.
    const isOpen = c.id === state.open && name === state.section;
    const tr = el('tr', `cr-row${isOpen ? ' is-chosen' : ''}${x.late ? ' is-late' : ''}`);
    tr.dataset.crRow = c.id;

    const req = el('th', 'cr-c-req');
    req.scope = 'row';
    const toggle = el('button', 'cr-toggle');
    toggle.type = 'button';
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.setAttribute('aria-controls', `cr-d-${name}-${c.id}`);
    toggle.append(el('span', 'sh-key', c.id), el('span', 'cr-title', c.title));
    toggle.onclick = () => openCr(isOpen ? '' : c.id, { move: false });
    req.append(toggle);
    const meta = el('span', 'cr-meta');
    meta.append(el('code', '', `${KINDS[c.target.kind] ?? c.target.kind} ${c.target.id}`));
    if (x.blocking) meta.append(el('span', 'cr-blocks', 'Blocks work'));
    req.append(meta);

    const side = el('td', 'cr-c-side');
    side.append(c.tag ? el('span', 'sh-side', slice(c)) : el('span', 'cr-unrouted', 'Nobody has said'));

    const raised = el('td', 'cr-c-raised');
    raised.append(personLink(c.raisedBy), el('span', 'cr-sub', `${ago(c.raisedAt)}${c.raisedVia === 'claude' ? ', via Claude' : ''}`));

    const holder = el('td', 'cr-c-holder');
    if (def.holder === 'should') {
      const who = state.overdue.get(c.id)?.shouldBe ?? [];
      if (who.length) who.forEach((p, i) => { if (i) holder.append(', '); holder.append(personLink(p.name)); });
      else holder.append(el('span', 'sh-quiet', c.tag ? `a lead on ${slice(c)}` : 'nobody owns it yet'));
    } else holder.append(personLink(c.pickedBy));

    const ticket = el('td', 'cr-c-ticket');
    ticket.append(ticketCell(c));

    const wait = el('td', `cr-c-wait is-num${x.late ? ' is-late' : ''}`, x.waiting !== null ? days(x.waiting) : '');
    if (x.late) wait.title = `Nobody has taken it on, past the ${days(state.afterDays)}`;

    const st = el('td', 'cr-c-state');
    st.append(badge(x.tone, x.word));

    const nx = nextCell(c, x.stage);

    tr.append(req, side, raised, holder, ticket, wait, st, nx);
    tbody.append(tr);

    if (isOpen) {
      const dr = el('tr', 'cr-detail-row');
      const td = el('td');
      td.colSpan = columns.length;
      td.id = `cr-d-${name}-${c.id}`;
      if (!inScope(c)) td.append(el('p', 'cr-flash', 'Shown because the address names it; the filter above would hide it.'));
      td.append(detail(c));
      dr.append(td);
      tbody.append(dr);
    }
  }
  host.replaceChildren(wrap);
}

function drawCounts() {
  for (const name of ['decide', 'untaken', 'unscheduled', 'fixing']) {
    const n = shown().filter((c) => SECTIONS[name].rows(c, facts(c))).length;
    const node = $(`cr-n-${name}`);
    node.textContent = n ? String(n) : '';
    node.setAttribute('aria-label', n ? `${n}` : '');
  }
}

// ── one request, in full ────────────────────────────────────────────

function part(label, content, pre = false) {
  if (!content || (Array.isArray(content) && !content.length)) return null;
  const box = el('div', 'cr-d-part');
  box.append(el('h4', 'cr-d-label', label));
  if (Array.isArray(content)) {
    const list = el('ol', 'cr-options');
    for (const o of content) list.append(el('li', '', o));
    box.append(list);
  } else box.append(el(pre ? 'pre' : 'p', pre ? 'cr-pre' : 'cr-text', content));
  return box;
}

function fact(dl, term, value) {
  if (value === null || value === undefined || value === '') return;
  dl.append(el('dt', '', term));
  const dd = el('dd');
  if (value instanceof Node) dd.append(value); else dd.append(String(value));
  dl.append(dd);
}

function detail(c) {
  const x = facts(c);
  const box = el('div', 'cr-detail');
  const said = state.said.get(c.id);
  if (said) box.append(el('p', `cr-flash${said.bad ? ' is-bad' : ''}`, said.text));

  const grid = el('div', 'cr-d-grid');
  const main = el('div', 'cr-d-main');
  for (const p of [
    part('Problem', c.problem),
    part('What was seen', c.evidence, true),
    part('Options', c.options ?? []),
    part('Recommended', c.recommendation),
  ]) if (p) main.append(p);
  if (c.resolvedAt && c.status !== 'open') {
    const settled = el('div', 'cr-d-part');
    const h = el('h4', 'cr-d-label', `${CHANGE_STATUS_LABEL[c.status] ?? 'Settled'} by `);
    h.append(personLink(c.resolvedBy), `, ${ago(c.resolvedAt)}`);
    settled.append(h, el('p', 'cr-text', c.resolution || 'No note was given.'));
    if (c.resolvedRef) settled.append(el('p', 'cr-sub', `Fixed by ${c.resolvedRef}`));
    main.append(settled);
  }

  const aside = el('aside', 'cr-d-facts');
  aside.setAttribute('aria-label', `About ${c.id}`);
  const dl = el('dl', 'cr-dl');
  fact(dl, 'About', `${KINDS[c.target.kind] ?? c.target.kind} ${c.target.id}`);
  fact(dl, 'Side', c.tag ? slice(c) : 'Nobody has said, so no lead owns it');
  const raised = el('span');
  raised.append(personLink(c.raisedBy), `, ${ago(c.raisedAt)}${c.raisedVia === 'claude' ? ', through Claude' : ''}`);
  fact(dl, 'Raised by', raised);
  if (c.ticket) {
    const t = el('span');
    t.append(opLink(c.ticket, c.ticketUrl, `Ticket #${c.ticket}`), el('span', 'cr-sub', ' ', ));
    t.lastChild.dataset.sourceOf = c.id;
    fact(dl, 'Raised from', t);
  }
  if (c.childTicket) fact(dl, 'Filed as', opLink(c.childTicket, c.childUrl, `Ticket #${c.childTicket}`));
  if (c.pickedBy) {
    const p = el('span');
    p.append(personLink(c.pickedBy), `, ${ago(c.pickedAt)}`);
    fact(dl, 'Taken on by', p);
  }
  fact(dl, 'Against release', c.raisedTag);
  aside.append(dl, intake(c));
  grid.append(main, aside);
  box.append(grid, actions(c, x));
  return box;
}

// Intake (C8): where it came from, what kind of change, what it costs. Read
// by everybody; completed or corrected by whoever settles the request, or by
// the person who raised it while it is still open - the service's rule.
const SOURCE_LABEL = { minutes: 'Meeting minutes', answer: 'An answer to a question', design: 'A design board',
  developer: 'A developer, while building', audit: 'An audit' };
const TRIAGE_LABEL = { clarification: 'Clarification', scope: 'Change of scope', defect: 'Defect' };
const IMPACT_LABEL = { none: 'None', additive: 'Additive (compatible)', breaking: 'Breaking' };

function intake(c) {
  const box = el('div', 'cr-intake');
  const may = c.maySettle || (mine(c.raisedBy) && c.status === 'open');
  const head = el('div', 'cr-intake-head');
  head.append(el('h4', 'cr-d-label', 'Intake'));
  box.append(head);
  const dl = el('dl', 'cr-dl');
  fact(dl, 'Source', c.source ? `${SOURCE_LABEL[c.source] ?? c.source}${c.sourceRef ? `: ${c.sourceRef}` : ''}` : '');
  fact(dl, 'Triage', c.triage ? `${TRIAGE_LABEL[c.triage] ?? c.triage}${c.when ? `, ${c.when}` : ''}` : '');
  fact(dl, 'Contract impact', c.contractImpact ? IMPACT_LABEL[c.contractImpact] ?? c.contractImpact : '');
  fact(dl, 'Approved by', c.approver);
  fact(dl, 'Effort change', c.effortPoints != null ? `${c.effortPoints > 0 ? '+' : ''}${c.effortPoints} points` : '');
  fact(dl, 'Client sign-off', c.clientSignoff);
  fact(dl, 'Also touches', c.artefacts?.length ? c.artefacts.join(', ') : '');
  if (!dl.children.length) box.append(el('p', 'sh-quiet', may ? 'Not filled in yet.' : 'Not filled in.'));
  else box.append(dl);
  if (!may) return box;

  const edit = el('button', 'chip cr-quiet', 'Edit the intake');
  edit.type = 'button';
  head.append(edit);
  edit.onclick = () => {
    edit.hidden = true;
    const form = el('form', 'cr-intake-form');
    const pick = (label, key, options, value) => {
      const l = el('label', 'cr-field', label);
      const s = el('select', 'scope-select');
      s.name = key;
      s.append(new Option('Not said', ''));
      for (const [v, t] of Object.entries(options)) s.append(new Option(t, v));
      s.value = value ?? '';
      l.append(s);
      return l;
    };
    const text = (label, key, value, attrs = {}) => {
      const l = el('label', 'cr-field', label);
      const i = el('input', 'sh-input');
      i.name = key;
      i.value = value ?? '';
      Object.assign(i, attrs);
      l.append(i);
      return l;
    };
    form.append(
      pick('Source', 'source', SOURCE_LABEL, c.source),
      text('Where it is recorded', 'source_ref', c.sourceRef, { maxLength: 300 }),
      pick('Triage', 'triage', TRIAGE_LABEL, c.triage),
      pick('When', 'when', { now: 'Now', later: 'Later' }, c.when),
      pick('Contract impact', 'contract_impact', IMPACT_LABEL, c.contractImpact),
      text('Approved by', 'approver', c.approver, { maxLength: 200 }),
      text('Effort change, in points', 'effort_points', c.effortPoints ?? '', { inputMode: 'decimal' }),
      text('Client sign-off', 'client_signoff', c.clientSignoff, { maxLength: 300 }),
      text('Also touches, comma separated', 'artefacts', (c.artefacts ?? []).join(', ')),
    );
    const err = el('p', 'auth-error');
    err.hidden = true;
    err.setAttribute('role', 'alert');
    const save = el('button', 'auth-button cr-primary', 'Save the intake');
    save.type = 'submit';
    const cancel = el('button', 'chip', 'Cancel');
    cancel.type = 'button';
    cancel.onclick = () => { form.remove(); edit.hidden = false; };
    const bar = el('div', 'cr-buttons');
    bar.append(save, cancel);
    form.append(err, bar);
    form.onsubmit = async (e) => {
      e.preventDefault();
      const v = Object.fromEntries(new FormData(form));
      const effort = String(v.effort_points ?? '').trim();
      save.disabled = true;
      try {
        await auth.changeIntake(state.project, c.id, {
          source: v.source, source_ref: v.source_ref, triage: v.triage, when: v.when,
          contract_impact: v.contract_impact, approver: v.approver, client_signoff: v.client_signoff,
          artefacts: String(v.artefacts ?? '').split(',').map((s) => s.trim()).filter(Boolean),
          ...(effort ? { effort_points: Number(effort) } : { clear_effort: true }),
        });
        state.said.set(c.id, { text: 'The intake is saved.' });
        await reload();
      } catch (error) {
        err.textContent = `Not saved: ${error.message}`;
        err.hidden = false;
        save.disabled = false;
      }
    };
    box.append(form);
    form.querySelector('select')?.focus();
  };
  return box;
}

// ── acting on it ────────────────────────────────────────────────────

/** What OpenProject says about the ticket this request tells. Asked once. */
function source(c) {
  if (!state.sources.has(c.id)) {
    state.sources.set(c.id, auth.changeSource(state.project, c.id)
      .catch((error) => ({ read: false, why: error.message })));
  }
  return state.sources.get(c.id);
}

/** "#6046 (In progress)" beside the ticket in the facts list, once it is known. */
function fillSourceFacts(c, info) {
  const slot = document.querySelector(`[data-source-of="${c.id}"]`);
  if (slot && info.read && info.key === c.ticket) {
    slot.textContent = ` ${info.statusName}${info.closed && !/closed/i.test(info.statusName) ? ', a closing status' : ''}`;
  }
}

/** What settling it this way would do in OpenProject, as a sentence. */
function consequence(c, info, status) {
  const plan = info?.onSettle?.[status];
  if (!info) return '';
  if (!plan) return info.why ? `OpenProject could not be read (${info.why}), so its ticket may not be told.` : '';
  const key = plan.key ? `#${plan.key}` : '';
  if (plan.action === 'comment') {
    return info.told?.includes(status)
      ? `${key} already carries this decision as a comment, so nothing more is sent.`
      : `This adds a comment to ${key}${info.statusName ? ` (${info.statusName})` : ''} for the developer's AI agent, which reads it on its next pull.`;
  }
  if (plan.action === 'ticket') return `${key} is closed, so this files a new ticket under it for the fix.`;
  if (!c.ticket && !c.childTicket) return 'It was raised from no ticket, so nothing in OpenProject is told.';
  return info.read ? '' : `OpenProject could not be read (${info.why}), so its ticket may not be told.`;
}

function followUp(told) {
  if (!told) return '';
  const key = told.key ? `#${told.key}` : 'its ticket';
  if (told.action === 'comment' && told.ok) return told.already ? `${key} already had this as a comment.` : `Added a comment to ${key} for the developer's AI agent.`;
  if (told.action === 'ticket' && told.ok) return `${key} is closed, so a new ticket, #${told.ticket}, was filed under it.`;
  if (told.ok === false) return `${key} was not told: ${told.error}.`;
  return told.why && told.why !== 'tell_ticket was false' ? `No ticket was told: ${told.why}.` : '';
}

async function reload() {
  await load();
  draw();
}

function button(text, primary = false) {
  const b = el('button', primary ? 'auth-button cr-primary' : 'chip', text);
  b.type = 'button';
  return b;
}

/** Run an action on a request, then redraw it with what happened said at its top. */
async function act(c, run, done) {
  try {
    const answer = await run();
    state.sources.delete(c.id);
    state.said.set(c.id, { text: typeof done === 'function' ? done(answer) : done });
    state.drafts.delete(c.id);
    await load();
    // Followed to wherever it now belongs: accepting moves a request out of
    // "Needs a decision", and what the action did is said at its top there.
    openCr(c.id);
  } catch (error) {
    state.said.set(c.id, { text: `${c.id}: ${error.message}`, bad: true });
    draw();
  }
}

function noteField(c, { label, hint, required }) {
  const id = `cr-note-${c.id}`;
  const wrap = el('div', 'cr-field');
  const l = el('label', '', label);
  l.htmlFor = id;
  if (required) l.append(el('span', 'cr-req', ' (required)'));
  const area = el('textarea', 'sh-input cr-note');
  area.id = id;
  area.rows = 3;
  area.maxLength = 4000;
  area.value = state.drafts.get(c.id)?.note ?? '';
  if (required) { area.required = true; area.setAttribute('aria-required', 'true'); }
  const h = el('p', 'cr-hint', hint);
  h.id = `${id}-hint`;
  area.setAttribute('aria-describedby', h.id);
  area.oninput = () => state.drafts.set(c.id, { ...state.drafts.get(c.id), note: area.value });
  wrap.append(l, area, h);
  return { wrap, area };
}

function refField(c) {
  const id = `cr-ref-${c.id}`;
  const wrap = el('div', 'cr-field');
  const l = el('label', '', 'Fixed by');
  l.htmlFor = id;
  const input = el('input', 'sh-input');
  input.id = id;
  input.maxLength = 300;
  input.placeholder = 'r6, a commit, or a decision record';
  input.value = state.drafts.get(c.id)?.ref ?? c.resolvedRef ?? '';
  input.oninput = () => state.drafts.set(c.id, { ...state.drafts.get(c.id), ref: input.value });
  wrap.append(l, input);
  return { wrap, input };
}

/**
 * The action area: one primary button, the step this request's state allows
 * this reader, with what it will do said before it is pressed. Everything
 * else - handing it back, reopening it - is quieter, below.
 */
function actions(c, x) {
  const box = el('div', 'cr-act');
  box.append(el('h4', 'cr-d-label', 'What happens next'));
  const admin = auth.isAdmin(state.me);
  const holder = mine(c.pickedBy);
  const quiet = el('div', 'cr-quiet-row');

  if (x.open && x.untaken) {
    if (c.mayPick) {
      box.append(el('p', 'cr-say', 'Nobody has said they are dealing with this. Taking it on says you are; it does not decide it.'));
      const take = button('Take this on', true);
      take.onclick = () => { take.disabled = true; act(c, () => auth.pickChange(state.project, c.id), 'You have taken it on. Decide it below when you are ready.'); };
      box.append(take);
    } else {
      const who = state.overdue.get(c.id)?.shouldBe?.map((p) => p.name) ?? [];
      box.append(el('p', 'cr-say', c.tag
        ? `Waiting for a team lead on ${slice(c)} to take it on${who.length ? `: ${who.join(' or ')}` : ''}.`
        : 'Nobody has said which side this is, so no lead owns it. An admin can take it on, or set its side.'));
    }
    if (c.maySettle && !(mine(c.raisedBy) && !admin)) {
      const now = button('Decide it without taking it on');
      now.classList.add('cr-quiet');
      now.setAttribute('aria-expanded', 'false');
      const holderBox = el('div');
      now.onclick = () => {
        const opening = now.getAttribute('aria-expanded') !== 'true';
        now.setAttribute('aria-expanded', String(opening));
        holderBox.replaceChildren(...(opening ? [decideForm(c)] : []));
      };
      quiet.append(now);
      box.append(quiet, holderBox);
      return box;
    }
  } else if (x.open) {
    if (c.maySettle && !(mine(c.raisedBy) && !admin)) {
      box.append(decideForm(c));
    } else if (mine(c.raisedBy) && !admin) {
      box.append(el('p', 'cr-say', `${c.pickedBy} has it. You raised it, so somebody else accepts or rejects it.`));
    } else {
      box.append(el('p', 'cr-say', `${c.pickedBy} has it. A team lead on ${slice(c) || 'its side'}, a reviewer on the project or an admin decides it.`));
    }
  } else if (x.stage === 'decided') {
    box.append(scheduleArea(c));
  } else if (x.stage === 'scheduled') {
    if (c.maySettle) box.append(doneForm(c));
    else box.append(el('p', 'cr-say', `Scheduled as #${c.childTicket}. Whoever settles it marks it done when the package is fixed.`));
  } else {
    box.append(el('p', 'cr-say', x.stage === 'done'
      ? 'Done: the package has been fixed.'
      : 'Rejected: the package was right as it was.'));
  }

  if (c.pickedBy && x.open && (holder || admin)) {
    const back = button('Hand it back');
    back.classList.add('cr-quiet');
    back.onclick = () => act(c, () => auth.unpickChange(state.project, c.id), 'Handed back. It waits for somebody to take it on again.');
    quiet.append(back);
  }
  if (!x.open && c.maySettle) {
    const reopen = button('Reopen');
    reopen.classList.add('cr-quiet');
    reopen.onclick = async () => {
      const yes = await confirmStep(reopen, {
        say: `Reopen ${c.id}? Its decision is cleared and it waits for a decision again.`,
        action: 'Reopen it',
      });
      if (yes) act(c, () => auth.resolveChange(state.project, c.id, 'open', ''), 'Reopened. It waits for a decision again.');
    };
    quiet.append(reopen);
  }
  if (quiet.children.length) box.append(quiet);
  return box;
}

/** Accept or reject: the note is shown, and marked required, before either is pressed. */
function decideForm(c) {
  const form = el('div', 'cr-decide');
  const { wrap, area } = noteField(c, {
    label: 'What was decided',
    required: true,
    hint: 'The person who raised it reads this, and so does the developer\'s AI agent on the ticket.',
  });
  const effect = el('p', 'cr-effect');
  effect.setAttribute('aria-live', 'polite');
  effect.textContent = c.ticket || c.childTicket ? 'Reading what its ticket in OpenProject would be told…' : '';
  source(c).then((info) => {
    fillSourceFacts(c, info);
    const accept = consequence(c, info, 'accepted');
    const reject = consequence(c, info, 'rejected');
    effect.textContent = accept === reject || !reject
      ? accept
      : `If accepted: ${accept} If rejected: ${reject}`;
  });
  const err = el('p', 'auth-error');
  err.hidden = true;
  err.setAttribute('role', 'alert');
  const accept = button('Accept', true);
  const reject = button('Reject');
  reject.classList.add('cr-reject');
  const go = async (status) => {
    const note = area.value.trim();
    if (!note) {
      err.textContent = `Say what was decided first: it is what the person who raised ${c.id} reads, and what the agent builds to.`;
      err.hidden = false;
      area.setAttribute('aria-invalid', 'true');
      area.focus();
      return;
    }
    err.hidden = true;
    area.removeAttribute('aria-invalid');
    const info = await source(c);
    // After the row, not the button, so Accept and Reject stay side by side.
    const yes = await confirmStep(bar, {
      say: `${status === 'accepted' ? 'Accept' : 'Reject'} ${c.id}? ${consequence(c, info, status)}`.trim(),
      action: status === 'accepted' ? 'Accept it' : 'Reject it',
    });
    if (!yes) return;
    accept.disabled = reject.disabled = true;
    act(c, () => auth.resolveChange(state.project, c.id, status, note),
      (answer) => `${status === 'accepted' ? 'Accepted' : 'Rejected'}. ${followUp(answer?.ticketFollowUp)}`.trim());
  };
  const bar = el('div', 'cr-buttons');
  bar.append(accept, reject);
  accept.onclick = () => go('accepted');
  reject.onclick = () => go('rejected');
  form.append(wrap, effect, err, bar);
  return form;
}

/** Mark done: say what fixed it. */
function doneForm(c) {
  const form = el('div', 'cr-decide');
  const { wrap: refWrap, input } = refField(c);
  const { wrap, area } = noteField(c, {
    label: 'Anything to add',
    required: false,
    hint: 'Left empty, the decision note stays as it is.',
  });
  const effect = el('p', 'cr-effect');
  effect.setAttribute('aria-live', 'polite');
  source(c).then((info) => { fillSourceFacts(c, info); effect.textContent = consequence(c, info, 'done'); });
  const doneB = button('Mark done', true);
  doneB.onclick = async () => {
    const info = await source(c);
    const yes = await confirmStep(doneB, {
      say: `Mark ${c.id} done${input.value.trim() ? `, fixed by ${input.value.trim()}` : ''}? ${consequence(c, info, 'done')}`.trim(),
      action: 'Mark it done',
    });
    if (!yes) return;
    doneB.disabled = true;
    act(c, () => auth.resolveChange(state.project, c.id, 'done', area.value.trim(), input.value.trim()),
      (answer) => `Done. ${followUp(answer?.ticketFollowUp)}`.trim());
  };
  const bar = el('div', 'cr-buttons');
  bar.append(doneB);
  form.append(refWrap, wrap, effect, bar);
  return form;
}

/**
 * Accepted and not scheduled: the 14 October rule decides what the one button
 * is. The ticket it came out of is closed (or there is none): make a ticket.
 * It is open and has not been told: add the comment. It is open and has been
 * told: the agent has it, and what is left is marking it done.
 */
function scheduleArea(c) {
  const box = el('div', 'cr-schedule');
  const may = c.mayFileTicket || c.maySettle;
  if (!may) {
    box.append(el('p', 'cr-say', 'Accepted. Whoever settles it, or whoever took it on, schedules it.'));
    return box;
  }
  const say = el('p', 'cr-say', c.ticket ? `Reading #${c.ticket} in OpenProject…` : '');
  const slot = el('div');
  box.append(say, slot);
  const ticketPath = (why) => {
    say.textContent = why;
    if (c.mayFileTicket) slot.replaceChildren(ticketing(c));
    else slot.replaceChildren(el('p', 'cr-say', 'Whoever settles it, or whoever took it on, files the ticket.'));
  };
  if (!c.ticket) {
    ticketPath(`${c.id} was raised from no ticket, so the fix needs a ticket of its own.`);
    return box;
  }
  source(c).then((info) => {
    fillSourceFacts(c, info);
    const plan = info.onSettle?.accepted;
    if (!info.read) {
      ticketPath(`#${c.ticket} could not be read from OpenProject (${info.why}). A ticket can still be made; the preview says what would be created.`);
    } else if (plan?.action === 'ticket') {
      ticketPath(`#${c.ticket} is closed, so the fix is new work: it gets a ticket of its own under #${c.ticket}.`);
    } else if (info.told?.includes('accepted')) {
      say.textContent = `#${c.ticket} is open and already carries this decision as a comment. The developer's AI agent reads it on its next pull.`;
      slot.replaceChildren(c.maySettle ? doneForm(c) : el('p', 'cr-say', 'Whoever settles it marks it done when the package is fixed.'));
    } else {
      say.textContent = `#${c.ticket} is still open (${info.statusName}), so the decision goes on it as a comment for the developer's AI agent rather than on a new ticket.`;
      slot.replaceChildren(commenting(c, info));
    }
  });
  return box;
}

/** The comment a settled request owes its open ticket: preview, then post. */
function commenting(c, info) {
  const wrap = el('div', 'cr-ticketing');
  const open = button(`Add a comment to #${info.key}`, true);
  const panel = el('div', 'cr-preview');
  panel.hidden = true;
  wrap.append(open, panel);
  open.onclick = async () => {
    open.disabled = true;
    panel.hidden = false;
    panel.replaceChildren(el('p', 'cr-hint', 'Writing the comment…'));
    let plan;
    try {
      plan = await auth.previewChangeComment(state.project, c.id);
    } catch (error) {
      panel.replaceChildren(el('p', 'auth-error', `${error.message}`));
      open.disabled = false;
      return;
    }
    panel.replaceChildren();
    const lead = el('p', 'cr-say');
    lead.append(`This is what `, opLink(plan.key, plan.url, `Ticket #${plan.key}`), ' will say, for the agent that pulls it:');
    panel.append(lead, el('pre', 'cr-preview-body', plan.text));
    const post = button('Post it', true);
    const stop = button('Cancel');
    stop.onclick = () => { panel.hidden = true; open.disabled = false; };
    post.onclick = () => {
      post.disabled = stop.disabled = true;
      act(c, () => auth.applyChangeComment(state.project, c.id, plan.proposal),
        (answer) => (answer?.already ? `#${answer.key} already had this decision as a comment.` : `Posted on #${answer?.key ?? plan.key}. The developer's AI agent reads it on its next pull.`));
    };
    const bar = el('div', 'cr-buttons');
    bar.append(post, stop);
    panel.append(bar, el('p', 'cr-hint', `Nothing has been posted yet. This preview lapses in ${plan.expiresInMinutes} minutes.`));
    post.focus();
  };
  return wrap;
}

/**
 * Turning the request into a ticket, under the ticket it came out of.
 *
 * **Preview then confirm, and the preview is the whole control.** Nothing is
 * sent when the button is pressed; the service works out exactly what it would
 * create and hands it back, and this draws it - the parent, the type, the
 * subject, the description in full. The second button is the one that writes.
 *
 * That is not ceremony. A ticket filed into the wrong project, or under no
 * parent, or with a subject somebody has to decode later, cannot be taken back
 * from here: OpenProject owns it the moment it exists. The cheapest place to
 * catch all three is a paragraph the person reads before saying yes.
 */
function ticketing(c) {
  const wrap = el('div', 'cr-ticketing');
  const open = button('Make a ticket', true);
  const panel = el('div', 'cr-preview');
  panel.hidden = true;
  wrap.append(open, panel);

  open.onclick = async () => {
    open.disabled = true;
    panel.hidden = false;
    panel.replaceChildren(el('p', 'cr-hint', 'Working out what this would create…'));
    let plan;
    try {
      plan = await auth.previewTicket(state.project, c.id);
    } catch (error) {
      panel.replaceChildren(el('p', 'auth-error', error.message));
      open.disabled = false;
      return;
    }
    panel.replaceChildren();

    const facts = el('dl', 'cr-dl');
    fact(facts, 'Project', plan.willCreate.project);
    fact(facts, 'Under', plan.willCreate.parent
      ? `#${plan.willCreate.parent.key} · ${plan.willCreate.parent.subject}`
      : 'nothing: this would be a top-level ticket');
    panel.append(facts);
    // The one case worth interrupting for. A top-level ticket is not what
    // "file it under the original" means, and it happens quietly whenever the
    // request was raised from the viewer rather than from a ticket.
    if (plan.topLevel) {
      panel.append(el('p', 'cr-warn', `${c.id} did not come from a ticket, so there is nothing to hang this `
        + 'under. It will sit at the top level of the project.'));
    }

    const subjectId = `cr-subject-${c.id}`;
    const subjectLabel = el('label', 'cr-field', 'Subject');
    subjectLabel.htmlFor = subjectId;
    const subject = el('input', 'sh-input');
    subject.id = subjectId;
    subject.value = plan.willCreate.subject;
    subject.maxLength = 255;
    subjectLabel.append(subject);

    const typeLabel = el('label', 'cr-field', 'Type');
    const type = el('select', 'scope-select');
    for (const kind of plan.types ?? []) {
      const option = new Option(kind.name, kind.id);
      option.selected = kind.name === plan.willCreate.type;
      type.append(option);
    }
    typeLabel.append(type);
    const row = el('div', 'cr-form-row');
    row.append(subjectLabel, typeLabel);
    subjectLabel.classList.add('cr-grow');
    panel.append(row);

    const text = el('details', 'cr-preview-text');
    text.append(el('summary', '', 'What the ticket will say'), el('pre', 'cr-preview-body', plan.willCreate.description));
    panel.append(text);

    const go = button('Create it', true);
    const stop = button('Cancel');
    stop.onclick = () => { panel.hidden = true; open.disabled = false; };
    go.onclick = () => {
      go.disabled = stop.disabled = true;
      act(c, async () => {
        // Re-previewed when either field was touched, so what is created is
        // what the person last saw rather than what the first preview held.
        // The service decides either way; this only spares them a refusal
        // they would not understand.
        let token = plan.proposal;
        if (subject.value.trim() !== plan.willCreate.subject
            || Number(type.value) !== (plan.types ?? []).find((k) => k.name === plan.willCreate.type)?.id) {
          token = (await auth.previewTicket(state.project, c.id, subject.value.trim(), Number(type.value))).proposal;
        }
        return auth.createTicket(state.project, c.id, token);
      }, (answer) => `Filed as #${answer?.ticket?.key}${answer?.how === 'linked' ? ', which already existed and is now linked' : ''}.`);
    };
    const bar = el('div', 'cr-buttons');
    bar.append(go, stop);
    panel.append(bar, el('p', 'cr-hint', `Nothing has been created yet. This preview lapses in ${plan.expiresInMinutes} minutes.`));
  };
  return wrap;
}

// ── changed this release ────────────────────────────────────────────

function settledTable(rows, caption, empty) {
  const wrap = el('div', 'sh-table-wrap');
  const t = el('table', 'sh-table cr-table');
  t.append(el('caption', '', caption));
  const hr = el('tr');
  for (const h of ['Request', 'Decision', 'Settled by', 'When', 'Fixed by']) { const th = el('th', '', h); th.scope = 'col'; hr.append(th); }
  const thead = el('thead'); thead.append(hr);
  const tbody = el('tbody');
  if (!rows.length) {
    const tr = el('tr'); const td = el('td', 'sh-empty', empty); td.colSpan = 5; tr.append(td); tbody.append(tr);
  }
  for (const c of rows) {
    const tr = el('tr');
    const th = el('th');
    th.scope = 'row';
    const local = state.items.find((i) => i.id === c.id) ?? c;
    th.append(crLink(local), el('span', 'cr-title cr-title-block', c.title));
    const decision = el('td');
    decision.append(badge(facts(local).tone, CHANGE_STATUS_LABEL[c.status] ?? c.status));
    if (c.resolution) decision.append(el('span', 'cr-sub cr-sub-block', c.resolution));
    const by = el('td'); by.append(personLink(c.resolvedBy));
    tr.append(th, decision, by, el('td', 'is-nowrap', ago(c.resolvedAt)), el('td', '', c.resolvedRef || ''));
    tbody.append(tr);
  }
  t.append(thead, tbody);
  wrap.append(t);
  return wrap;
}

function drawRelease() {
  const host = $('cr-release');
  const r = state.release;
  host.replaceChildren();
  if (!r) { host.append(el('p', 'sh-empty', 'Reading the release record…')); return; }
  const settled = (c) => ['accepted', 'done'].includes(c.status) && c.resolvedAt;
  if (r.error) {
    $('cr-release-note').textContent = r.error;
    host.append(settledTable(shown().filter(settled).sort((a, b) => Date.parse(b.resolvedAt) - Date.parse(a.resolvedAt)),
      'Accepted or done so far', 'Nothing has been accepted yet.'));
    return;
  }
  const tag = r.to.tag;
  const since = Date.parse(r.to.taggedAt);
  $('cr-release-note').textContent = `ADAM serves ${tag}, released ${ago(r.to.taggedAt)}. What was accepted or done since then goes into the next release; what was settled before it is in ${tag}.`;
  const next = shown().filter((c) => settled(c) && Date.parse(c.resolvedAt) > since)
    .sort((a, b) => Date.parse(b.resolvedAt) - Date.parse(a.resolvedAt));
  const inIt = r.items.filter((c) => inScope(state.items.find((i) => i.id === c.id) ?? c));

  const p1 = el('section', 'sh-part');
  p1.append(el('h3', 'sh-part-title', `Since ${tag}, for the next release`));
  p1.append(settledTable(next, `Settled after ${tag} was released`, `Nothing has been accepted or done since ${tag}.`));
  const p2 = el('section', 'sh-part');
  const head = el('div', 'sh-part-head');
  head.append(el('h3', 'sh-part-title', `In ${tag}`));
  if (r.markdown && r.items.length) {
    const copy = button('Copy the release note');
    const said = el('span', 'cr-hint');
    said.setAttribute('role', 'status');
    copy.onclick = async () => {
      try { await navigator.clipboard.writeText(r.markdown); said.textContent = 'Copied, as Markdown.'; } catch { said.textContent = 'This browser would not copy it; select the table instead.'; }
    };
    const tools = el('span', 'cr-all-actions');
    tools.append(copy, said);
    head.append(tools);
  }
  p2.append(head);
  p2.append(settledTable(inIt, `Settled ${r.from ? `after ${r.from.tag} and ` : ''}up to ${tag}`, `Nothing was settled in ${tag}.`));
  host.append(p1, p2);
}

// ── export ──────────────────────────────────────────────────────────

function exportCsv() {
  // Exactly the rows on screen, which is what makes "the CSV holds exactly
  // these rows" true. The columns, the labels and the quoting are not this
  // page's to decide: they are the file the service also writes and reads back,
  // and they live in change-csv.js so the two cannot drift apart.
  const rows = shown().sort(byUrgency);
  const url = URL.createObjectURL(new Blob([toChangeCsv(rows)], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  // "-filtered" whenever any part of the filter narrowed it, not only the three
  // the old page looked at: a file named as the whole register that holds one
  // platform's requests is a file somebody settles from by mistake.
  a.download = `${state.project}-change-requests${narrowed() ? '-filtered' : ''}-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// ── raising ─────────────────────────────────────────────────────────

function wireForm() {
  const form = $('cr-form');
  const kind = $('cr-f-kind');
  for (const [value, label] of Object.entries(KINDS)) kind.append(new Option(label, value));
  const err = $('cr-f-error');
  form.onreset = () => { err.hidden = true; };
  form.onsubmit = async (event) => {
    event.preventDefault();
    // The browser's own checks, said in this page's words rather than its
    // tooltip, which a screen reader announces poorly and a phone hides.
    const missing = [...form.querySelectorAll('[required]')].find((f) => !f.checkValidity());
    if (missing) {
      const name = missing.closest('label')?.firstChild?.textContent?.trim() ?? 'A field';
      err.textContent = `${name} is needed${missing.minLength > 0 ? ` (at least ${missing.minLength} characters)` : ''}.`;
      err.hidden = false;
      missing.focus();
      return;
    }
    const submit = form.querySelector('[type=submit]');
    submit.disabled = true;
    try {
      const made = await auth.raiseChange(state.project, {
        target_kind: kind.value,
        target_id: $('cr-f-target').value,
        title: $('cr-f-title').value,
        problem: $('cr-f-problem').value,
        evidence: $('cr-f-evidence').value,
        options: $('cr-f-options').value.split('\n').map((s) => s.trim()).filter(Boolean),
        recommendation: $('cr-f-recommendation').value,
        blocking: $('cr-f-blocking').checked,
        ticket: $('cr-f-ticket').value.trim(),
        tag: $('cr-f-tag').value,
        platform: $('cr-f-platform').value.trim(),
      });
      form.reset();
      await load();
      draw();
      const c = made.change;
      const box = $('cr-filed');
      box.replaceChildren();
      const p = el('p', 'cr-say');
      p.append(el('strong', '', `${c.id} is filed.`), ` "${c.title}" is open and waits for `
        + (c.tag ? `a team lead on ${slice(c)} to take it on.` : 'somebody to say which side it is.'));
      const go = el('p');
      const fresh = state.items.find((i) => i.id === c.id) ?? c;
      go.append(crLink(fresh, `Open ${c.id}`, 'sh-link'));
      box.append(p, go);
      box.hidden = false;
      box.tabIndex = -1;
      box.focus();
    } catch (error) {
      const message = Array.isArray(error.message) ? error.message.map((m) => m.msg ?? m).join('; ') : error.message;
      err.textContent = `Not raised: ${message}`;
      err.hidden = false;
    } finally {
      submit.disabled = false;
    }
  };
}

// ── drawing ─────────────────────────────────────────────────────────

function draw() {
  const rows = shown();
  $('cr-lede').textContent = state.items.length
    ? `${plural(state.items.length, 'change request')} in ${state.projectName || state.project || 'this project'}: places where the package was found wrong, contradictory or missing something a ticket needs.`
    : `No change requests in ${state.projectName || state.project || 'this project'} yet: places where the package was found wrong, contradictory or missing something a ticket needs.`;
  $('cr-asof').textContent = state.readAt ? `Read at ${state.readAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}` : '';
  drawVerdict(rows);
  drawFlow(rows);
  for (const name of Object.keys(SECTIONS)) drawTable(name);
  drawCounts();
  drawRelease();
  $('cr-all-note').textContent = SECTIONS.all.note();
}

/**
 * Open one request where it can be acted on: its section, its row expanded,
 * in view. `?cr=` follows, so the address is a link to send.
 */
function openCr(id, { move = true } = {}) {
  state.open = id || '';
  setParams({ cr: state.open });
  const c = state.items.find((i) => i.id === state.open);
  if (c && move && !SECTIONS[state.section]?.rows(c, facts(c))) showSection(homeOf(c));
  draw();
  if (!c) return;
  requestAnimationFrame(() => {
    const row = document.querySelector(`#${state.section} [data-cr-row="${c.id}"]`);
    row?.scrollIntoView({ block: 'start', behavior: 'smooth' });
    row?.querySelector('.cr-toggle')?.focus({ preventScroll: true });
  });
}

// ── start ───────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  state.project = await auth.ensureProject();
  state.projectName = state.project ?? '';
  state.open = param('cr').toUpperCase();

  const picker = $('cr-project');
  picker.onchange = () => {
    auth.rememberProject(picker.value);
    location.search = `?project=${encodeURIComponent(picker.value)}`;
  };

  $('cr-export').onclick = exportCsv;
  // Admin only, because /api/changes/import/* is. Hiding it is presentation -
  // the service refuses the upload to anybody else whatever this page draws.
  $('cr-settle-link').hidden = !auth.isAdmin(state.me);
  $('cr-refresh').onclick = async () => {
    $('cr-refresh').disabled = true;
    state.sources.clear();
    await Promise.all([load(), loadRelease()]);
    draw();
    $('cr-refresh').disabled = false;
  };
  wireForm();

  await Promise.all([load(firstList), loadRelease()]);
  // The projects this account may open, by name, for the switcher. After the
  // list, because the list is what says which project this is when neither
  // the address nor the last visit did.
  firstRegistry.then((registry) => {
    const names = Object.fromEntries((registry.projects ?? []).map((p) => [p.id, p.name || p.id]));
    state.projectName = names[state.project] ?? state.project ?? '';
    const mineOnly = (state.me?.projects ?? []).map((p) => p.id ?? p);
    for (const id of (mineOnly.length ? mineOnly : Object.keys(names))) {
      const o = new Option(names[id] ?? id, id);
      o.selected = id === state.project;
      picker.append(o);
    }
    // One project, or none listed: a picker with nothing to pick is a blank box.
    picker.hidden = picker.options.length < 2;
    draw();
  }).catch(() => { /* the page still works for the current project */ });
  mountFilter();
  // A link to one request opens on the section it can be acted on in, unless
  // the address already names a section it is in.
  const named = state.items.find((c) => c.id === state.open);
  if (named) {
    const want = location.hash.slice(1);
    if (!SECTIONS[want]?.rows(named, facts(named))) history.replaceState(null, '', `${location.pathname}${location.search}#${homeOf(named)}`);
  }
  showSection = mountPanels({
    nav: document.querySelector('#cr-page .set-nav'),
    fallback: 'decide',
    onShow: (name) => { state.section = name; draw(); },
  });
  draw();
  if (named) openCr(named.id, { move: false });
  hideLoader();
})();
