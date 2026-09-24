"""Check the board packs' own 'Matrix Coverage:' claims.

The Ticket Types pack prints a coverage claim on each board header. Those are
assertions about the client's matrix, so they can be checked two ways:

  1. Do the cited requirement IDs actually exist in the matrix?
  2. Does the blind read of that board land on the same matrix rows?

Neither check needs an opinion, which is what makes them worth printing.
"""
import json, io, os, sys, re, collections

BLIND = sys.argv[1]


def load(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]


matrix = load(os.path.join(BLIND, "matrix.jsonl"))
matrix_ids = {m["req_id"] for m in matrix if m["req_id"]}
extracted = load(os.path.join(BLIND, "extracted.jsonl"))

verdicts = {}
import glob
for f in glob.glob(os.path.join(BLIND, "verdicts", "chunk*.jsonl")):
    for r in load(f):
        if r.get("uid"):
            verdicts[r["uid"]] = r


def expand(claim):
    """'1.1.39, 1.1.41-49' -> ['1.1.39', '1.1.41', ... '1.1.49']"""
    out = []
    for part in claim.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+\.\d+)\.(\d+)\s*-\s*(\d+)$", part)
        if m:
            prefix, a, b = m.group(1), int(m.group(2)), int(m.group(3))
            if b >= a and b - a < 400:
                out += ["%s.%d" % (prefix, i) for i in range(a, b + 1)]
                continue
        m = re.match(r"^\d+\.\d+\.\d+$", part)
        if m:
            out.append(part)
    return out


claims = []
for r in extracted:
    text = r["evidence_quote"]
    m = re.search(r"Matrix Coverage:\s*(.+)", text)
    if m:
        claims.append((r["source_file"], r["uid"], m.group(1).strip()))
claims.sort()

rows = []
print("%-16s %-34s %6s %8s %8s" % ("BOARD", "CLAIM", "CITED", "REAL", "MISSING"))
for src, uid, claim in claims:
    ids = expand(claim)
    missing = [i for i in ids if i not in matrix_ids]
    # what the blind read actually matched on that board's rows
    ours = set()
    for e in extracted:
        if e["source_file"] != src:
            continue
        v = verdicts.get(e["uid"])
        if not v:
            continue
        for rid in [x.strip() for x in v.get("matrix_req_ids", "").split(",") if x.strip()]:
            ours.add(rid)
    claimed = set(ids)
    rows.append({
        "board": src, "claim": claim,
        "cited": len(ids), "real": len(ids) - len(missing),
        "missing": ", ".join(missing),
        "confirmed_by_blind_read": ", ".join(sorted(claimed & ours)),
        "claimed_not_found": ", ".join(sorted(claimed - ours)),
        "found_not_claimed": ", ".join(sorted(ours - claimed)),
        "n_confirmed": len(claimed & ours),
        "n_claimed_not_found": len(claimed - ours),
        "n_found_not_claimed": len(ours - claimed),
    })
    print("%-16s %-34s %6d %8d %8d" % (src, claim[:34], len(ids), len(ids) - len(missing), len(missing)))

dest = os.path.join(BLIND, "claims.jsonl")
with io.open(dest, "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

tot_cited = sum(r["cited"] for r in rows)
tot_missing = sum(len(r["missing"].split(", ")) if r["missing"] else 0 for r in rows)
tot_conf = sum(r["n_confirmed"] for r in rows)
print("\n%d claims, %d requirement ids cited, %d of those do not exist in the matrix"
      % (len(rows), tot_cited, tot_missing))
print("%d cited ids were independently landed on by the blind read" % tot_conf)
print("->", dest)
