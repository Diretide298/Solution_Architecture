# Report register

**133 requirements are primarily about a report.** CF-65 said 52 were named by title and
nothing listed them; counting properly found more, and split them in a way that matters.

| | | |
|---|---|---|
| **Engine capability** | **20** | Scheduling, export, saved formats, access rights, ranges. **Already contracted** |
| **Report definition** | **113** | A specific report a venue expects to exist. **Data, not code** |
| | **133** | |

## Why the split is the answer

A report engine and a report are different deliverables. **The engine is built once and the
reports are seeded**, and conflating them is why this looked like 133 units of work.

`reporting.yaml` has 23 operations covering definitions, parameters, fields, scheduling,
execution and export. **Every engine requirement above is already satisfied by it** — the
register below is what must exist *as data* on the day a venue opens.

**None of this is contract work.** It is a seeding task: each row becomes a
`reporting.report_definition` with its columns, filters and parameters, and `askReportingQuestion`
can generate most of them from the requirement text.

## Report definitions to seed

| Ref | Domain | Report | Reads |
|---|---|---|---|
| 12.1.48 | Accreditation & Creden | Accreditation utilization reporting - system shall provide accreditation utili | `— workshop-blocked` |
| 12.1.49 | Accreditation & Creden | Accreditation access reporting - system shall provide reports on accreditation | `— workshop-blocked` |
| 12.1.50 | Accreditation & Creden | Accreditation trend analysis - system shall provide accreditation trend report | `— workshop-blocked` |
| 12.1.51 | Accreditation & Creden | Accreditation audit reporting - system shall provide accreditation audit repor | `— workshop-blocked` |
| 12.1.7 | Accreditation & Creden | Accreditation reporting system shall provide reports on active, expired and re | `— workshop-blocked` |
| 3.2.65 | Admission and Access | An entry or exit report is expected presenting the readings per outcome (ok/ko | `access.scan_event` |
| 3.2.66 | Admission and Access | The in park report showing the difference between the entries and the exits | `access.scan_event` |
| 3.2.67 | Admission and Access | The entry report shall be linked to the revenue and present revenue per day | `access.scan_event` |
| 3.2.68 | Admission and Access | The length of stay report shall present the difference between the time in sca | `access.scan_event` |
| 3.3.38 | Admission and Access | Access investigation reporting - system shall provide reporting for access inv | `access.scan_event` |
| 3.3.48 | Admission and Access | Policy effectiveness reporting - system shall provide reporting on policy effe | `access.scan_event` |
| 3.6.15 | Admission and Access | The system shows if a coupon is redeemed or not, and a redemption report is av | `access.scan_event` |
| 3.7.11 | Admission and Access | System shall provide reporting on upsell impressions, conversion rates, revenu | `access.scan_event` |
| 11.1.26 | Approval Workflows & G | Approval history reporting - system shall provide historical reporting of appr | `approvals.request` |
| 11.1.49 | Approval Workflows & G | Escalation reporting - system shall provide escalation performance reporting | `approvals.request` |
| 11.1.70 | Approval Workflows & G | Approval volume analysis - system shall provide approval volume reporting | `approvals.request` |
| 11.1.71 | Approval Workflows & G | Approval trend analysis - system shall provide approval trend reporting | `approvals.request` |
| 4.3.36 | Bundles and Promotions | Gift card liability reporting system shall provide reporting of outstanding gi | `promotions.promotion, orders.order_discount` |
| 4.5.25 | Bundles and Promotions | Consolidated reporting across outlets | `promotions.promotion, orders.order_discount` |
| 4.9.12 | Bundles and Promotions | Print table management reports | `promotions.promotion, orders.order_discount` |
| 13.1.44 | Developer & API Manage | Api success rate reporting - system shall report api success rates | `— workshop-blocked` |
| 13.2.17 | Developer & API Manage | Sandbox usage analytics - system shall provide sandbox usage reporting | `— workshop-blocked` |
| 16.9.60 | Device Management | Device reporting - system shall provide device management reporting | `— workshop-blocked` |
| 18.4.1 | Employee Mobile App &  | Hazard reporting - users shall submit hazard reports | `workforce.attendance, maintenance.work_order` |
| 18.4.2 | Employee Mobile App &  | Incident reporting - users shall submit incident reports | `workforce.attendance, maintenance.work_order` |
| 18.4.3 | Employee Mobile App &  | Near-miss reporting - users shall submit near-miss reports | `workforce.attendance, maintenance.work_order` |
| 5.1.11 | F&B & Guest Management | Synchronize order statuses in real time between pos, kds, mobile ordering, qr | `fnb.fnb_order, orders.shift` |
| 5.12.6 | F&B & Guest Management | Financial reporting system shall provide deferred and recognized revenue repor | `fnb.fnb_order, orders.shift` |
| 5.12.61 | F&B & Guest Management | Suspense account reconciliation reporting | `fnb.fnb_order, orders.shift` |
| 5.6.28 | F&B & Guest Management | Reporting on wait times, abandonment rates, no-shows, throughput, utilization | `fnb.fnb_order, orders.shift` |
| 5.9.10 | F&B & Guest Management | The system should automatically generate consolidated payment reports each day | `fnb.fnb_order, orders.shift` |
| 5.9.3 | F&B & Guest Management | An end of shift report for the cashiers | `fnb.fnb_order, orders.shift` |
| 5.9.7 | F&B & Guest Management | A shift report with full transaction history | `fnb.fnb_order, orders.shift` |
| 5.9.9 | F&B & Guest Management | Generation of a temporary report at the closing of a session with total amount | `fnb.fnb_order, orders.shift` |
| 7.1.28 | F&B POS | Reports showing users, assigned roles, permissions, access rights, sensitive p | `fnb.fnb_order` |
| 7.1.59 | F&B POS | Investigation reports for failed access attempts, policy violations, override | `fnb.fnb_order` |
| 7.1.60 | F&B POS | Dashboards and reports measuring policy utilization, security incidents, compl | `fnb.fnb_order` |
| 7.5.7 | F&B POS | Track the complete invitation lifecycle from issuance to attendance | `fnb.fnb_order` |
| 15.1.27 | Inventory Management | Variance reporting - system shall provide stock variance reporting | `inventory.stock_level, inventory.movement` |
| 15.3.17 | Inventory Management | Supplier performance reports - system shall provide supplier reports | `inventory.stock_level, inventory.movement` |
| 17.5.3 | Maintenance & Safety M | Hazard reporting - system shall support hazard reporting | `maintenance.work_order, maintenance.asset` |
| 17.5.4 | Maintenance & Safety M | Incident reporting - system shall support incident reporting | `maintenance.work_order, maintenance.asset` |
| 17.5.5 | Maintenance & Safety M | Near-miss reporting - system shall support near-miss reporting | `maintenance.work_order, maintenance.asset` |
| 17.7.3 | Maintenance & Safety M | Asset performance reporting - system shall provide asset performance reports | `maintenance.work_order, maintenance.asset` |
| 17.7.5 | Maintenance & Safety M | Compliance reporting - system shall provide compliance reporting | `maintenance.work_order, maintenance.asset` |
| 22.13.17 | Marketing & CRM | Consent reporting system shall provide reports showing consent status, consent | `marketing.campaign, marketing.guest_profile` |
| 22.3.9 | Marketing & CRM | Case reporting & analytics system shall provide reporting and dashboards cover | `marketing.campaign, marketing.guest_profile` |
| 6.1.10 | Retail POS | Daily transactions summarized by | `retail.sale, orders.payment` |
| 6.1.11 | Retail POS | Specific transactions by | `retail.sale, orders.payment` |
| 6.1.17 | Retail POS | Discount types with pos id, staff info, date and time, ticket type, attraction | `retail.sale, orders.payment` |
| 6.1.18 | Retail POS | Run sales history reports based on multiple factors, including guest, item, da | `retail.sale, orders.payment` |
| 6.1.21 | Retail POS | Discrepancy report generated prior to making an inventory adjustment | `retail.sale, orders.payment` |
| 6.1.24 | Retail POS | Audit reporting for sales history | `retail.sale, orders.payment` |
| 6.1.27 | Retail POS | Reports for the external combo tickets which are sold with products/services + | `retail.sale, orders.payment` |
| 6.1.28 | Retail POS | A operational reporting view and extract options for | `retail.sale, orders.payment` |
| 6.1.29 | Retail POS | A void-check report for f&b outlets | `retail.sale, orders.payment` |
| 6.1.30 | Retail POS | All admission sales | `retail.sale, orders.payment` |
| 6.1.31 | Retail POS | All sales refund which consists of the ticket number, type of ticket (attracti | `retail.sale, orders.payment` |
| 6.1.32 | Retail POS | All sales by | `retail.sale, orders.payment` |
| 6.1.33 | Retail POS | The full reconciliations with payment gateway, refund, used, liability etc | `retail.sale, orders.payment` |
| 6.1.34 | Retail POS | Report that shows all bulk transaction details which are integrated with finan | `retail.sale, orders.payment` |
| 6.1.35 | Retail POS | Report that shows all pending transactions | `retail.sale, orders.payment` |
| 6.1.36 | Retail POS | The report that shows the sales transaction of the current month, while the re | `retail.sale, orders.payment` |
| 6.1.37 | Retail POS | Aging report for ticketing & reward age | `retail.sale, orders.payment` |
| 6.1.38 | Retail POS | F&b wastage | `retail.sale, orders.payment` |
| 6.1.39 | Retail POS | Aging stocks (comparison against defined/expiry vs actual) | `retail.sale, orders.payment` |
| 6.1.40 | Retail POS | Sales promotion with data consisting of promotion name /promotion code/ period | `retail.sale, orders.payment` |
| 6.1.41 | Retail POS | Daily, weekly and monthly reconciliation reports between (finance(erp) reporte | `retail.sale, orders.payment` |
| 6.1.42 | Retail POS | Corporate trade reports (ordered entity, validity , order qty, price, discount | `retail.sale, orders.payment` |
| 6.1.43 | Retail POS | Historical records up to 5 years for internal reporting requirements or as req | `retail.sale, orders.payment` |
| 6.1.44 | Retail POS | Staff performance report consisting of date/target/achievement/duty hours | `retail.sale, orders.payment` |
| 6.1.45 | Retail POS | Over all sales performance report consisting of location/ segment ( f&b, retai | `retail.sale, orders.payment` |
| 6.1.46 | Retail POS | The captured customer satisfaction feedback (based on number of stars or smile | `retail.sale, orders.payment` |
| 6.1.47 | Retail POS | Monthly , weekly and daily revenue reports with attributes of attraction name/ | `retail.sale, orders.payment` |
| 6.1.48 | Retail POS | Up-sell and cross-sell originating from | `retail.sale, orders.payment` |
| 6.1.49 | Retail POS | Refund control mechanism to ensure no commissions are added on refunds | `retail.sale, orders.payment` |
| 6.1.50 | Retail POS | Sales channel which includes | `retail.sale, orders.payment` |
| 6.1.51 | Retail POS | Profit center /cost center allocations for sub level attraction where applicab | `retail.sale, orders.payment` |
| 6.1.52 | Retail POS | Customized reports based on available fields and records | `retail.sale, orders.payment` |
| 6.1.53 | Retail POS | Report by meal type and quantity (daily, weekly and monthly) | `retail.sale, orders.payment` |
| 6.1.54 | Retail POS | Report by products (daily, weekly and monthly) | `retail.sale, orders.payment` |
| 6.1.55 | Retail POS | Statistics on | `retail.sale, orders.payment` |
| 6.1.57 | Retail POS | Exceptional reports when certain kpis are out of the range | `retail.sale, orders.payment` |
| 6.1.58 | Retail POS | Hourly foot fall reports with peak hours by attractions, f&b and retail etc | `retail.sale, orders.payment` |
| 6.1.59 | Retail POS | (daily, weekly and monthly) | `retail.sale, orders.payment` |
| 6.1.61 | Retail POS | A report for | `retail.sale, orders.payment` |
| 6.1.62 | Retail POS | A report for | `retail.sale, orders.payment` |
| 6.1.63 | Retail POS | A report consisting of average spend per hour for | `retail.sale, orders.payment` |
| 6.1.9 | Retail POS | Historical sales look up by item, ticket number etc | `retail.sale, orders.payment` |
| 21.12.1 | Seat Management & Venu | Seat occupancy reporting system shall support seat occupancy reporting | `seating.seat, orders.sales_order` |
| 21.12.2 | Seat Management & Venu | Zone performance reporting system shall support zone performance reporting | `seating.seat, orders.sales_order` |
| 21.12.3 | Seat Management & Venu | Revenue by section reporting system shall support revenue by section reporting | `seating.seat, orders.sales_order` |
| 21.12.4 | Seat Management & Venu | Revenue by seat category reporting system shall support revenue by seat catego | `seating.seat, orders.sales_order` |
| 21.12.6 | Seat Management & Venu | Hold inventory reporting system shall support hold inventory reporting | `seating.seat, orders.sales_order` |
| 1.2.69 | Ticketing Catalogue | System shall provide productivity reporting | `catalogue.product` |
| 1.6.15 | Ticketing Catalogue | System shall provide reporting for resale volume, resale revenue, commissions | `catalogue.product` |
| 2.14.17 | Ticketing Sales | Membership dashboards and kpis | `orders.sales_order, orders.payment` |
| 2.6.56 | Ticketing Sales | Consent audit trail maintain complete consent history | `orders.sales_order, orders.payment` |
| 2.7.45 | Ticketing Sales |  | `orders.sales_order, orders.payment` |
| 8.1.7 | Unified Operations Das | Ai usage analytics system shall provide reporting on ai usage and outcomes | `ledger.entry, access.scan_event` |
| 8.3.81 | Unified Operations Das | System shall support ai usage reporting | `ledger.entry, access.scan_event` |
| 8.4.14 | Unified Operations Das | System shall support ai-powered report generation | `ledger.entry, access.scan_event` |
| 8.5.28 | Unified Operations Das | System shall provide pricing performance reporting | `ledger.entry, access.scan_event` |
| 8.6.28 | Unified Operations Das | System shall support recommendation reporting | `ledger.entry, access.scan_event` |
| 8.7.11 | Unified Operations Das | System shall support self-service reporting | `ledger.entry, access.scan_event` |
| 8.7.12 | Unified Operations Das | System shall support drag-and-drop report creation | `ledger.entry, access.scan_event` |
| 8.7.13 | Unified Operations Das | System shall support ad-hoc reporting | `ledger.entry, access.scan_event` |
| 8.7.14 | Unified Operations Das | System shall support cross-domain reporting | `ledger.entry, access.scan_event` |
| 8.7.16 | Unified Operations Das | System shall support report subscriptions | `ledger.entry, access.scan_event` |
| 8.7.17 | Unified Operations Das | System shall support report sharing | `ledger.entry, access.scan_event` |
| 8.7.27 | Unified Operations Das | System shall support benchmark reporting | `ledger.entry, access.scan_event` |
| 8.7.30 | Unified Operations Das | System shall support natural language reporting | `ledger.entry, access.scan_event` |
| 8.7.32 | Unified Operations Das | System shall support report audit trails | `ledger.entry, access.scan_event` |

## Engine requirements, and the operation that satisfies each

| Ref | Requirement | Satisfied by |
|---|---|---|
| 2.6.64 | Administration portal administrators should be able to | `createReportSchedule` |
| 4.3.17 | Intensive reporting of all type of credits stored in the digital | `exportReportResult` |
| 6.1.13 | Management of access to reports based on group rights, operating | `x-ticvai-permission on every reporting operation` |
| 6.1.14 | Scheduling of report generation and delivery to web address loca | `createReportSchedule` |
| 6.1.15 | Report logs (e | `runReport` |
| 6.1.16 | The ability to configure reports required by finance (format to  | `exportReportResult` |
| 6.1.19 | Reporting ranges which allow for specific beginning/end points | `listReportFields` |
| 6.1.20 | All reporting functions should have export option to multiple fi | `exportReportResult` |
| 6.1.22 | Save report formats for recurring reports (e | `exportReportResult` |
| 6.1.23 | Tax reports in approved government formats for submittal | `exportReportResult` |
| 6.1.5 | Reports with admission types/information | `exportReportResult` |
| 6.1.56 | Daily revenue alerts in a mobile application format (dashboard i | `exportReportResult` |
| 6.1.6 | Use and allow standardized reporting structure/software | `runReport` |
| 6.1.60 | Reports on discount application and issuance | `exportReportResult` |
| 6.1.7 | Supporting nightly balancing | `exportReportResult` |
| 8.7.15 | System shall support report scheduling | `createReportSchedule` |
| 8.7.18 | System shall support report exports to excel | `exportReportResult` |
| 8.7.19 | System shall support report exports to pdf | `exportReportResult` |
| 8.7.20 | System shall support report exports through apis | `exportReportResult` |
| 8.9.10 | System shall provide dashboards, reports, drill-down analytics,  | `runReport` |

## What is still missing

**Two things, and neither is a contract.**

**Tax reports in approved government formats (6.1.23).** The format is a UAE FTA specification
nobody has supplied, and it is the one report where getting the layout wrong has a regulator
at the end of it. **Raised with the client rather than guessed.**

**Retention of five years for internal records (6.1.43).** Sits inside CF-64, which has no
answer yet.
