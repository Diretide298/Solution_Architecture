# Database migrations for the first release

**493 tables in 34 migrations.** Every table the first release reads or writes, plus every table their foreign keys reach. The DDL for all of them already exists in `backend/`; each migration takes its schema's tables from there, with the matching foreign keys, indexes and row-level security, and a ROLLBACK section tested in CI (`backend/MIGRATIONS.md`). Generated; do not edit.

Each migration only references tables created by the ones above it. Keys that would point forward are added by the last migration.

## Order

| Order | File | Task | Database | Schema | Tables | Columns | References | Assignee | Points |
|---|---|---|---|---|---|---|---|---|---|
| 0 | `V0001__baseline.sql` | MIG-BASELINE | both | (baseline) | 0 | 0 |  | Hrushikant Patkar | 3 |
| 1 | `V0002__control.sql` | MIG-CONTROL | control | control | 21 | 325 |  | Pranay Shinde | 8 |
| 2 | `V0003__kernel.sql` | MIG-KERNEL | tenant | kernel | 1 | 3 |  | Hrushikant Patkar | 1 |
| 3 | `V0004__tenancy.sql` | MIG-TENANCY | tenant | tenancy | 1 | 12 |  | Hrushikant Patkar | 1 |
| 4 | `V0005__subscription.sql` | MIG-SUBSCRIPTION | tenant | subscription | 5 | 52 | platform | Pranay Shinde | 3 |
| 5 | `V0006__transport.sql` | MIG-TRANSPORT | tenant | transport | 12 | 109 | assets | Hrushikant Patkar | 8 |
| 6 | `V0007__pii.sql` | MIG-PII | tenant | pii | 5 | 54 | access, marketing | Pranay Shinde | 3 |
| 7 | `V0008__games.sql` | MIG-GAMES | tenant | games | 2 | 17 | pii, platform | Hrushikant Patkar | 2 |
| 8 | `V0009__identity.sql` | MIG-IDENTITY | tenant | identity | 18 | 157 | pii, platform | Pranay Shinde | 8 |
| 9 | `V0010__approvals.sql` | MIG-APPROVALS | tenant | approvals | 6 | 108 | identity | Hrushikant Patkar | 5 |
| 10 | `V0011__reporting.sql` | MIG-REPORTING | tenant | reporting | 15 | 160 | identity, platform | Tanmay Dukhande | 8 |
| 11 | `V0012__sync.sql` | MIG-SYNC | tenant | sync | 1 | 11 | identity, platform | Hrushikant Patkar | 1 |
| 12 | `V0013__assets.sql` | MIG-ASSETS | tenant | assets | 7 | 74 | identity, platform | Hrushikant Patkar | 5 |
| 13 | `V0014__ai.sql` | MIG-AI | tenant | ai | 49 | 714 | assets, identity, pii, platform | Tanmay Dukhande | 8 |
| 14 | `V0015__resources.sql` | MIG-RESOURCES | tenant | resources | 7 | 89 | identity, orders, pii, platform | Hrushikant Patkar | 5 |
| 15 | `V0016__whitelabel.sql` | MIG-WHITELABEL | tenant | whitelabel | 29 | 270 | identity, platform, promotions | Tanmay Dukhande | 8 |
| 16 | `V0017__platform.sql` | MIG-PLATFORM | tenant | platform | 17 | 204 | access, approvals, identity, inventory, ledger | Hrushikant Patkar | 8 |
| 17 | `V0018__workforce.sql` | MIG-WORKFORCE | tenant | workforce | 3 | 39 | access, identity, platform | Hrushikant Patkar | 2 |
| 18 | `V0019__seating.sql` | MIG-SEATING | tenant | seating | 10 | 82 | catalogue, identity, pii, platform | Hrushikant Patkar | 5 |
| 19 | `V0020__maintenance.sql` | MIG-MAINTENANCE | tenant | maintenance | 6 | 148 | access, identity, inventory, platform | Hrushikant Patkar | 5 |
| 20 | `V0021__wallet.sql` | MIG-WALLET | tenant | wallet | 22 | 204 | identity, orders, pii, platform | Pranay Shinde | 8 |
| 21 | `V0022__catalogue.sql` | MIG-CATALOGUE | tenant | catalogue | 22 | 310 | access, identity, ledger, platform, seating | Hrushikant Patkar | 8 |
| 22 | `V0023__ledger.sql` | MIG-LEDGER | tenant | ledger | 18 | 271 | catalogue, identity, orders, platform | Tanmay Dukhande | 8 |
| 23 | `V0024__inventory.sql` | MIG-INVENTORY | tenant | inventory | 12 | 172 | identity, ledger, platform | Pranay Shinde | 8 |
| 24 | `V0025__promotions.sql` | MIG-PROMOTIONS | tenant | promotions | 16 | 182 | ledger, orders, pii, platform | Hrushikant Patkar | 8 |
| 25 | `V0026__orders.sql` | MIG-ORDERS | tenant | orders | 39 | 474 | access, catalogue, identity, ledger, pii, platform, promotions | Pranay Shinde | 8 |
| 26 | `V0027__access.sql` | MIG-ACCESS | tenant | access | 19 | 324 | catalogue, identity, orders, pii, platform | Hrushikant Patkar | 8 |
| 27 | `V0028__marketing.sql` | MIG-MARKETING | tenant | marketing | 55 | 672 | ai, catalogue, identity, ledger, orders, pii, platform | Pranay Shinde | 8 |
| 28 | `V0029__fnb.sql` | MIG-FNB | tenant | fnb | 41 | 397 | access, catalogue, identity, inventory, orders, pii, platform, seating | Tanmay Dukhande | 8 |
| 29 | `V0030__payments.sql` | MIG-PAYMENTS | tenant | payments | 12 | 141 | marketing, orders, pii | Pranay Shinde | 8 |
| 30 | `V0031__queue.sql` | MIG-QUEUE | tenant | queue | 4 | 77 | access, catalogue, maintenance, pii, platform | Hrushikant Patkar | 3 |
| 31 | `V0032__retail.sql` | MIG-RETAIL | tenant | retail | 10 | 110 | access, catalogue, fnb, identity, inventory, orders, pii, platform | Hrushikant Patkar | 5 |
| 32 | `V0033__venuemap.sql` | MIG-VENUEMAP | tenant | venuemap | 8 | 118 | access, assets, catalogue, marketing, orders, platform, promotions, resources | Hrushikant Patkar | 5 |
| 33 | `V0034__cross_schema_foreign_keys.sql` | MIG-FOREIGN-KEYS | tenant | (cross-schema) | 0 | 0 |  | Hrushikant Patkar | 2 |

## Tables

| Migration | Table | Columns | Row-level security | Partitioned | Read by | Written by | Why |
|---|---|---|---|---|---|---|---|
| MIG-CONTROL | `control.api_client` | 14 | none |  | 5 | 4 | used by the first release |
| MIG-CONTROL | `control.api_licence` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-CONTROL | `control.api_version` | 9 | none |  | 2 | 1 | used by the first release |
| MIG-CONTROL | `control.cell_tenant` | 10 | none |  | 0 | 0 | referenced by control.outbox_relay |
| MIG-CONTROL | `control.content_block` | 12 | scope_path |  | 6 | 3 | used by the first release |
| MIG-CONTROL | `control.developer_account` | 8 | none |  | 3 | 2 | used by the first release |
| MIG-CONTROL | `control.developer_member` | 7 | none |  | 1 | 1 | used by the first release |
| MIG-CONTROL | `control.integration_listing` | 12 | none |  | 3 | 1 | used by the first release |
| MIG-CONTROL | `control.invoice` | 14 | none |  | 0 | 0 | referenced by control.invoice_line |
| MIG-CONTROL | `control.invoice_line` | 10 | none |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.licence_add_on` | 7 | none |  | 4 | 1 | used by the first release |
| MIG-CONTROL | `control.licence_add_on_limit` | 6 | none |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.outbox_relay` | 6 | none |  | 0 | 0 | kernel machinery: the relay lease per tenant database (ADR-0058; PLATFORM-OUTBOX) |
| MIG-CONTROL | `control.partner` | 28 | scope_path |  | 0 | 0 | referenced by control.partner_agreement |
| MIG-CONTROL | `control.partner_agreement` | 53 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_application` | 31 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.partner_change_request` | 28 | scope_path |  | 0 | 1 | used by the first release |
| MIG-CONTROL | `control.production_access_request` | 14 | none |  | 1 | 1 | used by the first release |
| MIG-CONTROL | `control.seo_metadata` | 15 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CONTROL | `control.tenant` | 23 | none |  | 9 | 5 | used by the first release |
| MIG-CONTROL | `control.url_redirect` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-KERNEL | `kernel.inbox` | 3 | tenant root (one tenant per database; no tenant_id by design) | yes | 0 | 0 | kernel machinery: the inbox per tenant database (ADR-0058; PLATFORM-OUTBOX, MIG-PARTITIONS) |
| MIG-TENANCY | `tenancy.device_assignment` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.contract` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.module_listing` | 15 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan` | 16 | tenant root (one tenant per database; no tenant_id by design) |  | 6 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_limit` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 2 | used by the first release |
| MIG-SUBSCRIPTION | `subscription.plan_module` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.departure` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.fare_matrix_cell` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 7 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_passenger_type` | 11 | tenant root (one tenant per database; no tenant_id by design) |  | 6 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.fare_table` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 8 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.favourite_route` | 9 | venue_id |  | 3 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.network_import` | 10 | venue_id |  | 2 | 1 | used by the first release |
| MIG-TRANSPORT | `transport.pass_type` | 14 | venue_id |  | 4 | 2 | used by the first release |
| MIG-TRANSPORT | `transport.route` | 12 | venue_id |  | 12 | 4 | used by the first release |
| MIG-TRANSPORT | `transport.route_stop` | 7 | through its owner |  | 11 | 3 | used by the first release |
| MIG-TRANSPORT | `transport.station` | 8 | venue_id |  | 13 | 3 | used by the first release |
| MIG-TRANSPORT | `transport.timetable` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 7 | 4 | used by the first release |
| MIG-TRANSPORT | `transport.timetable_run` | 4 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 2 | used by the first release |
| MIG-PII | `pii.consent_identifier` | 6 | scope_path |  | 0 | 1 | used by the first release |
| MIG-PII | `pii.subject` | 13 | tenant root (one tenant per database; no tenant_id by design) |  | 20 | 7 | used by the first release |
| MIG-PII | `pii.subject_biometric` | 15 | through its owner |  | 4 | 3 | used by the first release |
| MIG-PII | `pii.subject_contact` | 10 | subject |  | 6 | 2 | used by the first release |
| MIG-PII | `pii.subject_document` | 10 | subject |  | 0 | 2 | used by the first release |
| MIG-GAMES | `games.card` | 15 | venue_id |  | 3 | 2 | used by the first release |
| MIG-GAMES | `games.credit_ledger` | 2 | through its owner |  | 1 | 0 | used by the first release |
| MIG-IDENTITY | `identity.capability_template` | 9 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.delegated_access` | 21 | scope_path |  | 14 | 2 | used by the first release |
| MIG-IDENTITY | `identity.guest_credential` | 6 | subject |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.guest_identity_verification` | 13 | subject |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.guest_verification_policy` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.mfa_challenge` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.mfa_method` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 11 | 3 | used by the first release |
| MIG-IDENTITY | `identity.mfa_recovery_code` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.otp_challenge` | 2 | subject |  | 2 | 2 | used by the first release |
| MIG-IDENTITY | `identity.password_policy` | 13 | scope_path |  | 3 | 1 | used by the first release |
| MIG-IDENTITY | `identity.platform_staff_grant` | 9 | scope_path |  | 2 | 1 | used by the first release |
| MIG-IDENTITY | `identity.principal` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 24 | 1 | used by the first release |
| MIG-IDENTITY | `identity.principal_credential` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 1 | used by the first release |
| MIG-IDENTITY | `identity.refresh_token` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 2 | used by the first release |
| MIG-IDENTITY | `identity.role` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 8 | 2 | used by the first release |
| MIG-IDENTITY | `identity.role_permission` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 2 | used by the first release |
| MIG-IDENTITY | `identity.segregation_rule` | 9 | scope_path |  | 3 | 1 | used by the first release |
| MIG-IDENTITY | `identity.session` | 12 | venue_id |  | 5 | 6 | used by the first release |
| MIG-APPROVALS | `approvals.decision` | 13 | through its owner |  | 3 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.delegation` | 13 | scope_path |  | 4 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.external_provider` | 16 | scope_path |  | 2 | 1 | used by the first release |
| MIG-APPROVALS | `approvals.matrix` | 6 | scope_path |  | 6 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.request` | 30 | scope_path |  | 3 | 2 | used by the first release |
| MIG-APPROVALS | `approvals.rule` | 30 | through its owner |  | 7 | 2 | used by the first release |
| MIG-REPORTING | `reporting.alert` | 18 | scope_path |  | 1 | 0 | used by the first release |
| MIG-REPORTING | `reporting.alert_rule` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-REPORTING | `reporting.dashboard` | 10 | venue_id |  | 6 | 3 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_tile` | 8 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 2 | used by the first release |
| MIG-REPORTING | `reporting.dashboard_view` | 5 | venue_id |  | 0 | 1 | used by the first release |
| MIG-REPORTING | `reporting.execution` | 15 | through its owner |  | 1 | 1 | used by the first release |
| MIG-REPORTING | `reporting.kpi_definition` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-REPORTING | `reporting.natural_language_query` | 9 | scope_path |  | 1 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_column` | 14 | through its owner |  | 6 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_definition` | 16 | scope_path |  | 8 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_definition_version` | 7 | scope_path |  | 1 | 2 | used by the first release |
| MIG-REPORTING | `reporting.report_filter` | 7 | through its owner |  | 6 | 4 | used by the first release |
| MIG-REPORTING | `reporting.report_parameter` | 7 | through its owner |  | 6 | 3 | used by the first release |
| MIG-REPORTING | `reporting.schedule` | 15 | through its owner |  | 0 | 0 | referenced by reporting.execution |
| MIG-REPORTING | `reporting.semantic_model` | 4 | scope_path |  | 2 | 1 | used by the first release |
| MIG-SYNC | `sync.rejection` | 11 | through its owner |  | 1 | 1 | used by the first release |
| MIG-ASSETS | `assets.asset_version` | 11 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_asset` | 25 | venue_id |  | 14 | 3 | used by the first release |
| MIG-ASSETS | `assets.media_collection` | 7 | venue_id |  | 3 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_collection_member` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 2 | used by the first release |
| MIG-ASSETS | `assets.media_fingerprint` | 7 | scope_path |  | 0 | 2 | used by the first release |
| MIG-ASSETS | `assets.media_upload` | 12 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ASSETS | `assets.media_usage` | 7 | through its owner |  | 4 | 1 | used by the first release |
| MIG-AI | `ai.action_plan` | 19 | scope_path |  | 1 | 2 | used by the first release |
| MIG-AI | `ai.activity` | 25 | scope_path |  | 1 | 12 | used by the first release |
| MIG-AI | `ai.anomaly_detector` | 14 | scope_path |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.answer_feedback` | 11 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.assistant_profile` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.byok_enablement` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.capability` | 18 | scope_path |  | 6 | 2 | used by the first release |
| MIG-AI | `ai.capability_maturity` | 9 | scope_path |  | 1 | 0 | used by the first release |
| MIG-AI | `ai.chunk_embedding` | 12 | through its owner |  | 4 | 2 | used by the first release |
| MIG-AI | `ai.conversation` | 8 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.decision_record` | 25 | scope_path |  | 2 | 15 | used by the first release |
| MIG-AI | `ai.eval_run` | 14 | scope_path |  | 4 | 1 | used by the first release |
| MIG-AI | `ai.eval_suite` | 9 | scope_path |  | 2 | 0 | used by the first release |
| MIG-AI | `ai.forecast_accuracy` | 13 | scope_path |  | 1 | 0 | used by the first release |
| MIG-AI | `ai.forecast_definition` | 20 | scope_path |  | 4 | 3 | used by the first release |
| MIG-AI | `ai.forecast_point` | 12 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.forecast_scenario` | 8 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.forecast_version` | 18 | scope_path |  | 7 | 2 | used by the first release |
| MIG-AI | `ai.governance_alert` | 14 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.governance_policy` | 9 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.governance_policy_version` | 12 | scope_path |  | 7 | 3 | used by the first release |
| MIG-AI | `ai.guided_choice_suggestion` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.history_import` | 18 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.history_observation` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.inbox` | 3 | tenant root (one tenant per database; no tenant_id by design) | yes | 0 | 0 | kernel machinery: the AI consumers' inbox, since only AI writes AI tables (ADR-0058, ADR-0020) |
| MIG-AI | `ai.incident` | 19 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.index_entry` | 2 | through its owner |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.index_job` | 14 | through its owner |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.index_source` | 15 | through its owner |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.insight` | 22 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.intervention` | 11 | scope_path |  | 1 | 3 | used by the first release |
| MIG-AI | `ai.knowledge_collection` | 12 | scope_path |  | 4 | 1 | used by the first release |
| MIG-AI | `ai.knowledge_document` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.knowledge_gap` | 13 | scope_path |  | 0 | 2 | used by the first release |
| MIG-AI | `ai.message` | 15 | through its owner |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.model` | 19 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.operational_requirement` | 17 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.policy` | 32 | scope_path |  | 15 | 4 | used by the first release |
| MIG-AI | `ai.policy_exception` | 13 | scope_path |  | 3 | 2 | used by the first release |
| MIG-AI | `ai.prompt_template` | 13 | scope_path |  | 3 | 1 | used by the first release |
| MIG-AI | `ai.proposed_action` | 19 | scope_path |  | 3 | 5 | used by the first release |
| MIG-AI | `ai.provider` | 27 | scope_path |  | 10 | 1 | used by the first release |
| MIG-AI | `ai.rec_decision` | 19 | scope_path |  | 1 | 1 | used by the first release |
| MIG-AI | `ai.rec_decline` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.rec_event` | 11 | scope_path |  | 0 | 1 | used by the first release |
| MIG-AI | `ai.release` | 18 | scope_path |  | 7 | 5 | used by the first release |
| MIG-AI | `ai.suggestion` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-AI | `ai.training_run` | 17 | scope_path |  | 1 | 0 | used by the first release |
| MIG-AI | `ai.venue_settings` | 14 | scope_path |  | 4 | 1 | used by the first release |
| MIG-RESOURCES | `resources.booking` | 16 | through its owner |  | 4 | 0 | used by the first release |
| MIG-RESOURCES | `resources.resource` | 17 | scope_path |  | 8 | 4 | used by the first release |
| MIG-RESOURCES | `resources.resource_block` | 8 | scope_path |  | 6 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_hold` | 15 | scope_path |  | 7 | 3 | used by the first release |
| MIG-RESOURCES | `resources.resource_package` | 13 | scope_path |  | 2 | 2 | used by the first release |
| MIG-RESOURCES | `resources.resource_requirement` | 12 | scope_path |  | 4 | 3 | used by the first release |
| MIG-RESOURCES | `resources.resource_schedule` | 8 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.analytics_provider` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.app_build` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.banner` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.booking_flow` | 10 | scope_path |  | 15 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.booking_flow_step` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 10 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.config_version` | 13 | scope_path |  | 8 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.content_page` | 11 | scope_path |  | 5 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.custom_domain` | 18 | tenant root (one tenant per database; no tenant_id by design) |  | 6 | 5 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_category` | 5 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.faq_entry` | 6 | through its owner |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.feature_toggle` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config` | 4 | scope_path |  | 4 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_column` | 3 | through its owner |  | 4 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.footer_config_social_link` | 4 | through its owner |  | 4 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice` | 13 | venue_id |  | 8 | 6 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_answer` | 12 | through its owner |  | 10 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.guided_choice_question` | 5 | through its owner |  | 8 | 4 | used by the first release |
| MIG-WHITELABEL | `whitelabel.homepage_layout` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 6 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.homepage_section` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 7 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.module_enablement` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.navigation_config` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.navigation_item` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 2 | used by the first release |
| MIG-WHITELABEL | `whitelabel.policy` | 10 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.promo_block` | 11 | scope_path |  | 5 | 3 | used by the first release |
| MIG-WHITELABEL | `whitelabel.publish_review_policy` | 5 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.site_package` | 9 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.site_setup_progress` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.store_account` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-WHITELABEL | `whitelabel.tenant_config` | 27 | tenant root (one tenant per database; no tenant_id by design) |  | 24 | 12 | used by the first release |
| MIG-PLATFORM | `platform.audit_record` | 8 | tenant root (one tenant per database; no tenant_id by design) | yes | 0 | 4 | used by the first release |
| MIG-PLATFORM | `platform.denomination` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-PLATFORM | `platform.device` | 41 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 1 | used by the first release |
| MIG-PLATFORM | `platform.device_heartbeat` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-PLATFORM | `platform.dsar_request` | 7 | through its owner |  | 0 | 2 | used by the first release |
| MIG-PLATFORM | `platform.guest_link` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by platform.dsar_request |
| MIG-PLATFORM | `platform.idempotency_record` | 11 | scope_path |  | 0 | 6 | used by the first release |
| MIG-PLATFORM | `platform.outbox` | 15 | scope_path | yes | 0 | 46 | used by the first release |
| MIG-PLATFORM | `platform.outlet` | 16 | venue_id |  | 10 | 2 | used by the first release |
| MIG-PLATFORM | `platform.region_settings` | 19 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board` | 6 | venue_id |  | 4 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board_page` | 4 | through its owner |  | 1 | 2 | used by the first release |
| MIG-PLATFORM | `platform.sale_board_tile` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 2 | used by the first release |
| MIG-PLATFORM | `platform.scope` | 8 | none |  | 9 | 2 | used by the first release |
| MIG-PLATFORM | `platform.tenant` | 2 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by whitelabel.tenant_config |
| MIG-PLATFORM | `platform.venue_settings` | 31 | venue_id |  | 5 | 2 | used by the first release |
| MIG-PLATFORM | `platform.workstation` | 20 | scope_path |  | 7 | 1 | used by the first release |
| MIG-WORKFORCE | `workforce.attendance` | 15 | venue_id |  | 1 | 1 | used by the first release |
| MIG-WORKFORCE | `workforce.attendance_amendment` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-WORKFORCE | `workforce.rota_assignment` | 17 | venue_id |  | 4 | 2 | used by the first release |
| MIG-SEATING | `seating.accessible` | 5 | scope_path |  | 2 | 1 | used by the first release |
| MIG-SEATING | `seating.recommendation_rules` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-SEATING | `seating.seat` | 11 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 0 | used by the first release |
| MIG-SEATING | `seating.seat_block` | 10 | scope_path |  | 0 | 0 | referenced by seating.seat_hold |
| MIG-SEATING | `seating.seat_block_item` | 4 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-SEATING | `seating.seat_category` | 7 | venue_id |  | 4 | 1 | used by the first release |
| MIG-SEATING | `seating.seat_hold` | 12 | through its owner |  | 6 | 4 | used by the first release |
| MIG-SEATING | `seating.seat_hold_item` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-SEATING | `seating.seat_map` | 12 | venue_id |  | 0 | 0 | referenced by catalogue.performance |
| MIG-SEATING | `seating.seat_price_band` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 2 | used by the first release |
| MIG-MAINTENANCE | `maintenance.asset` | 30 | venue_id |  | 0 | 0 | referenced by queue.queue |
| MIG-MAINTENANCE | `maintenance.incident` | 28 | venue_id |  | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.inspection` | 14 | venue_id |  | 0 | 0 | referenced by maintenance.work_order |
| MIG-MAINTENANCE | `maintenance.inspection_template` | 9 | venue_id |  | 2 | 1 | used by the first release |
| MIG-MAINTENANCE | `maintenance.inspection_template_item` | 11 | through its owner |  | 1 | 1 | used by the first release |
| MIG-MAINTENANCE | `maintenance.work_order` | 56 | venue_id |  | 2 | 0 | used by the first release |
| MIG-WALLET | `wallet.accounting_mapping` | 3 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.authentication_policy` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.auto_reload_setting` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.balance` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 2 | used by the first release |
| MIG-WALLET | `wallet.channel_rules` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-WALLET | `wallet.configuration_version_snapshot` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.consumption_policy` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.credit_lot` | 12 | scope_path |  | 5 | 2 | used by the first release |
| MIG-WALLET | `wallet.credit_type` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.exit_settlement` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.funding_rules` | 11 | scope_path |  | 3 | 2 | used by the first release |
| MIG-WALLET | `wallet.gift_card` | 11 | subject |  | 1 | 0 | used by the first release |
| MIG-WALLET | `wallet.hold` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by wallet.wallet_transaction |
| MIG-WALLET | `wallet.integration_mapping` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.reconciliation_source` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.refund_policy` | 8 | scope_path |  | 4 | 2 | used by the first release |
| MIG-WALLET | `wallet.risk_rules` | 2 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.transfer_rules` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-WALLET | `wallet.wallet` | 9 | subject |  | 8 | 4 | used by the first release |
| MIG-WALLET | `wallet.wallet_transaction` | 12 | venue_id |  | 2 | 4 | used by the first release |
| MIG-WALLET | `wallet.wallet_type` | 25 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.alternative_code` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_allocation` | 19 | through its owner |  | 2 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.channel_capacity` | 12 | through its owner |  | 11 | 5 | used by the first release |
| MIG-CATALOGUE | `catalogue.entitlement_template` | 32 | scope_path |  | 8 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.event` | 10 | scope_path |  | 9 | 4 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_capacity_profile` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_registration` | 7 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_resource_plan` | 4 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.event_schedule` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.group_package` | 11 | scope_path |  | 4 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.import_job` | 25 | scope_path |  | 1 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.inventory_hold` | 18 | through its owner |  | 9 | 10 | used by the first release |
| MIG-CATALOGUE | `catalogue.performance` | 11 | through its owner |  | 13 | 4 | used by the first release |
| MIG-CATALOGUE | `catalogue.price` | 5 | through its owner |  | 2 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.price_list` | 28 | venue_id |  | 9 | 5 | used by the first release |
| MIG-CATALOGUE | `catalogue.product` | 42 | scope_path |  | 31 | 4 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_category` | 12 | scope_path |  | 6 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_eligibility_rule` | 15 | scope_path |  | 8 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_media` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.product_version` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 2 | used by the first release |
| MIG-CATALOGUE | `catalogue.published_bundle` | 10 | venue_id |  | 3 | 1 | used by the first release |
| MIG-CATALOGUE | `catalogue.variant` | 9 | through its owner |  | 10 | 3 | used by the first release |
| MIG-LEDGER | `ledger.account` | 15 | through its owner |  | 0 | 0 | referenced by inventory.supplier |
| MIG-LEDGER | `ledger.cost_center` | 6 | venue_id |  | 0 | 0 | referenced by marketing.invitation |
| MIG-LEDGER | `ledger.credit_memo` | 30 | scope_path |  | 5 | 1 | used by the first release |
| MIG-LEDGER | `ledger.credit_memo_line` | 10 | through its owner |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.einvoice_transmission` | 17 | scope_path |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.einvoicing_provider` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-LEDGER | `ledger.fiscal_period` | 9 | through its owner |  | 0 | 0 | referenced by ledger.journal_entry |
| MIG-LEDGER | `ledger.fx_provider_assignment` | 6 | scope_path |  | 1 | 1 | used by the first release |
| MIG-LEDGER | `ledger.fx_rate` | 13 | through its owner |  | 7 | 2 | used by the first release |
| MIG-LEDGER | `ledger.journal_entry` | 20 | through its owner |  | 0 | 5 | used by the first release |
| MIG-LEDGER | `ledger.journal_line` | 9 | venue_id | yes | 0 | 2 | used by the first release |
| MIG-LEDGER | `ledger.legal_entity` | 11 | scope_path |  | 3 | 1 | used by the first release |
| MIG-LEDGER | `ledger.posting` | 12 | venue_id |  | 1 | 1 | used by the first release |
| MIG-LEDGER | `ledger.price_variance` | 15 | venue_id |  | 0 | 1 | used by the first release |
| MIG-LEDGER | `ledger.tax_code` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice` | 39 | scope_path |  | 6 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice_line` | 17 | through its owner |  | 6 | 2 | used by the first release |
| MIG-LEDGER | `ledger.tax_invoice_template` | 18 | scope_path |  | 2 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.goods_receipt` | 11 | through its owner |  | 3 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.goods_receipt_line` | 11 | through its owner |  | 2 | 2 | used by the first release |
| MIG-INVENTORY | `inventory.item` | 26 | venue_id |  | 6 | 3 | used by the first release |
| MIG-INVENTORY | `inventory.kit_component` | 6 | scope_path |  | 3 | 1 | used by the first release |
| MIG-INVENTORY | `inventory.location` | 7 | venue_id |  | 0 | 0 | referenced by platform.outlet |
| MIG-INVENTORY | `inventory.movement` | 17 | through its owner |  | 4 | 3 | used by the first release |
| MIG-INVENTORY | `inventory.purchase_order` | 29 | scope_path |  | 0 | 0 | referenced by inventory.goods_receipt |
| MIG-INVENTORY | `inventory.requisition` | 20 | venue_id |  | 0 | 0 | referenced by inventory.purchase_order |
| MIG-INVENTORY | `inventory.serialised_item` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.stock_batch` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 0 | used by the first release |
| MIG-INVENTORY | `inventory.stock_reservation` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-INVENTORY | `inventory.supplier` | 16 | scope_path |  | 0 | 0 | referenced by inventory.item |
| MIG-PROMOTIONS | `promotions.allocation_component` | 9 | venue_id |  | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.allocation_split` | 4 | through its owner |  | 0 | 0 | referenced by promotions.allocation_component |
| MIG-PROMOTIONS | `promotions.bundle` | 20 | venue_id |  | 5 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_group` | 6 | through its owner |  | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_choice_option` | 5 | through its owner |  | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.bundle_component` | 13 | venue_id |  | 3 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.code_assignment` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_campaign` | 14 | venue_id |  | 3 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code` | 17 | scope_path |  | 4 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.coupon_code_batch` | 11 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion` | 24 | venue_id |  | 13 | 4 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_audit` | 14 | venue_id |  | 0 | 9 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_channel_publication` | 9 | venue_id |  | 2 | 2 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_evaluation_trace` | 9 | venue_id |  | 0 | 3 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_rule` | 13 | venue_id |  | 1 | 0 | used by the first release |
| MIG-PROMOTIONS | `promotions.promotion_variant` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.cart` | 18 | venue_id |  | 11 | 8 | used by the first release |
| MIG-ORDERS | `orders.cart_line` | 21 | through its owner |  | 10 | 6 | used by the first release |
| MIG-ORDERS | `orders.cash_count_line` | 11 | through its owner |  | 6 | 4 | used by the first release |
| MIG-ORDERS | `orders.cash_movement` | 13 | through its owner |  | 4 | 3 | used by the first release |
| MIG-ORDERS | `orders.deposit_box` | 15 | venue_id |  | 4 | 3 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_foreign_holding` | 7 | through its owner |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.deposit_box_opening_denomination` | 4 | through its owner |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.fraud_rule` | 12 | scope_path |  | 3 | 0 | used by the first release |
| MIG-ORDERS | `orders.group_booking` | 21 | through its owner |  | 4 | 1 | used by the first release |
| MIG-ORDERS | `orders.group_customer_organization` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by orders.group_customer_organization_contact |
| MIG-ORDERS | `orders.group_customer_organization_contact` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by orders.group_visit_plan |
| MIG-ORDERS | `orders.group_participant` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-ORDERS | `orders.group_participant_list` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 0 | referenced by orders.group_participant |
| MIG-ORDERS | `orders.group_visit_plan` | 27 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.invitation` | 12 | through its owner |  | 1 | 0 | used by the first release |
| MIG-ORDERS | `orders.no_sale_event` | 8 | through its owner |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.order_event` | 16 | scope_path |  | 0 | 15 | used by the first release |
| MIG-ORDERS | `orders.order_line` | 23 | venue_id |  | 16 | 10 | used by the first release |
| MIG-ORDERS | `orders.order_line_discount` | 6 | through its owner |  | 12 | 3 | used by the first release |
| MIG-ORDERS | `orders.order_line_eligibility` | 7 | through its owner |  | 12 | 1 | used by the first release |
| MIG-ORDERS | `orders.payment` | 18 | through its owner |  | 26 | 17 | used by the first release |
| MIG-ORDERS | `orders.payment_link` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.pos_shift` | 30 | scope_path |  | 12 | 9 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_approval` | 6 | through its owner |  | 12 | 1 | used by the first release |
| MIG-ORDERS | `orders.pos_shift_incident` | 6 | through its owner |  | 12 | 2 | used by the first release |
| MIG-ORDERS | `orders.refund` | 20 | through its owner |  | 4 | 3 | used by the first release |
| MIG-ORDERS | `orders.refund_policy` | 8 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.refund_policy_time_band` | 4 | through its owner |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.resale_listing` | 16 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ORDERS | `orders.reservation` | 7 | venue_id |  | 7 | 4 | used by the first release |
| MIG-ORDERS | `orders.reservation_line` | 14 | through its owner |  | 4 | 1 | used by the first release |
| MIG-ORDERS | `orders.sales_order` | 25 | scope_path |  | 32 | 16 | used by the first release |
| MIG-ORDERS | `orders.stored_value_authorisation` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ORDERS | `orders.ticket_template` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 4 | used by the first release |
| MIG-ORDERS | `orders.ticket_template_channel` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 3 | used by the first release |
| MIG-ORDERS | `orders.ticket_transfer` | 12 | through its owner |  | 3 | 2 | used by the first release |
| MIG-ORDERS | `orders.till_shift_policy` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.visit_reminder` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ORDERS | `orders.wallet_pass` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.access_incident` | 12 | scope_path |  | 0 | 1 | used by the first release |
| MIG-ACCESS | `access.access_point` | 18 | scope_path |  | 12 | 6 | used by the first release |
| MIG-ACCESS | `access.access_point_group` | 8 | scope_path |  | 4 | 2 | used by the first release |
| MIG-ACCESS | `access.admission_rules` | 21 | scope_path |  | 4 | 3 | used by the first release |
| MIG-ACCESS | `access.biometric_audit_event` | 18 | scope_path |  | 0 | 2 | used by the first release |
| MIG-ACCESS | `access.biometric_profile` | 37 | scope_path |  | 6 | 4 | used by the first release |
| MIG-ACCESS | `access.blacklist` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.configuration_change` | 11 | scope_path |  | 0 | 18 | used by the first release |
| MIG-ACCESS | `access.credential_policy` | 32 | scope_path |  | 4 | 3 | used by the first release |
| MIG-ACCESS | `access.device_binding` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.device_placement` | 18 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.entitlement` | 30 | scope_path |  | 19 | 7 | used by the first release |
| MIG-ACCESS | `access.entry_rule_point` | 5 | through its owner |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.face_reenrolment_attempt` | 15 | scope_path |  | 1 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_change` | 13 | scope_path |  | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.gate_mode_policy` | 12 | scope_path |  | 3 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_entitlement` | 12 | subject |  | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.parking_facility` | 14 | venue_id |  | 2 | 1 | used by the first release |
| MIG-ACCESS | `access.scan_event` | 23 | scope_path | yes | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.agent_availability` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.attribution_touch` | 8 | through its owner |  | 2 | 0 | used by the first release |
| MIG-MARKETING | `marketing.booking_consent_record` | 20 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.campaign` | 22 | venue_id |  | 5 | 4 | used by the first release |
| MIG-MARKETING | `marketing.campaign_target` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 2 | used by the first release |
| MIG-MARKETING | `marketing.campaign_variant` | 10 | scope_path |  | 4 | 2 | used by the first release |
| MIG-MARKETING | `marketing.case` | 23 | venue_id |  | 5 | 3 | used by the first release |
| MIG-MARKETING | `marketing.case_message` | 11 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge` | 14 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.challenge_progress` | 9 | through its owner |  | 1 | 0 | used by the first release |
| MIG-MARKETING | `marketing.consent_propagation` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose` | 8 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_purpose_channel` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.consent_question` | 11 | scope_path |  | 12 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_question_version` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 11 | 2 | used by the first release |
| MIG-MARKETING | `marketing.consent_record` | 11 | subject |  | 8 | 6 | used by the first release |
| MIG-MARKETING | `marketing.conversation` | 21 | venue_id |  | 2 | 2 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message` | 8 | through its owner |  | 2 | 2 | used by the first release |
| MIG-MARKETING | `marketing.conversation_message_attachment` | 4 | through its owner |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.cookie_banner_design` | 18 | scope_path |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.customer_badge` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.device_consent` | 16 | scope_path |  | 4 | 2 | used by the first release |
| MIG-MARKETING | `marketing.device_consent_category` | 4 | through its owner |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition` | 16 | scope_path |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.form_definition_field` | 23 | scope_path |  | 3 | 2 | used by the first release |
| MIG-MARKETING | `marketing.form_submission` | 12 | subject |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_device` | 14 | subject |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_document` | 9 | subject |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_preference` | 7 | subject |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.guest_profile` | 23 | through its owner |  | 12 | 5 | used by the first release |
| MIG-MARKETING | `marketing.invitation` | 13 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.invitation_campaign` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.journey` | 9 | scope_path |  | 0 | 0 | referenced by marketing.attribution_touch |
| MIG-MARKETING | `marketing.lost_item` | 17 | venue_id |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_position` | 12 | through its owner |  | 7 | 2 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_programme` | 7 | venue_id |  | 6 | 2 | used by the first release |
| MIG-MARKETING | `marketing.loyalty_rule` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.message_dispatch` | 18 | subject | yes | 2 | 5 | used by the first release |
| MIG-MARKETING | `marketing.message_template` | 12 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 2 | used by the first release |
| MIG-MARKETING | `marketing.message_template_version` | 16 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 2 | used by the first release |
| MIG-MARKETING | `marketing.points_earning_rule` | 6 | through its owner |  | 3 | 2 | used by the first release |
| MIG-MARKETING | `marketing.points_redemption_rule` | 13 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.privacy_notice_governance` | 14 | scope_path |  | 0 | 1 | used by the first release |
| MIG-MARKETING | `marketing.programme_tier` | 11 | through its owner |  | 4 | 2 | used by the first release |
| MIG-MARKETING | `marketing.referral` | 10 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.review` | 13 | venue_id |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.reward` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.segment` | 14 | venue_id |  | 3 | 1 | used by the first release |
| MIG-MARKETING | `marketing.segment_criterion` | 6 | through its owner |  | 4 | 4 | used by the first release |
| MIG-MARKETING | `marketing.subscription` | 8 | subject |  | 2 | 1 | used by the first release |
| MIG-MARKETING | `marketing.tracking_technology` | 23 | scope_path |  | 4 | 1 | used by the first release |
| MIG-MARKETING | `marketing.waiver_field_rule` | 5 | through its owner |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.waiver_requirement` | 30 | scope_path |  | 1 | 1 | used by the first release |
| MIG-MARKETING | `marketing.waiver_requirement_event` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-MARKETING | `marketing.wishlist_item` | 12 | subject |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.allergen_verdict` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.bill_split` | 3 | through its owner |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.cold_chain_event` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.corrective_action` | 13 | scope_path |  | 4 | 4 | used by the first release |
| MIG-FNB | `fnb.course_rule` | 7 | scope_path |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.delivery_location` | 12 | venue_id |  | 7 | 2 | used by the first release |
| MIG-FNB | `fnb.delivery_location_outlet` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 2 | used by the first release |
| MIG-FNB | `fnb.delivery_policy` | 16 | scope_path |  | 4 | 1 | used by the first release |
| MIG-FNB | `fnb.dining_table` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 10 | 3 | used by the first release |
| MIG-FNB | `fnb.kitchen_exception` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 2 | used by the first release |
| MIG-FNB | `fnb.kitchen_sla` | 3 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.kitchen_station` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 5 | 1 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket` | 16 | through its owner |  | 22 | 9 | used by the first release |
| MIG-FNB | `fnb.kitchen_ticket_line` | 14 | through its owner |  | 19 | 3 | used by the first release |
| MIG-FNB | `fnb.location_session` | 10 | venue_id |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.menu` | 8 | through its owner |  | 7 | 6 | used by the first release |
| MIG-FNB | `fnb.menu_item` | 17 | through its owner |  | 14 | 6 | used by the first release |
| MIG-FNB | `fnb.menu_item_modifier` | 5 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.menu_schedule` | 9 | scope_path |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.menu_section` | 5 | through its owner |  | 5 | 3 | used by the first release |
| MIG-FNB | `fnb.menu_version` | 12 | scope_path |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.modifier_group` | 6 | scope_path |  | 4 | 1 | used by the first release |
| MIG-FNB | `fnb.modifier_option` | 7 | through its owner |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.order_fulfilment` | 10 | scope_path |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.production_plan` | 6 | tenant root (one tenant per database; no tenant_id by design) |  | 3 | 2 | used by the first release |
| MIG-FNB | `fnb.production_plan_line` | 7 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.production_run` | 11 | through its owner |  | 0 | 1 | used by the first release |
| MIG-FNB | `fnb.recipe` | 4 | through its owner |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.recipe_ingredient` | 6 | through its owner |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.reservation_table` | 4 | tenant root (one tenant per database; no tenant_id by design) |  | 6 | 4 | used by the first release |
| MIG-FNB | `fnb.service_order` | 17 | through its owner |  | 17 | 9 | used by the first release |
| MIG-FNB | `fnb.service_order_line` | 12 | through its owner |  | 12 | 1 | used by the first release |
| MIG-FNB | `fnb.sold_out_item` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 0 | used by the first release |
| MIG-FNB | `fnb.sub_bill` | 11 | through its owner |  | 1 | 1 | used by the first release |
| MIG-FNB | `fnb.substitution_rule` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.table_combination` | 6 | scope_path |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.table_reservation` | 24 | through its owner |  | 6 | 4 | used by the first release |
| MIG-FNB | `fnb.table_session` | 9 | through its owner |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.table_visit` | 16 | through its owner |  | 11 | 8 | used by the first release |
| MIG-FNB | `fnb.temperature_log` | 11 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-FNB | `fnb.waitlist_entry` | 11 | through its owner |  | 3 | 2 | used by the first release |
| MIG-PAYMENTS | `payments.dunning_case` | 14 | scope_path |  | 4 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.dunning_policy` | 8 | scope_path |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment` | 9 | through its owner |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment_plan` | 11 | scope_path |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.instalment_policy` | 10 | scope_path |  | 2 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.method` | 16 | scope_path |  | 0 | 0 | referenced by payments.payment_attempt |
| MIG-PAYMENTS | `payments.payment_attempt` | 19 | scope_path |  | 0 | 2 | used by the first release |
| MIG-PAYMENTS | `payments.provider` | 15 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.provider_connection` | 12 | scope_path |  | 3 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.routing_rule` | 9 | scope_path |  | 0 | 1 | used by the first release |
| MIG-PAYMENTS | `payments.stored_forward` | 9 | scope_path |  | 2 | 0 | used by the first release |
| MIG-PAYMENTS | `payments.token` | 9 | subject |  | 4 | 1 | used by the first release |
| MIG-QUEUE | `queue.entry` | 25 | through its owner |  | 4 | 2 | used by the first release |
| MIG-QUEUE | `queue.queue` | 40 | venue_id |  | 6 | 2 | used by the first release |
| MIG-QUEUE | `queue.queue_operating_window` | 4 | through its owner |  | 3 | 1 | used by the first release |
| MIG-QUEUE | `queue.reading` | 8 | through its owner |  | 5 | 0 | used by the first release |
| MIG-RETAIL | `retail.merchandise` | 16 | through its owner |  | 5 | 2 | used by the first release |
| MIG-RETAIL | `retail.reservation` | 8 | through its owner |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.reservation_line` | 5 | through its owner |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return` | 14 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_line` | 9 | tenant root (one tenant per database; no tenant_id by design) |  | 1 | 1 | used by the first release |
| MIG-RETAIL | `retail.return_policy` | 10 | through its owner |  | 2 | 1 | used by the first release |
| MIG-RETAIL | `retail.sale` | 13 | subject |  | 5 | 2 | used by the first release |
| MIG-RETAIL | `retail.sale_line` | 13 | tenant root (one tenant per database; no tenant_id by design) |  | 4 | 1 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop` | 15 | venue_id |  | 3 | 2 | used by the first release |
| MIG-RETAIL | `retail.shop_and_drop_line` | 7 | through its owner |  | 3 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.import_job` | 14 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.map` | 19 | scope_path |  | 11 | 3 | used by the first release |
| MIG-VENUEMAP | `venuemap.map_version` | 10 | tenant root (one tenant per database; no tenant_id by design) |  | 2 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.path` | 10 | through its owner |  | 6 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.placed_resource` | 11 | through its owner |  | 6 | 1 | used by the first release |
| MIG-VENUEMAP | `venuemap.point` | 21 | through its owner |  | 10 | 2 | used by the first release |
| MIG-VENUEMAP | `venuemap.visit_plan` | 14 | scope_path |  | 6 | 3 | used by the first release |
| MIG-VENUEMAP | `venuemap.visit_plan_item` | 19 | through its owner |  | 6 | 2 | used by the first release |

## Used by the release but not a table

- `identity.guest_session`: Redis. `GuestSession` declares `persistence: none — Redis session registry`. Separate from the staff session by lifetime and auth path, and neither is a row. Ha

## Forward migrations after the first release

**186 forward migrations**, V1000 upwards in build order (the Venue Management waves, then each later app-module). V0100-V0999 are derive-ddl's frozen-mode files in `backend/<db>/`; a number is never reused, and a planned number is kept on the next refresh. The ticket's subject names the same file.

| Number | File | Task | Database | Schema | Tables | Which tables |
|---|---|---|---|---|---|---|
| 1000 | `V1000__identity.sql` | VM-MIG-IDENTITY | tenant | identity | 1 | identity.access_decision |
| 1001 | `V1001__identity.sql` | MIG-IDENTITY-2 | tenant | identity | 2 | identity.sso_group_mapping, identity.sso_provider |
| 1002 | `V1002__platform.sql` | VM-MIG-PLATFORM | tenant | platform | 5 | platform.audit_read, platform.configuration_profile, platform.connectivity_policy, platform.offline_policy, platform.profile_deployment |
| 1003 | `V1003__control.sql` | VM-MIG-CONTROL | control | control | 2 | control.webhook_delivery, control.webhook_subscription |
| 1004 | `V1004__control.sql` | MIG-CONTROL-6 | control | control | 17 | control.cell, control.config_package, control.config_package_application, control.config_package_diff, control.environment, control.migration, control.migration_plan, control.migration_plan_cell, control.migration_run, control.migration_run_cell, control.migration_run_tenant, control.outbox_republish, control.release_component, control.rollout_cell, control.rollout_tenant, control.support_notice, control.upgrade_schedule |
| 1005 | `V1005__approvals.sql` | VM-MIG-APPROVALS | tenant | approvals | 1 | approvals.escalation |
| 1006 | `V1006__ai.sql` | VM-MIG-AI | tenant | ai | 1 | ai.approval_request_score |
| 1007 | `V1007__approvals.sql` | MIG-APPROVALS-2 | tenant | approvals | 2 | approvals.workflow_definition, approvals.workflow_version |
| 1008 | `V1008__approvals.sql` | MIG-APPROVALS-4 | tenant | approvals | 1 | approvals.sla_policy |
| 1009 | `V1009__approvals.sql` | MIG-APPROVALS-5 | tenant | approvals | 3 | approvals.automation_execution, approvals.external_dispatch, approvals.step_up_policy |
| 1010 | `V1010__ai.sql` | MIG-AI-2 | tenant | ai | 1 | ai.action_step |
| 1011 | `V1011__ai.sql` | MIG-AI-3 | tenant | ai | 1 | ai.tool |
| 1012 | `V1012__ai.sql` | MIG-AI-4 | tenant | ai | 3 | ai.risk_assessment, ai.risk_case, ai.risk_strategy |
| 1013 | `V1013__ai.sql` | MIG-AI-5 | tenant | ai | 6 | ai.case_action, ai.case_evidence, ai.entity_risk, ai.layout_draft, ai.risk_alert, ai.risk_edge |
| 1014 | `V1014__rental.sql` | VM-MIG-RENTAL | tenant | rental | 2 | rental.booking, rental.participant |
| 1015 | `V1015__resources.sql` | VM-MIG-RESOURCES | tenant | resources | 3 | resources.performance_participant, resources.qualification, resources.selection_policy |
| 1016 | `V1016__ledger.sql` | VM-MIG-LEDGER | tenant | ledger | 7 | ledger.account_mapping, ledger.deposit, ledger.event_budget, ledger.fiscal_period_event, ledger.recognition_schedule, ledger.settlement, ledger.settlement_exception |
| 1017 | `V1017__promotions.sql` | VM-MIG-PROMOTIONS | tenant | promotions | 2 | promotions.upsell_rule, promotions.voucher |
| 1018 | `V1018__orders.sql` | VM-MIG-ORDERS | tenant | orders | 8 | orders.after_sale_policy, orders.after_sale_request, orders.chargeback, orders.chargeback_evidence, orders.chargeback_investigation_log, orders.deposit, orders.group_quote, orders.refund_batch |
| 1019 | `V1019__access.sql` | VM-MIG-ACCESS | tenant | access | 10 | access.access_change, access.accreditation_credential, access.credential_binding, access.credential_event, access.dynamic_policy, access.dynamic_policy_version, access.media_replacement_policy, access.media_template, access.media_type, access.policy_scope_assignment |
| 1020 | `V1020__payments.sql` | VM-MIG-PAYMENTS | tenant | payments | 1 | payments.provider_cost |
| 1021 | `V1021__rental.sql` | MIG-RENTAL-2 | tenant | rental | 7 | rental.availability_rules, rental.blackout, rental.duration_rules, rental.equipment_assignment, rental.inventory_model, rental.location_rule, rental.product |
| 1022 | `V1022__rental.sql` | MIG-RENTAL-3 | tenant | rental | 6 | rental.deposit_policy, rental.incident, rental.inspection, rental.inspection_item, rental.pricing_profile, rental.quote |
| 1023 | `V1023__orders.sql` | MIG-ORDERS-10 | tenant | orders | 2 | orders.payment_allocation_rule, orders.payment_tip |
| 1024 | `V1024__orders.sql` | MIG-ORDERS-11 | tenant | orders | 3 | orders.order_source_channel, orders.reservation_hold_policy, orders.status_transition_rule |
| 1025 | `V1025__orders.sql` | MIG-ORDERS-2 | tenant | orders | 3 | orders.membership_activation_action, orders.membership_migration, orders.membership_renewal |
| 1026 | `V1026__orders.sql` | MIG-ORDERS-4 | tenant | orders | 1 | orders.member_exception |
| 1027 | `V1027__orders.sql` | MIG-ORDERS-5 | tenant | orders | 1 | orders.order_relationship |
| 1028 | `V1028__orders.sql` | MIG-ORDERS-6 | tenant | orders | 5 | orders.b2b_credit, orders.credit_override, orders.guest_credit_account, orders.invitation_allowance, orders.order_fee |
| 1029 | `V1029__orders.sql` | MIG-ORDERS-8 | tenant | orders | 1 | orders.resale_recommendation |
| 1030 | `V1030__payments.sql` | MIG-PAYMENTS-7 | tenant | payments | 5 | payments.currency_rule, payments.eligibility_rule, payments.failover_policy, payments.fee_rule, payments.provider_event |
| 1031 | `V1031__platform.sql` | MIG-PLATFORM-3 | tenant | platform | 2 | platform.cross_region_entitlement, platform.wallet_authorisation |
| 1032 | `V1032__ledger.sql` | MIG-LEDGER-2 | tenant | ledger | 2 | ledger.inter_entity_obligation, ledger.tax_exemption |
| 1033 | `V1033__fnb.sql` | VM-MIG-FNB | tenant | fnb | 2 | fnb.temperature_checkpoint, fnb.waste_approval_policy |
| 1034 | `V1034__fnb.sql` | MIG-FNB-3 | tenant | fnb | 1 | fnb.reservation_policy |
| 1035 | `V1035__fnb.sql` | MIG-FNB-4 | tenant | fnb | 3 | fnb.ingredient_substitute, fnb.prep_sheet_template, fnb.product_recommendation |
| 1036 | `V1036__workforce.sql` | VM-MIG-WORKFORCE | tenant | workforce | 6 | workforce.announcement, workforce.announcement_receipt, workforce.employee, workforce.job_title, workforce.shift, workforce.work_assignment |
| 1037 | `V1037__maintenance.sql` | VM-MIG-MAINTENANCE | tenant | maintenance | 9 | maintenance.asset_document, maintenance.asset_status_change, maintenance.incident_authority_notification, maintenance.incident_history, maintenance.incident_investigation_note, maintenance.incident_involved_party, maintenance.preventive_plan, maintenance.priority_scoring_model, maintenance.vendor_service_request |
| 1038 | `V1038__maintenance.sql` | MIG-MAINTENANCE-3 | tenant | maintenance | 1 | maintenance.asset_category |
| 1039 | `V1039__games.sql` | VM-MIG-GAMES | tenant | games | 5 | games.game, games.operational_config, games.play, games.pricing, games.reader_profile |
| 1040 | `V1040__games.sql` | MIG-GAMES-2 | tenant | games | 3 | games.authorisation, games.reader, games.reader_sync_status |
| 1041 | `V1041__accreditation.sql` | VM-MIG-ACCREDITATION | tenant | accreditation | 4 | accreditation.application, accreditation.credential, accreditation.holder, accreditation.validity |
| 1042 | `V1042__accreditation.sql` | MIG-ACCREDITATION-2 | tenant | accreditation | 1 | accreditation.audit |
| 1043 | `V1043__accreditation.sql` | MIG-ACCREDITATION-3 | tenant | accreditation | 1 | accreditation.access_profile |
| 1044 | `V1044__accreditation.sql` | MIG-ACCREDITATION-4 | tenant | accreditation | 2 | accreditation.holder_access, accreditation.programme |
| 1045 | `V1045__accreditation.sql` | MIG-ACCREDITATION-5 | tenant | accreditation | 4 | accreditation.document, accreditation.identity_conflict, accreditation.notification_rules, accreditation.requirements |
| 1046 | `V1046__accreditation.sql` | MIG-ACCREDITATION-6 | tenant | accreditation | 3 | accreditation.badge_template, accreditation.mobile_credential_delivery, accreditation.print_job |
| 1047 | `V1047__accreditation.sql` | MIG-ACCREDITATION-7 | tenant | accreditation | 1 | accreditation.data_export |
| 1048 | `V1048__reporting.sql` | VM-MIG-REPORTING | tenant | reporting | 2 | reporting.kpi_target, reporting.schedule_recipient |
| 1049 | `V1049__inventory.sql` | VM-MIG-INVENTORY | tenant | inventory | 9 | inventory.count, inventory.count_line, inventory.purchase_order_line, inventory.quotation, inventory.quotation_line, inventory.requisition_line, inventory.supplier_contract, inventory.transfer, inventory.transfer_line |
| 1050 | `V1050__inventory.sql` | MIG-INVENTORY-2 | tenant | inventory | 1 | inventory.daily_count_list |
| 1051 | `V1051__queue.sql` | VM-MIG-QUEUE | tenant | queue | 1 | queue.feed |
| 1052 | `V1052__marketing.sql` | VM-MIG-MARKETING | tenant | marketing | 1 | marketing.journey_step |
| 1053 | `V1053__marketing.sql` | MIG-MARKETING-5 | tenant | marketing | 1 | marketing.kiosk_assist_session |
| 1054 | `V1054__marketing.sql` | MIG-MARKETING-6 | tenant | marketing | 29 | marketing.agent_service_profile, marketing.business_event, marketing.case_internal_request, marketing.case_linked_record, marketing.case_resolution, marketing.case_routing_rule, marketing.communication_routing_rule, marketing.consent_record_channel, marketing.contact_automation, marketing.guest_extra_field, marketing.guest_extra_option, marketing.guest_extra_value, marketing.guest_match_policy, marketing.guest_relationship, marketing.message_trigger, marketing.message_trigger_condition, marketing.privacy_request_deadline, marketing.privacy_request_type, marketing.quality_evaluation, marketing.reward_assignment, marketing.sla_policy, marketing.suppression, marketing.tracking_technology_catalogue, marketing.waiver_association, marketing.waiver_exception, marketing.waiver_form_layout, marketing.waiver_master, marketing.waiver_trigger_rule, marketing.waiver_version_control |
| 1055 | `V1055__marketing.sql` | MIG-MARKETING-7 | tenant | marketing | 5 | marketing.duplicate_candidate, marketing.guest_attribute_model, marketing.identity_rules, marketing.privacy_exception, marketing.privacy_request |
| 1056 | `V1056__marketing.sql` | MIG-MARKETING-9 | tenant | marketing | 5 | marketing.case_category, marketing.case_service_action, marketing.communication_provider, marketing.message_dispatch_attempt, marketing.service_queue |
| 1057 | `V1057__subscription.sql` | MIG-SUBSCRIPTION-2 | tenant | subscription | 1 | subscription.go_live_readiness |
| 1058 | `V1058__identity.sql` | MIG-IDENTITY-3 | tenant | identity | 12 | identity.access_override, identity.access_review_campaign, identity.access_review_item, identity.authorisation_policy, identity.authorisation_policy_version, identity.authz_audit, identity.benefit_usage, identity.customer_membership, identity.membership_history, identity.module, identity.module_access, identity.permission |
| 1059 | `V1059__workforce.sql` | MIG-WORKFORCE-2 | tenant | workforce | 1 | workforce.shift_swap |
| 1060 | `V1060__marketing.sql` | MIG-MARKETING-10 | tenant | marketing | 3 | marketing.case_escalation, marketing.feedback_classification, marketing.review_response |
| 1061 | `V1061__marketing.sql` | MIG-MARKETING-12 | tenant | marketing | 4 | marketing.consent_capture_point, marketing.minor_privacy_rule, marketing.privacy_change_set, marketing.processing_purpose |
| 1062 | `V1062__marketing.sql` | MIG-MARKETING-2 | tenant | marketing | 4 | marketing.guest_note, marketing.loyalty_points, marketing.touch_point, marketing.waiver_signature |
| 1063 | `V1063__reporting.sql` | MIG-REPORTING-2 | tenant | reporting | 1 | reporting.analytics_governance_policy |
| 1064 | `V1064__reporting.sql` | MIG-REPORTING-3 | tenant | reporting | 1 | reporting.anomaly |
| 1065 | `V1065__control.sql` | MIG-CONTROL-2 | control | control | 3 | control.billing_entity, control.onboarding_application, control.venue_type_template |
| 1066 | `V1066__ai.sql` | MIG-AI-8 | tenant | ai | 4 | ai.blueprint, ai.blueprint_decision, ai.config_session, ai.config_source |
| 1067 | `V1067__ai.sql` | MIG-AI-9 | tenant | ai | 4 | ai.control, ai.control_test, ai.evidence_package, ai.risk_register |
| 1068 | `V1068__seating.sql` | MIG-SEATING-6 | tenant | seating | 3 | seating.import_job, seating.seat_map_template, seating.zone |
| 1069 | `V1069__marketing.sql` | MIG-MARKETING-4 | tenant | marketing | 1 | marketing.audience_list |
| 1070 | `V1070__payments.sql` | MIG-PAYMENTS-2 | tenant | payments | 1 | payments.reconciliation_source |
| 1071 | `V1071__payments.sql` | MIG-PAYMENTS-9 | tenant | payments | 4 | payments.chargeback_evidence, payments.credit_account, payments.matching_rules, payments.merchant_account |
| 1072 | `V1072__control.sql` | MIG-CONTROL-3 | control | control | 6 | control.channel_listing, control.partner_allocation, control.partner_booking_limit, control.partner_commercial_exception, control.partner_status_history, control.partner_user |
| 1073 | `V1073__tenancy.sql` | VM-MIG-TENANCY | tenant | tenancy | 4 | tenancy.device_audit, tenancy.device_credential, tenancy.device_firmware, tenancy.device_rollout |
| 1074 | `V1074__control.sql` | MIG-CONTROL-4 | control | control | 1 | control.tenant_domain |
| 1075 | `V1075__tenancy.sql` | MIG-TENANCY-2 | tenant | tenancy | 1 | tenancy.device_tamper_event |
| 1076 | `V1076__platform.sql` | MIG-PLATFORM-2 | tenant | platform | 1 | platform.cell_endpoint |
| 1077 | `V1077__tenancy.sql` | MIG-TENANCY-3 | tenant | tenancy | 2 | tenancy.data_retention_setting, tenancy.device_telemetry |
| 1078 | `V1078__access.sql` | MIG-ACCESS-2 | tenant | access | 1 | access.access_area |
| 1079 | `V1079__access.sql` | MIG-ACCESS-6 | tenant | access | 10 | access.access_map, access.attraction_access, access.configuration_version, access.consumption_rule, access.gate_lane, access.group_admission_rule, access.hardware_deployment, access.journey_sequence_rule, access.offline_policy, access.operating_calendar_entry |
| 1080 | `V1080__payments.sql` | MIG-PAYMENTS-3 | tenant | payments | 3 | payments.terminal, payments.terminal_certification, payments.terminal_certification_level3 |
| 1081 | `V1081__wallet.sql` | VM-MIG-WALLET | tenant | wallet | 1 | wallet.adjustment |
| 1082 | `V1082__marketing.sql` | MIG-MARKETING-3 | tenant | marketing | 5 | marketing.legal_hold, marketing.privacy_action, marketing.privacy_audit_event, marketing.retention_policy, marketing.retention_run |
| 1083 | `V1083__approvals.sql` | MIG-APPROVALS-3 | tenant | approvals | 1 | approvals.retention_policy |
| 1084 | `V1084__subscription.sql` | MIG-SUBSCRIPTION-3 | tenant | subscription | 10 | subscription.membership_eligibility_rule, subscription.membership_entitlement, subscription.membership_household_policy, subscription.membership_household_policy_role_limit, subscription.membership_product, subscription.membership_product_history, subscription.membership_renewal_policy, subscription.membership_usage_policy, subscription.tier_allowance, subscription.tier_module |
| 1085 | `V1085__control.sql` | MIG-CONTROL-5 | control | control | 2 | control.release, control.rollout |
| 1086 | `V1086__sync.sql` | MIG-SYNC-2 | tenant | sync | 2 | sync.cell_connection, sync.cross_cell_request |
| 1087 | `V1087__platform.sql` | MIG-PLATFORM-4 | tenant | platform | 1 | platform.dead_letter |
| 1088 | `V1088__catalogue.sql` | VM-MIG-CATALOGUE | tenant | catalogue | 3 | catalogue.donation_campaign, catalogue.performance_template, catalogue.waitlist_entry |
| 1089 | `V1089__subscription.sql` | MIG-SUBSCRIPTION-4 | tenant | subscription | 2 | subscription.licensing_model, subscription.vsi_assessment |
| 1090 | `V1090__control.sql` | MIG-CONTROL-7 | control | control | 20 | control.burst_environment, control.cell_cluster, control.partner_application_review_task, control.partner_capability_grant, control.partner_case, control.partner_commission_line, control.partner_commission_rule, control.partner_commission_rule_tier, control.partner_contact, control.partner_credit_profile, control.partner_distribution_right, control.partner_document, control.partner_rate, control.partner_reconciliation_exception, control.partner_scope_assignment, control.partner_security, control.partner_settlement_batch, control.tenant_migration, control.tenant_migration_plan, control.usage_record |
| 1091 | `V1091__catalogue.sql` | MIG-CATALOGUE-2 | tenant | catalogue | 2 | catalogue.membership_programme, catalogue.plan_benefit |
| 1092 | `V1092__control.sql` | MIG-CONTROL-8 | control | control | 2 | control.cell_instance, control.cell_job |
| 1094 | `V1094__subscription.sql` | MIG-SUBSCRIPTION-5 | tenant | subscription | 3 | subscription.capacity_pack, subscription.enforcement_policy, subscription.vsi_model |
| 1095 | `V1095__subscription.sql` | MIG-SUBSCRIPTION-6 | tenant | subscription | 1 | subscription.trial_config |
| 1098 | `V1098__control.sql` | MIG-CONTROL-9 | control | control | 2 | control.credit_note, control.credit_note_line |
| 1099 | `V1099__approvals.sql` | MIG-APPROVALS-6 | tenant | approvals | 12 | approvals.approved_action_execution, approvals.automation, approvals.business_rule, approvals.control_policy, approvals.decision_record, approvals.decision_table, approvals.decision_table_row, approvals.workflow_exception, approvals.workflow_instance, approvals.workflow_intervention, approvals.workflow_step_execution, approvals.workflow_trigger |
| 1100 | `V1100__seating.sql` | MIG-SEATING-2 | tenant | seating | 1 | seating.hold_pool |
| 1101 | `V1101__seating.sql` | MIG-SEATING-4 | tenant | seating | 2 | seating.hold_type, seating.seat_rules |
| 1102 | `V1102__workforce.sql` | MIG-WORKFORCE-4 | tenant | workforce | 4 | workforce.employment, workforce.staff_conversation, workforce.staff_conversation_participant, workforce.staff_message |
| 1103 | `V1103__approvals.sql` | MIG-APPROVALS-7 | tenant | approvals | 2 | approvals.evidence_package, approvals.signature |
| 1104 | `V1104__catalogue.sql` | MIG-CATALOGUE-3 | tenant | catalogue | 2 | catalogue.approval_policy, catalogue.audit_entry |
| 1105 | `V1105__approvals.sql` | MIG-APPROVALS-8 | tenant | approvals | 1 | approvals.approver_availability |
| 1107 | `V1107__control.sql` | MIG-CONTROL-10 | control | control | 2 | control.partner_billing_profile, control.partner_rate_volume_band |
| 1108 | `V1108__control.sql` | MIG-CONTROL-11 | control | control | 1 | control.api_anomaly |
| 1109 | `V1109__assets.sql` | MIG-ASSETS-2 | tenant | assets | 6 | assets.audit, assets.distribution_channel, assets.rendition, assets.share, assets.tag, assets.taxonomy |
| 1110 | `V1110__assets.sql` | MIG-ASSETS-3 | tenant | assets | 1 | assets.approval |
| 1111 | `V1111__seating.sql` | MIG-SEATING-3 | tenant | seating | 2 | seating.seating_rules, seating.section |
| 1112 | `V1112__pricing.sql` | MIG-PRICING-2 | tenant | pricing | 3 | pricing.dynamic_price_action, pricing.dynamic_price_condition, pricing.dynamic_price_rule |
| 1113 | `V1113__catalogue.sql` | MIG-CATALOGUE-4 | tenant | catalogue | 5 | catalogue.package_pricing, catalogue.price_assignment, catalogue.rate, catalogue.rollback_action, catalogue.variant_dimension |
| 1114 | `V1114__promotions.sql` | MIG-PROMOTIONS-2 | tenant | promotions | 4 | promotions.campaign, promotions.campaign_budget, promotions.stacking_rule, promotions.voucher_batch |
| 1115 | `V1115__access.sql` | MIG-ACCESS-3 | tenant | access | 1 | access.companion_rule |
| 1116 | `V1116__access.sql` | MIG-ACCESS-9 | tenant | access | 5 | access.fast_pass_profile, access.identity_lock, access.journey_profile, access.reason_code, access.security_investigation |
| 1117 | `V1117__fnb.sql` | MIG-FNB-2 | tenant | fnb | 3 | fnb.combo, fnb.combo_slot, fnb.combo_slot_option |
| 1118 | `V1118__catalogue.sql` | MIG-CATALOGUE-5 | tenant | catalogue | 5 | catalogue.event_change_treatment_policy, catalogue.membership_benefit, catalogue.seat_pricing_rule, catalogue.tax_profile, catalogue.waiting_room_setting |
| 1119 | `V1119__catalogue.sql` | MIG-CATALOGUE-6 | tenant | catalogue | 15 | catalogue.calculation_profile, catalogue.calculation_step, catalogue.demand_forecast, catalogue.dynamic_pricing_control, catalogue.dynamic_pricing_strategy, catalogue.fee, catalogue.fee_rule, catalogue.price_execution, catalogue.price_resolution_policy, catalogue.pricing_experiment, catalogue.pricing_recommendation, catalogue.pricing_recommendation_decision, catalogue.pricing_simulation, catalogue.rounding_profile, catalogue.tax_rule |
| 1120 | `V1120__catalogue.sql` | MIG-CATALOGUE-7 | tenant | catalogue | 12 | catalogue.ai_catalogue_session, catalogue.ai_finding, catalogue.change_request, catalogue.change_request_line, catalogue.configuration_template, catalogue.lifecycle_action, catalogue.lifecycle_workflow, catalogue.price_list_version, catalogue.pricing_publication, catalogue.product_channel_assignment, catalogue.product_link, catalogue.sales_channel |
| 1121 | `V1121__catalogue.sql` | MIG-CATALOGUE-8 | tenant | catalogue | 2 | catalogue.price_category, catalogue.pricing_market |
| 1122 | `V1122__catalogue.sql` | MIG-CATALOGUE-9 | tenant | catalogue | 1 | catalogue.pricing_publication_target |
| 1123 | `V1123__catalogue.sql` | MIG-CATALOGUE-10 | tenant | catalogue | 3 | catalogue.demand_signal, catalogue.price_ladder, catalogue.signal_registry |
| 1124 | `V1124__promotions.sql` | MIG-PROMOTIONS-3 | tenant | promotions | 2 | promotions.promotion_alert, promotions.recommendation_outcome |
| 1125 | `V1125__promotions.sql` | MIG-PROMOTIONS-5 | tenant | promotions | 2 | promotions.bundle_capacity_policy, promotions.promotion_conflict |
| 1126 | `V1126__catalogue.sql` | MIG-CATALOGUE-11 | tenant | catalogue | 2 | catalogue.channel_connection, catalogue.channel_sales_rule |
| 1127 | `V1127__orders.sql` | MIG-ORDERS-3 | tenant | orders | 1 | orders.discount |
| 1128 | `V1128__wallet.sql` | MIG-WALLET-2 | tenant | wallet | 1 | wallet.risk_rule |
| 1129 | `V1129__catalogue.sql` | MIG-CATALOGUE-12 | tenant | catalogue | 2 | catalogue.channel_incident, catalogue.channel_sync |
| 1130 | `V1130__catalogue.sql` | MIG-CATALOGUE-13 | tenant | catalogue | 3 | catalogue.event_type, catalogue.pricing_test_case, catalogue.space |
| 1131 | `V1131__promotions.sql` | MIG-PROMOTIONS-4 | tenant | promotions | 1 | promotions.partner_bundle_product |
| 1132 | `V1132__promotions.sql` | MIG-PROMOTIONS-6 | tenant | promotions | 4 | promotions.product_relationship, promotions.recommendation_experiment, promotions.recommendation_strategy, promotions.recommendation_suppression |
| 1134 | `V1134__maintenance.sql` | MIG-MAINTENANCE-2 | tenant | maintenance | 1 | maintenance.inspection_item |
| 1135 | `V1135__rental.sql` | MIG-RENTAL-5 | tenant | rental | 5 | rental.agreement, rental.agreement_item, rental.agreement_rules, rental.fee_policy, rental.operational_rules |
| 1136 | `V1136__seating.sql` | MIG-SEATING-5 | tenant | seating | 4 | seating.group_request, seating.group_request_participant, seating.reassignment, seating.section_row |
| 1137 | `V1137__access.sql` | MIG-ACCESS-4 | tenant | access | 2 | access.podium, access.podium_shift |
| 1138 | `V1138__orders.sql` | MIG-ORDERS-7 | tenant | orders | 4 | orders.resale_eligibility_rule, orders.resale_fee_policy, orders.resale_marketplace_config, orders.resale_settlement |
| 1139 | `V1139__payments.sql` | MIG-PAYMENTS-4 | tenant | payments | 2 | payments.mixed_tender_rules, payments.payment_terms |
| 1140 | `V1140__orders.sql` | MIG-ORDERS-9 | tenant | orders | 2 | orders.upgrade, orders.upgrade_rule |
| 1141 | `V1141__payments.sql` | MIG-PAYMENTS-5 | tenant | payments | 1 | payments.risk_rules |
| 1142 | `V1142__payments.sql` | MIG-PAYMENTS-6 | tenant | payments | 1 | payments.deposit_activity |
| 1143 | `V1143__orders.sql` | MIG-ORDERS-12 | tenant | orders | 6 | orders.after_sale_policy_window, orders.deposit_policy, orders.external_reference_mapping, orders.group_payment_milestone, orders.group_payment_schedule, orders.refund_calculation_policy |
| 1144 | `V1144__payments.sql` | MIG-PAYMENTS-8 | tenant | payments | 2 | payments.authentication_policy, payments.hosted_checkout |
| 1145 | `V1145__wallet.sql` | MIG-WALLET-3 | tenant | wallet | 1 | wallet.dispute |
| 1146 | `V1146__wallet.sql` | MIG-WALLET-4 | tenant | wallet | 1 | wallet.credit_eligibility |
| 1147 | `V1147__wallet.sql` | MIG-WALLET-5 | tenant | wallet | 3 | wallet.credential, wallet.shared_wallet, wallet.shared_wallet_member |
| 1148 | `V1148__access.sql` | MIG-ACCESS-5 | tenant | access | 1 | access.hardware_certification |
| 1149 | `V1149__access.sql` | MIG-ACCESS-7 | tenant | access | 7 | access.credential_event_propagation_rule, access.credential_security_profile, access.external_credential_integration, access.media_compatibility_test, access.media_encoding_profile, access.security_alert, access.verification_method_policy |
| 1150 | `V1150__access.sql` | MIG-ACCESS-8 | tenant | access | 6 | access.access_point_configuration, access.device_configuration, access.edge_node, access.edge_package, access.gate_outcome_profile, access.hardware_model |
| 1151 | `V1151__access.sql` | MIG-ACCESS-10 | tenant | access | 5 | access.access_attribute, access.credential_sharing_case, access.fraud_rule, access.policy_evaluation_setting, access.risk_scoring_config |
| 1152 | `V1152__access.sql` | MIG-ACCESS-11 | tenant | access | 5 | access.credential_exception, access.credential_issuance, access.media_binding_rule, access.security_playbook, access.ticket_status_transition |
| 1153 | `V1153__access.sql` | MIG-ACCESS-12 | tenant | access | 5 | access.branding_profile, access.credential_delivery, access.credential_issuance_retry_policy, access.dynamic_field, access.media_template_version |
| 1156 | `V1156__fnb.sql` | MIG-FNB-5 | tenant | fnb | 3 | fnb.kitchen_routing_rule, fnb.outlet_template, fnb.service_charge_policy |
| 1158 | `V1158__retail.sql` | MIG-RETAIL-2 | tenant | retail | 2 | retail.exchange, retail.product_recommendation |
| 1159 | `V1159__rental.sql` | MIG-RENTAL-4 | tenant | rental | 2 | rental.damage_assessment, rental.settlement |
| 1160 | `V1160__rental.sql` | MIG-RENTAL-6 | tenant | rental | 2 | rental.agreement_signature, rental.override |
| 1161 | `V1161__resources.sql` | MIG-RESOURCES-2 | tenant | resources | 1 | resources.resource_type |
| 1162 | `V1162__workforce.sql` | MIG-WORKFORCE-3 | tenant | workforce | 4 | workforce.field_ownership, workforce.integration_source, workforce.staffing_rules, workforce.training_record |
| 1163 | `V1163__resources.sql` | MIG-RESOURCES-3 | tenant | resources | 6 | resources.attribute_definition, resources.resource_audit, resources.resource_category, resources.resource_dependency, resources.resource_relation, resources.venue_assignment |
| 1164 | `V1164__workforce.sql` | MIG-WORKFORCE-5 | tenant | workforce | 9 | workforce.labour_budget, workforce.leave_balance, workforce.leave_request, workforce.leave_type, workforce.open_shift, workforce.position_requirement, workforce.shift_template, workforce.sync_conflict, workforce.sync_run |
| 1165 | `V1165__maintenance.sql` | MIG-MAINTENANCE-4 | tenant | maintenance | 2 | maintenance.incident_media, maintenance.work_order_attachment |
| 1166 | `V1166__games.sql` | MIG-GAMES-3 | tenant | games | 7 | games.attraction_type, games.entitlement, games.gameplay_transaction, games.pricing_exception, games.reader_deployment, games.redemption_rules, games.validation_rules |
| 1167 | `V1167__games.sql` | MIG-GAMES-4 | tenant | games | 5 | games.card_expiry_rules, games.prize, games.prize_cost, games.redemption, games.redemption_line |
| 1168 | `V1168__games.sql` | MIG-GAMES-5 | tenant | games | 1 | games.kiosk_config |
| 1169 | `V1169__marketing.sql` | MIG-MARKETING-8 | tenant | marketing | 5 | marketing.audience_activation, marketing.communication_preference_type, marketing.journey_enrollment, marketing.privacy_export_package, marketing.privacy_incident |
| 1170 | `V1170__marketing.sql` | MIG-MARKETING-11 | tenant | marketing | 4 | marketing.communication_policy_decision, marketing.sender_identity, marketing.waiver_signatory_rule, marketing.waiver_verification |
| 1171 | `V1171__marketing.sql` | MIG-MARKETING-13 | tenant | marketing | 1 | marketing.waiver_localisation |
| 1172 | `V1172__marketing.sql` | MIG-MARKETING-14 | tenant | marketing | 1 | marketing.case_compensation_request |
| 1173 | `V1173__marketing.sql` | MIG-MARKETING-15 | tenant | marketing | 3 | marketing.badge, marketing.loyalty_campaign, marketing.message_delivery |
| 1174 | `V1174__marketing.sql` | MIG-MARKETING-16 | tenant | marketing | 3 | marketing.cookie_scan_finding, marketing.cookie_scan_policy, marketing.cookie_scan_run |
| 1175 | `V1175__ai.sql` | MIG-AI-6 | tenant | ai | 1 | ai.suggestion_outcome |
| 1176 | `V1176__ai.sql` | MIG-AI-7 | tenant | ai | 1 | ai.signal_source |
| 1177 | `V1177__reporting.sql` | MIG-REPORTING-4 | tenant | reporting | 1 | reporting.export |
| 1178 | `V1178__reporting.sql` | MIG-REPORTING-5 | tenant | reporting | 2 | reporting.pipeline, reporting.site_normalisation_basis |
| 1179 | `V1179__reporting.sql` | MIG-REPORTING-6 | tenant | reporting | 2 | reporting.delivery, reporting.subscription |
| 1181 | `V1181__control.sql` | MIG-CONTROL-13 | control | control | 2 | control.api_anomaly_rule, control.api_limit |
| 1182 | `V1182__payments.sql` | MIG-PAYMENTS-10 | tenant | payments | 1 | payments.method_config |
| 1184 | `V1184__ai.sql` | MIG-AI-10 | tenant | ai | 2 | ai.index_failure, ai.spend_ceiling |
| 1185 | `V1185__workforce.sql` | MIG-WORKFORCE-6 | tenant | workforce | 1 | workforce.forecast_requirement |
| 1187 | `V1187__marketing.sql` | MIG-MARKETING-17 | tenant | marketing | 1 | marketing.service_copilot_config |
| 1188 | `V1188__ai.sql` | MIG-AI-11 | tenant | ai | 1 | ai.forecast_export |
| 1189 | `V1189__control.sql` | MIG-CONTROL-12 | control | control | 1 | control.sandbox |
| 1190 | `V1190__catalogue.sql` | MIG-CATALOGUE-14 | tenant | catalogue | 2 | catalogue.event_reschedule, catalogue.prepaid_minutes |
| 1192 | `V1192__orders.sql` | MIG-ORDERS-13 | tenant | orders | 6 | orders.group_enquiry, orders.group_quote_line, orders.group_task, orders.group_ticket_allocation, orders.group_ticket_allocation_line, orders.group_ticket_fulfillment |
| 1194 | `V1194__wallet.sql` | MIG-WALLET-6 | tenant | wallet | 2 | wallet.gift_card_product, wallet.voucher_type |
| 1195 | `V1195__resources.sql` | MIG-RESOURCES-4 | tenant | resources | 1 | resources.allocation_policy |
| 1196 | `V1196__catalogue.sql` | MIG-CATALOGUE-15 | tenant | catalogue | 1 | catalogue.performance_media |
| 1197 | `V1197__wallet.sql` | MIG-WALLET-7 | tenant | wallet | 1 | wallet.restriction |
| 1198 | `V1198__resources.sql` | MIG-RESOURCES-5 | tenant | resources | 2 | resources.resource_cost, resources.resource_request |

## Tables no migration creates

**9 tables** in `backend/` that no migration above creates, each with the reason. Row-level security on a table with no `tenant_id` is the tenant-root policy, by design: one tenant per database (ADR-0038), `platform.tenant_root_in_scope()`.

| Table | Database | Source DDL | Why |
|---|---|---|---|
| `ai.signal_observation` | tenant | backend/tenant/010-ai.sql | storage only: no operation reads or writes it and no task names it; its forward migration is planned when an operation first reaches it |
| `approvals.accreditation_badge` | tenant | backend/tenant/010-approvals.sql | held: only operations not built until their contract is agreed reach it (issueAccreditationBadge: stub, listAccreditationBadges: stub); its forward migration is planned with them |
| `control.archival_job` | control | backend/control/010-control.sql | held: only operations not built until their contract is agreed reach it (listArchivalJobs: stub); its forward migration is planned with them |
| `control.backup_run` | control | backend/control/010-control.sql | held: only operations not built until their contract is agreed reach it (listBackupRuns: stub); its forward migration is planned with them |
| `control.scaling_policy` | control | backend/control/010-control.sql | held: only operations not built until their contract is agreed reach it (getScalingPolicy: stub, setScalingPolicy: stub); its forward migration is planned with them |
| `control.waf_rule` | control | backend/control/010-control.sql | held: only operations not built until their contract is agreed reach it (listWafRules: stub, setWafPolicy: stub); its forward migration is planned with them |
| `marketing.guest_match_decision` | tenant | backend/tenant/010-marketing.sql | held: only operations not built until their contract is agreed reach it (decideGuestCheckoutMatch: deprecated); its forward migration is planned with them |
| `retail.store_rule` | tenant | backend/tenant/010-retail.sql | held: only operations not built until their contract is agreed reach it (listStoreRules: stub, setStoreRules: stub); its forward migration is planned with them |
| `subscription.partner_quote` | tenant | backend/tenant/010-subscription.sql | held: only operations not built until their contract is agreed reach it (createPartnerQuote: stub, listPartnerQuotes: stub); its forward migration is planned with them |
