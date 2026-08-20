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
import { tip, GLOSSARY } from './tips.js';

export const LAYERS = [
  {
    key: 'frontend',
    label: 'Frontend',
    hint: 'screens, journeys and the apps that implement them',
    tip:
      'What a person sees. **screens/** defines each one, **flows/** traces a job across ' +
      'several, **frontend/** says which app builds them, and **wireframes/** draws them. ' +
      'Every operation a screen names is resolved against the contracts.',
    modes: [
      ['screen', 'Screen'], ['journey', 'Journey'], ['apps', 'Apps'],
      ['waves', 'Waves'], ['audit', 'Audit'],
    ],
    groups: [['platforms', 'Platforms'], ['modules', 'Modules'], ['waves', 'Waves']],
  },
  {
    key: 'contracts',
    label: 'Contracts',
    hint: 'the API — the join between the other two layers',
    tip:
      'The 24 OpenAPI contracts. **The API is the join between every other layer**, so this ' +
      'sits in the middle and everything else is drawn by resolving against it. Hand-authored; ' +
      'servers and clients are generated from it, never the reverse.',
    modes: [
      ['graph', 'Graph'], ['structure', 'Structure'], ['er', 'ER'],
      ['lineage', 'Lineage'], ['reader', 'Reader'], ['audit', 'Audit'],
    ],
    groups: [['contracts', 'Contracts'], ['modules', 'Modules'], ['platforms', 'Platforms']],
  },
  {
    key: 'domain',
    label: 'Domain',
    hint: 'states/ and events/ — the legal moves, and what crosses the outbox',
    tip:
      'The two artefacts that check each other. **states/** says which moves between statuses ' +
      'are legal — 38 enums declare what states exist and none says which transitions are ' +
      'allowed. **events/** says what goes through the outbox when one happens.',
    modes: [['states', 'States'], ['events', 'Events'], ['audit', 'Audit']],
    groups: [['entities', 'Entities'], ['contexts', 'Contexts']],
  },
  {
    key: 'backend',
    label: 'Backend',
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
    modes: [
      ['timeline', 'Timeline'], ['supersession', 'Supersession'],
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
      'API entities — not database tables, which are the Backend layer.',
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
      'join between the Contracts layer and the Backend layer, which nothing else here can make. ' +
      '**336 of 654 resolve to a table**; the rest mostly return a computed projection and ' +
      'correctly resolve to none.',
  },
  waves: {
    title: 'Waves',
    body:
      'Delivery sequencing. All 347 screens across three waves and twelve platforms, with the ' +
      '**192 that name no operation** marked — a screen somebody can draw and nobody can build.',
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
  'graph', 'structure', 'er', 'lineage', 'journey', 'screen', 'apps', 'waves',
  'states', 'events', 'data', 'migrations', 'routing', 'reader', 'decisions', 'audit',
  'timeline', 'supersession', 'register', 'decision',
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
  lineageScope: 'operations',
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
  screenId: null,
  boardId: null, // a UI/UX board opened in place of a screen
  tableName: null,
  dataModule: null,
  dataRows: true,
  // The lineage filter — an anchor is where a table's own outbound keys stop,
  // so "anchored on scope_node" crosses every schema and is not a scope.
  dataAnchor: null,
  dataAnchorOnly: false,
  // each layer groups its sidebar by something different, so this is per layer
  groupBy: {
    frontend: 'platforms', contracts: 'contracts', domain: 'entities',
    backend: 'modules', decisions: 'decisions',
  },
  sideFilter: '',
  graphScope: 'spine',
  typeFilter: new Set(['operation', 'schema']),
  auditFilter: 'all',
  expandedFiles: new Set(),
  fileCache: new Map(),
  drawer: null, // 'left' | 'right' | null — only meaningful below the phone breakpoint
};

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
