"""Merge the blind extraction outputs into one normalised table."""
import json, glob, io, os, sys, collections, re

BLIND = sys.argv[1]
OUT = os.path.join(BLIND, "extracted.jsonl")

FIELDS = ["req_id","source_file","meeting_date","source_section","requirement",
          "evidence_quote","category","bd_scope","surface","persona","module",
          "decision_status","confidence"]

CAT = {"board","dashboard","report","kpi/metric","chart/visualisation","filter/drill-down",
       "alert/notification","export","access/permission","data/model","workflow/process",
       "integration","configuration","non-functional","open question"}
SCOPE = {"direct","indirect","not"}

def norm_scope(v):
    v = (v or "").strip().lower()
    if v.startswith("dir"): return "Direct"
    if v.startswith("ind"): return "Indirect"
    return "Not"

def norm_cat(v):
    v = (v or "").strip()
    return v if v else "Unclassified"

rows, problems = [], []
# only the canonical per-group files: g<n>.jsonl. Agents leave part/merge scratch
# files behind in the same directory and those must not be counted twice.
files = [p for p in glob.glob(os.path.join(BLIND, "out", "*.jsonl"))
         if re.fullmatch(r"g\d+\.jsonl", os.path.basename(p))]
files.sort(key=lambda p: int(re.search(r"g(\d+)", os.path.basename(p)).group(1)))
print("group files:", [os.path.basename(p) for p in files])
print()
for f in files:
    grp = os.path.splitext(os.path.basename(f))[0].upper()
    n_ok = n_bad = 0
    for ln, line in enumerate(io.open(f, encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        try:
            d = json.loads(line)
        except Exception as e:
            n_bad += 1; problems.append(f"{grp}:{ln} unparseable ({e})"); continue
        if not isinstance(d, dict) or not d.get("requirement"):
            n_bad += 1; problems.append(f"{grp}:{ln} no requirement field"); continue
        r = {k: str(d.get(k, "") or "").strip() for k in FIELDS}
        r["group"] = grp
        r["bd_scope"] = norm_scope(r["bd_scope"])
        r["category"] = norm_cat(r["category"])
        if not r["req_id"]:
            r["req_id"] = f"{grp}-{ln:03d}"
        rows.append(r); n_ok += 1
    print(f"{grp:5} {n_ok:5} rows  ({n_bad} rejected)")

# global sequential id, dedupe on normalised requirement text within the same source file
seen = {}
dupes = 0
final = []
for r in rows:
    key = (r["source_file"].lower(), re.sub(r"[^a-z0-9 ]", "", r["requirement"].lower())[:160])
    if key in seen:
        dupes += 1; continue
    seen[key] = True
    r["uid"] = f"MOM-{len(final)+1:04d}"
    final.append(r)

with io.open(OUT, "w", encoding="utf-8") as fh:
    for r in final:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"\nTOTAL {len(final)} rows after dropping {dupes} exact in-file duplicates -> {OUT}")
print("\nby bd_scope:", dict(collections.Counter(r["bd_scope"] for r in final)))
print("\nby category:")
for k, v in collections.Counter(r["category"] for r in final).most_common():
    print(f"  {k[:34]:36} {v}")
print("\nby module (top 20):")
for k, v in collections.Counter(r["module"] for r in final).most_common(20):
    print(f"  {(k or '(blank)')[:34]:36} {v}")
if problems:
    print(f"\n{len(problems)} problems, first 15:")
    for p in problems[:15]: print("  ", p)
