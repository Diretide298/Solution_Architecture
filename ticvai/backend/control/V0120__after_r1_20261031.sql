-- V0120 -- control database, after r1 (9cec72d) (20261031).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/control/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- Every statement that needs a table is a guarded block (CHG-R9MIG-002): it does nothing where its table
-- or a column it names is not there yet, so the file applies as one transaction, twice, on any database;
-- the migration that creates such a table later copies the block. A table's policy change is one block.
-- 0 table(s), 4 column(s), 2 index(es), 2 other statement(s).

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL THEN
ALTER TABLE control.release ADD COLUMN IF NOT EXISTS status_reason text;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL THEN
ALTER TABLE control.release ADD COLUMN IF NOT EXISTS status_changed_by_principal_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL THEN
ALTER TABLE control.release ADD COLUMN IF NOT EXISTS status_changed_at timestamptz;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL THEN
ALTER TABLE control.release ADD COLUMN IF NOT EXISTS withdrawal_approved_by_principal_id uuid;
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'release' AND column_name = 'status_changed_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS release_status_changed_by_principal_id_idx ON control.release (status_changed_by_principal_id);
END IF; END $$;

DO $$ BEGIN IF to_regclass('control.release') IS NOT NULL AND EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'control' AND table_name = 'release' AND column_name = 'withdrawal_approved_by_principal_id') THEN
CREATE INDEX IF NOT EXISTS release_withdrawal_approved_by_principal_id_idx ON control.release (withdrawal_approved_by_principal_id);
END IF; END $$;

DO $recorded$ BEGIN IF to_regprocedure('platform.grant_schema_to_role(text, text, boolean)') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.grant_schema_to_role(text, text, boolean)') AND md5(replace(prosrc, chr(13), '')) = 'cef82b6ff3f4f2edb8127acf24bbcc1a') THEN
CREATE OR REPLACE FUNCTION platform.grant_schema_to_role(target_schema text, target_role text, can_write boolean) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
$$;
END IF; END $recorded$;

DO $recorded$ BEGIN IF to_regprocedure('platform.apply_deployable_grants()') IS NULL OR NOT EXISTS (SELECT 1 FROM pg_proc WHERE oid = to_regprocedure('platform.apply_deployable_grants()') AND md5(replace(prosrc, chr(13), '')) = '6462e5aabaec31a3309d586032c2e5cf') THEN
CREATE OR REPLACE FUNCTION platform.apply_deployable_grants() RETURNS void
    LANGUAGE plpgsql
    AS $$
DECLARE
    mapped_oids oid[];
    host text;
    rel record;
BEGIN
    SELECT array_agg(oid) INTO mapped_oids FROM pg_namespace WHERE nspname IN ('control', 'platform');

    IF (SELECT rolsuper FROM pg_roles WHERE rolname = current_user) THEN
        EXECUTE format('GRANT CONNECT ON DATABASE %I TO ticvai_migrator, operations, workers', current_database());
        FOR rel IN SELECT nspname FROM pg_namespace WHERE oid = ANY (mapped_oids) AND nspowner <> 'ticvai_migrator'::regrole LOOP
            EXECUTE format('ALTER SCHEMA %I OWNER TO ticvai_migrator', rel.nspname);
        END LOOP;
        FOR rel IN
            SELECT c.oid::regclass AS name, c.relkind
              FROM pg_class c
             WHERE c.relnamespace = ANY (mapped_oids)
               AND c.relkind IN ('r', 'p', 'v', 'm', 'S')
               AND c.relowner <> 'ticvai_migrator'::regrole
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
    END IF;

    PERFORM platform.grant_schema_to_role('control', 'operations', true);
    PERFORM platform.grant_schema_to_role('control', 'workers', true);

    -- The policies call platform's predicates as the caller.
    FOREACH host IN ARRAY ARRAY['operations', 'workers'] LOOP
        EXECUTE format('GRANT USAGE ON SCHEMA platform TO %I', host);
    END LOOP;

    -- The register is the migrator's alone.
    REVOKE ALL ON platform.schema_version FROM commerce, access, operations, workers, ticvai_ai;

    -- The functions that change the schema are the migrator's; the predicates stay callable by all.
    FOR rel IN
        SELECT to_regprocedure(f) AS name
          FROM unnest(ARRAY['platform.apply_deployable_grants()', 'platform.grant_schema_to_role(text, text, boolean)',
                            'platform.apply_scope_rls(regclass)', 'platform.apply_shared_scope_rls(regclass, text)',
                            'platform.apply_parent_rls(regclass, text, regclass, text)']) f
         WHERE to_regprocedure(f) IS NOT NULL
    LOOP
        EXECUTE format('REVOKE EXECUTE ON FUNCTION %s FROM PUBLIC', rel.name);
    END LOOP;
END
$$;
END IF; END $recorded$;

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0120', 'after r1 (9cec72d): 0 table(s), 4 column(s), 2 index(es), 2 other statement(s)', 'ab5266b3d1b17e90e5386e486c6710bb6dc8f9ebe7132c2f319dd56322a6e4c9')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- DROP FUNCTION IF EXISTS platform.apply_deployable_grants();
-- DROP FUNCTION IF EXISTS platform.grant_schema_to_role(text, text, boolean);
-- DROP INDEX IF EXISTS control.release_withdrawal_approved_by_principal_id_idx;
-- DROP INDEX IF EXISTS control.release_status_changed_by_principal_id_idx;
-- ALTER TABLE control.release DROP COLUMN IF EXISTS withdrawal_approved_by_principal_id;
-- ALTER TABLE control.release DROP COLUMN IF EXISTS status_changed_at;
-- ALTER TABLE control.release DROP COLUMN IF EXISTS status_changed_by_principal_id;
-- ALTER TABLE control.release DROP COLUMN IF EXISTS status_reason;
-- DELETE FROM platform.schema_version WHERE version = 'V0120';
