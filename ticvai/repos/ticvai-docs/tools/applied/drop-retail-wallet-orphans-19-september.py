#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove the three wallet tables that `retail` no longer owns.

**`derive-schema` merges and never rebuilds — and that is deliberate.** `refresh.sh` says so
at the top: a contract revert is a two-part revert, because the merge preserves judgements a
derivation cannot reproduce. The cost is that a table which *moves* is added under its new
name and never removed under its old one.

On 19 September `Wallet`, `WalletTransaction` and `GiftCard` moved from `retail.yaml` to
`wallet.yaml` and their `x-ticvai-persistence` went from `retail.*` to `wallet.*`. The
refresh added `wallet.wallet`, `wallet.wallet_transaction` and `wallet.gift_card`, and left
`retail.wallet`, `retail.wallet_transaction` and `retail.gift_card` behind — **so every one
of the three existed twice**, in `cols`, `storage`, `store`, `origin` and `lineage`.

That is not cosmetic. The table count is inflated by three, `derive-ddl` would emit both, and
`check-package` reported `retail.wallet: stores currency` against a table that no contract
declares any more — an error naming a row nobody can fix, because the contract it came from
no longer mentions it.

**Only these three, and only because a contract moved them.** A table that merely disappeared
from a contract is a different question — it might be a deletion somebody has to confirm — so
this names its three rather than sweeping every orphan.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(ROOT, "handoff", "schema-reference.json")

ORPHANS = ["retail.wallet", "retail.wallet_transaction", "retail.gift_card"]
MOVED_TO = {"retail.wallet": "wallet.wallet",
            "retail.wallet_transaction": "wallet.wallet_transaction",
            "retail.gift_card": "wallet.gift_card"}


def main():
    apply = "--apply" in sys.argv
    d = json.load(io.open(REF, encoding="utf-8"))

    # Refuse unless the replacement is actually there. Removing the old name when the new one
    # never landed would delete the table rather than move it.
    cols = d.get("cols") or {}
    missing = [new for old, new in MOVED_TO.items() if new not in cols]
    if missing:
        raise SystemExit("replacement table(s) absent, refusing to drop the originals: %s"
                         % missing)

    # **Dropping the tables is half of it.** Six `wallet.*` columns still declared
    # `references: retail.wallet`, and the relationship graph carried edges keyed on all three
    # old names. A column pointing at a table that does not exist is exactly what `check-package`
    # reports, and it only became visible once the orphan rows stopped satisfying the lookup.
    repointed = 0
    for section, value in d.items():
        if not isinstance(value, dict):
            continue
        for _tbl, cs in value.items():
            if not isinstance(cs, list):
                continue
            for c in cs:
                if isinstance(c, dict) and c.get("references") in MOVED_TO:
                    if apply:
                        c["references"] = MOVED_TO[c["references"]]
                    repointed += 1
    if repointed:
        print("  %d column reference(s) repointed to the new table names" % repointed)

    # **And the graph, which is what kept bringing them back.** `derive-schema` reads
    # `relationship-graph.json` for edges the contracts do not declare — 486 of 514 references
    # are conventions rather than `$ref`, so the graph is the source. An edge whose `frm` or `to`
    # is a dropped table re-registers that table on the next run, and `derive-relationships`
    # then rebuilds the graph from the schema it just repopulated. **Cleaning either one alone
    # is undone by the other**; this was dropped three times before the cycle was visible.
    gpath = os.path.join(ROOT, "handoff", "relationship-graph.json")
    gmoved = 0
    if os.path.exists(gpath):
        g = json.load(io.open(gpath, encoding="utf-8"))
        for r in g.get("rels", []):
            for k in ("frm", "to"):
                if r.get(k) in MOVED_TO:
                    if apply:
                        r[k] = MOVED_TO[r[k]]
                    gmoved += 1
        if gmoved and apply:
            io.open(gpath, "w", encoding="utf-8", newline=chr(10)).write(
                json.dumps(g, indent=1, ensure_ascii=False))
        if gmoved:
            print("  %d relationship-graph endpoint(s) repointed" % gmoved)

    removed = 0
    for section, value in d.items():
        if not isinstance(value, dict):
            continue
        for o in ORPHANS:
            if o in value:
                print("  %-10s %s" % (section, o))
                if apply:
                    del value[o]
                removed += 1

    print("\n  %d entry(s) across %d section(s)"
          % (removed, len({s for s, v in d.items() if isinstance(v, dict)})))
    for old, new in MOVED_TO.items():
        print("     %-28s -> %s  (%d column(s))" % (old, new, len(cols.get(new) or [])))
    # **Both halves count as work.** The first cut returned here whenever there was
    # nothing left to drop — which is the state after a partial run — so the six
    # repointed references were computed, printed, and never written.
    if not removed and not repointed:
        print("\nnothing to do")
        return
    if not apply:
        print("\n  nothing written — pass --apply")
        return
    io.open(REF, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, indent=1, ensure_ascii=False))
    print("  -> handoff/schema-reference.json")


if __name__ == "__main__":
    main()
