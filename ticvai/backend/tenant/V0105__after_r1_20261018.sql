-- V0105 -- tenant database, after r1 (9cec72d) (20261018).
-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**
--
-- The baseline under backend/tenant/ is frozen at r1 (9cec72d), so the change to the schema reference
-- since then is written here instead: additive only. Changes that are not additive (drops, renames,
-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.
-- 0 table(s), 0 column(s), 0 index(es), 11 other statement(s), 25 row-level security polic(ies) re-applied.

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'invitation' AND column_name = 'product_id' AND is_nullable = 'NO') THEN ALTER TABLE marketing.invitation ALTER COLUMN product_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'marketing' AND table_name = 'invitation' AND column_name = 'offered_by_principal_id' AND is_nullable = 'NO') THEN ALTER TABLE marketing.invitation ALTER COLUMN offered_by_principal_id DROP NOT NULL; END IF; END $$;

ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_action_code_when_chk;

ALTER TABLE platform.sale_board_tile ADD CONSTRAINT sale_board_tile_action_code_when_chk CHECK (kind IS DISTINCT FROM 'action' OR action_code IS NOT NULL) NOT VALID;

ALTER TABLE platform.sale_board_tile VALIDATE CONSTRAINT sale_board_tile_action_code_when_chk;

ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_category_id_when_chk;

ALTER TABLE platform.sale_board_tile ADD CONSTRAINT sale_board_tile_category_id_when_chk CHECK (kind IS DISTINCT FROM 'category' OR category_id IS NOT NULL) NOT VALID;

ALTER TABLE platform.sale_board_tile VALIDATE CONSTRAINT sale_board_tile_category_id_when_chk;

ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_variant_id_when_chk;

ALTER TABLE platform.sale_board_tile ADD CONSTRAINT sale_board_tile_variant_id_when_chk CHECK (kind IS DISTINCT FROM 'product' OR variant_id IS NOT NULL) NOT VALID;

ALTER TABLE platform.sale_board_tile VALIDATE CONSTRAINT sale_board_tile_variant_id_when_chk;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'venue_settings' AND column_name = 'org_unit_id' AND is_nullable = 'NO') THEN ALTER TABLE platform.venue_settings ALTER COLUMN org_unit_id DROP NOT NULL; END IF; END $$;

DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND table_name = 'workstation' AND column_name = 'org_unit_id' AND is_nullable = 'NO') THEN ALTER TABLE platform.workstation ALTER COLUMN org_unit_id DROP NOT NULL; END IF; END $$;

CREATE OR REPLACE FUNCTION platform.visible_parent_ids(parent regclass, for_write boolean DEFAULT false)
    RETURNS SETOF uuid
    LANGUAGE plpgsql
    STABLE
    SECURITY DEFINER
    SET search_path = pg_catalog, public, pg_temp
AS $$
BEGIN
    IF parent = 'access.entitlement'::regclass THEN
        RETURN QUERY SELECT parent_row.id FROM access.entitlement parent_row;
        RETURN;
    END IF;
    IF parent = 'approvals.request'::regclass THEN
        RETURN QUERY SELECT parent_row.id FROM approvals.request parent_row;
        RETURN;
    END IF;
    IF parent = 'catalogue.performance'::regclass THEN
        RETURN QUERY SELECT parent_row.id FROM catalogue.performance parent_row;
        RETURN;
    END IF;
    IF parent = 'platform.outlet'::regclass THEN
        RETURN QUERY SELECT parent_row.id FROM platform.outlet parent_row;
        RETURN;
    END IF;
    IF parent = 'platform.workstation'::regclass THEN
        RETURN QUERY SELECT parent_row.id FROM platform.workstation parent_row;
        RETURN;
    END IF;
    RAISE EXCEPTION 'platform.visible_parent_ids: % is not a parent a policy names', parent;
END
$$;

CREATE OR REPLACE FUNCTION platform.visible_parent_ids_setup()
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    fn regprocedure := 'platform.visible_parent_ids(regclass, boolean)'::regprocedure;
    owner_bypasses boolean;
    me record;
    t text;
    rel regclass;
    r text;
BEGIN
    SELECT o.rolsuper OR o.rolbypassrls INTO owner_bypasses
      FROM pg_catalog.pg_proc f JOIN pg_catalog.pg_roles o ON o.oid = f.proowner WHERE f.oid = fn;
    IF owner_bypasses THEN
        SELECT m.rolsuper, m.rolcreaterole INTO me FROM pg_catalog.pg_roles m WHERE m.rolname = current_user;
        IF me.rolsuper OR me.rolcreaterole THEN
            IF NOT EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'ticvai_parent_visible') THEN
                CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE;
            END IF;
            IF NOT me.rolsuper THEN
                EXECUTE format('GRANT ticvai_parent_visible TO %I WITH INHERIT TRUE, SET TRUE', current_user);
            END IF;
            EXECUTE 'GRANT USAGE ON SCHEMA platform, public TO ticvai_parent_visible';
            EXECUTE 'GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA platform TO ticvai_parent_visible';
            -- ALTER ... OWNER needs CREATE on the schema for the new owner; it is taken back at once
            EXECUTE 'GRANT CREATE ON SCHEMA platform TO ticvai_parent_visible';
            ALTER FUNCTION platform.visible_parent_ids(regclass, boolean) OWNER TO ticvai_parent_visible;
            EXECUTE 'REVOKE CREATE ON SCHEMA platform FROM ticvai_parent_visible';
        ELSE
            RAISE EXCEPTION 'platform.visible_parent_ids is owned by %, which bypasses row-level security, and % may not create a role to own it instead: every child row of a parent in another deployable would be visible. Migrate as a role without BYPASSRLS (DB-ROLES), or as one that may create roles',
                (SELECT f.proowner::regrole FROM pg_catalog.pg_proc f WHERE f.oid = fn), current_user;
        END IF;
    END IF;
    IF (SELECT f.proowner::regrole::text FROM pg_catalog.pg_proc f WHERE f.oid = fn) = 'ticvai_parent_visible' THEN
        FOREACH t IN ARRAY ARRAY['access.entitlement', 'approvals.request', 'catalogue.event', 'catalogue.performance', 'platform.outlet', 'platform.scope', 'platform.workstation']::text[] LOOP
            rel := pg_catalog.to_regclass(t);
            CONTINUE WHEN rel IS NULL;
            EXECUTE format('GRANT USAGE ON SCHEMA %I TO ticvai_parent_visible',
                           (SELECT n.nspname FROM pg_catalog.pg_class c
                              JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.oid = rel));
            EXECUTE format('GRANT SELECT ON %s TO ticvai_parent_visible', rel);
        END LOOP;
    END IF;
    EXECUTE 'REVOKE EXECUTE ON FUNCTION platform.visible_parent_ids(regclass, boolean) FROM PUBLIC';
    FOREACH r IN ARRAY ARRAY['commerce', 'access', 'operations', 'workers', 'ticvai_ai'] LOOP
        IF EXISTS (SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = r) THEN
            EXECUTE format('GRANT EXECUTE ON FUNCTION platform.visible_parent_ids(regclass, boolean) TO %I', r);
        END IF;
    END LOOP;
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_parent_across_rls(target regclass, fk_column text,
                                                            parent regclass, parent_key text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('%I IN (SELECT platform.visible_parent_ids(%L::regclass))', fk_column, parent::text);
BEGIN
    IF parent_key <> 'id' THEN
        RAISE EXCEPTION 'apply_parent_across_rls: % keys its parent % by %, and platform.visible_parent_ids returns a parent''s id',
            target, parent, parent_key;
    END IF;
    PERFORM platform.visible_parent_ids_setup();
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (%s) WITH CHECK (%s)',
                   policy_name, target, predicate, predicate);
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_parent_split_across_rls(target regclass, fk_column text, parent regclass,
                                                                  parent_key text, parent_write text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    IF parent_key <> 'id' THEN
        RAISE EXCEPTION 'apply_parent_split_across_rls: % keys its parent % by %, and platform.visible_parent_ids returns a parent''s id',
            target, parent, parent_key;
    END IF;
    PERFORM platform.visible_parent_ids_setup();
    PERFORM platform.apply_split_rls(target,
        format('%I IN (SELECT platform.visible_parent_ids(%L::regclass))', fk_column, parent::text),
        format('%I IN (SELECT platform.visible_parent_ids(%L::regclass, true))', fk_column, parent::text));
END
$$;

SELECT platform.drop_rls_policies('access.policy_scope_assignment'::regclass);

SELECT platform.apply_read_beneath_rls('access.policy_scope_assignment'::regclass);

SELECT platform.drop_rls_policies('ai.provider'::regclass);

SELECT platform.apply_read_beneath_rls('ai.provider'::regclass);

SELECT platform.drop_rls_policies('approvals.matrix'::regclass);

SELECT platform.apply_read_beneath_rls('approvals.matrix'::regclass);

SELECT platform.drop_rls_policies('catalogue.dynamic_pricing_control'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.dynamic_pricing_control'::regclass);

SELECT platform.drop_rls_policies('catalogue.sales_channel'::regclass);

SELECT platform.apply_read_beneath_rls('catalogue.sales_channel'::regclass);

SELECT platform.drop_rls_policies('marketing.service_copilot_config'::regclass);

SELECT platform.apply_read_beneath_rls('marketing.service_copilot_config'::regclass);

SELECT platform.drop_rls_policies('payments.provider'::regclass);

SELECT platform.apply_read_beneath_rls('payments.provider'::regclass);

SELECT platform.drop_rls_policies('approvals.rule'::regclass);

SELECT platform.apply_parent_split_rls('approvals.rule'::regclass, 'matrix_id', 'approvals.matrix'::regclass, 'id', 'platform.in_scope(parent_row.scope_path)');

SELECT platform.drop_rls_policies('fnb.kitchen_sla'::regclass);

SELECT platform.apply_parent_across_rls('fnb.kitchen_sla'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.kitchen_ticket'::regclass);

SELECT platform.apply_parent_across_rls('fnb.kitchen_ticket'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.menu'::regclass);

SELECT platform.apply_parent_across_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.service_order'::regclass);

SELECT platform.apply_parent_across_rls('fnb.service_order'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.table_reservation'::regclass);

SELECT platform.apply_parent_across_rls('fnb.table_reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.table_session'::regclass);

SELECT platform.apply_parent_across_rls('fnb.table_session'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.table_visit'::regclass);

SELECT platform.apply_parent_across_rls('fnb.table_visit'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('fnb.waitlist_entry'::regclass);

SELECT platform.apply_parent_across_rls('fnb.waitlist_entry'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('pii.subject_biometric'::regclass);

SELECT platform.apply_parent_across_rls('pii.subject_biometric'::regclass, 'entitlement_id', 'access.entitlement'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.merchandise'::regclass);

SELECT platform.apply_parent_across_rls('retail.merchandise'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.reservation'::regclass);

SELECT platform.apply_parent_across_rls('retail.reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.return_policy'::regclass);

SELECT platform.apply_parent_across_rls('retail.return_policy'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.sale'::regclass);

SELECT platform.apply_parent_across_rls('retail.sale'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');

SELECT platform.drop_rls_policies('platform.dsar_request'::regclass);

SELECT platform.apply_parent_across_rls('platform.dsar_request'::regclass, 'request_id', 'approvals.request'::regclass, 'id');

SELECT platform.drop_rls_policies('sync.rejection'::regclass);

SELECT platform.apply_parent_across_rls('sync.rejection'::regclass, 'workstation_id', 'platform.workstation'::regclass, 'id');

SELECT platform.drop_rls_policies('resources.performance_participant'::regclass);

SELECT platform.apply_parent_across_rls('resources.performance_participant'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');

SELECT platform.drop_rls_policies('retail.exchange'::regclass);

SELECT platform.apply_parent_rls('retail.exchange'::regclass, 'sale_id', 'retail.sale'::regclass, 'id');

INSERT INTO platform.schema_version (version, description, checksum)
VALUES ('V0105', 'after r1 (9cec72d): 0 table(s), 0 column(s), 0 index(es), 11 other statement(s), 25 row-level security polic(ies) re-applied', 'de7e934e829dbaaade1838fa4d1b68f62aa5f2396a23de35419599782f5dc1bb')
ON CONFLICT (version) DO NOTHING;

-- ============================================================================
-- ROLLBACK
-- ============================================================================
-- Commented out so that applying this file never runs it: the rollback is run by removing the
-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).
-- SELECT platform.drop_rls_policies('retail.exchange'::regclass); SELECT platform.apply_tenant_rls('retail.exchange'::regclass); SELECT platform.apply_parent_rls('retail.exchange'::regclass, 'new_sale_id', 'retail.sale'::regclass, 'id');
-- SELECT platform.drop_rls_policies('resources.performance_participant'::regclass); SELECT platform.apply_subject_rls('resources.performance_participant'::regclass); SELECT platform.apply_parent_rls('resources.performance_participant'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');
-- SELECT platform.drop_rls_policies('sync.rejection'::regclass); SELECT platform.apply_parent_rls('sync.rejection'::regclass, 'workstation_id', 'platform.workstation'::regclass, 'id');
-- SELECT platform.drop_rls_policies('platform.dsar_request'::regclass); SELECT platform.apply_parent_rls('platform.dsar_request'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
-- SELECT platform.drop_rls_policies('retail.sale'::regclass); SELECT platform.apply_subject_rls('retail.sale'::regclass); SELECT platform.apply_parent_rls('retail.sale'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('retail.return_policy'::regclass); SELECT platform.apply_parent_rls('retail.return_policy'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('retail.reservation'::regclass); SELECT platform.apply_parent_rls('retail.reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('retail.merchandise'::regclass); SELECT platform.apply_parent_rls('retail.merchandise'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('pii.subject_biometric'::regclass); SELECT platform.apply_parent_rls('pii.subject_biometric'::regclass, 'entitlement_id', 'access.entitlement'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.waitlist_entry'::regclass); SELECT platform.apply_parent_rls('fnb.waitlist_entry'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.table_visit'::regclass); SELECT platform.apply_parent_rls('fnb.table_visit'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.table_session'::regclass); SELECT platform.apply_parent_rls('fnb.table_session'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.table_reservation'::regclass); SELECT platform.apply_parent_rls('fnb.table_reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.service_order'::regclass); SELECT platform.apply_parent_rls('fnb.service_order'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.menu'::regclass); SELECT platform.apply_parent_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.kitchen_ticket'::regclass); SELECT platform.apply_parent_rls('fnb.kitchen_ticket'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('fnb.kitchen_sla'::regclass); SELECT platform.apply_tenant_rls('fnb.kitchen_sla'::regclass); SELECT platform.apply_parent_rls('fnb.kitchen_sla'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
-- SELECT platform.drop_rls_policies('approvals.rule'::regclass); SELECT platform.apply_parent_rls('approvals.rule'::regclass, 'matrix_id', 'approvals.matrix'::regclass, 'id');
-- SELECT platform.drop_rls_policies('payments.provider'::regclass); SELECT platform.apply_scope_rls('payments.provider'::regclass);
-- SELECT platform.drop_rls_policies('marketing.service_copilot_config'::regclass); SELECT platform.apply_scope_rls('marketing.service_copilot_config'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.sales_channel'::regclass); SELECT platform.apply_scope_rls('catalogue.sales_channel'::regclass);
-- SELECT platform.drop_rls_policies('catalogue.dynamic_pricing_control'::regclass); SELECT platform.apply_scope_rls('catalogue.dynamic_pricing_control'::regclass);
-- SELECT platform.drop_rls_policies('approvals.matrix'::regclass); SELECT platform.apply_scope_rls('approvals.matrix'::regclass);
-- SELECT platform.drop_rls_policies('ai.provider'::regclass); SELECT platform.apply_scope_rls('ai.provider'::regclass);
-- SELECT platform.drop_rls_policies('access.policy_scope_assignment'::regclass); SELECT platform.apply_scope_rls('access.policy_scope_assignment'::regclass);
-- ALTER TABLE platform.workstation ALTER COLUMN org_unit_id SET NOT NULL;
-- ALTER TABLE platform.venue_settings ALTER COLUMN org_unit_id SET NOT NULL;
-- ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_variant_id_when_chk;
-- ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_category_id_when_chk;
-- ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS sale_board_tile_action_code_when_chk;
-- ALTER TABLE marketing.invitation ALTER COLUMN offered_by_principal_id SET NOT NULL;
-- ALTER TABLE marketing.invitation ALTER COLUMN product_id SET NOT NULL;
-- DELETE FROM platform.schema_version WHERE version = 'V0105';
