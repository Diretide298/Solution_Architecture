# WS75 — Digital Asset Management DAM board 2

**10 screens · 12 operations · 15 schemas · 3 permissions**

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
  `ASSET_LIBRARY_MANAGE, ASSET_LIBRARY_VIEW, ASSET_VIEW`. A control nobody can use must say so,
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
| `CMS-071` | AI Asset Intelligence Command Center | B–D | 0 | 34 | 6 | 0 | 0 | 0 | — | notStarted (—) |
| `CMS-072` | AI Auto-Tagging & Content Understanding | B–D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-073` | Semantic & Natural-Language Asset Search | B–D | 0 | 14 | 6 | 5 | 1 | 0 | — | notStarted (—) |
| `CMS-074` | Visual Similarity & Related Asset Discovery | B–D | 2 | 11 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-075` | Duplicate & Near-Duplicate Management | B–D | 19 | 0 | 6 | 0 | 1 | 2 | — | notStarted (—) |
| `CMS-076` | Asset Version Control & Revision History | B–D | 0 | 0 | 6 | 1 | 1 | 0 | — | notStarted (—) |
| `CMS-077` | Version Comparison & Replacement Impact | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-078` | Transformation & Rendition Management | B–D | 1 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-079` | Rendition Processing & Delivery Readiness | B–D | 0 | 0 | 6 | 0 | 1 | 0 | — | notStarted (—) |
| `CMS-080` | AI Quality, Intelligence Review & Recommendations | B–D | 0 | 18 | 6 | 0 | 1 | 0 | — | notStarted (—) |

## Thin screens in this batch

**CMS-073, CMS-076, CMS-077 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `CMS-071` AI Asset Intelligence Command Center

**Provide DAM administrators and content teams with an overview of AI processing, version activity, duplicate detection, rendition generation, and asset-quality issues.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW`, `ASSET_VIEW` (2 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Display; Show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/ai-asset-intelligence-command-center-cms-071` |

**Known gaps.** **The pack names 5 actions on this screen and the screen declares 0 operations.** Unserved: Review AI Results, Duplicate Review, Version Activity, Rendition Queue, Processing Failures. Each needs an … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Category | picker: choose a category | — | — | `listAssets` ?categoryId |
| Status | select | — | In service · Out of service · Under maintenance · Awaiting parts · Retired · Disposed | `listAssets` ?status |
| Maintenance due | toggle | — | — | `listAssets` ?maintenanceDue |
| From | date and time picker | — | — | `getMediaUsageAnalytics` ?from |
| To | date and time picker | — | — | `getMediaUsageAnalytics` ?to |
| Group by | radio group | — | Asset type · Category · Venue · Owner · Channel | `getMediaUsageAnalytics` ?groupBy |

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Every asset intelligence** (data table)

| Shows | Format | Notes |
|---|---|---|
| AI processed assets | text | not in the schema: `AI-Processed Assets` |
| Pending AI processing | text | not in the schema: `Pending AI Processing` |
| AI tags generated | text | not in the schema: `AI Tags Generated` |
| Duplicate candidates | text | not in the schema: `Duplicate Candidates` |
| Version updates | text | not in the schema: `Version Updates` |
| Renditions generated | text | not in the schema: `Renditions Generated` |
| Processing failures | text | not in the schema: `Processing Failures` |
| Assets requiring review | text | not in the schema: `Assets Requiring Review` |
| Processed | text | not in the schema: `Processed` |
| Queued | text | not in the schema: `Queued` |
| Processing | text | not in the schema: `Processing` |
| Review required | text | not in the schema: `Review Required` |
| Failed | text | not in the schema: `Failed` |
| 95–100% | text | not in the schema: `95–100%` |
| 80–94% | text | not in the schema: `80–94%` |
| 60–79% | text | not in the schema: `60–79%` |
| Below threshold | text | not in the schema: `Below Threshold` |

**The selected asset intelligence** (detail panel)

| Shows | Format | Notes |
|---|---|---|
| AI processed assets | text | not in the schema: `AI-Processed Assets` |
| Pending AI processing | text | not in the schema: `Pending AI Processing` |
| AI tags generated | text | not in the schema: `AI Tags Generated` |
| Duplicate candidates | text | not in the schema: `Duplicate Candidates` |
| Version updates | text | not in the schema: `Version Updates` |
| Renditions generated | text | not in the schema: `Renditions Generated` |
| Processing failures | text | not in the schema: `Processing Failures` |
| Assets requiring review | text | not in the schema: `Assets Requiring Review` |
| Processed | text | not in the schema: `Processed` |
| Queued | text | not in the schema: `Queued` |
| Processing | text | not in the schema: `Processing` |
| Review required | text | not in the schema: `Review Required` |
| Failed | text | not in the schema: `Failed` |
| 95–100% | text | not in the schema: `95–100%` |
| 80–94% | text | not in the schema: `80–94%` |
| 60–79% | text | not in the schema: `60–79%` |
| Below threshold | text | not in the schema: `Below Threshold` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Review AI Results (primary button) | navigation or local | — | — | — | — |
| Duplicate Review (secondary button) | navigation or local | — | — | — | — |
| Version Activity (secondary button) | navigation or local | — | — | — | — |
| Rendition Queue (secondary button) | navigation or local | — | — | — | — |
| Processing Failures (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `listAssets` (onLoad, List assets); `getMediaUsageAnalytics` (onLoad, What the library looks like to AI)

**Where the user goes next**

- → `CMS-001` Tenant Workspace: *Back to Tenant Workspace*
- → `CMS-072` AI Auto-Tagging & Content Understanding: *AI Auto-Tagging & Content Understanding*
- → `CMS-073` Semantic & Natural-Language Asset Search: *Semantic & Natural-Language Asset Search*
- → `CMS-074` Visual Similarity & Related Asset Discovery: *Visual Similarity & Related Asset Discovery*
- → `CMS-075` Duplicate & Near-Duplicate Management: *Duplicate & Near-Duplicate Management*
- → `CMS-076` Asset Version Control & Revision History: *Asset Version Control & Revision History*
- → `CMS-077` Version Comparison & Replacement Impact: *Version Comparison & Replacement Impact*
- → `CMS-078` Transformation & Rendition Management: *Transformation & Rendition Management*
- → `CMS-079` Rendition Processing & Delivery Readiness: *Rendition Processing & Delivery Readiness*
- → `CMS-080` AI Quality, Intelligence Review & Recommendations: *AI Quality, Intelligence Review & Recommendations*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset intelligence list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset intelligence untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset intelligence yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset intelligence are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listAssets` → `ASSET_VIEW` (read) · staff
- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

None names this screen.

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-071` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-071`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 1: Opens AI Asset Intelligence Command Center → Provide DAM administrators and content teams with an overview of AI processing, version activity, duplicate detection, rendition generation, and asset-quality issues.
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 3: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 5: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 7: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 9: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 11: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 13: Returns to the board's landing screen → Ready for the next screen on this board
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 15: Returns to the board's landing screen → Ready for the next screen on this board
- … and 1 more flow steps (`flows/`)
- Flow F184 branch at step 1 (expected): when Nothing has been set up on AI Asset Intelligence Command Center yet, The screen declares `emptyFirstRun`. **On a new tenant this is the expected state**, and it is a different situation from an empty result on an established one.
- Flow F184 branch at step 1 (requiresStaff): when The operator does not hold the permission this screen requires, The screen declares `emptyNoAccess`. **The journey stops here rather than failing later**, which is the right shape -- but the permission that would satisfy it is not granted by any role in …

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (34 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-071?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Review AI Results, Duplicate Review, Version Activity, Rendition Queue, Processing Failures.
- [ ] Every transition is wired: `CMS-001`, `CMS-072`, `CMS-073`, `CMS-074`, `CMS-075`, `CMS-076`, `CMS-077`, `CMS-078`, `CMS-079`, `CMS-080`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`, `ASSET_VIEW`.
- [ ] The module and platform inputs below are applied.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-072` AI Auto-Tagging & Content Understanding

**Automatically analyze uploaded assets and generate useful descriptive metadata.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE` (1 configure); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/ai-auto-tagging-content-understanding-cms-072` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Accept, Reject, Edit, Accept All Above Threshold. Each needs an operation, or needs removing from the … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Edit (secondary button) | navigation or local | — | — | — | — |
| Accept All Above Threshold (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Reject*: **Reject on a auto-tagging content understanding is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The auto-tagging content understanding list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the auto-tagging content understanding untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No auto-tagging content understanding yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the auto-tagging content understanding are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 A tag names a closed vocabulary (`MediaTaxonomy.keywordVocabularies[].closed`) and its value is not one of that vocabulary's terms. |

#### Permissions

- `analyseMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `setMediaAssetTags` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.7 | AI shall automatically generate tags, keywords, and classifications for uploaded assets. | Digital Asset Management | CONTRACTED | `analyseMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI auto-tagging proposes tags with a confidence score shown per tag (e.g. "family" 96%, "children" 94%, "waterpark" 90%). *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-848)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-072` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-072`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 2: Works in AI Auto-Tagging & Content Understanding → Automatically analyze uploaded assets and generate useful descriptive metadata.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (400).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-072?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept, Reject, Edit, Accept All Above Threshold.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-073` Semantic & Natural-Language Asset Search

**Allow users to search based on meaning rather than exact filenames or tags. Board 1 provided structured search.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Each result should show) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/semantic-natural-language-asset-search-cms-073` |

**Known gaps.** **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

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

**Shown**

**Every semantic natural-language asset** (data table)

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset | text | not in the schema: `asset` |
| Relevance score | text | not in the schema: `relevance score` |
| AI tags | text | not in the schema: `AI tags` |
| Matching reason | text | not in the schema: `matching reason` |
| Format | text | not in the schema: `format` |
| Dimensions | text | not in the schema: `dimensions` |

**The selected semantic natural-language asset** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Security”.

| Shows | Format | Notes |
|---|---|---|
| Thumbnail | text | not in the schema: `Thumbnail` |
| Asset | text | not in the schema: `asset` |
| Relevance score | text | not in the schema: `relevance score` |
| AI tags | text | not in the schema: `AI tags` |
| Matching reason | text | not in the schema: `matching reason` |
| Format | text | not in the schema: `format` |
| Dimensions | text | not in the schema: `dimensions` |

**Data it reads**: `searchMedia` (onLoad, Semantic search)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The semantic natural-language asset list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the semantic natural-language asset untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No semantic natural-language asset yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the semantic natural-language asset are still there. Names the active filter and offers to clear it. |
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

- Semantic/natural-language search finds images by visual content (e.g. "children playing in the pool"), not only filename or tags. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-847)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-073` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-073`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 4: Works in Semantic & Natural-Language Asset Search → Allow users to search based on meaning rather than exact filenames or tags. Board 1 provided structured search.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (403).
- [ ] Every output is drawn (14 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-073?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-074` Visual Similarity & Related Asset Discovery

**Allow users to find visually related or similar media.**

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
| Route | `/media-library/visual-similarity-related-asset-discovery-cms-074` |

**Known gaps.** **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Source asset | search field | — | — | — | — | Sends `?assetId=` (required). | `findSimilarMediaAssets` |
| Minimum similarity | number field | — | — | — | — | Sends `?minSimilarity=`. | — |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `findSimilarMediaAssets` ?assetId |
| Min similarity | number field | 0.8 | — | `findSimilarMediaAssets` ?minSimilarity |

#### Outputs: what the screen shows and produces

**Shown**

**Similar assets** (data table, from `findSimilarMediaAssets`): `relation` keeps similar, duplicate candidate and variant apart, as the pack requires; the pack's Version and Rendition are not among its values.

| Shows | Format | Notes |
|---|---|---|
| Asset | the image or video | — |
| Similarity | 1,234.5 | — |
| Relation | chip: Exact duplicate, Near duplicate, Variant, Related | — |
| Differing fields | list or chips (count when long) | — |
| Thumbnail | text | not in the schema: `Thumbnail` |

**The selected match** (detail panel, from `findSimilarMediaAssets`): The pack's Explain Match ("94% - Family, Water Attraction, Outdoor, Daytime").

| Shows | Format | Notes |
|---|---|---|
| Asset | the image or video | — |
| Similarity | 1,234.5 | — |
| Relation | chip: Exact duplicate, Near duplicate, Variant, Related | — |
| Differing fields | list or chips (count when long) | — |
| Similarity factors | text | not in the schema: `Similarity factors` |
| Matched because | text | not in the schema: `Matched because` |

**Data it reads**: `findSimilarMediaAssets` (onLoad, Visually similar and related)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The visual similarity related list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the visual similarity related untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No visual similarity related yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the visual similarity related are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `findSimilarMediaAssets` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-074` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-074`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 6: Works in Visual Similarity & Related Asset Discovery → Allow users to find visually related or similar media.

#### Acceptance for the design

- [ ] Every input above is drawn (2), with its required mark, default, format and its error state.
- [ ] Every output is drawn (11 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-074?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-075` Duplicate & Near-Duplicate Management

**Prevent the DAM from becoming filled with unnecessary copies of identical or nearly identical content.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `mediaId` (navigation) |
| Route | `/media-library/duplicate-near-duplicate-management-cms-075` |

**What the spec says about it.** **Archive and quarantine are reversible; deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA).** Archive Duplicate archives the copy (`updateMediaAsset`, `status: archived`) and can be undone with Restore Archived Copy; Delete Duplicate (`deleteMediaAsset`) removes it for good.

**Known gaps.** **The pack names 7 actions on this screen and the screen declares 0 operations.** Unserved: Exact Duplicate, Near Duplicate, Keep Both, Mark Related, Create Version Relationship, Replace Duplicate … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Asset | upload, or pick from the media library | — | — | `findSimilarMediaAssets` ?assetId |
| Min similarity | number field | 0.8 | — | `findSimilarMediaAssets` ?minSimilarity |

**Form: Archive Duplicate** (confirmDialog, opened by *Archive Duplicate*; *Archive* calls `updateMediaAsset`, *Cancel* sends nothing)

**Archive Duplicate is reversible** (decided 28 September, audit STATE-MEDIA): the copy leaves use and can be restored to `ready`; it is refused while the copy is referenced. Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Title `title` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Description `description` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | — | `updateMediaAsset` body |
| Alt text `altText` | text, one per language | optional | — | — | English and Arabic (Arabic right to left) | Accessibility text. Required before an asset may be used in a guest-facing surface — WCAG 2.2 AA is a stated target. | `updateMediaAsset` body |
| Tags `tags` | list of values (chips) | optional | — | — | — | — | `updateMediaAsset` body |
| Collections `collectionIds` | multi-picker: choose collections | optional | — | — | — | Replaces the asset's collection memberships. Stored as `MediaCollectionMember` rows, one per collection. | `updateMediaAsset` body |
| Rights `rights` | group | optional | — | — | — | Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item. | `updateMediaAsset` body |
| Licence kind `rights.licenceKind` | select | optional | — | Owned · Royalty free · Rights managed · Creative commons · Editorial only · Unknown | — | — | `updateMediaAsset` body |
| Licensor `rights.licensor` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Licence reference `rights.licenceReference` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Valid from `rights.validFrom` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Valid to `rights.validTo` | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | — | `updateMediaAsset` body |
| Permitted uses `rights.permittedUses` | multi-select chips | optional | — | Web · Print · Social media · In venue · Advertising · Internal | — | — | `updateMediaAsset` body |
| Attribution required `rights.attributionRequired` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Attribution text `rights.attributionText` | text field | optional | — | — | — | — | `updateMediaAsset` body |
| Permitted territories `rights.permittedTerritories` | list of values (chips) | optional | — | — | — | ISO country or region codes. Empty means unrestricted, which is a claim rather than an absence — an unknown territory and a worldwide licence are not the same thing, and … | `updateMediaAsset` body |
| Permitted channels `rights.permittedChannels` | list of values (chips) | optional | — | — | — | Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route. | `updateMediaAsset` body |
| Model release held `rights.modelReleaseHeld` | toggle | optional | off | — | — | — | `updateMediaAsset` body |
| Renewal owner `rights.renewalOwner` | picker: choose a renewal owner | optional | — | — | shows names, sends the id | — | `updateMediaAsset` body |
| Status `status` | segmented control | optional | — | Ready · Archived; Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | — | A lifecycle move from `states/media.yaml`. Any transition that model does not give `updateMediaAsset` is refused with 409 `transitionNotAllowed`. | `updateMediaAsset` body |

Errors to draw in the form: 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem)

**Form: Delete Duplicate** (confirmDialog, opened by *Delete Duplicate*; *Delete* calls `deleteMediaAsset`, *Cancel* sends nothing)

**Deletes the copy for good** — deletion is the only end of an asset's life (decided 28 September, audit STATE-MEDIA). Names the copy and the asset it duplicates, lists every reference when refused as in use, and offers Archive instead where the copy may be wanted again.

Sends no fields: a confirmation, not a form.

Errors to draw in the form: 409 Asset is in use. (MediaInUseProblem)

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Exact Duplicate (primary button) | navigation or local | — | — | — | — |
| Near Duplicate (secondary button) | navigation or local | — | — | — | — |
| Keep Both (secondary button) | navigation or local | — | — | — | — |
| Mark Related (secondary button) | navigation or local | — | — | — | — |
| Create Version Relationship (secondary button) | navigation or local | — | — | — | — |
| Replace Duplicate (secondary button) | navigation or local | — | — | — | — |
| Archive Duplicate (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Restore Archived Copy (secondary button) | `updateMediaAsset` PATCH `/media/{mediaId}` | inline | MediaAsset | 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) | opens confirmDialog first |
| Delete Duplicate (destructive button) | `deleteMediaAsset` DELETE `/media/{mediaId}` | — | — | 409 Asset is in use. (MediaInUseProblem) | opens confirmDialog first |

**Data it reads**: `findSimilarMediaAssets` (onLoad, Duplicates above the threshold)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The duplicate near-duplicate list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the duplicate near-duplicate untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No duplicate near-duplicate yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the duplicate near-duplicate are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Asset is in use. (MediaInUseProblem); 409 Status change refused: archiving an asset that is still referenced (`inUse`, with every reference listed), or a transition `states/media.yaml` does not allow … (MediaStatusRefusedProblem) |

#### Permissions

- `findSimilarMediaAssets` → `ASSET_LIBRARY_VIEW` (read) · staff
- `deleteMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff
- `updateMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Visual similarity search finds similar stored images; near-duplicate detection flags near-identical uploads (e.g. 99% similarity) for a keep / replace / discard decision. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-850)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

- **A69** Implement duplicate-account detection and profile-merge functionality (consolidating two profiles into one, carrying over the combined transaction history) *(Softlabs Backend Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 7 Aug 2026 · workshop tracker · keyword 'duplicate-account')*
- **A90** Implement consent-gated duplicate merge (fuzzy name / exact mobile / exact email matching, customer confirmation required, admin review queue, login-of-record rule) *(Softlabs Team · High · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 20 Aug 2026 · workshop tracker · keyword 'duplicate merge')*

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-075` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-075`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 8: Works in Duplicate & Near-Duplicate Management → Prevent the DAM from becoming filled with unnecessary copies of identical or nearly identical content.

#### Acceptance for the design

- [ ] Every input above is drawn (19), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-075?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Exact Duplicate, Near Duplicate, Keep Both, Mark Related, Create Version Relationship, Replace Duplicate, Archive Duplicate, Restore Archived Copy, Delete Duplicate.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-076` Asset Version Control & Revision History

**Maintain controlled versions of the same logical digital asset without creating unrelated master records.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation), `mediaId` (navigation) |
| Route | `/media-library/asset-version-control-revision-history-cms-076` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The asset version revision list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the asset version revision untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No asset version revision yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the asset version revision are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 The upload cannot be used: it is a different kind — an image cannot replace a document (`kindMismatch`) — or the transfer never finished … (UploadRefusedProblem) |

#### Permissions

- `listMediaAssetVersions` → `ASSET_LIBRARY_VIEW` (read) · staff
- `replaceMediaAsset` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

1 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 23.1.8 | System shall maintain historical versions of assets and allow comparison, rollback, and restoration. | Digital Asset Management | CONTRACTED | `replaceMediaAsset` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-076` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-076`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 10: Works in Asset Version Control & Revision History → Maintain controlled versions of the same logical digital asset without creating unrelated master records.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state (409).
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-076?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-077` Version Comparison & Replacement Impact

**Allow users to compare versions and understand the consequences of making a new version current.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/version-comparison-replacement-impact-cms-077` |

**Known gaps.** **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The version comparison replacement list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the version comparison replacement untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No version comparison replacement yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the version comparison replacement are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMediaAssetVersions` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Asset ID persists across versions (e.g. 1.0 -> 1.1); before confirming a replacement the user sees a replacement-impact analysis listing the live channels (kiosk, mobile app, etc.) that use the asset. *(agreed · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-851)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-077` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-077`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 12: Works in Version Comparison & Replacement Impact → Allow users to compare versions and understand the consequences of making a new version current.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-077?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-078` Transformation & Rendition Management

**Generate channel-appropriate media from a master asset without forcing users to manually upload many independent copies.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW` (1 configure, 1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | configEditor (compact density): the pack gives this screen a configuration directory (§Administrators should configure) and no display directory — it is settings, not a population |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/transformation-rendition-management-cms-078` |

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Rendition Presets | select field | — | — | — | — | — | — |

#### Outputs: what the screen shows and produces

**Shown**

**Data table** (data table): **Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows.

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
|  (primary button) | navigation or local | — | — | — | — |
| Cancel (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The transformation rendition configuration as saved. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the transformation rendition untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No transformation rendition configured yet. Carries the create action and says what the platform does in the meantime. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Empty, no results (`?state=emptyNoResults`) | **Nothing matched.** The filter or the scope narrowed it — naming which is what stops somebody concluding the record does not exist |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMediaRenditions` → `ASSET_LIBRARY_VIEW` (read) · staff
- `requestMediaRendition` → `ASSET_LIBRARY_MANAGE` (configure) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-078` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-078`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 14: Works in Transformation & Rendition Management → Generate channel-appropriate media from a master asset without forcing users to manually upload many independent copies.

#### Acceptance for the design

- [ ] Every input above is drawn (1), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-078?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, emptyNoResults, offline.
- [ ] Every action is wired with its success and its failure: , Cancel.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-079` Rendition Processing & Delivery Readiness

**Monitor media-processing jobs and ensure required formats are ready before content is distributed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): **nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than … |
| Offline | online only |
| Opens with | `assetId` (navigation) |
| Route | `/media-library/rendition-processing-delivery-readiness-cms-079` |

**Known gaps.** **The pack names 4 actions on this screen and the screen declares 0 operations.** Unserved: Retry, Cancel, View Error, Regenerate. Each needs an operation, or needs removing from the screen; this is … **The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. … **The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.

#### Inputs: what the user enters or picks

Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.

#### Outputs: what the screen shows and produces

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Retry (primary button) | navigation or local | — | — | — | — |
| Cancel (destructive button) | navigation or local | — | — | — | — |
| View Error (secondary button) | navigation or local | — | — | — | — |
| Regenerate (secondary button) | navigation or local | — | — | — | — |

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Cancel*: **Cancel on a rendition processing delivery is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The rendition processing delivery list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the rendition processing delivery untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No rendition processing delivery yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the rendition processing delivery are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `listMediaRenditions` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- One uploaded image is auto-optimised into channel renditions (mobile app, B2C website, kiosk, etc.); rendition status shows per channel whether each version is ready or missing. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-849)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-079` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-079`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 16: Works in Rendition Processing & Delivery Readiness → Monitor media-processing jobs and ensure required formats are ready before content is distributed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (0 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-079?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Retry, Cancel, View Error, Regenerate.
- [ ] Every transition is wired: `CMS-071`.
- [ ] Every gated control is gated: `ASSET_LIBRARY_VIEW`.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `CMS-080` AI Quality, Intelligence Review & Recommendations

**Provide a governed review workspace for AI results and identify content-quality issues before assets are reused or distributed.**

| | |
|---|---|
| App · platform | TICVAI Venue Management · P13 Venue CMS (web) |
| Module | Media Library · wave 3 · needs the `core` module |
| Block | after Block A (B to D: set per app-module by the sprint plan) |
| Who uses it | venue staff holding `ASSET_LIBRARY_VIEW` (1 read); in the flows as venue manager |
| Device and orientation | This is the back office on a desktop browser, 1440 wide: a left navigation rail with the module sections, a top bar with the venue switcher, and the screen in the main area, with a live preview of … · LTR and RTL · light theme |
| Pattern | listDetail (compact density): the pack gives this screen a display directory (§Track) and no metric row |
| Offline | online only |
| Opens with | nothing: it opens on its own |
| Route | `/media-library/ai-quality-intelligence-review-recommendations-cms-080` |

**Known gaps.** **The pack names 12 actions on this screen and the screen declares 0 operations.** Unserved: Accept Recommendation, Reject, Review Asset, Generate Rendition, Resolve Issue, Board 2 — Shared … **This screen's operations return no schema with described properties**, so not one of its columns can be bound. The columns are the pack's own labels and are carried as text until the response shape …

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

**Every quality intelligence review** (data table)

| Shows | Format | Notes |
|---|---|---|
| Assets processed | text | not in the schema: `Assets processed` |
| Images analyzed | text | not in the schema: `images analyzed` |
| Video minutes analyzed | text | not in the schema: `video minutes analyzed` |
| Audio minutes transcribed | text | not in the schema: `audio minutes transcribed` |
| OCR pages | text | not in the schema: `OCR pages` |
| Embedding generation | text | not in the schema: `embedding generation` |
| Semantic searches | text | not in the schema: `semantic searches` |
| AI requests | text | not in the schema: `AI requests` |
| Estimated/actual AI consumption cost | text | not in the schema: `estimated/actual AI consumption cost` |

**The selected quality intelligence review** (detail panel): The pack groups this record's detail under its own headings: “Digital Asset Management”, “Quality Score”, “Issues”, “Review Queue”, “DAM-IMG-008421”, “Versions”.

| Shows | Format | Notes |
|---|---|---|
| Assets processed | text | not in the schema: `Assets processed` |
| Images analyzed | text | not in the schema: `images analyzed` |
| Video minutes analyzed | text | not in the schema: `video minutes analyzed` |
| Audio minutes transcribed | text | not in the schema: `audio minutes transcribed` |
| OCR pages | text | not in the schema: `OCR pages` |
| Embedding generation | text | not in the schema: `embedding generation` |
| Semantic searches | text | not in the schema: `semantic searches` |
| AI requests | text | not in the schema: `AI requests` |
| Estimated/actual AI consumption cost | text | not in the schema: `estimated/actual AI consumption cost` |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Accept Recommendation (primary button) | navigation or local | — | — | — | — |
| Reject (destructive button) | navigation or local | — | — | — | — |
| Review Asset (secondary button) | navigation or local | — | — | — | — |
| Generate Rendition (secondary button) | navigation or local | — | — | — | — |
| Resolve Issue (secondary button) | navigation or local | — | — | — | — |
| Board 2 — Shared Configuration Requirements (secondary button) | navigation or local | — | — | — | — |
| AI processing enabled/disabled (secondary button) | navigation or local | — | — | — | — |
| supported AI capabilities (secondary button) | navigation or local | — | — | — | — |

**Data it reads**: `getMediaUsageAnalytics` (onLoad, Quality and coverage)

**Where the user goes next**

- → `CMS-071` AI Asset Intelligence Command Center: *Back to AI Asset Intelligence Command Center*

**What opens over it**

- confirmDialog *Reject*: **Reject on a quality intelligence review is not reversible from this screen.** Names what it affects and what it leaves alone. The pack requires the decision to reach the audit trail, so the dialog states that it is recorded.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The quality intelligence review list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the quality intelligence review untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No quality intelligence review yet. Carries the create action; distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | The filter narrowed it and the quality intelligence review are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question. |
| Offline (`?state=offline`) | online only |

#### Permissions

- `getMediaUsageAnalytics` → `ASSET_LIBRARY_VIEW` (read) · staff

**A refused user sees:** Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.

#### Requirements it meets

No matrix row traces to this screen's operations or data.

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- AI quality review flags low resolution, missing information, unsupported renditions or inconsistent formatting, with recommended fixes. *(client request · MoM 11 Sep 2026, 4.2 AI Asset Intelligence, Versioning & Deduplication · DI-852)*

Also apply: 8 for all of P13, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### References

- Wireframe frame: `wireframes/P13 Venue CMS.dc.html#cms-080` · status **notStarted** · provenance —
- Client workshop board: `wireframes/WS45 Digital Asset Management DAM Board 2.dc.html#cms-080`
- Workshop pack: Digital Asset Management DAM.pdf board 2
- Flow F184 *Digital Asset Management DAM board 2: AI Asset Intelligence Command Center*, step 18: Works in AI Quality, Intelligence Review & Recommendations → Provide a governed review workspace for AI results and identify content-quality issues before assets are reused or distributed.

#### Acceptance for the design

- [ ] Every input above is drawn (0), with its required mark, default, format and its error state.
- [ ] Every output is drawn (18 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#CMS-080?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Accept Recommendation, Reject, Review Asset, Generate Rendition, Resolve Issue, Board 2 — Shared Configuration …, AI processing enabled/disabled, supported AI capabilities.
- [ ] Every transition is wired: `CMS-071`.
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

**9 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"analyseMediaAsset": {"method":"POST","path":"/media-assets/{assetId}/analyse","contract":"assets","summary":"Auto-tag, describe and classify an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"deleteMediaAsset": {"method":"DELETE","path":"/media/{mediaId}","contract":"assets","summary":"Delete an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"findSimilarMediaAssets": {"method":"GET","path":"/media-assets/similar","contract":"assets","summary":"Visually similar, near-duplicate and related assets","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":"assetId","in":"query","required":true},{"name":"minSimilarity","in":"query","required":null}],"requestBody":null,"responds":"MediaSimilarity"},
"getMediaUsageAnalytics": {"method":"GET","path":"/media-usage","contract":"assets","summary":"Downloads, views, shares and library health","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"tenant","parameters":[{"name":"from","in":"query","required":null},{"name":"to","in":"query","required":null},{"name":"groupBy","in":"query","required":null}],"requestBody":null,"responds":"MediaUsageRow"},
"listAssets": {"method":"GET","path":"/assets","contract":"maintenance","summary":"List assets","permission":"ASSET_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"venueId","in":"query","required":null},{"name":"categoryId","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"maintenanceDue","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMediaAssetVersions": {"method":"GET","path":"/media-assets/{assetId}/versions","contract":"assets","summary":"Every revision, and what replacing it would affect","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaAssetVersion"},
"listMediaRenditions": {"method":"GET","path":"/media-assets/{assetId}/renditions","contract":"assets","summary":"The derived sizes and formats, and whether they are ready","permission":"ASSET_LIBRARY_VIEW","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"MediaRendition"},
"replaceMediaAsset": {"method":"POST","path":"/media/{mediaId}/replace","contract":"assets","summary":"Replace the file behind an asset","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaReplaceResult"},
"requestMediaRendition": {"method":"POST","path":"/media-assets/{assetId}/renditions","contract":"assets","summary":"Generate a size or format","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"MediaRendition","responds":null},
"searchMedia": {"method":"GET","path":"/media","contract":"assets","summary":"Search the asset library","permission":"ASSET_LIBRARY_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"kind","in":"query","required":null},{"name":"tag","in":"query","required":null},{"name":"collectionId","in":"query","required":null},{"name":"venueId","in":"query","required":null},{"name":"search","in":"query","required":null},{"name":"unusedOnly","in":"query","required":null},{"name":"rightsExpiringWithinDays","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"setMediaAssetTags": {"method":"PUT","path":"/media-assets/{assetId}/tags","contract":"assets","summary":"Tags and keywords, whoever or whatever supplied them","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":null,"conflictPolicy":null,"scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaTag"},
"updateMediaAsset": {"method":"PATCH","path":"/media/{mediaId}","contract":"assets","summary":"Amend metadata, tags or rights","permission":"ASSET_LIBRARY_MANAGE","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"MediaAsset"}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Asset": {"x-ticvai-persistence":"maintenance.asset","allOf":[{"$ref":"#/components/schemas/CreateAssetRequest"},{"type":"object","x-ticvai-retired-columns":["is_maintenance_overdue","document_refs"],"required":["id","status"],"properties":{"id":{"type":"string","format":"uuid"},"resourceId":{"type":"string","format":"uuid","nullable":true,"description":"1.2.x. **Where this asset is also bookable.** An AV rig is an asset to maintain and a resource to allocate, and they are the same object seen from two sides.\n**`resources` owns the calendar and this owns the condition.** An asset out of service makes its resource unbookable, which is one link rather than two models of availability.\n"},"deviceId":{"type":"string","format":"uuid","nullable":true,"description":"BL-160. **Where this asset is also a registered device.** A turnstile is an asset to maintain and a device to operate, and — exactly as with `resourceId` above — they are the same object seen from two sides.\n**Nothing joined them before this.** A turnstile controller reporting `needsAttention` could not raise a work order against itself, and an engineer closing one had no way back to the device whose firmware caused it.\n**Null for most assets and for most devices.** A chiller is not a device and a signature pad is not on the asset register; the link is sparse, and it lives here rather than on `platform.device` because `platform` is the foundation tier and a foreign key pointing from it into `maintenance` would invert the tiers — every cell running a spine would carry a column for a satellite it may not deploy.\n"},"acquisitionCost":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"acquiredOn":{"type":"string","format":"date","nullable":true},"depreciation":{"type":"object","nullable":true,"description":"**Recorded here and posted by `finance`.** Depreciation is an accounting act and the asset register is where the useful life is actually known — an engineer knows a chiller lasts fifteen years and an accountant knows what to do about it.\n","properties":{"method":{"type":"string","enum":["straightLine","reducingBalance","unitsOfProduction","none"]},"usefulLifeMonths":{"type":"integer"},"residualValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"accumulatedDepreciation":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},"retiredOn":{"type":"string","format":"date","nullable":true,"description":"**Retirement is not deletion.** A work order from three years ago still names this asset, and an inspection record with no asset is an inspection of nothing.\n"},"disposalProceeds":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"$ref":"#/components/schemas/AssetStatus"},"statusReason":{"type":"string","nullable":true},"openWorkOrderCount":{"type":"integer","readOnly":true,"x-ticvai-derived":"onWrite","description":"Work orders on this asset whose status is `open`, `assigned`, `inProgress`, `paused` or `awaitingParts` — the same set `AssetDetail.openWorkOrders` returns. **Maintained on write**: `createWorkOrder` and every transition into or out of that set (complete, cancel, close, reject back to open) adjust it in the same transaction as the work-order row.\n"},"nextMaintenanceDueAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"The earliest `nextDueAt` among this asset's active maintenance plans; null when none has one. **Maintained on write**: recomputed whenever one of those plans is created, amended, suspended or has its `nextDueAt` moved by a completed work order. `listAssets?maintenanceDue` filters on this column against the clock.\n"},"isMaintenanceOverdue":{"type":"boolean","readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"`nextMaintenanceDueAt` is in the past at the moment of the read. **Computed on read and not stored** — it depends on the clock, so a stored copy is stale the minute after it is written.\n"},"lastInspectionAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`performedAt` of the latest inspection submitted against this asset. **Maintained on write** by `submitInspection`, in the same transaction as the inspection row; an inspection synced late with an earlier `performedAt` does not move it back.\n"},"usageCounter":{"type":"number","nullable":true,"description":"Cycles, hours or kilometres. Drives usage-based maintenance."}}}]},
"AssetStatus": {"type":"string","enum":["inService","outOfService","underMaintenance","awaitingParts","retired","disposed"]},
"CreateAssetRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["assetTag","name","venueId","criticality"],"properties":{"assetTag":{"type":"string","maxLength":64,"x-ticvai-unique":"venue","description":"**Unique per venue** (decided 28 September, audit R108). Two assets in one venue never share a tag; `createAsset` refuses a duplicate with `409` `duplicate-code`. Two venues may each have an `A-001`.\n"},"name":{"type":"string","maxLength":200},"venueId":{"type":"string","format":"uuid"},"categoryId":{"type":"string","format":"uuid"},"locationDescription":{"type":"string","maxLength":500},"criticality":{"$ref":"#/components/schemas/AssetCriticality"},"priorityOverride":{"allOf":[{"$ref":"#/components/schemas/WorkOrderPriority"}],"nullable":true,"description":"**\"If this device goes down, raise this priority\"** (decided 17 September, M17-01). A corrective work order raised on this asset takes this priority instead of the score. Null means the score decides.\n"},"manufacturer":{"type":"string","maxLength":200},"model":{"type":"string","maxLength":200},"serialNumber":{"type":"string","maxLength":128},"commissionedAt":{"type":"string","format":"date"},"warrantyExpiresAt":{"type":"string","format":"date"},"supplierId":{"type":"string","format":"uuid"},"linkedProductIds":{"type":"array","description":"Products this asset delivers. A fault here can stop them selling.\n","items":{"type":"string","format":"uuid"}},"linkedAccessPointId":{"type":"string","format":"uuid","nullable":true,"description":"Access point this asset controls. Out of service blocks it."},"requiresInspectionToReturn":{"type":"boolean","default":false,"description":"True means a completed inspection is required before return to service. A technician cannot simply declare a ride safe.\n"},"documents":{"type":"array","description":"Manuals, procedures, certificates, each with its name and kind. Stored one row per document in `maintenance.asset_document`, which is where `AssetDetail.documents` reads them from.\n","items":{"$ref":"#/components/schemas/AssetDocumentInput"}},"documentRefs":{"type":"array","x-ticvai-persisted":false,"description":"**The refs alone, kept for callers that predate `documents`.** Each ref sent here is stored as an `asset_document` row with no name and no kind. Returned as the refs of `documents`, computed on read — there is no second copy to fall out of step.\n","items":{"type":"string"}}}},
"LocalisedText": {"x-ticvai-persistence":"none — jsonb column","type":"object","additionalProperties":{"type":"string"}},
"MediaAsset": {"x-ticvai-persistence":"assets.media_asset","type":"object","required":["id","kind","status","filename","contentType","sizeBytes","referenceCount","createdAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MediaKind"},"status":{"$ref":"#/components/schemas/MediaStatus"},"filename":{"type":"string"},"contentType":{"type":"string"},"sizeBytes":{"type":"integer"},"title":{"$ref":"#/components/schemas/LocalisedText"},"description":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Set by `updateMediaAsset` and matched by `searchMedia`'s `search`. It was accepted and searched on before it had anywhere to be stored.\n"},"altText":{"allOf":[{"$ref":"#/components/schemas/LocalisedText"}],"description":"Required before use in a guest-facing surface. WCAG 2.2 AA."},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"durationSeconds":{"type":"number","nullable":true},"customMetadata":{"type":"object","nullable":true,"additionalProperties":true,"description":"BL-178. **`assets` is a strong contract and its metadata was fixed** — kind, title, alt text, dimensions, rights. A venue photographing four thousand products wants its own fields: shoot date, photographer, model release, season.\n**Free-form and searchable, not a schema.** Every venue would want a different one, and a fixed set would be wrong for all of them.\n"},"sharedWithTenantIds":{"type":"array","items":{"type":"string","format":"uuid"},"description":"BL-178. **Cross-tenant sharing, and it is refused by default for a reason.** A brand operating three venues wants one logo library; two unrelated tenants sharing an asset store is the isolation breach ADR-0011 exists to prevent.\n**Only within one tenant's own scope tree.** A share naming a tenant outside it is refused rather than warned about — this is the one place where a permissive default would be a cross-tenant data leak.\n"},"tags":{"type":"array","items":{"type":"string"}},"categoryId":{"type":"string","format":"uuid","nullable":true,"description":"The asset's category, one of `MediaTaxonomy.categories[].id`; null while unclassified. Set by `bulkUpdateMediaAssets` (`setCategoryId`) (decided 29 September, data model DM4).\n"},"venueId":{"type":"string","format":"uuid","nullable":true},"url":{"type":"string","description":"Signed and expiring for private assets; stable CDN URL for public ones."},"thumbnailUrl":{"type":"string","nullable":true},"referenceCount":{"type":"integer","description":"How many surfaces reference this asset. Non-zero refuses deletion.\n"},"rights":{"$ref":"#/components/schemas/MediaRights"},"isRightsExpired":{"type":"boolean"},"version":{"type":"integer"},"uploadedByPrincipalId":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"}}},
"MediaAssetVersion": {"type":"object","x-ticvai-persistence":"assets.asset_version","description":"Boards 2.6 and 2.7. **Usage impact belongs to the version read**, because replacing a logo is routine or an incident depending on where it appears.\n","properties":{"assetId":{"type":"string","format":"uuid"},"version":{"type":"integer"},"fileName":{"type":"string"},"sizeBytes":{"type":"integer"},"checksum":{"type":"string","nullable":true},"createdBy":{"type":"string","format":"uuid"},"createdAt":{"type":"string","format":"date-time"},"note":{"type":"string","nullable":true},"isCurrent":{"type":"boolean"},"usageImpact":{"type":"array","readOnly":true,"items":{"type":"object","properties":{"surface":{"type":"string","enum":["campaign","journey","ticketTemplate","screen","publishedPage","product","signage"]},"referenceId":{"type":"string","format":"uuid"},"label":{"type":"string"},"live":{"type":"boolean"}}}},"scopePath":{"type":"string"}}},
"MediaKind": {"type":"string","enum":["image","video","audio","document","vector","font","archive"]},
"MediaRendition": {"type":"object","x-ticvai-persistence":"assets.rendition","description":"Boards 2.8 and 2.9. **Readiness is the fact that matters**, not existence.","required":["preset"],"properties":{"id":{"type":"string","format":"uuid"},"preset":{"type":"string","description":"e.g. `thumbnail`, `web1600`, `printCmyk`, `hls720`."},"format":{"type":"string","nullable":true},"width":{"type":"integer","nullable":true},"height":{"type":"integer","nullable":true},"sizeBytes":{"type":"integer","nullable":true},"status":{"type":"string","enum":["queued","processing","ready","failed"]},"failureReason":{"type":"string","nullable":true},"url":{"type":"string","nullable":true},"scopePath":{"type":"string"}}},
"MediaReplaceResult": {"x-ticvai-persistence":"none — computed","type":"object","required":["asset","affectedSurfaces"],"properties":{"asset":{"$ref":"#/components/schemas/MediaAsset"},"affectedSurfaces":{"type":"integer","description":"How many surfaces now show the new file."},"liveSurfaces":{"type":"integer","description":"Of those, how many are published to guests right now."},"derivativesRegenerating":{"type":"boolean"}}},
"MediaRights": {"x-ticvai-persistence":"none — embedded in asset","type":"object","description":"Licensing terms. Tracked because an expired licence on a live surface is a legal exposure, not a housekeeping item.\n","properties":{"licenceKind":{"type":"string","enum":["owned","royaltyFree","rightsManaged","creativeCommons","editorialOnly","unknown"]},"licensor":{"type":"string","nullable":true},"licenceReference":{"type":"string","nullable":true},"validFrom":{"type":"string","format":"date","nullable":true},"validTo":{"type":"string","format":"date","nullable":true},"permittedUses":{"type":"array","items":{"type":"string","enum":["web","print","socialMedia","inVenue","advertising","internal"]}},"attributionRequired":{"type":"boolean","default":false},"attributionText":{"type":"string","nullable":true},"permittedTerritories":{"type":"array","items":{"type":"string"},"description":"ISO country or region codes. **Empty means unrestricted, which is a claim rather than an absence** — an unknown territory and a worldwide licence are not the same thing, and `licenceKind: unknown` is how the second is said.\n"},"permittedChannels":{"type":"array","items":{"type":"string"},"description":"Distribution channel codes, checked by `setMediaDistributionChannels`. Narrower than `permittedUses`, which describes the medium rather than the route.\n"},"modelReleaseHeld":{"type":"boolean","default":false},"renewalOwner":{"type":"string","format":"uuid","nullable":true}}},
"MediaSimilarity": {"type":"object","description":"Boards 2.4 and 2.5. **Duplicate and related are one score at two thresholds.**","properties":{"assetId":{"type":"string","format":"uuid"},"similarity":{"type":"number"},"relation":{"type":"string","enum":["exactDuplicate","nearDuplicate","variant","related"]},"differingFields":{"type":"array","items":{"type":"string"}}}},
"MediaStatus": {"type":"string","enum":["processing","ready","quarantined","failed","archived"]},
"MediaTag": {"type":"object","x-ticvai-persistence":"assets.tag","description":"Board 2.2. **A tag carries its origin and confidence**, so machine labels can be filtered without being deleted.\n","required":["value"],"properties":{"value":{"type":"string"},"vocabulary":{"type":"string","nullable":true},"source":{"type":"string","enum":["human","autoTag","import","inherited"],"default":"human"},"confidence":{"type":"number","nullable":true},"accepted":{"type":"boolean","default":true,"description":"A proposed auto-tag below the promotion threshold sits here as false."},"addedBy":{"type":"string","format":"uuid","nullable":true},"addedAt":{"type":"string","format":"date-time"},"scopePath":{"type":"string"}}},
"MediaUsageRow": {"type":"object","description":"Boards 1.10 and 4.9. **Assets never used is the number that justifies the library.**","properties":{"key":{"type":"string"},"label":{"type":"string"},"assetCount":{"type":"integer"},"storageBytes":{"type":"integer"},"downloads":{"type":"integer"},"views":{"type":"integer"},"shares":{"type":"integer"},"neverUsedCount":{"type":"integer"},"unclassifiedCount":{"type":"integer"}}},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}}
}
```
