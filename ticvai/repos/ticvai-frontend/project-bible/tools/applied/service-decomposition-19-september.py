#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bring `handoff/service-decomposition.json` up to the contracts, and add WalletService.

**Nothing in `tools/` writes this file, and on 19 September its note still read "How 28
contracts and 378 tables become 16 deployable services".** There were 32 and 561.
`rental` and `accreditation` appeared in it nowhere, while `check-package`,
`derive-diagrams`, `derive-burst-scope` and both workbooks read it to draw the service
topology — so four contracts were missing from every service diagram and both workbooks
while every checker passed. It is ring 4 of `docs/contract-change-runbook.md`, the part no
refresh can reach.

## What changed and why

**WalletService is new.** Wallet types are needed by eight domains — orders, fnb, retail,
games, subscription, workforce, partner and venue. A Gold Membership issues F&B credit,
parking credits and ride credits into one wallet, so subscription, games and F&B all read
it. A contract that eight domains depend on is infrastructure, like identity, not a
member of any one of them.

**accreditation goes to TenancyService, not AccessService.** AccessService is
*"read-heavy, extreme latency sensitivity, edge-cached"* — the turnstile path. Accreditation
is a back-office apply/review/approve workflow whose writes would invalidate caches on the
scan path, and whose deploys would restart the turnstiles. TenancyService already holds
`workforce` and `approvals`; accreditation is an approvals workflow about people.

**rental to VenueOpsService** — it sits beside resources, assets and games, all "low and
steady". **payments to OrderService** — commerce tier, *"the one that autoscales"*, and
payments burst with orders.

## The counts are computed, not typed

`operations`, `tables` and the note's totals are derived here from the contracts and their
`x-ticvai-persistence` annotations. **The judgement stays authored** — `why`, `scale`,
`risk` and `tier` are decisions a derivation cannot reproduce, and are left exactly as
they are.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "handoff", "service-decomposition.json")

ADD = {
    "VenueOpsService": ["rental"],
    "OrderService": ["payments"],
    "TenancyService": ["accreditation"],
}

WALLET = {
    "tier": "commerce",
    "contracts": ["wallet"],
    "schemas": ["wallet"],
    "why": "**Eight domains need a wallet and none of them owns it.** A Gold Membership "
           "issues F&B credit, parking credits and ride credits into the same wallet, so "
           "subscription, games and F&B all read it; `getWalletLiability` aggregates "
           "outstanding value across every credit type, so it has to see all of them. The "
           "13 wallet types in the client's library are compositions of owner, credit type "
           "and scope rather than thirteen kinds, which is only expressible in one place. "
           "**Split out of `retail` on 19 September**, where 13 of retail's 37 operations "
           "were the entire wallet runtime while `wallet.yaml` held only its rules.",
    "scale": "Read-heavy on the sale path — every till and reader resolves a balance — and "
             "write-heavy on top-up. **Latency-critical in a way LedgerService is not**, "
             "which is why the two are separate: the ledger is append-only and batch-"
             "tolerant, a balance check is neither.",
    "risk": "**It holds a liability owed to a customer.** A wallet that double-spends is a "
            "financial loss, not a bug report. Deduction order across credit lots is FEFO "
            "and is decided here, once, rather than per caller.",
}


def contracts_and_tables():
    ops, tables = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        name = os.path.basename(f)[:-5]
        d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        n = 0
        for _p, m in (d.get("paths") or {}).items():
            if isinstance(m, dict):
                n += sum(1 for v in m if v in ("get", "post", "put", "patch", "delete"))
        ops[name] = n
        t = set()
        for _s, sc in ((d.get("components") or {}).get("schemas") or {}).items():
            p = (sc or {}).get("x-ticvai-persistence")
            if isinstance(p, str) and "." in p and not p.startswith("none"):
                for part in p.split("+"):
                    part = part.strip()
                    if "." in part:
                        t.add(part)
        tables[name] = t
    return ops, tables


def main():
    apply = "--apply" in sys.argv
    d = json.load(io.open(OUT, encoding="utf-8"))
    svc = d["services"]
    ops, tables = contracts_and_tables()

    for name, add in ADD.items():
        cur = svc[name].setdefault("contracts", [])
        for c in add:
            if c not in cur:
                cur.append(c)
                print("  %-18s += %s" % (name, c))

    if "WalletService" not in svc:
        svc["WalletService"] = dict(WALLET)
        print("  WalletService       created")

    # retail no longer carries the wallet runtime
    assigned = set()
    for name, s in svc.items():
        assigned |= set(s.get("contracts") or [])
    missing = sorted(set(ops) - assigned - {"common", "permissions"})
    if missing:
        raise SystemExit("contract(s) in no service: %s" % missing)

    total_tables = set()
    for name, s in svc.items():
        cs = s.get("contracts") or []
        s["operations"] = sum(ops.get(c, 0) for c in cs)
        t = set()
        for c in cs:
            t |= tables.get(c, set())
        s["tables"] = len(t)
        total_tables |= t

    n_contracts = len([c for c in ops if c not in ("common", "permissions")])
    d["note"] = ("How %d contracts and %d tables become %d deployable services. "
                 "**The data boundaries were drawn first and the service boundaries follow "
                 "them** — no service spans two schemas it does not own."
                 % (n_contracts, len(total_tables), len(svc)))
    d["generated"] = "19 September 2026"

    print("\n  %d services, %d contracts, %d tables"
          % (len(svc), n_contracts, len(total_tables)))
    for name in sorted(svc, key=lambda k: -svc[k]["operations"])[:6]:
        print("     %-18s %3d ops  %3d tables  %s"
              % (name, svc[name]["operations"], svc[name]["tables"],
                 ",".join(svc[name].get("contracts") or [])))
    if not apply:
        print("\n  nothing written — pass --apply")
        return
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(d, indent=1, ensure_ascii=False))
    print("  -> handoff/service-decomposition.json")


if __name__ == "__main__":
    main()
