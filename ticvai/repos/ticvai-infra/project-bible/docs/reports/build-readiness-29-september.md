# TICVAI — build readiness

29 September 2026 · Chinmay Parab · follows the report of 28 September (`docs/reports/build-readiness-28-september.md`)

## Verdict

**The back office is no longer waiting on the client.** On 28 September the answer was "build the sale-and-entry path, not the back office", because 577 operations had no agreement. On 29 September Chinmay decided that the readiness questions are ours to answer from the client's own minutes, packs and boards, and from our build plan where the client never ran a workshop. Only make-or-break questions stay with the client. The package now reflects that decision:

- **574 of 577 operations are agreed.** Each carries its evidence: 456 rest on the minutes and the pack, 105 on the pack and our build plan, and 13 on the pack alone. Three stay open, and they are make-or-break. The record is `docs/registers/readiness-closeout.md`.
- **The data model under them now exists.** Mapping those operations to tables showed that the packs gave screens, not tables. **211 tables** were designed and declared that day. Every new table has an operation that writes it, or a documented job. Agreed operations that touch no real table fell from 647 to 4.
- **Venue Management is complete as a specification.** Every screen binds its operations, and every configuration screen binds its write. BO-070 has a real entry point, and BO-051 moved to inventory. **It is ready to wireframe:** 142 Claude Design batches are exported, with the run order and prompt in `handoff/design-batches/VENUE-MANAGEMENT.md`.
- **The client's rev 3 prototype feedback is decided**, point by point: 55 decisions, four of which replace earlier audit decisions. The record is `docs/registers/rev3-decisions.md`.
- **148 screens show the client's own prototype** (POS terminal, guest web and guest mobile rev 3). The 8 views the prototypes lack were drawn in Claude Design and accepted.

|  | 28 Sep | 29 Sep |
| --- | --: | --: |
| Operations | 2,135 | 2,405 |
| Not agreed (provisional) | 577 | 4 |
| Agreed operations touching no table | 64 | 4 |
| Tables | 678 | 988 |
| Screens naming an operation | 2,319 of 2,427 | 2,334 of 2,440 |
| Screens showing the client's prototype | 0 | 148 |
| Questions for the client | five sessions and a decision | 14, all make-or-break |

## What is left for the client (make-or-break only)

These are the only questions, and they are in `handoff/TICVAI_Readiness_Questions.xlsx`, sheet "Make or break". Each is either law, a name only the client has, or money their customers pay or get back.

| Question | Why only the client can answer |
| --- | --- |
| At what age must a guardian consent to a minor's Face Pass enrolment, per jurisdiction? | Law (data protection, age of majority) |
| How long may Face Pass, Face Tag and failed capture data be kept, per region? | Law |
| When an event is cancelled after a resale, who is refunded, how much, and is the seller's payout clawed back? | Their customers' money |
| The age below which a guest is a minor | Law |
| How long each kind of guest document is kept | Law |
| The facial-reader vendor | A vendor only they choose |
| Approved dependencies, payment sandbox access, the design reviewer | Names and accounts only they hold |
| A/B price tests on live customers, cooling-off after auto-renewal | UAE consumer law. **Not blocking**: built as venue-configured policy that a person approves |

## What is left for us

Our work, not the client's. It is also in the workbook, sheet "Our work":

1. **Wireframes for Venue Management:** run the 142 Claude Design batches. Each returns a working file whose screens are captured as frames automatically.
2. **Six build gaps from the design packs**, sized at about 100 to 170 operations (`docs/active/design-pack-coverage.md`): Event Management, Entitlement Lifecycle (portfolio), Finance Backend, Virtual Queue, and the two AI packs.
3. **The AI screens:** 88 TICVAI admin (P09) screens name no operation. They wait on the AI system design review (`docs/architecture/ai-system-design.md`, not yet committed).
4. **Small leftovers:**
   - the kitchen SLA table and the F&B stock recount table
   - which partner settings a partner may edit on its own portal
   - rebinding the deprecated partner-agreement fields on four screens
   - a screen for membership case notes
   - a writer for partner compliance documents
   - the support SUP-024 summary tiles

## Where to start

The order from 28 September stands, and grows. The sale-and-entry path and the first Venue Management batch can be built now. Venue Management follows its wireframe batches, and the back-office tickets come from the regenerated ticket plan (the next step, after this report).
