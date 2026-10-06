# The client's tracker answers of 6 October 2026

> **From:** TICVAI (Allam / Qossai) · **Date:** 6 October 2026 · **Filed:** 6 October 2026 (CHG-R4-017), verbatim,
> so the package can cite it (`ticvai/CLAUDE.md` rule 12). Read-only, like everything in `sources/`.
>
> **Where it came from.** The "Viva Notes" column of the joint tracker `TICVAI_Task_Tracker_30-September.xlsx`
> (sheet *Tracker*), which the client returned on 6 October 2026. The rows the client had to act on (T1-T10) are
> below: the task and our note as we sent them, then the client's note exactly as written (spelling and wording
> unchanged). The Softlabs rows (S1-S16) carried no client note.

---

## T1. Feedback on the revised website and mobile wireframes

- **Owner / due:** Allam / Qossai · 1 Oct
- **Our note:** (none)
- **Viva Notes:**

Revised Feedback sent

## T2. Answers to the emailed questions (Decisions Register, 'For you to answer')

- **Owner / due:** Allam / Qossai · On receipt
- **Our note:** E-invoicing, biometrics incl. children, 99.99% scope, marketing consent, app store accounts, design
  reviewer, payment sandboxes, hardware and suppliers
- **Viva Notes:**

All the questions has been updated in the Decision register.

## T3. Event broker: RabbitMQ or Kafka

- **Owner / due:** Allam / Qossai · 12 Oct
- **Our note:** Needed for the first end-to-end purchase on 23 Oct
- **Viva Notes:**

Kindly refer to the decision register

## T4. Review the revised tracker

- **Owner / due:** Allam / Qossai · On receipt
- **Our note:** (none)
- **Viva Notes:**

Updated the tracker for the Ticvai owner points

## T5. Confirm the weekly stand-up day and time

- **Owner / due:** Allam / Qossai · (none)
- **Our note:** (none)
- **Viva Notes:**

We can every tuesday at 10:00 AM

## T6. Review the decision log

- **Owner / due:** Allam / Qossai · Next week
- **Our note:** (none)
- **Viva Notes:**

Done

## T7. Outstanding module documentation

- **Owner / due:** Allam · (none)
- **Our note:** Ticket template, events, resource management, wallet, resale, pricing/upgrades/orders, accreditation
  and virtual queue, BI and approvals, licensing, DAM and gaming, asset/sandbox/API, device template, CMS components
- **Viva Notes:**

All the documentation has been shared earlier during the workshops. Could you please review those workshop documents and let us know if you need any specific documentation

## T8. Hardware: vendor choices, specifications and test devices

- **Owner / due:** Qossai / Allam · (none)
- **Our note:** Not on your hardware list v1.1 yet: POS terminal (make, model, OS), kitchen display ('decide later')
  and kitchen printers, card payment terminals, SMS and email senders; still open in it: NFC reader ('China'), RFID
  reader (Kaptur), wristband chip type; confirm Chainway C66 for the staff app and flying POS; gaming reader vendor,
  turnstile SDKs, signature pad; ship test devices to Softlabs India. Details in the Decisions Register.
- **Viva Notes:**

All the details has been updated in the Decision Register. Kindly refer it and let us know in case of any other clarifications

## T9. Sizing benchmarks and data residency

- **Owner / due:** Qossai / Allam · (none)
- **Our note:** Concurrent users and volumes per venue size; regions beyond the UAE; banking and messaging
  integration documents
- **Viva Notes:**

TICVAI must support flexible, elastic infrastructure sizing across different venue profiles—from small sites with only 1–2 POS/access points and low B2C traffic to major football matches, concerts and events with 30,000–50,000+ attendees. Infrastructure and database capacity should start according to the tenant/site requirement and scale based on actual traffic, concurrency, transactions and data growth without fundamental application redesign.

For major-event sizing, use 1,000–2,000 active concurrent B2C users as the expected peak and 3,000 as the initial performance acceptance benchmark. High-demand onsales may generate 50,000+ simultaneous incoming visitors; therefore, an independently scalable edge-level Virtual Waiting Room/Queue Management layer should absorb excess demand and progressively admit customers into B2C. The 3,000-user benchmark must not be treated as a hard architectural limit.

The solution must support horizontal/auto-scaling, scalable database/storage, CDN/WAF/DDoS/bot protection, multi-tenant workload isolation and concurrency-safe ticket/seat inventory. Load testing should cover both small-site and major-event scenarios. Initial production data residency will be UAE, with architecture supporting future tenant-specific regional deployments where required.

## T10. Policy decisions

- **Owner / due:** Qossai / Allam · (none)
- **Our note:** Shift-close cash variance; B2B tickets under dynamic QR; F&B quick service vs dine-in; B2B portal
  option
- **Viva Notes:**

Policy decisions:
1. Shift-close cash variance: The system should support configurable cash variance tolerance. Variances within the permitted threshold may be closed with mandatory reason capture. Variances exceeding the threshold should require supervisor/manager approval. All variances and approvals must be fully audited and reported.
2. B2B tickets under Dynamic QR: Dynamic QR should be supported for B2B-issued tickets where the distribution channel supports digital tickets. Static QR/printable tickets should remain configurable where required by the B2B channel or venue.
3. F&B Quick Service vs Dine-in: Both operating modes should be supported and configurable by outlet. Quick Service should follow order → payment → preparation → collection, while Dine-in should support tables, open orders/tabs, multiple order rounds, kitchen routing, serving and final settlement.

---

**Note (filed 6 October 2026).** T2, T3, T7 and T8 point at the Decisions Register and the workshop documents
rather than answering in the tracker; those answers are filed when the register is received. T10 named four
policies in our note and the client answered three: the B2B portal option has no answer yet. Where the package
takes up an answer, the change entry cites this file (CHG-R4-017 onward).
