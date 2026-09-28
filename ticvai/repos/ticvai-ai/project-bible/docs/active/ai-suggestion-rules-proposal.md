# AI suggestion rules: one rule and a minimum history per kind

> **Purpose:** What each of the 13 `SuggestionKind` values bases its answer on on day one, and how much history is "enough data"  
> **Owner:** Chinmay  
> **Status:** **Proposed, client to correct (audit R213, decided 28 September 2026)**  
> **Who corrects it:** client product

`requestSuggestion` in `ai.yaml` answers thirteen kinds of question and **ships answering from heuristics**, but the contract stated a rule for only two of them (price: a margin rule; replenishment: par level minus on-hand plus lead time). Its `422` *not enough data* had no threshold. On 28 September Chinmay adopted our default: we draft a one-line rule and a minimum history per kind, and the client corrects them. The rules and minimums below are the ones `SuggestionKind` in `ai.yaml` now states.

**How to read the table.**

- **Rule** is the day-one heuristic (`SuggestionBasis: heuristic`). A model replaces it later as a provider change, not a contract change, and the response's `basis` says which one answered.
- **Minimum history** is the threshold for the `422`. Below it, `requestSuggestion` refuses with `InsufficientDataProblem`, naming the input in `missing[].input`, what exists in `have` and this figure in `need`.
- History is counted **at the scope the question is asked at** (usually the venue), in trading days that have sales or activity for the subject of the question.

| # | Kind | Rule (day one) | Minimum history |
|---|---|---|---|
| 1 | `price` | Unit cost plus the category's target margin, held inside the price band | A current cost; no history |
| 2 | `replenishment` | Par level minus on-hand, plus expected use over the supplier lead time | 14 days of stock movements |
| 3 | `requisition` | The next service's prep-plan ingredient needs minus kitchen stock | 14 days of sales |
| 4 | `demandForecast` | The average of the same weekday over the last 8 weeks, adjusted by admissions already booked | 8 weeks of sales |
| 5 | `prepPlan` | Forecast covers for the service times each item's share of the last 4 same weekdays | 4 weeks of sales |
| 6 | `menuEngineering` | Each item placed by popularity against margin, over 90 days | 90 days of sales |
| 7 | `staffing` | Forecast demand divided by the role's standard covers per staff hour | 8 weeks of sales (the forecast it rests on) |
| 8 | `slaTarget` | The 80th percentile of actual times over the last 30 days | 30 days of timed events |
| 9 | `waitTime` | People ahead divided by the throughput of the last 30 minutes | 30 minutes of throughput today |
| 10 | `upsell` | The item most often bought with the basket's items over 90 days | 90 days of orders |
| 11 | `segmentation` | Recency, frequency and spend scores over 12 months | 90 days of orders |
| 12 | `anomaly` | A value outside three standard deviations of the same weekday over 8 weeks | 8 weeks of the measure |
| 13 | `scenario` | The demand forecast re-run with the stated changes | As `demandForecast` (8 weeks of sales); a scenario never runs on less than its base forecast |

---

## Where this goes next

- **The contract.** Each rule and minimum above is stated on `SuggestionKind` in `ai.yaml`, and the `requestSuggestion` `422` points to it: below the minimum it answers `InsufficientDataProblem` with this figure in `need`. When the client corrects a rule or a minimum here, `SuggestionKind` is corrected to match in the same change; if the two ever disagree, the contract is what runs.
- **Part 2 of R213: expiry.** A proposal still `proposed` expires **7 days** after it was proposed; one `approved` but not applied expires **24 hours** after the decision. `ProposedAction.expiresAt` carries whichever applies, and deciding an expired proposal is refused `409`. Both figures are proposed, client to correct.
- **Part 3 of R213: approval levels.** Level **2** is anything touching prices or permissions — every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant. It needs `AI_APPROVE`, and the approver may not be the person who prompted it. Level **1** is everything else: the requester may decide their own level 1 proposal under `AI_USE`. Deciding **someone else's** proposal, at either level, needs `AI_APPROVE`. Each refusal is a `403` naming the rule that failed (`approval-level-requires-manager`, `approver-is-requester`, `not-own-proposal`), and `listProposedActions` shows an `AI_USE`-only caller just the proposals they prompted.
