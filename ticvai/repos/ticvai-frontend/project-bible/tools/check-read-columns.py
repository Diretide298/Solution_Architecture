#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A read of personal data by another module names its columns; every read's column list is derived and real.

**ADAM CR-004** (Hrushikant Patkar, ticket #27654 DB-READ-VIEWS, 12 October 2026; fixed in r6 on 14 October,
CHG-LIN-001). DB-READ-VIEWS generates one view per (reader module, owned table) from the lineage, exposing only the
columns the reader's operations read. The lineage recorded reads per table, so every view exposed every column, the
`pii.*` views included: six modules saw `pii.subject.date_of_birth` and `nationality` whether they used them or not.
`tools/derive-read-columns.py` now gives each read the columns it reads (`readColumns`), and this check keeps it so:

  RC-PII-NO-COLUMNS   a read of a `pii.*` table by an operation of another module (its service is not the
                      schema's owner in handoff/service-decomposition.json) with no column list: its view would
                      expose every personal field. Derive it, or add the read to docs/active/read-columns-override.yaml
  RC-STALE            an entry's `readColumns` differs from what tools/derive-read-columns.py derives now: the lists
                      are generated, never hand-edited (a hand list belongs in the override file)
  RC-UNKNOWN          a listed column the table does not have (handoff/schema-reference.json), or a listed table the
                      entry does not read
  RC-OVERRIDE-STALE   an override row whose operation does not read its table, or names a column the table lacks

**Coverage is reported, never failed**, outside `pii.*`: a read whose columns the contract does not show (most are
rule questions answered by a declared query, ADR-0055 as amended in r6, not by a view) keeps an all-column view.

Read-only. No baseline: every member of these rules was fixed when the rule was written.

    python3 tools/check-read-columns.py [--all]
"""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "RC-PII-NO-COLUMNS": "a cross-module read of a pii.* table with no column list: its view would expose every "
                         "personal field (ADAM CR-004, CHG-LIN-001)",
    "RC-STALE": "readColumns differs from tools/derive-read-columns.py: the lists are derived, never hand-edited",
    "RC-UNKNOWN": "a listed column the table does not have, or a listed table the entry does not read",
    "RC-OVERRIDE-STALE": "an override row for a read that does not exist, or with a column the table lacks",
}


def _deriver():
    spec = importlib.util.spec_from_file_location("derive_read_columns", g.ROOT / "tools" / "derive-read-columns.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-read-columns", RULES)
    rc = _deriver()
    lin = g.load_json(rc.LINEAGE, {}) or {}
    pkg = rc.Package()
    over = rc.overrides()
    want, how = rc.derive(pkg, lin, over)
    own = rc.owners()

    for oid, e in sorted(lin.items()):
        have = e.get("readColumns") or {}
        reads = set(e.get("reads") or [])
        for t in sorted(reads):
            if not t.startswith("pii.") or ":" in t:
                continue
            o = own.get(t.split(".", 1)[0])
            if o and o != e.get("service") and not have.get(t):
                guard.add("RC-PII-NO-COLUMNS", f"{oid}.{t}",
                          f"{oid} ({e.get('service')}) reads {t}, owned by {o}, with no column list")
        if have != (want.get(oid) or {}):
            guard.add("RC-STALE", oid, f"{oid}: readColumns is not what tools/derive-read-columns.py derives "
                                       f"(run it with --apply; a hand list goes in the override file)")
        for t, cols in sorted(have.items()):
            if t not in reads:
                guard.add("RC-UNKNOWN", f"{oid}.{t}", f"{oid}: readColumns names {t}, which it does not read")
                continue
            for c in cols:
                if c not in (pkg.cols.get(t) or ()):
                    guard.add("RC-UNKNOWN", f"{oid}.{t}.{c}", f"{oid}: {t} has no column {c}")

    for (oid, t), (cols, _why) in sorted(over.items()):
        if t not in ((lin.get(oid) or {}).get("reads") or []):
            guard.add("RC-OVERRIDE-STALE", f"{oid}.{t}",
                      f"docs/active/read-columns-override.yaml: {oid} does not read {t}")
        for c in cols:
            if c not in (pkg.cols.get(t) or ()):
                guard.add("RC-OVERRIDE-STALE", f"{oid}.{t}.{c}",
                          f"docs/active/read-columns-override.yaml: {t} has no column {c}")

    cov = rc.coverage(lin, how)
    for k, label in (("all", "every read"), ("cross", "cross-module reads"), ("pii_cross", "cross-module pii reads")):
        n = sum(cov[k].values())
        listed = n - cov[k]["none"]
        guard.note("%s: %d of %d have a column list (%.0f%%; %s)" % (
            label, listed, n, 100.0 * listed / max(1, n),
            ", ".join("%s %d" % (s, c) for s, c in sorted(cov[k].items()))))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
