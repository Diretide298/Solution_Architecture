/**
 * The screens, laid out and joined up.
 *
 * The board list next door answers "what has been drawn". This answers the
 * other question a reviewer asks and could not ask anywhere: **where does this
 * screen sit, and what leads to it.** The Frontend layer shows one screen at a
 * time and the journey view shows one journey at a time; neither puts 492
 * screens on one surface where the shape of the thing is visible.
 *
 * Three things it will not fake:
 *
 * **Inferred navigation is drawn as inferred.** 345 of the 492 screens carry
 * `navigationInferred`, so most of the 1,474 links here are the package's guess
 * from module and wave rather than anything anybody declared. Drawn the same as
 * the rest they would read as a designed flow, which is exactly the false
 * confidence a picture buys you. Dashed, and switchable off.
 *
 * **A frame is only mounted when it can be seen.** 492 live iframes is not a
 * canvas, it is a stall; and a thumbnail nobody generated cannot be shown. So a
 * node is a card until it is both inside the viewport and above the zoom where
 * a frame is legible, and it goes back to being a card when it leaves.
 *
 * **A screen with no board says so.** Every one of the 492 has a
 * `wireframe.board` today, but the reference can point at a board that is not
 * there, and an empty tile reads as a screen that failed to load rather than a
 * drawing that does not exist.
 *
 * **One platform at a time.** The first cut of this put all fifteen platforms
 * on one sheet, which fit at 8% — 492 screens rendered as dashes, and no zoom
 * at which any of it was both legible and navigable. Nobody reviews UI across
 * platforms anyway: the question is always "what does P08 look like", and the
 * answer to it was buried in a wall of everything. So the platform is chosen
 * first, in the rail, and the canvas holds that platform's screens and nothing
 * else. The journeys listed are the ones that touch it, and they say how much
 * of themselves is here rather than pretending a nine-step journey lives on one
 * platform. Crossing over is a click, not a scroll: an exit into another
 * platform switches the sheet and lands on the screen.
 */

import '/theme.js';
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';
import { attachSubSearch } from '/subsearch.js';

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

// ── the shape of the board ───────────────────────────────────────────
// A card is the aspect of a phone-ish screen rather than a square, because the
// frame that mounts inside it is a screen and a square would letterbox every
// one of them.
const CARD = { w: 232, h: 168 };
const GAP = { x: 26, y: 34 };
// A band is a module: a titled shelf the screens of one module sit on. Eight
// across is what fits a 1600px viewport at a zoom where the names are readable,
// and wrapping inside the band keeps a 30-screen module from becoming a column.
const BAND = { cols: 4, perRow: 3, top: 54, side: 22, bottom: 22, gap: 40 };
// A journey is laid out as a lane rather than a grid: six steps across, then it
// wraps, so a nine-step flow reads left to right and down like a sentence.
const LANE = { cols: 6, top: 62, side: 26, bottom: 26, gapX: 74, gapY: 62 };

// Below this the frames are unreadable, so mounting them costs a fetch to show
// a smudge. The cards carry the name at every zoom.
const FRAME_ZOOM = 0.55;
// A ceiling on live frames regardless of viewport: a wide monitor at high zoom
// can have sixty in view, and sixty documents is the stall this exists to
// avoid.
const MAX_LIVE = 28;

const state = {
  screens: [],
  flows: [],
  platforms: [],
  byId: new Map(),
  nodes: [],
  blocks: [],
  edges: [],
  extent: { w: 0, h: 0 },
  view: { x: 0, y: 0, k: 0.5 },
  selected: null,
  hover: null,
  journey: null,
  platform: '',
  // Read off the controls at boot rather than declared here. They were declared
  // here once, and the links box shipped unchecked against a state that said
  // true — so the sheet opened with all 501 links drawn under a control that
  // said they were not.
  links: 'cross',
  showInferred: true,
  tab: 'journeys',
};

// ── cards somebody moved ─────────────────────────────────────────────
/**
 * A layout is a starting point, not a verdict.
 *
 * The shelves put a module's screens in wave order, which is right until a
 * reviewer wants two screens beside each other to compare them, or wants the
 * exception path pulled out of the row. So a card can be dragged, and where it
 * was dragged to is kept — per platform, and per journey, because a card in a
 * lane and the same card on the board are in two different pictures.
 *
 * Kept in `localStorage` and nowhere else. This is one reader's arrangement of
 * one sheet, not a fact about the package: writing it back would make a private
 * preference look like a decision, and the package is the thing that is under
 * review.
 */
const moveKey = () => `aster-canvas-moved:${state.platform}:${state.journey ?? 'board'}`;

function readMoved() {
  try {
    const raw = localStorage.getItem(moveKey());
    const parsed = raw ? JSON.parse(raw) : null;
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch { return {}; }        // denied, or somebody hand-edited it to junk
}

function writeMoved(map) {
  try {
    if (Object.keys(map).length) localStorage.setItem(moveKey(), JSON.stringify(map));
    else localStorage.removeItem(moveKey());
  } catch { /* denied outright; the move still holds for this session */ }
}

/** Put the remembered positions back on, after a layout has run. */
function applyMoved(nodes) {
  const moved = readMoved();
  for (const n of nodes) {
    const at = moved[n.key];
    if (!Array.isArray(at) || at.length !== 2) continue;
    if (!Number.isFinite(at[0]) || !Number.isFinite(at[1])) continue;
    n.x = at[0];
    n.y = at[1];
    n.moved = true;
  }
  return nodes;
}

/** `wireframes/P01 Guest Web.dc.html#web-001` -> { board, anchor } */
function frameRef(screen) {
  const ref = screen?.wireframe?.board;
  if (typeof ref !== 'string' || !ref.includes('#')) return null;
  const [target, anchor] = ref.split('#');
  // `/frame` serves out of `wireframes/` only. A screen pointing anywhere else
  // gets a card and a reason rather than an iframe that 403s behind the scenes.
  if (!/^\.?\/?wireframes\//i.test(target)) return null;
  const board = target.replace(/^\.?\/*/, '').replace(/^wireframes\//i, '');
  if (!board || !anchor) return null;
  return { board, anchor: anchor.toLowerCase() };
}

// ── layout ───────────────────────────────────────────────────────────
/**
 * Two layouts, because there are two questions and one of them is not a grid.
 *
 * **The board** answers "what is on this platform". It is not one undivided
 * sheet of 143 tiles: the screens are shelved by module, which is a grouping the
 * package already declares and the only one a reviewer navigates by. Waves order
 * the shelves, so the thing that ships first is at the top.
 *
 * **The lane** answers "what happens in this journey", and it is the one that
 * had to stop being a grid. Navigation between screens is a cyclic graph — 143
 * screens on P08 carry 501 exits between them, and a longest-path ranking of it
 * runs away to rank 500, which is the arithmetic way of saying *there is no left
 * to right in it*. Drawn as lines over a grid it is a scribble, and a scribble
 * over a picture of the product reads as the product being a mess. The flows in
 * `flows/` are the part that genuinely has an order: **steps, numbered, one
 * after another**. So a journey is drawn as a lane of numbered steps with
 * arrows between them, and the hairball is not drawn at all unless it is asked
 * for.
 */
function boardLayout(screens) {
  const bands = new Map();
  for (const s of screens) {
    const key = s.module || 'Unmoduled';
    if (!bands.has(key)) bands.set(key, []);
    bands.get(key).push(s);
  }
  const ordered = [...bands.entries()].sort((a, b) => {
    const wa = Math.min(...a[1].map((s) => s.wave ?? 99));
    const wb = Math.min(...b[1].map((s) => s.wave ?? 99));
    return (wa - wb) || a[0].localeCompare(b[0]);
  });

  // **Shelves wrap, they do not stack.** One shelf per row made a sheet 13
  // shelves tall and one shelf wide, which fits at 20% and turns every link
  // between two modules into a diagonal streak the height of the page. Wrapped
  // into a landscape sheet the same links are short, and a crossing reads as a
  // crossing rather than as a scratch on the screen.
  //
  // Four cards across inside a shelf, three shelves across the sheet: measured
  // against 46 and 143 screens, that is the pair that keeps the whole platform
  // legible at a zoom where the names can be read.
  const cols = BAND.cols;
  const inner = cols * CARD.w + (cols - 1) * GAP.x;
  const bandW = inner + BAND.side * 2;
  const perRow = Math.max(1, Math.min(BAND.perRow, ordered.length));
  const blocks = [];
  const nodes = [];
  let penX = 0;
  let penY = 0;
  let rowTall = 0;
  let inRow = 0;

  for (const [module, list] of ordered) {
    list.sort((a, b) => ((a.wave ?? 99) - (b.wave ?? 99)) || a.id.localeCompare(b.id));
    const rows = Math.ceil(list.length / cols);
    const h = BAND.top + rows * CARD.h + (rows - 1) * GAP.y + BAND.bottom;
    const waves = [...new Set(list.map((s) => s.wave).filter((w) => w != null))].sort();

    if (inRow >= perRow) { penX = 0; penY += rowTall + BAND.gap; rowTall = 0; inRow = 0; }

    blocks.push({
      id: module,
      label: module,
      note: `${list.length} screen${list.length === 1 ? '' : 's'}`
        + (waves.length ? ` · wave ${waves.join(', ')}` : ''),
      x: penX, y: penY, w: bandW, h,
    });
    list.forEach((sc, i) => {
      nodes.push({
        screen: sc,
        id: sc.id,
        key: sc.id,
        x: penX + BAND.side + (i % cols) * (CARD.w + GAP.x),
        y: penY + BAND.top + Math.floor(i / cols) * (CARD.h + GAP.y),
        w: CARD.w, h: CARD.h,
        frame: frameRef(sc),
        node: null, live: false, ghost: false, step: 0,
      });
    });
    rowTall = Math.max(rowTall, h);
    penX += bandW + BAND.gap;
    inRow += 1;
  }

  applyMoved(nodes);
  return { blocks, nodes, extent: extentOf(blocks, nodes) };
}

/**
 * One journey, laid out as the sequence it is.
 *
 * Steps that are on another platform are drawn too, greyed, saying which — a
 * journey that crosses to the back office and back is most of what the flows
 * describe, and cutting the lane at the boundary would draw a four-step journey
 * where there is an eight-step one.
 */
function laneLayout(flow) {
  const steps = (flow?.steps ?? []).map((st) => st.screenId).filter(Boolean);
  const cols = Math.min(LANE.cols, Math.max(1, steps.length));
  const rows = Math.ceil(steps.length / cols) || 1;
  const inner = cols * CARD.w + (cols - 1) * LANE.gapX;

  const nodes = steps.map((id, i) => {
    const sc = state.byId.get(id);
    const ghost = !sc || sc.platform !== state.platform;
    return {
      screen: sc ?? { id, name: 'not in this package' },
      id,
      key: `${id}#${i}`,
      x: LANE.side + (i % cols) * (CARD.w + LANE.gapX),
      y: LANE.top + Math.floor(i / cols) * (CARD.h + LANE.gapY),
      w: CARD.w, h: CARD.h,
      frame: sc ? frameRef(sc) : null,
      node: null, live: false, ghost, step: i + 1,
    };
  });

  const here = nodes.filter((n) => !n.ghost).length;
  const blocks = [{
    id: flow.id,
    label: `${flow.id} · ${flow.name ?? ''}`,
    note: here === nodes.length
      ? `${nodes.length} steps`
      : `${nodes.length} steps · ${here} on ${state.platform}, ${nodes.length - here} elsewhere`,
    x: 0, y: 0,
    w: inner + LANE.side * 2,
    h: LANE.top + rows * CARD.h + (rows - 1) * LANE.gapY + LANE.bottom,
  }];

  applyMoved(nodes);
  return { blocks, nodes, extent: extentOf(blocks, nodes) };
}

/**
 * How big the world is.
 *
 * The shelves *and* the cards, because a card dragged past the edge of its
 * shelf would otherwise fall outside the world — off the end of the `#nodes`
 * box and off the SVG the links are drawn on, so the card would be there and
 * its links would stop at the boundary.
 */
const extentOf = (blocks, nodes = []) => ({
  w: Math.max(...blocks.map((b) => b.x + b.w), ...nodes.map((n) => n.x + n.w), 1) + 120,
  h: Math.max(...blocks.map((b) => b.y + b.h), ...nodes.map((n) => n.y + n.h), 1) + 120,
});

// ── what belongs to a platform ───────────────────────────────────────
const screensOn = (platform) => state.screens.filter((s) => s.platform === platform);

/**
 * The journeys that touch a platform, and how much of each one is here.
 *
 * A journey is not a platform's property — 'apply for a loan' crosses the
 * customer app, the branch console and the back office. Listing it under P02
 * without saying that would promise the whole flow and draw three of its nine
 * steps, which is the sort of quiet lie a picture tells best. So the count
 * rides in the row: **`4 of 9 steps here`**.
 *
 * Ordered by how much of the journey is on this platform, because the ones that
 * mostly live here are the ones this sheet can actually answer for.
 */
function journeysOn(platform) {
  const here = new Set(screensOn(platform).map((s) => s.id));
  return state.flows
    .map((flow) => {
      const steps = (flow.steps ?? []).map((st) => st.screenId).filter(Boolean);
      return { flow, steps: steps.length, on: steps.filter((id) => here.has(id)).length };
    })
    .filter((x) => x.on > 0)
    .sort((a, b) => (b.on - a.on) || a.flow.id.localeCompare(b.flow.id));
}

/**
 * Screen to screen, and whether the link leaves the shelf it starts on.
 *
 * `cross` is the interesting bit. The board shelves screens by module, so a
 * link inside a shelf mostly restates the shelf — the package infers that
 * everything in a module reaches everything else in it, which is where two
 * thirds of these come from. **A link that leaves the shelf is the one the
 * layout cannot show you**: it is where a journey hands off from one part of
 * the product to another, and it is the thing a reviewer is looking for.
 */
function buildEdges(nodes) {
  const at = new Map(nodes.map((n) => [n.id, n]));
  const edges = [];
  for (const n of nodes) {
    const exits = n.screen?.navigation?.exitTo ?? [];
    const inferred = Boolean(n.screen?.navigationInferred);
    for (const target of exits) {
      const to = at.get(target);
      if (!to) continue;          // the payload has none of these, but a
      if (to === n) continue;     // reference is a reference
      const cross = (n.screen?.module || '') !== (to.screen?.module || '');
      edges.push({ from: n, to, inferred, flow: false, cross });
    }
  }
  return edges;
}

/** Step to step. The one set of links in this package that is a sequence. */
const laneEdges = (nodes) =>
  nodes.slice(1).map((to, i) => ({ from: nodes[i], to, inferred: false, flow: true }));

// ── painting ─────────────────────────────────────────────────────────
const world = () => $('world');

function applyView() {
  const { x, y, k } = state.view;
  world().style.transform = `translate(${x}px, ${y}px) scale(${k})`;
  $('zoom-level').textContent = `${Math.round(k * 100)}%`;
}

/** Which world rectangle the viewport is showing, in world units. */
function visibleRect() {
  const box = $('viewport').getBoundingClientRect();
  const { x, y, k } = state.view;
  return {
    x0: (-x) / k, y0: (-y) / k,
    x1: (-x + box.width) / k, y1: (-y + box.height) / k,
  };
}

const hits = (n, r, pad = 240) =>
  n.x + n.w > r.x0 - pad && n.x < r.x1 + pad && n.y + n.h > r.y0 - pad && n.y < r.y1 + pad;

/**
 * Mount and unmount the frames.
 *
 * The iframe is created on the way in and *removed* on the way out rather than
 * hidden: a hidden iframe is still a live document with its own timers, and
 * four hundred of them hidden is the same stall as four hundred of them shown.
 */
function paintFrames() {
  const r = visibleRect();
  const wantFrames = state.view.k >= FRAME_ZOOM;
  const inView = state.nodes.filter((n) => n.node && !n.node.hidden && hits(n, r));

  let budget = MAX_LIVE;
  const keep = new Set();
  if (wantFrames) {
    for (const n of inView) {
      if (budget <= 0) break;
      if (!n.frame) continue;
      keep.add(n);
      budget -= 1;
    }
  }

  for (const n of state.nodes) {
    if (keep.has(n) && !n.live) {
      const shell = n.node.querySelector('.cv-frame');
      const frame = document.createElement('iframe');
      frame.className = 'cv-iframe';
      frame.loading = 'lazy';
      frame.setAttribute('tabindex', '-1');
      frame.setAttribute('aria-hidden', 'true');
      frame.setAttribute('sandbox', 'allow-same-origin');
      // `still=1`: the frame with its scripts stripped server-side. A tile has
      // no behaviour to run, and leaving them in means the sandbox blocks each
      // one and logs a console error per tile.
      frame.src = auth.pkgAsset(
        `/frame?board=${encodeURIComponent(n.frame.board)}`
        + `&anchor=${encodeURIComponent(n.frame.anchor)}&still=1`,
      );
      shell.replaceChildren(frame);
      n.node.classList.add('is-live');
      n.live = true;
    } else if (!keep.has(n) && n.live) {
      n.node.querySelector('.cv-frame').replaceChildren();
      n.node.classList.remove('is-live');
      n.live = false;
    }
  }

  // Its own element. This used to write into `#canvas-note`, which is where
  // the sheet says what it is holding — so "P04 · 24 screens in 4 modules"
  // survived exactly until the first pan, and the page then only ever told you
  // how many tiles were mounted, which is the least interesting true thing on
  // the screen.
  $('frame-note').textContent = wantFrames
    ? `${keep.size} of ${inView.length} drawn`
    : `zoom past ${Math.round(FRAME_ZOOM * 100)}% to draw the screens`;
}

let painting = false;
function schedulePaint() {
  if (painting) return;
  painting = true;
  requestAnimationFrame(() => { painting = false; paintFrames(); });
}

// ── edges ────────────────────────────────────────────────────────────
/**
 * Give every link its own place on the card's edge.
 *
 * Six links arriving at one screen all aimed at the middle of its left edge is
 * six curves converging on one pixel — they overlap into a ribbon on the way in
 * and the arrowheads stack into a blob. It reads as a rendering fault rather
 * than as six links.
 *
 * So each link gets a slot: the *n*th of *m* arrivals enters at *n/(m+1)* of the
 * way down the card's edge, over the middle 64% of it so nothing lands on a
 * rounded corner. Departures are spread the same way down the other side. The
 * order is by the other end's vertical position, which is what stops the fan
 * from crossing itself — the link coming from highest up arrives highest.
 */
function slotEdges(edges) {
  const group = (key, side) => {
    const by = new Map();
    for (const e of edges) {
      const k = key(e);
      if (!by.has(k)) by.set(k, []);
      by.get(k).push(e);
    }
    for (const list of by.values()) {
      list.sort((a, b) => (side === 'in' ? a.from.y - b.from.y : a.to.y - b.to.y));
      list.forEach((e, i) => {
        e[side === 'in' ? 'inSlot' : 'outSlot'] = i;
        e[side === 'in' ? 'inOf' : 'outOf'] = list.length;
      });
    }
  };
  group((e) => e.to.id, 'in');
  group((e) => e.from.id, 'out');
  return edges;
}

/** Where on a card's side a link with slot `i` of `n` attaches. */
const anchorY = (node, i = 0, n = 1) =>
  node.y + node.h * (0.18 + 0.64 * ((i + 1) / (n + 1)));

/**
 * A curve from the side of one card to the side of the next.
 *
 * A link that goes backwards leaves the **left** side and arrives at the
 * **right** side, rather than leaving the right and bulging all the way round.
 * The bulge was drawn to avoid passing under the cards and it did — by drawing
 * a loop half the width of the shelf, which is worse. Leaving from the side the
 * link is actually heading is what makes a return read as a return.
 */
function edgePath(e) {
  const { from, to } = e;
  const back = to.x + to.w / 2 < from.x + from.w / 2;
  const x1 = back ? from.x : from.x + from.w;
  const x2 = back ? to.x + to.w : to.x;
  const y1 = anchorY(from, e.outSlot, e.outOf);
  const y2 = anchorY(to, e.inSlot, e.inOf);
  // Proportional, but bounded at both ends: short links need a visible bend to
  // read as a curve, long ones need a flat one or they swing off the shelf.
  const reach = Math.min(180, Math.max(46, Math.abs(x2 - x1) * 0.42));
  const c1 = back ? x1 - reach : x1 + reach;
  const c2 = back ? x2 + reach : x2 - reach;
  return `M ${x1} ${y1} C ${c1} ${y1}, ${c2} ${y2}, ${x2} ${y2}`;
}

/**
 * Which links to draw.
 *
 * The whole platform's navigation is 501 links over 143 screens, two thirds of
 * them the package's guess. Drawn identically and all at once they say nothing
 * except that there are a lot of them, which is what made the first cut of this
 * a scribble over a grid. Drawn by *what they are* they say something: a link
 * that crosses from one module to another is a handoff between two parts of the
 * product, and a link inside a module is mostly the inference restating the
 * module. So the crossings are drawn plainly, the rest are drawn faintly behind
 * them, and the bar can turn either off.
 *
 * Whatever the setting, the links of the screen you picked are drawn. That is
 * the question the canvas exists to answer and it does not get switched off.
 */
/**
 * The screen the pointer is on, and the screens it reaches.
 *
 * Hover is a question — *what does this one connect to* — and the answer is
 * only legible if the rest of the sheet gets out of the way. So the links of
 * the screen under the pointer are drawn in the accent with their arrowheads,
 * every other link drops to a tenth of its opacity, and the screens at the far
 * end of those links are outlined. Nothing moves except the card itself, which
 * lifts.
 *
 * Repainted rather than restyled in place, because a link that was filtered out
 * — an inferred one inside a module, with the bar set to crossings — still has
 * to appear when you point at the screen it belongs to. There is no element to
 * restyle. Coalesced into one frame so that dragging the pointer across a shelf
 * of eight cards costs eight frames rather than eighty.
 */
function setHover(id) {
  if (state.hover === id) return;
  state.hover = id;
  const lit = new Set();
  if (id) {
    for (const e of state.edges) {
      if (e.from.id === id) lit.add(e.to.id);
      else if (e.to.id === id) lit.add(e.from.id);
    }
  }
  for (const n of state.nodes) {
    n.node?.classList.toggle('is-linked', lit.has(n.id) && n.id !== id);
  }
  $('world').classList.toggle('is-hovering', Boolean(id));
  scheduleEdges();
}

let edgesQueued = false;
function scheduleEdges() {
  if (edgesQueued) return;
  edgesQueued = true;
  requestAnimationFrame(() => { edgesQueued = false; paintEdges(); });
}

function paintEdges() {
  const svg = $('edges');
  svg.setAttribute('viewBox', `0 0 ${state.extent.w} ${state.extent.h}`);
  svg.setAttribute('width', state.extent.w);
  svg.setAttribute('height', state.extent.h);
  svg.replaceChildren(arrowDefs());
  svg.classList.toggle('is-focused', Boolean(state.hover || state.selected));

  const frag = document.createDocumentFragment();
  slotEdges(state.edges);
  for (const e of state.edges) {
    if (!e.flow) {
      if (e.inferred && !state.showInferred) continue;
      // The screen you picked *and* the screen you are pointing at. Both are
      // "this one" as far as the reader is concerned, and both have to bring
      // their links with them whatever the bar is set to.
      const lit = state.selected ?? state.hover;
      const near = Boolean(lit) && (e.from.id === lit || e.to.id === lit);
      if (!near) {
        if (state.links === 'none') continue;
        if (state.links === 'cross' && !e.cross) continue;
      }
      if (e.from.node?.hidden || e.to.node?.hidden) continue;
      frag.append(edgeLine(e, near));
    } else {
      frag.append(edgeLine(e, false, true));
    }
  }
  svg.append(frag);
}

function edgeLine(e, near, flow = false) {
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', edgePath(e));
  path.setAttribute('class',
    `cv-edge${e.inferred ? ' is-inferred' : ''}${e.cross ? ' is-cross' : ''}`
    + `${flow ? ' is-journey' : ''}${near ? ' is-near' : ''}`);
  const marker = flow ? 'cv-arrow-flow' : near ? 'cv-arrow-near' : e.cross ? 'cv-arrow-cross' : 'cv-arrow';
  path.setAttribute('marker-end', `url(#${marker})`);
  return path;
}

function arrowDefs() {
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  for (const [id, cls] of [
    ['cv-arrow', ''], ['cv-arrow-cross', 'is-cross'],
    ['cv-arrow-near', 'is-near'], ['cv-arrow-flow', 'is-journey'],
  ]) {
    const m = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
    m.setAttribute('id', id);
    m.setAttribute('viewBox', '0 0 10 10');
    m.setAttribute('refX', '9');
    m.setAttribute('refY', '5');
    m.setAttribute('markerWidth', '7');
    m.setAttribute('markerHeight', '7');
    m.setAttribute('orient', 'auto-start-reverse');
    const head = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    head.setAttribute('d', 'M 0 1 L 10 5 L 0 9 z');
    head.setAttribute('class', `cv-arrowhead ${cls}`);
    m.append(head);
    defs.append(m);
  }
  return defs;
}

const journeyPath = (id) =>
  (state.flows.find((f) => f.id === id)?.steps ?? [])
    .map((s) => s.screenId).filter(Boolean);

// ── the nodes ────────────────────────────────────────────────────────
function drawNodes() {
  // Bands are painted on their own layer *under* the links. They used to be
  // outlines in the node layer, and had to be, because `#nodes` sits over
  // `#edges` and a filled band hid every link crossing it. A layer of its own
  // buys the fill back: shelf, then links, then cards.
  const bandBox = $('bands');
  bandBox.replaceChildren();
  bandBox.style.width = `${state.extent.w}px`;
  bandBox.style.height = `${state.extent.h}px`;

  for (const b of state.blocks) {
    const band = el('div', 'cv-band');
    band.dataset.id = b.id;
    band.style.left = `${b.x}px`;
    band.style.top = `${b.y}px`;
    band.style.width = `${b.w}px`;
    band.style.height = `${b.h}px`;
    const head = el('div', 'cv-band-head');
    head.append(el('span', 'cv-band-label', b.label));
    head.append(el('span', 'cv-band-note', b.note));
    band.append(head);
    bandBox.append(band);
  }

  const box = $('nodes');
  box.replaceChildren();
  box.style.width = `${state.extent.w}px`;
  box.style.height = `${state.extent.h}px`;

  const frag = document.createDocumentFragment();
  for (const n of state.nodes) {
    const card = el('button', `cv-card${n.ghost ? ' is-ghost' : ''}${n.moved ? ' is-moved' : ''}`);
    card.type = 'button';
    card.style.left = `${n.x}px`;
    card.style.top = `${n.y}px`;
    card.style.width = `${n.w}px`;
    card.style.height = `${n.h}px`;
    card.dataset.id = n.id;
    card.title = n.ghost
      ? `${n.id} · ${n.screen.name ?? ''} — on ${n.screen.platform ?? 'another platform'}`
      : `${n.id} · ${n.screen.name ?? ''}`;

    // The step number, in a lane. It is the one thing a flow diagram must not
    // make you count.
    if (n.step) card.append(el('span', 'cv-step', String(n.step)));

    const shell = el('div', 'cv-frame');
    if (n.ghost) {
      shell.append(el('span', 'cv-noframe', `on ${n.screen.platform ?? '—'}`));
    } else if (!n.frame) {
      // Said, not left blank. An empty tile is read as a screen that failed to
      // load; this one has no drawing to fail.
      shell.append(el('span', 'cv-noframe', 'no board'));
    }
    card.append(shell);

    const label = el('div', 'cv-label');
    label.append(el('span', 'cv-id', n.id));
    label.append(el('span', 'cv-name', n.screen.name ?? ''));
    card.append(label);

    card.onclick = () => select(n.id);
    card.addEventListener('pointerenter', () => setHover(n.id));
    card.addEventListener('pointerleave', () => setHover(null));
    wireCardDrag(card, n);
    n.node = card;
    frag.append(card);
  }
  box.append(frag);
}

// Nothing is filtered any more. The platform decides what is drawn, and a
// journey is drawn as its own layout rather than as the same sheet with most of
// it hidden — hiding left the holes where the hidden cards were, which is a
// flow diagram with six blank pages in it.
function applyFilter() {
  paintEdges();
  schedulePaint();
  return state.nodes.filter((n) => !n.node?.hidden).length;
}

// ── the detail panel ─────────────────────────────────────────────────
function select(id) {
  state.selected = id;
  for (const n of state.nodes) n.node.classList.toggle('is-selected', n.id === id);
  paintEdges();
  drawDetail();
}

function closeDetail() {
  state.selected = null;
  for (const n of state.nodes) n.node.classList.remove('is-selected');
  $('detail').hidden = true;
  paintEdges();
}

function drawDetail() {
  const box = $('detail');
  const s = state.byId.get(state.selected);
  if (!s) { box.hidden = true; return; }
  box.hidden = false;
  box.replaceChildren();

  const head = el('div', 'cv-detail-head');
  head.append(el('span', 'cv-detail-id', s.id));
  const close = el('button', 'chip', 'Close');
  close.type = 'button';
  close.onclick = closeDetail;
  head.append(close);
  box.append(head);

  box.append(el('h2', 'cv-detail-name', s.name ?? s.id));
  box.append(el('p', 'cv-detail-where', `${s.platform} · ${s.platformName ?? ''} · ${s.module ?? ''}`));
  if (s.purpose) box.append(el('p', 'cv-detail-purpose', s.purpose));

  const facts = el('dl', 'cv-facts');
  const fact = (k, v) => { facts.append(el('dt', null, k)); facts.append(el('dd', null, v)); };
  fact('Wave', String(s.wave ?? '—'));
  fact('Operations', String((s.apis ?? []).length));
  fact('Permission', s.permission ?? 'none stated');
  fact('Offline', s.offlineCapable ? 'works offline' : 'needs the network');
  // The honest one. Two thirds of the screens are here, and a link drawn from a
  // guess should say so where somebody is reading the detail of it.
  fact('Navigation', s.navigationInferred
    ? 'inferred by the package, not declared'
    : 'declared in the screen');
  box.append(facts);

  // ── backlinks ──
  // Into the rest of the viewer rather than a second copy of it. Every one of
  // these is a route that already existed; the canvas only had no way to reach
  // them.
  const links = el('div', 'cv-links');
  const link = (href, text, blank = false) => {
    const a = el('a', 'chip', text);
    a.href = href;
    if (blank) { a.target = '_blank'; a.rel = 'noopener'; }
    links.append(a);
  };
  link(`/?layer=frontend&mode=screen&id=${encodeURIComponent(s.id)}`, 'Open in Frontend');
  link(`/#screen:${encodeURIComponent(s.id)}`, 'Deep link');
  const ref = frameRef(s);
  if (ref) {
    link(auth.pkgAsset(`/frame?board=${encodeURIComponent(ref.board)}&anchor=${encodeURIComponent(ref.anchor)}`),
      'The frame', true);
  }
  if (s.file) link(`/uiux.html`, 'Every board');
  box.append(links);

  const through = state.flows.filter((f) => (f.steps ?? []).some((st) => st.screenId === s.id));
  if (through.length) {
    box.append(el('h3', 'cv-detail-sub', `${through.length} journey${through.length === 1 ? '' : 's'} pass through here`));
    const list = el('div', 'cv-journey-links');
    for (const f of through.slice(0, 12)) {
      const b = el('button', 'chip', `${f.id} · ${f.name}`);
      b.type = 'button';
      b.onclick = () => pickJourney(f.id);
      list.append(b);
    }
    box.append(list);
  }

  const exits = s.navigation?.exitTo ?? [];
  if (exits.length) {
    // How many of them are off this sheet, said out loud. The canvas draws one
    // platform, so an exit into another one has no line — without this the
    // screen looks like a dead end when it is a doorway.
    const away = exits.filter((to) => state.byId.get(to)?.platform !== state.platform).length;
    box.append(el('h3', 'cv-detail-sub',
      away ? `Leads to ${exits.length} · ${away} on another platform` : `Leads to ${exits.length}`));
    const list = el('div', 'cv-journey-links');
    for (const to of exits.slice(0, 16)) {
      const target = state.byId.get(to);
      const off = target && target.platform !== state.platform;
      const b = el('button', `chip${off ? ' is-away' : ''}`,
        `${to} · ${target?.name ?? '—'}${off ? ` ↗ ${target.platform}` : ''}`);
      b.type = 'button';
      if (off) b.title = `On ${target.platform} — opening it changes the sheet`;
      b.onclick = () => {
        // Crossing over rather than refusing to. The sheet is swapped first,
        // which rebuilds the nodes, and only then is the screen picked — so
        // `centreOn` has something to centre on.
        if (off) setPlatform(target.platform);
        select(to);
        centreOn(to);
      };
      list.append(b);
    }
    box.append(list);
  }
}

/**
 * Drag one card.
 *
 * On the card rather than on the viewport, and `stopPropagation` on the way in,
 * because the viewport is itself a drag surface — without that, moving a card
 * would pan the sheet under it and the card would appear not to move at all.
 *
 * The pointer delta is divided by the zoom: at 40% a hundred pixels of mouse is
 * two hundred and fifty of world, and a card that lags the cursor at one zoom
 * and outruns it at another is a control nobody trusts.
 *
 * A drag that goes nowhere is a click. Six pixels is the same threshold the
 * viewport uses to tell a pan from a tap, so the two agree about what a click
 * is.
 */
function wireCardDrag(card, n) {
  let from = null;
  let moved = 0;

  card.addEventListener('pointerdown', (e) => {
    if (e.button !== 0) return;
    e.stopPropagation();                 // the viewport must not also pan
    from = { px: e.clientX, py: e.clientY, x: n.x, y: n.y };
    moved = 0;
    card.setPointerCapture(e.pointerId);
  });

  card.addEventListener('pointermove', (e) => {
    if (!from) return;
    const dx = e.clientX - from.px;
    const dy = e.clientY - from.py;
    moved = Math.max(moved, Math.abs(dx) + Math.abs(dy));
    if (moved <= 6) return;
    card.classList.add('is-dragging');
    setHover(null);
    n.x = from.x + dx / state.view.k;
    n.y = from.y + dy / state.view.k;
    card.style.left = `${n.x}px`;
    card.style.top = `${n.y}px`;
    // Live, so the links follow the card rather than snapping to it on drop.
    paintEdges();
  });

  const drop = (e) => {
    if (!from) return;
    const wasDrag = moved > 6;
    from = null;
    card.classList.remove('is-dragging');
    try { card.releasePointerCapture(e.pointerId); } catch { /* already gone */ }
    if (!wasDrag) return;
    card.classList.add('is-moved');
    n.moved = true;
    const map = readMoved();
    map[n.key] = [Math.round(n.x), Math.round(n.y)];
    writeMoved(map);
    // A card dragged past the old edge grows the world; without this its links
    // would be clipped at the boundary the layout happened to leave.
    state.extent = extentOf(state.blocks, state.nodes);
    $('nodes').style.width = `${state.extent.w}px`;
    $('nodes').style.height = `${state.extent.h}px`;
    paintEdges();
    schedulePaint();
  };
  card.addEventListener('pointerup', drop);
  card.addEventListener('pointercancel', drop);

  // A drag that ends on the card must not also open it.
  card.addEventListener('click', (e) => {
    if (moved > 6) { e.stopPropagation(); e.preventDefault(); }
  }, true);
}

/** Forget this sheet's moves and lay it out again. */
function resetLayout() {
  writeMoved({});
  buildSheet();
  noteSheet();
}

// ── moving about ─────────────────────────────────────────────────────
/**
 * The fit that runs a frame after the sheet is built, and the token that lets a
 * deliberate move outrun it.
 *
 * `fit` has to be deferred — the viewport is a flex child with no height at the
 * moment the sheet is drawn, and measured then it fits to a box of the wrong
 * size. But following an exit into another platform *also* builds a sheet, and
 * without this the pending fit would land a frame later and throw away the
 * screen the reader just asked for.
 */
let fitQueued = 0;
function queueFit() {
  const token = ++fitQueued;
  requestAnimationFrame(() => requestAnimationFrame(() => { if (token === fitQueued) fit(); }));
}

function centreOn(id) {
  const n = state.nodes.find((x) => x.id === id);
  if (!n) return;
  fitQueued += 1;              // outrun any fit still queued behind a rebuild
  const box = $('viewport').getBoundingClientRect();
  const k = Math.max(state.view.k, FRAME_ZOOM);
  state.view.k = k;
  state.view.x = box.width / 2 - (n.x + n.w / 2) * k;
  state.view.y = box.height / 2 - (n.y + n.h / 2) * k;
  applyView();
  schedulePaint();
}

function fit() {
  const box = $('viewport').getBoundingClientRect();
  const visible = state.nodes.filter((n) => !n.node?.hidden);
  const area = visible.length
    ? {
        x0: Math.min(...visible.map((n) => n.x)) - 60,
        y0: Math.min(...visible.map((n) => n.y)) - 90,
        x1: Math.max(...visible.map((n) => n.x + n.w)) + 60,
        y1: Math.max(...visible.map((n) => n.y + n.h)) + 60,
      }
    : { x0: 0, y0: 0, x1: state.extent.w, y1: state.extent.h };
  const k = Math.min(box.width / (area.x1 - area.x0), box.height / (area.y1 - area.y0));
  state.view.k = Math.max(0.06, Math.min(2, k));
  state.view.x = box.width / 2 - ((area.x0 + area.x1) / 2) * state.view.k;
  state.view.y = box.height / 2 - ((area.y0 + area.y1) / 2) * state.view.k;
  applyView();
  schedulePaint();
}

function zoomBy(factor, cx, cy) {
  const box = $('viewport').getBoundingClientRect();
  const px = cx ?? box.width / 2;
  const py = cy ?? box.height / 2;
  const k0 = state.view.k;
  const k1 = Math.max(0.06, Math.min(2.5, k0 * factor));
  // Hold the point under the cursor still, which is what makes a wheel zoom
  // feel like moving a map rather than resizing a picture.
  state.view.x = px - ((px - state.view.x) / k0) * k1;
  state.view.y = py - ((py - state.view.y) / k0) * k1;
  state.view.k = k1;
  applyView();
  schedulePaint();
}

function wireViewport() {
  const vp = $('viewport');
  let dragging = false;
  let last = null;
  let moved = 0;

  vp.addEventListener('pointerdown', (e) => {
    if (e.button !== 0) return;
    dragging = true; moved = 0;
    last = { x: e.clientX, y: e.clientY };
    vp.setPointerCapture(e.pointerId);
    vp.classList.add('is-dragging');
  });
  vp.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const dx = e.clientX - last.x;
    const dy = e.clientY - last.y;
    moved += Math.abs(dx) + Math.abs(dy);
    state.view.x += dx; state.view.y += dy;
    last = { x: e.clientX, y: e.clientY };
    applyView();
    schedulePaint();
  });
  const stop = (e) => {
    if (!dragging) return;
    dragging = false;
    vp.classList.remove('is-dragging');
    try { vp.releasePointerCapture(e.pointerId); } catch { /* already gone */ }
  };
  vp.addEventListener('pointerup', stop);
  vp.addEventListener('pointercancel', stop);
  // A drag that ends on a card must not also open it.
  vp.addEventListener('click', (e) => { if (moved > 6) { e.stopPropagation(); e.preventDefault(); } }, true);

  vp.addEventListener('wheel', (e) => {
    e.preventDefault();
    const box = vp.getBoundingClientRect();
    zoomBy(Math.exp(-e.deltaY * 0.0016), e.clientX - box.left, e.clientY - box.top);
  }, { passive: false });

  vp.addEventListener('keydown', (e) => {
    const step = e.shiftKey ? 240 : 80;
    if (e.key === 'ArrowLeft') { state.view.x += step; }
    else if (e.key === 'ArrowRight') { state.view.x -= step; }
    else if (e.key === 'ArrowUp') { state.view.y += step; }
    else if (e.key === 'ArrowDown') { state.view.y -= step; }
    else if (e.key === '+' || e.key === '=') { zoomBy(1.2); return; }
    else if (e.key === '-') { zoomBy(1 / 1.2); return; }
    else if (e.key === 'Escape') { closeDetail(); return; }
    else return;
    e.preventDefault();
    applyView();
    schedulePaint();
  });

  new ResizeObserver(() => schedulePaint()).observe(vp);
}

// ── the rail ─────────────────────────────────────────────────────────
function pickJourney(id) {
  state.journey = state.journey === id ? null : id;
  for (const row of $('rail-journeys').querySelectorAll('.cv-row')) {
    row.classList.toggle('is-on', row.dataset.id === state.journey);
  }
  buildSheet();
  noteSheet();
}

/**
 * Draw one platform's worth of sheet.
 *
 * Everything downstream of the platform is rebuilt rather than filtered: the
 * layout, the cards, the links. A filtered layout keeps the holes where the
 * hidden platforms were, which is how the first cut ended up unable to fit
 * anything above 8%.
 */
function buildSheet() {
  const flow = state.journey ? state.flows.find((f) => f.id === state.journey) : null;
  const built = flow ? laneLayout(flow) : boardLayout(screensOn(state.platform));
  state.blocks = built.blocks;
  state.nodes = built.nodes;
  state.extent = built.extent;
  state.edges = flow ? laneEdges(state.nodes) : buildEdges(state.nodes);
  state.selected = null;
  $('detail').hidden = true;
  document.body.classList.toggle('is-lane', Boolean(flow));
  drawNodes();
  applyFilter();
  queueFit();
}

function noteSheet() {
  if (state.journey) {
    const j = journeysOn(state.platform).find((x) => x.flow.id === state.journey);
    $('canvas-note').textContent = j && j.on < j.steps
      ? `${state.journey} · ${j.steps} steps, ${j.on} on ${state.platform}`
      : `${state.journey} · ${state.nodes.length} steps`;
    return;
  }
  const screens = screensOn(state.platform);
  const inferred = screens.filter((s) => s.navigationInferred).length;
  const flows = journeysOn(state.platform);
  const crossings = state.edges.filter((e) => e.cross).length;
  $('canvas-note').textContent =
    `${state.platform} · ${screens.length} screens in ${state.blocks.length} modules`
    + ` · ${state.edges.length} links, ${crossings} crossing a module`
    + ` · ${flows.length} journeys · ${inferred} screens' navigation inferred`;
}

/**
 * Change the sheet.
 *
 * Kept in the address so a platform can be sent to somebody, and in storage so
 * coming back lands where you left rather than on P01 every time.
 */
function setPlatform(id) {
  if (!id || id === state.platform) return;
  state.platform = id;
  state.journey = null;
  try { localStorage.setItem('aster-canvas-platform', id); } catch { /* denied outright */ }
  const url = new URL(location.href);
  url.searchParams.set('platform', id);
  history.replaceState(null, '', url);
  const select = $('platform');
  if (select && select.value !== id) select.value = id;
  buildSheet();
  drawRail();
  noteSheet();
}

function drawRail() {
  // **Platforms first, and always on screen.** The rail used to open on a list
  // of every journey in the package and a list of every screen in it, neither
  // of which is a thing a reader is looking for until they have said which
  // platform they are reviewing. It is the first question, so it is the first
  // list, and it does not go away when one is picked.
  const pbox = $('rail-platforms');
  pbox.replaceChildren();
  for (const p of state.platforms) {
    const row = el('button', 'ux-row is-tall cv-row');
    row.type = 'button';
    row.dataset.id = p.id;
    row.append(el('span', 'ux-row-code', p.id));
    row.append(el('span', 'ux-row-label', p.name));
    row.append(el('span', 'ux-row-meta',
      `${p.screens} screen${p.screens === 1 ? '' : 's'} · ${p.journeys} journey${p.journeys === 1 ? '' : 's'}`));
    row.classList.toggle('is-on', p.id === state.platform);
    row.onclick = () => setPlatform(p.id);
    pbox.append(row);
  }
  $('count-platforms').textContent = String(state.platforms.length);

  const here = state.platforms.find((p) => p.id === state.platform);
  $('rail-scope').textContent = here ? `on ${here.id} — ${here.name}` : '';

  const jbox = $('rail-journeys');
  jbox.replaceChildren();
  const flows = journeysOn(state.platform);
  for (const { flow, steps, on } of flows) {
    const row = el('button', 'ux-row is-tall cv-row');
    row.type = 'button';
    row.dataset.id = flow.id;
    row.append(el('span', 'ux-row-code', flow.id));
    row.append(el('span', 'ux-row-label', flow.name ?? ''));
    row.append(el('span', 'ux-row-meta',
      on === steps ? `${steps} steps` : `${on} of ${steps} steps here`));
    row.classList.toggle('is-on', flow.id === state.journey);
    row.onclick = () => pickJourney(flow.id);
    jbox.append(row);
  }
  $('count-journeys').textContent = String(flows.length);
  if (!flows.length) jbox.append(el('p', 'ux-none', 'No journey passes through this platform.'));

  const sbox = $('rail-screens');
  sbox.replaceChildren();
  for (const s of screensOn(state.platform)) {
    const row = el('button', 'ux-row is-tall cv-row');
    row.type = 'button';
    row.dataset.id = s.id;
    row.append(el('span', 'ux-row-code', s.id));
    row.append(el('span', 'ux-row-label', s.name ?? ''));
    row.append(el('span', 'ux-row-meta', `wave ${s.wave ?? '—'} · ${s.module ?? ''}`));
    row.onclick = () => { select(s.id); centreOn(s.id); };
    sbox.append(row);
  }
  $('count-screens').textContent = String(screensOn(state.platform).length);
}

function wireRail() {
  const tabs = [['tab-journeys', 'rail-journeys', 'journeys'], ['tab-screens', 'rail-screens', 'screens']];
  for (const [tabId, boxId, name] of tabs) {
    $(tabId).onclick = () => {
      state.tab = name;
      for (const [t, b] of tabs.map((x) => [x[0], x[1]])) {
        const on = t === tabId;
        $(t).classList.toggle('is-on', on);
        $(t).setAttribute('aria-selected', String(on));
        $(b).hidden = !on;
      }
    };
  }

  attachSubSearch($('rail-filter'), [
    { box: $('rail-platforms'), rows: '.cv-row' },
    { box: $('rail-journeys'), rows: '.cv-row' },
    { box: $('rail-screens'), rows: '.cv-row' },
  ], { onEmpty: 'Nothing here matches that.', count: $('rail-count') });
}

// ── boot ─────────────────────────────────────────────────────────────
(async function start() {
  await auth.requireSignIn();
  const me = auth.account();
  // Optional: inside the viewer these views are sections of a page that
  // already says who you are, so there is no `#whoami` to fill.
  $('whoami')?.replaceChildren(me ? `${me.name || me.email} · ${me.role}` : '');

  try {
    const journeys = await json('/api/journeys');
    state.screens = (journeys.screens ?? []).slice()
      .sort((a, b) => a.id.localeCompare(b.id));
    state.flows = (journeys.flows ?? []).slice()
      .sort((a, b) => a.id.localeCompare(b.id));
    state.byId = new Map(state.screens.map((s) => [s.id, s]));

    state.platforms = [...new Set(state.screens.map((s) => s.platform))].sort()
      .map((id) => ({
        id,
        name: state.screens.find((s) => s.platform === id)?.platformName ?? id,
        screens: screensOn(id).length,
        journeys: journeysOn(id).length,
      }));
    if (!state.platforms.length) throw new Error('the package names no platforms');

    for (const p of state.platforms) {
      const option = el('option', null, `${p.id} — ${p.name} · ${p.screens}`);
      option.value = p.id;
      $('platform').append(option);
    }

    // Where to land. The address wins — a link to a platform has to open that
    // platform — then wherever this reader was last, then the first one. There
    // is no "everything" to fall back to any more, and that is the point.
    const asked = new URLSearchParams(location.search).get('platform');
    const last = (() => { try { return localStorage.getItem('aster-canvas-platform'); } catch { return null; } })();
    const known = (id) => state.platforms.some((p) => p.id === id);
    state.platform = (known(asked) && asked) || (known(last) && last) || state.platforms[0].id;
    $('platform').value = state.platform;

    wireRail();
    wireViewport();
    buildSheet();
    drawRail();
    noteSheet();

    state.links = $('links-mode').value;
    state.showInferred = $('show-inferred').checked;

    $('platform').onchange = (e) => setPlatform(e.target.value);
    $('links-mode').onchange = (e) => { state.links = e.target.value; paintEdges(); };
    $('show-inferred').onchange = (e) => { state.showInferred = e.target.checked; paintEdges(); };
    $('zoom-in').onclick = () => zoomBy(1.25);
    $('zoom-out').onclick = () => zoomBy(1 / 1.25);
    $('zoom-fit').onclick = () => fit();
    // Inside the viewer this view is a section that is `hidden` until its tab
    // is picked, and a hidden section measures zero — so the fit that runs at
    // boot fits to nothing and the sheet opens off the edge of the screen.
    // `setMode` calls this once the section is actually on screen.
    window.__canvasFit = () => queueFit();
    $('reset-layout').onclick = resetLayout;
    $('show-board').onclick = () => {
      if (!state.journey) { fit(); return; }
      state.journey = null;
      for (const row of $('rail-journeys').querySelectorAll('.cv-row')) row.classList.remove('is-on');
      buildSheet();
      noteSheet();
    };
  } catch (e) {
    $('canvas-note').textContent = `Could not read the package: ${e.message}`;
  } finally {
    hideLoader();
  }
})();
