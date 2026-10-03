-- Row-level security.
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

-- **81 tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path`
-- alone leaves every one of them open.** `check-migrations` has said so since it was written --
-- checking only scope_path missed the tables that carry venue_id instead, and they would have
-- passed with no policy at all -- and the hand-written baseline never closed it because it
-- protected three tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on those 81 tables**, and
-- `platform.scope` is small, cached and indexed on `id` and, with GiST, on `path`.
--
-- **A null `venue_id` is a tenant-level row, and until 24 September nobody could see it** — not
-- even head office, because the function opened with `row_venue_id IS NOT NULL`. It now follows
-- the tenant-root rule: such a row sits at the tenant root, so it is visible exactly when a
-- grant *is* that root — the one `platform.scope` row whose `level` is `tenant` (ADR-0011; the
-- node the cell creates at provisioning, `parentId` null). A brand, region or venue grant is
-- beneath the root, not at it, and still sees none of it. No grants, still nothing.
CREATE OR REPLACE FUNCTION platform.venue_in_scope(row_venue_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND CASE
             WHEN row_venue_id IS NULL THEN EXISTS (
                  SELECT 1 FROM platform.scope s
                   WHERE s.level = 'tenant'
                     AND s.path = ANY (platform.current_scope_paths()))
                  -- one tenant per database (CF-161); if that ever stops being true, a null-venue
                  -- row has no single tenant to belong to, so it is hidden rather than shown to all
                  AND (SELECT count(*) FROM platform.scope s WHERE s.level = 'tenant') = 1
             ELSE EXISTS (
                  SELECT 1 FROM platform.scope s
                   WHERE s.id = row_venue_id
                     AND s.path <@ ANY (platform.current_scope_paths()))
           END;
$$;

CREATE OR REPLACE FUNCTION platform.apply_venue_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS venue_isolation ON %s', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.venue_in_scope(venue_id)) '
        'WITH CHECK (platform.venue_in_scope(venue_id))', policy_name, target);
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


-- True when the connection holds the tenant root itself (head office, or a worker's system scope).
CREATE OR REPLACE FUNCTION platform.tenant_root_in_scope()
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT cardinality(platform.current_scope_paths()) > 0
       AND EXISTS (SELECT 1 FROM platform.scope s
                    WHERE s.level = 'tenant'
                      AND s.path = ANY (platform.current_scope_paths()));
$$;

-- True when the row belongs to the session's own subject, or the connection holds the tenant root.
CREATE OR REPLACE FUNCTION platform.subject_in_scope(row_subject_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT (row_subject_id IS NOT NULL
            AND row_subject_id::text = NULLIF(current_setting('ticvai.subject_id', true), ''))
        OR platform.tenant_root_in_scope();
$$;

CREATE OR REPLACE FUNCTION platform.apply_tenant_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (platform.tenant_root_in_scope()) '
                   'WITH CHECK (platform.tenant_root_in_scope())', policy_name, target);
END
$$;

CREATE OR REPLACE FUNCTION platform.apply_subject_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := platform.rls_policy_name(target);
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format('CREATE POLICY %I ON %s USING (platform.subject_in_scope(subject_id)) '
                   'WITH CHECK (platform.subject_in_scope(subject_id))', policy_name, target);
END
$$;

-- **1027 tables: 584 scoped by `scope_path`, 81 by `venue_id`, 151 through the parent that owns them, 28 by subject, 182 to the tenant root only, 0 with no policy.**
-- A table with no policy is listed at the end of this file with the reason. It is not
-- claimed to be reference data: for most of them that is a scoping decision nobody has
-- made yet, and they stay readable by every connection to this database until it is.


ALTER TABLE platform.scope ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.scope FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS scope_isolation ON platform.scope;
DROP POLICY IF EXISTS scope_scope ON platform.scope;
CREATE POLICY scope_scope ON platform.scope
    USING (platform.in_scope(path))
    WITH CHECK (platform.in_scope(path));


-- Scoped by path.
SELECT platform.apply_scope_rls('access.access_area'::regclass);
SELECT platform.apply_scope_rls('access.access_attribute'::regclass);
SELECT platform.apply_scope_rls('access.access_incident'::regclass);
SELECT platform.apply_scope_rls('access.access_map'::regclass);
SELECT platform.apply_scope_rls('access.access_point'::regclass);
SELECT platform.apply_scope_rls('access.access_point_configuration'::regclass);
SELECT platform.apply_scope_rls('access.access_point_group'::regclass);
SELECT platform.apply_scope_rls('access.accreditation_credential'::regclass);
SELECT platform.apply_scope_rls('access.admission_rules'::regclass);
SELECT platform.apply_scope_rls('access.attraction_access'::regclass);
SELECT platform.apply_scope_rls('access.biometric_audit_event'::regclass);
SELECT platform.apply_scope_rls('access.biometric_profile'::regclass);
SELECT platform.apply_scope_rls('access.blacklist'::regclass);
SELECT platform.apply_scope_rls('access.branding_profile'::regclass);
SELECT platform.apply_scope_rls('access.companion_rule'::regclass);
SELECT platform.apply_scope_rls('access.configuration_change'::regclass);
SELECT platform.apply_scope_rls('access.configuration_version'::regclass);
SELECT platform.apply_scope_rls('access.consumption_rule'::regclass);
SELECT platform.apply_scope_rls('access.credential_binding'::regclass);
SELECT platform.apply_scope_rls('access.credential_delivery'::regclass);
SELECT platform.apply_scope_rls('access.credential_event'::regclass);
SELECT platform.apply_scope_rls('access.credential_event_propagation_rule'::regclass);
SELECT platform.apply_scope_rls('access.credential_exception'::regclass);
SELECT platform.apply_scope_rls('access.credential_issuance'::regclass);
SELECT platform.apply_scope_rls('access.credential_issuance_retry_policy'::regclass);
SELECT platform.apply_scope_rls('access.credential_policy'::regclass);
SELECT platform.apply_scope_rls('access.credential_security_profile'::regclass);
SELECT platform.apply_scope_rls('access.credential_sharing_case'::regclass);
SELECT platform.apply_scope_rls('access.device_binding'::regclass);
SELECT platform.apply_scope_rls('access.device_configuration'::regclass);
SELECT platform.apply_scope_rls('access.device_placement'::regclass);
SELECT platform.apply_scope_rls('access.dynamic_field'::regclass);
SELECT platform.apply_scope_rls('access.dynamic_policy'::regclass);
SELECT platform.apply_scope_rls('access.dynamic_policy_version'::regclass);
SELECT platform.apply_scope_rls('access.edge_node'::regclass);
SELECT platform.apply_scope_rls('access.edge_package'::regclass);
SELECT platform.apply_scope_rls('access.entitlement'::regclass);
SELECT platform.apply_scope_rls('access.external_credential_integration'::regclass);
SELECT platform.apply_scope_rls('access.face_reenrolment_attempt'::regclass);
SELECT platform.apply_scope_rls('access.fast_pass_profile'::regclass);
SELECT platform.apply_scope_rls('access.fraud_rule'::regclass);
SELECT platform.apply_scope_rls('access.gate_lane'::regclass);
SELECT platform.apply_scope_rls('access.gate_mode_change'::regclass);
SELECT platform.apply_scope_rls('access.gate_mode_policy'::regclass);
SELECT platform.apply_scope_rls('access.gate_outcome_profile'::regclass);
SELECT platform.apply_scope_rls('access.group_admission_rule'::regclass);
SELECT platform.apply_scope_rls('access.hardware_certification'::regclass);
SELECT platform.apply_scope_rls('access.hardware_deployment'::regclass);
SELECT platform.apply_scope_rls('access.hardware_model'::regclass);
SELECT platform.apply_scope_rls('access.identity_lock'::regclass);
SELECT platform.apply_scope_rls('access.journey_profile'::regclass);
SELECT platform.apply_scope_rls('access.journey_sequence_rule'::regclass);
SELECT platform.apply_scope_rls('access.media_binding_rule'::regclass);
SELECT platform.apply_scope_rls('access.media_compatibility_test'::regclass);
SELECT platform.apply_scope_rls('access.media_encoding_profile'::regclass);
SELECT platform.apply_scope_rls('access.media_replacement_policy'::regclass);
SELECT platform.apply_scope_rls('access.media_template'::regclass);
SELECT platform.apply_scope_rls('access.media_template_version'::regclass);
SELECT platform.apply_scope_rls('access.media_type'::regclass);
SELECT platform.apply_scope_rls('access.offline_policy'::regclass);
SELECT platform.apply_scope_rls('access.operating_calendar_entry'::regclass);
SELECT platform.apply_scope_rls('access.podium'::regclass);
SELECT platform.apply_scope_rls('access.podium_shift'::regclass);
SELECT platform.apply_scope_rls('access.policy_evaluation_setting'::regclass);
SELECT platform.apply_scope_rls('access.policy_scope_assignment'::regclass);
SELECT platform.apply_scope_rls('access.reason_code'::regclass);
SELECT platform.apply_scope_rls('access.risk_scoring_config'::regclass);
SELECT platform.apply_scope_rls('access.scan_event'::regclass);
SELECT platform.apply_scope_rls('access.security_alert'::regclass);
SELECT platform.apply_scope_rls('access.security_investigation'::regclass);
SELECT platform.apply_scope_rls('access.security_playbook'::regclass);
SELECT platform.apply_scope_rls('access.ticket_status_transition'::regclass);
SELECT platform.apply_scope_rls('access.verification_method_policy'::regclass);
SELECT platform.apply_scope_rls('accreditation.access_profile'::regclass);
SELECT platform.apply_scope_rls('accreditation.application'::regclass);
SELECT platform.apply_scope_rls('accreditation.audit'::regclass);
SELECT platform.apply_scope_rls('accreditation.badge_template'::regclass);
SELECT platform.apply_scope_rls('accreditation.credential'::regclass);
SELECT platform.apply_scope_rls('accreditation.data_export'::regclass);
SELECT platform.apply_scope_rls('accreditation.document'::regclass);
SELECT platform.apply_scope_rls('accreditation.holder'::regclass);
SELECT platform.apply_scope_rls('accreditation.holder_access'::regclass);
SELECT platform.apply_scope_rls('accreditation.identity_conflict'::regclass);
SELECT platform.apply_scope_rls('accreditation.mobile_credential_delivery'::regclass);
SELECT platform.apply_scope_rls('accreditation.notification_rules'::regclass);
SELECT platform.apply_scope_rls('accreditation.print_job'::regclass);
SELECT platform.apply_scope_rls('accreditation.programme'::regclass);
SELECT platform.apply_scope_rls('accreditation.requirements'::regclass);
SELECT platform.apply_scope_rls('accreditation.validity'::regclass);
SELECT platform.apply_scope_rls('ai.action_plan'::regclass);
SELECT platform.apply_scope_rls('ai.activity'::regclass);
SELECT platform.apply_scope_rls('ai.anomaly_detector'::regclass);
SELECT platform.apply_scope_rls('ai.answer_feedback'::regclass);
SELECT platform.apply_scope_rls('ai.approval_request_score'::regclass);
SELECT platform.apply_scope_rls('ai.assistant_profile'::regclass);
SELECT platform.apply_scope_rls('ai.blueprint'::regclass);
SELECT platform.apply_scope_rls('ai.byok_enablement'::regclass);
SELECT platform.apply_scope_rls('ai.capability'::regclass);
SELECT platform.apply_scope_rls('ai.capability_maturity'::regclass);
SELECT platform.apply_scope_rls('ai.config_session'::regclass);
SELECT platform.apply_scope_rls('ai.control'::regclass);
SELECT platform.apply_scope_rls('ai.control_test'::regclass);
SELECT platform.apply_scope_rls('ai.conversation'::regclass);
SELECT platform.apply_scope_rls('ai.decision_record'::regclass);
SELECT platform.apply_scope_rls('ai.entity_risk'::regclass);
SELECT platform.apply_scope_rls('ai.eval_run'::regclass);
SELECT platform.apply_scope_rls('ai.eval_suite'::regclass);
SELECT platform.apply_scope_rls('ai.evidence_package'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_accuracy'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_definition'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_export'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_point'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_scenario'::regclass);
SELECT platform.apply_scope_rls('ai.forecast_version'::regclass);
SELECT platform.apply_scope_rls('ai.governance_alert'::regclass);
SELECT platform.apply_scope_rls('ai.governance_policy'::regclass);
SELECT platform.apply_scope_rls('ai.governance_policy_version'::regclass);
SELECT platform.apply_scope_rls('ai.guided_choice_suggestion'::regclass);
SELECT platform.apply_scope_rls('ai.history_import'::regclass);
SELECT platform.apply_scope_rls('ai.history_observation'::regclass);
SELECT platform.apply_scope_rls('ai.incident'::regclass);
SELECT platform.apply_scope_rls('ai.index_failure'::regclass);
SELECT platform.apply_scope_rls('ai.insight'::regclass);
SELECT platform.apply_scope_rls('ai.intervention'::regclass);
SELECT platform.apply_scope_rls('ai.knowledge_collection'::regclass);
SELECT platform.apply_scope_rls('ai.knowledge_document'::regclass);
SELECT platform.apply_scope_rls('ai.knowledge_gap'::regclass);
SELECT platform.apply_scope_rls('ai.layout_draft'::regclass);
SELECT platform.apply_scope_rls('ai.model'::regclass);
SELECT platform.apply_scope_rls('ai.operational_requirement'::regclass);
SELECT platform.apply_scope_rls('ai.policy'::regclass);
SELECT platform.apply_scope_rls('ai.policy_exception'::regclass);
SELECT platform.apply_scope_rls('ai.prompt_template'::regclass);
SELECT platform.apply_scope_rls('ai.proposed_action'::regclass);
SELECT platform.apply_scope_rls('ai.provider'::regclass);
SELECT platform.apply_scope_rls('ai.rec_decision'::regclass);
SELECT platform.apply_scope_rls('ai.rec_decline'::regclass);
SELECT platform.apply_scope_rls('ai.rec_event'::regclass);
SELECT platform.apply_scope_rls('ai.release'::regclass);
SELECT platform.apply_scope_rls('ai.risk_alert'::regclass);
SELECT platform.apply_scope_rls('ai.risk_assessment'::regclass);
SELECT platform.apply_scope_rls('ai.risk_case'::regclass);
SELECT platform.apply_scope_rls('ai.risk_edge'::regclass);
SELECT platform.apply_scope_rls('ai.risk_register'::regclass);
SELECT platform.apply_scope_rls('ai.risk_strategy'::regclass);
SELECT platform.apply_scope_rls('ai.signal_observation'::regclass);
SELECT platform.apply_scope_rls('ai.signal_source'::regclass);
SELECT platform.apply_scope_rls('ai.spend_ceiling'::regclass);
SELECT platform.apply_scope_rls('ai.suggestion'::regclass);
SELECT platform.apply_scope_rls('ai.suggestion_outcome'::regclass);
SELECT platform.apply_scope_rls('ai.tool'::regclass);
SELECT platform.apply_scope_rls('ai.training_run'::regclass);
SELECT platform.apply_scope_rls('ai.venue_settings'::regclass);
SELECT platform.apply_scope_rls('approvals.approved_action_execution'::regclass);
SELECT platform.apply_scope_rls('approvals.approver_availability'::regclass);
SELECT platform.apply_scope_rls('approvals.automation'::regclass);
SELECT platform.apply_scope_rls('approvals.automation_execution'::regclass);
SELECT platform.apply_scope_rls('approvals.business_rule'::regclass);
SELECT platform.apply_scope_rls('approvals.control_policy'::regclass);
SELECT platform.apply_scope_rls('approvals.decision_record'::regclass);
SELECT platform.apply_scope_rls('approvals.decision_table'::regclass);
SELECT platform.apply_scope_rls('approvals.delegation'::regclass);
SELECT platform.apply_scope_rls('approvals.evidence_package'::regclass);
SELECT platform.apply_scope_rls('approvals.external_dispatch'::regclass);
SELECT platform.apply_scope_rls('approvals.external_provider'::regclass);
SELECT platform.apply_scope_rls('approvals.matrix'::regclass);
SELECT platform.apply_scope_rls('approvals.request'::regclass);
SELECT platform.apply_scope_rls('approvals.retention_policy'::regclass);
SELECT platform.apply_scope_rls('approvals.signature'::regclass);
SELECT platform.apply_scope_rls('approvals.sla_policy'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_definition'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_exception'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_instance'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_intervention'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_step_execution'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_trigger'::regclass);
SELECT platform.apply_scope_rls('approvals.workflow_version'::regclass);
SELECT platform.apply_scope_rls('assets.approval'::regclass);
SELECT platform.apply_scope_rls('assets.asset_version'::regclass);
SELECT platform.apply_scope_rls('assets.audit'::regclass);
SELECT platform.apply_scope_rls('assets.distribution_channel'::regclass);
SELECT platform.apply_scope_rls('assets.media_fingerprint'::regclass);
SELECT platform.apply_scope_rls('assets.rendition'::regclass);
SELECT platform.apply_scope_rls('assets.share'::regclass);
SELECT platform.apply_scope_rls('assets.tag'::regclass);
SELECT platform.apply_scope_rls('assets.taxonomy'::regclass);
SELECT platform.apply_scope_rls('catalogue.ai_catalogue_session'::regclass);
SELECT platform.apply_scope_rls('catalogue.ai_finding'::regclass);
SELECT platform.apply_scope_rls('catalogue.approval_policy'::regclass);
SELECT platform.apply_scope_rls('catalogue.audit_entry'::regclass);
SELECT platform.apply_scope_rls('catalogue.calculation_profile'::regclass);
SELECT platform.apply_scope_rls('catalogue.change_request'::regclass);
SELECT platform.apply_scope_rls('catalogue.channel_connection'::regclass);
SELECT platform.apply_scope_rls('catalogue.channel_incident'::regclass);
SELECT platform.apply_scope_rls('catalogue.channel_sales_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.channel_sync'::regclass);
SELECT platform.apply_scope_rls('catalogue.configuration_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.demand_forecast'::regclass);
SELECT platform.apply_scope_rls('catalogue.demand_signal'::regclass);
SELECT platform.apply_scope_rls('catalogue.dynamic_pricing_control'::regclass);
SELECT platform.apply_scope_rls('catalogue.dynamic_pricing_strategy'::regclass);
SELECT platform.apply_scope_rls('catalogue.entitlement_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.event'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_capacity_profile'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_change_treatment_policy'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_registration'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_reschedule'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_resource_plan'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_schedule'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_type'::regclass);
SELECT platform.apply_scope_rls('catalogue.fee'::regclass);
SELECT platform.apply_scope_rls('catalogue.fee_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.group_package'::regclass);
SELECT platform.apply_scope_rls('catalogue.import_job'::regclass);
SELECT platform.apply_scope_rls('catalogue.lifecycle_action'::regclass);
SELECT platform.apply_scope_rls('catalogue.lifecycle_workflow'::regclass);
SELECT platform.apply_scope_rls('catalogue.package_pricing'::regclass);
SELECT platform.apply_scope_rls('catalogue.performance_media'::regclass);
SELECT platform.apply_scope_rls('catalogue.performance_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.prepaid_minutes'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_assignment'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_category'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_execution'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_ladder'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_list_version'::regclass);
SELECT platform.apply_scope_rls('catalogue.price_resolution_policy'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_experiment'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_market'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_publication'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_recommendation'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_recommendation_decision'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_simulation'::regclass);
SELECT platform.apply_scope_rls('catalogue.pricing_test_case'::regclass);
SELECT platform.apply_scope_rls('catalogue.product'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_category'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_channel_assignment'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_eligibility_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_link'::regclass);
SELECT platform.apply_scope_rls('catalogue.rate'::regclass);
SELECT platform.apply_scope_rls('catalogue.rollback_action'::regclass);
SELECT platform.apply_scope_rls('catalogue.rounding_profile'::regclass);
SELECT platform.apply_scope_rls('catalogue.sales_channel'::regclass);
SELECT platform.apply_scope_rls('catalogue.seat_pricing_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.signal_registry'::regclass);
SELECT platform.apply_scope_rls('catalogue.space'::regclass);
SELECT platform.apply_scope_rls('catalogue.tax_profile'::regclass);
SELECT platform.apply_scope_rls('catalogue.tax_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.waiting_room_setting'::regclass);
SELECT platform.apply_scope_rls('fnb.corrective_action'::regclass);
SELECT platform.apply_scope_rls('fnb.course_rule'::regclass);
SELECT platform.apply_scope_rls('fnb.delivery_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.kitchen_routing_rule'::regclass);
SELECT platform.apply_scope_rls('fnb.menu_schedule'::regclass);
SELECT platform.apply_scope_rls('fnb.menu_version'::regclass);
SELECT platform.apply_scope_rls('fnb.modifier_group'::regclass);
SELECT platform.apply_scope_rls('fnb.order_fulfilment'::regclass);
SELECT platform.apply_scope_rls('fnb.outlet_template'::regclass);
SELECT platform.apply_scope_rls('fnb.prep_sheet_template'::regclass);
SELECT platform.apply_scope_rls('fnb.product_recommendation'::regclass);
SELECT platform.apply_scope_rls('fnb.reservation_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.service_charge_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.table_combination'::regclass);
SELECT platform.apply_scope_rls('fnb.temperature_checkpoint'::regclass);
SELECT platform.apply_scope_rls('fnb.waste_approval_policy'::regclass);
SELECT platform.apply_scope_rls('games.attraction_type'::regclass);
SELECT platform.apply_scope_rls('games.authorisation'::regclass);
SELECT platform.apply_scope_rls('games.card_expiry_rules'::regclass);
SELECT platform.apply_scope_rls('games.entitlement'::regclass);
SELECT platform.apply_scope_rls('games.gameplay_transaction'::regclass);
SELECT platform.apply_scope_rls('games.kiosk_config'::regclass);
SELECT platform.apply_scope_rls('games.operational_config'::regclass);
SELECT platform.apply_scope_rls('games.pricing'::regclass);
SELECT platform.apply_scope_rls('games.pricing_exception'::regclass);
SELECT platform.apply_scope_rls('games.prize_cost'::regclass);
SELECT platform.apply_scope_rls('games.reader'::regclass);
SELECT platform.apply_scope_rls('games.reader_profile'::regclass);
SELECT platform.apply_scope_rls('games.reader_sync_status'::regclass);
SELECT platform.apply_scope_rls('games.redemption_rules'::regclass);
SELECT platform.apply_scope_rls('games.validation_rules'::regclass);
SELECT platform.apply_scope_rls('identity.access_decision'::regclass);
SELECT platform.apply_scope_rls('identity.access_override'::regclass);
SELECT platform.apply_scope_rls('identity.access_review_campaign'::regclass);
SELECT platform.apply_scope_rls('identity.access_review_item'::regclass);
SELECT platform.apply_scope_rls('identity.authorisation_policy'::regclass);
SELECT platform.apply_scope_rls('identity.authorisation_policy_version'::regclass);
SELECT platform.apply_scope_rls('identity.capability_template'::regclass);
SELECT platform.apply_scope_rls('identity.delegated_access'::regclass);
SELECT platform.apply_scope_rls('identity.guest_verification_policy'::regclass);
SELECT platform.apply_scope_rls('identity.module_access'::regclass);
SELECT platform.apply_scope_rls('identity.password_policy'::regclass);
SELECT platform.apply_scope_rls('identity.platform_staff_grant'::regclass);
SELECT platform.apply_scope_rls('identity.segregation_rule'::regclass);
SELECT platform.apply_scope_rls('identity.sso_group_mapping'::regclass);
SELECT platform.apply_scope_rls('identity.sso_provider'::regclass);
SELECT platform.apply_scope_rls('inventory.kit_component'::regclass);
SELECT platform.apply_scope_rls('inventory.purchase_order'::regclass);
SELECT platform.apply_scope_rls('inventory.quotation'::regclass);
SELECT platform.apply_scope_rls('inventory.supplier'::regclass);
SELECT platform.apply_scope_rls('ledger.credit_memo'::regclass);
SELECT platform.apply_scope_rls('ledger.einvoice_transmission'::regclass);
SELECT platform.apply_scope_rls('ledger.einvoicing_provider'::regclass);
SELECT platform.apply_scope_rls('ledger.fx_provider_assignment'::regclass);
SELECT platform.apply_scope_rls('ledger.legal_entity'::regclass);
SELECT platform.apply_scope_rls('ledger.settlement'::regclass);
SELECT platform.apply_scope_rls('ledger.tax_invoice'::regclass);
SELECT platform.apply_scope_rls('ledger.tax_invoice_template'::regclass);
SELECT platform.apply_scope_rls('maintenance.asset_category'::regclass);
SELECT platform.apply_scope_rls('marketing.agent_service_profile'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_activation'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_list'::regclass);
SELECT platform.apply_scope_rls('marketing.booking_consent_record'::regclass);
SELECT platform.apply_scope_rls('marketing.business_event'::regclass);
SELECT platform.apply_scope_rls('marketing.campaign_variant'::regclass);
SELECT platform.apply_scope_rls('marketing.case_category'::regclass);
SELECT platform.apply_scope_rls('marketing.case_compensation_request'::regclass);
SELECT platform.apply_scope_rls('marketing.case_escalation'::regclass);
SELECT platform.apply_scope_rls('marketing.case_internal_request'::regclass);
SELECT platform.apply_scope_rls('marketing.case_linked_record'::regclass);
SELECT platform.apply_scope_rls('marketing.case_resolution'::regclass);
SELECT platform.apply_scope_rls('marketing.case_routing_rule'::regclass);
SELECT platform.apply_scope_rls('marketing.case_service_action'::regclass);
SELECT platform.apply_scope_rls('marketing.challenge'::regclass);
SELECT platform.apply_scope_rls('marketing.communication_preference_type'::regclass);
SELECT platform.apply_scope_rls('marketing.communication_provider'::regclass);
SELECT platform.apply_scope_rls('marketing.communication_routing_rule'::regclass);
SELECT platform.apply_scope_rls('marketing.consent_capture_point'::regclass);
SELECT platform.apply_scope_rls('marketing.consent_question'::regclass);
SELECT platform.apply_scope_rls('marketing.contact_automation'::regclass);
SELECT platform.apply_scope_rls('marketing.cookie_banner_design'::regclass);
SELECT platform.apply_scope_rls('marketing.cookie_scan_finding'::regclass);
SELECT platform.apply_scope_rls('marketing.cookie_scan_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.cookie_scan_run'::regclass);
SELECT platform.apply_scope_rls('marketing.device_consent'::regclass);
SELECT platform.apply_scope_rls('marketing.duplicate_candidate'::regclass);
SELECT platform.apply_scope_rls('marketing.feedback_classification'::regclass);
SELECT platform.apply_scope_rls('marketing.form_definition'::regclass);
SELECT platform.apply_scope_rls('marketing.form_definition_field'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_attribute_model'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_match_decision'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_match_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_relationship'::regclass);
SELECT platform.apply_scope_rls('marketing.identity_rules'::regclass);
SELECT platform.apply_scope_rls('marketing.invitation'::regclass);
SELECT platform.apply_scope_rls('marketing.invitation_campaign'::regclass);
SELECT platform.apply_scope_rls('marketing.journey'::regclass);
SELECT platform.apply_scope_rls('marketing.journey_enrollment'::regclass);
SELECT platform.apply_scope_rls('marketing.legal_hold'::regclass);
SELECT platform.apply_scope_rls('marketing.message_trigger'::regclass);
SELECT platform.apply_scope_rls('marketing.message_trigger_condition'::regclass);
SELECT platform.apply_scope_rls('marketing.minor_privacy_rule'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_action'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_change_set'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_exception'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_export_package'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_incident'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_notice_governance'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_request'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_request_type'::regclass);
SELECT platform.apply_scope_rls('marketing.processing_purpose'::regclass);
SELECT platform.apply_scope_rls('marketing.quality_evaluation'::regclass);
SELECT platform.apply_scope_rls('marketing.referral'::regclass);
SELECT platform.apply_scope_rls('marketing.retention_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.sender_identity'::regclass);
SELECT platform.apply_scope_rls('marketing.service_copilot_config'::regclass);
SELECT platform.apply_scope_rls('marketing.service_queue'::regclass);
SELECT platform.apply_scope_rls('marketing.sla_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.suppression'::regclass);
SELECT platform.apply_scope_rls('marketing.tracking_technology'::regclass);
SELECT platform.apply_scope_rls('marketing.tracking_technology_catalogue'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_association'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_exception'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_form_layout'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_localisation'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_master'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_requirement'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_requirement_event'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_signatory_rule'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_trigger_rule'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_verification'::regclass);
SELECT platform.apply_scope_rls('marketing.waiver_version_control'::regclass);
SELECT platform.apply_scope_rls('orders.after_sale_policy'::regclass);
SELECT platform.apply_scope_rls('orders.after_sale_request'::regclass);
SELECT platform.apply_scope_rls('orders.b2b_credit'::regclass);
SELECT platform.apply_scope_rls('orders.deposit_policy'::regclass);
SELECT platform.apply_scope_rls('orders.external_reference_mapping'::regclass);
SELECT platform.apply_scope_rls('orders.fraud_rule'::regclass);
SELECT platform.apply_scope_rls('orders.group_quote'::regclass);
SELECT platform.apply_scope_rls('orders.group_task'::regclass);
SELECT platform.apply_scope_rls('orders.group_visit_plan'::regclass);
SELECT platform.apply_scope_rls('orders.order_event'::regclass);
SELECT platform.apply_scope_rls('orders.order_relationship'::regclass);
SELECT platform.apply_scope_rls('orders.order_source_channel'::regclass);
SELECT platform.apply_scope_rls('orders.payment_allocation_rule'::regclass);
SELECT platform.apply_scope_rls('orders.payment_link'::regclass);
SELECT platform.apply_scope_rls('orders.pos_shift'::regclass);
SELECT platform.apply_scope_rls('orders.refund_batch'::regclass);
SELECT platform.apply_scope_rls('orders.resale_eligibility_rule'::regclass);
SELECT platform.apply_scope_rls('orders.resale_fee_policy'::regclass);
SELECT platform.apply_scope_rls('orders.resale_listing'::regclass);
SELECT platform.apply_scope_rls('orders.resale_marketplace_config'::regclass);
SELECT platform.apply_scope_rls('orders.resale_recommendation'::regclass);
SELECT platform.apply_scope_rls('orders.resale_settlement'::regclass);
SELECT platform.apply_scope_rls('orders.reservation_hold_policy'::regclass);
SELECT platform.apply_scope_rls('orders.sales_order'::regclass);
SELECT platform.apply_scope_rls('orders.status_transition_rule'::regclass);
SELECT platform.apply_scope_rls('orders.stored_value_authorisation'::regclass);
SELECT platform.apply_scope_rls('orders.till_shift_policy'::regclass);
SELECT platform.apply_scope_rls('orders.upgrade_rule'::regclass);
SELECT platform.apply_scope_rls('orders.visit_reminder'::regclass);
SELECT platform.apply_scope_rls('orders.wallet_pass'::regclass);
SELECT platform.apply_scope_rls('payments.authentication_policy'::regclass);
SELECT platform.apply_scope_rls('payments.chargeback_evidence'::regclass);
SELECT platform.apply_scope_rls('payments.credit_account'::regclass);
SELECT platform.apply_scope_rls('payments.currency_rule'::regclass);
SELECT platform.apply_scope_rls('payments.dunning_case'::regclass);
SELECT platform.apply_scope_rls('payments.dunning_policy'::regclass);
SELECT platform.apply_scope_rls('payments.eligibility_rule'::regclass);
SELECT platform.apply_scope_rls('payments.failover_policy'::regclass);
SELECT platform.apply_scope_rls('payments.hosted_checkout'::regclass);
SELECT platform.apply_scope_rls('payments.instalment_plan'::regclass);
SELECT platform.apply_scope_rls('payments.instalment_policy'::regclass);
SELECT platform.apply_scope_rls('payments.matching_rules'::regclass);
SELECT platform.apply_scope_rls('payments.merchant_account'::regclass);
SELECT platform.apply_scope_rls('payments.method'::regclass);
SELECT platform.apply_scope_rls('payments.method_config'::regclass);
SELECT platform.apply_scope_rls('payments.mixed_tender_rules'::regclass);
SELECT platform.apply_scope_rls('payments.payment_attempt'::regclass);
SELECT platform.apply_scope_rls('payments.payment_terms'::regclass);
SELECT platform.apply_scope_rls('payments.provider'::regclass);
SELECT platform.apply_scope_rls('payments.provider_connection'::regclass);
SELECT platform.apply_scope_rls('payments.provider_cost'::regclass);
SELECT platform.apply_scope_rls('payments.provider_event'::regclass);
SELECT platform.apply_scope_rls('payments.reconciliation_source'::regclass);
SELECT platform.apply_scope_rls('payments.risk_rules'::regclass);
SELECT platform.apply_scope_rls('payments.routing_rule'::regclass);
SELECT platform.apply_scope_rls('payments.stored_forward'::regclass);
SELECT platform.apply_scope_rls('payments.terminal'::regclass);
SELECT platform.apply_scope_rls('payments.terminal_certification'::regclass);
SELECT platform.apply_scope_rls('pii.consent_identifier'::regclass);
SELECT platform.apply_scope_rls('platform.configuration_profile'::regclass);
SELECT platform.apply_scope_rls('platform.connectivity_policy'::regclass);
SELECT platform.apply_scope_rls('platform.dead_letter'::regclass);
SELECT platform.apply_scope_rls('platform.idempotency_record'::regclass);
SELECT platform.apply_scope_rls('platform.offline_policy'::regclass);
SELECT platform.apply_scope_rls('platform.outbox'::regclass);
SELECT platform.apply_scope_rls('platform.workstation'::regclass);
SELECT platform.apply_scope_rls('pricing.dynamic_price_rule'::regclass);
SELECT platform.apply_scope_rls('promotions.coupon_code'::regclass);
SELECT platform.apply_scope_rls('promotions.product_relationship'::regclass);
SELECT platform.apply_scope_rls('promotions.recommendation_experiment'::regclass);
SELECT platform.apply_scope_rls('promotions.recommendation_outcome'::regclass);
SELECT platform.apply_scope_rls('promotions.recommendation_strategy'::regclass);
SELECT platform.apply_scope_rls('promotions.recommendation_suppression'::regclass);
SELECT platform.apply_scope_rls('rental.agreement_rules'::regclass);
SELECT platform.apply_scope_rls('rental.agreement_signature'::regclass);
SELECT platform.apply_scope_rls('rental.availability_rules'::regclass);
SELECT platform.apply_scope_rls('rental.blackout'::regclass);
SELECT platform.apply_scope_rls('rental.booking'::regclass);
SELECT platform.apply_scope_rls('rental.damage_assessment'::regclass);
SELECT platform.apply_scope_rls('rental.deposit_policy'::regclass);
SELECT platform.apply_scope_rls('rental.duration_rules'::regclass);
SELECT platform.apply_scope_rls('rental.equipment_assignment'::regclass);
SELECT platform.apply_scope_rls('rental.fee_policy'::regclass);
SELECT platform.apply_scope_rls('rental.incident'::regclass);
SELECT platform.apply_scope_rls('rental.inspection'::regclass);
SELECT platform.apply_scope_rls('rental.inventory_model'::regclass);
SELECT platform.apply_scope_rls('rental.location_rule'::regclass);
SELECT platform.apply_scope_rls('rental.operational_rules'::regclass);
SELECT platform.apply_scope_rls('rental.override'::regclass);
SELECT platform.apply_scope_rls('rental.pricing_profile'::regclass);
SELECT platform.apply_scope_rls('rental.product'::regclass);
SELECT platform.apply_scope_rls('rental.quote'::regclass);
SELECT platform.apply_scope_rls('rental.settlement'::regclass);
SELECT platform.apply_scope_rls('reporting.alert'::regclass);
SELECT platform.apply_scope_rls('reporting.alert_rule'::regclass);
SELECT platform.apply_scope_rls('reporting.analytics_governance_policy'::regclass);
SELECT platform.apply_scope_rls('reporting.anomaly'::regclass);
SELECT platform.apply_scope_rls('reporting.delivery'::regclass);
SELECT platform.apply_scope_rls('reporting.kpi_definition'::regclass);
SELECT platform.apply_scope_rls('reporting.kpi_target'::regclass);
SELECT platform.apply_scope_rls('reporting.natural_language_query'::regclass);
SELECT platform.apply_scope_rls('reporting.pipeline'::regclass);
SELECT platform.apply_scope_rls('reporting.report_definition'::regclass);
SELECT platform.apply_scope_rls('reporting.report_definition_version'::regclass);
SELECT platform.apply_scope_rls('reporting.semantic_model'::regclass);
SELECT platform.apply_scope_rls('reporting.site_normalisation_basis'::regclass);
SELECT platform.apply_scope_rls('reporting.subscription'::regclass);
SELECT platform.apply_scope_rls('resources.allocation_policy'::regclass);
SELECT platform.apply_scope_rls('resources.attribute_definition'::regclass);
SELECT platform.apply_scope_rls('resources.qualification'::regclass);
SELECT platform.apply_scope_rls('resources.resource'::regclass);
SELECT platform.apply_scope_rls('resources.resource_audit'::regclass);
SELECT platform.apply_scope_rls('resources.resource_block'::regclass);
SELECT platform.apply_scope_rls('resources.resource_category'::regclass);
SELECT platform.apply_scope_rls('resources.resource_cost'::regclass);
SELECT platform.apply_scope_rls('resources.resource_dependency'::regclass);
SELECT platform.apply_scope_rls('resources.resource_hold'::regclass);
SELECT platform.apply_scope_rls('resources.resource_package'::regclass);
SELECT platform.apply_scope_rls('resources.resource_relation'::regclass);
SELECT platform.apply_scope_rls('resources.resource_request'::regclass);
SELECT platform.apply_scope_rls('resources.resource_requirement'::regclass);
SELECT platform.apply_scope_rls('resources.resource_schedule'::regclass);
SELECT platform.apply_scope_rls('resources.resource_type'::regclass);
SELECT platform.apply_scope_rls('resources.selection_policy'::regclass);
SELECT platform.apply_scope_rls('resources.venue_assignment'::regclass);
SELECT platform.apply_scope_rls('retail.product_recommendation'::regclass);
SELECT platform.apply_scope_rls('seating.accessible'::regclass);
SELECT platform.apply_scope_rls('seating.group_request'::regclass);
SELECT platform.apply_scope_rls('seating.group_request_participant'::regclass);
SELECT platform.apply_scope_rls('seating.hold_pool'::regclass);
SELECT platform.apply_scope_rls('seating.hold_type'::regclass);
SELECT platform.apply_scope_rls('seating.reassignment'::regclass);
SELECT platform.apply_scope_rls('seating.recommendation_rules'::regclass);
SELECT platform.apply_scope_rls('seating.seat_block'::regclass);
SELECT platform.apply_scope_rls('seating.seat_rules'::regclass);
SELECT platform.apply_scope_rls('seating.section'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_eligibility_rule'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_entitlement'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_household_policy'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_product'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_product_history'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_renewal_policy'::regclass);
SELECT platform.apply_scope_rls('subscription.membership_usage_policy'::regclass);
SELECT platform.apply_scope_rls('tenancy.data_retention_setting'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_assignment'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_audit'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_credential'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_firmware'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_rollout'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_tamper_event'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_telemetry'::regclass);
SELECT platform.apply_scope_rls('venuemap.map'::regclass);
SELECT platform.apply_scope_rls('venuemap.visit_plan'::regclass);
SELECT platform.apply_scope_rls('wallet.accounting_mapping'::regclass);
SELECT platform.apply_scope_rls('wallet.adjustment'::regclass);
SELECT platform.apply_scope_rls('wallet.authentication_policy'::regclass);
SELECT platform.apply_scope_rls('wallet.auto_reload_setting'::regclass);
SELECT platform.apply_scope_rls('wallet.channel_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.configuration_version'::regclass);
SELECT platform.apply_scope_rls('wallet.configuration_version_snapshot'::regclass);
SELECT platform.apply_scope_rls('wallet.consumption_policy'::regclass);
SELECT platform.apply_scope_rls('wallet.credential'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_eligibility'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_lot'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_type'::regclass);
SELECT platform.apply_scope_rls('wallet.dispute'::regclass);
SELECT platform.apply_scope_rls('wallet.exit_settlement'::regclass);
SELECT platform.apply_scope_rls('wallet.funding_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.gift_card_product'::regclass);
SELECT platform.apply_scope_rls('wallet.integration_mapping'::regclass);
SELECT platform.apply_scope_rls('wallet.reconciliation_source'::regclass);
SELECT platform.apply_scope_rls('wallet.refund_policy'::regclass);
SELECT platform.apply_scope_rls('wallet.restriction'::regclass);
SELECT platform.apply_scope_rls('wallet.risk_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.shared_wallet'::regclass);
SELECT platform.apply_scope_rls('wallet.transfer_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.voucher_type'::regclass);
SELECT platform.apply_scope_rls('wallet.wallet_type'::regclass);
SELECT platform.apply_scope_rls('whitelabel.analytics_provider'::regclass);
SELECT platform.apply_scope_rls('whitelabel.app_build'::regclass);
SELECT platform.apply_scope_rls('whitelabel.booking_flow'::regclass);
SELECT platform.apply_scope_rls('whitelabel.config_version'::regclass);
SELECT platform.apply_scope_rls('whitelabel.content_page'::regclass);
SELECT platform.apply_scope_rls('whitelabel.faq_category'::regclass);
SELECT platform.apply_scope_rls('whitelabel.footer_config'::regclass);
SELECT platform.apply_scope_rls('whitelabel.policy'::regclass);
SELECT platform.apply_scope_rls('whitelabel.promo_block'::regclass);
SELECT platform.apply_scope_rls('whitelabel.publish_review_policy'::regclass);
SELECT platform.apply_scope_rls('whitelabel.site_package'::regclass);
SELECT platform.apply_scope_rls('whitelabel.site_setup_progress'::regclass);
SELECT platform.apply_scope_rls('whitelabel.store_account'::regclass);
SELECT platform.apply_scope_rls('workforce.field_ownership'::regclass);
SELECT platform.apply_scope_rls('workforce.forecast_requirement'::regclass);
SELECT platform.apply_scope_rls('workforce.integration_source'::regclass);
SELECT platform.apply_scope_rls('workforce.labour_budget'::regclass);
SELECT platform.apply_scope_rls('workforce.leave_request'::regclass);
SELECT platform.apply_scope_rls('workforce.open_shift'::regclass);
SELECT platform.apply_scope_rls('workforce.shift_template'::regclass);
SELECT platform.apply_scope_rls('workforce.staff_conversation'::regclass);
SELECT platform.apply_scope_rls('workforce.staffing_rules'::regclass);
SELECT platform.apply_scope_rls('workforce.sync_conflict'::regclass);
SELECT platform.apply_scope_rls('workforce.sync_run'::regclass);
SELECT platform.apply_scope_rls('workforce.work_assignment'::regclass);

-- Scoped by either of two paths: owned at scope_path, shared with a second scope (audit R183).
SELECT platform.apply_shared_scope_rls('inventory.transfer'::regclass, 'to_scope_path');

-- Scoped by venue, resolved through the scope tree.
SELECT platform.apply_venue_rls('access.parking_facility'::regclass);
SELECT platform.apply_venue_rls('assets.media_asset'::regclass);
SELECT platform.apply_venue_rls('assets.media_collection'::regclass);
SELECT platform.apply_venue_rls('assets.media_upload'::regclass);
SELECT platform.apply_venue_rls('catalogue.change_request_line'::regclass);
SELECT platform.apply_venue_rls('catalogue.donation_campaign'::regclass);
SELECT platform.apply_venue_rls('catalogue.price_list'::regclass);
SELECT platform.apply_venue_rls('catalogue.published_bundle'::regclass);
SELECT platform.apply_venue_rls('fnb.delivery_location'::regclass);
SELECT platform.apply_venue_rls('fnb.location_session'::regclass);
SELECT platform.apply_venue_rls('games.card'::regclass);
SELECT platform.apply_venue_rls('games.game'::regclass);
SELECT platform.apply_venue_rls('games.prize'::regclass);
SELECT platform.apply_venue_rls('games.redemption'::regclass);
SELECT platform.apply_venue_rls('identity."session"'::regclass);
SELECT platform.apply_venue_rls('inventory.item'::regclass);
SELECT platform.apply_venue_rls('inventory.location'::regclass);
SELECT platform.apply_venue_rls('inventory.requisition'::regclass);
SELECT platform.apply_venue_rls('ledger.account_mapping'::regclass);
SELECT platform.apply_venue_rls('ledger.cost_center'::regclass);
SELECT platform.apply_venue_rls('ledger.journal_line'::regclass);
SELECT platform.apply_venue_rls('ledger.posting'::regclass);
SELECT platform.apply_venue_rls('ledger.price_variance'::regclass);
SELECT platform.apply_venue_rls('maintenance.asset'::regclass);
SELECT platform.apply_venue_rls('maintenance.incident'::regclass);
SELECT platform.apply_venue_rls('maintenance.inspection'::regclass);
SELECT platform.apply_venue_rls('maintenance.inspection_template'::regclass);
SELECT platform.apply_venue_rls('maintenance.priority_scoring_model'::regclass);
SELECT platform.apply_venue_rls('maintenance.vendor_service_request'::regclass);
SELECT platform.apply_venue_rls('maintenance.work_order'::regclass);
SELECT platform.apply_venue_rls('marketing.campaign'::regclass);
SELECT platform.apply_venue_rls('marketing."case"'::regclass);
SELECT platform.apply_venue_rls('marketing.conversation'::regclass);
SELECT platform.apply_venue_rls('marketing.kiosk_assist_session'::regclass);
SELECT platform.apply_venue_rls('marketing.lost_item'::regclass);
SELECT platform.apply_venue_rls('marketing.loyalty_programme'::regclass);
SELECT platform.apply_venue_rls('marketing.review'::regclass);
SELECT platform.apply_venue_rls('marketing.segment'::regclass);
SELECT platform.apply_venue_rls('orders.cart'::regclass);
SELECT platform.apply_venue_rls('orders.deposit_box'::regclass);
SELECT platform.apply_venue_rls('orders.order_line'::regclass);
SELECT platform.apply_venue_rls('orders.refund_policy'::regclass);
SELECT platform.apply_venue_rls('orders.reservation'::regclass);
SELECT platform.apply_venue_rls('platform.cross_region_entitlement'::regclass);
SELECT platform.apply_venue_rls('platform.outlet'::regclass);
SELECT platform.apply_venue_rls('platform.sale_board'::regclass);
SELECT platform.apply_venue_rls('platform.venue_settings'::regclass);
SELECT platform.apply_venue_rls('promotions.allocation_component'::regclass);
SELECT platform.apply_venue_rls('promotions.bundle'::regclass);
SELECT platform.apply_venue_rls('promotions.bundle_capacity_policy'::regclass);
SELECT platform.apply_venue_rls('promotions.bundle_component'::regclass);
SELECT platform.apply_venue_rls('promotions.campaign'::regclass);
SELECT platform.apply_venue_rls('promotions.coupon_campaign'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_alert'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_audit'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_channel_publication'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_conflict'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_evaluation_trace'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion_rule'::regclass);
SELECT platform.apply_venue_rls('promotions.stacking_rule'::regclass);
SELECT platform.apply_venue_rls('promotions.voucher_batch'::regclass);
SELECT platform.apply_venue_rls('queue.queue'::regclass);
SELECT platform.apply_venue_rls('rental.agreement'::regclass);
SELECT platform.apply_venue_rls('reporting.dashboard'::regclass);
SELECT platform.apply_venue_rls('reporting.dashboard_view'::regclass);
SELECT platform.apply_venue_rls('retail.shop_and_drop'::regclass);
SELECT platform.apply_venue_rls('retail.store_rule'::regclass);
SELECT platform.apply_venue_rls('seating.seat_category'::regclass);
SELECT platform.apply_venue_rls('seating.seat_map'::regclass);
SELECT platform.apply_venue_rls('transport.favourite_route'::regclass);
SELECT platform.apply_venue_rls('transport.network_import'::regclass);
SELECT platform.apply_venue_rls('transport.pass_type'::regclass);
SELECT platform.apply_venue_rls('transport.route'::regclass);
SELECT platform.apply_venue_rls('transport.station'::regclass);
SELECT platform.apply_venue_rls('wallet.wallet_transaction'::regclass);
SELECT platform.apply_venue_rls('whitelabel.guided_choice'::regclass);
SELECT platform.apply_venue_rls('workforce.announcement'::regclass);
SELECT platform.apply_venue_rls('workforce.attendance'::regclass);
SELECT platform.apply_venue_rls('workforce.position_requirement'::regclass);
SELECT platform.apply_venue_rls('workforce.rota_assignment'::regclass);

-- Scoped through the parent that owns the row (a NOT NULL declared foreign key).
SELECT platform.apply_parent_rls('access.entry_rule_point'::regclass, 'admission_profile_id', 'access.admission_rules'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.action_step'::regclass, 'plan_id', 'ai.action_plan'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.blueprint_decision'::regclass, 'blueprint_id', 'ai.blueprint'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.case_action'::regclass, 'case_id', 'ai.risk_case'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.case_evidence'::regclass, 'case_id', 'ai.risk_case'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.chunk_embedding'::regclass, 'document_id', 'ai.knowledge_document'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.index_source'::regclass, 'collection_id', 'ai.knowledge_collection'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.message'::regclass, 'conversation_id', 'ai.conversation'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.decision'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.decision_table_row'::regclass, 'decision_table_id', 'approvals.decision_table'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.escalation'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.rule'::regclass, 'matrix_id', 'approvals.matrix'::regclass, 'id');
SELECT platform.apply_parent_rls('assets.media_usage'::regclass, 'asset_id', 'assets.media_asset'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.calculation_step'::regclass, 'calculation_profile_id', 'catalogue.calculation_profile'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.performance'::regclass, 'event_id', 'catalogue.event'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.price'::regclass, 'price_list_id', 'catalogue.price_list'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.pricing_publication_target'::regclass, 'pricing_publication_id', 'catalogue.pricing_publication'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.variant'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.variant_dimension'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.kitchen_ticket'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.modifier_option'::regclass, 'modifier_group_id', 'fnb.modifier_group'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.recipe_ingredient'::regclass, 'inventory_item_id', 'inventory.item'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.service_order'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.table_reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.table_session'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.table_visit'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.waitlist_entry'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('games.credit_ledger'::regclass, 'card_id', 'games.card'::regclass, 'card_code');
SELECT platform.apply_parent_rls('games.redemption_line'::regclass, 'redemption_id', 'games.redemption'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.goods_receipt'::regclass, 'purchase_order_id', 'inventory.purchase_order'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.movement'::regclass, 'item_id', 'inventory.item'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.purchase_order_line'::regclass, 'purchase_order_id', 'inventory.purchase_order'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.requisition_line'::regclass, 'requisition_id', 'inventory.requisition'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.transfer_line'::regclass, 'transfer_id', 'inventory.transfer'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.account'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.credit_memo_line'::regclass, 'credit_memo_id', 'ledger.credit_memo'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.event_budget'::regclass, 'event_id', 'catalogue.event'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.fiscal_period'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.fx_rate'::regclass, 'region_id', 'platform.scope'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.settlement_exception'::regclass, 'settlement_id', 'ledger.settlement'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.tax_invoice_line'::regclass, 'tax_invoice_id', 'ledger.tax_invoice'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.inspection_item'::regclass, 'inspection_id', 'maintenance.inspection'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.inspection_template_item'::regclass, 'inspection_template_id', 'maintenance.inspection_template'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.preventive_plan'::regclass, 'asset_id', 'maintenance.asset'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.work_order_attachment'::regclass, 'work_order_id', 'maintenance.work_order'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.attribution_touch'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.challenge_progress'::regclass, 'challenge_id', 'marketing.challenge'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.conversation_message'::regclass, 'conversation_id', 'marketing.conversation'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.device_consent_category'::regclass, 'device_consent_id', 'marketing.device_consent'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.guest_profile'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.journey_step'::regclass, 'journey_id', 'marketing.journey'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.loyalty_position'::regclass, 'programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.message_delivery'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.points_earning_rule'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.privacy_request_deadline'::regclass, 'privacy_request_type_id', 'marketing.privacy_request_type'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.programme_tier'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.segment_criterion'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.waiver_field_rule'::regclass, 'form_definition_field_id', 'marketing.form_definition_field'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.after_sale_policy_window'::regclass, 'after_sale_policy_id', 'orders.after_sale_policy'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cash_count_line'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cash_movement'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.credit_override'::regclass, 'b2b_credit_id', 'orders.b2b_credit'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit_box_foreign_holding'::regclass, 'deposit_box_id', 'orders.deposit_box'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit_box_opening_denomination'::regclass, 'deposit_box_id', 'orders.deposit_box'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.discount'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.group_booking'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.group_quote_line'::regclass, 'group_quote_id', 'orders.group_quote'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.invitation'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.no_sale_event'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_fee'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_line_discount'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_line_eligibility'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.payment'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.pos_shift_approval'::regclass, 'pos_shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.pos_shift_incident'::regclass, 'pos_shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.refund'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.refund_policy_time_band'::regclass, 'refund_policy_id', 'orders.refund_policy'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.reservation_line'::regclass, 'reservation_id', 'orders.reservation'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.upgrade'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('payments.instalment'::regclass, 'instalment_plan_id', 'payments.instalment_plan'::regclass, 'id');
SELECT platform.apply_parent_rls('payments.terminal_certification_level3'::regclass, 'terminal_certification_id', 'payments.terminal_certification'::regclass, 'id');
SELECT platform.apply_parent_rls('pii.subject_biometric'::regclass, 'entitlement_id', 'access.entitlement'::regclass, 'id');
SELECT platform.apply_parent_rls('platform.dsar_request'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('platform.sale_board_page'::regclass, 'sale_board_id', 'platform.sale_board'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.allocation_split'::regclass, 'bundle_id', 'promotions.bundle'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.bundle_choice_group'::regclass, 'bundle_id', 'promotions.bundle'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.campaign_budget'::regclass, 'campaign_id', 'promotions.campaign'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.voucher'::regclass, 'batch_id', 'promotions.voucher_batch'::regclass, 'id');
SELECT platform.apply_parent_rls('queue.entry'::regclass, 'queue_id', 'queue.queue'::regclass, 'id');
SELECT platform.apply_parent_rls('queue.feed'::regclass, 'queue_id', 'queue.queue'::regclass, 'id');
SELECT platform.apply_parent_rls('queue.queue_operating_window'::regclass, 'queue_id', 'queue.queue'::regclass, 'id');
SELECT platform.apply_parent_rls('queue.reading'::regclass, 'queue_id', 'queue.queue'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.execution'::regclass, 'report_id', 'reporting.report_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.report_column'::regclass, 'report_definition_id', 'reporting.report_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.report_filter'::regclass, 'report_definition_id', 'reporting.report_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.report_parameter'::regclass, 'definition_id', 'reporting.report_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.schedule'::regclass, 'report_id', 'reporting.report_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('resources.booking'::regclass, 'resource_id', 'resources.resource'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.merchandise'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.reservation'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.return_policy'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.shop_and_drop_line'::regclass, 'shop_and_drop_id', 'retail.shop_and_drop'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.import_job'::regclass, 'seat_map_id', 'seating.seat_map'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.seat_map_template'::regclass, 'region_id', 'platform.scope'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.seating_rules'::regclass, 'seat_map_id', 'seating.seat_map'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.section_row'::regclass, 'section_id', 'seating.section'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.zone'::regclass, 'seat_map_id', 'seating.seat_map'::regclass, 'id');
SELECT platform.apply_parent_rls('sync.rejection'::regclass, 'workstation_id', 'platform.workstation'::regclass, 'id');
SELECT platform.apply_parent_rls('transport.route_stop'::regclass, 'route_id', 'transport.route'::regclass, 'id');
SELECT platform.apply_parent_rls('venuemap.path'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');
SELECT platform.apply_parent_rls('venuemap.placed_resource'::regclass, 'resource_id', 'resources.resource'::regclass, 'id');
SELECT platform.apply_parent_rls('venuemap.point'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');
SELECT platform.apply_parent_rls('venuemap.visit_plan_item'::regclass, 'plan_id', 'venuemap.visit_plan'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.faq_entry'::regclass, 'faq_category_id', 'whitelabel.faq_category'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.footer_config_column'::regclass, 'footer_config_id', 'whitelabel.footer_config'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.footer_config_social_link'::regclass, 'footer_config_id', 'whitelabel.footer_config'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.guided_choice_answer'::regclass, 'guided_choice_id', 'whitelabel.guided_choice'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.guided_choice_question'::regclass, 'guided_choice_id', 'whitelabel.guided_choice'::regclass, 'id');
SELECT platform.apply_parent_rls('workforce.announcement_receipt'::regclass, 'announcement_id', 'workforce.announcement'::regclass, 'id');
SELECT platform.apply_parent_rls('workforce.shift_swap'::regclass, 'assignment_id', 'workforce.rota_assignment'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.index_entry'::regclass, 'source_id', 'ai.index_source'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.index_job'::regclass, 'source_id', 'ai.index_source'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.channel_capacity'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.waitlist_entry'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.bill_split'::regclass, 'visit_id', 'fnb.table_visit'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.kitchen_ticket_line'::regclass, 'kitchen_ticket_id', 'fnb.kitchen_ticket'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.menu_item'::regclass, 'product_variant_id', 'catalogue.variant'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.menu_section'::regclass, 'menu_id', 'fnb.menu'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.service_order_line'::regclass, 'service_order_id', 'fnb.service_order'::regclass, 'id');
SELECT platform.apply_parent_rls('inventory.goods_receipt_line'::regclass, 'goods_receipt_id', 'inventory.goods_receipt'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.fiscal_period_event'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.journal_entry'::regclass, 'fiscal_period_id', 'ledger.fiscal_period'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.conversation_message_attachment'::regclass, 'conversation_message_id', 'marketing.conversation_message'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.chargeback'::regclass, 'payment_id', 'orders.payment'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.payment_tip'::regclass, 'payment_id', 'orders.payment'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.bundle_choice_option'::regclass, 'bundle_choice_group_id', 'promotions.bundle_choice_group'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.export'::regclass, 'execution_id', 'reporting.execution'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.schedule_recipient'::regclass, 'schedule_id', 'reporting.schedule'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.reservation_line'::regclass, 'reservation_id', 'retail.reservation'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.seat_hold'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.channel_allocation'::regclass, 'envelope_id', 'catalogue.channel_capacity'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.inventory_hold'::regclass, 'channel_capacity_id', 'catalogue.channel_capacity'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.recipe'::regclass, 'menu_item_id', 'fnb.menu_item'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.sub_bill'::regclass, 'bill_split_id', 'fnb.bill_split'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.chargeback_evidence'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.chargeback_investigation_log'::regclass, 'chargeback_id', 'orders.chargeback'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.production_run'::regclass, 'recipe_id', 'fnb.recipe'::regclass, 'id');

-- By subject (SD-015): the session's own subject, or the tenant root.
SELECT platform.apply_subject_rls('access.parking_entitlement'::regclass);
SELECT platform.apply_subject_rls('identity.guest_identity_verification'::regclass);
SELECT platform.apply_subject_rls('identity.otp_challenge'::regclass);
SELECT platform.apply_subject_rls('ledger.deposit'::regclass);
SELECT platform.apply_subject_rls('maintenance.incident_involved_party'::regclass);
SELECT platform.apply_subject_rls('marketing.communication_policy_decision'::regclass);
SELECT platform.apply_subject_rls('marketing.consent_record'::regclass);
SELECT platform.apply_subject_rls('marketing.form_submission'::regclass);
SELECT platform.apply_subject_rls('marketing.guest_device'::regclass);
SELECT platform.apply_subject_rls('marketing.guest_document'::regclass);
SELECT platform.apply_subject_rls('marketing.guest_note'::regclass);
SELECT platform.apply_subject_rls('marketing.guest_preference'::regclass);
SELECT platform.apply_subject_rls('marketing.message_dispatch'::regclass);
SELECT platform.apply_subject_rls('marketing.privacy_audit_event'::regclass);
SELECT platform.apply_subject_rls('marketing.subscription'::regclass);
SELECT platform.apply_subject_rls('marketing.touch_point'::regclass);
SELECT platform.apply_subject_rls('marketing.wishlist_item'::regclass);
SELECT platform.apply_subject_rls('orders.guest_credit_account'::regclass);
SELECT platform.apply_subject_rls('orders.membership_activation_action'::regclass);
SELECT platform.apply_subject_rls('payments.token'::regclass);
SELECT platform.apply_subject_rls('pii.subject_contact'::regclass);
SELECT platform.apply_subject_rls('pii.subject_document'::regclass);
SELECT platform.apply_subject_rls('platform.audit_read'::regclass);
SELECT platform.apply_subject_rls('resources.performance_participant'::regclass);
SELECT platform.apply_subject_rls('retail.sale'::regclass);
SELECT platform.apply_subject_rls('wallet.gift_card'::regclass);
SELECT platform.apply_subject_rls('wallet.shared_wallet_member'::regclass);
SELECT platform.apply_subject_rls('wallet.wallet'::regclass);

-- Tenant root only (SD-015): no scope column and no protected owner, so visible only
-- to a connection holding the tenant root. `pii.*` and `payments.token` are also
-- reached only through their owning service's role; this policy is the floor.
SELECT platform.apply_tenant_rls('access.access_change'::regclass);  -- was: only nullable references (order_id -> orders.sales_order)
SELECT platform.apply_tenant_rls('ai.config_source'::regclass);  -- was: several protected owners (session_id -> ai.config_session, asset_id -> assets.media_asset); which one owns the row is not decided
SELECT platform.apply_tenant_rls('ai.inbox'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('approvals.accreditation_badge'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('approvals.step_up_policy'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('assets.media_collection_member'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('catalogue.alternative_code'::regclass);  -- was: only nullable references (variant_id -> catalogue.variant, product_id -> catalogue.product)
SELECT platform.apply_tenant_rls('catalogue.membership_benefit'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('catalogue.membership_programme'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('catalogue.plan_benefit'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('catalogue.product_media'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('catalogue.product_version'::regclass);  -- was: only nullable references (product_id -> catalogue.product)
SELECT platform.apply_tenant_rls('fnb.allergen_verdict'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.cold_chain_event'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.combo'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.combo_slot'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.delivery_location_outlet'::regclass);  -- was: only nullable references (location_id -> fnb.delivery_location, outlet_id -> platform.outlet)
SELECT platform.apply_tenant_rls('fnb.dining_table'::regclass);  -- was: only nullable references (outlet_id -> platform.outlet)
SELECT platform.apply_tenant_rls('fnb.ingredient_substitute'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.kitchen_exception'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.kitchen_sla'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.kitchen_station'::regclass);  -- was: only nullable references (outlet_id -> platform.outlet)
SELECT platform.apply_tenant_rls('fnb.menu_item_modifier'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.production_plan'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.production_plan_line'::regclass);  -- was: its owner fnb.production_plan has no policy either
SELECT platform.apply_tenant_rls('fnb.reservation_table'::regclass);  -- was: its owner fnb.dining_table has no policy either
SELECT platform.apply_tenant_rls('fnb.sold_out_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.substitution_rule'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('fnb.temperature_log'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('games.play'::regclass);  -- was: only nullable references (game_id -> games.game)
SELECT platform.apply_tenant_rls('games.reader_deployment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.authz_audit'::regclass);  -- was: only nullable references (actor_principal_id -> identity.principal, subject_principal_id -> identity.principal)
SELECT platform.apply_tenant_rls('identity.benefit_usage'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.customer_membership'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.membership_history'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.mfa_challenge'::regclass);  -- was: its owner identity.principal has no policy either
SELECT platform.apply_tenant_rls('identity.mfa_method'::regclass);  -- was: only nullable references (principal_id -> identity.principal)
SELECT platform.apply_tenant_rls('identity.mfa_recovery_code'::regclass);  -- was: only nullable references (principal_id -> identity.principal)
SELECT platform.apply_tenant_rls('identity.module'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.permission'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.principal'::regclass);  -- was: only nullable references (primary_role_id -> identity.role, home_scope_id -> platform.scope)
SELECT platform.apply_tenant_rls('identity.principal_credential'::regclass);  -- was: only nullable references (principal_id -> identity.principal)
SELECT platform.apply_tenant_rls('identity.refresh_token'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.role'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('identity.role_permission'::regclass);  -- was: its owner identity.role has no policy either
SELECT platform.apply_tenant_rls('inventory.count'::regclass);  -- was: only nullable references (started_by_principal_id -> identity.principal, posted_by_principal_id -> identity.principal, journal_entry_id -> ledger.journal_entry)
SELECT platform.apply_tenant_rls('inventory.count_line'::regclass);  -- was: its owner inventory.count has no policy either
SELECT platform.apply_tenant_rls('inventory.quotation_line'::regclass);  -- was: several protected owners (quotation_id -> inventory.quotation, item_id -> inventory.item); which one owns the row is not decided
SELECT platform.apply_tenant_rls('inventory.serialised_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('inventory.stock_batch'::regclass);  -- was: several protected owners (item_id -> inventory.item, location_id -> inventory.location); which one owns the row is not decided
SELECT platform.apply_tenant_rls('inventory.stock_reservation'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('inventory.supplier_contract'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('kernel.inbox'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('ledger.inter_entity_obligation'::regclass);  -- was: only nullable references (entitlement_id -> access.entitlement, order_id -> orders.sales_order)
SELECT platform.apply_tenant_rls('ledger.recognition_schedule'::regclass);  -- was: only nullable references (deferred_account_id -> ledger.account, recognised_account_id -> ledger.account, breakage_account_id -> ledger.account)
SELECT platform.apply_tenant_rls('ledger.tax_code'::regclass);  -- was: only nullable references (account_id -> ledger.account)
SELECT platform.apply_tenant_rls('ledger.tax_exemption'::regclass);  -- was: its owner ledger.tax_code has no policy either
SELECT platform.apply_tenant_rls('maintenance.asset_document'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('maintenance.asset_status_change'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('maintenance.incident_authority_notification'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('maintenance.incident_investigation_note'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('maintenance.incident_media'::regclass);  -- was: only nullable references (asset_ref -> assets.media_asset)
SELECT platform.apply_tenant_rls('marketing.agent_availability'::regclass);  -- was: its owner identity.principal has no policy either
SELECT platform.apply_tenant_rls('marketing.badge'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.campaign_target'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.case_message'::regclass);  -- was: only nullable references (author_principal_id -> identity.principal, case_id -> marketing.case)
SELECT platform.apply_tenant_rls('marketing.consent_propagation'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.consent_purpose'::regclass);  -- was: its owner platform.tenant has no policy either
SELECT platform.apply_tenant_rls('marketing.consent_purpose_channel'::regclass);  -- was: its owner marketing.consent_purpose has no policy either
SELECT platform.apply_tenant_rls('marketing.consent_question_version'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.consent_record_channel'::regclass);  -- was: its owner marketing.consent_record has no policy either
SELECT platform.apply_tenant_rls('marketing.customer_badge'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.guest_extra_field'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.guest_extra_option'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.guest_extra_value'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.loyalty_campaign'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.loyalty_points'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.loyalty_rule'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.message_dispatch_attempt'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.message_template'::regclass);  -- was: its owner platform.tenant has no policy either
SELECT platform.apply_tenant_rls('marketing.message_template_version'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.points_redemption_rule'::regclass);  -- was: only nullable references (product_id -> catalogue.product)
SELECT platform.apply_tenant_rls('marketing.retention_run'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.review_response'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.reward'::regclass);  -- was: only nullable references (product_id -> catalogue.product)
SELECT platform.apply_tenant_rls('marketing.reward_assignment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('marketing.waiver_signature'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.group_customer_organization'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.group_customer_organization_contact'::regclass);  -- was: its owner orders.group_customer_organization has no policy either
SELECT platform.apply_tenant_rls('orders.group_enquiry'::regclass);  -- was: only nullable references (organisation_id -> orders.group_customer_organization)
SELECT platform.apply_tenant_rls('orders.group_participant'::regclass);  -- was: its owner orders.group_participant_list has no policy either
SELECT platform.apply_tenant_rls('orders.group_participant_list'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.group_payment_milestone'::regclass);  -- was: its owner orders.group_payment_schedule has no policy either
SELECT platform.apply_tenant_rls('orders.group_payment_schedule'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.group_ticket_allocation'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.group_ticket_allocation_line'::regclass);  -- was: its owner orders.group_ticket_allocation has no policy either
SELECT platform.apply_tenant_rls('orders.group_ticket_fulfillment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.invitation_allowance'::regclass);  -- was: its owner identity.principal has no policy either
SELECT platform.apply_tenant_rls('orders.member_exception'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.membership_migration'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.membership_renewal'::regclass);  -- was: only nullable references (order_id -> orders.sales_order)
SELECT platform.apply_tenant_rls('orders.refund_calculation_policy'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.ticket_template'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('orders.ticket_template_channel'::regclass);  -- was: its owner orders.ticket_template has no policy either
SELECT platform.apply_tenant_rls('payments.deposit_activity'::regclass);  -- was: only nullable references (payment_id -> orders.payment)
SELECT platform.apply_tenant_rls('payments.fee_rule'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('pii.subject'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('platform.audit_record'::regclass);  -- was: only nullable references (principal_id -> identity.principal, org_unit_id -> platform.scope)
SELECT platform.apply_tenant_rls('platform.cell_endpoint'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('platform.denomination'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('platform.device'::regclass);  -- was: only nullable references (workstation_id -> platform.workstation)
SELECT platform.apply_tenant_rls('platform.device_heartbeat'::regclass);  -- was: only nullable references (device_id -> platform.device)
SELECT platform.apply_tenant_rls('platform.guest_link'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('platform.profile_deployment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('platform.region_settings'::regclass);  -- was: only nullable references (org_unit_id -> platform.scope)
SELECT platform.apply_tenant_rls('platform.sale_board_tile'::regclass);  -- was: only nullable references (page_id -> platform.sale_board_page)
SELECT platform.apply_tenant_rls('platform.tenant'::regclass);  -- was: only nullable references (home_region_id -> platform.scope)
SELECT platform.apply_tenant_rls('platform.wallet_authorisation'::regclass);  -- was: its owner platform.guest_link has no policy either
SELECT platform.apply_tenant_rls('pricing.dynamic_price_action'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('pricing.dynamic_price_condition'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('promotions.coupon_code_batch'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('promotions.partner_bundle_product'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('promotions.promotion_variant'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('promotions.upsell_rule'::regclass);  -- was: only nullable references (suggested_bundle_id -> promotions.bundle)
SELECT platform.apply_tenant_rls('rental.agreement_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('rental.inspection_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('rental.participant'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('reporting.dashboard_tile'::regclass);  -- was: several protected owners (dashboard_id -> reporting.dashboard, report_id -> reporting.report_definition); which one owns the row is not decided
SELECT platform.apply_tenant_rls('retail.exchange'::regclass);  -- was: its owners retail.return, retail.sale have no policy either
SELECT platform.apply_tenant_rls('retail."return"'::regclass);  -- was: its owner retail.sale has no policy either
SELECT platform.apply_tenant_rls('retail.return_line'::regclass);  -- was: its owner retail.return has no policy either
SELECT platform.apply_tenant_rls('retail.sale_line'::regclass);  -- was: its owner retail.sale has no policy either
SELECT platform.apply_tenant_rls('seating.seat'::regclass);  -- was: only nullable references (seat_map_id -> seating.seat_map)
SELECT platform.apply_tenant_rls('seating.seat_block_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('seating.seat_hold_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('seating.seat_price_band'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.capacity_pack'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.contract'::regclass);  -- was: its owners platform.tenant, subscription.plan have no policy either
SELECT platform.apply_tenant_rls('subscription.enforcement_policy'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.go_live_readiness'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.licensing_model'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.membership_household_policy_role_limit'::regclass);  -- was: only nullable references (membership_household_policy_id -> subscription.membership_household_policy)
SELECT platform.apply_tenant_rls('subscription.module_listing'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.partner_quote'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.plan'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.plan_limit'::regclass);  -- was: its owner subscription.plan has no policy either
SELECT platform.apply_tenant_rls('subscription.plan_module'::regclass);  -- was: its owner subscription.plan has no policy either
SELECT platform.apply_tenant_rls('subscription.tier_allowance'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.tier_module'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.trial_config'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.vsi_assessment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('subscription.vsi_model'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('sync.cell_connection'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('sync.cross_cell_request'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('transport.departure'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('transport.fare_matrix_cell'::regclass);  -- was: its owner transport.fare_table has no policy either
SELECT platform.apply_tenant_rls('transport.fare_passenger_type'::regclass);  -- was: its owner transport.fare_table has no policy either
SELECT platform.apply_tenant_rls('transport.fare_table'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('transport.timetable'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('transport.timetable_run'::regclass);  -- was: its owner transport.timetable has no policy either
SELECT platform.apply_tenant_rls('venuemap.import_job'::regclass);  -- was: only nullable references (map_id -> venuemap.map)
SELECT platform.apply_tenant_rls('venuemap.map_version'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('wallet.balance'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('wallet.hold'::regclass);  -- was: only nullable references (order_id -> orders.sales_order)
SELECT platform.apply_tenant_rls('whitelabel.banner'::regclass);  -- was: its owner whitelabel.tenant_config has no policy either
SELECT platform.apply_tenant_rls('whitelabel.booking_flow_step'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('whitelabel.custom_domain'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('whitelabel.feature_toggle'::regclass);  -- was: its owner whitelabel.tenant_config has no policy either
SELECT platform.apply_tenant_rls('whitelabel.homepage_section'::regclass);  -- was: only nullable references (content_page_id -> whitelabel.content_page)
SELECT platform.apply_tenant_rls('whitelabel.module_enablement'::regclass);  -- was: its owner whitelabel.tenant_config has no policy either
SELECT platform.apply_tenant_rls('whitelabel.navigation_item'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('whitelabel.tenant_config'::regclass);  -- was: its owner platform.tenant has no policy either
SELECT platform.apply_tenant_rls('workforce.attendance_amendment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.employee'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.employment'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.job_title'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.leave_balance'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.leave_type'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.shift'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.staff_conversation_participant'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.staff_message'::regclass);  -- was: no scope column and no declared owner
SELECT platform.apply_tenant_rls('workforce.training_record'::regclass);  -- was: no scope column and no declared owner
