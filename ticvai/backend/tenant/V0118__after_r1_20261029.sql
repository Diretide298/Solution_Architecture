-- V0118 -- tenant database, after r1 (9cec72d) (20261029).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 6 table(s), 14 column(s), 20 index(es), 25 other statement(s), 21 row-level security polic(ies) re-applied.

CREATE TABLE IF NOT EXISTS approvals.matrix_version (
    approval_matrix_id                uuid NOT NULL,
    version                           integer NOT NULL,
    is_active                         boolean NOT NULL,
    created_at                        timestamptz NOT NULL,
    CONSTRAINT matrix_version_pkey PRIMARY KEY (approval_matrix_id, version)
);

DO $$ BEGIN IF to_regclass('approvals.rule') IS NOT NULL THEN
ALTER TABLE approvals.rule ADD COLUMN IF NOT EXISTS matrix_version integer;
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.media_usage') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'assets' AND table_name = 'media_usage' AND column_name = 'surface') THEN
ALTER TABLE assets.media_usage DROP CONSTRAINT IF EXISTS media_usage_surface_chk;
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.media_usage') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'assets' AND table_name = 'media_usage' AND column_name = 'surface') THEN
ALTER TABLE assets.media_usage ADD CONSTRAINT media_usage_surface_chk CHECK (surface IN ('tenantBranding', 'homepageBanner', 'promoBlock', 'contentPage', 'product', 'event', 'menuItem', 'merchandise', 'workOrder', 'incident', 'inspection', 'campaign', 'aiConfigSource', 'aiHistoryImport', 'aiLayoutDraft', 'workOrderAttachment', 'seatingSection', 'transportNetworkImport', 'venueMap', 'venueMapVersion', 'mediaCollectionCover')) NOT VALID;
END IF; END $$;

DO $$ BEGIN IF to_regclass('assets.media_usage') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'assets' AND table_name = 'media_usage' AND column_name = 'surface') THEN
ALTER TABLE assets.media_usage VALIDATE CONSTRAINT media_usage_surface_chk;
END IF; END $$;

CREATE TABLE IF NOT EXISTS identity.guest_upload_ref (
    id                                uuid PRIMARY KEY NOT NULL,
    upload_id                         uuid NOT NULL,
    subject_id                        uuid NOT NULL,
    purpose                           text NOT NULL CONSTRAINT guest_upload_ref_purpose_chk CHECK (purpose IN ('identityDocument', 'selfie')),
    status                            text NOT NULL CONSTRAINT guest_upload_ref_status_chk CHECK (status IN ('uploaded', 'deleted')),
    last_event_at                     timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('identity.sso_provider') IS NOT NULL THEN
ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS audience text DEFAULT 'staff' CONSTRAINT sso_provider_audience_chk CHECK (audience IN ('staff', 'guest'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.sso_provider') IS NOT NULL THEN
ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS guest_provider text CONSTRAINT sso_provider_guest_provider_chk CHECK (guest_provider IN ('apple', 'google', 'uaePass'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.sso_provider') IS NOT NULL THEN
ALTER TABLE identity.sso_provider ADD COLUMN IF NOT EXISTS authorization_url text CONSTRAINT sso_provider_authorization_url_chk CHECK (char_length(authorization_url) <= 2000);
END IF; END $$;

CREATE TABLE IF NOT EXISTS identity.subject_data_export_part (
    id                                uuid PRIMARY KEY NOT NULL,
    export_id                         uuid NOT NULL,
    owner                             text NOT NULL CONSTRAINT subject_data_export_part_owner_chk CHECK (char_length(owner) <= 40),
    file_ref                          text NOT NULL CONSTRAINT subject_data_export_part_file_ref_chk CHECK (char_length(file_ref) <= 500),
    tables                            text[],
    row_count                         integer NOT NULL,
    written_at                        timestamptz NOT NULL
);

DO $$ BEGIN IF to_regclass('marketing.form_definition_field') IS NOT NULL THEN
ALTER TABLE marketing.form_definition_field ADD COLUMN IF NOT EXISTS option_labels jsonb;
END IF; END $$;

CREATE TABLE IF NOT EXISTS marketing.seo_metadata (
    id                                uuid PRIMARY KEY NOT NULL,
    entity_kind                       text NOT NULL CONSTRAINT seo_metadata_entity_kind_chk CHECK (entity_kind IN ('contentPage', 'product', 'event', 'performance', 'membership', 'promotion', 'venue')),
    entity_id                         uuid NOT NULL,
    locale                            text,
    title                             text,
    meta_description                  text,
    keywords                          text[],
    canonical_url                     text,
    slug                              text,
    hreflang                          jsonb,
    schema_org_type                   text,
    open_graph                        jsonb,
    is_auto_generated                 boolean DEFAULT true,
    is_excluded_from_index            boolean DEFAULT false,
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF to_regclass('payments.credit_account') IS NOT NULL THEN
ALTER TABLE payments.credit_account ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT credit_account_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.outlet') IS NOT NULL THEN
ALTER TABLE platform.outlet ADD COLUMN IF NOT EXISTS order_number_prefix text CONSTRAINT outlet_order_number_prefix_chk CHECK (order_number_prefix IN ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z') AND char_length(order_number_prefix) <= 1);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.venue_settings') IS NOT NULL THEN
ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS city text CONSTRAINT venue_settings_city_chk CHECK (char_length(city) <= 120);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.venue_settings') IS NOT NULL THEN
ALTER TABLE platform.venue_settings ADD COLUMN IF NOT EXISTS opening_hours jsonb;
END IF; END $$;

CREATE TABLE IF NOT EXISTS venuemap.visit_planner_question (
    question_key                      text NOT NULL CONSTRAINT visit_planner_question_question_key_chk CHECK (question_key IN ('party', 'heights', 'dates', 'dayVenues', 'pace', 'interests', 'retail', 'cuisine')),
    is_enabled                        boolean NOT NULL DEFAULT true,
    is_required                       boolean NOT NULL DEFAULT false,
    sort_order                        integer NOT NULL,
    label                             text NOT NULL CONSTRAINT visit_planner_question_label_chk CHECK (char_length(label) <= 120),
    label_localised                   jsonb,
    help                              text CONSTRAINT visit_planner_question_help_chk CHECK (char_length(help) <= 300),
    help_localised                    jsonb,
    scope_path                        ltree NOT NULL,
    updated_at                        timestamptz,
    CONSTRAINT visit_planner_question_pkey PRIMARY KEY (scope_path, question_key)
);

DO $$ BEGIN IF to_regclass('wallet.funding_rule') IS NOT NULL THEN
ALTER TABLE wallet.funding_rule ADD COLUMN IF NOT EXISTS version integer NOT NULL DEFAULT 1;
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.refund_policy') IS NOT NULL THEN
ALTER TABLE wallet.refund_policy ADD COLUMN IF NOT EXISTS version integer NOT NULL DEFAULT 1;
END IF; END $$;

CREATE TABLE IF NOT EXISTS whitelabel.received_release (
    id                                uuid PRIMARY KEY NOT NULL,
    release_id                        uuid NOT NULL,
    version                           text NOT NULL,
    guest_release_notes               jsonb,
    received_at                       timestamptz NOT NULL,
    scope_path                        ltree NOT NULL
);

DO $$ BEGIN IF to_regclass('workforce.job_title') IS NOT NULL THEN
ALTER TABLE workforce.job_title ADD COLUMN IF NOT EXISTS scope_path ltree;
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.leave_type') IS NOT NULL THEN
ALTER TABLE workforce.leave_type ADD COLUMN IF NOT EXISTS scope_path ltree;
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.shift') IS NOT NULL THEN
ALTER TABLE workforce.shift ADD COLUMN IF NOT EXISTS scope_path ltree;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.matrix_version') IS NOT NULL AND to_regclass('approvals.matrix') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix_version' AND column_name = 'approval_matrix_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'matrix_version_approval_matrix_id_fkey' AND conrelid = to_regclass('approvals.matrix_version')) THEN
ALTER TABLE approvals.matrix_version ADD CONSTRAINT matrix_version_approval_matrix_id_fkey FOREIGN KEY (approval_matrix_id) REFERENCES approvals.matrix(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.guest_upload_ref') IS NOT NULL AND to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'guest_upload_ref' AND column_name = 'subject_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'guest_upload_ref_subject_id_fkey' AND conrelid = to_regclass('identity.guest_upload_ref')) THEN
ALTER TABLE identity.guest_upload_ref ADD CONSTRAINT guest_upload_ref_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES pii.subject(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND to_regclass('identity.subject_data_export') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_data_export_part_export_id_fkey' AND conrelid = to_regclass('identity.subject_data_export_part')) THEN
ALTER TABLE identity.subject_data_export_part ADD CONSTRAINT subject_data_export_part_export_id_fkey FOREIGN KEY (export_id) REFERENCES identity.subject_data_export(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ai' AND table_name = 'proposed_action' AND column_name = 'map_id') THEN
CREATE INDEX IF NOT EXISTS proposed_action_map_id_idx ON ai.proposed_action (map_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.privacy_request') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'privacy_request' AND column_name = 'approval_request_id') THEN
CREATE INDEX IF NOT EXISTS privacy_request_approval_request_id_idx ON marketing.privacy_request (approval_request_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.matrix_version') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix_version' AND column_name = 'approval_matrix_id') THEN
CREATE INDEX IF NOT EXISTS matrix_version_approval_matrix_id_idx ON approvals.matrix_version (approval_matrix_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.guest_upload_ref') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'guest_upload_ref' AND column_name = 'subject_id') THEN
CREATE INDEX IF NOT EXISTS guest_upload_ref_subject_id_idx ON identity.guest_upload_ref (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') THEN
CREATE INDEX IF NOT EXISTS subject_data_export_part_export_id_idx ON identity.subject_data_export_part (export_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_preference') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_preference' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_preference_subject_id_uniq ON marketing.guest_preference (subject_id) WHERE subject_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_profile_subject_id_uniq ON marketing.guest_profile (subject_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.credit_lot') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'credit_lot' AND column_name = 'order_line_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS credit_lot_order_line_id_uniq ON wallet.credit_lot (order_line_id) WHERE order_line_id IS NOT NULL;
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.matrix') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix' AND column_name = 'kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix' AND column_name = 'scope_path') THEN
CREATE UNIQUE INDEX IF NOT EXISTS matrix_kind_scope_path_uniq ON approvals.matrix (lower(kind), scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.rule') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'code') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'matrix_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'rule' AND column_name = 'matrix_version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS rule_matrix_id_matrix_version_code_uniq ON approvals.rule (matrix_id, matrix_version, lower(code));
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.guest_upload_ref') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'guest_upload_ref' AND column_name = 'upload_id') THEN
CREATE UNIQUE INDEX IF NOT EXISTS guest_upload_ref_upload_id_uniq ON identity.guest_upload_ref (upload_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'export_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'subject_data_export_part' AND column_name = 'owner') THEN
CREATE UNIQUE INDEX IF NOT EXISTS subject_data_export_part_export_id_owner_uniq ON identity.subject_data_export_part (export_id, lower(owner));
END IF; END $$;

DO $$ BEGIN IF to_regclass('tenancy.device_firmware') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'device_kind') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'tenancy' AND table_name = 'device_firmware' AND column_name = 'version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS device_firmware_device_kind_version_uniq ON tenancy.device_firmware (lower(device_kind), lower(version));
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.received_release') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'received_release' AND column_name = 'release_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'received_release' AND column_name = 'scope_path') THEN
CREATE UNIQUE INDEX IF NOT EXISTS received_release_scope_path_release_id_uniq ON whitelabel.received_release (scope_path, release_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.job_title') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'job_title' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS job_title_scope_path_idx ON workforce.job_title USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.leave_type') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'leave_type' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS leave_type_scope_path_idx ON workforce.leave_type USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.received_release') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'received_release' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS received_release_scope_path_idx ON whitelabel.received_release USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.seo_metadata') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'seo_metadata' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS seo_metadata_scope_path_idx ON marketing.seo_metadata USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.shift') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'shift' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS shift_scope_path_idx ON workforce.shift USING gist (scope_path);
END IF; END $$;

DO $$ BEGIN IF to_regclass('venuemap.visit_planner_question') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'venuemap' AND table_name = 'visit_planner_question' AND column_name = 'scope_path') THEN
CREATE INDEX IF NOT EXISTS visit_planner_question_scope_path_idx ON venuemap.visit_planner_question USING gist (scope_path);
END IF; END $$;

CREATE OR REPLACE FUNCTION platform.apply_grant_holder_subject_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    PERFORM platform.apply_split_rls(target,
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)',
        'platform.grant_holder() OR platform.subject_in_scope(subject_id)');
END
$$;

DO $$ BEGIN IF to_regclass('marketing.seo_metadata') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'seo_metadata' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('marketing.seo_metadata'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('venuemap.visit_planner_question') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'venuemap' AND table_name = 'visit_planner_question' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('venuemap.visit_planner_question'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('whitelabel.received_release') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'whitelabel' AND table_name = 'received_release' AND column_name = 'scope_path') THEN
PERFORM platform.apply_scope_rls('whitelabel.received_release'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'granted_by_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'over_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('identity.delegated_access'::regclass);
PERFORM platform.apply_split_rls('identity.delegated_access'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, over_subject_id))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.refresh_token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'principal_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'refresh_token' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('identity.refresh_token'::regclass);
PERFORM platform.apply_own_row_rls('identity.refresh_token'::regclass, 'principal_id', 'subject_id');
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.communication_policy_decision') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'communication_policy_decision' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.communication_policy_decision'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.communication_policy_decision'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.consent_record') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'consent_record' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.consent_record'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.consent_record'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.cookie_banner_design') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'cookie_banner_design' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('marketing.cookie_banner_design'::regclass);
PERFORM platform.apply_read_beneath_rls('marketing.cookie_banner_design'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.form_submission') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'form_submission' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.form_submission'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('marketing.form_submission'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.tracking_technology') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'tracking_technology' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('marketing.tracking_technology'::regclass);
PERFORM platform.apply_read_beneath_rls('marketing.tracking_technology'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.cart'::regclass);
PERFORM platform.apply_split_rls('orders.cart'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_event') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_event' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('orders.order_event'::regclass);
PERFORM platform.apply_split_rls('orders.order_event'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.order_line') IS NOT NULL AND to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'order_line' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('orders.order_line'::regclass);
PERFORM platform.apply_split_rls('orders.order_line'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.sales_order') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'sales_order' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('orders.sales_order'::regclass);
PERFORM platform.apply_split_rls('orders.sales_order'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('payments.token') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'token' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('payments.token'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('payments.token'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.balance') IS NOT NULL THEN
PERFORM platform.drop_rls_policies('wallet.balance'::regclass);
PERFORM platform.apply_grant_holder_read_rls('wallet.balance'::regclass, 'platform.grant_holder()');
END IF; END $$;

DO $$ BEGIN IF to_regclass('wallet.wallet') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'wallet' AND table_name = 'wallet' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('wallet.wallet'::regclass);
PERFORM platform.apply_grant_holder_subject_rls('wallet.wallet'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.employee') IS NOT NULL THEN
PERFORM platform.drop_rls_policies('workforce.employee'::regclass);
PERFORM platform.apply_grant_holder_read_rls('workforce.employee'::regclass, 'platform.tenant_root_in_scope()');
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.job_title') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'job_title' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('workforce.job_title'::regclass);
PERFORM platform.apply_read_beneath_rls('workforce.job_title'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.leave_type') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'leave_type' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('workforce.leave_type'::regclass);
PERFORM platform.apply_read_beneath_rls('workforce.leave_type'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.shift') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'shift' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('workforce.shift'::regclass);
PERFORM platform.apply_read_beneath_rls('workforce.shift'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('approvals.matrix_version') IS NOT NULL AND to_regclass('approvals.matrix') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'approvals' AND table_name = 'matrix_version' AND column_name = 'approval_matrix_id') THEN
PERFORM platform.apply_parent_split_rls('approvals.matrix_version'::regclass, 'approval_matrix_id', 'approvals.matrix'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.guest_profile') IS NOT NULL AND to_regclass('marketing.segment') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'guest_profile' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('marketing.guest_profile'::regclass);
PERFORM platform.apply_split_rls('marketing.guest_profile'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)', '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND EXISTS (SELECT 1 FROM marketing.segment pr WHERE pr.id = marketing.guest_profile.segment_id)) OR platform.subject_in_scope(subject_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('orders.cart_line') IS NOT NULL AND to_regclass('orders.cart') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'orders' AND table_name = 'cart_line' AND column_name = 'cart_id') THEN
PERFORM platform.drop_rls_policies('orders.cart_line'::regclass);
PERFORM platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('workforce.leave_balance') IS NOT NULL AND to_regclass('workforce.leave_type') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'leave_balance' AND column_name = 'type_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'workforce' AND table_name = 'leave_type' AND column_name = 'id') THEN
PERFORM platform.drop_rls_policies('workforce.leave_balance'::regclass);
PERFORM platform.apply_parent_split_rls('workforce.leave_balance'::regclass, 'type_id', 'workforce.leave_type'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.guest_upload_ref') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'guest_upload_ref' AND column_name = 'subject_id') THEN
PERFORM platform.apply_subject_rls('identity.guest_upload_ref'::regclass);
END IF; END $$;

DO $$ BEGIN IF to_regclass('identity.subject_data_export_part') IS NOT NULL THEN
PERFORM platform.apply_tenant_rls('identity.subject_data_export_part'::regclass);
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'catalogue') THEN GRANT USAGE ON SCHEMA catalogue TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.variant') IS NOT NULL THEN GRANT SELECT ON catalogue.variant TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product') IS NOT NULL THEN GRANT SELECT ON catalogue.product TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product_media') IS NOT NULL THEN GRANT SELECT ON catalogue.product_media TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price') IS NOT NULL THEN GRANT SELECT ON catalogue.price TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price_assignment') IS NOT NULL THEN GRANT SELECT ON catalogue.price_assignment TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.price_list') IS NOT NULL THEN GRANT SELECT ON catalogue.price_list TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.performance') IS NOT NULL THEN GRANT SELECT ON catalogue.performance TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('catalogue.product_category') IS NOT NULL THEN GRANT SELECT ON catalogue.product_category TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('platform.workstation') IS NOT NULL THEN GRANT SELECT ON platform.workstation TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'pii') THEN GRANT USAGE ON SCHEMA pii TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'access') AND to_regclass('pii.subject') IS NOT NULL THEN GRANT SELECT ON pii.subject TO access; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'identity') THEN GRANT USAGE ON SCHEMA identity TO operations; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'operations') AND to_regclass('identity.sso_provider') IS NOT NULL THEN GRANT SELECT ON identity.sso_provider TO operations; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0118', 'after r1 (9cec72d): 6 table(s), 14 column(s), 20 index(es), 25 other statement(s), 21 row-level security polic(ies) re-applied', 'c50dc1c7d0b427092cfe744b2b969eb1402dff2f6217f0d2a989f33fae415b63')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- REVOKE SELECT ON identity.sso_provider FROM operations;
-- REVOKE USAGE ON SCHEMA identity FROM operations;
-- REVOKE SELECT ON pii.subject FROM access;
-- REVOKE USAGE ON SCHEMA pii FROM access;
-- REVOKE SELECT ON platform.workstation FROM operations;
-- REVOKE SELECT ON catalogue.product_category FROM operations;
-- REVOKE SELECT ON catalogue.performance FROM operations;
-- REVOKE SELECT ON catalogue.price_list FROM operations;
-- REVOKE SELECT ON catalogue.price_assignment FROM operations;
-- REVOKE SELECT ON catalogue.price FROM operations;
-- REVOKE SELECT ON catalogue.product_media FROM operations;
-- REVOKE SELECT ON catalogue.product FROM operations;
-- REVOKE SELECT ON catalogue.variant FROM operations;
-- REVOKE USAGE ON SCHEMA catalogue FROM operations;
-- SELECT platform.drop_rls_policies('workforce.leave_balance'::regclass); SELECT platform.apply_tenant_rls('workforce.leave_balance'::regclass);
-- SELECT platform.drop_rls_policies('orders.cart_line'::regclass); SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id'); SELECT platform.apply_parent_split_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id', '((platform.venue_in_scope(parent_row.venue_id)) OR (parent_row.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))');
-- SELECT platform.drop_rls_policies('marketing.guest_profile'::regclass); SELECT platform.apply_parent_rls('marketing.guest_profile'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
-- SELECT platform.drop_rls_policies('workforce.shift'::regclass); SELECT platform.apply_tenant_rls('workforce.shift'::regclass);
-- SELECT platform.drop_rls_policies('workforce.leave_type'::regclass); SELECT platform.apply_tenant_rls('workforce.leave_type'::regclass);
-- SELECT platform.drop_rls_policies('workforce.job_title'::regclass); SELECT platform.apply_tenant_rls('workforce.job_title'::regclass);
-- SELECT platform.drop_rls_policies('workforce.employee'::regclass); SELECT platform.apply_tenant_rls('workforce.employee'::regclass);
-- SELECT platform.drop_rls_policies('wallet.wallet'::regclass); SELECT platform.apply_subject_rls('wallet.wallet'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('wallet.wallet'::regclass);
-- SELECT platform.drop_rls_policies('wallet.balance'::regclass); SELECT platform.apply_tenant_rls('wallet.balance'::regclass); SELECT platform.apply_grant_holder_read_rls('wallet.balance'::regclass, 'platform.tenant_root_in_scope()');
-- SELECT platform.drop_rls_policies('payments.token'::regclass); SELECT platform.apply_subject_rls('payments.token'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('payments.token'::regclass);
-- SELECT platform.drop_rls_policies('orders.sales_order'::regclass); SELECT platform.apply_scope_rls('orders.sales_order'::regclass); SELECT platform.apply_split_rls('orders.sales_order'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.order_line'::regclass); SELECT platform.apply_venue_rls('orders.order_line'::regclass); SELECT platform.apply_split_rls('orders.order_line'::regclass, '(platform.venue_in_scope(venue_id)) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_line.sales_order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'platform.venue_in_scope(venue_id)');
-- SELECT platform.drop_rls_policies('orders.order_event'::regclass); SELECT platform.apply_scope_rls('orders.order_event'::regclass); SELECT platform.apply_split_rls('orders.order_event'::regclass, '(scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (EXISTS (SELECT 1 FROM orders.sales_order gp WHERE gp.id = orders.order_event.order_id AND gp.subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid)))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
-- SELECT platform.drop_rls_policies('orders.cart'::regclass); SELECT platform.apply_venue_rls('orders.cart'::regclass); SELECT platform.apply_split_rls('orders.cart'::regclass, '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', '(platform.venue_in_scope(venue_id)) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))');
-- SELECT platform.drop_rls_policies('marketing.tracking_technology'::regclass); SELECT platform.apply_scope_rls('marketing.tracking_technology'::regclass);
-- SELECT platform.drop_rls_policies('marketing.form_submission'::regclass); SELECT platform.apply_subject_rls('marketing.form_submission'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('marketing.form_submission'::regclass);
-- SELECT platform.drop_rls_policies('marketing.cookie_banner_design'::regclass); SELECT platform.apply_scope_rls('marketing.cookie_banner_design'::regclass);
-- SELECT platform.drop_rls_policies('marketing.consent_record'::regclass); SELECT platform.apply_subject_rls('marketing.consent_record'::regclass); SELECT platform.apply_grant_holder_subject_read_rls('marketing.consent_record'::regclass);
-- SELECT platform.drop_rls_policies('marketing.communication_policy_decision'::regclass); SELECT platform.apply_subject_rls('marketing.communication_policy_decision'::regclass);
-- SELECT platform.drop_rls_policies('identity.refresh_token'::regclass); SELECT platform.apply_tenant_rls('identity.refresh_token'::regclass); SELECT platform.apply_subject_rls('identity.refresh_token'::regclass);
-- SELECT platform.drop_rls_policies('identity.delegated_access'::regclass); SELECT platform.apply_scope_rls('identity.delegated_access'::regclass); SELECT platform.apply_split_rls('identity.delegated_access'::regclass, 'platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '(platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, over_subject_id))');
-- DROP INDEX IF EXISTS venuemap.visit_planner_question_scope_path_idx;
-- DROP INDEX IF EXISTS workforce.shift_scope_path_idx;
-- DROP INDEX IF EXISTS marketing.seo_metadata_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.received_release_scope_path_idx;
-- DROP INDEX IF EXISTS workforce.leave_type_scope_path_idx;
-- DROP INDEX IF EXISTS workforce.job_title_scope_path_idx;
-- DROP INDEX IF EXISTS whitelabel.received_release_scope_path_release_id_uniq;
-- DROP INDEX IF EXISTS tenancy.device_firmware_device_kind_version_uniq;
-- DROP INDEX IF EXISTS identity.subject_data_export_part_export_id_owner_uniq;
-- DROP INDEX IF EXISTS identity.guest_upload_ref_upload_id_uniq;
-- DROP INDEX IF EXISTS approvals.rule_matrix_id_matrix_version_code_uniq;
-- DROP INDEX IF EXISTS approvals.matrix_kind_scope_path_uniq;
-- DROP INDEX IF EXISTS wallet.credit_lot_order_line_id_uniq;
-- DROP INDEX IF EXISTS marketing.guest_profile_subject_id_uniq;
-- DROP INDEX IF EXISTS marketing.guest_preference_subject_id_uniq;
-- DROP INDEX IF EXISTS identity.subject_data_export_part_export_id_idx;
-- DROP INDEX IF EXISTS identity.guest_upload_ref_subject_id_idx;
-- DROP INDEX IF EXISTS approvals.matrix_version_approval_matrix_id_idx;
-- DROP INDEX IF EXISTS marketing.privacy_request_approval_request_id_idx;
-- DROP INDEX IF EXISTS ai.proposed_action_map_id_idx;
-- ALTER TABLE workforce.shift DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE workforce.leave_type DROP COLUMN IF EXISTS scope_path;
-- ALTER TABLE workforce.job_title DROP COLUMN IF EXISTS scope_path;
-- DROP TABLE IF EXISTS whitelabel.received_release;
-- ALTER TABLE wallet.refund_policy DROP COLUMN IF EXISTS version;
-- ALTER TABLE wallet.funding_rule DROP COLUMN IF EXISTS version;
-- DROP TABLE IF EXISTS venuemap.visit_planner_question;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS opening_hours;
-- ALTER TABLE platform.venue_settings DROP COLUMN IF EXISTS city;
-- ALTER TABLE platform.outlet DROP COLUMN IF EXISTS order_number_prefix;
-- ALTER TABLE payments.credit_account DROP COLUMN IF EXISTS currency_code;
-- DROP TABLE IF EXISTS marketing.seo_metadata;
-- ALTER TABLE marketing.form_definition_field DROP COLUMN IF EXISTS option_labels;
-- DROP TABLE IF EXISTS identity.subject_data_export_part;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS authorization_url;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS guest_provider;
-- ALTER TABLE identity.sso_provider DROP COLUMN IF EXISTS audience;
-- DROP TABLE IF EXISTS identity.guest_upload_ref;
-- ALTER TABLE assets.media_usage DROP CONSTRAINT IF EXISTS media_usage_surface_chk; ALTER TABLE assets.media_usage ADD CONSTRAINT media_usage_surface_chk CHECK (surface IN ('tenantBranding', 'homepageBanner', 'promoBlock', 'contentPage', 'product', 'event', 'menuItem', 'merchandise', 'workOrder', 'incident', 'inspection', 'campaign', 'aiConfigSource', 'aiHistoryImport', 'aiLayoutDraft', 'workOrderAttachment', 'seatingSection', 'transportNetworkImport', 'venueMap', 'venueMapVersion')) NOT VALID;
-- ALTER TABLE approvals.rule DROP COLUMN IF EXISTS matrix_version;
-- DROP TABLE IF EXISTS approvals.matrix_version;
-- DELETE FROM platform.schema_version WHERE version = 'V0118';
