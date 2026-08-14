-- =============================================================================
-- V0001 — Cell baseline
--
-- Applied to every tenant database in a cell. Establishes:
--   * module schemas with per-module roles
--   * the ltree scope hierarchy (Tenant -> ... -> Workstation)
--   * row-level security keyed off a session variable
--   * venue-partitioned hot tables
--   * the transactional outbox
--
-- Project Direction references are inline. Do not "simplify" the RLS policies —
-- the hierarchy diagram asserts "no cross-venue data access unless explicitly
-- permitted", and API-layer enforcement alone fails the first time somebody
-- writes a report query directly against the database.
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- pgvector is the fallback vector store while Qdrant residency is unconfirmed
-- (CF-20). Enabled here so the fallback needs no separate migration.
CREATE EXTENSION IF NOT EXISTS vector;

-- -----------------------------------------------------------------------------
-- Schemas. One per module (Direction: schema-per-module, database-per-tenant).
-- -----------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS platform;   -- shared reference data, scope tree
CREATE SCHEMA IF NOT EXISTS identity;
CREATE SCHEMA IF NOT EXISTS catalogue;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS access;
CREATE SCHEMA IF NOT EXISTS sync;
CREATE SCHEMA IF NOT EXISTS ledger;
CREATE SCHEMA IF NOT EXISTS pii;        -- separately erasable; see note below

COMMENT ON SCHEMA pii IS
  'Personal data lives here, referenced from ledger by opaque subject id. '
  'Reconciles the append-only ledger decision (12 Aug 2026) with PDPL/GDPR '
  'erasure obligations: erasure deletes the pii row, the ledger keeps its '
  'integrity and its 7-year audit trail with an orphaned but valid reference.';

-- -----------------------------------------------------------------------------
-- Scope hierarchy. Seven levels, materialised as ltree.
-- Recursive CTEs per request will not survive 70+ venues at 1,000 req/s.
-- -----------------------------------------------------------------------------
CREATE TYPE platform.scope_level AS ENUM (
    'tenant', 'brand', 'region', 'venue', 'department', 'sub_department', 'workstation'
);

CREATE TABLE platform.scope_node (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    level           platform.scope_level NOT NULL,
    parent_id       uuid REFERENCES platform.scope_node (id),
    path            ltree NOT NULL,
    code            text  NOT NULL,
    name            text  NOT NULL,
    is_active       boolean NOT NULL DEFAULT true,
    created_at      timestamptz NOT NULL DEFAULT now(),
    updated_at      timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT scope_node_path_unique UNIQUE (path)
);

CREATE INDEX scope_node_path_gist ON platform.scope_node USING gist (path);
CREATE INDEX scope_node_parent    ON platform.scope_node (parent_id);
CREATE INDEX scope_node_level     ON platform.scope_node (level) WHERE is_active;

-- Region owns currency, timezone and fiscal calendar — inherited by all venues
-- beneath it (hierarchy diagram, Region Level Settings).
CREATE TABLE platform.region_settings (
    scope_node_id      uuid PRIMARY KEY REFERENCES platform.scope_node (id) ON DELETE CASCADE,
    country_code       char(2) NOT NULL,
    currency_code      char(3) NOT NULL,
    currency_scale     smallint NOT NULL CHECK (currency_scale BETWEEN 0 AND 4),
    time_zone          text NOT NULL,
    date_format        text NOT NULL DEFAULT 'dd/MM/yyyy',
    fiscal_year_start  smallint NOT NULL DEFAULT 1 CHECK (fiscal_year_start BETWEEN 1 AND 12),
    placement          jsonb NOT NULL DEFAULT '{"mode":"shared"}'::jsonb
);

COMMENT ON COLUMN platform.region_settings.currency_scale IS
  'OMR is 3, AED is 2. Money columns are numeric(18,4); scale is carried '
  'explicitly so a 3dp currency is never silently truncated.';

COMMENT ON COLUMN platform.region_settings.placement IS
  'shared | dedicated:{cloud}:{region} | client_hosted:{endpoint}. '
  'A tenant may be mixed across regions (Direction §3.3.5).';

-- -----------------------------------------------------------------------------
-- Row-level security.
-- Services set these per connection, inside the transaction, before any query.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION platform.current_scope_paths()
RETURNS ltree[]
LANGUAGE sql STABLE
AS $$
    SELECT COALESCE(
        string_to_array(current_setting('ticvai.scope_paths', true), ',')::ltree[],
        ARRAY[]::ltree[]
    );
$$;

CREATE OR REPLACE FUNCTION platform.in_scope(target ltree)
RETURNS boolean
LANGUAGE sql STABLE
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM unnest(platform.current_scope_paths()) AS granted
        WHERE target <@ granted
    );
$$;

COMMENT ON FUNCTION platform.in_scope IS
  'True when the target node is at or beneath any granted scope path. '
  'Deny-overrides-allow is resolved once at login in the application layer; '
  'this function enforces the resulting allow set at the data layer.';

-- -----------------------------------------------------------------------------
-- Venue-partitioned hot tables.
-- Partitioning gives data isolation, partition pruning and per-venue archival
-- WITHOUT breaking cross-venue passes, wallets, memberships or consolidated
-- reporting the way separate databases would (Direction §3.3.4).
-- -----------------------------------------------------------------------------
CREATE TABLE orders.sales_order (
    id                  char(26) NOT NULL,              -- ULID, client-generated
    venue_id            uuid     NOT NULL,
    scope_path          ltree    NOT NULL,
    brand_id            uuid     NOT NULL,
    region_id           uuid     NOT NULL,
    channel             text     NOT NULL,
    status              text     NOT NULL,
    currency_code       char(3)  NOT NULL,
    currency_scale      smallint NOT NULL,
    gross_amount        numeric(18,4) NOT NULL,
    tax_amount          numeric(18,4) NOT NULL,
    net_amount          numeric(18,4) NOT NULL,
    subject_id          uuid,                           -- FK into pii, nullable for anonymous
    workstation_id      uuid,
    idempotency_key     char(26) NOT NULL,
    created_at          timestamptz NOT NULL DEFAULT now(),
    recorded_at         timestamptz NOT NULL DEFAULT now(),
    synced_at           timestamptz,
    PRIMARY KEY (id, venue_id)
) PARTITION BY LIST (venue_id);

COMMENT ON COLUMN orders.sales_order.recorded_at IS
  'When the device recorded it. Differs from synced_at for offline sales '
  '(31 Jul 2026: sequential sync with both recorded and synced timestamps).';

CREATE UNIQUE INDEX sales_order_idempotency
    ON orders.sales_order (venue_id, idempotency_key);

CREATE INDEX sales_order_created
    ON orders.sales_order (venue_id, created_at DESC);

ALTER TABLE orders.sales_order ENABLE ROW LEVEL SECURITY;

-- FORCE is essential: without it the table OWNER bypasses every policy, which
-- makes data-layer enforcement decorative for exactly the role most likely to
-- run an ad-hoc query.
ALTER TABLE orders.sales_order FORCE ROW LEVEL SECURITY;

CREATE POLICY sales_order_scope ON orders.sales_order
    USING (platform.in_scope(scope_path));

-- Default partition catches misconfiguration loudly rather than losing rows.
CREATE TABLE orders.sales_order_unassigned
    PARTITION OF orders.sales_order DEFAULT;

-- -----------------------------------------------------------------------------
-- Access control scans. Highest-volume table; most writes arrive batched from
-- venue edge nodes rather than in real time.
-- -----------------------------------------------------------------------------
CREATE TABLE access.scan_event (
    id                  char(26) NOT NULL,
    venue_id            uuid     NOT NULL,
    scope_path          ltree    NOT NULL,
    access_point_id     uuid     NOT NULL,
    ticket_id           char(26),
    media_code          text,
    result              text     NOT NULL,
    deny_reason         text,
    direction           text     NOT NULL,
    operator_id         uuid,
    device_id           uuid,
    recorded_at         timestamptz NOT NULL,
    synced_at           timestamptz,
    PRIMARY KEY (id, venue_id)
) PARTITION BY LIST (venue_id);

CREATE INDEX scan_event_ticket   ON access.scan_event (venue_id, ticket_id);
CREATE INDEX scan_event_recorded ON access.scan_event (venue_id, recorded_at DESC);

ALTER TABLE access.scan_event ENABLE ROW LEVEL SECURITY;
ALTER TABLE access.scan_event FORCE ROW LEVEL SECURITY;
CREATE POLICY scan_event_scope ON access.scan_event USING (platform.in_scope(scope_path));

CREATE TABLE access.scan_event_unassigned PARTITION OF access.scan_event DEFAULT;

-- -----------------------------------------------------------------------------
-- Transactional outbox. Publication is atomic with the state change; a crash
-- between commit and publish must not lose the event.
-- -----------------------------------------------------------------------------
CREATE TABLE platform.outbox (
    id              bigserial PRIMARY KEY,
    event_id        uuid        NOT NULL UNIQUE,
    event_type      text        NOT NULL,
    venue_id        uuid,
    payload         jsonb       NOT NULL,
    occurred_at     timestamptz NOT NULL DEFAULT now(),
    published_at    timestamptz,
    attempts        int         NOT NULL DEFAULT 0,
    last_error      text
);

CREATE INDEX outbox_unpublished
    ON platform.outbox (occurred_at)
    WHERE published_at IS NULL;


-- The outbox carries event payloads, and those payloads carry venue data. Without a
-- policy any authenticated connection could read another venue's events — the same
-- exposure the partitioned tables exist to prevent, through a side door.
--
-- The relay needs every row regardless of scope, so it runs as a dedicated role with
-- BYPASSRLS rather than the table having no policy. A bypass granted to one named role
-- is auditable; an absent policy is not.
ALTER TABLE platform.outbox ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.outbox FORCE ROW LEVEL SECURITY;
CREATE POLICY outbox_scope ON platform.outbox
    USING (venue_id IS NULL OR platform.in_scope(
        (SELECT path FROM platform.scope_node WHERE id = venue_id)));

COMMENT ON POLICY outbox_scope ON platform.outbox IS
  'venue_id NULL means a cell-wide event with no venue to restrict it to. Those are '
  'visible to any principal who can read the outbox at all, which is correct.';

-- -----------------------------------------------------------------------------
-- Schema version register. The migration orchestrator reads this per cell to
-- decide what to apply and to detect drift.
-- -----------------------------------------------------------------------------
CREATE TABLE platform.schema_version (
    version         int         PRIMARY KEY,
    name            text        NOT NULL,
    checksum        text        NOT NULL,
    applied_at      timestamptz NOT NULL DEFAULT now(),
    applied_by      text        NOT NULL DEFAULT current_user,
    duration_ms     int
);

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0001', 'baseline', 'set-by-runner');

-- -----------------------------------------------------------------------------
-- Per-module roles. Each service connects with a role granted access only to
-- its own schema. Boundaries enforced by the database, not by convention.
-- -----------------------------------------------------------------------------
DO $$
DECLARE
    module_name text;
BEGIN
    FOREACH module_name IN ARRAY ARRAY['identity','catalogue','orders','access','sync','ledger']
    LOOP
        EXECUTE format('CREATE ROLE ticvai_%I NOLOGIN', module_name);
        EXECUTE format('GRANT USAGE ON SCHEMA %I TO ticvai_%I', module_name, module_name);
        EXECUTE format('GRANT USAGE ON SCHEMA platform TO ticvai_%I', module_name);
        EXECUTE format(
            'ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT SELECT, INSERT, UPDATE ON TABLES TO ticvai_%I',
            module_name, module_name);
    END LOOP;
END
$$;

-- Reporting connects to a lag-tolerant replica and is granted no write access
-- anywhere. The single most likely cause of a venue spike taking down a tenant
-- is a month-end report running against the primary.
CREATE ROLE ticvai_reporting NOLOGIN;
GRANT USAGE ON SCHEMA platform, orders, catalogue, access, ledger TO ticvai_reporting;

-- =============================================================================
-- ROLLBACK
--
-- The baseline is the floor. Rolling it back destroys the cell, so this exists
-- to be tested against a scratch database in CI, never run against a live one.
-- The runner refuses to apply it where platform.scope_node has rows.
-- =============================================================================
-- DROP TABLE IF EXISTS access.scan_event_unassigned;
-- DROP TABLE IF EXISTS access.scan_event;
-- DROP TABLE IF EXISTS orders.sales_order_unassigned;
-- DROP TABLE IF EXISTS orders.sales_order;
-- DROP TABLE IF EXISTS pii.subject_contact;
-- DROP TABLE IF EXISTS pii.subject;
-- DROP TABLE IF EXISTS platform.outbox;
-- DROP TABLE IF EXISTS platform.region_settings;
-- DROP TABLE IF EXISTS platform.scope_node;
-- DROP TABLE IF EXISTS platform.schema_version;
-- DROP FUNCTION IF EXISTS platform.in_scope(ltree);
-- DROP FUNCTION IF EXISTS platform.current_scope_paths();
-- DROP TYPE IF EXISTS platform.scope_level;
-- DROP SCHEMA IF EXISTS pii, ledger, sync, access, orders, catalogue, identity, platform CASCADE;
-- DELETE FROM platform.schema_version WHERE version = 'V0001';
