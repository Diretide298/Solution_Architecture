# Notification catalogue

**200 requirements mention a notification, and nothing mapped event to audience to
channel to consent.** `MessageTemplate` exists; the mapping did not.

## The four questions each notification must answer

**Which event fires it** — not which screen, because a notification triggered by a screen does
not fire when the same thing happens through the API.

**Who receives it** — resolved from scope and role at send time, never a stored list, because a
list goes stale the day someone changes department.

**Which channel** — and a channel that fails does not silently fall back. Email failing to send
is not push succeeding.

**Whether consent is needed.** **Transactional messages need none and marketing needs it**, and
the difference is whether the guest asked for the thing the message is about. A booking
confirmation is not marketing; a discount for next month is.

| Event | Audience | Channel | Consent | |
|---|---|---|---|---|
| `order.paid` | guest | email, push, wallet | transactional — no consent needed | Confirmation with the QR. **The one notification a guest will chase if it does not arrive** |
| `order.refunded` | guest | email | transactional | What was refunded, and to which method |
| `order.completed` | guest | push | transactional | Redeemed, so a guest checking their phone sees it used |
| `entitlement.issued` | guest | push, wallet | transactional | A pass added to a wallet |
| `access.validated` | — | none | — | **Deliberately silent.** Notifying a guest they walked through a gate is noise |
| `approval.granted` | staff | push, in-app | operational | The requester learns immediately — a cashier with a guest waiting |
| `approval.rejected` | staff | push, in-app | operational | **With the reason.** A rejection that says nothing sends the requester back to ask |
| `maintenance.assetReturnedToService` | staff | in-app | operational | The queue reopened and the ride is bookable |
| `maintenance.workOrderCompleted` | staff | in-app | operational | Waiting on verification |
| `fnb.orderReady` | guest | push | transactional | **Collect or being delivered.** Late is worse than none — food goes cold |
| `stock.depleted` | staff | in-app, email | operational | An item cannot be sold. Reaches the storekeeper, not everyone |
| `shift.closed` | staff | in-app | operational | Variance beyond threshold reaches a supervisor; within it reaches nobody |
| `ledger.periodClosed` | staff | email | operational | Finance, and anyone whose reports just became final |
| `tenant.suspended` | staff | email | operational | **Platform to tenant.** A commercial notice, not an operational one |
| `whitelabel.contentPublished` | — | none | — | Silent. A tenant publishing their own homepage does not need telling |
| `marketing.caseClosed` | guest | email | transactional | Resolution, and how to reopen |
| `seat.sold` | — | none | — | Silent. Covered by order.paid |
| `inventory.purchaseOrderReceived` | staff | in-app | operational | The requisitioner, and the technician whose job was blocked |

## The three silences are decisions

`access.validated`, `seat.sold` and `whitelabel.contentPublished` fire and notify nobody. **A
catalogue that only lists what sends cannot be reviewed** — the reader cannot tell whether an
absent notification was decided against or forgotten.

## Rules

**Quiet hours are a venue setting, and `emergency` ignores them.** A safety announcement at
03:00 reaches the night shift.

**Failure to deliver is recorded, not retried forever.** `marketing.message_delivery` carries
one row per recipient, and a bounce is a fact about a contact point rather than a transient
error.

**Language follows the recipient, not the venue.** A guest who bought in Arabic is told in
Arabic, and the template is per locale rather than translated at send.

## What is missing

| | |
|---|---|
| **Templates per locale** | `MessageTemplate` exists; **no template content is written**, in any language |
| **Provider** | No SMS or push provider named. CF-69 named DET and DCT and nothing for messaging |
| **Guest preference centre** | `WEB-020` draws it; per-category opt-out is not in the contract |
| **Retention of delivery records** | CF-64 again |
