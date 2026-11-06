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
// The shared frame: on a phone, the app bar and the bottom bar every page has.
import '/page-chrome.js';

// Asked for at the top, beside the sign-in check rather than after it (13
// October). Anybody but the System Architect is refused it, and is shown the
// refusal below without this answer ever being read.
const firstPlan = auth.readPlan(auth.project());
firstPlan.catch(() => { /* answered by load(), or refused */ });

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const ZOOMS = { week: 28, month: 8, quarter: 3 };
const ROW_H = 38;

// A phone reads the plan and does not change it (decided with the lead, 4
// November): below 720px a bar opens a sheet with its dates instead of being
// dragged, and the editing controls are hidden by plan.css. A tablet or a
// laptop with a touch screen keeps the drag.
const phone = matchMedia('(max-width: 719px)');

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
      + (phone.matches ? 'Shows its dates.'
        : 'Arrow keys move it, shift and arrow keys change its length.'));
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
  // Only the filter can empty a chart that has dated modules (draw() says the
  // rest in the page's own empty state), so this line names the filter.
  $('pl-empty').hidden = on.length > 0;
  if (!on.length) {
    $('pl-empty').textContent = 'Every module with dates is finished. Untick Hide finished modules to see them.';
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
    // On a phone the finger scrolls the chart; nothing is dragged.
    if (phone.matches) return;
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
  block.addEventListener('click', () => { if (phone.matches) openBar(module, block); });

  block.addEventListener('keydown', (event) => {
    if (phone.matches) {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); openBar(module, block); }
      return;
    }
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
  // Nothing has dates at all: no axis to draw, so the page says why instead.
  const all = state.data?.modules ?? [];
  const datedAny = all.some(dated);
  $('pl-chart-panel').hidden = !datedAny;
  for (const n of $('pl-toolbar').querySelectorAll('.pl-zoom, .pl-switch')) n.hidden = !datedAny;
  // With no chart the toolbar has nothing to offer a desk (Refresh is in the
  // header there); a phone keeps it for its own Refresh.
  if (state.data) $('pl-toolbar').hidden = !datedAny && !phone.matches;
  if (!datedAny) {
    const n = all.length;
    showState('empty', n ? 'No module has dates yet' : 'There are no modules yet',
      n
        ? `A bar is a top-level ticket in OpenProject, drawn from its own start and finish, or else from the `
          + `earliest start and latest finish of the tickets under it. None of the ${n} module${n === 1 ? '' : 's'} `
          + `here has either yet, so there is nothing to draw. `
          + (phone.matches
            ? 'Give them dates in OpenProject, or place them on a larger screen.'
            : 'Put one on the chart from the list below to give it a fortnight from today, or give it dates in OpenProject.')
        : (state.data?.note || 'The OpenProject project has no top-level tickets, so there is nothing to draw.'));
  } else {
    showState(null);
  }
  const win = window_();
  drawAxis(win);
  drawRows(win);
  drawUndated();
  drawToolbar();
  showToday(win);
}

// On a phone the chart opens on today rather than on its first day, a third of
// the way in, so what is just behind is still in sight. Once per zoom, so a
// redraw does not pull the chart back from where somebody slid it.
let todayShownAt = '';
function showToday(win) {
  if (!phone.matches || todayShownAt === state.zoom) return;
  const scroller = $('pl-scroll');
  if (!scroller.clientWidth) return;
  todayShownAt = state.zoom;
  scroller.scrollLeft = Math.max(0, (TODAY - win.from) * pxPerDay() - scroller.clientWidth / 3);
}

// ── a bar's dates, on a phone ────────────────────────────────────────

let sheetFrom = null;
let sheetTimer = 0;

function showLoadFailure(title, text, retry) {
  $('plan').hidden = false;
  $('pl-chart-panel').hidden = true;
  $('pl-toolbar').hidden = true;
  $('pl-undated-panel').hidden = true;
  showState('error', title, text, retry);
}

function openBar(module, block) {
  const bar = barOf(module);
  let from = dayOf(bar.start);
  let to = dayOf(bar.due);
  if (from == null) from = to - 13;
  if (to == null) to = from + 13;
  const days = to - from + 1;
  $('pl-sheet-key').textContent = `#${module.key}${module.type ? ` · ${module.type}` : ''}`;
  $('pl-sheet-title').textContent = module.subject;

  // Where the bar sits against the whole chart, drawn small, so the sheet still
  // reads as the bar that was tapped.
  const win = window_();
  const range = win.to - win.from;
  const span = $('pl-sheet-span').firstElementChild;
  span.style.left = `${((from - win.from) / range) * 100}%`;
  span.style.width = `${Math.max(2, (days / range) * 100)}%`;
  span.className = ['is-moved', 'is-done', 'is-derived'].filter((c) => block.classList.contains(c)).join(' ');
  $('pl-sheet-span').style.setProperty('--now', `${((TODAY - win.from) / range) * 100}%`);

  const facts = [
    ['Starts', readable(isoOf(from))],
    ['Finishes', readable(isoOf(to))],
    ['Length', `${days} day${days === 1 ? '' : 's'}${days >= 14 ? `, about ${Math.round(days / 7)} weeks` : ''}`],
    ['Tickets', module.children ? `${module.openChildren} open of ${module.children}` : 'None underneath'],
  ];
  if (module.percent != null) facts.push(['Finished', `${module.percent}%`]);
  facts.push(['Dates set by', module.scheduleManually ? 'Hand, in OpenProject' : 'OpenProject, from its children']);
  $('pl-sheet-facts').replaceChildren(...facts.flatMap(([term, value]) => [el('dt', null, term), el('dd', null, value)]));

  const moved = state.moved.has(module.key);
  $('pl-sheet-note').hidden = !moved;
  $('pl-sheet-note').textContent = moved
    ? `Moved in your sketch and not yet sent. OpenProject still has ${readable(module.barStart)} to ${readable(module.barDue)}.`
    : '';
  $('pl-sheet-open').href = module.url || '#';
  $('pl-sheet-open').hidden = !module.url;

  clearTimeout(sheetTimer);
  sheetFrom = block.dataset.key;
  const sheet = $('pl-sheet');
  sheet.style.transform = '';
  $('pl-scrim').hidden = false;
  sheet.hidden = false;
  for (const id of ['plan', 'denied', 'unconnected']) $(id).inert = true;
  for (const n of document.querySelectorAll('.admin-bar, .phone-tabbar')) n.setAttribute('inert', '');
  // Two frames: one to lay the sheet out below the screen, one to slide it up.
  requestAnimationFrame(() => requestAnimationFrame(() => {
    $('pl-scrim').classList.add('is-open');
    sheet.classList.add('is-open');
  }));
  $('pl-sheet-title').focus({ preventScroll: true });
}

function closeBar() {
  const sheet = $('pl-sheet');
  if (sheet.hidden) return;
  $('pl-scrim').classList.remove('is-open');
  sheet.classList.remove('is-open');
  sheet.style.transform = '';
  for (const id of ['plan', 'denied', 'unconnected']) $(id).inert = false;
  for (const n of document.querySelectorAll('.admin-bar, .phone-tabbar')) n.removeAttribute('inert');
  const done = () => { $('pl-scrim').hidden = true; sheet.hidden = true; };
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) done();
  else sheetTimer = setTimeout(done, 280);
  const back = sheetFrom && document.querySelector(`.pl-bar[data-key="${CSS.escape(sheetFrom)}"]`);
  back?.focus({ preventScroll: true });
  sheetFrom = null;
}

/** The sheet's ways out: Done, the scrim, Escape, and pulling it down by its top. */
function mountSheet() {
  const sheet = $('pl-sheet');
  $('pl-scrim').onclick = closeBar;
  $('pl-sheet-close').onclick = closeBar;
  document.addEventListener('keydown', (event) => {
    if (sheet.hidden) return;
    if (event.key === 'Escape') closeBar();
    // Focus stays inside the sheet while it is open.
    if (event.key === 'Tab') {
      const stops = [...sheet.querySelectorAll('button, a[href]')].filter((n) => !n.hidden);
      const first = stops[0];
      const last = stops.at(-1);
      const at = document.activeElement;
      if (event.shiftKey && (at === first || at === $('pl-sheet-title'))) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && at === last) { event.preventDefault(); first.focus(); }
    }
  });
  let startY = null;
  let pulled = 0;
  sheet.addEventListener('pointerdown', (event) => {
    // Only by the grip and the heading, so the facts below can still scroll.
    if (!event.target.closest('.pl-sheet-grip, .pl-sheet-key, .pl-sheet-title')) return;
    startY = event.clientY;
    pulled = 0;
    sheet.setPointerCapture(event.pointerId);
    sheet.classList.add('is-pulling');
  });
  sheet.addEventListener('pointermove', (event) => {
    if (startY == null) return;
    pulled = Math.max(0, event.clientY - startY);
    sheet.style.transform = `translateY(${pulled}px)`;
  });
  const release = () => {
    if (startY == null) return;
    startY = null;
    sheet.classList.remove('is-pulling');
    if (pulled > 80) closeBar();
    else sheet.style.transform = '';
  };
  sheet.addEventListener('pointerup', release);
  sheet.addEventListener('pointercancel', release);
  // Turning the phone, or a window resized past the breakpoint: the drag comes
  // back on the wider side, and the bars' labels say which it is.
  phone.addEventListener('change', () => { closeBar(); todayShownAt = ''; if (state.data) draw(); });
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

// A Refresh is answered at once with the read the service holds, marked
// `refreshing` while a newer one is read behind it. The page asks again every
// ten seconds until it is in, and only then draws the chart again: drawing the
// same bars every ten seconds would reset a bar somebody is in the middle of
// dragging, for nothing.
let asking = 0;
const ASK_MS = 10_000;

function askAgain(asOf) {
  clearTimeout(asking);
  asking = setTimeout(async () => {
    let next;
    try { next = await auth.readPlan(auth.project()); } catch { return; }
    if (next.asOf !== asOf) return load(false, Promise.resolve(next));
    if (next.refreshing) return askAgain(asOf);
    if (next.refreshError) say('pl-error', `Could not refresh: ${next.refreshError}`);
    $('pl-asof').textContent = $('pl-asof').textContent.replace(/ · refreshing…$/, '');
  }, ASK_MS);
}

/** The page's one message when there is no chart: loading, empty or failed.
 *  `kind` null puts it away. */
function showState(kind, title = '', text = '', retry = false) {
  const box = $('pl-state');
  box.hidden = !kind;
  if (!kind) return;
  box.dataset.kind = kind;
  box.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  $('pl-state-title').textContent = title;
  $('pl-state-text').textContent = text;
  $('pl-state-retry').hidden = !retry;
}

/** "2 days ago", not "197741s ago". */
function ago(seconds) {
  const n = (count, unit) => `${count} ${unit}${count === 1 ? '' : 's'} ago`;
  if (seconds < 60) return 'under a minute ago';
  if (seconds < 3600) return n(Math.round(seconds / 60), 'minute');
  if (seconds < 86400) return n(Math.round(seconds / 3600), 'hour');
  return n(Math.round(seconds / 86400), 'day');
}

async function load(refresh = false, answer = null) {
  clearTimeout(asking);
  try {
    state.data = await (answer ?? auth.readPlan(auth.project(), { refresh }));
  } catch (error) {
    if (error.status === 428) {
      $('plan').hidden = true;
      $('unconnected').hidden = false;
      $('unconnected-why').textContent = error.message;
      return;
    }
    if (error.status === 503) {
      // The first read of a big project, still running on the server. It goes
      // on without this page; asking again is the whole of the fix.
      if (state.data) say('pl-error', `${error.message} Checking again in a few seconds…`);
      else showLoadFailure('OpenProject is still being read', `${error.message} This page checks again every ten seconds.`, false);
      asking = setTimeout(() => load(), ASK_MS);
      return;
    }
    // With a chart already drawn, the line above it says what went wrong and
    // the chart stays. With nothing drawn yet, the error was going into a page
    // that was still hidden, and the page was blank (the lead's phone, 5 Nov).
    if (state.data) say('pl-error', error.message);
    else {
      const said = String(error.message ?? '').trim();
      const why = !said || /^\d+$/.test(said)
        ? `ADAM answered ${error.status ?? said ?? 'nothing'} when asked for the plan`
        : said.replace(/\.$/, '');
      showLoadFailure('The plan could not be read',
        `${why}. Nothing was changed. Try again; if it keeps failing, the ADAM server needs a look.`, true);
    }
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
      + (state.data.ageSeconds ? ` · ${ago(state.data.ageSeconds)}` : '')
      + (state.data.truncated ? ' · more modules than this chart shows' : '')
      + (state.data.refreshing ? ' · refreshing…' : '')
    : '';
  if (state.data.refreshing) askAgain(state.data.asOf);
  draw();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';
  // The page hides itself, and every route it calls refuses anybody else. Both,
  // because one of them is presentation and the other is the rule.
  if (!auth.isOwner(me)) { $('denied').hidden = false; return; }

  // The page is shown at once, saying it is reading, rather than blank until
  // the plan arrives.
  $('plan').hidden = false;
  $('pl-chart-panel').hidden = true;
  $('pl-toolbar').hidden = true;
  showState('loading', 'Reading the plan', 'Every module and its dates, from OpenProject.');
  $('pl-state-retry').onclick = () => {
    showState('loading', 'Reading the plan', 'Every module and its dates, from OpenProject.');
    load();
  };

  for (const button of $('pl-toolbar').querySelectorAll('[data-zoom]')) {
    button.onclick = () => { state.zoom = button.dataset.zoom; draw(); };
  }
  $('pl-hide-done').onchange = () => { state.hideDone = $('pl-hide-done').checked; draw(); };
  $('pl-refresh').onclick = async () => {
    $('pl-refresh').disabled = true;
    $('pl-refresh-phone').disabled = true;
    await load(true);
    $('pl-refresh').disabled = false;
    $('pl-refresh-phone').disabled = false;
  };
  // The header's buttons give way to the phone's app bar, so a phone has its
  // own Refresh in the toolbar. Same action.
  $('pl-refresh-phone').onclick = () => $('pl-refresh').click();
  $('pl-discard').onclick = async () => {
    try { await auth.clearPlanDraft(auth.project()); await load(); }
    catch (error) { say('pl-error', error.message); }
  };
  $('pl-ship').onclick = openShip;
  $('pl-cancel').onclick = () => { $('pl-veil').hidden = true; state.proposal = null; };
  $('pl-confirm').onclick = confirmShip;
  mountSheet();
  $('pl-veil').onclick = (event) => {
    if (event.target === $('pl-veil')) { $('pl-veil').hidden = true; state.proposal = null; }
  };

  await load(false, firstPlan);
})();
