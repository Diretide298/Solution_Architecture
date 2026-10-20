-- V0109 -- tenant database, after r1 (9cec72d) (20261020): the names the contracts use.
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), but the schema reference has renamed columns,
-- added foreign keys and stopped generating some indexes since. Migrations written from the baseline DDL
-- create the old names; this file brings a database built from them to the names the contracts use.
-- Every statement is a guarded block: it does nothing when its table, key or index is not there yet, or is
-- there already under the new name, so the file can be applied twice and in any database. A table created
-- by a migration that runs after this one copies the blocks that name it (ticket text: 'Changes this file
-- makes to your tables'). A foreign key is added NOT VALID: it checks every new write, and the owner runs
-- ALTER TABLE ... VALIDATE CONSTRAINT when the rows already there are known to be clean.
-- 0 column rename(s), 4 key(s) added, renamed or dropped, 4 index(es) renamed or dropped.

-- ai.proposed_action | foreign key | proposed_action_translation_job_id_fkey | ai.translation_job
DO $$ BEGIN IF to_regclass('ai.proposed_action') IS NOT NULL AND to_regclass('ai.translation_job') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'proposed_action_translation_job_id_fkey' AND conrelid = to_regclass('ai.proposed_action')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('ai.proposed_action') AND attname = 'translation_job_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('ai.translation_job') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('ai.translation_job') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE ai.proposed_action ADD CONSTRAINT proposed_action_translation_job_id_fkey FOREIGN KEY (translation_job_id) REFERENCES ai.translation_job(id) NOT VALID; END IF; END $$;

-- platform.workstation | foreign key | workstation_configuration_profile_id_fkey | platform.configuration_profile
DO $$ BEGIN IF to_regclass('platform.workstation') IS NOT NULL AND to_regclass('platform.configuration_profile') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'workstation_configuration_profile_id_fkey' AND conrelid = to_regclass('platform.workstation')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.workstation') AND attname = 'configuration_profile_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.configuration_profile') AND attname = 'id') AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.workstation') AND attname = 'configuration_profile_version') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.configuration_profile') AND attname = 'version') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('platform.configuration_profile') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id', 'version']) THEN ALTER TABLE platform.workstation ADD CONSTRAINT workstation_configuration_profile_id_fkey FOREIGN KEY (configuration_profile_id, configuration_profile_version) REFERENCES platform.configuration_profile(id, version) NOT VALID; END IF; END $$;

-- tenancy.device_assignment | foreign key | device_assignment_device_id_fkey | platform.device
DO $$ BEGIN IF to_regclass('tenancy.device_assignment') IS NOT NULL AND to_regclass('platform.device') IS NOT NULL AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'device_assignment_device_id_fkey' AND conrelid = to_regclass('tenancy.device_assignment')) AND (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('tenancy.device_assignment') AND attname = 'device_id') = (SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('platform.device') AND attname = 'id') AND EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('platform.device') AND i.indisunique AND i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = ARRAY['id']) THEN ALTER TABLE tenancy.device_assignment ADD CONSTRAINT device_assignment_device_id_fkey FOREIGN KEY (device_id) REFERENCES platform.device(id) NOT VALID; END IF; END $$;

-- identity.platform_staff_grant | drop index | platform_staff_grant_operator_principal_id_idx
DO $$ BEGIN IF to_regclass('identity.platform_staff_grant_operator_principal_id_idx') IS NOT NULL THEN DROP INDEX identity.platform_staff_grant_operator_principal_id_idx; END IF; END $$;

-- platform.profile_deployment | drop index | profile_deployment_profile_id_idx
DO $$ BEGIN IF to_regclass('platform.profile_deployment_profile_id_idx') IS NOT NULL THEN DROP INDEX platform.profile_deployment_profile_id_idx; END IF; END $$;

-- platform.workstation | drop index | workstation_configuration_profile_id_idx
DO $$ BEGIN IF to_regclass('platform.workstation_configuration_profile_id_idx') IS NOT NULL THEN DROP INDEX platform.workstation_configuration_profile_id_idx; END IF; END $$;

-- subscription.membership_renewal_policy | drop index | membership_renewal_policy_cancellation_policy_id_idx
DO $$ BEGIN IF to_regclass('subscription.membership_renewal_policy_cancellation_policy_id_idx') IS NOT NULL THEN DROP INDEX subscription.membership_renewal_policy_cancellation_policy_id_idx; END IF; END $$;

-- identity.platform_staff_grant | drop foreign key | platform_staff_grant_operator_principal_id_fkey | identity.principal
DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'platform_staff_grant_operator_principal_id_fkey' AND conrelid = to_regclass('identity.platform_staff_grant')) THEN ALTER TABLE identity.platform_staff_grant DROP CONSTRAINT platform_staff_grant_operator_principal_id_fkey; END IF; END $$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0109', 'after r1 (9cec72d), names the contracts use: 0 column rename(s), 4 key(s) added, renamed or dropped, 4 index(es) renamed or dropped', '55380e10e49086b7d2129b13819cd6f77a369cbb4d54d57f4647b47335ccae52')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- ALTER TABLE identity.platform_staff_grant ADD CONSTRAINT platform_staff_grant_operator_principal_id_fkey FOREIGN KEY (operator_principal_id) REFERENCES identity.principal(id) NOT VALID;
-- CREATE INDEX IF NOT EXISTS membership_renewal_policy_cancellation_policy_id_idx ON subscription.membership_renewal_policy (cancellation_policy_id);
-- CREATE INDEX IF NOT EXISTS workstation_configuration_profile_id_idx ON platform.workstation (configuration_profile_id);
-- CREATE INDEX IF NOT EXISTS profile_deployment_profile_id_idx ON platform.profile_deployment (profile_id);
-- CREATE INDEX IF NOT EXISTS platform_staff_grant_operator_principal_id_idx ON identity.platform_staff_grant (operator_principal_id);
-- ALTER TABLE tenancy.device_assignment DROP CONSTRAINT IF EXISTS device_assignment_device_id_fkey;
-- ALTER TABLE platform.workstation DROP CONSTRAINT IF EXISTS workstation_configuration_profile_id_fkey;
-- ALTER TABLE ai.proposed_action DROP CONSTRAINT IF EXISTS proposed_action_translation_job_id_fkey;
-- DELETE FROM platform.schema_version WHERE version = 'V0109';
