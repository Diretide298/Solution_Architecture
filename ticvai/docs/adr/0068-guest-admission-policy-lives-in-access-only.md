# ADR-0068: Guest admission policy lives in Access only, and the offline package carries it

**Status:** Accepted · 1 October 2026 · Chinmay Parab
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-005 (medium), with SD-052
**Related:** ADR-0002 (authorisation is user-driven) · ADR-0013 (local-first) · ADR-0055 (modules and deployables)

---

## Context

**Two tables are called "access policy" and they decide different things.**

| | `identity.access_policy` (`010-identity.sql:37`) | `access.dynamic_policy` (`010-access.sql:753`) |
|---|---|---|
| Owner | Identity: `createAccessPolicy`, `simulateAccessPolicy`, `getAccessPolicyBundle` (`identity.yaml`) | Access: `setVisualDynamicPolicy`, `rollbackAccessPolicy` (`access.yaml`) |
| Shape | `permissions text[]`, `applies_to_role_ids`, `effect` permit/deny, `combining` | `policy_type` (guest attribute, accreditation, occupancy, membership, time event …), `condition_expression`, `result` (allow, deny, review, require ID, require biometric …) |
| What it really is | **Staff authorisation** | **Guest admission at the gate** |

**Offline and online decisions can differ.** Per lineage, `getOfflinePackage` (`access.yaml`)
reads **neither** policy table, and it also omits `access.entitlement` (SD-052). The gate decides
offline without the rules the cloud uses online.

**`getOfflinePackage` is in the Block A slice**, used by POS (POS-013) and by scanner and staff
screens (SCN-003 … SCN-015, EMP-010 …). What the package carries is fixed when its ticket is built.

**`condition_expression` is free text.** A rule written as free text cannot be evaluated the same way
on a .NET server and a TypeScript device without a shared language.

**The two owners now run in different deployables** (ADR-0055): Identity in `commerce`, Access in
`access`, which also builds the venue edge node. Guest admission belongs with the unit that decides at
the gate.

---

## Decision

- **Guest admission rules live in Access only**: `access.dynamic_policy` and its versions. `validateAccess` online and the gate offline evaluate **the same active version**.
- **`getOfflinePackage` carries the active policy version** (and the entitlements, SD-052). Each `scan_event` records the policy version that decided it.
- **Identity keeps staff authorisation only.** Rename `identity.access_policy` to `identity.authorisation_policy` (and its version table likewise), and its operations (`createAuthorisationPolicy`, `simulateAuthorisationPolicy`, `getAuthorisationPolicyBundle`). "Access policy" then means one thing.
- **One rule format that runs on both sides.** Replace free-text `condition_expression` with a closed JSON rule format (conditions drawn from the `policy_type` and `context_type` enums already in the table). One evaluator in .NET and one in TypeScript, **proven equal by a shared set of test vectors** in CI.

---

## Options Considered

### Option A: Keep two engines (status quo)

| Dimension | Assessment |
|---|---|
| Complexity | Medium, forever |
| Cost | Two editors, two simulators |
| Scalability | Fine |
| Team familiarity | High |
| Time to Block A | None |

**Pros:** No change. **Cons:** Two rule sets can disagree at the gate; the offline package carries neither.

### Option B: Guest admission in Access, staff authorisation in Identity, one portable rule format (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Medium. A rename, a contract move, two small evaluators |
| Cost | About 8 points of evaluator work in B1 |
| Scalability | The gate decides locally from the package, as ADR-0013 intends |
| Team familiarity | High |
| Time to Block A | The package contents are decided before POS-013; the evaluator lands with the scanner in B1 |

**Pros:** Offline and online decide the same way, and the scan records why. **Cons:** Two evaluators to keep equal (the test vectors do that).

### Option C: One generic policy engine in Identity for staff and guests

| Dimension | Assessment |
|---|---|
| Complexity | High. One engine for two very different questions |
| Cost | Moves Access's rules |
| Scalability | The gate would depend on Identity's engine |
| Team familiarity | Medium |
| Time to Block A | Slower |

**Pros:** One engine. **Cons:** Couples the gate to Identity, in another deployable; staff permissions and guest admission are different questions with different results.

---

## Trade-off Analysis

The two tables answer different questions: *may this staff member do this?* and *may this guest go
through this gate now?* B names them apart and gives each one owner. The real risk the finding
raises, offline and online disagreeing, is closed by carrying the version in the package and by one
rule format proven equal on both sides.

---

## Consequences

**Easier:** one admission editor; a scan can be explained by its policy version.
**Harder:** a rename across Identity's contract and screens; a second evaluator in TypeScript.
**Revisit:** if rules need more than the closed set, extend the set; do not reopen free text.

---

## Action Items

**Before the `getOfflinePackage` ticket (POS-013) is cut**

1. [x] Chinmay: accepted 1 October 2026.
2. [ ] Package: package contents (active policy version, entitlements); `scan_event.policy_version`; rename Identity's policy tables and operations; JSON rule schema replacing `condition_expression`. Renames need the vocabulary and naming checks, and a declared rename in the schema history. Re-derive, mirrors, check. (5 pts, the finding's estimate) — **Authored 1 October**: `identity.authorisation_policy` and `identity.authorisation_policy_version` (declared renames), eleven `*AuthorisationPolicy*` operations on `/authorisation-*`, four schemas; `OfflinePackage.policySetVersion` and `ScanEvent.policySetVersion` beside the existing `dynamicPolicyId`/`dynamicPolicyVersion`; `conditionRule` (`AdmissionRule`, `AdmissionCondition`) replaces `conditionExpression` on the policy and its builder shapes. Re-derive, mirrors and check at the next refresh.

**B1, with the scanner**

3. [ ] **ACC-RULE-EVAL**: evaluators in .NET and TypeScript with shared test vectors. (8 pts)
