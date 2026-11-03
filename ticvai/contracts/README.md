# Contracts — Status

Spec-first. Hand-authored here; servers and clients are generated. Never the reverse.

## Closed — v0.1, ready for Gate 1

| Contract | Ops | Capability | Settled by |
|---|---|---|---|
| `shared/common.yaml` | — | Money, ScopeRef, Problem, pagination, idempotency, consistency token | ADR-0008 |
| `shared/permissions.yaml` | — | **The permission vocabulary.** Single source for backend authz, frontend nav and AI scoping | permission-resolution spec |
| `spine/identity.yaml` | **38** | Staff auth, **guest-app auth (OTP, social, national ID)**, **SSO with group mapping**, **MFA and step-up**, **session administration**, principals, roles, grants, permission simulation | ADR-0002, 0003, 0004 |
| `spine/tenancy.yaml` | **15** | Scope hierarchy, region settings, workstation context, **sale boards**, **device registry with heartbeat** | ADR-0001, 0005 |
| `spine/finance.yaml` | **37** | Chart of accounts, ERP mapping, tax engine with compound tax, revenue recognition, deferred revenue, journals with approval, ledger, trial balance, price variance, settlement, fiscal periods, financial reporting | **12 Aug deep-dive · CF-38** |
| `spine/orders.yaml` | **31** | Orders, payments with inquiry recovery, refunds with venue policy, **modification, exchange, reschedule, ticket transfer with claim, order statement, B2B credit**, reservations, offline sync | **CF-36, CF-38, ADR-0013** |
| `spine/shift.yaml` | 10 | Shift lifecycle, blind close-out, cash lift, variance | C01 · 12 Aug §1, §19 |
| `spine/access.yaml` | **19** | Validation, override, lookup, offline sync, turnstile mode, cross-region rights, access points, admission profiles, blacklist, **group validation**, **geofencing** | C09 · ADR-0010 |
| `spine/cross-region.yaml` | **16** | Guest links, redemption delegation, wallet authorisation, DSAR fan-out | **ADR-0010, ADR-0014** |
| `spine/catalogue.yaml` | **45** | Products with **lifecycle and approval**, variants, pricing with **copy and uplift**, events, performances with **cancellation**, envelopes, channel allocations, signed bundles, inventory leases, **entitlement templates**, **alternative codes** | C20, C84, C85 · **ADR-0013** |

Every operation declares `x-ticvai-permission`, `x-ticvai-scope-level`,
`x-ticvai-offline-capable` and `x-ticvai-conflict-policy`. Redocly rejects any that does not.

## Satellite contracts

| Contract | Ops | Capability | Settled by |
|---|---|---|---|
| `satellite/subscription.yaml` | **28** | **Control Plane.** Tenant lifecycle, versioned plans, subscriptions with downgrade guards, **module licensing**, cell provisioning with jurisdiction enforcement, usage metering, billing | Domain 18 · C74, C75, C95, C96 |
| `satellite/white-label.yaml` | **41** | Brand, theme, Arabic/Latin fonts, navigation, homepage builder, banners, pages, FAQs, versioned policies, module enablement, preview, publish with version history and diff | C57, C105, C106 · UI/UX boards 1–2 |
| `satellite/maintenance.yaml` | **28** | Assets with operational linkage, work orders with timers and parts, planned maintenance by time or usage, inspections with safety-critical blocking, incidents with authority notification | Domain 15 · **10 Aug §5.3** |
| `satellite/marketing-crm.yaml` | **40** | Guest profiles, **append-only consent**, suppression, segments as definitions, campaigns with send-time consent checks, templates, service cases with SLA, loyalty, reviews | Domain 20 · 319 reqs · **gates AI-66** |
| `satellite/inventory.yaml` | **34** | Items, stock positions, movement ledger, blind counts, two-phase transfers, requisitions, quotation comparison, purchase orders, goods receipt | Domain 13 · **10 Aug §5.4** |
| `satellite/promotions.yaml` | **27** | Promotions with declared stacking, coupon campaigns and codes, vouchers, bundles, **allocation splits**, upsell rules, evaluation with reasons | Domain 4 · **12 Aug §16** |
| `satellite/fnb.yaml` | **30** | Menus, modifiers, quick + table service, visits, bill splitting, kitchen ticket handoff, recipes, waste | Domains 4 & 7 · 03 Aug §§4–5 · 31 Jul §11 |
| `satellite/games.yaml` | **13** | Game cards with separate credit and point balances, plays with offline sync, prize redemption depleting retail stock | Domain 9 · 25 reqs |
| `satellite/assets.yaml` | **10** | Media library, signed direct upload, collections, usage tracking, **rights and licence expiry** | Domain 21 · 15 reqs |
| `satellite/queue.yaml` | **20** | Queues bound to assets, entries with return windows, offline redemption, wait times carrying provenance, **vendor-agnostic inbound feed**, signage boards | Domain 5 · **ADR-0012** |
| `satellite/reporting.yaml` | **23** | Versioned definitions, execution against the reporting replica, schedules under owner permissions, audited exports, dashboards, **natural-language query returning its generated query** | Cross-cutting · AI-57 |
| `satellite/retail.yaml` | **23** | Merchandise, price and stock check, sales depleting the inventory ledger, returns with condition, exchanges, guest-app wallet, gift cards, collection reservations | Domain 6 |
| `satellite/seating.yaml` | **29** | Seat maps, manifest + plan import, categories, availability, holds, blocks, seating rules, recommendations | Domain 19 — 112 reqs |
| `satellite/transport.yaml` | **28** | **Scheduled transport ticketing.** Stations, routes with ordered stops and offsets, timetables releasing departures (each a catalogue performance), fare tables by passenger type, fare quotes, multi-trip and unlimited passes (catalogue `openDated` products), guest favourite routes, route map. Served by VenueOpsService. Real network, fares and timetable are an open value from the client | Decided 29 September, rev 3 REV3-21 |

## Authentication model

Four schemes, defined in `shared/common.yaml`:

| Scheme | Used by |
|---|---|
| `bearerAuth` | Staff sessions. Carries `sid`, validated against the session registry |
| `guestAuth` | Guest sessions. No workstation, no role selection, no single-session rule |
| `serviceAuth` | **Cell-to-cell and cell-to-Control-Plane.** mTLS plus a cell-identity token — the token says which cell, the certificate proves it |
| `apiKeyAuth` | Partner and developer. Deferred pending the Developer & API workshop. Also a device key (ADAM CR-451) |
| `deviceAuth` | **A registered device as itself** (CHG-R8SPN-030). The device doors (till, handheld, scanner) sign in and take the till's session-less step-up with it, and the workstation is the device's, never one the body names (r13 system review C-04, CHG-R14H-001) |

**Every token is bound to the host's tenant** (r13 system review C-05, CHG-R14H-002): a cell signs every tenant's tokens
with one key, so a token whose `tenant` (or whose `sid`'s registry entry) is not the tenant the request's host resolves to
is `401` before anything is read (`docs/architecture/specs/permission-resolution.md` section 7).

**Access markers added 3 November 2026** (r13 system review C-03, C-04, C-13; the lead: "All four, one release"):

- `x-ticvai-object-owner: [subject | share | delegation | session | token]` — on every operation a guest can call that
  is addressed by a per-object path id (not a published one: a venue, product, event, performance, map and the like),
  unless it is `x-ticvai-self-scoped`. Who, among guest callers, the object answers to: `subject` the guest whose record
  it is; `share` a guest it is shared with (an entitlement share not revoked); `delegation` a guest holding an active
  delegation over the subject that grants the operation's permission (`grantDelegation`'s guest-delegable list);
  `session` the guest session, anonymous included, that created it (a hold, a visit plan); `token` whoever holds the
  object's own unguessable id or token (an anonymous waiting-room entry). **Any other guest gets the shared `404`,
  exactly as for an id that does not exist**, as `x-ticvai-self-scoped` (CHG-GCF-002); staff are decided by the
  permission as before. `x-ticvai-guest-callable` (a guest may call it within their own session, needing no
  permission) does not say whose object it is: `check-contract-shapes` C-GUEST-OWNER fails an operation that leaves
  the owner unsaid, and C-SELF-404 an owned one without the `404`.
- `x-ticvai-workstation-from: device` — the operation's workstation is the one its `deviceAuth` device is bound to;
  a `workstationId` the request sends must equal it (`403 workstation-mismatch`), and one sent without `deviceAuth` is
  `401 device-unauthenticated` (`check-doors` D-DEVICE-DOOR).
- `x-ticvai-device-kinds: [<DeviceKind> ... | all]` — the device kinds whose credential (`deviceAuth`, or a device
  key on `apiKeyAuth`) the operation accepts; any other kind is `403 device-kind-not-allowed` (`check-doors`
  D-DEVICE-KINDS). A device that moves stored value authenticates by `deviceAuth`, never a device key (D-DEVICE-MONEY).
- `x-ticvai-secret: bearer` on a path or header parameter — the value is a credential (a payment-link or invitation
  token, a gift or game card code, a supervisor PIN): logs, traces and the edge record the route template and never
  the value (`docs/architecture/observability.md`, "Credentials in requests"; `check-contract-shapes` C-SECRET-PARAM).

Operations without a permission fall into three groups, each marked explicitly:

- `x-ticvai-auth: service` — 11 cell-to-cell operations
- `x-ticvai-self-scoped: principal \| subject` — 15 operations acting only on the caller's own resources. Supplying another identifier is never silently honoured: **a guest naming another guest's record gets 404, exactly as for a record that does not exist** (Pattern 4; Chinmay, 3 October 2026, CHG-GCF-002), so nothing reveals that the id exists; 403 is only for a staff caller without the permission (R8 blocker cause ORDERS-MONEY-C01, CHG-R8SPN-018)
- `security: []` — genuinely public: login, OTP request, SSO discovery, maintenance status

### Callers with no workstation: the guest and partner variants

A `x-ticvai-scope-level: workstation` operation is called from a session that signed a workstation in (R100). Two
markers say that the same operation also has a variant for a caller that signs none in; `check-screen-wiring`
S-WORKSTATION-OP accepts a workstation operation on such a platform only through them:

- `x-ticvai-guest-callable: true` — a guest (guestAuth) on the guest web, app or kiosk (P01, P02, P05), acting only
  for themselves in their own session; no permission (CHG-GCF-003, CHG-SCR-012).
- `x-ticvai-partner-callable: true` — a partner user (bearerAuth, no workstation; CHG-DOOR-001) on the partner portal
  (P10) (the lead, 3 November 2026; CHG-R14BO-005). **Who:** the operation's `x-ticvai-audience` includes `partner`.
  **Checked against:** the operation's own `x-ticvai-permission`, which the partner user must hold, at the session's
  venue grant, the venue of the record acted on, instead of a workstation (as partner carts and orders are written,
  ADAM CR-184). **How it answers:** only on records of the partner's own channel (`Order.channelProfileId` the
  session's); another channel's record is 404, exactly as one that does not exist (Pattern 4), and a partner user
  without the permission is 403. The operation's description carries the paragraph that says this and names the
  marker. The checker takes the marker only when all of that holds (audience, permission, the paragraph) and only on
  P10; an unmarked workstation operation on the partner portal is still a finding. On createPayment and
  inquirePaymentStatus.
## Personal data (3 November 2026, ADR-0023 as amended; CHG-R14M-001)

| Mark | Where | Means |
|---|---|---|
| `x-ticvai-data-class: personal` | a property | A natural person's data. Every property named as a person's identifier carries a class (`business` for an organisation's) |
| `x-ticvai-pii: {store, subject}` | a property of a persisted schema | Kept in `pii.*` (the store, `tools/personal_data.py`) for the subject the named property holds; no column on the module's row. Written through identity `recordSubjectDetails`, read through `identity#subjectDetails` |
| `x-ticvai-subject-kind` | the subject property | The kind of the `pii.subject` a row with none gets: guest, employee, contact, applicant |
| `x-ticvai-personal-data: gated` | an operation | Each personal field in the answer is answered only to a caller holding `GUEST_VIEW_PII` at the row's scope, null to anyone else (a guest's own record included) |
| `x-ticvai-personal-data: self` | an operation | Answers only the caller's own record |

`tools/check-personal-data.py` holds them.

## Amended 13 Aug — decisions landed

| Contract | Change |
|---|---|
| `tenancy.yaml` | `DeploymentProfile` (terminalLocal / venueEdge / thin) and `CatalogueState` on Workstation — ADR-0013. Cell = Tenant × Region — ADR-0014. `ScopeLevel` confirmed binding — ADR-0011 |
| `access.yaml` | `delegatedRights` in the offline package · `issuingCellId` and `guestLinkId` on TicketStatus · two new deny reasons — ADR-0010 |
| `shift.yaml` | `releaseHeldLeases` on close · `heldLeaseCount` on Shift — ADR-0013 |
| `identity.yaml` | `cellName` and `deploymentProfile` on WorkstationContext |

## Deferred — and why

| Contract | Blocked on |
|---|---|
| **Order create/modify** | Depends on catalogue and entitlement issuance. **CF-31** — do entitlements cross jurisdictions? — changes the issuance shape |
| **Refund** | Open question: does `ORDER_REFUND_APPROVE` carry a monetary threshold on the grant, or is the threshold separate role configuration? 2.12.3 implies a value; the grant model has none. See NOTE-1 in `permissions.yaml` |
| Catalogue remainder | Product lifecycle (C79), ticket resale marketplace (C80 — no MoM coverage), portfolio management (C81), alternative codes. ~19 ops |
| **FX-dependent finance** | **CF-37.** ~12 ops: cross-currency allocation splits, inter-company settlement, FX revaluation at period close, consolidated multi-currency reporting |
| **Virtual queue** | **CF-33** — Q1 vs Q2 ownership unresolved |
| **AI capabilities** | **CF-20** — residency ruling |
| Seating, F&B, retail, inventory, CRM | Wave 2+. Not through the context loop |

## Provisional

`ScopeLevel` in `tenancy.yaml` is provisional pending **CF-34** — the hierarchy diagram is
illustrative, not binding. Paths are variable-length `ltree`, so depth changes are absorbed
without redesign; the enum is what would change.

## Gates

**Gate 1 — contract review.** Three questions: can the frontend build every page against
it? Can the backend implement it without a missing field? Does every operation declare all
four extensions?

**Gate 2 — mock-proven.** One flow end to end against Prism with zero backend code. After
Gate 2 the contract is frozen for the context.

## Commands

    make lint       # Redocly
    make bundle     # resolve $refs into dist/
    make diff       # oasdiff breaking-change gate
    make mock       # Prism on :4010
    make generate   # .NET, TypeScript and Python clients
