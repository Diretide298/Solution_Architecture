# The Context Loop

> **Purpose:** Eight stages, repeated per bounded context  
> **Owner:** Chinmay  
> **Status:** Settled


**Per context: capabilities → contract → *(schema ∥ pages ∥ mock)* → build → harden.**

The contract sits between capability and implementation because it is the only artefact all three streams read. Schema and pages both derive from it, and derive **simultaneously** rather than sequentially.

8–12 weeks per context. Three streams concurrent from week 3.

| Stage | Duration | Output | Owner | Exit |
|---|---|---|---|---|
| **0. Capability scope** | 2–3 days | C-IDs + Requirement IDs from the register; explicit in/out list | Chinmay | Every requirement assigned to a capability or explicitly deferred |
| **1. Boundary + glossary** | 2–3 days | Context boundary, entities owned vs referenced, glossary terms | Chinmay + Dinesh | Dinesh signs off — these are service boundaries in his HLD |
| **2. Resource model** | 3–5 days | Nouns, relationships, aggregate roots. **Not endpoints yet** | Chinmay | Aggregates identified; transactional boundaries explicit |
| **3. Contract draft** | 1 week | OpenAPI + event schemas + error codes + permission enum | Chinmay | **Gate 1** |
| **4a. Schema + DDL** | 2 weeks | ERD, DDL, partitioning, indexes, RLS, migration | Backend | Migration runs and rolls back on a canary cell |
| **4b. Pages** | 2 weeks | Page inventory → capabilities → endpoints; screens built on mock | Frontend | **Gate 2** |
| **4c. AI capability** | 2 weeks | Retrieval scope, eval golden set | AI | Eval baseline exists |
| **5. Implementation** | 3–4 weeks | Backend behind the frozen contract | Backend | Contract tests pass both directions |
| **6. Vertical slice** | 1–2 weeks | Thinnest end-to-end path through this context | All | Runs against the reference fixture |
| **7. Harden** | 1 week | Load, offline, permission matrix, negative paths | All | Context closed; contract → v1.0 |

**4a, 4b and 4c run in parallel.** That is the entire point — frontend is not blocked on schema, AI is not blocked on backend, backend is not blocked on design.

## Contract authoring runs one context ahead

Chinmay drafts context N+1 while N is being implemented. This keeps the pipeline full — and is the single-point-of-failure worth naming: if the contract owner is unavailable, three streams stall within a week. **A second author should be trained by context 3.**

## Each context gets its own slice

Not one slice for the project. One per context, proving that context end to end before moving on.

## Once frozen, frozen

After Gate 2 a contract is frozen for the context. A satellite needing a spine change raises a **formal change request with review**, never an inline edit. This rule is what bounds rework to one context — the entire premise of the approach.

## Why not the alternatives

| Approach | Parallelism | Rework risk | Verdict |
|---|---|---|---|
| Global schema → pages → API | 1 stream | Schema frozen before coverage is complete | Rejected |
| Global API → schema → pages | 3 streams | 3,184 requirements of contract before running code | Rejected |
| Pages-first | 1 stream | Page inventory unstable while capabilities are undefined | Rejected |
| **Per-context: contract → schema ∥ pages → build** | **3** | **Bounded to one context** | **Recommended** |

Schema-first is right *within* a context. The error is doing it globally and deferring the contract to third place.
