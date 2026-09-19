#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""When each table first appeared, what it was called before, and what breaks if it moves.

**A workbook that cannot say "renamed" says "deleted" and "added" instead.** On 19 September
`retail.wallet`, `retail.wallet_transaction` and `retail.gift_card` became `wallet.*` when the
wallet runtime left `retail.yaml`. Nothing in the package records that they are the same three
tables, so anyone comparing this week's workbook to last week's sees three disappear and three
arrive — and the safe reading of a table disappearing is that its data was dropped.

**And the workbook's idea of what is new is a set literal typed on 14 August.** Eighteen names
in `build-schema-workbook.py`, still shown blue five weeks later, while the schema went from
378 tables to 556 — **178 tables arrived and not one of them is marked.** A highlight that
cannot go stale is a highlight nobody has to maintain; this one could, and did.

## Additive, like the lineage, and for the same reason

`handoff/schema-history.json` is appended and never rewritten. A table seen for the first time
records the date it was seen; a table that disappears is **kept**, because a name that stops
appearing is either a rename somebody must record or a deletion somebody must confirm, and a
tool cannot tell which. That is the same rule `derive-lineage` follows, arrived at the same
way: on 19 September an entry that silently vanished would have hidden three renames.

Renames are declared in `renames` by hand — a rename is a judgement about identity, not
something a diff can see, since to a diff it is exactly a delete and an add.

## Blast radius

For a table that moves, the answer to "what breaks" is already derivable: every operation that
reads or writes it, every service that owns or reaches it, every screen whose operations touch
it. `--radius <table>` prints that, so the question is answered before the rename rather than
by `check-package` three steps later.

    python3 tools/derive-schema-history.py              # report
    python3 tools/derive-schema-history.py --apply      # record what is new
    python3 tools/derive-schema-history.py --radius wallet.wallet
"""
import collections
import datetime
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
OUT = os.path.join(H, "schema-history.json")
TODAY = datetime.date.today().isoformat()

# **Seeded, not invented.** Four of the eighteen names `build-schema-workbook.py` carried as
# "new on 14 August" still exist under that name; the rest were renamed or absorbed in the
# five weeks since, which is itself the argument for recording this. Keeping these dated
# preserves the only evidence the package holds about when a table arrived. Everything else is
# recorded at the baseline — "at or before 19 September" — because there is no earlier
# evidence for it, and inventing one would be worse than saying so.
SEED_14_AUG = {
    "platform.outlet", "platform.tenant", "marketing.guest_device", "marketing.wishlist_item",
}

# A rename is a judgement about identity. Declared here, never inferred.
RENAMES = [
    {"from": "platform.org_unit", "to": "platform.scope", "on": "2026-09-20",
     "why": "scope is the word 58 of our configuration profiles already address by; org_unit is generic ERP vocabulary that appears nowhere else in our language"},
    {"from": "fnb.fnb_order", "to": "fnb.service_order", "on": "2026-09-20",
     "why": "fnb_order repeats its schema, which is the fault we ask them to fix in approvals.approval_matrix. Their name is fnb.order and we are not taking it: order is a reserved word in Postgres, so the table would need quoting in every hand-written query forever. We solved this once already with orders.sales_order, and their own purpose line calls this the operational food-service order"},
    {"from": "fnb.fnb_order_line", "to": "fnb.service_order_line", "on": "2026-09-20",
     "why": "their order_item plus our word: a line is what an order has"},
    {"from": "fnb.table", "to": "fnb.dining_table", "on": "2026-09-20",
     "why": "table alone is vague beside fnb.table_reservation and fnb.table_session"},
    {"from": "fnb.eighty_six_event", "to": "fnb.sold_out_item", "on": "2026-09-20",
     "why": "86 is US restaurant jargon and this platform ships in the Gulf"},
    {"from": "ai.interaction", "to": "ai.activity", "on": "2026-09-20",
     "why": "their purpose line: any AI request, including non-chat calls. An interaction reads as a conversation and most of these rows are not one"},
    {"from": "control.api_quota", "to": "control.api_limit", "on": "2026-09-20",
     "why": "rate limits and usage limits; quota covers only the second"},
    {"from": "queue.waiting_guest", "to": "queue.entry", "on": "2026-09-20",
     "why": "their purpose says a customer or party; waiting_guest misnames a party of six"},
    {"from": "orders.shift", "to": "orders.pos_shift", "on": "2026-09-20",
     "why": "disambiguates from workforce.shift, which they also hold"},
    {"from": "maintenance.maintenance_plan", "to": "maintenance.preventive_plan", "on": "2026-09-20",
     "why": "repeats its schema, and preventive is more specific"},
    {"from": "marketing.journey_entrant", "to": "marketing.journey_enrollment", "on": "2026-09-20",
     "why": "entrant reads as a person, not a record"},
    {"from": "orders.payment_provider", "to": "payments.provider", "on": "2026-09-20",
     "why": "decision 2: configuration belongs in payments, the transaction stays in orders"},
    {"from": "orders.payment_token", "to": "payments.token", "on": "2026-09-20",
     "why": "decision 2, same boundary"},
    {"from": "control.subscription", "to": "subscription.contract", "on": "2026-09-20",
     "why": "decision 3: subscription lived in three places. contract rather than subscription.subscription, which would repeat the schema"},
    {"from": "control.subscription_plan", "to": "subscription.plan", "on": "2026-09-20",
     "why": "decision 3, and it drops the repeated prefix"},
    {"from": "rental.category", "to": "maintenance.asset_category", "on": "2026-09-20",
     "why": "it is the asset-category master for the whole venue - maintenance.asset, maintenance_plan, inspection_template, resources.resource_category and resource_requirement all point at it. A forklift that is never rented had its category defined in rental"},
    {"from": "retail.wallet", "to": "wallet.wallet", "on": "2026-09-19",
     "why": "the wallet runtime left retail.yaml for wallet.yaml; a service that owns tables "
            "inside another service's schema is not its own service"},
    {"from": "retail.wallet_transaction", "to": "wallet.wallet_transaction", "on": "2026-09-19",
     "why": "moved with wallet.wallet"},
    {"from": "retail.gift_card", "to": "wallet.gift_card", "on": "2026-09-19",
     "why": "moved with wallet.wallet"},
]


def tables():
    ref = os.path.join(H, "schema-reference.json")
    cols = (json.load(io.open(ref, encoding="utf-8")).get("cols") or {})
    return {t for t in cols if ":" not in t}


def load():
    try:
        return json.load(io.open(OUT, encoding="utf-8"))
    except Exception:
        return {"note": "", "firstSeen": {}, "renames": [], "withdrawn": {}}


def radius(table):
    """Everything that would have to move with it."""
    lin = json.load(io.open(os.path.join(H, "api-data-lineage.json"), encoding="utf-8"))
    dec = json.load(io.open(os.path.join(H, "service-decomposition.json"), encoding="utf-8"))
    reads = sorted(o for o, v in lin.items() if table in (v.get("reads") or []))
    writes = sorted(o for o, v in lin.items() if table in (v.get("writes") or []))
    touch = set(reads) | set(writes)
    services = sorted({lin[o].get("service") for o in touch if lin[o].get("service")})
    owner = [n for n, s in (dec.get("services") or {}).items()
             if table.split(".")[0] in (s.get("schemas") or [])]
    screens = collections.Counter()
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        for s in (d.get("screens") or []):
            if touch & {a.get("operationId") for a in (s.get("apis") or [])}:
                screens[(d.get("platform") or {}).get("code")] += 1
    print("  %s" % table)
    print("    owned by        %s" % (", ".join(owner) or "NO SERVICE"))
    print("    read by         %d operation(s)" % len(reads))
    print("    written by      %d operation(s)  %s" % (len(writes), ", ".join(writes[:4])))
    print("    services        %s" % ", ".join(services))
    print("    screens         %d across %s"
          % (sum(screens.values()), ", ".join(sorted(screens))))
    print()
    print("    Renaming it means every one of those lineage entries, the relationship graph,")
    print("    schema-reference and the generated DDL — derive-lineage and derive-schema both")
    print("    add without removing, so the old name survives until it is repointed at source.")
    return 0


def main():
    argv = sys.argv[1:]
    if "--radius" in argv:
        return radius(argv[argv.index("--radius") + 1])

    apply = "--apply" in argv
    hist = load()
    now = tables()
    first = hist.setdefault("firstSeen", {})
    hist["renames"] = RENAMES
    renamed_from = {r["from"] for r in RENAMES}
    renamed_to = {r["to"] for r in RENAMES}

    # **The first run knows only that everything exists, not when it arrived.** Recording
    # 552 tables as "new today" would light the whole sheet on the one run that says least.
    # The opening population is a baseline — "at or before this date" — and only what appears
    # afterwards is a change.
    baseline = hist.get("baseline")
    if not baseline and not first:
        baseline = TODAY
        hist["baseline"] = baseline

    fresh = sorted(t for t in now if t not in first)
    gone = sorted(t for t in first if t not in now and t not in renamed_from)
    for t in fresh:
        first[t] = "2026-08-14" if t in SEED_14_AUG else TODAY
    # A name that stops appearing is kept and flagged, never dropped.
    withdrawn = hist.setdefault("withdrawn", {})
    for t in gone:
        withdrawn.setdefault(t, TODAY)

    by_date = collections.Counter(first.values())
    print("  %d table(s) tracked · %d first seen today · %d rename(s) declared"
          % (len(first), sum(1 for t in fresh if first[t] == TODAY), len(RENAMES)))
    if gone:
        print("  %d name(s) no longer present and not declared as renamed — a deletion "
              "somebody must confirm:" % len(gone))
        for t in gone[:8]:
            print("      %s" % t)
    print()
    for r in RENAMES:
        state = "resolved" if r["to"] in now and r["from"] not in now else "NOT APPLIED"
        print("  rename  %-30s -> %-26s %s" % (r["from"], r["to"], state))
    print()
    print("  first seen, by date: %s"
          % ", ".join("%s %d" % (d, n) for d, n in sorted(by_date.items())))

    hist["note"] = ("When each table first appeared, and what it was called before. Appended, "
                    "never rewritten — a name that stops appearing is kept, because a tool "
                    "cannot tell a rename from a deletion and both need a person.")
    hist["generated"] = TODAY
    if not apply:
        print("\n  nothing written — pass --apply")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(hist, indent=1, ensure_ascii=False))
    print("  -> handoff/schema-history.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
