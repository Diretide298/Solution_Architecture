"""Split candidates.jsonl into adjudication chunks, grouped so each agent sees
related subject matter together."""
import json, io, os, sys, collections, math

BLIND = sys.argv[1]
TARGET = int(sys.argv[2]) if len(sys.argv) > 2 else 220

rows = [json.loads(l) for l in io.open(os.path.join(BLIND, "candidates.jsonl"), encoding="utf-8") if l.strip()]

# Board/dashboard bearing only. The rest are carried into the workbook marked
# "Not assessed" rather than silently dropped - they are real requirements, they
# are simply not what this comparison is about.
rows = [r for r in rows if r["bd_scope"] in ("Direct", "Indirect")]

# trim candidate text so a chunk stays comfortably readable
for r in rows:
    r["candidates"] = r["candidates"][:4]
    for c in r["candidates"]:
        c["text"] = c["text"][:260]

# order by source pack then module: keeps a chunk thematically coherent
rows.sort(key=lambda r: (r["source_file"], r["module"], r["uid"]))

nchunks = max(1, math.ceil(len(rows) / TARGET))
per = math.ceil(len(rows) / nchunks)
d = os.path.join(BLIND, "chunks")
os.makedirs(d, exist_ok=True)
for old in os.listdir(d):
    os.remove(os.path.join(d, old))

manifest = []
for i in range(nchunks):
    part = rows[i*per:(i+1)*per]
    if not part: continue
    p = os.path.join(d, f"chunk{i+1:02d}.jsonl")
    with io.open(p, "w", encoding="utf-8") as fh:
        for r in part:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    srcs = collections.Counter(r["source_file"] for r in part)
    manifest.append((os.path.basename(p), len(part), ", ".join(f"{k}({v})" for k, v in srcs.most_common(4))))
    print(f"{os.path.basename(p)}  {len(part):4} rows  | {manifest[-1][2]}")
print(f"\n{len(rows)} rows -> {nchunks} chunks in {d}")
