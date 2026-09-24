/**
 * The package as a spreadsheet: one sheet per kind of thing, flat.
 *
 * **This is not the document in another format, and the difference is the
 * shape.** `document.mjs` nests — a table under its module, an operation under
 * its contract — because that is how somebody *reads* a package. A spreadsheet
 * is for the other thing: sorting, filtering, pivoting, pasting a column into
 * an estimate. So every sheet here is flat and every fact a row needs to stand
 * on its own is repeated onto it. A columns sheet carries its table name on
 * every one of eleven thousand rows, and that redundancy is the feature; a
 * reader who wants the nesting has the document.
 *
 * Counts stay numbers, so a column of them adds up. Everything else is text,
 * including ids like `P04` and versions like `1.10` that Excel would otherwise
 * decide were dates or decimals.
 *
 * The section ids are `document.mjs`'s, so the same picker drives both and the
 * same audience rules apply — with `wireframes` added, which the document has
 * no section for because a board is a picture and a document cannot show it.
 */

/** Prose in a cell. Newlines collapse: a cell with a paragraph in it makes the
 *  row taller than the screen, and the package has 25,000-character fields. */
function cell(value, at = 500) {
  if (value == null) return '';
  const s = String(value).replace(/\s*\n+\s*/g, ' ').trim();
  return s.length <= at ? s : `${s.slice(0, at).trimEnd()}…`;
}

const yes = (v) => (v ? 'yes' : '');

/** Board titles are lifted out of `<title>` in an HTML file, so they arrive
 *  carrying HTML entities. `TICVAI Guest &mdash; a pack` is the title; the
 *  em dash is what somebody meant to read. */
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
  mdash: '—', ndash: '–', hellip: '…', rsquo: '’', lsquo: '‘',
  ldquo: '“', rdquo: '”' };
const unescapeHtml = (text) => String(text ?? '').replace(
  /&(#x?[0-9a-fA-F]+|[a-zA-Z]+);/g, (whole, body) => {
    if (body[0] === '#') {
      const code = body[1] === 'x' || body[1] === 'X'
        ? parseInt(body.slice(2), 16) : parseInt(body.slice(1), 10);
      return Number.isFinite(code) && code > 0 ? String.fromCodePoint(code) : whole;
    }
    return ENTITIES[body.toLowerCase()] ?? whole;
  });
const list = (v) => (Array.isArray(v) ? v.filter(Boolean).join(', ') : cell(v));
/** A count, kept as a number so the column sums. Blank when it is not one —
 *  a zero and "nobody counted" are different facts. */
const num = (v) => (typeof v === 'number' && Number.isFinite(v) ? v : '');

// ── the sheets, by section ───────────────────────────────────────────

const overview = (pkg, meta) => {
  const ix = pkg.index?.stats ?? {};
  const rows = [
    ['Project', meta.name ?? meta.id],
    ['Generated', meta.on],
    ['Contracts', num(ix.files)],
    ['Operations', num(ix.operations)],
    ['Screens', num(pkg.journeys?.screens?.length)],
    ['Journeys', num(pkg.journeys?.flows?.length)],
    ['Platforms', num(pkg.journeys?.platforms?.length)],
    ['Modules', num(pkg.backend?.modules?.length)],
    ['Tables', num(pkg.backend?.tables?.length)],
    ['Services', num(pkg.diagrams?.services?.length)],
    ['State models', num(pkg.domain?.machines?.length)],
    ['Events', num(pkg.domain?.events?.length)],
    ['Decisions', num(pkg.decisions?.adrs?.length)],
    ['Wireframe boards', num(pkg.uiux?.stats?.boards)],
  ];
  return [{ name: 'Overview', columns: ['Thing', 'Count'], rows, widths: [28, 42] }];
};

const frontend = (pkg) => {
  const screens = pkg.journeys?.screens ?? [];
  const out = [];

  const platforms = pkg.journeys?.platforms ?? [];
  if (platforms.length) {
    out.push({
      name: 'Platforms',
      columns: ['Code', 'Name', 'Surface', 'Runtime', 'Works offline', 'Screens'],
      widths: [10, 34, 16, 16, 14, 10],
      rows: platforms.map((p) => [p.code, p.shortName || p.name, p.surface, p.runtime,
        yes(p.offlineCapable), screens.filter((s) => s.platform === p.code).length]),
    });
  }

  const flows = pkg.journeys?.flows ?? [];
  if (flows.length) {
    out.push({
      name: 'Journeys',
      columns: ['Id', 'Journey', 'Actor', 'Wave', 'How critical', 'Steps'],
      widths: [14, 40, 18, 10, 16, 8],
      rows: flows.map((f) => [f.id, f.name, f.actor, f.wave, f.criticality, (f.steps ?? []).length]),
    });
  }

  if (screens.length) {
    // One sheet, with the platform as a column. The document splits screens by
    // platform because 2,427 rows is a table nobody reads; a spreadsheet sorts
    // and filters, so splitting them here would take away the one thing it is
    // better at than the document.
    out.push({
      name: 'Screens',
      columns: ['Id', 'Screen', 'Platform', 'Module', 'Wave', 'What it is for'],
      widths: [16, 38, 22, 22, 8, 70],
      rows: screens.map((s) => [s.id, s.name, s.platformName || s.platform, s.module, s.wave,
        cell(s.purpose)]),
    });
  }
  return out;
};

const contracts = (pkg) => {
  const nodes = pkg.index?.nodes ?? [];
  const files = nodes.filter((n) => n.type === 'file');
  const operations = nodes.filter((n) => n.type === 'operation');
  const titleOf = new Map(files.map((f) => [f.file, f.title || f.name]));
  const out = [];

  if (files.length) {
    out.push({
      name: 'Contracts',
      columns: ['Contract', 'File', 'Tier', 'Operations', 'What it is'],
      widths: [30, 44, 16, 12, 70],
      rows: files.map((f) => [f.title || f.name, f.file, f.tier,
        operations.filter((op) => op.file === f.file).length, cell(f.description)]),
    });
  }

  if (operations.length) {
    out.push({
      name: 'Operations',
      columns: ['Operation', 'Method', 'Path', 'Contract', 'Permission', 'Offline', 'What it does'],
      widths: [34, 10, 46, 28, 26, 9, 60],
      rows: operations.map((op) => [op.name, (op.method || '').toUpperCase(), op.path,
        titleOf.get(op.file) ?? op.file, op.permission, yes(op.offlineCapable),
        cell(op.title || op.description)]),
    });
  }
  return out;
};

const domain = (pkg) => {
  const machines = pkg.domain?.machines ?? [];
  const events = pkg.domain?.events ?? [];
  const out = [];

  if (machines.length) {
    out.push({
      name: 'State models',
      columns: ['Entity', 'Owner', 'Starts at', 'Ends at', 'States', 'Transitions'],
      widths: [26, 24, 18, 26, 10, 12],
      rows: machines.map((m) => [m.entity || m.id, m.owner, m.initial, list(m.terminal),
        (m.states ?? []).length, (m.transitions ?? []).length]),
    });
    // Every move, on one sheet, each carrying its model. This is the part
    // somebody building against the package actually works from.
    const moves = machines.flatMap((m) => (m.transitions ?? []).map((t) => [
      m.entity || m.id, t.from, t.to, t.operation || t.trigger, cell(t.guard, 200),
      yes(t.requiresApproval), list(t.emits),
    ]));
    if (moves.length) {
      out.push({
        name: 'Transitions',
        columns: ['Entity', 'From', 'To', 'By', 'Only when', 'Needs approval', 'Emits'],
        widths: [24, 20, 20, 30, 50, 15, 30],
        rows: moves,
      });
    }
  }

  if (events.length) {
    out.push({
      name: 'Events',
      columns: ['Event', 'Published by', 'When', 'Consumed by'],
      widths: [32, 24, 60, 40],
      // A consumer names the context that listens, not a service: the field is
      // `context`, and reaching for `name` produced a column of bare commas
      // that looked like six consumers with no names rather than a wrong key.
      rows: events.map((e) => [e.name || e.id, e.publisher, cell(e.emittedWhen),
        (e.consumers ?? []).map((c) => (typeof c === 'string' ? c
          : c.context ?? c.name ?? c.service ?? '')).filter(Boolean).join(', ')]),
    });
  }
  return out;
};

const backend = (pkg) => {
  const modules = pkg.backend?.modules ?? [];
  const tables = pkg.backend?.tables ?? [];
  // An object keyed by table name, not a list — the shape that threw
  // `columns is not iterable` the first time anything read it.
  const columns = pkg.backend?.columns ?? {};
  const out = [];

  if (modules.length) {
    out.push({
      name: 'Modules',
      columns: ['Module', 'Tables', 'What it is', 'Why it exists'],
      widths: [26, 10, 70, 70],
      rows: modules.map((m) => [m.name, tables.filter((t) => t.module === m.name).length,
        cell(m.what), cell(m.why)]),
    });
  }

  if (tables.length) {
    out.push({
      name: 'Tables',
      columns: ['Table', 'Module', 'Columns', 'Storage only', 'Why it holds what it holds'],
      widths: [34, 24, 10, 14, 80],
      rows: tables.map((t) => [t.name, t.module, (columns[t.name] ?? []).length,
        yes(t.storageOnly), t.storageOnly ? '' : cell(t.storageReason)]),
    });

    const every = tables.flatMap((t) => (columns[t.name] ?? []).map((c) => [
      t.name, t.module, c.name, c.type, yes(c.required), c.source, cell(c.description, 300),
    ]));
    if (every.length) {
      out.push({
        name: 'Columns',
        columns: ['Table', 'Module', 'Column', 'Type', 'Required', 'From', 'Notes'],
        widths: [30, 22, 28, 22, 10, 22, 60],
        rows: every,
      });
    }
  }
  return out;
};

const services = (pkg) => {
  const all = pkg.diagrams?.services ?? [];
  if (!all.length) return [];
  return [{
    name: 'Services',
    columns: ['Service', 'Tier', 'Operations', 'Tables', 'Owns', 'Why it exists', 'If it is down'],
    widths: [26, 18, 12, 10, 34, 80, 60],
    rows: all.map((s) => [s.name, s.tier, num(s.operations), num(s.tables), list(s.schemas),
      cell(s.why), cell(s.ifDown)]),
  }];
};

const decisions = (pkg) => {
  const adrs = pkg.decisions?.adrs ?? [];
  const docs = pkg.decisions?.documents ?? [];
  const out = [];
  if (adrs.length) {
    out.push({
      name: 'Decisions',
      columns: ['Id', 'Title', 'Status', 'Verdict', 'Date', 'Superseded by'],
      widths: [12, 60, 16, 18, 14, 18],
      rows: [...adrs].sort((a, b) => Number(a.number) - Number(b.number))
        .map((a) => [a.id, a.title, a.status, a.verdict, a.date, a.supersededBy]),
    });
  }
  if (docs.length) {
    out.push({
      name: 'Registers',
      columns: ['Document', 'Group', 'Rows'],
      widths: [50, 26, 10],
      rows: docs.map((d) => [d.title || d.id, d.group, num(d.rows)]),
    });
  }
  return out;
};

const wireframes = (pkg) => {
  const boards = pkg.uiux?.boards ?? [];
  if (!boards.length) return [];
  return [{
    name: 'Wireframes',
    columns: ['Board', 'Folder', 'File', 'Kind', 'Revision', 'Frames', 'Links', 'Modified', 'Address'],
    widths: [40, 20, 44, 12, 12, 10, 10, 22, 50],
    rows: boards.map((b) => [unescapeHtml(b.title || b.name), b.folder, b.file, b.kind, b.revision,
      (b._frames ?? []).length, (b.links ?? []).length,
      String(b.modified ?? '').slice(0, 10), b.url]),
  }];
};

const BUILDERS = { overview, frontend, contracts, domain, backend, services, decisions, wireframes };

/** The sections a workbook can carry. The first seven are document.mjs's, by
 *  the same ids, so one picker drives both. */
export const SECTIONS = [
  { id: 'overview', title: 'Overview' },
  { id: 'frontend', title: 'Platforms, journeys and screens' },
  { id: 'contracts', title: 'Contracts and operations' },
  { id: 'domain', title: 'State models and events' },
  { id: 'backend', title: 'Modules, tables and columns' },
  { id: 'services', title: 'Services' },
  { id: 'decisions', title: 'Decisions' },
  { id: 'wireframes', title: 'Wireframe boards' },
];

/**
 * The sheets for one workbook.
 *
 * `allowed` is worked out from the audience rules by the caller, never here —
 * the same contract `buildDocument` has. A section whose layer has not been
 * built contributes no sheets rather than an empty one, because a sheet with
 * only a header row reads as "there are none" when the truth is "not read yet".
 */
export function buildSheets(pkg, meta, wanted, allowed) {
  const asked = new Set((wanted ?? []).filter((id) => allowed.includes(id)));
  const out = [];
  for (const section of SECTIONS) {
    if (!asked.has(section.id)) continue;
    out.push(...(BUILDERS[section.id]?.(pkg, meta) ?? []));
  }
  return out;
}
