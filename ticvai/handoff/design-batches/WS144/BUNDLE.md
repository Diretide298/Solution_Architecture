# WS144 — Marketing CRM Configuration Reference v1.0 board 10

**10 screens · 14 operations · 19 schemas · 4 permissions**

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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `GUEST_VIEW, MARKETING_MANAGE, MARKETING_VIEW, REPORT_VIEW_VENUE`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `BO-824` | Gamification Command Center | listDetail | 1 | 0 | — |
| `BO-825` | Challenge Builder | listDetail | 1 | 0 | — |
| `BO-826` | Achievement & Badge Engine | listDetail | 3 | 0 | — |
| `BO-827` | Points & Activity Rules | listDetail | 3 | 0 | — |
| `BO-828` | Milestones & Reward Rules | listDetail | 2 | 0 | — |
| `BO-829` | Family, Team & Event Challenges | listDetail | 1 | 0 | — |
| `BO-830` | Referral & Streak Management | listDetail | 1 | 0 | — |
| `BO-831` | Progress, Leaderboards & Hub | listDetail | 1 | 0 | — |
| `BO-832` | AI Engagement Optimization | listDetail | 1 | 0 | — |
| `BO-833` | Gamification Analytics & Audit | listDetail | 3 | 0 | — |

## Thin screens in this batch

**BO-825, BO-826, BO-827, BO-828, BO-829, BO-830, BO-832, BO-833 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "BO-824",
  "name": "Gamification Command Center",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "01",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/gamification-command-center-bo-824",
   "component": "apps/venue-management-web/src/routes/engagement-support/GamificationCommandCenter.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-100"
   ],
   "exitTo": [
    "BO-100",
    "BO-825",
    "BO-826",
    "BO-827",
    "BO-828",
    "BO-829",
    "BO-830",
    "BO-831",
    "BO-832",
    "BO-833"
   ],
   "transitions": [
    {
     "to": "BO-100",
     "trigger": "Back to Venue Home",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    },
    {
     "to": "BO-825",
     "trigger": "Challenge Builder",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-826",
     "trigger": "Achievement & Badge Engine",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-827",
     "trigger": "Points & Activity Rules",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-828",
     "trigger": "Milestones & Reward Rules",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-829",
     "trigger": "Family, Team & Event Challenges",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-830",
     "trigger": "Referral & Streak Management",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-831",
     "trigger": "Progress, Leaderboards & Hub",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-832",
     "trigger": "AI Engagement Optimization",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    },
    {
     "to": "BO-833",
     "trigger": "Gamification Analytics & Audit",
     "provenance": "structural — pack board 10 wiring, 19 September 2026"
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Monitor engagement programs and their financial and behavioral impact. Show active challenges, participants, completion, points issued, rewards claimed, streaks and referrals. Report engagement lift, repeat visits, revenue impact and unredeemed points/reward liability. Compare by challenge, audience, venue, event, membership, team, season and period. Surface fraud anomalies, overspend, low participation and explainable AI opportunities. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "headline",
     "components": [
      {
       "kind": "metricTile",
       "label": "Active challenges",
       "bindsTo": "Challenge",
       "columns": [
        "Challenge.status"
       ],
       "operation": "getMyChallenges",
       "notes": "Count where `status` is active. The bound read is the caller's own list (`/guests/me/challenges`), not the tenant's.",
       "provenance": "contract marketing-crm.yaml GET /guests/me/challenges"
      },
      {
       "kind": "metricTile",
       "label": "Participants",
       "columns": [
        "Participants"
       ],
       "notes": "The pack asks for participants; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
      },
      {
       "kind": "metricTile",
       "label": "Completion rate",
       "columns": [
        "Completion rate"
       ],
       "notes": "The pack asks for completion rate; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
      },
      {
       "kind": "metricTile",
       "label": "Points issued",
       "columns": [
        "Points issued"
       ],
       "notes": "The pack asks for points issued; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
      },
      {
       "kind": "metricTile",
       "label": "Rewards claimed",
       "columns": [
        "Rewards claimed"
       ],
       "notes": "The pack asks for rewards claimed; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
      },
      {
       "kind": "metricTile",
       "label": "Unredeemed points / reward liability",
       "columns": [
        "Unredeemed points / reward liability"
       ],
       "notes": "The pack asks for unredeemed points / reward liability; the contract has no field for it.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Challenges",
       "bindsTo": "Challenge",
       "columns": [
        "Challenge.name",
        "Challenge.kind",
        "Challenge.scope",
        "Challenge.eventId",
        "Challenge.rewardKind",
        "Challenge.rewardValue",
        "Challenge.startsAt",
        "Challenge.endsAt",
        "Challenge.status"
       ],
       "operation": "getMyChallenges",
       "provenance": "contract marketing-crm.yaml GET /guests/me/challenges"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected challenge",
       "bindsTo": "Challenge",
       "columns": [
        "Challenge.id",
        "Challenge.name",
        "Challenge.kind",
        "Challenge.scope",
        "Challenge.goal",
        "Challenge.rewardKind",
        "Challenge.rewardValue",
        "Challenge.rewardAmount",
        "Challenge.badgeAssetId",
        "Challenge.startsAt",
        "Challenge.endsAt",
        "Challenge.status",
        "Challenge.scopePath",
        "ChallengeProgress.current",
        "ChallengeProgress.target",
        "ChallengeProgress.streakCount",
        "ChallengeProgress.completedAt"
       ],
       "operation": "getMyChallenges",
       "notes": "Progress is the caller's own, from the same read.",
       "provenance": "contract marketing-crm.yaml GET /guests/me/challenges"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gamification list.",
   "error": "Could not load. Names which read failed and leaves the gamification untouched.",
   "emptyFirstRun": "No gamification yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gamification are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getMyChallenges",
    "contract": "marketing-crm",
    "purpose": "Challenges running",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-824",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-824"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Marketing_CRM_Configuration_Reference v1.0.pdf p.49; contract marketing-crm.yaml GET /guests/me/challenges. Pack labels with no schema field yet (shown as plain labels): Participants, Completion rate, Points issued, Rewards claimed, Unredeemed points / reward liability, Streaks, Referrals, Engagement lift, Repeat visits, Revenue impact, Fraud anomalies, A back-office challenge population read (bound op is the guest's own list).",
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
  "id": "BO-825",
  "name": "Challenge Builder",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "02",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/challenge-builder-bo-825",
   "component": "apps/venue-management-web/src/routes/engagement-support/ChallengeBuilder.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Create a governed challenge from objective through publication. Configure challenge name, objective, audience, actions, progress logic, start/end, recurrence and capacity. Define eligibility, terms, visibility, multilingual content, image, completion rule and reward. Support visit, purchase, scan, activity, referral, survey and approved social actions. Validate overlapping rules, reward budget, fraud controls, legal terms and approval before activation. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": "createChallenge",
    "why": "**`Challenge.kind` lacks scan, activity and purchase**, which the client keeps (decided 28 September, audit R275 (c)); handed to the contracts group to add to the enum.",
    "source": "audit R275 (c)"
   },
   {
    "operation": null,
    "why": "**Challenge Builder declares no operation that writes anything** — its only declared call is `none`, a read. The name promises authoring and the contract offers none, so either the write operations are missing or this screen is a view of something another screen builds.",
    "source": "contract — the screen's declared operations"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
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
       "impliedBy": "createChallenge",
       "label": "Create challenge",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "selectField",
       "label": "Challenge action",
       "operation": "createChallenge",
       "notes": "**Scan, activity and purchase are kept** (decided 28 September, audit R275 (c)) beside the contract's `Challenge.kind` values (visit, spend, ride, collection, streak, referral, survey, social, milestone). The three are handed to the contracts group to add to `Challenge.kind`; until then the picker offers them disabled.",
       "provenance": "contract marketing-crm.yaml POST /challenges"
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createChallenge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The challenge list.",
   "error": "Could not load. Names which read failed and leaves the challenge untouched.",
   "emptyFirstRun": "No challenge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the challenge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createChallenge",
    "contract": "marketing-crm",
    "purpose": "Build a challenge",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-825",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-825"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-826",
  "name": "Achievement & Badge Engine",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "03",
   "page": 49
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/achievement-badge-engine-bo-826",
   "component": "apps/venue-management-web/src/routes/engagement-support/AchievementBadgeEngine.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Manage achievements and digital badges. Define achievement type, badge name, tier, rarity, unlock criteria, points value, visibility and validity. Maintain an approved visual badge library and multilingual name/description and accessible alt text. Configuration Scope of Work | Version 1.0 49 Configure automatic or manual issuance, revocation, duplicate prevention and profile/mobile display. Track active challenges and rewards using each achievement before editing or retiring it. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 49"
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
       "impliedBy": "createChallenge",
       "label": "Create challenge",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createChallenge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The achievement badge list.",
   "error": "Could not load. Names which read failed and leaves the achievement badge untouched.",
   "emptyFirstRun": "No achievement badge yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the achievement badge are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createChallenge",
    "contract": "marketing-crm",
    "purpose": "Achievements and badges",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setBadge",
    "contract": "marketing-crm",
    "purpose": "Define a badge",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "awardBadge",
    "contract": "marketing-crm",
    "purpose": "Award a badge to a guest by hand",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "customerId",
     "from": "navigation"
    }
   ],
   "coldEntry": "Opened from BO-824 with the guest picked there. Opened cold (a bookmark or a refresh), it shows the list to pick from rather than an empty record, and says plainly if the guest no longer exists."
  },
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-826",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-826"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 49. 0 of 0 labels bound to a contract property; 0 of 11 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-827",
  "name": "Points & Activity Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "04",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/points-activity-rules-bo-827",
   "component": "apps/venue-management-web/src/routes/engagement-support/PointsActivityRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Translate qualifying guest actions into controlled loyalty points. Configure rules for visits, purchases, ticket scans, activities, referrals, surveys and other approved events. Set base points, multiplier, daily/monthly limit, validity, rounding and posting timing. Apply device, account, velocity, location and transaction fraud checks and exception review. Post through the shared Loyalty Engine and preserve source event, rule/version and adjustment history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
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
       "impliedBy": "createLoyaltyProgramme",
       "label": "Create loyalty programme",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createLoyaltyProgramme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The points activity rules list.",
   "error": "Could not load. Names which read failed and leaves the points activity rules untouched.",
   "emptyFirstRun": "No points activity rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the points activity rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createLoyaltyProgramme",
    "contract": "marketing-crm",
    "purpose": "Points and activity rules",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setLoyaltyRules",
    "contract": "marketing-crm",
    "purpose": "Replace a programme's earning rules as one set",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   },
   {
    "operationId": "setLoyaltyCampaign",
    "contract": "marketing-crm",
    "purpose": "Define a bonus-points campaign and its window",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-827",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-827"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "programmeId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-828",
  "name": "Milestones & Reward Rules",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "05",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/milestones-reward-rules-bo-828",
   "component": "apps/venue-management-web/src/routes/engagement-support/MilestonesRewardRules.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Reward cumulative progress consistently. Define thresholds, tiers and immediate or delayed reward fulfillment. Support loyalty points, wallet credit, voucher, product offer, badge and membership benefit rewards. Configure eligibility, inventory, validity, redemption limit, substitution and approval threshold. Forecast reward cost/liability and prevent issuance when funding, inventory or eligibility fails. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
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
       "impliedBy": "createLoyaltyProgramme",
       "label": "Create loyalty programme",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createLoyaltyProgramme"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The milestones reward rules list.",
   "error": "Could not load. Names which read failed and leaves the milestones reward rules untouched.",
   "emptyFirstRun": "No milestones reward rules yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the milestones reward rules are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createLoyaltyProgramme",
    "contract": "marketing-crm",
    "purpose": "Milestones and rewards",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "setReward",
    "contract": "marketing-crm",
    "purpose": "Define a reward and its points cost",
    "trigger": "onAction",
    "provenance": "decided 29 September, VM close-out (venue management and configuration)"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-828",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-828"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 8 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-829",
  "name": "Family, Team & Event Challenges",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "06",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/family-team-event-challenges-bo-829",
   "component": "apps/venue-management-web/src/routes/engagement-support/FamilyTeamEventChallenges.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Support collaborative and competitive engagement formats. Configure family/household, team, group and event membership and joining rules. Define individual versus shared contribution, group scoring, maximum members and visibility. Configure ranking, winner calculation, tie-break, prize allocation and guardian rules for minors. Show participant roster, progress, status, exceptions and auditable membership changes. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
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
       "impliedBy": "createChallenge",
       "label": "Create challenge",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createChallenge"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The family team event list.",
   "error": "Could not load. Names which read failed and leaves the family team event untouched.",
   "emptyFirstRun": "No family team event yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the family team event are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createChallenge",
    "contract": "marketing-crm",
    "purpose": "Family, team and event challenges",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-829",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-829"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-830",
  "name": "Referral & Streak Management",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "07",
   "page": 50
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/referral-streak-management-bo-830",
   "component": "apps/venue-management-web/src/routes/engagement-support/ReferralStreakManagement.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Configure repeat-behavior and referral mechanics. Define streak frequency, qualifying event, grace period, reset, maximum, milestone and reward. Configure referral code/link, attribution window, qualifying action, inviter/invitee reward and limits. Apply identity, account, device, payment, velocity and collusion fraud checks. Configuration Scope of Work | Version 1.0 50 Track invitation, qualification, reward posting, reversal and dispute history. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 50"
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
       "impliedBy": "createReferral",
       "label": "Create referral",
       "notes": "The act the screen exists for."
      },
      {
       "kind": "secondaryButton",
       "label": "Cancel",
       "notes": "**A screen that can submit must be leaveable without submitting.**",
       "derived": true,
       "impliedBy": "createReferral"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The referral streak list.",
   "error": "Could not load. Names which read failed and leaves the referral streak untouched.",
   "emptyFirstRun": "No referral streak yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the referral streak are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "createReferral",
    "contract": "marketing-crm",
    "purpose": "Referral and streak mechanics",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-830",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-830"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 50. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
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
  "id": "BO-831",
  "name": "Progress, Leaderboards & Hub",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "08",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/progress-leaderboards-hub-bo-831",
   "component": "apps/venue-management-web/src/routes/engagement-support/ProgressLeaderboardsHub.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Control how participants see progress and rankings. Show progress, points, milestones, next reward, streak and challenge status by participant. Configure leaderboard metric, scope, season, filters, dense ranking, privacy display and opt-out. Manage mobile gamification-hub content, featured challenges, quick actions and deep links. Provide near-real-time updates and resolve corrections without losing historical ranking evidence. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
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
       "label": "Programme",
       "operation": "getLoyaltyPosition",
       "notes": "Sends `?programmeId=` (required).",
       "provenance": "contract marketing-crm.yaml GET /loyalty/position"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Participant progress",
       "bindsTo": "LoyaltyPosition",
       "columns": [
        "LoyaltyPosition.subjectId",
        "LoyaltyPosition.programmeId",
        "LoyaltyPosition.pointsBalance",
        "LoyaltyPosition.pointsToNextTier",
        "tier",
        "nextTier",
        "pointsPending",
        "expiringPoints",
        "expiringAt"
       ],
       "operation": "getLoyaltyPosition",
       "notes": "The operation's response is an inline object: `tier`, `nextTier`, `pointsPending`, `expiringPoints` and `expiringAt` are its fields, not `LoyaltyPosition`'s. It returns the caller's own position, not a chosen participant's.",
       "provenance": "contract marketing-crm.yaml GET /loyalty/position"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Leaderboard",
       "columns": [
        "Rank",
        "Participant (nickname)",
        "Metric value",
        "Season",
        "Scope",
        "Opted out"
       ],
       "notes": "Leaderboard metric, scope, season, dense ranking and privacy display; no leaderboard read is bound.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
      },
      {
       "kind": "dataTable",
       "label": "Hub content",
       "columns": [
        "Featured challenge",
        "Quick action",
        "Deep link",
        "Order"
       ],
       "notes": "Mobile gamification-hub content.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "selectField",
       "label": "Leaderboard metric",
       "notes": "With scope, season and privacy display, the pack's leaderboard configuration.",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
      },
      {
       "kind": "toggle",
       "label": "Allow opt-out",
       "provenance": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The progress leaderboards list.",
   "error": "Could not load. Names which read failed and leaves the progress leaderboards untouched.",
   "emptyFirstRun": "No progress leaderboards yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the progress leaderboards are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getLoyaltyPosition",
    "contract": "marketing-crm",
    "purpose": "Progress and leaderboards",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-831",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-831"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 7 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here. **Layout drafted 29 September (VM close-out)** from pack Marketing_CRM_Configuration_Reference v1.0.pdf p.51; contract marketing-crm.yaml GET /loyalty/position. Pack labels with no schema field yet (shown as plain labels): Leaderboard rank, Leaderboard metric / scope / season, Opt-out, Next reward, Streak, Challenge status by participant, Hub featured challenges / quick actions / deep links.",
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
  "id": "BO-832",
  "name": "AI Engagement Optimization",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "09",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/ai-engagement-optimization-bo-832",
   "component": "apps/venue-management-web/src/routes/engagement-support/AiEngagementOptimization.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Recommend relevant, sustainable engagement programs. Recommend challenge type, audience, difficulty, actions, reward and timing using historical behavior. Predict participation, completion, engagement uplift, cost and liability with confidence and factors. Support what-if comparison and require approval before a suggestion becomes a challenge or rule. Monitor applied recommendation results and avoid manipulative, discriminatory or age- inappropriate designs. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history.",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getGuestIntelligence",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The engagement optimization list.",
   "error": "Could not load. Names which read failed and leaves the engagement optimization untouched.",
   "emptyFirstRun": "No engagement optimization yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the engagement optimization are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "getGuestIntelligence",
    "contract": "marketing-crm",
    "purpose": "Who to nudge, and why",
    "trigger": "onAction",
    "provenance": "board reading, 19 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-832",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-832"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 9 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "guestId",
     "from": "navigation"
    }
   ]
  },
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
  "id": "BO-833",
  "name": "Gamification Analytics & Audit",
  "module": "Engagement & Support",
  "requiresModule": "marketing",
  "wave": 3,
  "source": {
   "pack": "Marketing_CRM_Configuration_Reference v1.0.pdf",
   "board": "10",
   "number": "10",
   "page": 51
  },
  "implementation": {
   "app": "venue-management-web",
   "route": "/engagement-support/gamification-analytics-audit-bo-833",
   "component": "apps/venue-management-web/src/routes/engagement-support/GamificationAnalyticsAudit.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "BO-824"
   ],
   "exitTo": [
    "BO-824"
   ],
   "transitions": [
    {
     "to": "BO-824",
     "trigger": "Back to Gamification Command Center",
     "provenance": "structural — pack board 10 wiring, 19 September 2026",
     "back": true
    }
   ]
  },
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "**nothing in the pack chooses a pattern for this screen** — no metric directory, no display directory, no configuration directory. It falls to the default, and the fallback is recorded rather than passed off as a decision",
  "purpose": "Measure challenge performance, cost and long-term effect. Report participant funnel, completion, points, rewards, redemption, cost, revenue and repeat visits. Compare challenges, audiences, venues, events, seasons, reward types and membership groups. Measure retention and engagement lift against appropriate baselines and show points/reward liability. Audit definitions, approvals, events, progress adjustments, reward postings, AI recommendations and exports. Acceptance condition: Authorized users can complete the described task end to end; saved changes are validated, permission-controlled, integrated with the named shared services and traceable in the audit history. Configuration Scope of Work | Version 1.0 51 Board 11 - CMS, White-Label Content & SEO Figure 11. High-definition configuration board with all 10 screens. Configuration Scope of Work | Version 1.0 52",
  "gaps": [
   {
    "operation": null,
    "why": "**The pack gives this screen nothing that can be drawn.** Its sections are prose — purpose, acceptance conditions, worked examples — with no directory of metrics, columns or fields anywhere in them. The screen has no content region rather than an empty one, and it needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
   },
   {
    "operation": null,
    "why": "**The pack gives this screen no display, metric or configuration directory**, so its shape is a default rather than a reading. It needs a person before it is built.",
    "source": "pack Marketing_CRM_Configuration_Reference v1.0.pdf, page 51"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "components": [
      {
       "kind": "dataTable",
       "derived": true,
       "impliedBy": "listLoyaltyProgrammes",
       "notes": "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a venue's busiest hour is a list that skips rows."
      },
      {
       "kind": "detailPanel",
       "derived": true,
       "impliedBy": "getDashboard",
       "notes": "One record, read-only."
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The gamification analytics audit list.",
   "error": "Could not load. Names which read failed and leaves the gamification analytics audit untouched.",
   "emptyFirstRun": "No gamification analytics audit yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the gamification analytics audit are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listLoyaltyProgrammes",
    "contract": "marketing-crm",
    "purpose": "Gamification analytics",
    "trigger": "onLoad",
    "provenance": "board reading, 19 September 2026"
   },
   {
    "operationId": "getKpiValues",
    "contract": "reporting",
    "purpose": "Participation, loyalty/membership impact, retention",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   },
   {
    "operationId": "getDashboard",
    "contract": "reporting",
    "purpose": "Gamification analytics dashboard",
    "trigger": "onLoad",
    "provenance": "build, 29 September 2026"
   }
  ],
  "wireframe": {
   "status": "notStarted",
   "board": "wireframes/P08 Venue Management.dc.html#bo-833",
   "workshopBoard": "wireframes/WS79 Marketing CRM Configuration Reference v1.0 Board 10.dc.html#bo-833"
  },
  "apisNote": "Regenerated 9 September 2026 from Marketing_CRM_Configuration_Reference v1.0.pdf page 51. 0 of 0 labels bound to a contract property; 0 of 25 pack bullets carried onto the screen — the rest are acceptance prose, worked examples and AI narrative, which belong to the matrix and the contracts rather than here.",
  "entryState": {
   "params": [
    {
     "name": "dashboardId",
     "from": "navigation"
    }
   ]
  },
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
 "awardBadge": {
  "method": "POST",
  "path": "/customers/{customerId}/badges",
  "contract": "marketing-crm",
  "summary": "Award a badge",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "customerId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MarketingCustomerBadge",
  "responds": "MarketingCustomerBadge"
 },
 "createChallenge": {
  "method": "POST",
  "path": "/challenges",
  "contract": "marketing-crm",
  "summary": "Define a challenge, mission or streak",
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
  "requestBody": "Challenge",
  "responds": "Challenge"
 },
 "createLoyaltyProgramme": {
  "method": "POST",
  "path": "/loyalty/programmes",
  "contract": "marketing-crm",
  "summary": "Create a loyalty programme",
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
  "requestBody": "LoyaltyProgramme",
  "responds": "LoyaltyProgramme"
 },
 "createReferral": {
  "method": "POST",
  "path": "/referrals",
  "contract": "marketing-crm",
  "summary": "Issue a referral code",
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
  "requestBody": "Referral",
  "responds": "Referral"
 },
 "getDashboard": {
  "method": "GET",
  "path": "/dashboards/{dashboardId}",
  "contract": "reporting",
  "summary": "Read a dashboard with tile data",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "refresh",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "DashboardData"
 },
 "getGuestIntelligence": {
  "method": "GET",
  "path": "/guests/{guestId}/intelligence",
  "contract": "marketing-crm",
  "summary": "Value, engagement, churn and propensity, with their reasons",
  "permission": "GUEST_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "GuestIntelligence"
 },
 "getKpiValues": {
  "method": "GET",
  "path": "/kpi-values",
  "contract": "reporting",
  "summary": "Current values, against target, with movement",
  "permission": "REPORT_VIEW_VENUE",
  "offlineCapable": null,
  "conflictPolicy": null,
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "kpiIds",
    "in": "query",
    "required": null
   },
   {
    "name": "kpiCodes",
    "in": "query",
    "required": null
   },
   {
    "name": "scopePath",
    "in": "query",
    "required": null
   },
   {
    "name": "period",
    "in": "query",
    "required": null
   },
   {
    "name": "compareTo",
    "in": "query",
    "required": null
   },
   {
    "name": "interval",
    "in": "query",
    "required": null
   },
   {
    "name": "groupBy",
    "in": "query",
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "KpiValue"
 },
 "getLoyaltyPosition": {
  "method": "GET",
  "path": "/loyalty/position",
  "contract": "marketing-crm",
  "summary": "A guest's points, tier and what is within reach",
  "permission": null,
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": "programmeId",
    "in": "query",
    "required": true
   }
  ],
  "requestBody": null,
  "responds": null
 },
 "getMyChallenges": {
  "method": "GET",
  "path": "/guests/me/challenges",
  "contract": "marketing-crm",
  "summary": "Active challenges and how far along I am",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": null
 },
 "listLoyaltyProgrammes": {
  "method": "GET",
  "path": "/loyalty/programmes",
  "contract": "marketing-crm",
  "summary": "List loyalty programmes",
  "permission": "MARKETING_VIEW",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
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
 "setBadge": {
  "method": "PUT",
  "path": "/badges",
  "contract": "marketing-crm",
  "summary": "Define a badge",
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
  "requestBody": "MarketingBadge",
  "responds": "MarketingBadge"
 },
 "setLoyaltyCampaign": {
  "method": "PUT",
  "path": "/loyalty/campaigns",
  "contract": "marketing-crm",
  "summary": "Define a loyalty campaign and its window",
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
  "requestBody": "MarketingLoyaltyCampaign",
  "responds": "MarketingLoyaltyCampaign"
 },
 "setLoyaltyRules": {
  "method": "PUT",
  "path": "/loyalty/programmes/{programmeId}/rules",
  "contract": "marketing-crm",
  "summary": "Replace a programme's rules as one set",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "programmeId",
    "in": "path",
    "required": true
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "LoyaltyRuleSet",
  "responds": "LoyaltyRuleSet"
 },
 "setReward": {
  "method": "PUT",
  "path": "/loyalty/rewards",
  "contract": "marketing-crm",
  "summary": "Define a reward and its points cost",
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
  "requestBody": "MarketingReward",
  "responds": "MarketingReward"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "Challenge": {
  "type": "object",
  "x-ticvai-persistence": "marketing.challenge",
  "description": "BL-022, CF-137. **Section 22.6 is twenty requirements and 19.2.73–75 three more** — checked against the matrix on 18 August rather than assumed. It is asked for explicitly.\n**Gamification is not loyalty.** Loyalty pays for spend; a challenge pays for behaviour the venue wants and spend does not produce — a second visit, a quiet Tuesday, a ride nobody rides. **A challenge that only rewards spending is a loyalty programme with worse arithmetic.**\n",
  "required": [
   "id",
   "name",
   "kind",
   "goal",
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
    "description": "What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or point (a trail marker, a stand), `activity` counts completions of a named attraction or activity that is not a ride, and `purchase` counts purchases of named products or categories. **`purchase` is not `spend`**: `spend` counts money, whatever was bought; `purchase` counts items bought.\n",
    "enum": [
     "visit",
     "spend",
     "ride",
     "collection",
     "streak",
     "referral",
     "survey",
     "social",
     "milestone",
     "scan",
     "activity",
     "purchase"
    ]
   },
   "scope": {
    "type": "string",
    "enum": [
     "individual",
     "family",
     "group",
     "team"
    ],
    "default": "individual",
    "description": "22.6.7 and 22.6.8. **A family challenge is not a per-person challenge counted twice** — members contribute toward one shared goal, and a school competing against another school is a group scoring against a group.\n**This is the field that needs the portfolio work** (CF-132): a family challenge without a family is an individual challenge with a label.\n"
   },
   "goal": {
    "type": "object",
    "description": "What completes it.",
    "properties": {
     "metric": {
      "type": "string"
     },
     "target": {
      "type": "number"
     },
     "withinDays": {
      "type": "integer",
      "nullable": true
     }
    }
   },
   "eventId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rewardKind": {
    "type": "string",
    "enum": [
     "badge",
     "loyaltyPoints",
     "walletCredit",
     "voucher",
     "entitlement",
     "none"
    ],
    "description": "22.6.13. **A reward that issues wallet credit is money**, and it goes through the same stored-value mechanism as everything else rather than a parallel one.\n"
   },
   "rewardValue": {
    "type": "integer",
    "nullable": true,
    "minimum": 1,
    "description": "**Points, for `rewardKind: loyaltyPoints` only.** A count, not an amount — a money reward is `rewardAmount`, never this.\n"
   },
   "rewardAmount": {
    "allOf": [
     {
      "$ref": "../shared/common.yaml#/components/schemas/Money"
     }
    ],
    "nullable": true,
    "description": "**The credit, for `rewardKind: walletCredit` only.** The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money and naming-and-style 5.1 forbids money as a bare number.\n"
   },
   "badgeAssetId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "startsAt": {
    "type": "string",
    "format": "date-time"
   },
   "endsAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "draft",
     "active",
     "paused",
     "ended",
     "archived"
    ]
   },
   "scopePath": {
    "readOnly": true,
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"
   }
  }
 },
 "ChallengeProgress": {
  "type": "object",
  "x-ticvai-persistence": "marketing.challenge_progress",
  "description": "22.6.15. **Progress is shown, not just the outcome.** A guest two visits from a reward behaves differently from one who does not know how close they are, which is the entire mechanism.\n",
  "required": [
   "id",
   "challengeId",
   "subjectId",
   "current",
   "target"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "challengeId": {
    "type": "string",
    "format": "uuid"
   },
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "portfolioId": {
    "type": "string",
    "format": "uuid",
    "nullable": true,
    "description": "For a family or group challenge — where the shared progress accrues."
   },
   "current": {
    "type": "number"
   },
   "target": {
    "type": "number"
   },
   "streakCount": {
    "type": "integer",
    "nullable": true
   },
   "completedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "rewardIssuedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "Dashboard": {
  "x-ticvai-persistence": "reporting.dashboard + reporting.dashboard_tile",
  "allOf": [
   {
    "$ref": "#/components/schemas/CreateDashboardRequest"
   },
   {
    "type": "object",
    "required": [
     "id",
     "ownerPrincipalId",
     "aggregateCost",
     "createdAt"
    ],
    "properties": {
     "id": {
      "type": "string",
      "format": "uuid"
     },
     "ownerPrincipalId": {
      "type": "string",
      "format": "uuid"
     },
     "aggregateCost": {
      "type": "string",
      "enum": [
       "low",
       "medium",
       "high"
      ],
      "description": "Combined refresh load of every tile."
     },
     "archivedAt": {
      "type": "string",
      "format": "date-time",
      "nullable": true,
      "readOnly": true,
      "description": "**Set by `deleteDashboard`, which archives rather than removes.** A dashboard's tiles carry `visualisation`, `parameters` and `refresh_seconds` that somebody configured, and `reporting.dashboard_tile` cascades — so a hard delete takes an afternoon's work with it and leaves nothing to say what was there.\nArchived dashboards are excluded from `listDashboards` unless asked for with `includeArchived=true`.\n"
     },
     "createdAt": {
      "type": "string",
      "format": "date-time"
     }
    }
   }
  ]
 },
 "DashboardData": {
  "x-ticvai-persistence": "none — computed",
  "allOf": [
   {
    "$ref": "#/components/schemas/Dashboard"
   },
   {
    "type": "object",
    "properties": {
     "tileData": {
      "type": "array",
      "items": {
       "type": "object",
       "properties": {
        "tileId": {
         "type": "string",
         "format": "uuid"
        },
        "result": {
         "$ref": "#/components/schemas/ReportResult"
        },
        "isCached": {
         "type": "boolean"
        },
        "error": {
         "type": "string",
         "nullable": true
        }
       }
      }
     }
    }
   }
  ]
 },
 "GuestIntelligence": {
  "type": "object",
  "description": "Board 1.10. **Explainable, or an agent will ignore it or over-trust it.**",
  "properties": {
   "subjectId": {
    "type": "string",
    "format": "uuid"
   },
   "scores": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "kind": {
       "type": "string",
       "enum": [
        "historicalLtv",
        "predictedLtv",
        "engagement",
        "churnRisk",
        "inactivityRisk",
        "cancellationRisk",
        "upgradePropensity",
        "nextPurchasePropensity"
       ]
      },
      "value": {
       "type": "number"
      },
      "band": {
       "type": "string",
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "nullable": true
      },
      "modelId": {
       "type": "string",
       "nullable": true
      },
      "modelVersion": {
       "type": "string",
       "nullable": true
      },
      "computedAt": {
       "type": "string",
       "format": "date-time"
      },
      "factors": {
       "type": "array",
       "items": {
        "type": "object",
        "properties": {
         "factor": {
          "type": "string"
         },
         "contribution": {
          "type": "number"
         }
        }
       }
      },
      "limitations": {
       "type": "array",
       "items": {
        "type": "string"
       },
       "description": "**Policy and data limitations travel with the score**, so the rule that prediction never overrides consent cannot be forgotten downstream.\n"
      }
     }
    }
   },
   "affinities": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "productCategoryId": {
       "type": "string",
       "format": "uuid"
      },
      "label": {
       "type": "string"
      },
      "strength": {
       "type": "number"
      }
     }
    }
   },
   "nextBestActions": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "action": {
       "type": "string"
      },
      "expectedImpact": {
       "type": "string",
       "nullable": true
      },
      "confidence": {
       "type": "number",
       "nullable": true
      }
     }
    }
   }
  }
 },
 "KpiValue": {
  "type": "object",
  "description": "BI board 10.3. **Value, target, variance, direction and freshness in one read.**",
  "properties": {
   "kpiId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string"
   },
   "bucketStart": {
    "type": "string",
    "format": "date-time",
    "nullable": true,
    "description": "The start of the bucket this value covers, when `getKpiValues` was asked for an `interval`; null otherwise."
   },
   "groupKey": {
    "type": "string",
    "nullable": true,
    "description": "The value of the `groupBy` dimension this row is for (a status, a category code, a tier); null when no `groupBy` was asked."
   },
   "name": {
    "type": "string"
   },
   "scopePath": {
    "type": "string"
   },
   "period": {
    "type": "string"
   },
   "value": {
    "$ref": "#/components/schemas/MetricValue"
   },
   "target": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "comparison": {
    "allOf": [
     {
      "$ref": "#/components/schemas/MetricValue"
     }
    ],
    "nullable": true
   },
   "variancePercent": {
    "type": "number",
    "nullable": true
   },
   "direction": {
    "type": "string",
    "enum": [
     "up",
     "down",
     "flat"
    ]
   },
   "status": {
    "type": "string",
    "enum": [
     "green",
     "amber",
     "red",
     "noTarget"
    ]
   },
   "asOf": {
    "type": "string",
    "format": "date-time"
   },
   "stale": {
    "type": "boolean",
    "description": "**True when the pipeline behind it has not refreshed.** A number nobody flagged as stale is a number somebody will act on.\n"
   }
  }
 },
 "LoyaltyProgramme": {
  "x-ticvai-persistence": "marketing.loyalty_programme + marketing.points_earning_rule + marketing.programme_tier",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "earnRules",
   "tiers"
  ],
  "properties": {
   "tiers": {
    "type": "array",
    "description": "**Rows of `marketing.programme_tier`**, the same shape `MarketingProgrammeTier` has — one definition of a tier, not a second copy that cannot round-trip. `loyaltyProgrammeId` and `id` are the server's on create.\n",
    "items": {
     "$ref": "#/components/schemas/MarketingProgrammeTier"
    }
   },
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "x-ticvai-unique": "tenant",
    "description": "**Unique per tenant** (decided 28 September, audit R108). A code already used by any loyalty programme in the tenant, at any venue, is refused with `409 duplicate-code`.\n"
   },
   "name": {
    "type": "string"
   },
   "venueId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pointsLiabilityAccountId": {
    "type": "string",
    "format": "uuid",
    "description": "Points post here on accrual. They are a liability from the moment they are earned, not from the moment they are spent.\n"
   },
   "earnRules": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "trigger",
      "points"
     ],
     "properties": {
      "trigger": {
       "type": "string",
       "enum": [
        "perCurrencyUnit",
        "perVisit",
        "perProduct",
        "onSignup",
        "onBirthday",
        "onReview"
       ]
      },
      "points": {
       "type": "number"
      },
      "productKinds": {
       "type": "array",
       "description": "Limits a `perProduct` or `perCurrencyUnit` rule to these kinds. Empty means every kind.",
       "items": {
        "$ref": "../spine/catalogue.yaml#/components/schemas/ProductKind"
       }
      },
      "multiplier": {
       "type": "number"
      }
     }
    }
   },
   "pointsExpireAfterMonths": {
    "type": "integer",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "LoyaltyRuleSet": {
  "type": "object",
  "x-ticvai-persistence": "none — composed from the rule tables of one programme",
  "description": "**Every rule a programme runs on, read and written as one thing.** Earning, redemption and campaign rules only make sense against each other: a 500-point redemption beside a 5-point earning rule is a hundred visits, and that ratio is the artefact being configured.\nEarning rules are not repeated here — they are `LoyaltyProgramme.earnRules[]` and reached through the programme, which is where they were already declared.\n",
  "required": [
   "programmeId"
  ],
  "properties": {
   "programmeId": {
    "type": "string",
    "format": "uuid"
   },
   "campaignRules": {
    "type": "array",
    "description": "Bonus, multiplier and condition rules, each scoped to a campaign window.",
    "items": {
     "$ref": "#/components/schemas/MarketingLoyaltyRule"
    }
   },
   "tiers": {
    "type": "array",
    "description": "The programme's tiers, in `rank` order. **Read with the rules because a redemption rule that is tier-gated is meaningless without them** — 500 points off for Gold members is two facts, and reviewing one without the other is how a tier nobody can reach acquires a benefit.\n",
    "items": {
     "$ref": "#/components/schemas/MarketingProgrammeTier"
    }
   },
   "redemptionRules": {
    "type": "array",
    "items": {
     "$ref": "#/components/schemas/MarketingPointsRedemptionRule"
    }
   }
  }
 },
 "MarketingBadge": {
  "type": "object",
  "x-ticvai-persistence": "marketing.badge",
  "description": "**Taken from the backend workbook, 20 September.** Defines a digital badge that can be awarded to a customer for challenge completion or other engagement achievement.",
  "required": [
   "code",
   "name",
   "type",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 150
   },
   "description": {
    "type": "string",
    "maxLength": 500,
    "nullable": true
   },
   "iconUrl": {
    "type": "string",
    "maxLength": 1000,
    "nullable": true
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   },
   "updatedAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   }
  }
 },
 "MarketingCustomerBadge": {
  "type": "object",
  "x-ticvai-persistence": "marketing.customer_badge",
  "description": "**Taken from the backend workbook, 20 September.** Stores badges actually awarded to customers and the source that generated each award.",
  "required": [
   "customerId",
   "badgeId",
   "awardedAt",
   "status"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "customerId": {
    "type": "string",
    "format": "uuid"
   },
   "badgeId": {
    "type": "string",
    "format": "uuid"
   },
   "challengeId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "sourceType": {
    "type": "string",
    "maxLength": 30,
    "nullable": true
   },
   "sourceReferenceId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "awardedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "status": {
    "type": "string",
    "maxLength": 20
   }
  }
 },
 "MarketingLoyaltyCampaign": {
  "type": "object",
  "x-ticvai-persistence": "marketing.loyalty_campaign",
  "description": "**Taken from the backend workbook, 20 September.** Links a marketing campaign to temporary loyalty bonuses, rewards, or earning changes.",
  "required": [
   "programId",
   "code",
   "name",
   "startAt",
   "endAt",
   "isActive",
   "createdAt"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "programId": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "startAt": {
    "type": "string",
    "format": "date-time"
   },
   "endAt": {
    "type": "string",
    "format": "date-time"
   },
   "isActive": {
    "type": "boolean"
   },
   "createdAt": {
    "type": "string",
    "format": "date-time"
   }
  }
 },
 "MarketingLoyaltyRule": {
  "type": "object",
  "x-ticvai-persistence": "marketing.loyalty_rule",
  "description": "**Taken from the backend workbook, 20 September.** Defines temporary bonus points, multipliers, earning rules, or rewards applied by a loyalty campaign.",
  "required": [
   "campaignId",
   "type",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "campaignId": {
    "type": "string",
    "format": "uuid"
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "pointsEarningRuleId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "rewardId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "bonusPoints": {
    "type": "number",
    "nullable": true
   },
   "multiplier": {
    "type": "number",
    "nullable": true
   },
   "conditionsJson": {
    "type": "string",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MarketingPointsRedemptionRule": {
  "type": "object",
  "x-ticvai-persistence": "marketing.points_redemption_rule",
  "description": "**Taken from the backend workbook, 20 September.** Defines how loyalty points can be exchanged for discounts, products, or other benefits.",
  "required": [
   "loyaltyProgramId",
   "pointRedemptionRuleCode",
   "name",
   "redemptionType",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "loyaltyProgramId": {
    "type": "string",
    "format": "uuid"
   },
   "pointRedemptionRuleCode": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "redemptionType": {
    "type": "string",
    "maxLength": 30
   },
   "required": {
    "type": "number",
    "nullable": true
   },
   "monetaryValue": {
    "type": "number",
    "nullable": true
   },
   "minimumPoints": {
    "type": "number",
    "nullable": true
   },
   "maximumPoints": {
    "type": "number",
    "nullable": true
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "validFrom": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "validTo": {
    "type": "string",
    "format": "date-time",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MarketingProgrammeTier": {
  "type": "object",
  "x-ticvai-persistence": "marketing.programme_tier",
  "description": "**The tier definition decision 8 promised and nobody built.** `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as denormalised strings and a number, with no table saying what tiers exist or what each one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.\n**Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json` as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that contradicts the schema is worse than a longer name. Not named `marketing.tier` either, because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a package with two tier concepts is how `plan_id` came to point at `subscription.plan`.\n**The denormalised copy on the position stays.** A till rendering *Gold* beside a balance must not join, and must certainly not cross a cell boundary to print a word. This table is the source of truth and those columns are its cache.\n",
  "required": [
   "loyaltyProgrammeId",
   "code",
   "name",
   "rank"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "loyaltyProgrammeId": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "code": {
    "type": "string",
    "maxLength": 40
   },
   "name": {
    "type": "string",
    "maxLength": 120
   },
   "rank": {
    "type": "integer",
    "description": "**Order, not threshold.** Two tiers can share a qualifying rule and still have an order, and sorting by points breaks the moment a tier is granted rather than earned.\n"
   },
   "minLifetimePoints": {
    "type": "integer",
    "nullable": true,
    "description": "What reaching this tier requires. **`pointsToNextTier` on the position is this minus the guest's lifetime points**, and until now it was this minus nothing.\n"
   },
   "retainLifetimePoints": {
    "type": "integer",
    "nullable": true,
    "description": "What keeping it requires, per review period. **Usually lower than reaching it**, and a scheme that cannot express the difference either never demotes or demotes on the day a guest stops earning.\n"
   },
   "validityMonths": {
    "type": "integer",
    "nullable": true,
    "description": "Null means the tier does not lapse on its own."
   },
   "benefits": {
    "type": "array",
    "description": "What the tier gives, as the guest reads it. Text shown, not rules enforced.",
    "items": {
     "type": "string"
    }
   },
   "earnMultiplier": {
    "type": "number",
    "nullable": true,
    "description": "Applied to every earn rule while the guest holds this tier. Null means 1."
   },
   "isActive": {
    "type": "boolean",
    "default": true
   }
  }
 },
 "MarketingReward": {
  "type": "object",
  "x-ticvai-persistence": "marketing.reward",
  "description": "**Taken from the backend workbook, 20 September.** Defines a loyalty reward that can be issued to eligible customers.",
  "required": [
   "loyaltyProgramId",
   "code",
   "name",
   "type",
   "isActive"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "loyaltyProgramId": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 100
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "type": {
    "type": "string",
    "maxLength": 30
   },
   "productId": {
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "pointsCost": {
    "type": "number",
    "nullable": true
   },
   "discountValue": {
    "type": "number",
    "nullable": true
   },
   "validityDays": {
    "type": "integer",
    "nullable": true
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "MetricValue": {
  "x-ticvai-persistence-column": "numeric(18,4)",
  "description": "**A reading of a metric or KPI, or a threshold on one.** A `Money` where the metric is money-valued — `MetricSource` lists those in `x-ticvai-money-valued`, and a KPI is when its `unit` is `currency` — and a plain number otherwise. naming-and-style 5.1: money is never a float, at any layer.\nStored as `numeric(18,4)` either way: a money value stores its amount, and currency and scale resolve from the scope as they do for every `Money`.\n",
  "oneOf": [
   {
    "type": "number"
   },
   {
    "$ref": "../shared/common.yaml#/components/schemas/Money"
   }
  ]
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
 "Referral": {
  "type": "object",
  "x-ticvai-persistence": "marketing.referral",
  "description": "BL-034. **No referrer, no reward, nothing anywhere.**\n**The reward fires on the referee's qualifying act, not on the sign-up**, because a referral that pays on registration pays for accounts rather than for guests.\n",
  "required": [
   "id",
   "referrerSubjectId",
   "code",
   "status"
  ],
  "properties": {
   "id": {
    "readOnly": true,
    "type": "string",
    "format": "uuid"
   },
   "referrerSubjectId": {
    "type": "string",
    "format": "uuid"
   },
   "refereeSubjectId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "code": {
    "readOnly": true,
    "type": "string"
   },
   "status": {
    "readOnly": true,
    "type": "string",
    "enum": [
     "issued",
     "registered",
     "qualified",
     "rewarded",
     "expired",
     "void"
    ]
   },
   "qualifyingAction": {
    "type": "string",
    "enum": [
     "firstPurchase",
     "firstVisit",
     "membershipPurchase"
    ]
   },
   "referrerRewardId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "refereeRewardId": {
    "readOnly": true,
    "type": "string",
    "format": "uuid",
    "nullable": true
   },
   "expiresAt": {
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
 "ReportResult": {
  "x-ticvai-persistence": "none — result set, cached in object storage",
  "type": "object",
  "required": [
   "executionId",
   "columns",
   "rows"
  ],
  "properties": {
   "executionId": {
    "type": "string"
   },
   "columns": {
    "type": "array",
    "items": {
     "type": "object",
     "properties": {
      "key": {
       "type": "string"
      },
      "label": {
       "type": "string"
      },
      "type": {
       "$ref": "#/components/schemas/FieldType"
      }
     }
    }
   },
   "rows": {
    "type": "array",
    "description": "**Open on purpose; the shape is `columns`.** Each row is keyed by `columns[].key`, and each value is of that column's `type` — money as a `Money`, dates, date-times and uuids as strings. A report's columns are chosen at run time, so no fixed schema can name them.\n",
    "items": {
     "type": "object",
     "additionalProperties": true
    }
   },
   "totals": {
    "type": "object",
    "additionalProperties": true,
    "description": "Aggregated columns only, keyed and typed as a row is."
   },
   "rowCount": {
    "type": "integer"
   },
   "nextCursor": {
    "type": "string",
    "nullable": true
   },
   "generatedAt": {
    "type": "string",
    "format": "date-time"
   },
   "dataAsOf": {
    "type": "string",
    "format": "date-time",
    "description": "Replica position the result was read at. Reporting reads a lag-tolerant replica, so this may trail the primary by seconds — stating it prevents an argument about a figure that moved.\n"
   }
  }
 }
}
```
