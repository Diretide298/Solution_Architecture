// ADAM's table record (adam_table) says what the package SQL says: TICVAI ADAM CR-436, decided by Chinmay on 1 November
// 2026 ("The seven table records follow the package SQL, not the other way round").
//
//   node checks/table-record-check.mjs [path/to/ticvai]      (default ../ticvai; needs no viewer)
//
// Two ways the record and the SQL parted, each held here for the tables CR-436 names and for every table like them:
//   1. A table renamed after r1 and created under its name now (control.plan in control/V0108) took the DDL of its old
//      name (subscription.plan in the frozen tenant/010-subscription.sql, read later in file order), with the old
//      key and the tenant_isolation policy the control database does not have.
//   2. A primary key a later migration replaces (platform.configuration_profile, rekeyed (id, version) by tenant/V0115
//      under CR-228) kept the CREATE's key.
// A column's Required is the workbook's (build-schema-workbook.py, from the DDL records derive-ddl writes); the two
// columns CR-436 names are held to nullable there.
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildBackend } from '../lib/backend.mjs';
import { buildMigrations } from '../lib/migrations.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(process.argv[2] ?? path.join(here, '..', '..', 'ticvai'));
let ok = 0, bad = 0;
const check = (n, c, d = '') => { console.log(`${c ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); c ? ok++ : bad++; };

const backend = await buildBackend(root);
const migrations = await buildMigrations(root);
const byName = new Map((backend.tables ?? []).map((t) => [t.name, t]));
const same = (a, b) => JSON.stringify([...(a ?? [])].sort()) === JSON.stringify([...(b ?? [])].sort());

// CR-436's seven, as the SQL has them
const want = {
  'control.contract': { pk: ['id'], rls: false },
  'control.module_listing': { pk: ['id'], rls: false },
  'control.plan': { pk: ['id', 'version'], rls: false },
  'control.plan_limit': { pk: ['id'], rls: false },
  'control.plan_module': { pk: ['id'], rls: false },
  'platform.configuration_profile': { pk: ['id', 'version'], rls: true },
  'platform.audit_read': { pk: ['id'], rls: true, nullable: ['read_at', 'target'] },
};
for (const [name, w] of Object.entries(want)) {
  const t = byName.get(name);
  if (!t?.ddl) { check(`${name} has a record with its DDL`, false); continue; }
  check(`${name} keyed (${w.pk.join(', ')})`, same(t.ddl.primaryKey, w.pk), `record says (${(t.ddl.primaryKey ?? []).join(', ')}) from ${t.ddl.file}`);
  check(`${name} ${w.rls ? 'has' : 'has no'} row security`, Boolean(t.ddl.rls?.enabled) === w.rls,
    `record says ${t.ddl.rls?.policy ?? 'none'} from ${t.ddl.file}`);
  for (const c of w.nullable ?? []) {
    const col = (backend.columns?.[name] ?? []).find((x) => x.name === c);
    check(`${name}.${c} is nullable`, col && !col.required, col ? `record says required` : 'no such column');
  }
}

// 1, for every table: a table the SQL creates under its name now is recorded from that CREATE
const moved = (backend.tables ?? []).filter((t) => t.was && t.ddl && migrations.tables[t.name]);
const stale = moved.filter((t) => t.ddl.createdAs);
check(`${moved.length} renamed tables created under their name now are recorded from that CREATE`, !stale.length,
  stale.map((t) => `${t.name} from ${t.ddl.file}`).join('; '));

console.log(`\n${ok} passed, ${bad} failed`);
process.exit(bad ? 1 : 0);
