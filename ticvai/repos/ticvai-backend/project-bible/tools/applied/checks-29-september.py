# -*- coding: utf-8 -*-
"""The three check failures left by the build of 29 September. Re-runnable.

1. Six AI screens declare a publish-family operation (publishPromptTemplate, publishForecastVersion,
   promoteAiRelease, publishAiGovernancePolicy) and no publishGate. The gate is added at the top of
   the screen's first region, naming the operation that implies it.
2. Flow F90 step 1 still calls getRecommendations and getUpsellSuggestions on BO-119, which the build
   rebound onto the rules and decision operations (createUpsellRule, decideRecommendations).
3. BL-182 names no contract and lists 8 of the 73 rows that cite it. The package keeps the backlog
   reference on rows that were since completed, so refs list every citing row.
"""
import io, json, re, sys, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
GATES = {
    "screens/P09-platform-admin-console.yaml": {
        "ADM-037": "publishPromptTemplate", "ADM-508": "publishForecastVersion", "ADM-519": "promoteAiRelease",
        "ADM-528": "publishAiGovernancePolicy", "ADM-554": "promoteAiRelease"},
    "screens/P16-venue-analytics.yaml": {"ANL-060": "publishPromptTemplate"},
}


def gate_block(indent, op):
    i = " " * indent
    return (f"{i}- kind: publishGate\n"
            f"{i}  impliedBy: {op}\n"
            f"{i}  notes: 'Declares `{op}`. **The gate names what the publish will affect before it happens**:\n"
            f"{i}    which tenants, venues or capabilities take the new version, and that the previous one stays\n"
            f"{i}    available to roll back to.'\n"
            f"{i}  provenance: check-screens publish rule, 29 September 2026\n")


def add_gates(apply):
    n = 0
    for rel, want in GATES.items():
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.replace("\r\n", "\n").split("\n")
        for sid, op in want.items():
            start = next(i for i, l in enumerate(lines) if re.match(rf"^- id: {re.escape(sid)}\s*$", l))
            end = next((i for i in range(start + 1, len(lines)) if re.match(r"^- id: ", lines[i])), len(lines))
            body = "\n".join(lines[start:end])
            if "kind: publishGate" in body:
                continue
            ci = next(i for i in range(start, end) if re.match(r"^\s+components:\s*$", lines[i]))
            nxt = lines[ci + 1]
            indent = len(nxt) - len(nxt.lstrip()) if nxt.lstrip().startswith("- ") else len(lines[ci]) - len(lines[ci].lstrip()) + 2
            lines[ci + 1:ci + 1] = gate_block(indent, op).rstrip("\n").split("\n")
            n += 1
        if apply:
            io.open(p, "w", encoding="utf-8", newline="").write(nl.join(lines))
    print(f"  publish gates added: {n}")


def fix_flow(apply):
    p = next((ROOT / "flows").glob("F90-*.yaml"))
    t = p.read_text(encoding="utf-8")
    new = re.sub(r"(screen: BO-119\r?\n  action: [^\n]*\r?\n  operations:\r?\n)  - getRecommendations(\r?\n)  - getUpsellSuggestions",
                 r"\1  - createUpsellRule\2  - decideRecommendations", t)
    print(f"  F90 step 1: {'rebound' if new != t else 'already rebound'}")
    if apply and new != t:
        io.open(p, "w", encoding="utf-8", newline="").write(new)


def fix_backlog(apply):
    tp = ROOT / "handoff" / "traceability.json"
    rows = json.loads(tp.read_text(encoding="utf-8"))["rows"]
    cite = [r for r in rows if r.get("backlog") == "BL-182"]
    bp = ROOT / "handoff" / "contract-backlog.json"
    b = json.loads(bp.read_text(encoding="utf-8"))
    e = next(x for x in b["entries"] if x["id"] == "BL-182")
    e["refs"] = sorted({str(r["packageRef"]) for r in cite}, key=lambda s: [int(x) if x.isdigit() else x for x in re.split(r"[.]", s)])
    e["contracts"] = sorted({r["contract"] for r in cite if r.get("contract")})
    open_ = sum(1 for r in cite if r["verdict"] == "CONTRACTED_PARTIAL")
    e["why"] = ("**Found by the build of 29 September.** Of the " + str(len(cite)) + " rows the build touched as partial, "
                + str(len(cite) - open_) + " were completed the same evening (gap pass G1/G2) and keep the reference as history; "
                + str(open_) + " are still partial and wait on a make-or-break answer or a named owner decision, stated in each row's note.")
    print(f"  BL-182: {len(e['refs'])} refs, {len(e['contracts'])} contracts, {open_} still partial")
    if apply:
        bp.write_text(json.dumps(b, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    add_gates(apply); fix_flow(apply); fix_backlog(apply)
    print("  applied" if apply else "  dry run: pass --apply")
