# How you get your work, and how change reaches you

> **For:** every TICVAI developer, from Monday 5 October 2026. **From:** Chinmay. One page; read it before your first `/ticket`.

## Where things live
- **OpenProject holds who, when and order.** Your board, your assignee, your Block A week, the build order (Priority_No.) and the status you move the ticket through.
- **ADAM holds what: the spec.** The contract, the tables, the screen and its states come from the package, served by ADAM at a **release**: `r1`, `r2`, and so on. A ticket's text in OpenProject is only a pointer (from `r1`) or an old snapshot. **Never build from the OpenProject text. Build from `/ticket`.**

## Your day
1. `/board` shows your open tickets in build order: started work first, then the order to work in.
2. `/ticket <id>` pulls one ticket at the **latest release**. You and your agent are always on the latest release: there is no release to choose and nothing to re-pin (CHG-ADM-001, 14 October 2026).
3. Build against what `/ticket` gives you. If you can't finish the ticket in one go, pull it again the next day; that pull is at the latest release too.

## When the spec changes under you
Releases go out on **Tuesday and Friday**. If something your ticket touches changed, the next `/ticket` is already at the new release and says **"What changed since your previous pull (r1 -> r2)"**, with the diffs in `spec-diff.md`. Build against the files as they are now.
- **A breaking contract change** on an operation you produce or consume is called out in that section: both sides build against the latest release, so check the code you wrote before the pull.
- **Raise a CR** if a change doesn't fit your ticket, with the reason, and build the rest.

Nobody rewrites a ticket you've started.

## When a change request is settled
When the lead settles a CR raised from your ticket (accepted, done or rejected), ADAM tells the ticket (CHG-ADM-002):
- **Your ticket is not closed:** it gets a comment written for your agent ("ADAM CR-076 · accepted — read before building": what was decided, which release carries it, what to do now), and `/ticket` lists the CR near the top of README.md under "Change requests on this ticket". Follow a settled decision where it differs from the description; wait on the part an open CR covers.
- **Your ticket is closed:** the change becomes a **child task** of it, carrying the CR, the decision and the release. A CR's work is one child task; migration work it causes is a child task of the affected MIG-* ticket, for the migration owner.

## When you find a gap
If an operation, field, table or screen state is missing, or wrong, **raise it from `/ticket` as a CR** (source: developer). Don't work around it, and don't edit the package. If it blocks the ticket, the CR is `blocking`, the ticket goes On hold and you move to the next workable ticket (below). The lead triages it: clarification, scope or defect; now or later. It lands in a release.

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
3. **If it blocks the ticket, put the ticket On hold and move on.** A blocker is always a CR, raised with
   `blocking: true` (CHG-ADM-004). Never work around it and never build a guess. Your agent proposes the
   ticket **On hold** naming the CR, then the next ticket you can finish: `/board` marks each ticket an open
   blocking CR affects (`blocked`) and names the first workable one, and `/ticket` shows a **Blocked by**
   section. If the CR does not block the ticket, build the rest. The lead triages the CR in the daily slot,
   as a blocker, a fix-forward or a defer, and the fix reaches you as a comment for your agent (or a child
   task, if your ticket is closed by then; see "When a change request is settled"). Your ticket's text is
   never rewritten.

**Known issues** are listed in three places:
- the change log, one file per change in `changes/entries/` (indexed in `CHANGELOG.md` beside it at each release); open entries are the known, unfixed changes;
- the check reports in the last release run (`python3 tools/run-checks.py`): `check-audience-match`,
  `check-preauth-session`, `check-subject` and `check-binding-ratchet` list issues by screen;
- `/ticket`, which shows what changed since your previous pull and the change requests on your ticket.

If your ticket's screen appears in one of these, it is known. Raise a CR only if you have something to add.

## Tables
From `r1` the **baseline migrations are frozen**. A table change arrives as a **new forward migration** in a release. Never edit an applied migration.

## If ADAM is down
The same release is tagged in the six repos (`ticvai-contracts`, `ticvai-backend`, `ticvai-frontend` and the others): `git checkout r<N>` and read the spec there. Tell the lead.
