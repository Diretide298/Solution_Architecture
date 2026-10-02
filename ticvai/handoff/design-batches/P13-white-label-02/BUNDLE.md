# P13-white-label-02 — P13 · White Label (2 of 3)

**10 screens · 40 operations · 64 schemas · 10 permissions**

Platform P13 Venue CMS · ships as **venue-management** ·
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

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_USE, GUEST_MANAGE, GUEST_VIEW, MARKETING_MANAGE, PRODUCT_VIEW, ROLE_MANAGE, SCOPE_VIEW, TENANT_CONFIGURE, TENANT_PUBLISH, USER_MANAGE`. A control nobody can use must say so,
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

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `CMS-013` | SEO & Metadata | A | 28 | 0 | 5 | 12 | 0 | 0 | configures | notStarted (generated) |
| `CMS-011` | Translations | A | 4 | 0 | 5 | 5 | 2 | 0 | configures | notStarted (generated) |
| `CMS-012` | RTL Preview | A | 0 | 15 | 5 | 5 | 0 | 0 | — | notStarted (generated) |
| `CMS-014` | Publishing Workflow | A | 2 | 12 | 5 | 1 | 2 | 6 | — | notStarted (generated) |
| `CMS-015` | Version History | A | 0 | 18 | 6 | 3 | 0 | 0 | — | notStarted (generated) |
| `CMS-016` | Site Settings | A | 62 | 46 | 6 | 11 | 3 | 6 | configures | notStarted (generated) |
| `CMS-017` | Domain & Certificate | A | 3 | 18 | 6 | 0 | 1 | 0 | configures | notStarted (generated) |
| `CMS-018` | Consent & Legal | A | 25 | 51 | 6 | 4 | 2 | 4 | configures | notStarted (generated) |
| `CMS-019` | User Access | A | 2 | 27 | 6 | 0 | 0 | 0 | — | notStarted (generated) |
| `CMS-101` | Help Me Choose | A | 28 | 18 | 6 | 3 | 4 | 0 | configures | notStarted (generated) |

## Thin screens in this batch

**CMS-011, CMS-012 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-013` SEO & Metadata

**Control how a page looks everywhere it is not the page.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18194 (APP-WL-CMS-013) |
| Who uses it | venue staff holding `MARKETING_MANAGE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setSeoMetadata`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/seo-metadata` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| id | picker: choose an id (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `SeoMetadata.id` |
| entityKind | select | optional | — | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — | `SeoMetadata.entityKind` |
| entityId | picker: choose an entity (drawn as a picker, not a text box) | optional | — | — | shows names, sends the id | — | `SeoMetadata.entityId` |
| locale | text field | optional | — | — | — | — | `SeoMetadata.locale` |
| title | text field | optional | — | — | — | — | `SeoMetadata.title` |
| metaDescription | text field | optional | — | — | — | — | `SeoMetadata.metaDescription` |
| keywords | list of values (chips) | optional | — | — | — | — | `SeoMetadata.keywords` |
| canonicalUrl | text field | optional | — | — | — | — | `SeoMetadata.canonicalUrl` |
| slug | text field | optional | — | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. | `SeoMetadata.slug` |
| hreflang | key and value settings | optional | — | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. | `SeoMetadata.hreflang` |
| schemaOrgType | text field | optional | — | — | — | — | `SeoMetadata.schemaOrgType` |
| openGraph | key and value settings | optional | — | — | — | — | `SeoMetadata.openGraph` |
| isAutoGenerated | toggle | optional | on | — | — | 22.11.2. Generated by default and overridable. | `SeoMetadata.isAutoGenerated` |
| noIndex | toggle | optional | off | — | — | — | `SeoMetadata.noIndex` |
| scopePath | text field | optional | — | — | — | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — 49 tables were in that state, so a row could be written at … | `SeoMetadata.scopePath` |

**Sent by *Save SEO metadata*** (`setSeoMetadata`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entity kind `entityKind` | select | required | — | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — | `setSeoMetadata` body |
| Entity `entityId` | picker: choose an entity | required | — | — | shows names, sends the id | — | `setSeoMetadata` body |
| Locale `locale` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Title `title` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Meta description `metaDescription` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Keywords `keywords` | list of values (chips) | optional | — | — | — | — | `setSeoMetadata` body |
| Canonical URL `canonicalUrl` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Slug `slug` | text field | optional | — | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. | `setSeoMetadata` body |
| Hreflang `hreflang` | key and value settings | optional | — | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. | `setSeoMetadata` body |
| Schema org type `schemaOrgType` | text field | optional | — | — | — | — | `setSeoMetadata` body |
| Open graph `openGraph` | key and value settings | optional | — | — | — | — | `setSeoMetadata` body |
| Is auto generated `isAutoGenerated` | toggle | optional | on | — | — | 22.11.2. Generated by default and overridable. | `setSeoMetadata` body |
| No index `noIndex` | toggle | optional | off | — | — | — | `setSeoMetadata` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save SEO metadata (primary button) | `setSeoMetadata` PUT `/seo-metadata` | SeoMetadata | SeoMetadata | — | — |

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | Not found — it may have been deleted or moved out of scope |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `MARKETING_MANAGE`, which `setSeoMetadata` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `setSeoMetadata` → `MARKETING_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `MARKETING_MANAGE`, which `setSeoMetadata` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

12 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.11.1 | SEO Metadata Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.2 | Dynamic SEO Generation | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.3 | AI SEO Optimization | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.4 | Sitemap Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.5 | Schema Markup Support | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.6 | SEO-Friendly URL Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.7 | Redirect Management | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.8 | SEO Content Analysis | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.9 | Internal Linking Recommendations | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.10 | SEO Analytics Dashboard | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.11 | Multi-Language SEO | Marketing & CRM | CONTRACTED | data `SeoMetadata` |
| 22.11.12 | SEO Audit & Compliance | Marketing & CRM | CONTRACTED | data `SeoMetadata` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Entity kind (`seo.entityKind`) | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | every website screen | — |
| Entity (`seo.entityId`) | shows names, sends the id | — | every website screen | — |
| Locale (`seo.locale`) | — | — | GST-031, GST-073, WEB-011, WEB-017, WEB-024, WEB-027, WEB-044 | — |
| SEO metadata title (`seo.title`) | — | — | every website screen | — |
| Meta description (`seo.metaDescription`) | — | — | every website screen | — |
| Keywords (`seo.keywords`) | — | — | every website screen | — |
| Canonical URL (`seo.canonicalUrl`) | — | — | every website screen | — |
| Slug (`seo.slug`) | — | — | every website screen | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | — | — | every website screen | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | — | — | every website screen | — |
| Open graph (`seo.openGraph`) | — | — | every website screen | — |
| Is auto generated (`seo.isAutoGenerated`) | — | on | every website screen | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | — | off | every website screen | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-013` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-013?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save SEO metadata.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `MARKETING_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-011` Translations

**Fill in what every language is missing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18106 (APP-WL-CMS-011) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the screen declares only writes (`setLanguages`) and no read of a population — it is settings, not a list |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/translations` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Languages | multi select | — | — | — | — | Required. | — |
| Default language | text field | — | — | — | — | Required. | — |

**Sent by *Save languages*** (`setLanguages`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Languages `languages` | list of values (chips) | required | — | at least 1 | — | — | `setLanguages` body |
| Default language `defaultLanguage` | language picker | required | — | — | ISO 639-1 code, shown as the language name | — | `setLanguages` body |

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save languages (primary button) | `setLanguages` PUT `/tenant-config/languages` | inline | LanguageConfig | 400 Default is not among the enabled languages | — |

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The saved translations. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the translations untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No translations configured. The form opens empty and `setLanguages` saves the first one; it says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `setLanguages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Default is not among the enabled languages |

#### Permissions

- `setLanguages` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `setLanguages` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.4.1 | The system should support multiple languages for the Ticketing POS, Self-Service Kiosks, websites mobile app and backend . | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.7.35 | The system should support: - Multilingual with language to be chosen by B2B client. Languages to include at a minimum Arabic and English. - Use of base system currency and all transactions performed … | Ticketing Sales | CONTRACTED | `setLanguages` |
| 2.16.12 | The system should allow usage of English and Arabic language on the ticket templates. | Ticketing Sales | CONTRACTED | `setLanguages` |
| 22.8.21 | Multi-Language Support | Marketing & CRM | CONTRACTED | `setLanguages` |
| 22.10.13 | Multi-Language Content Management | Marketing & CRM | CONTRACTED | `setLanguages` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- A new language is added as a configuration change, not development. Qossai wants a table-driven workflow like his prior project: a translation spreadsheet with a column per language reviewed by native speakers, then fed back through an AI translation pass. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-083)*
- Translation workflow: text entered in English, machine-translated, then reviewed and validated by the tenant's own team in the back office/CMS before publishing; applies to website, POS and mobile app. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-081)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Languages (`languages.languages`) | at least 1 | — | every guest screen (web, app and kiosk) | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | ISO 639-1 code, shown as the language name | — | every guest screen (web, app and kiosk) | the language a first visit opens in |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-011` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-011?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save languages.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-012` RTL Preview

**See the site as an Arabic reader sees it.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18107 (APP-WL-CMS-012) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/rtl-preview` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Version | text field | — | — | `getTenantConfig` ?version |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**The tenant config** (detail panel, from `getTenantConfig`)

| Shows | Format | Notes |
|---|---|---|
| Is draft | yes / no (icon or chip) | True for the working draft, which is the only row. |
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
| App icons | grouped details | — |
| Theme | grouped details | — |
| Fonts | grouped details | — |
| Footer | grouped details | BL-002. `setHeader` and `HeaderConfig` exist and the footer does not, which looked like symmetry until you notice it is not: a header is … |
| Notification branding | grouped details | BL-003. `marketing-crm` holds the templates and nothing said whose identity they wear. |
| Enabled payment methods | list or chips (count when long) | BL-004. `FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts. |
| Accessibility | grouped details | BL-065, 2.1.27. POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated. |
| Header | grouped details | — |
| Navigation | grouped details | The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6). |
| Homepage | grouped details | — |
| Modules | list or chips (count when long) | — |
| Features | list or chips (count when long) | — |
| Languages | grouped details | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Validate tenant config (primary button) | `validateTenantConfig` POST `/tenant-config/validate` | — | ConfigValidationReport | — | — |

**Data it reads**: `getTenantConfig` (onLoad, Full working configuration)

**Where the user goes next**

- → `CMS-014` Publishing Workflow: *Publishes*
- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rtl preview, read by `getTenantConfig`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rtl preview untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rtl preview yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getTenantConfig` → `TENANT_CONFIGURE` (configure) · staff, guest
- `validateTenantConfig` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.19 | Tenant-Specific Branding - System shall support tenant-specific branding. | Guest Mobile App & Branding | CONTRACTED | `getTenantConfig` |
| 22.10.1 | Multi-Site CMS | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 22.10.3 | Multi-Brand Management | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 19.1.21 | Tenant-Specific Notifications - System shall support tenant-specific notifications. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |
| 19.1.23 | Tenant-Specific Payment Methods - System shall support tenant-specific payment methods. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-012` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 4: Previews in both directions → **Arabic is a mirror, not a translation** — the preview must show it
- Flow F22 branch at step 4 (recoverable): when Arabic layout breaks with the new logo, A wide logo that fits left-aligned may not fit mirrored. **This is why the preview toggles direction**, and it is the defect that reaches production without one.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403, 404).
- [ ] Every output is drawn (15 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-012?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Validate tenant config.
- [ ] Every transition is wired: `CMS-014`, `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-014` Publishing Workflow

**Move a change from draft to live, with someone accountable (Site Builder step 7).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18120 (APP-WL-CMS-014) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantAppStatus` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | `venueId` (session) |
| Route | `/white-label/publishing-workflow` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **A rollback arrives here as a draft (decided 28 September, audit R139 (b)).** Version History (CMS-015) restores an old version into the working draft with `restoreConfigVersion` and reviews it with `diffConfigVersion`; only this screen's `publishTenantConfig` puts it live, with a note. A rollback is never one click.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Flow type key | select | — | Dated day pass · Timed entry · Open dated · Seated fixed performance · Seated date time seat map · Experience workshop · Surf session · Meeting room hourly · Cabana map · Cabana by size · Guided tour by language · Transport … | `listBookingFlows` ?flowTypeKey |

**Form: Publish tenant config** (modal, opened by *Publish tenant config*; *Publish tenant config* calls `publishTenantConfig`, *Cancel* sends nothing)

**Collects what `publishTenantConfig` sends before it is called.** Required: `note`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Note `note` | text area | required | — | min length 3; max length 500 | — | — | `publishTenantConfig` body |
| Scheduled for `scheduledFor` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | Publish at a future time. Useful for a campaign launch. | `publishTenantConfig` body |

Errors to draw in the form: 409 Validation failed. (ConfigValidationProblem)

#### Outputs: what the screen shows and produces

**Shown**

**The tenant app status** (detail panel, from `getTenantAppStatus`)

| Shows | Format | Notes |
|---|---|---|
| Is published | yes / no (icon or chip) | True once any version has been published. |
| Published version | text | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Draft version | text | Staff only. |
| Has unpublished changes | yes / no (icon or chip) | Staff only. The working draft differs from the current version's `snapshot`. |
| Active module count | 1,234 | Staff only. `ModuleEnablement` rows with `isEnabled` true. |
| Licensed module count | 1,234 | Staff only. `ModuleEnablement` rows with `isLicensed` true. |
| Active page count | 1,234 | Staff only. Content pages that are `published` and enabled. |
| Is in maintenance | yes / no (icon or chip) | — |
| Maintenance message | in the reader's language | — |
| Expected back at | 1 Oct 2026, 14:30 | — |
| Recent changes | list or chips (count when long) | Staff only. Names the principal behind each change, so it never reaches a public response. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (publish gate) | navigation or local | — | — | — | — |
| Publish tenant config (primary button) | `publishTenantConfig` POST `/tenant-config/publish` | inline | ConfigVersion | 409 Validation failed. (ConfigValidationProblem) | opens modal first |
| Validate tenant config (secondary button) | `validateTenantConfig` POST `/tenant-config/validate` | — | ConfigValidationReport | — | — |
| What publishing changes (publish gate) | navigation or local | — | — | — | — |

**Data it reads**: `getTenantAppStatus` (onLoad, App status and recent changes); `listBookingFlows` (onLoad, The venue's flows and whether each is valid, for the gate …)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `version`
- → `CMS-103` Booking Flows: *Fix a booking flow*; carries `bookingFlowId`
- → `CMS-104` App Build & Store Publishing: *Build the mobile app*
- → `CMS-102` Site Builder: *Back to the Site Builder*
- → `CMS-015` Version History: *Rolls back when something is wrong*; carries `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The publishing workflow, read by `getTenantAppStatus`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the publishing workflow untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No publishing workflow yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_PUBLISH`, which `publishTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Validation failed. (ConfigValidationProblem) |

#### Permissions

- `publishTenantConfig` → `TENANT_PUBLISH` (configure) · staff
- `validateTenantConfig` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantAppStatus` → no permission · device, guest
- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_PUBLISH`, which `publishTenantConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.24 | White Label Configuration Portal - System shall provide self-service white label configuration. | Guest Mobile App & Branding | CONTRACTED | `publishTenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Each client owns its Apple and Google developer accounts; the app is built in the CMS from a published configuration, with an in-platform guide (D-U-N-S number, opening accounts, store listing, store review). *(agreed · MoM 24 Sep 2026, M24-08 · DI-998)*
- The builder flow ends in a Review & Publish step before configuration goes live. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-194)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-014` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 5: Publishes → Live on web immediately; the app picks it up on next launch
- Flow F22 *A tenant rebrands their app*, step 7: Publishes the restored draft → The previous brand is live again, through the same publish gate as any other change
- Flow F22 branch at step 5 (recoverable): when Published mid-transaction, A guest partway through checkout keeps the config version they started with. **A rebrand must not change a price or a layout under someone mid-purchase.**
- Flow F22 branch at step 5 (requiresStaff): when The app store build is older than the config, Config is data and the shell is a release. **Anything needing a new shell does not publish** — an app icon change is a store submission, not a config change (ADR-0006).

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403, 409).
- [ ] Every output is drawn (12 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-014?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Publish tenant config, Validate tenant config, What publishing changes.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-103`, `CMS-104`, `CMS-102`, `CMS-015`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-015` Version History

**See who changed what and go back if it was wrong — by restoring into the draft, reviewing, then publishing.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18121 (APP-WL-CMS-015) |
| Who uses it | venue staff holding `TENANT_CONFIGURE`, `TENANT_PUBLISH` (2 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listConfigVersions` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `version` (deepLink) · cold entry: **A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is … |
| Route | `/white-label/version-history` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Absorbed CMS-020 on 28 September (audit R276)**: the Change Log listed the same `listConfigVersions` rows (who published what, when, with which note) and nothing else, so it brought no operation; its entry from the Tenant Workspace (CMS-001) now lands here. **Rollback is restore, then review, then publish — never one click (decided 28 September, audit R139 (b)).** **Restore config version** calls `restoreConfigVersion`, which copies the chosen version into the working draft and publishes nothing. The screen then shows **Diff config version** of the live version against the restored draft (`diffConfigVersion`) as the review, and **Review and publish the restored draft** goes to the Publishing Workflow (CMS-014), where `publishTenantConfig` puts it live with a note.

#### Inputs: what the user enters or picks

**Form: Restore config version** (confirmDialog, opened by *Restore config version*; *Restore into draft* calls `restoreConfigVersion`, *Cancel* sends nothing)

**Restores the chosen version into the working draft and publishes nothing** (decided 28 September, audit R139 (b)). Names the version and says that any unpublished changes in the draft are replaced. Guests keep seeing the live version until the restored draft is reviewed (`diffConfigVersion`) and published on CMS-014.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every config version** (data table, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected config version** (detail panel, from `listConfigVersions`)

| Shows | Format | Notes |
|---|---|---|
| Published at | 1 Oct 2026, 14:30 | — |
| Published by principal | the name it points at, never the id | — |
| Published by name | text | — |
| Note | text | — |
| Is current | yes / no (icon or chip) | — |
| Scheduled for | 1 Oct 2026, 14:30 | — |
| Content hash | text | — |
| Pending build time changes | list or chips (count when long) | Changes in this version that will not reach guests until the next store release. |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Diff config version (primary button) | `diffConfigVersion` GET `/tenant-config/versions/{version}/diff` | — | ConfigDiff | — | — |
| Restore config version (secondary button) | `restoreConfigVersion` POST `/tenant-config/versions/{version}/restore` | — | TenantConfig | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens confirmDialog first |

**Data it reads**: `listConfigVersions` (onLoad, Version history)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `version`
- → `CMS-014` Publishing Workflow: *Review and publish the restored draft*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No version history yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listConfigVersions` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listConfigVersions` → `TENANT_CONFIGURE` (configure) · staff
- `diffConfigVersion` → `TENANT_CONFIGURE` (configure) · staff
- `restoreConfigVersion` → `TENANT_PUBLISH` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listConfigVersions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.10.30 | CMS Audit Trail | Marketing & CRM | CONTRACTED | `listConfigVersions` |
| 22.10.10 | Version Management | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |
| 22.10.11 | Rollback & Recovery | Marketing & CRM | CONTRACTED | `restoreConfigVersion` |

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-015` · status **notStarted** · provenance generated
- Flow F22 *A tenant rebrands their app*, step 6: Rolls back when something is wrong → **Restore, then review, then publish — not one click** (decided 28 September, audit R139 (b)). `restoreConfigVersion` copies the earlier version into the draft without publishing it, and …
- Flow F22 branch at step 6 (recoverable): when Rollback after guests have seen the new brand, Fine for a homepage, awkward for an app icon that is cached on a device. **The two roll back at different speeds** and the interface should say so.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-015?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Diff config version, Restore config version.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-014`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-016` Site Settings

**The values the whole site inherits from, and the venue-wide booking settings each venue may override (decided 29 September, rev 3 CFG-11); the settings of one flow are on CMS-103 (W12).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18108 (APP-WL-CMS-016) |
| Who uses it | venue staff holding `SCOPE_VIEW`, `TENANT_CONFIGURE` (1 read, 1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | statusTracker (compact density): `getTenantConfig` reads one record and nothing reads a population — the screen is about that one thing |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/site-settings` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Settings for | select field | — | — | — | — | **Which level is being edited** (decided 29 September, rev 3 CFG-11). *All venues* edits the tenant settings; picking a venue edits that venue's entry in `venueOverrides` and shows beside each field … | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Effective for venue | picker: choose an effective for venue | — | — | `getBookingFlowConfig` ?effectiveForVenueId |
| Version | text field | — | — | `getTenantConfig` ?version |
| Under | text field | — | — | `listOrgUnits` ?under |
| Level | select | — | Tenant · Brand · Region · Venue · Department · Sub department · Workstation · Outlet · Subject | `listOrgUnits` ?level |
| Include inactive | toggle | off | — | `listOrgUnits` ?includeInactive |

**Form: Save booking flow config** (modal, opened by *Save booking flow config*; *Save booking flow config* calls `setBookingFlowConfig`, *Cancel* sends nothing)

**Collects what `setBookingFlowConfig` sends before it is called.** Nothing in the body is required. Optional: `preset`, `stepIndicator`, `cartLayout`, `cardLayout`, `cardSize`, `seatPicker`, `mapView`, `density`, `embedMode`, `heroBanner`, `searchInBanner`, `singleEventPage`, `quantitiesOnAddOns`, the venue-wide rev 3 booking rules on the panel above, `guestContactFields` (W1), `dateStripDays` (M17-08) and `venueOverrides` (decided 29 September, rev 3 CFG-11). **The body is the tenant settings plus every venue override**: saving a venue's override sends the whole configuration with that venue's row changed. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Preset `preset` | select | optional | Auto | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | — | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | `setBookingFlowConfig` body |
| Step indicator `stepIndicator` | select | optional | Bar | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | — | — | `setBookingFlowConfig` body |
| Cart layout `cartLayout` | select | optional | Sidebar right | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | — | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Cart side in RTL `cartSideInRtl` | segmented control | optional | Keep right | Keep right · Mirror | — | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Card layout `cardLayout` | radio group | optional | Stacked rows | Stacked rows · Split rows · Cards across · Poster cards | — | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster … | `setBookingFlowConfig` body |
| Card size `cardSize` | radio group | optional | Compact | Compact · Standard · Large · Extra large | — | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Seat picker `seatPicker` | radio group | optional | Bowl | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | — | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | `setBookingFlowConfig` body |
| Map view `mapView` | segmented control | optional | 3D | 2D · 3D | — | — | `setBookingFlowConfig` body |
| Density `density` | segmented control | optional | Compact | Compact · Standard · Roomy | — | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Embed mode `embedMode` | segmented control | optional | Full page | Full page · Embedded | — | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. | `setBookingFlowConfig` body |
| Hero banner `heroBanner` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Search in banner `searchInBanner` | toggle | optional | off | — | — | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | `setBookingFlowConfig` body |
| Event banner dates `eventBannerDates` | toggle | optional | off | — | — | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. | `setBookingFlowConfig` body |
| Single event page `singleEventPage` | toggle | optional | off | — | — | — | `setBookingFlowConfig` body |
| Quantities on add ons `quantitiesOnAddOns` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Times per page `timesPerPage` | radio group | optional | 24 | 8 · 12 · 24 · All | — | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many … | `setBookingFlowConfig` body |
| Day part filter `dayPartFilter` | toggle | optional | on | — | — | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). | `setBookingFlowConfig` body |
| Day part boundaries `dayPartBoundaries` | group | optional | — | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). | `setBookingFlowConfig` body |
| Afternoon starts at `dayPartBoundaries.afternoonStartsAt` | time picker | optional | 12:00 | — | HH:mm, 24-hour | — | `setBookingFlowConfig` body |
| Evening starts at `dayPartBoundaries.eveningStartsAt` | time picker | optional | 17:00 | — | HH:mm, 24-hour | — | `setBookingFlowConfig` body |
| Seat view position `seatViewPosition` | radio group | optional | Bottom | Bottom · Right · Left · Top | — | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). | `setBookingFlowConfig` body |
| Seat time bar `seatTimeBar` | toggle | optional | on | — | — | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the … | `setBookingFlowConfig` body |
| Ticket categories `ticketCategories` | segmented control | optional | Category then subcategory | Category then subcategory · Flat list | — | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one … | `setBookingFlowConfig` body |
| Ticket tags `ticketTags` | toggle | optional | on | — | — | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. | `setBookingFlowConfig` body |
| Card info `cardInfo` | toggle | optional | on | — | — | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. | `setBookingFlowConfig` body |
| Concierge mascot `conciergeMascot` | toggle | optional | on | Read only where the `aiConciergeChat` feature is on. | — | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). | `setBookingFlowConfig` body |
| Show info only `showInfoOnly` | toggle | optional | on | — | — | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its … | `setBookingFlowConfig` body |
| Location switcher `locationSwitcher` | toggle | optional | off | — | — | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). | `setBookingFlowConfig` body |
| Guest contact fields `guestContactFields` | multi-select chips | optional | Email | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | — | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). | `setBookingFlowConfig` body |
| Date strip days `dateStripDays` | stepper or slider (days) | optional | 7 | min 3; max 31 | — | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked … | `setBookingFlowConfig` body |
| Venue overrides `venueOverrides` | repeatable rows | optional | — | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | `setBookingFlowConfig` body |
| Venue `venueOverrides[].venueId` | picker: choose a venue | required | — | At most one override per venue. | shows names, sends the id | One of the tenant's active venues. At most one override per venue. | `setBookingFlowConfig` body |
| Settings `venueOverrides[].settings` | group | required | — | — | — | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue … | `setBookingFlowConfig` body |
| Preset `venueOverrides[].settings.preset` | select | optional | Auto | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | — | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. | `setBookingFlowConfig` body |
| Step indicator `venueOverrides[].settings.stepIndicator` | select | optional | Bar | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | — | — | `setBookingFlowConfig` body |
| Cart layout `venueOverrides[].settings.cartLayout` | select | optional | Sidebar right | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | — | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Cart side in RTL `venueOverrides[].settings.cartSideInRtl` | segmented control | optional | Keep right | Keep right · Mirror | — | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). | `setBookingFlowConfig` body |
| Card layout `venueOverrides[].settings.cardLayout` | radio group | optional | Stacked rows | Stacked rows · Split rows · Cards across · Poster cards | — | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster … | `setBookingFlowConfig` body |
| Card size `venueOverrides[].settings.cardSize` | radio group | optional | Compact | Compact · Standard · Large · Extra large | — | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Seat picker `venueOverrides[].settings.seatPicker` | radio group | optional | Bowl | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | — | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. | `setBookingFlowConfig` body |
| Map view `venueOverrides[].settings.mapView` | segmented control | optional | 3D | 2D · 3D | — | — | `setBookingFlowConfig` body |
| Density `venueOverrides[].settings.density` | segmented control | optional | Compact | Compact · Standard · Roomy | — | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). | `setBookingFlowConfig` body |
| Embed mode `venueOverrides[].settings.embedMode` | segmented control | optional | Full page | Full page · Embedded | — | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. | `setBookingFlowConfig` body |
| Hero banner `venueOverrides[].settings.heroBanner` | toggle | optional | on | — | — | — | `setBookingFlowConfig` body |
| Search in banner `venueOverrides[].settings.searchInBanner` | toggle | optional | off | — | — | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). | `setBookingFlowConfig` body |
| … 16 more | | | | | | the rest are in `schemas.json` | `setBookingFlowConfig` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**The tenant config** (detail panel, from `getTenantConfig`)

| Shows | Format | Notes |
|---|---|---|
| Is draft | yes / no (icon or chip) | True for the working draft, which is the only row. |
| Brand | grouped details | Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB … |
| App icons | grouped details | — |
| Theme | grouped details | — |
| Fonts | grouped details | — |
| Footer | grouped details | BL-002. `setHeader` and `HeaderConfig` exist and the footer does not, which looked like symmetry until you notice it is not: a header is … |
| Notification branding | grouped details | BL-003. `marketing-crm` holds the templates and nothing said whose identity they wear. |
| Enabled payment methods | list or chips (count when long) | BL-004. `FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts. |
| Accessibility | grouped details | BL-065, 2.1.27. POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated. |
| Header | grouped details | — |
| Navigation | grouped details | The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6). |
| Homepage | grouped details | — |
| Modules | list or chips (count when long) | — |
| Features | list or chips (count when long) | — |
| Languages | grouped details | — |

**The booking flow config** (detail panel, from `getBookingFlowConfig`): **Venue-wide booking settings only (decided 29 September, W12).** The settings that belong to one flow (`performanceReveal`, `signInAt`, `seatEventDateMode`, `extrasStep`, `quickTour`, the flow's consent questions) moved to each flow on CMS-103, and `categoryDisplay` is gone (W7, superseding 23SEP-18: `cardLayout` carries rows or grid). Here: `timesPerPage` and the day-part chips (REV3-1) …

| Shows | Format | Notes |
|---|---|---|
| Preset | chip: Auto, Ticket box, Play centre, Venue site, Marketplace, Single event… | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator | chip: Bar, Numbered, Dots, Segmented, Breadcrumb, Pills… | — |
| Cart layout | chip: Sidebar right, Sidebar left, Slide in right, Slide up bottom, Single column … | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). |
| Card layout | chip: Stacked rows, Split rows, Cards across, Poster cards | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked … |
| Card size | chip: Compact, Standard, Large, Extra large | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). |
| Seat picker | chip: Bowl, Zones then seats, Zones only, Seats only | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view | chip: 2D, 3D | — |
| Density | chip: Compact, Standard, Roomy | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). |
| Embed mode | chip: Full page, Embedded | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. |
| Hero banner | yes / no (icon or chip) | — |
| Search in banner | yes / no (icon or chip) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Single event page | yes / no (icon or chip) | — |
| Quantities on add ons | yes / no (icon or chip) | — |
| Cart side in RTL | chip: Keep right, Mirror | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). |
| Event banner dates | yes / no (icon or chip) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Times per page | chip: 8, 12, 24, All | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 … |
| Day part filter | yes / no (icon or chip) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries | grouped details | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Seat view position | chip: Bottom, Right, Left, Top | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar | yes / no (icon or chip) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or … |
| Ticket categories | chip: Category then subcategory, Flat list | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles … |
| Ticket tags | yes / no (icon or chip) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on … |
| Card info | yes / no (icon or chip) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under … |
| Concierge mascot | yes / no (icon or chip) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Show info only | yes / no (icon or chip) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its … |
| Location switcher | yes / no (icon or chip) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the … |
| Guest contact fields | list or chips (count when long) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| Date strip days | 1,234 | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens … |
| Venue overrides | list or chips (count when long) | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with … |

**Venues that differ from the tenant** (data table, from `getBookingFlowConfig`): **One row per venue that overrides anything** (decided 29 September, rev 3 CFG-11). The editor sets only the fields that differ; a field left empty inherits the tenant value, and clearing one removes it from the override. A venue that is not one of the tenant's active venues, or a second row for the same venue, is refused `400` and the row is marked. An override kept for a closed venue is shown …

| Shows | Format | Notes |
|---|---|---|
| Venue | the name it points at, never the id | One of the tenant's active venues. At most one override per venue. |
| Settings | grouped details | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` … |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save booking flow config (primary button) | `setBookingFlowConfig` PUT `/tenant-config/booking-flow` | BookingFlowConfig | BookingFlowConfig | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `getBookingFlowConfig` (onLoad, How the guest booking flow looks and steps); `getTenantConfig` (onLoad, Full working configuration); `listOrgUnits` (onLoad, The tenant's venues, for the per-venue override picker (rev …); `listAnalyticsProviders` (onLoad, Connected analytics platforms)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `version`
- → `CMS-017` Domain & Certificate: *Domain & Certificate*
- → `CMS-018` Consent & Legal: *Consent & Legal*
- → `CMS-103` Booking Flows: *Booking flows*; carries `bookingFlowId`
- → `CMS-101` Help Me Choose: *Help me choose*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The site settings, read by `getTenantConfig`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the site settings untouched. |
| Empty, no results (`?state=emptyNoResults`) | A venue picked in Settings for with no override shows the tenant settings it inherits, labelled as inherited, rather than an empty form (rev 3 CFG-11). |
| Empty, first run (`?state=emptyFirstRun`) | No site settings yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `getBookingFlowConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 422 A `measurementId` that does not match the provider's format, or a `venueId` not among the tenant's active venues |

#### Permissions

- `getBookingFlowConfig` → `TENANT_CONFIGURE` (configure) · staff
- `setBookingFlowConfig` → `TENANT_CONFIGURE` (configure) · staff
- `getTenantConfig` → `TENANT_CONFIGURE` (configure) · staff, guest
- `listOrgUnits` → `SCOPE_VIEW` (read) · staff
- `listAnalyticsProviders` → `TENANT_CONFIGURE` (configure) · staff, guest
- `setAnalyticsProvider` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `getBookingFlowConfig` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

11 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.19 | Tenant-Specific Branding - System shall support tenant-specific branding. | Guest Mobile App & Branding | CONTRACTED | `getTenantConfig` |
| 22.10.1 | Multi-Site CMS | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 22.10.3 | Multi-Brand Management | Marketing & CRM | CONTRACTED | `getTenantConfig` |
| 3.3.41 | Venue-Specific Policies - System shall support venue-specific access policies. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 3.3.43 | Policy Inheritance - System shall support inheritance of policies across organizational structures. | Admission and Access | CONTRACTED | `listOrgUnits` |
| 7.1.13 | The system shall support permission assignment at company, department, venue, park, attraction, facility, event, sales channel, POS terminal, and product levels. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.27 | The system shall support management of companies, business units, departments, parks, venues, attractions, facilities, cost centers, and reporting structures. | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.37 | Allow administrators to restrict access by venue, park, facility, attraction, sales channel, POS terminal, country, region, IP address and network range. Policies should support allow/deny logic and … | F&B POS | CONTRACTED | `listOrgUnits` |
| 7.1.52 | Support policies spanning multiple parks, venues, attractions, departments and business units while maintaining centralized governance. | F&B POS | CONTRACTED | `listOrgUnits` |
| 19.1.21 | Tenant-Specific Notifications - System shall support tenant-specific notifications. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |
| 19.1.23 | Tenant-Specific Payment Methods - System shall support tenant-specific payment methods. | Guest Mobile App & Branding | CONTRACTED | data `TenantConfig` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest date picking shows a strip of the next seven days (venue setting dateStripDays, default 7, range 3-31) with a calendar icon that opens the full month for later dates. *(agreed · MoM 17 Sep 2026, M17-08 · DI-920)*
- CMS manages multiple sites/venues: branding, colour palette including custom hex codes, fonts, Google Analytics site IDs, production/staging environments. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-393)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker · keyword 'cms')*
- **A56** Confirm and implement branding rules across surfaces: TICVAI branding (with "Powered by TICVAI") on staff-facing POS/tablet devices, and white-labeled, client-branded UI on guest-facing kiosks *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker · keyword 'white-label')*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker · keyword 'white-label')*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker · keyword 'cms')*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker · keyword 'cms')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Booking settings preset (`bookingFlow.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Step indicator (`bookingFlow.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none |
| Cart layout (`bookingFlow.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon |
| Cart side in RTL (`bookingFlow.cartSideInRtl`) | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the cart's side in Arabic: kept right, or mirrored left |
| Card layout (`bookingFlow.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | ticket and product cards: stacked rows, split rows, cards across, or poster cards |
| Card size (`bookingFlow.cardSize`) | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | card size: compact, standard, large, extra large |
| Seat picker (`bookingFlow.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Map view (`bookingFlow.mapView`) | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Booking settings density (`bookingFlow.density`) | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | spacing of the booking screens: compact, standard, roomy |
| Embed mode (`bookingFlow.embedMode`) | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | full page, or embedded in the venue's own site (no hero, event page or venue header) |
| Hero banner (`bookingFlow.heroBanner`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | the hero banner at the top of the booking pages |
| Search in banner (`bookingFlow.searchInBanner`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Event banner dates (`bookingFlow.eventBannerDates`) | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Single event page (`bookingFlow.singleEventPage`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Quantities on add ons (`bookingFlow.quantitiesOnAddOns`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Times per page (`bookingFlow.timesPerPage`) | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Day part filter (`bookingFlow.dayPartFilter`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Day part boundaries (`bookingFlow.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Day part boundaries: afternoon starts at (`bookingFlow.dayPartBoundaries.afternoonStartsAt`) | HH:mm, 24-hour | 12:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Day part boundaries: evening starts at (`bookingFlow.dayPartBoundaries.eveningStartsAt`) | HH:mm, 24-hour | 17:00 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Seat view position (`bookingFlow.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Seat time bar (`bookingFlow.seatTimeBar`) | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Ticket categories (`bookingFlow.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Ticket tags (`bookingFlow.ticketTags`) | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Card info (`bookingFlow.cardInfo`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. |
| Concierge mascot (`bookingFlow.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Show info only (`bookingFlow.showInfoOnly`) | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Location switcher (`bookingFlow.locationSwitcher`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). |
| Guest contact fields (`bookingFlow.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| Date strip days (`bookingFlow.dateStripDays`) | min 3; max 31 | 7 | GST-007, GST-008, GST-009, GST-041, WEB-004, WEB-005, WEB-006, WEB-007 … (12) | The date strip (decided 17 September, M17-08). How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar. |
| Venue overrides (`bookingFlow.venueOverrides`) | at most 200; Per-venue overrides, at most one per venue.; A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. | — | GST-001, GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, GST-049 … (17) | Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. |
| Venue overrides: venue (`bookingFlow.venueOverrides[].venueId`) | At most one override per venue. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | One of the tenant's active venues. At most one override per venue. |
| Venue overrides: settings (`bookingFlow.venueOverrides[].settings`) | — | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Every guest booking-flow setting, once. `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). |
| Settings: preset (`bookingFlow.venueOverrides[].settings.preset`) | Auto · Ticket box · Play centre · Venue site · Marketplace · Single event · Season · Custom | Auto | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. |
| Settings: step indicator (`bookingFlow.venueOverrides[].settings.stepIndicator`) | Bar · Numbered · Dots · Segmented · Breadcrumb · Pills · Ticks · None | Bar | GST-007, GST-008, GST-009, GST-041, GST-051, WEB-005, WEB-006, WEB-007 … (13) | — |
| Settings: cart layout (`bookingFlow.venueOverrides[].settings.cartLayout`) | Sidebar right · Sidebar left · Slide in right · Slide up bottom · Single column · Floating icon | Sidebar right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). |
| Settings: cart side in RTL (`bookingFlow.venueOverrides[].settings.cartSideInRtl`) | Keep right · Mirror | Keep right | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10). |
| Settings: card layout (`bookingFlow.venueOverrides[].settings.cardLayout`) | Stacked rows · Split rows · Cards across · Poster cards | Stacked rows | GST-002, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-002, WEB-005 … (14) | How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards. |
| Settings: card size (`bookingFlow.venueOverrides[].settings.cardSize`) | Compact · Standard · Large · Extra large | Compact | GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005, WEB-006, WEB-007 … (12) | Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). |
| Settings: seat picker (`bookingFlow.venueOverrides[].settings.seatPicker`) | Bowl · Zones then seats · Zones only · Seats only; Read only for a seated event. | Bowl | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event. |
| Settings: map view (`bookingFlow.venueOverrides[].settings.mapView`) | 2D · 3D | 3D | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: density (`bookingFlow.venueOverrides[].settings.density`) | Compact · Standard · Roomy | Compact | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). |
| Settings: embed mode (`bookingFlow.venueOverrides[].settings.embedMode`) | Full page · Embedded | Full page | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | `embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site. |
| Settings: hero banner (`bookingFlow.venueOverrides[].settings.heroBanner`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: search in banner (`bookingFlow.venueOverrides[].settings.searchInBanner`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-005, WEB-006, WEB-007 … (12) | Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6). |
| Settings: event banner dates (`bookingFlow.venueOverrides[].settings.eventBannerDates`) | — | off | GST-004, GST-007, GST-008, GST-009, GST-041, WEB-001, WEB-004, WEB-005 … (14) | Dates in event banner (decided 29 September, rev 3 23SEP-19). On, the event banner lists the next dates; off by default. |
| Settings: single event page (`bookingFlow.venueOverrides[].settings.singleEventPage`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: quantities on add ons (`bookingFlow.venueOverrides[].settings.quantitiesOnAddOns`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | — |
| Settings: times per page (`bookingFlow.venueOverrides[].settings.timesPerPage`) | 8 · 12 · 24 · All | 24 | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Times per page (decided 29 September, rev 3 REV3-1). When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` … |
| Settings: day part filter (`bookingFlow.venueOverrides[].settings.dayPartFilter`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1). |
| Settings: day part boundaries (`bookingFlow.venueOverrides[].settings.dayPartBoundaries`) | `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400. | — | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1). |
| Settings: seat view position (`bookingFlow.venueOverrides[].settings.seatViewPosition`) | Bottom · Right · Left · Top | Bottom | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5). |
| Settings: seat time bar (`bookingFlow.venueOverrides[].settings.seatTimeBar`) | — | on | GST-007, GST-008, GST-009, GST-041, GST-049, WEB-005, WEB-006, WEB-007 … (12) | Time bar above the seat map (decided 29 September, rev 3 REV3-6). Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one. |
| Settings: ticket categories (`bookingFlow.venueOverrides[].settings.ticketCategories`) | Category then subcategory · Flat list | Category then subcategory | GST-002, GST-003, GST-007, GST-008, GST-009, GST-041, WEB-002, WEB-005 … (14) | How tickets are grouped (decided 29 September, rev 3 REV3-16). `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once. |
| Settings: ticket tags (`bookingFlow.venueOverrides[].settings.ticketTags`) | — | on | GST-004, GST-007, GST-008, GST-009, GST-013, GST-041, WEB-004, WEB-005 … (14) | Tags on tickets (decided 29 September, rev 3 23SEP-3). Shows a product's display tags (such as "2 Hours", "Min 1.10 m", "Valid 90 days") on its card. |
| Settings: card info (`bookingFlow.venueOverrides[].settings.cardInfo`) | — | on | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Extra info on cards (decided 29 September, rev 3 23SEP-6). Shows each ticket type's description, who it is for and what it includes, under its name. |
| Settings: concierge mascot (`bookingFlow.venueOverrides[].settings.conciergeMascot`) | Read only where the `aiConciergeChat` feature is on. | on | GST-007, GST-008, GST-009, GST-031, GST-041, WEB-005, WEB-006, WEB-007 … (13) | The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5). |
| Settings: show info only (`bookingFlow.venueOverrides[].settings.showInfoOnly`) | — | on | GST-003, GST-007, GST-008, GST-009, GST-041, GST-063, WEB-002, WEB-003 … (15) | Show info-only products (decided 29 September, rev 3 REV3-14). On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it. |
| Settings: location switcher (`bookingFlow.venueOverrides[].settings.locationSwitcher`) | — | off | GST-007, GST-008, GST-009, GST-041, WEB-005, WEB-006, WEB-007, WEB-008 … (11) | Location switcher (decided 29 September, rev 3 REV3-18). On, the booking screens carry a "Booking at" bar with Change location, reusing the guest's venue choice (audit R267). |
| Settings: guest contact fields (`bookingFlow.venueOverrides[].settings.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | GST-007, GST-008, GST-009, GST-041, GST-042, WEB-005, WEB-006, WEB-007 … (13) | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| … 10 more | | | | `WHITE-LABEL.md` |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-016` · status **notStarted** · provenance generated
- ADR-0018 *— Configuration scope* (`docs/adr/0018-configuration-scope.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (62), with its required mark, default, format and its error state (400, 403, 404, 422).
- [ ] Every output is drawn (46 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-016?state=<state>`: loading, error, emptyNoResults, emptyFirstRun, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save booking flow config.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`, `CMS-017`, `CMS-018`, `CMS-103`, `CMS-101`.
- [ ] Every gated control is gated: `SCOPE_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 3 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-017` Domain & Certificate

**Point the tenant’s own domain at their site.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18109 (APP-WL-CMS-017) |
| Who uses it | venue staff holding `TENANT_CONFIGURE` (1 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listCustomDomains` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `domainId` (navigation) · cold entry: **Verification and release act on one domain**, taken from the row. A release issued against a domain nobody can see is a site going dark with no record of who … |
| Route | `/white-label/domain-certificate` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**Form: Claim custom domain** (modal, opened by *Claim custom domain*; *Claim custom domain* calls `claimCustomDomain`, *Cancel* sends nothing)

**Collects what `claimCustomDomain` sends before it is called.** Required: `hostname`, `kind`. Optional: `verificationMethod`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Hostname `hostname` | text field | required | — | — | — | — | `claimCustomDomain` body |
| Kind `kind` | radio group | required | — | Guest web · Guest app · Partner portal · Developer portal | — | — | `claimCustomDomain` body |
| Verification method `verificationMethod` | segmented control | optional | Dns txt | Dns txt · Cname · Http file | — | — | `claimCustomDomain` body |

Errors to draw in the form: 409 Already claimed. Named as unavailable rather than attributed.

#### Outputs: what the screen shows and produces

**Shown**

**Every custom domain** (data table, from `listCustomDomains`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Hostname | text | — |
| Kind | chip: Guest web, Guest app, Partner portal, Developer portal | — |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Verification method | chip: Dns txt, Cname, Http file | — |
| Verification token | text | — |
| Certificate expires at | 1 Oct 2026, 14:30 | Renewal is a job, not a reminder. A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder … |
| Last checked at | 1 Oct 2026, 14:30 | — |
| Failure reason | text | — |

**The selected custom domain** (detail panel, from `listCustomDomains`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Hostname | text | — |
| Kind | chip: Guest web, Guest app, Partner portal, Developer portal | — |
| Status | chip: Pending, Verifying, Verified, Issuing, Active, Failed… | — |
| Verification method | chip: Dns txt, Cname, Http file | — |
| Verification token | text | — |
| Certificate expires at | 1 Oct 2026, 14:30 | Renewal is a job, not a reminder. A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder … |
| Last checked at | 1 Oct 2026, 14:30 | — |
| Failure reason | text | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Claim custom domain (primary button) | `claimCustomDomain` POST `/tenant-domains` | inline | CustomDomain | 409 Already claimed. Named as unavailable rather than attributed. | opens modal first |
| Verify custom domain (secondary button) | `verifyCustomDomain` POST `/tenant-domains/{domainId}/verify` | — | CustomDomain | 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued. | — |
| Release custom domain (secondary button) | `relinquishCustomDomain` DELETE `/tenant-domains/{domainId}` | — | — | 409 The only active domain for a live app. Refused, naming what would break. | — |

**Data it reads**: `listCustomDomains` (onLoad, Domains claimed, and their state)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Detail loads |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | Not found — it may have been deleted or moved out of scope |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listCustomDomains` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Already claimed. Named as unavailable rather than attributed.; 409 The hostname is already routed to another tenant (`hostname-taken`, from tenancy `setTenantDomainMapping`, SD-021); nothing was verified or issued.; 409 The only active domain for a live app. Refused, naming what would break. |

#### Permissions

- `listCustomDomains` → `TENANT_CONFIGURE` (configure) · staff
- `claimCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `verifyCustomDomain` → `TENANT_CONFIGURE` (configure) · staff
- `relinquishCustomDomain` → `TENANT_CONFIGURE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listCustomDomains` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Guest web hosting: small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a dedicated URL on their own domain. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-283)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Custom domain hostname (`domains.hostname`) | — | — | every website screen | — |
| Custom domain kind (`domains.kind`) | Guest web · Guest app · Partner portal · Developer portal | — | every website screen | — |
| Verification method (`domains.verificationMethod`) | Dns txt · Cname · Http file | Dns txt | every website screen | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-017` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (3), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Claim custom domain, Verify custom domain, Release custom domain.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `TENANT_CONFIGURE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-018` Consent & Legal

**Manage the notices every consent is captured against, and the booking consent questions a venue asks ("Are you able to swim?", "I accept the risk"), with the record of every answer (decided 29 September, rev 3 REV3-26).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18195 (APP-WL-CMS-018) |
| Who uses it | venue staff holding `GUEST_MANAGE`, `GUEST_VIEW`, `TENANT_CONFIGURE` (2 configure, 1 read) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPolicies` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | `policyKind` (navigation), `questionId` (navigation) |
| Route | `/white-label/consent-legal` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. **Rewired 23 September (L7).** The screen called the maintenance equipment register, guest CRM or subscription billing where its purpose names White Labelling. Its operations now match its purpose.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Include history | toggle | off | — | `listPolicies` ?includeHistory |
| Kind | radio group | — | Privacy · Terms and conditions · Refund · Cookie · Accessibility | `listPolicies` ?kind |
| Kind | radio group | — | Swim · Scuba · Risk · Custom | `listConsentQuestions` ?kind |
| Status | segmented control | — | Active · Retired | `listConsentQuestions` ?status |

**Form: Save policy** (modal, opened by *Save policy*; *Save policy* calls `setPolicy`, *Cancel* sends nothing)

**Collects what `setPolicy` sends before it is called.** Required: `body`, `requiresReconsent`. Optional: `effectiveFrom`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Body `body` | rich text, one per language | required | — | — | English and Arabic (Arabic right to left) | Keyed by language code. Values are sanitised HTML. | `setPolicy` body |
| Requires reconsent `requiresReconsent` | toggle | required | — | — | — | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. | `setPolicy` body |
| Effective from `effectiveFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `setPolicy` body |

Errors to draw in the form: 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096)

**Form: Save consent purposes** (modal, opened by *Save consent purposes*; *Save consent purposes* calls `setConsentPurposes`, *Cancel* sends nothing)

**Collects what `setConsentPurposes` sends before it is called.** Required: `purposes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purposes `purposes` | repeatable rows | required | — | — | — | — | `setConsentPurposes` body |
| Purpose `purposes[].purpose` | select | required | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `setConsentPurposes` body |
| Display name `purposes[].displayName` | text field | optional | — | — | — | — | `setConsentPurposes` body |
| Description `purposes[].description` | text area | optional | — | — | — | — | `setConsentPurposes` body |
| Channels `purposes[].channels` | multi-select chips | required | — | Email · SMS · Whatsapp · Push · In app · Post | — | — | `setConsentPurposes` body |
| Notice version `purposes[].noticeVersion` | text field | required | — | — | — | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. | `setConsentPurposes` body |
| Is required for service `purposes[].isRequiredForService` | toggle | required | — | Withdrawing it means the service cannot be delivered, so it is presented differently. | — | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. | `setConsentPurposes` body |
| Expires after months `purposes[].expiresAfterMonths` | number field | optional | — | — | — | — | `setConsentPurposes` body |

**Form: New consent question** (modal, opened by *New consent question*; *Create question* calls `createConsentQuestion`, *Cancel* sends nothing)

**Collects what `createConsentQuestion` sends before it is called.** Required: `kind`, `text` (every tenant language). Optional: `helpText`, `scope` (`perPerson`, the default, or `perBooking`), `required` (default true: checkout waits for it) and `blockingAnswer` (`yes`, `no` or `none`, the default: the answer that stops the booking for the person or booking it covers). Created at version 1 (rev 3 REV3-26). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Swim · Scuba · Risk · Custom | — | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue … | `createConsentQuestion` body |
| Text `text` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | The question as the guest reads it, per locale. | `createConsentQuestion` body |
| Help text `helpText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `createConsentQuestion` body |
| Scope `scope` | segmented control | required | Per person | Per person · Per booking | — | Asked for each declared person, or once for the whole booking. | `createConsentQuestion` body |
| Required `required` | toggle | required | on | — | — | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). | `createConsentQuestion` body |
| Blocking answer `blockingAnswer` | segmented control | required | None | Yes · No · None | — | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. | `createConsentQuestion` body |
| Status `status` | segmented control | required | Active | Active · Retired | — | — | `createConsentQuestion` body |

Errors to draw in the form: 400 Validation failed; 403 Authenticated but not permitted at the requested scope

**Form: Save as new version** (modal, opened by *Save as new version*; *Save new version* calls `updateConsentQuestion`, *Cancel* sends nothing)

**Says, before saving, that the guest will be asked version N+1 from the next cart read** and that answers already given keep their version (rev 3 REV3-26). Optional: `text`, `helpText`, `scope`, `required`, `blockingAnswer`, `status`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Kind `kind` | radio group | required | — | Swim · Scuba · Risk · Custom | — | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue … | `updateConsentQuestion` body |
| Text `text` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | The question as the guest reads it, per locale. | `updateConsentQuestion` body |
| Help text `helpText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateConsentQuestion` body |
| Scope `scope` | segmented control | required | Per person | Per person · Per booking | — | Asked for each declared person, or once for the whole booking. | `updateConsentQuestion` body |
| Required `required` | toggle | required | on | — | — | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). | `updateConsentQuestion` body |
| Blocking answer `blockingAnswer` | segmented control | required | None | Yes · No · None | — | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. | `updateConsentQuestion` body |
| Status `status` | segmented control | required | Active | Active · Retired | — | — | `updateConsentQuestion` body |

Errors to draw in the form: 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.

#### Outputs: what the screen shows and produces

**Shown**

**Every policy** (data table, from `listPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Privacy, Terms and conditions, Refund, Cookie, Accessibility | — |
| Title | text | The heading a guest sees, and the field a refund question retrieves against. |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent | yes / no (icon or chip) | — |
| Effective from | 1 Oct 2026 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**Every consent purpose config** (data table, from `listConsentPurposes`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |

**Every booking consent question** (data table, from `listConsentQuestions`): **A consent, not a data field** (decided 29 September, rev 3 REV3-26). Each question has its own text per locale, a version, and whether it is asked for each person or once per booking. Filter by `kind` and `status`. **Attaching** is done where the question is used: to a booking flow on CMS-016 (`BookingFlowConfig.consentQuestionIds`, per venue), to a product on BO-008 …

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Swim, Scuba, Risk, Custom | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others … |
| Text | in the reader's language | The question as the guest reads it, per locale. |
| Version | 1,234 | Raised by one each time the question changes (`updateConsentQuestion`). |
| Scope | chip: Per person, Per booking | Asked for each declared person, or once for the whole booking. |
| Required | yes / no (icon or chip) | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). |
| Blocking answer | chip: Yes, No, None | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. |
| Status | chip: Active, Retired | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**Consent records** (data table, from `listConsentAnswers`): **What was asked, at which version, what was answered, for whom, by whom and when** (rev 3 REV3-26). Filter by order, guest or question. Read-only: an answer is never edited here, and a superseded answer stays listed with `supersededAt`.

| Shows | Format | Notes |
|---|---|---|
| Answered at | 1 Oct 2026, 14:30 | — |
| Question | the name it points at, never the id | — |
| Question version | 1,234 | — |
| Answer | chip: Yes, No | — |
| Scope | chip: Per person, Per booking | — |
| Person name | text | — |
| Order | the name it points at, never the id | Set by `orders.checkoutCart` when the cart becomes an order. |
| Answered by subject | the name it points at, never the id | The guest who answered, from the session. Null for an anonymous cart. |
| Answered by principal | the name it points at, never the id | The staff member who answered on the guest's behalf. |
| Source | chip: Guest app, Website, Kiosk, POS, Call centre, Import… | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` … |
| Blocks booking | yes / no (icon or chip) | The answer is the question's `blockingAnswer` at that version. |
| Superseded at | 1 Oct 2026, 14:30 | — |

**The selected policy** (detail panel, from `listPolicies`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Privacy, Terms and conditions, Refund, Cookie, Accessibility | — |
| Title | text | The heading a guest sees, and the field a refund question retrieves against. |
| Body | in the reader's language | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent | yes / no (icon or chip) | — |
| Effective from | 1 Oct 2026 | — |
| Published by principal | the name it points at, never the id | — |
| Published at | 1 Oct 2026, 14:30 | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The selected consent question** (detail panel, from `listConsentQuestions`)

| Shows | Format | Notes |
|---|---|---|
| Kind | chip: Swim, Scuba, Risk, Custom | What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others … |
| Text | in the reader's language | The question as the guest reads it, per locale. |
| Help text | in the reader's language | — |
| Version | 1,234 | Raised by one each time the question changes (`updateConsentQuestion`). |
| Scope | chip: Per person, Per booking | Asked for each declared person, or once for the whole booking. |
| Required | yes / no (icon or chip) | Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`). |
| Blocking answer | chip: Yes, No, None | The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing. |
| Status | chip: Active, Retired | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save policy (primary button) | `setPolicy` PUT `/tenant-config/policies/{policyKind}` | inline | Policy | 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096) | opens modal first |
| Save consent purposes (secondary button) | `setConsentPurposes` PUT `/consent-purposes` | inline | ConsentPurposeConfig[] | — | opens modal first |
| New consent question (secondary button) | `createConsentQuestion` POST `/consent-questions` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 403 Authenticated but not permitted at the requested scope | opens modal first |
| Save as new version (secondary button) | `updateConsentQuestion` PATCH `/consent-questions/{questionId}` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |
| Retire question (destructive button) | `updateConsentQuestion` PATCH `/consent-questions/{questionId}` | ConsentQuestion | ConsentQuestion | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | opens modal first |

**Data it reads**: `listPolicies` (onLoad, Privacy, terms and cookie notices); `listConsentPurposes` (onLoad, What guests can consent to); `listConsentQuestions` (onLoad, The venue's booking consent questions (rev 3 REV3-26))

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*; carries `policyKind`, `version`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The consent legal list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the consent legal untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No consent legal yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | `listPolicies` takes no filter. The consent questions (kind, status) and the consent records (order, guest, question) do: an empty result names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listPolicies` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 The English (`en`) or Arabic (`ar`) version is missing (audit R096); 400 Validation failed |

#### Permissions

- `listPolicies` → `TENANT_CONFIGURE` (configure) · staff
- `setPolicy` → `TENANT_CONFIGURE` (configure) · staff
- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `setConsentPurposes` → `GUEST_MANAGE` (configure) · staff
- `listConsentQuestions` → `GUEST_VIEW` (read) · staff
- `createConsentQuestion` → `GUEST_MANAGE` (configure) · staff
- `updateConsentQuestion` → `GUEST_MANAGE` (configure) · staff
- `listConsentAnswers` → `GUEST_VIEW` (read) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listPolicies` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

4 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.1.17 | Policy Management - System shall support configurable policies. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 19.1.18 | Terms & Conditions Management - System shall support configurable terms and conditions. | Guest Mobile App & Branding | CONTRACTED | `setPolicy` |
| 2.6.59 | Policy Management Manage cookie policy content centrally. Version control for policy updates. Publish updated policies automatically. Maintain historical policy versions. | Ticketing Sales | CONTRACTED | `setPolicy` |
| 22.13.7 | Consent Expiration Management | Marketing & CRM | CONTRACTED | `setConsentPurposes` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Refund policy shown to guests is tiered and driven by back-office rules per business, e.g. no refund <24h, 50% between 24–48h, 100% >48h. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-192)*
- Configurable FAQ section plus Terms & Conditions, Privacy Policy and Cookie Policy with an accept/deny prompt. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-191)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A91** Build the consent & data-privacy layer (consent policy gating sends, data-subject-request module, per-tenant retention/archival with defaults) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'consent & data')*
- **A209** Build privacy consent capture at checkout and cookie policy management (configurable banner per site, mandatory vs. optional cookies, templated) *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 1 Sep 2026 · workshop tracker · keyword 'privacy')*
- **A227** Define biometric and guest data retention tiers and regional compliance requirements, using an existing client's live privacy policy as the model *(Softlabs Team / Qossai · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 2 Sep 2026 · workshop tracker · keyword 'privacy')*
- **C43** Confirm facial-recognition and guest data retention periods and any regional compliance requirements, and share the reference client's live privacy policy *(Qossai · Pending → 30 Sep: Closed, Moved to T2 · 2 Sep 2026 · workshop tracker · keyword 'privacy')*

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Body (`policies.body`) | English and Arabic (Arabic right to left) | — | the content and policy pages | Keyed by language code. Values are sanitised HTML. |
| Requires reconsent (`policies.requiresReconsent`) | — | — | the content and policy pages | True prompts existing guests to consent again on next launch. Material changes to a privacy notice generally require it. |
| Effective from (`policies.effectiveFrom`) | 1 Oct 2026 (dd MMM yyyy) | — | the content and policy pages | — |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-018` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (25), with its required mark, default, format and its error state (400, 403, 404).
- [ ] Every output is drawn (51 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save policy, Save consent purposes, New consent question, Save as new version, Retire question.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `GUEST_MANAGE`, `GUEST_VIEW`, `TENANT_CONFIGURE`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-019` User Access

**Say who in the tenant may change what.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #18084 (APP-WL-CMS-019) |
| Who uses it | venue staff holding `ROLE_MANAGE`, `USER_MANAGE` (2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listPrincipals` reads a population and nothing reads one of them; the detail is the row until a `get` exists |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/white-label/user-access` |

**What the spec says about it.** Definition derived from the wireframe board on 14 August. Components, states and operations still to be written. States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Scope path | text field | optional | — | — | — | Sends `?scopePath=` to `listPrincipals`. | `listPrincipals` ?scopePath |
| Is active | toggle | optional | — | — | — | Sends `?isActive=` to `listPrincipals`. | `listPrincipals` ?isActive |

#### Outputs: what the screen shows and produces

**Shown**

**Every principal** (data table, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Every role** (data table, from `listRoles`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Code | text | Unique within the tenant (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. |
| Name | text | — |
| Description | text | — |
| Permissions | list or chips (count when long) | A role that grants no permissions is not a role. `Role` carried a code, a name and two counts until 18 August, and … |
| Inherits from role | the name it points at, never the id | Role composition, one level deep and no deeper. A supervisor role that is a cashier plus three permissions is how venues actually describe … |
| Is system | yes / no (icon or chip) | Seeded roles ship and are editable; deleting one is refused. A venue that removes `cashier` and rebuilds it has two roles with one name in … |
| Principal count | 1,234 | — |
| Grant count | 1,234 | — |

**The selected principal** (detail panel, from `listPrincipals`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Username | text | — |
| Display name | text | — |
| Is active | yes / no (icon or chip) | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Past this, resolution returns DENY regardless of grants. |
| Primary role | the name it points at, never the id | Determines the landing screen when the principal holds several roles and picks one at login. |
| Roles | list or chips (count when long) | — |
| Last login at | 1 Oct 2026, 14:30 | — |

**Data it reads**: `listPrincipals` (onLoad, List principals); `listRoles` (onLoad, List roles)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Tenant Workspace*
- → `CMS-002` Brand Kit: *Brand Kit*
- → `CMS-003` Typography: *Typography*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The user access list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the user access untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No user access yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on scopePath, isActive and the user access are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listPrincipals` → `USER_MANAGE` (configure) · staff, partner
- `listRoles` → `ROLE_MANAGE` (configure) · staff

**A refused user sees:** Shown when the caller lacks `USER_MANAGE`, which `listPrincipals` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-019` · status **notStarted** · provenance generated

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (27 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-001`, `CMS-002`, `CMS-003`.
- [ ] Every gated control is gated: `ROLE_MANAGE`, `USER_MANAGE`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-101` Help Me Choose

**Set up a venue's Help me choose so its answers filter the catalogue, review the question set the assistant proposes from the venue's products, preview the filtered list and publish it (Site Builder step 4).**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | White Label · wave 2 · needs the `core` module |
| Block | Block A · ticket #20770 (APP-WL-CMS-101) |
| Who uses it | venue staff holding `AI_USE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH` (1 operate, 1 read, 2 configure) |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listGuidedChoices` reads the venue's set-ups and the editor acts on one of them — list, select, act |
| Offline | online only |
| Opens with | `venueId` (session), `guidedChoiceId` (navigation), `suggestionId` (navigation) · cold entry: Resolves the venue from the session and opens on the suggestions awaiting review, or on the list when there are none. |
| Route | `/white-label/help-me-choose` |

**What the spec says about it.** **Added 29 September for rev 3 REV3-11: Help me choose is venue configuration, never hard-coded.** A venue sets up one or two questions, each with two to four answers (title, one-liner, icon, optional badge), and the answer picked on the last question opens the product, category, event or booking module that fits through a result card. **Two sources, one review**: staff write a set-up here, and once the venue's products are uploaded the `ai` service proposes set-ups (`source` `aiSuggested`), which land here as drafts. **A suggestion is never published by itself**: a person reviews it, edits it or dismisses it, previews it and publishes it. One published set-up per venue; publishing another returns the old one to draft.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue | select field | — | — | — | — | The venue whose set-ups are shown (path `venueId`); defaults to the session venue. | — |
| Source | select field | — | — | — | — | Sends `?source=`, `manual` or `aiSuggested`. **Suggestions awaiting review** is `aiSuggested` with status `draft`, and is the default view while any exist. | — |
| Status | select field | — | — | — | — | Sends `?status=`, `draft` or `published`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Status | segmented control | Draft | Draft · Published | `listGuidedChoices` ?status |
| Source | segmented control | — | Manual · AI suggested | `listGuidedChoices` ?source |

**Form: New set-up** (modal, opened by *New set-up*; *Create draft* calls `createGuidedChoice`, *Cancel* sends nothing)

**Collects what `createGuidedChoice` sends before it is called.** Required: `name` (staff-facing), `mode`, `questions` (one or two, each with two to four answers and a target per answer). Optional: `showBanner` (default on). Created as a draft; guests see nothing until it is published. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | required | — | max length 80 | — | Staff-facing name, e.g. "Water park day planner". | `createGuidedChoice` body |
| Mode `mode` | segmented control | required | Button | Button · Popup on arrival · Off | — | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the … | `createGuidedChoice` body |
| Show banner `showBanner` | toggle | optional | on | — | — | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. | `createGuidedChoice` body |
| Behaviour `behaviour` | segmented control | optional | Filter | Filter · Recommend | — | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). | `createGuidedChoice` body |
| Show everything `showEverything` | toggle | optional | on | — | — | The "Show everything" link under a filtered list, which clears the answers (W4). | `createGuidedChoice` body |
| Questions `questions` | repeatable rows | required | — | at least 1; at most 4 | — | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). | `createGuidedChoice` body |
| Title `questions[].title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createGuidedChoice` body |
| Kind `questions[].kind` | radio group | optional | Choice | Choice · Yes no · Age · Level · Certification | — | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. | `createGuidedChoice` body |
| Sort order `questions[].sortOrder` | number field | required | — | min 0 | — | — | `createGuidedChoice` body |
| Answers `questions[].answers` | repeatable rows | required | — | at least 2; at most 4 | — | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). | `createGuidedChoice` body |
| Title `questions[].answers[].title` | text, one per language | required | — | — | English and Arabic (Arabic right to left) | — | `createGuidedChoice` body |
| Body `questions[].answers[].body` | text, one per language | optional | — | The one-liner under the title, at most 140 characters in each language. | English and Arabic (Arabic right to left) | The one-liner under the title, at most 140 characters in each language. | `createGuidedChoice` body |
| Icon `questions[].answers[].icon` | text field | optional | — | max length 40 | — | An icon name from the guest app's icon set. | `createGuidedChoice` body |
| Badge `questions[].answers[].badge` | text, one per language | optional | — | At most 24 characters in each language. | English and Arabic (Arabic right to left) | Optional, e.g. "Best value". | `createGuidedChoice` body |
| Sort order `questions[].answers[].sortOrder` | number field | required | — | min 0 | — | — | `createGuidedChoice` body |
| Target `questions[].answers[].target` | group | optional | — | — | — | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. | `createGuidedChoice` body |
| Filter `questions[].answers[].filter` | group | optional | — | — | — | What this answer keeps in the list (decided 29 September, W4). Every field set must hold; answers to different questions are combined with AND. | `createGuidedChoice` body |
| Consent prefill `questions[].answers[].consentPrefill` | group | optional | — | — | — | Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4). | `createGuidedChoice` body |
| Result `questions[].answers[].result` | group | optional | — | — | — | The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image. | `createGuidedChoice` body |

Errors to draw in the form: 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds

**Form: Publish** (confirmDialog, opened by *Publish*; *Publish to guests* calls `publishGuidedChoice`, *Cancel* sends nothing)

**Names the venue and the set-up that stops showing there**, since only one is published per venue. An answer whose target is not on sale or not enabled blocks the publish and is named (`422`).

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already `published`; 422 An answer's target is not on sale or not enabled, or an answer lacks the filter or target its behaviour needs; the problem names the answer

**Form: Delete draft or dismiss suggestion** (confirmDialog, opened by *Delete draft or dismiss suggestion*; *Delete* calls `deleteGuidedChoice`, *Keep it* sends nothing)

Names the set-up and, for an AI suggestion, says that dismissing it removes it and the assistant's reasoning with it. A published set-up cannot be deleted (`409`).

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published`

**Sent by *Save draft*** (`updateGuidedChoice`; no form is declared, so these are filled from the screen or collected inline)

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Name `name` | text field | optional | — | max length 80 | — | — | `updateGuidedChoice` body |
| Mode `mode` | segmented control | optional | — | Button · Popup on arrival · Off | — | — | `updateGuidedChoice` body |
| Show banner `showBanner` | toggle | optional | — | — | — | — | `updateGuidedChoice` body |
| Behaviour `behaviour` | segmented control | optional | — | Filter · Recommend | — | — | `updateGuidedChoice` body |
| Show everything `showEverything` | toggle | optional | — | — | — | — | `updateGuidedChoice` body |
| Questions `questions` | repeatable rows | optional | — | at least 1; at most 4 | — | Replaces the whole question list; same shape and bounds as `GuidedChoice.questions`. | `updateGuidedChoice` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every Help me choose set-up at this venue** (data table, from `listGuidedChoices`): **An AI suggestion is labelled as one** on its row, and keeps `source` `aiSuggested` after a person edits it, so a report can count how many proposals were published.

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Status | chip: Draft, Published | Draft until a person publishes it (decided 29 September, rev 3 REV3-11). Guests see only a `published` choice. |
| Source | chip: Manual, AI suggested | `manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Published at | 1 Oct 2026, 14:30 | — |
| Updated at | 1 Oct 2026, 14:30 | — |

**The selected set-up** (detail panel, from `listGuidedChoices`): **The editor.** `mode`: a button on the booking page, a pop-up on the guest's first arrival as well, or off (configured but not shown). `showBanner`: the dark banner under the products. One or two questions, two to four answers each: title, one-liner (140 characters), icon, badge (24 characters), target (a product, category, event or booking module, picked from `listProducts` …

| Shows | Format | Notes |
|---|---|---|
| Name | text | Staff-facing name, e.g. "Water park day planner". |
| Mode | chip: Button, Popup on arrival, Off | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on … |
| Show banner | yes / no (icon or chip) | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Behaviour | chip: Filter, Recommend | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything | yes / no (icon or chip) | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Questions | list or chips (count when long) | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Status | chip: Draft, Published | Draft until a person publishes it (decided 29 September, rev 3 REV3-11). Guests see only a `published` choice. |
| Source | chip: Manual, AI suggested | `manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). |
| Suggestion ref | text | For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`. |
| Published at | 1 Oct 2026, 14:30 | — |
| Published by | the name it points at, never the id | The person who published it. Never a service. |

**Preview** (live preview): **Renders the draft as a guest would meet it**: the button or pop-up, the banner, each question and the result card, in each language and in both directions. Drawn from the record in hand; it calls nothing and publishes nothing, and guests keep seeing the published set-up until Publish. **Preview the filtered list**: for each combination of answers, the products left (read with `listProducts` and …

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| What publishing changes (publish gate) | navigation or local | — | — | — | — |
| New set-up (primary button) | `createGuidedChoice` POST `/venues/{venueId}/guided-choices` | GuidedChoice | GuidedChoice | 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds | opens modal first |
| Save draft (secondary button) | `updateGuidedChoice` PATCH `/guided-choices/{guidedChoiceId}` | inline | GuidedChoice | 400 Validation failed; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published`; unpublish it first | — |
| Publish (secondary button) | `publishGuidedChoice` POST `/guided-choices/{guidedChoiceId}/publish` | — | GuidedChoice | 403 Authenticated but not permitted at the requested scope; 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Already `published` | opens confirmDialog first |
| Unpublish (secondary button) | `unpublishGuidedChoice` POST `/guided-choices/{guidedChoiceId}/unpublish` | — | GuidedChoice | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 Not `published` | — |
| Delete draft or dismiss suggestion (destructive button) | `deleteGuidedChoice` DELETE `/guided-choices/{guidedChoiceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path.; 409 The choice is `published` | opens confirmDialog first |

**Data it reads**: `listGuidedChoices` (onLoad, The venue's set-ups, filtered by source and status (rev 3 …)

**Where the user goes next**

- → `CMS-016` Site Settings: *Back to Site Settings*
- → `CMS-102` Site Builder: *Back to the Site Builder*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The venue's Help me choose set-ups, read by `listGuidedChoices`. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the set-ups untouched. |
| Empty, first run (`?state=emptyFirstRun`) | **No Help me choose at this venue, so guests see none.** Offers New set-up, and says that once the venue's products are uploaded the assistant proposes set-ups here as drafts for review. |
| Empty, no results (`?state=emptyNoResults`) | The source or status filter matched nothing and the venue's other set-ups are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Shown when the caller lacks `TENANT_CONFIGURE`, which `listGuidedChoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A `categoryId` that names no category of the venue, or a `guidedAnswerIds` entry that is not an answer of the venue's published guided choice (W4, 29 …; 400 A target is not in this venue, a required target id is missing for its `kind`, or the question and answer counts are outside their bounds; 400 Validation failed; 409 A suggestion for this venue is already running … |

#### Permissions

- `listGuidedChoices` → `TENANT_CONFIGURE` (configure) · staff
- `createGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `updateGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `deleteGuidedChoice` → `TENANT_CONFIGURE` (configure) · staff
- `publishGuidedChoice` → `TENANT_PUBLISH` (configure) · staff
- `unpublishGuidedChoice` → `TENANT_PUBLISH` (configure) · staff
- `listProducts` → `PRODUCT_VIEW` (read) · staff, guest, partner
- `listProductCategories` → `PRODUCT_VIEW` (read) · staff, guest
- `listEvents` → `PRODUCT_VIEW` (read) · staff
- `listBookingFlows` → `TENANT_CONFIGURE` (configure) · staff
- `suggestGuidedChoice` → `AI_USE` (operate) · staff
- `getGuidedChoiceSuggestion` → `AI_USE` (operate) · staff

**A refused user sees:** Shown when the caller lacks `TENANT_CONFIGURE`, which `listGuidedChoices` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

3 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.7 | For BtoC online sales, the following points shall be available online: | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.6.8 | - All PLUs | Ticketing Sales | CONTRACTED | `listProducts` |
| 2.13.21 | All PLUs can be sold on the POS (ticketing and non-ticketing) including Packages. | Ticketing Sales | CONTRACTED | `listProducts` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Help me choose needs a configuration page per venue; AI may propose the question set from the product catalogue for the operator to validate and edit. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1006)*
- "Help me choose" (experience builder) is not a consent step: its questions (yes/no, age, certified or not, etc.) filter the catalogue so only suitable products are shown (Deep Dive Dubai reference). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W4 Help me choose · DI-1005)*
- Help me choose setup per venue: up to 2 questions, 3 answers each (title, one-line description, icon, optional badge e.g. "Best value"), each answer mapped to one booking flow, a result card (title, description, image) per recommendable product, and placement (button above products, pop-up on arrival, off). *(agreed · design review 23 Sep 2026, What the venue sets up in the CMS (per venue) · DI-984)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*

Also apply: 9 for P13 · White Label, 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### What this screen configures on the guest surfaces

Each field here is an **input** a tenant sets; the right column is the **output** a guest sees once it is published (CMS-014). The full map: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Field | Allowed values | Default | Reaches | What it changes |
|---|---|---|---|---|
| Help me choose name (`guidedChoices.name`) | max length 80 | — | GST-003, GST-008, WEB-002, WEB-005 | Staff-facing name, e.g. "Water park day planner". |
| Help me choose mode (`guidedChoices.mode`) | Button · Popup on arrival · Off | Button | GST-003, GST-008, WEB-002, WEB-005 | How the guest reaches it (rev 3 REV3-11). `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on … |
| Show banner (`guidedChoices.showBanner`) | — | on | GST-003, GST-008, WEB-002, WEB-005 | The dark banner under the products ("Choose from the experiences above or let us help you decide") with a Help me choose button. |
| Help me choose behaviour (`guidedChoices.behaviour`) | Filter · Recommend | Filter | GST-003, GST-008, WEB-002, WEB-005 | `filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4). |
| Show everything (`guidedChoices.showEverything`) | — | on | GST-003, GST-008, WEB-002, WEB-005 | The "Show everything" link under a filtered list, which clears the answers (W4). |
| Help me choose questions (`guidedChoices.questions`) | at least 1; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | One to four questions (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). |
| Questions: title (`guidedChoices.questions[].title`) | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Questions: kind (`guidedChoices.questions[].kind`) | Choice · Yes no · Age · Level · Certification | Choice | GST-003, GST-008, WEB-002, WEB-005 | What the question asks (decided 29 September, W4). `choice` free answers; `yesNo` two answers (e.g. |
| Questions: sort order (`guidedChoices.questions[].sortOrder`) | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Questions: answers (`guidedChoices.questions[].answers`) | at least 2; at most 4 | — | GST-003, GST-008, WEB-002, WEB-005 | Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11). |
| Answers: title (`guidedChoices.questions[].answers[].title`) | English and Arabic (Arabic right to left) | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Answers: body (`guidedChoices.questions[].answers[].body`) | The one-liner under the title, at most 140 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | The one-liner under the title, at most 140 characters in each language. |
| Answers: icon (`guidedChoices.questions[].answers[].icon`) | max length 40 | — | GST-003, GST-008, WEB-002, WEB-005 | An icon name from the guest app's icon set. |
| Answers: badge (`guidedChoices.questions[].answers[].badge`) | At most 24 characters in each language. | — | GST-003, GST-008, WEB-002, WEB-005 | Optional, e.g. "Best value". |
| Answers: sort order (`guidedChoices.questions[].answers[].sortOrder`) | min 0 | — | GST-003, GST-008, WEB-002, WEB-005 | — |
| Answers: target (`guidedChoices.questions[].answers[].target`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list. |
| Answers: filter (`guidedChoices.questions[].answers[].filter`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | What this answer keeps in the list (decided 29 September, W4). Every field set must hold; answers to different questions are combined with AND. |
| Answers: consent prefill (`guidedChoices.questions[].answers[].consentPrefill`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4). |
| Answers: result (`guidedChoices.questions[].answers[].result`) | — | — | GST-003, GST-008, WEB-002, WEB-005 | The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image. |

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-101` · status **notStarted** · provenance generated
- ADR-0013 *Local-First Point of Sale* (`docs/adr/0013-local-first-point-of-sale.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (28), with its required mark, default, format and its error state (400, 403, 404, 409, 422).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-101?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: What publishing changes, New set-up, Save draft, Publish, Unpublish, Delete draft or dismiss suggestion.
- [ ] Every transition is wired: `CMS-016`, `CMS-102`.
- [ ] Every gated control is gated: `AI_USE`, `PRODUCT_VIEW`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`.
- [ ] The 4 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---



## Reference designs and the trackers for this platform

**P13 reference designs** (from `handoff/design-batches/apps/5-venue-management/README.md`)

- `sources/designs/guest-rev3-29-september/TICVAI Engine Controls Manual.dc.html`: the look of the controls: every configuration control, laid out and explained.
- `sources/designs/guest-rev3-29-september/TICVAI Guest Booking v2.dc.html`: the configuration side panel, for the controls, and the guest booking the live preview shows.
- `sources/designs/TICVAI_White_Label_Guest_App_UI_Reference_1.pdf`: the client's White Label Builder boards.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-037, DI-038, DI-039, DI-040, DI-042, DI-044, DI-045, DI-046, DI-047, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P13 as a whole** (5: 0 open, 5 closed). Open first; a closed row says where it went on 30 September.

- **A47** Advise Qossai/Allam on the Apple/Google Developer account ownership model and a simplified, low-effort app-publishing workflow for white-labelled tenant apps (incl. how to reflect "Powered by TICVAI" branding) *(Pradnya Yeram · Low · Done → 30 Sep: Closed, Done (as recorded earlier) · 24 Sep 2026 · workshop tracker)*
- **A99** Document reusable CMS page components per venue type (seat-map, park-map) and finalise landing-page component-count logic *(Allam / Aishwarya More · Medium · With client → 30 Sep: Closed, Moved to T7 (TICVAI to act) · 20 Aug 2026 · workshop tracker)*
- **A338** Build the real white-label CMS builder (client builds a site in ~30 min) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Sep 2026 · workshop tracker)*
- **C25** Decide the app-store account ownership model for white-labelled tenant apps (TICVAI-owned, Softlabs-owned, or tenant-owned) once Softlabs' guidance is provided *(Qossai · Received → 30 Sep: Closed, Received · workshop tracker)*
- **C31** Provide reusable CMS page-component documentation per venue type (seat-map, park-map and equivalents) *(Allam · Pending → 30 Sep: Closed, Moved to T7 · 20 Aug 2026 · workshop tracker)*

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

### Across P13 Venue CMS

- The config side panel is a reference tool only, not the CMS. The CMS will be step-based and include header/footer, logos and banners. *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W12 Config side panel · DI-1014)*
- Decision: RBAC per role, per module, three levels — edit/view, view-only, hidden (e.g. a marketing officer does not see Finance at all) — plus sub-permissions within a module (a CRM role may get Campaigns and Communications but not Journeys). Default role templates, admin-customisable. *(agreed · MoM 20 Aug 2026, 4.7 Role-Based Access Control (RBAC); 5. Key Decisions · DI-387)*
- Qossai: build AI-assisted site design/generation into the website builder, keeping site design (header, footer, color, font, layout) separate from content (tickets), with tickets flowing into the site's structure once published. To be explored. *(client request · MoM 3 Aug 2026, 7. AI-Assisted Website Generation · DI-115)*
- Qossai: give clients as much design flexibility as possible within the configurable structure. *(client request · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-114)*
- Typeface Inter (Light, Regular, Medium, Semibold, Bold). Scale: H1 32/40 Bold, H2 24/32 Semibold, H3 20/28 Semibold, Body 1 16/24 Regular, Body 2 14/20 Regular, Caption 12/16 Regular. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 2. Typography · DI-047)*
- Palette ("modern, trustworthy and accessible"): Primary #0D6EFD, #00B8FF, #00D4C4, #0B1324; Neutral #F7F9FC, #E5E7EB, #9CA3AF, #4B5563, #1F2937. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 1. Color Palette · DI-046)*
- Tables: titled card with "View all", columns (e.g. Order ID, Customer, Amount, Status), coloured status badges (Paid, Pending, Refunded) and pagination with "Showing 1 to 5 of 245" and page numbers. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Tables · DI-039)*
- Primary button spec: height 40px, padding 12px 24px, radius 8px, Inter 14 Semibold, colour #0D6EFD, width auto. *(agreed · Design Vision Book 29 Jul 2026, 09 Deliverables (p9) - Developer Handoff preview · DI-037)*

### In P13 · White Label

- Font, header/footer (not yet in the current wireframe build), card size and layout are configurable in the mobile app, consistent with the web app's white-labelling approach. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1097)*
- Qossai (rated the CMS prototype ~70%): a client should be able to build a working site "within 30 minutes", easily adding header, footer, fonts and its own images/graphics self-service; Allam: every CMS option must visibly change something and the interface must be intuitive to navigate. *(client request · MoM 24 Sep 2026, 4.8 Guest Web App CMS Prototype — Feedback on Maturity & Scope Expectations · DI-988)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- Base structure (header, footer, layout) is fixed across tenants; logo, colour, font and module visibility (e.g. hide Dining or Retail) are configurable per tenant, and independently for web and mobile (e.g. a different mobile header). *(agreed · MoM 14 Aug 2026, 4. White-Labeling and Customization Boundaries · DI-285)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Modules enabled/disabled per tenant by licence: Ticketing & Booking, Membership, Events, Attractions, Virtual Queue, F&B, Retail, Parking; add-ons (Lost & Found, AI Concierge Chat, multi-language, integrations) toggle the same way and appear automatically as new integrations are built. *(client request · MoM 10 Aug 2026, 4.1 B2C Guest Mobile App — Configuration & Builder Module · DI-193)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*

**14 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"claimCustomDomain": {"method":"POST","path":"/tenant-domains","contract":"white-label","summary":"Claim a domain and get a verification token","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"},
"createConsentQuestion": {"method":"POST","path":"/consent-questions","contract":"marketing-crm","summary":"Define a consent question","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConsentQuestion","responds":"ConsentQuestion"},
"createGuidedChoice": {"method":"POST","path":"/venues/{venueId}/guided-choices","contract":"white-label","summary":"Set up Help me choose for a venue","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuidedChoice","responds":"GuidedChoice"},
"deleteGuidedChoice": {"method":"DELETE","path":"/guided-choices/{guidedChoiceId}","contract":"white-label","summary":"Delete a Help me choose set-up, or dismiss a suggestion","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"diffConfigVersion": {"method":"GET","path":"/tenant-config/versions/{version}/diff","contract":"white-label","summary":"Compare a version against the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"against","in":"query","required":null}],"requestBody":null,"responds":"ConfigDiff"},
"getBookingFlowConfig": {"method":"GET","path":"/tenant-config/booking-flow","contract":"white-label","summary":"How the guest booking flow looks and steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"effectiveForVenueId","in":"query","required":false}],"requestBody":null,"responds":"BookingFlowConfig"},
"getGuidedChoiceSuggestion": {"method":"GET","path":"/guided-choice-suggestions/{suggestionId}","contract":"ai","summary":"The reasons behind a Help me choose suggestion","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"AiGuidedChoiceSuggestion"},
"getTenantAppStatus": {"method":"GET","path":"/tenant-config/status","contract":"white-label","summary":"App status and recent changes","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"TenantAppStatus"},
"getTenantConfig": {"method":"GET","path":"/tenant-config","contract":"white-label","summary":"Full working configuration","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"version","in":"query","required":null}],"requestBody":null,"responds":"TenantConfig"},
"listAnalyticsProviders": {"method":"GET","path":"/tenant-config/analytics-providers","contract":"white-label","summary":"The analytics platforms the storefront and app report to","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listBookingFlows": {"method":"GET","path":"/venues/{venueId}/booking-flows","contract":"white-label","summary":"A venue's booking flows, in the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"flowTypeKey","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConfigVersions": {"method":"GET","path":"/tenant-config/versions","contract":"white-label","summary":"Version history","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentAnswers": {"method":"GET","path":"/consent-answers","contract":"marketing-crm","summary":"The consent records given at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"orderId","in":"query","required":null},{"name":"subjectId","in":"query","required":null},{"name":"questionId","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listConsentQuestions": {"method":"GET","path":"/consent-questions","contract":"marketing-crm","summary":"The consent questions a venue asks at booking","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCustomDomains": {"method":"GET","path":"/tenant-domains","contract":"white-label","summary":"The domains this tenant has claimed","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"CustomDomain"},
"listEvents": {"method":"GET","path":"/events","contract":"catalogue","summary":"List events","permission":"PRODUCT_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuidedChoices": {"method":"GET","path":"/venues/{venueId}/guided-choices","contract":"white-label","summary":"List a venue's Help me choose set-ups","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"status","in":"query","required":null},{"name":"source","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listOrgUnits": {"method":"GET","path":"/org-units","contract":"tenancy","summary":"List scope nodes visible to the session","permission":"SCOPE_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"under","in":"query","required":null},{"name":"level","in":"query","required":null},{"name":"includeInactive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listPolicies": {"method":"GET","path":"/tenant-config/policies","contract":"white-label","summary":"List legal policies","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":"includeHistory","in":"query","required":null},{"name":"kind","in":"query","required":null}],"requestBody":null,"responds":"Policy"},
"listPrincipals": {"method":"GET","path":"/principals","contract":"identity","summary":"List principals","permission":"USER_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"scopePath","in":"query","required":null},{"name":"isActive","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listProductCategories": {"method":"GET","path":"/product-categories","contract":"catalogue","summary":"The merchandise hierarchy — categories, brands, collections","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"ProductCategoryNode"},
"listProducts": {"method":"GET","path":"/products","contract":"catalogue","summary":"List products","permission":"PRODUCT_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"kind","in":"query","required":null},{"name":"isSellable","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"segmentTag","in":"query","required":null},{"name":"guidedAnswerIds","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listRoles": {"method":"GET","path":"/roles","contract":"identity","summary":"List roles","permission":"ROLE_MANAGE","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"publishGuidedChoice": {"method":"POST","path":"/guided-choices/{guidedChoiceId}/publish","contract":"white-label","summary":"Publish a Help me choose set-up to guests","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"publishTenantConfig": {"method":"POST","path":"/tenant-config/publish","contract":"white-label","summary":"Publish the working draft","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigVersion"},
"relinquishCustomDomain": {"method":"DELETE","path":"/tenant-domains/{domainId}","contract":"white-label","summary":"Give the domain up","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"restoreConfigVersion": {"method":"POST","path":"/tenant-config/versions/{version}/restore","contract":"white-label","summary":"Restore a previous version","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TenantConfig"},
"setAnalyticsProvider": {"method":"PUT","path":"/tenant-config/analytics-providers","contract":"white-label","summary":"Connect the storefront and app to an analytics platform","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"StorefrontAnalyticsProvider","responds":"StorefrontAnalyticsProvider"},
"setBookingFlowConfig": {"method":"PUT","path":"/tenant-config/booking-flow","contract":"white-label","summary":"Set how the guest booking flow looks and steps","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"BookingFlowConfig","responds":"BookingFlowConfig"},
"setConsentPurposes": {"method":"PUT","path":"/consent-purposes","contract":"marketing-crm","summary":"Configure consent purposes","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConsentPurposeConfig"},
"setLanguages": {"method":"PUT","path":"/tenant-config/languages","contract":"white-label","summary":"Set enabled languages and default","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"LanguageConfig"},
"setPolicy": {"method":"PUT","path":"/tenant-config/policies/{policyKind}","contract":"white-label","summary":"Publish a policy version","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Policy"},
"setSeoMetadata": {"method":"PUT","path":"/seo-metadata","contract":"marketing-crm","summary":"Titles, descriptions, canonicals and hreflang","permission":"MARKETING_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"SeoMetadata","responds":"SeoMetadata"},
"suggestGuidedChoice": {"method":"POST","path":"/venues/{venueId}/guided-choice-suggestions","contract":"ai","summary":"Suggest a Help me choose set-up from the venue's catalogue","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"unpublishGuidedChoice": {"method":"POST","path":"/guided-choices/{guidedChoiceId}/unpublish","contract":"white-label","summary":"Take a Help me choose set-up off the guest app","permission":"TENANT_PUBLISH","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"updateConsentQuestion": {"method":"PATCH","path":"/consent-questions/{questionId}","contract":"marketing-crm","summary":"Reword, re-scope or retire a consent question","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ConsentQuestion","responds":"ConsentQuestion"},
"updateGuidedChoice": {"method":"PATCH","path":"/guided-choices/{guidedChoiceId}","contract":"white-label","summary":"Edit a Help me choose set-up, or review a suggestion","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuidedChoice"},
"validateTenantConfig": {"method":"POST","path":"/tenant-config/validate","contract":"white-label","summary":"Validate the working draft","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"ConfigValidationReport"},
"verifyCustomDomain": {"method":"POST","path":"/tenant-domains/{domainId}/verify","contract":"white-label","summary":"Check the record and issue the certificate","permission":"TENANT_CONFIGURE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CustomDomain"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"AccessibilitySettings": {"type":"object","description":"BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n","properties":{"largeTextAvailable":{"type":"boolean","default":true},"highContrastAvailable":{"type":"boolean","default":true},"simplifiedNavigationAvailable":{"type":"boolean","default":true},"screenReaderSupported":{"type":"boolean","default":true},"reachableHeightModeAvailable":{"type":"boolean","default":false,"description":"**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"},"sessionTimeoutMultiplier":{"type":"number","default":1,"description":"**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"}}},
"AiGuidedChoiceSuggestion": {"type":"object","x-ticvai-persistence":"ai.guided_choice_suggestion","description":"**One Help me choose suggestion for a venue** (design 3.11, decided 29 September; C7 at autonomy \"suggest\"). Holds the reasons: the products read, the one or two attributes chosen, the split each makes, the answer mapping and where the wording came from. Its `id` is the `suggestionRef` on the white-label draft (`white-label.proposeGuidedChoice`). Nothing is ever published from here.","required":["venueId","trigger","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid"},"trigger":{"type":"string","enum":["productsUploaded","mappedProductWithdrawn","productsUncovered","manual"]},"status":{"type":"string","enum":["running","proposed","noSuggestion","failed","superseded"],"readOnly":true},"productCount":{"type":"integer","minimum":0,"readOnly":true},"questions":{"type":"array","items":{"type":"object","properties":{"attribute":{"type":"string","description":"The catalogue attribute asked about: audience, level, minimum height or age, duration, price band, format, language."},"order":{"type":"integer","minimum":1},"split":{"type":"object","additionalProperties":true,"description":"How evenly it divides the bookable products: products per answer."},"droppedBecause":{"type":"string","nullable":true,"description":"Set where an attribute was considered and dropped (an answer would leave nothing bookable)."},"answers":{"type":"array","items":{"type":"object","properties":{"value":{"type":"string"},"leadsTo":{"type":"string","enum":["product","category","flow"]},"targetRef":{"type":"string"}}}}}},"readOnly":true,"description":"The questions chosen, in the order asked. Deterministic: the same catalogue gives the same questions."},"wordingSource":{"type":"string","enum":["model","attributeNames"],"readOnly":true,"description":"Where the text came from. `attributeNames` when no model was available: the rules alone still make a usable draft."},"modelVersion":{"type":"string","nullable":true,"readOnly":true},"promptTemplateVersion":{"type":"string","nullable":true,"readOnly":true},"guidedChoiceId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The white-label draft `GuidedChoice` it produced."},"decisionRecordId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"createdAt":{"type":"string","format":"date-time","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."}}},
"AppAvailability": {"type":"string","description":"**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n","enum":["open","soldOut","closed"],"default":"open"},
"AppIcons": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["sourceAssetRef","changeScope"],"properties":{"sourceAssetRef":{"type":"string","format":"uuid","description":"The `MediaAsset` id of the 1024×1024 source."},"derived":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).","items":{"type":"object","properties":{"platform":{"type":"string","enum":["ios","android","web"]},"size":{"type":"string"},"assetRef":{"type":"string","format":"uuid"}}}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` — icons are baked into the binary."},"liveVersion":{"type":"string","nullable":true,"readOnly":true,"description":"Icon currently shipped. Differs from the draft until the next release."},"requiresRebuild":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onRead","description":"True while the draft's source differs from the icon in `liveVersion`."}}},
"BookingConsentRecord": {"type":"object","x-ticvai-persistence":"marketing.booking_consent_record","description":"**One answer to one consent question, as given** (decided 29 September, rev 3 REV3-26). Append-only: a changed answer is a new record and this one gets `supersededAt`. Distinct from `ConsentRecord`, which is a guest's standing decision about a data-processing purpose; this is an answer given for a booking.\n","required":["id","questionId","questionVersion","questionKind","answer","scope","source","answeredAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"questionId":{"type":"string","format":"uuid"},"questionVersion":{"type":"integer","minimum":1},"questionKind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"answer":{"type":"string","enum":["yes","no"]},"scope":{"type":"string","enum":["perPerson","perBooking"]},"blocksBooking":{"type":"boolean","readOnly":true,"description":"The answer is the question's `blockingAnswer` at that version."},"cartId":{"type":"string","format":"uuid","nullable":true},"cartLineId":{"type":"string","format":"uuid","nullable":true},"orderId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Set by `orders.checkoutCart` when the cart becomes an order."},"orderLineId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"personIndex":{"type":"integer","minimum":0,"nullable":true},"personName":{"type":"string","maxLength":120,"nullable":true},"personSubjectId":{"type":"string","format":"uuid","nullable":true},"answeredBySubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The guest who answered, from the session. Null for an anonymous cart."},"answeredByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The staff member who answered on the guest's behalf."},"source":{"$ref":"#/components/schemas/ConsentSource"},"answeredAt":{"type":"string","format":"date-time"},"supersededAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."}}},
"BookingFlow": {"x-ticvai-persistence":"whitelabel.booking_flow","type":"object","description":"**A venue's booking flow (decided 29 September, W12: operators pick their flows, see which steps are required, set their own order).** Made from a `BookingFlowType`; lives in the working draft and reaches guests with `publishTenantConfig`, which copies the venue's flows into the version's snapshot. A product or category names its flow (catalogue `bookingFlowId`); otherwise the venue's default for the type serving its kind applies.\n","required":["flowTypeKey","name"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createBookingFlowDefinition`."},"flowTypeKey":{"$ref":"#/components/schemas/BookingFlowTypeKey"},"name":{"type":"string","maxLength":80,"description":"Staff-facing, e.g. \"Day pass, date first\". Not shown to guests."},"isDefaultForType":{"type":"boolean","default":false,"description":"At most one per venue and type; setting it takes it from the previous default."},"isEnabled":{"type":"boolean","default":true,"description":"A disabled flow is kept and not published; products naming it fall back to the default."},"steps":{"type":"array","maxItems":30,"description":"Every step of the type, in the venue's order. Filled from the type when left out on create.","items":{"$ref":"#/components/schemas/BookingFlowStep"}},"settings":{"$ref":"#/components/schemas/BookingFlowLevelSettings"},"isValid":{"type":"boolean","readOnly":true,"x-ticvai-derived":"onWrite","description":"Whether the flow passes `validateBookingFlow`; worked out in the same transaction as each write. `publishTenantConfig` refuses a draft holding an invalid enabled flow."},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005). Written at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"BookingFlowConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","description":"**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n","allOf":[{"$ref":"#/components/schemas/BookingFlowSettings"},{"type":"object","properties":{"venueOverrides":{"type":"array","maxItems":200,"default":[],"description":"Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.","items":{"$ref":"#/components/schemas/BookingFlowVenueOverride"}}}}]},
"BookingFlowLevelSettings": {"x-ticvai-persistence":"none — jsonb column on whitelabel.booking_flow","type":"object","description":"**The settings that belong to one flow, not to the venue (decided 29 September, W12).** Moved here from `BookingFlowSettings`, which keeps the venue-wide ones. Each keeps its rev 3 meaning and default. A field left out takes its default.\n","properties":{"performanceReveal":{"type":"string","enum":["dateTimeTicket","allAtOnce"],"default":"dateTimeTicket","description":"**Performance reveal (rev 3 REV3-2).** `dateTimeTicket` shows the times only once a date is picked and the tickets only once a time is picked; `allAtOnce` shows them together. Product-first (W8) is the step order of `experienceWorkshop`, not a value here.\n"},"signInAt":{"type":"string","enum":["afterAddOns","atPayment"],"default":"afterAddOns","description":"**Where the guest is asked to sign in, or for a guest-checkout code (rev 3 REV3-3).** `afterAddOns` asks as the guest leaves the extras step; `atPayment` asks at payment. The basket is kept either way.\n"},"seatEventDateMode":{"type":"string","enum":["inlineStep","popupOnSeatMap"],"default":"inlineStep","description":"**Date and time on a seated event (rev 3 REV3-4).** `inlineStep` asks for them before the seat map; `popupOnSeatMap` opens the seat map with a date and time pop-up. Read only by the seated flow types.\n"},"extrasStep":{"type":"string","enum":["auto","always","never"],"default":"auto","description":"`auto` shows the extras step only when the cart's products have add-ons; `never` is the same as turning the optional `extras` step off."},"quickTour":{"type":"boolean","default":false,"description":"**Quick tour (rev 3 REV3-20).** A first visit gets a coach-mark tour of this flow's steps, replayable from a Quick tour button. Seen-state kept on the device only.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"default":[],"description":"**The flow's own consent questions (rev 3 REV3-26).** Asked on every booking through this flow, together with those of each product in the cart, each question once. Each id names an active `ConsentQuestion` of the tenant in marketing-crm, or 400. A Help me choose answer may pre-fill one (`GuidedChoice` `consentPrefill`); the guest still confirms it.\n","items":{"type":"string","format":"uuid"}}}},
"BookingFlowSettings": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**Every guest booking-flow setting, once.** `BookingFlowConfig` is these at tenant level plus `venueOverrides`; a `BookingFlowVenueOverride` carries any subset of them for one venue (decided 29 September, rev 3 CFG-11). The Rev 3 settings (`timesPerPage` onwards) are the options the client's rev 3 prototype shows under Config → Booking rules and Build your experience.\n**Venue-wide only (decided 29 September, W12).** The settings that belong to one flow moved to `BookingFlowLevelSettings` on each `BookingFlow`; `categoryDisplay` was removed (W7).\n","properties":{"preset":{"type":"string","enum":["auto","ticketBox","playCentre","venueSite","marketplace","singleEvent","season","custom"],"default":"auto","description":"L1 Ticket box … L6 Season. `auto` picks by venue type; `custom` applies none. The UI preset of the prototype's drawer (rev 3 CFG-1, no change)."},"stepIndicator":{"type":"string","enum":["bar","numbered","dots","segmented","breadcrumb","pills","ticks","none"],"default":"bar"},"cartLayout":{"type":"string","enum":["sidebarRight","sidebarLeft","slideInRight","slideUpBottom","singleColumn","floatingIcon"],"default":"sidebarRight","description":"`floatingIcon` is a round basket button with the item count that opens the cart (decided 29 September, rev 3 REV3-10). Which side a sidebar or the icon sits on in a right-to-left language is `cartSideInRtl`."},"cartSideInRtl":{"type":"string","enum":["keepRight","mirror"],"default":"keepRight","description":"**The cart side when the guest reads Arabic or another right-to-left language (decided 29 September, rev 3 REV3-10).** `keepRight` keeps the cart (and the floating icon) on the right, as the client confirmed; `mirror` flips it to the left with the rest of the layout.\n"},"cardLayout":{"type":"string","enum":["stackedRows","splitRows","cardsAcross","posterCards"],"default":"stackedRows","description":"How ticket and product cards are laid out (decided 29 September, rev 3 DG-6). Was a free string; the four values are the design's Stacked rows, Split rows, Cards across and Poster cards."},"cardSize":{"type":"string","enum":["compact","standard","large","extraLarge"],"default":"compact","description":"Labels Compact, Standard, Large, Extra large (decided 29 September, rev 3 DG-6). `standard` replaces `regular`."},"seatPicker":{"type":"string","enum":["bowl","zonesThenSeats","zonesOnly","seatsOnly"],"default":"bowl","description":"Default `bowl`, as the prototype has it (decided 29 September, rev 3 CFG-6). Read only for a seated event."},"mapView":{"type":"string","enum":["2d","3d"],"default":"3d"},"density":{"type":"string","enum":["compact","standard","roomy"],"default":"compact","description":"Labels Compact, Standard, Roomy, default Compact as the design has it (decided 29 September, rev 3 DG-6). `standard` and `roomy` replace `comfortable` and `airy`."},"embedMode":{"type":"string","enum":["fullPage","embedded"],"default":"fullPage","description":"`embedded` hides the hero banner, event page and venue header, for a flow placed inside the venue's own site."},"heroBanner":{"type":"boolean","default":true},"searchInBanner":{"type":"boolean","default":false,"description":"Off by default, as the prototype has it (decided 29 September, rev 3 CFG-6)."},"eventBannerDates":{"type":"boolean","default":false,"description":"**Dates in event banner (decided 29 September, rev 3 23SEP-19).** On, the event banner lists the next dates; off by default. Either way the date picker sits at the top of the booking step.\n"},"singleEventPage":{"type":"boolean","default":false},"quantitiesOnAddOns":{"type":"boolean","default":true},"timesPerPage":{"type":"string","enum":["8","12","24","all"],"default":"24","description":"**Times per page (decided 29 September, rev 3 REV3-1).** When an event has more performances on the chosen day than fit, WEB-006 and GST-007 show them as compact tiles paged this many at a time with Earlier and Later; `all` shows every one. A string because `all` is one of the values.\n"},"dayPartFilter":{"type":"boolean","default":true,"description":"**Morning, afternoon and evening chips with counts above the times (decided 29 September, rev 3 REV3-1).** Where each part begins is `dayPartBoundaries`.\n"},"dayPartBoundaries":{"type":"object","description":"**Where the day parts divide, in the venue's time zone (decided 29 September, rev 3 REV3-1).** Morning is before `afternoonStartsAt`, afternoon runs to `eveningStartsAt`, evening is from `eveningStartsAt`. A venue sets its own through `venueOverrides`. `afternoonStartsAt` must be earlier than `eveningStartsAt`, or 400.\n","properties":{"afternoonStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"12:00"},"eveningStartsAt":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$","default":"17:00"}}},"seatViewPosition":{"type":"string","enum":["bottom","right","left","top"],"default":"bottom","description":"**Where the view-from-your-seat box sits around the seat map (decided 29 September, rev 3 REV3-5).** Web only; on mobile and on a narrow screen it is always below the map.\n"},"seatTimeBar":{"type":"boolean","default":true,"description":"**Time bar above the seat map (decided 29 September, rev 3 REV3-6).** Shows the chosen performance and lets the guest switch performance or change the date; switching releases the seats held for the previous one.\n"},"ticketCategories":{"type":"string","enum":["categoryThenSubcategory","flatList"],"default":"categoryThenSubcategory","description":"**How tickets are grouped (decided 29 September, rev 3 REV3-16).** `categoryThenSubcategory` shows the venue's top product categories as tiles, then the tickets in the chosen one; `flatList` lists every ticket at once.\n"},"ticketTags":{"type":"boolean","default":true,"description":"**Tags on tickets (decided 29 September, rev 3 23SEP-3).** Shows a product's display tags (such as \"2 Hours\", \"Min 1.10 m\", \"Valid 90 days\") on its card.\n"},"cardInfo":{"type":"boolean","default":true,"description":"**Extra info on cards (decided 29 September, rev 3 23SEP-6).** Shows each ticket type's description, who it is for and what it includes, under its name.\n"},"conciergeMascot":{"type":"boolean","default":true,"description":"**The concierge as mascot art or a plain button (decided 29 September, rev 3 CFG-5).** Read only where the `aiConciergeChat` feature is on.\n"},"showInfoOnly":{"type":"boolean","default":true,"description":"**Show info-only products (decided 29 September, rev 3 REV3-14).** On, a product with `guestListing` `infoOnly` (catalogue) is listed with its not-bookable label and opens its details; off, guests are not shown it.\n"},"locationSwitcher":{"type":"boolean","default":false,"description":"**Location switcher (decided 29 September, rev 3 REV3-18).** On, the booking screens carry a \"Booking at\" bar with Change location, reusing the guest's venue choice (audit R267). Off unless the tenant or venue enables it; it has no effect for a tenant with one venue.\n"},"guestContactFields":{"type":"array","minItems":1,"maxItems":3,"uniqueItems":true,"default":["email"],"items":{"type":"string","enum":["email","mobile","name"]},"description":"**What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1).** The prototype's Email only, + name and + mobile. Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.matchBy`), or 400. After the code is verified the guest is not asked for these again: the flow goes to the terms and payment, and the profile is completed later (WEB-020, GST-039). Read only where the `guestCheckout` feature is on.\n"},"dateStripDays":{"type":"integer","minimum":3,"maximum":31,"default":7,"description":"**The date strip (decided 17 September, M17-08).** How many days from today the date step shows as a strip before the calendar icon that opens the full month; later dates are picked from the calendar.\n"}}},
"BookingFlowStep": {"x-ticvai-persistence":"whitelabel.booking_flow_step","type":"object","description":"One step of a venue's flow, in the venue's order (decided 29 September, W12).","required":["stepKey","enabled","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"bookingFlowId":{"type":"string","format":"uuid","readOnly":true},"stepKey":{"$ref":"#/components/schemas/BookingFlowStepKey"},"enabled":{"type":"boolean","description":"A `required` step cannot be off; the flow saves and `isValid` turns false."},"sortOrder":{"type":"integer","minimum":0},"requirement":{"type":"string","enum":["required","optional","conditional"],"readOnly":true,"x-ticvai-derived":"onRead","description":"From the flow type, so the CMS can mark the step without a second read."},"settings":{"type":"object","additionalProperties":true,"default":{},"description":"The step's own settings, by the names the type's `stepSettings` gives for this step (e.g. `languages` on `language`, `minHours` on `duration`). A name the type does not give is refused with 400."}}},
"BookingFlowTypeKey": {"type":"string","description":"**The flow types the system catalogue offers (decided 29 September, W12; impact.md b).** `seatedFixedPerformance` and `seatedDateTimeSeatMap` are the two seated flows; `cabanaMap` and `cabanaBySize` are the two cabana flows (W6); `experienceWorkshop` puts the product before the date (W8); `multiLocation` opens on the location switcher.\n","enum":["datedDayPass","timedEntry","openDated","seatedFixedPerformance","seatedDateTimeSeatMap","experienceWorkshop","surfSession","meetingRoomHourly","cabanaMap","cabanaBySize","guidedTourByLanguage","transport","tableReservation","membership","giftCard","multiLocation"]},
"BookingFlowVenueOverride": {"type":"object","x-ticvai-persistence":"none — embedded in tenant_config","description":"**One venue's booking-flow settings where they differ from the tenant's (decided 29 September, rev 3 CFG-11).** `settings` carries only the fields the venue changes; a field left out inherits the tenant value, and the schema defaults do not apply inside an override.\n","required":["venueId","settings"],"properties":{"venueId":{"type":"string","format":"uuid","description":"One of the tenant's active venues. At most one override per venue."},"settings":{"$ref":"#/components/schemas/BookingFlowSettings"}}},
"BrandIdentity": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","description":"Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n","required":["logoAssetRef"],"properties":{"logoAssetRef":{"type":"string","format":"uuid","description":"The primary logo."},"logoDarkAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"Used on dark backgrounds. Falls back to the primary logo."},"logoVariant":{"type":"string","enum":["light","dark","duotone"],"default":"light","description":"**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"},"faviconAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"The browser tab icon for the guest web app."},"splashImageAssetRefs":{"type":"array","description":"Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).","items":{"type":"string","format":"uuid"}},"splashDurationSeconds":{"type":"integer","minimum":0,"maximum":10,"default":3},"splashBackgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"showLoadingIndicator":{"type":"boolean","default":true},"splashChangeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."},"introVideoAssetRef":{"type":"string","format":"uuid","nullable":true,"description":"**The optional intro video (decided 29 September, MOB-5).** A video `MediaAsset` from the media library (CMS-010). Streamed, so a change reaches guests with the publish and needs no app build.\n"},"introVideoMode":{"type":"string","enum":["off","firstLaunch","everyLaunch"],"default":"off","description":"When GST-001 plays it full screen. \"Skip introduction\" is always shown. Anything but `off` needs `introVideoAssetRef`, or 400."}}},
"ChangeScope": {"type":"string","description":"Whether a change reaches guests on publish or needs a store release.\n","enum":["runtime","buildTime"]},
"Channel": {"type":"string","enum":["pos","kiosk","web","mobile","b2b","ota","callCentre"]},
"ConfigDiff": {"x-ticvai-persistence":"none — computed","type":"object","required":["fromVersion","toVersion","changes"],"properties":{"fromVersion":{"type":"string"},"toVersion":{"type":"string"},"changes":{"type":"array","items":{"type":"object","required":["area","path","changeKind"],"properties":{"area":{"type":"string"},"path":{"type":"string"},"changeKind":{"type":"string","enum":["added","removed","modified"]},"before":{"type":"string","nullable":true},"after":{"type":"string","nullable":true},"changeScope":{"$ref":"#/components/schemas/ChangeScope"}}}}}},
"ConfigFindingKind": {"type":"string","enum":["missingTranslation","navigationTargetsDisabledModule","homepageReferencesMissingContent","contrastFailure","missingRequiredAsset","policyVersionMissing","noVisibleNavigationItems","unlicensedModuleEnabled","arabicFontMissing","bookingFlowInvalid","bookingFlowMissing"]},
"ConfigValidationReport": {"x-ticvai-persistence":"none — computed","type":"object","required":["passed","errorCount","warningCount","findings"],"properties":{"passed":{"type":"boolean"},"errorCount":{"type":"integer"},"warningCount":{"type":"integer"},"findings":{"type":"array","items":{"type":"object","required":["kind","severity","message"],"properties":{"kind":{"$ref":"#/components/schemas/ConfigFindingKind"},"severity":{"type":"string","enum":["error","warning"]},"message":{"type":"string"},"area":{"type":"string"},"reference":{"type":"string","nullable":true}}}}}},
"ConfigVersion": {"x-ticvai-persistence":"whitelabel.config_version","type":"object","required":["version","publishedAt","publishedByPrincipalId","note","isCurrent"],"properties":{"version":{"type":"string"},"publishedAt":{"type":"string","format":"date-time"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedByName":{"type":"string"},"note":{"type":"string"},"isCurrent":{"type":"boolean"},"scheduledFor":{"type":"string","format":"date-time","nullable":true},"contentHash":{"type":"string"},"pendingBuildTimeChanges":{"type":"array","description":"Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"platforms":{"type":"array","items":{"type":"string","enum":["ios","android","web"]}}}}},"snapshot":{"type":"object","additionalProperties":true,"readOnly":true,"description":"**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentQuestion": {"type":"object","x-ticvai-persistence":"marketing.consent_question + marketing.consent_question_version","description":"**A venue-defined consent question asked at booking** (decided 29 September, rev 3 REV3-26). Each version's text is kept in `consent_question_version`, so an answer always points at the exact words the guest saw. Attached to products by the catalogue and to booking flows by the white-label flow configuration; one or several per flow, as the venue chooses.\n","required":["id","kind","text","version","scope","required","blockingAnswer","status"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"kind":{"$ref":"#/components/schemas/ConsentQuestionKind"},"text":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The question as the guest reads it, per locale."},"helpText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"version":{"type":"integer","minimum":1,"readOnly":true,"description":"Raised by one each time the question changes (`updateConsentQuestion`)."},"scope":{"type":"string","enum":["perPerson","perBooking"],"default":"perPerson","description":"Asked for each declared person, or once for the whole booking."},"required":{"type":"boolean","default":true,"description":"Checkout waits until it is answered (`orders.checkoutCart` 422 `consentRequired`)."},"blockingAnswer":{"type":"string","enum":["yes","no","none"],"default":"none","description":"The answer that stops the booking, for the person or the booking it covers. `none` records the answer and blocks nothing."},"status":{"type":"string","enum":["active","retired"],"default":"active"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Operations write it at `venue` scope."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"ConsentQuestionKind": {"type":"string","description":"What the question is about (decided 29 September, rev 3 REV3-26). `swim` feeds the derived `confidentSwimmer` on the order line; the others are recorded and checked as the venue set them.","enum":["swim","scuba","risk","custom"]},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"CustomDomain": {"type":"object","x-ticvai-persistence":"whitelabel.custom_domain","description":"24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n","required":["id","tenantId","hostname","status"],"properties":{"id":{"type":"string","format":"uuid"},"tenantId":{"type":"string","format":"uuid"},"hostname":{"type":"string"},"kind":{"type":"string","enum":["guestWeb","guestApp","partnerPortal","developerPortal"]},"status":{"type":"string","enum":["pending","verifying","verified","issuing","active","failed","expired","revoked"]},"verificationMethod":{"type":"string","enum":["dnsTxt","cname","httpFile"]},"verificationToken":{"type":"string","readOnly":true},"verificationRecord":{"type":"object","readOnly":true,"description":"**The record the tenant must publish**, which `claimCustomDomain` promises and the claim had nowhere to hold. Set when the claim is made, from `hostname`, `verificationMethod` and `verificationToken`: a TXT record for `dnsTxt`, a CNAME for `cname`, and for `httpFile` the URL path to serve and the file's content.\n","required":["type","name","value"],"properties":{"type":{"type":"string","enum":["TXT","CNAME","httpFile"]},"name":{"type":"string","description":"The DNS name to create, or for `httpFile` the URL path on `hostname`."},"value":{"type":"string","description":"The record's value, CNAME target or file content."}}},"certificateExpiresAt":{"type":"string","format":"date-time","nullable":true,"description":"**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"},"lastCheckedAt":{"type":"string","format":"date-time","nullable":true},"failureReason":{"type":"string","nullable":true}}},
"Event": {"x-ticvai-persistence":"catalogue.event","type":"object","required":["id","code","name","venueId","scopePath"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"parentEventId":{"type":"string","format":"uuid","nullable":true,"description":"For grouped events."},"performanceCount":{"type":"integer","readOnly":true,"description":"How many performances the event has. Counted by the server; never sent by a client."},"isActive":{"type":"boolean"}}},
"FeatureToggle": {"x-ticvai-persistence":"whitelabel.feature_toggle","type":"object","required":["featureKey","isEnabled","changeScope"],"properties":{"featureKey":{"allOf":[{"$ref":"#/components/schemas/FeatureKey"}],"description":"`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"},"displayName":{"type":"string"},"isEnabled":{"type":"boolean"},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"description":"Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"},"requiresConfiguration":{"type":"boolean","description":"True where the feature needs credentials or setup elsewhere first."}}},
"FontConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryLatin"],"properties":{"primaryLatin":{"type":"string"},"primaryArabic":{"type":"string","nullable":true,"description":"Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"},"secondaryLatin":{"type":"string","nullable":true},"secondaryArabic":{"type":"string","nullable":true,"description":"Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."},"customFontAssetRefs":{"type":"array","description":"Uploaded font files, as `MediaAsset` ids.","items":{"type":"string","format":"uuid"}},"changeScope":{"allOf":[{"$ref":"#/components/schemas/ChangeScope"}],"readOnly":true,"x-ticvai-derived":"onRead","description":"Custom font files are `buildTime`; selecting a bundled face is `runtime`."}}},
"FooterConfig": {"type":"object","x-ticvai-persistence":"whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link","description":"BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n","required":["id","scopePath"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"scopePath":{"type":"string","readOnly":true,"description":"The partition key (ADR-0005), written at `tenant` scope by the server."},"columns":{"type":"array","items":{"type":"object","properties":{"heading":{"type":"string"},"links":{"type":"array","items":{"type":"object","properties":{"label":{"type":"string"},"url":{"type":"string"},"opensCookiePreferences":{"type":"boolean","default":false}}}}}}},"legalLinks":{"type":"object","description":"**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n","properties":{"termsUrl":{"type":"string"},"privacyUrl":{"type":"string"},"accessibilityUrl":{"type":"string","nullable":true},"cookiePolicyUrl":{"type":"string","nullable":true}}},"copyrightText":{"type":"string"},"socialLinks":{"type":"array","items":{"type":"object","properties":{"platform":{"type":"string"},"url":{"type":"string"}}}}}},
"GuestListing": {"type":"string","enum":["bookable","infoOnly","hidden"],"default":"bookable","description":"**How a product appears to a guest** (decided 29 September, rev 3 REV3-14). `bookable`: listed and searched while it is on sale, and added to the basket. `infoOnly`: listed and searched with its details, photo and `notBookableLabel` whether or not it is on sale, and **never added to a basket** (`addCartLine` refuses it with `409`); the screen opens its details instead. `hidden`: never listed or searched for a guest, and reachable only where a staff channel sells it. Independent of `isSellable`, which says whether a channel may sell it at all.\n"},
"GuidedChoice": {"x-ticvai-persistence":"whitelabel.guided_choice + whitelabel.guided_choice_question + whitelabel.guided_choice_answer","type":"object","description":"**Help me choose (decided 29 September, rev 3 REV3-11).** A venue's short set of questions that ends on a result card opening the booking flow, product, category or event that fits. Each question has a few answers with a title, a one-line body, an icon and an optional badge; **the answer the guest picks on the last question decides the result**, and each earlier answer carries a target too, so a one-question setting still ends on a result. Venue configuration, never hard-coded: set up in Venue Management, off unless the venue publishes one.\n**Two sources, one review.** `manual` is written by staff; `aiSuggested` is proposed by the `ai` service from the venue's uploaded products (a suggestion, reviewed and published by a person, never auto-published). Both arrive as `draft`.\n**Help me choose filters the catalogue (decided 29 September, W4).** With `behaviour` `filter`, the default, each answer's `filter` narrows the products the guest sees (web, mobile and kiosk alike, through catalogue `listProducts` and `searchCatalogue` `guidedAnswerIds`), with a \"Show everything\" link; `recommend` keeps the rev 3 result card from the last answer's `target`. **It is never a consent step**: an answer may pre-fill a REV3-26 consent question (`consentPrefill`), which the guest still confirms, so the question is not asked twice and the consent stays explicit.\n","required":["id","venueId","name","mode","questions","status","source"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"From the path of `createGuidedChoice`."},"name":{"type":"string","maxLength":80,"description":"Staff-facing name, e.g. \"Water park day planner\". Not shown to guests."},"mode":{"type":"string","enum":["button","popupOnArrival","off"],"default":"button","description":"**How the guest reaches it (rev 3 REV3-11).** `button` puts a Help me choose button on the booking page; `popupOnArrival` also opens it once on the guest's first arrival at the booking page (whether it was seen is kept on the device only); `off` keeps a published choice configured but not shown.\n"},"showBanner":{"type":"boolean","default":true,"description":"The dark banner under the products (\"Choose from the experiences above or let us help you decide\") with a Help me choose button. Ignored when `mode` is `off`."},"behaviour":{"type":"string","enum":["filter","recommend"],"default":"filter","description":"**`filter` (default) narrows the list; `recommend` ends on one result card (decided 29 September, W4).** With `filter`, every answer needs a `filter` and `target` is optional; with `recommend`, every answer on the last question needs a `target`. `publishGuidedChoice` refuses the other case with 422.\n"},"showEverything":{"type":"boolean","default":true,"description":"The \"Show everything\" link under a filtered list, which clears the answers (W4)."},"questions":{"type":"array","minItems":1,"maxItems":4,"description":"**One to four questions** (decided 29 September, W4: the Deep Dive reference asks three or four; rev 3 REV3-11 allowed two). Shown in `sortOrder`.\n","items":{"type":"object","required":["title","sortOrder","answers"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"kind":{"type":"string","enum":["choice","yesNo","age","level","certification"],"default":"choice","description":"**What the question asks (decided 29 September, W4).** `choice` free answers; `yesNo` two answers (e.g. \"Can everyone swim?\"); `age` answers carrying an age range; `level` answers carrying a level tag; `certification` answers saying whether the guest holds a certificate (e.g. a diving licence). The kind decides which `filter` fields its answers use.\n"},"sortOrder":{"type":"integer","minimum":0},"answers":{"type":"array","minItems":2,"maxItems":4,"description":"Two to four answers; the prototype shows three (proposed, client to correct, rev 3 REV3-11).","items":{"type":"object","required":["title","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"UUIDv7. The row's own key."},"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"The one-liner under the title, at most 140 characters in each language."},"icon":{"type":"string","maxLength":40,"nullable":true,"description":"An icon name from the guest app's icon set."},"badge":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Optional, e.g. \"Best value\". At most 24 characters in each language."},"sortOrder":{"type":"integer","minimum":0},"target":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceTarget"}],"nullable":true,"description":"Required with `behaviour` `recommend` on the last question; optional with `filter`, where it is the card shown above the filtered list."},"filter":{"type":"object","nullable":true,"description":"**What this answer keeps in the list (decided 29 September, W4).** Every field set must hold; answers to different questions are combined with AND. Required with `behaviour` `filter`. The server applies it (catalogue `guidedAnswerIds`), so web, mobile and kiosk show the same list.\n","properties":{"productIds":{"type":"array","items":{"type":"string","format":"uuid"}},"productCategoryIds":{"type":"array","items":{"type":"string","format":"uuid"}},"segmentTags":{"type":"array","description":"Catalogue `Product.segmentTags`, e.g. a level tag.","items":{"type":"string"}},"minAgeYears":{"type":"integer","minimum":0,"nullable":true},"maxAgeYears":{"type":"integer","minimum":0,"nullable":true,"description":"With `minAgeYears`, checked against each product's age rule (catalogue `ProductEligibilityRule`)."},"requiresSwimmer":{"type":"boolean","nullable":true,"description":"False hides products whose eligibility needs a swimmer; true keeps only those."},"certificationCode":{"type":"string","nullable":true,"maxLength":40,"description":"Keeps products that need this certificate, or with `holdsCertification` false, hides them."},"holdsCertification":{"type":"boolean","nullable":true}}},"consentPrefill":{"type":"object","nullable":true,"description":"**Pre-fills a REV3-26 consent question from this answer (decided 29 September, W4).** The guest still ticks it at the consent step; nothing is recorded as consent until they do.\n","required":["consentQuestionId","answer"],"properties":{"consentQuestionId":{"type":"string","format":"uuid"},"answer":{"type":"boolean"}}},"result":{"type":"object","nullable":true,"description":"The result card when this answer decides the result. Absent fields fall back to the target's own name, summary and image.","properties":{"title":{"$ref":"#/components/schemas/LocalisedText"},"body":{"$ref":"#/components/schemas/LocalisedText"},"imageAssetRef":{"type":"string","format":"uuid","nullable":true}}}}}}}}},"status":{"allOf":[{"$ref":"#/components/schemas/GuidedChoiceStatus"}],"readOnly":true},"source":{"type":"string","enum":["manual","aiSuggested"],"readOnly":true,"description":"`manual` when staff created it; `aiSuggested` when the `ai` service proposed it (a service caller). Kept after a person edits a suggestion, so a report can say how many AI proposals were published."},"suggestionRef":{"type":"string","nullable":true,"readOnly":true,"description":"For `aiSuggested`, the id of the `ai` job that proposed it. Null for `manual`."},"publishedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"publishedBy":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The person who published it. Never a service."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuidedChoiceStatus": {"type":"string","description":"**Draft until a person publishes it (decided 29 September, rev 3 REV3-11).** Guests see only a `published` choice. An AI-proposed choice arrives as `draft` and is never published by the system. Moves as `states/guided-choice.yaml` says: `publishGuidedChoice` and `unpublishGuidedChoice`, and a publish returns the venue's previously published choice to `draft`.\n","enum":["draft","published"],"default":"draft"},
"GuidedChoiceTarget": {"x-ticvai-persistence":"none — embedded","type":"object","description":"**What an answer opens (decided 29 September, rev 3 REV3-11).** A product (its kind picks the booking flow), a product category (its tickets, as `ticketCategories` shows them), an event, or a module such as `membership`. Each id must belong to the choice's venue and be on sale or enabled when the choice is published, or `publishGuidedChoice` refuses it.\n","required":["kind"],"properties":{"kind":{"type":"string","enum":["product","productCategory","event","module","bookingFlow"]},"productId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `product`. A catalogue `Product`."},"productCategoryId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `productCategory`. A catalogue `ProductCategory`."},"eventId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `event`."},"moduleKey":{"allOf":[{"$ref":"#/components/schemas/ModuleKey"}],"nullable":true,"description":"Required when `kind` is `module`. The module must be enabled."},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"Required when `kind` is `bookingFlow` (decided 29 September, W12; BUILD-YOUR-EXPERIENCE \"each answer points to one booking flow\"). One of the venue's enabled `BookingFlow`s."}}},
"HeaderConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["layout"],"properties":{"layout":{"type":"string","enum":["logoLeft","logoCentre","logoWithMenu"]},"showLogo":{"type":"boolean","default":true},"showMenu":{"type":"boolean","default":true},"showNotifications":{"type":"boolean","default":true},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},
"HomepageLayout": {"x-ticvai-persistence":"whitelabel.homepage_section","type":"object","required":["sections"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"sections":{"type":"array","items":{"type":"object","required":["kind","sortOrder","isVisible"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"kind":{"$ref":"#/components/schemas/HomepageSectionKind"},"title":{"$ref":"#/components/schemas/LocalisedText"},"sortOrder":{"type":"integer"},"isVisible":{"type":"boolean"},"contentPageId":{"type":"string","format":"uuid","nullable":true},"maxItems":{"type":"integer","nullable":true,"description":"How many items the section shows. On the mobile Home, `attractions`, `dining`, `whatsOn` and `shop` show 1 or 2 highlights (decided 29 September, MOB-3)."},"heroStyle":{"type":"string","nullable":true,"enum":["carousel","video","poster","split",null],"description":"For `heroBanner` only (decided 29 September, MOB-3)."}}}}}},
"LanguageConfig": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["languages","defaultLanguage"],"properties":{"languages":{"type":"array","items":{"type":"string","pattern":"^[a-z]{2}$"}},"defaultLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"rtlLanguages":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.","items":{"type":"string","pattern":"^[a-z]{2}$"}},"translationGaps":{"type":"array","readOnly":true,"description":"Content lacking a version in an enabled language.","items":{"type":"object","properties":{"language":{"type":"string"},"missingCount":{"type":"integer"},"areas":{"type":"array","items":{"type":"string"}}}}}}},
"LocalisedRichText": {"x-ticvai-persistence":"none — jsonb column","type":"object","description":"Keyed by language code. Values are sanitised HTML.","additionalProperties":{"type":"string"}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MinimumAppVersion": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n","properties":{"ios":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"},"android":{"type":"string","nullable":true,"pattern":"^\\d+\\.\\d+\\.\\d+$"}}},
"ModuleEnablement": {"x-ticvai-persistence":"whitelabel.module_enablement","type":"object","required":["moduleKey","isLicensed","isEnabled"],"properties":{"moduleKey":{"$ref":"#/components/schemas/ModuleKey"},"displayName":{"type":"string"},"isLicensed":{"type":"boolean","description":"From the tenant's subscription. False makes enablement impossible."},"isEnabled":{"type":"boolean"},"referencedBy":{"type":"array","readOnly":true,"x-ticvai-derived":"onWrite","description":"Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.","items":{"type":"string"}}}},
"NavigationConfig": {"x-ticvai-persistence":"whitelabel.navigation_item","type":"object","description":"**The mobile tab set is venue configuration (decided 29 September, MOB-1; 29 September brief decision 6).** Before a tenant saves its own, `bottomNavigation` is Home, Explore, Plan and Tickets (each an `appSection` link), with the Buy tickets button beside them; Map is an optional tab. Plan is left out while `visitPlanner` is off.\n","required":["kind","items"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"kind":{"type":"string","enum":["bottomNavigation","drawer","tabs"]},"items":{"type":"array","maxItems":12,"items":{"type":"object","required":["label","target","isVisible","sortOrder"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"},"label":{"$ref":"#/components/schemas/LocalisedText"},"icon":{"type":"string"},"target":{"$ref":"#/components/schemas/LinkTarget"},"isVisible":{"type":"boolean","description":"At most five may be visible in bottom navigation; the rest overflow."},"sortOrder":{"type":"integer"}}}},"buyButton":{"type":"object","nullable":true,"description":"**The persistent Buy tickets button (decided 29 September, MOB-2).** On every screen of the mobile app except the booking and checkout steps; it opens GST-003. Read with `bottomNavigation`.\n","properties":{"style":{"type":"string","enum":["raised","floating","flat","hidden"],"default":"raised","description":"`raised` sits in the centre of the tab bar, as the v4 prototype shows; `hidden` turns it off."},"label":{"$ref":"#/components/schemas/LocalisedText"}}}}},
"OrgUnit": {"x-ticvai-persistence":"platform.scope","type":"object","required":["id","level","path","code","name","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"level":{"$ref":"#/components/schemas/ScopeLevel"},"parentId":{"type":"string","format":"uuid","nullable":true},"path":{"type":"string","description":"Materialised ltree path, e.g. `t_ref.b_alpha.r_north.v_alpha1`.","pattern":"^[a-z0-9_]+(\\.[a-z0-9_]+)*$"},"code":{"type":"string","maxLength":64},"name":{"type":"string","maxLength":200},"isActive":{"type":"boolean","description":"False causes every permission query at or beneath this node to resolve to DENY.\n"},"childCount":{"type":"integer","minimum":0}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Policy": {"x-ticvai-persistence":"whitelabel.policy","type":"object","required":["kind","version","body","effectiveFrom","publishedAt"],"properties":{"kind":{"$ref":"#/components/schemas/PolicyKind"},"title":{"type":"string","description":"The heading a guest sees, and the field a refund question retrieves against.\n"},"version":{"type":"string","description":"Immutable. A guest who consented to version 3 consented to version 3, and a policy that changes under a recorded consent is a compliance failure.\n"},"body":{"$ref":"#/components/schemas/LocalisedRichText"},"requiresReconsent":{"type":"boolean"},"effectiveFrom":{"type":"string","format":"date"},"publishedByPrincipalId":{"type":"string","format":"uuid"},"publishedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"PolicyKind": {"type":"string","enum":["privacy","termsAndConditions","refund","cookie","accessibility"]},
"Principal": {"x-ticvai-persistence":"identity.principal","type":"object","required":["id","username","displayName","isActive"],"properties":{"id":{"type":"string","format":"uuid"},"username":{"type":"string"},"displayName":{"type":"string"},"isActive":{"type":"boolean"},"validFrom":{"type":"string","format":"date-time","nullable":true},"validTo":{"type":"string","format":"date-time","nullable":true,"description":"Past this, resolution returns DENY regardless of grants."},"primaryRoleId":{"type":"string","format":"uuid","nullable":true,"description":"Determines the landing screen when the principal holds several roles and picks one at login.\n"},"roles":{"type":"array","items":{"$ref":"#/components/schemas/RoleSummary"}},"lastLoginAt":{"type":"string","format":"date-time","nullable":true}}},
"Product": {"x-ticvai-persistence":"catalogue.product","type":"object","required":["id","code","name","kind","venueId","scopePath","isSellable","hasVariants"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","maxLength":64},"familyKey":{"type":"string","maxLength":64,"pattern":"^[A-Za-z0-9_-]+$","nullable":true,"x-ticvai-unique":"venue","description":"**The same product at another location** (decided 29 September, rev 3 REV3-18). Optional. A tenant that sells one attraction at several venues gives each venue's product the same key, e.g. `aquarium-entry`; the key names the family across the tenant and each venue has at most one product in it, so a second product at the same venue with the key is refused with `409 duplicate-code`. **What it is for:** when a guest changes location on the booking screen (the 'Booking at' switcher, `BookingFlowConfig.locationSwitcher`), lines whose product shares a `familyKey` with a product at the new venue are carried over to that product, with times and prices refreshed; every other line is cleared. Null means the product belongs to no family and its lines always clear on a switch. Compared case-insensitively, like `code`.\n"},"name":{"type":"string","maxLength":200},"description":{"type":"string"},"kind":{"$ref":"#/components/schemas/ProductKind"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"createdByPrincipalId":{"type":"string","format":"uuid","readOnly":true,"description":"1.4.18. **The approval gate refuses an approver who is the author, and nothing recorded either.** `SeatBlock`, `DelegatedAccess` and `ManualDiscountRequest` all carry this and the product passing through approval did not.\n"},"approvedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"responsibleDepartmentId":{"type":"string","format":"uuid","nullable":true,"description":"Who owns this product commercially. A scope node at `department` level."},"onSaleFrom":{"type":"string","format":"date-time","nullable":true,"description":"1.4.8. **A seasonal product should not need somebody awake at midnight.** Archiving already runs on a timer in this contract, so the machinery exists; `effectiveFrom` appears on tax codes, FX rates and white-label policies and not here.\n"},"onSaleTo":{"type":"string","format":"date-time","nullable":true,"description":"Retires the product automatically. **Retirement is not deletion** — the product stops selling and every order that referenced it still resolves.\n"},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"**Taken from their `fnb.product` and `retail.product`, 20 September.** `catalogue.product_category` has existed since 20 August with two operations and nothing could be filed under it — a merchandise hierarchy with a tree and no leaves. Their per-domain product tables both carried this column and ours did not.\n"},"lifecycleState":{"$ref":"#/components/schemas/ProductLifecycleState"},"isSellable":{"type":"boolean","readOnly":true,"description":"True only when live **and** carried by a published bundle. Approval and publication are different acts.\n**Derived, never set.** It changes when `transitionProductLifecycle` moves the product and when `publishBundle` carries it, so `updateProduct` does not take it — `withdraw` is how a product stops selling.\n"},"isStockTracked":{"type":"boolean","default":false,"description":"**Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock, which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a bottle of water is both. Without it, an F&B sale cannot tell inventory whether to move.\n"},"hasVariants":{"type":"boolean"},"variantCount":{"type":"integer"},"segmentTags":{"type":"array","description":"7.3.5. **A channel and a segment tag are mandatory and nothing required either.** A catalogue that cannot be filtered by segment is a catalogue nobody can report on.\n**Hierarchical, not flat** — `family/with-toddlers` narrows `family` without duplicating it, which is how the promotions engine already treats scope.\n**A level is a tag under `level/`** (decided 29 September, rev 3 REV3-19): `level/beginner`, `level/intermediate`, `level/advanced`, `level/expert` (proposed codes, client to correct). A guest screen filters on it with `listProducts` `segmentTag`, and the words a guest reads beside each option come from `ProductCategory.description`, not from the tag.\n","items":{"type":"string"}},"codeSchema":{"type":"string","readOnly":true,"description":"7.3.4 specifies `[ParkCode]-[ProductType]-[Variant]`. **`Product.code` existed and nothing required a format**, so a venue with three thousand products had three thousand conventions.\nThe tenant sets the pattern and the platform generates against it. **Validation is the point, not the string** — a code typed by hand is a code that will not sort.\n"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/Channel"}},"entitlementTemplateId":{"type":"string","format":"uuid","nullable":true,"description":"What the buyer receives. Null for products that grant nothing — F&B and retail. Identity and entitlement are separate concerns.\n"},"blockedOffline":{"type":"boolean","description":"True for seated and retail. Seated because a seat map is not a count; retail because stock depletes in real time.\n"},"dataMaskValues":{"type":"object","additionalProperties":true,"description":"Custom fields. JSONB-backed, defined by the venue's data mask."},"guestListing":{"$ref":"#/components/schemas/GuestListing"},"notBookableLabel":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The label a guest reads on an `infoOnly` product, e.g. *Info only* or *Not bookable online; ask at the desk* (decided 29 September, rev 3 REV3-14). Each value at most 60 characters. Null means the guest screen shows its default wording. Ignored unless `guestListing` is `infoOnly`.\n"},"salesContact":{"allOf":[{"$ref":"#/components/schemas/ProductSalesContact"}],"nullable":true,"description":"**Who a guest contacts to book a view-only product** (decided 29 September, W3), e.g. a training course listed with full details and no Book button. Shown as *Call sales* and *Email sales* on an `infoOnly` product. Null means the venue's own contact (white-label `getTenantAppStatus.contact`). Ignored unless `guestListing` is `infoOnly`.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow this product is sold through** (decided 29 September, W8 and W12): a white-label `BookingFlow` of the venue, which orders the guest's steps (for a workshop, the product first and then the date and time). Null means the category's flow (`ProductCategory.bookingFlowId`), and failing that the venue's flow for the product's `kind`. Written by `createProduct` and `updateProduct`, which refuse an id that is not a flow of the venue with `422`.\n"},"displayTags":{"type":"array","maxItems":6,"items":{"$ref":"#/components/schemas/ProductDisplayTag"},"description":"**Short facts a guest reads on the ticket card and under *Read more***: *2 Hours*, *Min 1.10 m*, *Free adult entry*, *Valid 90 days*, *Emirates ID* (decided 29 September, 23SEP-3). Not `segmentTags`, which are for reporting and segmentation and which a guest never reads.\n**Derived on read when none are set.** When the venue has written no tags, a read returns tags derived from the product's duration (`clock`), entitlement validity (`calendar`) and the eligibility rule's `minHeightCm` (`height`), each marked `derived: true`; they are never stored. Once the venue writes any tag, only what it wrote is returned. Whether the guest screen shows them is `BookingFlowConfig.ticketTags` (white-label).\n"},"media":{"type":"array","maxItems":20,"items":{"$ref":"#/components/schemas/ProductMedia"},"description":"**The product's own photos and video** (decided 29 September, 23SEP-4). *Read more* opens on the `isPrimary` item, and a listing shows each product's primary image, so two tickets in one category no longer share the category's picture (`ProductCategory.imageAssetId`).\nEvery `assetId` names an asset of the asset library (`assets.yaml` `MediaAsset`) in status `ready` whose kind matches `kind`; anything else is a `422`. **Exactly one item is `isPrimary`** when the list is not empty, and an `assetId` appears once; otherwise `400`. Setting the list records each reference as asset usage (`MediaUsage` with `surface: product`, `referenceId` the product id, `isLive` true while the product is listed to guests), which is what stops a used asset being archived from under the product.\n"},"consentQuestionIds":{"type":"array","maxItems":10,"uniqueItems":true,"items":{"type":"string","format":"uuid"},"description":"**The consent questions a guest answers when booking this product**, in the order they are asked (decided 29 September, rev 3 REV3-26): *Are you able to swim?*, *Do you hold a scuba certification?*, *I accept the risk*. Each id names a consent question defined in marketing-crm (`ConsentQuestion`), which owns the text, its version and whether it is asked per person or once per booking; the answer is stored there as a consent record (question version, answer, who answered, when). **One question or several, as the venue chooses.** A flow can carry its own list too (`white-label.BookingFlow.settings.consentQuestionIds`, on the product's published booking flow as `getPublishedBookingFlow` resolves it: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig` 29 September, W12); a booking asks the union of the flow's questions and those of every product in the cart, each question once (`orders.Cart.consentQuestions`). An id that names no active consent question of the tenant is a `422`.\n"},"requiresTimeWindow":{"type":"boolean","default":false,"description":"**True for a space sold by the hour**, e.g. a meeting room type (decided 29 September, rev 3 REV3-13). The product is the room type (*focus pod*, *majlis*, *boardroom*, *auditorium*), never a named room; its lengths are a `length` axis (`setProductAttributes`) whose values carry `durationMinutes`, and each length is a variant priced on its own in the price list, so price is the room rate for that length. The cart line carries the booked start and end (orders), the end being the start plus the chosen variant's `durationMinutes`; `resources.listProductStartTimes` supplies the start times for a variant and a date and `allocateResources` picks the room from the product's resource requirements (`setExperienceResourceRequirements`) at checkout. True requires every active variant to have a `durationMinutes`; otherwise `422`.\n"},"productOwnerPrincipalId":{"type":"string","format":"uuid","nullable":true,"description":"The product owner (29 September, data model DM3), set with `setProductContextOwnership`. `responsibleDepartmentId` is the owning department."},"operationalContact":{"type":"string","maxLength":200,"nullable":true,"description":"A principal id or a name, as the context screen takes it."},"businessUnitId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid","nullable":true,"description":"A `ledger.legal_entity`, read through finance."},"attractionId":{"type":"string","format":"uuid","nullable":true},"siteId":{"type":"string","format":"uuid","nullable":true},"locationId":{"type":"string","format":"uuid","nullable":true},"brandId":{"type":"string","format":"uuid","nullable":true,"description":"The brand, as the context screen names it (a catalogue brand category)."},"marketCode":{"type":"string","maxLength":40,"nullable":true},"salesTerritory":{"type":"string","maxLength":100,"nullable":true}}},
"ProductCategory": {"type":"object","x-ticvai-persistence":"catalogue.product_category","description":"Retail Board 2 of the client's design set, 20 August. **`listSeatCategories` existed and a product category did not** — a seat category prices a seat, and a merchandise hierarchy groups a catalogue.\n**Brand sits here rather than as its own entity.** A venue with four brands and a hierarchy five levels deep can express that with a parent; a venue with one brand should not have to maintain a table containing one row.\n**`displayOrder` is not alphabetical and that is the point.** A retail category list runs in the order the merchandiser wants a guest to see it, and sorting by name puts *Accessories* above *Apparel* forever.\n","required":["id","name","kind"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"},"code":{"type":"string","maxLength":64,"nullable":true,"x-ticvai-unique":"tenant","description":"**Taken from their category tables, 20 September.** Ours had a uuid and a localised name, so an importer matching *Beverages* had to match on a display string that a venue is free to translate.\n**Unique per tenant where set** (decided 28 September, audit R108): two categories in one tenant never share a code, and `setProductCategories` refuses a body that would, with `409 duplicate-code`.\n"},"nameLocalised":{"type":"object","additionalProperties":{"type":"string"}},"kind":{"type":"string","enum":["category","brand","collection","season","department"]},"parentId":{"type":"string","format":"uuid","nullable":true,"description":"**One tree, not four.** A brand under a department under a category is how a real merchandise hierarchy runs, and separate tables for each level cannot express a venue that nests them differently.\n"},"scopePath":{"type":"string","readOnly":true,"description":"Set by the server from the venue the caller acts at; not sent."},"displayOrder":{"type":"integer","default":100},"imageAssetId":{"type":"string","format":"uuid","nullable":true},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The short line a guest reads under a category option, e.g. *Surf lessons: learn on the beginner wave with a coach* (decided 29 September, rev 3 REV3-19). Each language value at most 200 characters.\n"},"bookingFlowId":{"type":"string","format":"uuid","nullable":true,"description":"**The booking flow for every product filed here** that names none of its own (decided 29 September, W12, BO-115). Null means the venue's flow for each product's `kind`. A white-label `BookingFlow` of the venue; `setProductCategories` refuses any other id with `422`.\n"},"isActive":{"type":"boolean","default":true,"description":"**Deactivated rather than deleted.** A category with a season behind it still names the products sold under it, and removing it rewrites last year's report.\n"}}},
"ProductCategoryNode": {"x-ticvai-persistence":"none — projection over catalogue.product_category","description":"**One node of the tree `listProductCategories` returns.** A `ProductCategory` with its children nested under it, in `displayOrder`, so no caller reassembles the hierarchy from `parentId`. `setProductCategories` still takes the flat list, because a write names each parent by id.\n","allOf":[{"$ref":"#/components/schemas/ProductCategory"},{"type":"object","required":["children"],"properties":{"children":{"type":"array","description":"Empty on a leaf.","items":{"$ref":"#/components/schemas/ProductCategoryNode"}}}}]},
"ProductDisplayTag": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","required":["kind","label"],"description":"One short fact on a ticket card (decided 29 September, 23SEP-3). `kind` picks the icon.","properties":{"kind":{"type":"string","enum":["clock","height","free","calendar","id"],"description":"`clock` a duration, `height` a height rule, `free` something included free, `calendar` a validity, `id` a document the guest must bring."},"label":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"What the guest reads, e.g. *2 Hours*. Each language value at most 40 characters."},"derived":{"type":"boolean","readOnly":true,"default":false,"description":"True on a tag the server derived on read because the venue set none. Never sent."}}},
"ProductKind": {"type":"string","description":"**`openDated` added 24 August** from the client's *Create Ticket Flow* board, which names six main ticket types and this was the one with no kind: **valid on any date within an eligible range, rather than for a named performance or a fixed date.**\nThe mechanism already existed — `access.entitlement` carries `valid_from`, `valid_to`, `entries_allowed` and `frozen_days`, which is exactly an open-dated pass. **What was missing was the product saying it is one**, so a catalogue could not offer it and a report could not count it.\n**`datedAdmission` is a different thing and the two were being conflated**: dated is *this Tuesday*, open-dated is *any Tuesday between March and June*. A guest buying the second and being sold the first has bought the wrong ticket.\n**Transport uses two existing kinds, not a new one** (decided 29 September, rev 3 REV3-21). A one-way trip is `timedAdmission`: `transport.createTransportRoute` creates the route's product with one variant per passenger type, and each departure is a performance. A multi-trip or unlimited pass is `openDated`: `transport.createTransportPassType` creates it, with `EntitlementTemplate.entriesAllowed` = the pass's trips (null for unlimited), the validity = `validityDays`, and `EntitlementTemplate.transportRestriction` naming the station pair the pass was bought for, so `access` refuses it on another journey. The sale path is unchanged: both are cart lines, priced by `transport.quoteTransportFare` (orders `TransportLineAttributes`).\n","enum":["admission","timedAdmission","datedAdmission","openDated","seated","membership","bundle","fnb","retail","rental","addOn","giftCard"]},
"ProductLifecycleState": {"type":"string","enum":["draft","inReview","approved","live","withdrawn","archived"]},
"ProductMedia": {"x-ticvai-persistence":"catalogue.product_media","type":"object","required":["assetId","kind","isPrimary"],"description":"One photo or video of a product, referencing the asset library (decided 29 September, 23SEP-4). One row per product and asset, so the asset library can answer which products use an asset.\n","properties":{"assetId":{"type":"string","format":"uuid","description":"A `MediaAsset` of `assets.yaml`, in status `ready`."},"kind":{"type":"string","enum":["image","video"]},"isPrimary":{"type":"boolean","default":false,"description":"The item *Read more* opens on and a listing shows. Exactly one per product."},"displayOrder":{"type":"integer","default":100},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true}}},
"ProductSalesContact": {"x-ticvai-persistence":"none — jsonb column on catalogue.product","type":"object","description":"Who to contact to book a view-only product (decided 29 September, W3). At least one of `phone` or `email`.\n","minProperties":1,"properties":{"phone":{"type":"string","maxLength":32,"nullable":true},"email":{"type":"string","format":"email","maxLength":254,"nullable":true},"note":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"A line shown under the contact, e.g. *Group courses are booked by phone*. At most 200 characters per language."}}},
"Role": {"x-ticvai-persistence":"identity.role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique within the tenant** (decided 28 September, audit R108). A seeded role's code is reserved in every tenant. Unique per tenant, not per venue, because a grant names a role anywhere in the tree; `createRole` refuses a duplicate with `409 duplicate-code`.\n"},"name":{"type":"string"},"description":{"type":"string"},"permissions":{"type":"array","description":"**A role that grants no permissions is not a role.** `Role` carried a code, a name and two counts until 18 August, and `identity.role_permission` derived from it with exactly one column — `role_id`. **A join table that joins to nothing**, found by Hrushikant in review and missed by the schema audit that ran the same day.\n**The audit asked whether every table had columns, a relationship and an owner, and this table had all three.** What it did not ask is whether a table with one column can do the job its name claims.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/Permission"}},"inheritsFromRoleId":{"type":"string","format":"uuid","nullable":true,"description":"**Role composition, one level deep and no deeper.** A supervisor role that is a cashier plus three permissions is how venues actually describe them.\n**Cycles are refused and depth is capped at one**, because a permission set nobody can read off the screen is a permission set nobody audits.\n"},"isSystem":{"type":"boolean","default":false,"description":"**Seeded roles ship and are editable; deleting one is refused.** A venue that removes `cashier` and rebuilds it has two roles with one name in the audit log.\n**The seeded system roles are Cashier, Supervisor, Venue Manager, Finance and Tenant Admin** (proposed in `docs/active/seed-data-proposal.md` section 2, client to correct; audit R229).\n"},"principalCount":{"type":"integer"},"grantCount":{"type":"integer"}}},
"RoleSummary": {"x-ticvai-persistence":"none — projection over role","type":"object","required":["id","code","name"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"isPrimary":{"type":"boolean"}}},
"ScopeLevel": {"type":"string","description":"**The eight organisational levels, plus `subject`.** Restored 24 August.\n`tenancy.yaml` holds the authoritative definition of the eight levels and this mirrors them so a contract can reference a level without depending on the whole tenancy surface. **Seven organisational levels plus `outlet`** — a commercial branch beside the organisational one (CF-138, ADR-0018). **A department has requisitions and rotas; an outlet has a menu and stock**, and modelling a restaurant as a department would put it in the staffing tree.\n\n**`subject` is the one value tenancy does not have, and it is not a level.** It is here because `check-package` reads this enum as the closed vocabulary for `x-ticvai-scope-level`, and some operations act on one guest's own resources, which sit in no node of the venue hierarchy. So `subject` is valid as an operation's scope level and never as a `ScopeRef.level`: every `ScopeRef` is a row of `platform.scope`, and those carry one of the eight.\n","enum":["tenant","brand","region","venue","department","subDepartment","workstation","outlet","subject"]},
"SeoMetadata": {"type":"object","x-ticvai-persistence":"control.seo_metadata","description":"22.11.1 to 22.11.12, CF-137. **Twelve requirements, checked against the matrix.**\n**SEO is not a marketing nicety for a venue selling online** — an attraction that does not appear in search sells through OTAs at OTA commission, which is the cost this avoids.\n","required":["id","entityKind","entityId"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"entityKind":{"type":"string","enum":["contentPage","product","event","performance","membership","promotion","venue"]},"entityId":{"type":"string","format":"uuid"},"locale":{"type":"string"},"title":{"type":"string","nullable":true},"metaDescription":{"type":"string","nullable":true},"keywords":{"type":"array","items":{"type":"string"}},"canonicalUrl":{"type":"string","nullable":true},"slug":{"type":"string","nullable":true,"description":"22.11.6. **Human-readable, and changing one is a redirect rather than an edit** — a slug that changes without a 301 is a page that was ranking and now is not.\n"},"hreflang":{"type":"object","additionalProperties":{"type":"string"},"description":"22.11.11. **Which URL serves which language**, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page.\n"},"schemaOrgType":{"type":"string","nullable":true},"openGraph":{"type":"object","additionalProperties":{"type":"string"}},"isAutoGenerated":{"type":"boolean","default":true,"description":"22.11.2. **Generated by default and overridable.** A venue with 400 products will not write 400 meta descriptions, and one with an important landing page will not accept a generated one.\n"},"noIndex":{"type":"boolean","default":false},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"}}},
"StorefrontAnalyticsProvider": {"type":"object","x-ticvai-persistence":"whitelabel.analytics_provider","description":"**One analytics platform the storefront or app reports to** (22.10.29, 29 September build). Venue configuration: a null `venueId` is the tenant-wide default a venue's own row replaces.","required":["provider","measurementId","surfaces","consentCategory","isEnabled"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"venueId":{"type":"string","format":"uuid","nullable":true},"provider":{"type":"string","enum":["googleAnalytics4","googleTagManager","adobeAnalytics","metaPixel","matomo","other"]},"providerLabel":{"type":"string","maxLength":100,"nullable":true,"description":"The name, when `provider` is `other`."},"measurementId":{"type":"string","maxLength":100,"description":"What the tag or SDK reports to (GA4 `G-...`, Tag Manager `GTM-...`, a pixel id)."},"surfaces":{"type":"array","minItems":1,"items":{"type":"string","enum":["guestWeb","guestApp"]}},"consentCategory":{"type":"string","enum":["functional","analytics","personalisation","marketing"],"default":"analytics","description":"The cookie category the visitor must grant before this provider loads (marketing-crm `CookieCategory`)."},"isEnabled":{"type":"boolean","default":true},"reportingPropertyId":{"type":"string","maxLength":100,"nullable":true,"description":"The property `getStorefrontInsights` asks the reporting API about (a GA4 property id). Staff only."},"reportingCredentialRef":{"type":"string","maxLength":200,"nullable":true,"writeOnly":true,"description":"The vault reference of the reporting credential. Accepted, never returned."},"hasReportingCredential":{"type":"boolean","readOnly":true,"description":"Whether a reporting credential is held, since the reference itself is never returned."},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005)."},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"TenantAppStatus": {"x-ticvai-persistence":"none — computed","type":"object","description":"Computed on read. The published fields come from the current `ConfigVersion`, the maintenance fields from the tenant's `tenant_config` row (`setMaintenanceMode`), and the draft fields from the working draft. **Fields marked staff only are left out of a response to a caller without a staff session** (`getTenantAppStatus`).\n","required":["tenantId","isPublished","isInMaintenance"],"properties":{"tenantId":{"type":"string","format":"uuid"},"isPublished":{"type":"boolean","x-ticvai-derived":"onRead","description":"True once any version has been published."},"publishedVersion":{"type":"string","nullable":true},"publishedAt":{"type":"string","format":"date-time","nullable":true},"draftVersion":{"type":"string","description":"Staff only."},"hasUnpublishedChanges":{"type":"boolean","x-ticvai-derived":"onRead","description":"Staff only. The working draft differs from the current version's `snapshot`."},"activeModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isEnabled` true."},"licensedModuleCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. `ModuleEnablement` rows with `isLicensed` true."},"activePageCount":{"type":"integer","x-ticvai-derived":"onRead","description":"Staff only. Content pages that are `published` and enabled."},"isInMaintenance":{"type":"boolean"},"maintenanceMessage":{"$ref":"#/components/schemas/LocalisedText"},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"$ref":"#/components/schemas/MinimumAppVersion"},"contact":{"$ref":"#/components/schemas/VenueContact"},"availability":{"$ref":"#/components/schemas/AppAvailability"},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"What the sold-out or closed screen says (WEB-029). Null shows the default wording."},"venues":{"type":"array","maxItems":200,"x-ticvai-derived":"onRead","description":"**Public: the venues a guest can pick** (decided 28 September, audit R267; schema named 29 September, readiness close-out, our build plan). The source of the venue picker on WEB-001 and GST-001, returned with or without a session. **Published only**: a venue is listed when its scope node is active (`tenancy.OrgUnit.isActive`) and it is in the tenant's current published `ConfigVersion`; a venue added or reactivated since the last publish appears after the next publish, and a draft never reaches a guest. Ordered by `name`. Empty when nothing is published.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid","description":"**The venue's scope node** (`tenancy.OrgUnit.id`, level venue): what every guest screen that declares `venueId` `from: session` reads once the guest picks it."},"name":{"type":"string","maxLength":200,"description":"The venue's name (`tenancy.OrgUnit.name`)."},"city":{"type":"string","maxLength":120,"nullable":true,"description":"Shown under the name so two venues with similar names can be told apart."},"openingHoursToday":{"type":"object","nullable":true,"description":"Today's opening hours in the venue's time zone, from `tenancy.VenueSettings` opening hours. Null when the venue is closed today or has none set.","properties":{"opens":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"},"closes":{"type":"string","pattern":"^([01][0-9]|2[0-3]):[0-5][0-9]$"}}}}}},"whatsNew":{"type":"array","maxItems":10,"x-ticvai-derived":"onRead","description":"**Public: the guest \"what's new\"** (decided 29 September, rev 3 GAP-B2). Newest first, at most 10, from `platform-ops.Release.guestReleaseNotes` of the releases the tenant's cell has received; a release with no guest notes is skipped. Returned with or without a staff session.\n","items":{"type":"object","required":["version","publishedAt","notes"],"properties":{"version":{"type":"string","description":"The release version."},"publishedAt":{"type":"string","format":"date-time","description":"When the release reached the tenant's cell."},"notes":{"$ref":"#/components/schemas/LocalisedText"}}}},"recentChanges":{"type":"array","description":"Staff only. Names the principal behind each change, so it never reaches a public response.","items":{"type":"object","properties":{"area":{"type":"string"},"description":{"type":"string"},"principalId":{"type":"string","format":"uuid"},"at":{"type":"string","format":"date-time"}}}}}},
"TenantConfig": {"x-ticvai-persistence":"whitelabel.tenant_config","type":"object","description":"**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n","required":["tenantId","version"],"properties":{"tenantId":{"type":"string","format":"uuid"},"version":{"type":"string","description":"The draft's working version label; the published one is `ConfigVersion.version`."},"isDraft":{"type":"boolean","readOnly":true,"description":"True for the working draft, which is the only row."},"brand":{"$ref":"#/components/schemas/BrandIdentity"},"appIcons":{"$ref":"#/components/schemas/AppIcons"},"bookingFlow":{"$ref":"#/components/schemas/BookingFlowConfig"},"bookingFlows":{"type":"array","readOnly":true,"x-ticvai-derived":"onRead","description":"Every venue's booking flows in the draft (`whitelabel.booking_flow`), so a publish snapshots them with the rest (decided 29 September, W12).","items":{"$ref":"#/components/schemas/BookingFlow"}},"theme":{"$ref":"#/components/schemas/Theme"},"fonts":{"$ref":"#/components/schemas/FontConfig"},"footer":{"$ref":"#/components/schemas/FooterConfig"},"notificationBranding":{"type":"object","nullable":true,"description":"BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n","properties":{"senderName":{"type":"string"},"replyToEmail":{"type":"string","format":"email"},"smsSenderId":{"type":"string","nullable":true},"whatsappBusinessId":{"type":"string","nullable":true},"logoAssetId":{"type":"string","format":"uuid","nullable":true}}},"enabledPaymentMethods":{"type":"array","nullable":true,"description":"BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n","items":{"type":"string"}},"accessibility":{"$ref":"#/components/schemas/AccessibilitySettings"},"header":{"$ref":"#/components/schemas/HeaderConfig"},"navigation":{"$ref":"#/components/schemas/NavigationConfig"},"homepage":{"$ref":"#/components/schemas/HomepageLayout"},"modules":{"type":"array","items":{"$ref":"#/components/schemas/ModuleEnablement"}},"features":{"type":"array","items":{"$ref":"#/components/schemas/FeatureToggle"}},"languages":{"$ref":"#/components/schemas/LanguageConfig"},"updatedAt":{"type":"string","format":"date-time"},"isInMaintenance":{"type":"boolean","default":false,"description":"Written by `setMaintenanceMode`; read by `getTenantAppStatus`."},"maintenanceMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"The message on the branded maintenance screen."},"expectedBackAt":{"type":"string","format":"date-time","nullable":true},"minimumAppVersion":{"allOf":[{"$ref":"#/components/schemas/MinimumAppVersion"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"contact":{"allOf":[{"$ref":"#/components/schemas/VenueContact"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availability":{"allOf":[{"$ref":"#/components/schemas/AppAvailability"}],"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"availabilityMessage":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Live state, written by `setMaintenanceMode` (audit R073)."},"venues":{"type":"array","x-ticvai-derived":"onRead","description":"The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n","items":{"type":"object","required":["venueId","name"],"properties":{"venueId":{"type":"string","format":"uuid"},"name":{"$ref":"#/components/schemas/LocalisedText"},"city":{"type":"string","nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."}}}}}},
"Theme": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","required":["primaryColour","secondaryColour","backgroundColour","textColour"],"properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"secondaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"accentColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"darkMode":{"type":"object","description":"Optional dark variant. Derived from the light theme when absent.","properties":{"primaryColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"backgroundColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"},"textColour":{"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}}},"cornerRadius":{"type":"integer","minimum":0,"maximum":32,"description":"The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."},"surfaceStyle":{"type":"string","enum":["glass","solid"],"default":"glass","description":"Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."},"buttonStyle":{"type":"string","enum":["solid","outline","pill"],"default":"solid","description":"Button shape (decided 29 September, rev 3 CFG-3)."},"componentColours":{"type":"object","description":"**Colours for single interactive elements (decided 17 September, M17-11).** Each is optional and falls back to the theme colours. Every pair passes the same contrast check as the theme (`ContrastProblem`), or `setTheme` refuses it with 400. The guest flow stays the standard one; only the colours change.\n","properties":{"primaryCta":{"$ref":"#/components/schemas/ThemeComponentColour"},"payButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"addToCart":{"$ref":"#/components/schemas/ThemeComponentColour"},"buyTicketsButton":{"$ref":"#/components/schemas/ThemeComponentColour"},"link":{"$ref":"#/components/schemas/ThemeComponentColour"},"badge":{"$ref":"#/components/schemas/ThemeComponentColour"}}}}},
"VenueContact": {"x-ticvai-persistence":"none — embedded in tenant_config","type":"object","nullable":true,"description":"How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n","properties":{"phone":{"type":"string","nullable":true},"email":{"type":"string","format":"email","nullable":true},"whatsapp":{"type":"string","nullable":true},"address":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true},"openingHours":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"nullable":true,"description":"Prose, as the guest reads it. The bookable hours are the catalogue's."}}}
}
```
