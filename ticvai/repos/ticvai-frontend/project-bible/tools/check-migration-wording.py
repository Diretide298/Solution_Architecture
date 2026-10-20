#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every [DB] migration ticket says it is written in our repository, copied from the package's SQL.

**7 October 2026, CHG-R5-002.** A developer's agent stopped MIG-BASELINE (#27646): the ticket names
V0001__baseline.sql, a file the package no longer holds, and sends the developer to the helper functions at the
top of backend/tenant/920-row-level-security.sql and 930-partitioning.sql, files headed "Derived by
tools/derive-ddl.py. Do not hand-edit." The agent read that as a ban on copying from them. The words that settle it
are tools/ticket_done.py MIGRATION_WORDING, written by tools/build-service-docs.py into every migration task.

**What fails** (handoff/service-docs/plan-tasks.csv; the package's 920 and 930 files):

  MW-SENTENCE    a [DB] migration task (key MIG-* or VM-MIG-*) whose description lacks MIGRATION_WORDING
  MW-BASELINE    MIG-BASELINE missing, or its description does not name every function 920 and 930 define (the
                 helpers it copies, read from the files, so a helper added there is named on the ticket)
  MW-MIGRATIONS  handoff/service-docs/backend/MIGRATIONS.md does not carry the same words
  MW-SOURCE      a [DB] migration task with no "Source DDL:" (MIG-FOREIGN-KEYS and MIG-PARTITIONS had none)
  MW-AFTER-R1    a table a frozen after-r1 file (backend/<db>/V01nn__after_r1_*.sql) changes without creating it, whose
                 creating migration task does not cite that file, or that no migration task creates (the lead's check
                 of 7 October: V0101's columns on catalogue.product and catalogue.performance were on no ticket).
                 A table no task creates because only held operations reach it (CHG-FXP-003; listed `held:` under
                 "Tables no migration creates" in MIGRATIONS.md) passes only when that row cites the file
                 ("Source DDL after r1: <file>"), so the migration planned with its operations applies the change
                 (CHG-GT1-007: CHG-MOD-007 scoped approvals.accreditation_badge in V0104)
                 A table no operation reaches yet (`storage only:`) passes the same way (CHG-R8MIG-024).

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-migration-wording.py [--all]
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import ticket_done as td  # noqa: E402

RULES = {
    "MW-SENTENCE": "a [DB] migration ticket without the 'write it in our repository' sentence (CHG-R5-002)",
    "MW-BASELINE": "MIG-BASELINE does not name every helper function 920 and 930 define (CHG-R5-002)",
    "MW-MIGRATIONS": "the generated MIGRATIONS.md does not carry the migration wording (CHG-R5-002)",
    "MW-SOURCE": "a [DB] migration ticket with no Source DDL (CHG-R5-002)",
    "MW-AFTER-R1": "a table an after-r1 file changes, not cited by the migration ticket that creates it (CHG-R5-002)",
}
SD = Path("handoff") / "service-docs"


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-migration-wording", RULES)
    plan = g.ROOT / SD / "plan-tasks.csv"
    if not plan.exists():
        guard.note("plan-tasks.csv missing: run tools/build-service-docs.py")
        return guard.finish()
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["type"] == "Task"]
    n = 0
    made_by = {}
    for r in rows:
        if not (td.MIGRATION_KEY.match(r["key"]) and (r["track"] == "Database" or r["subject"].startswith("[DB]"))):
            continue
        n += 1
        if td.MIGRATION_WORDING not in (r["description"] or ""):
            guard.add("MW-SENTENCE", r["key"], f"{r['key']}: its description lacks the migration wording")
        if "Source DDL:" not in (r["description"] or ""):
            guard.add("MW-SOURCE", r["key"], f"{r['key']}: its description names no Source DDL")
        m = re.search(r"Tables: (.+?)\. Source", r["description"] or "")
        for t in (m.group(1).split(", ") if m else []):
            made_by.setdefault(t.strip(), r)
    held = {}
    mmd = g.ROOT / SD / "backend" / "MIGRATIONS.md"
    if mmd.exists():
        seg = mmd.read_text(encoding="utf-8").split("## Tables no migration creates", 1)
        if len(seg) == 2:
            for t, why in re.findall(r"^\| `([a-z_]+\.[a-z_0-9]+)` \| \w+ \| [^|]* \| ((?:held|storage only): .+?) \|$", seg[1], re.M):
                held[t] = why
    # **A table a declared move took to another database** (ADAM CR-150, 18 October 2026; CHG-CRA-003): V0104 changed
    # subscription.plan and four others in the tenant database before they moved to control, where the next forward
    # migration creates them afresh and the tenant copy is dropped (handoff/migration-review.md). The change follows
    # the table: the task that creates it under its new name answers for it.
    try:
        import importlib.util as _iu
        _sp = _iu.spec_from_file_location("derive_schema_history", g.ROOT / "tools" / "derive-schema-history.py")
        _mod = _iu.module_from_spec(_sp)
        _sp.loader.exec_module(_mod)
        moved_to = {x["from"]: x["to"] for x in _mod.RENAMES
                    if x["from"].split(".")[0] != "control" and x["to"].split(".")[0] == "control"}
    except Exception:          # noqa: BLE001 -- no history: nothing has moved
        moved_to = {}
    n_ar1 = 0
    for (rel, t), _ in sorted(td.after_r1_changes(g.ROOT).items()):
        n_ar1 += 1
        r = made_by.get(t)
        if r is None and moved_to.get(t) in made_by:
            guard.note(f"{rel} changes {t}, which moved to {moved_to[t]} ({made_by[moved_to[t]]['key']} creates it "
                       "there; the tenant copy is dropped)")
            continue
        if r is None and f"Source DDL after r1: {rel}" in held.get(t, ""):
            continue          # held with its operations (CHG-FXP-003); the row cites the file (CHG-GT1-007)
        if r is None:
            guard.add("MW-AFTER-R1", f"{rel}:{t}", f"{rel} changes {t}, which no migration task creates"
                      + (" (it is held, and its row in MIGRATIONS.md does not cite the file)" if t in held else ""))
        elif f"Source DDL after r1: {rel}" not in (r["description"] or "") or t not in r["description"]:
            guard.add("MW-AFTER-R1", f"{rel}:{t}", f"{r['key']} creates {t} but does not cite {rel}, which changes it")
    base = next((r for r in rows if r["key"] == "MIG-BASELINE"), None)
    fns = td.baseline_functions(g.ROOT)
    if base is None:
        guard.add("MW-BASELINE", "MIG-BASELINE", "MIG-BASELINE is not in the plan")
    else:
        for name, names in fns.items():
            if not names:
                guard.add("MW-BASELINE", name, f"backend/tenant/{name} defines no function: the helpers moved")
            for f in names:
                if f not in (base["description"] or ""):
                    guard.add("MW-BASELINE", f, f"MIG-BASELINE does not name {f} ({name})")
    md = g.ROOT / SD / "backend" / "MIGRATIONS.md"
    if not md.exists() or td.MIGRATION_WORDING not in md.read_text(encoding="utf-8"):
        guard.add("MW-MIGRATIONS", "MIGRATIONS.md", "handoff/service-docs/backend/MIGRATIONS.md lacks the wording")
    guard.note(f"{n} [DB] migration tasks; {n_ar1} table(s) changed by after-r1 files; MIG-BASELINE copies {sum(len(v) for v in fns.values())} functions "
               f"({', '.join(f'{k}: {len(v)}' for k, v in fns.items())})")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
