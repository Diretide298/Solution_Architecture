# WS145 — Marketing CRM Configuration Reference v1.0 board 11

**10 screens · 13 operations · 33 schemas · 5 permissions**

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
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 5 permissions apply here:
  `ASSET_LIBRARY_VIEW, GUEST_MANAGE, MARKETING_MANAGE, TENANT_CONFIGURE, TENANT_PUBLISH`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-834` | Digital Experience Center | listDetail | 1 | 0 | — |
| `BO-835` | Site, Brand & Domain Setup | listDetail | 1 | 0 | — |
| `BO-836` | Design System & Components | listDetail | 1 | 0 | — |
| `BO-837` | Page & Landing Builder | listDetail | 2 | 0 | — |
| `BO-838` | Content, Media & Forms | listDetail | 2 | 0 | — |
| `BO-839` | Dynamic Product Pages | listDetail | 1 | 0 | — |
| `BO-840` | Mobile App CMS | listDetail | 1 | 0 | — |
| `BO-841` | Personalization & Localization | listDetail | 1 | 0 | — |
| `BO-842` | SEO Management | listDetail | 2 | 0 | — |
| `BO-843` | Publishing, Analytics & Audit | listDetail | 1 | 0 | — |

## Thin screens in this batch

**BO-835, BO-836, BO-837, BO-838, BO-839, BO-840, BO-841, BO-842, BO-843 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-834",
  "name": "Digital Experience Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "01",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/digital-experience-center-bo-834",
   "component": "apps/venue-management-web/src/routes/engagement-support/DigitalExperienceCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-835",
    "BO-836",
    "BO-837",
    "BO-838",
    "BO-839",
    "BO-840",
    "BO-841",
    "BO-842",
    "BO-843"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-835",
     "trigger": "Site, Brand & Domain Setup",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-836",
     "trigger": "Design System & Components",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-837",
     "trigger": "Page & Landing Builder",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-838",
     "trigger": "Content, Media & Forms",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-839",
     "trigger": "Dynamic Product Pages",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-840",
     "trigger": "Mobile App CMS",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-841",
     "trigger": "Personalization & Localization",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-842",
     "trigger": "SEO Management",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    },
    {
     "to": "BO-843",
     "trigger": "Publishing, Analytics & Audit",
     "provenance": "structural — pack board 11 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor websites, portals, mobile experiences and content health. Show sites, apps, pages, scheduled content, approvals, conversion, accessibility score and SEO health. List digital properties with environment, brand, domain, locale, status, owner and performance. Surface broken links, stale content, publishing errors, low-performing pages and compliance issues. Provide explainable AI content and SEO opportunities with drill-down to affected pages. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "filters",
     "slot": "filters",
     "components": [
      {
       "kind": "selectField",
       "label": "Configuration version",
       "operation": "getTenantConfig",
       "notes": "Sends `?version=`; defaults to live.",
       "provenance": "contract white-label.yaml GET /tenant-config"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Sites and apps",
       "columns": [
        "Sites and apps"
       ],
       "notes": "The pack asks for sites and apps; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      },
      {
       "kind": "metricTile",
       "label": "Pages",
       "columns": [
        "Pages"
       ],
       "notes": "The pack asks for pages; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      },
      {
       "kind": "metricTile",
       "label": "Scheduled content",
       "columns": [
        "Scheduled content"
       ],
       "notes": "The pack asks for scheduled content; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      },
      {
       "kind": "metricTile",
       "label": "Accessibility score",
       "columns": [
        "Accessibility score"
       ],
       "notes": "The pack asks for accessibility score; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      },
      {
       "kind": "metricTile",
       "label": "SEO health",
       "columns": [
        "SEO health"
       ],
       "notes": "The pack asks for seo health; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      },
      {
       "kind": "metricTile",
       "label": "Live configuration",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.version",
        "TenantConfig.isDraft",
        "TenantConfig.updatedAt"
       ],
       "operation": "getTenantConfig",
       "provenance": "contract white-label.yaml GET /tenant-config"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Digital properties",
       "bindsTo": "TenantConfig",
       "columns": [
        "Property",
        "Environment",
        "Brand",
        "Domain",
        "Locale",
        "Status",
        "Owner",
        "Performance",
        "TenantConfig.languages",
        "TenantConfig.isInMaintenance"
       ],
       "operation": "getTenantConfig",
       "notes": "The pack lists many properties; the tenant config describes one. Only locale and status are bound.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected property",
       "bindsTo": "TenantConfig",
       "columns": [
        "TenantConfig.tenantId",
        "TenantConfig.version",
        "TenantConfig.isDraft",
        "TenantConfig.brand",
        "TenantConfig.theme",
        "TenantConfig.header",
        "TenantConfig.navigation",
        "TenantConfig.homepage",
        "TenantConfig.languages",
        "TenantConfig.modules",
        "TenantConfig.features",
        "TenantConfig.enabledPaymentMethods",
        "TenantConfig.isInMaintenance",
        "TenantConfig.maintenanceMessage",
        "TenantConfig.updatedAt"
       ],
       "operation": "getTenantConfig",
       "provenance": "contract white-label.yaml GET /tenant-config"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The digital experience list.",
   "error": "Could not load. Names which read failed and leaves the digital experience untouched.",
   "emptyFirstRun": "No digital experience yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the digital experience are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getTenantConfig",
    "contract": "white-label",
    "purpose": "Site and tenant configuration",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-834",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-834"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Marketing_CRM_Configuration_Reference v1.0.pdf p.53; contract white-label.yaml GET /tenant-config. Pack labels with no schema field yet (shown as plain labels): Sites and apps, Pages, Scheduled content, Accessibility score, SEO health, Approvals pending, Conversion, Broken links, Stale content, Publishing errors, Low-performing pages, Property environment / domain / owner / performance.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-835",
  "name": "Site, Brand & Domain Setup",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "02",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/site-brand-domain-setup-bo-835",
   "component": "apps/venue-management-web/src/routes/engagement-support/SiteBrandDomainSetup.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure multiple white-label digital properties from one deployment. Create websites, portals, microsites and app experiences by tenant, brand, venue, destination and business unit. Configure domains, environments, logos, colors, typography, icons, headers, footers and navigation. Set locales, default language, analytics IDs, consent/cookie settings, integrations and ownership. Validate domain, certificate, branding completeness and environment promotion before go-live. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Site, Brand & Domain Setup declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "claimCustomDomain",
       "label": "Claim custom domain",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "claimCustomDomain"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The site brand domain list.",
   "error": "Could not load. Names which read failed and leaves the site brand domain untouched.",
   "emptyFirstRun": "No site brand domain yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the site brand domain are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "claimCustomDomain",
    "contract": "white-label",
    "purpose": "Site, brand and domain",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-835",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-835"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-836",
  "name": "Design System & Components",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "03",
   "page": 53
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/design-system-components-bo-836",
   "component": "apps/venue-management-web/src/routes/engagement-support/DesignSystemComponents.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Maintain reusable visual tokens and content components. Configure color, type, spacing, radius, shadow, breakpoint, transition and icon tokens by brand. Configuration Scope of Work | Version 1.0 53 Provide banner, event, ticket, membership, loyalty, gallery, video, map, form, countdown, promotion and CTA components. Define component variants, data properties, allowed placement, accessibility and responsive behavior. Version and approve changes and show every page/app experience affected before publication. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 53"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setBrandIdentity",
       "label": "Save brand identity",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setBrandIdentity"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The design system components list.",
   "error": "Could not load. Names which read failed and leaves the design system components untouched.",
   "emptyFirstRun": "No design system components yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the design system components are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setBrandIdentity",
    "contract": "white-label",
    "purpose": "Design system and components",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-836",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-836"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 53. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-837",
  "name": "Page & Landing Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "04",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/page-landing-builder-bo-837",
   "component": "apps/venue-management-web/src/routes/engagement-support/PageLandingBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Allow non-technical users to build pages and campaign landing experiences. Provide drag-and-drop sections, layer tree, reusable templates and desktop/tablet/mobile preview. Support content, product widgets, forms, countdowns, personalization, analytics tags and deep links. Configure slug, navigation, visibility, start/end schedule, campaign association and conversion goal. Validate responsive layout, required content, links, accessibility, SEO and approval before publish. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**Page & Landing Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createContentPage",
       "label": "Create content page",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listContentPages",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createContentPage"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The page landing list.",
   "error": "Could not load. Names which read failed and leaves the page landing untouched.",
   "emptyFirstRun": "No page landing yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the page landing are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createContentPage",
    "contract": "white-label",
    "purpose": "Build a page",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "listContentPages",
    "contract": "white-label",
    "purpose": "Pages published",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-837",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-837"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-838",
  "name": "Content, Media & Forms",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "05",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/content-media-forms-bo-838",
   "component": "apps/venue-management-web/src/routes/engagement-support/ContentMediaForms.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Centrally manage reusable content, assets and data-capture forms. Maintain multilingual content entries, metadata, tags, owner, status, schedule and workflow. Manage images, video, PDFs, icons, audio and documents with rights, alt text, renditions and usage references. Build forms for registration, inquiry, waiver, survey, lead and custom workflows with validation and consent. Secure submissions, route them to approved services and apply retention, export and audit controls. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createForm",
       "label": "Create form",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "searchField",
       "derived": true,
       "impliedBy": "searchMedia",
       "label": "Search",
       "notes": "A search that returns nothing must say so differently from a search not yet run."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createForm"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The content media forms list.",
   "error": "Could not load. Names which read failed and leaves the content media forms untouched.",
   "emptyFirstRun": "No content media forms yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the content media forms are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createForm",
    "contract": "marketing-crm",
    "purpose": "Forms on a page",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "searchMedia",
    "contract": "assets",
    "purpose": "Media to place",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-838",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-838"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-839",
  "name": "Dynamic Product Pages",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "06",
   "page": 54
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/dynamic-product-pages-bo-839",
   "component": "apps/venue-management-web/src/routes/engagement-support/DynamicProductPages.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Publish live transactional content directly from TICVAI product services. Configure dynamic pages/widgets for events, attractions, tickets, capacity, pricing and availability. Display membership benefits/prices, loyalty tiers/rewards, wallet offers, resources, F&B and retail products. Define filters, sorting, related content, upsell/cross-sell, sold-out fallback and cache/refresh behavior. Ensure displayed price, inventory, eligibility and purchase actions come from authoritative shared engines. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 54",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 54"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "createContentBlock",
       "label": "Create content block",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createContentBlock"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The dynamic product pages list.",
   "error": "Could not load. Names which read failed and leaves the dynamic product pages untouched.",
   "emptyFirstRun": "No dynamic product pages yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the dynamic product pages are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createContentBlock",
    "contract": "white-label",
    "purpose": "Dynamic product blocks",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-839",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-839"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 54. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-840",
  "name": "Mobile App CMS",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "07",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/mobile-app-cms-bo-840",
   "component": "apps/venue-management-web/src/routes/engagement-support/MobileAppCms.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage guest mobile-app content and navigation without releasing code. Configure home-screen layout, menus, banners, announcements, quick actions, widgets and featured content. Define deep links, audience visibility, language, schedule, app version and offline/cache behavior. Preview content for supported device sizes and validate inaccessible, missing or unsupported components. Publish through approval and staged rollout with version, rollback and analytics tracking. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setHomepageLayout",
       "label": "Save homepage layout",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setHomepageLayout"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The mobile app cms list.",
   "error": "Could not load. Names which read failed and leaves the mobile app cms untouched.",
   "emptyFirstRun": "No mobile app cms yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the mobile app cms are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setHomepageLayout",
    "contract": "white-label",
    "purpose": "Mobile app content",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-840",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-840"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-841",
  "name": "Personalization & Localization",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "08",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/personalization-localization-bo-841",
   "component": "apps/venue-management-web/src/routes/engagement-support/PersonalizationLocalization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Deliver relevant content variants under clear governance. Build visibility and content rules by segment, profile, language, loyalty, membership, geography and behavior. Configure variant priority, conflict resolution, fallback and real-guest/test-profile preview. Use AI for draft content and translation with glossary, brand tone, protected terms and manual review. Enforce consent and minimum-audience rules and audit the rule/version that produced each experience. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setLocalizationBrandingCustomer",
       "label": "Save",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setLocalizationBrandingCustomer"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The personalization localization list.",
   "error": "Could not load. Names which read failed and leaves the personalization localization untouched.",
   "emptyFirstRun": "No personalization localization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the personalization localization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setLocalizationBrandingCustomer",
    "contract": "marketing-crm",
    "purpose": "Personalisation and localisation",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-841",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-841"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 10 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-842",
  "name": "SEO Management",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "09",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/seo-management-bo-842",
   "component": "apps/venue-management-web/src/routes/engagement-support/SeoManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure technical and content SEO across dynamic and authored pages. Manage titles, descriptions, canonical URLs, Open Graph, keywords, slugs, aliases and 301/302 redirects. Generate XML sitemaps, hreflang and Schema.org markup for events, products, reviews, FAQs and organizations. Analyze readability, missing metadata, duplicates, broken links, crawl/index issues and internal- link opportunities. Provide AI recommendations with review and report ranking, organic traffic, conversion and revenue. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "setSeoMetadata",
       "label": "Save SEO metadata",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "setSeoMetadata"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The seo list.",
   "error": "Could not load. Names which read failed and leaves the seo untouched.",
   "emptyFirstRun": "No seo yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the seo are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "setSeoMetadata",
    "contract": "marketing-crm",
    "purpose": "SEO metadata",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "createUrlRedirect",
    "contract": "marketing-crm",
    "purpose": "Redirects",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-842",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-842"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "BO-843",
  "name": "Publishing, Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "11",
   "number": "10",
   "page": 55
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/publishing-analytics-audit-bo-843",
   "component": "apps/venue-management-web/src/routes/engagement-support/PublishingAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-834"
   ],
   "exitTo": [
    "BO-834"
   ],
   "transitions": [
    {
     "to": "BO-834",
     "trigger": "Back to Digital Experience Center",
     "provenance": "structural — pack board 11 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Govern content release and measure digital-experience performance. Support draft, review, approval, scheduled publication, expiration, environment promotion and emergency unpublish. Maintain versions, visual/text comparison, rollback, accessibility validation and dependency checks. Configuration Scope of Work | Version 1.0 55 Report page/app views, engagement, conversion, product sales, search behavior and personalized- variant results. Audit authored and AI-generated content, translations, approvals, publications, rollbacks and administrative actions. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 56 Board 12 - Digital Waivers & Signature Management Figure 12. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 57",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 55"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "primaryButton",
       "derived": true,
       "impliedBy": "publishTenantConfig",
       "label": "Publish tenant config",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "publishTenantConfig"
      },
      {
       "kind": "publishGate",
       "label": "What publishing changes",
       "notes": "**Goes live on the tenant’s own domains**, for every guest, at once. The previous version stays restorable.",
       "provenance": "authored — required by check-screens, 19 September 2026"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The publishing analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the publishing analytics audit untouched.",
   "emptyFirstRun": "No publishing analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the publishing analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "publishTenantConfig",
    "contract": "white-label",
    "purpose": "Publish",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-843",
   "workshopBoard": "wireframes/WS80 Marketing CRM Configuration Reference v1.0 Board 11.dc.html#bo-843"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 55. 0 of 0 labels bound to a contract property; 0 of 28 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "_platform": {
   "code": "P08",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Management",
   "name": "Venue Management — Back Office",
   "offlineCapable": false,
   "app": "venue-management-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P12",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "claimCustomDomain": {
  "method": "POST",
  "path": "/tenant-domains",
  "contract": "white-label",
  "summary": "Claim a domain and get a verification token",
  "permission": "TENANT_CONFIGURE",
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
  "responds": "CustomDomain"
 },
 "createContentBlock": {
  "method": "POST",
  "path": "/content-blocks",
  "contract": "white-label",
  "summary": "Author a block of content",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ContentBlock",
  "responds": "ContentBlock"
 },
 "createContentPage": {
  "method": "POST",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "Create a content page",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "ContentPage",
  "responds": "ContentPage"
 },
 "createForm": {
  "method": "POST",
  "path": "/forms",
  "contract": "marketing-crm",
  "summary": "Define a waiver, survey or capture form",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "FormDefinition",
  "responds": "FormDefinition"
 },
 "createUrlRedirect": {
  "method": "POST",
  "path": "/seo-redirects",
  "contract": "marketing-crm",
  "summary": "301, 302 and custom redirects",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "UrlRedirect",
  "responds": "UrlRedirect"
 },
 "getTenantConfig": {
  "method": "GET",
  "path": "/tenant-config",
  "contract": "white-label",
  "summary": "Full working configuration",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "version",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "TenantConfig"
 },
 "listContentPages": {
  "method": "GET",
  "path": "/tenant-config/pages",
  "contract": "white-label",
  "summary": "List custom content pages",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "status",
    "in": "query",
    "required": null
   },
   {
    "name": "categoryCode",
    "in": "query",
    "required": null
   },
   {
    "name": "slug",
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
 "publishTenantConfig": {
  "method": "POST",
  "path": "/tenant-config/publish",
  "contract": "white-label",
  "summary": "Publish the working draft",
  "permission": "TENANT_PUBLISH",
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
  "responds": "ConfigVersion"
 },
 "searchMedia": {
  "method": "GET",
  "path": "/media",
  "contract": "assets",
  "summary": "Search the asset library",
  "permission": "ASSET_LIBRARY_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kind",
    "in": "query",
    "required": null
   },
   {
    "name": "tag",
    "in": "query",
    "required": null
   },
   {
    "name": "collectionId",
    "in": "query",
    "required": null
   },
   {
    "name": "venueId",
    "in": "query",
    "required": null
   },
   {
    "name": "search",
    "in": "query",
    "required": null
   },
   {
    "name": "unusedOnly",
    "in": "query",
    "required": null
   },
   {
    "name": "rightsExpiringWithinDays",
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
 "setBrandIdentity": {
  "method": "PUT",
  "path": "/tenant-config/brand",
  "contract": "white-label",
  "summary": "Set logo, favicon and splash",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "BrandIdentity",
  "responds": "BrandIdentity"
 },
 "setHomepageLayout": {
  "method": "PUT",
  "path": "/tenant-config/homepage",
  "contract": "white-label",
  "summary": "Set homepage section order",
  "permission": "TENANT_CONFIGURE",
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
  "requestBody": "HomepageLayout",
  "responds": "HomepageLayout"
 },
 "setLocalizationBrandingCustomer": {
  "method": "PUT",
  "path": "/localization-branding-customer",
  "contract": "marketing-crm",
  "summary": "Set a waiver version's languages, branding and channels",
  "permission": "GUEST_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "LocalizationBrandingCustomerExperienceConfigurationInput",
  "responds": "LocalizationBrandingCustomerExperienceConfigurationView"
 },
 "setSeoMetadata": {
  "method": "PUT",
  "path": "/seo-metadata",
  "contract": "marketing-crm",
  "summary": "Titles, descriptions, canonicals and hreflang",
  "permission": "MARKETING_MANAGE",
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
  "requestBody": "SeoMetadata",
  "responds": "SeoMetadata"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccessibilitySettings": {
  "type": "object",
  "description": "BL-065, 2.1.27. **POS and kiosk accessibility, which is a legal obligation in most jurisdictions and was unstated.**\n**A kiosk is the hard case.** A guest with low vision using a website brings their own assistive technology; a guest at a kiosk gets whatever the kiosk offers, so the settings have to be on the device rather than in the browser.\n",
  "properties": {
   "largeTextAvailable": {
    "type": "boolean",
    "default": true
   },
   "highContrastAvailable": {
    "type": "boolean",
    "default": true
   },
   "simplifiedNavigationAvailable": {
    "type": "boolean",
    "default": true
   },
   "screenReaderSupported": {
    "type": "boolean",
    "default": true
   },
   "reachableHeightModeAvailable": {
    "type": "boolean",
    "default": false,
    "description": "**Moves the interface to the lower half of the screen** for a guest using a wheelchair. A kiosk mounted at standing height is unusable otherwise, and no software setting fixes the mounting — this is the mitigation.\n"
   },
   "sessionTimeoutMultiplier": {
    "type": "number",
    "default": 1,
    "description": "**Timeouts are an accessibility barrier nobody counts.** A guest who needs three times as long to read a screen should not lose their basket to a 90-second inactivity timer.\n"
   }
  }
 },
 "AppAvailability": {
  "type": "string",
  "description": "**The sold-out or closed signal (decided 28 September, audit R073).** `open` is the normal state. `soldOut` shows WEB-029's sold-out state across the app while browsing still works; `closed` shows the closed state (a weather closure, a private event). Neither refuses a request on its own: it is what the guest is told, and a sale is still refused by availability where it applies. Set with `setMaintenanceMode`.\n",
  "enum": [
   "open",
   "soldOut",
   "closed"
  ],
  "default": "open"
 },
 "AppIcons": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "sourceAssetRef",
   "changeScope"
  ],
  "properties": {
   "sourceAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The `MediaAsset` id of the 1024×1024 source."
   },
   "derived": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Generated by `setAppIcons` from the source, one entry per platform and size — the iOS and Android store sets and the web favicons listed on `setAppIcons` (audit R163).",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string",
       "enum": [
        "ios",
        "android",
        "web"
       ]
      },
      "size": {
       "type": "string"
      },
      "assetRef": {
       "type": "string",
       "format": "uuid"
      }
     }
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` — icons are baked into the binary."
   },
   "liveVersion": {
    "type": "string",
    "nullable": true,
    "readOnly": true,
    "description": "Icon currently shipped. Differs from the draft until the next release."
   },
   "requiresRebuild": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "True while the draft's source differs from the icon in `liveVersion`."
   }
  }
 },
 "BookingFlowConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "description": "**Set per tenant, with a per-venue override (decided 29 September, rev 3 CFG-11).** One tenant with several venues (the Kids Club branches, Coastal Aqua beside Union Arena) needs them to differ. The settings in force at a venue are the tenant's, with that venue's entry in `venueOverrides` laid over them field by field. The guest app resolves them for the venue the guest picked (audit R267); `effectiveForVenueId` on `getBookingFlowConfig` returns them resolved.\n",
  "allOf": [
   {
    "$ref": "#/components/schemas/BookingFlowSettings"
   },
   {
    "type": "object",
    "properties": {
     "venueOverrides": {
      "type": "array",
      "maxItems": 200,
      "default": [],
      "description": "Per-venue overrides, at most one per venue. A `venueId` that is not one of the tenant's active venues, or appears twice, is refused with 400. An override for a venue later closed is kept and has no effect.",
      "items": {
       "$ref": "#/components/schemas/BookingFlowVenueOverride"
      }
     }
    }
   }
  ]
 },
 "BrandIdentity": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "description": "Every `*AssetRef` here is a `MediaAsset` id from the `assets` library (`createUpload` then `completeUpload`), PNG or SVG and at most 2 MB (decided 28 September, audit R270).\n",
  "required": [
   "logoAssetRef"
  ],
  "properties": {
   "logoAssetRef": {
    "type": "string",
    "format": "uuid",
    "description": "The primary logo."
   },
   "logoDarkAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "Used on dark backgrounds. Falls back to the primary logo."
   },
   "logoVariant": {
    "type": "string",
    "enum": [
     "light",
     "dark",
     "duotone"
    ],
    "default": "light",
    "description": "**Which lockup sits in the nav bar, and whose colours drive the theme (decided 29 September, rev 3 CFG-4).** `light` uses `logoAssetRef`, `dark` uses `logoDarkAssetRef` (falling back to the primary logo), and `duotone` the two-colour reading of the primary logo.\n"
   },
   "faviconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "The browser tab icon for the guest web app."
   },
   "splashImageAssetRefs": {
    "type": "array",
    "description": "Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163).",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "splashDurationSeconds": {
    "type": "integer",
    "minimum": 0,
    "maximum": 10,
    "default": 3
   },
   "splashBackgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "showLoadingIndicator": {
    "type": "boolean",
    "default": true
   },
   "splashChangeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Always `buildTime` for native apps. The guest web app takes a splash change at the publish, with no build (audit R163)."
   }
  }
 },
 "ChangeScope": {
  "type": "string",
  "description": "Whether a change reaches guests on publish or needs a store release.\n",
  "enum": [
   "runtime",
   "buildTime"
  ]
 },
 "ConfigVersion": {
  "x-ticvai-persistence": "whitelabel.config_version",
  "type": "object",
  "required": [
   "version",
   "publishedAt",
   "publishedByPrincipalId",
   "note",
   "isCurrent"
  ],
  "properties": {
   "version": {
    "type": "string"
   },
   "publishedAt": {
    "type": "string",
    "format": "date-time"
   },
   "publishedByPrincipalId": {
    "type": "string",
    "format": "uuid"
   },
   "publishedByName": {
    "type": "string"
   },
   "note": {
    "type": "string"
   },
   "isCurrent": {
    "type": "boolean"
   },
   "scheduledFor": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "contentHash": {
    "type": "string"
   },
   "pendingBuildTimeChanges": {
    "type": "array",
    "description": "Changes in this version that will not reach guests until the next store release. Surfaced at publish so nobody expects a new icon tomorrow.\n",
    "items": {
     "type": "object",
     "properties": {
      "area": {
       "type": "string"
      },
      "description": {
       "type": "string"
      },
      "platforms": {
       "type": "array",
       "items": {
        "type": "string",
        "enum": [
         "ios",
         "android",
         "web"
        ]
       }
      }
     }
    }
   },
   "snapshot": {
    "type": "object",
    "additionalProperties": true,
    "readOnly": true,
    "description": "**What this version contained.** The working draft exactly as published, in the shape `getTenantConfig` returns (`TenantConfig`) — so `restoreConfigVersion` has something to copy back and `diffConfigVersion` something to compare. Deliberately an open object here: its shape is `TenantConfig`, and a `$ref` would make it a key to a `tenant_config` row rather than a copy. Written once by `publishTenantConfig` and never changed. Left out of `listConfigVersions` items; a version's content is read with `getTenantConfig?version=`.\n"
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentBlock": {
  "type": "object",
  "x-ticvai-persistence": "control.content_block",
  "description": "BL-172. **`white-label` is excellent as a configuration model and is not an authoring surface.** `HomepageLayout` with ordered sections, `Banner`, `PromoBlock` and `ContentPage` describe what a venue has chosen; **none of them lets a marketer write something new without a developer.**\nA block is a piece of authored content with a type, a body and a schedule. **The page builder is a frontend over this**, the same way the venue map's canvas is a frontend over its graph.\n",
  "required": [
   "id",
   "kind",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "pageId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "kind": {
    "type": "string",
    "enum": [
     "richText",
     "image",
     "video",
     "gallery",
     "cta",
     "faq",
     "form",
     "embed",
     "productGrid",
     "countdown",
     "testimonial"
    ]
   },
   "position": {
    "type": "integer"
   },
   "body": {
    "type": "object",
    "additionalProperties": true,
    "description": "Typed by `kind`, and validated against the block's own schema at save."
   },
   "localeVariants": {
    "type": "object",
    "additionalProperties": true,
    "description": "**Per-locale bodies, not per-locale pages.** A venue running Arabic and English should not maintain two page trees that drift — the structure is shared and the words are not.\n"
   },
   "status": {
    "type": "string",
    "readOnly": true,
    "description": "Created as `draft`; moved by `publishContentBlock` and the `publishAt`/`expireAt` timer (`states/content-block.yaml`), never by the body of a create.",
    "enum": [
     "draft",
     "scheduled",
     "published",
     "expired",
     "archived"
    ]
   },
   "publishAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Content scheduling, which the configuration model had no room for.** A seasonal banner that needs somebody awake at midnight is the same defect `Product.onSaleFrom` fixed.\n"
   },
   "expireAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "audienceSegmentId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "**Personalisation, evaluated at render.** A block shown only to members, or only to first-time visitors. Null shows it to everybody, which is what every block does today.\n"
   },
   "approvedByPrincipalId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentPage": {
  "x-ticvai-persistence": "whitelabel.content_page",
  "type": "object",
  "required": [
   "id",
   "slug",
   "title",
   "body",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "slug": {
    "type": "string",
    "pattern": "^[a-z0-9-]+$"
   },
   "title": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "body": {
    "$ref": "#/components/schemas/LocalisedRichText"
   },
   "isEnabled": {
    "type": "boolean",
    "default": true,
    "description": "BL-005. **Enablement is not publication.** A published page that is disabled exists, keeps its URL and its history, and does not render — which is what a tenant wants when a section is seasonal.\n**Unpublishing loses the version; disabling does not.** Collapsing them means a venue turning off its water-park section for winter has to republish it every spring.\n"
   },
   "status": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ContentStatus"
     }
    ],
    "readOnly": true,
    "description": "Created as `draft`, published by `publishTenantConfig`, archived through `updateContentPage` (`states/content.yaml`)."
   },
   "iconAssetRef": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "categoryCode": {
    "type": "string",
    "nullable": true
   },
   "sortOrder": {
    "type": "integer"
   },
   "isReferenced": {
    "type": "boolean",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "True when navigation or the homepage links to this page. Blocks deletion. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "ContentStatus": {
  "type": "string",
  "enum": [
   "draft",
   "published",
   "archived"
  ]
 },
 "CustomDomain": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.custom_domain",
  "description": "24 August. **`ADM-017 Domain & Certificate Management` declared 41 operations and not one of them was about a domain** — it carried the same bulk-attached set as every other white-label screen, and **no domain or certificate operation existed anywhere in 1,010.**\nA white-label platform whose tenants cannot use their own domain is a white-label platform in name only.\n**Verification before issuance, always.** A certificate issued for a domain the tenant does not control is a certificate issued to whoever asked.\n",
  "required": [
   "id",
   "tenantId",
   "hostname",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "hostname": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "guestWeb",
     "guestApp",
     "partnerPortal",
     "developerPortal"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "pending",
     "verifying",
     "verified",
     "issuing",
     "active",
     "failed",
     "expired",
     "revoked"
    ]
   },
   "verificationMethod": {
    "type": "string",
    "enum": [
     "dnsTxt",
     "cname",
     "httpFile"
    ]
   },
   "verificationToken": {
    "type": "string",
    "readOnly": true
   },
   "verificationRecord": {
    "type": "object",
    "readOnly": true,
    "description": "**The record the tenant must publish**, which `claimCustomDomain` promises and the claim had nowhere to hold. Set when the claim is made, from `hostname`, `verificationMethod` and `verificationToken`: a TXT record for `dnsTxt`, a CNAME for `cname`, and for `httpFile` the URL path to serve and the file's content.\n",
    "required": [
     "type",
     "name",
     "value"
    ],
    "properties": {
     "type": {
      "type": "string",
      "enum": [
       "TXT",
       "CNAME",
       "httpFile"
      ]
     },
     "name": {
      "type": "string",
      "description": "The DNS name to create, or for `httpFile` the URL path on `hostname`."
     },
     "value": {
      "type": "string",
      "description": "The record's value, CNAME target or file content."
     }
    }
   },
   "certificateExpiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "**Renewal is a job, not a reminder.** A certificate that expires on a Saturday takes a tenant's storefront down, and nobody reads a reminder email on a Saturday.\n"
   },
   "lastCheckedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "failureReason": {
    "type": "string",
    "nullable": true
   }
  }
 },
 "FeatureToggle": {
  "x-ticvai-persistence": "whitelabel.feature_toggle",
  "type": "object",
  "required": [
   "featureKey",
   "isEnabled",
   "changeScope"
  ],
  "properties": {
   "featureKey": {
    "allOf": [
     {
      "$ref": "#/components/schemas/FeatureKey"
     }
    ],
    "description": "`guestCheckout` is **off by default** (decided 17 September 2026, matrix 2.6.28, placement settled by [ADR-0045](../../docs/adr/0045-every-order-carries-a-proven-contact.md) 18 September): **the venue sets this from the configuration menu**, and it decides which routes the checkout page offers — off, the guest signs in verified at checkout; on, a guest may also check out without an account after proving their contact with a one-time code. **It gates checkout, never the cart.** The kiosk is not governed by it. Rule on `identity` `verifyGuestEmail`.\n"
   },
   "displayName": {
    "type": "string"
   },
   "isEnabled": {
    "type": "boolean"
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "description": "Wallet and payment integrations are `buildTime` on native apps — enabling one needs a release, not a publish.\n"
   },
   "requiresConfiguration": {
    "type": "boolean",
    "description": "True where the feature needs credentials or setup elsewhere first."
   }
  }
 },
 "FontConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryLatin"
  ],
  "properties": {
   "primaryLatin": {
    "type": "string"
   },
   "primaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required when `ar` is among the tenant's languages (audit R163). A Latin face alone leaves Arabic in a system fallback that will not match.\n"
   },
   "secondaryLatin": {
    "type": "string",
    "nullable": true
   },
   "secondaryArabic": {
    "type": "string",
    "nullable": true,
    "description": "Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163)."
   },
   "customFontAssetRefs": {
    "type": "array",
    "description": "Uploaded font files, as `MediaAsset` ids.",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "changeScope": {
    "allOf": [
     {
      "$ref": "#/components/schemas/ChangeScope"
     }
    ],
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "Custom font files are `buildTime`; selecting a bundled face is `runtime`."
   }
  }
 },
 "FooterConfig": {
  "type": "object",
  "x-ticvai-persistence": "whitelabel.footer_config + whitelabel.footer_config_column + whitelabel.footer_config_social_link",
  "description": "BL-002. **`setHeader` and `HeaderConfig` exist and the footer does not**, which looked like symmetry until you notice it is not: **a header is chrome and a footer is a link surface.**\nA footer carries the legal links — terms, privacy, accessibility statement, cookie preferences — and **those are the ones a regulator checks.** Treating it as a mirror of the header would have given it a logo and no way to reach a privacy notice.\n**Where it is stored.** `legalLinks` and `copyrightText` are columns of `whitelabel.footer_config`; each entry of `columns` is a `whitelabel.footer_config_column` row and each entry of `socialLinks` a `whitelabel.footer_config_social_link` row. Part of the working draft (see the header). **In the tenant's own database, not the control plane (decided 28 September, audit R163)**: it moved from `control.footer_config` and its two child tables.\n",
  "required": [
   "id",
   "scopePath"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "The partition key (ADR-0005), written at `tenant` scope by the server."
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "heading": {
       "type": "string"
      },
      "links": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "label": {
          "type": "string"
         },
         "url": {
          "type": "string"
         },
         "opensCookiePreferences": {
          "type": "boolean",
          "default": false
         }
        }
       }
      }
     }
    }
   },
   "legalLinks": {
    "type": "object",
    "description": "**Required links, held separately from the free-form columns** — a tenant reorganising their footer must not be able to remove the privacy notice by accident.\n",
    "properties": {
     "termsUrl": {
      "type": "string"
     },
     "privacyUrl": {
      "type": "string"
     },
     "accessibilityUrl": {
      "type": "string",
      "nullable": true
     },
     "cookiePolicyUrl": {
      "type": "string",
      "nullable": true
     }
    }
   },
   "copyrightText": {
    "type": "string"
   },
   "socialLinks": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "platform": {
       "type": "string"
      },
      "url": {
       "type": "string"
      }
     }
    }
   }
  }
 },
 "FormDefinition": {
  "type": "object",
  "x-ticvai-persistence": "marketing.form_definition + marketing.form_definition_field",
  "description": "CF-129, CL-04. **A waiver, a survey and a data-capture form are one mechanism.**\nA waiver is this form with a signature. A survey is this form with a scale. A demographic capture is this form at the point of sale. They were raised as three separate gaps and share every part: field configuration, conditional display, versioning, an acceptance record and a stored artefact.\n**Three implementations would drift on the version rule first.** A waiver signed against version 3 must stay bound to version 3, and that is the same requirement a survey has when question wording changes mid-campaign — **an NPS score means nothing if you cannot say which question produced it.**\n",
  "required": [
   "id",
   "name",
   "kind",
   "version",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "name": {
    "type": "string"
   },
   "kind": {
    "type": "string",
    "enum": [
     "waiver",
     "survey",
     "dataCapture",
     "consentForm",
     "incidentReport",
     "registration"
    ]
   },
   "version": {
    "readOnly": true,
    "type": "integer",
    "description": "**Set by the server** — 1 on `createForm`, the next number on every change. **Immutable once anything is submitted against it.** A change creates a new version, and the old one stays readable forever — 2.15.13 requires the exact accepted version retained, which is legal evidence rather than a nicety.\n"
   },
   "fields": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FormField"
    }
   },
   "requiresSignature": {
    "type": "boolean",
    "default": false,
    "description": "**What makes it a waiver.** And 2.15.9 makes ticket issuance conditional on one, which puts this in the purchase path rather than beside it.\n"
   },
   "signatureKind": {
    "type": "string",
    "enum": [
     "drawn",
     "typed",
     "checkbox",
     "none"
    ],
    "default": "none"
   },
   "scoreScale": {
    "type": "string",
    "nullable": true,
    "enum": [
     "nps",
     "csat",
     "ces",
     "likert5",
     "likert7",
     "stars"
    ],
    "description": "**What makes it a survey.** Named rather than free-form because a score whose scale is unknown cannot be compared to last quarter's.\n"
   },
   "appliesToProductIds": {
    "type": "array",
    "items": {
     "type": "string",
     "format": "uuid"
    }
   },
   "validForMonths": {
    "type": "integer",
    "nullable": true,
    "description": "**How long an acceptance lasts.** A waiver signed last summer may or may not still hold, and 2.15.x asks for a returning participant not to sign again — which only works if the expiry is stated.\n"
   },
   "minimumAge": {
    "type": "integer",
    "nullable": true
   },
   "requiresGuardianForMinors": {
    "type": "boolean",
    "default": true,
    "description": "**A minor cannot waive their own rights.** A guardian signs, and the record has to name them — an unsigned or self-signed minor waiver is worth nothing at the moment it matters.\n"
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "published",
     "superseded",
     "retired"
    ]
   },
   "legalReviewedBy": {
    "type": "string",
    "nullable": true
   },
   "legalReviewedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "FormField": {
  "type": "object",
  "description": "One field. **Conditional display is the shared requirement** — a survey branching on an answer and a waiver revealing a medical question on a yes are the same mechanism.\n",
  "required": [
   "key",
   "label",
   "type"
  ],
  "properties": {
   "key": {
    "type": "string"
   },
   "label": {
    "type": "string"
   },
   "labelLocalised": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "type": {
    "type": "string",
    "enum": [
     "text",
     "longText",
     "number",
     "date",
     "select",
     "multiSelect",
     "boolean",
     "scale",
     "signature",
     "file",
     "phone",
     "email"
    ]
   },
   "options": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "isRequired": {
    "type": "boolean",
    "default": false
   },
   "isPersonalData": {
    "type": "boolean",
    "default": false,
    "description": "**Marked at the field, because retention is decided at the field.** A survey answer and a medical condition on the same form have different lifetimes, and a form-level flag makes the whole thing as sensitive as its most sensitive field.\n"
   },
   "consentPurposeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "showWhen": {
    "type": "object",
    "nullable": true,
    "properties": {
     "field": {
      "type": "string"
     },
     "equals": {
      "type": "string"
     }
    }
   }
  }
 },
 "HeaderConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "layout"
  ],
  "properties": {
   "layout": {
    "type": "string",
    "enum": [
     "logoLeft",
     "logoCentre",
     "logoWithMenu"
    ]
   },
   "showLogo": {
    "type": "boolean",
    "default": true
   },
   "showMenu": {
    "type": "boolean",
    "default": true
   },
   "showNotifications": {
    "type": "boolean",
    "default": true
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   }
  }
 },
 "HomepageLayout": {
  "x-ticvai-persistence": "whitelabel.homepage_section",
  "type": "object",
  "required": [
   "sections"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "sections": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "kind",
      "sortOrder",
      "isVisible"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "kind": {
       "$ref": "#/components/schemas/HomepageSectionKind"
      },
      "title": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isVisible": {
       "type": "boolean"
      },
      "contentPageId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "maxItems": {
       "type": "integer",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "HomepageSectionKind": {
  "type": "string",
  "description": "**Which module each section needs, proposed, client to correct (decided 28 September, audit R163).** `tickets` needs `ticketsAndBooking`; `whatsOn` needs `events`; `attractions` needs `attractions`; `membership` needs `membership`; `dining` needs `diningAndFnb`; `shop` needs `shop`; `map` needs `map`. `heroBanner`, `quickActions`, `promotions`, `customContent` and `spacer` need no module. `setHomepageLayout` refuses a visible section whose module is not enabled, and `setModuleEnablement` refuses to disable a module a section still needs.\n",
  "enum": [
   "heroBanner",
   "quickActions",
   "tickets",
   "whatsOn",
   "attractions",
   "membership",
   "dining",
   "shop",
   "promotions",
   "map",
   "customContent",
   "spacer"
  ]
 },
 "LanguageConfig": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "languages",
   "defaultLanguage"
  ],
  "properties": {
   "languages": {
    "type": "array",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "defaultLanguage": {
    "type": "string",
    "pattern": "^[a-z]{2}$"
   },
   "rtlLanguages": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onRead",
    "description": "The enabled languages written right to left — those whose Unicode CLDR character order is `right-to-left` (Arabic, `ar`, among them). Not configured; it follows from `languages`.",
    "items": {
     "type": "string",
     "pattern": "^[a-z]{2}$"
    }
   },
   "translationGaps": {
    "type": "array",
    "readOnly": true,
    "description": "Content lacking a version in an enabled language.",
    "items": {
     "type": "object",
     "properties": {
      "language": {
       "type": "string"
      },
      "missingCount": {
       "type": "integer"
      },
      "areas": {
       "type": "array",
       "items": {
        "type": "string"
       }
      }
     }
    }
   }
  }
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalizationBrandingCustomerExperienceConfigurationInput": {
  "description": "The request body of `setLocalizationBrandingCustomer`, the record itself; read-only properties are ignored.",
  "allOf": [
   {
    "$ref": "#/components/schemas/LocalizationBrandingCustomerExperienceConfigurationView"
   }
  ]
 },
 "LocalizationBrandingCustomerExperienceConfigurationView": {
  "type": "object",
  "x-ticvai-persistence": "marketing.waiver_localisation",
  "description": "Languages, branding and channels of one waiver version (pack 11.1.9), keyed on `formId` + `formVersion`.",
  "required": [
   "formId",
   "formVersion",
   "sourceLanguage",
   "languages"
  ],
  "properties": {
   "formId": {
    "type": "string",
    "format": "uuid"
   },
   "formVersion": {
    "type": "integer",
    "minimum": 1
   },
   "sourceLanguage": {
    "type": "string",
    "maxLength": 10,
    "description": "The language the legal text is written and reviewed in."
   },
   "languages": {
    "type": "array",
    "minItems": 1,
    "description": "Every language the version is offered in, the source language included. Arabic renders right to left.",
    "items": {
     "type": "object",
     "required": [
      "language",
      "required",
      "translationStatus",
      "approvalStatus"
     ],
     "properties": {
      "language": {
       "type": "string",
       "maxLength": 10
      },
      "required": {
       "type": "boolean",
       "description": "Publication waits for this language's approval."
      },
      "translationStatus": {
       "type": "string",
       "enum": [
        "notStarted",
        "aiDrafted",
        "inTranslation",
        "inReview",
        "complete"
       ]
      },
      "translatorUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "reviewerUserId": {
       "type": "string",
       "format": "uuid",
       "nullable": true
      },
      "approvalStatus": {
       "type": "string",
       "enum": [
        "pending",
        "approved",
        "rejected"
       ]
      },
      "lastUpdated": {
       "type": "string",
       "format": "date-time",
       "readOnly": true
      }
     }
    }
   },
   "branding": {
    "type": "object",
    "properties": {
     "brandLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "venueLogoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     },
     "themeId": {
      "type": "string",
      "nullable": true,
      "description": "The white-label theme it takes colours and typography from."
     },
     "header": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "footer": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "customerInstructions": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "confirmationMessage": {
      "$ref": "#/components/schemas/LocalisedText"
     },
     "supportEmail": {
      "type": "string",
      "format": "email",
      "nullable": true
     },
     "supportPhone": {
      "type": "string",
      "maxLength": 30,
      "nullable": true
     }
    }
   },
   "channels": {
    "type": "array",
    "items": {
     "type": "string",
     "enum": [
      "b2cWeb",
      "mobileApp",
      "emailLink",
      "qrLink",
      "kiosk",
      "posFrontDesk",
      "groupPortal"
     ]
    },
    "description": "Where the waiver is offered; every channel renders the same version and rules."
   },
   "scopePath": {
    "type": "string",
    "readOnly": true,
    "description": "**The partition key** (ADR-0005)."
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true
   }
  }
 },
 "MinimumAppVersion": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "**The oldest guest app build still allowed to run (decided 28 September, audit R073).** A guest app whose own version is below the one for its platform shows the forced-upgrade screen (GST-047) and nothing else. Null, or a platform left null, forces nothing. Live at once through `setMaintenanceMode`, because an upgrade that must wait for a publish is not forced.\n",
  "properties": {
   "ios": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   },
   "android": {
    "type": "string",
    "nullable": true,
    "pattern": "^\\d+\\.\\d+\\.\\d+$"
   }
  }
 },
 "ModuleEnablement": {
  "x-ticvai-persistence": "whitelabel.module_enablement",
  "type": "object",
  "required": [
   "moduleKey",
   "isLicensed",
   "isEnabled"
  ],
  "properties": {
   "moduleKey": {
    "$ref": "#/components/schemas/ModuleKey"
   },
   "displayName": {
    "type": "string"
   },
   "isLicensed": {
    "type": "boolean",
    "description": "From the tenant's subscription. False makes enablement impossible."
   },
   "isEnabled": {
    "type": "boolean"
   },
   "referencedBy": {
    "type": "array",
    "readOnly": true,
    "x-ticvai-derived": "onWrite",
    "description": "Navigation items and homepage sections pointing at this module. Maintained by `setNavigation` and `setHomepageLayout` in the same transaction as the links they write.",
    "items": {
     "type": "string"
    }
   }
  }
 },
 "NavigationConfig": {
  "x-ticvai-persistence": "whitelabel.navigation_item",
  "type": "object",
  "required": [
   "kind",
   "items"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true,
    "description": "**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"
   },
   "kind": {
    "type": "string",
    "enum": [
     "bottomNavigation",
     "drawer",
     "tabs"
    ]
   },
   "items": {
    "type": "array",
    "maxItems": 12,
    "items": {
     "type": "object",
     "required": [
      "label",
      "target",
      "isVisible",
      "sortOrder"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid",
       "readOnly": true,
       "description": "**Added 20 August.** The table had no key at all — no id, no parent and no natural key, so **no row could be addressed, updated or deleted.** The response schema returned everything a caller needs and not the row's own identity, which is the difference between an API response and a table.\n"
      },
      "label": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "icon": {
       "type": "string"
      },
      "target": {
       "$ref": "#/components/schemas/LinkTarget"
      },
      "isVisible": {
       "type": "boolean",
       "description": "At most five may be visible in bottom navigation; the rest overflow."
      },
      "sortOrder": {
       "type": "integer"
      }
     }
    }
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
 "SeoMetadata": {
  "type": "object",
  "x-ticvai-persistence": "control.seo_metadata",
  "description": "22.11.1 to 22.11.12, CF-137. **Twelve requirements, checked against the matrix.**\n**SEO is not a marketing nicety for a venue selling online** — an attraction that does not appear in search sells through OTAs at OTA commission, which is the cost this avoids.\n",
  "required": [
   "id",
   "entityKind",
   "entityId"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "entityKind": {
    "type": "string",
    "enum": [
     "contentPage",
     "product",
     "event",
     "performance",
     "membership",
     "promotion",
     "venue"
    ]
   },
   "entityId": {
    "type": "string",
    "format": "uuid"
   },
   "locale": {
    "type": "string"
   },
   "title": {
    "type": "string",
    "nullable": true
   },
   "metaDescription": {
    "type": "string",
    "nullable": true
   },
   "keywords": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "canonicalUrl": {
    "type": "string",
    "nullable": true
   },
   "slug": {
    "type": "string",
    "nullable": true,
    "description": "22.11.6. **Human-readable, and changing one is a redirect rather than an edit** — a slug that changes without a 301 is a page that was ranking and now is not.\n"
   },
   "hreflang": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    },
    "description": "22.11.11. **Which URL serves which language**, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page.\n"
   },
   "schemaOrgType": {
    "type": "string",
    "nullable": true
   },
   "openGraph": {
    "type": "object",
    "additionalProperties": {
     "type": "string"
    }
   },
   "isAutoGenerated": {
    "type": "boolean",
    "default": true,
    "description": "22.11.2. **Generated by default and overridable.** A venue with 400 products will not write 400 meta descriptions, and one with an important landing page will not accept a generated one.\n"
   },
   "noIndex": {
    "type": "boolean",
    "default": false
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "TenantConfig": {
  "x-ticvai-persistence": "whitelabel.tenant_config",
  "type": "object",
  "description": "**The tenant's working draft**, one row per tenant (see the header). Published versions are `ConfigVersion.snapshot`, not further rows here.\n**Only `tenantId` and `version` are required**, because the draft is built one part at a time: the first `set*` call creates the row with that part alone. A part that is still unset is what `validateTenantConfig` reports (`missingRequiredAsset` and the like) and what blocks `publishTenantConfig` — a storage rule that every part exist would stop the first save.\n",
  "required": [
   "tenantId",
   "version"
  ],
  "properties": {
   "tenantId": {
    "type": "string",
    "format": "uuid"
   },
   "version": {
    "type": "string",
    "description": "The draft's working version label; the published one is `ConfigVersion.version`."
   },
   "isDraft": {
    "type": "boolean",
    "readOnly": true,
    "description": "True for the working draft, which is the only row."
   },
   "brand": {
    "$ref": "#/components/schemas/BrandIdentity"
   },
   "appIcons": {
    "$ref": "#/components/schemas/AppIcons"
   },
   "bookingFlow": {
    "$ref": "#/components/schemas/BookingFlowConfig"
   },
   "theme": {
    "$ref": "#/components/schemas/Theme"
   },
   "fonts": {
    "$ref": "#/components/schemas/FontConfig"
   },
   "footer": {
    "$ref": "#/components/schemas/FooterConfig"
   },
   "notificationBranding": {
    "type": "object",
    "nullable": true,
    "description": "BL-003. **`marketing-crm` holds the templates and nothing said whose identity they wear.** A message sent on behalf of a venue carries that venue's sender name, reply-to and logo — **an operational alert arriving from `noreply@ticvai.com` is one a guest marks as spam.**\nResolved on the template at send time rather than duplicated per template.\n",
    "properties": {
     "senderName": {
      "type": "string"
     },
     "replyToEmail": {
      "type": "string",
      "format": "email"
     },
     "smsSenderId": {
      "type": "string",
      "nullable": true
     },
     "whatsappBusinessId": {
      "type": "string",
      "nullable": true
     },
     "logoAssetId": {
      "type": "string",
      "format": "uuid",
      "nullable": true
     }
    }
   },
   "enabledPaymentMethods": {
    "type": "array",
    "nullable": true,
    "description": "BL-004. **`FeatureToggle` could turn Apple Pay on and could not say which cards a tenant accepts.** Resolved against `orders.PaymentProvider.supportedMethods` — the tenant's choice within what the gateway offers, and **a tenant enabling a method their provider does not support should fail here rather than at checkout.**\n",
    "items": {
     "type": "string"
    }
   },
   "accessibility": {
    "$ref": "#/components/schemas/AccessibilitySettings"
   },
   "header": {
    "$ref": "#/components/schemas/HeaderConfig"
   },
   "navigation": {
    "$ref": "#/components/schemas/NavigationConfig"
   },
   "homepage": {
    "$ref": "#/components/schemas/HomepageLayout"
   },
   "modules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/ModuleEnablement"
    }
   },
   "features": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/FeatureToggle"
    }
   },
   "languages": {
    "$ref": "#/components/schemas/LanguageConfig"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "isInMaintenance": {
    "type": "boolean",
    "default": false,
    "description": "Written by `setMaintenanceMode`; read by `getTenantAppStatus`."
   },
   "maintenanceMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "The message on the branded maintenance screen."
   },
   "expectedBackAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "minimumAppVersion": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MinimumAppVersion"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "contact": {
    "allOf": [
     {
      "$ref": "#/components/schemas/VenueContact"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availability": {
    "allOf": [
     {
      "$ref": "#/components/schemas/AppAvailability"
     }
    ],
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "availabilityMessage": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Live state, written by `setMaintenanceMode` (audit R073)."
   },
   "venues": {
    "type": "array",
    "x-ticvai-derived": "onRead",
    "description": "The tenant's active venues, for the guest venue picker on WEB-001 and GST-001 (decided 28 September, audit R267). Public: returned without a session and cached with the rest of the response. Read from `tenancy` venues; a closed or archived venue is left out.\n",
    "items": {
     "type": "object",
     "required": [
      "venueId",
      "name"
     ],
     "properties": {
      "venueId": {
       "type": "string",
       "format": "uuid"
      },
      "name": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "city": {
       "type": "string",
       "nullable": true
      },
      "openingHours": {
       "allOf": [
        {
         "$ref": "#/components/schemas/LocalisedText"
        }
       ],
       "nullable": true,
       "description": "Today's hours as shown to a guest, e.g. \"10:00 to 22:00\"."
      }
     }
    }
   }
  }
 },
 "Theme": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "required": [
   "primaryColour",
   "secondaryColour",
   "backgroundColour",
   "textColour"
  ],
  "properties": {
   "primaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "secondaryColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "accentColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "backgroundColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "textColour": {
    "type": "string",
    "pattern": "^#[0-9A-Fa-f]{6}$"
   },
   "darkMode": {
    "type": "object",
    "description": "Optional dark variant. Derived from the light theme when absent.",
    "properties": {
     "primaryColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "backgroundColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     },
     "textColour": {
      "type": "string",
      "pattern": "^#[0-9A-Fa-f]{6}$"
     }
    }
   },
   "cornerRadius": {
    "type": "integer",
    "minimum": 0,
    "maximum": 32,
    "description": "The prototype's 0 to 22 px slider sits inside these bounds (rev 3 CFG-2, no change). Its named palettes, font pairs and background tones are presets over the colours here and `FontConfig`, not stored values."
   },
   "surfaceStyle": {
    "type": "string",
    "enum": [
     "glass",
     "solid"
    ],
    "default": "glass",
    "description": "Cards and panels as frosted glass or opaque (decided 29 September, rev 3 CFG-3)."
   },
   "buttonStyle": {
    "type": "string",
    "enum": [
     "solid",
     "outline",
     "pill"
    ],
    "default": "solid",
    "description": "Button shape (decided 29 September, rev 3 CFG-3)."
   }
  }
 },
 "UrlRedirect": {
  "type": "object",
  "x-ticvai-persistence": "control.url_redirect",
  "description": "22.11.7. **Retired pages, expired campaigns and migrated content**, which is most of a website's history.\n**A redirect chain is the failure mode.** A → B → C loses ranking at every hop, so a new redirect whose target is itself a redirect is collapsed rather than appended.\n",
  "required": [
   "id",
   "fromPath",
   "toPath",
   "statusCode"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "fromPath": {
    "type": "string"
   },
   "toPath": {
    "type": "string"
   },
   "statusCode": {
    "type": "integer",
    "enum": [
     301,
     302,
     307,
     308
    ]
   },
   "reason": {
    "type": "string",
    "enum": [
     "contentMigrated",
     "pageRetired",
     "campaignExpired",
     "restructure",
     "slugChanged"
    ]
   },
   "createdAt": {
    "type": "string",
    "format": "date-time",
    "readOnly": true,
    "nullable": true,
    "description": "**Taken from their `whitelabel.redirect`, 20 September.** This table counts hits and could not say when a redirect was added — a record of a site's history with no date on its own rows. Ours had `hitCount` and no timestamp of any kind.\n"
   },
   "hitCount": {
    "type": "integer",
    "readOnly": true
   },
   "isActive": {
    "type": "boolean",
    "default": true
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "VenueContact": {
  "x-ticvai-persistence": "none — embedded in tenant_config",
  "type": "object",
  "nullable": true,
  "description": "How a guest reaches the venue: WEB-028 Contact & Venue Information, and the screen shown on an error or when the app cannot help (decided 28 September, audit R073). Public, because nothing here is personal.\n",
  "properties": {
   "phone": {
    "type": "string",
    "nullable": true
   },
   "email": {
    "type": "string",
    "format": "email",
    "nullable": true
   },
   "whatsapp": {
    "type": "string",
    "nullable": true
   },
   "address": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true
   },
   "openingHours": {
    "allOf": [
     {
      "$ref": "#/components/schemas/LocalisedText"
     }
    ],
    "nullable": true,
    "description": "Prose, as the guest reads it. The bookable hours are the catalogue's."
   }
  }
 }
}
```
