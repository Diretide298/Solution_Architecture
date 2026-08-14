// Reads backend/ — the database schema reference and the ADRs beside it.
//
// The schema reference is an .xlsx rather than YAML, so it is read directly
// instead of being converted: the spreadsheet stays the one source of truth and
// there is no generated copy to drift from it.
//
// The join that makes this worth drawing is the `Derived from` column. Every
// table names the contract schema it came from, so a table can be traced back to
// the API that defines it, and a contract schema with no table can be spotted.

import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { readWorkbook } from './xlsx.mjs';
import { buildMigrations } from './migrations.mjs';

// The workbook is delivered to more than one folder and the copies drift —
// backend/ held a build two versions behind handoff/ for a while. Rather than
// pick a folder and be quietly wrong, every copy is found and the newest wins.
const WORKBOOK_DIRS = ['backend', 'handoff', 'docs', 'sources'];

async function findWorkbook(root) {
  const candidates = [];
  for (const dir of WORKBOOK_DIRS) {
    let entries;
    try {
      entries = await readdir(path.join(root, dir), { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      if (!entry.isFile() || !/\.xlsx$/i.test(entry.name) || entry.name.startsWith('~$')) continue;
      const rel = `${dir}/${entry.name}`;
      const info = await stat(path.join(root, rel)).catch(() => null);
      if (info) candidates.push({ rel, mtime: info.mtimeMs, size: info.size });
    }
  }
  candidates.sort((a, b) => b.mtime - a.mtime);
  return candidates;
}

/**
 * Find the header row and map everything below it to objects.
 *
 * The sheets carry a title and a note above the header, so a fixed row index
 * breaks the first time someone adds a line of explanation. Columns come and go
 * too — the 14 August rebuild replaced `Child of` with `Written` — so only the
 * columns that identify the sheet are required, and the rest are read if
 * present and left empty if not. A rebuild should cost a column, not a sheet.
 */
function table(rows, required, optional = []) {
  const wanted = required.map((h) => h.toLowerCase());
  let headerRow = -1;

  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].map((c) => String(c ?? '').trim().toLowerCase());
    if (wanted.every((w) => cells.includes(w))) { headerRow = i; break; }
  }
  if (headerRow < 0) return { rows: [], missing: true, columns: [] };

  const cols = rows[headerRow].map((c) => String(c ?? '').trim().toLowerCase());
  const at = (row, name) => {
    const index = cols.indexOf(name.toLowerCase());
    return index < 0 ? '' : String(row[index] ?? '').trim();
  };

  const headers = [...required, ...optional];
  const out = [];
  for (let i = headerRow + 1; i < rows.length; i++) {
    const row = rows[i];
    if (!row.some((c) => String(c ?? '').trim())) continue;
    const record = {};
    for (const header of headers) record[header] = at(row, header);
    out.push(record);
  }
  return {
    rows: out,
    missing: false,
    columns: rows[headerRow].map((c) => String(c ?? '').trim()).filter(Boolean),
  };
}

/** Just enough to render an ADR heading and lede as plain text. */
const stripMarkdown = (text) =>
  text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/`(.*?)`/g, '$1')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .trim();

const number = (value) => {
  const text = String(value ?? '').replace(/,/g, '').trim();
  if (!text) return null; // Number('') is 0, which would make a blank cell data
  const n = Number(text);
  return Number.isFinite(n) ? n : null;
};

/** The leading prose of a sheet — the single-cell rows, wherever the cell sits. */
function preamble(rows, limit = 6) {
  const out = [];
  for (const row of rows.slice(0, limit)) {
    const filled = (row ?? []).map((c) => String(c ?? '').trim()).filter(Boolean);
    if (filled.length === 1) out.push(filled[0]);
  }
  return out;
}

/**
 * Foreign keys, without guessing at them.
 *
 * The workbook says which contract schema and property each column came from.
 * The contracts say whether that property is a `$ref` to another schema. Where
 * that target schema also has a table, the two tables are related — and every
 * link in that chain is declared, so nothing here is inferred from a column
 * being called `something_id`.
 */
function addReferences(tables, columns, contractSchemas) {
  const schemaById = new Map(contractSchemas.map((s) => [s.id, s]));
  const tableBySchema = new Map();
  for (const t of tables) if (t.schemaId) tableBySchema.set(t.schemaId, t.name);

  for (const t of tables) {
    t.references = [];
    const schema = t.schemaId ? schemaById.get(t.schemaId) : null;
    if (!schema?.properties) continue;

    const properties = new Map(schema.properties.map((p) => [p.name, p]));
    for (const column of columns[t.name] ?? []) {
      const property = properties.get(column.source?.split('.').pop() ?? column.name);
      const target = property?.refTarget ? tableBySchema.get(property.refTarget) : null;
      if (!target || target === t.name) continue;
      column.referencesTable = target;
      t.references.push({
        column: column.name,
        toTable: target,
        viaSchema: schemaById.get(property.refTarget)?.name ?? null,
        isArray: Boolean(property.isArray),
      });
    }
  }
}

/**
 * Foreign keys by naming convention — the other half of the ER diagram.
 *
 * The workbook has no key column, and only 11 relationships survive as `$ref`s
 * in the contracts, so an ER drawn from declarations alone is a page of boxes.
 * A column ending `_id` whose name resolves to a table almost always is a key,
 * so those edges are drawn too — but marked inferred, kept in their own count,
 * and switchable off, because "almost always" is not "declared".
 *
 * `added_by_principal_id` resolves by trying successively shorter suffixes:
 * `added_by_principal`, `by_principal`, `principal`. A table in the column's
 * own schema wins over one in another, and a name owned by two schemas is
 * refused rather than guessed at.
 */
function addForeignKeys(tables, columns, problems, workbookName, migrations) {
  const full = new Set(tables.map((t) => t.name));
  const short = new Map();
  const ambiguous = new Set();
  for (const table of tables) {
    const bare = table.name.split('.').slice(1).join('.');
    if (short.has(bare)) ambiguous.add(bare);
    else short.set(bare, table.name);
  }

  // Where a migration already resolves a column name, use its answer for the
  // same name elsewhere. venue_id has no venue table and never will — a venue
  // is a level of platform.scope_node — and only the DDL knows that.
  const taught = new Map();
  const conflicting = new Set();
  for (const ddl of Object.values(migrations?.tables ?? {})) {
    for (const key of ddl.foreignKeys) {
      // a composite key here is an id plus a level discriminator, so the first
      // column is the one that names the thing — (venue_id, venue_level)
      const column = key.columns[0];
      if (!column) continue;
      if (taught.has(column) && taught.get(column) !== key.toTable) conflicting.add(column);
      else taught.set(column, key.toTable);
    }
  }
  for (const column of conflicting) taught.delete(column);

  const resolve = (module, column) => {
    const parts = column.replace(/_id$/, '').split('_');
    for (let i = 0; i < parts.length; i++) {
      const candidate = parts.slice(i).join('_');
      if (full.has(`${module}.${candidate}`)) return `${module}.${candidate}`;
      if (short.has(candidate) && !ambiguous.has(candidate)) return short.get(candidate);
    }
    return taught.get(column) ?? null;
  };

  const unresolved = new Map();

  for (const table of tables) {
    table.foreignKeys = [];
    const declared = new Set((table.references ?? []).map((r) => r.column));

    for (const column of columns[table.name] ?? []) {
      if (!/_id$/.test(column.name) || declared.has(column.name)) continue;
      const target = resolve(table.module, column.name);
      if (!target) {
        unresolved.set(column.name, (unresolved.get(column.name) ?? 0) + 1);
        continue;
      }
      column.foreignKeyTable = target;
      table.foreignKeys.push({
        column: column.name,
        toTable: target,
        self: target === table.name,
        crossSchema: target.split('.')[0] !== table.module,
        // this one was learned from a migration, not from the table's name
        fromDdl: taught.get(column.name) === target,
      });
    }
  }

  // a name referenced everywhere with no table behind it is worth saying once
  for (const [column, count] of [...unresolved].sort((a, b) => b[1] - a[1])) {
    if (count < 5) continue;
    problems.push({
      severity: 'warning',
      kind: 'backend-dangling-key',
      file: workbookName,
      message:
        `${count} columns are called ${column}, and no table is named for it — ` +
        `either the entity is not persisted here or the table is missing`,
    });
  }

  return unresolved;
}

/**
 * Where a migration exists, the database has already answered the question the
 * name-matching was guessing at. A `REFERENCES` clause outranks both the
 * workbook and the column name, so a table covered by DDL drops its inferred
 * keys entirely and reports the real ones.
 */
function applyMigrations(tables, columns, migrations, problems) {
  if (!migrations.present) return;
  const byName = new Map(tables.map((t) => [t.name, t]));

  for (const [name, ddl] of Object.entries(migrations.tables)) {
    const table = byName.get(name);
    if (!table) {
      // a table in the DDL that the workbook has never heard of
      problems.push({
        severity: 'warning',
        kind: 'migration-table-not-in-workbook',
        file: `backend/${ddl.file}`,
        message: `${name} is created by ${ddl.file} but is not on the workbook's Tables sheet`,
      });
      continue;
    }

    table.ddl = {
      file: ddl.file,
      partitionBy: ddl.partitionBy,
      partitionOf: ddl.partitionOf,
      primaryKey: ddl.primaryKey,
      rls: ddl.rls ?? null,
      columns: ddl.columns.length,
      generated: ddl.columns.filter((c) => c.generated).map((c) => c.name),
    };
    table.keys = ddl.foreignKeys.map((key) => ({
      columns: key.columns,
      toTable: key.toTable,
      onDelete: key.onDelete,
      composite: key.composite,
      crossSchema: key.toTable.split('.')[0] !== table.module,
      self: key.toTable === table.name,
    }));

    // the DDL is the answer, so the guesses for this table go
    table.foreignKeys = [];
    for (const column of columns[name] ?? []) {
      delete column.foreignKeyTable;
      const key = ddl.foreignKeys.find((k) => k.columns.includes(column.name));
      if (key) column.keyTable = key.toTable;
      const declared = ddl.columns.find((c) => c.name === column.name);
      if (declared?.generated) column.generated = true;
    }
  }

  // columns the DDL has that the workbook does not
  for (const [name, ddl] of Object.entries(migrations.tables)) {
    if (!byName.has(name) || !ddl.columns.length) continue;
    const known = new Set((columns[name] ?? []).map((c) => c.name));
    // audit columns are on nearly every table and are not worth 25 warnings
    const AUDIT = /^(created|updated|deleted)_(at|by)$|^(row_)?version$/;
    const extra = ddl.columns
      .filter((c) => !known.has(c.name) && !AUDIT.test(c.name))
      .map((c) => c.name);
    if (extra.length) {
      problems.push({
        severity: 'info',
        kind: 'migration-extra-columns',
        file: `backend/${ddl.file}`,
        message: `${name} has ${extra.length} column(s) in the DDL that the workbook does not list: ${extra.join(', ')}`,
      });
    }
  }

  // the workbook's Written column against the SQL that is actually on disk —
  // a table claimed as written with no DDL behind it is the expensive kind of wrong
  for (const table of tables) {
    if (table.claimsWritten && !table.ddl) {
      problems.push({
        severity: 'error',
        kind: 'migration-claimed-not-written',
        file: 'backend/',
        message: `The workbook marks ${table.name} as written, but no migration in backend/ creates it`,
      });
    } else if (!table.claimsWritten && table.ddl) {
      problems.push({
        severity: 'info',
        kind: 'migration-written-not-claimed',
        file: `backend/${table.ddl.file}`,
        message: `${table.name} is created by ${table.ddl.file} but the workbook does not mark it written`,
      });
    }
  }
}

/**
 * @param contractSchemas  the schema nodes from the contract index, so each
 *                         table can be linked to the schema it derives from and
 *                         its columns to the `$ref`s that schema declares
 */
export async function buildBackend(root, contractSchemas = []) {
  const dir = path.join(root, 'backend');
  const problems = [];

  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return { present: false, modules: [], tables: [], columns: {}, scaling: [], adrs: [], problems, stats: {} };
  }

  const copies = await findWorkbook(root);
  const workbook = copies[0] ?? null;
  const workbookName = workbook?.rel ?? null;

  // copies that disagree are worth saying out loud — one of them is stale, and
  // whichever folder you happen to open decides which numbers you believe
  for (const other of copies.slice(1)) {
    if (other.size === workbook.size) continue;
    problems.push({
      severity: 'warning',
      kind: 'backend-stale-workbook',
      file: other.rel,
      message:
        `${other.rel} is an older build of the schema workbook than ${workbook.rel} ` +
        `(${other.size} bytes against ${workbook.size}). Reading the newer one.`,
    });
  }

  // ---- ADRs ---------------------------------------------------------------
  const adrs = [];
  for (const entry of entries) {
    if (!entry.isFile() || !/\.md$/i.test(entry.name)) continue;
    const text = await readFile(path.join(dir, entry.name), 'utf8').catch(() => '');
    const heading = text.match(/^#\s+(.+)$/m)?.[1] ?? entry.name.replace(/\.md$/, '');
    const paragraphs = text
      .split(/\n\s*\n/)
      .map((p) => p.trim())
      .filter((p) => p && !p.startsWith('#') && !/^[-=*_\s]+$/.test(p));
    // the status line is metadata; the decision is the paragraph after it
    const decision = paragraphs.find((p) => !/^\*{0,2}status/i.test(p)) ?? paragraphs[0] ?? '';
    adrs.push({
      file: `backend/${entry.name}`,
      title: stripMarkdown(heading),
      status: text.match(/\*\*Status:\*\*\s*([^\n*]+)/i)?.[1]?.trim() ?? null,
      summary: stripMarkdown(decision).replace(/\s+/g, ' ').slice(0, 400),
      body: text,
    });
  }

  if (!workbookName) {
    problems.push({
      severity: 'info',
      kind: 'backend-no-schema',
      file: 'backend/',
      message: 'No .xlsx schema reference in backend/ — only the ADRs are shown',
    });
    return { present: true, file: null, note: [], modules: [], tables: [], columns: {}, scaling: [], adrs, problems, stats: {} };
  }

  // ---- the workbook -------------------------------------------------------
  let sheets;
  try {
    sheets = readWorkbook(await readFile(path.join(root, workbookName)));
  } catch (err) {
    problems.push({
      severity: 'error',
      kind: 'backend-unreadable',
      file: workbookName,
      message: `Could not read the schema workbook: ${err.message}`,
    });
    return { present: true, file: workbookName, note: [], modules: [], tables: [], columns: {}, scaling: [], adrs, problems, stats: {} };
  }

  const sheet = (name) => sheets.get(name) ?? [];
  const note = preamble(sheet('Read me'), 8);

  const moduleRows = table(sheet('Modules'), ['Module', 'Tables', 'Columns'],
    ['Migration', 'Status', 'Written']).rows;
  const tableRows = table(sheet('Tables'), ['Module', 'Table', 'Columns'],
    ['Child of', 'Derived from', 'Migration', 'Written']).rows;
  const columnRows = table(sheet('Columns'), ['Table', 'Column', 'Type'],
    ['Required', 'Source', 'Description']).rows;
  const scalingRows = table(sheet('Scaling'), ['Contract', 'Writes'],
    ['Primary reads', 'Replica reads', 'Analytical reads']).rows;
  // added in the 14 August rebuild: the schemas that deliberately have no table
  const noTableRows = table(sheet('No table'), ['Contract', 'Schema'],
    ['Why there is no table']).rows;

  for (const [name, result] of [
    ['Modules', table(sheet('Modules'), ['Module', 'Tables', 'Columns'])],
    ['Tables', table(sheet('Tables'), ['Module', 'Table', 'Columns'])],
    ['Columns', table(sheet('Columns'), ['Table', 'Column', 'Type'])],
  ]) {
    if (result.missing) {
      problems.push({
        severity: 'error',
        kind: 'backend-sheet-unreadable',
        file: workbookName,
        message: `The ${name} sheet has no recognisable header row — the workbook layout has changed`,
      });
    }
  }

  const modules = moduleRows
    .filter((r) => r.Module && !/^total$/i.test(r.Module))
    .map((r) => ({
      name: r.Module,
      tables: number(r.Tables),
      columns: number(r.Columns),
      migration: r.Migration || null,
      status: r.Status || null,
      // "Derivable. Not written" also contains the word written, so the
      // negative has to be excluded before the positive is tested
      written: /\bwritten\b/i.test(r.Status ?? '') && !/\bnot\s+written\b/i.test(r.Status ?? ''),
    }));

  // ---- link each table back to the contract schema it derives from --------
  const byName = new Map();
  for (const schema of contractSchemas) {
    if (!byName.has(schema.name)) byName.set(schema.name, []);
    byName.get(schema.name).push(schema);
  }

  const resolveSchema = (derivedFrom) => {
    if (!derivedFrom) return null;
    // a child table names the property it came from — subscription.Invoice.lines[]
    // — so anything after the schema is trimmed back to the schema itself
    const path = derivedFrom.replace(/\[\]$/, '').split('.');
    const parts = path.length > 2 ? path.slice(0, 2) : path;
    const name = parts[parts.length - 1];
    const contract = parts.length > 1 ? parts[parts.length - 2] : null;
    const candidates = byName.get(name);
    if (!candidates?.length) return null;
    // several contracts can declare the same schema name, so prefer the one
    // whose file matches the module the workbook names
    const exact = contract
      ? candidates.find((c) => c.file.split('/').pop().replace(/\.ya?ml$/, '') === contract)
      : null;
    return exact ?? candidates[0];
  };

  const tables = tableRows
    .filter((r) => r.Table && !/^total$/i.test(r.Table))
    .map((r) => {
      const source = r['Derived from'] || null;
      // 16 of the 213 tables exist for storage reasons and name no schema —
      // the cell holds an explanation rather than a schema, so it is not a miss
      const storageOnly = !source || /^\s*storage[- ]only\b/i.test(source);
      const derivedFrom = storageOnly ? null : source;
      const schema = resolveSchema(derivedFrom);
      return {
        module: r.Module,
        name: r.Table,
        columns: number(r.Columns),
        childOf: r['Child of'] || null,
        derivedFrom,
        storageOnly,
        storageReason: storageOnly ? source : null,
        migration: r.Migration || null,
        // the rebuild added this column; the SQL in backend/ is checked against it
        claimsWritten: /^(yes|y|true|✓|written)$/i.test(r.Written ?? ''),
        schemaId: schema?.id ?? null,
        schemaFile: schema?.file ?? null,
      };
    });

  const known = new Set(tables.map((t) => t.name));
  for (const t of tables) {
    if (t.childOf && !known.has(t.childOf)) {
      problems.push({
        severity: 'warning',
        kind: 'backend-unknown-parent',
        file: workbookName,
        message: `${t.name} is a child of ${t.childOf}, which is not in the table list`,
      });
    }
    if (t.derivedFrom && !t.schemaId && contractSchemas.length) {
      problems.push({
        severity: 'warning',
        kind: 'backend-schema-not-found',
        file: workbookName,
        message: `${t.name} derives from ${t.derivedFrom}, which no contract declares as a schema`,
      });
    }
  }

  // ---- columns, grouped by their table ------------------------------------
  const columns = {};
  for (const r of columnRows) {
    if (!r.Table || !r.Column) continue;
    (columns[r.Table] ??= []).push({
      name: r.Column,
      type: r.Type || 'unknown',
      required: /^(yes|true|y)$/i.test(r.Required ?? ''),
      source: r.Source || null,
      description: r.Description || '',
    });
  }
  for (const t of tables) {
    // a partition child inherits its parent's columns and legitimately has none
    if (!columns[t.name] && !t.storageOnly) {
      problems.push({
        severity: 'info',
        kind: 'backend-no-columns',
        file: workbookName,
        message: `${t.name} has no rows on the Columns sheet`,
      });
    }
  }

  // the sheet carries explanatory prose below the table, which lands in the
  // first column — a row is only data if all four counts are numbers
  const scaling = scalingRows
    .filter((r) => r.Contract && !/^total$/i.test(r.Contract))
    .map((r) => ({
      contract: r.Contract,
      writes: number(r.Writes),
      primaryReads: number(r['Primary reads']),
      replicaReads: number(r['Replica reads']),
      analyticalReads: number(r['Analytical reads']),
    }))
    .filter((r) => [r.writes, r.primaryReads, r.replicaReads, r.analyticalReads].every((n) => n !== null));

  addReferences(tables, columns, contractSchemas);
  const migrations = await buildMigrations(root);
  // the DDL is read first so its keys can teach the name matching: venue_id
  // resolves to platform.scope_node because a migration says so, not because
  // a table happens to be called venue — there is none, and never will be
  addForeignKeys(tables, columns, problems, workbookName, migrations);
  applyMigrations(tables, columns, migrations, problems);
  problems.push(...migrations.problems);

  // "why is there no table for this schema" — keyed by contract schema name,
  // so the contracts layer can answer it on the schema itself
  const notPersisted = {};
  for (const row of noTableRows) {
    if (!row.Schema) continue;
    notPersisted[`${row.Contract}.${row.Schema}`] = {
      contract: row.Contract,
      schema: row.Schema,
      reason: row['Why there is no table'] || 'not stated',
    };
  }

  const columnCount = Object.values(columns).reduce((a, list) => a + list.length, 0);

  return {
    present: true,
    file: workbookName,
    note,
    modules,
    tables,
    columns,
    scaling,
    adrs,
    migrations,
    notPersisted,
    problems,
    stats: {
      modules: modules.length,
      tables: tables.length,
      columns: columnCount,
      written: modules.filter((m) => m.written).length,
      linked: tables.filter((t) => t.schemaId).length,
      childTables: tables.filter((t) => t.childOf).length,
      references: tables.reduce((a, t) => a + (t.references?.length ?? 0), 0),
      foreignKeys: tables.reduce((a, t) => a + (t.foreignKeys?.length ?? 0), 0),
      // what the DDL actually creates, as opposed to what is planned
      inDdl: tables.filter((t) => t.ddl).length,
      ddlKeys: tables.reduce((a, t) => a + (t.keys?.length ?? 0), 0),
      migrationFiles: migrations.stats.files ?? 0,
      notPersisted: Object.keys(notPersisted).length,
    },
  };
}
