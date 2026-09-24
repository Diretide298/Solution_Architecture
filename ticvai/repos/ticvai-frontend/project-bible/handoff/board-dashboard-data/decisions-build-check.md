# D-001 … D-008 — what already exists in the build

Checked against `d:\Chinmay\adam\ticvai` on 22 September 2026. Every claim below cites a file and a
line or a table name. Decision wording quoted from
`handoff/board-dashboard-data/decision-register.jsonl` (the register's own `question` field), which is
more precise than the `.md` summary table and is what I verified against.

## A fact that applies to all eight

**`implementation.status` carries no information in this package.** Every `status:` field in
`screens/P*.yaml` — 4,854 of them, covering both `implementation.status` and `wireframe.status` —
reads `notStarted`. There is not one other value anywhere. So the only distinction that discriminates
is *specified but unbuilt* versus *not specified at all*, exactly as the brief suspected. I have used
"does a screen for this exist in `screens/P*.yaml`" as the test throughout, and where a screen exists
I have said what it declares.

---

## D-001 — one section/tab IA for the configEditor frames

**Verdict: wrong question.**

**What exists.** The `configEditor` pattern is defined at `screens/_patterns.yaml:229-267`. It has
three required slots — `scope` (a `selectField`, *"What this configuration applies to — tenant, venue,
outlet"*), `fields` (form controls, `bindsTo: required`), and `publish` (a `publishGate`) — plus two
overlays (`confirmPublish`, `discard`) and `fetch.shape: singleFetch`. **504 screens across 14 of the
16 apps declare `pattern: configEditor`** (P08: 248, P09: 163, P13: 23, P16: 16, P10: 12, P02/P06: 9
each, rest smaller). It is by a wide margin the most-used pattern in the package.

**What is genuinely absent — and it is not what the decision says.** Three separate facts:

1. **The component library has no tab primitive.** `screens/_components.yaml` defines 47 component
   kinds (`dataTable`, `cardList`, `detailPanel`, `metricTile`, `chart`, `timeline`, `emptyState`,
   `textField`, `numberField`, `selectField`, `multiSelect`, `datePicker`, `toggle`, `searchField`,
   `fileUpload`, `signaturePad`, `primaryButton`, `secondaryButton`, `destructiveButton`, `iconButton`,
   `banner`, `toast`, `modal`, `confirmDialog`, `progressIndicator`, `duplicateMatch`, `publishGate`,
   `credentialDisplay`, `drawer`, `scanTarget`, `seatMap`, `assistantPanel`, `saleBoard`, `cartPanel`,
   `paymentTerminal`, `queuePosition`, `assetTag`, `consentBlock`, `livePreview`, `treeNav`,
   `codeBlock`, and 6 composites). **None of them is a tab, tab bar, section nav or stepper.**
2. **No screen in the package declares a tab list.** `grep` for `tabs:` / `sections:` / `kind: tabBar`
   across all 16 `screens/P*.yaml` returns nothing. The `configEditor` pattern has no section slot
   either.
3. **Most of the frames the 21 rows name do not exist as screens.** Reschedule Rules, Exchange Rules,
   Upgrade Rules, Downgrade Rules, Convert, Ownership Transfer (the ticketing one), Delivery Rules,
   Physical Media, Wallet (the ticketing frame), Draft & Edit Workspace, Association Impact Preview —
   none is in the screen register. The rows come from source pack `TICKETTYPES-p10` (Service Policies,
   Associations, Lifecycle & Governance sections), not from screens. The only near-matches in the
   register are unrelated: *Apple/Google Wallet Pass Designer* (BO), *Ticket Ownership Transfer
   Management* (ADM-…), *Version History* (P13 CMS).

**Whether any screen specifies it.** No. Every one of the 504 configEditor screens lays out flat
`fields` regions with `selectField`/`toggle`/`textField` components; e.g. BO-885 *Minimum Staffing &
Coverage Rule Configuration* (`screens/P08-venue-back-office.yaml:103012`) has one `contentBody/fields`
region with five `selectField`s and nothing else.

**Is the decision the right question.** No, and it is the clearest "would design something that
already exists / does not exist" in the set. The register frames it as *"nineteen-plus config frames
each declare their own tab list — do we run one IA pass or does every frame keep a bespoke tab list?"*
**Neither branch is true of the build.** Nothing declares a bespoke tab list because nothing declares
tabs at all, and nineteen of the frames are not screens. The real decision, in order, is:

- (a) does the component library gain a `tabSet`/`sectionNav` primitive at all, or does `configEditor`
  stay a single scrolling form with headings (this is D-018's territory — *"Add the missing canvas,
  grid and stepping components to the component library"* — and D-001 and D-018 are the same decision
  split across two register entries);
- (b) only if (a) is yes, what the standard section set is;
- (c) separately, whether the ~19 Ticketing Service-Policy / Association / Lifecycle frames enter the
  screen register at all.

Answering (b) first would produce an IA for screens that do not exist, expressed in a component the
library cannot render.

---

## D-002 — `DashboardTile.visualisation` (calibration)

**Verdict: partly built — and the register understates the gap.**

**What exists.** `contracts/satellite/reporting.yaml:3240` `DashboardTile`
(`x-ticvai-persistence: reporting.dashboard_tile`), whose `visualisation` at **:3256-3265** is a closed
enum of exactly **eight** members:

```
number, line, bar, stackedBar, pie, table, gauge, heatmap
```

Also present and relevant: `ReportColumn` (:2732, `reporting.report_column`) with
`field / label / aggregation / sortOrder / sortDirection / format`; `Aggregation` (:2720) with
`none…count, countDistinct, sum, average, min, max`; `ReportFilter` (:2765) with a ten-operator enum
and `isParameter: true` for run-time prompting; `ReportParameter` (:2810); `Dashboard` (:3320).

**Confirmed against the source.** `sources/requirements/Ticketing_Platform_Native_Dashboard_Visualization_Requirements.pdf`
(rows `MOM-2641`–`MOM-2908`). Parsing every row of the form *"The X visual/control shall … as an
MVP-priority component"* yields exactly **18 named components, all MVP**:

> KPI / card, bar / column, line / area, combo, pie / donut, table, matrix / pivot, slicer / filter,
> gauge / progress, funnel, waterfall, treemap, scatter / bubble, map, heatmap, ribbon / rank,
> decomposition tree, narrative / insight text

**Two corrections to the register's framing.**

1. **The register's list of what to add is wrong in both directions.** It names *"combo, matrix/pivot,
   funnel, waterfall, treemap, scatter/bubble, map, ribbon/rank, cohort and narrative text"*. **Cohort
   is not one of the 18** — it appears only in `MOM-2802` as a dashboard *usage* ("the Customer &
   Membership dashboard shall use cards, cohort and trend charts, a map and a matrix"), never as a
   specified visual. **Decomposition tree is one of the 18 and the register omits it.** Mapping the
   existing eight onto the source list (`number`→KPI/card, `bar`+`stackedBar`→bar/column layouts,
   `line`→line/area, `pie`→pie/donut, `gauge`→gauge/progress, `table`, `heatmap`), the marks genuinely
   missing are **nine**: combo, matrix/pivot, funnel, waterfall, treemap, scatter/bubble, map,
   ribbon/rank, decomposition tree. Two further source entries are **not marks at all** and must not
   join this enum: **slicer / filter** is a control, and the platform already has it as
   `ReportFilter.isParameter` + `ReportParameter`; **narrative / insight text** is generated prose and
   belongs with `ai.Suggestion`, not with a tile's mark.
2. **A third layer disagrees, and nobody has noticed.** `screens/_components.yaml:182` defines the
   `chart` component as *"Line, bar, pie, gauge. Rendered from a report definition."* — **four** marks.
   So the package holds three different answers to "what can be drawn": the source pack says 18, the
   contract enum says 8, the component library says 4. Extending the enum without extending the
   component's description leaves the screens unable to declare the new marks.

**The larger absence the register buries in a sub-clause.** The register's own question ends *"and for
each accepted mark, how do report columns bind to its axes, size and colour?"* — **there is no
encoding model at all.** `ReportColumn` has no `role` / `axis` / `channel` field. A `number` tile needs
no encoding and an eight-mark enum survived without one; a scatter/bubble needs x, y, size and colour,
and a combo needs a secondary axis with stated units (`MOM-2653`). Adding nine marks without adding
`ReportColumn.role` produces nine marks nothing can bind data to. **This half is the harder and
costlier decision and should be split out.**

**Whether any screen specifies it.** Yes — seven, all `notStarted`: P16 ANL *Live Operations
Dashboard* (:1728), *Dashboard Library* (:2851), *Dashboard Creation Wizard* (:3057),
*Drag-and-Drop Dashboard Canvas* (ANL-023, `screens/P16-venue-analytics.yaml:3179`),
*Dashboard Access, Publishing & Versioning* (:3898), *Dashboard Preview, Validation & Health* (:4004),
*AI-Generated Dashboard Studio* (:6738).

---

## D-003 — is a catalogue a first-class object, and how do channels bind to it

**Verdict: partly built — the channel half is done, the catalogue half is genuinely absent.**

**What exists.**

- **The channel vocabulary is settled and used twice.** `Channel` is a closed seven-member enum,
  identical in `contracts/spine/catalogue.yaml:10436` and `contracts/spine/orders.yaml:10701`:
  `pos, kiosk, web, mobile, b2b, ota, callCentre`. The register's own question asks how channels bind
  "to it" as though the channel vocabulary were open; it is not. (D-022 separately asks to *"fix the
  closed sales-channel vocabulary"* — same enum, and it is already closed and already shared.)
- **`catalogue.channel_allocation`** (`ChannelAllocation`, spine/catalogue.yaml:11212) already binds a
  channel to inventory: `channel`, `allocatedUnits`, `soldUnits`, `leasedUnits`, `remainingUnits`,
  `releaseAt`, with `generalPoolUnits` as the unallocated remainder on `channel_capacity`.
- **The price book exists.** `catalogue.price_list` (`code, name, venue_id, valid_from, valid_to,
  priority`) + `catalogue.price` (`price_list_id, variant_id, amount, tax_code_id`).
- **Three of the register's five "catalog types" already exist as a category kind.**
  `ProductCategory.kind` (spine/catalogue.yaml:9773) is `category, brand, collection, season,
  department`, over a single `parentId` tree (*"One tree, not four"*). `collection` and `season` are
  precisely the *Seasonal* / *Segment* catalogue types the rows ask for, and the "saved filter" branch
  of the decision is therefore already half-implemented.
- **The per-venue published bundle exists.** `catalogue.published_bundle` / `CatalogueBundle`
  (:11322) and `BundleSummary` (:11280) — version, venueId, isDelta, signature, contentHash,
  staleAfter, payload, appliedByWorkstations. This is the register's stated status-quo branch.
- **An OTA-facing per-channel product listing exists, and it is not the same thing.**
  `ChannelListing` (`contracts/satellite/subscription.yaml:6791`, `control.channel_listing`) carries
  `channelName` (`viator, klook, headout, getYourGuide, tiqets, expedia, other`), `productId`,
  `externalProductRef`, `status` (`draft, live, paused, delisted`), `allocationUnits`, **`priceListId`**,
  `adapter` (incl. `octoStandard`). Note the trap: it answers *"which products, at which price book,
  on which channel"* — but only for third-party OTA distribution, **not** for the on-site / online /
  kiosk retail channels `MOM-2206` and `MOM-4553` are about. Someone searching "channel listing" will
  find it and wrongly conclude the decision is closed.

**What is genuinely absent.** There is **no `Catalogue` / `Assortment` row anywhere** — no table in
`handoff/schema-reference.json` named `catalogue.catalogue`, `*.assortment` or equivalent; nothing
carrying a catalogue *name*, *type* (Global / Park / Seasonal / Event / Segment), *scope* (All Stores /
a named store group / VIP Stores), *status* (Draft / Scheduled / Published), *product count* or *last
updated*. And nothing binds an **outlet or store group** to a catalogue: `retail.merchandise` has
`outlet_id` per item, so retail assortment is currently expressed one SKU at a time.

**Whether any screen specifies it.** Partly, and revealingly.

- The two screens the rows come from — *Retail Product & Catalog Command Center* (`RETAIL-p02`) and
  *Catalog Builder & Store Assortment* — **are not in the screen register**.
- But **ADM-260 *Product & Catalogue Assignment*** is (`screens/P09-platform-admin-console.yaml:32503`,
  route `/commercial/product-catalogue-assignment-adm-260`, `pattern: listDetail`, status
  `notStarted`), purpose *"Control exactly which products are available through each sales channel."*
  It declares `setProductCatalogue` (`contracts/spine/catalogue.yaml:4276`) and binds to
  `ProductCatalogueAssignmentView` (:13208). That view is
  **`x-ticvai-drafted-shape: true`, `x-ticvai-persistence: none — projection over catalogue state`**,
  and every property is an untyped `string`: `individualProduct`, `productFamily`, `productCategory`,
  `event`, `attraction`, **`venueCatalogue`**, **`productCollection`**, **`entireApprovedCatalogue`**,
  `product`, `productType`, `venue`, `status`, `validity`, `channelStatus`, `pricingStatus`,
  `capacityStatus`, `effectiveFrom`, `effectiveTo`. The screen also records a gap: *"The pack names 6
  actions on this screen and the screen declares 1 operation. Unserved: Assign Products, Remove
  Products, Disable, Copy Assignment, Import Assignment."*

**Is the decision the right question.** Yes, and it is one of the two best-posed in the set — but it
should be told three things it does not currently know: (i) the channel enum is already closed and
shared, so only the *catalogue* object is at stake; (ii) `ProductCategory.kind` already carries
`collection` and `season`, so the "saved filter" branch is cheaper than the register implies; (iii)
whichever branch wins, `ProductCatalogueAssignmentView` — an eighteen-string stub with a
free-text `venueCatalogue` — is what gets replaced, and `setProductCatalogue` is the operation that
must be re-shaped. A decision taken without (iii) will leave a second, contradictory catalogue model
live in the spine.

---

## D-004 — extend `ApprovalKind` to the acts the screens gate

**Verdict: partly built — and materially more built than the register says.**

**What exists.** `contracts/spine/approvals.yaml:2563` `ApprovalKind`, a closed enum of **fifteen**
members:

```
refund, priceOverride, discountOverride, complimentaryTicket, membershipCancellation,
accessPermissionChange, configurationChange, aiRecommendation, shiftVariance, releasePromotion,
requisition, stockWriteOff, journalEntry, periodReopen, tenantMigration
```

Around it, a complete approvals engine already exists — this is the part the register's wording hides:

- `ApprovalStatus` (:2585): `draft, pending, escalated, approved, rejected, withdrawn, expired, cancelled`
- `ApprovalMode` (:2596): `sequential, parallel, consensus, majority` (with an explicit note on why
  parallel ≠ consensus)
- `ApprovalRule` (:2610) — `order`, `approverRoleIds`, `mode`
- `ApprovalMatrix` (:2691), read and written by `listApprovalMatrices` (:516) / `setApprovalMatrix` (:558)
- `evaluateApprovalRequirement` (:208) — the pre-flight call, taking `kind`, `scopePath`, `amount` and
  free-form `attributes` *"whatever the conditional rules match on"*
- `createApprovalRequest` (:149), `decideApprovalRequest` (:273), `withdrawApprovalRequest`,
  `escalateApprovalRequest`, `resubmitApprovalRequest`, delegations
  (`listApprovalDelegations` / `createApprovalDelegation` / `revokeApprovalDelegation`),
  `getApprovalAnalytics`, `setApprovalSlaPolicy`, `setApproverAvailability`, `signApprovalDecision`,
  `getApprovalRecord`, `setApprovalRetentionPolicy`, `createApprovalEvidencePackage`, `setStepUpPolicy`,
  `setApprovalControlPolicy` — **46 operationIds in the contract.**
- **The amount-band shape the register asks for already has a canonical form.**
  `orders.RefundPolicy` (`contracts/spine/orders.yaml:11350`, `orders.refund_policy`) carries
  `selfAuthoriseLimit` / `requiresSecondUserAbove` / `requiresApprovalAbove`, with the reasoning
  written down: *"Thresholds are policy, not permission scope."* `retail.return_policy` mirrors it
  field-for-field (`self_authorise_limit`, `requires_second_user_above`, `requires_approval_above`).
  `MOM-4166` (Adjustment Approval Limit in AED) and `MOM-4168` (Transfer Approval Limit in AED) are
  asking for exactly this shape in `inventory` — **and it does not exist there.**

**What is genuinely absent.** Two things, of which only the first is in the register's title.

1. The thirteen acts named by the rows are not enum members: check-in/check-out correction
   (`MOM-7005`), complimentary F&B (`MOM-3495`), stock adjustment (`MOM-4154`), stock transfer
   (`MOM-4168`), inventory reopen after operational cancellation / manual void (`MOM-6867/6868`),
   manual entitlement activation (`MOM-6585`), purchase order / supplier contract / supplier approval /
   budget (`MOM-4298`), overtime / resource override / shift swap (`MOM-6199`). Note `complimentaryTicket`
   exists but is ticket-specific — `MOM-3495` is about complimentary **F&B items** at Manager Level 2.
2. **The far bigger absence: 26 free-standing `requiresApproval` booleans across 12 contracts, none of
   which reaches `ApprovalKind`.** Found by grepping `requiresApproval|requires_approval|approvalRequired`
   outside `approvals.yaml`: `spine/access.yaml:10480`, `spine/catalogue.yaml:9473, :11070
   (requiresApprovalToCancel), :20924`, `spine/orders.yaml:601, :10055, :11389, :13632, :13702`,
   `satellite/ai.yaml:2043 (requiresApprovalFor)`, `satellite/fnb.yaml:5626, :5802`,
   `satellite/marketing-crm.yaml:10601`, `satellite/platform-ops.yaml:2136 (requiresApprovalToPromote)`,
   `satellite/resources.yaml:2533`, `satellite/retail.yaml:1495, :1522`,
   `satellite/subscription.yaml:7192, :11904`, `satellite/wallet.yaml:3230`,
   `satellite/workforce.yaml:2128 (WorkforceLeaveType.requiresApproval), :2345
   (StaffingRules.overtime.requiresApproval)`. Each of these is a toggle that, when true, has **no
   named route into the approvals engine** — no kind, no matrix row, no SLA, no delegation. Three of
   them are literally the acts `MOM-6199` names (overtime, resource override, shift swap) and are
   already modelled as booleans rather than as approval kinds.

**Whether any screen specifies it.** Yes, extensively, all `notStarted`. In P08 alone:
*Approval Inbox* (:19033), *Approval Request* (:19190), *Approval Matrix* (:19381),
*Approval Delegations* (:19506), *Approval Analytics* (:19660), *Approval Command Center Dashboard*
(:53500), *My Approval Inbox* (:53667), *Team / Shared Approval Queue* (:53775),
*Approval Request Detail* (:53851), *Escalated Approval Center* (:54102),
*Completed Approval History* (:54217), *Approval SLA & Workload Monitor* (:54302),
plus *Refund Approval Queue* (:6788) and *Variance Approval* (:9514) — the latter already served by
the existing `shiftVariance` kind.

**Is the decision the right question.** Half of it. *"Which of these become `ApprovalKind` values, and
what role, level and amount band does each take on the `ApprovalMatrix`"* is correct and buildable —
the matrix, the modes, the delegations and the SLA are all there, so this is a list of enum members
plus a set of matrix rows, **not a design task.** But the decision as scoped will miss two things that
cost more: (a) the 26 orphan `requiresApproval` booleans, which need a ruling on whether each is
replaced by an `ApprovalKind` or kept as a local flag; and (b) the fact that the amount bands
`MOM-4166`/`MOM-4168` want already exist verbatim in `orders.RefundPolicy` and `retail.return_policy`
and just need an inventory sibling — whoever answers D-004 should be told to copy that shape rather
than invent a third.

---

## D-005 — type the stock location hierarchy (calibration)

**Verdict: genuinely absent — but the register's evidence is wrong about screens, and one input is
already solved.**

**What exists.**

- **`StockLocation`** — `contracts/satellite/inventory.yaml:2882`, `x-ticvai-persistence:
  inventory.location`. Its entire property set is: `id, code, name, venueId, kind, parentLocationId,
  isActive`. That is all. `parentLocationId` gives an arbitrary-depth tree, so the *hierarchy* is
  expressible; nothing about a level is typed.
- **`LocationKind`** — **`contracts/satellite/inventory.yaml:2777-2786`** (the register's citation
  *"3290-3300"* is wrong), a seven-member closed enum:
  `mainStore, subStore, kitchen, bar, retailFloor, cellar, transit`. Note what these are: **outlet
  types, not storage levels.** There is no `warehouse`, no `zone`, no `bin`, no `pickFace`, no
  `receivingDock`. `listStockLocations` (:774) describes them in prose as *"Stores, bars, kitchens,
  retail floors, cellars"*.
- **Operations:** `listStockLocations` (:774, `PRODUCT_VIEW`, offline-capable) and
  `createStockLocation` (:805, `PRODUCT_CONFIGURE`) — whose request body accepts only
  `code, name, venueId, kind, parentLocationId`.
- **Temperature class — solved, as stated in the brief.** `fnb.TemperatureCheckpoint`
  (`contracts/satellite/fnb.yaml:5453`, `fnb.temperature_checkpoint`) carries `kind` as a closed
  eight-member enum — `fridge, freezer, holdingCabinet, blastChiller, coreProbe, delivery,
  displayCounter, ambient` — plus `minCelsius` / `maxCelsius` (either may be null, *"a core probe has a
  floor and no ceiling"*, both null is an unconfigured checkpoint), `checkFrequencyMinutes`,
  `requiresCorrectiveActionOnBreach`, `outletId`, `label`, `isActive`, `scopePath`. Read/written by
  `listTemperatureCheckpoints` (:2467) and `setTemperatureCheckpoint` (:2502). **`MOM-4002`'s
  "Ambient or 0-4 °C" and `MOM-4008`'s "Temperature Class" are both fully expressible today** — the
  enum member and the min/max pair already exist and are already snapshotted onto each reading.
- **`StockPosition`** (:2909, `x-ticvai-persistence: none — derived from movements`) already gives
  `itemId, locationId, locationName, onHand, allocated, available, unit, value, lastCountedAt,
  lastMovementAt` — i.e. the **numerator** of any utilisation figure is already derivable per location.

**What is genuinely absent.**

- **Capacity on a stock location, in any unit.** Searching every column in
  `handoff/schema-reference.json` for `capacit|utilis|utiliz` finds capacity on seats
  (`seating.zone.capacity`), spaces (`catalogue.space.maximum_capacity` / `safe_capacity`), dining
  tables (`fnb.dining_table.capacity`), queues (`queue.queue.capacity_per_cycle`), parking
  (`access.parking_facility.capacity`), rides (`games.operational_config.rider_capacity`), sessions
  (`catalogue.session_template.concurrent_capacity`) and channels
  (`catalogue.channel_capacity.capacity`) — **and on no inventory location.** There is no capacity
  unit register either (units / m³ / pallet positions / kilograms), which is D-040's subject.
- **Utilisation.** The only `utilisation` column in all 635 tables is
  `control.scaling_policy.target_utilisation_pct`, which is infrastructure autoscaling. Nothing
  computes or stores a location's used-versus-total percentage (`MOM-3949`).
- **Volume, contact person, address** (`MOM-3948`, `MOM-4004`) — and note there is **no shared
  `Address` or `Contact` schema in `contracts/shared/common.yaml`** to reuse, so this is not a
  one-line `$ref`.
- **Bin / zone / pick-face / dock as typed levels** (`MOM-4008`, `MOM-4009`, `MOM-4010`, `MOM-4013`).
  `parentLocationId` can hold the shape; `LocationKind` cannot name it. There is no `dock` concept on
  `inventory.goods_receipt` either (`MOM-4013`).

**Whether any screen specifies it.** **No — and this is the register's factual error.** Its
`why_it_matters` says *"Warehouse, zone, bin and utilisation screens all read fields that do not
exist."* There are **no warehouse, zone or bin screens in the package.** The only screen with
"Warehouse" in its name is **EMP-064 *Store-to-Store & Warehouse Transfers*** (P06 staff app), which
is a transfer screen. The Zone screens that exist are all seating / access / venue-map
(*Zones & Areas*, *Access Area & Zone Builder*, *Sections & Zones*, *Standing Zones*, *Venue & Zone
Access Matrix*) — none is a storage zone. The ten rows come from source pack pages `INVPROC-p01` and
`INVPROC-p02`, not from screens.

The one screen that *would* be the home is **BO-510 *Inventory Location Allocation***
(`screens/P08-venue-back-office.yaml:67674`, module Rentals, route
`/rentals/inventory-location-allocation-bo-510`, `pattern: listDetail`, status `notStarted`), purpose
*"Manage how inventory is distributed among rental locations."* It declares only `listStockLocations`
and `createStockLocation`, has a derived `dataTable` and a create button, and carries two explicit
gaps: *"The pack gives this screen nothing that can be drawn. Its sections are prose … The screen has
no content region rather than an empty one, and it needs a person before it is built."* Its
`apisNote` reads *"0 of 0 labels bound to a contract property; 0 of 15 pack bullets carried onto the
screen."*

**Is the decision the right question.** Yes on substance, but its four clauses are not one decision
and its premise about screens is false. Specifically:

- **The temperature clause is already answered** and should be struck. The register asks whether to
  *"reuse `fnb.TemperatureCheckpoint.kind` or a new set; free-text spec or min/max Celsius"* — as of
  today the eight-member `kind` enum and the `minCelsius`/`maxCelsius` pair both exist and are in
  production use by `TemperatureLog`. The residual question is one line: does `StockLocation` gain a
  `temperatureCheckpointId` (or a denormalised `kind` + range), and does a checkpoint attach to a
  location as well as to an `outletId`.
- **The capacity/utilisation clause has a precedent to copy**, not a model to invent:
  `catalogue.space` already runs `maximumCapacity` + `safeCapacity` as a pair, and `StockPosition`
  already derives the used figure. "Is utilisation stored or derived" answers itself — derived, from
  `StockPosition`, exactly as `StockValuation` is.
- **The `LocationKind` clause is the only genuinely open one** and it is the load-bearing one: adding
  `warehouse, zone, bin, pickFace, receivingDock` to a seven-member enum that currently means *outlet
  type* mixes two axes in one field. The alternative — a separate `level` field, with `kind` kept for
  what the place is used for — is not on the register and should be.
- **Nothing should be built until BO-510 (or a real warehouse screen) exists**, because the current
  screen explicitly says it has no drawable content.

---

## D-006 — are supplier compliance documents their own register

**Verdict: wrong question — a complete document register already exists, one contract away.**

**What exists on the supplier side.** Very little. `inventory.supplier` (`Supplier`,
`contracts/satellite/inventory.yaml:3495`) carries `id, code, name, contactName, contactEmail,
contactPhone, taxRegistrationNumber, paymentTermsDays, leadTimeDays, currency, accountId, isActive,
scopePath`. `inventory.supplier_contract` (`InventorySupplierContract`, :2562) carries `id, supplierId,
number, name, validFrom, validTo, currencyCode, paymentTermsDays, **documentReference**, status,
createdByPrincipalId, createdAt`. `documentReference` is a single free-text string on a contract —
one document, no type, no expiry of its own, no verification.

Grepping `compliance|certificat|insurance|licence|license` across
`contracts/satellite/inventory.yaml` returns **zero hits.** There is no supplier document table in
`handoff/schema-reference.json`.

**What already exists elsewhere, and is the whole answer.**
**`accreditation.document` / `AccreditationDocument`** — `contracts/satellite/accreditation.yaml:1443`.
It is exactly the register D-006 describes, already specified:

| what D-006 asks for | `AccreditationDocument` |
|---|---|
| a document row of its own | `accreditation.document`, own table, own id |
| typed against a required document | `requirementCode` (**required**) — *"Submitted against a named requirement, not into a folder"* |
| the file | `assetId` (**required**) → `assets.media_asset` |
| per-document status vocabulary | `status: submitted, verified, rejected, expired` |
| who verified and when | `verifiedBy`, `verifiedAt` |
| refusal reason | `rejectionReason` |
| expiry | `expiresAt` — *"an insurance certificate valid until March accredits somebody until March, whatever the programme says"* |
| scoping | `holderId`, `applicationId`, `scopePath` |

with operations `submitAccreditationDocument` (:396, guest-callable, `ACCREDITATION_APPLY`) and
`verifyAccreditationDocument` (:440, `ACCREDITATION_APPROVE`) — the latter's outcome enum being
`verified, rejected, illegible, wrongDocument, expired`, which is a richer refusal vocabulary than
`MOM-4310`'s Completed/Pending. Two screens already consume it: **BO-629 *Document Repository*** and
**BO-630 *Document Verification Queue***.

The weaker analogue the register cites is real but is a stub:
`PartnerDocumentationComplianceRepositoryView` (`contracts/satellite/subscription.yaml:12034`) is
`x-ticvai-drafted-shape: true`, `x-ticvai-persistence: none`, and every one of its ~24 properties is
an untyped `string` — `tradeLicense`, `taxVatCertificate`, `commercialRegistration`, `bankDetails`,
`insurance`, `signedAgreement`, `nda`, `apiAgreement`, `complianceDocuments`,
`identificationOfAuthorizedSignatory`, `otherRequiredDocuments`, `documentType`, `documentNumber`,
`expiryDate`, `issuingAuthority`, `file`, `verificationStatus`, `verifiedBy`, `verificationDate`,
`notes`, `missing`, `uploaded`. It is a screen-shaped flat record, **not** a register — one string
column per document type, which cannot express a second insurance certificate or an expiry per
document. It is served to screen **P10 *Partner Documentation & Compliance Repository***
(`screens/P10-partner-reseller-portal.yaml:5059`).

**What is genuinely absent.** One thing, shared by both existing implementations:
**there is no requirement register.** `AccreditationDocument.requirementCode` is a bare `type: string`
— nothing anywhere defines the set of codes, which are mandatory, which are conditional on category,
or what the expiring-soon window is. So `MOM-4309`'s list (Trade Licence, Tax Registration, HACCP,
Halal, Bank Details/IBAN, Insurance) and `MOM-4308`'s Required/Received columns have nowhere to live —
**and neither do accreditation's own**. Likewise `MOM-4217`'s three-state *Valid / Expiring Soon /
Expired* is a **derivation from `expiresAt` plus a window**, not a fourth status: `AccreditationDocument.status`
deliberately holds the *lifecycle* (`submitted/verified/rejected/expired`) and the compliance state is
a presentation of `expiresAt` against today. Conflating them, as `MOM-4217` reads, would produce a
status field that changes without anyone acting.

**Whether any screen specifies it.** No supplier-side screen exists. The only supplier screen in the
package is **BO *Suppliers*** (`screens/P08-venue-back-office.yaml:18875`, module *Stock & Supply*,
route `/inventory/suppliers`, wave 2, capability C00, status `notStarted`) — a directory, with no
document region. There is no *Supplier Documents & Compliance*, no *Supplier Command Center*, no
onboarding checklist screen. The nine rows come from source pack pages `INVPROC-p04` and `INVPROC-p??`.

**Is the decision the right question.** No — it offers a false binary. It asks *"do supplier documents
become a table, or an extension of `inventory.supplier_contract`?"* Neither branch mentions the option
that the package has already built and shipped a document register with requirement-binding,
verification, refusal reasons and expiry. The decision should instead be:

1. Does `accreditation.document` generalise into a shared document register keyed by
   `(subjectType, subjectId, requirementCode)` — serving accreditation holders, suppliers **and**
   partners — or does `inventory` get a copy of it?
2. Whichever, the **requirement register is the genuinely new entity** — a per-`requirementCode` row
   with owner, mandatory/conditional rule, applicable category, expiring-soon window. Building it
   closes `MOM-4308`/`MOM-4309` *and* fixes the free-text `requirementCode` that accreditation has
   been living with.
3. `PartnerDocumentationComplianceRepositoryView` is then a projection over that register rather than
   a 24-string stub, and P10's screen stops being a dead end.

Answering the question as posed would build a third document model beside two that already disagree.

---

## D-007 — define the stock-health measure and its band thresholds

**Verdict: wrong question — the inputs exist, and the mechanism for a named measure with bands exists;
what is missing is a row of configuration and one modelling ruling.**

**What exists — the inputs.** Every input the register lists is already on a schema:

- `InventoryItem` (`contracts/satellite/inventory.yaml:2797`, `inventory.item`): **`reorderPoint`**
  (:2824), **`parLevel`** (:2830), `onHand`, `onOrder`, `inTransit`, `available`, `averageCost`,
  `lastPurchasePrice`, `isPerishable`, `shelfLifeDays`, `costingMethod`, and the derived boolean
  **`isBelowReorderPoint`** (:2875). `createInventoryItem` accepts `reorderPoint` (:647) and
  `parLevel` (:653).
- **`RequisitionSuggestion`** (:3461, `x-ticvai-persistence: none — computed`) already computes, per
  item: `onHand`, `reorderPoint`, `parLevel`, `suggestedQuantity`, **`averageDailyConsumption`** and
  **`daysOfCoverRemaining`**, plus `preferredSupplierId` and `leadTimeDays`. **Days of cover — the
  register's first candidate input — is already a computed field with a named formula behind it.**
- `StockPosition` (:2909) gives per-location `onHand / allocated / available / value / lastCountedAt`.
- `stock_batch.expires_at` and `goods_receipt_line.expiry_date` give the expiry input.
- Retail: `OutletStockLine` (`contracts/satellite/retail.yaml:1578`, `x-ticvai-persistence: none —
  projection over inventory`) requires `isBelowReorderPoint`; `getOutletStock` (:774) takes a
  `lowStockFirst` parameter (:792).
- F&B: `setItemAvailability` (`contracts/satellite/fnb.yaml:3978`) — *"Mark an item available or
  eighty-sixed"* — is the 86'd column of `MOM-3772`, already an operation.

**What exists — the mechanism for the measure itself.** This is the finding that changes the decision.
`contracts/satellite/reporting.yaml` already holds a **KPI definition register**:

- **`KpiDefinition`** (:1881, `reporting.kpi_definition`) — *"One definition, referenced everywhere —
  otherwise *revenue* means two things in the same meeting."* Fields: `code`, `name`, `description`,
  `domain`, **`formula`** (*"Expressed against the semantic model, not against tables"*), **`unit`**
  (`currency, count, percentage, duration, ratio, score`), **`higherIsBetter`** (*"Refund rate and
  revenue both go up. Without this the status colour is a coin toss."*), `defaultPeriod`, `owner`,
  `scopePath`, `isActive`.
- **`KpiTarget`** (:1939, `reporting.kpi_target`) — *"The threshold is what turns a number into a
  status."* Fields: `kpiId`, `scopePath`, `period`, `target`, **`amberAt`**, **`redAt`**, `stretch`.
- `KpiValue` (:1958) returns value, target, comparison, variancePercent, direction and freshness.
- `SemanticModel` (:2030, `reporting.semantic_model`) with `getSemanticModel` / `setSemanticModel`
  (:1602 / :1633) is where the formula's terms are defined.

So *"a named measure, with a formula, a unit, an owner, a scope, and two band boundaries"* is not a
schema that needs designing — **it is a `KpiDefinition` row plus a `KpiTarget` row.** `stockHealth`
would be `unit: percentage`, `higherIsBetter: true`, `amberAt` = the Warning boundary, `redAt` = the
Critical boundary, `formula` written against the semantic model, `scopePath` letting a venue override
the bands.

**What is genuinely absent.**

1. **The formula text.** Nobody has written what stock health *is*. That is a real decision and it is
   the only one here — but it is a sentence, not a model.
2. **A modelling problem the register has not spotted.** Eight of the nine rows are a monotonic
   three-band ladder (Healthy / Warning / Critical, or Low / Healthy / Critical) and map cleanly onto
   `target` / `amberAt` / `redAt`. **`MOM-4384` does not.** *"The Stock Health Summary donut chart
   shall classify total items as Healthy, At Risk, Critical or **Overstock**"* — overstock is bad on
   the **other side** of healthy. A single `higherIsBetter` scalar with `amberAt`/`redAt` **cannot
   express a two-sided band**, and neither can `KpiTarget` as it stands. Either overstock becomes a
   separate KPI (distance above par level), or `KpiTarget` gains an upper pair. This is the one piece
   of D-007 that touches a schema, and the register does not mention it.
3. **A roll-up rule.** The rows mix three granularities — per-item status (`MOM-3780`), per-outlet
   percentage (`MOM-3770`, `MOM-4840`, `MOM-4483`, `MOM-4720`), and a whole-estate donut of item
   counts (`MOM-4384`, `MOM-3918`). Whether the outlet percentage is count-weighted or value-weighted
   is the register's question and is unanswered anywhere.

**Whether any screen specifies it.** Partly, and thinly. The named surfaces — *F&B Stock & Operations
Command Center* (`FB-p05`), *Outlet Stock & Ingredient Availability*, *Store Stock, Transfers &
Operational Inventory* (`RETAIL-p04`), *Retail Sales & POS Command Center* — are **not in the screen
register.** The nearest existing screen is **EMP-062 *Store Stock & SKU Availability***
(`screens/P06-staff-app.yaml:10952`, module *Stock on the Floor*, wave 2, status `notStarted`,
`pattern: statusTracker`), which binds a `detailPanel` to `StockPosition` and carries its own gap note
that its declared `getHaccpStatus` reaches no component. P08 has *Stock Levels* (BO-049) and
*Stock Position & Valuation* (BO-050) as `x-ticvai-consumed-by` targets of `getStockPositions` /
`getStockValuation`. **No screen anywhere declares a stock-health field.**

**Is the decision the right question.** Not as shaped. The register classifies it *"Undefined metric"*
alongside 26 others and implies a modelling exercise; in fact the platform has a first-class metric
register with formula, unit, owner, scope and amber/red bands sitting unused, and the two hardest
inputs (`daysOfCoverRemaining`, `averageDailyConsumption`) are already computed. Re-put, the decision
is three short questions: (i) what is the formula (one sentence, written into
`KpiDefinition.formula`); (ii) count-weighted or value-weighted at outlet level; (iii) does overstock
join the same measure — and if so, `KpiTarget` needs an upper band, which is the only schema change in
the whole decision. A team told to *"define the stock-health measure, its inputs and its band
thresholds"* will build a bespoke `StockHealth` schema beside `KpiDefinition`, and the package will
then have two metric registers — which is precisely the duplication this decision exists to prevent.

The same correction applies to D-016, D-041, D-043, D-067 and D-071, which are all "undefined metric"
decisions with the same already-built home.

---

## D-008 — express the staff-to-participant ratio once

**Verdict: genuinely absent — and the register's proposed enum would collide with an existing one.**

**What exists.**

- **The roster-cover side.** `StaffingRules` (`contracts/satellite/workforce.yaml:2283`,
  `workforce.staffing_rules`) — *"A safety rule before it is a cost rule."* Its `minimumCover[]` holds
  `positionCode`, `label`, `venueId`, `attractionId`, **`minimumHeadcount` (a plain integer)**,
  `requiredQualifications[]`, `appliesWhenOpen`, and **`blocksOperation`** (*"A ride requiring two
  operators cannot run with one. Where this is true the attraction closes rather than running short."*).
  Alongside: `maximumHoursPerDay/Week`, `minimumRestHours`, `maximumConsecutiveDays`, an `overtime`
  block (`allowed`, `afterHoursPerWeek`, `rateMultiplier`, `requiresApproval`), `minimumAgeForNightShift`.
  Written by `setStaffingRules` (:686).
- **The gap read already exists and is well-shaped.** `StaffingCoverage` (:2353) returns per date /
  venue / position: `required`, `rostered`, **`qualified`** (*"A position filled by somebody not
  qualified for it is still a gap"*), `gap`, `openShiftIds[]`, and a **four-band severity enum
  `covered, tight, short, blocking`**. Served by `getStaffingCoverage` (:723). Note: this is already
  the "derived read" the register asks for — from the *roster* side.
- **The requirement side.** `ResourceRequirement` (`contracts/satellite/resources.yaml:2540`,
  `resources.resource_requirement`) — *"A type and a quantity, never a named resource."* Holds
  `resourceTypeId`, `categoryId`, `resourceId`, **`quantity` (integer, default 1)**, `mandatory`,
  `requiredQualifications[]`, `requiredAttributes`, `substituteResourceIds[]`. Its parent (a resource
  package, :2470-2539) adds `components[]`, `allocationPriority`, `effectiveFrom/To`,
  `minimumMinutes/maximumMinutes`, `requiresApproval`, `internalCost`.
- **The sale-time capacity side.** `catalogue.session_template.concurrent_capacity`,
  `catalogue.space.maximum_capacity` / `safe_capacity`, `catalogue.event_capacity_profile`
  (`mode, safe_maximum, sellable, held, accessible_provision, companion_seats, overbook_percent`),
  `catalogue.channel_capacity`.

**What is genuinely absent.** **Every expression of the ratio.** Both `ResourceRequirement.quantity`
and `StaffingRules.minimumCover[].minimumHeadcount` are **fixed integers**. Nothing anywhere holds a
denominator, a per-position rate, a rounding rule, a minimum floor, a participant band table, or a
participant-count source. Searching all 32 contracts for `ratio` (word-boundary), `perParticipant`,
`participantsPer`, `staffPer`, `attendeesPer`, `supervis*`, `instructor`, `chaperone`, `lifeguard`
returns nothing on any capacity or staffing schema. "Participant" appears in the contracts only in
`marketing-crm.yaml` (waivers) and `accreditation.yaml` (participant categories) — different sense.
So `MOM-6099`'s *"1 Ski Instructor per 8 participants, 1 Snowboard Instructor per 10, 1 Group
Assistant per 15, 1 Customer Service per 200 visitors"* has nowhere to be stored, and
`MOM-5860`'s band table (1-8 → 1, 9-16 → 2, 17-24 → 3, 25-32 → 4, 33+ → 5) has nowhere either.
Nor does `MOM-5923`'s Min/Max Participants or Participant Count Source. `MOM-5924`'s live
"Capacity Calculation" preview has no read behind it.

**A collision the register would walk into.** It proposes *"the capacity-model enum around it
(`fixedQuantity`, `ratioBased`, `tiered`, `capacityBased`, `customFormula`)"*. **`capacityBasis`
already exists** — `contracts/spine/catalogue.yaml:9189`, on `catalogue.event_type`, enum
`perPerformance, perDay, perSession, unlimited`. The two are on **different axes**: the existing one
says *over what period capacity is counted*; the proposed one says *how the number is derived*. Adding
a second field called anything like "capacity model" without naming that distinction will produce two
similarly-named enums on adjacent entities and a long argument about which one a screen means. They
should be named to separate — e.g. keep `capacityBasis` for the period, and call the new one
`capacityDerivation` — and the decision should say so.

**A second gap the register does not mention.** **BO-885 *Minimum Staffing & Coverage Rule
Configuration*** (`screens/P08-venue-back-office.yaml:103012`, module Rentals, `pattern: configEditor`,
route `/rentals/minimum-staffing-coverage-rule-configuration-bo-885`, status `notStarted`) declares
exactly one API — `setStaffingRules` — and **five fields: Minimum, Target, Recommended, Maximum,
Enforcement.** `StaffingRules.minimumCover` has **only `minimumHeadcount` and `blocksOperation`.**
So the screen already specifies a **four-level cover ladder plus an enforcement mode**, and the
contract holds one level plus a boolean. Whoever extends `minimumCover` for the ratio must also
resolve this, or the ratio will be bolted onto a shape that is about to change again.

**Whether any screen specifies it.** The rows come from source pack `RESMGMT-p06` (*TICVAI Resource
Management*) and `MOM-2147` from the Back office pack. The relevant screens that **do** exist, all
`notStarted`:
- **BO-885 *Minimum Staffing & Coverage Rule Configuration*** (:103012) — see above, calls `setStaffingRules`
- **BO-886 *Staffing Gap & Coverage Control Center*** (:103089) — consumes `getStaffingCoverage`
- **BO-884 *Attraction & Operational Staffing Roster*** (:102897)
- **BO-892 *AI Workforce Planner & Roster Optimization*** and **BO-883 *Workforce Roster Command
  Center*** (both `x-ticvai-consumed-by` on `getStaffingCoverage`)
- **BO *Resource Creation & Profile*** (:99648) — also one of D-001's 21 rows (`MOM-5667`)
- **BO *Labor Cost & Staffing Budget Control*** (:103611), **BO *AI Staffing Requirement Forecast***
  (:107543), **ADM *Workforce Demand & Staffing Forecast*** (P09 :55842)

No screen on the **sale-time** side declares a derived-capacity field, so the half of the decision that
matters commercially — *"the venue oversells a session it cannot staff"* — has no surface at all.

**Is the decision the right question.** Yes — this is the best-posed of the eight, and the only one
where nothing at all exists to be re-designed. Three amendments: (i) name the collision with
`catalogue.event_type.capacityBasis` and pick a distinct field name; (ii) note that
`StaffingCoverage` already gives the roster-side derived read with a four-band severity, so only the
**sale-side** read (`MOM-5924`'s live preview) is new; (iii) fold in BO-885's Minimum/Target/
Recommended/Maximum/Enforcement ladder, because `minimumCover` is being opened anyway and doing it
twice is the avoidable cost.

---

## Summary table

| ID | Verdict | One line |
|---|---|---|
| D-001 | **wrong question** | No tab component exists in `_components.yaml` (47 kinds, none a tab), no screen declares tabs, and 19 of the named frames are not screens — the prior question is whether a tab primitive is added at all (= D-018). |
| D-002 | **partly built** | Enum is 8 of 18 MVP marks; register's add-list wrongly includes *cohort*, omits *decomposition tree*, and treats *slicer* (already `ReportFilter.isParameter`) and *narrative text* as marks — and `ReportColumn` has no axis/size/colour role, which is the larger gap. |
| D-003 | **partly built** | `Channel` enum, `channel_allocation`, `price_list` and the published bundle all exist; no catalogue/assortment row exists, and ADM-260 already binds to an 18-string drafted stub with a free-text `venueCatalogue`. |
| D-004 | **partly built** | The whole engine exists (46 ops, matrix, modes, delegations, SLA, 12 screens); only 13 enum members and their matrix rows are missing — plus 26 orphan `requiresApproval` booleans in 12 contracts that reach no kind. |
| D-005 | **genuinely absent** | Capacity, volume, utilisation, bins and docks exist nowhere on `inventory.location` (7 fields only); but temperature class **is** solved by `fnb.TemperatureCheckpoint`, and no warehouse/zone/bin screen exists, contrary to the register. |
| D-006 | **wrong question** | `accreditation.document` is already the register D-006 asks for — requirement-bound, verified, expiring, with two screens; the real new entity is the **requirement register** that accreditation also lacks. |
| D-007 | **wrong question** | `daysOfCoverRemaining` and `averageDailyConsumption` are already computed, and `KpiDefinition` + `KpiTarget` already provide a named formula with amber/red bands — what is missing is a formula sentence, a weighting choice, and an upper band for *Overstock*. |
| D-008 | **genuinely absent** | Both `ResourceRequirement.quantity` and `minimumCover.minimumHeadcount` are fixed integers and no ratio, band table or participant source exists anywhere; the proposed enum collides with the existing `capacityBasis`, and BO-885 already specifies a four-level cover ladder the contract lacks. |
