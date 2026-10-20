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

  // r8 final re-walk, expected-schema-statements-miss-schema-move (MIG-PLATFORM #27665 and #28358): a table's
  // statements belong to the ticket that owns its final name, whatever names it had on the way. Its CREATE, keys,
  // indexes and row-level security under every earlier name, and the RENAME TO or SET SCHEMA itself, in package order.
  const moves = [
    { name: '010-p.sql', text: `CREATE TABLE IF NOT EXISTS p.link (id uuid PRIMARY KEY NOT NULL);
CREATE TABLE IF NOT EXISTS p.request (id uuid PRIMARY KEY NOT NULL, link_id uuid NOT NULL);
CREATE TABLE IF NOT EXISTS p.hold (id uuid PRIMARY KEY NOT NULL);
CREATE TABLE IF NOT EXISTS q.line (id uuid PRIMARY KEY NOT NULL, hold_id uuid);` },
    { name: '900-foreign-keys.sql', text: `ALTER TABLE p.request ADD CONSTRAINT request_link_id_fkey FOREIGN KEY (link_id) REFERENCES p.link(id);
ALTER TABLE q.line ADD CONSTRAINT line_hold_id_fkey FOREIGN KEY (hold_id) REFERENCES p.hold(id);` },
    { name: '910-indexes.sql', text: `CREATE INDEX IF NOT EXISTS request_link_id_idx ON p.request (link_id);
CREATE INDEX IF NOT EXISTS hold_made_idx ON p.hold (id);
CREATE INDEX IF NOT EXISTS hold_made_idx ON q.line (id);` },
    { name: '920-row-level-security.sql', text: `SELECT platform.apply_tenant_rls('p.request'::regclass);
SELECT platform.apply_tenant_rls('p.hold'::regclass);` },
    { name: 'V0103a__names.sql', text: `DO $$ BEGIN IF to_regclass('p.link') IS NOT NULL AND to_regclass('s.link') IS NULL THEN ALTER TABLE p.link SET SCHEMA s; END IF; END $$;
DO $$ BEGIN IF to_regclass('p.hold') IS NOT NULL AND to_regclass('p.reservation') IS NULL THEN ALTER TABLE p.hold RENAME TO reservation; END IF; END $$;
DO $$ BEGIN IF to_regclass('p.hold_made_idx') IS NOT NULL THEN ALTER INDEX p.hold_made_idx RENAME TO reservation_made_idx; END IF; END $$;
DO $$ DECLARE p name; BEGIN IF to_regclass('p.reservation') IS NOT NULL THEN FOR p IN SELECT polname FROM pg_policy WHERE polrelid = to_regclass('p.reservation') AND left(polname, 5) = 'hold_' LOOP EXECUTE format('ALTER POLICY %I ON p.reservation RENAME TO %I', p, CASE WHEN substr(p, 5) = '_scope' THEN left('reservation', 57) ELSE left('reservation', 55) END || substr(p, 5)); END LOOP; END IF; END $$;` },
    { name: 'V0105a__names.sql', text: `DO $$ BEGIN IF to_regclass('p.request') IS NOT NULL AND to_regclass('s.request') IS NULL THEN ALTER TABLE p.request SET SCHEMA s; END IF; END $$;` },
    { name: 'V0108__after.sql', text: `ALTER TABLE s.request ADD COLUMN IF NOT EXISTS cell_results jsonb;
ALTER TABLE p.reservation ADD COLUMN IF NOT EXISTS note text;
DO $$ BEGIN IF to_regclass('p.reservation_made_idx') IS NOT NULL THEN DROP INDEX p.reservation_made_idx; END IF; END $$;` },
  ];
  // Each picked statement against what it must be, in order: [file, a pattern of its text].
  const same = (list, want) => list.length === want.length && want.every(([file, rx], i) => list[i].file === file && rx.test(list[i].sql));
  const brief = (list) => list.map((s) => `${s.file}: ${s.sql.replace(/^DO \$\$ (DECLARE p name; )?BEGIN IF .*? THEN /, '').slice(0, 60)}`);
  const moved = ticketStatements(moves, { kind: 'tables', tables: ['s.request', 's.link'] });
  ok(same(moved, [
    ['010-p.sql', /^CREATE TABLE IF NOT EXISTS p\.link /],
    ['010-p.sql', /^CREATE TABLE IF NOT EXISTS p\.request /],
    ['900-foreign-keys.sql', /^ALTER TABLE p\.request ADD CONSTRAINT request_link_id_fkey .* REFERENCES p\.link\(id\)$/],
    ['910-indexes.sql', /^CREATE INDEX IF NOT EXISTS request_link_id_idx ON p\.request /],
    ['920-row-level-security.sql', /^SELECT platform\.apply_tenant_rls\('p\.request'/],
    ['V0103a__names.sql', /ALTER TABLE p\.link SET SCHEMA s;/],
    ['V0105a__names.sql', /ALTER TABLE p\.request SET SCHEMA s;/],
    ['V0108__after.sql', /^ALTER TABLE s\.request ADD COLUMN IF NOT EXISTS cell_results/],
  ]) && moved[2].guard?.table === 'p.request' && moved[2].guard.references === 'p.link',
  '**a moved table (platform.dsar_request -> sync.dsar_request): its CREATE, key, index and policy under the old schema, the SET SCHEMA itself, then what names it in the new one, in package order**',
  brief(moved).join(' | '));
  const renamed = ticketStatements(moves, { kind: 'tables', tables: ['p.reservation'] });
  ok(same(renamed, [
    ['010-p.sql', /^CREATE TABLE IF NOT EXISTS p\.hold /],
    ['910-indexes.sql', /^CREATE INDEX IF NOT EXISTS hold_made_idx ON p\.hold /],
    ['920-row-level-security.sql', /^SELECT platform\.apply_tenant_rls\('p\.hold'/],
    ['V0103a__names.sql', /ALTER TABLE p\.hold RENAME TO reservation;/],
    ['V0103a__names.sql', /ALTER INDEX p\.hold_made_idx RENAME TO reservation_made_idx;/],
    ['V0103a__names.sql', /ALTER POLICY %I ON p\.reservation RENAME TO %I/],
    ['V0108__after.sql', /^ALTER TABLE p\.reservation ADD COLUMN IF NOT EXISTS note/],
    ['V0108__after.sql', /DROP INDEX p\.reservation_made_idx;/],
  ]), '**a renamed table (catalogue.inventory_hold -> inventory_reservation): the same, with its index and policy renames and a later DROP INDEX under the new name; q.line\'s index of the same name is not its**',
  brief(renamed).join(' | '));
  const line = ticketStatements(moves, { kind: 'tables', tables: ['q.line'] });
  const lineKey = line.find((s) => s.guard?.constraint === 'line_hold_id_fkey');
  ok(line.length === 3 && /REFERENCES p\.reservation\(id\)$/.test(lineKey?.sql) && lineKey.guard.references === 'p.reservation' && lineKey.guard.table === 'q.line'
    && line.some((s) => /hold_made_idx ON q\.line/.test(s.sql)) && !line.some((s) => /RENAME/.test(s.sql)),
  'another ticket\'s key into a renamed table names it as that table\'s ticket left it (REFERENCES p.reservation, not p.hold), guard too', brief(line).join(' | '));
  const request = ticketStatements(moves, { kind: 'tables', tables: ['s.request'] });
  const requestKey = request.find((s) => s.guard?.constraint === 'request_link_id_fkey');
  ok(!request.some((s) => /p\.link SET SCHEMA|TABLE IF NOT EXISTS p\.link/.test(s.sql)) && /REFERENCES s\.link\(id\)$/.test(requestKey?.sql) && requestKey.guard.references === 's.link'
    && request.some((s) => /p\.request SET SCHEMA s/.test(s.sql)),
  'a table moved with another ticket\'s: that move is not its, and its key into the other names it where that ticket left it (s.link)', brief(request).join(' | '));
  const movedModel = schemaModel(moves).tables;
  const reservation = movedModel.get('p.reservation');
  ok(movedModel.get('s.request')?.foreignKeys[0]?.references === 's.link' && movedModel.get('q.line')?.foreignKeys[0]?.references === 'p.reservation'
    && !movedModel.has('p.request') && !movedModel.has('p.hold')
    && reservation?.rls.policies.map((p) => p.name).join() === 'reservation_scope' && reservation.indexes.length === 0
    && movedModel.get('q.line')?.indexes.map((i) => i.name).join() === 'hold_made_idx',
  '**the expected shape: a key into a moved or renamed table names it where it is now (PostgreSQL follows the table), and its policies and indexes are renamed with it**',
  JSON.stringify([...movedModel.values()].map((t) => [t.name, t.foreignKeys.map((k) => k.references), t.rls.policies.map((p) => p.name), t.indexes.map((i) => i.name)])));

  // The same on the real r8 package: MIG-PLATFORM (#27665) and V1241__sync.sql (#28358).
  const platform = ['platform.audit_read', 'platform.audit_record', 'platform.denomination', 'platform.device', 'platform.idempotency_record',
    'platform.outbox', 'platform.outlet', 'platform.outlet_opening_hour', 'platform.region_settings', 'platform.sale_board', 'platform.sale_board_page',
    'platform.sale_board_tile', 'platform.scope', 'platform.tenant', 'platform.venue_settings', 'platform.workstation', 'sync.dsar_request', 'sync.guest_link'];
  const mig = ticketStatements(tenantFiles, { kind: 'tables', tables: platform });
  const at = (rx) => mig.findIndex((s) => rx.test(s.sql));
  const need = [/^CREATE TABLE IF NOT EXISTS platform\.dsar_request\b/, /^CREATE TABLE IF NOT EXISTS platform\.guest_link\b/,
    /^ALTER TABLE platform\.dsar_request ADD CONSTRAINT dsar_request_guest_link_id_fkey\b/, /^ALTER TABLE platform\.dsar_request ADD CONSTRAINT dsar_request_request_id_fkey\b/,
    /^CREATE INDEX IF NOT EXISTS dsar_request_guest_link_id_idx ON platform\.dsar_request\b/, /^CREATE INDEX IF NOT EXISTS dsar_request_request_id_idx ON platform\.dsar_request\b/,
    /^SELECT platform\.apply_parent_rls\('platform\.dsar_request'/, /^SELECT platform\.apply_tenant_rls\('platform\.guest_link'/,
    /ALTER TABLE platform\.guest_link SET SCHEMA sync/, /ALTER TABLE platform\.dsar_request SET SCHEMA sync/,
    /^ALTER TABLE sync\.dsar_request ADD COLUMN IF NOT EXISTS cell_results\b/];
  const where = need.map(at);
  ok(where.every((i) => i >= 0) && where[9] < where[10] && where[0] < where[9] && mig[where[9]].file.startsWith('V0105a__')
    && new Set(mig.map((s) => s.file)).has(mig[where[9]].file),
  '**MIG-PLATFORM: sync.dsar_request and sync.guest_link get their CREATEs, keys, indexes and policies under platform, the two moves (V0103a, V0105a) and then V0108**',
  need.map((rx, i) => `${where[i]} ${rx.source.slice(0, 50)}`).join(' | '));
  const sync = ticketStatements(tenantFiles, { kind: 'tables', tables: ['sync.cross_region_entitlement', 'sync.wallet_authorisation'], forward: true });
  const syncKey = (name) => sync.find((s) => s.guard?.constraint === name);
  ok(sync.some((s) => /^CREATE TABLE IF NOT EXISTS platform\.cross_region_entitlement\b/.test(s.sql)) && sync.some((s) => /^CREATE TABLE IF NOT EXISTS platform\.wallet_authorisation\b/.test(s.sql))
    && sync.some((s) => /ALTER TABLE platform\.cross_region_entitlement SET SCHEMA sync/.test(s.sql)) && sync.some((s) => /ALTER TABLE platform\.wallet_authorisation SET SCHEMA sync/.test(s.sql))
    && syncKey('cross_region_entitlement_guest_link_id_fkey')?.guard.references === 'sync.guest_link'
    && syncKey('wallet_authorisation_wallet_hold_id_fkey')?.guard.references === 'wallet.fund_reservation'
    && /REFERENCES wallet\.fund_reservation\(id\)/.test(syncKey('wallet_authorisation_wallet_hold_id_fkey')?.sql),
  '**#28358 V1241__sync.sql: its two tables made under platform and moved, and its keys into sync.guest_link and wallet.fund_reservation by the names earlier tickets left them**',
  `${sync.length} statements: ${brief(sync).slice(0, 6).join(' | ')}`);
  const hold = ticketStatements(tenantFiles, { kind: 'tables', tables: ['catalogue.inventory_reservation'] });
  ok(hold.some((s) => /^CREATE TABLE IF NOT EXISTS catalogue\.inventory_hold\b/.test(s.sql)) && hold.some((s) => /ALTER TABLE catalogue\.inventory_hold RENAME TO inventory_reservation/.test(s.sql))
    && hold.some((s) => /ALTER POLICY %I ON catalogue\.inventory_reservation RENAME/.test(s.sql)),
  'the real package\'s renames go the same way: catalogue.inventory_reservation gets catalogue.inventory_hold\'s CREATE, the rename and its policy rename',
  brief(hold).slice(0, 4).join(' | '));
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
  // r8's package makes a role itself (V0105's platform.visible_parent_ids_setup). The one parser (tools.mjs) reads
  // it from the package's text; the script holds the server to exactly that, plus its bootstrap superuser.
  const allowed = tools.serverAllowances([{ name: 'V0105.sql', text: "CREATE FUNCTION f() RETURNS void LANGUAGE plpgsql AS $$ BEGIN\n"
    + "  CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;\n"
    + "  EXECUTE format('GRANT ticvai_parent_visible TO %I WITH INHERIT TRUE, SET TRUE', current_user);\n"
    + "  EXECUTE 'GRANT USAGE ON SCHEMA platform TO ticvai_parent_visible';\nEND $$;" }]);
  ok(JSON.stringify(allowed) === JSON.stringify({ 'server roles': ['ticvai_parent_visible'], 'server role memberships': ['current_user in ticvai_parent_visible'], 'server role settings': [] })
    && script.allowancesIn === undefined && script.rolesCreatedIn === undefined,
  'the server state the package makes is read from its text, by one parser: the role, and its membership for the user running the migration', JSON.stringify(allowed));
  // Review 7, m3: comments, strings and dollar-quoted values are not statements; EXECUTE's string and a function
  // body are; and every attribute that matters is read.
  const read = (text) => JSON.stringify(Object.values(tools.serverAllowances([{ text }])).flat());
  const parsed = {
    '/* CREATE ROLE evil SUPERUSER; */ SELECT 1': '[]',
    "COMMENT ON TABLE a.t IS 'CREATE ROLE evil3 SUPERUSER'": '[]',
    "CREATE FUNCTION f() RETURNS text LANGUAGE sql AS $$ SELECT 'GRANT pg_read_all_data TO app' $$": '[]',
    'SELECT $q$CREATE ROLE evil4$q$': '[]',
    [String.raw`SELECT E'it\'s CREATE ROLE evil5'`]: '[]',
    "DO $$ BEGIN EXECUTE format('CREATE ROLE %I LOGIN', 'probe_fmt'); END $$": '["probe_fmt (login)"]',
    "DO $$ BEGIN EXECUTE format('CREATE ROLE %I LOGIN', r); END $$": '[]',
    "DO $$ BEGIN EXECUTE format('GRANT t TO %I', r); EXECUTE 'GRANT USAGE ON SCHEMA platform, public TO t'; END $$": '[]',
    "CREATE ROLE t NOLOGIN NOINHERIT CONNECTION LIMIT 1 PASSWORD 'x' VALID UNTIL '2030-01-01'":
      '["t (noinherit) (connection limit 1) (valid until 2030-01-01 00:00:00) (password)"]',
    'CREATE ROLE r NOLOGIN IN ROLE pg_read_all_data ADMIN app': '["r","app in r (admin)","r in pg_read_all_data"]',
    'GRANT ticvai_parent_visible TO CURRENT_USER WITH ADMIN OPTION': '["current_user in ticvai_parent_visible (admin)"]',
    "ALTER ROLE r SET work_mem = '8MB'": '["r: work_mem=8MB"]',
  };
  const misread = Object.entries(parsed).filter(([text, want]) => read(text) !== want).map(([text, want]) => `${text} -> ${read(text)}, not ${want}`);
  ok(misread.length === 0, 'the parser reads code only (no comment, string or dollar-quoted value), EXECUTE\'s string and format(), and every attribute', misread.join(' | '));
  const exp = script.expectedServer(allowed, { me: 'postgres', bootstrap: 'postgres' });
  const boot = 'postgres (superuser) (createrole) (createdb) (replication) (bypassrls) (login)';
  const at = (roles, members = [], settings = []) => ({ 'server roles': roles, 'server role memberships': members, 'server role settings': settings });
  const same = script.serverDiffs(at([`${boot} (password)`, 'ticvai_parent_visible'], ['postgres in ticvai_parent_visible']), exp);
  const stray = script.serverDiffs(at([boot, 'probe (login)']), exp, at([boot, 'probe (login)']));
  const attr = script.serverDiffs(at([boot, 'ticvai_parent_visible (bypassrls)']), exp, at([boot, 'ticvai_parent_visible']));
  const admin = script.serverDiffs(at([boot], ['postgres in ticvai_parent_visible (admin)', 'app in ticvai_parent_visible']), exp, at([boot]));
  ok(same.length === 0
    && /roles are not what the package makes: probe \(login\) \(on the server before this file ran\), which the package does not make/.test(stray[0]) && /--clean, then this again/.test(stray[0])
    && /ticvai_parent_visible \(bypassrls\) \(this file changed it from ticvai_parent_visible\), where the package makes ticvai_parent_visible/.test(attr[0])
    && /postgres in ticvai_parent_visible \(admin\) \(made by this file\), where the package makes postgres in ticvai_parent_visible; app in ticvai_parent_visible \(made by this file\), which the package does not make/.test(admin[0]),
  'the server must be exactly what the package makes: a role from earlier, an attribute, an ADMIN option or another member is a difference, each named', [...stray, ...attr, ...admin].join(' | '));
  const r8 = script.splitSql ? tools.doInner("DO $$ BEGIN IF to_regclass('a.i') IS NOT NULL THEN DROP INDEX a.i; END IF; END $$") : [];
  ok(r8.length === 1 && /^DROP INDEX a\.i$/.test(r8[0]) && tools.statementTarget("DO $$ BEGIN IF true THEN ALTER TABLE a.t RENAME COLUMN x TO y; END IF; END $$") === 'a.t'
    && tools.statementTarget('DROP INDEX IF EXISTS a.i', new Map([['i', 'a.t']])) === 'a.t'
    && tools.statementTarget("SELECT platform.drop_rls_policies('a.t'::regclass)") === 'a.t'
    && tools.statementTarget("SELECT platform.ensure_month_partitions('a.t'::regclass, 3)") === null,
  'r8\'s guarded DO statements, index drops by name and drop_rls_policies are picked for their table', JSON.stringify(r8));
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
    // Review 8: a tenant ticket whose package statements make V0105's role, and a control ticket.
    9300: { workPackage: { key: '9300', subject: '[DB] Migration V0002__fnb_menu.sql: platform outlet and fnb menu (2 tables)', description: 'Tenant database. Tables: platform.outlet, fnb.menu.' },
      touches: [{ kind: 'table', id: 'platform.outlet' }, { kind: 'table', id: 'fnb.menu' }] },
    9400: { workPackage: { key: '9400', subject: '[DB] Migration V0002__api_client.sql: control api client (1 tables)', description: 'Control database. Tables: control.api_client.' },
      touches: [{ kind: 'table', id: 'control.api_client' }] },
    // r8 final re-walk: MIG-PLATFORM (#27665) owns two tables r8 moves from platform to sync.
    9017: { workPackage: { key: '9017', subject: '[DB] Migration V0017__platform.sql: platform (3 tables)', description: 'Tenant database.' },
      touches: ['platform.scope', 'sync.dsar_request', 'sync.guest_link'].map((id) => ({ kind: 'table', id })) },
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
  ok(JSON.stringify(c?.server) === JSON.stringify({ 'server roles': ['ticvai_parent_visible'], 'server role memberships': ['current_user in ticvai_parent_visible'], 'server role settings': [] }),
    'and the server state the package\'s text makes (r8: V0105\'s role, granted only to the user running the migration)', JSON.stringify(c?.server));
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

  // Review 8: roles are the server's, so every check, of either database, carries the one server-wide set.
  await pull.run(client, { key: '9300', dir });
  await pull.run(client, { key: '9400', dir });
  expectedOf[9300] = JSON.parse(read('9300', 'expected-schema.json') ?? 'null');
  expectedOf[9400] = JSON.parse(read('9400', 'expected-schema.json') ?? 'null');
  const servers = [...base.checks, ...expectedOf[9300].checks, ...expectedOf[9400].checks, ...sub.checks].map((x) => `${x.database} ${JSON.stringify(x.server)}`);
  ok(expectedOf[9400]?.checks?.[0]?.database === 'control' && new Set(servers.map((x) => x.replace(/^\w+ /, ''))).size === 1
    && servers.every((x) => x.endsWith(JSON.stringify(c?.server))) && expectedOf[9300].checks[0].statements.some((s) => /apply_parent(_split)?_across_rls/.test(s.sql)),
  '**every check carries the same server-wide set, control\'s too (the role a tenant file makes is the server\'s)**', servers.join(' | '));

  await pull.run(client, { key: '9017', dir });
  const moved17 = JSON.parse(read('9017', 'expected-schema.json') ?? 'null')?.checks?.[0];
  const madeAt = (rx) => moved17?.statements.findIndex((s) => rx.test(s.sql)) ?? -1;
  ok(moved17 && !moved17.notInPackageDdl && moved17.sources.includes('backend/tenant/V0105a__names_early_after_r1_20261020.sql')
    && moved17.sources.includes('backend/tenant/V0103a__names_early_after_r1_20261020.sql')
    && madeAt(/^CREATE TABLE IF NOT EXISTS platform\.dsar_request\b/) >= 0
    && madeAt(/^CREATE TABLE IF NOT EXISTS platform\.dsar_request\b/) < madeAt(/ALTER TABLE platform\.dsar_request SET SCHEMA sync/)
    && madeAt(/ALTER TABLE platform\.dsar_request SET SCHEMA sync/) < madeAt(/^ALTER TABLE sync\.dsar_request ADD COLUMN/)
    && moved17.tables['sync.dsar_request']?.foreignKeys.find((k) => k.name === 'dsar_request_guest_link_id_fkey')?.references === 'sync.guest_link',
  '**r8 re-walk, MIG-PLATFORM: expected-schema.json makes sync.dsar_request from its CREATE under platform and V0105a\'s move (V0105a in sources), and its key names sync.guest_link**',
  JSON.stringify({ sources: moved17?.sources, statements: moved17?.statements?.length, absent: moved17?.notInPackageDdl,
    keys: moved17?.tables?.['sync.dsar_request']?.foreignKeys?.map((k) => `${k.name}->${k.references}`) }));

  await pull.run(client, { key: '9034', dir });
  const fk = JSON.parse(read('9034', 'expected-schema.json') ?? 'null')?.checks?.[0];
  ok(fk?.kind === 'foreign-keys' && fk.statements.length === 2 && Object.keys(fk.tables).length === 0 && !fk.keysNotInPackageDdl,
    'the cross-schema keys ticket: its two keys, and no tables of its own', JSON.stringify(fk?.statements?.map((s) => s.guard?.constraint)));

  failRead = 'tenant/910-indexes.sql';
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
// Another name with ADAM_DB_TICKET_CHECK_CONTAINER, so a run never removes a container of that name someone keeps.
const CONTAINER = process.env.ADAM_DB_TICKET_CHECK_CONTAINER || 'adam-db-ticket-check';
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

  // Review 8, C1: a control ticket before and after a tenant ticket whose package statements make V0105's role
  // (the server's, once made), in one folder with real r8 tickets. Every one MATCHes, and --clean changes nothing.
  {
    const both = path.join(SCRATCH, 'both-databases');
    for (const db of ['tenant', 'control']) mkdirSync(path.join(both, 'db', db), { recursive: true });
    for (const k of [9001, 9300, 9400]) {
      mkdirSync(path.join(both, '.adam', 'work', String(k)), { recursive: true });
      writeFileSync(path.join(both, '.adam', 'work', String(k), 'expected-schema.json'), JSON.stringify(expectedOf[k], null, 2));
    }
    const fileFor = (db, tables) => `${ticketStatements(pkgFiles(db), { kind: 'tables', tables })
      .filter((s) => !(s.guard && !tables.includes(s.guard.references)))
      .map((s) => {
        const add = /^ALTER TABLE ([\w.]+) ADD CONSTRAINT (\w+)/i.exec(s.sql);
        return add ? `ALTER TABLE ${add[1]} DROP CONSTRAINT IF EXISTS ${add[2]};\n${s.sql};` : `${s.sql};`;
      }).join('\n')}\n`;
    writeFileSync(path.join(both, 'db', 'tenant', 'V0001__baseline.sql'), baseline('tenant'));
    writeFileSync(path.join(both, 'db', 'control', 'V0001__baseline.sql'), baseline('control'));
    writeFileSync(path.join(both, 'db', 'tenant', 'V0002__fnb_menu.sql'), fileFor('tenant', ['platform.outlet', 'fnb.menu']));
    writeFileSync(path.join(both, 'db', 'control', 'V0002__api_client.sql'), fileFor('control', ['control.api_client']));
    const hasRole = () => docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', "SELECT count(*) FROM pg_roles WHERE rolname = 'ticvai_parent_visible'"]).stdout.trim();
    const roleBefore = hasRole();
    const steps = [['control 9400, before any tenant run', runScript(both, '9400')], ['tenant 9300', runScript(both, '9300')]];
    const roleAfter = hasRole();
    steps.push(['control 9400, after it', runScript(both, '9400')], ['baseline 9001 (both databases)', runScript(both, '9001')],
      ['--clean', runScript(both, '--clean')], ['control 9400, after --clean', runScript(both, '9400')]);
    const bad = steps.filter(([what, r]) => r.code !== 0 || (what === '--clean' ? !/The server's roles were already exactly what the package makes/.test(r.out)
      : (r.out.match(/^MATCH: /gm) ?? []).length !== (/9001/.test(what) ? 2 : 1)));
    ok(roleBefore === '0' && roleAfter === '1' && bad.length === 0,
      '**review 8: a control ticket MATCHes before and after a tenant ticket that makes the package\'s role, and --clean leaves the server as it is**',
      `role ${roleBefore} -> ${roleAfter}\n${bad.map(([what, r]) => `${what}: ${r.out}`).join('\n---\n')}`);
    runScript(both, '--clean');
  }

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
      /the server's roles are not what the package makes: .*probe_back \(login\) \(made by this file\), which the package does not make/, /run node \.claude\/scripts\/db-ticket\.mjs --clean, then this again/],
    // What review 4 found: privileges the snapshot did not judge, refused by text; hidden, seen.
    ['role membership for another role', `${good}GRANT pg_write_all_data TO probe_owner;\n`, /changes role membership/, /DIFFERENT/],
    ['role membership for the migration role', `${good}GRANT pg_read_all_data TO CURRENT_USER;\n`, /changes role membership/, /DIFFERENT/],
    ['a privilege on a parameter', `${good}GRANT SET ON PARAMETER work_mem TO PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['a privilege on a tablespace', `${good}GRANT CREATE ON TABLESPACE pg_default TO PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['a privilege on a language', `${good}REVOKE USAGE ON LANGUAGE plpgsql FROM PUBLIC;\n`, /privileges on the database, the server or a language/, /DIFFERENT/],
    ['replica mode through set_config', `${good}SELECT set_config('session_replication_role', 'replica', true);\n`, /through set_config/, /DIFFERENT/],
    ['role membership hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'GRANT pg_read_all_data TO postgres'; END $$;\n`,
      /the server's role memberships are not what the package makes: postgres in pg_read_all_data \(made by this file\)/, /--clean, then this again/],
    ['a role attribute hidden in a DO block', `${good}DO $$ BEGIN EXECUTE 'ALTER ROLE probe_owner BYPASSRLS'; END $$;\n`,
      /the server's roles are not what the package makes: .*probe_owner \(bypassrls\) \(this file changed it from probe_owner\)/, /DIFFERENT/],
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
  // Review 7: what the cases left on the server (the check's own probe_owner with BYPASSRLS, probe_back, postgres in
  // pg_read_all_data) is not the package's, so a good file is DIFFERENT until --clean puts the server back.
  const psqlAt = (sql) => docker(['exec', CONTAINER, 'psql', '-U', 'postgres', '-Atc', sql]).stdout.trim();
  const blocked = check(good);
  ok(blocked.code === 1 && /probe_owner \(bypassrls\) \(on the server before this file ran\), which the package does not make/.test(blocked.out)
    && /probe_back \(login\) \(on the server before this file ran\)/.test(blocked.out) && /postgres in pg_read_all_data \(on the server before this file ran\)/.test(blocked.out),
  '**a good file on a server that earlier runs changed: DIFFERENT, naming each role and membership the package does not make**', blocked.out);
  const cleanedRoles = runScript(repo, '--clean');
  const rolesLeft = psqlAt("SELECT string_agg(rolname, ',' ORDER BY rolname) FROM pg_roles WHERE rolname !~ '^pg_'");
  const memberLeft = psqlAt("SELECT count(*) FROM pg_auth_members a JOIN pg_roles m ON m.oid = a.member JOIN pg_roles g ON g.oid = a.roleid WHERE m.rolname = 'postgres' AND g.rolname = 'pg_read_all_data'");
  ok(cleanedRoles.code === 0 && /Removed 2 roles the package does not make \((probe_back, probe_owner|probe_owner, probe_back)\)/.test(cleanedRoles.out)
    && /Revoked 1 role membership the package does not make \(postgres in pg_read_all_data\)/.test(cleanedRoles.out) && !/probe_/.test(rolesLeft) && memberLeft === '0',
  '--clean removes every role and role membership the package does not make, in the check\'s own container', `${cleanedRoles.out} [${rolesLeft}] [${memberLeft}]`);
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
  ok(cleaned.code === 0 && /Dropped this folder's \d+ databases \(adam_/.test(cleaned.out) && Number(left) > 0
    && /The server's roles were already exactly what the package makes/.test(cleaned.out),
  '--clean drops this folder\'s databases and not the other folder\'s', `${cleaned.out} ${left} left`);

  // Review 6: a file's server state is read inside its own transaction, under a lock every migration
  // transaction in the container takes. Review 7: and it is judged absolutely, against the package's text.
  const idOf = (dir) => createHash('sha256').update(realpathSync.native(dir).toLowerCase()).digest('hex').slice(0, 8);
  const forget = (dir) => {
    for (const n of readdirSync(tmpdir()).filter((x) => x.startsWith(`adam-db-ticket-${idOf(dir)}-`) && x.endsWith('.json'))) rmSync(path.join(tmpdir(), n), { force: true });
  };
  const marker = () => psqlAt("SELECT shobj_description((SELECT oid FROM pg_database WHERE datname = 'postgres'), 'pg_database')");
  // The other folder's file sleeps a second inside its transaction, so its runs overlap this folder's. The stray
  // role is the server's once made, so the other folder may see it too: then it is DIFFERENT, naming only that
  // role as already on the server before its file ran, never as its own.
  const twinFile = path.join(twin, 'db', 'tenant', 'V0005__subscription.sql');
  const twinText = readFileSync(twinFile, 'utf8');
  writeFileSync(twinFile, `${twinText}SELECT pg_sleep(1);\n`);
  const STRAY = `${good}DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'probe_stray') THEN CREATE ROLE probe_stray LOGIN; END IF; END $$;\n`;
  const twinFine = (o) => o.code === 0 || (o.code === 1 && /probe_stray \(login\) \(on the server before this file ran\), which the package does not make/.test(o.out)
    && !/made by this file|changed it from/.test(o.out) && /DIFFERENT: 1 difference/.test(o.out));
  const verdicts = [];
  for (let i = 0; i < 3; i++) {
    runScript(repo, '--clean');
    forget(repo);
    writeFileSync(ticketFile, STRAY);
    const [stray, other] = await Promise.all([runAsync(repo, '9005'), runAsync(twin, '9005')]);
    verdicts.push(`${stray.code}:${/probe_stray \(login\) \(made by this file\), which the package does not make/.test(stray.out)}:${twinFine(other)}${twinFine(other) ? '' : ` [twin: ${other.out.trim()}]`}`);
  }
  writeFileSync(twinFile, twinText);
  ok(verdicts.every((v) => v === '1:true:true') && !/probe_stray/.test(marker()),
    '**a role the package does not make, inside a DO block: DIFFERENT on every run, with another folder running at the same time; never kept by --clean**',
    `${verdicts.join(' | ')} ${marker()}`);
  // Review 7, C1 (b): the same file again, with nothing in between, is still DIFFERENT; so is an unchanged other
  // folder; --clean then a fixed file is MATCH.
  const strayAgain = runScript(repo, '9005');
  const twinAgain = runScript(twin, '9005');
  writeFileSync(ticketFile, good);
  const fixedBefore = runScript(repo, '9005');
  const strayClean = runScript(repo, '--clean');
  const fixed = runScript(repo, '9005');
  ok(strayAgain.code === 1 && /probe_stray \(login\) \(on the server before this file ran\)/.test(strayAgain.out) && twinAgain.code === 1 && fixedBefore.code === 1
    && /Removed 1 role the package does not make \(probe_stray\)/.test(strayClean.out) && fixed.code === 0 && /MATCH: 5 tables/.test(fixed.out),
  '**a stray role left by an earlier run: DIFFERENT again on the next run and in every folder (the fixed file too), until --clean; then MATCH**',
  `${strayAgain.out}\n${twinAgain.out}\n${fixedBefore.out}\n${strayClean.out}\n${fixed.out}`);

  // A folder of small files, as review 7's reproductions build them: the package's role made by an earlier file.
  const PKG_ROLE = "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ticvai_parent_visible') THEN CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE; END IF; END $$;\n";
  const PKG_SERVER = { 'server roles': ['ticvai_parent_visible'], 'server role memberships': ['current_user in ticvai_parent_visible'], 'server role settings': [] };
  const smallFolder = (name, { earlier = PKG_ROLE, tickets }) => {
    const dir = path.join(SCRATCH, name);
    mkdirSync(path.join(dir, 'db', 'tenant'), { recursive: true });
    writeFileSync(path.join(dir, 'db', 'tenant', 'V0001__base.sql'), 'CREATE SCHEMA IF NOT EXISTS platform;\n'
      + 'CREATE TABLE IF NOT EXISTS platform.schema_version (version text PRIMARY KEY, description text, checksum text, execution_ms int);\n'
      + "CREATE SCHEMA IF NOT EXISTS a;\nCREATE OR REPLACE FUNCTION platform.visible_ids() RETURNS int LANGUAGE sql AS 'SELECT 1';\n");
    writeFileSync(path.join(dir, 'db', 'tenant', 'V0002__fnb.sql'), earlier);
    for (const [key, { file, sql, table = 'a.t', server = PKG_SERVER, extra = [] }] of Object.entries(tickets)) {
      mkdirSync(path.join(dir, '.adam', 'work', key), { recursive: true });
      writeFileSync(path.join(dir, 'db', 'tenant', file), sql);
      writeFileSync(path.join(dir, '.adam', 'work', key, 'expected-schema.json'), JSON.stringify({ checks: [{ database: 'tenant', migration: file,
        tables: { [table]: {} }, ...(server ? { server } : {}),
        statements: [{ file: '010-a.sql', sql: `CREATE TABLE IF NOT EXISTS ${table} (id int)` }, ...extra.map((x) => ({ file: '010-a.sql', sql: x }))] }] }));
    }
    return dir;
  };
  const verdict = (r) => `${r.code} ${(r.out.match(/^(MATCH|DIFFERENT|FAILED|Cannot).*$/m)?.[0] ?? r.out.slice(-200)).slice(0, 60)}`;
  const T = 'CREATE TABLE IF NOT EXISTS a.t (id int);\n';

  // Review 7, C1 (a): BYPASSRLS on the package's role. --clean puts the role back to what the package makes, so the
  // same file is DIFFERENT again, and stays so; without the ALTER it is MATCH.
  const bypass = smallFolder('bypass', { tickets: { 66: { file: 'V0003__t.sql', sql: `${T}DO $$ BEGIN ALTER ROLE ticvai_parent_visible BYPASSRLS; END $$;\n` } } });
  const by1 = runScript(bypass, '66');
  const byClean = runScript(bypass, '--clean');
  const byAttr = psqlAt("SELECT rolbypassrls FROM pg_roles WHERE rolname = 'ticvai_parent_visible'");
  const by2 = runScript(bypass, '66');
  const by3 = runScript(twin, '9005');
  runScript(bypass, '--clean');
  writeFileSync(path.join(bypass, 'db', 'tenant', 'V0003__t.sql'), T);
  const by4 = runScript(bypass, '66');
  const BYPASS = /ticvai_parent_visible \(bypassrls\) \(this file changed it from ticvai_parent_visible\), where the package makes ticvai_parent_visible/;
  ok(by1.code === 1 && BYPASS.test(by1.out) && /Put 1 role back to what the package makes: ticvai_parent_visible \(was ticvai_parent_visible \(bypassrls\)\)/.test(byClean.out)
    && byAttr === 'f' && by2.code === 1 && BYPASS.test(by2.out)
    && by3.code === 1 && /ticvai_parent_visible \(bypassrls\) \(on the server before this file ran\)/.test(by3.out) && by4.code === 0 && /MATCH: 1 table/.test(by4.out),
  '**review 7 C1: BYPASSRLS on ticvai_parent_visible is DIFFERENT, --clean takes it off, the same file is DIFFERENT again (and so is every other folder until --clean); without it, MATCH**',
  [by1, byClean, by2, by3, by4].map(verdict).join(' | ') + `\n${byClean.out}\n${by2.out}`);

  // The package's own membership, but with ADMIN, or to another member; a role of the package's name made with
  // attributes the package does not give it; a setting on it.
  const variants = {
    admin: `${T}DO $$ BEGIN EXECUTE 'GRANT ticvai_parent_visible TO postgres WITH ADMIN OPTION'; END $$;\n`,
    other: `${T}DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'probe_app') THEN CREATE ROLE probe_app; END IF; EXECUTE 'GRANT ticvai_parent_visible TO probe_app'; END $$;\n`,
    setting: `${T}DO $$ BEGIN ALTER ROLE ticvai_parent_visible SET row_security = off; END $$;\n`,
  };
  const want = {
    admin: /postgres in ticvai_parent_visible \(admin\) \(made by this file\), where the package makes postgres in ticvai_parent_visible/,
    other: /probe_app in ticvai_parent_visible \(made by this file\), which the package does not make/,
    setting: /ticvai_parent_visible: row_security=off \(made by this file\), which the package does not make/,
  };
  const seen = [];
  for (const [name, sql] of Object.entries(variants)) {
    writeFileSync(path.join(bypass, 'db', 'tenant', 'V0003__t.sql'), sql);
    const r = runScript(bypass, '66');
    const c = runScript(bypass, '--clean');
    seen.push(`${name}: ${r.code === 1 && want[name].test(r.out) && c.code === 0 && /Revoked|Reset|Removed/.test(c.out) ? 'ok' : `${r.out}\n${c.out}`}`);
  }
  // The role must not be there yet, or the file's guarded CREATE ROLE does nothing.
  psqlAt('DROP ROLE IF EXISTS ticvai_parent_visible');
  const unseen = smallFolder('unseen', { earlier: 'SELECT 1;\n', tickets: { 67: { file: 'V0003__t.sql',
    sql: `${T}DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'ticvai_parent_visible') THEN CREATE ROLE ticvai_parent_visible NOLOGIN NOINHERIT CONNECTION LIMIT 1 PASSWORD 'x' VALID UNTIL '2030-01-01'; END IF; END $$;\n` } } });
  const un = runScript(unseen, '67');
  const unClean = runScript(unseen, '--clean');
  const unAfter = psqlAt("SELECT rolinherit || ' ' || rolconnlimit || ' ' || coalesce(rolvaliduntil::text, '-') || ' ' || (rolpassword IS NULL) FROM pg_authid WHERE rolname = 'ticvai_parent_visible'");
  seen.push(`unseen: ${un.code === 1 && /ticvai_parent_visible \(noinherit\) \(connection limit 1\) \(valid until 2030-01-01 00:00:00\) \(password\) \(made by this file\), where the package makes ticvai_parent_visible/.test(un.out)
    && unClean.code === 0 && unAfter === 'true -1 - true' ? 'ok' : `${un.out}\n${unClean.out}\n[${unAfter}]`}`);
  ok(seen.every((s) => /: ok$/.test(s)), 'review 7 m1/m2: the package\'s membership with ADMIN or to another member, a setting on its role, and its role with NOINHERIT, a connection limit, a password and VALID UNTIL are each DIFFERENT; --clean puts each back', seen.join('\n'));
  runScript(unseen, '--clean');

  // Review 7, I1: the file of another ticket in the same folder is not the package's. Its role is a difference in
  // every later ticket of the folder, and --clean never keeps it.
  const chain = smallFolder('chain', { earlier: 'SELECT 1;\n', tickets: {
    10: { file: 'V0003__x.sql', table: 'a.x', sql: "CREATE TABLE IF NOT EXISTS a.x (id int);\nDO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'probe_x') THEN CREATE ROLE probe_x LOGIN BYPASSRLS; END IF; END $$;\n" },
    11: { file: 'V0004__y.sql', table: 'a.y', sql: 'CREATE TABLE IF NOT EXISTS a.y (id int);\n' },
  } });
  const steps = [runScript(chain, '10'), runScript(chain, '--clean'), runScript(chain, '10'), runScript(chain, '11'), runScript(chain, '--clean'), runScript(chain, '10')];
  ok(steps[0].code === 1 && /probe_x \(bypassrls\) \(login\) \(made by this file\)/.test(steps[0].out) && /Removed 1 role the package does not make \(probe_x\)/.test(steps[1].out)
    && steps[2].code === 1 && steps[3].code === 1 && /probe_x \(bypassrls\) \(login\) \(on the server before this file ran\), which the package does not make/.test(steps[3].out)
    && /Removed 1 role the package does not make \(probe_x\)/.test(steps[4].out) && steps[5].code === 1 && !/probe_x/.test(marker()),
  '**review 7 I1: the role another ticket\'s earlier file makes is DIFFERENT in the next ticket too, and --clean never keeps it**', steps.map(verdict).join(' | '));
  runScript(chain, '--clean');

  // A role the package's text makes, made by an earlier file (as r8's apply_parent_across_rls does), is in two
  // folders' templates: --clean in one keeps it, so the other's unchanged ticket still matches. The same folder
  // without the package's `server` (a role no package text makes) is DIFFERENT (review 7: no earlier-file allowance).
  const OWNS = 'GRANT EXECUTE ON FUNCTION platform.visible_ids() TO ticvai_parent_visible;\nALTER FUNCTION platform.visible_ids() OWNER TO ticvai_parent_visible;\n';
  const cA = smallFolder('roles-a', { earlier: PKG_ROLE + OWNS, tickets: { 88: { file: 'V0003__t.sql', sql: T, server: { 'server roles': ['ticvai_parent_visible'] } } } });
  const cB = smallFolder('roles-b', { earlier: PKG_ROLE + OWNS, tickets: { 88: { file: 'V0003__t.sql', sql: T, server: { 'server roles': ['ticvai_parent_visible'] } } } });
  const b1 = runScript(cB, '88');
  const a1 = runScript(cA, '88');
  const aClean = runScript(cA, '--clean');
  const b2 = runScript(cB, '88');
  ok(b1.code === 0 && a1.code === 0 && aClean.code === 0 && !/ticvai_parent_visible/.test(aClean.out) && b2.code === 0 && /MATCH: 1 table/.test(b2.out),
    '**folder A --clean keeps the role the package makes, which folder B\'s template relies on: B\'s unchanged ticket still MATCH**', `${aClean.out}\n${b2.out}`);
  const cC = smallFolder('roles-c', { earlier: PKG_ROLE.replace(/ticvai_parent_visible/g, 'probe_team_role') + OWNS.replace(/ticvai_parent_visible/g, 'probe_team_role'),
    tickets: { 88: { file: 'V0003__t.sql', sql: T, server: { 'server roles': ['ticvai_parent_visible'] } } } });
  const c1 = runScript(cC, '88');
  ok(c1.code === 1 && /probe_team_role \(on the server before this file ran\), which the package does not make/.test(c1.out),
    '**a role an earlier file of the folder makes that the package does not: DIFFERENT**', c1.out);
  runScript(cC, '--clean');
  const bAfter = runScript(cB, '88');
  ok(bAfter.code === 0 && /template built/.test(bAfter.out),
    'after a --clean that changed the server\'s roles, another folder\'s template is built again, and its unchanged ticket MATCHes', bAfter.out);

  // Review 7, m4: a wait for the role lock is said, and it ends (ADAM_DB_CHECK_LOCK_WAIT shortens the minute here).
  const hold = (secs) => {
    const child = spawn('docker', ['exec', '-i', CONTAINER, 'psql', '-U', 'postgres', '-q', '-c',
      `BEGIN; LOCK TABLE pg_catalog.pg_authid IN SHARE ROW EXCLUSIVE MODE; SELECT pg_sleep(${secs}); COMMIT;`]);
    child.done = new Promise((r) => { child.on('close', r); });
    return child;
  };
  const waitRun = (secs) => new Promise((resolve) => {
    const child = spawn(process.execPath, [SCRIPT, '88'], { cwd: cB, env: { ...OWNED, ADAM_DB_CHECK_LOCK_WAIT: String(secs) } });
    let out = '';
    child.stdout.on('data', (d) => { out += d; });
    child.stderr.on('data', (d) => { out += d; });
    child.on('close', (code) => resolve({ code, out }));
  });
  let holder = hold(6);
  await new Promise((r) => { setTimeout(r, 1500); });
  const waitedOk = await waitRun(20);
  await holder.done;
  holder = hold(15);
  await new Promise((r) => { setTimeout(r, 1500); });
  const t0 = Date.now();
  const timedOut = await waitRun(3);
  const waitedS = (Date.now() - t0) / 1000;
  await holder.done;
  ok(waitedOk.code === 0 && /MATCH/.test(waitedOk.out) && /- waited for the server-wide role lock, held by process \d+ in database postgres/.test(waitedOk.out)
    && timedOut.code === 1 && /FAILED: .*waited 5 s for the server-wide role lock in this container, and it is still held by process \d+ in database postgres/.test(timedOut.out) && waitedS < 14,
  'a run that waits for the role lock says what holds it, and gives up after the wait with a message naming it', `${waitedOk.out}\n---\n${timedOut.out} (${waitedS.toFixed(1)} s)`);
  // Review 8, m1: the ticket's copy and the package's copy of one run take the same lock. A wait for the other copy
  // says so, and is not counted in the file's time.
  const ownWait = smallFolder('own-wait', { earlier: 'SELECT 1;\n', tickets: { 69: { file: 'V0003__t.sql', sql: `${T}SELECT pg_sleep(4);\n`, extra: ['SELECT pg_sleep(4)'] } } });
  const ow = runScript(ownWait, '69');
  const owSecs = Number(/- first run: \d+ statements? applied in ([\d.]+) s/.exec(ow.out)?.[1] ?? 99);
  ok(ow.code === 0 && /- waited for the server-wide role lock, held by process \d+ in database adam_\w+_(expect|ticket), .*\(this run's own copy of the (package's statements|ticket's file)\)/.test(ow.out)
    && !/another folder/.test(ow.out) && owSecs < 6,
  'review 8 m1: a wait for the run\'s own other copy names it as such, and the first run\'s time leaves the wait out', ow.out);
  runScript(ownWait, '--clean');
  for (const d of [cA, cB, bypass]) runScript(d, '--clean');

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
    if (database === 'tenant') {
      // The server's roles once the package has run (as the bootstrap superuser, so V0105 makes its role and grants
      // it to no one) are exactly what the one parser reads from the package's text (both databases share them).
      const cluster = JSON.parse(psql('pkg_tenant', `SELECT ${script.CLUSTER_SQL};`).stdout.trim() || 'null');
      const both = tools.serverAllowances([...pkgFiles('tenant'), ...pkgFiles('control')]);
      const serverDiff = cluster ? script.serverDiffs(cluster, script.expectedServer(both, cluster)) : ['no answer'];
      ok(serverDiff.length === 0 && cluster['server roles'].includes('ticvai_parent_visible'),
        'the roles the package makes on the server are exactly what tools.mjs reads from its text', serverDiff.join(' | ') || JSON.stringify(cluster));
    }
    const model = schemaModel(files);
    const tables = [...model.tables.keys()];
    // What every ticket would be given, put together: the baseline, then each table's statements.
    // Put together in the package's own order: r8's helpers grant on the functions that exist when
    // they run, so the order is part of the result.
    const picked = new Map();
    for (const s of [...ticketStatements(files, { kind: 'baseline', tables: [] }), ...ticketStatements(files, { kind: 'tables', tables })]) {
      picked.set(`${s.file}\u0000${s.sql}`, true);
    }
    const ordered = [];
    for (const f of [...files].sort((a, b) => (a.name < b.name ? -1 : 1))) {
      for (const sql of sqlStatements(f.text)) {
        if (picked.delete(`${f.name}\u0000${sql}`)) ordered.push({ file: f.name, sql });
      }
    }
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
