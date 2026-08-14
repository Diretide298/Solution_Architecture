# Conflict register — status index

**74 conflicts raised — CF-01 to CF-72, plus CF-33a and one screen-level item.**

Generated from `conflicts.md`, which holds the full reasoning for each. This is the
index: one line per conflict, so anything's state can be checked without reading the
register.

| State | Count |
|---|---|
| OPEN — client | **9** |
| OPEN — Softlabs | **18** |
| CLOSED | **41** |
| WITHDRAWN | **6** |
| **Total** | **74** |

**Blocking: 0.** No conflict currently prevents contract, schema or build work.
**27 open, 41 closed.**


## Open — needs a client decision — 9

| ID | Issue | Owner |
|---|---|---|
| **CF-14** | AI concierge mechanism and token billing model. How AI usage is priced to tenants, and whether the concierge meters per interaction or per token | Both — workshop |
| **CF-17** | Venue-map format and guidance standard. Which CAD or SVG conventions venues will supply, so the importer targets something real | Both |
| **CF-35** | Biometric data is sensitive under PDPL — heightened protection, explicit consent, DPIA, stricter transfer rules. Affects Face Pass, facial readers and | Allam + counsel |
| **CF-40** | Training & Knowledge Base and Employee Recognition have no provenance. Both appear in the employee app design reference and in neither the matrix nor  | Qossai / Allam |
| **CF-41** | AI is a primary navigation tab in the employee app — Home, Tasks, Scan, AI, More. AI-06 sits in Wave 2, but the app shell cannot ship without the tab  | Qossai + Chinmay |
| **CF-48** | Q2 Virtual Waiting Room. ADR-0012 separated Q1 (ride queues, contracted) from Q2 (on-sale throttling). Q2 is edge infrastructure, not a product contra | Dinesh + Qossai |
| **CF-51** | Location-aware ticket activation is not contracted. 3.1.9 requires BLE beacon validation, geofencing, and entitlements that "shall only become active  | Chinmay + Qossai |
| **CF-53** | 73 back office screens are counted and never itemised. The page inventory carries "POS · Scanner · Back office — 73" from v1 with no list behind it. S | Chinmay |
| **CF-57** | AI configuration assistance is Wave 1 and is not in the phasing paper. Qossai: "one of the most important item for the AI… it's supposed to be from be | Chinmay |

## Open — Softlabs to resolve — 18

| ID | Issue | Owner |
|---|---|---|
| **CF-18** | Dynamic bundle auto-discounting design. How a dynamic bundle prices itself when its components change | Softlabs |
| **CF-21** | Undiscussed domains — restated 14 Aug after an audit. The original entry named four domains totalling ~276 requirements and was wrong on composition.  | Chinmay — schedule three workshops |
| **CF-23** | 10 Aug §5.1 has a lost subject — "agreed this makes more sense and will be adopted" names nobody. No owner for a decision since partially reversed | Chitrangi |
| **CF-24** | 9.2% actor coverage. 292 of 3,184 requirements name a human actor. Assignment for the remaining ~91% is undetermined, which makes permission design pa | Chinmay |
| **CF-42** | RTL and dark theme are Sprint 1 scope, not a later localisation pass. Arabic RTL means every layout mirrored, not translated, and the client's own hie | Chinmay / design |
| **CF-49** | Release-management scope skipped the matrix. Thirteen Platform Admin screens raised 30 July, minuted, never written into a requirement — absent from t | Chinmay |
| **CF-59** | Two domains have no owning contract, and neither is workshop-blocked. Approval Workflows & Governance (80 reqs) is genuinely cross-cutting — refund ap | Chinmay |
| **CF-60** | 113 requirements on three matrix sheets have never been counted. Every figure quoted since 30 July — 3,184 across 21 domains — is the Functionality sh | Chinmay |
| **CF-61** | On-premise deployment was never designed for. Settled 14 Aug as the third client-facing model: the platform on the venue's own hardware, nothing leavi | Chinmay + Qossai |
| **CF-62** | `createReservation` had been silently absent from the contracts. `/reservations` was declared twice in `orders.yaml`; YAML keeps the last block and dr | Chinmay |
| **CF-64** | 89 retention requirements, two stated periods. Only 4.3.4 (10 years, payment) and 6.1.78 (7 years) name a number. Combined with CF-60's 62 undesigned  | Dinesh + Qossai |
| **CF-65** | 52 reports are named by title and nothing lists them. 347 requirements mention reporting; the matrix names specific reports — Deferred Revenue, Commis | Chinmay |
| **CF-67** | Virtual and hybrid events appear once and nowhere else. 1.3.30 requires "physical, virtual and hybrid events with configurable attendance rules and ac | Qossai |
| **CF-68** | The contracts have no concept of a payment provider. Two gateways are named in the integrations sheet — Stripe and Network International — and there i | Chinmay |
| **CF-69** | Four named integrations have no trace in any contract. DET and DCT — the Dubai and Abu Dhabi tourism authorities — are almost certainly mandatory visi | Qossai + Allam |
| **CF-70** | Three Postgres enums disagreed with their contract counterparts. `platform.device_kind` held nine values the API did not and the API six the database  | Chinmay |
| **CF-71** | A task has no contract, and the employee app is fifty screens built around them. `listTasks`, `updateTask` and `createHandoverNote` appear in none of  | Chinmay |
| **CF-72** | Twelve more lifecycle operations were missing, found the same way as CF-66. Writing the remaining eighteen state models exposed `rejectRequisition`, ` | Chinmay |

## Closed — 41

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
| **CF-15** | Online-first vs offline-first POS catalogue |  |
| **CF-16** | Reference manual undelivered |  |
| **CF-19** | KDS scope |  |
| **CF-20** | AI data residency |  |
| **CF-22** | Accreditation vs entitlement |  |
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
| **CF-43** | AI governance has no screens |  |
| **CF-44** | Conversational coverage 3 of 8 |  |
| **CF-45** | Two Phase 1 screens require operating history |  |
| **CF-46** | 3,185 / 22 domains vs 3,184 / 21 |  |
| **CF-47** | ~102 screens absent from the page inventory |  |
| **CF-50** | Guest self-ordering had no contract. `diningAndFnb` is a module a tenant can switch on in the guest app, and nothing was reachable behind it — `listOu | Chinmay |
| **CF-52** | Parking scope |  |
| **CF-54** | The `pii` schema was declared and empty. V0001 created the schema, the V0001 rollback dropped two tables in it, and four foreign keys in V0003b refere | Chinmay |
| **CF-55** | Four POS operations existed in the delivered design and in no contract. The Park POS mockups show Hold Order, Discount, Add Tip and a cash drawer, non | Chinmay |
| **CF-56** | ADR-0014 contradicted by the shared-tenant hosting model. 14 Aug confirmed two models: dedicated infrastructure per tenant, and a shared TICVAI databa |  |
| **CF-58** | Entitlements could not be appended to an existing ticket |  |
| **CF-63** | 263 of 273 "configurable" requirements did not say at what level |  |
| **CF-66** | Seventeen enum values existed that nothing could reach. Writing state models for twenty entities found that the contracts could start and finish thing | Chinmay |
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

- **Numbering:** CF-01 to CF-72, no gaps
- **Duplicates:** none
- **Counts** are generated from the rows, so this file and the register's summary
  cannot disagree. Regenerate with `tools/build-cf-index.py` after editing.

