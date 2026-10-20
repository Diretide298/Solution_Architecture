-- V0110 -- tenant database, after r1 (9cec72d) (20261020).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 13 column(s), 13 index(es), 5 other statement(s).

ALTER TABLE orders.no_sale_event ADD COLUMN IF NOT EXISTS approved_by_principal_id uuid;

ALTER TABLE orders.order_event ADD COLUMN IF NOT EXISTS reason_code text CONSTRAINT order_event_reason_code_chk CHECK (char_length(reason_code) <= 60);

ALTER TABLE orders.order_event ADD COLUMN IF NOT EXISTS approved_by_principal_id uuid;

ALTER TABLE orders.order_event ADD COLUMN IF NOT EXISTS note text CONSTRAINT order_event_note_chk CHECK (char_length(note) <= 500);

ALTER TABLE orders.payment ADD COLUMN IF NOT EXISTS tip_amount numeric(18,4);

ALTER TABLE orders.payment ADD COLUMN IF NOT EXISTS tip_source text CONSTRAINT payment_tip_source_chk CHECK (tip_source IN ('terminalPrompt', 'cashierEntered', 'guestApp', 'serviceCharge'));

ALTER TABLE orders.payment ADD COLUMN IF NOT EXISTS tip_allocated_to_principal_id uuid;

ALTER TABLE orders.payment ADD COLUMN IF NOT EXISTS tip_recorded_at timestamptz;

ALTER TABLE orders.payment ADD COLUMN IF NOT EXISTS tip_recorded_by_principal_id uuid;

ALTER TABLE retail.shop_and_drop ADD COLUMN IF NOT EXISTS disposal_method text CONSTRAINT shop_and_drop_disposal_method_chk CHECK (disposal_method IN ('donated', 'destroyed', 'returnedToStock', 'heldLonger'));

ALTER TABLE retail.shop_and_drop ADD COLUMN IF NOT EXISTS disposal_note text CONSTRAINT shop_and_drop_disposal_note_chk CHECK (char_length(disposal_note) <= 300);

ALTER TABLE retail.shop_and_drop ADD COLUMN IF NOT EXISTS disposal_decided_at timestamptz;

ALTER TABLE retail.shop_and_drop ADD COLUMN IF NOT EXISTS disposal_decided_by_principal_id uuid;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'no_sale_event_approved_by_principal_id_fkey' AND conrelid = to_regclass('orders.no_sale_event')) THEN ALTER TABLE orders.no_sale_event ADD CONSTRAINT no_sale_event_approved_by_principal_id_fkey FOREIGN KEY (approved_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'order_event_approved_by_principal_id_fkey' AND conrelid = to_regclass('orders.order_event')) THEN ALTER TABLE orders.order_event ADD CONSTRAINT order_event_approved_by_principal_id_fkey FOREIGN KEY (approved_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'payment_tip_allocated_to_principal_id_fkey' AND conrelid = to_regclass('orders.payment')) THEN ALTER TABLE orders.payment ADD CONSTRAINT payment_tip_allocated_to_principal_id_fkey FOREIGN KEY (tip_allocated_to_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'payment_tip_recorded_by_principal_id_fkey' AND conrelid = to_regclass('orders.payment')) THEN ALTER TABLE orders.payment ADD CONSTRAINT payment_tip_recorded_by_principal_id_fkey FOREIGN KEY (tip_recorded_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'shop_and_drop_disposal_decided_by_principal_id_fkey' AND conrelid = to_regclass('retail.shop_and_drop')) THEN ALTER TABLE retail.shop_and_drop ADD CONSTRAINT shop_and_drop_disposal_decided_by_principal_id_fkey FOREIGN KEY (disposal_decided_by_principal_id) REFERENCES identity.principal(id); END IF; END $$;

CREATE INDEX IF NOT EXISTS conversation_subject_id_idx ON ai.conversation (subject_id);

CREATE INDEX IF NOT EXISTS open_shift_marker_venue_id_idx ON identity.open_shift_marker (venue_id);

CREATE INDEX IF NOT EXISTS form_submission_sale_link_order_line_id_idx ON marketing.form_submission_sale_link (order_line_id);

CREATE INDEX IF NOT EXISTS cart_session_id_idx ON orders.cart (session_id);

CREATE INDEX IF NOT EXISTS cart_workstation_id_idx ON orders.cart (workstation_id);

CREATE INDEX IF NOT EXISTS group_booking_performance_id_idx ON orders.group_booking (performance_id);

CREATE INDEX IF NOT EXISTS bundle_application_venue_id_idx ON catalogue.bundle_application (venue_id);

CREATE INDEX IF NOT EXISTS bundle_application_workstation_id_idx ON catalogue.bundle_application (workstation_id);

CREATE INDEX IF NOT EXISTS no_sale_event_approved_by_principal_id_idx ON orders.no_sale_event (approved_by_principal_id);

CREATE INDEX IF NOT EXISTS order_event_approved_by_principal_id_idx ON orders.order_event (approved_by_principal_id);

CREATE INDEX IF NOT EXISTS payment_tip_allocated_to_principal_id_idx ON orders.payment (tip_allocated_to_principal_id);

CREATE INDEX IF NOT EXISTS payment_tip_recorded_by_principal_id_idx ON orders.payment (tip_recorded_by_principal_id);

CREATE INDEX IF NOT EXISTS shop_and_drop_disposal_decided_by_principal_id_idx ON retail.shop_and_drop (disposal_decided_by_principal_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0110', 'after r1 (9cec72d): 0 table(s), 13 column(s), 13 index(es), 5 other statement(s)', '681d3afc45529728468636c9452614fba04edc4b52ee9564c8dd6dc64b08d674')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS retail.shop_and_drop_disposal_decided_by_principal_id_idx;
-- DROP INDEX IF EXISTS orders.payment_tip_recorded_by_principal_id_idx;
-- DROP INDEX IF EXISTS orders.payment_tip_allocated_to_principal_id_idx;
-- DROP INDEX IF EXISTS orders.order_event_approved_by_principal_id_idx;
-- DROP INDEX IF EXISTS orders.no_sale_event_approved_by_principal_id_idx;
-- DROP INDEX IF EXISTS catalogue.bundle_application_workstation_id_idx;
-- DROP INDEX IF EXISTS catalogue.bundle_application_venue_id_idx;
-- DROP INDEX IF EXISTS orders.group_booking_performance_id_idx;
-- DROP INDEX IF EXISTS orders.cart_workstation_id_idx;
-- DROP INDEX IF EXISTS orders.cart_session_id_idx;
-- DROP INDEX IF EXISTS marketing.form_submission_sale_link_order_line_id_idx;
-- DROP INDEX IF EXISTS identity.open_shift_marker_venue_id_idx;
-- DROP INDEX IF EXISTS ai.conversation_subject_id_idx;
-- ALTER TABLE retail.shop_and_drop DROP CONSTRAINT IF EXISTS shop_and_drop_disposal_decided_by_principal_id_fkey;
-- ALTER TABLE orders.payment DROP CONSTRAINT IF EXISTS payment_tip_recorded_by_principal_id_fkey;
-- ALTER TABLE orders.payment DROP CONSTRAINT IF EXISTS payment_tip_allocated_to_principal_id_fkey;
-- ALTER TABLE orders.order_event DROP CONSTRAINT IF EXISTS order_event_approved_by_principal_id_fkey;
-- ALTER TABLE orders.no_sale_event DROP CONSTRAINT IF EXISTS no_sale_event_approved_by_principal_id_fkey;
-- ALTER TABLE retail.shop_and_drop DROP COLUMN IF EXISTS disposal_decided_by_principal_id;
-- ALTER TABLE retail.shop_and_drop DROP COLUMN IF EXISTS disposal_decided_at;
-- ALTER TABLE retail.shop_and_drop DROP COLUMN IF EXISTS disposal_note;
-- ALTER TABLE retail.shop_and_drop DROP COLUMN IF EXISTS disposal_method;
-- ALTER TABLE orders.payment DROP COLUMN IF EXISTS tip_recorded_by_principal_id;
-- ALTER TABLE orders.payment DROP COLUMN IF EXISTS tip_recorded_at;
-- ALTER TABLE orders.payment DROP COLUMN IF EXISTS tip_allocated_to_principal_id;
-- ALTER TABLE orders.payment DROP COLUMN IF EXISTS tip_source;
-- ALTER TABLE orders.payment DROP COLUMN IF EXISTS tip_amount;
-- ALTER TABLE orders.order_event DROP COLUMN IF EXISTS note;
-- ALTER TABLE orders.order_event DROP COLUMN IF EXISTS approved_by_principal_id;
-- ALTER TABLE orders.order_event DROP COLUMN IF EXISTS reason_code;
-- ALTER TABLE orders.no_sale_event DROP COLUMN IF EXISTS approved_by_principal_id;
-- DELETE FROM platform.schema_version WHERE version = 'V0110';
