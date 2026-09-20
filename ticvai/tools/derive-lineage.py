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


def schema_defs() -> dict:
    """Schema name -> its definition, across every contract, so a `$ref` can be followed."""
    out = {}
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for n, sch in ((doc.get("components") or {}).get("schemas") or {}).items():
            out.setdefault(n, sch)
    return out


def persistence_map() -> dict:
    """Schema name -> the table(s) it persists to, across every contract."""
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
            # **A schema may persist to more than one table and twenty-four of them do.**
            # `x-ticvai-persistence: orders.sales_order + orders.order_line` is an order and its
            # lines returned as one object. Taken whole it is a table name with a plus sign in
            # it, which is in no schema reference and which `derive-schema` would then rebuild
            # as a real table from these very entries.
            #
            # This was invisible while `tables_in` looked one level deep: the stored entries were
            # hand-mapped with the tables split correctly, and nothing re-derived them. Following
            # refs reached the composed schemas and put the unsplit string into six operations
            # before `check-lineage` caught it.
            parts = [x.strip() for x in t.split("+") if x.strip() and "." in x]
            if parts:
                out[n] = parts
    return out


def tables_in(node, persist: dict, defs: dict = None, depth: int = 6) -> list:
    """Every persisted table reachable from a `$ref` inside this node.

    **This said "reachable" and only looked one level deep.** A response that returns a composed
    schema — `WorkforceEmployeeProfile`, `TenantConfig`, `BundleDetail` — has one `$ref` in the
    operation and the tables underneath it, and reading only the operation node found the wrapper,
    which persists nothing, and stopped.

    **151 operations under-reported, 217 table mentions missing.** `getTenantConfig` returns the
    feature toggles, the homepage sections and the module enablement and named none of them;
    `getEmployee` returned a profile over five tables and derived an empty read set.

    The refs are followed to a fixed point, with a depth bound because a schema may legitimately
    refer to itself — a category with a parent, a scope with a parent — and a self-reference adds
    no table the first visit did not.
    """
    refs = set(re.findall(r"#/components/schemas/([A-Za-z0-9_]+)", json.dumps(node or {})))
    if defs:
        seen, frontier = set(refs), set(refs)
        for _ in range(depth):
            nxt = set()
            for n in frontier:
                if n in defs:
                    nxt |= set(re.findall(r"#/components/schemas/([A-Za-z0-9_]+)",
                                          json.dumps(defs[n])))
            nxt -= seen
            if not nxt:
                break
            seen |= nxt
            frontier = nxt
        refs = seen
    return sorted({t for r in refs if r in persist for t in persist[r]})


# **A contract with no stored entry needs a person, and on 19 September five arrived at once.**
# The inference below reads the service off a contract's existing neighbours, which cannot work for
# a contract that has none — `derive-diagrams.py` then sorted a set containing `None` and stopped
# the whole refresh. These are the decisions, made once, in the same terms the existing ones use.
NEW_CONTRACT_SERVICE = {
    # Rental is venue floor operations — check-out, condition, return — beside `resources`,
    # `maintenance` and `games`, which are all VenueOps.
    "rental": "VenueOpsService",
    # **Wallet is its own service as of 19 September.** The first cut sent it to Retail on the
    # grounds that retail owned the balance — it did, and that was the bug: 13 of retail's 37
    # operations were the wallet runtime while `wallet.yaml` held only the rules. They are now
    # together in `wallet.yaml`, and the reason it is not inside Retail either is that eight
    # domains need a wallet. A Gold Membership issues F&B credit, parking credits and ride
    # credits into one wallet, so subscription, games and F&B all read it.
    "wallet": "WalletService",
    # Payment orchestration routes and settles, which is the Order service's existing work —
    # `createPayment` and `capturePayment` are already there.
    "payments": "OrderService",
    # **Not AccessService, though the read does happen at a turnstile.** AccessService is
    # "read-heavy, extreme latency sensitivity, edge-cached" — 30 operations on the scan path.
    # Accreditation is a back-office apply/review/approve/issue workflow whose writes would
    # invalidate those caches and whose deploys would restart the gates. TenancyService already
    # holds `workforce` and `approvals`; accreditation is an approvals workflow about people.
    "accreditation": "TenancyService",
}


def service_by_contract(stored: dict) -> dict:
    """Which service serves each contract, taken from the entries that already exist.

    **`service` is a deployment decision, not a contract fact**, so it cannot be read off the
    OpenAPI — and `derive-diagrams.py` indexes screens by it and raises `KeyError` without it.
    Every contract in the package already has operations assigned to a service, so the answer is
    the service its neighbours use; a contract with no stored entry at all is in
    `NEW_CONTRACT_SERVICE` above.

    **`handoff/service-decomposition.json` is the authority, and learning is the fallback.**
    The first version learned the mapping from the entries that already existed, which reads
    well until a contract moves service: the stored entries say the old service, the learned
    map agrees with them because they *are* the training data, and the answer is stable and
    wrong forever. On 19 September `wallet` became its own service and all 48 of its operations
    went on reporting `RetailService`, because every one of them voted for it.

    So the decomposition — which is where the deployment decision is actually recorded — is read
    first. Learning still covers any contract it has not heard of, and `NEW_CONTRACT_SERVICE`
    covers a contract with no neighbours at all.
    """
    import collections
    out = {}
    try:
        dec = json.loads((ROOT / "handoff" / "service-decomposition.json")
                         .read_text(encoding="utf-8"))
        for name, s in (dec.get("services") or {}).items():
            for c in (s.get("contracts") or []):
                out[c] = name
    except Exception:
        pass
    by = collections.defaultdict(collections.Counter)
    for v in stored.values():
        if v.get("service"):
            by[v.get("contract")][v["service"]] += 1
    for c, n in by.items():
        out.setdefault(c, n.most_common(1)[0][0])
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
    defs = schema_defs()
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
                    "reads": tables_in(op.get("responses"), persist, defs),
                    "writes": tables_in(op.get("requestBody"), persist, defs),
                    # Kept only long enough for the repair below to tell which tables are new
                    # *because refs are now followed*, and stripped before anything is written.
                    "_direct_reads": tables_in(op.get("responses"), persist),
                    "_direct_writes": tables_in(op.get("requestBody"), persist),
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
    #
    # **One more thing is a fact rather than a judgement: which contract defines an operation.**
    # On 19 September 15 operations moved from `retail.yaml` and `games.yaml` into `wallet.yaml`
    # — the wallet runtime, which had been living apart from the wallet rules. Their stored
    # entries still said `retail`, and therefore still said `RetailService`, and no amount of
    # re-running would have changed either: the key was present, so `--apply` left it. An
    # operation's owning contract is read straight off the file that declares it, so when the
    # two disagree the stored one is simply out of date, and the service inferred from it with
    # it. A hand-narrowed `audience` or a deliberate service override is still left alone.
    repaired = moved = rehomed = followed = 0
    svc = service_by_contract(stored)
    if a.apply:
        # **The one repair to an existing entry's reads and writes, and it is narrow on purpose.**
        # Until 20 September `tables_in` looked one level deep, so an operation returning a
        # composed schema recorded the wrapper's tables and not the ones underneath. The repair
        # adds ONLY the tables that appear because refs are now followed — the difference between
        # the transitive walk and the old direct one.
        #
        # **Nothing is ever removed and no other difference is touched.** A stored set that
        # disagrees with the contract for any other reason is a judgement somebody made, and
        # `--audit` reports it rather than overwriting it. This fixes a derivation that was
        # incomplete, not a decision that was wrong.
        for o in sorted(set(stored) & set(fresh)):
            for key, direct_key in (("reads", "_direct_reads"), ("writes", "_direct_writes")):
                gained = set(fresh[o].get(key) or []) - set(fresh[o].get(direct_key) or [])
                add = sorted(gained - set(stored[o].get(key) or []))
                if add:
                    stored[o][key] = sorted(set(stored[o].get(key) or []) | set(add))
                    followed += len(add)
        for o in sorted(set(stored) & set(fresh)):
            if not stored[o].get("service") and fresh[o].get("service"):
                stored[o]["service"] = fresh[o]["service"]
                repaired += 1
            if not stored[o].get("stores") and fresh[o].get("stores"):
                stored[o]["stores"] = fresh[o]["stores"]
            # **A service named in the decomposition is a decision, not a guess.** An operation
            # whose contract has not moved can still change service, because the service it
            # deploys to is recorded in `service-decomposition.json` and that file is edited by
            # a person. When the two disagree, the file wins — otherwise the 33 configuration
            # operations already in `wallet.yaml` would keep reporting `RetailService` while
            # the 15 that moved into it reported `WalletService`, and one contract would be
            # split across two services in the diagrams.
            want = svc.get(fresh[o].get("contract") or stored[o].get("contract"))
            if want and stored[o].get("service") not in (None, want):
                stored[o]["service"] = want
                rehomed += 1
            if fresh[o].get("contract") and stored[o].get("contract") != fresh[o]["contract"]:
                print("     moved %-28s %s -> %s" % (o, stored[o].get("contract"),
                                                     fresh[o]["contract"]))
                stored[o]["contract"] = fresh[o]["contract"]
                if fresh[o].get("service"):
                    stored[o]["service"] = fresh[o]["service"]
                moved += 1
    if followed:
        print("  %d table mention(s) added to existing entries by following refs into composed "
              "schemas" % followed)
    if repaired:
        print("  repaired %d entry(s) that had no service" % repaired)
    if moved:
        print("  re-attributed %d operation(s) that changed contract" % moved)
    if rehomed:
        print("  moved %d operation(s) to the service the decomposition names" % rehomed)

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    if not missing and not repaired and not moved and not rehomed and not followed:
        print("  nothing to add")
        return 0
    for o in missing:
        stored[o] = {k: v for k, v in fresh[o].items() if not k.startswith("_")}
    LINEAGE.write_text(json.dumps(stored, indent=1, ensure_ascii=False), encoding="utf-8")
    print("  added %d · %d operations total -> handoff/%s" % (len(missing), len(stored),
                                                              LINEAGE.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
