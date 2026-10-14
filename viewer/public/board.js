/**
 * My work: a developer's own tickets, and the testing gate standing in front
 * of them. Opened every morning to answer two questions — **what do I do next,
 * and am I about to hit the gate?** — so it opens on exactly that: where my
 * sprint stands, the next ticket in the build order, and the gate meter.
 *
 * **Everybody signed in gets this page and it is never anybody else's.** The
 * service answers `/api/board/mine` from the caller's own OpenProject token
 * with `assignee = me`, so there is no id to tamper with and no wider version
 * of this view to reach for. Where the delivery as a whole is read — Tasks —
 * is a different page with a different gate.
 *
 * **The same rules as Tasks, not a copy of them.** The six kinds of ticket,
 * the sprint calendar and the even pace come from ticket-kinds.js, which
 * Tasks reads too, so "6 of your 14 finished, 2 behind" here is the sentence
 * Tasks says about the same person. It used to sort by due date and
 * `percentDone` instead, which put a ticket waiting for QA under Overdue: the
 * developer had finished it, and the page told them they were late. Waiting
 * for QA is never late.
 *
 * The count is Tasks' too: tasks (OpenProject type Task, the unit the plan is
 * made of) or every ticket, under the same `?count=` and the same remembered
 * choice, so switching it on one page switches it on the other.
 *
 * The testing gate lives here as well. It shipped with the Claude connector as
 * its only interface, which meant somebody not using Claude Code could be
 * stopped from closing a ticket by a rule they had no way to satisfy.
 */
// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer.
import '/page-chrome.js';
import * as auth from '/validation.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, ago, daysSince, param, setParams, personHref, personLink,
  verdict, next, mountScope, legend, badge, table, confirmStep,
} from '/sheet.js';
import {
  today, asDate, addDays, learnStatuses, isDone, isAwaiting, isOpenWork, isStalled,
  kindOf, dueOn, isLate, isDueSoon, buildSprints, sprintOf, datedSprints, currentSprint,
  nextSprint, paceFor,
} from '/ticket-kinds.js';

// Both halves asked for at once, and before the sign-in check has answered
// rather than after it (13 October). They are independent of each other and
// of everything else the page does. Signed out, both come back 401 and are
// ignored: `requireSignIn` is already sending the reader to the door.
const firstProject = auth.ensureProject();
const firstBoard = firstProject.then((project) => auth.myBoard(project ?? ''));
const firstBatches = firstProject.then((project) => auth.listBatches(project ?? ''));
firstBoard.catch(() => { /* answered by load() */ });
firstBatches.catch(() => { /* answered by loadBatches() */ });

const $ = (id) => document.getElementById(id);

const state = {
  me: null,
  project: '',
  data: null,       // /api/board/mine
  all: [],          // every ticket of mine the page knows: open, finished this week, closed earlier
  batches: null,    // /api/test-batches
  readAt: null,
  queueLimit: 15,
  scope: null,      // mountScope's handle
};

// ── words ───────────────────────────────────────────────────────────

const unit = () => (state.scope?.state.count === 'tickets' ? 'tickets' : 'tasks');
const W1 = () => (unit() === 'tasks' ? 'task' : 'ticket');
const Ws = () => (unit() === 'tasks' ? 'tasks' : 'tickets');
const nu = (n) => plural(n, W1(), Ws());
const weekday = (d) => (d ? d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }) : '—');
const shortDay = (d) => (d ? d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) : '—');
const clockTime = (d) => d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
const KIND_WORD = { done: 'Closed', qa: 'Waiting for QA', going: 'In progress', stalled: 'On hold', fresh: 'Not started' };

function say(id, message) {
  $(id).textContent = message ?? '';
  $(id).hidden = !message;
}

/** A ticket's number, as a link to it in OpenProject. */
function keyLink(t) {
  const a = el('a', 'sh-key', `#${t.key}`);
  a.href = t.url || '#';
  a.target = '_blank';
  a.rel = 'noreferrer';
  a.title = `Open #${t.key} in OpenProject`;
  return a;
}

// ── what the page counts ────────────────────────────────────────────

/** Whether a ticket is counted in the unit, as Tasks decides it. */
const inUnit = (t) => unit() === 'tickets' || t.type === 'Task';
const sprintName = (t) => t.version || '(no sprint)';

/** Every ticket of mine in the unit, under the page's sprint and state filters. */
function scoped({ skipState = false } = {}) {
  const { sprint, kind } = state.scope?.state ?? {};
  return state.all.filter((t) => inUnit(t)
    && (!sprint || sprintName(t) === sprint)
    && (skipState || !kind || kindOf(t) === kind));
}

/** The sprint the opening is about: the one chosen in the filter, or the
 *  current one, or the first that has not started — Tasks' `focusSprint`. */
function focusSprint() {
  const chosen = state.scope?.state.sprint;
  if (chosen) { const s = sprintOf(chosen); return s?.start ? s : null; }
  return currentSprint() ?? datedSprints().find((s) => s.start > today()) ?? datedSprints().at(-1) ?? null;
}

const bySprintStart = (a, b) => (sprintOf(a)?.start ?? Infinity) - (sprintOf(b)?.start ?? Infinity) || a.localeCompare(b);

// ── the gate ────────────────────────────────────────────────────────

/** Where I stand on the gate: the batch from /api/test-batches when it came,
 *  or the board's summary of it when that is all there is. */
function myGate() {
  const every = state.batches?.every ?? state.data?.testing?.every ?? 10;
  const b = state.batches?.mine;
  if (b) return { every, closed: b.closed, full: b.full, submitted: !!b.submittedAt, verdict: b.verdict || '', note: b.checkerNote, by: b.checkedBy, submittedAt: b.submittedAt, tickets: b.tickets ?? [] };
  const t = state.data?.testing;
  if (t) return { every, closed: t.closed, full: t.full, submitted: t.submitted, verdict: t.verdict || '', note: t.checkerNote, tickets: [] };
  return { every, closed: 0, full: false, submitted: false, verdict: '', tickets: [] };
}

/** The same four states Tasks draws, and the same colour for each. */
function gateState(g) {
  if (g.verdict === 'failed') return { tone: 'bad', text: 'sent back' };
  if (g.submitted) return { tone: 'warn', text: 'waiting for a check' };
  if (g.full) return { tone: 'bad', text: 'full: test now' };
  return { tone: '', text: `${Math.max(0, g.every - g.closed)} to go` };
}

/** The sentence under the meter: what the gate will do, and what to do. */
function gateWords(g) {
  if (g.verdict === 'failed') {
    return `Sent back${g.by ? ` by ${g.by}` : ''}: ${g.note || 'no reason given'}. Deal with it and submit again; your next close is refused until a teammate passes it.`;
  }
  if (g.submitted) {
    return `Submitted ${ago(g.submittedAt) || 'already'}, waiting for a teammate to check it. Your next close is refused until they do, and it is not yours to wave through.`;
  }
  if (g.full) return 'Your next close is refused until you test this batch, submit what you ran, and a teammate passes it.';
  if (!g.closed) return `Nothing closed through ADAM since your last passed batch. Testing is due every ${g.every} tickets.`;
  const left = g.every - g.closed;
  return `${plural(left, 'more close', 'more closes')}, then test the batch and a teammate checks it before you close another. You can submit early.`;
}

/**
 * The gate meter, the one bold thing on the page: one cell per ticket the
 * gate allows, filled as they are closed. The colour says the state and the
 * words beside it say it again, with a legend and the tickets as a table for
 * anyone not reading the picture.
 */
function gateMeter(g) {
  const s = gateState(g);
  const wrap = el('div', 'bd-meter');
  const row = el('div', 'bd-meter-row');
  const cells = el('span', 'bd-cells');
  cells.setAttribute('role', 'img');
  cells.setAttribute('aria-label', `${g.closed} of ${g.every} tickets closed through ADAM: ${s.text}`);
  for (let i = 0; i < g.every; i += 1) {
    cells.append(el('span', `bd-cell${i < g.closed ? ` is-on${s.tone ? ` is-${s.tone}` : ''}` : ''}`));
  }
  const n = el('p', 'bd-meter-n');
  n.append(el('strong', '', String(g.closed)), ` of ${g.every}`);
  n.append(el('span', `bd-meter-state${s.tone ? ` is-${s.tone}` : ''}`, s.text));
  row.append(cells, n);
  wrap.append(row, el('p', 'bd-meter-say', gateWords(g)));
  const on = s.tone === 'bad' ? { kind: 'late', label: g.verdict === 'failed' ? 'Closed, sent back' : 'Closed, gate full' }
    : s.tone === 'warn' ? { kind: 'stalled', label: 'Closed, waiting for a check' }
      : { kind: 'done', label: 'Closed through ADAM' };
  wrap.append(legend([on, { kind: 'track', label: 'Still to go' }], 'bd-meter-key'));
  wrap.append(batchTable(g.tickets, { srOnly: true }));
  return wrap;
}

function batchTable(tickets, { srOnly = false } = {}) {
  return table({
    caption: srOnly ? 'The tickets in your current batch' : undefined,
    srOnly,
    columns: [
      { key: 'key', label: 'Ticket', render: (t) => (t.url ? keyLink(t) : `#${t.key}`), nowrap: true },
      { key: 'subject', label: 'Subject' },
      { key: 'closedAt', label: 'Closed through ADAM', nowrap: true, sort: (t) => t.closedAt ?? '',
        render: (t) => { const d = asDate(t.closedAt); return d ? `${shortDay(d)}, ${clockTime(d)}` : ''; } },
    ],
    rows: tickets,
    empty: 'Nothing in it yet.',
  });
}

// ── one ticket, as a line ───────────────────────────────────────────

/** What a ticket is part of, said quietly under its subject. */
function metaOf(t, { full = false } = {}) {
  const bits = [sprintName(t)];
  if (t.type) bits.push(t.type);
  if (full && t.priority && !/^normal$/i.test(t.priority)) bits.push(`${t.priority} priority`);
  if (t.parentSubject) bits.push(`under ${t.parentSubject}`);
  if (full && t.module?.subject && t.module.subject !== t.parentSubject) bits.push(`in ${t.module.subject}`);
  return bits.join(' · ');
}

function stateBadge(t) {
  const kind = kindOf(t);
  if (kind === 'rejected') return badge('quiet', t.status || 'Rejected');
  return badge(kind, t.status || KIND_WORD[kind]);
}

function line(t, right, { full = false, lead = null } = {}) {
  const li = el('li', `bd-line${lead != null ? ' has-lead' : ''}`);
  if (lead != null) li.append(lead);
  li.append(keyLink(t));
  const body = el('div', 'bd-body');
  const subject = el('span', 'bd-subject', t.subject || '—');
  subject.title = t.subject || '';
  body.append(subject, el('span', 'bd-meta', metaOf(t, { full })));
  li.append(body);
  const end = el('div', 'bd-end');
  for (const r of [].concat(right ?? [])) if (r) end.append(r);
  li.append(end);
  return li;
}

function list(host, rows, empty) {
  host.replaceChildren();
  if (!rows.length) { host.append(el('p', 'sh-empty', empty)); return; }
  const ul = el('ul', 'bd-list');
  ul.append(...rows);
  host.append(ul);
}

// ── this week: the opening ──────────────────────────────────────────

const TONE = { ok: ['ok', 'On pace'], warn: ['warn', 'A little behind'], bad: ['bad', 'Behind pace'] };

function drawWeek() {
  const root = $('bd-verdict');
  const focus = focusSprint();
  const mine = state.all.filter(inUnit);
  const g = myGate();

  if (!state.all.length) {
    verdict(root, {
      headline: 'Nothing in OpenProject is yours yet.',
      pace: state.data?.note ?? 'When a ticket is assigned to you it appears here, in the order the plan builds it.',
    });
  } else if (!focus) {
    const open = mine.filter(isOpenWork).length;
    verdict(root, {
      headline: `${nu(open)} open, none in a dated sprint.`,
      pace: `Your ${Ws()} name no sprint with dates, so there is no pace to hold them against.`,
    });
  } else {
    const items = mine.filter((t) => t.version === focus.name);
    const range = `${weekday(focus.start)} to ${weekday(focus.end)}`;
    const p = items.length ? paceFor(focus, items) : null;
    const when = [el('strong', '', focus.name), range];
    if (p?.k.phase === 'running' && p.k.dayNo) when.push(el('span', 'bd-day', `day ${p.k.dayNo} of ${p.k.n}`));
    if (!p || !p.c.live) {
      verdict(root, {
        when,
        headline: `Nothing of yours is planned in ${focus.name}.`,
        pace: nextSprint(focus) ? `${nextSprint(focus).name} starts ${weekday(nextSprint(focus).start)}.` : '',
      });
    } else {
      const { c, k } = p;
      let headline = `${fmt(c.finished)} of your ${nu(c.live)} finished`;
      if (k.phase === 'running' && c.finished >= c.live) headline = `All ${nu(c.live)} of yours in it finished.`;
      else if (k.phase === 'running') headline += p.behind ? `, ${fmt(p.behind)} behind an even pace.` : ', on an even pace.';
      else if (k.phase === 'ahead') headline += `; it starts ${weekday(focus.start)}.`;
      else headline += c.finished >= c.live ? '. It has ended.' : `. It ended with ${fmt(c.open)} still open.`;
      let pill = TONE[p.tone] ? { tone: TONE[p.tone][0], text: TONE[p.tone][1] } : null;
      if (k.phase === 'over') pill = c.finished >= c.live ? { tone: 'ok', text: 'Ended' } : { tone: 'bad', text: 'Ended unfinished' };

      const pace = [];
      if (k.phase === 'running') {
        const gone = k.dayNo ? `by the end of today, day ${k.dayNo} of ${k.n}` : `after ${k.through} of ${k.n} working days`;
        pace.push(`An even pace would have ${nu(p.expected)} of yours finished ${gone}.`);
        if (c.finished && k.through) {
          pace.push(`At your rate about ${nu(Math.min(c.live, Math.round((c.finished / k.through) * k.n)))} will be finished by ${weekday(focus.end)}.`);
        }
        pace.push(k.left ? `${plural(k.left, 'working day', 'working days')} left after today.` : 'Today is its last working day.');
      } else if (k.phase === 'ahead') {
        pace.push(`${plural(k.n, 'working day', 'working days')} long.`);
      }

      const said = [];
      if (c.qa) said.push(`Waiting for QA counts as finished: you are done with ${c.qa === 1 ? 'it' : 'those'}.`);
      if (!c.going && c.fresh && k.phase === 'running') said.push(`Nothing of yours in it is marked In progress.`);
      if (c.rejected) said.push(`${plural(c.rejected, `${W1()} was`, `${Ws()} were`)} rejected and ${c.rejected === 1 ? 'is' : 'are'} not counted.`);

      verdict(root, {
        when,
        headline,
        headlineId: 'bd-headline',
        pill,
        pace: pace.join(' '),
        ledger: [
          { label: `Planned ${Ws()}`, value: c.live },
          { label: 'Closed', value: c.done, swatch: 'done' },
          { label: 'Waiting for QA', value: c.qa, swatch: 'qa' },
          { label: 'In progress', value: c.going, swatch: 'going' },
          { label: 'On hold', value: c.stalled, swatch: 'stalled' },
          { label: 'Not started', value: c.fresh, swatch: 'fresh' },
          { label: 'Late', value: c.late, bad: true, title: 'Open, and past its own date or its sprint’s end' },
        ].filter((item) => item.value || item.label.startsWith('Planned')),
        saying: said.join(' '),
      });
    }
  }
  // `verdict` replaces the headline; keep the id the section is labelled by.
  root.querySelector('.sh-headline')?.setAttribute('id', 'bd-headline');

  // The bold thing: the gate, beside the verdict.
  $('bd-gate-figure').hidden = false;
  $('bd-gate-hero').replaceChildren(gateMeter(g));

  drawNextLine(g);
  drawDue();
}

/** The first ticket you can work on now: open, not on hold, and not held by
 *  an open blocking change request — in the service's build order. */
const workable = () => state.all.filter((t) => inUnit(t) && isOpenWork(t) && !isStalled(t) && !(t.blockedBy ?? []).length)
  .sort((a, b) => (a.position ?? Infinity) - (b.position ?? Infinity));

function drawNextLine(g) {
  const s = gateState(g);
  const parts = [];
  if (s.tone === 'bad') {
    const go = el('a', '', g.verdict === 'failed' ? 'deal with what was sent back' : 'test your batch and submit it');
    go.href = '#gate';
    parts.push(go, g.verdict === 'failed'
      ? '. Closing is refused until a teammate passes it again.'
      : `. Closing is refused until a teammate passes it: ${g.closed} of ${g.every}.`);
  } else {
    const first = workable()[0];
    if (first) {
      parts.push(keyLink(first), ' ', el('strong', '', first.subject || ''), `, ${sprintName(first)}`);
      if (first.parentSubject) parts.push(`, under ${first.parentSubject}`);
      parts.push('. ');
    } else {
      parts.push(`Nothing of yours is ready to start: everything open is on hold or blocked. Ask your lead for the next ${W1()}. `);
    }
    parts.push(g.submitted && g.full
      ? `Testing gate ${g.closed} of ${g.every}, waiting for a check: build it, but closing waits until a teammate passes your batch.`
      : g.submitted ? `Testing gate ${g.closed} of ${g.every}, waiting for a check.` : `Testing gate ${g.closed} of ${g.every}.`);
  }
  next($('bd-next'), parts);
}

function drawDue() {
  const rows = scoped({ skipState: true })
    .filter((t) => isLate(t) || isDueSoon(t))
    .sort((a, b) => (dueOn(a) ?? 0) - (dueOn(b) ?? 0));
  list($('bd-due'), rows.map((t) => {
    const d = dueOn(t);
    const own = !!t.dueDate;
    const late = isLate(t);
    // Late is said in words with the late mark, beside the ticket's own state
    // rather than instead of it: an On hold ticket past its date is both.
    const when = el('span', `bd-when${late ? ' is-late' : ''}`,
      `${late ? 'late, was due' : 'due'} ${weekday(d)}${own ? '' : ', when its sprint ends'}`);
    return line(t, [stateBadge(t), when]);
  }), `Nothing of yours is late or due in the next seven days.`);
}

// ── next up ─────────────────────────────────────────────────────────

function drawQueue() {
  const rows = scoped().filter(isOpenWork).sort((a, b) => (a.position ?? Infinity) - (b.position ?? Infinity));
  const served = state.data?.release?.tag;
  $('bd-next-note').textContent = rows.length
    ? `${nu(rows.length)} open, in the order the plan builds them: what you have started first, then the plan’s build order, a sub-task straight after its parent. The number is the place in that order, which is the order “my next 15” pulls in Claude Code.`
    + (served ? ` ADAM is serving release ${served}.` : '')
    : '';
  const shown = rows.slice(0, state.queueLimit);
  const ol = $('bd-queue');
  ol.replaceChildren(...shown.map((t) => {
    const right = [];
    for (const cr of t.blockedBy ?? []) {
      const a = el('a', 'sh-badge sh-badge-stalled bd-cr', `Blocked by ${cr.id}`);
      a.href = '/changes.html';
      a.title = cr.title ?? '';
      right.push(a);
    }
    right.push(stateBadge(t));
    if (isLate(t)) right.push(badge('late', 'Late'));
    if (t.pinStale) right.push(el('span', 'bd-pin is-stale', `Pulled at ${t.pin}: pull again, ${served} is served`));
    else if (t.pin) right.push(el('span', 'bd-pin', `Pulled at ${t.pin}`));
    const lead = el('span', 'bd-pos', String(t.position ?? ''));
    lead.title = `Place ${t.position} in the build order`;
    return line(t, right, { full: true, lead });
  }));
  if (!rows.length) {
    ol.replaceChildren(el('li', 'sh-empty', state.all.length
      ? 'Nothing open matches the filter. Show everything to see the rest.'
      : 'Nothing open is assigned to you. When a ticket is, it appears here in build order.'));
  }
  const more = $('bd-queue-more');
  const left = rows.length - shown.length;
  more.hidden = left <= 0;
  more.textContent = `Show ${fmt(Math.min(left, 30))} more of ${fmt(left)}`;
}

// ── waiting for QA, finished ────────────────────────────────────────

function drawQa() {
  const rows = scoped().filter(isAwaiting).sort((a, b) => (asDate(a.updatedAt) ?? 0) - (asDate(b.updatedAt) ?? 0));
  $('bd-qa-title').textContent = rows.length ? `Waiting for QA: ${nu(rows.length)}` : 'Waiting for QA';
  list($('bd-qa'), rows.map((t) => {
    const d = daysSince(t.updatedAt);
    return line(t, [stateBadge(t), el('span', 'bd-when', d == null ? '' : d === 0 ? 'since today' : `waiting ${plural(d, 'day', 'days')}`)]);
  }), `Nothing of yours is waiting for QA. When you move a finished ${W1()} to QA it waits here, and it is never late.`);
}

function drawFinished() {
  const closes = state.data?.closes ?? {};
  const weekAgo = addDays(today(), -7);
  const rows = scoped().filter((t) => isDone(t) && (asDate(closes[t.key] ?? t.updatedAt) ?? 0) >= weekAgo)
    .sort((a, b) => (asDate(closes[b.key] ?? b.updatedAt) ?? 0) - (asDate(closes[a.key] ?? a.updatedAt) ?? 0));
  const earlier = scoped().filter(isDone).length - rows.length;
  const throughAdam = rows.filter((t) => closes[t.key]).length;
  $('bd-done-title').textContent = rows.length ? `Finished this week: ${nu(rows.length)}` : 'Finished this week';
  $('bd-done-note').textContent = 'Closed in the last seven days. '
    + (rows.length && throughAdam < rows.length
      ? 'Where a close went through ADAM the date is when it was closed; otherwise OpenProject has no closing date, so it is the ticket’s last change, which a later comment can move. '
      : '')
    + (earlier > 0 ? `${nu(earlier)} of yours ${earlier === 1 ? 'was' : 'were'} closed before that.` : '');
  list($('bd-done'), rows.map((t) => {
    // No state badge: every row here is closed, and a column of the same word
    // is a column nobody reads. The date says which kind of date it is.
    const at = closes[t.key];
    const w = el('span', 'bd-when', at ? `closed ${ago(at)}` : `last changed ${ago(t.updatedAt)}`);
    w.title = at ? `Closed through ADAM, ${asDate(at).toLocaleString('en-GB')}`
      : 'Closed outside ADAM: OpenProject gives no closing date, so this is the ticket’s last change.';
    return line(t, [w]);
  }), `Nothing of yours was closed in the last seven days. What you finish and QA closes lands here.`);
}

// ── everything I hold ───────────────────────────────────────────────

let allTable = null;
function drawAll() {
  const rows = scoped().filter((t) => !isDone(t) && kindOf(t) !== 'rejected');
  $('bd-all-title').textContent = rows.length ? `Everything I hold: ${nu(rows.length)}` : 'Everything I hold';
  $('bd-all-note').textContent = `Every open ${W1()} assigned to you across the plan, in build order. Sort by any column. ${unit() === 'tasks' ? 'Sub-tasks and features are left out while the page counts tasks.' : ''}`;
  if (!allTable) {
    allTable = table({
      columns: [
        { key: 'position', label: 'Order', num: true, sort: (t) => t.position ?? Infinity },
        { key: 'key', label: 'Ticket', nowrap: true, render: keyLink, sort: (t) => Number(t.key) },
        { key: 'subject', label: 'Subject', sort: (t) => (t.subject || '').toLowerCase() },
        { key: 'state', label: 'State', render: stateBadge, sort: (t) => ['going', 'fresh', 'stalled', 'qa'].indexOf(kindOf(t)) },
        { key: 'sprint', label: 'Sprint', nowrap: true, render: sprintName, sort: (t) => sprintOf(t.version)?.start ?? new Date(8.64e15) },
        { key: 'type', label: 'Type', nowrap: true, sort: (t) => t.type || '' },
        { key: 'due', label: 'Due', nowrap: true, render: (t) => shortDay(dueOn(t)), sort: (t) => dueOn(t) ?? new Date(8.64e15),
          cellClass: (t) => (isLate(t) ? 'is-late' : '') },
        { key: 'module', label: 'Module', render: (t) => t.module?.subject ?? '', sort: (t) => t.module?.subject ?? '' },
      ],
      rows: [],
      empty: 'Nothing open matches the filter.',
      sortBy: { key: 'position', dir: 1 },
    });
    $('bd-all').replaceChildren(allTable);
  }
  allTable.redraw(rows);
  $('bd-note').textContent = state.data?.note ?? '';
}

// ── testing ─────────────────────────────────────────────────────────

function drawGateSection() {
  const g = myGate();
  const every = g.every;
  $('bd-gate-lede').textContent = `Every ${every} tickets you close through ADAM, the next close is refused until you have tested that batch and somebody else has passed it. You cannot check your own: that is the whole of what it is for. A ticket closed in OpenProject itself is not counted.`;
  const host = $('bd-batch');
  host.replaceChildren(gateMeter(g));
  const mine = state.batches?.mine;
  if (mine?.tickets?.length) {
    host.append(el('h3', 'sh-part-title bd-sub', `In this batch: ${plural(mine.tickets.length, 'ticket', 'tickets')}`), batchTable(mine.tickets));
  }
  if (mine?.notes) {
    host.append(el('h3', 'sh-part-title bd-sub', mine.verdict === 'failed' ? 'What you submitted' : 'What you ran'), el('pre', 'bd-notes', mine.notes));
    if (mine.evidence) host.append(el('pre', 'bd-notes bd-evidence', mine.evidence));
  }
  // Offered once there is something in the batch, not only once it is full:
  // testing eight and saying so is better than waiting to be stopped at ten.
  const form = $('bd-submit');
  form.hidden = !mine || !mine.closed || mine.verdict === 'passed';
  form.querySelector('h3').textContent = mine?.submittedAt && mine.verdict !== 'failed'
    ? 'Change what you submitted' : 'Submit this batch for checking';
  $('bd-submit-go').textContent = mine?.verdict === 'failed' ? 'Submit again' : mine?.submittedAt ? 'Submit the change' : 'Submit for checking';

  const past = state.batches?.past ?? [];
  $('bd-past').replaceChildren(past.length ? table({
    columns: [
      { key: 'openedAt', label: 'Opened', nowrap: true, render: (b) => shortDay(asDate(b.openedAt)), sort: (b) => b.openedAt },
      { key: 'closed', label: 'Tickets', num: true },
      { key: 'checkedBy', label: 'Passed by', render: (b) => (b.checkedBy ? personLink(b.checkedBy) : '') },
      { key: 'checkedAt', label: 'Passed', nowrap: true, render: (b) => shortDay(asDate(b.checkedAt)), sort: (b) => b.checkedAt ?? '' },
      { key: 'checkerNote', label: 'Their note', render: (b) => b.checkerNote || '' },
    ],
    rows: past,
  }) : el('p', 'sh-empty', 'No batch of yours has passed yet. When one does it is kept here, with who checked it.'));
}

function drawChecking() {
  const waiting = state.batches?.waiting ?? [];
  $('bd-nav-check').textContent = waiting.length ? String(waiting.length) : '';
  const box = $('bd-waiting');
  box.replaceChildren();
  if (!waiting.length) {
    box.append(el('p', 'sh-empty', 'Nothing is waiting for you to check. When a teammate submits a batch it appears here, with its tickets.'));
    return;
  }
  for (const b of waiting) box.append(waitingBatch(b));
}

function waitingBatch(b) {
  const name = b.who?.name ?? 'A teammate';
  const part = el('section', 'sh-part bd-check');
  const head = el('h3', 'sh-part-title');
  head.append(personLink(name), `’s batch of ${plural(b.closed, 'ticket', 'tickets')}`);
  part.append(head, el('p', 'sh-note', `Submitted ${ago(b.submittedAt) || ''}${b.openedAt ? `, opened ${shortDay(asDate(b.openedAt))}` : ''}. Open each ticket in OpenProject before you decide.`));
  part.append(batchTable(b.tickets ?? []));
  part.append(el('h4', 'bd-label', 'What they ran'), el('pre', 'bd-notes', b.notes || '—'));
  if (b.evidence) part.append(el('h4', 'bd-label', 'Output they kept'), el('pre', 'bd-notes bd-evidence', b.evidence));

  const id = `bd-reason-${b.id}`;
  const label = el('label', 'bd-field-label', 'Reason, needed to send it back');
  label.htmlFor = id;
  const note = el('input', 'auth-input bd-reason');
  note.id = id;
  note.type = 'text';
  note.maxLength = 2000;
  const bar = el('div', 'set-actions bd-decide');
  const pass = el('button', 'chip bd-pass', 'Mark passed');
  pass.type = 'button';
  const back = el('button', 'chip bd-fail', 'Send it back');
  back.type = 'button';
  bar.append(pass, back);
  // The error beside the buttons that caused it, not at the top of a section
  // the reader has scrolled away from.
  const problem = el('p', 'auth-error bd-check-error');
  problem.setAttribute('role', 'alert');
  problem.hidden = true;
  const tell = (text) => { problem.textContent = text; problem.hidden = !text; };

  // Both are a second press: passing opens their gate and cannot be taken
  // back; sending back keeps it shut until they submit again.
  const decide = async (verdictWord) => {
    tell('');
    if (verdictWord === 'failed' && !note.value.trim()) {
      tell(`Say why you are sending ${name}'s batch back: they need to know what to fix.`);
      note.focus();
      return;
    }
    const ok = await confirmStep(bar, verdictWord === 'passed'
      ? { say: `Pass ${name}'s batch? Their gate opens and they can close tickets again. This cannot be undone.`, action: 'Mark passed' }
      : { say: `Send ${name}'s batch back? Their gate stays shut until they submit again.`, action: 'Send it back' });
    if (!ok) return;
    pass.disabled = back.disabled = true;
    try {
      await auth.checkBatch(b.id, verdictWord, note.value.trim());
      await loadBatches();
    } catch (error) {
      pass.disabled = back.disabled = false;
      tell(`Could not record that: ${error.message} Nothing was changed; try again.`);
    }
  };
  pass.onclick = () => decide('passed');
  back.onclick = () => decide('failed');
  part.append(label, note, bar, problem);
  return part;
}

// ── the filter and the opening line ─────────────────────────────────

function mountFilter() {
  // ?count= wins, then the reader's last choice on Tasks or here (one key for
  // both pages), then tasks.
  if (!param('count')) {
    let saved = '';
    try { saved = localStorage.getItem('adam-tasks-count') ?? ''; } catch { /* storage denied */ }
    if (saved === 'tickets') setParams({ count: 'tickets' });
  }
  state.scope = mountScope({
    root: $('bd-scope'),
    fields: [
      { key: 'count', label: 'Count', kind: 'switch', sticky: true, options: [['tasks', 'Tasks'], ['tickets', 'Tickets']] },
      { key: 'sprint', label: 'Sprint', all: 'Every sprint',
        options: () => [...new Set(state.all.filter(inUnit).map(sprintName))].sort(bySprintStart).map((s) => [s, s]) },
      { key: 'kind', label: 'State', all: 'Every state',
        options: [['going', 'In progress'], ['fresh', 'Not started'], ['stalled', 'On hold'], ['qa', 'Waiting for QA'], ['done', 'Closed']] },
    ],
    says: saysLine,
    onChange: (s) => {
      try { localStorage.setItem('adam-tasks-count', s.count === 'tickets' ? 'tickets' : 'tasks'); } catch { /* storage denied */ }
      state.queueLimit = 15;
      drawAll_();
    },
  });
}

function saysLine(s) {
  if (!state.data) return '';
  const all = state.all.filter(inUnit);
  const shown = scoped();
  const bits = [];
  if (s.sprint) bits.push(`in ${s.sprint}`);
  if (s.kind) bits.push(KIND_WORD[s.kind].toLowerCase());
  const hidden = unit() === 'tasks' ? state.all.length - all.length : 0;
  let line = bits.length
    ? `Every section shows ${fmt(shown.length)} of your ${nu(all.length)}: ${bits.join(', ')}.`
    : `Every section shows all ${nu(all.length)} of yours: open, waiting for QA and closed.`;
  if (s.kind) line += ' The opening still counts the whole sprint.';
  if (hidden) line += ` ${plural(hidden, 'sub-task or feature', 'sub-tasks and features')} left out; count tickets to see them.`;
  return line;
}

function drawLede() {
  const d = state.data;
  const lede = $('bd-lede');
  lede.replaceChildren();
  if (!d) return;
  const op = d.openproject ?? {};
  const where = op.url ? Object.assign(el('a', '', op.name || op.identifier), { href: op.url, target: '_blank', rel: 'noreferrer' }) : (op.name || 'OpenProject');
  lede.append(`Yours in `, where, d.assignee ? `, as ${d.assignee} in OpenProject.` : '.',
    d.modulesKnown === false ? ' The project tree is still being read, so modules and sprint dates may be missing; Refresh in a minute.' : '');
  $('bd-asof').textContent = state.readAt ? `Read at ${clockTime(state.readAt)}` : '';
  const who = d.assignee || state.me?.name || '';
  $('bd-tasks-link').href = who ? personHref(who) : '/tasks.html#person';
}

function drawAll_() {
  state.scope?.redraw();
  drawLede();
  drawWeek();
  drawQueue();
  drawQa();
  drawFinished();
  drawAll();
  drawGateSection();
  drawChecking();
}

// ── loading ─────────────────────────────────────────────────────────

/** Everything of mine the board sent, once each: closed earlier (the shared
 *  project read), finished this week and open (both live, so they win). */
function absorb(data) {
  // The instance's statuses, or — when the project read could not be had —
  // what the two live lists say: the open list is open, the finished one closed.
  const statuses = data.statuses?.length ? data.statuses : [
    ...[...new Set((data.items ?? []).map((t) => t.status))].map((name) => ({ name, isClosed: false })),
    ...[...new Set((data.finished ?? []).map((t) => t.status))].map((name) => ({ name, isClosed: true })),
  ];
  learnStatuses(statuses);
  const byKey = new Map();
  for (const t of [...(data.closedEarlier ?? []), ...(data.finished ?? []), ...(data.items ?? [])]) byKey.set(t.key, t);
  state.all = [...byKey.values()];
  buildSprints(data.versions, state.all);
}

async function loadBatches(answer = null) {
  say('bd-batch-error', '');
  try {
    state.batches = await (answer ?? auth.listBatches(state.project));
  } catch (error) {
    if (error.status !== 428) say('bd-batch-error', `Could not read the testing gate: ${error.message} Press Refresh to try again.`);
  }
  if (state.data) { drawWeek(); drawGateSection(); }
  drawChecking();
}

async function load(answer = null) {
  say('bd-error', '');
  try {
    state.data = await (answer ?? auth.myBoard(state.project));
    state.readAt = new Date();
  } catch (error) {
    // 428 is "OpenProject is not connected", which is a setup step rather than
    // a failure, and it has its own panel saying which half is missing.
    if (error.status === 428) {
      $('board').hidden = true;
      $('unconnected').hidden = false;
      $('unconnected-why').textContent = error.message;
      return;
    }
    // Anything else is said where it can be seen: above every section, with
    // the page around it, and the last tickets read (if any) left in place.
    say('bd-error', `Could not read your tickets: ${error.message} Press Refresh to try again.`);
    if (!state.data) {
      verdict($('bd-verdict'), { headline: 'Your tickets could not be read.', pace: 'The reason is above. Nothing on this page is out of date; it is empty.' });
    }
    return;
  }
  $('unconnected').hidden = true;
  $('board').hidden = false;
  absorb(state.data);
  drawAll_();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  state.project = (await firstProject) ?? '';

  // The same project picker as Tasks: shown only when there is a choice.
  auth.listProjects().then(({ projects }) => {
    const mine = projects.filter((p) => !state.me.projects?.length || state.me.projects.includes(p.id));
    const picker = $('bd-project');
    picker.replaceChildren(...mine.map((p) => {
      const option = el('option', '', p.name || p.id);
      option.value = p.id;
      option.selected = p.id === state.project;
      return option;
    }));
    picker.onchange = () => {
      auth.rememberProject(picker.value);
      location.search = `?project=${encodeURIComponent(picker.value)}`;
    };
    $('bd-project-wrap').hidden = picker.options.length < 2;
  }).catch(() => { /* the page still works for the current project */ });

  mountFilter();
  mountPanels({ nav: document.querySelector('#board .set-nav'), fallback: 'week' });

  $('bd-queue-more').onclick = () => { state.queueLimit += 30; drawQueue(); };
  $('bd-refresh').onclick = async () => {
    const button = $('bd-refresh');
    button.disabled = true;
    button.textContent = 'Reading…';
    await Promise.all([load(), loadBatches()]);
    button.disabled = false;
    button.textContent = 'Refresh';
  };

  $('bd-submit').onsubmit = async (event) => {
    event.preventDefault();
    say('bd-batch-error', '');
    $('bd-submit-says').textContent = '';
    const go = $('bd-submit-go');
    go.disabled = true;
    try {
      await auth.submitBatch(state.batches.mine.id, $('bd-notes').value, $('bd-evidence').value);
      $('bd-notes').value = '';
      $('bd-evidence').value = '';
      $('bd-submit-says').textContent = 'Submitted. A teammate has to check it before you close another.';
      await Promise.all([loadBatches(), load()]);
    } catch (error) {
      say('bd-batch-error', `Not submitted: ${error.message}`);
    } finally {
      go.disabled = false;
    }
  };

  await load(firstBoard);
  await loadBatches(firstBatches);
  // The browser scrolls to the element the hash names once the page has grown
  // tall enough to, which is after the tickets are drawn; the rail shows that
  // section on its own, so the right place to be is its top.
  requestAnimationFrame(() => scrollTo({ top: 0 }));
})();
