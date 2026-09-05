#!/usr/bin/env python3
"""Generate Postgres DDL from `handoff/schema-reference.json`.

**This file used to say CF-161 could not change the DDL, and that was wrong.** It read: *"That
blocks the deployment topology and not the tables. The `CREATE TABLE` statements are identical
either way."* It was true when written and CF-161's answer contradicts it — ADR-0038 drops a
column, adds three tables and takes `control` out of the tenant template, so the DDL was blocked
on CF-161 after all, in the one way this docstring ruled out. **A claim that a question cannot
reach your artefact is the claim most likely to be left standing after it does.**

ADR-0038 and ADR-0039 make the output two artefacts rather than one:

    backend/control/000-schemas.sql       the control schema
    backend/control/010-control.sql       46 tables — the cell registry, tenants, billing, rollouts
    backend/control/900-foreign-keys.sql  references inside the control database
    backend/control/910-indexes.sql

    backend/tenant/000-schemas.sql        the 25-schema tenant template
    backend/tenant/010-<schema>.sql       one file per schema, 331 tables
    backend/tenant/900-foreign-keys.sql   references inside a tenant database
    backend/tenant/910-indexes.sql

    backend/990-cross-database-references.sql  the 21 that no longer fit in either
    backend/provision-tenant.sh                CREATE DATABASE, apply the template, register the row

**The 21 are the price of the split and they are stated rather than dropped.** Postgres has no
cross-database foreign key, so `control.subscription.tenant_id -> platform.tenant(id)` and twenty
others stop being constraints the moment `control` becomes a database of its own. They are emitted
as commented-out `ALTER TABLE` lines with an index each, because an integrity rule that moved into
application code is a rule somebody has to be told about — silently not emitting them would leave
the DDL looking complete.

**Foreign keys go in a separate file on purpose.** 932 relationships across 26 schemas cannot be
ordered so that every reference is already created — `orders` reaches `catalogue` and `catalogue`
reaches `platform` and something reaches back. **Creating tables first and constraining afterwards
is the only ordering that terminates.**

**`enforced: no` references become an index and a comment, not a constraint.** 486 of the 932 are
conventions rather than declared references (ADR-0011), and enforcing a convention the contracts
never asserted would fail on the first row of real data.

Run: `python3 tools/derive-ddl.py [--apply]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "backend"

# **The one schema that is a database.** ADR-0039 took `control` out of the tenant template,
# so the split is a fact this file has to hold rather than a string repeated in six branches.
CONTROL = "control"

# **Where a file lands.** A control table and a tenant table are no longer in the same
# database, and the directory is what says so — the deploy configs mount one of these as
# initdb and hand the other to the provisioning script.
def area(schema: str) -> str:
    return CONTROL if schema == CONTROL else "tenant"

INITDB_PROVISION = r"""#!/usr/bin/env bash
# Provision this cell's tenant databases, from inside the postgres container's initdb pass.
# **Derived by tools/derive-ddl.py. Do not hand-edit.**
#
# **The instance is the cell and the database is the tenant** (ADR-0038). initdb has just applied
# the control database; this creates the tenant databases the scenario says are in this region.
#
# TICVAI_TENANTS is a comma-separated list of tenant slugs. A slug may carry its uuid after a
# colon — `acme:3f2a...` — so the row in control.cell_tenant can be written at the same time.
# Without the uuid the database is still created and the row is not, and the script says so:
# **a database nothing knows about is worse than a database that is missing.**
set -euo pipefail

: "${TICVAI_TENANTS:=}"
if [ -z "$TICVAI_TENANTS" ]; then
  echo "no TICVAI_TENANTS set - control database only, no tenants in this cell" >&2
  exit 0
fi

export CONTROL_DB="${POSTGRES_DB:-control}"
export PGUSER="${POSTGRES_USER:-ticvai}"

IFS=',' read -ra ENTRIES <<< "$TICVAI_TENANTS"
for entry in "${ENTRIES[@]}"; do
  entry="$(echo "$entry" | tr -d '[:space:]')"
  [ -z "$entry" ] && continue
  slug="${entry%%:*}"
  uuid=""
  case "$entry" in *:*) uuid="${entry#*:}";; esac
  /opt/ticvai/provision-tenant.sh "$slug" "$uuid"
done

echo "provisioned ${#ENTRIES[@]} tenant database(s) in this cell"
"""

PROVISION = r"""#!/usr/bin/env bash
# Provision one tenant database in this region's instance.
# **Derived by tools/derive-ddl.py. Do not hand-edit.**
#
# ADR-0038: one Postgres instance per region, and the instance is the cell.
# ADR-0039: one database per tenant, and the database is the unit of provisioning, migration,
#           backup and destruction.
#
# **The database name does not encode the region.** The instance already is the region, and a
# name that repeats it is a name that can contradict it.
#
# **Provisioning is triggered by verification, not by application.**
# control.onboarding_application says it: nothing is provisioned until verification passes,
# because an unverified application that provisions a cell is a cell somebody has to clean up.
# This script is the step after that check, not instead of it.
#
# Usage: provision-tenant.sh <tenant-slug> [tenant-uuid]
set -euo pipefail

SLUG="${1:?tenant slug required}"
TENANT_ID="${2:-}"
: "${PGHOST:=postgres}"
: "${PGUSER:=ticvai}"
: "${CONTROL_DB:=control}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. The database. **Refused rather than reused** - provisioning over a live tenant is the one
#    mistake in this script that cannot be undone.
if psql -tAc "SELECT 1 FROM pg_database WHERE datname = '$SLUG'" -d "$CONTROL_DB" | grep -q 1
then
  echo "refused: database $SLUG already exists" >&2
  exit 1
fi
createdb "$SLUG"

# 2. The template, in the order the files are numbered: schemas, tables, constraints, indexes.
#    Every tenant database gets the same set, which is what makes two hundred migrations one job
#    rather than two hundred schemas.
for f in "$HERE"/tenant/*.sql; do
  psql -v ON_ERROR_STOP=1 -d "$SLUG" -f "$f" >/dev/null
done

# 3. The row. **A database with no row in control.cell_tenant is a database nothing knows
#    about** - it will not be migrated, backed up or billed, and it will be found by somebody
#    reading pg_database rather than by the control plane.
if [ -n "$TENANT_ID" ]; then
  psql -v ON_ERROR_STOP=1 -d "$CONTROL_DB" <<SQL >/dev/null
    INSERT INTO control.cell_tenant (id, cell_id, tenant_id, database_name, status,
                                     provisioned_at)
    SELECT gen_random_uuid(), c.id, '$TENANT_ID', '$SLUG', 'live', now()
      FROM control.cell c
     WHERE c.status = 'active'
     LIMIT 1;
SQL
else
  echo "warning: no tenant uuid given - $SLUG is not registered in control.cell_tenant" >&2
fi

echo "provisioned $SLUG"
"""


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# The contract vocabulary is already Postgres. **Only two need translating**, and both are cases
# where the deriver wrote a shape rather than a type.
TYPE_MAP = {
    "text[]": "text[]",
    "float[]": "double precision[]",
    "numeric": "numeric(18,4)",
}

RESERVED = {"table", "order", "user", "group", "check", "default", "references", "primary",
            "column", "constraint", "index", "unique", "all", "any", "case", "end", "from",
            "to", "grant", "limit", "offset", "return", "session", "authorization"}


def q(name: str) -> str:
    """Quote an identifier only where Postgres needs it.

    **`fnb.table` and `orders.order` are real tables** and both are reserved words. Quoting
    everything makes the DDL unreadable; quoting nothing makes it unparseable.
    """
    return f'"{name}"' if name.lower() in RESERVED else name


def pg_type(t: str | None) -> str:
    if not t:
        return "text"
    return TYPE_MAP.get(t, t)



def key_of(table: str, cols: dict) -> str | None:
    """The column a foreign key should point at.

    **Twelve tables have no `id`.** `games.card` is keyed by `card_code`, `platform.guest_link` by
    `guest_link_id`, `fnb.recipe` by the menu item it belongs to. **Emitting `REFERENCES t(id)`
    against those is a constraint that cannot be created**, and it would have failed on the first
    `psql -f` rather than here.

    Order matters: an explicit `id`, then `<table>_id`, then a single-column table's only column —
    a child keyed solely by its parent is legitimate and common here.
    """
    names = [c["column"] for c in cols.get(table, [])]
    if not names:
        return None
    if "id" in names:
        return "id"
    stem = table.split(".", 1)[1]
    for cand in (f"{stem}_id", f"{stem.rstrip('s')}_id", f"{stem}_code"):
        if cand in names:
            return cand
    if len(names) == 1:
        return names[0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    S = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    cols = S["cols"]
    storage = S.get("storage") or {}
    real = {t for t in cols if "." in t and ":" not in t}

    by_schema: dict[str, list] = defaultdict(list)
    for t in sorted(real):
        by_schema[t.split(".")[0]].append(t)

    files: dict[str, str] = {}

    # 1. schemas — **two artefacts, because a cell is a region and a database is a tenant.**
    # ADR-0038 put a database around each tenant and ADR-0039 gave `control` one of its own, so
    # `CREATE SCHEMA control` and the tenant template stopped being the same file. The 26th schema
    # is not a schema in the template at all.
    tenant_schemas = sorted(s for s in by_schema if s != CONTROL)
    n_tenant_tables = sum(len(by_schema[s]) for s in tenant_schemas)

    files[f"{CONTROL}/000-schemas.sql"] = "\n".join([
        "-- TICVAI — the control database.",
        "-- **Derived by tools/derive-ddl.py. Do not hand-edit.**",
        "--",
        "-- **One schema, and a database of its own** (ADR-0039). Every table here is *about*",
        "-- tenants rather than *inside* one: the cell registry, placement, licences, subscriptions,",
        "-- releases, rollouts, migration runs, onboarding, and the tenant registry itself.",
        "--",
        "-- A cell registry that exists two hundred times is two hundred registries that can",
        "-- disagree, and the first thing that disagrees is which of them is authoritative.",
        "--",
        f"-- {len(by_schema.get(CONTROL) or [])} tables. Applied once per region, to the instance.",
        "",
        f"CREATE SCHEMA IF NOT EXISTS {q(CONTROL)};",
    ]) + "\n"

    files["tenant/000-schemas.sql"] = "\n".join([
        "-- TICVAI — the tenant template.",
        "-- **Derived by tools/derive-ddl.py. Do not hand-edit.**",
        "--",
        f"-- {len(tenant_schemas)} schemas. The boundary is the service boundary (ADR-0028): no",
        "-- service spans a schema it does not own, and no schema is written by two services.",
        "-- **ADR-0038 left that decomposition untouched** — what changed is that this set now",
        "-- exists once per tenant rather than once for everybody.",
        "--",
        f"-- {n_tenant_tables} tables. Applied to every tenant database by provision-tenant.sh.",
        "--",
        "-- **`control` is not here.** It left the template in ADR-0039 and the count went 26 to 25.",
        "",
    ] + [f"CREATE SCHEMA IF NOT EXISTS {q(s)};" for s in tenant_schemas]) + "\n"

    # 2. tables, one file per schema
    # **Routed, not collected.** A reference whose two ends are now in different databases
    # cannot be a constraint, and a file that emits it anyway does not apply. Each line is kept
    # with the schema it came from so the assembly below can put it where it can actually run.
    fk_lines: list[tuple[str, str]] = []
    idx_lines: list[tuple[str, str]] = []
    xdb_lines: list[str] = []
    n_tables = n_cols = n_fk = n_idx = n_xdb = 0
    unkeyed: list = []

    for schema in sorted(by_schema):
        out = [
            f"-- {schema} — {len(by_schema[schema])} tables",
            "-- **Derived. Do not hand-edit.**",
            "",
        ]
        for t in by_schema[schema]:
            short = t.split(".", 1)[1]
            note = str(storage.get(t) or "").split(". **Hangs off**")[0].strip()
            note = re.sub(r"\*\*|`", "", note)[:400]
            if note:
                for line in re.findall(r".{1,96}(?:\s|$)", note):
                    if line.strip():
                        out.append(f"-- {line.strip()}")
            out.append(f"CREATE TABLE IF NOT EXISTS {q(schema)}.{q(short)} (")

            body = []
            names = [c["column"] for c in cols[t]]
            # **The key is whatever `key_of` says it is, not whatever is called `id`.** Until
            # 3 September this line read `if col == "id"`, so 84 tables reached Postgres with no
            # key — `games.card` is keyed by `card_code` and `platform.guest_link` by
            # `guest_link_id`, and both were emitted keyless while `key_of` sat in this same file
            # already returning the right answer for foreign keys.
            #
            # **A table with no key is not a table Postgres will let anything reference**, which is
            # how four constraints came to point at a column that is not unique.
            tkey = key_of(t, cols)
            for c in cols[t]:
                col = c["column"]
                typ = pg_type(c.get("type"))
                nn = " NOT NULL" if c.get("required") == "yes" else ""
                pk = " PRIMARY KEY" if col == tkey else ""
                body.append(f"    {q(col):<34}{typ}{pk}{nn}")
                n_cols += 1

                ref = c.get("references")
                if ref and ref in real:
                    tgt_s, tgt_t = ref.split(".", 1)
                    tgt_key = key_of(ref, cols)
                    if c.get("enforced") == "yes" and tgt_key:
                        stmt = (f"ALTER TABLE {q(schema)}.{q(short)} ADD CONSTRAINT "
                                f"fk_{short}_{col} FOREIGN KEY ({q(col)}) "
                                f"REFERENCES {q(tgt_s)}.{q(tgt_t)}({q(tgt_key)});")
                        if area(schema) != area(tgt_s):
                            # **Postgres has no cross-database foreign key.** The split ADR-0039
                            # makes turns 21 declared references into application-level rules, and
                            # they are written out rather than dropped: an integrity rule that
                            # moved into code is a rule somebody has to be told about.
                            xdb_lines.append(
                                f"-- {t}.{col} -> {ref}\n"
                                f"-- {area(schema)} database -> {area(tgt_s)} database. "
                                f"Enforced by the caller, not by Postgres.\n"
                                f"-- {stmt}")
                            # **The index still belongs in the database the column is in.** It is
                            # the only thing Postgres can still offer for a rule it can no longer
                            # enforce, and the join it serves did not stop happening.
                            idx_lines.append((schema,
                                f"-- crosses the database boundary: {t}.{col} -> {ref}\n"
                                f"CREATE INDEX IF NOT EXISTS ix_{short}_{col} "
                                f"ON {q(schema)}.{q(short)} ({q(col)});"))
                            n_idx += 1
                            n_xdb += 1
                        else:
                            fk_lines.append((schema, stmt))
                            n_fk += 1
                    elif c.get("enforced") == "yes":
                        # **A declared reference to a table with no addressable key.** Reported
                        # rather than emitted — a constraint that cannot be created fails the whole
                        # file, and silently downgrading it to an index hides a real modelling gap.
                        unkeyed.append(f"{t}.{col} -> {ref}")
                        idx_lines.append((schema,
                            f"-- declared but {ref} has no addressable key: {t}.{col}\n"
                            f"CREATE INDEX IF NOT EXISTS ix_{short}_{col} "
                            f"ON {q(schema)}.{q(short)} ({q(col)});"))
                        n_idx += 1
                    else:
                        # **A convention is indexed, not constrained.** 486 of 932 references are
                        # naming habits the contracts never asserted (ADR-0011) — enforcing one
                        # fails on the first row that legitimately points nowhere.
                        idx_lines.append((schema,
                            f"-- convention, not declared: {t}.{col} -> {ref}\n"
                            f"CREATE INDEX IF NOT EXISTS ix_{short}_{col} "
                            f"ON {q(schema)}.{q(short)} ({q(col)});"))
                        n_idx += 1

            # **Every table carries `scope_path` if it has one** — that is the partition key
            # (ADR-0005), and an ltree index on it is what makes a scope walk cheap.
            if "scope_path" in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS ix_{short}_scope "
                    f"ON {q(schema)}.{q(short)} ({q('scope_path')} text_pattern_ops);"))
                n_idx += 1

            out.append(",\n".join(body))
            out.append(");")
            out.append("")
            n_tables += 1
        files[f"{area(schema)}/010-{schema}.sql"] = "\n".join(out) + "\n"

    for db in (CONTROL, "tenant"):
        mine = sorted(line for s, line in fk_lines if area(s) == db)
        files[f"{db}/900-foreign-keys.sql"] = "\n".join([
            f"-- Declared references inside the {db} database, applied after every table exists.",
            "-- **Separate file because the schemas cannot be ordered so every reference precedes",
            "-- its use** — orders reaches catalogue, catalogue reaches platform, and something",
            "-- reaches back. Tables first, constraints last, is the only ordering that terminates.",
            "--",
            f"-- {len(mine)} of {len(fk_lines) + n_xdb} declared references. The ones that reach the",
            "-- other database are in ../990-cross-database-references.sql and are not constraints",
            "-- any more.",
            "",
        ] + mine) + "\n"

        idx = sorted({line for s, line in idx_lines if area(s) == db})
        files[f"{db}/910-indexes.sql"] = "\n".join([
            f"-- Conventions and scope paths in the {db} database.",
            "-- **A convention is indexed and not constrained** (ADR-0011): most references are",
            "-- naming habits the contracts never asserted, and enforcing one fails on the first",
            "-- row that legitimately points nowhere.",
            "",
        ] + idx) + "\n"

    # **The 21 that no longer fit in either database.** Emitted rather than dropped: silently not
    # writing them would leave the DDL looking complete, and the rule would be gone with nobody
    # told. This file is not applied — the indexes are, by the area files above.
    files["990-cross-database-references.sql"] = "\n".join([
        "-- References that cross the control/tenant database boundary.",
        "-- **Derived by tools/derive-ddl.py. Do not hand-edit.**",
        "--",
        f"-- {n_xdb} declared references stopped being constraints when ADR-0039 made `control` a",
        "-- database of its own. **Postgres has no cross-database foreign key**, so each one is now",
        "-- a rule the caller has to keep, and the index below is all the database can offer.",
        "--",
        "-- **This is the price of the split and it is stated rather than absorbed.** A reference",
        "-- that quietly stops being enforced is a reference that will be violated by the first",
        "-- code path nobody reviewed.",
        "--",
        "-- The ALTER TABLE lines are commented out on purpose: they are what the constraint would",
        "-- have been, kept so the rule is still readable at the place it used to be enforced.",
        "--",
        "-- **This file is applied to neither database.** The index for each column is in its own",
        "-- database's 910-indexes.sql \u2014 the join did not stop happening just because Postgres",
        "-- stopped checking it.",
        "",
    ] + sorted(xdb_lines)) + "\n"

    # **The provisioning script ADR-0039 assumes and nothing emitted.** A tenant database is the
    # unit of provisioning, migration, backup and destruction — which needs one artefact that
    # creates it, applies the template and registers the row. Without it, "apply the template" is
    # a sentence in an ADR rather than a thing that runs.
    # **The provisioning script ADR-0039 assumes and nothing emitted.** A tenant database is
    # the unit of provisioning, migration, backup and destruction, which needs one artefact
    # that creates it, applies the template and registers the row. Without it, “apply the
    # template” is a sentence in an ADR rather than a thing that runs.
    files["provision-tenant.sh"] = PROVISION

    # **The compose entry point.** provision-tenant.sh takes one tenant; a cell has several, and
    # the initdb pass is where a container gets them. Kept separate so the per-tenant script stays
    # usable by hand and by the control plane.
    files["initdb-provision.sh"] = INITDB_PROVISION

    if a.apply:
        # **The flat layout is removed, not left beside the new one.** The deploy configs mount
        # `backend/<area>` into initdb, and a stale `backend/010-orders.sql` sitting next to
        # `backend/tenant/010-orders.sql` is two answers to what a tenant database contains —
        # which is the failure this package has already had once, in the mirrors.
        OUT.mkdir(exist_ok=True)
        for stale in sorted(OUT.glob("0*.sql")) + sorted(OUT.glob("9*.sql")):
            if stale.name not in files:
                stale.unlink()
        for name, text in files.items():
            dest = OUT / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
            if dest.suffix == ".sh":
                dest.chmod(0o755)

    print(f"  {n_tables} tables · {n_cols} columns · {n_fk} foreign keys · {n_idx} indexes")
    print(f"  {len(by_schema.get(CONTROL) or [])} control tables · "
          f"{n_tenant_tables} tenant tables in {len(tenant_schemas)} schemas")
    if n_xdb:
        print(f"  {n_xdb} reference(s) cross the control/tenant boundary and are no longer "
              "constraints")
    if unkeyed:
        print(f"  {len(unkeyed)} declared reference(s) point at a table with no addressable key:")
        for u in unkeyed[:8]:
            print(f"     {u}")
    print(f"  {len(files)} files" + ("" if a.apply else " — nothing written, pass --apply"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
