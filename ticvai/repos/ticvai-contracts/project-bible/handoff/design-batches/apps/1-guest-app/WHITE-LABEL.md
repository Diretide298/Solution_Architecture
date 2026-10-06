# White label: what a tenant configures, and where a guest sees it

> **Generated** by `tools/build-white-label-map.py` from the contracts (`contracts/satellite/white-label.yaml` and the CMS operations in `marketing-crm.yaml`) and the screens. Edit those, never this file. The same map, per screen, is in every guest and CMS batch's `BUNDLE.md`.

**How to use it in a Claude Design session.** Draw each guest screen (web P01, app P02, kiosk P05) with the **default theme**, and show **one alternate tenant theme** on the key screens, so a reviewer can see the brand is configuration, not paint. Nothing on a guest screen may hard-code a brand colour, logo, font, card layout or step-indicator style: each comes from a field below. On a CMS screen, every field shows its allowed values and default, and the preview shows the output on the guest screen it reaches.

**329 configurable elements in 26 parts**, set on 22 CMS and console screens, reaching 144 guest screens.

## How an input becomes an output

1. **The tenant edits the working draft** on a CMS screen (`CMS-002` to `CMS-019`, `CMS-101` to `CMS-104`). Every `set*` call writes the draft only; nothing reaches a guest yet.
2. **Previews it** (`CMS-006` Component Preview, `CMS-012` RTL Preview): the draft rendered on the guest screens, in both directions. *Arabic is a mirror, not a translation.*
3. **Validates and publishes** (`CMS-014` Publishing Workflow): `validateTenantConfig` names every missing or failing part; `publishTenantConfig` makes it live. **The website takes it at once; the app on its next launch.**
4. **The guest surface reads it** once per visit through `getTenantConfig` (on `WEB-001`, `GST-001`, `KSK-002`), and the booking steps read their flow through `getPublishedBookingFlow`. Booking settings are resolved for the venue the guest picked: the tenant's values with that venue's override laid over them, field by field.
5. **Some changes need an app build** (`CMS-104`): app icons, and on the native apps the splash and custom font files. The website takes those on publish too.
6. **Rolls back** (`CMS-015` Version History): restore copies an earlier version into the draft; it is reviewed and published like any other change, never in one click.

**Flow F22, A tenant rebrands their app** (`flows/F22-a-tenant-rebrands-their-app.yaml`)

1. `CMS-002` Brand Kit: Uploads the new logo and icons → **Assets, not code.** A logo change must not be a release
2. `CMS-005` Theme Editor: Sets the colour theme → **Contrast checked and enforced**: a colour pair that fails 4.5:1 is refused by `setTheme` (`400 ContrastProblem`), because a brand colour that fails it is inaccessible (decided 28 September, audit R139 (a))
3. `CMS-007` Page Builder: Rearranges the homepage → Sections reordered, drag and drop
4. `CMS-012` RTL Preview: Previews in both directions → **Arabic is a mirror, not a translation** — the preview must show it
5. `CMS-014` Publishing Workflow: Publishes → Live on web immediately; the app picks it up on next launch
6. `CMS-015` Version History: Rolls back when something is wrong → **Restore, then review, then publish — not one click** (decided 28 September, audit R139 (b)). `restoreConfigVersion` copies the earlier version into the draft without publishing it, and `diffConfigVersion` shows what …
7. `CMS-014` Publishing Workflow: Publishes the restored draft → The previous brand is live again, through the same publish gate as any other change

**Flow F102, A brand is set, previewed, published and rolled back** (`flows/F102-a-brand-is-set-previewed-published-and-rolled-ba.yaml`)

1. `CMS-001` Tenant Workspace: Tenant Workspace. See what is live before changing the brand. → The current published state is known, so a change can be compared against it. Rewired 23 September (L7) from subscription and billing operations, which the screen no longer declares.
2. `CMS-003` Typography: Typography. → 2 operations, 2 of them previously unwalked.
3. `CMS-006` Component Preview: Component Preview. → 2 operations, 2 of them previously unwalked.
4. `CMS-014` Publishing Workflow: White-Label Branding Management. → 5 operations, 5 of them previously unwalked.

**Flow F103, A tenant claims a domain and gets a certificate** (`flows/F103-a-tenant-claims-a-domain-and-gets-a-certificate.yaml`)

1. `CMS-017` Domain & Certificate: The tenant claims the hostname for an app (guest web, guest app links, partner or developer portal). → **Claiming is not owning.** The claim answers with every record to publish (`dnsRecords`): the TXT `_dnsauth` validation record and the CNAME to the Front Door endpoint (decided 2 October 2026, Chinmay, batch 5 …
2. `CMS-017` Domain & Certificate: The tenant publishes the records at their DNS provider and the domain is verified. → **Retried by a job, not by the tenant.** The records list shows each record with the value observed now and its status; verification routes the hostname (tenancy `setTenantDomainMapping`) and Front Door issues a managed …
3. `CMS-017` Domain & Certificate: The domain is live; the tenant checks its readiness and makes it the primary domain. → **A live domain is not a ready one.** Per-domain readiness shows the UAE Pass redirect, the Apple Pay merchant domain and the app links (`CustomDomain.readiness`). The primary domain for each kind takes the traffic and …
4. `CMS-017` Domain & Certificate: Later, the tenant gives a domain up. → **The takeover warning is in the confirmation** (DEC-547): remove the CNAME and the TXT record from your DNS, because a record left pointing at TICVAI could be claimed by somebody else. Releasing unroutes the hostname …

## The white-label model, from the process owner

*From `handoff/design-notes/white-label.yaml` (white-label process agent (Claude), 1 October 2026). Authored; where it and the generated tables below disagree, it is the one to check first.*

A tenant (one operator, one or many venues) brands and arranges its own guest surfaces, the guest web (P01), the guest app (P02) and the kiosk (P05), from the Venue CMS (P13, a section of the Venue Management app), and TICVAI platform staff can do the same from the console (P09 ADM-016..018) only under a time-boxed grant into the tenant. Everything is configuration over a fixed structure: the guest flow, the page structure and the components are TICVAI's and stay the same for every tenant; the tenant chooses graphics, colours, fonts, which modules and tabs appear, the order of homepage sections and booking steps within allowed limits, copy in each language, and its domain. It never adds components. Work happens in ONE working draft per tenant; nothing a guest sees changes until a person with TENANT_PUBLISH publishes the draft as an immutable version (with a note), and a rollback is restore into the draft, review the diff, then publish, never one click. Three things are deliberately outside the draft and take effect at once: the live app status (maintenance, minimum app version, contact, sold out or closed), a venue's Help me choose publish, and policies (each save is a new version). Build-time parts (app icons, native splash, custom font files, wallet and payment integrations) reach guests only with a new store build, which the client publishes under its own Apple and Google accounts (CMS-104). Staff surfaces (POS, scanner, staff app, kitchen display) never take tenant branding; every guest surface carries the "Powered by TICVAI" credit, a toggle that is on by default (decided 2 October 2026, CHG-NOTE-009; DI-297 amended). Arabic is a first-class layout: enabling `ar` requires an Arabic font, the whole layout mirrors (numbers, times, codes and logos do not), and every authored text is a per-language value. The step-based Site Builder (CMS-102) walks a new tenant through seven steps from a venue-type preset so that a logo, four colours and a publish are enough for a working site in about 30 minutes; every step opens the full screen for its details. Vocabulary below; the element-by-element model follows; inputToOutput at the end gives worked examples.

*(source: contracts/satellite/white-label.yaml#/info; DI-223; DI-285; DI-111; DI-297; DI-296; DI-298; DI-997; DI-998; DI-1014; R139; R073; F22 step 5; F22 step 6; docs/architecture/rtl-and-theming.md)*

**Input → output, worked by the process owner**

- **CMS-005 Primary colour #0E7C86 (white text on it 4.9:1, passes AA)** → Primary buttons (Continue, Add to basket unless addToCart is set), the active step of the step indicator, links, selected date and time chips, the selected seat, the active tab icon and the Buy tickets button (unless buyTicketsButton is set) all turn #0E7C86 after the publish. *(source: contracts/satellite/white-label.yaml#/components/schemas/Theme; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **CMS-005 componentColours.payButton = {background #0B4F6C, text #FFFFFF}** → Only the Pay button changes; every other button stays primary. *(source: DI-922)*
- **CMS-005 accent #FFC845 used as badge background with white text** → Refused on save (400 ContrastProblem, 1.5:1 against 4.5:1); nothing changes for guests; the editor marks the pair. *(source: R139)*
- **CMS-005 cornerRadius 0, buttonStyle pill, surfaceStyle solid** → Square cards, inputs, chips and cart; fully rounded buttons regardless of radius; opaque cards without blur. *(source: DI-1066; DI-1067)*
- **CMS-004 logoVariant duotone** → The nav bar shows the two-colour reading of the logo and the page tint follows its colours; the stored theme colours stay as saved. *(source: DI-1068)*
- **CMS-004 new app icon, then publish** → Web favicons and touch icon change on next load; the installed app icon changes only after the next store build from CMS-104 is released; the publish result lists it under Needs an app update. *(source: contracts/satellite/white-label.yaml#setAppIcons)*
- **CMS-004 introVideoMode firstLaunch with a 9 s clip** → The first app open on a device plays the clip full screen and muted with Skip introduction; later opens go straight to Home. *(source: DI-1020)*
- **CMS-003 primary Manrope / Tajawal with ar enabled** → English text in Manrope, Arabic text in Tajawal on every guest screen; prices and times inside Arabic lines stay left-to-right. *(source: contracts/satellite/white-label.yaml#setFonts; docs/architecture/rtl-and-theming.md)*
- **CMS-011 languages [en, ar, ru], default en** → The header language button offers English, العربية, Русский; a first-time guest sees English; Arabic mirrors the layout; Russian text missing in pages falls back and the publish warns (missingTranslation). *(source: contracts/satellite/white-label.yaml#setLanguages; DI-975)*
- **CMS-016 cartSideInRtl keepRight with Arabic chosen** → The layout mirrors but the cart sidebar or floating basket stays on the right. *(source: DI-1051)*
- **CMS-016 stepIndicator numbered** → The booking steps show numbered, named steps under the powered-by strip; completed steps can be tapped to go back. *(source: DI-1093; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **CMS-016 cardLayout cardsAcross (tenant) with a posterCards override for Kids Club Mirdif** → Most venues show product cards in an equal-height grid; at Kids Club Mirdif the cards lead with full-width imagery and the price on the image. *(source: DI-1040; DI-1063)*
- **CMS-016 cartLayout floatingIcon** → A round basket button with the item count opens the slide-in basket instead of a sidebar. *(source: DI-1051)*
- **CMS-016 heroBanner off, embedMode embedded** → No hero, venue header or footer; the booking engine renders inside the tenant's own site with the powered-by strip and progress. *(source: DI-945; sources/designs/guest-rev3-30-september/TICVAI Engine Controls Manual.dc.html)*
- **CMS-016 timesPerPage 12 and dayPartFilter on** → More than 12 times on a day show as compact tiles 12 at a time with Earlier and Later, and Morning, Afternoon and Evening chips with counts. *(source: DI-1041)*
- **CMS-016 guestContactFields [email, mobile, name] with the guestCheckout feature on** → The guest-checkout pop-up asks email, mobile and name; after the code is verified the guest goes straight to terms and payment. *(source: MoM 29 Sep 1 W1)*
- **CMS-103 Kids Club Mirdif flow with extras turned off** → Ticket selection goes straight to the cart and checkout; the step indicator shows one step fewer. *(source: DI-428; contracts/satellite/white-label.yaml#/components/schemas/BookingFlowLevelSettings)*
- **CMS-103 signInAt atPayment** → Sign-in (or the guest code) is asked on the payment step instead of when leaving add-ons; the basket is kept either way. *(source: DI-1043)*
- **CMS-101 published set-up, mode popupOnArrival, behaviour filter** → On a guest's first arrival at the booking page a Help me choose pop-up asks the questions; answers narrow the product list, with Show everything to clear them; the dark banner offers it again under the products. *(source: DI-1052; MoM 29 Sep 1 W4)*
- **CMS-009 tabs Home, Explore, Map, Tickets with buyButton raised** → The app tab bar shows those four with a raised Buy tickets button in the centre on every screen except booking and checkout; Plan is gone. *(source: DI-1081; DI-1087)*
- **CMS-001 module diningAndFnb switched off, then publish** → The dining homepage section, the Food view in At the Venue and any Dining navigation item disappear; refused first if navigation or a section still points at it. *(source: contracts/satellite/white-label.yaml#setModuleEnablement)*
- **CMS-007 sections [heroBanner video, venueOverview, tickets, attractions maxItems 2, dining maxItems 1]** → App Home plays the hero video, then the venue overview with today's hours, the ticket entry, two attraction highlights and one dining highlight, in that order. *(source: DI-1018; contracts/satellite/white-label.yaml#/components/schemas/HomepageLayout)*
- **CMS-007 footer legal links and columns** → The web footer shows the columns, then terms, privacy, accessibility and cookie links, then Powered by TICVAI. *(source: contracts/satellite/white-label.yaml#setFooter; DI-111)*
- **CMS-008 banner placement homepageHero, 10 October 16:00 to 30 November 23:59 GST** → Appears in the Home hero rotation at 16:00 on 10 October and disappears after 30 November without a publish. *(source: contracts/satellite/white-label.yaml#/components/schemas/Banner)*
- **CMS-001 Live now availability soldOut with a message** → A Sold out today banner on Home and the sold-out state with another-day picker, at once, no publish. *(source: R073)*
- **CMS-001 Live now maintenance on, expected back 22:00** → Every guest route shows the branded maintenance page with "Back at 22:00" until it is cleared. *(source: contracts/satellite/white-label.yaml#setMaintenanceMode)*
- **CMS-001 minimumAppVersion iOS 2.3.0** → iPhones running 2.2.x show only the Update screen with a store button; Android is unaffected. *(source: R073; contracts/satellite/white-label.yaml#/components/schemas/MinimumAppVersion)*
- **CMS-017 tickets.coastalaqua.ae verified and active** → The guest web answers at tickets.coastalaqua.ae with a valid certificate; the TICVAI subdomain keeps working. *(source: contracts/satellite/white-label.yaml#verifyCustomDomain; DI-283)*
- **CMS-015 restore version 12, then CMS-014 publish** → Guests see nothing change at the restore; after the publish they see version 12's look as a new version 15; maintenance and availability are untouched. *(source: R139; F22 step 6; F22 step 7)*
- **Any tenant setting on a staff surface** → Nothing. POS, scanner, staff app and kitchen display keep TICVAI branding. *(source: DI-296)*

## Input → output, by example

Each line: the CMS field (input), the value an alternate tenant would set, and what changes on the guest screens (output).

- **Primary colour**: in `CMS-005` Theme Editor, the tenant sets *Primary colour* to **#0077B6** (default —) → on every guest screen (web, app and kiosk): the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings.
- **Button style**: in `CMS-005` Theme Editor, the tenant sets *Button style* to **Pill** (default Solid) → on every guest screen (web, app and kiosk): every button's shape: solid fill, outline, or pill.
- **Surface style**: in `CMS-005` Theme Editor, the tenant sets *Surface style* to **Solid** (default Glass) → on every guest screen (web, app and kiosk): cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token).
- **Corner radius**: in `CMS-005` Theme Editor, the tenant sets *Corner radius* to **18** (default —) → on every guest screen (web, app and kiosk): the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest).
- **Logo variant**: in `CMS-002` Brand Kit, the tenant sets *Logo variant* to **Duotone** (default Light) → on every guest screen (web, app and kiosk): which logo lockup sits in the nav bar, and whose colours drive the theme.
- **Header layout**: in `CMS-009` Navigation & Menus, the tenant sets *Header layout* to **Logo centre** (default —) → on every guest screen (web, app and kiosk): the header: logo left, logo centred, or logo with the menu.
- **Buy button: style**: in `CMS-009` Navigation & Menus, the tenant sets *Buy button: style* to **Floating** (default Raised) → on every P02 screen: the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden.
- **Languages**: in `CMS-011` Translations, the tenant sets *Languages* to **en, ar** (default —) → on every guest screen (web, app and kiosk): the language button in the header; Arabic flips every screen right to left.
- **Step indicator**: in `CMS-016` Site Settings, the tenant sets *Step indicator* to **Dots** (default Bar) → on GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13): the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none.
- **Card layout**: in `CMS-016` Site Settings, the tenant sets *Card layout* to **Cards across** (default Stacked rows) → on GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14): ticket and product cards: stacked rows, split rows, cards across, or poster cards.
- **Card size**: in `CMS-016` Site Settings, the tenant sets *Card size* to **Standard** (default Compact) → on GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12): card size: compact, standard, large, extra large.
- **Cart layout**: in `CMS-016` Site Settings, the tenant sets *Cart layout* to **Floating icon** (default Sidebar right) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon.
- **Cart side in RTL**: in `CMS-016` Site Settings, the tenant sets *Cart side in RTL* to **Mirror** (default Keep right) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): the cart's side in Arabic: kept right, or mirrored left.
- **Times per page**: in `CMS-016` Site Settings, the tenant sets *Times per page* to **8** (default 24) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` ….
- **Seat picker**: in `CMS-016` Site Settings, the tenant sets *Seat picker* to **Zones then seats** (default Bowl) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event..
- **Steps: enabled**: in `CMS-102` Site Builder, the tenant sets *Steps: enabled* to **On** (default —) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): A `required` step cannot be off; the flow saves and `isValid` turns false..
- **Settings: sign in at**: in `CMS-102` Site Builder, the tenant sets *Settings: sign in at* to **At payment** (default After add ons) → on GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11): Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3)..
- **Sections: kind**: in `CMS-007` Page Builder, the tenant sets *Sections: kind* to **Quick actions** (default —) → on the guest home screens: Which module each section needs, proposed, client to correct (decided 28 September, audit R163)..
- **Sections: card count**: in `CMS-007` Page Builder, the tenant sets *Sections: card count* to **6** (default —) → on GST-001, WEB-001: how many cards the section shows, the counts the approved wireframe offers.
- **Sections: scroll animation**: in `CMS-007` Page Builder, the tenant sets *Sections: scroll animation* to **Slide** (default Rise) → on the guest home screens: how the section enters as the guest scrolls: rise, scale, slide, blur or none (none whenever the device asks for reduced motion).
- **Landing-page template**: in `CMS-007` Page Builder, the tenant sets *Landing-page template* to **a TICVAI template, picked by its name and thumbnail** (default —) → on WEB-001: the landing-page template the home started from (listLandingPageTemplates); a tenant with no landing page of its own starts from one, and the sections it fills stay editable.
- **Powered by TICVAI credit**: in `CMS-104` App Build & Store Publishing, the tenant sets *Powered by TICVAI credit* to **off, where the licence allows it** (default on) → on every guest screen (web, app and kiosk): the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 powered-by-locked).

## The default theme and the alternate tenant theme

**Default theme.** The palette, type and shapes of the reference design (`sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, and Mobile App v4 for the app), with every setting at its default in the tables below (Glass surfaces, Solid buttons, Bar step indicator, Stacked rows, Compact cards, cart sidebar right).

**Alternate tenant theme: Coastal Aqua.** Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.

**Show it on:** `WEB-001` Home / Landing, `WEB-005` Ticket Type Selection, `WEB-006` Date & Performance Selection, `WEB-010` Shopping Cart, `WEB-012` Checkout — Payment, `GST-001` Home, `GST-007` Select Date & Time, `GST-041` Checkout Entry, `KSK-002` Language Select, `KSK-003` What are you buying.

## Every configurable element

Columns: the element (its id in the map), where it is set, the control, allowed values and rules, the default, the guest screens it reaches, and what it changes there.

### Brand: logo, splash, intro video

Set on `CMS-002` Brand Kit, `CMS-004` Logo & Assets, `CMS-104` App Build & Store Publishing, `ADM-016` White-Label Branding Management through `setBrandIdentity`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Logo `brand.logoAssetRef` | upload, or pick from the media library | yes | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo in the header or nav bar, the splash and the footer | on publish (CMS-014): web at once, the app on its next launch |
| Logo dark image `brand.logoDarkAssetRef` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every guest screen (web, app and kiosk) | the logo on dark backgrounds (falls back to the primary logo) | on publish (CMS-014): web at once, the app on its next launch |
| Logo variant `brand.logoVariant` | segmented control | no | Light · Dark · Duotone | Light | every guest screen (web, app and kiosk) | which logo lockup sits in the nav bar, and whose colours drive the theme | on publish (CMS-014): web at once, the app on its next launch |
| Favicon `brand.faviconAssetRef` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | every P01 screen | the browser tab icon (website only) | on publish (CMS-014): web at once, the app on its next launch |
| Splash image `brand.splashImageAssetRefs` | media picker (several) | no | PNG, JPG, SVG or MP4 from the media library | — | every P02 screen | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Splash duration seconds `brand.splashDurationSeconds` | stepper or slider (seconds) | no | min 0; max 10 | 3 | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Splash background colour `brand.splashBackgroundColour` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Show loading indicator `brand.showLoadingIndicator` | toggle | no | — | on | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Intro video `brand.introVideoAssetRef` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001 | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). | on publish (CMS-014): web at once, the app on its next launch |
| Intro video mode `brand.introVideoMode` | segmented control | no | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | GST-001 | When GST-001 plays it full screen. "Skip introduction" is always shown. | on publish (CMS-014): web at once, the app on its next launch |
| Powered by TICVAI credit `brand.showPoweredBy` | toggle | no | — | on | every guest screen (web, app and kiosk) | the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 powered-by-locked) | on publish (CMS-014): web at once, the app on its next launch |

### Theme: colours, shape, surfaces

Set on `CMS-005` Theme Editor, `ADM-016` White-Label Branding Management through `setTheme`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Primary colour `theme.primaryColour` | colour picker | yes | #RRGGBB | — | every guest screen (web, app and kiosk) | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings | on publish (CMS-014): web at once, the app on its next launch |
| Secondary colour `theme.secondaryColour` | colour picker | yes | #RRGGBB | — | every guest screen (web, app and kiosk) | secondary buttons and secondary emphasis: unselected chips, secondary tabs | on publish (CMS-014): web at once, the app on its next launch |
| Accent colour `theme.accentColour` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices | on publish (CMS-014): web at once, the app on its next launch |
| Background colour `theme.backgroundColour` | colour picker | yes | #RRGGBB | — | every guest screen (web, app and kiosk) | the page background behind every screen (the `ground` token) | on publish (CMS-014): web at once, the app on its next launch |
| Text colour `theme.textColour` | colour picker | yes | #RRGGBB | — | every guest screen (web, app and kiosk) | body text on the background | on publish (CMS-014): web at once, the app on its next launch |
| Corner radius `theme.cornerRadius` | stepper or slider | no | min 0; max 32 | — | every guest screen (web, app and kiosk) | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) | on publish (CMS-014): web at once, the app on its next launch |
| Surface style `theme.surfaceStyle` | segmented control | no | Glass · Solid | Glass | every guest screen (web, app and kiosk) | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) | on publish (CMS-014): web at once, the app on its next launch |
| Button style `theme.buttonStyle` | segmented control | no | Solid · Outline · Pill | Solid | every guest screen (web, app and kiosk) | every button's shape: solid fill, outline, or pill | on publish (CMS-014): web at once, the app on its next launch |
| Component colours `theme.componentColours` | group | no | — | — | every guest screen (web, app and kiosk) | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: primary CTA `theme.componentColours.primaryCta` | group | no | — | — | every guest screen (web, app and kiosk) | the one main call to action on each screen, when it should differ from the brand colour | on publish (CMS-014): web at once, the app on its next launch |
| Primary CTA: background `theme.componentColours.primaryCta.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Primary CTA: text `theme.componentColours.primaryCta.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: pay button `theme.componentColours.payButton` | group | no | — | — | every guest screen (web, app and kiosk) | the Pay button at checkout | on publish (CMS-014): web at once, the app on its next launch |
| Pay button: background `theme.componentColours.payButton.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Pay button: text `theme.componentColours.payButton.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: add to cart `theme.componentColours.addToCart` | group | no | — | — | every guest screen (web, app and kiosk) | every Add to cart button | on publish (CMS-014): web at once, the app on its next launch |
| Add to cart: background `theme.componentColours.addToCart.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Add to cart: text `theme.componentColours.addToCart.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: buy tickets button `theme.componentColours.buyTicketsButton` | group | no | — | — | every guest screen (web, app and kiosk) | the persistent Buy tickets button (mobile tab bar) | on publish (CMS-014): web at once, the app on its next launch |
| Buy tickets button: background `theme.componentColours.buyTicketsButton.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Buy tickets button: text `theme.componentColours.buyTicketsButton.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: link `theme.componentColours.link` | group | no | — | — | every guest screen (web, app and kiosk) | text links | on publish (CMS-014): web at once, the app on its next launch |
| Link: background `theme.componentColours.link.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Link: text `theme.componentColours.link.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Component colours: badge `theme.componentColours.badge` | group | no | — | — | every guest screen (web, app and kiosk) | badges on cards (LIMITED, NEW, 11 left) | on publish (CMS-014): web at once, the app on its next launch |
| Badge: background `theme.componentColours.badge.background` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Badge: text `theme.componentColours.badge.text` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |

### Fonts

Set on `CMS-003` Typography through `setFonts`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Primary latin `fonts.primaryLatin` | text field | yes | — | — | every guest screen (web, app and kiosk) | headings and body text in English | on publish (CMS-014): web at once, the app on its next launch |
| Primary arabic `fonts.primaryArabic` | text field | no | Required when `ar` is among the tenant's languages (audit R163). | — | every guest screen (web, app and kiosk) | headings and body text in Arabic | on publish (CMS-014): web at once, the app on its next launch |
| Secondary latin `fonts.secondaryLatin` | text field | no | — | — | every guest screen (web, app and kiosk) | the secondary face (eyebrows, numbers) in English | on publish (CMS-014): web at once, the app on its next launch |
| Secondary arabic `fonts.secondaryArabic` | text field | no | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | every guest screen (web, app and kiosk) | the secondary face in Arabic | on publish (CMS-014): web at once, the app on its next launch |
| Custom font images `fonts.customFontAssetRefs` | media picker (several) | no | PNG, JPG, SVG or MP4 from the media library | — | every guest screen (web, app and kiosk) | Uploaded font files, as `MediaAsset` ids. | on publish (CMS-014): web at once, the app on its next launch |

### Header

Set on `CMS-009` Navigation & Menus through `setHeader`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Header layout `header.layout` | segmented control | yes | Logo left · Logo centre · Logo with menu | — | every guest screen (web, app and kiosk) | the header: logo left, logo centred, or logo with the menu | on publish (CMS-014): web at once, the app on its next launch |
| Show logo `header.showLogo` | toggle | no | — | on | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Show menu `header.showMenu` | toggle | no | — | on | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Show notifications `header.showNotifications` | toggle | no | — | on | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Background colour `header.backgroundColour` | colour picker | no | #RRGGBB | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |

### Navigation: menu, tab bar, Buy tickets button

Set on `CMS-009` Navigation & Menus through `setNavigation`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Navigation kind `navigation.kind` | segmented control | yes | Bottom navigation · Drawer · Tabs | — | every guest screen (web, app and kiosk) | the main navigation: bottom tab bar, drawer, or tabs | on publish (CMS-014): web at once, the app on its next launch |
| Navigation items `navigation.items` | repeatable rows | yes | at most 12 | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Items: label `navigation.items[].label` | text, one per language | yes | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Items: icon `navigation.items[].icon` | text field | no | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Items: target `navigation.items[].target` | group | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Target: kind `navigation.items[].target.kind` | select | yes | Module · Content page · Product · Event · External URL · App section · None | — | every guest screen (web, app and kiosk) | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | on publish (CMS-014): web at once, the app on its next launch |
| Target: module key `navigation.items[].target.moduleKey` | select | no | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | on publish (CMS-014): web at once, the app on its next launch |
| Target: app section `navigation.items[].target.appSection` | select | no | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | every guest screen (web, app and kiosk) | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | on publish (CMS-014): web at once, the app on its next launch |
| Target: content page `navigation.items[].target.contentPageId` | picker: choose a content page | no | shows names, sends the id | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Target: product `navigation.items[].target.productId` | picker: choose a product | no | shows names, sends the id | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Target: event `navigation.items[].target.eventId` | picker: choose an event | no | shows names, sends the id | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Target: uRL `navigation.items[].target.url` | text field | no | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Items: is visible `navigation.items[].isVisible` | toggle | yes | At most five may be visible in bottom navigation; the rest overflow. | — | every guest screen (web, app and kiosk) | At most five may be visible in bottom navigation; the rest overflow. | on publish (CMS-014): web at once, the app on its next launch |
| Items: sort order `navigation.items[].sortOrder` | number field | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Buy button `navigation.buyButton` | group | no | — | — | GST-003 | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. | on publish (CMS-014): web at once, the app on its next launch |
| Buy button: style `navigation.buyButton.style` | radio group | no | Raised · Floating · Flat · Hidden | Raised | every P02 screen | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden | on publish (CMS-014): web at once, the app on its next launch |
| Buy button: label `navigation.buyButton.label` | text, one per language | no | English and Arabic (Arabic right to left) | — | every guest screen (web, app and kiosk) | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |

### Footer

Set on `CMS-009` Navigation & Menus through `setFooter`. Reaches every website screen.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Footer columns `footer.columns` | repeatable rows | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Columns: heading `footer.columns[].heading` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Columns: links `footer.columns[].links` | repeatable rows | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Links: label `footer.columns[].links[].label` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Links: uRL `footer.columns[].links[].url` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Links: opens cookie preferences `footer.columns[].links[].opensCookiePreferences` | toggle | no | — | off | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Legal links `footer.legalLinks` | group | no | — | — | every website screen | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. | on publish (CMS-014): web at once, the app on its next launch |
| Legal links: terms URL `footer.legalLinks.termsUrl` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Legal links: privacy URL `footer.legalLinks.privacyUrl` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Legal links: accessibility URL `footer.legalLinks.accessibilityUrl` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Legal links: cookie policy URL `footer.legalLinks.cookiePolicyUrl` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Copyright text `footer.copyrightText` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Social links `footer.socialLinks` | repeatable rows | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Social links: platform `footer.socialLinks[].platform` | text field | no | — | — | GST-018, GST-066, WEB-018 | — | on publish (CMS-014): web at once, the app on its next launch |
| Social links: uRL `footer.socialLinks[].url` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |

### Languages and right-to-left

Set on `CMS-011` Translations, `ADM-018` Interface Languages through `setLanguages`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Languages `languages.languages` | list of values (chips) | yes | at least 1 | — | every guest screen (web, app and kiosk) | the language button in the header; Arabic flips every screen right to left | on publish (CMS-014): web at once, the app on its next launch |
| Default language `languages.defaultLanguage` | language picker | yes | ISO 639-1 code, shown as the language name | — | every guest screen (web, app and kiosk) | the language a first visit opens in | on publish (CMS-014): web at once, the app on its next launch |

### Modules shown to guests

Set on `CMS-001` Tenant Workspace, `ADM-424` Module Activation & Dependency Validation through `setModuleEnablement`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Modules `modules.modules` | repeatable rows | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Modules: module key `modules.modules[].moduleKey` | select | yes | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | on publish (CMS-014): web at once, the app on its next launch |
| Modules: is enabled `modules.modules[].isEnabled` | toggle | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |

### Features

Set on `CMS-001` Tenant Workspace through `setFeatureToggles`. Reaches every guest screen (web, app and kiosk).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Features `features.features` | repeatable rows | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |
| Features: feature key `features.features[].featureKey` | select | yes | Digital companion mode · AI concierge chat · Lost and found · Push notifications · Social sharing · Multi language · Apple wallet · Google pay · Apple pay · Cash on delivery · Guest checkout · Uae pass login | — | every guest screen (web, app and kiosk) | The feature toggles a tenant can set — one list for `FeatureToggle` and the `setFeatureToggles` body, which took a free string where the response had this enum. | on publish (CMS-014): web at once, the app on its next launch |
| Features: is enabled `features.features[].isEnabled` | toggle | yes | — | — | every guest screen (web, app and kiosk) | — | on publish (CMS-014): web at once, the app on its next launch |

### Booking settings (tenant, with per-venue overrides)

Set on `CMS-016` Site Settings through `setBookingFlowConfig`. Reaches the booking steps. A venue may override any of these for itself (`venueOverrides`).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Booking settings preset `bookingFlow.preset` | select | no | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | on publish (CMS-014): web at once, the app on its next launch |
| Step indicator `bookingFlow.stepIndicator` | select | no | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none | on publish (CMS-014): web at once, the app on its next launch |
| Cart layout `bookingFlow.cartLayout` | select | no | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon | on publish (CMS-014): web at once, the app on its next launch |
| Cart side in RTL `bookingFlow.cartSideInRtl` | segmented control | no | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the cart's side in Arabic: kept right, or mirrored left | on publish (CMS-014): web at once, the app on its next launch |
| Card layout `bookingFlow.cardLayout` | radio group | no | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | ticket and product cards: stacked rows, split rows, cards across, or poster cards | on publish (CMS-014): web at once, the app on its next launch |
| Card size `bookingFlow.cardSize` | radio group | no | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | card size: compact, standard, large, extra large | on publish (CMS-014): web at once, the app on its next launch |
| Seat picker `bookingFlow.seatPicker` | radio group | no | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | on publish (CMS-014): web at once, the app on its next launch |
| Map view `bookingFlow.mapView` | segmented control | no | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Booking settings density `bookingFlow.density` | segmented control | no | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | spacing of the booking screens: compact, standard, roomy | on publish (CMS-014): web at once, the app on its next launch |
| Embed mode `bookingFlow.embedMode` | segmented control | no | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | full page, or embedded in the venue's own site (no hero, event page or venue header) | on publish (CMS-014): web at once, the app on its next launch |
| Hero banner `bookingFlow.heroBanner` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the hero banner at the top of the booking pages | on publish (CMS-014): web at once, the app on its next launch |
| Search in banner `bookingFlow.searchInBanner` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | on publish (CMS-014): web at once, the app on its next launch |
| Event banner dates `bookingFlow.eventBannerDates` | toggle | no | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. | on publish (CMS-014): web at once, the app on its next launch |
| Single event page `bookingFlow.singleEventPage` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Quantities on add ons `bookingFlow.quantitiesOnAddOns` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Times per page `bookingFlow.timesPerPage` | radio group | no | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … | on publish (CMS-014): web at once, the app on its next launch |
| Day part filter `bookingFlow.dayPartFilter` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). | on publish (CMS-014): web at once, the app on its next launch |
| Day part boundaries `bookingFlow.dayPartBoundaries` | group | no | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). | on publish (CMS-014): web at once, the app on its next launch |
| Day part boundaries: afternoon starts at `bookingFlow.dayPartBoundaries.afternoonStartsAt` | time picker | no | HH:mm, 24-hour | 12:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Day part boundaries: evening starts at `bookingFlow.dayPartBoundaries.eveningStartsAt` | time picker | no | HH:mm, 24-hour | 17:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Seat view position `bookingFlow.seatViewPosition` | radio group | no | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). | on publish (CMS-014): web at once, the app on its next launch |
| Seat time bar `bookingFlow.seatTimeBar` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. | on publish (CMS-014): web at once, the app on its next launch |
| Ticket categories `bookingFlow.ticketCategories` | segmented control | no | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. | on publish (CMS-014): web at once, the app on its next launch |
| Ticket tags `bookingFlow.ticketTags` | toggle | no | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. | on publish (CMS-014): web at once, the app on its next launch |
| Card info `bookingFlow.cardInfo` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. | on publish (CMS-014): web at once, the app on its next launch |
| Concierge mascot `bookingFlow.conciergeMascot` | toggle | no | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). | on publish (CMS-014): web at once, the app on its next launch |
| Show info only `bookingFlow.showInfoOnly` | toggle | no | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. | on publish (CMS-014): web at once, the app on its next launch |
| Location switcher `bookingFlow.locationSwitcher` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). | on publish (CMS-014): web at once, the app on its next launch |
| Guest contact fields `bookingFlow.guestContactFields` | multi-select chips | no | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). | on publish (CMS-014): web at once, the app on its next launch |
| Date strip days `bookingFlow.dateStripDays` | stepper or slider (days) | no | min 3; max 31 | 7 | GST-007, GST-008, GST-009, GST-041, WEB-004, WEB-005, WEB-006, WEB-007 … (12) | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. | on publish (CMS-014): web at once, the app on its next launch |
| Venue overrides `bookingFlow.venueOverrides` | repeatable rows | no | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | GST-001, GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, GST-049 … (17) | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | on publish (CMS-014): web at once, the app on its next launch |
| Venue overrides: venue `bookingFlow.venueOverrides[].venueId` | picker: choose a venue | yes | At most one override per venue. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | One of the tenant's active venues. At most one override per venue. | on publish (CMS-014): web at once, the app on its next launch |
| Venue overrides: settings `bookingFlow.venueOverrides[].settings` | group | yes | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: preset `bookingFlow.venueOverrides[].settings.preset` | select | no | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: step indicator `bookingFlow.venueOverrides[].settings.stepIndicator` | select | no | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Settings: cart layout `bookingFlow.venueOverrides[].settings.cartLayout` | select | no | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: cart side in RTL `bookingFlow.venueOverrides[].settings.cartSideInRtl` | segmented control | no | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: card layout `bookingFlow.venueOverrides[].settings.cardLayout` | radio group | no | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: card size `bookingFlow.venueOverrides[].settings.cardSize` | radio group | no | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: seat picker `bookingFlow.venueOverrides[].settings.seatPicker` | radio group | no | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: map view `bookingFlow.venueOverrides[].settings.mapView` | segmented control | no | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Settings: density `bookingFlow.venueOverrides[].settings.density` | segmented control | no | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: embed mode `bookingFlow.venueOverrides[].settings.embedMode` | segmented control | no | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: hero banner `bookingFlow.venueOverrides[].settings.heroBanner` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Settings: search in banner `bookingFlow.venueOverrides[].settings.searchInBanner` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: event banner dates `bookingFlow.venueOverrides[].settings.eventBannerDates` | toggle | no | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: single event page `bookingFlow.venueOverrides[].settings.singleEventPage` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Settings: quantities on add ons `bookingFlow.venueOverrides[].settings.quantitiesOnAddOns` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Settings: times per page `bookingFlow.venueOverrides[].settings.timesPerPage` | radio group | no | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … | on publish (CMS-014): web at once, the app on its next launch |
| Settings: day part filter `bookingFlow.venueOverrides[].settings.dayPartFilter` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: day part boundaries `bookingFlow.venueOverrides[].settings.dayPartBoundaries` | group | no | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: seat view position `bookingFlow.venueOverrides[].settings.seatViewPosition` | radio group | no | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: seat time bar `bookingFlow.venueOverrides[].settings.seatTimeBar` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: ticket categories `bookingFlow.venueOverrides[].settings.ticketCategories` | segmented control | no | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: ticket tags `bookingFlow.venueOverrides[].settings.ticketTags` | toggle | no | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: card info `bookingFlow.venueOverrides[].settings.cardInfo` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: concierge mascot `bookingFlow.venueOverrides[].settings.conciergeMascot` | toggle | no | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: show info only `bookingFlow.venueOverrides[].settings.showInfoOnly` | toggle | no | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: location switcher `bookingFlow.venueOverrides[].settings.locationSwitcher` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: guest contact fields `bookingFlow.venueOverrides[].settings.guestContactFields` | multi-select chips | no | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: date strip days `bookingFlow.venueOverrides[].settings.dateStripDays` | stepper or slider (days) | no | min 3; max 31 | 7 | GST-007, GST-008, GST-009, GST-041, WEB-004, WEB-005, WEB-006, WEB-007 … (12) | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. | on publish (CMS-014): web at once, the app on its next launch |

### Booking flows: steps, their order and per-flow settings

Set on `CMS-102` Site Builder, `CMS-103` Booking Flows through `createBookingFlowDefinition`, `updateBookingFlowDefinition`. Reaches the booking steps.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Flow type key `bookingFlows.flowTypeKey` | select | yes | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow types the system catalogue offers (decided 29 September, W12; impact.md b). | on publish (CMS-014): web at once, the app on its next launch |
| Booking flows name `bookingFlows.name` | text field | yes | max length 80 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Staff-facing, e.g. "Day pass, date first". | on publish (CMS-014): web at once, the app on its next launch |
| Is default for type `bookingFlows.isDefaultForType` | toggle | no | At most one per venue and type; setting it takes it from the previous default. | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | At most one per venue and type; setting it takes it from the previous default. | on publish (CMS-014): web at once, the app on its next launch |
| Booking flows is enabled `bookingFlows.isEnabled` | toggle | no | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A disabled flow is kept and not published; products naming it fall back to the default. | on publish (CMS-014): web at once, the app on its next launch |
| Steps `bookingFlows.steps` | repeatable rows | no | at most 30 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step of the type, in the venue's order. Filled from the type when left out on create. | on publish (CMS-014): web at once, the app on its next launch |
| Steps: step key `bookingFlows.steps[].stepKey` | select | yes | Location · Help me choose · Product · Date · Time · Performance · Level · Language · Duration · Route · Party size · Resource map … | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every step a guest booking flow can hold (decided 29 September, W12). What each step does on WEB and MOB, and which screen draws it, is in the screen definitions of P01 and P02; which types carry which steps is … | on publish (CMS-014): web at once, the app on its next launch |
| Steps: enabled `bookingFlows.steps[].enabled` | toggle | yes | A `required` step cannot be off; the flow saves and `isValid` turns false. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | A `required` step cannot be off; the flow saves and `isValid` turns false. | on publish (CMS-014): web at once, the app on its next launch |
| Steps: sort order `bookingFlows.steps[].sortOrder` | number field | yes | min 0 | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — | on publish (CMS-014): web at once, the app on its next launch |
| Steps: settings `bookingFlows.steps[].settings` | key and value settings | no | A name the type does not give is refused with 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. | on publish (CMS-014): web at once, the app on its next launch |
| Settings `bookingFlows.settings` | group | no | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The settings that belong to one flow, not to the venue (decided 29 September, W12). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: performance reveal `bookingFlows.settings.performanceReveal` | segmented control | no | Date time ticket · All at once | Date time ticket | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Performance reveal (rev 3 REV3-2). `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: sign in at `bookingFlows.settings.signInAt` | segmented control | no | After add ons · At payment | After add ons | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3). | on publish (CMS-014): web at once, the app on its next launch |
| Settings: seat event date mode `bookingFlows.settings.seatEventDateMode` | segmented control | no | Inline step · Popup on seat map; Read only by the seated flow types. | Inline step | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Date and time on a seated event (rev 3 REV3-4). `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: extras step `bookingFlows.settings.extrasStep` | segmented control | no | Auto · Always · Never; `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: quick tour `bookingFlows.settings.quickTour` | toggle | no | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Quick tour (rev 3 REV3-20). A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. | on publish (CMS-014): web at once, the app on its next launch |
| Settings: consent questions `bookingFlows.settings.consentQuestionIds` | multi-picker: choose consent questions | no | at most 10; no duplicates; Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The flow's own consent questions (rev 3 REV3-26). Asked on every booking through this flow, together with those of each product in the cart, each question once. | on publish (CMS-014): web at once, the app on its next launch |

### Homepage sections

Set on `CMS-007` Page Builder through `setHomepageLayout`. Reaches the guest home screens.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Landing-page template `homepage.templateKey` | template picker: name and thumbnail (listLandingPageTemplates) | no | — | — | WEB-001 | the landing-page template the home started from (listLandingPageTemplates); a tenant with no landing page of its own starts from one, and the sections it fills stay editable | on publish (CMS-014): web at once, the app on its next launch |
| Landing source `homepage.landingSource` | segmented control | no | Storefront · Own site | Storefront | the guest home screens | whether the storefront home is the landing page, or the tenant's own site is and links in with deep links | on publish (CMS-014): web at once, the app on its next launch |
| Sections `homepage.sections` | repeatable rows | yes | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Sections: kind `homepage.sections[].kind` | select | yes | Hero banner · Quick actions · Tickets · Whats on · Attractions · Membership · Dining · Shop · Promotions · Map · Custom content · Venue overview …; `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events` … | — | the guest home screens | Which module each section needs, proposed, client to correct (decided 28 September, audit R163). | on publish (CMS-014): web at once, the app on its next launch |
| Sections: title `homepage.sections[].title` | text, one per language | no | English and Arabic (Arabic right to left) | — | the guest home screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Sections: sort order `homepage.sections[].sortOrder` | number field | yes | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Sections: is visible `homepage.sections[].isVisible` | toggle | yes | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Sections: content page `homepage.sections[].contentPageId` | picker: choose a content page | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Sections: card count `homepage.sections[].maxItems` | number field | no | — | — | GST-001, WEB-001 | how many cards the section shows, the counts the approved wireframe offers | on publish (CMS-014): web at once, the app on its next launch |
| Sections: scroll animation `homepage.sections[].scrollAnimation` | radio group | no | Rise · Scale · Slide · Blur · None | Rise | the guest home screens | how the section enters as the guest scrolls: rise, scale, slide, blur or none (none whenever the device asks for reduced motion) | on publish (CMS-014): web at once, the app on its next launch |
| Sections: hero style `homepage.sections[].heroStyle` | radio group | no | Carousel · Video · Poster · Split | — | GST-001 | For `heroBanner` only (decided 29 September, MOB-3). | on publish (CMS-014): web at once, the app on its next launch |

### Banners

Set on `CMS-008` Content Blocks through `createBanner`, `updateBanner`. Reaches the guest home screens.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Banners title `banners.title` | text, one per language | yes | English and Arabic (Arabic right to left) | — | the guest home screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Banners subtitle `banners.subtitle` | text, one per language | no | English and Arabic (Arabic right to left) | — | the guest home screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Image `banners.imageAssetRef` | upload, or pick from the media library | yes | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Banners placement `banners.placement` | radio group | no | Homepage hero · Homepage block · Explore · Checkout | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Banners link target `banners.linkTarget` | group | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: kind `banners.linkTarget.kind` | select | yes | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: module key `banners.linkTarget.moduleKey` | select | no | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: app section `banners.linkTarget.appSection` | select | no | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: content page `banners.linkTarget.contentPageId` | picker: choose a content page | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: product `banners.linkTarget.productId` | picker: choose a product | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: event `banners.linkTarget.eventId` | picker: choose an event | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: uRL `banners.linkTarget.url` | text field | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Banners starts at `banners.startsAt` | date and time picker | yes | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Banners ends at `banners.endsAt` | date and time picker | no | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when set (decided 28 September, audit R163). Null runs the banner with no end. | on publish (CMS-014): web at once, the app on its next launch |
| Banners sort order `banners.sortOrder` | number field | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Is active `banners.isActive` | toggle | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |

### Promo blocks

Set on `CMS-008` Content Blocks through `createPromoBlock`, `updatePromoBlock`. Reaches the guest home screens.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Promo blocks title `promoBlocks.title` | text, one per language | yes | English and Arabic (Arabic right to left) | — | the guest home screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Promo blocks description `promoBlocks.description` | text, one per language | no | English and Arabic (Arabic right to left) | — | the guest home screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Icon `promoBlocks.iconAssetRef` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Promotion `promoBlocks.promotionId` | picker: choose a promotion | no | shows names, sends the id | — | the guest home screens | Presentation only. A block may point at a promotion; it does not create or price one. | on publish (CMS-014): web at once, the app on its next launch |
| Promo blocks link target `promoBlocks.linkTarget` | group | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: kind `promoBlocks.linkTarget.kind` | select | yes | Module · Content page · Product · Event · External URL · App section · None | — | the guest home screens | `appSection` points at a section of the guest mobile app (decided 29 September, MOB-1), so the bottom navigation can hold Home, Explore, Plan and Tickets. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: module key `promoBlocks.linkTarget.moduleKey` | select | no | Tickets and booking · Membership · Events · Attractions · Virtual queue · Dining and fnb · Shop · Parking · Gamification · Photo gallery · Wallet · Loyalty … | — | WEB-050 | `visitPlanner` (decided 29 September, MOB-1 and the Plan tab in Block A) is the Plan tab and WEB-050; off, the tab and the page are not shown. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: app section `promoBlocks.linkTarget.appSection` | select | no | Home · Explore · Plan · Tickets · Map · Account · Buy tickets; Required when `kind` is `appSection`. | — | the guest home screens | Required when `kind` is `appSection`. `plan` needs the `visitPlanner` module and `map` the `map` module enabled, or `setNavigation` refuses it. | on publish (CMS-014): web at once, the app on its next launch |
| Link target: content page `promoBlocks.linkTarget.contentPageId` | picker: choose a content page | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: product `promoBlocks.linkTarget.productId` | picker: choose a product | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: event `promoBlocks.linkTarget.eventId` | picker: choose an event | no | shows names, sends the id | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Link target: uRL `promoBlocks.linkTarget.url` | text field | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Promo blocks starts at `promoBlocks.startsAt` | date and time picker | no | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Promo blocks ends at `promoBlocks.endsAt` | date and time picker | no | 1 Oct 2026, 14:30 (venue time zone) | — | the guest home screens | Must follow `startsAt` when both are set (decided 28 September, audit R163). | on publish (CMS-014): web at once, the app on its next launch |
| Promo blocks sort order `promoBlocks.sortOrder` | number field | no | — | — | the guest home screens | — | on publish (CMS-014): web at once, the app on its next launch |

### Help me choose

Set on `CMS-101` Help Me Choose through `createGuidedChoice`, `updateGuidedChoice`. Reaches Help me choose.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Help me choose name `guidedChoices.name` | text field | yes | max length 80 | — | GST-003, GST-008, WEB-002, WEB-005 | Staff-facing name, e.g. "Water park day planner". | on publish (CMS-014): web at once, the app on its next launch |
| Help me choose mode `guidedChoices.mode` | segmented control | yes | Button · Popup on arrival · Off | Button | GST-003, GST-008, WEB-002, WEB-005 | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on … | on publish (CMS-014): web at once, the app on its next launch |
| Show banner `guidedChoices.showBanner` | toggle | no | — | on | GST-003, GST-008, WEB-002, WEB-005 | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. | on publish (CMS-014): web at once, the app on its next launch |
| Help me choose behaviour `guidedChoices.behaviour` | segmented control | no | Filter · Recommend | Filter | GST-003, GST-008, WEB-002, WEB-005 | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). | on publish (CMS-014): web at once, the app on its next launch |
| Show everything `guidedChoices.showEverything` | toggle | no | — | on | GST-003, GST-008, WEB-002, WEB-005 | The "Show everything" link under a filtered list, which clears the answers (W4). | on publish (CMS-014): web at once, the app on its next launch |
| Help me choose questions `guidedChoices.questions` | repeatable rows | yes | at least 1; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). | on publish (CMS-014): web at once, the app on its next launch |
| Questions: title `guidedChoices.questions[].title` | text, one per language | yes | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Questions: kind `guidedChoices.questions[].kind` | radio group | no | Choice · Yes no · Age · Level · Certification | Choice | GST-003, GST-008, WEB-002, WEB-005 | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. | on publish (CMS-014): web at once, the app on its next launch |
| Questions: sort order `guidedChoices.questions[].sortOrder` | number field | yes | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — | on publish (CMS-014): web at once, the app on its next launch |
| Questions: answers `guidedChoices.questions[].answers` | repeatable rows | yes | at least 2; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). | on publish (CMS-014): web at once, the app on its next launch |
| Answers: title `guidedChoices.questions[].answers[].title` | text, one per language | yes | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Answers: body `guidedChoices.questions[].answers[].body` | text, one per language | no | The one-liner under the title, at most 140 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | The one-liner under the title, at most 140 characters in each language. | on publish (CMS-014): web at once, the app on its next launch |
| Answers: icon `guidedChoices.questions[].answers[].icon` | text field | no | max length 40 | — | GST-003, GST-008, WEB-002, WEB-005 | An icon name from the guest app's icon set. | on publish (CMS-014): web at once, the app on its next launch |
| Answers: badge `guidedChoices.questions[].answers[].badge` | text, one per language | no | At most 24 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | Optional, e.g. "Best value". | on publish (CMS-014): web at once, the app on its next launch |
| Answers: sort order `guidedChoices.questions[].answers[].sortOrder` | number field | yes | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — | on publish (CMS-014): web at once, the app on its next launch |
| Answers: target `guidedChoices.questions[].answers[].target` | group | no | — | — | GST-003, GST-008, WEB-002, WEB-005 | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. | on publish (CMS-014): web at once, the app on its next launch |
| Answers: filter `guidedChoices.questions[].answers[].filter` | group | no | — | — | GST-003, GST-008, WEB-002, WEB-005 | What this answer keeps in the list (decided 29 September, W4). Every field set must hold; answers to different questions are combined with AND. | on publish (CMS-014): web at once, the app on its next launch |
| Answers: consent prefill `guidedChoices.questions[].answers[].consentPrefill` | group | no | — | — | GST-003, GST-008, WEB-002, WEB-005 | Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4). | on publish (CMS-014): web at once, the app on its next launch |
| Answers: result `guidedChoices.questions[].answers[].result` | group | no | — | — | GST-003, GST-008, WEB-002, WEB-005 | The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image. | on publish (CMS-014): web at once, the app on its next launch |

### Content pages

Set on `CMS-007` Page Builder through `createContentPage`, `updateContentPage`. Reaches the content and policy pages.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Slug `pages.slug` | text field | yes | pattern `^[a-z0-9-]+$` | — | the content and policy pages | — | on publish (CMS-014): web at once, the app on its next launch |
| Content pages title `pages.title` | text, one per language | yes | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Body `pages.body` | rich text, one per language | yes | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. | on publish (CMS-014): web at once, the app on its next launch |
| Content pages is enabled `pages.isEnabled` | toggle | no | — | on | the content and policy pages | BL-005. Enablement is not publication. | on publish (CMS-014): web at once, the app on its next launch |
| Icon `pages.iconAssetRef` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the content and policy pages | — | on publish (CMS-014): web at once, the app on its next launch |
| Category code `pages.categoryCode` | text field | no | — | — | GST-057 | — | on publish (CMS-014): web at once, the app on its next launch |
| Content pages sort order `pages.sortOrder` | number field | no | — | — | the content and policy pages | — | on publish (CMS-014): web at once, the app on its next launch |
| Content pages status `pages.status` | segmented control | no | Draft · Published · Archived | — | the content and policy pages | Only `archived` is taken — send it to withdraw a published page or abandon a draft (`states/content.yaml`). | on publish (CMS-014): web at once, the app on its next launch |

### Policies (terms, privacy, refunds)

Set on `CMS-018` Consent & Legal through `setPolicy`. Reaches the content and policy pages.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Body `policies.body` | rich text, one per language | yes | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. | on publish (CMS-014): web at once, the app on its next launch |
| Requires reconsent `policies.requiresReconsent` | toggle | yes | — | — | the content and policy pages | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. | on publish (CMS-014): web at once, the app on its next launch |
| Effective from `policies.effectiveFrom` | date picker | no | 1 Oct 2026 (dd MMM yyyy) | — | the content and policy pages | — | on publish (CMS-014): web at once, the app on its next launch |

### FAQs

Set on no CMS screen calls it yet through `setFaqs`. Reaches the FAQ screens.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Categories `faqs.categories` | repeatable rows | yes | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories: code `faqs.categories[].code` | text field | yes | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories: name `faqs.categories[].name` | text, one per language | yes | English and Arabic (Arabic right to left) | — | the FAQ screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Categories: sort order `faqs.categories[].sortOrder` | number field | no | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories: entries `faqs.categories[].entries` | repeatable rows | yes | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Entries: iD `faqs.categories[].entries[].id` | picker: choose an id | yes | shows names, sends the id | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Entries: question `faqs.categories[].entries[].question` | text, one per language | yes | English and Arabic (Arabic right to left) | — | the FAQ screens | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Entries: answer `faqs.categories[].entries[].answer` | rich text, one per language | yes | English and Arabic (Arabic right to left) | — | the FAQ screens | Keyed by language code. Values are sanitised HTML. | on publish (CMS-014): web at once, the app on its next launch |
| Entries: sort order `faqs.categories[].entries[].sortOrder` | number field | no | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |
| Entries: is published `faqs.categories[].entries[].isPublished` | toggle | no | — | — | the FAQ screens | — | on publish (CMS-014): web at once, the app on its next launch |

### Availability and maintenance

Set on `CMS-001` Tenant Workspace through `setMaintenanceMode`. Reaches the screens that check availability (every screen shows maintenance).

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Is in maintenance `maintenance.isInMaintenance` | toggle | yes | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Availability and maintenance message `maintenance.message` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Expected back at `maintenance.expectedBackAt` | date and time picker | no | 1 Oct 2026, 14:30 (venue time zone) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Minimum app version `maintenance.minimumAppVersion` | group | no | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | The oldest guest app build still allowed to run (decided 28 September, audit R073). | on publish (CMS-014): web at once, the app on its next launch |
| Minimum app version: ios `maintenance.minimumAppVersion.ios` | text field | no | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Minimum app version: android `maintenance.minimumAppVersion.android` | text field | no | pattern `^\d+\.\d+\.\d+$` | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Contact `maintenance.contact` | group | no | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (14) | How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). | on publish (CMS-014): web at once, the app on its next launch |
| Contact: phone `maintenance.contact.phone` | phone field | no | +971 5X XXX XXXX (E.164) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Contact: email `maintenance.contact.email` | email field | no | name@example.ae | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Contact: whatsapp `maintenance.contact.whatsapp` | text field | no | — | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | — | on publish (CMS-014): web at once, the app on its next launch |
| Contact: address `maintenance.contact.address` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |
| Contact: opening hours `maintenance.contact.openingHours` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | Prose, as the guest reads it. The bookable hours are the catalogue's. | on publish (CMS-014): web at once, the app on its next launch |
| Availability `maintenance.availability` | segmented control | no | Open · Sold out · Closed | Open | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | The sold-out or closed signal (decided 28 September, audit R073). `open` is the normal state. | on publish (CMS-014): web at once, the app on its next launch |
| Availability message `maintenance.availabilityMessage` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-029, GST-038, GST-040, GST-047, GST-051, KSK-002, KSK-014 … (13) | Keyed by ISO 639-1 code. Every enabled language should be present. | on publish (CMS-014): web at once, the app on its next launch |

### Custom domain

Set on `CMS-017` Domain & Certificate, `ADM-017` Domain & Certificate Management through `claimCustomDomain`. Reaches every website screen.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Custom domain hostname `domains.hostname` | text field | yes | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Custom domain kind `domains.kind` | radio group | yes | Guest web · Guest app · Partner portal · Developer portal | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Verification method `domains.verificationMethod` | segmented control | no | Dns txt · Cname · Http file | Dns txt | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |

### SEO metadata

Set on `CMS-013` SEO & Metadata through `setSeoMetadata`. Reaches every website screen.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Entity kind `seo.entityKind` | select | yes | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Entity `seo.entityId` | picker: choose an entity | yes | shows names, sends the id | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Locale `seo.locale` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| SEO metadata title `seo.title` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Meta description `seo.metaDescription` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Keywords `seo.keywords` | list of values (chips) | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Canonical URL `seo.canonicalUrl` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Slug `seo.slug` | text field | no | — | — | every website screen | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. | on publish (CMS-014): web at once, the app on its next launch |
| Hreflang `seo.hreflang` | key and value settings | no | — | — | every website screen | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. | on publish (CMS-014): web at once, the app on its next launch |
| Schema org type `seo.schemaOrgType` | text field | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Open graph `seo.openGraph` | key and value settings | no | — | — | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |
| Is auto generated `seo.isAutoGenerated` | toggle | no | — | on | every website screen | 22.11.2. Generated by default and overridable. | on publish (CMS-014): web at once, the app on its next launch |
| No index `seo.noIndex` | toggle | no | — | off | every website screen | — | on publish (CMS-014): web at once, the app on its next launch |

### Cookie banner

Set on `CMS-026` Cookie Banner & Preference Center Designer through `setCookieBannerDesign`. Reaches the cookie banner.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Brand `cookieBanner.brandId` | picker: choose a brand | no | shows names, sends the id | — | GST-001, GST-066, WEB-001, WEB-024 | Null for the corporate design every brand inherits. | on publish (CMS-014): web at once, the app on its next launch |
| Inherits from `cookieBanner.inheritsFromId` | picker: choose an inherits from | no | shows names, sends the id | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Cookie banner channel `cookieBanner.channel` | select | yes | B2C website · Customer portal · Mobile app · Embedded checkout · White label site · Partner microsite | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Logo `cookieBanner.logoAssetId` | upload, or pick from the media library | no | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Cookie banner title `cookieBanner.title` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. | on publish (CMS-014): web at once, the app on its next launch |
| Body `cookieBanner.body` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. | on publish (CMS-014): web at once, the app on its next launch |
| Position `cookieBanner.position` | radio group | yes | Top · Bottom · Popup · Modal | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Theme `cookieBanner.themeId` | text field | no | — | — | GST-001, GST-066, WEB-001, WEB-024 | The white-label theme it takes colours and fonts from. | on publish (CMS-014): web at once, the app on its next launch |
| Buttons `cookieBanner.buttons` | repeatable rows | no | — | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Buttons: action `cookieBanner.buttons[].action` | radio group | yes | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | GST-001, GST-042, GST-066, WEB-001, WEB-016, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Buttons: label `cookieBanner.buttons[].label` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. | on publish (CMS-014): web at once, the app on its next launch |
| Reject is one click `cookieBanner.rejectIsOneClick` | toggle | yes | — | on | GST-001, GST-066, WEB-001, WEB-024 | Must be true. | on publish (CMS-014): web at once, the app on its next launch |
| Links `cookieBanner.links` | repeatable rows | no | — | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Links: label `cookieBanner.links[].label` | text, one per language | yes | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. | on publish (CMS-014): web at once, the app on its next launch |
| Links: policy kind `cookieBanner.links[].policyKind` | segmented control | yes | Privacy · Cookie · Terms and conditions | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories `cookieBanner.categories` | repeatable rows | yes | at least 1 | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories: category `cookieBanner.categories[].category` | radio group | yes | Strictly necessary · Functional · Analytics · Personalisation · Marketing | — | GST-001, GST-066, WEB-001, WEB-024 | — | on publish (CMS-014): web at once, the app on its next launch |
| Categories: description `cookieBanner.categories[].description` | text, one per language | no | English and Arabic (Arabic right to left) | — | GST-001, GST-066, WEB-001, WEB-024 | Text keyed by locale code, one entry per locale the venue publishes. | on publish (CMS-014): web at once, the app on its next launch |
| Categories: default on `cookieBanner.categories[].defaultOn` | toggle | yes | True only for `strictlyNecessary`, which is always active. | — | GST-001, GST-066, WEB-001, WEB-024 | True only for `strictlyNecessary`, which is always active. | on publish (CMS-014): web at once, the app on its next launch |
| Cookie banner languages `cookieBanner.languages` | list of values (chips) | yes | at least 1 | — | GST-001, GST-066, WEB-001, WEB-024 | Every language the storefront serves; Arabic renders right to left. | on publish (CMS-014): web at once, the app on its next launch |
| Regulatory regimes `cookieBanner.regulatoryRegimes` | multi-select chips | no | Gdpr · E privacy · Ccpa cpra · Lgpd · Uae pdpl · Saudi pdpl | — | GST-001, GST-066, WEB-001, WEB-024 | 2.6.60 (29 September, build). The laws this design is published to satisfy, so compliance is stated rather than assumed. | on publish (CMS-014): web at once, the app on its next launch |
| Record ip address `cookieBanner.recordIpAddress` | toggle | no | — | off | GST-001, GST-066, WEB-001, WEB-024 | 2.6.55, "if legally permitted" (29 September, build). On, `recordDeviceConsent` writes the IP address and user agent to `pii.consent_identifier`; off, they are not kept anywhere. | on publish (CMS-014): web at once, the app on its next launch |

### Analytics providers

Set on `CMS-016` Site Settings through `setAnalyticsProvider`. Reaches nothing drawn: tracking only.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Venue `analytics.venueId` | picker: choose a venue | no | shows names, sends the id | — | nothing drawn: tracking only | — | on publish (CMS-014): web at once, the app on its next launch |
| Provider `analytics.provider` | select | yes | Google analytics4 · Google tag manager · Adobe analytics · Meta pixel · Matomo · Other | — | nothing drawn: tracking only | — | on publish (CMS-014): web at once, the app on its next launch |
| Provider label `analytics.providerLabel` | text field | no | max length 100 | — | nothing drawn: tracking only | The name, when `provider` is `other`. | on publish (CMS-014): web at once, the app on its next launch |
| Measurement `analytics.measurementId` | text field | yes | max length 100 | — | nothing drawn: tracking only | What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id). | on publish (CMS-014): web at once, the app on its next launch |
| Surfaces `analytics.surfaces` | multi-select chips | yes | Guest web · Guest app; at least 1 | — | nothing drawn: tracking only | — | on publish (CMS-014): web at once, the app on its next launch |
| Consent category `analytics.consentCategory` | radio group | yes | Functional · Analytics · Personalisation · Marketing | Analytics | nothing drawn: tracking only | The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`). | on publish (CMS-014): web at once, the app on its next launch |
| Analytics providers is enabled `analytics.isEnabled` | toggle | yes | — | on | nothing drawn: tracking only | — | on publish (CMS-014): web at once, the app on its next launch |
| Reporting property `analytics.reportingPropertyId` | text field | no | max length 100 | — | nothing drawn: tracking only | The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). | on publish (CMS-014): web at once, the app on its next launch |
| Reporting credential ref `analytics.reportingCredentialRef` | text field | no | max length 200 | — | nothing drawn: tracking only | The vault reference of the reporting credential. Accepted, never returned. | on publish (CMS-014): web at once, the app on its next launch |

### App icons

Set on `CMS-004` Logo & Assets, `ADM-016` White-Label Branding Management through `setAppIcons`. Reaches no guest screen: the phone's home screen and the store listing.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Source image `appIcons.sourceAssetRef` | upload, or pick from the media library | yes | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | no guest screen: the phone's home screen and the store listing | The `MediaAsset` id of the 1024×1024 source, from `assets` `createUpload` then `completeUpload`. | needs an app build (CMS-104) on the native apps; the website takes it on publish |

### Store accounts

Set on `CMS-104` App Build & Store Publishing through `setStoreAccounts`. Reaches no guest screen: the phone's home screen and the store listing.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Accounts `storeAccounts.accounts` | repeatable rows | yes | at most 2 | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: store `storeAccounts.accounts[].store` | segmented control | yes | Apple app store · Google play | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: account holder name `storeAccounts.accounts[].accountHolderName` | text field | yes | max length 200 | — | no guest screen: the phone's home screen and the store listing | The client's legal entity as the store knows it. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: duns number `storeAccounts.accounts[].dunsNumber` | text field | no | pattern `^[0-9]{9}$` | — | no guest screen: the phone's home screen and the store listing | Required for `appleAppStore`; Apple enrols an organisation only with its D-U-N-S number. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: developer account `storeAccounts.accounts[].developerAccountId` | text field | yes | max length 64 | — | no guest screen: the phone's home screen and the store listing | Apple Team ID, or the Google Play developer account id. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: app identifier `storeAccounts.accounts[].appIdentifier` | text field | yes | max length 155; pattern `^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z0-9_]+)+$` | — | no guest screen: the phone's home screen and the store listing | The bundle id (Apple) or application id (Google) the app is signed with. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: aPI credential secret ref `storeAccounts.accounts[].apiCredentialSecretRef` | text field | no | Needed only for `submitToStore`. | — | no guest screen: the phone's home screen and the store listing | App Store Connect API key or Play service-account key, sent once and kept in the secret store; this is its reference. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Accounts: listing `storeAccounts.accounts[].listing` | group | no | — | — | no guest screen: the phone's home screen and the store listing | The store listing. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: app name `storeAccounts.accounts[].listing.appName` | text, one per language | no | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: subtitle `storeAccounts.accounts[].listing.subtitle` | text, one per language | no | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: description `storeAccounts.accounts[].listing.description` | text, one per language | no | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: keywords `storeAccounts.accounts[].listing.keywords` | text, one per language | no | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: category `storeAccounts.accounts[].listing.category` | text field | no | — | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: support URL `storeAccounts.accounts[].listing.supportUrl` | URL field | no | https:// | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: privacy policy URL `storeAccounts.accounts[].listing.privacyPolicyUrl` | URL field | no | https:// | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Listing: screenshot images `storeAccounts.accounts[].listing.screenshotAssetRefs` | media picker (several) | no | PNG, JPG, SVG or MP4 from the media library | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |

### App builds

Set on `CMS-104` App Build & Store Publishing through `requestAppBuild`. Reaches no guest screen: the phone's home screen and the store listing.

| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |
|---|---|---|---|---|---|---|---|
| Platform `appBuilds.platform` | segmented control | yes | Ios · Android | — | no guest screen: the phone's home screen and the store listing | — | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Config version `appBuilds.configVersion` | text field | no | — | — | no guest screen: the phone's home screen and the store listing | A published `ConfigVersion.version`. Absent builds the current one. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Release notes `appBuilds.releaseNotes` | text, one per language | no | English and Arabic (Arabic right to left) | — | no guest screen: the phone's home screen and the store listing | Keyed by ISO 639-1 code. Every enabled language should be present. | needs an app build (CMS-104) on the native apps; the website takes it on publish |
| Submit to store `appBuilds.submitToStore` | toggle | no | — | off | no guest screen: the phone's home screen and the store listing | Submit with the client's recorded API credential once built. False leaves the package for the client to upload. | needs an app build (CMS-104) on the native apps; the website takes it on publish |

## Each guest screen and what it takes from the configuration

Every guest screen takes the shell-wide parts (brand, theme, fonts, header, navigation, languages, modules, features). Listed here: what each takes beyond them.

| Screen | Takes |
|---|---|
| `GST-001` Home | Brand (2); Booking settings (tenant, with per-venue overrides) (1); Homepage sections (2); Availability and maintenance (14); Cookie banner (22) |
| `GST-002` Explore | Booking settings (tenant, with per-venue overrides) (5) |
| `GST-003` Buy Tickets | Navigation (1); Booking settings (tenant, with per-venue overrides) (5); Help me choose (19) |
| `GST-004` Item Detail | Booking settings (tenant, with per-venue overrides) (4) |
| `GST-005` What's On | the shell only |
| `GST-006` Item Detail – Event / Exhibition | the shell only |
| `GST-007` Select Date & Time | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `GST-008` Tickets & Add-ons | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16); Help me choose (19) |
| `GST-009` Review & Payment | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `GST-010` Booking Confirmation | the shell only |
| `GST-011` Wallet Overview | the shell only |
| `GST-012` My Tickets | the shell only |
| `GST-013` Ticket Details | Booking settings (tenant, with per-venue overrides) (2) |
| `GST-014` Ticket Transfer | the shell only |
| `GST-015` Memberships | the shell only |
| `GST-016` My Reservations | the shell only |
| `GST-017` Reservation Details | the shell only |
| `GST-018` Add to Calendar / Reminders | Footer (1) |
| `GST-019` Order History | the shell only |
| `GST-020` Saved Items / Wishlist | the shell only |
| `GST-021` Interactive Map | the shell only |
| `GST-022` Attraction Wait Times | the shell only |
| `GST-023` Virtual Queue | the shell only |
| `GST-024` F&B – Browse & Order | the shell only |
| `GST-025` F&B – Order Tracking | the shell only |
| `GST-026` Retail / Merchandise | the shell only |
| `GST-027` Parking – Reserve & Pay | the shell only |
| `GST-028` Parking – Reservation Confirmed | the shell only |
| `GST-029` Venue Info & Services | Availability and maintenance (14) |
| `GST-030` In-Venue Notifications | the shell only |
| `GST-031` AI Concierge – Home | Booking settings (tenant, with per-venue overrides) (2) |
| `GST-032` AI Concierge – Chat | the shell only |
| `GST-033` AI Concierge – Contextual Help | the shell only |
| `GST-034` Lost & Found | the shell only |
| `GST-035` Feedback & Ratings | the shell only |
| `GST-036` Loyalty & Rewards | the shell only |
| `GST-037` Offers & Promotions | the shell only |
| `GST-038` At the Venue | Availability and maintenance (14) |
| `GST-039` Profile | the shell only |
| `GST-040` Help & Support | Availability and maintenance (14) |
| `GST-041` Checkout Entry | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `GST-042` Simple Registration & OTP | Booking settings (tenant, with per-venue overrides) (2); Cookie banner (1) |
| `GST-043` Arabic / RTL Experience | the shell only |
| `GST-044` Multi-Currency & Pricing | the shell only |
| `GST-045` Ticket Delivery & Sharing | the shell only |
| `GST-046` Branded Queue / Waiting Room | the shell only |
| `GST-047` Maintenance / Upgrade Page | Availability and maintenance (14) |
| `GST-048` Upsell / Cross-Sell | the shell only |
| `GST-049` Interactive Seat Selection | Booking settings (tenant, with per-venue overrides) (3); Booking flows (1) |
| `GST-050` Resource Booking – Cabana | the shell only |
| `GST-051` Plan | Booking settings (tenant, with per-venue overrides) (2); Availability and maintenance (14) |
| `GST-052` Suggested Itineraries | the shell only |
| `GST-053` Your Plan | the shell only |
| `GST-054` AI Planner | the shell only |
| `GST-055` Dynamic QR Ticket | the shell only |
| `GST-056` Bundle Package | the shell only |
| `GST-057` Accessibility Information | Content pages (1) |
| `GST-058` Resource Availability (Cabana) | the shell only |
| `GST-059` Plan in Progress | the shell only |
| `GST-061` Menu Item Detail | the shell only |
| `GST-062` Shop & Drop Collection | the shell only |
| `GST-063` Explore – Search Results | Booking settings (tenant, with per-venue overrides) (2) |
| `GST-065` Newsletter & Preferences | the shell only |
| `GST-066` Privacy & My Data | Footer (1); Cookie banner (22) |
| `GST-067` Refunds & Resale | the shell only |
| `GST-068` Help & My Cases | the shell only |
| `GST-069` Face Pass | the shell only |
| `GST-070` Reserve a Table | the shell only |
| `GST-071` Payment Methods | the shell only |
| `GST-072` Share & Group Booking | the shell only |
| `GST-073` Security & Sign-in | the shell only |
| `GST-074` Map Booking — Cabanas & Spots | the shell only |
| `GST-075` Book a Space by the Hour | the shell only |
| `GST-076` Intercity Trip — Route & Schedule | the shell only |
| `GST-077` Intercity Trip — Route & Passengers | the shell only |
| `GST-078` Intercity Trip — Multi-trip Passes | the shell only |
| `GST-079` Intercity Trip — Favourite Routes | the shell only |
| `KSK-001` Attract Loop | the shell only |
| `KSK-002` Language Select | Availability and maintenance (14) |
| `KSK-003` What are you buying | the shell only |
| `KSK-004` Choose tickets | the shell only |
| `KSK-005` Choose a performance | the shell only |
| `KSK-006` Review | the shell only |
| `KSK-007` Payment | the shell only |
| `KSK-008` Payment unresolved | the shell only |
| `KSK-009` Ticket issued | the shell only |
| `KSK-010` Print failure | the shell only |
| `KSK-011` Collect a booking | the shell only |
| `KSK-012` Booking found | the shell only |
| `KSK-013` Call staff | the shell only |
| `KSK-014` Out of service | Availability and maintenance (14) |
| `KSK-015` Assistant | the shell only |
| `KSK-016` Order Food | the shell only |
| `KSK-017` Shop | the shell only |
| `WEB-001` Home / Landing | Booking settings (tenant, with per-venue overrides) (7); Homepage sections (2); Availability and maintenance (14); Cookie banner (22) |
| `WEB-002` Event & Attraction Listing | Booking settings (tenant, with per-venue overrides) (9); Help me choose (19) |
| `WEB-003` Search Results | Booking settings (tenant, with per-venue overrides) (2) |
| `WEB-004` Attraction Details | Booking settings (tenant, with per-venue overrides) (6) |
| `WEB-005` Ticket Type Selection | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16); Help me choose (19) |
| `WEB-006` Date & Performance Selection | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-007` Interactive Seat Selection | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-008` Add-ons & Upsell | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-009` Wishlist | the shell only |
| `WEB-010` Shopping Cart | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-011` Guest Details & Attendee Forms | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-012` Checkout — Payment | Booking settings (tenant, with per-venue overrides) (61); Booking flows (16) |
| `WEB-013` Booking Confirmation | the shell only |
| `WEB-014` Pay for a Booking | the shell only |
| `WEB-015` Branded Queue / Waiting Room | the shell only |
| `WEB-016` Login / Register | Booking settings (tenant, with per-venue overrides) (2); Cookie banner (1) |
| `WEB-017` My Account Dashboard | the shell only |
| `WEB-018` My Tickets | Footer (1) |
| `WEB-019` Order History | the shell only |
| `WEB-020` Profile & Preferences | the shell only |
| `WEB-021` Wallet & Gift Cards | the shell only |
| `WEB-022` Membership Plans | the shell only |
| `WEB-023` Membership Management | the shell only |
| `WEB-024` Devices, Wishlist & Consent | Cookie banner (22) |
| `WEB-025` Help Centre / FAQ | Availability and maintenance (14) |
| `WEB-026` Survey & Feedback | the shell only |
| `WEB-027` Newsletter Subscription | the shell only |
| `WEB-028` Contact & Venue Information | Availability and maintenance (1) |
| `WEB-029` Error / Sold Out / Maintenance | Availability and maintenance (14) |
| `WEB-030` Ticket Transfer | the shell only |
| `WEB-031` My Reservations | the shell only |
| `WEB-032` Offers & Promotions | the shell only |
| `WEB-033` Shop | the shell only |
| `WEB-034` Lost & Found | the shell only |
| `WEB-035` Multi-Currency & Pricing | the shell only |
| `WEB-036` F&B – Browse & Order | the shell only |
| `WEB-037` Menu Item Detail | the shell only |
| `WEB-038` F&B – Order Tracking | the shell only |
| `WEB-039` Venue Map & Wait Times | the shell only |
| `WEB-040` Virtual Queue | the shell only |
| `WEB-041` Parking – Reserve & Pay | the shell only |
| `WEB-042` Retail & Shop and Drop | the shell only |
| `WEB-043` Loyalty & Rewards | the shell only |
| `WEB-044` AI Concierge – Home | Booking settings (tenant, with per-venue overrides) (2) |
| `WEB-045` Help Centre & Accessibility | Availability and maintenance (14) |
| `WEB-046` In-Venue Notifications | the shell only |
| `WEB-047` Map Booking — Cabanas & Spots | the shell only |
| `WEB-048` Book a Space by the Hour | the shell only |
| `WEB-049` Transport — Route & Schedule | the shell only |
| `WEB-050` Plan Your Visit | Navigation (1); Modules shown to guests (1); Booking settings (tenant, with per-venue overrides) (2); Banners (1); Promo blocks (1); Availability and maintenance (14) |

## Decided on 2 October

- **No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; CHG-CSA-035).
- ***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 `powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036).
- **Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, scale, slide, blur or none, default rise): every customisation option of the approved wireframe (Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040).
- **Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template (`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).

## Never configurable

- A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035).
- Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel).
- Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502).
- A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## What the client said about white label

147 design inputs from the meetings and design reviews on branding and configurability (`handoff/design-inputs/mom-design-inputs.yaml`), newest first. They win over this map where the two disagree; an open question is built to its stated default.

- **Open question.** Should each popular-route card's starting fare, featured order and image or badge be set per route in the back office? Default built: routes carry a featured order and an image; the starting fare is computed from the lowest fare. *(open · Decisions Register 1 Oct 2026, Questions for the client — Transport / Popular routes card · DI-1119)* — WEB-049, GST-076, BO-1184
- **Open question.** Each group ticket card shows a minimum group size; is it set per group ticket, and what values? Default built: each group ticket carries its own minimum, default 10. *(open · Decisions Register 1 Oct 2026, Questions for the client — Group booking / Minimum group size · DI-1116)* — WEB-031, GST-072
- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)* — P02, P13/White Label
- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)* — P01, P02, CMS-103
- Products can be presented in multiple card layout styles: carousel, video poster, split, etc. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1089)* — P02
- The landing page offers selectable scroll animations (venue choice). *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1088)* — GST-001
- The home-screen navigation bar layout is configurable: home/explore/map/buy-tickets in different arrangements. *(agreed · MoM 30 Sep 2026, 4.5 Mobile App — Configuration Flexibility · DI-1087)* — P02, CMS-009
- Mobile app must not open straight into booking (client found it unclear). Tabs: Home · Explore · Plan · Tickets (Yas Island / Six Flags references), with a persistent "Buy tickets" button on every screen (raised centre button, or floating / flat per venue). *(agreed · design review 29 Sep 2026, Mobile app (v4) — Tabs Home · Explore · Plan · Tickets, persistent Buy tickets · DI-1081)* — P02
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)* — P01, P02
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)* — WEB-016, GST-073
- Existing booking settings stay: step indicator, extras step, seat picker, map view, quantities on add-ons (−/+ stepper, price multiplies), embed mode, hero banner, search in banner, single-event page. Defaults: search in banner off, seat picker = bowl. *(agreed · design review 29 Sep 2026, CFG-6 · Step indicator; Extras step; Seat picker; Map view; Quantities on add-ons; Embed mode; Hero banner; Search in banner; Single-event page · DI-1070)* — WEB-001, WEB-007, WEB-008, CMS-103
- The concierge (Sahli) shows as mascot art or as a plain button; setting "Concierge mascot", default on. *(agreed · design review 29 Sep 2026, CFG-5 · Sahli mascot (on/off) · DI-1069)* — WEB-044, GST-031
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)* — P01, P02, CMS-004
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)* — P01, P02, CMS-005
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)* — P01, P02, CMS-002, CMS-003, CMS-005
- A UI preset (L1–L6, or Custom) picks a bundle of booking-UI settings per venue type. *(agreed · design review 29 Sep 2026, CFG-1 · Preset (UI preset L1-L6, Custom) · DI-1065)* — WEB-001, CMS-103
- Booking-flow settings are set per tenant with a per-venue override; the CMS booking-flow settings screen must show tenant defaults and venue overrides. *(agreed · rev 3 design review 29 Sep 2026, CFG-11 · Where the settings live · DI-1063)* — CMS-103
- Swim ability is a consent question a venue attaches to a product or flow (e.g. "Are you able to swim?", "Do you hold a scuba certification?", "I accept the risk"), each with its own text and per-person or once-per- booking setting. Shown as a pop-up in the venue's theme after session/date; answers recorded. *(agreed · rev 3 design review 29 Sep 2026, REV3-26 · Built to match your examples: Swim question (water park) · DI-1062)* — WEB-006, GST-007
- On a guest's first booking visit, a four-step coach-mark tour highlights date, time, tickets and basket, with Back, Next / Done and End tour; a "Quick tour" button on the booking page replays it. Setting "Quick tour", default off; first-visit flag kept on the device only. *(agreed · rev 3 design review 29 Sep 2026, REV3-20 · 20. Enable or disable a Quick Tour that describes the customer journey · DI-1060)* — WEB-005, WEB-006, GST-007, CMS-103
- Multi-location attractions: the guest picks a location first (e.g. Al Barsha, Mirdif, Yas Island, Sharjah); a "Booking at" bar on later booking steps has Change location. On a switch, times and prices refresh and the selection is cleared unless the products share a family. Setting "Location switcher". *(agreed · rev 3 design review 29 Sep 2026, REV3-18 · 18. One tenant with an attraction in several locations; change location · DI-1058)* — WEB-001, WEB-005, WEB-006, GST-001, GST-007, GST-008, CMS-103
- Category tiles (e.g. Permanent exhibition, Temporary exhibitions, Guided tours, Courses & workshops), then that category's tickets with Adult / Child / Student counters. Setting "Ticket categories": Category → subcategory (default) or Flat list (all tickets under category headings). *(agreed · rev 3 design review 29 Sep 2026, REV3-16 · 16. Choose category, then subcategory, configurable in the CMS · DI-1056)* — WEB-002, WEB-005, GST-002, GST-003, CMS-103
- Cart & summary options: sidebar fixed right, sidebar left, slide-in right, slide-up bottom, floating cart icon (round basket button with item count opening the slide-in basket), single column. In Arabic the basket stays on the right by default (client confirmed); "Cart side in Arabic" can mirror to left. *(agreed · rev 3 design review 29 Sep 2026, REV3-10 · 10. Cart display: fixed on right, slide bar, icon, bottom; right for Arabic · DI-1051)* — WEB-005, WEB-006, WEB-008, WEB-010, GST-041, CMS-103
- Dining deposit hold is a venue option, off unless enabled in Venue Management; amount and basis (per guest, per table, percentage) are venue configuration, never a hard-coded AED 100. Show the deposit step only when enabled. *(agreed · rev 3 design review 29 Sep 2026, REV3-8b · 8. deposit hold flow · DI-1049)* — WEB-036, GST-070
- A time bar above the seat map shows the chosen performance, lets the guest switch show and has Change date; switching releases held seats. Setting "Time bar above seat map", default on. On the selection step, time sits directly under the date, above language & format and tickets. *(agreed · rev 3 design review 29 Sep 2026, REV3-6 · 6. Time selection on top, configurable · DI-1046)* — WEB-006, WEB-007, GST-049, CMS-103
- The 'view from your seat' box can sit Bottom (default), Right, Left or Top of the seat map (web only); on narrow screens and mobile it is always below the map. Setting "Seat view box". *(agreed · rev 3 design review 29 Sep 2026, REV3-5 · 5. CMS option to show the seat view right, left, top or bottom · DI-1045)* — WEB-007, GST-049, CMS-103
- Seated events with one on-sale performance go straight to the seat map (Flow 1). Otherwise date and time come first (Flow 2), either as an inline step (timed-ticket style, default) or as a pop-up dialog over the seat map. Setting "Date & time on seat events". *(agreed · rev 3 design review 29 Sep 2026, REV3-4 · 4. Flow 1 (fixed date and time) and Flow 2 (select date, then time, then seat map) · DI-1044)* — WEB-006, WEB-007, GST-007, GST-049, CMS-103
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)* — WEB-008, WEB-011, WEB-012, WEB-016, GST-041, GST-042, CMS-103
- Dated flows reveal in order: date, then time (hidden until a date is picked), then tickets (hidden until a time is picked), with a hint in place telling the guest what to pick next; Continue off until both chosen. Setting "Performance reveal": Date → time → ticket (default) or All at once. *(agreed · rev 3 design review 29 Sep 2026, REV3-2 · 2. Step 1 date, step 2 time (only after the date), step 3 ticket · DI-1042)* — WEB-005, WEB-006, GST-007, GST-008, CMS-103
- More than eight times show as compact time tiles, paged with Earlier / Later (Times per page 8/12/24/all, default 24), with day-part chips (All, Morning, Afternoon, Evening) showing counts (filter on by default). Day-part boundaries are venue settings, default before 12:00 / 12:00–17:00 / from 17:00. *(agreed · rev 3 design review 29 Sep 2026, REV3-1 · 1. Many performances should resize and page; filter by morning, afternoon, evening · DI-1041)* — WEB-006, GST-007, CMS-103
- Card layout is a choice, not free text: Stacked rows (default) · Split rows · Cards across · Poster cards. Card size: Compact (default) · Standard · Large · Extra large. Density: Compact (default) · Standard · Roomy. *(agreed · design review 29 Sep 2026, 6. Booking-flow configuration (CMS-016): card-layout options · DI-1040)* — WEB-002, WEB-005, GST-003, CMS-103
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)* — WEB-012, WEB-016, GST-041, GST-042
- The date list in the event banner (for multi-date events) is a setting, "Dates in event banner", off by default. The date picker always sits at the top of the booking step. *(agreed · design review 29 Sep 2026, Settings 19. Why is there a date selection in the header? · DI-1033)* — WEB-001, WEB-004, CMS-103
- Each Adult / Child / Senior / Infant row has an (i) button showing who the ticket is for and what it includes (up to 300 characters). Setting "Extra info on cards", default on. *(agreed · design review 29 Sep 2026, Tickets 6. Extra information for each ticket in the ticket section · DI-1028)* — WEB-005, GST-008, CMS-103
- Ticket cards, Read more and the listing side panel show tags (e.g. "2 Hours", "Min 1.10 m", "Free adult entry", "Valid 90 days", "Emirates ID"), each with a kind icon (clock, height, free, calendar, id), max 6. Venue-set tags win, else derived from duration, validity, height rule. Setting "Tags on tickets", default on. *(agreed · design review 29 Sep 2026, Tickets 3. 'Read more' should carry tags customisable per ticket type · DI-1025)* — WEB-004, WEB-005, GST-004, GST-008, GST-013, CMS-103
- Optional intro video on opening the app, with a "Skip introduction" control. *(agreed · MoM 29 Sep 2026, 2. Mobile app · DI-1020)* — P02, GST-001
- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)* — P13/White Label, CMS-102, P13, CMS-103
- Cleaning buffer is configurable. Option A: fixed buffer (e.g. 15 min) after every booking. Option B: N cleanings per day; the system places the buffers into the day's schedule and adjusts availability. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W10 Meeting-room cleaning buffer · DI-1012)* — BO-096, WEB-048, GST-075, CMS-103
- The "Category display" configuration control is retired and has no effect: remove it. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W7 Config: Category display · DI-1009)* — CMS-102, CMS-103
- Map-based cabana booking stays optional per configuration, since not every operator uses the same flow; it uses the same map back end as theme-park F&B/locations (reusable later for in-park navigation). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W6 Cabanas · DI-1008)* — WEB-047, GST-074, GST-050, GST-058, CMS-103
- Help me choose needs a configuration page per venue; AI may propose the question set from the product catalogue for the operator to validate and edit. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1006)* — CMS-101
- CMS option to list a product (e.g. training courses) with full details but no Book button; instead show "Contact sales to book" with contact details. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W3 View-only products · DI-1004)* — WEB-004, GST-004, WEB-002, CMS-102, WEB-005, GST-003, CMS-103
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)* — WEB-011, WEB-016, GST-041, GST-042, WEB-012, GST-009
- The CMS is a step-based site builder started from the workspace; a preset keeps the minimum path short (modules, booking flows, home sections and mobile tabs proposed), so an operator supplies only a logo, four colours and Publish; aim about 30 minutes to a working site. *(agreed · MoM 24 Sep 2026, M24-05 · DI-997)* — CMS-001, CMS-102
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)* — P01, CMS-102
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)* — P13/White Label, CMS-102
- Help me choose setup per venue: up to 2 questions, 3 answers each (title, one-line description, icon, optional badge e.g. "Best value"), each answer mapped to one booking flow, a result card (title, description, image) per recommendable product, and placement (button above products, pop-up on arrival, off). *(agreed · design review 23 Sep 2026, What the venue sets up in the CMS (per venue) · DI-984)* — CMS-101
- With the "Slide in right" cart setting, the summary is a tab on the right edge that slides in from the right (not a bar at the bottom). *(client request · design review 23 Sep 2026, Cart 13. Cart summary: 'Slide in right' shows at the bottom · DI-981)* — WEB-005, WEB-006, WEB-008, WEB-010
- Recommendations stay within business limits, e.g. at most three recommendations shown at checkout and never a product the customer already owns; AI recommendations never override hard business rules or eligibility constraints. *(agreed · MoM 21 Sep 2026, 4.3 Recommendation Strategy — Business Priority, Conflict Suppression & Fallback · DI-959)* — WEB-008, GST-048, BO-119
- Single-event mode page: banner or video hero, a brief description, and a date strip of the next seven days with a calendar for later dates. *(agreed · MoM 18 Sep 2026, M18-13 · DI-953)* — WEB-004
- The hero banner and marketing layer (images, video, search, browse-by-venue, venue info) is optional and toggled in the white-label builder: on for clients without their own marketing site (Qossai: roughly 30%), off for a lean direct-to-ticket flow. *(agreed · MoM 18 Sep 2026, 4.11 Guest Website UX Review — Page Structure & Hero Banner Flexibility · DI-945)* — WEB-001, CMS-102, CMS-007
- Per-element colours in the theme editor: pickers for the main call to action, pay button, add to cart, Buy tickets button, links and badges, each with a live contrast warning; left empty they follow the theme. The guest flow itself stays standard. *(agreed · MoM 17 Sep 2026, M17-11 · DI-922)* — CMS-005
- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)* — WEB-004, WEB-006, GST-007, CMS-016
- Qossai: white-labelling needs more flexibility, e.g. setting the colour of specific interactive elements such as the "pay now" / "purchase" button independently, not only an overall palette, while the guest experience stays a standardised flow with configurable limits. *(client request · MoM 17 Sep 2026, 4.14 Guest Web App — Live UI/UX Feedback Walkthrough · DI-918)* — CMS-002, CMS-005, CMS-006
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)* — P01, P13/White Label, CMS-002, CMS-003, CMS-005
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)* — P01, P02, CMS-005, CMS-006
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)* — P01, P02, CMS-005, CMS-101
- Role-based access controls who can discover, preview, download, edit, approve, share or manage assets. *(client request · MoM 11 Sep 2026, 4.3 Asset Governance, Rights, Approvals & Secure Sharing · DI-855)* — CMS-086
- Qossai asked if guests pick a specific table; Allam: table choice can be an option, but the default is the guest gives party size and the system/host allocates a table. *(agreed · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough (Dining) · DI-689)* — GST-070, EMP-052
- Two face credentials: Face Pass (long-term, renewable, for memberships/season passes) and Face Tag (short-lived, single day or event). Retention is venue-configurable per tier. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-640)* — GST-069, BO-186, BO-188, BO-192
- Three resale access models: (1) the client's own B2C site, where a guest requests resale within an admin-set price range (e.g. 10-20% below original); (2) a TICVAI-hosted white-label resale portal (e.g. museum.tickvai.com) for clients without B2C; (3) API for clients' own resale markets. *(agreed · MoM 1 Sep 2026, 4.14 Resale Marketplace - Detailed Follow-Up · DI-618)* — ADM-298, ADM-300, ADM-303, ADM-307, GST-067
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)* — CMS-025, CMS-026, P01
- Channel rules govern which actions each channel can perform (create, upgrade, cancel) and whether checkout is guest checkout (name, phone, email only) or full registration/sign-in. Customer category (corporate, travel agent/B2B, school) determines extra information collected. *(client request · MoM 1 Sep 2026, 4.11 Order & Reservation Management · DI-613)* — BO-308, BO-309, WEB-011, GST-041
- Apple/Google Wallet configuration covers template design (background colour, header, footer) and the guest-facing "Add to Apple Wallet" flow after an online purchase. *(client request · MoM 1 Sep 2026, 4.10 Media & Credentials (QR, RFID, NFC & Wallets) · DI-609)* — BO-347, BO-348, WEB-013, GST-010, GST-013
- Group ticket upgrades are business-configurable (off by default); where allowed a group raises an upgrade request (e.g. via chat/support) rather than self-serving like an individual. *(agreed · MoM 1 Sep 2026, 4.9 Clarified (group upgrades) · DI-607)* — GST-068, ADM-315, SUP-014
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)* — global
- Fees are separate from taxes: e.g. a call-center convenience fee, or a shipping fee varying by destination (Dubai, Abu Dhabi, Ras Al Khaimah, international) calculated from the checkout address; applied at transaction, item or ticket level. Checkout must show the fee once the address is entered. *(client request · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-597)* — ADM-071, ADM-072, WEB-012, GST-009
- Support both redirect to the gateway's hosted page and embedded/iframe capture (card, Apple Pay, Tabby) on the platform's own checkout preserving its look and feel, for Network International and Stripe; embedded needs extra security certification to reassure guests. *(agreed · MoM 31 Aug 2026, 4.13 Payment gateway approach · DI-589)* — WEB-012, GST-009
- **Open question.** Resale lets a guest resell a ticket through a secured channel with configurable commission and eligibility (e.g. minimum time before validity date, no expired tickets). Open: TICVAI-owned secure portal vs inside each client's own B2C site/app. *(open · MoM 31 Aug 2026, 4.12 Resale Marketplace · DI-584)* — ADM-279, ADM-283, GST-067
- Start/stop-sell per channel: e.g. a distant desert safari allows no same-day online booking (next day minimum), while onsite stays open to sell-out or a cutoff (e.g. 15 minutes before a timed show). Guest date/time pickers must reflect the channel's window. *(client request · MoM 31 Aug 2026, 4.11 Sales schedule & validity · DI-583)* — ADM-263, WEB-006, GST-007, KSK-005, POS-003
- Waiver is triggered automatically when an associated product is bought; timing is business-configurable: at checkout, post-purchase, or on-site before entry. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-573)* — CMS-046, CMS-047, WEB-011, GST-009
- Allam: no single standard waiver; a default/pre-set template can be offered, but the builder must stay fully configurable because each business has its own requirements. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-571)* — CMS-042, CMS-043
- Peer-to-peer transfer from one guest's wallet to another guest's wallet; a configurable venue-level toggle (allowed or not), not a default feature. *(agreed · MoM 27 Aug 2026, 4.10 Transfers, Fraud/Risk Controls · DI-536)* — BO-1144, BO-1145, GST-011, WEB-021
- Two variants: monetary gift card (value usable on anything the venue offers) and product-specific gift voucher (redeemable only for a named product, e.g. a dolphin-show voucher). Redemption channel is configurable: online, on-site or both. *(client request · MoM 27 Aug 2026, 4.9 Gift Cards, Vouchers & Wallet Payments · DI-533)* — BO-1124, BO-1126, BO-1127, WEB-021, GST-011
- Balance can move between linked family/group wallets in either direction (parent to child, child to parent); a venue-controlled toggle, not always enabled. *(agreed · MoM 27 Aug 2026, 4.8 Shared wallet transfer · DI-532)* — BO-1121, GST-011, WEB-021
- A parent's wallet funds linked child wristbands/wallets with per-child spending allowances, e.g. of a AED 500 family balance one child is capped at AED 200 and another at AED 200. *(agreed · MoM 27 Aug 2026, 4.8 Family, Parent-Child & Corporate Wallets · DI-529)* — BO-1116, BO-1117, GST-011, WEB-021
- Guests must be able to configure auto-reload and recurring funding schedules themselves in the guest web/app, not only venue admins in the back office. *(agreed · MoM 27 Aug 2026, 4.5 Funding / 5. Key Decisions · DI-519)* — GST-011, WEB-021
- Top-up rules set minimum and maximum amounts per transaction; channel/funding-source mapping restricts which payment methods each channel offers (e.g. cash top-up on-site only, not online), so each channel's top-up screen offers only its allowed methods. *(client request · MoM 27 Aug 2026, 4.5 Funding, Top-Up & Reload Management · DI-517)* — BO-1095, BO-1096, WEB-021, GST-011, P04, P05
- Ownership and access rules are configurable per wallet type. Family default: only the parent/guardian can top up; children can view balance and transactions and spend, but cannot top up unless permissions are explicitly reconfigured. Guest wallet screens must hide or disable top-up for members without the right. *(agreed · MoM 27 Aug 2026, 4.2 Wallet Ownership / 4.8 Family Permission Rules · DI-509)* — BO-1086, BO-1118, GST-011, WEB-021
- Wallet type library: multiple wallet types (guest, family, membership wallet), each assigned to a category (individual, corporate, member). Provisioning rules set the trigger that creates a wallet (membership purchase, first top-up); two patterns: gift-card style (pre-defined value products listed on the website) and open-ended "add money to wallet". *(client request · MoM 27 Aug 2026, 4.2 Wallet Type Library, Ownership & Account Association · DI-508)* — BO-1084, BO-1085, WEB-021, GST-011
- Decision (raised by Aishwarya): F&B and retail/merchandise online sale are optional back-office-enabled modules; where enabled, the whole purchase (browse, cart, checkout, pickup-at-venue or ship-to-guest) completes inside TICVAI — guests are never sent to download a separate app. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-505)* — WEB-036, WEB-033, WEB-042, GST-024, GST-026, GST-062
- Decision (Qossai, Ski Dubai): instructor choice is a per-ticket-type setting — private-session products may let the guest pick a specific instructor; group-session products auto-assign without showing a choice. Private and group are separate, separately priced products (a private request on a group instructor is its own product). *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-504)* — BO-897, BO-899, WEB-005, GST-008
- Resources are one-to-one (dedicated to a booking) or shared (e.g. a meeting room with bookable pods, a vehicle across sequential slots); further sales are blocked once a shared resource's capacity/slot is full and reopened if a booking is cancelled. *(client request · MoM 26 Aug 2026, 4.7 Dynamic Resource Assignment for Experience Tickets · DI-496)* — BO-900, BO-855, WEB-048, GST-075
- Donation campaigns: fixed or variable amounts, enabled per sales channel, triggered on a specific product or across all products, proceeds tracked to a separate account code. *(client request · MoM 25 Aug 2026, 4.9 Bundles, Add-Ons, Donations & Policies · DI-471)* — BO-1190, WEB-012, GST-009, POS-005
- Membership lifecycle: upgrade, downgrade, suspend (freezes validity until re-enabled), deactivate and cancel, with configurable timing windows (e.g. upgrade allowed only in the final two months before expiry). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-467)* — BO-298, BO-299, GST-015, WEB-023
- Quantity/purchase limits can be set per order, per guest, per account category and per sales channel (e.g. maximum 6 tickets per transaction). *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-464)* — BO-008, WEB-005, GST-008, POS-002, KSK-004
- Eligibility rules are configurable: residency/nationality/geography (e.g. UAE-resident-only with Emirates ID capture), minimum age (date-of-birth check), guest-profile category (e.g. VIP-only) and minimum loyalty points/spend for a membership tier. *(client request · MoM 25 Aug 2026, 4.8 Eligibility Rules, Special Products & Memberships · DI-463)* — ADM-199, BO-008, WEB-011
- Referral rewards may be credited as currency/points directly into the guest's wallet (like Swiggy), in addition to discount vouchers — a business-configurable option. *(agreed · MoM 25 Aug 2026, 4.7 Entitlements & Access Control; 5. Key Decisions · DI-460)* — BO-830, GST-011, WEB-021
- Weekday/calendar rules give different validity and pricing to weekday-only vs. all-days products (e.g. Global Village). Blockout dates exclude some ticket types (e.g. memberships) on public holidays/special days, requiring a separate ticket for those dates. *(client request · MoM 25 Aug 2026, 4.5 Validity Management & Expiry Rules · DI-452)* — BO-019, BO-008, WEB-006, GST-007
- Time-slot (performance) tickets configure early/late entry and an entry window (e.g. from 30 minutes before start until a cut-off). Multi-day tickets are consecutive-day or flexible within a range (e.g. any 3 days within a month). *(client request · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive · DI-447)* — BO-008, BO-016, WEB-006, GST-007
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)* — BO-008, GST-013, GST-017, WEB-018
- Ticket attributes such as minimum age, ID-proof requirements (e.g. Emirates ID for UAE-resident tickets, with format validation or photo upload; passport; handicap/PoD documentation) or an embedded ID-reader for on-site verification are configurable per ticket and region, not fixed. *(agreed · MoM 25 Aug 2026, 4.2 Ticket Configuration Reference; 5. Key Decisions · DI-443)* — BO-008, WEB-011, P02/Cart & Checkout, POS-002
- Supporting configuration: ticket variants (adult/child/senior/VIP, configurable), waitlist, on-sale/off-sale timing and cut-offs, entitlement/access rules (single/multi-venue, entries, zones, early entry), fulfilment channels (email, WhatsApp, SMS), after-sales windows (upgrade, reschedule, cancel), dynamic/fixed pricing and promotions. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-437)* — BO-008, BO-158, GST-045
- Packages bundle any combination of ticket-type components with package-level pricing (e.g. admission + F&B item + retail item, or admission + show); F&B or retail is not required. *(client request · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough · DI-435)* — BO-011, GST-056, WEB-005
- Guest information capture (name, mobile number, nationality, visit survey, etc.) is configurable per ticket type; even an open-dated admission ticket can optionally collect it. *(agreed · MoM 24 Aug 2026, 4.5 Ticketing Configuration Walkthrough; 5. Key Decisions · DI-434)* — BO-008, WEB-011, P02/Cart & Checkout, POS-002
- Decision (raised by Qossai): the CMS/website builder supports two modes per client using the same builder — a full landing page plus integrated ticket-sale flow (clients without a website), or B2C-only (header, product cards, footer, checkout) embedded in/linked from an existing site. *(agreed · MoM 21 Aug 2026, 4.9 Website Builder Flexibility — Standalone vs. B2C-Only Configuration · DI-431)* — CMS-102, CMS-103, CMS-007, BO-837
- Decision: the add-ons step is optional/removable in configuration for products with no add-ons, collapsing the flow to Ticket Selection → Cart → Checkout. *(agreed · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review; 5. Key Decisions · DI-428)* — WEB-008, GST-008, GST-048, CMS-103
- Product cards/pages carry short descriptions with an expandable "view more details" control and a configurable hero image or video per product. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-425)* — WEB-004, WEB-005, GST-004, GST-008, BO-839
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)* — CMS-009, P01
- Decision: seats held in a cart auto-release after a configurable timeout if checkout is abandoned, and immediately if a payment attempt fails. *(agreed · MoM 21 Aug 2026, 4.6 Seat Inventory Status; 5. Key Decisions · DI-422)* — BO-998, BO-1008, WEB-007, GST-049, WEB-012, GST-009
- Decision: seating rules — consecutive-seat enforcement (no single empty seat left between bookings), social-distancing buffer (auto-block adjacent seats), seat-kill rule, company/held-seat rule — are configurable per venue/event, defaulting to the venue's operational policy. *(agreed · MoM 21 Aug 2026, 4.3 Best-Seat Logic, Seating Rules; 5. Key Decisions · DI-416)* — BO-1013, BO-1014, BO-1015, BO-1021, WEB-007, GST-049
- Decision: three seat-selection models, selectable per section, per event: (1) zone/capacity selling with no seat numbers (guest told zone only); (2) system-assigned "best available" — guest picks section + quantity, seats disclosed later; (3) full customer seat selection. *(agreed · MoM 21 Aug 2026, 4.1 Reference Walkthrough; 4.2 Seat Map Builder; 5. Key Decisions · DI-410)* — WEB-007, GST-049, POS-004, BO-705, BO-994, BO-995
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)* — P01, CMS-009, CMS-103
- Drag-and-drop page builder with a standardised layout (header, footer, hero/card components) that adapts to product type — seat map for seated products, standard flow for general admission. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-394)* — CMS-007, BO-837, WEB-007, GST-049
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)* — CMS-002, CMS-003, CMS-005, CMS-016, BO-835
- Surveys trigger at configurable points: post-purchase, post-visit, post-ticket-scan, membership renewal and case closure. *(client request · MoM 20 Aug 2026, 4.9 Surveys & Gamification · DI-391)* — BO-816, GST-035, WEB-026
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)* — BO-054, P08, P12, P13, P16
- **Open question.** Loyalty accrues points by product/spend tier (e.g. bronze/silver/gold thresholds) and unlocks tier benefits (e.g. platinum-tier discounts on F&B and ticketing). Full programme configuration (tiers, points, redemption, expiry) pending a dedicated session. *(open · MoM 20 Aug 2026, 4.5 Loyalty, Membership & Wallet · DI-382)* — GST-036, WEB-043, BO-758
- Consent policy governs marketing/newsletter/survey communications; customers who do not opt in must not receive promotional communications. *(client request · MoM 20 Aug 2026, 4.3 Consent, Data Privacy & Retention · DI-378)* — BO-747, GST-065, WEB-027
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)* — BO-736, WEB-016, WEB-011, GST-042
- Online retail offers buy-online-pickup-in-store and buy-online-ship-to-address. Shipping fees are set by region/city (e.g. Dubai, Abu Dhabi, international); decision: operations enter courier rates and margins manually, no live courier-API integration at this stage. *(agreed · MoM 19 Aug 2026, 4.3 Pricing, Bundles & Promotions; 4.8 Online Order Fulfilment & Shipping Configuration · DI-359)* — WEB-042, GST-062, BO-143
- Parking is barrier integration, not space counting: one configuration screen chooses a model - no integration (TICVAI QR checked by security), ANPR (guest enters a plate at checkout, pushed to the barrier whitelist) or QR handoff to the barrier. Pay-per-hour parking is out of scope. *(agreed · MoM 14 Aug 2026, 10 · DI-316)* — BO-006, WEB-041, GST-027
- Kiosks are guest-facing: white-labelled to the client's branding like the guest website, while keeping a kiosk-specific layout. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-298)* — P05
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)* — global
- Group bookings: one shared QR for the whole group (redeemed together at the counter) or one QR per person, each of which the guest can link to their own profile in the mobile app. *(agreed · MoM 14 Aug 2026, 6. Food & Beverage — Ordering, Delivery, and Redemption · DI-289)* — GST-012, GST-072, POS-002, BO-026
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)* — P13/White Label, CMS-009, CMS-016
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)* — P01, P02, P13/White Label
- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)* — CMS-017, ADM-017
- Support chat is native to TICVAI: a built-in AI chat assistant answers first, then escalates to a human "CR representative" role in the platform; offered white-labelled as a subscription add-on for smaller clients. *(agreed · MoM 12 Aug 2026, 10. Customer Support / Chat Integration Approach · DI-256)* — GST-040, GST-068, WEB-025, SUP-004, SUP-005
- **Open question.** Open: publishing model — each client's own App/Play Store listing vs one universal TICVAI app where the user selects the venue; and a client module with customisation screens plus a CI/CD-linked publish action vs a canvas the client exports and publishes. Softlabs to present pros/cons. *(open · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-251)* — CMS-104, P02
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)* — P01, P02, CMS-104
- Branded virtual waiting room activates automatically above a configurable concurrent-buyer threshold (e.g. 500) during high-demand on-sales, shows a wait time, and follows the tenant's app theme. *(client request · MoM 10 Aug 2026, 4.8 Checkout Extras — Delivery, Waiting Room, Upsell/Cross-Sell, Seating, Resources · DI-214)* — GST-046, WEB-015
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)* — P13/White Label, CMS-016
- Layout builder: header, footer, logo, bottom-navigation icons and colours are configurable; banner sizing is configurable and promotion blocks are switched on/off by toggle. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-189)* — CMS-005, CMS-008, CMS-009
- Font and image upload guardrails: size/format restrictions and pixel limits (e.g. banner image ≤ 1024px), validated on upload with an explanatory note to the tenant admin, so cursive/bold fonts cannot overflow banners or descriptions. *(agreed · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-188)* — CMS-003, CMS-004, CMS-010
- Guest-app builder: tenant uploads client logo (multiple formats), picks colour themes, app icon and custom font, with a live preview before publishing. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-187)* — CMS-002, CMS-003, CMS-004, CMS-005, CMS-006
- Ticket PDF carries a live QR code, a unique ticket number/barcode (media identifier), customisable branding/layout, terms and conditions and guest name; screens must distinguish ticket ID (one per ticket) from media code (can cover several tickets scanned as one group). *(agreed · MoM 7 Aug 2026, 20. Live Point-of-Sale Transaction Walkthrough · DI-180)* — BO-346, BO-345, GST-013
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)* — global
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)* — P01, P13/White Label
- **Open question.** Two selection patterns: (a) event, date, time, see availability, then product; (b) product, quantity, date, then only time slots with enough capacity. How many customization scenarios to support needs deeper UI exploration. *(open · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-118)* — P01/Booking & Selection, P02/Booking & Selection
- Some clients (e.g. museums with 5-6 standard configurations) start by asking the number of guests, which narrows the calendar to dates/times with sufficient availability. *(client request · MoM 3 Aug 2026, 8. Ticket Flow Variations by Product Type · DI-117)* — WEB-006, GST-007, WEB-005, GST-008
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)* — CMS-007, BO-837, P13
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)* — P13
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)* — P01, P13/White Label
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)* — P01, BO-835, CMS-016
- Ticket listings are data-driven: creating a new ticket automatically surfaces it on the relevant site according to its category configuration. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-109)* — WEB-001, WEB-002, BO-839
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)* — P01, P13/White Label
- The POS/tablet application carries TICVAI's own branding and UI direction; the B2C and B2B mobile applications are white-label by design. *(agreed · MoM 31 Jul 2026, 15. Monday UI/UX Session Planning · DI-084)* — P04, P02, P10
- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)* — ADM-018, CMS-011
- Qossai: the target product is a white-label application supporting both B2C and B2B mobile use cases, built around three to four distinct flows (e.g. admission ticket flow, seat assignment flow). *(client request · MoM 31 Jul 2026, 4. Application Flow & White-Label Requirements · DI-056)* — P02, P10
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)* — global
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)* — P04, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)* — P04, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)* — P04, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)* — global
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)* — global
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)* — global
- Virtual waiting room page: branded with the customer's venue logo, shows estimated waiting time and progress indicators, admits customers at controlled intervals. Configured independently per customer and venue. *(agreed · MoM 28 Jul 2026, 19. Auto-scaling and Virtual Waiting Room · DI-016)* — WEB-015, GST-046

## Sources

- `contracts/satellite/white-label.yaml`: TenantConfig and every `set*` operation; `marketing-crm.yaml` for SEO and the cookie banner.
- `screens/P13-white-label-cms.yaml`, `screens/P09-platform-admin-console.yaml`: where each is set.
- `screens/P01-guest-web-storefront.yaml`, `P02-guest-mobile-app.yaml`, `P05-guest-kiosk.yaml`: where each is read.
- `screens/_design-tokens.yaml` `whiteLabel`: which tokens a tenant may override.
- `flows/F22`, `F102`, `F103`; ADR-0006 (tiered app distribution), ADR-0018 (configuration scope).
- `handoff/design-inputs/white-label-map.json`: this map as data.
