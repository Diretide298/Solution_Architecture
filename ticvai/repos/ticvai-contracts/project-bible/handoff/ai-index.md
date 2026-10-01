# AI — the whole set

**Derived, not written.** Regenerate with `python3 tools/derive-domain.py ai && python3 tools/render-domain.py ai`. Nothing below is hand-typed, so nothing here goes stale — which the hand-maintained version did four times on 17 August alone.

**ai has no folder and should not.** The package is organised by artefact kind, and a single domain folder would raise the question of why there is no `finance/`. This page gathers what is spread across layers; each artefact stays where it belongs.

| | |
|---|---|
| **Operations** | 143 |
| **Schemas** | 122 |
| **States** | 42 |
| **Events** | 47 |
| **Tables** | 137 |
| **Screens** | 195 |
| **Flows** | 11 |
| **Documents** | 64 |
| **Open conflicts** | 1 |

## Reached outside the contract

**The closure follows behaviour, not folders.** These state models live under other contracts and specify things this domain depends on — the hand-written index named none of them.

| Model | Lives under | Reached via |
|---|---|---|
| `approval-request.yaml` | `approvals` | `approval.expired`, `approval.granted`, `approval.rejected` |
| `cart.yaml` | `orders` | `cart.abandoned` |
| `case.yaml` | `marketing-crm` | `marketing.caseClosed` |
| `chargeback.yaml` | `orders` | `order.chargebackRecorded` |
| `content.yaml` | `white-label` | `whitelabel.contentPublished` |
| `conversation.yaml` | `marketing-crm` | `conversation.handedOver` |
| `entitlement-status.yaml` | `orders` | `access.validated` |
| `media.yaml` | `assets` | `assets.documentIndexed` |
| `order.yaml` | `orders` | `order.cancelled`, `order.completed`, `order.paid`, `order.refunded` |
| `payment.yaml` | `orders` | `order.paid` |
| `performance.yaml` | `catalogue` | `performance.cancelled` |
| `period.yaml` | `finance` | `ledger.periodClosed` |
| `product.yaml` | `catalogue` | `catalogue.productPublished` |
| `promotion.yaml` | `promotions` | `promotions.recommendationStrategyPublished` |
| `refund.yaml` | `orders` | `order.refunded` |
| `registered-device.yaml` | `tenancy` | `device.statusChanged` |
| `resale-listing.yaml` | `orders` | `entitlement.transferred` |
| `schedule.yaml` | `white-label` | `whitelabel.contentPublished` |
| `seat.yaml` | `seating` | `seat.sold` |
| `shift.yaml` | `shift` | `shift.closed` |
| `stock-count.yaml` | `inventory` | `stock.depleted` |
| `tenant.yaml` | `subscription` | `tenant.suspended` |
| `ticket-transfer.yaml` | `orders` | `entitlement.transferred` |

## What it is walled off from

**A page showing only what a domain *is* answers half the question.** The other half is what it cannot reach, and what keeps that true rather than merely true today.

| | Holds | Enforced by |
|---|---|---|
| **The vector store is reached by one contract** — 1 collection, 9 operations, all in `ai`. No screen, service or other contract reaches it directly. | yes | tools/check-package.py — no non-AI contract writes an AI table |
| **Writes stay inside the domain** — AI reads the transactional core and writes only its own stores and caches. `generateVenueLayout` wrote into `seating.import_job` on 17 August and now stops at a draft. | yes | tools/check-package.py, with two stated exceptions (ADR-0020) |
| **Conversation logs sit off the transactional primary** — Prompt and response volume does not compete with a sale. 5 tables on the analytical store. | yes | ADR-0020, checked against the store map |
| **Every model call leaves an audit record** — 17 operations write an `ai.interaction` (8.3.55). | yes | tools/check-package.py — a model-calling operation with no interaction fails |
| **Only governed operations outside the domain may write to it** — 2 operations in other contracts write an `ai.*` table: ['askReportingQuestion', 'saveNaturalLanguageQuery']. Each is a governance record, not a bypass. | yes | tools/check-package.py allowlist, stated in ADR-0020 |

**Storage tiers** — `postgres` 122 · `postgres-analytical` 5 · `qdrant` 1 · `redis` 9

## Operations

**141 in the contract.**

| Operation | Verb | Guest | Scope |
|---|---|---|---|
| `addRiskCaseEvidence` | POST |  | venue |
| `answerConfigurationQuestion` | POST |  | venue |
| `attachConfigurationSource` | POST |  | venue |
| `backtestRiskStrategy` | POST |  | tenant |
| `buildConfigurationPlan` | POST |  | venue |
| `cancelActionPlan` | POST |  | venue |
| `closeAiIncident` | POST |  | tenant |
| `closeRiskCase` | POST |  | venue |
| `compareForecastScenarios` | POST |  | venue |
| `configureAiCapability` | PUT |  | tenant |
| `configureAnomalyDetector` | PUT |  | venue |
| `configureAssistantProfile` | PUT |  | tenant |
| `configureForecastSignalSource` | PUT |  | tenant |
| `configureRiskStrategy` | PUT |  | tenant |
| `containAiIncident` | POST |  | tenant |
| `createAiConversation` | POST |  | venue |
| `createAiGovernancePolicyDraft` | POST |  | tenant |
| `createAiPolicyException` | POST |  | tenant |
| `createForecastScenario` | POST |  | venue |
| `createKnowledgeCollection` | POST |  | tenant |
| `createRiskCase` | POST |  | venue |
| `decideAiGovernanceAlert` | POST |  | venue |
| `decideAiInsight` | POST |  | venue |
| `decideBlueprintRecommendation` | POST |  | venue |
| `decideOperationalRequirement` | POST |  | venue |
| `decideProposedAction` | POST |  | venue |
| `decideRecommendations` | POST |  | venue |
| `decideRiskAlert` | POST |  | venue |
| `evaluateAiGovernance` | POST |  | venue |
| `expandRiskNetwork` | GET |  | venue |
| `explainMetricChange` | POST |  | venue |
| `explainRecommendationDecision` | GET |  | venue |
| `exportAiEvidencePackage` | POST |  | venue |
| `exportForecastVersion` | POST |  | venue |
| `generateConfiguration` | POST |  | venue |
| `generateVenueLayout` | POST |  | venue |
| `getActionPlan` | GET |  | venue |
| `getAiByokEnablement` | GET |  | tenant |
| `getAiDecisionTrace` | GET |  | venue |
| `getAiPolicy` | GET |  | venue |
| `getAiUsage` | GET |  | tenant |
| `getAiVenueSettings` | GET |  | venue |
| `getApprovalRequestScore` | GET |  | venue |
| `getConfigurationBlueprint` | GET |  | venue |
| `getCustomerRecommendationProfile` | GET |  | venue |
| `getEffectiveAiPolicy` | GET |  | venue |
| `getEntityRisk` | GET |  | tenant |
| `getForecast` | GET |  | venue |
| `getForecastAccuracy` | GET |  | venue |
| `getGuidedChoiceSuggestion` | GET |  | venue |
| `getRiskCase` | GET |  | venue |
| `getVenueHistoryImport` | GET |  | venue |
| `importVenueHistory` | POST |  | venue |
| `ingestKnowledgeDocument` | POST |  | tenant |
| `listAiCapabilities` | GET |  | venue |
| `listAiCapabilityHealth` | GET |  | tenant |
| `listAiCapabilityMaturity` | GET |  | venue |
| `listAiControls` | GET |  | tenant |
| `listAiConversations` | GET |  | venue |
| `listAiEvaluations` | GET |  | tenant |
| `listAiGovernanceAlerts` | GET |  | venue |
| `listAiGovernancePolicyVersions` | GET |  | tenant |
| `listAiIncidents` | GET |  | tenant |
| `listAiInsights` | GET |  | venue |
| `listAiInteractions` | GET |  | tenant |
| `listAiModels` | GET |  | tenant |
| `listAiProviders` | GET |  | tenant |
| `listAiRiskRegister` | GET |  | tenant |
| `listAiTools` | GET |  | tenant |
| `listAiTrainingRuns` | GET |  | tenant |
| `listAnomalyDetectors` | GET |  | venue |
| `listAssistantProfiles` | GET |  | tenant |
| `listConfigurationSessions` | GET |  | venue |
| `listConfigurationSources` | GET |  | venue |
| `listForecastDefinitions` | GET |  | venue |
| `listForecastSignals` | GET |  | tenant |
| `listForecastVersions` | GET |  | venue |
| `listIndexFailures` | GET |  | tenant |
| `listIndexJobs` | GET |  | tenant |
| `listIndexSources` | GET |  | tenant |
| `listKnowledgeCollections` | GET |  | tenant |
| `listKnowledgeGaps` | GET |  | tenant |
| `listMarketingRecommendations` | GET |  | venue |
| `listOperationalRequirements` | GET |  | venue |
| `listPromptTemplates` | GET |  | tenant |
| `listProposedActions` | GET |  | venue |
| `listRiskAlerts` | GET |  | venue |
| `listVenueHistoryImports` | GET |  | venue |
| `openAiIncident` | POST |  | tenant |
| `overrideAiDecision` | POST |  | venue |
| `pauseActionPlan` | POST |  | venue |
| `pauseAiCapability` | POST |  | tenant |
| `promoteAiRelease` | POST |  | tenant |
| `proposeLookalikeSegment` | POST |  | venue |
| `proposeMarketingContent` | POST |  | venue |
| `proposeRiskAction` | POST |  | venue |
| `proposeSeatMapChanges` | POST |  | venue |
| `proposeTranslations` | POST |  | tenant |
| `proposeVenueLabels` | POST |  | venue |
| `proposeWalkways` | POST |  | venue |
| `publishAiGovernancePolicy` | POST |  | tenant |
| `publishForecastVersion` | POST |  | venue |
| `publishPromptTemplate` | POST |  | tenant |
| `recordAnswerFeedback` | POST |  | venue |
| `recordRecommendationEvents` | POST |  | venue |
| `recordSuggestionOutcome` | POST |  | venue |
| `reindexSource` | POST |  | tenant |
| `removeIndexEntry` | DELETE |  | tenant |
| `replayAiDecision` | POST |  | venue |
| `requestSuggestion` | POST |  | venue |
| `resumeActionPlan` | POST |  | venue |
| `resumeAiCapability` | POST |  | tenant |
| `retryActionStep` | POST |  | venue |
| `revokeAiPolicyException` | POST |  | tenant |
| `rollbackActionPlan` | POST |  | venue |
| `rollbackAiRelease` | POST |  | tenant |
| `runAiControlTest` | POST |  | tenant |
| `runAiEvaluation` | POST |  | tenant |
| `runForecast` | POST |  | venue |
| `scoreApprovalRequest` | POST |  | venue |
| `scoreTransactionRisk` | POST |  | venue |
| `searchAiDecisions` | GET |  | venue |
| `semanticSearch` | POST |  | venue |
| `sendAiMessage` | POST |  | venue |
| `setAiByokEnablement` | PUT |  | tenant |
| `setAiCredential` | PUT |  | tenant |
| `setAiModel` | PUT |  | platform |
| `setAiPolicy` | PUT |  | venue |
| `setAiProvider` | PUT |  | tenant |
| `setAiRiskRegisterEntry` | PUT |  | tenant |
| `setAiTool` | PUT |  | platform |
| `setAiVenueSettings` | PUT |  | venue |
| `setForecastDefinition` | PUT |  | venue |
| `setIndexSource` | PUT |  | tenant |
| `setSuggestionProvider` | PUT |  | tenant |
| `simulateActionPlan` | POST |  | venue |
| `simulateAiGovernancePolicy` | POST |  | tenant |
| `simulateRecommendationDecision` | POST |  | venue |
| `startConfigurationSession` | POST |  | venue |
| `suggestGuidedChoice` | POST |  | venue |
| `testAiProvider` | POST |  | tenant |

**2 elsewhere, writing a `ai.*` table.** Each one is another contract reaching into this domain, which is worth seeing rather than hiding.

- `askReportingQuestion` in `reporting`
- `saveNaturalLanguageQuery` in `reporting`

## States

| Model | Contract | Enum | Emits |
|---|---|---|---|
| `ai-action-plan.yaml` | ai | `AiActionPlan.status` | `ai.planExecuted`, `ai.planFailed` |
| `ai-capability.yaml` | ai | `AiCapabilityRegistration.status` | `ai.capabilityPaused` |
| `ai-evaluation-run.yaml` | ai | `AiEvaluationRun.status` | — |
| `ai-evidence-package.yaml` | ai | `AiEvidencePackage.status` | — |
| `ai-forecast-scenario.yaml` | ai | `AiForecastScenario.status` | — |
| `ai-forecast-version.yaml` | ai | `AiForecastVersion.status` | `ai.forecastPublished` |
| `ai-governance-alert.yaml` | ai | `AiGovernanceAlert.status` | — |
| `ai-governance-policy-version.yaml` | ai | `AiGovernancePolicyVersion.status` | — |
| `ai-guided-choice-suggestion.yaml` | ai | `AiGuidedChoiceSuggestion.status` | — |
| `ai-incident.yaml` | ai | `AiIncident.status` | — |
| `ai-index-job.yaml` | ai | `IndexJob.status` | — |
| `ai-insight.yaml` | ai | `AiInsight.status` | — |
| `ai-knowledge-document.yaml` | ai | `KnowledgeDocument.status` | — |
| `ai-layout-draft.yaml` | ai | `LayoutDraft.status` | — |
| `ai-operational-requirement.yaml` | ai | `AiOperationalRequirement.status` | `ai.operationalRequirementIssued` |
| `ai-policy-exception.yaml` | ai | `AiPolicyException.status` | — |
| `ai-proposed-action.yaml` | ai | `ProposedAction.status` | — |
| `ai-risk-case.yaml` | ai | `AiRiskCase.status` | `ai.riskCaseClosed` |
| `ai-tool.yaml` | ai | `AiTool.status` | — |
| `approval-request.yaml` | approvals | `ApprovalStatus` | `approval.escalated`, `approval.expired`, `approval.granted`, `approval.rejected`, `approval.requested`, `approval.stepCompleted` |
| `cart.yaml` | orders | `CartStatus` | `cart.abandoned` |
| `case.yaml` | marketing-crm | `CaseStatus` | `marketing.caseClosed` |
| `chargeback.yaml` | orders | `Chargeback.status` | `order.chargebackRecorded` |
| `content.yaml` | white-label | `ContentStatus` | `whitelabel.contentPublished` |
| `conversation.yaml` | marketing-crm | `ConversationState` | `conversation.handedOver` |
| `entitlement-status.yaml` | orders | `EntitlementStatus` | `access.validated` |
| `media.yaml` | assets | `MediaStatus` | `assets.documentIndexed` |
| `order.yaml` | orders | `OrderStatus` | `order.cancelled`, `order.completed`, `order.paid`, `order.refunded` |
| `payment.yaml` | orders | `Payment.status` | `order.paid` |
| `performance.yaml` | catalogue | `Performance.status` | `performance.cancelled` |
| `period.yaml` | finance | `PeriodStatus` | `ledger.periodClosed` |
| `product.yaml` | catalogue | `ProductLifecycleState` | `catalogue.productPublished` |
| `promotion.yaml` | promotions | `PromotionStatus` | `promotions.recommendationStrategyPublished` |
| `refund.yaml` | orders | `Refund.status` | `order.refunded` |
| `registered-device.yaml` | tenancy | `RegisteredDevice.status` | `device.statusChanged` |
| `resale-listing.yaml` | orders | `ResaleListing.status` | `entitlement.transferred` |
| `schedule.yaml` | white-label | `ScheduleState` | `whitelabel.contentPublished` |
| `seat.yaml` | seating | `SeatStatus` | `seat.blocked`, `seat.held`, `seat.released`, `seat.sold` |
| `shift.yaml` | shift | `ShiftStatus` | `shift.closed` |
| `stock-count.yaml` | inventory | `CountStatus` | `stock.depleted` |
| `tenant.yaml` | subscription | `TenantStatus` | `tenant.suspended` |
| `ticket-transfer.yaml` | orders | `TicketTransfer.status` | `entitlement.transferred` |

## Events

| Event | Role | Publisher | Critical consumer |
|---|---|---|---|
| `access.rejected` | consumes | access | no |
| `access.validated` | consumes | access | yes |
| `ai.capabilityPaused` | publishes | ai | yes |
| `ai.ceilingApproaching` | publishes | ai | yes |
| `ai.forecastPublished` | publishes | ai | no |
| `ai.incidentOpened` | publishes | ai | yes |
| `ai.insightRaised` | publishes | ai | no |
| `ai.operationalRequirementIssued` | publishes | ai | yes |
| `ai.planExecuted` | publishes | ai | yes |
| `ai.planFailed` | publishes | ai | yes |
| `ai.riskAlertRaised` | publishes | ai | yes |
| `ai.riskCaseClosed` | publishes | ai | yes |
| `approval.expired` | consumes | approvals | no |
| `approval.granted` | consumes | approvals | yes |
| `approval.rejected` | consumes | approvals | yes |
| `assets.documentIndexed` | consumes | assets | yes |
| `cart.abandoned` | consumes | orders | yes |
| `catalogue.productPublished` | consumes | catalogue | yes |
| `conversation.handedOver` | consumes | marketing | yes |
| `device.statusChanged` | consumes | tenancy | no |
| `entitlement.expiringSoon` | consumes | access | no |
| `entitlement.issued` | consumes | access | yes |
| `entitlement.transferred` | consumes | catalogue | no |
| `fnb.menuPublished` | consumes | fnb | yes |
| `identity.credentialResetRequested` | consumes | identity | no |
| `identity.loginRecorded` | consumes | identity | no |
| `ledger.periodClosed` | consumes | ledger | yes |
| `maintenance.templatePublished` | consumes | maintenance | yes |
| `marketing.caseClosed` | consumes | marketing | yes |
| `order.cancelled` | consumes | orders | no |
| `order.chargebackRecorded` | consumes | orders | no |
| `order.completed` | consumes | orders | no |
| `order.exchanged` | consumes | orders | no |
| `order.paid` | consumes | orders | yes |
| `order.refunded` | consumes | orders | yes |
| `payment.attemptFailed` | consumes | payments | no |
| `payment.captured` | consumes | orders | no |
| `performance.cancelled` | consumes | catalogue | yes |
| `promotions.recommendationStrategyPublished` | consumes | promotions | no |
| `reporting.definitionPublished` | consumes | reporting | yes |
| `retail.merchandisePublished` | consumes | retail | yes |
| `seat.sold` | consumes | seating | yes |
| `shift.closed` | consumes | shift | yes |
| `stock.depleted` | consumes | inventory | yes |
| `storefront.sessionEvent` | consumes | whitelabel | no |
| `tenant.suspended` | consumes | subscription | yes |
| `whitelabel.contentPublished` | consumes | whitelabel | yes |

## Storage

**`postgres`** — 122

`ai.action_plan` · `ai.action_step` · `ai.anomaly_detector` · `ai.answer_feedback` · `ai.approval_request_score` · `ai.assistant_profile` · `ai.blueprint` · `ai.blueprint_decision` · `ai.byok_enablement` · `ai.capability` · `ai.capability_maturity` · `ai.case_action` · `ai.case_evidence` · `ai.chunk_embedding` · `ai.config_session` · `ai.config_source` · `ai.control` · `ai.control_test` · `ai.decision_record` · `ai.entity_risk` · `ai.eval_run` · `ai.eval_suite` · `ai.evidence_package` · `ai.forecast_accuracy` · `ai.forecast_definition` · `ai.forecast_export` · `ai.forecast_point` · `ai.forecast_scenario` · `ai.forecast_version` · `ai.governance_alert` · `ai.governance_policy` · `ai.governance_policy_version` · `ai.guided_choice_suggestion` · `ai.history_import` · `ai.history_observation` · `ai.incident` · `ai.index_entry` · `ai.index_failure` · `ai.index_job` · `ai.index_source` · `ai.insight` · `ai.intervention` · `ai.knowledge_collection` · `ai.knowledge_document` · `ai.knowledge_gap` · `ai.layout_draft` · `ai.model` · `ai.operational_requirement` · `ai.policy` · `ai.policy_exception` · `ai.prompt_template` · `ai.proposed_action` · `ai.provider` · `ai.rec_decision` · `ai.rec_decline` · `ai.rec_event` · `ai.release` · `ai.risk_alert` · `ai.risk_assessment` · `ai.risk_case` · `ai.risk_edge` · `ai.risk_register` · `ai.risk_strategy` · `ai.signal_source` · `ai.tool` · `ai.training_run` · `ai.venue_settings` · `approvals.request` · `approvals.sla_policy` · `assets.media_asset` · `catalogue.channel_capacity` · `catalogue.entitlement_template` · `catalogue.event` · `catalogue.performance` · `catalogue.price` · `catalogue.price_list` · `catalogue.product` · `catalogue.variant_dimension` · `control.content_block` · `fnb.menu_item` · `fnb.production_plan` · `inventory.movement` · `inventory.stock_batch` · `maintenance.inspection_template` · `marketing.attribution_touch` · `marketing.audience_list` · `marketing.campaign` · `marketing.case` · `marketing.consent_record` · `marketing.guest_profile` · `marketing.loyalty_position` · `marketing.loyalty_programme` · `marketing.message_template` · `marketing.message_template_version` · `marketing.segment` · `marketing.segment_criterion` · `orders.order_line` · `platform.region_settings` · `platform.scope` · `promotions.promotion` · `queue.queue` · `queue.reading` · `reporting.report_definition` · `retail.merchandise` · `seating.accessible` · `seating.seat` · `seating.seat_category` · `seating.seat_map` · `seating.seating_rules` · `seating.section` · `seating.zone` · `venuemap.import_job` · `venuemap.map` · `venuemap.point` · `venuemap.visit_plan` · `venuemap.visit_plan_item` · `whitelabel.banner` · `whitelabel.content_page` · `whitelabel.faq_entry` · `whitelabel.homepage_section` · `whitelabel.policy` · `whitelabel.promo_block`

**`postgres-analytical`** — 5

`ai.activity` · `ai.conversation` · `ai.message` · `ai.suggestion` · `ai.suggestion_outcome`

**`qdrant`** — 1

`qdrant:knowledge`

**`redis`** — 9

`cache:ai-breaker` · `cache:answer` · `cache:embedding` · `cache:governance-policy` · `cache:idempotency` · `cache:rec-candidates` · `cache:rec-features` · `cache:resolution` · `cache:risk-features`

## Screens

**P01 Guest Web**

- `WEB-001` Home / Landing — wave 1, 2 operations
- `WEB-008` Add-ons & Upsell — wave 2, 2 operations
- `WEB-043` Loyalty & Rewards — wave 2, 2 operations
- `WEB-044` AI Concierge – Home — wave 2, 5 operations

**P02 Guest App**

- `GST-001` Home — wave 1, 2 operations
- `GST-031` AI Concierge – Home — wave 2, 3 operations
- `GST-032` AI Concierge – Chat — wave 2, 2 operations
- `GST-033` AI Concierge – Contextual Help — wave 2, 1 operation
- `GST-036` Loyalty & Rewards — wave 2, 2 operations
- `GST-048` Upsell / Cross-Sell — wave 2, 2 operations
- `GST-054` AI Planner — wave 1, 3 operations
- `GST-068` Help & My Cases — wave 2, 1 operation

**P04 Venue POS**

- `POS-008` Reports — wave 2, 2 operations

**P05 Guest Kiosk**

- `KSK-015` Assistant — wave 2, 2 operations

**P06 Venue Staff App**

- `EMP-019` AI assistant — home — wave 1, 3 operations
- `EMP-020` AI assistant — answer — wave 1, 4 operations
- `EMP-031` Queue monitor — wave 2, 1 operation
- `EMP-040` Knowledge base — wave 2, 1 operation
- `EMP-041` Training — wave 3, 1 operation

**P08 Venue Management**

- `BO-005` Queue Monitor — wave 1, 1 operation
- `BO-029` Report Builder — wave 2, 2 operations
- `BO-058` Reporting Home — wave 1, 2 operations
- `BO-059` Sales Reports — wave 1, 2 operations
- `BO-060` Attendance & Footfall — wave 2, 2 operations
- `BO-084` Approval Inbox — wave 1, 1 operation
- `BO-088` Approval Analytics — wave 3, 1 operation
- `BO-091` AI Policy & Spend — wave 1, 8 operations
- `BO-093` Map Import & Labelling — wave 2, 1 operation
- `BO-102` Sell — wave 1, 2 operations
- `BO-1048` Seat Upsell Recommendations — wave 3, 1 operation
- `BO-115` Category, Brand & Merchandise Hierarchy — wave 2, 1 operation
- `BO-1160` Fraud Alert & Investigation Case Management — wave 3, 5 operations
- `BO-117` Product Import, Governance & AI Configuration Assistant — wave 2, 2 operations
- `BO-119` Cross-Sell, Upsell & Recommendation Rules — wave 2, 1 operation
- `BO-138` Production Execution & Batch Management — wave 2, 1 operation
- `BO-139` Wastage, Spoilage, Returns & Write-Off — wave 2, 1 operation
- `BO-367` Approval Request Detail — wave 3, 1 operation
- `BO-369` High Priority & Risk Queue — wave 3, 1 operation
- `BO-593` AI Rental Management Copilot & Action Center — wave 3, 1 operation
- `BO-597` AI Configuration Workspace — wave 3, 2 operations
- `BO-598` AI Draft Review & Approval — wave 3, 2 operations
- `BO-761` AI Audience Discovery — wave 3, 1 operation
- `BO-762` Predictive Audiences — wave 3, 2 operations
- `BO-764` Campaign Command Center — wave 3, 1 operation
- `BO-766` Campaign Builder — wave 3, 1 operation
- `BO-772` A/B & AI Optimization — wave 3, 4 operations
- `BO-782` AI Journey Optimization — wave 3, 3 operations
- `BO-785` Template Library — wave 3, 2 operations
- `BO-786` Newsletter Builder — wave 3, 1 operation
- `BO-787` Content Blocks & Product Feed — wave 3, 1 operation
- `BO-789` Transactional Notification Rules — wave 3, 1 operation
- `BO-793` AI Content, Translation & Audit — wave 3, 3 operations
- `BO-798` Intent & Knowledge Management — wave 3, 1 operation
- `BO-919` AI Event Resource Forecasting — wave 3, 3 operations
- `BO-925` AI Staff Recommendation & Workforce Matching — wave 3, 2 operations
- `BO-926` Resource Demand Forecasting — wave 3, 2 operations
- `BO-927` AI Staffing Requirement Forecast — wave 3, 3 operations
- `BO-928` AI Conflict Resolution Assistant — wave 3, 4 operations
- `BO-929` Automatic Schedule Optimization — wave 3, 3 operations
- `BO-931` Operational Scenario Simulator & Digital Twin — wave 3, 2 operations
- `BO-932` Conversational AI Resource Copilot — wave 3, 3 operations
- `BO-959` Stage & Focal Point — wave 3, 1 operation
- `BO-970` AI Numbering & Labeling — wave 3, 3 operations
- `BO-975` Event-Specific Layout — wave 3, 3 operations
- `BO-982` Approval, Publish & Rollback — wave 3, 1 operation

**P09 TICVAI Web**

- `ADM-004` Platform Audit Log — wave 2, 2 operations
- `ADM-037` AI Provider & Credentials — wave 1, 10 operations
- `ADM-047` AI Delivery Optimization & Communication Platform Diagnostics — wave 3, 1 operation
- `ADM-249` Unified Approval Inbox & Decision Workspace — wave 3, 1 operation
- `ADM-366` AI Approval Intelligence Center — wave 3, 1 operation
- `ADM-469` AI Configuration Home & Start — wave 3, 3 operations
- `ADM-470` Setup Type & Business Intent Discovery — wave 3, 4 operations
- `ADM-471` Venue & Business Model Discovery — wave 3, 2 operations
- `ADM-472` Guided Question & Answer Workspace — wave 3, 2 operations
- `ADM-473` Product & Admission Model Discovery — wave 3, 2 operations
- `ADM-474` Operational Requirement Discovery — wave 3, 2 operations
- `ADM-475` Commercial Requirement Discovery — wave 3, 2 operations
- `ADM-476` Required, Recommended & Optional Decisions — wave 3, 2 operations
- `ADM-477` Missing Information & Clarification Center — wave 3, 5 operations
- `ADM-478` Configuration Blueprint & Dependency Map — wave 3, 2 operations
- `ADM-479` AI Configuration Build Command Center — wave 3, 3 operations
- `ADM-480` Venue & Organization Configuration — wave 3, 3 operations
- `ADM-481` Product Configuration Assistant — wave 3, 3 operations
- `ADM-482` Schedule, Capacity & Availability Configuration — wave 3, 3 operations
- `ADM-483` Pricing & Commercial Configuration — wave 3, 3 operations
- `ADM-484` Promotion, Bundle & Upsell Configuration — wave 3, 3 operations
- `ADM-485` Seating, Access & Operational Configuration — wave 3, 3 operations
- `ADM-486` Channel, Media & Fulfillment Configuration — wave 3, 3 operations
- `ADM-487` Cross-Module Conflict & Dependency Validation — wave 3, 2 operations
- `ADM-488` Configuration Preview & Impact Analysis — wave 3, 2 operations
- `ADM-489` AI Configuration Readiness Center — wave 3, 4 operations
- `ADM-490` Configuration Validation Results — wave 3, 2 operations
- `ADM-491` AI Recommendations & Best-Practice Review — wave 3, 2 operations
- `ADM-492` Configuration Approval Workflow — wave 3, 3 operations
- `ADM-493` AI Configuration Execution Center — wave 3, 3 operations
- `ADM-494` Execution Progress & Dependency Monitor — wave 3, 4 operations
- `ADM-495` Configuration Results & Object Mapping — wave 3, 2 operations
- `ADM-496` Configuration Change & Modification Assistant — wave 3, 3 operations
- `ADM-497` Configuration History, Versions & Rollback — wave 3, 3 operations
- `ADM-498` AI Configuration Audit & Governance — wave 3, 2 operations
- `ADM-499` Forecasting Command Center — wave 3, 3 operations
- `ADM-500` Forecast Configuration & Forecasting Strategy — wave 3, 3 operations
- `ADM-501` Forecast Data & Signal Configuration — wave 3, 3 operations
- `ADM-502` Attendance & Visitation Forecast — wave 3, 3 operations
- `ADM-503` Ticket, Product & Timeslot Demand Forecast — wave 3, 1 operation
- `ADM-504` Channel & Booking Pace Forecast — wave 3, 1 operation
- `ADM-505` Revenue & Commercial Forecast — wave 3, 1 operation
- `ADM-506` Forecast Drivers, Confidence & Explainability — wave 3, 4 operations
- `ADM-507` Forecast Scenario & What-If Simulator — wave 3, 3 operations
- `ADM-508` Forecast Accuracy, Review & Publication Center — wave 3, 5 operations
- `ADM-509` Operational Forecasting Command Center — wave 3, 2 operations
- `ADM-510` Capacity & Occupancy Forecast — wave 3, 4 operations
- `ADM-511` Attraction Utilization & Queue Forecast — wave 3, 3 operations
- `ADM-512` Entry, Access & Guest Flow Forecast — wave 3, 2 operations
- `ADM-513` Workforce Demand & Staffing Forecast — wave 3, 2 operations
- `ADM-514` POS, Kiosk & Frontline Service Forecast — wave 3, 2 operations
- `ADM-515` F&B, Retail & Inventory Demand Forecast — wave 3, 2 operations
- `ADM-516` Resource, Equipment & Facility Requirement Forecast — wave 3, 2 operations
- `ADM-517` Operational Scenario & Readiness Simulator — wave 3, 3 operations
- `ADM-518` Operational Forecast Review, Recommendations & Handover — wave 3, 2 operations
- `ADM-519` AI Governance Command Center — wave 3, 5 operations
- `ADM-520` AI Capability Registry & Ownership — wave 3, 2 operations
- `ADM-521` AI Risk Classification & Assessment — wave 3, 2 operations
- `ADM-522` AI Autonomy Level Configuration — wave 3, 3 operations
- `ADM-523` AI Action & Permission Policy Builder — wave 3, 4 operations
- `ADM-524` AI Data Access & Usage Policy — wave 3, 2 operations
- `ADM-525` Environment, Tenant & Scope Governance — wave 3, 2 operations
- `ADM-526` AI Policy Conflict, Exception & Override Management — wave 3, 4 operations
- `ADM-527` AI Policy Testing & Governance Simulation — wave 3, 2 operations
- `ADM-528` AI Governance Policy Publication & Effective Policy Map — wave 3, 3 operations
- `ADM-529` AI Human Oversight Command Center — wave 3, 2 operations
- `ADM-530` AI Approval Requirement & Routing Configuration — wave 3, 3 operations
- `ADM-531` AI Approval Review Workspace — wave 3, 3 operations
- `ADM-532` Conditional Approval & Approval Conditions — wave 3, 2 operations
- `ADM-533` Human Review, Challenge & AI Clarification Workspace — wave 3, 3 operations
- `ADM-534` Escalation, Delegation & Approval SLA Management — wave 3, 2 operations
- `ADM-535` Live AI Execution Oversight & Human Intervention — wave 3, 5 operations
- `ADM-536` Human Override & Manual Control Center — wave 3, 4 operations
- `ADM-537` Approval & Intervention History / Decision Timeline — wave 3, 2 operations
- `ADM-538` Human Oversight Workflow Simulator & Readiness Center — wave 3, 2 operations
- `ADM-539` AI Explainability & Audit Command Center — wave 3, 1 operation
- `ADM-540` AI Decision Explorer & Search — wave 3, 2 operations
- `ADM-541` AI Decision Explanation Workspace — wave 3, 1 operation
- `ADM-542` Data, Feature & Evidence Provenance — wave 3, 1 operation
- `ADM-543` Candidate, Rule & Decision Path Trace — wave 3, 2 operations
- `ADM-544` Model, Provider & AI Runtime Trace — wave 3, 2 operations
- `ADM-545` Governance, Approval & Human Decision Trace — wave 3, 1 operation
- `ADM-546` Execution & Business Outcome Trace — wave 3, 2 operations
- `ADM-547` AI Audit Record & Evidence Package — wave 3, 2 operations
- `ADM-548` AI Trace Investigation & Replay Simulator — wave 3, 2 operations
- `ADM-549` AI Governance Monitoring Command Center — wave 3, 4 operations
- `ADM-550` AI Risk Register & Risk Exposure Management — wave 3, 2 operations
- `ADM-551` AI Governance Control Library & Control Effectiveness — wave 3, 2 operations
- `ADM-552` AI Policy Compliance & Violation Monitoring — wave 3, 2 operations
- `ADM-553` AI Data, Privacy & Usage Compliance Monitoring — wave 3, 2 operations
- `ADM-554` AI Quality, Behavior & Governance Drift Monitoring — wave 3, 6 operations
- `ADM-555` AI Governance Alert & Detection Center — wave 3, 3 operations
- `ADM-556` AI Incident & Remediation Management — wave 3, 6 operations
- `ADM-557` AI Compliance, Assurance & Governance Reporting — wave 3, 3 operations
- `ADM-558` AI Governance Review, Action Plan & Continuous Improvement — wave 3, 2 operations
- `ADM-633` Fraud Alert, Investigation & Case Management\t170 — wave 3, 9 operations
- `ADM-637` AI Fraud, Anomaly & Payment Intelligence Center\t175 — wave 3, 3 operations
- `ADM-638` Payment Executive Intelligence, Risk Simulator & AI Advisor\t176 — wave 3, 1 operation
- `ADM-678` Journey Simulator, Decision Trace & AI Optimization — wave 3, 1 operation
- `ADM-680` Customer Recommendation Profile — wave 3, 2 operations
- `ADM-683` Next-Best-Offer Decision Studio — wave 3, 1 operation
- `ADM-686` Anonymous, Known & Identity-Transition Personalization.123 — wave 3, 1 operation
- `ADM-687` AI Explainability, Confidence & Model Governance — wave 3, 1 operation
- `ADM-696` AI Risk, Fairness, Explainability & Safety Center — wave 3, 1 operation
- `ADM-697` Recommendation Audit, Decision Trace & Investigation — wave 3, 1 operation

**P10 Partner Web**

- `PTR-018` Reports & Sales Performance — wave 3, 2 operations

**P12 Venue Support**

- `SUP-006` Knowledge Base Search — wave 3, 2 operations
- `SUP-008` Agent Performance & SLA View — wave 3, 2 operations
- `SUP-018` AI Customer Service Copilot & Knowledge Workspace — wave 3, 2 operations

**P13 Venue CMS**

- `CMS-007` Page Builder — wave 2, 2 operations
- `CMS-008` Content Blocks — wave 2, 2 operations
- `CMS-010` Media Library — wave 2, 1 operation
- `CMS-062` Central Digital Asset Library — wave 3, 1 operation
- `CMS-101` Help Me Choose — wave 2, 2 operations
- `CMS-104` App Build & Store Publishing — wave 1, 2 operations

**P15 Kitchen Display**

- `KIT-010` Kitchen Performance, AI & Operational Optimization — wave 2, 1 operation

**P16 Venue Analytics**

- `ANL-001` Executive Command Center — wave 3, 2 operations
- `ANL-006` Inventory & Waste Intelligence — wave 3, 1 operation
- `ANL-008` Demand Forecasting — wave 3, 2 operations
- `ANL-009` AI Assistant & Action Center — wave 3, 4 operations
- `ANL-010` Suggestions & Advice — wave 3, 2 operations
- `ANL-019` AI Management Insights — wave 3, 4 operations
- `ANL-052` Ask TICVAI — Natural Language Analytics — wave 3, 2 operations
- `ANL-055` Anomaly Detection Center — wave 3, 3 operations
- `ANL-056` Root-Cause Analysis Explorer — wave 3, 2 operations
- `ANL-057` Forecasting & Predictive Analytics Studio — wave 3, 4 operations
- `ANL-058` AI Recommendation & Next-Best-Action Center — wave 3, 1 operation
- `ANL-059` AI Insight History, Evidence & Explainability — wave 3, 2 operations
- `ANL-060` AI Analytics Governance & Model Control — wave 3, 8 operations
- `ANL-071` AI Maturity & Learning — wave 3, 6 operations

## Flows

- **F100** An AI provider is configured, budgeted and audited — wave 2
- **F101** A staff member asks the assistant and it answers from the venue — wave 2
- **F106** A security dashboard surfaces something and it is investigated — wave 3
- **F20** A manager asks a question and gets an answer — wave 1
- **F24** A guest asks the assistant and ends up with a person — wave 2
- **F26** A venue maps its site — wave 2
- **F49** A guest plans a day and follows it — wave 1
- **F77** A promotion is built, bundled, published and measured — wave 3
- **F82** A month is analysed from incrementality to a scheduled report — wave 3
- **F86** A POS layout is designed, previewed and deployed — wave 2
- **F90** An audience is built, offered to, and the result is judged — wave 3

## Decisions and documents

| Document | Status | Mentions |
|---|---|---|
| [Action register — 22 September 2026](..\docs\active\action-register-22-september.md) |  | 6 |
| [AI functions review: build every AI function now, then let it learn](..\docs\active\ai-functions-review-30-september.md) |  | 18 |
| [AI scope — for confirmation](..\docs\active\ai-scope-for-confirmation.md) |  | 1 |
| [AI suggestion rules: one rule and a minimum history per kind](..\docs\active\ai-suggestion-rules-proposal.md) |  | 3 |
| [BL-073 — cookie consent: what to buy, what to build, what is ours either way](..\docs\active\bl-073-cookie-consent-20-september.md) |  | 1 |
| [The event broker: RabbitMQ or Kafka](..\docs\active\broker-decision-pack.md) |  | 2 |
| [Build plan — 20 September 2026](..\docs\active\build-plan-20-september.md) |  | 1 |
| [Validating the developer team's Change Log](..\docs\active\change-log-validation-18-september.md) |  | 2 |
| [Configured limits: proposed values](..\docs\active\configured-limits-proposal.md) |  | 1 |
| [Contract audit — every contract against the four things that must agree with it](..\docs\active\contract-audit-19-september.md) |  | 7 |
| [The contract run — plan](..\docs\active\contract-run-plan-19-september.md) |  | 1 |
| [Current work](..\docs\active\current-work.md) |  | 2 |
| [Deep audit — module-wise build clearance](..\docs\active\deep-audit-21-september.md) |  | 1 |
| [Deep audit — ten invariants, run adversarially](..\docs\active\deep-audit-24-august.md) |  | 3 |
| [Deployment architecture — four configurations, costed on AWS and GCP](..\docs\active\deployment-configs-costed.md) |  | 7 |
| [Design pack coverage: the 40 "undrafted" PDFs](..\docs\active\design-pack-coverage.md) |  | 11 |
| [TICVAI development plan](..\docs\active\development-plan.md) |  | 1 |
| [Audit — the 3 September dump, its checks, and what trickles down](..\docs\active\dump-audit-3-september.md) |  | 2 |
| [Full-layer audit — 20 August](..\docs\active\full-layer-audit-20aug.md) |  | 3 |
| [TICVAI — Hierarchy, Data Segregation and Services](..\docs\active\hierarchy-segregation-services.md) |  | 1 |
| [Infrastructure answers: Qdrant, PostgreSQL extensions, the broker, the network and the cost sheet](..\docs\active\infra-answers-30-september.md) |  | 1 |
| [Optimisation assessment — RAG, caching, backend, frontend](..\docs\active\optimisation-assessment.md) |  | 4 |
| [Optimisation adoption plan](..\docs\active\optimisation-plan.md) |  | 3 |
| [Phase 0 — identity pass, all clusters](..\docs\active\phase0-identity-pass-all-clusters.md) |  | 2 |
| [Active](..\docs\active\README.md) |  | 1 |
| [> **SUPERSEDED, 20 September.** Written when 151 of 223 were reviewed and the review was](..\docs\active\rename-worklist-20-september.md) |  | 2 |
| [Schema merge — the decision log](..\docs\active\schema-merge-decision-log.md) |  | 2 |
| [Schema merge — final report](..\docs\active\schema-merge-final-report-20-september.md) |  | 2 |
| [Identical operation sets — what each cluster actually is](..\docs\active\screen-duplicate-triage.md) |  | 5 |
| [Screen estate audit — duplication, connectivity, and stranded capability](..\docs\active\screen-estate-audit.md) |  | 3 |
| [Regenerating the screen layer — plan](..\docs\active\screen-regeneration-plan.md) |  | 1 |
| [Six-month build plan, re-planned 29 September 2026](..\docs\active\six-month-plan-29-september.md) |  | 1 |
| [Ch03 capability coverage - the client's list against our screens](..\docs\active\spec-coverage-19-september.md) |  | 1 |
| [TICVAI system design review (re-audit before Block A tickets)](..\docs\active\system-design-review-30-september.md) |  | 4 |
| [The 26 undrafted packs — what is in them and what they would cost](..\docs\active\undrafted-packs-scope-20-september.md) |  | 1 |
| [Viewer — what changed in the package on 20 August](..\docs\active\viewer-update-brief-20aug.md) |  | 1 |
| [Workshop pack — what was done, and how to re-verify it](..\docs\active\workshop-pack-log.md) |  | 3 |
| [ADR-0007: Hybrid repository topology](..\docs\adr\0007-hybrid-repository-topology.md) | Accepted | 1 |
| [ADR-0020 — Where AI runs, and what it is isolated from](..\docs\adr\0020-ai-isolation-boundary.md) | Accepted · 30 September 2026 · Chinmay Parab — amended by [A | 20 |
| [ADR-0021 — Qdrant: one collection per embedding model, tenant is the shard, scope is the filter](..\docs\adr\0021-qdrant-partitioning.md) | Accepted in part · amended by [ADR-0049](0049-vectors-live-i | 4 |
| [ADR-0023 — Personal data lives apart from the append-only ledger](..\docs\adr\0023-pii-separation.md) | Accepted · 17 August 2026, recording a decision already impl | 2 |
| [ADR-0028: Seventeen modules, and the data boundary decides where they split](..\docs\adr\0028-service-decomposition.md) | Accepted · amended by [ADR-0055](0055-a-modular-monolith-dep | 1 |
| [ADR-0033: Every asynchronous handoff has an outbox and a place to fail](..\docs\adr\0033-outbox-and-dead-letters.md) | Accepted · amended by [ADR-0058](0058-one-relay-per-region-a | 3 |
| [ADR-0034: The cheapest AI call is the one that never reaches a provider](..\docs\adr\0034-ai-retrieval-and-cost.md) | Accepted | 6 |
| [ADR-0046: On-premise has two configurations, and the difference is a control channel](..\docs\adr\0046-on-premise-has-two-configurations.md) | Accepted | 1 |
| [ADR-0047: How long data is kept, and where it goes next](..\docs\adr\0047-how-long-data-is-kept-and-where-it-goes-next.md) | Accepted — the RPO floor decided 21 September; one number pe | 2 |
| [ADR-0049: Vectors live in Qdrant from day one, one collection per tenant, each with its own token](..\docs\adr\0049-vectors-live-in-qdrant-one-collection-per-tenant.md) | Accepted · 30 September 2026 · Chinmay Parab | 2 |
| [ADR-0050: One autonomy scale; the approval tier is not an autonomy level](..\docs\adr\0050-one-autonomy-scale.md) | Accepted · 30 September 2026 · Chinmay Parab — records AI-D0 | 1 |
| [ADR-0051: Every AI function ships on a baseline and learns per tenant; a model goes live only on evidence](..\docs\adr\0051-ai-ships-on-a-baseline-and-learns-per-tenant.md) | Accepted · 30 September 2026 · Chinmay Parab | 5 |
| [ADR-0052: One recommendation engine; runtime in AI, configuration in Promotions](..\docs\adr\0052-one-recommendation-engine.md) | Accepted · 1 October 2026 · Chinmay Parab — records AI-D07,  | 1 |
| [ADR-0053: Owners keep their deterministic rules; AI owns cross-entity risk, alerts and cases](..\docs\adr\0053-risk-layer-ownership.md) | Accepted · 1 October 2026 · Chinmay Parab — records AI-D06,  | 2 |
| [ADR-0054: Natural-language analytics goes through the semantic layer](..\docs\adr\0054-natural-language-analytics-goes-through-the-semantic-layer.md) | Accepted · 1 October 2026 · Chinmay Parab — records AI-D13 a | 3 |
| [ADR-0055: A modular monolith, deployed as five units](..\docs\adr\0055-a-modular-monolith-deployed-as-five-units.md) | Accepted · 30 September 2026 · Chinmay Parab | 1 |
| [ADR-0057: Events travel on RabbitMQ or Kafka, behind one kernel interface](..\docs\adr\0057-events-travel-on-rabbitmq-or-kafka.md) | Proposed · waiting on the client's choice between RabbitMQ a | 1 |
| [ADR-0058: One relay per region reads every tenant's outbox, and every consumer has an inbox](..\docs\adr\0058-one-relay-per-region-and-an-inbox-per-tenant-database.md) | Accepted · 30 September 2026 · Chinmay Parab · amended 1 Oct | 1 |
| [ADR-0059: AI phasing against the six-month plan](..\docs\adr\0059-ai-phasing-against-the-six-month-plan.md) | Accepted · 30 September 2026 · Chinmay Parab | 6 |
| [ADR-0060: Availability targets per tier, and how they are met](..\docs\adr\0060-availability-targets-high-availability-and-disaster-recovery.md) | Proposed · waiting on the client (which services the 99.99%  | 1 |
| [ADR-0061: Replica floors are set per deployable and per zone](..\docs\adr\0061-replica-floors-per-deployable.md) | Accepted · 1 October 2026 · Chinmay Parab | 1 |
| [ADR-0063: Encryption and keys, and biometric templates stay with the biometric vendor](..\docs\adr\0063-encryption-keys-and-biometric-templates.md) | Proposed · waiting on the client's data protection officer ( | 1 |
| [ADR-0064: Every tenant has a request budget, and a busy tenant cannot starve the others](..\docs\adr\0064-per-tenant-limits.md) | Accepted · 1 October 2026 · Chinmay Parab | 1 |
| [AI provider credentials — where the key lives and who can reach it](..\docs\architecture\ai-credentials.md) |  | 3 |
| [TICVAI AI subsystem: system design](..\docs\architecture\ai-system-design.md) |  | 162 |
| [Data Model](..\docs\architecture\data-model.md) |  | 1 |
| [Architecture](..\docs\architecture\README.md) |  | 1 |

## Conflicts

**1 open** — **CF-165**

34 closed — CF-160 · CF-41 · CF-57 · CF-139 · CF-61 · CF-74 · CF-123 · CF-120 · CF-141 · CF-144 · CF-17 · CF-119 · CF-118 · CF-113 · CF-109 · CF-107 · CF-106 · CF-105 · CF-14 · CF-96 · CF-94 · CF-92 · CF-93 · CF-90 · CF-89 · CF-88 · CF-59 · CF-80 · CF-78 · CF-76 · CF-73 · CF-166 · CF-20 · CF-43

