#!/usr/bin/env node
/**
 * A [DB] ticket's quick check, end to end: what adam_pull writes and what the starter's
 * .claude/scripts/db-ticket.mjs does with it.
 *
 *   node viewer/mcp/db-ticket-check.mjs              parser, compare and pull; then, with Docker, the script
 *   node viewer/mcp/db-ticket-check.mjs --package    also the whole package DDL against PostgreSQL 16 (~3 min)
 *
 * **Why this exists** (Chinmay, 20 October 2026). A [DB] ticket's agent rebuilt every migration from
 * an empty database, reasoned about the effect by itself and ran dotnet build and the whole dotnet
 * test suite on every ticket. Now the ticket folder holds expected-schema.json (the end state of the
 * ticket's tables, read from the package DDL by tools.mjs) and the script applies only the ticket's
 * file to a template copy of the previous state, runs it twice, and compares. Both halves are only
 * worth having if they agree with PostgreSQL, so:
 *
 *   1. the parser: statements, columns and inline constraints, ALTER TABLE, indexes, the 920 helpers;
 *   2. the compare: each kind of difference is reported, a key to a table not made yet is deferred;
 *   3. adam_pull, against a stand-in ADAM serving this repository's ticvai/ package, writes
 *      expected-schema.json and the README section for a [DB] ticket, and nothing for a [BE] one;
 *   4. with Docker: a developer folder made from the real package DDL (baseline, two earlier
 *      migrations, the ticket's, one later) - MATCH on the first run, the template reused on the
 *      second, and DIFFERENT / FAILED for a missing index, an extra table, a column changed and a
 *      file that does not apply; --full from empty;
 *   5. with --package: every table the package creates (tenant and control), parsed and compared
 *      with the catalog of the package applied to pgvector/pgvector:pg16. No difference allowed.
 *
 * Exits non-zero on a failure. Docker missing is a named skip of 4 and 5, never a pass.
 */

import { spawnSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const PACKAGE = path.join(REPO, 'ticvai');
const SCRIPT = path.join(HERE, 'setup', 'starters', 'backend', '.claude', 'scripts', 'db-ticket.mjs');
const PACKAGE_RUN = process.argv.includes('--package');

const tools = await import(pathToFileURL(path.join(HERE, 'tools.mjs')).href);
const script = await import(pathToFileURL(SCRIPT).href);
const { sqlStatements, schemaModel, expectedSchema, databaseTicket, BY_NAME } = tools;

let failures = 0;
const ok = (cond, what, detail = '') => {
  if (cond) console.log(`  ok    ${what}`);
  else { failures++; console.log(`  FAIL  ${what}${detail ? `\n        ${String(detail).slice(0, 600)}` : ''}`); }
};
const skip = (what, why) => console.log(`  skip  ${what} - ${why}`);
const section = (name) => console.log(`\n${name}`);

// ---- 1. the parser --------------------------------------------------------------------------

section('the DDL parser');
{
  const stmts = sqlStatements(`-- a comment; with a semicolon
CREATE TABLE a.t (x text DEFAULT 'a;b'); /* block; */
CREATE FUNCTION f() RETURNS void LANGUAGE plpgsql AS $$ BEGIN PERFORM 1; END $$;
SELECT 1`);
  ok(stmts.length === 3 && stmts[0].includes("'a;b'") && stmts[1].includes('PERFORM 1; END'),
    'statements split on ; outside strings, comments and dollar-quoted bodies', JSON.stringify(stmts));

  const model = schemaModel([
    { name: '010-a.sql', text: `
CREATE TABLE IF NOT EXISTS a.parent (id uuid PRIMARY KEY NOT NULL, scope_path ltree NOT NULL);
CREATE TABLE IF NOT EXISTS a.child (
    id                uuid NOT NULL,
    parent_id         uuid REFERENCES a.parent(id) ON DELETE CASCADE,
    status            text NOT NULL DEFAULT 'open' CONSTRAINT child_status_chk CHECK (status IN ('open', 'shut')),
    amount            numeric(18,4) DEFAULT 0,
    tags              text[],
    venue_id          uuid NOT NULL,
    occurred_at       timestamptz NOT NULL,
    CONSTRAINT child_pkey PRIMARY KEY (id, occurred_at),
    UNIQUE (venue_id, id, occurred_at)
) PARTITION BY RANGE (occurred_at);` },
    { name: '900-foreign-keys.sql', text: 'ALTER TABLE a.child ADD CONSTRAINT child_venue_fkey FOREIGN KEY (venue_id) REFERENCES b.scope(id);' },
    { name: '910-indexes.sql', text: `CREATE INDEX IF NOT EXISTS child_parent_id_idx ON a.child (parent_id);
CREATE UNIQUE INDEX IF NOT EXISTS parent_root_uniq ON a.parent ((true)) WHERE scope_path IS NULL;
CREATE INDEX IF NOT EXISTS parent_scope_path_idx ON a.parent USING gist (scope_path);` },
    { name: '920-row-level-security.sql', text: `SELECT platform.apply_scope_rls('a.parent'::regclass);
SELECT platform.apply_parent_rls('a.child'::regclass, 'parent_id', 'a.parent'::regclass, 'id');` },
    { name: '930-partitioning.sql', text: 'CREATE TABLE IF NOT EXISTS a.child_default PARTITION OF a.child DEFAULT;' },
    { name: 'V0101__after.sql', text: `ALTER TABLE a.child ADD COLUMN IF NOT EXISTS note text CONSTRAINT child_note_chk CHECK (char_length(note) < 9);
ALTER TABLE a.child ADD COLUMN IF NOT EXISTS status text;
ALTER TABLE a.child ALTER COLUMN amount SET NOT NULL;
ALTER TABLE a.child RENAME TO kid;` },
  ]);
  const child = model.tables.get('a.kid');
  const parent = model.tables.get('a.parent');
  ok(child && !model.tables.has('a.child'), 'RENAME TO moves the table', [...model.tables.keys()].join(', '));
  const col = (n) => child?.columns.find((c) => c.name === n);
  ok(col('status')?.notNull && col('status')?.default === "'open'" && col('status')?.type === 'text',
    'a column: type, NOT NULL and default, with its CHECK after', JSON.stringify(col('status')));
  ok(col('amount')?.type === 'numeric(18,4)' && col('amount')?.notNull, 'numeric(18,4), and ALTER ... SET NOT NULL', JSON.stringify(col('amount')));
  ok(col('tags')?.type === 'text[]' && !col('tags')?.notNull, 'an array type', JSON.stringify(col('tags')));
  ok(child?.columns.filter((c) => c.name === 'status').length === 1 && child?.columns.length === 8,
    'ADD COLUMN IF NOT EXISTS adds a new column once and leaves an existing one alone', child?.columns.map((c) => c.name).join(','));
  ok(child?.checks.map((c) => c.name).join(',') === 'child_status_chk,child_note_chk', 'named checks, inline and added', JSON.stringify(child?.checks));
  ok(child?.primaryKey?.columns.join(',') === 'id,occurred_at' && child?.primaryKey?.name === 'child_pkey', 'a table-level primary key', JSON.stringify(child?.primaryKey));
  ok(child?.unique.length === 1 && child.unique[0].columns.join(',') === 'venue_id,id,occurred_at', 'an unnamed table-level UNIQUE', JSON.stringify(child?.unique));
  const fks = child?.foreignKeys ?? [];
  ok(fks.length === 2 && fks[0].references === 'a.parent' && fks[0].onDelete === 'CASCADE' && fks[1].name === 'child_venue_fkey' && fks[1].references === 'b.scope',
    'foreign keys inline (ON DELETE) and from 900', JSON.stringify(fks));
  ok(child?.indexes[0]?.name === 'child_parent_id_idx' && child.indexes[0].keys === 'parent_id' && child.indexes[0].method === 'btree', 'an index', JSON.stringify(child?.indexes));
  const uniq = parent?.indexes.find((i) => i.name === 'parent_root_uniq');
  ok(uniq?.unique && uniq.keys === '(true)' && uniq.where === 'scope_path IS NULL', 'a unique partial expression index', JSON.stringify(uniq));
  ok(parent?.indexes.find((i) => i.name === 'parent_scope_path_idx')?.method === 'gist', 'USING gist', JSON.stringify(parent?.indexes));
  ok(parent?.rls.enabled && parent.rls.forced && parent.rls.policies[0]?.name === 'parent_scope' && parent.rls.policies[0].uses === 'in_scope(scope_path)',
    'apply_scope_rls: enabled, forced, the helper\'s policy name', JSON.stringify(parent?.rls));
  ok(child?.rls.policies[0]?.name === 'child_scope' && child.rls.policies[0].uses === 'a.parent',
    'apply_parent_rls names the parent (the policy keeps the name it was given before the rename)', JSON.stringify(child?.rls));
  ok(child?.partitionBy === 'RANGE (occurred_at)' && child.defaultPartition, 'PARTITION BY and the default partition', `${child?.partitionBy} ${child?.defaultPartition}`);
  ok(model.notModelled.length === 0, 'nothing left unread', JSON.stringify(model.notModelled));
  const unread = schemaModel([{ name: '010.sql', text: 'CREATE TABLE x.y (a int); ALTER TABLE x.y CLUSTER ON y_idx;' }]);
  ok(unread.notModelled.length === 1 && unread.notModelled[0].table === 'x.y', 'what it does not understand is listed, not guessed', JSON.stringify(unread.notModelled));

  const exp = expectedSchema(model, ['a.kid', 'a.gone'], { database: 'tenant', migration: 'V0002__a.sql' });
  ok(exp.tables['a.kid'] && exp.notInPackageDdl?.join() === 'a.gone' && exp.migration === 'V0002__a.sql', 'expectedSchema: the asked tables, and the ones the DDL lacks', JSON.stringify(Object.keys(exp)));

  const db = databaseTicket({ subject: '[DB] Migration V0027__access.sql: access (19 tables)', description: 'Tenant database. Tables: ...' },
    [{ kind: 'table', id: 'access.entitlement' }, { kind: 'table', id: 'access.scan_event' }]);
  ok(db?.migration === 'V0027__access.sql' && db.database === 'tenant' && db.tables.length === 2, 'a [DB] ticket: its file, database and tables', JSON.stringify(db));
  ok(databaseTicket({ subject: '[DB] Forward migration V1001__identity.sql: identity for X (2 tables)', description: '' }, [{ kind: 'table', id: 'identity.sso_provider' }])?.migration === 'V1001__identity.sql',
    'a forward migration ticket too');
  ok(databaseTicket({ subject: '[BE] Build listPasses', description: '' }, [{ kind: 'table', id: 'access.pass' }]) === null, 'a [BE] ticket that reads tables is not one');
  ok(databaseTicket({ subject: '[DB] Monthly partitions: create three months ahead', description: '' }, [{ kind: 'table', id: 'kernel.inbox' }]) === null,
    'a [DB] task with no migration file is not one');
}

// ---- 2. the compare -------------------------------------------------------------------------

section('the compare');
{
  ok(script.normType('timestamptz') === 'timestamp with time zone' && script.normType('char(2)') === 'character(2)'
    && script.normType('int[]') === 'integer[]' && script.normType('numeric(18, 4)') === 'numeric(18,4)', 'types to the catalog\'s spelling');
  ok(script.normDefault("'open'::text") === "'open'" && script.normDefault("'-1'::integer") === '-1' && script.normDefault("'{}'::text[]") === "'{}'"
    && script.normDefault('now()') === 'now()' && script.normDefault('NULL') === null, 'defaults without casts');
  const expected = {
    columns: [{ name: 'id', type: 'uuid', notNull: true }, { name: 'n', type: 'integer', notNull: false, default: '0' }],
    primaryKey: { name: null, columns: ['id'] }, unique: [], checks: [{ name: 't_n_chk' }],
    foreignKeys: [{ name: 't_p_fkey', columns: ['p'], references: 'b.later', refColumns: ['id'], onDelete: null }],
    indexes: [{ name: 't_n_idx', unique: false, method: 'btree', keys: 'n' }],
    rls: { enabled: true, forced: true, policies: [{ name: 't_scope', uses: 'in_scope(scope_path)' }] }, partitionBy: null, defaultPartition: false,
  };
  const actual = {
    columns: [{ name: 'id', type: 'uuid', notNull: true, default: null }, { name: 'n', type: 'integer', notNull: false, default: '0' }],
    constraints: [{ name: 't_pkey', type: 'p', columns: ['id'] }, { name: 't_n_chk', type: 'c', columns: ['n'] }],
    indexes: [{ name: 't_pkey', constraint: true, unique: true, def: 'CREATE UNIQUE INDEX t_pkey ON a.t USING btree (id)', method: 'btree' },
      { name: 't_n_idx', constraint: false, unique: false, def: 'CREATE INDEX t_n_idx ON a.t USING btree (n)', method: 'btree' }],
    rls: { enabled: true, forced: true, policies: [{ name: 't_scope', using: 'platform.in_scope(scope_path)' }] }, partitionBy: null, defaultPartition: false,
  };
  const same = script.compareTable('a.t', expected, actual, () => false);
  ok(same.diffs.length === 0 && same.deferred.length === 1, 'a match, with the key to a table not made yet deferred', JSON.stringify(same));
  const broken = structuredClone(actual);
  broken.columns[1] = { name: 'n', type: 'bigint', notNull: true, default: null };
  broken.columns.push({ name: 'extra', type: 'text', notNull: false, default: null });
  broken.indexes.pop();
  broken.rls.forced = false;
  broken.constraints = broken.constraints.filter((k) => k.type !== 'c');
  const r = script.compareTable('a.t', expected, broken, () => true);
  const want = ['column n is bigint', 'column n is NOT NULL', 'column n defaults to nothing', 'column extra is not in the package',
    'index t_n_idx is missing', 'is not FORCEd', 'check t_n_chk is missing', 'foreign key (p) -> b.later is missing'];
  ok(want.every((w) => r.diffs.some((d) => d.includes(w))) && r.diffs.length === want.length, 'each difference said once, in words', r.diffs.join(' | '));
  const created = script.compareSchema({ tables: { 'a.t': expected } }, { 'a.t': actual }, { created: ['a.t', 'a.stray'], exists: () => false });
  ok(created.diffs.length === 1 && /a\.stray: created by this file/.test(created.diffs[0]), 'a table the file made that is not the ticket\'s', created.diffs.join(' | '));
}

// ---- 3. adam_pull writes it ------------------------------------------------------------------

section('adam_pull writes expected-schema.json for a [DB] ticket');
const SCRATCH = mkdtempSync(path.join(tmpdir(), 'db-ticket-check-'));
const SUB = ['subscription.contract', 'subscription.module_listing', 'subscription.plan', 'subscription.plan_limit', 'subscription.plan_module'];
let expectedSub = null;
{
  const { buildBackend } = await import(pathToFileURL(path.join(REPO, 'viewer', 'lib', 'backend.mjs')).href);
  const backend = await buildBackend(PACKAGE);
  const tickets = {
    9005: { workPackage: { key: '9005', subject: '[DB] Migration V0005__subscription.sql: subscription (5 tables)', description: `Tenant database. Tables: ${SUB.join(', ')}.` },
      touches: SUB.map((id) => ({ kind: 'table', id })) },
    9100: { workPackage: { key: '9100', subject: '[BE] Build getPlan', description: '' }, touches: [{ kind: 'table', id: 'subscription.plan' }] },
  };
  let fileReads = 0;
  const client = {
    async projectId() { return 'ticvai'; },
    async layer(route) { return route === 'backend' ? backend : {}; },
    async file(p) {
      fileReads++;
      const full = path.join(PACKAGE, p);
      return existsSync(full) ? { ok: true, status: 200, text: readFileSync(full, 'utf8') } : { ok: false, status: 404, text: '' };
    },
    async service(route) {
      const m = /^\/api\/work-packages\/(\d+)\?/.exec(route);
      if (m && tickets[m[1]]) return { ok: true, status: 200, data: tickets[m[1]] };
      return { ok: false, status: 404, data: { detail: 'not here' } };
    },
  };
  const dir = path.join(SCRATCH, 'pulled');
  mkdirSync(dir);
  const pull = BY_NAME.get('adam_pull');
  const one = await pull.run(client, { key: '9005', dir });
  const folder = path.join(dir, '.adam', 'work', '9005');
  const file = path.join(folder, 'expected-schema.json');
  ok(one.found && existsSync(file), 'expected-schema.json is in the ticket folder', JSON.stringify(one).slice(0, 400));
  expectedSub = existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : null;
  ok(expectedSub?.database === 'tenant' && expectedSub.migration === 'V0005__subscription.sql' && Object.keys(expectedSub.tables).length === 5,
    'it names the database, the file and the five tables', JSON.stringify({ ...expectedSub, tables: Object.keys(expectedSub?.tables ?? {}) }));
  ok(expectedSub?.sources.includes('backend/tenant/010-subscription.sql') && expectedSub.sources.includes('backend/tenant/910-indexes.sql')
    && !expectedSub.sources.includes('backend/tenant/010-access.sql'), 'read from the 010 file that creates them and every later file', expectedSub?.sources.join(', '));
  const readme = readFileSync(path.join(folder, 'README.md'), 'utf8');
  ok(/## Checking this migration/.test(readme) && readme.includes('node .claude/scripts/db-ticket.mjs 9005') && readme.includes('db/tenant/V0005__subscription.sql')
    && /do not run `dotnet build`/.test(readme), 'README.md says how to check it, and that dotnet build and test are not for this ticket');
  ok(one.database?.migration === 'db/tenant/V0005__subscription.sql' && /db-ticket\.mjs 9005/.test(one.next), 'the answer points at the check', one.next);
  const reads = fileReads;
  await pull.run(client, { key: '9005', dir });
  ok(fileReads === reads, 'a second pull within the minute reads the DDL from memory', `${fileReads - reads} reads`);
  const be = await pull.run(client, { key: '9100', dir });
  ok(be.found && !existsSync(path.join(dir, '.adam', 'work', '9100', 'expected-schema.json')) && !be.database,
    'a [BE] ticket gets no expected-schema.json');
}

// ---- 4. the script, as a developer runs it -----------------------------------------------------

const dockerUp = spawnSync('docker', ['version', '--format', '{{.Server.Version}}'], { encoding: 'utf8' }).status === 0;
const CONTAINER = 'adam-db-ticket-check';
const docker = (args, input) => spawnSync('docker', args, { input, encoding: 'utf8', maxBuffer: 1 << 30 });

async function startContainer() {
  docker(['rm', '-f', CONTAINER]);
  const run = docker(['run', '-d', '--name', CONTAINER, '-e', 'POSTGRES_PASSWORD=check', 'pgvector/pgvector:pg16']);
  if (run.status !== 0) return run.stderr;
  for (let i = 0; i < 60; i++) {
    if (docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', 'SELECT 1']).status === 0) return null;
    await new Promise((r) => { setTimeout(r, 500); });
  }
  return 'did not become ready';
}

/** The package's statements for `tables`, as a developer's migration copies them. */
function migrationFor(tables, { skipKeysTo = () => false } = {}) {
  const dir = path.join(PACKAGE, 'backend', 'tenant');
  const want = new Set(tables);
  const target = (s) => /^(?:CREATE TABLE IF NOT EXISTS|ALTER TABLE|CREATE (?:UNIQUE )?INDEX IF NOT EXISTS \w+ ON|SELECT platform\.apply_\w+_rls\(')\s*([\w.]+)/i.exec(s)?.[1];
  const out = [];
  for (const f of readdirSync(dir).filter((n) => /\.sql$/.test(n)).sort()) {
    if (/^00/.test(f)) continue;
    for (const s of sqlStatements(readFileSync(path.join(dir, f), 'utf8'))) {
      const t = target(s)?.replace(/'$/, '');
      if (!t || !want.has(t)) continue;
      const ref = /REFERENCES\s+([\w.]+)/i.exec(s)?.[1];
      if (/^ALTER TABLE/i.test(s) && ref && skipKeysTo(ref)) continue;
      out.push(`${s};`);
    }
    if (f === '930-partitioning.sql') {
      for (const s of sqlStatements(readFileSync(path.join(dir, f), 'utf8'))) {
        const parent = /PARTITION OF ([\w.]+) DEFAULT/i.exec(s)?.[1];
        if (parent && want.has(parent)) out.push(`${s};`);
      }
    }
  }
  return `${out.join('\n')}\n`;
}

function baseline() {
  const dir = path.join(PACKAGE, 'backend', 'tenant');
  const read = (f) => readFileSync(path.join(dir, f), 'utf8');
  const functions = [read('920-row-level-security.sql'), read('930-partitioning.sql')]
    .flatMap((t) => sqlStatements(t)).filter((s) => /^CREATE OR REPLACE FUNCTION/i.test(s)).map((s) => `${s};`);
  // The SQL-language helpers read platform.scope, which a later migration creates.
  return ['SET check_function_bodies = off;', read('000-schemas.sql'), read('001-extensions.sql'), read('002-migration-register.sql'),
    ...functions].join('\n');
}

function runScript(cwd, ...args) {
  const r = spawnSync(process.execPath, [SCRIPT, ...args, '--container', CONTAINER], { cwd, encoding: 'utf8' });
  return { code: r.status, out: `${r.stdout}${r.stderr}` };
}

section('the script on a developer folder (Docker)');
if (!dockerUp) {
  skip('the script against PostgreSQL', 'Docker is not running here');
} else if (!expectedSub) {
  ok(false, 'the script needs the expected-schema.json from section 3');
} else {
  const started = await startContainer();
  ok(started === null, `a throwaway ${CONTAINER} container`, started);
  const repo = path.join(SCRATCH, 'backend');
  const db = path.join(repo, 'db', 'tenant');
  mkdirSync(db, { recursive: true });
  mkdirSync(path.join(repo, '.adam', 'work', '9005'), { recursive: true });
  writeFileSync(path.join(repo, '.adam', 'work', '9005', 'expected-schema.json'), JSON.stringify(expectedSub, null, 2));
  writeFileSync(path.join(db, 'V0001__baseline.sql'), baseline());
  writeFileSync(path.join(db, 'V0002__kernel.sql'), migrationFor(['kernel.inbox']));
  writeFileSync(path.join(db, 'V0003__tenancy.sql'), migrationFor(['tenancy.device_assignment']));
  writeFileSync(path.join(db, 'V0008__games.sql'), 'SELECT 1;\n');
  const made = new Set([...SUB, 'kernel.inbox', 'tenancy.device_assignment']);
  const good = migrationFor(SUB, { skipKeysTo: (t) => !made.has(t) });
  writeFileSync(path.join(db, 'V0005__subscription.sql'), good);

  let t = Date.now();
  const first = runScript(repo, '9005');
  const firstMs = Date.now() - t;
  ok(first.code === 0 && /MATCH: 5 tables/.test(first.out) && /template built/.test(first.out) && /second run: recorded in platform.schema_version with its checksum, so it applies nothing/.test(first.out),
    `first run: the template built, the file applied twice, MATCH (${(firstMs / 1000).toFixed(1)} s)`, first.out);
  ok(/1 later file left out/.test(first.out), 'a later file is left out of the previous state', first.out);
  ok(/left for a later migration/.test(first.out), 'keys to tables no migration has made yet are listed as deferred, not as differences', first.out);
  ok(existsSync(path.join(repo, '.adam', 'work', '9005', 'db-check.md')), 'the result is kept in db-check.md');

  t = Date.now();
  const again = runScript(repo, '9005');
  const againMs = Date.now() - t;
  ok(again.code === 0 && /template reused/.test(again.out), `second run: the template reused, MATCH (${(againMs / 1000).toFixed(1)} s)`, again.out);
  console.log(`        timings: first ${(firstMs / 1000).toFixed(1)} s, then ${(againMs / 1000).toFixed(1)} s`);

  writeFileSync(path.join(db, 'V0005__subscription.sql'), good.replace(/^CREATE INDEX IF NOT EXISTS plan_limit_plan_id_idx ON[^\n]*\n/m, ''));
  const noIndex = runScript(repo, '9005');
  ok(noIndex.code === 1 && /DIFFERENT/.test(noIndex.out) && /subscription\.plan_limit: index plan_limit_plan_id_idx is missing/.test(noIndex.out), 'a missing index is named', noIndex.out);

  writeFileSync(path.join(db, 'V0005__subscription.sql'), `${good}CREATE TABLE subscription.stray (id uuid PRIMARY KEY);\n`
    + 'ALTER TABLE subscription.plan ALTER COLUMN description SET NOT NULL;\n');
  const extra = runScript(repo, '9005');
  ok(extra.code === 1 && /subscription\.stray: created by this file, but not one of the ticket's tables/.test(extra.out)
    && /subscription\.plan: column description is NOT NULL; the package says nullable/.test(extra.out), 'an extra table and a changed column are named', extra.out);

  writeFileSync(path.join(db, 'V0005__subscription.sql'), `${good}ALTER TABLE subscription.nowhere ADD COLUMN x int;\n`);
  const fails = runScript(repo, '9005');
  ok(fails.code === 1 && /FAILED: V0005__subscription\.sql did not apply/.test(fails.out) && /subscription\.nowhere/.test(fails.out), 'a file that does not apply says why', fails.out);

  writeFileSync(path.join(db, 'V0003__tenancy.sql'), `${migrationFor(['tenancy.device_assignment'])}-- edited\n`);
  writeFileSync(path.join(db, 'V0005__subscription.sql'), good);
  const rebuilt = runScript(repo, '9005');
  ok(rebuilt.code === 0 && /template built/.test(rebuilt.out), 'an earlier file that changed rebuilds the template', rebuilt.out);

  rmSync(path.join(db, 'V0008__games.sql'));
  writeFileSync(path.join(db, 'V0010__keys.sql'), 'SELECT 1;\n');
  const full = runScript(repo, '--full', 'tenant');
  ok(full.code === 1 && /foreign key never created/.test(full.out), '--full from empty: a deferred key that no file ever adds is reported', full.out);

  const missing = runScript(repo, '9999');
  ok(missing.code === 2 && /Pull the ticket first/.test(missing.out), 'a ticket not pulled: exit 2 and what to do', missing.out);
}

// ---- 5. the whole package against PostgreSQL ----------------------------------------------------

section('the whole package DDL, parsed and compared with PostgreSQL (--package)');
if (!PACKAGE_RUN) {
  skip('every table of tenant and control', 'run with --package (about three minutes)');
} else if (!dockerUp) {
  skip('every table of tenant and control', 'Docker is not running here');
} else {
  for (const database of ['tenant', 'control']) {
    const dir = path.join(PACKAGE, 'backend', database);
    const files = readdirSync(dir).filter((f) => /\.sql$/.test(f)).sort();
    const name = `pkg_${database}`;
    docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-qc', `DROP DATABASE IF EXISTS ${name}`]);
    docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-qc', `CREATE DATABASE ${name}`]);
    const t = Date.now();
    let applyError = null;
    for (const f of files) {
      let sql = readFileSync(path.join(dir, f), 'utf8');
      // The package creates no pii.subject_kind or pii.contact_kind; give them one so 010-pii applies.
      if (database === 'tenant' && f === '010-pii.sql') sql = "CREATE TYPE pii.subject_kind AS ENUM ('a'); CREATE TYPE pii.contact_kind AS ENUM ('a');\n" + sql;
      const r = docker(['exec', '-i', CONTAINER, 'psql', '-X', '-q', '-U', 'postgres', '-d', name, '-v', 'ON_ERROR_STOP=1', '-f', '-'], sql);
      if (r.status !== 0) { applyError = `${f}: ${r.stderr}`; break; }
    }
    ok(!applyError, `${database}: the package applies to an empty database (${files.length} files, ${((Date.now() - t) / 1000).toFixed(0)} s)`, applyError);
    if (applyError) continue;
    const model = schemaModel(files.map((f) => ({ name: f, text: readFileSync(path.join(dir, f), 'utf8') })));
    const tables = [...model.tables.keys()];
    const exp = expectedSchema(model, tables, { database });
    const r = docker(['exec', '-i', CONTAINER, 'psql', '-X', '-q', '-At', '-U', 'postgres', '-d', name, '-f', '-'], `${script.catalogSql(tables)};`);
    const catalog = JSON.parse(r.stdout || '{}');
    const res = script.compareSchema(exp, catalog, {});
    const count = (o, f) => Object.values(o).reduce((a, x) => a + f(x), 0);
    ok(Object.keys(catalog).length === tables.length && res.diffs.length === 0 && model.notModelled.length === 0,
      `${database}: ${tables.length} tables, ${count(exp.tables, (x) => x.columns.length)} columns, ${count(exp.tables, (x) => x.indexes.length)} indexes, `
      + `${count(exp.tables, (x) => x.foreignKeys.length)} foreign keys, ${count(exp.tables, (x) => x.checks.length)} checks, `
      + `${count(exp.tables, (x) => x.rls.policies.length)} policies: parsed exactly as PostgreSQL has them`,
      `${Object.keys(catalog).length} in the catalog; ${res.diffs.length} differences: ${res.diffs.slice(0, 8).join(' | ')}; notModelled ${model.notModelled.length}`);
  }
}

if (dockerUp) docker(['rm', '-f', CONTAINER]);
rmSync(SCRATCH, { recursive: true, force: true });
console.log(failures ? `\n${failures} failed` : '\nall passed');
process.exitCode = failures ? 1 : 0;
