/**
 * The burst-environment model.
 *
 * Every structural fact here is transcribed from the delivery package and the
 * line it came from is named beside it. Three things are NOT the package's and
 * say so at the point of use: the per-cluster service times, the lease hold
 * time, and the container start time. The package states that these services
 * "autoscale on RPS" and never states at what, and nothing in it measures a
 * latency — so the model needs numbers the package does not have. They are
 * defaults on controls rather than constants in a diagram.
 *
 * SOURCES
 *   handoff/burst-scope.json          services, weightedShare, 34 operations, callsPerBuyer
 *   deploy/c-flash-sale.yml           replicas, cpu/memory limits, pgbouncer, postgres-hot
 *   states/burst-environment.yaml     9 states, 12 transitions, triggers, guards
 *   docs/adr/0035-burst-environments  5,000 RPS, the four cost points, the 409, the policies
 *   docs/adr/0032 (via burst-map.js)  shed order — guest and public first, staff and service last
 */

/* ── the package's facts ─────────────────────────────────────────────────── */

// handoff/burst-scope.json and tools/derive-sizing.py → the deployed three.
// **The floor is derive-sizing's, which is the expected peak.** "Floor is the
// expected peak. A burst environment warms before traffic arrives and the first
// seconds of a sale are the peak — thirty thousand people do not arrive
// gradually." burst-scope's own min (4 / 4 / 3) and expectedAtTarget (8 / 5 / 3)
// are kept beside it because the two files disagree and the disagreement is
// worth showing.
export const SERVICES = [
  ['CatalogueService', 'commerce', true, 63.6, true, 14, 4, 8, '63.6% of 5000 RPS at 400 RPS per replica and 60% target', 400, 240, 260, 'carries the burst — replicates on RPS'],
  ['OrderService', 'commerce', true, 21.8, true, 8, 4, 5, '21.8% of 5000 RPS at 250 RPS per replica and 60% target', 250, 150, 162, 'carries the burst — replicates on RPS'],
  ['TenancyService', 'foundation', true, 3.6, false, 0, 0, 0, null, 0, 0, 0, 'on the path but not the load — served from the shared cell'],
  ['RetailService', 'operations', true, 3.6, false, 0, 0, 0, null, 0, 0, 0, 'on the path but not the load — served from the shared cell'],
  ['MarketingService', 'engagement', true, 3.6, false, 0, 0, 0, null, 0, 0, 0, 'on the path but not the load — served from the shared cell'],
  ['IdentityService', 'foundation', true, 1.8, true, 2, 3, 3, '1.8% of 5000 RPS at 600 RPS per replica and 60% target — implies 1, floored at 2', 600, 360, 390, 'required for every purchase, small but not optional'],
  ['AccessService', 'commerce', true, 1.8, false, 0, 0, 0, null, 0, 0, 0, 'on the path but not the load — served from the shared cell'],
  ['LedgerService', 'commerce', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['InventoryService', 'operations', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['FnbService', 'operations', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['AiService', 'engagement', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['VenueOpsService', 'operations', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['PlatformService', 'platform', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['WhiteLabelService', 'platform', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['ReportingService', 'platform', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
  ['CrossRegionService', 'platform', false, 0, false, 0, 0, 0, null, 0, 0, 0, 'no part of a ticket sale — not deployed'],
].map(([name, tier, onPath, share, deployed, min, scopeMin, scopeExpected, derivedFrom, replicaRps, scaleOutAt, stepAddsAt, reason]) =>
  ({ name, tier, onPath, share, deployed, min, scopeMin, scopeExpected, derivedFrom,
    replicaRps, scaleOutAt, stepAddsAt, reason }));

/**
 * **The two paths, which are separate systems running concurrently.**
 * handoff/burst-scope.json → routing. The burst environment carries the on-sale
 * and nothing else; everything a venue does that day continues in the shared
 * cell. They meet once, afterwards, at reconciliation — so the routine 48.5 RPS
 * is NOT part of what the environment is sized for.
 */
export const ROUTING = {
  note: 'Normal traffic and sale traffic are separate systems running concurrently. The burst environment carries the on-sale and nothing else; everything a venue does that day continues in the shared cell. They meet once, afterwards, at reconciliation.',
  normal: {
    name: 'normal', target: 'shared cell',
    services: 16, operations: 998, tables: 373,
    exampleLoad: 'stadium, routine Saturday: 60,000 guests × 14 requests = 48.5 RPS',
    rps: 48.5,
    description: 'Everything except the sale. Admission, food, retail, stock, staff back-office, reporting. Runs whether or not a sale is happening.',
  },
  sale: {
    name: 'sale', target: 'burst environment',
    services: 3, operations: 34, tables: 42,
    exampleLoad: 'same stadium on-sale: 1.25M requests in 2h = 1,045 RPS at a 6× burst; compressed to 20 minutes, 6,270',
    description: 'The on-sale only. Provisioned before it opens, torn down after, and its orders reconcile back into the shared cell (ADR-0035) — which is the single point the two paths touch.',
  },
  meetingPoint: {
    operation: 'reconcileBurstEnvironment',
    mechanism: 'environment id, monotonic sequence, idempotent replay, sync.rejection',
    note: 'The same three properties as syncOrders one layer up. A till’s offline journal and a burst environment’s order log are the same problem at different scale.',
  },
};

// handoff/burst-scope.json → operations[]. [operationId, verb, service, callsPerBuyer, lock]
export const OPS = [
  ['getAvailability', 'GET', 'CatalogueService', 6, null],
  ['getCart', 'GET', 'OrderService', 4, null],
  ['getProduct', 'GET', 'CatalogueService', 4, null],
  ['acquireInventoryHold', 'POST', 'CatalogueService', 3, 'FOR UPDATE SKIP LOCKED'],
  ['listProducts', 'GET', 'CatalogueService', 3, null],
  ['addCartLine', 'POST', 'OrderService', 2, null],
  ['createSeatHold', 'POST', 'CatalogueService', 2, 'FOR UPDATE'],
  ['evaluatePromotions', 'POST', 'CatalogueService', 2, null],
  ['getSeatMap', 'GET', 'CatalogueService', 2, null],
  ['listPerformances', 'GET', 'CatalogueService', 2, null],
  ['listSeats', 'GET', 'CatalogueService', 2, null],
  ['analysePromotionConflicts', 'GET', 'CatalogueService', 1, null],
  ['appendEntitlementToMedia', 'POST', 'OrderService', 1, null],
  ['applyManualDiscount', 'POST', 'OrderService', 1, null],
  ['createApprovalRequest', 'POST', 'TenancyService', 1, null],
  ['createOrder', 'POST', 'OrderService', 1, null],
  ['createPayment', 'POST', 'OrderService', 1, null],
  ['createRefund', 'POST', 'OrderService', 1, null],
  ['evaluateApprovalRequirement', 'POST', 'TenancyService', 1, null],
  ['extendSeatHold', 'POST', 'CatalogueService', 1, null],
  ['getEvent', 'GET', 'CatalogueService', 1, null],
  ['getLoyaltyPosition', 'GET', 'MarketingService', 1, null],
  ['getMediaEntitlements', 'GET', 'OrderService', 1, null],
  ['getPerformance', 'GET', 'CatalogueService', 1, null],
  ['getReturnPolicy', 'GET', 'RetailService', 1, null],
  ['getSeatAvailability', 'GET', 'CatalogueService', 1, null],
  ['getSeatHold', 'GET', 'CatalogueService', 1, null],
  ['identifyGuest', 'POST', 'MarketingService', 1, null],
  ['listEvents', 'GET', 'CatalogueService', 1, null],
  ['listMyEntitlements', 'GET', 'AccessService', 1, null],
  ['lookupRetailSale', 'GET', 'RetailService', 1, null],
  ['refreshToken', 'POST', 'IdentityService', 1, null],
  ['renewInventoryHold', 'POST', 'CatalogueService', 1, null],
  ['searchCatalogue', 'GET', 'CatalogueService', 1, null],
].map(([id, verb, service, cpb, lock]) => ({ id, verb, service, cpb, lock }));

export const CALLS_PER_BUYER = OPS.reduce((a, o) => a + o.cpb, 0); // 55

/** Read and write rates, split by verb — what each database is actually asked for. */
export const READ_CPB = OPS.filter((o) => o.verb === 'GET').reduce((a, o) => a + o.cpb, 0);
export const WRITE_CPB = OPS.filter((o) => o.verb !== 'GET').reduce((a, o) => a + o.cpb, 0);

/**
 * **What reaches the burst environment, which is not all of it.** Of a buyer's
 * 55 calls, 48 land on the three deployed services; the other seven — Tenancy
 * 2, Retail 2, Marketing 2, Access 1 — are on the burst path and answered from
 * the shared cell rather than replicated here. Offered and served are both
 * counted on this basis, because a rate offered to this environment and a rate
 * served by it have to share a denominator or served comes out above offered.
 */
export const SHARED_CELL_CPB = ['TenancyService', 'RetailService', 'MarketingService', 'AccessService']
  .reduce((a, name) => a + OPS.filter((o) => o.service === name).reduce((b, o) => b + o.cpb, 0), 0);
export const DEPLOYED_CPB = CALLS_PER_BUYER - SHARED_CELL_CPB;

/**
 * **What one buying guest costs, and the package says two different things.**
 * burst-scope.json's own callsPerBuyer sums to 55 across the 34 operations;
 * TICVAI_Deployment_Technical Part 2 says "a buying guest costs about 22
 * requests", derived from flows F58, F59 and F61. Neither is measured. Both are
 * offered rather than reconciled, because the choice moves every number below
 * by a factor of 2.5 and somebody should make it deliberately.
 */
export const BASES = [
  { key: 'flows', calls: 22, label: '22 a buyer',
    note: 'TICVAI_Deployment_Technical Part 2 — “a buying guest costs about 22 requests”, walked from flows F58, F59 and F61. The figure the deployment arithmetic uses.' },
  { key: 'package', calls: CALLS_PER_BUYER, label: `${CALLS_PER_BUYER} a buyer`,
    note: 'summed from callsPerBuyer across the 34 operations in handoff/burst-scope.json. Higher, because it counts a buyer checking availability six times.' },
];
export const callsPerBuyer = (cfg) =>
  (BASES.find((b) => b.key === (cfg?.basis ?? 'flows')) ?? BASES[0]).calls;

/**
 * **The three venue tiers, from TICVAI_Deployment_Technical Part 2.** The
 * client's own numbers: 18,500 is Saturday's concert, 2,000 is the water park
 * Qossai named. The peak column is what the document derives, and the model
 * below reproduces both of its stated figures exactly — 1,045 RPS over two
 * hours and 6,270 compressed into twenty minutes.
 */
export const VENUES = [
  { key: 'small', label: 'Museum, water park', guests: 2000, buyPct: 30, reqDay: 41200, steadyRps: 1.0, docPeak: 2, window: 'steady across 12 hours' },
  { key: 'medium', label: 'Theme park, concert day', guests: 18500, buyPct: 55, reqDay: 482850, steadyRps: 11.2, docPeak: 124, window: 'peaks 3 hours before the gates' },
  { key: 'large', label: 'Stadium sell-out', guests: 60000, buyPct: 95, reqDay: 2094000, steadyRps: 48.5, docPeak: 1045, window: 'a two-hour sale window' },
];

// "1,045 RPS at a six-times burst" — Part 2. Arrival inside the window is not
// flat, and six is the document's own allowance for that.
export const BURST_FACTOR = 6;

/**
 * **What sharding the lease costs, which is not throughput.**
 *
 * **And ADR-0037 removed the reason to pay it.** A lease holding one statement
 * carries about 2,000 holds a second on a single row, and the hottest row in the
 * hardest scenario this model runs — `catalogue.channel_capacity` at 253 buyers
 * a second — asks for 405. **The wall is at 20% before a single shard is added.**
 * Sharding still multiplies it, and multiplying a ceiling nothing is reaching
 * buys headroom at the price of the fragmentation below. The ADR's own words:
 * variant C "stays in `deploy/variants/` as a measurement, not a candidate".
 * This function is what makes the cost visible when somebody runs it anyway.
 *
 * C-lease-shards.yml states it: "sixteen sub-pools sum to the performance
 * capacity and each can be exhausted separately, so the last seats fragment:
 * fifteen shards empty and one holding four is a performance that looks sold
 * out to most buyers. Rebalancing is the hard part and this variant does not
 * implement it."
 *
 * So a sharded lease trades a throughput wall for a correctness one, and the
 * correctness one only appears at the end of the sale. A buyer takes a shard;
 * if that shard is empty they are told there is nothing left while seats sit in
 * another. **This curve is mine** — the package states the failure and gives no
 * distribution for it. Mean remaining per shard against a spread: plenty left
 * and nobody sees it, nearly gone and almost everybody does.
 */
export function fragmentedShare(cfg, remaining, seats) {
  const shards = variantParams(cfg).leaseShards;
  if (shards <= 1 || seats <= 0) return 0;
  const perShard = seats / shards;
  const mean = remaining / shards;
  // A quarter of a shard's original depth as the spread: at that much left on
  // average, about a third of shards are already empty.
  const spread = Math.max(1, perShard * ((cfg?.fragSpreadPct ?? 25) / 100));
  return Math.max(0, Math.min(0.95, Math.exp(-mean / spread)));
}
/** Seats on sale — the venue's buying guests. Orders cannot exceed them. */
export const seatsFor = (cfg) => Math.round(
  (VENUES.find((v) => v.key === cfg.venue) ?? VENUES[2]).guests
  * ((VENUES.find((v) => v.key === cfg.venue) ?? VENUES[2]).buyPct / 100),
);

/** The document's arithmetic, run forwards: guests → buyers → mean → peak. */
export function derivePeak(cfg) {
  const venue = VENUES.find((v) => v.key === cfg.venue) ?? VENUES[2];
  const buyers = Math.round(venue.guests * (venue.buyPct / 100));
  const calls = callsPerBuyer(cfg);
  const requests = buyers * calls;
  const mean = requests / cfg.windowSec;
  return { venue, buyers, calls, requests, mean, peak: Math.round(mean * BURST_FACTOR) };
}

// deploy/c-flash-sale.yml → services.*.deploy.resources.limits and environment
export const COMPOSE = {
  file: 'deploy/c-flash-sale.yml',
  postgres: { cpus: 16, memGb: 32, maxConnections: 800, syncCommit: 'off' },
  redis: { cpus: 4, memGb: 16 },
  pgbouncer: { maxClient: 5000, poolSize: 80, mode: 'transaction' },
  clusters: {
    CatalogueService: { replicas: 4, cpus: 4, memGb: 2, poolMin: 8, poolMax: 40 },
    OrderService: { replicas: 4, cpus: 4, memGb: 2, poolMin: 8, poolMax: 40 },
    IdentityService: { replicas: 3, cpus: 2, memGb: 1, poolMin: 8, poolMax: 40 },
  },
  // The compose file is told one number because compose has no autoscaler, and
  // the number it is told is the minimum. Its own comment gives the arithmetic
  // at 5,000 RPS for reference: Catalogue 8, Order 5, Identity 3, and 640
  // client connections against pgbouncer's 5,000.
  composeNote: 'compose is told 4 / 4 / 3 because it has no autoscaler; the arithmetic implies 8 / 5 / 2',
};

// states/burst-environment.yaml
export const STATES = ['requested', 'provisioning', 'warming', 'live', 'draining',
  'reconciling', 'reconciled', 'decommissioned'];
export const MACHINE = {
  initial: 'requested',
  terminal: ['decommissioned', 'failed'],
  transitions: [
    { from: 'requested', to: 'provisioning', trigger: 'operation', operation: 'requestBurstEnvironment', guard: 'Requested against the sale calendar, not against arriving demand. Provisioning takes minutes and a sale takes seconds — requesting when the load appears is requesting too late.' },
    { from: 'provisioning', to: 'warming', trigger: 'system', guard: 'Infrastructure is up. Warming is the catalogue snapshot and the cache fill — an environment that goes live cold serves its first thousand guests from an empty cache.' },
    { from: 'warming', to: 'live', trigger: 'system', guard: 'Snapshot taken, caches warm, health checks passing. snapshotTakenAt is stamped here and it is the moment the price divergence question starts running.' },
    { from: 'live', to: 'draining', trigger: 'operation', operation: 'drainBurstEnvironment', guard: 'Draining is not stopping. A guest mid-checkout is allowed to finish; a guest arriving after is told the sale has ended.' },
    { from: 'live', to: 'draining', trigger: 'time', guard: 'onSaleTo plus graceMinutes. A queue does not empty at the instant the last ticket sells.' },
    { from: 'draining', to: 'reconciling', trigger: 'operation', operation: 'reconcileBurstEnvironment', guard: 'In-flight orders have completed or timed out.' },
    { from: 'reconciling', to: 'reconciling', trigger: 'operation', operation: 'reconcileBurstEnvironment', guard: 'Resumable, and this self-transition is why. A reconciliation interrupted at order 18,000 of 30,000 continues from 18,000.' },
    { from: 'reconciling', to: 'reconciled', trigger: 'system', guard: 'Every order applied or rejected. Rejections are kept in sync.rejection and worked afterwards.' },
    { from: 'reconciled', to: 'decommissioned', trigger: 'operation', operation: 'decommissionBurstEnvironment', guard: 'Explicit teardown.' },
    { from: 'reconciled', to: 'decommissioned', trigger: 'time', guard: 'autoDecommission is set. The only automatic path to teardown, and it sits after reconciliation rather than after the sale.' },
    { from: 'provisioning', to: 'failed', trigger: 'system', guard: 'Provisioning failed. No orders exist yet, so nothing is lost.' },
    { from: 'warming', to: 'failed', trigger: 'system', guard: 'Warming failed. No orders exist yet.' },
  ],
};

export const OP_LABEL = {
  requestBurstEnvironment: 'Stand it up',
  drainBurstEnvironment: 'Close the sale',
  reconcileBurstEnvironment: 'Merge back',
  decommissionBurstEnvironment: 'Tear it down',
};

// docs/adr/0035 — quoted, four durations
export const COST_POINTS = [
  { label: 'two-hour sale', hours: 2, usd: 24 },
  { label: 'six hours', hours: 6, usd: 71 },
  { label: 'a day', hours: 24, usd: 282 },
  { label: 'a month, forgotten', hours: 720, usd: 8587 },
];
// TICVAI_Hosting_Summary: option 3 is billed by the hour — $11.76 on Amazon,
// $9.76 on Google. ADR-0035's own month figure implies $11.93, a 1.4%
// difference; the document's stated hourly price is the one used here.
export const HOURLY = [
  { key: 'aws', name: 'Amazon', usd: 11.76 },
  { key: 'gcp', name: 'Google', usd: 9.76 },
];
export const RATE_PER_HOUR = 11.76;

/**
 * **The rows a sale converges on, and they are not two.**
 *
 * burst-scope.json flags two tables `contended: true`, but a purchase touches
 * more rows that all buyers reach at once. Two kinds, and they do not behave
 * alike:
 *
 * - **convergent** — every buyer hits the SAME row, so writes serialise and the
 *   ceiling is one over the hold time however much hardware is added.
 * - **insert-hot** — every buyer inserts its OWN row, so there is no row lock
 *   to queue on; the contention is on the index tail and the page, which is
 *   real but roughly an order of magnitude cheaper.
 *
 * Collapsing the second kind into the first would overstate the wall; leaving
 * it out entirely pretends a sale only touches two rows.
 */
export const CONTENDED = [
  { table: 'catalogue.inventory_hold', op: 'acquireInventoryHold', lock: 'FOR UPDATE SKIP LOCKED',
    cpb: 3, kind: 'convergent', flagged: true,
    note: 'A short-lived claim on contended stock while somebody decides. CF-115 settled that contended inventory is leased rather than reserved. One row a performance, and the wall.' },
  { table: 'seating.seat_hold', op: 'createSeatHold', lock: 'FOR UPDATE',
    cpb: 2, kind: 'convergent', flagged: true,
    note: 'A temporary claim on a seat. Expires, which is what stops two channels selling it. Flagged contended by the package — though its own note describes a per-seat claim, which would be many rows rather than one.' },
  { table: 'catalogue.channel_capacity', op: 'acquireInventoryHold', lock: 'decrement',
    cpb: 4, kind: 'convergent', flagged: false,
    note: 'How much of a performance each sales channel may sell. It is the envelope being decremented, one row per performance and channel, so every buyer on the web channel reaches the same row. Not flagged contended in burst-scope, and it is.' },
  { table: 'promotions.promotion', op: 'evaluatePromotions', lock: 'decrement',
    cpb: 3, kind: 'convergent', flagged: false,
    note: 'A rule that changes a price, with a budget. A promotion with a budget is decremented per redemption, so a single on-sale code is one row every buyer touches.' },
  { table: 'orders.sales_order', op: 'createOrder', lock: 'insert',
    cpb: 6, kind: 'insert', flagged: false,
    note: 'One row a sale, so no two buyers contend for the same row — but they all append to the same index tail and the same heap pages. Cheaper than a lock and not free.' },
  { table: 'platform.outbox', op: 'createPayment', lock: 'insert',
    cpb: 2, kind: 'insert', flagged: false,
    note: 'Written in the same transaction as the state change, by the platform, which is what makes it exactly-once — and puts every payment on one append path.' },
  { table: 'ledger.journal_entry', op: 'createPayment', lock: 'insert',
    cpb: 2, kind: 'insert', flagged: false,
    note: 'A balanced set of postings, append-only: a correction is another entry rather than an edit. Two inserts a payment, on the path that also takes the money.' },
];

// mine — an insert competes for an index tail rather than a row, so it costs a
// fraction of a lease. Stated as a multiple so it can be argued with.
export const INSERT_COST = 0.15;


// docs/adr/0032, as quoted in the viewer: guest and public first, staff and service last.
export const CHANNELS = [
  { key: 'guest', label: 'guest', mix: 0.70 },
  { key: 'public', label: 'public', mix: 0.15 },
  { key: 'staff', label: 'staff', mix: 0.10 },
  { key: 'service', label: 'service', mix: 0.05 },
];

/* ── the numbers that are mine ───────────────────────────────────────────── */

/* ── the configurations ───────────────────────────────────────────────

   **Everything is identical except the one thing named.** deploy/variants/README.md
   says so outright, and says why: 9 of a buyer's 55 calls touch a contended row,
   that is the wall, and it moves with none of replicas, Redis size or pooler
   settings. Four of these are in the package.

   **Two are not, and the README explains that they were deliberately not built.**
   They are here because a simulator can show that rather than assert it — R and
   P are the two instincts the README talks somebody out of, run to the point
   where they visibly fail to help. Both are marked as not the package's. */

export const VARIANTS = [
  {
    key: 'A',
    name: 'A · baseline',
    file: 'deploy/c-flash-sale.yml',
    changes: 'nothing',
    attacks: '—',
    inPackage: true,
    note: 'The environment as written. Three services, 17 tables, 45 containers, one database, and gone afterwards. The lease holds one statement — read the row, decide, write the row — so a convergent row carries about 2,000 holds a second rather than 167. That is ADR-0037 and the contracts implement it: all four locking operations declare x-ticvai-lock-excludes. Run E to see what the same environment did before they did.',
    params: {},
  },
  {
    key: 'B',
    name: 'B · read cache',
    file: 'deploy/variants/B-read-cache.yml',
    changes: '23 of 35 read calls served from Redis',
    attacks: 'database load',
    inPackage: true,
    note: 'getProduct 4, listProducts 3, getSeatMap 2, listPerformances 2, listSeats 2 and the rest — a catalogue snapshot cannot change during a sale, so TTL is zero meaning no expiry. It does not touch getAvailability or the hold path: caching availability is how two people buy the same seat. Expect the lease number to be unchanged — that is the point of running it beside C.',
    params: { cachedReadCpb: 23 },
  },
  {
    key: 'C',
    name: 'C · lease shards',
    file: 'deploy/variants/C-lease-shards.yml',
    changes: '16 sub-pools per performance',
    // **A measurement, not a candidate**, and that is ADR-0037's wording. It
    // widens the wall by sixteen where shrinking the lease widens it by twelve,
    // and it is the only one of the two that carries fragmentation.
    attacks: 'a wall that no longer needs widening',
    inPackage: true,
    superseded: 'ADR-0037',
    note: 'This was the only variant that attacked the wall, and ADR-0037 took the wall down without it: a lease holding one statement carries 2,000 holds a second on one row, and the hottest row at the hardest load here asks for 405. Sharding multiplies a ceiling already sitting at 20%. It stays as a measurement rather than a candidate — the ADR’s own words — and what it still shows is the cost: a buyer who does not care which seat takes any shard with capacity, but sixteen sub-pools each empty separately, so fifteen empty and one holding four is a performance that looks sold out to most buyers. Rebalancing is the hard part and the variant does not implement it. Run it beside A: nobody was being refused, and now some are told there is nothing left while seats remain.',
    params: { leaseShards: 16 },
  },
  {
    key: 'D',
    name: 'D · write batching',
    file: 'deploy/variants/D-write-batching.yml',
    changes: 'a 50ms coalescing window',
    attacks: 'lock acquisitions',
    inPackage: true,
    note: 'addCartLine is 2 calls a buyer and renewInventoryHold is 1, both against contended rows: three round trips each taking and releasing the same lock. A 50ms window batches them into one statement. The cost is up to 50ms on the first write in a window — invisible on a read path and not on a checkout. If lock acquisitions fall and holds a second do not rise, the batching is saving work nobody was waiting on.',
    params: { batchWindowMs: 50, batchedWriteCpb: 3 },
  },
  {
    key: 'R',
    name: 'R · Redis as the pooler',
    file: 'not in the package',
    changes: 'the read path leaves Postgres entirely',
    attacks: 'nothing that is failing',
    inPackage: false,
    note: 'Scale Redis up and let the services read through it rather than through pgbouncer. The README declines to build this and says why: Redis is not the constraint, nothing treats a cache entry as truth, and a bigger Redis makes misses cheaper when the misses are not what is failing. Run it and watch — the database read bar empties, and the lease ceiling does not move by one hold a second. B is the useful version of the same instinct: the lever is what is cached, not the tier size.',
    params: { redisPooler: true, cachedReadCpb: READ_CPB },
  },
  {
    // **This was the baseline's opposite and it is now the baseline's history.**
    // It used to read "E · shrink the lease · not in the package — a code change,
    // not an architecture change", offering ADR-0037's decision as something a
    // reader might try. The ADR was accepted on 31 August, two days before this
    // model was written, and the contracts carry it. Inverting it keeps the wall
    // reachable — which is the part worth seeing — without filing an accepted
    // decision under speculation.
    key: 'E',
    name: 'E · the lock, as it measured',
    file: 'docs/adr/0037-what-may-be-inside-a-lock.md — the arrangement it forbids',
    changes: 'the idempotency check and both reads go back inside the lock',
    attacks: 'nothing — it is the wall ADR-0037 took down',
    inPackage: false,
    regression: true,
    note: 'A Postgres row lock costs microseconds and acquireInventoryHold measured six milliseconds — a factor of five hundred, and the difference was a Redis round trip for the idempotency key plus a read of platform.workstation that the capacity decision never uses. Put them back and the per-row ceiling falls from 2,000/s to 167/s, which at 5,000 RPS turns a sale that clears into one that refuses buyers on the lease path while every replica sits near half utilisation. Run it to see why the ADR names an acceptance criterion: bench.py reports holdContentionMs, and anything above one millisecond means something forbidden is inside the lock again.',
    params: { lockMs: 6 },
  },
  {
    key: 'F',
    name: 'F · guarded decrement, no lock',
    file: 'not in the package — one statement',
    changes: 'UPDATE … SET remaining = remaining - $1 WHERE remaining >= $1',
    attacks: 'the lock itself',
    inPackage: false,
    note: 'A counter decrement does not need FOR UPDATE. One statement holds a row lock for the duration of the statement, Postgres serialises it correctly, and there is no read-then-write window at all. Zero rows updated means sold out — which is the answer you wanted. No explicit lock, no fragmentation, no reconciliation obligation: the ceiling becomes the statement rate rather than the lease.',
    params: { noLock: true },
  },
  {
    key: 'X',
    name: 'X · the unsafe path',
    file: 'not in the package — the latent bugs, detonated',
    changes: 'read-then-update instead of a guarded update',
    attacks: 'nothing — it is what failure looks like',
    inPackage: false,
    unsafe: true,
    note: 'Contention does not corrupt; it refuses. But it detonates the latent bugs, and every path here is safe at five buyers a second and unsafe at two hundred and eighty-three. This is the same environment with a read-then-update guard instead of a guarded one, and it oversells: the race window is microseconds, so at low load it never fires, and at 283/s convergent on one row it fires constantly. Run it beside A to see the difference between refusing buyers and overselling seats.',
    params: { unsafeGuard: true },
  },
  {
    key: 'N',
    name: 'N · no pre-warm',
    file: 'not in the package — the mistake ADR-0035 warns about',
    changes: 'the environment scales in reaction to load instead of ahead of it',
    attacks: 'nothing — it declines the anticipation',
    inPackage: false,
    unsafe: true,
    note: 'Stand the environment up at its resting count and let the autoscaler react. This is the configuration ADR-0035 exists to argue against: provisioning takes minutes and a sale takes seconds, so scaling into a fifty-second peak is scaling into a peak that is already over. The floors and the calculator are still there; nothing uses them until the load has already arrived.',
    params: { noPrewarm: true },
  },
  {
    key: 'M',
    name: 'M · compose as written',
    file: 'deploy/c-flash-sale.yml — taken literally',
    changes: 'no sizing algorithm at all: 4 / 4 / 3, fixed',
    attacks: 'nothing — it declines the calculator',
    inPackage: false,
    unsafe: true,
    note: 'Compose has no autoscaler, so it can only be told one number — and this is what happens if that number is taken as the deployment rather than as a floor. Eleven containers, fixed, whatever arrives. The file says so itself: “in a real deployment there is no maximum”, and its own reference line at 5,000 RPS is 8 / 5 / 3. Run this to see what that sentence is protecting against.',
    params: { fixedReplicas: true },
  },
];

/** The lease hold in force — a variant may lengthen it or remove the lock. */
export const lockMsFor = (cfg) => {
  const p = (VARIANTS.find((v) => v.key === (cfg?.variant ?? 'A')) ?? VARIANTS[0]).params;
  return p.lockMs ?? cfg?.lockMs ?? 0.5;
};

/** The one thing this configuration changes, resolved into numbers. */
export function variantParams(cfg) {
  const v = VARIANTS.find((x) => x.key === (cfg?.variant ?? 'A')) ?? VARIANTS[0];
  const p = v.params;
  return {
    variant: v,
    cachedReadCpb: Math.min(READ_CPB, p.cachedReadCpb ?? 0),
    leaseShards: p.leaseShards ?? 1,
    batchWindowMs: p.batchWindowMs ?? 0,
    batchedWriteCpb: p.batchedWriteCpb ?? 0,
    redisPooler: Boolean(p.redisPooler),
    noLock: Boolean(p.noLock),
    noPrewarm: Boolean(p.noPrewarm),
    fixedReplicas: Boolean(p.fixedReplicas),
    unsafeGuard: Boolean(p.unsafeGuard),
    lockMs: p.lockMs ?? null,
    poolSize: COMPOSE.pgbouncer.poolSize * (p.poolMultiplier ?? 1),
    maxClient: COMPOSE.pgbouncer.maxClient * (p.poolMultiplier ?? 1),
  };
}

// No maximum in the package: "in a real deployment there is no maximum." The
// reader may impose one, and this is what "none" means to the model.
export const NO_CEILING = 400;

/**
 * **tools/derive-sizing.py — the algorithm, stated.**
 *
 *   replicas = max(floor, ceil(load_rps × share / rps_per_replica))
 *
 * **Two loads, two mixes, and they are not the same shape.** Under a sale
 * Catalogue is 64% of the calls and F&B is absent; under normal operation
 * Catalogue is 11%, F&B is 13%, and Order is the largest at 15% because a venue
 * day is mostly transactions rather than browsing. A shared cell sized from the
 * burst mix would run eight Catalogue replicas and one F&B — backwards for 363
 * days of the year.
 *
 * `rpsPerReplica` comes from ADR-0032's autoscale triggers and is a HYPOTHESIS
 * until tools/bench.py runs. Everything else is arithmetic on top of it.
 */
export const SIZING = {
  // The algorithm as the generator now applies it: target utilisation is inside
  // it, which is what moves Catalogue from 8 to 14 at the same 5,000 RPS.
  algorithm: 'replicas = max(floor, ceil(load_rps × share / (rps_per_replica × target_utilisation)))',
  targetUtilisation: 0.6,
  unmeasured: 'rpsPerReplica comes from ADR-0032’s autoscale triggers and is a hypothesis until tools/bench.py runs. Everything else here is arithmetic on top of it.',
  finding: 'A shared cell sized from the burst mix would run eight Catalogue replicas and one F&B — backwards for 363 days of the year.',
  // **Two generated files disagree about the sale floors.** derive-sizing.py
  // says 14 / 8 / 2 with target utilisation inside the algorithm;
  // burst-scope.json says min 4 / 4 / 3 and expectedAtTarget 8 / 5 / 3 without
  // it; and compose is told 4 / 4 / 3. The sizing file is the one that states
  // its algorithm, so the model follows it — and says so rather than quietly
  // picking.
  conflict: 'derive-sizing.py puts the sale floors at 14 / 8 / 2 with target utilisation inside the algorithm. burst-scope.json still says min 4 / 4 / 3 and expectedAtTarget 8 / 5 / 3 without it, and compose is told 4 / 4 / 3. Two generated files, three answers for the same three numbers — the sizing file is the one that states its algorithm, so it is the one followed here.',
  // service → [normal share %, rps a replica, scaleOutAt, stepAddsAt]
  normalMix: [
    ['OrderService', 14.9, 250, 150, 162], ['FnbService', 12.7, 300, 180, 195],
    ['CatalogueService', 11.3, 400, 240, 260], ['VenueOpsService', 7.5, 300, 180, 195],
    ['InventoryService', 7.2, 300, 180, 195], ['MarketingService', 7.1, 400, 240, 260],
    ['PlatformService', 7.1, 400, 240, 260], ['TenancyService', 6.5, 500, 300, 325],
    ['LedgerService', 4.8, 300, 180, 195], ['IdentityService', 4.5, 600, 360, 390],
    ['AccessService', 4.3, 800, 480, 520], ['WhiteLabelService', 3.6, 500, 300, 325],
    ['ReportingService', 2.9, 200, 120, 130], ['RetailService', 2.9, 300, 180, 195],
    ['AiService', 2.4, 100, 60, 65], ['CrossRegionService', 0.4, 300, 180, 195],
  ].map(([name, share, rpsPerReplica, scaleOutAt, stepAddsAt]) =>
    ({ name, share, rpsPerReplica, scaleOutAt, stepAddsAt })),
  saleMix: [
    ['CatalogueService', 63.6, 400, 240, 260, 14], ['OrderService', 21.8, 250, 150, 162, 8],
    ['IdentityService', 1.8, 600, 360, 390, 2],
  ].map(([name, share, rpsPerReplica, scaleOutAt, stepAddsAt, floor]) =>
    ({ name, share, rpsPerReplica, scaleOutAt, stepAddsAt, floor })),
  saleLoadRps: 5000,
  saleFloor: 2,
  // The normal tiers carry their own peak, which is a venue's busy afternoon
  // rather than an on-sale — a different number from the 1,045 the sale derives.
  tiers: {
    small: { guests: 2000, example: 'museum, water park', dailyRequests: 41200, meanRps: 1.0, peakRps: 5.7 },
    medium: { guests: 18500, example: 'theme park, concert night', dailyRequests: 482850, meanRps: 11.2, peakRps: 67.1 },
    large: { guests: 60000, example: 'stadium, arena', dailyRequests: 2094000, meanRps: 48.5, peakRps: 290.8 },
  },
  cells: [
    { key: 'small cell', venues: { small: 20, medium: 4, large: 0 }, meanRps: 64.8, peakRps: 382.4, atFloor: 32, atPeak: 32 },
    { key: 'medium cell', venues: { small: 60, medium: 20, large: 2 }, meanRps: 381.0, peakRps: 2265.6, atFloor: 32, atPeak: 33 },
    { key: 'large cell', venues: { small: 120, medium: 60, large: 8 }, meanRps: 1180.0, peakRps: 7036.4, atFloor: 32, atPeak: 47 },
  ],
  normalFloor: 2,
  normalNote: 'Floor is survivability, not peak. The autoscaler has all day to react to a busy afternoon, so paying for the peak all night buys nothing.',
  saleNote: 'Floor is the expected peak. A burst environment warms before traffic arrives and the first seconds of a sale are the peak — thirty thousand people do not arrive gradually.',
};

/**
 * The stated algorithm, applied — with target utilisation inside it, which is
 * where the generator now puts it. At 5,000 RPS this reproduces the file's own
 * sale figures exactly: Catalogue 14, Order 8, Identity 2.
 */
export const sizeFor = (loadRps, share, rpsPerReplica, floor, targetUtil) =>
  Math.max(floor, Math.ceil((loadRps * (share / 100)) / (rpsPerReplica * (targetUtil ?? SIZING.targetUtilisation))));

/**
 * **The shared cell, sized and running.** It is not idle before the sale and it
 * does not stop during one: everything a venue does that day continues here
 * whether or not an on-sale is happening. Sized by the same algorithm as the
 * burst environment, from a completely different mix.
 */
export function normalSizing(cfg) {
  const cell = SIZING.cells.find((c) => c.key === (cfg?.cell ?? 'medium cell')) ?? SIZING.cells[1];
  const rps = (cfg?.normalLoad ?? 'mean') === 'peak' ? cell.peakRps : cell.meanRps;
  const util = SIZING.targetUtilisation;
  const services = SIZING.normalMix.map((x) => {
    const rpsAtLoad = rps * (x.share / 100);
    const n = sizeFor(rps, x.share, x.rpsPerReplica, SIZING.normalFloor, util);
    return {
      ...x,
      rpsAtLoad,
      impliedByLoad: Math.ceil(rpsAtLoad / (x.rpsPerReplica * util)),
      n,
      // Which of the two terms in the algorithm actually decided the count.
      drivenBy: Math.ceil(rpsAtLoad / (x.rpsPerReplica * util)) > SIZING.normalFloor
        ? 'load' : 'survivability floor',
      utilisationAtSteady: rpsAtLoad / (n * x.rpsPerReplica),
    };
  });
  return {
    cell, rps,
    load: (cfg?.normalLoad ?? 'mean') === 'peak' ? 'a busy afternoon' : 'the mean',
    services,
    replicas: services.reduce((a, x) => a + x.n, 0),
    atFloor: cell.atFloor,
    atPeak: cell.atPeak,
  };
}

/**
 * **TICVAI_Hosting_Summary — what each option costs, and how it is billed.**
 * Three of the four run all the time and are billed monthly. One runs for hours.
 * The burst environment is the only one billed by the hour, which is why its
 * cost and the platform's upkeep cannot be added without saying which is which.
 */
export const HOSTING = {
  source: 'TICVAI_Hosting_Summary · 24 August 2026',
  shared: { name: 'Shared — one cell per country', aws: 3485, gcp: 2874, billing: 'per month, always on' },
  private: { name: 'Private — a customer’s own setup', aws: 948, gcp: 779, billing: 'per month, always on' },
  venueLocal: { name: 'Shared + venue equipment', aws: 3965, gcp: 3237, billing: 'per month, always on' },
  burstHourly: { aws: 11.76, gcp: 9.76, billing: 'per hour, while it runs' },
  // The one thing we pay for behind the AI Concierge; the model itself is on
  // the customer's own provider account, capped.
  searchIndexMonthly: 1150,
  // A venue's share of the shared cell, per month.
  venueShare: { small: 310, medium: 780, large: 1900 },
  fleet: {
    customers: 200, venuesEach: 3,
    sharedMonthly: 96910, privateMonthly: 189600, venueLocalMonthly: 177283,
  },
  note: 'Google comes out 15–18% cheaper, mostly on database pricing — and that is not a reason to pick it. CF-64 is open on AWS against Azure, pending the Dubai Electronic Security Center.',
};

export const PROVIDERS = [
  { key: 'aws', name: 'Amazon' },
  { key: 'gcp', name: 'Google' },
];

export const DEFAULTS = {
  variant: 'A',
  provider: 'aws',
  // the sizing calculator's inputs
  sizingLoadRps: 5000,   // the load the floors are calculated for — ADR-0035's figure
  sizingFloor: 2,        // survivability: below this there is no redundancy at all
  rpsCatalogue: 400,     // ADR-0032's per-replica triggers, and a hypothesis
  rpsOrder: 250,
  rpsIdentity: 600,
  // **A visible steady period before anything is asked for.** Every scenario
  // opens with the shared cell alone — two across the board — so the timeline
  // shows what the platform looks like before the environment exists.
  steadySec: 180,
  normalLoad: 'mean',    // the shared cell at its mean, or at a busy afternoon
  salesPerMonth: 4,      // how many on-sales a month the upkeep carries
  cell: 'medium cell',   // which shared cell the normal path runs in
  // mine — the share of buyers who will take any seat, which is the share a
  // sharded lease can parallelise. A buyer choosing a specific seat still
  // serialises whatever the shard count.
  anySeatPct: 80,
  mode: 'scenario',       // 'scenario' — a scripted run · 'free' — the reader drives it
  freeBuyers: 0,          // free mode: buyers a second, held by the reader
  basis: 'flows',         // which of the two per-buyer figures to believe
  venue: 'large',         // stadium sell-out
  windowSec: 7200,        // the sale window the demand is compressed into
  // **The ceilings are the reader's, not the file's.** deploy/c-flash-sale.yml
  // declares 20 / 16 / 6 and nothing in the package derives them, so they are
  // no longer a wall the model obeys: it scales as far as it needs and these
  // are where the reader decides to stop it. The floors stay the package's —
  // burst-scope.json's own resting counts, 4 / 4 / 3.
  capCatalogue: NO_CEILING,
  capOrder: NO_CEILING,
  capIdentity: NO_CEILING,
  // Above the ceiling the overflow waits rather than being refused outright.
  // A buyer who has waited this long is gone.
  maxWaitSec: 30,
  fragSpreadPct: 25,   // mine — how unevenly sharded stock depletes
  holdTtlSec: 45,      // mine — the package states no checkout TTL at all
  dbStatementMs: 2,      // mine — mean statement time on postgres-hot
  peakRps: 5000,          // ADR-0035
  thresholdPct: 60,       // the reader's, defaulted at 60
  scaleStepPct: 5,        // add 5% of the ceiling per scaling decision
  // **ADR-0037, and the contracts implement it.** All four operations declaring
  // `x-ticvai-lock` carry `x-ticvai-lock-excludes` naming what may not be inside
  // the lock — `cache:idempotency` and `platform.workstation` — so the six
  // milliseconds this used to hold is the figure from before those exclusions
  // existed. The ADR's acceptance criterion is `holdContentionMs` under one, and
  // 0.5 is the figure it does the arithmetic at. This was `6` and marked "mine".
  lockMs: 0.5,            // ADR-0037 · docs/adr/0037-what-may-be-inside-a-lock.md
  // **Scale out, or scale up.** Horizontal keeps the replica the size compose
  // declares and adds more; vertical keeps the count at the redundancy floor
  // and buys a bigger machine. The package only ever modelled the first.
  scaling: 'horizontal',  // | 'vertical'
  startSec: 20,           // mine — container cold start to ready
  sloMs: 800,             // mine — p99 a buyer would tolerate
  divergencePct: 0,
  policy: 'honourSnapshot',
  rampSec: 20,
  saleSec: 50,
  graceSec: 120,
  leadSec: 600,           // requested this long before on-sale
  autoDecommission: true,
  forgottenHours: 0,
};

// **Derived from the package, not authored here.** burst-scope.json now states
// the per-replica rate each floor was calculated at — 400, 250 and 600 RPS a
// replica — so the mean service time follows from it rather than from a guess:
// a 4-cpu replica carrying 400 rps is 10ms a request. This used to be mine.
export const SERVICE_MS = Object.fromEntries(SERVICES
  .filter((s) => s.deployed)
  .map((s) => [s.name, (1000 * COMPOSE.clusters[s.name].cpus) / s.replicaRps]));

export const SCALE_TICK = 10;     // a scaling decision every ten seconds
export const SCALE_DOWN_SEC = 60; // and down no faster than one replica a minute

/* ── clusters ────────────────────────────────────────────────────────────── */

export const cpbFor = (service) => OPS.filter((o) => o.service === service)
  .reduce((a, o) => a + o.cpb, 0);

export const CLUSTERS = SERVICES.filter((s) => s.deployed).map((s) => {
  const c = COMPOSE.clusters[s.name];
  return {
    name: s.name,
    short: s.name.replace('Service', ''),
    min: s.min,               // derive-sizing's floor, which IS the expected peak
    scopeMin: s.scopeMin,     // burst-scope's resting min, which disagrees
    scopeExpected: s.scopeExpected,
    derivedFrom: s.derivedFrom,
    replicaRps: s.replicaRps,
    scaleOutAt: s.scaleOutAt,   // rps a replica at which the autoscaler adds
    stepAddsAt: s.stepAddsAt,
    connectionsAtExpected: s.min * c.poolMax,
    composeReplicas: c.replicas,    // what compose is told, because it cannot scale
    cpus: c.cpus,
    memGb: c.memGb,
    poolMax: c.poolMax,
    cpb: cpbFor(s.name),
    share: s.share,
    serviceMs: SERVICE_MS[s.name],
    reason: s.reason,
    capKey: `cap${s.name.replace('Service', '')}`,
    rpsKey: `rps${s.name.replace('Service', '')}`,
  };
});

/* ── the sizing calculator ──────────────────────────────────────────────

   **The floors are calculated, not transcribed.** Every input to the algorithm
   is a control, so the sale floors follow from what the reader believes rather
   than from a number copied out of a generated file — and at the package's own
   inputs they come out at the package's own answer: 14 / 8 / 2. */

/** The per-replica rate in force — the reader's, or ADR-0032's trigger. */
export const replicaRpsFor = (cfg, cluster) =>
  Math.max(20, Math.round(cfg?.[cluster.rpsKey] ?? cluster.replicaRps));

/** Mean service time follows from the per-replica rate; it is not independent. */
export const serviceMsFor = (cfg, cluster) =>
  (1000 * cluster.cpus) / replicaRpsFor(cfg, cluster);

/** **The sale floor, calculated.** The algorithm run on the reader's inputs. */
export function saleFloorFor(cfg, cluster) {
  const load = cfg?.sizingLoadRps ?? SIZING.saleLoadRps;
  const util = (cfg?.thresholdPct ?? 60) / 100;
  const survivability = cfg?.sizingFloor ?? SIZING.saleFloor;
  const rpsAtLoad = load * (cluster.share / 100);
  const implied = Math.ceil(rpsAtLoad / (replicaRpsFor(cfg, cluster) * util));
  return {
    load, util, survivability, rpsAtLoad, implied,
    n: Math.max(survivability, implied),
    drivenBy: implied > survivability ? 'load' : 'survivability floor',
    scaleOutAt: Math.round(replicaRpsFor(cfg, cluster) * util),
  };
}

/* ── horizontal or vertical ───────────────────────────────────────────────

   **The same capacity, bought two ways.** Horizontal keeps the replica the size
   compose declares and adds more of them; vertical keeps the count at the
   redundancy floor and makes each one bigger. The package only ever modelled
   the first, and "should this scale out or up" is a question somebody asks
   before signing an instance type, so it is worth being able to run.

   **Both reach the same wall and neither reaches it because of cpu.** The lease
   ceiling is one over the lease hold on a single row, and a row does not care
   how many machines are contending for it or how large they are. That is the
   finding, and running the two side by side is the clearest way to see it. */

/** The largest general-purpose instance a cloud will sell, in vCPU. */
export const MAX_VCPU = 96;

/**
 * **Vertical: the count is the redundancy floor and the machine absorbs the
 * rest.** Two replicas, because one is not redundancy — everything above that
 * goes into the instance size rather than into the count.
 *
 * `k` is what each replica has to be multiplied by. It is not rounded to a
 * whole number of anything except cpus, because that is what you buy.
 */
export function verticalFor(cfg, cluster) {
  const load = cfg?.sizingLoadRps ?? SIZING.saleLoadRps;
  const util = (cfg?.thresholdPct ?? 60) / 100;
  const n = Math.max(2, cfg?.sizingFloor ?? SIZING.saleFloor);
  const base = replicaRpsFor(cfg, cluster);
  const rpsAtLoad = load * (cluster.share / 100);
  // What one of the n replicas has to carry, against the same target.
  const wanted = Math.max(1, (rpsAtLoad / n) / (base * util));
  // **cpus are integral and the instance ceiling is real.** A cloud will not
  // sell half a core, and above MAX_VCPU there is no larger machine to move to
  // — which is the difference that matters: horizontal has no such stop.
  const cpus = Math.min(MAX_VCPU, Math.max(cluster.cpus, Math.ceil(wanted * cluster.cpus)));
  const k = cpus / cluster.cpus;
  return {
    n,
    k,
    cpus,
    memGb: cluster.memGb * k,
    replicaRps: base * k,
    // **The pool scales with the machine, so the pooler sees the same demand.**
    // Connections track concurrency, and concurrency tracks throughput — fewer,
    // larger replicas each holding proportionally more is the same total. A
    // vertical move does not relieve pgbouncer, and assuming it does is how an
    // instance gets sized against a limit that did not move.
    poolMax: cluster.poolMax * k,
    // Where it stops. Above this there is no bigger instance to buy and the
    // only remaining move is the one this mode was chosen to avoid.
    atInstanceCeiling: cpus >= MAX_VCPU,
    headroom: MAX_VCPU / cpus,
  };
}

export const isVertical = (cfg) => (cfg?.scaling ?? 'horizontal') === 'vertical';

/** The three clusters as the current config makes them. */
export const clustersFor = (cfg) => CLUSTERS.map((c) => {
  if (!isVertical(cfg)) {
    return {
      ...c,
      min: saleFloorFor(cfg, c).n,
      replicaRps: replicaRpsFor(cfg, c),
      serviceMs: serviceMsFor(cfg, c),
    };
  }
  const v = verticalFor(cfg, c);
  return {
    ...c,
    min: v.n,
    cpus: v.cpus,
    memGb: v.memGb,
    poolMax: v.poolMax,
    replicaRps: v.replicaRps,
    // **Unchanged, and that is the point.** A bigger machine does not serve one
    // request faster; it serves more of them at once. serviceMs is per request.
    serviceMs: serviceMsFor(cfg, c),
    vertical: v,
  };
});

/** The ceiling the reader has set, if any. */
export const ceilingFor = (cfg, cluster) =>
  Math.max(cluster.min, Math.round(cfg?.[cluster.capKey] ?? NO_CEILING));
export const isUncapped = (cfg, cluster) => ceilingFor(cfg, cluster) >= NO_CEILING;


/* ── M/M/c ───────────────────────────────────────────────────────────────── */

/** Erlang C — probability an arrival waits, in an M/M/c with offered load `a`. */
function erlangC(c, a) {
  if (a <= 0) return 0;
  if (a >= c) return 1;
  // Recursive Erlang B, which is stable where the factorials are not.
  let b = 1;
  for (let k = 1; k <= c; k += 1) b = (a * b) / (k + a * b);
  const rho = a / c;
  const denom = 1 - rho * (1 - b);
  return denom > 0 ? b / denom : 1;
}

/**
 * One cluster at one instant. `servers` is workers, one per cpu per replica;
 * `serviceMs` is the mean cpu-service time. Returns rps served, rps shed, and
 * the mean and 99th-percentile sojourn in milliseconds.
 *
 * The p99 is the exponential tail of the M/M/c wait plus the tail of one
 * service — an approximation, and labelled as one on the page.
 */
export function queue(lambda, replicas, cluster) {
  const servers = Math.max(0, Math.round(replicas)) * cluster.cpus;
  const mu = 1000 / cluster.serviceMs;         // per server, per second
  const capacity = servers * mu;
  if (lambda <= 0) return { rho: 0, capacity, served: 0, shed: 0, meanMs: cluster.serviceMs, p99Ms: cluster.serviceMs * 4.605, saturated: false };
  if (servers === 0) return { rho: 1, capacity: 0, served: 0, shed: lambda, meanMs: Infinity, p99Ms: Infinity, saturated: true };
  if (lambda >= capacity) {
    return { rho: lambda / capacity, capacity, served: capacity, shed: lambda - capacity, meanMs: Infinity, p99Ms: Infinity, saturated: true };
  }
  const a = lambda / mu;
  const c = erlangC(servers, a);
  const slack = capacity - lambda;
  const wqMean = c / slack;                                  // seconds
  const wq99 = c > 0.01 ? Math.log(c / 0.01) / slack : 0;    // seconds
  return {
    rho: lambda / capacity,
    capacity,
    served: lambda,
    shed: 0,
    meanMs: wqMean * 1000 + cluster.serviceMs,
    p99Ms: wq99 * 1000 + cluster.serviceMs * 4.605,
    saturated: false,
  };
}

/** Replicas needed to hold utilisation at `threshold` for arrival rate λ. */
export const wantedFor = (cluster, lambda, threshold) => {
  // **Vertical pins the count, and that is the difference worth running.** The
  // instance was sized before the sale opened, and a larger one is a stop and a
  // restart rather than a scale-up. So when load arrives above what the machine
  // was bought for, the request sheds — where horizontal would have added a
  // replica and served it. Neither mode moves the lease.
  if (cluster.vertical) return cluster.min;
  return Math.max(
    cluster.min,
    Math.ceil(lambda / (threshold * cluster.cpus * (1000 / cluster.serviceMs))) || cluster.min,
  );
};

/**
 * **What the environment is stood up at, before any traffic arrives.**
 *
 * This is the whole difference between the burst environment and the shared
 * cell, and the package states it: "floor is the expected peak. A burst
 * environment warms before traffic arrives and the first seconds of a sale are
 * the peak — thirty thousand people do not arrive gradually." Sizing reactively
 * here would mean scaling into a peak that is already over: provisioning takes
 * minutes and a sale takes seconds.
 *
 * So the algorithm is applied to the peak that is COMING rather than to the
 * load that is present, and the result is in place by the time the sale opens.
 */
export const anticipatedFor = (cfg, cluster) => {
  const p = variantParams(cfg);
  // Compose as written: the one number it was told, and nothing moves it.
  if (p.fixedReplicas) return cluster.composeReplicas;
  // No pre-warm: stand it up at the resting count and react afterwards. The
  // calculator still says what it should have been; nothing reads it in time.
  if (p.noPrewarm) return cluster.scopeMin || cluster.composeReplicas;
  // Vertical stands up the floor and nothing above it: the capacity went into
  // the size of each replica, so there is no larger count to anticipate.
  if (cluster.vertical) return cluster.min;
  return Math.min(ceilingFor(cfg, { ...cluster, min: saleFloorFor(cfg, cluster).n }),
    sizeFor(cfg.peakRps, cluster.share, replicaRpsFor(cfg, cluster),
      saleFloorFor(cfg, cluster).n, (cfg.thresholdPct ?? 60) / 100));
};

/** Requests a second one replica can carry at full utilisation. */
export const perReplicaRps = (cluster) => cluster.cpus * (1000 / cluster.serviceMs);

/* ── the buyer curve ─────────────────────────────────────────────────────── */

/**
 * Buyers arriving per second at time t. On-sale opens at `leadSec` — the
 * environment is requested at t=0 and the sale opens later, which is the whole
 * point of requesting against the calendar.
 *
 * In free mode there is no calendar: the reader holds the arrival rate.
 */
export function buyersAt(t, cfg) {
  if (cfg.mode === 'free') return cfg.freeBuyers ?? 0;
  const peakBuyers = cfg.peakRps / callsPerBuyer(cfg);
  // On-sale opens leadSec after the environment was REQUESTED, and the request
  // comes after a visible steady period. Provisioning takes minutes and a sale
  // takes seconds, so the lead is what makes the difference.
  const open = (cfg.steadySec ?? 0) + cfg.leadSec;
  const close = open + cfg.saleSec;
  if (t < open) return 0;
  if (t < open + cfg.rampSec) return peakBuyers * ((t - open) / cfg.rampSec) ** 2;
  if (t <= close) {
    const u = (t - open - cfg.rampSec) / Math.max(1, close - open - cfg.rampSec);
    return peakBuyers * (1 - 0.55 * u);
  }
  const after = t - close;
  return after < cfg.graceSec ? peakBuyers * 0.12 * Math.exp(-after / 25) : 0;
}

/* ── the world, and one step of it ───────────────────────────────────────── */

export const DWELL = { provisioning: 240, warming: 150 };

const BASE_CPU = COMPOSE.postgres.cpus + COMPOSE.redis.cpus;
const BASE_GB = COMPOSE.postgres.memGb + COMPOSE.redis.memGb;
// Priced at the package's own sale floors — 14 / 8 / 2 — because that is the
// configuration it costed. A reader who sizes differently is told what the
// difference costs rather than re-baselined onto their own number.
export const PEAK_CPU = BASE_CPU + CLUSTERS.reduce((a, c) => a + c.cpus * c.min, 0);
const PER_CPU_HOUR = RATE_PER_HOUR / PEAK_CPU;

/** Everything that changes as the run proceeds. Mutated in place by stepWorld. */
export function createWorld(cfg) {
  return {
    t: 0,
    state: MACHINE.initial,
    stateSince: 0,
    phases: [{ state: MACHINE.initial, from: 0, to: 0 }],
    running: new Map(CLUSTERS.map((c) => [c.name, 0])),
    pending: [],
    lastScale: -SCALE_TICK,
    lastDown: new Map(CLUSTERS.map((c) => [c.name, -SCALE_DOWN_SEC])),
    actions: [],
    nextAction: 0,
    orders: 0, replayed: 0, rejected: 0,
    offeredTotal: 0, shedTotal: 0, holdRefusedTotal: 0,
    cpuHours: 0, gbHours: 0, spent: 0,
    peakContainers: 0, peakConns: 0, peakP99: 0, peakOfferedRps: 0,
    events: [], openEv: new Map(),
    // The high-water mark per cluster, and the moment the ceiling was first
    // reached. Latched: a ceiling hit for one second is still a ceiling hit,
    // and it is the fact somebody sizing the file needs to see afterwards.
    queued: 0, abandoned: 0, peakQueue: 0, peakWait: 0,
    // **Why a buyer did not get a ticket, kept apart.** "Lost" is not one
    // number: a sale that sold out and a sale that could not serve are
    // opposite outcomes, and lumping them together reads as a failure when it
    // may be a success.
    lostSoldOut: 0, lostLease: 0, lostCapacity: 0, lostQueue: 0, lostFragmented: 0,
    // **Integrity, which is a different kind of failure from capacity.**
    // Contention refuses; it does not corrupt. These are the latent bugs it
    // detonates, and they only appear in the configuration that has them.
    oversold: 0, crashLost: 0, moneyNoSeat: 0, crashedAt: null,
    soldOutAt: null,
    peakN: new Map(CLUSTERS.map((c) => [c.name, 0])),
    peakWant: new Map(CLUSTERS.map((c) => [c.name, 0])),
    capHitAt: new Map(),
    sample: null,
  };
}

const enterState = (w, next, t) => {
  w.phases[w.phases.length - 1].to = t;
  w.state = next;
  w.stateSince = t;
  w.phases.push({ state: next, from: t, to: t });
  if (next === 'reconciling') { w.replayed = 0; w.rejected = 0; }
};

const fireEvent = (w, kind, t, payload) => {
  const cur = w.openEv.get(kind);
  if (cur) {
    cur.to = t;
    // Rewritten while the episode runs, so a window that got worse says how
    // much worse rather than what the first frame looked like.
    if ((payload.peak ?? 0) >= cur.peak) Object.assign(cur, payload, { from: cur.from, to: t });
    return cur;
  }
  const ev = { kind, from: t, to: t, peak: payload.peak ?? 0, ...payload };
  w.openEv.set(kind, ev);
  w.events.push(ev);
  return ev;
};
const clearEvent = (w, kind) => w.openEv.delete(kind);

/** An operation asked for at the world's current time. Refusals are recorded. */
export function applyOperation(w, operation) {
  const tr = MACHINE.transitions.find((x) => x.from === w.state && x.operation === operation);
  if (tr && tr.to !== w.state) { enterState(w, tr.to, w.t); return true; }
  if (tr) return true;
  // **One entry a refusal, not one a press.** Pressing teardown five times in
  // provisioning is the same 409 five times, and nine copies of it in the
  // ledger reads as a stale ledger rather than as an insistent reader.
  const key = `refused:${operation}:${w.state}`;
  const seen = w.events.find((e) => e.kind === key);
  if (seen) { seen.presses = (seen.presses ?? 1) + 1; seen.to = w.t; return false; }
  w.events.push({
    kind: `refused:${operation}:${w.state}`, from: w.t, to: w.t, severity: 'refused', peak: 0,
    title: `409 — ${operation} refused in ${w.state}`,
    detail: operation === 'decommissionBurstEnvironment'
      ? 'decommissioned is reachable only through reconciled. An environment torn down before its orders reach the permanent platform has lost real money and real tickets, and no path in the state model allows it.'
      : `states/burst-environment.yaml declares no transition out of ${w.state} for this operation.`,
    source: 'ADR-0035 · states/burst-environment.yaml',
  });
  return false;
}

/**
 * Advance the world by `dt` simulated seconds and return the sample at the new
 * time. One code path, so a scripted scenario and a free run cannot disagree.
 */
export function stepWorld(w, cfg, dt) {
  const t = w.t + dt;
  w.t = t;
  const threshold = cfg.thresholdPct / 100;
  // The clusters as this config makes them: floors calculated, service times
  // following from the per-replica rates rather than fixed beside them.
  const LIVE = clustersFor(cfg);
  const vp = variantParams(cfg);
  const leaseMs = lockMsFor(cfg);
  // Without an explicit lock the ceiling is the statement rate rather than the
  // lease: one statement, serialised by Postgres for its own duration.
  const holdCap = variantParams(cfg).noLock ? 1000 / 0.2 : 1000 / leaseMs;
  const cpb = callsPerBuyer(cfg);
  const scale = cpb / CALLS_PER_BUYER;   // the package's distribution, re-based
  const close = (cfg.steadySec ?? 0) + cfg.leadSec + cfg.saleSec;
  const fmt = (n) => Math.round(n).toLocaleString('en-GB');

  // scripted operations due by now
  while (w.nextAction < w.actions.length && w.actions[w.nextAction].t <= t) {
    applyOperation(w, w.actions[w.nextAction].operation);
    w.nextAction += 1;
  }

  // system dwell, and the two time-driven transitions
  const dwell = DWELL[w.state];
  if (dwell != null && t - w.stateSince >= dwell) {
    const tr = MACHINE.transitions.find((x) => x.from === w.state && x.trigger === 'system' && x.to !== 'failed');
    if (tr) enterState(w, tr.to, t);
  }
  if (cfg.mode !== 'free') {
    if (w.state === 'live' && t >= close + cfg.graceSec) enterState(w, 'draining', t);
    if (w.state === 'draining' && t - w.stateSince >= 60) enterState(w, 'reconciling', t);
  }

  const live = w.state === 'live';
  const infra = w.state !== 'requested' && w.state !== 'decommissioned';

  // containers arriving
  for (let k = w.pending.length - 1; k >= 0; k -= 1) {
    if (t >= w.pending[k].readyAt) {
      w.running.set(w.pending[k].name, (w.running.get(w.pending[k].name) ?? 0) + 1);
      w.pending.splice(k, 1);
    }
  }
  // **Provisioning stands up the size that was asked for.** requestBurstEnvironment
  // asks for an environment sized to the expected peak; it does not discover
  // that size later. So warming begins with those replicas already, and the
  // autoscaler only ever adds to them — scaling into a fifty-second peak after
  // it arrives is scaling into a peak that is already over.
  if (w.state === 'warming') {
    for (const c of LIVE) {
      const want = anticipatedFor(cfg, c);
      if ((w.running.get(c.name) ?? 0) < want) w.running.set(c.name, want);
    }
  }
  if (!infra) { for (const c of LIVE) w.running.set(c.name, 0); w.pending.length = 0; }

  const offeredBuyers = live ? buyersAt(t, cfg) : 0;

  const wants = new Map();
  for (const c of LIVE) {
    // The larger of what the coming peak needs and what the present load needs,
    // so it never scales back below the size the sale was provisioned for.
    const reactive = wantedFor(c, offeredBuyers * c.cpb * scale, threshold);
    wants.set(c.name, infra
      ? (vp.fixedReplicas ? c.composeReplicas
        : vp.noPrewarm ? reactive
          : Math.max(anticipatedFor(cfg, c), reactive))
      : 0);
  }
  if (vp.fixedReplicas) {
    // No autoscaler at all: whatever compose was told, for the whole sale.
    for (const c of LIVE) w.running.set(c.name, infra ? c.composeReplicas : 0);
    w.pending.length = 0;
  } else if (infra && t - w.lastScale >= SCALE_TICK) {
    w.lastScale = t;
    for (const c of LIVE) {
      const want = wants.get(c.name);
      const now = (w.running.get(c.name) ?? 0) + w.pending.filter((p) => p.name === c.name).length;
      const ceiling = ceilingFor(cfg, c);
      const stepN = Math.max(1, Math.ceil((cfg.scaleStepPct / 100) * Math.min(ceiling, c.min * 4)));
      if (want > now) {
        const add = Math.min(stepN, Math.min(ceiling, want) - now);
        for (let k = 0; k < add; k += 1) w.pending.push({ name: c.name, readyAt: t + cfg.startSec });
      } else if (want < now && now > c.min && t - w.lastDown.get(c.name) >= SCALE_DOWN_SEC) {
        w.lastDown.set(c.name, t);
        w.running.set(c.name, Math.max(c.min, (w.running.get(c.name) ?? 0) - 1));
      }
    }
  }

  // per-cluster queueing
  let offeredRps = 0, conns = 0, containers = 0;
  let cpu = infra ? BASE_CPU : 0;
  let gb = infra ? BASE_GB : 0;
  let worstP99 = 0;
  const capShort = [];
  const lag = [];
  const perCluster = [];
  for (const c of LIVE) {
    const n = w.running.get(c.name) ?? 0;
    const lambda = offeredBuyers * c.cpb * scale;
    const q = queue(lambda, n, c);
    offeredRps += lambda;
    conns += n * c.poolMax;
    containers += n;
    cpu += c.cpus * n;
    gb += c.memGb * n;
    // Per-cluster only; the lock wait is added after the contention block and
    // worstP99 is recomputed there.
    worstP99 = Number.isFinite(q.p99Ms) && Number.isFinite(worstP99)
      ? Math.max(worstP99, q.p99Ms) : (lambda > 0 ? Infinity : worstP99);
    const want = wants.get(c.name);
    const ceiling = ceilingFor(cfg, c);
    if (n > (w.peakN.get(c.name) ?? 0)) w.peakN.set(c.name, n);
    if (want > (w.peakWant.get(c.name) ?? 0)) w.peakWant.set(c.name, want);
    if (n >= ceiling && !w.capHitAt.has(c.name)) w.capHitAt.set(c.name, t);
    if (want > ceiling) capShort.push(`${c.short} wants ${want} of ${ceiling}`);
    else if (live && want > n + 0.5) lag.push(`${c.short} at ${n} of ${want}`);
    perCluster.push({ name: c.name, short: c.short, n, want, max: ceiling, uncapped: isUncapped(cfg, c), rho: q.rho,
      p99: q.p99Ms, lambda, capacity: q.capacity, saturated: q.saturated,
      peakN: w.peakN.get(c.name) ?? 0,
      peakWant: w.peakWant.get(c.name) ?? 0,
      capHitAt: w.capHitAt.get(c.name) ?? null,
      starting: w.pending.filter((p) => p.name === c.name).length });
  }

  /* ── the two leases, serialised ──────────────────────────────────────────
     Sharding is the only thing that moves this, and only for the buyers who
     will take any seat: somebody choosing a specific seat is contending for
     that seat rather than for capacity, and no shard count changes it. */
  const anyShare = cfg.anySeatPct / 100;
  const holdCapAny = holdCap * vp.leaseShards;
  // Every convergent row is its own queue; an insert-hot row competes for an
  // index tail rather than a lock, so it carries far more before it bites.
  const rowState = CONTENDED.map((k) => {
    const insert = k.kind === 'insert';
    const ceiling = insert ? holdCap / INSERT_COST : holdCap;
    const ceilingAny = insert ? ceiling : holdCapAny;
    const demand = live ? offeredBuyers * k.cpb * scale : 0;
    const served = insert
      ? Math.min(demand, ceiling)
      : Math.min(demand * anyShare, ceilingAny) + Math.min(demand * (1 - anyShare), ceiling);
    return { ...k, insert, ceiling, ceilingAny, demand, served, refused: Math.max(0, demand - served) };
  });
  const invDemand = rowState[0].demand;
  const seatDemand = rowState[1].demand;
  const invServed = rowState[0].served;
  const seatServed = rowState[1].served;
  const holdRefused = rowState.reduce((a, r) => a + r.refused, 0);
  const effectiveHoldCap = holdCapAny * anyShare + holdCap * (1 - anyShare);

  /* **Lock wait belongs in the latency, not beside it.**
   *
   * The queueing above is for cpu at the service; this is the wait for a row.
   * Reporting a p99 that excludes it makes the figure useless exactly when it
   * matters — a cluster can read 74ms while every buyer is convoying on one
   * lock. A held row is a deterministic service time, so M/D/1 rather than
   * M/M/1: Wq = ρD / 2(1−ρ). Above ρ = 1 there is no finite wait at all, and
   * under SKIP LOCKED the attempt returns no row rather than queueing.
   */
  // Utilisation of the busiest row, not of all of them added together: they
  // are separate queues, and the worst one is what a buyer waits behind.
  const lockRho = rowState.reduce((a, r) => Math.max(a,
    r.ceiling > 0 ? r.demand / (r.insert ? r.ceiling : effectiveHoldCap) : 0), 0);
  const lockWaitMs = lockRho >= 1 ? Infinity
    : (lockRho * leaseMs) / (2 * (1 - lockRho));
  // The tail of that wait. Approximated as exponential above the mean, and
  // labelled as an approximation wherever it is shown.
  const lockP99Ms = Number.isFinite(lockWaitMs) ? lockWaitMs * 4.605 : Infinity;

  // Only the service that actually takes the locks carries the wait:
  // acquireInventoryHold and createSeatHold are both CatalogueService.
  const HOLDERS = new Set(CONTENDED.map((k) => {
    const op = OPS.find((o) => o.id === k.op);
    return op ? op.service : null;
  }).filter(Boolean));
  for (const pc of perCluster) {
    pc.lockWaitMs = HOLDERS.has(pc.name) ? lockWaitMs : 0;
    pc.lockP99Ms = HOLDERS.has(pc.name) ? lockP99Ms : 0;
    pc.cpuP99 = pc.p99;
    if (HOLDERS.has(pc.name) && live) {
      pc.p99 = Number.isFinite(pc.p99) && Number.isFinite(lockP99Ms)
        ? pc.p99 + lockP99Ms : Infinity;
    }
  }
  worstP99 = perCluster.reduce((a, pc) => (
    Number.isFinite(pc.p99) && Number.isFinite(a) ? Math.max(a, pc.p99)
      : (pc.lambda > 0 ? Infinity : a)), 0);

  let buyerCap = offeredBuyers;
  let bindingStage = 'nothing';
  if (live) {
    // Any of the rows can be the one that holds the sale back.
    const leaseCap = rowState.reduce((a, r) => (
      r.demand > 0 ? Math.min(a, r.served / (r.cpb * scale)) : a), Infinity);
    let clusterCap = Infinity;
    for (const pc of perCluster) {
      const c = LIVE.find((x) => x.name === pc.name);
      clusterCap = Math.min(clusterCap, pc.capacity / (c.cpb * scale));
    }
    buyerCap = Math.min(offeredBuyers, leaseCap, clusterCap);
    // Which stage actually held them back — named, so the shortfall can be
    // attributed instead of reported as one undifferentiated loss.
    if (buyerCap >= offeredBuyers - 0.001) bindingStage = 'nothing';
    else bindingStage = leaseCap <= clusterCap ? 'lease' : 'capacity';
  }
  const completed = live ? Math.max(0, buyerCap) : 0;

  /* ── sold out ────────────────────────────────────────────────────────
     There are only so many seats. Orders stop at the venue's own number, and
     the moment they do is the moment worth seeing — a sale that sells out in
     twelve minutes and one that sheds for twenty look identical on a
     throughput chart and are not the same event. */
  const seats = seatsFor(cfg);
  const soldOut = w.orders >= seats - 0.5;
  const room = Math.max(0, seats - w.orders);
  // A sharded lease can refuse a buyer while stock remains: their shard is
  // empty even though the performance is not. Nothing rebalances it.
  const fragShare = soldOut ? 0 : fragmentedShare(cfg, room, seats);
  const beforeFrag = soldOut ? 0 : Math.min(completed, room / Math.max(dt, 0.001));
  const sellable = beforeFrag * (1 - fragShare);
  const fragmented = beforeFrag - sellable;
  if (soldOut && w.soldOutAt == null) w.soldOutAt = t;

  /* **Attribute the shortfall, exhaustively.** A buyer who arrives after the
     last seat is gone is not a buyer the environment failed to serve, and
     calling both "lost" hides the only distinction that matters. The split is
     by construction rather than by a chain of tests: every buyer who got
     nothing lands in exactly one bucket, so the buckets always sum to
     offered − orders. */
  const unmet = live ? Math.max(0, offeredBuyers - sellable) : 0;
  let unmetReason = 'nothing';
  if (unmet > 1e-9) {
    // The share refused by an empty shard is known exactly; the rest is
    // whatever stage was binding.
    const fragPart = Math.min(fragmented, unmet);
    const rest = unmet - fragPart;
    w.lostFragmented += fragPart * dt;
    // Stock can run out part-way through a step: the room left, not any stage
    // of the environment, is what refused them.
    const stockLimited = !soldOut && beforeFrag < completed - 1e-9;
    if (soldOut || stockLimited) w.lostSoldOut += rest * dt;
    else if (bindingStage === 'lease') w.lostLease += rest * dt;
    else if (bindingStage === 'capacity') w.lostCapacity += rest * dt;
    else w.lostQueue += rest * dt;
    unmetReason = fragPart > rest ? 'an empty shard'
      : (soldOut || stockLimited) ? 'no stock left'
        : bindingStage === 'lease' ? 'the lease path'
          : bindingStage === 'capacity' ? 'cluster capacity'
            : 'nothing identifiable';
  }

  /* ── integrity, which contention does not cause but does detonate ─────
     A row lock refuses; it does not corrupt. The paths below are safe at five
     buyers a second and unsafe at two hundred and eighty-three, and none of
     them shows up in testing. They only run in the configuration that has the
     bug, so A stays clean and X does not. */
  let oversold = 0;
  let moneyNoSeat = 0;
  if (live && vp.unsafeGuard) {
    // Read-then-update: SELECT remaining, check in the application, UPDATE.
    // The race window is the statement round trip, so the collision rate is
    // 1 − e^(−λw) on a single convergent row. Microseconds at low load,
    // constant at peak — and every collision is a lost update, so inventory
    // goes negative and seats are sold twice.
    const w0 = leaseMs / 1000;
    const collide = 1 - Math.exp(-Math.max(0, invDemand) * w0);
    oversold = sellable * collide;
    w.oversold += oversold * dt;
  }
  if (live && Number.isFinite(lockWaitMs) && lockWaitMs > 0) {
    // A guest who waits on the lock, goes to the gateway and comes back to a
    // hold that has expired: payment captured, seat gone. Not data loss — a
    // reconciliation break, and a guest at the gate with an invalid ticket.
    const gatewaySec = 9;                       // mine — 3 to 15 seconds
    const journeySec = lockWaitMs / 1000 + gatewaySec;
    if (journeySec > cfg.holdTtlSec) {
      moneyNoSeat = sellable * Math.min(1, (journeySec - cfg.holdTtlSec) / Math.max(1, cfg.holdTtlSec));
      w.moneyNoSeat += moneyNoSeat * dt;
    }
  }

  /* ── the waiting queue ────────────────────────────────────────────────
     The overflow above the ceiling is not refused, it waits. Drained by
     whatever spare capacity the clusters have; a buyer who has been waiting
     longer than maxWaitSec has gone, and that abandonment is the only thing
     the model now counts as lost. */
  let overflow = 0;
  let spare = 0;
  let capacityTotal = 0;
  for (const pc of perCluster) {
    capacityTotal += pc.capacity;
    overflow += Math.max(0, pc.lambda - pc.capacity);
    spare += Math.max(0, pc.capacity - pc.lambda);
  }
  const drain = Math.min(w.queued / Math.max(dt, 0.001), spare);
  w.queued = Math.max(0, w.queued + (overflow - drain) * dt);
  const waitSec = capacityTotal > 0 ? w.queued / capacityTotal : 0;
  let abandoned = 0;
  if (waitSec > cfg.maxWaitSec) {
    abandoned = w.queued - cfg.maxWaitSec * capacityTotal;
    w.queued -= abandoned;
    w.abandoned += abandoned;
  }
  w.peakQueue = Math.max(w.peakQueue, w.queued);
  w.peakWait = Math.max(w.peakWait, Math.min(waitSec, cfg.maxWaitSec));

  /* ── what each store is asked for ─────────────────────────────────────
     Split by verb: 35 of a buyer's 55 calls are GETs and 20 are writes.
     postgres-hot answers through the pooler's 80 server connections, so its
     ceiling is those 80 divided by the mean statement time. */
  const readRps = live ? offeredBuyers * READ_CPB * scale : 0;
  // B serves 23 of the 35 read calls from Redis and R takes the whole read path
  // off Postgres, so what reaches the database is what is left.
  const dbReadRps = live ? offeredBuyers * Math.max(0, READ_CPB - vp.cachedReadCpb) * scale : 0;
  const cacheReadRps = readRps - dbReadRps;
  // D coalesces three chatty writes a buyer into one statement.
  const writeCpbEff = Math.max(1, WRITE_CPB - (vp.batchedWriteCpb > 0 ? vp.batchedWriteCpb - 1 : 0));
  const writeRps = live ? offeredBuyers * writeCpbEff * scale : 0;
  const dbCapacity = (vp.poolSize * 1000) / cfg.dbStatementMs;

  w.orders += sellable * dt;
  w.offeredTotal += offeredBuyers * dt;
  w.shedTotal += Math.max(0, offeredBuyers - completed) * dt;
  w.holdRefusedTotal += holdRefused * dt;

  // the merge back
  if (w.state === 'reconciling' && w.orders > 0) {
    const rate = Math.max(400, w.orders / 180);
    const moved = Math.min(w.orders - w.replayed - w.rejected, rate * dt);
    const toReject = cfg.policy === 'reject' ? moved * (cfg.divergencePct / 100) : 0;
    w.rejected += toReject;
    w.replayed += moved - toReject;
    if (w.replayed + w.rejected >= w.orders - 1) enterState(w, 'reconciled', t);
  } else if (w.state === 'reconciling') enterState(w, 'reconciled', t);
  if (w.state === 'reconciled' && cfg.autoDecommission && t - w.stateSince >= 60) {
    enterState(w, 'decommissioned', t);
  }

  if (infra) {
    const hours = dt / 3600;
    w.cpuHours += cpu * hours;
    w.gbHours += gb * hours;
    w.spent += cpu * PER_CPU_HOUR * hours;
  }

  // named failures
  if (capShort.length) {
    fireEvent(w, 'cap', t, { severity: 'hard', peak: capShort.length,
      title: 'Replica ceiling reached',
      detail: `${capShort.join(' · ')}. That ceiling is yours: the package sets none, because a cap is a cap on absorbing a peak nobody predicted and the peak is the whole reason the environment exists. Above it the overflow waits, and a buyer who waits longer than ${cfg.maxWaitSec}s is gone.`,
      source: 'the reader’s ceilings · c-flash-sale.yml: “in a real deployment there is no maximum”' });
  } else clearEvent(w, 'cap');

  if (lag.length && live) {
    fireEvent(w, 'lag', t, { severity: 'hard', peak: lag.length,
      title: 'Scale-up could not keep pace',
      detail: `${lag.join(' · ')}. A scaling decision every ${SCALE_TICK}s, ${cfg.scaleStepPct}% of the ceiling a step, ${cfg.startSec}s to ready.`,
      source: 'the reader’s scale step and start time' });
  } else clearEvent(w, 'lag');

  const lostBuyers = live ? offeredBuyers - completed : 0;
  const envCalls = DEPLOYED_CPB * scale;
  if (soldOut && live) {
    fireEvent(w, 'soldout', t, { severity: 'soft', peak: seats,
      title: `Sold out — ${fmt(seats)} seats gone`,
      detail: `Every seat the venue put on sale is taken${w.soldOutAt != null ? ` at ${clock(w.soldOutAt)}` : ''}, so demand after this point is refused for want of stock rather than for want of capacity. That is the distinction a throughput chart hides: a sale that sells out and a sale that sheds look the same on it and are not the same event.`,
      source: `${(VENUES.find((v) => v.key === cfg.venue) ?? VENUES[2]).label} · ${fmt(seats)} buying guests, TICVAI_Deployment_Technical Part 2` });
  } else clearEvent(w, 'soldout');

  if (w.oversold > 1) {
    fireEvent(w, 'oversell', t, { severity: 'integrity', peak: Math.round(w.oversold),
      title: `Overselling — ${fmt(w.oversold)} seats sold twice`,
      detail: `A read-then-update guard on a convergent row. ${fmt(oversold)} a second are colliding now and ${fmt(w.oversold)} have been lost so far: inventory goes negative and two guests hold one seat. This is not what contention does — contention refuses — it is the latent bug contention detonates, and it is invisible at low load. A guarded update, remaining = remaining - 1 WHERE remaining > 0, is safe at any contention level.`,
      source: 'variant X · the unsafe path' });
  } else clearEvent(w, 'oversell');

  if (moneyNoSeat > 0.5) {
    fireEvent(w, 'ttl', t, { severity: 'integrity', peak: Math.round(w.moneyNoSeat),
      title: `Payment captured, seat gone — ${fmt(w.moneyNoSeat)} so far`,
      detail: `A ${fmt(lockWaitMs)}ms lock wait plus a gateway round trip is longer than the ${cfg.holdTtlSec}s hold, so the seat is released while the guest is paying. Money taken, no seat: a reconciliation break and a guest at the gate with an invalid ticket. The checkout TTL has to exceed worst-case lock wait plus gateway plus margin, and the package states no TTL at all.`,
      source: 'the reader’s hold TTL · the package sets none' });
  } else clearEvent(w, 'ttl');

  if (fragmented > 1) {
    fireEvent(w, 'fragment', t, { severity: 'hard', peak: Math.round(fragmented),
      title: 'Shards emptying unevenly',
      detail: `${Math.round(fragShare * 100)}% of buyers are told there is nothing left while ${fmt(room)} seats remain in other shards — ${fmt(fragmented)} a second. Sixteen sub-pools each empty separately and nothing rebalances them, so the last seats fragment. This is what sharding the lease costs: a throughput wall traded for a correctness one that only appears at the end of the sale.`,
      source: 'deploy/variants/C-lease-shards.yml · the distribution is mine' });
  } else clearEvent(w, 'fragment');

  if (w.queued > 1) {
    fireEvent(w, 'queue', t, { severity: waitSec > cfg.maxWaitSec * 0.5 ? 'hard' : 'soft', peak: Math.round(w.queued),
      title: 'Requests waiting',
      detail: `${fmt(w.queued)} requests held in the queue, ${waitSec.toFixed(1)}s of wait at the current drain rate. They are above the ceiling you set rather than above what the model could scale to${abandoned > 1 ? `, and ${fmt(abandoned)} a second are abandoning` : ''}.`,
      source: 'the reader’s ceilings and max wait' });
  } else clearEvent(w, 'queue');

  if (dbReadRps + writeRps > dbCapacity) {
    fireEvent(w, 'db', t, { severity: 'hard', peak: Math.round(dbReadRps + writeRps),
      title: 'postgres-hot at its statement ceiling',
      detail: `${fmt(dbReadRps + writeRps)} statements a second reaching the database — ${fmt(dbReadRps)} read, ${fmt(writeRps)} written — against ${fmt(dbCapacity)}: ${vp.poolSize} server connections at a ${cfg.dbStatementMs}ms mean statement. max_connections is ${COMPOSE.postgres.maxConnections}, and transaction pooling is what keeps the tier scaling past six replicas.`,
      source: `${vp.variant.file} · pgbouncer DEFAULT_POOL_SIZE` });
  } else clearEvent(w, 'db');

  if (abandoned > 1) {
    fireEvent(w, 'shed', t, { severity: 'hard', peak: Math.round(abandoned),
      title: 'Buyers abandoning the queue',
      detail: `${fmt(abandoned)} requests a second dropped after waiting ${cfg.maxWaitSec}s — about ${fmt(abandoned / Math.max(envCalls, 1))} buyers a second. ADR-0032 sheds guest and public first, staff and service last, and the reason the queue is bounded at all is that a guest waiting in one does not know whether they have a ticket.`,
      source: 'ADR-0032 · ADR-0035 alternatives' });
  } else clearEvent(w, 'shed');

  if (holdRefused > 1) {
    fireEvent(w, 'lock', t, { severity: 'hard', peak: Math.round(holdRefused),
      title: 'Lease path serialising',
      detail: (() => {
        const worst = rowState.reduce((a, r) => (r.refused > (a?.refused ?? -1) ? r : a), null);
        return worst ? `${fmt(holdRefused)} attempts a second find no row across ${rowState.filter((r) => r.refused > 1).length} of the ${rowState.length} rows a purchase converges on. The worst is ${worst.table} at ${fmt(worst.refused)} a second: ${worst.insert ? 'an insert-hot index tail' : 'one row every buyer reaches, so the writes serialise'}${worst.flagged ? ' (flagged contended in burst-scope)' : ' — not flagged contended in burst-scope, and it is'}.` : '';
      })() + ' ' + (vp.leaseShards > 1
        ? `The lease is sharded ${vp.leaseShards} ways, so a convergent row carries ${fmt(holdCapAny)} a second for the ${cfg.anySeatPct}% who will take any seat and ${fmt(holdCap)} for the rest, who are contending for a specific seat and cannot be sharded out of it.`
        : `At a ${leaseMs}ms hold a convergent row carries ${fmt(holdCap)} a second and an insert-hot one about ${fmt(holdCap / INSERT_COST)}. No replica count changes either.`),
      source: 'ADR-0031 · ADR-0035 consequences · burst-scope tables[]' });
  } else clearEvent(w, 'lock');

  if (Number.isFinite(worstP99) && worstP99 > cfg.sloMs) {
    fireEvent(w, 'slo', t, { severity: 'soft', peak: Math.round(worstP99),
      title: `p99 over ${cfg.sloMs}ms`,
      detail: (() => {
        const hot = perCluster.reduce((a, pc) => (pc.p99 > (a?.p99 ?? -1) ? pc : a), null);
        const lockPart = hot && Number.isFinite(hot.lockP99Ms) ? hot.lockP99Ms : 0;
        return `${fmt(worstP99)}ms at ${hot ? hot.short : 'the worst cluster'}`
          + (lockPart > 1
            ? ` — ${fmt(hot.cpuP99)}ms of it queueing for cpu and ${fmt(lockPart)}ms waiting for a row. The lock is ${Math.round(lockRho * 100)}% utilised, and that wait is in this figure rather than beside it.`
            : '. All of it is cpu queueing; the lease path is not contended at this load.');
      })(),
      source: 'the reader’s SLO · M/D/1 on the lease, M/M/c on the cpu' });
  } else clearEvent(w, 'slo');

  if (conns > vp.maxClient) {
    fireEvent(w, 'pool', t, { severity: 'hard', peak: conns,
      title: 'MAX_CLIENT_CONN exhausted',
      detail: `${fmt(conns)} client connections against ${fmt(vp.maxClient)}, answered from ${vp.poolSize} server connections.`,
      source: `${vp.variant.file} · pgbouncer` });
  } else clearEvent(w, 'pool');

  w.peakContainers = Math.max(w.peakContainers, containers);
  w.peakConns = Math.max(w.peakConns, conns);
  w.peakOfferedRps = Math.max(w.peakOfferedRps, offeredRps);
  if (Number.isFinite(worstP99)) w.peakP99 = Math.max(w.peakP99, worstP99);
  w.phases[w.phases.length - 1].to = t;

  const servedRps = live ? sellable * DEPLOYED_CPB * scale : 0;
  w.sample = {
    t, state: w.state, buyers: offeredBuyers, offeredRps,
    servedRps, shedRps: Math.max(0, offeredRps - servedRps),
    completed, orders: w.orders, containers, conns, p99: worstP99, cpu,
    spent: w.spent, replayed: w.replayed, rejected: w.rejected,
    invDemand, invServed, seatDemand, seatServed, holdRefused,
    holdCapAny, effectiveHoldCap, leaseShards: vp.leaseShards,
    rows: rowState,
    lockRho, lockWaitMs, lockP99Ms,
    cacheReadRps, dbReadRps, maxClient: vp.maxClient, poolSize: vp.poolSize,
    variant: vp.variant.key, batchWindowMs: vp.batchWindowMs, redisPooler: vp.redisPooler,
    envCalls, sharedCellRps: live ? offeredBuyers * SHARED_CELL_CPB * scale : 0,
    seats, soldOut, room, sellable, soldOutAt: w.soldOutAt,
    unmet, unmetReason, bindingStage, fragShare, fragmented,
    oversold, moneyNoSeat, oversoldTotal: w.oversold, moneyNoSeatTotal: w.moneyNoSeat,
    leaseMs, noLock: vp.noLock, unsafeGuard: vp.unsafeGuard,
    // The venue's ordinary day, which runs in the shared cell throughout —
    // before the environment is requested, while the sale is live, and after it
    // is torn down. It is no part of what this environment is sized for.
    routineRps: ROUTING.normal.rps,
    normal: normalSizing(cfg),
    queued: w.queued, waitSec: Math.min(waitSec, cfg.maxWaitSec), abandoned,
    readRps, writeRps, dbCapacity, dbLoad: dbCapacity > 0 ? (dbReadRps + writeRps) / dbCapacity : 0,
    capacityTotal, overflow,
    clusters: perCluster, holdCap,
  };
  return w.sample;
}

/** What the world adds up to, at whatever point it has reached. */
export function summarise(w, cfg) {
  return {
    endState: w.state,
    orders: Math.round(w.orders),
    offered: Math.round(w.offeredTotal),
    shed: Math.round(w.shedTotal),
    abandoned: Math.round(w.abandoned),
    peakQueue: Math.round(w.peakQueue),
    peakWait: w.peakWait,
    holdRefused: Math.round(w.holdRefusedTotal),
    replayed: Math.round(w.replayed),
    rejected: Math.round(w.rejected),
    peakContainers: w.peakContainers,
    peakConns: w.peakConns,
    peakP99: w.peakP99,
    peakOfferedRps: w.peakOfferedRps,
    cpuHours: w.cpuHours,
    gbHours: w.gbHours,
    spent: w.spent,
    conversion: w.offeredTotal > 0 ? w.orders / w.offeredTotal : 1,
    lostSoldOut: Math.round(w.lostSoldOut),
    lostLease: Math.round(w.lostLease),
    lostCapacity: Math.round(w.lostCapacity),
    lostQueue: Math.round(w.lostQueue),
    lostFragmented: Math.round(w.lostFragmented),
    oversold: Math.round(w.oversold),
    moneyNoSeat: Math.round(w.moneyNoSeat),
    // Everything the environment failed to serve, as opposed to had nothing to
    // sell. The two together must equal offered − orders, and `reconciles`
    // says whether they do — this identity has drifted twice.
    lostServed: Math.round(w.lostLease + w.lostCapacity + w.lostQueue + w.lostFragmented),
    reconciles: Math.abs(
      (w.lostSoldOut + w.lostLease + w.lostCapacity + w.lostQueue + w.lostFragmented)
      - (w.offeredTotal - w.orders),
    ) < Math.max(2, w.offeredTotal * 0.005),
    seats: seatsFor(cfg),
    soldOutAt: w.soldOutAt,
    forgotten: cfg.forgottenHours > 0
      ? { hours: cfg.forgottenHours, usd: cfg.forgottenHours * RATE_PER_HOUR }
      : null,
  };
}

/**
 * A whole scripted run as one value — which is what makes the timeline
 * scrubbable and a result reproducible. Free mode does not call this; it steps
 * the same world live.
 */
export function solve(cfg, script = []) {
  const close = (cfg.steadySec ?? 0) + cfg.leadSec + cfg.saleSec;
  const horizon = Math.max(close + cfg.graceSec + 900, 1800);
  const dt = Math.max(1, Math.round(horizon / 2400));

  const w = createWorld(cfg);
  w.actions = [...script].sort((a, b) => a.t - b.t);
  const samples = [stepWorld(w, cfg, 0)];
  for (let t = dt; t <= horizon; t += dt) {
    samples.push(stepWorld(w, cfg, dt));
    if (w.state === 'decommissioned') break;
  }

  const last = samples[samples.length - 1];
  for (const ev of w.events) if (ev.to <= ev.from) ev.to = Math.min(last.t, ev.from + dt);

  if (cfg.policy !== 'reject' && cfg.divergencePct > 0) {
    w.events.push({
      kind: 'policy', from: 0, to: last.t, severity: 'soft', peak: cfg.divergencePct,
      title: `${cfg.divergencePct}% of orders replay under ${cfg.policy}`,
      detail: cfg.policy === 'honourCurrent'
        ? 'Correct in the ledger, and it charges somebody a price they never saw.'
        : 'What a guest expects, and it may undercharge.',
      source: 'ADR-0035 · priceDivergencePolicy has no default',
    });
  }
  if (w.rejected >= 1) {
    w.events.push({
      kind: 'rejected', from: w.phases.find((p) => p.state === 'reconciling')?.from ?? 0,
      to: last.t, severity: 'hard', peak: Math.round(w.rejected),
      title: `${Math.round(w.rejected).toLocaleString('en-GB')} orders rejected at reconciliation`,
      detail: 'They land in sync.rejection and are worked afterwards. Safe, and it turns a completed purchase into a support case.',
      source: 'ADR-0035 · sync.rejection',
    });
  }

  return {
    dt, horizon: last.t, samples,
    events: w.events, phases: w.phases.filter((p) => p.to > p.from),
    summary: summarise(w, cfg),
    recommendation: recommend(cfg),
  };
}

/* ── the recommendation ──────────────────────────────────────────────────── */

/**
 * Not a rule of thumb: the same queueing model, solved at the peak the ADR
 * names, for the smallest replica count that holds the reader's SLO. The
 * contention limit is reported separately because no replica count moves it.
 */
export function recommend(cfg) {
  const vp = variantParams(cfg);
  const LIVE = clustersFor(cfg);
  const cpb = callsPerBuyer(cfg);
  const scale = cpb / CALLS_PER_BUYER;
  const peakBuyers = cfg.peakRps / cpb;
  const holdCap = vp.noLock ? 1000 / 0.2 : 1000 / lockMsFor(cfg);

  const perCluster = LIVE.map((c) => {
    const lambda = peakBuyers * c.cpb * scale;
    const atThreshold = wantedFor(c, lambda, cfg.thresholdPct / 100);
    // the smallest n whose p99 holds the SLO
    let forSlo = c.min;
    for (let n = c.min; n <= 400; n += 1) {
      const q = queue(lambda, n, c);
      if (Number.isFinite(q.p99Ms) && q.p99Ms <= cfg.sloMs) { forSlo = n; break; }
      forSlo = n;
    }
    const need = Math.max(atThreshold, forSlo);
    return {
      ...c, lambda, atThreshold, forSlo, need,
      ceiling: ceilingFor(cfg, c),
      shortfall: Math.max(0, need - ceilingFor(cfg, c)),
      p99AtCap: queue(lambda, ceilingFor(cfg, c), c).p99Ms,
      rhoAtCap: queue(lambda, ceilingFor(cfg, c), c).rho,
    };
  });

  // The highest target utilisation that still fits inside the file's ceilings
  // and holds the SLO. Descending, so the answer is the loosest that works.
  let bestThreshold = null;
  for (let pct = 95; pct >= 40; pct -= 1) {
    const ok = LIVE.every((c) => {
      const lambda = peakBuyers * c.cpb * scale;
      const n = wantedFor(c, lambda, pct / 100);
      if (n > ceilingFor(cfg, c)) return false;
      const q = queue(lambda, n, c);
      return Number.isFinite(q.p99Ms) && q.p99Ms <= cfg.sloMs;
    });
    if (ok) { bestThreshold = pct; break; }
  }

  const worstNeed = perCluster.reduce((a, c) => Math.max(a, Math.ceil((c.need - c.min) / Math.max(1, Math.ceil((cfg.scaleStepPct / 100) * Math.min(ceilingFor(cfg, c), c.min * 4))))), 0);
  const scaleSec = worstNeed * SCALE_TICK + cfg.startSec;
  const prewarmSec = DWELL.provisioning + DWELL.warming + scaleSec;

  const effHold = holdCap * (vp.leaseShards * (cfg.anySeatPct / 100) + (1 - cfg.anySeatPct / 100));
  const invCap = effHold / (CONTENDED[0].cpb * scale);   // buyers a second
  const seatCap = effHold / (CONTENDED[1].cpb * scale);
  const contentionBuyers = Math.min(invCap, seatCap);

  // Against the floors compose is told, which is the only number in the file.
  const diff = perCluster.filter((c) => c.need !== c.composeReplicas).map((c) => ({
    service: c.name.toLowerCase(),
    was: c.composeReplicas,
    now: c.need,
  }));
  const dbCapacity = (vp.poolSize * 1000) / cfg.dbStatementMs;
  const dbReads = peakBuyers * Math.max(0, READ_CPB - vp.cachedReadCpb) * scale;
  const dbWrites = peakBuyers * Math.max(1, WRITE_CPB - (vp.batchedWriteCpb > 0 ? vp.batchedWriteCpb - 1 : 0)) * scale;
  const store = {
    readRps: dbReads,
    writeRps: dbWrites,
    capacity: dbCapacity,
    over: dbReads + dbWrites > dbCapacity,
    cached: peakBuyers * vp.cachedReadCpb * scale,
  };

  return {
    perCluster,
    bestThreshold,
    prewarmSec,
    scaleSec,
    contention: {
      holdCap: effHold,
      baseHoldCap: holdCap,
      shards: vp.leaseShards,
      contentionBuyers,
      contentionRps: contentionBuyers * cpb,
      peakBuyers,
      shortfall: Math.max(0, peakBuyers - contentionBuyers),
      binding: contentionBuyers < peakBuyers,
    },
    diff, store, variant: vp.variant,
    aboveFloor: perCluster.filter((c) => c.need > c.min),
    verdict: perCluster.some((c) => c.shortfall > 0)
      ? `Your ceilings cannot serve ${cfg.peakRps.toLocaleString('en-GB')} RPS at ${cfg.thresholdPct}% — the overflow waits`
      : perCluster.some((c) => c.need > c.min)
        ? `It reaches ${cfg.peakRps.toLocaleString('en-GB')} RPS by scaling past the floors, which is what the floors are for`
        : `${cfg.peakRps.toLocaleString('en-GB')} RPS is carried by the floors alone — nothing has to scale`,
  };
}

/**
 * **What declining each improvement costs.** The comparison table answers
 * "does this help"; this answers "what does it cost you not to do it", which is
 * the question a client actually has to decide. Same arithmetic, opposite
 * framing, and it is weighted: only one of the four moves the binding
 * constraint, so presenting four equal risks would be its own kind of lie.
 */
export function regressions(cfg) {
  const base = recommend({ ...cfg, variant: 'A' });
  const peakBuyers = cfg.peakRps / callsPerBuyer(cfg);
  return VARIANTS.filter((v) => v.key !== 'A').map((v) => {
    const withIt = recommend({ ...cfg, variant: v.key });
    const holdsGain = withIt.contention.contentionRps - base.contention.contentionRps;
    const dbSaved = (base.store.readRps + base.store.writeRps)
      - (withIt.store.readRps + withIt.store.writeRps);
    // Buyers a second the lease can carry, with and without.
    const buyersWith = withIt.contention.contentionBuyers;
    const buyersWithout = base.contention.contentionBuyers;
    const refusedWithout = Math.max(0, Math.min(peakBuyers, buyersWith) - Math.min(peakBuyers, buyersWithout));
    const movesWall = holdsGain > base.contention.contentionRps * 0.05;
    const dbWasBinding = base.store.over;
    const severity = movesWall ? 'decisive'
      : (dbSaved > 1 && dbWasBinding) ? 'relieves a real limit'
        : dbSaved > 1 ? 'marginal — relieves a limit nothing reaches'
          : 'no effect on anything that is failing';
    return {
      key: v.key,
      name: v.name.replace(/^[A-Z] · /, ''),
      inPackage: v.inPackage,
      buys: v.changes,
      severity,
      movesWall,
      holdsWith: withIt.contention.contentionRps,
      holdsWithout: base.contention.contentionRps,
      dbSaved,
      refusedWithout,
      // What declining it actually costs, in the terms of the run.
      cost: movesWall
        ? `Declining it leaves the wall at ${Math.round(base.contention.contentionRps).toLocaleString('en-GB')} requests a second. At this peak that is ${Math.round(refusedWithout).toLocaleString('en-GB')} buyers a second refused with seats still on sale — and no replica count, cache or pooler setting recovers any of it.`
        : dbSaved > 1
          ? `Declining it puts ${Math.round(dbSaved).toLocaleString('en-GB')} more statements a second back on the primary${dbWasBinding ? ', which is already at its ceiling' : ' — which is running at a fraction of its ceiling, so the cost is real but not currently binding'}. The lease ceiling does not move by one hold a second.`
          : `Declining it costs nothing measurable in this model, which is the finding rather than a gap: ${v.inPackage ? 'it relieves a limit nothing is reaching' : 'the README declines to build it for exactly this reason'}.`,
      // And what taking it costs, which is not always nothing.
      price: v.key === 'C'
        ? 'Sixteen sub-pools each empty separately, so the last seats fragment: fifteen empty and one holding four looks sold out to most buyers. Rebalancing is the hard part and the variant does not implement it — a throughput wall traded for a correctness one.'
        : v.key === 'D'
          ? 'Up to 50ms on the first write in a window. Invisible on a read path and not on a checkout.'
          : v.key === 'B'
            ? 'A cache that must be invalidated on nothing, because the snapshot cannot change. Almost free — and the only risk is somebody later caching getAvailability, which is how two people buy the same seat.'
            : v.key === 'R'
              ? 'A bigger Redis, and a read path that no longer touches the primary. Nothing treats a cache entry as truth, so the risk is cost rather than correctness.'
              : 'Nothing but the configuration change. It is raising a limit nothing reaches.',
    };
  });
}

/* ── presets ─────────────────────────────────────────────────────────────── */

const script = (...pairs) => pairs.map(([t, operation]) => ({ t, operation }));

export const PRESETS = [
  {
    key: 'free',
    name: 'Free run — you drive it',
    blurb: 'No calendar, no horizon, no script. You hold the arrival rate and press the operations yourself; it runs until you stop it.',
    cfg: { mode: 'free', freeBuyers: 0, venue: 'large', windowSec: 1200, autoDecommission: false },
    script: () => [],
  },
  {
    key: 'stadium',
    name: 'Stadium, sold out in twenty minutes',
    blurb: '60,000 seats at 95% buying, compressed into twenty minutes — the 6,270 RPS the technical doc derives, and the Bahrain shape.',
    cfg: { venue: 'large', windowSec: 1200, saleSec: 1200, rampSec: 120 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + c.graceSec + 150, 'reconcileBurstEnvironment']),
  },
  {
    key: 'twohour',
    name: 'The same stadium over two hours',
    blurb: 'Identical demand, spread across the two-hour window the document assumes. 1,045 RPS, and everything holds. The window is the whole variable.',
    cfg: { venue: 'large', windowSec: 7200, saleSec: 7200, rampSec: 600 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + 260, 'reconcileBurstEnvironment']),
  },
  {
    key: 'concert',
    name: 'Theme park, concert day',
    blurb: 'Saturday\u2019s 18,500 guests at 55% buying, over the three hours before the gates. The medium tier, and the one that sizes nothing.',
    cfg: { venue: 'medium', windowSec: 10800, saleSec: 5400, rampSec: 900 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + 240, 'reconcileBurstEnvironment']),
  },
  {
    key: 'late',
    name: 'Requested too late',
    blurb: 'Requested when the load appears rather than against the calendar. Provisioning takes minutes and the sale takes seconds.',
    cfg: { venue: 'large', windowSec: 1200, saleSec: 900, rampSec: 90, leadSec: 30 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + 640, 'reconcileBurstEnvironment']),
  },
  {
    key: 'capped',
    name: 'Sold out in ten minutes',
    blurb: 'The same seats in half the window: 12,540 RPS against ceilings the file sets at 20, 16 and 6. A second concurrent sale looks like this.',
    cfg: { venue: 'large', windowSec: 600, saleSec: 600, rampSec: 60 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + c.graceSec + 170, 'reconcileBurstEnvironment']),
  },
  {
    key: 'botched',
    name: 'Botched teardown',
    blurb: 'Decommission pressed the moment the sale closes. Refused \u2014 409, and the state model is why.',
    cfg: { venue: 'large', windowSec: 1200, saleSec: 1200, rampSec: 120 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + 20, 'decommissionBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + c.graceSec + 70, 'decommissionBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + c.graceSec + 160, 'reconcileBurstEnvironment']),
  },
  {
    key: 'forgotten',
    name: 'Forgotten environment',
    blurb: 'Reconciled, and nobody tore it down. A month of forgetting costs $8,587 \u2014 more than the platform it was protecting.',
    cfg: { venue: 'large', windowSec: 1200, saleSec: 1200, rampSec: 120, autoDecommission: false, forgottenHours: 720 },
    script: (c) => script([c.steadySec, 'requestBurstEnvironment'], [c.steadySec + c.leadSec + c.saleSec + c.graceSec + 150, 'reconcileBurstEnvironment']),
  },
];

/** A config with the venue arithmetic already applied. */
export function configure(patch = {}) {
  const cfg = { ...DEFAULTS, ...patch };
  cfg.peakRps = derivePeak(cfg).peak;
  return cfg;
}

export const money = (n) => (n >= 100
  ? `$${Math.round(n).toLocaleString('en-GB')}`
  : `$${n.toFixed(2)}`);

export const clock = (sec) => {
  const s = Math.max(0, Math.round(sec));
  const m = Math.floor(s / 60);
  return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
};
