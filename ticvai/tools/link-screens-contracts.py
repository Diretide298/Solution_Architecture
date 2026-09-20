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
# The shipped `contracts/` is authoritative. Until 17 August these pointed at a sibling repo
# outside the package, so every validator passed for whoever had that repo checked out and read
# nothing for anyone working from the zip — which is the worst failure a checker can have, because
# it is silent and it looks like success.
CONTRACTS = ROOT / "contracts"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"

CHECK = "--check" in sys.argv


def contract_files() -> list[Path]:
    return sorted(list((CONTRACTS / "spine").glob("*.yaml")) +
                  list((CONTRACTS / "satellite").glob("*.yaml")))


def main() -> int:
    # --- operationId -> contract, from the contracts
    op_contract: dict[str, str] = {}
    for f in contract_files():
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
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
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
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
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        changed = False
        for s in doc["screens"]:
            for api in s.get("apis", []) or []:
                oid = api.get("operationId")
                if oid in op_contract and api.get("contract") != op_contract[oid]:
                    api["contract"] = op_contract[oid]
                    changed = True
        if changed:
            head = "".join(l for l in f.read_text(encoding="utf-8").splitlines(keepends=True) if l.startswith("#"))
            # **This writes a platform file with `allow_unicode=True`, so the encoding matters.**
            # Windows defaults to cp1252, which happily encodes an em dash and a curly quote to
            # bytes no `encoding="utf-8"` reader can decode — the file is written, nothing fails,
            # and the next tool to open it dies pointing at the wrong culprit.
            with f.open("w", encoding="utf-8") as out:
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
        text = f.read_text(encoding="utf-8")
        # strip any previous block, so the operation is idempotent
        # **Any list indentation, not the one this tool happens to write.** The pattern required
        # eight-space items; `yaml.safe_dump` writes them at six, level with the key. When five
        # contracts were reformatted on 10 September the strip stopped matching, the old block
        # survived, a new one was appended beside it, and `check-package` went from 16 errors to
        # 508 duplicate keys in a single run.
        #
        # **The `safe_load` at the end of this loop did not catch it**: PyYAML accepts a duplicate
        # key and keeps the last, so the file parsed cleanly the whole time. A guard that only asks
        # *does it parse* cannot see the one fault this loop is able to cause.
        # **Line-anchored, because two blocks can sit next to each other.** Matching a leading
        # `\n` meant the first block's match consumed the newline the second one needed to start,
        # so a pair was only ever half-removed — which is how the duplicates survived the first
        # attempt at this fix.
        text = _re.sub(r"^ +x-ticvai-consumed-by:\n(?:[ ]+- [^\n]*\n)+", "", text, flags=_re.M)
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
        f.write_text(text, encoding="utf-8")
        yaml.safe_load(f.read_text(encoding="utf-8"))  # fail loudly rather than leave a broken contract

    print(f"linked {consumed} operations to screens")
    print(f"{uncovered} operations have no screen consuming them")
    print()
    # **This number has been read as a design backlog at least three times and it is not one.**
    # On 20 September it was 257 and 105 of them needed no screen: a write reached from the
    # screen its sibling read feeds, an operation running inside a turnstile, a webhook, a job.
    # Printing the raw count with no route to the answer is what made it keep coming back.
    print("Most of these need no screen. `handoff/operations-without-screens.md` records which")
    print("kinds and why; `tools/audit-screenless-operations.py` applies it and prints only the")
    print("ones that are genuinely unspecified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
