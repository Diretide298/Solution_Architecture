#!/usr/bin/env python3
"""Propose components for screens whose layout says almost nothing.

**215 of 492 screens declare one component or none.** `POS-002` declares eleven — a search field, a
sale board, sort, filters, a cart panel and six buttons — and it is the screen a reviewer can
actually judge. A screen declaring `detailPanel` and nothing else is a screen a reviewer nods at.

**The operations already say what the screen needs.** A screen calling `listQueues` needs something
to list them in; one calling `createWorkOrder` needs a way to submit and a way to cancel; one
calling `validateAccess` needs a scan target. **That join exists and nothing has ever walked it.**

**Every proposed component is marked `derived: true`.** A reviewer must be able to tell what the
package was told from what it worked out — otherwise the next person reads a derivation as a
decision, which is how `platform-P01.md` came to claim 35 screens against a live 46.

Run: `python3 tools/derive-components.py [--apply]`
Without `--apply` it reports and writes nothing.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml


def _yload(src):
    """YAML with the C loader, the pure one where a file defeats it (20 October 2026, CHG-R8GEN-016): the screen files
    are 25 MB and the pure loader took most of each refresh step's minute; the loaded data is the same."""
    text = src.read() if hasattr(src, "read") else src
    try:
        return yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        return yaml.safe_load(text)

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# **Density decides the list component, not preference.** `_components.yaml` says a card list is
# preferred over a table on touch surfaces, and a cashier at arm's length cannot hit a table row.
TOUCH = {"touchLarge", "touch"}

# What an operation implies, by the shape of its name and verb. Ordered — the first match wins,
# because `listKitchenTickets` on a kitchen display is a rail before it is a table.
IMPLIES = [
    # (test, kind, label, why)
    (lambda o, v, p: "scan" in o.lower() or "validateaccess" in o.lower(),
     "scanTarget", None,
     "**A screen that validates a credential needs somewhere to point the camera.** `denied` and "
     "`hardwareError` look different because an operator facing a guest needs to know whether to "
     "try again or explain something."),
    (lambda o, v, p: o.startswith("get") and "{" in p and v == "GET",
     "detailPanel", None,
     "One record, read-only."),
    (lambda o, v, p: o.startswith("list") and v == "GET",
     "dataTable", None,
     "**Cursor pagination, never offset** — offset drifts under concurrent writes, which on a "
     "venue's busiest hour is a list that skips rows."),
    (lambda o, v, p: o.startswith("search") or "lookup" in o.lower(),
     "searchField", "Search",
     "A search that returns nothing must say so differently from a search not yet run."),
    (lambda o, v, p: v == "DELETE" or o.startswith(("delete", "revoke", "cancel", "void")),
     "destructiveButton", None,
     # Built per operation by destructive_note(): a fixed example about orders pasted onto a
     # button that voids a coupon code reads as that screen's copy (audit R260).
     None),
    (lambda o, v, p: v in ("POST", "PUT", "PATCH"),
     "primaryButton", None,
     "The act the screen exists for."),
]

# Screens that write need a way not to. A form with a submit and no escape is a trap.
CANCEL = {"kind": "secondaryButton", "label": "Cancel",
          "notes": "**A screen that can submit must be leaveable without submitting.**"}

VERB_LABEL = {
    "create": "Create", "add": "Add", "update": "Save", "set": "Save", "publish": "Publish",
    "approve": "Approve", "reject": "Reject", "submit": "Submit", "accept": "Accept",
    "cancel": "Cancel", "delete": "Delete", "revoke": "Revoke", "void": "Void",
    "assign": "Assign", "release": "Release", "sync": "Sync", "export": "Export",
    "import": "Import", "send": "Send", "verify": "Verify", "claim": "Claim",
}


# **Acronyms keep their capitals.** `setAiPolicy` split and lower-cased is *Save ai policy*, which
# is not a sentence-case label; the package writes AI, API, F&B, SLA, SEO and VSI everywhere else.
ACRONYMS = {
    "ai": "AI", "api": "API", "fnb": "F&B", "sla": "SLA", "seo": "SEO", "vsi": "VSI",
    "sms": "SMS", "pos": "POS", "kds": "KDS", "qr": "QR", "nfc": "NFC", "pdf": "PDF",
    "csv": "CSV", "url": "URL", "otp": "OTP", "kyc": "KYC", "vat": "VAT", "id": "ID",
    "fx": "FX", "rfid": "RFID", "sso": "SSO", "mfa": "MFA", "crm": "CRM", "cms": "CMS",
}


def noun_for(rest: str) -> str:
    """`FnbOrder` -> `F&B order`: split the camel case, lower-case it, restore acronyms."""
    words = re.sub(r"(?<!^)(?=[A-Z])", " ", rest).strip().lower().split()
    return " ".join(ACRONYMS.get(w, w) for w in words)


def destructive_note(op: str) -> str:
    """The confirmation guidance for a destructive button, about what *this* operation removes.

    It says what the body must name and never supplies example copy: a made-up count and amount
    reads as the screen's wording, and the real consequence is the screen's to state.
    """
    m = re.match(r"^([a-z]+)([A-Z].*)$", op)
    what = noun_for(m.group(2)) if m else "record"
    return ("**Always confirms, never the default focus.** The consequence goes in the body — "
            f"which {what} is affected and what goes with it, in the screen's own words; "
            "*are you sure* is not a confirmation.")


def label_for(op: str) -> str | None:
    """A button label from the operation name, or nothing.

    **`createWorkOrder` becomes *Raise*, not *Create work order*.** A label that reads back the
    operation name is a label written for the developer rather than the person pressing it — and
    where nothing sensible falls out, no label is better than a bad one.
    """
    m = re.match(r"^([a-z]+)([A-Z].*)$", op)
    if not m:
        return None
    verb, rest = m.group(1), m.group(2)
    if verb not in VERB_LABEL:
        return None
    noun = noun_for(rest)
    return f"{VERB_LABEL[verb]} {noun}" if len(noun) < 22 else VERB_LABEL[verb]


def propose(screen: dict, lin: dict, density: str) -> list[dict]:
    """Components this screen's operations imply, minus what it already declares."""
    ops = [a.get("operationId") for a in (screen.get("apis") or [])
           if a.get("operationId") in lin]
    if not ops:
        return []

    have = {c.get("kind") for r in ((screen.get("layout") or {}).get("regions") or [])
            for c in (r.get("components") or [])}
    out: list[dict] = []
    seen: set = set(have)

    for op in ops:
        v, p = lin[op]["verb"], lin[op]["path"]
        for test, kind, label, why in IMPLIES:
            if not test(op, v, p):
                continue
            # a touch surface lists in cards, not rows
            if kind == "dataTable" and density in TOUCH:
                kind = "cardList"
            if kind in seen:
                break
            c = {"kind": kind, "derived": True, "impliedBy": op}
            lbl = label or (label_for(op) if kind.endswith("Button") else None)
            if lbl:
                c["label"] = lbl
            c["notes"] = why if why is not None else destructive_note(op)
            out.append(c)
            seen.add(kind)
            break

    writes = [o for o in ops if lin[o]["verb"] in ("POST", "PUT", "PATCH", "DELETE")]
    if writes and "secondaryButton" not in seen:
        out.append({**CANCEL, "derived": True, "impliedBy": writes[0]})

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--min", type=int, default=2,
                    help="only touch screens declaring fewer than this many components")
    a = ap.parse_args()

    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    # **A client-approved screen is not proposed to** (r10 gate 2, 26 October 2026, CHG-R10GFP-004). What this adds is
    # visible UI, and the approved UI is fixed (CHG-GRD-002; since 22 October a change to it is a CR logged in ADAM and
    # docs/active/approved-ui-changes.yaml). CR-186 added updateMyProfile to GST-043's apis, an onAction call made after
    # the language is chosen, and this then gave the approved screen "Save my profile" and "Cancel", which no decision
    # asked for. The approved screens are the snapshot check-approved-ui compares with (handoff/approved-ui.json).
    try:
        approved = set((json.loads((ROOT / "handoff" / "approved-ui.json").read_text(encoding="utf-8"))
                        .get("screens") or {}))
    except (OSError, ValueError):
        approved = set()
    added = Counter()
    touched = 0

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = _yload(f.read_text(encoding="utf-8"))
        code = (doc.get("platform") or {}).get("code", "")
        changed = False
        for s in doc.get("screens") or []:
            if s.get("id") in approved:
                continue
            regions = (s.get("layout") or {}).get("regions") or []
            n = sum(len(r.get("components") or []) for r in regions)
            if n >= a.min:
                continue
            new = propose(s, lin, s.get("density", ""))
            if not new:
                continue
            # **The body region is made only for what goes into it** (CHG-R10GFP-004): it was appended, empty, to every
            # screen without one before the count, and written whenever another screen of the file gained components,
            # so five approved guest screens (GST-018, -042, -051, -056, -067) gained an empty region
            regions = s.setdefault("layout", {}).setdefault("regions", regions)
            body = next((r for r in regions if r.get("name") == "contentBody"), None)
            if body is None:
                body = {"name": "contentBody", "components": []}
                regions.append(body)
            body.setdefault("components", []).extend(new)
            for c in new:
                added[c["kind"]] += 1
            touched += 1
            changed = True
        if changed and a.apply:
            head = "".join(x for x in f.read_text(encoding="utf-8").splitlines(keepends=True)
                           if x.startswith("#"))
            # width 100, the derivers' form (derive-screen-wiring, derive-state-views): at 98 this rewrapped every long
            # note of a file it touched and the next refresh's width-100 writers wrapped them back, so the refresh
            # chain was no fixed point (check-regenerate-twice RT-CHAIN on P02, r10 gate 2, CHG-R10GFP-003)
            f.write_text(head + "\n" + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                                      width=100), encoding="utf-8")

    print(f"  {touched} screens would gain components" if not a.apply
          else f"  {touched} screens enriched")
    for k, v in added.most_common():
        print(f"    {v:>4}  {k}")
    if not a.apply:
        print("  nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
