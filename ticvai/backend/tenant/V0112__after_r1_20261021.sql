-- V0112 -- tenant database, after r1 (9cec72d) (20261021).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 2 column(s), 2 index(es), 3 other statement(s).

ALTER TABLE catalogue.product DROP CONSTRAINT IF EXISTS product_kind_chk;

ALTER TABLE catalogue.product ADD CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard', 'walletTopUp')) NOT VALID;

ALTER TABLE catalogue.product VALIDATE CONSTRAINT product_kind_chk;

ALTER TABLE retail.sale_line ADD COLUMN IF NOT EXISTS order_line_id uuid;

ALTER TABLE wallet.adjustment DROP CONSTRAINT IF EXISTS adjustment_kind_chk;

ALTER TABLE wallet.adjustment ADD CONSTRAINT adjustment_kind_chk CHECK (kind IN ('reversal', 'chargeback', 'goodwill', 'correction', 'writeOff', 'expiry', 'forfeiture', 'extension')) NOT VALID;

ALTER TABLE wallet.adjustment VALIDATE CONSTRAINT adjustment_kind_chk;

ALTER TABLE wallet.credit_lot ADD COLUMN IF NOT EXISTS order_line_id uuid;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'credit_lot_order_line_id_fkey' AND conrelid = to_regclass('wallet.credit_lot')) THEN ALTER TABLE wallet.credit_lot ADD CONSTRAINT credit_lot_order_line_id_fkey FOREIGN KEY (order_line_id) REFERENCES orders.order_line(id); END IF; END $$;

CREATE INDEX IF NOT EXISTS sale_line_order_line_id_idx ON retail.sale_line (order_line_id);

CREATE INDEX IF NOT EXISTS credit_lot_order_line_id_idx ON wallet.credit_lot (order_line_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0112', 'after r1 (9cec72d): 0 table(s), 2 column(s), 2 index(es), 3 other statement(s)', 'f82d7c4868dcf3f34fe44271c386b49e3f598749f3b9f4e93a9e56d9d08628ce')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS wallet.credit_lot_order_line_id_idx;
-- DROP INDEX IF EXISTS retail.sale_line_order_line_id_idx;
-- ALTER TABLE wallet.credit_lot DROP CONSTRAINT IF EXISTS credit_lot_order_line_id_fkey;
-- ALTER TABLE wallet.credit_lot DROP COLUMN IF EXISTS order_line_id;
-- ALTER TABLE wallet.adjustment DROP CONSTRAINT IF EXISTS adjustment_kind_chk; ALTER TABLE wallet.adjustment ADD CONSTRAINT adjustment_kind_chk CHECK (kind IN ('reversal', 'chargeback', 'goodwill', 'correction', 'writeOff')) NOT VALID;
-- ALTER TABLE retail.sale_line DROP COLUMN IF EXISTS order_line_id;
-- ALTER TABLE catalogue.product DROP CONSTRAINT IF EXISTS product_kind_chk; ALTER TABLE catalogue.product ADD CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard')) NOT VALID;
-- DELETE FROM platform.schema_version WHERE version = 'V0112';
