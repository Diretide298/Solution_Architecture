# -*- coding: utf-8 -*-
"""`ai.chunk_ref` merged into `ai.chunk_embedding` (30 September). Re-runnable.

**Two tables mapped a chunk to its Qdrant point.** ADR-0049 (accepted 30 September) made
`ai.chunk_embedding` the tenant database's record of each chunk's point: collection alias, point
id, embedding model, content hash, indexed_at. The older `ai.chunk_ref` ("maps a Qdrant point id
back to its document and scope") did the same job and nothing else, and no contract described it:
it was a table from the original dump whose only columns were a synthesised key and a
`document_id` the relationship graph supplied. Two tables answering "which points does this
document have" is two answers to keep equal, and erasure (ADR-0047, ADR-0049) needs exactly one.

**`ai.chunk_embedding` is kept and `ai.chunk_ref` is retired.** Nothing needs absorbing:
`chunk_ref` had `id` and `document_id`, and `chunk_embedding` already has both; its scope comes
through the document (`platform.apply_parent_rls`) exactly as `chunk_ref`'s did. It had no
status or retired_at to carry across.

What moves:

1. **Contract.** `AiChunkEmbedding` says it absorbed `chunk_ref`, and `parentChunkId` declares its
   target, `ai.chunk_embedding` (the parent section is another chunk row). It pointed at
   `ai.chunk_ref` by name convention only.
2. **`handoff/schema-reference.json`.** `ai.chunk_ref` leaves `cols`, `storage`, `store`, `module`,
   `origin` and `lineage`. Two catalogue columns pointed at it by a naming accident, not a
   decision: `fee_rule.eligibility_ref_id` and `price_assignment.scope_ref_id` end in `_ref_id` and
   `chunk_ref` was the only table whose short name ended `ref`. Those references are cleared,
   because `derive-relationships` skips a column that already carries one and would keep the
   stale target alive.
3. **`handoff/relationship-graph.json`.** Its edges from and to `ai.chunk_ref` are dropped (the
   parent-chunk edge comes back from the contract declaration on the next derive), and its
   operations and screens join `ai.chunk_embedding`'s.
4. **`handoff/api-data-lineage.json`.** The six operations that read `ai.chunk_ref`
   (`sendAiMessage`, `semanticSearch`, `listKnowledgeCollections`, `createKnowledgeCollection`,
   `ingestKnowledgeDocument`, `generateConfiguration`) read `ai.chunk_embedding` instead. This is a
   hand edit of existing entries, which `derive-lineage.py --apply` never makes.
5. **`docs/architecture/ai-system-design.md`** no longer lists `chunk_ref` among the AI tables
   gaining a policy.

ADR-0049's erasure and offboarding text already names `ai.chunk_embedding`, and still does.

    python tools/applied/chunk-ref-merge-30-september.py            dry run
    python tools/applied/chunk-ref-merge-30-september.py --apply
"""
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
H = ROOT / "handoff"
APPLY = "--apply" in sys.argv
OLD, NEW = "ai.chunk_ref", "ai.chunk_embedding"
# Pointed at chunk_ref by the `_ref_id` suffix alone.
ACCIDENTS = {("catalogue.fee_rule", "eligibility_ref_id"), ("catalogue.price_assignment", "scope_ref_id")}
CHANGED = []


def contract():
    p = ROOT / "contracts" / "satellite" / "ai.yaml"
    t = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    L = t.split(nl)
    s = next(i for i, l in enumerate(L) if l.rstrip() == "    AiChunkEmbedding:")
    e = next(i for i in range(s + 1, len(L)) if L[i].startswith("    ") and not L[i].startswith("     ")
             and L[i].strip())
    block = L[s:e]
    if not any("absorbed `ai.chunk_ref`" in l for l in block):
        d = next(i for i, l in enumerate(block) if l.startswith("      description: '**The tenant database"))
        k = d + 1
        while not block[k].rstrip().endswith("`platform.apply_parent_rls`).'"):
            k += 1
        block[k] = block[k].rstrip()[:-1]
        block[k + 1:k + 1] = [
            "",
            "        **It absorbed `ai.chunk_ref`** (30 September). That older table mapped a Qdrant point back to its",
            "        document and scope, which is this row''s job; its only columns, a key and `document_id`, are here",
            "        already. One table answers which points a document has, so erasure checks against one list.'",
        ]
        CHANGED.append("contracts/satellite/ai.yaml: AiChunkEmbedding absorbs ai.chunk_ref")
    p0 = next(i for i, l in enumerate(block) if l.strip() == "parentChunkId:")
    p1 = p0 + 1
    while p1 < len(block) and len(block[p1]) - len(block[p1].lstrip()) > 8:
        p1 += 1
    if not any("x-ticvai-references" in l for l in block[p0:p1]):
        block[p0 + 1:p1] = [
            "          type: string",
            "          format: uuid",
            "          nullable: true",
            "          x-ticvai-references: ai.chunk_embedding",
            "          description: The parent section's own row, where the source uses `parentChild` chunking.",
        ]
        CHANGED.append("contracts/satellite/ai.yaml: parentChunkId references ai.chunk_embedding")
    L[s:e] = block
    new = nl.join(L)
    if new != t and APPLY:
        io.open(p, "w", encoding="utf-8", newline="").write(new)


def schema_reference():
    p = H / "schema-reference.json"
    S = json.loads(p.read_text(encoding="utf-8"))
    n, before = 0, len(CHANGED)
    for section in ("cols", "storage", "store", "module", "origin", "lineage"):
        d = S.get(section)
        if isinstance(d, dict) and OLD in d:
            d.pop(OLD)
            n += 1
    if n:
        CHANGED.append(f"schema-reference: {OLD} removed from {n} section(s)")
    for table, cols in (S.get("cols") or {}).items():
        for c in cols:
            if c.get("references") != OLD:
                continue
            if (table, c.get("column")) in ACCIDENTS:
                for k in ("references", "referenceKind", "referenceHow", "enforced"):
                    c.pop(k, None)
                CHANGED.append(f"schema-reference: {table}.{c['column']} no longer points at {OLD}")
            else:
                c["references"] = NEW
                CHANGED.append(f"schema-reference: {table}.{c['column']} -> {NEW}")
    if APPLY and len(CHANGED) > before:
        p.write_text(json.dumps(S), encoding="utf-8")


def graph():
    p = H / "relationship-graph.json"
    G = json.loads(p.read_text(encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in G.get("rels") or [] if OLD not in (r.get("frm"), r.get("to"))]
    dropped = before - len(G["rels"])
    moved = 0
    for key in ("tab_ops", "tab_screens"):
        d = G.get(key) or {}
        if OLD in d:
            d[NEW] = sorted(set(d.get(NEW) or []) | set(d.pop(OLD)), key=str)
            moved += 1
    if dropped or moved:
        CHANGED.append(f"relationship-graph: {dropped} edge(s) dropped, {moved} index(es) merged")
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(G, indent=1))


def lineage():
    p = H / "api-data-lineage.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    ops = []
    for op, v in d.items():
        if not isinstance(v, dict):
            continue
        for k in ("reads", "writes"):
            row = v.get(k)
            if not isinstance(row, list) or OLD not in row:
                continue
            was_sorted = row == sorted(row)
            out = []
            for t in row:
                t = NEW if t == OLD else t
                if t not in out:
                    out.append(t)
            v[k] = sorted(out) if was_sorted else out
            ops.append(f"{op}.{k}")
    if ops:
        CHANGED.append(f"lineage: {OLD} -> {NEW} in {len(ops)} list(s): {', '.join(ops)}")
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, ensure_ascii=False))


def docs():
    p = ROOT / "docs" / "architecture" / "ai-system-design.md"
    t = io.open(p, encoding="utf-8", newline="").read()
    old = ("**The five existing AI tables with no policy** (`chunk_ref`, `index_failure`, `knowledge_document`, "
           "`proposed_action`, `suggestion_outcome`)")
    new = ("**The four existing AI tables with no policy** (`index_failure`, `knowledge_document`, "
           "`proposed_action`, `suggestion_outcome`; a fifth, `chunk_ref`, was merged into `ai.chunk_embedding` "
           "on 30 September)")
    if old in t:
        CHANGED.append("docs/architecture/ai-system-design.md: chunk_ref no longer listed")
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="").write(t.replace(old, new))


if __name__ == "__main__":
    contract()
    schema_reference()
    graph()
    lineage()
    docs()
    for c in CHANGED:
        print(f"  {c}")
    if not CHANGED:
        print("  nothing to do")
    print("  applied" if APPLY else "  dry run: pass --apply")
