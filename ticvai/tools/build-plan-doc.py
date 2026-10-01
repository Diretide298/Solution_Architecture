# -*- coding: utf-8 -*-
"""The build plan as a Word document for the PM: "TICVAI - Build Plan.docx" (1 October 2026).

Reads handoff/build-plan.json (written by tools/build-plan-deck.py) and docs/active/team.json, so it is rerun after
the plan is: python tools/build-plan-deck.py && python tools/build-plan-doc.py. Writes handoff/TICVAI - Build Plan.docx.
The numbers come from the plan; the words around them are the decisions of 29 September to 1 October.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "handoff" / "build-plan.json"
OUT = ROOT / "handoff" / "TICVAI - Build Plan.docx"
NAVY = RGBColor(0x14, 0x21, 0x3D)
ACCENT = "F2A46B"
HEAD_FILL = "14213D"
ZEBRA = "F6F4EF"


def d(x, year=True):
    if not x:
        return ""
    if isinstance(x, str):
        x = dt.date.fromisoformat(x)
    return x.strftime("%d %b %Y" if year else "%d %b").lstrip("0")


def n(x):
    return f"{int(round(x)):,}"


def shade(cell, fill):
    tc = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), fill)
    tc.append(s)


def table(doc, head, rows, widths=None, size=9):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(str(h))
        r.bold = True
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(c, HEAD_FILL)
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run("" if v is None else str(v))
            r.font.size = Pt(size)
            if k % 2:
                shade(cells[i], ZEBRA)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return t


def para(doc, text, bold_lead=None, style=None):
    p = doc.add_paragraph(style=style)
    if bold_lead:
        p.add_run(bold_lead).bold = True
    p.add_run(text)
    return p


def bullet(doc, text, bold_lead=None):
    return para(doc, text, bold_lead, style="List Bullet")


def main():
    plan = json.load(io.open(PLAN, encoding="utf-8"))
    b = plan["basis"]
    blocks = {x["block"]: x for x in plan["blocks"]}
    a = blocks["A"]
    opt_a = next((o for o in b.get("blockAOptions") or [] if o["sprint"] == a["targetSprint"]),
                 {"overtimeHours": 0, "byPerson": {}})
    sprints = [s for s in plan["sprints"] if s["inPlan"]]
    plat_name = plan["platforms"]
    ai_after = b["overtimeHours"] - b["overtimeHoursDevelopers"]

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in ("Heading 1", "Heading 2", "Heading 3", "Title"):
        doc.styles[s].font.color.rgb = NAVY
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2)
        sec.top_margin = sec.bottom_margin = Cm(1.8)

    doc.add_paragraph("TICVAI build plan", style="Title")
    p = doc.add_paragraph()
    p.add_run(f"Two-week sprints, four blocks of complete app-modules, every block tested end to end. "
              f"Plan of 1 October 2026; generated {d(plan['generated'][:10]) if plan.get('generated') else d(dt.date.today())} "
              f"from the package (handoff/build-plan.json).").italic = True

    # ------------------------------------------------------------------ 1
    doc.add_heading("1. The plan on one page", level=1)
    bullet(doc, f" {d(plan['calendar']['start'])} to {d(b['planEnd'])}, in {len(sprints)} two-week sprints "
                f"(Sprint 1 is {d(sprints[0]['start'], False)} to {d(sprints[0]['end'])}).", "When:")
    bullet(doc, f" four blocks, A to D. Each block is a set of complete app-modules: a business module on one app "
                f"(for example Ticketing · Guest Web, Ticketing · Guest App, Ticketing · POS) with the back end it needs. "
                f"{n(b['appModules'])} app-modules in all.", "How it is cut:")
    bullet(doc, " every app-module has a module test by a peer who did not build it; every block ends with a three-day "
                "block test of the journeys it completes, then the client's acceptance.", "How it is tested:")
    bullet(doc, f" about {n(b['totalHours'])} hours: build {n(b['buildHours'])}, testing {n(b['testHours'])}, "
                f"AI engine {n(b['aiEngineHours'])}.", "Effort:")
    bullet(doc, f" Block A (the first release) ends Sprint {a['targetSprint']}, {d(a['targetEndsOn'])}, with about "
                f"{n(opt_a['overtimeHours'])} hours of overtime. Block D finishes by {d(b['planEnd'])} with about "
                f"{n(b['overtimeHoursDevelopers'])} developer overtime hours over the six months. The AI engine work past "
                f"{d(b['planEnd'])} is created as tasks and left unassigned for the AI developers joining.",
           "Decided 1 October:")
    table(doc, ["Block", "Sprints", "Ends (decided)", "At normal hours", "App-modules", "Screens", "Journeys tested end to end"],
          [[k, f"{x['firstSprint']}–{x['targetSprint']}", f"{d(x['targetEndsOn'])} (Sprint {x['targetSprint']})",
            f"{d(x['endsOn'])} (Sprint {x['endSprint']})", x["appModuleCount"], n(x["screens"]),
            f"{x['flowsClaimed']}" + (f" (+{x['flowsPartly']} partly)" if x["flowsPartly"] else "")]
           for k, x in blocks.items()], widths=[1.2, 1.6, 3.4, 3.4, 2, 1.6, 3])

    # ------------------------------------------------------------------ 2
    doc.add_heading("2. Why it is cut this way", level=1)
    para(doc, "The PM call of 1 October asked for three things, and the plan is built around them:")
    bullet(doc, " Sprints run two weeks, Monday to Friday of the following week, with UAE public holidays taken out "
                "(Eid dates to be confirmed).", "Two-week sprints.")
    bullet(doc, " The old plan finished whole services and then whole apps, so nothing could be tested end to end until "
                "late. Now a business module is split by the app it lands in, so Ticketing on the guest web is finished, "
                "with its back end, before Ticketing on the POS. A large one is cut into parts that finish in one to "
                "three sprints, so tickets close often.", "Module-wise completion per app.")
    bullet(doc, " The old Block B was too big to test as one. It is now three blocks (B, C, D); each ends on a sprint "
                "boundary with its app-modules complete.", "A step in between.")

    # ------------------------------------------------------------------ 3
    doc.add_heading("3. What each block delivers", level=1)
    for k, x in blocks.items():
        doc.add_heading(f"Block {k}" + (": the first release" if k == "A" else ""), level=2)
        apps = ", ".join(f"{p} ({c})" for p, c in sorted(x["platforms"].items(), key=lambda kv: -kv[1]))
        para(doc, f" {x['appModuleCount']} app-modules: {n(x['screens'])} screens, {n(x['ops'])} operations, "
                  f"{n(x['tables'])} tables; {n(x['hours'])} build hours and {n(x['testHours'])} test hours.", "Scope.")
        para(doc, f" {apps}.", "App-modules by app.")
        para(doc, f" {d(x['testFrom'])} to {d(x['testTo'])} at normal hours, by {' and '.join(x['testers'])}, led by "
                  f"{x['testLead']}." + (f" With the decided overtime the block, and its test, close by "
                                          f"{d(x['targetEndsOn'])}." if x['targetSprint'] != x['endSprint'] else ""),
             "Block test.")
        crit = [f for f in plan["flows"] if f["complete"] == k and f["criticality"] in ("revenue", "safety", "legal")]
        if crit:
            para(doc, " " + "; ".join(f"{f['id']} {f['name']}" for f in crit[:12])
                 + (f"; and {len(crit) - 12} more" if len(crit) > 12 else "") + ".",
                 "Business-critical journeys it completes.")

    # ------------------------------------------------------------------ 4
    doc.add_heading("4. Sprint calendar", level=1)
    hol = {dt.date.fromisoformat(k) for k in plan["calendar"]["holidays"]}

    def last_days(end, k=3):            # the block test: the last k working days of the sprint
        out, x = [], dt.date.fromisoformat(end)
        while len(out) < k:
            if x.weekday() < 5 and x not in hol:
                out.append(x)
            x -= dt.timedelta(days=1)
        return out[-1], out[0]

    test_in = {}
    for k, x in blocks.items():
        s_ = next(s for s in sprints if s["n"] == x["targetSprint"])
        f_, t_ = last_days(s_["end"])
        test_in.setdefault(x["targetSprint"], []).append(f"Block {k}: {d(f_, False)} – {d(t_, False)}")
    table(doc, ["Sprint", "Dates", "Blocks in progress", "Capacity (h)", "Planned (h)", "Block test (decided dates)"],
          [[s["n"], f"{d(s['start'], False)} – {d(s['end'])}", ", ".join(s["blocks"]), n(s["capacity"]),
            n(s["planned"]), "; ".join(test_in.get(s["n"], []))]
           for s in sprints], widths=[1.3, 4.2, 2.8, 2.2, 2.2, 3.5])
    para(doc, "Capacity and planned hours are at normal hours; the block test dates are the decided ones (Block A in "
              f"Sprint {a['targetSprint']}, Block D in Sprint {blocks['D']['targetSprint']}, with overtime). Holidays: " + "; ".join(
        f"{d(k)} {v}" for k, v in plan["calendar"]["holidays"].items()) + ". The task-by-task sprint plan is in "
         "\"TICVAI - Sprint Plan.xlsx\" (Sprints, Tasks by sprint, Blocks, People, App-modules, Flows).")

    # ------------------------------------------------------------------ 5
    doc.add_heading("5. How every block is tested", level=1)
    table(doc, ["Unit", "Done when", "Tested by"],
          [["Ticket", "Unit and contract tests pass; screen states reachable; reviewed and tested by a peer; merged and green",
            "Its maker, then a peer in the same stack (never the maker)"],
           ["App-module", "Every ticket done; every screen state, link, permission and error tested on the integration "
            "environment; offline behaviour tested with the network cut (POS, scanner, staff app); no severity 1 or 2 defect open",
            "The module test ticket, about 10% of the module's points, by a peer who did not build most of it"],
           ["Block", "Every app-module done; every journey the block completes passes end to end; load tests where it adds "
            "a purchase or admission path; client acceptance", "A back-end and front-end pair, rotating per block, led by Chinmay Parab"]],
          widths=[2.2, 10, 5])
    bullet(doc, " the package's 290 journeys (flows) each list their apps, operations and offline behaviour; a block "
                "claims a journey when everything it needs is built by that block, and its steps are the test case.",
           "Journeys as tests:")
    bullet(doc, " the last three working days of each block's final sprint. No new feature work starts in them; the "
                "rest of the team fixes what the test finds.", "Block test window:")
    bullet(doc, " unit (xUnit, Jest/Vitest), contract (Pact against the OpenAPI contracts), integration (real PostgreSQL "
                "from the migrations), module, journey, offline and load (k6).", "Test levels:")
    bullet(doc, " severity 1 (journey cannot complete) and 2 (completes wrongly) block a module or block; 3 and 4 go to "
                "the next sprint. A defect that is really a gap in the specification becomes a change request.", "Defects:")
    bullet(doc, f" module tests {n(b['moduleTestHours'])} h, block tests {n(b['blockTestHours'])} h. The full strategy "
                "is docs/active/block-test-strategy.md in the package.", "Effort:")

    # ------------------------------------------------------------------ 6
    doc.add_heading("6. The team and the load", level=1)
    table(doc, ["Name", "Role", "Block A work ends", "Last day at normal hours", "Hours past 2 Apr", "Overtime h/week"],
          [[p["name"], p["role"], d(p.get("blockAEnd")), d(p["lastDay"]), n(p["hoursAfterPlanEnd"]),
            p["overtimeHoursPerWeek"]] for p in plan["people"]], widths=[3.6, 4, 2.6, 2.8, 2, 2])
    para(doc, f"{b['notCounted']} Loads follow skill and experience, so they are uneven on purpose. From release r2 a "
              "ticket keeps its owner once it is in OpenProject; moving it is a deliberate rebalance.")

    # ------------------------------------------------------------------ 7
    doc.add_heading("7. Dates, overtime and the AI engine: decided 1 October", level=1)
    table(doc, ["Question", "Decision", "What it costs"],
          [["When Block A ends", f"Sprint {a['targetSprint']}, {d(a['targetEndsOn'])}",
            f"About {n(opt_a['overtimeHours'])} h of overtime: " + ", ".join(f"{k} {v}" for k, v in opt_a["byPerson"].items())
            + f". Without it Block A ends {d(a['endsOn'])}."],
           ["Block D past 2 April", f"Keep its scope; finish by {d(b['planEnd'])} with overtime",
            f"About {n(b['overtimeHoursDevelopers'])} developer hours over the six months (the People table), about 4 to 5 "
            f"hours a week each. At normal hours the developers finish {d(b['forecastFinish'])}."],
           ["AI engine (about 50 AI-engineer weeks against 35)",
            "Every AI engine task is created; those past 2 April are unassigned for the AI developers joining",
            f"About {n(ai_after)} h of AI engine work past 2 April. Two AI engineers alone finish it {d(b['aiFinish'])}."]],
          widths=[3.5, 6, 7.5])
    para(doc, "Other options considered for Block A: " + "; ".join(
        f"Sprint {o['sprint']} ({d(o['endsOn'])}) {n(o['overtimeHours'])} h" for o in b.get("blockAOptions") or []) + ".")

    # ------------------------------------------------------------------ 8
    doc.add_heading("8. Where the work is tracked", level=1)
    table(doc, ["In OpenProject", "Is", "Example"],
          [["Epic", "A block", "Block A: the first release"],
           ["Feature", "An app-module (or a part of one)", "Ticketing · POS"],
           ["Task", "One piece of build: an operation, a table, a screen, a module test", "A screen of the POS, its wire, build and test sub-tasks"],
           ["Version", "The sprint", "Sprint 1 … Sprint 13"]], widths=[3, 7, 7])
    bullet(doc, " Blocks A and B are ticketed task by task. Blocks C and D are ticketed as app-modules until they are "
                "planned in detail; their tasks are already planned (plan-tasks.csv) with the keys they will get.",
           "Ticketing depth:")
    bullet(doc, " OpenProject holds who, when, the state and the order. What to build is the package, served by ADAM "
                "at the release a developer pulled.", "Who holds what:")
    bullet(doc, f" {n(b['tasks'])} tasks in the plan, {n(b['ticketedTasks'])} ticketed now.", "Size:")

    # ------------------------------------------------------------------ 9
    doc.add_heading("9. How a change reaches the build", level=1)
    for lead, txt in [
        ("Request.", " Every change is a change request in ADAM: its source, who approved it, what it touches and its "
                     "effort. Changes from meeting minutes need sign-off first."),
        ("Check.", " The package is rebuilt and over 40 checks run before anything is merged. Table changes only add; "
                   "a breaking change needs approval."),
        ("Release.", " Releases go out on Tuesday and Friday. Requests confirmed by noon on Monday or Thursday make the "
                     "next one. Each release is tagged (r1, r2, …) and updates ADAM and OpenProject together."),
        ("Build.", " A developer works against the release they pulled and sees what changed since. Started work is "
                   "never rewritten; a change to it arrives as a comment or a child ticket.")]:
        bullet(doc, txt, lead)

    # ------------------------------------------------------------------ 10
    doc.add_heading("10. Risks and what we do about them", level=1)
    import importlib.util
    spec = importlib.util.spec_from_file_location("deck", ROOT / "tools" / "build-plan-deck.py")
    deck = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(deck)
    table(doc, ["Risk", "Signal", "Action"], [list(r) for r in deck.RISKS], widths=[4, 5.5, 7.5])

    # ------------------------------------------------------------------ appendix
    doc.add_heading("Appendix: packages", level=1)
    table(doc, ["Package", "What it is", "App-modules", "Hours", "Lead"],
          [[p["package"], p["why"], p.get("appModules") if not isinstance(p.get("appModules"), list) else len(p["appModules"]),
            n(p["hours"]), p.get("lead", "")] for p in plan["packages"]], widths=[3.5, 8, 2, 1.8, 3])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
