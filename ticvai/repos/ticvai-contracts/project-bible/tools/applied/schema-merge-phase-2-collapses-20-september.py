#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2 of the schema merge: one collapse, one misnamed table, one phantom, one bad rule.

Phase 1 renamed tables that were merely badly named. **These four are wrong rather than
badly named**, and each was found by reading their workbook against ours rather than by any
checker in this package.

    orders.payment_routing      a duplicate of payments.routing_rule. Both are "priority plus
                                conditions decide which provider", and their single
                                orders.payment_route maps onto both of ours
    marketing.loyalty_tier      holds earning triggers and multipliers, not tiers, and is
                                referenced by nothing: 0 operations, 0 screens, 0 foreign keys
    orders.order_discount       a phantom. No contract describes it; it exists because one
                                lineage entry, compItem, lists it as a write, and its only two
                                columns are a synthesised key and a parent id the relationship
                                graph invented
    *_asset_id                  derive-relationships resolves every *_asset_id to the stem
                                `asset`, which is maintenance.asset. An icon, an image, a PDF
                                and two signature scans are not maintenance assets

**The convention fix cannot land on its own.** `derive-relationships` skips a column that
already carries a `references` value, and `derive-schema` persists those values between runs, so
the stale `maintenance.asset` target would block the corrected rule from ever firing. The stale
values are cleared here so the next refresh can re-derive them.

    python3 tools/applied/schema-merge-phase-2-collapses-20-september.py --apply
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")

# ── 1. the collapse, and the rename ──────────────────────────────────────────
# `orders.payment_routing` stops being a table and becomes more columns on
# `payments.routing_rule`. Both contract schemas keep their own shape; only the table they
# persist to is shared, which is what derive-schema merges on. **Unifying the two API shapes is
# a contract change and is deliberately not done here** — phase 2 moves no operation.
MERGE_INTO = {
    "orders.payment_routing": "payments.routing_rule",
}
RENAME = {
    "marketing.loyalty_tier": "marketing.points_earning_rule",
}
# A table nothing describes. Dropped rather than renamed: renaming a phantom moves the phantom.
PHANTOM = ["orders.order_discount"]

MOVED = dict(MERGE_INTO)
MOVED.update(RENAME)

# ── 2. the convention rule ───────────────────────────────────────────────────
# **Only prefixes we are sure of.** `outgoing`, `incoming`, `returned`, `missing` and
# `available` are rental equipment movements and stay on `maintenance.asset`, as does a bare
# `asset_id`. `plan`, `source`, `fallback` and `base` are genuinely ambiguous and are left
# alone rather than guessed at — the same rule this deriver already applies to `template_id`.
MEDIA_PREFIXES = [
    "icon", "image", "photo", "logo", "cover", "background", "branding", "badge",
    "signature", "document", "terms_document", "mandate_text", "schema", "evidence",
    "artefact",
]

RULE = '''
    # 2a. **A media asset is not a maintenance asset.** Every `*_asset_id` resolved to the stem
    #     `asset`, which is `maintenance.asset` — the only table whose short name is `asset`.
    #     That made an icon, a product image, a terms PDF and two signature scans into pieces of
    #     venue equipment, and inflated the rental-to-maintenance coupling by 70% at the moment
    #     that coupling was the argument in a schema merge.
    #
    #     Only prefixes we are sure of. `outgoing`, `incoming`, `returned`, `missing` and
    #     `available` are rental equipment movements and stay where they are, as does a bare
    #     `asset_id`; `plan`, `source`, `fallback` and `base` are genuinely ambiguous and are
    #     left unlinked rather than guessed at, which is what this deriver already does with
    #     `template_id`.
    MEDIA_PREFIXES = %r
    _media = 0
    if "assets.media_asset" in tables:
        for table, columns in cols.items():
            for c in columns:
                name = c["column"]
                if not name.endswith("_id") or c.get("references"):
                    continue
                stem = name[:-3]
                if not stem.endswith("_asset"):
                    continue
                if stem[:-len("_asset")] in MEDIA_PREFIXES:
                    add(table, name, "assets.media_asset", "convention", "foreignKey")
                    _media += 1
        if _media:
            print("  %%d media asset edge(s) sent to assets.media_asset, not maintenance.asset"
                  %% _media)
''' % (MEDIA_PREFIXES,)

ANCHOR = ("    # 2b. Precedent. A column name the contracts declare a target for everywhere "
          "they\n")


def clear_stale_media(cols):
    """The corrected rule cannot fire while the wrong answer is still on the column."""
    cleared = collections.Counter()
    for table, columns in cols.items():
        for c in columns:
            name = c.get("column", "")
            if not name.endswith("_asset_id"):
                continue
            if c.get("references") != "maintenance.asset":
                continue
            if name[:-len("_asset_id")] not in MEDIA_PREFIXES:
                continue
            c.pop("references", None)
            c.pop("referenceHow", None)
            c.pop("enforced", None)
            cleared[table + "." + name] += 1
    return cleared


def main():
    apply = "--apply" in sys.argv[1:]

    # ── contracts: repoint the two persistence tags ──────────────────────────
    for old, new in sorted(MOVED.items()):
        found = False
        for dirpath, _, names in os.walk(os.path.join(ROOT, "contracts")):
            for n in sorted(names):
                if not n.endswith(".yaml"):
                    continue
                p = os.path.join(dirpath, n)
                s = io.open(p, encoding="utf-8").read()
                pat = re.compile(r'(x-ticvai-persistence:[^\n]*?)\b' + re.escape(old) + r'\b')
                s2, k = pat.subn(lambda m: m.group(1) + new, s)
                if k:
                    found = True
                    kind = "merge into" if old in MERGE_INTO else "rename to"
                    print("    %-28s %s %-30s %s (%d)"
                          % (old, kind, new, os.path.relpath(p, ROOT), k))
                    if apply:
                        io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
        if not found:
            print("    !! %-28s no persistence tag found" % old)

    # ── schema-reference ─────────────────────────────────────────────────────
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    cols = S.get("cols") or {}

    absorbed = 0
    for old, new in MERGE_INTO.items():
        src, dst = cols.get(old), cols.get(new)
        if src is None:
            continue
        if dst is None:
            cols[new] = cols.pop(old)
            continue
        have = {c["column"] for c in dst}
        for c in src:
            if c["column"] not in have:
                dst.append(c)
                absorbed += 1
        cols.pop(old)
    for old, new in RENAME.items():
        if old in cols and new not in cols:
            cols[new] = cols.pop(old)
    for t in PHANTOM:
        cols.pop(t, None)
    for section in ("origin", "storage", "store", "lineage"):
        d = S.get(section)
        if not isinstance(d, dict):
            continue
        for old, new in MOVED.items():
            if old in d and new not in d:
                d[new] = d.pop(old)
            else:
                d.pop(old, None)
        for t in PHANTOM:
            d.pop(t, None)

    repointed = 0
    for columns in cols.values():
        for c in columns:
            if c.get("references") in MOVED:
                c["references"] = MOVED[c["references"]]
                repointed += 1
            elif c.get("references") in PHANTOM:
                c.pop("references", None)
                c.pop("referenceHow", None)
                repointed += 1
    cleared = clear_stale_media(cols)
    print("\n  schema-reference: %d column(s) absorbed, %d reference(s) repointed, "
          "%d stale media reference(s) cleared" % (absorbed, repointed, len(cleared)))
    for k in sorted(cleared)[:8]:
        print("      %s" % k)

    # ── relationship graph and lineage ───────────────────────────────────────
    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in (G.get("rels") or [])
                 if r.get("frm") not in PHANTOM and r.get("to") not in PHANTOM]
    ends = 0
    for r in G["rels"]:
        for side in ("frm", "to"):
            if r.get(side) in MOVED:
                r[side] = MOVED[r[side]]
                ends += 1
    for key in ("tab_ops", "tab_screens"):
        d = G.get(key) or {}
        for old, new in MOVED.items():
            if old in d:
                d.setdefault(new, [])
                d[new] = sorted(set(d[new]) | set(d.pop(old)))
        for t in PHANTOM:
            d.pop(t, None)
    print("  relationship-graph: %d edge(s) dropped, %d endpoint(s) repointed"
          % (before - len(G["rels"]), ends))

    lp = os.path.join(H, "api-data-lineage.json")
    L = json.load(io.open(lp, encoding="utf-8"))
    touched = 0
    for op, v in L.items():
        for key in ("reads", "writes"):
            row = v.get(key)
            if not isinstance(row, list):
                continue
            out, seen = [], set()
            for t in row:
                t = MOVED.get(t, t)
                if t in PHANTOM or t in seen:
                    continue
                seen.add(t)
                out.append(t)
            if out != row:
                v[key] = out
                touched += 1
    print("  lineage: %d operation entr(y/ies) repointed" % touched)

    # ── the deriver ──────────────────────────────────────────────────────────
    rp = os.path.join(ROOT, "tools", "derive-relationships.py")
    rs = io.open(rp, encoding="utf-8").read()
    if "MEDIA_PREFIXES" in rs:
        print("  derive-relationships.py already carries the media rule - left alone")
    elif ANCHOR in rs:
        print("  derive-relationships.py: media rule inserted before the precedent pass")
        if apply:
            io.open(rp, "w", encoding="utf-8", newline="\n").write(rs.replace(ANCHOR, RULE + "\n" + ANCHOR, 1))
    else:
        print("  !! derive-relationships.py: anchor not found, rule NOT inserted")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    for path, data in ((sp, S), (gp, G), (lp, L)):
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            json.dumps(data, indent=1 if path != sp else None, ensure_ascii=False))
        print("  -> handoff/%s" % os.path.basename(path))
    print("\n  Now run tools/refresh.sh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
