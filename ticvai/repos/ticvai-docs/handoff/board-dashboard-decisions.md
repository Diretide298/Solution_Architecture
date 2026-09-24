# Decision register

The 564 unresolved requirement rows reduce to **222 decisions**. 119 of them close more than one row and 103 are genuinely single-row questions that nothing else in the set touches. The rows were produced by 24 agents working on separate slices, and the duplication across slices is real: the same question about `DashboardTile.visualisation`, about `ApprovalKind`, about `Outlet.openingHours` and about what "stock health" means arrived under a dozen different uids and a dozen different wordings. Grouping removes that duplication without flattening the set - the largest decision closes 21 rows, and over a hundred close exactly one.

A handful of decisions carry a disproportionate share. The top eight close 98 rows (17% of the set) and the top twenty close 173. They are: one information-architecture pass over the configEditor frames (21 rows, almost all of them Ticketing config editors that each declared their own tab list); the `DashboardTile.visualisation` enum, which holds eight marks against the 17 or 18 the board packs draw (19 rows, six modules); whether a catalogue is a first-class object that channels, price books and inventory sources bind to (12); extending `ApprovalKind` to the acts the screens gate (10); typing the stock location hierarchy - capacity, temperature class, bins and utilisation (10); the supplier compliance document register (9); and one definition of stock health with its band thresholds (9), which nine screens across F&B, retail, warehouse and planning currently each compute their own way. The recurring shapes the brief predicted all show up: 12 closed enums the sources exceed, 38 missing status or lifecycle vocabularies, 27 composite scores and percentages with no formula or bands, 30 thresholds referred to but stored nowhere, and 2 places where free text stands in for a code list. Only one decision carries a High-severity row: whether F&B recipe depletion is real-time or end-of-day, which decides whether an F&B outlet can sell while offline and contradicts ADR-0013 either way.

| ID | Title | Rows | Shape | Sev | Modules |
| --- | --- | ---: | --- | --- | --- |
| D-001 | Agree one section/tab information architecture for the configEditor frames | 21 | Other | Low | Ticketing, Inventory, Resource Management |
| D-002 | Extend DashboardTile.visualisation or state what the platform refuses to draw | 19 | Closed enum | Medium | Reporting/BI, Ticketing, Membership, Finance, B2B/OTA |
| D-003 | Decide whether a catalogue is a first-class object and how channels bind to it | 12 | Missing entity | Medium | Product & Catalog, Retail |
| D-004 | Extend ApprovalKind to the acts the screens gate, and set their matrix rules | 10 | Closed enum | Medium | Inventory, Access Control, F&B, Ticketing, Procurement, Governance |
| D-005 | Type the stock location hierarchy: capacity, temperature class, utilisation and bins | 10 | Missing entity | Medium | Warehouse Operations, Inventory |
| D-006 | Decide whether supplier compliance documents are their own register | 9 | Missing entity | Medium | Procurement |
| D-007 | Define the stock-health measure, its inputs and its band thresholds | 9 | Undefined metric | Medium | F&B, Inventory, Planning, Retail, POS & Sales |
| D-008 | Express the staff-to-participant ratio once, so sale-time capacity and roster cover agree | 8 | Missing relationship | Medium | Ticketing, Staff, Resource Management |
| D-009 | Type Outlet.openingHours and decide the closure/exception record | 8 | Missing entity | Medium | Retail, F&B |
| D-010 | Define the expiry formula builder, or refuse an expression language | 7 | Other | Medium | Ticketing |
| D-011 | Define the policy register: the named policy set, and per policy its owner, version, status and effective date | 7 | Missing entity | Medium | Ticketing, Governance |
| D-012 | Define the store/outlet template entity and the capability switches it sets | 7 | Missing entity | Medium | Retail, F&B |
| D-013 | Fix the SuggestionKind catalogue and the rule and payload behind each recommendation | 7 | Closed enum | Medium | Reporting/BI, Frontline Operations, Events, Inventory, Promotions |
| D-014 | Decide the temporary capacity override entity and its expiry | 6 | Missing entity | Medium | Inventory |
| D-015 | Define kitchen station capacity, the load formula and its bands | 6 | Undefined metric | Medium | F&B |
| D-016 | Define the procurement savings measure and its baseline | 6 | Undefined metric | Medium | Procurement, Reporting/BI |
| D-017 | Give the stock adjustment a status vocabulary and a reason-code set | 6 | Reason codes | Medium | Inventory, Warehouse Operations |
| D-018 | Add the missing canvas, grid and stepping components to the component library | 5 | Missing entity | Medium | F&B, Calendar, POS Experience & Sales Configuration, Staff |
| D-019 | Decide the cash-limit set and where each limit is configured | 5 | Missing threshold | Medium | Cash Management & Till Control, Finance |
| D-020 | Decide whether resource matching returns a numeric score, and what it scores | 5 | Undefined metric | Medium | Assignments, Calendar, Inventory, Reporting/BI |
| D-021 | Decide whether the multi-day use pattern is consecutive or flexible, and what a skipped day does | 5 | Missing vocabulary | Medium | Ticketing, Access Control |
| D-022 | Fix the closed sales-channel vocabulary and use it in every subsystem | 5 | Closed enum | Medium | F&B, Reporting/BI, Promotions, Ticketing |
| D-023 | Fix the custom-attribute registry: its data types and its per-attribute flags | 5 | Missing entity | Medium | Ticketing, CRM, Resource Management, Inventory |
| D-024 | Fix the supplier onboarding case and its stages | 5 | Missing entity | Medium | Procurement |
| D-025 | Name the non-POS roles and bind them to existing permission keys | 5 | Missing vocabulary | Medium | Reporting/BI, Events |
| D-026 | Pin the workstation Type/Mode enum and bind venueKindScope to it | 5 | Closed enum | Medium | Workstation Management, POS, POS Configuration, Retail |
| D-027 | Set the kitchen SLA targets, the escalation ladder and the firing vocabulary | 5 | Missing threshold | Medium | F&B |
| D-028 | Decide whether inventory documents carry an explicit priority | 5 | Missing vocabulary | Low | Inventory, F&B, Planning |
| D-029 | Decide how a device, workstation or rental station is placed on a map | 4 | Missing relationship | Medium | Workstation Management, Workstation & Device Management, Device Management, Rental Management |
| D-030 | Decide the inventory reopen rules after a cancellation | 4 | Missing vocabulary | Medium | Inventory |
| D-031 | Decide the membership lifecycle: proration, dunning suspension, cancellation timing and grace access | 4 | Missing vocabulary | Medium | Ticketing |
| D-032 | Decide the till variance tolerance, its reason codes and the float status vocabulary | 4 | Reason codes | Medium | Cash Management, POS |
| D-033 | Decide what a shift template holds and where the attendance thresholds live | 4 | Missing threshold | Medium | Shift & Operator Management, POS, Shift Management |
| D-034 | Decide what defaults a category carries and how items inherit them | 4 | Missing entity | Medium | Inventory, Product & Catalog |
| D-035 | Decide whether a Promotion Group is a record, and whether it is versioned | 4 | Missing entity | Medium | Promotions |
| D-036 | Decide whether a session/timeslot template is versioned and how widely it applies | 4 | Missing entity | Medium | Ticketing |
| D-037 | Decide whether a variant dimension may hold capacity as well as price | 4 | Missing relationship | Medium | Ticketing |
| D-038 | Decide whether an RFQ evaluation is its own record, and fix its criteria and weights | 4 | Missing entity | Medium | Procurement |
| D-039 | Decide whether connectivity has a third 'weak' band and what it permits | 4 | Missing threshold | Medium | Offline Operations, Workstation Management, Offline POS & Synchronization |
| D-040 | Decide whether units of measure become a first-class register | 4 | Missing entity | Medium | Inventory |
| D-041 | Define the count and reconciliation accuracy percentage - one formula | 4 | Undefined metric | Medium | Inventory |
| D-042 | Define the order routing rule record and its precedence | 4 | Missing entity | Medium | F&B |
| D-043 | Define the resource health score and the utilisation bands | 4 | Undefined metric | Medium | Reporting/BI, Calendar |
| D-044 | Define the retail fulfilment state machine and its SLA | 4 | Missing vocabulary | Medium | POS & Sales |
| D-045 | Fix the channel capacity and allocation model vocabularies | 4 | Closed enum | Medium | Inventory, Promotions |
| D-046 | Fix the planning exception record, its classes, priority and AED impact | 4 | Missing entity | Medium | Planning |
| D-047 | Make the calendar Conflict a first-class record with a severity scale | 4 | Missing entity | Medium | Calendar, Assignments |
| D-048 | Register the P08 boards and the navigation rail | 4 | Other | Medium | Planning, Calendar |
| D-049 | Decide whether DashboardTile carries per-mark display settings | 4 | Other | Low | Reporting/BI |
| D-050 | Decide how a temporary or event selling location is modelled | 3 | Missing entity | Medium | Retail, POS & Sales, Inventory |
| D-051 | Decide how machine and system actors are attributed in audit trails | 3 | Missing vocabulary | Medium | Inventory, Governance |
| D-052 | Decide the SKU identifier model: barcode symbology, RFID and EPC | 3 | Missing entity | Medium | Product & Catalog |
| D-053 | Decide the allocation scoring policy: its factor codes, weights and hard constraints | 3 | Undefined metric | Medium | Assignments |
| D-054 | Decide the check-in/check-out session rules | 3 | Missing vocabulary | Medium | Access Control |
| D-055 | Decide the dashboard builder canvas and its binding model | 3 | Other | Medium | Reporting/BI |
| D-056 | Decide the deferred best-available seat model | 3 | Missing relationship | Medium | Seat Management |
| D-057 | Decide the reorder rule: method, review period, lead time and EOQ | 3 | Missing entity | Medium | Inventory |
| D-058 | Decide the shared audit-record shape and what it retains | 3 | Missing entity | Medium | Audit, Inventory, Governance |
| D-059 | Decide the supplier discovery and classification attributes | 3 | Missing vocabulary | Medium | Procurement |
| D-060 | Decide what a sale-board tile can be and how it is hidden | 3 | Closed enum | Medium | POS Experience & Sales Configuration, POS Configuration |
| D-061 | Decide what an entitlement/validity template records about itself | 3 | Missing vocabulary | Medium | Ticketing |
| D-062 | Decide where the margin threshold lives and the cost basis for margin | 3 | Missing threshold | Medium | Product & Catalog |
| D-063 | Decide whether first-use activation is its own event on the entitlement | 3 | Missing entity | Medium | Ticketing, Access Control |
| D-064 | Define lead time and booking cutoff: what each measures and where it is set | 3 | Missing threshold | Medium | Ticketing, Sales Channels |
| D-065 | Define offline exposure and what 'a venue is offline' means | 3 | Undefined metric | Medium | Frontline Operations, POS |
| D-066 | Define the POS/frontline exception record and its type taxonomy | 3 | Missing vocabulary | Medium | Frontline Operations |
| D-067 | Define the forecast measures and where a forecast is persisted | 3 | Undefined metric | Medium | Planning |
| D-068 | Define the impact field on ai.Suggestion and its band vocabulary | 3 | Undefined metric | Medium | Reporting/BI, Promotions |
| D-069 | Define the scenario simulator: its library, parameters and comparison shape | 3 | Missing entity | Medium | Reporting/BI |
| D-070 | Fix the product content field set and its length limits | 3 | Missing entity | Medium | Ticketing, CMS |
| D-071 | Fix the supplier performance scorecard formula and its bands | 3 | Undefined metric | Medium | Procurement |
| D-072 | Fix the validity-window time semantics: inclusivity, DST and overnight | 3 | Other | Medium | Ticketing |
| D-073 | Settle one severity scale across alerts, incidents and exception centres | 3 | Closed enum | Low | Frontline Operations, POS & Sales |
| D-074 | Settle whether recipe depletion is real-time or end-of-day | 2 | Other | High | F&B |
| D-075 | Decide the ID-proof and guest attribute requirements a ticket may demand | 2 | Missing vocabulary | Medium | Ticketing |
| D-076 | Decide the capacity forecast's input signals and safety bounds | 2 | Missing threshold | Medium | Inventory |
| D-077 | Decide the checkout donation prompt's placement and default state | 2 | Other | Medium | Ticketing |
| D-078 | Decide the count types and the cycle-count schedule | 2 | Missing vocabulary | Medium | Inventory |
| D-079 | Decide the donation campaign association model | 2 | Missing relationship | Medium | Ticketing |
| D-080 | Decide the kitchen and service alert trigger set and each threshold | 2 | Missing threshold | Medium | F&B |
| D-081 | Decide the reach of the profile-linking model | 2 | Missing relationship | Medium | CRM |
| D-082 | Decide the rental advance-booking window fields | 2 | Missing threshold | Medium | Rental Management |
| D-083 | Decide the reschedule and date-change policy | 2 | Missing threshold | Medium | Ticketing |
| D-084 | Decide the supplier contract status and its expiring-soon window | 2 | Missing threshold | Medium | Procurement |
| D-085 | Decide the table definition: capacity bands and the type taxonomy | 2 | Missing entity | Medium | F&B |
| D-086 | Decide the table-assignment rule for QR orders and waitlist parties | 2 | Missing relationship | Medium | F&B |
| D-087 | Decide the version-currency and update classification for workstations | 2 | Missing vocabulary | Medium | Workstation Management |
| D-088 | Decide the virtual queue target wait time and the lane reallocation trigger | 2 | Missing threshold | Medium | Virtual Queue |
| D-089 | Decide the warehouse alert-type set and the metric behind each | 2 | Closed enum | Medium | Warehouse Operations, Retail |
| D-090 | Decide when a stock transfer is overdue | 2 | Missing threshold | Medium | Inventory, Retail |
| D-091 | Decide where tax treatment is configured | 2 | Missing vocabulary | Medium | Pricing, Retail |
| D-092 | Decide whether a product variant combination can be excluded | 2 | Closed enum | Medium | Ticketing |
| D-093 | Decide whether a safe or vault is a modelled container | 2 | Missing entity | Medium | Cash Management, Cash Management & Till Control |
| D-094 | Decide whether an approval can be sent back for changes | 2 | Missing vocabulary | Medium | Mobile Operations, Finance |
| D-095 | Decide whether stock transfer and goods receipt carry a lifecycle | 2 | Missing vocabulary | Medium | Inventory |
| D-096 | Decide whether supplier categories are a first-class mapping | 2 | Missing relationship | Medium | Procurement |
| D-097 | Decide whether the commerce journey is its own entity | 2 | Missing entity | Medium | Omnichannel |
| D-098 | Define the F&B margin bridge stages | 2 | Undefined metric | Medium | Reporting/BI |
| D-099 | Define the four commercial performance measures | 2 | Undefined metric | Medium | Reporting/BI |
| D-100 | Define the purchase-limit model and its scopes | 2 | Missing relationship | Medium | Ticketing, POS Configuration |
| D-101 | Define the service level and safety stock measures | 2 | Undefined metric | Medium | Planning |
| D-102 | Define the store refund-value baseline and its alert deviation | 2 | Undefined metric | Medium | POS & Sales |
| D-103 | Define the supplier concentration measure and its bands | 2 | Undefined metric | Medium | Reporting/BI |
| D-104 | Fix the RFQ lifecycle and whether an RFQ is a first-class resource | 2 | Missing vocabulary | Medium | Procurement |
| D-105 | Fix the capacity hierarchy levels and their precedence | 2 | Missing relationship | Medium | Inventory |
| D-106 | Fix the procurement spend dimensions: spend category and business unit | 2 | Missing vocabulary | Medium | Procurement, Reporting/BI |
| D-107 | Fix the resource and labour cost breakdown taxonomies | 2 | Missing vocabulary | Medium | Reporting/BI, Staff |
| D-108 | Fix the supplier status vocabulary and its blocking effects | 2 | Missing vocabulary | Medium | Procurement |
| D-109 | Settle one evaluation order across price lists, promotions and store rules | 2 | Missing relationship | Medium | POS Configuration |
| D-110 | Decide the camp and recurring-day session treatment | 2 | Missing vocabulary | Low | Ticketing |
| D-111 | Decide the clone model for products and validity rules | 2 | Other | Low | Ticketing |
| D-112 | Decide the delivery retry policy and whether the next attempt is stored | 2 | Other | Low | Ticketing |
| D-113 | Decide the group entry rules: entry window and minimum presence | 2 | Missing threshold | Low | Access Control |
| D-114 | Decide the point-of-sale receipt and guest-identification defaults | 2 | Missing vocabulary | Low | Retail |
| D-115 | Decide the waitlist eligibility and cap | 2 | Missing threshold | Low | Ticketing |
| D-116 | Decide where the guest-facing rule message is authored and localised | 2 | Missing entity | Low | Inventory, Ticketing |
| D-117 | Decide whether OfflinePolicy carries a lifecycle | 2 | Missing vocabulary | Low | Offline Operations, Offline POS & Synchronization |
| D-118 | Decide whether dataTable gains a totals and averages footer | 2 | Other | Low | POS & Sales, Inventory |
| D-119 | Decide which storefront presentation options are tenant-configurable | 2 | Other | Low | Guest App |
| D-120 | Confirm the access control and facial recognition vendor | 1 | Other | Medium | Infrastructure |
| D-121 | Decide how a case escalation reaches a department | 1 | Missing relationship | Medium | Customer Service |
| D-122 | Decide how a guest photo becomes a saleable product | 1 | Missing relationship | Medium | Retail |
| D-123 | Decide how a replenishment source is selected | 1 | Missing relationship | Medium | F&B |
| D-124 | Decide how customer confirmation of a profile merge is obtained | 1 | Missing entity | Medium | CRM |
| D-125 | Decide how performance breadth is modelled on an entitlement | 1 | Missing vocabulary | Medium | Ticketing |
| D-126 | Decide how the Employee App home is derived from role | 1 | Other | Medium | Access Control |
| D-127 | Decide the Missing Data Behavior vocabulary | 1 | Missing vocabulary | Medium | Ticketing |
| D-128 | Decide the corporate quota allocation dimensions | 1 | Missing relationship | Medium | Ticketing |
| D-129 | Decide the entitlement conversion rule set | 1 | Missing vocabulary | Medium | Ticketing |
| D-130 | Decide the event resource shortfall bands | 1 | Missing threshold | Medium | Events |
| D-131 | Decide the four reservation requirement modes | 1 | Missing vocabulary | Medium | Ticketing |
| D-132 | Decide the guest-visible attribute allow-list for a person resource | 1 | Missing vocabulary | Medium | Assignments |
| D-133 | Decide the high-value variance threshold | 1 | Missing threshold | Medium | Inventory |
| D-134 | Decide the invoice-over-GRN tolerance | 1 | Missing threshold | Medium | Procurement |
| D-135 | Decide the late-entry grace window and whether it can charge | 1 | Missing relationship | Medium | Access Control |
| D-136 | Decide the manual usage declaration path for isolated tenants | 1 | Missing entity | Medium | Licensing & Subscription |
| D-137 | Decide the membership renewal overlap rule | 1 | Missing threshold | Medium | Ticketing |
| D-138 | Decide the modifier-group behaviour flags | 1 | Other | Medium | F&B |
| D-139 | Decide the on-device data retention period | 1 | Missing threshold | Medium | Offline Operations |
| D-140 | Decide the online return approval and collection workflow | 1 | Missing entity | Medium | Retail |
| D-141 | Decide the per-ticket transfer cap | 1 | Missing threshold | Medium | Ticketing |
| D-142 | Decide the performance association modes | 1 | Missing vocabulary | Medium | Ticketing |
| D-143 | Decide the precedence between day-of-week, time windows and blackouts | 1 | Missing relationship | Medium | Ticketing |
| D-144 | Decide the service-mode availability vocabulary | 1 | Missing vocabulary | Medium | Ticketing |
| D-145 | Decide the table-visit event vocabulary and its retention | 1 | Missing entity | Medium | F&B |
| D-146 | Decide the under-sold slot merge recommendation | 1 | Missing threshold | Medium | Ticketing |
| D-147 | Decide what a bulk-imported accreditation row becomes | 1 | Other | Medium | Accreditation |
| D-148 | Decide what a failed payment does to a seat hold | 1 | Other | Medium | Seat Management |
| D-149 | Decide what a refund does to a partly-used entitlement | 1 | Other | Medium | Ticketing |
| D-150 | Decide what the operational and review reporting pillar contains | 1 | Missing vocabulary | Medium | Finance |
| D-151 | Decide where a sale note, gift receipt and personalisation sit | 1 | Missing entity | Medium | POS & Sales |
| D-152 | Decide where an early-bird phase's quota lives | 1 | Missing relationship | Medium | Pricing |
| D-153 | Decide whether P08 has a global search | 1 | Missing entity | Medium | Calendar |
| D-154 | Decide whether a buzzer is a managed device | 1 | Missing entity | Medium | F&B |
| D-155 | Decide whether a donation line carries its own status | 1 | Missing vocabulary | Medium | Reporting/BI |
| D-156 | Decide whether a granted ticket exception is a standing record | 1 | Missing entity | Medium | Ticketing |
| D-157 | Decide whether a holiday calendar is a shared entity | 1 | Missing entity | Medium | Ticketing |
| D-158 | Decide whether a redeemable entitlement permits substitution | 1 | Missing relationship | Medium | Ticketing |
| D-159 | Decide whether a replenishment plan is a first-class object | 1 | Missing entity | Medium | Planning |
| D-160 | Decide whether a service purchase order is its own kind | 1 | Missing entity | Medium | Procurement |
| D-161 | Decide whether a store has an emergency stock source | 1 | Missing relationship | Medium | Retail |
| D-162 | Decide whether a suite can be sold both in bulk and by seat | 1 | Missing relationship | Medium | Seat Management |
| D-163 | Decide whether a virtual-card tender joins TenderKind | 1 | Closed enum | Medium | Payments |
| D-164 | Decide whether an add-on carries a sub-option axis | 1 | Missing relationship | Medium | Ticketing |
| D-165 | Decide whether an event resource plan can be locked | 1 | Missing vocabulary | Medium | Events |
| D-166 | Decide whether each Venue Size Index factor can be optional | 1 | Undefined metric | Medium | Licensing & Subscription |
| D-167 | Decide whether gaming gets its own reporting data source | 1 | Closed enum | Medium | Gaming |
| D-168 | Decide whether gateway-level Dynamic Currency Conversion is in scope | 1 | Other | Medium | Finance |
| D-169 | Decide whether tenant_config is scope-path keyed at brand level | 1 | Missing relationship | Medium | CMS |
| D-170 | Decide whether the allocation policy gets a dry-run | 1 | Missing entity | Medium | Assignments |
| D-171 | Decide whether the booking flow supports a party-size-first variant | 1 | Missing relationship | Medium | Ticketing |
| D-172 | Decide whether the group leader counts in the headcount | 1 | Other | Medium | Ticketing |
| D-173 | Decide whether the product dependency view is a graph | 1 | Missing relationship | Medium | Ticketing |
| D-174 | Decide whether the roles comparison is a screen or a diff operation | 1 | Other | Medium | Platform/Tenancy |
| D-175 | Decide whether there is one platform task scheduler | 1 | Missing entity | Medium | Platform/Tenancy |
| D-176 | Decide which subsystems a rollback is checked against | 1 | Other | Medium | Inventory |
| D-177 | Decide which transactions auto-reserve stock | 1 | Other | Medium | Inventory |
| D-178 | Define a customer impact event | 1 | Undefined metric | Medium | Reporting/BI |
| D-179 | Define stock availability as a percentage | 1 | Undefined metric | Medium | Reporting/BI |
| D-180 | Define the click-and-collect queue metric and its alert point | 1 | Undefined metric | Medium | POS & Sales |
| D-181 | Define the item cost-increase measure and its threshold | 1 | Undefined metric | Medium | Procurement |
| D-182 | Define the offline B2B ticket batch and its CSV | 1 | Missing entity | Medium | B2B |
| D-183 | Define the outlet performance score | 1 | Undefined metric | Medium | Reporting/BI |
| D-184 | Define the resource efficiency measures | 1 | Undefined metric | Medium | Reporting/BI |
| D-185 | Fix the Finance Dashboard tile set and each tile's KPI definition | 1 | Undefined metric | Medium | Finance |
| D-186 | Fix the age calculation basis for age-gated products | 1 | Other | Medium | Ticketing |
| D-187 | Set the accessibility conformance target for dashboard visuals | 1 | Other | Medium | Reporting/BI |
| D-188 | Set the ticket validation latency target and where it is measured | 1 | Missing threshold | Medium | Access Control |
| D-189 | Settle the stock reservation type vocabulary and its filters | 1 | Missing vocabulary | Medium | Inventory |
| D-190 | Decide how a fully free game is represented | 1 | Other | Low | Gaming |
| D-191 | Decide the QR table-ordering order limits | 1 | Missing threshold | Low | F&B |
| D-192 | Decide the automatic device-incident severity classification | 1 | Missing threshold | Low | Device Management |
| D-193 | Decide the batch expiry bands | 1 | Missing threshold | Low | Inventory |
| D-194 | Decide the food-safety attribute set and its values | 1 | Missing vocabulary | Low | Inventory |
| D-195 | Decide the owner-role set on a digital asset | 1 | Missing entity | Low | Digital Asset Management |
| D-196 | Decide the referral award cap | 1 | Missing threshold | Low | Ticketing |
| D-197 | Decide the scarcity band behind 'Few Left' | 1 | Missing threshold | Low | Bookings |
| D-198 | Decide the supplier address model | 1 | Missing entity | Low | Procurement |
| D-199 | Decide what a catalogue import job records about itself | 1 | Missing entity | Low | Ticketing |
| D-200 | Decide what a selling rule and a special product are | 1 | Missing entity | Low | F&B |
| D-201 | Decide what the access-control screen shows at the gate | 1 | Other | Low | Access Control |
| D-202 | Decide where operational event notes live | 1 | Missing entity | Low | Events |
| D-203 | Decide whether BLE operator presence is required at the gate | 1 | Missing threshold | Low | Access Control |
| D-204 | Decide whether a calendar filter set can be saved as a view | 1 | Missing entity | Low | Calendar |
| D-205 | Decide whether a campaign records a stated objective | 1 | Missing vocabulary | Low | Promotions |
| D-206 | Decide whether a denomination carries an image asset | 1 | Other | Low | POS |
| D-207 | Decide whether a multi-attraction entitlement has a minimum interval between uses | 1 | Missing threshold | Low | Ticketing |
| D-208 | Decide whether a product category is effective-dated | 1 | Other | Low | Ticketing |
| D-209 | Decide whether a remote cache clear exists | 1 | Other | Low | Offline POS & Synchronization |
| D-210 | Decide whether a resource version is materialised | 1 | Missing entity | Low | Resource Management |
| D-211 | Decide whether add-on eligibility is a stored flag | 1 | Other | Low | Ticketing |
| D-212 | Decide whether document extraction returns a per-attribute confidence | 1 | Missing entity | Low | Ticketing |
| D-213 | Decide whether performance capacity supports bulk edit | 1 | Other | Low | Ticketing |
| D-214 | Decide whether realised rental revenue appears on the availability view | 1 | Undefined metric | Low | Rental Management |
| D-215 | Decide whether recipe ingredients carry a yield percentage | 1 | Undefined metric | Low | F&B |
| D-216 | Decide whether revenue allocation supports fixed-amount splits | 1 | Missing entity | Low | Finance |
| D-217 | Decide whether the 3D section view is in scope | 1 | Other | Low | Seat Management |
| D-218 | Decide whether the catalogue emits a productUpdated event | 1 | Missing relationship | Low | Ticketing |
| D-219 | Decide whether the date picker gains a horizontal near-term variant | 1 | Other | Low | Ticketing |
| D-220 | Decide whether the sync queue exposes an in-flight state | 1 | Missing vocabulary | Low | POS & Sales |
| D-221 | Decide whether the terminal reports its local storage use | 1 | Missing entity | Low | Offline Operations |
| D-222 | Define outlet production risk | 1 | Undefined metric | Low | F&B |

Total: 222 decisions closing 564 rows. Every one of the 564 uids appears in exactly one decision.

