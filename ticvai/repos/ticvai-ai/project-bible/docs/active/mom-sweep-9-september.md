# What the minutes already decided — 9 September 2026

**Every minute in `sources/mom/` read against every open conflict and every screen question.**
22 minutes, 60,647 words, against 16 open conflicts and 74 `openQuestions`.

The reason to do this is that it has already gone wrong twice in a week. `BO-006` sat on a question
the 14 August minute answered three weeks earlier. `P11`'s eight screens were recorded as having
*zero MoM coverage* for a workshop that had already happened. **Both cost the work twice — once to
raise, once to withdraw** — and eight minutes were added to the package on 8 September, six of them
the most recent sessions on the project. Everything concluded before that date was concluded
without them.

Tools: `tools/mine-moms.py` (open items against the corpus) and `tools/extract-mom-decisions.py`
(every labelled outcome). Output in `sources/mom-corpus.json` and `sources/mom-decisions.json`.

---

## 1 · Two conflicts should close, and one has been open on a clerical error

### CF-164 — the F&B workshop happened. Twice.

**The entry says the F&B, Retail, Procurement and Inventory workshop is outstanding in three
consecutive MoMs. It is not outstanding and it was not outstanding when the entry was raised.**

| Minute | Covered |
|---|---|
| **18 August** | F&B POS backend, outlet setup, recipes and BOM, kitchen stations and KDS routing, menu builder, modifiers and combos, table management, course-wise ordering, procurement |
| **19 August** | Retail command centre, store setup, product catalogue and variants, price book, bundles and promotions, database architecture, inventory requisitions and transfers, stock counts, RFID, returns and refunds, omni-channel fulfilment |

Both are full technical workshops with decisions recorded in them — outlet-level configuration
agreed for F&B *and* Retail, inventory confirmed at outlet level, stock reservable and allocated
per sales channel, variant attributes configurable, shipping rates manual rather than
courier-API — plus open actions on RFID specifications and on the database comparison.

**The 20 August note is a filing-label error, not a missing workshop.** It reads *"This recording
is filed under 'F&B, Retail, Procurement & Inventory,' but the session actually covered CRM…"* —
and the 19 August minute's §4.10 says the CRM module *"will require a dedicated session,
tentatively the next day."* **The 20 August session was always going to be CRM.** Somebody
mislabelled the recording, wrote a correction saying the F&B workshop remained outstanding, and
the 21 August minute repeated it. The register has carried it since.

**This also corrects CF-171's premise.** It argues that *"the F&B/Retail/Procurement/Inventory
workshop that is outstanding in three consecutive MoMs is exactly the material nobody has drafted
from."* The workshop happened. The 26 uncited packs are still uncited — **but that is a drafting
gap, not a workshop gap**, and the remedy is different: nobody has to be scheduled, somebody has to
read them.

### CF-21 — the last remaining workshop ran on 7 September

The entry was split three ways on 18 August and reduced to one line: *"Accreditation still needs a
session. So one workshop remains, not three."* That session ran on **7 September** and covered
the application directory, form builder, categories and programme setup, document validation and
OCR auto-fill, identity verification and duplicate prevention, the approval workflow with SLA and
escalations, credential issuance and lifecycle, notifications, bulk operations, analytics, channel
placement and an accreditation API.

**CF-21 is the register's only "blocked work left on the project". Nothing is blocked.**

---

## 2 · Three conflicts change shape

**CF-165 — decided on 20 August, still unbuilt.** The entry says retention and archival *"are not
modelled anywhere."* The decision exists: *"data retention/archival periods (e.g., 3–5 years of
'live' data before archival) will be configurable per tenant/venue at setup time, with a system
default that administrators can override."* **The conflict changes from undecided to unbuilt**,
which is a different owner and a different remedy — it is now a column and a policy, not a
conversation.

**CF-64 — narrowed by the same sentence.** The 87 "configurable" retention requirements now have a
stated default range and an override model. The RPO floor question is untouched and still stands.

**CF-127 — narrowed to the scanner.** 1 September: *"Cookie policy management supports a
configurable consent banner (accept/reject) per website, with certain cookies flagged as mandatory
(non-rejectable) and others optional, templated and configurable within the system."* So the banner
and the categorisation are being built. **The minute does not mention site scanning or script
blocking**, which the entry correctly identifies as the part that makes this a product rather than
a form. Build-or-buy narrows to those two.

---

## 3 · The 70% in ADR-0042 has an input coming

**CF-162's three deployment scenarios are still owed** — the 24 August request is in the minute
verbatim. But 1 September adds the thing ADR-0042 is actually waiting for:

> asked Qossai and Allam for concrete venue-scenario benchmarks — expected requests-per-second for
> events, and daily transaction volumes by venue type — to translate into a recommended AWS/GCP
> configuration and cost estimate, rather than working only from the earlier placeholder figures.

**ADR-0042's open threshold is 70% of `max_connections` sustained over three days in a rolling
seven, and the reason it is a sign-off rather than arithmetic is that nobody has the load numbers.**
These are those numbers. The ADR should not be signed off before they arrive, and it should say so.

---

## 4 · Thirty-seven outcomes from the eight new minutes

`sources/mom-decisions.json` holds 86 labelled outcomes across 13 minutes; 37 come from the eight
added on 8 September. **Most are already absorbed** — checked against the contracts rather than
assumed, because that is the whole failure mode this document exists to correct. Three examples of
things *not* to add:

  **Tax on the pre-discount base** (1 September, the Egypt case) is `TaxCode.discountsAreTaxInclusive`
  — *"True reduces the taxable base by the discount. False applies tax to the undiscounted…"*
  Already modelled, already per tax code, which is already per jurisdiction.

  **Chart-of-account posting for every financial transaction** (27 August) is `Account`,
  `AccountMapping` and `PostingEventType`, which already carries `walletReceived`.

  **Wallet balance as a liability recognised on consumption** (27 August) is `RecognitionSchedule`
  and `DeferredRevenueReport`, and the expiry case is `PostingEventType.breakageRevenue`.

### What is genuinely not in the package

**Wallet validity is mandatory and the schema says it is optional.** 27 August: *"every wallet
requires a validity period; it cannot remain open indefinitely."* `Wallet.expiresAt` is
`nullable: true`. **This is a direct, checkable contradiction between a decision and a contract**,
and it is the cheapest thing on this list to fix.

**The expiry sweep has an accounting entry and no destination.** *"Any remaining balance is
automatically swept to a finance-designated account, per policy"* — and this applies to monetary
balances and non-monetary credits, not only points. `WalletTransactionKind.expiry` and
`breakageRevenue` record that it happened; **nothing says which account, after how long, or under
whose policy.**

**Guest-configurable funding is absent.** *"Both auto-reload and recurring funding schedules should
be configurable by the guest themselves via the guest/web app, not only by venue admins."* No
operation and no field.

**Guest-created family profiles with spending limits are absent.** *"Guests can create
family-member profiles themselves and configure spending limits directly from their own guest
account."* `WalletAllocation` looks close and is not it — that is a cross-cell ceiling on a
`guestLinkId`, not a family member a guest created.

**The six wallet types are a different axis from the five credit kinds.** Six were scoped on the
Softlabs side — attraction credit, game credit, rental credit, parking credit and others — and
`Wallet.credits[].kind` is `[cash, bonus, redemption, refund, goodwill]`. **Those are funding
sources; the six are spend categories.** A wallet holding parking credit and game credit needs both
axes, and modelling one as the other is how a guest spends their parking credit on a milkshake.

**A single centralised notification module was decided on 31 August** — *"rather than each module
building its own notification logic independently."* CF-140 lists a single notification service
(BL-052) among the delivery plan's own *Missing Components*. **It is no longer an open design
question**, and the register still reads as though it is.

**Scan means used, regardless of physical passage** (2 September) — a deliberate fraud-vector
decision, with genuine cases resolved manually from the scan-history log rather than by loosening
the rule. **This is a behavioural invariant that belongs in `access`**, and a screen or an
implementation that decides otherwise on its own is a security regression.

**Turnstile faults are pushed, not polled** (2 September) — devices send anti-passback attempts,
power loss and network loss to TICVAI over a TCP/IP API, *"rather than requiring TICVAI to poll or
independently detect."* TICVAI surfaces them as alerts and does not build fault-detection logic.
Bears directly on CF-33's vendor SDK question.

Also unabsorbed and smaller: price and configuration changes never apply retroactively to tickets
already sold (31 August); channel-specific pricing as a requirement rather than a capability
(31 August); automatic B2C→B2B inventory migration at a configured share (31 August); blocking
duplicate submissions on passport and Emirates ID (7 September); partial payment and deposit for
bulk school and corporate bookings (1 September); and upgrades completable in the guest app rather
than only at the counter (1 September).

---

## 5 · One open action that touches the database ADRs

**19 August, on Chinmay:** *"prepare a pros-and-cons comparison of the single-DB vs. multiple-DB
approaches (performance, reporting, offline sync) for further discussion."*

The minute records Allam proposing **one centralised database across all modules with a read-only
replica for reporting**, and Chinmay proposing **one database per module within a single instance**
for read/write segregation. The package has since decided something different again — a cell per
region, a database per tenant inside it (ADR-0038, ADR-0039, ADR-0043).

**Nothing here is being changed.** It is recorded because an action assigned in a workshop is still
open, the conversation it feeds has moved on without it, and the three ADRs would be easier to
defend if that comparison existed. **The decision itself is reserved** and stays that way.

---

## 6 · Twelve screen questions are stale, not open

22 of the 74 `openQuestions` have a minute discussing them, and nine of those already carry their
answers — `BO-006` and the eight `P11` screens, both recorded on 8 September.

**Twelve of the remainder are not questions at all.** All twelve are `P02`, all identical in shape:

> Inventory cites `GET /tickets` — no matching operation. Written before the contracts existed.

`GST-012 My Tickets` declares `listMyEntitlements`, `getEntitlement`, `transferOrderTickets`,
`getEntitlementCredential`, `getEntitlementHistory` and `listEntitlements`. **The operation exists;
it is not called `GET /tickets`.** The note records a path the page inventory invented before there
were contracts, and it was never retired when the contracts arrived. They should be deleted — they
are the only thing standing between six Wave 1 `P02` screens and a clean sheet for Design.

---

## 7 · The corpus is not what it says it is

**Only 8 of the 22 files in `sources/mom/` are Word documents.** Fourteen carry a `.docx` extension
over Markdown — eleven open `**Minutes`, three open with a table row — and the eight real ones are
exactly the eight added on 8 September.

Reading by extension raises `BadZipFile` on the first Markdown file and stops. **Read the first four
bytes.** It is recorded here because the failure mode is the week's recurring one: a tool that
silently sweeps a third of a corpus and reports success. `tools/mine-moms.py` checks the magic
bytes and handles both.

---

## What to do with this

**Close CF-164 and CF-21** — both on evidence in the minutes, and CF-21 is the register's only
claimed blocker.

**Re-word CF-165, CF-64 and CF-127** from undecided to unbuilt or narrowed, with the deciding
sentence quoted.

**Correct CF-171's premise** — the workshop is not outstanding; the packs are still undrafted.

**Note the benchmark request against ADR-0042** so the 70% is not signed off before the load
numbers land.

**Fix `Wallet.expiresAt`**, which contradicts a decision, and open the five wallet gaps as contract
work.

**Delete the twelve stale `P02` questions.**

None of this is applied yet.
