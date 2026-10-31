-- V0120 -- tenant database, after r1 (9cec72d) (20261031).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 2 table(s), 7 column(s), 7 index(es), 20 other statement(s), 6 row-level security polic(ies) re-applied.

DO $$ BEGIN IF to_regclass('identity.guest_verification_policy') IS NOT NULL THEN
ALTER TABLE identity.guest_verification_policy ADD COLUMN IF NOT EXISTS currency_code text CONSTRAINT guest_verification_policy_currency_code_chk CHECK (char_length(currency_code) <= 3);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL THEN
ALTER TABLE marketing.conversation ADD COLUMN IF NOT EXISTS disposition_outcome text CONSTRAINT conversation_disposition_outcome_chk CHECK (disposition_outcome IN ('information', 'resolved', 'noSale', 'saleCompleted', 'callbackScheduled', 'escalated', 'wrongNumber', 'abandoned', 'unreachable'));
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL THEN
ALTER TABLE marketing.conversation ADD COLUMN IF NOT EXISTS callback_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL THEN
ALTER TABLE marketing.conversation ADD COLUMN IF NOT EXISTS callback_assigned_to_principal_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL THEN
ALTER TABLE marketing.conversation ADD COLUMN IF NOT EXISTS disposition_note text;
END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'form_definition_field' AND column_name = 'form_definition_id' AND is_nullable = 'NO') THEN ALTER TABLE marketing.form_definition_field ALTER COLUMN form_definition_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL THEN
ALTER TABLE marketing.waiver_signature ADD COLUMN IF NOT EXISTS form_version integer;
END IF; END $$;

DO $type$ BEGIN IF EXISTS (SELECT 1 FROM pg_attribute WHERE attrelid = to_regclass('pii.subject') AND attname = 'kind' AND NOT attisdropped AND atttypid = to_regtype('pii.subject_kind')) THEN
ALTER TABLE pii.subject ALTER COLUMN kind TYPE text;
END IF;
IF to_regclass('pii.subject') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject' AND column_name = 'kind') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_kind_chk' AND conrelid = to_regclass('pii.subject')) THEN
ALTER TABLE pii.subject ADD CONSTRAINT subject_kind_chk CHECK (kind IN ('guest', 'employee', 'contact', 'applicant'));
END IF;
IF to_regtype('pii.subject_kind') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_attribute WHERE atttypid = to_regtype('pii.subject_kind') AND NOT attisdropped) THEN
DROP DOMAIN pii.subject_kind;
END IF; END $type$;

DO $type$ BEGIN IF EXISTS (SELECT 1 FROM pg_attribute WHERE attrelid = to_regclass('pii.subject_contact') AND attname = 'kind' AND NOT attisdropped AND atttypid = to_regtype('pii.contact_kind')) THEN
ALTER TABLE pii.subject_contact ALTER COLUMN kind TYPE text;
END IF;
IF to_regclass('pii.subject_contact') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_contact' AND column_name = 'kind') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'subject_contact_kind_chk' AND conrelid = to_regclass('pii.subject_contact')) THEN
ALTER TABLE pii.subject_contact ADD CONSTRAINT subject_contact_kind_chk CHECK (kind IN ('email', 'mobile', 'phone', 'whatsapp', 'postal'));
END IF;
IF to_regtype('pii.contact_kind') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_attribute WHERE atttypid = to_regtype('pii.contact_kind') AND NOT attisdropped) THEN
DROP DOMAIN pii.contact_kind;
END IF; END $type$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'pii' AND table_name = 'subject_document' AND column_name = 'number_hash' AND is_nullable = 'NO') THEN ALTER TABLE pii.subject_document ALTER COLUMN number_hash DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF to_regclass('pii.subject_document') IS NOT NULL THEN
ALTER TABLE pii.subject_document ADD COLUMN IF NOT EXISTS number_ciphertext text;
END IF; END $$;

CREATE TABLE IF NOT EXISTS platform.blind_index_rehash (
    id                                uuid PRIMARY KEY NOT NULL,
    column_name                       text NOT NULL CONSTRAINT blind_index_rehash_column_name_chk CHECK (char_length(column_name) <= 190),
    from_version                      integer NOT NULL,
    to_version                        integer NOT NULL,
    last_id                           uuid,
    started_at                        timestamptz NOT NULL,
    finished_at                       timestamptz
);

CREATE TABLE IF NOT EXISTS platform.tenant_field_key (
    id                                uuid PRIMARY KEY NOT NULL,
    purpose                           text NOT NULL CONSTRAINT tenant_field_key_purpose_chk CHECK (purpose IN ('dataKey', 'blindIndexKey')),
    key_version                       integer NOT NULL,
    wrapped_key                       bytea NOT NULL,
    wrapping_key_id                   text NOT NULL CONSTRAINT tenant_field_key_wrapping_key_id_chk CHECK (char_length(wrapping_key_id) <= 500),
    state                             text NOT NULL CONSTRAINT tenant_field_key_state_chk CHECK (state IN ('active', 'decryptOnly', 'retired')),
    created_at                        timestamptz NOT NULL,
    rotated_at                        timestamptz
);

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL AND to_regclass('identity.principal') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'conversation' AND column_name = 'callback_assigned_to_principal_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'conversation_callback_assigned_to_principal_id_fkey' AND conrelid = to_regclass('marketing.conversation')) THEN
ALTER TABLE marketing.conversation ADD CONSTRAINT conversation_callback_assigned_to_principal_id_fkey FOREIGN KEY (callback_assigned_to_principal_id) REFERENCES identity.principal(id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.form_definition_field') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'form_definition_field' AND column_name = 'form_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'form_definition_field' AND column_name = 'form_version') THEN
CREATE INDEX IF NOT EXISTS form_definition_field_form_id_form_version_idx ON marketing.form_definition_field (form_id, form_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_requirement') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_requirement' AND column_name = 'form_definition_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_requirement' AND column_name = 'form_version') THEN
CREATE INDEX IF NOT EXISTS waiver_requirement_form_definition_id_form_version_idx ON marketing.waiver_requirement (form_definition_id, form_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.waiver_signature') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'form_definition_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'waiver_signature' AND column_name = 'form_version') THEN
CREATE INDEX IF NOT EXISTS waiver_signature_form_definition_id_form_version_idx ON marketing.waiver_signature (form_definition_id, form_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('marketing.conversation') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'conversation' AND column_name = 'callback_assigned_to_principal_id') THEN
CREATE INDEX IF NOT EXISTS conversation_callback_assigned_to_principal_id_idx ON marketing.conversation (callback_assigned_to_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.blind_index_rehash') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'blind_index_rehash' AND column_name = 'column_name') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'blind_index_rehash' AND column_name = 'to_version') THEN
CREATE UNIQUE INDEX IF NOT EXISTS blind_index_rehash_column_name_to_version_uniq ON platform.blind_index_rehash (column_name, to_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.tenant_field_key') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'tenant_field_key' AND column_name = 'key_version') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'tenant_field_key' AND column_name = 'purpose') THEN
CREATE UNIQUE INDEX IF NOT EXISTS tenant_field_key_purpose_key_version_uniq ON platform.tenant_field_key (purpose, key_version);
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.tenant_field_key') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'tenant_field_key' AND column_name = 'purpose') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'tenant_field_key' AND column_name = 'state') THEN
CREATE UNIQUE INDEX IF NOT EXISTS tenant_field_key_purpose_uniq ON platform.tenant_field_key (purpose) WHERE state = 'active';
END IF; END $$;

CREATE OR REPLACE FUNCTION platform.subject_holds_household_grant_over(target_subject_id uuid)
    RETURNS boolean
    LANGUAGE plpgsql
    STABLE
AS $$
DECLARE
    me uuid := NULLIF(current_setting('ticvai.subject_id', true), '')::uuid;
BEGIN
    IF me IS NULL OR target_subject_id IS NULL THEN
        RETURN false;
    END IF;
    RETURN EXISTS (
        SELECT 1 FROM identity.delegated_access held
         WHERE held.subject_id = me
           AND held.over_subject_id = target_subject_id
           AND held.delegation_kind IN ('familyMember', 'primaryHolder')
           AND held.effect = 'ALLOW'
           AND held.revoked_at IS NULL
           AND (held.valid_from IS NULL OR held.valid_from <= now())
           AND (held.valid_to IS NULL OR now() < held.valid_to));
END
$$;

DO $$ BEGIN IF to_regclass('identity.delegated_access') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'granted_by_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'over_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'identity' AND table_name = 'delegated_access' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('identity.delegated_access'::regclass);
PERFORM platform.apply_split_rls('identity.delegated_access'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.subject_holds_household_grant_over(over_subject_id))');
END IF; END $$;

DO $$ BEGIN IF to_regclass('ledger.tax_invoice') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'tax_invoice' AND column_name = 'buyer_subject_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'tax_invoice' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('ledger.tax_invoice'::regclass);
PERFORM platform.apply_split_rls('ledger.tax_invoice'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (buyer_subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('payments.dunning_case') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'dunning_case' AND column_name = 'scope_path') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'payments' AND table_name = 'dunning_case' AND column_name = 'subject_id') THEN
PERFORM platform.drop_rls_policies('payments.dunning_case'::regclass);
PERFORM platform.apply_split_rls('payments.dunning_case'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])) OR (subject_id = (SELECT NULLIF(current_setting(''ticvai.subject_id'', true), '''')::uuid))', 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])');
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.blind_index_rehash') IS NOT NULL THEN
PERFORM platform.apply_split_rls('platform.blind_index_rehash'::regclass, 'cardinality(platform.current_scope_paths()) > 0', 'cardinality(platform.current_scope_paths()) > 0');
DROP POLICY IF EXISTS blind_index_rehash_delete ON platform.blind_index_rehash;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.region_settings') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'region_settings' AND column_name = 'scope_path') THEN
PERFORM platform.drop_rls_policies('platform.region_settings'::regclass);
PERFORM platform.apply_split_rls('platform.region_settings'::regclass, 'platform.in_scope(scope_path) OR platform.above_scope(scope_path) OR NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NOT NULL', 'platform.in_scope(scope_path)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.tenant_field_key') IS NOT NULL THEN
PERFORM platform.apply_split_rls('platform.tenant_field_key'::regclass, 'cardinality(platform.current_scope_paths()) > 0', 'cardinality(platform.current_scope_paths()) > 0');
DROP POLICY IF EXISTS tenant_field_key_delete ON platform.tenant_field_key;
END IF; END $$;

DO $$ BEGIN IF to_regclass('platform.venue_settings') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'venue_settings' AND column_name = 'venue_id') THEN
PERFORM platform.drop_rls_policies('platform.venue_settings'::regclass);
PERFORM platform.apply_split_rls('platform.venue_settings'::regclass, 'platform.venue_in_scope(venue_id) OR NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NOT NULL', 'platform.venue_in_scope(venue_id)');
END IF; END $$;

DO $$ BEGIN IF to_regclass('ledger.tax_invoice_line') IS NOT NULL AND to_regclass('ledger.tax_invoice') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'tax_invoice' AND column_name = 'id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'tax_invoice_line' AND column_name = 'tax_invoice_id') THEN
PERFORM platform.drop_rls_policies('ledger.tax_invoice_line'::regclass);
PERFORM platform.apply_parent_split_rls('ledger.tax_invoice_line'::regclass, 'tax_invoice_id', 'ledger.tax_invoice'::regclass, 'id', '(parent_row.scope_path IS NOT NULL AND parent_row.scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[]))');
END IF; END $$;

DO $recorded$ BEGIN IF to_regprocedure('platform.outbox_advance_sequence()') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.outbox_advance_sequence()') AND md5(replace(prosrc, chr(13), '')) = '1a82de76334b11f67d636c8d2e830570') THEN
CREATE OR REPLACE FUNCTION platform.outbox_advance_sequence() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO platform.outbox_sequence AS kept (aggregate_id, last_sequence)
    VALUES (NEW.aggregate_id, NEW.sequence)
    ON CONFLICT (aggregate_id) DO UPDATE SET last_sequence = EXCLUDED.last_sequence
     WHERE kept.last_sequence < EXCLUDED.last_sequence;
    RETURN NULL;
END;
$$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regclass('platform.outbox') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'outbox' AND column_name = 'aggregate_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'outbox' AND column_name = 'sequence') AND to_regclass('platform.outbox_sequence') IS NOT NULL AND to_regprocedure('platform.outbox_advance_sequence()') IS NOT NULL THEN
CREATE OR REPLACE TRIGGER outbox_advance_sequence AFTER INSERT ON platform.outbox FOR EACH ROW WHEN ((new.sequence > 0)) EXECUTE FUNCTION platform.outbox_advance_sequence();
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regclass('platform.outbox_sequence') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'outbox_sequence' AND column_name = 'last_sequence') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'outbox_sequence_last_sequence_chk' AND conrelid = to_regclass('platform.outbox_sequence')) THEN
ALTER TABLE platform.outbox_sequence ADD CONSTRAINT outbox_sequence_last_sequence_chk CHECK ((last_sequence > 0)) NOT VALID;
ALTER TABLE platform.outbox_sequence VALIDATE CONSTRAINT outbox_sequence_last_sequence_chk;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('ledger.journal_entry_legal_entity_sync()') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('ledger.journal_entry_legal_entity_sync()') AND md5(replace(prosrc, chr(13), '')) = 'cb1461d1282a3a83524bf49785d6ac87') THEN
CREATE OR REPLACE FUNCTION ledger.journal_entry_legal_entity_sync() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    SELECT fp.legal_entity_id INTO NEW.legal_entity_id FROM ledger.fiscal_period fp WHERE fp.id = NEW.fiscal_period_id;
    RETURN NEW;
END
$$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regclass('ledger.journal_entry') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'journal_entry' AND column_name = 'fiscal_period_id') AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'journal_entry' AND column_name = 'legal_entity_id') AND to_regclass('ledger.fiscal_period') IS NOT NULL AND to_regprocedure('ledger.journal_entry_legal_entity_sync()') IS NOT NULL THEN
CREATE OR REPLACE TRIGGER journal_entry_legal_entity_sync BEFORE INSERT OR UPDATE OF fiscal_period_id, legal_entity_id ON ledger.journal_entry FOR EACH ROW EXECUTE FUNCTION ledger.journal_entry_legal_entity_sync();
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regclass('ledger.journal_entry') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'ledger' AND table_name = 'journal_entry' AND column_name = 'legal_entity_id') AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'journal_entry_legal_entity_id_chk' AND conrelid = to_regclass('ledger.journal_entry')) THEN
ALTER TABLE ledger.journal_entry ADD CONSTRAINT journal_entry_legal_entity_id_chk CHECK ((legal_entity_id IS NOT NULL)) NOT VALID;
ALTER TABLE ledger.journal_entry VALIDATE CONSTRAINT journal_entry_legal_entity_id_chk;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('platform.grant_schema_to_role(text, text, boolean)') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.grant_schema_to_role(text, text, boolean)') AND md5(replace(prosrc, chr(13), '')) = '568c3a0fac8c7d7513e98e9e3478f361') THEN
CREATE OR REPLACE FUNCTION platform.grant_schema_to_role(target_schema text, target_role text, can_write boolean) RETURNS void
    LANGUAGE plpgsql
    AS $_$
DECLARE
    rel record;
BEGIN
    IF to_regnamespace(target_schema) IS NULL THEN
        RETURN;
    END IF;
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO %I', target_schema, target_role);
    FOR rel IN
        SELECT c.oid::regclass AS name, c.relkind
          FROM pg_class c
         WHERE c.relnamespace = to_regnamespace(target_schema)
           AND c.relkind IN ('r', 'p', 'v', 'm', 'S')
           AND NOT c.relispartition
           AND c.relname !~ '_p[0-9]{6}$'
    LOOP
        IF rel.relkind = 'S' THEN
            EXECUTE format('GRANT %s ON SEQUENCE %s TO %I',
                           CASE WHEN can_write THEN 'USAGE, SELECT' ELSE 'SELECT' END, rel.name, target_role);
        ELSIF rel.relkind IN ('v', 'm') OR NOT can_write THEN
            EXECUTE format('GRANT SELECT ON %s TO %I', rel.name, target_role);
        ELSE
            EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON %s TO %I', rel.name, target_role);
        END IF;
    END LOOP;
END
$_$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('platform.apply_deployable_grants()') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.apply_deployable_grants()') AND md5(replace(prosrc, chr(13), '')) = '7a015ffa2c105250062d74e1fa0cbf5f') THEN
CREATE OR REPLACE FUNCTION platform.apply_deployable_grants() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    owners constant jsonb := jsonb_build_object(
        'commerce',   jsonb_build_array('identity', 'pii', 'platform', 'workforce', 'approvals', 'accreditation',
                                        'tenancy', 'kernel', 'catalogue', 'pricing', 'promotions', 'seating',
                                        'orders', 'payments', 'ledger', 'wallet'),
        'access',     jsonb_build_array('access'),
        'operations', jsonb_build_array('inventory', 'fnb', 'retail', 'marketing', 'queue', 'maintenance',
                                        'resources', 'venuemap', 'assets', 'games', 'rental', 'transport',
                                        'subscription', 'whitelabel', 'reporting', 'sync'),
        'ticvai_ai',  jsonb_build_array('ai'));
    hosts constant text[] := ARRAY['commerce', 'access', 'operations', 'workers', 'ticvai_ai'];
    module_schemas text[];
    mapped_schemas text[];
    mapped_oids oid[];
    host text;
    owned_schema text;
    rel record;
BEGIN
    SELECT array_agg(s) INTO module_schemas
      FROM (SELECT jsonb_array_elements_text(owners -> o) AS s FROM unnest(ARRAY['commerce', 'access', 'operations']) o) x;
    mapped_schemas := module_schemas || ARRAY['ai'];
    SELECT array_agg(oid) INTO mapped_oids FROM pg_namespace WHERE nspname = ANY (mapped_schemas);

    -- Ownership, when the caller can give it away.
    IF (SELECT rolsuper FROM pg_roles WHERE rolname = current_user) THEN
        EXECUTE format('GRANT CONNECT ON DATABASE %I TO ticvai_migrator, commerce, access, operations, workers, ticvai_ai',
                       current_database());
        FOR rel IN SELECT nspname FROM pg_namespace WHERE oid = ANY (mapped_oids) AND nspowner <> 'ticvai_migrator'::regrole LOOP
            EXECUTE format('ALTER SCHEMA %I OWNER TO ticvai_migrator', rel.nspname);
        END LOOP;
        FOR rel IN
            SELECT c.oid::regclass AS name, c.relkind
              FROM pg_class c
             WHERE c.relnamespace = ANY (mapped_oids)
               AND c.relkind IN ('r', 'p', 'v', 'm', 'S')
               AND c.relowner <> 'ticvai_migrator'::regrole
               -- a sequence that belongs to a column moves with its table
               AND NOT (c.relkind = 'S' AND EXISTS (SELECT 1 FROM pg_depend d
                                                     WHERE d.objid = c.oid AND d.deptype IN ('a', 'i')))
        LOOP
            EXECUTE format('ALTER %s %s OWNER TO ticvai_migrator',
                           CASE rel.relkind WHEN 'S' THEN 'SEQUENCE' WHEN 'v' THEN 'VIEW'
                                            WHEN 'm' THEN 'MATERIALIZED VIEW' ELSE 'TABLE' END,
                           rel.name);
        END LOOP;
        FOR rel IN SELECT p.oid::regprocedure AS name FROM pg_proc p
                    WHERE p.pronamespace = ANY (mapped_oids) AND p.proowner <> 'ticvai_migrator'::regrole LOOP
            EXECUTE format('ALTER FUNCTION %s OWNER TO ticvai_migrator', rel.name);
        END LOOP;
        FOR rel IN SELECT t.oid::regtype AS name FROM pg_type t
                    WHERE t.typnamespace = ANY (mapped_oids) AND t.typtype IN ('e', 'd')
                      AND t.typowner <> 'ticvai_migrator'::regrole LOOP
            EXECUTE format('ALTER TYPE %s OWNER TO ticvai_migrator', rel.name);
        END LOOP;
    END IF;

    -- Each deployable writes the schemas its modules own.
    FOR host IN SELECT jsonb_object_keys(owners) LOOP
        FOR owned_schema IN SELECT jsonb_array_elements_text(owners -> host) LOOP
            PERFORM platform.grant_schema_to_role(owned_schema, host, true);
        END LOOP;
    END LOOP;

    -- workers runs every module's consumers, the relay and the jobs.
    FOREACH owned_schema IN ARRAY module_schemas LOOP
        PERFORM platform.grant_schema_to_role(owned_schema, 'workers', true);
    END LOOP;

    -- The AI reads the transactional schemas, never pii.
    FOREACH owned_schema IN ARRAY module_schemas LOOP
        IF owned_schema <> 'pii' THEN
            PERFORM platform.grant_schema_to_role(owned_schema, 'ticvai_ai', false);
        END IF;
    END LOOP;

    -- The kernel every host needs, whoever owns it.
    FOREACH host IN ARRAY hosts LOOP
        EXECUTE format('GRANT USAGE ON SCHEMA platform TO %I', host);
        IF to_regclass('platform.outbox') IS NOT NULL THEN
            EXECUTE format('GRANT INSERT ON platform.outbox TO %I', host);
            FOR rel IN SELECT d.objid::regclass AS name FROM pg_depend d JOIN pg_class s ON s.oid = d.objid AND s.relkind = 'S'
                        WHERE d.refobjid = 'platform.outbox'::regclass AND d.deptype IN ('a', 'i') LOOP
                EXECUTE format('GRANT USAGE ON SEQUENCE %s TO %I', rel.name, host);
            END LOOP;
        END IF;
        IF to_regclass('platform.scope') IS NOT NULL THEN
            EXECUTE format('GRANT SELECT ON platform.scope TO %I', host);
        END IF;
        IF to_regclass('platform.audit_record') IS NOT NULL THEN
            EXECUTE format('GRANT INSERT ON platform.audit_record TO %I', host);
        END IF;
        IF to_regclass('platform.idempotency_record') IS NOT NULL THEN
            EXECUTE format('GRANT SELECT, INSERT, UPDATE ON platform.idempotency_record TO %I', host);
        END IF;
        -- CR-166: every host allocates its events' sequences from the counter (240).
        IF to_regclass('platform.outbox_sequence') IS NOT NULL THEN
            EXECUTE format('GRANT SELECT, INSERT, UPDATE ON platform.outbox_sequence TO %I', host);
        END IF;
        -- CR-339: every host's kernel reads and creates the tenant's field keys and reads re-hash progress.
        IF to_regclass('platform.tenant_field_key') IS NOT NULL THEN
            EXECUTE format('GRANT SELECT, INSERT, UPDATE ON platform.tenant_field_key TO %I', host);
        END IF;
        IF to_regclass('platform.blind_index_rehash') IS NOT NULL THEN
            EXECUTE format('GRANT SELECT, INSERT, UPDATE ON platform.blind_index_rehash TO %I', host);
        END IF;
    END LOOP;

    -- The register is the migrator's alone.
    REVOKE ALL ON platform.schema_version FROM commerce, access, operations, workers, ticvai_ai;

    -- A partition is reached through its parent, whose policies then apply.
    FOR rel IN SELECT c.oid::regclass AS name FROM pg_class c
                WHERE c.relnamespace = ANY (mapped_oids) AND c.relispartition AND c.relkind IN ('r', 'p') LOOP
        EXECUTE format('REVOKE ALL ON %s FROM commerce, access, operations, workers, ticvai_ai', rel.name);
    END LOOP;

    -- The functions that change the schema are the migrator's; the predicates stay callable by all.
    -- Only those that exist yet: on a new database 050 (the detach function) arrives after 004.
    FOR rel IN
        SELECT to_regprocedure(f) AS name
          FROM unnest(ARRAY['platform.apply_deployable_grants()', 'platform.grant_schema_to_role(text, text, boolean)',
                            'platform.apply_scope_rls(regclass)', 'platform.apply_shared_scope_rls(regclass, text)',
                            'platform.apply_venue_rls(regclass)', 'platform.apply_parent_rls(regclass, text, regclass, text)',
                            'platform.apply_tenant_rls(regclass)', 'platform.apply_subject_rls(regclass)',
                            'platform.ensure_month_partition(regclass, date)', 'platform.ensure_month_partitions(regclass, integer)',
                            'platform.detach_month_partitions_before(regclass, date)']) f
         WHERE to_regprocedure(f) IS NOT NULL
    LOOP
        EXECUTE format('REVOKE EXECUTE ON FUNCTION %s FROM PUBLIC', rel.name);
    END LOOP;
END
$$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('platform.apply_statement_scope_rls(regclass)') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.apply_statement_scope_rls(regclass)') AND md5(replace(prosrc, chr(13), '')) = 'ad585f53b0be9eef8636a5649386b1dc') THEN
CREATE OR REPLACE FUNCTION platform.apply_statement_scope_rls(target regclass) RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := 'scope_path IS NOT NULL AND scope_path <@ ANY ((SELECT platform.current_scope_paths())::ltree[])';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    PERFORM platform.drop_rls_policies(target);
    EXECUTE format('CREATE POLICY %I ON %s USING (%s) WITH CHECK (%s)',
                   policy_name, target, predicate, predicate);
END
$$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('platform.detach_month_partitions_before(regclass, date)') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.detach_month_partitions_before(regclass, date)') AND md5(replace(prosrc, chr(13), '')) = '715840e5f313d4424b151793da92c028') THEN
CREATE OR REPLACE FUNCTION platform.detach_month_partitions_before(target regclass, cutoff date) RETURNS SETOF text
    LANGUAGE plpgsql
    AS $_$
DECLARE
    part record;
BEGIN
    FOR part IN
        SELECT c.oid::regclass AS name, c.relname
          FROM pg_inherits i
          JOIN pg_class c ON c.oid = i.inhrelid
         WHERE i.inhparent = target
           AND c.relname ~ '_p[0-9]{6}$'
         ORDER BY c.relname
    LOOP
        IF to_date(right(part.relname, 6), 'YYYYMM') + interval '1 month' <= cutoff THEN
            EXECUTE format('ALTER TABLE %s DETACH PARTITION %s', target, part.name);
            EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', part.name);
            EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', part.name);
            EXECUTE format('COMMENT ON TABLE %s IS %L', part.name,
                           format('Detached from %s on %s, past its retention (ADR-0047); awaiting archive.',
                                  target, current_date));
            RETURN NEXT part.name::text;
        END IF;
    END LOOP;
END
$_$;
END IF; END $recorded$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0120', 'after r1 (9cec72d): 2 table(s), 7 column(s), 7 index(es), 20 other statement(s), 6 row-level security polic(ies) re-applied', '8ec99a902d1c8e4b7ad1fc2206882028bbf8f400f4b7d8a4b06699aecdec2646')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP FUNCTION IF EXISTS platform.detach_month_partitions_before(regclass, date);
-- DROP FUNCTION IF EXISTS platform.apply_statement_scope_rls(regclass);
-- DROP FUNCTION IF EXISTS platform.apply_deployable_grants();
-- DROP FUNCTION IF EXISTS platform.grant_schema_to_role(text, text, boolean);
-- ALTER TABLE ledger.journal_entry DROP CONSTRAINT IF EXISTS journal_entry_legal_entity_id_chk;
-- DROP TRIGGER IF EXISTS journal_entry_legal_entity_sync ON ledger.journal_entry;
-- DROP FUNCTION IF EXISTS ledger.journal_entry_legal_entity_sync();
-- ALTER TABLE platform.outbox_sequence DROP CONSTRAINT IF EXISTS outbox_sequence_last_sequence_chk;
-- DROP TRIGGER IF EXISTS outbox_advance_sequence ON platform.outbox;
-- DROP FUNCTION IF EXISTS platform.outbox_advance_sequence();
-- SELECT platform.drop_rls_policies('ledger.tax_invoice_line'::regclass); SELECT platform.apply_parent_rls('ledger.tax_invoice_line'::regclass, 'tax_invoice_id', 'ledger.tax_invoice'::regclass, 'id');
-- SELECT platform.drop_rls_policies('platform.venue_settings'::regclass); SELECT platform.apply_venue_rls('platform.venue_settings'::regclass);
-- SELECT platform.drop_rls_policies('platform.region_settings'::regclass); SELECT platform.apply_tenant_rls('platform.region_settings'::regclass); SELECT platform.apply_read_beneath_rls('platform.region_settings'::regclass);
-- SELECT platform.drop_rls_policies('payments.dunning_case'::regclass); SELECT platform.apply_scope_rls('payments.dunning_case'::regclass);
-- SELECT platform.drop_rls_policies('ledger.tax_invoice'::regclass); SELECT platform.apply_scope_rls('ledger.tax_invoice'::regclass);
-- SELECT platform.drop_rls_policies('identity.delegated_access'::regclass); SELECT platform.apply_scope_rls('identity.delegated_access'::regclass); SELECT platform.apply_split_rls('identity.delegated_access'::regclass, 'platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '(platform.in_scope(scope_path) OR platform.own_row(NULL::uuid, over_subject_id))'); SELECT platform.apply_split_rls('identity.delegated_access'::regclass, '(NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, subject_id) OR platform.own_row(NULL::uuid, over_subject_id) OR platform.own_row(NULL::uuid, granted_by_subject_id)', '((NULLIF(current_setting(''ticvai.subject_id'', true), '''') IS NULL AND platform.in_scope(scope_path)) OR platform.own_row(NULL::uuid, over_subject_id))');
-- DROP INDEX IF EXISTS platform.tenant_field_key_purpose_uniq;
-- DROP INDEX IF EXISTS platform.tenant_field_key_purpose_key_version_uniq;
-- DROP INDEX IF EXISTS platform.blind_index_rehash_column_name_to_version_uniq;
-- DROP INDEX IF EXISTS marketing.conversation_callback_assigned_to_principal_id_idx;
-- DROP INDEX IF EXISTS marketing.waiver_signature_form_definition_id_form_version_idx;
-- DROP INDEX IF EXISTS marketing.waiver_requirement_form_definition_id_form_version_idx;
-- DROP INDEX IF EXISTS marketing.form_definition_field_form_id_form_version_idx;
-- ALTER TABLE marketing.conversation DROP CONSTRAINT IF EXISTS conversation_callback_assigned_to_principal_id_fkey;
-- DROP TABLE IF EXISTS platform.tenant_field_key;
-- DROP TABLE IF EXISTS platform.blind_index_rehash;
-- ALTER TABLE pii.subject_document DROP COLUMN IF EXISTS number_ciphertext;
-- ALTER TABLE pii.subject_document ALTER COLUMN number_hash SET NOT NULL;
-- ALTER TABLE pii.subject_contact DROP CONSTRAINT IF EXISTS subject_contact_kind_chk;
-- ALTER TABLE pii.subject DROP CONSTRAINT IF EXISTS subject_kind_chk;
-- ALTER TABLE marketing.waiver_signature DROP COLUMN IF EXISTS form_version;
-- ALTER TABLE marketing.form_definition_field ALTER COLUMN form_definition_id SET NOT NULL;
-- ALTER TABLE marketing.conversation DROP COLUMN IF EXISTS disposition_note;
-- ALTER TABLE marketing.conversation DROP COLUMN IF EXISTS callback_assigned_to_principal_id;
-- ALTER TABLE marketing.conversation DROP COLUMN IF EXISTS callback_at;
-- ALTER TABLE marketing.conversation DROP COLUMN IF EXISTS disposition_outcome;
-- ALTER TABLE identity.guest_verification_policy DROP COLUMN IF EXISTS currency_code;
-- DELETE FROM platform.schema_version WHERE version = 'V0120';
