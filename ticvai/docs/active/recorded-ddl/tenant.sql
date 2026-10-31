-- What the tenant database on live has that the package did not record, recorded. AUTHORED: a person writes it.
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
-- **The outbox's sequence counter follows the outbox** (the developers' migration 240, outbox sequence counter and
-- occurred_at; ADR-0058, ADAM CR-166, CHG-CRA-005). A writer allocates `sequence` from platform.outbox_sequence in
-- its transaction; this trigger keeps the counter at the highest sequence an outbox row was written with, so a row
-- written with a sequence of its own cannot be followed by a duplicate.
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

-- @beside 920
CREATE TRIGGER outbox_advance_sequence AFTER INSERT ON platform.outbox FOR EACH ROW WHEN ((new.sequence > 0)) EXECUTE FUNCTION platform.outbox_advance_sequence();

-- @beside 920
-- A sequence starts at 1 (migration 240).
ALTER TABLE platform.outbox_sequence ADD CONSTRAINT outbox_sequence_last_sequence_chk CHECK ((last_sequence > 0));

-- @beside 920
-- **A journal entry's legal entity is its fiscal period's** (ADAM CR-168, CHG-CRA-007: entry numbers are unique per
-- legal entity). finance.JournalEntry.legalEntityId is readOnly, "copied from its fiscal period": the copy is this
-- trigger, on every insert and on every change of the period or of the column itself, and the CHECK below makes it
-- present on every row (a fiscal period's legal_entity_id is NOT NULL).
CREATE OR REPLACE FUNCTION ledger.journal_entry_legal_entity_sync() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    SELECT fp.legal_entity_id INTO NEW.legal_entity_id FROM ledger.fiscal_period fp WHERE fp.id = NEW.fiscal_period_id;
    RETURN NEW;
END
$$;

-- @beside 920
CREATE TRIGGER journal_entry_legal_entity_sync BEFORE INSERT OR UPDATE OF fiscal_period_id, legal_entity_id ON ledger.journal_entry FOR EACH ROW EXECUTE FUNCTION ledger.journal_entry_legal_entity_sync();

-- @beside 920
-- Every entry has one: the trigger above sets it from the period. On a database built from the package before this
-- block, an entry written without it stops the VALIDATE: fill it from the period first (see CHG-R12DB-003).
ALTER TABLE ledger.journal_entry ADD CONSTRAINT journal_entry_legal_entity_id_chk CHECK ((legal_entity_id IS NOT NULL));

-- @beside 920
-- **One PostgreSQL role per deployable** (the developers' migration 004, deployable roles; DB-ROLES, ticket 27655;
-- ADR-0055). A role is granted USAGE and its privileges on every table, view and sequence of one schema;
-- `can_write` false is SELECT only (the AI). Monthly partitions are left out: they are reached through their parent.
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

-- @beside 920
-- **The grants of every deployable role** (migration 004). The owners below are handoff/service-decomposition.json's
-- deployables and their schemas, and the kernel grants are docs/active/cross-deployable-writes.yaml `kernel`, exactly
-- (tools/check-ddl-conventions.py D-RECORDED-GRANTS fails on any difference). The reads one deployable is granted on
-- another's tables are not here: derive-ddl writes them from that file's `reads` (deployable_read_grants). The
-- migrator calls it after each migration, as a superuser on a new database (ownership) and as itself after.
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

-- @beside 920
-- **A scope rule evaluated once per statement** (the developers' migration 225, row-level security on the hot tables).
-- The same rule as apply_scope_rls (`platform.in_scope(scope_path)`), with the caller's paths read in a subquery
-- the planner runs once, so a table read at the gate's rate does not call a function per row. On live it makes
-- access.scan_event's policy; the package still gives that table apply_scope_rls, which admits the same rows.
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

-- @beside 930
-- **Partition retention** (the developers' migration 050, partition maintenance; ADR-0056, ADR-0047; ticket 27649).
-- Detaches every monthly partition of `target` that ends on or before `cutoff`, puts row-level security on it and
-- says so in its comment, and returns the partitions it detached; archiving and dropping them stays the job's.
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
