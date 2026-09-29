# Database migrations for the first release

**469 tables in 34 migrations.** Every table the first release reads or writes, plus every table their foreign keys reach. The DDL for all of them already exists in `backend/`; each migration takes its schema's tables from there, with the matching foreign keys, indexes and row-level security, and a ROLLBACK section tested in CI (`backend/MIGRATIONS.md`). Generated; do not edit.

Each migration only references tables created by the ones above it. Keys that would point forward are added by the last migration.

## Order

| Order | File | Task | Database | Schema | Tables | Columns | References | Assignee | Points |
|---|---|---|---|---|---|---|---|---|---|
| 0 | `V0001__baseline.sql` | MIG-BASELINE | both | (baseline) | 0 | 0 |  | Hrushikant Patkar | 3 |
| 1 | `V0002__control.sql` | MIG-CONTROL | control | control | 17 | 293 |  | Hrushikant Patkar | 8 |
| 2 | `V0003__tenancy.sql` | MIG-TENANCY | tenant | tenancy | 1 | 12 |  | Tanmay Dukhande | 1 |
| 3 | `V0004__pricing.sql` | MIG-PRICING | tenant | pricing | 3 | 36 | catalogue | Tanmay Dukhande | 2 |
| 4 | `V0005__subscription.sql` | MIG-SUBSCRIPTION | tenant | subscription | 4 | 36 | platform | Hrushikant Patkar | 2 |
| 5 | `V0006__transport.sql` | MIG-TRANSPORT | tenant | transport | 12 | 107 | assets | Hrushikant Patkar | 8 |
| 6 | `V0007__pii.sql` | MIG-PII | tenant | pii | 5 | 51 | access, marketing | Tanmay Dukhande | 3 |
| 7 | `V0008__games.sql` | MIG-GAMES | tenant | games | 2 | 15 | pii, platform | Hrushikant Patkar | 2 |
| 8 | `V0009__identity.sql` | MIG-IDENTITY | tenant | identity | 13 | 113 | pii, platform | Tanmay Dukhande | 8 |
| 9 | `V0010__approvals.sql` | MIG-APPROVALS | tenant | approvals | 6 | 88 | identity | Tanmay Dukhande | 5 |
| 10 | `V0011__reporting.sql` | MIG-REPORTING | tenant | reporting | 15 | 154 | identity, platform | Hrushikant Patkar | 8 |
| 11 | `V0012__sync.sql` | MIG-SYNC | tenant | sync | 1 | 11 | identity, platform | Pranay Shinde | 1 |
| 12 | `V0013__assets.sql` | MIG-ASSETS | tenant | assets | 7 | 74 | identity, platform | Hrushikant Patkar | 5 |
| 13 | `V0014__ai.sql` | MIG-AI | tenant | ai | 47 | 661 | assets, identity, pii, platform | Pranay Shinde | 8 |
| 14 | `V0015__resources.sql` | MIG-RESOURCES | tenant | resources | 7 | 86 | identity, orders, pii, platform | Hrushikant Patkar | 5 |
| 15 | `V0016__whitelabel.sql` | MIG-WHITELABEL | tenant | whitelabel | 25 | 220 | identity, platform, promotions | Tanmay Dukhande | 8 |
| 16 | `V0017__workforce.sql` | MIG-WORKFORCE | tenant | workforce | 1 | 17 | identity, platform | Tanmay Dukhande | 2 |
| 17 | `V0018__platform.sql` | MIG-PLATFORM | tenant | platform | 17 | 167 | access, approvals, identity, inventory, ledger | Tanmay Dukhande | 8 |
| 18 | `V0019__seating.sql` | MIG-SEATING | tenant | seating | 6 | 62 | catalogue, identity, pii, platform | Tanmay Dukhande | 5 |
| 19 | `V0020__maintenance.sql` | MIG-MAINTENANCE | tenant | maintenance | 6 | 146 | access, identity, inventory, platform | Hrushikant Patkar | 8 |
| 20 | `V0021__wallet.sql` | MIG-WALLET | tenant | wallet | 23 | 208 | identity, orders, pii, platform | Pranay Shinde | 8 |
| 21 | `V0022__catalogue.sql` | MIG-CATALOGUE | tenant | catalogue | 31 | 484 | access, identity, ledger, pii, platform, seating | Tanmay Dukhande | 8 |
| 22 | `V0023__ledger.sql` | MIG-LEDGER | tenant | ledger | 19 | 261 | catalogue, identity, orders, platform | Tanmay Dukhande | 8 |
| 23 | `V0024__inventory.sql` | MIG-INVENTORY | tenant | inventory | 11 | 162 | identity, ledger, platform | Hrushikant Patkar | 8 |
| 24 | `V0025__promotions.sql` | MIG-PROMOTIONS | tenant | promotions | 17 | 193 | ledger, orders, pii, platform | Tanmay Dukhande | 8 |
| 25 | `V0026__orders.sql` | MIG-ORDERS | tenant | orders | 33 | 399 | access, catalogue, identity, ledger, pii, platform, promotions | Pranay Shinde | 8 |
| 26 | `V0027__access.sql` | MIG-ACCESS | tenant | access | 23 | 379 | catalogue, identity, orders, pii, platform | Hrushikant Patkar | 8 |
| 27 | `V0028__marketing.sql` | MIG-MARKETING | tenant | marketing | 49 | 585 | ai, catalogue, identity, ledger, orders, pii, platform | Pranay Shinde | 8 |
| 28 | `V0029__fnb.sql` | MIG-FNB | tenant | fnb | 34 | 325 | access, catalogue, identity, inventory, orders, pii, platform, seating | Hrushikant Patkar | 8 |
| 29 | `V0030__payments.sql` | MIG-PAYMENTS | tenant | payments | 11 | 132 | marketing, orders, pii | Pranay Shinde | 8 |
| 30 | `V0031__queue.sql` | MIG-QUEUE | tenant | queue | 5 | 81 | access, catalogue, maintenance, pii, platform | Hrushikant Patkar | 3 |
| 31 | `V0032__retail.sql` | MIG-RETAIL | tenant | retail | 10 | 110 | access, catalogue, fnb, identity, inventory, orders, pii, platform | Pranay Shinde | 5 |
| 32 | `V0033__venuemap.sql` | MIG-VENUEMAP | tenant | venuemap | 8 | 105 | access, assets, catalogue, marketing, orders, platform, promotions, resources | Hrushikant Patkar | 5 |
| 33 | `V0034__cross_schema_foreign_keys.sql` | MIG-FOREIGN-KEYS | tenant | (cross-schema) | 0 | 0 |  | Hrushikant Patkar | 3 |

## Tables

| Migration | Table | Columns | Row-level security | Partitioned | Read by | Written by | Why |
|---|---|---|---|---|---|---|---|
| MIG-CONTROL | `control.api_client` | 14 | none |  | 4 | 3 | used by the first release |
| MIG-CONTROL | `control.api_licence` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-CONTROL | `control.api_version` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-CONTROL | `control.content_block` | 12 | scope_path |  | 4 | 2 | used by the first release |
| MIG-CONTROL | `control.developer_account` | 8 | none |  | 3 | 2 | used by the first release |
| MIG-CONTROL | `control.integration_listing` | 12 | none |  | 3 | 1 | used by the first release |
| MIG-CONTROL | `control.invoice` | 14 | none |  | 0 | 0 | referenced by control.invoice_line |
| MIG-CONTROL | `control.invoice_line` | 10 | none |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.licence_add_on` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-CONTROL | `control.licence_add_on_limit` | 6 | none |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner` | 28 | scope_path |  | 0 | 0 | referenced by control.partner_agreement |
| MIG-CONTROL | `control.partner_agreement` | 53 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_application` | 31 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_change_request` | 28 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.production_access_request` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-CONTROL | `control.seo_metadata` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CONTROL | `control.tenant` | 23 | none |  | 9 | 5 | used by the first release |
| MIG-TENANCY | `tenancy.device_assignment` | 12 | scope_path |  | 1 | 1 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_action` | 7 | none |  | 4 | 3 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_condition` | 8 | none |  | 4 | 3 | used by the first release |
| MIG-PRICING | `pricing.dynamic_price_rule` | 21 | scope_path |  | 4 | 4 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.contract` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan` | 15 | none |  | 5 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_limit` | 6 | none |  | 2 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_module` | 3 | none |  | 2 | 0 | used by the first release |
| MIG-TRANSPORT | `transport.departure` | 10 | none |  | 2 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_matrix_cell` | 5 | none |  | 6 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_passenger_type` | 11 | none |  | 5 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_table` | 6 | none |  | 6 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.favourite_route` | 8 | venue_id | yes | 3 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.network_import` | 10 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.pass_type` | 14 | venue_id | yes | 3 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.route` | 12 | venue_id | yes | 10 | 3 | used by the first release |
| MIG-TRANSPORT | `transport.route_stop` | 7 | none |  | 9 | 3 | used by the first release |
| MIG-TRANSPORT | `transport.station` | 8 | venue_id | yes | 10 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.timetable` | 12 | none |  | 4 | 3 | used by the first release |
| MIG-TRANSPORT | `transport.timetable_run` | 4 | none |  | 2 | 2 | used by the first release |
| MIG-PII | `pii.consent_identifier` | 6 | scope_path |  | 0 | 1 | used by the first release |
| MIG-PII | `pii.subject` | 13 | none |  | 19 | 7 | used by the first release |
| MIG-PII | `pii.subject_biometric` | 12 | none |  | 4 | 3 | used by the first release |
| MIG-PII | `pii.subject_contact` | 10 | none |  | 6 | 2 | used by the first release |
| MIG-PII | `pii.subject_document` | 10 | none |  | 0 | 2 | used by the first release |
| MIG-GAMES | `games.card` | 13 | venue_id | yes | 4 | 3 | used by the first release |
| MIG-GAMES | `games.credit_ledger` | 2 | none |  | 1 | 0 | used by the first release |
| MIG-IDENTITY | `identity.delegated_access` | 21 | scope_path |  | 12 | 3 | used by the first release |
| MIG-IDENTITY | `identity.guest_identity_verification` | 13 | none |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.guest_verification_policy` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.mfa_challenge` | 2 | none |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.mfa_method` | 9 | none |  | 11 | 3 | used by the first release |
| MIG-IDENTITY | `identity.mfa_recovery_code` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.otp_challenge` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.password_policy` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.platform_staff_grant` | 9 | scope_path |  | 1 | 0 | used by the first release |
| MIG-IDENTITY | `identity.principal` | 9 | none |  | 24 | 2 | used by the first release |
| MIG-IDENTITY | `identity.principal_credential` | 2 | none |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.refresh_token` | 10 | none |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.role` | 8 | none |  | 6 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.decision` | 13 | none |  | 2 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.delegation` | 10 | scope_path |  | 4 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.external_provider` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.matrix` | 6 | scope_path |  | 5 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.request` | 27 | scope_path |  | 2 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.rule` | 18 | none |  | 6 | 2 | used by the first release |
| MIG-REPORTING | `reporting.alert` | 18 | scope_path |  | 1 | 0 | used by the first release |
| MIG-REPORTING | `reporting.alert_rule` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-REPORTING | `reporting.dashboard` | 10 | venue_id |  | 5 | 3 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_tile` | 8 | none |  | 4 | 2 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_view` | 5 | venue_id |  | 0 | 1 | used by the first release |
| MIG-REPORTING | `reporting.execution` | 15 | none |  | 1 | 1 | used by the first release |
| MIG-REPORTING | `reporting.kpi_definition` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-REPORTING | `reporting.natural_language_query` | 9 | scope_path |  | 1 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_column` | 8 | none |  | 6 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_definition` | 16 | scope_path |  | 8 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_definition_version` | 7 | scope_path |  | 1 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_filter` | 7 | none |  | 6 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_parameter` | 7 | none |  | 6 | 3 | used by the first release |
| MIG-REPORTING | `reporting.schedule` | 15 | none |  | 0 | 0 | referenced by reporting.execution |
| MIG-REPORTING | `reporting.semantic_model` | 4 | scope_path |  | 2 | 1 | used by the first release |
| MIG-SYNC | `sync.rejection` | 11 | none |  | 0 | 1 | used by the first release |
| MIG-ASSETS | `assets.asset_version` | 11 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_asset` | 25 | venue_id |  | 14 | 3 | used by the first release |
| MIG-ASSETS | `assets.media_collection` | 7 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_collection_member` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_fingerprint` | 7 | scope_path |  | 0 | 2 | used by the first release |
| MIG-ASSETS | `assets.media_upload` | 12 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_usage` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.action_plan` | 19 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.activity` | 24 | scope_path |  | 1 | 11 | used by the first release |
| MIG-AI | `ai.anomaly_detector` | 14 | scope_path |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.answer_feedback` | 11 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.assistant_profile` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.byok_enablement` | 10 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.capability` | 18 | scope_path |  | 5 | 3 | used by the first release |
| MIG-AI | `ai.capability_maturity` | 9 | scope_path |  | 1 | 0 | used by the first release |
| MIG-AI | `ai.chunk_embedding` | 11 | none |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.chunk_ref` | 2 | none |  | 4 | 0 | used by the first release |
| MIG-AI | `ai.conversation` | 8 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.decision_record` | 25 | scope_path |  | 1 | 15 | used by the first release |
| MIG-AI | `ai.eval_run` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.eval_suite` | 9 | scope_path |  | 1 | 0 | used by the first release |
| MIG-AI | `ai.forecast_definition` | 19 | scope_path |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.forecast_point` | 12 | scope_path |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.forecast_scenario` | 8 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.forecast_version` | 17 | scope_path |  | 4 | 2 | used by the first release |
| MIG-AI | `ai.governance_alert` | 14 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.governance_policy` | 9 | scope_path |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.governance_policy_version` | 12 | scope_path |  | 5 | 3 | used by the first release |
| MIG-AI | `ai.guided_choice_suggestion` | 12 | scope_path | yes | 2 | 1 | used by the first release |
| MIG-AI | `ai.history_import` | 18 | scope_path | yes | 3 | 1 | used by the first release |
| MIG-AI | `ai.history_observation` | 10 | scope_path | yes | 2 | 1 | used by the first release |
| MIG-AI | `ai.incident` | 16 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.index_entry` | 2 | none |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.index_job` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.index_source` | 15 | none |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.insight` | 22 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.intervention` | 11 | scope_path |  | 0 | 2 | used by the first release |
| MIG-AI | `ai.knowledge_collection` | 12 | scope_path |  | 4 | 1 | used by the first release |
| MIG-AI | `ai.knowledge_document` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.knowledge_gap` | 13 | scope_path |  | 0 | 2 | used by the first release |
| MIG-AI | `ai.message` | 15 | none |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.model` | 16 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.operational_requirement` | 17 | scope_path |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.policy` | 28 | scope_path |  | 14 | 4 | used by the first release |
| MIG-AI | `ai.policy_exception` | 13 | scope_path |  | 2 | 2 | used by the first release |
| MIG-AI | `ai.prompt_template` | 13 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.proposed_action` | 18 | scope_path |  | 2 | 5 | used by the first release |
| MIG-AI | `ai.provider` | 22 | scope_path |  | 10 | 2 | used by the first release |
| MIG-AI | `ai.rec_decision` | 19 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.rec_decline` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.rec_event` | 11 | scope_path |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.release` | 17 | scope_path |  | 6 | 5 | used by the first release |
| MIG-AI | `ai.suggestion` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.venue_settings` | 14 | scope_path | yes | 4 | 1 | used by the first release |
| MIG-RESOURCES | `resources.booking` | 16 | none |  | 3 | 0 | used by the first release |
| MIG-RESOURCES | `resources.resource` | 16 | scope_path | yes | 5 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_block` | 8 | scope_path |  | 5 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_hold` | 15 | scope_path |  | 7 | 1 | used by the first release |
| MIG-RESOURCES | `resources.resource_package` | 13 | scope_path |  | 2 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_requirement` | 10 | scope_path |  | 4 | 3 | used by the first release |
| MIG-RESOURCES | `resources.resource_schedule` | 8 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.analytics_provider` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.app_build` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.banner` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.booking_flow` | 10 | scope_path |  | 15 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.booking_flow_step` | 7 | none |  | 10 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.config_version` | 11 | scope_path |  | 8 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.content_page` | 11 | scope_path |  | 5 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.custom_domain` | 11 | none |  | 4 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_category` | 5 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_entry` | 6 | none |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.feature_toggle` | 7 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config` | 4 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_column` | 3 | none |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_social_link` | 4 | none |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice` | 13 | venue_id | yes | 8 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_answer` | 5 | none |  | 10 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_question` | 5 | none |  | 8 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.homepage_section` | 3 | none |  | 5 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.module_enablement` | 7 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.navigation_item` | 4 | none |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.policy` | 10 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.promo_block` | 11 | scope_path |  | 5 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.site_setup_progress` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.store_account` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.tenant_config` | 25 | none |  | 24 | 12 | used by the first release |
| MIG-WORKFORCE | `workforce.rota_assignment` | 17 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-PLATFORM | `platform.audit_record` | 8 | none |  | 0 | 3 | used by the first release |
| MIG-PLATFORM | `platform.denomination` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-PLATFORM | `platform.device` | 23 | none |  | 5 | 2 | used by the first release |
| MIG-PLATFORM | `platform.device_heartbeat` | 2 | none |  | 1 | 0 | used by the first release |
| MIG-PLATFORM | `platform.dsar_request` | 7 | none |  | 0 | 1 | used by the first release |
| MIG-PLATFORM | `platform.guest_link` | 5 | none |  | 0 | 0 | referenced by platform.dsar_request |
| MIG-PLATFORM | `platform.idempotency_record` | 11 | scope_path |  | 0 | 9 | used by the first release |
| MIG-PLATFORM | `platform.outbox` | 15 | scope_path |  | 0 | 42 | used by the first release |
| MIG-PLATFORM | `platform.outlet` | 9 | venue_id | yes | 10 | 2 | used by the first release |
| MIG-PLATFORM | `platform.region_settings` | 12 | none |  | 4 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board` | 6 | venue_id | yes | 3 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board_page` | 4 | none |  | 1 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board_tile` | 2 | none |  | 1 | 2 | used by the first release |
| MIG-PLATFORM | `platform.scope` | 8 | none |  | 9 | 2 | used by the first release |
| MIG-PLATFORM | `platform.tenant` | 2 | none |  | 0 | 0 | referenced by subscription.contract |
| MIG-PLATFORM | `platform.venue_settings` | 29 | venue_id |  | 4 | 1 | used by the first release |
| MIG-PLATFORM | `platform.workstation` | 17 | scope_path | yes | 7 | 1 | used by the first release |
| MIG-SEATING | `seating.seat` | 11 | none |  | 1 | 0 | used by the first release |
| MIG-SEATING | `seating.seat_block` | 10 | scope_path |  | 0 | 0 | referenced by seating.seat_hold |
| MIG-SEATING | `seating.seat_category` | 7 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-SEATING | `seating.seat_hold` | 12 | none |  | 5 | 3 | used by the first release |
| MIG-SEATING | `seating.seat_map` | 12 | venue_id | yes | 0 | 0 | referenced by seating.seat |
| MIG-SEATING | `seating.seat_price_band` | 10 | none |  | 1 | 1 | used by the first release |
| MIG-MAINTENANCE | `maintenance.asset` | 30 | venue_id | yes | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.incident` | 26 | venue_id | yes | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.inspection` | 14 | venue_id | yes | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.inspection_template` | 9 | venue_id |  | 2 | 1 | used by the first release |
| MIG-MAINTENANCE | `maintenance.inspection_template_item` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-MAINTENANCE | `maintenance.work_order` | 56 | venue_id | yes | 2 | 0 | used by the first release |
| MIG-WALLET | `wallet.accounting_mapping` | 3 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.adjustment` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-WALLET | `wallet.authentication_policy` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.auto_reload_setting` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.balance` | 9 | none |  | 5 | 3 | used by the first release |
| MIG-WALLET | `wallet.channel_rules` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version_snapshot` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.consumption_policy` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.credit_lot` | 12 | scope_path |  | 5 | 1 | used by the first release |
| MIG-WALLET | `wallet.credit_type` | 15 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.exit_settlement` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.funding_rules` | 11 | scope_path |  | 3 | 2 | used by the first release |
| MIG-WALLET | `wallet.gift_card` | 11 | none |  | 1 | 0 | used by the first release |
| MIG-WALLET | `wallet.hold` | 12 | none |  | 3 | 3 | used by the first release |
| MIG-WALLET | `wallet.integration_mapping` | 5 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.reconciliation_source` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.refund_policy` | 7 | scope_path |  | 4 | 2 | used by the first release |
| MIG-WALLET | `wallet.risk_rules` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.transfer_rules` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.wallet` | 9 | none |  | 9 | 3 | used by the first release |
| MIG-WALLET | `wallet.wallet_transaction` | 12 | venue_id |  | 2 | 6 | used by the first release |
| MIG-WALLET | `wallet.wallet_type` | 24 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.alternative_code` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.audit_entry` | 28 | scope_path |  | 0 | 10 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_allocation` | 19 | none |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_capacity` | 12 | none |  | 10 | 6 | used by the first release |
| MIG-CATALOGUE | `catalogue.dynamic_pricing_control` | 39 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.dynamic_pricing_strategy` | 26 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.entitlement_template` | 32 | scope_path |  | 8 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event` | 8 | scope_path | yes | 9 | 4 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_capacity_profile` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_registration` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_resource_plan` | 4 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_schedule` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.group_package` | 11 | scope_path |  | 4 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.import_job` | 25 | scope_path |  | 2 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.inventory_hold` | 18 | none |  | 10 | 11 | used by the first release |
| MIG-CATALOGUE | `catalogue.performance` | 11 | none |  | 13 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.price` | 5 | none |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_category` | 16 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_list` | 28 | venue_id | yes | 11 | 6 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_resolution_policy` | 11 | scope_path |  | 3 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.pricing_test_case` | 14 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product` | 41 | scope_path | yes | 32 | 5 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_category` | 12 | scope_path |  | 6 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_eligibility_rule` | 15 | scope_path |  | 8 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_media` | 6 | none |  | 5 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_version` | 9 | none |  | 0 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.published_bundle` | 10 | venue_id | yes | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.rate` | 17 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.rounding_profile` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.variant` | 9 | none |  | 8 | 3 | used by the first release |
| MIG-CATALOGUE | `catalogue.waitlist_entry` | 11 | none |  | 2 | 2 | used by the first release |
| MIG-LEDGER | `ledger.account` | 15 | none |  | 3 | 2 | used by the first release |
| MIG-LEDGER | `ledger.cost_center` | 6 | venue_id |  | 0 | 0 | referenced by orders.invitation |
| MIG-LEDGER | `ledger.credit_memo` | 21 | scope_path |  | 5 | 1 | used by the first release |
| MIG-LEDGER | `ledger.credit_memo_line` | 10 | none |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.einvoice_transmission` | 17 | scope_path |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.einvoicing_provider` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-LEDGER | `ledger.event_budget` | 8 | none |  | 1 | 0 | used by the first release |
| MIG-LEDGER | `ledger.fiscal_period` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-LEDGER | `ledger.fx_provider_assignment` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-LEDGER | `ledger.fx_rate` | 13 | none |  | 7 | 2 | used by the first release |
| MIG-LEDGER | `ledger.journal_entry` | 20 | none |  | 0 | 4 | used by the first release |
| MIG-LEDGER | `ledger.journal_line` | 8 | venue_id |  | 0 | 2 | used by the first release |
| MIG-LEDGER | `ledger.legal_entity` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.posting` | 12 | venue_id |  | 2 | 2 | used by the first release |
| MIG-LEDGER | `ledger.price_variance` | 15 | venue_id | yes | 0 | 1 | used by the first release |
| MIG-LEDGER | `ledger.tax_code` | 12 | none |  | 3 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice` | 32 | scope_path |  | 6 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice_line` | 16 | none |  | 6 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice_template` | 18 | scope_path |  | 2 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.goods_receipt` | 11 | none |  | 3 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.goods_receipt_line` | 11 | none |  | 2 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.item` | 26 | venue_id | yes | 5 | 3 | used by the first release |
| MIG-INVENTORY | `inventory.kit_component` | 6 | scope_path |  | 3 | 1 | used by the first release |
| MIG-INVENTORY | `inventory.location` | 7 | venue_id | yes | 0 | 0 | referenced by platform.outlet |
| MIG-INVENTORY | `inventory.movement` | 17 | none |  | 2 | 3 | used by the first release |
| MIG-INVENTORY | `inventory.purchase_order` | 29 | scope_path |  | 0 | 0 | referenced by inventory.goods_receipt |
| MIG-INVENTORY | `inventory.requisition` | 20 | venue_id | yes | 0 | 0 | referenced by inventory.purchase_order |
| MIG-INVENTORY | `inventory.serialised_item` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.stock_batch` | 10 | none |  | 2 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.supplier` | 16 | scope_path |  | 0 | 0 | referenced by maintenance.asset |
| MIG-PROMOTIONS | `promotions.allocation_component` | 9 | venue_id |  | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.allocation_split` | 4 | none |  | 0 | 0 | referenced by promotions.allocation_component |
| MIG-PROMOTIONS | `promotions.bundle` | 20 | venue_id | yes | 9 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_group` | 6 | none |  | 4 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_option` | 5 | none |  | 4 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_component` | 13 | venue_id |  | 4 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.campaign` | 9 | venue_id | yes | 5 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.campaign_budget` | 13 | none |  | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_campaign` | 14 | venue_id | yes | 5 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code` | 15 | scope_path |  | 4 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code_batch` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion` | 24 | venue_id | yes | 21 | 8 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_audit` | 14 | venue_id | yes | 0 | 22 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_channel_publication` | 9 | venue_id | yes | 2 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_evaluation_trace` | 9 | venue_id | yes | 0 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_rule` | 13 | venue_id | yes | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_variant` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.cart` | 18 | venue_id | yes | 11 | 8 | used by the first release |
| MIG-ORDERS | `orders.cart_line` | 21 | none |  | 10 | 6 | used by the first release |
| MIG-ORDERS | `orders.cash_count_line` | 11 | none |  | 5 | 4 | used by the first release |
| MIG-ORDERS | `orders.cash_movement` | 13 | none |  | 3 | 4 | used by the first release |
| MIG-ORDERS | `orders.deposit_box` | 15 | venue_id | yes | 5 | 4 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_foreign_holding` | 7 | none |  | 5 | 1 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_opening_denomination` | 4 | none |  | 5 | 1 | used by the first release |
| MIG-ORDERS | `orders.fraud_rule` | 12 | scope_path |  | 3 | 0 | used by the first release |
| MIG-ORDERS | `orders.group_booking` | 21 | none |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.invitation` | 12 | none |  | 1 | 0 | used by the first release |
| MIG-ORDERS | `orders.no_sale_event` | 8 | none |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.order_event` | 16 | scope_path |  | 0 | 11 | used by the first release |
| MIG-ORDERS | `orders.order_line` | 23 | venue_id |  | 15 | 9 | used by the first release |
| MIG-ORDERS | `orders.order_line_discount` | 6 | none |  | 11 | 2 | used by the first release |
| MIG-ORDERS | `orders.order_line_eligibility` | 7 | none |  | 11 | 1 | used by the first release |
| MIG-ORDERS | `orders.payment` | 18 | none |  | 22 | 15 | used by the first release |
| MIG-ORDERS | `orders.payment_link` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.pos_shift` | 24 | scope_path | yes | 10 | 7 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_approval` | 6 | none |  | 10 | 0 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_incident` | 6 | none |  | 10 | 0 | used by the first release |
| MIG-ORDERS | `orders.refund` | 18 | none |  | 4 | 3 | used by the first release |
| MIG-ORDERS | `orders.refund_policy` | 8 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.refund_policy_time_band` | 4 | none |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.resale_listing` | 16 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.reservation` | 7 | venue_id | yes | 5 | 2 | used by the first release |
| MIG-ORDERS | `orders.reservation_line` | 14 | none |  | 2 | 0 | used by the first release |
| MIG-ORDERS | `orders.sales_order` | 20 | scope_path | yes | 32 | 15 | used by the first release |
| MIG-ORDERS | `orders.stored_value_authorisation` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ORDERS | `orders.ticket_template` | 10 | none |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.ticket_template_channel` | 3 | none |  | 2 | 0 | used by the first release |
| MIG-ORDERS | `orders.ticket_transfer` | 12 | none |  | 2 | 2 | used by the first release |
| MIG-ORDERS | `orders.visit_reminder` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.wallet_pass` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.access_attribute` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.access_device` | 30 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.access_incident` | 12 | scope_path | yes | 0 | 1 | used by the first release |
| MIG-ACCESS | `access.access_point` | 17 | scope_path | yes | 11 | 5 | used by the first release |
| MIG-ACCESS | `access.access_point_group` | 8 | scope_path | yes | 4 | 2 | used by the first release |
| MIG-ACCESS | `access.accreditation_credential` | 12 | scope_path |  | 1 | 0 | used by the first release |
| MIG-ACCESS | `access.admission_rules` | 21 | scope_path |  | 5 | 3 | used by the first release |
| MIG-ACCESS | `access.biometric_audit_event` | 18 | scope_path | yes | 0 | 2 | used by the first release |
| MIG-ACCESS | `access.biometric_profile` | 37 | scope_path | yes | 6 | 4 | used by the first release |
| MIG-ACCESS | `access.blacklist` | 10 | scope_path |  | 3 | 1 | used by the first release |
| MIG-ACCESS | `access.configuration_change` | 11 | scope_path |  | 0 | 22 | used by the first release |
| MIG-ACCESS | `access.credential_policy` | 32 | scope_path |  | 4 | 3 | used by the first release |
| MIG-ACCESS | `access.device_binding` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.dynamic_policy` | 20 | scope_path |  | 5 | 3 | used by the first release |
| MIG-ACCESS | `access.dynamic_policy_version` | 10 | scope_path |  | 1 | 3 | used by the first release |
| MIG-ACCESS | `access.entitlement` | 26 | scope_path |  | 19 | 7 | used by the first release |
| MIG-ACCESS | `access.entry_rule_point` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.face_reenrolment_attempt` | 15 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_change` | 11 | scope_path | yes | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_policy` | 12 | scope_path | yes | 3 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_entitlement` | 12 | none |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_facility` | 13 | venue_id | yes | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.scan_event` | 22 | scope_path | yes | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.agent_availability` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.attribution_touch` | 8 | none |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.booking_consent_record` | 20 | scope_path |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.campaign` | 22 | venue_id |  | 5 | 4 | used by the first release |
| MIG-MARKETING | `marketing.campaign_target` | 7 | none |  | 0 | 2 | used by the first release |
| MIG-MARKETING | `marketing.campaign_variant` | 10 | scope_path |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.case` | 23 | venue_id |  | 6 | 2 | used by the first release |
| MIG-MARKETING | `marketing.case_message` | 11 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge_progress` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-MARKETING | `marketing.consent_propagation` | 9 | none |  | 0 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose` | 8 | none |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose_channel` | 3 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_question` | 11 | scope_path |  | 12 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_question_version` | 6 | none |  | 11 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_record` | 11 | none |  | 8 | 5 | used by the first release |
| MIG-MARKETING | `marketing.conversation` | 21 | venue_id |  | 2 | 2 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message` | 8 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message_attachment` | 4 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.cookie_banner_design` | 18 | scope_path |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.device_consent` | 16 | scope_path |  | 4 | 2 | used by the first release |
| MIG-MARKETING | `marketing.device_consent_category` | 4 | none |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition` | 15 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition_field` | 23 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_submission` | 12 | none |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.guest_device` | 14 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_document` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_preference` | 7 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_profile` | 23 | none |  | 12 | 5 | used by the first release |
| MIG-MARKETING | `marketing.invitation` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.invitation_campaign` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.journey` | 9 | scope_path |  | 0 | 0 | referenced by marketing.attribution_touch |
| MIG-MARKETING | `marketing.loyalty_position` | 12 | none |  | 5 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_programme` | 7 | venue_id |  | 5 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_rule` | 9 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.message_dispatch` | 18 | none |  | 2 | 5 | used by the first release |
| MIG-MARKETING | `marketing.message_template` | 12 | none |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.message_template_version` | 16 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.points_earning_rule` | 6 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.points_redemption_rule` | 13 | none |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.privacy_notice_governance` | 14 | scope_path |  | 0 | 1 | used by the first release |
| MIG-MARKETING | `marketing.programme_tier` | 11 | none |  | 3 | 2 | used by the first release |
| MIG-MARKETING | `marketing.referral` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.review` | 13 | venue_id | yes | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.segment` | 9 | venue_id |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.segment_criterion` | 6 | none |  | 4 | 4 | used by the first release |
| MIG-MARKETING | `marketing.subscription` | 8 | none |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.tracking_technology` | 23 | scope_path |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.wishlist_item` | 12 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.cold_chain_event` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.corrective_action` | 13 | scope_path |  | 4 | 4 | used by the first release |
| MIG-FNB | `fnb.course_rule` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.delivery_location` | 11 | venue_id | yes | 6 | 2 | used by the first release |
| MIG-FNB | `fnb.delivery_location_outlet` | 3 | none |  | 2 | 2 | used by the first release |
| MIG-FNB | `fnb.delivery_policy` | 16 | scope_path |  | 4 | 1 | used by the first release |
| MIG-FNB | `fnb.dining_table` | 8 | none |  | 10 | 3 | used by the first release |
| MIG-FNB | `fnb.kitchen_exception` | 9 | none |  | 1 | 2 | used by the first release |
| MIG-FNB | `fnb.kitchen_station` | 8 | none |  | 6 | 2 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket` | 15 | none |  | 18 | 9 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket_line` | 14 | none |  | 15 | 2 | used by the first release |
| MIG-FNB | `fnb.location_session` | 10 | venue_id |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.menu` | 8 | none |  | 6 | 3 | used by the first release |
| MIG-FNB | `fnb.menu_item` | 15 | none |  | 13 | 5 | used by the first release |
| MIG-FNB | `fnb.menu_item_modifier` | 5 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.menu_section` | 5 | none |  | 5 | 3 | used by the first release |
| MIG-FNB | `fnb.modifier_group` | 6 | scope_path |  | 4 | 1 | used by the first release |
| MIG-FNB | `fnb.modifier_option` | 7 | none |  | 3 | 1 | used by the first release |
| MIG-FNB | `fnb.order_fulfilment` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.production_plan` | 6 | none |  | 3 | 2 | used by the first release |
| MIG-FNB | `fnb.production_plan_line` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.production_run` | 11 | none |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.recipe` | 4 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.recipe_ingredient` | 6 | none |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.reservation_table` | 4 | none |  | 4 | 2 | used by the first release |
| MIG-FNB | `fnb.service_order` | 15 | none |  | 12 | 7 | used by the first release |
| MIG-FNB | `fnb.service_order_line` | 12 | none |  | 8 | 1 | used by the first release |
| MIG-FNB | `fnb.sold_out_item` | 9 | none |  | 1 | 0 | used by the first release |
| MIG-FNB | `fnb.table_combination` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.table_reservation` | 21 | none |  | 4 | 3 | used by the first release |
| MIG-FNB | `fnb.table_session` | 9 | none |  | 2 | 2 | used by the first release |
| MIG-FNB | `fnb.table_visit` | 14 | none |  | 5 | 5 | used by the first release |
| MIG-FNB | `fnb.temperature_log` | 11 | none |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.waitlist_entry` | 11 | none |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.dunning_case` | 14 | scope_path |  | 4 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment_plan` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment_policy` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.method` | 16 | scope_path |  | 0 | 0 | referenced by payments.payment_attempt |
| MIG-PAYMENTS | `payments.payment_attempt` | 19 | scope_path |  | 0 | 2 | used by the first release |
| MIG-PAYMENTS | `payments.provider` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.provider_connection` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.routing_rule` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.stored_forward` | 9 | scope_path |  | 2 | 0 | used by the first release |
| MIG-PAYMENTS | `payments.token` | 9 | none |  | 4 | 1 | used by the first release |
| MIG-QUEUE | `queue.entry` | 22 | none |  | 5 | 2 | used by the first release |
| MIG-QUEUE | `queue.feed` | 7 | none |  | 2 | 1 | used by the first release |
| MIG-QUEUE | `queue.queue` | 40 | venue_id | yes | 7 | 2 | used by the first release |
| MIG-QUEUE | `queue.queue_operating_window` | 4 | none |  | 4 | 1 | used by the first release |
| MIG-QUEUE | `queue.reading` | 8 | none |  | 5 | 0 | used by the first release |
| MIG-RETAIL | `retail.merchandise` | 16 | none |  | 5 | 2 | used by the first release |
| MIG-RETAIL | `retail.reservation` | 8 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.reservation_line` | 5 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_line` | 9 | none |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_policy` | 10 | none |  | 2 | 1 | used by the first release |
| MIG-RETAIL | `retail.sale` | 13 | none |  | 5 | 2 | used by the first release |
| MIG-RETAIL | `retail.sale_line` | 13 | none |  | 4 | 1 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop` | 15 | venue_id |  | 1 | 0 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop_line` | 7 | none |  | 1 | 0 | used by the first release |
| MIG-VENUEMAP | `venuemap.import_job` | 11 | none |  | 2 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.map` | 15 | scope_path | yes | 9 | 2 | used by the first release |
| MIG-VENUEMAP | `venuemap.map_version` | 7 | none |  | 2 | 0 | used by the first release |
| MIG-VENUEMAP | `venuemap.path` | 10 | none |  | 6 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.placed_resource` | 11 | none |  | 4 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.point` | 20 | none |  | 9 | 2 | used by the first release |
| MIG-VENUEMAP | `venuemap.visit_plan` | 13 | scope_path | yes | 6 | 3 | used by the first release |
| MIG-VENUEMAP | `venuemap.visit_plan_item` | 18 | none |  | 6 | 2 | used by the first release |

## Used by the release but not a table

- `identity.guest_session`: Redis. `GuestSession` declares `persistence: none — Redis session registry`. Separate from the staff session by lifetime and auth path, and neither is a row. Ha
- `identity.session`: Redis, not Postgres. `ActiveSession` and `Session` both declare `persistence: none — Redis session registry`, and ADR-0004 makes a session a token with a validi
- `inventory.stock_level`: Derived from movements, not stored. `StockPosition` declares `persistence: none — derived from movements`, which is the correct design: a stored level and a mov
