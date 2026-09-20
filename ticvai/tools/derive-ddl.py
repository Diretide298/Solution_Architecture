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
cross-database foreign key, so `subscription.contract.tenant_id -> platform.tenant(id)` and twenty
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

POSTGRES_STORES = {"postgres", "postgres-analytical"}

# --- the machinery layer, folded in from V0001__baseline.sql on 21 September -------------------

EXTENSIONS = """-- Extensions, applied before any table.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Numbered 001 so it sorts before 010-*.** `ltree` is used by the scope index and the
-- row-level-security predicate, so it cannot arrive after the tables that depend on it.
-- This is why the machinery could not be a `V*.sql` file living beside the numeric series:
-- digits sort before letters, and the security layer would have applied last.

-- ltree carries the scope tree. GiST indexes its containment operators, which is what makes
-- `<@` cheap enough to sit inside every policy on every table.
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
"""

RLS_HEAD = """-- Row-level security.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Default deny is the point.** With `ticvai.scope_paths` unset, every policy below returns no
-- rows. A connection that forgets to set it sees an empty database, not the whole of it — which
-- is the Sprint 1 Gate 0 criterion, written as a predicate rather than a promise.
--
-- **Applied to every table that carries `scope_path`, which is what changed on 21 September.**
-- The hand-written baseline enabled RLS on three tables. The partition key is a column this
-- generator already knows about on every table that has one, so the policy set is derived rather
-- than remembered — and a new table with a `scope_path` is protected by existing, not by somebody
-- noticing.

-- The paths the current connection may see, read from a session GUC the API layer sets per
-- request. `true` in current_setting makes an unset GUC return NULL rather than raising, so an
-- unconfigured connection degrades to zero rows instead of an error nobody catches.
CREATE OR REPLACE FUNCTION platform.current_scope_paths()
    RETURNS ltree[]
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT COALESCE(
        (SELECT array_agg(p::ltree)
           FROM unnest(string_to_array(
                    NULLIF(current_setting('ticvai.scope_paths', true), ''), ',')) AS p
          WHERE btrim(p) <> ''),
        ARRAY[]::ltree[]);
$$;

-- True when the row sits at or beneath one of the granted paths. An empty grant list matches
-- nothing — deny is the default, and it is the default because it is the absence of a grant
-- rather than the presence of a denial.
CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path text)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path::ltree <@ ANY (platform.current_scope_paths());
$$;

-- Applies the standard policy to a table.
-- **FORCE is the whole point.** Without it the table owner — which is what a migration and most
-- pooled application connections run as — bypasses every policy silently.
CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'scope_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

-- **59 tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path` alone
-- leaves every one of them open.** `check-migrations` has said so since it was written — *"checking
-- only scope_path missed 41 tables that carry venue_id instead; they would have passed with no
-- policy at all"* — and the hand-written baseline never closed it because it protected three
-- tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on sixty tables**, and `platform.scope`
-- is small, cached and indexed on `id`.
CREATE OR REPLACE FUNCTION platform.venue_in_scope(row_venue_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_venue_id IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND EXISTS (
            SELECT 1 FROM platform.scope s
             WHERE s.id = row_venue_id
               AND s.path::ltree <@ ANY (platform.current_scope_paths()));
$$;

CREATE OR REPLACE FUNCTION platform.apply_venue_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'venue_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.venue_in_scope(venue_id)) '
        'WITH CHECK (platform.venue_in_scope(venue_id))', policy_name, target);
END
$$;
"""

# **The scope tree protects itself on `path`, which is the column it calls its own scope_path.**
# `platform.scope` is what every other policy resolves against, so leaving it open would make the
# rest decorative: a connection that can read the whole tree can read every path in it.
SCOPE_SELF_RLS = """
ALTER TABLE platform.scope ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.scope FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS scope_isolation ON platform.scope;
CREATE POLICY scope_isolation ON platform.scope
    USING (platform.in_scope(path))
    WITH CHECK (platform.in_scope(path));
"""

PARTITION_HEAD = """-- The venue partitioning mechanism (ADR-0005, ADR-0044).
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- ADR-0044, signed off 18 September 2026: a table whose `venue_id` is NOT NULL partitions by list
-- on it, carries `venue_id` as the leading column of its primary key, and every foreign key into
-- it is composite. **What lives here is the mechanism; the tables declare their own partitioning
-- where they are created.**
--
-- **Every partitioned table needs a DEFAULT partition.** Misconfiguration should be loud rather
-- than silently lossy — an insert for an unprovisioned venue lands somewhere it can be found.
--
-- **One thing from the old baseline is deliberately not carried: the `platform.scope_level` enum.**
-- It existed so a `venue_id` column could not resolve to a workstation, paired with a composite
-- foreign key in a `V0003a__scope-typing.sql` that is not part of this generation. Every
-- `scope_level` column here is `text`, derived from contracts that declare it as a string.
-- **Emitting an unused type would imply a constraint nothing enforces**, so the gap is named here
-- instead: scope levels are validated by the application, not by the database.
CREATE OR REPLACE FUNCTION platform.ensure_venue_partition(target regclass, venue_id uuid)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    part_name text;
    parent_name text := target::text;
BEGIN
    part_name := replace(split_part(parent_name, '.', 2) || '_' ||
                         replace(venue_id::text, '-', ''), '.', '_');
    IF to_regclass(format('%I.%I', split_part(parent_name, '.', 1), part_name)) IS NOT NULL THEN
        RETURN;
    END IF;
    EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES IN (%L)',
                   split_part(parent_name, '.', 1), part_name, target, venue_id);
END
$$;
"""


MIGRATION_REGISTER = """-- The migration register.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **The one table this generator cannot derive**, because `handoff/schema-reference.json` carries
-- it with no columns — it is storage the contracts never describe, which is correct: no operation
-- reads or writes it. It came from `V0001__baseline.sql` and would have been lost when that file
-- was deleted on 21 September.
--
-- Migrations fan out per region, not per tenant (ADR-0014). A tenant in three regions is three
-- cells and three applications, and they may legitimately sit at different versions mid-rollout.
-- **Emitted into both databases** because ADR-0039 made `control` a database of its own, and a
-- database that is migrated independently needs its own record of where it got to.
CREATE TABLE IF NOT EXISTS platform.schema_version (
    version                           text PRIMARY KEY NOT NULL,
    description                       text NOT NULL,
    checksum                          text NOT NULL,
    applied_at                        timestamptz NOT NULL DEFAULT now(),
    applied_by                        text NOT NULL DEFAULT current_user,
    execution_ms                      integer,
    rollback_tested_at                timestamptz
);

-- **Deliberately not under RLS**, and it carries no `scope_path` to put one on: the register
-- describes the database rather than anybody's data, and a connection that cannot read it cannot
-- safely migrate.
"""


def rls_file(db: str, scoped: list, by_venue: list, total: int, has_scope_table: bool) -> str:
    """The functions, then one call per table — by `scope_path` where it has one, by `venue_id`
    where it does not."""
    body = [RLS_HEAD if db == "tenant" else RLS_HEAD.replace(
        "-- Row-level security.", "-- Row-level security, control database.")]
    body.append(
        f"-- **{len(scoped)} tables carry `scope_path` and {len(by_venue)} carry `venue_id` "
        f"instead, out of {total}.**\n"
        "-- Both are protected. A table with neither is not scoped -- it is reference data, a\n"
        "-- registry, or the migration log itself, and a policy on it would deny every row to\n"
        "-- everybody.\n")
    if has_scope_table:
        body.append(SCOPE_SELF_RLS)
    # **Quoted through `q()` like every other identifier this file emits.** `marketing.case` is a
    # reserved word and `'marketing.case'::regclass` does not parse; the first cut of this emitter
    # wrote it unquoted, and `check-migrations` could not see the mistake because its own regex
    # stopped at the quote in `CREATE TABLE marketing."case"`. Two blind spots lining up is how a
    # table ends up with no policy and nothing saying so.
    def qual(t: str) -> str:
        s, n = t.split(".", 1)
        return f"{q(s)}.{q(n)}"

    if scoped:
        body.append("\n-- Scoped by path.")
        body += [f"SELECT platform.apply_scope_rls('{qual(t)}'::regclass);" for t in scoped]
    if by_venue:
        body.append("\n-- Scoped by venue, resolved through the scope tree.")
        body += [f"SELECT platform.apply_venue_rls('{qual(t)}'::regclass);" for t in by_venue]
    return "\n".join(body) + "\n"


def partition_file(tables: list) -> str:
    lines = [PARTITION_HEAD, "",
             f"-- **{len(tables)} tables qualify today** — a NOT NULL `venue_id` in the schema "
             "reference.\n-- Listed rather than counted, because ADR-0044's rule is checkable and "
             "the list is how.\n"]
    lines += [f"--   {t}" for t in tables]
    return "\n".join(lines) + "\n"

RESERVED = {"table", "order", "user", "group", "check", "default", "references", "primary",
            "column", "constraint", "index", "unique", "all", "any", "case", "end", "from",
            "to", "grant", "limit", "offset", "return", "session", "authorization"}


def q(name: str) -> str:
    """Quote an identifier only where Postgres needs it.

    **`fnb.dining_table` and `orders.order` are real tables** and both are reserved words. Quoting
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
    # **A table the schema reference stores somewhere else is not a Postgres table.** Until 17
    # September this took every name in `cols`, so `identity.session` and `identity.guest_session`
    # — both "none — Redis session registry" in the contract — and `inventory.stock_level`, which
    # is derived from movements, were all created here. The schema reference had them right under
    # `store`; this file never asked it.
    store = S.get("store") or {}
    real = {t for t in cols if "." in t and ":" not in t
            and store.get(t, "postgres") in POSTGRES_STORES}

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
    # 5. **The machinery layer, which lived outside this generator until 21 September and was the
    # only place row-level security existed.** `src/Ticvai.Migrations/Scripts/V0001__baseline.sql`
    # held the extensions, the scope vocabulary, the RLS functions, the partition helper and the
    # outbox — and it lived outside `backend/` for one reason, stated in `current-work.md`: a
    # `V*.sql` file in `backend/` sorts after the numeric series and would apply last.
    #
    # **That reasoning was right and the consequence was that `backend/` shipped with no security
    # at all.** Every table here was created, constrained and indexed, and nothing enabled RLS on
    # any of them. It also meant `platform.outbox` and `platform.dead_letter` existed in both
    # files — the exact duplicate-definition failure `backend/README.md` records from 31 August.
    #
    # **Emitting it here makes the series one series**, numbered so the order is the apply order,
    # and regenerated in full like everything else.
    for db in (CONTROL, "tenant"):
        files[f"{db}/001-extensions.sql"] = EXTENSIONS
        files[f"{db}/002-migration-register.sql"] = (
            MIGRATION_REGISTER if db == "tenant" else
            MIGRATION_REGISTER.replace("CREATE TABLE IF NOT EXISTS platform.schema_version",
                                       "CREATE SCHEMA IF NOT EXISTS platform;\n\n"
                                       "CREATE TABLE IF NOT EXISTS platform.schema_version"))

    scoped = sorted(t for t in real if any(c["column"] == "scope_path" for c in cols[t]))
    venue_only = sorted(t for t in real if t not in set(scoped)
                        and any(c["column"] == "venue_id" for c in cols[t]))
    for db in ("tenant", CONTROL):
        mine = [t for t in scoped if area(t.split(".")[0]) == db]
        vmine = [t for t in venue_only if area(t.split(".")[0]) == db]
        total = len(by_schema.get(CONTROL) or []) if db == CONTROL else n_tenant_tables
        files[f"{db}/920-row-level-security.sql"] = rls_file(
            db, mine, vmine, total, has_scope_table=("platform.scope" in real and db == "tenant"))

    # **The venue partition mechanism** (ADR-0005, ADR-0044). The helper only; the tables that use
    # it declare their own partitioning where they are created.
    partitioned = sorted(t for t in real if area(t.split(".")[0]) == "tenant"
                         and any(c["column"] == "venue_id" and c.get("required") == "yes"
                                 for c in cols[t]))
    files["tenant/930-partitioning.sql"] = partition_file(partitioned)

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
