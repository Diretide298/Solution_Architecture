#!/usr/bin/env python3
"""The lineage half of the plan catalogue's move to the control database (18 October 2026; CHG-CRA-003).

ADAM CR-150 (completing CR-097) moved fourteen subscription tables about a tenant rather than inside one to the
control database (ADR-0039): the contracts' `x-ticvai-persistence` names `control.<table>` and the moves are declared
in `tools/derive-schema-history.py` RENAMES. `tools/derive-lineage.py` never removes a table from an entry, so every
lineage read, write and `readColumns` key that still names `subscription.<table>` is renamed here; otherwise
derive-schema would rebuild the old tables from the lineage (check-lineage: "a table that does not exist is rebuilt by
derive-schema from these entries"). The pattern of tools/applied/xdw-routes-14-october.py (CHG-XDW-001).

Run after `python tools/derive-lineage.py --apply`; a second run changes nothing.

    python tools/applied/control-plane-moves-18-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TABLES = ("plan", "plan_limit", "plan_module", "module_listing", "contract", "tier_allowance", "tier_module",
          "licensing_model", "trial_config", "capacity_pack", "go_live_readiness", "enforcement_policy", "vsi_model",
          "vsi_assessment")
MOVES = {"subscription." + t: "control." + t for t in TABLES}
MOVE_WHY = ("CHG-CRA-003: the plan catalogue and the records about a tenant moved from subscription to the control "
            "database (ADAM CR-150, CR-097)")


def note(e: dict, text: str) -> None:
    text = "18 October 2026: " + text
    if text not in str(e.get("fixNote") or ""):
        e["fixNote"] = (e["fixNote"] + "; " + text) if e.get("fixNote") else text


def rename(lin: dict) -> int:
    n = 0
    for _o, e in lin.items():
        changed = False
        for k in ("reads", "writes"):
            old = list(e.get(k) or [])
            if any(t in MOVES for t in old):
                e[k] = sorted({MOVES.get(t, t) for t in old})
                changed = True
        rc = e.get("readColumns")
        if isinstance(rc, dict) and any(t in MOVES for t in rc):
            merged: dict = {}
            for t, c in rc.items():
                key = MOVES.get(t, t)
                merged[key] = sorted(set(merged.get(key, [])) | set(c or [])) if isinstance(c, list) else c
            e["readColumns"] = merged
            changed = True
        if changed:
            note(e, MOVE_WHY)
            n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    raw = io.open(path, encoding="utf-8", newline="").read()
    lin = json.loads(raw)
    n = rename(lin)
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
