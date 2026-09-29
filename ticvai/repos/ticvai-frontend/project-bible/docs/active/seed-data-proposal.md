# Seed data proposal: UAE denominations and default staff roles

> **Purpose:** The seed SETUP-SEED loads: the UAE cash denominations and the default staff role set  
> **Owner:** Chinmay  
> **Status:** **Proposed, client to correct (audit R229, decided 28 September 2026)**  
> **Who corrects it:** client operations and client finance

SETUP-SEED asks for staff roles and UAE denominations, and until now the package held neither. `shift.yaml`'s `Denomination` says *"the UAE set he supplied is the seed"* and quotes only its bad `Coin, 0, COIN` row. On 28 September Chinmay adopted our default: the list below is the seed, and the client corrects it.

---

## 1. UAE denominations (AED)

Loaded into `platform.denomination` through `setDenominations` (`shift.yaml`), one row per denomination, `currencyCode: AED`. Values are `Money` with scale 2. **There is no zero-valued coin**: the `Coin, 0, COIN` row in the supplied list was a transcription slip and is not seeded.

`sortOrder` is **counting order, not value order**: notes highest first, then coins as they sit in the tray. The coin order below is our guess at the tray; the client corrects it to match the drawers they use.

| sortOrder | kind | value (AED) | displayName (en) | displayName (ar) |
|---|---|---|---|---|
| 1 | note | 1000.00 | AED 1000 | 1000 درهم |
| 2 | note | 500.00 | AED 500 | 500 درهم |
| 3 | note | 200.00 | AED 200 | 200 درهم |
| 4 | note | 100.00 | AED 100 | 100 درهم |
| 5 | note | 50.00 | AED 50 | 50 درهم |
| 6 | note | 20.00 | AED 20 | 20 درهم |
| 7 | note | 10.00 | AED 10 | 10 دراهم |
| 8 | note | 5.00 | AED 5 | 5 دراهم |
| 9 | coin | 1.00 | AED 1 | 1 درهم |
| 10 | coin | 0.50 | 50 fils | 50 فلس |
| 11 | coin | 0.25 | 25 fils | 25 فلس |

All rows seed `isActive: true`. The 1, 5 and 10 fils coins are left out because they are not in everyday circulation. **If a venue still takes them, the client adds them here and they are seeded active.**

---

## 2. Default staff roles

Seeded as **system roles** (`Role.isSystem: true` in `identity.yaml`: editable, not deletable). The glossary rule still holds: **roles are fully configurable and nothing is predefined** (12 Aug 2026). These five are templates a tenant starts from and edits, not fixed roles.

Every permission below is from `contracts/shared/permissions.yaml`. **No tenant role holds a `PLATFORM_*` permission** or `DEVELOPER_ADMIN`: those are TICVAI-side only. A permission says *what*; the grant's scope says *where*, so the scope column is the level each role is normally granted at.

| Role | Normally granted at | Who holds it |
|---|---|---|
| **Cashier** | Venue | Sells, takes payment, runs their own shift and Deposit Box |
| **Supervisor** | Venue | Approves what a cashier cannot do alone; runs other people's shifts |
| **Venue Manager** | Venue | Configures and runs one venue; holds the manager approval level |
| **Finance** | Region (the ledger's level) | Journals, settlements, reconciliation, tax and accounts |
| **Tenant Admin** | Tenant | Users, roles, hierarchy, configuration and publishing. No selling |

### 2.1 Cashier

| Area | Permissions |
|---|---|
| Sales | `ORDER_VIEW`, `ORDER_CREATE`, `ORDER_MODIFY`, `ORDER_CANCEL`, `ORDER_REFUND` (subject to the venue's refund threshold), `ORDER_REPRINT`, `DISCOUNT_APPLY` |
| Catalogue | `PRODUCT_VIEW`, `PRICE_VIEW` |
| Shift and cash | `SHIFT_OPEN`, `SHIFT_CLOSE`, `SHIFT_SUSPEND`, `DEPOSIT_BOX_MODIFY_OWN`, `CASH_NO_SALE` (reason required, counted per shift) |
| Guests and stored value | `GUEST_VIEW`, `WALLET_VIEW`, `LOYALTY_REDEEM`, `TICKET_LOOKUP` |
| Everyday | `REPORT_VIEW_OWN`, `APPROVAL_REQUEST`, `INCIDENT_REPORT`, `ATTENDANCE_RECORD` |

### 2.2 Supervisor

Everything the Cashier holds, plus:

| Area | Permissions |
|---|---|
| Sales | `ORDER_VIEW_OTHER`, `ORDER_VOID`, `ORDER_DISCOUNT`, `ORDER_REFUND_APPROVE` (above threshold), `ORDER_EXCHANGE`, `ORDER_RESCHEDULE`, `PRICE_OVERRIDE` |
| Shift and cash | `SHIFT_CLOSE_OTHER`, `SHIFT_APPROVE_OPEN`, `SHIFT_APPROVE_CLOSE`, `CASH_LIFT`, `CASH_ADD`, `DEPOSIT_BOX_MODIFY_OTHER`, `OVERSHORT_ACCEPT` |
| Floor | `ACCESS_VALIDATE`, `ACCESS_OVERRIDE`, `QUEUE_VIEW`, `QUEUE_OVERRIDE`, `KIOSK_ATTEND`, `SESSION_FORCE_LOGOUT` |
| Approvals and reports | `APPROVAL_VIEW`, `APPROVAL_ACT`, `REPORT_VIEW_WORKSTATION`, `INCIDENT_VIEW` |

### 2.3 Venue Manager

Everything the Supervisor holds, plus:

| Area | Permissions |
|---|---|
| Sales and money | `ORDER_REFUND_BULK`, `CREDIT_OVERRIDE`, `PAYMENT_VIEW`, `PAYMENT_VOID`, `SHIFT_REOPEN`, `WALLET_OPERATE` |
| Catalogue and capacity | `PRODUCT_CONFIGURE`, `PRICE_CONFIGURE`, `EVENT_CONFIGURE`, `PERFORMANCE_CONFIGURE`, `CAPACITY_CONFIGURE` |
| Venue set-up | `WORKSTATION_CONFIGURE`, `ACCESS_POINT_CONFIGURE`, `TURNSTILE_MODE_SET`, `DEVICE_VIEW`, `DEVICE_CONFIGURE`, `QUEUE_MANAGE`, `SCOPE_VIEW` |
| People | `USER_MANAGE`, `PERMISSION_VIEW`, `PERMISSION_GRANT`, `WORKFORCE_VIEW`, `WORKFORCE_MANAGE`, `ANNOUNCEMENT_PUBLISH` |
| Guests | `GUEST_MANAGE`, `CASE_VIEW`, `CASE_MANAGE`, `MARKETING_VIEW` |
| Operations | `ASSET_VIEW`, `WORK_ORDER_VIEW`, `INCIDENT_MANAGE` |
| Approvals, reports, AI | `APPROVAL_DECIDE`, `APPROVAL_DELEGATE`, `REPORT_VIEW_VENUE`, `REPORT_EXPORT`, `REPORT_MANAGE`, `REPORT_SCHEDULE`, `AUDIT_VIEW`, `AI_USE`, `AI_APPROVE` |

`AI_APPROVE` sits here because an AI-proposed change touching prices or permissions needs a manager (audit R213 (3)).

### 2.4 Finance

| Area | Permissions |
|---|---|
| Ledger | `LEDGER_VIEW`, `LEDGER_POST`, `LEDGER_APPROVE`, `ACCOUNT_CONFIGURE`, `TAX_CONFIGURE` |
| Settlement | `SETTLEMENT_VIEW`, `SETTLEMENT_RECONCILE`, `PAYMENT_VIEW`, `PAYMENT_DISPUTE` |
| Credit and stored value | `CREDIT_MANAGE`, `WALLET_VIEW` |
| Reading | `ORDER_VIEW`, `ORDER_VIEW_OTHER`, `REPORT_VIEW_REGION`, `REPORT_EXPORT`, `REPORT_SCHEDULE`, `APPROVAL_VIEW`, `APPROVAL_ACT` |

**For the client to decide:** `createJournalEntry` says *"a finance user posts it; a finance manager or director approves it"* (12 Aug §15). If the client wants posting and approving held by different people, split this into **Finance** (without `LEDGER_APPROVE`) and **Finance Manager** (with it).

### 2.5 Tenant Admin

| Area | Permissions |
|---|---|
| Identity | `USER_MANAGE`, `ROLE_MANAGE`, `PERMISSION_VIEW`, `PERMISSION_GRANT`, `PERMISSION_MANAGE`, `SESSION_FORCE_LOGOUT` |
| Hierarchy and configuration | `SCOPE_VIEW`, `SCOPE_MANAGE`, `REGION_CONFIGURE`, `TENANT_CONFIGURE`, `TENANT_PUBLISH`, `WORKSTATION_CONFIGURE` |
| Devices and payments | `DEVICE_VIEW`, `DEVICE_CONFIGURE`, `DEVICE_MANAGE`, `PAYMENT_VIEW`, `PAYMENT_CONFIGURE`, `PAYMENT_PROVIDER_MANAGE` |
| Governance | `APPROVAL_CONFIGURE`, `AUDIT_VIEW`, `AI_CONFIGURE`, `AI_AUDIT_VIEW`, `REPORT_VIEW_TENANT` |
| Content and developers | `ASSET_LIBRARY_VIEW`, `ASSET_LIBRARY_MANAGE`, `ASSET_LIBRARY_APPROVE`, `DEVELOPER_VIEW`, `DEVELOPER_MANAGE` |

**The Tenant Admin does not sell, refund or touch cash.** Configuration and trading are held apart so that one person cannot create a price and then refund against it.

---

## 2a. Demo tenant: the Emirates Link transport network

**This goes to the demo tenant only** (decided 29 September, rev 3 REV3-21). A real venue starts with an empty network and enters its own in Venue Management, one item at a time or in bulk with `importTransportNetwork`. The values come from the client's rev 3 prototype (`sources/designs/guest-rev3-28-september/`), so the demo shows the same flow the client approved.

| What | Demo value |
|---|---|
| Line | E101, Sharjah – Dubai – Abu Dhabi, as two routes (outbound and inbound) paired for the swap button |
| Stations | The nine E101 stations of the prototype, from Sharjah Al Jubail to Abu Dhabi Central, with their coordinates for the route map |
| Fare | AED 5 plus AED 2.50 per stop |
| Passenger types | Adult (full fare), child (half), student (half), person of determination (free) |
| Pass types | 5-trip, 10-trip, weekly unlimited, monthly unlimited |
| Timetable | 23 departures a day |

The exact station list and times are read from the prototype when SETUP-SEED builds the demo tenant. `contracts/satellite/transport.yaml` describes the network model.

## 3. What happens next

1. The client corrects this page (denominations, tray order, the five roles and their permissions).
2. SETUP-SEED loads what is agreed. The seed lives with the tenant provisioning scripts, not in a contract.
3. `identity.yaml`'s `Role.isSystem` description names only *cashier* today; it should point at this list once agreed (handoff to the identity contract owner).
