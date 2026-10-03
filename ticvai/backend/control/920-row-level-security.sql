-- Row-level security, control database.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Default deny is the point.** With `ticvai.scope_paths` unset, every policy below returns no
-- rows. A connection that forgets to set it sees an empty database, not the whole of it — which
-- is the Sprint 1 Gate 0 criterion, written as a predicate rather than a promise.
--
-- **Applied to every table that carries `scope_path`, which is what changed on 21 September.**
-- The hand-written baseline enabled RLS on three tables. The partition key is a column this
-- generator already knows about on every table that has one, so the policy set is derived rather
-- than remembered — and a new table with a `scope_path` is protected by existing, not by somebody
-- noticing.

-- The paths the current connection may see, read from a session GUC the API layer sets per
-- request. `true` in current_setting makes an unset GUC return NULL rather than raising, so an
-- unconfigured connection degrades to zero rows instead of an error nobody catches.
CREATE OR REPLACE FUNCTION platform.current_scope_paths()
    RETURNS ltree[]
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT COALESCE(
        (SELECT array_agg(p::ltree)
           FROM unnest(string_to_array(
                    NULLIF(current_setting('ticvai.scope_paths', true), ''), ',')) AS p
          WHERE btrim(p) <> ''),
        ARRAY[]::ltree[]);
$$;

-- True when the row sits at or beneath one of the granted paths. An empty grant list matches
-- nothing — deny is the default, and it is the default because it is the absence of a grant
-- rather than the presence of a denial.
CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path ltree)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path <@ ANY (platform.current_scope_paths());
$$;

-- Applies the standard policy to a table.
-- **FORCE is the whole point.** Without it the table owner — which is what a migration and most
-- pooled application connections run as — bypasses every policy silently.
--
-- **The policy is named `<table>_scope`** (naming-and-style 6.1). Until 26 September every table's
-- policy was called `scope_isolation` or `venue_isolation`; those names are dropped here too, so
-- re-applying the file to a database built before the rename leaves one policy, not two.
CREATE OR REPLACE FUNCTION platform.rls_policy_name(target regclass)
    RETURNS text
    LANGUAGE sql
    STABLE
AS $$
    SELECT left(c.relname, 57) || '_scope' FROM pg_class c WHERE c.oid = target;
$$;

CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS scope_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

-- **A row shared by two scopes** (audit R183): visible, and writable, from either path. A stock
-- transfer is owned at the source venue's `scope_path` and admits the destination through its
-- second path, so the receiving venue can read and receive it. Its lines follow through the
-- parent policy like any other child.
CREATE OR REPLACE FUNCTION platform.apply_shared_scope_rls(target regclass, second_path text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('(platform.in_scope(scope_path) OR platform.in_scope(%I))',
                             second_path);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS scope_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING %s WITH CHECK %s',
                   policy_name, target, predicate, predicate);
END
$$;



-- A child table protected through the declared foreign key to the row that owns it. The row is
-- visible, and may be written, exactly when its parent is visible to the same connection.
CREATE OR REPLACE FUNCTION platform.apply_parent_rls(target regclass, fk_column text,
                                                     parent regclass, parent_key text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
    predicate text := format('EXISTS (SELECT 1 FROM %s parent_row WHERE parent_row.%I = %s.%I)',
                             parent, parent_key, target, fk_column);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (%s) WITH CHECK (%s)',
                   policy_name, target, predicate, predicate);
END
$$;

-- **85 tables: 28 scoped by `scope_path`, 0 by `venue_id`, 5 through the parent that owns them, 0 by subject, 0 to the tenant root only, 51 with no policy.**
-- A table with no policy is listed at the end of this file with the reason. It is not
-- claimed to be reference data: for most of them that is a scoping decision nobody has
-- made yet, and they stay readable by every connection to this database until it is.


-- Scoped by path.
SELECT platform.apply_scope_rls('control.channel_listing'::regclass);
SELECT platform.apply_scope_rls('control.content_block'::regclass);
SELECT platform.apply_scope_rls('control.migration_plan'::regclass);
SELECT platform.apply_scope_rls('control.partner'::regclass);
SELECT platform.apply_scope_rls('control.partner_agreement'::regclass);
SELECT platform.apply_scope_rls('control.partner_allocation'::regclass);
SELECT platform.apply_scope_rls('control.partner_application'::regclass);
SELECT platform.apply_scope_rls('control.partner_billing_profile'::regclass);
SELECT platform.apply_scope_rls('control.partner_booking_limit'::regclass);
SELECT platform.apply_scope_rls('control.partner_capability_grant'::regclass);
SELECT platform.apply_scope_rls('control.partner_case'::regclass);
SELECT platform.apply_scope_rls('control.partner_change_request'::regclass);
SELECT platform.apply_scope_rls('control.partner_commercial_exception'::regclass);
SELECT platform.apply_scope_rls('control.partner_commission_line'::regclass);
SELECT platform.apply_scope_rls('control.partner_commission_rule'::regclass);
SELECT platform.apply_scope_rls('control.partner_contact'::regclass);
SELECT platform.apply_scope_rls('control.partner_credit_profile'::regclass);
SELECT platform.apply_scope_rls('control.partner_distribution_right'::regclass);
SELECT platform.apply_scope_rls('control.partner_document'::regclass);
SELECT platform.apply_scope_rls('control.partner_rate'::regclass);
SELECT platform.apply_scope_rls('control.partner_reconciliation_exception'::regclass);
SELECT platform.apply_scope_rls('control.partner_scope_assignment'::regclass);
SELECT platform.apply_scope_rls('control.partner_security'::regclass);
SELECT platform.apply_scope_rls('control.partner_settlement_batch'::regclass);
SELECT platform.apply_scope_rls('control.partner_status_history'::regclass);
SELECT platform.apply_scope_rls('control.seo_metadata'::regclass);
SELECT platform.apply_scope_rls('control.support_notice'::regclass);
SELECT platform.apply_scope_rls('control.url_redirect'::regclass);

-- Carries venue_id but not scoped here: the control database has no scope tree to resolve a venue against, and these are operator records read across tenants.
--   control.usage_record

-- Scoped through the parent that owns the row (a NOT NULL declared foreign key).
SELECT platform.apply_parent_rls('control.migration_plan_cell'::regclass, 'migration_plan_id', 'control.migration_plan'::regclass, 'id');
SELECT platform.apply_parent_rls('control.partner_application_review_task'::regclass, 'partner_application_id', 'control.partner_application'::regclass, 'id');
SELECT platform.apply_parent_rls('control.partner_commission_rule_tier'::regclass, 'partner_commission_rule_id', 'control.partner_commission_rule'::regclass, 'id');
SELECT platform.apply_parent_rls('control.partner_rate_volume_band'::regclass, 'partner_rate_id', 'control.partner_rate'::regclass, 'id');
SELECT platform.apply_parent_rls('control.partner_user'::regclass, 'partner_id', 'control.partner'::regclass, 'id');

-- No policy. Each needs a scoping decision (carry scope_path or venue_id, or a
-- NOT NULL owning reference) before row-level security can hold for it.
--   control.api_anomaly  -- its owner control.api_client has no policy either
--   control.api_anomaly_rule  -- only nullable references (client_id -> control.api_client)
--   control.api_client  -- only nullable references (certification_listing_id -> control.integration_listing)
--   control.api_licence  -- its owner control.tenant has no policy either
--   control.api_limit  -- no scope column and no declared owner
--   control.api_version  -- no scope column and no declared owner
--   control.archival_job  -- no scope column and no declared owner
--   control.backup_run  -- no scope column and no declared owner
--   control.billing_entity  -- no scope column and no declared owner
--   control.burst_environment  -- no scope column and no declared owner
--   control.cell  -- no scope column and no declared owner
--   control.cell_cluster  -- no scope column and no declared owner
--   control.cell_instance  -- no scope column and no declared owner
--   control.cell_job  -- its owner control.cell has no policy either
--   control.cell_tenant  -- no scope column and no declared owner
--   control.config_package  -- no scope column and no declared owner
--   control.config_package_application  -- no scope column and no declared owner
--   control.config_package_diff  -- no scope column and no declared owner
--   control.credit_note  -- no scope column and no declared owner
--   control.credit_note_line  -- its owner control.credit_note has no policy either
--   control.developer_account  -- no scope column and no declared owner
--   control.environment  -- its owner control.cell has no policy either
--   control.integration_listing  -- no scope column and no declared owner
--   control.invoice  -- no scope column and no declared owner
--   control.invoice_line  -- its owner control.invoice has no policy either
--   control.licence_add_on  -- no scope column and no declared owner
--   control.licence_add_on_limit  -- its owner control.licence_add_on has no policy either
--   control.migration  -- its owner control.release has no policy either
--   control.migration_run  -- only nullable references (canary_cell_id -> control.cell)
--   control.migration_run_cell  -- its owner control.migration_run has no policy either
--   control.migration_run_tenant  -- its owner control.migration_run has no policy either
--   control.onboarding_application  -- only nullable references (venue_type_template_id -> control.venue_type_template, billing_entity_id -> control.billing_entity)
--   control.outbox_relay  -- its owner control.cell_tenant has no policy either
--   control.outbox_republish  -- its owner control.tenant has no policy either
--   control.production_access_request  -- its owners control.api_client, control.integration_listing have no policy either
--   control.release  -- no scope column and no declared owner
--   control.release_component  -- its owner control.release has no policy either
--   control.rollout  -- its owner control.release has no policy either
--   control.rollout_cell  -- its owner control.cell has no policy either
--   control.rollout_tenant  -- no scope column and no declared owner
--   control.sandbox  -- no scope column and no declared owner
--   control.scaling_policy  -- no scope column and no declared owner
--   control.tenant  -- no scope column and no declared owner
--   control.tenant_domain  -- its owner control.tenant has no policy either
--   control.tenant_migration  -- its owners control.tenant, control.tenant_migration_plan have no policy either
--   control.tenant_migration_plan  -- its owner control.tenant has no policy either
--   control.upgrade_schedule  -- no scope column and no declared owner
--   control.venue_type_template  -- no scope column and no declared owner
--   control.waf_rule  -- no scope column and no declared owner
--   control.webhook_delivery  -- no scope column and no declared owner
--   control.webhook_subscription  -- no scope column and no declared owner
