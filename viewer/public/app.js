import { Graph, colorForNode } from './graph.js';
import { StructureTree, kindColor } from './structure.js';
import { BoxDiagram } from './boxdiagram.js';
import { StateMachine } from './statemachine.js';
import { installTips, tip, tipFor } from './tips.js';
import * as auth from './validation.js';
import {
  renderDecisions, openDoc, renderTimeline, renderSupersession, renderRegister,
  renderDecision, openDecision,
} from './layer-decisions.js';

// The shared vocabulary — layers, modes, state, the DOM helpers and the tip
// wiring. All of it used to be declared here; it moved to core.js so the layer
// modules could import it without importing the router.
import {
  LAYERS, MODE_TIPS, layerOf, VIEWS, state, groupBy, setDrawer, syncLinksToggle,
  $, el, TYPE_LABEL, escapeHtml, vocabularyTip, deliveryTip, permissionTip,
  inlineMarkdown, renderBoxLegend,
} from './core.js';
// ── boot ─────────────────────────────────────────────────────────────
let graph;
let tree;
let er;
let data;
let machine;

async function boot() {
  machine = new StateMachine($('states-canvas'), {
    onSelect: (node) => {
      state.stateName = node.name;
      renderStateLinks();
    },
    onEdge: (edge) => {
      const m = currentMachine();
      $('states-hint').textContent = edge
        ? describeTransition(edge)
        : m ? describeMachine(m) : '';
    },
  });

  const openRow = (row) => {
    if (row.refTarget && state.nodesById.has(row.refTarget)) select(row.refTarget);
  };
  er = new BoxDiagram($('er-canvas'), {
    onSelect: (node) => select(node.id),
    onRow: openRow,
  });

  // the same box renderer, drawing database tables — or, zoomed out, schemas
  data = new BoxDiagram($('data-canvas'), {
    onSelect: (node) => {
      if (node.id.startsWith('schema:')) openSchema(node.id.slice(7));
      else selectTable(node.id.replace(/^table:/, ''));
    },
    onRow: (row) => {
      if (!row.refTarget) return;
      if (state.dataModule === ALL_SCHEMAS) openSchema(row.refTarget);
      else selectTable(row.refTarget);
    },
  });

  tree = new StructureTree($('struct-canvas'), {
    onSelect: (node) => {
      $('struct-hint').textContent = describeTreeNode(node);
    },
    onRef: (node) => {
      const id = refToNodeId(node.value, state.structureFile);
      if (id && state.nodesById.has(id)) select(id, { fromStructure: false });
      else toast('That $ref does not resolve to a known component');
    },
  });

  graph = new Graph($('graph-canvas'), {
    onSelect: (node, opts) => {
      select(node.id);
      if (opts?.open) setMode('reader');
    },
    onHover: showTooltip,
  });

  // frame the graph once the force layout converges, unless the user has
  // already panned or zoomed — then the view is theirs, not ours
  graph.onSettle = () => {
    if (state.mode !== 'graph' || graph.userAdjusted) return;
    graph.resize();
    graph.recenter();
    graph.hasFramed = true;
  };

  // Selecting pushes a hash entry, so back/forward and pasted deep links both
  // arrive here rather than as a reload.
  window.addEventListener('hashchange', () => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    if (id !== state.selectedId && state.nodesById.has(id)) select(id);
    // a screen, table or board link followed while the app is already open
    else if (!state.nodesById.has(id)) openArtefactHash(id);
  });

  // handy for debugging layouts from the console
  window.__graph = graph;
  window.__tree = tree;
  window.__er = er;
  window.__data = data;
  window.__machine = machine;
  window.__state = state;

  // The viewer is behind a sign-in. Ask before fetching two megabytes that a
  // stranger is not going to be shown, and send them where they can do
  // something about it — carrying where they were headed, so a link into a
  // particular node still lands there afterwards.
  const signedIn = await auth.requireSignIn();
  if (!signedIn) return;

  await loadIndex();
  renderLayers();
  bindUI();
  connectLiveReload();
  bindSections();
  bindAccountUI();
  // delegated, so everything rendered from here on carries its tips without
  // being wired up individually
  installTips();

  // the scrolling panes pan like the canvases do
  for (const id of [
    'journey-body', 'screen-body', 'apps-body', 'routing-body', 'migrations-body',
    'lineage-body', 'waves-body', 'decisions-body',
  ]) {
    enableDragScroll($(id));
  }

  // restore from the url so links into a specific node survive a refresh
  const fromHash = decodeURIComponent(location.hash.slice(1));
  if (fromHash && state.nodesById.has(fromHash)) {
    select(fromHash);
    setMode(state.mode === 'graph' ? 'reader' : state.mode);
  } else if (fromHash && (await openArtefactHash(fromHash))) {
    // handled — a screen, table or board rather than a contract node
  } else {
    setMode('graph');
  }

  // The layer the app opens on never went through setLayer, so nothing has
  // asked for its parts yet.
  hydrateLayer();
}

/**
 * A deep link to one of the three artefacts that are not contract nodes.
 *
 * An operation is a node in the index and has always been linkable by its id.
 * A screen, a table and a design board are not — they live in state the hash
 * never carried, so the only way to reach one was to click through to it. That
 * was tolerable while nothing outside the app needed to point at them, and
 * stopped being so the moment the validation overview wanted to say "this
 * table is the one still unreviewed" and link to it.
 *
 *   #screen:WEB-001   #table:fnb.fnb_order   #board:P01
 *
 * The prefixes are the ones the app already uses for the same three things in
 * currentSideId(), and none can collide with a node id — those are `op:`,
 * `schema:`, `file:`, `perm:` and the rest, all of which are tried first.
 *
 * Returns false for anything it does not recognise, so the caller can fall
 * back rather than land on a blank view.
 */
async function openArtefactHash(hash) {
  const split = hash.indexOf(':');
  if (split < 0) return false;
  const kind = hash.slice(0, split);
  const id = hash.slice(split + 1);
  if (!id) return false;

  // The layer's own parts have to be in hand before anything can be said about
  // whether the artefact exists, so this waits rather than guessing.
  if (kind === 'screen' || kind === 'board') {
    await ensureParts(LAYER_PARTS.frontend, 'frontend');
    setLayer('frontend');
    if (kind === 'board') {
      if (!boards().some((b) => b.id === id)) return false;
      selectBoard(id);
    } else {
      if (!state.journeys?.screens?.some((s) => s.id === id)) return false;
      state.boardId = null;
      state.screenId = id;
      setMode('screen');
    }
    return true;
  }

  if (kind === 'table') {
    await ensureParts(LAYER_PARTS.backend, 'backend');
    if (!state.backend?.tables?.some((t) => t.name === id)) return false;
    setLayer('backend');
    selectTable(id);
    setMode('data');
    return true;
  }

  return false;
}

// ── layer switching ──────────────────────────────────────────────────
/**
 * Below 1100px the two topbar rails scroll instead of wrapping, so the button
 * that just became active can be off screen. Scroll it back — a segmented
 * control that does not show its own selection is worse than a wrapped one.
 */
function revealActive(rail) {
  const active = rail.querySelector('.active');
  if (!active || rail.scrollWidth <= rail.clientWidth) return;
  active.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' });
}

/**
 * The layers this account may open, in tab order.
 *
 * The list comes from the server, not from a decision made here. A client's
 * payload does not contain the Backend or Decisions branch at all, so drawing
 * the tab would offer a door onto an empty room — and deciding it here would
 * mean two places could disagree about what the account is allowed.
 */
function visibleLayers() {
  const allowed = state.session?.layers;
  if (!allowed) return LAYERS;
  const set = new Set(allowed);
  return LAYERS.filter((l) => set.has(l.key));
}

/** Modes within a layer. A client gets every mode of every layer they can
 *  open — the narrowing is by layer, not within one. */
function visibleModes(layer) {
  const only = state.session?.modes?.[layer.key];
  if (!only) return layer.modes;
  const set = new Set(only);
  return layer.modes.filter(([key]) => set.has(key));
}

function renderLayers() {
  const bar = $('layers');
  bar.innerHTML = '';
  document.body.dataset.layer = state.layer;
  for (const layer of visibleLayers()) {
    const button = el('button', null, layer.label);
    button.dataset.layer = layer.key;
    button.title = layer.hint;
    tip(button, layer.label, layer.tip ?? layer.hint);
    button.classList.toggle('active', layer.key === state.layer);
    button.onclick = () => setLayer(layer.key);
    bar.append(button);
  }
  renderModes();
}

function renderModes() {
  const bar = $('modes');
  bar.innerHTML = '';
  for (const [key, label] of visibleModes(layerOf(state.layer))) {
    const button = el('button', 'mode', label);
    button.dataset.mode = key;
    button.classList.toggle('active', key === state.mode);
    const about = MODE_TIPS[key];
    if (about) tip(button, about.title, about.body);
    if (key === 'audit') {
      const badge = el('span', 'audit-count');
      badge.id = 'audit-count';
      button.append(' ', badge);
    }
    button.onclick = () => setMode(key);
    bar.append(button);
  }
  updateAuditBadge();
}

function setLayer(key) {
  if (state.layer === key) return;
  state.layer = key;
  const layer = layerOf(key);

  for (const button of $('layers').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.layer === key);
  }
  revealActive($('layers'));
  document.body.dataset.layer = key;

  // stay on the current view if this layer also has it, else open its first
  const modes = layer.modes.map(([m]) => m);
  const next = modes.includes(state.mode) ? state.mode : modes[0];
  renderModes();
  renderSideGroups();
  renderTree();
  renderSideNote();
  renderSidePane();
  renderAudit();
  setMode(next);

  // Draw with what is here, then draw again with what arrives. On a layer
  // whose parts are already in hand this does nothing at all.
  hydrateLayer(key);
}

/**
 * What each layer opens on. These used to be picked at boot, when every part
 * was already in hand; a part now arrives later, so they are picked when it
 * does — and only if the reader has not already chosen for themselves.
 */
function applyPartDefaults() {
  // the whole database, so the first thing seen is the shape of it
  if (!state.dataModule && state.backend?.modules?.length) state.dataModule = ALL_SCHEMAS;
  if (!state.screenId) state.screenId = state.journeys?.screens?.[0]?.id ?? null;
  // the order machine first: fourteen transitions, four reversals and every
  // approval rule in the platform, so it shows what the view is for
  if (!state.machineId) {
    state.machineId =
      state.domain?.machines?.find((m) => m.id === 'order')?.id ??
      state.domain?.machines?.[0]?.id ?? null;
  }
}

/**
 * Fetches whatever the layer still needs, then rebuilds what was built from
 * it. The pickers and the laid-out diagrams are the subtle part: they used to
 * be filled once at boot, when every part was already in hand. A picker built
 * from a part that had not arrived holds nothing, and nothing would ever fill
 * it again — so each part refreshes exactly what is made from it.
 */
function hydrateLayer(key = state.layer) {
  return ensureParts(LAYER_PARTS[key] ?? [], key).then((arrived) => {
    if (!arrived.length) return;
    partsArrived(arrived);
    // setMode only resizes an already-drawn canvas, so the graph would keep
    // whatever it drew before the part landed — for the spine, no edges at all.
    renderGraph();

    renderSideGroups();
    renderTree();
    renderSideNote();
    renderSidePane();
    renderAudit();
    setMode(state.mode);
  }).then(() => hydrateExtras(key));
}

/**
 * The parts this layer's panes read but its views do not need to draw. Fetched
 * behind the layer rather than in front of it, so switching stays immediate,
 * and repainted when they arrive.
 */
function hydrateExtras(key = state.layer) {
  return ensureParts(LAYER_EXTRAS[key] ?? [], key).then((arrived) => {
    if (!arrived.length) return;
    // The same work a required part gets. A part fetched as an extra here is
    // the very same part another layer would call required, and it arrives
    // exactly once — so if the pickers and diagrams built from it are not set
    // up now, nothing will ever do it. That is not hypothetical: contracts
    // pulls in `backend` for its links pane, which meant that by the time the
    // reader reached the Backend layer the part was already in hand, `arrived`
    // was empty there, and the data view drew with no schema scope at all.
    partsArrived(arrived);
    renderSidePane();
    setMode(state.mode);
  });
}

/** Everything that has to happen once, whenever a part first lands. */
function partsArrived(arrived) {
  applyPartDefaults();
  if (arrived.includes('backend')) renderData();
  if (arrived.includes('domain')) {
    fillMachineSelect();
    fillEventSelect();
  }
  // The trail from a contract into the database is drawn from two parts that
  // are both extras on the Contracts layer, so the reader is on screen before
  // either lands. Redrawing just that block is cheaper than the whole reader,
  // which would re-fetch and re-highlight the source for no reason.
  if (arrived.includes('backend') || arrived.includes('lineage')) {
    const node = state.selectedId ? state.nodesById.get(state.selectedId) : null;
    if (node && !$('reader-body').hidden) renderTrace(node);
  }
}

// ── loading the delivery, a layer at a time ─────────────────────────
// Fetching all seven payloads up front cost 4.8 MB and four seconds before
// anything could be read, and six of the seven were for layers the reader had
// not opened. Each part is fetched when a layer that needs it is opened, and
// the view re-renders when it lands. Every render path already tolerates a
// missing part — they were all fetched with .catch(() => null) — so "not here
// yet" is a state the app was already built to survive.

/** Which parts a layer cannot be drawn without. */
/**
 * Which domain lenses claim an artefact, and a mark to put on its tree row.
 *
 * This is the "within" half of the lens. The artefact stays exactly where its
 * kind puts it — `ai.yaml` in Contracts, `conversation.yaml` in Domain under
 * marketing-crm, which is where it correctly belongs — and wears a dot saying
 * it is also part of something. The Domains page is the other half, gathering
 * the same set on one screen. One definition, two surfaces; neither replaces
 * the artefact-kind organisation, which is the thing the package is careful
 * about and the thing an "AI" tab would quietly undo.
 */
function lensesFor(kind, id) {
  if (!id) return [];
  const direct = state.lensOf?.get(`${kind}:${id}`);
  if (direct?.length) return direct;
  // a contract file, marked by what its operations belong to
  if (kind === 'file') return [...(state.lensByFile?.get(id) ?? [])];
  return [];
}

/** The dot itself, or nothing — a row in no lens gets no markup at all. */
function lensMark(kind, id) {
  const keys = lensesFor(kind, id);
  if (!keys.length) return null;
  const mark = el('span', 'lens-mark');
  mark.dataset.lens = keys.join(' ');
  for (const key of keys) {
    const dot = el('span', `lens-dot lens-${key}`);
    dot.textContent = (state.lensById?.get(key)?.label ?? key).slice(0, 2).toUpperCase();
    mark.append(dot);
  }
  mark.title = keys
    .map((k) => `Also in the ${state.lensById?.get(k)?.label ?? k} lens`)
    .join('\n');
  return mark;
}

/** Attach the mark if there is one. Returns the row, so it can be chained. */
function markLens(row, kind, id) {
  const mark = lensMark(kind, id);
  if (mark) {
    row.append(mark);
    row.dataset.lens = mark.dataset.lens;
  }
  return row;
}

const LAYER_PARTS = {
  frontend: ['journeys', 'lineage'],
  // the spine graph draws one edge per pair of contracts that share an event,
  // and the events are in the domain part — so contracts needs it too
  contracts: ['lineage', 'domain'],
  backend: ['backend', 'lineage'],
  domain: ['domain'],
  decisions: ['decisions'],
};
/**
 * Parts a layer does not need to draw itself, but which its panes read.
 *
 * This distinction is the one the first version of the lazy loading missed,
 * and it went wrong quietly rather than loudly. The Lineage view drew
 * perfectly well without the backend part — and then marked all 671 of its
 * table chips "not in the schema reference" and refused to open any of them,
 * because the list it checks them against was not there. Only 13 are really
 * unknown. A pane that reads a part must ask for it, even when the view around
 * it does not.
 *
 * These are fetched after the layer is already on screen and drawn again when
 * they land, so they cost nothing at the moment of switching.
 */
const LAYER_EXTRAS = {
  contracts: ['journeys', 'backend'], // links pane: called-by-screens, persisted-as; lineage chips
  backend: ['journeys'],              // table pane: the screens that reach it
  frontend: ['backend'],              // screen chips: is this table real
};

const ALL_PARTS = ['journeys', 'backend', 'domain', 'lineage', 'decisions'];

// ── the fields the index no longer carries ──────────────────────────
// The per-layer split above could not touch /api/index, because every layer
// needs it — it was 1.9 MB of the 3.0 MB the viewer fetched to open. Two
// fields are three tenths of that on their own, and neither is ever read for
// more than one contract at a time: the fields of all 554 schemas, which only
// the ER diagram reads, and the prose on every node, which only the reader
// shows.
//
// So they arrive per contract and are merged back into the node objects the
// index already delivered. Merging rather than keeping a second map is what
// makes this a small change: every existing reader of `node.description` or
// `schema.properties` goes on working, and only the two views that need the
// fields have to wait for them.

const detailInFlight = new Map();

/** Puts the held-back fields back on the nodes of one contract. */
function ensureDetail(file) {
  if (!file || state.detailLoaded.has(file)) return Promise.resolve();
  if (detailInFlight.has(file)) return detailInFlight.get(file);

  const request = fetch(`/api/detail?file=${encodeURIComponent(file)}`)
    .then((r) => r.json())
    .catch(() => null)
    .then((detail) => {
      for (const [id, fields] of Object.entries(detail ?? {})) {
        const node = state.nodesById.get(id);
        if (node) Object.assign(node, fields);
      }
      // A failed fetch is marked loaded too. Retrying on every render would
      // hammer a server that is already unhappy, and the views below all
      // tolerate the fields being absent — they did so before this existed.
      state.detailLoaded.add(file);
      detailInFlight.delete(file);
    });

  detailInFlight.set(file, request);
  return request;
}

/**
 * The ER diagram needs one more round than the reader does. It draws the
 * schemas of one contract plus any schema they reference from another — and
 * which ones those are is written in `properties`, which is exactly the field
 * that has not arrived yet. So: fetch the contract, read the refs that appear,
 * then fetch the contracts they point into.
 */
async function ensureERDetail(file) {
  await ensureDetail(file);
  const own = (state.index?.nodes ?? []).filter((n) => n.type === 'schema' && n.file === file);
  const elsewhere = new Set();
  for (const schema of own) {
    for (const property of schema.properties ?? []) {
      const target = property.refTarget ? state.nodesById.get(property.refTarget) : null;
      if (target && target.file !== file) elsewhere.add(target.file);
    }
  }
  await Promise.all([...elsewhere].map(ensureDetail));
}

/** True once ensureERDetail would have nothing left to fetch. */
function erDetailReady(file) {
  if (!state.detailLoaded.has(file)) return false;
  const own = (state.index?.nodes ?? []).filter((n) => n.type === 'schema' && n.file === file);
  for (const schema of own) {
    for (const property of schema.properties ?? []) {
      const target = property.refTarget ? state.nodesById.get(property.refTarget) : null;
      if (target && !state.detailLoaded.has(target.file)) return false;
    }
  }
  return true;
}

const partInFlight = new Map();

/** Fetches one part once, no matter how many views ask for it at the time. */
function loadPart(key) {
  if (state[key]) return Promise.resolve(state[key]);
  if (partInFlight.has(key)) return partInFlight.get(key);
  const request = fetch(`/api/${key}`)
    .then((r) => r.json())
    .catch(() => null)
    .then((data) => {
      state[key] = data;
      partInFlight.delete(key);
      return data;
    });
  partInFlight.set(key, request);
  return request;
}

/**
 * Makes sure a layer's parts are in hand, then redraws — but only if the
 * reader is still on that layer. Switching away twice while two fetches are in
 * flight must not repaint the layer they have since left.
 */
async function ensureParts(keys, layerAtRequest) {
  const missing = keys.filter((k) => !state[k]);
  if (!missing.length) return [];
  document.body.dataset.loading = '1';
  await Promise.all(missing.map(loadPart));
  delete document.body.dataset.loading;
  if (layerAtRequest && state.layer !== layerAtRequest) return [];
  return missing;
}

async function loadIndex() {
  // Who this is, and what they may open. First, because it decides which tabs
  // are drawn — and a client asking for a layer they cannot have would be met
  // with a 403 rather than a view.
  state.session = await fetch('/api/session').then((r) => r.json()).catch(() => null);
  if (state.session?.layers && !state.session.layers.includes(state.layer)) {
    state.layer = state.session.layers[0];
  }

  // The index is the one part nothing can be drawn without: the tree, the
  // graph and every selection resolve against it.
  const index = await fetch('/api/index').then((r) => r.json());
  state.index = index;
  state.journeys = null;
  state.backend = null;
  state.domain = null;
  state.lineage = null;
  state.decisions = null;

  // Small, and read by every layer's hover text, so it is not worth deferring.
  state.tooltips = await fetch('/api/tooltips').then((r) => r.json()).catch(() => null);

  // The domain lenses. Every layer's tree marks its members, so this cannot be
  // a per-layer part — and at 3 KB gzipped it does not want to be. `byArtefact`
  // is already keyed `kind:id`, which is what a tree row asks with.
  state.domains = await fetch('/api/domains').then((r) => r.json()).catch(() => null);
  state.lensOf = new Map(Object.entries(state.domains?.byArtefact ?? {}));
  state.lensById = new Map((state.domains?.lenses ?? []).map((l) => [l.key, l]));
  // A contract file is not itself a lens member; its operations are. Rolling
  // them up means the tree can mark the file a reader actually clicks.
  state.lensByFile = new Map();
  for (const lens of state.domains?.lenses ?? []) {
    for (const m of lens.members) {
      if (m.kind !== 'operation' || !m.file) continue;
      const at = state.lensByFile.get(m.file) ?? new Set();
      at.add(lens.key);
      state.lensByFile.set(m.file, at);
    }
  }

  state.nodesById = new Map(index.nodes.map((n) => [n.id, n]));

  state.incoming = new Map();
  state.outgoing = new Map();
  for (const edge of index.edges) {
    if (edge.kind === 'contains') continue;
    if (!state.outgoing.has(edge.source)) state.outgoing.set(edge.source, []);
    if (!state.incoming.has(edge.target)) state.incoming.set(edge.target, []);
    state.outgoing.get(edge.source).push(edge);
    state.incoming.get(edge.target).push(edge);
  }

  state.byFile = new Map();
  for (const node of index.nodes) {
    if (node.type === 'file' || node.type === 'permission') continue;
    if (!state.byFile.has(node.file)) state.byFile.set(node.file, []);
    state.byFile.get(node.file).push(node);
  }

  // default both box diagrams to the largest spine contract so the views are
  // never empty on first open
  const defaultFile =
    state.erScope ??
    index.nodes
      .filter((n) => n.type === 'file' && n.group === 'spine')
      .sort((a, b) => b.lineCount - a.lineCount)[0]?.file ??
    index.nodes.find((n) => n.type === 'file')?.file;

  state.erScope = state.erScope ?? defaultFile;
  fillScopeSelect($('er-scope'), state.erScope);

  applyPartDefaults();

  renderSideGroups();
  renderTree();
  renderTypeFilters();
  renderSideNote();
  renderAudit();
  renderGraph();
  renderER();
  // The data diagram and the two domain pickers are built from parts that are
  // now fetched on demand, so they are filled by hydrateLayer when those parts
  // arrive rather than here, where there would be nothing to fill them with.
}

/** Problems belong to the layer that produced them. */
function layerProblems(key = state.layer) {
  if (key === 'frontend') return state.journeys?.problems ?? [];
  if (key === 'backend') return state.backend?.problems ?? [];
  if (key === 'domain') return state.domain?.problems ?? [];
  // the tooltips are generated from the contracts and the lineage joins them to
  // the tables, so both of those are findings about the API rather than about docs
  if (key === 'decisions') return state.decisions?.problems ?? [];
  return [
    ...(state.index?.problems ?? []),
    ...(state.lineage?.problems ?? []),
    ...(state.tooltips?.problems ?? []),
  ];
}

function updateAuditBadge() {
  const badge = $('audit-count');
  if (!badge) return;
  const errors = layerProblems().filter((p) => p.severity === 'error').length;
  badge.textContent = errors;
  badge.classList.toggle('show', errors > 0);
}

// ── mode switching ───────────────────────────────────────────────────
export function setMode(mode) {
  // a keyboard shortcut can name a view another layer owns — follow it there
  if (!layerOf(state.layer).modes.some(([m]) => m === mode)) {
    const owner = LAYERS.find((l) => l.modes.some(([m]) => m === mode));
    if (owner && owner.key !== state.layer) {
      state.mode = mode;
      setLayer(owner.key);
      return;
    }
  }

  state.mode = mode;
  // whatever asked for this view — a mode button, a tree row, a search hit —
  // the point was to look at it, so nothing may be left covering it
  setDrawer(null);
  for (const view of VIEWS) $(`view-${view}`).hidden = view !== mode;
  for (const button of $('modes').querySelectorAll('.mode')) {
    button.classList.toggle('active', button.dataset.mode === mode);
  }
  revealActive($('modes'));
  if (mode === 'graph') {
    // the canvas measures 0x0 while hidden, so re-measure now that it is laid out
    graph.resize();
    if (!graph.hasFramed) {
      graph.recenter();
      graph.hasFramed = true;
    }
    graph.reheat(0.2);
  }

  if (mode === 'structure') {
    // the canvas was 0x0 while hidden, so re-measure before drawing
    tree.resize();
    if (!tree.root && state.selectedId) {
      renderStructure(state.nodesById.get(state.selectedId));
    } else if (tree.selectedPath) {
      tree.focusPath(tree.selectedPath, { zoom: Math.max(tree.transform.k, 1) });
    } else {
      tree.fit();
    }
    renderStructLegend();
  }

  // both box diagrams were 0x0 while hidden, so measure then frame
  if (mode === 'er') {
    er.resize();
    if (!er.nodes.length) renderER({ focus: state.selectedId });
    if (!er.userAdjusted) er.fit();
  }

  if (mode === 'data') {
    // measured 0x0 while hidden, so re-measure before framing anything
    data.resize();
    if (!data.nodes.length) renderData();
    else if (!data.userAdjusted) data.fit();
  }

  if (mode === 'states') {
    // measured 0x0 while hidden, like every other canvas here
    machine.resize();
    if (!machine.nodes.length) renderStates();
    if (!machine.userAdjusted) machine.fit();
  }
  if (mode === 'events') renderEvents();

  if (mode === 'journey') renderJourney();
  if (mode === 'screen') renderScreen();
  if (mode === 'apps') renderApps();
  if (mode === 'waves') renderWaves();
  if (mode === 'lineage') renderLineage();
  if (mode === 'decisions') renderDecisions();
  if (mode === 'timeline') renderTimeline();
  if (mode === 'supersession') renderSupersession();
  if (mode === 'register') renderRegister();
  if (mode === 'decision') renderDecision();
  if (mode === 'migrations') renderMigrations();
  if (mode === 'routing') renderRouting();
}

// ── selection ────────────────────────────────────────────────────────
function select(id, { scroll = true } = {}) {
  const node = state.nodesById.get(id);
  if (!node) return;

  state.selectedId = id;
  location.hash = encodeURIComponent(id);

  graph.setSelected(id);
  if (state.graphScope === 'local') renderGraph();

  renderLinksPane(node);
  syncLinksToggle();
  renderReader(node, { scroll });
  renderStructure(node);
  syncBoxDiagrams(node);
  markTreeSelection();
}

/**
 * Keep ER and Flow pointed at the selected node's contract. They only rebuild
 * when the contract actually changes, so selecting within one contract just
 * moves the highlight rather than relaying out the diagram.
 */
function syncBoxDiagrams(node) {
  const file = node.file;
  if (!file) return;

  if (state.erScope !== file) {
    state.erScope = file;
    fillScopeSelect($('er-scope'), file);
    renderER({ focus: node.type === 'schema' ? node.id : null });
  } else {
    er.setSelected(node.id);
    if (state.mode === 'er' && node.type === 'schema') er.focus(node.id, { zoom: Math.max(er.transform.k, 0.9) });
  }

}

// ── left tree ────────────────────────────────────────────────────────
function renderTypeFilters() {
  const container = $('type-filters');
  container.innerHTML = '';
  for (const [type, label] of [
    ['operation', 'Operations'],
    ['schema', 'Schemas'],
    ['param', 'Params'],
    ['response', 'Responses'],
  ]) {
    const chip = el('button', 'chip', label);
    chip.classList.toggle('on', state.typeFilter.has(type));
    chip.onclick = () => {
      if (state.typeFilter.has(type)) state.typeFilter.delete(type);
      else state.typeFilter.add(type);
      renderTypeFilters();
      renderTree();
    };
    container.append(chip);
  }
}

/** The grouping options in the left pane head, rebuilt for the current layer. */
function renderSideGroups() {
  const bar = $('group-by');
  bar.innerHTML = '';
  for (const [key, label] of layerOf(state.layer).groups) {
    const button = el('button', null, label);
    button.dataset.group = key;
    button.classList.toggle('active', key === groupBy());
    button.onclick = () => {
      state.groupBy[state.layer] = key;
      for (const other of bar.querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderSideNote();
      renderTree();
    };
    bar.append(button);
  }
  // the type chips only mean anything for contract members
  $('type-filters').hidden = state.layer !== 'contracts';
  renderLensFilters();
}

/**
 * One chip per lens, on every layer.
 *
 * The point of the "within" half is that a reader on the Backend layer can ask
 * "which of these tables are AI's?" without leaving the layer or losing the
 * schema grouping. So the chip filters the tree in place rather than navigating
 * anywhere, and the Domains page stays the separate view for the whole set.
 */
function renderLensFilters() {
  const bar = $('lens-filters');
  if (!bar) return;
  const lenses = state.domains?.lenses ?? [];
  bar.innerHTML = '';
  bar.hidden = lenses.length === 0;
  if (!lenses.length) return;

  for (const lens of lenses) {
    const on = state.lensFilter === lens.key;
    const chip = el('button', `chip lens-chip lens-${lens.key}`, lens.label);
    chip.classList.toggle('on', on);
    // how many of this layer's rows the chip would leave standing, so the
    // reader knows before clicking whether it is worth clicking
    const here = countLensRows(lens.key);
    if (here) chip.append(el('span', 'lens-chip-count', String(here)));
    chip.title = on
      ? `Showing only the ${lens.label} lens. Click to show everything again.`
      : `Show only what is in the ${lens.label} lens — ${lens.stats.total} artefacts across every layer, ${here} of them here.`;
    chip.onclick = () => {
      state.lensFilter = on ? null : lens.key;
      renderLensFilters();
      renderTree();
    };
    bar.append(chip);
  }
}

/**
 * Rows of this layer's tree the lens would leave standing.
 *
 * Counted as rows, not as members, because the two differ where a tree groups.
 * The Contracts tree lists files: the AI lens holds 24 operations and they are
 * all in one contract, so a chip reading 24 promises a filter that leaves 24
 * rows and then leaves one. The chip has to count what the click will do.
 */
function countLensRows(key) {
  const lens = state.lensById?.get(key);
  if (!lens) return 0;
  if (state.layer === 'contracts') {
    return new Set(
      lens.members.filter((m) => m.kind === 'operation' && m.file).map((m) => m.file)
    ).size;
  }
  const kinds = {
    frontend: ['screen'], backend: ['table'],
    domain: ['state', 'event'], decisions: ['decision'],
  }[state.layer] ?? [];
  return lens.members.filter((m) => kinds.includes(m.kind)).length;
}

/** True when a row survives the lens filter. No filter, everything survives. */
function passesLens(kind, id) {
  if (!state.lensFilter) return true;
  return lensesFor(kind, id).includes(state.lensFilter);
}

function renderTree() {
  if (state.layer === 'frontend') return renderScreenTree();
  if (state.layer === 'backend') return renderTableTree();
  if (state.layer === 'domain') return renderDomainTree();
  if (state.layer === 'decisions') return renderDecisionsTree();
  return renderContractTree();
}

/** The ADRs and the registers, as a list you can jump from. */
function renderDecisionsTree() {
  const box = $('tree');
  box.innerHTML = '';
  const needle = state.sideFilter;
  const hit = (s) => !needle || String(s ?? '').toLowerCase().includes(needle);
  const decisions = state.decisions;
  if (!decisions?.present) {
    box.append(el('p', 'pane-empty', 'No docs/ in this package.'));
    return;
  }

  let count = 0;
  const section = (label, sub, color) => {
    const group = el('div', 'tree-group');
    const head = el('div', 'tree-group-head');
    const dot = el('span', 'tree-group-dot');
    dot.style.background = color;
    head.append(dot, el('span', null, label));
    const badge = el('span', 'tree-group-count');
    head.append(badge);
    group.append(head);
    group.append(el('div', 'tree-group-sub', sub));
    return { group, badge };
  };

  if (groupBy() === 'decisions') {
    const { group, badge } = section('Decisions', 'docs/adr/', '#a78bfa');
    let shown = 0;
    for (const adr of decisions.adrs) {
      if (!hit(adr.title) && !hit(adr.id) && !hit(adr.closes)) continue;
      shown += 1;
      count += 1;
            if (!passesLens('decision', adr.id)) continue;
const row = el('div', 'tree-file');
      row.append(el('span', 'tree-file-name', `${adr.id} ${adr.title}`));
      const mark = el('span', 'tree-file-count', adr.partlySuperseded ? 'part' : (adr.verdict ?? '—'));
      markLens(row, 'decision', adr.id);
      if (adr.partlySuperseded) row.classList.add('problem');
      row.append(mark);
      deliveryTip(row, 'adrs', adr.id, {
        fallback: { title: `ADR-${adr.id}`, body: adr.decision || adr.lead },
      });
      row.onclick = () => {
        state.decisionsScope = 'adrs';
        state.decisionsFilter = adr.id;
        $('decisions-filter').value = adr.id;
        setLayer('decisions');
        setMode('decisions');
      };
      group.append(row);
    }
    badge.textContent = String(shown);
    box.append(group);
  } else {
    for (const [key, label, sub, color] of [
      ['register', 'Registers', 'docs/registers/', '#34d399'],
      ['handoff', 'Handoff', 'handoff/', '#60a5fa'],
      ['architecture', 'Architecture', 'docs/architecture/', '#fbbf24'],
      ['active', 'In flight', 'docs/active/', '#f472b6'],
      ['guide', 'Guides', 'docs/', '#94a3b8'],
    ]) {
      const list = decisions.documents.filter(
        (d) => d.group === key && (hit(d.title) || hit(d.id) || hit(d.lead))
      );
      if (!list.length) continue;
      const { group, badge } = section(label, sub, color);
      badge.textContent = String(list.length);
      for (const doc of list) {
        count += 1;
        const row = el('div', 'tree-file');
        row.append(el('span', 'tree-file-name', doc.title));
        if (doc.rows) row.append(el('span', 'tree-file-count', String(doc.rows)));
        tip(row, doc.title, doc.lead || 'No lead paragraph.',
          `${doc.lines} lines · ${doc.rows} table rows`);
        row.onclick = () => openDoc(doc.file);
        group.append(row);
      }
      box.append(group);
    }
  }

  $('file-count').textContent = `${count} items`;
}

function renderContractTree() {
  const tree = $('tree');
  tree.innerHTML = '';

  const groups = sidebarGroups();

  if (!groups.size) {
    tree.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
    return;
  }

  let shownFiles = 0;
  for (const [group, groupFiles] of groups) {
    const { code, label } = splitGroupLabel(group);
    const section = el('div', 'tree-group');
    const head = el('div', 'tree-group-head');
    const dot = el('span', 'tree-group-dot');
    dot.style.background = groupColor(group, groupFiles);
    head.append(dot, el('span', null, label));
    head.append(el('span', 'tree-group-count', String(groupFiles.length)));
    section.append(head);
    if (code) section.append(el('div', 'tree-group-sub', code));

    for (const file of groupFiles.sort((a, b) => a.name.localeCompare(b.name))) {
      if (!passesLens('file', file.file)) continue;
      shownFiles += 1;
      const row = el('div', 'tree-file');
      row.dataset.id = file.id;
      row.append(el('span', 'tree-file-name', file.name));
      // what this contract is for, in the delivery's own words
      deliveryTip(row, 'contracts', file.file.split('/').pop().replace(/\.ya?ml$/, ''));

      const children = state.byFile.get(file.file) ?? [];
      const visible = children.filter((c) => state.typeFilter.has(c.type));
      row.append(el('span', 'tree-file-count', String(visible.length)));
      markLens(row, 'file', file.file);

      const childBox = el('div', 'tree-children');

      row.onclick = () => {
        const expanded = state.expandedFiles.has(file.id);
        if (expanded) state.expandedFiles.delete(file.id);
        else state.expandedFiles.add(file.id);
        row.classList.toggle('expanded', !expanded);
        if (!expanded && !childBox.dataset.filled) {
          fillChildren(childBox, visible);
          childBox.dataset.filled = '1';
        }
        select(file.id);
      };

      if (state.expandedFiles.has(file.id)) {
        row.classList.add('expanded');
        fillChildren(childBox, visible);
        childBox.dataset.filled = '1';
      }

      section.append(row, childBox);
    }
    tree.append(section);
  }

  const label = groupBy() === 'contracts' ? 'tiers'
    : groupBy() === 'modules' ? 'modules' : 'platforms';
  $('file-count').textContent = `${groups.size} ${label} · ${shownFiles} listed`;
  markTreeSelection();
}

// ── sidebar: frontend layer ──────────────────────────────────────────
const PLATFORM_COLOR = ['#38bdf8', '#34d399', '#c084fc', '#fbbf24', '#f472b6', '#60a5fa'];

function renderScreenTree() {
  const box = $('tree');
  box.innerHTML = '';
  const screens = (state.journeys?.screens ?? []).filter(matchesScreenFilter);

  const key =
    groupBy() === 'modules' ? (s) => s.module ?? '(no module)'
    : groupBy() === 'waves' ? (s) => (s.wave ? `Wave ${s.wave}` : '(no wave)')
    : (s) => `${s.platform ?? '??'} ${s.platformName ?? ''}`.trim();

  const groups = new Map();
  for (const screen of screens) {
    const k = key(screen);
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(screen);
  }

  if (!groups.size) {
    box.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
    $('file-count').textContent = '';
    return;
  }

  let index = 0;
  for (const [group, list] of [...groups].sort((a, b) => a[0].localeCompare(b[0]))) {
    const { code, label } = splitGroupLabel(group);
    const section = el('div', 'tree-group');
    const head = el('div', 'tree-group-head');
    const dot = el('span', 'tree-group-dot');
    dot.style.background = PLATFORM_COLOR[index++ % PLATFORM_COLOR.length];
    head.append(dot, el('span', null, label || group));
    head.append(el('span', 'tree-group-count', String(list.length)));
    section.append(head);
    if (code) section.append(el('div', 'tree-group-sub', code));

    for (const screen of list.sort((a, b) => a.id.localeCompare(b.id))) {
      if (!passesLens('screen', screen.id)) continue;
      const row = el('div', 'tree-file');
      row.dataset.id = `screen:${screen.id}`;
      row.append(el('span', 'tree-file-code', screen.id));
      row.append(el('span', 'tree-file-name', screen.name));
      row.append(el('span', 'tree-file-count', String(screen.apis.length)));
      markLens(row, 'screen', screen.id);
      row.title = `${screen.purpose || screen.name}\n${screen.apis.length} operations · ${screen.file}`;
      row.onclick = () => selectScreen(screen.id);
      section.append(row);
    }
    box.append(section);
  }

  // ---- design boards ---------------------------------------------------
  // Listed on their own rather than under a platform group: the board for a
  // platform with no screen definitions has no group to sit in, and that is
  // exactly the case worth surfacing.
  const shown = boards().filter(matchesBoardFilter);
  if (shown.length) {
    const section = el('div', 'tree-group');
    const head = el('div', 'tree-group-head');
    const dot = el('span', 'tree-group-dot');
    dot.style.background = '#f0abfc';
    head.append(dot, el('span', null, 'DESIGN BOARDS'));
    head.append(el('span', 'tree-group-count', String(shown.length)));
    section.append(head);
    section.append(el('div', 'tree-group-sub', 'UIUX_html · exported HTML'));

    for (const board of shown) {
      const row = el('div', 'tree-file board-row');
      row.dataset.id = `board:${board.id}`;
      row.append(el('span', 'tree-file-code', board.platform ?? '—'));
      row.append(el('span', 'tree-file-name', board.name + (board.revision ? ` ${board.revision}` : '')));
      row.title =
        `${board.file}\n${board.platform ? `${board.platform} ${board.platformName}` : 'no platform matched'}` +
        `${board.inferred ? ` (inferred from the file name)` : ''}`;
      row.onclick = () => selectBoard(board.id);
      section.append(row);
    }
    box.append(section);
  }

  const noun = groupBy() === 'waves' ? 'waves' : groupBy() === 'modules' ? 'modules' : 'platforms';
  $('file-count').textContent =
    `${groups.size} ${noun} · ${screens.length} screens` +
    (shown.length ? ` · ${shown.length} boards` : '');
  markTreeSelection();
}

function matchesBoardFilter(board) {
  const needle = state.sideFilter;
  if (!needle) return true;
  return (
    board.name.toLowerCase().includes(needle) ||
    (board.platform ?? '').toLowerCase().includes(needle) ||
    (board.platformName ?? '').toLowerCase().includes(needle) ||
    'design board'.includes(needle)
  );
}

function matchesScreenFilter(screen) {
  const needle = state.sideFilter;
  if (!needle) return true;
  return (
    screen.id.toLowerCase().includes(needle) ||
    screen.name.toLowerCase().includes(needle) ||
    (screen.module ?? '').toLowerCase().includes(needle) ||
    (screen.purpose ?? '').toLowerCase().includes(needle) ||
    screen.apis.some((a) => a.operationId.toLowerCase().includes(needle))
  );
}

// ── sidebar: backend layer ───────────────────────────────────────────
function renderTableTree() {
  const box = $('tree');
  box.innerHTML = '';
  const tables = (state.backend?.tables ?? []).filter(matchesTableFilter);
  const byModule = new Map((state.backend?.modules ?? []).map((m) => [m.name, m]));

  const groups = new Map();
  for (const table of tables) {
    const k =
      groupBy() === 'migration' ? (table.migration ?? '(no migration)')
      : groupBy() === 'status' ? (table.ddl ? 'In the database' : 'Planned')
      : table.module;
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(table);
  }

  if (!groups.size) {
    box.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
    $('file-count').textContent = '';
    return;
  }

  for (const [group, list] of [...groups].sort((a, b) => a[0].localeCompare(b[0]))) {
    const module = byModule.get(group);
    const written = groupBy() === 'status' ? group === 'In the database' : module?.written;
    const section = el('div', 'tree-group');
    const head = el('div', 'tree-group-head');
    const dot = el('span', 'tree-group-dot');
    // green where the SQL exists, amber where the table is still only planned
    dot.style.background = written ? '#34d399' : '#fbbf24';
    head.append(dot, el('span', null, group));
    head.append(el('span', 'tree-group-count', String(list.length)));
    // The 14 August workbook added "What it is" and "Why it is separate" — the
    // best short description of a schema anywhere in the delivery, and until
    // now readable only by opening the spreadsheet.
    if (module?.what || module?.why) {
      tip(
        head,
        `${module.name}${module.tier ? ` — ${module.tier}` : ''}`,
        [module.what, module.why && `**Why it is separate.** ${module.why}`].filter(Boolean).join('\n\n'),
        [
          module.tables != null ? `${module.tables} tables` : null,
          module.operations != null ? `${module.operations} operations` : null,
          module.contract ? `contract ${module.contract}` : null,
        ].filter(Boolean).join(' · ') || null
      );
    }
    section.append(head);
    if (groupBy() !== 'status' && module?.migration) {
      section.append(el('div', 'tree-group-sub', module.migration));
    }

    for (const table of list.sort((a, b) => a.name.localeCompare(b.name))) {
            if (!passesLens('table', table.name)) continue;
const row = el('div', `tree-file${table.ddl ? ' written' : ''}`);
      row.dataset.id = `table:${table.name}`;
      const label = groupBy() === 'modules'
        ? table.name.split('.').slice(1).join('.') || table.name
        : table.name;
      row.append(el('span', 'tree-file-name', label));
      row.append(el('span', 'tree-file-count', String(table.columns ?? 0)));
      markLens(row, 'table', table.name);
      // "Table tips say why, not what" — the column list is already on screen
      deliveryTip(row, 'tables', table.name, {
        fallback: {
          title: table.name,
          // the workbook's own reason for the table is the better answer, and it
          // is the one the tooltip file was supposed to be carrying
          body:
            table.storageReason ||
            (table.ddl
              ? `Created by ${table.ddl.file}. No reason for it is recorded anywhere.`
              : '**Planned — no migration writes it yet**, and no reason for it is recorded.'),
          extra: [
            table.derivedFrom ? `from ${table.derivedFrom}` : null,
            table.columns ? `${table.columns} columns` : null,
          ].filter(Boolean).join(' · ') || null,
        },
      });
      row.title =
        `${table.name}\n` +
        `${table.ddl ? `created by ${table.ddl.file}` : 'planned — no migration yet'}\n` +
        `from ${table.derivedFrom ?? table.storageReason ?? 'nothing declared'}`;
      row.onclick = () => selectTable(table.name);
      section.append(row);
    }
    box.append(section);
  }

  const noun = groupBy() === 'migration' ? 'migrations' : groupBy() === 'status' ? 'states' : 'schemas';
  $('file-count').textContent = `${groups.size} ${noun} · ${tables.length} tables`;
  markTreeSelection();
}

function matchesTableFilter(table) {
  const needle = state.sideFilter;
  if (!needle) return true;
  return (
    table.name.toLowerCase().includes(needle) ||
    (table.derivedFrom ?? '').toLowerCase().includes(needle) ||
    (state.backend?.columns?.[table.name] ?? []).some((c) => c.name.toLowerCase().includes(needle))
  );
}

function fillChildren(container, children) {
  container.innerHTML = '';
  const operations = children.filter((c) => c.type === 'operation');
  const others = children.filter((c) => c.type !== 'operation');

  if (operations.length) {
    container.append(el('div', 'tree-section', `Operations · ${operations.length}`));
    for (const op of operations.sort((a, b) => a.path.localeCompare(b.path))) {
      const row = el('div', 'tree-child');
      row.dataset.id = op.id;
      row.append(el('span', `method ${op.method}`, op.method));
      row.append(el('span', 'tree-child-name', op.name));
      row.title = `${op.method} ${op.path}`;
      row.onclick = (e) => { e.stopPropagation(); select(op.id); setMode('reader'); };
      container.append(row);
    }
  }

  if (others.length) {
    container.append(el('div', 'tree-section', `Components · ${others.length}`));
    for (const item of others.sort((a, b) => a.name.localeCompare(b.name))) {
      const row = el('div', 'tree-child');
      row.dataset.id = item.id;
      const dot = el('span', 'type-dot');
      dot.style.background = colorForNode(item);
      row.append(dot, el('span', 'tree-child-name', item.name));
      row.title = `${TYPE_LABEL[item.type]} · ${item.inCount} backlinks`;
      row.onclick = (e) => { e.stopPropagation(); select(item.id); setMode('reader'); };
      container.append(row);
    }
  }
}

/** What the left pane should be highlighting, whichever layer is showing. */
function currentSideId() {
  if (state.layer === 'frontend') {
    if (state.boardId) return `board:${state.boardId}`;
    return state.screenId ? `screen:${state.screenId}` : null;
  }
  if (state.layer === 'backend') return state.tableName ? `table:${state.tableName}` : null;
  return state.selectedId;
}

function markTreeSelection() {
  const current = currentSideId();
  for (const row of $('tree').querySelectorAll('[data-id]')) {
    row.classList.toggle('selected', row.dataset.id === current);
  }
  const selected = $('tree').querySelector('.selected');
  selected?.scrollIntoView({ block: 'nearest' });
}

// ── graph ────────────────────────────────────────────────────────────
function renderGraph() {
  const { nodes, edges, fileEdges } = state.index;
  let viewNodes = [];
  let viewEdges = [];
  let hint = '';

  if (state.graphScope === 'spine') {
    return renderSpine();
  } else if (state.graphScope === 'files') {
    graph.reserveBottom = 0;
    viewNodes = nodes.filter((n) => n.type === 'file');
    viewEdges = fileEdges;
    // Every one of these 44 edges points at shared/common or shared/permissions;
    // no contract $refs another. Saying so is more use than a hint claiming the
    // dots are sized by something, when a file node's degree is always zero.
    const toShared = fileEdges.filter((e) => /\/shared\//.test(e.target)).length;
    hint =
      `${viewNodes.length} contracts · ${fileEdges.length} $ref links, ${toShared} of them to ` +
      `shared/. Spine has the picture that distinguishes them.`;
  } else if (state.graphScope === 'schemas') {
    const keep = new Set(['schema', 'param', 'response', 'requestBody']);
    viewNodes = nodes.filter((n) => keep.has(n.type));
    const ids = new Set(viewNodes.map((n) => n.id));
    viewEdges = edges.filter((e) => ids.has(e.source) && ids.has(e.target));
    hint = 'Components and the $refs between them';
  } else if (state.graphScope === 'permissions') {
    viewNodes = nodes.filter((n) => n.type === 'permission' || n.type === 'file');
    const permIds = new Set(nodes.filter((n) => n.type === 'permission').map((n) => n.id));
    const aggregate = new Map();
    for (const edge of edges) {
      if (edge.kind !== 'permission' || !permIds.has(edge.target)) continue;
      const file = state.nodesById.get(edge.source)?.file;
      if (!file) continue;
      const key = `file:${file}|${edge.target}`;
      if (aggregate.has(key)) aggregate.get(key).weight += 1;
      else aggregate.set(key, { source: `file:${file}`, target: edge.target, kind: 'permission', weight: 1 });
    }
    viewEdges = [...aggregate.values()];
    hint = 'Which contracts use which permissions';
  } else {
    // local — neighbourhood of the selection, two hops out
    const anchor = state.selectedId;
    if (!anchor) {
      hint = 'Select a node to see its local graph';
      graph.setData([], []);
      $('graph-hint').textContent = hint;
      renderLegend();
      return;
    }
    const anchorNode = state.nodesById.get(anchor);
    const keep = new Set([anchor]);

    // A contract has no $refs of its own — its operations and schemas do, and
    // the adjacency map deliberately leaves out `contains`. Walking from a file
    // node therefore found nothing at all, so a whole contract is seeded with
    // everything defined inside it and the walk starts from there.
    const isFile = anchorNode?.type === 'file';
    if (isFile) {
      for (const child of state.byFile.get(anchorNode.file) ?? []) keep.add(child.id);
    }

    // A contract is already dozens of nodes before the walk starts, so one hop
    // from it reaches as far as two hops from a single operation.
    const hops = isFile ? 1 : 2;
    let frontier = new Set(keep);
    for (let hop = 0; hop < hops; hop++) {
      const next = new Set();
      for (const id of frontier) {
        for (const edge of state.outgoing.get(id) ?? []) if (!keep.has(edge.target)) next.add(edge.target);
        for (const edge of state.incoming.get(id) ?? []) if (!keep.has(edge.source)) next.add(edge.source);
      }
      for (const id of next) keep.add(id);
      frontier = next;
      if (keep.size > 220) break; // hub nodes like Money would swamp the view
    }
    viewNodes = nodes.filter((n) => keep.has(n.id));
    // `contains` is structure rather than reference, so it stays out — except
    // from the contract itself, which would otherwise float unattached to the
    // components that are the reason it is on screen
    viewEdges = edges.filter(
      (e) =>
        keep.has(e.source) &&
        keep.has(e.target) &&
        (e.kind !== 'contains' || (isFile && e.source === anchor))
    );
    const name = anchorNode?.name ?? '';
    hint =
      viewNodes.length === 1
        ? `${name} references nothing and nothing references it`
        : isFile
          ? `${name} — what it defines and everything those reference · ${viewNodes.length} nodes`
          : `${viewNodes.length} nodes within 2 hops of ${name}`;
  }

  graph.colorBy = state.graphScope === 'files' ? 'group' : 'type';
  graph.setData(viewNodes, viewEdges);
  graph.setSelected(state.selectedId);
  $('graph-hint').textContent = hint;
  renderLegend();
  graph.hasFramed = false;

  // an early frame so a settling layout still looks sensible, then a final one
  // when the simulation converges (wired to onSettle in boot)
  setTimeout(() => {
    if (state.mode !== 'graph' || graph.userAdjusted) return;
    graph.resize();
    graph.recenter();
  }, 400);
}

// ── contracts: the spine ─────────────────────────────────────────────
// The Files graph draws 24 contracts and 44 links, and every single link points
// at shared/common or shared/permissions. Not one contract $refs another. So
// the picture it produces is a two-pointed starburst that is true of everything
// and distinguishes nothing — the same defect the schema notes call out for
// venue_id and principal_id in the data view.
//
// The contracts are not joined by $refs. They are joined by events: `order.paid`
// is published by orders and consumed by catalogue, finance, inventory,
// marketing and reporting. Until states/ and events/ arrived there was nothing
// to draw that from. Now there is, so this is what the layer opens on.
//
// Position carries meaning here and the force layout is switched off: shared at
// the centre because everything rests on it, spine in the inner ring, satellites
// outside. Within each ring the order is settled by pulling contracts that
// exchange events next to each other, so the arrows stay short.
const SPINE_RING = 215;
const SATELLITE_RING = 395;

function renderSpine() {
  const contracts = state.index.nodes.filter((n) => n.type === 'file');
  const byFile = new Map(contracts.map((c) => [c.file, c]));

  // one edge per ordered pair of contracts, carrying every event between them
  const pairs = new Map();
  for (const link of state.domain?.contextEdges ?? []) {
    if (!link.fromContract || !link.toContract || link.fromContract === link.toContract) continue;
    if (!byFile.has(link.fromContract) || !byFile.has(link.toContract)) continue;
    const key = `${link.fromContract}|${link.toContract}`;
    if (!pairs.has(key)) {
      pairs.set(key, {
        source: `file:${link.fromContract}`,
        target: `file:${link.toContract}`,
        events: [],
        critical: 0,
      });
    }
    const edge = pairs.get(key);
    edge.events.push(link.event);
    if (link.critical) edge.critical += 1;
  }

  const showShared = $('graph-shared')?.checked;
  const sharedEdges = showShared
    ? state.index.fileEdges.filter((e) => /\/shared\//.test(e.target))
    : [];

  // ---- placement ---------------------------------------------------------
  const ringOf = (node) => (node.group === 'shared' ? 0 : node.group === 'spine' ? 1 : 2);
  const rings = [[], [], []];
  for (const contract of contracts) rings[ringOf(contract)].push(contract);
  for (const ring of rings) ring.sort((a, b) => a.name.localeCompare(b.name));

  // neighbours by event, in both directions — adjacency is what decides the order
  const near = new Map(contracts.map((c) => [c.id, []]));
  for (const edge of pairs.values()) {
    near.get(edge.source)?.push(edge.target);
    near.get(edge.target)?.push(edge.source);
  }

  const angle = new Map();
  for (const ring of rings) {
    ring.forEach((node, i) => angle.set(node.id, (i / Math.max(1, ring.length)) * Math.PI * 2));
  }

  // Settle each ring by circular barycentre: a contract drifts towards the mean
  // direction of whatever it exchanges events with, then the ring is re-spaced
  // evenly in the new order. Re-spacing is what stops everything collapsing onto
  // the busiest quarter of the circle.
  for (let pass = 0; pass < 30; pass++) {
    const next = new Map(angle);
    for (const node of contracts) {
      const neighbours = near.get(node.id) ?? [];
      if (!neighbours.length) continue;
      let sin = 0;
      let cos = 0;
      for (const id of neighbours) {
        sin += Math.sin(angle.get(id) ?? 0);
        cos += Math.cos(angle.get(id) ?? 0);
      }
      if (sin === 0 && cos === 0) continue;
      next.set(node.id, Math.atan2(sin, cos));
    }
    for (const ring of rings) {
      if (ring.length < 2) continue;
      const sorted = [...ring].sort(
        (a, b) => (next.get(a.id) ?? 0) - (next.get(b.id) ?? 0) || a.name.localeCompare(b.name)
      );
      sorted.forEach((node, i) => angle.set(node.id, (i / ring.length) * Math.PI * 2));
      ring.splice(0, ring.length, ...sorted);
    }
  }

  const viewNodes = contracts.map((contract) => {
    const ring = ringOf(contract);
    const members = state.byFile.get(contract.file) ?? [];
    const operations = members.filter((m) => m.type === 'operation').length;
    const theta = angle.get(contract.id) ?? 0;
    const radius = ring === 0 ? (rings[0].length > 1 ? 62 : 0) : ring === 1 ? SPINE_RING : SATELLITE_RING;
    return {
      ...contract,
      // sized by what a contract actually contains, not by its degree — which
      // is zero for every one of them
      weight: Math.max(1, operations),
      operations,
      x: Math.cos(theta - Math.PI / 2) * radius,
      y: Math.sin(theta - Math.PI / 2) * radius,
    };
  });

  const light = document.documentElement.dataset.theme === 'light';
  const viewEdges = [
    ...sharedEdges.map((edge) => ({
      ...edge,
      width: 0.6,
      color: light ? 'rgba(0,0,0,.09)' : 'rgba(255,255,255,.07)',
      shared: true,
    })),
    ...[...pairs.values()].map((edge) => ({
      source: edge.source,
      target: edge.target,
      kind: 'event',
      weight: edge.events.length,
      events: edge.events,
      // a critical consumer is one the business breaks without: a dead-lettered
      // order.paid means a guest paid and holds nothing
      width: 1.1 + edge.events.length * 0.5 + (edge.critical ? 0.8 : 0),
      color: edge.critical
        ? (light ? 'rgba(180,83,9,.72)' : 'rgba(251,191,36,.72)')
        : (light ? 'rgba(37,99,235,.5)' : 'rgba(96,165,250,.5)'),
    })),
  ];

  graph.colorBy = 'group';
  // the spine legend is the tallest in the app — seven rows — so the frame has
  // to keep the ring out from under it
  graph.reserveBottom = 150;
  graph.setData(viewNodes, viewEdges, { placed: true, directed: true });
  graph.setSelected(state.selectedId);

  const d = state.domain?.stats;
  $('graph-hint').textContent = d
    ? `${contracts.length} contracts · ${pairs.size} event links between them · ` +
      `${d.criticalConsumers} critical consumers` +
      (showShared ? ` · ${sharedEdges.length} shared $refs` : '')
    : `${contracts.length} contracts · events/ not readable, so no links between them`;

  renderLegend();
  graph.hasFramed = true;
  requestAnimationFrame(() => {
    graph.resize();
    graph.recenter();
  });
}

/** Controls that only mean something in one scope are hidden in the others. */
function syncGraphControls() {
  const spine = state.graphScope === 'spine';
  for (const node of document.querySelectorAll('.spine-only')) node.hidden = !spine;
  // the spine layout is placed rather than simulated, so there is nothing to
  // recenter that Fit does not already do
  $('graph-recenter').textContent = spine ? 'Fit' : 'Recenter';
}

function renderLegend() {
  const legend = $('graph-legend');
  legend.innerHTML = '';
  if (state.graphScope === 'spine') {
    for (const [key, label] of [
      ['spine', 'spine — the inner ring'],
      ['satellite', 'satellite — the outer ring'],
      ['shared', 'shared — the centre, refd by all 22'],
    ]) {
      const row = el('div', 'legend-row');
      const dot = el('span', 'legend-dot');
      dot.style.background = colorForNode({ group: key, type: 'file' }, 'group');
      legend.append(row);
      row.append(dot, el('span', null, label));
    }
    for (const [color, label] of [
      ['#fbbf24', 'an event with a critical consumer'],
      ['#60a5fa', 'an event — the arrow runs publisher → consumer'],
    ]) {
      const row = el('div', 'legend-row');
      const dot = el('span', 'legend-dot');
      dot.style.background = color;
      row.append(dot, el('span', null, label));
      legend.append(row);
    }
    legend.append(el('div', 'legend-row', 'dot size is the operation count · hover a contract to isolate its events'));
    return;
  }
  const entries =
    state.graphScope === 'files'
      ? [['spine', 'spine'], ['satellite', 'satellite'], ['shared', 'shared']]
      : state.graphScope === 'permissions'
        ? [['file', 'contract'], ['permission', 'permission']]
        : state.graphScope === 'schemas'
          ? [['schema', 'schema'], ['param', 'parameter'], ['response', 'response']]
          : [['file', 'contract'], ['operation', 'operation'], ['schema', 'schema'], ['permission', 'permission']];

  for (const [key, label] of entries) {
    const row = el('div', 'legend-row');
    const dot = el('span', 'legend-dot');
    dot.style.background =
      state.graphScope === 'files'
        ? colorForNode({ group: key, type: 'file' }, 'group')
        : colorForNode({ type: key });
    row.append(dot, el('span', null, label));
    legend.append(row);
  }
  legend.append(el('div', 'legend-row', 'scroll to zoom · drag to pan · double-click to open'));
}

function showTooltip(node, event) {
  const tip = $('graph-tooltip');
  if (!node || !event) { tip.hidden = true; return; }

  tip.innerHTML = '';
  tip.append(el('div', 'tt-title', node.name));
  if (node.type === 'operation') {
    tip.append(el('div', 'tt-sub', `${node.method} ${node.path}`));
  } else if (node.type === 'file') {
    tip.append(el('div', 'tt-sub', node.file));
  } else {
    tip.append(el('div', 'tt-sub', TYPE_LABEL[node.type] ?? node.type));
  }
  const inCount = node.inCount ?? 0;
  const outCount = node.outCount ?? 0;
  tip.append(el('div', 'tt-stat', `${inCount} in · ${outCount} out`));
  tip.hidden = false;

  const rect = $('graph-canvas').getBoundingClientRect();
  const x = Math.min(event.offsetX + 14, rect.width - tip.offsetWidth - 10);
  const y = Math.min(event.offsetY + 14, rect.height - tip.offsetHeight - 10);
  tip.style.left = `${x}px`;
  tip.style.top = `${y}px`;
}

// ── structure diagram ────────────────────────────────────────────────
const COMPONENT_SECTION = {
  schema: 'schemas',
  param: 'parameters',
  response: 'responses',
  requestBody: 'requestBodies',
  securityScheme: 'securitySchemes',
};

/** Where an indexed node lives inside the structure tree of its file. */
function structurePathFor(node) {
  if (node.type === 'operation') return `paths/${node.path}/${node.method.toLowerCase()}`;
  const section = COMPONENT_SECTION[node.type];
  return section ? `components/${section}/${node.name}` : null;
}

function describeTreeNode(node) {
  const where = node.line ? `line ${node.line}` : '';
  if (node.kind === 'scalar') return `${node.key ?? 'value'} · scalar · ${where}`;
  if (node.kind === 'ref') return `$ref → ${node.value} · ${where}`;
  if (node.kind === 'alias') return `alias ${node.value} · ${where}`;
  const count = node.children.length;
  const kind = node.kind === 'seq' ? 'sequence' : 'mapping';
  return `${node.key ?? 'root'} · ${kind} of ${count} · ${node.descendants} descendants · ${where}`;
}

async function fetchTree(relPath) {
  if (state.treeCache.has(relPath)) return state.treeCache.get(relPath);
  const res = await fetch(`/api/tree?path=${encodeURIComponent(relPath)}`);
  const data = await res.json();
  state.treeCache.set(relPath, data);
  return data;
}

/** Diagram `node`'s file, revealing and centring the node's own subtree. */
async function renderStructure(node) {
  if (!node) return;
  const file = node.file;
  $('struct-file').textContent = file;

  if (state.structureFile !== file) {
    const data = await fetchTree(file);
    state.structureFile = file;
    // operations and components sit 3 levels down, so open enough to show them
    tree.setData(data.root, { expandDepth: 2 });

    for (const problem of data.errors ?? []) {
      toast(`${file}: ${problem.message}`);
    }
  }

  const path = structurePathFor(node);
  if (path) {
    tree.revealPath(path);
    tree.selectedPath = path;
    if (state.mode === 'structure') {
      tree.resize();
      tree.focusPath(path, { zoom: 1 }); // land at readable size, not fit-to-tree
    }
    $('struct-hint').textContent = `${node.name} · ${path}`;
  } else {
    tree.selectedPath = null;
    $('struct-hint').textContent = `${(tree.root?.children ?? []).length} top-level keys`;
  }
  tree.draw();
  renderStructLegend();
}

function renderStructLegend() {
  const legend = $('struct-legend');
  legend.innerHTML = '';
  for (const [kind, label] of [
    ['map', 'mapping'],
    ['seq', 'sequence'],
    ['scalar', 'value'],
    ['ref', '$ref (click to follow)'],
  ]) {
    // arcs on the right connect a $ref to its target block in the same file
    const row = el('div', 'legend-row');
    const dot = el('span', 'legend-dot');
    dot.style.background = kindColor(kind);
    row.append(dot, el('span', null, label));
    legend.append(row);
  }
  legend.append(el('div', 'legend-row', 'click to fold one level · double-click to fold the branch'));
  legend.append(el('div', 'legend-row', 'purple curves link a $ref to its target block'));
}

// ── sidebar grouping ─────────────────────────────────────────────────
// The left pane groups the same contracts three ways: by folder tier, by the
// declared x-ticvai-module, or by the declared x-ticvai-platforms.

const NO_MODULE = '(no module declared)';
const NO_PLATFORM = '(no platform declared)';

function matchesSideFilter(file) {
  const needle = state.sideFilter;
  if (!needle) return true;
  if (file.name.toLowerCase().includes(needle)) return true;
  if ((file.module ?? '').toLowerCase().includes(needle)) return true;
  if ((file.platforms ?? []).some((p) => p.raw.toLowerCase().includes(needle))) return true;
  return (state.byFile.get(file.file) ?? []).some(
    (child) =>
      child.name.toLowerCase().includes(needle) ||
      (child.path ?? '').toLowerCase().includes(needle) ||
      (child.permission ?? '').toLowerCase().includes(needle)
  );
}

/** groupKey -> files, in the order the taxonomy declares. */
function sidebarGroups() {
  const taxonomy = state.index.taxonomy ?? { modules: [], platforms: [] };
  const files = state.index.nodes
    .filter((n) => n.type === 'file')
    .filter(matchesSideFilter);

  const groups = new Map();
  const add = (key, file) => {
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(file);
  };

  if (groupBy() === 'contracts') {
    for (const key of ['spine', 'satellite', 'shared']) groups.set(key, []);
    for (const file of files) add(file.tier ?? file.group, file);
  } else if (groupBy() === 'modules') {
    for (const module of taxonomy.modules) groups.set(module.name, []);
    for (const file of files) add(file.module ?? NO_MODULE, file);
  } else {
    const coded = taxonomy.platforms.filter((p) => !p.wildcard);
    for (const platform of coded) groups.set(platform.raw, []);
    for (const file of files) {
      const declared = file.platforms ?? [];
      if (!declared.length) { add(NO_PLATFORM, file); continue; }
      // "All platforms" means every coded platform, not a bucket of its own
      const targets = declared.some((p) => p.wildcard)
        ? coded.map((p) => p.raw)
        : declared.map((p) => p.raw);
      for (const target of targets) add(target, file);
    }
  }

  for (const [key, list] of [...groups]) if (!list.length) groups.delete(key);
  return groups;
}

/** Split "2 — Ticketing Sales" / "P04 POS" into a code and a label. */
function splitGroupLabel(key) {
  const match = key.match(/^(P\d+|\d+)\s*(?:[—-]\s*)?(.+)$/);
  return match ? { code: match[1], label: match[2].trim() } : { code: '', label: key };
}

function groupColor(key, files) {
  if (groupBy() === 'contracts') return colorForNode({ group: key, type: 'file' }, 'group');
  const tier = files[0]?.tier ?? files[0]?.group;
  return colorForNode({ group: tier, type: 'file' }, 'group');
}

/** Where a grouping means something narrower than it looks, say so here. */
function renderSideNote() {
  const note = $('side-note');
  note.hidden = true;

  if (state.layer === 'contracts' && groupBy() === 'platforms') {
    const contracts = state.index.nodes.filter((n) => n.type === 'file');
    const declared = contracts.filter((n) => n.platforms?.length).length;
    note.innerHTML =
      `From <b>x-ticvai-platforms</b> (${declared}/${contracts.length} contracts). Declared per ` +
      `contract, so a contract appears under every platform it names — this is reach, not ` +
      `per-endpoint ownership.`;
    note.hidden = false;
  } else if (state.layer === 'frontend') {
    const screens = state.journeys?.screens ?? [];
    const defined = new Set(screens.map((s) => s.platform));
    // the full vocabulary is the deployment table's twelve, not the ones that
    // happen to have screen files today — the gap is the point
    const all = state.journeys?.allPlatforms ?? [];
    const missing = all.filter((p) => !defined.has(p.code));
    note.innerHTML =
      `<b>${screens.length} screens</b> across ${defined.size} platforms` +
      (missing.length
        ? `. ${missing.length} more — ${missing.map((p) => p.code).join(', ')} — have no screen ` +
          `files yet, so they are absent here: a gap in the definitions, not in the product.`
        : `, which is every platform in the deployment table.`);
    note.hidden = false;
  } else if (state.layer === 'domain') {
    const s = state.domain?.stats ?? {};
    if (groupBy() === 'contexts') {
      note.innerHTML =
        `<b>${s.contextEdges} links between ${s.contexts} contexts</b>, every one of them an ` +
        `event. The contracts do not <b>$ref</b> each other at all — all 44 of their file-level ` +
        `links point at <b>shared/</b> — so this is the only place the coupling between bounded ` +
        `contexts is written down.`;
    } else {
      const unmodelled = (s.statusEnums ?? 0) - (s.statusEnumsModelled ?? 0);
      note.innerHTML =
        `<b>${s.machines} state models</b> covering ${s.states} states and ${s.transitions} ` +
        `transitions. The contracts declare <b>${s.statusEnums} status enums</b>` +
        (unmodelled > 0
          ? `; ${unmodelled} of them have no model, so nothing says which of their moves are legal.`
          : `, and every one of them has a model.`);
    }
    note.hidden = false;
  } else if (state.layer === 'backend') {
    const s = state.backend?.stats ?? {};
    if (s.tables) {
      note.innerHTML =
        `<b>${s.inDdl} tables</b> exist as SQL in <b>backend/</b> across ${s.migrationFiles} ` +
        `migrations. The other ${s.tables - s.inDdl} come from the schema reference in ` +
        `<b>${state.backend.file?.split('/')[0]}/</b> — derived from the contracts, not written yet.`;
      note.hidden = false;
    }
  }
}

// ── ER diagram ───────────────────────────────────────────────────────
const METHOD_COLORS = {
  GET: '#60a5fa', POST: '#34d399', PUT: '#fbbf24', DELETE: '#f87171', PATCH: '#c084fc',
};

/** Contracts, for the ER / Flow scope pickers. */
function scopeOptions() {
  return state.index.nodes
    .filter((n) => n.type === 'file')
    .sort((a, b) => a.group.localeCompare(b.group) || a.name.localeCompare(b.name))
    .map((f) => ({ value: f.file, label: `${f.group} / ${f.name}` }));
}

function fillScopeSelect(select, current) {
  select.innerHTML = '';
  for (const option of scopeOptions()) {
    const node = el('option', null, option.label);
    node.value = option.value;
    if (option.value === current) node.selected = true;
    select.append(node);
  }
}

/**
 * Entities are the object-like schemas of one contract, plus any schema they
 * reference from elsewhere (drawn as external, so cross-contract links show).
 */
function buildER(file) {
  const own = state.index.nodes.filter((n) => n.type === 'schema' && n.file === file);
  const included = new Map(own.map((s) => [s.id, s]));

  for (const schema of own) {
    for (const property of schema.properties ?? []) {
      if (!property.refTarget || included.has(property.refTarget)) continue;
      const target = state.nodesById.get(property.refTarget);
      if (target) included.set(target.id, target);
    }
  }

  const nodes = [...included.values()].map((schema) => {
    const external = schema.file !== file;
    const rows = (schema.properties ?? []).map((property) => {
      const target = property.refTarget ? state.nodesById.get(property.refTarget) : null;
      const value = target
        ? `${target.name}${property.isArray ? '[]' : ''}`
        : `${property.type || 'any'}${property.format ? ` (${property.format})` : ''}`;
      return {
        label: `${property.required ? '• ' : ''}${property.name}`,
        value,
        strong: property.required,
        refTarget: property.refTarget,
      };
    });

    // enum-only schemas have no properties — show their values instead
    if (!rows.length && schema.enumValues) {
      for (const value of schema.enumValues.slice(0, 12)) rows.push({ label: value, value: '' });
    }

    return {
      id: schema.id,
      title: schema.name,
      badge: external ? schema.file.split('/').pop().replace(/\.ya?ml$/, '') : `${rows.length}`,
      color: external ? '#fbbf24' : schema.enumValues ? '#c084fc' : '#34d399',
      rows,
      external,
    };
  });

  const edges = [];
  const seen = new Set();
  for (const schema of own) {
    for (const property of schema.properties ?? []) {
      if (!property.refTarget || !included.has(property.refTarget)) continue;
      const key = `${schema.id}|${property.refTarget}`;
      if (seen.has(key)) continue;
      seen.add(key);
      edges.push({
        source: schema.id,
        target: property.refTarget,
        label: `${property.name}${property.isArray ? '[]' : ''}`,
      });
    }
  }

  return { nodes, edges, ownCount: own.length };
}

function renderER({ focus } = {}) {
  const file = state.erScope;
  if (!file) return;

  // The fields these boxes are made of arrive per contract. Drawing named but
  // empty boxes first and filling them a moment later would be worse than
  // waiting: an entity with no fields is a claim, and a wrong one. The hint
  // line says what is happening, because a diagram that is briefly blank with
  // no explanation reads as broken.
  if (!erDetailReady(file)) {
    $('er-hint').textContent = `reading the fields of ${file.split('/').pop()}…`;
    ensureERDetail(file).then(() => {
      // the reader may have moved on while it was in flight
      if (state.erScope === file) renderER({ focus });
    });
    return;
  }

  const { nodes, edges, ownCount } = buildER(file);
  er.setData(nodes, edges);
  er.setSelected(state.selectedId);
  $('er-hint').textContent =
    `${ownCount} entities · ${nodes.length - ownCount} referenced from other contracts · ${edges.length} relationships`;
  renderBoxLegend($('er-legend'), [
    ['#34d399', 'entity in this contract'],
    ['#c084fc', 'enum'],
    ['#fbbf24', 'entity from another contract'],
  ], 'click a field to follow its $ref · drag a box to pin it');
  if (focus) er.onSettle = () => { er.onSettle = null; if (!er.userAdjusted) er.focus(focus, { zoom: 1 }); };
}

// ── Flow diagram ─────────────────────────────────────────────────────
// ── journey ──────────────────────────────────────────────────────────
// A flow is one job a person came to do, traced across screens. Steps run left
// to right; the branches that can derail a step hang underneath it. Everything
// here is declared in flows/ and screens/ — no sequencing is inferred.

async function loadJourneys() {
  if (state.journeys) return state.journeys;
  const res = await fetch('/api/journeys');
  state.journeys = await res.json();
  return state.journeys;
}

/** Find the indexed contract operation behind an operationId, if it exists. */
function operationNodeFor(operationId) {
  for (const node of state.index.nodes) {
    if (node.type === 'operation' && node.name === operationId) return node;
  }
  return null;
}

async function renderJourney() {
  const data = await loadJourneys();
  const body = $('journey-body');
  const select$ = $('journey-scope');

  if (!data.flows.length) {
    body.innerHTML = '';
    body.append(el('p', 'pane-empty', 'No flows found in flows/.'));
    $('journey-hint').textContent = '';
    return;
  }

  if (select$.options.length !== data.flows.length) {
    select$.innerHTML = '';
    for (const flow of data.flows) {
      const option = el('option', null, `${flow.id} — ${flow.name}`);
      option.value = flow.id;
      select$.append(option);
    }
  }
  if (!state.journeyId || !data.flows.some((f) => f.id === state.journeyId)) {
    state.journeyId = data.flows[0].id;
  }
  select$.value = state.journeyId;

  const flow = data.flows.find((f) => f.id === state.journeyId);
  const showBranches = $('journey-branches').checked;
  const showOps = $('journey-ops').checked;

  const s = data.stats;
  $('journey-hint').textContent =
    `${flow.steps.length} steps · ${flow.branches.length} branches · ` +
    `drag to pan · ${s.flows} flows and ${s.screens} screens in all`;

  body.innerHTML = '';

  // ---- header ----------------------------------------------------------
  const head = el('div', 'journey-head');
  // the delivery narrates each flow in a paragraph — who arrives, wanting what
  head.append(deliveryTip(el('h2', 'journey-title', `${flow.id} — ${flow.name}`), 'flows', flow.id));

  const chips = el('div', 'journey-chips');
  const chip = (label, value, cls = '') => {
    const c = el('span', `jchip ${cls}`);
    c.append(el('span', null, label));
    c.append(el('b', null, String(value)));
    return c;
  };
  if (flow.actor) chips.append(chip('actor', flow.actor));
  if (flow.criticality) chips.append(chip('criticality', flow.criticality, flow.criticality));
  if (flow.frequency) chips.append(chip('frequency', flow.frequency));
  if (flow.wave) chips.append(chip('wave', flow.wave));
  if (flow.capability) chips.append(chip('capability', flow.capability));
  for (const platform of flow.platforms) chips.append(chip('platform', platform));
  head.append(chips);

  if (flow.trigger?.description || flow.offlineBehaviour) {
    const trigger = el('div', 'journey-trigger');
    if (flow.trigger?.description) {
      trigger.append(el('b', null, 'Trigger: '));
      trigger.append(document.createTextNode(flow.trigger.description));
    }
    if (flow.offlineBehaviour) {
      trigger.append(el('br'));
      trigger.append(el('b', null, 'Offline: '));
      trigger.append(document.createTextNode(flow.offlineBehaviour));
    }
    head.append(trigger);
  }
  body.append(head);

  // ---- the step track --------------------------------------------------
  const track = el('div', 'journey-track');

  flow.steps.forEach((step, i) => {
    if (i > 0) track.append(el('div', 'journey-arrow', '→'));

    const column = el('div', 'journey-col');
    const card = el('div', 'step-card');

    const top = el('div', 'step-top');
    top.append(el('span', 'step-num', String(step.step)));
    top.append(el('span', 'step-screen', step.screenId ?? '—'));
    if (step.platform) top.append(el('span', 'step-platform', step.platform));
    card.append(top);

    if (step.screenName) card.append(el('div', 'step-screen-name', step.screenName));
    if (step.action) card.append(el('div', 'step-action', step.action));

    if (showOps && step.operations.length) {
      const ops = el('div', 'step-ops');
      for (const op of step.operations) {
        const row = el('div', `step-op${op.known ? '' : ' unknown'}`);
        row.append(el('span', 'step-op-dot'));
        row.append(el('span', null, op.operationId));
        row.title = op.known
          ? `Open ${op.operationId} in the contracts`
          : `${op.operationId} is not declared by any contract`;
        row.onclick = (e) => {
          e.stopPropagation();
          const node = operationNodeFor(op.operationId);
          if (node) { select(node.id); setMode('reader'); }
          else toast(`${op.operationId} is not in the contracts`);
        };
        ops.append(row);
      }
      card.append(ops);
    }

    if (step.outcome) card.append(el('div', 'step-outcome', step.outcome));
    if (step.duration) card.append(el('span', 'step-duration', step.duration));

    // clicking the card opens the first operation the step calls
    card.onclick = () => {
      const first = step.operations[0];
      const node = first ? operationNodeFor(first.operationId) : null;
      if (node) { select(node.id); setMode('reader'); }
    };
    column.append(card);

    // branches that can happen at this step
    const atStep = flow.branches.filter((b) => b.at === step.step);
    if (showBranches && atStep.length) {
      column.append(el('div', 'journey-section-label', `${atStep.length} branch${atStep.length === 1 ? '' : 'es'}`));
      for (const branch of atStep) {
        const bc = el('div', `branch-card ${branch.severity ?? ''}`);
        bc.append(el('div', 'branch-cond', branch.condition));
        if (branch.behaviour) bc.append(el('div', 'branch-behaviour', branch.behaviour));
        if (branch.severity) bc.append(el('span', 'branch-sev', branch.severity));
        if (branch.resolvedBy) bc.append(el('div', 'branch-resolved', `resolved by ${branch.resolvedBy}`));
        column.append(bc);
      }
    }

    track.append(column);
  });

  // ---- exit states -----------------------------------------------------
  if (flow.exitStates.length) {
    track.append(el('div', 'journey-arrow', '→'));
    const exits = el('div', 'journey-exits');
    exits.append(el('div', 'journey-section-label', 'exit states'));
    for (const exit of flow.exitStates) {
      const card = el('div', `exit-card ${exit.state}`);
      card.append(el('div', 'exit-state', exit.state));
      card.append(el('div', 'exit-desc', exit.description));
      exits.append(card);
    }
    track.append(exits);
  }
  body.append(track);

  // branches whose step number does not match any step would otherwise vanish
  const orphanBranches = flow.branches.filter(
    (b) => !flow.steps.some((s) => s.step === b.at)
  );
  if (showBranches && orphanBranches.length) {
    const box = el('div', 'journey-questions');
    box.append(el('b', null, `${orphanBranches.length} branch(es) reference a step that does not exist: `));
    box.append(document.createTextNode(orphanBranches.map((b) => `step ${b.at} — ${b.condition}`).join('; ')));
    body.append(box);
  }

  // ---- the design boards for the platforms this flow runs on -----------
  // A flow names its platforms as "P01 Guest Web Storefront"; a board knows
  // its code, so match on the code rather than the whole label.
  const codes = new Set(
    flow.platforms
      .map((p) => /\bP\d{2}\b/.exec(String(p))?.[0])
      .concat(flow.steps.map((s) => s.platform))
      .filter(Boolean)
  );
  // This journey drawn end to end. The flat flow-fNN.html renders are generated
  // from the step list and say nothing the step list above does not; the boards
  // hold the drawn screens, so the journey is better told by walking its own
  // steps and showing each screen's frame in order.
  body.append(journeyFrames(flow));

  const flowBoards = currentOnly(boards().filter((b) => codes.has(b.platform)));
  body.append(
    boardSection(flowBoards, {
      label: 'design board · this journey’s platform',
      height: 460,
    })
  );

  if (flow.openQuestions.length) {
    const box = el('div', 'journey-questions');
    box.append(el('b', null, 'Open questions'));
    const list = el('ul');
    for (const question of flow.openQuestions) list.append(el('li', null, question));
    box.append(list);
    body.append(box);
  }
}

// ── frontend: the design boards ──────────────────────────────────────
// The exported UI/UX boards in UIUX_html/, framed live rather than as a
// screenshot — they are working HTML, so scrolling and hovering them works.
//
// Which platform a board belongs to is inferred from its file name, so every
// place one is shown says so. See lib/boards.mjs.

const boards = () => state.journeys?.boards ?? [];

/**
 * An earlier revision of a board that is also here is history, not a second
 * design — `Park POS v1` is not another board beside `Park POS`.
 */
function currentOnly(list) {
  const current = new Set(list.filter((b) => !b.revision).map((b) => b.name));
  return list.filter((b) => !b.revision || !current.has(b.name));
}

/**
 * The board to show beside a screen or a journey. A board a screen names
 * outright wins; failing that, the ones matched to its platform.
 */
function boardsFor({ platform = null, screenId = null } = {}) {
  const declared = screenId ? boards().filter((b) => b.screens.includes(screenId)) : [];
  if (declared.length) return declared;
  return currentOnly(boards().filter((b) => platform && b.platform === platform));
}

const formatBytes = (n) => (n > 1024 * 1024 ? `${(n / 1048576).toFixed(1)} MB` : `${Math.round(n / 1024)} KB`);

/**
 * One board, framed. The boards are laid out for a full desktop window, so the
 * frame renders at that size and is scaled down to whatever room it has —
 * shrinking the viewport instead would trigger their own responsive rules and
 * show a layout nobody designed.
 */
/**
 * An exported HTML page framed and scaled to whatever width it is given.
 *
 * Both the design boards and the wireframes are self-contained pages authored
 * at a fixed width, so the only honest way to show one inside a card is to
 * render it at its own width and scale the whole frame down. Zooming the page
 * instead would reflow it, and a reflowed wireframe is not the wireframe.
 */
/**
 * A screen, followed all the way down: operations, the services behind them,
 * and the tables those services actually touch.
 *
 * The screen already lists its operations, and that is where the trail stopped —
 * an operation is a name, and a name does not tell you that this screen writes
 * to the ledger. `handoff/screen-index.json` carries the whole chain
 * pre-computed, so this is the frontend end of the same join the Lineage view
 * shows from the contracts end.
 *
 * A screen naming no operation gets the honest version rather than an empty
 * block: 192 of the 347 are in that state, and it is the most useful thing this
 * page can tell you about them.
 */
function screenReach(screen) {
  const box = document.createDocumentFragment();
  const entry = state.lineage?.screens?.find((s) => s.id === screen.id);
  if (!entry) return box;

  if (!entry.operations.length) {
    box.append(el('div', 'journey-section-label', 'reaches'));
    box.append(
      el('p', 'pane-note board-empty',
        `This screen names no operation, so it reaches nothing. It can be drawn and it cannot be ` +
        `built — and 192 of the 347 screens are in the same position.`)
    );
    return box;
  }

  const tables = [...new Set([...entry.writes, ...entry.reads])];
  box.append(
    el('div', 'journey-section-label',
      `reaches · ${entry.services.length} service${entry.services.length === 1 ? '' : 's'} · ` +
      `${tables.length} table${tables.length === 1 ? '' : 's'}`)
  );

  const card = el('div', 'reach-card');
  const line = (label, nodes, note) => {
    if (!nodes.length) return;
    const row = el('div', 'reach-row');
    const key = el('span', 'reach-label', label);
    if (note) tip(key, label, note);
    row.append(key);
    const values = el('span', 'reach-values');
    for (const node of nodes) values.append(node);
    row.append(values);
    card.append(row);
  };

  line('services', entry.services.map((name) => {
    const chip = el('span', 'lineage-service', name);
    const ops = state.lineage?.operations?.filter((o) => o.service === name) ?? [];
    tip(chip, name, `Owns ${ops.length} of the 654 operations.`);
    return chip;
  }), 'The service that runs the operations this screen calls. 22 across the platform.');

  line('writes', entry.writes.map((t) => tableChip(t, { write: true })),
    'Tables this screen causes to change. The ones that make it a risk to get wrong.');
  line('reads', entry.reads.filter((t) => !entry.writes.includes(t)).map((t) => tableChip(t)),
    'Tables it reads and does not change.');
  line('stored procedures', entry.storedProcedures.map((p) => {
    const chip = el('span', 'lineage-procedure', p);
    tip(chip, 'Stored procedure',
      'This screen drives one of the few operations that runs as a stored procedure rather than in a service.');
    return chip;
  }), 'Eight operations in the platform run as a stored procedure. This screen calls one.');

  // Which of the screen's operations contributed nothing to that table list.
  //
  // The count above is a union of what the lineage resolved, and it was stated
  // as if it were the whole truth. On the Home Landing it said "1 table" while
  // two of the three operations behind it — listProducts among them — carry no
  // reads or writes at all, which is plainly not a claim that the product list
  // touches no table. A number that is right about the data and wrong about the
  // system has to say which it is.
  // Two different reasons an operation adds nothing, and they are not the same
  // claim. `unresolved` means the lineage was never filled in for it — a gap in
  // the delivery. Anything else means the lineage did look and found no table,
  // which is a real answer: the operation returns a computed projection.
  const unresolved = [];
  const projection = [];
  for (const name of entry.operations) {
    const op = state.lineage?.operations?.find((o) => o.name === name);
    if (op && (op.reads?.length ?? 0) + (op.writes?.length ?? 0) > 0) continue;
    (!op || op.source === 'unresolved' ? unresolved : projection).push(name);
  }

  if (unresolved.length) {
    const row = el('div', 'reach-row');
    row.append(el('span', 'reach-label warn', 'not resolved'));
    const values = el('span', 'reach-values');
    for (const name of unresolved) {
      const chip = el('button', 'lineage-table unknown', name);
      tip(chip, name,
        'The lineage carries no reads or writes for this operation, so whatever it touches is not ' +
        'counted above. 318 of the 654 operations are in that state.');
      chip.onclick = () => openOperation(name);
      values.append(chip);
    }
    row.append(values);
    card.append(row);
  }

  box.append(card);

  if (unresolved.length) {
    box.append(
      el('p', 'pane-note warn-note',
        `${unresolved.length} of the ${entry.operations.length} operation` +
        `${entry.operations.length === 1 ? '' : 's'} this screen calls ` +
        `${unresolved.length === 1 ? 'has' : 'have'} no lineage at all, so ` +
        `${tables.length
          ? `${tables.length} is a floor and not a total`
          : 'no table could be counted'}. ` +
        'That is a gap in handoff/api-data-lineage.json rather than a fact about this screen.')
    );
  } else if (!tables.length) {
    box.append(
      el('p', 'pane-note',
        `It calls ${projection.join(', ')}, and the lineage resolved every one of them to no table — ` +
        `usually because the operation returns a computed projection rather than reading one.`)
    );
  }

  box.append(
    el('p', 'pane-note',
      'From handoff/screen-index.json — the same chain the Lineage view shows from the contracts end.')
  );
  return box;
}

function frameStage(url, { height = 420, design = 1440, title = 'preview', kind = 'board' } = {}) {
  const stage = el('div', `board-stage ${kind}-stage`);
  stage.style.height = `${height}px`;

  const frame = document.createElement('iframe');
  // both kinds share the scaling and the frame styling, but a wireframe and an
  // exported design board are different claims and have to be distinguishable
  frame.className = `board-frame ${kind}-frame`;
  frame.src = url;
  frame.loading = 'lazy';
  frame.setAttribute('title', title);
  // local, static and trusted, but nothing here needs to navigate the viewer
  frame.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-popups');
  frame.style.width = `${design}px`;
  stage.append(frame);

  // A board is authored for a 1240–1440px window. Following the container all
  // the way down puts it at 0.27 on a 390px phone, which is not a small
  // preview but an unreadable one — and it costs the same full page load to
  // render. So the scale has a floor. Below it the board stops shrinking and
  // the stage scrolls sideways instead, which at least admits there is more
  // board than screen, and the card's "Open full size" link is promoted to a
  // button at the same width, because reading one properly is what a whole tab
  // is for. 0.42 is where the boards' 12–14px body text stops being a texture.
  const MIN_SCALE = 0.42;

  const fit = () => {
    const width = stage.clientWidth;
    if (!width) return;
    const scale = Math.max(width / design, MIN_SCALE);
    const frameHeight = Math.round(height / scale);
    frame.style.height = `${frameHeight}px`;
    frame.style.transform = `scale(${scale})`;
    // a transform does not shrink the box the layout reserves, so the stage
    // would report 1440px of scroll however far the frame is scaled down.
    // Pull the reserved box back to what is actually drawn.
    frame.style.marginRight = `${Math.floor(-design * (1 - scale))}px`;
    frame.style.marginBottom = `${Math.floor(-frameHeight * (1 - scale))}px`;
  };
  // the card is built before it is in the document, so measure on the next frame
  requestAnimationFrame(fit);
  if (window.ResizeObserver) new ResizeObserver(fit).observe(stage);
  return stage;
}

function boardCard(board, { height = 420, design = 1440 } = {}) {
  const card = el('div', 'board-card');

  const head = el('div', 'board-head');
  const title = el('div', 'board-title');
  title.append(el('b', null, board.name));
  if (board.revision) title.append(el('span', 'board-rev', board.revision));
  head.append(title);

  const meta = el('div', 'board-meta');
  if (board.platform) {
    const chip = el('span', `board-platform${board.inferred ? ' inferred' : ''}`);
    chip.textContent = `${board.platform} ${board.platformName}`;
    chip.title = board.inferred
      ? `Matched by ${board.matchedBy} — inferred from the file name, not declared anywhere.`
      : `Matched by ${board.matchedBy}.`;
    meta.append(chip);
  }
  meta.append(el('span', 'board-size', formatBytes(board.bytes)));
  const open = el('a', 'board-open', 'Open full size ↗');
  open.href = board.url;
  open.target = '_blank';
  open.rel = 'noopener';
  meta.append(open);
  head.append(meta);
  card.append(head);

  card.append(frameStage(board.url, { height, design, title: `${board.name} design board` }));

  if (board.inferred) {
    card.append(
      el('p', 'board-note',
        `Attached to ${board.platform} by ${board.matchedBy} — inferred from the file name. ` +
        `Nothing declares which platform a board is for.`)
    );
  }
  return card;
}

// ── wireframes ───────────────────────────────────────────────────────
// One rendered wireframe per screen, flow and platform, in `wireframes/`.
//
// These are attached by name — `screens/acc-001.html` is screen ACC-001, full
// stop — where a design board has to be matched to a platform by reading its
// file name and hoping. So there is no "inferred" caveat here and none is
// shown: 180 of 180 screens have one.

const wireframes = () => state.journeys?.wireframes ?? null;
const wireframeFor = (kind, id) => (id ? wireframes()?.[kind]?.[id] ?? null : null);

/**
 * @param entry  one wireframes.screens / .flows / .platforms record
 * @param label  what it draws, said plainly — this is the only caption
 */
function wireframeSection(entry, { label = 'wireframe', height = 520, design = 1240, empty = null, name = null } = {}) {
  const box = document.createDocumentFragment();
  if (!entry || (!entry.file && !entry.board)) {
    if (empty) {
      box.append(el('div', 'journey-section-label', label));
      box.append(el('p', 'pane-note board-empty', empty));
    }
    return box;
  }

  // Two drawings can exist for one screen and they are not equal. The board
  // frame is the drawn one — the platform board is 347 screens of design intent,
  // with real field names, states and deny reasons read off the package. The
  // standalone file is a structure-only render generated from the screen
  // definition, and says so itself: "Nothing here is a design decision."
  //
  // So the board wins when there is one, and the generated one is offered
  // underneath rather than dropped, because it is the thing that stays in step
  // with the definition automatically.
  const board = entry.board?.frameUrl ? entry.board : null;
  const primary = board
    ? {
        url: board.frameUrl,
        openUrl: board.url,
        // the board's own <title> names the whole board, so it is the wrong
        // caption for one frame out of it — the subject names itself
        title: name ?? entry.title ?? board.anchor?.toUpperCase() ?? label,
        source: board.file.split('/').pop(),
        anchor: board.anchor,
        chip: board.anchor ? 'from the platform board' : 'the platform board',
        why: board.anchor
          ? `${board.file}#${board.anchor} — this screen's frame, lifted out of the board it is ` +
            `drawn on. The link is declared by the screen itself, not matched by file name.`
          : `${board.file} — every screen on this platform, drawn, in one file. The platform ` +
            `declares this board itself, so nothing is matched by guessing.`,
        bytes: null,
      }
    : {
        url: entry.url,
        openUrl: entry.url,
        title: entry.title ?? entry.file.split('/').pop(),
        source: entry.file,
        chip: 'named for what it draws',
        why:
          `${entry.file} — matched by file name, so nothing here is inferred. Structure only: ` +
          `generated from the screen definition, so it carries no design decision.`,
        bytes: entry.bytes,
      };

  box.append(el('div', 'journey-section-label', label));
  const card = el('div', 'board-card wireframe-card');

  const head = el('div', 'board-head');
  const title = el('div', 'board-title');
  title.append(el('b', null, primary.title));
  head.append(title);

  const meta = el('div', 'board-meta');
  const declared = el('span', `board-platform${board ? ' from-board' : ''}`);
  declared.textContent = primary.chip;
  declared.title = primary.why;
  tip(declared, board ? 'From the platform board' : 'Generated from the definition', primary.why);
  meta.append(declared);
  if (primary.bytes) meta.append(el('span', 'board-size', formatBytes(primary.bytes)));
  const open = el('a', 'board-open', board ? 'Open the board ↗' : 'Open full size ↗');
  open.href = primary.openUrl;
  open.target = '_blank';
  open.rel = 'noopener';
  meta.append(open);
  head.append(meta);
  card.append(head);

  card.append(
    frameStage(primary.url, { height, design, title: primary.title, kind: 'wireframe' })
  );
  box.append(card);

  // the generated render, folded away — same screen, different claim
  if (board && entry.file) {
    const extra = el('details', 'wireframe-alt');
    const summary = el('summary', null, 'also: the structure-only render generated from the definition');
    tip(summary, 'The other drawing',
      `\`${entry.file}\` is generated from the screen definition — template, regions and component ` +
      `kinds. It stays in step with the definition automatically, and states outright that nothing ` +
      `in it is a design decision. The board above is the drawn one.`);
    extra.append(summary);
    extra.append(frameStage(entry.url, { height: 420, design, title: entry.title ?? label, kind: 'wireframe' }));
    box.append(extra);
  }
  return box;
}

/**
 * A journey as the screens it visits, in order, each lifted out of its board.
 *
 * The alternative is `wireframes/flow-f01.html`, which is generated from the
 * same step list this page has already drawn above — so it repeats the page
 * rather than adding to it. These are the drawn screens.
 */
function journeyFrames(flow) {
  const box = document.createDocumentFragment();
  const steps = flow.steps.filter((s) => s.screenId);
  const drawn = steps
    .map((step) => ({ step, entry: wireframeFor('screens', step.screenId) }))
    .filter((s) => s.entry?.board?.frameUrl);

  if (!drawn.length) {
    const fallback = wireframeFor('flows', flow.id);
    return wireframeSection(fallback, {
      label: 'wireframe · this journey, screen by screen',
      height: 620,
      name: `${flow.id} — ${flow.name}`,
      empty: `No screen on this journey resolves to a board frame.`,
    });
  }

  box.append(
    el('div', 'journey-section-label',
      `drawn · ${drawn.length} of ${steps.length} steps, each screen lifted from its platform board`)
  );

  const strip = el('div', 'journey-frames');
  for (const { step, entry } of drawn) {
    const card = el('div', 'journey-frame-card');
    const head = el('div', 'journey-frame-head');
    head.append(el('span', 'journey-frame-step', String(step.step)));
    const name = el('button', 'journey-frame-name', `${step.screenId} ${step.screenName ?? ''}`.trim());
    name.onclick = () => { state.screenId = step.screenId; setMode('screen'); };
    head.append(name);
    if (step.platform) {
      head.append(deliveryTip(el('span', 'journey-frame-platform', step.platform), 'platforms', step.platform));
    }
    card.append(head);
    if (step.action) card.append(el('div', 'journey-frame-action', step.action));
    card.append(
      frameStage(entry.board.frameUrl, {
        height: 460, design: 1240, title: step.screenName ?? step.screenId, kind: 'wireframe',
      })
    );
    strip.append(card);
  }
  box.append(strip);

  const skipped = steps.length - drawn.length;
  if (skipped) {
    box.append(
      el('p', 'pane-note board-empty',
        `${skipped} step${skipped > 1 ? 's are' : ' is'} not shown: the screen has no board frame declared.`)
    );
  }
  return box;
}

/** The "design board" block used by the screen, journey and apps views. */
function boardSection(list, { label = 'design board', height = 420, empty = null } = {}) {
  const box = document.createDocumentFragment();
  if (!list.length) {
    if (empty) {
      box.append(el('div', 'journey-section-label', label));
      box.append(el('p', 'pane-note board-empty', empty));
    }
    return box;
  }
  box.append(
    el('div', 'journey-section-label', `${label}${list.length > 1 ? ` · ${list.length}` : ''}`)
  );
  for (const board of list) box.append(boardCard(board, { height }));
  return box;
}

function selectBoard(id, { open = true } = {}) {
  state.boardId = id;
  state.screenId = null;
  if (state.layer !== 'frontend' && open) { setLayer('frontend'); setMode('screen'); return; }
  markTreeSelection();
  if (state.mode === 'screen') renderScreen();
  else if (open) setMode('screen');
}

/** A board on its own page, for a platform that has no screen definitions. */
function renderBoardPage(board) {
  const body = $('screen-body');
  body.innerHTML = '';
  $('screen-hint').textContent =
    `design board · ${formatBytes(board.bytes)} · ${board.file}`;

  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', board.name + (board.revision ? ` ${board.revision}` : '')));

  const chips = el('div', 'journey-chips');
  const chip = (label, value, cls = '') => {
    const c = el('span', `jchip ${cls}`);
    c.append(el('span', null, label));
    c.append(el('b', null, String(value)));
    return c;
  };
  if (board.platform) chips.append(chip('platform', `${board.platform} ${board.platformName}`));
  if (board.platformApp) chips.append(chip('app', board.platformApp));
  if (board.revision) chips.append(chip('revision', board.revision));
  chips.append(chip('source', board.dir ?? 'designs'));
  if (board.screens.length) chips.append(chip('drawn into', `${board.screens.length} screens`));
  head.append(chips);
  body.append(head);

  const screens = board.platform
    ? (state.journeys?.screens ?? []).filter((s) => s.platform === board.platform)
    : [];

  head.append(
    el('div', 'journey-trigger',
      screens.length
        ? `The design board for ${board.platformName}. That platform has ${screens.length} ` +
          `screen definitions — the board is how it looks, the screen files are what it does.`
        : `The design board for ${board.platformName ?? 'an unmatched platform'}. That platform ` +
          `has no screen definitions yet, so this board is the only description of it. ` +
          `The frontend plan was built from boards like this one.`)
  );

  body.append(boardCard(board, { height: 620 }));

  if (screens.length) {
    body.append(el('div', 'journey-section-label', `screens on ${board.platform}`));
    const row = el('div', 'nav-row');
    for (const screen of screens) {
      const pill = el('button', 'nav-pill', `${screen.id} ${screen.name}`);
      pill.onclick = () => selectScreen(screen.id);
      row.append(pill);
    }
    body.append(row);
  }

  body.append(auth.verdictBlock('board', board.id, board.name, { layer: 'frontend' }));

  const others = boards().filter((b) => b.id !== board.id);
  if (others.length) {
    body.append(el('div', 'journey-section-label', 'other boards'));
    const row = el('div', 'nav-row');
    for (const other of others) {
      const pill = el('button', 'nav-pill', other.name + (other.revision ? ` ${other.revision}` : ''));
      pill.onclick = () => selectBoard(other.id);
      row.append(pill);
    }
    body.append(row);
  }

  markTreeSelection();
}

// ── frontend: one screen ─────────────────────────────────────────────
// The schematic a wireframe implements: which regions exist, what sits in each,
// what happens when the data is missing, and which operations fill it.

function screenById(id) {
  return (state.journeys?.screens ?? []).find((s) => s.id === id) ?? null;
}

function selectScreen(id, { open = true } = {}) {
  state.screenId = id;
  state.boardId = null;
  if (state.layer !== 'frontend' && open) { setLayer('frontend'); setMode('screen'); return; }
  markTreeSelection();
  if (state.mode === 'screen') renderScreen();
  else if (open) setMode('screen');
  renderSidePane();
}

const STATE_NOTE = {
  loading: 'while the data is on its way',
  empty: 'when there is nothing to show',
  error: 'when the call fails',
  offline: 'with no connection',
  denied: 'without the permission',
};

function renderScreen() {
  const body = $('screen-body');
  const picker = $('screen-scope');
  const screens = state.journeys?.screens ?? [];

  if (!screens.length) {
    body.innerHTML = '';
    body.append(el('p', 'pane-empty', 'No screens found in screens/.'));
    $('screen-hint').textContent = '';
    return;
  }

  // the picker carries the design boards too, so a platform with no screen
  // definitions is still reachable from the screens page
  const wanted = screens.length + boards().length;
  if (picker.options.length !== wanted) {
    picker.innerHTML = '';
    const screenGroup = boards().length ? el('optgroup') : picker;
    if (screenGroup !== picker) {
      screenGroup.label = 'Screens';
      picker.append(screenGroup);
    }
    for (const s of screens) {
      const option = el('option', null, `${s.id} — ${s.name}`);
      option.value = `screen:${s.id}`;
      screenGroup.append(option);
    }
    if (boards().length) {
      const group = el('optgroup');
      group.label = 'Design boards';
      for (const b of boards()) {
        const option = el('option', null,
          `${b.platform ?? '—'} ${b.name}${b.revision ? ` ${b.revision}` : ''}`);
        option.value = `board:${b.id}`;
        group.append(option);
      }
      picker.append(group);
    }
  }

  // ---- a board opened in place of a screen ------------------------------
  const board = state.boardId ? boards().find((b) => b.id === state.boardId) : null;
  if (board) {
    picker.value = `board:${board.id}`;
    renderBoardPage(board);
    renderSidePane();
    return;
  }

  if (!state.screenId || !screens.some((s) => s.id === state.screenId)) state.screenId = screens[0].id;
  picker.value = `screen:${state.screenId}`;

  const screen = screenById(state.screenId);
  const showNotes = $('screen-notes').checked;
  const components = screen.regions.reduce((a, r) => a + r.components.length, 0);
  $('screen-hint').textContent =
    `${screens.length} screens · this one: ${screen.regions.length} regions · ` +
    `${components} components · ${screen.apis.length} operations`;

  body.innerHTML = '';

  // ---- header ----------------------------------------------------------
  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', `${screen.id} — ${screen.name}`));
  if (screen.platform) {
    head.dataset.platform = screen.platform;
    deliveryTip(head.lastChild, 'platforms', screen.platform);
  }

  const chips = el('div', 'journey-chips');
  const chip = (label, value, cls = '') => {
    const c = el('span', `jchip ${cls}`);
    c.append(el('span', null, label));
    c.append(el('b', null, String(value)));
    return c;
  };
  if (screen.platform) chips.append(chip('platform', `${screen.platform} ${screen.platformName ?? ''}`.trim()));
  if (screen.module) chips.append(chip('module', screen.module));
  if (screen.template) chips.append(chip('template', screen.template));
  if (screen.wave) chips.append(chip('wave', screen.wave));
  if (screen.capability) chips.append(chip('capability', screen.capability));
  if (screen.permission) chips.append(chip('permission', screen.permission, 'critical'));
  if (screen.wireframe?.status) chips.append(chip('wireframe', screen.wireframe.status));
  head.append(chips);

  if (screen.purpose) head.append(el('div', 'journey-trigger', screen.purpose));
  body.append(head);

  // ---- the layout board ------------------------------------------------
  if (screen.regions.length) {
    body.append(el('div', 'journey-section-label', 'layout'));
    const board = el('div', 'screen-board');
    for (const region of screen.regions) {
      const card = el('div', 'region-card');
      const top = el('div', 'region-head');
      top.append(el('span', 'region-name', region.name));
      // a region is a slot the template exposes; the library says what each one
      // is for, and until now that was only readable by opening the YAML
      if (region.ref) top.append(vocabularyTip(el('span', 'region-ref', region.ref), region.ref));
      top.append(
        tip(el('span', 'region-count', String(region.components.length)),
          'Components in this region',
          'A screen places components into a region; it does not position them. The template decides that.')
      );
      card.append(top);

      for (const component of region.components) {
        const item = el('div', 'component-row');
        item.append(vocabularyTip(el('span', 'component-kind', component.kind), component.kind));
        if (component.label) item.append(el('span', 'component-label', component.label));
        if (component.bindsTo) {
          item.append(
            tip(el('code', 'component-binds', component.bindsTo),
              'Binds to',
              `This control reads or writes \`${component.bindsTo}\`. The binding is what makes a ` +
              `screen traceable to the API — change the field and this is what breaks.`)
          );
        }
        if (component.permission) {
          item.append(permissionTip(el('span', 'component-perm', component.permission), component.permission));
        }
        if (showNotes && component.notes) item.append(el('div', 'component-notes', component.notes));
        card.append(item);
      }
      if (!region.components.length) card.append(el('div', 'component-notes', 'no components declared'));
      board.append(card);
    }
    body.append(board);
  } else {
    body.append(el('div', 'journey-questions', 'No layout declared — this screen carries structure only.'));
  }

  // ---- the four states -------------------------------------------------
  const order = ['loading', 'empty', 'error', 'offline', 'denied'];
  const required = screen.offlineCapable ? ['loading', 'empty', 'error', 'offline'] : ['loading', 'empty', 'error'];
  body.append(el('div', 'journey-section-label', 'states'));
  const states = el('div', 'state-grid');
  for (const key of order) {
    const value = screen.states?.[key];
    if (!value && !required.includes(key)) continue;
    const card = el('div', `state-card ${key}${value ? '' : ' missing'}`);
    const top = el('div', 'state-head');
    top.append(tipFor(el('span', 'state-name', key), key));
    top.append(el('span', 'state-when', STATE_NOTE[key]));
    card.append(top);
    card.append(el('div', 'state-desc', value ?? 'not declared'));
    states.append(card);
  }
  body.append(states);

  // ---- operations ------------------------------------------------------
  if (screen.apis.length) {
    body.append(el('div', 'journey-section-label', `operations · ${screen.apis.length}`));
    const list = el('div', 'api-list');
    for (const api of screen.apis) {
      const node = operationNodeFor(api.operationId);
      const row = el('div', `api-row${node ? '' : ' unknown'}`);
      if (api.trigger) {
        row.append(tipFor(el('span', `api-trigger ${api.trigger}`, api.trigger), api.trigger));
      }
      if (node) row.append(el('span', `method ${node.method}`, node.method));
      row.append(el('span', 'api-id', api.operationId));
      if (api.purpose) row.append(el('span', 'api-purpose', api.purpose));
      row.append(el('span', 'api-contract', node ? node.file.split('/').pop().replace(/\.ya?ml$/, '') : 'not in contracts'));
      row.onclick = () => {
        if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
        else toast(`${api.operationId} is not declared by any contract`);
      };
      list.append(row);
    }
    body.append(list);
  }

  // ---- what this screen reaches ----------------------------------------
  body.append(screenReach(screen));

  // ---- navigation ------------------------------------------------------
  const entryFrom = screen.navigation?.entryFrom ?? [];
  const exitTo = screen.navigation?.exitTo ?? [];
  if (entryFrom.length || exitTo.length || screen.navigation?.isEntryPoint) {
    const inferred = screen.navigationInferred;
    body.append(el('div', 'journey-section-label',
      inferred ? 'navigation · inferred' : 'navigation · declared'));
    const nav = el('div', 'nav-row');
    const side = (label, ids) => {
      const box = el('div', 'nav-side');
      box.append(el('div', 'nav-label', label));
      if (!ids.length) box.append(el('span', 'nav-none', '—'));
      for (const id of ids) {
        const target = screenById(id);
        const pill = el(
          'button',
          `nav-pill${target ? '' : ' unknown'}${inferred ? ' inferred' : ''}`,
          target ? `${id} ${target.name}` : id
        );
        pill.onclick = () => (target ? selectScreen(id) : toast(`${id} is not defined`));
        box.append(pill);
      }
      return box;
    };
    nav.append(side(screen.navigation?.isEntryPoint ? 'entry point · from' : 'from', entryFrom));
    nav.append(side('to', exitTo));
    body.append(nav);
    if (inferred) {
      body.append(el('p', 'pane-note nav-note',
        'This screen carries navigation: inferred — the routes were derived from the module ' +
        'and flow order, not drawn by anyone. Treat them as a starting point for the sitemap.'));
    }
  }

  // ---- deployment ------------------------------------------------------
  if (screen.deployment) {
    body.append(el('div', 'journey-section-label', 'deployment · whole platform'));
    const grid = el('div', 'deploy-grid');
    const LABELS = {
      target: 'runs on',
      distribution: 'ships by',
      hosting: 'hosted',
      bundleUpdate: 'updates',
      releaseCadence: 'cadence',
      networkAssumption: 'network',
      deviceOwnership: 'device',
      storeReview: 'store review',
    };
    for (const [key, label] of Object.entries(LABELS)) {
      const value = screen.deployment[key];
      if (value == null || value === '') continue;
      const cell = el('div', 'deploy-cell');
      cell.append(el('div', 'deploy-label', label));
      cell.append(el('div', 'deploy-value', String(value)));
      // store review turns a fix into a release, so it earns a colour
      if (key === 'storeReview' && value === true) cell.classList.add('warn');
      grid.append(cell);
    }
    body.append(grid);
  }

  // ---- the wireframe ---------------------------------------------------
  // This screen's own drawing, matched by id rather than guessed at.
  body.append(
    wireframeSection(wireframeFor('screens', screen.id), {
      label: 'wireframe',
      height: 560,
      name: `${screen.id} — ${screen.name}`,
      empty:
        `Nothing draws ${screen.id}: no wireframes/screens/${screen.id.toLowerCase()}.html, and no ` +
        `board frame declared on the screen.`,
    })
  );

  // ---- the design board ------------------------------------------------
  // The wireframe status says how far the design got; this is the design.
  body.append(
    boardSection(boardsFor({ platform: screen.platform, screenId: screen.id }), {
      label: 'design board · the exported artboard this platform was drawn from',
      height: 460,
    })
  );

  // ---- implementation --------------------------------------------------
  if (screen.implementation) {
    body.append(el('div', 'journey-section-label', 'implementation'));
    const impl = el('div', 'impl-card');
    const line = (label, value) => {
      if (!value) return;
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', label));
      row.append(el('code', null, String(value)));
      impl.append(row);
    };
    line('app', screen.implementation.app);
    line('route', screen.implementation.route);
    line('component', screen.implementation.component);
    line('status', screen.implementation.status);
    body.append(impl);
  }

  if (screen.openQuestions.length) {
    const box = el('div', 'journey-questions');
    box.append(el('b', null, 'Open questions'));
    const list = el('ul');
    for (const question of screen.openQuestions) list.append(el('li', null, question));
    box.append(list);
    body.append(box);
  }
  if (screen.notes) body.append(el('div', 'journey-questions', screen.notes));

  body.append(auth.verdictBlock('screen', screen.id, `${screen.id} ${screen.name}`, { layer: 'frontend' }));

  markTreeSelection();
  renderSidePane();
}

// ── frontend: the apps ───────────────────────────────────────────────
function renderApps() {
  const body = $('apps-body');
  const apps = state.journeys?.apps ?? [];
  body.innerHTML = '';

  if (!apps.length) {
    body.append(el('p', 'pane-empty', 'No app manifests in frontend/.'));
    $('apps-hint').textContent = '';
    return;
  }

  const scaffolded = apps.filter((a) => a.status === 'scaffolded');
  const screens = apps.reduce((a, x) => a + x.screenCount, 0);
  $('apps-hint').textContent =
    `${apps.length} apps · ${scaffolded.length} scaffolded · ${screens} screens assigned`;

  const grid = el('div', 'app-grid');
  for (const app of apps) {
    const built = app.status === 'scaffolded';
    const card = el('div', `app-card${built ? '' : ' pending'}`);

    const top = el('div', 'app-head');
    top.append(el('span', 'app-name', app.app));
    top.append(el('span', `app-status ${built ? 'ok' : 'warn'}`, app.status ?? 'unknown'));
    card.append(top);

    const meta = el('div', 'app-meta');
    if (app.runtime) meta.append(el('span', 'jchip', app.runtime));
    for (const platform of app.platforms) {
      // audience, form factor, screen count and whether it must work offline
      meta.append(deliveryTip(el('span', 'jchip', platform), 'platforms', platform));
    }
    if (app.offlineCapable) meta.append(tipFor(el('span', 'jchip', 'offline'), 'offline'));
    for (const dir of app.directions) meta.append(el('span', 'jchip', dir));
    card.append(meta);

    // screens by wave — the delivery shape of the app
    if (app.byWave) {
      const waves = el('div', 'wave-bar');
      const total = Object.values(app.byWave).reduce((a, n) => a + n, 0) || 1;
      for (const [wave, count] of Object.entries(app.byWave)) {
        const bar = el('div', `wave-seg ${wave}`, `${wave.replace('wave', 'W')} ${count}`);
        bar.style.flexGrow = String(count / total);
        waves.append(bar);
      }
      card.append(waves);
    }

    const contracts = el('div', 'app-contracts');
    contracts.append(el('div', 'nav-label', `consumes ${app.contracts.length} contracts`));
    for (const name of app.contracts) {
      const node = state.index.nodes.find(
        (n) => n.type === 'file' && n.file.split('/').pop().replace(/\.ya?ml$/, '') === name
      );
      const pill = el('button', `nav-pill${node ? '' : ' unknown'}`, name);
      pill.onclick = () => {
        if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
        else toast(`No contract file called ${name}`);
      };
      contracts.append(pill);
    }
    card.append(contracts);

    const routes = el('details', 'app-routes');
    routes.append(el('summary', null, `${app.screens.length} routes`));
    for (const screen of app.screens) {
      const row = el('div', 'route-row');
      row.append(el('span', 'route-id', screen.id));
      row.append(el('code', 'route-path', screen.route));
      row.append(el('span', 'route-status', screen.status ?? ''));
      row.onclick = () => selectScreen(screen.id);
      routes.append(row);
    }
    card.append(routes);
    grid.append(card);
  }
  body.append(grid);

  // ---- the platform wireframes -----------------------------------------
  // One page per platform, showing every screen on it. This is the closest
  // thing the delivery has to "what the app looks like", and unlike the boards
  // it exists for all eight platforms that have screens.
  const wf = wireframes();
  // ---- the platform boards ----------------------------------------------
  // The board is the drawing: every screen on a platform, drawn, in one file —
  // P08's is 713KB and holds 73 of them. The thin `p08.html` beside it is
  // generated from the screen list and shows the same list this page already
  // has. So the board is what gets framed, and the platform each one belongs to
  // is declared by that platform rather than read off the file name.
  const platformBoards = Object.entries(wf?.platformBoards ?? {}).filter(([, b]) => b);
  if (platformBoards.length) {
    const frames = platformBoards.reduce((n, [, b]) => n + (b.frames ?? 0), 0);
    body.append(
      el('div', 'journey-section-label',
        `platform boards · ${platformBoards.length} boards, ${frames} screens drawn`)
    );
    body.append(
      el('p', 'pane-note',
        `Every screen on a platform, drawn, in one file. Each platform declares its own board in ` +
        `\`platform.wireframeBoard\`, so nothing here is matched by guessing — which is the ` +
        `difference between these and the design boards below.`)
    );
    for (const [code, board] of platformBoards.sort(([a], [b]) => a.localeCompare(b))) {
      const platform = state.journeys?.platforms?.find((p) => p.code === code);
      body.append(
        wireframeSection(
          // a whole board rather than one frame out of it, so the frame url is
          // the board itself and there is no anchor
          { board: { ...board, frameUrl: board.url, url: board.url, anchor: null } },
          {
            label: `${code} — ${platform?.shortName ?? platform?.name ?? code} · ${board.frames} screens`,
            height: 620,
            design: 1240,
            name: board.title ?? `${code} board`,
          }
        )
      );
    }
  }

  // ---- the design boards -----------------------------------------------
  // frontend/README.md: the boards are what the frontend plan was built from,
  // and the two apps that were missed were missed because they had no board.
  // So they belong on the page about what actually gets built.
  if (boards().length) {
    const unbuilt = boards().filter((b) => b.platform && !b.platformHasScreens);
    body.append(el('div', 'journey-section-label', `design boards · ${boards().length}`));
    body.append(
      el('p', 'pane-note',
        unbuilt.length
          ? `The frontend plan was built from boards like these. ${unbuilt.length} of them are for ` +
            `a platform with no screen definitions yet — the board is the only description of it.`
          : 'The frontend plan was built from boards like these.')
    );
    for (const board of boards()) {
      const card = boardCard(board, { height: 480 });
      const openHere = el('button', 'ghost-btn board-page', 'Open as a page');
      openHere.onclick = () => selectBoard(board.id);
      card.querySelector('.board-meta').prepend(openHere);
      body.append(card);
    }
    $('apps-hint').textContent += ` · ${boards().length} design boards`;
  }
}

// ── domain: states and events ────────────────────────────────────────
// The contracts declare 38 status enums. Not one of them says which moves
// between those states are legal, so nothing catches an order going from `held`
// to `refunded` without ever having been paid. states/ says which are legal;
// events/ says what crosses the outbox when one happens. Each checks the other.

const machines = () => state.domain?.machines ?? [];
const domainEvents = () => state.domain?.events ?? [];
const currentMachine = () => machines().find((m) => m.id === state.machineId) ?? machines()[0] ?? null;

const TRIGGER_LABEL = {
  operation: 'called by an operation',
  timer: 'a timer, with nobody watching',
  job: 'a background job',
  externalEvent: 'an event from elsewhere',
  cascade: 'a cascade from a parent',
};

function describeMachine(m) {
  const anchored = m.enumValues
    ? `checked against ${m.contract}.${m.enum}`
    : `${m.contract}.${m.enum} is not an enum, so nothing checks these states`;
  return (
    `${m.stats.states} states · ${m.stats.transitions} transitions · ` +
    `${m.stats.reversals} reversals · ${anchored}`
  );
}

function describeTransition(t) {
  const cause = t.operation ? t.operation : TRIGGER_LABEL[t.trigger] ?? t.trigger ?? 'nothing declared';
  const marks = [
    t.isReversal ? 'reversal' : null,
    t.requiresApproval ? 'needs approval' : null,
    t.emits.length ? `emits ${t.emits.join(', ')}` : null,
  ].filter(Boolean);
  return `${t.from} → ${t.to} · ${cause}${marks.length ? ` · ${marks.join(' · ')}` : ''}`;
}

function fillMachineSelect() {
  const select = $('states-scope');
  if (!select) return;
  select.innerHTML = '';
  for (const m of machines()) {
    const option = el('option', null, `${m.entity} — ${m.stats.states} states`);
    option.value = m.id;
    if (m.id === state.machineId) option.selected = true;
    select.append(option);
  }
}

function renderStates() {
  const m = currentMachine();
  if (!m) {
    machine.setData(null);
    $('states-hint').textContent = 'No state models in states/';
    return;
  }
  state.machineId = m.id;
  machine.setData(m);
  machine.setSelected(state.stateName);
  machine.resize();
  if (!machine.userAdjusted) machine.fit();
  $('states-hint').textContent = describeMachine(m);
  renderStateLegend(m);
  renderStateLinks();
}

function renderStateLegend(m) {
  const entries = [
    ['#34d399', 'initial'],
    ['#a78bfa', 'terminal'],
    ['#60a5fa', 'operation moves it'],
    ['#34d399', 'timer or job — dashed, because no operation causes it'],
    ['#fbbf24', 'reversal — value moving backwards'],
  ];
  if (m.stats.approvals) entries.push(['transparent', '✓ on a label means it needs approval']);
  if (m.stats.offline) entries.push(['transparent', `${m.stats.offline} states reachable offline`]);
  renderBoxLegend(
    $('states-legend'),
    entries,
    'drag a state to move it · scroll to zoom · hover a transition for its guard'
  );
}

/** The right pane for the states view: the guard, and what it publishes. */
function renderStateLinks() {
  const pane = $('links-pane');
  const m = currentMachine();
  if (!m) return;
  pane.innerHTML = '';

  const name = state.stateName;
  pane.append(sectionHead(name ?? m.entity, name ? `state of ${m.entity}` : `${m.contract}.${m.enum}`));

  if (!name) {
    // The model is the reviewable thing, not the individual state. Which
    // moves are legal is a decision somebody makes once for the whole entity —
    // signing off `paid` on its own would be signing off a fragment of an
    // argument. First in the rail for the same reason it is on a table: a
    // review below four sections of detail is a review nobody scrolls to.
    pane.append(auth.verdictBlock('state', m.id, `${m.entity} — ${m.stats.states} states`,
      { layer: 'domain' }));

    const facts = el('div', 'links-section');
    facts.append(sectionHead('The model', m.stats.states));
    for (const [label, value] of [
      ['Owner', m.owner ?? '—'],
      ['Initial', m.initial.join(', ') || '—'],
      ['Terminal', m.terminal.join(', ') || '—'],
      ['Reachable offline', m.offlineReachable.join(', ') || 'none'],
    ]) {
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', label), el('code', null, value));
      facts.append(row);
    }
    pane.append(facts);

    if (!m.enumValues) {
      const warn = el('div', 'pane-warn');
      warn.innerHTML =
        `<b>${m.contract}.${m.enum}</b> is not an enum — it declares no values. These ` +
        `${m.states.length} states are checked against nothing, which is the one thing this ` +
        `file exists to prevent.`;
      pane.append(warn);
    }
    if (m.notes) pane.append(noteBlock('Note', m.notes));
    for (const q of m.openQuestions) pane.append(noteBlock('Open question', q));
    return;
  }

  const outgoing = m.transitions.filter((t) => t.from === name);
  const incoming = m.transitions.filter((t) => t.to === name);
  for (const [label, group] of [['Leaves by', outgoing], ['Arrives by', incoming]]) {
    const section = el('div', 'links-section');
    section.append(sectionHead(label, group.length));
    if (!group.length) {
      section.append(el('p', 'pane-empty', label === 'Leaves by'
        ? 'Nothing. This is where a record stops.'
        : 'Nothing — records begin here.'));
    }
    for (const t of group) {
      const item = el('div', 'link-item transition-item');
      const top = el('div', 'transition-head');
      top.append(el('span', 'transition-arrow', label === 'Leaves by' ? `→ ${t.to}` : `${t.from} →`));
      if (t.isReversal) top.append(tipFor(el('span', 'tag reversal', 'reversal'), 'reversal'));
      if (t.requiresApproval) top.append(tipFor(el('span', 'tag approval', 'approval'), 'approval'));
      item.append(top);

      if (t.operation) {
        const op = el('button', 'link-op', t.operation);
        op.disabled = !t.operationKnown;
        op.title = t.operationKnown ? 'Open in the contracts' : 'No contract declares this operation';
        op.onclick = () => openOperation(t.operation);
        item.append(op);
      } else if (t.trigger) {
        item.append(
          tipFor(el('div', 'link-trigger', TRIGGER_LABEL[t.trigger] ?? t.trigger), t.trigger)
        );
      }
      if (t.guard) {
        item.append(
          tip(el('div', 'link-guard', t.guard), 'Guard',
            'What must be true for this move to be allowed. Stated here so it is not only in ' +
            'whoever wrote the handler.')
        );
      }
      for (const emit of t.emitsKnown ?? []) {
        const chip = el('button', `emit-chip${emit.known ? '' : ' missing'}`, `publishes ${emit.name}`);
        chip.onclick = () => emit.known && openEvent(emit.name);
        chip.disabled = !emit.known;
        if (!emit.known) chip.title = 'The event catalogue has no such event';
        item.append(chip);
      }
      section.append(item);
    }
    pane.append(section);
  }
}

function noteBlock(label, text) {
  const box = el('div', 'links-section');
  box.append(sectionHead(label, ''));
  const body = el('div', 'link-guard');
  body.innerHTML = inlineMarkdown(text);
  box.append(body);
  return box;
}

/** Jump to an operation in the contracts layer by its operationId. */
function openOperation(operationId) {
  const node = state.index.nodes.find((n) => n.type === 'operation' && n.name === operationId);
  if (!node) return toast(`No contract declares ${operationId}`);
  select(node.id);
  setLayer('contracts');
  setMode('reader');
}

function openEvent(name) {
  state.eventId = name;
  fillEventSelect();
  if (state.layer !== 'domain') setLayer('domain');
  setMode('events');
  renderEvents();
}

// ── domain: the event catalogue ──────────────────────────────────────
const ALL_EVENTS = '__all__';

function fillEventSelect() {
  const select = $('events-scope');
  if (!select) return;
  select.innerHTML = '';
  const all = el('option', null, `All events — ${domainEvents().length}`);
  all.value = ALL_EVENTS;
  if (!state.eventId) all.selected = true;
  select.append(all);
  for (const event of domainEvents()) {
    const option = el('option', null, `${event.name} — ${event.consumers.length} consumers`);
    option.value = event.name;
    if (event.name === state.eventId) option.selected = true;
    select.append(option);
  }
}

function renderEvents() {
  const body = $('events-body');
  body.innerHTML = '';
  const events = domainEvents();
  if (!events.length) {
    body.append(el('p', 'pane-empty', 'No events in events/'));
    return;
  }
  if (state.eventId) {
    const event = events.find((e) => e.name === state.eventId);
    if (event) {
      renderEventPage(body, event);
      renderEventLinks();
      return;
    }
    state.eventId = null;
  }
  renderEventCatalogue(body, events);
  renderEventLinks();
}

/**
 * The right pane for the events view: which contexts talk to which, counted.
 * Reporting consumes nine events and publishes none; marketing seven. That
 * asymmetry is the shape of the platform, and it is only legible as a list.
 */
function renderEventLinks() {
  const pane = $('links-pane');
  pane.innerHTML = '';
  const event = state.eventId ? domainEvents().find((e) => e.name === state.eventId) : null;

  if (event) {
    pane.append(sectionHead(event.name, `v${event.version}`));
    const facts = el('div', 'links-section');
    for (const [label, value] of [
      ['Publisher', event.publisher ?? '—'],
      ['Aggregate', event.aggregate ?? '—'],
      ['Retention', event.retention ?? 'not stated'],
      ['Critical', `${event.critical} of ${event.consumers.length} consumers`],
    ]) {
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', label), el('code', null, value));
      facts.append(row);
    }
    pane.append(facts);
    if (event.notes) pane.append(noteBlock('Note', event.notes));
    return;
  }

  const contexts = state.domain?.contexts ?? [];
  pane.append(sectionHead('Contexts', contexts.length));
  for (const context of [...contexts].sort(
    (a, b) => b.consumes.length + b.publishes.length - (a.consumes.length + a.publishes.length)
  )) {
    const row = el('div', 'link-item');
    row.append(el('span', 'link-name', context.name));
    row.append(el('span', 'link-weight', `${context.publishes.length}↑ ${context.consumes.length}↓`));
    row.title =
      `publishes ${context.publishes.join(', ') || 'nothing'}\n` +
      `consumes ${context.consumes.join(', ') || 'nothing'}`;
    if (context.contract) {
      row.onclick = () => {
        const node = state.nodesById.get(`file:${context.contract}`);
        if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
      };
    }
    pane.append(row);
  }
  pane.append(el('p', 'pane-note', '↑ publishes · ↓ consumes. A context that only consumes is a read model; one that only publishes has nobody depending on it yet.'));
}

/**
 * The catalogue, read as a ledger of who tells whom. Each row is one event with
 * its publisher on the left and every consumer on the right, critical ones
 * marked — a dead-lettered critical event is a page, not a dashboard.
 */
function renderEventCatalogue(body, events) {
  const s = state.domain.stats;
  $('events-hint').textContent =
    `${s.events} events · ${s.consumers} consumers · ${s.criticalConsumers} critical · ` +
    `${s.contexts} contexts`;

  const lede = el('div', 'journey-trigger');
  lede.innerHTML =
    `<b>platform.outbox</b> has always existed and has always been correct — publication is ` +
    `atomic with the state change. What never existed was a description of what it carries. ` +
    `These are the ${s.events} facts that cross it, and the ${s.consumers} consumers that are ` +
    `waiting for them.`;
  body.append(lede);

  for (const event of events) {
    const card = el('div', 'event-card');
    const head = el('div', 'event-head');
    const title = el('button', 'event-name', event.name);
    title.onclick = () => openEvent(event.name);
    head.append(title);
    head.append(el('span', 'event-version', `v${event.version}`));
    if (event.critical) {
      head.append(tipFor(el('span', 'tag critical', `${event.critical} critical`), 'critical'));
    }
    card.append(head);
    if (event.description) card.append(el('div', 'event-desc', event.description));

    const wire = el('div', 'event-wire');
    const from = el('div', 'event-side');
    from.append(el('div', 'event-side-label', 'published by'));
    from.append(contextChip(event.publisher, event.publisherContract));
    wire.append(from);

    const arrow = el('div', 'event-arrow');
    arrow.append(el('div', 'event-arrow-line'));
    arrow.append(el('div', 'event-arrow-note', event.emittedWhen ?? 'no transition stated'));
    wire.append(arrow);

    const to = el('div', 'event-side consumers');
    to.append(el('div', 'event-side-label', `consumed by ${event.consumers.length}`));
    const chips = el('div', 'event-chips');
    for (const consumer of event.consumers) {
      const chip = contextChip(consumer.context, consumer.contract);
      chip.classList.toggle('critical', consumer.isCritical);
      tip(
        chip,
        `${consumer.context}${consumer.isCritical ? ' — critical' : ''}`,
        consumer.purpose,
        `idempotency: ${consumer.idempotencyKey ?? 'NOT DECLARED'} · on failure: ${consumer.onFailure ?? 'not stated'}`
      );
      chips.append(chip);
    }
    to.append(chips);
    wire.append(to);
    card.append(wire);

    // an event no state model emits is the other half of the pairing: the
    // catalogue claims a fact that nothing in states/ produces
    if (!event.emittedBy.length) {
      const warn = el('div', 'event-warn');
      warn.textContent =
        'No state model emits this. Either the transition that publishes it is not written ' +
        'down, or it is published from somewhere the models do not cover.';
      card.append(warn);
    }
    body.append(card);
  }
}

function contextChip(name, contract) {
  const chip = el('button', 'context-chip', name ?? '—');
  if (contract) {
    chip.onclick = () => {
      const node = state.nodesById.get(`file:${contract}`);
      if (!node) return;
      select(node.id);
      setLayer('contracts');
      setMode('reader');
    };
  } else {
    chip.classList.add('unknown');
    chip.disabled = true;
    chip.title = 'No contract of this name';
  }
  return chip;
}

/** One event, in full: payload, consumers, and the transition that emits it. */
function renderEventPage(body, event) {
  $('events-hint').textContent =
    `${event.payload.length} payload fields · ${event.consumers.length} consumers · ` +
    `${event.critical} critical`;

  const back = el('button', 'ghost-btn', '← all events');
  back.onclick = () => { state.eventId = null; fillEventSelect(); renderEvents(); };
  body.append(back);

  const head = el('div', 'journey-head');
  head.append(el('div', 'journey-title', event.name));
  const chips = el('div', 'journey-chips');
  chips.append(el('span', 'jchip', `v${event.version}`));
  chips.append(el('span', 'jchip', `aggregate ${event.aggregate ?? '—'}`));
  if (event.publisher) chips.append(el('span', 'jchip', `published by ${event.publisher}`));
  if (event.retention) chips.append(el('span', 'jchip', event.retention));
  head.append(chips);
  body.append(head);

  if (event.description) {
    const lede = el('div', 'journey-trigger');
    lede.innerHTML = inlineMarkdown(event.description);
    body.append(lede);
  }

  // where it comes from
  const origin = el('div', 'journey-section');
  origin.append(el('div', 'journey-section-label', 'Emitted when'));
  if (event.emittedBy.length) {
    for (const source of event.emittedBy) {
      const row = el('div', 'emit-source');
      const jump = el('button', 'link-op', `${source.entity}: ${source.from} → ${source.to}`);
      jump.onclick = () => openMachine(source.file, source.to);
      row.append(jump);
      if (source.operation) row.append(el('span', 'link-trigger', `via ${source.operation}`));
      origin.append(row);
    }
  } else {
    const warn = el('div', 'event-warn');
    warn.textContent = `${event.emittedWhen ?? 'Stated nowhere'} — but no state model declares this transition emits it.`;
    origin.append(warn);
  }
  body.append(origin);

  // payload
  const payload = el('div', 'journey-section');
  payload.append(el('div', 'journey-section-label', `Payload · ${event.payload.length} fields`));
  const table = el('table', 'domain-table');
  const thead = el('thead');
  const hrow = el('tr');
  for (const h of ['Field', 'Type', '', 'Notes']) hrow.append(el('th', null, h));
  thead.append(hrow);
  table.append(thead);
  const tbody = el('tbody');
  for (const field of event.payload) {
    const row = el('tr');
    row.append(el('td', 'mono strong', field.field));
    row.append(el('td', 'mono', field.type));
    row.append(el('td', 'dim', field.required ? 'required' : 'optional'));
    row.append(el('td', 'dim', field.notes ?? ''));
    tbody.append(row);
  }
  table.append(tbody);
  payload.append(table);
  body.append(payload);

  // consumers — the part the schema calls the rule that matters
  const consumers = el('div', 'journey-section');
  consumers.append(el('div', 'journey-section-label', `Consumers · ${event.consumers.length}`));
  const ctable = el('table', 'domain-table');
  const chead = el('thead');
  const crow = el('tr');
  for (const h of ['Context', 'Purpose', 'Idempotency key', 'On failure', '']) {
    crow.append(el('th', null, h));
  }
  chead.append(crow);
  ctable.append(chead);
  const cbody = el('tbody');
  for (const consumer of event.consumers) {
    const row = el('tr');
    row.classList.toggle('critical-row', consumer.isCritical);
    const first = el('td');
    first.append(contextChip(consumer.context, consumer.contract));
    row.append(first);
    row.append(el('td', 'dim', consumer.purpose));
    const key = el('td', 'mono', consumer.idempotencyKey ?? 'NOT DECLARED');
    if (!consumer.idempotencyKey) key.classList.add('missing');
    tipFor(key, 'idempotencyKey');
    row.append(key);
    row.append(tipFor(el('td', 'mono dim', consumer.onFailure ?? '—'), consumer.onFailure));
    row.append(
      consumer.isCritical ? tipFor(el('td', null, 'critical'), 'critical') : el('td', null, '')
    );
    cbody.append(row);
  }
  ctable.append(cbody);
  consumers.append(ctable);
  body.append(consumers);

  if (event.notes) {
    const notes = el('div', 'journey-section');
    notes.append(el('div', 'journey-section-label', 'Note'));
    const text = el('div', 'journey-trigger');
    text.innerHTML = inlineMarkdown(event.notes);
    notes.append(text);
    body.append(notes);
  }
}

/** Open a state model, optionally with one state already selected. */
function openMachine(file, stateName = null) {
  const found = machines().find((m) => m.file === file || m.id === file);
  if (!found) return;
  state.machineId = found.id;
  state.stateName = stateName;
  machine.userAdjusted = false;
  fillMachineSelect();
  if (state.layer !== 'domain') setLayer('domain');
  setMode('states');
  renderStates();
}

// ── sidebar: domain layer ────────────────────────────────────────────
function renderDomainTree() {
  const box = $('tree');
  box.innerHTML = '';
  const needle = state.sideFilter;
  const hit = (s) => !needle || String(s).toLowerCase().includes(needle);

  if (groupBy() === 'contexts') return renderContextTree(box, hit);

  let count = 0;
  const models = el('div', 'tree-group');
  const head = el('div', 'tree-group-head');
  const dot = el('span', 'tree-group-dot');
  dot.style.background = '#60a5fa';
  head.append(dot, el('span', null, 'State models'));
  head.append(el('span', 'tree-group-count', String(machines().length)));
  models.append(head);
  models.append(el('div', 'tree-group-sub', 'states/'));

  for (const m of machines()) {
    if (!hit(m.entity) && !hit(m.enum) && !m.states.some((s) => hit(s.name))) continue;
    count += 1;
        if (!passesLens('state', m.id)) continue;
const row = el('div', 'tree-file machine-row');
    row.dataset.id = `machine:${m.id}`;
    row.append(el('span', 'tree-file-name', m.entity));
    markLens(row, 'state', m.id);
    const counts = el('span', 'tree-file-count', `${m.stats.states}/${m.stats.transitions}`);
    // the bare "9/14" is the one unlabelled number in the sidebar, and the two
    // halves are what the whole layer is about: the contracts declare the states,
    // and only this file says which moves between them are legal
    tip(
      counts,
      `${m.stats.states} states, ${m.stats.transitions} transitions`,
      `${m.entity} can be in **${m.stats.states}** states, with **${m.stats.transitions}** legal moves ` +
      `between them. The contract enum declares the states; nothing but this file says which moves ` +
      `are allowed.`,
      [
        m.stats.reversals ? `${m.stats.reversals} reversals` : null,
        m.stats.approvals ? `${m.stats.approvals} need approval` : null,
        m.enumValues ? null : 'not checked against an enum',
      ].filter(Boolean).join(' · ') || null
    );
    row.append(counts);
    if (!m.enumValues) row.classList.add('problem');
    row.onclick = () => openMachine(m.id);
    models.append(row);
  }
  box.append(models);

  const catalogue = el('div', 'tree-group');
  const ehead = el('div', 'tree-group-head');
  const edot = el('span', 'tree-group-dot');
  edot.style.background = '#f472b6';
  ehead.append(edot, el('span', null, 'Events'));
  ehead.append(el('span', 'tree-group-count', String(domainEvents().length)));
  catalogue.append(ehead);
  catalogue.append(el('div', 'tree-group-sub', 'events/'));

  for (const event of domainEvents()) {
    if (!hit(event.name) && !hit(event.publisher)) continue;
    count += 1;
        if (!passesLens('event', event.name)) continue;
const row = el('div', 'tree-file event-row');
    row.dataset.id = `event:${event.name}`;
    row.append(el('span', 'tree-file-name', event.name));
    markLens(row, 'event', event.name);
    const consumers = el('span', 'tree-file-count', String(event.consumers.length));
    const critical = event.consumers.filter((c) => c.critical).length;
    tip(
      consumers,
      `${event.consumers.length} consumer${event.consumers.length === 1 ? '' : 's'}`,
      event.consumers.length
        ? `Contexts that react to this fact. Delivery is at-least-once, so each one declares an ` +
          `idempotency key and what to do on failure.`
        : '**Nothing consumes this event.** It is published and nobody is listening.',
      [
        critical ? `${critical} critical` : null,
        event.emittedBy.length ? null : 'no transition emits it',
      ].filter(Boolean).join(' · ') || null
    );
    row.append(consumers);
    if (!event.emittedBy.length) row.classList.add('problem');
    row.onclick = () => openEvent(event.name);
    catalogue.append(row);
  }
  box.append(catalogue);

  // The most actionable list in the layer: the status enums nobody has modelled.
  // Each one is a set of states with no statement of which moves between them
  // are legal — which is the gap the whole folder exists to close.
  const unmodelled = (state.domain?.statusEnums ?? []).filter((e) => !e.modelled);
  if (unmodelled.length) {
    const gap = el('div', 'tree-group');
    const ghead = el('div', 'tree-group-head');
    const gdot = el('span', 'tree-group-dot');
    gdot.style.background = '#fbbf24';
    ghead.append(gdot, el('span', null, 'Enums with no model'));
    ghead.append(el('span', 'tree-group-count', String(unmodelled.length)));
    gap.append(ghead);
    gap.append(el('div', 'tree-group-sub', 'states exist; the legal moves between them do not'));

    for (const entry of unmodelled) {
      if (!hit(entry.name) && !hit(entry.contract)) continue;
      count += 1;
      const row = el('div', 'tree-file enum-row');
      row.append(el('span', 'tree-file-name', entry.name));
      const values = el('span', 'tree-file-count', `${entry.values}`);
      tip(
        values,
        `${entry.values} states, no model`,
        `\`${entry.contract}.${entry.name}\` declares **${entry.values}** states and nothing says which ` +
        `moves between them are legal. So any value can follow any other, and no reviewer can tell a ` +
        `wrong transition from a right one.`
      );
      row.append(values);
      row.title = `${entry.contract}.${entry.name} — ${entry.values} states, no model`;
      row.onclick = () => {
        const node = state.index.nodes.find(
          (n) => n.type === 'schema' && n.name === entry.name && n.file.includes(`/${entry.contract}.`)
        );
        if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
      };
      gap.append(row);
    }
    box.append(gap);
  }

  const s = state.domain?.stats ?? {};
  $('file-count').textContent = `${s.states ?? 0} states · ${s.events ?? 0} events${
    needle ? ` · ${count} match` : ''
  }`;
  markTreeSelection();
}

/**
 * The other reading: not the artefacts, but the bounded contexts and what they
 * owe each other. This is the only place in the viewer where contract-to-
 * contract coupling is visible, because the contracts do not $ref each other.
 */
function renderContextTree(box, hit) {
  const contexts = state.domain?.contexts ?? [];
  for (const context of contexts) {
    if (!hit(context.name)) continue;
    const row = el('div', 'tree-file context-row');
    row.dataset.id = `context:${context.name}`;
    row.append(el('span', 'tree-file-name', context.name));
    const counts = el('span', 'tree-file-count');
    counts.textContent = `${context.publishes.length}↑ ${context.consumes.length}↓`;
    row.append(counts);
    row.title =
      `publishes ${context.publishes.join(', ') || 'nothing'}\n` +
      `consumes ${context.consumes.join(', ') || 'nothing'}`;
    if (!context.contract) row.classList.add('problem');
    row.onclick = () => {
      if (!context.contract) return;
      const node = state.nodesById.get(`file:${context.contract}`);
      if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
    };
    box.append(row);
  }
  const s = state.domain?.stats ?? {};
  $('file-count').textContent = `${contexts.length} contexts · ${s.contextEdges ?? 0} links`;
}

// ── backend: the data model ──────────────────────────────────────────
/** Drill from the schema map into one schema's tables. */
function openSchema(name) {
  if (!state.backend?.modules?.some((m) => m.name === name)) return;
  state.dataModule = name;
  $('data-scope').value = name;
  data.userAdjusted = false;
  renderData();
}

function selectTable(name) {
  state.tableName = name;
  const table = (state.backend?.tables ?? []).find((t) => t.name === name);
  if (state.layer !== 'backend') { setLayer('backend'); }
  if (table && table.module !== state.dataModule) {
    state.dataModule = table.module;
    $('data-scope').value = table.module;
    data.userAdjusted = false;
    renderData({ focus: name });
  } else {
    data.setSelected(`table:${name}`);
    if (state.mode === 'data') data.focus(`table:${name}`, { zoom: Math.max(data.transform.k, 0.9) });
  }
  if (state.mode !== 'data') setMode('data');
  markTreeSelection();
  renderSidePane();
}

const ALL_SCHEMAS = '*';

/**
 * All 197 tables at once is a hairball with no labels, so the whole-database
 * view zooms out a level instead: one box per schema, listing which other
 * schemas its keys reach into and how many columns do the reaching.
 */
function buildSchemaMap() {
  const backend = state.backend;
  const byName = new Map(backend.modules.map((m) => [m.name, m]));
  const tableModule = new Map(backend.tables.map((t) => [t.name, t.module]));

  // schema -> schema -> { count, declared }
  const links = new Map();
  const note = (from, to, declared) => {
    if (!from || !to || from === to) return;
    if (!links.has(from)) links.set(from, new Map());
    const row = links.get(from).get(to) ?? { count: 0, declared: 0 };
    row.count += 1;
    if (declared) row.declared += 1;
    links.get(from).set(to, row);
  };

  // How much of each schema exists as SQL. Counted here rather than read from
  // `module.written`, which is derived from a `Status` column the current
  // workbook does not have — an absent optional column reads as blank by
  // design, so every module came back false and every box drew amber. The one
  // fact this view exists to show was stated in the sidebar and drawn nowhere.
  //
  // `table.ddl` is set from the parsed .sql, which is the same source the
  // single-schema view and the sidebar note already trust.
  const ddl = new Map();
  for (const table of backend.tables) {
    const row = ddl.get(table.module) ?? { written: 0, total: 0 };
    row.total += 1;
    if (table.ddl) row.written += 1;
    ddl.set(table.module, row);

    note(table.module, tableModule.get(table.childOf), true);
    for (const ref of table.references ?? []) note(table.module, tableModule.get(ref.toTable), true);
    for (const key of table.foreignKeys ?? []) note(table.module, tableModule.get(key.toTable), false);
  }

  const nodes = backend.modules.map((module) => {
    const out = [...(links.get(module.name) ?? [])].sort((a, b) => b[1].count - a[1].count);
    // Three states, not two. Binary green/amber would still be wrong: only one
    // schema is complete, several are part-written, and most have nothing —
    // and "half built" is the state a reader most needs to see, because it is
    // the one that looks finished from either end.
    const built = ddl.get(module.name) ?? { written: 0, total: module.tables ?? 0 };
    const state_ =
      built.total && built.written === built.total ? 'written'
        : built.written > 0 ? 'part'
          : 'none';
    return {
      id: `schema:${module.name}`,
      title: module.name,
      badge: state_ === 'none' ? `${module.tables}t` : `${built.written}/${built.total}t`,
      // green written · blue part-written · amber derivable but not written
      color: { written: '#34d399', part: '#60a5fa', none: '#fbbf24' }[state_],
      rows: out.map(([target, info]) => ({
        label: `→ ${target}`,
        value: `${info.count}`,
        strong: info.declared > 0,
        refTarget: target,
      })),
    };
  });

  const edges = [];
  for (const [from, targets] of links) {
    for (const [to, info] of targets) {
      if (!byName.has(from) || !byName.has(to)) continue;
      edges.push({
        source: `schema:${from}`,
        target: `schema:${to}`,
        label: String(info.count),
        dashed: info.declared === 0,
      });
    }
  }

  return { nodes, edges, own: nodes.length, declared: 0, inferred: 0, links };
}

/**
 * The tables of one schema module, plus any table they relate to in another —
 * drawn external, so a cross-schema relationship is visible rather than implied.
 */
function buildData(module, { inferred = true, ambient = false } = {}) {
  const backend = state.backend;
  const all = new Map(backend.tables.map((t) => [t.name, t]));
  const everything = module === ALL_SCHEMAS;
  const included = new Map();

  // A default partition has no columns of its own — it inherits them from the
  // parent. handoff/schema-viewer-notes.md asks for these to be kept out of the
  // entity view rather than drawn as empty boxes.
  const isDefaultPartition = (table) =>
    Boolean(table.ddl?.partitionOf) && (backend.columns[table.name] ?? []).length === 0;

  // The anchor filter, when one is set, replaces the schema as the population.
  //
  // "Everything anchored only on scope_node" is "everything purely
  // tenancy-scoped", and that question crosses schemas — asking it inside one
  // schema would answer a different and much less useful question.
  const anchor = state.dataAnchor;
  const onlyAnchor = state.dataAnchorOnly;

  for (const table of backend.tables) {
    if (isDefaultPartition(table)) continue;
    if (anchor) {
      const anchors = table.anchors ?? [];
      if (!anchors.includes(anchor)) continue;
      if (onlyAnchor && anchors.length !== 1) continue;
      included.set(table.name, table);
      continue;
    }
    if (everything || table.module === module) included.set(table.name, table);
  }

  // handoff/relationships.csv, where it exists, is the stated answer — and the
  // only source that says what *kind* each relationship is
  const stated = backend.relationships?.present ? backend.relationships : null;
  const relevant = stated
    ? stated.edges.filter(
        (e) => (ambient || e.kind !== 'ambient') && (inferred || e.declared)
      )
    : [];

  const pull = (name) => {
    if (!name || included.has(name)) return;
    const table = all.get(name);
    if (table && !isDefaultPartition(table)) included.set(name, table);
  };
  for (const table of [...included.values()]) {
    pull(table.childOf);
    for (const ref of table.references ?? []) pull(ref.toTable);
    for (const key of table.keys ?? []) pull(key.toTable);
    if (!stated && inferred) for (const key of table.foreignKeys ?? []) pull(key.toTable);
  }
  // A reference leaving the schema is drawn on the column rather than by
  // dragging the other table in — schema-viewer-notes.md asks for "catalogue as
  // thirteen tables and their real relationships", not thirteen tables and
  // nineteen visitors. A child's parent is the exception: where a row belongs
  // to a row in another schema, that parent is part of this schema's shape.
  if (stated && !everything) {
    const here = new Set(included.keys());
    for (const edge of relevant) {
      if (edge.kind === 'child' && here.has(edge.from)) pull(edge.to);
    }
  }

  const isOwn = (table) => everything || table.module === module;

  // Which boxes are a parent of another box on screen.
  //
  // Two sources, because they answer slightly different questions and both
  // are true. A `child` edge in relationships.csv is the stated parentage —
  // "this row belongs to that row". The lineage block adds the tables other
  // tables reach on their way to a schema root. A box gets the caption if
  // either says something hangs off it *and that something is also on screen*:
  // labelling a box "parent" of a table the reader cannot see explains nothing.
  const parents = new Set();
  if (stated) {
    for (const edge of relevant) {
      if (edge.kind === 'child' && included.has(edge.from) && included.has(edge.to)) {
        parents.add(edge.to);
      }
    }
  }
  for (const table of included.values()) {
    const via = table.reachesRootVia;
    const named = table.parent ?? (via ? (/->\s*(.+)$/.exec(via)?.[1] ?? '').trim() : '');
    if (named && included.has(named)) parents.add(named);
  }

  // Both captions in the accent purple, and told apart by the word rather than
  // by colour. Green already means "created by a migration" in this legend and
  // amber means "from another schema" — giving green a second meaning above
  // the box would make the legend say two things at once.
  const CAPTION = '#a78bfa';

  const captionOf = (table) => {
    // Root beats parent: a schema root is the parent of everything below it,
    // and saying only "parent" of the table the whole schema hangs from would
    // be the weaker of two true statements.
    if (table.isSchemaRoot) return ['schema root', CAPTION];
    if (parents.has(table.name)) return ['parent', CAPTION];
    return [null, null];
  };

  const nodes = [...included.values()].map((table) => {
    const [caption, captionColor] = captionOf(table);
    const columns = backend.columns[table.name] ?? [];
    const own = isOwn(table);
    return {
      id: `table:${table.name}`,
      title: everything ? table.name : table.name.split('.').slice(1).join('.') || table.name,
      badge: own ? (table.ddl ? `${columns.length} · sql` : String(columns.length)) : table.module,
      // green means the migration exists and this table is really there;
      // blue means it is derived from the contracts and still only planned
      color: !own ? '#fbbf24' : table.ddl ? '#34d399' : '#60a5fa',
      caption,
      captionColor,
      rows: columns.map((column) => {
        const target =
          column.keyTable ??
          column.referencesTable ??
          (inferred ? column.foreignKeyTable : null) ??
          null;
        // a relationship that leaves this schema has no box on screen, so the
        // column says where it goes instead of pointing at nothing
        const leaves =
          target && !everything && !included.has(target) && all.has(target) ? target : null;
        return {
          label: `${column.required ? '• ' : ''}${column.name}`,
          value: leaves ? `→ ${leaves}` : column.type,
          strong: column.required,
          refTarget: target,
          external: Boolean(leaves),
        };
      }),
      external: !own,
    };
  });

  const edges = [];
  const seen = new Set();
  const push = (from, to, label, { dashed = false, kind = 'reference' } = {}) => {
    if (!included.has(from) || !included.has(to) || from === to) return false;
    const key = `${from}|${to}`;
    if (seen.has(key)) return false; // one line per pair, however many columns join them
    seen.add(key);
    edges.push({ source: `table:${from}`, target: `table:${to}`, label, dashed, kind });
    return true;
  };

  const counts = { child: 0, reference: 0, ambient: 0, declared: 0, inferred: 0 };

  if (stated) {
    // child first, so a pair joined more than one way keeps the stronger kind
    const order = { child: 0, reference: 1, ambient: 2 };
    for (const edge of [...relevant].sort((a, b) => order[a.kind] - order[b.kind])) {
      const label = edge.kind === 'child' ? `child · ${edge.column}` : edge.column;
      if (push(edge.from, edge.to, label, { dashed: !edge.declared, kind: edge.kind })) {
        counts[edge.kind] += 1;
        counts[edge.declared ? 'declared' : 'inferred'] += 1;
      }
    }
  } else {
    // no relationships.csv — fall back to reading the DDL and column names
    for (const table of included.values()) {
      for (const key of table.keys ?? []) {
        if (push(table.name, key.toTable, key.columns.join(', '), {})) counts.declared += 1;
      }
      if (table.childOf && push(table.name, table.childOf, 'child of', { kind: 'child' })) counts.child += 1;
      for (const ref of table.references ?? []) {
        if (push(table.name, ref.toTable, ref.column, {})) counts.declared += 1;
      }
    }
    if (inferred) {
      for (const table of included.values()) {
        for (const key of table.foreignKeys ?? []) {
          if (push(table.name, key.toTable, key.column, { dashed: true })) counts.inferred += 1;
        }
      }
    }
  }

  // how many ambient edges are being withheld, so the toggle can say so
  const hiddenAmbient =
    stated && !ambient
      ? stated.edges.filter(
          (e) => e.kind === 'ambient' && included.has(e.from) && (inferred || e.declared)
        ).length
      : 0;

  return {
    nodes,
    edges,
    own: [...included.values()].filter(isOwn).length,
    stated: Boolean(stated),
    hiddenAmbient,
    ...counts,
  };
}

function renderData({ focus } = {}) {
  const backend = state.backend;
  const picker = $('data-scope');

  if (!backend?.tables?.length) {
    data.setData([], []);
    $('data-hint').textContent = backend?.present
      ? 'No schema workbook in backend/ — only the ADRs are readable.'
      : 'No backend/ directory.';
    return;
  }

  // The anchors, ordered by how much of the package answers to each — the
  // useful ones are at the top rather than in alphabetical order, and the
  // count is the honest shape of the package: 289 of 353 on scope_node.
  const anchorPick = $('data-anchor');
  if (!anchorPick.options.length) {
    const tally = new Map();
    for (const t of backend.tables) {
      for (const a of t.anchors ?? []) tally.set(a, (tally.get(a) ?? 0) + 1);
    }
    const none = el('option', null, 'any anchor · scope by schema');
    none.value = '';
    anchorPick.append(none);
    for (const [name, n] of [...tally].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))) {
      const option = el('option', null, `anchored on ${name} · ${n}`);
      option.value = name;
      anchorPick.append(option);
    }
  }
  anchorPick.value = state.dataAnchor ?? '';
  $('data-anchor-only-wrap').hidden = !state.dataAnchor;
  $('data-anchor-only').checked = state.dataAnchorOnly;
  // The schema selector means nothing while an anchor is set, because the
  // anchor crosses schemas. Disabled rather than left live and ignored.
  picker.disabled = Boolean(state.dataAnchor);

  if (picker.options.length !== backend.modules.length + 1) {
    picker.innerHTML = '';
    const everything = el('option', null, `whole database · ${backend.modules.length} schemas`);
    everything.value = ALL_SCHEMAS;
    picker.append(everything);
    for (const module of backend.modules) {
      const option = el(
        'option',
        null,
        `${module.name} · ${module.tables} tables${module.unlisted ? ' · not on the Modules sheet' : ''}`
      );
      option.value = module.name;
      picker.append(option);
    }
  }
  // A workbook whose Modules sheet cannot be read leaves this empty. That is
  // reported in the audit; it must not also take the whole app down, which is
  // what indexing [0] of an empty list did — every view went blank because one
  // spreadsheet column had been renamed.
  const valid = state.dataModule === ALL_SCHEMAS || backend.modules.some((m) => m.name === state.dataModule);
  if (!valid) state.dataModule = backend.modules[0]?.name ?? ALL_SCHEMAS;
  picker.value = state.dataModule;

  const inferred = $('data-inferred').checked;
  const ambient = $('data-ambient')?.checked ?? false;
  const wholeDatabase = state.dataModule === ALL_SCHEMAS;
  const built = wholeDatabase ? buildSchemaMap() : buildData(state.dataModule, { inferred, ambient });
  const { nodes, edges, own } = built;

  data.showRows = state.dataRows;
  $('data-rows').checked = data.showRows;
  $('data-inferred').disabled = wholeDatabase;
  if ($('data-ambient')) $('data-ambient').disabled = wholeDatabase;

  data.setData(nodes, edges);
  data.setSelected(state.tableName && !wholeDatabase ? `table:${state.tableName}` : null);

  // An anchor drives the population, so it also owns the sentence describing
  // it — otherwise the hint reports a schema that is not what is on screen.
  if (state.dataAnchor) {
    // Counted off the tables, not the diagram nodes. Nodes include the ones
    // pulled in to make an edge land, so counting those reported 296 where the
    // package says 289 — a viewer disagreeing with its own source by seven.
    const anchored = backend.tables.filter((t) => {
      const anchors = t.anchors ?? [];
      return anchors.includes(state.dataAnchor)
        && (!state.dataAnchorOnly || anchors.length === 1);
    });
    const schemas = new Set(anchored.map((t) => t.module).filter(Boolean)).size;
    const roots = anchored.filter((t) => t.isSchemaRoot).length;
    $('data-hint').textContent =
      `${anchored.length} of ${backend.tables.length} tables anchored on ${state.dataAnchor}`
      + (state.dataAnchorOnly ? ' and nothing else' : '')
      + ` · across ${schemas} schema${schemas === 1 ? '' : 's'}`
      + (roots ? ` · ${roots} schema root${roots === 1 ? '' : 's'}` : '');
    renderBoxLegend($('data-legend'), [
      ['#a78bfa', `anchored on ${state.dataAnchor}`],
    ], 'an anchor is where a table’s own outbound keys stop · '
       + '“anchored only on scope_node” is “purely tenancy-scoped”'
       + ' · PARENT above a box = something on screen hangs off it'
       + ' · SCHEMA ROOT = nothing above it');
  } else if (wholeDatabase) {
    const crossings = edges.reduce((a, e) => a + Number(e.label), 0);
    const withDdl = backend.tables.filter((t) => t.ddl).length;
    $('data-hint').textContent =
      `${nodes.length} schemas · ${backend.tables.length} tables, ${withDdl} written as SQL · ` +
      `${edges.length} schema-to-schema relationships across ${crossings} columns · ` +
      `click a row to open that schema`;
    renderBoxLegend($('data-legend'), [
      ['#34d399', 'every table written'],
      ['#60a5fa', 'part written'],
      ['#fbbf24', 'derivable, none written'],
    ], 'one box per schema · the badge counts tables that exist as SQL · the number on a line is how many columns cross it');
  } else {
    const module = backend.modules.find((m) => m.name === state.dataModule);
    const pulled = nodes.length - own;
    const written = [...nodes].filter((n) => !n.external && /sql/.test(String(n.badge))).length;
    // ai draws thirteen boxes with nothing in them, which reads as a broken
    // view rather than as the fact it is: the workbook names the tables and
    // has never written their columns. Say so, or the reader blames the viewer.
    const bare = nodes.filter((n) => !n.external && !n.rows.length).length;
    $('data-hint').textContent =
      `${own} tables${written ? `, ${written} with DDL` : ''}` +
      `${bare ? `, ${bare === own ? 'none' : `${own - bare}`} with columns on the workbook` : ''}` +
      `${pulled ? ` · ${pulled} pulled in from other schemas` : ''} · ` +
      (built.stated
        ? `${built.child} child, ${built.reference} reference` +
          (ambient ? `, ${built.ambient} ambient` : '') +
          ` · ${built.declared} declared, ${built.inferred} inferred` +
          (built.hiddenAmbient ? ` · ${built.hiddenAmbient} ambient hidden` : '')
        : `${built.declared} declared, ${built.inferred} inferred`) +
      (module?.unlisted
        ? ' · no row on the Modules sheet — counted from the tables that name it'
        : module ? ` · migration ${module.migration ?? '—'} (${module.status ?? 'unknown'})` : '');
    renderBoxLegend($('data-legend'), [
      ['#34d399', 'created by a migration'],
      ['#60a5fa', 'derived from the contracts, not written yet'],
      ['#fbbf24', 'table from another schema'],
    ], (built.stated
      ? 'thick = child (belongs to) · plain = reference · solid = declared, dashed = inferred' +
        (built.hiddenAmbient
          ? ` · ${built.hiddenAmbient} ambient keys hidden — venue, principal, subject, tenant`
          : '')
      : 'solid = a REFERENCES clause or a contract $ref · dashed = inferred from a *_id column name')
      // The caption above a box, explained where the box is. A label nobody can
      // decode is a label that costs space and gives nothing back.
      + ' · PARENT above a box = something on screen hangs off it'
      + ' · SCHEMA ROOT = nothing above it, everything in the schema reaches it');
  }

  // the layout is seeded in a knot and spreads as it settles, so framing it
  // now would frame the knot — wait for the simulation to converge
  data.onSettle = () => {
    data.onSettle = null;
    if (data.userAdjusted) return;
    data.resize();
    if (focus) data.focus(`table:${focus}`, { zoom: 1 });
    else data.fit();
  };
}

// ── backend: the migrations ──────────────────────────────────────────
// backend/ is the database as it actually is; the workbook in handoff/ is the
// database as it is meant to become. This view is the first of those.

function renderMigrations() {
  const body = $('migrations-body');
  const backend = state.backend;
  const migrations = backend?.migrations;
  body.innerHTML = '';

  if (!migrations?.files?.length) {
    body.append(el('p', 'pane-empty', 'No .sql migrations in backend/.'));
    $('migrations-hint').textContent = '';
    return;
  }

  const s = migrations.stats;
  const planned = (backend.stats.tables ?? 0) - s.tables;
  $('migrations-hint').textContent =
    `${s.files} migrations · ${s.tables} tables · ${s.foreignKeys} foreign keys · ` +
    `${s.policies} policies · ${planned} more tables planned`;

  // ---- what the migrations amount to -----------------------------------
  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', 'The database as it stands'));
  head.append(el('div', 'journey-trigger',
    `backend/ holds the DDL. ${s.tables} of the ${backend.stats.tables} tables in the schema ` +
    `reference exist as SQL; the other ${planned} are derived from the contracts and not ` +
    `written yet. Everything on this page is read from the .sql files, not from the workbook.`));
  body.append(head);

  const counts = el('div', 'deploy-grid');
  const stat = (label, value, warn = false) => {
    if (value == null) return;
    const cell = el('div', `deploy-cell${warn ? ' warn' : ''}`);
    cell.append(el('div', 'deploy-label', label));
    cell.append(el('div', 'deploy-value stat-figure', String(value)));
    counts.append(cell);
  };
  stat('tables', s.tables);
  stat('foreign keys', s.foreignKeys);
  stat('composite keys', s.composite);
  stat('partitioned', s.partitioned);
  stat('row security forced', `${s.forced} of ${s.rls}`);
  stat('policies', s.policies);
  stat('generated columns', s.generated);
  stat('enum types', s.types);
  body.append(counts);

  // ---- the files, in the order they apply -------------------------------
  body.append(el('div', 'journey-section-label', 'migrations, in apply order'));
  for (const file of migrations.files) {
    const card = el('div', 'migration-card');

    const top = el('div', 'app-head');
    top.append(el('span', 'app-name', file.version));
    top.append(el('span', 'migration-title', file.title));
    top.append(el('span', 'app-status', `${file.lines} lines`));
    card.append(top);

    const meta = el('div', 'app-meta');
    const chip = (label, value) => {
      if (!value) return;
      const c = el('span', 'jchip');
      c.append(el('span', null, label), el('b', null, String(value)));
      meta.append(c);
    };
    chip('tables', file.tables.length);
    chip('policies', file.policies);
    chip('row security', file.rlsTables.length);
    card.append(meta);

    const list = el('div', 'migration-tables');
    for (const name of file.tables.sort()) {
      const ddl = migrations.tables[name];
      const pill = el('button', 'nav-pill', name);
      const bits = [];
      if (ddl?.partitionBy) bits.push(`partitioned by ${ddl.partitionBy}`);
      if (ddl?.partitionOf) bits.push(`partition of ${ddl.partitionOf}`);
      if (ddl?.rls?.forced) bits.push('row security FORCED');
      if (ddl?.foreignKeys?.length) bits.push(`${ddl.foreignKeys.length} foreign keys`);
      pill.title = bits.join(' · ') || name;
      // only tables the workbook also knows can be opened in the Data view
      const known = (backend.tables ?? []).some((t) => t.name === name);
      pill.classList.toggle('unknown', !known);
      pill.onclick = () => (known ? selectTable(name) : toast(`${name} is not on the workbook's Tables sheet`));
      list.append(pill);
    }
    card.append(list);
    body.append(card);
  }

  // ---- the prose that ships beside the SQL ------------------------------
  for (const doc of backend.docs ?? []) {
    const card = el('div', 'journey-head doc-card');
    card.append(el('h2', 'journey-title', doc.title));
    if (doc.summary) card.append(el('div', 'journey-trigger', doc.summary));
    card.append(el('div', 'adr-file', doc.file));
    body.append(card);
  }

  // 14 tables exist in storage with no contract schema, and that is a decision
  const storageOnly = (backend.tables ?? []).filter((t) => t.storageOnly);
  if (storageOnly.length) {
    body.append(el('div', 'journey-section-label', `storage-only · ${storageOnly.length}`));
    const list = el('div', 'api-list');
    for (const table of storageOnly) {
      const row = el('div', 'api-row');
      row.append(el('span', 'api-id', table.name));
      row.append(el('span', 'api-purpose', table.storageReason ?? 'no reason recorded'));
      row.append(el('span', 'api-contract', table.ddl ? 'written' : 'planned'));
      row.onclick = () => selectTable(table.name);
      list.append(row);
    }
    body.append(list);
  }
}

// ── backend: read and write routing ──────────────────────────────────
function renderRouting() {
  const body = $('routing-body');
  const rows = state.backend?.scaling ?? [];
  body.innerHTML = '';

  if (!rows.length) {
    body.append(el('p', 'pane-empty', 'No routing sheet in the schema workbook.'));
    $('routing-hint').textContent = '';
    return;
  }

  const total = rows.reduce(
    (a, r) => ({
      writes: a.writes + r.writes,
      primary: a.primary + r.primaryReads,
      replica: a.replica + r.replicaReads,
      analytical: a.analytical + r.analyticalReads,
    }),
    { writes: 0, primary: 0, replica: 0, analytical: 0 }
  );
  const operations = total.writes + total.primary + total.replica + total.analytical;
  $('routing-hint').textContent =
    `${rows.length} contracts · ${operations} routed operations · ` +
    `${total.writes} writes · ${total.primary + total.replica + total.analytical} reads`;

  for (const adr of state.backend.adrs ?? []) {
    const card = el('div', 'journey-head');
    card.append(el('h2', 'journey-title', adr.title));
    if (adr.status) {
      const chips = el('div', 'journey-chips');
      const chip = el('span', 'jchip');
      chip.append(el('span', null, 'status'), el('b', null, adr.status));
      chips.append(chip);
      card.append(chips);
    }
    if (adr.summary) card.append(el('div', 'journey-trigger', adr.summary));
    card.append(el('div', 'adr-file', adr.file));
    body.append(card);
  }

  body.append(el('div', 'journey-section-label', 'operations by routing target'));

  const KINDS = [
    ['writes', 'primary (write)', '#f87171'],
    ['primaryReads', 'primary (read)', '#fbbf24'],
    ['replicaReads', 'replica', '#34d399'],
    ['analyticalReads', 'analytical', '#c084fc'],
  ];

  const sumOf = (r) => r.writes + r.primaryReads + r.replicaReads + r.analyticalReads;
  const max = Math.max(...rows.map(sumOf));
  const table = el('div', 'routing-table');

  for (const row of [...rows].sort((a, b) => sumOf(b) - sumOf(a))) {
    const line = el('div', 'routing-row');
    const name = el('button', 'routing-name', row.contract);
    const node = state.index.nodes.find(
      (n) => n.type === 'file' && n.file.split('/').pop().replace(/\.ya?ml$/, '') === row.contract
    );
    name.classList.toggle('unknown', !node);
    name.onclick = () => {
      if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
      else toast(`No contract file called ${row.contract}`);
    };
    line.append(name);

    const bar = el('div', 'routing-bar');
    const sum = row.writes + row.primaryReads + row.replicaReads + row.analyticalReads;
    bar.style.width = `${(sum / max) * 100}%`;
    for (const [key, label, color] of KINDS) {
      if (!row[key]) continue;
      const seg = el('div', 'routing-seg', String(row[key]));
      seg.style.flexGrow = String(row[key]);
      seg.style.background = color;
      seg.title = `${row[key]} ${label}`;
      bar.append(seg);
    }
    line.append(bar);
    line.append(el('span', 'routing-total', String(sum)));
    table.append(line);
  }
  body.append(table);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, KINDS.map(([, label, color]) => [color, label]),
    'writes always go to the primary; reads are declared per operation and enforced by the router');
}

// ── contracts: lineage ───────────────────────────────────────────────
// Which tables an operation touches. This cannot be derived from the contracts
// — `x-ticvai-persistence` says which schemas become tables, not which
// operations reach them — so it arrives as data, and the data is candid about
// how much of itself is guesswork. That candour is the design constraint here:
// an unresolved operation is drawn, not dropped.

const ROUTING_COLOR = {
  primary: '#f87171',
  replica: '#34d399',
  analytical: '#c084fc',
};

/** A table name that opens the table in the Backend layer, if it exists there. */
function tableChip(name, { write = false } = {}) {
  const chip = el('button', `lineage-table${write ? ' write' : ''}`, name);
  const known = (state.backend?.tables ?? []).some((t) => t.name === name);
  deliveryTip(chip, 'tables', name, {
    fallback: {
      title: name,
      body: known
        ? 'A table in the schema reference. No tip shipped for it.'
        : '**The schema workbook does not list this table.** The lineage names it, so either the ' +
          'table was renamed or the lineage was generated against a different schema.',
    },
  });
  chip.classList.toggle('unknown', !known);
  chip.onclick = () => {
    if (!known) return toast(`${name} is not in the schema reference`);
    selectTable(name);
    setLayer('backend');
    setMode('data');
  };
  return chip;
}

function renderLineage() {
  const body = $('lineage-body');
  const lineage = state.lineage;
  body.innerHTML = '';

  if (!lineage?.present) {
    body.append(el('p', 'pane-empty', 'No handoff/api-data-lineage.json in this package.'));
    $('lineage-hint').textContent = '';
    return;
  }

  const s = lineage.stats;
  $('lineage-hint').textContent =
    `${s.operations} operations · ${s.resolved} resolved · ${s.unresolved} unresolved · ` +
    `${s.tablesTouched} tables · ${s.services} services · ${s.storedProcedures} stored procedures`;

  const needle = state.lineageFilter.trim().toLowerCase();
  const hit = (text) => !needle || String(text).toLowerCase().includes(needle);

  // The honest header. Every other view in the app can state a total and mean
  // it; this one cannot, and saying so once at the top is cheaper than marking
  // every row.
  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', 'Operation to table'));
  const chips = el('div', 'journey-chips');
  for (const [label, value, cls] of [
    ['resolved', `${s.resolved} of ${s.operations}`, 'ok'],
    ['derived', s.derived, ''],
    ['hand-mapped', s.handMapped, ''],
    ['unresolved', s.unresolved, 'warn'],
  ]) {
    const chip = el('span', `jchip ${cls}`);
    chip.append(el('span', null, label), el('b', null, String(value)));
    chips.append(chip);
  }
  head.append(chips);
  head.append(
    el(
      'div',
      'journey-trigger',
      `${s.resolved} of ${s.operations} resolve to a table — ${s.derived} derived from persistence ` +
        `markers, ${s.handMapped} projections mapped by hand. The other ${s.unresolved} are not a ` +
        `defect list: most return a computed projection like OrderSummary or MediaEntitlements, ` +
        `which has no persistence marker because there is nothing to mark. The rest are commands ` +
        `with no body, health checks and sync endpoints. They are shown, dimmed, because ` +
        `${s.resolved} rows presented as the whole set would be the more misleading number.`
    )
  );
  // two sources state this join, and one of them is lossy
  if (s.routingFromWorkbook) {
    head.append(
      el(
        'div',
        'journey-trigger',
        `Built from two sources that state the same thing: handoff/api-data-lineage.json and the ` +
          `Data lineage sheet of the schema workbook. They agree wherever both speak — but the JSON ` +
          `left the routing blank on ${s.routingFromWorkbook} operations that the workbook decides, ` +
          `so those are filled from the sheet and marked.`
      )
    );
  }
  body.append(head);

  if (state.lineageScope === 'tables') return renderLineageByTable(body, hit);
  if (state.lineageScope === 'services') return renderLineageByService(body, hit);
  return renderLineageByOperation(body, hit);
}

function renderLineageByOperation(body, hit) {
  const rows = state.lineage.operations.filter(
    (o) =>
      (state.lineageUnresolved || o.resolved) &&
      (hit(o.name) || hit(o.path ?? '') || hit(o.service ?? '') ||
        o.reads.some(hit) || o.writes.some(hit))
  );

  const byContract = new Map();
  for (const op of rows) {
    const key = op.contract ?? '—';
    if (!byContract.has(key)) byContract.set(key, []);
    byContract.get(key).push(op);
  }

  body.append(el('div', 'journey-section-label', `${rows.length} operations`));

  for (const [contract, ops] of [...byContract].sort((a, b) => b[1].length - a[1].length)) {
    const section = el('details', 'lineage-group');
    section.open = byContract.size <= 4 || Boolean(state.lineageFilter);
    const summary = el('summary', 'lineage-group-head');
    const title = el('span', 'lineage-group-name', contract);
    deliveryTip(title, 'contracts', contract);
    summary.append(title);
    const resolved = ops.filter((o) => o.resolved).length;
    summary.append(el('span', 'lineage-group-count', `${resolved} of ${ops.length} resolved`));
    section.append(summary);

    // A closed <details> still builds every child it is given, and this view
    // gave it all 654 operations across 24 contracts — 7,098 elements for a
    // list of which one or two groups are ever open. The rows are built when a
    // group is first opened instead, which is the only moment anyone can see
    // them, and a group opened once keeps what it built.
    //
    // A group is capped as well: a contract with 90 operations is still 900
    // elements arriving in one frame, and nobody reads 90 rows before
    // scrolling. The rest come a page at a time, on a button that says how
    // many are left rather than an infinite scroll that never says.
    const fill = () => {
      if (section.dataset.filled) return;
      section.dataset.filled = '1';
      appendLineageRows(section, ops);
    };
    if (section.open) fill();
    else section.addEventListener('toggle', fill, { once: true });

    body.append(section);
  }
}

/** How many rows of one group arrive at a time. */
const LINEAGE_PAGE = 60;

function appendLineageRows(section, ops, from = 0) {
  const page = ops.slice(from, from + LINEAGE_PAGE);
  const more = ops.length - (from + page.length);

  for (const op of page) {
    const row = el('div', `lineage-row${op.resolved ? '' : ' unresolved'}`);

    const name = el('button', 'lineage-op', op.name);
    name.onclick = () => openOperation(op.name);
    row.append(name);

    const meta = el('div', 'lineage-meta');
    if (op.verb) meta.append(el('span', `verb ${op.verb.toLowerCase()}`, op.verb));
    if (op.path) meta.append(el('span', 'lineage-path', op.path));
    if (op.routing) {
      const chip = el('span', `lineage-routing${op.routingFrom === 'workbook' ? ' from-workbook' : ''}`, op.routing);
      chip.style.borderColor = ROUTING_COLOR[op.routing] ?? 'currentColor';
      const ROUTING_WHY = {
        replica: 'A read that may be served from a replica. ADR-0016 — the write path and the read path are separated deliberately.',
        analytical: 'Served from the analytical store. Never on a transaction path.',
        write: 'A write. It goes to the primary by definition.',
        primary: 'Must hit the primary. Either it writes, or it reads something it just wrote.',
      };
      tip(chip, `Routed to the ${op.routing}`,
        ROUTING_WHY[op.routing] ?? 'Routing stated by the schema reference.',
        op.routingFrom === 'workbook'
          ? 'from the workbook — api-data-lineage.json left this blank'
          : null);
      meta.append(chip);
    }
    if (op.procedure) {
      const chip = el('span', 'lineage-procedure', op.procedure);
      tip(chip, 'Stored procedure',
        `One of the few operations that runs as a stored procedure. **Services for all 654 ` +
        `operations, stored procedures for ten** — a procedure per operation would be a second ` +
        `codebase in a second language, with no type checking against the contracts.`);
      meta.append(chip);
    }
    if (op.scope) {
      const chip = el('span', 'lineage-scope', op.scope);
      tip(chip, `Scoped to a ${op.scope}`,
        'The level in the seven-level hierarchy this operation is authorised at. A grant here ' +
        'inherits downward and never bubbles up.');
      meta.append(chip);
    }
    if (op.offline) meta.append(tipFor(el('span', 'lineage-offline', 'offline'), 'offline'));
    if (op.service) {
      const chip = el('span', 'lineage-service', op.service);
      tip(chip, op.service, 'The service that owns this operation. 22 services across 654 operations.');
      meta.append(chip);
    }
    row.append(meta);

    if (op.reads.length || op.writes.length) {
      const tables = el('div', 'lineage-tables');
      for (const t of op.writes) tables.append(tableChip(t, { write: true }));
      for (const t of op.reads) tables.append(tableChip(t));
      row.append(tables);
    } else {
      const none = el('div', 'lineage-tables');
      const chip = el('span', 'lineage-unresolved-chip', 'no table');
      tip(chip, 'Resolves to no table',
        'Marked `unresolved` by the lineage rather than left blank. **Usually correct rather than ' +
        'missing**: an operation returning a computed projection has no persistence marker because ' +
        'there is nothing to mark. Commands with no body, health checks and sync endpoints are ' +
        'the same. 318 of the 654 are in this state.');
      none.append(chip);
      row.append(none);
    }
    section.append(row);
  }

  // The button carries the count, so "there is more" and "how much more" are
  // the same glance. Removing itself before appending the next page keeps it
  // last without any reordering.
  if (more > 0) {
    const button = el('button', 'lineage-more', `${more} more in this contract`);
    button.type = 'button';
    button.onclick = () => {
      button.remove();
      appendLineageRows(section, ops, from + page.length);
    };
    section.append(button);
  }
}

function renderLineageByTable(body, hit) {
  const rows = state.lineage.tables.filter(
    (t) => hit(t.table) || t.reads.some(hit) || t.writes.some(hit)
  );
  const s = state.lineage.stats;

  // The workbook's own reverse index reaches further than the lineage does,
  // because it carries the screens too. Its subtitle is the reason to show it:
  // what breaks if this table changes.
  const unreached = (state.lineage.whereUsed ?? []).filter((t) => !t.reached);
  if (unreached.length) {
    const note = el('div', 'lineage-note');
    note.innerHTML = inlineMarkdown(
      `Of the ${s.tablesIndexed} tables in the schema reference, **${s.tablesReachedByAnOperation}** ` +
      `are reached by an operation and **${s.tablesReachedByAScreen}** by a screen. The other ` +
      `**${unreached.length}** are reached by nothing at all — written by a job, a migration or a ` +
      `trigger, or by nothing yet.`
    );
    body.append(note);
    const list = el('div', 'lineage-tables wrap');
    for (const entry of unreached) {
      const chip = tableChip(entry.table);
      chip.classList.add('unreached');
      tip(chip, entry.table,
        '**No operation in any contract reads or writes this table.** Not necessarily wrong — a job, ' +
        'a migration or a trigger may. But nothing in the API reaches it.');
      list.append(chip);
    }
    body.append(list);
  }

  body.append(
    el('div', 'journey-section-label', `${rows.length} tables reached by an operation`)
  );
  // A table written by many operations is the one a schema change costs most to
  // make, and that is not visible anywhere else in the viewer.
  const max = Math.max(1, ...rows.map((t) => t.reads.length + t.writes.length));
  const table = el('div', 'routing-table');
  for (const entry of rows) {
    const line = el('div', 'routing-row');
    const name = el('button', 'routing-name', entry.table);
    deliveryTip(name, 'tables', entry.table);
    name.onclick = () => { selectTable(entry.table); setLayer('backend'); setMode('data'); };
    line.append(name);

    const bar = el('div', 'routing-bar');
    bar.style.width = `${((entry.reads.length + entry.writes.length) / max) * 100}%`;
    for (const [count, label, color] of [
      [entry.writes.length, 'written by', '#f87171'],
      [entry.reads.length, 'read by', '#34d399'],
    ]) {
      if (!count) continue;
      const seg = el('div', 'routing-seg', String(count));
      seg.style.flexGrow = String(count);
      seg.style.background = color;
      seg.title = `${label} ${count} operation${count === 1 ? '' : 's'}`;
      bar.append(seg);
    }
    line.append(bar);
    line.append(el('span', 'routing-total', String(entry.reads.length + entry.writes.length)));
    table.append(line);
  }
  body.append(table);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [['#f87171', 'written by'], ['#34d399', 'read by']],
    'only the 165 tables some operation reaches — the other 65 are written by nothing the lineage resolved');
}

function renderLineageByService(body, hit) {
  const rows = state.lineage.services.filter(
    (s) => hit(s.name) || s.operations.some(hit) || s.writes.some(hit)
  );
  body.append(el('div', 'journey-section-label', `${rows.length} services`));

  // A table two services both write is a boundary somebody drew in the wrong
  // place, so it is worth computing rather than leaving to the eye.
  const writers = new Map();
  for (const service of state.lineage.services) {
    for (const t of service.writes) {
      if (!writers.has(t)) writers.set(t, []);
      writers.get(t).push(service.name);
    }
  }
  const shared = [...writers].filter(([, list]) => list.length > 1);

  for (const service of rows) {
    const card = el('div', 'lineage-service-card');
    const head = el('div', 'lineage-group-head');
    const name = el('span', 'lineage-group-name', service.name);
    tip(name, service.name,
      `One of the 22 services the 654 operations divide into. It owns ${service.operations.length} ` +
      `operation${service.operations.length === 1 ? '' : 's'}.`);
    head.append(name);
    head.append(el('span', 'lineage-group-count',
      `${service.operations.length} operations · writes ${service.writes.length} · reads ${service.reads.length}`));
    card.append(head);

    if (service.writes.length) {
      const line = el('div', 'lineage-tables');
      line.append(el('span', 'lineage-label', 'writes'));
      for (const t of service.writes) {
        const chip = tableChip(t, { write: true });
        if (writers.get(t)?.length > 1) chip.classList.add('contested');
        line.append(chip);
      }
      card.append(line);
    }
    body.append(card);
  }

  if (shared.length) {
    body.append(el('div', 'journey-section-label', `${shared.length} tables written by more than one service`));
    const note = el('div', 'lineage-note');
    note.innerHTML = inlineMarkdown(
      `A table two services both write is a boundary drawn in the wrong place — whichever service ` +
      `does not own it is reaching across one. Not a defect on its own, but every one of these is a ` +
      `question worth asking before the code exists.`
    );
    body.append(note);
    const list = el('div', 'lineage-tables wrap');
    for (const [table, services] of shared.sort((a, b) => b[1].length - a[1].length)) {
      const chip = tableChip(table, { write: true });
      chip.classList.add('contested');
      chip.append(el('span', 'lineage-count', String(services.length)));
      tip(chip, table, `Written by **${services.join('**, **')}**.`);
      list.append(chip);
    }
    body.append(list);
  }
}

// ── frontend: waves ──────────────────────────────────────────────────
// Delivery sequencing. Every screen carries a wave and a wave is a commitment,
// so this is the one view that answers "what did we say we would ship first".
function renderWaves() {
  const body = $('waves-body');
  const lineage = state.lineage;
  body.innerHTML = '';

  if (!lineage?.present || !lineage.waves.length) {
    body.append(el('p', 'pane-empty', 'No handoff/screen-index.json in this package, so no wave is stated for any screen.'));
    $('waves-hint').textContent = '';
    return;
  }

  const screens = lineage.screens.filter((s) => !state.wavesOffline || s.offline);
  const unbuildable = screens.filter((s) => !s.operations.length).length;
  $('waves-hint').textContent =
    `${screens.length} screens · ${lineage.waves.length} waves · ` +
    `${screens.length - unbuildable} name an operation`;

  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', 'What ships when'));
  const chips = el('div', 'journey-chips');
  for (const wave of lineage.waves) {
    const inWave = screens.filter((s) => String(s.wave ?? 'unsequenced') === String(wave.wave));
    const chip = el('span', 'jchip');
    chip.append(el('span', null, `wave ${wave.wave}`), el('b', null, String(inWave.length)));
    chips.append(chip);
  }
  head.append(chips);
  head.append(
    el(
      'div',
      'journey-trigger',
      `A screen that names no operation is a screen somebody can draw and nobody can build. ` +
        `${unbuildable} of ${screens.length} are in that state, and they are not evenly spread — ` +
        `which is the useful part.`
    )
  );
  body.append(head);

  const platformName = (code) =>
    state.journeys?.platforms?.find((p) => p.code === code)?.shortName ??
    state.journeys?.platforms?.find((p) => p.code === code)?.name ?? code;

  for (const wave of lineage.waves) {
    const inWave = screens.filter((s) => String(s.wave ?? 'unsequenced') === String(wave.wave));
    if (!inWave.length) continue;

    body.append(
      el('div', 'journey-section-label',
        `wave ${wave.wave} — ${inWave.length} screens, ` +
        `${inWave.filter((s) => s.operations.length).length} buildable`)
    );

    const byPlatform = new Map();
    for (const screen of inWave) {
      const key = screen.platform ?? '—';
      if (!byPlatform.has(key)) byPlatform.set(key, []);
      byPlatform.get(key).push(screen);
    }

    const grid = el('div', 'wave-grid');
    for (const [platform, list] of [...byPlatform].sort((a, b) => b[1].length - a[1].length)) {
      const card = el('div', 'wave-card');
      const title = el('div', 'wave-card-head');
      const code = el('span', 'wave-platform', platform);
      deliveryTip(code, 'platforms', platform);
      title.append(code, el('span', 'wave-platform-name', platformName(platform)));
      title.append(el('span', 'wave-count', String(list.length)));
      card.append(title);

      const cells = el('div', 'wave-cells');
      for (const screen of list.sort((a, b) => a.id.localeCompare(b.id))) {
        const buildable = screen.operations.length > 0;
        const cell = el('button', `wave-cell${!buildable && state.wavesUnbuilt ? ' unbuildable' : ''}`, screen.id);
        if (screen.reads.length || screen.writes.length) cell.classList.add('reaches-data');
        tip(
          cell,
          `${screen.id} — ${screen.name}`,
          buildable
            ? `Calls **${screen.operations.join('**, **')}**.` +
              (screen.services.length ? ` Served by ${screen.services.join(', ')}.` : '')
            : '**Names no operation.** Real screen, not yet specified — the index says so by returning ' +
              'an empty list rather than guessing one.',
          [screen.route, screen.offline ? 'offline-capable' : null,
           screen.storedProcedures.length ? `sproc: ${screen.storedProcedures.join(', ')}` : null]
            .filter(Boolean).join(' · ') || null
        );
        cell.onclick = () => { state.screenId = screen.id; setLayer('frontend'); setMode('screen'); };
        cells.append(cell);
      }
      card.append(cells);
      grid.append(card);
    }
    body.append(grid);
  }

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(
    legend,
    [['var(--accent)', 'reaches a table'], ['var(--text-dim)', 'names an operation'], ['#f87171', 'names none']],
    'wave and operations both from handoff/screen-index.json; the tables from the lineage behind it'
  );
}

// ── decisions ────────────────────────────────────────────────────────


// ── right pane ───────────────────────────────────────────────────────
/** Each layer answers "what links to this" about a different kind of thing. */
function renderSidePane() {
  fillSidePane();
  // the phone toggle only exists when there is something behind it
  syncLinksToggle();
}

function fillSidePane() {
  // Clear before the dispatch, not inside it.
  //
  // Each renderer below used to clear the pane itself, and the tail fell
  // through to `if (node) renderLinksPane(node)` with no else — so on any layer
  // with no dispatch line, and no selection ever made, nothing ran and nothing
  // cleared. The Frontend layer's links sat there on every Contracts view and
  // every Decisions view, describing a screen the reader was no longer looking
  // at. `state.selectedId` is never reset when the layer changes, so a reader
  // who had not clicked a contract kept the stale pane indefinitely.
  //
  // Clearing here also covers `renderStateLinks`, which returns early when
  // there is no machine — before its own clear, one line further down.
  const pane = $('links-pane');
  pane.innerHTML = '';

  if (state.layer === 'frontend') return renderScreenLinks();
  if (state.layer === 'backend') return renderTableLinks();
  // the states view explains a state in here; the events view is already a full
  // page about one event, so leaving the last state model up is just stale
  if (state.layer === 'domain') {
    return state.mode === 'events' ? renderEventLinks() : renderStateLinks();
  }
  const node = state.selectedId ? state.nodesById.get(state.selectedId) : null;
  if (node) return renderLinksPane(node);

  // Nothing selected. Say so in this layer's own noun — "Select a table." on
  // the Decisions layer was the Backend empty state left behind, which is the
  // same bug wearing a plausible sentence. `pane-empty` is what
  // syncLinksToggle counts as "not filled", so the phone toggle stays hidden.
  const ask = {
    contracts: 'Select a contract, an operation or a schema.',
    decisions: 'Select a decision or a register.',
  }[state.layer] ?? 'Select something to see what it links to.';
  pane.append(el('p', 'pane-empty', ask));
}

/** For a screen: the flows that traverse it and the screens either side. */
function renderScreenLinks() {
  const pane = $('links-pane');
  pane.innerHTML = '';

  // a board is open in place of a screen — say what it is and what it covers
  const board = state.boardId ? boards().find((b) => b.id === state.boardId) : null;
  if (board) {
    pane.append(sectionHead('Design board', 1));
    const facts = el('div', 'impl-card');
    const line = (label, value) => {
      if (!value) return;
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', label));
      row.append(el('code', null, String(value)));
      facts.append(row);
    };
    line('file', board.file);
    line('platform', board.platform ? `${board.platform} ${board.platformName}` : 'unmatched');
    line('matched by', board.matchedBy ?? '—');
    line('size', formatBytes(board.bytes));
    if (board.revision) line('revision', board.revision);
    pane.append(facts);
    pane.append(
      el('p', 'pane-note',
        board.inferred
          ? 'The platform is inferred from the file name. Renaming the file with the platform ' +
            'code, or naming the board in a screen’s wireframe block, makes it declared.'
          : 'The platform is declared.')
    );

    const on = board.platform
      ? (state.journeys?.screens ?? []).filter((s) => s.platform === board.platform)
      : [];
    pane.append(sectionHead('Screens on this platform', on.length));
    if (!on.length) {
      pane.append(
        el('p', 'pane-note',
          'None yet. This platform has no screen definitions, which is why the board is the ' +
          'only description of it.')
      );
    } else {
      for (const screen of on) {
        const row = el('div', 'link-item');
        row.append(el('span', 'link-name', `${screen.id} ${screen.name}`));
        row.onclick = () => selectScreen(screen.id);
        pane.append(row);
      }
    }
    return;
  }

  const screen = screenById(state.screenId);
  if (!screen) {
    pane.append(el('p', 'pane-empty', 'Select a screen.'));
    return;
  }

  const flows = (state.journeys?.flows ?? []).filter((f) =>
    f.steps.some((s) => s.screenId === screen.id)
  );
  pane.append(sectionHead('Flows through here', flows.length));
  if (!flows.length) {
    pane.append(el('p', 'pane-empty', 'No flow declares a step on this screen.'));
  }
  for (const flow of flows) {
    const steps = flow.steps.filter((s) => s.screenId === screen.id).map((s) => s.step);
    const row = el('div', 'link-item');
    row.append(el('span', 'link-name', `${flow.id} ${flow.name}`));
    row.append(el('span', 'link-weight', `step ${steps.join(', ')}`));
    row.onclick = () => { state.journeyId = flow.id; setMode('journey'); };
    pane.append(row);
  }

  // which screens reach this one, computed from every screen's exitTo
  const inbound = (state.journeys?.screens ?? []).filter((s) =>
    (s.navigation?.exitTo ?? []).includes(screen.id)
  );
  pane.append(sectionHead('Reached from', inbound.length));
  if (!inbound.length) {
    pane.append(el('p', 'pane-empty',
      screen.navigation?.isEntryPoint ? 'An entry point — reached from outside the app.' : 'No screen exits to this one.'));
  }
  for (const from of inbound) {
    const row = el('div', `link-item${from.navigationInferred ? ' inferred' : ''}`);
    row.append(el('span', 'link-name', `${from.id} ${from.name}`));
    row.append(el('span', 'link-file', from.navigationInferred ? 'inferred' : from.platform ?? ''));
    row.onclick = () => selectScreen(from.id);
    pane.append(row);
  }
  if (inbound.some((s) => s.navigationInferred)) {
    pane.append(el('p', 'pane-note', 'Underlined routes come from a navigation block marked inferred.'));
  }
}

/** For a table: the contract schema behind it, its children, and its keys. */
/**
 * The schema itself, when no single table is selected.
 *
 * This was "Select a table." — an instruction where the answer to the question
 * should be. A schema is a reviewable thing in its own right: whether `orders`
 * is the right set of tables with the right boundary is a decision somebody
 * makes once, and it is not the sum of 23 separate opinions about each table.
 * Reviewing it per table is how a boundary never gets reviewed at all.
 */
function renderSchemaLinks(pane) {
  const name = state.dataModule;
  const module = (state.backend?.modules ?? []).find((m) => m.name === name);
  if (!module) {
    // The scope selector above the diagram is what picks a schema, not the
    // left rail — the rail groups tables by schema but does not scope to one.
    // Naming the wrong control is worse than naming none.
    pane.append(el('p', 'pane-empty',
      state.dataModule === ALL_SCHEMAS
        ? 'The whole database is in scope. Pick one schema in the selector above to review it, '
          + 'or click a table to review that.'
        : 'Pick a schema in the selector above the diagram, or click a table to review that.'));
    return;
  }

  const tables = (state.backend?.tables ?? []).filter((t) => t.module === name);
  const written = tables.filter((t) => t.ddl).length;
  pane.append(sectionHead(name, `${tables.length} tables`));
  pane.append(auth.verdictBlock('schema', name, `${name} — ${tables.length} tables`,
    { layer: 'backend' }));

  const facts = el('div', 'impl-card');
  for (const [label, value] of [
    // Two counts, both named, because they disagree and the viewer is not the
    // place to decide which is right. `module.tables` is what the Modules sheet
    // declares; the other is how many tables actually carry this schema. They
    // sum to 267 against 358 across the package, so the sheet is behind — and a
    // reviewer signing off a boundary should see that rather than one number
    // picked quietly on their behalf.
    ['Tables carrying it', String(tables.length)],
    ['On the Modules sheet', String(module.tables ?? '—')],
    // `ddl` is the marker the rest of the viewer uses for written-as-SQL — 39
    // across the package, which is the figure in the sidebar note. Not
    // `migration`, which every one of the 358 has and which would report the
    // whole database as built.
    ['Written as SQL', `${written} of ${tables.length}`],
    ['Tier', module.tier ?? '—'],
  ]) {
    const row = el('div', 'impl-row');
    row.append(el('span', 'impl-label', label), el('code', null, value));
    facts.append(row);
  }
  if (module.tables != null && module.tables !== tables.length) {
    const warn = el('div', 'pane-warn');
    warn.innerHTML = `The Modules sheet says <b>${module.tables}</b> tables and `
      + `<b>${tables.length}</b> carry this schema. The sheet is the stale one — it is `
      + `hand-maintained and the schema assignment is derived.`;
    pane.append(warn);
  }
  pane.append(facts);

  pane.append(sectionHead('Its tables', tables.length));
  for (const t of tables) {
    const row = el('div', `link-item${t.ddl ? '' : ' planned'}`);
    row.append(el('span', 'link-name', t.name));
    row.append(el('span', 'link-file', t.ddl ? 'written' : 'planned'));
    row.onclick = () => selectTable(t.name);
    pane.append(row);
  }
}


/**
 * Where a table hangs, walked to its schema root.
 *
 * `handoff/schema-reference.json` gained this on 20 August and nothing read it.
 * `reachesRootVia` names the immediate parent and the column that reaches it —
 * "sales_order_id -> orders.sales_order" — so the chain is walked one hop at a
 * time rather than read off `parent`, which only 46 of the 353 tables carry.
 *
 * Guarded against a cycle: the data is derived and should be acyclic, but a
 * viewer that hangs on bad input is worse than one that reports it.
 */
function lineageChain(table) {
  const byName = new Map((state.backend?.tables ?? []).map((t) => [t.name, t]));
  const chain = [];
  const seen = new Set([table.name]);
  let current = table;

  while (current && !current.isSchemaRoot) {
    const via = current.reachesRootVia;
    if (!via) break;
    const m = /^(.*?)\s*->\s*(.+)$/.exec(via);
    if (!m) break;
    const [, column, parentName] = [null, m[1].trim(), m[2].trim()];
    if (seen.has(parentName)) {
      chain.push({ column, name: parentName, cycle: true });
      break;
    }
    seen.add(parentName);
    chain.push({ column, name: parentName, table: byName.get(parentName) ?? null });
    current = byName.get(parentName);
    if (chain.length > 12) break;
  }
  return chain;
}

/** The "where it hangs" block: the chain up, and what it is anchored on. */
function renderLineageSection(pane, table) {
  const chain = lineageChain(table);
  const anchors = table.anchors ?? [];
  if (!chain.length && !anchors.length && !table.isSchemaRoot && !table.isAnchor) return;

  pane.append(sectionHead('Where it hangs', chain.length || (table.isSchemaRoot ? 1 : 0)));
  const card = el('div', 'impl-card lineage-card');

  if (table.isSchemaRoot) {
    card.append(el('p', 'lineage-root-note',
      'A schema root — nothing above it. Every table below reaches this one.'));
  }

  if (chain.length) {
    const list = el('div', 'lineage-chain');
    // The table itself first, so the chain reads as a path rather than a list
    // of ancestors with the subject missing from its own lineage.
    list.append(lineageStep(table.name, null, { self: true }));
    for (const step of chain) {
      list.append(lineageStep(step.name, step.column, {
        root: step.table?.isSchemaRoot,
        cycle: step.cycle,
      }));
    }
    card.append(list);
    if (table.depth != null) {
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', 'Depth'),
        el('code', null, `${table.depth} from ${table.schemaRoot ?? 'its root'}`));
      card.append(row);
    }
  }

  if (anchors.length) {
    const row = el('div', 'impl-row lineage-anchor-row');
    row.append(el('span', 'impl-label', 'Anchored on'));
    const chips = el('div', 'lineage-anchors');
    for (const a of anchors) {
      const chip = el('button', 'lineage-anchor', a);
      chip.type = 'button';
      // Clicking an anchor is the question the brief asked for: everything
      // anchored on this. `scope_node` alone answers "what is purely
      // tenancy-scoped", which the diagram could not be asked before.
      chip.onclick = () => { state.dataAnchor = a; renderData(); fillSidePane(); };
      chip.title = `Show every table anchored on ${a}`;
      chips.append(chip);
    }
    row.append(chips);
    card.append(row);
  }
  if (table.isAnchor) {
    card.append(el('p', 'lineage-root-note',
      'An anchor — other tables’ keys stop here rather than passing through.'));
  }

  pane.append(card);
}

function lineageStep(name, column, { self = false, root = false, cycle = false } = {}) {
  const step = el('div', `lineage-step${self ? ' self' : ''}${root ? ' root' : ''}`);
  if (column) {
    step.append(el('span', 'lineage-via', column));
  }
  const link = el('button', 'lineage-name', name);
  link.type = 'button';
  if (!self) link.onclick = () => selectTable(name);
  else link.disabled = true;
  step.append(link);
  if (root) step.append(el('span', 'lineage-tag', 'schema root'));
  if (cycle) step.append(el('span', 'lineage-tag cycle', 'cycle — chain stops here'));
  return step;
}

function renderTableLinks() {
  const pane = $('links-pane');
  pane.innerHTML = '';
  const table = (state.backend?.tables ?? []).find((t) => t.name === state.tableName);
  if (!table) return renderSchemaLinks(pane);

  // First in the rail, not last. It sat under "Operations that touch it",
  // "Foreign keys", "Inferred keys" and "Keys with no table" — four sections
  // long enough that on a table of any size the review was below the fold, and
  // the backend schema read as the one layer with no sign-off at all. Nothing
  // about it changed except where it is.
  pane.append(auth.verdictBlock('table', table.name, table.name, { layer: 'backend' }));

  // Where it hangs, immediately under the review — the first question a
  // reviewer asks about a table they do not recognise is what it belongs to.
  renderLineageSection(pane, table);

  // ---- what reaches this table -------------------------------------------
  // The workbook's Where used sheet, whose own subtitle is the reason to lead
  // with it: what breaks if this table changes. A foreign key says what this
  // table is joined to; this says who would notice if it moved.
  const used = (state.lineage?.whereUsed ?? []).find((t) => t.table === table.name);
  if (used) {
    pane.append(sectionHead('Operations that touch it', used.operations.length));
    if (!used.operations.length) {
      pane.append(
        el('p', 'pane-empty',
          'No operation in any contract reads or writes this table. A job, a migration or a ' +
          'trigger may — but nothing in the API reaches it.')
      );
    }
    for (const name of used.operations) {
      const op = state.lineage?.operations?.find((o) => o.name === name);
      const row = el('div', 'link-item');
      row.append(el('span', 'link-name', name));
      // says whether this operation writes the table or only reads it
      const writes = op?.writes?.includes(table.name);
      row.append(el('span', `link-weight${writes ? ' writes' : ''}`, writes ? 'writes' : 'reads'));
      if (op?.service) row.append(el('span', 'link-file', op.service));
      row.onclick = () => openOperation(name);
      pane.append(row);
    }

    pane.append(sectionHead('Screens that reach it', used.screens.length));
    if (!used.screens.length) {
      pane.append(
        el('p', 'pane-empty',
          'No screen reaches this table. 180 of the 230 tables are in that position — the API ' +
          'reaches them and no drawn screen does.')
      );
    }
    for (const ref of used.screens) {
      // the sheet writes these as "P01 WEB-002"
      const id = /([A-Z]{2,4}-\d{3})/.exec(ref)?.[1] ?? ref;
      const screen = state.journeys?.screens?.find((s) => s.id === id);
      const row = el('div', 'link-item');
      row.append(el('span', 'link-name', screen ? `${id} ${screen.name}` : ref));
      if (screen?.platform) row.append(el('span', 'link-file', screen.platform));
      row.onclick = () => {
        if (!screen) return toast(`${id} is not defined in screens/`);
        state.screenId = id;
        setLayer('frontend');
        setMode('screen');
      };
      pane.append(row);
    }
    pane.append(
      el('p', 'pane-note',
        'From the Where used sheet of the schema reference — "what breaks if this table changes".')
    );
  }

  // what the migration actually says, where there is one
  if (table.ddl) {
    pane.append(sectionHead('In the database', 1));
    const facts = el('div', 'ddl-card');
    const line = (label, value) => {
      if (!value) return;
      const row = el('div', 'impl-row');
      row.append(el('span', 'impl-label', label));
      row.append(el('code', null, String(value)));
      facts.append(row);
    };
    line('migration', table.ddl.file);
    line('primary key', table.ddl.primaryKey?.join(', '));
    line('partition', table.ddl.partitionBy);
    line('partition of', table.ddl.partitionOf);
    line('generated', table.ddl.generated?.join(', '));
    if (table.ddl.rls?.enabled) {
      line('row security', table.ddl.rls.forced ? 'enabled and FORCED' : 'enabled');
    }
    pane.append(facts);

    pane.append(sectionHead('Foreign keys', table.keys?.length ?? 0));
    for (const key of table.keys ?? []) {
      const row = el('div', 'link-item');
      row.append(el('span', 'link-name', key.toTable));
      row.append(el('span', 'link-weight', key.columns.join(', ')));
      if (key.onDelete) row.append(el('span', 'link-file', `on delete ${key.onDelete.toLowerCase()}`));
      else if (key.composite) row.append(el('span', 'link-file', 'composite'));
      row.onclick = () => selectTable(key.toTable);
      pane.append(row);
    }
    if (!table.keys?.length) pane.append(el('p', 'pane-empty', 'The DDL declares no foreign keys here.'));
    pane.append(el('p', 'pane-note', 'Read from a REFERENCES clause — declared, not inferred.'));
  } else if (table.claimsWritten) {
    pane.append(sectionHead('In the database', 0));
    pane.append(el('p', 'pane-empty',
      'The workbook marks this written, but no migration in backend/ creates it.'));
  }

  pane.append(sectionHead('Derived from', table.derivedFrom ? 1 : 0));
  if (table.derivedFrom) {
    const row = el('div', 'link-item');
    const dot = el('span', 'type-dot');
    dot.style.background = '#34d399';
    row.append(dot, el('span', 'link-name', table.derivedFrom));
    row.append(el('span', 'link-file', table.schemaFile?.split('/').pop().replace(/\.ya?ml$/, '') ?? 'not found'));
    row.onclick = () => {
      if (table.schemaId && state.nodesById.has(table.schemaId)) {
        select(table.schemaId);
        setLayer('contracts');
        setMode('reader');
      } else toast(`${table.derivedFrom} is not a schema any contract declares`);
    };
    pane.append(row);
  } else if (table.storageOnly) {
    pane.append(el('p', 'pane-empty', table.storageReason ?? 'Storage-only — no contract schema behind it.'));
  } else {
    pane.append(el('p', 'pane-empty', 'No source schema declared.'));
  }

  const children = (state.backend?.tables ?? []).filter((t) => t.childOf === table.name);
  pane.append(sectionHead('Child tables', children.length));
  for (const child of children) {
    const row = el('div', 'link-item');
    row.append(el('span', 'link-name', child.name));
    row.append(el('span', 'link-weight', `${child.columns} cols`));
    row.onclick = () => selectTable(child.name);
    pane.append(row);
  }
  if (!children.length) pane.append(el('p', 'pane-empty', 'Nothing is a child of this table.'));

  const references = table.references ?? [];
  pane.append(sectionHead('Declared references', references.length));
  for (const ref of references) {
    const row = el('div', 'link-item');
    row.append(el('span', 'link-name', ref.toTable));
    row.append(el('span', 'link-weight', `${ref.column}${ref.isArray ? '[]' : ''}`));
    row.onclick = () => selectTable(ref.toTable);
    pane.append(row);
  }
  if (!references.length) {
    pane.append(el('p', 'pane-empty', 'No relationship the contracts declare as a $ref.'));
  }

  // a table with DDL has real keys; the guesses were dropped for it
  const keys = table.foreignKeys ?? [];
  if (!table.ddl) {
    pane.append(sectionHead('Inferred keys', keys.length));
    for (const key of keys) {
      const row = el('div', 'link-item inferred');
      row.append(el('span', 'link-name', key.toTable));
      row.append(el('span', 'link-weight', key.column));
      if (key.self) row.append(el('span', 'link-file', 'self'));
      else if (key.fromDdl) row.append(el('span', 'link-file', 'per DDL'));
      else if (key.crossSchema) row.append(el('span', 'link-file', key.toTable.split('.')[0]));
      row.onclick = () => selectTable(key.toTable);
      pane.append(row);
    }
    const learned = keys.filter((k) => k.fromDdl).length;
    pane.append(
      el('p', 'pane-note',
        !keys.length ? 'No column here ends in _id with a table named for it.'
        : learned
          ? `Read from *_id column names. ${learned} of them follow a key a migration ` +
            `already declares elsewhere for the same column name.`
          : 'Read from *_id column names, not declared anywhere. Treat as a strong hint.')
    );
  }

  // columns pointing at nothing are the interesting gap
  const dangling = (state.backend?.columns?.[table.name] ?? []).filter(
    (c) => /_id$/.test(c.name) && !c.foreignKeyTable && !c.referencesTable
  );
  if (dangling.length) {
    pane.append(sectionHead('Keys with no table', dangling.length));
    for (const column of dangling) {
      const row = el('div', 'link-item');
      row.append(el('span', 'link-name', column.name));
      row.append(el('span', 'link-weight', column.type));
      pane.append(row);
    }
  }
}

function sectionHead(title, count) {
  const head = el('div', 'links-section-head');
  head.append(el('span', null, title));
  head.append(el('b', null, String(count)));
  return head;
}

function renderLinksPane(node) {
  const pane = $('links-pane');
  pane.innerHTML = '';

  // traceability: which screens call this operation and which flows reach it
  if (node.type === 'operation') {
    const usage = state.journeys?.operationUsage?.[node.name];
    const screens = usage?.screens ?? [];
    const flows = usage?.flows ?? [];
    pane.append(sectionHead('Called by screens', screens.length));
    if (!screens.length) {
      pane.append(el('p', 'pane-empty', 'No screen definition calls this operation.'));
    }
    for (const id of screens) {
      const screen = screenById(id);
      const row = el('div', 'link-item');
      row.append(el('span', 'link-name', screen ? `${id} ${screen.name}` : id));
      row.append(el('span', 'link-file', screen?.platform ?? ''));
      row.onclick = () => selectScreen(id);
      pane.append(row);
    }
    if (flows.length) {
      pane.append(sectionHead('In flows', flows.length));
      for (const id of flows) {
        const flow = (state.journeys?.flows ?? []).find((f) => f.id === id);
        const row = el('div', 'link-item');
        row.append(el('span', 'link-name', flow ? `${id} ${flow.name}` : id));
        row.onclick = () => { state.journeyId = id; setLayer('frontend'); setMode('journey'); };
        pane.append(row);
      }
    }

    // The tables it touches, listed here as well as in the Reaches card.
    //
    // This pane answers "what does this connect to", and until now it answered
    // it about screens, flows and $refs while leaving out the database
    // entirely — so the one direction a reviewer most often follows was the
    // one direction the pane would not follow. Writes are listed apart from
    // reads rather than merged: what an operation changes is a different
    // question from what it needs, and it is the one that decides how much
    // care a change to it takes.
    const trace = state.lineage?.operations?.find((o) => o.name === node.name);
    if (trace) {
      const writes = trace.writes ?? [];
      // A table it both reads and writes belongs under writes, which is the
      // stronger claim; listing it twice would overstate the count.
      const reads = (trace.reads ?? []).filter((t) => !writes.includes(t));

      const tableRows = (title, names, write) => {
        pane.append(sectionHead(title, names.length));
        for (const name of names) {
          const known = (state.backend?.tables ?? []).some((t) => t.name === name);
          const row = el('div', `link-item${write ? ' writes-table' : ''}`);
          const dot = el('span', 'type-dot');
          dot.style.background = write ? '#f87171' : '#34d399';
          row.append(dot, el('span', 'link-name', name));
          row.append(el('span', 'link-file', name.split('.')[0]));
          row.onclick = () => {
            if (!known) return toast(`${name} is not in the schema reference`);
            selectTable(name);
            setLayer('backend');
            setMode('data');
          };
          if (!known) row.classList.add('problem');
          pane.append(row);
        }
      };

      tableRows('Writes', writes, true);
      tableRows('Reads', reads, false);

      if (!writes.length && !reads.length) {
        pane.append(
          el('p', 'pane-note',
            trace.source === 'unresolved'
              ? 'The lineage carries no tables for this operation — 318 of the 654 are in that ' +
                'state. It is not a claim that it touches nothing.'
              : 'The lineage resolved this and found no table, usually a computed projection.')
        );
      }
    }
  }

  // and, for a schema, the table it is persisted into — or why it is not
  if (node.type === 'schema') {
    const tables = (state.backend?.tables ?? []).filter((t) => t.schemaId === node.id);
    if (tables.length) {
      pane.append(sectionHead('Persisted as', tables.length));
      for (const table of tables) {
        const row = el('div', 'link-item');
        row.append(el('span', 'link-name', table.name));
        row.append(el('span', 'link-weight', `${table.columns} cols`));
        row.append(el('span', 'link-file', table.ddl ? 'in the database' : table.migration ?? ''));
        row.onclick = () => selectTable(table.name);
        pane.append(row);
      }
    } else {
      // the workbook's No table sheet says why, for 162 of them
      const contract = node.file.split('/').pop().replace(/\.ya?ml$/, '');
      const reason =
        state.backend?.notPersisted?.[`${contract}.${node.name}`] ??
        Object.values(state.backend?.notPersisted ?? {}).find((n) => n.schema === node.name);
      if (reason) {
        pane.append(sectionHead('Not persisted', 1));
        pane.append(el('p', 'pane-note', `No table, deliberately — ${reason.reason}.`));
      }
    }
  }

  const incoming = state.incoming.get(node.id) ?? [];
  const outgoing = state.outgoing.get(node.id) ?? [];

  // a file's links are its members' links, rolled up
  const isFile = node.type === 'file';
  const fileIncoming = [];
  const fileOutgoing = [];
  if (isFile) {
    for (const member of state.byFile.get(node.file) ?? []) {
      for (const edge of state.incoming.get(member.id) ?? []) {
        if (state.nodesById.get(edge.source)?.file !== node.file) fileIncoming.push(edge);
      }
      for (const edge of state.outgoing.get(member.id) ?? []) {
        if (state.nodesById.get(edge.target)?.file !== node.file) fileOutgoing.push(edge);
      }
    }
  }

  addLinkSection(
    pane,
    'Referenced by',
    (isFile ? fileIncoming : incoming).map((e) => ({ id: e.source, weight: e.weight, kind: e.kind })),
    'Nothing references this yet.'
  );
  addLinkSection(
    pane,
    'References',
    (isFile ? fileOutgoing : outgoing).map((e) => ({ id: e.target, weight: e.weight, kind: e.kind })),
    'This does not reference anything.'
  );
}

function addLinkSection(pane, title, entries, emptyText) {
  // collapse duplicates that came from different members of the same file
  const merged = new Map();
  for (const entry of entries) {
    if (merged.has(entry.id)) merged.get(entry.id).weight += entry.weight;
    else merged.set(entry.id, { ...entry });
  }
  const list = [...merged.values()].sort((a, b) => b.weight - a.weight);

  const head = el('div', 'links-section-head');
  head.append(el('span', null, title));
  head.append(el('b', null, String(list.length)));
  pane.append(head);

  if (!list.length) {
    pane.append(el('p', 'pane-empty', emptyText));
    return;
  }

  for (const entry of list.slice(0, 300)) {
    const target = state.nodesById.get(entry.id);
    if (!target) continue;
    const row = el('div', 'link-item');
    const dot = el('span', 'type-dot');
    dot.style.background = colorForNode(target);
    row.append(dot);

    if (target.type === 'operation') {
      row.append(el('span', `method ${target.method}`, target.method));
    }
    row.append(el('span', 'link-name', target.name));
    if (entry.weight > 1) row.append(el('span', 'link-weight', `×${entry.weight}`));
    row.append(el('span', 'link-file', target.file.split('/').pop().replace(/\.ya?ml$/, '')));
    row.title = target.type === 'operation' ? `${target.method} ${target.path}` : `${TYPE_LABEL[target.type]} in ${target.file}`;
    row.onclick = () => { select(entry.id); setMode('reader'); };
    pane.append(row);
  }
}

// ── where a contract lands in the database ───────────────────────────
/**
 * The Backend layer has said "this table came from that schema" since the
 * start, and the Contracts layer never said the reverse — so the trail ran one
 * way only. Reading a schema, "does this become a table, and which one" could
 * only be answered by switching layer and searching for it by name. 182 of the
 * 554 schemas become a table and 21 become more than one, which is exactly the
 * case a one-way link hides.
 *
 * For an operation the join is not in the contracts at all:
 * `x-ticvai-persistence` says which schemas persist, never which operations
 * reach them. So it comes from the lineage — and the lineage is candid about
 * how much of itself is unresolved. Saying "no tables, and here is why" is the
 * point; drawing nothing would read as "touches nothing", which is a different
 * claim and usually a false one.
 */
function renderTrace(node) {
  const box = $('reader-trace');
  box.innerHTML = '';
  if (node.type === 'schema') traceSchema(box, node);
  else if (node.type === 'operation') traceOperation(box, node);
}

function traceSchema(box, node) {
  // The backend part is an extra on this layer, so it lands after the reader is
  // already drawn. "Not here yet" and "none" are different answers, and only
  // one of them is worth printing — partsArrived redraws when it arrives.
  if (!state.backend) return;

  const tables = (state.backend.tables ?? []).filter((t) => t.schemaId === node.id);
  box.append(sectionHead('Stored as', tables.length));

  if (!tables.length) {
    box.append(
      el('p', 'pane-empty',
        'No table in the schema reference is derived from this schema. Most are not meant to be — ' +
        'a request body, a filter or a projection has nowhere to be stored — and 182 of the 554 ' +
        'schemas do become one.')
    );
    return;
  }

  for (const table of tables) {
    const row = el('div', 'link-item');
    const dot = el('span', 'type-dot');
    // green for what exists in SQL, blue for what is still only planned — the
    // same two colours the Backend layer uses for the same distinction
    dot.style.background = table.migration ? '#34d399' : '#60a5fa';
    row.append(dot, el('span', 'link-name', table.name));
    row.append(el('span', 'link-weight', `${table.columns} columns`));
    row.append(
      el('span', 'link-file',
        table.migration ? `${table.migration} · in SQL` : 'planned, no migration')
    );
    row.onclick = () => {
      selectTable(table.name);
      setLayer('backend');
      setMode('data');
    };
    box.append(row);
  }

  if (tables.length > 1) {
    box.append(
      el('p', 'pane-note',
        `This schema is stored across ${tables.length} tables. 21 of them are — usually a parent ` +
        'and its lines, flattened into one object by the API and kept apart in the database.')
    );
  }
  box.append(
    el('p', 'pane-note',
      'From the schema reference workbook, which names the schema each table was derived from.')
  );
}

function traceOperation(box, node) {
  const entry = state.lineage?.operations?.find((o) => o.name === node.name);
  if (!entry) return;

  const writes = entry.writes ?? [];
  const reads = (entry.reads ?? []).filter((t) => !writes.includes(t));
  const touched = new Set([...writes, ...(entry.reads ?? [])]).size;

  box.append(sectionHead('Reaches', touched));

  const card = el('div', 'reach-card');
  const line = (label, nodes) => {
    if (!nodes.length) return;
    const row = el('div', 'reach-row');
    row.append(el('span', 'reach-label', label));
    const values = el('span', 'reach-values');
    for (const item of nodes) values.append(item);
    row.append(values);
    card.append(row);
  };

  if (entry.service) line('service', [el('span', 'lineage-service', entry.service)]);
  line('writes', writes.map((t) => tableChip(t, { write: true })));
  line('reads', reads.map((t) => tableChip(t)));
  if (entry.procedure) line('stored procedure', [el('span', 'lineage-procedure', entry.procedure)]);
  if (entry.routing) line('routing', [el('span', 'badge', entry.routing)]);

  if (!touched) {
    card.append(
      el('div', 'reach-row',
        el('span', 'pane-note',
          entry.source === 'unresolved'
            ? 'The lineage carries no tables for this operation. 318 of the 654 are in that state: ' +
              'the row exists, the reads and writes were never filled in. It is not a claim that ' +
              'this operation touches nothing.'
            : 'The lineage resolved this operation and found no table — usually because it returns ' +
              'a computed projection rather than reading one.'))
    );
  }
  box.append(card);
  box.append(
    el('p', 'pane-note',
      `From handoff/api-data-lineage.json · ${entry.source}. The Lineage view shows the same join ` +
      'across all 654 operations at once.')
  );
}

// ── reader ───────────────────────────────────────────────────────────
async function renderReader(node, { scroll = true } = {}) {
  $('reader-empty').hidden = true;
  $('reader-body').hidden = false;

  // The prose is held back from the index and fetched per contract. The reader
  // is already about to fetch the source of the same file, so this costs it no
  // extra round trip worth measuring — and it has to be awaited rather than
  // filled in afterwards, because the header is written once, right below.
  await ensureDetail(node.file);

  // header
  const head = $('reader-head');
  head.innerHTML = '';
  const kicker = el('div', 'reader-kicker');
  const dot = el('span', 'type-dot');
  dot.style.background = colorForNode(node);
  kicker.append(dot, el('span', null, TYPE_LABEL[node.type] ?? node.type));
  kicker.append(el('span', null, '·'), el('span', null, node.file));
  head.append(kicker);
  head.append(el('h1', 'reader-title', node.type === 'file' ? node.title : node.name));

  if (node.type === 'operation') head.append(el('div', 'reader-path', `${node.method} ${node.path}`));
  if (node.description) {
    head.append(el('div', 'reader-desc', node.description.trim()));
  }

  // Where it lands in the database — drawn before the verdict, because it is
  // most of what somebody signing off an operation needs to know.
  renderTrace(node);

  // An operation is one of the four things a person signs off. Schemas and
  // params are parts of one, not artefacts in their own right, so they get no
  // verdict of their own — a verdict on every node would be noise, not rigour.
  const validation = $('reader-validation');
  validation.innerHTML = '';
  if (node.type === 'operation') {
    validation.append(auth.verdictBlock('operation', node.name, `${node.method} ${node.path}`, { layer: 'contracts' }));
  }

  // metadata badges
  const meta = $('reader-meta');
  meta.innerHTML = '';
  const badge = (label, value, className = '') => {
    const b = el('span', `badge ${className}`);
    b.append(el('span', null, label));
    b.append(el('b', null, String(value)));
    return b;
  };

  if (node.type === 'operation') {
    if (node.permission) {
      const b = badge('permission', node.permission, 'perm');
      b.onclick = () => { select(`perm:${node.permission}`); };
      meta.append(b);
    }
    if (node.scopeLevel) meta.append(badge('scope', node.scopeLevel));
    if (node.offlineCapable != null) meta.append(badge('offline', node.offlineCapable));
    if (node.conflictPolicy) meta.append(badge('conflict', node.conflictPolicy));
    if (node.auth) meta.append(badge('auth', node.auth, 'warn'));
    if (node.selfScoped) meta.append(badge('self-scoped', node.selfScoped, 'warn'));
    for (const tag of node.tags ?? []) meta.append(badge('tag', tag));
    if (node.module) meta.append(badge('module', node.module));
    // inherited from the contract, so label it rather than implying it is per-endpoint
    for (const platform of node.platforms ?? []) meta.append(badge('platform (contract)', platform));
    for (const consumer of node.consumers ?? []) meta.append(badge('consumer', consumer, 'perm'));
  } else if (node.type === 'permission') {
    meta.append(badge('domain', node.domain));
    meta.append(badge('used by', `${node.useCount} operations`));
    if (!node.declared) meta.append(badge('status', 'NOT IN ENUM', 'warn'));
  } else if (node.type === 'file') {
    if (node.tier) meta.append(badge('tier', node.tier));
    if (node.module) meta.append(badge('module', node.module));
    if (node.requirements != null) meta.append(badge('requirements', node.requirements));
    meta.append(badge('operations', (state.byFile.get(node.file) ?? []).filter((n) => n.type === 'operation').length));
    meta.append(badge('components', (state.byFile.get(node.file) ?? []).filter((n) => n.type !== 'operation').length));
    meta.append(badge('lines', node.lineCount));
    if (node.version) meta.append(badge('version', node.version));
    for (const platform of node.platforms ?? []) {
      const b = badge('platform', platform.raw, 'perm');
      b.onclick = () => {
        state.groupBy = 'platforms';
        for (const other of $('group-by').querySelectorAll('button')) {
          other.classList.toggle('active', other.dataset.group === 'platforms');
        }
        state.expandedFiles.add(node.id);
        renderSideNote();
        renderTree();
      };
      meta.append(b);
    }
    for (const capability of node.capabilities ?? []) meta.append(badge('capability', capability));
  } else {
    if (node.dataType) meta.append(badge('type', node.dataType));
    if (node.propertyCount) meta.append(badge('properties', node.propertyCount));
    if (node.enumValues) meta.append(badge('enum', `${node.enumValues.length} values`));
    meta.append(badge('backlinks', node.inCount ?? 0));
  }

  // permission nodes have no source block of their own — list their operations
  if (node.type === 'permission') {
    const box = $('reader-source');
    box.innerHTML = '';
    const header = el('div', 'source-head');
    header.append(el('span', null, `operations granted by ${node.name}`));
    box.append(header);
    const users = (state.incoming.get(node.id) ?? []).map((e) => state.nodesById.get(e.source)).filter(Boolean);
    if (!users.length) {
      box.append(el('p', 'pane-empty', 'No operation declares this permission.'));
    }
    for (const op of users.sort((a, b) => a.file.localeCompare(b.file) || a.path.localeCompare(b.path))) {
      const row = el('div', 'link-item');
      row.append(el('span', `method ${op.method}`, op.method));
      row.append(el('span', 'link-name', `${op.path}`));
      row.append(el('span', 'link-file', op.name));
      row.onclick = () => select(op.id);
      box.append(row);
    }
    return;
  }

  await renderSource(node, { scroll });
}

async function renderSource(node, { scroll }) {
  const box = $('reader-source');
  box.innerHTML = '';

  const text = await fetchFile(node.file);
  const lines = text.split(/\r?\n/);
  const range = node.type === 'file' ? { start: 1, end: lines.length } : blockRange(lines, node.line);

  const header = el('div', 'source-head');
  header.append(el('span', null, node.file));
  header.append(el('span', 'spacer'));
  header.append(el('span', null, `lines ${range.start}–${range.end}`));

  const full = el('button', 'ghost-btn', node.type === 'file' ? 'Collapse' : 'Show whole file');
  header.append(full);
  box.append(header);

  const pre = el('pre', 'code');
  const from = node.type === 'file' ? 0 : Math.max(0, range.start - 1);
  const to = node.type === 'file' ? lines.length : Math.min(lines.length, range.end);

  for (let i = from; i < to; i++) {
    pre.append(codeLine(i + 1, lines[i], node.file, i + 1 === node.line && node.type !== 'file'));
  }
  box.append(pre);

  full.onclick = async () => {
    const showAll = full.dataset.all !== '1';
    full.dataset.all = showAll ? '1' : '';
    full.textContent = showAll ? 'Show block only' : 'Show whole file';
    pre.innerHTML = '';
    const a = showAll ? 0 : Math.max(0, range.start - 1);
    const b = showAll ? lines.length : Math.min(lines.length, range.end);
    for (let i = a; i < b; i++) {
      pre.append(codeLine(i + 1, lines[i], node.file, i + 1 === node.line));
    }
    if (showAll) {
      pre.querySelector('.highlight')?.scrollIntoView({ block: 'center' });
    }
  };

  if (scroll) $('view-reader').scrollTop = 0;
}

/** Extent of the YAML block that starts at `startLine` (1-based). */
function blockRange(lines, startLine) {
  const startIndex = startLine - 1;
  const first = lines[startIndex] ?? '';
  const baseIndent = first.length - first.trimStart().length;

  let end = startLine;
  for (let i = startIndex + 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) continue; // blank lines may sit inside the block
    const indent = line.length - line.trimStart().length;
    if (indent <= baseIndent) break;
    end = i + 1;
  }
  return { start: startLine, end };
}

const PERMISSION_RE = /\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+\b/g;

function codeLine(number, raw, currentFile, highlight) {
  const row = el('div', `code-line${highlight ? ' highlight' : ''}`);
  row.append(el('span', 'ln', String(number)));
  const body = el('span', 'code-body');
  body.innerHTML = highlightYaml(raw ?? '', currentFile);

  // clickable $refs
  for (const link of body.querySelectorAll('.ref-link')) {
    link.onclick = (e) => {
      e.stopPropagation();
      const id = link.dataset.target;
      if (id && state.nodesById.has(id)) select(id);
      else toast('That $ref does not resolve to a known component');
    };
  }
  for (const perm of body.querySelectorAll('.tok-perm')) {
    perm.onclick = () => {
      const id = `perm:${perm.textContent}`;
      if (state.nodesById.has(id)) select(id);
    };
    perm.style.cursor = 'pointer';
  }

  row.append(body);
  return row;
}

/** Resolve a raw $ref against the file it appears in, mirroring the indexer. */
function refToNodeId(ref, fromFile) {
  const [rawTarget, pointer = ''] = ref.split('#');
  let targetFile = fromFile;
  if (rawTarget) {
    const base = fromFile.split('/').slice(0, -1);
    for (const part of rawTarget.split('/')) {
      if (part === '..') base.pop();
      else if (part !== '.' && part !== '') base.push(part);
    }
    targetFile = base.join('/');
  }
  const parts = pointer.split('/').filter(Boolean);
  if (parts[0] !== 'components' || parts.length < 3) return null;
  const kinds = {
    schemas: 'schema', parameters: 'param', responses: 'response',
    requestBodies: 'requestBody', securitySchemes: 'securityScheme',
  };
  const kind = kinds[parts[1]];
  return kind ? `${kind}:${targetFile}#${parts[2]}` : null;
}

function highlightYaml(line, currentFile) {
  // $ref lines get a link for the pointer, the rest highlighted normally
  const refMatch = line.match(/^(.*?\$ref:\s*)(['"])(.*?)\2(.*)$/);
  if (refMatch) {
    const [, prefix, quote, ref, suffix] = refMatch;
    const id = refToNodeId(ref, currentFile);
    const broken = !id || !state.nodesById.has(id);
    const target = state.nodesById.get(id);
    return (
      tokenize(prefix) +
      `<span class="ref-link${broken ? ' broken' : ''}" data-target="${escapeHtml(id ?? '')}" title="${
        broken ? 'unresolved reference' : escapeHtml(`${TYPE_LABEL[target.type]} · ${target.file}`)
      }">${escapeHtml(quote + ref + quote)}</span>` +
      tokenize(suffix)
    );
  }
  return tokenize(line);
}

function tokenize(text) {
  const TOKEN =
    /('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")|(#.*$)|([A-Za-z_$][\w$.\-]*)(?=\s*:)|(\b\d+(?:\.\d+)?\b)|(\b(?:true|false|null)\b)/g;

  let out = '';
  let last = 0;
  let match;
  while ((match = TOKEN.exec(text))) {
    out += markPermissions(text.slice(last, match.index));
    const [full, str, comment, key, num, bool] = match;
    if (str) out += `<span class="tok-str">${markPermissions(str)}</span>`;
    else if (comment) out += `<span class="tok-comment">${escapeHtml(comment)}</span>`;
    else if (key) {
      const cls = key.startsWith('x-ticvai') ? 'tok-ext' : 'tok-key';
      out += `<span class="${cls}">${escapeHtml(key)}</span>`;
    } else if (num) out += `<span class="tok-num">${escapeHtml(num)}</span>`;
    else if (bool) out += `<span class="tok-bool">${escapeHtml(bool)}</span>`;
    last = match.index + full.length;
  }
  out += markPermissions(text.slice(last));
  return out;
}

/** Wrap PERMISSION_STRINGS so they become clickable cross-references. */
function markPermissions(text) {
  const escaped = escapeHtml(text);
  return escaped.replace(PERMISSION_RE, (m) =>
    state.nodesById.has(`perm:${m}`) ? `<span class="tok-perm">${m}</span>` : m
  );
}

async function fetchFile(relPath) {
  if (state.fileCache.has(relPath)) return state.fileCache.get(relPath);
  const res = await fetch(`/api/file?path=${encodeURIComponent(relPath)}`);
  const text = await res.text();
  state.fileCache.set(relPath, text);
  return text;
}

// ── audit ────────────────────────────────────────────────────────────
/** What each layer is worth saying before the problem list. */
function auditSummary() {
  const errors = (list) => list.filter((p) => p.severity === 'error').length;

  if (state.layer === 'frontend') {
    const j = state.journeys;
    if (!j) return 'No frontend data.';
    const ops = state.index.stats.operations;
    return (
      `${j.stats.screens} screens across ${j.stats.platforms} platforms · ${j.stats.flows} flows · ` +
      `${j.stats.apps} apps (${j.stats.scaffolded} scaffolded) · ` +
      `${j.stats.operationsCovered} of ${ops} operations are called by a screen · ` +
      `${j.stats.navigationInferred} of ${j.stats.screensWithNavigation} navigation blocks are inferred · ` +
      `${errors(j.problems)} errors`
    );
  }
  if (state.layer === 'domain') {
    const d = state.domain;
    if (!d?.present) return 'No state models in states/ and no events in events/.';
    const s = d.stats;
    return (
      `${s.machines} state models · ${s.states} states · ${s.transitions} transitions ` +
      `(${s.reversals} reversals, ${s.approvals} needing approval) · ` +
      `${s.statusEnumsModelled} of ${s.statusEnums} status enums have a model · ` +
      `${s.events} events · ${s.consumers} consumers, ${s.criticalConsumers} critical · ` +
      `${s.emitted} of ${s.events} events are emitted by a modelled transition · ` +
      `${errors(d.problems)} errors`
    );
  }
  if (state.layer === 'decisions') {
    const d = state.decisions;
    if (!d?.present) return 'No docs/ in this package.';
    const s = d.stats;
    return (
      `${s.adrs} ADRs (${s.accepted} accepted, ${s.amended} amended after acceptance) · ` +
      `${s.documents} documents holding ${s.rows} rows of reference data · ` +
      `${s.vectorsPassed} of ${s.vectors} permission vectors resolve as the spec requires · ` +
      `${s.artefactGaps} of ${s.artefactClasses} artefact classes are open, with ` +
      `${s.requirementsUnserved} requirements behind them · ` +
      `${errors(d.problems)} errors`
    );
  }
  if (state.layer === 'backend') {
    const b = state.backend;
    if (!b?.stats?.tables) return 'No schema workbook in backend/.';
    const s = b.stats;
    return (
      `${s.tables} tables · ${s.columns} columns · ${s.modules} schemas · ` +
      `${s.inDdl} tables exist in ${s.migrationFiles} migrations with ${s.ddlKeys} real foreign keys, ` +
      `the other ${s.tables - s.inDdl} are derived from the contracts · ` +
      `${s.linked} trace to a contract schema, ${s.notPersisted} schemas deliberately have none · ` +
      `${errors(b.problems)} errors`
    );
  }
  const { stats, problems } = state.index;
  return (
    `${stats.operations} operations across ${stats.files} contracts · ${stats.links} resolved links · ` +
    `${errors(problems)} errors`
  );
}

function renderAudit() {
  const problems = layerProblems();
  $('audit-summary').textContent = auditSummary();
  updateAuditBadge();

  const counts = { all: problems.length };
  for (const problem of problems) counts[problem.severity] = (counts[problem.severity] ?? 0) + 1;

  const filters = $('audit-filters');
  filters.innerHTML = '';
  for (const [key, label] of [
    ['all', 'All'], ['error', 'Errors'], ['warning', 'Warnings'], ['info', 'Notes'],
  ]) {
    const chip = el('button', 'chip', `${label} ${counts[key] ?? 0}`);
    chip.classList.toggle('on', state.auditFilter === key);
    chip.onclick = () => { state.auditFilter = key; renderAudit(); };
    filters.append(chip);
  }

  const list = $('audit-list');
  list.innerHTML = '';
  const rank = { error: 0, warning: 1, info: 2 };
  const visible = problems
    .filter((p) => state.auditFilter === 'all' || p.severity === state.auditFilter)
    .sort((a, b) => rank[a.severity] - rank[b.severity]);

  if (!visible.length) {
    list.append(el('div', 'audit-clean', 'Nothing to report in this category.'));
    return;
  }

  for (const problem of visible.slice(0, 500)) {
    const item = el('div', `audit-item ${problem.severity}`);
    item.append(el('span', 'audit-icon', problem.severity === 'error' ? '✕' : problem.severity === 'warning' ? '!' : 'i'));
    const body = el('div', 'audit-body');
    body.append(el('div', 'audit-message', problem.message));
    body.append(el('div', 'audit-where', `${problem.file}${problem.line ? `:${problem.line}` : ''}`));
    item.append(body);
    item.append(el('span', 'audit-kind', problem.kind));
    item.onclick = () => {
      // a domain problem names a file in states/ or events/, which the contract
      // index has never heard of — open the artefact itself instead
      if (problem.file?.startsWith('states/')) return openMachine(problem.file);
      if (problem.file?.startsWith('events/')) {
        const event = domainEvents().find((e) => e.file === problem.file);
        if (event) return openEvent(event.name);
      }
      const id = problem.nodeId && state.nodesById.has(problem.nodeId) ? problem.nodeId : `file:${problem.file}`;
      if (state.nodesById.has(id)) { select(id); setMode('reader'); }
    };
    list.append(item);
  }
}

// ── command palette ──────────────────────────────────────────────────
let paletteItems = [];
let paletteActive = 0;

function openPalette() {
  $('palette').hidden = false;
  const input = $('palette-input');
  input.value = '';
  input.focus();
  runSearch('');
}

function closePalette() { $('palette').hidden = true; }

/** Subsequence match with a score that favours prefix and word-boundary hits. */
function fuzzyScore(haystack, needle) {
  if (!needle) return 0;
  const lower = haystack.toLowerCase();
  const index = lower.indexOf(needle);
  if (index === 0) return 1000 - haystack.length;
  if (index > 0) return 700 - index * 2 - haystack.length * 0.1;

  let score = 0;
  let position = 0;
  let streak = 0;
  for (const ch of needle) {
    const found = lower.indexOf(ch, position);
    if (found === -1) return -1;
    streak = found === position ? streak + 1 : 0;
    score += 12 + streak * 4 - Math.min(8, found - position);
    position = found + 1;
  }
  return score - haystack.length * 0.15;
}

function runSearch(query) {
  const needle = query.trim().toLowerCase();
  const results = [];

  for (const node of state.index.nodes) {
    let best = fuzzyScore(node.name, needle);
    if (node.type === 'operation') {
      best = Math.max(best, fuzzyScore(node.path, needle) - 20, fuzzyScore(node.title ?? '', needle) - 60);
    }
    if (node.type === 'file') best += 40; // contracts rank above their members
    if (best > 0 || !needle) results.push({ node, score: best + (node.inCount ?? 0) * 0.3 });
  }

  results.sort((a, b) => b.score - a.score);
  paletteItems = results.slice(0, 60).map((r) => r.node);
  paletteActive = 0;
  renderPalette(needle);
}

function renderPalette(needle) {
  const box = $('palette-results');
  box.innerHTML = '';
  $('palette-count').textContent = `${paletteItems.length} result${paletteItems.length === 1 ? '' : 's'}`;

  if (!paletteItems.length) {
    box.append(el('div', 'palette-empty', 'No match'));
    return;
  }

  paletteItems.forEach((node, i) => {
    const item = el('div', `palette-item${i === paletteActive ? ' active' : ''}`);
    const dot = el('span', 'type-dot');
    dot.style.background = colorForNode(node);
    item.append(dot);
    if (node.type === 'operation') item.append(el('span', `method ${node.method}`, node.method));

    const main = el('div', 'palette-item-main');
    const title = el('div', 'palette-item-title');
    title.innerHTML = markMatch(node.name, needle);
    main.append(title);
    main.append(
      el('div', 'palette-item-sub',
        node.type === 'operation' ? node.path
          : node.type === 'permission' ? `${node.useCount} operations`
          : node.file)
    );
    item.append(main);
    item.append(el('span', 'palette-item-kind', TYPE_LABEL[node.type] ?? node.type));
    item.onmouseenter = () => { paletteActive = i; renderPalette(needle); };
    item.onclick = () => { select(node.id); setMode('reader'); closePalette(); };
    box.append(item);
  });

  box.querySelector('.active')?.scrollIntoView({ block: 'nearest' });
}

function markMatch(text, needle) {
  const escaped = escapeHtml(text);
  if (!needle) return escaped;
  const index = text.toLowerCase().indexOf(needle);
  if (index === -1) return escaped;
  const before = escapeHtml(text.slice(0, index));
  const hit = escapeHtml(text.slice(index, index + needle.length));
  const after = escapeHtml(text.slice(index + needle.length));
  return `${before}<mark>${hit}</mark>${after}`;
}

// ── live reload ──────────────────────────────────────────────────────
function connectLiveReload() {
  const source = new EventSource('/api/events');
  const dot = $('live-dot');

  // the server process this page was served by
  let boot = null;

  source.onopen = () => dot.classList.remove('stale');
  source.onerror = () => dot.classList.add('stale');
  source.onmessage = async (event) => {
    const data = JSON.parse(event.data);

    // The browser reconnects by itself when the connection drops, and a
    // reconnect carries no reload event — so after the server restarts this
    // page keeps running the JavaScript it was served beforehand. It does not
    // look stale; it looks broken, because a view added since is simply absent.
    // A different boot id means a different server, so take the whole page back.
    if (data.type === 'hello') {
      if (boot && boot !== data.boot) return location.reload();
      boot = data.boot;
      return;
    }

    if (data.type !== 'reload') return;

    state.fileCache.clear();
    state.treeCache.clear();
    state.structureFile = null; // force the diagram to rebuild from fresh YAML
    const keepSelection = state.selectedId;
    await loadIndex(); // refetches every layer, so all three stay in step
    renderModes();

    if (state.mode === 'screen') renderScreen();
    if (state.mode === 'apps') renderApps();
    if (state.mode === 'migrations') renderMigrations();
    if (state.mode === 'routing') renderRouting();
    if (state.mode === 'journey') renderJourney();
    if (state.mode === 'data') { renderData(); data.resize(); }

    dot.classList.remove('pulse');
    void dot.offsetWidth; // restart the animation
    dot.classList.add('pulse');
    toast(`Reindexed after ${data.file} changed`);

    if (keepSelection && state.nodesById.has(keepSelection)) select(keepSelection, { scroll: false });
  };
}

// ── drag to pan ──────────────────────────────────────────────────────
/**
 * Click and drag to move a scrolling pane, the way the canvas views already
 * work. A journey track is wider than any window, and reaching for a scrollbar
 * to read a flow left to right is the wrong gesture for it.
 *
 * Everything in these panes is clickable, so a drag has to not become a click:
 * movement under a few pixels stays a click, anything more suppresses the one
 * that follows.
 */
function enableDragScroll(element) {
  const THRESHOLD = 4;
  let start = null;
  let dragging = false;
  let suppressClick = false;

  element.addEventListener('mousedown', (event) => {
    if (event.button !== 0) return;
    // let controls, links and disclosure triangles behave normally
    if (event.target.closest('input, select, textarea, button, summary, a')) return;
    start = { x: event.clientX, y: event.clientY, left: element.scrollLeft, top: element.scrollTop };
    dragging = false;
    suppressClick = false;
  });

  window.addEventListener('mousemove', (event) => {
    if (!start) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (!dragging && Math.hypot(dx, dy) < THRESHOLD) return;
    dragging = true;
    element.classList.add('dragging');
    element.scrollLeft = start.left - dx;
    element.scrollTop = start.top - dy;
    event.preventDefault(); // otherwise it turns into a text selection
  });

  window.addEventListener('mouseup', () => {
    if (!start) return;
    suppressClick = dragging;
    start = null;
    dragging = false;
    element.classList.remove('dragging');
  });

  // capture, so the card underneath never sees the click that ended a drag
  element.addEventListener('click', (event) => {
    if (!suppressClick) return;
    suppressClick = false;
    event.stopPropagation();
    event.preventDefault();
  }, true);

  // a wide track with nothing to scroll vertically should take a plain wheel
  element.addEventListener('wheel', (event) => {
    if (event.deltaX || event.shiftKey) return; // already horizontal
    const canScrollDown = element.scrollHeight - element.clientHeight > 1;
    const canScrollAcross = element.scrollWidth - element.clientWidth > 1;
    if (canScrollDown || !canScrollAcross) return;
    element.scrollLeft += event.deltaY;
    event.preventDefault();
  }, { passive: false });
}

let toastTimer;
function toast(message) {
  const box = $('toast');
  box.textContent = message;
  box.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { box.hidden = true; }, 2600);
}

// ── wiring ───────────────────────────────────────────────────────────
// ── collapsible sections ────────────────────────────────────────────
// Every pane in the app builds a section the same way: a section label
// followed by its content as siblings, up to the next label. That one shape,
// held to in 35 places, is what lets this be a single handler rather than 35
// edits — and what makes a new section collapsible the day it is written,
// without its author doing anything.

/** Sections the reader has shut, by view and heading, so the choice survives
 *  a re-render — and so collapsing "operations" on one screen does not also
 *  collapse the notes on another. */
const collapsedSections = new Set();

/**
 * The two shapes that fold, and the one handler that folds them.
 *
 * A pane section is a label followed by its content as siblings. A sidebar
 * group is a `.tree-group` whose head is its first child and whose rows are
 * the rest — twelve platforms of 29 screens each, which is the list that made
 * this worth doing: reaching the kiosk meant scrolling past the whole of Guest
 * Web every time.
 */
const FOLD_HEADS = '.journey-section-label, .tree-group-head';

const isTreeHead = (label) => label.classList.contains('tree-group-head');

/** By view and heading, so the choice survives a re-render — and so collapsing
 *  "operations" on one screen does not also collapse the notes on another. A
 *  sidebar group is keyed by its grouping instead of the mode, because the
 *  same layer regroups by platform, module or wave and those are different
 *  lists with different names. */
const sectionKey = (label) =>
  isTreeHead(label)
    ? `tree/${state.layer}/${groupBy()}/${label.textContent.trim().toLowerCase()}`
    : `${state.layer}/${state.mode}/${label.textContent.trim().toLowerCase()}`;

/** A section owns every sibling after its label, up to the next label. A
 *  sidebar group owns the rest of its container, which has no next label to
 *  stop at — the group element is the boundary. */
function sectionBody(label) {
  const out = [];
  for (
    let node = label.nextElementSibling;
    node && (isTreeHead(label) || !node.classList.contains('journey-section-label'));
    node = node.nextElementSibling
  ) out.push(node);
  return out;
}

function applyCollapse(label) {
  const shut = collapsedSections.has(sectionKey(label));
  label.classList.toggle('collapsed', shut);
  label.setAttribute('aria-expanded', String(!shut));
  if (!label.hasAttribute('tabindex')) {
    label.setAttribute('tabindex', '0');
    label.setAttribute('role', 'button');
  }
  const body = sectionBody(label);
  for (const node of body) node.hidden = shut;
  // A heading that hides nothing is not a control; say so rather than inviting
  // a click that does nothing.
  label.classList.toggle('empty-section', body.length === 0);
}

function toggleSection(label) {
  if (!sectionBody(label).length) return;
  const key = sectionKey(label);
  if (collapsedSections.has(key)) collapsedSections.delete(key);
  else collapsedSections.add(key);
  applyCollapse(label);
}

/** Re-applies the reader's choices to whatever a render just produced. */
function refreshSections(root = document) {
  for (const label of root.querySelectorAll(FOLD_HEADS)) applyCollapse(label);
}

function bindSections() {
  document.addEventListener('click', (event) => {
    const label = event.target.closest(FOLD_HEADS);
    if (label) toggleSection(label);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    const label = event.target.closest?.(FOLD_HEADS);
    if (!label) return;
    event.preventDefault();
    toggleSection(label);
  });

  // Panes re-render constantly and rebuild their DOM each time. Watching for
  // new labels keeps the collapse state without every render path having to
  // remember to ask for it.
  const observer = new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (node.nodeType !== 1) continue;
        if (node.matches?.(FOLD_HEADS)) applyCollapse(node);
        else if (node.querySelector?.(FOLD_HEADS)) refreshSections(node);
      }
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}

// ── accounts ────────────────────────────────────────────────────────
// The viewer reads without one. An account is needed to write a verdict,
// because a verdict is only worth having if it says who gave it.

function openAccountPanel() {
  $('account-panel').hidden = false;
  renderAccountPanel();
  const first = auth.account() ? null : $('signin-email');
  first?.focus();
}

function closeAccountPanel() {
  $('account-panel').hidden = true;
}

function renderAccountPanel() {
  const who = auth.account();
  const reachable = auth.reachable();

  $('account-offline').hidden = reachable;
  $('account-signin').hidden = Boolean(who) || !reachable;
  $('account-signed').hidden = !who;
  $('account-title').textContent = who ? 'Your account' : 'Sign in';

  if (who) {
    $('account-email').textContent = who.email;
    $('account-role-note').textContent = who.role === 'admin' ? ', an admin' : '';
    $('account-admin').hidden = who.role !== 'admin';
  }
}

/**
 * How many notes have named you, on the account button and on the link that
 * leads to them.
 *
 * The inbox itself lives on the review page, which is the right home for it —
 * it needs the note, the artefact and who wrote it, and none of that fits in a
 * topbar. But an inbox you only find by visiting the page it is on is not a
 * notification, so the count comes to you: the account button is on every
 * layer of the viewer and is the one thing always in view.
 *
 * Asked once per sign-in rather than polled. A mention arrives when somebody
 * types it, which is not often enough to be worth a timer, and the count is
 * re-read whenever the account panel is opened.
 */
let mentionCache = [];

async function showMentionCount() {
  const bell = $('bell-toggle');
  const link = $('mentions-link');
  if (!bell) return;

  let payload = null;
  try {
    payload = await auth.myMentions();
  } catch {
    return;                       // the viewer is not about this
  }
  mentionCache = payload.mentions ?? [];
  const unseen = payload.unseen ?? 0;

  // Shown once there is anything at all, read or unread — a bell that
  // disappears the moment you read the last note takes the history with it,
  // and "what did that say again" is a question people ask an hour later.
  bell.hidden = mentionCache.length === 0;
  bell.classList.toggle('has-mentions', unseen > 0);
  bell.title = unseen
    ? `${unseen} note${unseen === 1 ? '' : 's'} named you`
    : 'Where you were named';

  const count = $('bell-count');
  count.textContent = unseen > 9 ? '9+' : String(unseen);
  count.hidden = unseen === 0;

  if (link) {
    link.textContent = unseen ? `Review activity - ${unseen} named you` : 'Review activity';
    link.classList.toggle('auth-button-loud', unseen > 0);
  }
}

/** The panel behind the bell. Drawn from what the count already fetched, so
 *  opening it costs nothing and never shows a spinner over three rows. */
function renderBellPanel() {
  const list = $('bell-list');
  list.innerHTML = '';
  const unseen = mentionCache.filter((m) => !m.seen_at).length;
  $('bell-note').textContent = mentionCache.length
    ? (unseen ? `${unseen} unread of ${mentionCache.length}` : `${mentionCache.length}, all read`)
    : 'Nobody has named you yet.';
  $('bell-seen').hidden = unseen === 0;

  // Everything, not the newest eight. The list scrolls, so a cap here bought
  // nothing and cost the reader the difference between "that is all of them"
  // and "that is as many as this box felt like drawing".
  for (const m of mentionCache) {
    const row = el('div', `bell-row${m.seen_at ? '' : ' unread'}`);
    const head = el('div', 'bell-row-head');
    head.append(el('span', 'bell-who', m.by || m.by_email));
    const target = el('button', 'bell-target', m.target_id);
    target.type = 'button';
    // Goes to the thing rather than to a list of things, because the reason
    // somebody was named is always about one artefact.
    target.onclick = () => {
      closeBellPanel();
      location.hash = encodeURIComponent(
        m.target_kind === 'operation' ? m.target_id : `${m.target_kind}:${m.target_id}`);
    };
    head.append(target);
    row.append(head);
    row.append(auth.renderNote(m.note));
    list.append(row);
  }
}

function openBellPanel() {
  renderBellPanel();
  $('bell-panel').hidden = false;
  $('bell-toggle').setAttribute('aria-expanded', 'true');
}

function closeBellPanel() {
  $('bell-panel').hidden = true;
  $('bell-toggle').setAttribute('aria-expanded', 'false');
}

/** The initials in the topbar, and what the button says it is for. */
function renderAccountButton() {
  const who = auth.account();
  const badge = $('account-initials');
  const button = $('account-toggle');
  if (!badge || !button) return;

  if (!who) {
    badge.textContent = '·';
    button.classList.remove('signed-in');
    button.title = auth.reachable()
      ? 'Sign in to record verdicts'
      : 'The validation service is not running';
    return;
  }
  const source = (who.name || who.email).trim();
  const initials = source.includes(' ')
    ? source.split(/\s+/).slice(0, 2).map((w) => w[0]).join('')
    : source.slice(0, 2);
  badge.textContent = initials.toUpperCase();
  button.classList.add('signed-in');
  button.title = `${who.email} — ${who.role}`;
}

function bindAccountUI() {
  $('bell-toggle').onclick = () =>
    ($('bell-panel').hidden ? openBellPanel() : closeBellPanel());
  $('bell-panel').onclick = (e) => { if (e.target === $('bell-panel')) closeBellPanel(); };
  $('bell-seen').onclick = async () => {
    $('bell-seen').disabled = true;
    try {
      await auth.markMentionsSeen();
      for (const m of mentionCache) m.seen_at = m.seen_at ?? new Date().toISOString();
      renderBellPanel();
      showMentionCount();
    } finally {
      $('bell-seen').disabled = false;
    }
  };

  $('account-toggle').onclick = () =>
    ($('account-panel').hidden ? openAccountPanel() : closeAccountPanel());
  $('account-panel').onclick = (e) => { if (e.target === $('account-panel')) closeAccountPanel(); };
  // a verdict block asking for a sign-in
  document.addEventListener('ticvai:signin', openAccountPanel);

  const signInError = (message) => {
    $('signin-error').textContent = message;
    $('signin-error').hidden = false;
  };

  const doSignIn = async () => {
    $('signin-error').hidden = true;
    $('signin-submit').disabled = true;
    $('signin-submit').textContent = 'Signing in…';
    try {
      await auth.signIn($('signin-email').value.trim(), $('signin-password').value);
      $('signin-password').value = '';
      closeAccountPanel();
    } catch (error) {
      signInError(error.message);
    } finally {
      $('signin-submit').disabled = false;
      $('signin-submit').textContent = 'Sign in';
    }
  };

  $('signin-submit').onclick = doSignIn;
  for (const id of ['signin-email', 'signin-password']) {
    $(id).addEventListener('keydown', (e) => { if (e.key === 'Enter') doSignIn(); });
  }

  $('signout').onclick = async () => {
    await auth.signOut();
    closeAccountPanel();
  };

  auth.onAuthChange(() => {
    renderAccountButton();
    // The bell has to be told on sign-in, not on the first time somebody opens
    // the account panel. It was hanging off renderAccountPanel, which meant the
    // one control whose job is to tell you something unprompted only appeared
    // once you had gone looking — exactly the failure it exists to fix.
    if (auth.account()) showMentionCount();
    if (!$('account-panel').hidden) renderAccountPanel();
  });
  auth.refreshSession();
}

function bindUI() {
  // the layer and mode bars are rebuilt on every switch, so they wire
  // themselves in renderLayers / renderModes rather than here
  for (const button of $('graph-scope').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.scope === state.graphScope);
    button.onclick = () => {
      state.graphScope = button.dataset.scope;
      for (const other of $('graph-scope').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      syncGraphControls();
      renderGraph();
      setMode('graph');
    };
  }
  syncGraphControls();

  $('graph-labels').onchange = (e) => { graph.showLabels = e.target.checked; graph.draw(); };
  $('graph-recenter').onclick = () => { graph.resize(); graph.recenter(); };
  $('graph-shared').onchange = () => renderGraph();

  $('states-scope').onchange = (e) => {
    state.machineId = e.target.value;
    state.stateName = null;
    machine.userAdjusted = false;
    renderStates();
  };
  $('states-guards').onchange = (e) => {
    machine.showGuards = e.target.checked;
    machine.draw();
  };
  $('states-fit').onclick = () => { machine.resize(); machine.fit(); };
  $('events-scope').onchange = (e) => {
    state.eventId = e.target.value === ALL_EVENTS ? null : e.target.value;
    renderEvents();
  };

  $('side-filter').oninput = (e) => {
    state.sideFilter = e.target.value.trim().toLowerCase();
    renderTree();
  };

  $('er-scope').onchange = (e) => {
    state.erScope = e.target.value;
    er.userAdjusted = false;
    renderER();
  };
  $('journey-scope').onchange = (e) => {
    state.journeyId = e.target.value;
    renderJourney();
  };
  $('journey-branches').onchange = () => renderJourney();
  $('journey-ops').onchange = () => renderJourney();

  $('screen-scope').onchange = (e) => {
    const [kind, ...rest] = e.target.value.split(':');
    const id = rest.join(':');
    if (kind === 'board') selectBoard(id, { open: false });
    else selectScreen(id, { open: false });
  };
  $('screen-notes').onchange = () => renderScreen();

  // ---- the three views the handoff joins made possible -------------------
  for (const button of $('lineage-scope').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.scope === state.lineageScope);
    button.onclick = () => {
      state.lineageScope = button.dataset.scope;
      for (const other of $('lineage-scope').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderLineage();
    };
  }
  $('lineage-filter').oninput = (e) => { state.lineageFilter = e.target.value; renderLineage(); };
  $('lineage-unresolved').onchange = (e) => {
    state.lineageUnresolved = e.target.checked;
    renderLineage();
  };

  $('waves-unbuilt').onchange = (e) => { state.wavesUnbuilt = e.target.checked; renderWaves(); };
  $('waves-offline').onchange = (e) => { state.wavesOffline = e.target.checked; renderWaves(); };

  for (const button of $('decisions-scope').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.scope === state.decisionsScope);
    button.onclick = () => {
      state.decisionsScope = button.dataset.scope;
      for (const other of $('decisions-scope').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderDecisions();
    };
  }
  $('decisions-filter').oninput = (e) => { state.decisionsFilter = e.target.value; renderDecisions(); };

  // ── the four decision views ──────────────────────────────────────
  for (const button of $('timeline-scope').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.scope === state.timelineScope);
    button.onclick = () => {
      state.timelineScope = button.dataset.scope;
      for (const other of $('timeline-scope').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderTimeline();
    };
  }
  $('timeline-filter').oninput = (e) => { state.timelineFilter = e.target.value; renderTimeline(); };

  $('supersession-all').onchange = (e) => {
    state.supersessionAll = e.target.checked;
    renderSupersession();
  };

  $('register-pick').onchange = (e) => {
    state.registerId = e.target.value;
    // The state filter belongs to the conflicts register and means nothing on
    // any other, so it is dropped rather than carried across and silently
    // matching nothing.
    state.registerState = '';
    renderRegister();
  };
  $('register-filter').oninput = (e) => { state.registerFilter = e.target.value; renderRegister(); };

  $('decision-pick').onchange = (e) => { state.adrId = e.target.value; renderDecision(); };

  $('data-scope').onchange = (e) => {
    state.dataModule = e.target.value;
    data.userAdjusted = false;
    renderData();
    data.resize();
    data.fit();
    // Changing the scope changes what the rail is about — it now describes a
    // different schema, or none. Without this the rail kept describing the
    // schema that was scoped when it was last drawn.
    if (!state.tableName) fillSidePane();
  };
  $('data-anchor').onchange = (e) => {
    state.dataAnchor = e.target.value || null;
    if (!state.dataAnchor) state.dataAnchorOnly = false;
    data.userAdjusted = false;
    renderData();
    data.resize();
    data.fit();
    fillSidePane();
  };
  $('data-anchor-only').onchange = (e) => {
    state.dataAnchorOnly = e.target.checked;
    data.userAdjusted = false;
    renderData();
    data.resize();
    data.fit();
  };

  $('data-rows').onchange = (e) => {
    state.dataRows = e.target.checked;
    data.showRows = state.dataRows;
    data.draw();
  };
  $('data-inferred').onchange = () => {
    data.userAdjusted = false;
    renderData({ focus: state.tableName });
  };
  $('data-ambient').onchange = () => {
    data.userAdjusted = false;
    renderData({ focus: state.tableName });
  };
  $('data-fit').onclick = () => { data.resize(); data.fit(); };

  $('er-rows').onchange = (e) => { er.showRows = e.target.checked; er.draw(); };
  $('er-fit').onclick = () => { er.resize(); er.fit(); };

  for (const button of $('struct-layout').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.layout === tree.layoutMode);
    button.onclick = () => {
      tree.layoutMode = button.dataset.layout;
      for (const other of $('struct-layout').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      // relayout for the new mode before anything can draw with stale entries
      tree.layout();
      tree.resize();
      if (tree.selectedPath && tree.byPath.has(tree.selectedPath)) {
        tree.fit();
        tree.focusPath(tree.selectedPath, { zoom: Math.max(tree.transform.k, 0.7) });
      } else {
        tree.fit();
      }
    };
  }

  $('struct-fields').onchange = (e) => {
    tree.showFields = e.target.checked;
    tree.layout();
    tree.fit();
  };
  $('struct-links').onchange = (e) => { tree.showLinks = e.target.checked; tree.draw(); };
  $('struct-expand').onclick = () => tree.expandAll();
  $('struct-collapse').onclick = () => tree.collapseAll();
  // the explicit button really does fit everything, however small that gets
  $('struct-fit').onclick = () => { tree.resize(); tree.fit({ min: 0.05 }); };
  $('struct-filter').oninput = (e) => {
    tree.filter = e.target.value.trim().toLowerCase();
    // a filter is only useful if the matches are actually unfolded
    if (tree.filter) tree.collapsed.clear();
    tree.layout();
    tree.fit();
    const shown = tree.visible.length;
    $('struct-hint').textContent = tree.filter
      ? `${shown} node${shown === 1 ? '' : 's'} match "${tree.filter}"`
      : '';
  };
  $('search-trigger').onclick = openPalette;

  // ── drawers ───────────────────────────────────────────────────────
  $('drawer-left-toggle').onclick = () => setDrawer(state.drawer === 'left' ? null : 'left');
  $('drawer-right-toggle').onclick = () => setDrawer(state.drawer === 'right' ? null : 'right');
  $('drawer-backdrop').onclick = () => setDrawer(null);

  // Picking something in the tree is the whole reason the drawer was opened,
  // so get out of the way of the answer. A row that only discloses its
  // children has not answered anything yet, so it stays.
  $('tree').addEventListener('click', (event) => {
    if (!state.drawer) return;
    const row = event.target.closest('.tree-child, .tree-file');
    if (!row) return;
    const discloses = row.nextElementSibling?.classList.contains('tree-children');
    if (!discloses) setDrawer(null);
  });

  $('palette-input').oninput = (e) => runSearch(e.target.value);
  $('palette').onclick = (e) => { if (e.target === $('palette')) closePalette(); };

  $('theme-toggle').onclick = () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('ticvai-theme', next);
    // colour dots are inline styles, so anything already painted must repaint
    renderTree();
    renderLegend();
    const selected = state.selectedId && state.nodesById.get(state.selectedId);
    if (selected) renderLinksPane(selected);
    renderStructLegend();
    graph.draw();
    tree.draw();
    er.draw();
    data.draw();
  };

  const saved = localStorage.getItem('ticvai-theme');
  if (saved) document.documentElement.dataset.theme = saved;

  window.addEventListener('keydown', (e) => {
    const inPalette = !$('palette').hidden;

    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      inPalette ? closePalette() : openPalette();
      return;
    }

    if (inPalette) {
      if (e.key === 'Escape') { e.preventDefault(); closePalette(); }
      else if (e.key === 'ArrowDown') {
        e.preventDefault();
        paletteActive = Math.min(paletteItems.length - 1, paletteActive + 1);
        renderPalette($('palette-input').value.trim().toLowerCase());
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        paletteActive = Math.max(0, paletteActive - 1);
        renderPalette($('palette-input').value.trim().toLowerCase());
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const node = paletteItems[paletteActive];
        if (node) { select(node.id); setMode('reader'); closePalette(); }
      }
      return;
    }

    // before the input guard below: escape has to work from the tree's own
    // filter box, which is the field most likely to have focus inside a drawer
    if (e.key === 'Escape' && state.drawer) {
      e.preventDefault();
      setDrawer(null);
      return;
    }

    // Single letters pick a view, so they must not fire while someone is
    // writing. TEXTAREA belongs here as much as INPUT: without it, typing the
    // "e" of a word in the verdict note jumped to the ER view and took the
    // focus with it, losing the rest of the sentence. contenteditable is
    // included for the same reason, before something here becomes one.
    const target = e.target;
    if (
      target.tagName === 'INPUT' ||
      target.tagName === 'SELECT' ||
      target.tagName === 'TEXTAREA' ||
      target.isContentEditable
    ) return;

    // 1 / 2 / 3 pick the layer, in the order they appear in the bar
    const layerIndex = Number(e.key) - 1;
    if (layerIndex >= 0 && layerIndex < LAYERS.length) {
      setLayer(LAYERS[layerIndex].key);
      return;
    }

    if (e.key === 'm') {
      // cycle how the left pane groups, within whatever this layer offers
      const options = layerOf(state.layer).groups.map(([key]) => key);
      state.groupBy[state.layer] = options[(options.indexOf(groupBy()) + 1) % options.length];
      for (const other of $('group-by').querySelectorAll('button')) {
        other.classList.toggle('active', other.dataset.group === groupBy());
      }
      renderSideNote();
      renderTree();
    } else if (e.key === 'g') setMode('graph');
    else if (e.key === 's') setMode('structure');
    else if (e.key === 'e') setMode('er');
    else if (e.key === 'j') setMode('journey');
    else if (e.key === 'w') setMode('screen');
    else if (e.key === 'p') setMode('apps');
    else if (e.key === 'd') setMode('data');
    else if (e.key === 'v') setMode('migrations');
    else if (e.key === 'o') setMode('routing');
    else if (e.key === 'r') setMode('reader');
    else if (e.key === 'a') setMode('audit');
    else if (e.key === 'l' && state.selectedId) {
      state.graphScope = 'local';
      for (const b of $('graph-scope').querySelectorAll('button')) {
        b.classList.toggle('active', b.dataset.scope === 'local');
      }
      renderGraph();
      setMode('graph');
    }
  });
}

boot();
