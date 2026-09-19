#!/usr/bin/env python3
"""Fill `handoff/api-data-lineage.json` from the contracts, for operations it does not have.

**Twenty-plus tools read this file as authoritative and nothing in the package wrote it.** It
arrived with the dump. So an operation added to a contract was invisible to `check-package`,
`check-screens`, `derive-relationships`, `build-status`, the workbooks and the viewer until the
next drop — and `check-package` rule 32 failed the whole package for the gap, correctly, with no
tool able to close it. Sixteen operations drafted on 4 September hit exactly that.

**This is additive on purpose.** The 1,032 entries that came with the dump carry judgements a
derivation cannot reproduce — an `audience` narrowed by hand, a `service` assignment that is a
deployment decision rather than a contract fact. Rewriting them from the contracts would silently
replace considered values with inferred ones, so an entry that already exists is left exactly as
it is and only missing operations are added.

**`--audit` says where the two disagree** without changing anything, which is the honest way to
find out whether a full rebuild would be safe. It is not run by `refresh.sh`; somebody should read
it before anyone writes the rebuild this file eventually needs.

What is derived, and from where:

  `reads`   tables behind the schemas an operation RETURNS
  `writes`  tables behind the schema it ACCEPTS in a request body
  the rest  read straight off `x-ticvai-*` on the operation

Run: `python3 tools/derive-lineage.py [--apply] [--audit]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"

# A contract file's stem is the contract name every consumer uses.
SERVICE_OF = {}


def persistence_map() -> dict:
    """Schema name -> the table it persists to, across every contract."""
    out = {}
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for n, sch in ((doc.get("components") or {}).get("schemas") or {}).items():
            t = (sch or {}).get("x-ticvai-persistence")
            if not t:
                continue
            t = str(t).strip('"').strip()
            # **`none` is an answer, not a table.** Schemas that are computed, projected or held
            # only in a session say so here — "none — computed", "none — projection", "none —
            # Redis session registry". Taking that literally put a table called
            # `none — projection` into the lineage on 10 September, and `check-package` was right
            # to refuse a table the schema reference has never heard of.
            if t.lower().startswith("none"):
                continue
            out[n] = t
    return out


def tables_in(node, persist: dict) -> list:
    """Every persisted table reachable from a `$ref` inside this node."""
    refs = set(re.findall(r"#/components/schemas/([A-Za-z0-9_]+)", json.dumps(node or {})))
    return sorted({persist[r] for r in refs if r in persist})


# **A contract with no stored entry needs a person, and on 19 September five arrived at once.**
# The inference below reads the service off a contract's existing neighbours, which cannot work for
# a contract that has none — `derive-diagrams.py` then sorted a set containing `None` and stopped
# the whole refresh. These are the decisions, made once, in the same terms the existing ones use.
NEW_CONTRACT_SERVICE = {
    # Rental is venue floor operations — check-out, condition, return — beside `resources`,
    # `maintenance` and `games`, which are all VenueOps.
    "rental": "VenueOpsService",
    # Wallet configuration is stored value, which is Retail's: `retail` already owns the balance,
    # the transactions and the gift cards, and splitting the configuration onto another service
    # would put the rules a different side of a network boundary from the money.
    "wallet": "RetailService",
    # Payment orchestration routes and settles, which is the Order service's existing work —
    # `createPayment` and `capturePayment` are already there.
    "payments": "OrderService",
    # Accreditation grants places and times and is enforced at gates, so it sits with `access`
    # rather than with identity: the read that matters happens at a turnstile.
    "accreditation": "AccessService",
}


def service_by_contract(stored: dict) -> dict:
    """Which service serves each contract, taken from the entries that already exist.

    **`service` is a deployment decision, not a contract fact**, so it cannot be read off the
    OpenAPI — and `derive-diagrams.py` indexes screens by it and raises `KeyError` without it.
    Every contract in the package already has operations assigned to a service, so the answer is
    the service its neighbours use; a contract with no stored entry at all is in
    `NEW_CONTRACT_SERVICE` above.
    """
    import collections
    by = collections.defaultdict(collections.Counter)
    for v in stored.values():
        if v.get("service"):
            by[v.get("contract")][v["service"]] += 1
    out = {c: n.most_common(1)[0][0] for c, n in by.items()}
    for c, s in NEW_CONTRACT_SERVICE.items():
        out.setdefault(c, s)
    return out


def stores_by_contract(stored: dict) -> dict:
    """Which datastores a contract's operations touch — same reasoning as the service."""
    import collections
    by = collections.defaultdict(collections.Counter)
    for v in stored.values():
        for st in (v.get("stores") or []):
            by[v.get("contract")][st] += 1
    out = {c: sorted(n) for c, n in by.items()}
    # Same gap as the service, and the same fix: a brand-new contract has no neighbours to read
    # from. Every one of the five writes relational state and caches, which is what every other
    # contract in the package does.
    for c in NEW_CONTRACT_SERVICE:
        out.setdefault(c, ["postgres", "redis"])
    return out


def derive(stored: dict) -> dict:
    persist = persistence_map()
    svc = service_by_contract(stored)
    sto = stores_by_contract(stored)
    out = {}
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        contract = c.stem
        for path, item in (doc.get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                aud = op.get("x-ticvai-audience")
                out[op["operationId"]] = {
                    "contract": contract,
                    "verb": verb.upper(),
                    "path": path,
                    "reads": tables_in(op.get("responses"), persist),
                    "writes": tables_in(op.get("requestBody"), persist),
                    "routing": op.get("x-ticvai-read-routing"),
                    "scope": op.get("x-ticvai-scope-level"),
                    "perm": op.get("x-ticvai-permission"),
                    "offline": bool(op.get("x-ticvai-offline-capable")),
                    "summary": op.get("summary") or op["operationId"],
                    "source": "derived",
                    "audience": list(aud) if isinstance(aud, list) else ([aud] if aud else []),
                    "service": svc.get(contract),
                    "stores": sto.get(contract, ["postgres"]),
                }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--audit", action="store_true",
                    help="report where the stored entries and the contracts disagree")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    stored = json.loads(LINEAGE.read_text(encoding="utf-8")) if LINEAGE.exists() else {}
    fresh = derive(stored)
    missing = sorted(set(fresh) - set(stored))
    orphan = sorted(set(stored) - set(fresh))

    print("%d operations in the contracts · %d in the lineage" % (len(fresh), len(stored)))
    print("  in the contracts and not the lineage   %4d" % len(missing))
    print("  in the lineage and not the contracts   %4d" % len(orphan))
    for o in missing[:12]:
        print("     + %-32s %s" % (o, fresh[o]["contract"]))
    for o in orphan[:8]:
        print("     - %-32s %s" % (o, stored[o].get("contract")))

    if a.audit:
        # **Only reported, never applied.** A disagreement here is as likely to be a judgement the
        # dump made and the contract does not carry as it is to be staleness.
        fields = ("contract", "verb", "path", "routing", "scope", "perm", "reads", "writes")
        diffs = 0
        for o in sorted(set(stored) & set(fresh)):
            bad = [f for f in fields if stored[o].get(f) != fresh[o].get(f)]
            if bad:
                diffs += 1
                if diffs <= 15:
                    print("     ~ %-30s %s" % (o, ", ".join(bad)))
        print("  entries whose stored value differs from the contract  %d" % diffs)

    # **`--apply` adds and never updates, which is right and has one sharp edge.** An operation
    # written once with a null `service` keeps it forever: the next run sees the key present and
    # leaves it alone. On 19 September that happened to 133 operations across four new contracts,
    # and `derive-diagrams.py` then sorted a set containing `None` and stopped the whole refresh —
    # twice, because re-running the pipeline could not repair what re-running does not touch.
    #
    # So a null `service` or empty `stores` is repairable in place. Nothing else is: a stored value
    # that disagrees with the contract is a judgement somebody made, and `--audit` reports it
    # rather than overwriting it.
    repaired = 0
    if a.apply:
        for o in sorted(set(stored) & set(fresh)):
            if not stored[o].get("service") and fresh[o].get("service"):
                stored[o]["service"] = fresh[o]["service"]
                repaired += 1
            if not stored[o].get("stores") and fresh[o].get("stores"):
                stored[o]["stores"] = fresh[o]["stores"]
    if repaired:
        print("  repaired %d entry(s) that had no service" % repaired)

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    if not missing and not repaired:
        print("  nothing to add")
        return 0
    for o in missing:
        stored[o] = fresh[o]
    LINEAGE.write_text(json.dumps(stored, indent=1, ensure_ascii=False), encoding="utf-8")
    print("  added %d · %d operations total -> handoff/%s" % (len(missing), len(stored),
                                                              LINEAGE.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
