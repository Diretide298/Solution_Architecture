"""Merge blind and sighted verdicts into the final answer.

Two passes ran. The blind pass judged all 7,019 board-bearing rows against five
lexically retrieved matrix candidates. The sighted pass then re-judged every row the
blind pass called Absent or High severity, with the whole matrix and the repository
open.

Where both exist, the sighted verdict wins: it saw 3,184 matrix rows instead of five.

The rows the sighted pass never revisited - those the blind pass scored Covered, or
Partial at Medium or Low - keep their blind verdict. That matters for how the totals
are read, and is recorded per row in `verdict_source` so nobody has to guess.
"""
import json, io, os, sys, glob, re, collections

B = sys.argv[1]
S = os.path.join(os.path.dirname(B), "sighted")
load = lambda p: [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]

blind = {}
for f in glob.glob(os.path.join(B, "verdicts", "chunk*.jsonl")):
    if re.fullmatch(r"chunk\d+\.jsonl", os.path.basename(f)):
        for r in load(f):
            if r.get("uid"):
                r["verdict_source"] = "blind adjudication"
                blind[r["uid"]] = r
n_rej = 0
for f in glob.glob(os.path.join(B, "verdicts_recheck", "recheck*.jsonl")):
    if re.fullmatch(r"recheck\d+\.jsonl", os.path.basename(f)):
        for r in load(f):
            if r.get("uid"):
                r["verdict_source"] = "blind, re-judged on full matrix text"
                blind[r["uid"]] = r
                n_rej += 1

final = dict(blind)
n_sighted = 0
for f in sorted(glob.glob(os.path.join(S, "out", "sighted*.jsonl"))):
    for r in load(f):
        uid = r.get("uid")
        if not uid:
            continue
        prev = blind.get(uid, {})
        out = {
            "uid": uid,
            "verdict": r.get("verdict", ""),
            "matrix_req_ids": r.get("matrix_req_ids", ""),
            "matrix_domain": prev.get("matrix_domain", ""),
            "rationale": r.get("rationale", ""),
            "gap_severity": r.get("gap_severity", ""),
            "adjudicator_note": prev.get("adjudicator_note", ""),
            "evidence": r.get("evidence", ""),
            "where_else": r.get("where_else", ""),
            "searched": r.get("searched", ""),
            "blind_verdict": r.get("blind_verdict", prev.get("verdict", "")),
            "verdict_source": "sighted re-check, full matrix and repository",
        }
        final[uid] = out
        n_sighted += 1

dest = os.path.join(B, "verdicts-final.jsonl")
with io.open(dest, "w", encoding="utf-8") as fh:
    for uid in sorted(final):
        fh.write(json.dumps(final[uid], ensure_ascii=False) + "\n")

v = collections.Counter(r["verdict"] for r in final.values())
src = collections.Counter(r["verdict_source"] for r in final.values())
sev = collections.Counter(r.get("gap_severity") for r in final.values()
                          if r["verdict"] in ("Partial", "Absent"))
print("final verdicts written: %d -> %s" % (len(final), dest))
print("  %d re-judged for truncation, %d replaced by the sighted re-check" % (n_rej, n_sighted))
print("\nverdict source:")
for k, c in src.most_common():
    print("  %-46s %5d" % (k, c))
scored = sum(v[k] for k in ("Covered", "Partial", "Absent"))
print("\nFINAL VERDICTS (%d scored):" % scored)
for k in ("Covered", "Partial", "Absent", "Not a requirement"):
    if v[k]:
        pct = (" (%.1f%% of scored)" % (100.0 * v[k] / scored)) if k != "Not a requirement" else ""
        print("  %-20s %5d%s" % (k, v[k], pct))
print("\ngap severity:", dict(sev))
print("\nrows carrying a repo path (built, but not obliged by the matrix):",
      sum(1 for r in final.values() if r.get("where_else")))
