# Build readiness, 30 September 2026

> **Purpose:** what changed since the build of 29 September, and where the package stands before Block A tickets
> **Owner:** Chinmay Parab
> **Status:** Current. Previous: build-readiness-29-september.md

## Where it stands

| | |
|---|---|
| Requirements in scope specified | 3,153 of 3,165 (the 12 partly covered each wait on a client answer) |
| Operations | 2,660, of which 2,650 ready |
| Screens that call an operation | 2,438 of 2,445 |
| Block A slice | 696 operations, 1,056 tasks |
| Checks | 34 run; back to the known baseline (two naming errors in the 21 September report, seven stale authored inputs) |

## What changed overnight

1. **New client material imported.** The minutes of 17, 18, 21, 24 and 29 September and six design books are in `sources/`, and the 29 September wireframe drop (Mobile App v4, Booking v2, Visit Planner) is in `sources/designs/guest-rev3-29-september/`. 80 decisions were read from them; 52 needed package changes.
2. **The 29 September workshop is applied (W1–W12 and the mobile redesign).**
   - Guest app: Home, Explore, Plan and Tickets tabs with a Buy tickets button on every screen; Item Detail with the map and the right product (a meal combo adds admission); At the Venue.
   - **The Plan tab is Block A:** a rules planner with the AI planner agent on top, and Plan Your Visit on the web. This supersedes the itinerary deferral (R187, R209, GAP-C3).
   - Guest checkout asks only the configured fields; seat maps zoom by section; view-only products show "contact sales"; Help me choose filters the catalogue; meeting rooms check date, start and duration together, with a cleaning buffer.
3. **The CMS is a flow builder.** Operators pick booking flows from 16 types, see each step as required, optional or conditional, set their own order, then finish in the configuration panel (Site Builder, Booking Flows, App Build & Store Publishing).
4. **Every AI function is built inside the six months, baseline first** (decided 30 September). Each AI answer works on day one and states its stage (starting, learning, established, learned); a venue can import its own history; a trained model replaces the baseline only when an admin approves. Two AI engineers from 5 October, no third.
5. **The system-design review's package findings are fixed.** Among them:
   - the generated database script is valid again (the first migration no longer fails);
   - every contract declares authentication, and guest operations use the guest scheme;
   - a paid order issues its tickets (AccessService) and the ledger posts once;
   - a sale converts its hold and reduces capacity, so nothing oversells;
   - the payment provider's webhook, 3-D Secure and the card terminal are specified;
   - a POS food order reaches the kitchen;
   - wallet spending holds a lock; one bad offline sale no longer blocks a till;
   - every tenant table has a row-level policy.
6. **Partners no longer create products, prices or performances through the API** (17 September minutes), and production API keys are issued only after certification.

## Waiting on decisions

- **Before Monday 5 October (Chinmay):** the architecture decision drafts, in particular the key shape, the deployment shape, the message broker and relay, and .NET 10. Drafts: `audit/ticvai/steps/SD/adr-drafts/`.
- **The client:** e-invoicing (provider, mandate date, VAT 201 layout), what 99.99% covers, biometric template storage and retention, the guest-checkout marketing consent position, and the Apple and Google developer accounts per client.

## Documents

- Build plan: `handoff/TICVAI - Build Plan.xlsx`, `docs/active/build-plan-presentation.md`, and the deck https://claude.ai/artifact/NzvBoTU53zNbwCouMgz4ch
- Six-month plan and its decisions: `docs/active/six-month-plan-29-september.md` (decisions 1–12)
- Reviews: `docs/active/ai-functions-review-30-september.md`, `docs/active/system-design-review-30-september.md`
