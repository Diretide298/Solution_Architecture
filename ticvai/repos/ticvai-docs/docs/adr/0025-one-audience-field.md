# ADR-0025 — One field says who may call an operation

**Status:** Accepted · 18 August 2026
**Supersedes:** `x-ticvai-guest-callable` and `x-ticvai-auth`, both removed
**Relates to:** ADR-0002 (authorisation follows the user), CF-106

---

## Context

Two markers answered the same question differently and neither said so.

`x-ticvai-auth` carried a single value — `guest`, `anonymous`, `session`, `device`, `service` — on
46 operations. `x-ticvai-guest-callable` was a boolean on 59. **Three operations carried both, and
nothing anywhere stated the difference**, so each was applied by whoever touched the file last.

**The cost was not confusion, it was a wrong answer.** `check-screens` treated the accreditation
portal as a guest surface because there was no value for what it actually is, and
`decideApprovalRequest` was marked guest-callable to satisfy the guard — **a marking that reads as
a guest approving their own refund.**

And a viewer cannot build a guest mode against two vocabularies. That is what forced the decision:
**a filter needs one field, and the package could not supply one.**

---

## Decision

**`x-ticvai-audience`, a list, on every operation. Both old markers removed.**

    x-ticvai-audience: [staff]              652 — the default
    x-ticvai-audience: [staff, guest]        49 — a staff operation a guest may also call
    x-ticvai-audience: [guest]               46 — guest-only, no permission exists
    x-ticvai-audience: [staff, partner]     105 — partner-web
    x-ticvai-audience: [service]             12
    x-ticvai-audience: [anonymous]           10
    x-ticvai-audience: [device]               7
    x-ticvai-audience: [staff, public]        3 — an external accreditation reviewer

**A list rather than a scalar, because the answer genuinely is plural.** `cancelReservation` is
called by staff cancelling anyone's and by a guest cancelling their own — the same operation, two
audiences, and a scalar forces one of them to be a lie.

**Audience and permission are orthogonal and both stay.** Audience says who may call; permission
says what a staff caller must hold. An operation with `[staff, guest]` keeps its permission for
the staff case and resolves to the caller's own data for a guest.

### The two values that did not exist

**`partner`** — 105 operations reached by `partner-web`. A partner books on credit and settles
against an agreement; they are not employees of the venue.

**`public`** — an accreditation reviewer holds `APPROVAL_DECIDE` and signs in from outside the
organisation. **Neither staff nor guest, and the absence of this value is what produced the
misclassification.** Three operations, and the number being small is the point: it was invisible
precisely because it was rare.

### What `session` became

`session` meant *authenticated with no specific permission* — ten operations, all of them staff.
It described a mechanism rather than an audience and folded into `staff`.

---

## Consequences

**A viewer can filter in one lookup.** `handoff/audience-index.json` is derived from this field and
carries, per audience, the operations, screens, flows, contracts and tables it reaches.

**Guest mode is 96 operations, 111 screens, 9 flows and 95 tables** — against 776, 376, 24 and
287. Somebody reviewing the guest experience sees a twelfth of the package, and none of what they
see is irrelevant to them.

**Platform decides which screens count, not the operation.** An operation marked `[staff, guest]`
appears on a back-office screen and a guest-app screen; only the second belongs in guest mode, and
the platform's own `operator` field says which is which. **Filtering screens by operation audience
alone would put the back office in guest mode.**

**The closed set is enforced.** `check-package.py` validates every value, and it catches a list
member the way it catches a scalar — which it did not until this change, because `x-ticvai-audience`
was the first list-valued marker.

**One field can still be wrong; two could disagree.** That is the whole gain. A missing audience is
a visible gap; two markers that contradicted each other looked complete from either side.
