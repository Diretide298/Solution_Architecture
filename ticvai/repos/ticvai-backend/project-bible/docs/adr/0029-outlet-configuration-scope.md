# ADR-0029: Outlet configuration is outlet-scoped, and the path is the evidence

**Status:** Accepted
**Date:** 24 August 2026
**Supersedes:** the 14 August client correction recorded in `configuration-scope-decision.md`
**Related:** [ADR-0018](0018-configuration-scope.md), amended 18 August to add `outlet` · [ADR-0011](0011-hierarchy-is-binding.md), amended 18 August from seven levels to eight · CF-138

---

## Extended 2 October 2026: the outlet settings decided on the open questions

**Decided by Chinmay, 2 October 2026** (change entry CHG-DOC-010; each decision is in
`docs/registers/decisions-2-october.md`). Each of these is a property or setting **of the outlet**, so it
resolves at `outlet` (ADR-0018: nearest ancestor wins, outlet a sibling of department), and an operation on
`/outlets/{outletId}/…` that sets it carries the `outlet` scope, which `check-config-scope` enforces.

| Outlet setting | What it decides | Decision |
|---|---|---|
| **Payment timing** | *Pay first*, or *Send to kitchen first, then pay*. Amends audit R261 (send first, then charge, everywhere) into a per-outlet choice | DEC-064 |
| **Inside the venue or standalone** | An outlet inside the venue sells to guests who hold an admission ticket; a standalone restaurant sells takeaway and delivery without one. Amends DI-292 for standalone outlets; the admission check itself stays in Access (ADR-0068) | DEC-070, DEC-206 |
| **Outlet type and department** | Two fields on the outlet (DI-319) | DEC-196 |
| **Till layout** | Set per outlet; a till may override it. The override is an assignment (`Workstation.saleBoard`), not a configuration level: ADR-0018's "below venue you assign, you do not configure" | DEC-183 |
| **Producing outlet** | A commissary is an outlet that produces for others, and one kitchen outlet can produce for several outlets | DEC-186, DEC-188 |
| **Default kitchen station** | An item with no station goes to the outlet's named default station, after item and category routing (DI-323) | DEC-189, DEC-190 |

The contract fields and operations are the contracts' owners' to add; this ADR fixes where they resolve.

---

## Context

**Two client decisions point in opposite directions and no ADR arbitrated between them.**

On **14 August** the client corrected F&B configuration to `venue`. On **18 August** CF-138 moved it
to `outlet`, and **ADR-0018 was amended** to add `outlet` as an eighth scope level — **amending ADR-0011**,
which had made seven levels binding — a sibling of `department`, not a
child of it.

**The F&B drop followed the superseded decision.** Five operations arrived tagged `venue`:

| Operation | Path | Tagged |
|---|---|---|
| `setKitchenSla` | `/outlets/{outletId}/kitchen-sla` | venue |
| `setSectionLayout` | `/outlets/{outletId}/sections` | venue |
| `setTableCombinations` | `/outlets/{outletId}/table-combinations` | venue |
| `setCourseRules` | `/outlets/{outletId}/course-rules` | venue |
| `setSubstitutionRules` | `/substitution-rules` | venue |

**`setSectionLayout` sits beside `setTableLayout` on the same resource with the opposite scope.**
One says `outlet` and cites CF-138; the other says `venue`.

---

## Decision

**A path that names an outlet configures at that outlet.** The four operations on
`/outlets/{outletId}/…` are retagged `outlet`. `setSubstitutionRules` stays `venue` — its path names
no outlet, and a substitution rule is a venue-wide procurement policy rather than a menu decision.

**If a path names an outlet and the scope says otherwise, the outlet in the path is decoration.**
That is now a check rather than a convention.

---

## Why the checker did not catch it

**Two independent gaps, and each alone would have been enough.**

**`venue` is unconditionally valid.** `check-config-scope` validated the scope *value* against a
list and never read the *path*. The one piece of evidence that could have caught the conflict went
unexamined.

**Two of the five were never examined at all.** `setKitchenSla` and `setTableCombinations` did not
match `IS_CONFIG`, a keyword whitelist — so the checker skipped them before reaching the scope. **A
silent exemption is worse than a missing check, because nothing reports it.**

Both are now closed:

- A path containing `{outletId}` with a non-`outlet` scope is an error.
- **An operation carrying a config scope that the naming rules do not reach is an error.** That
  found 24 more, including `createMenu` and `updateMenu` — the two cited in review as correctly
  scoped, whose tags had never actually been read.

---

## What widening the vocabulary taught

**The first widening was wrong and I shipped it for about ten minutes.** Adding `Campaign`,
`Collection`, `Category` and `Resource` pulled in ten operations that author content: a marketing
campaign is a thing a venue *makes*, not a setting it *holds*.

**Then I dropped `create` from the verb list and made it worse** — 22 operations that legitimately
carry a scope stopped being examined, including `createMenu` and `createAdmissionRules`.
**Reverted.**

**The noun is the discriminator, not the verb.** `createResource`, `createVenueMap` and
`createDonationCampaign` are exempted by name because they author records that resolve *against*
configuration rather than being it.

---

## Consequences

**Four operations move from venue to outlet.** No contract path changes, no operation is renamed,
and nothing downstream shifts — the tag was wrong and the path was always right.

**Nine operations now resolve at outlet**, up from five: menu creation, updates, sections,
publishing, scheduling, table layout, table combinations, kitchen SLA, course rules, return policy.

**`hld/01-hierarchy.yaml` already said this** — *"only outlet, and only F&B and retail resolve
against it"* — and the contracts disagreed with it for six days.

---

## Alternatives considered

**Follow the 14 August correction and retag everything to venue.** It would make the file internally
consistent and it contradicts CF-138, ADR-0018 and the hierarchy diagram. **The later decision
governs, and it is the one with an amended ADR behind it** — ADR-0011 and ADR-0018 were both amended on
18 August to carry it.

**Leave both and let each operation declare its own level.** Defensible for a genuinely mixed
domain, and this is not one: a kitchen SLA and a section layout belong to the same outlet as the
menu they serve. **Two scopes on one resource is a resolution nobody can predict.**
