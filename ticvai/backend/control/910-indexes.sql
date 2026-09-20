-- Conventions and scope paths in the control database.
-- **A convention is indexed and not constrained** (ADR-0011): most references are
-- naming habits the contracts never asserted, and enforcing one fails on the first
-- row that legitimately points nowhere.

-- convention, not declared: control.api_client.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS ix_api_client_client_id ON control.api_client (client_id);
-- convention, not declared: control.api_client.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS ix_api_client_developer_id ON control.api_client (developer_id);
-- convention, not declared: control.api_limit.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS ix_api_limit_client_id ON control.api_limit (client_id);
-- convention, not declared: control.archival_job.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_archival_job_cell_id ON control.archival_job (cell_id);
-- convention, not declared: control.backup_run.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_backup_run_cell_id ON control.backup_run (cell_id);
-- convention, not declared: control.burst_environment.performance_id -> catalogue.performance
CREATE INDEX IF NOT EXISTS ix_burst_environment_performance_id ON control.burst_environment (performance_id);
-- convention, not declared: control.burst_environment.usage_record_id -> control.usage_record
CREATE INDEX IF NOT EXISTS ix_burst_environment_usage_record_id ON control.burst_environment (usage_record_id);
-- convention, not declared: control.cell.cluster_id -> control.cell_cluster
CREATE INDEX IF NOT EXISTS ix_cell_cluster_id ON control.cell (cluster_id);
-- convention, not declared: control.cell_cluster.modelled_on_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_cluster_modelled_on_cell_id ON control.cell_cluster (modelled_on_cell_id);
-- convention, not declared: control.cell_instance.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_instance_cell_id ON control.cell_instance (cell_id);
-- convention, not declared: control.cell_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_cell_tenant_cell_id ON control.cell_tenant (cell_id);
-- convention, not declared: control.cell_tenant.instance_id -> control.cell_instance
CREATE INDEX IF NOT EXISTS ix_cell_tenant_instance_id ON control.cell_tenant (instance_id);
-- convention, not declared: control.cell_tenant.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_cell_tenant_tenant_id ON control.cell_tenant (tenant_id);
-- convention, not declared: control.content_block.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_content_block_approved_by_principal_id ON control.content_block (approved_by_principal_id);
-- convention, not declared: control.content_block.audience_segment_id -> marketing.segment
CREATE INDEX IF NOT EXISTS ix_content_block_audience_segment_id ON control.content_block (audience_segment_id);
-- convention, not declared: control.content_block.page_id -> whitelabel.content_page
CREATE INDEX IF NOT EXISTS ix_content_block_page_id ON control.content_block (page_id);
-- convention, not declared: control.integration_listing.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS ix_integration_listing_developer_id ON control.integration_listing (developer_id);
-- convention, not declared: control.migration_run.canary_tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_migration_run_canary_tenant_id ON control.migration_run (canary_tenant_id);
-- convention, not declared: control.migration_run_cell.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_migration_run_cell_cell_id ON control.migration_run_cell (cell_id);
-- convention, not declared: control.migration_run_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_migration_run_tenant_cell_id ON control.migration_run_tenant (cell_id);
-- convention, not declared: control.migration_run_tenant.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_migration_run_tenant_tenant_id ON control.migration_run_tenant (tenant_id);
-- convention, not declared: control.onboarding_application.provisioned_tenant_id -> control.tenant
CREATE INDEX IF NOT EXISTS ix_onboarding_application_provisioned_tenant_id ON control.onboarding_application (provisioned_tenant_id);
-- convention, not declared: control.onboarding_application.requested_plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS ix_onboarding_application_requested_plan_id ON control.onboarding_application (requested_plan_id);
-- convention, not declared: control.partner_agreement.accepted_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_partner_agreement_accepted_by_principal_id ON control.partner_agreement (accepted_by_principal_id);
-- convention, not declared: control.partner_agreement.branding_asset_id -> assets.media_asset
CREATE INDEX IF NOT EXISTS ix_partner_agreement_branding_asset_id ON control.partner_agreement (branding_asset_id);
-- convention, not declared: control.release.created_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_release_created_by_principal_id ON control.release (created_by_principal_id);
-- convention, not declared: control.rollout.reinventory_hold_id -> wallet.hold
CREATE INDEX IF NOT EXISTS ix_rollout_reinventory_hold_id ON control.rollout (reinventory_hold_id);
-- convention, not declared: control.rollout_tenant.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_rollout_tenant_cell_id ON control.rollout_tenant (cell_id);
-- convention, not declared: control.rollout_tenant.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_rollout_tenant_tenant_id ON control.rollout_tenant (tenant_id);
-- convention, not declared: control.sandbox.developer_id -> control.developer_account
CREATE INDEX IF NOT EXISTS ix_sandbox_developer_id ON control.sandbox (developer_id);
-- convention, not declared: control.scaling_policy.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_scaling_policy_cell_id ON control.scaling_policy (cell_id);
-- convention, not declared: control.seo_metadata.entity_id -> ledger.legal_entity
CREATE INDEX IF NOT EXISTS ix_seo_metadata_entity_id ON control.seo_metadata (entity_id);
-- convention, not declared: control.tenant_migration.from_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_tenant_migration_from_cell_id ON control.tenant_migration (from_cell_id);
-- convention, not declared: control.tenant_migration.to_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_tenant_migration_to_cell_id ON control.tenant_migration (to_cell_id);
-- convention, not declared: control.tenant_migration_plan.from_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_tenant_migration_plan_from_cell_id ON control.tenant_migration_plan (from_cell_id);
-- convention, not declared: control.tenant_migration_plan.to_cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_tenant_migration_plan_to_cell_id ON control.tenant_migration_plan (to_cell_id);
-- convention, not declared: control.waf_rule.cell_id -> control.cell
CREATE INDEX IF NOT EXISTS ix_waf_rule_cell_id ON control.waf_rule (cell_id);
-- convention, not declared: control.webhook_subscription.client_id -> control.api_client
CREATE INDEX IF NOT EXISTS ix_webhook_subscription_client_id ON control.webhook_subscription (client_id);
-- crosses the database boundary: control.cell.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS ix_cell_region_id ON control.cell (region_id);
-- crosses the database boundary: control.cell_cluster.region_id -> platform.scope
CREATE INDEX IF NOT EXISTS ix_cell_cluster_region_id ON control.cell_cluster (region_id);
-- crosses the database boundary: control.channel_listing.price_list_id -> catalogue.price_list
CREATE INDEX IF NOT EXISTS ix_channel_listing_price_list_id ON control.channel_listing (price_list_id);
-- crosses the database boundary: control.channel_listing.product_id -> catalogue.product
CREATE INDEX IF NOT EXISTS ix_channel_listing_product_id ON control.channel_listing (product_id);
-- crosses the database boundary: control.invoice.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_invoice_tenant_id ON control.invoice (tenant_id);
-- crosses the database boundary: control.licence_add_on.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS ix_licence_add_on_plan_id ON control.licence_add_on (plan_id);
-- crosses the database boundary: control.migration_run.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS ix_migration_run_plan_id ON control.migration_run (plan_id);
-- crosses the database boundary: control.migration_run.started_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_migration_run_started_by_principal_id ON control.migration_run (started_by_principal_id);
-- crosses the database boundary: control.partner_agreement.approval_request_id -> approvals.request
CREATE INDEX IF NOT EXISTS ix_partner_agreement_approval_request_id ON control.partner_agreement (approval_request_id);
-- crosses the database boundary: control.partner_agreement.partner_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_partner_agreement_partner_id ON control.partner_agreement (partner_id);
-- crosses the database boundary: control.partner_user.principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_partner_user_principal_id ON control.partner_user (principal_id);
-- crosses the database boundary: control.release.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS ix_release_plan_id ON control.release (plan_id);
-- crosses the database boundary: control.rollout.approved_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_rollout_approved_by_principal_id ON control.rollout (approved_by_principal_id);
-- crosses the database boundary: control.rollout.started_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_rollout_started_by_principal_id ON control.rollout (started_by_principal_id);
-- crosses the database boundary: control.support_notice.published_by_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_support_notice_published_by_principal_id ON control.support_notice (published_by_principal_id);
-- crosses the database boundary: control.tenant.account_manager_principal_id -> identity.principal
CREATE INDEX IF NOT EXISTS ix_tenant_account_manager_principal_id ON control.tenant (account_manager_principal_id);
-- crosses the database boundary: control.tenant.plan_id -> subscription.plan
CREATE INDEX IF NOT EXISTS ix_tenant_plan_id ON control.tenant (plan_id);
-- crosses the database boundary: control.tenant.subscription -> subscription.contract
CREATE INDEX IF NOT EXISTS ix_tenant_subscription ON control.tenant (subscription);
-- crosses the database boundary: control.upgrade_schedule.tenant_id -> platform.tenant
CREATE INDEX IF NOT EXISTS ix_upgrade_schedule_tenant_id ON control.upgrade_schedule (tenant_id);
-- crosses the database boundary: control.usage_record.venue_id -> platform.scope
CREATE INDEX IF NOT EXISTS ix_usage_record_venue_id ON control.usage_record (venue_id);
-- crosses the database boundary: control.webhook_delivery.event_id -> catalogue.event
CREATE INDEX IF NOT EXISTS ix_webhook_delivery_event_id ON control.webhook_delivery (event_id);
-- crosses the database boundary: control.webhook_delivery.subscription_id -> subscription.contract
CREATE INDEX IF NOT EXISTS ix_webhook_delivery_subscription_id ON control.webhook_delivery (subscription_id);
CREATE INDEX IF NOT EXISTS ix_channel_listing_scope ON control.channel_listing (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_content_block_scope ON control.content_block (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_footer_config_scope ON control.footer_config (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_migration_plan_scope ON control.migration_plan (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_seo_metadata_scope ON control.seo_metadata (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_support_notice_scope ON control.support_notice (scope_path text_pattern_ops);
CREATE INDEX IF NOT EXISTS ix_url_redirect_scope ON control.url_redirect (scope_path text_pattern_ops);
