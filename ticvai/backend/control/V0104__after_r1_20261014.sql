-- V0104 -- control database, after r1 (9cec72d) (20261014).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 1 index(es), 1 other statement(s).

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

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0104', 'after r1 (9cec72d): 0 table(s), 0 column(s), 1 index(es), 1 other statement(s)', '621eada14ddbf131e32381aa72278e7456508ffbf1114fdcb74c578689669d4e')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP INDEX IF EXISTS control.tenant_domain_tenant_id_hostname_uniq; CREATE UNIQUE INDEX IF NOT EXISTS tenant_domain_tenant_id_hostname_uniq ON control.tenant_domain (tenant_id, hostname);
-- DELETE FROM platform.schema_version WHERE version = 'V0104';
