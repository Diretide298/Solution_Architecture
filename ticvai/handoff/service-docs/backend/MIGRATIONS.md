# Database migrations for the first release

**363 tables in 33 migrations.** Every table the first release reads or writes, plus every table their foreign keys reach. The DDL for all of them already exists in `backend/`; each migration takes its schema's tables from there, with the matching foreign keys, indexes and row-level security, and a ROLLBACK section tested in CI (`backend/MIGRATIONS.md`). Generated; do not edit.

Each migration only references tables created by the ones above it. Keys that would point forward are added by the last migration.

## Order

| Order | File | Task | Database | Schema | Tables | Columns | References | Assignee | Points |
|---|---|---|---|---|---|---|---|---|---|
| 0 | `V0001__baseline.sql` | MIG-BASELINE | both | (baseline) | 0 | 0 |  | Hrushikant Patkar | 3 |
| 1 | `V0002__control.sql` | MIG-CONTROL | control | control | 8 | 191 |  | Hrushikant Patkar | 8 |
| 2 | `V0003__tenancy.sql` | MIG-TENANCY | tenant | tenancy | 1 | 12 |  | Hrushikant Patkar | 1 |
| 3 | `V0004__transport.sql` | MIG-TRANSPORT | tenant | transport | 10 | 93 |  | Hrushikant Patkar | 8 |
| 4 | `V0005__pricing.sql` | MIG-PRICING | tenant | pricing | 3 | 36 | catalogue | Pranay Shinde | 2 |
| 5 | `V0006__subscription.sql` | MIG-SUBSCRIPTION | tenant | subscription | 4 | 34 | platform | Hrushikant Patkar | 2 |
| 6 | `V0007__pii.sql` | MIG-PII | tenant | pii | 4 | 45 | access, marketing | Pranay Shinde | 2 |
| 7 | `V0008__games.sql` | MIG-GAMES | tenant | games | 2 | 15 | pii, platform | Hrushikant Patkar | 2 |
| 8 | `V0009__identity.sql` | MIG-IDENTITY | tenant | identity | 10 | 77 | pii, platform | Pranay Shinde | 5 |
| 9 | `V0010__approvals.sql` | MIG-APPROVALS | tenant | approvals | 5 | 72 | identity | Hrushikant Patkar | 3 |
| 10 | `V0011__reporting.sql` | MIG-REPORTING | tenant | reporting | 11 | 122 | identity, platform | Hrushikant Patkar | 8 |
| 11 | `V0012__ai.sql` | MIG-AI | tenant | ai | 10 | 142 | identity, pii, platform | Tanmay Dukhande | 8 |
| 12 | `V0013__assets.sql` | MIG-ASSETS | tenant | assets | 6 | 69 | identity, platform | Hrushikant Patkar | 5 |
| 13 | `V0014__resources.sql` | MIG-RESOURCES | tenant | resources | 7 | 85 | identity, orders, pii, platform | Hrushikant Patkar | 5 |
| 14 | `V0015__wallet.sql` | MIG-WALLET | tenant | wallet | 19 | 161 | identity, orders, pii, platform | Pranay Shinde | 8 |
| 15 | `V0016__whitelabel.sql` | MIG-WHITELABEL | tenant | whitelabel | 19 | 152 | identity, platform, promotions | Tanmay Dukhande | 8 |
| 16 | `V0017__workforce.sql` | MIG-WORKFORCE | tenant | workforce | 1 | 17 | identity, platform | Hrushikant Patkar | 2 |
| 17 | `V0018__platform.sql` | MIG-PLATFORM | tenant | platform | 13 | 137 | access, approvals, inventory, ledger | Hrushikant Patkar | 8 |
| 18 | `V0019__ledger.sql` | MIG-LEDGER | tenant | ledger | 10 | 112 | catalogue, identity, platform | Pranay Shinde | 5 |
| 19 | `V0020__inventory.sql` | MIG-INVENTORY | tenant | inventory | 10 | 156 | identity, ledger, platform | Hrushikant Patkar | 8 |
| 20 | `V0021__maintenance.sql` | MIG-MAINTENANCE | tenant | maintenance | 4 | 121 | access, identity, inventory, platform | Hrushikant Patkar | 5 |
| 21 | `V0022__promotions.sql` | MIG-PROMOTIONS | tenant | promotions | 18 | 200 | ledger, orders, pii, platform | Pranay Shinde | 8 |
| 22 | `V0023__seating.sql` | MIG-SEATING | tenant | seating | 6 | 62 | catalogue, identity, pii, platform | Pranay Shinde | 5 |
| 23 | `V0024__fnb.sql` | MIG-FNB | tenant | fnb | 27 | 269 | catalogue, identity, pii, platform, seating | Hrushikant Patkar | 8 |
| 24 | `V0025__catalogue.sql` | MIG-CATALOGUE | tenant | catalogue | 39 | 694 | access, identity, ledger, pii, platform, seating | Pranay Shinde | 8 |
| 25 | `V0026__venuemap.sql` | MIG-VENUEMAP | tenant | venuemap | 6 | 69 | access, assets, catalogue, platform, resources | Hrushikant Patkar | 3 |
| 26 | `V0027__orders.sql` | MIG-ORDERS | tenant | orders | 31 | 384 | access, catalogue, identity, ledger, pii, platform | Tanmay Dukhande | 8 |
| 27 | `V0028__access.sql` | MIG-ACCESS | tenant | access | 19 | 323 | catalogue, identity, orders, pii, platform | Tanmay Dukhande | 8 |
| 28 | `V0029__marketing.sql` | MIG-MARKETING | tenant | marketing | 38 | 449 | ai, catalogue, identity, ledger, orders, pii, platform | Pranay Shinde | 8 |
| 29 | `V0030__payments.sql` | MIG-PAYMENTS | tenant | payments | 7 | 90 | marketing, orders, pii | Tanmay Dukhande | 5 |
| 30 | `V0031__queue.sql` | MIG-QUEUE | tenant | queue | 5 | 74 | access, catalogue, maintenance, pii, platform | Hrushikant Patkar | 3 |
| 31 | `V0032__retail.sql` | MIG-RETAIL | tenant | retail | 10 | 110 | access, catalogue, fnb, identity, inventory, orders, pii, platform | Tanmay Dukhande | 5 |
| 32 | `V0033__cross_schema_foreign_keys.sql` | MIG-FOREIGN-KEYS | tenant | (cross-schema) | 0 | 0 |  | Hrushikant Patkar | 2 |

## Tables

| Migration | Table | Columns | Row-level security | Partitioned | Read by | Written by | Why |
|---|---|---|---|---|---|---|---|
| MIG-CONTROL | `control.licence_add_on` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-CONTROL | `control.licence_add_on_limit` | 6 | none |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner` | 28 | scope_path |  | 0 | 0 | referenced by control.partner_agreement |
| MIG-CONTROL | `control.partner_agreement` | 53 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_application` | 31 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_change_request` | 28 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.seo_metadata` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CONTROL | `control.tenant` | 23 | none |  | 7 | 5 | used by the first release |
| MIG-TENANCY | `tenancy.device_assignment` | 12 | scope_path |  | 1 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.departure` | 10 | none |  | 2 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.fare_matrix_cell` | 5 | none |  | 6 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.fare_passenger_type` | 11 | none |  | 5 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_table` | 6 | none |  | 6 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.favourite_route` | 8 | venue_id | yes | 3 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.pass_type` | 14 | venue_id | yes | 2 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.route` | 12 | venue_id | yes | 8 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.route_stop` | 7 | none |  | 9 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.station` | 8 | venue_id | yes | 8 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.timetable` | 12 | none |  | 2 | 0 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_action` | 7 | none |  | 4 | 3 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_condition` | 8 | none |  | 4 | 3 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_rule` | 21 | scope_path |  | 4 | 4 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.contract` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan` | 13 | none |  | 4 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_limit` | 6 | none |  | 2 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_module` | 3 | none |  | 2 | 0 | used by the first release |
| MIG-PII | `pii.subject` | 13 | none |  | 19 | 7 | used by the first release |
| MIG-PII | `pii.subject_biometric` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-PII | `pii.subject_contact` | 10 | none |  | 6 | 2 | used by the first release |
| MIG-PII | `pii.subject_document` | 10 | none |  | 0 | 1 | used by the first release |
| MIG-GAMES | `games.card` | 13 | venue_id | yes | 4 | 3 | used by the first release |
| MIG-GAMES | `games.credit_ledger` | 2 | none |  | 1 | 0 | used by the first release |
| MIG-IDENTITY | `identity.delegated_access` | 21 | scope_path |  | 12 | 2 | used by the first release |
| MIG-IDENTITY | `identity.mfa_challenge` | 2 | none |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.mfa_method` | 9 | none |  | 11 | 3 | used by the first release |
| MIG-IDENTITY | `identity.mfa_recovery_code` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.otp_challenge` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.password_policy` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.platform_staff_grant` | 9 | scope_path |  | 1 | 0 | used by the first release |
| MIG-IDENTITY | `identity.principal` | 9 | none |  | 23 | 2 | used by the first release |
| MIG-IDENTITY | `identity.principal_credential` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.role` | 8 | none |  | 6 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.decision` | 13 | none |  | 2 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.delegation` | 10 | scope_path |  | 4 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.matrix` | 6 | scope_path |  | 5 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.request` | 26 | scope_path |  | 2 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.rule` | 17 | none |  | 6 | 2 | used by the first release |
| MIG-REPORTING | `reporting.alert` | 18 | scope_path |  | 1 | 0 | used by the first release |
| MIG-REPORTING | `reporting.alert_rule` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-REPORTING | `reporting.dashboard` | 10 | venue_id |  | 5 | 3 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_tile` | 8 | none |  | 4 | 2 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_view` | 5 | venue_id |  | 0 | 1 | used by the first release |
| MIG-REPORTING | `reporting.execution` | 15 | none |  | 1 | 1 | used by the first release |
| MIG-REPORTING | `reporting.report_column` | 8 | none |  | 4 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_definition` | 16 | scope_path |  | 5 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_filter` | 7 | none |  | 4 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_parameter` | 7 | none |  | 4 | 1 | used by the first release |
| MIG-REPORTING | `reporting.schedule` | 15 | none |  | 0 | 0 | referenced by reporting.execution |
| MIG-AI | `ai.activity` | 22 | scope_path |  | 0 | 4 | used by the first release |
| MIG-AI | `ai.chunk_ref` | 2 | none |  | 2 | 0 | used by the first release |
| MIG-AI | `ai.conversation` | 8 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.knowledge_collection` | 12 | scope_path |  | 0 | 0 | referenced by ai.knowledge_document |
| MIG-AI | `ai.knowledge_document` | 10 | none |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.message` | 15 | none |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.policy` | 28 | scope_path |  | 6 | 2 | used by the first release |
| MIG-AI | `ai.proposed_action` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.provider` | 19 | scope_path |  | 7 | 2 | used by the first release |
| MIG-AI | `ai.suggestion` | 12 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ASSETS | `assets.asset_version` | 11 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_asset` | 25 | venue_id |  | 9 | 3 | used by the first release |
| MIG-ASSETS | `assets.media_collection` | 7 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_fingerprint` | 7 | scope_path |  | 0 | 2 | used by the first release |
| MIG-ASSETS | `assets.media_upload` | 12 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_usage` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-RESOURCES | `resources.booking` | 16 | none |  | 3 | 0 | used by the first release |
| MIG-RESOURCES | `resources.resource` | 15 | scope_path | yes | 5 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_block` | 8 | scope_path |  | 4 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_hold` | 15 | scope_path |  | 6 | 1 | used by the first release |
| MIG-RESOURCES | `resources.resource_package` | 13 | scope_path |  | 2 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_requirement` | 10 | scope_path |  | 4 | 3 | used by the first release |
| MIG-RESOURCES | `resources.resource_schedule` | 8 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.accounting_mapping` | 3 | scope_path |  | 3 | 2 | used by the first release |
| MIG-WALLET | `wallet.adjustment` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-WALLET | `wallet.authentication_policy` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.channel_rules` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version_snapshot` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.consumption_policy` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.credit_lot` | 12 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WALLET | `wallet.credit_type` | 15 | scope_path |  | 4 | 3 | used by the first release |
| MIG-WALLET | `wallet.funding_rules` | 11 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.gift_card` | 11 | none |  | 1 | 0 | used by the first release |
| MIG-WALLET | `wallet.integration_mapping` | 5 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.reconciliation_source` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.refund_policy` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.risk_rules` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.transfer_rules` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.wallet` | 9 | none |  | 4 | 2 | used by the first release |
| MIG-WALLET | `wallet.wallet_transaction` | 10 | venue_id |  | 2 | 2 | used by the first release |
| MIG-WALLET | `wallet.wallet_type` | 24 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.banner` | 12 | none |  | 3 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.config_version` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.content_page` | 11 | scope_path |  | 3 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.custom_domain` | 11 | none |  | 4 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_category` | 5 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_entry` | 6 | none |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.feature_toggle` | 7 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config` | 4 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_column` | 3 | none |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_social_link` | 4 | none |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice` | 11 | venue_id | yes | 7 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_answer` | 4 | none |  | 7 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_question` | 4 | none |  | 7 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.homepage_section` | 3 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.module_enablement` | 7 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.navigation_item` | 3 | none |  | 3 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.policy` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.promo_block` | 11 | scope_path |  | 4 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.tenant_config` | 25 | none |  | 21 | 13 | used by the first release |
| MIG-WORKFORCE | `workforce.rota_assignment` | 17 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-PLATFORM | `platform.denomination` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-PLATFORM | `platform.device` | 23 | none |  | 5 | 2 | used by the first release |
| MIG-PLATFORM | `platform.device_heartbeat` | 2 | none |  | 1 | 0 | used by the first release |
| MIG-PLATFORM | `platform.dsar_request` | 7 | none |  | 0 | 1 | used by the first release |
| MIG-PLATFORM | `platform.guest_link` | 5 | none |  | 0 | 0 | referenced by platform.dsar_request |
| MIG-PLATFORM | `platform.outbox` | 11 | scope_path |  | 0 | 14 | used by the first release |
| MIG-PLATFORM | `platform.outlet` | 9 | venue_id | yes | 8 | 2 | used by the first release |
| MIG-PLATFORM | `platform.region_settings` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board` | 6 | venue_id | yes | 3 | 2 | used by the first release |
| MIG-PLATFORM | `platform.scope` | 8 | none |  | 10 | 2 | used by the first release |
| MIG-PLATFORM | `platform.tenant` | 2 | none |  | 0 | 0 | referenced by subscription.contract |
| MIG-PLATFORM | `platform.venue_settings` | 28 | venue_id |  | 4 | 1 | used by the first release |
| MIG-PLATFORM | `platform.workstation` | 17 | scope_path | yes | 7 | 1 | used by the first release |
| MIG-LEDGER | `ledger.account` | 15 | none |  | 3 | 2 | used by the first release |
| MIG-LEDGER | `ledger.cost_center` | 6 | venue_id |  | 0 | 0 | referenced by platform.outlet |
| MIG-LEDGER | `ledger.event_budget` | 8 | none |  | 1 | 0 | used by the first release |
| MIG-LEDGER | `ledger.fiscal_period` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-LEDGER | `ledger.fx_provider_assignment` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-LEDGER | `ledger.fx_rate` | 13 | none |  | 7 | 2 | used by the first release |
| MIG-LEDGER | `ledger.journal_entry` | 20 | none |  | 0 | 3 | used by the first release |
| MIG-LEDGER | `ledger.legal_entity` | 11 | scope_path |  | 0 | 0 | referenced by ledger.fiscal_period |
| MIG-LEDGER | `ledger.posting` | 12 | venue_id |  | 2 | 3 | used by the first release |
| MIG-LEDGER | `ledger.tax_code` | 12 | none |  | 0 | 0 | referenced by catalogue.price |
| MIG-INVENTORY | `inventory.goods_receipt` | 11 | none |  | 3 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.goods_receipt_line` | 11 | none |  | 2 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.item` | 26 | venue_id | yes | 4 | 3 | used by the first release |
| MIG-INVENTORY | `inventory.location` | 7 | venue_id | yes | 0 | 0 | referenced by platform.outlet |
| MIG-INVENTORY | `inventory.movement` | 17 | none |  | 0 | 1 | used by the first release |
| MIG-INVENTORY | `inventory.purchase_order` | 29 | scope_path |  | 0 | 0 | referenced by inventory.goods_receipt |
| MIG-INVENTORY | `inventory.requisition` | 20 | venue_id | yes | 0 | 0 | referenced by inventory.purchase_order |
| MIG-INVENTORY | `inventory.serialised_item` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.stock_batch` | 10 | none |  | 1 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.supplier` | 16 | scope_path |  | 0 | 0 | referenced by inventory.stock_batch |
| MIG-MAINTENANCE | `maintenance.asset` | 29 | venue_id | yes | 0 | 0 | referenced by queue.queue |
| MIG-MAINTENANCE | `maintenance.incident` | 26 | venue_id | yes | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.inspection` | 14 | venue_id | yes | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.work_order` | 52 | venue_id | yes | 2 | 0 | used by the first release |
| MIG-PROMOTIONS | `promotions.allocation_component` | 9 | venue_id |  | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.allocation_split` | 4 | none |  | 0 | 0 | referenced by promotions.allocation_component |
| MIG-PROMOTIONS | `promotions.bundle` | 20 | venue_id | yes | 7 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_group` | 6 | none |  | 4 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_option` | 5 | none |  | 4 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_component` | 10 | venue_id |  | 4 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.campaign` | 9 | venue_id | yes | 5 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.campaign_budget` | 13 | none |  | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_campaign` | 14 | venue_id | yes | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code` | 15 | scope_path |  | 3 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code_batch` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion` | 22 | venue_id | yes | 19 | 8 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_audit` | 14 | venue_id | yes | 0 | 21 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_channel_publication` | 9 | venue_id | yes | 2 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_evaluation_trace` | 9 | venue_id | yes | 0 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_rule` | 13 | venue_id | yes | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_variant` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.upsell_rule` | 12 | none |  | 3 | 2 | used by the first release |
| MIG-SEATING | `seating.seat` | 11 | none |  | 1 | 0 | used by the first release |
| MIG-SEATING | `seating.seat_block` | 10 | scope_path |  | 0 | 0 | referenced by seating.seat_hold |
| MIG-SEATING | `seating.seat_category` | 7 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-SEATING | `seating.seat_hold` | 12 | none |  | 5 | 3 | used by the first release |
| MIG-SEATING | `seating.seat_map` | 12 | venue_id | yes | 0 | 0 | referenced by catalogue.performance |
| MIG-SEATING | `seating.seat_price_band` | 10 | none |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.cold_chain_event` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.corrective_action` | 13 | scope_path |  | 4 | 4 | used by the first release |
| MIG-FNB | `fnb.course_rule` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.delivery_location` | 11 | venue_id | yes | 3 | 0 | used by the first release |
| MIG-FNB | `fnb.delivery_policy` | 16 | scope_path |  | 4 | 1 | used by the first release |
| MIG-FNB | `fnb.dining_table` | 8 | none |  | 9 | 3 | used by the first release |
| MIG-FNB | `fnb.kitchen_exception` | 9 | none |  | 1 | 2 | used by the first release |
| MIG-FNB | `fnb.kitchen_station` | 8 | none |  | 5 | 2 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket` | 15 | none |  | 12 | 8 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket_line` | 14 | none |  | 7 | 1 | used by the first release |
| MIG-FNB | `fnb.location_session` | 10 | venue_id |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.menu` | 8 | none |  | 6 | 3 | used by the first release |
| MIG-FNB | `fnb.menu_item` | 15 | none |  | 8 | 4 | used by the first release |
| MIG-FNB | `fnb.menu_section` | 5 | none |  | 5 | 3 | used by the first release |
| MIG-FNB | `fnb.modifier_group` | 6 | scope_path |  | 3 | 1 | used by the first release |
| MIG-FNB | `fnb.modifier_option` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-FNB | `fnb.order_fulfilment` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.reservation_table` | 4 | none |  | 4 | 2 | used by the first release |
| MIG-FNB | `fnb.service_order` | 15 | none |  | 12 | 7 | used by the first release |
| MIG-FNB | `fnb.service_order_line` | 11 | none |  | 8 | 1 | used by the first release |
| MIG-FNB | `fnb.sold_out_item` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-FNB | `fnb.table_combination` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.table_reservation` | 8 | none |  | 4 | 3 | used by the first release |
| MIG-FNB | `fnb.table_session` | 9 | none |  | 2 | 2 | used by the first release |
| MIG-FNB | `fnb.table_visit` | 14 | none |  | 5 | 5 | used by the first release |
| MIG-FNB | `fnb.temperature_log` | 11 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.waitlist_entry` | 11 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.ai_catalogue_session` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.alternative_code` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.audit_entry` | 28 | scope_path |  | 0 | 23 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_allocation` | 19 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_capacity` | 12 | none |  | 10 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_connection` | 23 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_sales_rule` | 50 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.dynamic_pricing_control` | 39 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.dynamic_pricing_strategy` | 26 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.entitlement_template` | 31 | scope_path |  | 8 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event` | 8 | scope_path | yes | 8 | 4 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_capacity_profile` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_registration` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_resource_plan` | 4 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_schedule` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.fee` | 19 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.group_package` | 11 | scope_path |  | 4 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.import_job` | 25 | scope_path |  | 2 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.inventory_hold` | 14 | none |  | 8 | 7 | used by the first release |
| MIG-CATALOGUE | `catalogue.performance` | 11 | none |  | 9 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.price` | 5 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_assignment` | 26 | scope_path |  | 3 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_category` | 16 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_list` | 28 | venue_id | yes | 14 | 6 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_resolution_policy` | 11 | scope_path |  | 3 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.pricing_test_case` | 14 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product` | 39 | scope_path | yes | 34 | 12 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_category` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_channel_assignment` | 17 | scope_path |  | 3 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_eligibility_rule` | 14 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_media` | 6 | none |  | 8 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_version` | 9 | none |  | 1 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.published_bundle` | 10 | venue_id | yes | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.rate` | 17 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.rollback_action` | 26 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.rounding_profile` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.sales_channel` | 45 | scope_path |  | 8 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.variant` | 9 | none |  | 6 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.waitlist_entry` | 11 | none |  | 2 | 2 | used by the first release |
| MIG-VENUEMAP | `venuemap.import_job` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.map` | 15 | scope_path | yes | 9 | 2 | used by the first release |
| MIG-VENUEMAP | `venuemap.map_version` | 7 | none |  | 2 | 0 | used by the first release |
| MIG-VENUEMAP | `venuemap.path` | 10 | none |  | 4 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.placed_resource` | 11 | none |  | 4 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.point` | 15 | none |  | 5 | 2 | used by the first release |
| MIG-ORDERS | `orders.cart` | 18 | venue_id | yes | 11 | 6 | used by the first release |
| MIG-ORDERS | `orders.cart_line` | 22 | none |  | 9 | 4 | used by the first release |
| MIG-ORDERS | `orders.cash_count_line` | 11 | none |  | 5 | 4 | used by the first release |
| MIG-ORDERS | `orders.cash_movement` | 13 | none |  | 3 | 4 | used by the first release |
| MIG-ORDERS | `orders.deposit_box` | 15 | venue_id | yes | 5 | 4 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_foreign_holding` | 7 | none |  | 5 | 1 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_opening_denomination` | 4 | none |  | 5 | 1 | used by the first release |
| MIG-ORDERS | `orders.group_booking` | 21 | none |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.invitation` | 12 | none |  | 1 | 0 | used by the first release |
| MIG-ORDERS | `orders.no_sale_event` | 8 | none |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.order_event` | 16 | scope_path |  | 0 | 11 | used by the first release |
| MIG-ORDERS | `orders.order_line` | 26 | none |  | 13 | 8 | used by the first release |
| MIG-ORDERS | `orders.order_line_eligibility` | 7 | none |  | 11 | 0 | used by the first release |
| MIG-ORDERS | `orders.payment` | 16 | none |  | 20 | 12 | used by the first release |
| MIG-ORDERS | `orders.payment_link` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.pos_shift` | 24 | scope_path | yes | 10 | 7 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_approval` | 6 | none |  | 10 | 0 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_incident` | 6 | none |  | 10 | 0 | used by the first release |
| MIG-ORDERS | `orders.refund` | 18 | none |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.refund_policy` | 8 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.refund_policy_time_band` | 4 | none |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.resale_listing` | 16 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.reservation` | 7 | venue_id | yes | 5 | 2 | used by the first release |
| MIG-ORDERS | `orders.reservation_line` | 15 | none |  | 2 | 0 | used by the first release |
| MIG-ORDERS | `orders.sales_order` | 20 | scope_path | yes | 31 | 15 | used by the first release |
| MIG-ORDERS | `orders.stored_value_authorisation` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ORDERS | `orders.ticket_template` | 10 | none |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.ticket_template_channel` | 3 | none |  | 2 | 0 | used by the first release |
| MIG-ORDERS | `orders.ticket_transfer` | 12 | none |  | 2 | 2 | used by the first release |
| MIG-ORDERS | `orders.visit_reminder` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.wallet_pass` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.access_device` | 30 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.access_incident` | 12 | scope_path | yes | 0 | 1 | used by the first release |
| MIG-ACCESS | `access.access_point` | 17 | scope_path | yes | 11 | 5 | used by the first release |
| MIG-ACCESS | `access.access_point_group` | 8 | scope_path | yes | 4 | 2 | used by the first release |
| MIG-ACCESS | `access.admission_rules` | 21 | scope_path |  | 5 | 3 | used by the first release |
| MIG-ACCESS | `access.biometric_audit_event` | 18 | scope_path | yes | 0 | 2 | used by the first release |
| MIG-ACCESS | `access.biometric_profile` | 36 | scope_path | yes | 5 | 4 | used by the first release |
| MIG-ACCESS | `access.blacklist` | 10 | scope_path |  | 3 | 1 | used by the first release |
| MIG-ACCESS | `access.configuration_change` | 11 | scope_path |  | 0 | 18 | used by the first release |
| MIG-ACCESS | `access.credential_policy` | 32 | scope_path |  | 4 | 3 | used by the first release |
| MIG-ACCESS | `access.device_binding` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.entitlement` | 26 | scope_path |  | 20 | 7 | used by the first release |
| MIG-ACCESS | `access.entry_rule_point` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.face_reenrolment_attempt` | 15 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_change` | 11 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_policy` | 12 | scope_path | yes | 3 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_entitlement` | 12 | none |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_facility` | 13 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.scan_event` | 19 | scope_path | yes | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.agent_availability` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.booking_consent_record` | 20 | scope_path |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.campaign` | 19 | venue_id |  | 0 | 0 | referenced by marketing.message_dispatch |
| MIG-MARKETING | `marketing.case` | 23 | venue_id |  | 5 | 2 | used by the first release |
| MIG-MARKETING | `marketing.case_message` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge_progress` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-MARKETING | `marketing.consent_propagation` | 9 | none |  | 0 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose` | 8 | none |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose_channel` | 3 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_question` | 11 | scope_path |  | 11 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_question_version` | 6 | none |  | 11 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_record` | 9 | none |  | 7 | 3 | used by the first release |
| MIG-MARKETING | `marketing.conversation` | 21 | venue_id |  | 2 | 2 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message` | 8 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message_attachment` | 4 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition` | 15 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition_field` | 23 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_submission` | 12 | none |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.guest_device` | 14 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_document` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_preference` | 7 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_profile` | 23 | none |  | 11 | 5 | used by the first release |
| MIG-MARKETING | `marketing.invitation` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.invitation_campaign` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_position` | 12 | none |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_programme` | 7 | venue_id |  | 5 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_rule` | 9 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.message_dispatch` | 16 | none |  | 2 | 3 | used by the first release |
| MIG-MARKETING | `marketing.points_earning_rule` | 6 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.points_redemption_rule` | 13 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.privacy_notice_governance` | 14 | scope_path |  | 0 | 1 | used by the first release |
| MIG-MARKETING | `marketing.programme_tier` | 11 | none |  | 3 | 2 | used by the first release |
| MIG-MARKETING | `marketing.referral` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.review` | 13 | venue_id | yes | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.segment` | 9 | venue_id |  | 0 | 0 | referenced by marketing.guest_profile |
| MIG-MARKETING | `marketing.subscription` | 8 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.wishlist_item` | 12 | none |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.dunning_case` | 14 | scope_path |  | 4 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.method` | 16 | scope_path |  | 0 | 0 | referenced by payments.payment_attempt |
| MIG-PAYMENTS | `payments.payment_attempt` | 16 | scope_path |  | 0 | 2 | used by the first release |
| MIG-PAYMENTS | `payments.provider` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.provider_connection` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.routing_rule` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.token` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-QUEUE | `queue.entry` | 18 | none |  | 5 | 2 | used by the first release |
| MIG-QUEUE | `queue.feed` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-QUEUE | `queue.queue` | 37 | venue_id | yes | 5 | 2 | used by the first release |
| MIG-QUEUE | `queue.queue_operating_window` | 4 | none |  | 4 | 1 | used by the first release |
| MIG-QUEUE | `queue.reading` | 8 | none |  | 1 | 0 | used by the first release |
| MIG-RETAIL | `retail.merchandise` | 16 | none |  | 4 | 2 | used by the first release |
| MIG-RETAIL | `retail.reservation` | 8 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.reservation_line` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_line` | 9 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_policy` | 10 | none |  | 2 | 1 | used by the first release |
| MIG-RETAIL | `retail.sale` | 13 | none |  | 5 | 2 | used by the first release |
| MIG-RETAIL | `retail.sale_line` | 13 | none |  | 4 | 1 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop` | 15 | venue_id |  | 1 | 0 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop_line` | 7 | none |  | 1 | 0 | used by the first release |

## Used by the release but not a table

- `embedded as attributes (jsonb) on orders.cart_line and orders.order_line`: Holds 2 columns. No description has been written for this table — the name is the only thing saying what it is. Hangs off: a root — nothing above it in its sche
- `embedded as window_starts_at and window_ends_at on orders.cart_line and orders.order_line`: Holds 3 columns. No description has been written for this table — the name is the only thing saying what it is. Hangs off: a root — nothing above it in its sche
- `fnb.table_reservation (deposit_* columns; the money itself is orders.deposit)`: Holds 8 columns. No description has been written for this table — the name is the only thing saying what it is. Hangs off: reaches `fnb.service_order` through i
- `identity.guest_session`: Redis. `GuestSession` declares `persistence: none — Redis session registry`. Separate from the staff session by lifetime and auth path, and neither is a row. Ha
- `identity.session`: Redis, not Postgres. `ActiveSession` and `Session` both declare `persistence: none — Redis session registry`, and ADR-0004 makes a session a token with a validi
- `inventory.stock_level`: Derived from movements, not stored. `StockPosition` declares `persistence: none — derived from movements`, which is the correct design: a stored level and a mov
