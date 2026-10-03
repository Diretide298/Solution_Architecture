#!/usr/bin/env python3
"""Every primary-key column is required in the schema reference.

**3 October 2026, CHG-TBF-001** (Block A audit on live r2, pattern 6: "table specs that cannot be migrated as
written"; `changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`). PostgreSQL makes every primary-key
column NOT NULL, but 355 key columns (`return_policy.id`, `control.api_licence.id` ...) were `required: no` in
`handoff/schema-reference.json`, because the field behind them is optional on the wire (a create request has
no id yet). The schema reference is what a ticket and ADAM's table view show, so a developer was told a key
may be null. `derive-schema.py` now marks key columns required; this holds it.

**What fails:** a column that the DDL makes (part of) a table's primary key -- an inline `PRIMARY KEY`, a
`CONSTRAINT ... PRIMARY KEY (...)` or an `ALTER TABLE ... ADD PRIMARY KEY` in `backend/<db>/` (the baseline and
the forward migrations after r1) -- that the schema reference lists with `required` other than `yes`. A key
column the schema reference does not list at all (the hand-written machinery tables) is not this check's.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-table-keys.py [--all]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "K-PK-REQUIRED": "a primary-key column the schema reference marks not required (CHG-TBF-001)",
}
CREATE = re.compile(r'CREATE TABLE IF NOT EXISTS ([a-z_]+\.(?:"?[a-z_0-9]+"?)) \((.*?)\n\)[^;]*;', re.S)
ALTER_PK = re.compile(r"ALTER TABLE (?:ONLY )?([a-z_]+\.[a-z_0-9]+) ADD (?:CONSTRAINT \w+ )?PRIMARY KEY \(([^)]*)\)")


def ddl_keys() -> dict:
    """{table: [key columns]} from backend/<db>/*.sql (the partitioning file only adds partitions)."""
    keys = {}
    for db in ("tenant", "control"):
        for f in sorted((g.ROOT / "backend" / db).glob("*.sql")):
            if f.name.startswith("930"):
                continue
            text = f.read_text(encoding="utf-8")
            for m in CREATE.finditer(text):
                name, pk = m.group(1).replace('"', ""), []
                for line in m.group(2).split("\n"):
                    line = line.strip().rstrip(",")
                    c = re.match(r"CONSTRAINT \w+ PRIMARY KEY \(([^)]*)\)", line)
                    if c:
                        pk = [x.strip() for x in c.group(1).split(",")]
                        continue
                    c = re.match(r"([a-z_][a-z_0-9]*)\s+\S+(.*)", line)
                    if c and "PRIMARY KEY" in c.group(2):
                        pk.append(c.group(1))
                keys.setdefault(name, pk)
            for m in ALTER_PK.finditer(text):
                keys[m.group(1)] = [x.strip() for x in m.group(2).split(",")]
    return keys


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-table-keys", RULES)
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = ref.get("cols") or {}
    if not cols:
        guard.note("handoff/schema-reference.json missing or empty - nothing to check")
        return guard.finish()
    n = 0
    for t, pk in sorted(ddl_keys().items()):
        listed = {c.get("column"): c for c in cols.get(t) or []}
        for c in pk:
            rc = listed.get(c)
            if rc is None:
                continue
            n += 1
            if str(rc.get("required")).lower() not in ("yes", "true"):
                guard.add("K-PK-REQUIRED", f"{t}.{c}",
                          f"{t}.{c} is in the primary key but the schema reference says required "
                          f"{rc.get('required')!r} (derive-schema.py marks key columns required)")
    guard.note(f"{n} key column(s) checked against the schema reference")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
