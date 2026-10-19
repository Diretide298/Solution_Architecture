#!/usr/bin/env node
/**
 * Checks a [DB] ticket's migration quickly, and says MATCH or what differs.
 *
 *     node .claude/scripts/db-ticket.mjs <ticket>             one ticket (pull it first)
 *     node .claude/scripts/db-ticket.mjs <ticket> --file db/tenant/V0027__access.sql
 *     node .claude/scripts/db-ticket.mjs --full tenant        every file from an empty database
 *     node .claude/scripts/db-ticket.mjs --clean              drop this folder's check databases
 *
 * For one ticket it:
 *   1. keeps a template database at the state before the ticket's file: every earlier file in
 *      db/<database>/, applied once and reused until one of them changes;
 *   2. copies it and applies only the ticket's file, the way SqlMigrationRunner does (one
 *      transaction, recorded in platform.schema_version);
 *   3. applies the file a second time on the result (not recorded): it must succeed and change nothing;
 *   4. copies the template again and applies the package's own statements for the ticket, from
 *      .adam/work/<ticket>/expected-schema.json (written by adam_pull);
 *   5. compares a snapshot of the whole database (every schema, table, column, constraint, index,
 *      policy, trigger, view, sequence, function and type, as PostgreSQL itself prints them) of the
 *      two copies. The ticket's objects must be what the package's statements make, and everything
 *      else must be exactly as it was before the file ran.
 * MATCH is the evidence for done. The result is also written to .adam/work/<ticket>/db-check.md.
 *
 * --full applies every file to an empty database and then every file a second time. Run it once
 * before opening the merge request.
 *
 * Each statement of a file is run through PL/pgSQL EXECUTE, so psql never reads it: no backslash
 * commands and no :variables, as with SqlMigrationRunner. A file must not BEGIN or COMMIT itself:
 * the runner already wraps each file in one transaction.
 *
 * Needs Docker Desktop running. PostgreSQL runs in its own container (adam-db-check,
 * pgvector/pgvector:pg16, no port published). --container <name> uses another container, which
 * must already be running; it is never started or stopped. Databases are named after this
 * folder, and one run at a time per folder holds a lock, so two folders or two agents never meet.
 * Exit code: 0 match, 1 a difference, a failed apply or a partial check, 2 cannot run.
 */

import { spawn, spawnSync } from 'node:child_process';
import { createHash, randomBytes } from 'node:crypto';
import { closeSync, existsSync, openSync, readFileSync, readdirSync, realpathSync, statSync, unlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const VERSION = 2; // a template built by another version is rebuilt
const IMAGE = 'pgvector/pgvector:pg16';

// ---- a file, split the way the server sees it -------------------------------------------------

/** The statements of a SQL file, as written, with the line each starts on. Comments stay in. */
export function splitSql(text) {
  const s = String(text ?? '');
  const out = [];
  let start = 0;
  let line = 1;
  let startLine = 1;
  let meaningful = false;
  const push = (end) => {
    const sql = s.slice(start, end).trim();
    if (sql && meaningful) out.push({ sql, line: startLine });
    meaningful = false;
  };
  for (let i = 0; i < s.length;) {
    const ch = s[i];
    const two = s.slice(i, i + 2);
    const begin = (to) => { for (let k = i; k < to && k < s.length; k++) if (s[k] === '\n') line++; i = to; };
    if (!meaningful && /\s/.test(ch)) { if (ch === '\n') line++; i++; startLine = line; start = i; continue; }
    if (two === '--') { const end = s.indexOf('\n', i); begin(end < 0 ? s.length : end); continue; }
    if (two === '/*') {
      let depth = 0;
      let j = i;
      for (; j < s.length; j++) {
        if (s.slice(j, j + 2) === '/*') { depth++; j++; } else if (s.slice(j, j + 2) === '*/') { depth--; j++; if (!depth) break; }
      }
      begin(j + 1);
      continue;
    }
    meaningful = true;
    if (ch === "'") {
      const escapes = /[eE]/.test(s[i - 1] ?? '') && !/\w/.test(s[i - 2] ?? '');
      let j = i + 1;
      for (; j < s.length; j++) {
        if (escapes && s[j] === '\\') { j++; continue; }
        if (s[j] === "'") { if (s[j + 1] === "'") { j++; continue; } break; }
      }
      begin(j + 1);
      continue;
    }
    if (ch === '"') { const end = s.indexOf('"', i + 1); begin(end < 0 ? s.length : end + 1); continue; }
    if (ch === '$') {
      const tag = /^\$(?:[A-Za-z_]\w*)?\$/.exec(s.slice(i, i + 64))?.[0];
      if (tag && !/\w/.test(s[i - 1] ?? '')) {
        const end = s.indexOf(tag, i + tag.length);
        begin(end < 0 ? s.length : end + tag.length);
        continue;
      }
    }
    if (ch === ';') { push(i); i++; start = i; startLine = line; continue; }
    if (ch === '\n') line++;
    i++;
  }
  push(s.length);
  return out;
}

const TRANSACTION = /^(?:(?:--[^\n]*\n|\/\*[\s\S]*?\*\/|\s)*)(BEGIN|COMMIT|ROLLBACK|START\s+TRANSACTION|END|SAVEPOINT|RELEASE|ABORT)\b\s*(?:TRANSACTION|WORK)?\s*$/i;

// ---- the snapshot: everything a migration can make, as PostgreSQL prints it --------------------

const OWN = "n.nspname NOT IN ('pg_catalog', 'information_schema') AND n.nspname NOT LIKE 'pg\\_%'";
const NOT_EXTENSION = "NOT EXISTS (SELECT 1 FROM pg_depend e WHERE e.objid = x.oid AND e.deptype = 'e')";

/** One JSON object: a key per object ("table a.t column c") and its definition. */
export const SNAPSHOT_SQL = `(SELECT coalesce(json_object_agg(k, v ORDER BY k), '{}'::json) FROM (
  SELECT 'schema ' || n.nspname AS k, '' AS v FROM pg_namespace n WHERE ${OWN}
  UNION ALL SELECT 'extension ' || extname, extversion FROM pg_extension
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname,
      x.relkind::text || ' rls ' || x.relrowsecurity::text || ' force ' || x.relforcerowsecurity::text
      || coalesce(' partition by ' || pg_get_partkeydef(x.oid), '')
    FROM pg_class x JOIN pg_namespace n ON n.oid = x.relnamespace
    WHERE ${OWN} AND x.relkind IN ('r', 'p') AND NOT x.relispartition AND ${NOT_EXTENSION}
  UNION ALL SELECT 'table ' || pn.nspname || '.' || p.relname || ' default partition ' || n.nspname || '.' || x.relname, ''
    FROM pg_class x JOIN pg_namespace n ON n.oid = x.relnamespace JOIN pg_inherits h ON h.inhrelid = x.oid
    JOIN pg_class p ON p.oid = h.inhparent JOIN pg_namespace pn ON pn.oid = p.relnamespace
    WHERE ${OWN} AND x.relispartition AND pg_get_expr(x.relpartbound, x.oid) = 'DEFAULT'
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname || ' column ' || a.attname,
      format_type(a.atttypid, a.atttypmod) || CASE WHEN a.attnotnull THEN ' not null' ELSE '' END
      || coalesce(' default ' || pg_get_expr(d.adbin, d.adrelid), '')
      || CASE a.attgenerated WHEN 's' THEN ' generated stored' ELSE '' END
      || CASE WHEN a.attidentity <> '' THEN ' identity ' || a.attidentity::text ELSE '' END
      || coalesce(' collate ' || (SELECT collname FROM pg_collation c WHERE c.oid = a.attcollation AND c.collname <> 'default'), '')
    FROM pg_attribute a JOIN pg_class x ON x.oid = a.attrelid JOIN pg_namespace n ON n.oid = x.relnamespace
    LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
    WHERE ${OWN} AND x.relkind IN ('r', 'p') AND NOT x.relispartition AND a.attnum > 0 AND NOT a.attisdropped AND ${NOT_EXTENSION}
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname || ' constraint ' || k.conname, pg_get_constraintdef(k.oid)
    FROM pg_constraint k JOIN pg_class x ON x.oid = k.conrelid JOIN pg_namespace n ON n.oid = x.relnamespace
    WHERE ${OWN} AND NOT x.relispartition
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname || ' index ' || i.relname, pg_get_indexdef(i.oid)
    FROM pg_index ix JOIN pg_class i ON i.oid = ix.indexrelid JOIN pg_class x ON x.oid = ix.indrelid
    JOIN pg_namespace n ON n.oid = x.relnamespace WHERE ${OWN} AND NOT x.relispartition
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname || ' policy ' || p.polname,
      CASE WHEN p.polpermissive THEN 'permissive' ELSE 'restrictive' END
      || ' for ' || CASE p.polcmd WHEN '*' THEN 'all' WHEN 'r' THEN 'select' WHEN 'a' THEN 'insert' WHEN 'w' THEN 'update' ELSE 'delete' END
      || ' to ' || coalesce((SELECT string_agg(CASE WHEN r = 0 THEN 'public' ELSE r::regrole::text END, ',' ORDER BY 1) FROM unnest(p.polroles) r), '')
      || ' using ' || coalesce(pg_get_expr(p.polqual, p.polrelid), '-')
      || ' with check ' || coalesce(pg_get_expr(p.polwithcheck, p.polrelid), '-')
    FROM pg_policy p JOIN pg_class x ON x.oid = p.polrelid JOIN pg_namespace n ON n.oid = x.relnamespace
    WHERE ${OWN} AND NOT x.relispartition
  UNION ALL SELECT 'table ' || n.nspname || '.' || x.relname || ' trigger ' || t.tgname, pg_get_triggerdef(t.oid)
    FROM pg_trigger t JOIN pg_class x ON x.oid = t.tgrelid JOIN pg_namespace n ON n.oid = x.relnamespace
    WHERE ${OWN} AND NOT t.tgisinternal AND NOT x.relispartition
  UNION ALL SELECT CASE x.relkind WHEN 'v' THEN 'view ' ELSE 'materialized view ' END || n.nspname || '.' || x.relname, pg_get_viewdef(x.oid)
    FROM pg_class x JOIN pg_namespace n ON n.oid = x.relnamespace WHERE ${OWN} AND x.relkind IN ('v', 'm') AND ${NOT_EXTENSION}
  UNION ALL SELECT 'sequence ' || n.nspname || '.' || x.relname,
      format('%s start %s increment %s cycle %s', s.seqtypid::regtype, s.seqstart, s.seqincrement, s.seqcycle)
    FROM pg_sequence s JOIN pg_class x ON x.oid = s.seqrelid JOIN pg_namespace n ON n.oid = x.relnamespace
    WHERE ${OWN} AND ${NOT_EXTENSION}
  UNION ALL SELECT 'function ' || x.oid::regprocedure::text, md5(pg_get_functiondef(x.oid))
    FROM pg_proc x JOIN pg_namespace n ON n.oid = x.pronamespace WHERE ${OWN} AND x.prokind IN ('f', 'p') AND ${NOT_EXTENSION}
  UNION ALL SELECT 'type ' || n.nspname || '.' || x.typname, x.typtype::text
      || coalesce(' ' || (SELECT string_agg(enumlabel, ',' ORDER BY enumsortorder) FROM pg_enum WHERE enumtypid = x.oid), '')
      || CASE WHEN x.typtype = 'd' THEN ' ' || format_type(x.typbasetype, x.typtypmod) ELSE '' END
    FROM pg_type x JOIN pg_namespace n ON n.oid = x.typnamespace
    WHERE ${OWN} AND x.typtype IN ('e', 'd', 'c') AND ${NOT_EXTENSION}
      AND (x.typtype <> 'c' OR (SELECT relkind FROM pg_class WHERE oid = x.typrelid) = 'c')
) s)`;

// ---- comparing snapshots --------------------------------------------------------------------------

const tableOf = (key) => /^table (\S+)/.exec(key)?.[1] ?? null;
const clip = (v) => (String(v).length > 300 ? `${String(v).slice(0, 297)}...` : String(v));

/** "a.t: column c" for a table's part, "a.t: the table" for the table, the key itself otherwise. */
export function label(key) {
  const m = /^table (\S+)(?: (.+))?$/.exec(key);
  if (!m) return key;
  return `${m[1]}: ${m[2] ?? 'the table'}`;
}

/**
 * What differs, in sentences. `before` is the copy before the file, `after` after it, `expected`
 * the copy with the package's statements. An object is the ticket's when it belongs to one of
 * `owned` (table names) or when the package's statements change it; everything else must be
 * exactly as it was before.
 */
export function diffSnapshots({ before, after, expected, owned = [] }) {
  const own = new Set(owned);
  const mine = (key) => own.has(tableOf(key)) || expected[key] !== before[key];
  const diffs = [];
  for (const key of [...new Set([...Object.keys(after), ...Object.keys(expected)])].sort()) {
    const a = after[key];
    const b = expected[key];
    if (a === b) continue;
    const s = before[key];
    if (mine(key)) {
      if (a === undefined) diffs.push(`${label(key)} is missing`);
      else if (b === undefined) diffs.push(`${label(key)} is not in the package`);
      else diffs.push(`${label(key)} is ${clip(a)}; the package has ${clip(b)}`);
    } else if (a === undefined) {
      diffs.push(`${label(key)} was dropped by this file, but it is not part of this ticket`);
    } else if (s === undefined) {
      diffs.push(`${label(key)} was created by this file, but it is not part of this ticket`);
    } else {
      diffs.push(`${label(key)} was changed by this file, but it is not part of this ticket (was ${clip(s)}; now ${clip(a)})`);
    }
  }
  return diffs;
}

/** What a second run changed. */
export function againDiffs(first, second) {
  const out = [];
  for (const key of [...new Set([...Object.keys(first), ...Object.keys(second)])].sort()) {
    if (first[key] === second[key]) continue;
    out.push(first[key] === undefined ? `the second run created ${label(key)}`
      : second[key] === undefined ? `the second run dropped ${label(key)}`
        : `the second run changed ${label(key)} (from ${clip(first[key])} to ${clip(second[key])})`);
  }
  return out;
}

// ---- docker and psql ---------------------------------------------------------------------------
//
// Every docker exec costs most of a second on Windows, so the work is done in few psql sessions.
// A session's answers come back as `<nonce>_TAG|value` lines (the nonce is new every run, so a
// file's own SELECT cannot pass for one); everything else it prints is ignored.

let CONTAINER = 'adam-db-check';
const NONCE = `n${randomBytes(5).toString('hex')}`;
const tag = (name, valueSql) => `SELECT '${NONCE}_${name}|' || ${valueSql};\n`;

class Usage extends Error {}

function docker(args, input) {
  const r = spawnSync('docker', args, { input, encoding: 'utf8', maxBuffer: 1024 * 1024 * 1024, windowsHide: true });
  if (r.error) return { ok: false, out: '', err: r.error.code === 'ENOENT' ? 'docker is not installed or not on PATH' : r.error.message };
  return { ok: r.status === 0, out: r.stdout ?? '', err: (r.stderr ?? '').trim() };
}

const psqlArgs = (db) => ['exec', '-i', CONTAINER, 'psql', '-X', '-q', '-A', '-t', '-U', 'postgres', '-d', db,
  '-v', 'ON_ERROR_STOP=1', '-f', '-'];

function session(db, sql) {
  return answers(docker(psqlArgs(db), sql));
}

/** The same, without waiting: the ticket's copy and the package's copy run side by side. */
function sessionAsync(db, sql) {
  return new Promise((resolve) => {
    const child = spawn('docker', psqlArgs(db), { windowsHide: true });
    const out = [];
    const err = [];
    child.stdout.on('data', (d) => out.push(d));
    child.stderr.on('data', (d) => err.push(d));
    child.on('error', (e) => resolve(answers({ ok: false, out: '', err: e.message })));
    child.on('close', (code) => resolve(answers({ ok: code === 0, out: Buffer.concat(out).toString('utf8'), err: Buffer.concat(err).toString('utf8').trim() })));
    child.stdin.on('error', () => { /* psql stopped reading: its exit says why */ });
    child.stdin.end(sql);
  });
}

function answers(r) {
  const tags = {};
  const prefix = `${NONCE}_`;
  for (const line of r.out.split(/\r?\n/)) {
    if (!line.startsWith(prefix)) continue;
    const bar = line.indexOf('|');
    (tags[line.slice(prefix.length, bar)] ??= []).push(line.slice(bar + 1));
  }
  const last = (name) => tags[name]?.[tags[name].length - 1];
  return { ok: r.ok, tags, last, err: r.err };
}

function firstError(text) {
  const lines = String(text).split(/\r?\n/)
    .filter((l) => l.trim() && !/^(NOTICE|DETAIL: +\w+ .* will|HINT: +see)/.test(l) && !/PL\/pgSQL function inline_code_block/.test(l))
    .map((l) => clip(l.replace(/^psql:<stdin>:\d+:\s*/, '')));
  const at = lines.findIndex((l) => /ERROR|FATAL|error/.test(l));
  return (at >= 0 ? lines.slice(at, at + 3) : lines.slice(0, 3)).join('\n').trim() || 'failed with no message';
}

function must(result) {
  if (!result.ok) throw new Error(firstError(result.err));
  return result;
}

const quote = (s) => `'${String(s).replace(/'/g, "''")}'`;
const sleep = (ms) => new Promise((r) => { setTimeout(r, ms); });

async function ensureContainer(named) {
  const state = docker(['inspect', '-f', '{{.State.Running}}', CONTAINER]);
  if (!state.ok) {
    if (!/no such object/i.test(state.err)) throw new Usage(`Docker is not running (${firstError(state.err)}). Start Docker Desktop and run this again.`);
    if (named) throw new Usage(`there is no container called ${CONTAINER}`);
    console.log(`Starting PostgreSQL 16 in a container called ${CONTAINER} (${IMAGE}; the first time downloads it)...`);
    const run = docker(['run', '-d', '--name', CONTAINER, '-e', 'POSTGRES_PASSWORD=adam-local', IMAGE]);
    if (!run.ok) throw new Usage(`could not start ${CONTAINER}: ${firstError(run.err)}`);
  } else if (state.out.trim() !== 'true') {
    // Someone else's container is theirs to start.
    if (named) throw new Usage(`the container ${CONTAINER} is not running; start it yourself, or leave out --container`);
    const start = docker(['start', CONTAINER]);
    if (!start.ok) throw new Usage(`could not start ${CONTAINER}: ${firstError(start.err)}`);
  }
}

/** A session against `postgres` once the server answers (it may still be starting). */
async function ready(sql) {
  let last = null;
  for (let i = 0; i < 60; i++) {
    last = session('postgres', `${tag('VERSION', 'current_setting(\'server_version_num\')')}${sql}`);
    if (last.ok) {
      if (Number(last.last('VERSION')) < 130000) throw new Usage(`${CONTAINER} runs PostgreSQL ${last.last('VERSION')}; this needs 13 or later`);
      return last;
    }
    if (!/starting up|could not connect|No such file|is not running|the database system is/i.test(last.err)) break;
    await sleep(500);
  }
  throw new Usage(`PostgreSQL in ${CONTAINER} does not answer: ${firstError(last?.err ?? '')}`);
}

// ---- running statements ----------------------------------------------------------------------

const readSql = (file) => readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
const checksum = (text) => createHash('sha256').update(text, 'utf8').digest('hex').toUpperCase();
const ordinal = (a, b) => (a < b ? -1 : a > b ? 1 : 0);
const sqlFiles = (dir) => (existsSync(dir) ? readdirSync(dir).filter((f) => /\.sql$/i.test(f)).sort(ordinal) : []);

/** A statement run through EXECUTE: psql only sees a dollar-quoted string. */
function execute(sql, condition = null) {
  let q = `${NONCE}q`;
  while (sql.includes(`$${q}$`)) q += 'x';
  const body = `EXECUTE $${q}$${sql}$${q}$;`;
  return `DO $${NONCE}$ BEGIN ${condition ? `IF ${condition} THEN ${body} END IF;` : body} END $${NONCE}$;\n`;
}

/**
 * SQL that runs one file's statements, as it is or recorded the way SqlMigrationRunner records it.
 * AT lines say which statement was running when one fails.
 */
function fileSql(file, folder, { record, label: which }) {
  const text = readSql(file);
  const name = path.basename(file);
  const statements = splitSql(text);
  const bad = statements.find((s) => TRANSACTION.test(s.sql));
  if (bad) throw new Error(`${name}, line ${bad.line}: the file manages its own transaction; SqlMigrationRunner already runs each file in one, so remove it`);
  let out = 'BEGIN;\n';
  statements.forEach((s, i) => { out += tag('AT', quote(`${which}|${name}|${i + 1}|${s.line}`)) + execute(s.sql); });
  if (record) {
    out += `INSERT INTO platform.schema_version (version, description, checksum, execution_ms) VALUES (${quote(name)}, `
      + `${quote(`applied from ${folder}`)}, ${quote(checksum(text))}, 0);\n`;
  }
  out += 'COMMIT;\n';
  out += tag('DONE', quote(`${which}|${name}|${statements.length}`));
  return out;
}

/** What a failed session was doing, in words. */
function failure(result) {
  const at = result.last('AT');
  const err = firstError(result.err);
  if (!at) return err;
  const [which, name, n, line] = at.split('|');
  const again = which === 'second run'
    ? '\nEvery statement must be safe to run again (IF NOT EXISTS, CREATE OR REPLACE, DROP ... IF EXISTS before ADD CONSTRAINT).'
    : '';
  return `${which}: ${name}, statement ${n}${line === '-' ? '' : ` (line ${line})`} failed:\n${err}${again}`;
}

// ---- the template of the previous state --------------------------------------------------------

async function ensureBase(names, database, dir, files, folder) {
  const want = files.map((f) => ({ name: f, sha: checksum(readSql(path.join(dir, f))) }));
  const r = await ready(tag('BASE', `coalesce((SELECT coalesce(shobj_description(oid, 'pg_database'), '') FROM pg_database WHERE datname = ${quote(names.base)}), '')`));
  const server = r.last('VERSION');
  let have = null;
  try { have = JSON.parse(r.last('BASE') || 'null'); } catch { have = null; }
  const same = have && have.v === VERSION && have.server === server && Array.isArray(have.files)
    && have.files.length <= want.length && have.files.every((h, i) => h.name === want[i].name && h.sha === want[i].sha);
  const from = same ? have.files.length : 0;
  const action = !same ? 'built' : from < want.length ? 'extended' : 'reused';
  const comment = (list) => `COMMENT ON DATABASE ${names.base} IS ${quote(JSON.stringify({ v: VERSION, server, files: list }))};\n`;
  if (!same) must(session('postgres', `DROP DATABASE IF EXISTS ${names.base} WITH (FORCE);\nCREATE DATABASE ${names.base};\n${comment([])}`));
  const started = Date.now();
  if (from < want.length) {
    const sql = want.slice(from).map((w) => fileSql(path.join(dir, w.name), folder, { record: true, label: 'previous state' })).join('');
    const result = session(names.base, sql);
    const done = (result.tags.DONE ?? []).length;
    must(session('postgres', comment(want.slice(0, from + done))));
    if (!result.ok) throw new Error(`an earlier migration does not apply, so the previous state cannot be built: ${failure(result)}`);
  }
  return { action, applied: want.length - from, ms: Date.now() - started, state: { server, files: want } };
}

// ---- one folder, one lock ---------------------------------------------------------------------

function folderId(root) {
  return createHash('sha256').update(root.toLowerCase()).digest('hex').slice(0, 8);
}

function databaseNames(id, database) {
  if (!/^[a-z][a-z0-9_]{0,30}$/.test(database)) throw new Usage(`"${database}" is not a database name this check uses (tenant or control)`);
  const p = `adam_${id}_${database}`;
  return { base: `${p}_base`, ticket: `${p}_ticket`, expect: `${p}_expect`, full: `${p}_full` };
}

async function withLock(id, work) {
  const file = path.join(os.tmpdir(), `adam-db-ticket-${id}.lock`);
  let said = false;
  for (let waited = 0; ; waited += 500) {
    try {
      const fd = openSync(file, 'wx');
      writeFileSync(fd, String(process.pid));
      closeSync(fd);
      break;
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      let holder = 0;
      try { holder = Number(readFileSync(file, 'utf8').trim()) || 0; } catch { continue; }
      let alive = false;
      try { if (holder) { process.kill(holder, 0); alive = true; } } catch (e) { alive = e.code === 'EPERM'; }
      if (!alive) { try { unlinkSync(file); } catch { /* another run took it */ } continue; }
      if (waited > 20 * 60 * 1000) throw new Usage(`another check in this folder (process ${holder}) has held the lock for 20 minutes`);
      if (!said) { console.log(`Waiting for another check in this folder to finish (process ${holder})...`); said = true; }
      await sleep(500);
    }
  }
  try {
    return await work();
  } finally {
    try { unlinkSync(file); } catch { /* gone already */ }
  }
}

/** Kept snapshots older than a week go. */
function pruneCache(id) {
  try {
    for (const f of readdirSync(os.tmpdir()).filter((n) => n.startsWith(`adam-db-ticket-${id}-`) && n.endsWith('.json'))) {
      const p = path.join(os.tmpdir(), f);
      if (Date.now() - statSync(p).mtimeMs > 7 * 24 * 3600 * 1000) unlinkSync(p);
    }
  } catch { /* nothing to prune */ }
}

// ---- one ticket ---------------------------------------------------------------------------------

const secs = (ms) => `${(ms / 1000).toFixed(1)} s`;
const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`;

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--file' || a === '--container' || a === '--full') args[a.slice(2)] = argv[++i];
    else if (a === '--clean') args.clean = true;
    else if (a === '--help' || a === '-h') args.help = true;
    else args._.push(a);
  }
  return args;
}

/** One database of a ticket. */
async function checkOne(root, id, key, check, args, out) {
  const database = check.database ?? 'tenant';
  const names = databaseNames(id, database);
  const folder = `db/${database}`;
  const dir = path.join(root, 'db', database);
  const file = args.file ? path.resolve(root, args.file) : path.join(dir, check.migration);
  if (!existsSync(file)) {
    const number = /^(V\d+[A-Za-z]?)__/.exec(check.migration ?? '')?.[1];
    const near = number ? sqlFiles(dir).filter((f) => f.startsWith(`${number}__`)) : [];
    throw new Usage(`${path.relative(root, file)} does not exist yet. Write it first`
      + `${near.length ? ` (found ${near.join(', ')}: rename it, or pass --file)` : ''}.`);
  }
  const name = path.basename(file);
  const all = sqlFiles(path.dirname(file));
  const earlier = all.filter((f) => f !== name && ordinal(f, name) < 0);
  const later = all.filter((f) => f !== name && ordinal(f, name) > 0);
  const owned = Object.keys(check.tables ?? {});
  const statements = check.statements ?? [];

  const base = await ensureBase(names, database, path.dirname(file), earlier, folder);
  // The previous state's snapshot and the package's result depend only on the template and the
  // package statements, so they are kept between runs: while the file is being fixed, a run copies
  // the template once and applies the file, and nothing else.
  const cacheFile = path.join(os.tmpdir(), `adam-db-ticket-${id}-${database}-${createHash('sha256')
    .update(JSON.stringify({ v: VERSION, base: base.state, statements })).digest('hex').slice(0, 16)}.json`);
  let cached = null;
  try { cached = JSON.parse(readFileSync(cacheFile, 'utf8')); } catch { cached = null; }
  must(session('postgres', `DROP DATABASE IF EXISTS ${names.ticket} WITH (FORCE);\nDROP DATABASE IF EXISTS ${names.expect} WITH (FORCE);\n`
    + `CREATE DATABASE ${names.ticket} TEMPLATE ${names.base};\n${cached ? '' : `CREATE DATABASE ${names.expect} TEMPLATE ${names.base};\n`}`));

  out(`Ticket ${key}: ${path.relative(root, file).split(path.sep).join('/')}`);
  out(`- previous state: ${plural(earlier.length, 'earlier file')} (template ${base.action}`
    + `${base.applied ? `, ${base.applied} applied in ${secs(base.ms)}` : ''})`
    + `${later.length ? `; ${plural(later.length, 'later file')} left out` : ''}`);

  // The ticket's file on one copy: snapshot, apply (recorded), snapshot, apply again (not recorded),
  // snapshot. The package's statements on the other copy, at the same time.
  const time = tag('T', 'extract(epoch FROM clock_timestamp())');
  const aSql = (cached ? '' : tag('SNAP0', SNAPSHOT_SQL)) + time
    + fileSql(file, folder, { record: true, label: 'first run' }) + time + tag('SNAP1', SNAPSHOT_SQL)
    + fileSql(file, folder, { record: false, label: 'second run' }) + tag('SNAP2', SNAPSHOT_SQL);
  let b = 'SET check_function_bodies = off;\nBEGIN;\n';
  statements.forEach((s, i) => {
    b += tag('AT', quote(`the package's statements|${s.file}|${i + 1}|-`));
    if (s.guard) {
      const both = `to_regclass(${quote(s.guard.table)}) IS NOT NULL AND to_regclass(${quote(s.guard.references)}) IS NOT NULL`;
      b += `SELECT '${NONCE}_DEFER|' || ${quote(`${s.guard.table} (${s.guard.columns.join(', ')}) -> ${s.guard.references}`)} WHERE NOT (${both});\n`;
      b += execute(s.sql, `${both} AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conrelid = to_regclass(${quote(s.guard.table)}) AND conname = ${quote(s.guard.constraint)})`);
    } else {
      b += execute(s.sql);
    }
  });
  b += `COMMIT;\n${tag('SNAPB', SNAPSHOT_SQL)}`;
  const [a, e] = await Promise.all([sessionAsync(names.ticket, aSql), cached ? null : sessionAsync(names.expect, b)]);
  if (!a.ok) return { failed: failure(a) };
  const [t0, t1] = (a.tags.T ?? []).map(Number);
  const count = Number(a.tags.DONE?.[0]?.split('|')[2] ?? 0);
  out(`- first run: ${plural(count, 'statement')} applied in ${secs((t1 - t0) * 1000)}`);
  const after = JSON.parse(a.last('SNAP1'));
  const again = againDiffs(after, JSON.parse(a.last('SNAP2')));
  if (!again.length) out('- second run: applied again, changed nothing');

  if (e && !e.ok) {
    return {
      failed: 'the package\'s own DDL for this ticket does not apply on the previous state, so there is nothing to compare '
        + `with. That is a change request against the package (CLAUDE.md, "When the package is wrong"):\n${failure(e)}`,
    };
  }
  const known = cached ?? { before: JSON.parse(a.last('SNAP0')), expected: JSON.parse(e.last('SNAPB')), deferred: e.tags.DEFER ?? [] };
  if (!cached) {
    try { writeFileSync(cacheFile, JSON.stringify(known)); } catch { /* the next run works it out again */ }
  }
  const { deferred } = known;
  out(`- the package's statements: ${statements.length} applied to a second copy${cached ? ' (kept from an earlier run)' : ''}`
    + `${deferred.length ? `; ${plural(deferred.length, 'foreign key')} left for a later migration (the table is not created yet)` : ''}`);
  for (const d of deferred) out(`  - ${d}`);

  const diffs = [...again, ...diffSnapshots({ before: known.before, after, expected: known.expected, owned })];
  const gaps = [...(check.notInPackageDdl ?? []), ...(check.keysNotInPackageDdl ?? [])];
  return { diffs, gaps, empty: !statements.length, owned };
}

async function ticket(root, id, key, args) {
  const work = path.join(root, '.adam', 'work', key);
  const expectedFile = path.join(work, 'expected-schema.json');
  if (!existsSync(expectedFile)) {
    const readme = path.join(work, 'README.md');
    const why = existsSync(readme) && /could not be written \(([^)]*)\)/.exec(readFileSync(readme, 'utf8'))?.[1];
    throw new Usage(why
      ? `ADAM could not write expected-schema.json for this ticket (${why}). Check it by hand as README.md says; pulling again will not change that.`
      : `${path.relative(root, expectedFile)} is missing. Pull the ticket first (adam_pull ${key}).`);
  }
  const expected = JSON.parse(readFileSync(expectedFile, 'utf8'));
  const checks = expected.checks ?? [];
  if (!checks.length) throw new Usage(`${path.relative(root, expectedFile)} lists nothing to check; pull the ticket again.`);
  if (args.file && checks.length > 1) throw new Usage('--file cannot be used for a ticket with a file in each database');

  const lines = [];
  const out = (s = '') => { lines.push(s); console.log(s); };
  const started = Date.now();
  pruneCache(id);
  await ensureContainer(Boolean(args.container));
  let code = 0;
  for (const check of checks) {
    let r;
    try {
      r = await checkOne(root, id, key, check, args, out);
    } catch (error) {
      if (error instanceof Usage) throw error;
      r = { failed: error.message };
    }
    if (r.failed) {
      out(`FAILED: ${r.failed}`);
      code = 1;
    } else if (r.diffs.length) {
      out(`DIFFERENT: ${plural(r.diffs.length, 'difference')} from what the package's statements leave`);
      for (const d of r.diffs) out(`  - ${d}`);
      code = 1;
    } else if (r.gaps.length || r.empty) {
      out(`PARTIAL: the file matches the package's statements, but ${r.empty ? 'there were none to compare with'
        : `the package DDL lacks ${r.gaps.join(', ')}`}. Not evidence for done: that is a change request.`);
      code = 1;
    } else {
      out(`MATCH: ${r.owned.length ? `${plural(r.owned.length, 'table')} (${r.owned.join(', ')})` : 'everything the package\'s statements make'}`
        + ' exactly as the package makes them, a second run changed nothing, and nothing else changed');
    }
  }
  out(`- took ${secs(Date.now() - started)}. The copies are left in container ${CONTAINER} to look at; --clean drops them.`);
  writeFileSync(path.join(work, 'db-check.md'), `# db-ticket check, ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}\n\n${lines.join('\n')}\n`);
  return code;
}

// ---- every file from empty ----------------------------------------------------------------------

async function full(root, id, database, args) {
  const names = databaseNames(id, database);
  const dir = path.join(root, 'db', database);
  const folder = `db/${database}`;
  const files = sqlFiles(dir).map((f) => path.join(dir, f));
  if (!files.length) throw new Usage(`no .sql files in ${folder}`);
  const started = Date.now();
  await ensureContainer(Boolean(args.container));
  // Each file is applied and then applied again straight away, as a ticket's check does: a later
  // file may rightly drop what an earlier one added, so the second runs are not saved for the end.
  const hash = (name) => tag(name, `md5(${SNAPSHOT_SQL}::text)`);
  let sql;
  try {
    sql = files.map((f) => fileSql(f, folder, { record: true, label: 'first run' }) + hash('H1')
      + fileSql(f, folder, { record: false, label: 'second run' }) + hash('H2')).join('');
  } catch (error) {
    console.log(`FAILED: ${error.message}`);
    return 1;
  }
  await ready(`DROP DATABASE IF EXISTS ${names.full} WITH (FORCE);\nCREATE DATABASE ${names.full};\n`);
  const r = session(names.full, sql);
  if (!r.ok) {
    console.log(`FAILED: ${failure(r)}`);
    return 1;
  }
  console.log(`- ${plural(files.length, 'file')} applied to an empty database, each applied a second time straight after`);
  const again = files.map((f, i) => ((r.tags.H1?.[i] !== r.tags.H2?.[i]) ? `the second run of ${path.basename(f)} changed the schema` : null)).filter(Boolean);
  if (again.length) { console.log(`DIFFERENT: ${plural(again.length, 'difference')}`); for (const d of again) console.log(`  - ${d}`); }
  else console.log(`MATCH: ${folder} applies to an empty database, and a second run of each file changes nothing`);
  console.log(`- took ${secs(Date.now() - started)}. The database is left as ${names.full} in container ${CONTAINER}; --clean drops it.`);
  return again.length ? 1 : 0;
}

async function clean(id) {
  const state = docker(['inspect', '-f', '{{.State.Running}}', CONTAINER]);
  if (!state.ok || state.out.trim() !== 'true') { console.log(`Nothing to clean: ${CONTAINER} is not running.`); return 0; }
  const r = await ready(tag('DBS', `coalesce((SELECT string_agg(datname, ',') FROM pg_database WHERE datname LIKE ${quote(`adam\\_${id}\\_%`)}), '')`));
  const dbs = (r.last('DBS') ?? '').split(',').filter(Boolean);
  if (dbs.length) must(session('postgres', dbs.map((d) => `DROP DATABASE IF EXISTS ${d} WITH (FORCE);\n`).join('')));
  console.log(`Dropped ${plural(dbs.length, 'database')} of this folder. To remove the container too: docker rm -f ${CONTAINER}`);
  return 0;
}

// ---- main ---------------------------------------------------------------------------------------

export async function main(argv) {
  const args = parseArgs(argv);
  if (args.container) CONTAINER = args.container;
  if (args.help || (!args._.length && !args.full && !args.clean)) {
    console.log('node .claude/scripts/db-ticket.mjs <ticket> [--file db/<database>/<file>.sql] [--container <name>]\n'
      + 'node .claude/scripts/db-ticket.mjs --full <tenant|control> [--container <name>]\n'
      + 'node .claude/scripts/db-ticket.mjs --clean [--container <name>]');
    return args.help ? 0 : 2;
  }
  try {
    const root = realpathSync.native(process.cwd());
    const id = folderId(root);
    if (args.clean) return await withLock(id, () => clean(id));
    if (args.full) return await withLock(id, () => full(root, id, args.full, args));
    return await withLock(id, () => ticket(root, id, String(args._[0]).replace(/^#/, ''), args));
  } catch (error) {
    console.log(error instanceof Usage ? `Cannot run: ${error.message}` : `FAILED: ${error.message}`);
    return error instanceof Usage ? 2 : 1;
  }
}

// Run as a command, whatever path it was reached by (a junction, a subst drive, a short name).
// Until main answers, the exit code says "did not run", never "passed".
function same(a, b) {
  try {
    const x = realpathSync.native(a);
    const y = realpathSync.native(b);
    return process.platform === 'win32' ? x.toLowerCase() === y.toLowerCase() : x === y;
  } catch {
    return false;
  }
}
if (process.argv[1] && same(process.argv[1], fileURLToPath(import.meta.url))) {
  process.exitCode = 2;
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; }, (error) => {
    console.log(`FAILED: ${error?.message ?? error}`);
    process.exitCode = 1;
  });
} else if (/db-ticket\.mjs$/i.test(process.argv[1] ?? '')) {
  // Named as the command but not recognised as this file: say so rather than exit 0 in silence.
  console.log(`Cannot run: ${process.argv[1]} could not be matched to ${fileURLToPath(import.meta.url)}`);
  process.exitCode = 2;
}
