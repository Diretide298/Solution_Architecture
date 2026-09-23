/**
 * The delivery as bars on a time axis, dragged by hand, shipped on confirm.
 *
 * **A sketch that knows it is a sketch.** Dragging a bar changes nothing
 * anywhere: it writes to `plan_draft`, which is private to one account and is
 * emptied by the only thing that can send it — the confirm. So the chart and
 * OpenProject are allowed to disagree for as long as somebody is thinking, and
 * the moment they stop disagreeing is a moment somebody chose.
 *
 * **Dates are days, and days are not milliseconds.** Every position on this
 * chart is a whole number of days from an epoch, computed from the ISO date
 * string rather than from a Date. `new Date('2026-03-19')` is midnight UTC,
 * which in a timezone behind it is the 18th — and a chart that reads a day
 * earlier than the ticket it draws is worse than no chart. `dayOf` parses the
 * three numbers and does the arithmetic itself, so nothing here has a timezone
 * at all.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const ZOOMS = { week: 28, month: 8, quarter: 3 };
const ROW_H = 38;

const state = {
  data: null,
  zoom: 'month',
  hideDone: false,
  // key -> {start, due}: what this screen believes, draft included. The bars
  // are drawn from here, and the server is told about it after a drag settles.
  bars: new Map(),
  moved: new Set(),
  saving: null,
  proposal: null,
};

function say(id, message) {
  $(id).textContent = message ?? '';
  $(id).hidden = !message;
}

// ── days, without a timezone anywhere ────────────────────────────────

/** An ISO date as a day number. Null for a blank, which is a real value here. */
function dayOf(iso) {
  if (!iso) return null;
  const parts = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso);
  if (!parts) return null;
  return Math.floor(Date.UTC(+parts[1], +parts[2] - 1, +parts[3]) / 86400000);
}

/** Back the other way. Date.UTC and getUTC* only, so the round trip is exact. */
function isoOf(day) {
  if (day == null) return '';
  const at = new Date(day * 86400000);
  const pad = (n) => String(n).padStart(2, '0');
  return `${at.getUTCFullYear()}-${pad(at.getUTCMonth() + 1)}-${pad(at.getUTCDate())}`;
}

const TODAY = dayOf(new Date().toISOString().slice(0, 10));

const readable = (iso) => {
  if (!iso) return 'unset';
  const at = new Date(`${iso}T00:00:00Z`);
  return at.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' });
};

// ── what is on the chart ─────────────────────────────────────────────

/** Every module, with the dragged position winning over the stored one. */
function modules() {
  const all = state.data?.modules ?? [];
  return all.filter((m) => !(state.hideDone && m.openChildren === 0 && m.percent === 100));
}

const barOf = (m) => state.bars.get(m.key) ?? { start: m.barStart, due: m.barDue };
const dated = (m) => { const b = barOf(m); return b.start || b.due; };

/** The window the axis covers: everything drawn, plus a margin, plus today.
 *
 *  Today is included deliberately. A plan entirely in the future draws with no
 *  "now" line, and a chart whose only reference point is itself is one you can
 *  read for a while before noticing the whole thing has slipped. */
function window_() {
  const days = [TODAY];
  for (const m of modules()) {
    const b = barOf(m);
    const s = dayOf(b.start);
    const d = dayOf(b.due);
    if (s != null) days.push(s);
    if (d != null) days.push(d);
  }
  const from = Math.min(...days) - 7;
  const to = Math.max(...days) + 7;
  // A single-day plan would divide by zero below.
  return { from, to: Math.max(to, from + 14) };
}

const pxPerDay = () => ZOOMS[state.zoom];

// ── the axis ─────────────────────────────────────────────────────────

function drawAxis(win) {
  const axis = $('pl-axis');
  axis.replaceChildren();
  const per = pxPerDay();
  axis.style.width = `${(win.to - win.from) * per}px`;

  // One tick per month at the two wider zooms, one per week at the closest.
  // Ticks every day at any zoom is a grey block, not an axis.
  const ticks = [];
  if (state.zoom === 'week') {
    // Mondays. 1970-01-01 was a Thursday, so +4 lands the modulo on Monday.
    let day = win.from + ((11 - ((win.from + 4) % 7)) % 7);
    for (; day <= win.to; day += 7) ticks.push({ day, label: readable(isoOf(day)).replace(/,.*/, '') });
  } else {
    const first = new Date(win.from * 86400000);
    let cursor = Date.UTC(first.getUTCFullYear(), first.getUTCMonth(), 1);
    for (let guard = 0; guard < 200; guard += 1) {
      const day = Math.floor(cursor / 86400000);
      if (day > win.to) break;
      if (day >= win.from) {
        const at = new Date(cursor);
        ticks.push({
          day,
          label: at.toLocaleDateString(undefined, { month: 'short', year: '2-digit', timeZone: 'UTC' }),
        });
      }
      const at = new Date(cursor);
      cursor = Date.UTC(at.getUTCFullYear(), at.getUTCMonth() + 1, 1);
    }
  }

  for (const tick of ticks) {
    const mark = el('div', 'pl-tick', tick.label);
    mark.style.left = `${(tick.day - win.from) * per}px`;
    axis.append(mark);
  }

  const now = el('div', 'pl-now');
  now.style.left = `${(TODAY - win.from) * per}px`;
  now.title = `Today — ${readable(isoOf(TODAY))}`;
  axis.append(now);
}

// ── the bars ─────────────────────────────────────────────────────────

function drawRows(win) {
  const rows = $('pl-rows');
  rows.replaceChildren();
  const per = pxPerDay();
  const width = (win.to - win.from) * per;
  const on = modules().filter(dated);

  rows.style.width = `${width}px`;
  rows.style.height = `${Math.max(on.length, 1) * ROW_H}px`;

  const nowLine = el('div', 'pl-now pl-now-full');
  nowLine.style.left = `${(TODAY - win.from) * per}px`;
  rows.append(nowLine);

  on.forEach((module, index) => {
    const bar = barOf(module);
    // A module with one end missing still gets drawn: a fortnight anchored on
    // whichever end it has. Refusing to draw it would hide work, and pretending
    // it is a point would put a one-pixel sliver on the chart nobody can grab.
    let from = dayOf(bar.start);
    let to = dayOf(bar.due);
    if (from == null) from = to - 13;
    if (to == null) to = from + 13;
    if (to < from) to = from;

    const lane = el('div', 'pl-lane');
    lane.style.top = `${index * ROW_H}px`;
    lane.style.width = `${width}px`;
    rows.append(lane);

    const block = el('div', 'pl-bar');
    block.dataset.key = module.key;
    block.style.top = `${index * ROW_H + 6}px`;
    block.style.left = `${(from - win.from) * per}px`;
    block.style.width = `${Math.max((to - from + 1) * per, 12)}px`;
    if (state.moved.has(module.key)) block.classList.add('is-moved');
    if (module.percent === 100) block.classList.add('is-done');
    if (!module.scheduleManually) block.classList.add('is-derived');

    block.tabIndex = 0;
    block.setAttribute('role', 'button');
    block.setAttribute('aria-label',
      `${module.subject}, ${readable(isoOf(from))} to ${readable(isoOf(to))}. `
      + 'Arrow keys move it, shift and arrow keys change its length.');
    block.title = [
      `#${module.key} — ${module.subject}`,
      `${readable(isoOf(from))} → ${readable(isoOf(to))} (${to - from + 1} days)`,
      module.children ? `${module.children} tickets, ${module.openChildren} open` : 'no tickets underneath',
      module.scheduleManually ? '' : 'OpenProject schedules this one from its children — '
        + 'moving it will switch it to manual scheduling.',
    ].filter(Boolean).join('\n');

    if (module.percent != null && module.percent > 0) {
      const done = el('div', 'pl-bar-done');
      done.style.width = `${Math.min(100, module.percent)}%`;
      block.append(done);
    }
    block.append(el('span', 'pl-bar-label', `${module.subject}`));
    block.append(el('span', 'pl-grip pl-grip-start'));
    block.append(el('span', 'pl-grip pl-grip-end'));

    grab(block, module, win);
    rows.append(block);
  });

  drawNames(on);
  $('pl-empty').hidden = on.length > 0;
  if (!on.length) {
    $('pl-empty').textContent = state.data?.note
      ?? 'Nothing here has dates yet, so there is nothing to arrange.';
  }
}

/** The names, in a column that does not scroll sideways with the chart. */
function drawNames(on) {
  const names = $('pl-names');
  names.replaceChildren();
  names.style.height = `${Math.max(on.length, 1) * ROW_H + 30}px`;
  names.append(el('div', 'pl-names-head', 'Module'));
  on.forEach((module) => {
    const row = el('div', 'pl-name');
    row.style.height = `${ROW_H}px`;
    const link = el('a', 'pl-name-text', module.subject);
    link.href = module.url || '#';
    link.target = '_blank';
    link.rel = 'noreferrer';
    link.title = `#${module.key} — open in OpenProject`;
    row.append(link);
    row.append(el('span', 'pl-name-count',
      module.children ? `${module.openChildren}/${module.children}` : '—'));
    names.append(row);
  });
}

// ── dragging ─────────────────────────────────────────────────────────

/** Move and resize, on one pointer and one keyboard handler.
 *
 *  The drag works in day deltas rather than pixels-then-convert: the pointer
 *  movement is divided by the day width and rounded once, so a bar lands on a
 *  whole day every time and a slow drag across two pixels does not creep. */
function grab(block, module, win) {
  const per = pxPerDay();

  const begin = (event) => {
    if (event.button != null && event.button !== 0) return;
    const edge = event.target.classList.contains('pl-grip-start') ? 'start'
      : event.target.classList.contains('pl-grip-end') ? 'end' : 'move';
    const bar = barOf(module);
    let from = dayOf(bar.start);
    let to = dayOf(bar.due);
    if (from == null) from = to - 13;
    if (to == null) to = from + 13;
    const originX = event.clientX;
    block.setPointerCapture(event.pointerId);
    block.classList.add('is-dragging');

    const move = (at) => {
      const days = Math.round((at.clientX - originX) / per);
      let start = from;
      let due = to;
      if (edge === 'move') { start = from + days; due = to + days; }
      // A bar cannot be dragged inside out. Clamping rather than swapping: a
      // person pulling the left edge past the right means "make it short",
      // not "reverse it".
      if (edge === 'start') start = Math.min(from + days, to);
      if (edge === 'end') due = Math.max(to + days, from);
      block.style.left = `${(start - win.from) * per}px`;
      block.style.width = `${Math.max((due - start + 1) * per, 12)}px`;
      block.dataset.start = isoOf(start);
      block.dataset.due = isoOf(due);
    };

    const end = () => {
      block.releasePointerCapture(event.pointerId);
      block.classList.remove('is-dragging');
      block.removeEventListener('pointermove', move);
      block.removeEventListener('pointerup', end);
      block.removeEventListener('pointercancel', end);
      const start = block.dataset.start;
      const due = block.dataset.due;
      if (start && due) place(module, start, due);
      else draw();
    };

    block.addEventListener('pointermove', move);
    block.addEventListener('pointerup', end);
    block.addEventListener('pointercancel', end);
    event.preventDefault();
  };

  block.addEventListener('pointerdown', begin);

  block.addEventListener('keydown', (event) => {
    const step = event.key === 'ArrowLeft' ? -1 : event.key === 'ArrowRight' ? 1 : 0;
    if (!step) return;
    event.preventDefault();
    const bar = barOf(module);
    let from = dayOf(bar.start);
    let to = dayOf(bar.due);
    if (from == null) from = to - 13;
    if (to == null) to = from + 13;
    // Shift stretches the finish; on its own it moves the whole bar. The same
    // two gestures the pointer has, for somebody who is not using one.
    if (event.shiftKey) place(module, isoOf(from), isoOf(Math.max(to + step, from)));
    else place(module, isoOf(from + step), isoOf(to + step));
  });
}

/** Where a bar now is. Optimistic on screen, then told to the service. */
function place(module, start, due) {
  state.bars.set(module.key, { start, due });
  const back = start === module.barStart && due === module.barDue;
  if (back) state.moved.delete(module.key);
  else state.moved.add(module.key);
  draw();
  const focused = document.querySelector(`.pl-bar[data-key="${CSS.escape(module.key)}"]`);
  if (focused && document.activeElement?.dataset?.key === module.key) focused.focus();
  save();
}

// A drag produces a burst of these. One request per burst rather than one per
// pixel, and the last state wins — the draft is a position, not a history.
let pending = null;
function save() {
  clearTimeout(pending);
  pending = setTimeout(async () => {
    const bars = [...state.bars.entries()].map(([key, b]) => ({ key, start: b.start, due: b.due }));
    if (!bars.length) return;
    try {
      const said = await auth.savePlanDraft(auth.project(), bars);
      state.saving = null;
      say('pl-error', '');
      drawToolbar(said.draftCount);
    } catch (error) {
      say('pl-error', `That move was not saved: ${error.message}`);
    }
  }, 350);
}

// ── the toolbar, and what it says about the sketch ───────────────────

function drawToolbar(count) {
  const moved = count ?? state.moved.size;
  $('pl-dirty').hidden = !moved;
  $('pl-dirty').textContent = moved
    ? `${moved} module${moved === 1 ? '' : 's'} moved, not yet sent`
    : '';
  $('pl-discard').hidden = !moved;
  $('pl-ship').hidden = !moved;
  for (const button of $('pl-toolbar').querySelectorAll('[data-zoom]')) {
    button.classList.toggle('is-on', button.dataset.zoom === state.zoom);
  }
}

// ── modules with no dates at all ─────────────────────────────────────

function drawUndated() {
  const none = modules().filter((m) => !dated(m));
  $('pl-undated-panel').hidden = !none.length;
  $('pl-undated-count').textContent = none.length ? String(none.length) : '';
  const box = $('pl-undated');
  box.replaceChildren();
  for (const module of none) {
    const row = el('div', 'admin-row pl-undated-row');
    row.append(el('span', 'pl-name-text', module.subject));
    row.append(el('span', 'auth-fine', `#${module.key} · ${module.children} tickets`));
    const go = el('button', 'chip', 'Put it on the chart');
    go.type = 'button';
    go.onclick = () => place(module, isoOf(TODAY), isoOf(TODAY + 13));
    row.append(go);
    box.append(row);
  }
}

// ── drawing the lot ──────────────────────────────────────────────────

function draw() {
  const win = window_();
  drawAxis(win);
  drawRows(win);
  drawUndated();
  drawToolbar();
}

// ── shipping ─────────────────────────────────────────────────────────

async function openShip() {
  say('pl-dialog-error', '');
  $('pl-dialog-list').replaceChildren();
  $('pl-dialog-lede').textContent = 'Reading every ticket again…';
  $('pl-veil').hidden = false;
  $('pl-confirm').disabled = true;
  try {
    const preview = await auth.previewPlan(auth.project());
    state.proposal = preview.proposal;
    const n = preview.changes.length;
    $('pl-dialog-lede').textContent =
      `${n} module${n === 1 ? '' : 's'} will be given new dates in OpenProject, `
      + 'as you, from your own OpenProject account.';
    for (const change of preview.changes) {
      const row = el('div', 'admin-row');
      const link = el('a', 'pl-name-text', change.subject);
      link.href = change.url;
      link.target = '_blank';
      link.rel = 'noreferrer';
      row.append(link);
      row.append(el('span', 'pl-said', change.said));
      $('pl-dialog-list').append(row);
    }
    const manual = preview.becomingManual;
    $('pl-dialog-manual').hidden = !manual;
    $('pl-dialog-manual').textContent = manual
      ? `${manual} of these are scheduled by OpenProject from their children today. `
        + 'Giving them dates switches them to manual scheduling, so they will stop '
        + 'moving on their own when the tickets underneath them move.'
      : '';
    $('pl-dialog-skipped').hidden = !preview.skipped?.length;
    $('pl-dialog-skipped').textContent = (preview.skipped ?? []).join(' ');
    $('pl-confirm').disabled = false;
  } catch (error) {
    $('pl-dialog-lede').textContent = '';
    say('pl-dialog-error', error.message);
  }
}

async function confirmShip() {
  $('pl-confirm').disabled = true;
  try {
    const said = await auth.shipPlan(auth.project(), state.proposal);
    $('pl-veil').hidden = true;
    state.proposal = null;
    await load(true);
    say('pl-error', said.failed?.length
      ? `${said.note} ${said.failed.map((f) => f.why).join(' ')}`
      : '');
  } catch (error) {
    say('pl-dialog-error', error.message);
    $('pl-confirm').disabled = false;
  }
}

// ── loading ──────────────────────────────────────────────────────────

async function load(refresh = false) {
  try {
    state.data = await auth.readPlan(auth.project(), { refresh });
  } catch (error) {
    if (error.status === 428) {
      $('plan').hidden = true;
      $('unconnected').hidden = false;
      $('unconnected-why').textContent = error.message;
      return;
    }
    say('pl-error', error.message);
    return;
  }
  state.bars.clear();
  state.moved.clear();
  for (const module of state.data.modules) {
    if (!module.draft) continue;
    state.bars.set(module.key, { start: module.draft.start, due: module.draft.due });
    state.moved.add(module.key);
  }
  $('plan').hidden = false;
  $('pl-asof').textContent = state.data.asOf
    ? `OpenProject read ${new Date(state.data.asOf).toLocaleString()}`
      + (state.data.ageSeconds ? ` · ${state.data.ageSeconds}s ago` : '')
      + (state.data.truncated ? ' · more modules than this chart shows' : '')
    : '';
  draw();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';
  // The page hides itself, and every route it calls refuses anybody else. Both,
  // because one of them is presentation and the other is the rule.
  if (!auth.isOwner(me)) { $('denied').hidden = false; return; }

  for (const button of $('pl-toolbar').querySelectorAll('[data-zoom]')) {
    button.onclick = () => { state.zoom = button.dataset.zoom; draw(); };
  }
  $('pl-hide-done').onchange = () => { state.hideDone = $('pl-hide-done').checked; draw(); };
  $('pl-refresh').onclick = async () => {
    $('pl-refresh').disabled = true;
    await load(true);
    $('pl-refresh').disabled = false;
  };
  $('pl-discard').onclick = async () => {
    try { await auth.clearPlanDraft(auth.project()); await load(); }
    catch (error) { say('pl-error', error.message); }
  };
  $('pl-ship').onclick = openShip;
  $('pl-cancel').onclick = () => { $('pl-veil').hidden = true; state.proposal = null; };
  $('pl-confirm').onclick = confirmShip;
  $('pl-veil').onclick = (event) => {
    if (event.target === $('pl-veil')) { $('pl-veil').hidden = true; state.proposal = null; }
  };

  await load();
})();
