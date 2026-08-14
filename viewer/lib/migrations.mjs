// Reads the versioned SQL in backend/ — the DDL the workbook only describes.
//
// This matters more than it looks. Every relationship in the Data view was
// either declared in a contract as a `$ref` (11 of them) or inferred from a
// column name (244). A `REFERENCES` clause is neither: it is the database
// saying what is true. Where a migration covers a table, its keys replace the
// guesses entirely.
//
// The parser is deliberately small. It reads the subset of DDL these files
// use and ignores the rest rather than pretending to be a SQL parser.

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

/** Strip comments and string bodies so keywords inside them are not parsed. */
function scrub(sql) {
  return sql
    .replace(/\/\*[\s\S]*?\*\//g, ' ')
    .replace(/--[^\n]*/g, ' ')
    // a comment string can contain the word FOREIGN KEY, and one of them does
    .replace(/'(?:[^']|'')*'/g, "''");
}

/** Split on top-level separators, ignoring anything inside parentheses. */
function splitTopLevel(text, separator) {
  const out = [];
  let depth = 0;
  let start = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === '(') depth++;
    else if (ch === ')') depth--;
    else if (ch === separator && depth === 0) {
      out.push(text.slice(start, i));
      start = i + 1;
    }
  }
  out.push(text.slice(start));
  return out.map((s) => s.trim()).filter(Boolean);
}

const qualify = (name, fallbackSchema) => {
  const clean = String(name).replace(/"/g, '').trim();
  return clean.includes('.') ? clean : `${fallbackSchema}.${clean}`;
};

/** The (a, b) after a keyword, as a list of names. */
const columnList = (text) =>
  text.replace(/^\(|\)$/g, '').split(',').map((c) => c.trim().replace(/"/g, '')).filter(Boolean);

const REFERENCES = /\bREFERENCES\s+([\w".]+)\s*(\([^)]*\))?/i;

function parseCreateTable(statement, file) {
  // a partition child inherits its parent's columns and has no list of its own
  const child = statement.match(
    /CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w".]+)\s+PARTITION\s+OF\s+([\w".]+)([\s\S]*)$/i
  );
  if (child) {
    const name = String(child[1]).replace(/"/g, '');
    return {
      name,
      schema: name.includes('.') ? name.split('.')[0] : 'public',
      file,
      columns: [],
      foreignKeys: [],
      primaryKey: [],
      unique: [],
      checks: 0,
      partitionBy: null,
      partitionOf: String(child[2]).replace(/"/g, ''),
      forValues: child[3].match(/FOR\s+VALUES\s+([^;]+)/i)?.[1]?.trim() ?? null,
    };
  }

  const head = statement.match(/CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w".]+)\s*\(/i);
  if (!head) return null;

  const open = statement.indexOf('(', head.index + head[0].length - 1);
  let depth = 0;
  let close = -1;
  for (let i = open; i < statement.length; i++) {
    if (statement[i] === '(') depth++;
    else if (statement[i] === ')' && --depth === 0) { close = i; break; }
  }
  if (close < 0) return null;

  const name = String(head[1]).replace(/"/g, '');
  const schema = name.includes('.') ? name.split('.')[0] : 'public';
  const tail = statement.slice(close + 1);

  const table = {
    name,
    schema,
    file,
    columns: [],
    foreignKeys: [],
    primaryKey: [],
    unique: [],
    checks: 0,
    partitionBy: tail.match(/PARTITION\s+BY\s+(\w+)\s*\(([^)]*)\)/i)?.slice(1).join(' ') ?? null,
    partitionOf: statement.match(/PARTITION\s+OF\s+([\w".]+)/i)?.[1] ?? null,
  };

  for (const part of splitTopLevel(statement.slice(open + 1, close), ',')) {
    const constraint = part.replace(/^CONSTRAINT\s+[\w".]+\s+/i, '');

    if (/^FOREIGN\s+KEY/i.test(constraint)) {
      const columns = columnList(constraint.match(/FOREIGN\s+KEY\s*(\([^)]*\))/i)?.[1] ?? '');
      const reference = constraint.match(REFERENCES);
      if (reference) {
        table.foreignKeys.push({
          columns,
          toTable: qualify(reference[1], schema),
          toColumns: reference[2] ? columnList(reference[2]) : [],
          onDelete: constraint.match(/ON\s+DELETE\s+(\w+(?:\s+\w+)?)/i)?.[1] ?? null,
          composite: columns.length > 1,
        });
      }
      continue;
    }
    if (/^PRIMARY\s+KEY/i.test(constraint)) {
      table.primaryKey = columnList(constraint.match(/\(([^)]*)\)/)?.[0] ?? '');
      continue;
    }
    if (/^UNIQUE/i.test(constraint)) {
      table.unique.push(columnList(constraint.match(/\(([^)]*)\)/)?.[0] ?? ''));
      continue;
    }
    if (/^(CHECK|EXCLUDE|LIKE)\b/i.test(constraint)) { table.checks++; continue; }

    // otherwise it is a column definition
    const column = part.match(/^([\w"]+)\s+([\s\S]+)$/);
    if (!column) continue;
    const columnName = column[1].replace(/"/g, '');
    const rest = column[2];
    const reference = rest.match(REFERENCES);

    table.columns.push({
      name: columnName,
      type: rest.split(/\s+/)[0].replace(/,$/, ''),
      notNull: /\bNOT\s+NULL\b/i.test(rest),
      primaryKey: /\bPRIMARY\s+KEY\b/i.test(rest),
      generated: /\bGENERATED\s+ALWAYS\s+AS\b/i.test(rest),
      references: reference ? qualify(reference[1], schema) : null,
    });
    if (/\bPRIMARY\s+KEY\b/i.test(rest)) table.primaryKey.push(columnName);
    if (reference) {
      table.foreignKeys.push({
        columns: [columnName],
        toTable: qualify(reference[1], schema),
        toColumns: reference[2] ? columnList(reference[2]) : [],
        onDelete: rest.match(/ON\s+DELETE\s+(\w+(?:\s+\w+)?)/i)?.[1] ?? null,
        composite: false,
      });
    }
  }
  return table;
}

/**
 * @returns the tables the DDL actually creates, keyed by qualified name,
 *          plus what each migration file contributes
 */
export async function buildMigrations(root) {
  const dir = path.join(root, 'backend');
  const problems = [];
  const empty = {
    present: false, files: [], tables: {}, types: [], schemas: [],
    problems, stats: { files: 0, tables: 0, foreignKeys: 0 },
  };

  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return empty;
  }

  const sqlFiles = entries
    .filter((e) => e.isFile() && /\.sql$/i.test(e.name))
    .map((e) => e.name)
    .sort();
  if (!sqlFiles.length) return empty;

  const tables = {};
  const types = [];
  const schemas = new Set();
  const files = [];

  for (const name of sqlFiles) {
    const raw = await readFile(path.join(dir, name), 'utf8').catch(() => '');
    const sql = scrub(raw);
    const statements = splitTopLevel(sql, ';');

    const file = {
      name,
      // V0003a__scope-typing.sql -> V0003a, scope typing
      version: name.match(/^(V[\w]+?)__/i)?.[1] ?? name,
      title: (name.match(/__(.+)\.sql$/i)?.[1] ?? '').replace(/[-_]/g, ' '),
      tables: [],
      policies: 0,
      rlsTables: [],
      lines: raw.split(/\r?\n/).length,
    };

    for (const statement of statements) {
      if (/^\s*CREATE\s+TABLE\b/i.test(statement)) {
        const table = parseCreateTable(statement, name);
        if (!table) continue;
        if (tables[table.name]) {
          problems.push({
            severity: 'warning',
            kind: 'migration-duplicate-table',
            file: `backend/${name}`,
            message: `${table.name} is created in both ${tables[table.name].file} and ${name}`,
          });
        }
        tables[table.name] = table;
        file.tables.push(table.name);
        schemas.add(table.schema);
        continue;
      }

      const alter = statement.match(/^\s*ALTER\s+TABLE\s+(?:ONLY\s+)?([\w".]+)([\s\S]*)$/i);
      if (alter) {
        const target = String(alter[1]).replace(/"/g, '');
        const body = alter[2];
        const table = tables[target];

        if (/ROW\s+LEVEL\s+SECURITY/i.test(body)) {
          if (table) {
            table.rls = table.rls ?? {};
            if (/\bENABLE\b/i.test(body)) table.rls.enabled = true;
            if (/\bFORCE\b/i.test(body)) table.rls.forced = true;
          }
          if (!file.rlsTables.includes(target)) file.rlsTables.push(target);
          continue;
        }
        if (/FOREIGN\s+KEY/i.test(body) && table) {
          const columns = columnList(body.match(/FOREIGN\s+KEY\s*(\([^)]*\))/i)?.[1] ?? '');
          const reference = body.match(REFERENCES);
          if (reference) {
            table.foreignKeys.push({
              columns,
              toTable: qualify(reference[1], table.schema),
              toColumns: reference[2] ? columnList(reference[2]) : [],
              onDelete: body.match(/ON\s+DELETE\s+(\w+(?:\s+\w+)?)/i)?.[1] ?? null,
              composite: columns.length > 1,
              addedLater: true,
            });
          }
        }
        continue;
      }

      if (/^\s*CREATE\s+POLICY\b/i.test(statement)) { file.policies++; continue; }
      if (/^\s*CREATE\s+SCHEMA\b/i.test(statement)) {
        const name = statement.match(/CREATE\s+SCHEMA\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w"]+)/i)?.[1];
        if (name) schemas.add(name.replace(/"/g, ''));
        continue;
      }
      if (/^\s*CREATE\s+TYPE\b/i.test(statement)) {
        const name = statement.match(/CREATE\s+TYPE\s+([\w".]+)/i)?.[1];
        const values = statement.match(/AS\s+ENUM\s*\(([\s\S]*)\)/i)?.[1];
        if (name) {
          types.push({
            name: name.replace(/"/g, ''),
            file: name,
            values: values ? values.split(',').map((v) => v.trim().replace(/''/g, '')).filter(Boolean).length : 0,
          });
        }
      }
    }
    files.push(file);
  }

  // a key pointing at a table no migration creates would fail on apply
  for (const table of Object.values(tables)) {
    for (const key of table.foreignKeys) {
      if (!tables[key.toTable]) {
        problems.push({
          severity: 'error',
          kind: 'migration-dangling-key',
          file: `backend/${table.file}`,
          message: `${table.name}.${key.columns.join(', ')} references ${key.toTable}, which no migration creates`,
        });
      }
    }
  }

  const foreignKeys = Object.values(tables).reduce((a, t) => a + t.foreignKeys.length, 0);

  return {
    present: true,
    files,
    tables,
    types,
    schemas: [...schemas].sort(),
    problems,
    stats: {
      files: files.length,
      tables: Object.keys(tables).length,
      foreignKeys,
      composite: Object.values(tables).reduce(
        (a, t) => a + t.foreignKeys.filter((k) => k.composite).length, 0),
      partitioned: Object.values(tables).filter((t) => t.partitionBy).length,
      rls: Object.values(tables).filter((t) => t.rls?.enabled).length,
      forced: Object.values(tables).filter((t) => t.rls?.forced).length,
      policies: files.reduce((a, f) => a + f.policies, 0),
      generated: Object.values(tables).reduce(
        (a, t) => a + t.columns.filter((c) => c.generated).length, 0),
      types: types.length,
    },
  };
}
