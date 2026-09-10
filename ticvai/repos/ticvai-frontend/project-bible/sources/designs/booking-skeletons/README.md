# TICVAI — white-label booking skeletons

One file, five venue types, 34 booking flows. Open `TICVAI Booking Skeletons.dc.html`
in a browser — no build step, no server, no dependencies beyond `support.js` (the
runtime) and the `logos/` folder.

---

## What this is

A white-label booking engine skeleton. Venues own their own home page; "Buy tickets"
redirects into this engine, which is re-skinned per venue. The engine's **structure**
is fixed; the **brand, palette, type, density, layout and flow** are configuration.

The design proves three things:

1. One step spine covers every vertical.
2. Every screen is composed from a small set of reusable layout modules, so a new
   flow is a data entry — not new UI.
3. All theming is data, extractable from a client's logo.

---

## Step spine

```
Select  →  Seats (only if the flow needs them)  →  Extras  →  Details  →  Payment  →  Confirmed
```

- **Seats** appears only when the flow declares `seats: true`.
- **Extras** is skippable per the client decision of 21 Aug — set `extrasStep: Never`
  (or let Auto drop it) and the flow collapses to Selection → Cart → Checkout.
- **Payment** has four modes: `full`, `deposit`, `none` (nothing charged) and
  `invoice` (quote requested, no card).
- Step labels, titles, subheads, buttons, empty states and confirmation copy all come
  from one per-vertical / per-flow vocabulary map (`vocab()`), so a food order never
  says "tickets".

---

## The five skeletons and their flows

### Theme park — Summit Peaks (7 flows)
Dated day pass · Timed entry / capacity slots · Multi-park combo · Annual pass /
membership · Fast-track upgrade · Height & age eligibility gate · Group / school booking

### Water park — Coastal Aqua (5 flows)
Day pass · Timed session · Cabana & locker rentals · Swim ability & height gate ·
Group booking

### Stadium — Union Arena (8 flows)
Zone → seat map · Direct interactive seat map · Best available · Season ticket /
multi-match · Hospitality & VIP box · Accessible seating · Deferred seat assignment ·
Group block booking

### Theatre — Grand Playhouse (6 flows)
Showtime + language/format matrix · Play with numbered seats · Best available ·
Season subscription · Accessible seating · Group block booking

### Dining — Saffron Table (9 flows)
Table reservation · Prepaid set menu · Ticketed dinner event · Deposit-only hold ·
Deals & offer redemption · Waitlist / join queue · **Takeaway — collect** ·
**Delivery** · Large group enquiry

Dining opens with a service gate (Dine in / Takeaway / Delivery / Supper club) that
switches the flow before the guest sees a menu.

---

## Layout modules

Each flow's `modules()` returns an ordered list. Every module is one of these; add a
flow by composing them, not by writing screens.

| Module | What it renders | Used by |
| --- | --- | --- |
| `chips` | Row of two-line chips (dates, windows, times, party size) | everywhere |
| `counters` | Rows with price and a −/+ stepper | guest types, seat quantities |
| `cards` | Photo product grid with rating, badge, struck-through was-price | passes, combos, cabanas, films |
| `expand` | In-page expandable ticket-type rows revealing counters | park & water day passes |
| `menu` | Category filter + ecommerce dish grid with Add → stepper | takeaway, delivery |
| `sessions` | Capacity grid: time, fill bar, % sold, demand-priced | water park sessions |
| `heights` | Height bands with proportional rulers and what each can ride | water park guests |
| `benefits` | Tier cards: big price, "What you get" checklist, savings, exclusions | memberships, seasons, hospitality, fast-track |
| `event` | Single hero fixture: photo, kicker, meta row, price-from, alt dates | all stadium flows |
| `matrix` | Language × format grid | cinema |
| `spec` | Key/value spec table | rider requirements, cabana inclusions, collection |
| `timeline` | Numbered "what happens next" steps with timings | group, block, enquiry, waitlist, delivery, deferred seats |
| `form` | Auto-laid-out field grid (text/select/area/upload/check/signature) | enquiries, addresses, access needs |
| `note` | Tinted callout with an optional action | nudges, policy notes |

Seat maps come in two modes: `rows` (lettered rows, aisles, price bands) and `tables`
(round tables / cabanas on a plan).

---

## Cross-sell

All six placements are live:

1. Inline `note` nudge on the selection step
2. Dedicated Extras step
3. Slide-in panel when a product card is tapped
4. "Often added" in the cart sidebar
5. Combo suggestion on the payment step
6. Post-payment upsell on the confirmation

---

## Compulsory information

The Details step is generated from each flow's `requires` list — nothing more is
asked than the flow needs:

`lead` (contact) · `guests` (per-guest names and ages) · `id` (Emirates ID / passport
+ upload) · `waiver` (health declaration + signature) · `cert` (certification upload)
· `plate` (vehicle) · `consent` (terms + marketing)

---

## Tweaks

Exposed as props on the root component; the host renders them as a panel.

**Brand** — `palette` (18 presets or Auto-per-venue) · `primary` · `accent` · `fontPair`
**Background** — `bgTone` (29 grounds, incl. brand- and accent-derived) · `bg` · `surface` · `ground`
**Shape** — `radius` · `buttonStyle` (solid / outline / pill) · `density`
**Layout** — `embedMode` (full page vs B2C-embedded) · `extrasStep` · `layout` (cart sidebar vs single column) · `progressStyle` (bar / numbered / dots) · `showConfig`
**Locale** — `currency` (AED / SAR / USD / INR / GBP) · `rtl`

Each venue also carries its own default palette, so switching vertical re-skins the
whole engine. Anything left on Auto follows the venue; anything set overrides globally.

### Theming mechanics

`theme()` resolves a token set and writes it to `document.documentElement` as CSS
custom properties. Surfaces, borders and the three ink levels are *mixed* from the
chosen background, so an arbitrary ground still gets correct contrast. The template
only ever references `var(--token, fallback)`.

Tokens: `--brand --accent --bg --surface --surface-2 --ink --ink-2 --ink-3 --line
--r --r-sm --sp --sp2 --sp3 --sp4 --font-h --font-b --btn-bg --btn-fg --btn-bd --btn-r
--tint --tint-2 --ring --sh-sm --sh-md --sh-lg --img`

### Palette from a logo

Upload a logo (or pick a sample) in the config bar. The engine samples the image on a
canvas, buckets colours, weights frequency by saturation so the brand colour beats the
greys, and derives an accent — either a second distinct hue from the logo or a
computed complement. Three apply modes: light ground, dark ground, duotone.

It also generates **light and dark versions of the logo itself**: neutral pixels are
remapped toward white or near-black while brand colours are left alone, so the same
mark works on either ground. The venue header picks the right one automatically.

Note: extraction requires a same-origin image. Uploads and files in `logos/` work;
hotlinked remote images cannot be read pixel-by-pixel by the browser.

---

## Sources this was built from

- Meeting minutes, `_dump/mom-markdown-transcriptions/` in the `ticvai` repo —
  Ticketing & Product Configuration (25 Aug) and Seat Management (21 Aug). These
  supplied ticket types (open-dated, dated/special-day, time-slot, multi-day
  consecutive vs flexible, membership, lesson-based), validity rules (fixed, rolling,
  first-use activation, blockout dates), the guest-category × tier × residency matrix,
  entitlements, the six-per-transaction purchase limit, the three seat-selection
  scenarios, the four section types, seat-hold auto-release, tranche inventory release,
  deferred seat assignment, and the confirmed B2C checkout pattern.
- The POS terminal reference HTML, for visual language: dark ground, teal, elevated
  cards, photo tiles with badges and ratings, heavy price type.
- Venue logos from the client's asset pack.

Photography is Unsplash, referenced by URL and assigned per vertical from a curated
pool so no two tiles on screen repeat. Swap `pools()` for the client's own library.

---

## Not yet built

- **White-label process flow board** — a board for picking the layout per step and
  editing it. Scoped, not built.
- **More venue logos** — only the five from the asset pack are present. Drop more into
  `logos/` and add a chip; both variants generate at runtime.
- Flow depth is the spine for all 34. Deepening any individual flow (live seat-map
  inventory, real pricing rules, wallet mechanics) is the next pass.

---

## Files

```
TICVAI Booking Skeletons.dc.html   the design — template + logic + tweak metadata
support.js                          runtime (do not edit)
logos/                              venue logos used by the palette extractor
README.md                           this file
uploads/                            reference material supplied by the client
```
