"""Generated. The declared reads and writes of each operation."""

READS = {
 "addLicenceAddOn": [
  "SELECT * FROM control.licence_add_on LIMIT 50"
 ],
 "applyMigration": [
  "SELECT * FROM control.migration_run LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "cancelDecommission": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "cancelInvoice": [
  "SELECT * FROM control.invoice LIMIT 50"
 ],
 "cancelSubscription": [
  "SELECT * FROM control.subscription LIMIT 50",
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "certifyIntegration": [
  "SELECT * FROM control.api_version LIMIT 50",
  "SELECT * FROM control.integration_listing LIMIT 50"
 ],
 "createApiClient": [
  "SELECT * FROM control.api_licence LIMIT 50",
  "SELECT * FROM control.developer_account LIMIT 50"
 ],
 "createPartnerAgreement": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM platform.tenant LIMIT 50"
 ],
 "createPartnerQuote": [
  "SELECT * FROM subscription.partner_quote LIMIT 50"
 ],
 "createPartnerUser": [
  "SELECT * FROM control.partner_agreement LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM platform.org_unit LIMIT 50"
 ],
 "createPlan": [
  "SELECT * FROM control.subscription_plan LIMIT 50"
 ],
 "createPlanVersion": [
  "SELECT * FROM control.subscription_plan LIMIT 50"
 ],
 "createRelease": [
  "SELECT * FROM control.release LIMIT 50"
 ],
 "createSandbox": [
  "SELECT * FROM control.developer_account LIMIT 50"
 ],
 "createTenant": [
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "createWebhookSubscription": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "decommissionCell": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "deprecateApiVersion": [
  "SELECT * FROM control.api_client LIMIT 50",
  "SELECT * FROM control.api_version LIMIT 50"
 ],
 "disputeInvoice": [
  "SELECT * FROM control.invoice LIMIT 50"
 ],
 "executeTenantMigration": [
  "SELECT * FROM control.tenant_migration LIMIT 50"
 ],
 "exportPartnerInvoice": [
  "SELECT * FROM control.partner_agreement LIMIT 50",
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM ledger.legal_entity WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "generateInvoice": [
  "SELECT * FROM control.invoice LIMIT 50"
 ],
 "getApiUsage": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "getCell": [
  "SELECT * FROM control.cell LIMIT 50",
  "SELECT * FROM control.cell_job LIMIT 50"
 ],
 "getCellCapacity": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "getCellHealth": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "getCommissionStatement": [
  "SELECT * FROM control.partner_agreement LIMIT 50",
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.refund LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getEntitlementUsage": [
  "SELECT * FROM access.entitlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM control.licence_add_on LIMIT 50",
  "SELECT * FROM control.usage_record LIMIT 50"
 ],
 "getMigrationRun": [
  "SELECT * FROM control.migration_run LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "getPlan": [
  "SELECT * FROM control.subscription_plan LIMIT 50"
 ],
 "getRelease": [
  "SELECT * FROM control.rollout LIMIT 50"
 ],
 "getReleaseReadiness": [
  "SELECT * FROM control.release LIMIT 50"
 ],
 "getRollout": [
  "SELECT * FROM control.rollout LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "getScalingPolicy": [
  "SELECT * FROM control.scaling_policy LIMIT 50"
 ],
 "getSubscription": [
  "SELECT * FROM control.subscription LIMIT 50"
 ],
 "getTenant": [
  "SELECT * FROM control.cell LIMIT 50",
  "SELECT * FROM control.subscription LIMIT 50",
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "getTenantLicences": [
  "SELECT * FROM control.licence_add_on LIMIT 50",
  "SELECT * FROM control.subscription_plan LIMIT 50",
  "SELECT * FROM control.subscription LIMIT 50"
 ],
 "getUsageMetering": [
  "SELECT * FROM control.subscription LIMIT 50",
  "SELECT * FROM control.usage_record LIMIT 50"
 ],
 "getVersionSkew": [
  "SELECT * FROM control.migration LIMIT 50"
 ],
 "issueApiToken": [
  "SELECT * FROM control.api_client LIMIT 50",
  "SELECT * FROM control.api_licence LIMIT 50"
 ],
 "launchCellCluster": [
  "SELECT * FROM control.cell_cluster LIMIT 50"
 ],
 "listApiClients": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "listApiVersions": [
  "SELECT * FROM control.api_version LIMIT 50"
 ],
 "listArchivalJobs": [
  "SELECT * FROM control.archival_job LIMIT 50"
 ],
 "listBackupRuns": [
  "SELECT * FROM control.backup_run LIMIT 50"
 ],
 "listBurstEnvironments": [
  "SELECT * FROM catalogue.performance LIMIT 50"
 ],
 "listCellClusters": [
  "SELECT * FROM control.cell_cluster LIMIT 50"
 ],
 "listCellJobs": [
  "SELECT * FROM control.cell_job LIMIT 50"
 ],
 "listChannelListings": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM control.channel_listing WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listDeadLetters": [
  "SELECT * FROM platform.dead_letter WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM platform.outbox WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listEnvironments": [
  "SELECT * FROM control.environment LIMIT 50"
 ],
 "listIntegrationListings": [
  "SELECT * FROM control.integration_listing LIMIT 50"
 ],
 "listMigrations": [
  "SELECT * FROM control.migration LIMIT 50"
 ],
 "listPartnerAgreements": [
  "SELECT * FROM control.partner_agreement LIMIT 50"
 ],
 "listPartnerQuotes": [
  "SELECT * FROM subscription.partner_quote LIMIT 50"
 ],
 "listPartnerUsers": [
  "SELECT * FROM control.partner_user LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "listPlans": [
  "SELECT * FROM control.subscription_plan LIMIT 50"
 ],
 "listReleases": [
  "SELECT * FROM control.release LIMIT 50"
 ],
 "listRollouts": [
  "SELECT * FROM control.rollout LIMIT 50"
 ],
 "listSandboxes": [
  "SELECT * FROM control.sandbox LIMIT 50"
 ],
 "listSubscriptionInvoices": [
  "SELECT * FROM control.invoice LIMIT 50"
 ],
 "listSupportNotices": [
  "SELECT * FROM control.support_notice WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listTenantCells": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "listTenantMigrations": [
  "SELECT * FROM control.tenant_migration LIMIT 50"
 ],
 "listTenants": [
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "listUpgradeSchedules": [
  "SELECT * FROM control.upgrade_schedule LIMIT 50"
 ],
 "listVenueTypeTemplates": [
  "SELECT * FROM control.venue_type_template LIMIT 50"
 ],
 "listWafRules": [
  "SELECT * FROM control.waf_rule LIMIT 50"
 ],
 "listWebhookDeliveries": [
  "SELECT * FROM control.webhook_delivery LIMIT 50"
 ],
 "listWebhookSubscriptions": [
  "SELECT * FROM control.webhook_subscription LIMIT 50"
 ],
 "pauseRollout": [
  "SELECT * FROM control.rollout LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "planMigration": [
  "SELECT * FROM control.migration_plan WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "planTenantMigration": [
  "SELECT * FROM control.tenant_migration_plan LIMIT 50"
 ],
 "previewSubscriptionChange": [
  "SELECT * FROM control.subscription_plan LIMIT 50",
  "SELECT * FROM control.subscription LIMIT 50",
  "SELECT * FROM platform.tenant LIMIT 50"
 ],
 "promoteRelease": [
  "SELECT * FROM control.rollout LIMIT 50"
 ],
 "provisionCell": [
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "publishSupportNotice": [
  "SELECT * FROM control.support_notice WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "reactivateTenant": [
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "reconcileBurstEnvironment": [
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recordInvoicePayment": [
  "SELECT * FROM control.invoice LIMIT 50",
  "SELECT * FROM ledger.fx_rate LIMIT 50"
 ],
 "recordUsage": [
  "SELECT * FROM ai.interaction WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM control.usage_record LIMIT 50"
 ],
 "registerDeveloper": [
  "SELECT * FROM control.developer_account LIMIT 50"
 ],
 "registerEnvironment": [
  "SELECT * FROM control.environment LIMIT 50"
 ],
 "rejectRelease": [
  "SELECT * FROM control.release LIMIT 50"
 ],
 "removeLicenceAddOn": [
  "SELECT * FROM control.licence_add_on LIMIT 50"
 ],
 "replayDeadLetter": [
  "SELECT * FROM platform.dead_letter WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "replayEvents": [
  "SELECT * FROM control.webhook_subscription LIMIT 50",
  "SELECT * FROM platform.outbox WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "requestBurstEnvironment": [
  "SELECT * FROM catalogue.performance LIMIT 50",
  "SELECT * FROM control.cell LIMIT 50"
 ],
 "resetSandbox": [
  "SELECT * FROM control.sandbox LIMIT 50"
 ],
 "resolveInvoiceDispute": [
  "SELECT * FROM control.invoice LIMIT 50"
 ],
 "revokeApiCredential": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "rollbackMigrationRun": [
  "SELECT * FROM control.migration_run LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "rollbackRollout": [
  "SELECT * FROM control.rollout LIMIT 50",
  "SELECT * FROM control.rollout_cell LIMIT 50"
 ],
 "rollbackTenantMigration": [
  "SELECT * FROM control.tenant_migration LIMIT 50"
 ],
 "rotateApiCredential": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "scheduleTenantUpgrade": [
  "SELECT * FROM control.upgrade_schedule LIMIT 50"
 ],
 "setApiLicensing": [
  "SELECT * FROM control.api_licence LIMIT 50"
 ],
 "setApiQuota": [
  "SELECT * FROM control.api_client LIMIT 50"
 ],
 "setChannelListing": [
  "SELECT * FROM catalogue.channel_capacity LIMIT 50",
  "SELECT * FROM catalogue.price_list LIMIT 50",
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setDeveloperMembers": [
  "SELECT * FROM control.developer_account LIMIT 50",
  "SELECT * FROM identity.principal LIMIT 50"
 ],
 "setScalingPolicy": [
  "SELECT * FROM control.scaling_policy LIMIT 50"
 ],
 "setSubscription": [
  "SELECT * FROM control.subscription LIMIT 50"
 ],
 "setWafPolicy": [
  "SELECT * FROM control.waf_rule LIMIT 50"
 ],
 "settleAiUsage": [
  "SELECT * FROM ai.interaction WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM control.subscription_plan LIMIT 50",
  "SELECT * FROM control.subscription LIMIT 50"
 ],
 "skipRolloutCell": [
  "SELECT * FROM control.rollout LIMIT 50"
 ],
 "startRollout": [
  "SELECT * FROM control.rollout LIMIT 50"
 ],
 "submitIntegrationListing": [
  "SELECT * FROM control.developer_account LIMIT 50"
 ],
 "submitOnboardingApplication": [
  "SELECT * FROM control.subscription_plan LIMIT 50",
  "SELECT * FROM control.venue_type_template LIMIT 50"
 ],
 "suspendTenant": [
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "terminateTenant": [
  "SELECT * FROM control.subscription LIMIT 50",
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "updateCellTier": [
  "SELECT * FROM control.cell_job LIMIT 50"
 ],
 "updatePartnerAgreement": [
  "SELECT * FROM control.partner_agreement LIMIT 50",
  "SELECT * FROM ledger.fx_rate LIMIT 50"
 ],
 "updateTenant": [
  "SELECT * FROM control.tenant LIMIT 50"
 ],
 "withdrawRelease": [
  "SELECT * FROM control.release LIMIT 50"
 ]
}

WRITES = {
 "addLicenceAddOn": [
  "SELECT id FROM control.licence_add_on ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "applyMigration": [
  "SELECT id FROM control.migration_run ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.rollout_cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelDecommission": [
  "SELECT id FROM control.cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelInvoice": [
  "SELECT id FROM control.invoice ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelSubscription": [
  "SELECT id FROM control.subscription ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "certifyIntegration": [
  "SELECT id FROM control.integration_listing ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createApiClient": [
  "SELECT id FROM control.api_client ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPartnerAgreement": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.partner_agreement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPartnerQuote": [
  "SELECT id FROM subscription.partner_quote ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPartnerUser": [
  "SELECT id FROM control.partner_user ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPlan": [
  "SELECT id FROM control.subscription_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createPlanVersion": [
  "SELECT id FROM control.subscription_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRelease": [
  "SELECT id FROM control.release ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createSandbox": [
  "SELECT id FROM control.sandbox ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createTenant": [
  "SELECT id FROM control.tenant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createWebhookSubscription": [
  "SELECT id FROM control.webhook_subscription ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "decommissionBurstEnvironment": [
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "decommissionCell": [
  "SELECT id FROM control.cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deprecateApiVersion": [
  "SELECT id FROM control.api_version ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM marketing.message_dispatch ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "disputeInvoice": [
  "SELECT id FROM control.invoice ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "executeTenantMigration": [
  "SELECT id FROM control.tenant_migration ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "generateInvoice": [
  "SELECT id FROM control.invoice ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "launchCellCluster": [
  "SELECT id FROM control.cell_cluster ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "pauseRollout": [
  "SELECT id FROM control.rollout ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.rollout_cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "planMigration": [
  "SELECT id FROM control.migration_plan WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "planTenantMigration": [
  "SELECT id FROM control.tenant_migration_plan ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "promoteRelease": [
  "SELECT id FROM control.rollout ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "provisionCell": [
  "SELECT id FROM control.cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "publishSupportNotice": [
  "SELECT id FROM control.support_notice WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reactivateTenant": [
  "SELECT id FROM control.tenant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reconcileBurstEnvironment": [
  "SELECT id FROM orders.order_line ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM orders.payment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordInvoicePayment": [
  "SELECT id FROM control.invoice ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordUsage": [
  "SELECT id FROM control.usage_record ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerDeveloper": [
  "SELECT id FROM control.developer_account ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerEnvironment": [
  "SELECT id FROM control.environment ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "registerPartner": [
  "SELECT id FROM approvals.request WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.partner_agreement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rejectRelease": [
  "SELECT id FROM control.release ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "removeLicenceAddOn": [
  "SELECT id FROM control.licence_add_on ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.subscription ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "replayDeadLetter": [
  "SELECT id FROM platform.dead_letter WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "replayEvents": [
  "SELECT id FROM control.webhook_delivery ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resetSandbox": [
  "SELECT id FROM control.sandbox ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resolveInvoiceDispute": [
  "SELECT id FROM control.invoice ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "revokeApiCredential": [
  "SELECT id FROM control.api_client ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rollbackMigrationRun": [
  "SELECT id FROM control.migration_run ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.rollout_cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rollbackRollout": [
  "SELECT id FROM control.rollout ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.rollout_cell ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rollbackTenantMigration": [
  "SELECT id FROM control.tenant_migration ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rotateApiCredential": [
  "SELECT id FROM control.api_client ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "scheduleTenantUpgrade": [
  "SELECT id FROM control.upgrade_schedule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setApiLicensing": [
  "SELECT id FROM control.api_licence ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setApiQuota": [
  "SELECT id FROM control.api_quota ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setChannelListing": [
  "SELECT id FROM control.channel_listing WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setDeveloperMembers": [
  "SELECT id FROM control.developer_account ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM identity.delegated_access WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setScalingPolicy": [
  "SELECT id FROM control.scaling_policy ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setSubscription": [
  "SELECT id FROM control.subscription ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setWafPolicy": [
  "SELECT id FROM control.waf_rule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "settleAiUsage": [
  "SELECT id FROM control.usage_record ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "skipRolloutCell": [
  "SELECT id FROM control.rollout ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "startRollout": [
  "SELECT id FROM control.rollout ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitIntegrationListing": [
  "SELECT id FROM control.integration_listing ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "submitOnboardingApplication": [
  "SELECT id FROM control.onboarding_application ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "suspendTenant": [
  "SELECT id FROM control.tenant ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "terminateTenant": [
  "SELECT id FROM control.subscription ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM control.tenant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateCellTier": [
  "SELECT id FROM control.cell_job ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updatePartnerAgreement": [
  "SELECT id FROM control.partner_agreement ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateTenant": [
  "SELECT id FROM control.tenant ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "withdrawRelease": [
  "SELECT id FROM control.release ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "addLicenceAddOn": [
  "cache:idempotency:bench"
 ],
 "applyMigration": [
  "cache:idempotency:bench"
 ],
 "cancelDecommission": [
  "cache:idempotency:bench"
 ],
 "cancelInvoice": [
  "cache:idempotency:bench"
 ],
 "cancelSubscription": [
  "cache:idempotency:bench"
 ],
 "certifyIntegration": [
  "cache:idempotency:bench"
 ],
 "createApiClient": [
  "cache:idempotency:bench"
 ],
 "createPartnerAgreement": [
  "cache:idempotency:bench"
 ],
 "createPartnerUser": [
  "cache:idempotency:bench"
 ],
 "createPlan": [
  "cache:idempotency:bench"
 ],
 "createPlanVersion": [
  "cache:idempotency:bench"
 ],
 "createRelease": [
  "cache:idempotency:bench"
 ],
 "createSandbox": [
  "cache:idempotency:bench"
 ],
 "createTenant": [
  "cache:idempotency:bench"
 ],
 "createWebhookSubscription": [
  "cache:idempotency:bench"
 ],
 "decommissionBurstEnvironment": [
  "cache:idempotency:bench"
 ],
 "decommissionCell": [
  "cache:idempotency:bench"
 ],
 "deprecateApiVersion": [
  "cache:idempotency:bench"
 ],
 "disputeInvoice": [
  "cache:idempotency:bench"
 ],
 "drainBurstEnvironment": [
  "cache:idempotency:bench"
 ],
 "executeTenantMigration": [
  "cache:idempotency:bench"
 ],
 "exportPartnerInvoice": [
  "cache:idempotency:bench"
 ],
 "generateInvoice": [
  "cache:idempotency:bench"
 ],
 "launchCellCluster": [
  "cache:idempotency:bench"
 ],
 "pauseRollout": [
  "cache:idempotency:bench"
 ],
 "planMigration": [
  "cache:idempotency:bench"
 ],
 "planTenantMigration": [
  "cache:idempotency:bench"
 ],
 "previewSubscriptionChange": [
  "cache:idempotency:bench"
 ],
 "promoteRelease": [
  "cache:idempotency:bench"
 ],
 "provisionCell": [
  "cache:idempotency:bench"
 ],
 "publishSupportNotice": [
  "cache:idempotency:bench"
 ],
 "reactivateTenant": [
  "cache:idempotency:bench"
 ],
 "reconcileBurstEnvironment": [
  "cache:idempotency:bench"
 ],
 "recordInvoicePayment": [
  "cache:idempotency:bench"
 ],
 "recordUsage": [
  "cache:idempotency:bench"
 ],
 "registerDeveloper": [
  "cache:idempotency:bench"
 ],
 "registerEnvironment": [
  "cache:idempotency:bench"
 ],
 "registerPartner": [
  "cache:idempotency:bench"
 ],
 "rejectRelease": [
  "cache:idempotency:bench"
 ],
 "removeLicenceAddOn": [
  "cache:idempotency:bench"
 ],
 "replayDeadLetter": [
  "cache:idempotency:bench"
 ],
 "replayEvents": [
  "cache:idempotency:bench"
 ],
 "requestBurstEnvironment": [
  "cache:idempotency:bench"
 ],
 "resetSandbox": [
  "cache:idempotency:bench"
 ],
 "resolveInvoiceDispute": [
  "cache:idempotency:bench"
 ],
 "revokeApiCredential": [
  "cache:idempotency:bench"
 ],
 "rollbackMigrationRun": [
  "cache:idempotency:bench"
 ],
 "rollbackRollout": [
  "cache:idempotency:bench"
 ],
 "rollbackTenantMigration": [
  "cache:idempotency:bench"
 ],
 "rotateApiCredential": [
  "cache:idempotency:bench"
 ],
 "scheduleTenantUpgrade": [
  "cache:idempotency:bench"
 ],
 "setApiLicensing": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setApiQuota": [
  "cache:idempotency:bench",
  "cache:resolution:bench"
 ],
 "setChannelListing": [
  "cache:idempotency:bench"
 ],
 "setDeveloperMembers": [
  "cache:idempotency:bench"
 ],
 "setSubscription": [
  "cache:idempotency:bench"
 ],
 "settleAiUsage": [
  "cache:idempotency:bench"
 ],
 "skipRolloutCell": [
  "cache:idempotency:bench"
 ],
 "startRollout": [
  "cache:idempotency:bench"
 ],
 "submitIntegrationListing": [
  "cache:idempotency:bench"
 ],
 "submitOnboardingApplication": [
  "cache:idempotency:bench"
 ],
 "suspendTenant": [
  "cache:idempotency:bench"
 ],
 "terminateTenant": [
  "cache:idempotency:bench"
 ],
 "updateCellTier": [
  "cache:idempotency:bench"
 ],
 "updatePartnerAgreement": [
  "cache:idempotency:bench"
 ],
 "updateTenant": [
  "cache:idempotency:bench"
 ],
 "withdrawRelease": [
  "cache:idempotency:bench"
 ]
}
