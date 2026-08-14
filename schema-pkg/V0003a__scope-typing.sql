-- =============================================================================
-- V0003a — Level-typed scope references, and the tenant projection
--
-- Two defects, both found by asking why `venue_id` had no table.
--
-- 1. THE MASTER IS scope_node, AND THAT IS CORRECT.
--
--    There is no `venue` table because the hierarchy is one table holding seven
--    levels. That is deliberate: the ltree path in scope_node is what every RLS
--    policy evaluates, and ancestor and descendant queries across arbitrary
--    depth need one table, not seven joined ones. Splitting tenant, region and
--    venue into separate masters would mean in_scope() could not be written.
--
--    Level-specific attributes already hang off it — region_settings (V0001) and
--    venue_settings (V0003) — which is the right shape: shared identity and
--    hierarchy in one place, differing attributes in their own.
--
-- 2. BUT NOTHING ENFORCED THE LEVEL.
--
--    `venue_id uuid` appeared on 48 tables with no foreign key at all. Not one
--    of them prevented pointing at a workstation, a department, or a row that
--    does not exist. The type said uuid; the intent said venue; nothing checked.
--
--    This migration makes it enforceable. scope_node gains UNIQUE (id, level),
--    and a table wanting a venue carries a generated column pinned to 'venue'
--    and a composite foreign key. Postgres then refuses a reference to anything
--    that is not a venue — no trigger, no application check, no hope.
--
-- 3. AND TENANT WAS NOT ADDRESSABLE INSIDE A CELL.
--
--    control.tenant lives in the Control Plane database, outside every cell. A
--    cell could not resolve its own tenant's name, status or plan without a
--    cross-database call it is not permitted to make. A read-only projection
--    fixes that, fed by the Control Plane.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Make the level referenceable.
-- -----------------------------------------------------------------------------
ALTER TABLE platform.scope_node
    ADD CONSTRAINT scope_node_id_level_unique UNIQUE (id, level);

COMMENT ON CONSTRAINT scope_node_id_level_unique ON platform.scope_node IS
  'Redundant on its own — id is already the primary key. It exists so a composite '
  'foreign key can pin a reference to a level: FOREIGN KEY (venue_id, venue_level) '
  'REFERENCES scope_node (id, level). Without it, level typing is a comment.';

-- The pattern, applied to the tables that already carry a scope reference.
-- Every future table with venue_id gets the same two lines.
--
--     venue_level platform.scope_level GENERATED ALWAYS AS ('venue') STORED,
--     FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)

ALTER TABLE platform.venue_settings
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT venue_settings_is_venue
        FOREIGN KEY (scope_node_id, venue_level)
        REFERENCES platform.scope_node (id, level);

COMMENT ON COLUMN platform.venue_settings.venue_level IS
  'Always the literal venue. Exists solely to make the composite foreign key '
  'possible, which is what turns "this should be a venue" into something the '
  'database refuses to break. The V0003 trigger that asserted the same thing is '
  'now redundant and is dropped below.';

DROP TRIGGER IF EXISTS venue_settings_level ON platform.venue_settings;

ALTER TABLE platform.region_settings
    ADD COLUMN region_level platform.scope_level
        GENERATED ALWAYS AS ('region'::platform.scope_level) STORED,
    ADD CONSTRAINT region_settings_is_region
        FOREIGN KEY (scope_node_id, region_level)
        REFERENCES platform.scope_node (id, level);

ALTER TABLE platform.workstation
    ADD COLUMN workstation_level platform.scope_level
        GENERATED ALWAYS AS ('workstation'::platform.scope_level) STORED,
    ADD CONSTRAINT workstation_is_workstation
        FOREIGN KEY (scope_node_id, workstation_level)
        REFERENCES platform.scope_node (id, level);

DROP TRIGGER IF EXISTS workstation_level ON platform.workstation;

-- Tables carrying venue_id as a plain attribute rather than as their own scope.
ALTER TABLE platform.workstation
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT workstation_venue_is_venue
        FOREIGN KEY (venue_id, venue_level)
        REFERENCES platform.scope_node (id, level);

ALTER TABLE platform.sale_board
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT sale_board_venue_is_venue
        FOREIGN KEY (venue_id, venue_level)
        REFERENCES platform.scope_node (id, level);

ALTER TABLE platform.device
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT device_venue_is_venue
        FOREIGN KEY (venue_id, venue_level)
        REFERENCES platform.scope_node (id, level);

-- The two partitioned hot tables. Postgres allows an outgoing foreign key from a
-- partitioned table since 12, and the check is a unique-index lookup — a few
-- microseconds per insert against a table that already writes a row per scan.
-- Worth it: a scan_event pointing at a venue that does not exist is an admission
-- nobody can attribute afterwards.
ALTER TABLE orders.sales_order
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT sales_order_venue_is_venue
        FOREIGN KEY (venue_id, venue_level)
        REFERENCES platform.scope_node (id, level);

ALTER TABLE access.scan_event
    ADD COLUMN venue_level platform.scope_level
        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    ADD CONSTRAINT scan_event_venue_is_venue
        FOREIGN KEY (venue_id, venue_level)
        REFERENCES platform.scope_node (id, level);

-- platform.outbox is deliberately exempt. It is written inside the same
-- transaction as the state change it records, and a foreign key failure there
-- would roll back a sale for a bookkeeping reason. Its venue_id is copied from a
-- row that has already been validated.

-- -----------------------------------------------------------------------------
-- 2. Outlets. Referenced nine times by F&B, retail and games; defined nowhere.
-- -----------------------------------------------------------------------------
CREATE TYPE platform.outlet_kind AS ENUM (
    'shop', 'restaurant', 'bar', 'cafe', 'kiosk', 'gameFloor', 'ticketOffice', 'mobile'
);

CREATE TABLE platform.outlet (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id            uuid NOT NULL,
    venue_level         platform.scope_level
                        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    scope_path          ltree NOT NULL,
    code                text NOT NULL,
    name                text NOT NULL,
    kind                platform.outlet_kind NOT NULL,
    zone                text,
    stock_location_id   uuid,
    cost_center_id      uuid,
    opening_hours       jsonb NOT NULL DEFAULT '[]'::jsonb,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT outlet_code_unique UNIQUE (venue_id, code),
    FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)
);

COMMENT ON TABLE platform.outlet IS
  'A point of sale within a venue — a shop, a restaurant, a bar. F&B, retail and '
  'games all key off it, and until now it was referenced by all three and defined '
  'by none. An outlet is not a workstation: several workstations sit in one '
  'outlet, and the outlet carries the menu, the stock location and the revenue '
  'attribution.';

CREATE INDEX outlet_venue ON platform.outlet (venue_id) WHERE is_active;
CREATE INDEX outlet_gist  ON platform.outlet USING gist (scope_path);

ALTER TABLE platform.outlet ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.outlet FORCE ROW LEVEL SECURITY;
CREATE POLICY outlet_scope ON platform.outlet
    USING (platform.in_scope(scope_path));

-- -----------------------------------------------------------------------------
-- 3. Tenant projection. Read-only inside the cell.
-- -----------------------------------------------------------------------------
CREATE TABLE platform.tenant (
    id                  uuid PRIMARY KEY,
    code                text NOT NULL,
    name                text NOT NULL,
    status              text NOT NULL
        CHECK (status IN ('onboarding','active','suspended','terminating','terminated')),
    suspension_mode     text
        CHECK (suspension_mode IN ('readOnly','noNewSales','fullLockout')),
    plan_code           text,
    licensed_modules    text[] NOT NULL DEFAULT '{}',
    home_region_id      uuid REFERENCES platform.scope_node (id),
    projected_at        timestamptz NOT NULL DEFAULT now(),
    source_version      text,
    CONSTRAINT tenant_code_unique UNIQUE (code)
);

COMMENT ON TABLE platform.tenant IS
  'A read-only projection of control.tenant, which lives in the Control Plane '
  'database outside every cell. A cell could not previously resolve its own '
  'tenant name, status or licensed modules without a cross-database call it is '
  'not permitted to make.

Written only by the Control Plane through the projection channel. Nothing in the '
  'cell updates it, and a stale projection is visible through projected_at rather '
  'than being silently wrong.';

COMMENT ON COLUMN platform.tenant.licensed_modules IS
  'Denormalised from the licence position so module enablement can be checked '
  'without leaving the cell. The Control Plane remains authoritative — this is a '
  'cache with a timestamp, not a second source of truth.';

COMMENT ON COLUMN platform.tenant.suspension_mode IS
  'Access validation continues under every mode. A commercial dispute must not '
  'strand guests at a gate holding valid tickets.';

CREATE INDEX tenant_status ON platform.tenant (status);

-- No RLS. A cell holds exactly one tenant, so there is nothing to isolate from —
-- and a policy here would suggest otherwise to whoever reads it next.
COMMENT ON INDEX platform.tenant_status IS
  'A cell holds one tenant. This table has one row in practice; the index exists '
  'for the suspended-tenant check on the hot path, not for selectivity.';

-- -----------------------------------------------------------------------------
-- 4. A view that answers "what is this scope node, really".
-- -----------------------------------------------------------------------------
CREATE VIEW platform.scope_resolved AS
SELECT
    n.id,
    n.level,
    n.code,
    n.name,
    n.path,
    n.is_active,
    (SELECT a.id   FROM platform.scope_node a WHERE a.path @> n.path AND a.level = 'tenant') AS tenant_id,
    (SELECT a.id   FROM platform.scope_node a WHERE a.path @> n.path AND a.level = 'region') AS region_id,
    (SELECT a.id   FROM platform.scope_node a WHERE a.path @> n.path AND a.level = 'venue')  AS venue_id,
    (SELECT a.name FROM platform.scope_node a WHERE a.path @> n.path AND a.level = 'venue')  AS venue_name,
    r.currency_code,
    r.currency_scale
FROM platform.scope_node n
LEFT JOIN platform.region_settings r
       ON r.scope_node_id = (SELECT a.id FROM platform.scope_node a
                             WHERE a.path @> n.path AND a.level = 'region');

COMMENT ON VIEW platform.scope_resolved IS
  'Flattens the hierarchy so a caller can ask "which venue and region is this '
  'node in, and what currency does it trade in" without writing an ltree ancestor '
  'query each time. Reporting and the AI layer are the intended consumers.

Not for the transaction path — the correlated subqueries are fine for a handful of '
  'rows and wrong for a scan event.';

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0003a', 'scope-typing-outlet-tenant', 'set-by-runner');

-- =============================================================================
-- ROLLBACK
-- =============================================================================
-- DROP VIEW IF EXISTS platform.scope_resolved;
-- DROP TABLE IF EXISTS platform.tenant;
-- DROP TABLE IF EXISTS platform.outlet;
-- DROP TYPE IF EXISTS platform.outlet_kind;
-- ALTER TABLE platform.device DROP CONSTRAINT IF EXISTS device_venue_is_venue;
-- ALTER TABLE platform.device DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE platform.sale_board DROP CONSTRAINT IF EXISTS sale_board_venue_is_venue;
-- ALTER TABLE platform.sale_board DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE platform.workstation DROP CONSTRAINT IF EXISTS workstation_venue_is_venue;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE platform.workstation DROP CONSTRAINT IF EXISTS workstation_is_workstation;
-- ALTER TABLE platform.workstation DROP COLUMN IF EXISTS workstation_level;
-- ALTER TABLE platform.region_settings DROP CONSTRAINT IF EXISTS region_settings_is_region;
-- ALTER TABLE platform.region_settings DROP COLUMN IF EXISTS region_level;
-- ALTER TABLE platform.venue_settings DROP CONSTRAINT IF EXISTS venue_settings_is_venue;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE access.scan_event DROP CONSTRAINT IF EXISTS scan_event_venue_is_venue;
-- ALTER TABLE access.scan_event DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE orders.sales_order DROP CONSTRAINT IF EXISTS sales_order_venue_is_venue;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS venue_level;
-- ALTER TABLE platform.scope_node DROP CONSTRAINT IF EXISTS scope_node_id_level_unique;
-- DELETE FROM platform.schema_version WHERE version = 'V0003a';
--
-- Note: dropping the level typing restores the V0003 triggers' absence, not the
-- triggers themselves. Re-applying V0003 after this rollback would recreate them.
