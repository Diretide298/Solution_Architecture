"""Rebuild the rows whose matrix candidates were truncated, with full text.

The first adjudication pass trimmed each candidate's matrix text to 260 characters
to keep chunks readable. 213 matrix rows are longer than that - mostly the ones that
enumerate a list of required reports - and a row cut off mid-list reads as if it does
not contain the thing it actually contains further down. That biases a verdict
towards Partial or Absent.

This rebuilds only the affected rows, with the candidate text untruncated, so they
can be judged again on what the matrix really says.
"""
import json, io, os, sys, glob, math, collections

BLIND = sys.argv[1]
PER = int(sys.argv[2]) if len(sys.argv) > 2 else 215
MAXTEXT = 1600

load = lambda p: [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]

matrix = {m["req_id"]: m for m in load(os.path.join(BLIND, "matrix.jsonl"))}
full = lambda m: (m["requirement"] + (" || " + m["details"] if m["details"] else "")).strip()
long_ids = {k for k, m in matrix.items() if len(full(m)) > 260}

cand = {}
for f in sorted(glob.glob(os.path.join(BLIND, "chunks", "chunk*.jsonl"))):
    for r in load(f):
        cand[r["uid"]] = r

verd = {}
for f in glob.glob(os.path.join(BLIND, "verdicts", "chunk*.jsonl")):
    for r in load(f):
        if r.get("uid"):
            verd[r["uid"]] = r

targets = []
for uid, r in cand.items():
    v = verd.get(uid)
    if not v or v["verdict"] not in ("Partial", "Absent"):
        continue
    if not any(c["matrix_req_id"] in long_ids for c in r["candidates"]):
        continue
    out = dict(r)
    out["candidates"] = []
    for c in r["candidates"]:
        m = matrix.get(c["matrix_req_id"])
        c2 = dict(c)
        if m:
            c2["text"] = full(m)[:MAXTEXT]
            c2["was_truncated"] = len(full(m)) > 260
        out["candidates"].append(c2)
    out["previous_verdict"] = v["verdict"]
    out["previous_matrix_req_ids"] = v.get("matrix_req_ids", "")
    out["previous_rationale"] = v.get("rationale", "")
    targets.append(out)

targets.sort(key=lambda r: (r["source_file"], r["uid"]))

d = os.path.join(BLIND, "recheck")
os.makedirs(d, exist_ok=True)
for old in glob.glob(os.path.join(d, "*.jsonl")):
    os.remove(old)

n = max(1, math.ceil(len(targets) / PER))
per = math.ceil(len(targets) / n)
for i in range(n):
    part = targets[i * per:(i + 1) * per]
    if not part:
        continue
    p = os.path.join(d, "recheck%02d.jsonl" % (i + 1))
    with io.open(p, "w", encoding="utf-8") as fh:
        for r in part:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("%s  %4d rows" % (os.path.basename(p), len(part)))

print("\n%d rows to re-judge -> %d files in %s" % (len(targets), n, d))
print("previous verdicts:", dict(collections.Counter(r["previous_verdict"] for r in targets)))
