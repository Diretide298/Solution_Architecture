#!/usr/bin/env python3
"""Declare how a guest calls the staff-permission operations the guest screens bind (Pattern 4).

**Decided by Chinmay on 3 October 2026** in the answers to the Block A audit on live r2 (section
"Pattern 4", all as recommended; CHG-AUD-001). The audit found guest screens (P01 guest web, P02 guest
app, P05 kiosk) binding 49 operations that carry a staff permission and declare neither
`x-ticvai-guest-callable` nor `x-ticvai-self-scoped`, so nothing said what a guest, who holds no
permission, is allowed and what they get back (ADR-0025: audience and permission are orthogonal; the
permission is what a staff caller must hold). Each group is a change entry:

  CHG-GCF-001  public catalogue reads: `x-ticvai-guest-callable: true`, a guest or a visitor sees
               published data only (said in the description); staff keep their permission and also
               see drafts.
  CHG-GCF-002  the guest's own records: `x-ticvai-self-scoped: subject`; another guest's record is
               refused as not found; staff keep their permission to act for any guest.
  CHG-GCF-003  purchase actions: `x-ticvai-guest-callable: true` within the guest's own session; staff
               keep the permission to act for a guest.
  CHG-GCF-004  AI and chat: the guest's own assistant conversations are self-scoped; `reprintOrder` is
               the guest's own order and a kiosk may call it as a registered device (`device` audience,
               the kiosk's `apiKeyAuth`). The new `sendGuestConversationMessage` and
               `getGuestConversation` are written by hand in marketing-crm, not here.
  CHG-GCF-005  `listAnalyticsProviders` stays a staff read; a guest reads the providers from the
               published tenant config (the PublishedTenantConfig field is written by hand).

Only flags and one appended description paragraph per operation are written, at the operation's own
lines, so nothing else in a file moves and edits other branches made to the same operations merge.
Every edit finds its target and does nothing when it is already done: a second run says there is
nothing to do.

    python tools/applied/guest-scoping-3-october.py [--apply]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC = "Chinmay, 3 October 2026, Pattern 4"

FILES = {
    "catalogue": "spine", "orders": "spine", "access": "spine", "finance": "spine",
    "promotions": "satellite", "seating": "satellite", "retail": "satellite", "queue": "satellite",
    "marketing-crm": "satellite", "wallet": "satellite", "ai": "satellite", "white-label": "satellite",
}

# Group 1: public catalogue reads. op -> (contract, what a guest gets)
G1 = {
    "listProducts": ("catalogue", "products that are published and on sale"),
    "getProduct": ("catalogue", "a product that is published"),
    "listProductVariants": ("catalogue", "the published variants of a published product"),
    "listPerformances": ("catalogue", "published performances"),
    "getPerformance": ("catalogue", "a published performance"),
    "getAvailability": ("catalogue", "the availability of published products"),
    "listCatalogueBundles": ("catalogue", "published bundles"),
    "getBundle": ("promotions", "a published bundle"),
    "listPromotions": ("promotions", "live, published promotions"),
    "getPromotion": ("promotions", "a live, published promotion"),
    "getCouponCode": ("promotions", "whether a code of a live, published promotion is valid and what it gives"),
    "getSeatAvailability": ("seating", "the seat availability of a published performance"),
    "listMerchandise": ("retail", "active merchandise that is on sale"),
    "lookupMerchandise": ("retail", "active merchandise that is on sale"),
    "listQueues": ("queue", "queues that are open and visible"),
    "listParkingFacilities": ("access", "the car parks offered to guests"),
    "listFxRates": ("finance", "the published rates in force"),
    "listLoyaltyProgrammes": ("marketing-crm", "published loyalty programmes"),
    "listRewards": ("marketing-crm", "published rewards"),
    "listConsentPurposes": ("marketing-crm", "the active consent purposes a guest is asked for"),
}

# Group 2 (and the AI conversations and reprintOrder of group 4): the guest's own records.
# op -> (contract, entry, what is the guest's own, what is refused)
G2 = {
    "getOrder": ("orders", "002", "an order they placed", "another guest's order"),
    "getReservation": ("orders", "002", "their own reservations", "another guest's reservation"),
    "listReservations": ("orders", "002", "their own reservations", "another guest's reservation"),
    "cancelReservation": ("orders", "002", "their own reservations", "another guest's reservation"),
    "getWallet": ("wallet", "002", "their own wallet (`subjectId` is the caller's)", "another guest's wallet"),
    "listWalletTransactions": ("wallet", "002", "their own wallet (`subjectId` is the caller's)",
                               "another guest's wallet"),
    "getGiftCard": ("wallet", "002", "a gift card held in their own wallet", "any other card code"),
    "getGuestConsents": ("marketing-crm", "002", "their own consents (`subjectId` is the caller's)",
                         "another guest's consents"),
    "getMarketingSubscription": ("marketing-crm", "002", "their own marketing subscription",
                                 "another guest's subscription"),
    "setMarketingSubscription": ("marketing-crm", "002", "their own marketing subscription",
                                 "another guest's subscription"),
    "listCustomerBadges": ("marketing-crm", "002", "their own badges (`customerId` is the caller's)",
                           "another guest's badges"),
    "getFacePassEnrolment": ("access", "002", "their own FacePass enrolment", "another guest's enrolment"),
    "enrolFacePass": ("access", "002", "their own FacePass enrolment", "another guest's enrolment"),
    "revokeFacePass": ("access", "002", "their own FacePass enrolment", "another guest's enrolment"),
    "lookupShopAndDrop": ("retail", "002", "goods they dropped themselves", "another guest's goods"),
    "createAiConversation": ("ai", "004", "their own assistant conversations", "another guest's conversation"),
    "listAiConversations": ("ai", "004", "their own assistant conversations", "another guest's conversation"),
    "sendAiMessage": ("ai", "004", "their own assistant conversations", "another guest's conversation"),
    "reprintOrder": ("orders", "004", "an order they placed (resend or reprint)", "another guest's order"),
}

# Group 3: purchase actions in the guest's own session.
G3 = {
    "createOrder": "orders", "createPayment": "orders", "inquirePaymentStatus": "orders",
    "createSeatHold": "seating", "recommendSeats": "seating", "reserveMerchandise": "retail",
    "evaluatePromotions": "promotions",
}

# Group 4 and 5: notes only (no flag).
NOTES = {
    "sendConversationMessage": ("marketing-crm",
        "**A guest writes with `sendGuestConversationMessage`** ({src}; CHG-GCF-004): the guest screens "
        "(GST-031, GST-032, WEB-044) no longer call this; it is the agent's send and needs `CASE_MANAGE`. "
        "The guest audience and `guestAuth` stay only so a client built against r1 is not broken; they go "
        "at the next major version."),
    "listAnalyticsProviders": ("white-label",
        "**A guest reads the providers from the published tenant config** ({src}; CHG-GCF-005): the "
        "storefront and app tag loader reads `PublishedTenantConfig.analyticsProviders` from "
        "`getPublishedTenantConfig`, which needs no session, and GST-001 and WEB-001 no longer call this. "
        "This stays a staff read under `TENANT_CONFIGURE`; the guest audience and the optional credential "
        "stay only so a client built against r1 is not broken, and a guest caller still gets the rows "
        "described above."),
}

DEVICE_NOTE = ("**A kiosk reprints as a registered device** ({src}; CHG-GCF-004): the kiosk (P05) calls "
               "this with its device credential (`apiKeyAuth`, audience `device`) and holds no permission; "
               "it reprints only an order the guest at it has identified (KSK-012 booking found, KSK-009 "
               "ticket issued, KSK-010 print failure), and each reprint is recorded against the device.")


def g1_text(perm, what):
    return (f"**A guest calls this without a permission and sees published data only** ({SRC}; "
            f"CHG-GCF-001; `x-ticvai-guest-callable`): a guest or a visitor gets {what}, and nothing in "
            f"draft, unpublished or withdrawn; asked for by id, such a record answers as not found. "
            f"`{perm}` is what a staff caller must hold, and staff also see drafts (ADR-0025).")


def g2_text(perm, entry, own, other):
    return (f"**A guest acts on their own only** ({SRC}; CHG-GCF-{entry}; `x-ticvai-self-scoped: subject`): "
            f"a guest caller needs no permission and is answered for {own}; {other} is refused exactly as "
            f"one that does not exist, never returned. `{perm}` is what a staff caller must hold to act "
            f"for any guest (ADR-0025).")


def g3_text(perm):
    return (f"**A guest does this within their own session** ({SRC}; CHG-GCF-003; "
            f"`x-ticvai-guest-callable`): a guest needs no permission and acts only for themselves, on "
            f"their own cart, hold, order or payment in their own session. `{perm}` is what a staff caller "
            f"must hold to do it for a guest at a till or in the back office (ADR-0025).")


class Op:
    """The lines of one operation inside a contract file's text."""

    def __init__(self, lines, op_id):
        idx = [i for i, l in enumerate(lines) if re.match(rf"^\s+operationId: {re.escape(op_id)}\s*$", l)]
        if len(idx) != 1:
            raise SystemExit(f"{op_id}: found {len(idx)} times")
        i = idx[0]
        self.key_indent = len(lines[i]) - len(lines[i].lstrip())
        s = i
        while len(lines[s - 1]) - len(lines[s - 1].lstrip()) >= self.key_indent or not lines[s - 1].strip():
            s -= 1
        self.start = s - 1  # the method line
        e = i + 1
        while e < len(lines) and (not lines[e].strip() or
                                  len(lines[e]) - len(lines[e].lstrip()) >= self.key_indent):
            e += 1
        self.end = e
        self.lines = lines

    def key_line(self, key):
        pad = " " * self.key_indent
        for i in range(self.start + 1, self.end):
            if self.lines[i].startswith(pad + key + ":") and not self.lines[i][self.key_indent].isspace():
                return i
        return None

    def list_end(self, i):
        """The line after the block list under key line i."""
        pad = " " * self.key_indent
        j = i + 1
        while j < self.end and (self.lines[j].startswith(pad + "- ") or
                                self.lines[j].startswith(pad + "  ")):
            j += 1
        return j

    def value_end(self, i):
        """The line after the value of key line i (block scalar, quoted or plain, multi-line)."""
        j = i + 1
        while j < self.end and (not self.lines[j].strip() or
                                len(self.lines[j]) - len(self.lines[j].lstrip()) > self.key_indent):
            j += 1
        while j - 1 > i and not self.lines[j - 1].strip():
            j -= 1
        return j


def wrap(text, indent, width=110):
    out, line = [], ""
    for w in text.split():
        if line and len(indent) + len(line) + 1 + len(w) > width:
            out.append(indent + line)
            line = w
        else:
            line = f"{line} {w}" if line else w
    if line:
        out.append(indent + line)
    return out


def append_description(lines, op, text):
    """Append a paragraph to the operation's description, in whatever style it is written."""
    i = op.key_line("description")
    pad = " " * op.key_indent
    body_pad = pad + "  "
    if i is None:
        j = op.key_line("summary")
        j = op.value_end(j) if j is not None else op.start + 2
        new = [pad + "description: >"] + wrap(text, body_pad)
        lines[j:j] = new
        return
    head = lines[i][len(pad) + len("description:"):].strip()
    end = op.value_end(i)
    if head[:1] in (">", "|"):
        new = [""] + wrap(text, body_pad)
        lines[end:end] = new
    elif head.startswith("'"):
        # single-quoted, possibly multi-line: the closing quote ends the last non-blank line
        last = end - 1
        closing = lines[last].rstrip()
        assert closing.endswith("'"), (op, closing)
        esc = text.replace("'", "''")
        if closing.strip() == "'":
            # trailing "\n\n" then the bare quote: insert the paragraph before it
            new = wrap(esc, body_pad) + [""]
            lines[last:last] = new
        else:
            lines[last] = closing[:-1]
            lines[last + 1:last + 1] = [""] + wrap(esc, body_pad)[:-1] + [wrap(esc, body_pad)[-1] + "'"]
    elif head.startswith('"'):
        raise SystemExit(f"double-quoted description not handled at line {i + 1}")
    else:
        # plain scalar: turn into a folded block
        first = head
        rest = [l.strip() for l in lines[i + 1:end]]
        old = " ".join([first] + [r for r in rest if r])
        new = [pad + "description: >"] + wrap(old, body_pad) + [""] + wrap(text, body_pad)
        lines[i:end] = new


def set_flag(lines, op, key, value):
    if op.key_line(key) is not None:
        return False
    anchor = op.key_line("x-ticvai-permission")
    if anchor is None:
        anchor = op.key_line("x-ticvai-audience")
        anchor = op.list_end(anchor) - 1
    lines.insert(anchor + 1, " " * op.key_indent + f"{key}: {value}")
    return True


def add_list_item(lines, op, key, item):
    i = op.key_line(key)
    pad = " " * op.key_indent
    j = op.list_end(i)
    if any(lines[k].strip() == f"- {item}" for k in range(i + 1, j)):
        return False
    lines.insert(j, pad + f"- {item}")
    return True


def perm_of(doc_ops, op_id):
    return doc_ops[op_id].get("x-ticvai-permission")


def load_ops(path):
    doc = yaml.load(path.read_text(encoding="utf-8"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    out = {}
    for item in (doc.get("paths") or {}).values():
        for v, o in (item or {}).items():
            if isinstance(o, dict) and "operationId" in o:
                out[o["operationId"]] = o
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    plan = {}  # contract -> [(op, action)]
    for op, (c, what) in G1.items():
        plan.setdefault(c, []).append((op, "g1", what))
    for op, (c, entry, own, other) in G2.items():
        plan.setdefault(c, []).append((op, "g2", (entry, own, other)))
    for op, c in G3.items():
        plan.setdefault(c, []).append((op, "g3", None))
    for op, (c, text) in NOTES.items():
        plan.setdefault(c, []).append((op, "note", text))
    plan["orders"].append(("reprintOrder", "device", None))

    done = 0
    for contract, items in sorted(plan.items()):
        path = ROOT / "contracts" / FILES[contract] / f"{contract}.yaml"
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        ops = load_ops(path)
        changed = []
        for op_id, action, arg in items:
            o = ops[op_id]
            if action == "g1":
                if o.get("x-ticvai-guest-callable"):
                    continue
                set_flag(lines, Op(lines, op_id), "x-ticvai-guest-callable", "true")
                append_description(lines, Op(lines, op_id), g1_text(perm_of(ops, op_id), arg))
            elif action == "g2":
                if o.get("x-ticvai-self-scoped"):
                    continue
                set_flag(lines, Op(lines, op_id), "x-ticvai-self-scoped", "subject")
                append_description(lines, Op(lines, op_id), g2_text(perm_of(ops, op_id), *arg))
            elif action == "g3":
                if o.get("x-ticvai-guest-callable"):
                    continue
                set_flag(lines, Op(lines, op_id), "x-ticvai-guest-callable", "true")
                append_description(lines, Op(lines, op_id), g3_text(perm_of(ops, op_id)))
            elif action == "note":
                if "CHG-GCF-00" in (o.get("description") or ""):
                    continue
                append_description(lines, Op(lines, op_id), arg.format(src=SRC))
            elif action == "device":
                if "device" in (o.get("x-ticvai-audience") or []):
                    continue
                add_list_item(lines, Op(lines, op_id), "x-ticvai-audience", "device")
                add_list_item(lines, Op(lines, op_id), "security", "apiKeyAuth: []")
                append_description(lines, Op(lines, op_id), DEVICE_NOTE.format(src=SRC))
            changed.append(f"{op_id} ({action})")
        if not changed:
            continue
        new = "\n".join(lines)
        after = load_ops_text(new)
        for op_id, action, arg in items:
            verify(contract, op_id, action, ops[op_id], after[op_id])
        done += len(changed)
        print(f"{contract}: {', '.join(changed)}")
        if args.apply:
            path.write_text(new, encoding="utf-8")
    if not done:
        print("nothing to do: every Pattern 4 operation already declares how a guest calls it")
    elif not args.apply:
        print(f"{done} operation edit(s); dry run, pass --apply to write")
    return 0


def load_ops_text(text):
    doc = yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    out = {}
    for item in (doc.get("paths") or {}).values():
        for v, o in (item or {}).items():
            if isinstance(o, dict) and "operationId" in o:
                out[o["operationId"]] = o
    return out


def verify(contract, op_id, action, before, after):
    """The edit changed only what it meant to: the flag, the audience and security items, and the
    description gained a paragraph at its end."""
    b, a = dict(before), dict(after)
    db, da = b.pop("description", "") or "", a.pop("description", "") or ""
    if " ".join(da.split())[:len(" ".join(db.split()))] != " ".join(db.split()):
        raise SystemExit(f"{contract} {op_id}: the description changed, not only grew")
    if action in ("g1", "g3"):
        assert a.pop("x-ticvai-guest-callable") is True, op_id
    if action == "g2":
        assert a.pop("x-ticvai-self-scoped") == "subject", op_id
    if op_id == "reprintOrder":
        a.pop("x-ticvai-self-scoped", None)
        b.pop("x-ticvai-self-scoped", None)
        assert "device" in a["x-ticvai-audience"] and {"apiKeyAuth": []} in a["security"], op_id
        a["x-ticvai-audience"] = [x for x in a["x-ticvai-audience"] if x != "device"]
        a["security"] = [x for x in a["security"] if x != {"apiKeyAuth": []}]
    if a != b:
        keys = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
        raise SystemExit(f"{contract} {op_id}: unexpected change to {sorted(keys)}")


if __name__ == "__main__":
    sys.exit(main())
