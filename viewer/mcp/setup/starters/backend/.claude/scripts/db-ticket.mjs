#!/usr/bin/env node
/**
 * Checks a [DB] ticket's migration quickly, and says MATCH or what differs.
 *
 *     node .claude/scripts/db-ticket.mjs <ticket>             one ticket (pull it first)
 *     node .claude/scripts/db-ticket.mjs <ticket> --file db/tenant/V0027__access.sql
 *     node .claude/scripts/db-ticket.mjs --full tenant        every file from an empty database
 *
 * For one ticket it:
 *   1. keeps a template database at the state before the ticket's file: every earlier file in
 *      db/<database>/, applied once and reused until one of them changes;
 *   2. copies it (CREATE DATABASE ... TEMPLATE) and applies only the ticket's file, the way
 *      SqlMigrationRunner does: one transaction, recorded in platform.schema_version;
 *   3. runs it a second time, which must apply nothing and change nothing;
 *   4. compares the ticket's tables with .adam/work/<ticket>/expected-schema.json (written by
 *      adam_pull from the package DDL): columns, types, nullability, defaults, keys, checks,
 *      indexes, row-level security and partitioning.
 * MATCH is the evidence for done. The result is also written to .adam/work/<ticket>/db-check.md.
 *
 * --full applies every file to an empty database, runs them all a second time, and compares
 * every pulled ticket's expected-schema.json for that database. That is the once-a-day check,
 * with dotnet build and dotnet test; a ticket does not need it.
 *
 * Needs Docker Desktop running. PostgreSQL runs in its own container (adam-db-check,
 * pgvector/pgvector:pg16, no port published), so it never clashes with a database you already
 * run. --container <name> uses another running container instead (user postgres).
 * Exit code: 0 match, 1 a difference or a failed apply, 2 cannot run (no Docker, no ticket file).
 */

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const IMAGE = 'pgvector/pgvector:pg16';

// ---- normalising: the DDL's spelling and the catalog's, made one ----------------------------

const TYPE_ALIASES = [
  [/^timestamptz$/, 'timestamp with time zone'],
  [/^timestamp$/, 'timestamp without time zone'],
  [/^timestamp\((\d+)\)$/, 'timestamp($1) without time zone'],
  [/^timestamptz\((\d+)\)$/, 'timestamp($1) with time zone'],
  [/^timetz$/, 'time with time zone'],
  [/^time$/, 'time without time zone'],
  [/^(int|int4)$/, 'integer'],
  [/^int8$/, 'bigint'],
  [/^int2$/, 'smallint'],
  [/^bool$/, 'boolean'],
  [/^varchar$/, 'character varying'],
  [/^varchar\((\d+)\)$/, 'character varying($1)'],
  [/^char$/, 'character(1)'],
  [/^character$/, 'character(1)'],
  [/^char\((\d+)\)$/, 'character($1)'],
  [/^decimal/, 'numeric'],
  [/^(float8|float)$/, 'double precision'],
  [/^float4$/, 'real'],
  [/^public\./, ''],
];

export function normType(type) {
  if (type === null || type === undefined) return null;
  let t = String(type).replace(/"/g, '').trim().toLowerCase().replace(/\s+/g, ' ').replace(/\s*\(\s*/g, '(')
    .replace(/\s*,\s*/g, ',').replace(/\s*\)/g, ')');
  let dims = '';
  while (/\[\d*\]$/.test(t)) { dims += '[]'; t = t.replace(/\s*\[\d*\]$/, ''); }
  for (const [rx, to] of TYPE_ALIASES) t = t.replace(rx, to);
  return t + dims;
}

const CAST = /::\s*"?[a-z_][\w.]*"?(?:\s+(?:with|without|varying|precision|time|zone))*(?:\(\d+(?:,\s*\d+)?\))?(?:\[\])*/gi;

/** Outer parentheses that wrap the whole expression, removed. */
function unwrap(s) {
  let out = s.trim();
  for (;;) {
    if (!out.startsWith('(') || !out.endsWith(')')) return out;
    let depth = 0;
    let whole = true;
    for (let i = 0; i < out.length; i++) {
      if (out[i] === '(') depth++;
      else if (out[i] === ')') depth--;
      if (depth === 0 && i < out.length - 1) { whole = false; break; }
    }
    if (!whole) return out;
    out = out.slice(1, -1).trim();
  }
}

export function normDefault(value) {
  if (value === null || value === undefined) return null;
  let d = String(value).trim();
  if (/^null$/i.test(d)) return null;
  d = d.replace(CAST, '');
  d = unwrap(d);
  d = d.replace(/^'(-?\d+(?:\.\d+)?)'$/, '$1');
  // outside string literals: one case, no spaces
  return d.split(/('(?:[^']|'')*')/).map((part, i) => (i % 2 ? part : part.toLowerCase().replace(/\s+/g, ''))).join('');
}

export function normKeys(keys) {
  return String(keys ?? '').replace(CAST, '').replace(/"/g, '').toLowerCase().replace(/\s+/g, '')
    .replace(/\(\(([^()]*)\)\)/g, '($1)');
}

const normExpr = (s) => String(s ?? '').replace(CAST, '').replace(/["()\s]/g, '').toLowerCase();

const ON_DELETE = { a: null, r: 'RESTRICT', c: 'CASCADE', n: 'SET NULL', d: 'SET DEFAULT' };
const onDelete = (v) => (v === 'NO ACTION' ? null : v ?? null);
const list = (cols) => `(${(cols ?? []).join(', ')})`;

/** Index key text and the rest, from pg_get_indexdef. */
function indexParts(def) {
  const at = def.search(/ USING \w+ \(/);
  if (at < 0) return { keys: '', where: false };
  const open = def.indexOf('(', at);
  let depth = 0;
  let end = open;
  for (let i = open; i < def.length; i++) {
    if (def[i] === '(') depth++;
    else if (def[i] === ')' && --depth === 0) { end = i; break; }
  }
  return { keys: def.slice(open + 1, end), where: /\sWHERE\s/.test(def.slice(end)) };
}

// ---- comparing one table ----------------------------------------------------------------------

/**
 * What differs between a table's expected shape and the catalog's, in plain sentences.
 * `exists(name)` says whether a table is in the database: a foreign key to a table no migration
 * has created yet belongs to a later migration, and is listed as deferred instead.
 */
export function compareTable(name, expected, actual, exists = () => true) {
  const diffs = [];
  const deferred = [];
  if (!actual) return { diffs: [`${name}: the table is missing`], deferred };
  const say = (text) => diffs.push(`${name}: ${text}`);

  // columns
  const actualCols = new Map(actual.columns.map((c) => [c.name, c]));
  for (const c of expected.columns) {
    const a = actualCols.get(c.name);
    if (!a) { say(`column ${c.name} is missing`); continue; }
    actualCols.delete(c.name);
    if (normType(a.type) !== normType(c.type)) say(`column ${c.name} is ${a.type}; the package says ${c.type}`);
    if (Boolean(a.notNull) !== Boolean(c.notNull)) say(`column ${c.name} is ${a.notNull ? 'NOT NULL' : 'nullable'}; the package says ${c.notNull ? 'NOT NULL' : 'nullable'}`);
    if (!c.generated && normDefault(a.default) !== normDefault(c.default)) {
      say(`column ${c.name} defaults to ${a.default ?? 'nothing'}; the package says ${c.default ?? 'nothing'}`);
    }
  }
  for (const extra of actualCols.keys()) say(`column ${extra} is not in the package`);

  const cons = actual.constraints ?? [];
  // primary key
  const pk = cons.find((k) => k.type === 'p');
  const wantPk = expected.primaryKey?.columns ?? null;
  if (wantPk && !pk) say(`no primary key; the package says ${list(wantPk)}`);
  else if (!wantPk && pk) say(`primary key ${list(pk.columns)} is not in the package`);
  else if (wantPk && pk.columns.join(',') !== wantPk.join(',')) say(`primary key is ${list(pk.columns)}; the package says ${list(wantPk)}`);

  // unique constraints, by their columns
  const uniques = cons.filter((k) => k.type === 'u').map((k) => ({ ...k, key: k.columns.join(',') }));
  for (const u of expected.unique ?? []) {
    const at = uniques.findIndex((k) => k.key === u.columns.join(','));
    if (at < 0) { say(`unique ${list(u.columns)} is missing`); continue; }
    if (u.name && uniques[at].name !== u.name) say(`unique ${list(u.columns)} is named ${uniques[at].name}; the package says ${u.name}`);
    uniques.splice(at, 1);
  }
  for (const u of uniques) say(`unique ${u.name} ${list(u.columns)} is not in the package`);

  // foreign keys, by columns and target
  const fks = cons.filter((k) => k.type === 'f');
  for (const f of expected.foreignKeys ?? []) {
    const at = fks.findIndex((k) => k.columns.join(',') === f.columns.join(',') && k.references === f.references
      && (!f.refColumns?.length || (k.refColumns ?? []).join(',') === f.refColumns.join(',')));
    if (at < 0) {
      if (!exists(f.references)) deferred.push(`${name} ${list(f.columns)} -> ${f.references} (not created yet)`);
      else say(`foreign key ${list(f.columns)} -> ${f.references} is missing`);
      continue;
    }
    const k = fks[at];
    if (f.name && k.name !== f.name) say(`foreign key ${list(f.columns)} is named ${k.name}; the package says ${f.name}`);
    if (ON_DELETE[k.onDelete] !== onDelete(f.onDelete)) {
      say(`foreign key ${list(f.columns)} is ON DELETE ${ON_DELETE[k.onDelete] ?? 'NO ACTION'}; the package says ${f.onDelete ?? 'NO ACTION'}`);
    }
    fks.splice(at, 1);
  }
  for (const k of fks) say(`foreign key ${k.name} ${list(k.columns)} -> ${k.references} is not in the package`);

  // checks, by name
  const checks = new Set(cons.filter((k) => k.type === 'c').map((k) => k.name));
  for (const c of expected.checks ?? []) {
    if (!checks.delete(c.name)) say(`check ${c.name} is missing`);
  }
  for (const c of checks) say(`check ${c} is not in the package`);

  // indexes not behind a constraint, by name
  const indexes = new Map((actual.indexes ?? []).filter((i) => !i.constraint).map((i) => [i.name, i]));
  for (const i of expected.indexes ?? []) {
    const a = indexes.get(i.name);
    if (!a) { say(`index ${i.name} is missing`); continue; }
    indexes.delete(i.name);
    const parts = indexParts(a.def);
    if (Boolean(a.unique) !== Boolean(i.unique)) say(`index ${i.name} is ${a.unique ? '' : 'not '}unique; the package says ${i.unique ? '' : 'not '}unique`);
    if (a.method !== (i.method ?? 'btree')) say(`index ${i.name} uses ${a.method}; the package says ${i.method ?? 'btree'}`);
    if (normKeys(parts.keys) !== normKeys(i.keys)) say(`index ${i.name} is on (${parts.keys}); the package says (${i.keys})`);
    if (parts.where !== Boolean(i.where)) say(`index ${i.name} is ${parts.where ? 'partial' : 'not partial'}; the package says ${i.where ? `WHERE ${i.where}` : 'not partial'}`);
  }
  for (const extra of indexes.keys()) say(`index ${extra} is not in the package`);

  // row-level security
  const rls = actual.rls ?? {};
  const want = expected.rls ?? { enabled: false, forced: false, policies: [] };
  if (Boolean(rls.enabled) !== Boolean(want.enabled)) say(`row-level security is ${rls.enabled ? 'on' : 'off'}; the package says ${want.enabled ? 'on' : 'off'}`);
  if (Boolean(rls.forced) !== Boolean(want.forced)) say(`row-level security is ${rls.forced ? '' : 'not '}FORCEd; the package says ${want.forced ? 'FORCE' : 'not forced'}`);
  const policies = new Map((rls.policies ?? []).map((p) => [p.name, p]));
  for (const p of want.policies ?? []) {
    const a = policies.get(p.name);
    if (!a) { say(`policy ${p.name} is missing`); continue; }
    policies.delete(p.name);
    if (p.uses && !normExpr(a.using).includes(normExpr(p.uses))) say(`policy ${p.name} is USING ${a.using}; the package's uses ${p.uses}`);
  }
  for (const extra of policies.keys()) say(`policy ${extra} is not in the package`);

  // partitioning
  const partition = (v) => (v ? String(v).replace(/\s+/g, '').toLowerCase() : null);
  if (partition(actual.partitionBy) !== partition(expected.partitionBy)) {
    say(`partitioned by ${actual.partitionBy ?? 'nothing'}; the package says ${expected.partitionBy ?? 'not partitioned'}`);
  }
  if (Boolean(actual.defaultPartition) !== Boolean(expected.defaultPartition)) {
    say(`${actual.defaultPartition ? 'has' : 'has no'} default partition; the package says ${expected.defaultPartition ? 'one' : 'none'}`);
  }
  return { diffs, deferred };
}

/** Every expected table against the catalog. `created` are the tables the run made. */
export function compareSchema(expected, catalog, { created = [], exists = (t) => Boolean(catalog[t]) } = {}) {
  const diffs = [];
  const deferred = [];
  for (const [name, shape] of Object.entries(expected.tables ?? {})) {
    const r = compareTable(name, shape, catalog[name], exists);
    diffs.push(...r.diffs);
    deferred.push(...r.deferred);
  }
  for (const t of created) {
    if (!(t in (expected.tables ?? {}))) diffs.push(`${t}: created by this file, but not one of the ticket's tables`);
  }
  return { diffs, deferred };
}

// ---- the catalog ------------------------------------------------------------------------------

const quote = (s) => `'${String(s).replace(/'/g, "''")}'`;


const SYSTEM = "n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg\\_toast%' AND n.nspname NOT LIKE 'pg\\_temp%'";
const TABLE_NAMES = `SELECT n.nspname || '.' || c.relname AS name FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind IN ('r', 'p') AND NOT c.relispartition AND ${SYSTEM}`;

/**
 * The catalog's shape of `tables`, as one JSON object keyed by table name. With `alsoNew`, also
 * every table not in the temporary table adam_before: what the ticket's file created.
 */
export function catalogSql(tables, { alsoNew = false } = {}) {
  const names = tables.filter((t) => /^[a-z_][\w]*\.[a-z_][\w]*$/i.test(t)).map(quote).join(', ') || "''";
  return `
WITH t AS (
  SELECT c.oid, n.nspname || '.' || c.relname AS name, c.relkind, c.relrowsecurity, c.relforcerowsecurity
  FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind IN ('r', 'p') AND NOT c.relispartition AND ${SYSTEM}
    AND ((n.nspname || '.' || c.relname) = ANY (ARRAY[${names}]::text[])
      ${alsoNew ? 'OR (n.nspname || \'.\' || c.relname) NOT IN (SELECT name FROM adam_before)' : ''})
)
SELECT coalesce(json_object_agg(t.name, json_build_object(
  'columns', (SELECT coalesce(json_agg(json_build_object('name', a.attname, 'type', format_type(a.atttypid, a.atttypmod),
      'notNull', a.attnotnull, 'default', pg_get_expr(d.adbin, d.adrelid)) ORDER BY a.attnum), '[]')
    FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
    WHERE a.attrelid = t.oid AND a.attnum > 0 AND NOT a.attisdropped),
  'constraints', (SELECT coalesce(json_agg(json_build_object('name', k.conname, 'type', k.contype,
      'columns', (SELECT json_agg(att.attname ORDER BY u.ord) FROM unnest(k.conkey) WITH ORDINALITY u(num, ord)
                  JOIN pg_attribute att ON att.attrelid = k.conrelid AND att.attnum = u.num),
      'references', (SELECT rn.nspname || '.' || rc.relname FROM pg_class rc JOIN pg_namespace rn ON rn.oid = rc.relnamespace
                     WHERE rc.oid = k.confrelid),
      'refColumns', (SELECT json_agg(att.attname ORDER BY u.ord) FROM unnest(k.confkey) WITH ORDINALITY u(num, ord)
                     JOIN pg_attribute att ON att.attrelid = k.confrelid AND att.attnum = u.num),
      'onDelete', k.confdeltype) ORDER BY k.conname), '[]')
    FROM pg_constraint k WHERE k.conrelid = t.oid),
  'indexes', (SELECT coalesce(json_agg(json_build_object('name', ic.relname, 'unique', i.indisunique,
      'constraint', EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conindid = i.indexrelid AND k.conrelid = t.oid),
      'def', pg_get_indexdef(i.indexrelid), 'method', am.amname) ORDER BY ic.relname), '[]')
    FROM pg_index i JOIN pg_class ic ON ic.oid = i.indexrelid JOIN pg_am am ON am.oid = ic.relam WHERE i.indrelid = t.oid),
  'rls', json_build_object('enabled', t.relrowsecurity, 'forced', t.relforcerowsecurity,
    'policies', (SELECT coalesce(json_agg(json_build_object('name', p.polname, 'using', pg_get_expr(p.polqual, p.polrelid))
      ORDER BY p.polname), '[]') FROM pg_policy p WHERE p.polrelid = t.oid)),
  'partitionBy', CASE WHEN t.relkind = 'p' THEN pg_get_partkeydef(t.oid) END,
  'defaultPartition', EXISTS (SELECT 1 FROM pg_inherits h JOIN pg_class ch ON ch.oid = h.inhrelid
    WHERE h.inhparent = t.oid AND pg_get_expr(ch.relpartbound, ch.oid) = 'DEFAULT')
)), '{}'::json) FROM t`;
}

// ---- docker and psql --------------------------------------------------------------------------
//
// Every docker exec costs most of a second on Windows, so the work is done in as few psql
// sessions as it can be: one to read the template's state, one to copy it, one for the ticket.
// A session's answers come back as `TAG|value` lines; everything else it prints is ignored.

let CONTAINER = 'adam-db-check';

function docker(args, input) {
  const r = spawnSync('docker', args, { input, encoding: 'utf8', maxBuffer: 512 * 1024 * 1024, windowsHide: true });
  if (r.error) return { ok: false, out: '', err: r.error.code === 'ENOENT' ? 'docker is not installed or not on PATH' : r.error.message };
  return { ok: r.status === 0, out: r.stdout ?? '', err: (r.stderr ?? '').trim() };
}

function session(db, sql) {
  const r = docker(['exec', '-i', CONTAINER, 'psql', '-X', '-q', '-A', '-t', '-U', 'postgres', '-d', db,
    '-v', 'ON_ERROR_STOP=1', '-f', '-'], sql);
  const tags = {};
  for (const line of r.out.split(/\r?\n/)) {
    const m = /^([A-Z_]+)\|([\s\S]*)$/.exec(line);
    if (m) (tags[m[1]] ??= []).push(m[2]);
  }
  return { ok: r.ok, tags, err: r.err };
}

function firstError(text) {
  const lines = String(text).split(/\r?\n/).filter((l) => !/^(NOTICE|DETAIL: +\w+ .* will|HINT: +see)/.test(l));
  const at = lines.findIndex((l) => /ERROR|FATAL|error/.test(l));
  return (at >= 0 ? lines.slice(at, at + 4) : lines.slice(0, 4)).join('\n').trim() || 'failed with no message';
}

function must(result) {
  if (!result.ok) throw new Error(firstError(result.err));
  return result.tags;
}

const sleep = (ms) => new Promise((r) => { setTimeout(r, ms); });

class Usage extends Error {}

async function ensureContainer(named) {
  const state = docker(['inspect', '-f', '{{.State.Running}}', CONTAINER]);
  if (!state.ok) {
    if (/no such object/i.test(state.err)) {
      if (named) throw new Usage(`there is no container called ${CONTAINER}`);
      console.log(`Starting PostgreSQL 16 in a container called ${CONTAINER} (${IMAGE}; the first time downloads it)...`);
      const run = docker(['run', '-d', '--name', CONTAINER, '-e', 'POSTGRES_PASSWORD=adam-local', IMAGE]);
      if (!run.ok) throw new Usage(`could not start ${CONTAINER}: ${firstError(run.err)}`);
    } else {
      throw new Usage(`Docker is not running (${firstError(state.err)}). Start Docker Desktop and run this again.`);
    }
  } else if (state.out.trim() !== 'true') {
    const start = docker(['start', CONTAINER]);
    if (!start.ok) throw new Usage(`could not start ${CONTAINER}: ${firstError(start.err)}`);
  }
}

/** A session against `postgres` once the server answers; it may still be starting. */
async function ready(sql) {
  let last = null;
  for (let i = 0; i < 60; i++) {
    last = session('postgres', sql);
    if (last.ok) return last.tags;
    if (!/starting up|could not connect|No such file|is not running|the database system is/i.test(last.err)) break;
    await sleep(500);
  }
  throw new Usage(`PostgreSQL in ${CONTAINER} does not answer: ${firstError(last?.err ?? '')}`);
}

// ---- applying files the way SqlMigrationRunner does ------------------------------------------

const readSql = (file) => readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
const checksum = (text) => createHash('sha256').update(text, 'utf8').digest('hex').toUpperCase();

/**
 * SQL that applies `files` in one session, each in its own transaction and recorded in
 * platform.schema_version, as SqlMigrationRunner does. APPLY and DONE lines say how far it got.
 */
function applySql(files, folder) {
  return files.map((file) => {
    const sql = readSql(file);
    const name = path.basename(file);
    return `SELECT 'APPLY|' || ${quote(name)} || '|' || extract(epoch FROM clock_timestamp());\nBEGIN;\n${sql}\n;\n`
      + `INSERT INTO platform.schema_version (version, description, checksum, execution_ms) VALUES (${quote(name)}, `
      + `${quote(`applied from ${folder}`)}, ${quote(checksum(sql))}, 0);\nCOMMIT;\n`
      + `SELECT 'DONE|' || ${quote(name)} || '|' || extract(epoch FROM clock_timestamp());\n`;
  }).join('');
}

/** What a failed apply session got to, in words. */
function applyFailure(result) {
  const started = result.tags.APPLY ?? [];
  const done = new Set((result.tags.DONE ?? []).map((l) => l.split('|')[0]));
  const stuck = started.map((l) => l.split('|')[0]).find((n) => !done.has(n));
  return `${stuck ?? 'the session'} did not apply:\n${firstError(result.err)}`;
}

/** The runner's second pass: every file recorded with the checksum it has now applies nothing. */
function secondRunSql(files) {
  const rows = files.map((f) => `(${quote(path.basename(f))}, ${quote(checksum(readSql(f)))})`).join(', ');
  return `SELECT 'AGAIN|' || w.version || '|' || CASE
    WHEN to_regclass('platform.schema_version') IS NULL THEN 'unrecorded'
    WHEN NOT EXISTS (SELECT 1 FROM platform.schema_version s WHERE s.version = w.version) THEN 'unrecorded'
    WHEN EXISTS (SELECT 1 FROM platform.schema_version s WHERE s.version = w.version AND upper(s.checksum) = w.checksum) THEN 'skipped'
    ELSE 'changed' END
  FROM (VALUES ${rows}) AS w(version, checksum);\n`;
}

function secondRunProblems(tags) {
  return (tags.AGAIN ?? []).map((l) => l.split('|')).filter(([, s]) => s !== 'skipped').map(([name, s]) => (s === 'unrecorded'
    ? `second run: ${name} is not recorded in platform.schema_version, so a second run would apply it again`
    : `second run: ${name} is recorded with another checksum, so a second run would refuse it`));
}

const ordinal = (a, b) => (a < b ? -1 : a > b ? 1 : 0);
const sqlFiles = (dir) => (existsSync(dir) ? readdirSync(dir).filter((f) => /\.sql$/i.test(f)).sort(ordinal) : []);

/**
 * The template database at the state before the ticket's file: reused as it is, extended by the
 * files added since, or rebuilt from empty when an earlier file changed. What it holds (each
 * file's name and checksum) is kept in its comment.
 */
async function ensureBase(database, dir, files, folder) {
  const base = `adam_base_${database}`;
  const want = files.map((f) => ({ name: f, sha: checksum(readSql(path.join(dir, f))) }));
  const tags = await ready(`SELECT 'BASE|' || coalesce((SELECT coalesce(shobj_description(oid, 'pg_database'), '[]') FROM pg_database WHERE datname = ${quote(base)}), '');\n`);
  const comment = tags.BASE?.[0] ?? '';
  let have = null;
  try { have = comment ? JSON.parse(comment) : null; } catch { have = null; }
  const prefix = have && have.length <= want.length && have.every((h, i) => h.name === want[i].name && h.sha === want[i].sha);
  const from = prefix ? have.length : 0;
  const action = !prefix ? 'built' : from < want.length ? 'extended' : 'reused';
  if (!prefix) must(session('postgres', `DROP DATABASE IF EXISTS ${base} WITH (FORCE);\nCREATE DATABASE ${base};\n`));
  const started = Date.now();
  if (from < want.length) {
    const result = session(base, applySql(want.slice(from).map((w) => path.join(dir, w.name)), folder));
    const done = (result.tags.DONE ?? []).length;
    must(session('postgres', `COMMENT ON DATABASE ${base} IS ${quote(JSON.stringify(want.slice(0, from + done)))};\n`));
    if (!result.ok) throw new Error(`an earlier migration does not apply, so the previous state cannot be built: ${applyFailure(result)}`);
    must(session('postgres', `COMMENT ON DATABASE ${base} IS ${quote(JSON.stringify(want))};\n`));
  }
  return { base, action, applied: want.length - from, ms: Date.now() - started };
}

// ---- one ticket ---------------------------------------------------------------------------------

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--file' || a === '--container' || a === '--full') args[a.slice(2)] = argv[++i];
    else if (a === '--help' || a === '-h') args.help = true;
    else args._.push(a);
  }
  return args;
}

const secs = (ms) => `${(ms / 1000).toFixed(1)} s`;
const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;

async function ticket(root, key, args) {
  const work = path.join(root, '.adam', 'work', key);
  const expectedFile = path.join(work, 'expected-schema.json');
  if (!existsSync(expectedFile)) {
    throw new Usage(`${path.relative(root, expectedFile)} is missing. Pull the ticket first (adam_pull ${key}); `
      + 'a [DB] ticket whose subject names its migration file gets one.');
  }
  const expected = JSON.parse(readFileSync(expectedFile, 'utf8'));
  const database = expected.database ?? 'tenant';
  const folder = `db/${database}`;
  const dir = path.join(root, 'db', database);
  const file = args.file ? path.resolve(root, args.file) : path.join(dir, expected.migration);
  if (!existsSync(file)) {
    const number = /^(V\d+[A-Za-z]?)__/.exec(expected.migration ?? '')?.[1];
    const near = number ? sqlFiles(dir).filter((f) => f.startsWith(`${number}__`)) : [];
    throw new Usage(`${path.relative(root, file)} does not exist yet. Write it first`
      + `${near.length ? ` (found ${near.join(', ')}: rename it, or pass --file)` : ''}.`);
  }
  const name = path.basename(file);
  const all = sqlFiles(path.dirname(file));
  const earlier = all.filter((f) => f !== name && ordinal(f, name) < 0);
  const later = all.filter((f) => f !== name && ordinal(f, name) > 0);
  const tables = Object.keys(expected.tables ?? {});

  const started = Date.now();
  await ensureContainer(Boolean(args.container));
  const base = await ensureBase(database, path.dirname(file), earlier, folder);
  const db = `adam_ticket_${database}`;
  must(session('postgres', `DROP DATABASE IF EXISTS ${db} WITH (FORCE);\nCREATE DATABASE ${db} TEMPLATE ${base.base};\n`));

  const lines = [];
  const out = (s = '') => { lines.push(s); console.log(s); };
  out(`Ticket ${key}: ${path.relative(root, file).replace(/\\/g, '/')}`);
  out(`- previous state: ${plural(earlier.length, 'earlier file')} (template ${base.action}`
    + `${base.applied ? `, ${base.applied} applied in ${secs(base.ms)}` : ''})`
    + `${later.length ? `; ${plural(later.length, 'later file')} left out` : ''}`);

  // One session: note the tables there are, apply the file, run it again, read the catalog.
  const result = session(db, `CREATE TEMP TABLE adam_before AS ${TABLE_NAMES};\n`
    + applySql([file], folder)
    + secondRunSql([file])
    + `SELECT 'TABLES|' || coalesce(string_agg(name, ','), '') FROM (${TABLE_NAMES}) s;\n`
    + `SELECT 'NEW|' || coalesce(string_agg(name, ','), '') FROM (${TABLE_NAMES}) s WHERE name NOT IN (SELECT name FROM adam_before);\n`
    + `SELECT 'CATALOG|' || translate((${catalogSql(tables, { alsoNew: true })})::text, E'\\n\\r', '  ');\n`);

  let diffs = [];
  let deferred = [];
  let failed = null;
  if (!result.ok) {
    failed = applyFailure(result);
  } else {
    const [, t0] = (result.tags.APPLY?.[0] ?? '').split('|');
    const [, t1] = (result.tags.DONE?.[0] ?? '').split('|');
    out(`- first run: applied in ${secs((Number(t1) - Number(t0)) * 1000)}`);
    const again = secondRunProblems(result.tags);
    if (again.length) diffs.push(...again);
    else out('- second run: recorded in platform.schema_version with its checksum, so it applies nothing and changes nothing');
    const exists = new Set((result.tags.TABLES?.[0] ?? '').split(',').filter(Boolean));
    const created = (result.tags.NEW?.[0] ?? '').split(',').filter(Boolean);
    const catalog = JSON.parse(result.tags.CATALOG?.[0] || '{}');
    const r = compareSchema(expected, catalog, { created, exists: (t) => exists.has(t) });
    diffs.push(...r.diffs);
    deferred = r.deferred;
  }

  const count = tables.length;
  if (failed) {
    out(`FAILED: ${failed}`);
  } else if (diffs.length) {
    out(`DIFFERENT: ${plural(diffs.length, 'difference')} from expected-schema.json`);
    for (const d of diffs) out(`  - ${d}`);
  } else {
    out(`MATCH: ${plural(count, 'table')} as expected-schema.json says (columns, types, nullability, `
      + 'defaults, keys, checks, indexes, row-level security, partitioning)');
  }
  if (deferred.length) {
    out(`- left for a later migration (the table they point at is not created yet): ${plural(deferred.length, 'foreign key')}`);
    for (const d of deferred) out(`  - ${d}`);
  }
  if (expected.notInPackageDdl?.length) out(`- not checked (not in the package DDL): ${expected.notInPackageDdl.join(', ')}`);
  if (expected.notModelled?.length) out(`- not checked (DDL this check does not read): ${plural(expected.notModelled.length, 'statement')}; see expected-schema.json`);
  out(`- took ${secs(Date.now() - started)}. The database is left as ${db} in container ${CONTAINER} to look at.`);

  writeFileSync(path.join(work, 'db-check.md'), `# db-ticket check, ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}\n\n`
    + `File checksum (SHA-256): ${checksum(readSql(file))}\n\n${lines.join('\n')}\n`);
  return failed || diffs.length ? 1 : 0;
}

// ---- every file from empty ----------------------------------------------------------------------

async function full(root, database, args) {
  const dir = path.join(root, 'db', database);
  const folder = `db/${database}`;
  const files = sqlFiles(dir).map((f) => path.join(dir, f));
  if (!files.length) throw new Usage(`no .sql files in ${folder}`);
  const started = Date.now();
  await ensureContainer(Boolean(args.container));
  const db = `adam_full_${database}`;
  await ready(`DROP DATABASE IF EXISTS ${db} WITH (FORCE);\nCREATE DATABASE ${db};\n`);

  const work = path.join(root, '.adam', 'work');
  const pulled = (existsSync(work) ? readdirSync(work) : [])
    .filter((k) => existsSync(path.join(work, k, 'expected-schema.json')))
    .map((k) => ({ key: k, expected: JSON.parse(readFileSync(path.join(work, k, 'expected-schema.json'), 'utf8')) }))
    .filter((p) => (p.expected.database ?? 'tenant') === database);
  const tables = [...new Set(pulled.flatMap((p) => Object.keys(p.expected.tables ?? {})))];

  const result = session(db, applySql(files, folder) + secondRunSql(files)
    + `SELECT 'TABLES|' || coalesce(string_agg(name, ','), '') FROM (${TABLE_NAMES}) s;\n`
    + `SELECT 'CATALOG|' || translate((${catalogSql(tables)})::text, E'\\n\\r', '  ');\n`);
  let failed = null;
  const diffs = [];
  if (!result.ok) {
    failed = applyFailure(result);
  } else {
    console.log(`- first run: ${plural(files.length, 'file')} applied from empty in ${secs(Date.now() - started)}`);
    diffs.push(...secondRunProblems(result.tags));
    if (!diffs.length) console.log('- second run: every file recorded with its checksum, so it applies nothing');
    const exists = new Set((result.tags.TABLES?.[0] ?? '').split(',').filter(Boolean));
    const catalog = JSON.parse(result.tags.CATALOG?.[0] || '{}');
    for (const p of pulled) {
      const r = compareSchema(p.expected, catalog, { exists: (t) => exists.has(t) });
      diffs.push(...r.diffs.map((d) => `#${p.key} ${d}`));
      // A key left for later must exist once every file has run.
      diffs.push(...r.deferred.map((d) => `#${p.key} foreign key never created: ${d}`));
    }
    console.log(`- compared ${plural(tables.length, 'table')} from ${plural(pulled.length, 'pulled ticket')}`);
  }
  if (failed) console.log(`FAILED: ${failed}`);
  else if (diffs.length) { console.log(`DIFFERENT: ${plural(diffs.length, 'difference')}`); for (const d of diffs) console.log(`  - ${d}`); }
  else console.log(`MATCH: ${folder} applies from empty, a second run applies nothing, and every pulled table matches`);
  console.log(`- took ${secs(Date.now() - started)}. The database is left as ${db} in container ${CONTAINER}.`);
  return failed || diffs.length ? 1 : 0;
}

// ---- main ---------------------------------------------------------------------------------------

async function main(argv) {
  const args = parseArgs(argv);
  if (args.container) CONTAINER = args.container;
  const root = process.cwd();
  if (args.help || (!args._.length && !args.full)) {
    console.log('node .claude/scripts/db-ticket.mjs <ticket> [--file db/<database>/<file>.sql] [--container <name>]\n'
      + 'node .claude/scripts/db-ticket.mjs --full <tenant|control> [--container <name>]');
    return args.help ? 0 : 2;
  }
  try {
    if (args.full) return await full(root, args.full, args);
    return await ticket(root, String(args._[0]).replace(/^#/, ''), args);
  } catch (error) {
    console.log(error instanceof Usage ? `Cannot run: ${error.message}` : `FAILED: ${error.message}`);
    return error instanceof Usage ? 2 : 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
}
