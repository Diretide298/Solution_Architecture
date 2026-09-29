# TICVAI — build readiness

29 September 2026, updated that evening · Chinmay Parab · follows the report of 28 September (`docs/reports/build-readiness-28-september.md`)

## Verdict

**The back office is no longer waiting on the client.** On 28 September the answer was "build the sale-and-entry path, not the back office", because 577 operations had no agreement. On 29 September Chinmay decided that the readiness questions are ours to answer from the client's own minutes, packs and boards, and from our build plan where the client never ran a workshop. Only make-or-break questions stay with the client. The package now reflects that decision:

- **574 of 577 operations are agreed.** Each carries its evidence: 456 rest on the minutes and the pack, 105 on the pack and our build plan, and 13 on the pack alone. Three stay open, and they are make-or-break. The record is `docs/registers/readiness-closeout.md`.
- **The data model under them now exists.** Mapping those operations to tables showed that the packs gave screens, not tables. **211 tables** were designed and declared that day. Every new table has an operation that writes it, or a documented job. Agreed operations that touch no real table fell from 647 to 4.
- **Venue Management is complete as a specification.** Every screen binds its operations, and every configuration screen binds its write. BO-070 has a real entry point, and BO-051 moved to inventory. **It is ready to wireframe:** 142 Claude Design batches are exported, with the run order and prompt in `handoff/design-batches/VENUE-MANAGEMENT.md`.
- **The client's rev 3 prototype feedback is decided**, point by point: 55 decisions, four of which replace earlier audit decisions. The record is `docs/registers/rev3-decisions.md`.
- **148 screens show the client's own prototype** (POS terminal, guest web and guest mobile rev 3). The 8 views the prototypes lack were drawn in Claude Design and accepted.

|  | 28 Sep | 29 Sep |
| --- | --: | --: |
| Requirements specified | 2,650 of 2,788 (95%) | 2,781 of 2,848 (98%) |
| Operations | 2,135 | 2,405 |
| Not agreed (provisional) | 577 | 4 |
| Agreed operations touching no table | 64 | 4 |
| Tables | 678 | 988 |
| Screens naming an operation | 2,319 of 2,427 | 2,337 of 2,440 |
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

## Later on 29 September

Three more pieces of work landed after the morning's close-out.

**The requirements were re-traced.** The trace still said "no contract" for areas that had since been contracted: Accreditation (Domain 12), access policies (ABAC) and device management. 198 rows were checked against the contracts as they now stand, and 174 changed verdict. **2,781 of 2,848 requirements in scope are now specified (98%)**, up from 2,650 of 2,788 (95%). The 67 left are 5 not covered and 62 partly covered, and every one has a contract-backlog entry, so none is untracked:

- **Not covered (5):** a guest tax invoice and a credit memo (F&B), the e-invoicing export (Retail, which depends on the tax invoice), staff verifying a presented accreditation (Staff App), and storefront analytics (Marketing).
- **Partly covered (62):** mostly cookie consent for anonymous visitors (15), accreditation (13: document reads, credential delivery, renewal, events, export; backlog BL-180), F&B (7) and promotions (7).

The client workbook (`TICVAI - Build Readiness.xlsx`) now shows this per application: one sheet per application listing its requirements with what is left first, and a Requirements sheet with the client's own wording and filters.

**The AI design is decided.** Chinmay answered every question in the AI system design on 29 September, under the same rule as the close-out; none was make-or-break, so **none goes to the client.** The main decisions:

- Rules first, and a trained model per tenant only once a shadow run beats the rule. The admin is alerted, and a person promotes it; nothing switches by itself.
- TICVAI-managed Azure OpenAI in UAE North, re-billed per token as a line in the module-based subscription. Bring-your-own-key is available when TICVAI enables it for a tenant.
- All AI data retention is a tenant configuration, 90 days by default for prompts and responses, longer or shorter as the tenant sets it. Only a legal floor refuses a shorter value.
- Language models never work on data directly: figures are computed first and bound into the text, or the model writes the query and the platform runs it.

The design waits only on Chinmay's final read before it is committed. The record is section 8 of `docs/architecture/ai-system-design.md`.

**Four small leftovers were closed:**

- The Accreditation portal's applicant and reviewer screens call the accreditation operations instead of the approvals placeholders.
- The last resources operation without a screen, `getResourceQualifications`, is on the resource profile.
- 19 tables that no operation reached now have their writers named. Most are child tables written by their parent's operation.
- Staff reading a billing statement need `ORDER_VIEW`.

## What is left for us

Our work, not the client's. It is also in the workbook, sheet "Our work":

1. **Wireframes for Venue Management:** run the 142 Claude Design batches. Each returns a working file whose screens are captured as frames automatically.
2. **The 67 requirements not yet fully covered**, above. Each is in the workbook's Missing sheet and on its application's sheet, with the operation that would serve it.
3. **Six build gaps from the design packs**, sized at about 100 to 170 operations (`docs/active/design-pack-coverage.md`): Event Management, Entitlement Lifecycle (portfolio), Finance Backend, Virtual Queue, and the two AI packs.
4. **The AI contract work**, now that the design is decided:
   - the 89 new AI operations in `ai.yaml`, then binding the 88 TICVAI admin (P09) screens and the 8 Venue Management AI screens to them;
   - AI retention as a tenant configuration;
   - the bring-your-own-key switch on the platform side;
   - a private-to-tenant flag on subscription plans, so a custom package is not offered to everyone;
   - the six new ADRs (0049 to 0054) and the four amended ones.
5. **Small leftovers:**
   - the kitchen SLA table and the F&B stock recount table
   - which partner settings a partner may edit on its own portal
   - rebinding the deprecated partner-agreement fields on four screens
   - a screen for membership case notes
   - a writer for partner compliance documents
   - the support SUP-024 summary tiles
   - found on 29 September: nothing writes which outlets serve a delivery location; supplier contracts have no operation of their own; nothing reads an accreditation application's documents back, so reviewers cannot yet verify them on screen

## Where to start

The order from 28 September stands, and grows. The sale-and-entry path and the first Venue Management batch can be built now. Venue Management follows its wireframe batches, and the back-office tickets come from the regenerated ticket plan (the next step, after this report).
