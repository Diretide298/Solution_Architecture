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

-- **59 tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path`
-- alone leaves every one of them open.** `check-migrations` has said so since it was written --
-- checking only scope_path missed the tables that carry venue_id instead, and they would have
-- passed with no policy at all -- and the hand-written baseline never closed it because it
-- protected three tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on those 59 tables**, and
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

-- **630 tables: 267 scoped by `scope_path`, 59 by `venue_id`, 129 through the parent that owns them, 174 with no policy.**
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
SELECT platform.apply_scope_rls('access.access_point'::regclass);
SELECT platform.apply_scope_rls('access.admission_rules'::regclass);
SELECT platform.apply_scope_rls('access.blacklist'::regclass);
SELECT platform.apply_scope_rls('access.entitlement'::regclass);
SELECT platform.apply_scope_rls('access.scan_event'::regclass);
SELECT platform.apply_scope_rls('accreditation.access_profile'::regclass);
SELECT platform.apply_scope_rls('accreditation.application'::regclass);
SELECT platform.apply_scope_rls('accreditation.audit'::regclass);
SELECT platform.apply_scope_rls('accreditation.badge_template'::regclass);
SELECT platform.apply_scope_rls('accreditation.credential'::regclass);
SELECT platform.apply_scope_rls('accreditation.document'::regclass);
SELECT platform.apply_scope_rls('accreditation.holder'::regclass);
SELECT platform.apply_scope_rls('accreditation.holder_access'::regclass);
SELECT platform.apply_scope_rls('accreditation.notification_rules'::regclass);
SELECT platform.apply_scope_rls('accreditation.print_job'::regclass);
SELECT platform.apply_scope_rls('accreditation.programme'::regclass);
SELECT platform.apply_scope_rls('accreditation.requirements'::regclass);
SELECT platform.apply_scope_rls('accreditation.validity'::regclass);
SELECT platform.apply_scope_rls('ai.activity'::regclass);
SELECT platform.apply_scope_rls('ai.conversation'::regclass);
SELECT platform.apply_scope_rls('ai.knowledge_collection'::regclass);
SELECT platform.apply_scope_rls('ai.layout_draft'::regclass);
SELECT platform.apply_scope_rls('ai.policy'::regclass);
SELECT platform.apply_scope_rls('ai.provider'::regclass);
SELECT platform.apply_scope_rls('ai.suggestion'::regclass);
SELECT platform.apply_scope_rls('approvals.approver_availability'::regclass);
SELECT platform.apply_scope_rls('approvals.control_policy'::regclass);
SELECT platform.apply_scope_rls('approvals.decision_record'::regclass);
SELECT platform.apply_scope_rls('approvals.delegation'::regclass);
SELECT platform.apply_scope_rls('approvals.evidence_package'::regclass);
SELECT platform.apply_scope_rls('approvals.matrix'::regclass);
SELECT platform.apply_scope_rls('approvals.request'::regclass);
SELECT platform.apply_scope_rls('approvals.retention_policy'::regclass);
SELECT platform.apply_scope_rls('approvals.signature'::regclass);
SELECT platform.apply_scope_rls('approvals.sla_policy'::regclass);
SELECT platform.apply_scope_rls('assets.approval'::regclass);
SELECT platform.apply_scope_rls('assets.asset_version'::regclass);
SELECT platform.apply_scope_rls('assets.audit'::regclass);
SELECT platform.apply_scope_rls('assets.distribution_channel'::regclass);
SELECT platform.apply_scope_rls('assets.rendition'::regclass);
SELECT platform.apply_scope_rls('assets.share'::regclass);
SELECT platform.apply_scope_rls('assets.tag'::regclass);
SELECT platform.apply_scope_rls('assets.taxonomy'::regclass);
SELECT platform.apply_scope_rls('catalogue.entitlement_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.event'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_capacity_profile'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_registration'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_reschedule'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_resource_plan'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_schedule'::regclass);
SELECT platform.apply_scope_rls('catalogue.event_type'::regclass);
SELECT platform.apply_scope_rls('catalogue.group_package'::regclass);
SELECT platform.apply_scope_rls('catalogue.import_job'::regclass);
SELECT platform.apply_scope_rls('catalogue.performance_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.prepaid_minutes'::regclass);
SELECT platform.apply_scope_rls('catalogue.product'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_category'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_eligibility_rule'::regclass);
SELECT platform.apply_scope_rls('catalogue.space'::regclass);
SELECT platform.apply_scope_rls('fnb.corrective_action'::regclass);
SELECT platform.apply_scope_rls('fnb.course_rule'::regclass);
SELECT platform.apply_scope_rls('fnb.delivery_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.menu_schedule'::regclass);
SELECT platform.apply_scope_rls('fnb.menu_version'::regclass);
SELECT platform.apply_scope_rls('fnb.modifier_group'::regclass);
SELECT platform.apply_scope_rls('fnb.order_fulfilment'::regclass);
SELECT platform.apply_scope_rls('fnb.product_recommendation'::regclass);
SELECT platform.apply_scope_rls('fnb.reservation_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.service_charge_policy'::regclass);
SELECT platform.apply_scope_rls('fnb.table_combination'::regclass);
SELECT platform.apply_scope_rls('fnb.temperature_checkpoint'::regclass);
SELECT platform.apply_scope_rls('games.attraction_type'::regclass);
SELECT platform.apply_scope_rls('games.authorisation'::regclass);
SELECT platform.apply_scope_rls('games.card_expiry_rules'::regclass);
SELECT platform.apply_scope_rls('games.entitlement'::regclass);
SELECT platform.apply_scope_rls('games.gameplay_transaction'::regclass);
SELECT platform.apply_scope_rls('games.kiosk_config'::regclass);
SELECT platform.apply_scope_rls('games.operational_config'::regclass);
SELECT platform.apply_scope_rls('games.pricing'::regclass);
SELECT platform.apply_scope_rls('games.prize_cost'::regclass);
SELECT platform.apply_scope_rls('games.reader'::regclass);
SELECT platform.apply_scope_rls('games.reader_profile'::regclass);
SELECT platform.apply_scope_rls('games.redemption_rules'::regclass);
SELECT platform.apply_scope_rls('games.validation_rules'::regclass);
SELECT platform.apply_scope_rls('identity.access_decision'::regclass);
SELECT platform.apply_scope_rls('identity.access_override'::regclass);
SELECT platform.apply_scope_rls('identity.access_policy'::regclass);
SELECT platform.apply_scope_rls('identity.access_policy_version'::regclass);
SELECT platform.apply_scope_rls('identity.capability_template'::regclass);
SELECT platform.apply_scope_rls('identity.delegated_access'::regclass);
SELECT platform.apply_scope_rls('identity.module_access'::regclass);
SELECT platform.apply_scope_rls('identity.password_policy'::regclass);
SELECT platform.apply_scope_rls('identity.platform_staff_grant'::regclass);
SELECT platform.apply_scope_rls('identity.segregation_rule'::regclass);
SELECT platform.apply_scope_rls('identity.sso_group_mapping'::regclass);
SELECT platform.apply_scope_rls('identity.sso_provider'::regclass);
SELECT platform.apply_scope_rls('inventory.purchase_order'::regclass);
SELECT platform.apply_scope_rls('inventory.quotation'::regclass);
SELECT platform.apply_scope_rls('inventory.supplier'::regclass);
SELECT platform.apply_scope_rls('ledger.fx_provider_assignment'::regclass);
SELECT platform.apply_scope_rls('ledger.legal_entity'::regclass);
SELECT platform.apply_scope_rls('ledger.settlement'::regclass);
SELECT platform.apply_scope_rls('maintenance.asset_category'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_activation'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_list'::regclass);
SELECT platform.apply_scope_rls('marketing.challenge'::regclass);
SELECT platform.apply_scope_rls('marketing.duplicate_candidate'::regclass);
SELECT platform.apply_scope_rls('marketing.form_definition'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_attribute_model'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_match_decision'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_match_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_relationship'::regclass);
SELECT platform.apply_scope_rls('marketing.identity_rules'::regclass);
SELECT platform.apply_scope_rls('marketing.invitation'::regclass);
SELECT platform.apply_scope_rls('marketing.invitation_campaign'::regclass);
SELECT platform.apply_scope_rls('marketing.journey'::regclass);
SELECT platform.apply_scope_rls('marketing.journey_enrollment'::regclass);
SELECT platform.apply_scope_rls('marketing.message_trigger'::regclass);
SELECT platform.apply_scope_rls('marketing.privacy_incident'::regclass);
SELECT platform.apply_scope_rls('marketing.referral'::regclass);
SELECT platform.apply_scope_rls('marketing.retention_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.sla_policy'::regclass);
SELECT platform.apply_scope_rls('marketing.suppression'::regclass);
SELECT platform.apply_scope_rls('orders.b2b_credit'::regclass);
SELECT platform.apply_scope_rls('orders.deposit_policy'::regclass);
SELECT platform.apply_scope_rls('orders.fraud_rule'::regclass);
SELECT platform.apply_scope_rls('orders.payment_link'::regclass);
SELECT platform.apply_scope_rls('orders.pos_shift'::regclass);
SELECT platform.apply_scope_rls('orders.refund_batch'::regclass);
SELECT platform.apply_scope_rls('orders.resale_fee_policy'::regclass);
SELECT platform.apply_scope_rls('orders.resale_listing'::regclass);
SELECT platform.apply_scope_rls('orders.sales_order'::regclass);
SELECT platform.apply_scope_rls('orders.stored_value_authorisation'::regclass);
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
SELECT platform.apply_scope_rls('payments.matching_rules'::regclass);
SELECT platform.apply_scope_rls('payments.merchant_account'::regclass);
SELECT platform.apply_scope_rls('payments.method'::regclass);
SELECT platform.apply_scope_rls('payments.method_config'::regclass);
SELECT platform.apply_scope_rls('payments.mixed_tender_rules'::regclass);
SELECT platform.apply_scope_rls('payments.payment_terms'::regclass);
SELECT platform.apply_scope_rls('payments.provider'::regclass);
SELECT platform.apply_scope_rls('payments.provider_connection'::regclass);
SELECT platform.apply_scope_rls('payments.reconciliation_source'::regclass);
SELECT platform.apply_scope_rls('payments.risk_rules'::regclass);
SELECT platform.apply_scope_rls('payments.routing_rule'::regclass);
SELECT platform.apply_scope_rls('payments.stored_forward'::regclass);
SELECT platform.apply_scope_rls('payments.terminal'::regclass);
SELECT platform.apply_scope_rls('platform.configuration_profile'::regclass);
SELECT platform.apply_scope_rls('platform.connectivity_policy'::regclass);
SELECT platform.apply_scope_rls('platform.dead_letter'::regclass);
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
SELECT platform.apply_scope_rls('rental.settlement'::regclass);
SELECT platform.apply_scope_rls('reporting.alert'::regclass);
SELECT platform.apply_scope_rls('reporting.alert_rule'::regclass);
SELECT platform.apply_scope_rls('reporting.anomaly'::regclass);
SELECT platform.apply_scope_rls('reporting.delivery'::regclass);
SELECT platform.apply_scope_rls('reporting.kpi_definition'::regclass);
SELECT platform.apply_scope_rls('reporting.kpi_target'::regclass);
SELECT platform.apply_scope_rls('reporting.natural_language_query'::regclass);
SELECT platform.apply_scope_rls('reporting.pipeline'::regclass);
SELECT platform.apply_scope_rls('reporting.report_definition'::regclass);
SELECT platform.apply_scope_rls('reporting.report_definition_version'::regclass);
SELECT platform.apply_scope_rls('reporting.semantic_model'::regclass);
SELECT platform.apply_scope_rls('reporting.subscription'::regclass);
SELECT platform.apply_scope_rls('resources.allocation_policy'::regclass);
SELECT platform.apply_scope_rls('resources.attribute_definition'::regclass);
SELECT platform.apply_scope_rls('resources.qualification'::regclass);
SELECT platform.apply_scope_rls('resources.resource'::regclass);
SELECT platform.apply_scope_rls('resources.resource_audit'::regclass);
SELECT platform.apply_scope_rls('resources.resource_block'::regclass);
SELECT platform.apply_scope_rls('resources.resource_category'::regclass);
SELECT platform.apply_scope_rls('resources.resource_dependency'::regclass);
SELECT platform.apply_scope_rls('resources.resource_package'::regclass);
SELECT platform.apply_scope_rls('resources.resource_relation'::regclass);
SELECT platform.apply_scope_rls('resources.resource_requirement'::regclass);
SELECT platform.apply_scope_rls('resources.resource_schedule'::regclass);
SELECT platform.apply_scope_rls('resources.resource_type'::regclass);
SELECT platform.apply_scope_rls('resources.venue_assignment'::regclass);
SELECT platform.apply_scope_rls('retail.product_recommendation'::regclass);
SELECT platform.apply_scope_rls('seating.accessible'::regclass);
SELECT platform.apply_scope_rls('seating.group_request'::regclass);
SELECT platform.apply_scope_rls('seating.hold_pool'::regclass);
SELECT platform.apply_scope_rls('seating.hold_type'::regclass);
SELECT platform.apply_scope_rls('seating.reassignment'::regclass);
SELECT platform.apply_scope_rls('seating.recommendation_rules'::regclass);
SELECT platform.apply_scope_rls('seating.seat_block'::regclass);
SELECT platform.apply_scope_rls('seating.seat_rules'::regclass);
SELECT platform.apply_scope_rls('seating.section'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_assignment'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_audit'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_credential'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_rollout'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_tamper_event'::regclass);
SELECT platform.apply_scope_rls('tenancy.device_telemetry'::regclass);
SELECT platform.apply_scope_rls('venuemap.map'::regclass);
SELECT platform.apply_scope_rls('wallet.accounting_mapping'::regclass);
SELECT platform.apply_scope_rls('wallet.adjustment'::regclass);
SELECT platform.apply_scope_rls('wallet.channel_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.configuration_version'::regclass);
SELECT platform.apply_scope_rls('wallet.consumption_policy'::regclass);
SELECT platform.apply_scope_rls('wallet.credential'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_eligibility'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_lot'::regclass);
SELECT platform.apply_scope_rls('wallet.credit_type'::regclass);
SELECT platform.apply_scope_rls('wallet.dispute'::regclass);
SELECT platform.apply_scope_rls('wallet.funding_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.gift_card_product'::regclass);
SELECT platform.apply_scope_rls('wallet.refund_policy'::regclass);
SELECT platform.apply_scope_rls('wallet.restriction'::regclass);
SELECT platform.apply_scope_rls('wallet.risk_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.shared_wallet'::regclass);
SELECT platform.apply_scope_rls('wallet.transfer_rules'::regclass);
SELECT platform.apply_scope_rls('wallet.voucher_type'::regclass);
SELECT platform.apply_scope_rls('wallet.wallet_type'::regclass);
SELECT platform.apply_scope_rls('whitelabel.config_version'::regclass);
SELECT platform.apply_scope_rls('whitelabel.content_page'::regclass);
SELECT platform.apply_scope_rls('whitelabel.faq_category'::regclass);
SELECT platform.apply_scope_rls('whitelabel.footer_config'::regclass);
SELECT platform.apply_scope_rls('whitelabel.policy'::regclass);
SELECT platform.apply_scope_rls('whitelabel.promo_block'::regclass);
SELECT platform.apply_scope_rls('workforce.field_ownership'::regclass);
SELECT platform.apply_scope_rls('workforce.integration_source'::regclass);
SELECT platform.apply_scope_rls('workforce.leave_request'::regclass);
SELECT platform.apply_scope_rls('workforce.open_shift'::regclass);
SELECT platform.apply_scope_rls('workforce.shift_template'::regclass);
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
SELECT platform.apply_venue_rls('catalogue.donation_campaign'::regclass);
SELECT platform.apply_venue_rls('catalogue.price_list'::regclass);
SELECT platform.apply_venue_rls('catalogue.published_bundle'::regclass);
SELECT platform.apply_venue_rls('fnb.delivery_location'::regclass);
SELECT platform.apply_venue_rls('fnb.location_session'::regclass);
SELECT platform.apply_venue_rls('games.card'::regclass);
SELECT platform.apply_venue_rls('games.game'::regclass);
SELECT platform.apply_venue_rls('games.prize'::regclass);
SELECT platform.apply_venue_rls('games.redemption'::regclass);
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
SELECT platform.apply_venue_rls('orders.refund_policy'::regclass);
SELECT platform.apply_venue_rls('orders.reservation'::regclass);
SELECT platform.apply_venue_rls('platform.cross_region_entitlement'::regclass);
SELECT platform.apply_venue_rls('platform.outlet'::regclass);
SELECT platform.apply_venue_rls('platform.sale_board'::regclass);
SELECT platform.apply_venue_rls('platform.venue_settings'::regclass);
SELECT platform.apply_venue_rls('promotions.allocation_component'::regclass);
SELECT platform.apply_venue_rls('promotions.bundle'::regclass);
SELECT platform.apply_venue_rls('promotions.bundle_component'::regclass);
SELECT platform.apply_venue_rls('promotions.coupon_campaign'::regclass);
SELECT platform.apply_venue_rls('promotions.promotion'::regclass);
SELECT platform.apply_venue_rls('promotions.voucher_batch'::regclass);
SELECT platform.apply_venue_rls('queue.queue'::regclass);
SELECT platform.apply_venue_rls('rental.agreement'::regclass);
SELECT platform.apply_venue_rls('reporting.dashboard'::regclass);
SELECT platform.apply_venue_rls('retail.shop_and_drop'::regclass);
SELECT platform.apply_venue_rls('retail.store_rule'::regclass);
SELECT platform.apply_venue_rls('seating.seat_category'::regclass);
SELECT platform.apply_venue_rls('seating.seat_map'::regclass);
SELECT platform.apply_venue_rls('wallet.wallet_transaction'::regclass);
SELECT platform.apply_venue_rls('workforce.announcement'::regclass);
SELECT platform.apply_venue_rls('workforce.attendance'::regclass);
SELECT platform.apply_venue_rls('workforce.rota_assignment'::regclass);

-- Scoped through the parent that owns the row (a NOT NULL declared foreign key).
SELECT platform.apply_parent_rls('access.entry_rule_point'::regclass, 'admission_profile_id', 'access.admission_rules'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.index_source'::regclass, 'collection_id', 'ai.knowledge_collection'::regclass, 'id');
SELECT platform.apply_parent_rls('ai.message'::regclass, 'conversation_id', 'ai.conversation'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.decision'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.escalation'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('approvals.rule'::regclass, 'matrix_id', 'approvals.matrix'::regclass, 'id');
SELECT platform.apply_parent_rls('assets.media_usage'::regclass, 'asset_id', 'assets.media_asset'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.inventory_hold'::regclass, 'holder_workstation_id', 'platform.workstation'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.performance'::regclass, 'event_id', 'catalogue.event'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.price'::regclass, 'price_list_id', 'catalogue.price_list'::regclass, 'id');
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
SELECT platform.apply_parent_rls('ledger.event_budget'::regclass, 'event_id', 'catalogue.event'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.fiscal_period'::regclass, 'legal_entity_id', 'ledger.legal_entity'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.fx_rate'::regclass, 'region_id', 'platform.scope'::regclass, 'id');
SELECT platform.apply_parent_rls('ledger.settlement_exception'::regclass, 'settlement_id', 'ledger.settlement'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.inspection_item'::regclass, 'inspection_id', 'maintenance.inspection'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.inspection_template_item'::regclass, 'inspection_template_id', 'maintenance.inspection_template'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.preventive_plan'::regclass, 'asset_id', 'maintenance.asset'::regclass, 'id');
SELECT platform.apply_parent_rls('maintenance.work_order_attachment'::regclass, 'work_order_id', 'maintenance.work_order'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.attribution_touch'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.challenge_progress'::regclass, 'challenge_id', 'marketing.challenge'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.conversation_message'::regclass, 'conversation_id', 'marketing.conversation'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.form_definition_field'::regclass, 'form_definition_id', 'marketing.form_definition'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.guest_profile'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.journey_step'::regclass, 'journey_id', 'marketing.journey'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.loyalty_position'::regclass, 'programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.message_delivery'::regclass, 'campaign_id', 'marketing.campaign'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.points_earning_rule'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.programme_tier'::regclass, 'loyalty_programme_id', 'marketing.loyalty_programme'::regclass, 'id');
SELECT platform.apply_parent_rls('marketing.segment_criterion'::regclass, 'segment_id', 'marketing.segment'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cart_line'::regclass, 'cart_id', 'orders.cart'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cash_count_line'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.cash_movement'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.credit_override'::regclass, 'b2b_credit_id', 'orders.b2b_credit'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit_box_foreign_holding'::regclass, 'deposit_box_id', 'orders.deposit_box'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.deposit_box_opening_denomination'::regclass, 'deposit_box_id', 'orders.deposit_box'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.discount'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.group_booking'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.invitation'::regclass, 'product_id', 'catalogue.product'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.no_sale_event'::regclass, 'shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_fee'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_line'::regclass, 'sales_order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.payment'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.pos_shift_approval'::regclass, 'pos_shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.pos_shift_incident'::regclass, 'pos_shift_id', 'orders.pos_shift'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.refund'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.refund_policy_time_band'::regclass, 'refund_policy_id', 'orders.refund_policy'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.reservation_line'::regclass, 'reservation_id', 'orders.reservation'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.ticket_transfer'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.upgrade'::regclass, 'order_id', 'orders.sales_order'::regclass, 'id');
SELECT platform.apply_parent_rls('pii.subject_biometric'::regclass, 'entitlement_id', 'access.entitlement'::regclass, 'id');
SELECT platform.apply_parent_rls('platform.device'::regclass, 'workstation_id', 'platform.workstation'::regclass, 'id');
SELECT platform.apply_parent_rls('platform.dsar_request'::regclass, 'request_id', 'approvals.request'::regclass, 'id');
SELECT platform.apply_parent_rls('platform.sale_board_page'::regclass, 'sale_board_id', 'platform.sale_board'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.allocation_split'::regclass, 'bundle_id', 'promotions.bundle'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.bundle_choice_group'::regclass, 'bundle_id', 'promotions.bundle'::regclass, 'id');
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
SELECT platform.apply_parent_rls('venuemap.path'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');
SELECT platform.apply_parent_rls('venuemap.point'::regclass, 'map_id', 'venuemap.map'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.faq_entry'::regclass, 'faq_category_id', 'whitelabel.faq_category'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.footer_config_column'::regclass, 'footer_config_id', 'whitelabel.footer_config'::regclass, 'id');
SELECT platform.apply_parent_rls('whitelabel.footer_config_social_link'::regclass, 'footer_config_id', 'whitelabel.footer_config'::regclass, 'id');
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
SELECT platform.apply_parent_rls('marketing.wishlist_item'::regclass, 'variant_id', 'catalogue.variant'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.chargeback'::regclass, 'payment_id', 'orders.payment'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.order_line_eligibility'::regclass, 'order_line_id', 'orders.order_line'::regclass, 'id');
SELECT platform.apply_parent_rls('orders.payment_tip'::regclass, 'payment_id', 'orders.payment'::regclass, 'id');
SELECT platform.apply_parent_rls('promotions.bundle_choice_option'::regclass, 'bundle_choice_group_id', 'promotions.bundle_choice_group'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.export'::regclass, 'execution_id', 'reporting.execution'::regclass, 'id');
SELECT platform.apply_parent_rls('reporting.schedule_recipient'::regclass, 'schedule_id', 'reporting.schedule'::regclass, 'id');
SELECT platform.apply_parent_rls('retail.reservation_line'::regclass, 'reservation_id', 'retail.reservation'::regclass, 'id');
SELECT platform.apply_parent_rls('seating.seat_hold'::regclass, 'performance_id', 'catalogue.performance'::regclass, 'id');
SELECT platform.apply_parent_rls('catalogue.channel_allocation'::regclass, 'envelope_id', 'catalogue.channel_capacity'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.recipe'::regclass, 'menu_item_id', 'fnb.menu_item'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.sub_bill'::regclass, 'bill_split_id', 'fnb.bill_split'::regclass, 'id');
SELECT platform.apply_parent_rls('fnb.production_run'::regclass, 'recipe_id', 'fnb.recipe'::regclass, 'id');

-- No policy. Each needs a scoping decision (carry scope_path or venue_id, or a
-- NOT NULL owning reference) before row-level security can hold for it.
--   access.access_change  -- only nullable references (order_id -> orders.sales_order)
--   access.parking_entitlement  -- several protected owners (facility_id -> access.parking_facility, order_id -> orders.sales_order); which one owns the row is not decided
--   ai.chunk_ref  -- its owner ai.knowledge_document has no policy either
--   ai.index_failure  -- no scope column and no declared owner
--   ai.knowledge_document  -- only nullable references (collection_id -> ai.knowledge_collection)
--   ai.proposed_action  -- only nullable references (interaction_id -> ai.activity, decided_by_principal_id -> identity.principal)
--   ai.suggestion_outcome  -- no scope column and no declared owner
--   approvals.accreditation_badge  -- no scope column and no declared owner
--   approvals.step_up_policy  -- no scope column and no declared owner
--   assets.media_collection_member  -- no scope column and no declared owner
--   catalogue.alternative_code  -- only nullable references (variant_id -> catalogue.variant, product_id -> catalogue.product)
--   catalogue.membership_benefit  -- no scope column and no declared owner
--   catalogue.membership_programme  -- no scope column and no declared owner
--   catalogue.plan_benefit  -- no scope column and no declared owner
--   catalogue.product_version  -- only nullable references (product_id -> catalogue.product)
--   fnb.allergen_verdict  -- no scope column and no declared owner
--   fnb.cold_chain_event  -- no scope column and no declared owner
--   fnb.combo  -- no scope column and no declared owner
--   fnb.combo_slot  -- no scope column and no declared owner
--   fnb.delivery_location_outlet  -- only nullable references (location_id -> fnb.delivery_location, outlet_id -> platform.outlet)
--   fnb.dining_table  -- only nullable references (outlet_id -> platform.outlet)
--   fnb.ingredient_substitute  -- no scope column and no declared owner
--   fnb.kitchen_exception  -- no scope column and no declared owner
--   fnb.kitchen_station  -- only nullable references (outlet_id -> platform.outlet)
--   fnb.menu_item_modifier  -- no scope column and no declared owner
--   fnb.production_plan  -- no scope column and no declared owner
--   fnb.production_plan_line  -- its owner fnb.production_plan has no policy either
--   fnb.reservation_table  -- its owner fnb.dining_table has no policy either
--   fnb.sold_out_item  -- no scope column and no declared owner
--   fnb.substitution_rule  -- no scope column and no declared owner
--   fnb.temperature_log  -- no scope column and no declared owner
--   games.play  -- only nullable references (game_id -> games.game)
--   games.reader_deployment  -- no scope column and no declared owner
--   identity.authz_audit  -- only nullable references (actor_principal_id -> identity.principal, subject_principal_id -> identity.principal)
--   identity.benefit_usage  -- no scope column and no declared owner
--   identity.customer_membership  -- no scope column and no declared owner
--   identity.membership_history  -- no scope column and no declared owner
--   identity.mfa_challenge  -- its owner identity.principal has no policy either
--   identity.mfa_method  -- only nullable references (principal_id -> identity.principal)
--   identity.mfa_recovery_code  -- only nullable references (principal_id -> identity.principal)
--   identity.module  -- no scope column and no declared owner
--   identity.otp_challenge  -- its owner pii.subject has no policy either
--   identity.permission  -- no scope column and no declared owner
--   identity.principal  -- only nullable references (primary_role_id -> identity.role, home_scope_id -> platform.scope)
--   identity.principal_credential  -- only nullable references (principal_id -> identity.principal)
--   identity.refresh_token  -- no scope column and no declared owner
--   identity.role  -- no scope column and no declared owner
--   identity.role_permission  -- its owner identity.role has no policy either
--   inventory.count  -- only nullable references (started_by_principal_id -> identity.principal, posted_by_principal_id -> identity.principal, journal_entry_id -> ledger.journal_entry)
--   inventory.count_line  -- its owner inventory.count has no policy either
--   inventory.quotation_line  -- several protected owners (quotation_id -> inventory.quotation, item_id -> inventory.item); which one owns the row is not decided
--   inventory.serialised_item  -- no scope column and no declared owner
--   inventory.stock_batch  -- several protected owners (item_id -> inventory.item, location_id -> inventory.location); which one owns the row is not decided
--   inventory.stock_reservation  -- no scope column and no declared owner
--   inventory.supplier_contract  -- no scope column and no declared owner
--   ledger.deposit  -- only nullable references (subject_id -> pii.subject, order_id -> orders.sales_order)
--   ledger.inter_entity_obligation  -- only nullable references (entitlement_id -> access.entitlement, order_id -> orders.sales_order)
--   ledger.recognition_schedule  -- only nullable references (deferred_account_id -> ledger.account, recognised_account_id -> ledger.account, breakage_account_id -> ledger.account)
--   ledger.tax_code  -- only nullable references (account_id -> ledger.account)
--   ledger.tax_exemption  -- its owner ledger.tax_code has no policy either
--   maintenance.asset_document  -- no scope column and no declared owner
--   maintenance.asset_status_change  -- no scope column and no declared owner
--   maintenance.incident_authority_notification  -- no scope column and no declared owner
--   maintenance.incident_investigation_note  -- no scope column and no declared owner
--   maintenance.incident_involved_party  -- no scope column and no declared owner
--   marketing.agent_availability  -- its owner identity.principal has no policy either
--   marketing.badge  -- no scope column and no declared owner
--   marketing.campaign_target  -- no scope column and no declared owner
--   marketing.case_message  -- only nullable references (author_principal_id -> identity.principal, case_id -> marketing.case)
--   marketing.consent_purpose  -- its owner platform.tenant has no policy either
--   marketing.consent_purpose_channel  -- its owner marketing.consent_purpose has no policy either
--   marketing.consent_record  -- its owner pii.subject has no policy either
--   marketing.consent_record_channel  -- its owner marketing.consent_record has no policy either
--   marketing.customer_badge  -- no scope column and no declared owner
--   marketing.form_submission  -- its owner pii.subject has no policy either
--   marketing.guest_device  -- its owner pii.subject has no policy either
--   marketing.guest_document  -- its owner pii.subject has no policy either
--   marketing.guest_extra_field  -- no scope column and no declared owner
--   marketing.guest_extra_option  -- no scope column and no declared owner
--   marketing.guest_extra_value  -- no scope column and no declared owner
--   marketing.guest_note  -- no scope column and no declared owner
--   marketing.guest_preference  -- no scope column and no declared owner
--   marketing.loyalty_campaign  -- no scope column and no declared owner
--   marketing.loyalty_points  -- no scope column and no declared owner
--   marketing.loyalty_rule  -- no scope column and no declared owner
--   marketing.message_dispatch  -- its owner pii.subject has no policy either
--   marketing.message_template  -- its owner platform.tenant has no policy either
--   marketing.points_redemption_rule  -- only nullable references (product_id -> catalogue.product)
--   marketing.review_response  -- no scope column and no declared owner
--   marketing.reward  -- only nullable references (product_id -> catalogue.product)
--   marketing.reward_assignment  -- no scope column and no declared owner
--   marketing.subscription  -- no scope column and no declared owner
--   marketing.touch_point  -- its owner pii.subject has no policy either
--   marketing.waiver_signature  -- no scope column and no declared owner
--   orders.invitation_allowance  -- its owner identity.principal has no policy either
--   orders.membership_renewal  -- only nullable references (order_id -> orders.sales_order)
--   orders.ticket_template  -- no scope column and no declared owner
--   orders.ticket_template_channel  -- its owner orders.ticket_template has no policy either
--   payments.deposit_activity  -- only nullable references (payment_id -> orders.payment)
--   payments.fee_rule  -- no scope column and no declared owner
--   payments.token  -- its owner pii.subject has no policy either
--   pii.subject  -- no scope column and no declared owner
--   pii.subject_contact  -- its owner pii.subject has no policy either
--   pii.subject_document  -- its owner pii.subject has no policy either
--   platform.audit_read  -- its owners identity.principal, pii.subject have no policy either
--   platform.audit_record  -- only nullable references (principal_id -> identity.principal, org_unit_id -> platform.scope)
--   platform.cell_endpoint  -- no scope column and no declared owner
--   platform.denomination  -- no scope column and no declared owner
--   platform.device_heartbeat  -- only nullable references (device_id -> platform.device)
--   platform.guest_link  -- no scope column and no declared owner
--   platform.profile_deployment  -- no scope column and no declared owner
--   platform.region_settings  -- only nullable references (org_unit_id -> platform.scope)
--   platform.sale_board_tile  -- only nullable references (page_id -> platform.sale_board_page)
--   platform.tenant  -- only nullable references (home_region_id -> platform.scope)
--   platform.wallet_authorisation  -- its owner platform.guest_link has no policy either
--   pricing.dynamic_price_action  -- no scope column and no declared owner
--   pricing.dynamic_price_condition  -- no scope column and no declared owner
--   promotions.coupon_code_batch  -- no scope column and no declared owner
--   promotions.promotion_variant  -- no scope column and no declared owner
--   promotions.upsell_rule  -- only nullable references (suggested_bundle_id -> promotions.bundle)
--   rental.agreement_item  -- no scope column and no declared owner
--   rental.inspection_item  -- no scope column and no declared owner
--   rental.participant  -- no scope column and no declared owner
--   reporting.dashboard_tile  -- several protected owners (dashboard_id -> reporting.dashboard, report_id -> reporting.report_definition); which one owns the row is not decided
--   resources.performance_participant  -- no scope column and no declared owner
--   retail.exchange  -- its owners retail.return, retail.sale have no policy either
--   retail."return"  -- its owner retail.sale has no policy either
--   retail.return_line  -- its owner retail.return has no policy either
--   retail.sale  -- several protected owners (order_id -> orders.sales_order, outlet_id -> platform.outlet); which one owns the row is not decided
--   retail.sale_line  -- its owner retail.sale has no policy either
--   seating.seat  -- only nullable references (seat_map_id -> seating.seat_map)
--   seating.seat_block_item  -- no scope column and no declared owner
--   seating.seat_hold_item  -- no scope column and no declared owner
--   seating.seat_price_band  -- no scope column and no declared owner
--   subscription.capacity_pack  -- no scope column and no declared owner
--   subscription.contract  -- its owners platform.tenant, subscription.plan have no policy either
--   subscription.enforcement_policy  -- no scope column and no declared owner
--   subscription.go_live_readiness  -- no scope column and no declared owner
--   subscription.licensing_model  -- no scope column and no declared owner
--   subscription.module_listing  -- no scope column and no declared owner
--   subscription.partner_quote  -- no scope column and no declared owner
--   subscription.plan  -- no scope column and no declared owner
--   subscription.plan_limit  -- its owner subscription.plan has no policy either
--   subscription.plan_module  -- its owner subscription.plan has no policy either
--   subscription.tier_allowance  -- no scope column and no declared owner
--   subscription.tier_module  -- no scope column and no declared owner
--   subscription.trial_config  -- no scope column and no declared owner
--   subscription.vsi_assessment  -- no scope column and no declared owner
--   subscription.vsi_model  -- no scope column and no declared owner
--   sync.cell_connection  -- no scope column and no declared owner
--   sync.cross_cell_request  -- no scope column and no declared owner
--   tenancy.device_firmware  -- no scope column and no declared owner
--   venuemap.import_job  -- only nullable references (map_id -> venuemap.map)
--   venuemap.map_version  -- no scope column and no declared owner
--   wallet.balance  -- no scope column and no declared owner
--   wallet.gift_card  -- its owner pii.subject has no policy either
--   wallet.hold  -- only nullable references (order_id -> orders.sales_order)
--   wallet.shared_wallet_member  -- no scope column and no declared owner
--   wallet.wallet  -- its owner pii.subject has no policy either
--   whitelabel.banner  -- its owner whitelabel.tenant_config has no policy either
--   whitelabel.custom_domain  -- no scope column and no declared owner
--   whitelabel.feature_toggle  -- its owner whitelabel.tenant_config has no policy either
--   whitelabel.homepage_section  -- only nullable references (content_page_id -> whitelabel.content_page)
--   whitelabel.module_enablement  -- its owner whitelabel.tenant_config has no policy either
--   whitelabel.navigation_item  -- no scope column and no declared owner
--   whitelabel.tenant_config  -- its owner platform.tenant has no policy either
--   workforce.attendance_amendment  -- no scope column and no declared owner
--   workforce.employee  -- no scope column and no declared owner
--   workforce.employment  -- no scope column and no declared owner
--   workforce.job_title  -- no scope column and no declared owner
--   workforce.leave_balance  -- no scope column and no declared owner
--   workforce.leave_type  -- no scope column and no declared owner
--   workforce.shift  -- no scope column and no declared owner
--   workforce.training_record  -- no scope column and no declared owner
