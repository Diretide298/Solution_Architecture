#!/usr/bin/env python3
"""Derive handoff/relationship-graph.json from the schema reference and the lineage.

The graph was hand-maintained and drifted. On 18 August it described 540 relationships across
192 tables while the package held 352 tables — **it had not been touched since the schema grew
past it**, and "Tables with a relationship" read 79% because 160 tables the graph had never
heard of counted as orphans.

Three sources, in order of authority:

  1. `references` on a column in schema-reference.json. Derived by derive-schema.py from
     `x-ticvai-persistence` and the OpenAPI property names, so it moves when a contract moves.
  2. Convention: a `*_id` column naming a table that exists. Weaker, and marked as such.
  3. The lineage: two tables written by one operation are related in fact even where no column
     says so. Marked `ambient` — it is a real coupling and not a foreign key.

**A hand-maintained graph that drifts is worse than none**, because it reports confidently. This
replaces it with something that cannot drift without the schema drifting first.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "handoff"


def main() -> int:
    schema = json.loads((HANDOFF / "schema-reference.json").read_text(encoding="utf-8"))
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))

    cols: dict = schema.get("cols", {})
    storage: dict = schema.get("storage", {})
    # ,  and  are stores rather than tables.
    # **They appear in the lineage and are not relatable** — a foreign key into a cache is not a
    # thing, and counting them as orphans would understate the real coverage.
    tables = {t for t in (set(cols) | set(storage)) if "." in t and ":" not in t}

    rels: list[dict] = []
    seen: set = set()

    def add(frm: str, col: str, to: str, how: str, kind: str, required: str = "") -> None:
        key = (frm, col, to)
        # **Self-references are real edges.** `parent_location_id`, `failover_provider_id` and
        # `compound_on_tax_code_id` all point at their own table, and dropping them loses the
        # hierarchy they express.
        if key in seen or frm not in tables or to not in tables:
            return
        seen.add(key)
        rels.append({
            "frm": frm, "col": col, "to": to, "how": how,
            "cross": "yes" if frm.split(".")[0] != to.split(".")[0] else "",
            "required": required, "edgeKind": kind,
        })

    # 1. Declared references.
    #
    # **`referenceHow` is read, not just `references`.** The two derivers feed each other —
    # derive-schema annotates a column *from* this graph — so reading `references` alone promotes
    # last run's convention guess to this run's declaration. On 18 August that inflated declared
    # edges from 518 to 705 in one pass, and it would have kept climbing.
    #
    # **A number that grows because it was measured is the worst kind of drift**: it looks like
    # progress.
    for table, columns in cols.items():
        for c in columns:
            target = c.get("references")
            if not target:
                continue
            how = c.get("referenceHow") or "declared"
            if how not in ("declared", "convention", "lineage"):
                how = "declared"
            add(table, c["column"], target, how,
                "ambient" if how == "lineage" else "foreignKey",
                "yes" if c.get("required") else "")

    # 2. Convention. A `*_id` column whose stem names a real table, in this schema or a
    #    well-known one. Weaker than declared and marked so — a reader should be able to tell
    #    which edges were asserted and which were inferred from a naming habit.
    # **A stem may be a prefix of the table name as well as the whole of it.** `developer_id`
    # points at `control.developer_account` and `entitlement_id` at `access.entitlement`; matching
    # only the full name left 23 tables orphaned on 18 August, most of them added that day.
    #
    # Exact match wins over prefix, and a prefix that matches two tables is ambiguous and is
    # skipped — **guessing between `control.tenant` and `platform.tenant` would be worse than
    # leaving the column unlinked.**
    stems: dict[str, str] = {}
    prefixes: dict[str, list] = {}
    for t in tables:
        short = t.split(".", 1)[1]
        stems.setdefault(short, t)
        head = short.split("_")[0]
        prefixes.setdefault(head, []).append(t)
    suffixes: dict[str, list] = {}
    for t in tables:
        short = t.split(".", 1)[1]
        if "_" in short:
            suffixes.setdefault(short.split("_", 1)[1], []).append(t)
    for head, matches in prefixes.items():
        if len(matches) == 1 and head not in stems:
            stems[head] = matches[0]
    # And a suffix: `client_id` points at `control.api_client`. **Ambiguity is refused the same
    # way** — `template_id` matches four tables and stays unlinked, which is the correct answer:
    # a guess between `message_template` and `ticket_template` would be worse than a gap.
    for tail, matches in suffixes.items():
        if len(matches) == 1 and tail not in stems:
            stems[tail] = matches[0]
    #    **The stem is a suffix, not the whole column name.** Matching only the bare stem missed
    #    61 real relationships on 18 August — every `created_by_principal_id`,
    #    `approved_by_principal_id` and `published_by_principal_id` failed, and so did every
    #    self-reference like `parent_location_id` and `failover_provider_id`.
    #
    #    Longest match wins, so `no_show_account_id` resolves to `ledger.account` rather than
    #    stopping at a shorter stem that happens to exist.
    for table, columns in cols.items():
        for c in columns:
            name = c["column"]
            if not name.endswith("_id") or c.get("references"):
                continue
            parts = name[:-3].split("_")
            target = next((stems["_".join(parts[i:])] for i in range(len(parts))
                           if "_".join(parts[i:]) in stems), None)
            if target:
                add(table, name, target, "convention", "foreignKey")

    # 3. Ambient coupling from the lineage. Two tables written by one operation are related in
    #    fact — an order and its lines, a shift and its deposit box — even where the column-level
    #    reference is absent because one side holds no id.
    #
    #    **Capped per operation.** An operation writing eight tables would otherwise produce
    #    twenty-eight edges and drown the declared ones.
    for oid, v in lineage.items():
        writes = [t for t in v.get("writes", []) if t in tables]
        if len(writes) < 2 or len(writes) > 4:
            continue
        anchor = writes[0]
        for other in writes[1:]:
            add(anchor, f"via {oid}", other, "lineage", "ambient")

    tab_ops: dict[str, list[str]] = {}
    for oid, v in lineage.items():
        for t in set(v.get("reads", [])) | set(v.get("writes", [])):
            if t in tables:
                tab_ops.setdefault(t, []).append(oid)

    tab_screens: dict[str, list[str]] = {}
    idx_path = HANDOFF / "screen-index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        for sid, s in idx.items():
            for t in set(s.get("reads", [])) | set(s.get("writes", [])):
                if t in tables:
                    tab_screens.setdefault(t, []).append(sid)

    linked = {r["frm"] for r in rels} | {r["to"] for r in rels}
    out = {
        "generated": "2026-08-18",
        "note": ("Derived by tools/derive-relationships.py from schema-reference.json and "
                 "api-data-lineage.json. **Not hand-maintained** — the previous graph described "
                 "540 relationships across 192 tables while the package held 352, because it had "
                 "not been touched since the schema grew past it."),
        "rels": rels,
        "tab_ops": tab_ops,
        "tab_screens": tab_screens,
    }
    (HANDOFF / "relationship-graph.json").write_text(json.dumps(out, indent=1), encoding="utf-8")

    by_kind: dict[str, int] = {}
    for r in rels:
        by_kind[r["how"]] = by_kind.get(r["how"], 0) + 1
    print(f"  {len(rels)} relationships · {', '.join(f'{v} {k}' for k, v in sorted(by_kind.items()))}")
    print(f"  {len(linked & tables)} of {len(tables)} tables linked")
    orphans = sorted(tables - linked)
    if orphans:
        print(f"  {len(orphans)} with no relationship: {', '.join(orphans[:6])}"
              + (" …" if len(orphans) > 6 else ""))
    print("  → handoff/relationship-graph.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
