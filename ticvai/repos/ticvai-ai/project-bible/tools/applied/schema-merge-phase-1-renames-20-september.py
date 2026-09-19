#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1 of the schema merge: eleven renames and five moves. No new operations.

**A rename in the contract alone does not land.** `derive-schema.py` merges into the previous
`schema-reference.json` rather than rebuilding it — `untouched = [t for t in existing if t not in
derived]` — and there is no mechanism to retire a table, only
`x-ticvai-retired-columns` for columns. Change the persistence tag and the package ends up
holding **both** names: the new one from the contract and the old one kept as-is, with every
foreign key, operation and screen still pointing at the old.

That is the same fault the retail wallet orphans had on 19 September, and this script has the
same shape as the one that fixed them: edit the source, then repoint every derived file that
cannot repoint itself.

    contracts/                the x-ticvai-persistence tag, which is the only source
    schema-reference.json     five table-keyed sections, plus every `references` value
    relationship-graph.json   both endpoints of every edge, and the tab_ops / tab_screens keys
    api-data-lineage.json     reads and writes, which are additive and never updated
    derive-schema-history.py  the rename declared, so a workbook diff reads sixteen renames
                              rather than sixteen deletions and sixteen additions

**Nothing here changes an operationId or a schema name.** `OrgUnit` stays `OrgUnit` in
`tenancy.yaml`; only the table it persists to is renamed. That is what keeps phase 1 free of new
operations and therefore free of new screens.

    python3 tools/applied/schema-merge-phase-1-renames-20-september.py --apply
"""
import collections
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")

# old, new, the contract that carries the tag, why
MOVES = [
    # --- renames, decided on readability against their workbook -------------
    ("platform.org_unit", "platform.scope", "contracts/spine/tenancy.yaml",
     "scope is the word 58 of our configuration profiles already address by; org_unit is generic "
     "ERP vocabulary that appears nowhere else in our language"),
    ("fnb.fnb_order", "fnb.service_order", "contracts/satellite/fnb.yaml",
     "fnb_order repeats its schema, which is the fault we ask them to fix in approvals."
     "approval_matrix. Their name is fnb.order and we are not taking it: order is a reserved "
     "word in Postgres, so the table would need quoting in every hand-written query forever. "
     "We solved this once already with orders.sales_order, and their own purpose line calls "
     "this the operational food-service order"),
    ("fnb.fnb_order_line", "fnb.service_order_line", "contracts/satellite/fnb.yaml",
     "their order_item plus our word: a line is what an order has"),
    ("fnb.table", "fnb.dining_table", "contracts/satellite/fnb.yaml",
     "table alone is vague beside fnb.table_reservation and fnb.table_session"),
    ("fnb.eighty_six_event", "fnb.sold_out_item", "contracts/satellite/fnb.yaml",
     "86 is US restaurant jargon and this platform ships in the Gulf"),
    ("ai.interaction", "ai.activity", "contracts/satellite/ai.yaml",
     "their purpose line: any AI request, including non-chat calls. An interaction reads as a "
     "conversation and most of these rows are not one"),
    ("control.api_quota", "control.api_limit", "contracts/satellite/public-api.yaml",
     "rate limits and usage limits; quota covers only the second"),
    ("queue.waiting_guest", "queue.entry", "contracts/satellite/queue.yaml",
     "their purpose says a customer or party; waiting_guest misnames a party of six"),
    ("orders.shift", "orders.pos_shift", "contracts/spine/shift.yaml",
     "disambiguates from workforce.shift, which they also hold"),
    ("maintenance.maintenance_plan", "maintenance.preventive_plan",
     "contracts/satellite/maintenance.yaml", "repeats its schema, and preventive is more specific"),
    ("marketing.journey_entrant", "marketing.journey_enrollment",
     "contracts/satellite/marketing-crm.yaml", "entrant reads as a person, not a record"),
    # --- moves, decided on the service and schema boundaries ----------------
    ("orders.payment_provider", "payments.provider", "contracts/spine/orders.yaml",
     "decision 2: configuration belongs in payments, the transaction stays in orders"),
    ("orders.payment_token", "payments.token", "contracts/spine/orders.yaml",
     "decision 2, same boundary"),
    ("control.subscription", "subscription.contract", "contracts/satellite/subscription.yaml",
     "decision 3: subscription lived in three places. contract rather than subscription."
     "subscription, which would repeat the schema"),
    ("control.subscription_plan", "subscription.plan", "contracts/satellite/subscription.yaml",
     "decision 3, and it drops the repeated prefix"),
    ("rental.category", "maintenance.asset_category", "contracts/satellite/rental.yaml",
     "it is the asset-category master for the whole venue - maintenance.asset, maintenance_plan, "
     "inspection_template, resources.resource_category and resource_requirement all point at it. "
     "A forklift that is never rented had its category defined in rental"),
]

# Prose that names a table by hand and would otherwise go stale.
PROSE = [
    ("contracts/satellite/ai.yaml", "aggregated from ai.interaction", "aggregated from ai.activity"),
]

NEW_OF = {old: new for old, new, _, _ in MOVES}
TABLE_SECTIONS = ("cols", "origin", "storage", "store", "lineage")


def rename_keys(d, note):
    """Rename table keys in place, reporting collisions rather than silently merging."""
    hit = 0
    for old, new in NEW_OF.items():
        if old not in d:
            continue
        if new in d:
            print("    !! %s already holds %s - left alone (%s)" % (note, new, old))
            continue
        d[new] = d.pop(old)
        hit += 1
    return hit


def main():
    apply = "--apply" in sys.argv[1:]
    print("  %d rename(s) and move(s)\n" % len(MOVES))

    # ── 1. the contracts, which are the only source ──────────────────────────
    edits = 0
    for old, new, rel, _ in MOVES:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding="utf-8").read()
        # Only the persistence tag. A compound tag (`a + b`) keeps its partner.
        pat = re.compile(r'(x-ticvai-persistence:[^\n]*?)\b' + re.escape(old) + r'\b')
        s2, n = pat.subn(lambda m: m.group(1) + new, s)
        if not n:
            print("    !! %-32s -> %-30s tag NOT FOUND in %s" % (old, new, rel))
            continue
        print("    %-32s -> %-30s %s (%d tag)" % (old, new, os.path.basename(rel), n))
        edits += n
        if apply:
            io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
    for rel, old, new in PROSE:
        p = os.path.join(ROOT, rel)
        s = io.open(p, encoding="utf-8").read()
        if old in s:
            print("    prose: %s" % old)
            if apply:
                io.open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))

    # ── 2. schema-reference: five table-keyed sections and every reference ───
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    moved = sum(rename_keys(S[k], k) for k in TABLE_SECTIONS if isinstance(S.get(k), dict))
    repointed = 0
    for table, columns in (S.get("cols") or {}).items():
        for c in columns:
            tgt = c.get("references")
            if tgt in NEW_OF:
                c["references"] = NEW_OF[tgt]
                repointed += 1
            src = c.get("source") or ""
            if isinstance(src, str) and src.startswith("rental.RentalCategory"):
                pass  # the schema name is unchanged; only its table moved
    print("\n  schema-reference: %d table key(s) renamed, %d column reference(s) repointed"
          % (moved, repointed))

    # ── 3. relationship graph: both endpoints, and the two index maps ────────
    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    ends = 0
    for r in G.get("rels") or []:
        for side in ("frm", "to"):
            if r.get(side) in NEW_OF:
                r[side] = NEW_OF[r[side]]
                ends += 1
    idx = sum(rename_keys(G[k], k) for k in ("tab_ops", "tab_screens") if isinstance(G.get(k), dict))
    print("  relationship-graph: %d endpoint(s), %d index key(s)" % (ends, idx))

    # ── 4. lineage, which is additive and never updates itself ───────────────
    lp = os.path.join(H, "api-data-lineage.json")
    L = json.load(io.open(lp, encoding="utf-8"))
    touched = 0
    for op, v in L.items():
        for key in ("reads", "writes"):
            row = v.get(key)
            if not isinstance(row, list):
                continue
            new_row = [NEW_OF.get(t, t) for t in row]
            if new_row != row:
                # A move can make a duplicate if both names were listed.
                seen, out = set(), []
                for t in new_row:
                    if t not in seen:
                        seen.add(t)
                        out.append(t)
                v[key] = out
                touched += 1
    print("  lineage: %d operation entr(y/ies) repointed" % touched)

    # ── 5. the tools that name a table by hand ──────────────────────────────
    #
    # **Eight tools hardcode one of these names and several are lookups, not prose.**
    # `check-package.py` fails every AI operation that "writes no ai.interaction";
    # `derive-schema.py` carries a MISTARGETED override keyed on `queue.waiting_guest`;
    # `derive-schema-roots.py` names `fnb.fnb_order` as the F&B schema root;
    # `derive-table-notes.py` keys ten hand-written notes on names that are about to move.
    # The rest is prose describing the package, which goes stale the moment a table is renamed.
    #
    # **Two files are excluded and it matters.** `build-merge-workbook.py` and
    # `derive-schema-history.py` carry the OLD names deliberately — one says "rename
    # platform.org_unit to platform.scope" and the other declares the rename — so a blanket
    # replace would turn both into "rename platform.scope to platform.scope".
    SKIP = ("build-merge-workbook.py", "derive-schema-history.py")
    tool_edits = collections.Counter()
    for name in sorted(os.listdir(os.path.join(ROOT, "tools"))):
        if not name.endswith(".py") or name in SKIP:
            continue
        tp = os.path.join(ROOT, "tools", name)
        text = io.open(tp, encoding="utf-8").read()
        out = text
        n = 0
        for old, new in NEW_OF.items():
            pat = r'(?<![\w.])' + re.escape(old) + r'(?![\w])'
            n += len(re.findall(pat, out))
            out = re.sub(pat, new, out)
        if out != text:
            tool_edits[name] = n
            if apply:
                io.open(tp, "w", encoding="utf-8", newline="\n").write(out)
    print("\n  tools: %d file(s), %d name(s)" % (len(tool_edits), sum(tool_edits.values())))
    for name, n in tool_edits.most_common():
        print("    %-34s %d" % (name, n))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0

    for path, data in ((sp, S), (gp, G), (lp, L)):
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            json.dumps(data, indent=1 if path != sp else None, ensure_ascii=False))
        print("  -> handoff/%s" % os.path.basename(path))

    # ── 6. declare the renames, so a diff does not read them as deletions ────
    hp = os.path.join(ROOT, "tools", "derive-schema-history.py")
    s = io.open(hp, encoding="utf-8").read()
    block = "".join(
        '    {"from": "%s", "to": "%s", "on": "2026-09-20",\n     "why": "%s"},\n'
        % (old, new, why.replace('"', "'"))
        for old, new, _, why in MOVES)
    marker = "RENAMES = [\n"
    if "2026-09-20" not in s and marker in s:
        io.open(hp, "w", encoding="utf-8", newline="\n").write(s.replace(marker, marker + block, 1))
        print("  -> tools/derive-schema-history.py (%d rename(s) declared)" % len(MOVES))
    else:
        print("  derive-schema-history.py already carries a 2026-09-20 rename - left alone")

    print("\n  Now run tools/refresh.sh. derive-schema will read the new tags; everything\n"
          "  downstream was repointed above because none of it can repoint itself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
