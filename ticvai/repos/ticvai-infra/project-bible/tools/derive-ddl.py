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
(the name Postgres itself gives) for a foreign key. A monthly partition is `<table>_p<YYYYMM>` and
the catch-all `<table>_default`. **6.1's venue partition `<table>_v<venue_number>` is not emitted**:
ADR-0056 (30 September) defers venue list partitioning, so no table partitions by venue.

**ADR-0056 and ADR-0058, accepted 30 September**, are carried as rules, not lists:

  * **One id type.** Every key named `id` or `*_id` is `uuid`, and so is every declared reference
    to one (new ids are UUIDv7). A human code used as a key (`games.card.card_code`) is not an id.
  * **Range partitioning by month** for a table whose contract schema is marked
    `x-ticvai-append-only: <time property>`, which has that column and no inbound foreign key. Its
    key becomes `(<key>, <time column>)`; 930-partitioning.sql creates the partitions.
  * **Composite venue keys** where a child and its parent both carry a NOT NULL `venue_id`: the
    reference is `(venue_id, x) -> parent (venue_id, id)` against a parent `UNIQUE (venue_id, id)`.
  * **A key the contract names** (`x-ticvai-primary-key`, `kernel.inbox`'s `(consumer, event_id)`).

Vectors are not here: they live in each tenant's Qdrant collection (decided 30 September), and
`ai.chunk_embedding` holds only the reference to the point.

**Contract enums, maxLength and defaults are carried** as a `<table>_<column>_chk` CHECK and a
column DEFAULT (storage-design.md, "Enum agreement": the database holds the same values as the
contract). **Uniqueness is carried where the contract marks it**: a property with
`x-ticvai-unique: tenant` or `venue` becomes a `<table>_<columns>_uniq` unique index (audit R108,
28 September). Uniqueness and immutability rules the contracts state only in prose are not --
there is nothing machine-readable to derive them from.

**Frozen once the git tag `r1` exists** (plan item 1C, C3, 1 October). From then on this does not
rewrite a baseline `.sql` file under `backend/`: databases were built from them. It writes the
additive part of the change (new tables, columns, indexes) as the next forward migration,
`backend/<area>/V<nnnn>__after_r1_<yyyymmdd>.sql`, numbered from V0100, and lists everything that is
not additive (drops, renames, type changes) for a person in `handoff/migration-review.md`
(`tools/ddl_forward.py`). `tools/check-migration-freeze.py` fails if a baseline file changes anyway.

Run: `python3 tools/derive-ddl.py [--apply] [--baseline REF]`   (--baseline: test a freeze without the tag)
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ddl_forward  # noqa: E402
from release_baseline import baseline_commit, ls_tree, show  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "backend"
REVIEW = ROOT / "handoff" / "migration-review.md"
# **A forward migration: written after r1, never regenerated.** `V` sorts after every digit, so
# provision-tenant.sh and the initdb pass, which apply `<area>/*.sql` in name order, run these after the
# baseline's 930 file.
FORWARD_FILE = re.compile(r"^V(\d+)__[\w.-]+\.sql$")
FORWARD_FIRST = 100

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

# **A table name is `<schema>.<table>` in lower-case identifiers, and nothing else is a table.**
# Until 29 September (system-design review SD-007) the schema reference carried two "tables" named
# `embedded as attributes (jsonb) on orders.cart_line and orders.order_line` and `embedded as
# window_starts_at and window_ends_at on ...`: the text after `none —` in an `x-ticvai-persistence`
# tag, kept by an additive lineage entry and re-derived every run. This file created two schemas,
# two tables and six foreign keys from them, so the first migration (MIG-BASELINE) failed on
# `CREATE SCHEMA IF NOT EXISTS embedded as ...`. A name that is not an identifier pair is refused
# here whatever upstream says, and a column pointing at one is dropped with it.
VALID_TABLE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


def is_not_persisted(tag) -> bool:
    """`x-ticvai-persistence` values that name no table: anything starting with `none`."""
    return isinstance(tag, str) and tag.strip().strip('"').lower().startswith("none")

# **A row that belongs to two scopes at once.** A stock transfer is owned at the source venue and
# has to be read and received at the destination (decided 28 September, audit R183). It used to
# sit at the tenant above both, where neither venue could see it. The second path is named here
# rather than inferred from any `*_scope_path` column: `target_scope_path` and
# `branch_scope_path` elsewhere name what a row is *about*, not who may see it, and widening
# visibility is a decision, not a naming habit.
SHARED_SCOPE = {
    "inventory.transfer": "to_scope_path",
}

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

-- **A row shared by two scopes** (audit R183): visible, and writable, from either path. A stock
-- transfer is owned at the source venue's `scope_path` and admits the destination through its
-- second path, so the receiving venue can read and receive it. Its lines follow through the
-- parent policy like any other child.
CREATE OR REPLACE FUNCTION platform.apply_shared_scope_rls(target regclass, second_path text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('(platform.in_scope(scope_path) OR platform.in_scope(%I))',
                             second_path);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS scope_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING %s WITH CHECK %s',
                   policy_name, target, predicate, predicate);
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

# **No tenant table is left open** (system-design review SD-015, 29 September). Until then 212 tenant
# tables -- `pii.subject*`, `payments.token`, `wallet.*`, `identity.principal` among them -- had no policy
# and were readable by every connection to the tenant database. A table with neither a scope column nor
# a protected owner now gets one of two policies instead of none:
#
#   * **by subject** where it carries `subject_id`: the row is visible to the session whose
#     `ticvai.subject_id` it is (a guest reading their own wallet), and to a tenant-root grant;
#   * **tenant root only** otherwise: visible only to a connection whose grant *is* the tenant root --
#     head office and the system scope workers run under -- and to nobody scoped below it.
#
# `pii.*` and `payments.token` are additionally meant to be reached only through their owning service's
# role (grants, not RLS); that is recorded in the file, and the policy is the floor under it.
RLS_TENANT = """
-- True when the connection holds the tenant root itself (head office, or a worker's system scope).
CREATE OR REPLACE FUNCTION platform.tenant_root_in_scope()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND EXISTS (SELECT 1 FROM platform.scope s
                    WHERE s.level = 'tenant'
                      AND s.path = ANY (platform.current_scope_paths()));
$$;

-- True when the row belongs to the session's own subject, or the connection holds the tenant root.
CREATE OR REPLACE FUNCTION platform.subject_in_scope(row_subject_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT (row_subject_id IS NOT NULL
            AND row_subject_id::text = NULLIF(current_setting('ticvai.subject_id', true), ''))
        OR platform.tenant_root_in_scope();
$$;

CREATE OR REPLACE FUNCTION platform.apply_tenant_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (platform.tenant_root_in_scope()) '
                   'WITH CHECK (platform.tenant_root_in_scope())', policy_name, target);
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_subject_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (platform.subject_in_scope(subject_id)) '
                   'WITH CHECK (platform.subject_in_scope(subject_id))', policy_name, target);
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

PARTITION_HEAD = """-- Partitioning (ADR-0056, accepted 30 September 2026; amends ADR-0044).
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Release 1 partitions by time, not by venue.** The tables that grow, grow with time: scans,
-- the outbox and its dead letters, the audit trail, journal lines, message dispatches and the
-- consumer inboxes. The rule is read from the schema, like every other rule in this generator: a
-- contract schema marked `x-ticvai-append-only: <time property>`, whose table has that column and
-- no inbound foreign key, is created `PARTITION BY RANGE` on the column, with the column in its
-- primary key. **Those tables declare their partitioning where they are created** (`010-<schema>.sql`);
-- what lives here is each one's DEFAULT partition and the monthly partitions ahead of today.
--
-- **Nothing points at a partitioned table**, which is part of the rule rather than a coincidence:
-- a foreign key into it would have to carry the time column too. Retention (ADR-0047) detaches
-- and archives a whole month instead of deleting rows.
--
-- **The inboxes partition on `event_id`, not on `processed_at`.** Their key is `(consumer,
-- event_id)` because that pair is the de-duplication rule (ADR-0058), and Postgres requires the
-- partition column in every unique key; a key that also carried `processed_at` would let a
-- redelivery insert a second row. The event id is a UUIDv7 (ADR-0056), whose first 48 bits are its
-- millisecond timestamp, so a month is the range between two UUIDv7 floors.
--
-- **Every partitioned table has a DEFAULT partition.** Misconfiguration should be loud rather than
-- silently lossy: a row for a month nobody created (an offline scan from before the first
-- partition, a clock years out) lands somewhere it can be found, and the job that creates the next
-- month fails on it instead of dropping it.
--
-- **Venue list partitioning is deferred, not cancelled** (ADR-0056 section 3). `venue_id NOT NULL`
-- stays where it is and no table gains a `venue_id` column for it. Where a child and its parent both
-- carry a NOT NULL `venue_id`, the foreign key between them is composite `(venue_id, <key>)` against a
-- parent `UNIQUE (venue_id, id)` (900-foreign-keys.sql), which keeps most of ADR-0044's cross-venue
-- guarantee; venue isolation on reads is row-level security (920-row-level-security.sql). Revisit:
-- a tenant with more than 100 venues, or one venue that needs its own vacuum or archive.

-- The smallest UUIDv7 minted at or after `ts`: its 48-bit millisecond timestamp and zeros after.
-- uuid comparison is bytewise, so every UUIDv7 from that millisecond on sorts at or above it.
CREATE OR REPLACE FUNCTION platform.uuidv7_floor(ts timestamptz)
    RETURNS uuid
    LANGUAGE sql
    IMMUTABLE
    PARALLEL SAFE
AS $$
    SELECT (substr(h, 1, 8) || '-' || substr(h, 9, 4) || '-0000-0000-000000000000')::uuid
      FROM (SELECT lpad(to_hex(floor(extract(epoch FROM ts) * 1000)::bigint), 12, '0') AS h) x;
$$;

-- Creates `<table>_p<YYYYMM>` for the month containing `month_start`, if it is missing. The bounds
-- follow the partition column's type: timestamps for a time column, UUIDv7 floors for a uuid.
CREATE OR REPLACE FUNCTION platform.ensure_month_partition(target regclass, month_start date)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    schema_name text := split_part(target::text, '.', 1);
    part_name text := split_part(replace(target::text, '"', ''), '.', 2) || '_p'
                      || to_char(date_trunc('month', month_start), 'YYYYMM');
    key_type text;
    lo timestamptz := date_trunc('month', month_start);
    hi timestamptz := date_trunc('month', month_start) + interval '1 month';
BEGIN
    IF to_regclass(format('%I.%I', schema_name, part_name)) IS NOT NULL THEN
        RETURN;
    END IF;
    SELECT format_type(a.atttypid, a.atttypmod) INTO key_type
      FROM pg_partitioned_table p
      JOIN pg_attribute a ON a.attrelid = p.partrelid AND a.attnum = p.partattrs[0]
     WHERE p.partrelid = target;
    IF key_type = 'uuid' THEN
        EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES FROM (%L) TO (%L)',
                       schema_name, part_name, target,
                       platform.uuidv7_floor(lo), platform.uuidv7_floor(hi));
    ELSE
        EXECUTE format('CREATE TABLE %I.%I PARTITION OF %s FOR VALUES FROM (%L) TO (%L)',
                       schema_name, part_name, target, lo, hi);
    END IF;
END
$$;

-- This month and `months_ahead` after it. The kernel's partition job (MIG-PARTITIONS) calls this
-- daily with 3; the calls at the end of this file give a new tenant database the same horizon.
CREATE OR REPLACE FUNCTION platform.ensure_month_partitions(target regclass, months_ahead integer)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    FOR i IN 0..months_ahead LOOP
        PERFORM platform.ensure_month_partition(
            target, (date_trunc('month', now()) + make_interval(months => i))::date);
    END LOOP;
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
             total: int, has_scope_table: bool, shared: dict | None = None,
             by_subject: list | None = None, tenant_only: list | None = None) -> str:
    """The functions, then one call per table -- by `scope_path` where it has one, by `venue_id`
    where it does not, and through its owning parent where it has neither.

    `by_parent` is `(table, fk_column, parent, parent_key)`; `unscoped` is `(table, why)`;
    `shared` maps a scoped table to the second path column that also admits a caller."""
    shared = shared or {}
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
    by_subject = by_subject or []
    tenant_only = tenant_only or []
    if by_parent:
        body.append(RLS_PARENT)
    if by_subject or tenant_only:
        body.append(RLS_TENANT)
    n_venue = len(by_venue) if db == "tenant" else 0
    # **Counted, not asserted.** The line this replaced called every table with neither column
    # "reference data, a registry, or the migration log", and the audit of 26 September found
    # PII, principals and order lines among them. What is left unscoped is now listed by name with
    # the reason, so the claim can be checked rather than believed.
    body.append(
        f"-- **{total} tables: {len(scoped)} scoped by `scope_path`, {n_venue} by `venue_id`, "
        f"{len(by_parent)} through the parent that owns them, {len(by_subject)} by subject, "
        f"{len(tenant_only)} to the tenant root only, {len(unscoped)} with no policy.**\n"
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
        body += [f"SELECT platform.apply_scope_rls('{qual(t)}'::regclass);" for t in scoped
                 if t not in shared]
    mine_shared = sorted(t for t in scoped if t in shared)
    if mine_shared:
        body.append("\n-- Scoped by either of two paths: owned at scope_path, shared with a second "
                    "scope (audit R183).")
        body += [f"SELECT platform.apply_shared_scope_rls('{qual(t)}'::regclass, '{shared[t]}');"
                 for t in mine_shared]
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
    if by_subject:
        body.append("\n-- By subject (SD-015): the session's own subject, or the tenant root.")
        body += [f"SELECT platform.apply_subject_rls('{qual(t)}'::regclass);" for t, _ in by_subject]
    if tenant_only:
        body.append("\n-- Tenant root only (SD-015): no scope column and no protected owner, so visible only\n"
                    "-- to a connection holding the tenant root. `pii.*` and `payments.token` are also\n"
                    "-- reached only through their owning service's role; this policy is the floor.")
        body += [f"SELECT platform.apply_tenant_rls('{qual(t)}'::regclass);  -- was: {why}"
                 for t, why in tenant_only]
    if unscoped:
        body.append("\n-- No policy. Each needs a scoping decision (carry scope_path or venue_id, or a\n"
                    "-- NOT NULL owning reference) before row-level security can hold for it.")
        body += [f"--   {qual(t)}  -- {why}" for t, why in unscoped]
    return "\n".join(body) + "\n"


def partition_file(partitioned: dict, declined: list) -> str:
    """The DEFAULT partition of every range-partitioned table, then this month and three ahead.

    `partitioned` maps a table to its partition column; `declined` is `(table, why)` for a table
    whose contract says append-only and which the rule still refused."""
    def qual(t: str) -> str:
        s, n = t.split(".", 1)
        return f"{q(s)}.{q(n)}"

    lines = [PARTITION_HEAD,
             f"-- **{len(partitioned)} tables are range-partitioned by month** — append-only in "
             "their contract,\n-- with the time column present and no inbound foreign key. "
             "Listed rather than counted, because\n-- the rule is checkable and the list is how.",
             ""]
    lines += [f"--   {t:<34} on {c}" for t, c in sorted(partitioned.items())]
    if declined:
        lines += ["", "-- Marked append-only in the contract and not partitioned, with the reason:"]
        lines += [f"--   {t}  -- {why}" for t, why in sorted(declined)]
    lines += ["", "-- DEFAULT partitions: a row for a month nobody created is kept, and found."]
    for t in sorted(partitioned):
        s, n = t.split(".", 1)
        lines.append(f"CREATE TABLE IF NOT EXISTS {q(s)}.{q(n + '_default')} "
                     f"PARTITION OF {qual(t)} DEFAULT;")
    lines += ["", "-- This month and the next three (ADR-0056); the partition job keeps the horizon."]
    lines += [f"SELECT platform.ensure_month_partitions('{qual(t)}'::regclass, 3);"
              for t in sorted(partitioned)]
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
            # **Schema-level marks, and the item schema behind an array property** (ADR-0056). A
            # table derived from `JournalEntry.lines[]` takes its marks from `JournalLine`, the
            # schema the array's items are, because that is where the contract describes the row.
            if isinstance(schema, dict):
                SCHEMA_MARKS[f"{mod}.{name}"] = {k: v for k, v in schema.items()
                                                 if str(k).startswith("x-ticvai-")}
                for prop, spec in props_of(doc, schema).items():
                    if isinstance(spec, dict) and spec.get("type") == "array":
                        ref = str((spec.get("items") or {}).get("$ref") or "")
                        if ref.startswith("#/components/schemas/"):
                            ITEM_SCHEMA[f"{mod}.{name}.{prop}"] = f"{mod}.{ref.rsplit('/', 1)[-1]}"
    return found


# `module.Schema` -> its `x-ticvai-*` keys, and `module.Schema.arrayProp` -> `module.ItemSchema`.
# Filled by `load_contract_props`, read by `table_marks`.
SCHEMA_MARKS: dict = {}
ITEM_SCHEMA: dict = {}


def table_marks(cols: dict, tables) -> dict:
    """What the contract schema a table is derived from says about the table as a whole.

    **A table is found from its columns' `source`**, which names `module.Schema.property` or
    `module.Parent.array[].property` — so a table with no persistence tag of its own
    (`platform.audit_record`) or one derived from an array (`ledger.journal_line`) resolves too.
    Returns `table -> {"append_only": column, "primary_key": [columns], "schema": name}`, with
    property names already turned into this table's column names."""
    out = {}
    for t in tables:
        votes: dict = defaultdict(int)
        for c in cols.get(t, []):
            src = str(c.get("source") or "")
            m = re.match(r"^([\w-]+)\.(\w+)\.(\w+)\[\]\.\w+$", src)
            if m:
                key = ITEM_SCHEMA.get(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")
                if key:
                    votes[key] += 1
                continue
            m = re.match(r"^([\w-]+)\.(\w+)\.\w+$", src)
            if m:
                votes[f"{m.group(1)}.{m.group(2)}"] += 1
        if not votes:
            continue
        schema = max(sorted(votes), key=lambda k: votes[k])
        marks = SCHEMA_MARKS.get(schema) or {}

        def column_of(prop):
            for c in cols.get(t, []):
                if str(c.get("source") or "").rsplit(".", 1)[-1] == prop:
                    return c["column"]
            return None

        entry = {"schema": schema}
        ao = marks.get("x-ticvai-append-only")
        if isinstance(ao, str) and ao.strip():
            entry["append_only"] = column_of(ao.strip()) or f"?{ao.strip()}"
        pk = marks.get("x-ticvai-primary-key")
        if isinstance(pk, list) and pk:
            entry["primary_key"] = [column_of(str(p)) or f"?{p}" for p in pk]
        if len(entry) > 1:
            out[t] = entry
    return out


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



# `table -> [columns]` from `x-ticvai-primary-key`, filled in `main` before any key is asked for.
DECLARED_PK: dict = {}


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
    # **A key the contract names wins** (`x-ticvai-primary-key`, ADR-0058). One column is the key a
    # foreign key can point at; several (`kernel.inbox`'s `(consumer, event_id)`) are a key nothing
    # references by a single column, so there is no single answer to give.
    declared = DECLARED_PK.get(table)
    if declared:
        return declared[0] if len(declared) == 1 else None
    if "id" in names:
        return "id"
    stem = table.split(".", 1)[1]
    for cand in (f"{stem}_id", f"{stem.rstrip('s')}_id", f"{stem}_code"):
        if cand in names:
            return cand
    if len(names) == 1:
        return names[0]
    return None


def frozen_mode(files: dict, tag: str, commit: str, apply: bool) -> None:
    """After r1: leave every baseline `.sql` file as it is and write the difference as a forward migration.

    **The baseline is read from the tag, not from disk**, so a baseline file somebody edited by hand is
    not mistaken for the release (check-migration-freeze.py fails on that edit separately). The old side
    of the comparison is the baseline at the tag plus every forward migration already in
    `backend/<area>/`; the new side is what this run generated. Additive changes go into
    `backend/<area>/V<nnnn>__after_<tag>_<yyyymmdd>.sql`, one number for the run, shared by both
    databases (each keeps its own `platform.schema_version`). **Numbering starts at V0100** so it can
    never meet the V0001-V0034 names handoff/service-docs/backend/MIGRATIONS.md plans for the baseline.

    Everything else goes to handoff/migration-review.md for a person. Scripts (`*.sh`) are not
    migrations and are still written."""
    import datetime as _dt
    stamp = _dt.date.today().strftime("%Y%m%d")
    baseline = f"{tag} ({commit[:7]})"
    existing = sorted(p for d in (CONTROL, "tenant") for p in (OUT / d).glob("V*.sql")
                      if FORWARD_FILE.match(p.name))
    version_n = max([int(FORWARD_FILE.match(p.name).group(1)) + 1 for p in existing] + [FORWARD_FIRST])
    version = f"V{version_n:04d}"
    safe_tag = re.sub(r"[^\w]+", "_", tag).strip("_") or "baseline"

    plans, extra = [], []
    for area_dir in (CONTROL, "tenant"):
        old, new = ddl_forward.Model(), ddl_forward.Model()
        for path in sorted(ls_tree(commit, f"backend/{area_dir}")):
            name = path.rsplit("/", 1)[-1]
            if path.endswith(".sql") and not FORWARD_FILE.match(name):
                old.add_file((show(commit, path) or b"").decode("utf-8"))
        for fwd in sorted((OUT / area_dir).glob("V*.sql"), key=lambda p: int(FORWARD_FILE.match(p.name).group(1))
                          if FORWARD_FILE.match(p.name) else 0):
            if FORWARD_FILE.match(fwd.name):
                text = fwd.read_text(encoding="utf-8")
                old.apply_forward(re.split(r"^-- =+\n-- ROLLBACK\b", text, maxsplit=1, flags=re.M)[0])
        for name in sorted(n for n in files if n.startswith(area_dir + "/") and n.endswith(".sql")):
            new.add_file(files[name])
        plans.append(ddl_forward.diff(area_dir, old, new))
    # **Root-level files are documentation of references that are not constraints** (990): nothing
    # applies them, so a change is listed rather than migrated.
    for name in sorted(n for n in files if "/" not in n and n.endswith(".sql")):
        was = show(commit, f"backend/{name}")
        if was is not None and was.decode("utf-8").replace("\r\n", "\n") != files[name]:
            extra.append(("both", "file changed", name, "the generator would write it differently",
                          "not applied anywhere: bring the application rules it documents up to date by hand"))

    written = []
    for p in plans:
        if not p.statements:
            continue
        dest = OUT / p.area / f"{version}__after_{safe_tag}_{stamp}.sql"
        written.append((dest, p))
        if apply:
            dest.write_text(ddl_forward.render(p, version, baseline, stamp), encoding="utf-8")
    review = ddl_forward.render_review(plans, baseline, stamp, extra)
    if apply:
        for name, text in files.items():
            if name.endswith(".sh"):
                dest = OUT / name
                dest.write_text(text, encoding="utf-8")
                dest.chmod(0o755)
        REVIEW.write_text(review, encoding="utf-8")

    n_review = sum(len(p.review) for p in plans) + len(extra)
    print(f"  FROZEN at {baseline}: the baseline files under backend/ are not rewritten")
    for dest, p in written:
        c = p.counts
        print(f"  forward migration {dest.relative_to(ROOT).as_posix()}: {c['tables']} table(s), "
              f"{c['columns']} column(s), {c['indexes']} index(es), {c['other']} other"
              + ("" if apply else " (not written, pass --apply)"))
    if not written:
        print("  no additive change since the baseline and the forward migrations; nothing to write")
    print(f"  {n_review} change(s) not generated, for a person: {REVIEW.relative_to(ROOT).as_posix()}"
          + ("" if apply else " (not written, pass --apply)"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    # **Frozen mode** (plan item 1C, C3): once the tag r1 exists the baseline files are never rewritten.
    # --baseline names another commit-ish, for testing a freeze without creating the tag.
    ap.add_argument("--baseline", default=None, help="freeze against this commit-ish (default: the tag r1)")
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
    refused = sorted(t for t in real if not VALID_TABLE.match(t))
    real -= set(refused)
    for t in refused:
        print(f"  ! refused a table whose name is not <schema>.<table>: {t!r}")
    # ...and every column whose only job was to point at one (`attributes_id`, `booked_window_id`).
    for t in list(cols):
        cols[t] = [c for c in cols[t] if not (
            c.get("references") and "." in str(c["references"]) and ":" not in str(c["references"])
            and not VALID_TABLE.match(str(c["references"])))]

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
    no_unique: list = []
    n_uniq = 0
    # A table's NOT NULL declared references inside its own database: `(column, parent, key)`.
    # Row-level security uses them to protect a child through the row that owns it.
    owners: dict[str, list] = defaultdict(list)
    contract_props = load_contract_props()
    # **A uniqueness marker on `Create<X>Request` or `Update<X>Request` speaks for `<X>`.**
    # The contracts state a code's uniqueness where a developer writes one -- on the create
    # request -- but a column's `source` names the persisted schema, so the marker would be
    # invisible here unless the persisted schema happens to allOf-include its request (as
    # maintenance.AssetDetail does). Only the marker is carried across, and never over one the
    # persisted schema declares itself.
    for key, spec in list(contract_props.items()):
        lvl = (spec or {}).get("x-ticvai-unique")
        if not lvl:
            continue
        mreq = re.match(r"^([\w-]+)\.(?:Create|Update)(\w+)Request\.(\w+)$", key)
        if not mreq:
            continue
        tgt = f"{mreq.group(1)}.{mreq.group(2)}.{mreq.group(3)}"
        if tgt in contract_props and "x-ticvai-unique" not in contract_props[tgt]:
            contract_props[tgt] = {**contract_props[tgt], "x-ticvai-unique": lvl}

    # ---- ADR-0056 and ADR-0058, accepted 30 September ---------------------------------------
    # **What the contract schema says about a table as a whole**: a named key
    # (`x-ticvai-primary-key`) and whether its rows are only ever appended
    # (`x-ticvai-append-only: <time property>`).
    marks = table_marks(cols, real)
    DECLARED_PK.clear()
    DECLARED_PK.update({t: m["primary_key"] for t, m in marks.items()
                        if m.get("primary_key") and not any(c.startswith("?")
                                                            for c in m["primary_key"])})

    # **One id type** (ADR-0056 section 1). The package held text and uuid keys side by side, so
    # `platform.outbox.aggregate_id` could not hold an order id and 285 references joined a text
    # column to a uuid one. **Every key named `id` or `*_id` is `uuid`, and every reference to one
    # is too** — new ids are UUIDv7. A key that is a human code (`games.card.card_code`) is not an
    # id and stays text: a person types it, and ADR-0056 keeps human codes apart from ids.
    #
    # A declared reference takes its target key's type, because Postgres refuses a foreign key
    # between two types. A convention takes it only where the target's key was converted here —
    # it held the same text as that key until today — and only when its name does not say it
    # holds somebody else's identifier (`provider_*`, `external_*`, `partner_*`).
    TEXTY = {"text", "jsonb", "char(26)", "varchar"}

    def id_like(c: str) -> bool:
        return c == "id" or c.endswith("_id")

    key_type_before: dict = {}
    for t in real:
        k = key_of(t, cols)
        if k:
            spec = next((c for c in cols[t] if c["column"] == k), {})
            key_type_before[t] = pg_type(spec.get("type"))
    converted_keys = {t for t, ty in key_type_before.items()
                      if ty in TEXTY and id_like(key_of(t, cols))}

    def key_type(t: str) -> str | None:
        if t not in key_type_before:
            return None
        return "uuid" if t in converted_keys else key_type_before[t]

    EXTERNAL = ("provider_", "external_", "partner_")

    def id_type(t: str, c: dict, typ: str) -> str:
        """The column's type once ADR-0056's one-id-type rule has been applied."""
        col = c["column"]
        if typ not in TEXTY:
            return typ
        if t in converted_keys and col == key_of(t, cols):
            return "uuid"
        if col in (DECLARED_PK.get(t) or []) and id_like(col):
            return "uuid"
        ref = c.get("references")
        if not ref or ref not in real or key_type(ref) != "uuid":
            return typ
        if c.get("enforced") == "yes":
            return "uuid"
        if ref in converted_keys and id_like(col) and not col.startswith(EXTERNAL):
            return "uuid"
        return typ

    # **Which tables partition by month** (ADR-0056 section 2): append-only in the contract, with
    # the time column present, and nothing pointing at them. The last condition is checked rather
    # than assumed, because a foreign key into a partitioned table would have to carry the time
    # column, and that is a different design.
    inbound: dict = defaultdict(set)
    for t in real:
        for c in cols[t]:
            ref = c.get("references")
            if (ref in real and c.get("enforced") == "yes" and key_of(ref, cols)
                    and area(t.split(".")[0]) == area(ref.split(".")[0])):
                inbound[ref].add(f"{t}.{c['column']}")
    partitioned: dict = {}
    declined: list = []
    for t, m in sorted(marks.items()):
        col = m.get("append_only")
        if not col:
            continue
        if col.startswith("?"):
            declined.append((t, f"the contract names {col[1:]}, which is not a column of the table"))
        elif area(t.split(".")[0]) != "tenant":
            declined.append((t, "not in the tenant template"))
        elif inbound.get(t):
            declined.append((t, "referenced by " + ", ".join(sorted(inbound[t]))))
        else:
            partitioned[t] = col

    # **Composite keys where venue_id already exists** (ADR-0056 section 3). A declared reference
    # between two tables that both carry a NOT NULL `venue_id` becomes `(venue_id, <column>) ->
    # parent (venue_id, <key>)`, so a row can only point at a parent in its own venue. The parent
    # gains `UNIQUE (venue_id, <key>)`; no table gains a column.
    def venue_nn(t: str) -> bool:
        return any(c["column"] == "venue_id" and c.get("required") == "yes" for c in cols.get(t, []))

    composite_parents: set = set()
    n_composite = 0
    n_id_converted = 0

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
            # **A partitioned table's key carries its partition column** (Postgres requires it), and a
            # key the contract names with several columns is a table constraint rather than a column's.
            part_col = partitioned.get(t)
            declared_pk = DECLARED_PK.get(t)
            inline_pk = not (part_col or (declared_pk and len(declared_pk) > 1))
            pk_cols = list(declared_pk or ([tkey] if tkey else []))
            if part_col and part_col not in pk_cols:
                pk_cols.append(part_col)
            for c in cols[t]:
                col = c["column"]
                # A column that exists only to point at a refused pseudo-table (`attributes_id`
                # -> `embedded as ...`, SD-007) is not a column either.
                _ref = c.get("references")
                if (_ref and "." in str(_ref) and ":" not in str(_ref)
                        and not VALID_TABLE.match(str(_ref))):
                    continue
                typ = pg_type(c.get("type"))
                one_type = id_type(t, c, typ)
                if one_type != typ:
                    n_id_converted += 1
                    typ = one_type
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
                if col == "scope_path" or col == part_col:
                    nn = " NOT NULL"
                pk = " PRIMARY KEY" if inline_pk and col == tkey else ""
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
                        # **Composite where both ends already carry a NOT NULL venue_id** (ADR-0056
                        # section 3): the child cannot point at a parent in another venue.
                        if (col != "venue_id" and ref != t and tgt_key != "venue_id"
                                and area(schema) == "tenant" and area(tgt_s) == "tenant"
                                and venue_nn(t) and venue_nn(ref)):
                            stmt = (f"ALTER TABLE {q(schema)}.{q(short)} ADD CONSTRAINT "
                                    f"{obj_name(short, 'venue_id', col, suffix='fkey')} FOREIGN KEY "
                                    f"(venue_id, {q(col)}) REFERENCES {q(tgt_s)}.{q(tgt_t)}"
                                    f"(venue_id, {q(tgt_key)});")
                            composite_parents.add(ref)
                            n_composite += 1
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
            # **The relay's queue is the unpublished rows** (system-design review SD-030, 29 September).
            # Its only index was the GiST one on `scope_path`, so every poll scanned the table.
            # ADR-0058: each poll is `WHERE published_at IS NULL ORDER BY created_at, id ... FOR UPDATE
            # SKIP LOCKED`, so the index is on both, and holds only the rows still to publish.
            if t == "platform.outbox" and {"published_at", "created_at"} <= set(names):
                idx_lines.append((schema,
                    "-- the relay polls unpublished rows oldest first (SD-030, ADR-0058)\n"
                    "CREATE INDEX IF NOT EXISTS outbox_unpublished_idx ON platform.outbox (created_at, id) "
                    "WHERE published_at IS NULL;"))
                n_idx += 1
            # **The scope tree's own path, GiST-indexed** as 001-extensions says it is: every venue
            # policy resolves a venue through it with `<@`.
            if t == SCOPE_TABLE and "path" in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, 'path')} "
                    f"ON {q(schema)}.{q(short)} USING gist (path);"))
                n_idx += 1
            # **A second visibility path is indexed like the first** -- the shared policy tests it
            # on every read.
            second = SHARED_SCOPE.get(t)
            if second and second in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, second)} "
                    f"ON {q(schema)}.{q(short)} USING gist ({q(second)});"))
                n_idx += 1

            # **Uniqueness the contract marks, as a unique index** (audit R108, 28 September).
            # `x-ticvai-unique: tenant` is unique within the tenant database -- one tenant per
            # database (ADR-0038), so the column alone, or with `tenant_id` where a table carries
            # one. `venue` is unique per venue: with `venue_id`, else with `scope_path` (a venue's
            # rows sit at its path). A nullable column gets a partial index, so rows without a
            # value never collide. Named `<table>_<columns>_uniq` (naming-and-style 6.1).
            for c in cols[t]:
                col = c["column"]
                level = contract_props.get(str(c.get("source") or ""), {}).get("x-ticvai-unique")
                if not level:
                    continue
                if level == "tenant":
                    lead = ["tenant_id"] if "tenant_id" in names else []
                elif level == "venue":
                    lead = (["venue_id"] if "venue_id" in names
                            else ["scope_path"] if "scope_path" in names else None)
                else:
                    lead = None
                if lead is None:
                    no_unique.append(f"{t}.{col} (x-ticvai-unique: {level}): "
                                     + ("no venue_id or scope_path to key it by"
                                        if level == "venue" else "not a recognised level"))
                    continue
                keycols = lead + [col]
                # A unique index on a partitioned table must include the partition column.
                if part_col and part_col not in keycols:
                    keycols.append(part_col)
                where = "" if c.get("required") == "yes" else f" WHERE {q(col)} IS NOT NULL"
                uname = obj_name(short, *keycols, suffix="uniq")
                idx_lines.append((schema,
                    f"-- unique per {level} (x-ticvai-unique): {t}.{col}\n"
                    f"CREATE UNIQUE INDEX IF NOT EXISTS {uname} ON {q(schema)}.{q(short)} "
                    f"({', '.join(q(k) for k in keycols)}){where};"))
                n_uniq += 1

            if not inline_pk and pk_cols:
                body.append(f"    CONSTRAINT {obj_name(short, suffix='pkey')} PRIMARY KEY "
                            f"({', '.join(q(k) for k in pk_cols)})")
            out.append(",\n".join(body))
            # ADR-0056: range-partitioned by month; the partitions are in 930-partitioning.sql.
            out.append(f") PARTITION BY RANGE ({q(part_col)});" if part_col else ");")
            out.append("")
            n_tables += 1
        files[f"{area(schema)}/010-{schema}.sql"] = "\n".join(out) + "\n"

    for db in (CONTROL, "tenant"):
        mine = sorted(line for s, line in fk_lines if area(s) == db)
        # **The parents of a composite key first** (ADR-0056): a foreign key on `(venue_id, x)`
        # needs a unique constraint on the same pair in the parent before it can be created.
        uniq = sorted(
            f"ALTER TABLE {q(p.split('.')[0])}.{q(p.split('.')[1])} ADD CONSTRAINT "
            f"{obj_name(p.split('.')[1], 'venue_id', key_of(p, cols), suffix='uniq')} "
            f"UNIQUE (venue_id, {q(key_of(p, cols))});"
            for p in composite_parents if area(p.split(".")[0]) == db)
        if uniq:
            mine = (["-- Parents of a composite venue key (ADR-0056): UNIQUE (venue_id, <key>).",
                     "-- A child and its parent that both carry a NOT NULL venue_id are joined on "
                     "both columns,", "-- so a row cannot point at a parent in another venue."]
                    + uniq + ["", "-- The references."] + mine)
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
    # A shared-scope table is honoured only when both of its paths exist; a declared pair whose
    # second column has not reached the schema reference yet is reported, not silently dropped.
    shared_scope = {t: c for t, c in SHARED_SCOPE.items()
                    if t in scoped and any(x["column"] == c for x in cols[t])}
    for t, c in sorted(SHARED_SCOPE.items()):
        if t not in shared_scope:
            print(f"  shared scope declared but not applied: {t}.{c} is not in the schema "
                  "reference; the table keeps its single-path policy")
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

    n_subject_rls, n_tenant_rls = [0], [0]
    unscoped_all = [t for t in sorted(real)
                    if t not in protected and t not in venue_only and t != SCOPE_TABLE]
    for db in ("tenant", CONTROL):
        mine = [t for t in scoped if area(t.split(".")[0]) == db]
        vmine = [t for t in venue_only if area(t.split(".")[0]) == db]
        pmine = [p for p in by_parent if area(p[0].split(".")[0]) == db]
        umine = [(t, why_unscoped(t)) for t in unscoped_all if area(t.split(".")[0]) == db]
        smine, tmine = [], []
        if db == "tenant" and SCOPE_TABLE in real:
            for t, why in umine:
                if any(c["column"] == "subject_id" for c in cols[t]):
                    smine.append((t, why))
                else:
                    tmine.append((t, why))
            umine = []
            n_subject_rls[0] += len(smine)
            n_tenant_rls[0] += len(tmine)
        total = len(by_schema.get(CONTROL) or []) if db == CONTROL else n_tenant_tables
        files[f"{db}/920-row-level-security.sql"] = rls_file(
            db, mine, vmine, pmine, umine, total,
            has_scope_table=(SCOPE_TABLE in real and db == "tenant"),
            shared={t: c for t, c in shared_scope.items() if t in mine},
            by_subject=smine, tenant_only=tmine)

    # **Range partitioning by month** (ADR-0056). The tables declare `PARTITION BY RANGE` where they
    # are created; this file holds each one's DEFAULT partition and the months ahead.
    files["tenant/930-partitioning.sql"] = partition_file(partitioned, declined)

    files["provision-tenant.sh"] = PROVISION

    # **The compose entry point.** provision-tenant.sh takes one tenant; a cell has several, and
    # the initdb pass is where a container gets them. Kept separate so the per-tenant script stays
    # usable by hand and by the control plane.
    files["initdb-provision.sh"] = INITDB_PROVISION

    frozen_at = baseline_commit(a.baseline)
    if frozen_at:
        frozen_mode(files, a.baseline or "r1", frozen_at, a.apply)
    elif a.apply:
        # **The flat layout is removed, not left beside the new one.** The deploy configs mount
        # `backend/<area>` into initdb, and a stale `backend/010-orders.sql` sitting next to
        # `backend/tenant/010-orders.sql` is two answers to what a tenant database contains —
        # which is the failure this package has already had once, in the mirrors.
        OUT.mkdir(exist_ok=True)
        for stale in sorted(OUT.glob("0*.sql")) + sorted(OUT.glob("9*.sql")):
            if stale.name not in files:
                stale.unlink()
        # **A per-schema file this run did not write is a schema that no longer exists** (SD-007, 29
        # September): `tenant/010-embedded as attributes (jsonb) on orders.sql` outlived the fix that
        # stopped generating it, and initdb would still have applied it.
        for area_dir in (CONTROL, "tenant"):
            for stale in sorted((OUT / area_dir).glob("*.sql")):
                # A forward migration is never generated in this branch and never removed by it.
                if FORWARD_FILE.match(stale.name):
                    continue
                if f"{area_dir}/{stale.name}" not in files:
                    print(f"  removed stale {area_dir}/{stale.name}")
                    stale.unlink()
        for name, text in files.items():
            dest = OUT / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text, encoding="utf-8")
            if dest.suffix == ".sh":
                dest.chmod(0o755)

    print(f"  {n_tables} tables · {n_cols} columns · {n_fk} foreign keys · {n_idx} indexes · "
          f"{n_chk} checks · {n_def} defaults · {n_uniq} unique indexes")
    if no_unique:
        print(f"  {len(no_unique)} uniqueness rule(s) the contract marks but the DDL cannot key:")
        for u in no_unique:
            print(f"     {u}")
    print(f"  ADR-0056: {n_id_converted} id column(s) made uuid ({len(converted_keys)} keys) · "
          f"{len(partitioned)} table(s) range-partitioned by month · {n_composite} composite venue "
          f"foreign key(s) onto {len(composite_parents)} parent(s)")
    for t, why in declined:
        print(f"     append-only but not partitioned: {t} -- {why}")
    print(f"  row-level security: {len(scoped)} by scope_path · {len(venue_only)} carry venue_id · "
          f"{len(by_parent)} through their owner · {n_subject_rls[0]} by subject · "
          f"{n_tenant_rls[0]} tenant root only · "
          f"{len(unscoped_all) - n_subject_rls[0] - n_tenant_rls[0]} with no policy")
    print(f"  {len(by_schema.get(CONTROL) or [])} control tables · "
          f"{n_tenant_tables} tenant tables in {len(tenant_schemas)} schemas")
    if n_xdb:
        print(f"  {n_xdb} reference(s) cross the control/tenant boundary and are no longer "
              "constraints")
    if unkeyed:
        print(f"  {len(unkeyed)} declared reference(s) point at a table with no addressable key:")
        for u in unkeyed[:8]:
            print(f"     {u}")
    print(f"  {len(files)} files" + (" generated; baseline frozen, see above" if frozen_at
                                      else "" if a.apply else " — nothing written, pass --apply"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
