-- =============================================================================
-- V0003b — Guest-facing tables
--
-- Four features that were reachable in a tenant's feature toggles and nowhere
-- else. Each was found by asking what sits behind a switch:
--
--   * push notifications          — no device table, so no token had anywhere to live
--   * guest self-ordering         — every F&B read needed a staff permission
--   * delivery to a location      — 4.6.26 names cabanas and seats; only tables existed
--   * shop and drop               — 4.4.7, not modelled at all
--
-- The migration sits between V0003 and V0004 because it depends on scope typing
-- from V0003a and must exist before catalogue, which references entitlements.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Satellite schemas.
--
-- V0001 declared only the spine — platform, identity, catalogue, orders, access,
-- sync, ledger, pii. Every satellite module needs its own, and this is the first
-- migration that writes into one. Declared here rather than in each module's
-- migration so the boundary is visible in one place.
-- -----------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS marketing;
CREATE SCHEMA IF NOT EXISTS fnb;
CREATE SCHEMA IF NOT EXISTS retail;
CREATE SCHEMA IF NOT EXISTS seating;
CREATE SCHEMA IF NOT EXISTS promotions;
CREATE SCHEMA IF NOT EXISTS inventory;
CREATE SCHEMA IF NOT EXISTS maintenance;
CREATE SCHEMA IF NOT EXISTS queue;
CREATE SCHEMA IF NOT EXISTS whitelabel;
CREATE SCHEMA IF NOT EXISTS assets;
CREATE SCHEMA IF NOT EXISTS games;
CREATE SCHEMA IF NOT EXISTS reporting;

COMMENT ON SCHEMA fnb IS
  'Satellite. Menus, service, kitchen handoff and delivery locations.';
COMMENT ON SCHEMA marketing IS
  'Satellite. Guest profiles, consent, campaigns, cases, loyalty. Personal data still '
  'lives in pii and is referenced by opaque id — this schema holds behaviour, not identity.';

-- -----------------------------------------------------------------------------
-- Guest devices. Push has to land somewhere.
-- -----------------------------------------------------------------------------
CREATE TABLE marketing.guest_device (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id          uuid NOT NULL REFERENCES pii.subject (id) ON DELETE CASCADE,
    platform            text NOT NULL CHECK (platform IN ('ios','android','web')),
    token               text NOT NULL,
    token_fingerprint   text NOT NULL,
    app_version         text,
    os_version          text,
    device_model        text,
    locale              text,
    status              text NOT NULL DEFAULT 'active'
                        CHECK (status IN ('active','revoked','failed')),
    failure_count       smallint NOT NULL DEFAULT 0,
    registered_at       timestamptz NOT NULL DEFAULT now(),
    last_seen_at        timestamptz,
    revoked_at          timestamptz,
    CONSTRAINT guest_device_token_unique UNIQUE (platform, token_fingerprint),
    CONSTRAINT guest_device_revocation CHECK (status <> 'revoked' OR revoked_at IS NOT NULL)
);

COMMENT ON COLUMN marketing.guest_device.token IS
  'Write-only. Never returned by any API — only the fingerprint is. A push credential '
  'in a response is a credential every support agent can read.';

COMMENT ON COLUMN marketing.guest_device.failure_count IS
  'Consecutive delivery failures. Past the threshold the row moves to failed and stops '
  'being targeted. A dead token retried forever is wasted quota and a delivery rate that '
  'lies.';

COMMENT ON CONSTRAINT guest_device_token_unique ON marketing.guest_device IS
  'One registration per token. Providers rotate tokens without an uninstall, so '
  're-registration must update rather than accumulate — a guest with forty rows gets '
  'forty notifications.';

CREATE INDEX guest_device_subject ON marketing.guest_device (subject_id)
    WHERE status = 'active';
CREATE INDEX guest_device_failing ON marketing.guest_device (status)
    WHERE status = 'failed';

-- No venue_id. A guest device belongs to a person, not a venue, and push is sent
-- from the tenant. Scoping it to a venue would break the guest who visits two.

-- -----------------------------------------------------------------------------
-- Wishlist. Guest intent, not a catalogue property.
-- -----------------------------------------------------------------------------
CREATE TABLE marketing.wishlist_item (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id          uuid NOT NULL REFERENCES pii.subject (id) ON DELETE CASCADE,
    variant_id          uuid NOT NULL,
    performance_id      uuid,
    note                varchar(200),
    added_at            timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT wishlist_unique UNIQUE (subject_id, variant_id, performance_id)
);

COMMENT ON CONSTRAINT wishlist_unique ON marketing.wishlist_item IS
  'Saving twice is one entry. The count matters to the guest and to demand signals, so a '
  'double tap must not inflate it.';

CREATE INDEX wishlist_subject ON marketing.wishlist_item (subject_id);
CREATE INDEX wishlist_variant ON marketing.wishlist_item (variant_id);

-- -----------------------------------------------------------------------------
-- Delivery locations. 4.6.26 — tables, seats, cabanas or designated locations.
-- -----------------------------------------------------------------------------
CREATE TYPE fnb.delivery_location_kind AS ENUM (
    'table', 'seat', 'cabana', 'sunbed', 'poolside', 'box', 'suite', 'lawn',
    'collectionPoint', 'namedLocation'
);

CREATE TABLE fnb.delivery_location (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    venue_id            uuid NOT NULL,
    venue_level         platform.scope_level
                        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    scope_path          ltree NOT NULL,
    kind                fnb.delivery_location_kind NOT NULL,
    label               text NOT NULL,
    zone                text,
    table_id            uuid,
    seat_id             char(26),
    walk_time_minutes   smallint,
    is_serviceable      boolean NOT NULL DEFAULT true,
    unserviceable_reason text,
    is_active           boolean NOT NULL DEFAULT true,
    created_at          timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT delivery_location_label_unique UNIQUE (venue_id, label),
    CONSTRAINT delivery_location_serviceable
        CHECK (is_serviceable OR unserviceable_reason IS NOT NULL),
    FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)
);

COMMENT ON TABLE fnb.delivery_location IS
  'One table for ten kinds, because a runner needs one instruction and a guest needs one '
  'way to say where they are. A separate table per furniture type would be ten ways to '
  'express one sentence.';

COMMENT ON COLUMN fnb.delivery_location.walk_time_minutes IS
  'From the serving outlet. A cabana eight minutes away is not the same promise as a table '
  'by the kitchen, and the guest estimate should say so.';

COMMENT ON COLUMN fnb.delivery_location.seat_id IS
  'Set where the seat is the address — an auditorium or a stadium. References the seat map '
  'by its stable identifier, not by section, row and number, which change on a refit.';

CREATE INDEX delivery_location_venue ON fnb.delivery_location (venue_id)
    WHERE is_active AND is_serviceable;
CREATE INDEX delivery_location_gist  ON fnb.delivery_location USING gist (scope_path);

ALTER TABLE fnb.delivery_location ENABLE ROW LEVEL SECURITY;
ALTER TABLE fnb.delivery_location FORCE ROW LEVEL SECURITY;
CREATE POLICY delivery_location_scope ON fnb.delivery_location
    USING (platform.in_scope(scope_path));

-- Which outlets serve which locations. A cabana served by the pool bar and not the
-- restaurant is normal; a location nothing serves is not an address.
CREATE TABLE fnb.delivery_location_outlet (
    location_id         uuid NOT NULL REFERENCES fnb.delivery_location (id) ON DELETE CASCADE,
    outlet_id           uuid NOT NULL REFERENCES platform.outlet (id) ON DELETE CASCADE,
    PRIMARY KEY (location_id, outlet_id)
);

-- -----------------------------------------------------------------------------
-- Location sessions. A guest scanning a code to say where they are sitting.
-- -----------------------------------------------------------------------------
CREATE TABLE fnb.location_session (
    id                  char(26) PRIMARY KEY,
    location_id         uuid NOT NULL REFERENCES fnb.delivery_location (id),
    venue_id            uuid NOT NULL,
    venue_level         platform.scope_level
                        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    scope_path          ltree NOT NULL,
    subject_id          uuid REFERENCES pii.subject (id) ON DELETE SET NULL,
    outlet_id           uuid REFERENCES platform.outlet (id),
    visit_id            char(26),
    joined_existing_visit boolean NOT NULL DEFAULT false,
    party_size          smallint,
    claimed_at          timestamptz NOT NULL DEFAULT now(),
    expires_at          timestamptz NOT NULL,
    FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)
);

COMMENT ON TABLE fnb.location_session IS
  'A claim is not a booking. It attaches a guest to a location so an order can be routed '
  'there, and it expires — otherwise a guest who left can order to a lounger now occupied '
  'by someone else.';

COMMENT ON COLUMN fnb.location_session.visit_id IS
  'Set where the location is a table with an open visit. The guest joins it rather than '
  'starting a second, so a starter ordered from a server and a dessert ordered by phone '
  'land on one bill.';

CREATE INDEX location_session_live ON fnb.location_session (location_id, expires_at)
    WHERE expires_at > now();
CREATE INDEX location_session_subject ON fnb.location_session (subject_id);
CREATE INDEX location_session_gist ON fnb.location_session USING gist (scope_path);

ALTER TABLE fnb.location_session ENABLE ROW LEVEL SECURITY;
ALTER TABLE fnb.location_session FORCE ROW LEVEL SECURITY;
CREATE POLICY location_session_scope ON fnb.location_session
    USING (platform.in_scope(scope_path));

-- Rotating codes. A static code photographed once lets someone order to a cabana
-- they are not at, from outside the venue.
CREATE TABLE fnb.location_code (
    location_id         uuid NOT NULL REFERENCES fnb.delivery_location (id) ON DELETE CASCADE,
    code_hash           text NOT NULL,
    valid_from          timestamptz NOT NULL DEFAULT now(),
    valid_to            timestamptz NOT NULL,
    PRIMARY KEY (location_id, code_hash),
    CONSTRAINT location_code_window CHECK (valid_to > valid_from)
);

COMMENT ON TABLE fnb.location_code IS
  'Hashed and time-bounded. Several may be valid at once during rotation, so a guest who '
  'scanned thirty seconds before the change is not refused.';

CREATE INDEX location_code_valid ON fnb.location_code (valid_to);

-- -----------------------------------------------------------------------------
-- Shop and drop. 4.4.7 — buy now, collect on the way out.
-- -----------------------------------------------------------------------------
CREATE TABLE retail.shop_and_drop (
    id                  char(26) PRIMARY KEY,
    drop_reference      text NOT NULL,
    sale_id             char(26) NOT NULL,
    venue_id            uuid NOT NULL,
    venue_level         platform.scope_level
                        GENERATED ALWAYS AS ('venue'::platform.scope_level) STORED,
    scope_path          ltree NOT NULL,
    entitlement_id      char(26),
    subject_id          uuid REFERENCES pii.subject (id) ON DELETE SET NULL,
    collection_point_id uuid NOT NULL REFERENCES fnb.delivery_location (id),
    status              text NOT NULL DEFAULT 'awaitingCollection'
        CHECK (status IN ('awaitingCollection','partiallyCollected','collected','uncollected','disposed')),
    dropped_at          timestamptz NOT NULL DEFAULT now(),
    collect_by          timestamptz NOT NULL,
    collected_at        timestamptz,
    collected_by        uuid REFERENCES identity.principal (id),
    verified_by         text CHECK (verified_by IN ('entitlementScan','receipt','dropReference','staffOverride')),
    CONSTRAINT shop_and_drop_reference_unique UNIQUE (venue_id, drop_reference),
    FOREIGN KEY (venue_id, venue_level) REFERENCES platform.scope_node (id, level)
);

COMMENT ON TABLE retail.shop_and_drop IS
  'Paid goods awaiting handover. Deliberately not a reservation: retail.reservation holds '
  'unsold stock for someone who has not paid, and conflating the two produces a stock '
  'figure nobody can explain.

Stock left at purchase, not at collection. These items are sold; they are merely elsewhere.';

COMMENT ON COLUMN retail.shop_and_drop.entitlement_id IS
  'The ticket that claims these goods — the point of 4.4.7. A guest should not have to keep '
  'a paper slip safe for eight hours in a water park; the thing they cannot leave without '
  'is the thing that claims their shopping.';

COMMENT ON COLUMN retail.shop_and_drop.collect_by IS
  'Usually venue close. Past it the row moves to uncollected, which is an exception someone '
  'works through rather than a permanent shelf occupant.';

CREATE INDEX shop_and_drop_entitlement ON retail.shop_and_drop (entitlement_id)
    WHERE status IN ('awaitingCollection','partiallyCollected');
CREATE INDEX shop_and_drop_pending ON retail.shop_and_drop (collection_point_id, collect_by)
    WHERE status IN ('awaitingCollection','partiallyCollected');
CREATE INDEX shop_and_drop_gist ON retail.shop_and_drop USING gist (scope_path);

ALTER TABLE retail.shop_and_drop ENABLE ROW LEVEL SECURITY;
ALTER TABLE retail.shop_and_drop FORCE ROW LEVEL SECURITY;
CREATE POLICY shop_and_drop_scope ON retail.shop_and_drop
    USING (platform.in_scope(scope_path));

CREATE TABLE retail.shop_and_drop_line (
    id                  char(26) PRIMARY KEY,
    drop_id             char(26) NOT NULL REFERENCES retail.shop_and_drop (id) ON DELETE CASCADE,
    sale_line_id        char(26) NOT NULL,
    merchandise_id      uuid NOT NULL,
    quantity            integer NOT NULL CHECK (quantity > 0),
    collected_quantity  integer NOT NULL DEFAULT 0,
    CONSTRAINT drop_line_collected CHECK (collected_quantity <= quantity)
);

COMMENT ON CONSTRAINT drop_line_collected ON retail.shop_and_drop_line IS
  'Partial collection is permitted — a guest may take some and leave the rest for a later '
  'trip on the same ticket. Collecting more than was dropped is not.';

CREATE INDEX shop_and_drop_line_drop ON retail.shop_and_drop_line (drop_id);

INSERT INTO platform.schema_version (version, name, checksum)
VALUES ('V0003b', 'guest-facing', 'set-by-runner');

-- =============================================================================
-- ROLLBACK
-- =============================================================================
-- DROP TABLE IF EXISTS retail.shop_and_drop_line;
-- DROP TABLE IF EXISTS retail.shop_and_drop;
-- DROP TABLE IF EXISTS fnb.location_code;
-- DROP TABLE IF EXISTS fnb.location_session;
-- DROP TABLE IF EXISTS fnb.delivery_location_outlet;
-- DROP TABLE IF EXISTS fnb.delivery_location;
-- DROP TYPE IF EXISTS fnb.delivery_location_kind;
-- DROP TABLE IF EXISTS marketing.wishlist_item;
-- DROP TABLE IF EXISTS marketing.guest_device;
-- DELETE FROM platform.schema_version WHERE version = 'V0003b';
