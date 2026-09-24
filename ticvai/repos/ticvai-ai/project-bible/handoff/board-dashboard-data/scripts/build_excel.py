"""Build the single deliverable workbook: requirements, specs, matrix verdicts, gaps."""
import json, io, os, sys, glob, re, collections, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BLIND = sys.argv[1]
DEST = sys.argv[2]


def load(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]


extracted = load(os.path.join(BLIND, "extracted.jsonl"))
matrix = load(os.path.join(BLIND, "matrix.jsonl"))
verdicts = {}
# Only the canonical chunk files - adjudicators leave namespaced part files behind.
for f in glob.glob(os.path.join(BLIND, "verdicts", "chunk*.jsonl")):
    if not re.fullmatch(r"chunk\d+\.jsonl", os.path.basename(f)):
        continue
    for r in load(f):
        if r.get("uid"):
            verdicts[r["uid"]] = r

# The re-judgement pass saw the full matrix text where the first pass saw it truncated,
# so where the two disagree the re-judgement wins.
rejudged = 0
for f in glob.glob(os.path.join(BLIND, "verdicts_recheck", "recheck*.jsonl")):
    if not re.fullmatch(r"recheck\d+\.jsonl", os.path.basename(f)):
        continue
    for r in load(f):
        if r.get("uid"):
            r["_rejudged"] = True
            verdicts[r["uid"]] = r
            rejudged += 1
print("verdicts loaded: %d (%d re-judged against untruncated matrix text)"
      % (len(verdicts), rejudged))

NAVY = "1F3864"
HEAD = PatternFill("solid", fgColor=NAVY)
HFONT = Font(color="FFFFFF", bold=True, size=10)
WRAP = Alignment(wrap_text=True, vertical="top")
TOP = Alignment(vertical="top")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FILL = {
    "Covered": PatternFill("solid", fgColor="E2EFDA"),
    "Partial": PatternFill("solid", fgColor="FFF2CC"),
    "Absent": PatternFill("solid", fgColor="FCE4E4"),
    "Not a requirement": PatternFill("solid", fgColor="F2F2F2"),
    "High": PatternFill("solid", fgColor="F8CBAD"),
    "Medium": PatternFill("solid", fgColor="FFE699"),
    "Low": PatternFill("solid", fgColor="E2EFDA"),
}


def sheet(wb, title, headers, rows, widths, wrapcols=(), fillcol=None):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = HEAD
        cell.font = HFONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    maxr, maxc = ws.max_row, len(headers)
    for row in ws.iter_rows(min_row=2, max_row=maxr, max_col=maxc):
        for cell in row:
            cell.alignment = WRAP if cell.column in wrapcols else TOP
            cell.border = BORDER
            cell.font = Font(size=10)
    if fillcol:
        for r in range(2, maxr + 1):
            key = ws.cell(row=r, column=fillcol).value
            if key in FILL:
                ws.cell(row=r, column=fillcol).fill = FILL[key]
    ws.freeze_panes = "A2"
    if maxr > 1:
        ws.auto_filter.ref = "A1:" + get_column_letter(maxc) + str(maxr)
    ws.sheet_view.showGridLines = False
    return ws


wb = openpyxl.Workbook()
wb.remove(wb.active)

MOM_GROUPS = {"G1", "G2", "G3", "G4", "G5", "G6"}


def src_type(g):
    if g in MOM_GROUPS:
        return "Meeting minutes"
    if g == "G7":
        return "Written dashboard spec"
    return "Board design pack"


# ---------- 1. Requirements ----------
HDRS = ["Req ID", "Source type", "Source document", "Section / page",
        "Requirement (specification)", "Evidence - verbatim from source", "Category",
        "Board/dashboard scope", "Surface", "Persona", "Module", "Status in source",
        "Confidence", "Matrix verdict", "Matrix requirement IDs", "Matrix domain",
        "Why / what is missing", "Gap severity", "Reviewer note", "Checked twice"]

NOT_ASSESSED = ("Not assessed - no board or dashboard bearing")

rows = []
for e in extracted:
    v = verdicts.get(e["uid"], {})
    verdict = v.get("verdict", "")
    if not verdict:
        verdict = NOT_ASSESSED if e["bd_scope"] == "Not" else ""
    rows.append([
        e["uid"], src_type(e["group"]), e["source_file"], e["source_section"],
        e["requirement"], e["evidence_quote"], e["category"], e["bd_scope"],
        e["surface"], e["persona"], e["module"], e["decision_status"], e["confidence"],
        verdict, v.get("matrix_req_ids", ""), v.get("matrix_domain", ""),
        v.get("rationale", ""), v.get("gap_severity", ""), v.get("adjudicator_note", ""),
        "Yes" if v.get("_rejudged") else "",
    ])
sheet(wb, "Requirements", HDRS, rows,
      [11, 18, 34, 30, 66, 60, 18, 14, 18, 16, 20, 14, 11, 16, 20, 22, 56, 12, 30, 12],
      wrapcols={5, 6, 17}, fillcol=14)

# ---------- 2. Gaps ----------
order = {"High": 0, "Medium": 1, "Low": 2, "": 3}
gaps = [r for r in rows if r[13] in ("Absent", "Partial")]
gaps.sort(key=lambda r: (order.get(r[17], 3), r[13] != "Absent", r[10]))
GH = ["Req ID", "Verdict", "Gap severity", "Module", "Board/dashboard scope",
      "Requirement (specification)", "What the matrix leaves out", "Nearest matrix IDs",
      "Source document", "Section / page", "Evidence"]
sheet(wb, "Gaps", GH,
      [[r[0], r[13], r[17], r[10], r[7], r[4], r[16], r[14], r[2], r[3], r[5]] for r in gaps],
      [11, 12, 12, 20, 14, 66, 56, 20, 32, 28, 54], wrapcols={6, 7, 11}, fillcol=3)

# ---------- 3. Matrix coverage (reverse view) ----------
hit = collections.Counter()
for uid, v in verdicts.items():
    for rid in [x.strip() for x in v.get("matrix_req_ids", "").split(",") if x.strip()]:
        hit[rid] += 1
MH = ["Matrix Req ID", "Domain", "Sub-domain", "Matrix requirement text",
      "Additional details", "Extracted requirements mapped here",
      "Evidenced by MoM / board pack?"]
mrows = [[m["req_id"], m["domain"], m["subdomain"], m["requirement"], m["details"],
          hit.get(m["req_id"], 0), "Yes" if hit.get(m["req_id"], 0) else "No"] for m in matrix]
sheet(wb, "Matrix coverage", MH, mrows, [14, 30, 30, 70, 50, 14, 14], wrapcols={4, 5})

# ---------- 4. Boards & screens inventory ----------
inv = []
for f in sorted(glob.glob(os.path.join(BLIND, "out", "*board-inventory*.txt"))):
    grp = os.path.basename(f).split("-")[0].upper()
    section = ""
    for line in io.open(f, encoding="utf-8"):
        line = line.rstrip()
        if not line or line.startswith("# "):
            continue
        if line.startswith("##"):
            section = line.lstrip("# ").strip()
            continue
        parts = [p.strip() for p in line.split("|")]
        inv.append([grp, section, parts[0],
                    parts[1] if len(parts) > 1 else "",
                    parts[2] if len(parts) > 2 else ""])
sheet(wb, "Boards and screens",
      ["Group", "Pack / section", "Board, dashboard or screen", "Source file", "Page"],
      inv, [9, 46, 52, 46, 14], wrapcols={3})

# ---------- 4a. The packs' own coverage claims, checked ----------
claims = load(os.path.join(BLIND, "claims.jsonl"))
if claims:
    sheet(wb, "Pack coverage claims",
          ["Board page", "Coverage claimed on the board header", "IDs cited",
           "IDs that exist in the matrix", "IDs cited that do not exist",
           "Confirmed by the blind read", "Claimed but not reached by the blind read",
           "Reached by the blind read but not claimed"],
          [[c["board"], c["claim"], c["cited"], c["real"], c["missing"],
            c["confirmed_by_blind_read"], c["claimed_not_found"], c["found_not_claimed"]]
           for c in claims],
          [18, 44, 10, 14, 20, 40, 40, 44], wrapcols={2, 6, 7, 8})

# ---------- 4b. Source defects found along the way ----------
inc = load(os.path.join(BLIND, "inconsistencies.jsonl"))
sheet(wb, "Source and matrix issues",
      ["ID", "Source document", "Where", "What was found", "Why it matters",
       "Raised by", "Suggested action"],
      [[d["id"], d["source"], d["where"], d["finding"], d["why_it_matters"],
        d["raised_by"], d["action"]] for d in inc],
      [9, 46, 30, 70, 62, 12, 54], wrapcols={4, 5, 7})

# ---------- 4c. Summary by module and by source ----------
def tally(keyfn, label):
    out = []
    keys = sorted({keyfn(r) for r in rows if keyfn(r)})
    for k in keys:
        sub = [r for r in rows if keyfn(r) == k]
        vc = collections.Counter(r[13] for r in sub)
        scored = sum(vc[v] for v in ("Covered", "Partial", "Absent"))
        hi = sum(1 for r in sub if r[17] == "High")
        pct = ("%.0f%%" % (100.0 * vc["Covered"] / scored)) if scored else "-"
        out.append([k, len(sub), vc["Covered"], vc["Partial"], vc["Absent"], pct, hi])
    out.sort(key=lambda r: -r[1])
    return out

SUMH = ["", "Requirements", "Covered", "Partial", "Absent",
        "Covered as a share of those assessed", "High-severity gaps"]

# The matrix read the other way round: of its own 3,184 rows, how many did anything
# in the minutes or the board packs actually land on? A row reached only by a Partial
# verdict is counted as Partial - something touches it, nothing fully evidences it.
strong, weak = collections.Counter(), collections.Counter()
for v in verdicts.values():
    for rid in [x.strip() for x in v.get("matrix_req_ids", "").split(",") if x.strip()]:
        if v.get("verdict") == "Covered":
            strong[rid] += 1
        elif v.get("verdict") == "Partial":
            weak[rid] += 1
m_cov = sum(1 for m in matrix if strong.get(m["req_id"]))
m_par = sum(1 for m in matrix if not strong.get(m["req_id"]) and weak.get(m["req_id"]))
m_non = len(matrix) - m_cov - m_par

srows = [["THE MATRIX, READ THE OTHER WAY", "", "", "", "", "", ""],
         ["Requirements matrix - its rows, against what the sources evidence",
          len(matrix), m_cov, m_par, m_non,
          "%.0f%%" % (100.0 * m_cov / len(matrix)), ""],
         ["   (Covered = a source requirement fully evidences this matrix row; "
          "Partial = something touches it; Absent = nothing in the minutes or packs reaches it)",
          "", "", "", "", "", ""],
         ["", "", "", "", "", "", ""],
         ["BY SOURCE TYPE", "", "", "", "", "", ""]] + tally(lambda r: r[1], "src")
srows += [["", "", "", "", "", "", ""], ["BY MODULE", "", "", "", "", "", ""]] + tally(lambda r: r[10], "mod")
sheet(wb, "Summary", SUMH, srows, [40, 14, 11, 11, 11, 16, 16])

# ---------- 5. Sources ----------
bysrc = collections.Counter(e["source_file"] for e in extracted)
bygrp = collections.defaultdict(set)
for e in extracted:
    bygrp[e["source_file"]].add(e["group"])
srows = [[s, src_type(sorted(bygrp[s])[0]), ", ".join(sorted(bygrp[s])), n]
         for s, n in bysrc.most_common()]
sheet(wb, "Sources",
      ["Source document", "Source type", "Extraction group", "Requirements extracted"],
      srows, [62, 24, 18, 22])

# ---------- 6. Read me ----------
ws = wb.create_sheet("Read me", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 112
vc = collections.Counter(r[13] for r in rows)
sc = collections.Counter(r[7] for r in rows)
gs = collections.Counter(r[17] for r in rows if r[13] in ("Absent", "Partial"))
lines = [
    ("TICVAI - board and dashboard requirements, checked against the matrix", ""),
    ("Generated", datetime.date.today().isoformat()),
    ("", ""),
    ("What this is", "Requirements read out of the meeting minutes and the board/dashboard "
                     "design packs, then checked one by one against the client requirements matrix."),
    ("How it was produced", "The extraction was run blind. The agents that read the minutes and "
                            "the board packs were given those documents and nothing else - no matrix, "
                            "no existing coverage note, no prior requirement list. They could not copy "
                            "an answer, so where this workbook agrees with the matrix, that agreement "
                            "is evidence rather than restatement."),
    ("Every row carries its source", "Each requirement quotes the verbatim sentence, table cell or "
                                     "on-screen label it came from, with the document and page or section."),
    ("", ""),
    ("Requirements extracted", len(rows)),
    ("  from meeting minutes", sum(1 for r in rows if r[1] == "Meeting minutes")),
    ("  from written dashboard specs", sum(1 for r in rows if r[1] == "Written dashboard spec")),
    ("  from board design packs", sum(1 for r in rows if r[1] == "Board design pack")),
    ("", ""),
    ("Board/dashboard bearing", "Direct %d  |  Indirect %d  |  None %d"
     % (sc.get("Direct", 0), sc.get("Indirect", 0), sc.get("Not", 0))),
    ("Matrix verdict", "  |  ".join("%s %d" % (k, v) for k, v in vc.most_common() if k)),
    ("Gap severity", "  |  ".join("%s %d" % (k, v) for k, v in gs.most_common() if k)),
    ("", ""),
    ("Matrix compared against", "%d functional requirements, Ticvai_matrix_20260621_2.xlsx" % len(matrix)),
    ("", ""),
    ("Covered", "The matrix already requires substantially the same thing."),
    ("Partial", "The matrix names the area but not the specific thing asked for - typically it "
                "says 'provide a dashboard' where the source specifies the tiles on it."),
    ("Absent", "Nothing in the matrix covers it."),
    ("", ""),
    ("Sheets", "Requirements - every extracted requirement with its verdict. "
               "Gaps - only Partial and Absent, worst first. "
               "Matrix coverage - the reverse view: every matrix row and whether anything in the "
               "minutes or packs evidences it. "
               "Boards and screens - the inventory of named surfaces. "
               "Sources - what was read."),
]
for k, v in lines:
    ws.append([k, v])
ws["A1"].font = Font(bold=True, size=14, color=NAVY)
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=2):
    if row[0].value:
        row[0].font = Font(bold=True, size=10, color=NAVY)
    row[0].alignment = TOP
    row[1].alignment = WRAP
    if isinstance(row[1].value, int):
        row[1].font = Font(bold=True, size=11)

wb.save(DEST)
print("saved:", DEST)
print("  Requirements %d | Gaps %d | Matrix rows %d | Boards %d"
      % (len(rows), len(gaps), len(mrows), len(inv)))
print("  verdicts present for", len(verdicts), "rows")
