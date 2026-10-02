#!/usr/bin/env python3
"""The flow steps the guest, till and P08/P09 batches left for the flows owner, and the screen edits that wait on them
(2 October 2026, cleanup pass; CHG-CLN-005, CHG-CLN-006, CHG-CLN-007).

Flows (CHG-CLN-005):
  F01 s6, F02 s4  getGuestProfile -> getMyProfile (WEB-011 reads the signed-in guest's own profile, CHG-SGU)
  F55 s2          getMyProfile and listConsentPurposes; the opt-ins ride on checkoutCart and recordCheckoutConsents
                  (the order.created consumer) records them, never the screen
  F53 s2          addToWishlist off WEB-024 (the wishlist is saved on GST-020, step 5)
  F18 s2          the card balance is read on the app's wallet, GST-011, which now declares getGameCard as its web twin
                  WEB-021 does (the shop GST-026 dropped it, CHG-SGU-018)
  F102 s1         getTenantConfig off CMS-001 (it reads getTenantAppStatus); P09 leaves the platforms (step 4 is CMS-014)
  F22 s4          createPreview, which CMS-012 declares, in place of getTenantConfig
  F50 s6          the rotating code is getEntitlementCredential on GST-055, not transferOrderTickets
  F17             s3 the bag is dropped at the till (POS-005 createShopAndDrop), s4 tracked on GST-062 (lookupShopAndDrop),
                  s5 handed over at the exit desk (POS-012 lookupShopAndDrop, collectShopAndDrop); BO-048 leaves the flow
  F51 s4          rewritten: the guest collects at the exit desk (POS-012), not from a kiosk that cannot hand goods over
  F59 s3          the hold is not extended at the till (POSV2-11): a lapsed hold is taken again (createSeatHold)
  F88 s2          fire and hold leave the station display; the pass (KIT-003, step 3) fires and holds
  F74 s1, s4      closeShift with the supervisor's PIN (POS-007) and in the daily reconciliation (BO-043)
  F73 s2          the till shift policy: getTillShiftPolicy and setTillShiftPolicy on POS-019
  F81 s1          the operator arrives from the till's own overview (POS-025), not the back office's order search
  F34 s8          trimmed: the retail return restocks the item; there is no separate manual disposition
Screens (CHG-CLN-006): GST-011 getGameCard; POS-005 createShopAndDrop; POS-012 lookupShopAndDrop and collectShopAndDrop;
POS-004 drops extendSeatHold; KIT-002 drops fireCourse and holdCourse; the flow-derived edges the repointed steps leave
behind (POS-005 -> BO-048, BO-048 -> GST-026, BO-021 -> POS-002, GST-062 -> KSK-017) come off.

    python3 tools/applied/cleanup-flows-2-october.py [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCREENS = ROOT / "screens"
FLOWS = ROOT / "flows"
CONTRACTS = ROOT / "contracts"
CHG_F, CHG_S = "CHG-CLN-005", "CHG-CLN-006"
DAY = "2 October 2026"


def text(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return "\r\n" in raw, raw.replace("\r\n", "\n")


def put(path: Path, crlf: bool, body: str, apply: bool) -> None:
    if apply:
        path.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))


def flow(fid: str) -> Path:
    return next(FLOWS.glob(f"{fid}-*.yaml"))


def step_block(body: str, n: int) -> tuple[int, int]:
    """The start and end offsets of `- step: n` in a flow's text."""
    m = re.search(rf"^- step: {n}\s*$", body, re.M)
    if not m:
        raise SystemExit(f"step {n} not found")
    nxt = re.search(r"^(- step: \d+\s*$|[a-zA-Z$#])", body[m.end():], re.M)
    return m.start(), m.end() + (nxt.start() if nxt else len(body) - m.end())


def set_step(body: str, n: int, screen=None, action=None, ops=None, outcome=None, extra=None, drop_keys=()) -> str:
    a, b = step_block(body, n)
    blk = body[a:b]
    lines = blk.rstrip("\n").split("\n")
    out = [lines[0]]
    i = 1
    keys = {}
    while i < len(lines):
        m = re.match(r"^  ([A-Za-z]+):", lines[i])
        j = i + 1
        while j < len(lines) and not re.match(r"^  [A-Za-z]+:", lines[j]):
            j += 1
        keys[m.group(1) if m else f"_{i}"] = lines[i:j]
        i = j
    if screen:
        keys["screen"] = [f"  screen: {screen}"]
    if action:
        keys["action"] = [f"  action: {yaml_str(action)}"]
    if ops is not None:
        keys["operations"] = ["  operations: []"] if not ops else ["  operations:"] + [f"  - {o}" for o in ops]
    if outcome:
        keys["outcome"] = [f"  outcome: {yaml_str(outcome)}"]
    for k in drop_keys:
        keys.pop(k, None)
    for k, v in (extra or {}).items():
        keys[k] = [f"  {k}: {v}"] if not isinstance(v, list) else [f"  {k}:"] + [f"  - {x}" for x in v]
    order = ["screen", "action", "operations", "outcome"]
    for k in order:
        if k in keys:
            out += keys.pop(k)
    for v in keys.values():
        out += v
    return body[:a] + "\n".join(out) + "\n" + body[b:]


def yaml_str(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def platforms(body: str, keep: list) -> str:
    m = re.search(r"^platforms:\n((?:- .*\n)+)", body, re.M)
    return body[:m.start()] + "platforms:\n" + "".join(f"- {p}\n" for p in keep) + body[m.end():]


def flows(apply: bool) -> None:
    edits = {}
    f = flow("F01"); c, b = text(f)
    b = set_step(b, 6, ops=["getMyProfile", "listConsentPurposes"]); edits[f] = (c, b)
    f = flow("F02"); c, b = text(f)
    b = set_step(b, 4, ops=["getMyProfile", "listConsentPurposes"]); edits[f] = (c, b)
    f = flow("F55"); c, b = text(f)
    b = set_step(b, 2, ops=["getMyProfile", "listConsentPurposes"], outcome=(
        "**Consent per attendee, not per purchase.** A guest buying for three friends cannot consent on their behalf "
        "(CF-160 again, and this is where it bites). The marketing opt-ins ticked here travel with `checkoutCart` and "
        "are recorded by `recordCheckoutConsents`, the `order.created` consumer, never by the screen (CHG-CSA-025; "
        f"{CHG_F})."))
    edits[f] = (c, b)
    f = flow("F53"); c, b = text(f)
    b = set_step(b, 2, ops=["getWishlist", "recordConsent", "listGuestDevices"]); edits[f] = (c, b)
    f = flow("F18"); c, b = text(f)
    b = set_step(b, 2, screen="GST-011", action="Checks the card's balance in the app's wallet", ops=["getGameCard"])
    edits[f] = (c, b)
    f = flow("F102"); c, b = text(f)
    b = set_step(b, 1, ops=["getTenantAppStatus", "getModuleEnablement"])
    b = platforms(b, ["P13"])
    edits[f] = (c, b)
    f = flow("F22"); c, b = text(f)
    b = set_step(b, 4, ops=["createPreview", "validateTenantConfig"]); edits[f] = (c, b)
    f = flow("F50"); c, b = text(f)
    b = set_step(b, 6, ops=["getEntitlementCredential"]); edits[f] = (c, b)
    f = flow("F17"); c, b = text(f)
    b = set_step(b, 3, screen="POS-005", action="Bag is dropped and tagged at the till", ops=["createShopAndDrop"],
                 outcome="**A reference the guest can present**, not a receipt they will lose; the ticket they carry "
                         f"claims it too ({CHG_F})")
    b = set_step(b, 4, screen="GST-062", ops=["lookupShopAndDrop"], extra={"crossesDevice": "true"})
    b = set_step(b, 5, screen="POS-012", action="Collected on the way out, at the exit desk",
                 ops=["lookupShopAndDrop", "collectShopAndDrop"], extra={"crossesDevice": "true"})
    b = platforms(b, ["P04 Venue POS", "P02 Guest App"])
    edits[f] = (c, b)
    f = flow("F51"); c, b = text(f)
    b = set_step(b, 4, screen="POS-012", action="They collect at the exit desk on the way out",
                 ops=["lookupShopAndDrop", "collectShopAndDrop"],
                 outcome="**Staff hand the goods over**, against the ticket, the drop reference or the receipt: a kiosk "
                         "cannot hand goods over (collectShopAndDrop is staff-only), so the guest's way out passes the "
                         f"desk ({CHG_F}; design-note correction KSK-017)", extra={"crossesDevice": "true"})
    edits[f] = (c, b)
    f = flow("F59"); c, b = text(f)
    b = set_step(b, 3, action="The guest is slow. The hold is not extended at the till; when it lapses the seat is "
                              "held again", ops=["getSeatHold", "createSeatHold"],
                 outcome="**No extend at the till** (POSV2-11, DEC-552): the hold runs its venue-set time, and a lapsed "
                         "hold is taken again if the seat is still free; if it sold meanwhile, the map shows it taken "
                         f"({CHG_F})")
    edits[f] = (c, b)
    f = flow("F88"); c, b = text(f)
    b = set_step(b, 2, ops=["listKitchenTickets", "notifyServer"]); edits[f] = (c, b)
    f = flow("F74"); c, b = text(f)
    b = set_step(b, 1, ops=["submitShiftCount", "acceptShiftVariance", "listDenominations", "closeShift"])
    b = set_step(b, 4, ops=["listShifts", "getShiftCountLines", "closeShift"])
    edits[f] = (c, b)
    f = flow("F73"); c, b = text(f)
    b = set_step(b, 2, ops=["getTillShiftPolicy", "setTillShiftPolicy"]); edits[f] = (c, b)
    f = flow("F81"); c, b = text(f)
    b = set_step(b, 1, screen="POS-025", action="Till Home: the store's overview before the sale.",
                 ops=["getWorkstationShift", "listSaleBoards"],
                 outcome="**The operator arrives at the sale from the till's own overview** (repointed 2 October 2026, "
                         f"{CHG_F}): RET-3A is the client's cross-store command centre, not the back office's order "
                         "search (BO-021), and a back-office search does not open a till on another device.")
    b = set_step(b, 2, drop_keys=("crossesDevice",))
    b = platforms(b, ["P04"])
    edits[f] = (c, b)
    f = flow("F34"); c, b = text(f)
    a, e = step_block(b, 8)
    b = b[:a] + b[e:]
    b = platforms(b, ["P04"])
    b = b.replace("  description: Refunded to the original tender and dispositioned.",
                  "  description: Refunded to the original tender; the return put a resaleable item back in stock "
                  f"(createRetailReturn), so no manual movement follows ({CHG_F}).")
    edits[f] = (c, b)
    for f, (c, b) in edits.items():
        print(f"  {f.name}")
        put(f, c, b, apply)


# ------------------------------------------------------------------------------------------------ screens
def read(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw, yaml.load(raw.replace("\r\n", "\n"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def write(path: Path, raw: str, doc, apply: bool) -> None:
    out = yaml.dump(doc, Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True, width=100)
    if apply:
        path.write_bytes((out.replace("\n", "\r\n") if "\r\n" in raw else out).encode("utf-8"))


def region(s, name):
    return next(r for r in s["layout"]["regions"] if r["name"] == name)


def drop_op(s, ops):
    s["apis"] = [a for a in s["apis"] if a["operationId"] not in ops]
    for r in s["layout"]["regions"]:
        r["components"] = [c for c in r.get("components") or [] if c.get("operation") not in ops]
    if s.get("overlays"):
        s["overlays"] = [o for o in s["overlays"] if (o.get("confirm") or {}).get("operation") not in ops]


def drop_edges(s, to):
    nav = s.get("navigation") or {}
    nav["transitions"] = [t for t in nav.get("transitions") or [] if t.get("to") != to]
    if to in (nav.get("exitTo") or []) and not any(t.get("to") == to for t in nav["transitions"]):
        nav["exitTo"] = [x for x in nav["exitTo"] if x != to]


def screens(apply: bool) -> None:
    p04 = SCREENS / "P04-point-of-sale.yaml"
    raw, d = read(p04)
    S = {s["id"]: s for s in d["screens"]}
    s = S["POS-004"]
    drop_op(s, {"extendSeatHold"})
    s["notes"] = (f"**extendSeatHold off the till** ({DAY}, {CHG_S}): flow F59 step 3 no longer calls it, so the "
                  "declaration POSV2-11 left until then comes off (CHG-SPO-020).\n\n" + str(s.get("notes") or "")).strip()
    s = S["POS-005"]
    if "createShopAndDrop" not in {a["operationId"] for a in s["apis"]}:
        region(s, "actionBar")["components"].append({
            "kind": "secondaryButton", "label": "Leave it with us (Shop & Drop)", "operation": "createShopAndDrop",
            "notes": "After a paid retail sale: the goods wait at a collection point and the guest's ticket or the drop "
                     "reference claims them on the way out (4.4.7, R236). Refused for an item that cannot be dropped "
                     f"(chilled, fragile, oversized) or a point that closes before the collect-by time ({CHG_S}).",
            "provenance": "contract retail.yaml POST /shop-and-drop"})
        s.setdefault("overlays", []).append({
            "id": "formCreateShopAndDrop", "component": "modal", "trigger": "Leave it with us (Shop & Drop)",
            "body": "**Collects what `createShopAndDrop` sends before it is called.** Required: `id` (a client UUIDv7, "
                    "generated silently), `collectionPointId` (picked by name, with its hours), `recordedAt`. Optional: "
                    "`entitlementId` (the guest's ticket, scanned), `lineIds`, `collectBy` (venue close by default). "
                    "`saleId` is the sale just paid. Dismissing sends nothing; the sale stands.",
            "confirm": {"label": "Drop it", "operation": "createShopAndDrop"},
            "dismiss": {"label": "Cancel", "discards": ["collectionPointId", "entitlementId", "lineIds", "collectBy"]},
            "provenance": "contract retail.yaml POST /shop-and-drop"})
        s["apis"].append({"operationId": "createShopAndDrop", "contract": "retail",
                          "purpose": "Leave the paid goods at a collection point for the way out", "trigger": "onAction",
                          "provenance": f"flow F17 step 3, {DAY} ({CHG_S})"})
    drop_edges(s, "BO-048")
    s = S["POS-012"]
    if "collectShopAndDrop" not in {a["operationId"] for a in s["apis"]}:
        region(s, "contentBody")["components"].insert(0, {
            "kind": "searchField", "label": "Find dropped goods", "operation": "lookupShopAndDrop",
            "notes": "By the guest's ticket (scanned), the drop reference or the receipt number, whichever the guest "
                     f"still has (4.4.7, R236; {CHG_S}).",
            "provenance": "contract retail.yaml GET /shop-and-drop/lookup"})
        region(s, "actionBar")["components"].append({
            "kind": "secondaryButton", "label": "Hand over dropped goods", "operation": "collectShopAndDrop",
            "notes": "Records who handed over and against what; the guest may take part and leave the rest for "
                     f"later on the same ticket ({CHG_S}).",
            "provenance": "contract retail.yaml POST /shop-and-drop/{dropId}/collect"})
        s.setdefault("overlays", []).append({
            "id": "formCollectShopAndDrop", "component": "confirmDialog", "trigger": "Hand over dropped goods",
            "body": "**Collects what `collectShopAndDrop` sends before it is called.** Required: `recordedAt`. Optional: "
                    "`lineIds` (a partial collection), `verifiedBy` (ticket, reference or receipt). Dismissing sends "
                    "nothing.",
            "confirm": {"label": "Hand over", "operation": "collectShopAndDrop"},
            "dismiss": {"label": "Cancel", "discards": ["lineIds"]},
            "provenance": "contract retail.yaml POST /shop-and-drop/{dropId}/collect"})
        s["apis"] += [
            {"operationId": "lookupShopAndDrop", "contract": "retail", "purpose": "Find a guest's dropped goods",
             "trigger": "onAction", "provenance": f"flow F17 step 5 and F51 step 4, {DAY} ({CHG_S})"},
            {"operationId": "collectShopAndDrop", "contract": "retail", "purpose": "Hand the dropped goods over",
             "trigger": "onAction", "provenance": f"flow F17 step 5 and F51 step 4, {DAY} ({CHG_S})"}]
    write(p04, raw, d, apply)
    print("  P04: POS-004 -extendSeatHold; POS-005 +createShopAndDrop; POS-012 +lookupShopAndDrop +collectShopAndDrop")

    p15 = SCREENS / "P15-kitchen-display.yaml"
    raw, d = read(p15)
    s = next(x for x in d["screens"] if x["id"] == "KIT-002")
    drop_op(s, {"fireCourse", "holdCourse"})
    s["notes"] = (f"**Fire and hold leave the station display** ({DAY}, {CHG_S}): the pass fires and holds courses "
                  "(DI-407; KIT-003), and flow F88 step 2 no longer calls them here (CHG-SPO-020).\n\n"
                  + str(s.get("notes") or "")).strip()
    write(p15, raw, d, apply)
    print("  P15: KIT-002 -fireCourse -holdCourse")

    p08 = SCREENS / "P08-venue-back-office.yaml"
    raw, d = read(p08)
    S = {x["id"]: x for x in d["screens"]}
    drop_edges(S["BO-048"], "GST-026")
    drop_edges(S["BO-021"], "POS-002")
    write(p08, raw, d, apply)
    print("  P08: BO-048 -> GST-026 and BO-021 -> POS-002 removed")

    # P02 does not round-trip through the dumper byte for byte, so GST-011 and GST-062 are edited as text.
    p02 = SCREENS / "P02-guest-mobile-app.yaml"
    c, body = text(p02)
    if "operation: getGameCard" not in body.split("\n- id: GST-011\n", 1)[1].split("\n- id: ", 1)[0]:
        head, rest = body.split("\n- id: GST-011\n", 1)
        blk, tail = rest.split("\n- id: ", 1)
        anchor = "        operation: getWallet\n        provenance: contract wallet.yaml GET /wallets/{subjectId}\n"
        assert anchor in blk, "GST-011 wallet panel not found"
        panel = ("      - kind: detailPanel\n        label: The game card\n        bindsTo: GameCard\n        columns:\n"
                 + "".join(f"        - GameCard.{x}\n" for x in ("cardCode", "kind", "credits", "bonusCredits", "points",
                                                                  "status", "blockedReason", "lastPlayedAt", "expiresAt"))
                 + "        operation: getGameCard\n"
                 + f"        notes: An arcade card's balance, read by its code, as the web wallet WEB-021 shows it (flow F18 step 2; {CHG_S}).\n"
                 + "        provenance: contract games.yaml GET /game-cards/{cardCode}\n")
        blk = blk.replace(anchor, anchor + panel, 1)
        api_anchor = "  - operationId: settleWalletAtExit\n    contract: wallet\n    purpose: Settle the wallet at exit\n    trigger: onAction\n    provenance: build, 29 September 2026\n"
        assert api_anchor in blk, "GST-011 apis not found"
        blk = blk.replace(api_anchor, api_anchor + "  - operationId: getGameCard\n    contract: games\n    purpose: Balance on a game card\n"
                          f"    trigger: onAction\n    provenance: flow F18 step 2, {DAY} ({CHG_S})\n", 1)
        body = head + "\n- id: GST-011\n" + blk + "\n- id: " + tail
    # GST-062's edge to the kiosk (flow F51 step 3 -> 4) goes with the rewritten step
    head, rest = body.split("\n- id: GST-062\n", 1)
    blk, tail = rest.split("\n- id: ", 1)
    blk2 = re.sub(r"    - to: KSK-017\n(?:      .*\n)+", "", blk)
    body = head + "\n- id: GST-062\n" + blk2 + "\n- id: " + tail
    put(p02, c, body, apply)
    print("  P02: GST-011 +getGameCard; GST-062 -> KSK-017 removed")


def consumed_by(apply: bool) -> None:
    """x-ticvai-consumed-by follows the screens (check-screen-wiring S-CONSUMED-MIRROR)."""
    add = {("retail", "createShopAndDrop"): "P04 POS-005 Payment",
           ("retail", "lookupShopAndDrop"): "P04 POS-012 Omnichannel Order & Fulfilment Center",
           ("retail", "collectShopAndDrop"): "P04 POS-012 Omnichannel Order & Fulfilment Center",
           ("games", "getGameCard"): "P02 GST-011 Wallet Overview"}
    drop = {("seating", "extendSeatHold"): "P04 POS-004", ("fnb", "fireCourse"): "P15 KIT-002",
            ("fnb", "holdCourse"): "P15 KIT-002"}
    for f in sorted(CONTRACTS.glob("*/*.yaml")):
        name = f.stem
        mine = {k: v for k, v in add.items() if k[0] == name}
        gone = {k: v for k, v in drop.items() if k[0] == name}
        if not mine and not gone:
            continue
        c, body = text(f)
        lines = body.split("\n")
        for (_, op), entry in list(mine.items()) + list(gone.items()):
            at = next(i for i, l in enumerate(lines) if re.match(rf"^\s+operationId:\s*{op}\s*$", l))
            ind = len(lines[at]) - len(lines[at].lstrip())
            j = at + 1
            cb = None
            while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) >= ind):
                if len(lines[j]) - len(lines[j].lstrip()) == ind and lines[j].strip().startswith("x-ticvai-consumed-by:"):
                    cb = j
                    break
                if len(lines[j]) - len(lines[j].lstrip()) < ind:
                    break
                j += 1
            if (_, op) in gone:
                if cb is not None:
                    k = cb + 1
                    while k < len(lines) and re.match(r"^\s+-\s", lines[k]):
                        if entry in lines[k]:
                            del lines[k]
                            break
                        k += 1
                    if not re.match(r"^\s+-\s", lines[cb + 1]):
                        lines[cb] = lines[cb].rstrip() + " []"
                continue
            q = '"'
            if cb is None:
                lines[at + 1:at + 1] = [" " * ind + "x-ticvai-consumed-by:", " " * (ind + 2) + f"- {q}{entry}{q}"]
            else:
                k = cb + 1
                items = []
                while k < len(lines) and re.match(r"^\s+-\s", lines[k]):
                    items.append(k)
                    k += 1
                pref = re.match(r"^(\s+-\s+)", lines[items[0]]).group(1) if items else " " * (ind + 2) + "- "
                pos = cb + 1
                while pos < k and lines[pos].strip().lstrip("- ").strip("'\"") < entry:
                    pos += 1
                lines.insert(pos, f"{pref}{q}{entry}{q}")
        put(f, c, "\n".join(lines), apply)
        print(f"  {f.relative_to(ROOT).as_posix()}: consumed-by")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    flows(a.apply)
    screens(a.apply)
    consumed_by(a.apply)
    print("applied" if a.apply else "dry run: --apply writes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
