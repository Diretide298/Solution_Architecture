#!/usr/bin/env python3
"""Give the operations agreed on 29 September the tables they read and write.

The readiness close-out agreed 574 provisional operations (docs/registers/readiness-closeout.md). Their
lineage entries had been written empty while they were drafts, and `derive-lineage.py --apply` only adds
entries and never updates one, so they stayed empty. The ticket generator builds a Venue Management
ticket only for screens whose operations are agreed *and* have lineage, and twenty-plus tools read the
lineage as authoritative.

Mapping them showed about 250 tables they need did not exist. Those were designed and declared in their
contracts the same day (groups DM1 to DM6). This writes the resulting mappings (reads, writes, a one-line
evidence note) into handoff/api-data-lineage.json.

It fills **entries whose reads and writes are both empty**. An entry somebody already mapped is a judgement:
it is only ever **added to** (the union of what it had and the tables the new model gives it), never
reduced, so a writer of a table declared today (for example `escalateCase` writing
`marketing.case_escalation`) records it without losing what it recorded before. Each written entry is marked
`source: "hand-mapped 29 September (readiness close-out)"`.

    python tools/applied/closeout-lineage-29-september.py <mapping.json> [...] [--apply]
"""
import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mappings", nargs="+")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    raw = LINEAGE.read_text(encoding="utf-8")
    lin = json.loads(raw)
    # The tables derive-schema knows (run it first): the DDL itself is only written later in the refresh.
    tables = set(json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))["cols"])
    # Read routing straight off the contracts: the writers pass moved 20 promotions analytics reads from
    # replica to analytical there, and a stored lineage entry never picks that up on its own.
    routing_of = {}
    for cf in sorted((ROOT / "contracts").glob("*/*.yaml")):
        for item in ((yaml.safe_load(cf.read_text(encoding="utf-8")) or {}).get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId") and op.get("x-ticvai-read-routing"):
                    routing_of[op["operationId"]] = op["x-ticvai-read-routing"]
    written = kept = unknown = 0
    bad = set()
    for path in a.mappings:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        # DM files map operations at the top level; writers-pass files nest them under "lineage".
        for op, m in (doc.get("lineage") if isinstance(doc.get("lineage"), dict) else doc).items():
            if op.startswith("_") or not isinstance(m, dict):
                continue
            if op not in lin:
                unknown += 1
                continue
            e = lin[op]
            had = set(e.get("reads") or []) | set(e.get("writes") or [])
            # A value that is not a list ("unchanged (DM5)") means the mapping leaves that side alone.
            mr = m.get("reads") if isinstance(m.get("reads"), list) else []
            mw = m.get("writes") if isinstance(m.get("writes"), list) else []
            reads = sorted(set(mr) | set(e.get("reads") or []))
            writes = sorted(set(mw) | set(e.get("writes") or []))
            # A routing decision (replica -> analytical for reporting reads, WC) travels with the mapping.
            routing = m.get("routing") or routing_of.get(op)
            rerouted = bool(routing and routing != e.get("routing"))
            if rerouted:
                e["routing"] = routing
            if (not rerouted and had and set(reads) | set(writes) == had
                    and reads == sorted(e.get("reads") or [])):
                kept += 1
                continue
            bad |= {t for t in reads + writes if not t.startswith("cache:") and t not in tables}
            if reads or writes:
                e["reads"], e["writes"] = reads, writes
                if not had:
                    e["source"] = "hand-mapped 29 September (readiness close-out)"
                if m.get("note"):
                    e["lineageNote"] = m["note"]
                written += 1
    print(f"{written} entries written or extended, {kept} unchanged, {unknown} not in the lineage")
    if bad:
        print(f"{len(bad)} tables named that the DDL does not have yet (derive-schema must run first): "
              + ", ".join(sorted(bad)[:30]))
    if a.apply:
        # newline="" so Windows does not turn the file's LF into CRLF.
        with open(LINEAGE, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(lin, indent=1, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
    else:
        print("dry run; pass --apply")


if __name__ == "__main__":
    main()
