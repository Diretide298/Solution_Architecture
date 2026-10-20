#!/usr/bin/env python3
"""Derive `handoff/api-data-lineage.json` from the contracts and a short list of overrides.

**Since 20 October 2026 the lineage is derived, not hand-kept** (the lead: "contracts are the single source;
generators derive everything and never write back"; CHG-R8GEN-001). Until then this tool only added operations the
file did not have and left every existing entry alone, on the reasoning that the 1,032 entries of the dump carried
judgements a derivation could not reproduce. The cost of that was a file nobody could correct by changing a contract:
178 entries named a permission the contract no longer required, 36 a readVia the contract had changed, six operations
were missing, and every r8 lineage cause had to be a hand edit that the next rename would leave behind.

So every run now writes, for every operation a contract declares:

  `reads`   the tables behind the schemas it returns, `cache:idempotency` when it takes the Idempotency-Key header
  `writes`  the tables behind the schema it accepts (and the line table its body's lines land in, `child_writes`),
            what a 201 creates, what a write with no stored body returns, `platform.outbox` for an emitter, the
            change-log table `x-ticvai-config-change-log` names, `cache:idempotency` as for reads, the audit row for
            `x-ticvai-audits-itself`, and the tables `x-ticvai-reads` / `x-ticvai-writes` name (`{table, for}`)
  `readVia`, `writeVia`, `contract`, `verb`, `path`, `routing`, `scope`, `perm`, `offline`, `summary`, `audience`
            straight off the operation
  plus and minus `handoff/api-data-lineage-overrides.json`: what no contract fact can state, each entry with its
  reason. The entries carried from the hand-kept file on 20 October are marked `carried` and may only fall
  (check-lineage LN-OVERRIDE); a new one is added by hand with its own reason. `service` comes from
  service-decomposition.json; notes, `pure`, `storageUndecided` and `readColumns` (derive-read-columns) are kept.

An operation no contract declares leaves the lineage. The output depends only on the contracts and the override
list, so a second run changes nothing (check-lineage LN-DERIVED compares the file with this derivation).

Run: `python3 tools/derive-lineage.py [--apply] [--audit]`; `--seed-overrides` wrote the carried list once and
refuses to run again.
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


_DOCS = None


def contract_docs() -> list:
    """Every contract, parsed once: `(path, document)` in file order.

    **Parsed once, with the C loader where it exists** (20 October 2026, CHG-R8GEN-001). The four passes below each
    parsed all 40 contracts with the pure-Python loader, about seventy seconds a run; check-lineage now runs this
    derivation to compare against it (LN-DERIVED), so it has to be cheap enough to run twice.
    """
    global _DOCS
    if _DOCS is None:
        loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
        _DOCS = []
        for c in sorted((ROOT / "contracts").rglob("*.yaml")):
            try:
                doc = yaml.load(c.read_text(encoding="utf-8"), Loader=loader) or {}
            except yaml.YAMLError:
                continue
            _DOCS.append((c, doc))
    return _DOCS


def schema_defs() -> dict:
    """Schema name -> its definition, across every contract, so a `$ref` can be followed."""
    out = {}
    for c, doc in contract_docs():
        for n, sch in ((doc.get("components") or {}).get("schemas") or {}).items():
            out.setdefault(n, sch)
    return out


def persistence_map() -> dict:
    """Schema name -> the table(s) it persists to, across every contract."""
    out = {}
    for c, doc in contract_docs():
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


_VALID_TABLE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


def _snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _local_ref(node) -> str | None:
    r = (node or {}).get("$ref") if isinstance(node, dict) else None
    m = re.match(r"^#/components/schemas/([A-Za-z0-9_]+)$", r or "")
    return m.group(1) if m else None


def body_arrays(node, persist: dict, defs: dict, depth: int = 4) -> set:
    """Names of the array-of-object properties a request body carries.

    Walks inline objects, `allOf`/`oneOf`/`anyOf`, and `$ref`s to schemas that persist to
    nothing themselves (a `Create…Request`, a `JournalLine` item). A persisted schema is not
    walked: its tables are already reported by `tables_in`.
    """
    out = set()
    if depth <= 0 or not isinstance(node, dict):
        return out
    if "content" in node:           # the requestBody object itself
        for media in (node.get("content") or {}).values():
            out |= body_arrays((media or {}).get("schema"), persist, defs, depth)
        return out
    n = _local_ref(node)
    if n:
        if n in persist or n not in defs:
            return out
        return body_arrays(defs[n], persist, defs, depth - 1)
    for k in ("allOf", "oneOf", "anyOf"):
        for sub in node.get(k) or []:
            out |= body_arrays(sub, persist, defs, depth - 1)
    for pname, p in (node.get("properties") or {}).items():
        if not isinstance(p, dict):
            continue
        if p.get("type") == "array" and isinstance(p.get("items"), dict):
            it = p["items"]
            iname = _local_ref(it)
            if iname in persist:
                continue            # a persisted item schema is already a write via tables_in
            if iname or it.get("type") == "object" or it.get("properties"):
                out.add(pname)
        elif p.get("type") == "object" or p.get("properties") or p.get("allOf"):
            out |= body_arrays(p, persist, defs, depth - 1)
    return out


def child_writes(op: dict, path: str, persist: dict, defs: dict, known: set) -> list:
    """The line table a request body writes when the lines are not a persisted `$ref`.

    **`tables_in` only sees persisted `$ref`s, and a body's lines are usually neither.**
    `createJournalEntry` accepts `CreateJournalEntryRequest`, which persists nothing, with
    `lines: JournalLine[]`, which persists nothing either — the lines are stored as part of
    `JournalEntry` (`ledger.journal_entry + ledger.journal_line`). `submitCountLines` has an
    inline body of `lines` against `/stock-counts/{countId}`. Both derived no line-table write,
    and the pull audit of 26 September then read "nothing writes `journal_line`" as a missing
    operation when the operation was there all along.

    The line table is found from facts the contract states, never guessed into existence:
    the parent is a table the operation is about — the head table of a persisted schema it
    returns or accepts, or the table a `{xId}` path parameter names — and the child is
    `<parent prefix>_<singular array name>` **only if some schema already persists to it**.
    """
    arrays = body_arrays(op.get("requestBody"), persist, defs)
    if not arrays:
        return []
    parents = set()
    refs = set(re.findall(r"#/components/schemas/([A-Za-z0-9_]+)",
                          json.dumps([op.get("responses") or {}, op.get("requestBody") or {}])))
    for r in refs:
        if r in persist:
            parents.add(persist[r][0])
    # **A path parameter names a table in the operation's own schemas, not any table of that name** (12 October 2026,
    # CHG-R6-021). `issueCreditMemo` is `/tax-invoices/{invoiceId}/credit-memos` and returns `ledger.credit_memo`;
    # `{invoiceId}` matched `control.invoice`, the platform's subscription invoice in the control database, and its
    # body's `lines` became a write of `control.invoice_line` from a ledger operation (ADAM CR-002 found it as a
    # cross-deployable write). Where the operation's persisted refs name schemas, a parameter's table must be in one.
    own = {p.split(".", 1)[0] for p in parents}
    for pm in re.findall(r"\{([A-Za-z0-9_]+?)Id\}", path):
        short = _snake(pm)
        named = {t for t in known if t.split(".", 1)[1] == short}
        if own:
            named = {t for t in named if t.split(".", 1)[0] in own}
        parents |= named
    out = set()
    for arr in arrays:
        sing = _snake(arr)
        sing = sing[:-3] + "y" if sing.endswith("ies") else (sing[:-1] if sing.endswith("s") else sing)
        for parent in parents:
            schema, name = parent.split(".", 1)
            toks = name.split("_")
            for k in range(len(toks), 0, -1):
                cand = "%s.%s_%s" % (schema, "_".join(toks[:k]), sing)
                if cand in known:
                    out.add(cand)
                    break
    return sorted(out)


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
    # **Transport ticketing is VenueOps, beside rental and queue** (decided 29 September, rev 3
    # REV3-21). It owns stations, routes, timetables, fares, passes and favourites; the sale runs
    # through catalogue and orders (a departure is a performance, a pass an openDated product),
    # so it is not on the sale path, it is venue-scoped, and it is licensed as an optional module.
    "transport": "VenueOpsService",
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


def event_emitters() -> set:
    """**An operation that emits an event writes the outbox** (3 October 2026, CHG-R1S-005). The event is
    written to `platform.outbox` in the same transaction as the change it reports, so the outbox is one of
    the operation's writes. The HLD/LLD cross-check found ten emitters, `createOrder` among them, whose
    lineage left it out; the emitters are `emittedBy` in `events/` and `x-ticvai-emits` on the operation."""
    out = set()
    for f in sorted((ROOT / "events").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        try:
            e = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        out |= {str(o).split(".")[-1] for o in e.get("emittedBy") or []}
    return out


def derive(stored: dict) -> dict:
    emitting = event_emitters()
    persist = persistence_map()
    defs = schema_defs()
    svc = service_by_contract(stored)
    sto = stores_by_contract(stored)
    known = {t for ts in persist.values() for t in ts}
    out = {}
    for c, doc in contract_docs():
        contract = c.stem
        for path, item in (doc.get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                aud = op.get("x-ticvai-audience")
                body_writes = (set(tables_in(op.get("requestBody"), persist, defs))
                               | set(child_writes(op, path, persist, defs, known)))
                # **A new write whose body is not the record writes what it returns** (CHG-GTRB-004). A body of a
                # few inline fields (`setVenueMapArtwork` sends `baseAssetId` and alignment points, returns the
                # `VenueMap` it changed) derived no table, and check-write-lineage failed the r1 merge refresh on it
                # (W-NOTABLE). The one-off of CHG-R1S-005 gave the stored entries the same reading: "the table the
                # operation changes, read off its response schema's persistence". Kept apart as `_response_writes`
                # and used only for an operation the lineage does not have yet: a stored entry's writes, `pure` and
                # `storageUndecided` are judgements the ref-following repair below must not widen.
                response_writes = []
                if verb != "get" and not body_writes:
                    response_writes = sorted(tables_in({c: r for c, r in (op.get("responses") or {}).items()
                                                        if str(c).startswith("2")}, persist, defs))
                # **A 201 creates what it returns** (4 October 2026, CHG-FXC-002). `recordWriteOff` answers 201 with
                # the JournalEntry it posted and its lineage wrote only `ledger.posting`; `createPlan` returns the plan
                # with its modules and never wrote `subscription.plan_module`; `topUpWallet` creates a credit lot it did
                # not list. A 201 response is a created row by definition, so the tables its schema persists to
                # (directly, not through refs into neighbours) are writes, for new and existing entries alike.
                created = (set(tables_in({c: r for c, r in (op.get("responses") or {}).items() if str(c) == "201"},
                                         persist)) if verb != "get" else set())
                # **Two writes every operation of a kind makes, read off the contract** (20 October 2026, CHG-R8GEN-001).
                # A write that takes the shared `Idempotency-Key` header dedups on `cache:idempotency` (common.yaml: a
                # replay gets the stored first answer), unless it says `x-ticvai-idempotency-exempt`; an operation with
                # `x-ticvai-config-change-log` appends the change-log row that extension names. Both were kept by hand
                # in the lineage (1,110 and 84 entries) and missing from about 430 operations that take the header.
                ruled_r, ruled_w = set(), set()
                if _idempotent(op, item):
                    ruled_r.add("cache:idempotency")
                    ruled_w.add("cache:idempotency")
                ruled_w |= {x for x in _TABLE_TEXT.findall(str(op.get("x-ticvai-config-change-log") or ""))
                            if x in known}
                # An operation that writes its own audit row says so (x-ticvai-audits-itself, r8 cause
                # FOUNDATION-AI-C49, CHG-R8GEN-012); the kernel interceptor skips it, and the row is its write.
                if op.get("x-ticvai-audits-itself") and verb != "get":
                    ruled_w.add("platform.audit_record")
                # **A table the operation reads or writes that no schema it takes or returns persists to** (20 October
                # 2026, CHG-R8GEN-014): `x-ticvai-reads` / `x-ticvai-writes`, a list of `{table, for}` (or bare table
                # names) in the operation's own module. It is how a carried override becomes a contract fact: once the
                # contract says it, derive-lineage --audit lists the override as redundant and it is removed. A read of
                # another module's table is never this: it is an x-ticvai-read-via to the owner's query.
                for key, into in (("x-ticvai-reads", ruled_r), ("x-ticvai-writes", ruled_w)):
                    for x in op.get(key) or []:
                        tb = str(x.get("table") if isinstance(x, dict) else x).strip()
                        if tb in known:
                            into.add(tb)
                out[op["operationId"]] = {
                    "contract": contract,
                    "verb": verb.upper(),
                    "path": path,
                    "reads": sorted(set(tables_in(op.get("responses"), persist, defs)) | ruled_r),
                    "writes": sorted(body_writes | created | ruled_w
                                     | ({"platform.outbox"} if (op["operationId"] in emitting
                                        or op.get("x-ticvai-emits")) and contract != "ai" else set())),
                    # Kept only long enough for the repair below to tell which tables are new
                    # *because refs are now followed*, and stripped before anything is written.
                    "_old_reads": tables_in(op.get("responses"), persist, defs),
                    "_old_writes": sorted(body_writes | created
                                          | ({"platform.outbox"} if (op["operationId"] in emitting
                                             or op.get("x-ticvai-emits")) and contract != "ai" else set())),
                    "_direct_reads": tables_in(op.get("responses"), persist),
                    "_direct_writes": tables_in(op.get("requestBody"), persist),
                    "_response_writes": response_writes,
                    "routing": op.get("x-ticvai-read-routing"),
                    "scope": op.get("x-ticvai-scope-level"),
                    "perm": op.get("x-ticvai-permission"),
                    "offline": bool(op.get("x-ticvai-offline-capable")),
                    "summary": op.get("summary") or op["operationId"],
                    "source": "derived",
                    "_declared": bool(op.get("x-ticvai-reads") or op.get("x-ticvai-writes")),
                    "audience": list(aud) if isinstance(aud, list) else ([aud] if aud else []),
                    "service": svc.get(contract),
                    "stores": sto.get(contract, ["postgres"]),
                }
                # **A write into another deployable's schema names the route it takes** (12 October 2026, ADAM
                # CR-002, CHG-R6-020). DB-ROLES grants each deployable's role DML only on its own modules' schemas, so
                # PostgreSQL refuses such a write made with the caller's own SQL; ADR-0055 rule 4 sends it by event or
                # by the owner's published operation, and `x-ticvai-write-via` on the operation says which. A fact
                # read off the contract, so it is copied as `writeVia` onto new and existing entries alike, below.
                via = write_via(op)
                if via:
                    out[op["operationId"]]["writeVia"] = via
                # **A rule question asked of another module names the query it asks** (14 October 2026, CHG-GEN-009,
                # ADR-0055 amended 14 October). `x-ticvai-read-via` on the operation names the owner's declared query
                # (`x-ticvai-queries` in the owner's contract) and the route it takes; copied as `readVia`, like
                # `writeVia`.
                rvia = read_via(op)
                if rvia:
                    out[op["operationId"]]["readVia"] = rvia
    return out


_TABLE_TEXT = re.compile(r"\b([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)\b")


def _idempotent(op: dict, item: dict) -> bool:
    """The operation takes the shared `Idempotency-Key` header and does not say it is exempt."""
    if op.get("x-ticvai-idempotency-exempt"):
        return False
    for p in list(op.get("parameters") or []) + list((item or {}).get("parameters") or []):
        if not isinstance(p, dict):
            continue
        if str(p.get("$ref") or "").endswith("/IdempotencyKey") or str(p.get("name") or "") == "Idempotency-Key":
            return True
    return False


def read_via(op: dict) -> list:
    """`x-ticvai-read-via` as the lineage records it: one `{query, route, for}` per question asked of another module."""
    out = []
    for r in op.get("x-ticvai-read-via") or []:
        if isinstance(r, dict) and r.get("query"):
            out.append({k: str(r[k]) for k in ("query", "route", "for") if r.get(k)})
    return sorted(out, key=lambda r: (r["query"], r.get("for", "")))


def write_via(op: dict) -> list:
    """`x-ticvai-write-via` as the lineage records it: one `{table, event}` or `{table, operation}` per routed table."""
    out = []
    for w in op.get("x-ticvai-write-via") or []:
        if isinstance(w, dict) and w.get("table"):
            out.append({k: str(w[k]) for k in ("table", "event", "operation") if w.get(k)})
    return sorted(out, key=lambda w: w["table"])


OVERRIDES = ROOT / "handoff" / "api-data-lineage-overrides.json"

# The fields of an entry that are contract facts: re-read from the contract on every run (CHG-R8GEN-001). `audience` and
# `perm` were left alone as "judgements" until r8, and 178 entries named a permission the contract no longer required.
CONTRACT_FIELDS = ("contract", "verb", "path", "routing", "scope", "perm", "offline", "summary", "audience")

CARRIED_REASON = ("hand-kept in the lineage before r8; no contract fact states it yet (carried 20 October 2026, "
                  "CHG-R8GEN-001)")


def load_overrides(path: Path = OVERRIDES) -> dict:
    """`handoff/api-data-lineage-overrides.json`: what the contracts cannot state, one entry per operation.

    `reads`/`writes` add tables, `notReads`/`notWrites` remove ones the contract derives, `stores` replaces the
    entry's datastores (a generated file, say), `reason` says why. An entry
    with `carried: true` was copied from the hand-kept lineage when it became derived (20 October 2026); their number
    may only fall (`carriedCeiling`, check-lineage LN-OVERRIDE). Authored by hand; nothing in the refresh writes it."""
    if not path.exists():
        return {"operations": {}}
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc.setdefault("operations", {})
    return doc


def _same(a, b) -> bool:
    if isinstance(a, list) or isinstance(b, list):
        return sorted(a or []) == sorted(b or [])
    return (a if a not in ("", None) else None) == (b if b not in ("", None) else None)


def expected(stored: dict, fresh: dict, overrides: dict, stale: list = None) -> dict:
    """The lineage the contracts and the override list give, keeping each stored entry's annotations.

    **The contract is the source** (the lead, 20 October 2026: "contracts are the single source; generators derive
    everything and never write back"). For every operation a contract declares: the contract facts
    (`CONTRACT_FIELDS`, `readVia`, `writeVia`) are read off it; `reads` and `writes` are the tables its schemas persist
    to and the rule-derived ones (`derive`), plus and minus the override list; `cache` is the resolution-cache rule.
    `service` is the decomposition's (a deployment decision), `stores` is kept where set. What only a person can say
    (notes, `pure`, `storageUndecided`, `readColumns`, which derive-read-columns refreshes next) is carried as it is.
    An operation no contract declares is not in the result. The result depends on the contracts and the overrides
    only, so a second run over its own output gives the same file.
    """
    ops = overrides.get("operations") or {}
    svc = service_by_contract(stored)
    order = [o for o in stored if o in fresh] + [o for o in fresh if o not in stored]
    out = {}
    for o in order:
        f = fresh[o]
        new = o not in stored
        e = {k: v for k, v in f.items() if not k.startswith("_")} if new else json.loads(json.dumps(stored[o]))
        for k in CONTRACT_FIELDS:
            if not _same(e.get(k), f.get(k)):
                e[k] = f.get(k)
        want = svc.get(f.get("contract"))
        if want:
            e["service"] = want
        elif not e.get("service"):
            e["service"] = f.get("service")
        if not e.get("stores"):
            e["stores"] = f.get("stores") or ["postgres"]
        ov = ops.get(o) or {}
        if ov.get("stores"):
            e["stores"] = list(ov["stores"])     # where the operation's data lives, when no table says it
        reads = set(f.get("reads") or [])
        writes = set(f.get("writes") or []) | set(f.get("_response_writes") or [])
        if e.get("pure"):
            # A `pure` entry writes nothing, whatever its body refs (CHG-FXC-004); a cache it fills is not a table.
            writes = {t for t in writes if ":" in t}
        reads = (reads | set(ov.get("reads") or [])) - set(ov.get("notReads") or [])
        writes = (writes | set(ov.get("writes") or [])) - set(ov.get("notWrites") or [])
        # A name that is not `<schema>.<table>` is not a table (SD-007).
        e["reads"] = sorted(t for t in reads if ":" in t or _VALID_TABLE.match(t))
        e["writes"] = sorted(t for t in writes if ":" in t or _VALID_TABLE.match(t))
        for key in ("writeVia", "readVia"):
            if f.get(key):
                e[key] = f[key]
            else:
                e.pop(key, None)
        # **A path-inferred entry stops being one when somebody states its tables** (r8 walk, 20 October 2026,
        # CHG-R8WFC-004). `source` was carried from the hand-kept file, so 86 entries still said "path-inferred" (tables
        # guessed from the URL) after their contract or a reviewed override had stated them, and the developer could
        # not tell a guess from a decision. It is relabelled once the operation declares x-ticvai-reads /
        # x-ticvai-writes, or its override is a reviewed one (not `carried`); check-lineage LN-PATH-INFERRED counts
        # what is left.
        if e.get("source") == "path-inferred":
            if f.get("_declared") or (ov and not ov.get("carried")):
                e["source"] = "declared (contract x-ticvai-reads/x-ticvai-writes or a reviewed override; r8 walk fix)"
            elif not ov:
                e["source"] = "derived"         # nothing but the contract's schemas gives its tables now
        out[o] = e
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("resolution_cache", ROOT / "tools" / "resolution_cache.py")
    _rc = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_rc)
    for o in out:
        want = _rc.resolution_cache(o, out[o], out)
        if want:
            out[o]["cache"] = want
        else:
            out[o].pop("cache", None)
    if stale is not None:
        stale.extend(sorted(set(ops) - set(fresh)))
    return out


def seed_overrides(stored: dict, fresh: dict) -> dict:
    """The override list that reproduces today's hand-kept reads and writes: run once, when the lineage became
    derived (20 October 2026). Each entry's reason is the entry's own note where it has one."""
    ops = {}
    for o in stored:
        if o not in fresh:
            continue
        f = fresh[o]
        base_w = set(f.get("writes") or []) | set(f.get("_response_writes") or [])
        if stored[o].get("pure"):
            base_w = {t for t in base_w if ":" in t}
        add_r = sorted(set(stored[o].get("reads") or []) - set(f.get("reads") or []))
        add_w = sorted(set(stored[o].get("writes") or []) - base_w)
        # Only a removal of what the old derivation gave: the two rules added on 20 October (idempotency, change
        # log) are contract facts the hand-kept file had missed, so they are applied, not seeded away.
        old_r = set(f.get("_old_reads") or [])
        old_w = set(f.get("_old_writes") or []) | set(f.get("_response_writes") or [])
        if stored[o].get("pure"):
            old_w = {t for t in old_w if ":" in t}
        not_r = sorted(old_r - set(stored[o].get("reads") or []))
        not_w = sorted(old_w - set(stored[o].get("writes") or []))
        if not (add_r or add_w or not_r or not_w):
            continue
        notes = [str(stored[o][k]) for k in ("lineageNote", "writesNote", "fixNote", "note") if stored[o].get(k)]
        e = {}
        for k, v in (("reads", add_r), ("writes", add_w), ("notReads", not_r), ("notWrites", not_w)):
            if v:
                e[k] = v
        e["reason"] = ("; ".join(notes) + " (" + CARRIED_REASON + ")") if notes else CARRIED_REASON
        e["carried"] = True
        ops[o] = e
    return {
        "about": "What the contracts cannot state about an operation's tables, one entry per operation, each with "
                 "its reason. tools/derive-lineage.py adds `reads`/`writes` to what the contract derives and takes "
                 "`notReads`/`notWrites` away. Authored by hand: nothing in the refresh writes it. An entry marked "
                 "`carried` was copied from the hand-kept lineage when it became derived (20 October 2026, "
                 "CHG-R8GEN-001); their number may only fall (carriedCeiling, check-lineage LN-OVERRIDE). To change "
                 "an operation's tables, change its contract (a persisted schema, x-ticvai-read-via, "
                 "x-ticvai-write-via, x-ticvai-config-change-log); add an override only for what no contract fact "
                 "can say, with a reason, and without `carried`.",
        "carriedCeiling": len(ops),
        "operations": {o: ops[o] for o in sorted(ops)},
    }


def write_json(path: Path, doc) -> None:
    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write handoff/api-data-lineage.json")
    ap.add_argument("--audit", action="store_true",
                    help="report what the override list holds and what it no longer needs")
    ap.add_argument("--seed-overrides", action="store_true",
                    help="once: write the override list that reproduces the hand-kept lineage (refuses if it exists)")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    stored = json.loads(LINEAGE.read_text(encoding="utf-8")) if LINEAGE.exists() else {}
    fresh = derive(stored)
    if a.seed_overrides:
        if OVERRIDES.exists():
            print("FAIL - %s exists; it is authored now, edit it by hand" % OVERRIDES.relative_to(ROOT))
            return 1
        doc = seed_overrides(stored, fresh)
        write_json(OVERRIDES, doc)
        print("  seeded %d override entr(ies) -> %s" % (len(doc["operations"]), OVERRIDES.relative_to(ROOT)))
        return 0
    overrides = load_overrides()
    stale = []
    want = expected(stored, fresh, overrides, stale)
    missing = sorted(set(want) - set(stored))
    orphan = sorted(set(stored) - set(want))
    changed = sorted(o for o in set(want) & set(stored) if want[o] != stored[o])
    print("%d operations in the contracts · %d in the lineage · %d override entries"
          % (len(fresh), len(stored), len(overrides.get("operations") or {})))
    print("  in the contracts and not the lineage   %4d" % len(missing))
    print("  in the lineage and not the contracts   %4d (removed)" % len(orphan))
    print("  entries the contracts now change        %4d" % len(changed))
    for o in missing[:12]:
        print("     + %-32s %s" % (o, fresh[o]["contract"]))
    for o in orphan[:12]:
        print("     - %-32s %s" % (o, stored[o].get("contract")))
    by_field = {}
    for o in changed:
        for k in set(want[o]) | set(stored[o]):
            if want[o].get(k) != stored[o].get(k):
                by_field[k] = by_field.get(k, 0) + 1
    for k, n in sorted(by_field.items(), key=lambda x: -x[1]):
        print("     ~ %-12s %4d entr(ies)" % (k, n))
    for o in stale:
        print("  WARN override for %s, which no contract declares" % o)

    if a.audit:
        ops = overrides.get("operations") or {}
        carried = sum(1 for v in ops.values() if v.get("carried"))
        redundant = []
        for o, v in ops.items():
            if o not in fresh:
                continue
            base_r, base_w = set(fresh[o].get("reads") or []), set(fresh[o].get("writes") or [])
            red = sorted(set(v.get("reads") or []) & base_r) + sorted(set(v.get("writes") or []) & base_w)
            if red:
                redundant.append((o, red))
        print("  override entries %d (carried %d, ceiling %s); tables they add: reads %d, writes %d"
              % (len(ops), carried, overrides.get("carriedCeiling"),
                 sum(len(v.get("reads") or []) for v in ops.values()),
                 sum(len(v.get("writes") or []) for v in ops.values())))
        print("  overrides the contracts now derive (remove them): %d" % len(redundant))
        for o, red in redundant[:15]:
            print("     = %-32s %s" % (o, ", ".join(red)))

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    if not (missing or orphan or changed) and list(want) == list(stored):
        print("  nothing to change")
        return 0
    write_json(LINEAGE, want)
    print("  %d operations -> handoff/%s" % (len(want), LINEAGE.name))
    return 0



if __name__ == "__main__":
    sys.exit(main())
