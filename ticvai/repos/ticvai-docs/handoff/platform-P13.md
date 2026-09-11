# P13 Venue CMS — platform

**Derived.** `python3 tools/derive-platform.py P13`. App `venue-management-web` · venue · web

| | |
|---|---|
| Screens | 100 |
| Operations | 122 |
| Contracts | 8 |
| Modules | 3 |
| Undrawn | 0 |
| Operations with no screen | 110 |
| Waves | wave2 20 · wave3 80 |

## Gaps

### 110 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `attachModifierGroup` | fnb | PUT | Give an item its choices |
| `closeCorrectiveAction` | fnb | POST | Close a signed finding |
| `createCombo` | fnb | POST | A meal deal, priced as one thing |
| `createModifierGroup` | fnb | POST | Create a modifier group |
| `createTable` | fnb | POST | A table as a thing, not an inference |
| `escalateCorrectiveAction` | fnb | POST | Escalate a finding |
| `getTableVisit` | fnb | GET | Read a visit with all its orders |
| `rebalanceStationLoad` | fnb | POST | Move work between stations mid-service |
| `recordCorrectiveAction` | fnb | POST | Record what was done about a finding |
| `requestBill` | fnb | POST | The party asked to pay |
| `resolveBookingConflict` | fnb | GET | Two bookings, one table — and what to do about it |
| `sendBookingConfirmation` | fnb | POST | Confirm a booking, and ask them to confirm back |
| `sendOrderNotification` | fnb | POST | Tell the guest where their order is |
| `setComboSlots` | fnb | PUT | What the guest chooses, and what it costs extra |
| `setKitchenSla` | fnb | PUT | How long a ticket may sit before it is late |
| `setSectionLayout` | fnb | PUT | Divide the floor into sections and give each a server |
| `updateTable` | fnb | PUT | Change what a table is |
| `setPasswordPolicy` | identity | PUT | Length, breach check, lockout and step-up |
| `setSegregationRules` | identity | PUT | Which permissions may not be held together |
| `updateMaintenancePlan` | maintenance | PATCH | Amend or suspend a plan |
| `activateJourney` | marketing-crm | POST | Start it, or stop it |
| `addGuestNote` | marketing-crm | POST | What the floor needs to know about this table |
| `addSuppression` | marketing-crm | POST | Suppress an address |
| `createChallenge` | marketing-crm | POST | Define a challenge, mission or streak |
| `createForm` | marketing-crm | POST | Define a waiver, survey or capture form |
| `createInvitationCampaign` | marketing-crm | POST | A quota-bounded, addressed invitation |
| `createLoyaltyProgramme` | marketing-crm | POST | Create a loyalty programme |
| `createUrlRedirect` | marketing-crm | POST | 301, 302 and custom redirects |
| `getJourneyPerformance` | marketing-crm | GET | Entrants, completions, goals reached |
| `getLostItemMatches` | marketing-crm | GET | Candidate matches, scored |
| `getSuppressionList` | marketing-crm | GET | Addresses suppressed from all sending |
| `listMessageTriggers` | marketing-crm | GET | What fires a message, and when |
| `listReviews` | marketing-crm | GET | List guest reviews and ratings |
| `listSegmentMembers` | marketing-crm | GET | List guests currently matching a segment |
| `recordLostItem` | marketing-crm | POST | Report something lost, or hand something in |
| `recordPrivacyIncident` | marketing-crm | POST | Log a personal-data breach and start the clock |
| `respondToReview` | marketing-crm | POST | Respond to a review |
| `retryMessageDispatch` | marketing-crm | POST | Send it again, or by another channel |
| `setCallDisposition` | marketing-crm | POST | Why the conversation ended, and any callback |
| `setMessageTrigger` | marketing-crm | POST | Fire a message from a platform event |
| … | | | 70 more |

## Modules

| Module | Screens | Waves |
|---|---|---|
| Policy | 40 | 3 |
| Media Library | 40 | 3 |
| White Label | 20 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `CMS-001` | Tenant Workspace | White Label | 2 | 21 | yes |
| `CMS-002` | Brand Kit | White Label | 2 | 4 | yes |
| `CMS-003` | Typography | White Label | 2 | 4 | yes |
| `CMS-004` | Logo & Assets | White Label | 2 | 7 | yes |
| `CMS-005` | Theme Editor | White Label | 2 | 2 | yes |
| `CMS-006` | Component Preview | White Label | 2 | 5 | yes |
| `CMS-007` | Page Builder | White Label | 2 | 2 | yes |
| `CMS-008` | Content Blocks | White Label | 2 | 2 | yes |
| `CMS-009` | Navigation & Menus | White Label | 2 | 5 | yes |
| `CMS-010` | Media Library | White Label | 2 | 12 | yes |
| `CMS-011` | Translations | White Label | 2 | 1 | yes |
| `CMS-012` | RTL Preview | White Label | 2 | 2 | yes |
| `CMS-013` | SEO & Metadata | White Label | 2 | 1 | yes |
| `CMS-014` | Publishing Workflow | White Label | 2 | 3 | yes |
| `CMS-015` | Version History | White Label | 2 | 3 | yes |
| `CMS-016` | Site Settings | White Label | 2 | 1 | yes |
| `CMS-017` | Domain & Certificate | White Label | 2 | 4 | yes |
| `CMS-018` | Consent & Legal | White Label | 2 | 11 | yes |
| `CMS-019` | User Access | White Label | 2 | 2 | yes |
| `CMS-020` | Change Log | White Label | 2 | 1 | yes |
| `CMS-021` | Privacy & Consent Configuration Command Center | Policy | 3 | 1 | yes |
| `CMS-022` | Data Processing Purpose & Lawful Basis Registry | Policy | 3 | 1 | yes |
| `CMS-023` | Consent Purpose & Consent Type Builder | Policy | 3 | 1 | yes |
| `CMS-024` | Communication Preference & Marketing Permission Configuration | Policy | 3 | 1 | yes |
| `CMS-025` | Cookie, Tracking & Digital Technology Registry | Policy | 3 | 1 | yes |
| `CMS-026` | Cookie Banner & Preference Center Designer | Policy | 3 | 1 | yes |
| `CMS-027` | Consent Capture Point & Customer Journey Configuration | Policy | 3 | 1 | yes |
| `CMS-028` | Privacy Notice, Policy & Terms Version Management | Policy | 3 | 1 | yes |
| `CMS-029` | Minor, Guardian & Age-Based Privacy Configuration | Policy | 3 | 1 | yes |
| `CMS-030` | Privacy Configuration Testing, Approval & Publication | Policy | 3 | 1 | yes |
| `CMS-031` | Privacy Operations Command Center | Policy | 3 | 1 | yes |
| `CMS-032` | Customer Privacy, Consent & Preference 360° | Policy | 3 | 1 | yes |
| `CMS-033` | Consent Evidence, History & Withdrawal Management | Policy | 3 | 1 | yes |
| `CMS-034` | Data Subject / Customer Privacy Request Management | Policy | 3 | 1 | yes |
| `CMS-035` | Data Discovery, Access, Export & Correction Workspace | Policy | 3 | 1 | yes |
| `CMS-036` | Deletion, Anonymization & Restriction Operations | Policy | 3 | 1 | yes |
| `CMS-037` | Data Retention, Expiry & Legal Hold Operations | Policy | 3 | 1 | yes |
| `CMS-038` | Privacy Compliance, Exception & Investigation Workspace | Policy | 3 | 1 | yes |
| `CMS-039` | Privacy Audit, Evidence & Compliance Reporting | Policy | 3 | 1 | yes |
| `CMS-040` | Privacy Analytics & AI Compliance Intelligence | Policy | 3 | 1 | yes |
| `CMS-041` | Waiver & Consent Command Center | Policy | 3 | 1 | yes |
| `CMS-042` | Waiver Template Library & Master Setup | Policy | 3 | 1 | yes |
| `CMS-043` | Digital Waiver & Form Builder | Policy | 3 | 1 | yes |
| `CMS-044` | Dynamic Fields, Questions & Conditional Logic | Policy | 3 | 1 | yes |
| `CMS-045` | Signatory, Signature & Guardian Rule Configuration | Policy | 3 | 1 | yes |
| `CMS-046` | Product, Event & Experience Association | Policy | 3 | 1 | yes |
| `CMS-047` | Waiver Trigger, Eligibility & Completion Rules | Policy | 3 | 1 | yes |
| `CMS-048` | Versioning, Effective Dates & Legal Change Control | Policy | 3 | 1 | yes |
| `CMS-049` | Localization, Branding & Customer Experience Configuration | Policy | 3 | 1 | yes |
| `CMS-050` | Waiver Approval, Testing & Publication Workspace | Policy | 3 | 1 | yes |
| `CMS-051` | Waiver Operations Command Center | Policy | 3 | 1 | yes |
| `CMS-052` | Participant Waiver Status & Tracking | Policy | 3 | 1 | yes |
| `CMS-053` | Digital Signing & Collection Operations | Policy | 3 | 1 | yes |
| `CMS-054` | Minor, Guardian & Group Consent Management | Policy | 3 | 1 | yes |
| `CMS-055` | Waiver Verification & Validation Workspace | Policy | 3 | 1 | yes |
| `CMS-056` | Missing, Expired & Invalid Waiver Management | Policy | 3 | 1 | yes |
| `CMS-057` | On-Site Waiver & Exception Handling | Policy | 3 | 1 | yes |
| `CMS-058` | Compliance Evidence, Audit & Waiver Repository | Policy | 3 | 1 | yes |
| `CMS-059` | Waiver Analytics, Compliance & Operational Insights | Policy | 3 | 1 | yes |
| `CMS-060` | AI Waiver Compliance & Risk Intelligence Center | Policy | 3 | 1 | yes |
| `CMS-061` | Digital Asset Management Command Center | Media Library | 3 | 0 | yes |
| `CMS-062` | Central Digital Asset Library | Media Library | 3 | 0 | yes |
| `CMS-063` | Upload & Asset Ingestion Workspace | Media Library | 3 | 0 | yes |
| `CMS-064` | Folder, Collection & Workspace Management | Media Library | 3 | 0 | yes |
| `CMS-065` | Metadata & Taxonomy Management | Media Library | 3 | 0 | yes |
| `CMS-066` | Tags, Keywords & Classification | Media Library | 3 | 0 | yes |
| `CMS-067` | Advanced Search & Discovery | Media Library | 3 | 0 | yes |
| `CMS-068` | Digital Asset 360° Profile | Media Library | 3 | 0 | yes |
| `CMS-069` | Bulk Asset Management Workspace | Media Library | 3 | 0 | yes |
| `CMS-070` | Asset Activity, Recent Assets & Library Health | Media Library | 3 | 0 | yes |
| `CMS-071` | AI Asset Intelligence Command Center | Media Library | 3 | 0 | yes |
| `CMS-072` | AI Auto-Tagging & Content Understanding | Media Library | 3 | 0 | yes |
| `CMS-073` | Semantic & Natural-Language Asset Search | Media Library | 3 | 0 | yes |
| `CMS-074` | Visual Similarity & Related Asset Discovery | Media Library | 3 | 0 | yes |
| `CMS-075` | Duplicate & Near-Duplicate Management | Media Library | 3 | 0 | yes |
| `CMS-076` | Asset Version Control & Revision History | Media Library | 3 | 0 | yes |
| `CMS-077` | Version Comparison & Replacement Impact | Media Library | 3 | 0 | yes |
| `CMS-078` | Transformation & Rendition Management | Media Library | 3 | 0 | yes |
| `CMS-079` | Rendition Processing & Delivery Readiness | Media Library | 3 | 0 | yes |
| `CMS-080` | AI Quality, Intelligence Review & Recommendations | Media Library | 3 | 0 | yes |
| `CMS-081` | DAM Governance & Rights Command Center | Media Library | 3 | 0 | yes |
| `CMS-082` | Asset Ownership & Responsibility Management | Media Library | 3 | 0 | yes |
| `CMS-083` | Rights, License & Usage Policy Management | Media Library | 3 | 0 | yes |
| `CMS-084` | Asset Approval Workflow Management | Media Library | 3 | 0 | yes |
| `CMS-085` | Publication Eligibility & Governance Validation | Media Library | 3 | 0 | yes |
| `CMS-086` | Role-Based Asset Access & Permission Management | Media Library | 3 | 0 | yes |
| `CMS-087` | Secure Internal & External Sharing | Media Library | 3 | 0 | yes |
| `CMS-088` | Rights Expiry, Renewal & Usage Impact | Media Library | 3 | 0 | yes |
| `CMS-089` | Governance Audit Trail & Compliance Evidence | Media Library | 3 | 0 | yes |
| `CMS-090` | Governance Risk, Compliance & AI Recommendations | Media Library | 3 | 0 | yes |
| `CMS-091` | Asset Distribution & Delivery Command Center | Media Library | 3 | 0 | yes |
| `CMS-092` | Asset Usage & Distribution Map | Media Library | 3 | 0 | yes |
| `CMS-093` | Channel & Distribution Configuration | Media Library | 3 | 0 | yes |
| `CMS-094` | Secure Delivery URL, CDN & Rendition Delivery | Media Library | 3 | 0 | yes |
| `CMS-095` | Asset Replacement & Propagation Management | Media Library | 3 | 0 | yes |
| `CMS-096` | Fallback, Expiry & Distribution Continuity | Media Library | 3 | 0 | yes |
| `CMS-097` | DAM API & Integration Hub | Media Library | 3 | 0 | yes |
| `CMS-098` | Delivery Monitoring & Integration Health | Media Library | 3 | 0 | yes |
| `CMS-099` | Asset Usage & Performance Analytics | Media Library | 3 | 0 | yes |
| `CMS-100` | Distribution Intelligence, AI Insights & Optimization | Media Library | 3 | 0 | yes |

