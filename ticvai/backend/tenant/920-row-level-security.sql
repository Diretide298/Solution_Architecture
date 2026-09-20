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
CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path text)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_scope_path IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND row_scope_path::ltree <@ ANY (platform.current_scope_paths());
$$;

-- Applies the standard policy to a table.
-- **FORCE is the whole point.** Without it the table owner — which is what a migration and most
-- pooled application connections run as — bypasses every policy silently.
CREATE OR REPLACE FUNCTION platform.apply_scope_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'scope_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.in_scope(scope_path)) '
        'WITH CHECK (platform.in_scope(scope_path))', policy_name, target);
END
$$;

-- **59 tables carry `venue_id` and no `scope_path`, and a policy set built on `scope_path` alone
-- leaves every one of them open.** `check-migrations` has said so since it was written — *"checking
-- only scope_path missed 41 tables that carry venue_id instead; they would have passed with no
-- policy at all"* — and the hand-written baseline never closed it because it protected three
-- tables in total.
--
-- A venue id is resolved to its path through the scope tree rather than assumed. **The subquery is
-- the price of not carrying a redundant `scope_path` column on sixty tables**, and `platform.scope`
-- is small, cached and indexed on `id`.
CREATE OR REPLACE FUNCTION platform.venue_in_scope(row_venue_id uuid)
    RETURNS boolean
    LANGUAGE sql
    STABLE
    PARALLEL SAFE
AS $$
    SELECT row_venue_id IS NOT NULL
       AND cardinality(platform.current_scope_paths()) > 0
       AND EXISTS (
            SELECT 1 FROM platform.scope s
             WHERE s.id = row_venue_id
               AND s.path::ltree <@ ANY (platform.current_scope_paths()));
$$;

CREATE OR REPLACE FUNCTION platform.apply_venue_rls(target regclass)
    RETURNS void
    LANGUAGE plpgsql
AS $$
DECLARE
    policy_name text := 'venue_isolation';
BEGIN
    EXECUTE format('ALTER TABLE %s ENABLE ROW LEVEL SECURITY', target);
    EXECUTE format('ALTER TABLE %s FORCE ROW LEVEL SECURITY', target);
    EXECUTE format('DROP POLICY IF EXISTS %I ON %s', policy_name, target);
    EXECUTE format(
        'CREATE POLICY %I ON %s USING (platform.venue_in_scope(venue_id)) '
        'WITH CHECK (platform.venue_in_scope(venue_id))', policy_name, target);
END
$$;

-- **242 tables carry `scope_path` and 58 carry `venue_id` instead, out of 572.**
-- Both are protected. A table with neither is not scoped -- it is reference data, a
-- registry, or the migration log itself, and a policy on it would deny every row to
-- everybody.


ALTER TABLE platform.scope ENABLE ROW LEVEL SECURITY;
ALTER TABLE platform.scope FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS scope_isolation ON platform.scope;
CREATE POLICY scope_isolation ON platform.scope
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
SELECT platform.apply_scope_rls('catalogue.import_job'::regclass);
SELECT platform.apply_scope_rls('catalogue.prepaid_minutes'::regclass);
SELECT platform.apply_scope_rls('catalogue.product'::regclass);
SELECT platform.apply_scope_rls('catalogue.product_category'::regclass);
SELECT platform.apply_scope_rls('catalogue.session_template'::regclass);
SELECT platform.apply_scope_rls('catalogue.space'::regclass);
SELECT platform.apply_scope_rls('fnb.corrective_action'::regclass);
SELECT platform.apply_scope_rls('fnb.modifier_group'::regclass);
SELECT platform.apply_scope_rls('fnb.product_recommendation'::regclass);
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
SELECT platform.apply_scope_rls('identity.delegated_access'::regclass);
SELECT platform.apply_scope_rls('identity.password_policy'::regclass);
SELECT platform.apply_scope_rls('identity.segregation_rule'::regclass);
SELECT platform.apply_scope_rls('identity.sso_group_mapping'::regclass);
SELECT platform.apply_scope_rls('identity.sso_provider'::regclass);
SELECT platform.apply_scope_rls('inventory.purchase_order'::regclass);
SELECT platform.apply_scope_rls('inventory.quotation'::regclass);
SELECT platform.apply_scope_rls('inventory.supplier'::regclass);
SELECT platform.apply_scope_rls('inventory.transfer'::regclass);
SELECT platform.apply_scope_rls('ledger.legal_entity'::regclass);
SELECT platform.apply_scope_rls('ledger.settlement'::regclass);
SELECT platform.apply_scope_rls('maintenance.asset_category'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_activation'::regclass);
SELECT platform.apply_scope_rls('marketing.audience_list'::regclass);
SELECT platform.apply_scope_rls('marketing.challenge'::regclass);
SELECT platform.apply_scope_rls('marketing.duplicate_candidate'::regclass);
SELECT platform.apply_scope_rls('marketing.form_definition'::regclass);
SELECT platform.apply_scope_rls('marketing.guest_attribute_model'::regclass);
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
SELECT platform.apply_scope_rls('orders.fraud_rule'::regclass);
SELECT platform.apply_scope_rls('orders.payment_link'::regclass);
SELECT platform.apply_scope_rls('orders.pos_shift'::regclass);
SELECT platform.apply_scope_rls('orders.resale_listing'::regclass);
SELECT platform.apply_scope_rls('orders.sales_order'::regclass);
SELECT platform.apply_scope_rls('orders.stored_value_authorisation'::regclass);
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
SELECT platform.apply_scope_rls('reporting.pipeline'::regclass);
SELECT platform.apply_scope_rls('reporting.report_definition'::regclass);
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

-- Scoped by venue, resolved through the scope tree.
SELECT platform.apply_venue_rls('access.parking_facility'::regclass);
SELECT platform.apply_venue_rls('assets.media_asset'::regclass);
SELECT platform.apply_venue_rls('assets.media_collection'::regclass);
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
