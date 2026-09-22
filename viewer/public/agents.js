/**
 * How much the agent is being used, and what keeps failing.
 *
 * **Three groupings because three different questions get asked**, and a single
 * list answers none of them well: by person (is this being used at all), by tool
 * (what is broken), and session by session (what did this one actually cost).
 *
 * Everybody signed in may open this. What they see is not the same: a developer
 * reads their own sessions, and an administrator or a project manager reads the
 * project's. The service decides that and says which it gave — `whole` on the
 * reply — so the page can label what it is showing rather than let somebody
 * conclude the team has been quiet when they are looking at their own row.
 *
 * The lede says what is not collected, in the place where somebody would
 * otherwise assume it is. A page of per-person timings that does not say where
 * its numbers stop is a page people are right to be uneasy about.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

/** Durations people can read. Minutes up to a couple of hours, then hours —
 *  "412 minutes" is a number somebody has to divide before it means anything. */
function spell(ms) {
  if (!ms) return '—';
  const seconds = ms / 1000;
  if (seconds < 90) return `${Math.round(seconds)}s`;
  const minutes = seconds / 60;
  if (minutes < 120) return `${Math.round(minutes)} min`;
  const hours = minutes / 60;
  return `${hours.toFixed(1)} h`;
}

const fmt = (iso) => (iso ? new Date(iso).toLocaleString(undefined,
  { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '—');

const state = { days: 14, data: null };

function say(message) {
  $('ag-error').textContent = message ?? '';
  $('ag-error').hidden = !message;
}

function drawStats() {
  const d = state.data ?? {};
  const people = d.people ?? [];
  const tools = d.tools ?? [];
  const box = $('ag-stats');
  box.innerHTML = '';
  const stat = (value, label, hint) => {
    const card = el('div', 'stat-card');
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };
  const active = people.reduce((n, p) => n + p.activeMs, 0);
  const calls = tools.reduce((n, t) => n + t.calls, 0);
  const failed = tools.reduce((n, t) => n + t.failed, 0);
  box.append(stat(spell(active), 'agent time', `over ${d.days} days`));
  box.append(stat(people.length, d.whole ? 'people' : 'you', d.whole ? 'sent anything at all' : ''));
  box.append(stat((d.sessions ?? []).length, 'sessions', 'each one ended'));
  box.append(stat(calls, 'tool calls', ''));
  const bad = stat(failed, 'failed', calls ? `${Math.round((failed / calls) * 100)}% of calls` : '');
  if (failed) bad.classList.add('ag-stat-bad');
  box.append(bad);

  $('ag-scope').textContent = d.whole ? 'the whole project' : 'your own';
  $('ag-nothing').hidden = Boolean(people.length);
}

function drawPeople() {
  const people = state.data?.people ?? [];
  $('ag-people-count').textContent = people.length ? String(people.length) : '';
  const host = $('ag-people');
  host.innerHTML = '';
  if (!people.length) {
    host.append(el('p', 'auth-note auth-fine', 'Nobody has sent anything in this window.'));
    return;
  }
  for (const person of people) {
    const row = el('div', 'admin-row ag-row');
    row.append(el('span', 'account-name', person.name));
    row.append(el('span', 'ag-num', spell(person.activeMs)));
    row.append(el('span', 'invite-who',
      `${person.sessions} session${person.sessions === 1 ? '' : 's'} · `
      + `${person.tickets} ticket${person.tickets === 1 ? '' : 's'}`));
    row.append(el('span', 'ag-num', `${person.calls} calls`));
    // A rate rather than a count: ten failures out of a thousand calls and ten
    // out of twelve are the same number and not the same situation.
    const rate = person.calls ? Math.round((person.failures / person.calls) * 100) : 0;
    const bad = el('span', `ag-verdict${person.failures ? ' bad' : ''}`,
      person.failures ? `${person.failures} failed · ${rate}%` : 'nothing failed');
    row.append(bad);
    host.append(row);
  }
}

function drawTools() {
  const tools = state.data?.tools ?? [];
  $('ag-tools-count').textContent = tools.length ? String(tools.length) : '';
  const host = $('ag-tools');
  host.innerHTML = '';
  if (!tools.length) {
    host.append(el('p', 'auth-note auth-fine', 'No tool calls in this window.'));
    return;
  }
  for (const tool of tools) {
    const row = el('div', `admin-row ag-row${tool.failed ? ' ag-row-bad' : ''}`);
    row.append(el('span', 'ag-tool', tool.tool));
    row.append(el('span', 'ag-num', `${tool.calls} calls`));
    const mean = tool.calls ? tool.totalMs / tool.calls : 0;
    const timing = el('span', 'invite-who', `${spell(mean)} typical · ${spell(tool.worstMs)} worst`);
    timing.title = `Total ${spell(tool.totalMs)} across ${tool.calls} calls`;
    row.append(timing);
    // Which kinds, not just how many. "Edit failed twice" is a count; "Edit
    // failed twice, both not-found" is a lead.
    const why = Object.entries(tool.why ?? {})
      .sort((a, b) => b[1] - a[1]).map(([word, n]) => `${word} ×${n}`).join(', ');
    row.append(el('span', 'ag-why', why || '—'));
    row.append(el('span', `ag-verdict${tool.failed ? ' bad' : ' ok'}`,
      tool.failed ? `${tool.failed} failed` : 'clean'));
    host.append(row);
  }
}

function drawSessions() {
  const sessions = state.data?.sessions ?? [];
  $('ag-sessions-count').textContent = sessions.length ? String(sessions.length) : '';
  const host = $('ag-sessions');
  host.innerHTML = '';
  if (!sessions.length) {
    host.append(el('p', 'auth-note auth-fine', 'No sessions in this window.'));
    return;
  }
  for (const session of sessions) {
    const box = el('details', 'ag-session');
    const head = el('summary', 'ag-session-head');
    head.append(el('span', 'account-name', session.who));
    head.append(el('span', 'ag-tool', session.ticket ? `#${session.ticket}` : 'no ticket'));
    head.append(el('span', 'invite-who', session.repo || '—'));
    head.append(el('span', 'ag-num', spell(session.activeMs)));
    head.append(el('span', 'invite-who', fmt(session.startedAt)));
    box.append(head);

    // Fetched when opened, not with the list. A fortnight of sessions is a
    // fortnight of event lists, and almost none of them get looked at.
    let loaded = false;
    box.addEventListener('toggle', async () => {
      if (!box.open || loaded) return;
      loaded = true;
      const body = el('div', 'ag-events');
      body.append(el('p', 'auth-note auth-fine', 'Reading…'));
      box.append(body);
      try {
        const full = await auth.agentSession(session.id);
        body.innerHTML = '';
        if (!full.events.length) {
          body.append(el('p', 'auth-note auth-fine', 'Nothing recorded in this session.'));
          return;
        }
        for (const event of full.events) {
          const line = el('div', `ag-event${event.ok ? '' : ' bad'}`);
          line.append(el('span', 'ag-event-at', fmt(event.at)));
          line.append(el('span', 'ag-tool', event.tool || event.kind));
          line.append(el('span', 'ag-num', event.ms ? spell(event.ms) : ''));
          line.append(el('span', 'ag-why', event.ok ? '' : event.why || 'error'));
          body.append(line);
        }
      } catch (error) {
        body.innerHTML = '';
        body.append(el('p', 'auth-error', error.message));
        loaded = false;
      }
    });
    host.append(box);
  }
}

async function load() {
  say('');
  try {
    state.data = await auth.agentUsage(state.days);
  } catch (error) {
    say(error.message);
    return;
  }
  drawStats();
  drawPeople();
  drawTools();
  drawSessions();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';
  $('agents').hidden = false;
  $('ag-days').onchange = (e) => { state.days = Number(e.target.value); load(); };
  await load();
})();
