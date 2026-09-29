# B2B reseller portal, two options: brief

> **What:** the reseller portal (P10 Partner Web) drawn two ways, so the client can choose.
> **Decided:** MoM 29 September, section 3. Qossai proposed a POS-style portal for high-volume sellers. Muhamed accepted, and said supporting both per customer is fine if effort allows. Chinmay draws both; the client decides after review.
> **Screens:** the partner-facing P10 screens, PTR-001 to PTR-021. PTR-022 to PTR-051 are TICVAI's own partner-management screens (workshop boards WS21 to WS23) and are not part of this.
> **Platform:** P10 Partner Web, part of TICVAI Control. Desktop web. Online only. Light theme, left-to-right and right-to-left.

Read this file first. Then `BUNDLE.md` in this folder: every field of the 21 screens, the operations they call and their schemas. This brief outranks the bundle where they differ.

## The two options

**Same data, same operations, same permissions.** Only the shell and the selling flow differ. Anything one option can do, the other can too; a customer could run either.

### Option A: POS-style (for high-volume sellers)

For a hotel concierge desk or a travel agent selling many tickets a day.

- **After login, the sell screen.** The partner sees only the tickets assigned to them, at their partner prices. No browsing a storefront.
- **A fast sell grid**, like the till: product tiles, quantity, date and time where the product needs it, a running basket, one Sell button. Keyboard shortcuts. Repeat last sale.
- **Guest details at the end**: name, email or mobile, so the tickets can be sent.
- **Payment on account** against the partner's credit, or by card. **Optional cash drawer** for desks that take cash, on or off per partner.
- **Sent tickets**: a history of every ticket sent, with its status (sent, opened, used), and **Resend** to the same or a new email or mobile.
- **Balance**: credit limit, used, available, and what is due, always visible in the top bar, with a statement view.
- Left rail: Sell, Sent tickets, Orders, Balance and statements, Reports, Settings.

Reference: `sources/designs/TICVAI_POS_Terminal_client_approved.html`. Match its sell grid, basket, payment and receipt flow, and its density.

### Option B: website-style (a B2C-like storefront with a partner login)

For partners who sell less often and prefer to browse.

- **The guest website, signed in as a partner.** Same product pages, same booking steps, but partner prices, and a partner bar across the top: agency name, balance, statements.
- **Cart and checkout** as on the guest site. Payment on account or by card.
- **Bookings**: the partner's orders, each with its tickets, download and resend.
- **Statements**: balance, invoices, commission.
- **Quotes** for groups, which turn into bookings.

Reference: `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`. Match its storefront, product cards, booking steps and checkout.

## What both options must show

| need | screens | operations |
|---|---|---|
| Sign in, with MFA | PTR-001 | `login`, `createMfaChallenge`, `verifyMfaChallenge`, `getCurrentSession` |
| Home: today's sales, balance, recent orders | PTR-002 | `listOrders`, `getB2bCredit` |
| Company profile and users | PTR-003, PTR-020 | `getPrincipal`, `updatePrincipal`, `listDelegatedAccess`, `createDelegatedAccess` |
| Notifications | PTR-004 | `sendTransactionalMessage`, `getMessageStatus` |
| Assigned tickets and allocation | PTR-005 | `getChannelAllocations`, `listChannelCapacities` |
| Partner prices | PTR-006 | `listProducts`, `getProduct`, `listPriceLists`, `getPriceList`, `listPrices` |
| Availability | PTR-007 | `getAvailability` |
| Make a booking | PTR-008 | `createOrder`, `getOrder` |
| Group or bulk booking | PTR-009 | `createSeatBlock`, `allocateBlockedSeats`, `listSeatBlocks` |
| Cart and quote | PTR-010, PTR-011 | `getCart`, `addCartLine`, `updateCartLine`, `removeCartLine`, `checkoutCart`, `evaluatePromotions`, `listPartnerQuotes`, `createPartnerQuote` |
| Pay: on account or card | PTR-012 | `createPayment`, `capturePayment`, `inquirePaymentStatus` |
| Balance and credit | PTR-013 | `getB2bCredit` |
| Settlements and payments | PTR-014 | `listSettlements`, `getSettlement` |
| Orders | PTR-015 | `listOrders`, `getOrder`, `getOrderStatement` |
| Sent tickets: download and resend | PTR-016 | `reprintOrder`, `getOrder`, `sendTransactionalMessage` |
| Commission | PTR-017 | `getCommissionStatement`, `listPartnerAgreements` |
| Reports | PTR-018 | `listReports`, `runReport`, `askReportingQuestion` |
| API keys | PTR-019 | `listApiClients`, `createApiClient`, `rotateApiCredential`, `revokeApiCredential` |
| Support | PTR-021 | `listCases`, `createCase`, `addCaseMessage` |

The full list per screen is in `screens.json` (`apis`), with paths and schemas in `operations.json` and `schemas.json`.

## Be careful with the P10 specs

**The P10 screens are generated, not client-drawn.** Several list operations a partner must never have: `voidOrder`, `overrideCreditLimit`, `setB2bCreditLimit`, `ingestSettlementFile`, `resolveSettlementException`, `applyManualDiscount`. Those are TICVAI or venue staff actions. **Do not draw them as partner controls.** Where a screen lists one, leave it out and note it in `return/FINDINGS.md`. Filters labelled "Venue id", "Principal id" or "Shift id" are the generator's; replace them with what a partner would filter by (date, product, status, guest name).

**Known gaps. Draw them greyed and list them in FINDINGS.md; do not invent endpoints:**

- **Cash drawer for Option A.** There is no partner-side cash operation. The POS uses the shift contract (`recordNoSale`, `listCashMovements`), which is for venue staff.
- **Sent-ticket history.** No operation lists the messages sent for a partner's orders. `getMessageStatus` reads one message. The history can be built from `listOrders` with each order's delivery, but say so.
- **Delivery status "opened".** Nothing reports it. Show sent and used only, and note it.

## Seed data

A fictional UAE partner, for example "Palm Crescent Hotel, Dubai" (concierge desk) for Option A, and "Desert Rose Travel, Abu Dhabi" (travel agent) for Option B. Products from a fictional venue: day pass, fast track, cabana, dinner cruise. Prices in AED, partner price below the public price. Credit limit AED 50,000. No real client names or logos.

## Deliverable

Three files in `return/`:

1. `return/B2B-option-A.dc.html`: Option A, one self-contained working file.
2. `return/B2B-option-B.dc.html`: Option B, one self-contained working file.
3. `return/COMPARISON.md`: one page for the client. For each option: who it suits, how many clicks to sell two day passes to a walk-in guest, what the partner sees first, what it costs to build on top of the other (both share the same data and operations), and the risks. End with a recommendation and the option of offering both, set per partner.

In both working files: each screen opens from `#ptr-001` and so on, already populated; each declared state from `#<id>?state=<state>`. The element holding a screen carries `data-screen-label="<SCREEN ID> <Screen name>"`. Gate every control on its permission. No external requests except Google Fonts. Nothing from the bundle (operation ids, field names, permission keys, screen ids) appears as text a user reads. Also list gaps in `return/FINDINGS.md`.

**No frames are imported from this folder until the client chooses.** The chosen option's screens then go into the P10 batches.
