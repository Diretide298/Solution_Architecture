#!/usr/bin/env bash
# Provision this cell's tenant databases, from inside the postgres container's initdb pass.
# **Derived by tools/derive-ddl.py. Do not hand-edit.**
#
# **The instance is the cell and the database is the tenant** (ADR-0038). initdb has just applied
# the control database; this creates the tenant databases the scenario says are in this region.
#
# TICVAI_TENANTS is a comma-separated list of `slug:uuid` pairs (`acme:3f2a...`). The uuid is required:
# provisioning registers every database in control.cell_tenant, and a database nothing knows about
# is worse than a database that is missing.
#
# **A compose stack is its own control plane** (CHG-R14J-001). Nothing else registers its cell, its
# instance or its tenants, so this does, once, before provisioning: the cell TICVAI_CELL (default
# `local`), its one instance TICVAI_INSTANCE (default `local-1`, live, primary) and a control.tenant
# row per entry. In a real cell those rows come from onboarding (verification, then the provisioning
# operation, ADR-0039 and ADR-0042), and this script is not run there.
set -euo pipefail

: "${TICVAI_TENANTS:=}"
if [ -z "$TICVAI_TENANTS" ]; then
  echo "no TICVAI_TENANTS set - control database only, no tenants in this cell" >&2
  exit 0
fi

export CONTROL_DB="${POSTGRES_DB:-control}"
export PGUSER="${POSTGRES_USER:-ticvai}"
export TICVAI_CELL="${TICVAI_CELL:-local}"
export TICVAI_INSTANCE="${TICVAI_INSTANCE:-local-1}"
: "${TICVAI_COUNTRY:=AE}"

# UUIDv7 (ADR-0056): 48 bits of Unix milliseconds, the version, then random bits with the RFC 9562 variant.
uuid7() {
  local hex rnd
  hex="$(printf '%012x' "$(( $(date +%s) * 1000 ))")"
  rnd="$(od -An -N10 -tx1 /dev/urandom | tr -d ' \n')"
  printf '%s-%s-7%s-%x%s-%s\n' "${hex:0:8}" "${hex:8:4}" "${rnd:0:3}" \
    "$(( (0x${rnd:3:1} & 0x3) | 0x8 ))" "${rnd:4:3}" "${rnd:7:12}"
}

psql -v ON_ERROR_STOP=1 -d "$CONTROL_DB" -v cell_id="$(uuid7)" -v region_id="$(uuid7)" \
     -v instance_id="$(uuid7)" -v cell="$TICVAI_CELL" -v instance="$TICVAI_INSTANCE" \
     -v country="$TICVAI_COUNTRY" <<'SQL' >/dev/null
  INSERT INTO control.cell (id, name, region_id, country_code, tier, status, provisioned_at)
  VALUES (:'cell_id', :'cell', :'region_id', :'country', 'shared', 'active', now())
  ON CONFLICT DO NOTHING;
  INSERT INTO control.cell_instance (id, cell_id, name, status, role, created_at)
  VALUES (:'instance_id', (SELECT id FROM control.cell WHERE name = :'cell'), :'instance', 'live', 'primary', now())
  ON CONFLICT DO NOTHING;
SQL

IFS=',' read -ra ENTRIES <<< "$TICVAI_TENANTS"
for entry in "${ENTRIES[@]}"; do
  entry="$(echo "$entry" | tr -d '[:space:]')"
  [ -z "$entry" ] && continue
  slug="${entry%%:*}"
  uuid=""
  case "$entry" in *:*) uuid="${entry#*:}";; esac
  if [ -z "$uuid" ]; then
    echo "refused: $slug has no tenant uuid in TICVAI_TENANTS (slug:uuid); nothing can register it" >&2
    exit 1
  fi
  psql -v ON_ERROR_STOP=1 -d "$CONTROL_DB" -v tenant_id="$uuid" -v slug="$slug" <<'SQL' >/dev/null
    INSERT INTO control.tenant (id, code, name, status, created_at, activated_at)
    VALUES (:'tenant_id', :'slug', :'slug', 'active', now(), now())
    ON CONFLICT DO NOTHING;
SQL
  /opt/ticvai/provision-tenant.sh "$slug" "$uuid"
done

echo "provisioned ${#ENTRIES[@]} tenant database(s) in cell $TICVAI_CELL, instance $TICVAI_INSTANCE"
