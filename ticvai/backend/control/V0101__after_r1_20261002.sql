-- V0101 -- control database, after r1 (a1ba956) (20261002).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (a1ba956), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 4 table(s), 4 column(s), 1 index(es), 0 other statement(s).

CREATE TABLE IF NOT EXISTS control.billing_entity (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid,
    legal_name                        text CONSTRAINT billing_entity_legal_name_chk CHECK (char_length(legal_name) <= 300),
    trade_licence_number              text CONSTRAINT billing_entity_trade_licence_number_chk CHECK (char_length(trade_licence_number) <= 100),
    trn                               text CONSTRAINT billing_entity_trn_chk CHECK (char_length(trn) <= 30),
    country_code                      text CONSTRAINT billing_entity_country_code_chk CHECK (char_length(country_code) <= 2),
    address                           text CONSTRAINT billing_entity_address_chk CHECK (char_length(address) <= 1000),
    invoice_email                     text,
    documents                         jsonb,
    missing_documents                 text[],
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.config_package (
    id                                uuid PRIMARY KEY,
    tenant_id                         uuid,
    source_environment                text CONSTRAINT config_package_source_environment_chk CHECK (source_environment IN ('dev', 'staging', 'production')),
    version                           integer,
    checksum                          text,
    record_counts                     jsonb,
    excluded_kinds                    text[],
    created_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.config_package_application (
    id                                uuid PRIMARY KEY,
    diff_id                           uuid,
    status                            text CONSTRAINT config_package_application_status_chk CHECK (status IN ('applying', 'applied', 'failed')),
    applied_count                     integer,
    previous_package_id               uuid,
    started_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.config_package_diff (
    id                                uuid PRIMARY KEY,
    package_id                        uuid,
    target_environment                text CONSTRAINT config_package_diff_target_environment_chk CHECK (target_environment IN ('dev', 'staging', 'production')),
    computed_at                       timestamptz,
    changes                           jsonb
);

ALTER TABLE control.onboarding_application ADD COLUMN IF NOT EXISTS billing_entity_id uuid;

ALTER TABLE control.tenant_domain ADD COLUMN IF NOT EXISTS is_primary boolean DEFAULT false;

ALTER TABLE control.tenant_domain ADD COLUMN IF NOT EXISTS redirect_to_hostname text CONSTRAINT tenant_domain_redirect_to_hostname_chk CHECK (char_length(redirect_to_hostname) <= 253);

ALTER TABLE control.tenant_domain ADD COLUMN IF NOT EXISTS last_validated_at timestamptz;

CREATE INDEX IF NOT EXISTS onboarding_application_billing_entity_id_idx ON control.onboarding_application (billing_entity_id);

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0101', 'after r1 (a1ba956): 4 table(s), 4 column(s), 1 index(es), 0 other statement(s)', 'f8e1ca5f4b391ba4d03891ff8d59664d4595191aca404365f086d1925a99efe0')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.onboarding_application_billing_entity_id_idx;
-- ALTER TABLE control.tenant_domain DROP COLUMN IF EXISTS last_validated_at;
-- ALTER TABLE control.tenant_domain DROP COLUMN IF EXISTS redirect_to_hostname;
-- ALTER TABLE control.tenant_domain DROP COLUMN IF EXISTS is_primary;
-- ALTER TABLE control.onboarding_application DROP COLUMN IF EXISTS billing_entity_id;
-- DROP TABLE IF EXISTS control.config_package_diff;
-- DROP TABLE IF EXISTS control.config_package_application;
-- DROP TABLE IF EXISTS control.config_package;
-- DROP TABLE IF EXISTS control.billing_entity;
-- DELETE FROM platform.schema_version WHERE version = 'V0101';
