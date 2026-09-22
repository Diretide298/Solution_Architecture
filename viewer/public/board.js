/**
 * A developer's own work, and the gate standing in front of it.
 *
 * **Everybody signed in gets this page and it is never anybody else's.** The
 * service answers `/api/board/mine` from the caller's own OpenProject token
 * with `assignee = me`, so there is no id to tamper with and no wider version
 * of this view to reach for. Where the delivery as a whole is read — Tasks —
 * is a different page with a different gate.
 *
 * **Grouped by what the data can honestly say.** OpenProject statuses are the
 * team's own words and a project can rename them any afternoon, so nothing here
 * matches on a status name to decide whether work has started. Two fields can
 * be trusted: the due date, and `percentDone`. Everything below is built from
 * those, which is why the sections are *overdue / this week / started / backlog*
 * rather than the columns a board usually has.
 *
 * The testing gate lives here too. It shipped with the Claude connector as its
 * only interface, which meant somebody not using Claude Code could be stopped
 * from closing a ticket by a rule they had no way to satisfy.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const DAY = 86_400_000;
const midnight = () => { const d = new Date(); d.setHours(0, 0, 0, 0); return d; };
const asDate = (iso) => { const d = iso ? new Date(iso) : null; return d && !Number.isNaN(+d) ? d : null; };
const fmtDay = (iso) => {
  const d = asDate(iso);
  return d ? d.toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : '';
};
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;

const state = { data: null, batches: null };

function say(id, message) {
  $(id).textContent = message ?? '';
  $(id).hidden = !message;
}

// ── one ticket ───────────────────────────────────────────────────────

function ticketRow(t, extra) {
  const row = el('div', 'admin-row bd-row');
  const key = el('a', 'bd-key', `#${t.key}`);
  key.href = t.url;
  key.target = '_blank';
  key.rel = 'noreferrer';
  row.append(key);

  const title = el('span', 'bd-subject', t.subject || '—');
  title.title = t.subject || '';
  row.append(title);

  // What it touches in the package, which is the join neither system can make
  // on its own and the reason a ticket is worth opening here rather than in
  // OpenProject.
  const touches = el('span', 'bd-touches');
  for (const touch of (t.touches ?? []).slice(0, 4)) {
    touches.append(el('span', 'bd-touch', `${touch.kind} ${touch.id}`));
  }
  if ((t.touches ?? []).length > 4) {
    touches.append(el('span', 'bd-touch bd-touch-more', `+${t.touches.length - 4}`));
  }
  if (!(t.touches ?? []).length) touches.append(el('span', 'bd-touch-none', 'not linked'));
  row.append(touches);

  row.append(el('span', 'bd-status', t.status || ''));
  row.append(el('span', 'bd-when', extra ?? ''));
  return row;
}

function fill(hostId, countId, rows, empty) {
  const host = $(hostId);
  host.replaceChildren();
  $(countId).textContent = rows.length ? String(rows.length) : '';
  if (!rows.length) {
    host.append(el('p', 'auth-note auth-fine', empty));
    return;
  }
  for (const [ticket, extra] of rows) host.append(ticketRow(ticket, extra));
}

// ── the board ────────────────────────────────────────────────────────

function drawBoard() {
  const items = state.data?.items ?? [];
  const finished = state.data?.finished ?? [];
  const now = midnight();
  const soon = new Date(+now + 7 * DAY);

  const overdue = [];
  const week = [];
  const started = [];
  const backlog = [];
  for (const t of items) {
    const due = asDate(t.dueDate);
    if (due && due < now) { overdue.push([t, `due ${fmtDay(t.dueDate)}`]); continue; }
    if (due && due <= soon) { week.push([t, `due ${fmtDay(t.dueDate)}`]); continue; }
    // `percentDone` is the only field that says work has happened without
    // reading a status name, and a status name is a thing a team renames.
    if (t.percentDone > 0) { started.push([t, `${t.percentDone}% done`]); continue; }
    backlog.push([t, due ? `due ${fmtDay(t.dueDate)}` : 'no date']);
  }
  const byDue = (a, b) => (asDate(a[0].dueDate) ?? 0) - (asDate(b[0].dueDate) ?? 0);
  overdue.sort(byDue);
  week.sort(byDue);

  fill('bd-overdue', 'bd-overdue-count', overdue, 'Nothing of yours is past its date.');
  fill('bd-week', 'bd-week-count', week, 'Nothing of yours is due in the next seven days.');
  fill('bd-started', 'bd-started-count', started, 'Nothing of yours is part finished.');
  fill('bd-backlog', 'bd-backlog-count', backlog, 'Nothing waiting.');
  fill('bd-done', 'bd-done-count',
    finished.map((t) => [t, `closed ${fmtDay(t.updatedAt)}`]),
    'Nothing closed in the last seven days.');

  const box = $('bd-stats');
  box.replaceChildren();
  const stat = (value, label, hint, tone) => {
    const card = el('div', `stat-card${tone ? ` bd-stat-${tone}` : ''}`);
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };
  box.append(stat(items.length, 'open', 'assigned to you'));
  box.append(stat(overdue.length, 'overdue', overdue.length ? 'past the date' : 'nothing late',
    overdue.length ? 'bad' : ''));
  box.append(stat(week.length, 'due this week', ''));
  box.append(stat(finished.length, 'closed', 'in the last seven days'));

  $('bd-note').textContent = state.data?.note ?? '';
}

// ── the gate ─────────────────────────────────────────────────────────

function drawGate() {
  const gate = state.data?.testing;
  const box = $('bd-gate');
  if (!gate || (!gate.full && !gate.submitted && gate.verdict !== 'failed')) {
    box.hidden = true;
    return;
  }
  box.hidden = false;
  box.classList.toggle('is-blocked', Boolean(gate.full));
  if (gate.verdict === 'failed') {
    $('bd-gate-title').textContent = 'Your last batch was sent back.';
    $('bd-gate-detail').textContent =
      `${gate.checkerNote || 'No reason given.'} Deal with it and submit again — `
      + 'closing is refused until then.';
  } else if (gate.submitted) {
    $('bd-gate-title').textContent = 'Submitted, waiting on a teammate.';
    $('bd-gate-detail').textContent =
      'Closing is refused until somebody checks it. That is deliberate, and it '
      + 'is not yours to wave through.';
  } else {
    $('bd-gate-title').textContent = `${gate.closed} tickets closed since your last tested batch.`;
    $('bd-gate-detail').textContent =
      'Test them and submit what you ran. The next close is refused until a teammate has checked it.';
  }
}

// ── testing ──────────────────────────────────────────────────────────

function batchRow(batch, checking) {
  const card = el('div', 'bd-batch');
  const head = el('div', 'bd-batch-head');
  head.append(el('span', 'account-name', checking ? batch.who.name : 'Your batch'));
  head.append(el('span', 'invite-who',
    `${plural(batch.closed, 'ticket', 'tickets')} · opened ${fmtDay(batch.openedAt)}`));
  const verdict = batch.verdict
    ? el('span', `bd-verdict ${batch.verdict}`, batch.verdict)
    : el('span', 'bd-verdict', batch.submittedAt ? 'waiting' : 'open');
  head.append(verdict);
  card.append(head);

  if (batch.tickets?.length) {
    const chips = el('div', 'bd-chips');
    for (const t of batch.tickets) {
      const chip = el('span', 'bd-touch', `#${t.key}`);
      chip.title = t.subject || '';
      chips.append(chip);
    }
    card.append(chips);
  }
  if (batch.notes) {
    card.append(el('div', 'bd-label', 'What they ran'));
    card.append(el('pre', 'bd-notes', batch.notes));
  }
  if (batch.evidence) card.append(el('pre', 'bd-notes bd-evidence', batch.evidence));
  if (batch.checkerNote) {
    card.append(el('div', 'bd-label', `${batch.verdict} by ${batch.checkedBy ?? '?'}`));
    card.append(el('p', 'auth-note', batch.checkerNote));
  }

  if (checking) {
    const note = el('input', 'auth-input', null);
    note.placeholder = 'Why — required to send it back';
    const bar = el('div', 'set-actions');
    const decide = async (verdict) => {
      say('bd-batch-error', '');
      try {
        await auth.checkBatch(batch.id, verdict, note.value);
        await loadBatches();
      } catch (error) { say('bd-batch-error', error.message); }
    };
    const pass = el('button', 'chip bd-pass', 'Passed');
    pass.type = 'button';
    pass.onclick = () => decide('passed');
    const back = el('button', 'chip bd-fail', 'Send it back');
    back.type = 'button';
    back.onclick = () => decide('failed');
    bar.append(note, pass, back);
    card.append(bar);
  }
  return card;
}

function drawBatches() {
  const mine = state.batches?.mine;
  const waiting = state.batches?.waiting ?? [];
  const every = state.batches?.every ?? 10;

  const host = $('bd-batch');
  host.replaceChildren();
  $('bd-batch-count').textContent = mine ? `${mine.closed} of ${every}` : '';
  if (!mine) {
    host.append(el('p', 'auth-note auth-fine',
      `Nothing closed yet in this batch. Testing is due every ${every} tickets.`));
  } else {
    host.append(batchRow(mine, false));
  }
  // Offered once there is something in the batch, not only once it is full:
  // testing eight and saying so is better than waiting to be stopped at ten.
  $('bd-submit').hidden = !mine || !mine.closed || mine.verdict === 'passed';

  $('bd-checking').hidden = !waiting.length;
  $('bd-waiting-count').textContent = waiting.length ? String(waiting.length) : '';
  const box = $('bd-waiting');
  box.replaceChildren(...waiting.map((b) => batchRow(b, true)));
}

// ── loading ──────────────────────────────────────────────────────────

async function loadBatches() {
  try {
    state.batches = await auth.listBatches();
    drawBatches();
  } catch (error) {
    say('bd-batch-error', error.message);
  }
}

async function load() {
  say('bd-error', '');
  try {
    state.data = await auth.myBoard();
  } catch (error) {
    // 428 is "OpenProject is not connected", which is a setup step rather than
    // a failure, and it has its own panel saying which half is missing.
    if (error.status === 428) {
      $('board').hidden = true;
      $('unconnected').hidden = false;
      $('unconnected-why').textContent = error.message;
      return;
    }
    say('bd-error', error.message);
    return;
  }
  $('unconnected').hidden = true;
  $('board').hidden = false;
  drawBoard();
  drawGate();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';

  $('bd-refresh').onclick = async () => {
    $('bd-refresh').disabled = true;
    await load();
    await loadBatches();
    $('bd-refresh').disabled = false;
  };

  $('bd-submit').onsubmit = async (event) => {
    event.preventDefault();
    say('bd-batch-error', '');
    $('bd-submit-says').textContent = '';
    try {
      await auth.submitBatch(state.batches.mine.id, $('bd-notes').value, $('bd-evidence').value);
      $('bd-notes').value = '';
      $('bd-evidence').value = '';
      $('bd-submit-says').textContent = 'Submitted. A teammate has to check it before you close another.';
      await loadBatches();
      await load();
    } catch (error) { say('bd-batch-error', error.message); }
  };

  await load();
  await loadBatches();
})();
