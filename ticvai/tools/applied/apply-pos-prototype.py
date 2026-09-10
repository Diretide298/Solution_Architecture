#!/usr/bin/env python3
"""Take into P04 the five surfaces the POS Terminal prototype has and the package never drew.

**The prototype has been mined once, and only along the sell path.** Eighteen transitions on eleven
screens cite `board TICVAI POS Terminal` — how the cart reaches payment, what a hold carries, which
hot key recalls it. That work was real and is not repeated here.

**What it never took is the other half of the terminal.** The prototype's `NAV` names eleven
destinations and P04 has no equivalent for five of them:

| prototype | what it is | P04 before this |
|---|---|---|
| `home`    | the till launcher a cashier lands on | nothing — P04 had no entry surface of its own |
| `receipt` | reprint and reissue | nothing, though `reprintReceipt` has existed all along |
| `guests`  | guest lookup at the till | `identifyGuest` was called from the catalogue and had no screen |
| `tables`  | table service | nineteen table operations, not one of them on a till screen |
| `queue`   | the order queue | nineteen queue operations, same |

**Every operation these screens call already exists in the contracts.** Nothing here invents an
endpoint: the gap was never the API surface, it was that no screen reached for it. That is the
same finding as the device panel below, and it is the finding that matters — *the contract layer
was ahead of the screen layer, and only the screens are read by anyone drawing.*

**And the peripherals.** `TICVAI_Hardware_Integration v1.0.xlsx` lists fifteen integrations and
nothing in this package had ever opened it. Fourteen are modelled; the contracts carry a
twenty-value `DeviceKind` enum, richer than the prototype's six. But `receiptPrinter`, `cashDrawer`
and `customerDisplay` appeared in the contracts and **on no screen anywhere** — every device
operation sits on P08 back office or P06 staff app. **A cashier could not see whether their own
receipt printer was alive.** The prototype could, and gated the cash drawer's test kick behind a
permission while it was at it. That panel goes on `POS-016 Till Configuration`.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
P04 = ROOT / "screens" / "P04-point-of-sale.yaml"
HOME = "POS-025"

CITE = "board TICVAI POS Terminal"


def api(op, contract, purpose, trigger="onLoad"):
    return {"operationId": op, "contract": contract, "purpose": purpose, "trigger": trigger}


def states(subject: str, offline: str) -> dict:
    return {
        "loading": f"The saved {subject}.",
        "error": f"Could not load. Names which read failed and leaves the {subject} untouched.",
        "emptyFirstRun": f"No {subject} yet. Carries the create action and says what the till does "
                         f"in the meantime.",
        "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as "
                         "*there is no data* and sends somebody to support with the wrong question.",
        "offline": offline,
    }


def screen(sid, name, module, route, component, purpose, pattern, reason, apis, regions,
           st, exits, transitions, notes, params=None):
    s = {
        "id": sid,
        "name": name,
        "module": module,
        "wave": 1,
        "implementation": {"app": "venue-pos", "route": route,
                           "component": component, "status": "notStarted"},
        "navigation": {"entryFrom": [HOME] if sid != HOME else ["POS-001"],
                       "exitTo": exits, "transitions": transitions},
        "notes": notes,
        "density": "touchLarge",
        "pattern": pattern,
        "patternReason": reason,
        "purpose": purpose,
        "layout": {"template": "split", "regions": regions},
        "states": st,
        "apis": apis,
        "entryState": {
            "params": params or [{"name": "workstationId", "from": "session"}],
            "coldEntry": "**Resolves from the session, which carries the workstation** — a till is "
                         "signed into, not navigated to.",
        },
    }
    if sid == HOME:
        s["navigation"]["isEntryPoint"] = True
    return s


def region(slot, comps):
    return {"name": "contentBody", "slot": slot, "components": comps}


def comp(kind, label, binds=None):
    c = {"kind": kind, "label": label}
    if binds:
        c["bindsTo"] = binds
    return c


def build() -> list:
    """The five screens, each with the operations the contracts already carry."""
    out = []

    # ---------------------------------------------------------------- home
    out.append(screen(
        HOME, "Till Home", "Sell", "/home",
        "apps/venue-pos/src/routes/home/TillHomeBoard.tsx",
        "The surface a cashier lands on after opening a shift, and the one they return to between "
        "sales.",
        "dashboard",
        "`getCurrentShift` reads the one thing that is true right now and the tiles read counts — "
        "a dashboard, not a list",
        [api("getCurrentShift", "shift", "Whose shift this is and when it opened"),
         api("listSaleBoards", "sales", "Which sale boards this workstation may open"),
         api("getWorkstationHealth", "tenancy", "Whether the till and its peripherals are well"),
         api("listAlerts", "ops", "Anything the cashier must see before selling"),
         api("listDevices", "tenancy", "The peripherals bound to this workstation")],
        [region("summary", [
            comp("metricTile", "Shift takings so far", "Shift"),
            comp("metricTile", "Open holds", "Order"),
            comp("metricTile", "Queue waiting", "Queue"),
            comp("cardList", "Sale boards — tickets, F&B, retail", "SaleBoard"),
            comp("statusList", "Peripheral health", "DeviceBinding"),
            comp("alertBanner", "Alerts for this workstation", "Alert")])],
        states("till home", "**Working from the local journal.** The tiles show what this "
                            "workstation knows; the queue and alerts are last-known and say so."),
        ["POS-002", "POS-021", "POS-023", "POS-006", "POS-027", "POS-028", "POS-029",
         "POS-026", "POS-007"],
        [{"to": "POS-002", "trigger": "Tickets", "control": "cardList#saleBoards",
          "provenance": f"{CITE} · NAV entry `tickets` — the launcher's first tile"},
         {"to": "POS-021", "trigger": "F&B", "control": "cardList#saleBoards",
          "provenance": f"{CITE} · NAV entry `fnb`"},
         {"to": "POS-023", "trigger": "Retail", "control": "cardList#saleBoards",
          "provenance": f"{CITE} · NAV entry `retail`"},
         {"to": "POS-029", "trigger": "Queue", "control": "metricTile#queue",
          "provenance": f"{CITE} · NAV entry `queue`"},
         {"to": "POS-027", "trigger": "Guests", "control": "cardList#saleBoards",
          "provenance": f"{CITE} · NAV entry `guests`"},
         {"to": "POS-028", "trigger": "Tables", "control": "cardList#saleBoards",
          "provenance": f"{CITE} · NAV entry `tables`"},
         {"to": "POS-006", "trigger": "Held orders", "control": "metricTile#holds",
          "provenance": f"{CITE} · the launcher reaches holds directly"},
         {"to": "POS-007", "trigger": "Close shift", "guard": "shift.close",
          "provenance": f"{CITE} · NAV `closeout`"}],
        "**P04 had no entry surface.** Eleven of its screens declared `entryFrom: POS-001`, which "
        "is the sign-in — so the model said a cashier signs in and is somehow already inside a "
        "sale. The prototype's `home` is the missing step, and it is what makes the rail in "
        "`posPrimaryRail` mean something: **twelve screens named that set and shared no "
        "destination**, because the destination they share is this one."))

    # ---------------------------------------------------------------- receipt
    out.append(screen(
        "POS-026", "Receipt & Reprint", "Sell", "/sell/receipt",
        "apps/venue-pos/src/routes/sell/ReceiptReprintBoard.tsx",
        "Reprint a receipt or reissue an entitlement when the guest is still at the counter.",
        "detail",
        "One order is named and acted on — detail, not a list",
        [api("reprintReceipt", "sales", "Print the receipt again", "onAction"),
         api("reprintOrder", "sales", "Print the whole order again", "onAction"),
         api("reissueEntitlement", "ticketing", "Reissue the ticket or wristband", "onAction")],
        [region("detail", [
            comp("detailPanel", "The order, as it was sold", "Order"),
            comp("dataTable", "What was issued against it", "Entitlement"),
            comp("primaryButton", "Reprint receipt"),
            comp("secondaryButton", "Reissue entitlement")])],
        states("receipt", "**Reprint is available offline; reissue is not.** A reissue changes what "
                          "the gate will admit, and the gate cannot be told from here."),
        [HOME, "POS-011"],
        [{"to": "POS-011", "trigger": "This needs a refund, not a reprint",
          "provenance": f"{CITE} · `receipt` offers the refund path when a reprint is not the fix"}],
        "**`reprintReceipt` has existed in the contracts all along and no screen called it.** The "
        "prototype puts it at the counter because that is where the guest is standing — a reprint "
        "requested from the back office is a different, slower thing.",
        params=[{"name": "orderId", "from": "navigation"},
                {"name": "workstationId", "from": "session"}]))

    # ---------------------------------------------------------------- guests
    out.append(screen(
        "POS-027", "Guest Lookup", "Sell", "/sell/guests",
        "apps/venue-pos/src/routes/sell/GuestLookupBoard.tsx",
        "Find the guest in front of you, so the sale carries their entitlements and their wallet.",
        "listDetail",
        "`searchGuests` reads the population and `identifyGuest` reads one of them — list, select, act",
        [api("searchGuests", "crm", "Find a guest by name, phone or media"),
         api("identifyGuest", "crm", "Attach that guest to the sale", "onAction")],
        [region("collection", [
            comp("searchField", "Name, phone, booking reference or scan a wristband"),
            comp("dataTable", "Matching guests", "Guest"),
            comp("detailPanel", "Wallet, passes and open reservations", "Guest"),
            comp("primaryButton", "Attach to sale")])],
        states("guest lookup", "**Search needs the network.** A scanned wristband still resolves "
                               "offline against the local entitlement cache; a name search does not."),
        [HOME, "POS-002"],
        [{"to": "POS-002", "trigger": "Attach to sale", "control": "primaryButton#attach",
          "carries": ["guest", "workstationId"],
          "provenance": f"{CITE} · `guests` hands the identified guest back to the catalogue"}],
        "**`identifyGuest` was called from the catalogue and had no screen of its own**, so the "
        "model could attach a guest to a sale and could not say how the cashier found them. "
        "The prototype makes lookup a surface, which is also where the wallet and open "
        "reservations become visible before the sale rather than after it."))

    # ---------------------------------------------------------------- tables
    out.append(screen(
        "POS-028", "Table Service", "Sell", "/sell/tables",
        "apps/venue-pos/src/routes/sell/TableServiceBoard.tsx",
        "Open, move, merge and close table visits from the floor.",
        "board",
        "`getTableMap` reads a floor and the visits are worked on it — a board, not a table of rows",
        [api("getTableMap", "fnb", "The floor, as it is laid out"),
         api("listTableReservations", "fnb", "Who is booked and when"),
         api("openTableVisit", "fnb", "Seat a party", "onAction"),
         api("moveTableVisit", "fnb", "Move a party to another table", "onAction"),
         api("mergeTableVisits", "fnb", "Join two parties onto one bill", "onAction"),
         api("closeTableVisit", "fnb", "Close the visit and take payment", "onAction"),
         api("clearTable", "fnb", "Mark the table ready again", "onAction"),
         api("seatTableReservation", "fnb", "Seat a booked party", "onAction")],
        [region("board", [
            comp("cardList", "The floor", "Table"),
            comp("detailPanel", "The visit on the selected table", "TableVisit"),
            comp("dataTable", "Reservations due", "TableReservation"),
            comp("primaryButton", "Close visit & charge")])],
        states("floor", "**The floor is held locally and reconciles on sync.** Two tills moving the "
                        "same party while offline is the conflict this screen must survive."),
        [HOME, "POS-005", "POS-021"],
        [{"to": "POS-005", "trigger": "Close visit & charge",
          "control": "primaryButton#closeVisit", "guard": "payment.take",
          "carries": ["cart", "guest", "orderType", "table", "taxTotals"],
          "returnsTo": "POS-028",
          "provenance": f"{CITE} · `tables` closes into the same checkout the other boards use"},
         {"to": "POS-021", "trigger": "Add to this table's order",
          "provenance": f"{CITE} · `tables` sends the order to the F&B board"}],
        "**Nineteen table operations existed and not one was on a till screen.** The F&B pack drew "
        "table service on board 4 and the package put the operations in the contracts; the surface "
        "that uses them was never specified. A venue running table service had a kitchen display, "
        "a menu configuration screen and no way to seat a party."))

    # ---------------------------------------------------------------- queue
    out.append(screen(
        "POS-029", "Order Queue", "Sell", "/sell/queue",
        "apps/venue-pos/src/routes/sell/OrderQueueBoard.tsx",
        "Watch orders move from received to handed over, and act on the ones that stall.",
        "board",
        "Orders move between named stages and are acted on in place — a board",
        [api("listFnbOrders", "fnb", "Every order this outlet is working"),
         api("listQueueEntries", "queue", "Who is waiting and for how long"),
         api("getQueue", "queue", "The queue this workstation serves"),
         api("getQueueFeedHealth", "queue", "Whether the feed is current")],
        [region("board", [
            comp("cardList", "Orders by stage — received, preparing, ready, out, completed",
                 "FnbOrder"),
            comp("detailPanel", "The selected order", "FnbOrder"),
            comp("primaryButton", "Advance stage"),
            comp("statusList", "Feed health", "QueueFeed")])],
        states("queue", "**The queue is the one thing that must never look current when it is "
                        "not.** Offline, every card carries the time it was last known and the "
                        "advance action is withheld."),
        [HOME, "POS-022"],
        [{"to": "POS-022", "trigger": "Send to kitchen", "control": "primaryButton#advance",
          "provenance": f"{CITE} · STAGES[0].action is `Send to kitchen`"}],
        "**The prototype models five stages with the action that leaves each one** — received → "
        "*send to kitchen*, preparing → *mark ready*, ready → *dispatch / hand over*, out for "
        "delivery → *mark delivered*, completed → *reopen*. P04 had `listFnbOrders` and nineteen "
        "queue operations and no board to work them on."))

    return out


def device_panel(screens: dict) -> tuple:
    """The peripherals, on the till that owns them."""
    s = screens.get("POS-016")
    if not s:
        return None, []
    want = [
        api("listDevices", "tenancy", "The peripherals bound to this workstation"),
        api("setReaderScannerPeripheral", "tenancy", "Bind or replace a reader or scanner",
            "onAction"),
        api("recordDeviceHeartbeat", "tenancy", "Whether each peripheral is answering"),
    ]
    have = {a.get("operationId") for a in (s.get("apis") or [])}
    add = [a for a in want if a["operationId"] not in have]
    return s, add


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    doc = yaml.safe_load(P04.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in doc["screens"]}

    new = [s for s in build() if s["id"] not in by_id]
    target, add_apis = device_panel(by_id)

    if not new and not add_apis:
        print("nothing to do — the five prototype surfaces and the device panel are already in P04")
        return 0

    for s in new:
        print(f"  + {s['id']}  {s['name']:<22} {len(s['apis'])} operation(s), "
              f"{len(s['navigation']['transitions'])} labelled edge(s)")
    if add_apis:
        print(f"  ~ POS-016 Till Configuration — add {len(add_apis)} device operation(s): "
              + ", ".join(a["operationId"] for a in add_apis))

    if not apply:
        print("\nrun with --apply to write")
        return 0

    # **The launcher has to be reachable from the sign-in, or it is another orphan.**
    signin = by_id.get("POS-001")
    if signin and HOME not in ((signin.get("navigation") or {}).get("exitTo") or []):
        nav = signin.setdefault("navigation", {})
        nav.setdefault("exitTo", []).append(HOME)
        nav["exitTo"] = sorted(set(nav["exitTo"]))
        nav.setdefault("transitions", []).append({
            "to": HOME, "trigger": "Open shift",
            "provenance": f"{CITE} · `login` lands on `home`, not inside a sale"})

    for s in new:
        doc["screens"].append(s)
        # the destination has to know it can be arrived at
        for t in s["navigation"]["transitions"]:
            dst = by_id.get(str(t["to"]).partition("#")[0])
            if dst is not None:
                dnav = dst.setdefault("navigation", {})
                dnav["entryFrom"] = sorted(set((dnav.get("entryFrom") or []) + [s["id"]]))

    if add_apis:
        target.setdefault("apis", []).extend(add_apis)

    doc["screens"].sort(key=lambda s: s["id"])
    doc["platform"]["screenCount"] = len(doc["screens"])
    P04.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                   encoding="utf-8")
    print(f"\nP04 is now {len(doc['screens'])} screens — written")
    print("run tools/derive-id-register.py --apply, then tools/refresh.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
