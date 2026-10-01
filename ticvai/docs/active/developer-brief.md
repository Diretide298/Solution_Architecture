# How you get your work, and how change reaches you

> **For:** every TICVAI developer, from Monday 5 October 2026. **From:** Chinmay. One page; read it before your first `/ticket`.

## Where things live
- **OpenProject holds who, when and order.** Your board, your assignee, your Block A week, the build order (Priority_No.) and the status you move the ticket through.
- **ADAM holds what: the spec.** The contract, the tables, the screen and its states come from the package, served by ADAM at a **release**: `r1`, `r2`, and so on. A ticket's text in OpenProject is only a pointer (from `r1`) or an old snapshot. **Never build from the OpenProject text. Build from `/ticket`.**

## Your day
1. `/board` shows your open tickets in build order: started work first, then the order to work in.
2. `/ticket <id>` pulls one ticket at the current release. ADAM **records the release you pulled at** (your pin).
3. Build against what `/ticket` gives you. If you can't finish the ticket in one go, pull it again the next day; you stay on your pin.

## When the spec changes under you
Releases go out on **Tuesday and Friday**. If something your ticket touches changed, the next `/ticket` says **"Spec changed since you pulled at r1 (now r2)"**, and shows what changed.
- **Accept:** re-pin to the new release and build to it.
- **Or raise a CR** if it doesn't fit, with the reason.
- **A breaking contract change is not optional.** When an operation you produce or consume changed in a breaking way, both sides re-pin to the same release. `/ticket` marks it as required.

Nobody rewrites a ticket you've started. You see the change as a diff, and you decide.

## When you find a gap
If an operation, field, table or screen state is missing, or wrong, **raise it from `/ticket` as a CR** (source: developer). Don't work around it silently, and don't edit the package. The lead triages it: clarification, scope or defect; now or later. It lands in a release.

## When a ticket conflicts with the spec
Sometimes what you pulled contradicts itself or the contract. For example: a guest screen calls a staff-only
operation, a form sends a field the request schema lacks, a till reads the cashier's own record instead of
the guest's, or a screen that loads before sign-in calls an operation that needs a session. When that
happens:
1. **Raise a "spec defect" CR from `/ticket`.** Name the ticket and the artefacts, and quote both sides
   ("the ticket says X, the contract says Y").
2. **Name the invariant it breaks**, in one line. Examples: "a guest screen never binds a staff-audience
   operation", "every form control maps to a contract field", "a pre-sign-in load needs no session". This
   is what lets the lead turn your report into a check, so it cannot happen again anywhere.
3. **Carry on with the rest of the ticket.** Don't invent the missing piece. The lead triages the CR in the
   daily slot, as a blocker, a fix-forward or a defer, and the fix reaches you as a comment plus a linked
   delta ticket. Your ticket is never rewritten.

**Known issues** are listed in three places:
- the change log, `changes/CHANGELOG.md`; open entries are the known, unfixed changes;
- the check reports in the last release run (`python3 tools/run-checks.py`): `check-audience-match`,
  `check-preauth-session`, `check-subject` and `check-binding-ratchet` list issues by screen;
- `/ticket`, where each one shows what changed since your pin.

If your ticket's screen appears in one of these, it is known. Raise a CR only if you have something to add.

## Tables
From `r1` the **baseline migrations are frozen**. A table change arrives as a **new forward migration** in a release. Never edit an applied migration.

## If ADAM is down
The same release is tagged in the six repos (`ticvai-contracts`, `ticvai-backend`, `ticvai-frontend` and the others): `git checkout r<N>` and read the spec there. Tell the lead.
