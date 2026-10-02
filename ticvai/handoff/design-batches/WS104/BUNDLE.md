# WS104 — Subscription Licensing AI Self Service board 7

**10 screens · 10 operations · 19 schemas · 7 permissions**

Platform P08 Venue Management · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `AI_USE, PLATFORM_TENANT_MANAGE, PRICE_CONFIGURE, PRICE_VIEW, PRODUCT_CONFIGURE, TENANT_CONFIGURE, WORKSTATION_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The processes these screens belong to

Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the process runs end to end and which words the screens must use.

### Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management)

Platform Foundation is everything the apps stand on. Five apps each have one door: the guest app and website (WEB-016, GST-042: a six-digit code to email or mobile, a password, Apple or Google, UAE Pass; never enterprise SSO), the till (POS-000: employee number and PIN, recent operators as tiles; the kitchen display is the same app), the staff handheld and scanner (EMP-001, SCN-001), Venue Management (SUP-001, the single door for the back office P08, the CMS P13, analytics P16 and the support desk P12) and TICVAI Control (ADM-001 for TICVAI's own platform operators, PTR-001 for partner users; the developer portal P14 and the sign-up P17 belong to this app too). A second factor is required by permission, not by role or device: ROLE_MANAGE, LEDGER_APPROVE and every PLATFORM_* permission, plus any the tenant adds; so a cashier never sees it and a platform operator always does. The factor is an authenticator app with an emailed code as fallback; five wrong codes lock step-up for the lockout minutes, never permanently. Guests get two-step verification only at a venue that switched it on. One person holds one session per workstation: a second sign-in is refused and only a supervisor ends the other session. Several roles mean a role prompt; one role goes straight in. The workstation decides the Sale Board, hardware and till identity, never what a person may do. Sensitive actions (refund approval, journal approval, credential reset, partner credit, commission rules, opening a platform-staff grant and 17 more) demand a fresh step-up on the operation itself, asked in place in the action's confirmation; the tenant may raise the strength, never remove it. Permission outcomes are three, never one word: self-authorised (proceeds, audited), escalated (a supervisor PIN in place), refused (the denied state, naming the permission); a missing permission is never an empty table, and a record outside the person's venues is "not found", indistinguishable from absent. The hierarchy is binding (tenant, brand, region, venue, department, sub-department, workstation; outlet beside department for F&B and retail); region owns currency, decimals, time zone, date format and fiscal year; configuration resolves nearest-ancestor across tenant, region and venue (outlet for F&B and retail), venue is the floor and a workstation is assigned a profile, never configured; every configuration screen says which level it writes and what it inherits. Venue Management is one tenant-level surface filtering across the venues in the session's scope. TICVAI's Console runs outside every cell: a platform operator picks a tenant and opens a time-boxed, audited platform-staff grant (with step-up) before any tenant action, and the tenant sees every action in its audit log (ADM-412 is the reference implementation). Approval workflows record authorisations and never perform the action; the requester cannot approve their own request; a venue may tighten and never loosen a rule from above; in-flight …
*(source: screens/P12-support-agent-console.yaml#SUP-001; R135; R126; R167; DI-1072; ADR-0002; ADR-0003; ADR-0004; R184; contracts/spine/identity.yaml#createMfaChallenge; contracts/spine/approvals.yaml#setStepUpPolicy; ADR-0011; ADR-0018; ADR-0029; R098; contracts/spine/approvals.yaml#decideApprovalRequest …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sign in / Sign out | Entering and leaving any app, staff or guest. | Login, Log in, Logon, Logout | screens/P04-point-of-sale.yaml#POS-000 … |
| Authentication code | The staff second factor from the authenticator app (or the emailed fallback). | OTP, 2FA code, token | screens/P09-platform-admin-console.yaml#ADM-001 |
| One-time code | The six-digit code a guest receives to sign in or prove a contact. | OTP, PIN, password | DI-1034; R167 |
| Two-step verification | The guest's optional second factor, asked only at venues that switched it on. | MFA, 2FA | DI-1072 |
| Tenant / Brand / Region / Venue / Department / Outlet | The binding hierarchy levels; region owns currency and dates; outlet is F&B or retail inside a venue. | Client, Customer, Org (for tenant), Site, Park, Property (for venue), Area, Territory (for region) | ADR-0011; ADR-0018 |
| Workstation (back office) / till (operator copy) | A configured device; decides Sale Board, hardware and till identity, never authorisation. | Terminal, Station, POS (for the device), till (for the Deposit Box) | ADR-0002; R156 |
| Sale Board | The configured front end a workstation loads (ticketing, F&B or retail). | Screen, Layout, Menu | ADR-0003 |
| Role | A named, fully configurable grouping of permissions; the seeded five are editable starting points. | Group, Profile | R229 |
| Staff member / Partner user / Platform operator | A tenant's staff principal; a partner's user; a TICVAI employee in the Console. | User (alone), Account, Agent (for venue staff) | F104 step 1; F104 step 4; F104 step 5 |
| Platform-staff grant | The time-boxed, audited access a platform operator opens into one tenant before acting in it. | Impersonation, Support login | R098 |
| Escalate / Refused | Escalate is supervisor approval captured in place; Refused is the denied state that names the permission. | Denied (for an action that can be escalated) | R197 |
| Approve / Reject / Return / Request information | The four decisions on an approval request; Withdraw is the requester's own act and never a rejection. | Accept, Decline, Cancel (for withdraw) | contracts/spine/approvals.yaml#decideApprovalRequest … |
| Subscription / Plan / Module / Licence | TICVAI's commercial relationship with a tenant, its plan, the modules it licenses and the limits. | Membership (that is the guest's pass) | R214 |
| Membership / Annual pass | A guest's pass product and its holder (BO-284 to BO-303). | Subscription (that is the tenant's TICVAI plan) | screens/P08-venue-back-office.yaml#BO-284 |
| Sandbox client / Production client | A developer's own test credential; a TICVAI-issued live credential after certification. | Test key, Live key, API key (without environment) | DI-927 |
| Asset (DAM) / Media (ticket) | A digital file in the library; ticket media is a wristband or card carrying entitlements. Never mix them. | Media (for a library asset) | contracts/satellite/assets.yaml#searchMedia … |

### AI & Intelligence

AI in TICVAI is one governed engine behind many screens. The guest meets it as Sahli, the concierge (WEB-044, GST-031, GST-033), as the planner agent that refines a rules-built day plan by chat (GST-054), and as upsell and cross-sell offers on a separate Extras step (WEB-008, GST-048). Staff meet it as the Staff App's AI tab (EMP-019/020, knowledge EMP-040/041), the kiosk assistant (KSK-015) and the support copilot (SUP-006, SUP-018). Venue managers meet it in Venue Management (BO-091 policy and spend, BO-919/BO-925..932 resource and staffing forecasts, BO-597/598 configuration drafts, BO-772/782 marketing optimisation, BO-793 translations, BO-970/975 seat-map generation, BO-1048 seat upsell, BO-1160 fraud cases) and in Analytics (ANL-010 suggestions, ANL-019 management insights, ANL-055 anomalies, ANL-057 forecasting studio, ANL-059 insight history, ANL-060 governance, ANL-071 AI maturity). The governance, configuration-assistant, forecasting, oversight, audit and monitoring boards sit on the TICVAI Console (P09: ADM-037 providers, ADM-469..498 configuration assistant, ADM-499..518 forecasting, ADM-519..558 governance, ADM-633/637 fraud, ADM-680..697 recommendation governance). Five rules hold on every one of these screens. (1) Baseline first, then it learns per tenant: every data-driven answer (forecast, suggestion, risk score, recommendation) exists from day one, from the venue AI profile, a starting pattern for the venue type, the UAE calendar and the weather, and shifts to the venue's own data as it trades; nothing says "comes later" or refuses for lack of history - a refusal only names a missing setting. (2) Every answer shows its basis and maturity: a "Based on" line, a stage badge (Starting, Learning, Established, Trained on your data), "Limited historical data" while the starting pattern carries more than half the weight, ranges or bands rather than a bare percentage, a confidence only where the producer really has one, a plain-words explanation always. (3) A trained model replaces the baseline only when it beats it in a shadow run of at least six weeks and an admin promotes it; the platform raises "Ready to promote" and never switches by itself. (4) The LLM never reads raw data: numbers come only from query results the platform runs (the answer shows the query), only the masked prompt and retrieved context leave the platform, and AI only drafts - the owning screen applies. (5) One autonomy scale, L0 Disabled to L4 Controlled auto, with first-release ceilings, separate from user permission and from the approval tier; impactful actions route to a person, who sees current against proposed, impact, risk and what is affected, and can approve within a limit, challenge, override or roll back; every decision is traceable (data, model, approver, time) and searchable by customer, venue and capability. In Block A (5 October to 20 November 2026) the guest concierge with retrieval, Help me choose, translations, the planner agent, the gateway and …
*(source: ADR-0051; ADR-0050; ADR-0020; ADR-0052; ADR-0053; ADR-0054; ADR-0059; ADR-0051 (AI-D01..AI-D20); ADR-0051 (AI functions review 30 Sep §2 §4 §9); MoM 18 Sep 4.1-4.10; MoM 21 Sep 4.1-4.14; MoM 30 Sep 4.1 4.7; ADR-0059 (Block A slice: tasks.csv))*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Sahli | The guest concierge's name; the entry reads "Ask Sahli" and shows as mascot art when the venue's Concierge mascot setting is on (default), otherwise a plain button. | Chatbot, Bot, AI Concierge (as a visible label), Virtual agent | DI-1069 / screens/P01-guest-web-storefront.yaml#WEB-044 |
| Based on | The line on every AI answer that says what it was computed from, e.g. "Based on: your venue profile, UAE calendar, weather, 23 days of your sales". Always present. | Data sources, Model inputs, Powered by AI | ADR-0051 Maturity / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Starting / Learning / Established / Trained on your data | The four maturity stages (enum starting, learning, established, learned), shown as one badge. Moves by itself from Starting to Established as own data arrives; Trained on your data only after an admin promotion. | Beta, Experimental, Low confidence, Cold start (in UI), Not enough data | ADR-0051 / ADR-0051 (AI functions review 30 Sep §2) |
| Limited historical data | Shown while own data carries less than half the weight (AiMaturity.limitedHistory, ownDataShare < 0.5). An honest qualifier, never a refusal. | Insufficient data, Not available until, Comes later | ADR-0051 / contracts/satellite/ai.yaml#/components/schemas/AiMaturity |
| Range | The 10th-90th percentile band a forecast or estimate is shown with (e.g. "1,850-3,400 guests, most likely 2,600"). Never a bare accuracy percentage on an answer; measured accuracy (WAPE, bias, coverage) appears only on accuracy screens … | Accuracy 92%, Confidence 0.87 (on a heuristic), Exact | ADR-0051 / contracts/satellite/ai.yaml#getForecast / … |
| Running in the background | A trained model in shadow next to the live answer (AiRelease.stage shadow); it changes nothing a person sees. | Live, Active model, Testing in production | ADR-0051 Promotion / ADR-0051 (AI functions review 30 Sep §2) |
| Ready to promote / Promote | A shadow model passed its gate (governance alert promotionReady); an admin promotes it one stage at a time (canary, then production). The only way a model replaces the baseline. | Deploy, Go live, Auto-switch, Activate model, Upgrade AI | ADR-0051 (AI-D16) / contracts/satellite/ai.yaml#promoteAiRelease |
| L0 Disabled / L1 Advisory / L2 Prepare / L3 Execute with … | The one autonomy scale for every AI capability, shown as "L2 Prepare" etc. with the capability's ceiling beside it. Lower scopes tighten, never raise. | Autopilot, Copilot mode, Level 0-3 (CFG book), Approval level (for autonomy), Manual/Semi/Auto | ADR-0050 / ADR-0050 (AI-D04) / … |
| Approval tier | How many people must approve a proposed action (ProposedAction.approvalLevel, 1 or 2). Not an autonomy level. | Autonomy level, Approval level (ambiguous) | ADR-0050 |
| Suggestion / Draft | What AI produces. A suggestion advises; a draft is a ready-to-review change that a person applies in the owning screen. Copy says "Nothing is applied until you approve it." | AI changed, Auto-applied, AI updated your prices | ADR-0020 / ADR-0051 (AI functions review 30 Sep §4 Configuration assistant) / … |
| Why this? | The link or expander that opens an answer's explanation (Suggestion.explanation, recommendation template reason, decision trace). Plain words; for guests a template reason. | Explainability, SHAP, Feature importance (in operator copy) | ADR-0052 (AI-D09) / contracts/satellite/ai.yaml#/components/schemas/Suggestion |
| No thanks | The explicit decline on an offer. Only this counts as a decline and it is remembered across channels; scrolling past or closing the step is not a decline. | Dismiss (as a decline), Skip (as a decline), X (as a decline) | ADR-0052 (AI-D07) / DI-962 / … |
| Hold for review | What a high fraud or risk score does to a payment or order. The transaction goes through; it is held for a person. | Decline, Block, Reject (for a risk score), Fraud detected | ADR-0053 / ADR-0053 (AI-D06) |
| Hand over to a person | The concierge passes the whole conversation and its own summary to a live agent; the guest does not repeat themselves. | Escalate, Transfer, Contact bot | contracts/satellite/marketing-crm.yaml#handoverToAgent |
| Not available yet | The analytics assistant's answer to a question outside the semantic model; it records a knowledge gap and never improvises a number. | I cannot answer, Error, Unknown | ADR-0054 |

### White Label & CMS

A tenant (one operator, one or many venues) brands and arranges its own guest surfaces, the guest web (P01), the guest app (P02) and the kiosk (P05), from the Venue CMS (P13, a section of the Venue Management app), and TICVAI platform staff can do the same from the console (P09 ADM-016..018) only under a time-boxed grant into the tenant. Everything is configuration over a fixed structure: the guest flow, the page structure and the components are TICVAI's and stay the same for every tenant; the tenant chooses graphics, colours, fonts, which modules and tabs appear, the order of homepage sections and booking steps within allowed limits, copy in each language, and its domain. It never adds components. Work happens in ONE working draft per tenant; nothing a guest sees changes until a person with TENANT_PUBLISH publishes the draft as an immutable version (with a note), and a rollback is restore into the draft, review the diff, then publish, never one click. Three things are deliberately outside the draft and take effect at once: the live app status (maintenance, minimum app version, contact, sold out or closed), a venue's Help me choose publish, and policies (each save is a new version). Build-time parts (app icons, native splash, custom font files, wallet and payment integrations) reach guests only with a new store build, which the client publishes under its own Apple and Google accounts (CMS-104). Staff surfaces (POS, scanner, staff app, kitchen display) never take tenant branding; every guest surface carries the "Powered by TICVAI" credit, a toggle that is on by default (decided 2 October 2026, CHG-NOTE-009; DI-297 amended). Arabic is a first-class layout: enabling `ar` requires an Arabic font, the whole layout mirrors (numbers, times, codes and logos do not), and every authored text is a per-language value. The step-based Site Builder (CMS-102) walks a new tenant through seven steps from a venue-type preset so that a logo, four colours and a publish are enough for a working site in about 30 minutes; every step opens the full screen for its details. Vocabulary below; the element-by-element model follows; inputToOutput at the end gives worked examples.
*(source: contracts/satellite/white-label.yaml#/info; DI-223; DI-285; DI-111; DI-297; DI-296; DI-298; DI-997; DI-998; DI-1014; R139; R073; F22 step 5; F22 step 6; docs/architecture/rtl-and-theming.md)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Draft | The tenant's one working configuration. Every Save writes it; guests never see it. | Staging, Unsaved, Pending | contracts/satellite/white-label.yaml#/info |
| Publish | Make the draft the live version guests read, with a note. Needs TENANT_PUBLISH. | Go live, Deploy, Push, Save and publish | contracts/satellite/white-label.yaml#publishTenantConfig |
| Save | Write to the draft. Never publishes. | Apply, Update live | contracts/satellite/white-label.yaml#/info |
| Version | An immutable published snapshot, numbered, with who published it and the note. | Release, Revision, Backup | contracts/satellite/white-label.yaml#/components/schemas/ConfigVersion |
| Restore into draft | Copy an old version back into the draft. Publishes nothing. | Roll back, Revert, Undo | R139 |
| Live now | The changes that bypass the draft and apply at once (maintenance, availability, minimum app version, contact, Help me choose publish, policies). | Instant publish | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Needs an app update | A build-time change (app icon, native splash, uploaded font, wallet or payment integration) that reaches app users only with a new store build. | Rebuild required, Build-time, Pending release | contracts/satellite/white-label.yaml#/components/schemas/ChangeScope |
| Theme | The tenant's colours, corner radius, surfaces and buttons. | Skin, Template, Style sheet | contracts/satellite/white-label.yaml#/components/schemas/Theme |
| Booking flow | The ordered steps a guest goes through to book one kind of product at one venue. | Checkout flow, Journey, Funnel, Wizard | contracts/satellite/white-label.yaml#/components/schemas/BookingFlow |
| Step | One stage of a booking flow (Date, Time, Tickets, Extras, Payment...). Marked Required, Optional or Conditional. | Page, Stage, Screen | contracts/satellite/white-label.yaml#/components/schemas/BookingFlowStepKey |
| Help me choose | The venue's short set of questions that filters the products shown. Never a consent step. | Quiz, Experience builder, Wizard, Recommender | DI-1005 |
| Module | A licensed product area a tenant switches on for guests (Dining, Shop, Map...). Off means hidden, not greyed. | Plugin, App, Feature | contracts/satellite/white-label.yaml#setModuleEnablement |
| Feature | A finer switch inside the guest app (guest checkout, AI concierge, Apple Wallet...). | Module, Add-on | contracts/satellite/white-label.yaml#setFeatureToggles |
| Buy tickets | The persistent button in the guest app that opens GST-003, and its label. | Book now, Shop, Purchase | DI-1081 |
| Powered by TICVAI | The platform credit on every guest surface; a toggle, on by default, off only where the venue's licence allows. | Built by TICVAI, Made by TICVAI | DI-297 / decided 2 October 2026 by Chinmay (CHG-NOTE-009) |
| Site Builder | The seven-step guided set-up (CMS-102). | Wizard, Onboarding, Setup assistant | DI-997 |
| Venue override | A booking setting one venue sets differently from the tenant; everything else is inherited. | Exception, Custom setting | DI-1063 |
| Sold out today / Closed | The two availability signals guests see; sold out means come another day, closed means the venue is not open. | Unavailable, Error | R073 |
| Maintenance | The tenant-branded page shown while the guest web and app are switched off, with when they are expected back. | Down, Outage, Offline | contracts/satellite/white-label.yaml#setMaintenanceMode |
| Domain | The web address the tenant's guests use; Verify proves the tenant controls it before a certificate is issued. | URL, Site address, DNS | contracts/satellite/white-label.yaml#claimCustomDomain |

### Ticketing & Guest Commerce, as the venue and TICVAI configure and run it

WHAT THE PROCESS IS. Everything a guest can buy is set up, priced, promoted and serviced here, on Venue Management (P08, the venue's own back office, served inside the venue's cell) and on the TICVAI Console (P09, TICVAI's control plane, outside every cell). End to end: (1) CATALOGUE. A product has one of twelve kinds (admission, timedAdmission, datedAdmission, openDated, seated, membership, bundle, fnb, retail, rental, addOn, giftCard). Its ticket types (adult, child, senior, resident...) are not typed one by one: they are generated from the product's attributes (components) and each value combination becomes a sellable ticket type with no extra setup (DI-164). What a ticket grants (validity, entries, re-entry, days of week, blackout dates, expiry anchor, fast track, transfer) lives on a reusable entitlement template, not on the product. Who may take part (age, height, supervision, certification) is the eligibility rule; what the guest must answer is the data mask and the consent questions; how the guest sees it is guestListing (bookable, infoOnly, hidden), display tags (at most six), media and the booking flow. Group, family and corporate products and every after-sales policy (reschedule, exchange, refund, cancellation, upgrade, transfer) are configured inside the one product configuration, never on separate screens (DI-465, DI-466). (2) LIFECYCLE AND PUBLICATION. A product moves draft, inReview, approved, live, withdrawn, archived. Approval and publication are two acts with two permissions (PRODUCT_APPROVE, PRODUCT_PUBLISH, R091); every product is authorised before it sells online or on site (DI-438). Approved is still not on a till: a till sells only what is in the signed catalogue release it pulled (publishBundle, ADR-0013), so a saved price is a back-office fact until the venue publishes to tills. Changing something that has sold is preceded by an impact check (assessProductChange: orders affected, entitlements issued, future performances, open carts); restoring a version creates a new version, and sold tickets keep the price and terms they were sold under (restoreProductVersion, DI-938, TRACKER Actions row 145). (3) PRICE. Prices live in price lists: per venue, per channel set, with validity dates and a priority, copied for the next season with an uplift (copyPriceList) and repriced in bulk only after a dry run (bulkChangePrices). Currency and decimal scale are never chosen on a form: they resolve from the venue's region (ADR-0008, ADR-0018; AED 2 places, OMR and BHD 3). When several rules apply, the configured hierarchy decides; there is no "lowest price wins" default (DI-595). Tax on the pre-discount price and three-decimal rounding are regional settings (DI-598). Dynamic rules always show their minimum and maximum price guardrails beside the trigger (getDynamicPriceRule). (4) PROMOTE AND BUNDLE. A promotion is a rule (automatic, or gated by a code) created in draft, made live only by Publish, which first analyses stacking; a …
*(source: DI-164; DI-171; DI-438; DI-465; DI-466; DI-595; DI-598; DI-387; DI-039; DI-044; DI-474; DI-671; DI-987; DI-019; DI-080; ADR-0008; ADR-0013; ADR-0018; ADR-0019; ADR-0030; R091; R098; R101; R222; REV3-21; contracts/spine/catalogue.yaml#transitionProductLifecycle …)*

| Say | Meaning | Never say | Source |
|---|---|---|---|
| Product | Anything sellable, of one of the twelve kinds. The record that carries names, channels, listing, media and policies. | Item (except on F&B and retail screens), SKU (for tickets), Offering | contracts/spine/catalogue.yaml#/components/schemas/ProductKind |
| Ticket type | One sellable variant of an admission or event product (Adult, Child, Resident Adult), generated from the product's attributes. For retail and F&B the same record is labelled Variant. | Variant (on ticket screens), Sub-product, Rate (that is a price), Axis value | contracts/spine/catalogue.yaml#updateProductVariant / DI-164 / DI-437 |
| Attribute | A dimension that generates ticket types (Guest category, Residency, Tier, Length). Each has values; adding a value adds ticket types. | Axis, Component (the client's word; use it only in help text), Option | contracts/spine/catalogue.yaml#setProductAttributes / DI-164 / DI-450 |
| Entitlement | What a ticket lets the holder do (validity, entries, re-entry, days, blackout dates, expiry, fast track, transfer), defined once on an entitlement template and shared by several products. | Access rights, Ticket rules, Validity profile | contracts/spine/catalogue.yaml#createEntitlementTemplate / DI-171 / DI-451 |
| Eligibility rule | Who may take part in or buy a product (age, height, supervision, waiver, certification). Distinct from a promotion's eligibility, which decides who gets a discount. | Restriction, Access rule (that is access control) | contracts/spine/catalogue.yaml#setProductEligibilityRule / DI-463 |
| Price list | A set of prices for one venue and a set of channels, valid between two dates, with a priority. Several coexist (B2C, B2B, season). | Price book, Rate card, Tariff | contracts/spine/catalogue.yaml#createPriceList / DI-140 / DI-163 |
| Price category | A standard rate type (Adult, Child, Member) reused across lists so venues do not invent "Adult Standard" and "Normal Adult". | Price band (that is a seat-category band), Fare type (transport) | contracts/spine/catalogue.yaml#setPriceCategoryRateType / … |
| Price band | A priced band on a seat category (code, label, colour, amount, channel, from-date). | Price category, Zone price | contracts/satellite/seating.yaml#/components/schemas/SeatPriceBand |
| Promotion | A rule that changes a price automatically or when a code is entered; draft until published; declares how it stacks. | Offer (except in guest copy), Deal, Discount rule | contracts/satellite/promotions.yaml#createPromotion / DI-173 / DI-174 |
| Coupon code | A code issued from a coupon campaign that applies a promotion-style discount; one shared code or many single-use codes. | Voucher, Promo voucher | contracts/satellite/promotions.yaml#createCouponCampaign / DI-173 |
| Voucher | A code that carries money (face value, balance), sold or issued; a liability until redeemed or expired. | Coupon, Credit note | contracts/satellite/promotions.yaml#listVoucherBatches / … |
| Bundle | A product sold as one line whose price differs from the sum of its components, with a mandatory revenue allocation. "Package" is acceptable in guest copy. | Combo (that is an F&B meal deal), Catalogue bundle | contracts/satellite/promotions.yaml#createBundle / DI-220 / ADR-0019 |
| Catalogue release | The signed snapshot of a venue's catalogue, prices, promotions and sale boards that tills, kiosks and devices pull. Its action label is "Publish to tills". | Bundle, Catalogue bundle, Sync, Deploy | contracts/spine/catalogue.yaml#publishBundle / … |
| Approve / Publish / Save | Save keeps a draft; Approve records that it is authorised (PRODUCT_APPROVE); Publish makes it live for guests and channels (PRODUCT_PUBLISH). Three different buttons, never merged. | Submit, Go live, Activate (except CatalogueConfigStatus active), Deploy | R091 / contracts/spine/catalogue.yaml#transitionProductLifecycle / DI-438 |
| Product states | Draft, In review, Approved, Live, Withdrawn, Archived (ProductLifecycleState), always as coloured badges with these exact labels. | Published (for a product), Pending, Inactive (for a product) | contracts/spine/catalogue.yaml#/components/schemas/ProductLifecycleState |
| Channel | Where something is sold. Labels: pos Point of sale; kiosk Kiosk; web and guestWeb Website; mobile and guestApp App; b2b B2B partners; partner Partner; ota Travel agents (OTA); callCentre Call centre; api API; backOffice Back office. | Touchpoint, Outlet (an outlet is a business inside a venue), raw enum values | contracts/spine/catalogue.yaml#/components/schemas/Channel / … |
| Refund | Money returned after settlement, wholly or for some lines, under the venue's refund policy. | Return (that is retail goods), Reversal, Void | contracts/spine/orders.yaml#createRefund / DI-252 |
| Void | Cancelling a whole order before settlement, within the same shift, with a reason from the void list. After settlement it is a refund. | Cancel order, Delete | contracts/spine/orders.yaml#voidOrder / R222 |
| Exchange / Reschedule | Exchange swaps lines for other products or dates and settles only the difference; Reschedule is the same product moved to another date or time. | Rebook, Date change (acceptable only in guest copy), Refund and resell | contracts/spine/orders.yaml#exchangeOrderLines / … |
| Hold / Capture / Release | A deposit or stored-value amount is held, then partly or fully captured, and the rest released. A held deposit is not a payment. | Charge, Pre-auth (in staff copy), Block funds | contracts/spine/orders.yaml#authoriseStoredValue / … |
| Wallet (TICVAI wallet) | The guest's stored-value balance on TICVAI, spent by hold and capture. Distinct from the tender "Apple Pay / Google Pay", which the contract also calls wallet. | Digital wallet (for stored value), E-wallet, Credit (without a type) | contracts/spine/orders.yaml#/components/schemas/TenderKind / R080 |
| Credit lot | One amount of wallet credit of one credit type (cash, bonus, gift) with its own expiry; lots are spent nearest expiry first and the guest sees the breakdown but cannot choose. | Bucket, Batch, Top-up | TRACKER Actions row 171 / contracts/satellite/wallet.yaml#expireCreditLots |
| Venue map / Seat map | A venue map is the wayfinding map of a park or a floor (points, paths, bookable places); a seat map is the seating layout of an auditorium or stand. Never just "map" where both could be meant. | Layout (alone), Floor plan (unless it is a floor map), Map (alone) | contracts/satellite/venue-map.yaml#createVenueMap / … |
| Point / Bookable place | A point is a place on a venue map (toilet, ride, restaurant, exit). A bookable place is a cabana, lounger, table or pitch placed on the map and sold through its price band. | Pin, POI, Marker, Resource (in staff copy) | contracts/satellite/venue-map.yaml#setVenuePoint / … |
| Station / Route / Timetable / Departure / Fare table / Pass … | A route is an ordered list of stations with offsets; a timetable generates departures up to its release horizon; a fare table prices a route per passenger type; a pass type is a multi-trip or unlimited pass sold as a product. | Stop (except in the stop list), Line (except lineCode), Schedule, Trip (except a guest's journey) | contracts/satellite/transport.yaml / REV3-21 |
| Applies from | The effective date of a change. Every dated change shows it, and sold items keep their old terms. | Effective date (in labels), Start date (for a change) | contracts/satellite/seating.yaml#updateSeatCategory / TRACKER Actions row 194 |


## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `BO-595` | AI Setup Command Center | B–D | 0 | 15 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-596` | Guided Setup Plan | B–D | 0 | 12 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-597` | AI Configuration Workspace | B–D | 0 | 0 | 6 | 19 | 1 | 0 | — | notStarted (—) |
| `BO-598` | AI Draft Review & Approval | B–D | 2 | 0 | 6 | 20 | 1 | 3 | — | notStarted (—) |
| `BO-599` | Manual Configuration Center | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-600` | Venue, Calendar & Operational Setup | B–D | 0 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-601` | Product, Pricing & Sales Channel Setup | B–D | 16 | 8 | 6 | 5 | 0 | 0 | — | notStarted (—) |
| `BO-602` | POS, Payment & Access Setup | B–D | 13 | 0 | 6 | 10 | 0 | 0 | — | notStarted (—) |
| `BO-603` | Configuration Health & AI Review | B–D | 1 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `BO-604` | Setup Completion & Handoff to Go-Live | B–D | 3 | 0 | 6 | 0 | 0 | 0 | — | notStarted (—) |

## Thin screens in this batch

**BO-595, BO-596, BO-597, BO-598, BO-599, BO-600, BO-603, BO-604 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `BO-595` AI Setup Command Center

**Provide the customer with one central place to understand the overall configuration status and what needs to be completed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Setup Progress) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/setup-go-live/ai-setup-command-center-bo-595` |

**What the spec says about it.** **Moved from P09 `ADM-429` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-429` is retired and never reissued.

**Known gaps.** **AI Setup Command Center declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** The tenant's configuration status in one place: what is done, what remains, what AI can set up.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: getGoLiveReadiness (PLATFORM_TENANT_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): The only component is a field labelled "42% Configuration Complete". (CHG-SBO-015); emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Configuration complete** (progress indicator, from `getGoLiveReadiness`): The percentage is an output of the go-live readiness, not a field.

| Shows | Format | Notes |
|---|---|---|
| Run at | 1 Oct 2026, 14:30 | — |
| Status | chip: Not started, Running, Blocked, Ready with warnings, Ready | — |
| Groups | list or chips (count when long) | — |
| Code | chip: Ticketing and products, Sales channels, Payment, Ticket QR access, Users and … | — |
| Label | text | — |
| Checks | list or chips (count when long) | — |
| Code | text | — |
| Label | text | — |
| Outcome | chip: Pass, Warn, Fail, Skipped | — |
| Detail | text | — |
| Remediation | text | — |
| Blockers | 1,234 | — |
| Warnings | 1,234 | — |
| Signed off by | the name it points at, never the id | — |
| Signed off at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `getGoLiveReadiness` (onLoad, Setup progress)

**Where the user goes next**

- → `BO-100` Venue Home: *Back to Venue Home*
- → `BO-596` Guided Setup Plan: *Guided Setup Plan*
- → `BO-597` AI Configuration Workspace: *AI Configuration Workspace*
- → `BO-598` AI Draft Review & Approval: *AI Draft Review & Approval*
- → `BO-599` Manual Configuration Center: *Manual Configuration Center*
- → `BO-600` Venue, Calendar & Operational Setup: *Venue, Calendar & Operational Setup*
- → `BO-601` Product, Pricing & Sales Channel Setup: *Product, Pricing & Sales Channel Setup*
- → `BO-602` POS, Payment & Access Setup: *POS, Payment & Access Setup*
- → `BO-603` Configuration Health & AI Review: *Configuration Health & AI Review*
- → `BO-604` Setup Completion & Handoff to Go-Live: *Setup Completion & Handoff to Go-Live*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getGoLiveReadiness (GoLiveReadiness):
- runAt: 01/10/2026 09:14
  status: active
  blockers: 12
  warnings: 12
  signedOffAt: 01/10/2026 09:14
- runAt: 30/09/2026 18:02
  status: pending
  blockers: 3
  warnings: 3
  signedOffAt: 30/09/2026 18:02
```

#### Permissions

- `getGoLiveReadiness` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-595` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-595`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 2: Opens AI Setup Command Center → Provide the customer with one central place to understand the overall configuration status and what needs to be completed.
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 4: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 6: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 8: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 10: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 12: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 14: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 16: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F213 branch at step 2 (expected): when Nothing has been set up on AI Setup Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F213 branch at step 2 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-595?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-100`, `BO-596`, `BO-597`, `BO-598`, `BO-599`, `BO-600`, `BO-601`, `BO-602`, `BO-603`, `BO-604`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-596` Guided Setup Plan

**Turn a complex TICVAI implementation into a simple sequence of configuration tasks. Instead of expecting the customer to understand all TICVAI modules, the system creates a personalized setup plan.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each Task Shows) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/setup-go-live/guided-setup-plan-bo-596` |

**What the spec says about it.** **Moved from P09 `ADM-430` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-430` is retired and never reissued.

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape … **Guided Setup Plan declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** A personalised setup plan: ordered tasks with status, estimated time, dependencies and whether AI can do it.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: getGoLiveReadiness (PLATFORM_TENANT_MANAGE). (CHG-SBO-005)
- The table's columns are the workshop pack's labels with no bound response field (0 of 6 labels bound). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every guided plan** (data table)

| Shows | Format | Notes |
|---|---|---|
| Status | text | not in the schema: `Status` |
| Estimated time | text | not in the schema: `Estimated time` |
| Required/optional | text | not in the schema: `Required/Optional` |
| Dependency | text | not in the schema: `Dependency` |
| AI available | text | not in the schema: `AI available` |
| Manual configuration available | text | not in the schema: `Manual configuration available` |

**The selected guided plan** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| Status | text | not in the schema: `Status` |
| Estimated time | text | not in the schema: `Estimated time` |
| Required/optional | text | not in the schema: `Required/Optional` |
| Dependency | text | not in the schema: `Dependency` |
| AI available | text | not in the schema: `AI available` |
| Manual configuration available | text | not in the schema: `Manual configuration available` |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Money columns (AI available, Manual configuration available)**: Money in the region's currency and scale, never a bare number: AED to 2 decimals, OMR/BHD/KWD to 3, the third decimal never rounded away (2.013 stays 2.013); the currency code is shown with the figure. *(source: ADR-0008; ADR-0011; DI-306)*

**Data it reads**: `getGoLiveReadiness` (onLoad, The guided plan)

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The guided plan list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the guided plan untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No guided plan yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the guided plan are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
Every guided plan:
- Status: 57
  Estimated time: 1.8 s
  Required/Optional: 46
  Dependency: 312
  AI available: 19
  Manual configuration available: 57
- Status: 11
  Estimated time: 3 h 20 min
  Required/Optional: 312
  Dependency: 74
  AI available: 233
  Manual configuration available: 11
- Status: 128
  Estimated time: 42 min
  Required/Optional: 74
  Dependency: 19
  AI available: 57
  Manual configuration available: 128
```

#### Permissions

- `getGoLiveReadiness` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-596` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-596`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 3: Works in Guided Setup Plan → Turn a complex TICVAI implementation into a simple sequence of configuration tasks. Instead of expecting the customer to understand all TICVAI modules, the system creates a personalized setup plan.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-596?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-597` AI Configuration Workspace

**Allow the customer to configure TICVAI using natural language. This is the main AI configuration screen.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation) |
| Route | `/setup-go-live/ai-configuration-workspace-bo-597` |

**What the spec says about it.** **Moved from P09 `ADM-431` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-431` is retired and never reissued.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** The customer's own AI configuration workspace in Venue Management (moved from the console on 11 September): describe what you want - a product, membership, pass, promotion, discount rule, pricing calendar, seating zone, opening hours, campaign - and get a draft to review. The one thing to get right: it is drafting, not doing - "Nothing is applied until you approve it" sits on the page.

**Known correction pending (do not draw the wrong version)**

- **requiresModule core.** Why: The workspace needs the AI module. *(source: contracts/satellite/ai.yaml#/components/schemas/AiPolicy (enabledCapabilities configurationAssistant); AI & Intelligence)*

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **kind + description**: Kind as a picker (product, membership, pass, promotion, discount rule, pricing calendar, seating zone, opening hours, campaign) and a free description; follow-up questions come back in the conversation when something required is missing. *(source: contracts/satellite/ai.yaml#generateConfiguration / DI-279 / MoM 18 Sep 4.5)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **draft**: The draft as the owning module's fields with provenance; "Review and approve" opens BO-598. *(source: contracts/satellite/ai.yaml#generateConfiguration)*

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The record list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the record untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No record yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the record are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Consistency with other screens

- Match `ADM-472`: Same conversation and blueprint components as the console assistant.

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
request:
  kind: product
  description: A sunset session ticket for Fridays 18:00-22:00, adults AED 99, kids AED 69, max 800
```

#### Permissions

- `generateConfiguration` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

19 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.41 | System shall allow administrators to upload documents, spreadsheets, brochures, PDFs or price lists and use AI to automatically generate ticket products, pricing structures, capacities, timeslots … | Ticketing Catalogue | CONTRACTED | `generateConfiguration` |
| 8.4.7 | System shall support AI-powered configuration assistance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.8 | System shall support AI-powered workflow assistance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.9 | System shall support AI-powered operational guidance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.10 | System shall support AI-powered knowledge retrieval. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.11 | System shall support AI-powered document search. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.12 | System shall support AI-powered FAQ generation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.13 | System shall support AI-powered configuration recommendations. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.31 | System shall support AI-assisted promotion configuration. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.32 | System shall support AI-assisted discount rule creation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.33 | System shall support AI-assisted pricing calendar generation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.34 | System shall support AI-assisted promotional campaign creation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| … 7 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Phase-one AI priority is a conversational configuration assistant: the admin says e.g. "I want to configure a new product" and it asks the product type (admission, time slot, etc.) and walks through product/promotion setup. *(agreed · MoM 14 Aug 2026, 1. AI Configuration Assistant — Phase-One Scope · DI-279)*

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-597` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-597`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 5: Works in AI Configuration Workspace → Allow the customer to configure TICVAI using natural language. This is the main AI configuration screen.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-597?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] The 1 pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-598` AI Draft Review & Approval

**Provide structured review of AI-generated configuration before it is committed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE` (1 operate); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `planId` (navigation), `actionId` (navigation) |
| Route | `/setup-go-live/ai-draft-review-approval-bo-598` |

**What the spec says about it.** **Moved from P09 `ADM-432` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-432` is retired and never reissued.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the AI & Intelligence process.** Review and approve AI-generated configuration before it is committed: the draft field by field, what it will create and change, validation results, then approve (or send for approval) or reject. Execution is shown step by step and a partial failure rolls back. The one thing to get right: approval is per draft with the before/after visible, and the approver cannot be the requester where the approval tier needs a second person.

**Fixed on main** (the package already carries these; draw what it says): Only generateConfiguration and getActionPlan are declared - no decide or execute operation. (CHG-WIR-012).

#### Inputs: what the user enters or picks

**Form: Approve or reject** (modal, opened by *Approve or reject*; *Approve or reject* calls `decideProposedAction`, *Cancel* sends nothing)

**Collects what `decideProposedAction` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Decision `decision` | segmented control | required | — | Approve · Reject | — | — | `decideProposedAction` body |
| Reason `reason` | text area | optional | — | max length 500 | — | — | `decideProposedAction` body |

Errors to draw in the form: 403 The caller may not decide this proposal (audit R213 (3)): a level 2 proposal and the caller lacks `AI_APPROVE` (`approval-level-requires-manager`), a level 2 …; 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213).

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |
| Approve or reject (secondary button) | `decideProposedAction` POST `/proposed-actions/{actionId}/decide` | inline | ProposedAction | 403 The caller may not decide this proposal (audit R213 (3)): a level 2 proposal and the caller lacks `AI_APPROVE` (`approval-level-requires-manager`), a level 2 …; 409 The action is no longer `proposed` — already … | opens modal first |

**Rules for what is shown** (from the AI & Intelligence process; these refine the tables above and win where they differ)

- **draft review**: Field, proposed value, provenance; affected objects; validation; approval tier. *(source: contracts/satellite/ai.yaml#getActionPlan / contracts/satellite/ai.yaml#/components/schemas/ProposedAction)*
- **execution**: Steps with status; on partial completion, "Rolled back - nothing was left half-configured" with the reason. *(source: DI-965 / MoM 21 Sep 4.9)*

**Data it reads**: `getActionPlan` (onLoad, A plan with its steps)

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The draft review approval list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the draft review approval untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No draft review approval yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the draft review approval are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The action is no longer `proposed` — already decided, or expired (7 days after it was proposed, audit R213). |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
draft:
  product: Sunset Session (Fri)
  fields:
    adult: AED 99.00
    child: AED 69.00
    capacity: 800
    time: 18:00-22:00
  approval: Tier 1 - Venue manager
```

#### Permissions

- `generateConfiguration` → `AI_USE` (operate) · staff
- `getActionPlan` → `AI_USE` (operate) · staff
- `decideProposedAction` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

20 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 1.1.41 | System shall allow administrators to upload documents, spreadsheets, brochures, PDFs or price lists and use AI to automatically generate ticket products, pricing structures, capacities, timeslots … | Ticketing Catalogue | CONTRACTED | `generateConfiguration` |
| 8.4.7 | System shall support AI-powered configuration assistance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.8 | System shall support AI-powered workflow assistance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.9 | System shall support AI-powered operational guidance. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.10 | System shall support AI-powered knowledge retrieval. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.11 | System shall support AI-powered document search. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.12 | System shall support AI-powered FAQ generation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.13 | System shall support AI-powered configuration recommendations. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.31 | System shall support AI-assisted promotion configuration. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.32 | System shall support AI-assisted discount rule creation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.33 | System shall support AI-assisted pricing calendar generation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| 8.4.34 | System shall support AI-assisted promotional campaign creation. | Unified Operations Dashboard | CONTRACTED | `generateConfiguration` |
| … 8 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI actions in progress are shown step by step in an AI action command center; if a process only partly completes (e.g. missing information) it rolls back rather than leaving a product half-configured, and a full change history records everything AI modified. *(client request · MoM 21 Sep 2026, 4.9 Core AI Platform — AI Tools, Agents & Action Orchestration · DI-965)*

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A72** Design a generic, configurable multi-stage approval-workflow engine (approve / reject / return / request-more-information, AI-generated summary, audit trail) applicable to procurement, pricing changes, product creation … *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 18 Aug 2026 · workshop tracker · keyword 'multi-stage approval')*
- **A256** Build approval workflow builder: amount/authority rules, N-of-M groups, delegation, SLA tracking *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*
- **C48** Share BI/reporting and approval workflow documentation *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 8 Sep 2026 · workshop tracker · keyword 'approval workflow')*

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-598` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-598`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 7: Works in AI Draft Review & Approval → Provide structured review of AI-generated configuration before it is committed.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 404, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-598?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel, Approve or reject.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `AI_USE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-599` Manual Configuration Center

**Allow customers who prefer traditional administration to configure TICVAI without AI.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue; in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/setup-go-live/manual-configuration-center-bo-599` |

**What the spec says about it.** **Moved from P09 `ADM-433` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-433` is retired and never reissued.

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built. Removed 2 October 2026 (CHG-WIR-015): The screen is navigation; a full configuration read (getTenantConfig) is not needed (design-notes correction white-label BO-599).

**From the White Label & CMS process.** For a customer who prefers traditional administration to the AI setup: a plain index of every configuration area (including the white-label ones) with links to their screens. It configures nothing itself.

**Fixed on main** (the package already carries these; draw what it says): The screen's only call is getTenantConfig and its pack gives no content. (CHG-WIR-015).

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Access (primary button) | navigation or local | — | — | — | — |
| Queue (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the White Label & CMS process; these refine the tables above and win where they differ)

- **Configuration index**: Areas grouped as in the Venue Management app; for white-label, links to CMS-001, CMS-102 and the CMS screens. *(source: screens/P08-venue-back-office.yaml#BO-599)*

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The manual list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the manual untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No manual yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the manual are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access. |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
areas:
- Site and brand
- Booking flows
- Products
- Access
- Queue
```

#### Permissions

**A refused user sees:** Not shown: nothing on this screen needs a permission of its own; the app's sign-in decides access.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-599` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-599`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 9: Works in Manual Configuration Center → Allow customers who prefer traditional administration to configure TICVAI without AI.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-599?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Access, Queue.
- [ ] Every transition is wired: `BO-595`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-600` Venue, Calendar & Operational Setup

**Provide a guided workspace for the fundamental venue configuration.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `venueId` (session) |
| Route | `/setup-go-live/venue-calendar-operational-setup-bo-600` |

**What the spec says about it.** **Moved from P09 `ADM-434` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-434` is retired and never reissued.

**Known gaps.** **Venue, Calendar & Operational Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Guided setup of a venue's fundamentals during onboarding: name, address, time zone, calendar day start, operating hours. Region settings (currency, date format) are inherited and shown read-only.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: setVenueSettings: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#setVenueSettings)*

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save venue settings (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Rules for what is shown** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Inherited from region**: Currency, decimal scale, date format, time zone and fiscal year shown as inherited and not editable here. *(source: ADR-0011)*

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue calendar operational list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the venue calendar operational untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No venue calendar operational yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the venue calendar operational are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 An enable the venue cannot evidence. Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender … |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **setVenueSettings answers 422**: Show it as something the person can act on, not a failure: **An enable the venue cannot evidence.** Biometrics switched on without a DPIA reference and a consent-notice acknowledgement, or device-assisted gender verification where no device in the venue reports `genderClassification`. `errors[]` names each missing field or the missing capability. *(source: contracts/spine/tenancy.yaml#setVenueSettings)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
venue:
  name: AquaCove Abu Dhabi
  timeZone: Asia/Dubai
  currency: AED (inherited)
  dayStartsAt: 05:00
  opening: 10:00-18:00
```

#### Permissions

- `setVenueSettings` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-600` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-600`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 11: Works in Venue, Calendar & Operational Setup → Provide a guided workspace for the fundamental venue configuration.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-600?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save venue settings, Cancel.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-601` Product, Pricing & Sales Channel Setup

**Configure the customer's initial products and where they can be sold.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE` (2 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `priceListId` (navigation) |
| Route | `/setup-go-live/product-pricing-sales-channel-setup-bo-601` |

**What the spec says about it.** **Moved from P09 `ADM-435` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-435` is retired and never reissued.

**Known gaps.** **Product, Pricing & Sales Channel Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either … Removed 2 October 2026 (CHG-WIR-025): setChannelListing lists products on OTAs (subscription, PARTNER_MANAGE), not on the venue's own channels; first-time channel setup is publishChannelAvailability. …

**From the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process.** Part of go-live setup for a new tenant: the customer's own administrator sets its first products' prices and lists them on channels. Moved from the TICVAI Console because the customer works it inside their tenant.

**Fixed on main** (the package already carries these; draw what it says): setChannelListing lists on OTAs, not on the venue's own channels. (CHG-WIR-025); No read operation: the screen declares only setPrices, setChannelListing and nothing that returns the current configuration. (CHG-WIR-025).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Price | select field | — | — | — | — | — | — |
| Tax | select field | — | — | — | — | — | — |
| Validity | select field | — | — | — | — | — | — |
| Capacity | select field | — | — | — | — | — | — |
| Eligibility | select field | — | — | — | — | — | — |
| Sales Channels | select field | — | — | — | — | — | — |
| Ticket Media | select field | — | — | — | — | — | — |

**Form: Publish to channels** (modal, opened by *Publish to channels*; *Publish to channels* calls `publishChannelAvailability`, *Cancel* sends nothing)

**Collects what `publishChannelAvailability` sends before it is called.** Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Channels `channels` | repeatable rows | optional | — | — | — | Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates | `publishChannelAvailability` body |
| Channel `channels[].channel` | select | optional | — | POS · Kiosk · Web · Mobile · B2B · Ota · Call centre | — | — | `publishChannelAvailability` body |
| Enabled `channels[].enabled` | toggle | optional | — | — | — | — | `publishChannelAvailability` body |
| Sites `channels[].siteIds` | list of values (chips) | optional | — | — | — | Specific sites/webstores; empty = all | `publishChannelAvailability` body |
| POS groups `channels[].posGroupIds` | list of values (chips) | optional | — | — | — | Specific POS groups; empty = all | `publishChannelAvailability` body |
| Venues `channels[].venueIds` | list of values (chips) | optional | — | — | — | Availability by venue; empty = all the product's venues | `publishChannelAvailability` body |
| Effective from `channels[].effectiveFrom` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Effective to `channels[].effectiveTo` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `publishChannelAvailability` body |
| Product `productId` | picker: choose a product | optional | — | — | shows names, sends the id | Product id | `publishChannelAvailability` body |

**Rules for these inputs** (from the Ticketing & Guest Commerce, as the venue and TICVAI configure and run it process; these refine the tables above and win where they differ)

- **starter prices**: A short price grid for the products created in setup, per channel. *(source: contracts/spine/catalogue.yaml#setPrices / DI-833)*

#### Outputs: what the screen shows and produces

**Shown**

**Prices** (data table, from `listPrices`)

| Shows | Format | Notes |
|---|---|---|
| Items | list or chips (count when long) | — |
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Price list | the name it points at, never the id | — |
| Variant | the name it points at, never the id | — |
| Amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax code | the name it points at, never the id | — |
| Next cursor | text | — |
| Has more | yes / no (icon or chip) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | `publishChannelAvailability` PUT `/channel-availability` | ChannelPublicationAvailabilityInput | ChannelPublicationAvailabilityView | — | opens modal first |
| Publish to channels (secondary button) | `publishChannelAvailability` PUT `/channel-availability` | ChannelPublicationAvailabilityInput | ChannelPublicationAvailabilityView | — | opens modal first |

**Data it reads**: `listPrices` (onLoad, The prices already in the list)

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The product pricing sales configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the product pricing sales untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No product pricing sales configured yet. Offers no create action — this screen declares no operation that makes one and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Currency or scale mismatch against the region |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
setup:
  tenant: Pearl Museum
  products:
  - General admission
  - Guided tour
  prices:
    General admission Adult: AED 50.00
```

#### Permissions

- `setPrices` → `PRICE_CONFIGURE` (configure) · staff
- `listPrices` → `PRICE_VIEW` (read) · staff, partner
- `publishChannelAvailability` → `PRODUCT_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.10.4 | The system should allow sales of free tickets. These tickets can be configured as a standard ticket with a price of zero or as a full price ticket with a 100% discount. | Ticketing Sales | CONTRACTED | `setPrices` |
| 7.4.17 | For each PLU, it is possible to manage its Unit price and the related currency | F&B POS | CONTRACTED | `setPrices` |
| 7.4.19 | For each PLU, it is possible to manage its VAT rate | F&B POS | CONTRACTED | `setPrices` |
| 19.2.22 | Dynamic Pricing Display - System shall display dynamic pricing. | Guest Mobile App & Branding | CONTRACTED | `listPrices` |
| 2.9.8 | The system should be able to regroup prices by category: Full price / reduced price / complimentary. | Ticketing Sales | CONTRACTED | `listPrices` |

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-601` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-601`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 13: Works in Product, Pricing & Sales Channel Setup → Configure the customer's initial products and where they can be sold.

#### Acceptance for the design

- [ ] Every input above is drawn (16), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (8 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-601?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: , Publish to channels.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `PRICE_CONFIGURE`, `PRICE_VIEW`, `PRODUCT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-602` POS, Payment & Access Setup

**Guide the customer through the key operational configuration required to actually sell and validate tickets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `WORKSTATION_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configured; Configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `workstationId` (session) |
| Route | `/setup-go-live/pos-payment-access-setup-bo-602` |

**What the spec says about it.** **Moved from P09 `ADM-436` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-436` is retired and never reissued. Progress ("6 of 12", "10") is shown from the go-live readiness on BO-595, not as fields here.

**Known gaps.** **POS, Payment & Access Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Onboarding step that sets up the first tills, payment methods and gates so the venue can sell and validate tickets. Each item ends in a configured workstation or access point; progress shown as done of total.

**Fixed on main** (the package already carries these; draw what it says): Field labels "6/12" and "10" are data rendered as fields. (CHG-SBO-015).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| POS Name | select field | — | — | — | — | — | — |
| Location | select field | — | — | — | — | — | — |
| Device | select field | — | — | — | — | — | — |
| Sales Profile | select field | — | — | — | — | — | — |
| Payment Methods | select field | — | — | — | — | — | — |
| Receipt | select field | — | — | — | — | — | — |
| User Assignment | select field | — | — | — | — | — | — |
| Gate | select field | — | — | — | — | — | — |
| Reader | select field | — | — | — | — | — | — |
| Entry/Exit | select field | — | — | — | — | — | — |
| Ticket Rules | select field | — | — | — | — | — | — |
| Re-entry | select field | — | — | — | — | — | — |
| Validation Mode | select field | — | — | — | — | — | — |

**Rules for these inputs** (from the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process; these refine the tables above and win where they differ)

- **Scope this applies at**: Not a free choice; each write has one level and the selector says it: configureWorkstation: set for the venue chosen in the venue filter, showing beside each value the tenant or region value it overrides. Nearest ancestor wins; a workstation is assigned a profile, never configured. *(source: ADR-0018; ADR-0029; screens/_patterns.yaml#configEditor; contracts/spine/tenancy.yaml#configureWorkstation)*

#### Outputs: what the screen shows and produces

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The pos payment access configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the pos payment access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No pos payment access configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 A shift is open on this workstation. The change is not applied; it can be made once the shift has closed.; 422 No board would apply: the request sends no `saleBoardId` and the workstation's outlet has none (`sale-board-required`; CHG-CSP-006). |

#### Edge cases to draw

- **A person whose grants cover only some venues, or a link to a record in another venue**: The venue filter lists only venues in the session's scope (Session.scope, resolved at sign-in); a record outside it renders Not found, deliberately indistinguishable from absent, never a 'you may not see venue X' message. *(source: ADR-0011; contracts/shared/common.yaml#/components/schemas/Problem; contracts/spine/identity.yaml#getCurrentSession)*
- **configureWorkstation answers 409**: Show it as something the person can act on, not a failure: **A shift is open on this workstation.** The change is not applied; it can be made once the shift has closed. Names the open shift. *(source: contracts/spine/tenancy.yaml#configureWorkstation)*

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
progress: 6 of 12 configured
till:
  name: Main Gate Till 1
  location: Main Gate
  device: Sunmi T2s
  salesProfile: Ticketing till
  paymentMethods:
  - card
  - cash
```

#### Permissions

- `configureWorkstation` → `WORKSTATION_CONFIGURE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

10 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.1.30 | Administrators shall remotely manage POS layouts, products, promotions, payment methods, permissions, and device settings without local intervention. | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.2.2 | The system should allow creation of Mobile POS, depending on the activities, activation on demand, either on site or off site. Mobile-POS should have all the same features as a normal POS. The sales … | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.12.21 | Mobile POS system support: 1. Sales functionality: Must support the sale of park admission tickets and Quick Passes at least 2. Ticket issuance: Must support printing physical tickets for purchased … | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.13.19 | This process is expected to be possible not only at front gate but on all POS in or out of the venue. | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.13.25 | The POS can print on more than 3 different printers (tickets, wristbands, RFID, …) | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.13.27 | It is possible to perform POS sales on the fly on tablet computers or mobile POS. | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.13.28 | Sales on the fly shall be used to prepare the sales at Front gate. | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 2.13.29 | Sales on the fly shall be used to print tickets or wristbands | Ticketing Sales | CONTRACTED | `configureWorkstation` |
| 16.3.13 | Device Configuration Management - System shall support device configuration management. | Device Management | CONTRACTED | `configureWorkstation` |
| 16.3.14 | Remote Configuration - System shall support remote configuration of devices. | Device Management | CONTRACTED | `configureWorkstation` |

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-602` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-602`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 15: Works in POS, Payment & Access Setup → Guide the customer through the key operational configuration required to actually sell and validate tickets.

#### Acceptance for the design

- [ ] Every input above is drawn (13), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-602?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `WORKSTATION_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] The 2 edge case(s) from the process notes are drawn.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-603` Configuration Health & AI Review

**Allow AI to analyze the complete configuration and identify missing, inconsistent, or potentially incorrect settings before formal go-live validation.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Configuration Health) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/setup-go-live/configuration-health-ai-review-bo-603` |

**What the spec says about it.** **Moved from P09 `ADM-437` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-437` is retired and never reissued.

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** AI review of the whole configuration for missing, inconsistent or risky settings before validation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: runGoLiveValidation (PLATFORM_TENANT_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| 84% Healthy | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The health review configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the health review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No health review configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
health: 84% healthy
findings:
- Refund policy missing for AquaCove Muscat
- Two sale boards with no products
- Tax code not set for Wave Shop
```

#### Permissions

- `runGoLiveValidation` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-603` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-603`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 17: Works in Configuration Health & AI Review → Allow AI to analyze the complete configuration and identify missing, inconsistent, or potentially incorrect settings before formal go-live validation.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-603?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `BO-595`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `BO-604` Setup Completion & Handoff to Go-Live

**Confirm that customer configuration is sufficiently complete to begin formal Board 8 validation. Board 8 is the final quality and operational control layer between configuration and production launch.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P08 Venue Management (web) |
| Module | Setup & Go-Live · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `PLATFORM_TENANT_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area. · LTR and RTL · light, dark theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Export Configuration Summary; AI Creates Configuration Proposal; Configuration Saved) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/setup-go-live/setup-completion-handoff-to-go-live-bo-604` |

**What the spec says about it.** **Moved from P09 `ADM-438` on 11 September 2026.** Board 7 is worked by the new customer's own administrator inside their tenant, not by TICVAI; `tools/applied/apply-subscription-placement.py` records why. `ADM-438` is retired and never reissued.

**Known gaps.** **Setup Completion & Handoff to Go-Live declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either …

**From the Platform Foundation (identity, roles and security; tenancy, venues and devices; platform operations; subscription and licensing; approval workflows; developer portal and public API; digital asset management) process.** Confirm configuration is complete enough to start go-live validation.

**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the corrected version and mark what waits on the contract, as the open change entry says)

- A Venue Management screen calls operations gated by TICVAI-only permissions: getGoLiveReadiness (PLATFORM_TENANT_MANAGE). (CHG-SBO-005)

**Fixed on main** (the package already carries these; draw what it says): emptyFirstRun says it 'carries the create action', and the screen declares no operation that creates anything. (CHG-SBO-002).

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Board 7 — AI Governance Model | text field | — | — | — | — | — | — |
| ↓ | select field | — | — | — | — | — | — |
| Customer Review / Approval where required | text field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getGoLiveReadiness` (onLoad, Handoff to go-live)

**Where the user goes next**

- → `BO-595` AI Setup Command Center: *Back to AI Setup Command Center*
- → `BO-605` Go-Live Readiness Command Center: *Go-Live Readiness Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The completion handoff go-live configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the completion handoff go-live untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No completion handoff go-live configured yet. Offers no create action — this screen declares no operation that makes one; distinct from a filter that matched nothing. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Sample data for the mock-up

Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema outranks them where a value would not validate.

```yaml
getGoLiveReadiness (GoLiveReadiness):
- runAt: 01/10/2026 09:14
  status: active
  blockers: 12
  warnings: 12
  signedOffAt: 01/10/2026 09:14
- runAt: 30/09/2026 18:02
  status: pending
  blockers: 3
  warnings: 3
  signedOffAt: 30/09/2026 18:02
```

#### Permissions

- `getGoLiveReadiness` → `PLATFORM_TENANT_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 3 for P08 · Setup & Go-Live, 24 for all of P08, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P08 Venue Management.dc.html#bo-604` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS159 Subscription Licensing AI Self Service Board 7.dc.html#bo-604`
- Workshop pack: Subscription_Licensing_AI_Self_Service.pdf board 7
- Flow F213 *Subscription Licensing AI Self Service board 7: AI Setup Command Center*, step 19: Works in Setup Completion & Handoff to Go-Live → Confirm that customer configuration is sufficiently complete to begin formal Board 8 validation.

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#BO-604?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `BO-595`, `BO-605`.
- [ ] Every gated control is gated: `PLATFORM_TENANT_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P08 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/TICVAI_POS_Terminal_client_approved.html`: the client-approved POS, for operator density and components.
- `sources/designs/TICVAI_Mobile.dc.html`: for finish and motion.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-028, DI-029, DI-030, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-041, DI-042, DI-043, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051, DI-052 (each is in the design inputs below).

**Workshop tracker rows about P08 as a whole** (1: 1 open, 0 closed). Open first; a closed row says where it went on 30 September.

- **S8** Venue Management back-end configuration wireframes *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P08 Venue Management

- Qossai: configuration screens should consolidate related functionality, potentially merging 3-4 previously separate screens into one, rather than the repetitive one-screen-per-concept pattern of the AI-built reference system. *(agreed · MoM 24 Sep 2026, 4.5 Screen Consolidation Philosophy · DI-987)*
- **Open question.** Open: should AI monitoring live in one centralised AI command dashboard or be distributed as widgets in each functional module's own dashboard? Allam: Softlabs' call; the current proposal is illustrative and Softlabs may propose a better structure. *(open · MoM 18 Sep 2026, 4.4 AI Governance — Risk, Compliance & Continuous Monitoring · DI-936)*
- Simulation functionality stays embedded within each relevant configuration section rather than being consolidated, since it tests that section's own configuration. *(agreed · MoM 8 Sep 2026, 4.11 Dashboard & Reporting Module Consolidation Strategy · DI-722)*
- Client boards (POS Frontline, F&B, Retail, Inventory & Procurement) share one architecture: six boards of ten screens per domain, a command centre first and an AI/analytics board last, under the hierarchy Company > Venue > Department > Workstation > Operator/Shift > Transaction > Exception > Reconciliation > Analytics. *(agreed · client-design-boards-audit 20 Aug 2026, Opening / What the boards give us · DI-400)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- **Open question.** Allam: a user's visibility must be restrictable to specific outlets (an F&B manager of one outlet should not see other outlets' items); also relevant for ticketing/event-specific access. Implementation approach still open. *(open · MoM 18 Aug 2026, 4.6 Role-Based & Outlet-Level Access Control — Open Item · DI-331)*
- Access loads automatically at login on POS and web/admin. A user with one role logs straight in; a user with several roles (e.g. admin, cashier, supervisor, manager) is prompted to choose which role to use. *(agreed · MoM 12 Aug 2026, 4. Multiple Roles per User and Role Switching · DI-249)*
- Back office is role-driven from any device: a finance user signing in from a workstation, laptop or home sees only finance reports and related information. *(agreed · MoM 12 Aug 2026, 3. Role-Based Access and Workstation-Linked Front-End · DI-248)*
- Built-in help menu with step-by-step tutorials with screenshots for common tasks (e.g. how to sell a ticket at the POS). *(client request · MoM 7 Aug 2026, 8. Legacy POS Layout Designer & System Logging · DI-160)*
- Custom data-capture fields ("data mask") at account, event, extended-ticket and product level: field types text, dropdown, radio, true/false; multi-language labels; validation (min/max length, required/optional); reusable value lists (e.g. country list). Standard fields come out of the box. *(agreed · MoM 7 Aug 2026, 6. Data Mask: Flexible Custom Data Capture · DI-155)*
- Load/traffic dashboards respect the tenancy model: a venue manager sees traffic for their own venue only. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-061)*
- Allam: queue management is built into the system (not third-party) so traffic entering the site can be throttled from the back office itself. *(agreed · MoM 31 Jul 2026, 4. Non-Functional Requirements: Scalability & Availability · DI-060)*
- **Open question.** Proposed tenant hierarchy Tenant > Organization/Brand > Region > Branch > Venue > Department, under review against TICVAI's own organisational hierarchy before finalising. *(open · MoM 30 Jul 2026, 2. Proposed Multi-Tenant Hierarchy · DI-055)*
- Documentation deliverable includes user guides and help content; the preview shows a TICVAI Help Center with categories (Getting Started, Events, Tickets, Orders, Payments, Memberships, Access Control, Reports, Integrations), a "Welcome to TICVAI" getting-started article and Quick Links (Create an Event, Set Pricing, Manage Access, View Reports). *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - What We Deliver / Key Deliverables Preview · DI-052)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- AI Assistant panel: a short framing ("Based on last 30 days, here are 3 actions that can improve your revenue") then actionable recommendations, each with its potential impact (e.g. "Increase pricing for VIP seats, +12%") and a chevron, plus "View all recommendations". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - AI Panels · DI-043)*
- Chart cards: title with period dropdown ("This Week"), headline metrics with deltas (Tickets Sold 12,840 +8.7%, Visitors, Conversion). Data visualisations must be easy to read. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Charts · DI-041)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*
- Back-office shell: collapsible left sidebar with Overview, Events, Tickets, Orders, Customers, Memberships, Access Control, POS, Reports, Analytics, AI Assistant, Settings, and the signed-in user (name, role) at the bottom; top bar with global search (Cmd+K), current time and date, Notifications with unread dot, and user menu. *(agreed · Design Vision Book 29 Jul 2026, 04 Dashboard Vision (p4) - navigation shell · DI-030)*
- Dynamic KPIs, forecasts and real-time insights; role-based dashboards, preferences and smart shortcuts for every user (e.g. greeting "Good morning, Ahmed" on the home screen, p2). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Smarter Data / Personalized Experience · DI-028)*
- Reports and historical searches must still retrieve archived transactions when required; the retention period (e.g. keep 3 of 5+ years live) is configurable per customer, archival manual or automated. *(agreed · MoM 28 Jul 2026, 23. Database Optimisation and Archiving · DI-018)*
- Back-office controls for the waiting room: configurable maximum active users and admission intervals, set per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-017)*

### In P08 · Setup & Go-Live

- Go-live readiness validates end-to-end: products set up correctly, pricing displays correctly, and a full test transaction completes in the target environment. *(client request · MoM 10 Sep 2026, 4.14 Go-Live Readiness Validation · DI-835)*
- After contract, TICVAI provisions the tenant with a basic setup reflecting the tier and licensed modules (e.g. mobile app, B2C, B2B enabled as contracted) before handover; AI can assist initial product/event/ticket setup following the same process as manual setup. *(client request · MoM 10 Sep 2026, 4.12 Tenant Provisioning & Go-Live Setup · DI-833)*
- AI-created product/ticket configuration likewise asks follow-ups before finalising (e.g. is the ticket admission, time-slot or seat-assignment type; which categories and discounts apply). *(agreed · MoM 8 Sep 2026, 4.7 AI-Assisted Report & Configuration Generation · DI-713)*

**2 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"configureWorkstation": {"method":"PUT","path":"/workstations/{workstationId}","contract":"tenancy","summary":"Configure a workstation","permission":"WORKSTATION_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConfigureWorkstationRequest","responds":"Workstation"},
"decideProposedAction": {"method":"POST","path":"/proposed-actions/{actionId}/decide","contract":"ai","summary":"Approve or reject a proposal","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ProposedAction"},
"generateConfiguration": {"method":"POST","path":"/generate/configuration","contract":"ai","summary":"Draft a configuration from a description","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GeneratedConfiguration"},
"getActionPlan": {"method":"GET","path":"/action-plans/{planId}","contract":"ai","summary":"A plan with its steps","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiActionPlanDetail"},
"getGoLiveReadiness": {"method":"GET","path":"/go-live-readiness","contract":"subscription","summary":"Everything that must pass before a tenant can sell","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":"tenantId","in":"query","required":true}],"requestBody":null,"responds":"GoLiveReadiness"},
"listPrices": {"method":"GET","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"List prices in a list","permission":"PRICE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishChannelAvailability": {"method":"PUT","path":"/channel-availability","contract":"catalogue","summary":"Channel Publication & Availability","permission":"PRODUCT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ChannelPublicationAvailabilityInput","responds":"ChannelPublicationAvailabilityView"},
"runGoLiveValidation": {"method":"POST","path":"/go-live-readiness/run","contract":"subscription","summary":"Run the validation plan against a tenant","permission":"PLATFORM_TENANT_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"platform","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setPrices": {"method":"PUT","path":"/price-lists/{priceListId}/prices","contract":"catalogue","summary":"Set prices in bulk","permission":"PRICE_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"setVenueSettings": {"method":"PUT","path":"/venues/{venueId}/settings","contract":"tenancy","summary":"Set support hours, quiet hours, segregated access and alerting","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"VenueSettings","responds":"VenueSettings"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AiActionPlan": {"type":"object","x-ticvai-persistence":"ai.action_plan","description":"**A plan: plan, validate, simulate, approve, execute, with rollback** (design 2.2 D, 3.8; AIC-086..107). Independent of any conversation (AIC-102). Its steps are `ai.action_step`; the change set is hashed so what was approved is what runs (AIC-181).","required":["origin","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"origin":{"type":"string","enum":["configurationSession","generateConfiguration","assistant","riskCase","operationalRequirement","rollback"]},"originRef":{"type":"string","nullable":true},"summary":{"type":"string"},"status":{"type":"string","enum":["draft","validated","simulated","awaitingApproval","approved","executing","paused","completed","partiallyCompleted","failed","compensated","cancelled","rolledBack"],"readOnly":true},"autonomyLevel":{"$ref":"#/components/schemas/AiAutonomyLevel"},"approvalTier":{"type":"integer","minimum":1,"maximum":2,"description":"The approval tier (1 or 2), the floor the approvals matrix adds to (design 3.8). Not an autonomy level."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request, where tier 2 or the matrix caught the plan."},"proposedActionId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.proposed_action","description":"The `ai.proposed_action` the plan is presented as for a decision."},"changeSetHash":{"type":"string","readOnly":true},"governanceOutcome":{"allOf":[{"$ref":"#/components/schemas/AiGovernanceOutcome"}],"readOnly":true},"policyVersionRef":{"type":"string","readOnly":true,"description":"The governance policy version that decided it."},"simulation":{"type":"object","additionalProperties":true,"nullable":true,"readOnly":true,"description":"Current versus proposed state, channels, future orders and issued tickets affected (flow D step 4)."},"partialCompletionAllowed":{"type":"boolean","default":false,"description":"Where governance allows a partial completion; otherwise a failure compensates in reverse dependency order (AIC-098, AIC-134)."},"rollbackOfPlanId":{"type":"string","format":"uuid","nullable":true,"x-ticvai-references":"ai.action_plan"},"requestedByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"x-ticvai-references":"identity.principal"},"createdAt":{"type":"string","format":"date-time","readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AiActionPlanDetail": {"type":"object","x-ticvai-persistence":"none — ai.action_plan with its ai.action_step rows","description":"A plan with its steps in DAG order.","required":["plan","steps"],"properties":{"plan":{"$ref":"#/components/schemas/AiActionPlan"},"steps":{"type":"array","items":{"$ref":"#/components/schemas/AiActionStep"}}}},
"AiActionStep": {"type":"object","x-ticvai-persistence":"ai.action_step","description":"One step of a plan: a registered tool against `targetContract.targetOperation` at a contract version (AIC-095), with payload, provenance, compensation and the idempotency key `plan:{id}:step:{n}`. **Scoped through its plan** (`platform.apply_parent_rls`). Each step records its target object's version; drift pauses the plan (AIC-182).","required":["planId","stepNumber","toolKey","targetContract","targetOperation","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"planId":{"type":"string","format":"uuid","x-ticvai-references":"ai.action_plan"},"stepNumber":{"type":"integer","minimum":1},"dependsOn":{"type":"array","items":{"type":"integer","minimum":1},"description":"Step numbers that must succeed first. The plan is a DAG."},"toolKey":{"type":"string"},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"contractVersion":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body of `targetOperation`, validated against it before the plan is approved."},"provenance":{"$ref":"#/components/schemas/AiProvenance"},"idempotencyKey":{"type":"string","readOnly":true},"targetObjectRef":{"type":"string","nullable":true},"targetObjectVersion":{"type":"string","nullable":true,"description":"The version the step was planned against. A different version at execution is drift."},"reversible":{"type":"boolean"},"compensation":{"type":"object","additionalProperties":true,"nullable":true},"status":{"type":"string","enum":["pending","validated","running","succeeded","failed","compensated","skipped","paused"],"readOnly":true},"attempts":{"type":"integer","minimum":0,"maximum":3,"readOnly":true,"description":"Bounded at 3 (AIC-135)."},"lastError":{"type":"string","nullable":true,"readOnly":true},"resultRef":{"type":"string","nullable":true,"readOnly":true,"description":"The owning service's response: success is its answer, not a model's judgement (AIC-097)."},"startedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"completedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"CatalogueState": {"x-ticvai-persistence":"none — computed from workstation bundle_version","type":"object","description":"The workstation's local catalogue position. A terminal beyond `staleAfter` must refuse to trade rather than transact against stale prices.\n","required":["appliedBundleVersion","appliedAt","staleAfter","isStale"],"properties":{"appliedBundleVersion":{"type":"string"},"appliedAt":{"type":"string","format":"date-time"},"staleAfter":{"type":"string","format":"date-time","description":"Beyond this the terminal refuses to trade."},"isStale":{"type":"boolean"},"pendingBundleVersion":{"type":"string","nullable":true,"description":"Published but not yet applied."}}},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ChannelPublicationAvailabilityInput": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — request only; **no existing table shares a single field with this**, so nothing the package stores today is what this configures","description":"**What Channel Publication & Availability submits.** The configurable fields from the pack's directory for this screen; the metrics the screen displays are deliberately absent, because a figure the system computed is not a figure a client may send back.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"productId":{"type":"string","description":"Product id","format":"uuid"}}},
"ChannelPublicationAvailabilityView": {"type":"object","x-ticvai-drafted-shape":true,"x-ticvai-persistence":"none — projection over catalogue state, assembled at read time from tables that already exist","description":"**What Channel Publication & Availability displays.** Read from the workshop pack's own display and configuration directory for this screen; each property names the sentence it came from. **Not a row** - the screen is a view over the module's existing state.","properties":{"channels":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"enabled":{"type":"boolean"},"siteIds":{"type":"array","items":{"type":"string"},"description":"Specific sites/webstores; empty = all"},"posGroupIds":{"type":"array","items":{"type":"string"},"description":"Specific POS groups; empty = all"},"venueIds":{"type":"array","items":{"type":"string"},"description":"Availability by venue; empty = all the product's venues"},"effectiveFrom":{"type":"string","format":"date-time","nullable":true},"effectiveTo":{"type":"string","format":"date-time","nullable":true}}},"description":"Channels the product is published on, with channel-specific sites, POS groups, venues and effective dates"},"publicationPreview":{"type":"array","items":{"type":"object","properties":{"channel":{"$ref":"#/components/schemas/Channel"},"venueId":{"type":"string"},"exposed":{"type":"boolean"},"reason":{"type":"string","nullable":true}}},"description":"Preview of where the product will actually be on sale"},"validationIssues":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["channelNotConfigured","noPriceForChannel","noCapacityAllocation","productNotApproved","venueNotAssigned"]},"message":{"type":"string"}}},"description":"Missing channel dependencies (decided 29 September, readiness close-out)"},"productId":{"type":"string","description":"Product id","format":"uuid"},"issuedEntitlementsUnaffected":{"type":"integer","description":"Valid issued tickets/entitlements that remain valid whatever the channel change (pack p.10 Important Rule)"}}},
"ConfigureWorkstationRequest": {"type":"object","required":["name"],"properties":{"cashierInputMode":{"type":"string","enum":["keyboard","touch","scanner","hybrid"],"default":"hybrid","description":"BL-061. **A till operator who touch-types is slower on a touchscreen and a new starter is faster.** The mode is per workstation because the operator is.\n"},"guestDisplayContent":{"type":"array","description":"**What the guest-facing screen shows while a sale is in progress.** Line items always; the rest is the venue's choice — and **a second screen showing nothing is a second screen the guest ignores when it does show something that matters.**\n","items":{"type":"string","enum":["lineItems","total","loyaltyBalance","promotions","branding","upsell","queuePosition"]}},"loadedMediaStockId":{"type":"string","format":"uuid","nullable":true,"description":"BL-095. **Neither which stock a printer is loaded with nor how much is left.** A till that runs out of wristbands mid-queue is an outage nobody predicted, and the stock is inventory like anything else — this names which.\n"},"mediaStockRemaining":{"type":"integer","nullable":true,"readOnly":true,"description":"Decremented on issue. **The number that turns a surprise into a reorder**, and it is read-only because the count comes from what was printed rather than from somebody's estimate.\n"},"name":{"type":"string","maxLength":200},"saleBoardId":{"type":"string","format":"uuid","nullable":true,"description":"**This till's own layout, overriding its outlet's** (DEC-183; CHG-CSP-006). Optional since 2 October 2026: absent or null, the till uses `Outlet.saleBoardId`.\n"},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"The outlet this till stands in (CHG-CSP-006)."},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"This till's drawer limit; null inherits `VenueSettings.cashDrawerLimit` (DEC-179; CHG-CSP-016)."},"departmentId":{"type":"string","format":"uuid","nullable":true},"accessPointId":{"type":"string","format":"uuid","nullable":true},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true},"isActive":{"type":"boolean","default":true}}},
"DeploymentProfile": {"type":"string","description":"How this workstation obtains catalogue and inventory (ADR-0013).\n- `terminalLocal` — own SQLite, leases direct from the cell. Small venues, 4G sites - `venueEdge` — own SQLite, distributed via the venue edge node which holds the\n  venue lease and sub-leases to terminals. Mid and large venues, stadium gates\n- `thin` — no local catalogue, server reads. Non-transactional surfaces only\n","enum":["terminalLocal","venueEdge","thin"]},
"DeviceBinding": {"x-ticvai-persistence":"platform.device","type":"object","required":["kind","driver"],"properties":{"kind":{"$ref":"#/components/schemas/DeviceKind"},"driver":{"type":"string","description":"Driver identifier. Adding a vendor is a driver plus configuration, never a core change — every venue arrives with hardware not previously seen.\n"},"identifier":{"type":"string","description":"Serial","port or network address.":null},"isRequired":{"type":"boolean","default":false,"description":"When true, the workstation refuses to open a shift if the device is absent.\n"}}},
"GeneratedConfiguration": {"type":"object","x-ticvai-persistence":"none — a draft, applied through the owning contract; the draft itself is the ai.proposed_action row named by proposedActionId","required":["proposedActionId","kind","targetContract","targetOperation","payload"],"properties":{"proposedActionId":{"type":"string","format":"uuid","description":"**The `ai.proposed_action` row this draft was written as**, and the id `decideProposedAction` takes. Without it a reviewer (BO-598) has a draft and no way to approve it.\n"},"kind":{"type":"string","enum":["product","membership","pass","promotion","discountRule","pricingCalendar","seatingZone","operatingHours","campaign"],"description":"The `kind` the request asked for."},"targetContract":{"type":"string"},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"**Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, validated against that operation before it is returned — this contract does not restate thirty other contracts' request schemas.\n"},"assumptions":{"type":"array","description":"**What it had to guess.** An admin reviewing a draft needs to know which fields came from what they said and which the assistant chose, or they approve a decision they did not make.\n","items":{"type":"object","properties":{"field":{"type":"string"},"value":{"type":"string"},"reason":{"type":"string"}}}},"clarificationsNeeded":{"type":"array","description":"What it could not resolve and should ask about.","items":{"type":"string"}},"confidence":{"type":"number","nullable":true},"traceId":{"type":"string"},"planId":{"type":"string","format":"uuid","description":"The one-step `ai.action_plan` the draft was written as (AI design 2.3), readable with `getActionPlan`."}}},
"GoLiveReadiness": {"type":"object","x-ticvai-persistence":"subscription.go_live_readiness","description":"Board 8. **The screen that stops a launch going wrong in public.**","properties":{"tenantId":{"type":"string","format":"uuid"},"runAt":{"type":"string","format":"date-time"},"status":{"type":"string","enum":["notStarted","running","blocked","readyWithWarnings","ready"]},"groups":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string","enum":["ticketingAndProducts","salesChannels","payment","ticketQrAccess","usersAndSecurity","integrations","communications","financialSetup"]},"label":{"type":"string"},"checks":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"outcome":{"type":"string","enum":["pass","warn","fail","skipped"]},"detail":{"type":"string","nullable":true},"remediation":{"type":"string","nullable":true}}}}}}},"blockers":{"type":"integer"},"warnings":{"type":"integer"},"signedOffBy":{"type":"string","format":"uuid","nullable":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Price": {"x-ticvai-persistence":"catalogue.price","type":"object","required":["priceListId","variantId","amount"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"priceListId":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true}}},
"ProposedAction": {"type":"object","x-ticvai-persistence":"ai.proposed_action","required":["id","kind","targetContract","targetOperation","payload","status"],"properties":{"id":{"type":"string","format":"uuid"},"interactionId":{"type":"string","format":"uuid"},"kind":{"type":"string","enum":["pricing","promotion","operational","financial","configuration","content","audience"],"description":"`content` (a marketing or storefront draft from `proposeMarketingContent`) and `audience` (a lookalike segment from `proposeLookalikeSegment`) added 29 September (build); both are applied by a person in the owning screen."},"targetContract":{"type":"string","description":"Which contract would perform it. The assistant never performs it itself."},"targetOperation":{"type":"string"},"payload":{"type":"object","additionalProperties":true,"description":"The request body a person would submit, ready to review. **Open on purpose: its shape is the request body of `targetOperation` in `targetContract`**, and it is validated against that operation, not restated here.\n"},"summary":{"type":"string"},"status":{"type":"string","description":"**Expiry (decided 28 September, audit R213)**: a `proposed` action expires 7 days after `proposedAt`; an `approved` action not applied expires 24 hours after `decidedAt`. Both are proposed values, client to correct, and `expiresAt` carries the one that applies.\n","enum":["proposed","approved","rejected","applied","expired"]},"expiresAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"When the expiry timer moves this action to `expired` — `proposedAt` plus 7 days while `proposed`, `decidedAt` plus 24 hours once `approved`, null once `rejected`, `applied` or `expired` (audit R213)."},"approvalLevel":{"type":"integer","minimum":1,"maximum":2,"description":"8.3.65. Multi-level, because a discount and a pricing change differ in authority. **Two levels (decided 28 September, audit R213)**: `2` for anything touching prices or permissions (every `pricing` and `promotion` action, and any other whose payload sets a price, a discount, a role or a permission grant), which needs a manager other than the requester; `1` for everything else, which the requester approves themselves.\n"},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true},"decisionReason":{"type":"string","nullable":true,"description":"Required on rejection. **The only signal the assistant is proposing badly**, and without it a poor model degrades silently.\n"},"proposedAt":{"type":"string","format":"date-time"},"decidedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","readOnly":true,"description":"**Added 29 September (AI design 3.1):** `ai.proposed_action` had no policy — its only references were nullable. The scope it was proposed at, and the partition key row-level security reads.\n"},"planId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-references":"ai.action_plan","description":"The plan this action presents for a decision (AI design 2.2 D, 3.8)."},"approvalRequestId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The `approvals` request deciding a tier 2 or matrix-caught action (AI design 2.3)."},"changeSetHash":{"type":"string","nullable":true,"readOnly":true,"description":"Hash of the change set approved; execution refuses a plan whose hash differs (AIC-181)."}}},
"SaleBoardKind": {"type":"string","enum":["ticketing","fnb","retail","mixed"]},
"SetPriceRequest": {"type":"object","required":["variantId","amount"],"properties":{"variantId":{"type":"string","format":"uuid"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid"}}},
"VenueSettings": {"type":"object","x-ticvai-persistence":"platform.venue_settings","description":"**Venue-level operational configuration that no other level can answer.**\nRegion owns currency, tax regime and fiscal year (ADR-0011). Venue owns the things that vary between two venues in one region — **opening hours, support hours, and what the local law requires of the gate.**\n**And the configured limits** (decided 28 September, audit R094): every limit the contracts call *configured* is a field here, from `displayCurrencies` and `cartLeaseSeconds` down to the grouped `catalogue`, `inventory`, `seating`, `promotions`, `fnb`, `queue`, `reporting`, `marketing` and `identity` settings. **Each has a tenant-level default**: the tenant sets it once with `setVenueSettingsDefaults`, a venue overrides it within the field's bounds, and a null field here inherits it. Each field's `default` is the proposed tenant default, marked proposed, client to correct (audit R094); `docs/active/configured-limits-proposal.md` is the sheet the client corrects, and where the two differ this contract is what runs.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `setVenueSettings`."},"calendarDayStartHour":{"type":"integer","minimum":0,"maximum":23,"nullable":true,"default":6,"description":"**Where the venue's calendar day starts** (17 September minutes M17-03, added 30 September): the first hour row of every day and week calendar view (`calendarView` in `screens/_components.yaml`), so a venue open 06:00 to 02:00 sees its night on the day it belongs to. Display only: it moves no booking, slot or business date. Null inherits the tenant default (proposed 6, client to correct).\n"},"currencyCode":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"readOnly":true,"description":"**`readOnly` is the freeze.** `setVenueSettings` takes this whole schema as its request body, so without it any settings save could rewrite the currency of a venue that had already traded — which is the one thing ADR-0018's amendment forbids. It is set when the venue is provisioned, defaulted from the region, and changed only by an operation whose precondition is that the venue has not yet traded.\n**The venue's trading currency, defaulted from its region and frozen once the venue has traded** (ADR-0018, amended 20 September). Currency was a region-only fact, grouped with tax rates on the reasoning that *\"a venue cannot choose its VAT\"* -- true of tax and over-applied to currency, because a free-zone unit, a duty-free shop and a cruise terminal genuinely trade in a currency their region does not.\n**This column exists because the freeze needs somewhere to live.** A venue that resolved purely from its region would silently follow a region currency change after it had already traded, and every dated artefact beneath it -- a price list is a `validFrom`/`validTo` range -- would render retrospectively wrong. Null means \"resolve from the region\", which is the answer for every venue that has not overridden.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"nullable":true,"readOnly":true,"description":"**Scale travels with currency** (ADR-0008), and so does the freeze. OMR is three decimal places because Oman says so; overriding the currency without the scale gets rounding wrong. Set together or not at all.\n"},"supportHours":{"type":"object","description":"CF-100. **A venue decides whether its support desk is 24/7 or bounded, and the platform does not.** This was recorded as an open question for eleven days and was never one — the code is identical either way, and what was missing was somewhere to put the answer.\n","properties":{"mode":{"type":"string","enum":["alwaysOn","businessHours","custom","none"]},"timezone":{"type":"string","description":"IANA zone the `windows` are read in. Absent, they are read in the region's `timeZone`, like every other wall-clock time in this contract.\n"},"windows":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time the desk opens."},"to":{"type":"string","description":"Wall-clock time the desk closes."}}}},"outOfHoursMessage":{"type":"string","nullable":true}}},"quietHours":{"type":"object","nullable":true,"description":"**When the platform does not send.** A wallet low-balance alert at 3am is a complaint, and journeys and message triggers both respect this.\n**Operational messages ignore it** — a queue-turn alert is why a guest is holding the phone.\n","properties":{"from":{"type":"string","description":"Wall-clock time sending stops","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time sending resumes","in the region's time zone.":null}}},"biometrics":{"type":"object","nullable":true,"description":"CF-35, BL-096, BL-105, BL-106. **The venue-level master switch, and the one place a person is asked whether the paperwork exists.** Biometric data is sensitive under PDPL (Federal Decree-Law 45/2021) — heightened protection, explicit consent, and an Article 21 assessment before the processing rather than after it.\n**Nothing below this switch operates while it is off.** `AdmissionRules` may carry a `biometricPolicy` per ticket type and those rules are inert until a venue enables biometrics here, which means a profile copied between venues cannot start capturing faces at the destination.\n**Venue level because that is where the assessment is filed.** Region owns tax and currency; the DPIA, the consent notice and the hardware are a venue's.\n","properties":{"isEnabled":{"type":"boolean","default":false,"description":"**Off by default, and turning it on is refused without the two fields below.** `setVenueSettings` answers 422 rather than accepting an enable it cannot evidence — **a DPIA nobody can name is a DPIA nobody did**, and the point of the refusal is that the person switching this on is asked at the moment they switch it on rather than by an auditor a year later.\n"},"dpiaReference":{"type":"string","nullable":true,"maxLength":200,"description":"**The venue's own reference for its Article 21 assessment.** The platform does not hold the document and does not judge it; it records that one was named, by whom, and when — which is what an audit asks for and what the venue can produce.\n"},"consentNoticeAcknowledgedAt":{"type":"string","format":"date-time","nullable":true,"description":"**When somebody confirmed the consent forms are in place at the point of capture.** A guest consenting in an app is a record; a guest consenting at a ticket counter is a notice somebody has to have printed and a question somebody has to have asked.\n"},"acknowledgedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Who confirmed it.** An acknowledgement with no name behind it cannot be followed up, and this is the field that makes the switch an act rather than a setting. Recorded by the server as the caller whose save carried the acknowledgement, so it cannot name somebody else.\n"},"faceTagPurgeMinutesAfterClose":{"type":"integer","nullable":true,"default":0,"description":"BL-106. **How long a same-visit Face Tag survives past the close of the operating day**, and zero is the default because that is what 3.2.44 describes. A non-zero value is an operational allowance for a late reconciliation, not a retention period — **`facePass` ignores this entirely** and is bounded by its entitlement.\n"},"consentFormId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's own consent form, which every biometric capture is taken on** (decided 2 October 2026, Chinmay, batch 4, BO-188: \"Consent first, on the venue's consent form\"; DEC-128, DEC-549; CHG-CSP-018). A form from the venue's consent-form builder in Venue Management (the one builder Face Pass, Face Tag, marketing and waivers share; marketing-crm `setDigitalWaiverForm`). Turning `isEnabled` on without one is refused `422 consent-form-required`, as a missing DPIA is; each Face Pass and Face Tag capture records the form and its version it was consented on (access `enrolFacePass`, `enrolFaceTag`).\n"},"templatesHeldByTicvai":{"type":"boolean","readOnly":true,"description":"**True where TICVAI's platform stores this venue's biometric templates** (rather than the venue's own on-premises reader estate). Derived from the venue's access deployment. While true, Venue Management shows the venue a standing warning that every guest must accept the venue's consent form before capture, because the data sits with TICVAI as the venue's processor (decided 2 October 2026, Chinmay, batch 4, BO-188: \"If we store the data, highlight or notify the venue that the client must accept a consent form\"; DEC-128; CHG-CSP-018).\n"},"allowMinors":{"type":"boolean","default":true,"description":"**Whether this venue enrols minors at all** (decided 2 October 2026, Chinmay, critical set 1, BO-187 and CMS-029: \"Guardian consent on the venue's form; minor age per country; the venue can switch minors off\"; supersedes the GST-069 default; DEC-237; CHG-CSP-019). On: a minor (below `RegionSettings.minorAgeThreshold`) is enrolled only with a guardian's consent on the venue's consent form. Off: a minor's enrolment is refused (`422 minors-not-enrolled`) and the guest uses another verification method.\n"},"accreditationFaceMatching":{"type":"object","nullable":true,"description":"**Face matching to find duplicate accreditation applicants, off unless the venue enables it** (decided 2 October 2026, Chinmay, critical set 3, BO-631: \"Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default\"; DEC-461; CHG-CSP-022). Enabling it is refused without `legalSignOffReference` (`422 legal-sign-off-required`); each applicant matched must have consented on the application (accreditation's own record). Null is off.\n","properties":{"isEnabled":{"type":"boolean","default":false},"legalSignOffReference":{"type":"string","nullable":true,"maxLength":200,"description":"The venue's own reference for its legal sign-off; the platform records that one was named, by whom and when."},"signedOffByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"signedOffAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}}}},"segregatedAccess":{"type":"object","nullable":true,"description":"CF-130. **Configured at venue level because it changes by region and the venue is where it is known** — a Ladies Night, a family session, a prayer-time closure.\n**The platform does not infer gender.** 3.2.45 asks for automatic gender recognition and 3.2.46 for rule-based facial recognition validation, and neither is built. Two reasons, and the second is the one that decided it:\n**A Ladies Night ticket is already gendered at the point of sale**, so the gate checks the entitlement the platform issued rather than the face in front of it — deterministic, auditable, and already contracted through `admissionRules`.\n**And these events are staffed.** A steward at the entrance is making the judgment anyway, and a classifier that overrules a person who can see more than it can is a machine and a human disagreeing while a guest waits.\n**`genderVerification` is a switch, not an implementation.** Where a venue's access hardware offers the capability and the venue chooses to use it, this turns it on — following ADR-0015's standards-first driver model, where the device does what the device does. **Not everything needs to be built.**\n","properties":{"isEnabled":{"type":"boolean","default":false},"appliesToAccessPointIds":{"type":"array","items":{"type":"string","format":"uuid"}},"schedule":{"type":"array","items":{"type":"object","properties":{"day":{"type":"string","enum":["mon","tue","wed","thu","fri","sat","sun"]},"from":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"to":{"type":"string","description":"Wall-clock time","in the region's time zone.":null},"admits":{"type":"string","enum":["all","women","womenAndChildren","families","members"]}}}},"entitlementGated":{"type":"boolean","default":true,"readOnly":true,"description":"**Always true, and stated rather than assumed.** The gate admits on the entitlement. Everything below is advisory on top of that, and nothing replaces it.\n"},"genderVerification":{"type":"string","enum":["off","staffAssisted","deviceAssisted"],"default":"off","description":"`off` — the entitlement decides and a steward handles exceptions. **The default, and what is contracted.**\n`staffAssisted` — the steward's screen shows the ticket type so they can ask. No inference anywhere.\n`deviceAssisted` — **the venue's access hardware performs the check, not the platform.** Available only where the driver reports the capability, and the result is **advisory to the steward rather than decisive at the turnstile** (3.2.45 asks for rejection; this deviates deliberately).\n"},"overrideRateAlertThreshold":{"type":"number","nullable":true,"description":"Where `deviceAssisted` is on. **An override rate near zero means the steward has stopped deciding**, and that is the number that says whether the human safeguard is working or decorative.\n"}}},"alerting":{"type":"object","description":"CF-134. **On-platform notification, marked as read.** Six contracts detect their own trouble and none told a person.\n**The panel is the default and email or WhatsApp only where the matrix names them** — an operational alert that arrives by email is an alert nobody sees in time.\n","properties":{"channel":{"type":"string","enum":["dashboardPanel","dashboardAndEmail","dashboardAndWhatsapp"],"default":"dashboardPanel"},"acknowledgementRequired":{"type":"boolean","default":true},"escalateAfterMinutes":{"type":"integer","nullable":true}}},"displayCurrencies":{"type":"array","nullable":true,"description":"**Which currencies this venue shows guests** (decided 28 September, audit R120 (a)). ISO 4217 codes, each one its region holds an `FxRate` for; the rate itself stays per region and is never set here. `finance.listFxRates` with `venueId` narrows the region's rates to these. Null or empty shows the trading currency only. A code the region has no rate for is refused `400`.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"chargeCurrencies":{"type":"array","nullable":true,"description":"**Which currencies a guest may select and pay in** (decided 2 October 2026, Chinmay; CHG-FIN-001; MoM 10 Aug 2026 4.7 option (b), DI-211). A subset of `displayCurrencies`: each code must also be one the venue's payment provider can charge (`orders.PaymentProvider.presentmentCurrencies`) and one the region holds a `tender` rate for; anything else is refused `400`. Null or empty: guests pay in the trading (base) currency only and the other display currencies stay approximate. The ledger is always in the base currency, with the rate recorded on every payment and refund.\n","items":{"type":"string","pattern":"^[A-Z]{3}$"}},"cartLeaseSeconds":{"type":"integer","nullable":true,"minimum":30,"maximum":3600,"default":900,"description":"**How long a cart holds capacity** (decided 28 September, audit R169): 15 minutes, the default `catalogue.acquireInventoryHold` takes for `ttlSeconds`. Proposed, client to correct (audit R094).\n"},"cartHoldExtensionMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":5,"description":"How long one `orders.extendCart` extension adds. Proposed, client to correct (audit R094)."},"cartMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many extensions a cart may take before `extensionCapReached` (`Cart.maxExtensions`). Proposed, client to correct (audit R094)."},"resaleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":168,"default":24,"description":"Hours before the performance after which a ticket can no longer be listed for resale (`orders.createResaleListing`). Proposed, client to correct (audit R094)."},"exchangeCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which lines can no longer be exchanged (`orders.exchangeOrderLines`, `outsideExchangeWindow`). Proposed, client to correct (audit R094)."},"rescheduleCutoffHours":{"type":"integer","nullable":true,"minimum":0,"maximum":720,"default":24,"description":"Hours before the original performance after which an order can no longer be rescheduled (`orders.rescheduleOrder`, `outsideRescheduleWindow`). Proposed, client to correct (audit R094)."},"reservationMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":1,"description":"How many times `orders.extendReservation` may extend one reservation. Proposed, client to correct (audit R094)."},"shiftVarianceThreshold":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Over or short at shift close beyond which the shift waits in `pendingVariance` for `shift.acceptShiftVariance`. **Proposed tenant default AED 20.00, bounds 0 to 1,000 in the venue currency; client finance to correct (audit R094).**\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The most cash a till drawer should hold before some is lifted to the safe** (decided 2 October 2026, Chinmay, batch 6 set 3, BO-042: \"Add drawer limit setting (warn + offer cash lift)\"; DEC-179; CHG-CSP-016; DI-274: on a busy day the cashier unloads excess cash mid-shift and it is reconciled at close). The venue default; a till may set its own (`Workstation.cashDrawerLimit`). When the cash a till has taken since its last count takes the drawer over it, the till warns and offers a cash lift (`shift.createCashMovement` kind `lift`) and BO-042 flags the box (`shift.DepositBox.overDrawerLimit`). A warning, never a block: a sale is not refused because the drawer is full. Null sets no limit. **No proposed default: the client's finance team sets it.**\n"},"catalogue":{"type":"object","nullable":true,"properties":{"maxVariantsPerProduct":{"type":"integer","nullable":true,"minimum":1,"maximum":2000,"default":200,"description":"Variants one product may generate from its attributes (`setProductAttributes` refuses above it). Proposed, client to correct (audit R094)."},"waitlistOfferHoldMinutes":{"type":"integer","nullable":true,"minimum":1,"maximum":1440,"default":30,"description":"How long a waitlist offer holds the released capacity for the guest it was offered to. Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":10,"description":"A `bulkChangePrices` run changing any price by more than this percentage needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."},"bulkPriceChangeEscalationCount":{"type":"integer","nullable":true,"minimum":1,"default":50,"description":"A `bulkChangePrices` run touching more prices than this needs `PRICE_CONFIGURE` (audit R197). Proposed, client to correct (audit R094)."}}},"inventory":{"type":"object","nullable":true,"properties":{"overReceiptTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":5,"description":"Percent above the outstanding ordered quantity a goods receipt line may record (`createGoodsReceipt`). Proposed, client to correct (audit R094)."},"countVarianceTolerancePercent":{"type":"number","nullable":true,"minimum":0,"maximum":25,"default":2,"description":"Percent difference between counted and expected quantity before a count line is an exception (`getCountVariance`). Proposed, client to correct (audit R094)."},"countVarianceApprovalAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Total variance value of a count above which posting it needs approval (`postStockCount`). **Proposed tenant default 1,000.00 in the venue currency, client finance to correct (audit R094).**\n"}}},"seating":{"type":"object","nullable":true,"properties":{"seatHoldExtensionSeconds":{"type":"integer","nullable":true,"minimum":60,"maximum":1800,"default":300,"description":"What one `extendSeatHold` adds. No hold outlives 30 minutes in all (audit R169). Proposed, client to correct (audit R094)."},"seatHoldMaxExtensions":{"type":"integer","nullable":true,"minimum":0,"maximum":5,"default":2,"description":"How many times a seat hold may be extended. Proposed, client to correct (audit R094). A resource hold on a venue map (`resources.extendResourceHold`) uses the same two bounds (decided 29 September, rev 3 REV3-15)."},"maxSeatsPerGuestOrder":{"type":"integer","nullable":true,"minimum":1,"maximum":50,"default":10,"description":"**Seats one guest may take in one booking on a guest channel** (Guest Web, Guest App), decided 29 September, rev 3 REV3-7. `seating.createSeatHold` counts the seats in the request plus the seats the same guest already holds on the same performance, and refuses above this with `422` `seat-limit-exceeded`, naming the limit. Default 10, bounds 1 to 50; a venue sets its own in Venue Management. Staff and POS sales keep 10 per sale (audit R080 (c)) and do not read this field.\n"}}},"promotions":{"type":"object","nullable":true,"properties":{"maxDiscountPercent":{"type":"number","nullable":true,"minimum":0,"maximum":100,"default":30,"description":"The largest discount one promotion may give (`createPromotion` refuses above it). Proposed, client to correct (audit R094)."},"nearZeroLinePrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Net line price below which a stacked combination is flagged near-zero in `analysePromotionConflicts` (audit R096 (5)); a warning, not a refusal. **Proposed tenant default AED 1.00, client to correct (audit R094).**\n"}}},"fnb":{"type":"object","nullable":true,"properties":{"recallWindowMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":60,"default":10,"description":"Minutes after a bump during which `recallKitchenTicket` still recalls; after it the act is a refire. Proposed, client to correct (audit R094)."},"tableReservedLeadMinutes":{"type":"integer","nullable":true,"minimum":0,"maximum":240,"default":30,"deprecated":true,"description":"**Deprecated (2 October 2026, CHG-CLN-009): `fnb.FnbReservationPolicy.reservedLeadMinutes` is canonical.** The table state model reads the reservation policy (`states/table.yaml`); this venue setting is kept for compatibility, never read, and not drawn. Its former meaning: **How long before a pre-allocated booking its table shows Reserved** (decided 2 October 2026, Chinmay, batch 6 set 6b, EMP-052: \"Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking\"; DEC-202; CHG-CSP-017; DI-689, DI-336). A booking that names its table holds it as Reserved for the booking's whole slot; a booking the host pre-allocated shows its table Reserved from this many minutes before it. Zero shows Reserved only once the booking is due. The fnb table state model applies it (`states/table.yaml`, owned by fnb). Proposed default 30 minutes, client to correct.\n"},"compEscalationAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"Line value above which `compItem` needs `ORDER_DISCOUNT` (audit R197). **Proposed tenant default AED 100.00, client to correct (audit R094).**\n"},"foodSafetyLeadPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"**The venue's food-safety lead**, to whom `escalateCorrectiveAction` sends every escalation (decided 28 September, audit R096 (9)). A venue fact, so it has no tenant default; while it is null an escalation is refused `409 no-food-safety-lead`.\n"}}},"queue":{"type":"object","nullable":true,"properties":{"crossQueueLimit":{"type":"integer","nullable":true,"minimum":1,"maximum":10,"default":2,"description":"Virtual queues one guest party may wait in at once (`joinQueue`, `crossQueueLimitReached`). Proposed, client to correct (audit R094)."}}},"reporting":{"type":"object","nullable":true,"properties":{"inlineRunRowLimit":{"type":"integer","nullable":true,"minimum":1000,"maximum":100000,"default":5000,"description":"Estimated rows above which `runReport` answers `202` and runs in the background. Proposed, client to correct (audit R094)."},"dashboardRefreshBudgetPerMinute":{"type":"integer","nullable":true,"minimum":1,"default":24,"description":"Tile refreshes per minute, summed over a dashboard's tiles, that `createDashboard` allows. Proposed, client to correct (audit R094)."}}},"marketing":{"type":"object","nullable":true,"properties":{"attributionWindowDays":{"type":"integer","nullable":true,"minimum":1,"maximum":30,"default":7,"description":"Days after a campaign touch within which a booking is attributed to it (`getCampaignPerformance`). Proposed, client to correct (audit R094)."}}},"identity":{"type":"object","nullable":true,"properties":{"guestOtpMaxAttempts":{"type":"integer","nullable":true,"minimum":3,"maximum":10,"default":5,"description":"Wrong entries allowed per guest one-time code before `verifyGuestOtp` invalidates it. A guest code is tenant-scoped, so the tenant default is the value used. Proposed, client to correct (audit R094).\n"},"guestTwoStep":{"type":"object","nullable":true,"description":"**Guest two-step verification: a venue option, off unless the venue enables it in Venue Management** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of audit R167, \"no guest MFA\"; an earlier draft of the same day put it on the tenant's `PasswordPolicy`, which no longer carries it). **The guest's enrolment stays tenant-wide**: one guest account across the tenant's venues, so a method enrolled once is used in every venue that has this on, and is never asked in a venue that has it off. Identity learns the venue from `venueId` on the guest sign-in (`verifyGuestOtp`, `guestPasswordLogin`, `guestSocialLogin`, `guestUaePassLogin`) and on `createMfaChallenge`: the venue the guest app or booking is in; with no venue given, an enrolled guest is asked when any venue of the tenant has it on. Guests may enrol `totp` with `emailOtp` as the fallback, as staff do (audit R126 (5)); it is never forced. Guests still never use enterprise SSO (R167, first part). A null inherits the tenant default set with `setVenueSettingsDefaults`.\n","properties":{"enabled":{"type":"boolean","default":false,"description":"Off unless the venue enables it. While no venue of the tenant has it on, guests cannot enrol (`enrolMfaMethod` answers 403 `guest-two-step-disabled`)."},"stepUpActions":{"type":"array","uniqueItems":true,"description":"The guest actions in this venue that ask an enrolled guest for the factor again, whatever the age of the session. The service performing the action passes this venue to `createMfaChallenge`. Proposed, client to correct (rev 3 GAP-B1).\n","items":{"type":"string","enum":["changeContactDetails","changePassword","managePaymentMethods","transferTickets","deleteAccount"]},"default":["changeContactDetails","changePassword","managePaymentMethods","deleteAccount"]}}}}}}},
"Workstation": {"x-ticvai-persistence":"platform.workstation","type":"object","required":["id","code","name","venueId","regionId","scopePath","saleBoard","currency","currencyScale","timeZone"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"departmentId":{"type":"string","format":"uuid","nullable":true},"outletId":{"type":"string","format":"uuid","nullable":true,"description":"**The outlet this till stands in** (CHG-CSP-006). Its board is the till's board unless the till overrides it. Null on a workstation that belongs to no outlet (a ticket office counter set up before outlets), which must then carry its own board.\n"},"scopePath":{"type":"string"},"saleBoard":{"type":"object","description":"Determines which front end loads. Bound to the workstation, not the role — the F&B terminal opens the F&B board. What the operator may then DO within it is governed by their permissions.\n**The effective board** since 2 October 2026 (DEC-183; CHG-CSP-006): the till's own when it overrides the outlet, otherwise the outlet's (`saleBoardSource`).\n","required":["id","kind"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/SaleBoardKind"},"name":{"type":"string"}}},"saleBoardSource":{"type":"string","enum":["outlet","workstation"],"readOnly":true,"description":"**Where `saleBoard` came from** (decided 2 October 2026, Chinmay, BO-109: \"Per outlet, with a till override\"; DEC-183; CHG-CSP-006): `outlet` when the till uses its outlet's layout, `workstation` when this till overrides it. BO-109 shows which tills differ from their outlet.\n"},"cashDrawerLimit":{"oneOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**This till's drawer limit, overriding the venue's** (`VenueSettings.cashDrawerLimit`; DEC-179; CHG-CSP-016). Null inherits the venue's. Above it the till warns and offers a cash lift.\n"},"accessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Inherited from the workstation, never selected by the operator. Null where the workstation is not at an access point.\n"},"devices":{"type":"array","items":{"$ref":"#/components/schemas/DeviceBinding"}},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"timeZone":{"type":"string"},"deploymentProfile":{"$ref":"#/components/schemas/DeploymentProfile"},"edgeNodeId":{"type":"string","format":"uuid","nullable":true,"description":"Present when `deploymentProfile` is `venueEdge`."},"healthScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"readOnly":true,"description":"Board 1 of the client's POS set. **A number a manager can sort by** — the package held `lastHeartbeatAt` and a heartbeat timestamp is not a score.\nThe client's board shows 1,248 workstations at 96% healthy, and **the value of that figure is that it ranks**: a fleet dashboard exists so somebody can open the worst one first.\n**Derived from its devices, its heartbeat age, its firmware currency and its error rate.** Read-only, because a workstation that could set its own score would.\n**The formula, proposed, client to correct (audit R096 (2)):** score = 40% device online share (the share of its devices reporting online) + 25% heartbeat freshness (100 at one minute old or less, 0 at 15 minutes or more, linear between) + 20% firmware and profile currency (100 on the latest, 50 one version behind, 0 older) + 15% error rate (100 at 0 errors an hour, 0 at 10 or more, linear between), rounded to a whole number. **Below 80 is a warning and below 60 a failure.**\n"},"configurationProfileId":{"type":"string","format":"uuid","nullable":true,"description":"Which profile this workstation runs, and at which version. **The client's board shows a fleet split four ways — 72% latest, 18.8% one behind, 6.1% outdated** — and the package had a firmware version field and no profile.\n**A profile is what a venue changes; a version is what it deploys.** Conflating them means a venue cannot say *roll the ticketing counters back and leave the kiosks*.\n"},"catalogueState":{"$ref":"#/components/schemas/CatalogueState"},"offlineCapable":{"type":"boolean","description":"Derived from `deploymentProfile`. False only for `thin`. Under local-first, catalogue READS are always local on transactional surfaces; this flag governs whether WRITES can be queued.\n"},"isActive":{"type":"boolean"}}}
}
```
