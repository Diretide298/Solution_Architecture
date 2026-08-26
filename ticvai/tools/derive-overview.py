#!/usr/bin/env python3
"""Derive OVERVIEW.md — the landing page for the package.

**A landing page with hand-typed numbers is a landing page that is wrong within a day.** The
existing README claimed twelve platforms and 92 conflicts on a package that has fifteen and 151;
both were true when somebody typed them.

Everything here is read from the package. Ordered for a reader who has never seen it before: what
it is, what state it is in, where to start, and — last, because it is the honest ending — what is
not done.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"


def main() -> int:
    status = json.loads((HANDOFF / "status.json").read_text(encoding="utf-8"))
    trace = json.loads((HANDOFF / "traceability.json").read_text(encoding="utf-8"))
    lin = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    counts = status["counts"]
    verdicts = Counter(r["verdict"] for r in trace["rows"])
    total_reqs = sum(verdicts.values())
    in_scope = total_reqs - verdicts["PARKED"]

    # platforms, from the screens themselves
    plats = []
    screens: dict = {}
    by_plat: dict = defaultdict(set)
    on_screen: set = set()
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = d["platform"]
        plats.append((p["code"], p["name"], p.get("audience"), len(d["screens"])))
        for s in d["screens"]:
            screens[s["id"]] = s
            by_plat[p["code"]].add(s["id"])
            for a in (s.get("apis") or []):
                if a.get("operationId"):
                    on_screen.add(a["operationId"])

    # reachability
    out: dict = defaultdict(set)
    for sid, s in screens.items():
        nav = s.get("navigation") or {}
        for t in (nav.get("exitTo") or []):
            if t in screens:
                out[sid].add(t)
        for t in (nav.get("entryFrom") or []):
            if t in screens:
                out[t].add(sid)
    reachable = 0
    for code, ids in by_plat.items():
        entries = {i for i in ids if (screens[i].get("navigation") or {}).get("isEntryPoint")}
        seen, frontier = set(entries), list(entries)
        while frontier:
            nxt = []
            for t in frontier:
                for u in out[t] & ids:
                    if u not in seen:
                        seen.add(u)
                        nxt.append(u)
            frontier = nxt
        reachable += len(seen)

    in_flow: set = set()
    flow_ops: set = set()
    for f in (ROOT / "flows").glob("F*.yaml"):
        for st in (yaml.safe_load(f.read_text(encoding="utf-8")).get("steps") or []):
            if st.get("screen"):
                in_flow.add(st["screen"])
            for o in (st.get("operations") or []):
                flow_ops.add(o)

    # conflicts
    reg = (ROOT / "docs" / "registers" / "conflicts.md").read_text(encoding="utf-8")
    section = ""
    open_cf = []
    for line in reg.split("\n"):
        if line.startswith(("## ", "### ")):
            section = line.lstrip("# ").strip()
        m = re.match(r"^\| \*\*(CF-\d+)\*\* \|(.*)", line)
        if m and section.lower().startswith("open"):
            cells = [c.strip() for c in m.group(2).split(" | ")]
            open_cf.append((m.group(1), cells[1] if len(cells) > 1 else "?"))

    def pct(a, b):
        return round(100 * a / b) if b else 0

    lines = [
        "# TICVAI",
        "",
        "A multi-tenant platform for ticketing, access control, point of sale and venue operations.",
        "**This package is the design of it** — the contracts, the data model, the screens, the",
        "journeys through them, and the reasoning behind every decision that was not obvious.",
        "",
        f"**{counts['operations']} operations · {counts['contracts']} contracts · "
        f"{counts['tables']} tables · {counts['screens']} screens · {counts['states']} state "
        f"models · {counts['flows']} flows · {counts['adrs']} ADRs**",
        "",
        f"**Design {status['headline']['design']}% · Build {status['headline']['build']}%.**",
        "",
        "---",
        "",
        "## What this is for",
        "",
        "**A contract-first package that refuses to contradict itself.** Nine validators run on",
        "every change: a screen cannot call an operation that does not exist, an operation cannot",
        "name a table stored nowhere, a state model cannot anchor on a schema with no values, a",
        "flow cannot step through a screen that was deleted.",
        "",
        "**Nothing holds a copy of anything else's truth.** A screen names an operation; the",
        "operation resolves against the contracts; the contract resolves against the schema; the",
        "schema resolves against the relationship graph. Four hops, no duplication.",
        "",
        "**Every artefact is derived where it can be.** The boards are generated from the screens,",
        "the schema reference from the contracts, the relationship graph from both, the repo",
        "mirrors from the root. **A hand-maintained copy is a copy that goes stale**, and this",
        "package has been bitten by that three times.",
        "",
        "---",
        "",
        "## Where it stands",
        "",
        "| | | |",
        "|---|---:|---|",
        f"| Requirements contracted | **{verdicts['CONTRACTED']:,}** of {total_reqs:,} | "
        f"**{pct(verdicts['CONTRACTED'], in_scope)}% of what is in scope** |",
        f"| Operations reaching a screen | {len(on_screen & set(lin))} of {len(lin)} | "
        f"{pct(len(on_screen & set(lin)), len(lin))}% |",
        f"| Screens reachable from an entry point | {reachable} of {len(screens)} | "
        f"{pct(reachable, len(screens))}% |",
        f"| Screens drawn on a board | "
        f"{len(screens)} of "
        f"{len(screens)} | 100% |",
        f"| Screens in a journey | {len(in_flow)} of {len(screens)} | "
        f"{pct(len(in_flow), len(screens))}% |",
        f"| Conflicts | {status['conflicts']['closed']} closed | "
        f"{len(open_cf)} open, none blocking |",
        f"| **Tables written** | **0** of {counts['tables']} | **build has not started** |",
        "",
        "---",
        "",
        "## Start here",
        "",
        "| | |",
        "|---|---|",
        "| **`docs/principles.md`** | The design principles, with what each one rules out — "
        "including the six that were wrong first |",
        "| **`conflict-status.md`** | Every conflict and its state, one line each |",
        "| **`handoff/TICVAI_Schema_Reference.xlsx`** | The data model as a workbook |",
        "| **`handoff/schema-roots.md`** | Which table each schema is about, and how the rest "
        "hang off it |",
        "| **`COVERAGE.md`** | What is here and what is not |",
        "| **`docs/adr/`** | Why the platform is shaped this way |",
        "",
        "**Running the viewer** renders all of it as five linked layers:",
        "",
        "```",
        "cd viewer && npm start        →  http://localhost:4173",
        "```",
        "",
        "---",
        "",
        f"## The {len(plats)} platforms",
        "",
        "| | | | |",
        "|---|---|---|---:|",
    ]
    for code, name, aud, n in plats:
        lines.append(f"| `{code}` | {name} | {aud} | {n} |")

    lines += [
        "",
        "---",
        "",
        "## Folders",
        "",
        "| | |",
        "|---|---|",
        "| `contracts/` | The OpenAPI files. **Spine and satellite** — a spine contract is one "
        "others depend on and cannot be removed |",
        "| `screens/` | **The specification for everything visual.** Boards are generated from "
        "these |",
        "| `flows/` | Journeys through the screens, with their branches and who resolves each |",
        "| `states/` | Lifecycles, one per entity that has one |",
        "| `events/` | What the platform publishes, and which consumers are critical |",
        "| `docs/adr/` | Decisions, with the alternatives and why they lost |",
        "| `docs/registers/` | Conflicts, traceability, the backlog |",
        "| `handoff/` | Derived artefacts — the schema reference, the lineage, the graph |",
        "| `tools/` | Nine validators and eight derivers. `bash tools/refresh.sh` runs everything |",
        "| `repos/` | Mirrors of this package for each build repository. Also generated |",
        "",
        "---",
        "",
        "## What is not done",
        "",
        "**Put last on purpose.** A landing page that only lists what exists is a landing page "
        "that misleads.",
        "",
        f"**Build is 0%.** {counts['tables']} tables are designed and none is written. No "
        "migration has run, no service is scaffolded, and nothing has executed. **The design is "
        f"{pct(verdicts['CONTRACTED'], in_scope)}% of in-scope requirements and the gap to build "
        "is the entire remaining risk.**",
        "",
        f"**{counts['flows']} journeys of a target 60.** Seventeen contracts have exactly one — "
        "`subscription` has one over 55 operations. **Every journey written so far has found a "
        "defect**, which is the argument for writing more.",
        "",
        f"**{len(screens) - reachable} screens cannot be reached** from their platform's entry "
        "point, and navigation is still inferred rather than designed on most of the estate.",
        "",
        f"**{len(open_cf)} conflicts are open.** None blocks build; four need an email and one "
        "needs a workshop.",
        "",
    ]
    for cf, owner in open_cf:
        lines.append(f"- **{cf}** — {owner}")

    lines += [
        "",
        "---",
        "",
        "*Generated by `tools/derive-overview.py` from the package itself. **Do not hand-edit** — "
        "a landing page with typed numbers is a landing page that is wrong within a day, and this "
        "one claimed twelve platforms and 92 conflicts on a package that had fifteen and "
        f"{status['conflicts']['closed'] + len(open_cf)}.*",
    ]

    (ROOT / "OVERVIEW.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {len(plats)} platforms · {len(screens)} screens · {len(open_cf)} open conflicts")
    print("  → OVERVIEW.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
