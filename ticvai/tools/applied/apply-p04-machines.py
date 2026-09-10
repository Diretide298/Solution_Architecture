#!/usr/bin/env python3
"""Phase 0 §2.2 and §2.3 for P04 — the step machines, and what closing an overlay does.

**These machines are transcribed, not invented.** Every state and edge below was read off the
working POS prototype (`TICVAI POS Terminal (1) 1.html`, received 9 September 2026), where six of
them are implemented in JavaScript and declared nowhere: `payStage`, `closeStep`, `dstep`,
`reversalStage`, `netStatus`, and the top-level `screen`. The sixth is the platform's own
navigation and belongs in `navigation`, not here; the other five are screen state and are written
onto the five screens that hold them.

**Why `machine` is not `states`.** `states` is a rendering vocabulary — loading, empty, error,
offline, denied — and it is correct. It cannot say the thing that actually breaks a till: the
terminal charged a card and never answered, so the only safe move is to *inquire*, never retry,
because a retry takes the money twice. `payStage: unknown` says that. No value of `states` can.

**`dstep` is the four ticket-flow variants, in code.** The 3 August minute recorded them as
Admission → straight to quantity; Dated → date only; Timed → date then time; Seated → date, time,
then seat. The prototype implements exactly that as `detail → qty`, `detail → datetime → qty`,
`detail → zone → seats → qty`. It has been the shape of the sell flow since August and this is the
first time the package has said so.

Also here, because they are the same defect: five `onFailure` anchors pointing at states nobody
declared. Two are answered by `payStage` and are repointed at its real state names; three name
conditions that are genuinely rendering states and are declared as such.

Idempotent. Run with no arguments to see what it would do; `--apply` to write.
"""

from __future__ import annotations
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
P04 = ROOT / "screens" / "P04-point-of-sale.yaml"

PROTOTYPE = "prototype TICVAI POS Terminal, received 9 September 2026"
MINUTE = "minute 2026-08-03 §Ticket Flow Variations by Product Type"

# --------------------------------------------------------------------------- machines

MACHINES = {
    "POS-005": {
        "key": "payStage",
        "initial": "idle",
        "provenance": f"{PROTOTYPE} · payStage",
        "states": {
            "idle": {"note": "Nothing has been sent to the terminal yet."},
            "processing": {
                "operation": "createPayment",
                "note": "Authorisation in flight. **The idempotency key is minted here and "
                        "reused on every subsequent attempt** — it is what makes the inquiry "
                        "path safe.",
            },
            "unknown": {
                "note": "**The terminal charged a card and never answered.** Inquiry, never "
                        "retry: a retry takes the money a second time, and the guest is "
                        "standing there.",
            },
            "checking": {
                "operation": "inquirePaymentStatus",
                "note": "Asking the gateway what actually happened to the attempt.",
            },
            "completed": {
                "terminal": True,
                "goes": "POS-002",
                "note": "Settled. The till returns to the catalogue for the next sale.",
            },
            "failed": {
                "terminal": True,
                "retryTo": "idle",
                "note": "Declined or cancelled, and known to be so. Safe to take again.",
            },
        },
        "transitions": [
            {"from": "idle", "on": "Charge", "to": "processing"},
            {"from": "processing", "on": "approved", "to": "completed"},
            {"from": "processing", "on": "declined or cancelled", "to": "failed"},
            {"from": "processing", "on": "gatewayTimeout", "to": "unknown",
             "note": "The network dropped between the charge and the answer."},
            {"from": "unknown", "on": "Check status", "to": "checking"},
            {"from": "checking", "on": "settled", "to": "completed",
             "note": "Confirmed with the gateway — the payment succeeded and no duplicate "
                     "was created."},
            {"from": "checking", "on": "notFound", "to": "failed"},
        ],
    },
    "POS-007": {
        "key": "closeStep",
        "initial": "count",
        "provenance": f"{PROTOTYPE} · closeStep",
        "states": {
            "count": {"note": "Counting the drawer down, denomination by denomination, against "
                              "the float declared at open."},
            "variance": {"note": "**The count is outside tolerance.** A supervisor PIN is "
                                 "required before the shift can close, and the approval is "
                                 "recorded against their name."},
            "summary": {"operation": "closeShift",
                        "note": "The count is accepted. What is left is the close itself."},
        },
        "transitions": [
            {"from": "count", "on": "Next, within tolerance", "to": "summary"},
            {"from": "count", "on": "Next, outside tolerance", "to": "variance"},
            {"from": "variance", "on": "Supervisor PIN accepted", "to": "summary",
             "note": "Recorded as a cash variance in the audit trail, against the approver."},
            {"from": "summary", "on": "Back to count", "to": "count"},
        ],
    },
    "POS-002": {
        "key": "dstep",
        "initial": "detail",
        "provenance": f"{PROTOTYPE} · dstep · {MINUTE}",
        "states": {
            "detail": {"operation": "getProduct",
                       "note": "The ticket is chosen and its detail is open. Which step comes "
                               "next is decided by the product, not by the cashier."},
            "datetime": {"note": "Date, and for a timed product a session. **Dated products stop "
                                 "at the date**; timed ones carry on to the time."},
            "zone": {"note": "Which part of the house, before any individual seat."},
            "seats": {"note": "Individual seats within the chosen zone, held while the cashier "
                              "decides."},
            "qty": {"note": "Quantity by variant — adult, child, concession. **Every variant "
                            "arrives here**, whatever route it took."},
        },
        "transitions": [
            {"from": "detail", "on": "product is admission", "to": "qty",
             "note": "Admission — straight to quantity, no date at all."},
            {"from": "detail", "on": "product is dated or timed", "to": "datetime"},
            {"from": "detail", "on": "product is seated", "to": "zone"},
            {"from": "datetime", "on": "date and session chosen", "to": "qty"},
            {"from": "zone", "on": "zone chosen", "to": "seats"},
            {"from": "seats", "on": "seats picked", "to": "qty"},
        ],
    },
    "POS-011": {
        "key": "reversalStage",
        "initial": "requested",
        "provenance": f"{PROTOTYPE} · reversalStage",
        "states": {
            "requested": {"note": "A reversal has been asked for. **Whether the operator may "
                                  "approve their own is a policy question**, and the prototype "
                                  "checks it before offering the control."},
            "processing": {"operation": "createRefund",
                           "note": "The reversal is with the gateway."},
            "done": {"terminal": True,
                     "note": "Reversed, and written to the audit trail against the operator."},
        },
        "transitions": [
            {"from": "requested", "on": "Confirm reversal", "to": "processing"},
            {"from": "processing", "on": "gateway acknowledged", "to": "done"},
        ],
    },
    "POS-013": {
        "key": "netStatus",
        "initial": "online",
        "provenance": f"{PROTOTYPE} · netStatus",
        "states": {
            "online": {"operation": "syncOrders",
                       "note": "Connected. Anything queued while offline is replayed in order."},
            "offline": {"note": "**Selling continues.** Orders are written to the local queue "
                                "and carry a conflict status until they are replayed."},
        },
        "transitions": [
            {"from": "online", "on": "connection lost", "to": "offline"},
            {"from": "offline", "on": "connection restored", "to": "online"},
        ],
    },
}

# ------------------------------------------------------- states the transitions ask for

# **A failure path has to land somewhere that exists.** These three anchors were written by the
# transition work and named nothing; each is a genuine rendering state of the target screen.
STATES = {
    "POS-004": {"zoneUnavailable":
                "The zone sold out while the cashier was choosing. **The board refuses the zone "
                "rather than the sale** — the seat map reloads with that zone struck out and the "
                "cart intact."},
    "POS-007": {"awaitingApproval":
                "The close is waiting on a supervisor who is not at the till. The count is held; "
                "the drawer stays shut."},
    "POS-023": {"stockConflict":
                "The merchandise line went out of stock between scan and charge. The line is "
                "flagged and the rest of the sale stands."},
}

# `payStage` answers these two, under its own state names — the machine key already scopes them.
ANCHORS = {"POS-005#paymentFailed": "POS-005#failed",
           "POS-005#paymentUnknown": "POS-005#unknown"}

# ----------------------------------------------------------------- overlay confirm/dismiss

_STAY = "stays on the screen behind"

OVERLAYS = {
    "confirmVoidOrder": {
        "confirm": {"label": "Void", "operation": "voidOrder", "carries": ["orderId", "reason"]},
        "dismiss": {"label": "Keep the sale", "discards": ["reason"]},
    },
    "confirmCloseShift": {
        "confirm": {"label": "Close the shift", "operation": "closeShift",
                    "carries": ["shiftId", "countedFloat", "varianceReason"]},
        "dismiss": {"label": "Not yet", "discards": []},
    },
    "confirmSuspendShift": {
        "confirm": {"label": "Suspend", "operation": "suspendShift", "carries": ["shiftId"]},
        "dismiss": {"label": "Cancel", "discards": []},
    },
    "confirmCloseDepositBoxes": {
        "confirm": {"label": "Close the boxes", "operation": "closeDepositBoxes",
                    "carries": ["depositBoxIds"]},
        "dismiss": {"label": "Cancel", "discards": []},
    },
    "confirmWithdrawFromDepositBox": {
        "confirm": {"label": "Withdraw", "operation": "withdrawFromDepositBox",
                    "carries": ["depositBoxId", "amount"]},
        "dismiss": {"label": "Cancel", "discards": ["amount"]},
    },
    "confirmDeleteReport": {
        "confirm": {"label": "Delete", "operation": "deleteReport", "carries": ["reportId"]},
        "dismiss": {"label": "Keep", "discards": []},
    },
    # **The three drawers are the 3 August decision.** Each returns to the catalogue rather than
    # navigating away, and what it hands back is the whole reason it is a drawer and not a page.
    "drawerTicketDetail": {
        "confirm": {"label": "Continue", "to": "POS-002",
                    "carries": ["productId", "variantQty"]},
        "dismiss": {"label": "Close", "to": "POS-002", "discards": ["variantQty"]},
    },
    "drawerDateAndSession": {
        "confirm": {"label": "Continue", "to": "POS-002",
                    "carries": ["productId", "visitDate", "sessionTime"]},
        "dismiss": {"label": "Close", "to": "POS-002",
                    "carries": ["productId"], "discards": ["visitDate", "sessionTime"]},
    },
    "drawerSeatSelection": {
        "confirm": {"label": "Add to sale", "to": "POS-002",
                    "carries": ["productId", "performanceId", "seatPicks", "holdExpiresAt"]},
        "dismiss": {"label": "Close", "to": "POS-002",
                    "carries": ["productId"], "discards": ["seatPicks", "zoneId"]},
    },
}


def main() -> int:
    apply = "--apply" in sys.argv
    doc = yaml.safe_load(P04.read_text(encoding="utf-8"))
    by = {s["id"]: s for s in doc["screens"]}
    todo: list[str] = []

    for sid, machine in MACHINES.items():
        s = by.get(sid)
        if s is None:
            print(f"  !! {sid} is not in P04"); continue
        ops = {a.get("operationId") for a in (s.get("apis") or [])}
        for sname, sv in machine["states"].items():
            op = sv.get("operation")
            if op and op not in ops:
                # **Better to drop the citation than to write one the screen cannot honour.**
                print(f"  !! {sid} machine state {sname}: {op} not in apis[] — citation dropped")
                sv.pop("operation")
        if s.get("machine") == machine:
            continue
        todo.append(f"{sid}: machine {machine['key']} — {len(machine['states'])} states, "
                    f"{len(machine['transitions'])} transitions")
        if apply:
            s["machine"] = machine

    for sid, states in STATES.items():
        s = by.get(sid)
        if s is None:
            continue
        cur = s.setdefault("states", {})
        for sname, text in states.items():
            if cur.get(sname) == text:
                continue
            todo.append(f"{sid}: states.{sname}")
            if apply:
                cur[sname] = text

    fixed = 0
    for s in doc["screens"]:
        for t in ((s.get("navigation") or {}).get("transitions") or []):
            for f in (t.get("onFailure") or []):
                if f.get("to") in ANCHORS:
                    fixed += 1
                    if apply:
                        f["to"] = ANCHORS[f["to"]]
    if fixed:
        todo.append(f"repoint {fixed} onFailure anchor(s) onto payStage's own state names")

    for s in doc["screens"]:
        ops = {a.get("operationId") for a in (s.get("apis") or [])}
        for o in (s.get("overlays") or []):
            spec = OVERLAYS.get(o["id"])
            if not spec:
                continue
            for half in ("confirm", "dismiss"):
                block = {k: v for k, v in spec[half].items()}
                op = block.get("operation")
                if op and op not in ops:
                    print(f"  !! {s['id']} {o['id']}.{half}: {op} not in apis[] — citation dropped")
                    block.pop("operation")
                if o.get(half) == block:
                    continue
                todo.append(f"{s['id']} overlay {o['id']}.{half}")
                if apply:
                    o[half] = block

    if not todo:
        print("nothing to do — every machine, state and overlay return is already recorded")
        return 0

    print(f"{len(todo)} change(s){' applied' if apply else ' pending (run with --apply)'}:")
    for t in todo:
        print(f"  {t}")
    if apply:
        P04.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                       encoding="utf-8")
        print(f"\nwritten {P04}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
