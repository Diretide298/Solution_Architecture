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
  const { journeys, domain, decisions, backend, uiux, platforms, burst } = subjects;
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

  // ---- pages ---------------------------------------------------------------
  // The viewer's standalone pages, so Ctrl+K can reach them.
  //
  // **They were reachable only from the account panel.** Every one of these is
  // about what the package contains, and the way in was a list of links beside
  // "Manage accounts and invites" — where somebody goes to change their sign-in
  // and not to ask what a flash sale runs. A page nothing points at from the
  // view that raises its question is a page that does not exist, and search is
  // the one place a reader looks for something by name rather than by route.
  //
  // Gated on the subject actually being in the package: a scenario with no
  // burst scope should not offer a page that opens on nothing.
  // The handoff pages ship as standalone HTML inside the package rather than
  // as viewer routes, so they are listed only when the package actually holds
  // them: a drop without the simulator should not offer to open it. Named
  // rather than globbed — `handoff/` is full of `.dc.html` boards elsewhere in
  // the tree and these two are the ones that are pages in their own right.
  const handoffFiles = new Set(await readdir(path.join(root, 'handoff')).catch(() => []));

  const pages = [
    burst?.services?.length && {
      id: 'burst', name: 'Flash sale — what an environment runs',
      sub: `${burst.totals?.deployed ?? 0} of ${burst.totals?.services ?? 0} services deployed`,
      // The layer, not the old page. `burst.html` still redirects here, and a
      // search result that lands on a redirect is a result that flashes.
      href: '/?layer=cicd&mode=cicd-burst',
      terms: 'flash sale burst scope deployment map environment clusters replicas '
        + 'scale out scaling contended inventory hold seat hold pgbouncer scenario c '
        + (burst.services ?? []).map((x) => x.name).join(' '),
    },
    handoffFiles.has('Burst Simulator.dc.html') && {
      id: 'burst-simulator', name: 'Burst simulator — a flash sale solved',
      sub: 'the package’s own model: queueing, contention and eleven configurations',
      pkgHref: '/handoff/Burst Simulator.dc.html',
      terms: 'burst simulator flash sale model queueing mmc m/m/c lease contention '
        + 'p99 latency shed oversell sharding coalescing idempotency scenario '
        + 'configurations variants recommendation timeline scrub free run',
    },
    handoffFiles.has('Shared Cell.dc.html') && {
      id: 'shared-cell', name: 'Shared cell — the platform at rest',
      sub: 'what runs between sales, two venues to a cell',
      // The tab that frames it rather than the file, so a reader arrives with
      // the rest of the layer around them. The file is still openable from
      // there, and from the burst simulator's own header.
      href: '/?layer=cicd&mode=cicd-cell',
      terms: 'shared cell platform at rest steady state two venues per cell '
        + 'b-shared-platform tenancy isolation cost per venue',
    },
    { id: 'cicd', name: 'CI/CD — how this is built, shipped and run',
      sub: 'pipelines, images and the four deployments — and what they disagree about',
      href: '/?layer=cicd&mode=cicd-pipeline',
      terms: 'cicd ci cd pipeline delivery build ship deploy github actions workflow job step '
        + 'gate dockerfile image registry publish terraform runbook repos services deploy '
        + 'compose scenario variant continuous integration deployment' },
    // The layer, not the old page: `uiux.html` only redirects here now, and a
    // search result that lands on a redirect is a result that flashes.
    { id: 'uiux', name: 'UI/UX — screens, flows and boards', href: '/?layer=uiux&mode=uiux-screens',
      terms: 'uiux wireframes boards frames screens flows' },
    // Everybody's own settings. Findable by what people call the things on it,
    // because nobody searches for "settings" when what they want is to change a
    // password or paste an OpenProject token.
    { id: 'settings', name: 'Settings — password, OpenProject, git identity, Claude connector',
      sub: 'your account, and signing out of other devices',
      href: '/settings.html',
      terms: 'settings account profile password change openproject token pms git email identity '
        + 'claude connector mcp bridge sessions sign out everywhere preferences' },
    { id: 'domains', name: 'Domain lenses', href: '/domains.html',
      terms: 'domain lenses cross-cutting subjects ai flash sale' },
    { id: 'audit', name: 'Audit the delivery package', href: '/audit.html',
      terms: 'audit dump checks validators problems package' },
    { id: 'validation', name: 'What has been signed off', href: '/validation.html',
      terms: 'validation sign-off verdicts reviews approved' },
  ].filter(Boolean);
  for (const page of pages) {
    entries.push({
      kind: 'page',
      id: page.id,
      name: page.name,
      sub: page.sub ?? 'a page of its own',
      file: null, line: null,
      hash: null, layer: null,
      href: page.href ?? null,
      // A page inside the package rather than a viewer route. Kept apart from
      // `href` because it is not an address yet — the project prefix goes on
      // in the client, which is the only place that knows which project the
      // reader has open.
      pkgHref: page.pkgHref ?? null,
      terms: `${page.name} ${page.terms}`,
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
