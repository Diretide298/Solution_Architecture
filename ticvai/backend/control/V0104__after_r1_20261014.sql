-- V0104 -- control database, after r1 (9cec72d) (20261014).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 3 column(s), 2 index(es), 1 other statement(s), 3 row-level security polic(ies) re-applied.

ALTER TABLE control.api_client ADD COLUMN IF NOT EXISTS status_reason text CONSTRAINT api_client_status_reason_chk CHECK (char_length(status_reason) <= 500);

ALTER TABLE control.api_version ADD COLUMN IF NOT EXISTS changes jsonb;

ALTER TABLE control.tenant_migration_plan ADD COLUMN IF NOT EXISTS blockers jsonb;

CREATE UNIQUE INDEX IF NOT EXISTS tenant_code_uniq ON control.tenant (lower(code));

DROP INDEX IF EXISTS control.tenant_domain_tenant_id_hostname_uniq;

CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_tenant_id_hostname_uniq ON control.tenant_domain (tenant_id, lower(hostname));

CREATE OR REPLACE FUNCTION platform.drop_rls_policies(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    pol record;
BEGIN
    FOR pol IN SELECT polname FROM pg_policy WHERE polrelid = target LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON %s', pol.polname, target);
    END LOOP;
END
$$;

SELECT platform.drop_rls_policies('control.migration_run'::regclass);

SELECT platform.apply_parent_rls('control.migration_run'::regclass, 'plan_id', 'control.migration_plan'::regclass, 'id');

SELECT platform.drop_rls_policies('control.migration_run_cell'::regclass);

SELECT platform.apply_parent_rls('control.migration_run_cell'::regclass, 'migration_run_id', 'control.migration_run'::regclass, 'id');

SELECT platform.drop_rls_policies('control.migration_run_tenant'::regclass);

SELECT platform.apply_parent_rls('control.migration_run_tenant'::regclass, 'migration_run_id', 'control.migration_run'::regclass, 'id');

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0104', 'after r1 (9cec72d): 0 table(s), 3 column(s), 2 index(es), 1 other statement(s), 3 row-level security polic(ies) re-applied', 'c7433ca4186f0166926c98a76266dd60275947590b2a98d046709c6dc4abc314')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('control.migration_run_tenant'::regclass); 
-- SELECT platform.drop_rls_policies('control.migration_run_cell'::regclass); 
-- SELECT platform.drop_rls_policies('control.migration_run'::regclass); 
-- DROP INDEX IF EXISTS control.tenant_domain_tenant_id_hostname_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_tenant_id_hostname_uniq ON control.tenant_domain (tenant_id, hostname);
-- DROP INDEX IF EXISTS control.tenant_code_uniq;
-- ALTER TABLE control.tenant_migration_plan DROP COLUMN IF EXISTS blockers;
-- ALTER TABLE control.api_version DROP COLUMN IF EXISTS changes;
-- ALTER TABLE control.api_client DROP COLUMN IF EXISTS status_reason;
-- DELETE FROM platform.schema_version WHERE version = 'V0104';
