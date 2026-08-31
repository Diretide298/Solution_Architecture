/**
 * Every board in the package, listed from the disk.
 *
 * The rest of the viewer reaches a board *through* a screen — the Frontend
 * layer frames the board a screen's `wireframe.board` points at. That is the
 * right shape for reviewing a screen and the wrong one for reviewing the
 * drawing, because `buildWireframes` only describes boards something already
 * references. **23 of the 58 were reachable from nothing**, including the whole
 * Inventory pack and `TICVAI All Boards Index.dc.html` — 255 frame links, every
 * one of which resolves, and no way to open it.
 *
 * So this page is not a second view of the same list. It is the list the other
 * one cannot show.
 *
 * What it reports per board, and why each is worth a column:
 *
 *   frames       what is drawn
 *   named        how many of those frames anything can name. A generated board
 *                titles its own; a hand-drawn pack does not, and there only the
 *                screen pointing at a frame knows what it is. **0 named out of
 *                10 is the signature of an unmapped pack** and is the whole of
 *                the Inventory problem in one number.
 *   unclaimed    frames no screen points at — what is left of the mapping job
 *   screens      what it draws, and whether as the current board or as the
 *                generated one a client pack has since replaced
 */

import '/theme.js';   // the saved day/night choice, before anything paints
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const json = (path) => auth.apiFetch(path).then((r) => {
  if (!r.ok) throw new Error(`${path} answered ${r.status}`);
  return r.json();
});

/**
 * What each kind is, in a reader's words rather than the payload's.
 *
 * `single` and `index` exist so that "0 frames" stops reading as a fault. The
 * two `designs/` boards carry no `id` attributes at all — they are one artboard
 * each — and the index board is 255 links and no frames because it is a
 * contents page. Both are working exactly as drawn.
 */
const KINDS = {
  pack: { label: 'drawn by hand', hint: 'A design pack. The frames are somebody’s work, and the package can only name them once a screen points at each one.' },
  generated: { label: 'generated', hint: '`derive-wireframes.py` draws this from the screen definitions on every refresh, and titles every frame itself.' },
  index: { label: 'contents', hint: 'Links to other boards rather than drawing anything. No frames is correct here.' },
  single: { label: 'single artboard', hint: 'One drawing, with no frame anchors to divide it. No frames is correct here.' },
};

const bytes = (n) => (n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.round(n / 1024)} KB`);
const day = (iso) => {
  try { return new Date(iso).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }); }
  catch { return ''; }
};

const state = { boards: [], stats: null, filter: '', kind: '', sort: 'unclaimed', onlyUnwired: false };

/** Everything a filter should be able to match, flattened once per board. */
const haystack = (b) => [
  b.name, b.file, b.title, b.kind, ...b.platforms,
  ...b.screens.map((s) => `${s.id} ${s.name ?? ''}`),
  ...b.frames.map((f) => `${f.anchor} ${f.name ?? ''}`),
].join(' ').toLowerCase();

const SORTS = {
  // Unclaimed first, because that is the worklist. Ties break on frame count so
  // a big unmapped pack outranks a small one.
  unclaimed: (a, b) => b.unclaimedFrames - a.unclaimedFrames || b.frameCount - a.frameCount,
  name: (a, b) => a.name.localeCompare(b.name),
  frames: (a, b) => b.frameCount - a.frameCount,
  modified: (a, b) => String(b.modified).localeCompare(String(a.modified)),
};

function renderLead() {
  const s = state.stats;
  if (!s) return;
  $('lead').textContent =
    `${s.boards} boards, ${s.frames} frames. `
    + `${s.wired} are pointed at by a screen and ${s.unwired} are not. `
    + `${s.framesNamed} frames can be named; ${s.frames - s.framesClaimed} are claimed by no screen. `
    + `${s.screensDrawn} of the ${s.screensDrawn + s.screensGenerated} screens are drawn by a pack rather than generated.`;
  const fine = $('fine-unwired');
  if (fine) fine.textContent = String(s.unwired);
}

/** The screens a board draws, kept in two lists because they mean two things. */
function screensBlock(board) {
  const wrap = el('div', 'uiux-screens');
  const current = board.screens.filter((s) => s.via === 'board');
  const superseded = board.screens.filter((s) => s.via === 'generatedFallback');

  if (current.length) {
    wrap.append(el('span', 'uiux-screens-label', `draws ${current.length} screen${current.length === 1 ? '' : 's'}`));
    for (const s of current.slice(0, 12)) {
      const chip = el('a', 'uiux-screen', s.id);
      chip.href = `/?layer=frontend&mode=screen&id=${encodeURIComponent(s.id)}`;
      chip.title = s.name ? `${s.id} — ${s.name}` : s.id;
      wrap.append(chip);
    }
    if (current.length > 12) wrap.append(el('span', 'uiux-more', `and ${current.length - 12} more`));
  }

  if (superseded.length) {
    // `generatedFallback` is not a second way of saying "used by". It records a
    // screen that *was* drawn here and is drawn by a client pack now — the
    // generator still writes this frame on every refresh. Merging the two lists
    // would report a superseded board as current, which is the thing the field
    // was added to make visible.
    const note = el('span', 'uiux-screens-label uiux-superseded',
      `${superseded.length} screen${superseded.length === 1 ? '' : 's'} kept this as a generated fallback`);
    note.title = 'A client pack draws these now. The generator still writes these frames, so both exist and a regeneration cannot quietly remove the drawn one.';
    wrap.append(note);
  }
  return wrap;
}

function framesBlock(board) {
  const box = el('details', 'uiux-frames');
  const named = board.namedFrames;
  const sum = el('summary', null,
    `${board.frameCount} frames · ${named} named · ${board.unclaimedFrames} claimed by no screen`);
  box.append(sum);
  const list = el('div', 'uiux-frame-list');
  for (const f of board.frames) {
    const row = el('div', `uiux-frame${f.screens.length ? '' : ' is-unclaimed'}`);
    // Only the wireframes folder is served by /frame, and only a frame with an
    // anchor can be lifted out of a board at all.
    if (board.folder === 'wireframes') {
      const link = el('a', 'uiux-anchor', f.anchor);
      link.href = auth.pkgAsset(`/frame?board=${encodeURIComponent(board.file)}&anchor=${encodeURIComponent(f.anchor)}`);
      link.target = '_blank';
      link.rel = 'noopener';
      row.append(link);
    } else {
      row.append(el('span', 'uiux-anchor', f.anchor));
    }
    row.append(el('span', `uiux-frame-name${f.name ? '' : ' is-unnamed'}`,
      f.name ?? 'no screen names this frame'));
    row.append(el('span', 'uiux-frame-src', f.source === 'board' ? 'from the board'
      : f.source === 'screen' ? 'from the screen' : '—'));
    list.append(row);
  }
  box.append(list);
  return box;
}

/**
 * One board.
 *
 * The head is **two fixed rows, and neither of them wraps**. It used to be one
 * flex row holding the name, the revision, the kind and, on the 55 boards
 * nothing points at, a pill reading "nothing points at this" — which pushed the
 * pill onto a second line on most cards and a third on some, so the grid was a
 * field of cards of different heights with badges hanging off them at random.
 * Name on its own line, then one line of facts, ellipsised. A card's height now
 * varies with what is *in* the board rather than with how its title happened to
 * break.
 */
function card(board) {
  const box = el('article', `uiux-card${board.wired ? '' : ' is-unwired'}`);

  const open = el('a', 'uiux-name', board.name);
  open.href = auth.pkgAsset(board.url);
  open.target = '_blank';
  open.rel = 'noopener';
  open.title = board.file;
  box.append(open);

  if (board.title && board.title !== board.name) box.append(el('p', 'uiux-title', board.title));

  // One line, in the order a reader asks: what kind of board, who points at it,
  // how big, how recent. `nothing points at this` is a phrase rather than a
  // pill because a pill among pills reads as a category, and this is a state.
  const facts = el('p', 'uiux-facts');
  const kind = KINDS[board.kind] ?? { label: board.kind, hint: '' };
  const kindTag = el('span', `uiux-kind is-${board.kind}`, kind.label);
  kindTag.title = kind.hint;
  facts.append(kindTag);
  if (board.revision) facts.append(el('span', 'uiux-rev', board.revision));

  if (board.platforms.length) {
    facts.append(el('span', 'uiux-plat', board.platforms.join(' · ')));
  } else if (!board.wired) {
    const warn = el('span', 'uiux-unwired', 'nothing points at this');
    warn.title = 'No screen names this board, so it appears nowhere else in the viewer.';
    facts.append(warn);
  }
  facts.append(el('span', 'uiux-dim', `${bytes(board.bytes)} · ${day(board.modified)}`));
  box.append(facts);

  if (board.screens.length) box.append(screensBlock(board));
  if (board.frameCount) box.append(framesBlock(board));
  else if (board.kind === 'index') {
    box.append(el('p', 'uiux-note', `${board.links} links to other boards. Open it — it is the catalogue.`));
  }
  return box;
}

function draw() {
  const box = $('boards');
  box.textContent = '';
  const needle = state.filter.trim().toLowerCase();

  let shown = state.boards
    .filter((b) => !state.kind || b.kind === state.kind)
    .filter((b) => !state.onlyUnwired || !b.wired)
    .filter((b) => !needle || haystack(b).includes(needle));
  shown = [...shown].sort(SORTS[state.sort] ?? SORTS.unclaimed);

  if (!shown.length) {
    box.append(el('p', 'plat-none', 'No board matches that.'));
    return;
  }

  // Grouped by folder, and the heading says how many of the whole this is —
  // a count with no denominator beside a filter box is a number that lies.
  for (const folder of state.folders) {
    const mine = shown.filter((b) => b.folder === folder.id);
    if (!mine.length) continue;
    const label = mine.length === folder.count
      ? `${folder.label} — ${folder.count}`
      : `${folder.label} — ${mine.length} of ${folder.count}`;
    box.append(el('h2', 'uiux-folder', label));
    const grid = el('div', 'uiux-grid');
    for (const b of mine) grid.append(card(b));
    box.append(grid);
  }
}

(async () => {
  await auth.requireSignIn();

  const me = auth.account();
  // Optional: inside the viewer these views are sections of a page that
  // already says who you are, so there is no `#whoami` to fill.
  $('whoami')?.replaceChildren(me ? `${me.name || me.email} · ${me.role}` : '');

  let uiux;
  try {
    uiux = await json('/api/uiux');
  } catch (error) {
    hideLoader();
    $('lead').textContent = `Could not read the package: ${error.message}`;
    return;
  }

  if (!uiux?.present) {
    hideLoader();
    $('lead').textContent = 'This package has no wireframes/ or designs/ directory.';
    return;
  }

  state.boards = uiux.boards ?? [];
  state.folders = (uiux.folders ?? []).filter((f) => f.present && f.count);
  state.stats = uiux.stats;

  renderLead();
  draw();
  hideLoader();

  $('filter').oninput = (e) => { state.filter = e.target.value; draw(); };
  $('kind').onchange = (e) => { state.kind = e.target.value; draw(); };
  $('sort').onchange = (e) => { state.sort = e.target.value; draw(); };
  $('only-unwired').onchange = (e) => { state.onlyUnwired = e.target.checked; draw(); };
})();
