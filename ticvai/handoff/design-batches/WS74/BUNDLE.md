# WS74 — Digital Asset Management DAM board 1

**10 screens · 15 operations · 16 schemas · 3 permissions**

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

- **Every control that can be refused must be gated.** 3 permissions apply here:
  `AI_USE, ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW`. A control nobody can use must say so,
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
| `CMS-061` | Digital Asset Management Command Center | B–D | 0 | 16 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `CMS-062` | Central Digital Asset Library | B–D | 2 | 18 | 6 | 7 | 1 | 0 | — | notStarted (—) |
| `CMS-063` | Upload & Asset Ingestion Workspace | B–D | 0 | 0 | 6 | 2 | 1 | 0 | — | notStarted (—) |
| `CMS-064` | Folder, Collection & Workspace Management | B–D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-065` | Metadata & Taxonomy Management | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-066` | Tags, Keywords & Classification | B–D | 4 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-067` | Advanced Search & Discovery | B–D | 0 | 0 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `CMS-068` | Digital Asset 360° Profile | B–D | 0 | 36 | 6 | 1 | 2 | 0 | — | notStarted (—) |
| `CMS-069` | Bulk Asset Management Workspace | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-070` | Asset Activity, Recent Assets & Library Health | B–D | 0 | 14 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**CMS-063, CMS-068, CMS-069 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-061` Digital Asset Management Command Center

**Provide a centralized operational dashboard showing the complete digital asset estate across the authorized tenant and venue scope.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/digital-asset-management-command-center-cms-061` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Upload Assets, Browse Library, Create Collection. Each needs an operation, or needs removing from the … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Search | text field | — | — | `searchMedia` ?search |
| Unused only | toggle | off | — | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | — | — | `searchMedia` ?rightsExpiringWithinDays |
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every digital asset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Total digital assets | text | not in the schema: `Total Digital Assets` |
| Images | text | not in the schema: `Images` |
| Videos | text | not in the schema: `Videos` |
| Uploads | text | not in the schema: `Uploads` |
| Updates | text | not in the schema: `Updates` |
| Downloads | text | not in the schema: `Downloads` |
| Shares | text | not in the schema: `Shares` |
| Recently used | text | not in the schema: `Recently Used` |

**The selected digital asset** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Unclassified 128”, “Charts by”.

| Shows | Format | Notes |
|---|---|---|
| Total digital assets | text | not in the schema: `Total Digital Assets` |
| Images | text | not in the schema: `Images` |
| Videos | text | not in the schema: `Videos` |
| Uploads | text | not in the schema: `Uploads` |
| Updates | text | not in the schema: `Updates` |
| Downloads | text | not in the schema: `Downloads` |
| Shares | text | not in the schema: `Shares` |
| Recently used | text | not in the schema: `Recently Used` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Upload Assets (primary button) | navigation or local | — | — | — | — |
| Browse Library (secondary button) | navigation or local | — | — | — | — |
| Create Collection (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `searchMedia` (onLoad, The estate, counted and charted); `getMediaUsageAnalytics` (onLoad, Storage, uploads and library health)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Back to Tenant Workspace*
- → `CMS-062` Central Digital Asset Library: *Central Digital Asset Library*
- → `CMS-063` Upload & Asset Ingestion Workspace: *Upload & Asset Ingestion Workspace*
- → `CMS-064` Folder, Collection & Workspace Management: *Folder, Collection & Workspace Management*
- → `CMS-065` Metadata & Taxonomy Management: *Metadata & Taxonomy Management*
- → `CMS-066` Tags, Keywords & Classification: *Tags, Keywords & Classification*
- → `CMS-067` Advanced Search & Discovery: *Advanced Search & Discovery*
- → `CMS-068` Digital Asset 360° Profile: *Digital Asset 360° Profile*
- → `CMS-069` Bulk Asset Management Workspace: *Bulk Asset Management Workspace*
- → `CMS-070` Asset Activity, Recent Assets & Library Health: *Asset Activity, Recent Assets & Library Health*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital asset yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital asset are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- DAM overview shows total assets by type (images, videos, documents, brand assets); central library browses folders and subfolders (e.g. Marketing -> Campaigns -> Social Media -> Brand). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-842)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-061` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-061`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 1: Opens Digital Asset Management Command Center → Provide a centralized operational dashboard showing the complete digital asset estate across the authorized tenant and venue scope.
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F183 branch at step 1 (expected): when Nothing has been set up on Digital Asset Management Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F183 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-061?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Upload Assets, Browse Library, Create Collection.
- [ ] Every transition is wired: `CMS-001`, `CMS-062`, `CMS-063`, `CMS-064`, `CMS-065`, `CMS-066`, `CMS-067`, `CMS-068`, `CMS-069`, `CMS-070`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-062` Central Digital Asset Library

**Provide the main workspace for browsing all digital assets available to the authorized user.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `AI_USE`, `ASSET_LIBRARY_VIEW` (1 operate, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each card should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/central-digital-asset-library-cms-062` |

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: File Size, Ticket Media, Preview, View Details, Download, Add to Collection, Move. Each needs an operation … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Search central digital asset | search field | — | — | — | — | — | — |
| Filter by | multi select | — | — | — | — | The pack filters this screen by tenant, venue, asset type, category, collection, tags and 5 more — which are present is a decision the pack already made. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Search | text field | — | — | `searchMedia` ?search |
| Unused only | toggle | off | — | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | — | — | `searchMedia` ?rightsExpiringWithinDays |

#### Outputs: what the screen shows and produces

**Shown**

**Every central digital asset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset name | text | not in the schema: `asset name` |
| Asset type | text | not in the schema: `asset type` |
| Category | text | not in the schema: `category` |
| Dimensions/duration where applicable | text | not in the schema: `dimensions/duration where applicable` |
| File size | text | not in the schema: `file size` |
| Status | text | not in the schema: `status` |
| Owner | text | not in the schema: `owner` |
| Updated date | text | not in the schema: `updated date` |

**The selected central digital asset** (detail panel): The pack groups this record's detail under its own headings: “Image”, “Venue Media”, “Archive”.

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset name | text | not in the schema: `asset name` |
| Asset type | text | not in the schema: `asset type` |
| Category | text | not in the schema: `category` |
| Dimensions/duration where applicable | text | not in the schema: `dimensions/duration where applicable` |
| File size | text | not in the schema: `file size` |
| Status | text | not in the schema: `status` |
| Owner | text | not in the schema: `owner` |
| Updated date | text | not in the schema: `updated date` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| File Size (primary button) | navigation or local | — | — | — | — |
| Ticket Media (secondary button) | navigation or local | — | — | — | — |
| Preview (secondary button) | navigation or local | — | — | — | — |
| View Details (secondary button) | navigation or local | — | — | — | — |
| Download (secondary button) | navigation or local | — | — | — | — |
| Add to Collection (secondary button) | navigation or local | — | — | — | — |
| Move (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `searchMedia` (onLoad, Browse and filter the library); `listCollections` (onLoad, Collections to file into)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The central digital asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the central digital asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No central digital asset yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the central digital asset are still there. The pack's own statuses are 🟢 Active — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listCollections` → `ASSET_LIBRARY_VIEW` (read) · staff
- `semanticSearch` → `AI_USE` (operate) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

7 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 8.4.39 | System shall support semantic search across products, tickets, memberships, documents, knowledge bases, support content, assets, and operational data using vector-based retrieval and relevance … | Unified Operations Dashboard | CONTRACTED | `semanticSearch` |
| 23.1.6 | AI shall support semantic search allowing users to locate assets using natural language queries. | Digital Asset Management | CONTRACTED | `semanticSearch` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- DAM overview shows total assets by type (images, videos, documents, brand assets); central library browses folders and subfolders (e.g. Marketing -> Campaigns -> Social Media -> Brand). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-842)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-062` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-062`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 2: Works in Central Digital Asset Library → Provide the main workspace for browsing all digital assets available to the authorized user.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-062?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: File Size, Ticket Media, Preview, View Details, Download, Add to Collection, Move.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `AI_USE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-063` Upload & Asset Ingestion Workspace

**Provide a controlled process for adding digital assets into TICVAI. before or after upload.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation), `uploadId` (navigation) |
| Route | `/media-library/upload-asset-ingestion-workspace-cms-063` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Browse Files, Bulk Upload, Import from Approved Source. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Browse Files (primary button) | navigation or local | — | — | — | — |
| Bulk Upload (secondary button) | navigation or local | — | — | — | — |
| Import from Approved Source (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The upload asset ingestion list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the upload asset ingestion untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No upload asset ingestion yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the upload asset ingestion are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Content type not permitted, or size beyond the limit for that kind. Checked here rather than after a guest has uploaded two hundred megabytes.; 409 The transfer never finished (`transferIncomplete`), the upload ticket expired (`uploadExpired`), or the stored file is larger than the ticket allowed … (UploadRefusedProblem) |

#### Permissions

- `createUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `completeUpload` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `analyseMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

2 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.4 | Authorized users shall upload assets individually or in bulk through web interfaces and APIs. | Digital Asset Management | CONTRACTED | `createUpload` |
| 23.1.7 | AI shall automatically generate tags, keywords, and classifications for uploaded assets. | Digital Asset Management | CONTRACTED | `analyseMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upload accepts any asset type (image, video, audio, document); folder/collection workspaces group assets without duplicating files. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-843)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-063` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-063`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 4: Works in Upload & Asset Ingestion Workspace → Provide a controlled process for adding digital assets into TICVAI. before or after upload.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400, 409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-063?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Browse Files, Bulk Upload, Import from Approved Source.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-064` Folder, Collection & Workspace Management

**Allow users to organize assets without relying only on physical file-storage concepts.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/folder-collection-workspace-management-cms-064` |

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Manual Collection, Dynamic Collection, Campaign Collection, Brand Collection, Event Collection, Create … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Manual Collection (primary button) | navigation or local | — | — | — | — |
| Dynamic Collection (secondary button) | navigation or local | — | — | — | — |
| Campaign Collection (secondary button) | navigation or local | — | — | — | — |
| Brand Collection (secondary button) | navigation or local | — | — | — | — |
| Event Collection (secondary button) | navigation or local | — | — | — | — |
| Create Folder (secondary button) | navigation or local | — | — | — | — |
| Create Collection (secondary button) | navigation or local | — | — | — | — |
| Move Assets (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listCollections` (onLoad, Folders and collections)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The folder collection list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the folder collection untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No folder collection yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the folder collection are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 A business code the request names is already used within its uniqueness scope (the scope the property's `x-ticvai-unique` names; decided 28 September, audit … |

#### Permissions

- `listCollections` → `ASSET_LIBRARY_VIEW` (read) · staff
- `createCollection` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.2 | System shall support configurable asset categories, folders, collections, tags, and classifications. | Digital Asset Management | CONTRACTED | `createCollection` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Upload accepts any asset type (image, video, audio, document); folder/collection workspaces group assets without duplicating files. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-843)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-064` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-064`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 6: Works in Folder, Collection & Workspace Management → Allow users to organize assets without relying only on physical file-storage concepts.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-064?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Manual Collection, Dynamic Collection, Campaign Collection, Brand Collection, Event Collection, Create Folder, Create Collection, Move Assets.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-065` Metadata & Taxonomy Management

**Create the structured metadata model that makes TICVAI's DAM searchable and scalable.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/metadata-taxonomy-management-cms-065` |

**Known gaps.** **The pack names 9 actions on this screen and the screen declares 0 operations.** Unserved: Asset Name, Asset Type, Venue, Campaign, Event, Attraction, Owner, Source …. Each needs an operation, or … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Asset Name (primary button) | navigation or local | — | — | — | — |
| Asset Type (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Campaign (secondary button) | navigation or local | — | — | — | — |
| Event (secondary button) | navigation or local | — | — | — | — |
| Attraction (secondary button) | navigation or local | — | — | — | — |
| Owner (secondary button) | navigation or local | — | — | — | — |
| Source (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaTaxonomy` (onLoad, Categories and metadata fields)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The metadata taxonomy list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the metadata taxonomy untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No metadata taxonomy yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the metadata taxonomy are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getMediaTaxonomy` → `ASSET_LIBRARY_VIEW` (read) · staff
- `setMediaTaxonomy` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Metadata links each asset to its campaign/category (e.g. promo image tagged to a summer campaign) and captures image specifications; tags (season, venue type, audience, location, indoor/outdoor) drive search and filtering. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-844)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-065` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-065`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 8: Works in Metadata & Taxonomy Management → Create the structured metadata model that makes TICVAI's DAM searchable and scalable.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-065?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Asset Name, Asset Type, Venue, Campaign, Event, Attraction, Owner, Source.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-066` Tags, Keywords & Classification

**Provide flexible classification in addition to formal taxonomy.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Select 100 assets and apply) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/tags-keywords-classification-cms-066` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Venue: Dubai Park | select field | — | — | — | — | — | — |
| Category: Marketing | select field | — | — | — | — | — | — |
| Campaign: Summer 2026 | select field | — | — | — | — | — | — |
| Tags: Family, Outdoor | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Data it reads**: `getMediaTaxonomy` (onLoad, The controlled vocabularies)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The tags keywords classification configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the tags keywords classification untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No tags keywords classification configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tag names a closed vocabulary (`MediaTaxonomy.keywordVocabularies[].closed`) and its value is not one of that vocabulary's terms. |

#### Permissions

- `setMediaAssetTags` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `getMediaTaxonomy` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Metadata links each asset to its campaign/category (e.g. promo image tagged to a summer campaign) and captures image specifications; tags (season, venue type, audience, location, indoor/outdoor) drive search and filtering. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-844)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-066` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-066`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 10: Works in Tags, Keywords & Classification → Provide flexible classification in addition to formal taxonomy.

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-066?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-067` Advanced Search & Discovery

**Allow users to find assets quickly even when the library contains hundreds of thousands or millions of records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/advanced-search-discovery-cms-067` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Asset Type, File Format, Venue, Collection, Owner. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Kind | select | — | Image · Video · Audio · Document · Vector · Font · Archive | `searchMedia` ?kind |
| Tag | text field | — | — | `searchMedia` ?tag |
| Collection | picker: choose a collection | — | — | `searchMedia` ?collectionId |
| Search | text field | — | — | `searchMedia` ?search |
| Unused only | toggle | off | — | `searchMedia` ?unusedOnly |
| Rights expiring within days | number field (days) | — | — | `searchMedia` ?rightsExpiringWithinDays |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Asset Type (primary button) | navigation or local | — | — | — | — |
| File Format (secondary button) | navigation or local | — | — | — | — |
| Venue (secondary button) | navigation or local | — | — | — | — |
| Collection (secondary button) | navigation or local | — | — | — | — |
| Owner (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `searchMedia` (onLoad, Advanced search)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The advanced search discovery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the advanced search discovery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No advanced search discovery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the advanced search discovery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `searchMedia` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

5 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 22.1.9 | Campaign Asset Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 22.10.25 | Media Library | Marketing & CRM | CONTRACTED | `searchMedia` |
| 23.1.1 | System shall provide a centralized repository for storing and managing digital assets including images, videos, documents, PDFs, marketing materials, brand assets, audio files, templates, and … | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.5 | System shall support searching assets using keywords, metadata, tags, categories, and filters. | Digital Asset Management | CONTRACTED | `searchMedia` |
| 23.1.15 | System shall expose DAM functionality through APIs and support integration with CMS, CRM, marketing platforms, mobile applications, and third-party systems. | Digital Asset Management | CONTRACTED | `searchMedia` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-067` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-067`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 12: Works in Advanced Search & Discovery → Allow users to find assets quickly even when the library contains hundreds of thousands or millions of records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-067?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Asset Type, File Format, Venue, Collection, Owner.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-068` Digital Asset 360° Profile

**Provide one authoritative record for every digital asset.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Show; Display) and no metric row |
| Offline | online only |
| Opens with | `assetId` (navigation), `mediaId` (navigation) |
| Route | `/media-library/digital-asset-360-profile-cms-068` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `getMediaDistribution` ?assetId |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every digital asset 360°** (data table)

| Shows | Format | Notes |
|---|---|---|
| Asset ID | text | not in the schema: `Asset ID` |
| Title | text | not in the schema: `title` |
| Filename | text | not in the schema: `filename` |
| Type | text | not in the schema: `type` |
| Format | text | not in the schema: `format` |
| Category | text | not in the schema: `category` |
| Owner | text | not in the schema: `owner` |
| Tenant | text | not in the schema: `tenant` |
| Venue | text | not in the schema: `venue` |
| Upload date | text | not in the schema: `upload date` |
| Last modified | text | not in the schema: `last modified` |
| File size | text | not in the schema: `file size` |
| Campaign | text | not in the schema: `Campaign` |
| Event | text | not in the schema: `Event` |
| Attraction | text | not in the schema: `Attraction` |
| Language | text | not in the schema: `Language` |
| Tags | text | not in the schema: `Tags` |
| Keywords | text | not in the schema: `Keywords` |

**The selected digital asset 360°** (detail panel): The pack groups this record's detail under its own headings: “Preview”, “JPEG”, “Board Boundaries”.

| Shows | Format | Notes |
|---|---|---|
| Asset ID | text | not in the schema: `Asset ID` |
| Title | text | not in the schema: `title` |
| Filename | text | not in the schema: `filename` |
| Type | text | not in the schema: `type` |
| Format | text | not in the schema: `format` |
| Category | text | not in the schema: `category` |
| Owner | text | not in the schema: `owner` |
| Tenant | text | not in the schema: `tenant` |
| Venue | text | not in the schema: `venue` |
| Upload date | text | not in the schema: `upload date` |
| Last modified | text | not in the schema: `last modified` |
| File size | text | not in the schema: `file size` |
| Campaign | text | not in the schema: `Campaign` |
| Event | text | not in the schema: `Event` |
| Attraction | text | not in the schema: `Attraction` |
| Language | text | not in the schema: `Language` |
| Tags | text | not in the schema: `Tags` |
| Keywords | text | not in the schema: `Keywords` |

**Data it reads**: `getMediaDistribution` (onLoad, Where it is used)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The digital asset 360° list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the digital asset 360° untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No digital asset 360° yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the digital asset 360° are still there. The pack's own statuses are 🟢 Active — the state names which is selected. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getMediaAsset` → `ASSET_LIBRARY_VIEW` (read) · staff
- `listMediaAssetVersions` → `ASSET_LIBRARY_VIEW` (read) · staff
- `getMediaDistribution` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.12 | System shall track where assets are used across websites, mobile applications, campaigns, kiosks, emails, and digital channels. | Digital Asset Management | CONTRACTED | `getMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Activity view tracks additions, updates, missing metadata and duplicates; every asset shows a persistent digital asset ID with version control. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-846)*
- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-068` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-068`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 14: Works in Digital Asset 360° Profile → Provide one authoritative record for every digital asset.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (404).
- [ ] Every output is drawn (36 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-068?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-069` Bulk Asset Management Workspace

**Allow enterprise users to efficiently manage large groups of digital assets.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/bulk-asset-management-workspace-cms-069` |

**Known gaps.** **The pack names 3 actions on this screen and the screen declares 0 operations.** Unserved: Select Individual, Select Search Results, Select Collection. Each needs an operation, or needs removing … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Select Individual (primary button) | navigation or local | — | — | — | — |
| Select Search Results (secondary button) | navigation or local | — | — | — | — |
| Select Collection (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The bulk asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the bulk asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No bulk asset yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the bulk asset are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `bulkUpdateMediaAssets` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Advanced search by name, description or tag; a 360 asset detail view; bulk upload and batch changes (re-tag or re-categorise multiple selected assets at once). *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-845)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-069` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-069`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 16: Works in Bulk Asset Management Workspace → Allow enterprise users to efficiently manage large groups of digital assets.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-069?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Select Individual, Select Search Results, Select Collection.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-070` Asset Activity, Recent Assets & Library Health

**Give administrators and DAM managers visibility into the health and operational quality of the asset library.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/asset-activity-recent-assets-library-health-cms-070` |

**Known gaps.** **The pack names 8 actions on this screen and the screen declares 0 operations.** Unserved: Review Unclassified, Fix Metadata, Review Duplicate Candidates, Review Orphaned Assets, View Activity Log … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every asset activity recent** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets added | text | not in the schema: `Assets Added` |
| Assets updated | text | not in the schema: `Assets Updated` |
| Unclassified assets | text | not in the schema: `Unclassified Assets` |
| Missing metadata | text | not in the schema: `Missing Metadata` |
| Orphaned assets | text | not in the schema: `Orphaned Assets` |
| Used storage | text | not in the schema: `Used Storage` |
| Monthly growth | text | not in the schema: `Monthly Growth` |

**The selected asset activity recent** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Activity Asset User Time”, “Orphaned Assets”, “DAM-IMG-008421”, “Physical File”, “Digital Asset Master Record”.

| Shows | Format | Notes |
|---|---|---|
| Assets added | text | not in the schema: `Assets Added` |
| Assets updated | text | not in the schema: `Assets Updated` |
| Unclassified assets | text | not in the schema: `Unclassified Assets` |
| Missing metadata | text | not in the schema: `Missing Metadata` |
| Orphaned assets | text | not in the schema: `Orphaned Assets` |
| Used storage | text | not in the schema: `Used Storage` |
| Monthly growth | text | not in the schema: `Monthly Growth` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review Unclassified (primary button) | navigation or local | — | — | — | — |
| Fix Metadata (secondary button) | navigation or local | — | — | — | — |
| Review Duplicate Candidates (secondary button) | navigation or local | — | — | — | — |
| Review Orphaned Assets (secondary button) | navigation or local | — | — | — | — |
| View Activity Log (secondary button) | navigation or local | — | — | — | — |
| Board 1 — Shared Configuration Requirements (secondary button) | navigation or local | — | — | — | — |
| Asset types (secondary button) | navigation or local | — | — | — | — |
| supported file formats (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Activity and library health)

**Where the user goes next**

- → `CMS-061` Digital Asset Management Command Center: *Back to Digital Asset Management Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset activity recent list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset activity recent untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset activity recent yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset activity recent are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Activity view tracks additions, updates, missing metadata and duplicates; every asset shows a persistent digital asset ID with version control. *(client request · MoM 11 Sep 2026, 4.1 Digital Asset Library & Organization · DI-846)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-070` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS44 Digital Asset Management DAM Board 1.dc.html#cms-070`
- Workshop pack: Digital Asset Management DAM.pdf board 1
- Flow F183 *Digital Asset Management DAM board 1: Digital Asset Management Command Center*, step 18: Works in Asset Activity, Recent Assets & Library Health → Give administrators and DAM managers visibility into the health and operational quality of the asset library.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-070?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review Unclassified, Fix Metadata, Review Duplicate Candidates, Review Orphaned Assets, View Activity Log, Board 1 — Shared Configuration …, Asset types, supported file formats.
- [ ] Every transition is wired: `CMS-061`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
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

**11 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"analyseMediaAsset": {"method":"POST","path":"/media-assets/{assetId}/analyse","contract":"assets","summary":"Auto-tag, describe and classify an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"bulkUpdateMediaAssets": {"method":"POST","path":"/media-assets/bulk","contract":"assets","summary":"Retag, reclassify, move or archive many assets at once","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"completeUpload": {"method":"POST","path":"/media/uploads/{uploadId}/complete","contract":"assets","summary":"Confirm an upload and create the asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"},
"createCollection": {"method":"POST","path":"/media/collections","contract":"assets","summary":"Create a collection","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Collection"},
"createUpload": {"method":"POST","path":"/media/uploads","contract":"assets","summary":"Request a signed upload URL","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"UploadTicket"},
"getMediaAsset": {"method":"GET","path":"/media/{mediaId}","contract":"assets","summary":"Read an asset with derivatives and usage","permission":"ASSET_LIBRARY_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetDetail"},
"getMediaDistribution": {"method":"GET","path":"/media-distribution","contract":"assets","summary":"Where an asset is used and how it is delivered","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"assetId","in":"query","required":true}],"requestBody":null,"responds":"MediaDistribution"},
"getMediaTaxonomy": {"method":"GET","path":"/media-taxonomy","contract":"assets","summary":"The categories, metadata fields and controlled vocabularies","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"MediaTaxonomy"},
"getMediaUsageAnalytics": {"method":"GET","path":"/media-usage","contract":"assets","summary":"Downloads, views, shares and library health","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"MediaUsageRow"},
"listCollections": {"method":"GET","path":"/media/collections","contract":"assets","summary":"List collections","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Collection"},
"listMediaAssetVersions": {"method":"GET","path":"/media-assets/{assetId}/versions","contract":"assets","summary":"Every revision, and what replacing it would affect","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetVersion"},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"semanticSearch": {"method":"POST","path":"/search","contract":"ai","summary":"Search meaning, not words","permission":"AI_USE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"SearchResult"},
"setMediaAssetTags": {"method":"PUT","path":"/media-assets/{assetId}/tags","contract":"assets","summary":"Tags and keywords, whoever or whatever supplied them","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTag"},
"setMediaTaxonomy": {"method":"PUT","path":"/media-taxonomy","contract":"assets","summary":"Define categories, fields and keyword vocabularies","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaTaxonomy","responds":"MediaTaxonomy"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Collection": {"x-ticvai-persistence":"assets.media_collection","type":"object","required":["id","name","assetCount"],"properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string","x-ticvai-unique":"tenant","description":"**Unique per tenant** (decided 28 September, audit R108). A name already used by any collection in the tenant, at any venue or level, is refused with `409 duplicate-code`.\n"},"description":{"type":"string","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"parentCollectionId":{"type":"string","format":"uuid","nullable":true},"assetCount":{"type":"integer"},"coverAssetId":{"type":"string","format":"uuid","nullable":true}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetDetail": {"x-ticvai-persistence":"assets.media_asset","allOf":[{"$ref":"#/components/schemas/MediaAsset"},{"type":"object","properties":{"derivatives":{"type":"array","description":"Generated from the original, never uploaded separately. A new breakpoint is a re-render rather than a re-upload of everything.\n","items":{"type":"object","properties":{"label":{"type":"string"},"width":{"type":"integer"},"height":{"type":"integer"},"sizeBytes":{"type":"integer"},"url":{"type":"string"}}}},"usage":{"type":"array","description":"Every place this asset is referenced.","items":{"$ref":"#/components/schemas/MediaUsage"}},"collections":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"name":{"type":"string"}}}},"previousVersions":{"type":"array","items":{"type":"object","properties":{"version":{"type":"integer"},"replacedAt":{"type":"string","format":"date-time"},"replacedByPrincipalId":{"type":"string","format":"uuid"}}}}}}]},
"MediaAssetVersion": {"type":"object","x-ticvai-persistence":"assets.asset_version","description":"Boards 2.6 and 2.7. **Usage impact belongs to the version read**, because replacing a logo is routine or an incident depending on where it appears.\n","properties":{"assetId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"fileName":{"type":"string"},"sizeBytes":{"type":"integer"},"checksum":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"usageImpact":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"surface":{"type":"string","enum":["campaign","journey","ticketTemplate","screen","publishedPage","product","signage"]},"referenceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"live":{"type":"boolean"}}}},"scopePath":{"type":"string"}}},
"MediaDistribution": {"type":"object","description":"Boards 4.2 and 4.5. **The usage map that makes replacement safe.**","properties":{"assetId":{"type":"string","format":"uuid"},"deliveryUrls":{"type":"array","items":{"type":"object","properties":{"channel":{"type":"string"},"rendition":{"type":"string"},"url":{"type":"string"},"cdn":{"type":"string","nullable":true}}}},"usedBy":{"type":"array","items":{"type":"object","properties":{"surface":{"type":"string"},"referenceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"live":{"type":"boolean"}}}},"lastDeliveredAt":{"type":"string","format":"date-time","nullable":true}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaTag": {"type":"object","x-ticvai-persistence":"assets.tag","description":"Board 2.2. **A tag carries its origin and confidence**, so machine labels can be filtered without being deleted.\n","required":["value"],"properties":{"value":{"type":"string"},"vocabulary":{"type":"string","nullable":true},"source":{"type":"string","enum":["human","autoTag","import","inherited"],"default":"human"},"confidence":{"type":"number","nullable":true},"accepted":{"type":"boolean","default":true,"description":"A proposed auto-tag below the promotion threshold sits here as false."},"addedBy":{"type":"string","format":"uuid","nullable":true},"addedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"MediaTaxonomy": {"type":"object","x-ticvai-persistence":"assets.taxonomy","description":"Boards 1.5 and 1.6. **Metadata fields are per asset type**, because an image has dimensions and a contract has an expiry.\n","properties":{"categories":{"type":"array","items":{"type":"object","properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"name":{"type":"string"},"parentCategoryId":{"type":"string","format":"uuid","nullable":true},"applicableAssetTypes":{"type":"array","items":{"type":"string"}}}}},"fields":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"label":{"type":"string"},"dataType":{"type":"string"},"applicableAssetTypes":{"type":"array","items":{"type":"string"}},"mandatory":{"type":"boolean"},"allowedValues":{"type":"array","items":{"type":"string"}}}}},"keywordVocabularies":{"type":"array","items":{"type":"object","properties":{"code":{"type":"string"},"terms":{"type":"array","items":{"type":"string"}},"closed":{"type":"boolean","default":false,"description":"**A closed vocabulary refuses terms not in the list.** Open vocabularies are how a library ends up with `logo`, `logos`, `Logo` and `brand-logo`.\n"}}}},"scopePath":{"type":"string"}}},
"MediaUsage": {"x-ticvai-persistence":"assets.media_usage","type":"object","description":"One place an asset is used. **`surface: product` is written by catalogue** for each item of `Product.media` (decided 29 September, rev 3 23SEP-4): `referenceId` is the product id and `isLive` is true while the product is listed to guests, which is what stops an asset in use on a ticket card being archived from under it.\n","required":["surface","referenceId"],"properties":{"extractedText":{"type":"string","description":"**Text pulled out of an uploaded document**, after extraction. The generic retrieval path for anything a tenant uploads — a PDF nobody can search is a PDF nobody reads.\n"},"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"surface":{"type":"string","enum":["tenantBranding","homepageBanner","promoBlock","contentPage","product","event","menuItem","merchandise","workOrder","incident","inspection","campaign"]},"referenceId":{"type":"string"},"label":{"type":"string"},"isLive":{"type":"boolean","description":"True where the referencing surface is published to guests."}}},
"MediaUsageRow": {"type":"object","description":"Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"assetCount":{"type":"integer"},"storageBytes":{"type":"integer"},"downloads":{"type":"integer"},"views":{"type":"integer"},"shares":{"type":"integer"},"neverUsedCount":{"type":"integer"},"unclassifiedCount":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"SearchResult": {"type":"object","x-ticvai-persistence":"none — computed","properties":{"kind":{"type":"string"},"id":{"type":"string"},"title":{"type":"string"},"excerpt":{"type":"string"},"relevance":{"type":"number"},"collectionId":{"type":"string","format":"uuid","nullable":true},"scopePath":{"type":"string"},"assetId":{"type":"string","format":"uuid","nullable":true,"description":"For kind `media`, the asset (29 September, build; 23.1.6)."},"mediaType":{"type":"string","nullable":true,"enum":["image","video","audio","document"]},"matchedOn":{"type":"string","nullable":true,"enum":["title","description","tags","aiDescription"],"description":"Which text the match came from, so a wrong hit can be traced to a wrong tag."}}},
"UploadTicket": {"x-ticvai-persistence":"assets.media_upload","type":"object","required":["uploadId","uploadUrl","method","expiresAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"uploadId":{"type":"string","format":"uuid"},"uploadUrl":{"type":"string","description":"Signed. PUT the file here, then confirm with `/complete`."},"method":{"type":"string","enum":["PUT","POST"]},"headers":{"type":"object","additionalProperties":{"type":"string"}},"maxSizeBytes":{"type":"integer"},"expiresAt":{"type":"string","format":"date-time"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"venueId":{"type":"string","format":"uuid","nullable":true},"assetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The asset this upload became — created by `completeUpload`, or the asset whose file `replaceMediaAsset` swapped. Null while the transfer is outstanding.\n"}}}
}
```
