#!/usr/bin/env python3
"""
Link screens and contracts, both directions, from one source.

Screens declare which operations they call. That is the only place the relationship is
hand-written; everything else here is derived from it, so the two can never disagree.

Injects:
  * into each screen's api entry — `contract`, so you know which file to open
  * into each operation — `x-ticvai-consumed-by`, the screens that call it
  * into each contract's info — `x-ticvai-screen-count`

Also reports operations no screen consumes. That number is the useful output: an endpoint
nobody calls is either a screen not yet specified, or an endpoint that should not exist.

Run: python3 tools/link-screens-contracts.py [--check]
"""
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai-contracts" / "openapi"

CHECK = "--check" in sys.argv


def contract_files() -> list[Path]:
    return sorted(list((CONTRACTS / "spine").glob("*.yaml")) +
                  list((CONTRACTS / "satellite").glob("*.yaml")))


def main() -> int:
    # --- operationId -> contract, from the contracts
    op_contract: dict[str, str] = {}
    for f in contract_files():
        doc = yaml.safe_load(f.read_text())
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                    if oid := op.get("operationId"):
                        op_contract[oid] = f.stem

    # --- operationId -> screens, from the screens
    op_screens: dict[str, list[str]] = defaultdict(list)
    screen_files = sorted(SCREENS.glob("P*.yaml"))
    for f in screen_files:
        doc = yaml.safe_load(f.read_text())
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            for api in s.get("apis", []) or []:
                oid = api.get("operationId")
                if oid and oid != "TODO":
                    op_screens[oid].append(f"{code} {s['id']} {s['name']}")

    unknown = sorted(o for o in op_screens if o not in op_contract)
    if unknown:
        for o in unknown:
            print(f"  FAIL  screen references unknown operationId '{o}'")
        return 1

    if CHECK:
        print(f"{len(op_screens)} operations referenced by screens, all resolve")
        return 0

    # --- write `contract` back into the screens
    for f in screen_files:
        doc = yaml.safe_load(f.read_text())
        changed = False
        for s in doc["screens"]:
            for api in s.get("apis", []) or []:
                oid = api.get("operationId")
                if oid in op_contract and api.get("contract") != op_contract[oid]:
                    api["contract"] = op_contract[oid]
                    changed = True
        if changed:
            head = "".join(l for l in f.read_text().splitlines(keepends=True) if l.startswith("#"))
            with f.open("w") as out:
                out.write(head + "\n")
                yaml.safe_dump(doc, out, sort_keys=False, allow_unicode=True, width=98)

    # --- write `x-ticvai-consumed-by` back into the contracts
    #
    # By targeted text insertion, not yaml.safe_dump. Re-dumping would reformat every
    # description, collapse `{ $ref: ... }` to block style and produce a diff nobody can
    # review — for the sake of adding one key per operation.
    import re as _re
    consumed = uncovered = 0
    for f in contract_files():
        text = f.read_text()
        # strip any previous block, so the operation is idempotent
        text = _re.sub(r"\n      x-ticvai-consumed-by:\n(?:        - [^\n]*\n)+", "\n", text)
        n = 0
        for oid, screens in sorted(op_screens.items()):
            marker = f"      operationId: {oid}\n"
            if marker not in text:
                continue
            block = "      x-ticvai-consumed-by:\n" + "".join(
                f"        - \"{s}\"\n" for s in sorted(set(screens)))
            text = text.replace(marker, marker + block, 1)
            n += 1
        total_ops = len(_re.findall(r"^      operationId: ", text, _re.M))
        consumed += n
        uncovered += total_ops - n

        if "x-ticvai-screen-count:" in text:
            text = _re.sub(r"  x-ticvai-screen-count: \d+", f"  x-ticvai-screen-count: {n}", text)
        else:
            text = _re.sub(r"(\n  version: [^\n]+\n)", rf"\1  x-ticvai-screen-count: {n}\n",
                           text, count=1)
        f.write_text(text)
        yaml.safe_load(f.read_text())  # fail loudly rather than leave a broken contract

    print(f"linked {consumed} operations to screens")
    print(f"{uncovered} operations have no screen consuming them")
    print()
    print("An operation nobody calls is either a screen not yet specified, or an endpoint")
    print("that should not exist. Worth reading the gap report before assuming the former.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
