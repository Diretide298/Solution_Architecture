/**
 * Everything a reader can search for, and where each thing is written down.
 *
 * The command palette searched `index.nodes` — **1,979 contract nodes and
 * nothing else.** Its own placeholder said so: "Search operations…". So a
 * reviewer looking for `POS-006`, `ADR-0016`, `access.scan_event` or a state
 * model got "No match", which does not mean "not in this package"; it means
 * "not a contract", and nothing on the screen said which.
 *
 * This adds the other 1,220: 492 screens, 123 state machines, 94 flows, 379
 * tables, 58 boards, 31 ADRs, 29 events and the platforms.
 *
 * Two things per entry, because "find it" and "go to it" are different needs:
 *
 *   where it is shown    a `kind:id` hash — the spelling `openArtefactHash`
 *                        already resolves and `currentSideId` already emits, so
 *                        every result is a shareable link and none of this
 *                        invents a second way to address the same artefact
 *   where it is written  file and line, resolved by finding the artefact's own
 *                        id in its own source
 *
 * **`line` is null rather than 1 when it could not be found.** A default of 1
 * is indistinguishable from a real answer at the top of a file, and sending
 * somebody to the wrong line is worse than telling them you only know the file:
 * they read what is there and believe it.
 */

import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

/** Read every file in a directory once, and hand back [name, lines]. */
async function readDir(root, dir, filter = /\.ya?ml$/i) {
  const abs = path.join(root, dir);
  const names = (await readdir(abs).catch(() => [])).filter((f) => filter.test(f));
  const out = [];
  for (const name of names) {
    const text = await readFile(path.join(abs, name), 'utf8').catch(() => null);
    if (text != null) out.push([`${dir}/${name}`, text.split(/\r?\n/)]);
  }
  return out;
}

/**
 * `- id: POS-006` and `id: F74`, mapped to where they are written.
 *
 * Anchored on the whole value so `POS-6` cannot match the line that defines
 * `POS-60`, and `-` is optional because a screen is a list item and a flow is
 * the document root.
 */
function idIndex(files) {
  const map = new Map();
  const ID = /^\s*-?\s*id:\s*['"]?([A-Za-z0-9][\w.-]*)['"]?\s*$/;
  for (const [file, lines] of files) {
    for (let i = 0; i < lines.length; i += 1) {
      const hit = ID.exec(lines[i]);
      // First wins: an id repeated further down a file is a reference to the
      // definition above it, not a second definition.
      if (hit && !map.has(hit[1])) map.set(hit[1], { file, line: i + 1 });
    }
  }
  return map;
}

/** `CREATE TABLE access.scan_event (` across the migrations. */
function tableIndex(files) {
  const map = new Map();
  const RE = /^\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][\w]*\.[A-Za-z_][\w]*)/i;
  for (const [file, lines] of files) {
    for (let i = 0; i < lines.length; i += 1) {
      const hit = RE.exec(lines[i]);
      if (hit && !map.has(hit[1].toLowerCase())) {
        map.set(hit[1].toLowerCase(), { file, line: i + 1 });
      }
    }
  }
  return map;
}

/**
 * Where a one-artefact-per-file document actually starts.
 *
 * A state model carries no `id:` — `states/work-order.yaml` opens with three
 * comment lines and then `entity: Work order`. Indexing those files by `id:`
 * matched nothing at all and every state model came back file-only. The first
 * line that is neither blank nor a comment is where the model begins, which is
 * the line somebody reading it wants.
 */
function firstContentLine(lines) {
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line.trim() || /^\s*#/.test(line) || /^---\s*$/.test(line)) continue;
    return i + 1;
  }
  return null;
}

function startIndex(files) {
  const map = new Map();
  for (const [file, lines] of files) map.set(file, firstContentLine(lines));
  return map;
}

/** The heading of a markdown file — where an ADR actually starts. */
async function headingLine(root, rel) {
  const text = await readFile(path.join(root, rel), 'utf8').catch(() => null);
  if (text == null) return null;
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    if (/^#\s+\S/.test(lines[i])) return i + 1;
  }
  return null;
}

/**
 * @param root      the package directory
 * @param subjects  the built payloads — journeys, domain, decisions, backend, uiux, platforms
 */
export async function buildSearch(root, subjects = {}) {
  const { journeys, domain, decisions, backend, uiux, platforms } = subjects;
  const entries = [];

  const screenFiles = await readDir(root, 'screens');
  const flowFiles = await readDir(root, 'flows');
  const stateFiles = await readDir(root, 'states');
  const eventFiles = await readDir(root, 'events');
  const sqlFiles = await readDir(root, 'backend', /\.sql$/i);

  const screenAt = idIndex(screenFiles);
  const flowAt = idIndex(flowFiles);
  const stateAt = idIndex(stateFiles);
  const eventAt = idIndex(eventFiles);
  const tableAt = tableIndex(sqlFiles);
  const startsAt = startIndex([...stateFiles, ...eventFiles]);

  // A state model and an event are one file each, so the file itself is the
  // answer when the document carries no `id:` of its own.
  const fileStems = new Map();
  for (const [file] of [...stateFiles, ...eventFiles]) {
    fileStems.set(path.basename(file).replace(/\.ya?ml$/i, '').toLowerCase(), file);
  }

  const at = (map, id, fallbackFile = null) => {
    const found = id == null ? null : map.get(String(id));
    if (found) return found;
    return fallbackFile ? { file: fallbackFile, line: null } : { file: null, line: null };
  };

  // ---- screens -------------------------------------------------------------
  for (const s of journeys?.screens ?? []) {
    const where = at(screenAt, s.id, s.file);
    entries.push({
      kind: 'screen',
      id: s.id,
      name: s.name ?? s.id,
      sub: [s.platform, s.module].filter(Boolean).join(' · ') || null,
      file: where.file, line: where.line,
      hash: `screen:${s.id}`, layer: 'frontend',
      terms: [s.id, s.name, s.module, s.platform, s.purpose].filter(Boolean).join(' '),
    });
  }

  // ---- flows ---------------------------------------------------------------
  for (const f of journeys?.flows ?? []) {
    const where = at(flowAt, f.id, f.file);
    entries.push({
      kind: 'flow',
      id: f.id,
      name: f.name ?? f.id,
      sub: `${(f.steps ?? []).length} steps`,
      file: where.file, line: where.line,
      hash: `flow:${f.id}`, layer: 'frontend',
      terms: [f.id, f.name, ...(f.steps ?? []).map((x) => x.screenId)].filter(Boolean).join(' '),
    });
  }

  // ---- state machines ------------------------------------------------------
  for (const m of domain?.machines ?? []) {
    const file = m.file ?? fileStems.get(String(m.id).toLowerCase()) ?? null;
    const where = stateAt.get(String(m.id))
      ?? (file ? { file, line: startsAt.get(file) ?? null } : { file: null, line: null });
    entries.push({
      kind: 'state',
      id: m.id,
      name: m.entity ?? m.id,
      sub: [m.enum, m.owner].filter(Boolean).join(' · ') || null,
      file: where.file, line: where.line,
      hash: `machine:${m.id}`, layer: 'domain',
      terms: [m.id, m.entity, m.enum, m.owner, m.domain, ...(m.enumValues ?? [])]
        .filter(Boolean).join(' '),
    });
  }

  // ---- events --------------------------------------------------------------
  for (const e of domain?.events ?? []) {
    const id = e.id ?? e.name;
    const efile = e.file ?? fileStems.get(String(id).toLowerCase()) ?? null;
    const where = eventAt.get(String(id))
      ?? (efile ? { file: efile, line: startsAt.get(efile) ?? null } : { file: null, line: null });
    entries.push({
      kind: 'event',
      id,
      name: e.name ?? id,
      sub: e.producer ?? e.owner ?? null,
      file: where.file, line: where.line,
      hash: `event:${id}`, layer: 'domain',
      terms: [id, e.name, e.producer, e.owner, ...(e.consumers ?? [])].filter(Boolean).join(' '),
    });
  }

  // ---- ADRs ----------------------------------------------------------------
  for (const a of decisions?.adrs ?? []) {
    entries.push({
      kind: 'adr',
      id: a.id,
      name: a.title ?? a.id,
      sub: [a.status, a.date].filter(Boolean).join(' · ') || null,
      file: a.file ?? null,
      line: a.file ? await headingLine(root, a.file) : null,
      hash: `adr:${a.id}`, layer: 'decisions',
      terms: [`ADR-${a.number ?? a.id}`, a.id, a.title, a.status].filter(Boolean).join(' '),
    });
  }

  // ---- tables --------------------------------------------------------------
  // **Only 39 of the 379 tables have DDL**, and that is not a gap in this
  // lookup — it is the same 39 the workbook's `Written` column counts. A table
  // with no `CREATE TABLE` is a table nobody has migrated yet, so the honest
  // second-best is the contract schema that defines its shape, labelled as
  // such. Reporting the schema as though it were the definition would turn
  // "not built yet" into "here it is".
  for (const t of backend?.tables ?? []) {
    const ddl = tableAt.get(String(t.name).toLowerCase());
    const where = ddl ?? (t.schemaFile ? { file: t.schemaFile, line: null } : { file: null, line: null });
    entries.push({
      kind: 'table',
      id: t.name,
      name: t.name,
      sub: [t.module, t.columns ? `${t.columns} columns` : null].filter(Boolean).join(' · ') || null,
      file: where.file, line: where.line,
      // What the file above actually is, so the reader is not told a contract
      // is a migration.
      fileIs: ddl ? 'migration' : (t.schemaFile ? 'contract' : null),
      written: Boolean(ddl),
      hash: `table:${t.name}`, layer: 'backend',
      terms: [t.name, t.module, t.derivedFrom, t.migration].filter(Boolean).join(' '),
    });
  }

  // ---- boards --------------------------------------------------------------
  // No line: a board is a rendered page, not a document with a definition in
  // it, and its frames are anchors rather than lines.
  for (const b of uiux?.boards ?? []) {
    entries.push({
      kind: 'board',
      id: b.id,
      name: b.name,
      sub: [b.kind, `${b.frameCount} frames`].filter(Boolean).join(' · '),
      file: `${b.folder}/${b.file}`, line: null,
      hash: `board:${b.name}`, layer: 'frontend',
      // A board also has a page of its own, and for the 23 nothing points
      // at, that page is the only place it appears.
      href: '/uiux.html',
      terms: [b.name, b.file, b.title, ...b.platforms,
        ...b.frames.map((f) => `${f.anchor} ${f.name ?? ''}`)].filter(Boolean).join(' '),
    });
  }

  // ---- platforms -----------------------------------------------------------
  for (const p of platforms?.platforms ?? []) {
    entries.push({
      kind: 'platform',
      id: p.code ?? p.name,
      name: p.name ?? p.code,
      sub: p.appName ?? null,
      file: p.file ?? null, line: null,
      hash: `platform:${p.code ?? p.name}`, layer: 'frontend',
      terms: [p.code, p.name, p.appName].filter(Boolean).join(' '),
    });
  }

  const byKind = {};
  for (const e of entries) byKind[e.kind] = (byKind[e.kind] ?? 0) + 1;

  return {
    present: entries.length > 0,
    entries,
    stats: {
      entries: entries.length,
      byKind,
      // How much of this can actually take somebody to a line, which is the
      // difference between "we have it" and "we can show you".
      located: entries.filter((e) => e.file && e.line).length,
      fileOnly: entries.filter((e) => e.file && !e.line).length,
      unplaced: entries.filter((e) => !e.file).length,
    },
  };
}
