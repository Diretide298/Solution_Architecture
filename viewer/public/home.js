/**
 * The door.
 *
 * Five bodies in space, one per layer of the delivery package, that you scroll
 * through, click into and back out of. It answers "what is in here" in one
 * picture before anybody has clicked anything, and then hands them to the
 * viewer at the layer they picked.
 *
 * The renderer is `galaxy.js` — the same engine the Events sphere and the two
 * join maps use, at a different scale. Nothing here draws: this file builds a
 * model, moves the camera, and keeps the chrome in step with it.
 *
 * Two things are the whole argument of the layout and are not decoration:
 *
 *   Contracts sits at the origin, nearest the reader, and is the only amber
 *   body. The package's claim is that the API is the join between the outer
 *   layers, and the arrangement says it rather than captioning it.
 *
 *   Labels alternate above and below. The scene turns, so any two labels in
 *   the same horizontal band will collide eventually; alternating removes the
 *   class of collision rather than nudging until one frame looks right.
 */
import { Galaxy } from './galaxy.js';
import { LAYERS, $ } from './core.js';
import { hideLoader, loaderSays } from './loader.js';
import * as auth from './validation.js';
import { setTheme } from './theme.js';
import { mountPhoneBar } from './page-chrome.js';

// ── the layout ──────────────────────────────────────────────────────
/**
 * Where each layer sits, and which side of it its name goes.
 *
 * `tier` is the engine's colour, not a claim about importance: `core` is the
 * amber, and Contracts is the only thing here that should be amber.
 *
 * `flat` is the 2D arrangement — Contracts centred, the other four on the
 * corners. It is given rather than derived for the same reason `pos` is: an
 * even ring would spread the satellites evenly and say nothing about which one
 * the other four resolve against.
 */
// The z is negated from the design's table. LANDING.md reads +z as towards the
// reader — it puts Contracts at +0.55 and calls it "nearest the viewer" — and
// galaxy.js reads the opposite: "negative z is towards the viewer throughout".
// Copied across unchanged, that put the one body the whole layout is an
// argument about at the *back*, and hid its contents behind the depth cull that
// keeps far-side labels off the screen.
const LAYOUT = {
  frontend:  { pos: [-1.45,  0.78,  0.50], flat: [-0.82, -0.58], up: true,  tier: 'spine' },
  contracts: { pos: [ 0.00, -0.05, -0.55], flat: [ 0.00,  0.00], up: false, tier: 'core' },
  domain:    { pos: [ 1.50,  0.72,  0.25], flat: [ 0.82, -0.58], up: true,  tier: 'spine' },
  backend:   { pos: [ 1.15, -0.88, -0.20], flat: [ 0.82,  0.58], up: false, tier: 'satellite' },
  decisions: { pos: [-1.35, -0.92,  0.55], flat: [-0.82,  0.58], up: false, tier: 'spine' },
  // Below the square and behind Contracts, on the axis rather than on the ring.
  // A fifth satellite would make the four corners a pentagon, and an even ring
  // says nothing about which body the others resolve against — which is the
  // whole point of the arrangement above. It is also true of the thing: this is
  // not a fifth kind of artefact, it is a cut through two of the others.
  services:  { pos: [ 0.10, -1.55, -0.30], flat: [ 0.00,  0.86], up: false, tier: 'satellite' },
  // Outside Frontend, on the same side, further from the centre. It has one
  // lane and that lane goes to Frontend: a board resolves against a screen and
  // against nothing else. Placing it out past the corner it hangs off says that
  // — it is the only body here that does not reach Contracts, and it should not
  // look like it does.
  //
  // Missing from this table, `LAYOUT[key].tier` threw while the focus panel was
  // being built, so the row was in the rail, the body was in the graph, and
  // clicking either opened an empty panel and killed the page's scripts.
  uiux:      { pos: [-2.30,  1.52,  0.85], flat: [-1.34, -0.95], up: true,  tier: 'satellite' },
  // Out past Architecture on the same side, for the same reason UI/UX sits
  // out past Frontend: it hangs off one body and reaches nothing else, and
  // a position among the six would draw joins that are not there.
  cicd:      { pos: [ 2.55, -1.42, -0.70], flat: [ 1.46, -1.02], up: false, tier: 'satellite' },
};

/** What the headline number counts, and where on disk it comes from. */
const UNITS = {
  frontend:  { unit: 'screens',      from: 'screens/ · flows/ · frontend/ · wireframes/' },
  uiux:      { unit: 'design boards', from: 'wireframes/ · designs/ · ui-design/' },
  cicd:      { unit: 'delivery artefacts', from: 'repos/ · services/ · deploy/' },
  contracts: { unit: 'contracts',    from: 'the OpenAPI contracts' },
  // State models, not status enums. A status enum is a list of values a
  // contract declares — it is not a lifecycle, and under a layer named for
  // lifecycles the number should be the thing the name promises.
  domain:    { unit: 'state models',  from: 'states/ · events/' },
  backend:   { unit: 'tables',       from: 'backend/ · handoff/' },
  decisions: { unit: 'ADRs',         from: 'docs/' },
  services:  { unit: 'designs',      from: 'diagrams/ · the schema workbook' },
};

/**
 * A line per layer, for the panel.
 *
 * Deliberately not core.js's `hint`, which is a tab-strip subtitle written for
 * somebody already inside the viewer and reads as a fragment out here. These
 * are written for a reader who has not opened anything yet.
 */
const BLURB = {
  frontend:
    'What a person sees. Every screen, the journeys that string them together, and which app '
    + 'builds each one — with every operation a screen names resolved against the contracts.',
  uiux:
    'What has actually been drawn, and what has not. Every design board on disk — including the '
    + 'ones no screen points at — the screens of a platform on one canvas, and the gap between '
    + 'the screens each app names and the ones somebody has drawn.',
  contracts:
    'The API, and the join between every other layer. Hand-authored; servers and clients are '
    + 'generated from it, never the reverse, so everything else here is drawn by resolving '
    + 'against it.',
  domain:
    'What can happen to a thing, and in what order. A state model is a lifecycle within one '
    + 'entity and an event is one crossing between two — the two artefacts check each other: '
    + 'which moves between statuses are legal, and what goes through the outbox when one happens.',
  backend:
    'The database. Versioned SQL checked against the schema reference, so a table that exists '
    + 'can be told from one that is only planned — and every table traces back to the contract '
    + 'schema it came from.',
  decisions:
    'Why the shape is the shape. Everything else here is machine-readable and can be checked '
    + 'mechanically; this is prose, and prose is where the reasons live.',
  cicd:
    'How a commit becomes a running venue. What a pull request has to pass, what each service '
    + 'becomes when it is built, and which of the four deployments it lands in — read off the '
    + 'three folders that hold those answers, and compared, because none of them knows what the '
    + 'other two say.',
  services:
    'What ships together. Sixteen deployable services in five tiers, cut where the data '
    + 'boundary falls — no service spans a schema it does not own — with every place one '
    + 'writes another\u2019s tables, and the order they have to deploy in.',
};

/**
 * The links, and the direction each one runs.
 *
 * Every lane that touches Contracts is critical, which is the same statement
 * the position makes and is worth making twice: those four are the joins the
 * API is, and the other two are the shortcuts between neighbours.
 */
const LINKS = [
  ['frontend', 'contracts'],
  // One lane, to Frontend. UI/UX draws the screens that layer declares and
  // nothing else — a board resolves against a screen, never against a contract
  // or a table — so joining it any further would draw a relation that is not
  // there. Same argument as the two Services lanes below.
  ['uiux', 'frontend'],
  ['contracts', 'domain'],
  ['contracts', 'backend'],
  ['contracts', 'decisions'],
  ['domain', 'backend'],
  ['backend', 'decisions'],
  // Two lanes, not four. Services is a cut through the contracts and the
  // tables, and joining it to anything else would draw a relation that is not
  // there.
  ['contracts', 'services'],
  ['backend', 'services'],
  // One lane, to Architecture. Delivery is a cut through the services — what
  // builds them, what they become, where they run — and it reaches nothing
  // else here directly.
  ['services', 'cicd'],
];

const ORDER = ['frontend', 'uiux', 'contracts', 'domain', 'backend', 'services', 'cicd', 'decisions'];

// Six bodies in a full viewport, against thirty on a ring inside a panel.
// Same formula, three times the scale — see `spread` in galaxy.js.
//
// 3.0 is as far as the spread goes before `roomFor` starts clamping it: past
// that the two largest bodies both hit the ceiling set by the gap to their
// nearest neighbour, and Frontend against Decisions stops reading as 14:1 and
// starts reading as 1.2:1 — which is the one thing the sizes are for.
const SPREAD = 3;
const CEILING = 420;
// Five clusters sharing 900 motes is ~180 each over a 200px ball, which draws
// a wireframe rather than a body.
const BUDGET = 1700;
const MOTE_GAIN = 1.3;
// **The scale the overview opens at.** One knob, and the only one to touch when
// the constellation stops fitting.
//
// It was 1 while the page carried six bodies. It now carries eight, and the ring
// grew to seat them: the two ends of it — CI/CD out to the left, UI/UX down to
// the right — reached past the window and the reader arrived already inside the
// picture, having to scroll out before they could see what it was of.
//
// **Zoom rather than spread, deliberately.** Pulling the bodies together would
// have fitted them too, and would have cost the thing the layout is for: at
// SPREAD 3 the largest body reads 14:1 against the smallest, and past that
// `roomFor` starts clamping and the ratio collapses toward 1.2:1. The bodies are
// the right size and in the right places; the frame was too close.
//
// Expect to revisit it the next time a layer is added — the constellation widens
// each time, and nothing here measures itself.
const ZOOM = 0.78;

const HINTS = {
  overview: 'Click a layer  ·  ↑ ↓ to step through  ·  drag to turn, scroll to zoom',
  focused: 'Click again or press Enter to open it  ·  Esc to back out',
  zoomed: 'Zoomed in — the names are what each layer actually holds  ·  Esc to reset',
};

// ── state ───────────────────────────────────────────────────────────
const state = {
  counts: {},
  detail: {},
  items: {},
  focus: null,      // a layer key, or null for the overview
  mode: '3d',
};

let scene = null;

/**
 * The phone layout, by the same query as home.css (keep the two in step).
 *
 * On a phone the scene is the same live scene as the desktop's (same engine,
 * same model, same bodies and colours) in a band of its own, turned and zoomed
 * by touch through galaxy.js. What differs is what a battery asks for:
 *
 *   it draws only while something moves (a finger, a throw, a camera flight,
 *   the one turn it makes on arrival) and parks otherwise, so it does not spin
 *   by itself; it parks when the band is scrolled away or the page is hidden;
 *   under reduced motion it never turns by itself and a focus jumps to its pose.
 *
 * The band leaves vertical swipes to the page (`touch-action: pan-y` in
 * home.css): a sideways drag turns the scene, a pinch zooms it, a tap picks a
 * layer. Explore opens the same canvas full screen with every gesture.
 */
const PHONE = window.matchMedia('(max-width: 600px), (pointer: coarse)');
const phone = () => PHONE.matches;
const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)');

/**
 * Where the camera puts things, as fractions of the canvas width (galaxy.js
 * CAM_AT and CAM_AT_FOCUS): the overview's centre at 0.58, a focused body at
 * 0.66. Both are biased right to clear the desktop's hero copy, which a phone
 * does not have. So on a phone the canvas is wider than its band and slid, by
 * CSS, until the point that matters is the band's middle: the overview's
 * centre at rest, the focused body once one is chosen. home.css sizes the
 * canvas at CANVAS_SPAN of the band and offsets it so 0.58 lands mid-band;
 * keep the two in step.
 */
const CANVAS_SPAN = 1.5;
const CAM_AT_X = 0.58;
const CAM_FOCUS_X = 0.66;

/** The share of the band the overview is fitted to, across and down. */
const FIT_ACROSS = 0.9;
const FIT_DOWN = 0.78;

/** The turn the scene makes once on arrival, in radians, and how long it takes. */
const INTRO_TURN = 0.75;
const INTRO_MS = 1600;

const HINT_BAND = 'Swipe sideways to turn it. Tap a layer.';
const HINT_FULL = 'Drag to turn. Pinch to zoom. Tap a layer.';
const PHONE_SCENE_LABEL = 'The layers of the delivery package, drawn as a constellation you can turn, zoom and tap. '
  + 'The list of layers below does the same.';
let deskLabel = '';

/** The phone's pacing: whether the scene may draw, and whether it has a reason to. */
const pace = { on: false, seen: true, intro: false, flightMax: 0 };
let exploring = false;
let hashAfterPop = false;

/**
 * Leave Home for `url`. From the full-screen view the page goes in place of
 * that view's history entry: left behind, it would come back as Home with
 * nothing open, and the first Back from it would seem to do nothing.
 */
function leave(url) {
  if (exploring) location.replace(url);
  else location.href = url;
}
/** The phone's bottom bar (page-chrome.js), once mounted. */
let phoneBar = null;

/**
 * Park the loop after any frame where nothing moved.
 *
 * galaxy.js keeps its loop running for as long as the scene turns by itself,
 * which is right for a desktop and wrong for a battery. Rather than a second
 * loop, the scene's own `draw` is wrapped: after each frame on a phone, if no
 * finger is down, no throw or camera flight is running and the arrival turn is
 * over (or the band is off screen, or the page hidden), the loop is stopped.
 * Anything that moves it again calls `start()`, which every input path in
 * galaxy.js already does. The stop is queued as a microtask because the loop
 * schedules its next frame straight after `draw` returns.
 */
function pacer() {
  const draw = scene.draw.bind(scene);
  scene.draw = () => {
    draw();
    if (!pace.on) return;
    const flight = scene._flight ?? 0;
    pace.flightMax = Math.max(pace.flightMax, flight);
    const flying = flight < pace.flightMax || Boolean(scene._warp);
    const moving = scene.gesturing() || flying || pace.intro;
    syncReset();
    if (moving && pace.seen && !document.hidden) return;
    queueMicrotask(() => {
      if (scene.gesturing() && pace.seen && !document.hidden) return;
      scene.stop();
    });
  };
}

/** Under reduced motion a focus does not fly: the camera jumps to its pose. */
function land() {
  if (!REDUCED.matches) return;
  // galaxy.js paints a held scene once, in `setFocus`, before this runs; the
  // frame that shows the arrival is this one.
  scene._flight = Number.MAX_VALUE;
  scene.draw();
}

/**
 * Fit the overview to the band, from the frame itself: draw it, read the
 * bodies' projected extent back from the hit list the draw fills, and scale.
 * The result becomes the zoom Reset comes back to. Only at the overview, at
 * rest: a focus or a hand on the camera would measure the wrong picture.
 */
function fitPhone() {
  const view = document.querySelector('.home-stage-view');
  const band = view?.getBoundingClientRect();
  if (!band?.width || !band.height || scene.focusId || exploring) return;
  choosePose(band.width, band.height);
  const guess = 0.6;
  scene.spin = { yaw: 0, pitch: 0 };
  scene.baseZoom = scene.zoom = guess;
  scene._lastFrame = null;
  scene.draw();
  let hubs = scene._screen ?? [];
  if (!hubs.length) return;
  // A hub's `r` is the hit radius, two thirds of its cloud; the cloud is what shows.
  const reach = (h) => h.r * 1.5;
  const extent = () => ({
    left: Math.min(...hubs.map((h) => h.sx - reach(h))),
    right: Math.max(...hubs.map((h) => h.sx + reach(h))),
    top: Math.min(...hubs.map((h) => h.sy - reach(h))),
    bottom: Math.max(...hubs.map((h) => h.sy + reach(h))),
  });
  let at = extent();
  const fit = Math.min(
    (band.width * FIT_ACROSS) / (at.right - at.left),
    (band.height * FIT_DOWN) / (at.bottom - at.top));
  scene.baseZoom = scene.zoom = Math.max(0.35, Math.min(1.2, guess * fit));
  scene._lastFrame = null;
  scene.draw();
  hubs = scene._screen ?? [];
  at = extent();
  // What is left to centre, in the band's own pixels, held to a small slide:
  // the turn pivots on the engine's origin, and a long slide would turn the
  // scene round a point visibly off the middle.
  const canvasLeft = $('home-scene').offsetLeft;
  const midX = (at.left + at.right) / 2 + canvasLeft;
  const midY = (at.top + at.bottom) / 2;
  pace.dx = Math.max(-0.1 * band.width, Math.min(0.1 * band.width, band.width / 2 - midX));
  pace.dy = Math.max(-0.1 * band.height, Math.min(0.1 * band.height, band.height / 2 - midY));
}

/**
 * Which way round the constellation faces a portrait band, chosen once.
 *
 * The desktop turns all the time, so every heading is "the" constellation.
 * A phone holds still between touches, so it holds the heading that reads
 * best in a tall, narrow band: of 36 headings round the vertical axis, the
 * one whose closest two bodies end up furthest apart on screen once the
 * whole thing is fitted, which is the one whose names collide least. The
 * projection is the engine's (galaxy.js `project`) at the camera's resting
 * tilt, without its slight perspective, which does not change the answer.
 */
function choosePose(bandW, bandH) {
  const hubs = scene.model?.hubs ?? [];
  if (hubs.length < 2) return;
  const tilt = -0.2;   // galaxy.js CAM_PITCH_BASE
  const cp = Math.cos(tilt);
  const sp = Math.sin(tilt);
  let best = null;
  for (let i = 0; i < 36; i++) {
    const yaw = (i / 36) * Math.PI * 2;
    const c = Math.cos(yaw);
    const s = Math.sin(yaw);
    const pts = hubs.map((h) => {
      const z1 = -h.x * s + h.z * c;
      return { x: h.x * c + h.z * s, y: h.y * cp - z1 * sp, r: h.cr ?? 0 };
    });
    const wide = Math.max(...pts.map((p) => p.x + p.r)) - Math.min(...pts.map((p) => p.x - p.r));
    const tall = Math.max(...pts.map((p) => p.y + p.r)) - Math.min(...pts.map((p) => p.y - p.r));
    const scale = Math.min((bandW * FIT_ACROSS) / wide, (bandH * FIT_DOWN) / tall);
    let gap = Infinity;
    for (let a = 0; a < pts.length; a++) {
      for (let b = a + 1; b < pts.length; b++) {
        gap = Math.min(gap, Math.hypot(pts[a].x - pts[b].x, pts[a].y - pts[b].y));
      }
    }
    const score = gap * scale;
    if (!best || score > best.score) best = { yaw, score };
  }
  scene._yaw = best.yaw;
}

/**
 * Slide the canvas so the thing that matters is mid-band: the overview's
 * centre, or the focused body. A CSS transition carries it over the same time
 * as the camera's flight (none under reduced motion).
 */
function placeCanvas() {
  const canvas = $('home-scene');
  const view = canvas.parentElement;
  if (!phone()) { canvas.style.transform = ''; return; }
  const [x, y] = scene.focusId
    ? [-(CAM_FOCUS_X - CAM_AT_X) * CANVAS_SPAN * view.clientWidth, 0]
    : [pace.dx ?? 0, pace.dy ?? 0];
  canvas.style.transform = `translate3d(${x.toFixed(1)}px, ${y.toFixed(1)}px, 0)`;
}

/**
 * The counts under the names. On a desktop each body carries its count; in a
 * phone's band eight names and eight counts in 10px type collide, and the
 * count of the one being looked at is on its card, larger. Names stay.
 */
function setCounts(on) {
  for (const hub of scene.model?.hubs ?? []) {
    if (hub.fullSub === undefined) hub.fullSub = hub.sub;
    hub.sub = on ? hub.fullSub : '';
  }
}

/** The one orchestrated moment: on arrival the scene turns into its pose, once. */
function intro() {
  if (REDUCED.matches || pace.intro) return;
  pace.intro = true;
  const t0 = performance.now();
  const ease = (u) => 1 - (1 - u) ** 3;
  const step = (now) => {
    if (!pace.intro) return;
    const u = Math.min(1, (now - t0) / INTRO_MS);
    // A finger on it takes over: the turn so far is kept, the rest is dropped.
    if (scene.gesturing()) { pace.intro = false; return; }
    scene.spin.yaw = INTRO_TURN * (1 - ease(u));
    if (u >= 1) { scene.spin.yaw = 0; pace.intro = false; scene.start(); return; }
    scene.start();
    requestAnimationFrame(step);
  };
  scene.spin.yaw = INTRO_TURN;
  requestAnimationFrame(step);
}

/** The card over the scene for the focused layer: its name, its count, and the way in. */
function renderCard() {
  const card = $('home-card');
  const hint = $('home-stage-hint');
  if (!card) return;
  const key = phone() ? state.focus : null;
  hint.hidden = !phone() || Boolean(key);
  hint.textContent = exploring ? HINT_FULL : HINT_BAND;
  if (!key) {
    card.hidden = true;
    card.textContent = '';
    return;
  }
  const layer = LAYERS.find((l) => l.key === key);
  const label = layer?.label ?? key;
  const count = state.counts[key];
  card.textContent = '';
  card.dataset.tier = LAYOUT[key].tier;
  card.setAttribute('role', 'group');
  card.setAttribute('aria-label', label);

  const head = el('div', 'home-card-head');
  const dot = el('span', 'home-card-dot');
  dot.setAttribute('aria-hidden', 'true');
  const words = el('div', 'home-card-words');
  words.append(el('p', 'home-card-name', label));
  const tally = el('p', 'home-card-count');
  if (count == null) tally.textContent = UNITS[key].unit;
  else tally.append(el('b', '', String(count)), ` ${UNITS[key].unit}`);
  words.append(tally);
  const close = el('button', 'home-card-close');
  close.type = 'button';
  close.setAttribute('aria-label', 'Back to all the layers');
  close.append(icon('M6 6l12 12M18 6 6 18', 'home-card-x'));
  close.addEventListener('click', () => focus(null));
  head.append(dot, words, close);

  const open = el('a', 'home-card-open', `Open ${label}`);
  open.href = into(key);
  card.append(head, open);
  card.hidden = false;
  clearOfBar(card);
}

/**
 * A card that lands under the bottom bar (the band half scrolled away, a body
 * tapped near the foot of the screen) is brought up above it. Not full
 * screen, where the frame covers the bar.
 */
function clearOfBar(node) {
  if (exploring || !phoneBar?.tabbar) return;
  requestAnimationFrame(() => {
    const tabs = phoneBar.tabbar.getBoundingClientRect();
    if (!tabs.height) return;   // no bar at this width
    const under = node.getBoundingClientRect().bottom - (tabs.top - 12);
    if (under > 0) {
      document.body.scrollBy({ top: under, behavior: REDUCED.matches ? 'auto' : 'smooth' });
    }
  });
}

/** Reset, in the full-screen view, once the hand has moved the camera. */
function syncReset() {
  const reset = $('home-explore-reset');
  if (!reset) return;
  const show = exploring && scene.moved() && !pace.intro;
  if (reset.hidden === show) reset.hidden = !show;
}

/**
 * The scene full screen: the same canvas, every gesture, a way out.
 *
 * The stage keeps its height in the column, so the page under it does not
 * move; only the frame inside it is fixed to the screen. It is a modal dialog
 * (the page behind is inert, focus moves to Close and comes back to Explore),
 * and it is a history entry so Android's back gesture closes it.
 */
function openExplorer() {
  if (exploring || !phone()) return;
  exploring = true;
  const frame = $('home-stage-frame');
  frame.classList.add('is-full');
  frame.setAttribute('role', 'dialog');
  frame.setAttribute('aria-modal', 'true');
  frame.setAttribute('aria-label', 'The layers, full screen');
  document.body.classList.add('is-exploring');
  for (const node of document.querySelectorAll('.home-hero, .home-colophon, .phone-tabbar')) node.inert = true;
  $('home-explore').hidden = true;
  $('home-explore-close').hidden = false;
  history.pushState({ ...(history.state ?? {}), explore: true }, '', location.href);
  renderCard();
  syncReset();
  scene.start();
  $('home-explore-close').focus();
}

function closeExplorer({ fromHistory = false } = {}) {
  if (!exploring) return;
  exploring = false;
  const frame = $('home-stage-frame');
  frame.classList.remove('is-full');
  frame.removeAttribute('role');
  frame.removeAttribute('aria-modal');
  frame.removeAttribute('aria-label');
  document.body.classList.remove('is-exploring');
  for (const node of document.querySelectorAll('.home-hero, .home-colophon, .phone-tabbar')) node.inert = false;
  $('home-explore').hidden = !phone();
  $('home-explore-close').hidden = true;
  $('home-explore-reset').hidden = true;
  // Back to the entry under this one, then the address is brought up to date
  // there (see writeHash). From the browser's own Back it is already there.
  if (!fromHistory && history.state?.explore) { hashAfterPop = true; history.back(); }
  else writeHash();
  // Back in the band, where a vertical swipe scrolls the page and cannot undo
  // a tilt, the camera goes back to the band's pose. The focus is kept.
  if (scene.moved()) { scene.resetView(); land(); }
  renderCard();
  scene.start();
  $('home-explore').focus({ preventScroll: true });
}

/** Watch the band and the page, and park the scene while neither can be seen. */
function watchVisibility() {
  const wake = () => { if (pace.on && pace.seen && !document.hidden) scene.start(); };
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      pace.seen = entry.isIntersecting || exploring;
      if (!pace.seen && pace.on) scene.stop();
      wake();
    }).observe($('home-stage'));
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && pace.on) scene.stop();
    else wake();
  });
}

// ── the model ───────────────────────────────────────────────────────
/**
 * Built once. Only the counts changing rebuilds it, and they arrive once.
 *
 * A layer's mass is its headline count, so Frontend is visibly the largest
 * body and Decisions the smallest without the difference being twenty to one —
 * the compression is the engine's, and it is the same compression the graph
 * views use, so a reader who learns to read size in one place has learned it
 * everywhere.
 */
function build() {
  const hubs = ORDER.map((key) => {
    const layer = LAYERS.find((l) => l.key === key);
    const count = state.counts[key] ?? 0;
    return {
      id: key,
      name: layer?.label ?? key,
      // The count, under the name. On the body, because that is the thing it
      // is a count of.
      sub: `${count} ${UNITS[key].unit}`,
      // What is actually in there, for when somebody zooms in far enough to
      // ask. Anonymous filler makes up the rest of the cloud.
      items: state.items[key] ?? [],
      // The ring that appears when this one is focused. Built from the same
      // table the panel chips and the viewer's own tab strip are drawn from, so
      // the door cannot offer a view that has been renamed or removed.
      views: (layer?.modes ?? []).map(([id, label]) => ({ id, label })),
      ...LAYOUT[key],
      // The dot in the middle of a cluster is a marker, not a measurement —
      // the cloud around it is the measurement — so they are all one size, bar
      // Contracts. That one is marked harder because it is the thing the other
      // four resolve against, and by count alone (30 against 392) the layer the
      // whole package hangs off would be the faintest speck on the page.
      weight: key === 'contracts' ? 15 : 6,
      mass: count,
      hot: 0,
    };
  });

  const links = LINKS.map(([source, target]) => ({
    source,
    target,
    critical: source === 'contracts' || target === 'contracts',
  }));

  scene.setData({ hubs, links }, {
    spread: SPREAD, ceiling: CEILING, budget: BUDGET,
  });
}

// ── the chrome ──────────────────────────────────────────────────────
function renderRail() {
  const rail = $('home-rail');
  rail.textContent = '';

  const overview = document.createElement('button');
  overview.type = 'button';
  overview.className = 'rail-overview';
  overview.textContent = 'Overview';
  overview.classList.toggle('is-on', !state.focus);
  overview.addEventListener('click', () => { scene.resetView(); focus(null); });
  rail.append(overview);

  for (const key of ORDER) {
    const layer = LAYERS.find((l) => l.key === key);
    const row = document.createElement('button');
    row.type = 'button';
    row.className = 'rail-row';
    row.classList.toggle('is-on', state.focus === key);
    row.setAttribute('aria-pressed', String(state.focus === key));

    const name = document.createElement('span');
    name.className = 'rail-name';
    name.textContent = layer?.label ?? key;

    const count = document.createElement('span');
    count.className = 'rail-count';
    count.textContent = state.counts[key] ?? '—';

    const bar = document.createElement('span');
    bar.className = 'rail-bar';

    row.append(name, count, bar);
    row.addEventListener('click', () => focus(key));
    rail.append(row);
  }
}

/** The viewer, at a given layer and optionally a given view, in this package. */
const into = (key, mode) =>
  `/?project=${encodeURIComponent(auth.project() ?? '')}`
  + `&layer=${encodeURIComponent(key)}${mode ? `&mode=${encodeURIComponent(mode)}` : ''}`;

/**
 * The packages there are, and which one these numbers are counting.
 *
 * Choosing one is a navigation and not a state change: it reloads the door with
 * `?project=<id>`, which is the rule the viewer follows too and the reason two
 * tabs can hold two projects at once. Anchors rather than buttons for the same
 * reason — a middle click should open the other project beside this one.
 *
 * Drawn even when there is one. A picker that appears on the day the second
 * project arrives is a picker nobody knows about, and the row is also the only
 * place this page says which package the figures below it are counting.
 */
function renderProjects(list, current) {
  const box = $('home-projects');
  if (!box) return;
  box.textContent = '';
  if (!list.length) {
    const empty = document.createElement('p');
    empty.className = 'home-project-count';
    empty.textContent = 'No packages are registered — see viewer/projects.json';
    box.append(empty);
    return;
  }
  for (const project of list) {
    const row = document.createElement('a');
    row.className = 'home-project';
    row.href = `/home.html?project=${encodeURIComponent(project.id)}`;
    if (project.id === current) row.setAttribute('aria-current', 'true');

    const name = document.createElement('span');
    name.className = 'home-project-name';
    name.textContent = project.name || project.id;
    row.append(name);

    const count = document.createElement('span');
    count.className = 'home-project-count';
    // Null while that package is still building. A dash says "not yet", where a
    // zero would say "empty" — and the two are the mistake this whole viewer
    // exists to stop people making.
    count.textContent = project.artefacts == null
      ? '—'
      : `${project.artefacts} contract${project.artefacts === 1 ? '' : 's'}`;
    row.append(count);
    box.append(row);
  }
}

/** A line icon, `aria-hidden`: DESIGN-SYSTEM.md's 24px grid, drawn as Decide's are. */
function icon(d, className) {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('class', className);
  const path = document.createElementNS(ns, 'path');
  path.setAttribute('d', d);
  svg.append(path);
  return svg;
}
const chevron = () => icon('M9 5.5 15.5 12 9 18.5', 'home-chevron');

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
};

/**
 * The layers as a list, for a phone: the rail and the panel in one place.
 *
 * A row is a disclosure, not a link, because a click on the rail is one too:
 * it shows what the layer holds and offers its views, and the second step
 * (Open, or a view) is what leaves the page. Built once when the counts are
 * in; `syncLayerList` opens and closes rows so a row keeps its focus.
 */
function renderLayerList() {
  const list = $('home-layer-list');
  if (!list) return;
  list.textContent = '';
  for (const key of ORDER) {
    const layer = LAYERS.find((l) => l.key === key);
    const label = layer?.label ?? key;
    const unit = UNITS[key];
    const count = state.counts[key];

    const item = el('li', 'home-layer');
    item.dataset.layer = key;
    item.dataset.tier = LAYOUT[key].tier;

    const row = el('button', 'home-layer-row');
    row.type = 'button';
    row.setAttribute('aria-expanded', 'false');
    row.setAttribute('aria-controls', `home-layer-${key}`);
    const tally = el('span', 'home-layer-count');
    if (count == null) tally.textContent = '—';
    else tally.append(el('b', '', String(count)), ` ${unit.unit}`);
    const dot = el('span', 'home-layer-dot');
    dot.setAttribute('aria-hidden', 'true');
    row.append(dot, el('span', 'home-layer-name', label), tally, chevron());
    row.addEventListener('click', () => focus(state.focus === key ? null : key));

    const detail = el('div', 'home-layer-detail');
    detail.id = `home-layer-${key}`;
    detail.hidden = true;
    detail.append(el('p', 'home-layer-blurb', BLURB[key]));
    // The same second line as the desktop panel, less the folder list, which
    // is a note for somebody at a desk.
    const also = Object.entries(state.detail[key] ?? {})
      .filter(([, n]) => n > 0)
      .slice(0, 2)
      .map(([name, n]) => `${n} ${name}`);
    if (also.length) detail.append(el('p', 'home-layer-meta', also.join('  ·  ')));

    const open = el('a', 'home-layer-open', `Open ${label}`);
    open.href = into(key);
    detail.append(open);

    const modes = layer?.modes ?? [];
    if (modes.length) {
      const title = el('p', 'home-layer-views-title', 'Or go straight to a view');
      title.id = `home-layer-${key}-views`;
      const views = el('div', 'home-layer-views');
      views.setAttribute('role', 'group');
      views.setAttribute('aria-labelledby', title.id);
      for (const [mode, name] of modes) {
        const chip = el('a', '', name);
        chip.href = into(key, mode);
        views.append(chip);
      }
      detail.append(title, views);
    }

    item.append(row, detail);
    list.append(item);
  }
  syncLayerList();
}

function syncLayerList() {
  for (const item of $('home-layer-list')?.children ?? []) {
    const on = item.dataset.layer === state.focus;
    item.classList.toggle('is-open', on);
    item.querySelector('.home-layer-row')?.setAttribute('aria-expanded', String(on));
    const detail = item.querySelector('.home-layer-detail');
    if (detail) detail.hidden = !on;
  }
}

/**
 * The rest of ADAM, for a phone. The desktop door is reached from every
 * page's top bar and leaves through the viewer; a phone that lands here (the
 * app opens on it) needs the way on written down. The pages people open daily,
 * as the account drawer groups them, and Decide for the two roles that decide.
 */
const PAGES = [
  { href: '/decide', label: 'Decide', who: (a) => a?.role === 'owner' || a?.role === 'lead',
    // A tick in a ring: a decision made.
    icon: 'M12 20.5a8.5 8.5 0 1 0 0-17 8.5 8.5 0 0 0 0 17ZM8.3 12.3l2.6 2.6 4.8-5.2' },
  { href: '/board.html', label: 'My work',
    icon: 'M12 11.5a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5ZM5 20a7 7 0 0 1 14 0' },
  { href: '/tasks.html', label: 'Tasks',
    icon: 'M11 6.5h9M11 12h9M11 17.5h9M4 6.5l1.4 1.4L8 5.2M4 12l1.4 1.4L8 10.7M4 17.5l1.4 1.4L8 16.2' },
  { href: '/changes.html', label: 'Change requests',
    // Two arrows passing: something asked to move one way, and the answer back.
    icon: 'M7.5 4v15M4 15.5 7.5 19l3.5-3.5M16.5 20V5M13 8.5 16.5 5 20 8.5' },
  { href: '/reviews.html', label: 'Reviews',
    icon: 'M2.5 12s3.5-6.5 9.5-6.5 9.5 6.5 9.5 6.5-3.5 6.5-9.5 6.5S2.5 12 2.5 12ZM12 14.75a2.75 2.75 0 1 0 0-5.5 2.75 2.75 0 0 0 0 5.5Z' },
  { href: '/chat.html', label: 'Ask about the package',
    icon: 'M4.5 5.5h15v10h-9l-6 4.5v-14.5Z' },
  { href: '/updates.html', label: 'What is new in ADAM',
    icon: 'M12 3.5l2 5.5 5.5 2-5.5 2-2 5.5-2-5.5-5.5-2 5.5-2 2-5.5Z' },
  { href: '/settings.html', label: 'Settings',
    // Sliders: settings as things set, not a cog.
    icon: 'M4 7h9M17 7h3M15 5v4M4 17h3M11 17h9M9 15v4' },
];

function renderPages() {
  const list = $('home-pages-list');
  if (!list) return;
  list.textContent = '';
  const who = auth.account();
  for (const page of PAGES) {
    if (page.who && !page.who(who)) continue;
    const item = el('li');
    const link = el('a');
    link.href = page.href;
    link.append(icon(page.icon, 'home-page-icon'), el('span', 'home-page-name', page.label), chevron());
    item.append(link);
    list.append(item);
  }
}

function renderPanel() {
  const panel = $('home-panel');
  const key = state.focus;
  // A phone has the list instead. Kept hidden there too, because an open
  // panel is what the narrow-window rule reads to fold the colophon away.
  if (!key || phone()) {
    panel.hidden = true;
    panel.textContent = '';
    return;
  }

  const layer = LAYERS.find((l) => l.key === key);
  const count = state.counts[key] ?? 0;
  const unit = UNITS[key];
  const extra = state.detail[key] ?? {};

  panel.textContent = '';
  panel.hidden = false;
  panel.style.setProperty('--tint', LAYOUT[key].tier === 'core' ? '#e0ae52' : '#00c4e8');

  const head = document.createElement('div');
  head.className = 'panel-head';
  const dot = document.createElement('span');
  dot.className = 'panel-dot';
  const title = document.createElement('h2');
  title.textContent = layer?.label ?? key;
  head.append(dot, title);

  const meta = document.createElement('p');
  meta.className = 'panel-meta';
  // What else is in there, after the headline number. Two figures, because a
  // third turns a line into a table and the table is what the viewer is for.
  const also = Object.entries(extra)
    .filter(([, n]) => n > 0)
    .slice(0, 2)
    .map(([name, n]) => `${n} ${name}`);
  meta.textContent = [`${count} ${unit.unit}`, ...also, unit.from].join('  ·  ');

  const blurb = document.createElement('p');
  blurb.className = 'panel-blurb';
  blurb.textContent = BLURB[key];

  // The views this layer offers, named exactly as the viewer names them —
  // they come from the same table the tab strip is drawn from, so the door
  // cannot promise a view that has been renamed or removed.
  const chips = document.createElement('div');
  chips.className = 'panel-chips';
  for (const [mode, label] of layer?.modes ?? []) {
    const chip = document.createElement('a');
    chip.href = into(key, mode);
    chip.textContent = label;
    chips.append(chip);
  }

  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const go = document.createElement('a');
  go.className = 'panel-go';
  go.href = into(key);
  go.textContent = `Open ${layer?.label ?? key}`;
  const back = document.createElement('button');
  back.type = 'button';
  back.className = 'panel-back';
  back.textContent = 'Back out';
  back.addEventListener('click', () => focus(null));
  actions.append(go, back);

  panel.append(head, meta, blurb, chips, actions);
}

// ── navigation ──────────────────────────────────────────────────────
/**
 * Focus a layer, or back out.
 *
 * Going in is two steps on purpose: the first shows what the layer holds, the
 * second opens it. A single click straight through makes the body a menu item
 * and throws away the reason the page exists.
 */
function focus(key, { open = false } = {}) {
  if (open && key && state.focus === key) {
    leave(into(key));
    return;
  }
  state.focus = key ?? null;
  // The same on a phone: the scene flies to the body (or jumps, under reduced
  // motion), and the canvas slides so it lands mid-band.
  scene.setFocus(state.focus);
  if (phone()) { land(); placeCanvas(); }
  // Linkable in the state a reader was sent to — and back/forward through the
  // layers works, which is what a reader expects of something they scrolled.
  // `location.pathname` alone drops the query, and the query is where the
  // project is -- so clearing a focus quietly un-named the package the page was
  // reading, and the next thing to look at the address found none.
  writeHash();
  renderRail();
  renderPanel();
  syncLayerList();
  renderCard();
  sayHint();
  syncBack();
}

/**
 * The address says which layer is open. Not while the full-screen view is
 * open: that view is a history entry of its own (so Back closes it), and
 * changing its address would make the Back that closes it also a change of
 * hash, which reopens whatever layer was open before. The address is written
 * once, on the way out, instead.
 */
function writeHash() {
  if (exploring) return;
  history.replaceState(
    history.state, '',
    state.focus ? `#layer=${state.focus}` : `${location.pathname}${location.search}`);
}

/**
 * Put the scene in the state the layout asks for: the band, paced, on a phone;
 * the full-window field everywhere else. Run on start and whenever the query
 * flips (a window narrowed past 600px, a tablet's keyboard detached).
 */
function applyLayout() {
  const canvas = $('home-scene');
  scene.showLabels = true;
  if (phone()) {
    canvas.setAttribute('aria-label', PHONE_SCENE_LABEL);
    pace.on = true;
    setCounts(false);
    $('home-explore').hidden = exploring;
    // Fitted at the overview, then put back on whatever the reader had open.
    const had = state.focus;
    if (scene.focusId) scene.setFocus(null);
    fitPhone();
    scene.setFocus(had);
    land();
    placeCanvas();
    scene.start();
    intro();
  } else {
    if (exploring) closeExplorer();
    pace.on = false;
    pace.intro = false;
    setCounts(true);
    canvas.setAttribute('aria-label', deskLabel);
    $('home-explore').hidden = true;
    canvas.style.transform = '';
    scene.baseZoom = scene.zoom = ZOOM;
    scene.spin = { yaw: 0, pitch: 0 };
    scene.setFocus(state.focus);
    scene.start();
  }
  renderPanel();
  renderCard();
  syncBack();
}

/**
 * Back out of whatever the reader is in, in order: the zoom first, then the
 * focus. Two presses to get all the way out, which is right — one press should
 * not undo two separate things.
 */
function backOut() {
  if (scene.moved()) { scene.resetView(); land(); sayHint(); syncBack(); syncReset(); return; }
  focus(null);
}

/** The way out, shown only once there is something to come back from. */
function syncBack() {
  const button = $('home-back');
  if (!button) return;
  button.hidden = !state.focus && !scene?.moved();
}

/** The line whose job is to say what to do next, not what the page is. */
function sayHint() {
  $('home-hint').textContent = scene?.zoom >= 1.7 ? HINTS.zoomed
    : state.focus ? HINTS.focused
    : HINTS.overview;
}

/** One layer along, wrapping off the front of the list into the overview. */
function step(delta) {
  const at = state.focus ? ORDER.indexOf(state.focus) : -1;
  const next = at + delta;
  if (next < 0 || next >= ORDER.length) focus(null);
  else focus(ORDER[next]);
}

function bind() {
  // The wheel belongs to the scene now — galaxy.js binds it to zoom. This one
  // only stops the page itself scrolling anywhere the canvas does not reach.
  // A phone layout scrolls like a page, so there it is left alone.
  window.addEventListener('wheel', (e) => { if (!phone()) e.preventDefault(); }, { passive: false });

  $('home-back').addEventListener('click', backOut);

  window.addEventListener('keydown', (e) => {
    // Not while somebody is tabbing through the rail and pressing space on a
    // button — that is the button's key, not ours.
    if (e.target instanceof HTMLElement && e.target.tagName === 'BUTTON' && e.key === 'Enter') return;
    if (e.key === 'Escape') {
      // The account drawer (opened from More) closes itself on Escape.
      if (document.getElementById('account-panel')?.hidden === false) return;
      // The full-screen view is a dialog, and Escape closes a dialog.
      if (exploring) { closeExplorer(); return; }
      // On a phone, Escape closes the open row and hands focus back to it.
      const open = phone() && state.focus;
      backOut();
      if (open) document.querySelector(`.home-layer[data-layer="${open}"] .home-layer-row`)?.focus();
      return;
    }
    // The arrows and Enter step the scene on a desktop. A phone layout is a
    // page, whose arrows scroll it and whose Enter belongs to the link it is on.
    if (phone()) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); step(1); return; }
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); step(-1); return; }
    if (e.key === 'Enter' && state.focus) { leave(into(state.focus)); }
  });


  // Clicking nothing backs out. On the canvas only, so a click on the panel or
  // the rail is not also a click on the void behind them.
  // A tap has already been answered by galaxy.js's touch handlers; the click
  // the browser sends after it is not read again here.
  $('home-scene').addEventListener('click', (e) => {
    if (scene.recentTouch()) return;
    const box = e.currentTarget.getBoundingClientRect();
    if (!scene.hubAt(e.clientX - box.left, e.clientY - box.top)) focus(null);
  });

  // In the band a wheel scrolls the page, as a swipe does; the scene zooms by
  // pinch there, and by wheel only full screen. Caught on the way down, before
  // galaxy.js's own wheel handler on the canvas sees it.
  $('home-stage').addEventListener('wheel', (e) => {
    if (phone() && !exploring) e.stopPropagation();
  }, { capture: true });

  $('home-explore').addEventListener('click', openExplorer);
  $('home-explore-close').addEventListener('click', () => closeExplorer());
  $('home-explore-reset').addEventListener('click', () => {
    scene.resetView();
    land();
    syncReset();
    $('home-explore-close').focus();
  });
  // A link in the full-screen view (the card's "Open …") leaves the same way.
  $('home-stage-frame').addEventListener('click', (e) => {
    const link = e.target.closest?.('a[href]');
    if (!exploring || !link || e.defaultPrevented || e.button !== 0
      || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || link.target) return;
    e.preventDefault();
    leave(link.href);
  });
  window.addEventListener('popstate', () => {
    if (exploring && !history.state?.explore) { closeExplorer({ fromHistory: true }); return; }
    if (hashAfterPop) { hashAfterPop = false; writeHash(); }
  });

  // A phone's band is re-fitted when it changes size (a rotation), unless the
  // reader has the camera somewhere of their own.
  window.addEventListener('resize', () => {
    if (!phone()) { scene.draw(); return; }
    if (!scene.moved() && !pace.intro) fitPhone();
    placeCanvas();
    scene.start();
  });
  PHONE.addEventListener('change', applyLayout);
}

async function renderAccount() {
  const line = $('home-account');
  const who = auth.account();
  if (!who) return;
  line.hidden = false;
  // In spans so a phone can set the name apart and drop the separator; on a
  // desktop it reads exactly as it did, "Signed in as … · Sign out".
  line.textContent = '';
  const said = el('span', 'home-account-who', 'Signed in as ');
  said.append(el('span', '', who.name || who.email));
  line.append(said, el('span', 'home-account-sep', ' · '));
  const out = document.createElement('button');
  out.type = 'button';
  out.textContent = 'Sign out';
  out.addEventListener('click', async () => {
    out.disabled = true;
    await auth.signOut().catch(() => {});
    location.href = '/login.html';
  });
  line.append(out);
}

// ── start ───────────────────────────────────────────────────────────
async function main() {
  if (!(await auth.requireSignIn())) { hideLoader(); return; }

  // The bottom bar every page has on a phone, Home lit as this page. Shown by
  // CSS under 720 px only, and on this page only with its phone column (home.css).
  phoneBar = mountPhoneBar({
    current: 'home',
    drawer: true,
    // The scene holds still between touches, so it is told to paint the new
    // palette rather than waiting for the next thing to move it.
    setTheme: (theme) => { setTheme(theme); scene?.start(); },
  });

  // Which packages there are, before what is in one of them. The listing sits
  // outside the project prefix precisely because it is what a reader needs
  // before they can name a project.
  loaderSays('Finding the packages…');
  const registry = await auth.listProjects().catch(() => null);
  const projects = registry?.projects ?? [];
  // The address, then what the reader chose last, then whatever the server
  // calls default. A door with no project named still has to open on one.
  const current = auth.project()
    ?? (projects.some((p) => p.id === registry?.default) ? registry.default : projects[0]?.id)
    ?? null;
  if (current) auth.rememberProject(current);
  renderProjects(projects, current);

  // The lockup stays on the door.
  //
  // It shipped as a bare `href="/"`, and `/` is `index.html`, which sends a
  // reader back here on the **first** load of a session — it gates that on a
  // `ticvai-session` flag it sets itself, and the door never sets it. So the
  // first click went `/home.html?project=ticvai` -> `/` -> `/home.html`,
  // landing back on the door **with the project dropped from the address**,
  // and every click after that fell through into whichever package was last
  // opened. One link, two behaviours, and neither is what a brand mark should
  // do: **the logo on a landing page is not a way into a package.** Choosing a
  // package is what the rail and the project row are for, and they say which
  // one; the lockup says nothing, so it must not pick.
  //
  // Pointed at the door itself, carrying the project so the address still names
  // what the figures below are counting. Still an anchor with a real href, so
  // middle-click and open-in-new-tab keep working.
  //
  // 15 September: the lockup goes to the landing page now, as it does from every
  // other page. It still picks no package — the landing page names none.
  const lockup = document.querySelector('.home-lockup');
  if (lockup) {
    lockup.href = '/landing.html';
    lockup.setAttribute('aria-label', 'Adam — about Adam');
  }

  // A first visit names no project, and every package read below hangs off one.
  // The address is made to say which -- once, on a cold visit -- so that what a
  // reader copies out of the bar is a link to a package rather than to whatever
  // the next person happened to open last.
  if (current && !auth.project()) {
    location.replace(`/home.html?project=${encodeURIComponent(current)}`);
    return;
  }
  if (!current) {
    loaderSays('No packages are registered.');
    hideLoader();
    return;
  }

  loaderSays('Counting what is in the package…');
  const summary = await auth.apiFetch('/api/summary')
    .then((r) => r.json())
    .catch(() => null);

  // A door that cannot count is still a door. Every layer is reachable from
  // the rail and the panel with or without its number, so a summary that did
  // not arrive costs the figures and nothing else.
  state.counts = summary?.counts ?? {};
  state.detail = summary?.detail ?? {};
  state.items = summary?.items ?? {};
  $('fig-artefacts').textContent = summary?.artefacts ?? '—';
  $('fig-operations').textContent = summary?.operations ?? '—';

  scene = new Galaxy($('home-scene'), {
    camera: true,
    hoops: true,
    moteGain: MOTE_GAIN,
    zoom: ZOOM,
    onSelect: (hub, { open }) => focus(hub.id, { open: open || state.focus === hub.id }),
    // A tap on nothing backs out one step on a phone, as Back does: the focus
    // first, then the reader's own turn and zoom (the band has no Reset).
    onEmpty: () => (phone() && !state.focus && scene.moved() ? backOut() : focus(null)),
    onZoom: () => { sayHint(); syncBack(); },
    // Straight through, unlike a click on a body: choosing a named view is
    // already the second decision, and asking for a third would be a menu.
    onView: (hub, view) => { leave(into(hub.id, view.id)); },
  });
  // Same convention as the viewer's `window.__galaxy`: the scene is reachable
  // from the console, which is how a layout gets debugged without a rebuild.
  window.__home = scene;
  deskLabel = $('home-scene').getAttribute('aria-label') ?? '';
  pacer();
  build();
  bind();
  watchVisibility();
  renderRail();
  renderLayerList();
  renderPages();
  renderAccount();
  applyLayout();

  // Opened focused when the link said so, so the page is linkable in the state
  // a reader was sent to — on arrival, and again if the hash changes under it,
  // which is what a link to `#layer=…` on this same page does.
  const fromHash = () => {
    const wanted = new URLSearchParams(location.hash.slice(1)).get('layer');
    focus(ORDER.includes(wanted) ? wanted : null);
    // A link to `#layer=…` on a phone opens that row; bring it into view.
    // Not while full screen, where the card over the scene is that row.
    if (phone() && state.focus && !exploring) {
      document.querySelector(`.home-layer[data-layer="${state.focus}"]`)
        ?.scrollIntoView({ block: 'nearest' });
    }
  };
  window.addEventListener('hashchange', fromHash);
  fromHash();

  hideLoader();
}

main();
