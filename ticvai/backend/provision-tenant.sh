#!/usr/bin/env bash
# Provision one tenant database on one instance of one cell, and register it.
# **Derived by tools/derive-ddl.py. Do not hand-edit.**
#
# ADR-0038: a cell is a region and holds many tenants, each in its own database.
# ADR-0039: one database per tenant, and the database is the unit of provisioning, migration,
#           backup and destruction.
# ADR-0042: the address is the cell and the instance (control.cell_tenant.instance_id, required from
#           the first row). **Placement is the caller's**: the provisioning operation picks the live
#           instance with the most headroom, or the tenant's pinned one, and runs this on that host
#           (PGHOST). This script refuses an instance that is not live in the cell it names.
#
# **The database name does not encode the region.** The instance already is the region, and a
# name that repeats it is a name that can contradict it.
#
# **Provisioning is triggered by verification, not by application.**
# control.onboarding_application says it: nothing is provisioned until verification passes,
# because an unverified application that provisions a cell is a cell somebody has to clean up.
# This script is the step after that check, not instead of it: the control.tenant row must exist.
#
# Usage: TICVAI_CELL=<cell name> TICVAI_INSTANCE=<instance name> provision-tenant.sh <tenant-slug> <tenant-uuid>
set -euo pipefail

SLUG="${1:?tenant slug required}"
TENANT_ID="${2:?tenant uuid required: a database is registered when it is created, never later}"
: "${TICVAI_CELL:?TICVAI_CELL (the cell name in control.cell) required}"
: "${TICVAI_INSTANCE:?TICVAI_INSTANCE (the instance name in control.cell_instance) required}"
: "${PGHOST:=postgres}"
: "${PGUSER:=ticvai}"
: "${CONTROL_DB:=control}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "$SLUG" in
  ''|*[!a-z0-9_-]*) echo "refused: tenant slug '$SLUG' is not lower-case letters, digits, '-' or '_'" >&2; exit 1 ;;
esac

# UUIDv7 (ADR-0056): ids are minted here, never in SQL.
uuid7() {
  local hex rnd
  hex="$(printf '%012x' "$(( $(date +%s) * 1000 ))")"
  rnd="$(od -An -N10 -tx1 /dev/urandom | tr -d ' \n')"
  printf '%s-%s-7%s-%x%s-%s\n' "${hex:0:8}" "${hex:8:4}" "${rnd:0:3}" \
    "$(( (0x${rnd:3:1} & 0x3) | 0x8 ))" "${rnd:4:3}" "${rnd:7:12}"
}

# 0. **Everything this needs exists before anything is created.** A failure after createdb leaves a
#    database nothing knows about, and a re-run is then refused by step 1.
PLACE="$(psql -v ON_ERROR_STOP=1 -tA -F ' ' -d "$CONTROL_DB" -v tenant_id="$TENANT_ID" -v cell="$TICVAI_CELL" \
         -v instance="$TICVAI_INSTANCE" <<'SQL'
  SELECT c.id, i.id
    FROM control.tenant t
    JOIN control.cell c ON c.name = :'cell' AND c.status = 'active'
    JOIN control.cell_instance i ON i.cell_id = c.id AND i.name = :'instance' AND i.status = 'live'
   WHERE t.id = :'tenant_id'
     AND NOT EXISTS (SELECT 1 FROM control.cell_tenant ct
                      WHERE ct.tenant_id = t.id AND ct.status <> 'dropped');
SQL
)"
CELL_ID="${PLACE%% *}"
INSTANCE_ID="${PLACE#* }"
if [ -z "$PLACE" ] || [ -z "$CELL_ID" ] || [ "$INSTANCE_ID" = "$PLACE" ]; then
  echo "refused: tenant $TENANT_ID must exist in control.tenant with no live registration, cell '$TICVAI_CELL'" \
       "must be active and instance '$TICVAI_INSTANCE' live in it; nothing was created" >&2
  exit 1
fi

# 1. The database. **Refused rather than reused** - provisioning over a live tenant is the one
#    mistake in this script that cannot be undone.
EXISTS="$(psql -tA -d "$CONTROL_DB" -v slug="$SLUG" <<'SQL'
  SELECT 1 FROM pg_database WHERE datname = :'slug';
SQL
)"
if [ -n "$EXISTS" ]; then
  echo "refused: database $SLUG already exists" >&2
  exit 1
fi
createdb "$SLUG"

# 2a. **The types the frozen r1 baseline names and no file creates** (CHG-R12DB-001; CHG-R6-001, ADAM CR-001).
#     Created as domains over the type CHG-R6-001 decided, with its CHECK, so the baseline applies as written;
#     the forward migration then makes each column that type with its named CHECK and drops the domain.
#     Derived from the baseline at r1 (tools/derive-ddl.py FROZEN_TYPES_MARK); check-ddl-conventions
#     D-PROVISION-TYPE fails on a type a provisioned file uses before a step creates it.
psql -v ON_ERROR_STOP=1 -d "$SLUG" <<'SQL' >/dev/null
CREATE SCHEMA IF NOT EXISTS pii;
CREATE DOMAIN pii.contact_kind AS text CHECK (VALUE IN ('email', 'mobile', 'phone', 'whatsapp', 'postal'));
CREATE DOMAIN pii.subject_kind AS text CHECK (VALUE IN ('guest', 'employee', 'contact', 'applicant'));
SQL

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
#     path first (set_config(..., true) is SET LOCAL); without it only a superuser could write the row, and on a
#     managed server provisioning would stop after createdb.
# **The label is the tenant's id** (r13 system review finding C-05, CHG-R14H-002): `t_` and the uuid's 32 hex digits,
#     one label per tenant by construction. The slug made a label was lossy (`acme-1` and `acme_1` both gave
#     `t_acme_1`), and a cell holds many tenants. A database with no tenant id (a local one, never registered) keeps
#     the slug's label.
if [ -n "$TENANT_ID" ]; then
  ROOT_PATH="t_$(printf '%s' "$TENANT_ID" | tr '[:upper:]' '[:lower:]' | tr -d -c '0-9a-f')"
else
  ROOT_PATH="t_$(printf '%s' "$SLUG" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_' '_')"
fi
psql -v ON_ERROR_STOP=1 -d "$SLUG" -v scope_id="$(uuid7)" -v root_path="$ROOT_PATH" -v code="${ROOT_PATH#t_}" \
     -v slug="$SLUG" <<'SQL' >/dev/null
  BEGIN;
  SELECT set_config('ticvai.scope_paths', :'root_path', true);
  INSERT INTO platform.scope (id, level, parent_id, path, code, name, is_active)
  VALUES (:'scope_id', 'tenant', NULL, :'root_path', :'code', :'slug', true);
  COMMIT;
SQL

# 3. The row. **A database with no row in control.cell_tenant is a database nothing knows
#    about** - it will not be migrated, backed up or billed, and it will be found by somebody
#    reading pg_database rather than by the control plane. Exactly one row, or this fails.
REGISTERED="$(psql -v ON_ERROR_STOP=1 -tA -d "$CONTROL_DB" -v id="$(uuid7)" -v cell_id="$CELL_ID" \
              -v instance_id="$INSTANCE_ID" -v tenant_id="$TENANT_ID" -v slug="$SLUG" \
              -v root_path="$ROOT_PATH" <<'SQL'
  INSERT INTO control.cell_tenant (id, cell_id, tenant_id, instance_id, database_name, status,
                                   provisioned_at, root_scope_path)
  VALUES (:'id', :'cell_id', :'tenant_id', :'instance_id', :'slug', 'live', now(), :'root_path')
  RETURNING id;
SQL
)"
if [ "$(printf '%s\n' "$REGISTERED" | grep -c .)" != 1 ]; then
  echo "failed: $SLUG was created and control.cell_tenant did not take its row; drop it before a re-run" >&2
  exit 1
fi

echo "provisioned $SLUG on $TICVAI_CELL/$TICVAI_INSTANCE (registration $REGISTERED)"
