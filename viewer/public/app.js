import { Graph, colorForNode, colorForLink } from './graph.js';
import { StructureTree, kindColor } from './structure.js';
import { BoxDiagram } from './boxdiagram.js';
import { StateMachine } from './statemachine.js';
import { Galaxy, galaxyLegend } from './galaxy.js';
import { installTips, tip, tipFor } from './tips.js';
import * as auth from './validation.js';
import { hideLoader, loaderSays } from './loader.js';
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
  hue, markdownBlock,
} from './core.js';
// ── boot ─────────────────────────────────────────────────────────────
let graph;
let tree;
let er;
let serviceEr;   // the same renderer again, with services as the entities
let servicesGalaxy;
let data;
let machine;
let eventGalaxy; // the outbox, as contexts and the traffic between them
let dataGalaxy;  // the database, as schemas over their tables
let graphGalaxy; // the Spine, Schemas and Permissions scopes of the contract graph
let lineageGalaxy; // services against the tables they touch
let appsGalaxy;  // the apps against the contracts their screens call

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

  // The services as a field. A body is a service, and the two things a reader
  // wants of an architecture before reading a word of it — which are the big
  // ones, and which are written into by everything — are size and position.
  servicesGalaxy = new Galaxy($('services-galaxy'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        servicesGalaxy.setSelected(hub.id === servicesGalaxy.selectedId ? null : hub.id);
        selectService(hub.key);
        $('services-graph-hint').textContent = describeServiceHub(hub);
        return;
      }
      // Fly into it rather than cut: the field and the service page are the
      // same claim at different magnification, and a cut hides that.
      servicesGalaxy.warpInto(hub.id, () => { selectService(hub.key); setMode('service'); });
    },
    onHover: (hub) => {
      $('services-graph-hint').textContent = hub ? describeServiceHub(hub) : servicesGalaxySummary;
    },
  });

  // The third box diagram: the same renderer again, with services as the
  // entities. A service is a bigger thing than a schema or a table, and the
  // relationships between them are the same kind of fact, so it is the same
  // picture at another altitude rather than a new idea.
  serviceEr = new BoxDiagram($('er-services-canvas'), {
    onSelect: (node) => { selectService(node.id.replace(/^service:/, '')); },
    onRow: (row) => { if (row.refTarget) openSchemaModule(row.refTarget); },
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

  // The outbox drawn rather than listed. A single click pins a context and
  // says what it does; a double click leaves for its contract, because a graph
  // that navigates away on one click cannot be explored.
  eventGalaxy = new Galaxy($('events-canvas'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        eventGalaxy.setSelected(hub.id === eventGalaxy.selectedId ? null : hub.id);
        $('events-hint').textContent = describeContext(hub);
        return;
      }
      const node = hub.context?.contract
        ? state.nodesById.get(`file:${hub.context.contract}`)
        : null;
      if (node) { select(node.id); setLayer('contracts'); setMode('reader'); }
      else toast(`${hub.name} is not a contract in this package`);
    },
    onHover: (hub) => {
      $('events-hint').textContent = hub ? describeContext(hub) : eventGalaxySummary;
    },
  });

  // The database as bodies rather than boxes. Clicking drills: a schema opens
  // to its own tables, and a table opens in the ER view, where the columns are.
  dataGalaxy = new Galaxy($('data-galaxy'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        dataGalaxy.setSelected(hub.id === dataGalaxy.selectedId ? null : hub.id);
        $('data-hint').textContent = describeDataHub(hub);
        return;
      }
      // Fly into it. The two pictures are the same claim at different
      // magnification and a cut is the one thing that hides that.
      if (hub.module) dataGalaxy.warpInto(hub.id, () => openSchema(hub.module));
      // `selectTable` owns the switch into the ER view — setting the layout
      // here and leaving it to redraw was how this landed on a hidden canvas.
      else if (hub.table) selectTable(hub.table);
    },
    onHover: (hub) => {
      $('data-hint').textContent = hub ? describeDataHub(hub) : dataGalaxySummary;
    },
  });

  // Two of the five graph scopes are the ones a force simulation cannot hold:
  // 714 schemas is a hairball, and 141 permissions against 30 contracts is a
  // join rather than a network. Both get the field instead.
  graphGalaxy = new Galaxy($('graph-galaxy'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        graphGalaxy.setSelected(hub.id === graphGalaxy.selectedId ? null : hub.id);
        $('graph-hint').textContent = describeGraphHub(hub);
        return;
      }
      if (state.nodesById.has(hub.id)) { select(hub.id); setMode('reader'); }
      else toast(`${hub.name} is not a node in the index`);
    },
    onHover: (hub) => {
      $('graph-hint').textContent = hub ? describeGraphHub(hub) : graphGalaxySummary;
    },
  });

  // The one join the package cannot derive for itself, drawn as a join.
  appsGalaxy = new Galaxy($('apps-galaxy'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        appsGalaxy.setSelected(hub.id === appsGalaxy.selectedId ? null : hub.id);
        $('apps-hint').textContent = describeAppsHub(hub);
        return;
      }
      // A contract is a node the rest of the viewer knows about; an app is not,
      // so opening one is the most it can say about itself.
      if (hub.contractFile) select(hub.id);
      else toast(`${hub.full ?? hub.name} builds ${hub.mass} screens across ${hub.contracts} contracts`);
    },
    onHover: (hub) => {
      $('apps-hint').textContent = hub ? describeAppsHub(hub) : appsGalaxySummary;
    },
  });

  lineageGalaxy = new Galaxy($('lineage-galaxy'), {
    onSelect: (hub, { open }) => {
      if (!open) {
        lineageGalaxy.setSelected(hub.id === lineageGalaxy.selectedId ? null : hub.id);
        $('lineage-hint').textContent = describeLineageHub(hub);
        return;
      }
      if (hub.table) selectTable(hub.table);
      else toast(`${hub.full ?? hub.name} owns ${hub.weight} table${hub.weight === 1 ? '' : 's'}`);
    },
    onHover: (hub) => {
      $('lineage-hint').textContent = hub ? describeLineageHub(hub) : lineageGalaxySummary;
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
  window.__galaxy = eventGalaxy;
  window.__dataGalaxy = dataGalaxy;
  window.__graphGalaxy = graphGalaxy;
  window.__lineageGalaxy = lineageGalaxy;
  window.__appsGalaxy = appsGalaxy;
  window.__state = state;

  // The viewer is behind a sign-in. Ask before fetching two megabytes that a
  // stranger is not going to be shown, and send them where they can do
  // something about it — carrying where they were headed, so a link into a
  // particular node still lands there afterwards.
  const signedIn = await auth.requireSignIn();
  // The curtain comes down either way. Signed out, requireSignIn is already
  // navigating to the door, and a redirect that leaves a loading screen up
  // behind it looks like the redirect is what stalled.
  if (!signedIn) { hideLoader(); return; }

  loaderSays('Reading the contracts, screens and state models…');
  // Where the reader is going is in the address, and the address is readable
  // before anything has been fetched. Handing it to loadIndex starts that
  // layer's parts beside the index rather than after it — on Frontend, 430K
  // that used to begin only once 171K had arrived and been parsed.
  await loadIndex(layerFromUrl());
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
  // Where the landing page sends a reader. A layer and optionally one of its
  // views — `setMode` already follows a view to whichever layer owns it, so a
  // view on its own is enough and the layer is the fallback for "just open it".
  const query = new URLSearchParams(location.search);
  const wantLayer = query.get('layer');
  const wantMode = query.get('mode');
  // Written by syncUrl on the way out, so a refresh comes back to the same
  // scope rather than to the default one with the same view around it.
  const wantScope = query.get('scope');
  if (wantScope) state.graphScope = wantScope;
  const mayOpen = (key) =>
    LAYERS.some((l) => l.key === key)
    && (!state.session?.layers || state.session.layers.includes(key));
  // Which layer a view belongs to.
  //
  // A named layer decides it. Searching every layer for whoever owns the view
  // name answers the wrong question the moment the address has already said
  // where to be: `audit` is a view on four layers and `graph` on one, so
  // `?layer=backend&mode=audit` opened Frontend's audit and
  // `?layer=domain&mode=graph` opened Contracts. The layer names a place; the
  // view names what to do there; the place wins.
  //
  // A named layer that does not have the view leaves this null, and the branch
  // below opens that layer at its own first view — still where they asked to
  // be. Only with no layer named does the view name its own owner, which is
  // what lets a view on its own be a complete address.
  const named = LAYERS.find((l) => l.key === wantLayer) ?? null;
  const owner = !wantMode ? null
    : named ? (named.modes.some(([m]) => m === wantMode) ? named : null)
    : LAYERS.find((l) => l.modes.some(([m]) => m === wantMode));

  // The layer has to be set before the view, and cannot be left to `setMode`.
  // `setMode` only walks to another layer when the one it is standing in does
  // not have the view — which is right for a keyboard shortcut and wrong here:
  // the app boots on Contracts, Contracts has an `audit`, so `?layer=backend&
  // mode=audit` found its view already underfoot and never moved.
  const goTo = (layer, mode) => {
    if (layer.key !== state.layer) setLayer(layer.key);
    setMode(mode);
  };

  if (fromHash && state.nodesById.has(fromHash)) {
    select(fromHash);
    // A hash with a view beside it is a refresh, and the view is where they
    // were. A hash on its own is a link somebody pasted, where the id is the
    // whole message — and the view that answers "show me this node" is the
    // Reader, not whichever graph the app happens to open on.
    if (owner && mayOpen(owner.key)) goTo(owner, wantMode);
    else setMode(state.mode === 'graph' ? 'reader' : state.mode);
  } else if (fromHash && (await openArtefactHash(fromHash))) {
    // handled — a screen, table or board rather than a contract node
  } else if (owner && mayOpen(owner.key)) {
    goTo(owner, wantMode);
  } else if (mayOpen(wantLayer)) {
    setLayer(wantLayer);
    setMode(layerOf(wantLayer).modes[0][0]);
  } else {
    setMode('graph');
  }

  // From here the address follows the reader instead of leading them.
  urlLive = true;
  syncUrl();

  // Everything the other layers need, fetched while nobody is waiting for it,
  // so the second click has nothing left to load. At idle rather than on a
  // timer, so it yields to whatever the reader is doing; one at a time rather
  // than all at once, so six downloads do not compete with the diagram in front
  // of them; and smallest first, so the cheap layers are ready soonest.
  prefetchRemainingParts();



  // The layer the app opens on never went through setLayer, so nothing has
  // asked for its parts yet.
  hydrateLayer();

  // The head set `data-entry` before anything painted; this takes it off once
  // the last piece has landed, so none of it is live during use. The field it
  // paints goes with it, which is right: by then the chrome is in place and the
  // views own their own backgrounds again.
  if (document.documentElement.dataset.entry) {
    setTimeout(() => { delete document.documentElement.dataset.entry; }, 1300);
  }

  // Last, and only here: everything above it is what the curtain was covering.
  // A no-op on an arrival from the door, where there was never a curtain.
  hideLoader();
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

/**
 * How much each layer holds, for the count inside its pill.
 *
 * Which layer is the big one is a thing worth knowing *before* you open it —
 * the tray used to be five equal words, and "Decisions" reading the same
 * weight as "Contracts" when one is 18 documents and the other 364 operations
 * is the tray failing to say the only thing it is well placed to say.
 *
 * Everything here is already loaded by the time the tray is drawn; a layer
 * whose payload has not arrived yet simply carries no count rather than a
 * zero, because zero is a claim and "not yet" is not.
 */
function layerCount(key) {
  const nodes = state.index?.nodes ?? [];
  switch (key) {
    case 'frontend': return state.journeys?.screens?.length ?? null;
    case 'contracts': return nodes.filter((n) => n.type === 'operation').length || null;
    case 'domain': return state.domain?.machines?.length ?? null;
    case 'backend': return state.backend?.tables?.length ?? null;
    // Designs, not services. Every other tab here counts what its layer is
    // made of; this one counted the subject of one of its nine views while the
    // folder behind it held 177 files.
    case 'services': {
      const dia = state.diagrams;
      if (!dia?.present) return null;
      const subjects = ['platform', 'hierarchy', 'contracts', 'lifecycles']
        .filter((k) => dia[k]?.present).length + 1;
      const detail = Object.values(dia.lld ?? {}).reduce((a, list) => a + list.length, 0);
      return subjects + detail || null;
    }
    case 'decisions': return state.decisions?.adrs?.length ?? null;
    default: return null;
  }
}

/**
 * Fill the counts back in as their payloads arrive.
 *
 * Each layer fetches its own data the first time it is opened, so at boot only
 * the layer you land on can answer for itself. Rather than draw a zero — which
 * is a claim, where "not yet" is not — the pill starts bare and gains its count
 * the moment the number becomes true. Updated in place so the tray never
 * reflows under the pointer.
 */
function refreshLayerCounts() {
  for (const button of $('layers').querySelectorAll('button')) {
    const count = layerCount(button.dataset.layer);
    const span = button.querySelector('.layer-count');
    if (count == null) { span?.remove(); continue; }
    if (span) span.textContent = String(count);
    else button.append(el('span', 'layer-count', String(count)));
  }
}

function renderLayers() {
  const bar = $('layers');
  bar.innerHTML = '';
  document.body.dataset.layer = state.layer;
  visibleLayers().forEach((layer, index) => {
    const button = el('button', null, layer.label);
    button.dataset.layer = layer.key;
    button.title = layer.hint;
    tip(button, layer.label, layer.tip ?? layer.hint);
    const count = layerCount(layer.key);
    if (count != null) button.append(el('span', 'layer-count', String(count)));
    button.classList.toggle('active', layer.key === state.layer);
    button.onclick = () => setLayer(layer.key);
    bar.append(button);
  });
  renderModes();
}

/**
 * The keys the view tabs answer to: the top row, left to right, matched to the
 * tabs left to right.
 *
 * Positional rather than mnemonic, and the trade is deliberate. A mnemonic set
 * has to be unique across every view in the package, so it drifts away from the
 * word it stands for as the list grows — Waves was V, Migrations was M until
 * Modules wanted M, and Screen was W because S had gone to Structure. A reader
 * cannot guess any of those. This set is guessable from the shape of the tab
 * bar alone: fourth tab, fourth key.
 *
 * They are read against the current layer, so the same key means the fourth tab
 * of whatever page you are on. Ten is well past the six the longest layer has;
 * the surplus is headroom, not a plan.
 */
const MODE_ROW = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'];

/**
 * The layer bar answers to 1, 2, 3 in the order it draws them, and says so
 * nowhere. That row is the first thing anybody sees and the one place the
 * package should look like a document rather than a tool — a digit in a box
 * beside every name is five pieces of furniture bought to solve a problem the
 * view tabs already solve, since anyone who has met Q there will try 1 here.
 */

function renderModes() {
  const bar = $('modes');
  bar.innerHTML = '';
  visibleModes(layerOf(state.layer)).forEach(([key, label], index) => {
    const button = el('button', 'mode', label);
    button.dataset.mode = key;
    button.classList.toggle('active', key === state.mode);
    const about = MODE_TIPS[key];
    if (about) tip(button, about.title, about.body);
    // The shortcut is already bound; printing it on the tab is what turns it
    // from a thing in the manual into a thing people use. Taken from the
    // position rather than the name, so the printed key and the bound key
    // cannot disagree — they are the same index into the same row.
    const hint = MODE_ROW[index];
    if (hint) button.append(el('kbd', 'mode-key', hint.toUpperCase()));
    if (key === 'audit') {
      const badge = el('span', 'audit-count');
      badge.id = 'audit-count';
      button.append(' ', badge);
    }
    button.onclick = () => setMode(key);
    bar.append(button);
  });
  updateAuditBadge();
  renderLayerSummary();
}

/**
 * The one-line count of what this layer holds, in the second chrome row.
 *
 * The left column already spells this out in its advisory note, but that note
 * is below the fold on a short window and is about a caveat rather than a
 * size. This answers "how much is here" before anybody scrolls to find out.
 */
function renderLayerSummary() {
  const out = $('layer-summary');
  if (!out) return;
  const parts = [];
  if (state.layer === 'frontend') {
    const screens = state.journeys?.screens?.length ?? 0;
    const platforms = state.journeys?.allPlatforms?.length ?? 0;
    if (screens) parts.push(`${screens} screens`);
    if (platforms) parts.push(`${platforms} platforms`);
  } else if (state.layer === 'contracts') {
    const nodes = state.index?.nodes ?? [];
    const files = nodes.filter((n) => n.type === 'file').length;
    const ops = nodes.filter((n) => n.type === 'operation').length;
    if (files) parts.push(`${files} contracts`);
    if (ops) parts.push(`${ops} operations`);
  } else if (state.layer === 'domain') {
    const machines = state.domain?.machines?.length ?? 0;
    const events = state.domain?.events?.length ?? 0;
    if (machines) parts.push(`${machines} state models`);
    if (events) parts.push(`${events} events`);
  } else if (state.layer === 'backend') {
    const tables = state.backend?.tables?.length ?? 0;
    if (tables) parts.push(`${tables} tables`);
  } else if (state.layer === 'decisions') {
    const adrs = state.decisions?.adrs?.length ?? 0;
    if (adrs) parts.push(`${adrs} decisions`);
  }
  out.textContent = parts.join(' · ');
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
  // `diagrams` for the fifteen platform designs, which are this layer's own
  // subject and happen to live in the diagrams payload.
  frontend: ['journeys', 'lineage', 'diagrams'],
  // the spine graph draws one edge per pair of contracts that share an event,
  // and the events are in the domain part — so contracts needs it too.
  // `diagrams` is the contracts HLD, which is a diagram of this layer's own
  // subject rather than of the architecture.
  contracts: ['lineage', 'domain', 'diagrams'],
  backend: ['backend', 'lineage'],
  // `diagrams` for the lifecycles HLD, same reason as contracts: the design of
  // this layer's subject happens to live in the diagrams payload.
  domain: ['domain', 'diagrams'],
  decisions: ['decisions'],
  // The map checks its own table counts against the workbook, so it needs the
  // backend part to draw honestly rather than merely to draw.
  services: ['diagrams', 'backend'],
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
  services: ['journeys'],             // service pane: the screens and flows it names
};

const ALL_PARTS = ['journeys', 'backend', 'domain', 'lineage', 'decisions', 'diagrams'];

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

  const request = auth.apiFetch(`/api/detail?file=${encodeURIComponent(file)}`)
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

/**
 * The layer the address asks for, before any of it has been fetched.
 *
 * A view names its own layer, so `?mode=screen` is as good an answer as
 * `?layer=frontend`; a named layer wins, which is the same precedence the boot
 * below applies once the index is in hand. Wrong is cheap here — it costs one
 * part fetched early that turns out not to be wanted — so this deliberately
 * does not try to reproduce the whole of that reasoning.
 */
function layerFromUrl() {
  const query = new URLSearchParams(location.search);
  const named = query.get('layer');
  if (named && LAYERS.some((l) => l.key === named)) return named;
  const mode = query.get('mode');
  return LAYERS.find((l) => l.modes.some(([m]) => m === mode))?.key ?? null;
}

const partInFlight = new Map();

/** Fetches one part once, no matter how many views ask for it at the time. */
function loadPart(key) {
  if (state[key]) return Promise.resolve(state[key]);
  if (partInFlight.has(key)) return partInFlight.get(key);
  const request = auth.apiFetch(`/api/${key}`)
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

/**
 * The four the app cannot start without, fetched together.
 *
 * None of them reads any of the others — `tooltips` is hover text, `domains` is
 * the lens membership every tree marks against, `session` decides which tabs are
 * drawn, and the index is the graph everything resolves into. They were four
 * awaits in a row, which is four round trips before a byte of the index is
 * parsed: invisible on a workstation, four times the latency on a deployment.
 *
 * `openTo` is the layer the address asks for, and its parts are started here
 * too. `loadPart` dedupes in flight, so the view that asks for them a moment
 * later joins this request rather than making a second one.
 */
/**
 * The parts no view has asked for yet, fetched at idle after the first paint.
 *
 * Ordered smallest first — measured gzipped, `diagrams` is 67K and `journeys` is
 * 250K — so the layers that are cheap to make ready are ready first. Serial on
 * purpose: the point is to use the time a reader spends looking at the view they
 * asked for, not to compete with it for bandwidth.
 *
 * Anything already in hand or in flight is skipped by `loadPart` itself, so this
 * needs no bookkeeping of its own and cannot double-fetch what the boot started.
 */
const PART_ORDER = ['domains', 'diagrams', 'domain', 'lineage', 'decisions', 'backend', 'journeys'];

function prefetchRemainingParts() {
  const allowed = new Set(state.session?.layers ?? LAYERS.map((l) => l.key));
  const wanted = new Set();
  for (const [layer, parts] of Object.entries(LAYER_PARTS)) {
    if (!allowed.has(layer)) continue;
    for (const key of parts) wanted.add(key);
  }
  const queue = PART_ORDER.filter((k) => wanted.has(k) && !state[k]);
  const idle = window.requestIdleCallback ?? ((fn) => setTimeout(fn, 400));
  const next = () => {
    const key = queue.shift();
    if (!key) return;
    // Still missing? A layer the reader opened in the meantime may have taken
    // it already, and re-asking would be a second request for the same bytes.
    if (state[key]) return next();
    loadPart(key).then(() => idle(next), () => idle(next));
  };
  idle(next);
}

async function loadIndex(openTo = null) {
  const sessionP = auth.apiFetch('/api/session').then((r) => r.json()).catch(() => null);
  const indexP = auth.apiFetch('/api/index').then((r) => r.json());
  const tooltipsP = auth.apiFetch('/api/tooltips').then((r) => r.json()).catch(() => null);
  const domainsP = auth.apiFetch('/api/domains').then((r) => r.json()).catch(() => null);

  // Started as soon as the session says it is allowed — a microtask, not a round
  // trip, since the session is already in flight beside the index. The check is
  // there so a reader who may not open a layer does not fetch it: the 403 would
  // be caught, cached as null, and leave a part that looks loaded and is empty.
  sessionP.then((who) => {
    if (!openTo || !LAYER_PARTS[openTo]) return;
    if (who?.layers && !who.layers.includes(openTo)) return;
    for (const key of LAYER_PARTS[openTo]) loadPart(key);
  });

  state.session = await sessionP;
  if (state.session?.layers && !state.session.layers.includes(state.layer)) {
    state.layer = state.session.layers[0];
  }

  // The index is the one part nothing can be drawn without: the tree, the
  // graph and every selection resolve against it.
  const index = await indexP;
  state.index = index;
  state.journeys = null;
  state.backend = null;
  state.domain = null;
  state.lineage = null;
  state.decisions = null;

  // Small, and read by every layer's hover text, so it is not worth deferring.
  // In flight since the top of this function, so this await is already settled.
  state.tooltips = await tooltipsP;

  // The domain lenses. Every layer's tree marks its members, so this cannot be
  // a per-layer part — and at 3 KB gzipped it does not want to be. `byArtefact`
  // is already keyed `kind:id`, which is what a tree row asks with.
  state.domains = await domainsP;
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
  if (key === 'services') return state.diagrams?.problems ?? [];
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
/**
 * Off until the restore below has read the address, so the first setMode of the
 * session cannot overwrite the thing it is about to be restored from.
 */
let urlLive = false;

/**
 * Keep the query in step with the position. replaceState rather than pushState:
 * switching views is not navigation, and a Back that stepped through every view
 * a reader had glanced at would never reach the page they came from.
 *
 * The hash is left exactly as it is — it belongs to the selection and has its
 * own listener.
 */
function syncUrl() {
  if (!urlLive) return;
  const query = new URLSearchParams();
  // First, and always: a deep link that loses the project is a link to whatever
  // the reader who opens it happens to have been looking at last.
  if (auth.project()) query.set('project', auth.project());
  query.set('layer', state.layer);
  query.set('mode', state.mode);
  // Only where it means something. A scope on the address in a view that has
  // no scopes is noise a reader will copy into a link and wonder about.
  if (state.mode === 'graph') query.set('scope', state.graphScope);
  history.replaceState(null, '', `${location.pathname}?${query}${location.hash}`);
}

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
  // Here rather than at the end: the galaxy scopes and the data view both
  // return early further down, and a position recorded only on the paths that
  // fall through is worse than one never recorded at all.
  syncUrl();
  // whatever asked for this view — a mode button, a tree row, a search hit —
  // the point was to look at it, so nothing may be left covering it
  setDrawer(null);
  for (const view of VIEWS) $(`view-${view}`).hidden = view !== mode;
  for (const button of $('modes').querySelectorAll('.mode')) {
    button.classList.toggle('active', button.dataset.mode === mode);
  }
  revealActive($('modes'));
  // by the time a view has been asked for, its layer's payload is either here
  // or on its way; either way the tray and the summary want re-reading
  queueMicrotask(() => { refreshLayerCounts(); renderLayerSummary(); });
  if (mode === 'graph') {
    // A galaxy scope parks its frame loop when the view goes away, so coming
    // back has to ask for it again — and the force renderer is not drawing at
    // all in those scopes, so reheating it would be reheating an empty graph.
    if (GALAXY_SCOPES.has(state.graphScope)) {
      graphGalaxy.start();
      graphGalaxy.draw();
      return;
    }
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
    if (state.dataLayout === 'galaxy') {
      renderDataGalaxy();
      return;
    }
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
  // The galaxy parks its own frame loop when its canvas goes off screen, so
  // coming back has to start it again. renderEvents does that.
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
  // The galaxy parks its own frame loop when its canvas goes off screen, so
  // coming back has to start it again. renderServicesGalaxy does that.
  if (mode === 'services-graph') renderServicesGalaxy();

  if (mode === 'er-services') {
    // measured 0x0 while hidden, like every other canvas here
    serviceEr.resize();
    if (!serviceEr.nodes.length) renderServiceEr();
    else if (!serviceEr.userAdjusted) serviceEr.fit();
  }
  if (mode === 'service') renderService();
  if (mode === 'platform-lld') renderPlatformLld();
  if (mode === 'contracts-hld') renderContractsHld();
  if (mode === 'lifecycles-hld') renderLifecyclesHld();
  if (mode === 'overview') renderOverview();
  if (mode === 'hierarchy') renderHierarchy();
  if (mode === 'hld') renderHld();
  if (mode === 'deploy') renderDeploy();
  if (mode === 'context') renderContext();
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
  if (state.layer === 'services') return renderServiceTree();
  return renderContractTree();
}

/**
 * The services, by tier or by size.
 *
 * By tier is the default because the tier is the only grouping that carries an
 * argument: it is what decides deploy order and what may be down. By size is
 * the one that answers "where is the weight", which is the other question
 * anybody asks of a decomposition, and it is the same sixteen rows sorted
 * differently rather than a second list.
 */
function renderServiceTree() {
  const box = $('tree');
  box.innerHTML = '';
  const needle = state.sideFilter;
  const hit = (text) => !needle || String(text ?? '').toLowerCase().includes(needle);
  const diagrams = state.diagrams;

  if (!diagrams?.present) {
    box.append(el('p', 'pane-empty', 'No diagrams/ in this package.'));
    $('file-count').textContent = '';
    return;
  }

  const byKey = new Map(diagrams.services.map((service) => [service.key, service]));
  const row = (service) => {
    const line = el('div', 'tree-file');
    line.classList.toggle('selected', service.key === state.serviceKey);
    line.append(el('span', 'tree-file-name', service.name.replace(/Service$/, '')));
    const count = el('span', 'tree-file-count', `${service.operations ?? 0}`);
    count.title = `${service.operations ?? 0} operations · ${service.tables ?? 0} tables`;
    line.append(count);
    line.onclick = () => { selectService(service.key); setMode('service'); };
    return line;
  };

  let shown = 0;
  if (groupBy() === 'size') {
    const sorted = [...diagrams.services]
      .filter((service) => hit(service.name) || hit(service.tier))
      .sort((a, b) => (b.operations ?? 0) - (a.operations ?? 0));
    for (const service of sorted) { box.append(row(service)); shown += 1; }
  } else {
    for (const tier of diagrams.tiers) {
      const services = tier.services
        .map((key) => byKey.get(key))
        .filter(Boolean)
        .filter((service) => hit(service.name) || hit(tier.tier));
      if (!services.length) continue;
      const group = el('div', 'tree-group');
      const head = el('div', 'tree-group-head');
      const dot = el('span', 'tree-group-dot');
      dot.style.background = tierColour(tier.tier);
      head.append(dot, el('span', null, tier.tier));
      head.append(el('span', 'tree-group-count', String(services.length)));
      group.append(head);
      for (const service of services) { group.append(row(service)); shown += 1; }
      box.append(group);
    }
  }

  if (!shown) box.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
  $('file-count').textContent =
    `${diagrams.services.length} services · ${diagrams.tiers.length} tiers`;
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
    const { group, badge } = section('Decisions', 'docs/adr/', hue('accent'));
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
      ['register', 'Registers', 'docs/registers/', hue('ok')],
      ['handoff', 'Handoff', 'handoff/', hue('info')],
      ['architecture', 'Architecture', 'docs/architecture/', hue('warning')],
      ['active', 'In flight', 'docs/active/', hue('permission')],
      ['guide', 'Guides', 'docs/', hue('text-faint')],
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
const PLATFORM_TOKENS = ['layer-frontend', 'ok', 'patch', 'warning', 'permission', 'info'];

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
    dot.style.background = hue(PLATFORM_TOKENS[index++ % PLATFORM_TOKENS.length]);
    head.append(dot, el('span', null, label || group));
    head.append(el('span', 'tree-group-count', String(list.length)));
    // Grouped by platform, the head names a thing that has its own design, and
    // the only way to reach it was a dropdown in the other pane. Under Modules
    // or Waves it stays a label: a module is not something this viewer draws a
    // design for, and a head that is a control in one grouping and inert in
    // another is worse than one that never was.
    if (groupBy() === 'platforms' && code
        && (state.diagrams?.lld?.platforms ?? []).some((r) => r.name === code)) {
      head.dataset.id = `platform:${code}`;
      head.classList.add('linked');
      head.tabIndex = 0;
      head.title = `${label || group} \u2014 open its design`;
      const open = () => {
        state.platformKey = code;
        if (state.mode === 'platform-lld') renderPlatformLld();
        else setMode('platform-lld');
        markTreeSelection();
      };
      head.onclick = open;
      head.onkeydown = (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
      };
    }
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
    dot.style.background = hue('boards');
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
    dot.style.background = written ? hue('ok') : hue('warning');
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
/**
 * Which tree row is the one being looked at.
 *
 * The answer depends on the view, not only the layer: the Frontend tree holds
 * screens, boards *and* platform groups, and which of those is "current"
 * changes when the mode does. Getting this wrong is invisible — nothing errors,
 * the row simply never highlights — which is why three of the six cases below
 * were missing for as long as they were.
 */
function currentSideId() {
  if (state.layer === 'frontend') {
    // The Platform view is about a platform, so the group head is the row that
    // is current — not whichever screen happens to be remembered from earlier.
    if (state.mode === 'platform-lld') {
      return state.platformKey ? `platform:${state.platformKey}` : null;
    }
    if (state.boardId) return `board:${state.boardId}`;
    return state.screenId ? `screen:${state.screenId}` : null;
  }
  if (state.layer === 'backend') return state.tableName ? `table:${state.tableName}` : null;
  // The domain tree has written `machine:` and `event:` on its rows since it was
  // built and nothing has ever compared anything to them.
  if (state.layer === 'domain') {
    if (state.mode === 'events') return state.eventId ? `event:${state.eventId}` : null;
    if (state.mode === 'states' || state.mode === 'lifecycles-hld') {
      return state.machineId ? `machine:${state.machineId}` : null;
    }
  }
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
// ── two graph scopes that are not networks ───────────────────────────
// The force simulation earns its keep on Files and Local, where the question is
// "what is near what" and nobody has ordered the answer. It does not on these
// two. Schemas is 714 nodes, which settles into a hairball whatever the spring
// constants say; Permissions is a join between two sets, and a join laid out by
// repulsion tells you about the repulsion.

let graphGalaxySummary = '';

/** True for the scopes drawn as a field rather than simulated. */
const GALAXY_SCOPES = new Set(['spine', 'files', 'schemas', 'permissions']);
/** The two whose mass is one field over the whole sphere rather than a halo per
 *  hub — and so the two that need a smaller budget to stay readable. */
const GALAXY_FIELD = new Set(['spine', 'files']);

/**
 * The architecture picture: every contract, and the events that pass between
 * them.
 *
 * The two shared contracts sit inside everything else because `tier: 'core'`
 * puts them on the inner shell, and they are the only things here that are
 * `core`. No contract $refs another — every file-level link points at shared/ —
 * so the lanes are events, which is the only coupling the platform actually
 * has.
 *
 * The mass belongs to the model rather than to any one hub, which is why this
 * passes `motes` instead of putting a `mass` on each contract: the claim is
 * that the package is bigger than its labels, not that this contract is bigger
 * than that one. The hub radius already says the second thing.
 */
function buildSpineGalaxy({ refs = false } = {}) {
  const contracts = state.index.nodes.filter((n) => n.type === 'file');
  const byFile = new Set(contracts.map((c) => c.file));

  // One lane per ordered pair, carrying every event that runs between them.
  // Never symmetrised — which way a packet travels is the payload.
  const pairs = new Map();
  for (const link of state.domain?.contextEdges ?? []) {
    const { fromContract: from, toContract: to } = link;
    if (!from || !to || from === to || !byFile.has(from) || !byFile.has(to)) continue;
    const key = `${from}|${to}`;
    if (!pairs.has(key)) {
      pairs.set(key, { source: `file:${from}`, target: `file:${to}`, events: 0, critical: 0 });
    }
    const lane = pairs.get(key);
    lane.events += 1;
    if (link.critical) lane.critical += 1;
  }

  const TIER = { shared: 'core', spine: 'spine' };
  const hubs = contracts.map((contract) => {
    const members = state.byFile.get(contract.file) ?? [];
    const operations = members.filter((m) => m.type === 'operation').length;
    return {
      ...contract,
      // Sized by what it declares, not by its degree — which is zero for every
      // one of them, since no contract $refs another.
      weight: Math.max(1, operations),
      operations,
      tier: TIER[contract.group] ?? 'satellite',
    };
  });

  const links = [...pairs.values()].map((lane) => ({
    source: lane.source,
    target: lane.target,
    events: lane.events,
    critical: lane.critical > 0,
  }));

  // The $refs. In the Files scope they are the whole picture; in Spine they are
  // an optional backdrop the events are read against, and off by default.
  const known = new Set(hubs.map((h) => h.id));
  const wantRefs = refs || $('graph-shared')?.checked;
  const shared = wantRefs
    ? state.index.fileEdges
      .filter((e) => known.has(e.source) && known.has(e.target)
        && (refs || /\/shared\//.test(e.target)))
      // In Files the amber is the finding: a link that points at shared/, which
      // is 56 of the 57. The one that does not is the thing worth spotting.
      .map((e) => ({ source: e.source, target: e.target, critical: refs && /\/shared\//.test(e.target) }))
    : [];

  const stats = state.index.stats ?? {};
  const lanes = refs ? shared : [...links, ...shared];
  return {
    hubs,
    links: lanes,
    motes: {
      count: (stats.operations ?? 0) + (stats.schemas ?? 0) + (stats.permissions ?? 0),
      hot: stats.permissions ?? 0,
    },
    contracts: hubs.length,
    lanes: lanes.length,
    events: links.length,
    shared: shared.length,
    toShared: shared.filter((l) => l.critical).length,
    critical: links.filter((l) => l.critical).length,
  };
}

function describeGraphHub(hub) {
  if (hub.kind === 'permission') {
    return [
      hub.name,
      hub.declared
        ? `used by ${hub.weight} operation${hub.weight === 1 ? '' : 's'} across `
          + `${hub.holders} contract${hub.holders === 1 ? '' : 's'}`
        : 'no contract declares this — nothing will grant it',
      'double-click to open it',
    ].join(' · ');
  }
  return [
    `${hub.name} · ${hub.tier === 'core' ? 'shared' : hub.tier}`,
    hub.schemas != null ? `${hub.schemas} schemas` : null,
    hub.permissions != null ? `${hub.permissions} permissions used` : null,
    hub.operations != null ? `${hub.operations} operations` : null,
    'double-click to open it',
  ].filter(Boolean).join(' · ');
}

const TIER_OF_GROUP = { shared: 'core', spine: 'spine' };

/**
 * The contracts as bodies, their components as the mass, and every `$ref` that
 * crosses a contract boundary as a lane.
 *
 * The mass is the argument. 30 contracts is the visible layer; the 714 schemas,
 * 935 operations and 141 permissions underneath it are what the package
 * actually is, and drawing them as unlabelled motes says "this is bigger than
 * the labels" without putting 1,800 things on screen to read.
 */
function buildSchemaScopeGalaxy() {
  const { nodes, edges } = state.index;
  const contracts = nodes.filter((n) => n.type === 'file');
  const fileOf = new Map(nodes.map((n) => [n.id, n.file]));

  const count = new Map();
  for (const node of nodes) {
    if (node.type !== 'schema' || !node.file) continue;
    count.set(node.file, (count.get(node.file) ?? 0) + 1);
  }

  // Everything defined inside each contract, and how much of it is an enum.
  const inside = new Map();
  const enumsIn = new Map();
  for (const node of nodes) {
    if (node.type === 'file' || !node.file) continue;
    inside.set(node.file, (inside.get(node.file) ?? 0) + 1);
    if (node.type === 'schema' && node.enumValues?.length) {
      enumsIn.set(node.file, (enumsIn.get(node.file) ?? 0) + 1);
    }
  }

  const hubs = contracts.map((contract) => ({
    id: contract.id,
    name: contract.name,
    weight: Math.max(1, count.get(contract.file) ?? 1),
    schemas: count.get(contract.file) ?? 0,
    tier: TIER_OF_GROUP[contract.group] ?? 'satellite',
    // The 935 operations, 714 schemas and 141 permissions are what the package
    // is; they belong to a contract, so they sit round the contract that owns
    // them rather than being scattered over the whole sphere.
    mass: inside.get(contract.file) ?? 0,
    hot: enumsIn.get(contract.file) ?? 0,
  }));

  // One lane per ordered pair of contracts, however many refs cross it. Drawing
  // a line per $ref would put four hundred strokes between the same two bodies.
  const lanes = new Map();
  for (const edge of edges) {
    if (edge.kind === 'contains') continue;
    const from = fileOf.get(edge.source);
    const to = fileOf.get(edge.target);
    if (!from || !to || from === to) continue;
    const key = `file:${from}|file:${to}`;
    const row = lanes.get(key) ?? { source: `file:${from}`, target: `file:${to}`, count: 0 };
    row.count += 1;
    lanes.set(key, row);
  }
  const known = new Set(hubs.map((h) => h.id));
  const links = [...lanes.values()].filter((l) => known.has(l.source) && known.has(l.target));

  const enums = nodes.filter((n) => n.type === 'schema' && n.enumValues?.length).length;
  const mass = nodes.filter((n) => n.type !== 'file').length;
  return {
    hubs,
    links,
    schemas: nodes.filter((n) => n.type === 'schema').length,
    enums,
    mass,
  };
}

/**
 * Contracts on the inner shell, permissions on the outer, one line per pair.
 *
 * Not a sphere: this is a join between two sets, and there is no third
 * dimension for a projection to mean anything in. A permission no contract
 * declares goes amber — it is used here and it is not in the single enum in
 * `shared/permissions.yaml`, so nothing will ever grant it.
 */
function buildPermissionScopeGalaxy() {
  const { nodes, edges } = state.index;
  const permissions = nodes.filter((n) => n.type === 'permission');
  const permIds = new Set(permissions.map((n) => n.id));

  const used = new Map();     // contract file -> distinct permissions
  const holders = new Map();  // permission -> distinct contracts
  const lanes = new Map();
  for (const edge of edges) {
    if (edge.kind !== 'permission' || !permIds.has(edge.target)) continue;
    const file = state.nodesById.get(edge.source)?.file;
    if (!file) continue;
    const key = `file:${file}|${edge.target}`;
    const row = lanes.get(key) ?? { source: `file:${file}`, target: edge.target, count: 0 };
    row.count += 1;
    lanes.set(key, row);
    if (!used.has(file)) used.set(file, new Set());
    used.get(file).add(edge.target);
    if (!holders.has(edge.target)) holders.set(edge.target, new Set());
    holders.get(edge.target).add(file);
  }

  // A permission only one contract names is that contract's business, and 141
  // dots on a ring is 141 things to read that differ in a label none of them is
  // wide enough to carry. What earns a node here is a permission that is
  // *shared* — the vocabulary two contracts have to agree on — or one that no
  // contract declares, which is a finding.
  const named = (permission) =>
    (holders.get(permission.id)?.size ?? 0) > 1 || permission.declared === false;
  const shared = permissions.filter(named);
  const privateTo = new Map();
  for (const permission of permissions) {
    if (named(permission)) continue;
    const only = [...(holders.get(permission.id) ?? [])][0];
    if (only) privateTo.set(only, (privateTo.get(only) ?? 0) + 1);
  }

  const hubs = [];
  for (const contract of nodes.filter((n) => n.type === 'file')) {
    const n = used.get(contract.file)?.size ?? 0;
    if (!n) continue;   // a contract using no permission has nothing to join to
    hubs.push({
      id: contract.id,
      name: contract.name,
      weight: Math.max(1, n),
      permissions: n,
      tier: 'spine',
      // The inner shell in 3D, the inner ring in 2D. Same claim either way —
      // these are the things the outer set is used *by* — but a shell has room
      // for 28 names and a circle of the same radius has room for about eight.
      shell: 0.68,
      ring: 0.46,
      // the ones nobody else uses, as a halo rather than a hundred more dots
      mass: privateTo.get(contract.file) ?? 0,
    });
  }
  for (const permission of shared) {
    hubs.push({
      id: permission.id,
      name: permission.name,
      kind: 'permission',
      weight: Math.max(1, permission.useCount ?? 1),
      declared: permission.declared !== false,
      holders: holders.get(permission.id)?.size ?? 0,
      // Amber is the finding, and it is the finding this scope exists to make.
      tier: permission.declared === false ? 'core' : 'satellite',
      // Amber, but not inner. `core` carries the colour here and would
      // otherwise drag an undeclared permission onto the 0.34 shell — inside
      // the contracts that use it, which is the wrong way round.
      shell: 1,
      ring: permission.declared === false ? 0.78 : 1,
    });
  }

  const known = new Set(hubs.map((h) => h.id));
  const links = [...lanes.values()]
    .filter((l) => known.has(l.source) && known.has(l.target))
    .map((l) => ({ ...l, critical: state.nodesById.get(l.target)?.declared === false }));

  return {
    hubs,
    links,
    permissions: permissions.length,
    shared: shared.length,
    undeclared: permissions.filter((p) => p.declared === false).length,
    contracts: hubs.filter((h) => h.kind !== 'permission').length,
  };
}

function renderGraphGalaxy() {
  const scope = state.graphScope;
  const built = scope === 'permissions' ? buildPermissionScopeGalaxy()
    : scope === 'spine' ? buildSpineGalaxy()
    : scope === 'files' ? buildSpineGalaxy({ refs: true })
    : buildSchemaScopeGalaxy();
  const permissions = scope === 'permissions';

  graphGalaxy.setSphere(true);
  graphGalaxy.labelMax = 40;
  // Spine is the one view whose mass is a single field over the whole sphere
  // rather than a halo per hub, so it is the one that fills the picture with
  // dots nobody can click. The design asks for 900; at the scale this panel
  // actually gets, that is a fog over thirty labelled contracts.
  graphGalaxy.setData(built, GALAXY_FIELD.has(scope) ? { budget: 380 } : {});
  graphGalaxy.setMode(state.galaxyMode);
  graphGalaxy.setSelected(state.selectedId);
  graphGalaxy.start();

  graphGalaxySummary = scope === 'files'
    ? `${built.contracts} contracts · ${built.lanes} $ref links, ${built.toShared} of them `
      + `to shared/ · not one contract $refs another, which is why Spine draws the `
      + `events instead`
    : scope === 'spine'
    ? `${built.contracts} contracts · ${built.lanes} event lanes between them · `
      + `${built.critical} with a critical consumer`
      + (built.shared ? ` · ${built.shared} shared $refs` : '')
      + ` · ${built.motes.count} operations, schemas and permissions in the field`
    : permissions
    ? `${built.permissions} permissions across ${built.contracts} contracts · `
      + `${built.shared} used by more than one, drawn · the rest sit with the contract that owns them`
      + (built.undeclared ? ` · ${built.undeclared} declared by no contract` : '')
    : `${built.hubs.length} contracts · ${built.schemas} schemas, ${built.enums} of them enums · `
      + `${built.links.length} contract-to-contract $ref lanes · `
      + `${built.mass} components in the field`;
  if (graphGalaxy.moteSampled) graphGalaxySummary += ' · the field is a sample';
  $('graph-hint').textContent = graphGalaxySummary;

  $('graph-legend').classList.add('galaxy-legend');
  // Spine and Schemas colour the same three tiers the same way and mean the
  // same thing by them; what differs is what the dot size and the field are
  // counting, which is the note.
  const CONTRACT_KEYS = [
    ['core', 'shared/ — everything points at these, and they sit inside'],
    ['spine', 'a spine contract'],
    ['satellite', 'a satellite contract'],
  ];
  const FILES_NOTE =
    'dot size is the operations it declares · an amber lane is a $ref into shared/ · '
    + 'every lane in this picture ends in the middle, which is the finding · '
    + 'double-click a contract to open it';
  galaxyLegend($('graph-legend'), permissions
    ? [
        ['spine', 'a contract, on the inner shell'],
        ['satellite', 'a permission more than one contract uses'],
        ['core', 'used but declared by no contract'],
      ]
    : CONTRACT_KEYS,
    permissions
      ? 'dot size is how many operations name it · the halo round a contract is the '
        + 'permissions only it uses · double-click to open one'
      : scope === 'files'
      ? FILES_NOTE
      : scope === 'spine'
      ? 'dot size is the operations it declares · a lane is an event, publisher → consumer · '
        + 'amber is a critical consumer · the field is every operation, schema and permission '
        + 'underneath · double-click a contract to open it'
      : 'dot size is how many schemas the contract defines · the cloud round it is '
        + 'everything it holds, a bright mote being an enum · double-click a contract to open it');
}

function renderGraph() {
  // Two scopes are drawn rather than simulated. Everything below — the node
  // filtering, the force layout, the legend — belongs to the other three.
  const asGalaxy = GALAXY_SCOPES.has(state.graphScope);
  $('graph-canvas').hidden = asGalaxy;
  $('graph-galaxy').hidden = !asGalaxy;
  $('graph-mode').hidden = !GALAXY_SCOPES.has(state.graphScope);
  $('graph-labels-wrap').hidden = asGalaxy;
  $('graph-recenter').hidden = asGalaxy;   // a sphere and a ring are always framed
  $('graph-legend').classList.toggle('galaxy-legend', asGalaxy);
  if (asGalaxy) {
    graph.setData([], []);
    renderGraphGalaxy();
    return;
  }
  graphGalaxy.stop();

  const { nodes, edges, fileEdges } = state.index;
  let viewNodes = [];
  let viewEdges = [];
  let hint = '';

  // Only Local reaches this renderer now. Spine, Files, Schemas and
  // Permissions are drawn as spheres and returned above; their branches
  // below are unreachable and kept only because the force path still shares
  // the node and edge filtering with them. Local keeps the force layout
  // because it has no fixed arrangement to remember — it is the neighbourhood
  // of whatever is selected, a different shape every time.

  if (state.graphScope === 'files') {
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

/** Controls that only mean something in one scope are hidden in the others. */
function syncGraphControls() {
  const spine = state.graphScope === 'spine';
  for (const node of document.querySelectorAll('.spine-only')) node.hidden = !spine;
  // the spine layout is placed rather than simulated, so there is nothing to
  // recenter that Fit does not already do
  $('graph-recenter').textContent = spine ? 'Fit' : 'Recenter';
}

/**
 * The key for the force graph — which is only Local now.
 *
 * Two halves, because the picture makes two kinds of statement. A dot is a
 * thing: a contract, an operation, a schema, a permission. A line is a claim
 * about two of them, and there are three different claims on screen at once —
 * what this contract defines, what those definitions reference, and what an
 * operation requires to be called. Until the lines were coloured there was no
 * point saying so; now there is.
 */
function renderLegend() {
  const legend = $('graph-legend');
  legend.innerHTML = '';
  const entries =
    state.graphScope === 'files'
      ? [['spine', 'spine'], ['satellite', 'satellite'], ['shared', 'shared']]
      : state.graphScope === 'permissions'
        ? [['file', 'contract'], ['permission', 'permission']]
        : state.graphScope === 'schemas'
          ? [['schema', 'schema'], ['param', 'parameter'], ['response', 'response']]
          : [
              ['file', 'contract'], ['operation', 'operation'],
              ['schema', 'schema'], ['enum', 'enum'], ['param', 'parameter'],
              ['response', 'response'], ['permission', 'permission'],
              ['securityScheme', 'security scheme'],
            ];

  // Only the kinds actually on screen. A key listing eight when the graph holds
  // four is a key that has to be read against the picture instead of with it.
  const present = new Set(graph.nodes.map(
    (n) => (n.type === 'schema' && n.enumValues ? 'enum' : n.type)
  ));
  const shown = state.graphScope === 'local'
    ? entries.filter(([key]) => present.has(key))
    : entries;

  for (const [key, label] of shown) {
    const row = el('div', 'legend-row');
    const dot = el('span', 'legend-dot');
    dot.style.background =
      state.graphScope === 'files'
        ? colorForNode({ group: key, type: 'file' }, 'group')
        : colorForNode({ type: key });
    row.append(dot, el('span', null, label));
    legend.append(row);
  }

  const EDGES = [
    ['contains', 'defines it'],
    ['ref', '$ref'],
    ['permission', 'requires the scope'],
  ];
  const kinds = new Set(graph.links.map((l) => l.kind));
  let first = true;
  for (const [kind, label] of EDGES) {
    if (!kinds.has(kind)) continue;
    const row = el('div', `legend-row${first ? ' legend-split' : ''}`);
    first = false;
    const bar = el('span', 'legend-dot bar');
    bar.style.background = colorForLink({ kind });
    row.append(bar, el('span', null, label));
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
  const res = await auth.apiFetch(`/api/tree?path=${encodeURIComponent(relPath)}`);
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
const METHOD_TOKENS = {
  GET: 'info', POST: 'ok', PUT: 'warning', DELETE: 'error', PATCH: 'patch',
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
      color: external ? hue('warning') : schema.enumValues ? hue('patch') : hue('ok'),
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
    [hue('ok'), 'entity in this contract'],
    [hue('patch'), 'enum'],
    [hue('warning'), 'entity from another contract'],
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
  const res = await auth.apiFetch('/api/journeys');
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
        `built — and {screensNoOperation} of the {screens} screens are in the same position.`)
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
    tip(chip, name, `Owns ${ops.length} of the {operations} operations.`);
    return chip;
  }), 'The service that runs the operations this screen calls. {services} across the platform.');

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
        'counted above. {unresolved} of the {operations} operations are in that state.');
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

/**
 * A framed package file — a board, a wireframe, one frame out of a board.
 *
 * The URL arrives from the payload as `/wireframes/…`, which was the whole
 * address while there was one package. `pkgAsset` puts the project on it; the
 * builders that emit these have no idea which project they are being built for.
 */
function frameStage(url, { height = 420, design = 1440, title = 'preview', kind = 'board' } = {}) {
  url = auth.pkgAsset(url);
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
  // Opened in a tab of its own, so it needs the project on it the same way
  // the framed copy does.
  open.href = auth.pkgAsset(board.url);
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
  // frame is the drawn one — the platform board is design intent, with real
  // field names, states and deny reasons read off the package. The
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
  open.href = auth.pkgAsset(primary.openUrl);
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
      // Empty, and either explained or not. The note is the difference between
      // a region that renders from somewhere else and one nobody finished, and
      // it is the only place a reader can see which.
      if (!region.components.length) {
        card.append(el('div', 'component-notes',
          region.notes ? region.notes : 'no components declared'));
      }
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
/**
 * The apps, and the contracts they rest on.
 *
 * The chain is app → platform → screen → operation → contract, and every step of
 * it is declared somewhere in the package. Resolving it rather than reading
 * `app.contracts` is the point: the manifest's own list is a claim, and this is
 * what the screens actually call.
 */
function buildAppsGalaxy() {
  const apps = state.journeys?.apps ?? [];
  const screens = state.journeys?.screens ?? [];

  // Platform code -> the app that owns it, so a screen can find its app.
  //
  // An app manifest names its platforms in full — "P08 Venue Management — Back
  // Office" — and a screen carries only the code, "P08". Matching the two
  // whole strings finds nothing, which is exactly what this view did on its
  // first run: twelve apps, zero contracts, no lanes at all.
  const appOf = new Map();
  for (const app of apps) {
    for (const platform of app.platforms ?? []) {
      const code = String(platform).match(/^(P\d+)/)?.[1];
      if (code) appOf.set(code, app.app);
    }
  }

  // operationId -> the contract that declares it. Built once: a node id is
  // `op:<file>#<name>`, so there is no id to look an operationId up by.
  const fileOf = new Map();
  for (const node of state.index.nodes) {
    if (node.type === 'operation' && node.name) fileOf.set(node.name, node.file);
  }

  const lanes = new Map();          // app|contract -> distinct operations
  const reach = new Map();          // app -> distinct contracts
  const opsIn = new Map();          // contract -> distinct operations called
  const unresolved = new Map();     // app -> operations no contract declares

  for (const screen of screens) {
    const app = appOf.get(screen.platform);
    if (!app) continue;
    for (const api of screen.apis ?? []) {
      const id = api.operationId;
      if (!id) continue;
      const file = fileOf.get(id);
      if (!file) {
        unresolved.set(app, (unresolved.get(app) ?? 0) + 1);
        continue;
      }
      const key = `${app}|${file}`;
      if (!lanes.has(key)) lanes.set(key, new Set());
      lanes.get(key).add(id);
      if (!reach.has(app)) reach.set(app, new Set());
      reach.get(app).add(file);
      if (!opsIn.has(file)) opsIn.set(file, new Set());
      opsIn.get(file).add(id);
    }
  }

  const TIER = { shared: 'core', spine: 'spine' };
  const hubs = [];
  for (const app of apps) {
    hubs.push({
      id: `app:${app.app}`,
      name: app.app.replace(/^venue-/, ''),
      full: app.app,
      app: app.app,
      offline: Boolean(app.offlineCapable),
      status: app.status ?? null,
      contracts: reach.get(app.app)?.size ?? 0,
      // Sized by how far it reaches, not by how much it holds — the cloud
      // round it already says how much it holds.
      weight: Math.max(1, reach.get(app.app)?.size ?? 1),
      tier: 'spine',
      shell: 0.68,
      ring: 0.46,
      // The screens it builds. 392 of them across eleven apps, and not one is
      // worth a labelled node of its own.
      mass: app.screenCount ?? 0,
      hot: unresolved.get(app.app) ?? 0,
    });
  }
  const contractOf = new Map(
    state.index.nodes.filter((n) => n.type === 'file').map((n) => [n.file, n])
  );
  for (const [file, ops] of opsIn) {
    const contract = contractOf.get(file);
    if (!contract) continue;
    hubs.push({
      id: contract.id,
      name: contract.name,
      contractFile: file,
      operations: ops.size,
      weight: Math.max(1, ops.size),
      tier: TIER[contract.group] ?? 'satellite',
      shell: 1,
      ring: 1,
    });
  }

  const known = new Set(hubs.map((h) => h.id));
  const offline = new Set(apps.filter((a) => a.offlineCapable).map((a) => a.app));
  const links = [];
  for (const [key, ops] of lanes) {
    const [app, file] = key.split('|');
    const source = `app:${app}`;
    const target = `file:${file}`;
    if (!known.has(source) || !known.has(target)) continue;
    links.push({ source, target, operations: ops.size, critical: offline.has(app) });
  }

  return {
    hubs,
    links,
    apps: apps.length,
    contracts: opsIn.size,
    screens: apps.reduce((a, x) => a + (x.screenCount ?? 0), 0),
    calls: [...lanes.values()].reduce((a, set) => a + set.size, 0),
    offline: offline.size,
    unresolved: [...unresolved.values()].reduce((a, n) => a + n, 0),
  };
}

function renderAppsGalaxy() {
  const built = buildAppsGalaxy();
  appsGalaxy.labelMax = 40;
  appsGalaxy.setData(built);
  appsGalaxy.setMode(state.galaxyMode);
  appsGalaxy.start();

  appsGalaxySummary =
    `${built.apps} apps · ${built.contracts} contracts they call · `
    + `${built.calls} distinct operations · ${built.offline} apps queue writes offline`
    + (built.unresolved ? ` · ${built.unresolved} calls no contract declares` : '');
  $('apps-hint').textContent = appsGalaxySummary;

  galaxyLegend($('apps-legend'), [
    ['spine', 'an app, on the inner shell'],
    ['core', 'shared/ — every app reaches it'],
    ['satellite', 'a contract an app calls'],
  ], 'dot size is how many contracts an app reaches · the cloud round it is the screens it '
     + 'builds · an amber lane is an offline-capable app, so those calls have to survive a '
     + 'dropped connection · double-click a contract to open it');
}

function renderApps() {
  const map = state.appsLayout === 'galaxy';
  $('apps-body').hidden = map;
  $('apps-galaxy').hidden = !map;
  $('apps-legend').hidden = !map;
  $('apps-mode').hidden = !map;
  if (map) {
    if (!state.journeys) {
      appsGalaxy.setData({ hubs: [], links: [] });
      $('apps-hint').textContent = 'Reading the app manifests…';
      return;
    }
    renderAppsGalaxy();
    return;
  }
  appsGalaxy.stop();
  renderAppsList();
}

function renderAppsList() {
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
    [hue('ok'), 'initial'],
    [hue('accent'), 'terminal'],
    [hue('info'), 'operation moves it'],
    [hue('ok'), 'timer or job — dashed, because no operation causes it'],
    [hue('warning'), 'reversal — value moving backwards'],
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
  markTreeSelection();
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

// ── the outbox, as a galaxy ──────────────────────────────────────────
// The contracts do not $ref each other at all — every file-level link points at
// shared/ — so the only real coupling between bounded contexts runs through
// `platform.outbox`. The catalogue lists what is declared; this draws what it
// adds up to, and it is the one place in the viewer where the packet travelling
// from publisher to consumer is not a metaphor for anything.

/** The hint line, kept so hovering a context can borrow it and give it back. */
let eventGalaxySummary = '';

/** One line about a context, for the hint. */
function describeContext(hub) {
  const context = hub.context ?? {};
  const role = hub.publishes && hub.consumes
    ? 'publishes and consumes'
    : hub.publishes ? 'a source — publishes only' : 'a read model — consumes only';
  return [
    `${hub.name} · ${role}`,
    hub.publishes ? `${hub.publishes} published` : null,
    hub.consumes ? `${hub.consumes} consumed` : null,
    context.criticalIn ? `${context.criticalIn} critical in` : null,
    context.contract ? 'double-click to open its contract' : 'no contract of this name',
  ].filter(Boolean).join(' · ');
}

/**
 * Contexts as hubs, the outbox traffic as lanes.
 *
 * The tier is the argument the view exists to make. A context that only
 * publishes is a source and sits on the inner shell; one that only consumes is
 * a read model and sits outside everything; whatever does both is the coupled
 * middle. Reporting consumes nine events and publishes none — that asymmetry is
 * the shape of the platform, and no ordering of a list will show it.
 */
function buildEventGalaxy() {
  const domain = state.domain;
  const criticalOnly = $('events-critical').checked;

  const payload = new Map((domain?.events ?? []).map((e) => [e.name, e.payload.length]));
  const criticalTo = new Map();
  for (const event of domain?.events ?? []) {
    for (const consumer of event.consumers) {
      if (!consumer.isCritical || !consumer.context) continue;
      criticalTo.set(consumer.context, (criticalTo.get(consumer.context) ?? 0) + 1);
    }
  }

  const hubs = (domain?.contexts ?? []).map((context) => {
    const publishes = context.publishes.length;
    const consumes = context.consumes.length;
    return {
      id: context.name,
      name: context.name,
      weight: Math.max(1, publishes + consumes),
      tier: publishes && consumes ? 'spine' : publishes ? 'core' : 'satellite',
      // What this context actually handles: every field of every event it
      // publishes, plus every message delivered to it. None of those is worth
      // a label — a payload field is not a thing you click — so they are the
      // body of the context rather than more nodes on the screen.
      mass: context.publishes.reduce((a, name) => a + (payload.get(name) ?? 0), 0) + consumes,
      hot: criticalTo.get(context.name) ?? 0,
      context,
      publishes,
      consumes,
    };
  });

  // One lane per ordered pair, carrying every event that runs along it. Drawing
  // one line per event would put nine parallel strokes between the same two
  // contexts and say nothing the thickness could not.
  const lanes = new Map();
  for (const link of domain?.contextEdges ?? []) {
    if (criticalOnly && !link.critical) continue;
    if (!link.from || !link.to || link.from === link.to) continue;
    const key = `${link.from}|${link.to}`;
    if (!lanes.has(key)) {
      lanes.set(key, { source: link.from, target: link.to, events: [], critical: false });
    }
    const lane = lanes.get(key);
    lane.events.push(link.event);
    if (link.critical) lane.critical = true;
  }

  return { hubs, links: [...lanes.values()] };
}

function renderEventGalaxy() {
  const built = buildEventGalaxy();
  eventGalaxy.setData(built);
  eventGalaxy.setMode(state.galaxyMode);
  eventGalaxy.start();

  const stats = state.domain?.stats ?? {};
  const sources = built.hubs.filter((h) => h.tier === 'core').length;
  const sinks = built.hubs.filter((h) => h.tier === 'satellite').length;
  eventGalaxySummary =
    `${built.hubs.length} contexts · ${built.links.length} lanes · ` +
    `${stats.consumers ?? 0} deliveries, ${stats.criticalConsumers ?? 0} critical · ` +
    `${sources} publish only, ${sinks} consume only`
    + (eventGalaxy.moteSampled ? ' · the field is a sample' : '');
  $('events-hint').textContent = eventGalaxySummary;

  galaxyLegend($('events-legend'), [
    ['core', 'a source — publishes, consumes nothing'],
    ['spine', 'publishes and consumes'],
    ['satellite', 'a read model — consumes only'],
  ], 'dot size is how many events it touches · amber lane = a critical consumer · '
     + 'the packet runs publisher → consumer · click a context, double-click to open it');
}

function renderEvents() {
  const galaxy = state.eventsLayout === 'galaxy';
  const events = domainEvents();

  // Only one reading is on screen at a time, and the toolbar sheds the controls
  // that mean nothing to it — an event picker over a diagram of every context
  // is a control that cannot be obeyed.
  $('events-body').hidden = galaxy;
  $('events-canvas').hidden = !galaxy;
  $('events-legend').hidden = !galaxy;
  $('events-scope').hidden = galaxy;
  $('events-mode').hidden = !galaxy;
  $('events-critical-wrap').hidden = !galaxy;
  if (!galaxy) eventGalaxy.stop();

  if (galaxy) {
    if (!events.length) {
      eventGalaxy.setData({ hubs: [], links: [] });
      $('events-hint').textContent = state.domain ? 'No events in events/' : 'Reading events/…';
      return;
    }
    renderEventGalaxy();
    renderEventLinks();
    return;
  }

  const body = $('events-body');
  body.innerHTML = '';
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

/**
 * Open the state model for an entity named in the lifecycles design.
 *
 * The design names entities; `openMachine` takes the `states/` file. The
 * low-level index rows carry `source`, which is that file — so the join goes
 * through them rather than deriving one name from the other. Deriving would be
 * wrong 22 times: `LLD-Operational alert` lives in `alert.yaml`, and 22 of the
 * 113 name themselves that way on purpose.
 */
function openStateModel(entity) {
  const row = (state.diagrams?.lld?.lifecycles ?? []).find((r) => r.entity === entity);
  if (row?.source) return openMachine(row.source);
  const found = machines().find((m) => m.entity === entity);
  if (found) openMachine(found.file);
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
  markTreeSelection();
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
  dot.style.background = hue('info');
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
  edot.style.background = hue('permission');
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
    gdot.style.background = hue('warning');
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

/**
 * Put one table on screen, wherever the ask came from.
 *
 * **A table's detail is its columns, and only the ER view has columns** — a mote
 * in the galaxy is a table's mass, not its shape. So asking for a table is
 * asking for the ER view, and this says it once instead of each of the five
 * callers deciding for itself.
 *
 * It had been left to them, and the galaxy was the only one that tried: the
 * drill set `state.dataLayout` and called this, which then took the branch that
 * talks to the canvas rather than the one that redraws it. The canvas was hidden
 * *and* empty — `setData([], [])` runs on the way into the galaxy — so a click
 * moved the scope select, marked the tree row, filled the side pane, and changed
 * nothing a reader could see.
 */
function selectTable(name) {
  state.tableName = name;
  const table = (state.backend?.tables ?? []).find((t) => t.name === name);
  if (state.layer !== 'backend') { setLayer('backend'); }
  const fromGalaxy = state.dataLayout === 'galaxy';
  if (fromGalaxy) {
    state.dataLayout = 'boxes';
    // The control is told, not just the state. A segmented button that
    // disagrees with what is drawn is worse than a wrong view, because
    // `bindSeg` returns early when the state already matches — so the one
    // control that looks like it would fix it is the one that cannot.
    syncSegs('dataLayout');
  }
  if (fromGalaxy || (table && table.module !== state.dataModule)) {
    if (table) {
      state.dataModule = table.module;
      $('data-scope').value = table.module;
    }
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
      color: { written: hue('ok'), part: hue('info'), none: hue('warning') }[state_],
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
  const CAPTION = hue('accent');

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
      color: !own ? hue('warning') : table.ddl ? hue('ok') : hue('info'),
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

// ── the database, as a galaxy ────────────────────────────────────────
// The box view is the one to read a schema with. It is not the one to see the
// database with: 31 boxes with no centre is the picture the sphere was invented
// to replace, and the single-schema view already answers "what is in here".
//
// Two scopes, one renderer. Zoomed out the bodies are schemas and the mass
// behind them is every table; drilled in they are the tables of one schema and
// the mass is its columns. Both are the same claim at different magnification,
// which is what the box view cannot do — a box is a box at every zoom.

let dataGalaxySummary = '';

function describeDataHub(hub) {
  if (hub.module) {
    return [
      `${hub.name} · ${hub.tables} table${hub.tables === 1 ? '' : 's'}`,
      hub.written ? `${hub.written} written as SQL` : 'none written as SQL',
      hub.inbound ? `${hub.inbound} schema${hub.inbound === 1 ? '' : 's'} key into it` : 'nothing keys into it',
      hub.outbound ? `keys into ${hub.outbound}` : 'keys into nothing — an anchor',
      'double-click to open it',
    ].filter(Boolean).join(' · ');
  }
  return [
    hub.name,
    `${hub.weight} column${hub.weight === 1 ? '' : 's'}`,
    hub.ddl ? 'written as SQL' : 'derived from the contracts, not yet written',
    'double-click to open it in the ER view',
  ].join(' · ');
}

/**
 * Every schema as a body, every table as a mote.
 *
 * The tier is structural, and it is the one thing the box view never showed:
 * a schema that everything keys into and which keys into nothing is an anchor
 * and sits inside; a schema nothing depends on is a leaf and sits outside. The
 * built-or-planned story that the boxes carry in their colour moves to the
 * mass — a bright mote is a table whose SQL exists — so each channel says one
 * thing rather than two.
 */
function buildSchemaGalaxy() {
  const backend = state.backend;
  const modules = backend?.modules ?? [];
  const tables = backend?.tables ?? [];
  const tableModule = new Map(tables.map((t) => [t.name, t.module]));

  const built = new Map();
  for (const table of tables) {
    const row = built.get(table.module) ?? { written: 0, total: 0 };
    row.total += 1;
    if (table.ddl) row.written += 1;
    built.set(table.module, row);
  }

  // schema → schema, counted by the columns that cross
  const out = new Map();
  const inbound = new Map();
  const cross = (from, to, declared) => {
    if (!from || !to || from === to) return;
    const key = `${from}|${to}`;
    const row = out.get(key) ?? { source: from, target: to, count: 0, declared: 0 };
    row.count += 1;
    if (declared) row.declared += 1;
    out.set(key, row);
    if (!inbound.has(to)) inbound.set(to, new Set());
    inbound.get(to).add(from);
  };
  for (const table of tables) {
    cross(table.module, tableModule.get(table.childOf), true);
    for (const ref of table.references ?? []) cross(table.module, tableModule.get(ref.toTable), true);
    for (const key of table.foreignKeys ?? []) cross(table.module, tableModule.get(key.toTable), false);
  }
  const outbound = new Map();
  for (const row of out.values()) {
    if (!outbound.has(row.source)) outbound.set(row.source, new Set());
    outbound.get(row.source).add(row.target);
  }

  const hubs = modules.map((module) => {
    const inn = inbound.get(module.name)?.size ?? 0;
    const outn = outbound.get(module.name)?.size ?? 0;
    const stat = built.get(module.name) ?? { written: 0, total: module.tables ?? 0 };
    return {
      id: `schema:${module.name}`,
      name: module.name,
      module: module.name,
      weight: Math.max(1, stat.total),
      tables: stat.total,
      written: stat.written,
      inbound: inn,
      outbound: outn,
      // The tables are the schema's body. 359 of them as separate nodes would
      // be 359 things to read that differ only in a name nobody can see at
      // this zoom; as mass they say which schema is the big one at a glance.
      mass: stat.total,
      hot: stat.written,
      // An anchor is where a schema's own outbound keys stop — everything keys
      // into it and it keys into nothing. That is what sits at the middle.
      tier: inn >= 2 && outn === 0 ? 'core' : inn === 0 ? 'satellite' : 'spine',
    };
  });

  const known = new Set(hubs.map((h) => h.id));
  const links = [...out.values()]
    .filter((row) => known.has(`schema:${row.source}`) && known.has(`schema:${row.target}`))
    .map((row) => ({
      source: `schema:${row.source}`,
      target: `schema:${row.target}`,
      // Amber is the lane worth looking at twice: nothing declares these, they
      // were read off column names, and the box view draws them dashed for the
      // same reason.
      critical: row.declared === 0,
      count: row.count,
    }));

  const columns = Object.values(backend?.columns ?? {}).reduce((a, c) => a + c.length, 0);
  return { hubs, links, tables: tables.length, columns };
}

/** The tables of one schema as bodies, their columns as the mass. */
function buildTableGalaxy(module) {
  const backend = state.backend;
  const tables = (backend?.tables ?? []).filter((t) => t.module === module);
  const here = new Set(tables.map((t) => t.name));

  const hubs = tables.map((table) => {
    const columns = (backend.columns[table.name] ?? []).length;
    const leaves = (table.references ?? []).concat(table.keys ?? [])
      .some((r) => r.toTable && !here.has(r.toTable));
    return {
      id: `table:${table.name}`,
      name: table.name.split('.').slice(1).join('.') || table.name,
      table: table.name,
      weight: Math.max(1, columns),
      ddl: Boolean(table.ddl),
      mass: columns,
      hot: table.ddl ? columns : 0,
      // A root that nothing in the schema hangs off sits inside; a table that
      // reaches out of this schema sits outside; the rest are the body of it.
      tier: table.isSchemaRoot ? 'core' : leaves ? 'satellite' : 'spine',
    };
  });

  const known = new Set(hubs.map((h) => h.id));
  const seen = new Set();
  const links = [];
  const join = (from, to, declared) => {
    if (!to || from === to) return;
    const key = `${from}|${to}`;
    if (seen.has(key) || !known.has(`table:${from}`) || !known.has(`table:${to}`)) return;
    seen.add(key);
    links.push({ source: `table:${from}`, target: `table:${to}`, critical: !declared });
  };
  for (const table of tables) {
    join(table.name, table.childOf, true);
    for (const ref of table.references ?? []) join(table.name, ref.toTable, true);
    for (const key of table.keys ?? []) join(table.name, key.toTable, true);
    for (const key of table.foreignKeys ?? []) join(table.name, key.toTable, false);
  }

  const columns = tables.reduce((a, t) => a + (backend.columns[t.name] ?? []).length, 0);
  return { hubs, links, tables: tables.length, columns };
}

function renderDataGalaxy() {
  const whole = state.dataModule === ALL_SCHEMAS;
  const built = whole ? buildSchemaGalaxy() : buildTableGalaxy(state.dataModule);
  dataGalaxy.labelMax = whole ? 40 : 30;
  dataGalaxy.setData(built);
  dataGalaxy.setMode(state.galaxyMode);
  dataGalaxy.setSelected(state.tableName ? `table:${state.tableName}` : null);
  dataGalaxy.start();

  const anchors = built.hubs.filter((h) => h.tier === 'core').length;
  dataGalaxySummary = whole
    ? `${built.hubs.length} schemas · ${built.tables} tables, ${built.columns} columns · `
      + `${built.links.length} relationships between schemas · `
      + `${anchors} anchor${anchors === 1 ? '' : 's'} — keyed into, keying into nothing`
    : `${state.dataModule} · ${built.tables} tables, ${built.columns} columns · `
      + `${built.links.length} relationships inside this schema`;
  if (dataGalaxy.moteSampled) dataGalaxySummary += ' · the field is a sample';
  $('data-hint').textContent = dataGalaxySummary;

  $('data-legend').classList.add('galaxy-legend');
  galaxyLegend($('data-legend'), whole
    ? [
        ['core', 'an anchor — everything keys into it, it keys into nothing'],
        ['spine', 'keys both ways'],
        ['satellite', 'nothing keys into it'],
      ]
    : [
        ['core', 'the schema root'],
        ['spine', 'inside this schema'],
        ['satellite', 'reaches into another schema'],
      ],
    whole
      ? 'dot size is how many tables · a bright mote is a table whose SQL exists · '
        + 'amber lane = read off column names, nothing declares it · double-click a schema to open it'
      : 'dot size is how many columns · double-click a table to open it in the ER view');
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

  const galaxy = state.dataLayout === 'galaxy';
  $('data-canvas').hidden = galaxy;
  $('data-galaxy').hidden = !galaxy;
  $('data-mode').hidden = !galaxy;
  // The box view's own controls say nothing to a field of motes.
  for (const id of ['data-rows', 'data-inferred', 'data-ambient']) {
    $(id)?.closest('.toggle')?.toggleAttribute('hidden', galaxy);
  }
  $('data-fit').hidden = galaxy;   // a sphere is always framed
  $('data-legend').classList.toggle('galaxy-legend', galaxy);

  if (galaxy) {
    data.setData([], []);
    renderDataGalaxy();
    return;
  }
  dataGalaxy.stop();

  // The canvas was hidden while the galaxy had the view, and a hidden canvas
  // measures 0x0 — so laying out against it produces a diagram with nothing in
  // it. `setMode` resizes on the way into the view, which is why this only
  // ever went wrong on a layout switch. Now that the galaxy is the default,
  // a layout switch is the only way anybody gets here.
  data.resize();
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
      [hue('accent'), `anchored on ${state.dataAnchor}`],
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
      [hue('ok'), 'every table written'],
      [hue('info'), 'part written'],
      [hue('warning'), 'derivable, none written'],
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
      [hue('ok'), 'created by a migration'],
      [hue('info'), 'derived from the contracts, not written yet'],
      [hue('warning'), 'table from another schema'],
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
    // Say which of the two it is. "No routing sheet" sent a reader looking for
    // a missing sheet when the sheet was present, carried its header, and held
    // one row reading `TOTAL 0 0 0 0` — a generator that ran and produced
    // nothing, which is a different thing to go and fix.
    body.append(el('p', 'pane-empty', state.backend?.scalingSheet
      ? 'The workbook’s Scaling sheet is empty — it carries its header and no contract rows, '
        + 'so nothing here is routed. The sheet is generated, so this is upstream of the viewer.'
      : 'No routing sheet in the schema workbook.'));
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
    ['writes', 'primary (write)', hue('error')],
    ['primaryReads', 'primary (read)', hue('warning')],
    ['replicaReads', 'replica', hue('ok')],
    ['analyticalReads', 'analytical', hue('patch')],
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

// ── services: what ships together ────────────────────────────────────
//
// Three views over diagrams/, which is the only artefact in the package that
// says what deploys as one unit. Everything in it is stated twice — here and in
// the schema workbook — and the builder reports where the two disagree rather
// than picking one, so what these views draw is the claim, with its own
// contradiction visible in the Audit beside it.

/**
 * Watches the map for a size change, because the arrows are pixel positions and
 * are wrong the instant the pane moves. Held here rather than in `state`: it is
 * a live browser object belonging to one drawing of one view, and `state` is
 * what the rest of the app reads.
 */
let mapObserver = null;

/** One colour per tier, ordered the way the tiers deploy. */
const TIER_TOKENS = {
  foundation: 'ok',
  commerce: 'error',
  operations: 'warning',
  engagement: 'patch',
  platform: 'muted',
};
const tierColour = (tier) => hue(TIER_TOKENS[tier] ?? 'muted');

function selectService(key) {
  state.serviceKey = key;
  renderServiceTree();
}

// Every name a service holds belongs to another layer. These four go there and
// do exactly what that layer does when anything else jumps into it — the same
// state, the same setMode — rather than inventing a second way in.
function openContract(stem) {
  const node = state.index?.nodes?.find(
    (n) => n.type === 'file'
      && String(n.file ?? '').split('/').pop().replace(/\.ya?ml$/, '') === stem
  );
  if (!node) return toast(`No contract file called ${stem}`);
  select(node.id);
  setLayer('contracts');
  setMode('reader');
}

function openSchemaModule(name) {
  if (!state.backend?.modules?.some((m) => m.name === name)) {
    return toast(`${name} is not a schema in the workbook`);
  }
  setLayer('backend');
  openSchema(name);
  setMode('data');
}

/** `F01 Guest buys a ticket online` — the id is the first word. */
function openServiceFlow(text) {
  const id = String(text).trim().split(/\s+/)[0].toUpperCase();
  if (!state.journeys?.flows?.some((f) => f.id === id)) return toast(`No flow called ${id}`);
  state.journeyId = id;
  setLayer('frontend');
  setMode('journey');
}

/** `P01:WEB-008 Add-ons & Upsell` — platform, colon, screen id, then a label. */
function openServiceScreen(text) {
  const id = /^[A-Za-z0-9]+:([A-Za-z0-9-]+)/.exec(String(text).trim())?.[1];
  if (!id || !state.journeys?.screens?.some((screen) => screen.id === id)) {
    return toast(`No screen called ${text}`);
  }
  state.screenId = id;
  setLayer('frontend');
  setMode('screen');
}

const serviceByKey = (key) =>
  state.diagrams?.services?.find((service) => service.key === key) ?? null;

/**
 * Which file this is, and what wrote it.
 *
 * Every other layer shows the artefact behind what it draws — a contract names
 * its yaml, an ADR names its markdown — and this one drew two files and named
 * neither, so the diagrams looked absent to anyone who came looking for them by
 * name. The generator is worth saying too: these are derived, and a reader who
 * edits one by hand should know it will be overwritten.
 */
function sourceLine(file, generatedBy) {
  const line = el('div', 'adr-file', file);
  if (generatedBy) {
    line.append(el('span', 'artefact-generator', ` \u00b7 generated by ${generatedBy}`));
  }
  return line;
}

/** A `**bold**` line from the diagrams, as a paragraph. */
function proseLine(text, className = 'service-prose') {
  const box = el('div', className);
  box.innerHTML = inlineMarkdown(String(text ?? ''));
  return box;
}

/**
 * Which file the services index was actually read from.
 *
 * `diagrams/` was reorganised on 25 August and the old paths were left on disk
 * holding the previous drop, so a constant here was not merely out of date — it
 * named a real file with the wrong contents in it, which is the version of this
 * mistake that nothing catches. The reader reports where it read; this is the
 * fallback for a payload from before it did.
 */
const hldFile = () => state.diagrams?.servicesFile ?? 'diagrams/hld/02-services.yaml';

/** ops · tables · coverage, the three numbers every service is compared on. */
function serviceFigures(service) {
  const figures = el('div', 'service-figures');
  const figure = (value, label, title) => {
    const cell = el('div', 'service-figure');
    cell.append(el('b', null, String(value)));
    cell.append(el('span', null, label));
    if (title) cell.title = title;
    return cell;
  };
  figures.append(figure(service.operations ?? 0, 'operations'));
  // The workbook's count, not the diagram's, wherever the two are both present:
  // the workbook is where a table is actually assigned, and a difference
  // between them is already a finding in the Audit rather than something to
  // paper over here.
  const owned = service.workbookTables?.length ?? 0;
  const claimed = service.tables ?? 0;
  figures.append(figure(
    owned || claimed,
    'tables',
    owned && claimed && owned !== claimed
      ? `the diagram says ${claimed}, the workbook assigns ${owned}`
      : null
  ));
  if (service.flowCoverage != null) {
    figures.append(figure(`${service.flowCoverage}%`, 'walked',
      'how much of this service a journey has walked'));
  }
  return figures;
}

/**
 * What a service touches: screens, APIs, schemas.
 *
 * The three coarse counts, for the diagrams. The line above them in either box
 * gives the fine grain — operations and tables — so these say across how many
 * APIs those operations are served and across how many schemas those tables
 * sit, and add the one number neither box had: how far into the product the
 * service actually reaches.
 *
 * Screens come from the detail file. A service without one has no screen list,
 * which is not the same as appearing on no screens, so it is left out rather
 * than reported as zero.
 */
function serviceTouches(service) {
  const count = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const parts = [];
  if (service.detailFile) parts.push(count(service.screens?.length ?? 0, 'screen', 'screens'));
  parts.push(count(service.contracts?.length ?? 0, 'API', 'APIs'));
  parts.push(count(service.schemas?.length ?? 0, 'ER', 'ERs'));
  return parts.join(' · ');
}

// \u2500\u2500 one platform, drawn \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
//
// The modules a surface is assembled from above it, the services it calls
// beside it. Same arrangement as the service LLD because it is the same kind of
// statement about a different thing \u2014 what it is built from, and what it
// depends on.
//
// The services are ordered and sized by operation calls. A platform making 112
// calls into OrderService and 1 into InventoryService has one real dependency
// and eleven incidental ones, and that is the whole shape of a surface; sorted
// alphabetically it would be fifteen names.

const PLT = {
  width: 1080, boxW: 140, boxH: 40, gap: 10,
  coreW: 260, coreH: 96, rowGap: 58, sideW: 210, sideH: 30, sideGap: 6,
  perRow: 6, shown: 8,
};

function renderPlatformLld() {
  const body = $('platform-lld-body');
  const pick = $('platform-pick');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  const rows = diagrams?.lld?.platforms ?? [];
  if (!rows.length) {
    body.append(el('p', 'pane-empty', 'This package has no diagrams/lld/platforms/.'));
    $('platform-lld-hint').textContent = '';
    pick.innerHTML = '';
    return;
  }

  if (!state.platformKey || !rows.some((r) => r.name === state.platformKey)) {
    state.platformKey = rows[0].name;
  }
  if (pick.options.length !== rows.length) {
    pick.innerHTML = '';
    for (const row of rows) {
      const option = document.createElement('option');
      option.value = row.name;
      option.textContent = row.title ?? row.name;
      pick.append(option);
    }
    pick.onchange = () => { state.platformKey = pick.value; renderPlatformLld(); };
  }
  pick.value = state.platformKey;

  const row = rows.find((r) => r.name === state.platformKey);

  // The index row is the summary; the body is on disk behind one request,
  // because 15 platform files inlined would be 15 nobody asked for.
  const detail = state.platformDetail?.[row.name];
  if (detail === undefined) {
    body.append(el('p', 'pane-empty', 'Reading the design\u2026'));
    auth.apiFetch(`/api/diagrams/detail?set=platforms&name=${encodeURIComponent(row.name)}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((found) => {
        state.platformDetail = { ...(state.platformDetail ?? {}), [row.name]: found?.doc ?? null };
        if (state.mode === 'platform-lld') renderPlatformLld();
      })
      .catch(() => {
        state.platformDetail = { ...(state.platformDetail ?? {}), [row.name]: null };
        if (state.mode === 'platform-lld') renderPlatformLld();
      });
    return;
  }
  if (!detail) {
    body.append(el('p', 'pane-empty', `Could not read ${row.file}.`));
    return;
  }

  const modules = detail.modulesUsed ?? [];
  const called = (detail.servicesCalled ?? [])
    .slice()
    .sort((a, b) => (b.operationCalls ?? 0) - (a.operationCalls ?? 0));
  const shown = called.slice(0, PLT.shown);
  const coverage = detail.coverage ?? {};

  $('platform-lld-hint').textContent =
    `${detail.screens?.length ?? row.screens ?? 0} screens \u00b7 ${modules.length} modules \u00b7 `
    + `${called.length} services`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'Low-level design \u00b7 one surface'));
  head.append(el('h2', 'journey-title', detail.title ?? row.title ?? row.name));
  head.append(sourceLine(row.file, detail.generatedBy ?? diagrams.generatedBy));
  body.append(head);

  // ---- lay it out --------------------------------------------------------
  const mid = PLT.width / 2 - PLT.sideW / 2 + 20;
  const rowW = (n) => n * PLT.boxW + Math.max(0, n - 1) * PLT.gap;
  const topY = 20;
  const modRows = Math.ceil(modules.length / PLT.perRow) || 0;
  const coreY = topY + (modRows ? modRows * (PLT.boxH + PLT.gap) - PLT.gap + PLT.rowGap : 10);
  const sideTop = coreY + PLT.coreH / 2
    - (shown.length * (PLT.sideH + PLT.sideGap) - PLT.sideGap) / 2;
  const height = Math.max(
    coreY + PLT.coreH + 30,
    sideTop + shown.length * (PLT.sideH + PLT.sideGap) + 20
  );

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${PLT.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });
  const defs = svgEl('defs');
  const marker = svgEl('marker', {
    id: 'plt-head', viewBox: '0 0 8 8', refX: 7, refY: 4,
    markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse',
  });
  marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: 'dia-arrow-head' }));
  defs.append(marker);
  svg.append(defs);
  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  const boxes = svgEl('g', { class: 'dia-boxes' });
  svg.append(boxes);
  const tight = [];

  const tint = audienceColour(detail.audience);
  const coreX = mid - PLT.coreW / 2;

  const link = (a, b) => lanes.append(svgEl('path', {
    d: `M ${a.x} ${a.y} C ${a.x + (b.x - a.x) * 0.4} ${a.y}, `
      + `${a.x + (b.x - a.x) * 0.6} ${b.y}, ${b.x} ${b.y}`,
    class: 'dia-arrow', 'marker-end': 'url(#plt-head)',
  }));

  // ---- the surface -------------------------------------------------------
  const core = svgEl('g', { class: 'dia-box' });
  core.append(svgEl('rect', {
    x: coreX, y: coreY, width: PLT.coreW, height: PLT.coreH, rx: 7,
    class: 'dia-box-bg', style: `--tier:${tint}`,
  }));
  core.append(svgEl('rect', {
    x: coreX, y: coreY, width: 3, height: PLT.coreH, fill: tint, rx: 1.5,
  }));
  const coreName = svgEl('text', {
    x: coreX + 12, y: coreY + 22, class: 'dia-box-name', 'font-size': 13,
  });
  coreName.textContent = `${row.name} ${String(detail.title ?? '')
    .replace(new RegExp(`^${row.name}\\s*`), '').split('\u2014')[0].trim()}`;
  core.append(coreName);
  tight.push([coreName, PLT.coreW - 24]);
  for (const [i, line] of [
    `${detail.audience ?? '?'} \u00b7 ${detail.operator ?? '?'} \u00b7 ${detail.formFactor ?? '?'}`,
    `${detail.app ?? '?'}${detail.offlineCapable ? ' \u00b7 offline-capable' : ''}`,
  ].entries()) {
    const node = svgEl('text', {
      x: coreX + 12, y: coreY + 40 + i * 14, class: 'dia-box-counts', 'font-size': 10.5,
    });
    node.textContent = line;
    core.append(node);
    tight.push([node, PLT.coreW - 24]);
  }
  // Flow coverage: the one number here about the package rather than the
  // product. A screen in no flow has been specified and never walked.
  if (coverage.screens) {
    const walked = (coverage.inAFlow ?? 0) / coverage.screens;
    boxes.append(svgEl('rect', {
      x: coreX + 12, y: coreY + 74, width: PLT.coreW - 24, height: 5, rx: 2.5,
      fill: 'var(--border)',
    }));
    boxes.append(svgEl('rect', {
      x: coreX + 12, y: coreY + 74, width: (PLT.coreW - 24) * walked,
      height: 5, rx: 2.5, fill: tint, opacity: 0.85,
    }));
    const note = svgEl('text', {
      x: coreX + 12, y: coreY + 69, class: 'dia-box-counts', 'font-size': 10,
    });
    note.textContent =
      `${coverage.inAFlow ?? 0} of ${coverage.screens} screens walked by a flow`;
    core.append(note);
  }
  const coreTitle = svgEl('title');
  coreTitle.textContent = detail.why
    ? String(detail.why).replace(/\*\*/g, '')
    : String(detail.title ?? row.name);
  core.append(coreTitle);
  boxes.append(core);

  // ---- what it is assembled from ----------------------------------------
  if (modules.length) {
    modules.forEach((mod, i) => {
      const r = Math.floor(i / PLT.perRow);
      const c = i % PLT.perRow;
      const wide = Math.min(modules.length - r * PLT.perRow, PLT.perRow);
      const left = mid - rowW(wide) / 2;
      const x = left + c * (PLT.boxW + PLT.gap);
      const y = topY + r * (PLT.boxH + PLT.gap);
      const group = svgEl('g', { class: 'dia-box' });
      group.append(svgEl('rect', {
        x, y, width: PLT.boxW, height: PLT.boxH, rx: 6, class: 'dia-box-bg',
      }));
      const name = svgEl('text', {
        x: x + 10, y: y + 17, class: 'dia-box-name', 'font-size': 11,
      });
      name.textContent = mod.module;
      group.append(name);
      tight.push([name, PLT.boxW - 20]);
      const sub = svgEl('text', {
        x: x + 10, y: y + 30, class: 'dia-box-counts', 'font-size': 9.5,
      });
      sub.textContent = `${mod.screens ?? 0} screens`;
      group.append(sub);
      boxes.append(group);
      if (r === modRows - 1 || (r + 1) * PLT.perRow >= modules.length) {
        link({ x: x + PLT.boxW / 2, y: y + PLT.boxH }, { x: coreX + PLT.coreW / 2, y: coreY });
      }
    });
    const label = svgEl('text', {
      x: mid - rowW(Math.min(modules.length, PLT.perRow)) / 2, y: topY - 6,
      class: 'dia-band-label', 'font-size': 10,
    });
    label.textContent = 'WHAT IT IS ASSEMBLED FROM';
    svg.append(label);
  }

  // ---- what it calls -----------------------------------------------------
  if (shown.length) {
    const x = PLT.width - PLT.sideW - 16;
    const label = svgEl('text', {
      x, y: sideTop - 8, class: 'dia-band-label', 'font-size': 10,
    });
    label.textContent = 'WHAT IT CALLS';
    svg.append(label);
    const most = shown[0]?.operationCalls || 1;
    shown.forEach((call, i) => {
      const y = sideTop + i * (PLT.sideH + PLT.sideGap);
      const service = (diagrams.services ?? []).find((v) => v.name === call.service);
      const colour = service ? tierColour(service.tier) : hue('muted');
      const group = svgEl('g', { class: 'dia-box', tabindex: service ? 0 : null });
      group.append(svgEl('rect', {
        x, y, width: PLT.sideW, height: PLT.sideH, rx: 5,
        class: 'dia-box-bg', style: `--tier:${colour}`,
      }));
      // As wide as the calls are many. This is the one place the proportion is
      // the point: one dependency that matters and seven that do not.
      group.append(svgEl('rect', {
        x, y: y + PLT.sideH - 3,
        width: Math.max(2, PLT.sideW * ((call.operationCalls ?? 0) / most)),
        height: 3, rx: 1.5, fill: colour, opacity: 0.85,
      }));
      const name = svgEl('text', {
        x: x + 9, y: y + 18, class: 'dia-box-name', 'font-size': 10.5,
      });
      name.textContent = String(call.service).replace(/Service$/, '');
      group.append(name);
      const count = svgEl('text', {
        x: x + PLT.sideW - 9, y: y + 18, class: 'dia-box-counts',
        'font-size': 10.5, 'text-anchor': 'end',
      });
      count.textContent = String(call.operationCalls ?? 0);
      group.append(count);
      const title = svgEl('title');
      title.textContent = `${call.service} \u2014 ${call.operationCalls ?? 0} operation calls`;
      group.append(title);
      if (service) {
        const open = () => { selectService(service.key); setLayer('services'); setMode('service'); };
        group.addEventListener('click', open);
        group.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
        });
      }
      boxes.append(group);
      link({ x: coreX + PLT.coreW, y: coreY + PLT.coreH / 2 }, { x, y: y + PLT.sideH / 2 });
    });
  }

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);
  trimToBox(tight);
  wireIsolate(svg);
  // The picker moved, so the tree has to follow it.
  markTreeSelection();
  if (called.length > shown.length) {
    frame.append(el('div', 'dia-note',
      `${called.length - shown.length} further service${called.length - shown.length === 1 ? '' : 's'} `
      + `${called.length - shown.length === 1 ? 'is' : 'are'} called fewer times than these and `
      + 'listed below rather than drawn.'));
  }

  // ---- how it gets there -------------------------------------------------
  if (detail.deployment) {
    body.append(el('div', 'journey-section-label', 'how a release reaches it'));
    const stack = el('div', 'detail-stack');
    for (const [key, value] of Object.entries(detail.deployment)) {
      if (value == null || value === '') continue;
      const card = el('div', 'detail-card');
      card.append(el('div', 'detail-card-name',
        key.replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase()));
      card.append(proseLine(String(value)));
      stack.append(card);
    }
    body.append(stack);
  }

  if (coverage.note) {
    body.append(el('div', 'journey-section-label', 'flow coverage'));
    body.append(proseLine(coverage.note));
  }

  if (called.length) {
    body.append(el('div', 'journey-section-label',
      `${called.length} services called \u2014 by operation calls`));
    const chips = el('div', 'service-tables');
    for (const call of called) {
      chips.append(el('span', 'service-table',
        `${String(call.service).replace(/Service$/, '')} ${call.operationCalls ?? 0}`));
    }
    body.append(chips);
  }
}

// ── the contracts, drawn ───────────────────────────────
//
// Banded by tier, spine first, because the tier is the rule: a satellite reads
// down into the spine and is never read by it. Each box carries its verb mix as
// a bar — a contract that is nine tenths POST is a command surface, one that is
// nine tenths GET is a read model, and that is worth seeing rather than
// totting up.

const CTR = {
  width: 1160, boxW: 176, boxH: 62, gapX: 14, gapY: 12,
  bandPadX: 96, bandPadY: 30, bandGap: 24, perRow: 5,
};

const VERB_TOKENS = {
  GET: 'ok', POST: 'error', PUT: 'warning', PATCH: 'patch', DELETE: 'muted',
};
const TIER_ORDER = ['spine', 'satellite', 'shared'];

function renderContractsHld() {
  const body = $('contracts-hld-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  const doc = diagrams?.contracts;
  if (!doc?.present) {
    body.append(el('p', 'pane-empty',
      'This package has no diagrams/hld/03-contracts.yaml.'));
    $('contracts-hld-hint').textContent = '';
    return;
  }

  const contracts = doc.contracts ?? [];
  const total = contracts.reduce((a, c) => a + (c.operations ?? 0), 0);
  $('contracts-hld-hint').textContent =
    `${contracts.length} contracts \u00b7 ${total} operations \u00b7 `
    + `${contracts.filter((c) => (c.events ?? []).length).length} emit events`;
  // The edge count is appended once the edges are known, at the end of the
  // render — it is the one figure here that is computed rather than read.

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'High-level design \u00b7 the API'));
  head.append(el('h2', 'journey-title', doc.title ?? '28 contracts'));
  head.append(sourceLine(doc.file, doc.generatedBy ?? diagrams.generatedBy));
  body.append(head);

  // Tiers in dependency order, then whatever the file names that this does not.
  const tiers = doc.tiers ?? {};
  const order = [
    ...TIER_ORDER.filter((t) => contracts.some((c) => c.tier === t)),
    ...[...new Set(contracts.map((c) => c.tier))]
      .filter((t) => t && !TIER_ORDER.includes(t)),
  ];

  let y = 12;
  const bands = [];
  for (const tier of order) {
    const list = contracts
      .filter((c) => c.tier === tier)
      .sort((a, b) => (b.operations ?? 0) - (a.operations ?? 0));
    const rows = Math.ceil(list.length / CTR.perRow) || 1;
    const height = CTR.bandPadY + rows * CTR.boxH + (rows - 1) * CTR.gapY + 16;
    bands.push({ tier, list, y, height });
    y += height + CTR.bandGap;
  }
  const height = y + 4;

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${CTR.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });
  const defs = svgEl('defs');
  const marker = svgEl('marker', {
    id: 'ctr-head', viewBox: '0 0 8 8', refX: 7, refY: 4,
    markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse',
  });
  marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: 'dia-arrow-head' }));
  defs.append(marker);
  svg.append(defs);
  // The band panels go down first, then the lanes, then the boxes. Order is the
  // whole of it: the bands were painted after the lanes, so 57 arrows crossing
  // three opaque panels were visible only in the two gaps between them.
  const bandArt = svgEl('g', { class: 'dia-bands' });
  svg.append(bandArt);
  // Under the boxes: a line that runs the width of the diagram should pass
  // behind what it connects rather than across it.
  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  const boxes = svgEl('g', { class: 'dia-boxes' });
  const tight = [];
  // Where each contract's box landed, so the edges below can find both ends.
  // Not `at`: the verb-mix bar already uses that name as its cursor inside the
  // same block, and this was landing in its dead zone.
  const placed = new Map();

  for (const band of bands) {
    bandArt.append(svgEl('rect', {
      x: 8, y: band.y, width: CTR.width - 16, height: band.height,
      rx: 10, class: 'dia-band',
    }));
    const label = svgEl('text', {
      x: 22, y: band.y + 20, class: 'dia-band-label', 'font-size': 10.5,
    });
    label.textContent = `${band.tier.toUpperCase()}  ${band.list.length}`;
    svg.append(label);
    if (tiers[band.tier]) {
      const meaning = svgEl('title');
      meaning.textContent = String(tiers[band.tier]).replace(/\*\*/g, '');
      label.append(meaning);
    }

    band.list.forEach((contract, i) => {
      const row = Math.floor(i / CTR.perRow);
      const col = i % CTR.perRow;
      const wide = Math.min(band.list.length - row * CTR.perRow, CTR.perRow);
      const span = wide * CTR.boxW + (wide - 1) * CTR.gapX;
      const x = CTR.bandPadX + (CTR.width - 2 * CTR.bandPadX - span) / 2
        + col * (CTR.boxW + CTR.gapX);
      const top = band.y + CTR.bandPadY + row * (CTR.boxH + CTR.gapY);
      const owner = (diagrams.services ?? []).find((v) => v.name === contract.service);
      const colour = owner ? tierColour(owner.tier) : hue('muted');

      const group = svgEl('g', { class: 'dia-box', tabindex: 0 });
      placed.set(contract.contract, { x, y: top, w: CTR.boxW, h: CTR.boxH });
      group.append(svgEl('rect', {
        x, y: top, width: CTR.boxW, height: CTR.boxH, rx: 6,
        class: 'dia-box-bg', style: `--tier:${colour}`,
      }));
      group.append(svgEl('rect', {
        x, y: top, width: 3, height: CTR.boxH, fill: colour, rx: 1.5,
      }));

      const name = svgEl('text', {
        x: x + 11, y: top + 19, class: 'dia-box-name', 'font-size': 12,
      });
      name.textContent = fit(contract.contract, CTR.boxW - 60, 12);
      group.append(name);
      tight.push([name, CTR.boxW - 60]);

      const ops = svgEl('text', {
        x: x + CTR.boxW - 11, y: top + 19, class: 'dia-box-counts',
        'font-size': 11, 'text-anchor': 'end',
      });
      ops.textContent = String(contract.operations ?? 0);
      group.append(ops);

      const sub = svgEl('text', {
        x: x + 11, y: top + 33, class: 'dia-box-counts', 'font-size': 9.5,
      });
      const marks = [];
      if (contract.guestCallable) marks.push(`${contract.guestCallable} guest`);
      if (contract.offlineCapable) marks.push(`${contract.offlineCapable} offline`);
      if ((contract.events ?? []).length) marks.push(`${contract.events.length} events`);
      sub.textContent = fit(marks.join(' \u00b7 ') || 'no guest, offline or event operations',
        CTR.boxW - 22, 9.5);
      group.append(sub);
      tight.push([sub, CTR.boxW - 22]);

      // The verb mix. Stacked rather than five numbers, because the shape of a
      // contract is the proportion and not the counts.
      const verbs = Object.entries(contract.verbs ?? {})
        .filter(([, n]) => n > 0)
        .sort((a, b) => b[1] - a[1]);
      const sum = verbs.reduce((a, [, n]) => a + n, 0) || 1;
      let at = x + 11;
      const barW = CTR.boxW - 22;
      for (const [verb, n] of verbs) {
        const w = (barW * n) / sum;
        const seg = svgEl('rect', {
          x: at, y: top + 42, width: Math.max(1, w), height: 5, rx: 2,
          fill: hue(VERB_TOKENS[verb] ?? 'muted'), opacity: 0.85,
        });
        const label = svgEl('title');
        label.textContent = `${verb} ${n}`;
        seg.append(label);
        group.append(seg);
        at += w + 1;
      }

      const service = svgEl('text', {
        x: x + 11, y: top + 56, class: 'dia-box-counts', 'font-size': 9.5,
      });
      service.textContent = fit(String(contract.service ?? 'no service')
        .replace(/Service$/, ''), CTR.boxW - 22, 9.5);
      group.append(service);

      const title = svgEl('title');
      title.textContent =
        `${contract.contract} \u00b7 ${contract.tier}\n`
        + `${contract.operations ?? 0} operations, served by ${contract.service ?? 'nobody'}\n`
        + verbs.map(([v, n]) => `${v} ${n}`).join(', ')
        + ((contract.events ?? []).length ? `\nemits ${contract.events.join(', ')}` : '');
      group.append(title);

      const open = () => openContract(contract.contract);
      group.addEventListener('click', open);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
      });
      boxes.append(group);
    });
  }
  svg.append(boxes);

  // ---- what one contract takes from another -----------------------------
  //
  // Already in the index: `fileEdges` is the file-level aggregate the indexer
  // folds every resolved `$ref` into, weighted by how many crossed. Nothing new
  // is read and `03-contracts.yaml` carries no dependency of any kind.
  const stemOf = (id) => String(id).replace(/^file:/, '').split('/').pop()
    .replace(/\.ya?ml$/, '');
  const pairs = [];
  for (const edge of state.index?.fileEdges ?? []) {
    const from = stemOf(edge.source);
    const to = stemOf(edge.target);
    if (from === to || !placed.has(from) || !placed.has(to)) continue;
    pairs.push({ from, to, weight: edge.weight ?? 1 });
  }
  // An edge every node has is an edge that says nothing about any node — the
  // same problem the data view solves for `platform.scope_node`. A target more
  // than half the contracts reference is ambient. Counted rather than named, so
  // a package where the shared vocabulary moved redraws itself.
  const referrers = new Map();
  for (const { from, to } of pairs) {
    if (!referrers.has(to)) referrers.set(to, new Set());
    referrers.get(to).add(from);
  }
  const ambient = new Set([...referrers]
    .filter(([, who]) => who.size > contracts.length / 2)
    .map(([to]) => to));
  // On by default. The fan into the two shared contracts *is* the finding here
    // — one shared vocabulary and almost no other coupling — and a reader cannot
  // see that from a diagram that withholds it. The toggle turns it off for the
  // reading where the fan is in the way.
  const showShared = $('contracts-shared')?.checked ?? true;
  const drawn = pairs.filter((p) => showShared || !ambient.has(p.to));

  for (const pair of drawn) {
    const a = placed.get(pair.from);
    const b = placed.get(pair.to);
    const shared = ambient.has(pair.to);
    // Down the page where the target is below, and round the row where the two
    // sit in the same one.
    //
    // *Round*, not across: a curve along a band row passes behind every box
    // between its ends, and lanes are drawn under boxes on purpose — so the one
    // edge on this diagram that is not part of the shared fan was invisible.
    // It leaves the bottom of one box, dips clear of the row, and comes up into
    // the bottom of the other.
    let d;
    if (b.y >= a.y + a.h) {
      const from = { x: a.x + a.w / 2, y: a.y + a.h };
      const to = { x: b.x + b.w / 2, y: b.y };
      const bend = Math.max(18, (to.y - from.y) * 0.4);
      d = `M ${from.x} ${from.y} C ${from.x} ${from.y + bend}, `
        + `${to.x} ${to.y - bend}, ${to.x} ${to.y}`;
    } else if (b.y + b.h <= a.y) {
      const from = { x: a.x + a.w / 2, y: a.y };
      const to = { x: b.x + b.w / 2, y: b.y + b.h };
      const bend = Math.max(18, (from.y - to.y) * 0.4);
      d = `M ${from.x} ${from.y} C ${from.x} ${from.y - bend}, `
        + `${to.x} ${to.y + bend}, ${to.x} ${to.y}`;
    } else {
      const from = { x: a.x + a.w / 2, y: a.y + a.h };
      const to = { x: b.x + b.w / 2, y: b.y + b.h };
      const under = Math.max(from.y, to.y) + 26;
      d = `M ${from.x} ${from.y} C ${from.x} ${under}, `
        + `${to.x} ${under}, ${to.x} ${to.y}`;
    }
    const path = svgEl('path', {
      d,
      // The shared fan reads as a fan; the one coupling that is not shared reads
      // as a line. `.soft` at 13% was a hint rather than either.
      class: `dia-arrow${shared ? '' : ' strong'}`,
      style: shared ? 'opacity:.3' : null,
      'marker-end': 'url(#ctr-head)',
    });
    const label = svgEl('title');
    label.textContent = `${pair.from} → ${pair.to} · `
      + `${pair.weight} reference${pair.weight === 1 ? '' : 's'}`;
    path.append(label);
    lanes.append(path);
  }

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);
  trimToBox(tight);
  wireIsolate(svg);

  // What is not on the page, said on the page. A quiet diagram and a sparse
  // one look identical, and only one of them is true here.
  const withheld = pairs.length - drawn.length;
  const own = drawn.filter((p) => !ambient.has(p.to)).length;
  frame.append(el('div', 'dia-note', withheld
    ? `${withheld} edge${withheld === 1 ? '' : 's'} into `
      + `${[...ambient].sort().join(' and ')} `
      + `${withheld === 1 ? 'is' : 'are'} hidden — Shared vocabulary draws `
      + `${withheld === 1 ? 'it' : 'them'} again.`
    : `${drawn.length} edges, and ${drawn.length - own} of them go into `
      + `${[...ambient].sort().join(' and ')}, which nearly every contract references — `
      + `drawn quietly, because the fan is the point. `
      + `${own === 1 ? 'The one in red is the only place' : `The ${own} in red are the places`} `
      + `one contract reaches into another's vocabulary.`));

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [
    [hue('error'), 'POST'], [hue('ok'), 'GET'], [hue('warning'), 'PUT'],
    [hue('patch'), 'PATCH'], [hue('muted'), 'DELETE'],
  ], 'the bar is the verb mix · the left rule is the tier of the service that serves it · '
    + 'a line is one contract referencing another, weighted by how many refs cross · '
    + 'click a contract to open it');

  if (doc.about) {
    body.append(el('div', 'journey-section-label', 'what this says'));
    body.append(proseLine(doc.about));
  }
  if (Object.keys(tiers).length) {
    body.append(el('div', 'journey-section-label', 'what a tier means'));
    const stack = el('div', 'detail-stack');
    for (const [tier, meaning] of Object.entries(tiers)) {
      const card = el('div', 'detail-card');
      card.append(el('div', 'detail-card-name', tier));
      card.append(proseLine(meaning));
      stack.append(card);
    }
    body.append(stack);
  }
}

// \u2500\u2500 the lifecycles, drawn \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
//
// 113 state models, banded by the contract that owns them. Too many to draw as
// 113 labelled boxes and exactly right to draw as 113 small ones: the band says
// where the complexity sits before a name is read, and it sits very unevenly.
//
// A box is as wide as its transitions and marked when every transition on it is
// guarded. The 29 events are listed rather than drawn \u2014 an event crosses
// between two models and the file names neither end, so an edge here would be
// an edge invented here.

const LIF = {
  width: 1160, boxW: 156, boxH: 30, gapX: 8, gapY: 7,
  bandPadX: 150, bandPadY: 7, bandGap: 7, perRow: 6,
};

function renderLifecyclesHld() {
  const body = $('lifecycles-hld-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  const doc = diagrams?.lifecycles;
  if (!doc?.present) {
    body.append(el('p', 'pane-empty',
      'This package has no diagrams/hld/04-lifecycles.yaml.'));
    $('lifecycles-hld-hint').textContent = '';
    return;
  }

  const models = doc.stateModels ?? [];
  const events = doc.events ?? [];
  const transitions = models.reduce((a, m) => a + (m.transitions ?? 0), 0);
  const guarded = models.reduce((a, m) => a + (m.guarded ?? 0), 0);

  // The low-level rows know which models emit \u2014 the index rows do not.
  const emitsBy = new Map(
    (diagrams.lld?.lifecycles ?? []).map((r) => [r.entity, r.emits ?? 0]));
  const emitting = models.filter((m) => (emitsBy.get(m.entity) ?? 0) > 0).length;

  $('lifecycles-hld-hint').textContent =
    `${models.length} state models \u00b7 ${transitions} transitions \u00b7 `
    + `${guarded} guarded \u00b7 ${emitting} emit`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'High-level design \u00b7 what can happen'));
  head.append(el('h2', 'journey-title', doc.title ?? 'The lifecycles'));
  head.append(sourceLine(doc.file, doc.generatedBy ?? diagrams.generatedBy));
  body.append(head);

  // Heaviest band first: the question this answers is where the behaviour
  // lives, and the answer should be at the top.
  const byOwner = new Map();
  for (const model of models) {
    const owner = model.contract ?? model.owner ?? 'unowned';
    if (!byOwner.has(owner)) byOwner.set(owner, []);
    byOwner.get(owner).push(model);
  }
  const bands = [...byOwner.entries()]
    .map(([owner, list]) => ({
      owner,
      list: list.slice().sort((a, b) => (b.transitions ?? 0) - (a.transitions ?? 0)),
      weight: list.reduce((a, m) => a + (m.transitions ?? 0), 0),
    }))
    .sort((a, b) => b.weight - a.weight);

  let y = 10;
  for (const band of bands) {
    band.rowCount = Math.ceil(band.list.length / LIF.perRow) || 1;
    band.y = y;
    band.height = LIF.bandPadY * 2
      + band.rowCount * LIF.boxH + (band.rowCount - 1) * LIF.gapY;
    y += band.height + LIF.bandGap;
  }
  const height = y + 4;

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${LIF.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });
  const boxes = svgEl('g', { class: 'dia-boxes' });
  const tight = [];

  for (const band of bands) {
    const label = svgEl('text', {
      x: LIF.bandPadX - 14, y: band.y + LIF.bandPadY + 19,
      class: 'dia-band-label', 'font-size': 10.5, 'text-anchor': 'end',
    });
    label.textContent = `${band.owner}  ${band.list.length}`;
    // The band is a contract, and a contract is a thing this viewer holds.
    // Only where it resolves \u2014 `unowned` is a band too, and it is not a file.
    if ((state.index?.nodes ?? []).some(
      (n) => n.type === 'file'
        && String(n.file ?? '').split('/').pop().replace(/\.ya?ml$/, '') === band.owner)) {
      label.classList.add('linked');
      label.setAttribute('tabindex', '0');
      const open = () => openContract(band.owner);
      label.addEventListener('click', open);
      label.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
      });
    }
    svg.append(label);

    band.list.forEach((model, i) => {
      const row = Math.floor(i / LIF.perRow);
      const col = i % LIF.perRow;
      const x = LIF.bandPadX + col * (LIF.boxW + LIF.gapX);
      const top = band.y + LIF.bandPadY + row * (LIF.boxH + LIF.gapY);
      const owner = (diagrams.services ?? []).find((v) => v.name === model.service);
      const colour = owner ? tierColour(owner.tier) : hue('muted');
      const emits = emitsBy.get(model.entity) ?? 0;

      const group = svgEl('g', { class: 'dia-box', tabindex: 0 });
      group.append(svgEl('rect', {
        x, y: top, width: LIF.boxW, height: LIF.boxH, rx: 5,
        class: 'dia-box-bg', style: `--tier:${colour}`,
      }));
      group.append(svgEl('rect', {
        x, y: top, width: 2.5, height: LIF.boxH, fill: colour, rx: 1.25,
      }));

      const name = svgEl('text', {
        x: x + 8, y: top + 13, class: 'dia-box-name', 'font-size': 10,
      });
      name.textContent = fit(model.entity, LIF.boxW - 16, 10);
      group.append(name);
      tight.push([name, LIF.boxW - 16]);

      const sub = svgEl('text', {
        x: x + 8, y: top + 24, class: 'dia-box-counts', 'font-size': 9,
      });
      sub.textContent = `${model.transitions ?? 0} transitions`
        + ((model.guarded ?? 0) < (model.transitions ?? 0)
          ? ` \u00b7 ${(model.transitions ?? 0) - (model.guarded ?? 0)} unguarded` : '');
      group.append(sub);
      tight.push([sub, LIF.boxW - 30]);

      // An emitting model is somebody else's problem as well as its own, which
      // is the one property here that changes who has to care.
      if (emits > 0) {
        const dot = svgEl('circle', {
          cx: x + LIF.boxW - 9, cy: top + 10, r: 3.2,
          fill: hue('warning'), opacity: 0.9,
        });
        const why = svgEl('title');
        why.textContent = `emits ${emits} event${emits === 1 ? '' : 's'}`;
        dot.append(why);
        group.append(dot);
      }

      const title = svgEl('title');
      title.textContent =
        `${model.entity}\n${model.transitions ?? 0} transitions, `
        + `${model.guarded ?? 0} guarded\n`
        + `starts ${(model.initial ?? []).join(', ') || 'nowhere stated'} \u2192 `
        + `ends ${(model.terminal ?? []).join(', ') || 'nowhere stated'}`
        + (model.service ? `\n${model.service}` : '')
        + (emits ? `\nemits ${emits}` : '');
      group.append(title);

      const open = () => openStateModel(model.entity);
      group.addEventListener('click', open);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
      });
      boxes.append(group);
    });
  }
  svg.append(boxes);

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);
  trimToBox(tight);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [
    ...(diagrams.tiers ?? []).map((t) => [tierColour(t.tier), t.tier]),
    [hue('warning'), 'emits an event'],
  ], 'a band is the contract that owns the model \u00b7 the colour is the service that '
    + 'serves it, which is a different cut \u00b7 click a model to open it');

  if (doc.about) {
    body.append(el('div', 'journey-section-label', 'what this says'));
    body.append(proseLine(doc.about));
  }
  // The file argues for the rename this layer has now had; keeping it visible
  // is how the argument outlives whoever made it.
  if (doc.naming) {
    body.append(el('div', 'journey-section-label', 'why this layer is called Lifecycles'));
    body.append(proseLine(doc.naming));
  }
  if (events.length) {
    body.append(el('div', 'journey-section-label',
      `${events.length} events \u2014 a lifecycle crossing between two things`));
    // An event named here is an event the Events view draws \u2014 but the two files
    // do not spell it the same way. `events/` says `approval.granted`; the
    // diagram says `approval-granted`. Neither is wrong and neither is going to
    // change, so both fold to a key, exactly as the services do for
    // `OrderService` against `Order`.
    //
    // Comparing the raw strings would have linked none of the 29 while looking
    // like code that works. `openEvent` gets the name `events/` knows, because
    // that is the name the select on the other side is built from.
    const foldEvent = (name) => String(name ?? '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const knownBy = new Map(
      (state.domain?.events ?? []).map((e) => [foldEvent(e.name ?? e.id), e.name ?? e.id]));
    const stack = el('div', 'detail-stack');
    for (const event of events) {
      const real = knownBy.get(foldEvent(event.event)) ?? null;
      const card = el('div', `detail-card${real ? ' linked' : ''}`);
      card.append(el('div', 'detail-card-name', event.event));
      if (event.description) card.append(proseLine(event.description));
      if (real) {
        card.tabIndex = 0;
        card.title = `Open ${real} in Events`;
        card.onclick = () => openEvent(real);
        card.onkeydown = (e) => {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openEvent(real); }
        };
      }
      stack.append(card);
    }
    body.append(stack);
  }
}

// ── the platform, drawn ────────────────────────────────
//
// Five columns, left to right in the order a request travels: who uses it, on
// what surface, against which services, over which stores, and what sits
// outside. All four joins are drawn.
//
// Services-to-stores is not stated in `00-platform.yaml`, which counts the
// stores and joins them to nothing. It is stated a level down: every table in a
// service's LLD carries a `store`, so a service's stores are its tables' stores,
// tallied. Nothing is invented and the tally is the weight on the line.
//
// Each header names the question the column answers; the line under it names
// what the boxes in it are, in the word the rest of the package files them
// under — `ON WHAT` is fifteen *platforms*, and a reader who has not already
// made that connection had no way to make it here.

const OVW = {
  width: 1080,
  rowH: 30,
  gap: 6,
  padX: 24,
  headY: 26,
  // Room for the header and the noun under it, above the first box.
  topPad: 30,
  cols: [
    { key: 'actors', label: 'WHO USES IT', kind: 'actors', w: 138 },
    { key: 'surfaces', label: 'ON WHAT', kind: 'platforms', w: 196 },
    { key: 'services', label: 'AGAINST WHAT', kind: 'services', w: 150 },
    { key: 'stores', label: 'OVER WHAT', kind: 'stores', w: 128 },
    { key: 'external', label: 'AND OUTSIDE IT', kind: 'outside systems', w: 178 },
  ],
};

/** Who a surface is for, as a colour. */
const AUDIENCE_TOKENS = {
  guest: 'ok', staff: 'error', partner: 'warning',
  operator: 'muted', developer: 'patch', device: 'patch',
};
const audienceColour = (who) => hue(AUDIENCE_TOKENS[String(who ?? '').toLowerCase()] ?? 'muted');

/**
 * Trim labels that turned out not to fit, once the diagram is in the page.
 *
 * `fit` below has to guess, because a box's width is decided before anything is
 * drawn and a guess is all there is at that point. The browser knows exactly,
 * but only for a node that is in the document — `getComputedTextLength` returns
 * 0 on a detached one — so the exact answer can only be applied afterwards.
 *
 * Nothing is re-laid out. A label that overran the box it already has is cut to
 * the box it already has.
 */
function trimToBox(pairs) {
  for (const [node, max] of pairs) {
    if (!node.isConnected || node.getComputedTextLength() <= max) continue;
    let text = node.textContent.replace(/\u2026$/, '');
    while (text.length > 1) {
      text = text.slice(0, -1);
      node.textContent = `${text}\u2026`;
      if (node.getComputedTextLength() <= max) break;
    }
  }
}

/**
 * Hovering a box lights the boundaries that are its own.
 *
 * The Overview and the services HLD do this themselves, because their arrows
 * carry a pair of keys naming the boxes at either end. The platform design, the
 * scope hierarchy and one service's LLD draw `link(a, b)` from two points and
 * have no keys to write — so this asks the geometry the same question.
 *
 * Every arrow in these diagrams begins and ends on a box's edge; that is how
 * they were laid out. So the two endpoints name the two boxes, and the smallest
 * box containing an endpoint is the one it was drawn for — which matters where a
 * small box sits against a large one.
 *
 * Call it after the diagram is in the page. Nothing here measures rendered text,
 * but a detached node is a node whose geometry a browser is free to decline.
 */
function wireIsolate(svg) {
  const arrows = [...svg.querySelectorAll('.dia-arrow')];
  const at = [...svg.querySelectorAll('.dia-box')]
    .map((group) => ({ group, rect: group.querySelector('rect') }))
    .filter((b) => b.rect)
    .map(({ group, rect }) => ({
      group,
      x: Number(rect.getAttribute('x')),
      y: Number(rect.getAttribute('y')),
      w: Number(rect.getAttribute('width')),
      h: Number(rect.getAttribute('height')),
    }));
  if (!arrows.length || !at.length) return;

  const TOL = 5; // an endpoint sits *on* an edge, and a curve's first point rounds
  const boxAt = (point) => at
    .filter((b) => point.x >= b.x - TOL && point.x <= b.x + b.w + TOL
      && point.y >= b.y - TOL && point.y <= b.y + b.h + TOL)
    .sort((a, b) => a.w * a.h - b.w * b.h)[0] ?? null;

  const ends = new Map();
  for (const arrow of arrows) {
    const length = arrow.getTotalLength();
    const own = new Set();
    for (const point of [arrow.getPointAtLength(0), arrow.getPointAtLength(length)]) {
      const hit = boxAt(point);
      if (hit) own.add(hit.group);
    }
    ends.set(arrow, own);
  }

  const light = (group, on) => {
    svg.classList.toggle('lit', on);
    // A box at the far end of one of this box's boundaries is part of the
    // answer, so it stays bright with it.
    const reached = new Set();
    for (const arrow of arrows) {
      const mine = on && ends.get(arrow).has(group);
      arrow.classList.toggle('lit', mine);
      if (mine) for (const other of ends.get(arrow)) reached.add(other);
    }
    for (const b of at) {
      b.group.classList.toggle('lit', on && (b.group === group || reached.has(b.group)));
    }
  };

  for (const b of at) {
    b.group.addEventListener('mouseenter', () => light(b.group, true));
    b.group.addEventListener('mouseleave', () => light(b.group, false));
    b.group.addEventListener('focus', () => light(b.group, true));
    b.group.addEventListener('blur', () => light(b.group, false));
  }
}

/** As much of a label as fits, with the whole of it in the tooltip. */
function fit(text, width, size = 10.5) {
  const room = Math.floor(width / (size * 0.53));
  const flat = String(text ?? '');
  return flat.length <= room ? flat : flat.slice(0, Math.max(1, room - 1)) + '\u2026';
}

function renderOverview() {
  const body = $('overview-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  const doc = diagrams?.platform;
  if (!doc?.present) {
    body.append(el('p', 'pane-empty',
      'This package has no diagrams/hld/00-platform.yaml.'));
    $('overview-hint').textContent = '';
    return;
  }

  // `callsServices` and `via` name a service the way the diagrams spell it
  // — `OrderService`. The payload holds them under a folded key. Built once,
  // because the surface column alone asks this 121 times.
  const keyByName = new Map((diagrams.services ?? []).map((v) => [v.name, v.key]));

  const actors = doc.actors ?? [];
  const surfaces = doc.surfaces ?? [];
  const services = diagrams.services ?? [];
  const stores = doc.stores ?? [];
  const external = doc.external ?? [];

  // ---- which store each service sits on ---------------------------------
  //
  // The join the platform file does not state and the file below it does. Every
  // table in a service's LLD carries a `store`; a service's stores are its
  // tables' stores, and the count is the weight on the line. `tableDetail` has
  // been in the payload since the reader was written — this page had simply
  // never asked it.
  const storeNames = new Set(stores.map((t) => t.store));
  const storeUse = new Map(); // service key \u2192 Map(store \u2192 tables)
  for (const v of services) {
    const tally = new Map();
    for (const table of v.tableDetail ?? []) {
      if (!storeNames.has(table.store)) continue;
      tally.set(table.store, (tally.get(table.store) ?? 0) + 1);
    }
    // A schema named after a store is a store the service uses with no tables of
    // its own — AiService against qdrant, which is a vector index rather than
    // anything the workbook has rows for. Zero is the true weight, not a reason
    // to drop the line.
    for (const schema of v.schemas ?? []) {
      if (storeNames.has(schema) && !tally.has(schema)) tally.set(schema, 0);
    }
    if (tally.size) storeUse.set(v.key, tally);
  }
  // A store every service uses says nothing about any one of them, and sixteen
  // lines into one box hide the four that matter. Counted rather than named, so
  // a package that moves off Postgres redraws itself.
  const ubiquitous = new Set([...storeNames].filter((name) =>
    services.length > 1 && services.every((v) => storeUse.get(v.key)?.has(name))));
  const tablesInStore = new Map();
  for (const tally of storeUse.values()) {
    for (const [store, n] of tally) tablesInStore.set(store, (tablesInStore.get(store) ?? 0) + n);
  }

  $('overview-hint').textContent =
    `${actors.length} actors \u00b7 ${surfaces.length} surfaces \u00b7 `
    + `${services.length} services \u00b7 ${stores.length} stores \u00b7 ${external.length} outside`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'High-level design \u00b7 the whole system'));
  head.append(el('h2', 'journey-title', doc.title ?? 'The platform'));
  head.append(sourceLine(doc.file, doc.generatedBy ?? diagrams.generatedBy));
  body.append(head);

  // ---- the columns ------------------------------------------------------
  const rows = {
    actors: actors.map((a) => ({
      key: `actor:${a.actor}`,
      name: a.actor,
      sub: `${a.operations ?? 0} operations`,
      colour: audienceColour(a.actor === 'venue staff' ? 'staff' : a.actor),
      tip: a.note ? a.note.replace(/\*\*/g, '') : null,
      out: (a.reaches ?? []).map((code) => `surface:${code}`),
    })),
    surfaces: surfaces.map((f) => ({
      key: `surface:${f.platform}`,
      name: `${f.platform} ${f.name}`,
      sub: `${f.screens ?? 0} screens \u00b7 ${(f.modules ?? []).length} modules`
        + (f.offlineCapable ? ' \u00b7 offline' : ''),
      colour: audienceColour(f.audience),
      tip: `${f.name}\n${f.audience} \u00b7 ${f.app} \u00b7 ${f.formFactor}`,
      out: (f.callsServices ?? [])
        .map((n) => keyByName.get(n))
        .filter(Boolean)
        .map((k) => `service:${k}`),
      // Was the Apps map, which was the best answer available when nothing drew
      // one platform. The Platform view does now.
      go: () => {
        state.platformKey = f.platform;
        setLayer('frontend');
        setMode('platform-lld');
      },
    })),
    services: services.map((v) => ({
      key: `service:${v.key}`,
      name: v.name.replace(/Service$/, ''),
      sub: `${v.operations ?? 0} ops \u00b7 ${v.tier}`,
      colour: tierColour(v.tier),
      tip: v.scale ? v.scale.replace(/\*\*/g, '') : null,
      out: [...(storeUse.get(v.key) ?? new Map())].map(([store, tables]) => ({
        to: `store:${store}`,
        soft: ubiquitous.has(store),
        note: tables
          ? `${v.name} \u2192 ${store} \u00b7 ${tables} ${tables === 1 ? 'table' : 'tables'}`
          : `${v.name} \u2192 ${store} \u00b7 declared as a schema, no tables of its own`,
      })),
      go: () => { selectService(v.key); setMode('service'); },
    })),
    stores: stores.map((t) => ({
      key: `store:${t.store}`,
      name: t.store,
      sub: `${t.operations ?? 0} ops`
        + (tablesInStore.get(t.store) ? ` \u00b7 ${tablesInStore.get(t.store)} tables` : ''),
      colour: hue('muted'),
      tip: t.note ? t.note.replace(/\*\*/g, '') : null,
    })),
    // `via` is one service or several — the payment gateway names one, messaging
    // names six — and reading it as a string drew a line for the scalars and
    // nothing at all for the lists. Six lines out of messaging is the file's own
    // finding: one dispatch table, six services that send through it.
    external: external.map((x) => {
      const via = (Array.isArray(x.via) ? x.via : [x.via]).filter(Boolean).map(String);
      const known = via.map((name) => keyByName.get(name)).filter(Boolean);
      return {
        key: `external:${x.system}`,
        name: x.system,
        // A name where there is one; a count where there are more, because six
        // of them do not fit in 178px and a truncated list names nobody. The
        // hover has them in full.
        sub: known.length === 1
          ? `via ${via[0].replace(/Service$/, '')}`
          : `via ${via.length} services`,
        colour: hue('warning'),
        tip: [
          via.length > 1 ? via.map((n) => n.replace(/Service$/, '')).join(', ') : null,
          // The table the traffic lands in, which this page had never shown and
          // which is the thing a reader chasing a boundary actually wants.
          x.reachedThrough ? `reaches ${x.reachedThrough}` : null,
          x.note ? x.note.replace(/\*\*/g, '') : null,
        ].filter(Boolean).join('\n') || null,
        out: known.map((key) => `service:${key}`),
      };
    }),
  };

  const tallest = Math.max(...OVW.cols.map((c) => rows[c.key].length));
  const height = OVW.headY + OVW.topPad + tallest * (OVW.rowH + OVW.gap) + 20;

  const svg = svgEl('svg', {
    class: 'dia ovw', viewBox: `0 0 ${OVW.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });

  const defs = svgEl('defs');
  const marker = svgEl('marker', {
    id: 'ovw-head', viewBox: '0 0 8 8', refX: 7, refY: 4,
    markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse',
  });
  marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: 'dia-arrow-head' }));
  defs.append(marker);
  svg.append(defs);

  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  const boxes = svgEl('g', { class: 'dia-boxes' });
  svg.append(boxes);

  // Lay every column out first: an edge has to know where both ends are, and
  // half of them run backwards up the page.
  const at = new Map();
  let x = OVW.padX;
  for (const col of OVW.cols) {
    const list = rows[col.key];
    const top = OVW.headY + OVW.topPad
      + ((tallest - list.length) * (OVW.rowH + OVW.gap)) / 2;
    const label = svgEl('text', {
      x, y: OVW.headY, class: 'dia-band-label', 'font-size': 10,
    });
    label.textContent = col.label;
    svg.append(label);
    // The header says what the column is for; this says what is in it.
    const kind = svgEl('text', {
      x, y: OVW.headY + 13, class: 'dia-band-kind', 'font-size': 9.5,
    });
    kind.textContent = `${list.length} ${col.kind}`;
    svg.append(kind);
    list.forEach((row, i) => {
      at.set(row.key, {
        row, col,
        x, y: top + i * (OVW.rowH + OVW.gap), w: col.w, h: OVW.rowH,
      });
    });
    x += col.w + (OVW.width - 2 * OVW.padX
      - OVW.cols.reduce((a, c) => a + c.w, 0)) / (OVW.cols.length - 1);
  }

  // ---- the joins the file states ---------------------------------------
  //
  // Actor to surface and outside-system to service are drawn at rest: there are
  // twenty-odd of them and each is a fact somebody should see without asking.
  // Surface to service is 121 lines, which at rest is a grey wash that answers
  // nothing \u2014 dim until a box is hovered, then only that box's own.
  //
  // An entry in `out` is a key, or a key with something to say about itself: the
  // store lines carry their weight and choose their own softness, because how
  // many tables a service keeps in a store is the fact the line is *for*.
  const edges = [];
  for (const [key, box] of at) {
    for (const target of box.row.out ?? []) {
      const spec = typeof target === 'string' ? { to: target } : target;
      const other = at.get(spec.to);
      if (!other) continue;
      const soft = spec.soft ?? (box.col.key === 'surfaces');
      const path = svgEl('path', {
        d: `M ${box.x + box.w} ${box.y + box.h / 2} `
          + `C ${box.x + box.w + 26} ${box.y + box.h / 2}, `
          + `${other.x - 26} ${other.y + other.h / 2}, `
          + `${other.x} ${other.y + other.h / 2}`,
        class: `dia-arrow${soft ? ' soft' : ''}`,
        'marker-end': 'url(#ovw-head)',
        'data-from': key, 'data-to': spec.to,
      });
      if (spec.note) {
        const label = svgEl('title');
        label.textContent = spec.note;
        path.append(label);
      }
      lanes.append(path);
      edges.push(path);
    }
  }
  // External sits to the right of services, so its arrow runs backwards; the
  // curve above assumed left-to-right and would loop. Redraw those from the
  // left edge instead.
  for (const path of edges) {
    const from = at.get(path.dataset.from);
    const to = at.get(path.dataset.to);
    if (!from || !to || from.x < to.x) continue;
    path.setAttribute('d',
      `M ${from.x} ${from.y + from.h / 2} `
      + `C ${from.x - 26} ${from.y + from.h / 2}, `
      + `${to.x + to.w + 26} ${to.y + to.h / 2}, `
      + `${to.x + to.w} ${to.y + to.h / 2}`);
  }

  // ---- the boxes --------------------------------------------------------
  for (const [key, box] of at) {
    const { row } = box;
    const group = svgEl('g', {
      class: 'dia-box', 'data-key': key, tabindex: row.go ? 0 : null,
    });
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: box.w, height: box.h, rx: 5,
      class: 'dia-box-bg', style: `--tier:${row.colour}`,
    }));
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: 2.5, height: box.h, fill: row.colour, rx: 1.25,
    }));
    const name = svgEl('text', {
      x: box.x + 9, y: box.y + 13, class: 'dia-box-name', 'font-size': 10.5,
    });
    name.textContent = fit(row.name, box.w - 16, 10.5);
    group.append(name);
    const sub = svgEl('text', {
      x: box.x + 9, y: box.y + 24, class: 'dia-box-counts', 'font-size': 9.5,
    });
    sub.textContent = fit(row.sub, box.w - 16, 9.5);
    group.append(sub);

    const title = svgEl('title');
    title.textContent = row.name + (row.tip ? `\n${row.tip}` : '');
    group.append(title);

    const light = (on) => {
      svg.classList.toggle('lit', on);
      for (const path of edges) {
        path.classList.toggle('lit',
          on && (path.dataset.from === key || path.dataset.to === key));
      }
      for (const other of boxes.querySelectorAll('.dia-box')) {
        const id = other.dataset.key;
        other.classList.toggle('lit', on && (
          id === key
          || edges.some((p) => p.classList.contains('lit')
            && (p.dataset.from === id || p.dataset.to === id))));
      }
    };
    group.addEventListener('mouseenter', () => light(true));
    group.addEventListener('mouseleave', () => light(false));
    group.addEventListener('focus', () => light(true));
    group.addEventListener('blur', () => light(false));
    if (row.go) {
      group.addEventListener('click', row.go);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); row.go(); }
      });
    }
    boxes.append(group);
  }

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [
    [hue('ok'), 'guest'], [hue('error'), 'staff'], [hue('warning'), 'partner and outside'],
    [hue('muted'), 'operator, device and the stores'],
  ], 'an actor reaches a surface \u00b7 an outside system speaks through the services '
    + 'named on it \u00b7 '
    + 'hover a surface for the services it calls \u00b7 a line into a store is how many tables '
    + 'the service keeps there, and the store all sixteen use is drawn faint');

  // ---- what the file says for itself ------------------------------------
  if (doc.about) {
    body.append(el('div', 'journey-section-label', 'what this is'));
    body.append(proseLine(doc.about));
  }

  if (doc.scale) {
    body.append(el('div', 'journey-section-label', 'the size of it'));
    const figures = el('div', 'service-figures');
    for (const [label, value] of Object.entries(doc.scale)) {
      const cell = el('div', 'service-figure');
      cell.append(el('b', null, String(value)));
      cell.append(el('span', null, label.replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase()));
      figures.append(cell);
    }
    body.append(figures);
  }

  if (doc.regions) {
    body.append(el('div', 'journey-section-label', `regions \u2014 ${doc.regions.model ?? ''}`));
    if (doc.regions.note) body.append(proseLine(doc.regions.note));
    if (doc.regions.unresolved) {
      body.append(proseLine(`**Unresolved.** ${doc.regions.unresolved}`, 'service-prose warn'));
    }
  }

  // The one paragraph on this page that is about the project rather than the
  // system, and the only one anybody would be tempted to leave out.
  if (doc.honestly) {
    body.append(el('div', 'journey-section-label', 'honestly'));
    body.append(proseLine(doc.honestly, 'service-prose warn'));
  }
}

// \u2500\u2500 the scope hierarchy, drawn \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
//
// A tree with one fork in it, and the fork is the point: `outlet` is a sibling
// of `department` rather than a child, because the same physical restaurant can
// be one department and two outlets \u2014 a kitchen and a bar \u2014 or two departments
// and one outlet. Drawn as a ladder with that one branch, because that is the
// shape, and a list of eight names is not.
//
// Depth is walked from each level's `parent` rather than taken from the file's
// order, so a level inserted between two others lands where it belongs without
// anything here changing.

const HIER = { width: 940, boxW: 210, boxH: 52, rowGap: 34, padY: 18 };

const BRANCH_TOKENS = { root: 'patch', organisational: 'ok', commercial: 'warning' };
const branchColour = (b) => hue(BRANCH_TOKENS[String(b ?? '').toLowerCase()] ?? 'muted');

function renderHierarchy() {
  const body = $('hierarchy-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  const doc = diagrams?.hierarchy;
  if (!doc?.present) {
    body.append(el('p', 'pane-empty',
      'This package has no diagrams/hld/01-hierarchy.yaml.'));
    $('hierarchy-hint').textContent = '';
    return;
  }

  const levels = doc.levels ?? [];
  const byName = new Map(levels.map((l) => [l.level, l]));
  const depthOf = (level) => {
    let depth = 0;
    let at = level;
    const seen = new Set();
    while (at?.parent && !seen.has(at.level)) {
      seen.add(at.level);
      at = byName.get(at.parent);
      depth += 1;
    }
    return depth;
  };

  $('hierarchy-hint').textContent =
    `${levels.length} levels \u00b7 ${doc.spine?.table ?? ''}`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'High-level design \u00b7 where configuration lives'));
  head.append(el('h2', 'journey-title', doc.title ?? 'The scope hierarchy'));
  head.append(sourceLine(doc.file, doc.generatedBy ?? diagrams.generatedBy));
  body.append(head);

  // ---- lay the ladder out ------------------------------------------------
  const byDepth = new Map();
  for (const level of levels) {
    const depth = depthOf(level);
    if (!byDepth.has(depth)) byDepth.set(depth, []);
    byDepth.get(depth).push(level);
  }
  const depths = [...byDepth.keys()].sort((a, b) => a - b);
  const height = HIER.padY * 2 + depths.length * (HIER.boxH + HIER.rowGap) - HIER.rowGap;

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${HIER.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });
  const defs = svgEl('defs');
  const marker = svgEl('marker', {
    id: 'hier-head', viewBox: '0 0 8 8', refX: 7, refY: 4,
    markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse',
  });
  marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: 'dia-arrow-head' }));
  defs.append(marker);
  svg.append(defs);
  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  const boxes = svgEl('g', { class: 'dia-boxes' });
  svg.append(boxes);

  const at = new Map();
  depths.forEach((depth, i) => {
    // The organisational spine keeps the centre line at every depth; a
    // commercial sibling sits beside it. Sorting rather than special-casing
    // `outlet` means a second commercial level would place itself.
    const row = byDepth.get(depth).slice().sort((a, b) =>
      (a.branch === 'root' || String(a.branch).toLowerCase() === 'organisational' ? 0 : 1)
      - (b.branch === 'root' || String(b.branch).toLowerCase() === 'organisational' ? 0 : 1));
    const span = row.length * HIER.boxW + (row.length - 1) * 46;
    const left = row.length === 1
      ? HIER.width / 2 - HIER.boxW / 2
      : HIER.width / 2 - span / 2;
    row.forEach((level, j) => {
      at.set(level.level, {
        level,
        x: left + j * (HIER.boxW + 46),
        y: HIER.padY + i * (HIER.boxH + HIER.rowGap),
        w: HIER.boxW, h: HIER.boxH,
      });
    });
  });

  for (const [name, box] of at) {
    const parent = at.get(box.level.parent);
    if (!parent) continue;
    lanes.append(svgEl('path', {
      d: `M ${parent.x + parent.w / 2} ${parent.y + parent.h} `
        + `C ${parent.x + parent.w / 2} ${parent.y + parent.h + 18}, `
        + `${box.x + box.w / 2} ${box.y - 18}, `
        + `${box.x + box.w / 2} ${box.y}`,
      class: `dia-arrow${String(box.level.branch).toLowerCase() === 'commercial' ? ' strong' : ''}`,
      'marker-end': 'url(#hier-head)',
      'data-to': name,
    }));
  }

  for (const [, box] of at) {
    const { level } = box;
    const colour = branchColour(level.branch);
    const group = svgEl('g', { class: 'dia-box' });
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: box.w, height: box.h, rx: 6,
      class: 'dia-box-bg', style: `--tier:${colour}`,
    }));
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: 3, height: box.h, fill: colour, rx: 1.5,
    }));
    const name = svgEl('text', {
      x: box.x + 11, y: box.y + 20, class: 'dia-box-name', 'font-size': 12.5,
    });
    name.textContent = level.level;
    group.append(name);
    const sub = svgEl('text', {
      x: box.x + 11, y: box.y + 35, class: 'dia-box-counts', 'font-size': 10.5,
    });
    sub.textContent =
      `${level.operations ?? 0} operations \u00b7 ${level.configurations ?? 0} configurations`;
    group.append(sub);
    const branch = svgEl('text', {
      x: box.x + box.w - 11, y: box.y + 20, class: 'dia-box-counts',
      'font-size': 9.5, 'text-anchor': 'end',
    });
    branch.textContent = String(level.branch ?? '').toLowerCase();
    group.append(branch);
    const title = svgEl('title');
    title.textContent = level.why ? level.why.replace(/\*\*/g, '') : level.level;
    group.append(title);
    boxes.append(group);
  }

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);
  wireIsolate(svg);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [
    [hue('patch'), 'the root \u2014 what is bought'],
    [hue('ok'), 'organisational \u2014 who works where'],
    [hue('warning'), 'commercial \u2014 what is sold where'],
  ], 'configuration resolves by walking upward until something answers \u00b7 '
    + 'an absent level is skipped, not empty');

  if (doc.about) {
    body.append(el('div', 'journey-section-label', 'what this is'));
    body.append(proseLine(doc.about));
  }

  if (doc.spine) {
    // `platform.scope_node` is a table in the DB layer, and 304 of 379 tables
    // anchor on it \u2014 which makes it the single most worth-opening name on the
    // page.
    const label = el('div', 'journey-section-label', `the spine \u2014 ${doc.spine.table ?? ''}`);
    const schema = String(doc.spine.table ?? '').split('.')[0];
    if (schema && (state.backend?.modules ?? []).some((m) => m.name === schema)) {
      label.classList.add('linked');
      label.tabIndex = 0;
      label.onclick = () => openSchemaModule(schema);
      label.onkeydown = (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openSchemaModule(schema); }
      };
    }
    body.append(label);
    if (doc.spine.note) body.append(proseLine(doc.spine.note));
    const chips = el('div', 'service-tables');
    for (const column of doc.spine.columns ?? []) {
      chips.append(el('span', 'service-table', column));
    }
    body.append(chips);
  }

  // What each level owns, which is the half of the file the boxes cannot hold.
  body.append(el('div', 'journey-section-label', 'what lives at each level'));
  const list = el('div', 'detail-stack');
  for (const level of levels) {
    const card = el('div', 'detail-card');
    card.append(el('div', 'detail-card-name', level.level));
    if (level.why) card.append(proseLine(level.why));
    if ((level.owns ?? []).length) {
      const chips = el('div', 'service-tables');
      for (const owns of level.owns) chips.append(el('span', 'service-table', owns));
      card.append(chips);
    }
    list.append(card);
  }
  body.append(list);

  if ((doc.rules ?? []).length) {
    body.append(el('div', 'journey-section-label', `${doc.rules.length} rules`));
    const rules = el('div', 'detail-stack');
    for (const rule of doc.rules) {
      const card = el('div', 'detail-card');
      card.append(el('div', 'detail-card-name', rule.rule));
      if (rule.why) card.append(proseLine(rule.why));
      rules.append(card);
    }
    body.append(rules);
  }

  if ((doc.decisions ?? []).length) {
    body.append(el('div', 'journey-section-label', 'decided in'));
    const chips = el('div', 'service-tables');
    for (const file of doc.decisions) chips.append(el('span', 'service-table', file));
    body.append(chips);
  }
}

// ── the high-level design, drawn ─────────────────────────────────────
//
// Five tier bands, sixteen services, and an arrow wherever one writes another's
// data. The layout is computed here rather than measured back out of the
// browser: an arrow that has to land on a particular box edge needs to know
// where that edge is before it is drawn, not after.
//
// SVG rather than canvas because nothing moves. It is a diagram — it should
// stay sharp when the page is zoomed to read a label, and be styled by the same
// sheet as everything around it.

const SVG_NS = 'http://www.w3.org/2000/svg';
const svgEl = (tag, attrs = {}) => {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value != null) node.setAttribute(key, String(value));
  }
  return node;
};

/** A box of text that wraps to the width it is given. */
function svgText(parent, text, { x, y, width, size = 11, fill, weight, anchor = 'start', lines = 2 }) {
  const words = String(text).split(/\s+/);
  const perLine = Math.max(6, Math.floor(width / (size * 0.54)));
  const rows = [];
  let row = '';
  for (const word of words) {
    const next = row ? `${row} ${word}` : word;
    if (next.length > perLine && row) { rows.push(row); row = word; } else { row = next; }
    if (rows.length >= lines) break;
  }
  if (row && rows.length < lines) rows.push(row);
  rows.forEach((line, i) => {
    parent.append(svgEl('text', {
      x, y: y + i * (size + 2), 'font-size': size, fill,
      'font-weight': weight, 'text-anchor': anchor, class: 'dia-text',
    })).lastChild.textContent = line;
  });
  return y + rows.length * (size + 2);
}

const DIA = {
  width: 1160,
  boxW: 168,
  boxH: 66,
  gapX: 14,
  gapY: 12,
  bandPadX: 92,
  bandPadY: 30,
  bandGap: 26,
  perRow: 5,
};

function renderHld() {
  const body = $('hld-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  if (!diagrams?.present) {
    body.append(el('p', 'pane-empty', 'No diagrams/ in this package.'));
    $('hld-hint').textContent = '';
    return;
  }

  $('hld-hint').textContent =
    `${diagrams.stats.services} services · ${diagrams.stats.tiers} tiers · `
    + `${diagrams.stats.crossWrites} cross-service writes`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind',
    'High-level design \u00b7 all sixteen services'));
  head.append(el('h2', 'journey-title', diagrams.title));
  head.append(sourceLine(hldFile(), diagrams.generatedBy));
  body.append(head);

  // ---- lay the bands out ------------------------------------------------
  const at = new Map();
  const bands = [];
  let y = 0;
  for (const tier of diagrams.tiers) {
    const services = tier.services.map(serviceByKey).filter(Boolean);
    const rows = Math.max(1, Math.ceil(services.length / DIA.perRow));
    const height = DIA.bandPadY + rows * (DIA.boxH + DIA.gapY) + 6;
    const band = { tier, services, y, height };
    services.forEach((service, i) => {
      const row = Math.floor(i / DIA.perRow);
      const inRow = services.slice(row * DIA.perRow, (row + 1) * DIA.perRow).length;
      const rowW = inRow * DIA.boxW + (inRow - 1) * DIA.gapX;
      const left = DIA.bandPadX + ((DIA.width - DIA.bandPadX - 20) - rowW) / 2;
      at.set(service.key, {
        x: left + (i % DIA.perRow) * (DIA.boxW + DIA.gapX),
        y: y + DIA.bandPadY + row * (DIA.boxH + DIA.gapY),
        w: DIA.boxW, h: DIA.boxH, service,
      });
    });
    bands.push(band);
    y += height + DIA.bandGap;
  }
  // The gap goes between bands, not after the last one — carrying it into the
  // height left an empty strip under the bottom tier.
  const height = Math.max(0, y - DIA.bandGap) + 10;

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${DIA.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });

  // an arrowhead, once
  const defs = svgEl('defs');
  for (const [id, cls] of [['dia-head', 'dia-arrow-head'], ['dia-head-strong', 'dia-arrow-head strong']]) {
    const marker = svgEl('marker', {
      id, viewBox: '0 0 8 8', refX: 7, refY: 4,
      markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse',
    });
    marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: cls }));
    defs.append(marker);
  }
  svg.append(defs);

  // ---- the bands --------------------------------------------------------
  for (const band of bands) {
    svg.append(svgEl('rect', {
      x: 8, y: band.y, width: DIA.width - 16, height: band.height,
      rx: 10, class: 'dia-band',
    }));
    const label = svgEl('text', {
      x: 22, y: band.y + 22, class: 'dia-band-label', 'font-size': 11,
    });
    label.textContent = band.tier.tier.toUpperCase();
    svg.append(label);
    svg.append(svgEl('rect', {
      x: 22, y: band.y + 30, width: 3, height: band.height - 42,
      rx: 1.5, fill: tierColour(band.tier.tier), opacity: 0.55,
    }));
  }

  // ---- the arrows, behind the boxes -------------------------------------
  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  for (const edge of diagrams.crossServiceWrites) {
    const from = at.get(edge.from);
    const to = at.get(edge.to);
    if (!from || !to) continue;

    // Leave and arrive on the nearer horizontal edge when the two are on
    // different rows, which is nearly always: an arrow into the top of a box
    // reads as "into this", an arrow into its side reads as "past it".
    const down = to.y > from.y;
    const a = { x: from.x + from.w / 2, y: down ? from.y + from.h : from.y };
    const b = { x: to.x + to.w / 2, y: down ? to.y : to.y + to.h };
    const lift = Math.max(26, Math.abs(b.y - a.y) * 0.42);
    const path = svgEl('path', {
      d: `M ${a.x} ${a.y} C ${a.x} ${a.y + (down ? lift : -lift)}, `
        + `${b.x} ${b.y - (down ? lift : -lift)}, ${b.x} ${b.y}`,
      class: `dia-arrow${edge.kind === 'strong' ? ' strong' : ''}`,
      'marker-end': edge.kind === 'strong' ? 'url(#dia-head-strong)' : 'url(#dia-head)',
      'data-from': edge.from, 'data-to': edge.to,
    });
    const title = svgEl('title');
    title.textContent =
      `${edge.fromName} writes ${edge.toName} — ${edge.writes ?? '?'} operations`
      + (edge.reads != null ? `, reads ${edge.reads}` : '')
      + (edge.why ? `\n${edge.why.replace(/\*\*/g, '')}` : '');
    path.append(title);
    lanes.append(path);
  }

  // ---- the services -----------------------------------------------------
  const boxes = svgEl('g', { class: 'dia-boxes' });
  svg.append(boxes);
  for (const [key, box] of at) {
    const service = box.service;
    const group = svgEl('g', { class: 'dia-box', 'data-key': key, tabindex: 0 });
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: box.w, height: box.h, rx: 7,
      class: 'dia-box-bg', style: `--tier:${tierColour(service.tier)}`,
    }));
    group.append(svgEl('rect', {
      x: box.x, y: box.y, width: 3, height: box.h,
      fill: tierColour(service.tier), rx: 1.5,
    }));

    const name = svgEl('text', {
      x: box.x + 12, y: box.y + 21, class: 'dia-box-name', 'font-size': 12.5,
    });
    name.textContent = service.name.replace(/Service$/, '');
    group.append(name);

    const counts = svgEl('text', {
      x: box.x + 12, y: box.y + 39, class: 'dia-box-counts', 'font-size': 10.5,
    });
    counts.textContent =
      `${service.operations ?? 0} ops · `
      + `${service.workbookTables?.length ?? service.tables ?? 0} tables`;
    group.append(counts);

    // What it reaches, under what it is made of. Sixteen coverage bars made
    // the documentation's gaps the loudest thing in the design; these say what
    // each service actually touches instead. Coverage is still a figure under
    // the LLD head, where it is a fact about the package rather than the
    // headline of a diagram about the platform.
    const touches = svgEl('text', {
      x: box.x + 12, y: box.y + 56, class: 'dia-box-counts', 'font-size': 10.5,
    });
    touches.textContent = serviceTouches(service);
    group.append(touches);

    const title = svgEl('title');
    title.textContent =
      `${service.name} · ${service.tier}\n`
      + `${service.operations ?? 0} operations, `
      + `${service.workbookTables?.length ?? 0} tables\n`
      + serviceTouches(service)
      + (service.flowCoverage != null ? ` · ${service.flowCoverage}% walked by a flow` : '')
      + (service.scale ? `\n${service.scale.replace(/\*\*/g, '')}` : '');
    group.append(title);

    // Hovering a service dims every boundary that is not its own. Sixteen
    // boxes and thirty-four arrows cannot answer "whose" without it.
    const light = (on) => {
      svg.classList.toggle('lit', on);
      for (const path of lanes.querySelectorAll('.dia-arrow')) {
        path.classList.toggle('lit',
          on && (path.dataset.from === key || path.dataset.to === key));
      }
      for (const other of boxes.querySelectorAll('.dia-box')) {
        other.classList.toggle('lit', on && (
          other.dataset.key === key
          || diagrams.crossServiceWrites.some((edge) =>
            (edge.from === key && edge.to === other.dataset.key)
            || (edge.to === key && edge.from === other.dataset.key))
        ));
      }
    };
    group.addEventListener('mouseenter', () => light(true));
    group.addEventListener('mouseleave', () => light(false));
    group.addEventListener('focus', () => light(true));
    group.addEventListener('blur', () => light(false));
    group.addEventListener('click', () => { selectService(key); setMode('service'); });
    boxes.append(group);
  }

  const frame = el('div', 'dia-frame');
  frame.append(svg);
  body.append(frame);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend, [
    [hue('error'), 'a strong coupling — the two are near enough to argue about'],
    [hue('muted'), 'an ordinary write, permitted by the append rule'],
  ], 'an arrow is one service writing another\u2019s tables · the third line is what each '
    + 'service reaches · hover a service to see only its own boundaries · click one to '
    + 'open its LLD');

  // ---- the document's own words, under its picture ----------------------
  if (diagrams.about) {
    body.append(el('div', 'journey-section-label', 'what this says'));
    body.append(proseLine(diagrams.about));
  }

  body.append(el('div', 'journey-section-label', `${diagrams.tiers.length} tiers`));
  const tiers = el('div', 'service-edges');
  for (const tier of diagrams.tiers) {
    const row = el('div', 'hld-tier');
    const title = el('div', 'hld-tier-head');
    const dot = el('span', 'tree-group-dot');
    dot.style.background = tierColour(tier.tier);
    title.append(dot, el('span', 'service-band-name', tier.tier));
    title.append(el('span', 'service-schema-count', `${tier.services.length} services`));
    row.append(title);
    if (tier.meaning) row.append(proseLine(tier.meaning));
    tiers.append(row);
  }
  body.append(tiers);

  body.append(el('div', 'journey-section-label',
    `${diagrams.crossServiceWrites.length} cross-service writes`));
  const list = el('div', 'service-edges');
  for (const edge of [...diagrams.crossServiceWrites]
    .sort((a, b) => (b.writes ?? 0) - (a.writes ?? 0))) {
    const line = el('div', `service-edge ${edge.kind === 'strong' ? 'strong' : ''}`);
    const pair = el('div', 'service-edge-pair');
    const from = el('button', 'service-edge-name', edge.fromName.replace(/Service$/, ''));
    from.onclick = () => { selectService(edge.from); setMode('service'); };
    const to = el('button', 'service-edge-name', edge.toName.replace(/Service$/, ''));
    to.onclick = () => { selectService(edge.to); setMode('service'); };
    pair.append(from, el('span', 'service-edge-arrow', '\u2192'), to);
    line.append(pair);
    const counts = el('div', 'service-edge-counts');
    counts.append(el('b', null, `${edge.writes ?? 0}`), el('span', null, 'writes'));
    if (edge.reads != null) counts.append(el('b', null, `${edge.reads}`), el('span', null, 'reads'));
    line.append(counts);
    if (edge.why) line.append(proseLine(edge.why, 'service-edge-why'));
    list.append(line);
  }
  body.append(list);

  if (diagrams.decision) {
    body.append(el('div', 'journey-section-label', 'the decision behind it'));
    body.append(el('div', 'adr-file', diagrams.decision));
  }
  if (diagrams.notes) {
    body.append(el('div', 'journey-section-label', 'notes'));
    body.append(proseLine(diagrams.notes));
  }
}

// ── the services, as a field ─────────────────────────────────────────
//
// The Map bands the sixteen by tier, which is the HLD's argument and therefore
// fixes where each one sits. What it cannot show is weight — which services are
// large, which are peripheral, how much of the platform is in four of them —
// and that is the first thing anybody wants of an architecture, before any of
// the reasoning. So this opens the layer.

let servicesGalaxySummary = '';

function describeServiceHub(hub) {
  const shape = hub.tier === 'core' ? 'more services write into it than it writes into'
    : hub.tier === 'satellite' ? 'writes others, nothing writes it'
    : 'writes and is written';
  const parts = [`${hub.name} · ${shape}`];
  parts.push(`${hub.operations} operations`);
  parts.push(`${hub.tables} tables${hub.written ? `, ${hub.written} with SQL` : ''}`);
  if (hub.deploys) parts.push(`${hub.deploys} tier`);
  if (hub.coverage != null) parts.push(`${hub.coverage}% walked`);
  return parts.join(' · ');
}

function buildServicesGalaxy() {
  const diagrams = state.diagrams;
  const services = diagrams?.services ?? [];
  const ddl = new Set((state.backend?.tables ?? []).filter((t) => t.ddl).map((t) => t.name));

  // Who writes whom, so a service can be placed by what it is to the others
  // rather than by which tier it was put in.
  //
  // Not the schema field's rule. There, an anchor is written into and writes
  // nothing back; no service is — the nearest, Ledger and Ai, are each written
  // into once — so borrowing it left the field with no centre. What separates a
  // service is the balance: more write into it than it writes into. Identity,
  // Tenancy, Catalogue, Inventory and Marketing are those. Order, written into
  // four times and writing into six, is not, and should not be: it is the
  // middle of the sale path rather than something to deploy behind.
  const inbound = new Map();
  const outbound = new Map();
  for (const edge of diagrams?.crossServiceWrites ?? []) {
    if (!outbound.has(edge.from)) outbound.set(edge.from, new Set());
    outbound.get(edge.from).add(edge.to);
    if (!inbound.has(edge.to)) inbound.set(edge.to, new Set());
    inbound.get(edge.to).add(edge.from);
  }

  const hubs = services.map((service) => {
    const owned = service.workbookTables ?? [];
    const written = owned.filter((name) => ddl.has(name)).length;
    const inn = inbound.get(service.key)?.size ?? 0;
    const outn = outbound.get(service.key)?.size ?? 0;
    return {
      id: `service:${service.key}`,
      key: service.key,
      name: service.name.replace(/Service$/, ''),
      // Size is operations: it is what the service *does*, and it is the number
      // that differs most between them — 132 against 16.
      weight: Math.max(1, service.operations ?? 1),
      operations: service.operations ?? 0,
      tables: owned.length || service.tables || 0,
      written,
      deploys: service.tier,
      coverage: service.flowCoverage,
      // The cloud is the tables. Bright ones are the tables whose SQL exists,
      // the same distinction the schema field draws, so "how much of this is
      // actually built" reads at a glance in both places.
      mass: owned.length || service.tables || 0,
      hot: written,
      // Three, not two: two services writing into something is a pair, not a
      // dependency anybody plans a deploy around.
      tier: inn >= 3 && outn < inn ? 'core' : inn === 0 ? 'satellite' : 'spine',
    };
  });

  const known = new Set(hubs.map((hub) => hub.id));
  const links = (diagrams?.crossServiceWrites ?? [])
    .filter((edge) => known.has(`service:${edge.from}`) && known.has(`service:${edge.to}`))
    .map((edge) => ({
      source: `service:${edge.from}`,
      target: `service:${edge.to}`,
      // Amber is the lane to look at twice, which here is the strong coupling —
      // the four where the two services are near enough to argue about.
      critical: edge.kind === 'strong',
      count: edge.writes ?? 1,
    }));

  return { hubs, links };
}

function renderServicesGalaxy() {
  const diagrams = state.diagrams;
  if (!diagrams?.present) {
    servicesGalaxy.setData({ hubs: [], links: [] });
    $('services-graph-hint').textContent = 'No diagrams/ in this package.';
    return;
  }

  const built = buildServicesGalaxy();
  servicesGalaxy.setData(built);
  servicesGalaxy.setMode(state.galaxyMode);
  servicesGalaxy.setSelected(state.serviceKey ? `service:${state.serviceKey}` : null);
  servicesGalaxy.start();

  const anchors = built.hubs.filter((hub) => hub.tier === 'core').length;
  const strong = built.links.filter((link) => link.critical).length;
  servicesGalaxySummary =
    `${built.hubs.length} services · ${built.hubs.reduce((a, h) => a + h.operations, 0)} operations, `
    + `${built.hubs.reduce((a, h) => a + h.tables, 0)} tables · ${built.links.length} cross-service writes`
    + (strong ? ` · ${strong} strong` : '')
    + ` · ${anchors} written into more than they write`;
  if (servicesGalaxy.moteSampled) servicesGalaxySummary += ' · the field is a sample';
  $('services-graph-hint').textContent = servicesGalaxySummary;

  galaxyLegend($('services-graph-legend'), [
    ['core', 'more services write into it than it writes into — deploy behind these'],
    ['spine', 'writes others and is written'],
    ['satellite', 'writes others, nothing writes it'],
  ], 'dot size is how many operations · a bright mote is a table whose SQL exists · '
    + 'amber lane = a strong coupling · double-click a service to open it');
}

// ── the services, as an ER diagram ───────────────────────────────────
//
// The map fixes every service in its tier so the shape can be read. This is the
// same sixteen with that constraint removed: boxes you can drag, pin and open
// out, joined by what they actually depend on.
//
// Entities are services and rows are the schemas they own, rather than tables
// and columns — the DB layer already draws all 379 tables with their foreign
// keys, and redrawing them coloured by service would be that diagram with a
// legend. What only this layer can say is which service depends on which, and
// on whose data.

function buildServiceEr() {
  const diagrams = state.diagrams;
  const scope = state.serviceErScope ?? 'all';
  const withReads = state.serviceErReads === true;

  const inScope = (service) => scope === 'all' || service.tier === scope;
  const services = (diagrams?.services ?? []).filter(inScope);
  const shown = new Set(services.map((service) => service.key));

  const nodes = services.map((service) => {
    // Owned schemas, with the table count the workbook actually assigns. A
    // schema is the unit a service owns outright — the rule the whole
    // decomposition rests on is that no schema is written by two services — so
    // it is the right row, and the count is what makes the row worth reading.
    const detail = new Map((service.schemaDetail ?? []).map((row) => [row.schema, row]));
    const rows = (service.schemas ?? []).map((name) => ({
      label: name,
      value: detail.get(name)?.tables != null ? `${detail.get(name).tables}` : '',
      strong: true,
      refTarget: name,
    }));
    // A service that owns no schema is a real and interesting case rather than
    // an error — it is one that exists to orchestrate — so it draws as a box
    // with a line saying so instead of an empty one.
    if (!rows.length) rows.push({ label: 'owns no schema', value: '' });

    return {
      id: `service:${service.key}`,
      title: service.name.replace(/Service$/, ''),
      badge: `${service.workbookTables?.length ?? service.tables ?? 0}`,
      color: tierColour(service.tier),
      rows,
    };
  });

  const edges = [];
  const seen = new Set();
  const add = (from, to, label) => {
    if (!shown.has(from) || !shown.has(to) || from === to) return;
    const key = `${from}|${to}|${label}`;
    if (seen.has(key)) return;
    seen.add(key);
    edges.push({ source: `service:${from}`, target: `service:${to}`, label });
  };

  // A write is a boundary somebody had to justify; a read is a dependency that
  // cannot corrupt anything. Both are real, and they are not the same fact, so
  // the label says which and the reads can be turned off.
  for (const edge of diagrams?.crossServiceWrites ?? []) {
    add(edge.from, edge.to, `${edge.writes ?? 0} writes`);
  }
  if (withReads) {
    for (const service of services) {
      for (const row of service.readsFrom ?? []) {
        const to = (diagrams.services.find((other) => other.name === row.service))?.key;
        if (to) add(service.key, to, `${row.operations ?? 0} reads`);
      }
    }
  }

  return { nodes, edges };
}

function renderServiceEr() {
  const diagrams = state.diagrams;
  if (!diagrams?.present) {
    $('er-services-hint').textContent = 'No diagrams/ in this package.';
    serviceEr.setData([], []);
    return;
  }

  // The tiers, as a scope. Sixteen boxes and fifty edges is legible and one
  // tier is legible; the point of the picker is that they are different
  // questions, not that sixteen is too many.
  const scopes = $('er-services-scope');
  scopes.innerHTML = '';
  for (const [key, label] of [['all', 'All tiers'], ...diagrams.tiers.map((t) => [t.tier, t.tier])]) {
    const button = el('button', null, label);
    button.classList.toggle('active', key === (state.serviceErScope ?? 'all'));
    button.onclick = () => {
      state.serviceErScope = key;
      serviceEr.userAdjusted = false;
      renderServiceEr();
      serviceEr.fit();
    };
    scopes.append(button);
  }

  const { nodes, edges } = buildServiceEr();
  serviceEr.setData(nodes, edges);
  serviceEr.setSelected?.(state.serviceKey ? `service:${state.serviceKey}` : null);

  // Framed here rather than on a settle. This renderer places its boxes in a
  // hierarchy and only runs physics to settle a drag, so the arrangement is
  // already final and `onSettle` is never called — waiting for it left the
  // diagram at 1:1 with its top three services above the pane.
  if (!serviceEr.userAdjusted) serviceEr.fit();

  const writes = edges.filter((edge) => /writes$/.test(edge.label)).length;
  $('er-services-hint').textContent =
    `${nodes.length} services · ${writes} write${writes === 1 ? '' : 's'} · ` +
    `${edges.length - writes} read dependencies`;

  renderBoxLegend($('er-services-legend'),
    diagrams.tiers.map((tier) => [tierColour(tier.tier), tier.tier]),
    'a row is a schema this service owns · an edge is data it depends on · drag a box to pin it');
}

// ── one service, drawn ───────────────────────────────────────────────
//
// The service in the middle; its contracts above, because that is the surface
// anything outside it touches; its schemas below, because that is what it is;
// what it reads on the left and what it writes on the right, because a
// dependency you can only read is a different thing from one you can write and
// the two should not look alike.
//
// The arrangement carries the rule: no service spans a schema it does not own,
// and no schema is written by two. The schemas hang off this service and off
// nothing else, so a schema appearing under two services would be visible as
// the contradiction it is.

const LLD = {
  width: 1080,
  boxW: 150,
  boxH: 44,
  gap: 12,
  coreW: 240,
  coreH: 92,
  rowGap: 62,
  sideW: 156,
};

function drawService(service, diagrams) {
  const contracts = service.contracts ?? [];
  const schemaRows = (service.schemas ?? []).map((name) => ({
    name,
    tables: (service.schemaDetail ?? []).find((row) => row.schema === name)?.tables ?? null,
  }));
  const reads = (service.readsFrom ?? []).slice(0, 5);
  const writes = (service.writesOutside ?? []).slice(0, 5);

  const rowW = (n) => n * LLD.boxW + Math.max(0, n - 1) * LLD.gap;
  const mid = LLD.width / 2;

  // Enough height for the tallest side column, so nothing is clipped when a
  // service reads five others and owns one schema.
  const sideRows = Math.max(reads.length, writes.length);
  const topY = 16;
  const coreY = topY + (contracts.length ? LLD.boxH + LLD.rowGap : 24);
  const belowY = coreY + LLD.coreH + LLD.rowGap;
  // The side columns are centred on the service box, so their lowest point is
  // half a column below its middle — not a column below its top, which is what
  // taking the taller of two guesses assumed.
  const sideSpan = sideRows ? sideRows * (LLD.boxH + LLD.gap) - LLD.gap : 0;
  const sideBottom = coreY + LLD.coreH / 2 + sideSpan / 2;
  const height = Math.max(
    belowY + (schemaRows.length ? LLD.boxH : 0),
    sideBottom,
    coreY + LLD.coreH
  ) + 22;

  const svg = svgEl('svg', {
    class: 'dia', viewBox: `0 0 ${LLD.width} ${height}`,
    width: '100%', height, preserveAspectRatio: 'xMidYMin meet',
  });

  const defs = svgEl('defs');
  const marker = svgEl('marker', {
    id: 'lld-head', viewBox: '0 0 8 8', refX: 7, refY: 4,
    markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse',
  });
  marker.append(svgEl('path', { d: 'M 0 1 L 8 4 L 0 7 z', class: 'dia-arrow-head' }));
  defs.append(marker);
  svg.append(defs);

  const lanes = svgEl('g', { class: 'dia-lanes' });
  svg.append(lanes);
  const boxes = svgEl('g', { class: 'dia-boxes' });
  svg.append(boxes);

  const tint = tierColour(service.tier);

  const label = (text, x, y, cls, size = 10) => {
    const node = svgEl('text', { x, y, class: cls, 'font-size': size });
    node.textContent = text;
    svg.append(node);
    return node;
  };

  const box = (x, y, w, h, { title, sub, cls = '', colour, onClick, tip }) => {
    const group = svgEl('g', { class: `dia-box ${cls}`.trim() });
    group.append(svgEl('rect', {
      x, y, width: w, height: h, rx: 6,
      class: 'dia-box-bg', style: colour ? `--tier:${colour}` : null,
    }));
    if (colour) {
      group.append(svgEl('rect', { x, y, width: 3, height: h, rx: 1.5, fill: colour }));
    }
    const name = svgEl('text', {
      x: x + 11, y: y + (sub ? 20 : h / 2 + 4), class: 'dia-box-name', 'font-size': 12,
    });
    name.textContent = title;
    group.append(name);
    if (sub) {
      const under = svgEl('text', {
        x: x + 11, y: y + 35, class: 'dia-box-counts', 'font-size': 10.5,
      });
      under.textContent = sub;
      group.append(under);
    }
    if (tip) {
      const t = svgEl('title');
      t.textContent = tip;
      group.append(t);
    }
    if (onClick) {
      group.setAttribute('tabindex', '0');
      group.addEventListener('click', onClick);
      group.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); onClick(); }
      });
    }
    boxes.append(group);
    return { x, y, w, h };
  };

  const link = (a, b, text) => {
    const path = svgEl('path', {
      d: `M ${a.x} ${a.y} C ${a.x + (b.x - a.x) * 0.4} ${a.y}, `
        + `${a.x + (b.x - a.x) * 0.6} ${b.y}, ${b.x} ${b.y}`,
      class: 'dia-arrow', 'marker-end': 'url(#lld-head)',
    });
    lanes.append(path);
    if (text) {
      const node = svgEl('text', {
        x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 - 5,
        class: 'dia-lane-label', 'font-size': 9.5, 'text-anchor': 'middle',
      });
      node.textContent = text;
      svg.append(node);
    }
  };

  // ---- the service ------------------------------------------------------
  const coreX = mid - LLD.coreW / 2;
  // The counts go through the helper as the line they are. Passing no `sub`
  // centres the name vertically, which is where these were being drawn — the
  // two landed on top of each other.
  const core = box(coreX, coreY, LLD.coreW, LLD.coreH, {
    title: service.name.replace(/Service$/, ''),
    sub: `${service.operations ?? 0} operations · `
      + `${service.workbookTables?.length ?? service.tables ?? 0} tables`,
    colour: tint,
    tip: service.scale ? service.scale.replace(/\*\*/g, '') : null,
  });
  const tierText = svgEl('text', {
    x: coreX + 11, y: coreY + 54, class: 'dia-box-counts', 'font-size': 10.5,
  });
  tierText.textContent = `${service.tier} tier`;
  boxes.append(tierText);
  // Same three counts as the HLD box, so a service reads the same in the
  // diagram of the platform and the diagram of itself.
  const touches = svgEl('text', {
    x: coreX + 11, y: coreY + 74, class: 'dia-box-counts', 'font-size': 10.5,
  });
  touches.textContent = serviceTouches(service);
  boxes.append(touches);

  // ---- the contracts it serves -----------------------------------------
  if (contracts.length) {
    label('THE API IT SERVES', mid - rowW(contracts.length) / 2, topY - 4, 'dia-band-label');
    const left = mid - rowW(contracts.length) / 2;
    contracts.forEach((stem, i) => {
      const x = left + i * (LLD.boxW + LLD.gap);
      const at = box(x, topY, LLD.boxW, LLD.boxH, {
        title: stem,
        cls: 'contract',
        onClick: () => openContract(stem),
        tip: `contracts/…/${stem}.yaml — click to open it`,
      });
      link({ x: at.x + at.w / 2, y: at.y + at.h },
        { x: coreX + LLD.coreW / 2, y: coreY });
    });
  }

  // ---- the schemas it owns ---------------------------------------------
  if (schemaRows.length) {
    const left = mid - rowW(schemaRows.length) / 2;
    label('THE DATA IT OWNS', left, belowY - 10, 'dia-band-label');
    schemaRows.forEach((row, i) => {
      const x = left + i * (LLD.boxW + LLD.gap);
      const at = box(x, belowY, LLD.boxW, LLD.boxH, {
        title: row.name,
        sub: row.tables != null ? `${row.tables} tables` : null,
        cls: 'schema',
        colour: tint,
        onClick: () => openSchemaModule(row.name),
        tip: `${row.name} — click to open it in the DB layer`,
      });
      link({ x: coreX + LLD.coreW / 2, y: coreY + LLD.coreH },
        { x: at.x + at.w / 2, y: at.y });
    });
  }

  // ---- what it reads, and what it writes -------------------------------
  const side = (rows, isRead) => {
    if (!rows.length) return;
    const x = isRead ? 12 : LLD.width - LLD.sideW - 12;
    const top = coreY + LLD.coreH / 2 - (rows.length * (LLD.boxH + LLD.gap)) / 2;
    label(isRead ? 'READS' : 'WRITES', x, top - 8, 'dia-band-label');
    rows.forEach((row, i) => {
      const y = top + i * (LLD.boxH + LLD.gap);
      const other = diagrams.services.find((s2) => s2.name === row.service);
      const at = box(x, y, LLD.sideW, LLD.boxH, {
        title: String(row.service).replace(/Service$/, ''),
        sub: `${row.operations ?? 0} operations`,
        cls: isRead ? 'reads' : 'writes',
        colour: other ? tierColour(other.tier) : null,
        onClick: other ? () => { selectService(other.key); renderService(); } : null,
        tip: row.why ? row.why.replace(/\*\*/g, '') : null,
      });
      if (isRead) {
        link({ x: at.x + at.w, y: at.y + at.h / 2 },
          { x: coreX, y: coreY + LLD.coreH / 2 });
      } else {
        link({ x: coreX + LLD.coreW, y: coreY + LLD.coreH / 2 },
          { x: at.x, y: at.y + at.h / 2 });
      }
    });
  };
  side(reads, true);
  side(writes, false);

  const frame = el('div', 'dia-frame');
  frame.append(svg);

  // Only the first five each side are drawn; a service reading nine others
  // would draw nine boxes nobody can tell apart. Saying how many were left out
  // is the difference between a summary and a wrong picture.
  const hidden = (service.readsFrom?.length ?? 0) - reads.length
    + (service.writesOutside?.length ?? 0) - writes.length;
  if (hidden > 0) {
    frame.append(el('div', 'dia-note',
      `${hidden} further read or write ${hidden === 1 ? 'dependency is' : 'dependencies are'} `
      + 'listed below rather than drawn.'));
  }
  return frame;
}

// ── one service ──────────────────────────────────────────────────────
function renderService() {
  const body = $('service-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  if (!diagrams?.present) {
    body.append(el('p', 'pane-empty', 'No diagrams/ in this package.'));
    $('service-hint').textContent = '';
    return;
  }

  const service = serviceByKey(state.serviceKey) ?? diagrams.services[0] ?? null;
  if (!service) {
    body.append(el('p', 'pane-empty', 'No services in this package.'));
    return;
  }
  state.serviceKey = service.key;

  $('service-hint').textContent =
    `${service.tier} tier · ${service.operations ?? 0} operations · ` +
    `${service.workbookTables?.length ?? service.tables ?? 0} tables`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'Low-level design \u00b7 one service'));
  head.append(el('h2', 'journey-title', service.name));
  const chips = el('div', 'journey-chips');
  const chip = (label, value) => {
    const box = el('span', 'jchip');
    box.append(el('span', null, label), el('b', null, String(value)));
    return box;
  };
  chips.append(chip('tier', service.tier));
  for (const contract of service.contracts ?? []) {
    const box = el('button', 'jchip link');
    box.append(el('span', null, 'contract'), el('b', null, contract));
    box.onclick = () => openContract(contract);
    chips.append(box);
  }
  head.append(chips);
  if (service.why) head.append(proseLine(service.why, 'journey-trigger'));
  if (service.detailFile) head.append(sourceLine(service.detailFile, diagrams.generatedBy));
  body.append(head);

  const drawn = drawService(service, diagrams);
  body.append(drawn);
  wireIsolate(drawn.querySelector('svg.dia'));

  body.append(serviceFigures(service));

  // scale, and what breaks
  const facts = el('div', 'service-facts');
  const fact = (label, text) => {
    if (!text) return;
    const box = el('div', 'service-fact');
    box.append(el('div', 'service-fact-label', label));
    box.append(proseLine(text));
    facts.append(box);
  };
  fact('scale', service.scale);
  fact('if it is down', service.ifDown);
  fact('why this tier', service.tierMeaning);
  if (service.coverage?.note) fact('flow coverage', service.coverage.note);
  if (facts.children.length) body.append(facts);

  // what it owns
  if (service.schemaDetail?.length || service.schemas?.length) {
    body.append(el('div', 'journey-section-label', 'the schemas it owns'));
    const owned = el('div', 'service-schemas');
    const detail = new Map((service.schemaDetail ?? []).map((row) => [row.schema, row]));
    for (const name of service.schemas ?? []) {
      const row = el('div', 'service-schema');
      const title = el('div', 'service-schema-head');
      const button = el('button', 'service-schema-name', name);
      button.onclick = () => openSchemaModule(name);
      title.append(button);
      const count = detail.get(name)?.tables;
      if (count != null) title.append(el('span', 'service-schema-count', `${count} tables`));
      row.append(title);
      if (detail.get(name)?.storage) row.append(proseLine(detail.get(name).storage));
      owned.append(row);
    }
    body.append(owned);
  }

  // the tables, from the workbook rather than from the diagram
  const tables = service.workbookTables ?? [];
  if (tables.length) {
    body.append(el('div', 'journey-section-label',
      `${tables.length} tables the workbook ships in this service`));
    const grid = el('div', 'service-tables');
    for (const name of [...tables].sort()) {
      const button = el('button', 'service-table', name);
      button.onclick = () => { setLayer('backend'); selectTable(name); setMode('data'); };
      grid.append(button);
    }
    body.append(grid);
  }

  // who it reads, who it writes
  const neighbours = [
    ['reads from', service.readsFrom, 'operations'],
    ['writes outside itself', service.writesOutside, 'operations'],
  ];
  for (const [label, rows, unit] of neighbours) {
    if (!rows?.length) continue;
    body.append(el('div', 'journey-section-label', label));
    const list = el('div', 'service-edges');
    for (const row of rows) {
      const line = el('div', 'service-edge');
      const pair = el('div', 'service-edge-pair');
      const name = el('button', 'service-edge-name', String(row.service).replace(/Service$/, ''));
      name.onclick = () => {
        const key = diagrams.services.find((other) =>
          other.name === row.service || other.key === String(row.service).toLowerCase().replace(/service$/, ''))?.key;
        if (key) { selectService(key); renderService(); }
      };
      pair.append(name);
      line.append(pair);
      const counts = el('div', 'service-edge-counts');
      counts.append(el('b', null, String(row.operations ?? 0)), el('span', null, unit));
      line.append(counts);
      if (row.why) line.append(proseLine(row.why, 'service-edge-why'));
      list.append(line);
    }
    body.append(list);
  }

  // the operations, by contract
  for (const group of service.operationsByContract ?? []) {
    body.append(el('div', 'journey-section-label',
      `${group.count} operations in ${group.contract}`));
    const grid = el('div', 'service-ops');
    for (const op of group.operations ?? []) {
      const button = el('button', 'service-op');
      button.append(el('span', `verb ${String(op.verb ?? '').toLowerCase()}`, op.verb ?? ''));
      button.append(el('span', 'service-op-name', op.operation));
      button.title = `${op.verb ?? ''} ${op.path ?? ''}${op.scope ? ` · ${op.scope}` : ''}`;
      button.onclick = () => openOperation(op.operation);
      grid.append(button);
    }
    body.append(grid);
  }

  // the journeys that walk it
  for (const [label, rows, go] of [
    ['flows that walk it', service.flows, openServiceFlow],
    ['screens it serves', service.screens, openServiceScreen],
  ]) {
    if (!rows?.length) continue;
    body.append(el('div', 'journey-section-label', `${rows.length} ${label}`));
    const grid = el('div', 'service-tables');
    for (const text of rows) {
      const button = el('button', 'service-table', String(text));
      button.onclick = () => go(text);
      grid.append(button);
    }
    body.append(grid);
  }
}

// ── context, for building against this package ───────────────────────
//
// Every other view here is for reading. This one is for a coding session: the
// handful of files that define one service, so whatever loads context loads
// those and not the whole delivery.
//
// Nothing here assumes an MCP server, and none is configured in this package —
// it produces the lists, and wiring them to a command belongs wherever that
// server is defined.

/** Where a contract named `orders` actually lives. */
function contractPath(stem) {
  const node = state.index?.nodes?.find(
    (n) => n.type === 'file'
      && String(n.file ?? '').split('/').pop().replace(/\.ya?ml$/, '') === stem
  );
  return node?.file ?? null;
}

/**
 * The files that define one service, and what each answers.
 *
 * Ordered the way somebody should read them: what it is, then the interface it
 * serves, then the data it owns, then why it is shaped that way. An agent that
 * reads the contract and not the LLD will confidently move a table across the
 * boundary the LLD exists to defend, which is the failure this ordering is
 * against.
 */
function contextFor(service) {
  const rows = [];
  if (service.detailFile) {
    rows.push([service.detailFile,
      'what this service is, what it owns, and why it is one service']);
  }
  rows.push([hldFile(),
    'where it sits, what it may write, and what deploys before it']);
  for (const stem of service.contracts ?? []) {
    const file = contractPath(stem);
    if (file) rows.push([file, `the ${stem} API it serves`]);
  }
  if (state.backend?.file) {
    rows.push([state.backend.file,
      `the schema reference — its ${service.workbookTables?.length ?? 0} tables and their columns`]);
  }
  // The workbook's Migration cell is prose, not a filename — `V0001 / V0003 /
  // V0003a`, `V0003b (part) / V0011`, `unassigned`. So the version tokens come
  // out of it and are matched against the six files actually in backend/, which
  // the migrations payload lists with their versions.
  //
  // A version with no file contributes nothing rather than a path that 404s:
  // V0007 upwards are not written yet, and a list of paths whose whole job is to
  // be pasted somewhere is worse than useless when some of them do not exist.
  const fileFor = new Map(
    (state.backend?.migrations?.files ?? []).map((m) => [m.version, m.name])
  );
  const owned = new Set(service.workbookTables ?? []);
  const migrations = new Set();
  for (const table of state.backend?.tables ?? []) {
    if (!owned.has(table.name) || !table.migration) continue;
    for (const [version] of String(table.migration).matchAll(/\bV\d{3,4}[a-z]?\b/g)) {
      const name = fileFor.get(version);
      if (name) migrations.add(`backend/${name}`);
    }
  }
  for (const file of [...migrations].sort()) {
    rows.push([file, 'the SQL that creates its tables']);
  }
  if (state.diagrams?.decision) {
    rows.push([state.diagrams.decision, 'why the services are cut where they are']);
  }
  return rows;
}

function copyToClipboard(text, said) {
  navigator.clipboard.writeText(text)
    .then(() => toast(said))
    .catch(() => toast('The browser would not give access to the clipboard'));
}

function renderContext() {
  const body = $('context-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  if (!diagrams?.present) {
    body.append(el('p', 'pane-empty', 'No diagrams/ in this package.'));
    $('context-hint').textContent = '';
    return;
  }

  const service = serviceByKey(state.serviceKey) ?? diagrams.services[0];
  if (!service) return;
  state.serviceKey = service.key;

  const rows = contextFor(service);
  $('context-hint').textContent =
    `${service.name.replace(/Service$/, '')} · ${rows.length} files`;

  const head = el('div', 'journey-head');
  head.append(el('div', 'artefact-kind', 'For building, not reading'));
  head.append(el('h2', 'journey-title', `Context for ${service.name}`));
  head.append(proseLine(
    'The files that define this service \u2014 **' + rows.length + ' out of the whole package**. '
    + 'Paths are relative to the package root. Pick a service on the left to change them.',
    'journey-trigger'));
  body.append(head);

  const paths = rows.map(([file]) => file).join('\n');
  const brief =
    `Read these before changing ${service.name}. Paths are relative to the package root.\n\n`
    + rows.map(([file, why]) => `${file}\n    ${why}`).join('\n')
    + `\n\nThe rule this service is cut by: no service spans a schema it does not own, and no `
    + `schema is written by two services. The owner defines a row; a foreign writer may only `
    + `append to it.`;

  const actions = el('div', 'context-actions');
  const copy = (label, text, said) => {
    const button = el('button', 'context-copy', label);
    button.onclick = () => copyToClipboard(text, said);
    return button;
  };
  actions.append(copy('Copy the paths', paths, `${rows.length} paths copied`));
  actions.append(copy('Copy the brief', brief, 'The brief is on the clipboard'));
  body.append(actions);

  body.append(el('div', 'journey-section-label', 'what each file answers'));
  const list = el('div', 'context-files');
  for (const [file, why] of rows) {
    const row = el('div', 'context-file');
    const name = el('button', 'context-path', file);
    name.onclick = () => copyToClipboard(file, `${file} copied`);
    row.append(name);
    row.append(el('div', 'context-why', why));
    list.append(row);
  }
  body.append(list);

  // The names, not the paths. A service touches dozens of each and pasting
  // sixty file paths into a session is how a context window is spent on
  // things nobody asked about — but knowing which ones exist is worth having.
  for (const [label, items] of [
    ['flows that walk it', service.flows ?? []],
    ['screens it serves', service.screens ?? []],
  ]) {
    if (!items.length) continue;
    body.append(el('div', 'journey-section-label', `${items.length} ${label}`));
    const chips = el('div', 'service-tables');
    for (const text of items) chips.append(el('span', 'service-table', String(text)));
    body.append(chips);
  }

  body.append(el('div', 'journey-section-label', 'connecting this to a session'));
  body.append(proseLine(
    'This package has no MCP server configured. When one is, these are the paths a command '
    + 'should load: **the list above is the whole answer for one service**, and the same shape '
    + 'works for a layer or a flow. Point the server at the package root and the paths resolve '
    + 'as they are.'));
}

// ── deploy order ─────────────────────────────────────────────────────
function renderDeploy() {
  const body = $('deploy-body');
  const diagrams = state.diagrams;
  body.innerHTML = '';

  if (!diagrams?.present) {
    body.append(el('p', 'pane-empty', 'No diagrams/ in this package.'));
    $('deploy-hint').textContent = '';
    return;
  }

  const steps = diagrams.deployOrder ?? [];
  $('deploy-hint').textContent =
    `${steps.length} steps · ${diagrams.survivable.length} services may be down`;

  const head = el('div', 'journey-head');
  // The same artefact as the Map. Saying so is the point: three views over two
  // files reads as three sources unless the files are named.
  head.append(el('div', 'artefact-kind', 'High-level design \u00b7 deploy order'));
  head.append(el('h2', 'journey-title', 'What ships in what order'));
  head.append(proseLine(
    'A service is deployable once everything it writes already exists, so the order is a ' +
    'consequence of the arrows on the map rather than a separate decision.', 'journey-trigger'));
  head.append(sourceLine(hldFile(), diagrams.generatedBy));
  body.append(head);

  const list = el('div', 'deploy-steps');
  for (const step of steps) {
    const row = el('div', 'deploy-step');
    const badge = el('div', 'deploy-order');
    badge.textContent = String(step.order ?? '');
    badge.style.background = tierColour(step.tier);
    row.append(badge);

    const box = el('div', 'deploy-body-col');
    box.append(el('div', 'deploy-tier', step.tier ?? ''));
    const names = el('div', 'service-row tight');
    for (const key of step.services) {
      const service = serviceByKey(key);
      if (!service) continue;
      const button = el('button', 'service-pill');
      button.style.setProperty('--tier', tierColour(step.tier));
      button.textContent = service.name.replace(/Service$/, '');
      if (diagrams.survivable.includes(key)) button.classList.add('survivable');
      button.onclick = () => { selectService(key); setMode('service'); };
      names.append(button);
    }
    box.append(names);
    if (step.rule) box.append(proseLine(step.rule));
    row.append(box);
    list.append(row);
  }
  body.append(list);

  if (diagrams.survivable?.length) {
    body.append(el('div', 'journey-section-label',
      'may be down while a sale still goes through'));
    const grid = el('div', 'service-tables');
    for (const key of diagrams.survivable) {
      const service = serviceByKey(key);
      const button = el('button', 'service-table',
        (service?.name ?? key).replace(/Service$/, ''));
      button.onclick = () => { selectService(key); setMode('service'); };
      grid.append(button);
    }
    body.append(grid);
  }

  if (diagrams.notes) {
    body.append(el('div', 'journey-section-label', 'notes'));
    body.append(proseLine(diagrams.notes));
  }
}

// ── contracts: lineage ───────────────────────────────────────────────
// Which tables an operation touches. This cannot be derived from the contracts
// — `x-ticvai-persistence` says which schemas become tables, not which
// operations reach them — so it arrives as data, and the data is candid about
// how much of itself is guesswork. That candour is the design constraint here:
// an unresolved operation is drawn, not dropped.

const ROUTING_TOKENS = {
  primary: 'error',
  replica: 'ok',
  analytical: 'patch',
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

// ── the lineage, as a join ───────────────────────────────────────────
// Which tables an operation touches is the one thing the viewer cannot work out
// for itself — the contracts say which schemas become tables and nothing in
// them says which operations reach them, which is why
// `handoff/api-data-lineage.json` exists and was filled in by hand.
//
// Three sheets already read it one row at a time. What none of them can be
// sorted into is the question a reviewer actually has: which tables more than
// one service writes. That is a boundary, and a boundary that nobody drew is
// the kind that gets crossed.

let lineageGalaxySummary = '';
let appsGalaxySummary = '';

function describeAppsHub(hub) {
  if (hub.contractFile) {
    return `${hub.name} · ${hub.operations} operation${hub.operations === 1 ? '' : 's'} called by apps`
      + ' · double-click to open it';
  }
  return [
    hub.full ?? hub.name,
    `${hub.mass} screens`,
    `${hub.contracts} contracts`,
    hub.offline ? 'queues writes offline' : 'online only',
    hub.hot ? `${hub.hot} calls no contract declares` : null,
  ].filter(Boolean).join(' · ');
}

function describeLineageHub(hub) {
  if (hub.table) {
    return [
      hub.name,
      `${hub.weight} operation${hub.weight === 1 ? '' : 's'}`,
      hub.services > 1 ? `**${hub.services} services touch it**` : 'one service',
      hub.written ? `${hub.written} of them write` : 'read only',
      'double-click to open it',
    ].join(' · ').replace(/\*\*/g, '');
  }
  return `${hub.full ?? hub.name} · ${hub.operations} operations · ${hub.weight} tables`;
}

/**
 * Services on the inner shell, the tables they touch on the outer.
 *
 * This was drawn on two flat rings, on the reasoning that a join between two
 * sets has no meaningful third dimension. That is true, and it turned out not
 * to be an argument for a circle: what carries the claim is *inside against
 * outside*, and a shell says that as plainly as a ring while seating far more
 * names — a ring of radius r has 2πr of edge to put labels on, a shell of the
 * same radius has 4πr² of surface. At 31 services and 90 shared tables the ring
 * version had labels lying across each other in the middle of the picture.
 *
 * The rings are still there, as the 2D layout, which is what they were always
 * the right answer for.
 */
function buildLineageGalaxy() {
  const lineage = state.lineage;
  const services = lineage?.services ?? [];
  // how many services touch each table, and how many of them write to it
  const touched = new Map();
  for (const service of services) {
    for (const table of new Set([...(service.reads ?? []), ...(service.writes ?? [])])) {
      const row = touched.get(table) ?? { services: 0, writers: 0 };
      row.services += 1;
      if ((service.writes ?? []).includes(table)) row.writers += 1;
      touched.set(table, row);
    }
  }
  const opsOn = new Map(
    (lineage?.tables ?? []).map((t) => [t.table, t.reads.length + t.writes.length])
  );

  const hubs = [];
  for (const service of services) {
    const own = [...new Set([...(service.reads ?? []), ...(service.writes ?? [])])];
    if (!own.length) continue;
    const alone = own.filter((table) => (touched.get(table)?.services ?? 0) === 1);
    hubs.push({
      id: `service:${service.name}`,
      // Every one of the 31 ends in "Service", so the suffix is 40% of the
      // label width spent repeating what the legend already says. The full
      // name stays for the hint line and the toast.
      name: service.name.replace(/Service$/, ''),
      full: service.name,
      weight: Math.max(1, own.length),
      operations: service.operations?.length ?? 0,
      owns: own.length,
      alone: alone.length,
      tier: 'spine',
      shell: 0.68,
      ring: 0.46,
      // A table one service owns is that service's business. It gets a mote in
      // the service's halo rather than a node of its own, which is what lets
      // the ones that matter be seen at all: 318 dots on a ring, none of them
      // labelled, is 318 things to read that say nothing.
      mass: alone.length,
    });
  }
  for (const [table, row] of touched) {
    // Only the shared ones are named. That is the whole question the view
    // exists to ask — a table two services write is a boundary, and a boundary
    // nobody drew is the kind that gets crossed.
    if (row.services < 2) continue;
    hubs.push({
      id: `table:${table}`,
      name: table,
      table,
      weight: Math.max(1, opsOn.get(table) ?? 1),
      services: row.services,
      written: row.writers,
      // `core` is the amber for a table two services write, not a claim that
      // it belongs inside them — every table sits on the outer shell.
      tier: row.writers > 1 ? 'core' : 'satellite',
      shell: 1,
      ring: 1,
    });
  }

  const known = new Set(hubs.map((h) => h.id));
  const links = [];
  for (const service of services) {
    for (const table of new Set([...(service.reads ?? []), ...(service.writes ?? [])])) {
      if (!known.has(`table:${table}`) || !known.has(`service:${service.name}`)) continue;
      links.push({
        source: `service:${service.name}`,
        target: `table:${table}`,
        critical: (service.writes ?? []).includes(table),
      });
    }
  }

  const shared = [...touched.values()].filter((r) => r.services > 1).length;
  const contested = [...touched.values()].filter((r) => r.writers > 1).length;
  return { hubs, links, services: services.length, tables: touched.size, shared, contested };
}

function renderLineageGalaxy() {
  const built = buildLineageGalaxy();
  lineageGalaxy.labelMax = 40;
  lineageGalaxy.setData(built);
  lineageGalaxy.setMode(state.galaxyMode);
  lineageGalaxy.start();

  lineageGalaxySummary =
    `${built.services} services · ${built.tables} tables · `
    + `${built.shared} touched by more than one service, drawn`
    + (built.contested ? ` · ${built.contested} written by more than one` : '')
    + ` · the rest sit with the service that owns them`;
  $('lineage-hint').textContent = lineageGalaxySummary;

  galaxyLegend($('lineage-legend'), [
    ['spine', 'a service, on the inner shell'],
    ['core', 'a table more than one service writes'],
    ['satellite', 'a table more than one service reads'],
  ], 'dot size is how many operations reach it · the halo round a service is the tables '
     + 'only it touches · an amber lane is a write · double-click a table to open it');
}

function renderLineage() {
  const map = state.lineageLayout === 'map';
  $('lineage-body').hidden = map;
  $('lineage-galaxy').hidden = !map;
  $('lineage-legend').hidden = !map;
  $('lineage-mode').hidden = !map;
  $('lineage-scope').hidden = map;
  $('lineage-filter').hidden = map;
  $('lineage-unresolved').closest('.toggle').hidden = map;

  if (map) {
    if (!state.lineage) {
      lineageGalaxy.setData({ hubs: [], links: [] });
      $('lineage-hint').textContent = 'Reading the data lineage…';
      return;
    }
    renderLineageGalaxy();
    return;
  }
  lineageGalaxy.stop();
  renderLineageList();
}

function renderLineageList() {
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
    // gave it all of them at once — at the time 654 operations across 24
    // contracts, 7,098 elements — for a
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
      chip.style.borderColor = ROUTING_TOKENS[op.routing] ? hue(ROUTING_TOKENS[op.routing]) : 'currentColor';
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
        `One of the few operations that runs as a stored procedure. **Services for all {operations} ` +
        `operations, stored procedures for {storedProcedures}** — a procedure per operation would be a second ` +
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
      tip(chip, op.service, 'The service that owns this operation. {services} services across {operations} operations.');
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
        'the same. {unresolved} of the {operations} are in this state.');
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
      [entry.writes.length, 'written by', hue('error')],
      [entry.reads.length, 'read by', hue('ok')],
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
  renderBoxLegend(legend, [[hue('error'), 'written by'], [hue('ok'), 'read by']],
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
      `One of the {services} services the {operations} operations divide into. It owns ${service.operations.length} ` +
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
    [['var(--accent)', 'reaches a table'], ['var(--text-dim)', 'names an operation'], [hue('error'), 'names none']],
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
  // The node fall-through belongs to Contracts alone.
  //
  // `state.nodesById` holds contract artefacts and nothing else — a schema, an
  // operation, a file — and `select()` is the only thing that writes
  // `selectedId`. The Decisions layer never calls it: it tracks its own choice
  // in `state.adrId`. So reading `selectedId` here meant that on Decisions the
  // pane showed whichever contract the reader last clicked, under a heading
  // about decisions. The clear above fixed the *text* left behind on a layer
  // with no selection; this is the same leak carrying real content, which is
  // the harder one to notice because it looks like an answer.
  //
  // `selectedId` is deliberately not cleared when the layer changes. Clearing
  // it would cost the reader their place in Contracts on every excursion;
  // scoping the read keeps it, and coming back restores the pane.
  const node = state.layer === 'contracts' && state.selectedId
    ? state.nodesById.get(state.selectedId)
    : null;
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
    dot.style.background = hue('ok');
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
          dot.style.background = write ? hue('error') : hue('ok');
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
              ? 'The lineage carries no tables for this operation — {unresolved} of the {operations} are in ' +
                'that state. It is not a claim that it touches nothing.'
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
    dot.style.background = table.migration ? hue('ok') : hue('info');
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
            ? 'The lineage carries no tables for this operation. {unresolved} of the {operations} are in that state: ' +
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
      'across all {operations} operations at once.')
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
    // The description is markdown — headings, a table of tiers and consumers,
    // bold labels, fenced examples. It was being set as text content inside a
    // `white-space: pre-wrap` block, so every `##`, every `**` and the whole
    // header table rendered as literal syntax in one undifferentiated slab.
    // ADR links are off: this view has no handler for them.
    const desc = markdownBlock(node.description.trim(), { adrLinks: false });
    desc.classList.add('reader-desc');
    head.append(desc);
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
  const res = await auth.apiFetch(`/api/file?path=${encodeURIComponent(relPath)}`);
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
    // U+00D7 rather than U+2715: the multiplication sign is in Latin-1 and so
    // is in every font that can render the message beside it. The other two are
    // ASCII already.
    item.append(el('span', 'audit-icon', problem.severity === 'error' ? '\u00d7' : problem.severity === 'warning' ? '!' : 'i'));
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

// ── keyboard navigation for the canvases ─────────────────────────────
/**
 * Which way the offset moves for each arrow, as [dx, dy] multipliers.
 *
 * The arrow moves the *reader*, not the drawing: pressing Right looks further
 * right, which means the picture slides left, which means the offset goes down.
 * Written out rather than negated at the call site because the sign is the one
 * thing that gets this backwards, and a table can be read.
 */
const ARROW_PAN = {
  ArrowLeft: [1, 0],
  ArrowRight: [-1, 0],
  ArrowUp: [0, 1],
  ArrowDown: [0, -1],
};

/**
 * The renderer whose canvas is on screen, or null if none is.
 *
 * Graph, StructureTree, BoxDiagram and StateMachine each hold their own canvas
 * and a { x, y, k } transform, so "move the thing the reader is looking at" is
 * one lookup rather than a mode-to-renderer table that has to be extended every
 * time a view is added — which is the table that would quietly go stale.
 *
 * getClientRects() rather than `.hidden`: several of these are hidden by an
 * ancestor rather than by their own attribute, and `.hidden` cannot see that.
 */
function activeDiagram() {
  // Galaxies first. Every galaxy view has a flat canvas behind it for the 2D
  // cut, and the Contracts graph opens on the galaxy with `#graph-canvas`
  // hidden — so a list that checked the flat renderers first would answer with
  // the one nobody is looking at.
  const all = [
    graphGalaxy, dataGalaxy, lineageGalaxy, appsGalaxy, servicesGalaxy, eventGalaxy,
    graph, tree, er, serviceEr, data, machine,
  ];
  for (const d of all) {
    if (d?.canvas?.getClientRects().length) return d;
  }
  return null;
}

/**
 * Zoom a diagram about the middle of its canvas.
 *
 * The wheel zooms toward the cursor, which a key has no equivalent of, so the
 * middle is the anchor — it is where the eye already is after panning there.
 *
 * Two projections to serve. Graph, BoxDiagram and StateMachine put world origin
 * at the centre of the canvas, so holding the middle still is a straight scale
 * of the offset. StructureTree projects from the top-left corner instead and
 * says so at its enableTouch call; for that one the offset has to be solved. A
 * `toWorld` method is what separates them — the tree is the one without.
 */
function zoomDiagram(d, factor) {
  const t = d.transform;
  const k0 = t.k;
  const k1 = Math.max(0.1, Math.min(3, k0 * factor));
  if (k1 === k0) return;
  if (typeof d.toWorld === 'function') {
    t.x *= k1 / k0;
    t.y *= k1 / k0;
  } else {
    const cx = (d.width ?? d.canvas.clientWidth) / 2;
    const cy = (d.height ?? d.canvas.clientHeight) / 2;
    const wx = (cx - t.x) / k0;
    const wy = (cy - t.y) / k0;
    t.x = cx - wx * k1;
    t.y = cy - wy * k1;
  }
  t.k = k1;
  d.draw();
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
    // Hover moves the highlight and nothing else.
    //
    // This called renderPalette(), which empties the box and rebuilds every
    // row. So the row under the pointer was destroyed and replaced the moment
    // it was entered, the replacement fired its own mouseenter, and the list
    // churned for as long as the pointer sat still. A click needs mousedown and
    // mouseup on the *same* element and there was never one, so search results
    // were reachable by keyboard only — clicking one did nothing at all.
    item.onmouseenter = () => setPaletteActive(i);
    // Keep the caret in the search field. Without this, pressing on a row blurs
    // the input and the arrow keys stop reaching the list.
    item.onmousedown = (e) => e.preventDefault();
    item.onclick = () => { select(node.id); setMode('reader'); closePalette(); };
    box.append(item);
  });

  box.querySelector('.active')?.scrollIntoView({ block: 'nearest' });
}

/**
 * Move the palette highlight without rebuilding the list.
 *
 * The rows are static once drawn — only which one is active ever changes — so a
 * re-render buys nothing and costs the click, for the reason written on the
 * hover handler above. The pointer and the arrow keys both come through here,
 * so the two cannot drift into disagreeing about what "active" means.
 */
function setPaletteActive(i) {
  if (!paletteItems.length) return;
  paletteActive = Math.max(0, Math.min(paletteItems.length - 1, i));
  const rows = $('palette-results').children;
  for (let n = 0; n < rows.length; n += 1) {
    rows[n].classList.toggle('active', n === paletteActive);
  }
  rows[paletteActive]?.scrollIntoView({ block: 'nearest' });
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
  const source = new EventSource(auth.apiUrl('/api/events'), { withCredentials: true });
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
 * the rest — fifteen platforms, the largest 143 screens, which is the list that made
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
    // Never reopen already armed. This panel is opened and closed all day, and
    // a confirm left standing from a change of mind ten minutes ago would sit
    // one click from ending every session on the account.
    disarmSignOutAll();
  }
}

/** Puts "Sign out everywhere" back to its resting state — asking nothing. */
function disarmSignOutAll() {
  $('signout-all').hidden = false;
  $('signout-all-confirm').hidden = true;
  $('signout-all-error').hidden = true;
  $('signout-all-go').disabled = false;
  $('signout-all-go').textContent = 'Yes, end every session';
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

  // Shown for anyone signed in, whether or not anything is waiting — and
  // before the fetch, so a slow or unreachable accounts service does not take
  // the control with it.
  //
  // It used to appear only once somebody had named you, which turned a thing
  // you are meant to *check* into one that materialises out of the chrome.
  // Nothing is where you last saw it, so its absence reads as breakage rather
  // than as quiet — and there is no way to confirm you have nothing waiting,
  // because the control that would tell you is the one that is missing. Empty
  // is a state a bell can say out loud. Gone is not.
  bell.hidden = false;

  let payload = null;
  try {
    payload = await auth.myMentions();
  } catch {
    return;                       // the viewer is not about this
  }
  mentionCache = payload.mentions ?? [];
  const unseen = payload.unseen ?? 0;

  // Only the *unread* mark comes and goes. The bell itself stays put, and it
  // keeps the history: "what did that say again" is a question people ask an
  // hour after reading something, and a control that empties itself on the
  // last read takes the answer with it.
  bell.classList.toggle('has-mentions', unseen > 0);
  bell.title = unseen
    ? `${unseen} note${unseen === 1 ? '' : 's'} named you`
    : mentionCache.length
      ? 'Where you were named'
      : 'No notifications';

  const count = $('bell-count');
  count.textContent = unseen > 9 ? '9+' : String(unseen);
  count.hidden = unseen === 0;

  if (link) {
    link.textContent = unseen ? `Review activity - ${unseen} named you` : 'Review activity';
    link.classList.toggle('auth-button-loud', unseen > 0);
  }
}

/** The other half of `showMentionCount`: the bell persists across having
 *  nothing to say, but not across having nobody to say it to. Signed out there
 *  is no "you" for a note to have named, so the control goes with the session
 *  rather than sitting there offering to show a stranger somebody's mail. */
function hideBell() {
  const bell = $('bell-toggle');
  if (!bell) return;
  mentionCache = [];
  bell.hidden = true;
  bell.classList.remove('has-mentions');
  $('bell-count').hidden = true;
  if (!$('bell-panel').hidden) closeBellPanel();
}

/** The panel behind the bell. Drawn from what the count already fetched, so
 *  opening it costs nothing and never shows a spinner over three rows. */
function renderBellPanel() {
  const list = $('bell-list');
  list.innerHTML = '';
  const unseen = mentionCache.filter((m) => !m.seen_at).length;
  $('bell-note').textContent = mentionCache.length
    ? (unseen ? `${unseen} unread of ${mentionCache.length}` : `${mentionCache.length}, all read`)
    : 'No notifications';
  $('bell-seen').hidden = unseen === 0;

  // Said in the list rather than only in the line above it, because the empty
  // list is the thing the eye lands on and a blank box is ambiguous between
  // "nothing here" and "did not load". It also says what would put something
  // here, which is the question anyone reading an empty inbox actually has.
  if (!mentionCache.length) {
    const empty = el('p', 'bell-empty');
    empty.append('Nobody has named you yet. When someone writes ');
    empty.append(el('span', 'bell-empty-handle', `@${auth.account()?.email ?? 'your address'}`));
    empty.append(' in a note on a contract, a screen or a table, it will show up here.');
    list.append(empty);
    return;
  }

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
    // Same landing as Sign out everywhere below, and for the same reason: the
    // session behind this panel is gone, so closing the panel would leave a
    // fully drawn viewer — the tree, the graph, somebody's verdicts — sitting
    // there looking signed in. Every next click would 401 and bounce, which
    // reads as the app breaking rather than as the sign-out having worked.
    // Arriving at the door is also how somebody knows it did.
    location.replace('/login.html');
  };

  // Two presses, and the second one is a different button under a paragraph
  // that says what the first one only implies. Same shape as sending a verdict
  // back on the reviews page: pressing the control opens it rather than doing
  // it. confirm() would have been a line, and would have been a browser dialog
  // nobody reads on a control whose entire problem is that people do not
  // expect what it does.
  $('signout-all').onclick = () => {
    $('signout-all').hidden = true;
    $('signout-all-confirm').hidden = false;
    $('signout-all-error').hidden = true;
    $('signout-all-go').focus();
  };
  $('signout-all-cancel').onclick = disarmSignOutAll;

  $('signout-all-go').onclick = async () => {
    $('signout-all-error').hidden = true;
    $('signout-all-go').disabled = true;
    $('signout-all-go').textContent = 'Ending every session…';
    try {
      await auth.logoutAll();
      // Everywhere included here, so there is no signed-in viewer left behind
      // this panel to return to. The door is the only honest place to land,
      // and arriving there is also how somebody knows it worked.
      location.replace('/login.html');
    } catch (error) {
      // Nothing was revoked, so nothing about the panel changes except this
      // line. Leaving it armed is deliberate: the usual cause is the service
      // being down for a moment, and the next press is the one that works.
      $('signout-all-error').textContent = error.message;
      $('signout-all-error').hidden = false;
      $('signout-all-go').disabled = false;
      $('signout-all-go').textContent = 'Yes, end every session';
    }
  };

  auth.onAuthChange(() => {
    renderAccountButton();
    // The bell has to be told on sign-in, not on the first time somebody opens
    // the account panel. It was hanging off renderAccountPanel, which meant the
    // one control whose job is to tell you something unprompted only appeared
    // once you had gone looking — exactly the failure it exists to fix.
    if (auth.account()) showMentionCount();
    else hideBell();
    if (!$('account-panel').hidden) renderAccountPanel();
  });
  auth.refreshSession();
}

/**
 * A segmented control that writes one field of state and asks for a redraw.
 *
 * The structure view has had one of these since it grew a tree mode, written
 * inline. Every galaxy view wants the same behaviour twice over — which reading,
 * and 3D or 2D — so it is a function rather than a seventh copy.
 */
/**
 * Every bar bound to a given state field, so they can be kept in step.
 *
 * `galaxyMode` is one field read by four separate trays — Events, Data, Graph
 * and Lineage all offer 3D/2D and all write the same value, deliberately, so a
 * reader who picks flat once gets flat everywhere. Marking the active button on
 * only the bar that was clicked meant the other three went on showing whatever
 * was chosen the last time *they* were touched: switch Events to 2D, open the
 * Graph, and its tray says 3D over a flat picture.
 */
const SEG_BARS = new Map();

function syncSegs(field) {
  for (const { bar, attribute } of SEG_BARS.get(field) ?? []) {
    for (const button of bar.querySelectorAll('button')) {
      button.classList.toggle('active', button.dataset[attribute] === state[field]);
    }
  }
}

function bindSeg(id, attribute, field, redraw) {
  const bar = $(id);
  if (!bar) return;
  if (!SEG_BARS.has(field)) SEG_BARS.set(field, []);
  SEG_BARS.get(field).push({ bar, attribute });

  for (const button of bar.querySelectorAll('button')) {
    const value = button.dataset[attribute];
    button.onclick = () => {
      if (state[field] === value) return;
      state[field] = value;
      syncSegs(field);
      redraw();
    };
  }
  syncSegs(field);
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
      syncUrl();
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
  bindSeg('events-layout', 'layout', 'eventsLayout', () => renderEvents());
  bindSeg('events-mode', 'mode', 'galaxyMode', () => eventGalaxy.setMode(state.galaxyMode));
  $('events-critical').onchange = () => renderEventGalaxy();

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
  if ($('contracts-shared')) $('contracts-shared').onchange = () => renderContractsHld();
  $('data-ambient').onchange = () => {
    data.userAdjusted = false;
    renderData({ focus: state.tableName });
  };
  $('data-fit').onclick = () => { data.resize(); data.fit(); };

  $('services-graph-reset').onclick = () => servicesGalaxy.resetView();

  $('er-services-fit').onclick = () => {
    serviceEr.userAdjusted = false;
    serviceEr.resize();
    serviceEr.fit();
  };
  $('er-services-reads').onchange = (event) => {
    state.serviceErReads = event.target.checked;
    renderServiceEr();
  };
  bindSeg('data-layout', 'layout', 'dataLayout', () => renderData({ focus: state.tableName }));
  bindSeg('data-mode', 'mode', 'galaxyMode', () => dataGalaxy.setMode(state.galaxyMode));

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
  bindSeg('graph-mode', 'mode', 'galaxyMode', () => graphGalaxy.setMode(state.galaxyMode));
  bindSeg('services-graph-mode', 'mode', 'galaxyMode',
    () => servicesGalaxy.setMode(state.galaxyMode));
  bindSeg('lineage-mode', 'mode', 'galaxyMode', () => lineageGalaxy.setMode(state.galaxyMode));
  bindSeg('apps-layout', 'layout', 'appsLayout', renderApps);
  bindSeg('apps-mode', 'mode', 'galaxyMode', () => appsGalaxy.setMode(state.galaxyMode));

  bindSeg('lineage-layout', 'layout', 'lineageLayout', () => renderLineage());

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
    const next = document.documentElement.dataset.theme !== 'dark' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('ticvai-theme', next);
    // colour dots are inline styles, so anything already painted must repaint
    renderTree();
    renderLegend();
    // Re-render the rail through the dispatch rather than calling
    // `renderLinksPane` on the contract selection directly: that is the
    // Contracts renderer, and on any other layer a theme flip would repaint the
    // rail with the last contract's links — the leak fillSidePane exists to
    // stop, coming back through a repaint.
    renderSidePane();
    renderStructLegend();
    graph.draw();
    tree.draw();
    er.draw();
    data.draw();
    // The galaxies keep their own palette on a fixed dark field, so a theme
    // change does not alter them — but their legends are viewer chrome and the
    // hint lines beside them are not, so the views that own one are re-asked.
    if (state.mode === 'events') renderEvents();
    if (state.mode === 'lineage') renderLineage();
  };

  // Restoring the saved theme lives in core.js now, so the standalone pages —
  // reviews, domains, platforms — get it too. They never imported this file,
  // which is why the toggle only ever held on the main view.

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
        setPaletteActive(paletteActive + 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setPaletteActive(paletteActive - 1);
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

    // Escape, once nothing else has claimed it — the palette and the drawer
    // both take it first, above. From a view with nothing open it means "out",
    // and out of the viewer is the door.
    if (e.key === 'Escape'
        && !(e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA'
             || e.target.isContentEditable)) {
      e.preventDefault();
      location.href = '/home.html';
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

    // Arrow keys move whichever diagram is on screen, and + / - zoom it.
    //
    // Every canvas here has panned by drag and zoomed by wheel since it was
    // written, which is a pointer-only contract: a reader working from the
    // keyboard could open a graph and then not move it. Shift takes a longer
    // step, so crossing a wide graph is a few presses rather than a held key.
    //
    // Below the input guard on purpose — an arrow key inside the tree's filter
    // box belongs to the filter, and a reader typing there is the common case.
    const diagram = activeDiagram();
    if (diagram) {
      const nudge = ARROW_PAN[e.key];
      if (nudge) {
        e.preventDefault();
        const step = e.shiftKey ? 240 : 60;
        // A galaxy is a scene with a camera, not a plane with an offset: the
        // arrow turns it rather than sliding it, and `nudge` takes the same
        // pixels-of-travel a drag would have supplied. The flat renderers move
        // their own { x, y } instead. Told apart by the method rather than by a
        // list of which is which, so a new galaxy needs no edit here.
        if (typeof diagram.nudge === 'function') {
          diagram.nudge(nudge[0] * -step, nudge[1] * -step);
        } else {
          diagram.transform.x += nudge[0] * step;
          diagram.transform.y += nudge[1] * step;
          diagram.draw();
        }
        return;
      }
      // Both faces of each key, so it works with and without shift and on a
      // numpad: a zoom control that depends on which "+" you reached for is a
      // zoom control that looks broken half the time.
      const zoomBy = (f) => (typeof diagram.zoomBy === 'function' ? diagram.zoomBy(f) : zoomDiagram(diagram, f));
      if (e.key === '+' || e.key === '=') { e.preventDefault(); zoomBy(1.15); return; }
      if (e.key === '-' || e.key === '_') { e.preventDefault(); zoomBy(1 / 1.15); return; }
    }

    // 1 2 3 pick the layer, in the order the bar draws them. visibleLayers()
    // rather than LAYERS, because a client is not shown Decisions and the
    // digits have to match the bar in front of *this* reader, not the full set.
    const shown = visibleLayers();
    const layerIndex = Number(e.key) - 1;
    if (Number.isInteger(layerIndex) && layerIndex >= 0 && layerIndex < shown.length) {
      setLayer(shown[layerIndex].key);
      return;
    }

    // q w e r t y pick the view, matched to the tabs left to right. Read
    // against the current layer every time, so the fourth key is the fourth tab
    // of the page you are on rather than a fixed view somewhere else — which is
    // also why none of these jump layers any more. Moving between pages is what
    // the digits are for, and a key that silently changed both was the thing
    // that made the old set hard to trust.
    const slot = MODE_ROW.indexOf(e.key.toLowerCase());
    if (slot >= 0) {
      const modes = visibleModes(layerOf(state.layer));
      // A key past the end of this layer's tabs does nothing, deliberately: the
      // alternative is falling through to whatever else that letter once meant.
      if (slot < modes.length) setMode(modes[slot][0]);
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
    } else if (e.key === 'l' && state.selectedId) {
      state.graphScope = 'local';
      for (const b of $('graph-scope').querySelectorAll('button')) {
        b.classList.toggle('active', b.dataset.scope === 'local');
      }
      renderGraph();
      setMode('graph');
    }
  });
}

// A throw anywhere in boot() would otherwise leave the curtain up for the full
// twelve seconds of the head guard, turning a page that failed fast into one
// that looks like it hung. The error still reaches the console.
boot().catch((error) => { hideLoader(); throw error; });
