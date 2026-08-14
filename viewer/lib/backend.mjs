// Reads backend/ — the database schema reference and the ADRs beside it.
//
// The schema reference is an .xlsx rather than YAML, so it is read directly
// instead of being converted: the spreadsheet stays the one source of truth and
// there is no generated copy to drift from it.
//
// The join that makes this worth drawing is the `Derived from` column. Every
// table names the contract schema it came from, so a table can be traced back to
// the API that defines it, and a contract schema with no table can be spotted.

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { readWorkbook } from './xlsx.mjs';

/**
 * Find the header row and map everything below it to objects.
 * The sheets carry a title and a note above the header, so a fixed row index
 * would break the first time someone adds a line of explanation.
 */
function table(rows, headers) {
  const wanted = headers.map((h) => h.toLowerCase());
  let headerRow = -1;

  for (let i = 0; i < rows.length; i++) {
    const cells = rows[i].map((c) => String(c ?? '').trim().toLowerCase());
    if (wanted.every((w) => cells.includes(w))) { headerRow = i; break; }
  }
  if (headerRow < 0) return { rows: [], missing: true };

  const cols = rows[headerRow].map((c) => String(c ?? '').trim().toLowerCase());
  const at = (row, name) => {
    const index = cols.indexOf(name.toLowerCase());
    return index < 0 ? '' : String(row[index] ?? '').trim();
  };

  const out = [];
  for (let i = headerRow + 1; i < rows.length; i++) {
    const row = rows[i];
    if (!row.some((c) => String(c ?? '').trim())) continue;
    const record = {};
    for (const header of headers) record[header] = at(row, header);
    out.push(record);
  }
  return { rows: out, missing: false };
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

  const workbookName = entries.find((e) => e.isFile() && /\.xlsx$/i.test(e.name))?.name ?? null;

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
    sheets = readWorkbook(await readFile(path.join(dir, workbookName)));
  } catch (err) {
    problems.push({
      severity: 'error',
      kind: 'backend-unreadable',
      file: `backend/${workbookName}`,
      message: `Could not read the schema workbook: ${err.message}`,
    });
    return { present: true, file: `backend/${workbookName}`, note: [], modules: [], tables: [], columns: {}, scaling: [], adrs, problems, stats: {} };
  }

  const sheet = (name) => sheets.get(name) ?? [];
  const note = preamble(sheet('Read me'), 8);

  const moduleRows = table(sheet('Modules'), ['Module', 'Tables', 'Columns', 'Migration', 'Status']).rows;
  const tableRows = table(sheet('Tables'), ['Module', 'Table', 'Columns', 'Child of', 'Derived from', 'Migration']).rows;
  const columnRows = table(sheet('Columns'), ['Table', 'Column', 'Type', 'Required', 'Source', 'Description']).rows;
  const scalingRows = table(sheet('Scaling'), ['Contract', 'Writes', 'Primary reads', 'Replica reads', 'Analytical reads']).rows;

  const modules = moduleRows
    .filter((r) => r.Module && !/^total$/i.test(r.Module))
    .map((r) => ({
      name: r.Module,
      tables: number(r.Tables),
      columns: number(r.Columns),
      migration: r.Migration || null,
      status: r.Status || null,
      // "Written and checked" is the only state that means the migration exists
      written: /written/i.test(r.Status ?? ''),
    }));

  // ---- link each table back to the contract schema it derives from --------
  const byName = new Map();
  for (const schema of contractSchemas) {
    if (!byName.has(schema.name)) byName.set(schema.name, []);
    byName.get(schema.name).push(schema);
  }

  const resolveSchema = (derivedFrom) => {
    if (!derivedFrom) return null;
    const parts = derivedFrom.split('.');
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
      const derivedFrom = r['Derived from'] || null;
      const schema = resolveSchema(derivedFrom);
      return {
        module: r.Module,
        name: r.Table,
        columns: number(r.Columns),
        childOf: r['Child of'] || null,
        derivedFrom,
        migration: r.Migration || null,
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
        file: `backend/${workbookName}`,
        message: `${t.name} is a child of ${t.childOf}, which is not in the table list`,
      });
    }
    if (t.derivedFrom && !t.schemaId && contractSchemas.length) {
      problems.push({
        severity: 'warning',
        kind: 'backend-schema-not-found',
        file: `backend/${workbookName}`,
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
    if (!columns[t.name]) {
      problems.push({
        severity: 'info',
        kind: 'backend-no-columns',
        file: `backend/${workbookName}`,
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

  const columnCount = Object.values(columns).reduce((a, list) => a + list.length, 0);

  return {
    present: true,
    file: `backend/${workbookName}`,
    note,
    modules,
    tables,
    columns,
    scaling,
    adrs,
    problems,
    stats: {
      modules: modules.length,
      tables: tables.length,
      columns: columnCount,
      written: modules.filter((m) => m.written).length,
      linked: tables.filter((t) => t.schemaId).length,
      childTables: tables.filter((t) => t.childOf).length,
      references: tables.reduce((a, t) => a + (t.references?.length ?? 0), 0),
    },
  };
}
