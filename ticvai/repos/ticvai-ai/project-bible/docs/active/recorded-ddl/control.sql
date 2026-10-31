-- What the control database on live has that the package did not record, recorded. AUTHORED: a person writes it.
--
-- **The lead, 30 October 2026: "Record all"** (CHG-R12DB-002 to CHG-R12DB-006). The comparison of live with r11 that
-- day found objects the developers built in their own migrations and the package never had, so a database built from
-- the package alone lacked them. Each is copied here **verbatim** from live's schema-only dump of 30 October 2026
-- (PostgreSQL 17.6): a function's text is live's own, so applying the package's version to live changes nothing.
--
-- tools/derive-ddl.py reads this file (RECORDED_DDL) and writes each object into the generated file named by the
-- `-- @beside <file>` line above it, so the next forward migration carries it (tools/ddl_forward.py):
--   CREATE OR REPLACE FUNCTION      one guarded block: created where the function is missing or its text differs
--                                   (carriage returns aside: live's copies were applied from Windows checkouts and
--                                   have CRLF line endings, which a file in git cannot keep), so on live nothing is
--                                   replaced.
--   CREATE TRIGGER                  one guarded block (`DO $recorded$`): CREATE OR REPLACE TRIGGER, only where the
--                                   table, the columns it names, the tables its function names and the function are.
--   ALTER TABLE ... ADD CONSTRAINT  one guarded block: the CHECK added NOT VALID and validated, only where the table
--   ... CHECK                       and its columns are and no constraint of that name is yet (so not on live).
-- Nothing else is read here. A comment above each object says where it came from and what it is for.

-- @beside 920
-- **One PostgreSQL role per deployable**, the control database's (the developers' migration 004; DB-ROLES). As the
-- tenant's, but for the partition filter: the control database partitions nothing.
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

-- @beside 920
-- **The grants on the control database** (migration 004): `control` is written by operations (the Control Plane,
-- handoff/service-decomposition.json) and by workers.
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
