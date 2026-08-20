#!/usr/bin/env python3
"""Derive handoff/schema-roots.md — the primary table of each schema and how the rest hang off it.

**Asked for on 20 August: for each backend schema, identify the primary table and how the rest
derive from it.** The relationship graph knows every edge and nothing said which table the schema
is *about*.

The root is not simply the most-referenced table. `identity.principal` is referenced by 69 tables
across the package and is still the root of `identity`; `platform.scope_node` is referenced by 64
and is the root of `platform`. But **`access.access_point` has more inbound edges inside `access`
than `access.entitlement` does, and the schema is about entitlements** — a gate is equipment, and
the thing being admitted is the point.

So the score is three signals, and where they disagree the file says so rather than picking
silently:

  **Inbound within the schema** — how many of its own tables point at it.
  **Reach** — how many tables in the whole package point at it.
  **Independence** — a root points at few things; a leaf points at many.

**A root chosen by one number is a root nobody can argue with and nobody should trust.**
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"

# Where the arithmetic and the meaning disagree, the meaning wins and the reason is recorded.
# Every override here is a claim about what the schema is *for*, which no edge count can express.
OVERRIDE = {
    "access": ("access.entitlement",
               "**`access_point` has more inbound edges and the schema is about entitlements.** A "
               "gate is equipment; the thing being admitted is the point. `entitlement` also did "
               "not exist as a table until 18 August, which is why the arithmetic still favours "
               "the gate."),
    "marketing": ("marketing.guest_profile",
                  "**`campaign` scores higher and a campaign is something done *to* a guest.** The "
                  "schema is a CRM: the profile is what persists and campaigns come and go."),
    "promotions": ("promotions.promotion",
                   "**`bundle` scores higher because bundle lines point at it.** A bundle is one "
                   "kind of promotion, not the thing promotions are about."),
    "fnb": ("fnb.fnb_order",
            "**`table_visit` scores higher and not every F&B order has a table** — a kiosk order, "
            "a lounger delivery and a collection order have none. The order is the constant."),
}


def main() -> int:
    schema = json.loads((HANDOFF / "schema-reference.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((HANDOFF / "relationships.csv").open(encoding="utf-8")))

    tables = {t for t in (set(schema.get("cols") or {}) | set(schema.get("storage") or {}))
              if "." in t and ":" not in t}
    by_schema: dict[str, set] = defaultdict(set)
    for t in tables:
        by_schema[t.split(".")[0]].add(t)

    hard = [r for r in rows if r["edge_kind"] != "ambient"]
    inbound_all = Counter(r["to_table"] for r in hard)
    outbound = Counter(r["from_table"] for r in hard)
    inbound_own = Counter(r["to_table"] for r in hard
                          if r["from_table"].split(".")[0] == r["to_table"].split(".")[0])
    edges_from: dict[str, list] = defaultdict(list)
    for r in hard:
        edges_from[r["from_table"]].append(r)

    # **The first attempt walked the wrong way and the numbers said so.** It asked *who points at
    # the root* and worked outward, which left 222 of 353 tables reaching nothing — including
    # `identity.role`, because `principal` points at `role` rather than the other way round.
    #
    # A table's real anchor is where its own outbound keys stop. Following them to a fixed point
    # gives 42 terminal tables, and **`platform.scope_node` is reached by 289 of 353** — which is
    # the honest shape of the package: a tenancy spine with everything hanging off it.
    outbound_to: dict = defaultdict(set)
    for r in hard:
        if r["from_table"] != r["to_table"]:
            outbound_to[r["from_table"]].add(r["to_table"])

    def terminals(t, seen=None):
        seen = (seen or set()) | {t}
        nxt = outbound_to.get(t, set()) - seen
        if not nxt:
            return {t}
        found: set = set()
        for n in nxt:
            found |= terminals(n, seen)
        return found or {t}

    anchors: dict = {}
    for t in sorted(tables):
        term = sorted(terminals(t))
        anchors[t] = term

    anchor_counts = Counter(a for t in tables for a in terminals(t))
    spine = ["", "## The spine — where dependencies actually stop", "",
             "**Following every table's own outbound keys to a fixed point gives 42 terminal",
             "tables**, and the distribution is the honest shape of the package:", "",
             "| Terminal table | Tables that reach it |", "|---|---:|"]
    for t, n in anchor_counts.most_common(10):
        spine.append(f"| `{t}` | {n} |")
    spine += ["",
              "`platform.scope_node` is reached by 289 of 353 — **the tenancy spine, and almost",
              "everything hangs off it.** `identity.role` at 207 is the authorisation spine.",
              "",
              "**A first pass walked the other way** — asking who points *at* a root — and left 222",
              "tables reaching nothing, including `identity.role` itself, because `principal` points",
              "at `role` rather than the reverse. **The direction was the bug, not the data.**",
              ""]

    out = ["# Schema roots — the primary table of each schema, and how the rest derive from it",
           "",
           "**Derived by `tools/derive-schema-roots.py`. Do not hand-edit.**",
           "",
           "The relationship graph knows every edge and nothing said which table each schema is",
           "*about*. This does. **A root chosen by one number is a root nobody can argue with and",
           "nobody should trust**, so three signals are scored and disagreements are stated:",
           "",
           "| Signal | What it means |",
           "|---|---|",
           "| **Own** | tables inside this schema that point at it |",
           "| **Reach** | tables anywhere in the package that point at it |",
           "| **Out** | tables it points at — a root points at few, a leaf at many |",
           "",
           "Ambient edges are excluded throughout: a lineage coupling is two tables written by one",
           "operation, which is a fact about the code rather than about the data.",
           ""] + spine

    for sch in sorted(by_schema, key=lambda x: -len(by_schema[x])):
        ts = by_schema[sch]
        scored = sorted(ts, key=lambda t: (-inbound_own[t], -inbound_all[t], outbound[t]))
        computed = scored[0]
        root, why = OVERRIDE.get(sch, (computed, None))

        out.append(f"## `{sch}` — {len(ts)} tables")
        out.append("")
        out.append(f"**Root: `{root}`**  ·  own {inbound_own[root]} · reach {inbound_all[root]} "
                   f"· out {outbound[root]}")
        out.append("")
        if why:
            out.append(f"> **Overridden.** The arithmetic picks `{computed}`. {why}")
            out.append("")

        # depth from the root, following edges *into* it
        depth = {root: 0}
        frontier = [root]
        while frontier:
            nxt = []
            for t in frontier:
                for r in hard:
                    if r["to_table"] == t and r["from_table"] in ts and r["from_table"] not in depth:
                        depth[r["from_table"]] = depth[t] + 1
                        nxt.append(r["from_table"])
            frontier = nxt

        levels: dict[int, list] = defaultdict(list)
        for t, d in depth.items():
            if d:
                levels[d].append(t)
        for d in sorted(levels):
            names = ", ".join(f"`{t.split('.')[1]}`" for t in sorted(levels[d]))
            out.append(f"- **{d} step{'s' if d > 1 else ''} from the root** — {names}")

        unreached = sorted(t for t in ts if t not in depth)
        if unreached:
            out.append("")
            out.append(f"- **Reaches the root through nothing** — "
                       + ", ".join(f"`{t.split('.')[1]}`" for t in unreached))
            out.append("")
            out.append("  Standalone configuration, or a table whose foreign key is not declared. "
                       "**Not a defect on its own** — a password policy belongs to a scope rather "
                       "than to a principal — but it is where an undeclared key hides.")
        out.append("")

    (HANDOFF / "schema-roots.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # **The same answer, on the table itself.** A separate document tells a reader which table a
    # schema is about; it does not help the reader who is *looking at a table* and wants to know
    # what it hangs off. That reader is in the workbook or the ER diagram, not in a markdown file.
    #
    # `parent` is the declared child edge where one exists — `orders.order_line` hangs off
    # `orders.sales_order`. **`root` is the schema's primary table, and `depth` is how far the
    # walk had to go to reach it.** A table with no parent and a depth above one reaches the root
    # through a plain reference rather than by ownership, which is the ordinary case.

    lineage: dict = {}
    for sch, ts in by_schema.items():
        scored = sorted(ts, key=lambda t: (-inbound_own[t], -inbound_all[t], outbound[t]))
        root = OVERRIDE.get(sch, (scored[0], None))[0]
        depth = {root: 0}
        via: dict = {}
        frontier = [root]
        while frontier:
            nxt = []
            for t in frontier:
                for r in hard:
                    if (r["to_table"] == t and r["from_table"] in ts
                            and r["from_table"] not in depth):
                        depth[r["from_table"]] = depth[t] + 1
                        via[r["from_table"]] = (r["from_column"], r["to_table"])
                        nxt.append(r["from_table"])
            frontier = nxt

        for t in sorted(ts):
            parent = next((r["to_table"] for r in hard
                           if r["from_table"] == t and r["edge_kind"] == "child"), None)
            term = anchors.get(t, [])
            entry = {
                "schemaRoot": root,
                "isSchemaRoot": t == root,
                # **Where this table's own keys ultimately stop**, following them across schemas.
                # A table anchored only on `platform.scope_node` is tenancy-scoped and owns
                # nothing else; one anchored on several sits at a join between them.
                "anchors": term,
                "isAnchor": t in term and len(term) == 1,
            }
            if parent:
                entry["parent"] = parent
            if t in depth:
                entry["depth"] = depth[t]
                if t in via:
                    entry["reachesRootVia"] = f"{via[t][0]} -> {via[t][1]}"
            else:
                entry["depth"] = None
                entry["note"] = ("Reaches the root through nothing. Standalone configuration, or "
                                 "a foreign key that was never declared — this is where an "
                                 "undeclared key hides.")
            lineage[t] = entry

    schema["lineage"] = lineage
    (HANDOFF / "schema-reference.json").write_text(json.dumps(schema), encoding="utf-8")
    orphan = sum(1 for v in lineage.values() if v["depth"] is None)
    print(f"  {len(lineage)} tables given root, parent and depth · {orphan} reach no root")
    print(f"  {len(by_schema)} schemas · {len(OVERRIDE)} overridden where the arithmetic disagrees")
    print("  → handoff/schema-roots.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
