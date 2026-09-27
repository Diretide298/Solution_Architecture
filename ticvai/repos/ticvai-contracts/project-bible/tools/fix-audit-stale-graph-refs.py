#!/usr/bin/env python3
"""Bring schema-reference.json's column references into line with the regenerated graph (R082).

**Why this exists.** Audit root R082: `derive-relationships.py` read a stored
`referenceHow: declared` back as a declaration, so name guesses such as
`payments.token.provider_id -> ai.provider`, `inventory.movement.location_id ->
fnb.delivery_location` and `platform.guest_link.guest_link_id -> platform.guest_link` became
enforced foreign keys in `backend/*/900-foreign-keys.sql`. The generator now reads declarations
off the contracts, and `refresh.sh` runs it on every refresh. Two gaps are left that the generator
cannot close by itself:

  1. **Order.** `refresh.sh` runs `derive-schema` *before* `derive-relationships`, and
     `derive-ddl` after both. On the first refresh the DDL is still built from the labels
     derive-schema copied out of the *old* graph; only the second refresh carries the new ones.
  2. **Columns the graph created.** derive-schema keeps a column whose `source` is
     `relationship-graph.json` and only ever *sets* its reference from an edge. When the edge is
     withdrawn, as it is for `whitelabel.navigation_item.navigation_item_id` (a key pointing at
     itself) and `control.release.plan_id`, the stale `references` and `enforced: yes` stay, and
     every later refresh emits the same foreign key again.

This script copies the graph's verdict onto the columns in place. It is idempotent: a second
run finds nothing to do.

  * A column with a foreign-key edge takes the edge's target and `how`, and `enforced` is `yes`
    only for `declared`, which is derive-schema's own rule.
  * A column whose source is a contract property or the graph, and which has no edge, loses its
    reference. A contract `$ref` always produces an edge, so nothing the contract declares is
    touched.
  * Hand-written columns (any other source, e.g. `storage only — pii schema`) are left alone.

Usage (after a refresh, so the graph is the regenerated one):

    python3 tools/fix-audit-stale-graph-refs.py            # dry run: prints what would change
    python3 tools/fix-audit-stale-graph-refs.py --apply    # writes handoff/schema-reference.json

then run `tools/refresh.sh` again so `derive-ddl` rebuilds 900/910/990 from the corrected labels.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "handoff"
KEYS = ("references", "referenceKind", "referenceHow", "enforced")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="write the changes (default: dry run)")
    args = ap.parse_args()

    graph = json.loads((HANDOFF / "relationship-graph.json").read_text(encoding="utf-8"))
    if graph.get("declarations") != "contract":
        print("relationship-graph.json was not produced by the R082 derive-relationships.py "
              "(no `declarations: contract` marker). Run tools/refresh.sh first; nothing done.")
        return 1
    ref_path = HANDOFF / "schema-reference.json"
    schema = json.loads(ref_path.read_text(encoding="utf-8"))

    edges = {}
    for r in graph.get("rels", []):
        if r.get("edgeKind") == "ambient" or str(r.get("col", "")).startswith("via "):
            continue
        edges[(r["frm"], r["col"])] = r

    changes: list[str] = []
    for table, columns in (schema.get("cols") or {}).items():
        for c in columns:
            key = (table, c["column"])
            src = str(c.get("source", ""))
            from_contract = src.count(".") >= 2 and src != "relationship-graph.json" \
                and not src.startswith("derive-schema.py")
            from_graph = src == "relationship-graph.json"
            e = edges.get(key)
            if e:
                want = {
                    "references": e["to"],
                    "referenceKind": e.get("edgeKind", "reference"),
                    "referenceHow": e.get("how", "convention"),
                    "enforced": "yes" if e.get("how") == "declared" else "no",
                }
                have = {k: c.get(k) for k in KEYS}
                if have != want:
                    changes.append(f"{table}.{c['column']}: {have.get('references')} "
                                   f"({have.get('referenceHow')}, enforced={have.get('enforced')})"
                                   f" -> {want['references']} ({want['referenceHow']}, "
                                   f"enforced={want['enforced']})")
                    c.update(want)
            elif c.get("references") and (from_contract or from_graph):
                changes.append(f"{table}.{c['column']}: {c.get('references')} "
                               f"({c.get('referenceHow')}, enforced={c.get('enforced')}) -> "
                               f"no reference")
                for k in KEYS:
                    c.pop(k, None)

    for line in changes:
        print("  " + line)
    print(f"{len(changes)} column(s) {'changed' if args.apply else 'would change'}")
    if args.apply and changes:
        # Same serialisation as derive-schema.py writes it.
        ref_path.write_text(json.dumps(schema), encoding="utf-8")
        print("  -> handoff/schema-reference.json  (now run tools/refresh.sh again)")
    elif not args.apply:
        print("  dry run; pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
