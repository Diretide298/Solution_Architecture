#!/usr/bin/env python3
"""The guest and kiosk cross-check of 3 October 2026 (CHG-R1S-022, CHG-R1S-023).

**From the lead's design-batch cross-check, 3 October** (the kiosk is drawn in full now):

* **Flow steps that call what their screen does not bind** (CHG-R1S-023): WEB-005 adds the chosen tickets to the
  cart (`addCartLine`); WEB-011 extends the seat hold once at the warning (`extendSeatHold`, made guest-callable
  within the guest's own session, as `createSeatHold` is: Pattern 4 group 3); KSK-014 reads the app status that
  takes it out of service (`getTenantAppStatus`); KSK-015 adds what the assistant suggests (`addCartLine`); KSK-013
  hands the guest to a person (`handoverToAgent`).
* **The eleven open process-notes corrections on kiosk screens** (CHG-R1S-022, `handoff/design-notes/`), applied
  and marked `status: fixed`.

Screens are spliced one at a time by the 3 October pattern fix's writer; contracts and notes by exact text.
Idempotent.

    python tools/applied/guest-kiosk-3-october.py [--apply]
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
_spec = importlib.util.spec_from_file_location("spf", HERE / "spec-screen-patterns-3-october.py")
spf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(spf)

C22, C23 = "CHG-R1S-022", "CHG-R1S-023"
P22 = f"design cross-check, 3 October 2026 ({C22})"
P23 = f"design cross-check, 3 October 2026 ({C23})"


def api(s, oid, contract, purpose, trigger, prov):
    if any(a.get("operationId") == oid for a in s.get("apis") or []):
        return False
    s.setdefault("apis", []).append({"operationId": oid, "contract": contract, "purpose": purpose,
                                     "trigger": trigger, "provenance": prov})
    return True


def comps(s):
    for r in (s.get("layout") or {}).get("regions") or []:
        for c in r.get("components") or []:
            yield r, c


def region(s, name="contentBody"):
    for r in (s.get("layout") or {}).get("regions") or []:
        if r.get("name") == name:
            return r
    r = {"name": name, "slot": "record", "components": []}
    s.setdefault("layout", {"template": "detail", "regions": []})["regions"].append(r)
    return r


def screens(F, log):
    S = F.screens

    def touch(sid, what):
        F.dirty.add(sid)
        log.append(f"{sid}: {what}")

    # ── CHG-R1S-023: flow steps' operations bound on their screens ──
    if api(S["WEB-005"], "addCartLine", "orders", "Continue adds the chosen tickets to the cart", "onAction", P23):
        touch("WEB-005", "+ addCartLine")
    if api(S["WEB-011"], "extendSeatHold", "seating",
           "Extend the seat hold once, from the warning before it lapses", "onAction", P23):
        touch("WEB-011", "+ extendSeatHold")
    if api(S["KSK-015"], "addCartLine", "orders", "Add what the assistant suggests to the basket", "onAction", P23):
        touch("KSK-015", "+ addCartLine")

    # KSK-013 Call staff: something calls a person (correction + flow F75); the kiosk's conversation arrives
    # with the screen (conversationId), so no conversation is opened here
    s = S["KSK-013"]
    if any(x.get("operationId") == "createAiConversation" for x in s.get("apis") or []):
        s["apis"] = [x for x in s["apis"] if x.get("operationId") != "createAiConversation"]
        touch("KSK-013", "- createAiConversation")
    # a binding is reached by a control (check-screen-wiring S-OP-UNREACHED)
    for sid, oid, kind, label in (("WEB-005", "addCartLine", "primaryButton", "Continue"),
                                  ("WEB-011", "extendSeatHold", "secondaryButton", "Keep my seats longer"),
                                  ("KSK-015", "addCartLine", "secondaryButton", "Add to basket")):
        s = S[sid]
        if any(c.get("operation") == oid for _, c in comps(s)):
            continue
        hit = next((c for _, c in comps(s) if c.get("kind") == kind and c.get("label") == label
                    and not c.get("operation")), None)
        if hit:
            hit["operation"] = oid
        else:
            region(s, "actionBar").setdefault("components", []).append(
                {"kind": kind, "label": label, "operation": oid, "provenance": P23})
        touch(sid, f"control reaches {oid}")
    if api(s, "handoverToAgent", "marketing-crm",
           "Call a member of staff: the conversation goes to the agent workspace (BO-799), where staff join "
           "with startKioskAssist", "onAction", P22):
        r = region(s, "actionBar")
        r.setdefault("components", []).insert(0, {
            "kind": "primaryButton", "label": "Call a member of staff", "operation": "handoverToAgent",
            "notes": "Hands the kiosk's conversation to a person; the agent workspace (BO-799) shows it and staff "
                     "help remotely with startKioskAssist. The guest sees who is helping and can end it "
                     f"(endKioskAssist) ({C22}).", "provenance": P22})
        s["gaps"] = [g for g in s.get("gaps") or [] if g.get("operation") != "endKioskAssist"]
        for _, c in comps(s):
            if c.get("operation") == "endKioskAssist":
                c["label"] = "End the help session"
        touch("KSK-013", "+ handoverToAgent, call button")

    # KSK-014 Out of service: the status that takes it out of service
    s = S["KSK-014"]
    if api(s, "getTenantAppStatus", "white-label",
           "Read whether the app is in service; the screen leaves when it is back", "onLoad", P22):
        s["gaps"] = [g for g in s.get("gaps") or [] if g.get("operation") is not None]
        region(s)["components"].append({
            "kind": "banner", "label": "Out of service", "operation": "getTenantAppStatus",
            "notes": "Shown while the tenant's app status or this kiosk's own health (its heartbeat, "
                     "recordDeviceHeartbeat) says it cannot sell; polled, and the attract loop returns when both "
                     f"clear ({C22}).", "provenance": P22})
        touch("KSK-014", "+ getTenantAppStatus")

    # KSK-001 Attract loop: the venue's products and media fill it
    s = S["KSK-001"]
    if api(s, "listProducts", "catalogue", "Fill the loop with the venue's products and their media", "onLoad", P22):
        s["gaps"] = [g for g in s.get("gaps") or [] if g.get("operation") is not None]
        region(s)["components"].append({
            "kind": "cardList", "label": "What's on", "operation": "listProducts", "bindsTo": "Product",
            "columns": ["Product.name", "Product.media"],
            "notes": f"Published products only, primary media first; a touch opens the language choice ({C22}).",
            "provenance": P22})
        touch("KSK-001", "+ listProducts loop")

    # KSK-006 Review: lines are added before, offers apply on their own
    s = S["KSK-006"]
    before = len(s.get("apis") or [])
    s["apis"] = [a for a in s.get("apis") or [] if a.get("operationId") not in ("addCartLine", "evaluatePromotions")]
    if len(s["apis"]) != before:
        for r in (s.get("layout") or {}).get("regions") or []:
            keep = []
            for c in r.get("components") or []:
                if c.get("operation") == "addCartLine":
                    continue
                if c.get("operation") == "evaluatePromotions":
                    c["operation"] = "getCart"
                    c["notes"] = ("The offers the cart already carries (`Cart.discountTotal`): promotions apply on "
                                  f"their own, nothing is pressed ({C22}).")
                keep.append(c)
            r["components"] = keep
        touch("KSK-006", "- addCartLine, - evaluatePromotions")

    # a button is not a form (check-screen-wiring S-BUTTON-FORM): the kiosk's two calls with a body say
    # what they send, and the guest types nothing
    for sid, oid, label, body in (
            ("KSK-006", "checkoutCart", "Pay",
             "**Confirms the basket before payment; the guest types nothing.** The kiosk sends the cart it holds "
             "and its sales channel; offers are already on the cart. Then the terminal takes the payment (KSK-007)."),
            ("KSK-013", "handoverToAgent", "Call a member of staff",
             "**Asks what the guest needs help with, in one tap** (paying, finding a booking, something else); "
             "the kiosk sends its conversation and that reason, and a member of staff joins from the agent "
             "workspace (BO-799)."),
            ("KSK-015", "addCartLine", "Add to basket",
             "**Confirms what the assistant suggested: the item and how many** (a quantity stepper, 1 by default); "
             "the kiosk sends its cart, the product or variant the answer named, and the quantity.")):
        s = S[sid]
        if not any((o.get("confirm") or {}).get("operation") == oid for o in s.get("overlays") or []):
            s.setdefault("overlays", []).append({
                "id": "form" + oid[0].upper() + oid[1:], "component": "modal", "trigger": label,
                "body": body + f" ({C22})", "confirm": {"label": label, "operation": oid},
                "dismiss": {"label": "Back"}, "provenance": P22})
            touch(sid, f"overlay for {oid}")

    # KSK-008 Payment unresolved: a status, not an editor
    s = S["KSK-008"]
    if s.get("pattern") != "statusTracker":
        s["pattern"] = "statusTracker"
        s["patternReason"] = ("`inquirePaymentStatus` asks the provider what became of one payment; the screen shows "
                              f"the answer, it edits nothing ({C22})")
        s["gaps"] = [g for g in s.get("gaps") or [] if g.get("operation") != "inquirePaymentStatus"]
        for _, c in comps(s):
            if c.get("operation") == "inquirePaymentStatus":
                c["label"] = "Check the payment again"
        touch("KSK-008", "status, not editor")

    # KSK-011 Collect a booking: ticketing, not retail; no plumbing on a kiosk
    s = S["KSK-011"]
    if s.get("requiresModule") == "retail":
        s["requiresModule"] = "core"
        s["apis"] = [a for a in s.get("apis") or [] if a.get("operationId") != "lookupShopAndDrop"]
        for r in (s.get("layout") or {}).get("regions") or []:
            keep = []
            for c in r.get("components") or []:
                if c.get("operation") == "lookupShopAndDrop":
                    continue
                if c.get("kind") == "searchField" and not c.get("operation"):
                    c.update({"kind": "scanTarget", "label": "Scan your booking QR", "operation": "getOrder",
                              "notes": "The booking's QR carries the order; scanning it opens the booking. "
                                       f"Shop-and-drop collection is staff-only and not here ({C22})."})
                if c.get("operation") == "getOrder" and c.get("kind") == "detailPanel":
                    c["columns"] = ["Order.orderNumber", "Order.status", "Order.grossAmount"]
                keep.append(c)
            r["components"] = keep
        touch("KSK-011", "core, getOrder by scan, columns narrowed")

    # KSK-016 Order Food: pay, then the order is placed; no plumbing in the modal
    s = S["KSK-016"]
    nav = s.setdefault("navigation", {}).setdefault("transitions", [])
    if not any(t.get("to") == "KSK-007" for t in nav):
        nav.append({"to": "KSK-007", "trigger": "Pays for the food order", "carries": ["orderId"],
                    "provenance": P22})
        s["navigation"].setdefault("exitTo", []).append("KSK-007")
        for o in s.get("overlays") or []:
            if (o.get("confirm") or {}).get("operation") == "createGuestFnbOrder":
                o["body"] = ("**Confirms the basket before it is sent; the guest types nothing here.** The kiosk "
                             "sends the basket's lines; `id`, `recordedAt`, `quotedTotal` and `locationSessionId` are "
                             "set by the kiosk and `fulfilment` is the outlet's counter pickup. Then the guest pays at "
                             "the terminal (KSK-007) and the kitchen sees the order only once it is paid; KSK-009 "
                             f"confirms it ({C22}). Dismissing sends nothing.")
        for _, c in comps(s):
            if c.get("kind") == "banner" and not c.get("operation"):
                c["notes"] = ("Says *contains* and *may contain* apart, from each item's `allergenDetail` "
                              f"(`Allergen.contains`, `Allergen.mayContain`) ({C22}).")
        touch("KSK-016", "pay step, allergen detail, modal")


def contracts(apply, log):
    edits = [
        ("contracts/satellite/seating.yaml", """    post:
      operationId: extendSeatHold
      x-ticvai-audience:
      - staff
      summary: Extend a hold
""", """    post:
      operationId: extendSeatHold
      security:
      - guestAuth: []
      - bearerAuth: []
      x-ticvai-audience:
      - staff
      - guest
      summary: Extend a hold
"""),
        ("contracts/satellite/seating.yaml", """        extensions, client to correct (audit R094).**

        '
      tags:
      - hold
      x-ticvai-permission: ORDER_CREATE
      x-ticvai-scope-level: venue
      x-ticvai-offline-capable: false""", """        extensions, client to correct (audit R094).**


        **A guest extends their own hold within their own session** (3 October 2026, """ + C23 + """; as
        `createSeatHold`, Chinmay, 3 October, Pattern 4 group 3: purchase actions are guest-callable within the
        guest''s own session). WEB-011 offers it from the warning before the hold lapses; a guest needs no
        permission and extends only a hold of their own cart. `ORDER_CREATE` is what a staff caller holds to do it
        for a guest.

        '
      tags:
      - hold
      x-ticvai-permission: ORDER_CREATE
      x-ticvai-guest-callable: true
      x-ticvai-scope-level: venue
      x-ticvai-offline-capable: false"""),
        ("contracts/satellite/fnb.yaml", """                    allergens:
                      type: array
                      description: Always present. Not a field a tenant may choose to omit.
                      items:
                        $ref: '#/components/schemas/AllergenCode'
                    preparationMinutes:""", """                    allergens:
                      type: array
                      description: Always present. Not a field a tenant may choose to omit.
                      items:
                        $ref: '#/components/schemas/AllergenCode'
                    allergenDetail:
                      allOf:
                      - $ref: '#/components/schemas/Allergen'
                      description: '**What the dish contains and what it may contain, told apart** (3 October 2026,
                        """ + C22 + """: the kiosk and guest menus promise the difference and the flat list cannot
                        carry it). `allergens` stays the flat list.'
                    preparationMinutes:"""),
    ]
    for rel, a, b in edits:
        f = ROOT / rel
        raw = io.open(f, encoding="utf-8", newline="").read()
        crlf = "\r\n" in raw
        t = raw.replace("\r\n", "\n")
        if b in t or (rel.endswith("seating.yaml") and C23 in t) or (rel.endswith("fnb.yaml") and "allergenDetail:" in t):
            continue  # already applied (the consumed-by refresh may have moved the anchor text)
        assert t.count(a) == 1, (rel, a[:60])
        t = t.replace(a, b)
        if crlf:
            t = t.replace("\n", "\r\n")
        if apply:
            io.open(f, "w", encoding="utf-8", newline="").write(t)
        log.append(f"{rel}: edited")


def notes(apply, log):
    for rel in ("handoff/design-notes/ticketing-guest.yaml", "handoff/design-notes/fnb-retail.yaml",
                "handoff/design-notes/customer-marketing.yaml"):
        f = ROOT / rel
        raw = io.open(f, encoding="utf-8", newline="").read()
        crlf = "\r\n" in raw
        lines = raw.replace("\r\n", "\n").split("\n")
        out, cur, n = [], None, 0
        i = 0
        while i < len(lines):
            l = lines[i]
            m = re.match(r"^  (KSK-\d{3}):\s*$", l)
            if m:
                cur = m.group(1)
            elif re.match(r"^  [A-Z]+-\d+:\s*$", l):
                cur = None
            out.append(l)
            mm = re.match(r"^(\s+)- what:", l)
            if cur and mm:
                ind = mm.group(1) + "  "
                j = i + 1
                block = []
                while j < len(lines) and lines[j].startswith(ind) or (j < len(lines) and lines[j].startswith(ind + " ")):
                    block.append(lines[j])
                    j += 1
                out.extend(block)
                if not any(b.strip().startswith("status:") for b in block):
                    out.append(f"{ind}status: fixed")
                    out.append(f"{ind}by: {C22}")
                    n += 1
                i = j
                continue
            i += 1
        if n:
            t = "\n".join(out)
            if crlf:
                t = t.replace("\n", "\r\n")
            import yaml
            yaml.load(t, Loader=yaml.CSafeLoader)
            if apply:
                io.open(f, "w", encoding="utf-8", newline="").write(t)
            log.append(f"{rel}: {n} kiosk correction(s) marked fixed")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    log = []
    contracts(a.apply, log)
    notes(a.apply, log)
    F = spf.ScreenFiles()
    screens(F, log)
    if a.apply and F.dirty:
        F.write()
    print("\n".join(log) or "nothing to do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
