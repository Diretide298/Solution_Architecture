# Guest web and guest app — parity

**They should have near-identical functionality, and today they do not.** 25 capabilities are on
both, **five are web-only and 23 are app-only.**

Most of that gap is not a decision anybody made. It is where the wireframe boards happened to
draw more screens for one surface than the other.

---

## What the matrix actually says

**143 of 3,184 requirements name a guest surface at all** — 32 the website only, 89 the app only,
22 both. *(This paragraph said 54 until 17 August, which was neither the sum nor any of its parts.
An external audit caught it: 32 + 89 + 22 is 143.)* **The overwhelming majority are platform-neutral**, which is the correct reading: a
requirement that says "the system shall allow guests to transfer tickets" is a requirement for
both surfaces unless it says otherwise.

**The default should therefore be parity, and a difference should need a reason.**

---

## Where the matrix contradicts what we built

| | We have | The matrix says |
|---|---|---|
| **Multi-currency** | **App only** (`GST-044`) | **Website.** 2.6.33: *"Website should be able to display multi currency and users should be able to switch the prices"*. 2.9.1: *"display prices in multiple currencies in the B2C portal for guests comparison"* |

**This is backwards.** Multi-currency display is specified twice for the website and never for
the app, and we built it on the app and not the website.

The reasoning behind the requirement is sound: **the website is where an overseas guest compares
prices before travelling.** Someone already in the venue with the app installed has largely
decided. Both requirements are explicit that **the sale settles in base currency regardless**
(CF-37) — the display is a comparison aid, not a pricing feature.

**`GST-044` should exist on the website first**, and on the app second or not at all.

---

## Where a screen exists and no requirement does

| | Screens | Requirement |
|---|---|---|
| **Itinerary planning** | **`GST-051` Plan Your Adventure · `GST-052` Suggested Itineraries · `GST-053` Build Your Own · `GST-054` AI Optimized · `GST-059` Plan My Day** | **One requirement, 4.1.1, and it is about external operators booking time-based services — not guest itinerary planning at all** |

**Five screens, no provenance.** They come from the design boards rather than the matrix, and
`GST-054` additionally assumes AI capability that sits in the parked 194.

To be clear about what "Plan Your Adventure" and "Plan My Day" are: **`GST-051` starts a plan
before the visit and `GST-059` shows it in progress during the visit.** They are two halves of
one capability, not two capabilities — and neither is asked for.

This is CF-40 repeating: a feature in the design that nobody can trace to a requirement, and the
question is whether the client wants it or whether a designer liked it.

**Also unsourced:** `GST-050` Cabana booking, `GST-057` Accessibility information,
`GST-038` Digital Companion Mode.

---

## Where the app is genuinely right to be ahead

**In-venue capabilities belong on a phone in a pocket, and putting them on a website would be
building something nobody opens.**

`GST-021` interactive map · `GST-022` wait times · `GST-023` virtual queue · `GST-024` F&B
ordering to a location · `GST-025` order tracking · `GST-030` in-venue notifications ·
`GST-055` dynamic QR · `GST-062` shop-and-drop collection.

**None of these is a parity gap.** A guest standing at a ride does not open a laptop.

---

## Where the website is missing something it should have

| | |
|---|---|
| **Ticket transfer** — `GST-014` | Nine requirements. **A guest who bought on a laptop for their family will send tickets from a laptop** |
| **Reservations** — `GST-016` | Booked on the web and viewable only on the app |
| **Offers** — `GST-037` | Promotions displayed in one place and not the other |
| **Retail browse** — `GST-026` | Merchandise pre-purchase is a web behaviour as much as an app one |
| **Lost and found** — `GST-034` | Reported after leaving, which is usually from a computer |

---

## Where the app is missing something the web has

| | |
|---|---|
| **`WEB-003` Search** | The app browses by category and has no search. **On a venue with 200 products that is a real gap** |
| **`WEB-024` Loyalty** | 158 loyalty requirements, 11 naming the app, and no loyalty screen on it |
| **`WEB-027` Newsletter** | Consent capture, and the app is where a guest is most reachable |
| **`WEB-014` Payment link** | Correctly web-only — a link from an email opens a browser |
| **`WEB-011` Guest details** | Folded into `GST-009` on the app. Not a gap |

---

## Resolved 17 August

**Nine screens added, two operations written, eighteen marked guest-callable.**

| Added to guest web | Mirrors |
|---|---|
| `WEB-030` Ticket Transfer | `GST-014` |
| `WEB-031` My Reservations | `GST-016` |
| `WEB-032` Offers & Promotions | `GST-037` |
| `WEB-033` Shop | `GST-026` |
| `WEB-034` Lost & Found | `GST-034` |
| **`WEB-035` Multi-Currency & Pricing** | **CF-91, then CF-111 — the matrix asks for it on the web and the storyboard draws it on the app. Both surfaces carry it** |

| Added to guest app | Mirrors |
|---|---|
| `GST-063` Search | `WEB-003` |
| `GST-064` Loyalty & Rewards | `WEB-024` |
| `GST-065` Newsletter & Preferences | `WEB-027` |

### Two operations did not exist

**`searchCatalogue`** — the app could browse by category and not search at all. Distinct from
`semanticSearch`, which is AI and retrieves from documents: this is keyword search over the
sellable catalogue, and **it works with no AI configured**, because a venue without an assistant
still needs a search box. Results show sold-out items rather than filtering them, since a guest
searching for a closed attraction should learn it is closed and not that it does not exist.

**`getLoyaltyPosition`** — 158 loyalty requirements and **no operation returned a guest their own
balance**. Returns points, tier, and how far from the next one, plus what expires and when.
**Points that lapse unannounced are a complaint**, and the date is what lets an interface warn.

### Eighteen operations were staff-only and should not have been

`listLoyaltyProgrammes`, `getWallet`, `listReservations`, `cancelReservation`, `listPromotions`,
`listMerchandise`, `listCases`, `listFxRates` and others. **The permission stays for staff acting
on a guest's behalf; a guest session resolves the same operation to their own data** — the rule
already used for `getGuestProfile`.

`cancelReservation` is the sharpest: a guest could make a reservation on the web and not cancel
it.

## What remains



**Parity is the default and a difference needs a stated reason.** Three groups:

**In-venue only, app by design** — 8 capabilities. No action.

**Should be on both** — ticket transfer, reservations, offers, retail, lost and found, search,
loyalty, newsletter. **8 capabilities, and each is a screen rather than a contract**, because
the operations already exist.

**Multi-currency on both** — the matrix asks for it on the web (2.6.33, 2.9.1) and guest storyboard board 7 draws it on the app. **Both are client documents**, and parity is the default this document argues for everywhere else (CF-111).

**Raise with the client** — the five itinerary screens, cabana booking, accessibility
information and companion mode. **Eight screens with no requirement behind them**, and the
question is whether they were agreed somewhere we have not seen or whether they are design
enthusiasm.
