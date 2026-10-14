#!/usr/bin/env python3
"""The 17 cross-deployable write exceptions removed, in r6 (14 October 2026, batch XDW; CHG-XDW-001 to CHG-XDW-005).

CR-002 (CHG-R6-020) left 17 writes that could not route yet on `docs/active/cross-deployable-writes.yaml`, each to be
removed by r5. r5 was tagged and `tools/check-cross-deployable-writes.py` failed all 17 X-EXPIRED. Chinmay asked
"Remove them now ?" on 14 October 2026. This is the lineage half; the contracts carry the rest.

* **CrossRegionService's four records move from `platform` to `sync`** (CHG-XDW-001; XDW-001 to XDW-011).
  `platform.guest_link`, `platform.dsar_request`, `platform.cross_region_entitlement` and
  `platform.wallet_authorisation` are read and written only by CrossRegionService (operations) and sat in
  TenancyService's schema (commerce). Every lineage read, write and `readColumns` key naming them is renamed, so
  their writes are the owner's own (the renames are declared in `tools/derive-schema-history.py`).
* **`platform.dead_letter` is requeued by its owner** (CHG-XDW-003; XDW-012). `replayDeadLetter` (operations) calls
  tenancy `requeueDeadLetter`, which writes the dead letter and the outbox row; the caller no longer writes
  `platform.outbox` itself. `requeueDeadLetter` reads and writes `platform.dead_letter` and writes `platform.outbox`.
* **Identity writes its `pii` rows for Marketing** (CHG-XDW-004, CHG-XDW-005; XDW-016, XDW-017).
  `recordConsentIdentifier` writes `pii.consent_identifier`; `updateGuestSubjectDetails` reads and writes
  `pii.subject`. Their request bodies are `none — request only`, so derive-lineage gives them no table.

`sync.rejection` (CHG-XDW-002; XDW-013 to XDW-015) needs nothing here: derive-lineage reads `recordSyncRejection`'s
and `recordSyncRejectionResolution`'s tables off the contract, and copies every route into `writeVia`.

Run after `python tools/derive-lineage.py --apply` has added the five new operations; a second run changes nothing.

    python tools/applied/xdw-routes-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MOVES = {"platform." + t: "sync." + t for t in ("guest_link", "dsar_request", "cross_region_entitlement",
                                                 "wallet_authorisation")}
MOVE_WHY = "CHG-XDW-001: CrossRegionService's records moved from platform to sync (XDW-001 to XDW-011 removed)"

# operation -> ({field: value}, why)
SET = {
    "requeueDeadLetter": ({"reads": ["platform.dead_letter"], "writes": ["platform.dead_letter", "platform.outbox"]},
                          "CHG-XDW-003: the owner requeues a dead letter for replayDeadLetter (XDW-012 removed)"),
    "replayDeadLetter": ({"writes": ["cache:idempotency", "platform.dead_letter"]},
                         "CHG-XDW-003: platform.dead_letter is written by tenancy requeueDeadLetter (writeVia), which "
                         "also writes the outbox row; this no longer writes platform.outbox itself"),
    "recordConsentIdentifier": ({"writes": ["pii.consent_identifier"]},
                                "CHG-XDW-004: Identity keeps the consent identifier for recordDeviceConsent "
                                "(XDW-016 removed)"),
    "updateGuestSubjectDetails": ({"reads": ["pii.subject"], "writes": ["pii.subject"]},
                                  "CHG-XDW-005: Identity corrects the guest's subject for updateMyProfile "
                                  "(XDW-017 removed)"),
}


def note(e: dict, text: str) -> None:
    text = "14 October 2026: " + text
    if text not in str(e.get("fixNote") or ""):
        e["fixNote"] = (e["fixNote"] + "; " + text) if e.get("fixNote") else text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    missing = [o for o in SET if o not in lin]
    if missing:
        raise SystemExit("not in the lineage (run tools/derive-lineage.py --apply first): " + ", ".join(missing))
    n = 0
    for o, e in lin.items():
        changed = False
        for k in ("reads", "writes"):
            old = list(e.get(k) or [])
            new = sorted({MOVES.get(t, t) for t in old})
            if any(t in MOVES for t in old):
                e[k] = new
                changed = True
        rc = e.get("readColumns")
        if isinstance(rc, dict) and any(t in MOVES for t in rc):
            e["readColumns"] = {MOVES.get(t, t): c for t, c in rc.items()}
            changed = True
        if changed:
            note(e, MOVE_WHY)
            n += 1
    for o, (fields, why) in SET.items():
        e = lin[o]
        if any(e.get(k) != v for k, v in fields.items()):
            e.update(fields)
            note(e, why)
            n += 1
    print("lineage entries changed: %d" % n)
    if a.apply and n:
        out = json.dumps(lin, indent=1, ensure_ascii=False)
        if raw.endswith("\n"):
            out += "\n"
        if "\r\n" in raw:
            out = out.replace("\n", "\r\n")
        io.open(path, "w", encoding="utf-8", newline="").write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
