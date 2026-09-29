-- Indexes in the control database: declared foreign keys, conventions and scope paths.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Every declared foreign key is indexed** (data-and-storage.md) -- Postgres does not
-- index the referencing column itself. **A convention is indexed and not constrained**
-- (ADR-0011): most references are naming habits the contracts never asserted, and
-- enforcing one fails on the first row that legitimately points nowhere.
-- Names follow naming-and-style 6.1: `<table>_<columns>_idx`.

-- convention, not declared: control.api_client.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS api_client_developer_id_idx ON control.api_client (developer_id);
-- convention, not declared: control.api_limit.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS api_limit_client_id_idx ON control.api_limit (client_id);
-- convention, not declared: control.archival_job.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS archival_job_cell_id_idx ON control.archival_job (cell_id);
-- convention, not declared: control.backup_run.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS backup_run_cell_id_idx ON control.backup_run (cell_id);
-- convention, not declared: control.burst_environment.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS burst_environment_performance_id_idx ON control.burst_environment (performance_id);
-- convention, not declared: control.burst_environment.usage_record_id -> control.usage_record
CREATE INDEX IF NOT EXISTS burst_environment_usage_record_id_idx ON control.burst_environment (usage_record_id);
-- convention, not declared: control.cell.cluster_id -> control.cell_cluster
CREATE INDEX IF NOT EXISTS cell_cluster_id_idx ON control.cell (cluster_id);
-- convention, not declared: control.cell_cluster.modelled_on_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_cluster_modelled_on_cell_id_idx ON control.cell_cluster (modelled_on_cell_id);
-- convention, not declared: control.cell_instance.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_instance_cell_id_idx ON control.cell_instance (cell_id);
-- convention, not declared: control.cell_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_tenant_cell_id_idx ON control.cell_tenant (cell_id);
-- convention, not declared: control.cell_tenant.instance_id -> control.cell_instance
CREATE INDEX IF NOT EXISTS cell_tenant_instance_id_idx ON control.cell_tenant (instance_id);
-- convention, not declared: control.cell_tenant.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS cell_tenant_tenant_id_idx ON control.cell_tenant (tenant_id);
-- convention, not declared: control.content_block.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS content_block_approved_by_principal_id_idx ON control.content_block (approved_by_principal_id);
-- convention, not declared: control.content_block.audience_segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS content_block_audience_segment_id_idx ON control.content_block (audience_segment_id);
-- convention, not declared: control.content_block.page_id -> whitelabel.content_page
CREATE INDEX IF NOT EXISTS content_block_page_id_idx ON control.content_block (page_id);
-- convention, not declared: control.credit_note.invoice_id -> control.invoice
CREATE INDEX IF NOT EXISTS credit_note_invoice_id_idx ON control.credit_note (invoice_id);
-- convention, not declared: control.credit_note.issued_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS credit_note_issued_by_principal_id_idx ON control.credit_note (issued_by_principal_id);
-- convention, not declared: control.credit_note.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS credit_note_tenant_id_idx ON control.credit_note (tenant_id);
-- convention, not declared: control.developer_account.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS developer_account_partner_id_idx ON control.developer_account (partner_id);
-- convention, not declared: control.integration_listing.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS integration_listing_developer_id_idx ON control.integration_listing (developer_id);
-- convention, not declared: control.invoice.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS invoice_tenant_id_idx ON control.invoice (tenant_id);
-- convention, not declared: control.licence_add_on.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS licence_add_on_tenant_id_idx ON control.licence_add_on (tenant_id);
-- convention, not declared: control.migration_run.canary_tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS migration_run_canary_tenant_id_idx ON control.migration_run (canary_tenant_id);
-- convention, not declared: control.migration_run.plan_id -> control.migration_plan
CREATE INDEX IF NOT EXISTS migration_run_plan_id_idx ON control.migration_run (plan_id);
-- convention, not declared: control.migration_run_cell.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS migration_run_cell_cell_id_idx ON control.migration_run_cell (cell_id);
-- convention, not declared: control.migration_run_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS migration_run_tenant_cell_id_idx ON control.migration_run_tenant (cell_id);
-- convention, not declared: control.migration_run_tenant.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS migration_run_tenant_tenant_id_idx ON control.migration_run_tenant (tenant_id);
-- convention, not declared: control.onboarding_application.provisioned_tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS onboarding_application_provisioned_tenant_id_idx ON control.onboarding_application (provisioned_tenant_id);
-- convention, not declared: control.partner.account_manager_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_account_manager_principal_id_idx ON control.partner (account_manager_principal_id);
-- convention, not declared: control.partner.commercial_manager_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_commercial_manager_principal_id_idx ON control.partner (commercial_manager_principal_id);
-- convention, not declared: control.partner.finance_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_finance_owner_principal_id_idx ON control.partner (finance_owner_principal_id);
-- convention, not declared: control.partner.operational_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_operational_owner_principal_id_idx ON control.partner (operational_owner_principal_id);
-- convention, not declared: control.partner.parent_partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_parent_partner_id_idx ON control.partner (parent_partner_id);
-- convention, not declared: control.partner.technical_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_technical_owner_principal_id_idx ON control.partner (technical_owner_principal_id);
-- convention, not declared: control.partner_agreement.accepted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_agreement_accepted_by_principal_id_idx ON control.partner_agreement (accepted_by_principal_id);
-- convention, not declared: control.partner_agreement.branding_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS partner_agreement_branding_asset_id_idx ON control.partner_agreement (branding_asset_id);
-- convention, not declared: control.partner_agreement.commercial_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_agreement_commercial_owner_principal_id_idx ON control.partner_agreement (commercial_owner_principal_id);
-- convention, not declared: control.partner_agreement.finance_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_agreement_finance_owner_principal_id_idx ON control.partner_agreement (finance_owner_principal_id);
-- convention, not declared: control.partner_agreement.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS partner_agreement_legal_entity_id_idx ON control.partner_agreement (legal_entity_id);
-- convention, not declared: control.partner_allocation.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_allocation_agreement_id_idx ON control.partner_allocation (agreement_id);
-- convention, not declared: control.partner_allocation.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_allocation_approval_request_id_idx ON control.partner_allocation (approval_request_id);
-- convention, not declared: control.partner_allocation.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS partner_allocation_event_id_idx ON control.partner_allocation (event_id);
-- convention, not declared: control.partner_allocation.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_allocation_partner_id_idx ON control.partner_allocation (partner_id);
-- convention, not declared: control.partner_allocation.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS partner_allocation_product_id_idx ON control.partner_allocation (product_id);
-- convention, not declared: control.partner_allocation.venue_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS partner_allocation_venue_id_idx ON control.partner_allocation (venue_id);
-- convention, not declared: control.partner_application.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_application_approval_request_id_idx ON control.partner_application (approval_request_id);
-- convention, not declared: control.partner_application.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_application_partner_id_idx ON control.partner_application (partner_id);
-- convention, not declared: control.partner_application_review_task.assignee_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_application_review_task_assignee_principal_id_idx ON control.partner_application_review_task (assignee_principal_id);
-- convention, not declared: control.partner_billing_profile.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_billing_profile_agreement_id_idx ON control.partner_billing_profile (agreement_id);
-- convention, not declared: control.partner_billing_profile.billing_contact_id -> control.partner_contact
CREATE INDEX IF NOT EXISTS partner_billing_profile_billing_contact_id_idx ON control.partner_billing_profile (billing_contact_id);
-- convention, not declared: control.partner_billing_profile.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_billing_profile_partner_id_idx ON control.partner_billing_profile (partner_id);
-- convention, not declared: control.partner_billing_profile.tax_profile_id -> catalogue.tax_profile
CREATE INDEX IF NOT EXISTS partner_billing_profile_tax_profile_id_idx ON control.partner_billing_profile (tax_profile_id);
-- convention, not declared: control.partner_booking_limit.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_booking_limit_agreement_id_idx ON control.partner_booking_limit (agreement_id);
-- convention, not declared: control.partner_booking_limit.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_booking_limit_partner_id_idx ON control.partner_booking_limit (partner_id);
-- convention, not declared: control.partner_capability_grant.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS partner_capability_grant_event_id_idx ON control.partner_capability_grant (event_id);
-- convention, not declared: control.partner_capability_grant.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_capability_grant_partner_id_idx ON control.partner_capability_grant (partner_id);
-- convention, not declared: control.partner_case.contact_id -> control.partner_contact
CREATE INDEX IF NOT EXISTS partner_case_contact_id_idx ON control.partner_case (contact_id);
-- convention, not declared: control.partner_case.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS partner_case_order_id_idx ON control.partner_case (order_id);
-- convention, not declared: control.partner_case.owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_case_owner_principal_id_idx ON control.partner_case (owner_principal_id);
-- convention, not declared: control.partner_case.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_case_partner_id_idx ON control.partner_case (partner_id);
-- convention, not declared: control.partner_case.settlement_batch_id -> control.partner_settlement_batch
CREATE INDEX IF NOT EXISTS partner_case_settlement_batch_id_idx ON control.partner_case (settlement_batch_id);
-- convention, not declared: control.partner_change_request.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_change_request_approval_request_id_idx ON control.partner_change_request (approval_request_id);
-- convention, not declared: control.partner_change_request.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_change_request_approved_by_principal_id_idx ON control.partner_change_request (approved_by_principal_id);
-- convention, not declared: control.partner_change_request.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS partner_change_request_order_id_idx ON control.partner_change_request (order_id);
-- convention, not declared: control.partner_change_request.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_change_request_partner_id_idx ON control.partner_change_request (partner_id);
-- convention, not declared: control.partner_change_request.refund_id -> orders.refund
CREATE INDEX IF NOT EXISTS partner_change_request_refund_id_idx ON control.partner_change_request (refund_id);
-- convention, not declared: control.partner_change_request.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_change_request_requested_by_principal_id_idx ON control.partner_change_request (requested_by_principal_id);
-- convention, not declared: control.partner_change_request.target_performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS partner_change_request_target_performance_id_idx ON control.partner_change_request (target_performance_id);
-- convention, not declared: control.partner_commercial_exception.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_commercial_exception_agreement_id_idx ON control.partner_commercial_exception (agreement_id);
-- convention, not declared: control.partner_commercial_exception.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_commercial_exception_approval_request_id_idx ON control.partner_commercial_exception (approval_request_id);
-- convention, not declared: control.partner_commercial_exception.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_commercial_exception_partner_id_idx ON control.partner_commercial_exception (partner_id);
-- convention, not declared: control.partner_commercial_exception.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_commercial_exception_requested_by_principal_id_idx ON control.partner_commercial_exception (requested_by_principal_id);
-- convention, not declared: control.partner_commission_line.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_commission_line_agreement_id_idx ON control.partner_commission_line (agreement_id);
-- convention, not declared: control.partner_commission_line.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS partner_commission_line_legal_entity_id_idx ON control.partner_commission_line (legal_entity_id);
-- convention, not declared: control.partner_commission_line.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS partner_commission_line_order_id_idx ON control.partner_commission_line (order_id);
-- convention, not declared: control.partner_commission_line.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_commission_line_partner_id_idx ON control.partner_commission_line (partner_id);
-- convention, not declared: control.partner_commission_line.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS partner_commission_line_product_id_idx ON control.partner_commission_line (product_id);
-- convention, not declared: control.partner_commission_line.settlement_batch_id -> control.partner_settlement_batch
CREATE INDEX IF NOT EXISTS partner_commission_line_settlement_batch_id_idx ON control.partner_commission_line (settlement_batch_id);
-- convention, not declared: control.partner_commission_rule.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_commission_rule_agreement_id_idx ON control.partner_commission_rule (agreement_id);
-- convention, not declared: control.partner_commission_rule.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_commission_rule_approval_request_id_idx ON control.partner_commission_rule (approval_request_id);
-- convention, not declared: control.partner_commission_rule.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS partner_commission_rule_event_id_idx ON control.partner_commission_rule (event_id);
-- convention, not declared: control.partner_commission_rule.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_commission_rule_partner_id_idx ON control.partner_commission_rule (partner_id);
-- convention, not declared: control.partner_commission_rule.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS partner_commission_rule_product_id_idx ON control.partner_commission_rule (product_id);
-- convention, not declared: control.partner_commission_rule.venue_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS partner_commission_rule_venue_id_idx ON control.partner_commission_rule (venue_id);
-- convention, not declared: control.partner_contact.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_contact_partner_id_idx ON control.partner_contact (partner_id);
-- convention, not declared: control.partner_contact.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_contact_principal_id_idx ON control.partner_contact (principal_id);
-- convention, not declared: control.partner_credit_profile.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_credit_profile_agreement_id_idx ON control.partner_credit_profile (agreement_id);
-- convention, not declared: control.partner_credit_profile.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_credit_profile_approval_request_id_idx ON control.partner_credit_profile (approval_request_id);
-- convention, not declared: control.partner_credit_profile.credit_owner_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_credit_profile_credit_owner_principal_id_idx ON control.partner_credit_profile (credit_owner_principal_id);
-- convention, not declared: control.partner_credit_profile.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_credit_profile_partner_id_idx ON control.partner_credit_profile (partner_id);
-- convention, not declared: control.partner_distribution_right.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS partner_distribution_right_event_id_idx ON control.partner_distribution_right (event_id);
-- convention, not declared: control.partner_distribution_right.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_distribution_right_partner_id_idx ON control.partner_distribution_right (partner_id);
-- convention, not declared: control.partner_distribution_right.venue_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS partner_distribution_right_venue_id_idx ON control.partner_distribution_right (venue_id);
-- convention, not declared: control.partner_document.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_document_agreement_id_idx ON control.partner_document (agreement_id);
-- convention, not declared: control.partner_document.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_document_partner_id_idx ON control.partner_document (partner_id);
-- convention, not declared: control.partner_document.verified_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_document_verified_by_principal_id_idx ON control.partner_document (verified_by_principal_id);
-- convention, not declared: control.partner_rate.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_rate_agreement_id_idx ON control.partner_rate (agreement_id);
-- convention, not declared: control.partner_rate.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_rate_approval_request_id_idx ON control.partner_rate (approval_request_id);
-- convention, not declared: control.partner_rate.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS partner_rate_event_id_idx ON control.partner_rate (event_id);
-- convention, not declared: control.partner_rate.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_rate_partner_id_idx ON control.partner_rate (partner_id);
-- convention, not declared: control.partner_rate.pricing_profile_id -> rental.pricing_profile
CREATE INDEX IF NOT EXISTS partner_rate_pricing_profile_id_idx ON control.partner_rate (pricing_profile_id);
-- convention, not declared: control.partner_rate.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS partner_rate_product_id_idx ON control.partner_rate (product_id);
-- convention, not declared: control.partner_rate.venue_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS partner_rate_venue_id_idx ON control.partner_rate (venue_id);
-- convention, not declared: control.partner_reconciliation_exception.assignee_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_reconciliation_exception_assignee_principal_id_idx ON control.partner_reconciliation_exception (assignee_principal_id);
-- convention, not declared: control.partner_reconciliation_exception.order_id -> orders.sales_order
CREATE INDEX IF NOT EXISTS partner_reconciliation_exception_order_id_idx ON control.partner_reconciliation_exception (order_id);
-- convention, not declared: control.partner_reconciliation_exception.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_reconciliation_exception_partner_id_idx ON control.partner_reconciliation_exception (partner_id);
-- convention, not declared: control.partner_scope_assignment.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_scope_assignment_partner_id_idx ON control.partner_scope_assignment (partner_id);
-- convention, not declared: control.partner_scope_assignment.venue_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS partner_scope_assignment_venue_id_idx ON control.partner_scope_assignment (venue_id);
-- convention, not declared: control.partner_security.agreement_id -> control.partner_agreement
CREATE INDEX IF NOT EXISTS partner_security_agreement_id_idx ON control.partner_security (agreement_id);
-- convention, not declared: control.partner_security.document_id -> control.partner_document
CREATE INDEX IF NOT EXISTS partner_security_document_id_idx ON control.partner_security (document_id);
-- convention, not declared: control.partner_security.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_security_partner_id_idx ON control.partner_security (partner_id);
-- convention, not declared: control.partner_settlement_batch.legal_entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS partner_settlement_batch_legal_entity_id_idx ON control.partner_settlement_batch (legal_entity_id);
-- convention, not declared: control.partner_settlement_batch.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_settlement_batch_partner_id_idx ON control.partner_settlement_batch (partner_id);
-- convention, not declared: control.partner_status_history.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_status_history_approval_request_id_idx ON control.partner_status_history (approval_request_id);
-- convention, not declared: control.partner_status_history.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_status_history_partner_id_idx ON control.partner_status_history (partner_id);
-- convention, not declared: control.partner_status_history.requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_status_history_requested_by_principal_id_idx ON control.partner_status_history (requested_by_principal_id);
-- convention, not declared: control.release.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS release_created_by_principal_id_idx ON control.release (created_by_principal_id);
-- convention, not declared: control.rollout.reinventory_hold_id -> wallet.hold
CREATE INDEX IF NOT EXISTS rollout_reinventory_hold_id_idx ON control.rollout (reinventory_hold_id);
-- convention, not declared: control.rollout_cell.rollout_id -> control.rollout
CREATE INDEX IF NOT EXISTS rollout_cell_rollout_id_idx ON control.rollout_cell (rollout_id);
-- convention, not declared: control.rollout_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS rollout_tenant_cell_id_idx ON control.rollout_tenant (cell_id);
-- convention, not declared: control.rollout_tenant.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS rollout_tenant_tenant_id_idx ON control.rollout_tenant (tenant_id);
-- convention, not declared: control.sandbox.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS sandbox_developer_id_idx ON control.sandbox (developer_id);
-- convention, not declared: control.scaling_policy.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS scaling_policy_cell_id_idx ON control.scaling_policy (cell_id);
-- convention, not declared: control.tenant.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS tenant_region_id_idx ON control.tenant (region_id);
-- convention, not declared: control.tenant.termination_requested_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS tenant_termination_requested_by_principal_id_idx ON control.tenant (termination_requested_by_principal_id);
-- convention, not declared: control.tenant_migration.from_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS tenant_migration_from_cell_id_idx ON control.tenant_migration (from_cell_id);
-- convention, not declared: control.tenant_migration.to_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS tenant_migration_to_cell_id_idx ON control.tenant_migration (to_cell_id);
-- convention, not declared: control.tenant_migration_plan.from_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS tenant_migration_plan_from_cell_id_idx ON control.tenant_migration_plan (from_cell_id);
-- convention, not declared: control.tenant_migration_plan.to_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS tenant_migration_plan_to_cell_id_idx ON control.tenant_migration_plan (to_cell_id);
-- convention, not declared: control.upgrade_schedule.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS upgrade_schedule_tenant_id_idx ON control.upgrade_schedule (tenant_id);
-- convention, not declared: control.waf_rule.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS waf_rule_cell_id_idx ON control.waf_rule (cell_id);
-- convention, not declared: control.webhook_delivery.subscription_id -> control.webhook_subscription
CREATE INDEX IF NOT EXISTS webhook_delivery_subscription_id_idx ON control.webhook_delivery (subscription_id);
-- convention, not declared: control.webhook_subscription.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS webhook_subscription_client_id_idx ON control.webhook_subscription (client_id);
-- crosses the database boundary: control.cell.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS cell_region_id_idx ON control.cell (region_id);
-- crosses the database boundary: control.cell_cluster.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS cell_cluster_region_id_idx ON control.cell_cluster (region_id);
-- crosses the database boundary: control.channel_listing.price_list_id -> catalogue.price_list
CREATE INDEX IF NOT EXISTS channel_listing_price_list_id_idx ON control.channel_listing (price_list_id);
-- crosses the database boundary: control.channel_listing.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS channel_listing_product_id_idx ON control.channel_listing (product_id);
-- crosses the database boundary: control.migration_run.started_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS migration_run_started_by_principal_id_idx ON control.migration_run (started_by_principal_id);
-- crosses the database boundary: control.partner_agreement.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS partner_agreement_approval_request_id_idx ON control.partner_agreement (approval_request_id);
-- crosses the database boundary: control.partner_case.sla_policy_id -> approvals.sla_policy
CREATE INDEX IF NOT EXISTS partner_case_sla_policy_id_idx ON control.partner_case (sla_policy_id);
-- crosses the database boundary: control.partner_user.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS partner_user_principal_id_idx ON control.partner_user (principal_id);
-- crosses the database boundary: control.rollout.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS rollout_approved_by_principal_id_idx ON control.rollout (approved_by_principal_id);
-- crosses the database boundary: control.rollout.started_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS rollout_started_by_principal_id_idx ON control.rollout (started_by_principal_id);
-- crosses the database boundary: control.support_notice.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS support_notice_published_by_principal_id_idx ON control.support_notice (published_by_principal_id);
-- crosses the database boundary: control.tenant.account_manager_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS tenant_account_manager_principal_id_idx ON control.tenant (account_manager_principal_id);
-- crosses the database boundary: control.tenant.subscription_id -> subscription.contract
CREATE INDEX IF NOT EXISTS tenant_subscription_id_idx ON control.tenant (subscription_id);
-- crosses the database boundary: control.usage_record.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS usage_record_venue_id_idx ON control.usage_record (venue_id);
-- declared: control.api_licence.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS api_licence_tenant_id_idx ON control.api_licence (tenant_id);
-- declared: control.cell_job.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS cell_job_cell_id_idx ON control.cell_job (cell_id);
-- declared: control.credit_note_line.credit_note_id -> control.credit_note
CREATE INDEX IF NOT EXISTS credit_note_line_credit_note_id_idx ON control.credit_note_line (credit_note_id);
-- declared: control.environment.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS environment_cell_id_idx ON control.environment (cell_id);
-- declared: control.invoice_line.invoice_id -> control.invoice
CREATE INDEX IF NOT EXISTS invoice_line_invoice_id_idx ON control.invoice_line (invoice_id);
-- declared: control.licence_add_on_limit.licence_add_on_id -> control.licence_add_on
CREATE INDEX IF NOT EXISTS licence_add_on_limit_licence_add_on_id_idx ON control.licence_add_on_limit (licence_add_on_id);
-- declared: control.migration.release_id -> control.release
CREATE INDEX IF NOT EXISTS migration_release_id_idx ON control.migration (release_id);
-- declared: control.migration_plan_cell.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS migration_plan_cell_cell_id_idx ON control.migration_plan_cell (cell_id);
-- declared: control.migration_plan_cell.migration_plan_id -> control.migration_plan
CREATE INDEX IF NOT EXISTS migration_plan_cell_migration_plan_id_idx ON control.migration_plan_cell (migration_plan_id);
-- declared: control.migration_run.canary_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS migration_run_canary_cell_id_idx ON control.migration_run (canary_cell_id);
-- declared: control.migration_run_cell.migration_run_id -> control.migration_run
CREATE INDEX IF NOT EXISTS migration_run_cell_migration_run_id_idx ON control.migration_run_cell (migration_run_id);
-- declared: control.migration_run_tenant.migration_run_id -> control.migration_run
CREATE INDEX IF NOT EXISTS migration_run_tenant_migration_run_id_idx ON control.migration_run_tenant (migration_run_id);
-- declared: control.onboarding_application.venue_type_template_id -> control.venue_type_template
CREATE INDEX IF NOT EXISTS onboarding_application_venue_type_template_id_idx ON control.onboarding_application (venue_type_template_id);
-- declared: control.partner_agreement.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_agreement_partner_id_idx ON control.partner_agreement (partner_id);
-- declared: control.partner_application_review_task.partner_application_id -> control.partner_application
CREATE INDEX IF NOT EXISTS partner_application_review_task_partner_application_id_idx ON control.partner_application_review_task (partner_application_id);
-- declared: control.partner_commission_rule_tier.partner_commission_rule_id -> control.partner_commission_rule
CREATE INDEX IF NOT EXISTS partner_commission_rule_tier_partner_commission_rule_id_idx ON control.partner_commission_rule_tier (partner_commission_rule_id);
-- declared: control.partner_rate_volume_band.partner_rate_id -> control.partner_rate
CREATE INDEX IF NOT EXISTS partner_rate_volume_band_partner_rate_id_idx ON control.partner_rate_volume_band (partner_rate_id);
-- declared: control.partner_user.partner_id -> control.partner
CREATE INDEX IF NOT EXISTS partner_user_partner_id_idx ON control.partner_user (partner_id);
-- declared: control.release_component.release_id -> control.release
CREATE INDEX IF NOT EXISTS release_component_release_id_idx ON control.release_component (release_id);
-- declared: control.rollout.release_id -> control.release
CREATE INDEX IF NOT EXISTS rollout_release_id_idx ON control.rollout (release_id);
-- declared: control.rollout_cell.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS rollout_cell_cell_id_idx ON control.rollout_cell (cell_id);
-- declared: control.tenant_migration.plan_id -> control.tenant_migration_plan
CREATE INDEX IF NOT EXISTS tenant_migration_plan_id_idx ON control.tenant_migration (plan_id);
-- declared: control.tenant_migration.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS tenant_migration_tenant_id_idx ON control.tenant_migration (tenant_id);
-- declared: control.tenant_migration_plan.tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS tenant_migration_plan_tenant_id_idx ON control.tenant_migration_plan (tenant_id);
CREATE INDEX IF NOT EXISTS channel_listing_scope_path_idx ON control.channel_listing USING gist (scope_path);
CREATE INDEX IF NOT EXISTS content_block_scope_path_idx ON control.content_block USING gist (scope_path);
CREATE INDEX IF NOT EXISTS migration_plan_scope_path_idx ON control.migration_plan USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_agreement_scope_path_idx ON control.partner_agreement USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_allocation_scope_path_idx ON control.partner_allocation USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_application_scope_path_idx ON control.partner_application USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_billing_profile_scope_path_idx ON control.partner_billing_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_booking_limit_scope_path_idx ON control.partner_booking_limit USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_capability_grant_scope_path_idx ON control.partner_capability_grant USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_case_scope_path_idx ON control.partner_case USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_change_request_scope_path_idx ON control.partner_change_request USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_commercial_exception_scope_path_idx ON control.partner_commercial_exception USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_commission_line_scope_path_idx ON control.partner_commission_line USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_commission_rule_scope_path_idx ON control.partner_commission_rule USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_contact_scope_path_idx ON control.partner_contact USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_credit_profile_scope_path_idx ON control.partner_credit_profile USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_distribution_right_scope_path_idx ON control.partner_distribution_right USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_document_scope_path_idx ON control.partner_document USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_rate_scope_path_idx ON control.partner_rate USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_reconciliation_exception_scope_path_idx ON control.partner_reconciliation_exception USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_scope_assignment_scope_path_idx ON control.partner_scope_assignment USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_scope_path_idx ON control.partner USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_security_scope_path_idx ON control.partner_security USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_settlement_batch_scope_path_idx ON control.partner_settlement_batch USING gist (scope_path);
CREATE INDEX IF NOT EXISTS partner_status_history_scope_path_idx ON control.partner_status_history USING gist (scope_path);
CREATE INDEX IF NOT EXISTS seo_metadata_scope_path_idx ON control.seo_metadata USING gist (scope_path);
CREATE INDEX IF NOT EXISTS support_notice_scope_path_idx ON control.support_notice USING gist (scope_path);
CREATE INDEX IF NOT EXISTS url_redirect_scope_path_idx ON control.url_redirect USING gist (scope_path);
