# Minutes of Meeting — Workshop: Licensing / B2C Review

**Date:** 29 September 2026, 06:01 (1h 05m)
**Attendees:** Muhamed Allam, Qossai Alqawasmi (client) · Chinmay Parab, Aishwarya More, Hrushikant Patkar

## 1. Website (B2C) — review of Rev 3

Client confirmed most Rev 3 feedback is now reflected. Qossai: once the items below are applied, the website is **approved to start development**. Muhamed will re-check the revised build.

| # | Item | Decision / change |
|---|------|-------------------|
| W1 | Guest checkout | The email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again — go straight to T&Cs and complete the booking. Profile is created; details can be completed later (Platinumlist pattern). |
| W2 | Seat maps (stadium / theatre) | Show sections first with colour and price; zoom into a section to see seats. Pinch-out / scroll-out returns to the full map so other sections can be compared. |
| W3 | View-only products | CMS option to list a product (e.g. training courses) with full details but no Book button — show "Contact sales to book" with contact details. |
| W4 | Help me choose (experience builder) | Not a consent step. Questions (yes/no, age, certified or not, etc.) must filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). Needs a configuration page per venue; AI may propose the question set from the product catalogue for the operator to validate and edit. |
| W5 | Surf sessions | Same pattern as the time selection: products (beginner, intermediate…) appear only after a time slot is chosen. |
| W6 | Cabanas | Map-based cabana booking stays optional per configuration; not every operator uses the same flow. Same map back end as theme-park F&B/locations (reusable later for in-park navigation). |
| W7 | Config: "Category display" | Retired control, has no effect — remove. |
| W8 | Workshops (museum) | After Help me choose, the guest selects the workshop first, then date/time. Only relevant products shown. |
| W9 | Meeting rooms | Availability is checked against date + start time + duration together; changing any of the three re-checks all rooms. |
| W10 | Meeting-room cleaning buffer | Configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. |
| W11 | Guided tours / sessions | Confirmed correct (date → language → time slot). Sessions come from configuration; grid reflows for many slots. |
| W12 | Config side panel | Reference tool only, not the CMS. CMS will be step-based and include header/footer, logos and banners. |

## 2. Mobile app

Current mobile build goes straight into the booking journey; client finds it unclear. Redesign the UI (all web products and flows, incl. cabanas and surf, must remain available):

- **Tabs:** Home · Explore · Plan · Tickets (Yas Island / Six Flags references).
- **Persistent "Buy tickets"** button on every screen.
- **Home / Discover:** venue overview — description, opening hours, types (rides, dining, events, shops). One or two sample items per type are enough.
- **Item detail:** shows location on map and proposes the relevant product, e.g. restaurant → "Buy meal combo", which automatically adds the required admission ticket (checkout in ~3 steps).
- **Optional intro video** with "Skip introduction".
- **Plan:** trip planner — party size, heights, dates, pace (packed/relaxed), interests, cuisine → proposed itinerary per day, with add-ons (e.g. quick pass).
- **Tickets:** purchased tickets and scan code.

## 3. B2B / reseller portal

- Qossai proposes a POS-style interface for resellers (high-volume sellers: hotels, travel agents) instead of a B2C-style site with a login. Assigned tickets and partner prices after login; optional cash drawer; sent-ticket history and resend; balance view.
- Muhamed: acceptable; supporting both per customer is fine if effort allows.
- **Decision:** Chinmay to wireframe both options; decide after review.
- TICVAI marketing site should also showcase demo versions of each platform (POS, kiosk, mobile app, menu management).

## 4. Architecture

HLD/LLD in progress (Azure and AWS pages). To be shared after corrections.

## Actions

| Owner | Action | Due |
|---|---|---|
| Chinmay | Apply website changes W1–W10 and share revised build | This week |
| Chinmay | Mobile app first revised version (new UI) | 30 Sep |
| Chinmay | HLD / LLD | After mobile |
| Chinmay | B2B wireframes — POS-style and website-style | After mobile + HLD/LLD |
| Chinmay | Update tracker, send link in a separate email thread | Today |
| Muhamed / Qossai | Review tracker internally; call tomorrow to align | 30 Sep |
| Muhamed | Re-review revised website | On receipt |
