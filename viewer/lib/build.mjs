/**
 * How the package was built, in the order it is built.
 *
 * **`tools/refresh.sh` is the only place that order is written down.** Every
 * other layer shows a derived artefact as it stands, and none of them shows
 * that the lineage has to exist before the schema can be derived from it, or
 * that the id register has to be current before a screen check will pass. The
 * script says so — in its order, and in the comments above each call — so this
 * reads the script rather than restating it.
 *
 * Two things here are authored, and they are marked where they sit: which
 * tools make up a named step, and which files that step writes. A write cannot
 * be told from a read by looking at a Python file without running it, and a
 * guess would draw arrows that are wrong. Everything else is read: the order,
 * the note above each call, each tool's own docstring, whether each file exists
 * and how big it is, the figure on each card, and which earlier step a later
 * one reads.
 */

import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';

const SCRIPT = 'tools/refresh.sh';

const ACTS = [
  { key: 'data', label: 'Data', blurb: 'What the contracts store, and where it is stored.' },
  { key: 'scale', label: 'Scale', blurb: 'What a flash sale runs, and how big each piece has to be.' },
  { key: 'design', label: 'Design', blurb: 'The apps, the board panels and the diagrams, drawn from the data.' },
  { key: 'screens', label: 'Screens', blurb: 'Every screen wired, drawn, numbered and linked to what it calls.' },
  { key: 'backlog', label: 'Backlog', blurb: 'What the contracts still owe, and how it groups.' },
  { key: 'platform', label: 'Platform', blurb: 'Which surface ships where, and who it is for.' },
  { key: 'publish', label: 'Publish', blurb: 'The figures every document quotes, and the copy each repository carries.' },
];

/**
 * The named steps. **Authored**: the grouping of tools into a step and the
 * files a step writes. The position of each step is not — it is the line its
 * first tool is called on, so reordering the script reorders this.
 *
 * `figure` describes the one number worth putting on the card:
 *   size  — entries in the array or object at `path` (the whole file if none)
 *   value — the number at `path`
 *   files — files matching `glob`
 *   match — occurrences of `pattern` across `glob` (or `file`)
 */
const STAGES = [
  {
    key: 'lineage', act: 'data', label: 'Lineage',
    tools: ['derive-lineage'],
    writes: ['handoff/api-data-lineage.json'],
    figure: { of: 'size', file: 'handoff/api-data-lineage.json', unit: 'operations traced to their tables' },
    open: ['contracts', 'lineage'],
  },
  {
    key: 'schema', act: 'data', label: 'Schema',
    tools: ['derive-schema'],
    writes: ['handoff/schema-reference.json'],
    figure: { of: 'size', file: 'handoff/schema-reference.json', path: 'storage', unit: 'tables placed in a store' },
    open: ['backend', 'data'],
  },
  {
    key: 'relationships', act: 'data', label: 'Relationships',
    tools: ['derive-relationships'],
    writes: ['handoff/relationship-graph.json'],
    figure: { of: 'size', file: 'handoff/relationship-graph.json', path: 'rels', unit: 'relationships between tables' },
    open: ['contracts', 'er'],
  },
  {
    key: 'ddl', act: 'data', label: 'DDL',
    tools: ['derive-ddl'],
    writes: ['backend/**/*.sql'],
    figure: { of: 'match', glob: 'backend/**/*.sql', pattern: 'CREATE TABLE', unit: 'CREATE TABLE statements' },
    open: ['backend', 'migrations'],
  },
  {
    key: 'burst', act: 'scale', label: 'Burst scope',
    tools: ['derive-burst-scope'],
    writes: ['handoff/burst-scope.json'],
    figure: { of: 'size', file: 'handoff/burst-scope.json', path: 'operations', unit: 'operations on the sale path' },
    open: ['cicd', 'cicd-burst'],
  },
  {
    key: 'sizing', act: 'scale', label: 'Sizing',
    tools: ['derive-sizing'],
    writes: ['handoff/sizing.json'],
    figure: { of: 'size', file: 'handoff/sizing.json', path: 'venueTiers', unit: 'venue tiers sized' },
    open: ['cicd', 'cicd-burst'],
  },
  {
    key: 'table-notes', act: 'scale', label: 'Table notes',
    tools: ['derive-table-notes'],
    writes: ['handoff/schema-reference.json'],
    figure: null,
    open: ['backend', 'data'],
  },
  {
    key: 'schema-roots', act: 'scale', label: 'Schema roots',
    tools: ['derive-schema-roots'],
    writes: ['handoff/schema-roots.md'],
    figure: { of: 'match', file: 'handoff/schema-roots.md', pattern: '^## ', flags: 'gm', unit: 'sections' },
    open: ['backend', 'data'],
  },
  {
    key: 'frontend', act: 'design', label: 'Frontend',
    tools: ['derive-frontend'],
    writes: ['frontend/*.yaml'],
    figure: { of: 'files', glob: 'frontend/*.yaml', unit: 'frontend definitions' },
    open: ['frontend', 'apps'],
  },
  {
    key: 'board-panels', act: 'design', label: 'Board-panel map',
    tools: ['derive-board-panel-map'],
    writes: ['handoff/board-panel-map.json'],
    figure: { of: 'size', file: 'handoff/board-panel-map.json', path: 'panels', unit: 'board panels mapped to operations' },
    open: ['uiux', 'uiux-boards'],
  },
  {
    key: 'diagrams', act: 'design', label: 'Diagrams',
    tools: ['derive-diagrams'],
    writes: ['diagrams/hld/*.yaml'],
    figure: { of: 'files', glob: 'diagrams/hld/*.yaml', unit: 'high-level designs' },
    open: ['services', 'overview'],
  },
  {
    key: 'workbooks', act: 'design', label: 'Both workbooks',
    tools: ['build-schema-workbook', 'build-services-workbook'],
    writes: [
      'handoff/TICVAI_Schema_Reference.xlsx',
      'handoff/TICVAI_Services_and_Data_Segregation.xlsx',
    ],
    figure: { of: 'files', glob: 'handoff/TICVAI_*.xlsx', unit: 'workbooks' },
    open: ['services', 'hld'],
  },
  {
    // The six screen-authoring tools run between the workbooks and the boards,
    // and they are this step's own groundwork: the boards draw what they fill.
    key: 'wireframes', act: 'screens', label: 'Wireframes',
    tools: [
      'derive-transitions-from-flows', 'label-launcher-edges', 'derive-entrystate-params',
      'derive-carries-from-entrystate', 'derive-components', 'derive-board-anchors',
      'derive-wireframes',
    ],
    writes: ['wireframes/*.dc.html', 'wireframes/manifest.json'],
    figure: { of: 'files', glob: 'wireframes/**/*.dc.html', unit: 'wireframe boards' },
    open: ['uiux', 'uiux-screens'],
  },
  {
    key: 'workshop-boards', act: 'screens', label: 'Workshop boards',
    tools: ['index-boards', 'derive-design-manifest', 'derive-app-roles'],
    writes: ['wireframes/board-index.json', 'wireframes/design-manifest.json', 'roles-by-app.yaml'],
    figure: { of: 'value', file: 'wireframes/board-index.json', path: 'counts.screensDrawnByEither', unit: 'screens with a drawn frame' },
    open: ['uiux', 'uiux-boards'],
  },
  {
    key: 'id-register', act: 'screens', label: 'Id register',
    tools: ['derive-id-register'],
    writes: ['screens/_id-register.yaml'],
    figure: { of: 'size', file: 'screens/_id-register.yaml', path: 'prefixes', unit: 'id prefixes with a high-water mark' },
    open: ['frontend', 'screen'],
  },
  {
    key: 'screen-links', act: 'screens', label: 'Screen-contract links',
    tools: ['link-screens-contracts', '@inline'],
    writes: ['handoff/screen-index.json'],
    figure: { of: 'size', file: 'handoff/screen-index.json', unit: 'screens indexed against operations' },
    open: ['frontend', 'screen'],
  },
  {
    key: 'backlog', act: 'backlog', label: 'Backlog',
    tools: ['build-backlog-index'],
    writes: ['docs/registers/contract-backlog.md'],
    figure: { of: 'size', file: 'handoff/contract-backlog.json', path: 'entries', unit: 'backlog entries' },
    open: ['decisions', 'register'],
  },
  {
    key: 'clusters', act: 'backlog', label: 'Clusters',
    tools: ['build-cluster-index'],
    writes: ['docs/registers/clusters.md'],
    figure: { of: 'size', file: 'handoff/backlog-clusters.json', path: 'clusters', unit: 'clusters' },
    open: ['decisions', 'register'],
  },
  {
    key: 'platform', act: 'platform', label: 'Platform',
    tools: ['derive-platform'],
    writes: ['handoff/platform-index.json', 'handoff/platform-P*.json', 'handoff/platform-P*.md'],
    figure: { of: 'size', file: 'handoff/platform-index.json', unit: 'platforms' },
    open: ['frontend', 'platform-lld'],
  },
  {
    key: 'deployment', act: 'platform', label: 'Deployment',
    tools: ['derive-platform-deployment'],
    writes: ['handoff/platform-deployment.md'],
    figure: { of: 'match', file: 'handoff/platform-deployment.md', pattern: '^\\|\\s*\\**P\\d', flags: 'gm', unit: 'platform rows' },
    open: ['services', 'deploy'],
  },
  {
    key: 'audience', act: 'platform', label: 'Audience',
    tools: ['build-audience'],
    writes: ['handoff/audience-index.json'],
    figure: { of: 'size', file: 'handoff/audience-index.json', path: 'audiences', unit: 'audiences' },
    open: ['frontend', 'apps'],
  },
  {
    key: 'overview', act: 'publish', label: 'Overview',
    tools: ['derive-overview'],
    writes: ['OVERVIEW.md'],
    figure: { of: 'size', file: 'handoff/traceability.json', path: 'rows', unit: 'traceability rows' },
    open: null,
  },
  {
    key: 'counts', act: 'publish', label: 'Counts',
    tools: ['sync-counts'],
    writes: ['README.md', 'COVERAGE.md', 'MANIFEST.md'],
    figure: { of: 'size', file: 'handoff/status.json', path: 'counts', unit: 'figures kept in step' },
    open: null,
  },
  {
    key: 'mirrors', act: 'publish', label: 'Mirrors',
    tools: ['derive-mirrors'],
    writes: ['repos/*/project-bible', 'repos/ticvai-docs'],
    figure: { of: 'files', glob: 'repos/*/project-bible', unit: 'repository mirrors' },
    open: ['cicd', 'cicd-pipeline'],
  },
];

/* ── files ────────────────────────────────────────────────────────────── */

/** A glob of the three shapes the steps use — `*`, `**` and literals — as a
 *  regular expression over forward-slashed package paths. */
function globRegex(pattern) {
  let re = '';
  for (let i = 0; i < pattern.length; i += 1) {
    const c = pattern[i];
    if (c === '*' && pattern[i + 1] === '*') {
      re += '.*';
      i += 1;
      if (pattern[i + 1] === '/') i += 1;
    } else if (c === '*') {
      re += '[^/]*';
    } else if ('.+?^${}()|[]\\'.includes(c)) {
      re += `\\${c}`;
    } else {
      re += c;
    }
  }
  return new RegExp(`^${re}$`);
}

/**
 * The files (or folders) a pattern names, with their size and age.
 *
 * Walks from the pattern's literal prefix only, and no deeper than the pattern
 * can reach — `repos/*\/project-bible` looks two levels into `repos/` and not
 * into every mirror under it.
 */
async function expand(root, pattern) {
  const facts = async (rel) => {
    const s = await stat(path.join(root, rel)).catch(() => null);
    return s ? { path: rel, bytes: s.isDirectory() ? 0 : s.size, modified: s.mtimeMs, dir: s.isDirectory() } : null;
  };
  if (!pattern.includes('*')) {
    const one = await facts(pattern);
    return one ? [one] : [];
  }
  const segs = pattern.split('/');
  const lead = [];
  for (const s of segs) {
    if (s.includes('*')) break;
    lead.push(s);
  }
  const re = globRegex(pattern);
  const reach = pattern.includes('**') ? 12 : segs.length - lead.length;
  const out = [];
  async function walk(rel, depth) {
    const entries = await readdir(path.join(root, rel), { withFileTypes: true }).catch(() => []);
    for (const entry of entries) {
      if (entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
      const child = rel ? `${rel}/${entry.name}` : entry.name;
      if (re.test(child)) {
        const f = await facts(child);
        if (f) out.push(f);
      }
      if (entry.isDirectory() && depth + 1 < reach) await walk(child, depth + 1);
    }
  }
  await walk(lead.join('/'), 0);
  return out.sort((a, b) => a.path.localeCompare(b.path));
}

const parsed = new Map();

/** JSON or YAML, parsed once per build however many steps quote it. */
async function load(root, rel) {
  if (!parsed.has(rel)) {
    parsed.set(rel, readFile(path.join(root, rel), 'utf8')
      .then((text) => (rel.endsWith('.json') ? JSON.parse(text) : yaml.load(text)))
      .catch(() => null));
  }
  return parsed.get(rel);
}

async function figureOf(root, spec) {
  if (!spec) return null;
  try {
    let value = null;
    if (spec.of === 'files') {
      value = (await expand(root, spec.glob)).length;
    } else if (spec.of === 'match') {
      const files = spec.glob ? (await expand(root, spec.glob)).map((f) => f.path) : [spec.file];
      const re = new RegExp(spec.pattern, spec.flags ?? 'g');
      value = 0;
      for (const rel of files) {
        const text = await readFile(path.join(root, rel), 'utf8').catch(() => '');
        value += (text.match(re) ?? []).length;
      }
    } else {
      const data = await load(root, spec.file);
      const at = spec.path ? spec.path.split('.').reduce((o, k) => o?.[k], data) : data;
      if (spec.of === 'value') value = typeof at === 'number' ? at : null;
      else if (Array.isArray(at)) value = at.length;
      else if (at && typeof at === 'object') value = Object.keys(at).length;
    }
    if (value == null) return null;
    return { value, unit: spec.unit, source: spec.file ?? spec.glob };
  } catch {
    return null;
  }
}

/* ── the script ───────────────────────────────────────────────────────── */

/**
 * Every tool call in the script, in order, with the comment that sits directly
 * above it. A blank line ends a comment's claim on the next call, which is how
 * the script itself separates one argument from the next.
 *
 * The one call that is not a file — the screen index, written by a heredoc — is
 * recorded as `@inline` with its body, so what it reads can be found the same
 * way as for a tool.
 */
function parseScript(text) {
  const lines = text.split(/\r?\n/);
  const calls = [];
  let checks = [];
  let comment = [];
  let heredoc = null;
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i].trim();
    if (heredoc) {
      if (line === heredoc.end) {
        heredoc = null;
      } else {
        heredoc.call.body.push(lines[i]);
      }
      continue;
    }
    if (line.startsWith('#!')) continue;
    if (line.startsWith('#')) {
      comment.push(line.replace(/^#\s?/, ''));
      continue;
    }
    if (!line) {
      comment = [];
      continue;
    }
    const inline = /^python3\s+-\s+<<\s*'?(\w+)'?/.exec(line);
    if (inline) {
      const call = { tool: '@inline', line: i + 1, note: comment.join('\n') || null, body: [] };
      calls.push(call);
      heredoc = { end: inline[1], call };
      comment = [];
      continue;
    }
    const tools = [...line.matchAll(/python3\s+"?tools\/([\w-]+)\.py/g)].map((m) => m[1]);
    if (tools.length) {
      const trailing = /\s#\s*(.+)$/.exec(line)?.[1] ?? null;
      for (const tool of tools) {
        calls.push({ tool, line: i + 1, note: comment.join('\n') || null, trailing });
      }
      comment = [];
      continue;
    }
    const loop = /^for\s+t\s+in\s+(.+?);\s*do\b/.exec(line);
    if (loop) checks = loop[1].split(/\s+/).filter(Boolean);
    comment = [];
  }
  return { calls, checks };
}

/** A Python module's docstring: the first paragraph is what the tool does, the
 *  second is usually why it had to. */
function docstringOf(src) {
  const m = /^(?:\s*#[^\n]*\n)*\s*[rRuU]?("""|''')([\s\S]*?)\1/.exec(src);
  if (!m) return { summary: null, detail: null };
  const paras = m[2].trim().split(/\n\s*\n/)
    .map((p) => p.replace(/\s*\n\s*/g, ' ').trim())
    .filter(Boolean);
  return { summary: paras[0] ?? null, detail: paras[1] ?? null };
}

const FILE_NAME = /[A-Za-z0-9_-]+\.(?:json|md|sql|xlsx|yaml)/g;
const READS_CONTRACTS = /["'/]contracts["'/]/;

async function contractsOf(root) {
  const files = await expand(root, 'contracts/**/*.yaml');
  const tierRank = { spine: 0, satellite: 1, shared: 2 };
  const out = [];
  for (const f of files) {
    const text = await readFile(path.join(root, f.path), 'utf8').catch(() => '');
    const title = /^\s{2}title:\s*(.+)$/m.exec(text)?.[1]?.trim().replace(/^['"]|['"]$/g, '') ?? null;
    out.push({
      file: f.path,
      name: path.basename(f.path, '.yaml'),
      tier: f.path.split('/').length > 2 ? f.path.split('/')[1] : null,
      title,
      operations: (text.match(/^\s+operationId:/gm) ?? []).length,
    });
  }
  return out.sort((a, b) => ((tierRank[a.tier] ?? 9) - (tierRank[b.tier] ?? 9)) || a.name.localeCompare(b.name));
}

export async function buildChronology(root) {
  parsed.clear();
  const script = await readFile(path.join(root, SCRIPT), 'utf8').catch(() => null);
  if (script == null) return { present: false, script: SCRIPT };

  const { calls, checks } = parseScript(script);
  const firstCall = new Map();
  for (const call of calls) if (!firstCall.has(call.tool)) firstCall.set(call.tool, call);

  const sources = new Map();
  const toolFacts = async (name) => {
    const call = firstCall.get(name) ?? null;
    if (name === '@inline') {
      const body = call?.body?.join('\n') ?? '';
      sources.set(name, body);
      return {
        name: 'screen index', file: `${SCRIPT}:${call?.line ?? '?'}`, inScript: Boolean(call),
        line: call?.line ?? null, lines: call?.body?.length ?? 0,
        summary: 'Writes `handoff/screen-index.json` — every screen with its route, operations, services, stores, transitions and states — inline in the script.',
        detail: null,
      };
    }
    const file = `tools/${name}.py`;
    const src = await readFile(path.join(root, file), 'utf8').catch(() => null);
    sources.set(name, src ?? '');
    return {
      name, file, exists: src != null, inScript: Boolean(call), line: call?.line ?? null,
      lines: src ? src.split('\n').length : 0,
      ...(src ? docstringOf(src) : { summary: null, detail: null }),
    };
  };

  const stages = [];
  for (const spec of STAGES) {
    const tools = [];
    for (const name of spec.tools) tools.push(await toolFacts(name));
    const lead = tools.filter((t) => t.inScript).sort((a, b) => a.line - b.line)[0] ?? null;
    const call = lead ? firstCall.get(spec.tools.find((n) => firstCall.get(n)?.line === lead.line)) : null;

    const writes = [];
    for (const pattern of spec.writes) {
      const files = await expand(root, pattern);
      writes.push({
        pattern,
        files: files.length,
        bytes: files.reduce((a, f) => a + f.bytes, 0),
        modified: files.length ? Math.max(...files.map((f) => f.modified)) : null,
        sample: files.slice(0, 3).map((f) => f.path),
      });
    }

    stages.push({
      key: spec.key,
      act: spec.act,
      label: spec.label,
      line: lead?.line ?? null,
      inScript: Boolean(lead),
      note: call?.note ?? null,
      trailing: call?.trailing ?? null,
      tools,
      writes,
      figure: await figureOf(root, spec.figure),
      readsContracts: spec.tools.some((n) => READS_CONTRACTS.test(sources.get(n) ?? '')),
      open: spec.open ? { layer: spec.open[0], mode: spec.open[1] } : null,
    });
  }

  // In the script's order. A step whose tools have all left the script sinks to
  // the end and says so, rather than keeping a place it no longer has.
  stages.sort((a, b) => (a.line ?? Infinity) - (b.line ?? Infinity));

  // Which earlier step a step reads: a file an earlier step writes, named in
  // this step's own source. Earliest writer wins, so a file two steps touch
  // (the schema reference) is credited to the step that made it.
  const writer = new Map();
  for (const stage of stages) {
    const names = new Set();
    for (const w of stage.writes) {
      if (!w.pattern.includes('*')) names.add(path.basename(w.pattern));
      for (const s of w.sample) names.add(path.basename(s));
    }
    stage.writeNames = names;
  }
  for (const stage of stages) {
    const mentioned = new Set();
    for (const tool of STAGES.find((s) => s.key === stage.key).tools) {
      for (const name of (sources.get(tool) ?? '').match(FILE_NAME) ?? []) mentioned.add(name);
    }
    const upstream = new Set();
    for (const name of mentioned) {
      if (stage.writeNames.has(name)) continue;
      const from = writer.get(name);
      if (from && from !== stage.key) upstream.add(from);
    }
    stage.upstream = [...upstream];
    for (const name of stage.writeNames) if (!writer.has(name)) writer.set(name, stage.key);
  }
  for (const stage of stages) delete stage.writeNames;

  const staged = new Set(STAGES.flatMap((s) => s.tools));
  const also = [];
  const seen = new Set();
  for (const call of calls) {
    if (staged.has(call.tool) || seen.has(call.tool)) continue;
    seen.add(call.tool);
    also.push({ tool: call.tool, line: call.line });
  }

  const contracts = await contractsOf(root);
  parsed.clear();

  return {
    present: true,
    script: SCRIPT,
    acts: ACTS,
    stages,
    contracts,
    checks,
    also,
    stats: {
      stages: stages.length,
      tools: new Set(calls.map((c) => c.tool)).size,
      outputs: stages.reduce((a, s) => a + s.writes.reduce((b, w) => b + w.files, 0), 0),
      checks: checks.length,
      contracts: contracts.length,
      operations: contracts.reduce((a, c) => a + c.operations, 0),
    },
  };
}
