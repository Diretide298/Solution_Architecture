/**
 * The board workbench — every board in the package, read off the disk.
 *
 * The rest of the viewer reaches a board *through* a screen: the Frontend layer
 * frames whatever a screen's `wireframe.board` points at. That is the right
 * shape for reviewing a screen and the wrong one for reviewing the drawing,
 * because `buildWireframes` only describes boards something already references.
 * A large minority of them are reachable from nothing at all — whole hand-drawn
 * packs, and `TICVAI All Boards Index.dc.html`, which is 255 frame links every
 * one of which resolves and which nothing in the viewer could open.
 *
 * So this is not a second view of the same list. It is the list the other one
 * cannot show.
 *
 * ── why three columns ─────────────────────────────────────────────────
 *
 * This was a filter box over a masonry of cards, and it answered "what boards
 * are there" well enough. It could not answer the question a reader actually
 * arrives with — *which frames does nothing claim, and where are they* —
 * because a board's frames were folded inside its own card and the only way to
 * compare two boards was to open both and scroll.
 *
 * The rail on the left is the worklist: the folders, the boards nothing points
 * at, and the platforms with no hand-drawn pack. The middle is what is drawn.
 * The right is the one board you picked, in full.
 *
 * ── the three middle views ────────────────────────────────────────────
 *
 *   Map     one tile per board, one chip per frame. The chips are the point:
 *           a board's mapping state is a colour you can read across a
 *           hundred boards at once, and "0 named of 10" — the signature of an
 *           unmapped pack — is a tile of hollow squares.
 *   List    the reading view, a card per board with its screens and frames.
 *   Frames  the flat worklist. Every frame, every board, one row each.
 *
 * ── on tile size ──────────────────────────────────────────────────────
 *
 * The tiles are all the same size and deliberately so. Sizing a tile by how
 * much it draws is the more informative layout and it is unreadable: it packs
 * into a ragged wall where a row of four is four different shapes, and the eye
 * spends its effort on the mosaic rather than on the colours inside it. Every
 * tile is one board, so every tile is one size, and the quantity a reader wants
 * — how much is drawn, how much is claimed — is in the chips and in the footer
 * where it can be compared straight across a row.
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
 * `designs/` boards carry no `id` attributes at all — one artboard each — and
 * an index board is links and no frames because it is a contents page. Both are
 * working exactly as drawn.
 */
const KINDS = {
  pack: { label: 'drawn by hand', hint: 'A design pack. The frames are somebody’s work, and the package can only name them once a screen points at each one.' },
  generated: { label: 'generated', hint: '`derive-wireframes.py` draws this from the screen definitions on every refresh, and titles every frame itself.' },
  index: { label: 'contents', hint: 'Links to other boards rather than drawing anything. No frames is correct here.' },
  single: { label: 'single artboard', hint: 'One drawing, with no frame anchors to divide it. No frames is correct here.' },
};
const KIND_ORDER = ['pack', 'generated', 'index', 'single'];

const bytes = (n) => (n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.round(n / 1024)} KB`);
const day = (iso) => {
  try { return new Date(iso).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }); }
  catch { return ''; }
};
const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

/** How many chips a tile shows before it stops and says how many are left. */
const CHIP_CAP = 60;
/** How many rows the flat frame list draws before it says what it is holding back. */
const ROW_CAP = 600;

const VIEW_KEY = 'aster-uiux-view';

const state = {
  boards: [],
  folders: [],
  stats: null,
  platforms: [],          // from /api/journeys, for the platform rail
  screensPer: new Map(),  // platform code -> screen count
  view: 'map',
  group: 'folder',
  rail: 'folders',
  railFilter: '',
  filter: '',
  onlyUnwired: false,
  onlyUnclaimed: false,
  sel: { type: 'all', value: null },
  pick: null,
};

/** Everything a filter should be able to match, flattened once per board. */
const haystack = (b) => [
  b.name, b.file, b.title, b.kind, ...b.platforms,
  ...b.screens.map((s) => `${s.id} ${s.name ?? ''}`),
  ...b.frames.map((f) => `${f.anchor} ${f.name ?? ''}`),
].join(' ').toLowerCase();

/**
 * A frame is in one of three states, and they are three different jobs.
 *
 *   ok     a screen claims it and something can name it — finished
 *   named  something can name it, no screen claims it — the mapping job
 *   bare   nobody names it and nobody claims it — the mapping job, blind
 */
const frameState = (f) => (f.screens.length ? 'ok' : f.name ? 'named' : 'bare');

const byId = (id) => state.boards.find((b) => b.id === id) ?? null;

// ── which boards are on the page ─────────────────────────────────────

/** The rail's selection, as a predicate. */
function inSelection(b) {
  const { type, value } = state.sel;
  if (type === 'folder') return b.folder === value;
  if (type === 'kind') return b.kind === value;
  if (type === 'platform') return b.platforms.includes(value);
  if (type === 'unwired') return !b.wired;
  if (type === 'board') return b.id === value;
  return true;
}

function shownBoards() {
  const needle = state.filter.trim().toLowerCase();
  return state.boards
    .filter(inSelection)
    .filter((b) => !state.onlyUnwired || !b.wired)
    .filter((b) => !state.onlyUnclaimed || b.unclaimedFrames > 0)
    .filter((b) => !needle || haystack(b).includes(needle));
}

/** Is anything being held back? Headings need a denominator when there is. */
const isFiltered = () =>
  state.sel.type !== 'all' || state.onlyUnwired || state.onlyUnclaimed || state.filter.trim() !== '';

// ── the rail ─────────────────────────────────────────────────────────

/** Platforms no hand-drawn pack covers — the other half of the worklist.
 *
 *  Only claims from a `pack` board count. The generator draws every screen on
 *  every platform, so counting its claims too says every platform is covered,
 *  which is true of the generated drawing and false of the design.
 *
 *  `generatedFallback` is excluded for the same reason and no other: it says a
 *  board *used to* draw this. `board` and `frame` both say a pack draws it now.
 */
function platformsWithNoPack() {
  const covered = new Set(
    state.boards.filter((b) => b.kind === 'pack')
      .flatMap((b) => b.screens.filter((s) => s.via !== 'generatedFallback').map((s) => s.platform))
      .filter(Boolean)
  );
  return state.platforms
    .filter((p) => !covered.has(p.code))
    .map((p) => ({ ...p, screens: state.screensPer.get(p.code) ?? 0 }))
    .filter((p) => p.screens > 0)
    .sort((a, b) => b.screens - a.screens);
}

function railRow({ label, code, count, active, on, title }) {
  const row = el('button', `ux-row${active ? ' is-on' : ''}`);
  row.type = 'button';
  if (code) row.append(el('span', 'ux-row-code', code));
  row.append(el('span', 'ux-row-label', label));
  if (count != null) row.append(el('span', 'ux-row-count', String(count)));
  if (title) row.title = title;
  row.onclick = on;
  return row;
}

function railGroup(label, count) {
  const head = el('div', 'ux-group');
  head.append(el('span', 'ux-group-caret', '▾'));
  head.append(el('span', null, label));
  if (count != null) head.append(el('span', 'ux-group-count', String(count)));
  return head;
}

function pickSel(type, value) {
  const same = state.sel.type === type && state.sel.value === value;
  state.sel = same ? { type: 'all', value: null } : { type, value };
  if (type === 'board' && !same) state.pick = value;
  drawTree();
  drawBody();
  drawDetail();
}

function drawTree() {
  const tree = $('bd-tree');
  const needle = state.railFilter.trim().toLowerCase();
  const hit = (s) => !needle || String(s).toLowerCase().includes(needle);
  tree.textContent = '';
  let rows = 0;

  const add = (node) => { tree.append(node); rows += 1; };

  if (state.rail === 'folders') {
    const folders = state.folders.filter((f) => hit(f.label));
    if (folders.length) {
      tree.append(railGroup('Folders', state.folders.length));
      for (const f of folders) {
        add(railRow({
          label: f.label,
          count: f.count,
          active: state.sel.type === 'folder' && state.sel.value === f.id,
          on: () => pickSel('folder', f.id),
        }));
      }
    }

    // The boards nothing points at, by name. This is the group the page was
    // written for: they appear nowhere else in the viewer at all.
    const orphans = state.boards.filter((b) => !b.wired && hit(b.name))
      .sort((a, b) => b.frameCount - a.frameCount || a.name.localeCompare(b.name));
    if (orphans.length) {
      tree.append(railGroup('Nothing points at these', state.stats.unwired));
      for (const b of orphans) {
        add(railRow({
          label: b.name,
          count: b.frameCount,
          active: state.sel.type === 'board' && state.sel.value === b.id,
          title: `${b.file} — ${plural(b.frameCount, 'frame')}, none of them reachable from a screen`,
          on: () => pickSel('board', b.id),
        }));
      }
    }

    const noPack = platformsWithNoPack().filter((p) => hit(p.name) || hit(p.code));
    if (noPack.length) {
      tree.append(railGroup('Platforms with no pack', platformsWithNoPack().length));
      for (const p of noPack) {
        add(railRow({
          label: p.name,
          code: p.code,
          count: p.screens,
          active: state.sel.type === 'platform' && state.sel.value === p.code,
          title: `${plural(p.screens, 'screen')} on ${p.code}, and no hand-drawn board covers any of them`,
          on: () => pickSel('platform', p.code),
        }));
      }
    }
  }

  if (state.rail === 'platforms') {
    const counts = new Map();
    for (const b of state.boards) for (const p of b.platforms) counts.set(p, (counts.get(p) ?? 0) + 1);
    const known = new Map(state.platforms.map((p) => [p.code, p.name]));
    const codes = [...new Set([...counts.keys(), ...known.keys()])]
      .filter((c) => hit(c) || hit(known.get(c) ?? ''))
      .sort();
    tree.append(railGroup('Platforms', codes.length));
    for (const code of codes) {
      add(railRow({
        label: known.get(code) ?? code,
        code,
        count: counts.get(code) ?? 0,
        active: state.sel.type === 'platform' && state.sel.value === code,
        title: counts.get(code)
          ? `${plural(counts.get(code), 'board')} draw ${code}`
          : `nothing draws ${code}`,
        on: () => pickSel('platform', code),
      }));
    }
    const none = state.boards.filter((b) => !b.platforms.length).length;
    if (none && !needle) {
      add(railRow({
        label: 'no platform declared',
        count: none,
        active: state.sel.type === 'platform' && state.sel.value === '',
        on: () => pickSel('platform', ''),
      }));
    }
  }

  if (state.rail === 'kinds') {
    tree.append(railGroup('Kinds', KIND_ORDER.length));
    for (const kind of KIND_ORDER) {
      const mine = state.boards.filter((b) => b.kind === kind);
      if (!mine.length) continue;
      const k = KINDS[kind];
      if (!hit(k.label) && !hit(kind)) continue;
      add(railRow({
        label: k.label,
        count: mine.length,
        active: state.sel.type === 'kind' && state.sel.value === kind,
        title: k.hint,
        on: () => pickSel('kind', kind),
      }));
    }
    tree.append(railGroup('State', 1));
    add(railRow({
      label: 'nothing points at it',
      count: state.stats.unwired,
      active: state.sel.type === 'unwired',
      on: () => pickSel('unwired', null),
    }));
  }

  if (!rows) tree.append(el('p', 'ux-none', 'Nothing in the rail matches that.'));
  $('bd-rail-count').textContent = String(rows);
}

// ── the figures across the top ───────────────────────────────────────

function figure({ label, value, note, fill, tone }) {
  const box = el('div', `bd-figure${tone ? ` is-${tone}` : ''}`);
  box.append(el('p', 'bd-figure-value', String(value)));
  box.append(el('p', 'bd-figure-label', label));
  const meter = el('div', 'bd-meter');
  const bar = el('div', 'bd-meter-fill');
  bar.style.width = `${Math.max(0, Math.min(100, fill))}%`;
  meter.append(bar);
  box.append(meter);
  box.append(el('p', 'bd-figure-note', note));
  return box;
}

function drawFigures() {
  const s = state.stats;
  const unclaimed = s.frames - s.framesClaimed;
  const pct = (n, d) => (d ? Math.round((n / d) * 100) : 0);

  $('bd-figures').replaceChildren(
    figure({
      value: s.boards, label: 'boards on disk', fill: 100,
      note: `${plural(state.folders.length, 'folder')}, read directly`,
    }),
    figure({
      value: s.frames, label: 'frames drawn', fill: 100,
      note: 'across every board',
    }),
    figure({
      value: s.framesClaimed, label: 'claimed by a screen',
      fill: pct(s.framesClaimed, s.frames), tone: 'ok',
      note: `${pct(s.framesClaimed, s.frames)}% of what is drawn`,
    }),
    figure({
      value: unclaimed, label: 'claimed by nothing',
      fill: pct(unclaimed, s.frames), tone: 'warn',
      note: 'the mapping backlog',
    }),
    figure({
      value: s.unwired, label: 'boards nothing points at',
      fill: pct(s.unwired, s.boards), tone: 'warn',
      note: 'reachable from nowhere else',
    }),
  );
}

function drawLegend() {
  const box = $('bd-legend');
  box.textContent = '';
  const keys = el('div', 'bd-keys');
  const key = (cls, label) => {
    const k = el('span', 'bd-key');
    k.append(el('span', `bd-chip is-${cls}`));
    k.append(label);
    return k;
  };
  keys.append(key('ok', 'claimed and named'));
  keys.append(key('named', 'named, no screen claims it'));
  keys.append(key('bare', 'unnamed and unclaimed'));
  const orphan = el('span', 'bd-key');
  orphan.append(el('span', 'bd-key-rule'));
  orphan.append('board nothing points at');
  keys.append(orphan);
  box.append(keys);
  box.append(el('p', 'bd-legend-note',
    'A tile is a board and every tile is the same size, so a row compares like with like. '
    + 'The amber is the backlog — the same figure the rail counts, drawn.'));
}

// ── the middle ───────────────────────────────────────────────────────

/** One board as a tile: a chip per frame, and the two numbers underneath. */
function tile(board) {
  const box = el('article', `bd-tile${board.wired ? '' : ' is-unwired'}`
    + (state.pick === board.id ? ' is-picked' : ''));
  box.dataset.id = board.id;
  box.tabIndex = 0;

  const head = el('div', 'bd-tile-head');
  head.append(el('span', 'bd-tile-name', board.name));
  if (board.platforms.length) head.append(el('span', 'bd-tile-code', board.platforms[0]));
  box.append(head);

  const chips = el('div', 'bd-chips');
  if (board.frameCount) {
    for (const f of board.frames.slice(0, CHIP_CAP)) {
      const chip = el('span', `bd-chip is-${frameState(f)}`);
      chip.title = `${f.anchor} — ${f.name ?? 'nothing names this frame'}`;
      chips.append(chip);
    }
    if (board.frameCount > CHIP_CAP) {
      chips.append(el('span', 'bd-chip-more', `+${board.frameCount - CHIP_CAP}`));
    }
  } else {
    chips.append(el('span', 'bd-chips-none',
      board.kind === 'index' ? `${board.links} links, nothing drawn`
        : board.kind === 'single' ? 'one artboard, no frames'
          : 'no frames'));
  }
  box.append(chips);

  const foot = el('div', 'bd-tile-foot');
  foot.append(el('span', 'bd-tile-kind', (KINDS[board.kind] ?? { label: board.kind }).label));
  const right = board.unclaimedFrames
    ? el('span', 'bd-tile-left', `${board.unclaimedFrames} unclaimed`)
    : el('span', 'bd-tile-done', board.frameCount ? `${board.frameCount} claimed` : '');
  foot.append(right);
  box.append(foot);

  const open = () => { state.pick = board.id; drawBody(); drawDetail(); };
  box.onclick = open;
  box.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } };
  return box;
}

/** One entry per screen, in the order the claims arrived.
 *
 *  A screen claims a board once through `wireframe.board` and once per frame
 *  through `boardFrames`, so BO-044 arrives ten times on Retail Board 1 -- the
 *  drawing it calls its own, plus the nine frames it owns. Folding by id is what
 *  keeps a chip list from repeating one screen ten times over.
 */
function byScreen(claims) {
  const seen = new Map();
  for (const c of claims) if (!seen.has(c.id)) seen.set(c.id, c);
  return [...seen.values()];
}

/** The screens a board draws, kept in two lists because they mean two things. */
function screensBlock(board) {
  const wrap = el('div', 'uiux-screens');
  const current = byScreen(board.screens.filter((s) => s.via !== 'generatedFallback'));
  const superseded = byScreen(board.screens.filter((s) => s.via === 'generatedFallback'));

  if (current.length) {
    wrap.append(el('span', 'uiux-screens-label', `draws ${plural(current.length, 'screen')}`));
    for (const s of current.slice(0, 12)) {
      const chip = el('a', 'uiux-screen', s.id);
      chip.href = `/#screen:${encodeURIComponent(s.id)}`;
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
      `${plural(superseded.length, 'screen')} kept this as a generated fallback`);
    note.title = 'A client pack draws these now. The generator still writes these frames, so both exist and a regeneration cannot quietly remove the drawn one.';
    wrap.append(note);
  }
  return wrap;
}

/** One board as a card — the reading view. */
function card(board) {
  const box = el('article', `uiux-card${board.wired ? '' : ' is-unwired'}`
    + (state.pick === board.id ? ' is-picked' : ''));
  box.dataset.id = board.id;

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
  if (board.frameCount) {
    const strip = el('div', 'bd-chips is-inline');
    for (const f of board.frames.slice(0, CHIP_CAP)) {
      const chip = el('span', `bd-chip is-${frameState(f)}`);
      chip.title = `${f.anchor} — ${f.name ?? 'nothing names this frame'}`;
      strip.append(chip);
    }
    if (board.frameCount > CHIP_CAP) {
      strip.append(el('span', 'bd-chip-more', `+${board.frameCount - CHIP_CAP}`));
    }
    box.append(strip);
    box.append(el('p', 'uiux-note',
      `${board.frameCount} frames · ${board.namedFrames} named · ${board.unclaimedFrames} claimed by no screen`));
  } else if (board.kind === 'index') {
    box.append(el('p', 'uiux-note', `${board.links} links to other boards. Open it — it is the catalogue.`));
  }

  box.onclick = (e) => {
    if (e.target.closest('a')) return;   // the name still opens the board
    state.pick = board.id;
    drawBody();
    drawDetail();
  };
  return box;
}

/** How the boards on the page divide up. */
function groupsOf(shown) {
  if (state.group === 'none') {
    return [{ id: 'all', label: 'Every board', total: state.boards.length, members: shown }];
  }
  if (state.group === 'folder') {
    return state.folders.map((f) => ({
      id: f.id,
      label: f.label,
      total: f.count,
      members: shown.filter((b) => b.folder === f.id),
    }));
  }
  if (state.group === 'kind') {
    return KIND_ORDER.map((k) => ({
      id: k,
      label: (KINDS[k] ?? { label: k }).label,
      total: state.boards.filter((b) => b.kind === k).length,
      members: shown.filter((b) => b.kind === k),
    }));
  }
  // platform
  const names = new Map(state.platforms.map((p) => [p.code, p.name]));
  const codes = [...new Set(state.boards.flatMap((b) => b.platforms))].sort();
  const groups = codes.map((c) => ({
    id: c,
    label: `${c} ${names.get(c) ?? ''}`.trim(),
    total: state.boards.filter((b) => b.platforms.includes(c)).length,
    members: shown.filter((b) => b.platforms.includes(c)),
  }));
  groups.push({
    id: '',
    label: 'No platform declared',
    total: state.boards.filter((b) => !b.platforms.length).length,
    members: shown.filter((b) => !b.platforms.length),
  });
  return groups;
}

function sectionHead(group) {
  const wrap = el('div', 'bd-section-head');
  // `.uiux-folder` carries the label and the count and nothing else: a count
  // beside a filter box with no denominator is a number that lies, and the
  // denominator has to be the last thing in this element for that to read.
  const label = isFiltered() && group.members.length !== group.total
    ? `${group.label} — ${group.members.length} of ${group.total}`
    : `${group.label} — ${group.total}`;
  wrap.append(el('h2', 'uiux-folder', label));

  const frames = group.members.reduce((n, b) => n + b.frameCount, 0);
  const unclaimed = group.members.reduce((n, b) => n + b.unclaimedFrames, 0);
  const unwired = group.members.filter((b) => !b.wired).length;
  const note = el('span', 'bd-section-note');
  note.append(el('span', null, `${plural(frames, 'frame')}`));
  if (unclaimed) note.append(el('span', 'is-warn', `${unclaimed} unclaimed`));
  if (unwired) note.append(el('span', 'is-warn', `${unwired} unwired`));
  wrap.append(note);
  return wrap;
}

/** The flat worklist: one row per frame, across every board on the page. */
function framesTable(shown) {
  const rows = [];
  for (const b of shown) {
    for (const f of b.frames) {
      if (state.onlyUnclaimed && f.screens.length) continue;
      rows.push({ b, f });
    }
  }
  const wrap = el('div', 'bd-frames');
  if (!rows.length) {
    wrap.append(el('p', 'ux-none', 'No frame matches that.'));
    return wrap;
  }

  const table = el('table', 'bd-table');
  const thead = el('thead');
  const hr = el('tr');
  for (const h of ['Frame', 'What names it', 'Board', 'From']) hr.append(el('th', null, h));
  thead.append(hr);
  table.append(thead);

  const tb = el('tbody');
  for (const { b, f } of rows.slice(0, ROW_CAP)) {
    const tr = el('tr', `is-${frameState(f)}`);
    const anchorCell = el('td');
    if (b.folder === 'wireframes') {
      // Only `wireframes/` is served by /frame, and only a frame with an anchor
      // can be lifted out of a board at all.
      const link = el('a', 'bd-anchor', f.anchor);
      link.href = auth.pkgAsset(`/frame?board=${encodeURIComponent(b.file)}&anchor=${encodeURIComponent(f.anchor)}`);
      link.target = '_blank';
      link.rel = 'noopener';
      anchorCell.append(link);
    } else {
      anchorCell.append(el('span', 'bd-anchor', f.anchor));
    }
    tr.append(anchorCell);
    tr.append(el('td', f.name ? '' : 'is-unnamed', f.name ?? 'nothing names this frame'));

    const boardCell = el('td');
    const pickIt = el('button', 'bd-linkish', b.name);
    pickIt.type = 'button';
    pickIt.onclick = () => { state.pick = b.id; drawDetail(); };
    boardCell.append(pickIt);
    tr.append(boardCell);

    tr.append(el('td', 'bd-dim',
      f.source === 'board' ? 'the board' : f.source === 'screen' ? 'a screen' : '—'));
    tb.append(tr);
  }
  table.append(tb);
  wrap.append(table);

  if (rows.length > ROW_CAP) {
    wrap.append(el('p', 'ux-none',
      `${rows.length} frames match. The first ${ROW_CAP} are drawn — narrow it with the filter or the rail.`));
  }
  return wrap;
}

function drawBody() {
  const body = $('bd-body');
  body.textContent = '';
  const shown = shownBoards();

  if (!shown.length) {
    body.append(el('p', 'ux-none', 'No board matches that.'));
    return;
  }

  if (state.view === 'frames') {
    body.append(framesTable(shown));
    return;
  }

  for (const group of groupsOf(shown)) {
    if (!group.members.length) continue;
    body.append(sectionHead(group));
    if (state.view === 'map') {
      const map = el('div', 'bd-map');
      for (const b of group.members) map.append(tile(b));
      body.append(map);
    } else {
      const grid = el('div', 'uiux-grid');
      for (const b of group.members) grid.append(card(b));
      body.append(grid);
    }
  }
}

// ── the panel on the right ───────────────────────────────────────────

/**
 * What this board's numbers mean, in a sentence.
 *
 * A count of named frames is only interesting against the count of frames, and
 * the interesting case — a hand-drawn pack where *nothing* names anything — is
 * the one a reader will otherwise scroll straight past.
 */
function verdict(board) {
  const { frameCount: n, namedFrames: named, unclaimedFrames: left } = board;
  if (board.kind === 'index') {
    return [`A contents page: ${board.links} links to other boards and nothing drawn of its own. `,
      'No frames is correct here — but nothing in the viewer opens it except this panel.'];
  }
  if (board.kind === 'single') {
    return ['One artboard, with no frame anchors to divide it. ',
      'No frames is correct here; there is nothing to claim.'];
  }
  if (!n) return ['Nothing drawn on it that the reader can find — no frame anchors at all.', ''];
  if (named === 0) {
    return [`${plural(n, 'frame')}, none of them named by anything. `,
      `0 named of ${n} is the signature of an unmapped pack — somebody drew it, and the package cannot say what it draws.`];
  }
  if (left === 0) {
    return [`${plural(n, 'frame')}, every one of them claimed by a screen. `,
      'This board is finished as far as the mapping goes.'];
  }
  return [`${plural(n, 'frame')}, ${named} of them named and ${left} claimed by no screen. `,
    'The unclaimed ones are what is left of the mapping job on this board.'];
}

function detailEmpty() {
  const box = $('bd-detail');
  box.textContent = '';
  box.append(el('p', 'bd-detail-eyebrow', 'Nothing picked'));
  box.append(el('h2', 'bd-detail-title', 'Pick a board'));
  box.append(el('p', 'bd-detail-lead',
    'Read off the disk, not off the screens. The rest of the viewer shows a board '
    + 'through a screen that points at it, which is right for reviewing a screen and is '
    + 'why a board nobody has wired up appears nowhere at all — including a hand-built '
    + 'index of every frame in the package.'));
  box.append(el('p', 'bd-detail-lead',
    'A board nobody has claimed is not a board that does not exist. It is the one most '
    + 'worth looking at, because somebody drew it and the package cannot yet say what it draws.'));
}

function drawDetail() {
  const board = state.pick ? byId(state.pick) : null;
  if (!board) { detailEmpty(); return; }

  const box = $('bd-detail');
  box.textContent = '';

  const pills = el('div', 'bd-pills');
  if (!board.wired) {
    const p = el('span', 'bd-pill is-warn', 'unwired');
    p.title = 'No screen names this board, so it appears nowhere else in the viewer.';
    pills.append(p);
  }
  const kind = KINDS[board.kind] ?? { label: board.kind, hint: '' };
  const kp = el('span', `bd-pill is-${board.kind}`, kind.label);
  kp.title = kind.hint;
  pills.append(kp);
  if (board.revision) pills.append(el('span', 'bd-pill', board.revision));
  box.append(pills);

  box.append(el('h2', 'bd-detail-title', board.name));
  if (board.title && board.title !== board.name) {
    box.append(el('p', 'bd-detail-sub', board.title));
  }
  box.append(el('p', 'bd-detail-path',
    `${board.folder}/${board.file} · ${bytes(board.bytes)} · ${day(board.modified)}`));

  // The board itself, one click away. Not an inline preview: these files run to
  // hundreds of kilobytes of exported design markup with scripts of their own,
  // and framing one inside the viewer means the viewer inherits whatever it
  // logs. The link is the honest version of the same affordance.
  const open = el('a', 'bd-open');
  open.href = auth.pkgAsset(board.url);
  open.target = '_blank';
  open.rel = 'noopener';
  open.append(el('span', 'bd-open-mark', '↗'));
  open.append(el('span', 'bd-open-label', 'Open the board'));
  open.append(el('span', 'bd-open-note', board.file));
  box.append(open);

  const [head, tail] = verdict(board);
  const lead = el('p', 'bd-detail-lead');
  lead.append(head);
  if (tail) lead.append(el('strong', null, tail));
  box.append(lead);

  const facts = el('dl', 'bd-dl');
  const fact = (k, v, warn = false) => {
    facts.append(el('dt', null, k));
    facts.append(el('dd', warn ? 'is-warn' : null, v));
  };
  fact('frames', String(board.frameCount));
  fact('named', String(board.namedFrames), board.frameCount > 0 && board.namedFrames === 0);
  fact('unclaimed', String(board.unclaimedFrames), board.unclaimedFrames > 0);
  fact('platform', board.platforms.join(' · ') || 'nothing declares one', !board.platforms.length);
  box.append(facts);

  const current = byScreen(board.screens.filter((s) => s.via !== 'generatedFallback'));
  const superseded = byScreen(board.screens.filter((s) => s.via === 'generatedFallback'));
  if (current.length || superseded.length) {
    box.append(el('h3', 'bd-detail-h3', `Screens — ${current.length} drawn here`));
    const wrap = el('div', 'uiux-screens');
    for (const s of current.slice(0, 40)) {
      const chip = el('a', 'uiux-screen', s.id);
      chip.href = `/#screen:${encodeURIComponent(s.id)}`;
      chip.title = s.name ? `${s.id} — ${s.name}` : s.id;
      wrap.append(chip);
    }
    if (current.length > 40) wrap.append(el('span', 'uiux-more', `and ${current.length - 40} more`));
    if (superseded.length) {
      const note = el('span', 'uiux-screens-label uiux-superseded',
        `${plural(superseded.length, 'screen')} kept this as a generated fallback`);
      note.title = 'A client pack draws these now, and the generator still writes these frames.';
      wrap.append(note);
    }
    box.append(wrap);
  } else {
    box.append(el('h3', 'bd-detail-h3', 'Screens'));
    box.append(el('p', 'bd-detail-none', 'None point here.'));
  }

  if (board.frameCount) {
    const left = board.unclaimedFrames;
    box.append(el('h3', 'bd-detail-h3',
      left ? `Frames — ${left} to claim` : `Frames — all ${board.frameCount} claimed`));
    const list = el('div', 'bd-frame-list');
    // Unclaimed first: this list is a worklist, and the finished rows are
    // context rather than the reason anybody opened it.
    const order = [...board.frames].sort(
      (a, b) => (a.screens.length ? 1 : 0) - (b.screens.length ? 1 : 0));
    for (const f of order) {
      const row = el('div', `bd-frame is-${frameState(f)}`);
      if (board.folder === 'wireframes') {
        const link = el('a', 'bd-anchor', f.anchor);
        link.href = auth.pkgAsset(`/frame?board=${encodeURIComponent(board.file)}&anchor=${encodeURIComponent(f.anchor)}`);
        link.target = '_blank';
        link.rel = 'noopener';
        row.append(link);
      } else {
        row.append(el('span', 'bd-anchor', f.anchor));
      }
      row.append(el('span', `bd-frame-name${f.name ? '' : ' is-unnamed'}`,
        f.name ?? 'nothing names this frame'));
      list.append(row);
    }
    box.append(list);
  }
}

// ── boot ─────────────────────────────────────────────────────────────

function drawLead() {
  const s = state.stats;
  const unclaimed = s.frames - s.framesClaimed;
  $('lead').textContent =
    `${plural(s.boards, 'board')} · ${plural(s.frames, 'frame')} · `
    + `${unclaimed} claimed by nothing · ${s.unwired} nothing points at`;
  const fine = $('fine-unwired');
  if (fine) fine.textContent = String(s.unwired);
}

function drawCallout() {
  const s = state.stats;
  const unclaimed = s.frames - s.framesClaimed;
  const boards = state.boards.filter((b) => b.unclaimedFrames > 0).length;
  const box = $('bd-callout');
  box.textContent = '';
  if (!unclaimed) {
    box.classList.add('is-clear');
    box.append(el('p', 'ux-callout-lead', 'Every frame is claimed'));
    box.append(el('p', null, 'There is no mapping backlog on this package.'));
    return;
  }
  box.append(el('p', 'ux-callout-lead', String(unclaimed)));
  box.append(el('p', null,
    `frames no screen claims, across ${plural(boards, 'board')}. `
    + 'That is the mapping job, and it is the whole reason this layer has a worklist.'));
  box.onclick = () => {
    state.onlyUnclaimed = true;
    $('bd-unclaimed').checked = true;
    setView('frames');
  };
}

function setView(view) {
  state.view = view;
  try { localStorage.setItem(VIEW_KEY, view); } catch { /* private window */ }
  for (const b of $('bd-seg').querySelectorAll('button')) {
    b.classList.toggle('on', b.dataset.view === view);
  }
  drawBody();
}

(async () => {
  await auth.requireSignIn();

  const me = auth.account();
  // Optional: inside the viewer these views are sections of a page that already
  // says who you are, so there is no `#whoami` to fill.
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

  // The platform rail needs the platform list, which is the Frontend layer's to
  // know. It is a second request and the page is useful without it, so a
  // failure here costs one rail group rather than the page.
  try {
    const journeys = await json('/api/journeys');
    state.platforms = (journeys.platforms ?? []).map((p) => ({
      code: p.code,
      name: p.shortName || p.name || p.code,
    }));
    for (const s of journeys.screens ?? []) {
      if (!s.platform) continue;
      state.screensPer.set(s.platform, (state.screensPer.get(s.platform) ?? 0) + 1);
    }
  } catch { /* the folders and kinds rails still work */ }

  try {
    const saved = localStorage.getItem(VIEW_KEY);
    if (saved === 'map' || saved === 'list' || saved === 'frames') state.view = saved;
  } catch { /* private window */ }

  drawLead();
  drawCallout();
  drawFigures();
  drawLegend();
  drawTree();
  setView(state.view);      // paints the segment and calls drawBody
  drawDetail();
  hideLoader();

  $('bd-tabs').onclick = (e) => {
    const b = e.target.closest('button[data-rail]');
    if (!b) return;
    state.rail = b.dataset.rail;
    for (const t of $('bd-tabs').querySelectorAll('button')) t.classList.toggle('is-on', t === b);
    drawTree();
  };
  $('bd-seg').onclick = (e) => {
    const b = e.target.closest('button[data-view]');
    if (b) setView(b.dataset.view);
  };
  $('bd-rail-filter').oninput = (e) => { state.railFilter = e.target.value; drawTree(); };
  $('filter').oninput = (e) => { state.filter = e.target.value; drawBody(); };
  $('bd-group').onchange = (e) => { state.group = e.target.value; drawBody(); };
  $('only-unwired').onchange = (e) => { state.onlyUnwired = e.target.checked; drawBody(); };
  $('bd-unclaimed').onchange = (e) => { state.onlyUnclaimed = e.target.checked; drawBody(); };
  $('bd-claim').onclick = () => {
    state.onlyUnclaimed = true;
    $('bd-unclaimed').checked = true;
    setView('frames');
    $('bd-scroll').scrollTop = 0;
  };
})();
