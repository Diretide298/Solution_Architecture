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

# Windows consoles are cp1252 and this tool closes by printing a unicode arrow. **The write
# has already happened by then**, so the traceback reported a failure on a run that succeeded
# — the most misleading shape an error can take.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"


def render() -> tuple:
    """OVERVIEW.md's text, and the line main() prints; check-landing-figures LF-OVERVIEW compares the file with it."""
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
        # a redirect is reached when the screen its route goes to is (CHG-R14J-030, the r13 system review F-14)
        to = (s.get("implementation") or {}).get("redirect")
        if to in screens:
            out[to].add(sid)
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

    # **Authored journeys and board-derived routes are counted apart** (r13 system review F-13, CHG-R14J-041), as
    # build-status.py counts them: a route generated against every client board is scaffolding, not a journey, and
    # "98 flows" beside 291 flow files read as a contradiction. The target is the Flows metric's own total.
    in_flow: set = set()
    in_authored: set = set()
    flow_ops: set = set()
    n_derived = 0
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        text = f.read_text(encoding="utf-8")
        derived = "provenance: derived-from-board" in text
        n_derived += derived
        for st in (yaml.safe_load(text).get("steps") or []):
            if st.get("screen"):
                in_flow.add(st["screen"])
                if not derived:
                    in_authored.add(st["screen"])
            for o in (st.get("operations") or []):
                if not derived:
                    flow_ops.add(o)
    flows_metric = next((m for m in (status.get("metrics") or {}).get("design") or [] if m.get("name") == "Flows"), {})
    flows_target = flows_metric.get("total")
    by_contract: dict = defaultdict(set)
    for op, row in lin.items():
        by_contract[row.get("contract") or "?"].add(op)
    no_journey = sorted(c for c, ops in by_contract.items() if not ops & flow_ops)
    # The checks the gate runs, as tools/run-checks.py lists them, and how many of them gate.
    import importlib.util
    spec = importlib.util.spec_from_file_location("run_checks", str(ROOT / "tools" / "run-checks.py"))
    run_checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_checks)
    n_checks = len(run_checks.CHECKS)
    n_gating = len([c for c in run_checks.CHECKS if c not in run_checks.REPORT_ONLY])
    n_derivers = len(list((ROOT / "tools").glob("derive-*.py")))

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
        f"models · {counts['flows']} authored flows · {counts['adrs']} ADRs**",
        "",
        f"**Design {status['headline']['design']}% · Build {status['headline']['build']}%** (handoff/status.json).",
        "",
        "---",
        "",
        "## What this is for",
        "",
        f"**A contract-first package that refuses to contradict itself.** {n_checks} checks run on",
        f"every refresh, {n_gating} of them gating: a screen cannot call an operation that does not exist, an operation cannot",
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
        f"| Screens in an authored journey | {len(in_authored)} of {len(screens)} | "
        f"{pct(len(in_authored), len(screens))}% |",
        f"| Screens on any flow, board-derived routes included | {len(in_flow)} of {len(screens)} | "
        f"{pct(len(in_flow), len(screens))}% |",
        f"| Conflicts | {status['conflicts']['closed']} closed | "
        f"{len(open_cf)} open, {status['conflicts'].get('blocking', 0)} blocking |",
        f"| Tables in the DDL | {counts.get('tablesWritten', 0):,} of {counts['tables']:,} | "
        f"{pct(counts.get('tablesWritten', 0), counts['tables'])}% |",
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
        "| **`COVERAGE.md`** | The account of 17 August 2026 of what was here and what was not (historical) |",
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
        f"| `tools/` | {n_checks} checks (tools/run-checks.py) and {n_derivers} derivers. `bash tools/refresh.sh` runs everything |",
        "| `repos/` | Mirrors of this package for each build repository. Also generated |",
        "",
        "---",
        "",
        "## What is not done",
        "",
        "**Put last on purpose.** A landing page that only lists what exists is a landing page "
        "that misleads.",
        "",
        f"**Build is {status['headline']['build']}%** by the package's own measure (handoff/status.json). "
        f"**The design is {pct(verdicts['CONTRACTED'], in_scope)}% of in-scope requirements and the gap to build "
        "is the remaining risk.**",
        "",
        f"**{counts['flows']} authored journeys"
        + (f" of a target {flows_target}" if flows_target else "")
        + f"**, beside {n_derived} routes derived from the client boards. "
        f"{len(no_journey)} of {len(by_contract)} contracts have no operation in an authored journey"
        + (" (" + ", ".join(f"`{c}`" for c in no_journey) + ")" if no_journey else "")
        + ". **Every journey written so far has found a defect**, which is the argument for writing more.",
        "",
        f"**{len(screens) - reachable} screens cannot be reached** from their platform's entry "
        "point, and navigation is still inferred rather than designed on most of the estate.",
        "",
        f"**{len(open_cf)} conflicts are open**, {status['conflicts'].get('blocking', 0)} of them blocking. "
        "Each is listed with who answers it:",
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

    return ("\n".join(lines) + "\n",
            f"  {len(plats)} platforms · {len(screens)} screens · {len(open_cf)} open conflicts")


def main() -> int:
    text, said = render()
    # **Nothing rewrites this page after it is written** (CHG-R14J-041): sync-counts.py edited it in place with bare
    # "<n> screens" patterns and turned "2 screens cannot be reached" into "2453 screens cannot be reached".
    with open(ROOT / "OVERVIEW.md", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(said)
    print("  → OVERVIEW.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
