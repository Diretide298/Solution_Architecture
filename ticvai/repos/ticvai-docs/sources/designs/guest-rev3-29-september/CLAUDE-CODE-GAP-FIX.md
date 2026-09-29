# Prompt for Claude Code — close Guest App gaps against the Development Plan

You are working in the TICVAI Guest Booking prototype. Source of truth for scope is the Development Plan (23 Sep 2026): Guest App Web = 46 screens, Guest App Mobile = 71 screens. The prototypes currently fall short of that. Close the gaps below without redesigning anything that already exists.

## Files
- `TICVAI Guest Booking.dc.html` — web app (views: home, list, book, tickets, account, help, venue, wish, offers, fx, login, waiting room, single event).
- `TICVAI Guest Booking Mobile.dc.html` — mobile app (views: home, tickets, venue, account, settings, book, seats, ident, confirm, billing, privacy) + `MobileTabBar.dc.html`.
- Shared helpers: `venueplan.js`, `stadium3d.js`, `venuemap3d.js`, `support.js`. Do not edit `support.js`.

## Rules
1. Follow the existing visual vocabulary exactly: inline styles only, the per-venue palettes and fonts (theme park, water park, stadium, theatre, dining, kids club), existing card, chip, sheet and button patterns, and existing copy tone. Every new screen must render correctly for all six venue types and in RTL.
2. One decision per screen for staged flows. Keep the persistent cart, identity gating at checkout entry, the "Sign-in required" guest checkout default, the mandatory code proof, and profile dedup (Email / Mobile / Email or mobile) as they are.
3. Add every new screen as a view in the existing router (`view` / `go()`), with a `data-screen-label` using the plan's screen name and the existing ID scheme (`WEB-0xx` web, `GST-0xx` mobile). Each screen needs loading, empty, error and offline states.
4. Reuse existing mock data and state. Add new mock data in the same shape as the data already there. No new libraries.
5. Web and mobile must mirror each other where the plan has the screen on both.
6. Do not rebuild the scroll-animation watch list or config drawer; only register new views with them.

## A. Web — missing screens (add as views, linked from Account / Help / footer)
- Profile & Preferences — edit details, verify email, contact + marketing prefs, privacy choices, save.
- Order History — list, order detail, request refund, transfer tickets.
- My Reservations — list, check availability for a change, change or cancel.
- Wallet & Gift Cards — balance + transactions, gift card and game card balance, save card, move value between wallets.
- Membership Management — memberships, benefits, history, transfer (reuse mobile billing statement pattern).
- Ticket Transfer — transfer, claim, list for resale, sent history.
- Newsletter Subscription — opted-in list, subscribe/unsubscribe, notification devices, save.
- Contact & Venue Information — contact details, info, link to newsletter.
- Error / Sold Out / Maintenance — one screen with three states, wait-or-leave guidance.
- Lost & Found — report (lost item / complaint / question), my reports, reply thread.
- Survey & Feedback — rating, written feedback, link to order, submit.
- Devices, Wishlist & Consent — devices, consent history, waivers signed/outstanding, delegate a booking to someone, download data, delete account (tombstone, same as mobile).
- Help Centre & Accessibility — FAQ + policies + accessibility statement (extend existing help view if cleaner).

## B. Web — missing functions on existing screens
- Cart: promo code field with valid/invalid/expired states; empty basket with confirm.
- Payment: interrupted-payment recovery ("we are checking with your bank" → success / failed / unknown).
- Confirmation: reprint / reissue tickets, resend.
- Login: national ID sign-in (UAE Pass), set up two-step verification, link a guest checkout to an account, sign out.
- Help: raise a support case, see open cases, app status + recent changes, "speak to a person" handoff from Sahli.
- Multi-currency: show exchange rates in use and their timestamp.
- My Tickets: remaining entitlements per ticket, scan and sharing history.

## C. Mobile — missing screens (71 total; build in wave order)
Wave 1 (build first): Arabic/RTL experience, Attraction Details, Event/Exhibition Details, Explore Categories, Event & Attraction Listing, What's On, Search, Select Date & Time (split from book if merged), Ticket Details, Tickets & Add-ons (transfer, cancel transfer), Profile, Maintenance/Upgrade, Branded Queue/Waiting Room, Dynamic QR Ticket (confirm it matches plan functions), Review & Payment (pay for someone else's booking, open payment link, payment outcome).
Wave 2: AI Concierge Home / Chat / Contextual Help, Accessibility Information, Attraction Wait Times, Bundle Package, F&B Browse & Order, F&B Order Tracking, Face Pass (register / status / withdraw), Help & Support, Help & My Cases, In-Venue Notifications, Interactive Map, Lost & Found, Loyalty & Rewards, Memberships (incl. delegates), Menu Item Detail (allergens), Multi-Currency, My Reservations, Reservation Details, Offers & Promotions, Order History, Payment Methods, Refunds & Resale (incl. waiver check), Reserve a Table or Cabana (waitlist, notify), Retail/Merchandise, Security & Sign-in (devices, trust device, sign out lost device, recovery email/phone, step-up auth), Share & Group Booking (invites, referral code, challenges), Ticket Delivery & Sharing, Ticket Transfer, Upsell/Cross-Sell, Venue Info & Services, Wallet Overview.
Wave 3: AI Optimized Itinerary, Add to Calendar/Reminders, Build Your Own Itinerary, Digital Companion Mode, Feedback & Ratings, Newsletter & Preferences, Parking Reserve & Pay, Parking Confirmed, Plan My Day In Progress, Plan Your Adventure Start, Resource Availability (Cabana), Resource Booking Cabana, Saved Items/Wishlist, Shop & Drop Collection, Suggested Itineraries, Virtual Queue.
Account menu rows "Reservations", "Ticket transfer", "Lost & found" must open real screens.
Where web already has the equivalent (map, order tracking, virtual queue, parking, shop and drop, loyalty, notifications, menu item, wishlist, offers, fx, concierge), port the logic and re-lay it out for mobile rather than inventing new behaviour.

## D. Plan inconsistencies — already raised with the client; build interim versions now
Until the client answers, build every item below so nothing is missing. Keep each one self-contained so it is easy to merge or remove later.
- Wave mismatches (Parking, Virtual Queue, Multi-Currency): build on both web and mobile now, whatever wave they're in.
- Duplicate screens: build one screen that covers the functions of all the duplicate names, with a `data-screen-label` that lists every plan ID it covers.
  - Mobile: Ticket Transfer + Ticket Delivery & Sharing + Tickets & Add-ons → one Transfer screen.
  - Web: Wishlist + Devices, Wishlist & Consent → Wishlist view plus a separate Devices & Consent view. Help Centre / FAQ + Help Centre & Accessibility → one Help view with FAQ, cases, policies and accessibility tabs.
- Mobile-only features: add web equivalents.
  - Face Pass (register, status, withdraw) → Account on web.
  - Security & Sign-in (devices, trust device, sign out a lost device, recovery email/phone, step-up auth) → Account on web.
  - Arabic/RTL is already covered by the RTL toggle; make sure every new web view passes in RTL.
- Group and school booking on web: add a Group Booking view (see the group, invite, accept or decline, referral code) mirroring mobile Share & Group Booking. Link it from the existing kids, park and stadium group booking products.
- Things we built that the plan doesn't list (guest-checkout gating, code proof, profile dedup, billing statement, kids height/age gate, school trips, parties, dining takeaway/delivery, config drawer): keep all of them unchanged.
- The White Labelling duplicates (Domain, Brand Kit/Logo, Theme/Typography) are out of scope for this repo; don't touch them.

## Deliverables
1. Updated `TICVAI Guest Booking.dc.html` and `TICVAI Guest Booking Mobile.dc.html`.
2. `handoff/SCREEN-COVERAGE.md` — a table of every plan screen (web 46, mobile 71): plan name, wave, `data-screen-label`, view key, status (done / partial + what's missing).
3. In `SCREEN-COVERAGE.md`, flag every interim item from section D with `interim — pending client`.
4. Before finishing: open both files, click through every new view for each of the six venue types and RTL, and confirm there are no console errors.

Work in order: B (web functions) → A (web screens) → C Wave 1 → C Wave 2 → C Wave 3. Commit after each block.
