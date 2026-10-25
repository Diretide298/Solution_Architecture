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
28 September). A contract schema's `x-ticvai-unique-together: [[a, b, ...]]` is a unique index over
several columns, each named by property or by column (CHG-R6-006); with `x-ticvai-unique-nulls: not-distinct` on
the schema a null member still collides (`NULLS NOT DISTINCT`, CHG-MKT-002). **A text member of either is
indexed as `lower(column)`**, so a code is unique whatever its case, as common.yaml says; an opaque
external id marked `x-ticvai-unique-compare: exact` is not (CHG-GEN-001). `x-ticvai-required-when:
{prop: {other: value}}` is a table CHECK that the column is set on rows where `other` is `value`
(CHG-TEN-001: a product tile names its variant). Uniqueness and immutability rules
the contracts state only in prose are not -- there is nothing machine-readable to derive them from.
**A storage-only column carries its own `enum`** (and `maxLength`, `default`) on its schema-reference
record, and gets the same CHECK (CHG-R6-001).

**Row-level security, by rule** (920): `scope_path`, else `venue_id`, else through the NOT NULL declared
reference that owns the row (`ROW_OWNER` decides where two could), else by subject or at the tenant
root -- except an `APPEND_AUDIT` trail, which any grant appends to and only the tenant root reads
(CHG-R6-002). A contract schema marked `x-ticvai-rls: read-beneath` (rows readable by grants beneath their
`scope_path` too) or `grant-holder-read` (any staff grant reads) keeps its base rule for writes, and a child that
follows it through the parent rule follows it for reading only (CHG-GEN-005, `RLS_MARKS`, `SPLIT_CHILDREN`).
**A schema marked `x-ticvai-scope: none` takes no scope** (CHG-R9MIG-001, ADAM CR-166 as the lead ruled it, 21 October
2026): no `scope_path` and no scope policy. Frozen mode removes what a forward migration gave such a table, guarded
(`DESCOPED`, ddl_forward.descope_block).

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
# baseline's 930 file. A letter after the number (`V0103a`) is a file that has to run between two frozen ones: it
# sorts after `V0103__` (`_` < `a`) and before `V0104` by name, the order SqlMigrationRunner applies (R8-MIG-001).
FORWARD_FILE = re.compile(r"^V(\d+)[a-z]?__[\w.-]+\.sql$")
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

# 2b. The root of the scope tree (ADAM CR-163, 18 October 2026; CHG-CRA-005). The cell creates the
#     tenant's `level` tenant node here, and its path is recorded in control.cell_tenant below and
#     never changes: the migrator and the fan-out read it there. The label is the slug made a valid
#     ltree label (lower case, every other character an underscore), written once; nothing derives it
#     again from control.tenant.code, whose pattern allows hyphens a scope label does not.
#     platform.scope forces row security, so the insert runs in a transaction that grants the session the root
#     path first (SET LOCAL ticvai.scope_paths); without it only a superuser could write the row, and on a
#     managed server provisioning would stop after createdb.
ROOT_PATH="t_$(printf '%s' "$SLUG" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_' '_')"
psql -v ON_ERROR_STOP=1 -d "$SLUG" <<SQL >/dev/null
  BEGIN;
  SET LOCAL ticvai.scope_paths = '$ROOT_PATH';
  INSERT INTO platform.scope (id, level, parent_id, path, code, name, is_active)
  VALUES (gen_random_uuid(), 'tenant', NULL, '$ROOT_PATH', '${ROOT_PATH#t_}', '$SLUG', true);
  COMMIT;
SQL

# 3. The row. **A database with no row in control.cell_tenant is a database nothing knows
#    about** - it will not be migrated, backed up or billed, and it will be found by somebody
#    reading pg_database rather than by the control plane.
if [ -n "$TENANT_ID" ]; then
  psql -v ON_ERROR_STOP=1 -d "$CONTROL_DB" <<SQL >/dev/null
    INSERT INTO control.cell_tenant (id, cell_id, tenant_id, database_name, status,
                                     provisioned_at, root_scope_path)
    SELECT gen_random_uuid(), c.id, '$TENANT_ID', '$SLUG', 'live', now(), '$ROOT_PATH'
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

# **Which reference owns the row, where several could** (CHG-R6-005, ADAM CR-009, 12 October 2026). A table
# with two NOT NULL declared references to protected tables gets no parent policy: which of them owns the
# row is a modelling decision (see the owner rounds in `main`), and until somebody makes it the table sits
# at the tenant root. Each entry here is that decision, made. `catalogue.product_media` is a product's
# photo (the rows of `Product.media[]`, so `product_id` is its parent key); `asset_id -> assets.media_asset`
# names what the photo shows and does not own it. `inventory.quotation_line` and `reporting.dashboard_tile`
# had the same shape (CHG-R6-013, 12 October 2026): a quotation's line is the rows of `Quotation.lines[]`
# (`quotation_id`), and `item_id -> inventory.inventory_item` names what is quoted; a dashboard's tile is
# the rows of `Dashboard.tiles[]` (`dashboard_id`), and `report_id -> reporting.report_definition` names
# what the tile shows. Each follows its parent.
ROW_OWNER = {
    # CHG-R10ORD-014 (ADAM CR-208, 25 October 2026): a refund's line and payment rows are the refund's. Each has a
    # second protected candidate (`order_line_id -> orders.order_line`, `payment_id -> orders.payment`), which names
    # what the refund took from; the payment rows fell to the tenant root ("several protected owners").
    "orders.refund_line": "refund_id",            # CHG-R10ORD-014 (CR-208)
    "orders.refund_payment": "refund_id",         # CHG-R10ORD-014 (CR-208)
    "catalogue.product_media": "product_id",   # CHG-R6-005 (CR-009)
    "inventory.quotation_line": "quotation_id",   # CHG-R6-013
    "reporting.dashboard_tile": "dashboard_id",   # CHG-R6-013
    # CHG-R6-015 (ADAM CR-013): declaring `location_id -> inventory.location` gave these a second protected
    # owner. A stock row follows its inventory item, as the movement did at r1 (and the serialised item and the
    # count line do); a goods receipt follows its purchase order, as at r1.
    "inventory.movement": "item_id",              # CHG-R6-015
    "inventory.stock_earmark": "item_id",         # CHG-R6-015
    "inventory.goods_receipt": "purchase_order_id",   # CHG-R6-015
    # CHG-GEN-007 (ADAM CR-071, 14 October 2026): a till sale belongs to the outlet that rang it up. With two protected
    # owners (`order_id -> orders.sales_order`, `outlet_id -> platform.outlet`) it fell to the subject rule, and its
    # lines, returns and return lines to the tenant root ("its owner has no policy"), so a cashier could write a sale
    # and none of its lines, and no venue role could record a return. Following the outlet, the sale is the venue's,
    # and sale_line, return and return_line follow it by their NOT NULL keys.
    "retail.sale": "outlet_id",                  # CHG-GEN-007 (CR-071)
    # CHG-DDL-004 (ADAM CR-069, 14 October 2026): declaring the Sprint 1 modules' keys gave these a second
    # candidate. A placed resource is drawn on its map (the rows a map version publishes), and the resource it
    # places names what is drawn: it follows the map, as map_version now does. A payment token is the guest's
    # (subject policy, as at r1); `provider_id` names who issued it and must not make it the provider's row.
    "venuemap.placed_resource": "map_id",         # CHG-DDL-004
    "payments.token": "subject_id",               # CHG-DDL-004: no protected owner, so the subject rule applies
    # CHG-MOD-007 (MOD audit, 14 October 2026): giving fnb.dining_table a scope_path gave a table visit and a table
    # session a second protected owner (`table_id`). They stay the outlet's, as at r1: the table names where the
    # party sits, the outlet owns the service.
    "fnb.table_visit": "outlet_id",               # CHG-MOD-007
    "fnb.table_session": "outlet_id",             # CHG-MOD-007
    # CHG-STO-001 (Block A storage audit, 14 October 2026): declaring every NOT NULL key (SP-KEY-UNDECLARED) gave these
    # a second protected candidate, and the rule picked the one protected first, which is not the row's owner: a line,
    # a cell, a point or an option is its parent's (the table it is the rows of); the other key names what it is about.
    "access.entry_rule_point": "admission_rules_id",          # a rule's points; the access point is where
    "assets.media_collection_member": "collection_id",        # a collection's member rows; the asset is what is in it
    "fnb.menu_item": "menu_section_id",                       # CHG-STO-004: the section's item; the variant is reported as
    "fnb.menu_item_modifier": "item_id",                      # a menu item's attachment of a (tenant) modifier group
    "fnb.substitution_rule": "recipe_id",                     # a recipe's rule; the ingredients are what it swaps
    "fnb.sub_bill": "bill_split_id",                          # a split's sub-bill, as at r1; the visit is what it bills
    "marketing.wishlist_item": "subject_id",                  # the guest's own row, as at r1 (the subject rule applies)
    "orders.group_ticket_allocation_line": "group_ticket_allocation_id",   # the allocation's line; the product sold
    "orders.membership_renewal": "customer_membership_id",    # the membership renewed; the template it renews to
    "orders.upgrade": "order_id",                             # the order upgraded, as at r1; the line it replaced
    "promotions.bundle_choice_option": "bundle_choice_group_id",   # the group's option, as at r1; the variant offered
    "transport.departure": "timetable_id",                    # the timetable's departure; route and performance named
    "transport.fare_matrix_cell": "fare_table_id",            # the fare table's cell; the stations are its axes
    "transport.route_stop": "route_id",                       # the route's stop, as at r1; the station is where
    # CHG-GT1-001 (r6 gate, 14 October 2026): the merged batches gave these a second protected candidate (STO declared
    # the keys, MOD scoped the tables they name), and with two owners protected in one round the table fell to the
    # tenant root, so a till could not count its own shift and a venue could not read its seat blocks (RF-TENANT-ROOT).
    "orders.cash_count_line": "shift_id",                     # the shift's count, as at r1; the box is what was counted
    "orders.deposit_box_opening_denomination": "deposit_box_id",   # the box's opening float, as at r1; the coin is what
    "seating.seat_block_item": "block_id",                    # the block's seats; the seat is what the block holds
    # CHG-MGN-001 (18 October 2026): two NOT NULL keys to one parent went to the first in alphabetical order. These two
    # the published answers decide; the others are listed for a decision (pick_owner, an "owner undecided" review row).
    "fnb.ingredient_substitute": "from_inventory_item_id",    # ADAM CR-148: the row belongs to the ingredient replaced
    "ledger.inter_entity_obligation": "from_legal_entity_id",  # ADAM CR-149: writes stay with the selling entity; the
                                                              # consuming side's read path is the row-security lane's
    # The controller's ruling of 18 October 2026 (r7 integration gate, D-FWD-OWNER): an exchange belongs to the original
    # sale it is made against; new_sale_id is the replacement sale it produces. V0104 had applied new_sale_id's parent
    # policy (the alphabet); the next forward migration re-applies it on sale_id.
    "retail.exchange": "sale_id",                             # CHG-MGN-001: the original sale, not the replacement
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

# **An audit trail every principal writes and only the tenant root reads** (CHG-R6-002, ADAM CR-005,
# 12 October 2026). `platform.audit_record` had no scope column and no protected owner, so SD-015 put it
# under `apply_tenant_rls`, whose WITH CHECK is the tenant root. Every operation that audits itself
# writes a row there in the same transaction as its business write, so a venue-scoped principal's audit
# INSERT failed the WITH CHECK and took the business write down with it: the policy meant to protect
# the trail stopped venues doing anything that is audited. Chinmay chose option B: INSERT is open to
# any connection holding a grant (a scope path set, so an unconfigured connection still writes
# nothing); SELECT, UPDATE and DELETE stay at the tenant root. One policy per command, because a single
# FOR ALL policy cannot give INSERT a different check from the rest.
#
# **Listed, not inferred.** Which tables are append-only trails that every scope writes is a decision
# per table (a venue reading another venue's trail is the risk this keeps out); the list is short and
# each entry names its change.
# `identity.authz_audit` (CHG-R6-014, 12 October 2026) is the second: every authorisation decision a
# principal's request takes is appended there, venue-scoped principals included, and it sat at the tenant
# root under `apply_tenant_rls` for the same reason `platform.audit_record` did.
# `platform.audit_read` (CHG-R8MIG-004, R8 blocker APPROVALS-TENANCY-C09) is the third: every `listAuditRecords` call,
# a venue's included, appends who read the trail; under the subject rule a row with no subject took the tenant-root
# WITH CHECK and refused every venue reader.
APPEND_AUDIT = {
    "platform.audit_record",   # CHG-R6-002 (CR-005)
    "platform.audit_read",     # CHG-R8MIG-004
    "identity.authz_audit",    # CHG-R6-014
}

# **A trail a venue reads its own part of** (CHG-R10TEN-006; ADAM CR-185, option B, decided 21 October 2026).
# listAuditRecords is a venue operation behind six venue screens, and the tenant-root read gave a venue manager
# holding AUDIT_VIEW an empty page with no error. `x-ticvai-rls: audit-read-beneath` on an APPEND_AUDIT table's
# contract schema keeps every write where CR-005 put it (any grant appends; the tenant root alone corrects or
# removes) and widens SELECT: the tenant root reads every row, and a grant reads the rows whose org-unit column
# names a platform.scope node at or beneath it. A row with no org unit (a consumer, a job, the webhook) stays the
# tenant root's. The value is the column the mark reads.
APPEND_AUDIT_MARKS = {"audit-read-beneath": "org_unit_id"}
APPEND_AUDIT_BENEATH = ("platform.tenant_root_in_scope() OR ({col} IS NOT NULL AND EXISTS (SELECT 1 FROM "
                        "platform.scope au WHERE au.id = {col} AND platform.in_scope(au.path)))")

RLS_APPEND_AUDIT = """
-- **An append-only audit trail** (CHG-R6-002): any connection holding a grant may append a row, and
-- only the tenant root may read, correct or remove one. A venue principal's business write audits itself
-- in the same transaction, and a tenant-root WITH CHECK on the INSERT failed that whole write.
CREATE OR REPLACE FUNCTION platform.apply_append_audit_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    -- the single FOR ALL policy apply_tenant_rls created, if the table had it
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', platform.rls_policy_name(target), target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_append', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_read', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_update', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_delete', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR INSERT '
                   'WITH CHECK (cardinality(platform.current_scope_paths()) > 0)', base || '_append', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (platform.tenant_root_in_scope())',
                   base || '_read', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR UPDATE USING (platform.tenant_root_in_scope()) '
                   'WITH CHECK (platform.tenant_root_in_scope())', base || '_update', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR DELETE USING (platform.tenant_root_in_scope())',
                   base || '_delete', target);
END
$$;

-- **An append-only audit trail with a wider read** (CHG-R10TEN-006, ADAM CR-185): as apply_append_audit_rls,
-- but SELECT is `read_check`, generated from the table's `x-ticvai-rls` mark (the tenant root, or a grant over
-- the row's org unit). Appending, correcting and removing are unchanged.
CREATE OR REPLACE FUNCTION platform.apply_append_audit_read_rls(target regclass, read_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    PERFORM platform.apply_append_audit_rls(target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', base || '_read', target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (%s)', base || '_read', target, read_check);
END
$$;
"""

# **A policy change reaches the databases in the forward migration** (CHG-GEN-004, 14 October 2026). CR-005's
# append-only policies were listed in handoff/migration-review.md for a person and never reached a database: the
# review row was read as done, and 920 at r5 still gave platform.audit_record the tenant-root policy. ddl_forward now
# writes a policy change on an existing table into the next forward migration as this call, then the table's
# generated helper call: every policy on the table goes, and the helper creates its own again. Idempotent, and it
# touches no row. It is needed because the helpers name their policies differently (`<t>_scope` for one policy,
# `<t>_append`, `<t>_read`... for one per command), and none drops the other's.
RLS_RESET = """
-- Drops every policy on a table, so a forward migration can apply a different generated policy to it
-- (CHG-GEN-004). Row-level security stays enabled and forced: until the next call creates a policy the
-- table returns no rows, and both run in the migration's one transaction.
CREATE OR REPLACE FUNCTION platform.drop_rls_policies(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    pol record;
BEGIN
    FOR pol IN SELECT polname FROM pg_policy WHERE polrelid = target LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON %s', pol.polname, target);
    END LOOP;
END
$$;
"""

# **Read beneath the owner, and read by any grant holder** (CHG-GEN-005, ADAM CR-076, audit R183, 14 October 2026).
# The scope rule makes a row visible at and beneath the path that owns it, and the tenant-root rule only to the root,
# so a row owned above the caller was invisible to every grant below: a venue's ROLE_MANAGE read no roles, no
# capability presets and no segregation rules (identity.role tenant root, capability_template and segregation_rule at
# the tenant's path), and no venue could read a supplier owned at tenant or an upsell rule owned at region (R183,
# "owned above, read below", decided 28 September and never built). Two schema-level marks open SELECT and leave
# every write where the base rule put it:
#
#   * `x-ticvai-rls: read-beneath` (a table with `scope_path`): a row is readable at and beneath its path, as
#     before, and also by a grant beneath it, `scope_path @> ANY (current_scope_paths())`;
#   * `x-ticvai-rls: grant-holder-read`: any staff connection holding a grant (scope paths set, no guest subject)
#     may read every row.
#
# One policy per command, as the append-only trail has, because one FOR ALL policy cannot give SELECT a wider
# check than INSERT, UPDATE and DELETE. A table that follows such a row through the parent rule follows it for
# reading only: its writes need the parent's write check, so its policy is split the same way (otherwise opening
# a parent's SELECT would open its children's writes, since the parent rule's WITH CHECK is "the parent is
# visible"). A tenant-root table is not a parent of anything, so marking one does not make tables that reference
# it follow it, except where SPLIT_CHILDREN says so.
#   * `x-ticvai-rls: own-row` (CHG-R8MIG-007; R8 blocker causes IDENTITY-C12, IDENTITY-C37, IDENTITY-C48): a row is read
#     and written by the principal or the guest it belongs to (`principal_id` = the session's `ticvai.principal_id`,
#     `subject_id` = its `ticvai.subject_id`), and by the tenant root, for a credential or second factor that is its
#     owner's alone: changeOwnCredential, the MFA tables a guest enrols in too. Not split: one check for both.
#   * `x-ticvai-rls: home-scope-write` (CHG-R8MIG-007; R8 blocker IDENTITY-C37, the lead's option A): any staff grant
#     reads, as grant-holder-read; a row is written by the tenant root or by a grant over the row's `home_scope_id`, so
#     a venue manager creates and updates the principals homed in their venue and nobody else's (CR-076's tenant-root
#     writers keep their reach).
#   * `x-ticvai-rls: subject-self` (CHG-R8MIG-007; IDENTITY-C48 option A): the guest record itself (`pii.subject`, whose
#     `id` is the subject): any staff grant reads, the guest reads and writes its own row, and the tenant root writes.
#   * `x-ticvai-rls: own-or-home-scope` (CHG-R8MIG-007; IDENTITY-C37): a principal's credential rows, read and written
#     by that principal (`ticvai.principal_id`), by a grant over the principal's home scope (createPrincipal and
#     resetPrincipalCredential at a venue) and by the tenant root.
#   * `x-ticvai-rls: signed-in-read` (CHG-R8MIG-011; the storage-sat lane's request 6, ORDERS-MONEY-C27 and C33): any
#     signed-in caller of the tenant, staff or guest, reads every row; writes keep the base rule. For rows that are not
#     personal or whose secret is the key itself: badge definitions, a gift card read by its code.
#   * `x-ticvai-rls: scope-or-subject` (CHG-R8MIG-021; R8 blocker IDENTITY-C42 and C48): a scoped row a guest is party
#     to. Staff read and write by `scope_path`, as the scope rule; a guest reads a row naming its subject in
#     `subject_id`, `over_subject_id` or `granted_by_subject_id`, and writes one whose `over_subject_id` (else
#     `subject_id`) is its own: the account holder grants and revokes. identity.delegated_access, guest to guest.
#   * `x-ticvai-rls: any-grant-no-delete` (CHG-R9MIG-001; ADAM CR-166 as the lead ruled it, 21 October 2026): any
#     connection holding a grant (a scope path set) reads, inserts and updates a row, and no policy lets one be deleted.
#     For a row that belongs to no scope (`x-ticvai-scope: none`): platform.outbox_sequence, the per-aggregate counter
#     every host allocates from. A deleted counter would start its aggregate's sequence again. The three policies are
#     our team's repository migration 240's (`_read`, `_append`, `_update`), made with apply_split_rls and its
#     `_delete` dropped, so no new helper function reaches a database that already has them.
#   * `x-ticvai-rls: guest-owns` (CHG-R9CR-003; ADAM CR-184, option A, decided 21 October 2026): staff and partners
#     read and write by the base rule as before (the venue, or the scope path), and a guest reads and writes the rows
#     of its own subject (`subject_id` = the session's `ticvai.subject_id`), and no other: orders.cart, so a guest
#     reaches its own cart without a grant on the venue, which would show it every cart there ("a guest token can
#     never widen to another subject", guestAuth). Its children follow it through the parent rule, split.
#   * `x-ticvai-rls: guest-reads-own` (CHG-R9CR-004; ADAM CR-191, option A, and CR-199): staff read and write by the
#     base rule, and a guest reads (never writes) the rows of its own subject, or, on a table with no `subject_id`,
#     the rows whose parent it names by a declared reference is the guest's own (`orders.order_line` and
#     `orders.order_event` through `orders.sales_order`). The scope-path rule is written in the per-statement shape of
#     our team's repository migration 225 (`scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])`,
#     evaluated once per statement on these hot tables), and the guest's subject the same way.
RLS_MARKS = ("read-beneath", "grant-holder-read", "own-row", "home-scope-write", "subject-self", "own-or-home-scope",
             "signed-in-read", "scope-or-subject", "any-grant-no-delete", "guest-owns", "guest-reads-own")
# The checks `guest-owns` and `guest-reads-own` build on, `{a}` standing for the row's alias (CHG-R9CR-003/004). The
# scope rule is migration 225's per-statement predicate (apply_statement_scope_rls in our team's repository), the
# guest's subject compared the same way, so neither calls a function per row.
STATEMENT_SCOPE = ("{a}scope_path IS NOT NULL AND {a}scope_path <@ ANY ((SELECT platform.current_scope_paths())"
                   "::ltree[])")
GUEST_SUBJECT = "{a}subject_id = (SELECT NULLIF(current_setting('ticvai.subject_id', true), '')::uuid)"

# The check apply_split_rls gets for `any-grant-no-delete`: a scope path set, the WITH CHECK the append-only trail's
# INSERT has (CHG-R6-002).
ANY_GRANT = "cardinality(platform.current_scope_paths()) > 0"

# **A child that follows a split parent which the parent rule would not otherwise pick** (the parent sits at the tenant
# root, so it is no owner). `identity.role_permission` is the rows of a role's permission set (CR-076 decision:
# "role_permission follows role via the parent rule once role has a policy"): readable where the role is, written
# only where the role may be written.
SPLIT_CHILDREN = {
    "identity.role_permission": "role_id",   # CHG-GEN-005 (CR-076)
    # a replaced hash is moved by the call that replaces the credential, at the principal's own or home scope
    "identity.principal_credential_history": "principal_credential_id",   # CHG-R8MIG-007 (IDENTITY-C37)
}

# **The same marks for a table no contract schema describes** (MOD audit, 14 October 2026, CHG-MOD-007). `pii.subject`
# and `pii.subject_contact` are storage-only (Identity's PII store), and two tables are derived from an array or a
# relationship rather than a schema of their own, so `x-ticvai-rls` has nowhere to be written. Every one is read by
# staff operations below the tenant (check-rls-scope-fit RF-TENANT-ROOT): a venue's guest lookup read no guest at all.
TABLE_RLS = {
    # a guest reads and updates its own record (CHG-R8MIG-007, IDENTITY-C48): grant-holder-read alone shut it out
    "pii.subject": "subject-self",
    "pii.subject_contact": "grant-holder-read",
    "fnb.delivery_location_outlet": "grant-holder-read",
    "whitelabel.homepage_section": "grant-holder-read",
    # The balances closeFiscalPeriod (region) reads through Wallet's periodCloseChecks (CHG-FIN-012). Batch STO declares
    # wallet_id, after which the table follows wallet.wallet (opened the same way) and this line is moot.
    "wallet.balance": "grant-holder-read",
}

RLS_SPLIT = """
-- **Read beneath the owner, read by any grant holder** (CHG-GEN-005): SELECT opened, writes unchanged.
-- A staff connection holding a grant: scope paths set and no guest subject (a guest's session names its
-- own subject and reads only its own rows).
CREATE OR REPLACE FUNCTION platform.grant_holder()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND NULLIF(current_setting('ticvai.subject_id', true), '') IS NULL;
$$;

-- True when the row sits at or above one of the granted paths: owned above, read below (audit R183).
CREATE OR REPLACE FUNCTION platform.above_scope(row_scope_path ltree)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path @> ANY (platform.current_scope_paths());
$$;

-- One policy per command: SELECT on `read_check`, INSERT, UPDATE and DELETE on `write_check`.
CREATE OR REPLACE FUNCTION platform.apply_split_rls(target regclass, read_check text, write_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    base text := (SELECT left(c.relname, 55) FROM pg_class c WHERE c.oid = target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    PERFORM platform.drop_rls_policies(target);
    EXECUTE format('CREATE POLICY %I ON %s FOR SELECT USING (%s)', base || '_read', target, read_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR INSERT WITH CHECK (%s)', base || '_append', target, write_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR UPDATE USING (%s) WITH CHECK (%s)',
                   base || '_update', target, write_check, write_check);
    EXECUTE format('CREATE POLICY %I ON %s FOR DELETE USING (%s)', base || '_delete', target, write_check);
END
$$;

-- `x-ticvai-rls: read-beneath` on a table with scope_path: read at, beneath and above a grant; write at and
-- beneath it, as apply_scope_rls does.
CREATE OR REPLACE FUNCTION platform.apply_read_beneath_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.in_scope(scope_path) OR platform.above_scope(scope_path)',
        'platform.in_scope(scope_path)');
END
$$;

-- `x-ticvai-rls: grant-holder-read`: any staff grant reads; `write_check` is the table's base rule.
CREATE OR REPLACE FUNCTION platform.apply_grant_holder_read_rls(target regclass, write_check text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target, 'platform.grant_holder()', write_check);
END
$$;

-- `x-ticvai-rls: grant-holder-read` on a table owned by subject (CHG-MOD-007): any staff grant reads and the guest
-- still reads its own rows; written only by that guest or the tenant root, as apply_subject_rls writes.
CREATE OR REPLACE FUNCTION platform.apply_grant_holder_subject_read_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)',
        'platform.subject_in_scope(subject_id)');
END
$$;

-- `x-ticvai-rls: own-row` (CHG-R8MIG-007): the row's own principal (`ticvai.principal_id`, set with the session at
-- sign-in) or guest (`ticvai.subject_id`), or the tenant root. A credential or a second factor is its owner's alone.
CREATE OR REPLACE FUNCTION platform.own_row(row_principal_id uuid, row_subject_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT (row_principal_id IS NOT NULL
            AND row_principal_id::text = NULLIF(current_setting('ticvai.principal_id', true), ''))
        OR (row_subject_id IS NOT NULL
            AND row_subject_id::text = NULLIF(current_setting('ticvai.subject_id', true), ''))
        OR platform.tenant_root_in_scope();
$$;

CREATE OR REPLACE FUNCTION platform.apply_own_row_rls(target regclass, principal_column text, subject_column text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    chk text := format('platform.own_row(%s, %s)',
                       CASE WHEN principal_column IS NULL THEN 'NULL::uuid' ELSE quote_ident(principal_column) END,
                       CASE WHEN subject_column IS NULL THEN 'NULL::uuid' ELSE quote_ident(subject_column) END);
BEGIN
    PERFORM platform.apply_split_rls(target, chk, chk);
END
$$;

-- `x-ticvai-rls: signed-in-read` (CHG-R8MIG-011): any signed-in caller of the tenant, staff (a scope path set) or a
-- guest (its subject set), reads; nobody unconfigured does.
CREATE OR REPLACE FUNCTION platform.signed_in()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
        OR NULLIF(current_setting('ticvai.subject_id', true), '') IS NOT NULL;
$$;

-- A child of a split row: read where the parent is visible, written only where the parent may be written
-- (`parent_write`, the parent's write check on the alias `parent_row`).
CREATE OR REPLACE FUNCTION platform.apply_parent_split_rls(target regclass, fk_column text, parent regclass,
                                                           parent_key text, parent_write text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    link text := format('parent_row.%I = %s.%I', parent_key, target, fk_column);
BEGIN
    PERFORM platform.apply_split_rls(target,
        format('EXISTS (SELECT 1 FROM %s parent_row WHERE %s)', parent, link),
        format('EXISTS (SELECT 1 FROM %s parent_row WHERE %s AND (%s))', parent, link, parent_write));
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
-- A parent in another deployable is asked through platform.visible_parent_ids instead (apply_parent_across_rls).
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

VISIBLE_PARENT_IDS_HEAD = """
-- **The parent rows this connection may see** (ADAM CR-108, 18 October 2026; CHG-RSF-001). A child whose parent is in
-- another deployable asks this instead of reading the parent with its host's own grants, which DB-ROLES does not give
-- (each deployable has only its own schemas). SECURITY DEFINER: it runs as its owner, and every parent forces
-- row-level security, so the parent's own policy still decides, against the caller's session settings; it returns
-- exactly the parent ids the caller would see with a grant on the parent, and nothing else.
-- **Set-based** (fix round 1, 18 October 2026, as the controller ruled): the child's policy is
-- `<fk> IN (SELECT platform.visible_parent_ids(parent))`, an uncorrelated subquery, so the parent's policy runs once
-- per query rather than once per child row. On 100,000 rows the per-row form took 10-19 s against r6's 23-58 ms; this
-- takes 12 ms. It answers only the parents listed below (static SQL, no argument reaches a statement); any other
-- raises. `for_write` applies the parent's write check where a split child needs it. Its search path is fixed;
-- `public` is on it because the ltree type and operators the scope checks use live there (001-extensions.sql), and no
-- host role may CREATE in it (DB-ROLES). Its owner and who may execute it: platform.visible_parent_ids_setup, below.
CREATE OR REPLACE FUNCTION platform.visible_parent_ids(parent regclass, for_write boolean DEFAULT false)
    RETURNS SETOF uuid
    LANGUAGE plpgsql
    STABLE
    SECURITY DEFINER
    SET search_path = pg_catalog, public, pg_temp
AS $$
BEGIN
"""

VISIBLE_PARENT_IDS_TAIL = """
    RAISE EXCEPTION 'platform.visible_parent_ids: % is not a parent a policy names', parent;
END
$$;

-- **Who owns platform.visible_parent_ids, and who may call it** (decision D5 as the lead ruled it, and fix round 1,
-- 18 October 2026; CHG-RSF-001). A SECURITY DEFINER function runs as its owner, and a superuser or a BYPASSRLS role
-- skips every policy, FORCE or not: owned by one, the function would return every parent and so show every child row.
-- In production the migration role owns it, and DB-ROLES (#27655) gives that role neither.
--   * Where its owner bypasses row-level security and the migration may create roles (a developer's or test database
--     migrated as `postgres`), it gets a dedicated owner that does not, `ticvai_parent_visible` (no login, no
--     superuser, no BYPASSRLS), with SELECT on every table a listed parent's own policy reads, up its chain (a parent
--     with a parent of its own: catalogue.performance -> catalogue.event).
--   * Where its owner bypasses row-level security and the migration may not create roles, **the migration refuses**.
--     D5 forbids refusing at run time, which would break databases migrated as postgres; those never reach here.
--   * EXECUTE is revoked from PUBLIC and granted to the deployable roles of DB-ROLES that exist (commerce, access,
--     operations, workers, ticvai_ai): a policy runs with the querying role's EXECUTE right.
-- Called by the across helpers, so every across policy applied re-checks it; it touches no row and takes no argument.
CREATE OR REPLACE FUNCTION platform.visible_parent_ids_setup()
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    fn regprocedure := 'platform.visible_parent_ids(regclass, boolean)'::regprocedure;
    owner_bypasses boolean;
    me record;
    t text;
    rel regclass;
    r text;
BEGIN
    SELECT o.rolsuper OR o.rolbypassrls INTO owner_bypasses
      FROM pg_catalog.pg_proc f JOIN pg_catalog.pg_roles o ON o.oid = f.proowner WHERE f.oid = fn;
    IF owner_bypasses THEN
        SELECT m.rolsuper, m.rolcreaterole INTO me FROM pg_catalog.pg_roles m WHERE m.rolname = current_user;
        IF me.rolsuper OR me.rolcreaterole THEN
            IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'ticvai_parent_visible') THEN
                CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
            END IF;
            IF NOT me.rolsuper THEN
                EXECUTE format('GRANT ticvai_parent_visible TO %I WITH INHERIT TRUE, SET TRUE', current_user);
            END IF;
            EXECUTE 'GRANT USAGE ON SCHEMA platform, public TO ticvai_parent_visible';
            EXECUTE 'GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA platform TO ticvai_parent_visible';
            -- ALTER ... OWNER needs CREATE on the schema for the new owner; it is taken back at once
            EXECUTE 'GRANT CREATE ON SCHEMA platform TO ticvai_parent_visible';
            ALTER FUNCTION platform.visible_parent_ids(regclass, boolean) OWNER TO ticvai_parent_visible;
            EXECUTE 'REVOKE CREATE ON SCHEMA platform FROM ticvai_parent_visible';
        ELSE
            RAISE EXCEPTION 'platform.visible_parent_ids is owned by %, which bypasses row-level security, and % may not create a role to own it instead: every child row of a parent in another deployable would be visible. Migrate as a role without BYPASSRLS (DB-ROLES), or as one that may create roles',
                (SELECT f.proowner::regrole FROM pg_catalog.pg_proc f WHERE f.oid = fn), current_user;
        END IF;
    END IF;
    IF (SELECT f.proowner::regrole::text FROM pg_catalog.pg_proc f WHERE f.oid = fn) = 'ticvai_parent_visible' THEN
        FOREACH t IN ARRAY ARRAY[{owner_reads}]::text[] LOOP
            rel := pg_catalog.to_regclass(t);
            CONTINUE WHEN rel IS NULL;
            EXECUTE format('GRANT USAGE ON SCHEMA %I TO ticvai_parent_visible',
                           (SELECT n.nspname FROM pg_catalog.pg_class c
                              JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.oid = rel));
            EXECUTE format('GRANT SELECT ON %s TO ticvai_parent_visible', rel);
        END LOOP;
    END IF;
    EXECUTE 'REVOKE EXECUTE ON FUNCTION platform.visible_parent_ids(regclass, boolean) FROM PUBLIC';
    FOREACH r IN ARRAY ARRAY['commerce', 'access', 'operations', 'workers', 'ticvai_ai'] LOOP
        IF EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = r) THEN
            EXECUTE format('GRANT EXECUTE ON FUNCTION platform.visible_parent_ids(regclass, boolean) TO %I', r);
        END IF;
    END LOOP;
END
$$;

-- **A child whose parent is in another deployable** (ADAM CR-108, 18 October 2026; CHG-RSF-001). Its host's role has
-- no grant on the parent's schema (DB-ROLES grants each deployable only its own), so r6's EXISTS on the parent failed
-- with "permission denied". The parent ids are asked of platform.visible_parent_ids, once per query, under the
-- parent's own policy. **Only these children** (decision D9 as the lead ruled it, 18 October): a child whose parent is
-- in its own deployable keeps apply_parent_rls. A chain that crosses further up (fnb.menu_item -> fnb.menu_section ->
-- fnb.menu -> platform.outlet) crosses at one table, and only that table asks the function.
CREATE OR REPLACE FUNCTION platform.apply_parent_across_rls(target regclass, fk_column text,
                                                            parent regclass, parent_key text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('%I IN (SELECT platform.visible_parent_ids(%L::regclass))', fk_column, parent::text);
BEGIN
    IF parent_key <> 'id' THEN
        RAISE EXCEPTION 'apply_parent_across_rls: % keys its parent % by %, and platform.visible_parent_ids returns a parent''s id',
            target, parent, parent_key;
    END IF;
    PERFORM platform.visible_parent_ids_setup();
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (%s) WITH CHECK (%s)',
                   policy_name, target, predicate, predicate);
END
$$;

-- The same for a child of a split parent in another deployable: read where the parent is visible, written only where
-- the parent may be written (platform.visible_parent_ids' write branch carries the parent's write check;
-- `parent_write` names the same check, kept so the call reads like apply_parent_split_rls's).
CREATE OR REPLACE FUNCTION platform.apply_parent_split_across_rls(target regclass, fk_column text, parent regclass,
                                                                  parent_key text, parent_write text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    IF parent_key <> 'id' THEN
        RAISE EXCEPTION 'apply_parent_split_across_rls: % keys its parent % by %, and platform.visible_parent_ids returns a parent''s id',
            target, parent, parent_key;
    END IF;
    PERFORM platform.visible_parent_ids_setup();
    PERFORM platform.apply_split_rls(target,
        format('%I IN (SELECT platform.visible_parent_ids(%L::regclass))', fk_column, parent::text),
        format('%I IN (SELECT platform.visible_parent_ids(%L::regclass, true))', fk_column, parent::text));
END
$$;
"""


def parents_of(by_parent: list) -> dict:
    """Each parent a parent policy names -> the write check its split children carry (on `parent_row`), or None."""
    out: dict = {}
    for t, _col, par, key, *rest in by_parent:
        if key != "id":
            raise ValueError(f"{t}: its parent {par} is keyed by {key}; platform.visible_parent_ids returns ids")
        w = rest[0] if rest else None
        if w and out.get(par) and out[par] != w:
            raise ValueError(f"{par}: two write checks for one parent ({out[par]!r}, {w!r})")
        out[par] = out.get(par) or w
    return out


TABLE_IN_CHECK = re.compile(r'FROM\s+("?[a-z_][a-z0-9_]*"?\."?[a-z_][a-z0-9_]*"?)\s+p\d+\b', re.I)


def owner_reads(parents: dict, by_parent: list) -> list:
    """Every table the function's dedicated owner must read (fix round 1, I1): each listed parent, every table up its
    own parent chain, every table a split write check names, and platform.scope, which the scope checks read."""
    up = {e[0]: e for e in by_parent}
    out, todo = {"platform.scope"}, list(parents)
    for par, w in parents.items():
        todo += [m.group(1).replace('"', "") for m in TABLE_IN_CHECK.finditer(w or "")]
    while todo:
        t = todo.pop()
        if t in out:
            continue
        out.add(t)
        e = up.get(t)
        if e:
            todo.append(e[2])
            if len(e) > 4:
                todo += [m.group(1).replace('"', "") for m in TABLE_IN_CHECK.finditer(e[4] or "")]
    return sorted(out)


def visible_parent_ids_sql(parents: dict, reads: list) -> str:
    """platform.visible_parent_ids with one branch per parent (see VISIBLE_PARENT_IDS_HEAD), then its setup and the
    two across helpers. `reads`: owner_reads()."""
    def qual(t: str) -> str:
        sch, n = t.split(".", 1)
        return f"{q(sch)}.{q(n)}"

    branches = []
    for par in sorted(parents):
        rel = qual(par)
        read = f"RETURN QUERY SELECT parent_row.id FROM {rel} parent_row;"
        if parents[par]:
            branches.append(
                f"    IF parent = '{rel}'::regclass THEN\n"
                f"        IF for_write THEN\n"
                f"            RETURN QUERY SELECT parent_row.id FROM {rel} parent_row WHERE ({parents[par]});\n"
                f"            RETURN;\n"
                f"        END IF;\n"
                f"        {read}\n"
                f"        RETURN;\n"
                f"    END IF;")
        else:
            branches.append(f"    IF parent = '{rel}'::regclass THEN\n        {read}\n        RETURN;\n    END IF;")
    tail = VISIBLE_PARENT_IDS_TAIL.replace("{owner_reads}", ", ".join(sql_literal(t) for t in reads) or "NULL")
    return VISIBLE_PARENT_IDS_HEAD + "\n".join(branches) + tail

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
             by_subject: list | None = None, tenant_only: list | None = None,
             append_audit: list | None = None, split: list | None = None, across: set | None = None) -> str:
    """The functions, then one call per table -- by `scope_path` where it has one, by `venue_id`
    where it does not, and through its owning parent where it has neither.

    `by_parent` is `(table, fk_column, parent, parent_key)`; `unscoped` is `(table, why)`;
    `shared` maps a scoped table to the second path column that also admits a caller;
    `append_audit` is `(table, why)` for an APPEND_AUDIT trail (CHG-R6-002); `split` is `(table, call, why)` for a
    table marked `x-ticvai-rls` (CHG-GEN-005), and a `by_parent` entry with a fifth member, the parent's write check,
    follows a split parent for reading only. Every parent a `by_parent` entry names gets a branch of
    platform.visible_parent_ids: those whose table is in `across` (a parent in another deployable, decision D9) are
    applied with apply_parent_across_rls / apply_parent_split_across_rls, which ask it; the rest keep r6's helpers
    (CHG-RSF-001)."""
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
    body = [head, RLS_RESET]
    by_subject = by_subject or []
    tenant_only = tenant_only or []
    append_audit = append_audit or []
    split = split or []
    across = across or set()
    if by_parent:
        body.append(RLS_PARENT)
    if any(e[0] in across for e in by_parent):
        cross = parents_of([e for e in by_parent if e[0] in across])
        body.append(visible_parent_ids_sql(cross, owner_reads(cross, by_parent)))
    if by_subject or tenant_only or append_audit:
        body.append(RLS_TENANT)
    if append_audit:
        body.append(RLS_APPEND_AUDIT)
    if split or any(len(e) > 4 for e in by_parent):
        body.append(RLS_SPLIT)
    n_venue = len(by_venue) if db == "tenant" else 0
    # **Counted, not asserted.** The line this replaced called every table with neither column
    # "reference data, a registry, or the migration log", and the audit of 26 September found
    # PII, principals and order lines among them. What is left unscoped is now listed by name with
    # the reason, so the claim can be checked rather than believed.
    body.append(
        f"-- **{total} tables: {len(scoped)} scoped by `scope_path`, {n_venue} by `venue_id`, "
        f"{len(by_parent)} through the parent that owns them, {len(by_subject)} by subject, "
        f"{len(tenant_only)} to the tenant root only, "
        + (f"{len(append_audit)} append-only audit trail(s), " if append_audit else "")
        + (f"{len(split)} read beneath their owner or by any grant holder, " if split else "")
        + f"{len(unscoped)} with no policy.**\n"
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
    if split:
        body.append("\n-- Read beneath the owner, or by any grant holder; written as the base rule says (CHG-GEN-005,\n"
                    "-- x-ticvai-rls on the contract schema).")
        body += [f"{call}  -- {why}" for t, call, why in split]
    if by_parent:
        # **In dependency order**, parents before children: a child's policy reads its parent, and
        # the parent's policy has to exist for that read to be scoped at all.
        body.append("\n-- Scoped through the parent that owns the row (a NOT NULL declared foreign key).")
        for t, col, par, key, *rest in by_parent:
            # a parent in another deployable is asked through platform.visible_parent_ids (CHG-RSF-001, decision D9)
            how = "across_" if t in across else ""
            if len(rest) >= 3:
                # under a parent a guest may read: staff read through it, a guest only its own rows (CHG-R8MIG-026)
                body.append(f"SELECT platform.apply_split_rls('{qual(t)}'::regclass, {sql_literal(rest[1])}, "
                            f"{sql_literal(rest[2])});")
            elif rest:
                # follows a split parent for reading; written where the parent may be written (CHG-GEN-005)
                body.append(f"SELECT platform.apply_parent_split_{how}rls('{qual(t)}'::regclass, '{col}', "
                            f"'{qual(par)}'::regclass, '{key}', {sql_literal(rest[0])});")
            else:
                body.append(f"SELECT platform.apply_parent_{how}rls('{qual(t)}'::regclass, '{col}', "
                            f"'{qual(par)}'::regclass, '{key}');")
    if by_subject:
        body.append("\n-- By subject (SD-015): the session's own subject, or the tenant root.")
        body += [f"SELECT platform.apply_subject_rls('{qual(t)}'::regclass);" for t, _ in by_subject]
    if tenant_only:
        body.append("\n-- Tenant root only (SD-015): no scope column and no protected owner, so visible only\n"
                    "-- to a connection holding the tenant root. `pii.*` and `payments.token` are also\n"
                    "-- reached only through their owning service's role; this policy is the floor.")
        body += [f"SELECT platform.apply_tenant_rls('{qual(t)}'::regclass);  -- was: {why}"
                 for t, why in tenant_only]
    if append_audit:
        body.append("\n-- Append-only audit trails (CHG-R6-002): any connection holding a grant appends, only the\n"
                    "-- tenant root reads, corrects or removes; a trail marked audit-read-beneath (CHG-R10TEN-006,\n"
                    "-- CR-185) is also read by a grant over the row's org unit.")
        for t, why, *col in append_audit:
            if col and col[0]:
                read = APPEND_AUDIT_BENEATH.format(col=col[0])
                body.append(f"SELECT platform.apply_append_audit_read_rls('{qual(t)}'::regclass, "
                            f"{sql_literal(read)});  -- was: {why}")
            else:
                body.append(f"SELECT platform.apply_append_audit_rls('{qual(t)}'::regclass);  -- was: {why}")
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


# The authored list of the cross-deployable grants (CHG-R6-020; `reads` since CHG-R9CR-005).
CROSS_DEPLOYABLE = ROOT / "docs" / "active" / "cross-deployable-writes.yaml"


def deployable_read_grants() -> str:
    """The `reads` of docs/active/cross-deployable-writes.yaml as guarded GRANT blocks (ADAM CR-196, CHG-R9CR-005).

    One block per table: `GRANT <privileges> ON <table> TO <reader>` when the role and the table exist. DB-ROLES makes
    the roles (`commerce`, `access`, `operations`, `workers`, `ticvai_ai`); a database without them is left alone."""
    doc = yaml.safe_load(CROSS_DEPLOYABLE.read_text(encoding="utf-8")) or {}
    out = []
    for r in doc.get("reads") or []:
        role = str(r.get("reader") or "")
        privs = ", ".join(str(p).upper() for p in r.get("privileges") or [])
        if not re.match(r"^[a-z_]+$", role) or privs not in ("SELECT",):
            print(f"  ! cross-deployable read {r.get('id')}: reader {role!r} with {privs!r} is not a role and SELECT; "
                  "no grant written")
            continue
        for t in r.get("tables") or []:
            out.append(f"-- {r.get('id')}: {role} reads {t} in process (ADR-0055 rule 4 as amended; "
                       f"{r.get('decision_ref') or ''})")
            out.append(f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = {sql_literal(role)}) AND "
                       f"to_regclass({sql_literal(t)}) IS NOT NULL THEN GRANT {privs} ON {t} TO {role}; "
                       "END IF; END $$;")
    if not out:
        return ""
    return ("\n-- **Reads granted across deployables** (docs/active/cross-deployable-writes.yaml `reads`; ADAM CR-196,\n"
            "-- CHG-R9CR-005). Row-level security still applies to every row these roles read.\n" + "\n".join(out) + "\n")


# **Ending every session of a principal, whatever venue the caller acts at** (ADAM CR-180, option A, accepted 21 October
# 2026; CHG-R10ID-006). updatePrincipal runs at venue scope, but identity.refresh_token is tenant-root and
# identity.session venue-isolated, so a venue manager's revoke updated no token and only its own venue's sessions, and
# the PATCH still answered 200. This one SECURITY DEFINER function first checks the caller may update the principal, by
# the principal's own write rule (x-ticvai-rls home-scope-write: the tenant root, or a grant over its home scope), then
# ends every live session and revokes every live refresh token of that principal. No grant or policy is widened: the
# function lifts the connection to the tenant root for its own two statements only and puts the caller's scope back
# before it returns. updatePrincipal (deactivation, validTo, primaryRoleId) and forceLogout call it.
END_PRINCIPAL_SESSIONS_SQL = """
-- **identity.end_principal_sessions** (ADAM CR-180, option A; CHG-R10ID-006): ends every live session and revokes every
-- live refresh token of one principal, at every venue, once the caller is shown to be allowed to update that principal
-- (identity.principal's write rule, home-scope-write). Returns the number of sessions ended. Whatever its owner, it
-- reads and writes the two tables at the tenant root for these statements only, and restores the caller's
-- ticvai.scope_paths before returning.
CREATE OR REPLACE FUNCTION identity.end_principal_sessions(target_principal_id uuid, ended_by uuid, reason text)
    RETURNS integer
    LANGUAGE plpgsql
    VOLATILE
    SECURITY DEFINER
    SET search_path = pg_catalog, public, pg_temp
AS $$
DECLARE
    caller_paths text := current_setting('ticvai.scope_paths', true);
    root_path text;
    ended integer := 0;
BEGIN
    IF NOT (platform.tenant_root_in_scope() OR EXISTS (
            SELECT 1 FROM identity.principal hp JOIN platform.scope hs ON hs.id = hp.home_scope_id
             WHERE hp.id = target_principal_id AND platform.in_scope(hs.path))) THEN
        RAISE EXCEPTION 'identity.end_principal_sessions: the caller may not update principal %', target_principal_id
            USING ERRCODE = '42501';
    END IF;
    SELECT s.path::text INTO root_path FROM platform.scope s WHERE s.level = 'tenant' LIMIT 1;
    PERFORM set_config('ticvai.scope_paths', COALESCE(root_path, ''), true);
    UPDATE identity.session
       SET status = 'terminated', ended_at = now(), ended_by_principal_id = ended_by, end_reason = left(reason, 500)
     WHERE principal_id = target_principal_id AND status = 'active';
    GET DIAGNOSTICS ended = ROW_COUNT;
    UPDATE identity.refresh_token
       SET revoked_at = now(), revocation_reason = left(reason, 250)
     WHERE principal_id = target_principal_id AND revoked_at IS NULL;
    PERFORM set_config('ticvai.scope_paths', COALESCE(caller_paths, ''), true);
    RETURN ended;
END
$$;
"""


def exactly_one_sql(short: str, group: list) -> str:
    """`x-ticvai-exactly-one-of` (ADAM CR-158, CHG-CRA-002): the table CHECK line that exactly one column is set."""
    return (f"    CONSTRAINT {obj_name(short, *group, 'one', suffix='chk')} CHECK ("
            f"num_nonnulls({', '.join(q(k) for k in group)}) = 1)")


# **A change version every writer moves** (ADAM CR-239, option A, settled 25 October 2026; CHG-R10ORD-011). The
# property mark `x-ticvai-change-version: true` on a bigint property makes its column the row's change version: a
# per-database sequence `<table>_<column>_seq`, and a BEFORE INSERT OR UPDATE trigger that sets the column from it, so
# every operation that writes the table moves it without remembering to (access.entitlement has seventeen writers).
# A delta read ("changed after N") then has something to count. One guarded block, written as it is into a forward
# migration by tools/ddl_forward.py (CHANGE_VERSION); it does nothing where the table or the column is missing.
CHANGE_VERSION_MARK = "x-ticvai-change-version"


def change_version_sql(schema: str, short: str, table: str, col: str) -> str:
    """The sequence, the function and the trigger behind `x-ticvai-change-version` (ADAM CR-239, CHG-R10ORD-011)."""
    seq = f"{schema}.{short}_{col}_seq"
    fn = f"{schema}.{short}_{col}_set"
    trg = f"{short}_{col}_trg"
    return (f"-- change version (x-ticvai-change-version): {table}.{col}, from {seq}, set on every insert and update\n"
            f"DO $$ BEGIN IF to_regclass({sql_literal(table)}) IS NOT NULL AND EXISTS (SELECT 1 FROM "
            f"information_schema.columns WHERE table_schema = {sql_literal(schema)} AND table_name = "
            f"{sql_literal(short)} AND column_name = {sql_literal(col)}) THEN "
            f"CREATE SEQUENCE IF NOT EXISTS {seq}; "
            f"CREATE OR REPLACE FUNCTION {fn}() RETURNS trigger LANGUAGE plpgsql AS $f$ BEGIN "
            f"NEW.{col} := nextval({sql_literal(seq)}); RETURN NEW; END $f$; "
            f"DROP TRIGGER IF EXISTS {trg} ON {table}; "
            f"CREATE TRIGGER {trg} BEFORE INSERT OR UPDATE ON {table} FOR EACH ROW EXECUTE FUNCTION {fn}(); "
            "END IF; END $$;")


def index_sql(schema: str, short: str, table: str, group: list) -> str:
    """`x-ticvai-index` (ADAM CR-165, CR-166; CHG-CRA-004): a plain index over the columns the contract names."""
    return (f"-- declared index (x-ticvai-index): {table} ({', '.join(group)})\n"
            f"CREATE INDEX IF NOT EXISTS {obj_name(short, *group, suffix='idx')} ON {q(schema)}.{q(short)} "
            f"({', '.join(q(k) for k in group)});")


def unique_when_sql(schema: str, short: str, table: str, keycols: list, cond: dict, keys: list) -> str:
    """`x-ticvai-unique-when` (ADAM CR-154; CHG-CRA-004): a partial unique index. `keys` are the index's
    expressions (a text key as `lower(...)`); `cond` maps a column to the value that selects the rows, or to
    `{not: value}` for the rows whose value is anything else (CHG-R10TEN-011, ADAM CR-105: a hostname is unique among
    a tenant's claims that are not revoked, since a revoked claim is kept and the domain may be claimed again), or to
    `{in: [values]}` for the rows holding one of them (CHG-R10TEN-012, ADAM CR-106)."""
    preds = []
    for k, v in sorted(cond.items()):
        if v is True:
            preds.append(q(k))
        elif v is False:
            preds.append(f"NOT {q(k)}")
        elif isinstance(v, dict) and set(v) == {"not"}:
            preds.append(f"{q(k)} IS DISTINCT FROM {sql_literal(v['not'])}")
        elif isinstance(v, dict) and set(v) == {"in"} and isinstance(v["in"], list) and v["in"]:
            # one of several values (CHG-R10TEN-012, ADAM CR-106: one app build per platform while queued or building)
            preds.append(f"{q(k)} IN ({', '.join(sql_literal(x) for x in v['in'])})")
        else:
            preds.append(f"{q(k)} = {sql_literal(v)}")
    where = " AND ".join(preds)
    return (f"-- unique when (x-ticvai-unique-when): {table} ({', '.join(keycols)}) where {where}\n"
            f"CREATE UNIQUE INDEX IF NOT EXISTS {obj_name(short, *keycols, suffix='uniq')} "
            f"ON {q(schema)}.{q(short)} ({', '.join(keys)}) WHERE {where};")


def load_contract_props(docs: dict | None = None) -> dict:
    """`module.Schema.property` -> the contract property, with `$ref` and `allOf` followed.

    The schema reference names each column's contract `source` but does not carry its enum,
    maxLength or default, so they are read from the contracts here. `docs` (stem -> parsed contract) lets a check that
    has already read the contracts reuse them (check-ddl-conventions, CHG-MGN-001)."""
    if docs is None:
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
                retired_columns(schema)
                for prop, spec in props_of(doc, schema).items():
                    if isinstance(spec, dict) and spec.get("type") == "array":
                        ARRAY_PROPS.add(f"{mod}.{name}.{prop}")
                        ref = str((spec.get("items") or {}).get("$ref") or "")
                        if ref.startswith("#/components/schemas/"):
                            ITEM_SCHEMA[f"{mod}.{name}.{prop}"] = f"{mod}.{ref.rsplit('/', 1)[-1]}"
    return found


def retired_columns(schema: dict) -> None:
    """**The columns a contract withdraws** (`x-ticvai-retired-columns`), into RETIRED, read as derive-schema's
    `retired_of` reads them: on the schema or an `allOf` branch, beside the persistence tag; a bare name is the
    tagged table's column, `schema.table.column` a child table's (CHG-FXC-003). Frozen mode hands them to ddl_forward,
    so a retired column's row says drop it rather than "a rename or a drop: decide" (CHG-MGN-001, ADAM CR-157)."""
    branches = [schema] + [b for b in (schema.get("allOf") or []) if isinstance(b, dict)]
    tag = next((b.get("x-ticvai-persistence") for b in branches if isinstance(b.get("x-ticvai-persistence"), str)),
               None)
    table = tag.split("+")[0].strip() if tag and "." in tag and "\u2014" not in tag else None
    for b in branches:
        for rc in (b.get("x-ticvai-retired-columns") or []) if isinstance(b.get("x-ticvai-retired-columns"),
                                                                          list) else []:
            rc = str(rc)
            if rc.count(".") == 2:
                t, c = rc.rsplit(".", 1)
                RETIRED.setdefault(t, set()).add(c)
            elif table:
                RETIRED.setdefault(table, set()).add(rc)


# `module.Schema` -> its `x-ticvai-*` keys, and `module.Schema.arrayProp` -> `module.ItemSchema`.
# Filled by `load_contract_props`, read by `table_marks`. RETIRED: table -> the columns its contract withdraws.
SCHEMA_MARKS: dict = {}
ITEM_SCHEMA: dict = {}
ARRAY_PROPS: set = set()     # `module.Schema.arrayProp`, every array property (a child table's parent key names one)
RETIRED: dict = {}
# **The tables whose contract says `x-ticvai-scope: none`** (CHG-R9MIG-001, ADAM CR-166 as the lead ruled it, 21
# October 2026). Filled by main from table_marks; frozen mode hands it to ddl_forward.diff, which removes a scope_path,
# its index and its scope policy that a forward migration gave such a table (V0108 gave platform.outbox_sequence all
# three by the generator's habit, while CR-166's decision and our team's repository migration 240 have none).
DESCOPED: set = set()


# **A key into a partitioned table is indexed, never constrained** (ADR-0056; CHG-MGN-001, ADAM CR-138, 18 October
# 2026). Nothing points at a partitioned table, so the contract leaves such a key undeclared (`x-ticvai-references:
# none`) and the code checks it; `none` also drops the reference the index is written from, and r1 had the index (a
# convention). `(table, column) -> the partitioned table it names`: the generator writes the index and its comment as
# for a convention, with no foreign key and no inbound key for partition_plan.
UNENFORCED_KEYS = {
    ("marketing.message_dispatch_attempt", "message_dispatch_id"): "marketing.message_dispatch",
}


def apply_unenforced_keys(cols: dict) -> None:
    """Mark UNENFORCED_KEYS' columns as convention references (indexed, not constrained) where nothing else names
    their target."""
    for (t, col), ref in UNENFORCED_KEYS.items():
        for c in cols.get(t, []):
            if c.get("column") == col and not c.get("references"):
                c.update({"references": ref, "referenceHow": "convention", "enforced": "no"})


def pick_owner(t: str, cands: list) -> tuple:
    """The key a child's row-level security follows, among its NOT NULL keys to protected parents: `(pick, undecided)`.

    `pick` is `(column, parent, key)`, or None when the keys reach different parents (a modelling decision; the table
    stays unscoped). **Two keys to the same parent are a decision too** (CHG-MGN-001, ADAM CR-148, CR-149, 18 October
    2026): `sorted(cands)[0]` took the first in alphabetical order, which was right for fnb.ingredient_substitute and
    left ledger.inter_entity_obligation's consuming entity unable to read its obligations. The first is still taken, so
    nothing moves until a person decides, but `undecided` names the columns, and derive-ddl lists the table for a
    decision in ROW_OWNER ("owner undecided" in migration-review.md)."""
    if not cands or len({o[1] for o in cands}) != 1:
        return None, []
    cols = sorted({o[0] for o in cands})
    return sorted(cands)[0], (cols if len(cols) > 1 else [])


# Tables pick_owner found with two keys to one parent and no ROW_OWNER entry: table -> (columns, parent, column taken).
OWNER_UNDECIDED: dict = {}


def partition_plan(marks: dict, inbound: dict) -> tuple:
    """Which append-only tables are range-partitioned by month (ADR-0056 section 2): `(partitioned, declined,
    refused)`. `partitioned`: table -> time column. `declined`: `(table, why)` for one the contract marks but that
    cannot be partitioned (no such column, not in the tenant template). `refused`: `(table, [inbound keys])` for one
    something declares a key into.

    **An inbound key fails the run instead of turning partitioning off** (CHG-MGN-001, ADAM CR-138, 18 October
    2026). Until then it moved the table to `declined` with a line in the run's output: CHG-STO-001 declared
    `MessageDispatchAttempt.messageDispatchId` on 14 October, marketing.message_dispatch lost its partitioning in the
    generated DDL, and the migration review asked the migration owner to un-partition a table built partitioned.
    ADR-0056: nothing points at a partitioned table."""
    partitioned: dict = {}
    declined: list = []
    refused: list = []
    for t, m in sorted(marks.items()):
        col = m.get("append_only")
        if not col:
            continue
        if col.startswith("?"):
            declined.append((t, f"the contract names {col[1:]}, which is not a column of the table"))
        elif area(t.split(".")[0]) != "tenant":
            declined.append((t, "not in the tenant template"))
        elif inbound.get(t):
            refused.append((t, sorted(inbound[t])))
        else:
            partitioned[t] = col
    return partitioned, declined, refused


def table_marks(cols: dict, tables) -> dict:
    """What the contract schema a table is derived from says about the table as a whole.

    **A table is found from its columns' `source`**, which names `module.Schema.property` or
    `module.Parent.array[].property` — so a table with no persistence tag of its own
    (`platform.audit_record`) or one derived from an array (`ledger.journal_line`) resolves too.
    Returns `table -> {"append_only": column, "primary_key": [columns], "unique_together": [[columns]],
    "schema": name}`, with property names already turned into this table's column names."""
    out = {}
    for t in tables:
        votes: dict = defaultdict(int)
        # **A child table derived from an array is not its parent** (14 October 2026, CHG-CRD-001). Its parent-key
        # column's source names the parent's array (`identity.PrincipalCredential.history`), which voted for the parent
        # schema, so `identity.principal_credential_history` took `PrincipalCredential`'s unique-together and failed to
        # key it. Where a table has item columns (`...array[].prop`) that resolve to an item schema, only those vote.
        #
        # **...and a parent key never votes** (CHG-MGN-001, ADAM CR-156, 18 October 2026). `platform.sale_board_tile`'s
        # parent key comes from `tenancy.SaleBoard.pages[].tiles`, an item-shaped source whose array (`pages`) has
        # inline items, so it resolved to nothing; under the rule above it was the table's only item column, every
        # `tenancy.SaleBoardTile.*` column was skipped, and the table got no marks: its unique (sale_board_page_id,
        # position) and its three required-when CHECKs were never derived. Item columns vote when one resolves;
        # otherwise the plain columns do, less any whose source is an array property (the parent's, naming the parent).
        item_votes: dict = defaultdict(int)
        for c in cols.get(t, []):
            src = str(c.get("source") or "")
            m = re.match(r"^([\w-]+)\.(\w+)\.(\w+)\[\]\.\w+$", src)
            if m:
                key = ITEM_SCHEMA.get(f"{m.group(1)}.{m.group(2)}.{m.group(3)}")
                if key:
                    item_votes[key] += 1
                continue
            if "[]." in src or src in ARRAY_PROPS:
                continue
            m = re.match(r"^([\w-]+)\.(\w+)\.\w+$", src)
            if m:
                votes[f"{m.group(1)}.{m.group(2)}"] += 1
        if item_votes:
            votes = item_votes
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
        # **A natural key over several columns** (CHG-R6-006, ADAM CR-010): `x-ticvai-unique-together` lists
        # column sets, each named by contract property or, for a column no property carries (`seat_map_id`
        # comes from the relationship graph), by its column name.
        names = {c["column"] for c in cols.get(t, [])}
        ut = marks.get("x-ticvai-unique-together")
        if isinstance(ut, list) and ut:
            entry["unique_together"] = [
                [column_of(str(p)) or (str(p) if str(p) in names else f"?{p}") for p in group]
                for group in ut if isinstance(group, list) and group]
            # **A null member that still collides** (CHG-MKT-002, ADAM CR-087, 14 October 2026). A wishlist entry
            # is `variantId` plus `performanceId`, and a save with no performance is one date-less entry
            # (R149); Postgres treats nulls as distinct, so two date-less saves of one variant were two rows.
            # `x-ticvai-unique-nulls: not-distinct` on the schema makes its unique-together sets
            # `NULLS NOT DISTINCT` (PostgreSQL 15 and later; the platform is on 16).
            if str(marks.get("x-ticvai-unique-nulls") or "").strip() == "not-distinct":
                entry["unique_nulls_not_distinct"] = True
        # **Who may read a row the scope rule would hide** (CHG-GEN-005): `x-ticvai-rls: read-beneath` or
        # `grant-holder-read` on the schema; see RLS_MARKS.
        rls = marks.get("x-ticvai-rls")
        if rls is not None:
            entry["rls"] = str(rls).strip()
        # **A table that takes no scope** (CHG-R9MIG-001, CR-166): `x-ticvai-scope: none`; see DESCOPED.
        sc = marks.get("x-ticvai-scope")
        if sc is not None:
            entry["scope"] = str(sc).strip()
        # **A field needed for one kind of row only** (CHG-TEN-001, ADAM CR-080): `x-ticvai-required-when`
        # maps a property to the values that require it, `{variantId: {kind: product}}`, so a product tile
        # with no variant cannot be stored. Becomes `CHECK (<when> IS DISTINCT FROM 'v' OR <col> IS NOT NULL)`.
        rw = marks.get("x-ticvai-required-when")
        if isinstance(rw, dict) and rw:
            entry["required_when"] = [
                (column_of(str(p)) or f"?{p}",
                 {(column_of(str(k)) or f"?{k}"): v for k, v in (cond or {}).items()})
                for p, cond in rw.items() if isinstance(cond, dict) and cond]
        # **A row names exactly one of two things** (ADAM CR-158, 18 October 2026; CHG-CRA-002):
        # `x-ticvai-exactly-one-of: [[permission, roleId]]` on the schema is a table CHECK that exactly one column of
        # each set is set, `num_nonnulls(a, b) = 1`. A grant names a permission or a role, never both and never neither.
        eo = marks.get("x-ticvai-exactly-one-of")
        if isinstance(eo, list) and eo:
            entry["exactly_one_of"] = [
                [column_of(str(p)) or (str(p) if str(p) in names else f"?{p}") for p in group]
                for group in eo if isinstance(group, list) and len(group) > 1]
        # **A plain index over several columns the contract asks for** (ADAM CR-165, CR-166; CHG-CRA-004):
        # `x-ticvai-index: [[aggregateId, sequence]]` on the schema, for a lookup no key or unique index serves
        # (a provider's reference, an aggregate's next sequence). Named `<table>_<columns>_idx`.
        ix = marks.get("x-ticvai-index")
        if isinstance(ix, list) and ix:
            entry["index"] = [
                [column_of(str(p)) or (str(p) if str(p) in names else f"?{p}") for p in group]
                for group in ix if isinstance(group, list) and group]
        # **Unique among the rows of one kind only** (ADAM CR-154; CHG-CRA-004): `x-ticvai-unique-when:
        # [{columns: [scopePath], when: {isCurrent: true}}]` is a partial unique index, so one tenant has one
        # current version however many it keeps. Named `<table>_<columns>_<when column>_uniq`.
        uw = marks.get("x-ticvai-unique-when")
        if isinstance(uw, list) and uw:
            entry["unique_when"] = [
                ([column_of(str(p)) or (str(p) if str(p) in names else f"?{p}") for p in (u.get("columns") or [])],
                 {(column_of(str(k)) or (str(k) if str(k) in names else f"?{k}")): v
                  for k, v in (u.get("when") or {}).items()})
                for u in uw if isinstance(u, dict) and u.get("columns") and u.get("when")]
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
    # **An integer column with a contract enum carries it too** (14 October 2026, CHG-CRD-002): the tenant's PIN
    # settings (`PasswordPolicy.pinLength` 4, 6 or 8) are drop-downs of numbers, typed integer by
    # `x-ticvai-persistence-column` in derive-schema, and the database holds the same values as the contract.
    if typ in ("integer", "bigint", "smallint"):
        values = [v for v in (spec.get("enum") or []) if v is not None]
        if values and all(isinstance(v, int) and not isinstance(v, bool) for v in values):
            checks.append(f"{q(col)} IN ({', '.join(str(v) for v in values)})")
    if checks:
        out += (f" CONSTRAINT {obj_name(short, col, suffix='chk')} CHECK ("
                + " AND ".join(checks) + ")")
    return out


# **A storage-only column states its own rules** (CHG-R6-001, ADAM CR-001, 12 October 2026).
# `pii.subject.kind` and `pii.subject_contact.kind` are columns no contract describes, and the schema reference
# typed them `pii.subject_kind` and `pii.contact_kind` -- enum types no file creates, so 010-pii.sql could not be
# applied. Their values were only in the description. A column record may now carry `enum` (and `maxLength`,
# `default`) itself, read where the column has no contract property, and the column is plain `text` with the
# `<table>_<column>_chk` CHECK every contract enum gets. check-ddl-conventions D-UNDEFINED-TYPE fails on a type
# that names a schema-qualified type nothing creates.
STORAGE_RULE_KEYS = ("enum", "maxLength", "default")


def column_spec(c: dict, contract_props: dict) -> dict:
    """The rules a column's CHECK and DEFAULT come from: its contract property, else its own record."""
    spec = contract_props.get(str(c.get("source") or ""))
    if spec:
        return spec
    return {k: c[k] for k in STORAGE_RULE_KEYS if k in c}


def pg_type(t: str | None) -> str:
    if not t:
        return "text"
    return TYPE_MAP.get(t, t)



# **Case-insensitive uniqueness** (CHG-GEN-001, ADAM CR-079, CR-066): the property mark that keeps a value exact.
UNIQUE_COMPARE = "x-ticvai-unique-compare"


def unique_key(col: str, col_type: dict, src_of: dict) -> str:
    """One member of a unique index: `lower(col)` for a text column, unless its contract property says
    `x-ticvai-unique-compare: exact` (an opaque external id); the column as it is otherwise. common.yaml
    (`Problem`, the uniqueness rule) states the same rule, and check-ddl-conventions D-UNIQUE-CASE holds the
    index to it."""
    if col_type.get(col) == "text" and str((src_of.get(col) or {}).get(UNIQUE_COMPARE) or "") != "exact":
        return f"lower({q(col)})"
    return q(col)


# `table -> [columns]` from `x-ticvai-primary-key`, filled in `main` before any key is asked for.
DECLARED_PK: dict = {}

# **The type each column takes in the generated DDL** (ADAM CR-067, 14 October 2026, CHG-DDL-002), filled in `main`
# and written to `handoff/ddl-column-types.json`. The schema reference keeps the contract's shape (`text` for an
# id the wire sends as a string, `numeric` for a quantity), and this file applies ADR-0056's one id type and
# `numeric(18,4)` on top. ADAM's table view and the workbook's Columns sheet took the type from the frozen r1
# SQL where a CREATE TABLE of the same name existed and from the schema reference where none did -- so every
# table renamed after r1 (`seating.seat_reservation`, `inventory.inventory_item`) showed `text` ids and bare
# `numeric` quantities nobody intends, while the DDL generated for it says uuid and numeric(18,4).
DDL_TYPES: dict = {}
DDL_TYPES_FILE = ROOT / "handoff" / "ddl-column-types.json"


def ddl_records(files: dict) -> dict:
    """**The whole table record, read from the DDL this run generates** (CHG-R10TEN-014; ADAM CR-092, accepted 15
    October 2026). The workbook's Columns sheet, and ADAM's table view built from it, took `Required` from the schema
    reference, which leaves a `scope_path` optional where every scoped table's DDL says `ltree NOT NULL`, and listed
    only the columns the schema reference names; #27686 was done when "every table matches its record", and 218 of
    497 records disagreed with the DDL they come from. CR-067 settled that the DDL is right and took the types from it;
    this takes the rest: per table, each column in the generated CREATE TABLE with whether it is NOT NULL (a primary-key
    column always is), the declared keys (the primary key, every foreign key and every unique index, partial ones with
    their condition) and the row-level-security helper the table's policy is made with.

    Returns `{table: {"columns": [[column, notNull]], "primaryKey": [...], "keys": [...], "policy": helper}}`."""
    out: dict = {}

    def rec(t: str) -> dict:
        return out.setdefault(t, {"columns": [], "primaryKey": [], "keys": [], "policy": ""})

    for name in sorted(files):
        if not name.endswith(".sql"):
            continue
        for st in ddl_forward.split_statements(files[name]):
            s = ddl_forward.norm(st)
            m = re.match(r"CREATE TABLE (?:IF NOT EXISTS )?(\S+)\s*\(", s, re.I)
            if m:
                t = ddl_forward.unq(m.group(1))
                start = s.index("(", m.start(1))
                body = s[start + 1:ddl_forward.balanced(s, start)]
                r = rec(t)
                for item in ddl_forward.top_level_split(body):
                    head = item.split()[0].upper() if item.split() else ""
                    if item.upper().startswith(ddl_forward.TABLE_LEVEL):
                        pk = re.search(r"PRIMARY KEY\s*\(([^)]*)\)", item, re.I)
                        if pk:
                            r["primaryKey"] = [ddl_forward.unq(x.strip()) for x in pk.group(1).split(",")]
                        continue
                    if head in ("LIKE",):
                        continue
                    col = ddl_forward.unq(item.split()[0])
                    is_pk = bool(re.search(r"\bPRIMARY KEY\b", item, re.I))
                    if is_pk:
                        r["primaryKey"] = [col]
                    r["columns"].append([col, is_pk or bool(re.search(r"\bNOT NULL\b", item, re.I))])
                continue
            m = re.match(r"ALTER TABLE (?:ONLY )?(\S+) ADD CONSTRAINT (\S+) FOREIGN KEY \(([^)]*)\) REFERENCES "
                         r"(\S+?)\s*\(([^)]*)\)", s, re.I)
            if m:
                rec(ddl_forward.unq(m.group(1)))["keys"].append(
                    f"foreign key ({m.group(3).replace(chr(34), '')}) -> {ddl_forward.unq(m.group(4))}"
                    f"({m.group(5).replace(chr(34), '')})")
                continue
            m = re.match(r"CREATE UNIQUE INDEX (?:IF NOT EXISTS )?\S+ ON (\S+)(?: USING \w+)? \((.*?)\)(?: WHERE (.+))?$",
                         s.rstrip(";"), re.I)
            if m:
                rec(ddl_forward.unq(m.group(1)))["keys"].append(
                    f"unique ({m.group(2).replace(chr(34), '')})" + (f" where {m.group(3)}" if m.group(3) else ""))
                continue
            m = re.match(r"SELECT platform\.(apply_\w*rls)\('([^']+)'::regclass", s, re.I)
            if m:
                rec(ddl_forward.unq(m.group(2)))["policy"] = m.group(1)
    for t, r in out.items():
        if r["primaryKey"]:
            pkset = set(r["primaryKey"])
            r["columns"] = [[c, nn or c in pkset] for c, nn in r["columns"]]
        r["keys"] = sorted(set(r["keys"]))
    return {t: r for t, r in sorted(out.items()) if r["columns"]}


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


def declared_renames() -> dict:
    """The renames declared in `tools/derive-schema-history.py`: `RENAMES` (tables) and `COLUMN_RENAMES`
    (columns, by the table's name now), read from its source so importing it runs nothing (CHG-R6-010).
    Frozen mode hands them to ddl_forward, so a renamed table or column reaches migration-review.md as a
    rename rather than as a new table or column beside the old one."""
    import ast
    out = {"tables": {}, "columns": {}}
    try:
        tree = ast.parse((ROOT / "tools" / "derive-schema-history.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return out
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        names = {getattr(t, "id", None) for t in node.targets}
        if "RENAMES" in names:
            out["tables"] = {r["from"]: r["to"] for r in ast.literal_eval(node.value)}
        if "COLUMN_RENAMES" in names:
            out["columns"] = {(r["table"], r["from"]): r["to"] for r in ast.literal_eval(node.value)}
    return out


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
    renames = declared_renames()
    # **The declared renames go first, in an early names file, and everything else is derived after them**
    # (CHG-R8WFM-001; r8 sample walk, table-rename-not-in-migrations). Pass 1 asks which declared renames the old side
    # still has and where each may run (ddl_forward.place_renames: after the last frozen file that names its old name,
    # before the first that names its new one); their files are then folded into the old side at their place by name,
    # and the diff runs again, so the additive file and the names file are derived against the renamed tables, exactly
    # as the next refresh, with the early files on disk, derives them. A rename no slot fits stays a review row.
    early_files = {CONTROL: {}, "tenant": {}}     # area -> {file name: text}, the early names files this run writes
    early_meta = {CONTROL: {}, "tenant": {}}      # area -> {file name: (version, the file it runs before, items)}
    taken_versions = {x.name.split("__", 1)[0] for d in (CONTROL, "tenant") for x in (OUT / d).glob("V*.sql")}

    def old_model(area_dir: str):
        old = ddl_forward.Model()
        for path in sorted(ls_tree(commit, f"backend/{area_dir}")):
            name = path.rsplit("/", 1)[-1]
            if path.endswith(".sql") and not FORWARD_FILE.match(name):
                old.add_file((show(commit, path) or b"").decode("utf-8"))
        fwd = {p.name: p.read_text(encoding="utf-8") for p in (OUT / area_dir).glob("V*.sql") if FORWARD_FILE.match(p.name)}
        fwd.update(early_files[area_dir])
        for name in sorted(fwd):   # the order a database applies them: by name
            old.apply_forward(re.split(r"^-- =+\n-- ROLLBACK\b", fwd[name], maxsplit=1, flags=re.M)[0])
        return old, fwd

    news = {}
    for area_dir in (CONTROL, "tenant"):
        new = ddl_forward.Model()
        for name in sorted(n for n in files if n.startswith(area_dir + "/") and n.endswith(".sql")):
            new.add_file(files[name])
        news[area_dir] = new
    for area_dir in (CONTROL, "tenant"):
        for _pass in range(4):
            old, fwd = old_model(area_dir)
            items = ddl_forward.declared_rename_items(old, news[area_dir], renames)
            if not items:
                break
            placed, unplaced = ddl_forward.place_renames(items, fwd, taken_versions)
            for it in unplaced:
                print(f"  {area_dir}: a declared rename no slot fits, left for a person: {it['stmt'].splitlines()[0]}")
            if not placed:
                break
            names_sorted = sorted(fwd)
            for ev, (after, its) in placed.items():
                nxt = next((n for n in names_sorted if n > after), None)
                name = f"{ev}__names_early_after_{safe_tag}_{stamp}.sql"
                early_meta[area_dir][name] = (ev, nxt, its)
                # folded into the old side for the next pass; written with its final header below
                early_files[area_dir][name] = ddl_forward.render_recon(
                    ddl_forward.early_plan(area_dir, its), ev, baseline, stamp, before=nxt or "", rest="")
    for area_dir in (CONTROL, "tenant"):
        old, _fwd = old_model(area_dir)
        plans.append(ddl_forward.diff(area_dir, old, news[area_dir], renames, retired=RETIRED, descoped=DESCOPED))
    # **Root-level files are documentation of references that are not constraints** (990): nothing
    # applies them, so a change is listed rather than migrated.
    for name in sorted(n for n in files if "/" not in n and n.endswith(".sql")):
        was = show(commit, f"backend/{name}")
        if was is not None and was.decode("utf-8").replace("\r\n", "\n") != files[name]:
            extra.append(("both", "file changed", name, "the generator would write it differently",
                          "not applied anywhere: bring the application rules it documents up to date by hand"))
    # **Two keys to one parent wait for a decision** (CHG-MGN-001, ADAM CR-148, CR-149): listed, not resolved
    # alphabetically. Nothing to migrate until the package decides; the policy then reaches a forward migration.
    for t, (cols, par, took) in sorted(OWNER_UNDECIDED.items()):
        extra.append(("tenant" if area(t.split(".")[0]) == "tenant" else CONTROL, "owner undecided", t,
                      f"two NOT NULL keys to {par} ({', '.join(cols)}); its row-level security follows {took}, the "
                      "first in alphabetical order, until the row's owner is decided",
                      "nothing to migrate yet: the package decides which key owns the row (tools/derive-ddl.py "
                      "ROW_OWNER) and the next release writes the policy"))

    written = []
    for p in plans:
        if not p.statements:
            continue
        dest = OUT / p.area / f"{version}__after_{safe_tag}_{stamp}.sql"
        written.append((dest, p))
        if apply:
            dest.write_text(ddl_forward.render(p, version, baseline, stamp), encoding="utf-8")
    # **The second file: the names** (R8-MIG-001). It takes the next number after the additive file, or the same
    # number when nothing additive is due, and is one number for both databases like the first.
    recon_n = version_n + (1 if any(p.statements for p in plans) else 0)
    recon_version = f"V{recon_n:04d}"
    # the early names files of the declared renames (CHG-R8WFM-001), with their final header
    for area_dir, meta in early_meta.items():
        for name, (ev, nxt, its) in sorted(meta.items()):
            ep = ddl_forward.early_plan(area_dir, its)
            edest = OUT / area_dir / name
            written.append((edest, ep))
            if apply:
                edest.write_text(ddl_forward.render_recon(ep, ev, baseline, stamp, before=nxt or "",
                                                          rest=recon_version), encoding="utf-8")
    for p in plans:
        if not p.recon:
            continue
        # **The renames a frozen file already needs go in a file that sorts before it** (R8-MIG-001, CHG-R8MIG-003):
        # V0104 applies row-level security on four columns by their new names, so a fresh database stopped there.
        # The file takes the number before the first frozen file that needs one and the next free letter (V0103a
        # for V0104), which sorts between the two by name; a number of its own would be a number already taken
        # (V01035 reads as 1035, the plan's V1035__fnb.sql). This run's own additive file counts as frozen too.
        frozen = {x.name: x.read_text(encoding="utf-8") for x in (OUT / p.area).glob("V*.sql")
                  if FORWARD_FILE.match(x.name) and "__names_" not in x.name}
        frozen.update({f"{version}__after_{safe_tag}_{stamp}.sql": ddl_forward.render(q, version, baseline, stamp)
                       for q in plans if q.area == p.area and q.statements})
        early, rest, first = ddl_forward.split_early(p, frozen)
        if early[0]:
            import dataclasses as _dc
            taken = {x.name.split("__", 1)[0] for x in (OUT / p.area).glob("V*.sql")}
            ev = ddl_forward.early_version(first, taken)
            ep = _dc.replace(p, recon=early[0], recon_rollback=early[1],
                             recon_counts={"renames": len(early[0]), "keys": 0, "indexes": 0})
            edest = OUT / p.area / f"{ev}__names_early_after_{safe_tag}_{stamp}.sql"
            written.append((edest, ep))
            if apply:
                edest.write_text(ddl_forward.render_recon(ep, ev, baseline, stamp, before=first, rest=recon_version),
                                 encoding="utf-8")
            p.recon, p.recon_rollback = rest
            p.recon_counts["renames"] -= len(early[0])
            if not p.recon:
                continue
        dest = OUT / p.area / f"{recon_version}__names_after_{safe_tag}_{stamp}.sql"
        written.append((dest, p))
        if apply:
            dest.write_text(ddl_forward.render_recon(p, recon_version, baseline, stamp), encoding="utf-8")
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
        if "__names_" in dest.name:
            r = p.recon_counts
            print(f"  forward migration {dest.relative_to(ROOT).as_posix()}: {r.get('tables', 0)} table(s), {r['renames']} column rename(s), "
                  f"{r['keys']} key(s), {r['indexes']} index(es)" + ("" if apply else " (not written, pass --apply)"))
            continue
        print(f"  forward migration {dest.relative_to(ROOT).as_posix()}: {c['tables']} table(s), "
              f"{c['columns']} column(s), {c['indexes']} index(es), {c['other']} other"
              + (f", {c['policies']} row-level security polic(ies) re-applied" if c.get("policies") else "")
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
    apply_unenforced_keys(cols)

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
            if spec.get(UNIQUE_COMPARE) and UNIQUE_COMPARE not in contract_props[tgt]:
                contract_props[tgt][UNIQUE_COMPARE] = spec[UNIQUE_COMPARE]

    # ---- ADR-0056 and ADR-0058, accepted 30 September ---------------------------------------
    # **What the contract schema says about a table as a whole**: a named key
    # (`x-ticvai-primary-key`) and whether its rows are only ever appended
    # (`x-ticvai-append-only: <time property>`).
    marks = table_marks(cols, real)
    DESCOPED.clear()
    for t, m in sorted(marks.items()):
        if m.get("scope") is None:
            continue
        if m["scope"] != "none":
            print(f"  ! {t}: x-ticvai-scope {m['scope']!r} is not 'none'; nothing else is defined")
            continue
        if any(c["column"] == "scope_path" for c in cols.get(t, [])):
            print(f"  ! {t}: x-ticvai-scope: none, but the schema reference gives it a scope_path; its scope stays")
            continue
        DESCOPED.add(t)
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
    partitioned, declined, refused = partition_plan(marks, inbound)
    if refused:
        for t, refs in refused:
            print(f"  ! {t} is partitioned by month (x-ticvai-append-only, ADR-0056) and {', '.join(refs)} "
                  "declares a key into it. Nothing points at a partitioned table: mark that property "
                  "`x-ticvai-references: none` (the code checks it; UNENFORCED_KEYS keeps its index), then run "
                  "derive-schema before derive-ddl")
        print("  derive-ddl refuses to drop a table's partitioning; nothing written (CHG-MGN-001, ADAM CR-138)")
        return 1

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
            col_type: dict = {}   # column -> its DDL type, for the case-insensitive unique indexes below
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
                DDL_TYPES.setdefault(t, {})[col] = typ
                pk = " PRIMARY KEY" if inline_pk and col == tkey else ""
                # **Contract enums, maxLength and defaults become a CHECK and a DEFAULT.** Not on
                # a path column: its contract type is a string and its column is an ltree.
                rules = "" if is_path else column_rules(short, col, typ, column_spec(c, contract_props))
                if " CONSTRAINT " in rules:
                    n_chk += 1
                if " DEFAULT " in rules:
                    n_def += 1
                # **The space after the name is not padding.** Until 26 September this was
                # `{q(col):<34}{typ}` with nothing between, so a name of 34 characters or more ran
                # into its type -- `requires_corrective_action_on_breachboolean` -- and five
                # CREATE TABLE statements in four files could not be parsed.
                body.append(f"    {q(col):<33} {typ}{pk}{nn}{rules}")
                col_type[col] = typ
                n_cols += 1
                # `x-ticvai-change-version` (ADAM CR-239, CHG-R10ORD-011): the sequence and trigger that move it.
                if (column_spec(c, contract_props) or {}).get(CHANGE_VERSION_MARK) is True:
                    if typ != "bigint":
                        print(f"  ! {t}.{col}: x-ticvai-change-version needs a bigint (integer, int64), not {typ}")
                    else:
                        idx_lines.append((schema, change_version_sql(schema, short, t, col)))

                ref = c.get("references")
                if ref and ref in real:
                    tgt_s, tgt_t = ref.split(".", 1)
                    tgt_key = key_of(ref, cols)
                    # **A key into a versioned row names its version too** (CHG-R8MIG-019; R8 blocker
                    # APPROVALS-TENANCY-C08): `x-ticvai-references-version: <sibling property>` on a reference whose
                    # parent's declared key is (id, version) makes the key (col, version col) -> parent (id, version).
                    vprop = (contract_props.get(str(c.get("source") or "")) or {}).get("x-ticvai-references-version")
                    vcol = next((x["column"] for x in cols[t]
                                 if str(x.get("source") or "").rsplit(".", 1)[-1] == str(vprop)), None) if vprop else None
                    # A derived child of a versioned parent names its version column itself (derive-schema,
                    # CHG-R8INT-023): `plan_module.plan_id` with `plan_version`.
                    vcol = vcol or c.get("referencesVersionColumn")
                    ppk = DECLARED_PK.get(ref) or []
                    if (c.get("enforced") == "yes" and vcol and len(ppk) == 2
                            and area(schema) == area(tgt_s)):
                        fk_lines.append((schema,
                            f"ALTER TABLE {q(schema)}.{q(short)} ADD CONSTRAINT "
                            f"{obj_name(short, col, suffix='fkey')} FOREIGN KEY ({q(col)}, {q(vcol)}) "
                            f"REFERENCES {q(tgt_s)}.{q(tgt_t)}({q(ppk[0])}, {q(ppk[1])});"))
                        n_fk += 1
                        idx_lines.append((schema,
                            f"-- declared, with its version: {t}.({col}, {vcol}) -> {ref}\n"
                            f"CREATE INDEX IF NOT EXISTS {obj_name(short, col, vcol, suffix='idx')} "
                            f"ON {q(schema)}.{q(short)} ({q(col)}, {q(vcol)});"))
                        n_idx += 1
                    elif c.get("enforced") == "yes" and tgt_key:
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
            # **The scope tree is a tree with one root, and a path names one node** (CHG-R6-003, ADAM CR-006,
            # 12 October 2026). `venue_in_scope` and `tenant_root_in_scope` resolve a grant by `level = 'tenant'`
            # and by `path`, and a second tenant row or a duplicated path would make both answer for two nodes;
            # `venue_in_scope` even counts the tenant rows to hide null-venue rows when there are two. Nothing
            # stopped either. The tenant root is unique through a partial index on a constant, and the path by a
            # plain unique index beside the GiST one (GiST cannot be unique). `parent_id -> platform.scope(id)`
            # is declared in the contract (`OrgUnit.parentId`, x-ticvai-references) and comes out as a foreign key.
            if t == SCOPE_TABLE and "level" in names:
                idx_lines.append((schema,
                    "-- one tenant root per tenant database (CHG-R6-003)\n"
                    f"CREATE UNIQUE INDEX IF NOT EXISTS {obj_name(short, 'tenant_root', suffix='uniq')} "
                    f"ON {q(schema)}.{q(short)} ((true)) WHERE level = 'tenant';"))
                n_uniq += 1
            if t == SCOPE_TABLE and "path" in names:
                idx_lines.append((schema,
                    "-- a path names one node (CHG-R6-003)\n"
                    f"CREATE UNIQUE INDEX IF NOT EXISTS {obj_name(short, 'path', suffix='uniq')} "
                    f"ON {q(schema)}.{q(short)} (path);"))
                n_uniq += 1
            # **A second visibility path is indexed like the first** -- the shared policy tests it
            # on every read.
            second = SHARED_SCOPE.get(t)
            if second and second in names:
                idx_lines.append((schema,
                    f"CREATE INDEX IF NOT EXISTS {index_name(schema, short, second)} "
                    f"ON {q(schema)}.{q(short)} USING gist ({q(second)});"))
                n_idx += 1

            # **A code is unique whatever its case** (CHG-GEN-001, ADAM CR-079 and CR-066, 14 October 2026).
            # common.yaml says a value under `x-ticvai-unique` is compared case-insensitively, and every index
            # derived from it was a plain one, so `VIP` and `vip` were two role codes and two promotion codes.
            # A text column in a unique index is indexed as `lower(column)`; an opaque external id whose property
            # says `x-ticvai-unique-compare: exact` (a provider's event id, what a gate reads off a credential)
            # is compared as it is. A key that is not text (`venue_id`, `scope_path`) is never wrapped.
            src_of = {c["column"]: contract_props.get(str(c.get("source") or ""), {}) for c in cols[t]}
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
                    f"({', '.join(unique_key(k, col_type, src_of) for k in keycols)}){where};"))
                n_uniq += 1

            # **Uniqueness over several columns the contract schema names** (`x-ticvai-unique-together`,
            # CHG-R6-006). Postgres treats nulls as distinct, so a row with a null member never collides.
            for group in (marks.get(t) or {}).get("unique_together") or []:
                missing = [k for k in group if k.startswith("?")]
                if missing:
                    no_unique.append(f"{t} (x-ticvai-unique-together {group}): "
                                     f"{', '.join(k[1:] for k in missing)} is not a column")
                    continue
                keycols = list(group)
                if part_col and part_col not in keycols:
                    keycols.append(part_col)
                uname = obj_name(short, *keycols, suffix="uniq")
                nnd = " NULLS NOT DISTINCT" if (marks.get(t) or {}).get("unique_nulls_not_distinct") else ""
                idx_lines.append((schema,
                    f"-- unique together (x-ticvai-unique-together): {t} ({', '.join(group)})\n"
                    f"CREATE UNIQUE INDEX IF NOT EXISTS {uname} ON {q(schema)}.{q(short)} "
                    f"({', '.join(unique_key(k, col_type, src_of) for k in keycols)}){nnd};"))
                n_uniq += 1

            # `x-ticvai-unique-when` (ADAM CR-154, CHG-CRA-004): unique among the rows the condition selects only,
            # a partial unique index named like any other, `<table>_<columns>_uniq` (the name the published answer
            # gave developers for their own migration).
            for group, cond in (marks.get(t) or {}).get("unique_when") or []:
                bad = [k[1:] for k in [*group, *cond] if k.startswith("?")]
                if bad:
                    no_unique.append(f"{t} (x-ticvai-unique-when {group}): {', '.join(bad)} is not a column")
                    continue
                keycols = list(group)
                if part_col and part_col not in keycols:
                    keycols.append(part_col)
                idx_lines.append((schema, unique_when_sql(schema, short, t, keycols, cond,
                                                          [unique_key(k, col_type, src_of) for k in keycols])))
                n_uniq += 1

            # `x-ticvai-index` (ADAM CR-165, CR-166; CHG-CRA-004): a plain index over the columns the contract names.
            for group in (marks.get(t) or {}).get("index") or []:
                missing = [k for k in group if k.startswith("?")]
                if missing:
                    no_unique.append(f"{t} (x-ticvai-index {group}): {', '.join(k[1:] for k in missing)} is not a column")
                    continue
                idx_lines.append((schema, index_sql(schema, short, t, group)))
                n_idx += 1

            if not inline_pk and pk_cols:
                body.append(f"    CONSTRAINT {obj_name(short, suffix='pkey')} PRIMARY KEY "
                            f"({', '.join(q(k) for k in pk_cols)})")
            # `x-ticvai-required-when` (CHG-TEN-001): a column required only for some rows, as a table CHECK.
            for rcol, cond in (marks.get(t) or {}).get("required_when") or []:
                bad = [k[1:] for k in [rcol, *cond] if k.startswith("?")]
                if bad:
                    no_unique.append(f"{t} (x-ticvai-required-when {rcol}): {', '.join(bad)} is not a column")
                    continue
                exempt = []
                for k, v in sorted(cond.items()):
                    if v is None:
                        # `{reservationId: {orderId: null}}`: required where the other column is null (CHG-R8MIG-017,
                        # ORDERS-MONEY-C35), so a row names at least one of the two
                        exempt.append(f"{q(k)} IS NOT NULL")
                        continue
                    if isinstance(v, dict) and list(v) == ["not"] and v["not"] is None:
                        # `{planVersion: {planId: {not: null}}}`: required wherever the other column is set (r8 gate
                        # residue, CHG-R8RES-006). Written both ways, two columns are both set or both null: a
                        # two-column key with one null column is never checked by its foreign key (MATCH SIMPLE).
                        exempt.append(f"{q(k)} IS NULL")
                        continue
                    vals = v if isinstance(v, list) else [v]
                    lits = ", ".join(sql_literal(x) for x in vals)
                    exempt.append(f"{q(k)} IS DISTINCT FROM {lits}" if len(vals) == 1
                                  else f"{q(k)} IS NULL OR {q(k)} NOT IN ({lits})")
                body.append(f"    CONSTRAINT {obj_name(short, rcol, 'when', suffix='chk')} CHECK ("
                            f"{' OR '.join(exempt)} OR {q(rcol)} IS NOT NULL)")
            # `x-ticvai-exactly-one-of` (ADAM CR-158, CHG-CRA-002): exactly one column of the set is set.
            for group in (marks.get(t) or {}).get("exactly_one_of") or []:
                bad = [k[1:] for k in group if k.startswith("?")]
                if bad:
                    no_unique.append(f"{t} (x-ticvai-exactly-one-of {group}): {', '.join(bad)} is not a column")
                    continue
                body.append(exactly_one_sql(short, group))
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
    for t, col in sorted(ROW_OWNER.items()):
        if t in real and not any(o[0] == col for o in owners.get(t, [])):
            print(f"  ! ROW_OWNER names {t}.{col}, which is not a NOT NULL declared reference; the table "
                  "falls back to the default owner rule")
    while True:
        round_ = []
        for t in sorted(real):
            if t in protected:
                continue
            own = owners.get(t, [])
            if t in ROW_OWNER:
                own = [o for o in own if o[0] == ROW_OWNER[t]]
            cands = [o for o in own if o[1] in protected]
            pick, undecided = pick_owner(t, cands)
            if pick:
                col, par, key = pick
                round_.append((t, col, par, key))
                if undecided:
                    OWNER_UNDECIDED[t] = (undecided, par, col)
        if not round_:
            break
        for t, col, par, key in round_:
            protected[t] = "parent"
            by_parent.append((t, col, par, key))

    # **`x-ticvai-rls` on the contract schema** (CHG-GEN-005, ADAM CR-076, audit R183): SELECT opened beneath the
    # owner, or to any grant holder; every write keeps the check the base rule gives it. See RLS_MARKS.
    def tq(t: str) -> str:
        sch, n = t.split(".", 1)
        return f"{q(sch)}.{q(n)}"

    split_calls: dict = {}    # table -> (call, why)
    split_mark: dict = {}     # table -> (its x-ticvai-rls mark, its base rule)
    split_write: dict = {}    # table -> its write check, `{a}` standing for the row's alias
    split_depth: dict = {}
    parent_of = {p[0]: p for p in by_parent}
    for t in sorted(real):
        mark = (marks.get(t) or {}).get("rls") or TABLE_RLS.get(t)
        if not mark:
            continue
        if t in APPEND_AUDIT and mark in APPEND_AUDIT_MARKS:
            continue   # an append-only trail's wider read is its own helper (CHG-R10TEN-006), applied below
        if mark not in RLS_MARKS:
            print(f"  ! {t}: x-ticvai-rls {mark!r} is not one of {', '.join(RLS_MARKS)}; the base rule stands")
            continue
        if area(t.split(".")[0]) != "tenant" or SCOPE_TABLE not in real:
            print(f"  ! {t}: x-ticvai-rls applies in the tenant database only; the base rule stands")
            continue
        if t in shared_scope or t in parent_of or t in APPEND_AUDIT or t == SCOPE_TABLE:
            print(f"  ! {t}: x-ticvai-rls {mark} on a shared-scope, parent-owned or append-only table is not "
                  "defined; the base rule stands")
            continue
        has = {c["column"] for c in cols[t]}
        if t in scoped:
            base, write = "scope_path", "platform.in_scope({a}scope_path)"
        elif t in venue_only:
            base, write = "venue_id", "platform.venue_in_scope({a}venue_id)"
        elif "subject_id" in has:
            base, write = "subject", "platform.subject_in_scope({a}subject_id)"
        else:
            base, write = "tenant root", "platform.tenant_root_in_scope()"
        if mark in ("guest-owns", "guest-reads-own"):
            if base not in ("scope_path", "venue_id"):
                print(f"  ! {t}: x-ticvai-rls {mark} needs a scope_path or venue_id for staff; the base rule stands")
                continue
            staff = STATEMENT_SCOPE if base == "scope_path" else "platform.venue_in_scope({a}venue_id)"
            if "subject_id" in has:
                guest = GUEST_SUBJECT
            elif mark == "guest-reads-own":
                # the guest's own parent: the one declared reference to a table that carries the guest's subject and
                # is itself marked for the guest (orders.sales_order)
                via = sorted({(c["column"], c["references"]) for c in cols[t]
                              if c.get("references") in real and c.get("enforced") == "yes"
                              and ((marks.get(c["references"]) or {}).get("rls") in ("guest-owns", "guest-reads-own"))
                              and any(x["column"] == "subject_id" for x in cols.get(c["references"], []))})
                if len(via) != 1:
                    print(f"  ! {t}: x-ticvai-rls guest-reads-own on a table with no subject_id needs exactly one "
                          f"declared reference to a table with one (found {via}); the base rule stands")
                    continue
                fk, par_t = via[0]
                guest = (f"EXISTS (SELECT 1 FROM {tq(par_t)} gp WHERE gp.id = {tq(t)}.{q(fk)} AND "
                         + GUEST_SUBJECT.format(a="gp.") + ")")
            else:
                print(f"  ! {t}: x-ticvai-rls guest-owns needs a subject_id; the base rule stands")
                continue
            read = f"({staff}) OR ({guest})"
            write = staff if mark == "guest-reads-own" else read
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, {sql_literal(read.format(a=''))}, "
                    f"{sql_literal(write.format(a=''))});")
            write = "(" + write + ")"
            base = ("the guest's own subject, or staff by " + base if mark == "guest-owns"
                    else "staff by " + base + "; read also by the guest it belongs to")
        elif mark == "any-grant-no-delete":
            if base != "tenant root" or t not in DESCOPED:
                print(f"  ! {t}: x-ticvai-rls any-grant-no-delete is for a table that takes no scope (x-ticvai-scope: "
                      "none) and has no venue, subject or owner; the base rule stands")
                continue
            write = ANY_GRANT
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, {sql_literal(ANY_GRANT)}, "
                    f"{sql_literal(ANY_GRANT)});\nDROP POLICY IF EXISTS {q(t.split('.', 1)[1][:55] + '_delete')} "
                    f"ON {tq(t)};")
            base = "any grant, never deleted"
        elif mark == "home-scope-write":
            if "home_scope_id" not in has or base in ("scope_path", "venue_id"):
                print(f"  ! {t}: x-ticvai-rls home-scope-write needs home_scope_id and no scope_path or venue_id; "
                      "the base rule stands")
                continue
            write = ("(platform.tenant_root_in_scope() OR EXISTS (SELECT 1 FROM platform.scope hs WHERE hs.id = "
                     "{a}home_scope_id AND platform.in_scope(hs.path)))")
            call = (f"SELECT platform.apply_grant_holder_read_rls('{tq(t)}'::regclass, "
                    f"{sql_literal(write.format(a=''))});")
            base = "the tenant root or a grant over its home scope"
        elif mark == "scope-or-subject":
            subs = [x for x in ("subject_id", "over_subject_id", "granted_by_subject_id") if x in has]
            holder = "over_subject_id" if "over_subject_id" in has else ("subject_id" if "subject_id" in has else None)
            if base != "scope_path" or not holder:
                print(f"  ! {t}: x-ticvai-rls scope-or-subject needs a scope_path and a subject column; the base rule "
                      "stands")
                continue
            read = " OR ".join(["platform.in_scope(scope_path)"]
                               + [f"platform.own_row(NULL::uuid, {x})" for x in subs])
            write = "(platform.in_scope({a}scope_path) OR platform.own_row(NULL::uuid, {a}" + holder + "))"
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, {sql_literal(read)}, "
                    f"{sql_literal(write.format(a=''))});")
            base = "its scope, or the guest account it is about"
        elif mark == "signed-in-read":
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, 'platform.signed_in()', "
                    f"{sql_literal(write.format(a=''))});")
        elif mark == "own-or-home-scope":
            if "principal_id" not in has or base in ("scope_path", "venue_id"):
                print(f"  ! {t}: x-ticvai-rls own-or-home-scope needs principal_id and no scope_path or venue_id; "
                      "the base rule stands")
                continue
            write = ("(platform.own_row({a}principal_id, NULL::uuid) OR EXISTS (SELECT 1 FROM identity.principal hp "
                     "JOIN platform.scope hs ON hs.id = hp.home_scope_id WHERE hp.id = {a}principal_id "
                     "AND platform.in_scope(hs.path)))")
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, {sql_literal(write.format(a=''))}, "
                    f"{sql_literal(write.format(a=''))});")
            base = "its principal, a grant over the principal's home scope, or the tenant root"
        elif mark == "subject-self":
            if "subject_id" in has or base in ("scope_path", "venue_id"):
                print(f"  ! {t}: x-ticvai-rls subject-self is for the subject record itself (its id is the subject); "
                      "the base rule stands")
                continue
            write = "platform.own_row(NULL::uuid, {a}id)"
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, "
                    f"{sql_literal('platform.grant_holder() OR platform.own_row(NULL::uuid, id)')}, "
                    f"{sql_literal(write.format(a=''))});")
            base = "the guest itself or the tenant root"
        elif mark == "own-row":
            pc = "principal_id" if "principal_id" in has else None
            sc = "subject_id" if "subject_id" in has else None
            if not (pc or sc) or base in ("scope_path", "venue_id"):
                print(f"  ! {t}: x-ticvai-rls own-row needs principal_id or subject_id and no scope_path or venue_id; "
                      "the base rule stands")
                continue
            lit = lambda c: sql_literal(c) if c else "NULL"
            call = f"SELECT platform.apply_own_row_rls('{tq(t)}'::regclass, {lit(pc)}, {lit(sc)});"
            write = ("platform.own_row(" + ("{a}principal_id" if pc else "NULL::uuid") + ", "
                     + ("{a}subject_id" if sc else "NULL::uuid") + ")")
            base = "its own principal or guest"
        elif mark == "read-beneath" and base == "venue_id":
            # **Owned above, read below, for a venue_id table** (CHG-R8MIG-026; the storage-sat lane's request 7,
            # ORDERS-MONEY-C33 answer A): a row with no venue is the tenant's and is read at every venue; a venue's row
            # is read and written at that venue, as apply_venue_rls.
            call = (f"SELECT platform.apply_split_rls('{tq(t)}'::regclass, "
                    f"'venue_id IS NULL OR platform.venue_in_scope(venue_id)', 'platform.venue_in_scope(venue_id)');")
        elif mark == "read-beneath":
            if base != "scope_path":
                print(f"  ! {t}: x-ticvai-rls read-beneath needs a scope_path (its rows are owned by {base}); "
                      "use grant-holder-read, or give the schema a scopePath. The base rule stands")
                continue
            call = f"SELECT platform.apply_read_beneath_rls('{tq(t)}'::regclass);"
        elif base == "subject":
            # **A guest still reads its own rows** (MOD audit, 14 October 2026, CHG-MOD-007): opening a subject-owned
            # table to staff grants must not close it to the guest it belongs to, which the grant-holder check
            # alone would (it requires no guest subject on the session).
            call = f"SELECT platform.apply_grant_holder_subject_read_rls('{tq(t)}'::regclass);"
        else:
            call = (f"SELECT platform.apply_grant_holder_read_rls('{tq(t)}'::regclass, "
                    f"{sql_literal(write.format(a=''))});")
        split_mark[t] = (mark, base)
        split_calls[t] = (call, f"x-ticvai-rls: {mark}, written by {base} "
                                f"({(marks.get(t) or {}).get('schema') or 'TABLE_RLS'})")
        split_write[t] = write.format(a="{a}.")
        split_depth[t] = 0
    # A child the parent rule would not pick, because its split parent sits at the tenant root (SPLIT_CHILDREN).
    for t, col in sorted(SPLIT_CHILDREN.items()):
        own = [o for o in owners.get(t, []) if o[0] == col]
        if t not in real or t in protected:
            continue
        if not own or own[0][1] not in split_write:
            print(f"  ! SPLIT_CHILDREN names {t}.{col}, which is not a NOT NULL declared reference to a table "
                  "marked x-ticvai-rls; the table keeps its base rule")
            continue
        by_parent.append((t, col, own[0][1], own[0][2]))
        protected[t] = "parent"
    # A child of a split row follows it for reading only: its writes take the parent's write check, down the chain.
    for i, (t, col, par, key, *_rest) in enumerate(list(by_parent)):
        if par not in split_write:
            continue
        d = split_depth[par] + 1
        by_parent[i] = (t, col, par, key, split_write[par].format(a="parent_row"))
        # **A parent a guest may read does not open its children to every guest** (CHG-R8MIG-026; the storage-sat lane's
        # request 7): marketing.badge is signed-in-read, and marketing.customer_badge followed it for reading, so any
        # guest would have read every customer's awards. Under such a parent (signed-in-read, or read-beneath on
        # venue_id) a child is read by staff where the parent is visible, by a guest only for its own subject
        # (customer_id or subject_id), and written where the parent may be written.
        pm = split_mark.get(par)
        if pm and (pm[0] == "signed-in-read" or (pm[0] == "read-beneath" and pm[1] == "venue_id")):
            ccols = {c_["column"] for c_ in cols.get(t, [])}
            subj = "customer_id" if "customer_id" in ccols else ("subject_id" if "subject_id" in ccols else None)
            link = f"pr.{q(key)} = {tq(t)}.{q(col)}"
            wr = f"EXISTS (SELECT 1 FROM {tq(par)} pr WHERE {link} AND ({split_write[par].format(a='pr')}))"
            rd = f"(platform.grant_holder() AND EXISTS (SELECT 1 FROM {tq(par)} pr WHERE {link}))"
            if subj:
                rd += f" OR platform.own_row(NULL::uuid, {q(subj)})"
            by_parent[i] = (t, col, par, key, split_write[par].format(a="parent_row"), rd, wr)
        alias = f"p{d}"
        split_write[t] = (f"EXISTS (SELECT 1 FROM {tq(par)} {alias} WHERE {alias}.{q(key)} = {{a}}.{q(col)} AND ("
                          + split_write[par].format(a=alias) + "))")
        split_depth[t] = d
    n_split_parent = sum(1 for e in by_parent if len(e) > 4)

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

    n_subject_rls, n_tenant_rls, n_append_rls = [0], [0], [0]
    # **An APPEND_AUDIT table that another rule already protects is not silently left to it**: the list
    # names a decision about who may append, and a scope column added later would undo it unseen.
    for t in sorted(APPEND_AUDIT):
        if t in real and (t in protected or t in venue_only):
            print(f"  ! {t} is in APPEND_AUDIT but protected by another rule; its append policy is not applied")
    unscoped_all = [t for t in sorted(real)
                    if t not in protected and t not in venue_only and t != SCOPE_TABLE]
    # **A child whose parent is in another deployable** (ADAM CR-108, CHG-RSF-001): its host cannot read the parent
    # with its own grants (DB-ROLES), so its policy asks platform.visible_parent_ids. The deployables are the authored
    # boundary in handoff/service-decomposition.json.
    services = (json.loads((ROOT / "handoff" / "service-decomposition.json").read_text(encoding="utf-8"))
                .get("services") or {})
    dep_of_schema = {sc: v.get("deployable") for v in services.values() for sc in v.get("schemas") or []}
    across = {t for t, _c, par, *_r in by_parent
              if dep_of_schema.get(t.split(".", 1)[0]) and dep_of_schema.get(par.split(".", 1)[0])
              and dep_of_schema[t.split(".", 1)[0]] != dep_of_schema[par.split(".", 1)[0]]}
    for db in ("tenant", CONTROL):
        mine = [t for t in scoped if area(t.split(".")[0]) == db and t not in split_calls]
        vmine = [t for t in venue_only if area(t.split(".")[0]) == db and t not in split_calls]
        pmine = [p for p in by_parent if area(p[0].split(".")[0]) == db]
        umine = [(t, why_unscoped(t)) for t in unscoped_all if area(t.split(".")[0]) == db]
        smine, tmine, amine = [], [], []
        if db == "tenant" and SCOPE_TABLE in real:
            for t, why in umine:
                if t in split_calls:
                    continue
                if t in APPEND_AUDIT:
                    amark = (marks.get(t) or {}).get("rls")
                    acol = APPEND_AUDIT_MARKS.get(amark) if amark else None
                    if amark and not acol:
                        print(f"  ! {t}: x-ticvai-rls {amark!r} on an append-only trail is not one of "
                              f"{', '.join(APPEND_AUDIT_MARKS)}; the append policy stands")
                    if acol and not any(c["column"] == acol for c in cols[t]):
                        print(f"  ! {t}: x-ticvai-rls {amark} needs a {acol} column; the append policy stands")
                        acol = None
                    amine.append((t, why, acol))
                elif any(c["column"] == "subject_id" for c in cols[t]):
                    smine.append((t, why))
                else:
                    tmine.append((t, why))
            umine = []
            n_subject_rls[0] += len(smine)
            n_tenant_rls[0] += len(tmine)
            n_append_rls[0] += len(amine)
        total = len(by_schema.get(CONTROL) or []) if db == CONTROL else n_tenant_tables
        files[f"{db}/920-row-level-security.sql"] = rls_file(
            db, mine, vmine, pmine, umine, total,
            has_scope_table=(SCOPE_TABLE in real and db == "tenant"),
            shared={t: c for t, c in shared_scope.items() if t in mine},
            by_subject=smine, tenant_only=tmine, append_audit=amine,
            split=[(t, c, w) for t, (c, w) in sorted(split_calls.items()) if area(t.split(".")[0]) == db],
            across=across)

    # **A deployable's role reads a table another deployable owns, where the lead granted it** (ADAM CR-196, option B,
    # decided 21 October 2026; CHG-R9CR-005; ADR-0055 rule 4 and DB-ROLES as amended). The grants are the `reads` of
    # docs/active/cross-deployable-writes.yaml, appended to the tenant row-level security file, so the forward
    # migration carries them to databases already built. Each is guarded on the role and the table existing: a
    # database built without DB-ROLES' roles, or before the table, is left as it is. Row-level security still
    # applies to every row the role reads.
    files["tenant/920-row-level-security.sql"] = (files["tenant/920-row-level-security.sql"].rstrip("\n") + "\n"
                                                  + deployable_read_grants())

    # ADAM CR-180 (CHG-R10ID-006): the one function that ends a principal's sessions everywhere, written beside the
    # policies it works within; the forward migration carries it (CREATE OR REPLACE) to databases already built.
    if all(t in cols for t in ("identity.session", "identity.refresh_token", "identity.principal")):
        files["tenant/920-row-level-security.sql"] = (files["tenant/920-row-level-security.sql"].rstrip("\n") + "\n"
                                                      + END_PRINCIPAL_SESSIONS_SQL)

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

    if a.apply:
        # `records` one table to a line (CHG-R10TEN-014): a column per line would add some 70,000 lines to the file.
        _recs = ddl_records(files)
        _rec_text = ("{\n" + ",\n".join(f"  {json.dumps(t_)}: {json.dumps(r_, ensure_ascii=False)}"
                                         for t_, r_ in _recs.items()) + "\n }") if _recs else "{}"
        DDL_TYPES_FILE.write_text(json.dumps({
            "note": "Derived by tools/derive-ddl.py. Do not hand-edit. The type each column takes in the DDL this run "
                    "generates (ADR-0056 one id type, numeric(18,4)), under the names the tables and columns have now, "
                    "including those renamed after r1 whose rename is still a forward migration to write "
                    "(handoff/migration-review.md). Read by build-schema-workbook.py for the Columns sheet (CR-067). "
                    "`records` is the rest of each table's record from the same DDL: its columns in order with "
                    "NOT NULL, its primary key, its declared keys and its row-level-security helper (CR-092).",
            "tables": {t: dict(sorted(c.items())) for t, c in sorted(DDL_TYPES.items())},
            "records": "@RECORDS@",
        }, indent=1, ensure_ascii=False).replace('"@RECORDS@"', _rec_text) + "\n", encoding="utf-8")
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
    for t, (cols, par, took) in sorted(OWNER_UNDECIDED.items()):
        print(f"  ! {t}: two keys to {par} ({', '.join(cols)}), owner not decided in ROW_OWNER; follows {took} "
              "for now (listed in migration-review.md)")
    print(f"  row-level security: {len(scoped)} by scope_path · {len(venue_only)} carry venue_id · "
          f"{len(by_parent)} through their owner · {n_subject_rls[0]} by subject · "
          f"{n_tenant_rls[0]} tenant root only · {n_append_rls[0]} append-only audit · "
          f"{len(split_calls)} read beneath or by any grant holder (+{n_split_parent} children) · "
          f"{len(unscoped_all) - n_subject_rls[0] - n_tenant_rls[0] - n_append_rls[0] - len(set(unscoped_all) & set(split_calls))} with no policy")
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
