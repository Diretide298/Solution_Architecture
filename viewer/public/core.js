/**
 * The things every layer needs and no layer owns.
 *
 * Split out of app.js, which had grown to 7,509 lines holding the router, the
 * state, every render function and the lens logic in one file. The seam is the
 * one the code already described: `LAYERS` names five layers with their own
 * modes and render functions, so the render functions moved out along it and
 * what was left — the shared vocabulary below — moved here.
 *
 * Nothing in this file reaches back into a layer. That is the rule that keeps
 * the split from being a rename: a layer imports from core, never the reverse.
 */
import { tip, GLOSSARY, setFactProvider } from './tips.js';
import './theme.js';   // stamps the saved theme before anything paints

export const LAYERS = [
  {
    key: 'frontend',
    label: 'Frontend',
    hint: 'screens, journeys and the apps that implement them',
    tip:
      'What a person sees. **screens/** defines each one, **flows/** traces a job across ' +
      'several, **frontend/** says which app builds them, and **wireframes/** draws them. ' +
      'Every operation a screen names is resolved against the contracts.',
    // Apps first, and so the one this layer opens on: it is the map of the
    // layer, and Screen is a view of exactly one thing that you go to once you
    // know which thing.
    // Apps is the map of all twelve; Platform is the design of one, which is
    // the question you ask second.
    modes: [
      ['apps', 'Apps'], ['platform-lld', 'Platform'], ['screen', 'Screen'],
      ['journey', 'Journey'], ['waves', 'Waves'], ['audit', 'Audit'],
    ],
    groups: [['platforms', 'Platforms'], ['modules', 'Modules'], ['waves', 'Waves']],
  },
  {
    // **UI/UX is a layer, not a set of pages beside the app.**
    //
    // It was three standalone pages with their own header, their own navigation
    // and their own idea of what the chrome should look like — which is how it
    // ended up with a row of five unrelated chips and no way to tell where you
    // were. A section of the product does not need a second application to live
    // in; it needs a tab.
    //
    // The cost that argument usually loses to is load time, and it does not
    // apply: every layer here fetches its own payload the first time it is
    // opened, and these three views are *imported* the first time they are
    // opened as well. Nothing about the design work is fetched, parsed or drawn
    // for a reader who never opens the tab.
    key: 'uiux',
    label: 'UI/UX',
    hint: 'screens, flows and the design boards they are drawn on',
    tip:
      'The design work. **screens/** and **flows/** drawn as a canvas you can move ' +
      'around, one platform at a time; every board on disk, including the ones no ' +
      'screen points at; and what each platform is still missing. Navigation the ' +
      'package inferred is marked as inferred throughout — two thirds of it is a ' +
      'guess, and a picture is the easiest place to forget that.',
    modes: [
      ['uiux-screens', 'Screens & flows'],
      ['uiux-boards', 'Boards'],
      ['uiux-platforms', 'Platforms'],
    ],
    groups: [['platforms', 'Platforms'], ['modules', 'Modules']],
  },
  {
    key: 'contracts',
    label: 'Contracts',
    hint: 'the API — the join between the other two layers',
    tip:
      'The 24 OpenAPI contracts. **The API is the join between every other layer**, so this ' +
      'sits in the middle and everything else is drawn by resolving against it. Hand-authored; ' +
      'servers and clients are generated from it, never the reverse.',
    // HLD second: the shape of all 28 at once, which is the thing Graph
    // cannot say and every view after it assumes you already know.
    modes: [
      ['graph', 'Graph'], ['contracts-hld', 'HLD'], ['structure', 'Structure'],
      ['er', 'ER'], ['lineage', 'Lineage'], ['reader', 'Reader'], ['audit', 'Audit'],
    ],
    groups: [['contracts', 'Contracts'], ['modules', 'Modules'], ['platforms', 'Platforms']],
  },
  {
    // The key stays `domain`: it is in deep links, API paths and every mode id
    // below. Only the label changes, because only the label was wrong — *domain*
    // names a methodology, and every other layer here names a subject.
    key: 'domain',
    label: 'Lifecycles',
    hint: 'states/ and events/ — the legal moves, and what crosses the outbox',
    tip:
      'What can happen to a thing, and in what order. **A state model is a lifecycle within ' +
      'one entity; an event is one crossing between two** — which is why the two sit in one ' +
      'layer. **states/** says which moves between statuses are legal: 38 enums declare what ' +
      'states exist and none says which transitions are allowed. **events/** says what goes ' +
      'through the outbox when one happens.',
    // Events first, and so the one this layer opens on. States draws one state
     // model at a time and asks which; Events draws the whole layer at once.
    modes: [
      ['events', 'Events'], ['lifecycles-hld', 'HLD'], ['states', 'States'],
      ['audit', 'Audit'],
    ],
    groups: [['entities', 'Entities'], ['contexts', 'Contexts']],
  },
  {
    key: 'backend',
    // The tab says DB and the key stays `backend`. The key is in every deep
    // link, every part name and the API path; the label is the only part of it
    // a reader ever sees, and it is the only part that was wrong.
    label: 'DB',
    hint: 'the SQL in backend/, against the schema reference in handoff/',
    tip:
      'The database. The versioned SQL in **backend/** checked against the schema reference in ' +
      '**handoff/**, so a table that exists can be told from one that is only planned — and ' +
      'every table traces back to the contract schema it came from.',
    modes: [
      ['data', 'Data'], ['migrations', 'Migrations'], ['routing', 'Routing'], ['audit', 'Audit'],
    ],
    groups: [['modules', 'Schemas'], ['status', 'Status'], ['migration', 'Migration']],
  },
  {
    key: 'services',
    // Architecture, not Services. `diagrams/` is a high-level design and sixteen
    // low-level ones, and `docs/diagrams/` draws three pictures of the same
    // thing — together that is the architecture, and "Services" named only what
    // the largest part of it happened to hold. The key stays `services` for the
    // same reason DB kept `backend`: it is in every address and no reader sees
    // it.
    label: 'Architecture',
    hint: 'diagrams/ — the HLD, the sixteen LLDs, and what ships in what order',
    tip:
      'The deployment cut. Sixteen services in five tiers, where **the data boundary decides ' +
      'where they split** — no service spans a schema it does not own, and no schema is written ' +
      'by two. Every number here is stated twice, in **diagrams/** and in the schema workbook, ' +
      'so the two can be checked against each other rather than one being believed.',
    // Ordered by how far out the reader is standing: the shape of the sixteen,
    // then the whole platform, then where configuration lives, then the
    // decomposition, then one service, then the same sixteen pulled apart, then
    // the order they ship in, the bundles and the check.
    //
    // Graph stays first because it is what the layer opens on — `setLayer` takes
    // `modes[0]` when the reader has not chosen — and it is the only view that
    // answers "what shape is this" without first being read.
    //
    // The folder's other two subjects, contracts and lifecycles, are not here.
    // They are the subjects of two layers this viewer already has, and a tab
    // answering a question the tab beside it owns is a worse answer than either.
    // The tabs name the subject, not the document type. `HLD` here used to mean
    // the *services* HLD while the whole-system one was called Overview — a
    // collision that arrived when 00-platform.yaml was added beside a view that
    // had been the only design in the layer. The ids are untouched: a label is
    // read, an id is depended on, and only the label was wrong.
    modes: [
      ['services-graph', 'Graph'], ['overview', 'System'], ['hierarchy', 'Scopes'],
      ['hld', 'Services'], ['service', 'Service'], ['er-services', 'ER'],
      ['deploy', 'Deploy'], ['context', 'Context'], ['audit', 'Audit'],
    ],
    groups: [['tiers', 'Tiers'], ['size', 'Size']],
  },
  {
    key: 'decisions',
    label: 'Decisions',
    hint: 'docs/ — the ADRs, the registers, and the authorisation spec',
    tip:
      'Why the shape is the shape. Everything else here is machine-readable and can be checked ' +
      'mechanically; **docs/** is prose, and prose is where the reasons live. One thing in it is ' +
      'executable — the permission vectors — so the viewer runs them rather than listing them.',
    // Four views of the prose, where there used to be one file tree.
    //
    // The layer a client reviewer opens first was the layer that showed least:
    // 26 ADRs and a conflict register rendered as a directory listing, under a
    // tip saying prose is where the reasons live. Each of these answers a
    // question the tree could not — when, what replaced what, which are open,
    // and what one decision actually says.
    // The one layer with no galaxy in it. Supersession is the nearest thing it
    // has to a map — the only view here that draws a relation between decisions
    // rather than listing them a row at a time — so it opens on that, and the
    // timeline moves to second, where "when" belongs.
    modes: [
      ['supersession', 'Supersession'], ['timeline', 'Timeline'],
      ['register', 'Register'], ['decision', 'Decision'],
      ['decisions', 'Index'], ['audit', 'Audit'],
    ],
    groups: [['decisions', 'Decisions'], ['registers', 'Registers']],
  },
];

/**
 * What each view is for, in one place. Shown on hover over the mode buttons,
 * and reused by the manual — a view whose purpose has to be explained in a
 * conversation is a view nobody opens twice.
 */
export const MODE_TIPS = {
  'services-graph': {
    title: 'Graph',
    body:
      'The sixteen services as a field. **A body is a service, its size is the operations it '
      + 'serves, and the cloud around it is its tables** \u2014 so the weight of the platform is '
      + 'visible before a word of it is read. A lane is a cross-service write. The HLD beside it '
      + 'bands the same sixteen by tier, which is the argument; this is the shape.',
  },
  'platform-lld': {
    title: 'Platform',
    body:
      'One surface\u2019s design: what it is deployed onto, how a release reaches it, the modules ' +
      'it is assembled from and the services it calls. **The services are sized by how many ' +
      'operation calls go that way** \u2014 a platform making 112 calls into one service and 1 into ' +
      'another has a single real dependency, which an alphabetical list would hide.',
  },
  'contracts-hld': {
    title: 'HLD',
    body:
      'All 28 contracts at once, banded by tier. **A satellite reads down into the spine and is ' +
      'never read by it** \u2014 that rule is the reason the shape is worth seeing before any one ' +
      'contract is. Each bar is the verb mix, because a contract that is nine tenths POST is a ' +
      'different kind of thing from one that is nine tenths GET.',
  },
  'lifecycles-hld': {
    title: 'HLD',
    body:
      'Every state model in the package, banded by the contract that owns it, and the 29 events ' +
      'that cross between them. **223 of 1,014 operations are named by a transition** \u2014 a ' +
      'quarter of the API is a state change somewhere. A guarded transition is one with a rule ' +
      'on it, and the rule that a critical finding cannot be signed by whoever raised it lives ' +
      'here and nowhere else.',
  },
  overview: {
    title: 'System — the high-level design',
    body:
      'The whole platform on one page: who uses it, on what surface, against which services, ' +
      'over which stores, and what it depends on outside itself. **Only the boundaries the file ' +
      'actually states are drawn** — an actor to a surface it reaches, an outside system to the ' +
      'service that speaks to it. The rest is counted, not joined, because a line nobody stated ' +
      'would be a line invented here.',
  },
  hierarchy: {
    title: 'Scopes — the hierarchy',
    body:
      'Where configuration lives. Eight scope levels on `platform.scope_node`, which **304 of ' +
      '379 tables anchor on** — a node has a level, a parent and a materialised path, and ' +
      '**configuration resolves by walking that path upward until something answers.** An ' +
      'absent level is skipped rather than empty, which is what makes an optional level free.',
  },
  hld: {
    title: 'Services — all sixteen, the high-level design',
    body:
      'The high-level design, drawn: five tier bands, sixteen services, and an arrow wherever ' +
      'one writes another\'s data. **The arrows are the argument** — a decomposition with none ' +
      'is sixteen databases, and one with too many is a single service in sixteen deployments. ' +
      'Hover a service to see only its own boundaries. The document\'s prose sits below it.',
  },
  context: {
    title: 'Context',
    body:
      'The files that define one service — six to ten paths out of five thousand — ready to ' +
      'paste into a command, a config, or a session. **For building against this package rather ' +
      'than reading it.** The brief version says what each file answers, because an agent given ' +
      'ten paths and no reason guesses at why.',
  },
  'er-services': {
    title: 'ER',
    body:
      'The sixteen services as entities, the schemas they own as their rows, and an edge ' +
      'wherever one depends on another\'s data. **The same diagram as the HLD and a different ' +
      'question**: the HLD fixes everything in its tier so you can read the shape, and this ' +
      'lets you pull one service out and see what it is joined to. Drag a box to pin it.',
  },
  service: {
    title: 'Service — one of the sixteen, the low-level design',
    body:
      'One service, drawn: the contracts it serves above it, the schemas it owns below it, and ' +
      'the services it reads and writes either side. **What a service owns is what it is** — the ' +
      'data boundary is the whole design. The table count comes from the workbook rather than ' +
      'from the diagram, so a service that has drifted from the data says so.',
  },
  deploy: {
    title: 'Deploy',
    body:
      'What ships in what order, and what may be down while a sale still goes through. **Order ' +
      'is a consequence of the arrows**, not a separate decision: a service is deployable once ' +
      'everything it writes already exists.',
  },
  graph: {
    title: 'Graph',
    body:
      'The contracts as a network, in five scopes. **Spine** is the architecture picture — ' +
      'contracts joined by the events between them. The others show `$ref`s, permissions, and ' +
      'the neighbourhood of whatever is selected.',
  },
  structure: {
    title: 'Structure',
    body:
      'What is actually inside one contract file, as a block diagram. Every mapping and ' +
      'sequence is a block; scalars are rows inside their parent, so an operation is one card ' +
      'rather than eleven boxes.',
  },
  er: {
    title: 'ER',
    body:
      'The schemas of one contract as entity boxes, with every `$ref` between them drawn. ' +
      'API entities — not database tables, which are the DB layer.',
  },
  reader: {
    title: 'Reader',
    body:
      'The YAML itself, syntax highlighted, with every `$ref` and every permission string ' +
      'clickable. Unresolved refs are underlined in red.',
  },
  screen: {
    title: 'Screen',
    body:
      'One screen: its wireframe, its regions and components, the four states it must handle, ' +
      'every operation it calls, and where it can be reached from.',
  },
  journey: {
    title: 'Journey',
    body:
      'One job a person came to do, traced across screens and the operations each step calls — ' +
      'with the branches, because a flow with only a happy path describes a demo.',
  },
  apps: {
    title: 'Apps',
    body:
      'What actually gets built: the app manifests, their routes, the contracts each consumes, ' +
      'and the platform wireframes.',
  },
  states: {
    title: 'States',
    body:
      'The legal moves between the states of one entity. The contracts declare what states ' +
      'exist; nothing but this says which transitions are allowed.',
  },
  events: {
    title: 'Events',
    body:
      'What crosses `platform.outbox`: who publishes each fact, who consumes it, what the ' +
      'payload is, and what happens on a redelivery.',
  },
  data: {
    title: 'Data',
    body:
      'The database. Zoomed out, the schemas and how they reference each other; drilled in, ' +
      'one schema’s tables with every column. Green exists in SQL, blue is still only planned.',
  },
  migrations: {
    title: 'Migrations',
    body: 'The versioned SQL in `backend/` — what each file creates, and the prose beside it.',
  },
  routing: {
    title: 'Routing',
    body: 'ADR-0016 made visible: every operation split across primary-write, primary-read, replica and analytical.',
  },
  lineage: {
    title: 'Lineage',
    body:
      'Which tables each operation actually touches, plus its service and stored procedure — the ' +
      'join between the Contracts layer and the DB layer, which nothing else here can make. ' +
      '**{resolved} of {operations} resolve**, across {tables} tables; the rest return a computed ' +
      'projection and correctly resolve to none.',
  },
  waves: {
    title: 'Waves',
    body:
      'Delivery sequencing. All {screens} screens across {waves} waves and {platforms} platforms, ' +
      'with the **{screensNoOperation} that name no operation** marked — a screen somebody can ' +
      'draw and nobody can build.',
  },
  decisions: {
    title: 'Decisions',
    body:
      'The ADRs, the registers, and the authorisation spec **executed rather than listed** — ' +
      'each permission vector resolved against the rule, because a failing vector is a build failure.',
  },
  audit: {
    title: 'Audit',
    body:
      'Everything wrong with **this layer**, from resolving the files rather than reading them. ' +
      'The badge counts errors. Click a finding to open what it is about.',
  },
};

export const layerOf = (key) => LAYERS.find((l) => l.key === key) ?? LAYERS[1];
export const VIEWS = [
  'uiux-screens', 'uiux-boards', 'uiux-platforms',
  'graph', 'structure', 'er', 'lineage', 'journey', 'screen', 'apps', 'waves',
  'states', 'events', 'data', 'migrations', 'routing', 'reader', 'decisions', 'audit',
  'timeline', 'supersession', 'register', 'decision',
  'services-graph', 'er-services', 'hld', 'service', 'deploy', 'context',
  'overview', 'hierarchy', 'contracts-hld', 'lifecycles-hld', 'platform-lld',
];

// ── state ────────────────────────────────────────────────────────────
export const state = {
  index: null,
  nodesById: new Map(),
  incoming: new Map(), // node id -> edges pointing at it
  outgoing: new Map(), // node id -> edges leaving it
  byFile: new Map(), // file path -> nodes defined in it
  selectedId: null,
  layer: 'contracts',
  mode: 'graph',
  structureFile: null, // file currently diagrammed
  treeCache: new Map(),
  detailLoaded: new Set(), // contracts whose held-back fields have been merged in
  erScope: null,
  journeyId: null,
  journeys: null,
  backend: null,
  domain: null,
  lineage: null, // operation -> tables, and screen -> everything
  tooltips: null, // the delivery's own hover text, 340 entries
  decisions: null, // the ADRs, the registers and the permission vectors
  diagrams: null,  // the service decomposition: what ships together
  serviceKey: null, // the service the Service view is showing
  platformKey: null,   // which of the fifteen the Platform view is showing
  // One platform design at a time, fetched on demand and kept. 15 files inlined
  // in the payload would be 15 nobody asked for; re-fetching one every time the
  // select moves back and forth would be a request per glance.
  platformDetail: null,
  serviceErScope: 'all', // which tier the services ER is showing
  // Off to open on. See renderServiceEr: with reads on, sixteen services depend
  // on so nearly all of each other that the layout has nothing to arrange and
  // stacks them in one column.
  serviceErReads: false, // whether it draws read dependencies as well as writes
  lineageScope: 'operations',
  lineageLayout: 'map',
  lineageFilter: '',
  lineageUnresolved: true,
  decisionsScope: 'adrs',
  decisionsFilter: '',
  adrId: null,
  timelineScope: 'all',
  timelineFilter: '',
  supersessionAll: false,
  registerId: 'conflict-status', // which register is on screen
  registerState: '',             // OPEN, CLOSED, … or '' for every row
  registerFilter: '',
  wavesUnbuilt: true,
  wavesOffline: false,
  machineId: null, // state model on screen
  stateName: null, // state selected within it
  eventId: null, // event opened in the events view, or null for the catalogue
  // Which reading of a view that offers more than one. The galaxy views sit
  // on a fixed dark field and answer a different question from the list or
  // the boxes beside them, so which one is showing is worth remembering.
  // Every galaxy view opens on its map. The list, the card grid and the box
  // diagram all answer "what is in this" one row at a time; the map answers it
  // in one picture, and that is what a view should open on.
  eventsLayout: 'galaxy',
  galaxyMode: '3d', // 3d | 2d — shared by every galaxy, so the choice sticks
  screenId: null,
  boardId: null, // a UI/UX board opened in place of a screen
  tableName: null,
  dataModule: null,
  dataLayout: 'galaxy',
  appsLayout: 'galaxy',
  dataRows: true,
  // The lineage filter — an anchor is where a table's own outbound keys stop,
  // so "anchored on scope_node" crosses every schema and is not a scope.
  dataAnchor: null,
  dataAnchorOnly: false,
  // each layer groups its sidebar by something different, so this is per layer
  groupBy: {
    frontend: 'platforms', contracts: 'contracts', domain: 'entities',
    backend: 'modules', decisions: 'decisions', services: 'tiers',
  },
  sideFilter: '',
  graphScope: 'spine',
  typeFilter: new Set(['operation', 'schema']),
  auditFilter: 'all',
  expandedFiles: new Set(),
  fileCache: new Map(),
  drawer: null, // 'left' | 'right' | null — only meaningful below the phone breakpoint
};

// ── the numbers the prose is allowed to quote ────────────────────────
//
// Read off the payload at hover, never typed into a sentence. See the note in
// tips.js for what this replaced and why it kept being wrong.
//
// Everything is optional-chained and every miss returns `undefined`, which
// leaves the `{token}` visible: a tip opened before its layer has loaded says
// `{operations}` rather than a confident zero.
setFactProvider(() => {
  const lineage = state.lineage?.stats;
  const journeys = state.journeys?.stats;
  const screens = lineage?.screens ?? journeys?.screens;
  const withOps = lineage?.screensWithOperations;

  return {
    operations: lineage?.operations,
    resolved: lineage?.resolved,
    unresolved: lineage?.unresolved,
    services: lineage?.services,
    tables: lineage?.tablesTouched,
    storedProcedures: lineage?.storedProcedures,
    screens,
    platforms: journeys?.platforms,
    waves: journeys?.waves ?? lineage?.waves,
    // The figure the Waves view exists to show: drawable, unbuildable.
    screensNoOperation:
      screens !== undefined && withOps !== undefined ? screens - withOps : undefined,
    adrs: state.decisions?.adrs?.length,
  };
});

export const groupBy = () => state.groupBy[state.layer];

// ── drawers ──────────────────────────────────────────────────────────
// On a phone both rails are off-canvas. The state is one field; CSS does the
// animation off body.dataset, so nothing here measures or positions anything.
export function setDrawer(next) {
  state.drawer = next;
  if (next) document.body.dataset.drawer = next;
  else delete document.body.dataset.drawer;
  $('drawer-left-toggle').setAttribute('aria-expanded', String(next === 'left'));
  $('drawer-right-toggle').setAttribute('aria-expanded', String(next === 'right'));
}

/**
 * The links pane is a reverse index of a selection. Before there is one — and
 * on the Decisions layer, which never fills it — the toggle would open an
 * empty drawer, so it is not offered. Read off the pane rather than a list of
 * views, so a view that starts filling it needs no change here.
 */
export function syncLinksToggle() {
  const pane = $('links-pane');
  const filled = state.layer !== 'decisions'
    && [...pane.children].some((child) => !child.classList.contains('pane-empty'));
  $('drawer-right-toggle').hidden = !filled;
  if (!filled && state.drawer === 'right') setDrawer(null);
}

export const $ = (id) => document.getElementById(id);
export const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  // A node passed here used to be stringified into "[object HTMLSpanElement]"
  // and rendered as that, in the page, where a reader would see it. Append it
  // instead, which is plainly what the caller meant.
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

export const TYPE_LABEL = {
  file: 'contract',
  operation: 'operation',
  schema: 'schema',
  param: 'parameter',
  response: 'response',
  requestBody: 'request body',
  securityScheme: 'security scheme',
  permission: 'permission',
  // The kinds search can find that are not contract nodes. Without these a
  // result's badge fell back to the raw key, so a state model was labelled
  // `machine` — the app's internal word for it, not the package's.
  screen: 'screen',
  flow: 'journey',
  // Both spellings, because the app and the package disagree and each is right
  // in its own place: the hash prefix is `machine:`, which is what
  // `currentSideId` has always emitted, and the search entry's kind is `state`,
  // which is what `states/` is called. Labelling only one left the other
  // falling through to the raw key, so a state model's badge read `state`.
  machine: 'state model',
  state: 'state model',
  event: 'event',
  adr: 'decision',
  table: 'table',
  board: 'board',
  platform: 'platform',
};

export const escapeHtml = (s) =>
  s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/**
 * The `notes` fields in states/ and events/ are prose with **bold** and `code`
 * in it, and the bold is always the sentence that matters — "**held → refunded
 * is not a transition.**". Escaped first, so only these two ever become markup.
 */
// ── explaining things ────────────────────────────────────────────────
// Two sources, and the delivery's own words always win over the viewer's.

/**
 * A component kind, region or pattern, explained from `screens/_components.yaml`
 * — the file that exists precisely so the vocabulary is shared and reviewed. A
 * kind that is not in there is a finding, so that is what the tip says.
 */
export function vocabularyTip(element, name) {
  const entry = state.journeys?.vocabulary?.[name];
  if (!entry) {
    return tip(element, name,
      `Not in the shared component library. A \`kind\` used on a screen must exist in ` +
      `screens/_components.yaml — free-text names are how one product ends up with four date pickers.`);
  }
  // 14 of the 46 entries are primitives the library describes only by naming —
  // `textField`, `toggle`, `primaryButton`. Saying so is better than an empty
  // panel, and the states it must handle are useful on their own.
  const described = [entry.description, entry.notes].filter(Boolean).join('\n\n');
  return tip(
    element,
    `${entry.id} — ${entry.group}`,
    described ||
      'In the shared component library, which declares the states it must handle but no ' +
      'description — one of the primitives taken as self-evident.',
    entry.states.length ? `must handle: ${entry.states.join(', ')}` : null
  );
}

/**
 * The delivery's own hover text, from `handoff/tooltips.json` — 340 entries
 * across nine categories, generated from the contracts, the schema reference and
 * the ADRs.
 *
 * This is the half a glossary cannot hold. `GLOSSARY` explains what a *kind* of
 * thing is — what "ambient" means, what a spine contract is. This explains the
 * individual thing: what `platform.outbox` is for, what `catalogue` covers, what
 * ADR-0013 decided. So the two compose, and where both have something the
 * delivery's own words win, for the same reason a component description does.
 *
 * `extra` carries the metadata that shipped alongside the tip — column counts,
 * operation counts, whether a platform is offline-capable — because the file
 * went to the trouble of including it and it is exactly what you want on the
 * same card.
 */
export function deliveryTip(element, category, key, { fallback = null } = {}) {
  const entry = state.tooltips?.entries?.[category]?.[key];
  // 202 of the 230 table tips say only "Derived from access.AccessPoint." — where
  // the row came from, which the viewer already shows, rather than why the thing
  // exists, which it cannot. The delivery's own README calls that "the same
  // failure wearing text", so a caller with something better to say wins here.
  if (!entry?.tip || (entry.restated && fallback)) {
    if (fallback) return tip(element, fallback.title, fallback.body, fallback.extra);
    return element;
  }
  const facts = [];
  const note = (label, value) => {
    if (value === undefined || value === null || value === '') return;
    facts.push(typeof value === 'boolean' ? (value ? label : null) : `${label} ${value}`);
  };
  note('columns', entry.columns);
  note('tables', entry.tables);
  note('operations', entry.operations);
  note('screens', entry.screens);
  note('steps', entry.steps);
  note('branches', entry.branches);
  note('tier', entry.tier);
  note('offline-capable', entry.offline);
  const title = entry.title ?? entry.name ?? entry.short ?? key;
  return tip(element, title, entry.tip, facts.filter(Boolean).join(' · ') || null);
}

/** A permission, explained from the vocabulary in `shared/permissions.yaml`. */
export function permissionTip(element, name) {
  const node = state.nodesById?.get(`perm:${name}`);
  if (node && !node.declared) {
    return tip(element, name,
      `**No contract declares this permission.** It is used here but is not in the enum in ` +
      `shared/permissions.yaml, which is the single source for backend authz, frontend ` +
      `navigation and AI scoping — so nothing will grant it.`);
  }
  return tip(
    element,
    name,
    `A permission from the single enum in **shared/permissions.yaml** — the one source used for ` +
    `backend authorisation, frontend navigation and AI scoping. Whoever holds it can do this; ` +
    `whoever does not never sees the control.`,
    node?.useCount ? `used by ${node.useCount} operation${node.useCount === 1 ? '' : 's'}` : null
  );
}

export const inlineMarkdown = (text) =>
  escapeHtml(String(text ?? ''))
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');


/**
 * The dot-and-label key under a diagram. Five layers draw one, so it lives
 * here rather than in whichever layer happened to need it first.
 */
/**
 * A palette token, resolved to a colour string.
 *
 * The legends, tree dots and canvas fills used to name their colours as literal
 * hexes, which meant every one of them was a dark-theme value that stayed a
 * dark-theme value on a white page. They name a token now. Inline styles could
 * have taken `var(--ok)` directly, but a canvas cannot — `fillStyle` wants a
 * real colour — so both go through here and get the same answer.
 *
 * Read live rather than cached: the theme toggle repaints everything that uses
 * this, and a lookup on the root element is cheap next to the repaint itself.
 */
export const hue = (token) =>
  getComputedStyle(document.documentElement).getPropertyValue('--' + token).trim() || '#8b8b93';

/**
 * A token at some transparency, for a canvas.
 *
 * `ctx.strokeStyle` takes a CSS colour string but nothing computed, so a
 * renderer that wants "the accent at 50%" cannot write color-mix() and had to
 * write the rgba out by hand — which is how four canvases ended up holding a
 * private copy of a colour the palette had already moved on from. Accepts the
 * #rgb and #rrggbb the tokens are written in, and passes anything else through
 * so a token that is already rgba() still works.
 */
export function alpha(color, a) {
  const hex = String(color).trim();
  const m = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(hex);
  if (!m) return hex;
  const h = m[1].length === 3 ? m[1].replace(/./g, (c) => c + c) : m[1];
  const n = parseInt(h, 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${a})`;
}

/**
 * `inlineMarkdown` plus links, which the prose in these files uses constantly
 * and which were rendering as raw `[ADR-0014](0014-cell-per-region.md)`.
 *
 * A link to a sibling ADR becomes a real link into the decisions view, but only
 * where something is listening for one — `adrLinks` is off in the reader, which
 * has no such handler and would otherwise show a dead link wearing a live one's
 * clothes. Anything else keeps its text and drops the URL, for the same reason.
 */
export function docMarkdown(text, { adrLinks = true } = {}) {
  // Italics after inlineMarkdown has taken the double asterisks, so a single
  // `*` is unambiguous by the time this runs — `*Cell = Tenant x Region*` was
  // rendering with its asterisks showing.
  const marked = inlineMarkdown(text).replace(/\*([^*\n]+)\*/g, '<i>$1</i>');
  return marked.replace(/\[([^\]]*)\]\(([^)]*)\)/g, (whole, label, href) => {
    if (!adrLinks) return label;
    const adr = /(\d{4})-/.exec(href) ?? /ADR-(\d{3,4})/.exec(label);
    if (adr) return `<a class="md-adr" data-adr="${adr[1].padStart(4, '0')}" href="#">${label}</a>`;
    return label;
  });
}

const TABLE_ROW = /^\s*\|(.*)\|\s*$/;
const TABLE_RULE = /^\s*\|[\s:|-]+\|\s*$/;

/** `| a | b |` → ['a', 'b'], with the empty edges the outer pipes leave. */
const cellsOf = (line) =>
  TABLE_ROW.exec(line)[1].split('|').map((c) => c.trim());

/**
 * Enough markdown for the prose in a contract or an ADR, and no more.
 *
 * Headings, paragraphs, lists, block quotes, fenced code, rules and tables —
 * which is what these files use. Deliberately not a markdown library: that
 * would be the first dependency the frontend takes, for six kinds of block.
 *
 * Tables are here because every contract's header is one. Without them the
 * reader was showing `| |---|---| | **Tier** | spine |` as a run-on sentence in
 * the middle of the description, which is the single worst thing on that page.
 */
export function markdownBlock(text, { adrLinks = true } = {}) {
  const host = el('div', 'md');
  const lines = String(text).split(/\r?\n/);
  const inline = (t) => docMarkdown(t, { adrLinks });
  let list = null;
  let para = [];

  const closeList = () => { if (list) { host.append(list); list = null; } };
  const closePara = () => {
    if (!para.length) return;
    const p = el('p', 'md-p');
    p.innerHTML = inline(para.join(' '));
    host.append(p);
    para = [];
  };
  const close = () => { closeList(); closePara(); };

  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];

    if (/^```/.test(raw)) {
      close();
      const fence = el('pre', 'md-code');
      i += 1;
      while (i < lines.length && !/^```/.test(lines[i])) {
        fence.textContent += `${lines[i]}\n`;
        i += 1;
      }
      host.append(fence);
      continue;
    }

    // A table is a row followed by the dashed rule; anything else starting with
    // a pipe is just a line that starts with a pipe.
    if (TABLE_ROW.test(raw) && i + 1 < lines.length && TABLE_RULE.test(lines[i + 1])) {
      close();
      const header = cellsOf(raw);
      const table = el('table', 'md-table');
      // Contract headers open with `| | |` — an empty header row that exists to
      // satisfy the syntax. Rendering it leaves a blank band above the table,
      // so a header with nothing in it is dropped and the table is all body.
      if (header.some((c) => c)) {
        const thead = el('thead');
        const tr = el('tr');
        for (const cell of header) {
          const th = el('th');
          th.innerHTML = inline(cell);
          tr.append(th);
        }
        thead.append(tr);
        table.append(thead);
      }
      const tbody = el('tbody');
      i += 2;
      while (i < lines.length && TABLE_ROW.test(lines[i])) {
        const tr = el('tr');
        for (const cell of cellsOf(lines[i])) {
          const td = el('td');
          td.innerHTML = inline(cell);
          tr.append(td);
        }
        tbody.append(tr);
        i += 1;
      }
      i -= 1;
      table.append(tbody);
      const scroller = el('div', 'md-table-wrap');
      scroller.append(table);
      host.append(scroller);
      continue;
    }

    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(raw)) {
      close();
      host.append(el('hr', 'md-rule'));
      continue;
    }

    const head = /^(#{1,6})\s+(.*)$/.exec(raw);
    if (head) {
      close();
      const h = el(`h${Math.min(head[1].length + 1, 6)}`, `md-head md-h${head[1].length}`);
      h.innerHTML = inline(head[2]);
      host.append(h);
      continue;
    }

    const item = /^\s*[-*+]\s+(.*)$/.exec(raw);
    if (item) {
      closePara();
      if (!list) list = el('ul', 'md-list');
      const li = el('li');
      li.innerHTML = inline(item[1]);
      list.append(li);
      continue;
    }

    const quote = /^>\s?(.*)$/.exec(raw);
    if (quote) {
      close();
      const q = el('blockquote', 'md-quote');
      q.innerHTML = inline(quote[1]);
      host.append(q);
      continue;
    }

    if (!raw.trim()) { close(); continue; }
    closeList();
    // A paragraph runs until a blank line. These files are hard-wrapped at
    // about 100 columns, so treating each line as its own paragraph broke every
    // sentence in the middle — "…which are history rather than" and "decision."
    // as two paragraphs.
    para.push(raw.trim());
  }
  close();
  return host;
}

export function renderBoxLegend(container, entries, note) {
  container.innerHTML = '';
  for (const [color, label] of entries) {
    const row = el('div', 'legend-row');
    const dot = el('span', 'legend-dot');
    dot.style.background = color;
    row.append(dot, el('span', null, label));
    container.append(row);
  }
  container.append(el('div', 'legend-row', note));
}
