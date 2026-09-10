# Audit — `TICVAI POS Terminal (1) 1.html`

**9 September 2026.** The interactive POS prototype delivered by the team, audited against
`screens/P04-point-of-sale.yaml` (24 screens, 214 operation declarations, 118 unique operations),
`screens/_components.yaml`, `screens/_schema.yaml` and the thirteen `platforms: [P04]` flows.

**Every correction below is additive.** Nothing in this document asks for a line to be deleted or
a screen to be redrawn. The file is the best artefact in the package and the corrections are the
things a frontend team or an AI agent cannot get from it *yet*.

---

## 0 · What the file actually is

| | |
|---|---|
| On disk | 5.67 MB, 393 lines |
| Shape | Claude Design bundle — `__bundler/manifest` (4.67 MB of fonts and images) + `__bundler/template` (951 KB) |
| Inside the template | 315 KB of `x-dc` markup + **618 KB of JavaScript** in one `<script type="text/x-dc">` |
| Markup directives | 115 `sc-if`, 105 `sc-for`, **217 `onClick` handlers**, 13 `onChange` |
| Artboard | **One** device frame, 1620 × 1080, chromed as *TERMINAL POS-014 · AQUA PARK GATE A* |
| Author-exposed props | `startScreen` (enum), `cartHold` (bool), `cartHoldSeconds` (int, 60–900) |

**This is not a board. It is a running application.** The distinction matters for everything that
follows: the twenty other boards in `wireframes/` are N static frames per platform; this is one
frame with a state machine behind it. It is the thing the package has been missing, and it is why
`derive-wireframes.py` cannot produce it and must not be pointed at P04 again.

**It is genuinely good.** Before the corrections, what it gets right that no other artefact does:

- **A real permission model.** `ROLE_ORDER` → `ROLE_BASE_PERMS` → cumulative `ROLE_PERMISSIONS`,
  six roles, and `hasPerm()` guarding eleven distinct actions. A cashier who lacks `void.standard`
  is stopped and offered a supervisor PIN, and **the escalation writes an audit record naming user,
  role, action, transaction and whether it was self-authorised**. This is ADR-0002 implemented, not
  illustrated.
- **The payment lifecycle including the outcome nobody draws.** `payStage` runs
  `null → processing → checking → unknown | completed | failed`, with `payIdemKey`, `payAuthRef`,
  `payGatewayRef` and `payTrueOutcome` held separately. **`unknown` is the state POS-005 exists for**
  — the contract note says *"a terminal that charged a card and never returned a response is the
  normal failure"* — and this file is the only artefact in the package that draws it.
- **Offline as a first-class screen.** `netStatus`, a `syncQueue` with per-item status meta, a
  manual sync control and a `conflictModal`. ADR-0013 made visible.
- **Tax read from configuration.** `TAX_RULES` and `VENUE_TAX_CONFIG`, with the comment
  *"consumed by the POS, never hardcoded into a screen"*.
- **Inventory that can actually conflict.** `stockQty` / `stockReserved` / `inventoryLedger`, with
  check → reserve → deduct → release/return run for real on one SKU.

---

## 1 · Coverage against the P04 contract

**16 prototype surfaces against 24 declared screens.** Fifteen contract screens are covered whole
or in part; **nine have no surface at all**; **four prototype surfaces are not declared anywhere in
P04**.

### 1.1 Covered

| Prototype surface | Contract screen | Note |
|---|---|---|
| `login` + `float` | POS-001 Begin Shift | Both halves. The float is non-editable after open, as the client mockup requires |
| `tickets` | POS-002 Sell — Ticket Catalogue | 41 declared operations, the busiest screen in the package |
| drawer `dstep: datetime` | POS-003 Sell — Timed Entry | **Drawn as an overlay on POS-002, not a page** — which is the 8 September drawer decision, arrived at independently |
| drawer `dstep: seats` | POS-004 Sell — Seat Map | `SEATMAPS` + `ARENA_SECTIONS`, both grid and sectioned |
| `checkout` | POS-005 Payment | See §0 on `payStage` |
| modal `held` | POS-006 Held Orders | Modal rather than screen; `heldList`, recall restores cart and `cartAt` |
| `closeout` | POS-007 Close Shift | `closeStep: count → variance → summary`, supervisor PIN, `closeLocked` |
| `reports` | POS-008 Reports | Cross-outlet revenue, footfall, terminal health |
| `refunds` | POS-011 Returns, Refunds & Exchanges | **Refund only.** See C-07 |
| `queue` | POS-012 Omnichannel Order & Fulfilment | Aggregator partners, drivers, cancel reasons — a close match |
| `sync` | POS-013 Mobile POS, Event Sales & Offline | Offline half only; `EVENTPLANS` sits under `tickets` |
| modal `disc` + `pinAsk` | POS-014 Sales Exceptions & Controls | Discount, void and override with audit. Partial — see C-08 |
| `setup` | POS-016 Till Configuration + POS-024 Outlet Setup | One screen doing two contract screens' work |
| `fnb` | POS-021 Sell — Food & Drink | |
| `retail` | POS-023 Sell — Merchandise | |

### 1.2 Declared and not drawn — **nine screens**

| Screen | Declared ops | What is missing |
|---|---|---|
| **POS-009** Staff Roster | 16 | Nothing in the file. `roster` appears zero times |
| **POS-010** Add to Existing Ticket | 5 | No way to attach a line to a sale already settled |
| **POS-015** Cash Operations Dashboard | 2 | `home` is a *sales* board; there is no cash position view |
| **POS-017** Cash In / Cash Out | 1 | `paidIn`, `payout`, `cashIn` — zero occurrences |
| **POS-018** Safe Drop & Cash Transfer | 5 | `safeDrop` — zero occurrences. A till that cannot drop to the safe accumulates unbounded cash |
| **POS-019** Shift Templates & Policies | 3 | |
| **POS-020** Shift Exceptions & Alerts | 5 | `POS-002` and `POS-007` both declare an exit to it |
| **POS-022** Send to Kitchen | 4 | The F&B subtitle says *"kitchen fires on payment"* and `kds` exists only as a hardware status light. **The KDS handover is asserted and never shown** |
| **POS-013** (event-sales half) | 8 | `EVENTPLANS`/`EVTIERS` exist but no mobile or event-sales surface |

### 1.3 Drawn and not declared — **four surfaces**

| Surface | Where the package puts it today |
|---|---|
| `home` — *Sales board* | Nowhere. A shift dashboard is not POS-015 (cash) and not POS-008 (reports) |
| `receipt` — post-sale, 12-second auto-return with a pause control | Nowhere. `reprintReceipt` hangs off POS-005 |
| `tables` — floor plan, reservations, waitlist, coursing | **P06** as EMP-052, 053, 054, 055, 056, 058, 059, 060 |
| `guests` — identify, loyalty, wallet top-up, enrol | **P01/P02** as WEB-021, WEB-043, GST-011, GST-036 |

**The last two are the real question in this audit.** The package's own rule, written on POS-005 on
24 August, is that *"a till does not navigate to a back office and a guest app does not navigate to
either — those are device handovers"*. The prototype puts eight P06 screens and four guest screens
**on the till**, which is either correct (a table-service till *is* the floor plan) or a boundary
violation. It cannot be both, and **no artefact currently records which**.

---

## 2 · Corrections

Numbered so they can be tracked. **All additive.**

### C-01 · There is no machine-readable identity on anything *(blocking, for the AI-agent goal)*

`data-*` attributes in the markup: **0**. `aria-*`: **0**. Screen IDs: **0** — the only `POS-0xx`
string in the file is the terminal's asset number in the chrome. Operation IDs: **0** — not one of
the 118 operations P04 declares is named anywhere.

A developer, or an agent, reading this file can see *that* pressing Charge moves to a receipt. It
cannot learn that this is `POS-005 → POS-005#receipt`, driven by `createPayment` in
`contracts/orders.yaml`, invalidating `listRetailSales`. **That join is the entire value of the
package and the prototype does not carry it.**

**Correction.** Every screen root and every interactive element gains attributes taken from the
contract:

    data-screen="POS-005"            data-op="createPayment"
    data-state="payStage:processing" data-contract="orders"
    data-to="POS-005#receipt"        data-carries="orderId,paymentId,tenderCurrency"
    data-guard="payment.reversal"    data-overlay="held"

Plus one sidecar `P04.meta.json` holding the same graph in one place, so an agent reads a small
index instead of parsing 951 KB of template.

### C-02 · The state machines are real and undeclared

Five machines run in this file and none is written down anywhere a person or a tool can read:

| Machine | States |
|---|---|
| `screen` | login, float, home, tickets, fnb, tables, retail, queue, guests, refunds, sync, reports, setup, checkout, receipt, closeout |
| `payStage` | null → processing → checking → **unknown** \| completed \| failed |
| `closeStep` | count → variance → summary |
| `dstep` (the sell drawer) | detail → datetime → seats → qty → done |
| `reversalStage` | requested → processing → done |
| `netStatus` | online ⇄ offline |

**`screens/_schema.yaml` cannot express any of them.** Its `states` block is a fixed map of five
load states — `loading`, `empty`, `error`, `offline`, `denied` — which is a *rendering* vocabulary,
not a *process* one. **This is the schema gap the whole exercise turns on.**

**Correction.** Add a `machine` block to the screen schema and populate it for all 24 P04 screens
from this file. Do not lose `unknown`: it is the most valuable state in the package.

### C-03 · Transitions have no trigger and carry no payload

`navigation.exitTo` on POS-002 lists eleven targets. **It does not say what the cashier presses to
reach any of them, nor what travels with them.** Across the package: **2,684 declared edges, zero
triggers, zero payloads.** The prototype knows all of it — `goCheckout()` carries the cart and
resets `tendered`/`tendStr`; `recall(i)` restores `cart` and `cartAt` and clears `holdBonus` — and
none of it is recoverable without reading the JavaScript.

**Correction.** A `navigation.transitions[]` block: `to`, `trigger`, `operation`, `carries[]`,
`guard`, `back`, `crossesDevice`. Derived where a flow already walks the edge (275 ordered screen
pairs across 94 flows), authored where it does not.

### C-04 · No foreign currency, and POS-005 says this is the one screen that takes it

`fxRate`: 0 occurrences. `tenderCurrency`: 0. `currency`: 0. Every amount is AED (103 hits) through
`money()`, hardcoded to `en-AE`.

The POS-005 note is explicit: *"**The one surface that takes foreign cash** (4.6.11). Records
`tenderCurrency`, `tenderAmount` and the `fxRate` applied, and **gives change in base currency
only** — a till giving change in five currencies needs five floats and the variance becomes
unattributable."*

**And the data layer already has it.** `handoff/screen-index.json` lists `ledger.fx_rate` among
POS-005's reads. **The table exists, the operation reads it, and the only artefact a frontend
developer will look at does not know it is there.**

**Correction.** A currency selector on the cash tender path and an FX line on the receipt. Change
stays AED. `CLOSE_DENOMS` is already per-denomination, so foreign notes need their own denomination
group at close-out — not a second float.

### C-05 · The tip toggle exists and tipping does not

`flags.tips` is a Setup switch labelled *"Show a tip step on card payments"*. **There is no tip
step.** POS-005 declares `addTip` (`POST /payments/{paymentId}/tip`) and the contract note says *"A
tip posts to a liability, not to sales"* — so a tip is also missing from the Z-report and from
close-out reconciliation, where it must not appear as revenue.

**Correction.** Tip step after card authorisation, gated on `flags.tips`; tip total broken out
separately on the receipt and on `closeout`.

### C-06 · No RTL and no dark theme, both declared on the platform

`P04.directions: [ltr, rtl]` and `P04.themes: [light, dark]`. The file has **no `dir` attribute, no
`lang`, no Arabic, and one hardcoded light palette** (`--ink`, `--paper`, `--line` on the root div).

The schema is blunt about this: *"RTL is first-class, not a later localisation (CF-42). A platform
listing `rtl` has every layout mirrored, not merely translated."*

**Correction.** Two additive props — `dir` and `theme` — driving the existing custom properties and
a mirrored flex direction. **Not a translation pass**: the point is to prove the layout survives
mirroring, and Arabic label copy can stay lorem.

### C-07 · Refunds without exchanges

The screen is titled *Refund & void*; the contract screen is **POS-011 Returns, Refunds & Exchanges**.
`exchange`: 0 occurrences. An exchange is not two transactions — it is one with a price difference
either way, and the difference decides whether the till collects or refunds.

**Correction.** An exchange path on the refund screen, reusing `rfScope` and adding a
replacement-line picker. `REFUND_METHODS` already carries store credit, which is the third leg.

### C-08 · The exceptions surface is an audit log, not a control panel

POS-014 declares three operations for exceptions, controls **and operational alerts**. The prototype
has `audit[]`, `pinAsk`, `exception.approve` and an alert count in the chrome (`notifs: 3`) — but
the notification tray has no screen behind it and there is nowhere to *work* an exception.

**Correction.** Either give POS-014 a surface, or lift the audit ledger out of the refund screen and
make it that surface. The second is cheaper and the ledger is already built.

### C-09 · `startScreen` exposes 4 of 16 screens

`data-props` enumerates `login, home, reports, checkout`. A reviewer cannot open the file on `sync`,
`closeout`, `queue`, `tables`, `guests`, `refunds` or `setup` — the seven screens most likely to be
reviewed by the people who own them — and **the `unknown` payment state is unreachable entirely**.

**Correction.** Widen the enum to all 16, and add a `startStage` prop for the sub-state, so a link
can open the terminal on `checkout` with `payStage: unknown`.

### C-10 · Nothing is deep-linkable

No URL state, no anchors, no `#POS-005`. Every review comment has to begin *"sign in, add a ticket,
press Charge, wait for the timeout"*. On a 24-screen prototype with five machines behind it, **a
reviewer will not do that more than twice.**

**Correction.** Hash routing — `#/POS-005?payStage=unknown` — and a frame index listing all 24 with
a link into each. This also gives `check-wireframes.py` something it can verify.

### C-11 · Four undrawn component kinds this file could retire

Of the eight kinds in `_components.yaml` with no user, this prototype already draws four in
substance and could claim them: `toast` (`flash()` / `s.toast`), `modal` (six), `queuePosition`
(`QUEUE` + `STAGES`), `emptyState` (six in markup). The other four — `signaturePad`,
`duplicateMatch`, `assetTag`, `livePreview` — remain unclaimed and unasked.

### C-12 · Assets are inline base64 and the file is 5.67 MB

Ten `_imgN` JPEG data URIs in the script plus a 4.67 MB font-and-image manifest. Fifteen platforms
at this weight is an 85 MB `wireframes/` directory, and **it is already why two sessions failed to
read this file at all**.

**Correction.** A shared asset bundle referenced by id, as `board-data.js` and `support.js` already
do for the generated boards. Not urgent for P04 alone; **blocking before the other fourteen**.

---

## 3 · Summary

| | Count |
|---|---|
| Contract screens covered | 15 of 24 |
| Contract screens with no surface | **9** |
| Prototype surfaces not declared in P04 | **4** |
| Corrections raised | 12 |
| — blocking the AI-agent goal | C-01, C-02, C-03 |
| — blocking the fourteen-platform rebuild | C-12 |
| — behaviour the contract requires and the file lacks | C-04, C-05, C-06, C-07 |
| — reviewability | C-09, C-10 |
| Open boundary question | Tables and Guests on the till (§1.3) |

**Nothing here is a criticism of the drawing.** Nine of the twelve corrections are the package
failing to give the prototype a vocabulary — no way to declare a step machine, no way to declare
what a transition carries, no way to stamp a screen id. Those are fixed in `_schema.yaml` first and
in the artefact second, which is the order the plan follows.
