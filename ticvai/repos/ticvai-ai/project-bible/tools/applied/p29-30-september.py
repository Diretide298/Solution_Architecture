# -*- coding: utf-8 -*-
"""Apply the lineage and trace results of the 29 September pass (groups A, B, C, G, S). Re-runnable.

The groups edited contracts, screens and flows directly. What they could not write is the derived
lineage and the traceability rows, because those are handoff files. Each group returned them in
audit/ticvai/steps/P29/<group>.json:

  lineage  {operationId: {reads, writes, note}}: the tables the operation reads and writes after the
           change. **Set, not unioned**: group S removed writes on purpose (a payment no longer posts
           revenue; AccessService issues the tickets), and a union would put them back.
  trace    [{matrixRef, verdict, contract, evidence, note}]

Run `python tools/derive-lineage.py --apply` first so every new operation has an entry to fill.

    python tools/applied/p29-30-september.py [--apply]
"""
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEPS = ROOT.parent / "audit" / "ticvai" / "steps" / "P29"
GROUPS = ["A", "B", "C", "G", "S", "W2"]          # later groups win on the same operation
SOURCE = "29 September pass (P29), applied 30 September 2026"


def main():
    apply = "--apply" in sys.argv
    lp = ROOT / "handoff" / "api-data-lineage.json"
    tp = ROOT / "handoff" / "traceability.json"
    lin = json.loads(lp.read_text(encoding="utf-8"))
    L = lin.get("lineage") if isinstance(lin.get("lineage"), dict) else lin
    tr = json.loads(tp.read_text(encoding="utf-8"))
    rows = {str(r.get("matrixRef")): r for r in tr["rows"]}
    set_, missing, traced, notrow = 0, [], 0, []
    for g in GROUPS:
        f = STEPS / f"{g}.json"
        if not f.exists():
            print(f"  {g}: no result yet")
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        for op, v in (d.get("lineage") or {}).items():
            if op not in L:
                missing.append(op)
                continue
            e = L[op]
            reads = sorted(set(v.get("reads") or []))
            writes = sorted(set(v.get("writes") or []))
            if e.get("reads") != reads or e.get("writes") != writes:
                e["reads"], e["writes"] = reads, writes
                if v.get("note"):
                    e["note"] = v["note"]
                e["source"] = SOURCE
                set_ += 1
        for t in d.get("trace") or []:
            r = rows.get(str(t["matrixRef"]))
            if not r:
                notrow.append(t["matrixRef"])
                continue
            for k in ("verdict", "contract", "evidence", "note"):
                if t.get(k):
                    r[k] = t[k]
            traced += 1
    print(f"  lineage set: {set_}; not yet in lineage (run derive-lineage --apply): {len(missing)} {missing[:8]}")
    print(f"  trace rows set: {traced}; unknown refs: {notrow}")
    if apply:
        lp.write_text(json.dumps(lin, indent=1, ensure_ascii=False), encoding="utf-8")
        tp.write_text(json.dumps(tr, indent=1, ensure_ascii=False), encoding="utf-8")
        print("  applied")
    else:
        print("  dry run: pass --apply")


if __name__ == "__main__":
    main()
