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
};

/** What the headline number counts, and where on disk it comes from. */
const UNITS = {
  frontend:  { unit: 'screens',      from: 'screens/ · flows/ · frontend/ · wireframes/' },
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
];

const ORDER = ['frontend', 'contracts', 'domain', 'backend', 'services', 'decisions'];

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

function renderPanel() {
  const panel = $('home-panel');
  const key = state.focus;
  if (!key) {
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
  panel.style.setProperty('--tint', LAYOUT[key].tier === 'core' ? '#e0ae52' : '#48cfcb');

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
    location.href = into(key);
    return;
  }
  state.focus = key ?? null;
  scene.setFocus(state.focus);
  // Linkable in the state a reader was sent to — and back/forward through the
  // layers works, which is what a reader expects of something they scrolled.
  // `location.pathname` alone drops the query, and the query is where the
  // project is -- so clearing a focus quietly un-named the package the page was
  // reading, and the next thing to look at the address found none.
  history.replaceState(
    null, '',
    state.focus ? `#layer=${state.focus}` : `${location.pathname}${location.search}`);
  renderRail();
  renderPanel();
  sayHint();
  syncBack();
}

/**
 * Back out of whatever the reader is in, in order: the zoom first, then the
 * focus. Two presses to get all the way out, which is right — one press should
 * not undo two separate things.
 */
function backOut() {
  if (scene.moved()) { scene.resetView(); sayHint(); syncBack(); return; }
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
  window.addEventListener('wheel', (e) => e.preventDefault(), { passive: false });

  $('home-back').addEventListener('click', backOut);

  window.addEventListener('keydown', (e) => {
    // Not while somebody is tabbing through the rail and pressing space on a
    // button — that is the button's key, not ours.
    if (e.target instanceof HTMLElement && e.target.tagName === 'BUTTON' && e.key === 'Enter') return;
    if (e.key === 'Escape') { backOut(); return; }
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); step(1); return; }
    if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); step(-1); return; }
    if (e.key === 'Enter' && state.focus) { location.href = into(state.focus); }
  });


  // Clicking nothing backs out. On the canvas only, so a click on the panel or
  // the rail is not also a click on the void behind them.
  $('home-scene').addEventListener('click', (e) => {
    const box = e.currentTarget.getBoundingClientRect();
    if (!scene.hubAt(e.clientX - box.left, e.clientY - box.top)) focus(null);
  });

  window.addEventListener('resize', () => scene.draw());
}

async function renderAccount() {
  const line = $('home-account');
  const who = auth.account();
  if (!who) return;
  line.hidden = false;
  line.textContent = `Signed in as ${who.name || who.email} · `;
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
    onSelect: (hub, { open }) => focus(hub.id, { open: open || state.focus === hub.id }),
    onEmpty: () => focus(null),
    onZoom: () => { sayHint(); syncBack(); },
    // Straight through, unlike a click on a body: choosing a named view is
    // already the second decision, and asking for a third would be a menu.
    onView: (hub, view) => { location.href = into(hub.id, view.id); },
  });
  // Same convention as the viewer's `window.__galaxy`: the scene is reachable
  // from the console, which is how a layout gets debugged without a rebuild.
  window.__home = scene;
  build();
  bind();
  renderRail();
  renderAccount();

  // Opened focused when the link said so, so the page is linkable in the state
  // a reader was sent to — on arrival, and again if the hash changes under it,
  // which is what a link to `#layer=…` on this same page does.
  const fromHash = () => {
    const wanted = new URLSearchParams(location.hash.slice(1)).get('layer');
    focus(ORDER.includes(wanted) ? wanted : null);
  };
  window.addEventListener('hashchange', fromHash);
  fromHash();

  hideLoader();
}

main();
