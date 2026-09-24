"""Candidate matching: every extracted requirement against every matrix requirement.

Lexical retrieval only. It proposes candidates; adjudication is done by agents that
read both texts. Nothing here decides coverage.
"""
import json, io, os, sys, re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

BLIND = sys.argv[1]
TOPN = 6

def load(p):
    return [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]

matrix = load(os.path.join(BLIND, "matrix.jsonl"))
extracted = load(os.path.join(BLIND, "extracted.jsonl"))

def mtext(d):
    return " ".join([d["domain"], d["subdomain"], d["requirement"], d["details"]])

def etext(d):
    return " ".join([d["module"], d["surface"], d["requirement"]])

STOP = "the system should be able to shall must provide support allow user users".split()

vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True,
                      stop_words=STOP, strip_accents="unicode", lowercase=True)
M = vec.fit_transform([mtext(d) for d in matrix])
E = vec.transform([etext(d) for d in extracted])

# cosine (tf-idf rows are l2-normalised by default)
sims = E @ M.T
sims = np.asarray(sims.todense())

out = []
for i, d in enumerate(extracted):
    idx = np.argsort(-sims[i])[:TOPN]
    cands = []
    for j in idx:
        s = float(sims[i, j])
        if s < 0.05:
            continue
        m = matrix[j]
        cands.append({"matrix_req_id": m["req_id"], "domain": m["domain"],
                      "subdomain": m["subdomain"], "row": m["row"],
                      "text": (m["requirement"] + (" || " + m["details"] if m["details"] else ""))[:600],
                      "score": round(s, 3)})
    out.append({"uid": d["uid"], "req_id": d["req_id"], "requirement": d["requirement"],
                "module": d["module"], "surface": d["surface"], "category": d["category"],
                "bd_scope": d["bd_scope"], "source_file": d["source_file"],
                "evidence_quote": d["evidence_quote"][:300], "candidates": cands})

dest = os.path.join(BLIND, "candidates.jsonl")
with io.open(dest, "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

top = np.array([c["candidates"][0]["score"] if c["candidates"] else 0.0 for c in out])
print(f"{len(out)} extracted x {len(matrix)} matrix rows -> {dest}")
print(f"top-1 score: mean {top.mean():.3f}  median {np.median(top):.3f}")
for th in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
    print(f"  top-1 >= {th:.1f}: {(top >= th).sum():5}  ({(top >= th).mean()*100:.1f}%)")
