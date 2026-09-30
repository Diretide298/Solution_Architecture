# Six-month build plan, re-planned 29 September 2026

> **Purpose:** the delivery plan and the decisions behind it, for the project manager
> **Owner:** Chinmay Parab
> **Status:** Agreed 29 September 2026. The shareable page is https://claude.ai/artifact/VT8rQQSBPkzgm4XyGazUdd

## Why re-planned

On 29 September the specification reached **3,153 of 3,165 requirements in scope covered**. The 12 still partly covered each wait on a client answer, and 19 are parked (declined by the client or ruled out by the minutes). The plan could therefore be sized against real scope instead of estimates. Block B was sized with the same points formula as Block A.

## Timeline

| Phase | Dates | Scope |
|---|---|---|
| Block A | Mon 5 Oct – Fri 20 Nov 2026 (35 working days) | POS with Kitchen Display; Guest Web; Guest App with the 29 September Mobile v4 redesign and the Plan tab; the CMS flow builder; Venue Management setup screens; AI that needs no accumulated data |
| B1 | 23 Nov 2026 – 1 Jan 2027 | Scanner; Staff App waves 1–2; Kiosk; remaining CMS steps; Venue Management waves 1–2 and the first wave-3 modules; TICVAI console waves 1–2; Sign-up; AI action pipeline and events |
| B2 | 4 Jan – 12 Feb 2027 | Partner portal with the B2B option; Support; Accreditation; Developer Portal; Staff App wave 3; Venue Management wave 3 continues; AI rules-first forecasting, fraud and recommendations |
| B3 | 15 Feb – 2 Apr 2027 | The rest of Venue Management and the console, including the AI console; Analytics; hardening |

The holidays (National Day, New Year, Eid al-Fitr around 10 March 2027) are counted: about 7 working days. The calendar is to be confirmed.

## Size and capacity

- **Pace:** Block A's planned 3,018 points in 35 days is about 86 points a day for the team, or 9.6 per developer. The real pace is measured after three weeks (23 October), and Block B is recomputed from it.
- **Block A:** about 3,320 points after the 29 September additions. Surendra takes the Venue Management setup screens. The remaining CMS steps (about 200 points) open Block B. The last ~100 points are spread across the team at ticket assignment, roughly an hour a week each.
- **Block B:** about 9,850 points: screens by the formula, and the back end at Block A's 2.11 points per operation. That needs about 11.7 developer-equivalents; with two more developers the team is 11.6.

## Decisions (29 September)

1. **Block A starts Monday 5 October 2026.**
2. *(Data-driven AI: see decision 10.)* **AI that needs no accumulated data may be in Block A,** where the Block A apps need it: the gateway and governance, the guest concierge, the Help me choose suggestion, translations and the planner agent. **Data-dependent AI waits:** forecasting, anomaly detection, trained fraud and recommendation models. Block A uses rules until then: upsell from the Promotions relationship map, fraud from Orders' own rules.
3. **The planner is in Block A:** a rules-based Plan tab with the AI planner agent on top.
4. **The CMS becomes a flow builder.** Operators pick their ticketing flows, see which steps are required and which optional, compose their own order, and finish in a configuration panel. The rest of the CMS steps from the requirements matrix follow.
5. **Team:**
   - the current nine;
   - Kalpita on AI;
   - Surendra (full stack, counted at ~60% pace) on Venue Management from week 1;
   - a second AI engineer from Monday 5 October (changed 30 September, decision 11);
   - **two more full-stack developers joining by early November** for Block B.
6. *(Superseded 30 September by decision 10.)* **The analytics assistant and the configuration assistant move past month 6** as a phase-2 item, to be told to the client. The platform runs without them. The narrow Help me choose suggestion stays in Block A. Anomaly detection also starts after month 6, and trained models were always after month 6.
7. **Wave-3 deferral list:** a contingency only, decided on 18 December if the first Venue Management wave-3 modules do not come in at least 25% under the formula.
8. **B2B reseller portal:** Claude Design draws both options (POS-style and website-style) first, plus a demo page for our other apps with simple simulations. The choice follows the review.
9. **A re-audit runs just before tickets,** against the deployed ADAM. It covers every new and changed Block A ticket and a sample of 30 unchanged ones.

## Decisions (30 September)

10. **Every AI function is built inside the six months.** Data-driven AI ships with a working baseline on
    day one (venue profile, venue-type starting pattern, UAE calendar and weather, the venue's own imported
    history) and grows more accurate as the tenant's data builds up. A trained model runs in the background
    and replaces the baseline only when it beats it and an admin approves (AI-D16). No customer hears
    "this arrives when you have data". This reverses decision 6: the analytics assistant, the configuration
    assistant and anomaly detection come back inside the six months. What cannot happen by 2 April is a
    trained model going live for a tenant, because that needs a season of the tenant's own data; the code
    ships, the switch happens per tenant later. Review: `audit/ticvai/steps/AI2/ai-functions-review.md`.
11. **The second AI engineer starts Monday 5 October** with Block A. **No third AI engineer.** The two AI
    engineers carry the engine work (models, pipelines, backtests, the baseline-then-learn layer); the AI
    endpoints and screens are built by the developers like any other module.
12. **Deep Khanvilkar takes a larger back-end share, proportional to his ratings** (.NET 2 and PostgreSQL 2
    against the owners' 3–4): about 55% of an owner's load, tasks up to 3 points. Loads otherwise follow
    skill and experience and are uneven on purpose.
13. **Architecture, from the system-design review** (`docs/adr/`): a modular monolith of 17 modules
    deployed as five units, `commerce`, `access`, `operations`, `ticvai-ai` and `workers` (ADR-0055); .NET 10
    LTS from day one; one id type, UUIDv7, and monthly time partitioning, with venue partitioning deferred
    (ADR-0056); one outbox relay per region and an inbox per tenant database (ADR-0058); vectors in Qdrant from
    day one, one collection per tenant with a collection-scoped token (ADR-0049); AI on a baseline, learning per tenant (ADR-0051), phased per
    ADR-0059; one autonomy scale (ADR-0050). **The event broker is RabbitMQ or Kafka, not Azure Service
    Bus, and the client chooses** (ADR-0057, proposed): our recommendation is RabbitMQ; we need the answer
    before sprint 1 week 2 so the relay is proven by 23 October. Until then everything is built behind the
    kernel interface on a local RabbitMQ.

## Headcount to finish in six months

| | People |
|---|---|
| Current developers | 9 (Pradnya, Chitrangi, Chinmay Patkar, Sanket, Pallavi, Hrushikant, Pranay, Tanmay, Deep) |
| Surendra | 1 (Venue Management) |
| New full-stack developers | 2 (by early November) |
| AI | Kalpita + a second engineer from 5 October (no third) |
| **Total** | **14**. Chinmay Parab is not counted in capacity. |

## Checkpoints

- **23 October:** Block A's real pace is known, and Block B is recomputed. Hiring the two developers is confirmed.
- **20 November:** Block A done.
- **18 December:** the deferral decision, only if needed.
- **2 April 2027:** end of the six months.

## Outside the plan

- **Screen engine:** Chinmay's own experiment, with no dates. It does not change the plan's totals. Design: https://claude.ai/artifact/7szQsV5omPjxzYumAAej6T
