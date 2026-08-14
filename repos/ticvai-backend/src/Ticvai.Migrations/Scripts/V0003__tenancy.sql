-- =============================================================================
-- V0003 — Tenancy & Organisation
--
-- Venue settings, workstations, sale boards and the device registry.
--
-- The scope tree itself is in V0001 — it is needed before anything else can
-- reference it. This migration adds what hangs off the venue and workstation
-- levels of that tree.
--
-- A note on workstations. ADR-0002 settled that a workstation is presentation,
-- hardware, till and reporting context — never a source of permission. Nothing
-- in this schema stores a permission against a workstation, and that absence is
-- the enforcement.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Venue settings. Hangs off a scope_node of level 'venue'.
-- -----------------------------------------------------------------------------
CREATE TABLE platform.venue_settings (
    scope_node_id       uuid PRIMARY KEY REFERENCES platform.scope_node (id) ON DELETE CASCADE,
    scope_path          ltree NOT NULL,
    legal_entity_id     uuid,
    address             jsonb NOT NULL DEFAULT '{}'::jsonb,
    latitude            numeric(9,6),
    longitude           numeric(9,6),
    opening_hours       jsonb NOT NULL DEFAULT '[]'::jsonb,
    capacity            integer,
    refund_threshold    numeric(18,4),
    currency_code       char(3),
    variance_threshold  numeric(18,4) NOT NULL DEFAULT 0,
    cash_lift_threshold numeric(18,4),
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now()
    -- Level is enforced by trigger below. A CHECK constraint cannot subquery,
    -- and a constraint that always passes is worse than none — it reads like
    -- enforcement to anyone skimming.
);

COMMENT ON COLUMN platform.venue_settings.refund_threshold IS
  'Above this, a refund needs approval. CF-36: this is venue policy, not a '
  'permission scope — the permission says who may refund, this says when a '
  'second person is involved.';

COMMENT ON COLUMN platform.venue_settings.variance_threshold IS
  'Price variance above this becomes a reviewable exception rather than a '
  'routine posting (CF-38).';

COMMENT ON COLUMN platform.venue_settings.currency_code IS
  'Normally NULL — currency is a region setting and inherited. Populated only '
  'where a venue legitimately differs, which should be rare enough to question.';

CREATE INDEX venue_settings_gist ON platform.venue_settings USING gist (scope_path);

ALTER TABLE platform.venue_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.venue_settings FORCE ROW LEVEL SECURITY;
CREATE POLICY venue_settings_scope ON platform.venue_settings
    USING (platform.in_scope(scope_path));

-- Level enforcement. A CHECK constraint cannot query another table, so this is
-- a trigger — but it is not optional. Venue settings on a region node would be
-- inherited by every venue beneath it, silently.
CREATE OR REPLACE FUNCTION platform.assert_scope_level()
RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    actual platform.scope_level;
    wanted platform.scope_level := TG_ARGV[0]::platform.scope_level;
BEGIN
    SELECT level, path INTO actual, NEW.scope_path
    FROM platform.scope_node WHERE id = NEW.scope_node_id;

    IF actual IS NULL THEN
        RAISE EXCEPTION 'scope_node % not found', NEW.scope_node_id;
    END IF;
    IF actual <> wanted THEN
        RAISE EXCEPTION 'scope_node % is level %, expected %', NEW.scope_node_id, actual, wanted;
    END IF;
    RETURN NEW;
END $$;

CREATE TRIGGER venue_settings_level
    BEFORE INSERT OR UPDATE OF scope_node_id ON platform.venue_settings
    FOR EACH ROW EXECUTE FUNCTION platform.assert_scope_level('venue');

-- -----------------------------------------------------------------------------
-- Workstations. Presentation, hardware and till context. Never authorisation.
-- -----------------------------------------------------------------------------
CREATE TYPE platform.workstation_kind AS ENUM (
    'pos', 'kiosk', 'handheld', 'turnstile', 'backOffice', 'callCentre', 'kitchenDisplay'
);

CREATE TABLE platform.workstation (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    scope_node_id       uuid NOT NULL REFERENCES platform.scope_node (id),
    scope_path          ltree NOT NULL,
    venue_id            uuid NOT NULL,
    code                text NOT NULL,
    name                text NOT NULL,
    kind                platform.workstation_kind NOT NULL,
    sale_board_id       uuid,
    default_channel     text NOT NULL DEFAULT 'pos',
    till_id             text,
    is_shared           boolean NOT NULL DEFAULT true,
    requires_shift      boolean NOT NULL DEFAULT true,
    is_active           boolean NOT NULL DEFAULT true,
    last_seen_at        timestamptz,
    bundle_version      text,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT workstation_code_unique UNIQUE (venue_id, code)
);

COMMENT ON TABLE platform.workstation IS
  'ADR-0002: a workstation determines what is presented and which hardware is '
  'attached. It grants nothing. There is deliberately no permission column here '
  'and there should never be one.';

COMMENT ON COLUMN platform.workstation.bundle_version IS
  'Catalogue bundle currently applied (ADR-0013). Compared against the published '
  'version to detect a terminal running behind — the usual explanation for a '
  'price variance.';

COMMENT ON COLUMN platform.workstation.is_shared IS
  'A shared terminal is used by successive staff across a day; a personal one is '
  'not. Affects shift handover, not authorisation.';

CREATE INDEX workstation_venue ON platform.workstation (venue_id) WHERE is_active;
CREATE INDEX workstation_gist  ON platform.workstation USING gist (scope_path);
CREATE INDEX workstation_stale ON platform.workstation (last_seen_at)
    WHERE is_active;

ALTER TABLE platform.workstation ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.workstation FORCE ROW LEVEL SECURITY;
CREATE POLICY workstation_scope ON platform.workstation
    USING (platform.in_scope(scope_path));

CREATE TRIGGER workstation_level
    BEFORE INSERT OR UPDATE OF scope_node_id ON platform.workstation
    FOR EACH ROW EXECUTE FUNCTION platform.assert_scope_level('workstation');

-- -----------------------------------------------------------------------------
-- Sale boards. The tile layout a terminal presents.
-- -----------------------------------------------------------------------------
CREATE TABLE platform.sale_board (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id            uuid NOT NULL,
    scope_path          ltree NOT NULL,
    code                text NOT NULL,
    name                text NOT NULL,
    kind                text NOT NULL,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    updated_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sale_board_code_unique UNIQUE (venue_id, code)
);

ALTER TABLE platform.sale_board ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.sale_board FORCE ROW LEVEL SECURITY;
CREATE POLICY sale_board_scope ON platform.sale_board
    USING (platform.in_scope(scope_path));

CREATE TABLE platform.sale_board_page (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sale_board_id       uuid NOT NULL REFERENCES platform.sale_board (id) ON DELETE CASCADE,
    name                text NOT NULL,
    sort_order          smallint NOT NULL,
    CONSTRAINT sale_board_page_order UNIQUE (sale_board_id, sort_order)
);

CREATE TABLE platform.sale_board_tile (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    page_id             uuid NOT NULL REFERENCES platform.sale_board_page (id) ON DELETE CASCADE,
    position            smallint NOT NULL,
    kind                text NOT NULL CHECK (kind IN ('product','category','action','spacer')),
    variant_id          uuid,
    label               text,
    colour              char(7),
    image_asset_ref     text,
    CONSTRAINT sale_board_tile_position UNIQUE (page_id, position),
    CONSTRAINT sale_board_tile_product CHECK (kind <> 'product' OR variant_id IS NOT NULL)
);

COMMENT ON CONSTRAINT sale_board_tile_product ON platform.sale_board_tile IS
  'A product tile with no variant is a button that does nothing. Caught here '
  'rather than by a cashier during service.';

-- -----------------------------------------------------------------------------
-- Device registry. The binding a workstation needs at boot.
--
-- Distinct from Device Management (domain 14, workshop-blocked), which covers
-- the estate lifecycle. This is only what a terminal must know to drive its
-- attached hardware.
-- -----------------------------------------------------------------------------
CREATE TYPE platform.device_kind AS ENUM (
    'receiptPrinter', 'ticketPrinter', 'cashDrawer', 'cardReader', 'barcodeScanner',
    'customerDisplay', 'scale', 'turnstileController', 'accessReader', 'wristbandEncoder',
    'signaturePad', 'camera', 'kitchenDisplay', 'labelPrinter'
);

CREATE TABLE platform.device (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workstation_id      uuid NOT NULL REFERENCES platform.workstation (id) ON DELETE CASCADE,
    venue_id            uuid NOT NULL,
    scope_path          ltree NOT NULL,
    kind                platform.device_kind NOT NULL,
    driver              text NOT NULL,
    identifier          text,
    model               text,
    firmware_version    text,
    is_required         boolean NOT NULL DEFAULT false,
    status              text NOT NULL DEFAULT 'unknown'
        CHECK (status IN ('online','offline','error','consumableLow','needsAttention','unknown')),
    status_detail       text,
    last_heartbeat_at   timestamptz,
    created_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT device_identifier_unique UNIQUE (venue_id, kind, identifier)
);

COMMENT ON COLUMN platform.device.driver IS
  'ADR-0015: built to an open standard where one exists — ESC/POS, UnifiedPOS, '
  'OSDP. Adding a vendor is a driver plus configuration, not a core change. '
  'Around nine of the fourteen kinds above have a real standard.';

COMMENT ON COLUMN platform.device.is_required IS
  'A required device that is unreachable blocks shift open. Better discovered '
  'before a queue forms than during one.';

CREATE INDEX device_workstation ON platform.device (workstation_id);
CREATE INDEX device_unhealthy   ON platform.device (venue_id, status)
    WHERE status <> 'online';

ALTER TABLE platform.device ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.device FORCE ROW LEVEL SECURITY;
CREATE POLICY device_scope ON platform.device
    USING (platform.in_scope(scope_path));

-- Heartbeats are high-volume and short-lived. Kept separate so the device row
-- stays small and cacheable.
CREATE TABLE platform.device_heartbeat (
    device_id           uuid NOT NULL REFERENCES platform.device (id) ON DELETE CASCADE,
    recorded_at         timestamptz NOT NULL,
    status              text NOT NULL,
    detail              text,
    firmware_version    text,
    PRIMARY KEY (device_id, recorded_at)
);

COMMENT ON TABLE platform.device_heartbeat IS
  'Retained briefly — long enough to diagnose an intermittent reader, not long '
  'enough to become the largest table in the cell. Trimmed by the retention job.';

-- -----------------------------------------------------------------------------
-- Deferred foreign key. sale_board is created after workstation because
-- workstation is referenced more widely; the constraint is added once both exist.
-- -----------------------------------------------------------------------------
ALTER TABLE platform.workstation
    ADD CONSTRAINT workstation_sale_board_fk
    FOREIGN KEY (sale_board_id) REFERENCES platform.sale_board (id);

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0003', 'tenancy', 'set-by-runner');

-- =============================================================================
-- ROLLBACK
-- =============================================================================
-- ALTER TABLE platform.workstation DROP CONSTRAINT IF EXISTS workstation_sale_board_fk;
-- DROP TABLE IF EXISTS platform.device_heartbeat;
-- DROP TABLE IF EXISTS platform.device;
-- DROP TYPE IF EXISTS platform.device_kind;
-- DROP TABLE IF EXISTS platform.sale_board_tile;
-- DROP TABLE IF EXISTS platform.sale_board_page;
-- DROP TABLE IF EXISTS platform.sale_board;
-- DROP TABLE IF EXISTS platform.workstation;
-- DROP TYPE IF EXISTS platform.workstation_kind;
-- DROP TABLE IF EXISTS platform.venue_settings;
-- DROP FUNCTION IF EXISTS platform.assert_scope_level();
-- DELETE FROM platform.schema_version WHERE version = 'V0003';
