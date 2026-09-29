# Status against the 29 September MoM

**Files:** `TICVAI Guest Booking v2.dc.html` (web) · `TICVAI Mobile App v4.dc.html` (mobile) · `TICVAI Visit Planner.dc.html` · `ticvai-ar-app.js`, `ticvai-ar-venues.js` (Arabic)

## Website (B2C)

| # | Item | Status |
|---|------|--------|
| W1 | Guest checkout asks only configured fields; no re-entry after code | Done. Config: *Guest pop-up asks for* (Email only / + name / + mobile). After the code, only T&Cs. |
| W2 | Seat maps: sections first, zoom into section, pinch/scroll out to return | Done on web and mobile. Tapping a zone zooms the map to it and shows seats in place. |
| W3 | View-only products with contact sales | Done. Info-only cards show Call sales / Email sales. Toggle: *Show info-only products*. |
| W4 | Help me choose filters products; configurable; AI-suggested set | Done. Age and surf-level questions filter the list, with *Show everything*. Config: on/off, filter on/off, *Question set* (operator / AI-suggested). |
| W5 | Surf: products only after a time slot | Done. |
| W6 | Cabana map booking, optional per configuration | Done on web and mobile, using the real map with 34 huts. |
| W7 | Remove retired "Category display" | Done. |
| W8 | Workshops: workshop first, then date/time | Done. The date-first rule no longer overrides product-first flows. |
| W9 | Meeting rooms checked against date + start + duration | Done. 15-minute start times; busy rooms show "free from". |
| W10 | Cleaning buffer: per booking or N per day | Done. Config: *Meeting-room cleaning*, *buffer length*, *cleanings per day*. |
| W11 | Guided tours and session grid | Unchanged, as confirmed. |
| W12 | Config panel is a reference tool | Noted. The CMS remains a separate step-based build. |
| + | Visit planner on web | Added. *Plan your visit* in the header opens it full screen, and *Book this plan* goes straight into booking. |
| + | Meal combo + admission product | Added to the theme park (used by mobile item pages). |

## Mobile app (v4)

| Item | Status |
|------|--------|
| Tabs Home · Explore · Plan · Tickets, persistent Buy tickets | Done. The raised centre button (or floating / flat, per venue) sits on every screen. |
| Home / Discover: overview, hours, types, 1–2 items each | Done. Photo hero (carousel / video / poster / split per venue), category tiles, highlights, info. |
| Item detail: map location and relevant product (meal combo includes admission) | Done. Gallery, 2D/3D map pin, product card. |
| Optional intro video with Skip | Done (Pexels clips per venue). |
| Plan: party, heights, dates, pace, interests, cuisine → itinerary, add-ons | Done. Swap, remove, add and undo per day; Fast Track add-on; *Book this plan*. |
| Tickets and scan | Done. Dynamic QR (30 s refresh), wallet, calendar, send, share, refund/resale. |
| All web products and flows available | Done natively from the same engine. Each product has its own step order, style and seat, cabana and route maps. |
| White label | Venue selector at launch; per-venue brand, theme, fonts, hero, tabs, motion, mascot, booking style and separate sign-in. |
| Config panel | Left of the phone: venue app, booking-flow dropdown, step order, theme, sizes, layout, maps, booking rules, language, currency. |
| Guest app services (from P02) | Assistant chat, virtual queue, food ordering and tracking, offers, rewards, parking, notifications, saved, orders, lost & found, feedback, help, accessibility, search, security, currency. |
| Arabic | Interface and venue content translated; layout flips. Venue names stay as written. |

## Audit fixes (29 Sep)

Every item in AUDIT-29SEP.md is closed, including the website at-venue additions: Happening now, Book a table and Shop with collect-at-gate.

## Not in this round (per MoM actions)

- **B2B / reseller portal:** POS-style and website-style wireframes. Scheduled after mobile and HLD/LLD.
- **HLD / LLD:** separate workstream.
- **TICVAI marketing site demos:** not started.
- **Tracker update and email thread:** outside the design files.

## Open or needs client input

- Real station list, fares and timetable for intercity transport.
- Confirm cabana numbering and pricing.
- Real venue photos and videos to replace the stand-ins.
- Offline builds are rebuilt (29 Sep). The street map, fonts and Pexels videos still need internet. The mobile single file loads the booking engine from the website single file beside it.
