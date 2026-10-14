/**
 * Agent activity: is the agent being used, and what keeps failing?
 *
 * Asked weekly by a project manager or an administrator, and by a developer of
 * their own usage. The page opens on the answer to both halves as one sentence
 * each — how many people used it and for how long, then which tool fails most
 * and why — and spends its one picture on the second half, because that is the
 * half somebody can do something about.
 *
 * **Three groupings because three different questions get asked**, and a single
 * list answers none of them well: by person (is this being used at all), by tool
 * (what is broken), and session by session (what did this one actually cost).
 * They are the rail's three sections after the opening.
 *
 * **Who sees whose is the service's decision, not this page's.** A developer
 * reads their own sessions and an administrator or a pm reads the project's;
 * the reply says which it gave (`whole`), and the page words itself from that —
 * "You: 6.2 h…" against "9 of 11 people…" — rather than let somebody conclude
 * the team has been quiet when they are looking at their own row. Only those
 * who read the whole get a person filter; the service ignores one from anybody
 * else.
 *
 * **Every figure is the window's.** The service counts in SQL over the whole
 * window and sends the session list capped at 100 with the true count beside it,
 * so "the latest 100 of 312" is said rather than 100 being passed off as the
 * total.
 *
 * The lede says what is not collected, in the place where somebody would
 * otherwise assume it is. A page of per-person timings that does not say where
 * its numbers stop is a page people are right to be uneasy about.
 */
// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer.
import '/page-chrome.js';
import * as auth from '/validation.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, verdict, next, mountScope, legend, table, personLink, param,
} from '/sheet.js';

const $ = (id) => document.getElementById(id);

/** Durations people can read. Minutes up to a couple of hours, then hours —
 *  "412 minutes" is a number somebody has to divide before it means anything. */
function spell(ms) {
  if (!ms) return '—';
  const seconds = ms / 1000;
  if (seconds < 90) return `${Math.round(seconds)} s`;
  const minutes = seconds / 60;
  if (minutes < 120) return `${Math.round(minutes)} min`;
  const hours = minutes / 60;
  return `${hours < 10 ? hours.toFixed(1) : Math.round(hours)} h`;
}

const when = (iso) => (iso ? new Date(iso).toLocaleString('en-GB',
  { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—');
const clock = (iso) => (iso ? new Date(iso).toLocaleTimeString('en-GB',
  { hour: '2-digit', minute: '2-digit' }) : '');
const pct = (part, whole) => (whole ? Math.round((part / whole) * 100) : 0);

/** The windows offered, the default first and as value '' (the sheet's rule:
 *  the first option is what an absent parameter means). */
const WINDOWS = [['', 'Last 14 days'], ['7', 'Last 7 days'], ['30', 'Last 30 days'], ['90', 'Last 90 days']];
const RAIL_NAME = { 7: 'Last 7 days', 14: 'This fortnight', 30: 'Last 30 days', 90: 'Last 90 days' };
const daysOf = (scope) => Number(scope?.days) || 14;

/** A connector tool's name without its address: `mcp__adam__adam_board` is
 *  `adam_board` on a bar with room for a dozen characters. The tables keep
 *  the whole name, and the bar's title carries it. */
const shortTool = (name) => (name.startsWith('mcp__') ? name.split('__').slice(2).join('__') || name : name);

/** The failure word a tool gets most, for "mostly not-found". */
const mostly = (tool) => Object.entries(tool.why ?? {}).sort((a, b) => b[1] - a[1])[0]?.[0] ?? '';
/** "not-found 30, timeout 4": every word, most first. */
const whyAll = (tool) => Object.entries(tool.why ?? {})
  .sort((a, b) => b[1] - a[1]).map(([word, n]) => `${word} ${fmt(n)}`).join(', ');

const state = { me: null, data: null, whole: false, scope: null, roster: [] };

function say(message) {
  $('ag-error').textContent = message ?? '';
  $('ag-error').hidden = !message;
}

// ── the opening ─────────────────────────────────────────────────────

/** Whose figures these are, as the subject of the headline. */
function subject(d) {
  if (!d.whole) return 'You';
  if (d.person) return state.roster.find((p) => p.id === d.person)?.name ?? 'This person';
  return null;
}

function drawOverview() {
  const d = state.data;
  const t = d.totals;
  const days = d.days;
  const tools = d.tools ?? [];
  const worst = tools.find((x) => x.failed);
  const rate = pct(t.failed, t.calls);
  const who = subject(d);
  const windowWords = RAIL_NAME[days] === 'This fortnight' ? 'Last 14 days' : (RAIL_NAME[days] ?? `Last ${days} days`);

  const whenLine = el('span');
  whenLine.append(el('strong', '', windowWords),
    d.whole ? (d.person ? ` · one person, of ${plural(state.roster.length, 'person', 'people')} who used it` : ' · the whole project') : ' · your own sessions');

  $('ag-nothing').hidden = true;
  if (!t.sessions) {
    // Nothing arrived. Said as what to do, because an empty page here almost
    // always means the hooks are not installed rather than that nobody worked.
    verdict($('ag-verdict'), {
      when: whenLine,
      headline: who && who !== 'You'
        ? `Nothing has arrived from ${who} in this window.`
        : who === 'You' ? 'Nothing has arrived from you in this window.'
          : 'Nothing has arrived in this window.',
      pace: 'A session is sent when it ends, not while it runs, by the usage hooks on '
        + 'each machine.',
    });
    $('ag-figure').hidden = true;
    $('ag-hero').classList.add('is-single');
    drawNothing();
    next($('ag-next'), d.whole && (d.quiet ?? []).length && !d.person
      ? `${plural(d.quiet.length, 'person', 'people')} on the project could have used it. `
        + 'Ask them whether the ADAM plugin is installed.'
      : '');
    return;
  }

  // The headline: is it being used.
  let headline;
  if (who) {
    headline = `${who}: ${spell(t.activeMs)} across ${plural(t.sessions, 'session')}`
      + `${t.tickets ? ` on ${plural(t.tickets, 'ticket')}` : ''}; ${rate}% of calls failed.`;
  } else {
    const used = t.people;
    headline = d.expected > used
      ? `${fmt(used)} of ${plural(d.expected, 'person', 'people')} used the agent, ${spell(t.activeMs)} active.`
      : `${plural(used, 'person', 'people')} used the agent, ${spell(t.activeMs)} active.`;
  }

  // The line under it: what keeps failing.
  let pace;
  if (worst) {
    const word = mostly(worst);
    pace = `${worst.tool} fails most${d.whole && !d.person ? '' : (who === 'You' ? ' for you' : '')}: `
      + `${fmt(worst.failed)} of ${plural(worst.calls, 'call')}${word ? `, mostly ${word}` : ''}.`;
  } else {
    pace = `Nothing failed in ${plural(t.calls, 'tool call')}.`;
  }

  verdict($('ag-verdict'), {
    when: whenLine,
    headline,
    headlineId: 'ag-headline',
    // The judgement in words. The rate itself is in the headline when the
    // page is about one person, and the failed count is in the ledger, so the
    // pill does not repeat either: it says what the figure amounts to.
    pill: t.calls ? {
      tone: rate >= 10 ? 'bad' : rate >= 4 ? 'warn' : 'ok',
      text: rate >= 10 ? 'Failing often' : rate >= 4 ? `${who ? 'Some' : `${rate}% of`} calls failing` : 'Mostly working',
    } : null,
    pace,
    ledger: [
      { label: 'Active time', value: spell(t.activeMs), title: 'Gaps over five minutes are not counted' },
      { label: 'Sessions', value: t.sessions },
      ...(who ? [] : [{ label: 'People', value: t.people }]),
      { label: 'Tickets', value: t.tickets, title: 'Tickets open while the agent ran' },
      { label: 'Tool calls', value: t.calls },
      { label: 'Failed', value: t.failed, bad: t.failed > 0, swatch: t.failed ? 'late' : undefined },
    ],
  });
  drawFigure();
  drawNext(worst);
}

/** The one thing to do. Somebody not using it at all comes before a tool that
 *  fails, because nothing on this page can be learned about a person whose
 *  machine sends nothing. */
function drawNext(worst) {
  const d = state.data;
  const quiet = d.whole && !d.person ? (d.quiet ?? []) : [];
  if (quiet.length) {
    const names = quiet.slice(0, 3);
    const line = el('span');
    line.append(`Ask ${names.length === quiet.length ? '' : 'people like '}`);
    names.forEach((name, i) => {
      if (i) line.append(i === names.length - 1 ? ' and ' : ', ');
      line.append(personLink(name));
    });
    line.append(` whether the ADAM plugin is installed: nothing has arrived from `
      + `${quiet.length === 1 ? 'them' : `these ${plural(quiet.length, 'person', 'people')}`} `
      + `in ${d.days} days. `);
    const go = el('a', '', 'Who has used it');
    go.href = '#people';
    line.append(go);
    next($('ag-next'), line);
    return;
  }
  if (worst) {
    const line = el('span');
    const word = mostly(worst);
    line.append(`Look at ${worst.tool}${word ? `'s ${word} failures` : ''}: `
      + `${fmt(worst.why?.[word] ?? worst.failed)} in this window. `);
    const go = el('a', '', 'Every tool, with why');
    go.href = '#tools';
    line.append(go);
    next($('ag-next'), line);
    return;
  }
  next($('ag-next'), '');
}

/** The bold thing: failed calls per tool, as bars against the tool that fails
 *  most. The count is the bar; how many calls it was out of, and the word it
 *  failed with most, are the words beside it. Only failing tools are drawn —
 *  the clean ones are in the table on Tools failing. */
function drawFigure() {
  const tools = (state.data.tools ?? []).filter((t) => t.failed).slice(0, 8);
  const figure = $('ag-figure');
  $('ag-hero').classList.toggle('is-single', !tools.length);
  figure.hidden = !tools.length;
  if (!tools.length) return;
  const most = Math.max(...tools.map((t) => t.failed));
  const box = $('ag-bars');
  box.replaceChildren();
  for (const tool of tools) {
    const row = el('div', 'sh-bar-row ag-bar-row');
    row.append(el('span', 'sh-bar-label ag-tool', shortTool(tool.tool)));
    const track = el('span', 'ag-track');
    track.setAttribute('aria-hidden', 'true');
    const fill = el('span', 'ag-fill sh-fill-late');
    fill.style.width = `${Math.max(2, (tool.failed / most) * 100)}%`;
    track.append(fill);
    row.append(track);
    row.append(el('span', 'sh-bar-count ag-bar-count', fmt(tool.failed)));
    const word = mostly(tool);
    // Under the bar rather than beside it: "of 702 calls, mostly not-found" is
    // the half of the row that explains it, and a fourth column cut it to "m…".
    row.append(el('span', 'sh-bar-extra ag-bar-extra',
      `of ${plural(tool.calls, 'call')} (${pct(tool.failed, tool.calls)}%)${word ? `, mostly ${word}` : ''}`));
    row.title = `${tool.tool}: ${fmt(tool.failed)} of ${plural(tool.calls, 'call')} failed (${whyAll(tool)})`;
    box.append(row);
  }
  const more = (state.data.tools ?? []).filter((t) => t.failed).length - tools.length;
  $('ag-figure-caption').textContent = `Failed calls, by tool${more > 0 ? ` (the ${tools.length} failing most; ${more} more on Tools failing)` : ''}`;
  $('ag-bars-key').replaceChildren(legend([
    { kind: 'late', label: 'Failed calls; the longest bar is the tool failing most' },
  ]));
  // The picture's twin, for a screen reader and for copying.
  $('ag-bars-twin').replaceChildren(table({
    caption: 'Failed calls, by tool',
    srOnly: true,
    columns: [
      { key: 'tool', label: 'Tool' },
      { key: 'failed', label: 'Failed', num: true },
      { key: 'calls', label: 'Calls', num: true },
      { key: 'why', label: 'Why', render: whyAll },
    ],
    rows: tools,
  }));
}

/** No sessions in the window, and why that usually is. The plugin installs the
 *  hooks now (updates, 28 September); the old README asked people to paste
 *  JSON into settings.json by hand, which is to say they mostly did not. */
function drawNothing() {
  const box = $('ag-nothing');
  box.hidden = false;
  box.replaceChildren();
  box.append(el('h3', 'sh-part-title', 'Getting sessions to arrive'));
  const p = el('p', 'sh-note');
  p.append('The usage hooks come with the ADAM plugin for Claude Code. On each '
    + 'developer’s machine, in Claude Code:');
  box.append(p);
  const code = el('pre', 'ag-code', '/plugin marketplace add Diretide298/Solution_Architecture\n/plugin install adam@adam');
  box.append(code);
  const after = el('p', 'sh-note');
  after.append('Somebody still on the zip install has the connector without the hooks, '
    + 'and sends nothing here until they move to the plugin. ');
  const more = el('a', 'sh-link', 'What changed, and why');
  more.href = '/updates.html';
  after.append(more, '.');
  box.append(after);
}

// ── people ──────────────────────────────────────────────────────────

function drawPeople() {
  const d = state.data;
  const host = $('ag-people');
  // The roster is the whole window, whoever the filter names, so the picker can
  // be changed back. The table follows the filter, though: narrowed to one
  // person, it shows that person.
  const rows = d.person ? d.people.filter((p) => p.id === d.person) : d.people;
  host.replaceChildren(table({
    caption: d.whole ? `Everybody who sent a session in the last ${d.days} days` : `Your sessions in the last ${d.days} days`,
    columns: [
      { key: 'name', label: 'Person', render: (p) => personLink(p.name), sort: (p) => p.name.toLowerCase() },
      { key: 'activeMs', label: 'Active', num: true, render: (p) => spell(p.activeMs), sort: (p) => p.activeMs },
      { key: 'sessions', label: 'Sessions', num: true, sort: (p) => p.sessions },
      {
        key: 'tickets', label: 'Tickets worked on',
        render: (p) => {
          const cell = el('span', 'ag-tickets');
          cell.append(el('span', 'ag-ticket-count', fmt(p.tickets)));
          for (const key of p.ticketKeys ?? []) cell.append(el('span', 'ag-key', `#${key}`));
          if (p.tickets > (p.ticketKeys ?? []).length) {
            cell.append(el('span', 'sh-quiet', `and ${fmt(p.tickets - p.ticketKeys.length)} more`));
          }
          return cell;
        },
        sort: (p) => p.tickets,
      },
      { key: 'calls', label: 'Calls', num: true, sort: (p) => p.calls },
      {
        key: 'failures', label: 'Failed', num: true,
        // A rate beside the count: ten failures out of a thousand calls and ten
        // out of twelve are the same number and not the same situation.
        render: (p) => (p.failures ? `${fmt(p.failures)} · ${pct(p.failures, p.calls)}%` : 'none'),
        sort: (p) => pct(p.failures, p.calls),
      },
    ],
    rows,
    empty: d.whole ? 'Nobody sent a session in this window. The ADAM plugin installs the hooks that send them.'
      : 'Nothing from you in this window. The ADAM plugin installs the hooks that send it.',
  }));

  const quiet = $('ag-quiet');
  const names = d.whole && !d.person ? (d.quiet ?? []) : [];
  quiet.hidden = !names.length;
  quiet.replaceChildren();
  if (names.length) {
    quiet.append(el('strong', '', `Not used in ${d.days} days: `));
    names.forEach((name, i) => {
      if (i) quiet.append(', ');
      quiet.append(personLink(name));
    });
    quiet.append('. Developers and team leads on this project with no session in the window. '
      + 'Usually the plugin is not installed on their machine.');
  }
}

// ── tools ───────────────────────────────────────────────────────────

function drawTools() {
  const tools = state.data.tools ?? [];
  $('ag-tools').replaceChildren(table({
    caption: 'Tool calls in this window, the ones failing most first',
    columns: [
      { key: 'tool', label: 'Tool', render: (t) => el('span', 'ag-tool', t.tool), sort: (t) => t.tool.toLowerCase() },
      { key: 'calls', label: 'Calls', num: true, sort: (t) => t.calls },
      {
        key: 'failed', label: 'Failed', num: true, sort: (t) => t.failed,
        cellClass: (t) => (t.failed ? 'is-late' : ''),
        render: (t) => (t.failed ? fmt(t.failed) : 'none'),
      },
      { key: 'rate', label: 'Rate', num: true, render: (t) => `${pct(t.failed, t.calls)}%`, sort: (t) => pct(t.failed, t.calls) },
      { key: 'why', label: 'Why it failed', render: (t) => whyAll(t) || '—' },
      {
        key: 'typical', label: 'Typical', num: true,
        render: (t) => spell(t.calls ? t.totalMs / t.calls : 0), sort: (t) => (t.calls ? t.totalMs / t.calls : 0),
      },
      { key: 'worstMs', label: 'Slowest', num: true, render: (t) => spell(t.worstMs), sort: (t) => t.worstMs },
    ],
    rows: tools,
    empty: 'No tool calls in this window.',
  }));
}

// ── sessions ────────────────────────────────────────────────────────

/** A table with a row that opens under each session. Not the sheet's table:
 *  that one has no row that opens, and the events are fetched only when one
 *  is opened — a fortnight of sessions is a fortnight of event lists, and
 *  almost none of them get looked at. */
function drawSessions() {
  const d = state.data;
  const sessions = d.sessions ?? [];
  const shown = sessions.length;
  $('ag-sessions-note').textContent = !shown ? 'No sessions in this window.'
    : d.sessionCount > shown
      ? `The latest ${fmt(shown)} of ${plural(d.sessionCount, 'session')} in this window, newest first. `
        + 'Every figure elsewhere on the page counts all of them. Open one to read it event by event.'
      : `${plural(shown, 'session')}, newest first. Open one to read it event by event.`;
  const host = $('ag-sessions');
  host.replaceChildren();
  if (!shown) return;

  const wrap = el('div', 'sh-table-wrap');
  const t = el('table', 'sh-table ag-sessions');
  const head = el('tr');
  const cols = ['Started', ...(d.whole ? ['Person'] : []), 'Ticket', 'Repository', 'Active', 'Ended', 'Agent', 'Machine'];
  for (const label of cols) {
    const th = el('th', label === 'Active' ? 'is-num' : '', label);
    th.scope = 'col';
    head.append(th);
  }
  const thead = el('thead');
  thead.append(head);
  const tbody = el('tbody');
  t.append(thead, tbody);
  wrap.append(t);
  host.append(wrap);

  for (const s of sessions) {
    const tr = el('tr');
    const first = el('th', 'is-nowrap');
    first.scope = 'row';
    const open = el('button', 'ag-open', when(s.startedAt));
    open.type = 'button';
    open.setAttribute('aria-expanded', 'false');
    open.title = 'Read this session event by event';
    first.append(open);
    tr.append(first);
    if (d.whole) {
      const td = el('td');
      td.append(personLink(s.who));
      tr.append(td);
    }
    tr.append(el('td', s.ticket ? 'ag-key' : 'sh-quiet', s.ticket ? `#${s.ticket}` : 'none'));
    tr.append(el('td', '', s.repo || '—'));
    tr.append(el('td', 'is-num', spell(s.activeMs)));
    // Ended as a clock time when it is the same day, which it nearly always
    // is; the date again only when a session ran past midnight.
    const sameDay = s.endedAt && s.startedAt && s.endedAt.slice(0, 10) === s.startedAt.slice(0, 10);
    tr.append(el('td', 'is-nowrap', sameDay ? clock(s.endedAt) : when(s.endedAt)));
    tr.append(el('td', '', s.agent || '—'));
    tr.append(el('td', '', s.host || '—'));
    tbody.append(tr);

    let detail = null;
    open.onclick = async () => {
      if (detail) {
        const opening = detail.hidden;
        detail.hidden = !opening;
        open.setAttribute('aria-expanded', String(opening));
        return;
      }
      detail = el('tr', 'ag-detail');
      const cell = el('td');
      cell.colSpan = cols.length;
      detail.append(cell);
      tr.after(detail);
      open.setAttribute('aria-expanded', 'true');
      cell.append(el('p', 'sh-quiet', 'Reading the events…'));
      try {
        const full = await auth.agentSession(s.id);
        cell.replaceChildren(drawEvents(full));
      } catch (error) {
        cell.replaceChildren(el('p', 'auth-error', `Could not read this session: ${error.message}. Close it and open it again to retry.`));
        detail.remove();
        detail = null;
        open.setAttribute('aria-expanded', 'false');
        say(`Could not read the session started ${when(s.startedAt)}: ${error.message}.`);
      }
    };
  }
}

function drawEvents(full) {
  const box = el('div', 'ag-events');
  if (!full.events.length) {
    box.append(el('p', 'sh-quiet', 'Nothing was recorded in this session.'));
    return box;
  }
  const bad = full.events.filter((e) => !e.ok).length;
  box.append(el('p', 'ag-events-head',
    `${plural(full.events.length, 'event')}${bad ? `, ${fmt(bad)} failed` : ', none failed'}.`));
  const list = el('ol', 'ag-event-list');
  for (const event of full.events) {
    const li = el('li', `ag-event${event.ok ? '' : ' is-bad'}`);
    li.append(el('span', 'ag-event-at', clock(event.at)));
    li.append(el('span', 'ag-tool', event.tool || event.kind));
    li.append(el('span', 'ag-event-ms', event.ms ? spell(event.ms) : ''));
    li.append(el('span', 'ag-event-why', event.ok ? '' : `failed: ${event.why || 'error'}`));
    list.append(li);
  }
  box.append(list);
  return box;
}

// ── the filter ──────────────────────────────────────────────────────

function mountFilter() {
  const fields = [{ key: 'days', label: 'Window', options: WINDOWS, sticky: true }];
  if (state.whole) {
    fields.push({
      key: 'person', label: 'Person', all: 'Everybody',
      options: () => state.roster.map((p) => [p.name, p.name]),
    });
  }
  state.scope = mountScope({
    root: $('ag-scope'),
    fields,
    says: (s) => {
      const span = `the last ${daysOf(s)} days`;
      if (!state.whole) return `Showing your own sessions in ${span}. Only an administrator or a project manager sees the team's.`;
      return s.person ? `Showing ${s.person}'s sessions in ${span}.`
        : `Showing everybody's sessions in ${span}.`;
    },
    onChange: () => load(),
  });
}

// ── reading ─────────────────────────────────────────────────────────

let asking = 0;
let showPanel = null;
async function load() {
  say('');
  const mine = ++asking;
  const days = daysOf(state.scope?.state ?? { days: param('days') });
  const wantName = state.scope?.state?.person ?? param('person');
  const wantId = state.roster.find((p) => p.name === wantName)?.id ?? 0;
  $('ag-nav-overview').textContent = RAIL_NAME[days] ?? `Last ${days} days`;
  $('ag-asof').textContent = 'Reading…';
  let data;
  try {
    data = await auth.agentUsageFor(days, wantId);
    // The first read cannot name a person by id: the roster that maps the name
    // in the address to an account comes back with it. Asked again, once.
    if (wantName && !wantId && data.whole) {
      const found = data.people.find((p) => p.name === wantName);
      if (found) {
        state.roster = data.people;
        data = await auth.agentUsageFor(days, found.id);
      }
    }
  } catch (error) {
    if (mine !== asking) return;
    say(`Could not read the agent sessions: ${error.message}. Reload the page to try again.`);
    $('ag-asof').textContent = '';
    $('ag-asof').classList.add('is-failed');
    return;
  }
  if (mine !== asking) return;
  state.data = data;
  state.whole = data.whole;
  if (!data.person) state.roster = data.people;
  else if (!state.roster.length) state.roster = data.people;
  $('ag-asof').classList.remove('is-failed');
  $('ag-asof').textContent = `Read at ${new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`;

  // A developer's People is their own row, which the opening already says.
  const peopleWas = $('ag-nav-people').hidden;
  $('ag-nav-people').hidden = !data.whole;
  $('ag-nav-who').textContent = data.whole ? 'Who and what' : 'What';
  // A link to #people that a developer followed landed before the rail knew
  // to hide it; sent on to the opening now that it does.
  if (peopleWas !== $('ag-nav-people').hidden && location.hash === '#people') showPanel?.('overview');

  if (!state.scope) mountFilter();
  else state.scope.redraw();
  drawOverview();
  drawPeople();
  drawTools();
  drawSessions();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  state.me = me;
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';
  $('agents').hidden = false;
  showPanel = mountPanels({ nav: document.querySelector('#agents .set-nav'), fallback: 'overview' });
  await load();
})();
