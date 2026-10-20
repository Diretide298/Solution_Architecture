#!/usr/bin/env node
/**
 * A [DB] ticket's quick check, end to end: what adam_pull writes and what the starter's
 * .claude/scripts/db-ticket.mjs does with it.
 *
 *   node viewer/mcp/db-ticket-check.mjs              parser, pull, snapshot compare; then, with Docker, the script
 *   node viewer/mcp/db-ticket-check.mjs --package    also the whole package DDL against PostgreSQL 16 (~4 min)
 *
 * **Why this exists** (Chinmay, 20 October 2026). A [DB] ticket's agent rebuilt every migration from
 * an empty database, reasoned about the effect by itself and ran dotnet build and the whole dotnet
 * test suite on every ticket. Now the ticket folder holds expected-schema.json (the package
 * statements that make the ticket's tables, picked out by tools.mjs) and the script applies only the
 * ticket's file to a template copy of the previous state, applies it again, applies the package's
 * statements to a second copy, and compares the two databases whole. So:
 *
 *   1. the parser and the statement picking: a [DB] ticket's kinds, the statements of its tables;
 *   2. the snapshot compare: the ticket's objects, everything else, and a second run;
 *   3. adam_pull, against a stand-in ADAM serving this repository's ticvai/ package: expected-schema.json
 *      and the README section for a [DB] ticket, the baseline in both databases, the failure README,
 *      and for a [BE] ticket a README byte for byte what 41caabcc wrote;
 *   4. with Docker: a developer folder made from the real package DDL - MATCH on the baseline (both
 *      databases) and on a ticket, the template reused and extended, and DIFFERENT / FAILED for a
 *      missing index, an extra table, a changed column, a dropped and an altered earlier table, a
 *      changed CHECK, a changed index WHERE, a weakened policy, a file that fails its second run, one
 *      whose second run changes the schema, one that does not apply, one that BEGINs itself; the
 *      script through a junction; two runs at once in one folder; --full; --clean;
 *   5. with --package: every package statement for every table, picked as tickets pick them, makes
 *      exactly the database the whole package makes (tenant and control), and the parsed shape in
 *      expected-schema.json names every column, index, constraint and policy PostgreSQL has.
 *
 * Exits non-zero on a failure. Docker missing is a named skip of 4 and 5, never a pass.
 */

import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, realpathSync, rmSync, statSync, writeFileSync } from 'node:fs';
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
const { sqlStatements, schemaModel, databaseTicket, ticketStatements, statementTarget, forgetPackageFiles, BY_NAME } = tools;

let failures = 0;
const ok = (cond, what, detail = '') => {
  if (cond) console.log(`  ok    ${what}`);
  else { failures++; console.log(`  FAIL  ${what}${detail ? `\n        ${String(detail).slice(0, 900)}` : ''}`); }
};
const skip = (what, why) => console.log(`  skip  ${what} - ${why}`);
const section = (name) => console.log(`\n${name}`);
const SCRATCH = mkdtempSync(path.join(tmpdir(), 'db-ticket-check-'));
const CHECK_STARTED = Date.now();

// ---- 1. the parser and the statement picking ------------------------------------------------------

section('the DDL parser and the statements a ticket gets');
{
  const stmts = sqlStatements(`-- a comment; with a semicolon
CREATE TABLE a.t (x text DEFAULT 'a;b'); /* block; */
CREATE FUNCTION f() RETURNS void LANGUAGE plpgsql AS $$ BEGIN PERFORM 1; END $$;
SELECT 1`);
  ok(stmts.length === 3 && stmts[0].includes("'a;b'") && stmts[1].includes('PERFORM 1; END'),
    'statements split on ; outside strings, comments and dollar-quoted bodies', JSON.stringify(stmts));

  const files = [
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
    { name: '920-row-level-security.sql', text: `CREATE OR REPLACE FUNCTION platform.helper() RETURNS int LANGUAGE sql AS $$ SELECT 1 $$;
SELECT platform.apply_scope_rls('a.parent'::regclass);
SELECT platform.apply_parent_rls('a.child'::regclass, 'parent_id', 'a.parent'::regclass, 'id');` },
    { name: '930-partitioning.sql', text: `CREATE TABLE IF NOT EXISTS a.child_default PARTITION OF a.child DEFAULT;
CREATE TABLE IF NOT EXISTS a.child_2026_10 PARTITION OF a.child FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
SELECT platform.ensure_month_partitions('a.child'::regclass, 3);` },
    { name: 'V0101__after.sql', text: `ALTER TABLE a.child ADD COLUMN IF NOT EXISTS note text CONSTRAINT child_note_chk CHECK (char_length(note) < 9);
ALTER TABLE a.child ADD COLUMN IF NOT EXISTS status text;
ALTER TABLE a.child ALTER COLUMN amount SET NOT NULL;
INSERT INTO platform.schema_version (version, description, checksum) VALUES ('V0101', 'x', 'y') ON CONFLICT (version) DO NOTHING;` },
  ];
  const model = schemaModel(files);
  const child = model.tables.get('a.child');
  const col = (n) => child?.columns.find((c) => c.name === n);
  ok(col('status')?.notNull && col('status')?.default === "'open'" && col('amount')?.notNull && child.columns.length === 8,
    'the parsed shape: columns, NOT NULL, defaults, ADD COLUMN IF NOT EXISTS once', JSON.stringify(child?.columns));
  ok(child?.checks.map((c) => c.name).join(',') === 'child_status_chk,child_note_chk' && child.foreignKeys.length === 2
    && child.partitionBy === 'RANGE (occurred_at)' && child.defaultPartition, 'checks, keys, partitioning', JSON.stringify(child));
  ok(model.tables.get('a.parent')?.rls.policies[0]?.name === 'parent_scope', 'the 920 helper\'s policy name');

  const tables = ticketStatements(files, { kind: 'tables', tables: ['a.child'] });
  const picked = tables.map((s) => `${s.file}: ${s.sql.slice(0, 40)}`);
  ok(tables.length === 8 && tables.every((s) => statementTarget(s.sql) === 'a.child'),
    'a table\'s statements: its CREATE, its key, index, policy, default partition and after-r1 changes, nothing else', picked.join(' | '));
  ok(!tables.some((s) => /child_2026_10|ensure_month|INSERT/.test(s.sql)), 'a month\'s partition, the partition helper and INSERTs are not picked');
  ok(tables.find((s) => s.file === '900-foreign-keys.sql')?.guard?.references === 'b.scope', 'a foreign key carries its guard (both tables, the name)');
  const baseline = ticketStatements([...files, { name: '000-schemas.sql', text: 'CREATE SCHEMA IF NOT EXISTS a;' }],
    { kind: 'baseline', tables: ['platform.schema_version'] });
  ok(baseline.length === 2 && /CREATE SCHEMA/.test(baseline[0].sql) && /platform\.helper/.test(baseline[1].sql),
    'the baseline: 000-002 and the 920/930 functions only', baseline.map((s) => s.sql.slice(0, 40)).join(' | '));
  const keys = ticketStatements(files, { kind: 'foreign-keys', tables: [], constraints: ['child_venue_fkey'] });
  ok(keys.length === 1 && keys[0].guard.constraint === 'child_venue_fkey', 'the cross-schema keys ticket: its named keys only');

  const kind = (subject, description = '', touches = [{ kind: 'table', id: 'a.t' }]) => databaseTicket({ subject, description }, touches);
  ok(kind('[DB] Migration V0027__access.sql: access (19 tables)', 'Tenant database. Tables: ...')?.kind === 'tables', 'a [DB] migration ticket');
  ok(kind('[DB] Forward migration V1001__identity.sql: identity for X (2 tables)')?.migration === 'V1001__identity.sql', 'a forward migration ticket');
  ok(kind('[DB] Migration V0001__baseline.sql: schemas, extensions')?.kind === 'baseline', 'the baseline');
  const fk = kind('[DB] Migration V0034__cross_schema_foreign_keys.sql (35 keys)', 'ai.policy(tenant_id) -> platform.tenant as policy_tenant_id_fkey; x as b_fkey');
  ok(fk?.kind === 'foreign-keys' && fk.tables.length === 0 && fk.constraints.join() === 'policy_tenant_id_fkey,b_fkey', 'the cross-schema keys, by name', JSON.stringify(fk));
  ok(kind('[BE] Build listPasses') === null && kind('[DB] Monthly partitions: create three months ahead') === null,
    'a [BE] ticket and a [DB] task with no file are not migrations');
  ok(kind('[DB] Forward migration V1114__promotions.sql: promotions')?.forward === true && !kind('[DB] Migration V0025__promotions.sql: promotions')?.forward,
    'V1000 and later is a forward migration');
  const tenantFiles = readdirSync(path.join(PACKAGE, 'backend', 'tenant')).filter((n) => /\.sql$/.test(n))
    .map((name) => ({ name, text: readFileSync(path.join(PACKAGE, 'backend', 'tenant', name), 'utf8') }));
  const batch = ticketStatements(tenantFiles, { kind: 'tables', tables: ['promotions.voucher_batch'], forward: true });
  const into = batch.find((s) => s.guard?.constraint === 'voucher_batch_id_fkey');
  ok(into?.guard.incoming && into.guard.table === 'promotions.voucher',
    'a forward migration also gets the keys into its tables from tables made before it (promotions.voucher.voucher_batch_id_fkey)', JSON.stringify(into?.guard));
  ok(!ticketStatements(tenantFiles, { kind: 'tables', tables: ['promotions.voucher_batch'] }).some((s) => s.guard?.incoming),
    'a first-release migration does not: the cross-schema keys ticket adds those');
}

// ---- 2. the snapshot compare --------------------------------------------------------------------

section('the snapshot compare');
{
  const split = script.splitSql("-- head\nCREATE TABLE a (x text DEFAULT 'a;b');\n\n/* one; /* two; */ */\nSELECT E'it\\'s;';\nDO $x$ BEGIN PERFORM 1; END $x$;\n-- tail only\n");
  ok(split.length === 3 && split[0].line === 2 && split[1].line === 5 && split[2].sql.startsWith('DO $x$') && split[2].line === 6,
    'a file split as the server reads it, with each statement\'s line', JSON.stringify(split));
  const before = { 'table k.old': 'r', 'table k.old column a': 'integer', 'table k.keep': 'r' };
  const expected = { ...before, 'table a.t': 'r', 'table a.t column id': 'uuid not null', 'table a.t constraint t_chk': "CHECK ((s = ANY (ARRAY['x'::text, 'y'::text])))",
    'table a.t policy t_scope': 'permissive for all to public using platform.in_scope(scope_path) with check platform.in_scope(scope_path)', 'function platform.f()': 'abc' };
  const match = script.diffSnapshots({ before, after: { ...expected }, expected, owned: ['a.t'] });
  ok(match.length === 0, 'the same database: no difference', match.join(' | '));
  const after = { ...expected };
  delete after['table k.old column a'];
  after['table k.new'] = 'r';
  after['table a.t constraint t_chk'] = "CHECK ((s = ANY (ARRAY['x'::text])))";
  after['table a.t policy t_scope'] = 'permissive for all to public using (platform.in_scope(scope_path) OR true) with check platform.in_scope(scope_path)';
  delete after['function platform.f()'];
  after['table a.t index t_extra_idx'] = 'CREATE INDEX t_extra_idx ON a.t USING btree (id)';
  const d = script.diffSnapshots({ before, after, expected, owned: ['a.t'] });
  const want = ['k.old: column a was dropped by this file, but it is not part of this ticket', 'k.new: the table was created by this file',
    'a.t: constraint t_chk is CHECK', 'a.t: policy t_scope is permissive', 'function platform.f() is missing', 'a.t: index t_extra_idx is not in the package'];
  ok(want.every((w) => d.some((x) => x.includes(w))) && d.length === want.length, 'each difference said once, in words', d.join(' | '));
  const changed = script.diffSnapshots({ before, after: { ...expected, 'table k.keep': 'r rls true' }, expected, owned: ['a.t'] });
  ok(changed.length === 1 && /k\.keep: the table was changed by this file.*was r; now r rls true/.test(changed[0]), 'a change to another table is named with before and after', changed.join(' | '));
  const again = script.againDiffs({ a: '1', b: '2' }, { a: '1', b: '3', c: '4' });
  ok(again.length === 2 && /changed b/.test(again[0]) && /created c/.test(again[1]), 'what a second run changed', again.join(' | '));
  const atomic = script.splitSql('CREATE FUNCTION f() RETURNS int LANGUAGE sql BEGIN ATOMIC SELECT CASE WHEN true THEN 1 END; SELECT 2; END;\nSELECT 3;');
  ok(atomic.length === 2 && /SELECT 2; END$/.test(atomic[0].sql), 'a BEGIN ATOMIC body is one statement', JSON.stringify(atomic));
  const data = script.dataDiffs(script.splitSql('INSERT INTO a.t VALUES (1);\nTRUNCATE k.old, a.t;\nWITH x AS (SELECT 1) UPDATE platform.schema_version SET checksum = 1;\nCREATE TABLE a.u (id int);'), ['a.t'], 'V9__x.sql');
  ok(data.length === 2 && /statement 2 \(line 2\) writes rows into k\.old/.test(data[0]) && /platform\.schema_version/.test(data[1]),
    'rows written into a table that is not the ticket\'s are named; into its own, not', data.join(' | '));
  const rows = script.backfills({ after: { 'rows a.t': '3', 'rows k.old': '0' }, expected: { 'rows a.t': '0' }, owned: ['a.t'] });
  ok(rows.length === 1 && /a\.t: 3 rows/.test(rows[0]) && script.diffSnapshots({ before: { 'rows a.t': '0' }, after: { 'rows a.t': '3' }, expected: { 'rows a.t': '0' }, owned: ['a.t'] }).length === 0,
    'rows left in the ticket\'s own table are listed as a backfill, not a difference', rows.join(' | '));
}

// ---- 3. adam_pull writes it ------------------------------------------------------------------------

section('adam_pull writes expected-schema.json for a [DB] ticket');
const SUB = ['subscription.contract', 'subscription.module_listing', 'subscription.plan', 'subscription.plan_limit', 'subscription.plan_module'];
const expectedOf = {};
{
  const { buildBackend } = await import(pathToFileURL(path.join(REPO, 'viewer', 'lib', 'backend.mjs')).href);
  const backend = await buildBackend(PACKAGE);
  const tickets = {
    9005: { workPackage: { key: '9005', subject: '[DB] Migration V0005__subscription.sql: subscription (5 tables)', description: `Tenant database. Tables: ${SUB.join(', ')}.` },
      touches: SUB.map((id) => ({ kind: 'table', id })) },
    9001: { workPackage: { key: '9001', subject: '[DB] Migration V0001__baseline.sql: schemas, extensions, migration register, RLS helper functions', description: 'Tables: platform.schema_version.' },
      touches: [{ kind: 'table', id: 'platform.schema_version' }] },
    9034: { workPackage: { key: '9034', subject: '[DB] Migration V0034__cross_schema_foreign_keys.sql (2 keys)',
      description: 'ai.policy(tenant_id) -> platform.tenant as policy_tenant_id_fkey; ai.provider(region_id) -> platform.scope as provider_region_id_fkey.' },
      touches: [{ kind: 'table', id: 'ai.policy' }, { kind: 'table', id: 'ai.provider' }] },
    9006: { workPackage: { key: '9006', subject: '[DB] Migration V0006__transport.sql: transport (1 tables)', description: 'Tenant database.' },
      touches: [{ kind: 'table', id: 'transport.departure' }] },
    9100: { workPackage: { key: '9100', subject: '[BE] Build getPlan', description: 'Builds getPlan.' }, touches: [{ kind: 'table', id: 'subscription.plan' }] },
  };
  let fileReads = 0;
  let failRead = null;
  const client = {
    async projectId() { return 'ticvai'; },
    async layer(route) { return route === 'backend' ? backend : {}; },
    async file(p) {
      fileReads++;
      const full = path.join(PACKAGE, p);
      if (failRead && p.endsWith(failRead)) return { ok: false, status: 500, text: 'broken' };
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
  const read = (key, f) => { const p = path.join(dir, '.adam', 'work', key, f); return existsSync(p) ? readFileSync(p, 'utf8') : null; };

  const one = await pull.run(client, { key: '9005', dir });
  const sub = JSON.parse(read('9005', 'expected-schema.json') ?? 'null');
  expectedOf[9005] = sub;
  const c = sub?.checks?.[0];
  ok(one.found && sub?.checks.length === 1 && c.database === 'tenant' && c.migration === 'V0005__subscription.sql' && Object.keys(c.tables).length === 5,
    'expected-schema.json: one database, the file, the five tables\' shape', JSON.stringify({ ...c, tables: Object.keys(c?.tables ?? {}), statements: c?.statements?.length }));
  ok(c?.statements.length > 10 && c.statements.every((s) => SUB.includes(statementTarget(s.sql))) && c.statements.some((s) => s.file === '920-row-level-security.sql')
    && c.statements.some((s) => s.guard?.references === 'platform.tenant'), 'and the package statements that make them, each about one of them, keys guarded',
  c?.statements.map((s) => s.file).join(', '));
  const readme = read('9005', 'README.md');
  ok(/## Checking this migration/.test(readme) && readme.includes('node .claude/scripts/db-ticket.mjs 9005') && readme.includes('db/tenant/V0005__subscription.sql')
    && /This replaces older instructions for a \[DB\] ticket/.test(readme) && /--full tenant/.test(readme) && !/once a day|pipeline/.test(readme),
  'README.md: the command, that it replaces the older rule, the full run before the merge request, no daily or pipeline promise');
  ok(one.database?.migration === 'db/tenant/V0005__subscription.sql' && /db-ticket\.mjs 9005/.test(one.next) && /replaces older/.test(one.next), 'the answer points at the check', one.next);
  const reads = fileReads;
  await pull.run(client, { key: '9005', dir });
  ok(fileReads === reads, 'a second pull within the minute reads the DDL from memory', `${fileReads - reads} reads`);

  await pull.run(client, { key: '9001', dir });
  const base = JSON.parse(read('9001', 'expected-schema.json') ?? 'null');
  expectedOf[9001] = base;
  ok(base?.checks.map((x) => x.database).join() === 'tenant,control' && base.checks.every((x) => x.kind === 'baseline'
    && x.statements.some((s) => /^CREATE (OR REPLACE )?FUNCTION/i.test(s.sql)) && x.statements.some((s) => s.file === '002-migration-register.sql')),
  'the baseline: one check per database, with 000-002 and the helper functions', JSON.stringify(base?.checks.map((x) => [x.database, x.statements.length])));
  ok(/`db\/tenant\/V0001__baseline\.sql` and `db\/control\/V0001__baseline\.sql`/.test(read('9001', 'README.md')), 'README.md names both files');

  await pull.run(client, { key: '9034', dir });
  const fk = JSON.parse(read('9034', 'expected-schema.json') ?? 'null')?.checks?.[0];
  ok(fk?.kind === 'foreign-keys' && fk.statements.length === 2 && Object.keys(fk.tables).length === 0 && !fk.keysNotInPackageDdl,
    'the cross-schema keys ticket: its two keys, and no tables of its own', JSON.stringify(fk?.statements?.map((s) => s.guard?.constraint)));

  failRead = '910-indexes.sql';
  forgetPackageFiles();
  const broken = await pull.run(client, { key: '9005', dir });
  ok(!read('9005', 'expected-schema.json') && /could not be written \(backend\/tenant\/910-indexes\.sql would not read\)/.test(read('9005', 'README.md'))
    && broken.database?.error, 'a DDL file that will not read: no expected-schema.json left from before, and README.md says why');
  const r = spawnSync(process.execPath, [SCRIPT, '9005'], { cwd: dir, encoding: 'utf8' });
  ok(r.status === 2 && /could not write expected-schema\.json for this ticket/.test(r.stdout) && !/Pull the ticket first/.test(r.stdout),
    'and the script says so, instead of sending the agent to pull again', r.stdout);
  failRead = null;
  forgetPackageFiles();

  await pull.run(client, { key: '9006', dir });
  ok(!/Not in the package DDL/.test(read('9006', 'README.md'))
    && JSON.parse(read('9006', 'expected-schema.json'))?.checks?.[0]?.statements.length > 0, 'a table the DDL has: no "not in the package" note');

  // A [BE] ticket's README is what the connector wrote before this change, byte for byte (but the time).
  const old = path.join(SCRATCH, 'old-connector');
  mkdirSync(old);
  for (const f of ['tools.mjs']) {
    const g = spawnSync('git', ['-C', REPO, 'show', `41caabcc:viewer/mcp/${f}`], { encoding: 'utf8', maxBuffer: 1 << 26 });
    writeFileSync(path.join(old, f), g.stdout);
  }
  const oldTools = await import(pathToFileURL(path.join(old, 'tools.mjs')).href);
  const oldDir = path.join(SCRATCH, 'pulled-old');
  mkdirSync(oldDir);
  const nowBe = await pull.run(client, { key: '9100', dir });
  const thenBe = await oldTools.BY_NAME.get('adam_pull').run(client, { key: '9100', dir: oldDir });
  const strip = (t) => String(t).replace(/Pulled \S+ by/, 'Pulled <time> by');
  const oldReadme = readFileSync(path.join(oldDir, '.adam', 'work', '9100', 'README.md'), 'utf8');
  ok(strip(read('9100', 'README.md')) === strip(oldReadme) && !read('9100', 'expected-schema.json') && !nowBe.database
    && JSON.stringify(nowBe).split(JSON.stringify(dir).slice(1, -1)).join('<dir>') === JSON.stringify(thenBe).split(JSON.stringify(oldDir).slice(1, -1)).join('<dir>'),
  'a [BE] ticket: README.md, the files and the answer are what 41caabcc wrote');
}

// ---- 4. the script, as a developer runs it -----------------------------------------------------

const dockerUp = spawnSync('docker', ['version', '--format', '{{.Server.Version}}'], { encoding: 'utf8' }).status === 0;
const CONTAINER = 'adam-db-ticket-check';
const docker = (args, input) => spawnSync('docker', args, { input, encoding: 'utf8', maxBuffer: 1 << 30 });

async function startContainer() {
  if (docker(['inspect', '-f', '{{.State.Running}}', CONTAINER]).stdout.trim() === 'true') return null;
  docker(['rm', '-f', CONTAINER]);
  const run = docker(['run', '-d', '--name', CONTAINER, '-e', 'POSTGRES_PASSWORD=check', 'pgvector/pgvector:pg16']);
  if (run.status !== 0) return run.stderr;
  for (let i = 0; i < 60; i++) {
    if (docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', 'SELECT 1']).status === 0) return null;
    await new Promise((r) => { setTimeout(r, 500); });
  }
  return 'did not become ready';
}

const pkgRead = (db, f) => readFileSync(path.join(PACKAGE, 'backend', db, f), 'utf8');
const pkgFiles = (db) => readdirSync(path.join(PACKAGE, 'backend', db)).filter((n) => /\.sql$/.test(n)).sort()
  .map((name) => ({ name, text: pkgRead(db, name) }));

/** A developer's migration for `tables`: the package's statements, each safe to run twice. */
function migrationFor(tables, { skipKeysTo = () => false } = {}) {
  return `${ticketStatements(pkgFiles('tenant'), { kind: 'tables', tables })
    .filter((s) => !(s.guard && skipKeysTo(s.guard.references)))
    .map((s) => {
      const add = /^ALTER TABLE ([\w.]+) ADD CONSTRAINT (\w+)/i.exec(s.sql);
      return add ? `ALTER TABLE ${add[1]} DROP CONSTRAINT IF EXISTS ${add[2]};\n${s.sql};` : `${s.sql};`;
    }).join('\n')}\n`;
}

/** A developer's baseline for one database: the package's 000-002 and helper functions. */
function baseline(db) {
  return `SET check_function_bodies = off;\n${ticketStatements(pkgFiles(db), { kind: 'baseline', tables: [] }).map((s) => `${s.sql};`).join('\n')}\n`;
}

// The check's container is the script's own for these runs (it may start it, note its roles, clean them).
const OWNED = { ...process.env, ADAM_DB_CHECK_CONTAINER: CONTAINER };
function runScript(cwd, ...args) {
  const r = spawnSync(process.execPath, [SCRIPT, ...args], { cwd, encoding: 'utf8', env: OWNED });
  return { code: r.status, out: `${r.stdout}${r.stderr}` };
}
function runAsync(cwd, ...args) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [SCRIPT, ...args], { cwd, env: OWNED });
    let out = '';
    child.stdout.on('data', (d) => { out += d; });
    child.stderr.on('data', (d) => { out += d; });
    child.on('close', (code) => resolve({ code, out }));
  });
}

section('the script on a developer folder (Docker)');
if (!dockerUp) {
  skip('the script against PostgreSQL', 'Docker is not running here');
} else if (!expectedOf[9005] || !expectedOf[9001]) {
  ok(false, 'the script needs the expected-schema.json files from section 3');
} else {
  const started = await startContainer();
  ok(started === null, `a throwaway ${CONTAINER} container`, started);
  const repo = path.join(SCRATCH, 'backend');
  const tenant = path.join(repo, 'db', 'tenant');
  const control = path.join(repo, 'db', 'control');
  mkdirSync(tenant, { recursive: true });
  mkdirSync(control, { recursive: true });
  for (const k of [9001, 9005]) {
    mkdirSync(path.join(repo, '.adam', 'work', String(k)), { recursive: true });
    writeFileSync(path.join(repo, '.adam', 'work', String(k), 'expected-schema.json'), JSON.stringify(expectedOf[k], null, 2));
  }
  writeFileSync(path.join(tenant, 'V0001__baseline.sql'), baseline('tenant'));
  writeFileSync(path.join(control, 'V0001__baseline.sql'), baseline('control'));
  const first = runScript(repo, '9001');
  ok(first.code === 0 && (first.out.match(/MATCH: /g) ?? []).length === 2, 'the baseline: MATCH in both databases', first.out);

  writeFileSync(path.join(tenant, 'V0002__kernel.sql'), migrationFor(['kernel.inbox']));
  writeFileSync(path.join(tenant, 'V0008__games.sql'), 'SELECT 1;\n');
  const made = new Set([...SUB, 'kernel.inbox', 'tenancy.device_assignment']);
  const good = migrationFor(SUB, { skipKeysTo: (t) => !made.has(t) });
  const ticketFile = path.join(tenant, 'V0005__subscription.sql');
  const check = (sql) => { writeFileSync(ticketFile, sql); return runScript(repo, '9005'); };

  let t = Date.now();
  const m1 = check(good);
  const ms1 = Date.now() - t;
  ok(m1.code === 0 && /MATCH: 5 tables/.test(m1.out) && /template (built|extended)/.test(m1.out) && /second run: applied again, changed nothing/.test(m1.out),
    `a ticket: the template made, applied twice, the package's statements on a second copy, MATCH (${(ms1 / 1000).toFixed(1)} s)`, m1.out);
  ok(/1 later file left out/.test(m1.out) && /1 foreign key left for a later migration/.test(m1.out), 'a later file is left out; a key to a table not made yet is deferred', m1.out);
  ok(existsSync(path.join(repo, '.adam', 'work', '9005', 'db-check.md')), 'the result is kept in db-check.md');
  t = Date.now();
  const m2 = check(good);
  const ms2 = Date.now() - t;
  ok(m2.code === 0 && /template reused/.test(m2.out) && /\(kept from an earlier run\)/.test(m2.out),
    `run again: the template reused and the package's result kept, MATCH (${(ms2 / 1000).toFixed(1)} s)`, m2.out);
  writeFileSync(path.join(tenant, 'V0003__tenancy.sql'), migrationFor(['tenancy.device_assignment']));
  const m3 = check(good);
  ok(m3.code === 0 && /template extended, 1 applied/.test(m3.out), 'a new earlier file extends the template', m3.out);

  const cases = [
    ['a missing index', good.replace(/^CREATE INDEX IF NOT EXISTS plan_limit_plan_id_idx ON[^\n]*\n/m, ''),
      /DIFFERENT/, /subscription\.plan_limit: index plan_limit_plan_id_idx is missing/],
    ['an extra table and a changed column', `${good}CREATE TABLE IF NOT EXISTS subscription.stray (id uuid PRIMARY KEY);\nALTER TABLE subscription.plan ALTER COLUMN description SET NOT NULL;\n`,
      /subscription\.stray: the table was created by this file, but it is not part of this ticket/, /subscription\.plan: column description is text not null; the package has text/],
    ['an earlier table dropped', `${good}DROP TABLE IF EXISTS tenancy.device_assignment;\n`,
      /tenancy\.device_assignment: the table was dropped by this file, but it is not part of this ticket/, /DIFFERENT/],
    ['an earlier table altered (kernel.inbox)', `${good}ALTER TABLE kernel.inbox ADD COLUMN IF NOT EXISTS note text;\nALTER TABLE kernel.inbox DROP CONSTRAINT IF EXISTS inbox_consumer_chk;\n`,
      /kernel\.inbox: column note was created by this file/, /kernel\.inbox: constraint inbox_consumer_chk was dropped by this file/],
    ['a changed CHECK body', good.replace(/CONSTRAINT plan_cell_tier_chk CHECK \(cell_tier IN \('shared', 'dedicated', 'isolated', 'clientHosted'\)\)/, "CONSTRAINT plan_cell_tier_chk CHECK (cell_tier IN ('shared'))"),
      /subscription\.plan: constraint plan_cell_tier_chk is CHECK \(\(cell_tier = 'shared'::text\)\); the package has CHECK .*'clientHosted'/, /DIFFERENT/],
    ['a changed index WHERE', good.replace(/(CREATE INDEX IF NOT EXISTS plan_limit_plan_id_idx ON subscription\.plan_limit \(plan_id\))/, '$1 WHERE plan_id IS NOT NULL'),
      /subscription\.plan_limit: index plan_limit_plan_id_idx is CREATE INDEX .* WHERE \(plan_id IS NOT NULL\); the package has/, /DIFFERENT/],
    ['a weakened policy', good.replace("SELECT platform.apply_tenant_rls('subscription.plan'::regclass);",
      'ALTER TABLE subscription.plan ENABLE ROW LEVEL SECURITY;\nALTER TABLE subscription.plan FORCE ROW LEVEL SECURITY;\nDROP POLICY IF EXISTS plan_scope ON subscription.plan;\n'
      + 'CREATE POLICY plan_scope ON subscription.plan USING (platform.tenant_root_in_scope() OR true) WITH CHECK (platform.tenant_root_in_scope());'),
    /subscription\.plan: policy plan_scope is permissive for all to public using \(platform\.tenant_root_in_scope\(\) OR true\)/, /DIFFERENT/],
    ['a file that fails its second run', good.replace('CREATE INDEX IF NOT EXISTS plan_limit_plan_id_idx', 'CREATE INDEX plan_limit_plan_id_idx'),
      /FAILED: second run: V0005__subscription\.sql, statement \d+ \(line \d+\) failed/, /already exists[\s\S]*safe to run again/],
    ['a file whose second run changes the schema', `${good}DO $$ BEGIN IF to_regclass('subscription.plan_note') IS NULL THEN CREATE TABLE subscription.plan_note (id int); ELSE ALTER TABLE subscription.plan_note ADD COLUMN IF NOT EXISTS x int; END IF; END $$;\n`,
      /the second run created subscription\.plan_note: column x/, /DIFFERENT/],
    ['a file that does not apply', `${good}ALTER TABLE subscription.nowhere ADD COLUMN x int;\n`,
      /FAILED: first run: V0005__subscription\.sql, statement \d+ \(line \d+\) failed/, /subscription\.nowhere/],
    ['a file that begins its own transaction', `BEGIN;\n${good}COMMIT;\n`, /FAILED: V0005__subscription\.sql, line 1: the file manages its own transaction/, /FAILED/],
    ['a BEGIN ATOMIC function is read whole (and, not being the package\'s, is a difference)',
      `${good}CREATE OR REPLACE FUNCTION subscription.f_atomic() RETURNS int LANGUAGE sql BEGIN ATOMIC SELECT 1; SELECT 2; END;\n`,
      /function subscription\.f_atomic\(\) was created by this file/, /^(?![\s\S]*manages its own transaction)/],
    // What review 2 found outside the snapshot: each must now be a difference.
    ['GRANT on an earlier table', `${good}GRANT ALL ON kernel.inbox TO PUBLIC;\n`, /kernel\.inbox: the table was changed by this file.*acl \{/, /DIFFERENT/],
    ['GRANT on the ticket\'s own table', `${good}GRANT ALL ON subscription.plan TO PUBLIC;\n`, /subscription\.plan: the table is .*acl \{.*; the package has .*acl -/, /DIFFERENT/],
    ['a new owner for an earlier table', `${good}ALTER TABLE kernel.inbox OWNER TO probe_owner;\n`, /kernel\.inbox: the table was changed by this file.*now .*owner probe_owner/, /DIFFERENT/],
    ['an UNLOGGED table', good.replace('CREATE TABLE IF NOT EXISTS subscription.plan_module', 'CREATE UNLOGGED TABLE IF NOT EXISTS subscription.plan_module'),
      /subscription\.plan_module: the table is p?r? ?persistence u|subscription\.plan_module: the table is r persistence u/, /DIFFERENT/],
    ['a storage option', `${good}ALTER TABLE subscription.plan SET (fillfactor = 10);\n`, /subscription\.plan: the table is .*options \{fillfactor=10\}/, /DIFFERENT/],
    ['a replica identity on an earlier table', `${good}ALTER TABLE tenancy.device_assignment REPLICA IDENTITY FULL;\n`, /tenancy\.device_assignment: the table was changed by this file.*replica identity f/, /DIFFERENT/],
    ['a comment on an earlier table', `${good}COMMENT ON TABLE kernel.inbox IS 'x';\n`, /kernel\.inbox: the table was changed by this file.*comment x/, /DIFFERENT/],
    ['a database setting', `${good}DO $$ BEGIN EXECUTE format('ALTER DATABASE %I SET row_security = off', current_database()); END $$;\n`,
      /database settings was changed by this file/, /DIFFERENT/],
    ['an earlier file\'s register row changed', `${good}UPDATE platform.schema_version SET checksum = 'X' WHERE version = 'V0002__kernel.sql';\n`,
      /register V0002__kernel\.sql was changed by this file/, /writes rows into platform\.schema_version/],
    ['an earlier file\'s register row deleted', `${good}DELETE FROM platform.schema_version WHERE version = 'V0002__kernel.sql';\n`,
      /register V0002__kernel\.sql was dropped by this file/, /DIFFERENT/],
    ['an earlier table truncated', `${good}TRUNCATE tenancy.device_assignment;\n`, /writes rows into tenancy\.device_assignment, which is not one of this ticket's tables/, /DIFFERENT/],
    ['rows put into an earlier table where the text cannot show it', `${good}DO $$ BEGIN INSERT INTO kernel.inbox (consumer, event_id, processed_at) VALUES ('x', '00000000-0000-0000-0000-000000000001', now()) ON CONFLICT DO NOTHING; END $$;\n`,
      /kernel\.inbox: its row count was changed by this file/, /DIFFERENT/],
    // What review 3 found: refused by their text, and, hidden in a DO block, seen by the snapshot.
    ['triggers switched off on an earlier table', `${good}ALTER TABLE tenancy.device_assignment DISABLE TRIGGER ALL;\n`,
      /statement \d+ \(line \d+\) switches triggers off or to replica mode/, /may not be in a ticket's file/],
    ['triggers switched off on the ticket\'s own table', `${good}ALTER TABLE subscription.plan_limit DISABLE TRIGGER ALL;\n`, /switches triggers off/, /DIFFERENT/],
    ['triggers switched off inside a DO block', `${good}DO $$ BEGIN EXECUTE 'ALTER TABLE subscription.plan_limit DISABLE TRIGGER ALL'; END $$;\n`,
      /subscription\.plan_limit: the table is .*triggers not on [1-9]/, /DIFFERENT/],
    ['ALTER DEFAULT PRIVILEGES', `${good}ALTER DEFAULT PRIVILEGES GRANT ALL ON TABLES TO PUBLIC;\n`, /changes the privileges of tables not made yet/, /DIFFERENT/],
    ['ALTER DEFAULT PRIVILEGES IN SCHEMA, inside a DO block', `${good}DO $$ BEGIN EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA kernel GRANT ALL ON TABLES TO PUBLIC'; END $$;\n`,
      /default privileges postgres in kernel for r was created by this file/, /DIFFERENT/],
    ['GRANT on the database', `${good}DO $$ BEGIN EXECUTE format('GRANT ALL ON DATABASE %I TO PUBLIC', current_database()); END $$;\n`,
      /database was changed by this file/, /DIFFERENT/],
    ['a rule on an earlier table', `${good}CREATE RULE r_ignore AS ON INSERT TO kernel.inbox DO INSTEAD NOTHING;\n`, /adds a rule/, /DIFFERENT/],
    ['a rule hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'CREATE OR REPLACE RULE r_ignore AS ON INSERT TO kernel.inbox DO INSTEAD NOTHING'; END $$;\n`,
      /kernel\.inbox: rule r_ignore was created by this file/, /DIFFERENT/],
    ['a publication', `${good}DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'p_all') THEN CREATE PUBLICATION p_all FOR ALL TABLES; END IF; END $$;\n`,
      /publication p_all was created by this file/, /DIFFERENT/],
    ['a constraint on the default partition of an earlier table', `${good}ALTER TABLE kernel.inbox_default DROP CONSTRAINT IF EXISTS probe_no;\nALTER TABLE kernel.inbox_default ADD CONSTRAINT probe_no CHECK (false) NOT VALID;\n`,
      /kernel\.inbox_default: constraint probe_no was created by this file/, /DIFFERENT/],
    ['row-level security on the default partition', `${good}ALTER TABLE kernel.inbox_default ENABLE ROW LEVEL SECURITY;\n`,
      /kernel\.inbox: default partition kernel\.inbox_default was changed by this file.*rls true/, /DIFFERENT/],
    ['a DELETE inside a WITH', `${good}WITH d AS (DELETE FROM kernel.inbox RETURNING 1) SELECT count(*) FROM d;\n`,
      /writes rows into kernel\.inbox, which is not one of this ticket's tables/, /DIFFERENT/],
    ['a role made inside a DO block (it stays in the server until --clean)', `${good}DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'probe_back') THEN CREATE ROLE probe_back LOGIN; END IF; END $$;\n`,
      /this file changed server roles .*probe_back/, /run --clean afterwards/],
    // What review 4 found: privileges the snapshot did not judge, refused by text; hidden, seen.
    ['role membership for another role', `${good}GRANT pg_write_all_data TO probe_owner;\n`, /changes role membership/, /DIFFERENT/],
    ['role membership for the migration role', `${good}GRANT pg_read_all_data TO CURRENT_USER;\n`, /changes role membership/, /DIFFERENT/],
    ['a privilege on a parameter', `${good}GRANT SET ON PARAMETER work_mem TO PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['a privilege on a tablespace', `${good}GRANT CREATE ON TABLESPACE pg_default TO PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['a privilege on a language', `${good}REVOKE USAGE ON LANGUAGE plpgsql FROM PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['replica mode through set_config', `${good}SELECT set_config('session_replication_role', 'replica', true);\n`, /through set_config/, /DIFFERENT/],
    ['role membership hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'GRANT pg_read_all_data TO postgres'; END $$;\n`,
      /this file changed server role memberships .*postgres in pg_read_all_data/, /run --clean afterwards/],
    ['a role attribute hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'ALTER ROLE probe_owner BYPASSRLS'; END $$;\n`,
      /this file changed server roles .*probe_owner \(bypassrls\)/, /DIFFERENT/],
    ['a language privilege hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'REVOKE USAGE ON LANGUAGE plpgsql FROM PUBLIC'; END $$;\n`,
      /language plpgsql was changed by this file/, /DIFFERENT/],
    ['a connection limit hidden in a DO block', `${good}DO $$ BEGIN EXECUTE format('ALTER DATABASE %I CONNECTION LIMIT 50', current_database()); END $$;\n`,
      /database was changed by this file.*connection limit 50/, /DIFFERENT/],
  ];
  docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-qc', 'DROP ROLE IF EXISTS probe_owner; CREATE ROLE probe_owner']);
  for (const [what, sql, a, b] of cases) {
    const r = check(sql);
    ok(r.code === 1 && a.test(r.out) && b.test(r.out), what, r.out);
  }
  const path1 = check(`SET search_path = subscription, public;\n${good}`);
  ok(path1.code === 0 && /MATCH: 5 tables/.test(path1.out), 'a file that sets search_path still matches (names print the same in every snapshot)', path1.out);
  const path2 = check(`SET search_path = subscription, public;\n${good}INSERT INTO module_listing (id, module_code) VALUES ('00000000-0000-0000-0000-000000000002', 'core') ON CONFLICT (id) DO NOTHING;\n`);
  ok(path2.code === 0 && /MATCH/.test(path2.out) && /subscription\.module_listing: 1 rows/.test(path2.out),
    'an unqualified backfill after SET search_path is read as the ticket\'s own table', path2.out);
  const path3 = check(`SET LOCAL search_path = subscription, public; -- the file's own transaction\n${good}INSERT INTO module_listing (id, module_code) VALUES ('00000000-0000-0000-0000-000000000003', 'core') ON CONFLICT (id) DO NOTHING;\n`);
  ok(path3.code === 0 && /MATCH/.test(path3.out) && /subscription\.module_listing: 1 rows/.test(path3.out),
    'SET LOCAL search_path is followed too, with a comment on its line', path3.out);
  const words = check(`${good}ALTER TABLE subscription.plan\n-- a backfill here must not DISABLE TRIGGER: the keys are triggers\nALTER COLUMN description DROP NOT NULL;\n`);
  ok(words.code === 0 && /MATCH: 5 tables/.test(words.out), 'a refused word in a comment inside a statement is not a refusal', words.out);
  const backfill = check(`${good}INSERT INTO subscription.module_listing (id, module_code) VALUES ('00000000-0000-0000-0000-000000000001', 'core') ON CONFLICT (id) DO NOTHING;\n`);
  ok(backfill.code === 0 && /MATCH/.test(backfill.out) && /rows this file leaves in the ticket's own tables[\s\S]*subscription\.module_listing: 1 rows/.test(backfill.out),
    'rows in the ticket\'s own table: MATCH, with the backfill listed for the person to judge', backfill.out);

  // A run killed while it builds the template: the next run must not trust what it left.
  writeFileSync(path.join(tenant, 'V0004__slow.sql'), 'SELECT pg_sleep(8);\n');
  writeFileSync(ticketFile, good);
  const killed = spawn(process.execPath, [SCRIPT, '9005'], { cwd: repo, env: OWNED });
  await new Promise((r) => { setTimeout(r, 4500); });
  killed.kill();
  await new Promise((r) => { setTimeout(r, 500); });
  const dbsAfterKill = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT string_agg(datname || ':' || coalesce(shobj_description(oid, 'pg_database'), ''), ' ') FROM pg_database WHERE datname LIKE 'adam\\_%\\_base' OR datname LIKE 'adam\\_%\\_build'"]).stdout;
  ok(/_build:\{"complete":false,/.test(dbsAfterKill) && !/V0004__slow/.test(dbsAfterKill.replace(/_build:[^ ]*/g, '')),
    'killed half way: the build is under its temporary name, and the template does not list the file', dbsAfterKill);
  const resumed = check(good);
  ok(resumed.code === 0 && /template extended, 1 applied/.test(resumed.out) && /MATCH: 5 tables/.test(resumed.out),
    'the next run drops the half-built one and builds again, then MATCH', resumed.out);
  rmSync(path.join(tenant, 'V0004__slow.sql'));
  const leftover = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT count(*) FROM pg_database WHERE datname LIKE 'adam\\_%\\_build'"]).stdout.trim();
  ok(leftover === '0', 'no half-built database is left', leftover);

  // Through a junction, as a folder reached another way would run it.
  const link = path.join(SCRATCH, 'scripts-link');
  spawnSync('cmd', ['/c', 'mklink', '/J', link, path.dirname(SCRIPT)], { encoding: 'utf8' });
  writeFileSync(ticketFile, good);
  const viaLink = spawnSync(process.execPath, [path.join(link, 'db-ticket.mjs'), '9005'], { cwd: repo, encoding: 'utf8', env: OWNED });
  ok(viaLink.status === 0 && /MATCH: 5 tables/.test(viaLink.stdout), 'the script reached through a junction runs (it used to print nothing and exit 0)', `${viaLink.status} ${viaLink.stdout}`);

  // Two at once in one folder: one waits for the other, both match.
  const [p1, p2] = await Promise.all([runAsync(repo, '9005'), runAsync(repo, '9005')]);
  ok(p1.code === 0 && p2.code === 0 && /Waiting for another check in this folder/.test(p1.out + p2.out), 'two runs at once in one folder: one waits, both MATCH', `${p1.out}\n---\n${p2.out}`);

  // A second folder gets databases of its own.
  const twin = path.join(SCRATCH, 'backend-twin');
  spawnSync('cmd', ['/c', 'xcopy', '/E', '/I', '/Q', repo, twin], { encoding: 'utf8' });
  const tw = runScript(twin, '9005');
  ok(tw.code === 0 && /template built/.test(tw.out), 'another folder builds its own template and leaves this one\'s alone', tw.out);

  const full = runScript(repo, '--full', 'tenant');
  ok(full.code === 0 && /MATCH: db\/tenant applies to an empty database: 5 files, once each, in order/.test(full.out), '--full: every file once, in order, from empty', full.out);
  // An applied file from before the run-twice rule: it stays as it is, and nothing fails on it.
  writeFileSync(path.join(tenant, 'V0004__once.sql'), 'CREATE TABLE kernel.once (id int);\n');
  const fullOld = runScript(repo, '--full', 'tenant');
  const ticketOld = check(good);
  ok(fullOld.code === 0 && /MATCH/.test(fullOld.out) && ticketOld.code === 0 && /MATCH: 5 tables/.test(ticketOld.out),
    'an earlier file that cannot run twice: --full and the ticket both MATCH (only the ticket\'s own file runs twice)', `${fullOld.out}\n${ticketOld.out}`);
  rmSync(path.join(tenant, 'V0004__once.sql'));
  writeFileSync(path.join(tenant, 'V0009__bad.sql'), 'ALTER TABLE kernel.nowhere ADD COLUMN x int;\n');
  const fullBad = runScript(repo, '--full', 'tenant');
  ok(fullBad.code === 1 && /FAILED: from empty: V0009__bad\.sql, statement 1 \(line 1\) failed/.test(fullBad.out), '--full: a file that does not apply fails, naming it', fullBad.out);
  rmSync(path.join(tenant, 'V0009__bad.sql'));

  const missing = runScript(repo, '9999');
  ok(missing.code === 2 && /Pull the ticket first/.test(missing.out), 'a ticket not pulled: exit 2 and what to do', missing.out);
  const badDb = runScript(repo, '--full', 'x;drop');
  ok(badDb.code === 2 && /is not a database name/.test(badDb.out), 'a database name that is not one is refused', badDb.out);
  docker(['stop', CONTAINER]);
  const stoppedRun = spawnSync(process.execPath, [SCRIPT, '9005', '--container', CONTAINER], { cwd: repo, encoding: 'utf8' });
  const stopped = { code: stoppedRun.status, out: stoppedRun.stdout + stoppedRun.stderr };
  ok(stopped.code === 2 && /^Ticket 9005: /.test(stopped.out) && /^Ticket 9005: /.test(readFileSync(path.join(repo, '.adam', 'work', '9005', 'db-check.md'), 'utf8').split('\n')[2])
    && /is not running; start it yourself/.test(stopped.out)
    && docker(['inspect', '-f', '{{.State.Running}}', CONTAINER]).stdout.trim() === 'false', '--container never starts someone else\'s container', stopped.out);
  docker(['start', CONTAINER]);
  await startContainer();
  for (let i = 0; i < 60 && docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', 'SELECT 1']).status !== 0; i++) await new Promise((r) => { setTimeout(r, 500); });
  const cleaned = runScript(repo, '--clean');
  const left = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT count(*) FROM pg_database WHERE datname LIKE 'adam\\_%'"]).stdout.trim();
  ok(cleaned.code === 0 && /Dropped this folder's \d+ databases \(adam_/.test(cleaned.out) && Number(left) > 0, '--clean drops this folder\'s databases and not the other folder\'s', `${cleaned.out} ${left} left`);
  const roles = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT string_agg(rolname, ',') FROM pg_roles WHERE rolname IN ('probe_back', 'probe_owner')"]).stdout.trim();
  ok(/Removed 2 roles a file had made \((probe_back, probe_owner|probe_owner, probe_back)\)/.test(cleaned.out) && roles === '',
    '--clean removes the roles made after the container was first set up, in the check\'s own container', `${cleaned.out} [${roles}]`);
  const membership = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT count(*) FROM pg_auth_members a JOIN pg_roles m ON m.oid = a.member JOIN pg_roles g ON g.oid = a.roleid WHERE m.rolname = 'postgres' AND g.rolname = 'pg_read_all_data'"]).stdout.trim();
  ok(/Revoked 1 role membership a file had granted \(postgres in pg_read_all_data\)/.test(cleaned.out) && membership === '0',
    '--clean revokes the role memberships granted after the container was first set up', `${cleaned.out} [${membership}]`);

  // Another folder's databases, last used more than two weeks ago: kept while that folder holds its
  // lock (it may be building), dropped once it does not, with its kept snapshots.
  const twinId = createHash('sha256').update(realpathSync.native(twin).toLowerCase()).digest('hex').slice(0, 8);
  const twinDbs = () => docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', `SELECT count(*) FROM pg_database WHERE datname LIKE 'adam\\_${twinId}\\_%'`]).stdout.trim();
  const stale = docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', `SELECT shobj_description(oid, 'pg_database') FROM pg_database WHERE datname = 'adam_${twinId}_tenant_base'`]).stdout.trim();
  docker(['exec', '-i', CONTAINER, 'psql', '-U', 'postgres', '-q', '-f', '-'],
    `COMMENT ON DATABASE adam_${twinId}_tenant_base IS '${JSON.stringify({ ...JSON.parse(stale), used: '2026-09-01' }).replace(/'/g, "''")}';\n`);
  const twinLock = path.join(tmpdir(), `adam-db-ticket-${twinId}.lock`);
  writeFileSync(twinLock, String(process.pid));
  writeFileSync(ticketFile, good);
  const held = runScript(repo, '9005');
  const keptWhileHeld = twinDbs();
  rmSync(twinLock, { force: true });
  const freed = runScript(repo, '9005');
  ok(held.code === 0 && Number(keptWhileHeld) > 0 && !/dropped \d+ database/.test(held.out),
    'a stale folder that holds its lock (running or building) is left alone', `${keptWhileHeld} kept\n${held.out}`);
  ok(freed.code === 0 && twinDbs() === '0' && /^Ticket 9005: db\/tenant\/V0005__subscription\.sql\n- dropped \d+ databases left over or unused for 14 days/.test(freed.out)
    && !readdirSync(tmpdir()).some((n) => n.startsWith(`adam-db-ticket-${twinId}-`)),
  'once free, its databases and kept snapshots go after 14 days unused; the Ticket line still comes first', freed.out);
}

// ---- 5. the whole package against PostgreSQL ----------------------------------------------------

section('the whole package DDL against PostgreSQL (--package)');
if (!PACKAGE_RUN) {
  skip('every table of tenant and control', 'run with --package (about four minutes)');
} else if (!dockerUp) {
  skip('every table of tenant and control', 'Docker is not running here');
} else {
  const started = await startContainer();
  ok(started === null, `the ${CONTAINER} container`, started);
  const psql = (db, sql) => docker(['exec', '-i', CONTAINER, 'psql', '-X', '-q', '-At', '-U', 'postgres', '-d', db, '-v', 'ON_ERROR_STOP=1', '-f', '-'], sql);
  // The package creates no pii.subject_kind or pii.contact_kind; give them one so 010-pii applies.
  const types = "CREATE TYPE pii.subject_kind AS ENUM ('a'); CREATE TYPE pii.contact_kind AS ENUM ('a');\n";
  for (const database of ['tenant', 'control']) {
    const files = pkgFiles(database);
    for (const n of ['pkg', 'picked']) {
      docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-qc', `DROP DATABASE IF EXISTS ${n}_${database}`]);
      docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-qc', `CREATE DATABASE ${n}_${database}`]);
    }
    const t = Date.now();
    let applyError = null;
    for (const f of files) {
      const sql = database === 'tenant' && f.name === '010-pii.sql' ? types + f.text : f.text;
      const r = psql(`pkg_${database}`, sql);
      if (r.status !== 0) { applyError = `${f.name}: ${r.stderr}`; break; }
    }
    ok(!applyError, `${database}: the package applies to an empty database (${files.length} files, ${((Date.now() - t) / 1000).toFixed(0)} s)`, applyError);
    if (applyError) continue;
    const model = schemaModel(files);
    const tables = [...model.tables.keys()];
    // What every ticket would be given, put together: the baseline, then each table's statements.
    const picked = [...ticketStatements(files, { kind: 'baseline', tables: [] }), ...ticketStatements(files, { kind: 'tables', tables })];
    const ordered = [...picked.filter((s) => /^00[0-2]-/.test(s.file)), ...picked.filter((s) => !/^00[0-2]-/.test(s.file))];
    const pickedSql = `SET check_function_bodies = off;\n${database === 'tenant' ? types.replace('CREATE TYPE pii.subject_kind', 'CREATE SCHEMA IF NOT EXISTS pii; CREATE TYPE pii.subject_kind') : ''}`
      + ordered.map((s) => `${s.sql};`).join('\n');
    const pr = psql(`picked_${database}`, pickedSql);
    ok(pr.status === 0, `${database}: the statements tickets are given apply in package order`, pr.stderr);
    const snap = (db) => {
      // The package's own register rows (V01nn INSERTs) are data no ticket is given; left out.
      const s = JSON.parse(psql(db, script.SNAPSHOT_SETUP + script.snapshotSql((body) => `SELECT ${body};\n`)).stdout.trim() || '{}');
      for (const k of Object.keys(s)) if (k.startsWith('register ')) delete s[k];
      return s;
    };
    const whole = snap(`pkg_${database}`);
    const fromTickets = snap(`picked_${database}`);
    const diff = script.againDiffs(whole, fromTickets);
    ok(diff.length === 0 && Object.keys(whole).length > 1000,
      `${database}: ${Object.keys(whole).length} objects; the picked statements make exactly what the whole package makes`, diff.slice(0, 10).join(' | '));
    const missing = [];
    for (const [name, shape] of model.tables) {
      const keys = new Set(Object.keys(whole).filter((k) => k.startsWith(`table ${name} `)));
      const cols = [...keys].filter((k) => k.startsWith(`table ${name} column `)).length;
      if (cols !== shape.columns.length) missing.push(`${name}: ${shape.columns.length} columns parsed, ${cols} in PostgreSQL`);
      for (const c of shape.columns) if (!keys.has(`table ${name} column ${c.name}`)) missing.push(`${name}.${c.name}`);
      for (const i of shape.indexes) if (!keys.has(`table ${name} index ${i.name}`)) missing.push(`${name} index ${i.name}`);
      for (const k of [...shape.checks, ...shape.foreignKeys, ...shape.unique, shape.primaryKey].filter((x) => x?.name)) if (!keys.has(`table ${name} constraint ${k.name}`)) missing.push(`${name} constraint ${k.name}`);
      for (const p of shape.rls.policies) if (!keys.has(`table ${name} policy ${p.name}`)) missing.push(`${name} policy ${p.name}`);
    }
    ok(missing.length === 0 && model.notModelled.length === 0, `${database}: the parsed shape of all ${tables.length} tables names what PostgreSQL has`, missing.slice(0, 10).join(' | '));
  }
}

if (dockerUp) docker(['rm', '-f', CONTAINER]);
// The script keeps snapshots in the temp folder; this run's go with it.
const ids = readdirSync(SCRATCH).map((d) => createHash('sha256').update(realpathSync.native(path.join(SCRATCH, d)).toLowerCase()).digest('hex').slice(0, 8));
for (const f of readdirSync(tmpdir()).filter((n) => ids.some((id) => n.startsWith(`adam-db-ticket-${id}-`)) && n.endsWith('.json'))) {
  const p = path.join(tmpdir(), f);
  if (statSync(p).mtimeMs >= CHECK_STARTED) rmSync(p, { force: true });
}
rmSync(SCRATCH, { recursive: true, force: true });
console.log(failures ? `\n${failures} failed` : '\nall passed');
process.exitCode = failures ? 1 : 0;
