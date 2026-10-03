#!/usr/bin/env python3
"""Every migration ticket names its file, the names agree everywhere, and every table is in a migration or says why not.

**3 October 2026, CHG-TBF-002 and CHG-TBF-003** (Block A audit on live r2, pattern 6;
`changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`). The audit found 492 table rows whose forward
migration ticket named no file ("their file numbers are given when they merge"), 304 whose first-release
ticket named one file while `backend/MIGRATIONS.md` named another for the same schema (`V0026__access.sql` on
the ticket, `V0007__access.sql` in the document; neither exists, and MIG-RETAIL had two), and 148 tables in
`backend/` that no migration created. The plan's numbering is `tools/build-service-docs.py` (FORWARD_TICKET_FIRST):

    V0001          the baseline (MIG-BASELINE)
    V0002-V0099    the first release, one per schema in key order (MIG-<SCHEMA>, MIG-FOREIGN-KEYS last)
    V0100-V0999    derive-ddl's frozen-mode files, backend/<db>/V01xx__after_r1_<date>.sql (never a ticket's)
    V1000-         every later forward migration (VM-MIG-*, MIG-<SCHEMA>-<n>), in build order, kept once planned

**What fails** (from handoff/service-docs/plan-tasks.csv, the plan build-service-docs.py writes):

  M-FILE-NAMED      a migration ticket (a Database task) whose subject names no V-file
  M-FILE-UNIQUE     two tickets name the same file number
  M-FILE-RANGE      a number outside its range (a first-release migration from V0100, a forward one below V1000)
  M-FILE-ORDER      a migration that depends on a migration with a higher number (it would run first)
  M-MD-AGREES       the generated handoff/service-docs/backend/MIGRATIONS.md gives a task another file, or misses it
  M-BACKEND-MD      backend/MIGRATIONS.md names a V-file that is neither in backend/<db>/ nor on any ticket
  M-TABLE-ASSIGNED  a table in backend/ in no migration ticket and not listed, with its reason, under
                    "Tables no migration creates"; or listed there although an operation reads or writes it

**Exempt, with the reason:** MIG-PARTITIONS is a job in the workers host that creates and detaches monthly
partitions (ADR-0056), not a migration file. The baseline tables in 000-002 are MIG-BASELINE's.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-migration-tickets.py [--all]
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "M-FILE-NAMED": "a migration ticket names no V-file (CHG-TBF-002)",
    "M-FILE-UNIQUE": "two migration tickets name the same file number (CHG-TBF-002)",
    "M-FILE-RANGE": "a migration file number outside its range (CHG-TBF-002)",
    "M-FILE-ORDER": "a migration depends on one with a higher file number (CHG-TBF-002)",
    "M-MD-AGREES": "the generated MIGRATIONS.md and the ticket name different files (CHG-TBF-002)",
    "M-BACKEND-MD": "backend/MIGRATIONS.md names a file no ticket and no backend/ file has (CHG-TBF-002)",
    "M-TABLE-ASSIGNED": "a table in no migration and not listed with its reason (CHG-TBF-003)",
}
EXEMPT = {"MIG-PARTITIONS": "a job in the workers host (ADR-0056), not a migration file"}
FILE = re.compile(r"\b(V(\d{4})[a-z]?__[\w.-]+\.sql)\b")
FIRST, FORWARD_FIRST = (2, 99), 1000
CREATE = re.compile(r'CREATE TABLE IF NOT EXISTS ([a-z_]+)\."?([a-z_0-9]+)"? \(')


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-migration-tickets", RULES)
    sd = g.ROOT / "handoff" / "service-docs"
    plan = sd / "plan-tasks.csv"
    if not plan.exists():
        guard.note("handoff/service-docs/plan-tasks.csv missing - run tools/build-service-docs.py")
        return guard.finish()
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh)]
    migs = {r["key"]: r for r in rows if r["type"] == "Task" and r["track"] == "Database" and "#" not in r["key"]}
    file_of, num_of, by_num = {}, {}, {}
    for k, r in sorted(migs.items()):
        if k in EXEMPT:
            guard.note(f"{k} exempt: {EXEMPT[k]}")
            continue
        m = FILE.search(r["subject"])
        if not m:
            guard.add("M-FILE-NAMED", k, f"{k}: '{r['subject'][:90]}' names no migration file")
            continue
        file_of[k], num_of[k] = m.group(1), int(m.group(2))
        by_num.setdefault(num_of[k], []).append(k)
        forward = "Forward migration" in r["subject"]
        n = num_of[k]
        if k == "MIG-BASELINE":
            ok = n == 1
        elif forward:
            ok = n >= FORWARD_FIRST
        else:
            ok = FIRST[0] <= n <= FIRST[1]
        if not ok:
            guard.add("M-FILE-RANGE", k, f"{k}: {file_of[k]} is outside the range for "
                                         f"{'a forward' if forward else 'a first-release'} migration")
    for n, ks in sorted(by_num.items()):
        if len(ks) > 1:
            guard.add("M-FILE-UNIQUE", f"V{n:04d}", f"V{n:04d} is named by {', '.join(ks)}")
    for k, r in sorted(migs.items()):
        for d in (r.get("dependsOn") or "").split():
            if k in num_of and d in num_of and num_of[d] >= num_of[k]:
                guard.add("M-FILE-ORDER", f"{k}->{d}",
                          f"{k} ({file_of[k]}) depends on {d} ({file_of[d]}), which would run after it")

    # The generated MIGRATIONS.md: the first-release order table and the forward table.
    md = sd / "backend" / "MIGRATIONS.md"
    listed_storage = {}
    if md.exists():
        text = md.read_text(encoding="utf-8")
        in_md = {}
        for f, task in re.findall(r"^\| \d+ \| `(V\d{4}[^`]*\.sql)` \| ([A-Z][A-Z0-9-]+) \|", text, re.M):
            in_md[task] = f
        for k, f in sorted(file_of.items()):
            if in_md.get(k) != f:
                guard.add("M-MD-AGREES", k, f"{k}: the ticket names {f}, handoff/service-docs/backend/MIGRATIONS.md "
                                            f"{in_md.get(k) or 'nothing'}")
        seg = text.split("## Tables no migration creates", 1)
        if len(seg) == 2:
            for t, why in re.findall(r"^\| `([a-z_]+\.[a-z_0-9]+)` \| \w+ \| [^|]* \| (.+?) \|$", seg[1], re.M):
                listed_storage[t] = why
    else:
        guard.note("handoff/service-docs/backend/MIGRATIONS.md missing - the agreement rule did not run")

    # backend/MIGRATIONS.md, the hand-written account of the layout.
    real = {p.name for d in ("tenant", "control") for p in (g.ROOT / "backend" / d).glob("V*.sql")}
    named = set(file_of.values())
    bmd = g.ROOT / "backend" / "MIGRATIONS.md"
    if bmd.exists():
        for f in sorted(set(FILE.findall(bmd.read_text(encoding="utf-8")))):
            name = f[0]
            if name not in real and name not in named and not re.match(r"V\d{4}__after_r1_<", name):
                guard.add("M-BACKEND-MD", name, f"backend/MIGRATIONS.md names {name}, which is neither a file in "
                                                f"backend/<db>/ nor on any migration ticket")

    # Every table in backend/ is in a migration ticket, or listed with the reason it is not.
    tables = set()
    for d in ("tenant", "control"):
        for p in (g.ROOT / "backend" / d).glob("*.sql"):
            if p.name.startswith(("000", "001", "002")):
                continue                                   # the baseline's own: MIG-BASELINE
            tables |= {f"{a}.{b}" for a, b in CREATE.findall(p.read_text(encoding="utf-8"))}
    on_ticket = set()
    for r in migs.values():
        m = re.search(r"Tables: (.+?)\. Source", r["description"] or "")
        if m:
            on_ticket |= set(m.group(1).split(", "))
    lineage = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    reached = {}
    for o, x in lineage.items():
        for kk in ("reads", "writes"):
            for t in (x or {}).get(kk) or []:
                reached.setdefault(t, set()).add(o)
    for t in sorted(tables - on_ticket):
        why = listed_storage.get(t)
        if not why:
            guard.add("M-TABLE-ASSIGNED", t, f"{t}: in backend/ but in no migration ticket and not listed under "
                                             "'Tables no migration creates'")
        elif reached.get(t) or why.startswith("GAP"):
            guard.add("M-TABLE-ASSIGNED", t, f"{t}: listed as needing no migration, but "
                                             f"{', '.join(sorted(reached.get(t, ()))[:3]) or 'it'} reads or writes it")
    guard.note(f"{len(file_of)} migration ticket(s) named, {len(tables)} table(s) in backend/, "
               f"{len(tables & on_ticket)} in a migration, {len(listed_storage)} listed as storage only")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
