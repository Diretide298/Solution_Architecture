import { Graph, colorForNode } from './graph.js';
import { StructureTree, kindColor } from './structure.js';
import { BoxDiagram } from './boxdiagram.js';

// ── state ────────────────────────────────────────────────────────────
const state = {
  index: null,
  nodesById: new Map(),
  incoming: new Map(), // node id -> edges pointing at it
  outgoing: new Map(), // node id -> edges leaving it
  byFile: new Map(), // file path -> nodes defined in it
  selectedId: null,
  mode: 'graph',
  structureFile: null, // file currently diagrammed
  treeCache: new Map(),
  erScope: null,
  journeyId: null,
  journeys: null,
  groupBy: 'contracts',
  sideFilter: '',
  graphScope: 'files',
  typeFilter: new Set(['operation', 'schema']),
  auditFilter: 'all',
  expandedFiles: new Set(),
  fileCache: new Map(),
};

const $ = (id) => document.getElementById(id);
const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
};

const TYPE_LABEL = {
  file: 'contract',
  operation: 'operation',
  schema: 'schema',
  param: 'parameter',
  response: 'response',
  requestBody: 'request body',
  securityScheme: 'security scheme',
  permission: 'permission',
};

const escapeHtml = (s) =>
  s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

// ── boot ─────────────────────────────────────────────────────────────
let graph;
let tree;
let er;

async function boot() {
  const openRow = (row) => {
    if (row.refTarget && state.nodesById.has(row.refTarget)) select(row.refTarget);
  };
  er = new BoxDiagram($('er-canvas'), {
    onSelect: (node) => select(node.id),
    onRow: openRow,
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
    if (id && id !== state.selectedId && state.nodesById.has(id)) select(id);
  });

  // handy for debugging layouts from the console
  window.__graph = graph;
  window.__tree = tree;
  window.__er = er;
  await loadIndex();
  bindUI();
  connectLiveReload();

  // restore from the url so links into a specific node survive a refresh
  const fromHash = decodeURIComponent(location.hash.slice(1));
  if (fromHash && state.nodesById.has(fromHash)) {
    select(fromHash);
    setMode(state.mode === 'graph' ? 'reader' : state.mode);
  } else {
    setMode('graph');
  }
}

async function loadIndex() {
  const res = await fetch('/api/index');
  const index = await res.json();
  state.index = index;

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

  renderTree();
  renderTypeFilters();
  renderSideNote();
  renderAudit();
  renderGraph();
  renderER();

  const errors = index.stats.errors;
  const badge = $('audit-count');
  badge.textContent = errors;
  badge.classList.toggle('show', errors > 0);
  $('file-count').textContent = `${index.stats.files} files · ${index.stats.operations} ops`;
}

// ── mode switching ───────────────────────────────────────────────────
function setMode(mode) {
  state.mode = mode;
  for (const view of ['graph', 'structure', 'er', 'journey', 'reader', 'audit']) {
    $(`view-${view}`).hidden = view !== mode;
  }
  for (const button of $('modes').querySelectorAll('.mode')) {
    button.classList.toggle('active', button.dataset.mode === mode);
  }
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

  if (mode === 'journey') renderJourney();
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

function renderTree() {
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
      shownFiles += 1;
      const row = el('div', 'tree-file');
      row.dataset.id = file.id;
      row.append(el('span', 'tree-file-name', file.name));

      const children = state.byFile.get(file.file) ?? [];
      const visible = children.filter((c) => state.typeFilter.has(c.type));
      row.append(el('span', 'tree-file-count', String(visible.length)));

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

  const label = state.groupBy === 'contracts' ? 'tiers'
    : state.groupBy === 'modules' ? 'modules' : 'platforms';
  $('file-count').textContent = `${groups.size} ${label} · ${shownFiles} listed`;
  markTreeSelection();
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

function markTreeSelection() {
  for (const row of $('tree').querySelectorAll('[data-id]')) {
    row.classList.toggle('selected', row.dataset.id === state.selectedId);
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

  if (state.graphScope === 'files') {
    viewNodes = nodes.filter((n) => n.type === 'file');
    viewEdges = fileEdges;
    hint = 'Contracts, sized by how much links to them';
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
    const keep = new Set([anchor]);
    let frontier = new Set([anchor]);
    for (let hop = 0; hop < 2; hop++) {
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
    viewEdges = edges.filter((e) => keep.has(e.source) && keep.has(e.target) && e.kind !== 'contains');
    hint = `${viewNodes.length} nodes within 2 hops of ${state.nodesById.get(anchor)?.name ?? ''}`;
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

  if (state.groupBy === 'contracts') {
    for (const key of ['spine', 'satellite', 'shared']) groups.set(key, []);
    for (const file of files) add(file.tier ?? file.group, file);
  } else if (state.groupBy === 'modules') {
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
  if (state.groupBy === 'modules') {
    const match = key.match(/^(\d+)\s*[—-]\s*(.*)$/);
    return match ? { code: match[1], label: match[2] } : { code: '', label: key };
  }
  if (state.groupBy === 'platforms') {
    const match = key.match(/^(P\d+)\s+(.*)$/);
    return match ? { code: match[1], label: match[2] } : { code: '', label: key };
  }
  return { code: '', label: key };
}

function groupColor(key, files) {
  if (state.groupBy === 'contracts') return colorForNode({ group: key, type: 'file' }, 'group');
  const tier = files[0]?.tier ?? files[0]?.group;
  return colorForNode({ group: tier, type: 'file' }, 'group');
}

/** The platform grouping is contract-level, which the pane should not imply otherwise. */
function renderSideNote() {
  const note = $('side-note');
  if (state.groupBy !== 'platforms') { note.hidden = true; return; }
  const contracts = state.index.nodes.filter((n) => n.type === 'file');
  const declared = contracts.filter((n) => n.platforms?.length).length;
  note.innerHTML =
    `From <b>x-ticvai-platforms</b> (${declared}/${contracts.length} contracts). Declared per ` +
    `contract, so a contract appears under every platform it names — this is reach, not ` +
    `per-endpoint ownership.`;
  note.hidden = false;
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
    `${s.flows} flows · ${s.steps} steps · ${s.branches} branches · ` +
    `${s.screens} screens · ${s.operationsCovered} operations covered`;

  body.innerHTML = '';

  // ---- header ----------------------------------------------------------
  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', `${flow.id} — ${flow.name}`));

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

  if (flow.openQuestions.length) {
    const box = el('div', 'journey-questions');
    box.append(el('b', null, 'Open questions'));
    const list = el('ul');
    for (const question of flow.openQuestions) list.append(el('li', null, question));
    box.append(list);
    body.append(box);
  }
}

function renderBoxLegend(container, entries, note) {
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

// ── right pane: links ────────────────────────────────────────────────
function renderLinksPane(node) {
  const pane = $('links-pane');
  pane.innerHTML = '';

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

// ── reader ───────────────────────────────────────────────────────────
async function renderReader(node, { scroll = true } = {}) {
  $('reader-empty').hidden = true;
  $('reader-body').hidden = false;

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
function renderAudit() {
  const { problems, stats } = state.index;

  $('audit-summary').textContent =
    `${stats.operations} operations across ${stats.files} contracts · ${stats.links} resolved links · ` +
    `${stats.errors} error${stats.errors === 1 ? '' : 's'}, ${problems.filter((p) => p.severity === 'warning').length} warnings, ` +
    `${problems.filter((p) => p.severity === 'info').length} notes`;

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

  source.onopen = () => dot.classList.remove('stale');
  source.onerror = () => dot.classList.add('stale');
  source.onmessage = async (event) => {
    const data = JSON.parse(event.data);
    if (data.type !== 'reload') return;

    state.fileCache.clear();
    state.treeCache.clear();
    state.journeys = null; // flows and screens are watched too
    state.structureFile = null; // force the diagram to rebuild from fresh YAML
    const keepSelection = state.selectedId;
    await loadIndex();

    dot.classList.remove('pulse');
    void dot.offsetWidth; // restart the animation
    dot.classList.add('pulse');
    toast(`Reindexed after ${data.file} changed`);

    if (keepSelection && state.nodesById.has(keepSelection)) select(keepSelection, { scroll: false });
  };
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
function bindUI() {
  for (const button of $('modes').querySelectorAll('.mode')) {
    button.onclick = () => setMode(button.dataset.mode);
  }

  for (const button of $('graph-scope').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.scope === state.graphScope);
    button.onclick = () => {
      state.graphScope = button.dataset.scope;
      for (const other of $('graph-scope').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderGraph();
      setMode('graph');
    };
  }

  $('graph-labels').onchange = (e) => { graph.showLabels = e.target.checked; graph.draw(); };
  $('graph-recenter').onclick = () => graph.recenter();

  for (const button of $('group-by').querySelectorAll('button')) {
    button.classList.toggle('active', button.dataset.group === state.groupBy);
    button.onclick = () => {
      state.groupBy = button.dataset.group;
      for (const other of $('group-by').querySelectorAll('button')) {
        other.classList.toggle('active', other === button);
      }
      renderSideNote();
      renderTree();
    };
  }
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

    if (e.target.tagName === 'INPUT') return;
    if (e.key === 'm') {
      // cycle how the left pane groups: contracts → modules → platforms
      const order = ['contracts', 'modules', 'platforms'];
      state.groupBy = order[(order.indexOf(state.groupBy) + 1) % order.length];
      for (const other of $('group-by').querySelectorAll('button')) {
        other.classList.toggle('active', other.dataset.group === state.groupBy);
      }
      renderSideNote();
      renderTree();
    } else if (e.key === 'g') setMode('graph');
    else if (e.key === 's') setMode('structure');
    else if (e.key === 'e') setMode('er');
    else if (e.key === 'j') setMode('journey');
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
