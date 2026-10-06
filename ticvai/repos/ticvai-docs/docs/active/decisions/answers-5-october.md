# Chinmay's answers of 5 October 2026: kiosk customisation

> **The cited copy (5 October 2026, CHG-R4-001, CHG-R4-003, CHG-R4-004).** Chinmay Parab, the lead, in conversation on
> Monday 5 October 2026, copied into git so the R4 change entries can cite it (`ticvai/CLAUDE.md` rule 12: never
> cite `audit/` or a scratchpad). His words are quoted verbatim; the scope below them is the brief the lead gave the
> agent the same day, which the R4 entries apply.

## The request (Chinmay, 5 October 2026)

- "kiosk customisation option? of course it won't be like mobile app but screen saver video or photo, click to
  start, head footer content, size of the card etc. think of all things we can get from mobile to here"
- "update the rest"
- "run the agent now. we add it as release now to make sure that it goes out"
- Block: "A2"
- "it is a addition so it shouldnt break existing"

## What was decided

**The kiosk (P05, KSK-001 to KSK-017) becomes the third channel of the white-label Website & App builder, beside
web and app.** It inherits what the tenant has already published: the brand, theme, fonts (the Arabic pair),
content pages, products, waivers and consents (`getPublishedTenantConfig` already serves these to KSK-002). It adds
only what differs on a kiosk, as a kiosk configuration:

- **Device profile and kiosk groups** (by gate, zone or outlet; a kiosk in no group takes the default): orientation,
  screen size and resolution, mounting height (it sets the reachable-height default), touch scale, card size (small,
  medium, large) and columns per row.
- **Attract loop (the screen saver):** a playlist of video, photo and text slides (media library assets), their order,
  seconds per slide, transition, sound on or off; a schedule by time of day and weekday; "Touch to start" text per
  language, its position and animation; a "Download our app" QR slide; offline, the last cached loop plays.
- **Start screen tiles:** which functions this kiosk offers (sell tickets, collect a booking, order food, shop,
  membership, wallet top-up, map, assistant), their order, tile size and image; one hero banner.
- **Header and footer on the kiosk:** logo position, language switch, basket, Call staff, accessibility button, clock;
  footer payment logos, help text, and the legal links shown as QR codes.
- **Journey:** the kiosk channel's booking flows (custom flows allowed; the payment and legal steps locked as on web
  and app), the most steps a journey may take, upsell and cross-sell on or off and how many.
- **Session and privacy:** idle timeout in seconds, a "Still there?" countdown, then the basket is cleared and the
  kiosk returns to the attract loop and the default language; sign-in only by the app's QR or a one-time code.
- **Payment and output:** accepted methods; the receipt (print, email, SMS, QR); the ticket stock (80 mm thermal,
  wristband, card) and its print layout from the ticket designer; a "Send to my phone" QR.
- **Languages** shown on KSK-002 and the default. **Accessibility** reuses the existing `AccessibilitySettings`
  (BL-065); it is not duplicated.
- **Messages per language:** the idle warning; out of service by group with the expected-back time (KSK-014);
  offline; printer failure (KSK-010); payment unresolved (KSK-008); Call staff (KSK-013).
- **Hours per group:** outside them a "Closed" loop plays and nothing is sold.
- **Publish:** checks (the loop has an item, its media fits the screen, every enabled tile has products, an Arabic
  font when Arabic is on, the journeys are valid), publish to all kiosks or to one group, versions and roll back.
- **Not carried over from the app, deliberately:** app icons, the store listing, push notifications, dark mode and
  saved sign-in.

**Where it lands.** A new app-module in **Block A2** (not A1); its tasks go to Block A2, which ends Friday 11 December
2026 (Sprint 5). No existing ticket's owner, sprint or key moves.

**Additive only** ("it is a addition so it shouldnt break existing"): no operation, field, schema, enum value, table,
column, screen id or ticket key is removed or renamed; no required field is added to an existing request; no existing
operation's behaviour changes. New operations, schemas, optional fields, tables (as a new forward migration) and
screens only.

**The release.** It ships as release r2 ("we add it as release now to make sure that it goes out"). Chinmay waived,
for this release only, the 24-hour cooling-off of a plan change (`ticvai/CLAUDE.md` rule 9) on 5 October 2026.
**Updated the same evening (Chinmay, relayed by the lead):** r2 is not tagged on Monday 5 October; it is cut on
Tuesday 6 October, a regular release day, together with the other changes going in, so the Tuesday and Friday cadence
(rule 8) is kept. Only the cooling-off is waived.
**The release is named r2 (Chinmay, relayed by the lead, 6 October 2026).** Only r1 has gone live (OpenProject and
ADAM are on r1), so the release first called r4 is tagged r2. The earlier unreleased tags were renamed on both
remotes: r2 (9cce86a0) is now old-r2-ai-hosting and r3 (a67ca498) old-r3-aws; neither went live, and their changes
(CHG-R11-001 to 003, CHG-R3-001) ship in r2 with this one, with CHG-SQL-001 and the r4 batch (CHG-R4-001 onwards,
whose ids stay as names).

## Why (the gap it closes)

The package had no kiosk configuration. KSK-001 Attract Loop is ticketed (APP-KIOSK-KSK-001) but "declares no
operation; nothing fills the loop" (CHG-R1S-022). The white-label app-module on the kiosk (AM-WHITE-LABEL-P05) builds
only KSK-002 and KSK-014. BO-485 "Self-Service Kiosk Profile & Channel Configuration" (P08, wave 3, games only, no
ticket) was an empty Save/Cancel form on the games-only `setGameKioskConfiguration`, with gaps saying it "needs a
person before it is built". ADM-582 "POS, Kiosk & Terminal Assignment Manager" assigns devices but no kiosk to a
configuration.
