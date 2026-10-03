# The AI engine after Block A: phase 1 by 2 April, phase 2 after (4 October 2026)

> **The cited copy (4 October 2026, CHG-AIPH-001).** From Chinmay's answers log (the lead's working log of batch 1
> onward), the section "AI work after Block A: phase 1 by 2 April, phase 2 after", and Chinmay's instruction to the
> plan agent the same morning about Block A. Copied into git so CHG-AIPH-001, `docs/active/ai-phase-plan.json` and
> `tools/build-service-docs.py` can cite them (`ticvai/CLAUDE.md` rule 12). Both are verbatim. Applied by CHG-AIPH-001.

## AI work after Block A: phase 1 by 2 April, phase 2 after (Chinmay, 4 Oct 2026, ~04:00)
- Chinmay: "collect tasks that need data we can do those phase 2. fit what we can till release and rest is phase 2 also pick most beneficial ones to prioritise first." And: "do not pick trails that we cannot complete."
- **Rule.** Phase 1 (by 2 Apr 2027) = the parts of each AI capability that work on day one without tenant history (rules, priors, LLM over the venue's own config and data). Phase 2 (after 2 Apr) = every part that learns from tenant data: statistical engines fitted on own history, trained models in shadow, classifiers, learning-to-rank, the training/backtest/shadow job and the promotion rule. **Why:** no tenant has real history before go-live, so those parts could not be finished or proven by 2 Apr anyway; phase 2 lands when the data exists.
- **Completion rule.** A capability goes into phase 1 only as a whole unit that finishes by 2 Apr, including its backend and screen dependencies. No "2 of 5" chains across the line. **Why:** Chinmay, "do not pick trails that we cannot complete".
- **Priority (benefit first):** configuration assistant (client's first AI priority, MoM 14 Aug, CF-57); seat-map and layout generation (client priority 17 Aug, AI import decided 21 Aug); fraud and risk rules scoring; recommendations runtime with rules; analytics assistant; forecast prior producer; operational requirements; queue and wait time; approval scoring; marketing playbooks.
- **Phase 2:** forecasting statistical engine and learned producer; fraud classifier; learning-to-rank; the shared training/backtest/shadow job and promotion rule; anomaly detection; dynamic pricing suggestions.
- **Correction to "all unassigned AI tasks are recommendations":** most came from the 30 Sep AI review, but recommendations, operational requirements and queue/wait time were in the original plan (B2), and seat-map generation and the analytics assistant were client-named. The client message for phase 2 must say this.
- **Double count to remove:** AI-ENGINE-SHARED-BASELINE-THEN-LEARN-1..4 (40 days, Block D) repeat the estimator, venue profile and benchmark priors that AI-ENGINE-BASELINE (Block A, 15 days) already builds; only the training/backtest/shadow job and the promotion rule remain, and they are phase 2.
- Capacity after A2: Kalpita ~82 working days (4 Dec to 2 Apr), the second AI engineer ~75 (15 Dec to 2 Apr). Phase 1 is ~115 days, which leaves ~40 days of buffer for the evaluation gates and the Block A AI overrun already on record (13 AI-weeks against 10).

## No Block A change (Chinmay, 4 Oct 2026, to the plan agent)
- "do NOT change any Block A or A2 AI task (AI-ENGINE-GATEWAY, GUIDED, TRANSLATE, QDRANT, CONCIERGE, BASELINE, SCRUB-GUARD, EVAL, PLANNER, SUGGESTIONS) or any Block A dependency, dates or assignee. If the phase split seems to need a Block A change (e.g. a dependency you would move earlier into Block A, or the double count touching AI-ENGINE-BASELINE), do not make it: list it in your report under "Block A changes needed" with the reason, and choose phase 2 for the affected unit instead."
