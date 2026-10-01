# P09-overview-health-01 — P09 · Overview & Health

**5 screens · 25 operations · 38 schemas · 10 permissions**

Platform P09 TICVAI Web · ships as **ticvai-control** ·
platformAdmin audience · web ·
online only

## Who this is for

**platformAdmin on web.** Everything below is how you know what is
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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 10 permissions apply here:
  `AI_AUDIT_VIEW, ORDER_VIEW, PLATFORM_CELL_MANAGE, PLATFORM_CELL_VIEW, PLATFORM_RELEASE_PROMOTE, PLATFORM_RELEASE_VIEW, PLATFORM_TENANT_VIEW, REGION_CONFIGURE, TICKET_LOOKUP, USER_MANAGE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ADM-002` | Platform Dashboard | listDetail | 6 | 0 | — |
| `ADM-003` | Cross-Tenant Health Dashboard | listDetail | 12 | 5 | — |
| `ADM-004` | Platform Audit Log | listDetail | 2 | 0 | — |
| `ADM-013` | Tenant Performance Monitor | listDetail | 7 | 3 | — |
| `ADM-029` | Deployment Monitor | listDetail | 12 | 6 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ADM-002",
  "name": "Platform Dashboard",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 1,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-dashboard",
   "component": "apps/ticvai-web/src/routes/general/PlatformDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "ADM-001",
    "ADM-003",
    "ADM-004",
    "ADM-005",
    "ADM-006",
    "ADM-007",
    "ADM-008",
    "ADM-009",
    "ADM-010",
    "ADM-011",
    "ADM-012",
    "ADM-013",
    "ADM-014",
    "ADM-015",
    "ADM-016",
    "ADM-017",
    "ADM-018",
    "ADM-019",
    "ADM-020",
    "ADM-021",
    "ADM-022",
    "ADM-023",
    "ADM-024",
    "ADM-025",
    "ADM-026",
    "ADM-027",
    "ADM-028",
    "ADM-029",
    "ADM-030",
    "ADM-031",
    "ADM-032",
    "ADM-033",
    "ADM-034",
    "ADM-035",
    "ADM-036",
    "ADM-037",
    "ADM-038",
    "ADM-048",
    "ADM-058",
    "ADM-068",
    "ADM-078",
    "ADM-088",
    "ADM-098",
    "ADM-108",
    "ADM-118",
    "ADM-128",
    "ADM-138",
    "ADM-148",
    "ADM-158",
    "ADM-168",
    "ADM-178",
    "ADM-188",
    "ADM-198",
    "ADM-208",
    "ADM-218",
    "ADM-228",
    "ADM-238",
    "ADM-248",
    "ADM-258",
    "ADM-268",
    "ADM-278",
    "ADM-288",
    "ADM-298",
    "ADM-308",
    "ADM-318",
    "ADM-319",
    "ADM-329",
    "ADM-339",
    "ADM-349",
    "ADM-359",
    "ADM-369",
    "ADM-379",
    "ADM-389",
    "ADM-399",
    "ADM-409",
    "ADM-419",
    "ADM-449",
    "ADM-459",
    "ADM-469",
    "ADM-479",
    "ADM-489",
    "ADM-499",
    "ADM-509",
    "ADM-519",
    "ADM-529",
    "ADM-539",
    "ADM-549",
    "ADM-559",
    "ADM-569",
    "ADM-579",
    "ADM-589",
    "ADM-599",
    "ADM-609",
    "ADM-619",
    "ADM-629",
    "ADM-639",
    "ADM-649",
    "ADM-659",
    "ADM-669",
    "ADM-679",
    "ADM-689"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "ADM-319",
     "trigger": "Approval Workflow Library",
     "provenance": "structural — pack board 2 wiring, 9 September 2026"
    },
    {
     "to": "ADM-329",
     "trigger": "Approval Matrix Command Center",
     "provenance": "structural — pack board 3 wiring, 9 September 2026"
    },
    {
     "to": "ADM-339",
     "trigger": "Governance & Compliance Command Center",
     "provenance": "structural — pack board 6 wiring, 9 September 2026"
    },
    {
     "to": "ADM-349",
     "trigger": "Approval Integration Command Center",
     "provenance": "structural — pack board 7 wiring, 9 September 2026"
    },
    {
     "to": "ADM-359",
     "trigger": "Approval Executive KPI Dashboard",
     "provenance": "structural — pack board 8 wiring, 9 September 2026"
    },
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "cellId"
     ]
    },
    {
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-005",
     "trigger": "Tenant Directory",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "tenantId"
     ]
    },
    {
     "to": "ADM-006",
     "trigger": "Tenant Hierarchy Explorer",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "tenantId"
     ]
    },
    {
     "to": "ADM-007",
     "trigger": "Module & Feature Entitlement",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "tenantId"
     ]
    },
    {
     "to": "ADM-008",
     "trigger": "Subscription & Plan Management",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "planId",
      "tenantId"
     ]
    },
    {
     "to": "ADM-012",
     "trigger": "Tenant Isolation & Resource Pool",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher",
     "carries": [
      "cellId",
      "tenantId"
     ]
    },
    {
     "to": "ADM-020",
     "trigger": "Creates the first principal and grants it the role",
     "provenance": "flow F109 step 4→5",
     "operation": "listTenants"
    },
    {
     "to": "ADM-021",
     "trigger": "Defines the role the first administrator will hold",
     "provenance": "flow F109 step 2→3"
    },
    {
     "to": "ADM-369",
     "trigger": "Commercial Command Center",
     "provenance": "structural — pack board 1 wiring, 11 September 2026"
    },
    {
     "to": "ADM-459",
     "trigger": "Billing & Commercial Command Center",
     "provenance": "structural — pack board 10 wiring, 11 September 2026"
    },
    {
     "to": "ADM-379",
     "trigger": "Welcome & Start Your TICVAI Journey",
     "provenance": "structural — pack board 2 wiring, 11 September 2026"
    },
    {
     "to": "ADM-389",
     "trigger": "Commercial Rules Engine Overview",
     "provenance": "structural — pack board 3 wiring, 11 September 2026"
    },
    {
     "to": "ADM-399",
     "trigger": "Recommended Package Overview",
     "provenance": "structural — pack board 4 wiring, 11 September 2026"
    },
    {
     "to": "ADM-409",
     "trigger": "Purchase / Trial Journey Selection",
     "provenance": "structural — pack board 5 wiring, 11 September 2026"
    },
    {
     "to": "ADM-419",
     "trigger": "Provisioning Command Center",
     "provenance": "structural — pack board 6 wiring, 11 September 2026"
    },
    {
     "to": "ADM-449",
     "trigger": "Usage & License Command Center",
     "provenance": "structural — pack board 9 wiring, 11 September 2026"
    },
    {
     "to": "ADM-469",
     "trigger": "AI Configuration Home & Start",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-479",
     "trigger": "AI Configuration Build Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-489",
     "trigger": "AI Configuration Readiness Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-499",
     "trigger": "Forecasting Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-509",
     "trigger": "Operational Forecasting Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-519",
     "trigger": "AI Governance Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-529",
     "trigger": "AI Human Oversight Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-539",
     "trigger": "AI Explainability & Audit Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-549",
     "trigger": "AI Governance Monitoring Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-559",
     "trigger": "Payment Command Center\\t7",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-569",
     "trigger": "Payment Orchestration Command Center\\t27",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-579",
     "trigger": "Terminal & Card-Present Command Center\\t48",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-589",
     "trigger": "Digital Payments Command Center\\t71",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-599",
     "trigger": "Mixed Tender & Credit Command Center\\t93",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-609",
     "trigger": "Refund & Payment Adjustment Command Center\\t116",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-619",
     "trigger": "Reconciliation & Settlement Command Center\\t139",
     "provenance": "structural — pack board 7 wiring, 19 September 2026"
    },
    {
     "to": "ADM-629",
     "trigger": "Payment Risk & Fraud Command Center\\t166",
     "provenance": "structural — pack board 8 wiring, 19 September 2026"
    },
    {
     "to": "ADM-639",
     "trigger": "Recommendation Command Center",
     "provenance": "structural — pack board 1 wiring, 19 September 2026"
    },
    {
     "to": "ADM-649",
     "trigger": "Upsell & Upgrade Command Center",
     "provenance": "structural — pack board 2 wiring, 19 September 2026"
    },
    {
     "to": "ADM-659",
     "trigger": "Cross-Sell Command Center",
     "provenance": "structural — pack board 3 wiring, 19 September 2026"
    },
    {
     "to": "ADM-669",
     "trigger": "Journey & Context Command Center",
     "provenance": "structural — pack board 4 wiring, 19 September 2026"
    },
    {
     "to": "ADM-679",
     "trigger": "Personalization & NBO Command Center",
     "provenance": "structural — pack board 5 wiring, 19 September 2026"
    },
    {
     "to": "ADM-689",
     "trigger": "Recommendation Performance Command Center",
     "provenance": "structural — pack board 6 wiring, 19 September 2026"
    },
    {
     "to": "ADM-009",
     "trigger": "Tenant Billing & Invoicing",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-009 declares entryState.params tenantId and ADM-002 holds tenantId, so an edge into it carries them"
    },
    {
     "to": "ADM-010",
     "trigger": "Usage Metering",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-010 declares entryState.params tenantId and ADM-002 holds tenantId, so an edge into it carries them"
    },
    {
     "to": "ADM-011",
     "trigger": "Licence & Seat Management",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-011 declares entryState.params tenantId and ADM-002 holds tenantId, so an edge into it carries them"
    },
    {
     "to": "ADM-013",
     "trigger": "Tenant Performance Monitor",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-013 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-014",
     "trigger": "Auto-Scaling Configuration",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-014 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-015",
     "trigger": "API Rate Limit & Quota Management",
     "carries": [
      "tenantId"
     ],
     "provenance": "derived — ADM-015 declares entryState.params requestId, tenantId and ADM-002 holds tenantId, so an edge into it carries them"
    },
    {
     "to": "ADM-016",
     "trigger": "White-Label Branding Management",
     "provenance": "derived — ADM-016 declares entryState.params bannerId, pageId, policyKind, version and ADM-002 holds none of them. The edge carries nothing: bannerId, pageId, policyKind, version only pre-select (deep link or optional), and ADM-016 opens on its own"
    },
    {
     "to": "ADM-017",
     "trigger": "Domain & Certificate Management",
     "provenance": "derived — ADM-017 declares entryState.params bannerId, domainId, pageId, policyKind, version and ADM-002 holds none of them. The edge carries nothing: bannerId, pageId, policyKind, version, domainId only pre-select (deep link or optional), and ADM-017 opens on its own"
    },
    {
     "to": "ADM-018",
     "trigger": "Localisation & Language Pack",
     "provenance": "derived — ADM-018 declares entryState.params bannerId, pageId, policyKind, version and ADM-002 holds none of them. The edge carries nothing: bannerId, pageId, policyKind, version only pre-select (deep link or optional), and ADM-018 opens on its own"
    },
    {
     "to": "ADM-019",
     "trigger": "Global Configuration & Defaults",
     "carries": [
      "planId"
     ],
     "provenance": "derived — ADM-019 declares entryState.params planId and ADM-002 holds planId, so an edge into it carries them"
    },
    {
     "to": "ADM-022",
     "trigger": "Release & Version Management",
     "provenance": "derived — ADM-022 declares entryState.params releaseId and ADM-002 holds none of them. The edge carries nothing: releaseId only pre-selects (deep link or optional), and ADM-022 opens on its own"
    },
    {
     "to": "ADM-023",
     "trigger": "Staging Promotion & Approval",
     "provenance": "derived — ADM-023 declares entryState.params releaseId and ADM-002 holds none of them. The edge carries nothing: releaseId only pre-selects (deep link or optional), and ADM-023 opens on its own"
    },
    {
     "to": "ADM-026",
     "trigger": "End-of-Support Notice Management",
     "provenance": "derived — ADM-026 declares entryState.params version and ADM-002 holds none of them. The edge carries nothing: ADM-026 finds version (listSupportNotices) itself, and ADM-026 opens on its own"
    },
    {
     "to": "ADM-027",
     "trigger": "Database Migration Console",
     "provenance": "derived — ADM-027 declares entryState.params runId and ADM-002 holds none of them. The edge carries nothing: runId only pre-selects (deep link or optional), and ADM-027 opens on its own"
    },
    {
     "to": "ADM-029",
     "trigger": "Deployment Monitor",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-029 declares entryState.params cellId, rolloutId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-030",
     "trigger": "Infrastructure Sizing & Scaling Policy",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-030 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-031",
     "trigger": "Security & Compliance Dashboard",
     "provenance": "derived — ADM-031 declares entryState.params dashboardId and ADM-002 holds none of them. The edge carries nothing: dashboardId only pre-selects (deep link or optional), and ADM-031 opens on its own"
    },
    {
     "to": "ADM-032",
     "trigger": "WAF & Security Policy View",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-032 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-033",
     "trigger": "Backup & DR Status",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-033 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-034",
     "trigger": "Archival Job Monitor",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-034 declares entryState.params cellId and ADM-002 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-037",
     "trigger": "AI Provider & Credentials",
     "carries": [
      "regionId"
     ],
     "provenance": "derived — ADM-037 declares entryState.params modelId, providerId, regionId, templateKey and ADM-002 holds regionId, so an edge into it carries them"
    },
    {
     "to": "ADM-138",
     "trigger": "Promotion Command Center Dashboard",
     "provenance": "derived — ADM-138 declares entryState.params promotionId and ADM-002 holds none of them. The edge carries nothing: ADM-138 finds promotionId (listPromotions) itself, and ADM-138 opens on its own"
    },
    {
     "to": "ADM-158",
     "trigger": "Coupon & Promo Code Command Center",
     "provenance": "derived — ADM-158 declares entryState.params campaignId and ADM-002 holds none of them, so the edge carries nothing and ADM-158 opens cold"
    },
    {
     "to": "ADM-318",
     "trigger": "Dead Letters",
     "provenance": "derived — ADM-318 declares entryState.params deadLetterId and ADM-002 holds none of them. The edge carries nothing: deadLetterId only pre-selects (deep link or optional), and ADM-318 opens on its own"
    },
    {
     "to": "ADM-024",
     "trigger": "Release Notification Composer",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-025",
     "trigger": "Tenant Upgrade Scheduler",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-028",
     "trigger": "Environment Registry",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-035",
     "trigger": "Support & Escalation Console",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-036",
     "trigger": "Platform Notification Broadcast",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-038",
     "trigger": "Communication Service Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-048",
     "trigger": "Commercial Pricing Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-058",
     "trigger": "Pricing Rule Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-068",
     "trigger": "Tax, Fee & Calculation Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-078",
     "trigger": "Pricing Governance Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-088",
     "trigger": "Dynamic Pricing Strategy Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-098",
     "trigger": "AI Pricing Intelligence Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-108",
     "trigger": "Revenue Optimization Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-118",
     "trigger": "Product Lifecycle Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-128",
     "trigger": "Product Governance Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-148",
     "trigger": "Promotion Rule Builder",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-168",
     "trigger": "Advanced Offer Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-178",
     "trigger": "Bundle & Combo Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-188",
     "trigger": "Dynamic Bundle Operations Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-198",
     "trigger": "Targeting & Eligibility Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-208",
     "trigger": "Stacking & Conflict Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-218",
     "trigger": "Campaign Governance & Budget Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-228",
     "trigger": "Promotion Performance Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-238",
     "trigger": "Rules & Workflow Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-248",
     "trigger": "Workflow Operations Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-258",
     "trigger": "Sales Channel Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-268",
     "trigger": "Channel Operations Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-278",
     "trigger": "Resale Marketplace Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-288",
     "trigger": "Resale Operations Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-298",
     "trigger": "My Tickets & Resale Marketplace Entry",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    },
    {
     "to": "ADM-308",
     "trigger": "Upgrade & Conversion Command Center",
     "provenance": "structural — ADM-002 is P09's home screen and its exits are its launcher"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Removed 24 August**: generateInvoice, getSubscription, getUsageMetering, listSubscriptionInvoices, previewSubscriptionChange, setSubscription. **Eleven P09 screens carried the same nine subscription operations** — a platform dashboard, a tenant directory and a rate-limit console all able to preview a subscription change. **Bulk-attach residue at platform scale**, and each screen now keeps only what it is for. **Removed 24 August**: addLicenceAddOn, createTenant, provisionCell, reactivateTenant, removeLicenceAddOn, setSsoConfig, suspendTenant, terminateTenant, updateTenant. **`ADM-015 API Rate Limit & Quota Management` could create and terminate tenants.** The 18 August bulk attach reached the platform console too — provisioning, licensing and SSO were on every screen that mentioned a tenant. **Drawn 26 August** — `Dashboards Board` frame `adm-002`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#adm-002"
  ],
  "pattern": "listDetail",
  "patternReason": "`listTenants` reads the population and `getEntitlementUsage` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Status",
       "operation": "listTenants",
       "notes": "Sends `?status=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "textField",
       "label": "Plan id",
       "operation": "listTenants",
       "notes": "Sends `?planId=` to `listTenants`.",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "dataTable",
       "label": "Every tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.suspensionMode",
        "Tenant.suspensionReason",
        "Tenant.planId",
        "Tenant.planName",
        "Tenant.cellCount",
        "Tenant.venueCount",
        "Tenant.billingEmail",
        "Tenant.accountManagerPrincipalId"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "dataTable",
       "label": "Every cell",
       "bindsTo": "Cell",
       "columns": [
        "Cell.id",
        "Cell.name",
        "Cell.kind",
        "Cell.clusterId",
        "Cell.isReachable",
        "Cell.lastContactAt",
        "Cell.licenceExpiresAt",
        "Cell.participatesInCrossCell",
        "Cell.regionId",
        "Cell.regionName",
        "Cell.countryCode",
        "Cell.tier"
       ],
       "operation": "listTenantCells",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/cells"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected tenant",
       "bindsTo": "Tenant",
       "columns": [
        "Tenant.id",
        "Tenant.code",
        "Tenant.name",
        "Tenant.status",
        "Tenant.suspensionMode",
        "Tenant.suspensionReason",
        "Tenant.suspensionEffectiveAt",
        "Tenant.suspensionNoticeMessage",
        "Tenant.terminationScheduledAt",
        "Tenant.terminationRetentionUntil",
        "Tenant.terminationReason",
        "Tenant.terminationRequestedByPrincipalId",
        "Tenant.planId",
        "Tenant.planName",
        "Tenant.cellCount",
        "Tenant.venueCount"
       ],
       "operation": "listTenants",
       "provenance": "contract subscription.yaml GET /tenants"
      },
      {
       "kind": "detailPanel",
       "label": "The SSO provider config",
       "bindsTo": "SsoProviderConfig",
       "columns": [
        "SsoProviderConfig.id",
        "SsoProviderConfig.displayName",
        "SsoProviderConfig.protocol",
        "SsoProviderConfig.metadataUrl",
        "SsoProviderConfig.issuer",
        "SsoProviderConfig.clientId",
        "SsoProviderConfig.clientSecretRef",
        "SsoProviderConfig.groupMappings",
        "SsoProviderConfig.autoProvisionPrincipals",
        "SsoProviderConfig.isEnforced",
        "SsoProviderConfig.isActive"
       ],
       "operation": "getSsoConfig",
       "provenance": "contract identity.yaml GET /tenants/sso-config"
      },
      {
       "kind": "detailPanel",
       "label": "The tenant",
       "bindsTo": "TenantDetail",
       "columns": [
        "TenantDetail.id",
        "TenantDetail.code",
        "TenantDetail.name",
        "TenantDetail.status",
        "TenantDetail.suspensionMode",
        "TenantDetail.suspensionReason",
        "TenantDetail.suspensionEffectiveAt",
        "TenantDetail.suspensionNoticeMessage",
        "TenantDetail.terminationScheduledAt",
        "TenantDetail.terminationRetentionUntil",
        "TenantDetail.terminationReason",
        "TenantDetail.terminationRequestedByPrincipalId",
        "TenantDetail.planId",
        "TenantDetail.planName",
        "TenantDetail.cellCount",
        "TenantDetail.venueCount"
       ],
       "operation": "getTenant",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}"
      },
      {
       "kind": "detailPanel",
       "label": "The licence position",
       "bindsTo": "LicencePosition",
       "columns": [
        "LicencePosition.planId",
        "LicencePosition.licensedModules",
        "LicencePosition.limits"
       ],
       "operation": "getTenantLicences",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/licences"
      },
      {
       "kind": "detailPanel",
       "label": "The entitlement usage",
       "bindsTo": "EntitlementUsage",
       "columns": [
        "EntitlementUsage.metrics",
        "EntitlementUsage.asAt"
       ],
       "operation": "getEntitlementUsage",
       "provenance": "contract subscription.yaml GET /tenants/{tenantId}/entitlement-usage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform list.",
   "error": "Could not load. Names which read failed and leaves the platform untouched.",
   "emptyFirstRun": "No platform yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on status, planId and the platform are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_TENANT_VIEW`, which `listTenants` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listTenants",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "getEntitlementUsage",
    "contract": "subscription",
    "purpose": "Usage against licensed limits",
    "trigger": "onLoad"
   },
   {
    "operationId": "getSsoConfig",
    "contract": "identity",
    "purpose": "Read SSO configuration",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenant",
    "contract": "subscription",
    "purpose": "Read a tenant with cells and subscription",
    "trigger": "onLoad"
   },
   {
    "operationId": "getTenantLicences",
    "contract": "subscription",
    "purpose": "What a tenant is licensed to use",
    "trigger": "onLoad"
   },
   {
    "operationId": "listTenantCells",
    "contract": "subscription",
    "purpose": "List a tenant's cells",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "tenantId",
     "from": "session"
    }
   ],
   "coldEntry": "Resolves from the session; a cold arrival is the ordinary case.",
   "preloaded": [
    "Tenant.id",
    "Tenant.code",
    "Tenant.name",
    "Tenant.status",
    "Tenant.suspensionMode"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-002",
   "derivedFrom": "wireframes/reference/Dashboards Board.dc.html",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 6 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-003",
  "name": "Cross-Tenant Health Dashboard",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C95",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/cross-tenant-health-dashboard",
   "component": "apps/ticvai-web/src/routes/general/CrossTenantHealthDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-004"
   ],
   "fromFlows": true,
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-003 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-003 holds none of them. The edge carries nothing: ADM-003 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-004",
     "trigger": "Platform Audit Log",
     "provenance": "derived — ADM-004 declares entryState.params decisionRecordId and ADM-003 holds none of them. The edge carries nothing: ADM-004 finds decisionRecordId (listAiInteractions) itself, and ADM-004 opens on its own"
    },
    {
     "to": "SCN-003",
     "trigger": "Guest scans at the other venue",
     "provenance": "flow F19 step 2→3",
     "crossesDevice": true,
     "back": false,
     "carries": [
      "rightId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Cross-platform navigation removed 24 August**: SCN-003. **A till does not navigate to a back office and a guest app does not navigate to either** — those are device handovers, and a flow declares them with `crossesDevice` rather than a screen pretending there is a link. **Drawn 26 August** — `Dashboards Board` frame `adm-003`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.",
  "density": "compact",
  "boardFrames": [
   "Dashboards Board.dc.html#adm-003"
  ],
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "The screen this app sits on. Everything else is entered from here and returns to it.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "detailPanel",
       "label": "The cell",
       "bindsTo": "CellDetail",
       "columns": [
        "CellDetail.id",
        "CellDetail.name",
        "CellDetail.kind",
        "CellDetail.clusterId",
        "CellDetail.isReachable",
        "CellDetail.lastContactAt",
        "CellDetail.licenceExpiresAt",
        "CellDetail.participatesInCrossCell",
        "CellDetail.regionId",
        "CellDetail.regionName",
        "CellDetail.countryCode",
        "CellDetail.tier",
        "CellDetail.status",
        "CellDetail.cloudProvider",
        "CellDetail.cloudRegion",
        "CellDetail.apiEndpoint"
       ],
       "operation": "getCell",
       "provenance": "contract subscription.yaml GET /cells/{cellId}"
      },
      {
       "kind": "detailPanel",
       "label": "The cell capacity",
       "bindsTo": "CellCapacity",
       "columns": [
        "CellCapacity.kind",
        "CellCapacity.tenantCount",
        "CellCapacity.isConstrained",
        "CellCapacity.constrainedDimension",
        "CellCapacity.dimensions",
        "CellCapacity.forecastBreachAt",
        "CellCapacity.measuredAt"
       ],
       "operation": "getCellCapacity",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/capacity"
      },
      {
       "kind": "detailPanel",
       "label": "The cross region entitlement",
       "bindsTo": "CrossRegionEntitlement",
       "columns": [
        "CrossRegionEntitlement.id",
        "CrossRegionEntitlement.rightId",
        "CrossRegionEntitlement.ticketId",
        "CrossRegionEntitlement.guestLinkId",
        "CrossRegionEntitlement.issuingCellName",
        "CrossRegionEntitlement.consumingCellName",
        "CrossRegionEntitlement.mediaCodes",
        "CrossRegionEntitlement.validFrom",
        "CrossRegionEntitlement.validTo",
        "CrossRegionEntitlement.admissionRulesId",
        "CrossRegionEntitlement.venueId",
        "CrossRegionEntitlement.entriesAllowed",
        "CrossRegionEntitlement.entriesConsumed",
        "CrossRegionEntitlement.status",
        "CrossRegionEntitlement.lastConsumedAt",
        "CrossRegionEntitlement.lastReconciledAt"
       ],
       "operation": "getCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml GET /cross-region-entitlements/{rightId}"
      },
      {
       "kind": "detailPanel",
       "label": "The cell health",
       "bindsTo": "CellHealth",
       "columns": [
        "CellHealth.isHealthy",
        "CellHealth.isSchemaBehind",
        "CellHealth.databaseStatus",
        "CellHealth.replicationLagSeconds",
        "CellHealth.lastBackupAt",
        "CellHealth.lastRestoreDrillAt",
        "CellHealth.checkedAt"
       ],
       "operation": "getCellHealth",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/health"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel decommission",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission cell",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Save cell tier",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      },
      {
       "kind": "secondaryButton",
       "label": "Propagate cross region entitlement",
       "operation": "propagateCrossRegionEntitlement",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements"
      },
      {
       "kind": "secondaryButton",
       "label": "Reconcile redemptions",
       "operation": "reconcileRedemptions",
       "provenance": "contract cross-region.yaml POST /cross-region-entitlements/reconcile"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel decommission",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A cross-tenant health this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   },
   {
    "id": "formDecommissionCell",
    "component": "modal",
    "trigger": "Decommission cell",
    "body": "**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decommission cell",
     "operation": "decommissionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
   },
   {
    "id": "formUpdateCellTier",
    "component": "modal",
    "trigger": "Save cell tier",
    "body": "**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cell tier",
     "operation": "updateCellTier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tier",
      "scheduledFor"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
   },
   {
    "id": "formPropagateCrossRegionEntitlement",
    "component": "modal",
    "trigger": "Propagate cross region entitlement",
    "body": "**Collects what `propagateCrossRegionEntitlement` sends before it is called.** Required: `rightId`, `ticketId`, `issuingCellName`, `validFrom`, `validTo`, `admissionRulesId`, `entriesAllowed`. Optional: `guestLinkId`, `mediaCodes`, `venueId`. Dismissing sends nothing; the screen behind is unchanged.",
    "bindsTo": "PropagateRightRequest",
    "confirm": {
     "label": "Propagate cross region entitlement",
     "operation": "propagateCrossRegionEntitlement"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "rightId",
      "ticketId",
      "issuingCellName",
      "validFrom",
      "validTo",
      "admissionRulesId",
      "entriesAllowed",
      "guestLinkId",
      "mediaCodes",
      "venueId"
     ]
    },
    "provenance": "contract cross-region.yaml POST /cross-region-entitlements"
   },
   {
    "id": "formReconcileRedemptions",
    "component": "modal",
    "trigger": "Reconcile redemptions",
    "body": "**Collects what `reconcileRedemptions` sends before it is called.** Required: `consumingCellName`, `consumptions`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Reconcile redemptions",
     "operation": "reconcileRedemptions"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "consumingCellName",
      "consumptions"
     ]
    },
    "provenance": "contract cross-region.yaml POST /cross-region-entitlements/reconcile"
   }
  ],
  "states": {
   "loading": "The cross-tenant health list.",
   "error": "Could not load. Names which read failed and leaves the cross-tenant health untouched.",
   "emptyFirstRun": "No cross-tenant health yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelDecommission",
    "contract": "subscription",
    "purpose": "Halt a decommission",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "decommissionCell",
    "contract": "subscription",
    "purpose": "Begin decommissioning a cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCell",
    "contract": "subscription",
    "purpose": "Read a cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "Provisioning, migration and maintenance jobs",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "propagateCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Propagate a right from the issuing cell to a consuming cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCrossRegionEntitlement",
    "contract": "cross-region",
    "purpose": "Read a redemption right",
    "trigger": "onLoad"
   },
   {
    "operationId": "reconcileRedemptions",
    "contract": "cross-region",
    "purpose": "Report consumption back to the issuing cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getWalletAllocation",
    "contract": "cross-region",
    "purpose": "How wallet funds are allocated across regions",
    "trigger": "onLoad",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setWalletAllocationPolicy",
    "contract": "cross-region",
    "purpose": "Set the cross-region wallet allocation policy",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)",
    "invalidates": [
     "getWalletAllocation"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cellId",
     "from": "deepLink"
    },
    {
     "name": "rightId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`, `rightId`.",
   "preloaded": [
    "CellJob.id",
    "CellJob.kind",
    "CellJob.status",
    "CellJob.progressPercent",
    "CellJob.message"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-003",
   "derivedFrom": "wireframes/reference/Dashboards Board.dc.html",
   "note": "**Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed once and is not starting from nothing."
  },
  "apisNote": "Rebuilt 9 September 2026 from the 10 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-004",
  "name": "Platform Audit Log",
  "module": "Overview & Health",
  "requiresModule": "ai",
  "wave": 2,
  "capability": "C97",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/platform-audit-log",
   "component": "apps/ticvai-web/src/routes/general/PlatformAuditLogList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-031"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-004 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-004 holds none of them. The edge carries nothing: ADM-004 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-004 holds none of them. The edge carries nothing: cellId, rightId only pre-select (deep link or optional), and ADM-003 opens on its own"
    },
    {
     "to": "BO-068",
     "trigger": "Audit Log",
     "provenance": "flow F106 step 2→3",
     "operation": "listAiInteractions",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "openQuestions": [
   "No contract — Control Plane audit not specified"
  ],
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listAiInteractions` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find platform audit log for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "textField",
       "label": "Principal id",
       "operation": "listAiInteractions",
       "notes": "Sends `?principalId=` to `listAiInteractions`.",
       "provenance": "contract ai.yaml GET /interactions"
      },
      {
       "kind": "selectField",
       "label": "Outcome",
       "operation": "listAiInteractions",
       "notes": "Sends `?outcome=` to `listAiInteractions`.",
       "provenance": "contract ai.yaml GET /interactions"
      },
      {
       "kind": "datePicker",
       "label": "From",
       "operation": "listAiInteractions",
       "notes": "Sends `?from=` to `listAiInteractions`.",
       "provenance": "contract ai.yaml GET /interactions"
      },
      {
       "kind": "dataTable",
       "label": "Every AI interaction",
       "bindsTo": "AiInteraction",
       "columns": [
        "AiInteraction.id",
        "AiInteraction.conversationId",
        "AiInteraction.principalId",
        "AiInteraction.audience",
        "AiInteraction.subjectId",
        "AiInteraction.billableToTenantId",
        "AiInteraction.scopePath",
        "AiInteraction.capability",
        "AiInteraction.prompt",
        "AiInteraction.response",
        "AiInteraction.sources",
        "AiInteraction.outcome"
       ],
       "operation": "listAiInteractions",
       "provenance": "contract ai.yaml GET /interactions"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected AI interaction",
       "bindsTo": "AiInteraction",
       "columns": [
        "AiInteraction.id",
        "AiInteraction.conversationId",
        "AiInteraction.principalId",
        "AiInteraction.audience",
        "AiInteraction.subjectId",
        "AiInteraction.billableToTenantId",
        "AiInteraction.scopePath",
        "AiInteraction.capability",
        "AiInteraction.prompt",
        "AiInteraction.response",
        "AiInteraction.sources",
        "AiInteraction.outcome",
        "AiInteraction.refusalReason",
        "AiInteraction.provider",
        "AiInteraction.model",
        "AiInteraction.promptTokens"
       ],
       "operation": "listAiInteractions",
       "provenance": "contract ai.yaml GET /interactions"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The platform audit log list.",
   "error": "Could not load. Names which read failed and leaves the platform audit log untouched.",
   "emptyFirstRun": "No platform audit log yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Nothing matches the filter on principalId, outcome, from and the platform audit log are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Shown when the caller lacks `AI_AUDIT_VIEW`, which `listAiInteractions` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listAiInteractions",
    "contract": "ai",
    "purpose": "Every prompt, response and action",
    "trigger": "onLoad"
   },
   {
    "operationId": "getAiDecisionTrace",
    "contract": "ai",
    "purpose": "The full trace of a decision",
    "trigger": "onAction",
    "provenance": "build, 29 September 2026"
   }
  ],
  "entryState": {
   "preloaded": [
    "AiInteraction.id",
    "AiInteraction.conversationId",
    "AiInteraction.principalId",
    "AiInteraction.audience",
    "AiInteraction.subjectId"
   ],
   "params": [
    {
     "name": "decisionRecordId",
     "from": "navigation"
    }
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-004"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 1 operation this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-013",
  "name": "Tenant Performance Monitor",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/tenant-performance-monitor",
   "component": "apps/ticvai-web/src/routes/general/TenantPerformanceMonitorDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-012"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003",
    "ADM-014"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-013 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-013 holds none of them. The edge carries nothing: ADM-013 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-013 holds cellId, so an edge into it carries them"
    },
    {
     "to": "ADM-014",
     "trigger": "Auto-Scaling Configuration",
     "provenance": "flow F97 step 2→3",
     "carries": [
      "cellId"
     ]
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getCellHealth` reads one of them — list, select, act",
  "purpose": "See tenant performance monitor for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "detailPanel",
       "label": "The cell",
       "bindsTo": "CellDetail",
       "columns": [
        "CellDetail.id",
        "CellDetail.name",
        "CellDetail.kind",
        "CellDetail.clusterId",
        "CellDetail.isReachable",
        "CellDetail.lastContactAt",
        "CellDetail.licenceExpiresAt",
        "CellDetail.participatesInCrossCell",
        "CellDetail.regionId",
        "CellDetail.regionName",
        "CellDetail.countryCode",
        "CellDetail.tier",
        "CellDetail.status",
        "CellDetail.cloudProvider",
        "CellDetail.cloudRegion",
        "CellDetail.apiEndpoint"
       ],
       "operation": "getCell",
       "provenance": "contract subscription.yaml GET /cells/{cellId}"
      },
      {
       "kind": "detailPanel",
       "label": "The cell capacity",
       "bindsTo": "CellCapacity",
       "columns": [
        "CellCapacity.kind",
        "CellCapacity.tenantCount",
        "CellCapacity.isConstrained",
        "CellCapacity.constrainedDimension",
        "CellCapacity.dimensions",
        "CellCapacity.forecastBreachAt",
        "CellCapacity.measuredAt"
       ],
       "operation": "getCellCapacity",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/capacity"
      },
      {
       "kind": "detailPanel",
       "label": "The cell health",
       "bindsTo": "CellHealth",
       "columns": [
        "CellHealth.isHealthy",
        "CellHealth.isSchemaBehind",
        "CellHealth.databaseStatus",
        "CellHealth.replicationLagSeconds",
        "CellHealth.lastBackupAt",
        "CellHealth.lastRestoreDrillAt",
        "CellHealth.checkedAt"
       ],
       "operation": "getCellHealth",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/health"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "destructiveButton",
       "label": "Cancel decommission",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission cell",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Save cell tier",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel decommission",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A tenant performance this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   },
   {
    "id": "formDecommissionCell",
    "component": "modal",
    "trigger": "Decommission cell",
    "body": "**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decommission cell",
     "operation": "decommissionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
   },
   {
    "id": "formUpdateCellTier",
    "component": "modal",
    "trigger": "Save cell tier",
    "body": "**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cell tier",
     "operation": "updateCellTier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tier",
      "scheduledFor"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
   }
  ],
  "states": {
   "loading": "The tenant performance list.",
   "error": "Could not load. Names which read failed and leaves the tenant performance untouched.",
   "emptyFirstRun": "No tenant performance yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `getCellHealth` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "cancelDecommission",
    "contract": "subscription",
    "purpose": "Halt a decommission",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "decommissionCell",
    "contract": "subscription",
    "purpose": "Begin decommissioning a cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCell",
    "contract": "subscription",
    "purpose": "Read a cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
    "trigger": "onLoad"
   },
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "Provisioning, migration and maintenance jobs",
    "trigger": "onLoad"
   },
   {
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cellId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`.",
   "preloaded": [
    "CellJob.id",
    "CellJob.kind",
    "CellJob.status",
    "CellJob.progressPercent",
    "CellJob.message"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-013"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 7 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ADM-029",
  "name": "Deployment Monitor",
  "module": "Overview & Health",
  "requiresModule": "membership",
  "wave": 2,
  "capability": "C96",
  "implementation": {
   "app": "ticvai-web",
   "route": "/general/deployment-monitor",
   "component": "apps/ticvai-web/src/routes/general/DeploymentMonitorDashboard.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "ADM-002",
    "ADM-023"
   ],
   "inferred": true,
   "exitTo": [
    "ADM-001",
    "ADM-002",
    "ADM-003"
   ],
   "transitions": [
    {
     "to": "ADM-001",
     "trigger": "Platform Login / MFA",
     "provenance": "derived — ADM-001 declares entryState.params challengeId, methodId and ADM-029 holds none of them. The edge carries nothing: ADM-001 finds challengeId (createMfaChallenge), methodId (enrolMfaMethod) itself, and ADM-001 opens on its own"
    },
    {
     "to": "ADM-002",
     "trigger": "Platform Dashboard",
     "provenance": "derived — ADM-002 declares entryState.params  and ADM-029 holds none of them. The edge carries nothing: ADM-029 is opened from ADM-002, so this edge is the way back and ADM-002 keeps its own state"
    },
    {
     "to": "ADM-003",
     "trigger": "Cross-Tenant Health Dashboard",
     "carries": [
      "cellId"
     ],
     "provenance": "derived — ADM-003 declares entryState.params cellId, rightId and ADM-029 holds cellId, so an edge into it carries them"
    }
   ]
  },
  "notes": "Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listCellJobs` reads the population and `getRollout` reads one of them — list, select, act",
  "purpose": "Find deployment monitor for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "dataTable",
       "label": "Every rollout",
       "bindsTo": "Rollout",
       "columns": [
        "Rollout.id",
        "Rollout.releaseId",
        "Rollout.environment",
        "Rollout.status",
        "Rollout.cellsTotal",
        "Rollout.cellsComplete",
        "Rollout.cellsFailed",
        "Rollout.startedByPrincipalId",
        "Rollout.approvedByPrincipalId",
        "Rollout.pausedReason",
        "Rollout.startedAt",
        "Rollout.completedAt"
       ],
       "operation": "listRollouts",
       "provenance": "contract platform-ops.yaml GET /rollouts"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected cell job",
       "bindsTo": "CellJob",
       "columns": [
        "CellJob.id",
        "CellJob.kind",
        "CellJob.status",
        "CellJob.progressPercent",
        "CellJob.message",
        "CellJob.error",
        "CellJob.scheduledFor",
        "CellJob.completedAt"
       ],
       "operation": "listCellJobs",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/jobs"
      },
      {
       "kind": "detailPanel",
       "label": "The cell",
       "bindsTo": "CellDetail",
       "columns": [
        "CellDetail.id",
        "CellDetail.name",
        "CellDetail.kind",
        "CellDetail.clusterId",
        "CellDetail.isReachable",
        "CellDetail.lastContactAt",
        "CellDetail.licenceExpiresAt",
        "CellDetail.participatesInCrossCell",
        "CellDetail.regionId",
        "CellDetail.regionName",
        "CellDetail.countryCode",
        "CellDetail.tier",
        "CellDetail.status",
        "CellDetail.cloudProvider",
        "CellDetail.cloudRegion",
        "CellDetail.apiEndpoint"
       ],
       "operation": "getCell",
       "provenance": "contract subscription.yaml GET /cells/{cellId}"
      },
      {
       "kind": "detailPanel",
       "label": "The cell capacity",
       "bindsTo": "CellCapacity",
       "columns": [
        "CellCapacity.kind",
        "CellCapacity.tenantCount",
        "CellCapacity.isConstrained",
        "CellCapacity.constrainedDimension",
        "CellCapacity.dimensions",
        "CellCapacity.forecastBreachAt",
        "CellCapacity.measuredAt"
       ],
       "operation": "getCellCapacity",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/capacity"
      },
      {
       "kind": "detailPanel",
       "label": "The cell health",
       "bindsTo": "CellHealth",
       "columns": [
        "CellHealth.isHealthy",
        "CellHealth.isSchemaBehind",
        "CellHealth.databaseStatus",
        "CellHealth.replicationLagSeconds",
        "CellHealth.lastBackupAt",
        "CellHealth.lastRestoreDrillAt",
        "CellHealth.checkedAt"
       ],
       "operation": "getCellHealth",
       "provenance": "contract subscription.yaml GET /cells/{cellId}/health"
      },
      {
       "kind": "detailPanel",
       "label": "The rollout",
       "bindsTo": "RolloutDetail",
       "columns": [
        "RolloutDetail.id",
        "RolloutDetail.releaseId",
        "RolloutDetail.environment",
        "RolloutDetail.status",
        "RolloutDetail.cellsTotal",
        "RolloutDetail.cellsComplete",
        "RolloutDetail.cellsFailed",
        "RolloutDetail.startedByPrincipalId",
        "RolloutDetail.approvedByPrincipalId",
        "RolloutDetail.pausedReason",
        "RolloutDetail.startedAt",
        "RolloutDetail.completedAt",
        "RolloutDetail.cells"
       ],
       "operation": "getRollout",
       "provenance": "contract platform-ops.yaml GET /rollouts/{rolloutId}"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Pause rollout",
       "operation": "pauseRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/pause"
      },
      {
       "kind": "secondaryButton",
       "label": "Rollback rollout",
       "operation": "rollbackRollout",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/rollback"
      },
      {
       "kind": "destructiveButton",
       "label": "Cancel decommission",
       "operation": "cancelDecommission",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Decommission cell",
       "operation": "decommissionCell",
       "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
      },
      {
       "kind": "secondaryButton",
       "label": "Start rollout",
       "operation": "startRollout",
       "notes": "Requests the stage; it does not move it. `startRollout` answers 202 with `approvalRequestId` and the rollout unchanged until the platform release manager approves (decided 28 September, audit R144).",
       "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/start"
      },
      {
       "kind": "secondaryButton",
       "label": "Save cell tier",
       "operation": "updateCellTier",
       "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmCancelDecommission",
    "component": "confirmDialog",
    "trigger": "Cancel decommission",
    "body": "**Names what `cancelDecommission` changes and what it leaves alone**, in the consequence rather than the verb. A deployment this affects should be identified in the dialog, not just counted. **Collects what `cancelDecommission` sends before it is called.** Required: `reason`.",
    "provenance": "contract subscription.yaml POST /cells/{cellId}/cancel-decommission"
   },
   {
    "id": "formPauseRollout",
    "component": "modal",
    "trigger": "Pause rollout",
    "body": "**Collects what `pauseRollout` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Pause rollout",
     "operation": "pauseRollout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/pause"
   },
   {
    "id": "formRollbackRollout",
    "component": "modal",
    "trigger": "Rollback rollout",
    "body": "**Collects what `rollbackRollout` sends before it is called.** Required: `reason`, `stepUpToken`. Optional: `cellIds`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Rollback rollout",
     "operation": "rollbackRollout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason",
      "stepUpToken",
      "cellIds"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/rollback"
   },
   {
    "id": "formDecommissionCell",
    "component": "modal",
    "trigger": "Decommission cell",
    "body": "**Collects what `decommissionCell` sends before it is called.** Required: `reason`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Decommission cell",
     "operation": "decommissionCell"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "reason"
     ]
    },
    "provenance": "contract subscription.yaml POST /cells/{cellId}/decommission"
   },
   {
    "id": "formStartRollout",
    "component": "modal",
    "trigger": "Start rollout",
    "body": "**Collects what `startRollout` sends before it is called.** Required: `stage`. **Sending it asks for approval, it does not promote** (decided 28 September, audit R144): the answer is 202 with a pending `releasePromotion` request, routed to a holder of `PLATFORM_RELEASE_PROMOTE` other than the requester — nobody approves their own promotion. The rollout moves to the stage when that request is approved. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Start rollout",
     "operation": "startRollout"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "stage"
     ]
    },
    "provenance": "contract platform-ops.yaml POST /rollouts/{rolloutId}/start"
   },
   {
    "id": "formUpdateCellTier",
    "component": "modal",
    "trigger": "Save cell tier",
    "body": "**Collects what `updateCellTier` sends before it is called.** Required: `tier`. Optional: `scheduledFor`. Dismissing sends nothing; the screen behind is unchanged.",
    "confirm": {
     "label": "Save cell tier",
     "operation": "updateCellTier"
    },
    "dismiss": {
     "label": "Cancel",
     "discards": [
      "tier",
      "scheduledFor"
     ]
    },
    "provenance": "contract subscription.yaml PATCH /cells/{cellId}"
   }
  ],
  "states": {
   "loading": "The deployment list.",
   "error": "Could not load. Names which read failed and leaves the deployment untouched.",
   "emptyFirstRun": "No deployment yet. **Offers no create action** — this screen declares no operation that makes one — and says so rather than showing an empty table.",
   "emptyNoResults": "Never shown: `listCellJobs` takes no filter, so an empty list is always the first-run state above.",
   "emptyNoAccess": "Shown when the caller lacks `PLATFORM_CELL_VIEW`, which `listCellJobs` requires, and names that permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question.",
   "rolloutPendingApproval": "**Requested, not moved.** `startRollout` answered 202: the rollout shows the stage it has reached, the stage requested and that a `releasePromotion` approval is pending with the platform release manager. The requester sees no approve action for their own request (decided 28 September, audit R144)."
  },
  "apis": [
   {
    "operationId": "listCellJobs",
    "contract": "subscription",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "listRollouts",
    "contract": "platform-ops",
    "purpose": "Rollouts in flight",
    "trigger": "onLoad"
   },
   {
    "operationId": "getRollout",
    "contract": "platform-ops",
    "purpose": "Per-cell progress",
    "trigger": "onAction"
   },
   {
    "operationId": "pauseRollout",
    "contract": "platform-ops",
    "purpose": "Halt before the next cell",
    "trigger": "onAction"
   },
   {
    "operationId": "rollbackRollout",
    "contract": "platform-ops",
    "purpose": "Revert, where every migration is reversible",
    "trigger": "onAction"
   },
   {
    "operationId": "cancelDecommission",
    "contract": "subscription",
    "purpose": "Halt a decommission",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "decommissionCell",
    "contract": "subscription",
    "purpose": "Begin decommissioning a cell",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "getCell",
    "contract": "subscription",
    "purpose": "Read a cell",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellCapacity",
    "contract": "subscription",
    "purpose": "Load against headroom",
    "trigger": "onLoad"
   },
   {
    "operationId": "getCellHealth",
    "contract": "subscription",
    "purpose": "Cell health and schema version",
    "trigger": "onLoad"
   },
   {
    "operationId": "startRollout",
    "contract": "platform-ops",
    "purpose": "Request the next rollout stage; 202 pending the platform release manager's releasePromotion approval, never the requester's own (audit R144)",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   },
   {
    "operationId": "updateCellTier",
    "contract": "subscription",
    "purpose": "Change a cell's tier",
    "trigger": "onAction",
    "invalidates": [
     "listCellJobs"
    ]
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "cellId",
     "from": "deepLink"
    },
    {
     "name": "rolloutId",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A platform-admin link resolves against the tenant in the link and refuses if the operator does not hold that tenant.** A link is not authorisation. If the target is gone the screen says so and returns to the directory — **an admin console that silently shows the wrong tenant is worse than one that shows nothing.** Arrives with `cellId`, `rolloutId`.",
   "preloaded": [
    "CellJob.id",
    "CellJob.kind",
    "CellJob.status",
    "CellJob.progressPercent",
    "CellJob.message"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P09 TICVAI Web.dc.html#adm-029"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 12 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P09",
   "audience": "platformAdmin",
   "formFactor": "web",
   "shortName": "TICVAI Web",
   "name": "TICVAI Web — Platform Console",
   "offlineCapable": false,
   "app": "ticvai-web",
   "operator": "ticvai",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P10",
     "P11",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "cancelDecommission": {
  "method": "POST",
  "path": "/cells/{cellId}/cancel-decommission",
  "contract": "subscription",
  "summary": "Halt a decommission",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "decommissionCell": {
  "method": "POST",
  "path": "/cells/{cellId}/decommission",
  "contract": "subscription",
  "summary": "Begin decommissioning a cell",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getAiDecisionTrace": {
  "method": "GET",
  "path": "/decision-records/{decisionRecordId}/trace",
  "contract": "ai",
  "summary": "The full trace of a decision",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "depth",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "AiDecisionTrace"
 },
 "getCell": {
  "method": "GET",
  "path": "/cells/{cellId}",
  "contract": "subscription",
  "summary": "Read a cell",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CellDetail"
 },
 "getCellCapacity": {
  "method": "GET",
  "path": "/cells/{cellId}/capacity",
  "contract": "subscription",
  "summary": "Load against headroom",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "window",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "CellCapacity"
 },
 "getCellHealth": {
  "method": "GET",
  "path": "/cells/{cellId}/health",
  "contract": "subscription",
  "summary": "Cell health and schema version",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "CellHealth"
 },
 "getCrossRegionEntitlement": {
  "method": "GET",
  "path": "/cross-region-entitlements/{rightId}",
  "contract": "cross-region",
  "summary": "Read a redemption right",
  "permission": "TICKET_LOOKUP",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "CrossRegionEntitlement"
 },
 "getEntitlementUsage": {
  "method": "GET",
  "path": "/tenants/{tenantId}/entitlement-usage",
  "contract": "subscription",
  "summary": "Usage against licensed limits",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "EntitlementUsage"
 },
 "getRollout": {
  "method": "GET",
  "path": "/rollouts/{rolloutId}",
  "contract": "platform-ops",
  "summary": "Rollout progress per cell",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "RolloutDetail"
 },
 "getSsoConfig": {
  "method": "GET",
  "path": "/tenants/sso-config",
  "contract": "identity",
  "summary": "Read SSO configuration",
  "permission": "USER_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "SsoProviderConfig"
 },
 "getTenant": {
  "method": "GET",
  "path": "/tenants/{tenantId}",
  "contract": "subscription",
  "summary": "Read a tenant with cells and subscription",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "TenantDetail"
 },
 "getTenantLicences": {
  "method": "GET",
  "path": "/tenants/{tenantId}/licences",
  "contract": "subscription",
  "summary": "What a tenant is licensed to use",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "LicencePosition"
 },
 "getWalletAllocation": {
  "method": "GET",
  "path": "/wallet-allocations",
  "contract": "cross-region",
  "summary": "The consuming cell's bounded offline allocation",
  "permission": "ORDER_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "guestLinkId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": "WalletAllocation"
 },
 "listAiInteractions": {
  "method": "GET",
  "path": "/interactions",
  "contract": "ai",
  "summary": "Every prompt, response and action",
  "permission": "AI_AUDIT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "principalId",
    "in": "query",
    "required": null
   },
   {
    "name": "outcome",
    "in": "query",
    "required": null
   },
   {
    "name": "from",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listCellJobs": {
  "method": "GET",
  "path": "/cells/{cellId}/jobs",
  "contract": "subscription",
  "summary": "Provisioning, migration and maintenance jobs",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listRollouts": {
  "method": "GET",
  "path": "/rollouts",
  "contract": "platform-ops",
  "summary": "List rollouts",
  "permission": "PLATFORM_RELEASE_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "listTenantCells": {
  "method": "GET",
  "path": "/tenants/{tenantId}/cells",
  "contract": "subscription",
  "summary": "List a tenant's cells",
  "permission": "PLATFORM_CELL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "Cell"
 },
 "listTenants": {
  "method": "GET",
  "path": "/tenants",
  "contract": "subscription",
  "summary": "List tenants",
  "permission": "PLATFORM_TENANT_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "planId",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 },
 "pauseRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/pause",
  "contract": "platform-ops",
  "summary": "Halt a rollout in progress",
  "permission": "PLATFORM_RELEASE_PROMOTE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "RolloutDetail"
 },
 "propagateCrossRegionEntitlement": {
  "method": "POST",
  "path": "/cross-region-entitlements",
  "contract": "cross-region",
  "summary": "Propagate a right from the issuing cell to a consuming cell",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "PropagateRightRequest",
  "responds": "CrossRegionEntitlement"
 },
 "reconcileRedemptions": {
  "method": "POST",
  "path": "/cross-region-entitlements/reconcile",
  "contract": "cross-region",
  "summary": "Report consumption back to the issuing cell",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "append",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "rollbackRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/rollback",
  "contract": "platform-ops",
  "summary": "Roll a rollout back",
  "permission": "PLATFORM_RELEASE_PROMOTE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "setWalletAllocationPolicy": {
  "method": "PUT",
  "path": "/wallet-allocations",
  "contract": "cross-region",
  "summary": "Set the allocation cap policy",
  "permission": "REGION_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "region",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "WalletAllocation"
 },
 "startRollout": {
  "method": "POST",
  "path": "/rollouts/{rolloutId}/start",
  "contract": "platform-ops",
  "summary": "Start or continue a rollout",
  "permission": "PLATFORM_RELEASE_PROMOTE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "updateCellTier": {
  "method": "PATCH",
  "path": "/cells/{cellId}",
  "contract": "subscription",
  "summary": "Change a cell's tier",
  "permission": "PLATFORM_CELL_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": null
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AiActionPlanDetail": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.action_plan with its ai.action_step rows",
  "description": "A plan with its steps in DAG order.",
  "required": [
   "plan",
   "steps"
  ],
  "properties": {
   "plan": {
    "$ref": "#/components/schemas/AiActionPlan"
   },
   "steps": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiActionStep"
    }
   }
  }
 },
 "AiDecisionRecord": {
  "type": "object",
  "x-ticvai-persistence": "ai.decision_record",
  "description": "**The standard record for every governed decision** (design 3.9, C12; AIC-193..209): a recommendation summary, a risk assessment, a forecast publication, a plan step, an assistant answer at significant depth, a governance block, a Help me choose suggestion. **Append-only; corrections are annotations; hash-chained per tenant** so tampering is detectable (AIC-203, AIC-204). **AI log database** (design 2.4): append-only, partitioned by month, one Postgres database per tenant on the regional AI log server. The table name stays `ai.<table>`; which server holds it is a deployment matter, not a contract one.",
  "required": [
   "traceId",
   "capabilityKey",
   "outcome",
   "recordHash"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "traceId": {
    "type": "string"
   },
   "capabilityKey": {
    "type": "string"
   },
   "task": {
    "type": "string",
    "nullable": true
   },
   "subjectKind": {
    "type": "string",
    "nullable": true
   },
   "subjectRef": {
    "type": "string",
    "nullable": true
   },
   "inputsRef": {
    "type": "string",
    "nullable": true,
    "description": "Where the inputs are kept (Blob or `ai.activity`), never the prompt text itself."
   },
   "evidence": {
    "$ref": "#/components/schemas/AiEvidenceItemList"
   },
   "producer": {
    "type": "string",
    "nullable": true
   },
   "modelVersion": {
    "type": "string",
    "nullable": true
   },
   "promptTemplateVersion": {
    "type": "string",
    "nullable": true
   },
   "featureSetVersion": {
    "type": "string",
    "nullable": true
   },
   "knowledgeVersion": {
    "type": "string",
    "nullable": true
   },
   "ruleVersions": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "governanceOutcome": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiGovernanceOutcome"
     }
    ],
    "nullable": true
   },
   "policyVersion": {
    "type": "string",
    "nullable": true
   },
   "approvals": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Approval requests and their decisions."
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true,
    "description": "Override or intervention, where a person changed the outcome."
   },
   "executionResult": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "outcomeRef": {
    "type": "string",
    "nullable": true,
    "description": "The business outcome it links to (an order, a published version, a closed case)."
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "allowed",
     "blocked",
     "executed",
     "failed",
     "approvedThenFailed",
     "published",
     "suggested"
    ],
    "description": "`approvedThenFailed` is kept distinct from `executed` (design 1.2 Audit)."
   },
   "annotations": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "at": {
       "type": "string",
       "format": "date-time"
      },
      "byPrincipalId": {
       "type": "string",
       "format": "uuid"
      },
      "note": {
       "type": "string"
      }
     }
    },
    "readOnly": true,
    "description": "Corrections, appended; the original fields are never edited."
   },
   "previousHash": {
    "type": "string",
    "readOnly": true
   },
   "recordHash": {
    "type": "string",
    "readOnly": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiDecisionTrace": {
  "type": "object",
  "x-ticvai-persistence": "none — ai.decision_record with the rows it references",
  "description": "**The full trace of one decision** (ADM-540..546): record, evidence, candidates and rules, model and runtime, governance and approvals, execution and business outcome. Depth is gated by permission (AIC-195).",
  "required": [
   "record"
  ],
  "properties": {
   "record": {
    "$ref": "#/components/schemas/AiDecisionRecord"
   },
   "depth": {
    "type": "string",
    "enum": [
     "business",
     "governance",
     "technical"
    ]
   },
   "explanation": {
    "type": "string",
    "description": "Built from structured evidence, never a model's chain of thought (AIC-192)."
   },
   "activity": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiInteraction"
    },
    "description": "The model calls behind it (`technical` depth)."
   },
   "plan": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AiActionPlanDetail"
     }
    ],
    "nullable": true
   },
   "interventions": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/AiIntervention"
    }
   },
   "chainVerified": {
    "type": "boolean",
    "description": "The hash chain around this record verifies."
   }
  }
 },
 "AiInteraction": {
  "type": "object",
  "x-ticvai-persistence": "ai.activity",
  "required": [
   "id",
   "principalId",
   "capability",
   "outcome",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "conversationId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "principalId": {
    "type": "string",
    "format": "uuid"
   },
   "audience": {
    "type": "string",
    "enum": [
     "staff",
     "guest"
    ],
    "description": "**Billing divides on this.** Staff usage is bounded by headcount; guest usage is bounded by footfall and curiosity, and a venue cannot stop guests asking questions.\n"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The guest, where the audience is `guest`. `principalId` is null in that case — **a guest is not a principal**, and attributing their tokens to a staff member would be wrong twice.\n"
   },
   "billableToTenantId": {
    "type": "string",
    "format": "uuid",
    "description": "Resolved from `scopePath` at write time, not derived later. **Billing must not depend on walking a scope tree that has since been reorganised.**\n"
   },
   "scopePath": {
    "type": "string"
   },
   "capability": {
    "type": "string"
   },
   "prompt": {
    "type": "string"
   },
   "response": {
    "type": "string"
   },
   "sources": {
    "$ref": "#/components/schemas/AiSourceList"
   },
   "outcome": {
    "type": "string",
    "enum": [
     "answered",
     "refused",
     "applied",
     "rejected",
     "failed"
    ]
   },
   "refusalReason": {
    "type": "string",
    "nullable": true
   },
   "provider": {
    "$ref": "#/components/schemas/AiProviderKind"
   },
   "model": {
    "type": "string"
   },
   "promptTokens": {
    "type": "integer"
   },
   "completionTokens": {
    "type": "integer"
   },
   "cost": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "x-ticvai-column": "cost_amount",
    "description": "What the call cost at the provider. **Money like every other amount** (naming-and-style 5.1) — it replaces an integer `costMinor` that carried no currency or scale, which AED and OMR read differently.\n"
   },
   "latencyMs": {
    "type": "integer"
   },
   "maskedFieldCount": {
    "type": "integer",
    "description": "How many fields were redacted. Zero on a prompt touching guest data is a defect."
   },
   "traceId": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The `ai.decision_record` this call belongs to, where it was part of a governed decision (AI design 2.3, 3.9). Null for a call audited by this row alone."
   },
   "cacheLayer": {
    "type": "string",
    "nullable": true,
    "enum": [
     "guardrail",
     "semantic",
     "exact",
     "negative",
     "analytics"
    ],
    "description": "Which cache answered, where one did (AI design 3.6). Null for a model call."
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "AiIntervention": {
  "type": "object",
  "x-ticvai-persistence": "ai.intervention",
  "description": "**A person stepping in** (AIC-187, ADM-535, ADM-536): an override, pause, resume, stop, retry or rollback, with the original AI decision and the human one side by side.",
  "required": [
   "kind",
   "targetKind",
   "targetRef"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "override",
     "pause",
     "resume",
     "cancel",
     "retry",
     "rollback",
     "capabilityPause",
     "capabilityResume"
    ]
   },
   "targetKind": {
    "type": "string",
    "enum": [
     "plan",
     "step",
     "decision",
     "capability"
    ]
   },
   "targetRef": {
    "type": "string"
   },
   "decisionRecordId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "originalDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "humanDecision": {
    "type": "object",
    "additionalProperties": true,
    "nullable": true
   },
   "reason": {
    "type": "string",
    "maxLength": 2000
   },
   "principalId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "x-ticvai-references": "identity.principal"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Row-level security compares it with `ticvai.scope_paths` (`platform.apply_scope_rls`), on the tenant database and on the AI log database alike (design 3.1)."
   }
  }
 },
 "AiProviderKind": {
  "type": "string",
  "enum": [
   "openai",
   "gemini",
   "anthropic",
   "azureOpenai",
   "localLlm",
   "openaiCompatible"
  ],
  "description": "`openaiCompatible` (added 29 September, AI design 3.3): a customer endpoint that speaks the OpenAI API, taken with no custom development (AIC-009). Any other protocol needs an adapter.\n"
 },
 "AiSourceList": {
  "type": "array",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "jsonb",
  "description": "**The sources an answer was grounded in, stored with the answer** (8.3.70). One `jsonb` column on the row that carries it — `ai.message.sources` and `ai.activity.sources` — because the grounding audit reads the list as it was when the answer was given, and a source is never queried on its own.\n",
  "items": {
   "$ref": "#/components/schemas/AiSource"
  }
 },
 "Cell": {
  "x-ticvai-persistence": "control.cell",
  "x-ticvai-retired-columns": [
   "tenant_id"
  ],
  "type": "object",
  "required": [
   "id",
   "name",
   "regionId",
   "countryCode",
   "tier",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "$ref": "#/components/schemas/CellKind"
   },
   "clusterId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "isReachable": {
    "type": "boolean",
    "default": true,
    "description": "False for `onPremiseIsolated`, true for `onPremiseConnected` (ADR-0046). When false, the Control Plane holds the record for licensing and support and **cannot reach the installation** — it may sit behind a firewall with no inbound route. Every operation assuming reachability must handle absence rather than timing out, and a cell that has not called home for a month is not necessarily broken.\n"
   },
   "lastContactAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the site last called out. The only liveness signal for an unreachable cell, and the number a support engineer asks for first.\n"
   },
   "licenceExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "On-premise only. Licensing cannot be enforced by a Control Plane the site cannot reach, so a signed licence file is verified locally. **An expired licence degrades rather than stops** — a venue whose gates refuse entry because a licence lapsed over a weekend is worse than one running unlicensed until Monday.\n"
   },
   "participatesInCrossCell": {
    "type": "boolean",
    "default": true,
    "description": "False by default for `onPremiseIsolated`, available for `onPremiseConnected` (ADR-0046). Redeeming a pass issued elsewhere requires reaching the issuing cell at that moment, and an on-premise site may not be able to. Exclusion is the honest default; local-then-reconcile carries a double-redemption risk that needs a decision rather than an assumption.\n"
   },
   "regionId": {
    "type": "string",
    "format": "uuid"
   },
   "regionName": {
    "type": "string"
   },
   "countryCode": {
    "type": "string"
   },
   "tier": {
    "$ref": "#/components/schemas/CellTier"
   },
   "status": {
    "$ref": "#/components/schemas/CellStatus"
   },
   "cloudProvider": {
    "type": "string",
    "nullable": true
   },
   "cloudRegion": {
    "type": "string",
    "nullable": true
   },
   "apiEndpoint": {
    "type": "string",
    "nullable": true
   },
   "venueCount": {
    "type": "integer"
   },
   "provisionedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "deploymentRef": {
    "type": "string",
    "nullable": true,
    "description": "**A pointer to where this cell runs, not a description of it.** A Kubernetes namespace, an ECS cluster ARN, a stack name — whatever the orchestrator calls the thing.\n\n**The platform does not model instances, nodes or shards** (31 August). Kubernetes already holds instance counts and they change by the second; a table copying them drifts within minutes and the copy would win.\n\n**The line is: routing decisions belong to the platform, provisioning facts belong to the orchestrator.** Qdrant is the proof — ADR-0021 makes the tenant *the* shard key, so nine operations route without a lookup and **a stored shard assignment would be a second copy of something derivable.**\n\n**CF-161 needed a table after all, and this said it did not.** The claim here was that one database per cell or one per service is a build-time decision and the DDL is identical either way. **ADR-0038 answered it per tenant**, which drops `Cell.tenantId`, adds `CellTenant`, `RolloutTenant` and a per-tenant migration row, and takes `control` out of the tenant template. `tools/derive-ddl.py` carried the same claim in its docstring.\n\n**A claim that a question cannot affect your artefact is the one most likely to be left standing after it does**, which is why the correction is recorded here rather than the sentence simply deleted."
   }
  }
 },
 "CellCapacity": {
  "type": "object",
  "x-ticvai-persistence": "none — measured, not stored",
  "required": [
   "cellId",
   "isConstrained",
   "dimensions",
   "measuredAt"
  ],
  "properties": {
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "$ref": "#/components/schemas/CellKind"
   },
   "tenantCount": {
    "type": "integer",
    "description": "Reported, and **deliberately not the sizing signal.** Forty quiet tenants may load a cell less than three busy ones.\n"
   },
   "isConstrained": {
    "type": "boolean"
   },
   "constrainedDimension": {
    "type": "string",
    "nullable": true
   },
   "dimensions": {
    "type": "array",
    "description": "Per dimension, because the response differs. Short of connections and long on storage is a different problem from short of both.\n",
    "items": {
     "type": "object",
     "required": [
      "dimension",
      "used",
      "headroom"
     ],
     "properties": {
      "dimension": {
       "type": "string",
       "enum": [
        "concurrentUsers",
        "transactionsPerSecond",
        "scansPerSecond",
        "databaseConnections",
        "storageGb",
        "replicationLag",
        "cpu"
       ]
      },
      "used": {
       "type": "number"
      },
      "limit": {
       "type": "number"
      },
      "headroom": {
       "type": "number",
       "description": "Fraction remaining. Negative means already over."
      },
      "peakAt": {
       "type": "string",
       "format": "date-time",
       "nullable": true
      }
     }
    }
   },
   "forecastBreachAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the constrained dimension is projected to run out at the current trend. Null where there is no trend to project — an honest null beats an invented date.\n"
   },
   "measuredAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CellDetail": {
  "x-ticvai-persistence": "control.cell",
  "allOf": [
   {
    "$ref": "#/components/schemas/Cell"
   },
   {
    "type": "object",
    "properties": {
     "health": {
      "$ref": "#/components/schemas/CellHealth"
     },
     "activeJobs": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/CellJob"
      }
     }
    }
   }
  ]
 },
 "CellHealth": {
  "x-ticvai-persistence": "none — polled, not stored",
  "type": "object",
  "required": [
   "cellId",
   "isHealthy",
   "schemaVersion",
   "checkedAt"
  ],
  "properties": {
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "isHealthy": {
    "type": "boolean"
   },
   "schemaVersion": {
    "type": "string",
    "description": "From the cell's version register. Skew across a tenant's cells is expected during rollout; unexplained skew is a defect.\n"
   },
   "isSchemaBehind": {
    "type": "boolean"
   },
   "databaseStatus": {
    "type": "string"
   },
   "replicationLagSeconds": {
    "type": "number",
    "nullable": true
   },
   "lastBackupAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastRestoreDrillAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "checkedAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "CellJob": {
  "x-ticvai-persistence": "control.cell_job",
  "type": "object",
  "required": [
   "id",
   "cellId",
   "kind",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "kind": {
    "type": "string",
    "enum": [
     "provision",
     "tierMigration",
     "schemaMigration",
     "backup",
     "restore",
     "decommission"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "queued",
     "running",
     "completed",
     "failed",
     "rolledBack"
    ]
   },
   "progressPercent": {
    "type": "integer",
    "minimum": 0,
    "maximum": 100
   },
   "message": {
    "type": "string",
    "nullable": true
   },
   "error": {
    "type": "string",
    "nullable": true
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "CellKind": {
  "type": "string",
  "description": "Two deployment locations (ADR-0017, amended by ADR-0046). `shared` is the default; the others exist because a client asked or a law requires it.\n\n**On-premise is two configurations, not one (ADR-0046).** `onPremiseIsolated` keeps no channel to TICVAI — updates are pull-initiated or physically delivered, licensing is a signed file, support is blind. `onPremiseConnected` keeps an outbound control channel and is reachable, updatable and licensable in the ordinary way. The channel carries control traffic only and no natural person (ADR-0043); **AI inference is data, not control**, so connectivity alone does not grant the assistant.\n\nThere is no `hybrid`. The RFP's third model is answered by `onPremiseConnected`; a genuine split workload has never been asked for and would be a new decision.\n\n\n**`burst` added 31 August.** An environment stood up for one on-sale and torn down after (CF-162 scenario c). **It is not a jurisdiction and it is not permanent** — it holds a catalogue snapshot, three services of sixteen, and 17 tables of 380.\n\n**The other four are places data lives. This one is a place data passes through**, which is why it has its own lifecycle and a reconciliation obligation the others do not.",
  "enum": [
   "shared",
   "dedicated",
   "onPremiseIsolated",
   "onPremiseConnected",
   "controlPlane",
   "burst"
  ]
 },
 "CellStatus": {
  "type": "string",
  "enum": [
   "provisioning",
   "active",
   "migrating",
   "suspended",
   "decommissioning",
   "failed"
  ]
 },
 "CellTier": {
  "type": "string",
  "enum": [
   "shared",
   "dedicated",
   "isolated",
   "clientHosted"
  ]
 },
 "CrossRegionEntitlement": {
  "x-ticvai-persistence": "platform.cross_region_entitlement",
  "type": "object",
  "required": [
   "rightId",
   "ticketId",
   "issuingCellName",
   "consumingCellName",
   "validFrom",
   "validTo",
   "entriesAllowed",
   "entriesConsumed",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "rightId": {
    "type": "string",
    "format": "uuid"
   },
   "ticketId": {
    "type": "string"
   },
   "guestLinkId": {
    "type": "string",
    "nullable": true
   },
   "issuingCellName": {
    "type": "string"
   },
   "consumingCellName": {
    "type": "string"
   },
   "mediaCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Null where the right is valid at any venue in the consuming cell."
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true,
    "description": "Null means unlimited."
   },
   "entriesConsumed": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "active",
     "exhausted",
     "revoked",
     "expired"
    ]
   },
   "lastConsumedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "lastReconciledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "EntitlementLimit": {
  "type": "object",
  "required": [
   "metric",
   "limit"
  ],
  "properties": {
   "metric": {
    "$ref": "#/components/schemas/UsageMetric"
   },
   "limit": {
    "type": "integer",
    "nullable": true,
    "x-ticvai-column": "limit_value",
    "description": "Null means unlimited. Stored as `limit_value` — `limit` is a reserved word, and `subscription.tier_allowance` already names the same figure `limit_value`."
   },
   "overageAllowed": {
    "type": "boolean",
    "default": false
   },
   "overageUnitPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  }
 },
 "EntitlementUsage": {
  "x-ticvai-persistence": "none — aggregated from usage_record",
  "type": "object",
  "required": [
   "tenantId",
   "metrics"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "metrics": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "metric",
      "current",
      "isNearLimit"
     ],
     "properties": {
      "metric": {
       "$ref": "#/components/schemas/UsageMetric"
      },
      "current": {
       "type": "integer"
      },
      "limit": {
       "type": "integer",
       "nullable": true
      },
      "percentUsed": {
       "type": "number",
       "nullable": true
      },
      "isNearLimit": {
       "type": "boolean",
       "description": "Approaching a limit is an account conversation. Hitting one silently at a gate is an incident.\n"
      },
      "isExceeded": {
       "type": "boolean"
      }
     }
    }
   },
   "asAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "EnvironmentKind": {
  "type": "string",
  "enum": [
   "dev",
   "staging",
   "production"
  ]
 },
 "LicencePosition": {
  "x-ticvai-persistence": "none — union of the tenant's plan (control.tenant.plan_id -> subscription.plan_module, subscription.plan_limit) and its add-ons (control.licence_add_on, control.licence_add_on_limit by tenant_id)",
  "type": "object",
  "required": [
   "tenantId",
   "licensedModules",
   "limits"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "licensedModules": {
    "type": "array",
    "description": "Union of plan modules and add-ons. The White Label Builder reads this and cannot enable anything absent from it.\n",
    "items": {
     "type": "object",
     "required": [
      "moduleKey",
      "source"
     ],
     "properties": {
      "moduleKey": {
       "type": "string"
      },
      "displayName": {
       "type": "string"
      },
      "source": {
       "type": "string",
       "enum": [
        "plan",
        "addOn"
       ]
      },
      "validTo": {
       "type": "string",
       "format": "date",
       "nullable": true
      }
     }
    }
   },
   "limits": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/EntitlementLimit"
    }
   }
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "Money": {
  "type": "object",
  "x-ticvai-persistence-kind": "valueObject",
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**On the wire this is three fields; in the database it is one column.**\n24 August. Every column typed `Money` was landing as `jsonb` — 129 of them, including `orders.shift.opening_float`, `inventory.purchase_order.total` and `promotions.voucher.balance`. **`orders.cash_movement.amount` was `numeric(18,4)` because somebody hand-typed that one**, and the inconsistency is what made it visible.\n**A jsonb price cannot be summed in SQL.** Every total, variance and reconciliation moves into application code — and a shift variance computed in .NET against a ledger computed in Postgres is two answers to one question. That is F13 month-end and F98 takings-to-ledger, both walked, both assuming the arithmetic is in the database.\n**`currency` and `scale` are not stored per row.** ADR-0018 makes them region-scoped and not overridable below, so they resolve from the scope walk — storing AED against nine million rows in a UAE region is nine million copies of a fact that cannot differ. A row that needed its own currency would be a row in the wrong region.\n**They stay on the wire** because a client reading a figure should not have to walk a hierarchy to know what it means.\n",
  "required": [
   "amount",
   "currency",
   "scale"
  ],
  "properties": {
   "amount": {
    "type": "string",
    "description": "Decimal string, never a float. Up to 4 decimal places. **Persisted as `numeric(18,4)`** — the string is a transport choice, so a JavaScript client cannot round a fare in transit.\n",
    "pattern": "^-?\\d+(\\.\\d{1,4})?$"
   },
   "currency": {
    "type": "string",
    "description": "**Resolved from the region, not stored on the row** (ADR-0018). OMR uses 3 decimal places and AED uses 2 — a venue on a different scale from its region is a ledger that cannot consolidate.\n",
    "pattern": "^[A-Z]{3}$"
   },
   "scale": {
    "type": "integer",
    "description": "Resolved from the region alongside `currency`.",
    "minimum": 0,
    "maximum": 4
   }
  }
 },
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 },
 "PropagateRightRequest": {
  "type": "object",
  "required": [
   "rightId",
   "ticketId",
   "issuingCellName",
   "validFrom",
   "validTo",
   "admissionRulesId",
   "entriesAllowed"
  ],
  "properties": {
   "rightId": {
    "type": "string",
    "format": "uuid"
   },
   "ticketId": {
    "type": "string"
   },
   "guestLinkId": {
    "type": "string"
   },
   "issuingCellName": {
    "type": "string"
   },
   "mediaCodes": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "validFrom": {
    "type": "string",
    "format": "date-time"
   },
   "validTo": {
    "type": "string",
    "format": "date-time"
   },
   "admissionRulesId": {
    "type": "string",
    "format": "uuid"
   },
   "venueId": {
    "type": "string",
    "format": "uuid"
   },
   "entriesAllowed": {
    "type": "integer",
    "nullable": true
   }
  }
 },
 "Rollout": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout",
  "required": [
   "id",
   "releaseId",
   "environment",
   "status",
   "startedAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "releaseId": {
    "type": "string",
    "format": "uuid"
   },
   "environment": {
    "$ref": "#/components/schemas/EnvironmentKind"
   },
   "status": {
    "$ref": "#/components/schemas/RolloutStatus"
   },
   "cellsTotal": {
    "type": "integer"
   },
   "cellsComplete": {
    "type": "integer"
   },
   "cellsFailed": {
    "type": "integer"
   },
   "startedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pausedReason": {
    "type": "string",
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time"
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RolloutCell": {
  "type": "object",
  "x-ticvai-persistence": "control.rollout_cell",
  "description": "One cell's state within one rollout. **`rolloutId` is the row's parent**: a cell takes part in many rollouts over its life, and `skipRolloutCell` addresses `/rollouts/{rolloutId}/cells/{cellId}`, so a row keyed on the cell alone cannot say which run it belongs to or be found by that path.\n\nA migration run's per-cell rows are the same fields under a different parent, and use `MigrationRunCell`.\n",
  "required": [
   "rolloutId",
   "cellId",
   "status"
  ],
  "properties": {
   "rolloutId": {
    "type": "string",
    "format": "uuid",
    "description": "The rollout this row belongs to (`control.rollout`)."
   },
   "cellId": {
    "type": "string",
    "format": "uuid"
   },
   "cellName": {
    "type": "string"
   },
   "regionName": {
    "type": "string"
   },
   "countryCode": {
    "type": "string"
   },
   "isCanary": {
    "type": "boolean"
   },
   "wave": {
    "type": "integer"
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "running",
     "complete",
     "failed",
     "skipped",
     "rolledBack"
    ]
   },
   "fromVersion": {
    "type": "string",
    "nullable": true
   },
   "toVersion": {
    "type": "string",
    "nullable": true
   },
   "error": {
    "type": "string",
    "nullable": true
   },
   "startedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "RolloutDetail": {
  "allOf": [
   {
    "$ref": "#/components/schemas/Rollout"
   },
   {
    "type": "object",
    "x-ticvai-persistence": "none — projection over rollout and cell state",
    "properties": {
     "cells": {
      "type": "array",
      "description": "Per-cell state. \"60% complete\" says nothing about whether the failing 40% is one region or forty venues.\n",
      "items": {
       "$ref": "#/components/schemas/RolloutCell"
      }
     }
    }
   }
  ]
 },
 "RolloutStatus": {
  "type": "string",
  "enum": [
   "queued",
   "canary",
   "rolling",
   "paused",
   "complete",
   "failed",
   "rolledBack"
  ]
 },
 "SsoGroupMapping": {
  "x-ticvai-persistence": "identity.sso_group_mapping",
  "type": "object",
  "required": [
   "externalGroup",
   "roleId"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The table had no key at all — the response returned the external group, the role and the scope, which is everything a caller needs and not the row own identity.\n**(provider, external_group) is unique and would serve**, but a mapping is edited and revoked by an administrator, and **a row addressed by the values it holds cannot be corrected** — changing the group means deleting a mapping and creating another, which loses who granted it and when.\n"
   },
   "externalGroup": {
    "type": "string"
   },
   "roleId": {
    "type": "string",
    "format": "uuid"
   },
   "scopePath": {
    "type": "string",
    "description": "Scope the mapped role is granted at."
   }
  }
 },
 "SsoProtocol": {
  "type": "string",
  "enum": [
   "oidc",
   "saml2"
  ]
 },
 "SsoProviderConfig": {
  "x-ticvai-persistence": "identity.sso_provider",
  "type": "object",
  "required": [
   "id",
   "displayName",
   "protocol",
   "groupMappings"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "displayName": {
    "type": "string"
   },
   "protocol": {
    "$ref": "#/components/schemas/SsoProtocol"
   },
   "metadataUrl": {
    "type": "string",
    "nullable": true
   },
   "issuer": {
    "type": "string",
    "nullable": true
   },
   "clientId": {
    "type": "string",
    "nullable": true
   },
   "clientSecretRef": {
    "type": "string",
    "nullable": true,
    "description": "Key vault reference. The secret itself is never returned."
   },
   "groupMappings": {
    "type": "array",
    "minItems": 1,
    "description": "**A group with no mapping grants nothing.** No default role, ever — otherwise the identity provider becomes a way to mint access nobody configured.\n",
    "items": {
     "$ref": "#/components/schemas/SsoGroupMapping"
    }
   },
   "autoProvisionPrincipals": {
    "type": "boolean",
    "default": false,
    "description": "Create a principal on first successful sign-in."
   },
   "isEnforced": {
    "type": "boolean",
    "default": false
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "Subscription": {
  "x-ticvai-persistence": "subscription.contract",
  "type": "object",
  "required": [
   "tenantId",
   "planId",
   "planVersion",
   "status",
   "startsAt"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "planId": {
    "type": "string",
    "format": "uuid"
   },
   "planName": {
    "type": "string"
   },
   "planVersion": {
    "type": "string"
   },
   "status": {
    "type": "string",
    "enum": [
     "trial",
     "active",
     "pastDue",
     "cancelled",
     "expired"
    ]
   },
   "startsAt": {
    "type": "string",
    "format": "date"
   },
   "renewsAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "cancelledAt": {
    "type": "string",
    "format": "date",
    "nullable": true
   },
   "scheduledChange": {
    "type": "object",
    "nullable": true,
    "readOnly": true,
    "description": "A downgrade waiting for the next renewal (decided 28 September, audit R214 (1)). Null when none is scheduled.",
    "properties": {
     "planId": {
      "type": "string",
      "format": "uuid"
     },
     "planVersion": {
      "type": "string"
     },
     "effectiveFrom": {
      "type": "string",
      "format": "date",
      "description": "Always the `renewsAt` it was scheduled against."
     }
    }
   },
   "currentPrice": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "billingPeriod": {
    "type": "string"
   }
  }
 },
 "SuspensionMode": {
  "type": "string",
  "description": "Access validation continues under every mode. A commercial dispute must not strand guests at a gate holding valid tickets.\n",
  "enum": [
   "readOnly",
   "noNewSales",
   "fullLockout"
  ]
 },
 "Tenant": {
  "x-ticvai-persistence": "control.tenant",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "status",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "name": {
    "type": "string"
   },
   "status": {
    "$ref": "#/components/schemas/TenantStatus"
   },
   "suspensionMode": {
    "$ref": "#/components/schemas/SuspensionMode"
   },
   "suspensionReason": {
    "type": "string",
    "nullable": true
   },
   "suspensionEffectiveAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When the suspension takes, or took, effect — `suspendTenant.effectiveAt`. **A future value is a pending suspension**: the tenant stays `active` until then, and this row is the only place that says a suspension is coming."
   },
   "suspensionNoticeMessage": {
    "$ref": "#/components/schemas/LocalisedText",
    "description": "The notice shown to the tenant's users about the suspension — `suspendTenant.noticeMessage`."
   },
   "terminationScheduledAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "When `terminateTenant` started the retention window. Null when no termination is under way."
   },
   "terminationRetentionUntil": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "`terminationScheduledAt` plus the request's `retentionDays`. **Stored, not recomputed** — the day count is client-supplied and exists nowhere else, and this is the date the cells are destroyed after."
   },
   "terminationReason": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "terminationRequestedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "planName": {
    "type": "string",
    "nullable": true
   },
   "cellCount": {
    "type": "integer"
   },
   "venueCount": {
    "type": "integer"
   },
   "regionId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true,
    "description": "The tenant's home region: the `tenancy` region node whose `RegionSettings` govern tenant-wide gates, today `allowedAiResidencies` (decided 28 September, audit R203). Written by the server when the tenant's first region is created; null until then. ADM-037 reads it to show the region's residency restriction, and `ai.setAiProvider` checks against the same region.\n"
   },
   "billingEmail": {
    "type": "string"
   },
   "billingAddress": {
    "type": "string",
    "maxLength": 500,
    "nullable": true,
    "description": "Accepted by `createTenant` and `updateTenant`; stored here so the response can return what was sent."
   },
   "accountManagerPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "activatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "TenantDetail": {
  "x-ticvai-persistence": "control.tenant",
  "allOf": [
   {
    "$ref": "#/components/schemas/Tenant"
   },
   {
    "type": "object",
    "properties": {
     "subscription": {
      "$ref": "#/components/schemas/Subscription"
     },
     "cells": {
      "type": "array",
      "items": {
       "$ref": "#/components/schemas/Cell"
      }
     },
     "licences": {
      "$ref": "#/components/schemas/LicencePosition"
     }
    }
   }
  ]
 },
 "TenantStatus": {
  "type": "string",
  "enum": [
   "onboarding",
   "active",
   "suspended",
   "terminating",
   "terminated"
  ]
 },
 "UsageMetric": {
  "type": "string",
  "enum": [
   "venues",
   "workstations",
   "activeUsers",
   "devices",
   "brandedApps",
   "aiTokens",
   "apiCalls",
   "storageGb",
   "transactions",
   "guestProfiles"
  ]
 },
 "WalletAllocation": {
  "x-ticvai-persistence": "platform.wallet_authorisation",
  "type": "object",
  "required": [
   "guestLinkId",
   "mode",
   "availableAmount"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "guestLinkId": {
    "type": "string"
   },
   "mode": {
    "type": "string",
    "enum": [
     "none",
     "fixed",
     "percentageOfBalance"
    ]
   },
   "allocatedAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "drawnAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "availableAmount": {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   },
   "lastToppedUpAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "allocationCurrency": {
    "type": "string",
    "pattern": "^[A-Z]{3}$",
    "description": "**The allocation is denominated in the home currency.** A ceiling set in AED does not become a different ceiling because the guest walked into a Saudi venue — converting the limit as well as the spend is how a policy silently loosens when a rate moves."
   }
  }
 }
}
```
