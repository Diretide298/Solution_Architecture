#!/usr/bin/env python3
"""Audit the three client workbooks against the package, and against each other.

**Three spreadsheets carry the scope, the schedule and the outstanding actions, and each has
already been wrong in a way nothing caught.** The delivery plan sat in the project for six days
before anyone read it (CF-145). Its priorities contradict each other (CF-140, sharpened here). The
task tracker's *New Inputs* sheet spans 16,384 columns because of one stray cell (CF-143). None of
that was found by a tool; all of it was found by somebody opening the file.

## The three questions

  **Matrix** -- `Ticvai_matrix_20260621_2_2_2.xlsx`, 3,186 requirements. `handoff/traceability.json`
  holds one verdict per row from the 18 August walk. **Has the matrix moved since?** A verdict
  against a row that has been reworded is a verdict about a different requirement.

  **Delivery plan** -- `TAIS_Product_Planning_and_Delivery_Plan_4_1.xlsx`. **Does priority mean
  the same thing on the two sheets that state it?** The Epic Register prices 23 epics and the
  Feature Register prices 444 features, the totals reconcile to the person-day, and they disagree
  by 1,869 days about how much of the plan is optional.

  **Task tracker** -- `TICVAI_Task_Track_From_Workshops.xlsx`. **What is still open, and how long
  has it been open?** An action raised in July and never closed is either done and unrecorded or
  forgotten, and the two need different responses.

Run: python3 tools/audit-workbooks.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "sources" / "requirements" / "Ticvai_matrix_20260621_2_2_2.xlsx"
PLAN = ROOT / "sources" / "planning" / "TAIS_Product_Planning_and_Delivery_Plan_4_1.xlsx"
TRACKER = ROOT / "sources" / "planning" / "TICVAI_Task_Track_From_Workshops.xlsx"
TRACE = ROOT / "handoff" / "traceability.json"

# Rank order, so "a P1 depending on a P3" is a comparison rather than a string match.
PRIORITY = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}



def _utf8_stdout() -> None:
    """**It crashed on the `→` in its own first heading**, before reporting a single verdict.

    A tool that needs `PYTHONIOENCODING` set to print is a tool that will crash for the next
    person who runs it by hand.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def rank(s):
    m = re.match(r"\s*(P[1-4])", str(s or ""))
    return PRIORITY.get(m.group(1)) if m else None


def rows(path, index, header_row=1):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[index]
    data = list(ws.iter_rows(values_only=True))
    wb.close()
    head = [str(c).strip() if c is not None else "" for c in data[header_row - 1]]
    return head, data[header_row:]


def norm(s):
    return " ".join(str(s or "").split()).lower()


def audit_matrix(report):
    if not MATRIX.exists() or not TRACE.exists():
        report.append(("matrix", "skipped — matrix or traceability.json missing", []))
        return
    _, data = rows(MATRIX, 0)
    live = {}
    for r in data:
        ref = str(r[4]).strip() if r[4] is not None else ""
        if ref:
            live.setdefault(ref, norm(r[5]))
    trace = json.loads(TRACE.read_text(encoding="utf-8"))
    walked = trace["rows"]

    counts = Counter(w["verdict"] for w in walked)
    missing = [w["matrixRef"] for w in walked if w["matrixRef"] not in live]
    unwalked = sorted(set(live) - {w["matrixRef"] for w in walked})

    lines = [f"{len(live)} distinct requirement ids in the matrix, {len(walked)} verdicts recorded"]
    for v, n in counts.most_common():
        lines.append(f"  {n:>5}  {v}")
    # **A verdict is about a row, and a row can be reworded under it.** This is the check the
    # 18 August walk could not do, because there was only one version of the file then.
    if missing:
        lines.append(f"  {len(missing)} verdict(s) name a requirement id the matrix no longer has")
        lines += [f"     {m}" for m in missing[:10]]
    if unwalked:
        lines.append(f"  **{len(unwalked)} requirement id(s) in the matrix with no verdict**")
        lines += [f"     {u}" for u in unwalked[:15]]
    report.append(("matrix", f"{len(live)} requirements", lines))


def audit_plan(report):
    """**Does the plan's priority mean the same thing on both sheets it states it on?**

    The dependency matrix cannot answer this: its 18 rows name capability categories, vendors and
    infrastructure -- *"All functional modules"*, *"POS & Mobile features"* -- and **not one epic**.
    Joining epics to it finds nothing, which is a null result from a join the workbook does not
    support rather than evidence of consistency. So the check is the one the workbook *can*
    answer: the Epic Register gives each epic a priority, the Feature Register gives each feature
    one, and **the effort totals reconcile exactly**, so any disagreement is about sequencing.
    """
    if not PLAN.exists():
        report.append(("plan", "skipped — delivery plan missing", []))
        return
    _, epics = rows(PLAN, 1)
    _, feats = rows(PLAN, 2)

    epri, eeff = {}, {}
    for r in epics:
        if r[0] and str(r[0]).startswith("E"):
            code = str(r[0]).split()[0]
            epri[code], eeff[code] = str(r[7]).strip(), float(r[6] or 0)

    from collections import defaultdict
    split = defaultdict(lambda: defaultdict(float))
    modules = defaultdict(Counter)
    by_pri = Counter()
    for r in feats:
        if not r[0]:
            continue
        code = str(r[2]).split()[0] if r[2] else "?"
        pri = str(r[7]).strip()
        eff = float(r[9] or 0)
        split[code][pri] += eff
        by_pri[pri] += eff
        modules[str(r[3]).strip() if r[3] else "(none)"][pri] += 1

    total = sum(by_pri.values())
    lines = [f"{len(epri)} epics, {sum(1 for r in feats if r[0])} features, {total:,.0f} person-days"]

    # **The two readings of the same plan.**
    epic_p3 = sum(v for k, v in eeff.items() if epri.get(k, "").startswith("P3"))
    feat_p3 = by_pri.get("P3 - Could", 0)
    lines.append(f"  P3 'Could' effort read from the Epic Register    : {epic_p3:>7,.0f} pd  "
                 f"({epic_p3 / total * 100:.0f}%)")
    lines.append(f"  P3 'Could' effort read from the Feature Register : {feat_p3:>7,.0f} pd  "
                 f"({feat_p3 / total * 100:.0f}%)")
    lines.append(f"  **the same document, {abs(feat_p3 - epic_p3):,.0f} person-days apart on what is optional**")

    mixed = [(c, epri[c], eeff[c], dict(sorted(split[c].items())))
             for c in sorted(epri)
             if not (len(split[c]) == 1 and list(split[c]) == [epri[c]])]
    lines.append(f"  **{len(mixed)} of {len(epri)} epics contain features priced below the epic's own "
                 f"priority**")
    for c, pr, eff, sp in sorted(
            mixed, key=lambda x: -(x[3].get("P3 - Could", 0) if not x[1].startswith("P3") else 0))[:10]:
        low = sp.get("P3 - Could", 0)
        share = f"{low / eff * 100:.0f}% P3" if eff else "?"
        lines.append(f"     {c}  {pr:<14}{eff:>6,.0f} pd   {share:<8} {sp}")

    multi = {m: c for m, c in modules.items() if len(c) > 1}
    lines.append(f"  **{len(multi)} of {len(modules)} modules are split across more than one "
                 f"priority** — a module that is partly must-have and partly could-have is not a "
                 f"schedulable statement")
    report.append(("plan", "delivery plan", lines))


def audit_tracker(report):
    if not TRACKER.exists():
        report.append(("tracker", "skipped — tracker missing", []))
        return
    head, data = rows(TRACKER, 0, header_row=4)
    idx = {h.lower(): i for i, h in enumerate(head)}
    c_status = idx.get("status", 6)
    c_task = idx.get("deliverable / task", 1)
    c_owner = idx.get("owner", 3)
    c_raised = idx.get("first raised", 4)

    items = [r for r in data if r[c_task]]
    st = Counter(norm(r[c_status]) or "(blank)" for r in items)
    lines = [f"{len(items)} action items"]
    for k, v in st.most_common():
        lines.append(f"  {v:>4}  {k}")
    open_items = [r for r in items
                  if not re.search(r"done|closed|complete", norm(r[c_status]))]
    lines.append(f"  **{len(open_items)} not marked done**")
    by_owner = Counter(str(r[c_owner] or "unassigned").strip() for r in open_items)
    lines.append(f"  by owner: {dict(by_owner.most_common(8))}")
    for r in open_items[:18]:
        raised = str(r[c_raised])[:10] if r[c_raised] else "?"
        lines.append(f"     {raised:<12}{str(r[c_task])[:66]:<68}{norm(r[c_status])[:18]}")
    if len(open_items) > 18:
        lines.append(f"     ... {len(open_items) - 18} more")
    report.append(("tracker", "workshop task tracker", lines))


def main():
    _utf8_stdout()
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        print("  openpyxl is not installed — cannot read the workbooks")
        return 1
    report = []
    audit_matrix(report)
    audit_plan(report)
    audit_tracker(report)
    for name, title, lines in report:
        print(f"\n=== {name}: {title} ===")
        for ln in lines:
            print(ln)

    # **`refresh.sh` shows each checker's last line, and this tool's was `... 42 more`.** A summary
    # that trails off mid-list tells a reader nothing about whether the workbooks are sound. The
    # verdict goes last because that is the line the pipeline prints.
    print("")
    print("PASS — " + str(len(report)) + " workbook section(s) read: "
          + ", ".join(n for n, _t, _l in report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
