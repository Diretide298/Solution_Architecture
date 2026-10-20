-- V0112 -- tenant database, after r1 (9cec72d) (20261021).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 2 column(s), 0 index(es), 2 other statement(s).

ALTER TABLE catalogue.product DROP CONSTRAINT IF EXISTS product_kind_chk;

ALTER TABLE catalogue.product ADD CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard', 'walletTopUp')) NOT VALID;

ALTER TABLE catalogue.product VALIDATE CONSTRAINT product_kind_chk;

ALTER TABLE orders.sales_order ADD COLUMN IF NOT EXISTS kind text DEFAULT 'sale' CONSTRAINT sales_order_kind_chk CHECK (kind IN ('sale', 'walletTopUp'));

ALTER TABLE retail.sale_line ADD COLUMN IF NOT EXISTS order_line_id uuid;

ALTER TABLE wallet.adjustment DROP CONSTRAINT IF EXISTS adjustment_kind_chk;

ALTER TABLE wallet.adjustment ADD CONSTRAINT adjustment_kind_chk CHECK (kind IN ('reversal', 'chargeback', 'goodwill', 'correction', 'writeOff', 'expiry', 'forfeiture', 'extension')) NOT VALID;

ALTER TABLE wallet.adjustment VALIDATE CONSTRAINT adjustment_kind_chk;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0112', 'after r1 (9cec72d): 0 table(s), 2 column(s), 0 index(es), 2 other statement(s)', 'f20de698a682bf959c43944ab27627e4694b993bd479ffea13bce0a689b61bf4')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE wallet.adjustment DROP CONSTRAINT IF EXISTS adjustment_kind_chk; ALTER TABLE wallet.adjustment ADD CONSTRAINT adjustment_kind_chk CHECK (kind IN ('reversal', 'chargeback', 'goodwill', 'correction', 'writeOff')) NOT VALID;
-- ALTER TABLE retail.sale_line DROP COLUMN IF EXISTS order_line_id;
-- ALTER TABLE orders.sales_order DROP COLUMN IF EXISTS kind;
-- ALTER TABLE catalogue.product DROP CONSTRAINT IF EXISTS product_kind_chk; ALTER TABLE catalogue.product ADD CONSTRAINT product_kind_chk CHECK (kind IN ('admission', 'timedAdmission', 'datedAdmission', 'openDated', 'seated', 'membership', 'bundle', 'fnb', 'retail', 'rental', 'addOn', 'giftCard')) NOT VALID;
-- DELETE FROM platform.schema_version WHERE version = 'V0112';
