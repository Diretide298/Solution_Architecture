# Council of 2 October 2026: a complete audit, and a change log with prevention rules

> **For:** everyone changing the package. **Source of** `ticvai/CLAUDE.md`, `changes/`, the new checks
> (`check-changelog`, `check-binding-ratchet`, `check-audience-match`, `check-preauth-session`,
> `check-subject`) and the "Rules from 5 October" in `release-runbook.md`.
> **Why this file exists:** the council's transcripts live in `audit/ticvai/council/`, which git ignores.
> A rule must cite a source every clone can open, so the two verdicts are copied here verbatim.
> Full transcripts (not in git): `audit/ticvai/council/council-transcript-2026-10-02.md` (Sonnet run) and
> `council-transcript-2026-10-02-opus.md` (Opus run).

**The question (Chinmay, 2 October):** "I feel let's do a complete audit, not just for Block A. Then, for
any changes ahead, we write a log and instructions, so we can avoid them going forward and have a better
way to integrate them."

**Chinmay's instruction after the council:** "Take in the council's input, log them, hard-code them as
strict instructions for further inputs after Monday." Also confirmed: the weekly AI budget is Block A 50%,
Block B 25%, Blocks C and D 15%, finding new kinds of issue 10%. And, the same night: "All the changes and
fixes: log them, also the decision and why."

---

# Verdict of the Opus run

## Where the Council Agrees
- **Checks, not sweeps.** About 34 findings per root cause. Every known cause becomes a deterministic check. AI is spent only on finding new classes of issue.
- **The generator's three counts become ratchet merge gates now:** 5,613 unbound controls, 55 undefined operations, 42 missing fields. A merge fails if any count goes up.
- **Typed properties close the "semantic" cases.** Each operation is declared and checked for: its audience (guest or staff), whether it needs a session, and whether it acts on the caller or a named customer.
- **The prevention record is enforced:** no change-log entry closes without a check ID, and the merge gate enforces it.
- **Plan changes ship only in the Tue/Fri release.**

## Where the Council Clashes
- **Complete audit vs. no audit.** Resolution: "complete" means every artefact class in every block passes a check or a sampled AI pass. It does not mean re-reading every screen.
- **Gate Monday's pulls vs. let developers pull.** Gating on screens that fully resolve would idle developers, because only 1,330 do. Resolution: gate only Sprint 1 tickets, and only on the known defects.
- **Productising the method.** Deferred. The 12 developers act as auditors.
- **Monday-12:30 timing.** Obsolete: capacity is available now.

## Blind Spots the Council Caught
- **The 5,613 count needs classifying first.** Much of it is static text, so it needs an allowlist whose entries expire. 1,683 earlier findings were false or only partly real.
- **No weekly AI budget.**
- **No release tag named for agent output.** Agents need isolated worktrees and checkpoint commits.
- **No tasks named for the AI engineers.**
- **Command centres, dashboards and simulation** haven't been checked for completeness.
- **No contract tests** on developer code.
- **Two screen counts:** 2,447 vs 2,422.

## The Recommendation
**Today and this weekend**
- **Apply r2 to OpenProject.** It is the baseline; fixes go into later tags.
- **Clean the tree.**
- **Fix before Friday's release, before any Block A ticket starts:** the storefront theme read, the policy read, and staff fields on guest screens.
- **New checks:**
  - check-binding-ratchet, with checks/baseline.json recorded from r2 and an allowlist whose entries expire after 14 days;
  - check-audience-match;
  - check-preauth-session;
  - check-subject (caller vs. named customer);
  - check-changelog.
- **Reconcile the screen count.**
- **Re-audit:** F8 on the Sprint 1–2 Block A tickets.
- **Process agents:** Block A apps first, each in its own worktree with checkpoint commits.
- **Weekly AI budget:** A 50%, B 25%, C and D 15%, sampling for new classes 10%.
- **Publish the Sprint 1 pull list.**

**Monday**
- Developers pull from that list.
- ADAM gets a "spec defect" change-request type that must name the broken invariant.

**Weeks 1–2**
- Every Tue/Fri release carries fixes.
- Each new root class gets one check, which then runs across all blocks.

**The complete audit, by block**
- **A:** F8 on all 659 tickets, plus process agents on guest web, guest app, POS and kitchen display.
- **B:** all checks, plus a simulated pull of one ticket per root class per app.
- **C and D:** checks and process agents now; a ticket-level audit when they are broken into tasks.
- **Across all blocks:**
  - trace the 1,119 MoM inputs and 53 open questions;
  - check command centres, dashboards and simulation for completeness;
  - close the 435 tracker rows.

**The change log: `ticvai/changes/CHANGELOG.yaml`**
- **Fields:**
  - `id` (CHG-nnn) and `date`;
  - `source`: MoM, change request, audit root or client review;
  - `kind`: spec, contract, plan or design input;
  - `keys_touched`, `root_class`, `tickets` (started or unstarted) and `release_tag`;
  - `client_signoff`, required when the source is a MoM;
  - `prevention`: a check ID, a generator rule, a template field, or `none:<reason>` approved by the lead;
  - `status`.
- **Closing rule:** an entry closes only when its prevention is merged and fails on the commit before the fix. check-changelog blocks any spec merge that has no CHG id.

**How changes reach tickets**
- **Unstarted:** picks up the fix at the next tag, through its pointer body.
- **Started:**
  - never rewritten;
  - the change request generates a linked delta ticket;
  - ADAM keeps serving the tag the developer started on until they finish.

**Decision churn**
- A plan change is a CHG entry of kind `plan`.
- It changes only at a Tue/Fri release, after 24 hours of cooling off.
- MoM sign-offs are batched weekly.

**Who does what**
- **Lead:** decisions, sign-offs, approvals, releases.
- **AI engineers:** checks, and the AI audit spend.
- **Developers:** build, raise spec-defect change requests, write contract tests.

## The One Thing to Do First
When r2 lands, record its counts in checks/baseline.json and make check-binding-ratchet a merge gate before any audit fix merges.

---

# Verdict of the Sonnet run

## Where the Council Agrees
- **Audit by root cause, not by screen.** The 9,976 findings came down to 293 root issues, and the 248 corrections on 143 screens are a few dozen patterns repeated by the generator. Turn each root into a deterministic check and sweep all 2,447 screens inside the refresh, at zero AI cost.
- **Spend AI only where scripts can't see:**
  - new rule classes, found by sampling per app;
  - the 7 unfinished process agents;
  - the meaning of the contracts.
- **Freeze started tickets:** nothing rewrites a ticket a developer has pulled.
- **Run the F8 re-audit on Block A first.**
- **A change-log row closes only when it links a check or generator rule** that now fails if the problem comes back.

## Where the Council Clashes
- **When to run the full audit.**
  - The Contrarian and the Executor would defer it.
  - The Expansionist would turn it into a product.
  - **Resolution:** deliver it in full, as a free scripted sweep first, then AI by block in block order.
- **Sample size.** The Contrarian wants 10% per app, First Principles about 20 screens per app. **Resolution:** 20 per app, widened only where a new class of issue appears.
- **Change churn.**
  - The Outsider wants a 48-hour rule against reversing a decision.
  - First Principles wants one decision register with one owner.
  - **Resolution:** both.
- **Commercial extras** (priced change requests, a tenant-config validator sold as a feature) are parked for now.
- **The Executor's premise that C1–C15 isn't built is wrong.** C1–C15 is live and r1 has shipped, so that point is discarded.

## Blind Spots the Council Caught
- **Fixes to started tickets go through C1–C15:** a change-request delta against the release tag, never a re-derive of the ticket.
- **Test every new check against the F1–F7 fixed set first.** 367 findings were false, and an unvalidated check would block merges.
- **Some gaps need decisions, not checks:** controls with no field behind them, the theme read that needs a signed-in session, and guests being unable to read policies.
- **Errors of meaning in the contracts can't be caught by checks.** Examples are the cart audience and the loyalty read. They need a review for meaning, and each fix can expose a deeper slip.
- **The client needs a sign-off queue,** with batching and a default if they don't answer. It covers the 1,119 meeting inputs, the 53 open questions and the 435 tracker rows.
- **Developers need support on Monday:** a known-issues note per ticket and a way to escalate through ADAM.
- **Still open:** the 248 corrections already found, and the lead being the single point of failure.

## The Recommendation
**Phase 0: before Monday, no AI.**
- Commit or discard partial agent work; get every cited source file into git.
- Write `ticvai/handoff/known-issues-block-a.md`, keyed by ticket: the open root issues and the F1–F7 outcomes. Link it from the pointer bodies.
- **Freeze line:** any ticket past "New" is frozen. It changes only through an ADAM change-request delta against the release tag, arriving as a comment plus an addendum ticket. Its body is never rewritten.

**Phase 1: Monday 5 Oct, after the 12:30 IST reset.**
1. Run the F8 re-audit of the Block A tickets.
2. With scripts only, turn the 293 roots and the 248 corrections into checks, in deterministic classes:
   - audience vs field;
   - a config read that needs a session;
   - an enum that differs between contract, screen and prototype;
   - an orphan control;
   - an operation with no contract behind it;
   - an unbound field.

   Each check is validated against the F1–F7 set before it joins the merge gate.
3. Run all checks over all 16 apps, in block order A, B, C, D. That gives the complete count with no AI.

**Phase 2: weeks 1–2.**
- **New classes:** sample 20 screens per app with AI.
- **Process agents:** finish the 7 in block order.
- **Contracts:** review their meaning, app by app.
- **Contract decisions and the 53 open questions:** one client sign-off queue, one batch per release; silence is treated as acceptance after 5 working days.
- **Fix forward block by block:** A and B first, C and D before their own sprints.

**The change log: `ticvai/changes/CHANGELOG.yaml`.**
- One row per change, with these fields: `id`, `date`, `source`, `root_class`, `artefacts_cascaded`, `blast_radius`, `frozen_tickets_affected`, `decision_owner`, `check_added` (or `none-possible: <reason>`), `release_tag`.
- **No row closes and no change merges without a `check_added` that fails before the fix and passes after it.**
- It starts with this week's churn as its first entries.

**How changes come in.**
- **Decisions:** one decision register, owned by the lead. No decision is reversed within 48 hours, and none is announced until it is committed.
- **Triage:** every change request is classed as a blocker, fixed forward, or deferred.
- **Releases:** Tuesday and Friday, with no spec edits the day before.
- **Canary:** after each release, one AI session pulls 5 tickets as a developer would.
- **Lead's load:** a daily 30-minute triage slot caps it.

## The One Thing to Do First
Today: write `known-issues-block-a.md` and declare the freeze line, so Block A is stable for Monday. Then, at 12:30 on Monday, start the F8 re-audit.
