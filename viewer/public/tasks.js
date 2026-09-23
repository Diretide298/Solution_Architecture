/**
 * The delivery overview: every ticket in the project's OpenProject project, in
 * every state, for an admin.
 *
 * The viewer already answers "what am I holding" — `adam_board` in Claude Code,
 * one person, open work only. This is the other question, the one asked in a
 * status meeting: where is the delivery, who is holding what, what is late, what
 * is finished, and which parts of the package nobody has a ticket for. That
 * needs the closed and the rejected tickets too, which is why it is a separate
 * route (`/api/board/overview`) and not the board with a wider filter.
 *
 * **Every state name comes from OpenProject.** ADAM keeps no list of statuses:
 * the service hands back the instance's own, each with its `isClosed` flag, and
 * "finished" here means exactly that flag. A team that renames "Closed" to
 * "Shipped" keeps its numbers. The one guess this page makes is which open
 * states mean *stopped* rather than *going* — a name containing "hold",
 * "block" or "wait" — and it is only ever used to colour and to count a
 * "stalled" figure that the States section shows in full underneath.
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
import { followSections } from '/sections.js';

const $ = (id) => document.getElementById(id);
const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const state = {
  me: null,
  project: '',
  data: null,
  closedByName: new Map(),   // status name -> isClosed, from OpenProject
  filter: { text: '', status: '', person: '', openOnly: false },
  // The timeline's own switch, kept out of `filter` because that one drives
  // the ticket list at the bottom and these are different questions.
  ganttOpenOnly: false,
};

// Open states that mean the work has stopped. A guess, and the only one on the
// page: OpenProject has no "blocked" flag, so the name is all there is.
const STALLED = /hold|block|wait|pend/i;

const DAY = 86_400_000;
const today = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const asDate = (iso) => { const d = iso ? new Date(iso) : null; return d && !Number.isNaN(+d) ? d : null; };
const days = (from, to) => Math.round((to - from) / DAY);
const fmtDay = (iso) => {
  const d = asDate(iso);
  return d ? d.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : '—';
};
const fmtWhen = (iso) => {
  const d = asDate(iso);
  return d ? d.toLocaleString(undefined, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—';
};
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;

// ── what a ticket is ────────────────────────────────────────────────
//
// Every question the page asks about one ticket, asked once here so the
// sections cannot disagree about what "done" or "late" means.

const isDone = (t) => state.closedByName.get(t.status) === true;
const isStalled = (t) => !isDone(t) && STALLED.test(t.status || '');
const dueOn = (t) => asDate(t.dueDate);
const isOverdue = (t) => { const d = dueOn(t); return !isDone(t) && d != null && d < today(); };
const isDueSoon = (t) => {
  const d = dueOn(t);
  return !isDone(t) && d != null && d >= today() && d <= new Date(+today() + 7 * DAY);
};
// A closed ticket's last change is the closest thing to a closing date this API
// offers without reading every activity, so it is what "closed this week" means.
const closedAt = (t) => (isDone(t) ? asDate(t.updatedAt) : null);
const who = (t) => t.assignee || 'Nobody';

// ── reading ─────────────────────────────────────────────────────────

async function load({ refresh = false } = {}) {
  $('tk-error').hidden = true;
  if (refresh) $('tk-asof').textContent = 'Reading OpenProject…';
  try {
    const data = await auth.boardOverview(state.project, { refresh });
    state.data = data;
    state.closedByName = new Map((data.statuses ?? []).map((s) => [s.name, !!s.isClosed]));
    draw();
  } catch (error) {
    // 428 is the service saying the token or the project link is missing. It is
    // not an error the reader can do anything about here, so it gets the panel
    // that says which of the two and where to fix it, not a red line.
    if (error.status === 428) return needsSetup(error.message);
    if (error.status === 403) return denied();
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
  const items = state.data.items ?? [];
  drawLede();
  drawStats(items);
  drawStates(items);
  drawPeople(items);
  drawDates(items);
  drawTimeline(items);
  drawDeliverables(items);
  drawParents(items);
  drawThroughput(items);
  drawFilters(items);
  drawList();
}

function drawLede() {
  const d = state.data;
  const op = d.openproject ?? {};
  const lede = $('tk-lede');
  lede.replaceChildren(
    `${plural(d.total ?? 0, 'ticket', 'tickets')} in `,
    op.url ? Object.assign(el('a', null, op.name || op.identifier), { href: op.url, target: '_blank', rel: 'noreferrer' })
           : el('span', null, op.name || op.identifier || 'OpenProject'),
    d.truncated ? ' — the newest of a larger project; older tickets are not counted.' : '.',
  );
  const age = d.ageSeconds ?? 0;
  $('tk-asof').textContent = d.fromCache
    ? `Read ${age < 60 ? 'less than a minute' : plural(Math.round(age / 60), 'minute', 'minutes')} ago. Refresh for the live numbers.`
    : `Read just now, ${fmtWhen(d.asOf)}.`;
  $('tk-asof').dataset.tone = '';
}

function statCard(value, label, hint) {
  const card = el('div', 'stat-card');
  card.append(el('div', 'stat-value', String(value)), el('div', 'stat-label', label));
  if (hint) card.append(el('div', 'stat-hint', hint));
  return card;
}

function drawStats(items) {
  const done = items.filter(isDone);
  const open = items.filter((t) => !isDone(t));
  const stalled = open.filter(isStalled);
  const overdue = items.filter(isOverdue);
  const soon = items.filter(isDueSoon);
  const share = items.length ? Math.round((done.length / items.length) * 100) : 0;

  const weekAgo = new Date(+today() - 7 * DAY);
  const lastWeek = done.filter((t) => { const c = closedAt(t); return c && c >= weekAgo; });
  const median = medianDaysToClose(done);

  const strip = $('tk-stats');
  strip.replaceChildren(
    statCard(items.length, 'Tickets', 'every state'),
    statCard(`${share}%`, 'Finished', `${done.length} of ${items.length}`),
    statCard(open.length - stalled.length, 'In flight', 'open and moving'),
    statCard(stalled.length, 'Stalled', 'on hold, blocked or waiting'),
    statCard(overdue.length, 'Overdue', 'open, past the due date'),
    statCard(soon.length, 'Due this week', 'the next seven days'),
    statCard(lastWeek.length, 'Closed this week', 'in the last seven days'),
    statCard(median == null ? '—' : median, 'Days to close',
      median == null ? 'nothing closed yet' : 'median, opened to closed'),
  );
  // Only the two that mean somebody has to do something get a colour.
  strip.children[4].classList.toggle('stat-bad', overdue.length > 0);
  strip.children[3].classList.toggle('stat-warn', stalled.length > 0);
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

/** A row of `.admin-row`, with a bar showing its share of the biggest count. */
function barRow(label, count, biggest, tone, extra) {
  const row = el('div', 'admin-row tk-bar-row');
  row.append(el('span', 'tk-bar-label', label));
  const track = el('span', 'tk-bar');
  const fill = el('span', `tk-bar-fill${tone ? ` tk-bar-${tone}` : ''}`);
  fill.style.width = `${biggest ? Math.max(2, Math.round((count / biggest) * 100)) : 0}%`;
  track.append(fill);
  row.append(track, el('span', 'tk-bar-count', String(count)), el('span', 'tk-bar-extra', extra ?? ''));
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
    const closed = state.closedByName.get(name) === true;
    const tone = closed ? 'done' : STALLED.test(name) ? 'warn' : 'open';
    return barRow(name, n, biggest, tone, closed ? 'finished' : '');
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'No tickets to count.'));
  $('tk-states-count').textContent = `${rows.length} in use`;
}

function drawPeople(items) {
  const people = new Map();
  for (const t of items) {
    const name = who(t);
    const row = people.get(name) ?? { name, open: 0, stalled: 0, overdue: 0, done: 0 };
    if (isDone(t)) row.done += 1; else row.open += 1;
    if (isStalled(t)) row.stalled += 1;
    if (isOverdue(t)) row.overdue += 1;
    people.set(name, row);
  }
  const rows = [...people.values()].sort((a, b) => b.open - a.open || a.name.localeCompare(b.name));
  const biggest = Math.max(1, ...rows.map((r) => r.open));
  const box = $('tk-people');
  box.replaceChildren(...rows.map((r) => {
    const parts = [];
    if (r.overdue) parts.push(`${r.overdue} overdue`);
    if (r.stalled) parts.push(`${r.stalled} stalled`);
    if (r.done) parts.push(`${r.done} finished`);
    const row = barRow(r.name, r.open, biggest, r.overdue ? 'bad' : 'open', parts.join(' · '));
    row.classList.add('people-row');
    return row;
  }));
  if (!rows.length) box.append(el('p', 'tk-empty', 'Nobody has a ticket in this project.'));
  $('tk-people-count').textContent = plural(rows.length, 'person', 'people');
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

function stateBadge(t) {
  const done = isDone(t);
  const tone = done ? 'done' : isStalled(t) ? 'warn' : isOverdue(t) ? 'bad' : 'open';
  return el('span', `tk-badge tk-badge-${tone}`, t.status || '—');
}

function drawDates(items) {
  const overdue = items.filter(isOverdue)
    .sort((a, b) => +dueOn(a) - +dueOn(b));
  const soon = items.filter(isDueSoon)
    .sort((a, b) => +dueOn(a) - +dueOn(b));

  const late = $('tk-overdue');
  late.replaceChildren(...overdue.map((t) => {
    const by = days(dueOn(t), today());
    return ticketRow(t, `${plural(by, 'day', 'days')} late · due ${fmtDay(t.dueDate)}`);
  }));
  if (!overdue.length) late.append(el('p', 'tk-empty', 'Nothing open is past its due date.'));

  const next = $('tk-soon');
  next.replaceChildren(...soon.map((t) => ticketRow(t, `due ${fmtDay(t.dueDate)}`)));
  if (!soon.length) next.append(el('p', 'tk-empty', 'Nothing open is due in the next seven days.'));

  const undated = items.filter((t) => !isDone(t) && !dueOn(t)).length;
  $('tk-dates-count').textContent = `${overdue.length} overdue · ${soon.length} this week`;
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
      const done = tickets.filter(isDone).length;
      row.append(el('span', 'tk-artefact', id));
      const chips = el('span', 'tk-chips');
      for (const t of tickets.sort((a, b) => Number(a.key) - Number(b.key))) {
        const chip = el('a', `tk-badge tk-badge-${isDone(t) ? 'done' : isStalled(t) ? 'warn' : isOverdue(t) ? 'bad' : 'open'}`,
          `#${t.key} ${t.status}`);
        chip.href = t.url; chip.target = '_blank'; chip.rel = 'noreferrer';
        chip.title = t.subject || '';
        chips.append(chip);
      }
      // With one ticket the chip beside it already says the state, so the only
      // thing worth adding is the count when there is more than one.
      row.append(chips, el('span', 'tk-bar-extra',
        done === tickets.length ? 'done'
          : tickets.length > 1 ? `${done} of ${tickets.length} done` : ''));
      table.append(row);
    }
    group.append(table);
    box.append(group);
  }
  if (!kinds.length) {
    box.append(el('p', 'tk-empty',
      'No ticket is linked to a part of the package yet. Claude Code links one with adam_link, '
      + 'and then a ticket and the screen or contract it builds are the same piece of work here.'));
  }
  $('tk-deliverables-count').textContent = artefacts ? `${plural(artefacts, 'artefact', 'artefacts')}` : '';
  const loose = items.length - linked;
  $('tk-unlinked').textContent = loose
    ? `${plural(loose, 'ticket is', 'tickets are')} not linked to anything in the package, so ${loose === 1 ? 'it does' : 'they do'} not appear above.`
    : 'Every ticket is linked to something in the package.';
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
    : 'Every ticket has a date.';

  if (!placed.length) {
    box.append(el('p', 'tk-empty',
      'No ticket in this project carries a start or a due date, so there is nothing '
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
  const pct = (d) => `${Math.max(0, Math.min(100, ((d - start) / width) * 100))}%`;

  const milestones = new Map();
  for (const [t, at] of placed) {
    const key = t.version || '';
    const group = milestones.get(key) ?? { name: t.version || 'No milestone', epics: new Map() };
    const epicKey = t.parent ? String(t.parent) : `loose:${t.key}`;
    const epic = group.epics.get(epicKey) ?? {
      key: t.parent ? String(t.parent) : '',
      name: t.parentSubject || (t.parent ? `#${t.parent}` : t.subject || `#${t.key}`),
      from: at[0], to: at[1], tickets: [],
    };
    if (at[0] < epic.from) epic.from = at[0];
    if (at[1] > epic.to) epic.to = at[1];
    epic.tickets.push(t);
    group.epics.set(epicKey, epic);
    milestones.set(key, group);
  }

  // The months, once, above everything.
  const scale = el('div', 'tk-gantt-scale');
  for (let d = new Date(start); d <= end; d = new Date(d.getFullYear(), d.getMonth() + 1, 1)) {
    const tick = el('div', 'tk-gantt-month', `${MONTH[d.getMonth()]} ${String(d.getFullYear()).slice(2)}`);
    tick.style.left = pct(d);
    scale.append(tick);
  }
  const now = today();
  if (now >= start && now <= end) {
    const line = el('div', 'tk-gantt-now');
    line.style.left = pct(now);
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
    const allDone = epics.every((e) => e.tickets.every(isDone));
    if (state.ganttOpenOnly && allDone) continue;

    const wrap = el('div', 'tk-gantt-group');
    const total = epics.reduce((n, e) => n + e.tickets.length, 0);
    const done = epics.reduce((n, e) => n + e.tickets.filter(isDone).length, 0);
    wrap.append(el('h3', 'tk-sub', `${group.name} — ${done} of ${total} done`));

    for (const epic of epics) {
      shown += 1;
      const row = el('div', 'tk-gantt-row');
      const label = el('span', 'tk-gantt-label', epic.name);
      label.title = epic.name;
      row.append(label);

      const track = el('div', 'tk-gantt-track');
      const late = epic.tickets.some(isOverdue);
      const finished = epic.tickets.every(isDone);
      const bar = el('div', `tk-gantt-bar${finished ? ' is-done' : late ? ' is-late' : ''}`);
      bar.style.left = pct(epic.from);
      // A single-day epic would be zero wide and invisible, so it gets a floor.
      bar.style.width = `max(3px, ${((epic.to - epic.from) / width) * 100}%)`;
      const share = epic.tickets.length
        ? epic.tickets.filter(isDone).length / epic.tickets.length : 0;
      const fill = el('div', 'tk-gantt-fill');
      fill.style.width = `${Math.round(share * 100)}%`;
      bar.append(fill);
      // Newlines as escapes, not as real line breaks: a tooltip built from a
      // template literal spanning lines carries the source indentation into
      // the tooltip.
      bar.title = [
        epic.name,
        `${fmtDay(epic.from.toISOString())} – ${fmtDay(epic.to.toISOString())}`,
        `${epic.tickets.filter(isDone).length} of ${epic.tickets.length} done`,
        late ? 'something in it is overdue' : '',
      ].filter(Boolean).join('\n');
      track.append(bar);
      row.append(track);
      row.append(el('span', 'tk-gantt-count',
        `${epic.tickets.filter(isDone).length}/${epic.tickets.length}`));
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
    const done = r.tickets.filter(isDone).length;
    const late = r.tickets.filter(isOverdue).length;
    const extra = [`${done} of ${r.tickets.length} done`, late ? `${late} overdue` : ''].filter(Boolean).join(' · ');
    const row = barRow(r.name, r.tickets.length, biggest, done === r.tickets.length ? 'done' : late ? 'bad' : 'open', extra);
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

const WEEKS = 8;

function drawThroughput(items) {
  const done = items.filter(isDone);
  const start = new Date(+today() - (WEEKS * 7 - 1) * DAY);
  const buckets = Array.from({ length: WEEKS }, (_, i) => ({
    from: new Date(+start + i * 7 * DAY), count: 0,
  }));
  for (const t of done) {
    const when = closedAt(t);
    if (!when || when < start) continue;
    const index = Math.min(WEEKS - 1, Math.floor(days(start, when) / 7));
    buckets[index].count += 1;
  }
  const biggest = Math.max(1, ...buckets.map((b) => b.count));
  const box = $('tk-weeks');
  box.replaceChildren(...buckets.map((b) => {
    const column = el('div', 'tk-week');
    // A week where nothing closed draws nothing. A minimum-height bar on a zero
    // is a week that looks like it delivered a little, which is the one thing
    // the column must not say.
    const bar = el('div', `tk-week-bar${b.count ? '' : ' tk-week-none'}`);
    bar.style.height = b.count ? `${Math.round((b.count / biggest) * 100)}%` : '0';
    bar.title = `${plural(b.count, 'ticket', 'tickets')} closed in the week of ${fmtDay(b.from.toISOString())}`;
    column.append(el('div', 'tk-week-count', String(b.count)), el('div', 'tk-week-track', bar),
      el('div', 'tk-week-label', b.from.toLocaleDateString(undefined, { day: 'numeric', month: 'short' })));
    return column;
  }));
  const closed = buckets.reduce((sum, b) => sum + b.count, 0);
  const median = medianDaysToClose(done);
  $('tk-throughput-lede').textContent =
    `${plural(closed, 'ticket', 'tickets')} closed in the last ${WEEKS} weeks`
    + (median == null ? '.' : `, and the median ticket took ${plural(median, 'day', 'days')} from opened to closed.`)
    + ' A ticket counts in the week it was last changed, which for a closed ticket is as close to a closing date as OpenProject 10 gives without reading every comment.';
}

// ── the list, its filters, and the download ─────────────────────────

function drawFilters(items) {
  const statuses = [...new Set(items.map((t) => t.status))].filter(Boolean).sort();
  const people = [...new Set(items.map(who))].sort();
  fillSelect($('tk-status'), 'Every state', statuses, state.filter.status);
  fillSelect($('tk-person'), 'Everyone', people, state.filter.person);
}

function fillSelect(select, allLabel, values, chosen) {
  select.replaceChildren(el('option', null, allLabel), ...values.map((v) => {
    const option = el('option', null, v);
    option.value = v;
    option.selected = v === chosen;
    return option;
  }));
  select.firstChild.value = '';
}

function shown() {
  const { text, status, person, openOnly } = state.filter;
  const needle = text.trim().toLowerCase();
  return (state.data.items ?? []).filter((t) => {
    if (status && t.status !== status) return false;
    if (person && who(t) !== person) return false;
    if (openOnly && isDone(t)) return false;
    if (!needle) return true;
    return [t.key, t.subject, t.assignee, t.parentSubject, t.type, t.version]
      .some((field) => String(field ?? '').toLowerCase().includes(needle));
  }).sort((a, b) => Number(b.key) - Number(a.key));
}

function drawList() {
  const rows = shown();
  const box = $('tk-list');
  box.replaceChildren(...rows.map((t) => ticketRow(t, t.dueDate ? `due ${fmtDay(t.dueDate)}` : fmtWhen(t.updatedAt))));
  if (!rows.length) {
    box.append(el('p', 'tk-empty', state.data.items?.length
      ? 'Nothing matches these filters.'
      : (state.data.note ?? 'This project has no tickets in OpenProject yet.')));
  }
  $('tk-tickets-count').textContent = rows.length === (state.data.items ?? []).length
    ? plural(rows.length, 'ticket', 'tickets')
    : `${rows.length} of ${state.data.items.length}`;
}

function exportCsv() {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const rows = shown();
  const lines = [
    ['number', 'subject', 'type', 'status', 'finished', 'assignee', 'epic', 'milestone',
      'start', 'due', 'overdue', 'percentDone', 'created', 'lastChanged', 'artefacts', 'url'].join(','),
    ...rows.map((t) => [
      t.key, t.subject, t.type, t.status, isDone(t) ? 'yes' : 'no', who(t), t.parentSubject, t.version,
      t.startDate, t.dueDate, isOverdue(t) ? 'yes' : 'no', t.percentDone, t.createdAt, t.updatedAt,
      (t.touches ?? []).map((x) => `${x.kind}:${x.id}`).join(' '), t.url,
    ].map(esc).join(',')),
  ].join('\r\n');
  // A BOM, so Excel on Windows reads the dashes and quotes as written.
  const url = URL.createObjectURL(new Blob(['﻿' + lines], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  const narrowed = Object.values(state.filter).some(Boolean);
  a.download = `${state.project}-tasks${narrowed ? '-filtered' : ''}-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// ── start ───────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  // A reader's page, not an administrator's: it shows the delivery and changes
  // nothing on it. A pm was refused here, which left the role with no view of
  // the thing it exists to oversee.
  if (!auth.isReader(state.me)) { denied(); return hideLoader(); }

  state.project = await auth.ensureProject();
  $('tasks').hidden = false;

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
    drawTimeline(state.data?.items ?? []);
  };

  $('tk-refresh').onclick = async () => {
    $('tk-refresh').disabled = true;
    await load({ refresh: true });
    $('tk-refresh').disabled = false;
  };
  $('tk-search').oninput = (e) => { state.filter.text = e.target.value; drawList(); };
  $('tk-status').onchange = (e) => { state.filter.status = e.target.value; drawList(); };
  $('tk-person').onchange = (e) => { state.filter.person = e.target.value; drawList(); };
  $('tk-open-only').onchange = (e) => { state.filter.openOnly = e.target.checked; drawList(); };
  $('tk-export').onclick = exportCsv;

  loaderSays('Reading the delivery board…');
  await load();
  followSections('overview');
  hideLoader();
})();
