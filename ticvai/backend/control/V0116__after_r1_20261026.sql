-- V0116 -- control database, after r1 (9cec72d) (20261026).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 6 table(s), 13 column(s), 10 index(es), 7 other statement(s).

CREATE TABLE IF NOT EXISTS control.api_client_secret (
    id                                uuid PRIMARY KEY NOT NULL,
    api_client_id                     uuid NOT NULL,
    secret_hash                       text NOT NULL CONSTRAINT api_client_secret_secret_hash_chk CHECK (char_length(secret_hash) <= 64),
    hash_key_version                  integer NOT NULL,
    issued_at                         timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    revoked_at                        timestamptz
);

DO $$ BEGIN IF to_regclass('control.billing_entity') IS NOT NULL THEN
ALTER TABLE control.billing_entity ADD COLUMN IF NOT EXISTS billing_currency text CONSTRAINT billing_entity_billing_currency_chk CHECK (char_length(billing_currency) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.capacity_pack') IS NOT NULL THEN
ALTER TABLE control.capacity_pack ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT capacity_pack_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.contract') IS NOT NULL THEN
ALTER TABLE control.contract ADD COLUMN IF NOT EXISTS issuing_legal_entity text CONSTRAINT contract_issuing_legal_entity_chk CHECK (issuing_legal_entity IN ('ainfiniteAiUae', 'ainfiniteAiIndia'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.contract') IS NOT NULL THEN
ALTER TABLE control.contract ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT contract_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.credit_note') IS NOT NULL THEN
ALTER TABLE control.credit_note ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT credit_note_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice' AND column_name = 'invoice_number' AND is_nullable = 'NO') THEN ALTER TABLE control.invoice ALTER COLUMN invoice_number DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('control.invoice') IS NOT NULL THEN
ALTER TABLE control.invoice ADD COLUMN IF NOT EXISTS issuing_legal_entity text CONSTRAINT invoice_issuing_legal_entity_chk CHECK (issuing_legal_entity IN ('ainfiniteAiUae', 'ainfiniteAiIndia'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.invoice') IS NOT NULL THEN
ALTER TABLE control.invoice ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT invoice_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

CREATE TABLE IF NOT EXISTS control.invoice_number_sequence (
    id                                uuid PRIMARY KEY NOT NULL,
    legal_entity_code                 text NOT NULL CONSTRAINT invoice_number_sequence_legal_entity_code_chk CHECK (char_length(legal_entity_code) <= 50),
    document_kind                     text NOT NULL CONSTRAINT invoice_number_sequence_document_kind_chk CHECK (document_kind IN ('invoice', 'creditNote')),
    prefix                            text NOT NULL CONSTRAINT invoice_number_sequence_prefix_chk CHECK (char_length(prefix) <= 20),
    next_number                       bigint NOT NULL DEFAULT 1,
    updated_at                        timestamptz
);

DO $$ BEGIN IF to_regclass('control.licence_add_on') IS NOT NULL THEN
ALTER TABLE control.licence_add_on ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT licence_add_on_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.licensing_model') IS NOT NULL THEN
ALTER TABLE control.licensing_model ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT licensing_model_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.module_listing') IS NOT NULL THEN
ALTER TABLE control.module_listing ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT module_listing_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.plan') IS NOT NULL THEN
ALTER TABLE control.plan ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT plan_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

CREATE TABLE IF NOT EXISTS control.platform_operator (
    id                                uuid PRIMARY KEY NOT NULL,
    email                             text NOT NULL CONSTRAINT platform_operator_email_chk CHECK (char_length(email) <= 320),
    display_name                      text NOT NULL CONSTRAINT platform_operator_display_name_chk CHECK (char_length(display_name) <= 200),
    platform_permissions              text[] NOT NULL,
    is_active                         boolean NOT NULL DEFAULT true,
    created_at                        timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS control.platform_operator_mfa (
    id                                uuid PRIMARY KEY NOT NULL,
    operator_id                       uuid NOT NULL,
    kind                              text NOT NULL CONSTRAINT platform_operator_mfa_kind_chk CHECK (kind IN ('totp', 'emailOtp')),
    secret                            text CONSTRAINT platform_operator_mfa_secret_chk CHECK (char_length(secret) <= 500),
    destination                       text CONSTRAINT platform_operator_mfa_destination_chk CHECK (char_length(destination) <= 500),
    is_primary                        boolean DEFAULT false,
    is_active                         boolean NOT NULL DEFAULT true,
    enrolled_at                       timestamptz NOT NULL,
    last_used_at                      timestamptz
);

CREATE TABLE IF NOT EXISTS control.platform_session (
    id                                uuid PRIMARY KEY NOT NULL,
    operator_id                       uuid NOT NULL,
    started_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL,
    ended_at                          timestamptz,
    mfa_verified_at                   timestamptz,
    step_up_action                    text CONSTRAINT platform_session_step_up_action_chk CHECK (char_length(step_up_action) <= 100),
    step_up_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.platform_tax_rate (
    id                                uuid PRIMARY KEY NOT NULL,
    country_code                      text NOT NULL CONSTRAINT platform_tax_rate_country_code_chk CHECK (char_length(country_code) <= 2),
    tax_name                          text NOT NULL CONSTRAINT platform_tax_rate_tax_name_chk CHECK (char_length(tax_name) <= 50),
    rate_percent                      numeric(18,4) NOT NULL,
    effective_from                    date NOT NULL,
    effective_to                      date,
    updated_at                        timestamptz
);

DO $$ BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL THEN
ALTER TABLE control.webhook_replay ADD COLUMN IF NOT EXISTS tenant_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL THEN
ALTER TABLE control.webhook_replay ADD COLUMN IF NOT EXISTS failure_reason text CONSTRAINT webhook_replay_failure_reason_chk CHECK (char_length(failure_reason) <= 500);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.api_client_secret') IS NOT NULL AND to_regclass('control.api_client') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client_secret' AND column_name = 'api_client_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'api_client_secret_api_client_id_fkey' AND conrelid = to_regclass('control.api_client_secret')) THEN
ALTER TABLE control.api_client_secret ADD CONSTRAINT api_client_secret_api_client_id_fkey FOREIGN KEY (api_client_id) REFERENCES control.api_client(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_operator_mfa') IS NOT NULL AND to_regclass('control.platform_operator') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_operator_mfa' AND column_name = 'operator_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'platform_operator_mfa_operator_id_fkey' AND conrelid = to_regclass('control.platform_operator_mfa')) THEN
ALTER TABLE control.platform_operator_mfa ADD CONSTRAINT platform_operator_mfa_operator_id_fkey FOREIGN KEY (operator_id) REFERENCES control.platform_operator(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_session') IS NOT NULL AND to_regclass('control.platform_operator') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_session' AND column_name = 'operator_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'platform_session_operator_id_fkey' AND conrelid = to_regclass('control.platform_session')) THEN
ALTER TABLE control.platform_session ADD CONSTRAINT platform_session_operator_id_fkey FOREIGN KEY (operator_id) REFERENCES control.platform_operator(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL AND to_regclass('control.tenant') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_replay' AND column_name = 'tenant_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'webhook_replay_tenant_id_fkey' AND conrelid = to_regclass('control.webhook_replay')) THEN
ALTER TABLE control.webhook_replay ADD CONSTRAINT webhook_replay_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.api_client_secret') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'api_client_secret' AND column_name = 'api_client_id') THEN
CREATE INDEX IF NOT EXISTS api_client_secret_api_client_id_idx ON control.api_client_secret (api_client_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_operator_mfa') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_operator_mfa' AND column_name = 'operator_id') THEN
CREATE INDEX IF NOT EXISTS platform_operator_mfa_operator_id_idx ON control.platform_operator_mfa (operator_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_session') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_session' AND column_name = 'operator_id') THEN
CREATE INDEX IF NOT EXISTS platform_session_operator_id_idx ON control.platform_session (operator_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.webhook_replay') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'webhook_replay' AND column_name = 'tenant_id') THEN
CREATE INDEX IF NOT EXISTS webhook_replay_tenant_id_idx ON control.webhook_replay (tenant_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_operator') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_operator' AND column_name = 'email') THEN
CREATE UNIQUE INDEX IF NOT EXISTS platform_operator_email_uniq ON control.platform_operator (lower(email));
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.developer_account') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'developer_account' AND column_name = 'contact_email') THEN
CREATE UNIQUE INDEX IF NOT EXISTS developer_account_contact_email_uniq ON control.developer_account (lower(contact_email));
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.invoice_number_sequence') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice_number_sequence' AND column_name = 'document_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice_number_sequence' AND column_name = 'legal_entity_code') THEN
CREATE UNIQUE INDEX IF NOT EXISTS invoice_number_sequence_legal_entity_code_document_kind_uniq ON control.invoice_number_sequence (lower(legal_entity_code), lower(document_kind));
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.platform_tax_rate') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_tax_rate' AND column_name = 'country_code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'platform_tax_rate' AND column_name = 'effective_from') THEN
CREATE UNIQUE INDEX IF NOT EXISTS platform_tax_rate_country_code_effective_from_uniq ON control.platform_tax_rate (lower(country_code), effective_from);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.invoice') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice' AND column_name = 'period_end') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice' AND column_name = 'period_start') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice' AND column_name = 'status') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'invoice' AND column_name = 'tenant_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS invoice_tenant_id_period_start_period_end_uniq ON control.invoice (tenant_id, period_start, period_end) WHERE status IS DISTINCT FROM 'cancelled';
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.tenant_domain') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'tenant_domain' AND column_name = 'channel') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'tenant_domain' AND column_name = 'is_primary') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'tenant_domain' AND column_name = 'status') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'tenant_domain' AND column_name = 'tenant_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_tenant_id_channel_uniq ON control.tenant_domain (tenant_id, lower(channel)) WHERE is_primary AND status = 'active';
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'control') THEN GRANT USAGE ON SCHEMA control TO commerce; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'commerce') AND to_regclass('control.api_client') IS NOT NULL THEN GRANT SELECT ON control.api_client TO commerce; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0116', 'after r1 (9cec72d): 6 table(s), 13 column(s), 10 index(es), 7 other statement(s)', 'b761d3312a059ecef702669c41bf64c0f53ce64924228d75c2a14fddcb74d412')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON control.api_client FROM commerce;
-- REVOKE USAGE ON SCHEMA control FROM commerce;
-- DROP INDEX IF EXISTS control.tenant_domain_tenant_id_channel_uniq;
-- DROP INDEX IF EXISTS control.invoice_tenant_id_period_start_period_end_uniq;
-- DROP INDEX IF EXISTS control.platform_tax_rate_country_code_effective_from_uniq;
-- DROP INDEX IF EXISTS control.invoice_number_sequence_legal_entity_code_document_kind_uniq;
-- DROP INDEX IF EXISTS control.developer_account_contact_email_uniq;
-- DROP INDEX IF EXISTS control.platform_operator_email_uniq;
-- DROP INDEX IF EXISTS control.webhook_replay_tenant_id_idx;
-- DROP INDEX IF EXISTS control.platform_session_operator_id_idx;
-- DROP INDEX IF EXISTS control.platform_operator_mfa_operator_id_idx;
-- DROP INDEX IF EXISTS control.api_client_secret_api_client_id_idx;
-- ALTER TABLE control.webhook_replay DROP CONSTRAINT IF EXISTS webhook_replay_tenant_id_fkey;
-- ALTER TABLE control.webhook_replay DROP COLUMN IF EXISTS failure_reason;
-- ALTER TABLE control.webhook_replay DROP COLUMN IF EXISTS tenant_id;
-- DROP TABLE IF EXISTS control.platform_tax_rate;
-- DROP TABLE IF EXISTS control.platform_session;
-- DROP TABLE IF EXISTS control.platform_operator_mfa;
-- DROP TABLE IF EXISTS control.platform_operator;
-- ALTER TABLE control.plan DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.module_listing DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.licensing_model DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.licence_add_on DROP COLUMN IF EXISTS currency_code;
-- DROP TABLE IF EXISTS control.invoice_number_sequence;
-- ALTER TABLE control.invoice DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.invoice DROP COLUMN IF EXISTS issuing_legal_entity;
-- ALTER TABLE control.invoice ALTER COLUMN invoice_number SET NOT NULL;
-- ALTER TABLE control.credit_note DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.contract DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.contract DROP COLUMN IF EXISTS issuing_legal_entity;
-- ALTER TABLE control.capacity_pack DROP COLUMN IF EXISTS currency_code;
-- ALTER TABLE control.billing_entity DROP COLUMN IF EXISTS billing_currency;
-- DROP TABLE IF EXISTS control.api_client_secret;
-- DELETE FROM platform.schema_version WHERE version = 'V0116';
