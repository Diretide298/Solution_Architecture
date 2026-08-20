# AI — the whole set

**Derived, not written.** Regenerate with `python3 tools/derive-domain.py ai && python3 tools/render-domain.py ai`. Nothing below is hand-typed, so nothing here goes stale — which the hand-maintained version did four times on 17 August alone.

**ai has no folder and should not.** The package is organised by artefact kind, and a single domain folder would raise the question of why there is no `finance/`. This page gathers what is spread across layers; each artefact stays where it belongs.

| | |
|---|---|
| **Operations** | 29 |
| **Schemas** | 18 |
| **States** | 11 |
| **Events** | 11 |
| **Tables** | 48 |
| **Screens** | 22 |
| **Flows** | 3 |
| **Documents** | 9 |
| **Open conflicts** | 0 |

## Reached outside the contract

**The closure follows behaviour, not folders.** These state models live under other contracts and specify things this domain depends on — the hand-written index named none of them.

| Model | Lives under | Reached via |
|---|---|---|
| `approval-request.yaml` | `approvals` | `approval.granted` |
| `case.yaml` | `marketing-crm` | `marketing.caseClosed` |
| `content.yaml` | `white-label` | `whitelabel.contentPublished` |
| `conversation.yaml` | `marketing-crm` | `conversation.handedOver` |
| `media.yaml` | `assets` | `assets.documentIndexed` |
| `product.yaml` | `catalogue` | `catalogue.productPublished` |
| `schedule.yaml` | `white-label` | `whitelabel.contentPublished` |

## What it is walled off from

**A page showing only what a domain *is* answers half the question.** The other half is what it cannot reach, and what keeps that true rather than merely true today.

| | Holds | Enforced by |
|---|---|---|
| **The vector store is reached by one contract** — 1 collection, 9 operations, all in `ai`. No screen, service or other contract reaches it directly. | yes | tools/check-package.py — no non-AI contract writes an AI table |
| **Writes stay inside the domain** — AI reads the transactional core and writes only its own stores and caches. `generateVenueLayout` wrote into `seating.import_job` on 17 August and now stops at a draft. | yes | tools/check-package.py, with two stated exceptions (ADR-0020) |
| **Conversation logs sit off the transactional primary** — Prompt and response volume does not compete with a sale. 3 tables on the analytical store. | yes | ADR-0020, checked against the store map |
| **Every model call leaves an audit record** — 9 operations write an `ai.interaction` (8.3.55). | yes | tools/check-package.py — a model-calling operation with no interaction fails |
| **Only governed operations outside the domain may write to it** — 2 operations in other contracts write an `ai.*` table: ['askReportingQuestion', 'saveNaturalLanguageQuery']. Each is a governance record, not a bypass. | yes | tools/check-package.py allowlist, stated in ADR-0020 |

**Storage tiers** — `postgres` 41 · `postgres-analytical` 3 · `qdrant` 1 · `redis` 3

## Operations

**27 in the contract.**

| Operation | Verb | Guest | Scope |
|---|---|---|---|
| `createAiConversation` | POST |  | venue |
| `createKnowledgeCollection` | POST |  | tenant |
| `decideProposedAction` | POST |  | venue |
| `generateConfiguration` | POST |  | venue |
| `generateVenueLayout` | POST |  | venue |
| `getAiPolicy` | GET |  | tenant |
| `getAiUsage` | GET |  | tenant |
| `ingestKnowledgeDocument` | POST |  | tenant |
| `listAiConversations` | GET |  | venue |
| `listAiInteractions` | GET |  | tenant |
| `listAiProviders` | GET |  | region |
| `listIndexJobs` | GET |  | tenant |
| `listIndexSources` | GET |  | tenant |
| `listKnowledgeCollections` | GET |  | tenant |
| `listProposedActions` | GET |  | venue |
| `proposeTranslations` | POST |  | tenant |
| `proposeVenueLabels` | POST |  | venue |
| `proposeWalkways` | POST |  | venue |
| `reindexSource` | POST |  | tenant |
| `removeIndexEntry` | DELETE |  | tenant |
| `semanticSearch` | POST |  | venue |
| `sendAiMessage` | POST |  | venue |
| `setAiCredential` | PUT |  | tenant |
| `setAiPolicy` | PUT |  | tenant |
| `setAiProvider` | PUT |  | region |
| `setIndexSource` | PUT |  | tenant |
| `testAiProvider` | POST |  | tenant |

**2 elsewhere, writing a `ai.*` table.** Each one is another contract reaching into this domain, which is worth seeing rather than hiding.

- `askReportingQuestion` in `reporting`
- `saveNaturalLanguageQuery` in `reporting`

## States

| Model | Contract | Enum | Emits |
|---|---|---|---|
| `ai-index-job.yaml` | ai | `IndexJob.status` | — |
| `ai-knowledge-document.yaml` | ai | `KnowledgeDocument.status` | — |
| `ai-layout-draft.yaml` | ai | `LayoutDraft.status` | — |
| `ai-proposed-action.yaml` | ai | `ProposedAction.status` | — |
| `approval-request.yaml` | approvals | `ApprovalStatus` | `approval.granted`, `approval.rejected` |
| `case.yaml` | marketing-crm | `CaseStatus` | `marketing.caseClosed` |
| `content.yaml` | white-label | `ContentStatus` | `whitelabel.contentPublished` |
| `conversation.yaml` | marketing-crm | `ConversationState` | `conversation.handedOver` |
| `media.yaml` | assets | `MediaStatus` | `assets.documentIndexed` |
| `product.yaml` | catalogue | `ProductLifecycleState` | `catalogue.productPublished` |
| `schedule.yaml` | white-label | `ScheduleState` | `whitelabel.contentPublished` |

## Events

| Event | Role | Publisher | Critical consumer |
|---|---|---|---|
| `ai.ceilingApproaching` | publishes | ai | yes |
| `approval.granted` | consumes | approvals | yes |
| `assets.documentIndexed` | consumes | assets | yes |
| `catalogue.productPublished` | consumes | catalogue | yes |
| `conversation.handedOver` | consumes | marketing | yes |
| `fnb.menuPublished` | consumes | fnb | yes |
| `maintenance.templatePublished` | consumes | maintenance | yes |
| `marketing.caseClosed` | consumes | marketing | yes |
| `reporting.definitionPublished` | consumes | reporting | yes |
| `retail.merchandisePublished` | consumes | retail | yes |
| `whitelabel.contentPublished` | consumes | whitelabel | yes |

## Storage

**`postgres`** — 41

`ai.chunk_ref` · `ai.index_entry` · `ai.index_job` · `ai.index_source` · `ai.knowledge_collection` · `ai.knowledge_document` · `ai.layout_draft` · `ai.policy` · `ai.proposed_action` · `ai.provider` · `assets.media_asset` · `catalogue.attribute_axis` · `catalogue.entitlement_template` · `catalogue.envelope` · `catalogue.event` · `catalogue.performance` · `catalogue.price` · `catalogue.price_list` · `catalogue.product` · `control.content_block` · `fnb.menu_item` · `maintenance.inspection_template` · `marketing.case` · `marketing.conversation_message` · `marketing.loyalty_programme` · `platform.region_settings` · `platform.scope_node` · `promotions.promotion` · `reporting.report_definition` · `retail.merchandise` · `seating.seat` · `seating.seat_category` · `seating.seat_map` · `seating.seating_rules` · `seating.section` · `venuemap.import_job` · `venuemap.map` · `venuemap.point` · `whitelabel.content_page` · `whitelabel.faq_entry` · `whitelabel.policy`

**`postgres-analytical`** — 3

`ai.conversation` · `ai.interaction` · `ai.message`

**`qdrant`** — 1

`qdrant:knowledge`

**`redis`** — 3

`cache:answer` · `cache:embedding` · `cache:idempotency`

**Keys pointing in from other domains.** Each is a place another part of the platform depends on this one.

- `marketing.conversation_message.ai_interaction_id` → `ai.interaction`

## Screens

**P02 Guest App**

- `GST-031` AI Concierge – Home — wave 2, 1 operation
- `GST-032` AI Concierge – Chat — wave 2, 1 operation
- `GST-033` AI Concierge – Contextual Help — wave 2, 1 operation
- `GST-054` AI Optimized Itinerary — wave 3, 1 operation

**P04 Venue POS**

- `POS-008` Reports — wave 2, 2 operations

**P05 Guest Kiosk**

- `KSK-015` Assistant — wave 2, 1 operation

**P06 Venue Staff App**

- `EMP-019` AI assistant — home — wave 1, 3 operations
- `EMP-020` AI assistant — answer — wave 1, 3 operations
- `EMP-040` Knowledge base — wave 2, 1 operation
- `EMP-041` Training — wave 3, 1 operation

**P08 Venue Management**

- `BO-029` Report Builder — wave 2, 2 operations
- `BO-058` Reporting Home — wave 1, 2 operations
- `BO-059` Sales Reports — wave 1, 2 operations
- `BO-060` Attendance & Footfall — wave 2, 2 operations
- `BO-061` Scheduled Reports — wave 3, 2 operations
- `BO-068` Audit Log — wave 2, 1 operation
- `BO-091` AI Policy & Spend — wave 1, 3 operations
- `BO-093` Map Import & Labelling — wave 2, 1 operation

**P09 TICVAI Web**

- `ADM-004` Platform Audit Log — wave 2, 1 operation
- `ADM-037` AI Provider & Credentials — wave 1, 4 operations

**P10 Partner Web**

- `PTR-018` Reports & Sales Performance — wave 3, 2 operations

**P12 Venue Support**

- `SUP-008` Agent Performance & SLA View — wave 3, 2 operations

## Flows

- **F20** A manager asks a question and gets an answer — wave 1
- **F24** A guest asks the assistant and ends up with a person — wave 2
- **F26** A venue maps its site — wave 2

## Decisions and documents

| Document | Status | Mentions |
|---|---|---|
| [AI scope — for confirmation](../docs/active/ai-scope-for-confirmation.md) |  | 1 |
| [Optimisation assessment — RAG, caching, backend, frontend](../docs/active/optimisation-assessment.md) |  | 4 |
| [Optimisation adoption plan](../docs/active/optimisation-plan.md) |  | 3 |
| [ADR-0007: Hybrid repository topology](../docs/adr/0007-hybrid-repository-topology.md) | Accepted | 1 |
| [ADR-0020 — Where AI runs, and what it is isolated from](../docs/adr/0020-ai-isolation-boundary.md) | Proposed · 17 August 2026 | 14 |
| [ADR-0021 — Qdrant: one collection per embedding model, tenant is the shard, scope is the filter](../docs/adr/0021-qdrant-partitioning.md) | Proposed · 17 August 2026 | 4 |
| [ADR-0023 — Personal data lives apart from the append-only ledger](../docs/adr/0023-pii-separation.md) | Accepted · 17 August 2026, recording a decision already impl | 3 |
| [Architecture](../docs/architecture/README.md) |  | 1 |
| [AI provider credentials — where the key lives and who can reach it](../docs/architecture/ai-credentials.md) |  | 4 |

## Conflicts


32 closed — CF-41 · CF-57 · CF-139 · CF-61 · CF-74 · CF-123 · CF-120 · CF-141 · CF-144 · CF-17 · CF-119 · CF-118 · CF-113 · CF-109 · CF-107 · CF-106 · CF-105 · CF-14 · CF-96 · CF-94 · CF-92 · CF-93 · CF-90 · CF-89 · CF-88 · CF-59 · CF-80 · CF-78 · CF-76 · CF-73 · CF-20 · CF-43

