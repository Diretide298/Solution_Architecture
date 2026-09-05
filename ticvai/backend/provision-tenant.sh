#!/usr/bin/env bash
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
