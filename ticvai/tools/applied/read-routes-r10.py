#!/usr/bin/env python3
"""Read routes between modules, r10 (r10 lane E, 25 October 2026; CHG-R10GEN-001; PROCESS-LOG P-30).

**The class release the 18 October sweep left for later.** tools/applied/read-routes-18-october.py (CHG-RTE-001)
routed the facts named in the fact phrases of check-cross-module-reads (`how == fact`). Every other XR-FACT finding,
an operation's text naming another module's table, field or schema with no query asked over it, was baselined on 18
October (354acd74) and acknowledged on started tickets "until the next class release" (again at the r8 gate,
92eb4150). That release never ran, and about 13 of the 48 change requests of 21-24 October (CR-186 to CR-240) were
findings the build had reported and acknowledged: listDepositBoxes' drawer limits came back as CR-218.

On r9 the class query (`check-cross-module-reads --list-facts`) held 720 facts on 436 operations over 114 tables. The
check now judges a read (GET) as the sweep's fix round 1 did (a fact only in its response schema is the writer's
rule, unless the schema says it is worked out on read) and leaves out the sentences the dry run showed are not reads
(NOT_READ, NOT_READ_FOR); what is left is what this script routes. For each finding it writes, at the operation's own
lines, an `x-ticvai-read-via` entry:

  ROUTE     to the owner's query over that table (a `<table>Records` data read where the owner has several), `in-process`
            within one deployable and `service` across, the query's `served` gaining the route (CHG-RTE-001's rule);
  QUERY     where the owner declares no query over the table, a per-table data read in the shape of the
            `<table>Records` queries of CHG-MOD-001 (tenancy#venueSettingsRecords), declared in the owner's contract
            beside the schema that persists the table, then routed to;
  EXPLICIT  the reads whose words the check leaves to the writer that sets the value (holdOrder's held expiry and
            buildProductionPlan's business date, from the venue's business-day cut-off).

It does not route, and prints for the lead:

  * an Identity operation reading above the foundation tier, which only a projection may answer (ADR-0028);
  * the `fact` phrases it routes, so the lead can see each is a read (the 18 October rule: a phrase is a read only
    where the operation uses the fact);
  * a table whose owner has no schema persisting it, so no typed query can be declared.

A route this script wrote that no finding justifies any more is removed, and a query it declared that nobody asks
goes. A second run writes nothing. The contracts keep their own line endings, and a read-via list indented deeper than
its key (addCartLine's) is written at its own indent.

    python tools/applied/read-routes-r10.py            # what it would write
    python tools/applied/read-routes-r10.py --apply    # then: python tools/derive-lineage.py --apply
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_guard as g  # noqa: E402


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rr = _load("rr", TOOLS / "applied" / "read-routes-18-october.py")
ROUTES = rr.ROUTES
TAG = "CHG-R10GEN-001"
SRC = "r10 lane E, 25 October 2026, CHG-R10GEN-001"
OWN_FOR = re.compile(r"^what its text calls \".*\(CHG-R10GEN-001\)$|^.*\(r10 read routes; CHG-R10GEN-001\)$")
# The name a module's own queries use for it ("F&B answers with its ..."), where it is not the service's.
LABEL = {"FnbService": "F&B"}
# The reads the check leaves to the writer that sets the value: (operation, query, for).
EXPLICIT = [
    ("holdOrder", "tenancy#venueSettingsRecords",
     "heldUntil where the cashier sent no holdUntil: the venue's next business-day cut-off (businessDayCutoff) "
     "(r10 read routes; CHG-R10GEN-001)"),
    ("buildProductionPlan", "tenancy#venueSettingsRecords",
     "the plan's trading day, a business date closing at the venue's businessDayCutoff "
     "(r10 read routes; CHG-R10GEN-001)"),
]


def is_own(route: dict) -> bool:
    """A read route this script wrote (its `for` ends with this change's tag in one of the two forms it writes)."""
    return bool(OWN_FOR.match(str((route or {}).get("for") or "")))


def route_for(reader_deployable, owner_deployable) -> str:
    return "in-process" if reader_deployable == owner_deployable else "service"


def records_name(table: str) -> str:
    """`orders.deposit_policy` -> `depositPolicyRecords`, the CHG-MOD-001 naming of a per-table data read."""
    parts = table.split(".", 1)[1].split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:]) + "Records"


def pick_query(table: str, owner: str, queries: dict, svc_of_contract: dict):
    """The owner's query to ask over `table`: one whose tables include it and which some route serves other than a
    projection alone; the table's own `<table>Records` first, then any `...Records`, then by name. None when the owner
    declares none. `queries`: `<contract>#<name>` -> (stem, declaration)."""
    xr = _xr()
    cands = []
    for key, (stem, q) in queries.items():
        if svc_of_contract.get(stem) != owner or table not in xr.query_tables(q):
            continue
        served = [r for r in (q.get("served") or []) if r in ROUTES]
        if served and set(served) <= {"projection"}:
            continue
        name = key.split("#", 1)[1]
        cands.append((name != records_name(table), not name.endswith("Records"), key))
    return sorted(cands)[0][2] if cands else None


def schema_for(table: str, owner: str, persist: dict, svc_of_contract: dict, by: dict = None):
    """(contract stem, schema) of the owner's that persists `table`: the schema named like the table first. Where none
    names it first in its x-ticvai-persistence, a schema of the owner's named like the table (`JournalLine`, the line
    of `JournalEntry`'s `ledger.journal_entry + ledger.journal_line`)."""
    want = "".join(p[:1].upper() + p[1:] for p in table.split(".", 1)[1].split("_"))
    hits = sorted((sch != want, stem, sch) for (stem, sch), t in persist.items()
                  if t == table and svc_of_contract.get(stem) == owner)
    if hits:
        return hits[0][1], hits[0][2]
    named = sorted(stem for (stem, sch) in (by or {}) if sch == want and svc_of_contract.get(stem) == owner)
    return (named[0], want) if named else None


def contract_rel(stem: str):
    for r in (f"contracts/spine/{stem}.yaml", f"contracts/satellite/{stem}.yaml", f"contracts/{stem}.yaml"):
        if (ROOT / r).exists():
            return r
    return next((str(p.relative_to(ROOT)).replace("\\", "/") for p in (ROOT / "contracts").rglob(f"{stem}.yaml")),
                None)


def add_read_via(text: str, op: str, entries: list):
    """read-routes-18-october's add_read_via, writing at the list's own indent (four of the 660 lists in r9 indent
    their items two more than the key, addCartLine's). entries: [(query, route, for)]. Returns (text, added)."""
    lines = text.split("\n")
    i, end, ind = rr._op_block(lines, op)
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is None:
        return rr.add_read_via(text, op, entries)
    m = re.match(r"^(\s*)- ", lines[k + 1]) if k + 1 < end else None
    item = m.group(1) if m else ind
    have, at = set(), k + 1
    while at < end and (lines[at].startswith(f"{item}- ") or lines[at].startswith(f"{item}  ")):
        q = re.match(r"^\s+- query:\s*(\S+)", lines[at])
        if q:
            have.add(q.group(1))
        at += 1
    new = []
    for q, route, w in entries:
        if q in have:
            continue
        have.add(q)
        new += [f"{item}- query: {q}", f"{item}  route: {route}", f"{item}  for: '" + w.replace("'", "''") + "'"]
    if not new:
        return text, 0
    lines[at:at] = new
    return "\n".join(lines), len(new) // 3


def remove_own(text: str, op: str, query: str):
    """Removes the operation's route to `query` that this script wrote; drops the list when it empties."""
    lines = text.split("\n")
    i, end, ind = rr._op_block(lines, op)
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is None:
        return text, 0
    m = re.match(r"^(\s*)- ", lines[k + 1]) if k + 1 < end else None
    ind = m.group(1) if m else ind
    at, items = k + 1, []
    while at < end and (lines[at].startswith(f"{ind}- ") or lines[at].startswith(f"{ind}  ")):
        if lines[at].startswith(f"{ind}- "):
            items.append([at, at + 1])
        else:
            items[-1][1] = at + 1
        at += 1
    for a, b in items:
        block = lines[a:b]
        q = re.match(r"^\s+- query:\s*(\S+)", block[0])
        w = next((re.match(r"^\s+for:\s*'(.*)'\s*$", l) for l in block if re.match(r"^\s+for:", l)), None)
        if q and q.group(1) == query and w and is_own({"for": w.group(1).replace("''", "'")}):
            del lines[a:b]
            if len(items) == 1:
                del lines[k]
            return "\n".join(lines), 1
    return text, 0


def remove_query(text: str, name: str):
    """Removes query `name` from the x-ticvai-queries map, where this script declared it (its rule cites TAG)."""
    lines = text.split("\n")
    try:
        i, end = rr._query_block(lines, name)
    except SystemExit:
        return text, False
    if TAG not in " ".join(lines[i:end]):
        return text, False
    while end > i + 1 and not lines[end - 1].strip():
        end -= 1
    del lines[i:end]
    return "\n".join(lines), True


_XR = None


def _xr():
    global _XR
    if _XR is None:
        _XR = _load("xr", TOOLS / "check-cross-module-reads.py")
    return _XR


def plan_routes(findings, ctx: dict):
    """The sweep, as data: (plan {op: [(query, route, for)]}, new queries {key: (stem, table, schema)}, held [lines],
    fact phrases routed [lines]). `findings`: check-cross-module-reads' fact_findings rows. `ctx` holds services,
    queries, persist and svc_of_contract."""
    services, queries = ctx["services"], ctx["queries"]
    svc_of_contract, persist = ctx["svc_of_contract"], ctx["persist"]
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    tier_of = {s: v.get("tier") for s, v in services.items()}
    plan, new_q, held, facts = {}, {}, [], []
    for op, reader, t, owner, how, phrase in findings:
        if reader == "IdentityService" and tier_of.get(owner) != "foundation":
            held.append(f"{op}: {t} ({owner}, {tier_of.get(owner)}) - Identity asks above the foundation tier only by "
                        f"projection (ADR-0028): {how} {phrase!r}")
            continue
        q = pick_query(t, owner, queries, svc_of_contract)
        if q is None:
            sch = schema_for(t, owner, persist, svc_of_contract, ctx.get("by"))
            if sch is None:
                held.append(f"{op}: {t} ({owner}) - no schema of {owner}'s persists it, so no typed query can be "
                            f"declared: {how} {phrase!r}")
                continue
            q = f"{sch[0]}#{records_name(t)}"
            new_q.setdefault(q, (sch[0], t, sch[1]))
        words = re.sub(r"\s+", " ", phrase.replace("`", "")).strip()
        label = LABEL.get(owner, owner[:-len("Service")])
        plan.setdefault(op, []).append((q, route_for(dep_of.get(reader), dep_of.get(owner)),
                                        f'what its text calls "{words}": {t}, {label}\'s data ({TAG})'))
        if how == "fact":
            facts.append(f"{op}: {t} ({phrase!r}) -> {q}")
    return plan, new_q, held, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    xr = _xr()
    services = (g.load_json(ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    tables = set((g.load_json(ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    by, _names = g.schemas()
    persist = xr.persisted(by, tables)
    queries = xr.declared_queries()
    ops = g.operations()
    ctx = {"services": services, "queries": queries, "svc_of_contract": svc_of_contract, "persist": persist, "by": by}
    texts: dict = {}

    def text(rel):
        if rel not in texts:
            texts[rel] = rr._read(ROOT / rel)
        return texts[rel]

    findings = xr.fact_findings(ignore=is_own)
    plan, new_q, held, facts = plan_routes(findings, ctx)
    for op, q, why in EXPLICIT:
        if op in ops:
            stem = q.split("#", 1)[0]
            owner = svc_of_contract.get(stem)
            reader = svc_of_contract.get(ops[op]["contract"])
            plan.setdefault(op, []).append((q, route_for(dep_of.get(reader), dep_of.get(owner)), why))
    # 1. the new per-table data reads, each in its owner's contract
    for key, (stem, t, sch) in sorted(new_q.items()):
        rel = contract_rel(stem)
        owner = svc_of_contract.get(stem)
        label = LABEL.get(owner, owner[:-len("Service")])
        block = rr.data_query(key.split("#", 1)[1], stem, t, label, dep_of.get(owner), ["service"], sch, SRC)
        texts[rel], added = rr.add_query(text(rel), key.split("#", 1)[1], block)
        if added:
            print(f"  QUERY {key} over {t} ({sch})")
    # 2. the routes
    n_via = 0
    for op, entries in sorted(plan.items()):
        rel = ops[op]["file"]
        texts[rel], n = add_read_via(text(rel), op, entries)
        n_via += n
        if n:
            for q, route, why in entries:
                print(f"  ROUTE {op}: {q} ({route}) - {why}")
    # 3. a route this script wrote that nothing justifies any more goes
    wanted = {(op, q) for op, entries in plan.items() for q, _r, _w in entries}
    n_gone = 0
    for op, f in sorted(ops.items()):
        for r in f["op"].get("x-ticvai-read-via") or []:
            if isinstance(r, dict) and is_own(r) and (op, r.get("query")) not in wanted:
                texts[f["file"]], n = remove_own(text(f["file"]), op, r.get("query"))
                n_gone += n
                if n:
                    print(f"  GONE {op}: {r.get('query')} - no longer named in its text")
    # 4. served: every route an asker takes; a query this script declared serves exactly those, and goes unasked
    used: dict = {}
    for rel in sorted({f["file"] for f in ops.values()}):
        for m in re.finditer(r"- query:\s*(\S+)\s*\n\s+route:\s*(\S+)", text(rel)):
            used.setdefault(m.group(1), set()).add(m.group(2))
    mine = {k for k, (_s, q) in queries.items() if TAG in str(q.get("rule") or "")} | set(new_q)
    for key in sorted(set(used) | mine):
        stem, name = key.split("#", 1)
        rel = contract_rel(stem)
        if rel is None:
            continue
        lines = text(rel).split("\n")
        try:
            rr._query_block(lines, name)
        except SystemExit:
            continue
        owner_dep = dep_of.get(svc_of_contract.get(stem))
        if key in mine:
            if not used.get(key):
                texts[rel], gone = remove_query(text(rel), name)
                if gone:
                    print(f"  QUERY GONE {key} - nobody asks it")
                continue
            want = [r for r in ROUTES if r in used[key]]
        else:
            want = rr.served_for(rr.served_of(text(rel), name), used.get(key, set()))
        texts[rel], changed = rr.set_served(text(rel), name, want, owner_dep)
        if changed:
            print(f"  SERVED {key}: {want}")
    for s in facts:
        print(f"  FACT PHRASE routed (the lead checks it is a read) {s}")
    for s in held:
        print(f"  NOT ROUTED (for the lead) {s}")
    changed = [rel for rel, t in texts.items() if t != rr._read(ROOT / rel)]
    print(f"{len(findings)} finding(s); {n_via} read route(s) in {len(plan)} operation(s); {len(new_q)} new "
          f"quer(ies); {n_gone} route(s) removed; {len(held)} not routed; {len(changed)} contract file(s) change"
          + ("" if a.apply else " (nothing written, pass --apply)"))
    if a.apply:
        for rel in changed:
            rr._write(ROOT / rel, texts[rel])
    return 0


if __name__ == "__main__":
    sys.exit(main())
