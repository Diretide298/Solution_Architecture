# Guest App (P02): findings from the 30 September v4 drawing

Nineteen changed Block A screens with no view in Mobile App v4 were drawn by Claude Code on 30 September 2026 in the v4 look. They are **not client-verified**; they wait for the client's design reviewer. Each one opens in `TICVAI Guest App.dc.html` in this folder from `#<screen id>`, and each declared state from `#<screen id>?state=<state>`. The same frames are imported as `wireframes/frames/<id>.html` and shown on `wireframes/P02 Guest App.dc.html`.

**How the look was matched.** Tokens, type, radii, shadows, the phone shell, the light status bar, the account row list, the back button and title, the plan timeline rows, the raised and floating tab bars and their icons are taken from `sources/designs/guest-rev3-29-september/TICVAI Mobile App v4.dc.html`: skin `park` (Summit Peaks), `water` (Coastal Aqua) and `rooms` (House of Pages). The booking-step pills follow `TICVAI Guest Booking v2.dc.html`. The tab bar is Home, Explore, Buy tickets, Plan, Tickets.

**Design choices to confirm with the reviewer**

- **Tab bar in booking steps.** v4 hides the tab bar inside the booking engine. The five booking steps drawn here (upsell, cabana by size, cabana map, room by the hour, review and pay) follow v4: they have a bottom action bar and no tab bar. Every other screen has the tab bar with Buy tickets. If the 29 September rule "Buy tickets on every screen" is meant to cover booking steps too, these five need it added.
- **Venue skins.** Cabana screens are drawn in the Coastal Aqua app (the water park that has Cabana Row) and the room booking in the House of Pages app. Everything else is the Summit Peaks app. This shows the white label working; it is still one look.
- **Photos.** Frames on a board cannot load images, so photos are brand-tinted gradient tiles. The build uses the venue's own images.

## Things the screens need that the operations do not provide

Drawn greyed with a short note on the screen, and listed here. Nothing was invented: where an operation exists in the contracts but is not declared on the screen, that is said.

| screen | what is missing | what exists | suggested fix |
|---|---|---|---|
| GST-039 Profile | The screen shows what we hold about the guest but declares no read of it: only saving (`updateMyProfile`) and consent recording. | `getMyProfile` (marketing-crm) exists. | Declare `getMyProfile` on GST-039. |
| GST-039 Profile | The form's components are the fields of a consent request (`purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`), not profile fields. Drawn as name, email, mobile, language and currency, with consent as switches and a one-line record of when it was given. | `updateMyProfile` takes the profile fields. | Rebind the form to the profile fields. |
| GST-066 Privacy & my data | The purpose says the screen shows where a request has got to, but nothing reads the progress of an export or erasure request. Drawn greyed. | `getDsarRequest` exists but needs a request id; there is no list of the guest's own requests. | A guest-callable list of my data requests, or return the request from `exportSubjectData` and declare `getDsarRequest`. |
| GST-048 Upsell | The suggestion panel is bound to `getUpsellSuggestions`, which the screen does not declare; it declares `decideRecommendations`. Drawn from the declared operation. | `getUpsellSuggestions` (promotions) exists. | Pick one and declare it. The screen is also thin (one panel, one button). |
| GST-056 Bundle package | The bundle list and its selection are bound to `listCatalogueBundles`, which returns catalogue publishing records (content hash, signature key, workstations), not packages a guest can buy. Drawn: the meal combo itself from `getBundle`; the list of other packages greyed. | `getBundle`. | A guest-facing list of bundles on sale, or drop the list and open this screen from the product only (MOB-4 already does). |
| GST-058 Cabana availability | The purpose is availability "by area and date", but nothing on the screen says which area a cabana is in (`Product` has no zone; `getAvailability` has no area). Drawn by type and day; area counts greyed. | Zones exist on the venue map (`PlacedResource.zone`, GST-074). | Drop "by area" from this list screen, or add the zone to the capacity product. |
| GST-058 / GST-050 | The filters are staff filters (`venueId`, `kind`, `isSellable`). A guest sees a date and nothing else; drawn that way. | – | Replace with a date. |
| GST-019 Order history | The filters are staff filters (`principalId`, `shiftId`, `venueId`). Drawn as guest filters: status and a date range. `listOrders` is still declared beside `listMyOrders`. | `listMyOrders` is the guest's own list. | Drop `listOrders` and its staff filters from the guest screen. |
| GST-031 Concierge home | No list of the guest's past conversations. Drawn greyed. The screen's only read is an F&B menu (`getGuestMenu`), drawn as "Order food". | `listAiConversations`, `listConversations` exist. | Declare one of them. |
| GST-011 Wallet | No way to top up the wallet. Drawn as a greyed button. Auto top-up and settle at exit are wired. | `topUpWallet` exists. | Declare `topUpWallet` on GST-011. |
| GST-036 Loyalty | Recommended rewards show a points price but nothing redeems them. Drawn with greyed Redeem buttons. | `redeemLoyaltyPoints` exists. | Declare it on GST-036, or route Redeem to the screen that has it. |
| GST-009 Review & payment | The rev 3 prototype offered Tabby. Tenders are card or wallet (decided 28 September, R080 (a)); no instalment tender exists. Drawn with card, Apple Pay (a card) and wallet only. | – | Confirm Tabby is out, or add a tender. |
| GST-009 Review & payment | "Transfer order tickets", "Create order" and "Acquire inventory hold" are listed as buttons, but a guest cannot transfer before paying and the other two are steps of checkout, not choices. Drawn as one Pay button and a line saying tickets can be sent once paid. | – | Keep transfer on order history (it is there) and drop the other two from the action bar. |

## Other things noticed

- **GST-052 and GST-059 are out of the first release** (itinerary planner deferred, decided 28 September, R187: `wave: 4` with a `deferred` block) but are listed as changed Block A screens. Drawn anyway; check whether they belong in Block A.
- **GST-059** declares Swap and Re-order only; `updateVisitPlan` also supports remove and undo. Drawn as declared.
- **GST-073** shows two-step verification because Summit Peaks and Union Arena are drawn with it on (GAP-B1). At a tenant where no venue turned it on, the section is hidden.
- **GST-042**: the "who is signed in on this device" panel shows only when a session exists; the main state (nobody signed in) draws it as a one-line reassurance.
- **Old captures.** The 28 September Mobile v2 captures for these 19 screens (`wireframes/frames/img/gst-*.png`) are no longer referenced by their frames. Left in place.
