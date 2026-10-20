-- V0108 -- control database, after r1 (9cec72d) (20261020).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 19 table(s), 4 column(s), 18 index(es), 18 other statement(s).

CREATE TABLE IF NOT EXISTS control.audit_record (
    id                                uuid PRIMARY KEY NOT NULL,
    operator_principal_id             uuid,
    tenant_id                         uuid,
    action                            text NOT NULL CONSTRAINT audit_record_action_chk CHECK (char_length(action) <= 100),
    subject_ref                       text CONSTRAINT audit_record_subject_ref_chk CHECK (char_length(subject_ref) <= 200),
    details                           jsonb,
    occurred_at                       timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS control.capacity_pack (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    unit                              text NOT NULL,
    quantity                          integer NOT NULL,
    list_price                        numeric(18,4),
    valid_from                        date,
    valid_to                          date,
    is_temporary                      boolean DEFAULT true,
    approved_by                       uuid,
    invoice_id                        uuid
);

CREATE TABLE IF NOT EXISTS control.cell_endpoint (
    id                                uuid PRIMARY KEY NOT NULL,
    cell_id                           uuid NOT NULL,
    service_name                      text NOT NULL CONSTRAINT cell_endpoint_service_name_chk CHECK (char_length(service_name) <= 100),
    url                               text NOT NULL CONSTRAINT cell_endpoint_url_chk CHECK (char_length(url) <= 1000),
    contract_version                  text CONSTRAINT cell_endpoint_contract_version_chk CHECK (char_length(contract_version) <= 50),
    authentication_type               text CONSTRAINT cell_endpoint_authentication_type_chk CHECK (char_length(authentication_type) <= 50),
    credential_reference              text CONSTRAINT cell_endpoint_credential_reference_chk CHECK (char_length(credential_reference) <= 500),
    status                            text NOT NULL CONSTRAINT cell_endpoint_status_chk CHECK (char_length(status) <= 30),
    last_health_check_at              timestamptz,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

ALTER TABLE control.cell_job ADD COLUMN IF NOT EXISTS target_tier text;

ALTER TABLE control.cell_tenant ADD COLUMN IF NOT EXISTS root_scope_path ltree;

CREATE TABLE IF NOT EXISTS control.contract (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_name                         text,
    plan_version                      text NOT NULL,
    status                            text NOT NULL CONSTRAINT contract_status_chk CHECK (status IN ('trial', 'active', 'pastDue', 'cancelled', 'expired')),
    starts_at                         date NOT NULL,
    renews_at                         date,
    cancelled_at                      date,
    scheduled_change                  jsonb,
    current_price                     numeric(18,4),
    billing_period                    text
);

CREATE TABLE IF NOT EXISTS control.enforcement_policy (
    id                                uuid PRIMARY KEY NOT NULL,
    thresholds                        jsonb,
    is_hard_stop_allowed              boolean DEFAULT false,
    grace_days                        integer DEFAULT 7
);

CREATE TABLE IF NOT EXISTS control.go_live_readiness (
    id                                uuid PRIMARY KEY NOT NULL,
    tenant_id                         uuid,
    run_at                            timestamptz,
    status                            text CONSTRAINT go_live_readiness_status_chk CHECK (status IN ('notStarted', 'running', 'blocked', 'readyWithWarnings', 'ready')),
    groups                            jsonb,
    blockers                          integer,
    warnings                          integer,
    signed_off_by                     uuid,
    signed_off_at                     timestamptz
);

CREATE TABLE IF NOT EXISTS control.idempotency_record (
    id                                uuid PRIMARY KEY NOT NULL,
    idempotency_key                   uuid NOT NULL,
    operation_id                      text NOT NULL CONSTRAINT idempotency_record_operation_id_chk CHECK (char_length(operation_id) <= 100),
    request_hash                      text NOT NULL CONSTRAINT idempotency_record_request_hash_chk CHECK (char_length(request_hash) <= 64),
    status                            text NOT NULL CONSTRAINT idempotency_record_status_chk CHECK (status IN ('inProgress', 'completed')),
    response_status                   integer,
    response_body                     jsonb,
    operator_principal_id             uuid,
    created_at                        timestamptz NOT NULL,
    expires_at                        timestamptz NOT NULL
);

ALTER TABLE control.licence_add_on DROP CONSTRAINT IF EXISTS licence_add_on_module_key_chk;

ALTER TABLE control.licence_add_on ADD CONSTRAINT licence_add_on_module_key_chk CHECK (module_key IN ('core', 'ticketing', 'access', 'fnb', 'retail', 'inventory', 'seating', 'membership', 'marketing', 'resources', 'queue', 'transport', 'games', 'maintenance', 'accreditation', 'partner', 'developerApi', 'analytics', 'ai', 'poweredByRemoval')) NOT VALID;

CREATE TABLE IF NOT EXISTS control.licensing_model (
    id                                uuid PRIMARY KEY NOT NULL,
    code                              text NOT NULL,
    name                              text,
    billable_unit                     text NOT NULL CONSTRAINT licensing_model_billable_unit_chk CHECK (billable_unit IN ('perVenue', 'perAdmission', 'perTransaction', 'perActiveUser', 'perDevice', 'perModule', 'flatFee', 'revenueShare')),
    unit_price                        numeric(18,4),
    revenue_share_percent             numeric(18,4),
    minimum_guarantee                 numeric(18,4),
    minimum_guarantee_period          text CONSTRAINT licensing_model_minimum_guarantee_period_chk CHECK (minimum_guarantee_period IN ('monthly', 'quarterly', 'annual')),
    on_below_minimum                  text DEFAULT 'chargeMinimum' CONSTRAINT licensing_model_on_below_minimum_chk CHECK (on_below_minimum IN ('chargeMinimum', 'carryForward', 'waive')),
    included_allowances               jsonb,
    overage_pricing                   jsonb,
    tier_code                         text,
    effective_from                    date
);

CREATE TABLE IF NOT EXISTS control.module_listing (
    id                                uuid PRIMARY KEY NOT NULL,
    module_code                       text NOT NULL,
    name                              text,
    description                       text,
    category                          text,
    requires_modules                  text[],
    incompatible_with_modules         text[],
    included_in_tiers                 text[],
    list_price                        numeric(18,4),
    pricing_basis                     text CONSTRAINT module_listing_pricing_basis_chk CHECK (pricing_basis IN ('included', 'flatFee', 'perVenue', 'perUnit', 'revenueShare', 'metered')),
    metered_metric                    text,
    metered_unit_size                 integer,
    provisioning_minutes              integer,
    requires_professional_services    boolean DEFAULT false,
    status                            text CONSTRAINT module_listing_status_chk CHECK (status IN ('available', 'beta', 'deprecated', 'withdrawn'))
);

CREATE TABLE IF NOT EXISTS control.outbox (
    id                                uuid PRIMARY KEY NOT NULL,
    event_id                          uuid NOT NULL,
    event_name                        text NOT NULL,
    event_version                     integer,
    tenant_id                         uuid NOT NULL,
    aggregate_type                    text NOT NULL,
    aggregate_id                      uuid NOT NULL,
    payload                           jsonb NOT NULL,
    sequence                          integer NOT NULL,
    trace_id                          text CONSTRAINT outbox_trace_id_chk CHECK (char_length(trace_id) <= 64),
    occurred_at                       timestamptz NOT NULL,
    published_at                      timestamptz,
    attempts                          integer DEFAULT 0,
    last_error                        text,
    created_at                        timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS control.plan (
    code                              text NOT NULL CONSTRAINT plan_code_chk CHECK (char_length(code) <= 64),
    name                              text NOT NULL CONSTRAINT plan_name_chk CHECK (char_length(name) <= 200),
    description                       text CONSTRAINT plan_description_chk CHECK (char_length(description) <= 1000),
    cell_tier                         text NOT NULL CONSTRAINT plan_cell_tier_chk CHECK (cell_tier IN ('shared', 'dedicated', 'isolated', 'clientHosted')),
    base_price                        numeric(18,4) NOT NULL,
    billing_period                    text CONSTRAINT plan_billing_period_chk CHECK (billing_period IN ('monthly', 'quarterly', 'annual')),
    includes_branded_app              boolean,
    included_ai_tokens                integer,
    request_limits                    jsonb,
    package_kind                      text DEFAULT 'standard' CONSTRAINT plan_package_kind_chk CHECK (package_kind IN ('standard', 'custom')),
    offered_to_tenant_id              uuid,
    id                                uuid NOT NULL,
    version                           text NOT NULL,
    is_active                         boolean NOT NULL,
    subscriber_count                  integer NOT NULL,
    published_at                      timestamptz,
    CONSTRAINT plan_pkey PRIMARY KEY (id, version)
);

CREATE TABLE IF NOT EXISTS control.plan_limit (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_version                      text NOT NULL,
    metric                            text NOT NULL,
    limit_value                       integer,
    is_overage_allowed                boolean,
    overage_unit_price                numeric(18,4)
);

CREATE TABLE IF NOT EXISTS control.plan_module (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_version                      text NOT NULL,
    licensed_module                   text NOT NULL
);

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'release' AND column_name = 'plan_id' AND is_nullable = 'NO') THEN ALTER TABLE control.release ALTER COLUMN plan_id DROP NOT NULL; END IF; END $$;

ALTER TABLE control.tenant ADD COLUMN IF NOT EXISTS plan_version text;

ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_plan_id_when_chk;

ALTER TABLE control.tenant ADD CONSTRAINT tenant_plan_id_when_chk CHECK (plan_version IS NULL OR plan_id IS NOT NULL) NOT VALID;

ALTER TABLE control.tenant VALIDATE CONSTRAINT tenant_plan_id_when_chk;

ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_plan_version_when_chk;

ALTER TABLE control.tenant ADD CONSTRAINT tenant_plan_version_when_chk CHECK (plan_id IS NULL OR plan_version IS NOT NULL) NOT VALID;

ALTER TABLE control.tenant VALIDATE CONSTRAINT tenant_plan_version_when_chk;

ALTER TABLE control.tenant_domain DROP CONSTRAINT IF EXISTS tenant_domain_channel_chk;

ALTER TABLE control.tenant_domain ADD CONSTRAINT tenant_domain_channel_chk CHECK (channel IN ('guestWeb', 'backOffice', 'partnerPortal', 'developerPortal', 'staffApp')) NOT VALID;

ALTER TABLE control.tenant_domain VALIDATE CONSTRAINT tenant_domain_channel_chk;

CREATE TABLE IF NOT EXISTS control.tier_allowance (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_version                      text NOT NULL,
    code                              text NOT NULL CONSTRAINT tier_allowance_code_chk CHECK (char_length(code) <= 100),
    name                              text NOT NULL CONSTRAINT tier_allowance_name_chk CHECK (char_length(name) <= 150),
    limit_value                       numeric(18,4),
    period                            text CONSTRAINT tier_allowance_period_chk CHECK (char_length(period) <= 20),
    is_unlimited                      boolean NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.tier_module (
    id                                uuid PRIMARY KEY NOT NULL,
    plan_id                           uuid NOT NULL,
    plan_version                      text NOT NULL,
    code                              text NOT NULL CONSTRAINT tier_module_code_chk CHECK (char_length(code) <= 100),
    is_included                       boolean NOT NULL,
    notes                             text CONSTRAINT tier_module_notes_chk CHECK (char_length(notes) <= 500),
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    updated_at                        timestamptz
);

CREATE TABLE IF NOT EXISTS control.trial_config (
    id                                uuid PRIMARY KEY NOT NULL,
    tier_code                         text,
    duration_days                     integer DEFAULT 30,
    included_modules                  text[],
    usage_caps                        jsonb,
    requires_payment_method_up_front  boolean DEFAULT false,
    conversion_offer_percent          numeric(18,4),
    notice_days_before_expiry         integer[],
    on_expiry                         text DEFAULT 'suspend' CONSTRAINT trial_config_on_expiry_chk CHECK (on_expiry IN ('suspend', 'convert', 'decommission')),
    retain_data_days                  integer DEFAULT 90
);

CREATE TABLE IF NOT EXISTS control.vsi_assessment (
    id                                uuid PRIMARY KEY NOT NULL,
    organisation_name                 text,
    contact_email                     text,
    venue_type                        text,
    answers                           jsonb,
    requested_modules                 text[],
    submitted_at                      timestamptz
);

CREATE TABLE IF NOT EXISTS control.vsi_model (
    id                                uuid PRIMARY KEY NOT NULL,
    version                           integer,
    factors                           jsonb,
    tiers                             jsonb,
    published_at                      timestamptz
);

ALTER TABLE control.webhook_delivery ADD COLUMN IF NOT EXISTS replay_id uuid;

CREATE TABLE IF NOT EXISTS control.webhook_replay (
    id                                uuid PRIMARY KEY NOT NULL,
    subscription_id                   uuid NOT NULL,
    window_from                       timestamptz NOT NULL,
    window_to                         timestamptz,
    event_types                       text[],
    status                            text NOT NULL DEFAULT 'queued' CONSTRAINT webhook_replay_status_chk CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    queued_at                         timestamptz NOT NULL,
    completed_at                      timestamptz,
    requested_by_principal_id         uuid
);

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'audit_record_tenant_id_fkey' AND conrelid = to_regclass('control.audit_record')) THEN ALTER TABLE control.audit_record ADD CONSTRAINT audit_record_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'capacity_pack_tenant_id_fkey' AND conrelid = to_regclass('control.capacity_pack')) THEN ALTER TABLE control.capacity_pack ADD CONSTRAINT capacity_pack_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cell_endpoint_cell_id_fkey' AND conrelid = to_regclass('control.cell_endpoint')) THEN ALTER TABLE control.cell_endpoint ADD CONSTRAINT cell_endpoint_cell_id_fkey FOREIGN KEY (cell_id) REFERENCES control.cell(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'contract_plan_id_fkey' AND conrelid = to_regclass('control.contract')) THEN ALTER TABLE control.contract ADD CONSTRAINT contract_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'contract_tenant_id_fkey' AND conrelid = to_regclass('control.contract')) THEN ALTER TABLE control.contract ADD CONSTRAINT contract_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'go_live_readiness_tenant_id_fkey' AND conrelid = to_regclass('control.go_live_readiness')) THEN ALTER TABLE control.go_live_readiness ADD CONSTRAINT go_live_readiness_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES control.tenant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'plan_offered_to_tenant_id_fkey' AND conrelid = to_regclass('control.plan')) THEN ALTER TABLE control.plan ADD CONSTRAINT plan_offered_to_tenant_id_fkey FOREIGN KEY (offered_to_tenant_id) REFERENCES control.tenant(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'plan_limit_plan_id_fkey' AND conrelid = to_regclass('control.plan_limit')) THEN ALTER TABLE control.plan_limit ADD CONSTRAINT plan_limit_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'plan_module_plan_id_fkey' AND conrelid = to_regclass('control.plan_module')) THEN ALTER TABLE control.plan_module ADD CONSTRAINT plan_module_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tier_allowance_plan_id_fkey' AND conrelid = to_regclass('control.tier_allowance')) THEN ALTER TABLE control.tier_allowance ADD CONSTRAINT tier_allowance_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'tier_module_plan_id_fkey' AND conrelid = to_regclass('control.tier_module')) THEN ALTER TABLE control.tier_module ADD CONSTRAINT tier_module_plan_id_fkey FOREIGN KEY (plan_id, plan_version) REFERENCES control.plan(id, version); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'webhook_delivery_replay_id_fkey' AND conrelid = to_regclass('control.webhook_delivery')) THEN ALTER TABLE control.webhook_delivery ADD CONSTRAINT webhook_delivery_replay_id_fkey FOREIGN KEY (replay_id) REFERENCES control.webhook_replay(id); END IF; END $$;

DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'webhook_replay_subscription_id_fkey' AND conrelid = to_regclass('control.webhook_replay')) THEN ALTER TABLE control.webhook_replay ADD CONSTRAINT webhook_replay_subscription_id_fkey FOREIGN KEY (subscription_id) REFERENCES control.webhook_subscription(id); END IF; END $$;

CREATE INDEX IF NOT EXISTS capacity_pack_invoice_id_idx ON control.capacity_pack (invoice_id);

CREATE INDEX IF NOT EXISTS contract_plan_id_plan_version_idx ON control.contract (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS plan_limit_plan_id_plan_version_idx ON control.plan_limit (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS plan_module_plan_id_plan_version_idx ON control.plan_module (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS tenant_plan_id_plan_version_idx ON control.tenant (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS tier_allowance_plan_id_plan_version_idx ON control.tier_allowance (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS tier_module_plan_id_plan_version_idx ON control.tier_module (plan_id, plan_version);

CREATE INDEX IF NOT EXISTS audit_record_tenant_id_idx ON control.audit_record (tenant_id);

CREATE INDEX IF NOT EXISTS capacity_pack_tenant_id_idx ON control.capacity_pack (tenant_id);

CREATE INDEX IF NOT EXISTS cell_endpoint_cell_id_idx ON control.cell_endpoint (cell_id);

CREATE INDEX IF NOT EXISTS contract_tenant_id_idx ON control.contract (tenant_id);

CREATE INDEX IF NOT EXISTS go_live_readiness_tenant_id_idx ON control.go_live_readiness (tenant_id);

CREATE INDEX IF NOT EXISTS plan_offered_to_tenant_id_idx ON control.plan (offered_to_tenant_id);

CREATE INDEX IF NOT EXISTS webhook_delivery_replay_id_idx ON control.webhook_delivery (replay_id);

CREATE INDEX IF NOT EXISTS webhook_replay_subscription_id_idx ON control.webhook_replay (subscription_id);

CREATE UNIQUE INDEX IF NOT EXISTS plan_code_uniq ON control.plan (lower(code));

CREATE UNIQUE INDEX IF NOT EXISTS idempotency_record_idempotency_key_operation_id_uniq ON control.idempotency_record (idempotency_key, lower(operation_id));

CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_hostname_uniq ON control.tenant_domain (lower(hostname)) WHERE status = 'active';

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0108', 'after r1 (9cec72d): 19 table(s), 4 column(s), 18 index(es), 18 other statement(s)', 'b4f6ccddc3ad907a3725f55c776c06557dfa5ab7bcb514f51ed8c915e4b5361a')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.tenant_domain_hostname_uniq;
-- DROP INDEX IF EXISTS control.idempotency_record_idempotency_key_operation_id_uniq;
-- DROP INDEX IF EXISTS control.plan_code_uniq;
-- DROP INDEX IF EXISTS control.webhook_replay_subscription_id_idx;
-- DROP INDEX IF EXISTS control.webhook_delivery_replay_id_idx;
-- DROP INDEX IF EXISTS control.plan_offered_to_tenant_id_idx;
-- DROP INDEX IF EXISTS control.go_live_readiness_tenant_id_idx;
-- DROP INDEX IF EXISTS control.contract_tenant_id_idx;
-- DROP INDEX IF EXISTS control.cell_endpoint_cell_id_idx;
-- DROP INDEX IF EXISTS control.capacity_pack_tenant_id_idx;
-- DROP INDEX IF EXISTS control.audit_record_tenant_id_idx;
-- DROP INDEX IF EXISTS control.tier_module_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.tier_allowance_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.tenant_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.plan_module_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.plan_limit_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.contract_plan_id_plan_version_idx;
-- DROP INDEX IF EXISTS control.capacity_pack_invoice_id_idx;
-- ALTER TABLE control.webhook_delivery DROP CONSTRAINT IF EXISTS webhook_delivery_replay_id_fkey;
-- DROP TABLE IF EXISTS control.webhook_replay;
-- ALTER TABLE control.webhook_delivery DROP COLUMN IF EXISTS replay_id;
-- DROP TABLE IF EXISTS control.vsi_model;
-- DROP TABLE IF EXISTS control.vsi_assessment;
-- DROP TABLE IF EXISTS control.trial_config;
-- DROP TABLE IF EXISTS control.tier_module;
-- DROP TABLE IF EXISTS control.tier_allowance;
-- ALTER TABLE control.tenant_domain DROP CONSTRAINT IF EXISTS tenant_domain_channel_chk; ALTER TABLE control.tenant_domain ADD CONSTRAINT tenant_domain_channel_chk CHECK (channel IN ('guestWeb', 'backOffice', 'partnerPortal', 'developerPortal')) NOT VALID;
-- ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_plan_version_when_chk;
-- ALTER TABLE control.tenant DROP CONSTRAINT IF EXISTS tenant_plan_id_when_chk;
-- ALTER TABLE control.tenant DROP COLUMN IF EXISTS plan_version;
-- ALTER TABLE control.release ALTER COLUMN plan_id SET NOT NULL;
-- DROP TABLE IF EXISTS control.plan_module;
-- DROP TABLE IF EXISTS control.plan_limit;
-- DROP TABLE IF EXISTS control.plan;
-- DROP TABLE IF EXISTS control.outbox;
-- DROP TABLE IF EXISTS control.module_listing;
-- DROP TABLE IF EXISTS control.licensing_model;
-- ALTER TABLE control.licence_add_on DROP CONSTRAINT IF EXISTS licence_add_on_module_key_chk;
-- DROP TABLE IF EXISTS control.idempotency_record;
-- DROP TABLE IF EXISTS control.go_live_readiness;
-- DROP TABLE IF EXISTS control.enforcement_policy;
-- DROP TABLE IF EXISTS control.contract;
-- ALTER TABLE control.cell_tenant DROP COLUMN IF EXISTS root_scope_path;
-- ALTER TABLE control.cell_job DROP COLUMN IF EXISTS target_tier;
-- DROP TABLE IF EXISTS control.cell_endpoint;
-- DROP TABLE IF EXISTS control.capacity_pack;
-- DROP TABLE IF EXISTS control.audit_record;
-- DELETE FROM platform.schema_version WHERE version = 'V0108';
