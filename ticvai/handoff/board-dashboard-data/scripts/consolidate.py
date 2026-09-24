"""Fold the Partial-resolution pass into the final verdicts.

After this, every assessed requirement carries an `action` - what a human would actually
do with it - rather than a verdict that needs interpreting:

  Covered        the matrix obliges it. Nothing to do.
  Traceability   the build specifies it, the matrix does not. Needs a register entry.
  Settled against  the build deliberately refused what the source asks for. This is not a
                 register entry - it goes back to whoever drew the board.
  Specification  neither pins it down. A real decision is outstanding.
  Absent         nothing covers it and nothing was found. Scope.
  Not assessed   no board or dashboard bearing.
"""
import json, io, os, sys, glob, re, collections

B = sys.argv[1]
P = os.path.join(os.path.dirname(B), "partial", "out")
load = lambda p: [json.loads(l) for l in io.open(p, encoding="utf-8") if l.strip()]

final = {r["uid"]: r for r in load(os.path.join(B, "verdicts-final.jsonl"))}

resolved = 0
for f in sorted(glob.glob(os.path.join(P, "partial*.jsonl"))):
    for r in load(f):
        uid = r.get("uid")
        if not uid or uid not in final:
            continue
        cur = final[uid]
        outcome = r.get("outcome", "")
        rationale = r.get("rationale", "") or ""
        settled = rationale.strip().lower().startswith("settled against")

        if outcome == "Covered":
            cur["verdict"] = "Covered"
            cur["action"] = "Covered"
            cur["gap_severity"] = ""
        elif outcome == "Traceability":
            cur["verdict"] = "Partial"
            cur["action"] = "Settled against" if settled else "Traceability"
        elif outcome == "Specification":
            cur["verdict"] = "Partial"
            cur["action"] = "Specification"
        if r.get("matrix_req_ids"):
            cur["matrix_req_ids"] = r["matrix_req_ids"]
        if r.get("build_path"):
            cur["where_else"] = r["build_path"]
        if r.get("evidence"):
            cur["evidence"] = r["evidence"]
        if rationale:
            cur["rationale"] = rationale
        if r.get("remaining_work"):
            cur["remaining_work"] = r["remaining_work"]
        if r.get("gap_severity") is not None and outcome != "Covered":
            cur["gap_severity"] = r.get("gap_severity", cur.get("gap_severity", ""))
        cur["verdict_source"] = "partial resolution, full matrix and repository"
        resolved += 1

# anything not touched by the partial pass gets an action derived from its verdict
for uid, cur in final.items():
    if cur.get("action"):
        continue
    v = cur.get("verdict", "")
    if v == "Covered":
        cur["action"] = "Covered"
    elif v == "Absent":
        cur["action"] = "Absent"
    elif v == "Not a requirement":
        cur["action"] = "Not a requirement"
    else:
        # a Partial the resolution pass never revisited
        cur["action"] = "Partial, not yet resolved"

dest = os.path.join(B, "verdicts-consolidated.jsonl")
with io.open(dest, "w", encoding="utf-8") as fh:
    for uid in sorted(final):
        fh.write(json.dumps(final[uid], ensure_ascii=False) + "\n")

print("%d rows, %d resolved by the partial pass -> %s" % (len(final), resolved, dest))
a = collections.Counter(r["action"] for r in final.values())
tot = len(final)
print("\nACTION:")
for k, c in a.most_common():
    print("  %-28s %5d  (%.1f%%)" % (k, c, 100.0 * c / tot))

spec = [r for r in final.values() if r["action"] == "Specification"]
print("\n%d Specification rows - the real remaining decisions" % len(spec))
print("severity:", dict(collections.Counter(r.get("gap_severity") for r in spec)))
