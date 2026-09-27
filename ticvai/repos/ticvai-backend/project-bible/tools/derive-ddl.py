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
    backend/control/010-control.sql       the cell registry, tenants, billing, rollouts
    backend/control/900-foreign-keys.sql  references inside the control database
    backend/control/910-indexes.sql

    backend/tenant/000-schemas.sql        the tenant template's schemas
    backend/tenant/010-<schema>.sql       one file per schema
    backend/tenant/900-foreign-keys.sql   references inside a tenant database
    backend/tenant/910-indexes.sql

    backend/990-cross-database-references.sql  the references that no longer fit in either
    backend/provision-tenant.sh                CREATE DATABASE, apply the template, register the row

**The counts are printed by the run and written into each file's header, not kept here.** Every
number this docstring used to carry (46, 331, 25, 21, 932, 486) had gone stale by the time the
audit of 26 September read it.

**The cross-database references are the price of the split and they are stated rather than
dropped.** Postgres has no cross-database foreign key, so `subscription.contract.tenant_id ->
platform.tenant(id)` and the others stop being constraints the moment `control` becomes a database
of its own. They are emitted as commented-out `ALTER TABLE` lines with an index each, because an
integrity rule that moved into application code is a rule somebody has to be told about.

**Foreign keys go in a separate file on purpose.** The relationships cannot be ordered so that
every reference is already created -- `orders` reaches `catalogue` and `catalogue` reaches
`platform` and something reaches back. **Creating tables first and constraining afterwards is the
only ordering that terminates.**

**`enforced: no` references become an index and a comment, not a constraint.** Most references
are conventions rather than declared references (ADR-0011), and enforcing a convention the
contracts never asserted would fail on the first row of real data. **Every declared foreign key
is indexed as well** (data-and-storage.md: "Every foreign key indexed") -- Postgres does not index
the referencing column on its own.

**Object names follow naming-and-style 6.1**: `<table>_<columns>_idx` for an index,
`<table>_<column>_chk` for a check, `<table>_scope` for an RLS policy, and `<table>_<column>_fkey`
(the name Postgres itself gives) for a foreign key. The one 6.1 name not followed is the
partition's `<table>_v<venue_number>`: nothing in the package defines a venue number, so
`ensure_venue_partition` still names a partition after the venue's uuid.

**Contract enums, maxLength and defaults are carried** as a `<table>_<column>_chk` CHECK and a
column DEFAULT (storage-design.md, "Enum agreement": the database holds the same values as the
contract). Uniqueness and immutability rules the contracts state only in prose are not -- there
is nothing machine-readable to derive them from.

Run: `python3 tools/derive-ddl.py [--apply]`
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "backend"

# **The one schema that is a database.** ADR-0039 took `control` out of the tenant template,
# so the split is a fact this file has to hold rather than a string repeated in six branches.
CONTROL = "control"

# The scope tree: its `path` is the ltree every `scope_path` is compared against.
SCOPE_TABLE = "platform.scope"

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
CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path ltree)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path <@ ANY (platform.current_scope_paths());
$$;

-- Applies the standard policy to a table.
-- **FORCE is the whole point.** Without it the table owner — which is what a migration and most
-- pooled application connections run as — bypasses every policy silently.
--
-- **The policy is named `<table>_scope`** (naming-and-style 6.1). Until 26 September every table's
-- policy was called `scope_isolation` or `venue_isolation`; those names are dropped here too, so
-- re-applying the file to a database built before the rename leaves one policy, not two.
CREATE OR REPLACE FUNCTION platform.rls_policy_name(target regclass)
    RETURNS text
    LANGUAGE sql
    STABLE
AS $$
    SELECT left(c.relname, 57) || '_scope' FROM pg_class c WHERE c.oid = target;
$$;

CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS scope_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

-- **{n_venue} tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path`
-- alone leaves every one of them open.** `check-migrations` has said so since it was written --
-- checking only scope_path missed the tables that carry venue_id instead, and they would have
-- passed with no policy at all -- and the hand-written baseline never closed it because it
-- protected three tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on those {n_venue} tables**, and
-- `platform.scope` is small, cached and indexed on `id` and, with GiST, on `path`.
--
-- **A null `venue_id` is a tenant-level row, and until 24 September nobody could see it** — not
-- even head office, because the function opened with `row_venue_id IS NOT NULL`. It now follows
-- the tenant-root rule: such a row sits at the tenant root, so it is visible exactly when a
-- grant *is* that root — the one `platform.scope` row whose `level` is `tenant` (ADR-0011; the
-- node the cell creates at provisioning, `parentId` null). A brand, region or venue grant is
-- beneath the root, not at it, and still sees none of it. No grants, still nothing.
CREATE OR REPLACE FUNCTION platform.venue_in_scope(row_venue_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND CASE
             WHEN row_venue_id IS NULL THEN EXISTS (
                  SELECT 1 FROM platform.scope s
                   WHERE s.level = 'tenant'
                     AND s.path = ANY (platform.current_scope_paths()))
                  -- one tenant per database (CF-161); if that ever stops being true, a null-venue
                  -- row has no single tenant to belong to, so it is hidden rather than shown to all
                  AND (SELECT count(*) FROM platform.scope s WHERE s.level = 'tenant') = 1
             ELSE EXISTS (
                  SELECT 1 FROM platform.scope s
                   WHERE s.id = row_venue_id
                     AND s.path <@ ANY (platform.current_scope_paths()))
           END;
$$;

CREATE OR REPLACE FUNCTION platform.apply_venue_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS venue_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.venue_in_scope(venue_id)) '
        'WITH CHECK (platform.venue_in_scope(venue_id))', policy_name, target);
END
$$;
"""

# Where the venue half of RLS_HEAD starts; the control database's file is cut here.
VENUE_MARKER = "-- **{n_venue} tables carry `venue_id`"
assert VENUE_MARKER in RLS_HEAD

# **A child row is as visible as the row that owns it.** Until 26 September a table with neither
# `scope_path` nor `venue_id` got no policy at all and the file called it "reference data, a
# registry, or the migration log" -- while `orders.order_line`, `games.credit_ledger`,
# `approvals.decision` and a hundred others like them are tenant data hanging off a scoped parent
# by a NOT NULL declared foreign key. permission-resolution 7.1 says every tenant-scoped table is
# under FORCE row-level security; this is how those tables meet it without carrying a copied
# `scope_path` that could disagree with the parent's.
#
# The subquery reads the parent **under the parent's own policy**, so the rule composes down a
# chain (line -> order -> scope) and a grant that cannot see the order cannot see its lines. The
# generator only ever points a child at a parent that already has a policy, so no chain can loop
# back on itself -- a cycle of policies is an error Postgres raises at query time.
RLS_PARENT = """
-- A child table protected through the declared foreign key to the row that owns it. The row is
-- visible, and may be written, exactly when its parent is visible to the same connection.
CREATE OR REPLACE FUNCTION platform.apply_parent_rls(target regclass, fk_column text,
                                                     parent regclass, parent_key text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('EXISTS (SELECT 1 FROM %s parent_row WHERE parent_row.%I = %s.%I)',
                             parent, parent_key, target, fk_column);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (%s) WITH CHECK (%s)',
                   policy_name, target, predicate, predicate);
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
DROP POLICY IF EXISTS scope_scope ON platform.scope;
CREATE POLICY scope_scope ON platform.scope
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
-- `scope_level` column here is `text`; where its contract declares the enum, the column carries a
-- `<table>_<column>_chk` CHECK with the contract's values, like every other contract enum. That a
-- `venue_id` resolves to a venue and not a workstation is still the application's to check.
--
-- **Partitions are named `<table>_<venue uuid hex>`, not naming-and-style 6.1's
-- `<table>_v<venue_number>`.** Nothing in the package defines or allocates a venue number, so
-- there is nothing to derive the 6.1 name from; that is a decision to make, not a rename.
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


def rls_file(db: str, scoped: list, by_venue: list, by_parent: list, unscoped: list,
             total: int, has_scope_table: bool) -> str:
    """The functions, then one call per table -- by `scope_path` where it has one, by `venue_id`
    where it does not, and through its owning parent where it has neither.

    `by_parent` is `(table, fk_column, parent, parent_key)`; `unscoped` is `(table, why)`."""
    head = RLS_HEAD.replace("{n_venue}", str(len(by_venue)))
    if db != "tenant":
        # **The control database has no scope tree** (ADR-0039 took `control` out of the tenant
        # template), so `venue_in_scope` there looked up a `platform.scope` that does not exist and the
        # migration failed at the function. Found 24 September. Its venue tables are the operator's
        # own cross-tenant records -- today only `control.usage_record`, the billing log the invoice run
        # reads -- guarded by who may connect to the control database, not by a venue grant. So the
        # control file carries no venue functions and no venue policies.
        cut = head.index(VENUE_MARKER.replace("{n_venue}", str(len(by_venue))))
        head = head[:cut].replace("-- Row-level security.", "-- Row-level security, control database.")
    body = [head]
    if by_parent:
        body.append(RLS_PARENT)
    n_venue = len(by_venue) if db == "tenant" else 0
    # **Counted, not asserted.** The line this replaced called every table with neither column
    # "reference data, a registry, or the migration log", and the audit of 26 September found
    # PII, principals and order lines among them. What is left unscoped is now listed by name with
    # the reason, so the claim can be checked rather than believed.
    body.append(
        f"-- **{total} tables: {len(scoped)} scoped by `scope_path`, {n_venue} by `venue_id`, "
        f"{len(by_parent)} through the parent that owns them, {len(unscoped)} with no policy.**\n"
        "-- A table with no policy is listed at the end of this file with the reason. It is not\n"
        "-- claimed to be reference data: for most of them that is a scoping decision nobody has\n"
        "-- made yet, and they stay readable by every connection to this database until it is.\n")
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
    if by_venue and db != "tenant":
        body.append("\n-- Carries venue_id but not scoped here: the control database has no scope tree to "
                    "resolve a venue against, and these are operator records read across tenants.")
        body += [f"--   {qual(t)}" for t in by_venue]
    elif by_venue:
        body.append("\n-- Scoped by venue, resolved through the scope tree.")
        body += [f"SELECT platform.apply_venue_rls('{qual(t)}'::regclass);" for t in by_venue]
    if by_parent:
        # **In dependency order**, parents before children: a child's policy reads its parent, and
        # the parent's policy has to exist for that read to be scoped at all.
        body.append("\n-- Scoped through the parent that owns the row (a NOT NULL declared foreign key).")
        body += [f"SELECT platform.apply_parent_rls('{qual(t)}'::regclass, '{col}', "
                 f"'{qual(par)}'::regclass, '{key}');" for t, col, par, key in by_parent]
    if unscoped:
        body.append("\n-- No policy. Each needs a scoping decision (carry scope_path or venue_id, or a\n"
                    "-- NOT NULL owning reference) before row-level security can hold for it.")
        body += [f"--   {qual(t)}  -- {why}" for t, why in unscoped]
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


def obj_name(*parts: str, suffix: str) -> str:
    """A naming-and-style 6.1 object name, `<table>_<columns>_<suffix>`, within Postgres's 63 bytes.

    **Postgres truncates a longer identifier silently**, and two truncated names that collide make
    the second `CREATE INDEX IF NOT EXISTS` a no-op nobody sees. A long name is cut and given a
    hash of the whole, so it stays unique and stays the same from run to run."""
    name = "_".join(parts + (suffix,))
    if len(name.encode("utf-8")) <= 63:
        return name
    h = hashlib.sha1(name.encode("utf-8")).hexdigest()[:8]
    return f"{name[:63 - len(suffix) - 10]}_{h}_{suffix}"


def sql_literal(v) -> str:
    return "'" + str(v).replace("'", "''") + "'"


def load_contract_props() -> dict:
    """`module.Schema.property` -> the contract property, with `$ref` and `allOf` followed.

    The schema reference names each column's contract `source` but does not carry its enum,
    maxLength or default, so they are read from the contracts here."""
    docs = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        try:
            docs[f.stem] = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue

    def resolve(doc, node, depth=0):
        while isinstance(node, dict) and "$ref" in node and depth < 8:
            file_part, _, frag = str(node["$ref"]).partition("#")
            if file_part:
                doc = docs.get(Path(file_part).stem)
                if doc is None:
                    return None, {}
            cur = doc
            for p in frag.lstrip("/").split("/"):
                cur = cur.get(p, {}) if isinstance(cur, dict) else {}
            node, depth = cur, depth + 1
        return doc, node if isinstance(node, dict) else {}

    def props_of(doc, schema, depth=0):
        doc, schema = resolve(doc, schema)
        out = {}
        if doc is None or depth > 8:
            return out
        for part in schema.get("allOf") or []:
            out.update(props_of(doc, part, depth + 1))
        for k, v in (schema.get("properties") or {}).items():
            out[k] = resolve(doc, v)[1]
        return out

    found = {}
    for mod, doc in docs.items():
        if not isinstance(doc, dict):
            continue
        for name, schema in ((doc.get("components") or {}).get("schemas") or {}).items():
            for prop, spec in props_of(doc, schema).items():
                found[f"{mod}.{name}.{prop}"] = spec
    return found


def column_rules(short: str, col: str, typ: str, spec: dict) -> str:
    """The DEFAULT and CHECK a contract property asks of its column, or "".

    **Carried, not left to the application** (storage-design.md "Enum agreement": the database
    holds the same values as the contract; naming-and-style 6.1 names the check). Adding an enum
    value is already a breaking change under ADR-0026, so the migration a new value needs is not a
    new cost. Only a scalar column is given a check; an array's items and a json shape are left to
    the application, and so is anything a contract states only in prose -- a uniqueness rule in a
    description, "immutable once complete" -- because there is nothing machine-readable to derive
    it from."""
    out = ""
    d = spec.get("default")
    if d is not None:
        if typ == "boolean" and isinstance(d, bool):
            out += f" DEFAULT {'true' if d else 'false'}"
        elif (typ in ("integer", "bigint", "smallint") and isinstance(d, int)
              and not isinstance(d, bool)):
            out += f" DEFAULT {d}"
        elif (typ.startswith(("numeric", "double precision", "real"))
              and isinstance(d, (int, float)) and not isinstance(d, bool)):
            out += f" DEFAULT {d}"
        elif typ == "text" and isinstance(d, str):
            out += f" DEFAULT {sql_literal(d)}"
    checks = []
    if typ == "text":
        values = [v for v in (spec.get("enum") or []) if v is not None]
        if values and all(isinstance(v, str) for v in values):
            checks.append(f"{q(col)} IN ({', '.join(sql_literal(v) for v in values)})")
        n = spec.get("maxLength")
        if isinstance(n, int) and not isinstance(n, bool) and n > 0:
            checks.append(f"char_length({q(col)}) <= {n}")
    if checks:
        out += (f" CONSTRAINT {obj_name(short, col, suffix='chk')} CHECK ("
                + " AND ".join(checks) + ")")
    return out


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
    # **No schema history is written into the header.** "the count went 26 to 25" sat beside a
    # computed "32 schemas" for weeks; a count this run cannot compute is a count that goes stale.
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
        "-- **`control` is not here.** It left the template in ADR-0039 and is a database of its own.",
        "",
    ] + [f"CREATE SCHEMA IF NOT EXISTS {q(s)};" for s in tenant_schemas]) + "\n"

    # 2. tables, one file per schema
    # **Routed, not collected.** A reference whose two ends are now in different databases
    # cannot be a constraint, and a file that emits it anyway does not apply. Each line is kept
    # with the schema it came from so the assembly below can put it where it can actually run.
    fk_lines: list[tuple[str, str]] = []
    idx_lines: list[tuple[str, str]] = []
    xdb_lines: list[str] = []
    n_tables = n_cols = n_fk = n_idx = n_xdb = n_chk = n_def = 0
    unkeyed: list = []
    # A table's NOT NULL declared references inside its own database: `(column, parent, key)`.
    # Row-level security uses them to protect a child through the row that owns it.
    owners: dict[str, list] = defaultdict(list)
    contract_props = load_contract_props()

    # **One name per index per schema.** naming-and-style 6.1's `<table>_<columns>_idx` can make
    # the same string from two tables (`a_b` + `c`, `a` + `b_c`), and `CREATE INDEX IF NOT EXISTS`
    # would quietly skip the second. A clash is made unique with a hash of the table and column.
    index_names: dict[tuple[str, str], str] = {}

    def index_name(schema: str, short: str, col: str) -> str:
        name = obj_name(short, col, suffix="idx")
        owner = f"{short}.{col}"
        if index_names.setdefault((schema, name), owner) != owner:
            h = hashlib.sha1(owner.encode("utf-8")).hexdigest()[:6]
            name = obj_name(short, col, h, suffix="idx")
            index_names[(schema, name)] = owner
        return name

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
                # **`scope_path` is an ltree** (ADR-0011, naming-and-style 5.3). Until 24 September it
                # came through as the contract's `string`, so 515 tables stored text and `in_scope`
                # cast every row to ltree at query time, which no index can serve.
                #
                # **`platform.scope.path` is the same thing under its own name** -- the materialised
                # path every other `scope_path` is compared against. It stayed text after 24
                # September, so every venue policy cast it with `s.path::ltree` and the GiST index
                # 001-extensions promises for the scope tree did not exist.
                is_path = (col == "scope_path" or col.endswith("_scope_path")
                           or (t == SCOPE_TABLE and col == "path"))
                if is_path:
                    typ = "ltree"
                nn = " NOT NULL" if c.get("required") == "yes" else ""
                # **A row-level-security `scope_path` cannot be null.** `in_scope` opens with
                # `row_scope_path IS NOT NULL` and is both USING and WITH CHECK under FORCE, so a
                # null path could never be inserted and would be invisible to head office if it
                # were. Until 26 September 252 of the 263 tables under `apply_scope_rls` declared it
                # nullable anyway. A tenant-level row is stored at the tenant root path
                # (naming-and-style 5.3), not at null.
                if col == "scope_path":
                    nn = " NOT NULL"
                pk = " PRIMARY KEY" if col == tkey else ""
                # **Contract enums, maxLength and defaults become a CHECK and a DEFAULT.** Not on
                # a path column: its contract type is a string and its column is an ltree.
                rules = "" if is_path else column_rules(
                    short, col, typ, contract_props.get(str(c.get("source") or ""), {}))
                if " CONSTRAINT " in rules:
                    n_chk += 1
                if " DEFAULT " in rules:
                    n_def += 1
                # **The space after the name is not padding.** Until 26 September this was
                # `{q(col):<34}{typ}` with nothing between, so a name of 34 characters or more ran
                # into its type -- `requires_corrective_action_on_breachboolean` -- and five
                # CREATE TABLE statements in four files could not be parsed.
                body.append(f"    {q(col):<33} {typ}{pk}{nn}{rules}")
                n_cols += 1

                ref = c.get("references")
                if ref and ref in real:
                    tgt_s, tgt_t = ref.split(".", 1)
                    tgt_key = key_of(ref, cols)
                    if c.get("enforced") == "yes" and tgt_key:
                        stmt = (f"ALTER TABLE {q(schema)}.{q(short)} ADD CONSTRAINT "
                                f"{obj_name(short, col, suffix='fkey')} FOREIGN KEY ({q(col)}) "
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
                            if col != tkey:
                                idx_lines.append((schema,
                                    f"-- crosses the database boundary: {t}.{col} -> {ref}\n"
                                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, col)} "
                                    f"ON {q(schema)}.{q(short)} ({q(col)});"))
                                n_idx += 1
                            n_xdb += 1
                        else:
                            fk_lines.append((schema, stmt))
                            n_fk += 1
                            # **Every declared foreign key is indexed** (data-and-storage.md). Until
                            # 26 September only conventions were: Postgres does not index the
                            # referencing column itself, so none of the declared keys had one, and
                            # every parent delete or join scanned the child. The primary key already
                            # serves a column that is the key.
                            if col != tkey:
                                idx_lines.append((schema,
                                    f"-- declared: {t}.{col} -> {ref}\n"
                                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, col)} "
                                    f"ON {q(schema)}.{q(short)} ({q(col)});"))
                                n_idx += 1
                            if c.get("required") == "yes" and ref != t:
                                owners[t].append((col, ref, tgt_key))
                    elif c.get("enforced") == "yes":
                        # **A declared reference to a table with no addressable key.** Reported
                        # rather than emitted — a constraint that cannot be created fails the whole
                        # file, and silently downgrading it to an index hides a real modelling gap.
                        unkeyed.append(f"{t}.{col} -> {ref}")
                        if col != tkey:
                            idx_lines.append((schema,
                                f"-- declared but {ref} has no addressable key: {t}.{col}\n"
                                f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, col)} "
                                f"ON {q(schema)}.{q(short)} ({q(col)});"))
                            n_idx += 1
                    else:
                        # **A convention is indexed, not constrained.** Most references are naming
                        # habits the contracts never asserted (ADR-0011) -- enforcing one fails on
                        # the first row that legitimately points nowhere. A self-reference on the
                        # key (`games.play.play_id`) is not indexed twice: the primary key is it.
                        if col != tkey:
                            idx_lines.append((schema,
                                f"-- convention, not declared: {t}.{col} -> {ref}\n"
                                f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, col)} "
                                f"ON {q(schema)}.{q(short)} ({q(col)});"))
                            n_idx += 1

            # **Every table carries `scope_path` if it has one** — that is the partition key
            # (ADR-0005), and an ltree index on it is what makes a scope walk cheap.
            if "scope_path" in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, 'scope_path')} "
                    f"ON {q(schema)}.{q(short)} USING gist ({q('scope_path')});"))
                n_idx += 1
            # **The scope tree's own path, GiST-indexed** as 001-extensions says it is: every venue
            # policy resolves a venue through it with `<@`.
            if t == SCOPE_TABLE and "path" in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, 'path')} "
                    f"ON {q(schema)}.{q(short)} USING gist (path);"))
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
            f"-- Indexes in the {db} database: declared foreign keys, conventions and scope paths.",
            "-- **Derived by tools/derive-ddl.py. Do not hand-edit.**",
            "--",
            "-- **Every declared foreign key is indexed** (data-and-storage.md) -- Postgres does not",
            "-- index the referencing column itself. **A convention is indexed and not constrained**",
            "-- (ADR-0011): most references are naming habits the contracts never asserted, and",
            "-- enforcing one fails on the first row that legitimately points nowhere.",
            "-- Names follow naming-and-style 6.1: `<table>_<columns>_idx`.",
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
    # **The rest are protected through the row that owns them, where one does.** A table with
    # neither column gets a parent policy when it has a NOT NULL declared reference, inside its own
    # database, to a table that is already protected. Built in rounds so a parent's policy always
    # exists before its child's, which is also what keeps a chain of policies from looping.
    #
    # **Only a NOT NULL reference owns a row.** A nullable one would hide every row where it is
    # null -- the defect `scope_path` had -- and it usually names an association (a cost centre, a
    # home scope) rather than an owner. **Only one protected owner, or several that are the same
    # table.** A reference to a table with no policy (`approvals.decision.principal_id`) carries no
    # scope to inherit and is not a candidate, and a parent protected in an earlier round (nearer a
    # scope column) is taken before one protected later. Where two different parents become
    # protected in the same round, which of them owns the row is a modelling decision, and the
    # table is listed as unscoped with both named.
    protected: dict[str, str] = {t: "scope" for t in scoped}
    protected.update({t: "venue" for t in venue_only if area(t.split(".")[0]) == "tenant"})
    if SCOPE_TABLE in real:
        protected[SCOPE_TABLE] = "self"
    by_parent: list[tuple[str, str, str, str]] = []
    while True:
        round_ = []
        for t in sorted(real):
            if t in protected:
                continue
            cands = [o for o in owners.get(t, []) if o[1] in protected]
            if cands and len({o[1] for o in cands}) == 1:
                col, par, key = sorted(cands)[0]
                round_.append((t, col, par, key))
        if not round_:
            break
        for t, col, par, key in round_:
            protected[t] = "parent"
            by_parent.append((t, col, par, key))

    def why_unscoped(t: str) -> str:
        own = owners.get(t, [])
        prot = [o for o in own if o[1] in protected]
        if len({o[1] for o in prot}) > 1:
            return ("several protected owners (" + ", ".join(f"{c} -> {p}" for c, p, _ in prot)
                    + "); which one owns the row is not decided")
        if own:
            return ("its owner" + ("s " if len({o[1] for o in own}) > 1 else " ")
                    + ", ".join(sorted({o[1] for o in own})) + " ha"
                    + ("ve" if len({o[1] for o in own}) > 1 else "s") + " no policy either")
        nullable = [c for c in cols[t] if c.get("references") in real and c.get("enforced") == "yes"
                    and c.get("required") != "yes"
                    and area(str(c["references"]).split(".")[0]) == area(t.split(".")[0])]
        if nullable:
            return ("only nullable references (" + ", ".join(
                f"{c['column']} -> {c['references']}" for c in nullable) + ")")
        return "no scope column and no declared owner"

    unscoped_all = [t for t in sorted(real)
                    if t not in protected and t not in venue_only and t != SCOPE_TABLE]
    for db in ("tenant", CONTROL):
        mine = [t for t in scoped if area(t.split(".")[0]) == db]
        vmine = [t for t in venue_only if area(t.split(".")[0]) == db]
        pmine = [p for p in by_parent if area(p[0].split(".")[0]) == db]
        umine = [(t, why_unscoped(t)) for t in unscoped_all if area(t.split(".")[0]) == db]
        total = len(by_schema.get(CONTROL) or []) if db == CONTROL else n_tenant_tables
        files[f"{db}/920-row-level-security.sql"] = rls_file(
            db, mine, vmine, pmine, umine, total,
            has_scope_table=(SCOPE_TABLE in real and db == "tenant"))

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

    print(f"  {n_tables} tables · {n_cols} columns · {n_fk} foreign keys · {n_idx} indexes · "
          f"{n_chk} checks · {n_def} defaults")
    print(f"  row-level security: {len(scoped)} by scope_path · {len(venue_only)} carry venue_id · "
          f"{len(by_parent)} through their owner · {len(unscoped_all)} with no policy")
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
