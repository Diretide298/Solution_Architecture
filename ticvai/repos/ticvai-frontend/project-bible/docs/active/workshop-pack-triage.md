# Workshop pack — triage

**590 screens across 59 boards, held against the 500 the package already has.** Produced by
`tools/parse-workshop-pack.py` and `tools/check-screen-redundancy.py --pack`; regenerate both
rather than editing this file.

**This is a review queue, not a verdict.** A screen parsed from a PDF has no operations, and
operations are what decide whether two screens are the same. The scores below rank a shortlist
for a person; they do not settle anything on their own.

---

## Per module

| Module | Boards | Screens | Check first | Check | No near match |
|---|---:|---:|---:|---:|---:|
| Promotions   Bundles Management | 10 | 100 | 6 | 12 | 82 |
| Access Control Module | 12 | 120 | 5 | 12 | 103 |
| Sales Channel Management | 2 | 20 | 2 | 7 | 11 |
| B2B, Reseller & OTA Partner Management | 3 | 30 | 3 | 5 | 22 |
| Pricing   Revenue Management | 7 | 70 | 3 | 4 | 63 |
| Product Lifecycle   Catalogue Governance | 2 | 20 | 2 | 3 | 15 |
| Customer Service | 2 | 20 | 0 | 4 | 16 |
| Communication & Notification Platform Services | 1 | 10 | 1 | 2 | 7 |
| Order   Reservation Management | 3 | 30 | 1 | 2 | 27 |
| Ticket Media   Credential Management | 3 | 30 | 1 | 2 | 27 |
| Privacy  Consent   Preference Management | 2 | 20 | 1 | 1 | 18 |
| Ticket Resale Marketplace | 3 | 30 | 0 | 2 | 28 |
| Group Sales   Corporate Booking Management | 2 | 20 | 0 | 1 | 19 |
| Rules  Workflow  Approval   Automation Engine | 2 | 20 | 1 | 0 | 19 |
| Waiver, Consent & Digital Form Management | 2 | 20 | 0 | 1 | 19 |
| Membership   Annual Pass Management | 2 | 20 | 0 | 0 | 20 |
| Ticket Upgrade, Exchange & Conversion | 1 | 10 | 0 | 0 | 10 |
| **Total** | **59** | **590** | **26** | **58** | **506** |

## The 26 to check first

| Pack screen | Module | Closest built screen | Score |
|---|---|---|---:|
| Consent Capture Point & Customer Journey Configuration | Privacy  Consent   Preference  | `GST-065` Newsletter & Preferences | 0.24 |
| Commission Calculation & Settlement Management | B2B, Reseller & OTA Partner Ma | `PTR-011` Quote Management | 0.22 |
| Reader, Scanner & Peripheral Configuration | Access Control Module | `BO-127` Hardware & Peripherals Management | 0.22 |
| Channel Pricing & Commercial Profile Assignment | Sales Channel Management | `WEB-035` Multi-Currency & Pricing | 0.20 |
| Upsell, Cross-Sell & Attach-Rate Analytics | Promotions   Bundles Managemen | `BO-119` Cross-Sell, Upsell & Recommendation Rules | 0.20 |
| Channel Fees, Payment & Fulfillment Configuration | Sales Channel Management | `GST-018` Add to Calendar / Reminders | 0.20 |
| Membership & Loyalty Pricing Rules | Pricing   Revenue Management | `GST-036` Loyalty & Rewards | 0.20 |
| Approval Inbox & Decision Workspace | Promotions   Bundles Managemen | `BO-084` Approval Inbox | 0.20 |
| Redemption, Conversion & Funnel Analytics | Promotions   Bundles Managemen | `BO-121` Personalized Offers & Guest Engagement | 0.20 |
| Market, Venue & Currency Pricing Structure | Pricing   Revenue Management | `WEB-035` Multi-Currency & Pricing | 0.20 |
| Bulk Product Creation & Catalogue Import | Product Lifecycle   Catalogue  | `BO-117` Product Import, Governance & AI Configuration Assistant | 0.20 |
| Partner Access, Roles & Permission Profile | B2B, Reseller & OTA Partner Ma | `PTR-020` Sub-Agent Management | 0.19 |
| Graphical Access Map & Live Gate Performance | Access Control Module | `EMP-030` Venue map | 0.19 |
| Partner Contacts & User Administration | B2B, Reseller & OTA Partner Ma | `SUP-001` Agent Login | 0.19 |
| Provider Health, Usage & Cost Monitoring | Communication & Notification P | `ADM-015` API Rate Limit & Quota Management | 0.19 |
| Promotion Approval Inbox | Promotions   Bundles Managemen | `BO-084` Approval Inbox | 0.19 |
| Live Access Operations Command Center | Access Control Module | `GST-046` Branded Queue / Waiting Room | 0.19 |
| Rate Structure Builder | Pricing   Revenue Management | `WEB-035` Multi-Currency & Pricing | 0.19 |
| Roles, Authority, Delegation & Approval Limits | Rules  Workflow  Approval   Au | `BO-087` Approval Delegations | 0.19 |
| Connectivity Failure & Degraded Mode Policy | Access Control Module | `BO-131` Connectivity & Auto-Switch Settings | 0.18 |
| Code Eligibility & Restriction Manager | Promotions   Bundles Managemen | `GST-015` Memberships | 0.18 |
| Guest Choice & Build-Your-Own Bundle Designer | Promotions   Bundles Managemen | `GST-053` Build Your Own Itinerary | 0.18 |
| Payment Reconciliation & Exception Management | Order   Reservation Management | `BO-025` Chargebacks & Disputes | 0.18 |
| Media Replacement, Revocation & Rebinding Rules | Ticket Media   Credential Mana | `BO-027` Reissue & Media Replacement | 0.18 |
| Live Venue Occupancy & People Counting | Access Control Module | `GST-004` Attraction Details | 0.18 |
| Product Retirement, Suspension & Archive | Product Lifecycle   Catalogue  | `ADM-036` Platform Notification Broadcast | 0.18 |
