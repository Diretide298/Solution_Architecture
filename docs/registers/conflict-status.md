# Conflict register — status index

**113 conflicts raised — CF-01 to CF-110, plus CF-33a and one screen-level item.**

Generated from `conflicts.md`, which holds the full reasoning for each. This is the
index: one line per conflict, so anything's state can be checked without reading the
register.

| State | Count |
|---|---|
| OPEN — client | **17** |
| OPEN — Softlabs | **1** |
| CLOSED | **89** |
| WITHDRAWN | **6** |
| **Total** | **113** |

**Blocking: 0.** No conflict currently prevents contract, schema or build work.
**18 open, 89 closed.**


## Open — needs a client decision — 17

| ID | Issue | Owner |
|---|---|---|
| **CF-17** | Venue-map format and guidance standard. Which CAD or SVG conventions venues will supply, so the importer targets something real | Both |
| **CF-35** | Biometric data is sensitive under PDPL — heightened protection, explicit consent, DPIA, stricter transfer rules. Affects Face Pass, facial readers and | Allam + counsel |
| **CF-40** | Training & Knowledge Base and Employee Recognition have no provenance. Both appear in the employee app design reference and in neither the matrix nor  | Qossai / Allam |
| **CF-41** | AI is a primary navigation tab in the employee app — Home, Tasks, Scan, AI, More. AI-06 sits in Wave 2, but the app shell cannot ship without the tab  | Qossai + Chinmay |
| **CF-48** | Q2 Virtual Waiting Room. ADR-0012 separated Q1 (ride queues, contracted) from Q2 (on-sale throttling). Q2 is edge infrastructure, not a product contra | Dinesh + Qossai |
| **CF-51** | Location-aware ticket activation is not contracted. 3.1.9 requires BLE beacon validation, geofencing, and entitlements that "shall only become active  | Chinmay + Qossai |
| **CF-57** | AI configuration assistance is Wave 1 and is not in the phasing paper. Qossai: "one of the most important item for the AI… it's supposed to be from be | Chinmay |
| **CF-61** | On-premise deployment was never designed for. Settled 14 Aug as the third client-facing model: the platform on the venue's own hardware, nothing leavi | Chinmay + Qossai |
| **CF-64** | 89 retention requirements, two stated periods — and RPO/RTO is a narrower question than it looked. Only 4.3.4 (10 years, payment) and 6.1.78 (7 years) | Dinesh + Qossai |
| **CF-67** | Virtual and hybrid events appear once and nowhere else. 1.3.30 requires "physical, virtual and hybrid events with configurable attendance rules and ac | Qossai |
| **CF-69** | Four named integrations have no trace in any contract. DET and DCT — the Dubai and Abu Dhabi tourism authorities — are almost certainly mandatory visi | Qossai + Allam |
| **CF-74** | "AI Configuration Assistant" is two unrelated things, and six ids exist twice. 8.1.1–8.1.6 are no-show revenue recognition and complimentary/invitatio | Chinmay — raise with Qossai |
| **CF-83** | Abandoned-cart recovery may not be lawful as specified, and I built it without asking. 22.3.6 and 2.6.45 require identifying incomplete purchases and  | Allam + counsel |
| **CF-84** | Donation VAT treatment is unstated and it is a tax question. 1.1.128–1.1.133 require donation collection through all POS channels. I posted donations  | Qossai + finance |
| **CF-85** | Four holding windows were set by me as defaults and all four are commercial decisions. Cart expiry and extension cap — how long a guest holds capacity | Qossai + Allam |
| **CF-97** | A superseded ADR was cited as current, and nothing in the package could have stopped it. ADR-0021 reasoned from ADR-0001's *"Cell = Tenant × Jurisdict | Chinmay + Dinesh |
| **CF-100** | Agent hours for the conversation queue are unstated, and the handover depends on them. Raised 17 August when CF-99 was closed. 22.8.5 requires seamles | Qossai + Allam |

## Open — Softlabs to resolve — 1

| ID | Issue | Owner |
|---|---|---|
| **CF-21** | Three domains have no contract and no workshop scheduled — Developer & API (94), Device Management (60), Accreditation (58). 212 requirements, and the | Chinmay — schedule |

## Closed — 89

| ID | Issue | Owner |
|---|---|---|
| **CF-01** | Multi-role login contradiction |  |
| **CF-02** | Session concurrency | Client — single session only |
| **CF-03** | Role vs workstation authorisation |  |
| **CF-04** | Front-gate scanning surface |  |
| **CF-05** | Four competing role taxonomies |  |
| **CF-07** | Refund authorisation |  |
| **CF-08** | Flying POS |  |
| **CF-09** | Kiosk operator model |  |
| **CF-10** | Till handover on breaks |  |
| **CF-11** | Approval model depth |  |
| **CF-12** | Universal Cashier landing screen |  |
| **CF-13** | Guest app publishing | Client — Option C, tiered |
| **CF-14** | Guest concierge in Phase 1, charged per token, capped as a warning rather than a stop — decided by Chinmay, 17 August. Closed. Three decisions and eac |  |
| **CF-15** | Online-first vs offline-first POS catalogue |  |
| **CF-16** | Reference manual undelivered |  |
| **CF-18** | Dynamic bundle auto-discounting design. Closed 17 August — ADR-0019, and the gap was two things wearing one name. The contract could not express a dyn |  |
| **CF-19** | KDS scope |  |
| **CF-20** | AI data residency |  |
| **CF-22** | Accreditation vs entitlement |  |
| **CF-23** | 10 Aug §5.1 has a lost subject — "agreed this makes more sense and will be adopted" names nobody. Closed 17 August: the missing name no longer matters |  |
| **CF-24** | 9.2% actor coverage — 292 of 3,184 requirements name a human actor. Closed 17 August, and the measure was wrong. Actor coverage in requirement *text*  |  |
| **CF-25** | Party inversion in the 12 Aug MoM | Client correcting the record | |
| **CF-31** | Do entitlements cross jurisdictions? |  |
| **CF-32** | Hyperscaler presence in the second jurisdiction |  |
| **CF-33** | Queue management ownership |  |
| **CF-33a** | Queue vendor selection |  |
| **CF-34** | Is the hierarchy binding or illustrative? |  |
| **CF-36** | `ORDER_REFUND_APPROVE` threshold |  |
| **CF-37** | FX policy for cross-region revenue splits |  |
| **CF-38** | Price variance on re-pricing |  |
| **CF-39** | White Label Builder had no owning context |  |
| **CF-42** | RTL and dark theme are Sprint 1 scope, not a later localisation pass. Closed 17 August with a specification rather than a restatement — `docs/architec |  |
| **CF-43** | AI governance has no screens |  |
| **CF-44** | Conversational coverage 3 of 8 |  |
| **CF-45** | Two Phase 1 screens require operating history |  |
| **CF-46** | 3,185 / 22 domains vs 3,184 / 21 |  |
| **CF-47** | ~102 screens absent from the page inventory |  |
| **CF-49** | Release-management scope skipped the matrix. Thirteen Platform Admin screens raised 30 July, minuted, contracted as `platform-ops`, never written as a |  |
| **CF-50** | Guest self-ordering had no contract. `diningAndFnb` is a module a tenant can switch on in the guest app, and nothing was reachable behind it — `listOu | Chinmay |
| **CF-52** | Parking scope |  |
| **CF-53** | 73 back office screens are counted and never itemised. The page inventory carries "POS · Scanner · Back office — 73" from v1 with no list behind it. S | Chinmay |
| **CF-54** | The `pii` schema was declared and empty. V0001 created the schema, the V0001 rollback dropped two tables in it, and four foreign keys in V0003b refere | Chinmay |
| **CF-55** | Four POS operations existed in the delivered design and in no contract. The Park POS mockups show Hold Order, Discount, Add Tip and a cash drawer, non | Chinmay |
| **CF-56** | ADR-0014 contradicted by the shared-tenant hosting model. 14 Aug confirmed two models: dedicated infrastructure per tenant, and a shared TICVAI databa |  |
| **CF-58** | Entitlements could not be appended to an existing ticket |  |
| **CF-59** | Two domains had no owning contract, and neither was workshop-blocked. Approval Workflows & Governance (80 reqs) and Employee Mobile App & AI Assistant |  |
| **CF-59a** | Approval Workflows — 80 requirements, no contract, implemented four times. Refund thresholds, shift variance, release promotion and manual discount ea | Chinmay |
| **CF-60** | 113 requirements on three matrix sheets had never been counted. Every figure quoted since 30 July was the Functionality sheet alone. Counted 17 August |  |
| **CF-62** | `createReservation` had been silently absent from the contracts. `/reservations` was declared twice in `orders.yaml`; YAML keeps the last block and dr | Chinmay |
| **CF-63** | 263 of 273 "configurable" requirements did not say at what level |  |
| **CF-65** | 52 reports named by title and nothing listed them. Closed 17 August, and counting properly found 133 rather than 52 — plus a split that matters more t |  |
| **CF-66** | Seventeen enum values existed that nothing could reach. Writing state models for twenty entities found that the contracts could start and finish thing | Chinmay |
| **CF-68** | The contracts have no concept of a payment provider. Two gateways are named in the integrations sheet — Stripe and Network International — and there i | Chinmay |
| **CF-70** | Three Postgres enums disagreed with their contract counterparts. `platform.device_kind` held nine values the API did not and the API six the database  | Chinmay |
| **CF-71** | A task has no contract, and the employee app is fifty screens built around them. Closed 17 August, and the premise was half wrong. Reading all fifty r |  |
| **CF-72** | Twelve more lifecycle operations were missing, found the same way as CF-66. Writing the remaining eighteen state models exposed `rejectRequisition`, ` | Chinmay |
| **CF-73** | 288 AI requirements had no contract, and the reqs-per-operation ratio hid it. The matrix files the entire AI platform under "Unified Operations Dashbo | Chinmay |
| **CF-75** | The lineage read 51% because the deriver gave up at six levels of nesting. A paged response nests nine before its item ref — `responses → 200 → conten | Chinmay |
| **CF-76** | Seven domain events are needed for RAG indexing and none exists. `whitelabel.contentPublished`, `fnb.menuPublished`, `retail.merchandisePublished`, `m |  |
| **CF-77** | Package audit, 17 August — five defects across artefacts that each validated cleanly on their own. (1) `permissions.yaml` existed three times — `share | Chinmay |
| **CF-78** | `askReportingQuestion` is an AI capability outside the AI governance boundary. Reporting's natural-language query calls a model, and wrote no `ai.inte | Chinmay |
| **CF-79** | The register drifted from its own rows a second time |  |
| **CF-80** | Table reference audit — one duplicate and 59 unlinked tables. `whitelabel.faq` was added by hand for the RAG source list and duplicated `whitelabel.fa |  |
| **CF-81** | There was no cart, and nine requirements needed one. `createOrder` takes a whole basket at once — correct for a till, which builds locally and submits |  |
| **CF-82** | Three more concepts the matrix names and the contracts did not. Found by sweeping every repeated noun in the matrix against the operation and schema v |  |
| **CF-86** | Two commercial surfaces had screens and no contract behind them. Partner agreements: `getB2bCredit`, `setB2bCreditLimit`, `getChannelAllocations` and  |  |
| **CF-87** | A warning I chose to leave was hiding two defects. `check-states` reported that `states/entitlement.yaml` referenced `access.TicketStatus`, which does |  |
| **CF-88** | The state checker had a blind spot covering 31 lifecycles. It collected enums declared as named schemas — `OrderStatus`, `WorkOrderStatus` — and never | Chinmay |
| **CF-89** | ADR-0009 answered whether AI data may leave the country and never where the AI service runs. Raised by a question about folders that turned out to be  | Chinmay + Dinesh |
| **CF-90** | AI had four lifecycles and no state model, found by asking whether it needed a folder. It does not — the package is organised by artefact kind — but t |  |
| **CF-91** | Multi-currency was built on the app and the matrix asks for it on the website. 2.6.33 and 2.9.1 both name the website; neither names the app. Closed 1 |  |
| **CF-92** | Eight guest-app screens had no requirement behind them. Closed 17 Aug, and it was my error: I searched the matrix and never the minutes. Seven of the  |  |
| **CF-93** | Guest web and guest app had drifted apart and nobody decided they should. Closed 17 Aug: nine screens added, two operations written, fourteen marked g |  |
| **CF-94** | Two AI isolation breaches, both invisible to every checker. `generateVenueLayout` wrote directly into `seating.import_job` — AI writing into a transac | Chinmay |
| **CF-95** | Qdrant collection-per-tenant was wrong twice, and both were visible without new information. The rule *"tenant isolation is partition-level, never fil | Chinmay + Dinesh |
| **CF-96** | Full recheck of screens, flows, states, events and contracts — five gaps no validator was looking for. All seven passed throughout. (1) The guest-perm |  |
| **CF-98** | An orphan sweep across tables, permissions, events and schemas found four gaps no checker looks for. (1) Deposit boxes are nine requirements (5.8.1–5. | Chinmay |
| **CF-99** | 22.8.5 live-agent handover — closed 17 August, and it was 26 requirements rather than one. Domain 22.8 is a whole omnichannel conversation platform: i |  |
| **CF-101** | Eight flows stepped through screens from a later wave, and nothing checked it. Found 17 August while establishing that CF-100 was not a blocker. Corre |  |
| **CF-102** | RAG optimisation: the contract shape that must exist before anything is indexed — landed 17 August, and one claim retracted. Seven of fourteen techniq | Chinmay |
| **CF-103** | The rest of the optimisation work — landed 17 August, and two of my own defects with it. `cache:resolution` and `cache:idempotency` were declared as s | Chinmay |
| **CF-104** | Full audit of contracts, spine, API, data, screens, journeys and derived artefacts — three findings, and the largest was a schema nobody defined. `Sal | Chinmay |
| **CF-105** | External audit of the package found 21 contradictions; the six that mattered are closed, and five were mine from the same day. The worst was silent: s | Chinmay |
| **CF-106** | The remaining 15 of the external audit's 21 contradictions — all closed, and four were losing data silently. Four duplicate YAML keys, where the loade | Chinmay |
| **CF-107** | The archive unpacked as `ticvai-full/` beside the tree instead of into it, and the package was not self-contained. Two problems from the same cause. E | Chinmay |
| **CF-108** | Two vocabularies for who may call an operation, collapsed into one — a decision rather than a patch, forced by the viewer's guest mode. `x-ticvai-auth | Chinmay |
| **CF-109** | Vector store separation audited end to end, and the AI page now shows what AI is walled off from rather than only what it is. The separation holds at  | Chinmay |
| **CF-110** | Step-by-step check of screens, APIs and the workbook — one real gap: the vector store and the four caches were in the workbook with no fields. They ap | Chinmay |
| **P08-047** | Channel-based offline inventory pooling — "design not yet agreed" (2 Aug) |  |

## Withdrawn or absorbed — 6

| ID | Issue | Owner |
|---|---|---|
| **CF-06** | `User` vs `StaffResource` |  |
| **CF-26** | SOAP / ISAPI incompatibility |  |
| **CF-27** | Hierarchy depth vs reference model |  |
| **CF-28** | One user, two workstations |  |
| **CF-29** | Reference modules absent from the matrix |  |
| **CF-30** | Integration surface 3× the matrix |  |

---

## Integrity

- **Numbering:** CF-01 to CF-110, no gaps
- **Duplicates:** none
- **Counts** are generated from the rows, so this file and the register's summary
  cannot disagree. Regenerate with `tools/build-cf-index.py` after editing.

