# Partner portal: added when the B2B option is finalised

> **Logged:** 30 September 2026
> **Status:** Parked. No operation, backlog entry, ticket or plan hours exist for these yet.
> **Trigger:** the client picks Option A, Option B or both (MoM 29 September, section 3). Then each item below becomes a contract backlog entry, its operations and its P10 tasks. After that, re-run `tools/refresh.sh` and `tools/build-plan-deck.py` so the hours land in B2.

## For Claude Design

Draw these controls greyed out in both option files and list them in `return/FINDINGS.md`. Do not invent endpoints for them. When the option is finalised, the greyed controls become live in the one working file for that option.

## For us

| # | Gap | Needed when | What gets added | Open question |
|---|---|---|---|---|
| PA-1 | **Partner cash drawer.** No partner-side cash operation. The POS shift operations (`recordNoSale`, `listCashMovements`) are for venue staff. | Option A only | Partner shift open and close, cash in and out, and a list of cash movements, scoped to the partner's branch rather than the venue's shifts. | None, once Option A is chosen. |
| PA-2 | **Sent-ticket history.** No operation lists the messages sent for a partner's orders. `getMessageStatus` reads one message. | Either option | A paged list of the messages sent for the partner's orders: recipient, channel, sent time and status, built on the existing messaging data. | None. |
| PA-3 | **"Opened" delivery status.** Nothing reports that a guest opened a sent ticket. The portals show sent and used only. | Either option, if wanted | An `opened` message status, fed by the email and SMS providers' delivery events. | Whether our providers report opens, and the client's consent position on open tracking. |
