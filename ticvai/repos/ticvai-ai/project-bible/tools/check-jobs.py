#!/usr/bin/env python3
"""Every job, timer and event consumer the package describes is declared, and a task builds it (r13, CHG-R13JOB-001).

**Why** (2 November 2026, the r13 job scan): 127 pieces of work the package described had no plan task, 98 of them
in Block A. The plan made a task per contract operation only; 148 state models moved on a timer or a job that named
no operation, and of 266 event consumers 10 had an operation. Each contract now declares its background work in
`x-ticvai-jobs` (tools/ticvai_jobs.py says the shape) and tools/build-service-docs.py makes one task per declaration.
This check holds both ends:

  J-TRANSITION  a state transition with trigger timer or job and no operation is moved by no declared job
                (or by two)
  J-CONSUMER    an event consumer with no operation, in a server module's context, is the consumer of no declared
                job of that module (or of two); a consumer whose context is no server module (a client app) is
                printed, never planned
  J-HANDOFF     an operation whose text hands work to a named job ("the export job", "the expiry sweeper", "the
                webhook replay dispatcher") is relied on by no declared job (`reliesOn`, or the emitters and state
                models tj.relies_on reads)
  J-READ-MODEL  a reporting consumer keeps a separate read model or dimension: ADR-0016 rules out separate read
                models, reports read the owning modules' data (the lead, 2 November 2026: "Drop them")
  J-EMITTER     an event no operation (`emittedBy`) and no declared job (`emits`) writes; where its emittedWhen
                names an operation, that operation goes in `emittedBy` (since r14, CHG-R14J-010, an event whose text
                names neither fails too: it was printed, and five events, two with critical consumers, had none)
  J-SHAPE       a declaration that is not well formed: module is its contract, host workers (ticvai-ai for AI;
                `undecided` only with a `decision`), a known trigger kind (event exactly when it consumes), an
                ISO-8601 `every`, moves and events and tables and operations that exist, writes in the module's own
                schemas (ADR-0055 rule 3: another module's rows are written by their owner)
  J-TASK        a declaration no task builds: its own plan task (JOB-/CONS-<contract>-<name> in
                handoff/service-docs/plan-tasks.csv, naming it), or the plan task or ticket (#nnnnn) `builtBy` names

A declaration with a `decision` (the text does not say which host or which modules) is printed as open and gets no
task until the lead decides; it still answers J-TRANSITION, J-CONSUMER and J-HANDOFF, so the gap stays named.

    python3 tools/check-jobs.py [--self-test]      (the self-tests run first, every time)

Read-only. Exit 1 on a finding.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ticvai_jobs as tj  # noqa: E402

ROOT = tj.ROOT
PLAN = ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"
# "the <name> job": a named job, sweeper or dispatcher; a phrase whose words are these is not a name ("the same job",
# "the assignee takes the job", "the rows back by job")
HANDOFF = re.compile(r"\b[Tt]he\s+((?:[A-Za-z][\w-]*\s+){1,3}?)(job|sweeper|dispatcher)\b")
NOT_A_NAME = {"same", "entire", "larger", "day", "whole", "this", "that", "assignee", "person", "first", "last",
              "next", "the", "a", "its", "one", "each", "any", "every", "other", "another", "by", "of", "for", "to",
              "back"}
READ_MODEL = re.compile(r"read model|\bdimension\b", re.I)


def handoff_names(text: str) -> list:
    out = []
    for words, kind in HANDOFF.findall(text or ""):
        ws = words.split()
        if ws and not any(w.lower() in NOT_A_NAME for w in ws):
            out.append(f"the {' '.join(ws)} {kind}")
    return out


def own_schemas(lineage: dict) -> dict:
    """schema -> the service whose operations write it most (the owner, as the lineage shows it)."""
    cnt = defaultdict(lambda: defaultdict(int))
    for v in lineage.values():
        for t in v.get("writes") or []:
            if "." in t and not t.startswith("cache:"):
                cnt[t.split(".")[0]][v.get("service")] += 1
    return {s: max(c, key=c.get) for s, c in cnt.items()}


def findings(jobs: dict, states: dict, events: dict, ops: dict, lineage: dict, contracts: set, plan: dict,
             tables: set) -> tuple[list, list]:
    """(findings, notes). ops: operationId -> {contract, text}; plan: task key -> row."""
    bad, notes = [], []
    svc_of_c = {}
    for v in lineage.values():
        svc_of_c.setdefault(v.get("contract"), v.get("service"))
    owner = own_schemas(lineage)
    moved, consumed = defaultdict(list), defaultdict(list)
    relied = set()
    for ref, j in sorted(jobs.items()):
        c = j["contract"]
        trig = j.get("trigger") or {}
        kind = trig.get("kind")
        ctx = j.get("context") or tj.context_of(c)
        if j.get("module") != c:
            bad.append(("J-SHAPE", ref, f"module is {j.get('module')!r}, not its contract {c!r}"))
        host = j.get("host")
        if host == "undecided":
            if not j.get("decision"):
                bad.append(("J-SHAPE", ref, "host undecided with no `decision` saying what the lead is asked"))
        # a module's job on the AI server only where the lead decided it, quoted in `hostDecision` (2 November 2026:
        # access#fraudDetection and catalogue#pricingEngine, CHG-R13INT-009); any other is a declaration error
        elif host not in tj.HOSTS or ((host == "ticvai-ai") != (c == "ai")
                                      and not (host == "ticvai-ai" and str(j.get("hostDecision") or "").strip())):
            bad.append(("J-SHAPE", ref, f"host {host!r}: AI's jobs run in ticvai-ai (ADR-0020), every other "
                                        "module's in workers (ADR-0055), unless `hostDecision` quotes the lead"))
        if kind not in tj.KINDS:
            bad.append(("J-SHAPE", ref, f"trigger kind {kind!r} is not one of {sorted(tj.KINDS)}"))
        if (kind == "event") != bool(j.get("consumes")):
            bad.append(("J-SHAPE", ref, "an event trigger consumes events, and only an event trigger does"))
        if trig.get("every") and not tj.DURATION.match(str(trig["every"])):
            bad.append(("J-SHAPE", ref, f"every {trig['every']!r} is not an ISO-8601 duration"))
        if tj.contract_of_context(ctx, contracts) != c:
            bad.append(("J-SHAPE", ref, f"context {ctx!r} is not this module's"))
        for e in j.get("consumes") or []:
            ev = events.get(e)
            mine = [x for x in (ev or {}).get("consumers") or [] if x.get("context") == ctx]
            if not mine:
                bad.append(("J-SHAPE", ref, f"consumes {e}, which has no consumer in context {ctx}"))
            elif all(x.get("operation") for x in mine):
                bad.append(("J-SHAPE", ref, f"consumes {e}, whose {ctx} consumer is an operation (SD-026)"))
            else:
                consumed[(e, ctx)].append(ref)
        for m in j.get("moves") or []:
            st = states.get(m.get("model"))
            hit = [t for t in (st or {}).get("transitions") or []
                   if t.get("from") == m.get("from") and t.get("to") == m.get("to") and tj.is_job_move(t)]
            if not hit:
                bad.append(("J-SHAPE", ref, f"moves {m.get('model')} {m.get('from')} -> {m.get('to')}, which is no "
                                            "job or timer transition of states/"))
            else:
                moved[(m["model"], m["from"], m["to"])].append(ref)
                if st.get("contract") != c:
                    bad.append(("J-SHAPE", ref, f"moves {m['model']}, whose contract is {st.get('contract')}"))
        for t in (j.get("reads") or []) + (j.get("writes") or []):
            if t not in tables:
                bad.append(("J-SHAPE", ref, f"names table {t}, which no DDL or lineage has"))
        for t in j.get("writes") or []:
            if owner.get(t.split(".")[0]) not in (None, svc_of_c.get(c)) and t.split(".")[0] != "platform":
                bad.append(("J-SHAPE", ref, f"writes {t}, {owner[t.split('.')[0]]}'s: another module's rows are "
                                            "written by their owner (ADR-0055 rule 3)"))
        if c == "reporting" and kind == "event" and not any(t.startswith("reporting.") for t in j.get("writes") or []):
            bad.append(("J-READ-MODEL", ref, "a reporting consumer writes no reporting table: reports read the owning "
                                             "modules' data (ADR-0016), so a consumer exists only to raise or record "
                                             "something in a reporting table"))
        for e in j.get("emits") or []:
            if e not in events:
                bad.append(("J-SHAPE", ref, f"emits {e}, which is no event in events/"))
        for o in j.get("reliesOn") or []:
            if o not in ops:
                bad.append(("J-SHAPE", ref, f"reliesOn {o}, which no contract declares"))
        relied |= tj.relies_on(j, states, events)
        # J-TASK
        if j.get("decision"):
            notes.append(f"OPEN {ref}: {j['decision']}")
            continue
        by = j.get("builtBy")
        if by:
            if not (re.fullmatch(r"#\d{4,6}", str(by)) or str(by) in plan):
                bad.append(("J-TASK", ref, f"builtBy {by}, which is no plan task and no ticket number"))
        else:
            row = plan.get(j["key"])
            if not row:
                bad.append(("J-TASK", ref, f"no plan task {j['key']} builds it (tools/build-service-docs.py)"))
            elif f"`{ref}`" not in (row.get("description") or ""):
                bad.append(("J-TASK", ref, f"plan task {j['key']} does not name it"))
    for (model, f, t), refs in sorted(moved.items()):
        if len(refs) > 1:
            bad.append(("J-TRANSITION", f"{model}:{f}->{t}", f"moved by two jobs: {', '.join(refs)}"))
    for name, st in sorted(states.items()):
        for t in st.get("transitions") or []:
            if tj.is_job_move(t) and (name, t.get("from"), t.get("to")) not in moved:
                bad.append(("J-TRANSITION", f"{name}:{t.get('from')}->{t.get('to')}",
                            f"states/{name}.yaml: a {t.get('trigger')} transition no declared job moves "
                            f"(x-ticvai-jobs `moves` in contracts/*/{st.get('contract')}.yaml)"))
    for e, ev in sorted(events.items()):
        seen_ctx = set()
        for x in ev.get("consumers") or []:
            ctx = x.get("context")
            if x.get("operation"):
                continue
            if ctx in seen_ctx and not (ctx == "reporting" and READ_MODEL.search(x.get("purpose") or "")):
                continue
            seen_ctx.add(ctx)
            if ctx == "reporting" and READ_MODEL.search(x.get("purpose") or ""):
                if len(ev.get("consumers") or []) == 1:
                    notes.append(f"KEPT {e} consumer reporting (a read model): it is the event's only consumer, so "
                                 "dropping it is a decision about the event (retire it, or give it a consumer)")
                    continue
                bad.append(("J-READ-MODEL", f"{e}:{ctx}", f"{ev.get('_file', e)}: a reporting consumer keeps a "
                                                          "separate read model (ADR-0016; the lead, 2 November 2026: "
                                                          "\"Drop them\")"))
                continue
            if not tj.contract_of_context(ctx, contracts):
                notes.append(f"CLIENT {e} consumer {ctx}: not a server module, not planned")
                continue
            refs = consumed.get((e, ctx)) or []
            entries = sum(1 for y in ev.get("consumers") or [] if y.get("context") == ctx and not y.get("operation"))
            if not refs:
                bad.append(("J-CONSUMER", f"{e}:{ctx}", f"{ev.get('_file', e)}: consumer {ctx} has no operation and "
                                                        "no declared job consumes it"))
            elif len(refs) > entries:
                bad.append(("J-CONSUMER", f"{e}:{ctx}", f"{len(refs)} jobs share {entries} consumer entr"
                                                        f"{'y' if entries == 1 else 'ies'}: {', '.join(refs)}"))
    job_emits = {e for j in jobs.values() for e in j.get("emits") or []}
    for e, ev in sorted(events.items()):
        if ev.get("emittedBy") or e in job_emits:
            continue
        named = sorted({w for w in re.findall(r"\b([a-z][A-Za-z0-9]+)\b", ev.get("emittedWhen") or "") if w in ops})
        critical = sorted({x.get("context") for x in ev.get("consumers") or [] if x.get("isCritical")})
        if named:
            bad.append(("J-EMITTER", e, f"emittedWhen names {', '.join(named)}, and emittedBy is empty"))
        else:
            # **An event nothing emits fails, it is not printed** (r13 system review B-09; CHG-R14J-010): five events
            # had no emitter and were notes here, fnb.menuPublished among them, which carries allergen changes to two
            # critical consumers; a consumer was built and waited for an event no handler wrote.
            bad.append(("J-EMITTER", e, f"{ev.get('_file', e)}: no operation (`emittedBy`) and no declared job "
                                        "(`emits`) writes it"
                                        + (f", and its consumers {', '.join(critical)} are critical" if critical else "")))
    for o, x in sorted(ops.items()):
        names = handoff_names(x.get("text") or "")
        if names and o not in relied:
            bad.append(("J-HANDOFF", o, f"{x.get('contract')}#{o} hands work to {names[0]}, and no declared job "
                                        "relies on it"))
    return bad, notes


def load_ops(root: Path) -> dict:
    ops = {}
    for c, p in tj.contract_files(root).items():
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for pi in (d.get("paths") or {}).values():
            for o in (pi or {}).values():
                if isinstance(o, dict) and o.get("operationId"):
                    ops[o["operationId"]] = {"contract": c, "text": f"{o.get('summary') or ''} {o.get('description') or ''}"}
    return ops


def self_test() -> list:
    fails = []
    st = {"cart": {"contract": "orders", "transitions": [
        {"from": "active", "to": "expired", "trigger": "timer"},
        {"from": "active", "to": "checkedOut", "operation": "checkoutCart", "trigger": "operation"}]}}
    ev = {"order.paid": {"name": "order.paid", "emittedBy": ["orders.createPayment"], "emittedWhen": "createPayment",
                         "consumers": [{"context": "ledger", "purpose": "Post revenue"},
                                       {"context": "reporting", "purpose": "Update the sales read model"},
                                       {"context": "guest-app", "purpose": "Refresh"}]},
          "cart.abandoned": {"name": "cart.abandoned", "emittedWhen": "the cart expired", "consumers": []},
          "order.exchanged": {"name": "order.exchanged", "emittedWhen": "exchangeOrderLines succeeds", "consumers": []}}
    ops = {"checkoutCart": {"contract": "orders", "text": "Checks out the cart."},
           "createPayment": {"contract": "orders", "text": "Pays. The expiry sweeper returns the holds."},
           "exchangeOrderLines": {"contract": "orders", "text": "Exchanges lines; the same job as before."},
           "closeFiscalPeriod": {"contract": "finance", "text": "Closes."}}
    lin = {"checkoutCart": {"contract": "orders", "service": "OrderService", "writes": ["orders.cart"]},
           "closeFiscalPeriod": {"contract": "finance", "service": "LedgerService", "writes": ["ledger.journal_entry"]}}
    tables = {"orders.cart", "ledger.journal_entry"}
    contracts = {"orders", "finance", "reporting"}
    good = {
        "orders#holdExpiry": {"contract": "orders", "name": "holdExpiry", "key": "JOB-ORDERS-HOLD-EXPIRY",
                              "module": "orders", "host": "workers", "trigger": {"kind": "timer", "every": "PT1M"},
                              "moves": [{"model": "cart", "from": "active", "to": "expired"}],
                              "writes": ["orders.cart"], "emits": ["cart.abandoned"], "reliesOn": ["createPayment"]},
        "finance#postings": {"contract": "finance", "name": "postings", "key": "CONS-FINANCE-POSTINGS",
                             "module": "finance", "host": "workers", "trigger": {"kind": "event"},
                             "consumes": ["order.paid"], "writes": ["ledger.journal_entry"], "builtBy": "#37212"}}
    plan = {"JOB-ORDERS-HOLD-EXPIRY": {"description": "Builds: `adr ADR-0055`. The job `orders#holdExpiry` ..."}}
    ev_ok = json.loads(json.dumps(ev))
    ev_ok["order.paid"]["consumers"] = [c for c in ev_ok["order.paid"]["consumers"] if c["context"] != "reporting"]
    ev_ok["order.exchanged"]["emittedBy"] = ["orders.exchangeOrderLines"]
    b, n = findings(good, st, ev_ok, ops, lin, contracts, plan, tables)
    if b:
        fails.append(f"a well-declared package has findings: {b}")
    if not any("CLIENT order.paid" in x for x in n):
        fails.append("a client-app consumer is not printed")
    b, _ = findings(good, st, ev, ops, lin, contracts, plan, tables)
    rules = {r for r, _, _ in b}
    for want in ("J-READ-MODEL", "J-EMITTER"):
        if want not in rules:
            fails.append(f"{want} did not fire")
    orphan = json.loads(json.dumps(ev_ok))
    orphan["menu.published"] = {"name": "menu.published", "emittedWhen": "a menu goes live",
                                "consumers": [{"context": "ai", "purpose": "Reindex", "isCritical": True,
                                               "operation": "reindexMenu"}]}
    b, _ = findings(good, st, orphan, ops, lin, contracts, plan, tables)
    if not any(r == "J-EMITTER" and k == "menu.published" and "critical" in m for r, k, m in b):
        fails.append("J-EMITTER did not fail an event no operation or job emits (B-09)")
    b, _ = findings({}, st, ev_ok, ops, lin, contracts, plan, tables)
    rules = {r for r, _, _ in b}
    for want in ("J-TRANSITION", "J-CONSUMER", "J-HANDOFF"):
        if want not in rules:
            fails.append(f"{want} did not fire on a package with no declarations")
    if any(k == "exchangeOrderLines" for r, k, _ in b if r == "J-HANDOFF"):
        fails.append("'the same job' was read as a named job")
    worse = json.loads(json.dumps(good))
    worse["orders#holdExpiry"].update(host="ticvai-ai", writes=["ledger.journal_entry"], trigger={"kind": "event"})
    worse["finance#postings"]["builtBy"] = "NOT-A-TASK"
    b, _ = findings(worse, st, ev_ok, ops, lin, contracts, {}, tables)
    msgs = " | ".join(m for _, _, m in b)
    for want in ("host 'ticvai-ai'", "written by their owner", "an event trigger consumes", "builtBy NOT-A-TASK"):
        if want not in msgs:
            fails.append(f"J-SHAPE/J-TASK missed: {want}")
    decided = json.loads(json.dumps(good))
    decided["orders#holdExpiry"].update(host="ticvai-ai", hostDecision="the lead, a test")
    b, _ = findings(decided, st, ev_ok, ops, lin, contracts, plan, tables)
    if any(r == "J-SHAPE" and k == "orders#holdExpiry" and "host" in m for r, k, m in b):
        fails.append("J-SHAPE refused a module's AI-server job the lead decided (hostDecision)")
    b, _ = findings({k: v for k, v in good.items() if k != "finance#postings"} | {
        "orders#holdExpiry": dict(good["orders#holdExpiry"])}, st, ev_ok, ops, lin, contracts, {}, tables)
    if not any(r == "J-TASK" for r, _, _ in b):
        fails.append("J-TASK did not fire on a declaration with no plan task")
    return fails


def main() -> int:
    fails = self_test()
    if fails:
        for f in fails:
            print(f"  self-test: {f}")
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if "--self-test" in sys.argv:
        print("check-jobs: self-tests pass")
        return 0
    lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
    tables = {t for v in lineage.values() for t in (v.get("reads") or []) + (v.get("writes") or [])
              if "." in t and not t.startswith("cache:")}
    for db in ("tenant", "control"):
        for p in (ROOT / "backend" / db).glob("*.sql"):
            tables |= {f"{a}.{b}" for a, b in re.findall(r'CREATE TABLE IF NOT EXISTS (\w+)\."?(\w+)"?',
                                                           p.read_text(encoding="utf-8"))}
    plan = {}
    if PLAN.exists():
        plan = {r["key"]: r for r in csv.DictReader(PLAN.open(encoding="utf-8"))}
    jobs = tj.load(ROOT)
    bad, notes = findings(jobs, tj.load_states(ROOT), tj.load_events(ROOT), load_ops(ROOT), lineage,
                          set(tj.contract_files(ROOT)), plan, tables)
    for n_ in notes:
        print(f"  note: {n_}")
    by_rule = defaultdict(list)
    for r, k, m in bad:
        by_rule[r].append((k, m))
    for r in sorted(by_rule):
        print(f"{r}: {len(by_rule[r])}")
        for k, m in by_rule[r][:40]:
            print(f"  {k}: {m}")
        if len(by_rule[r]) > 40:
            print(f"  ... and {len(by_rule[r]) - 40} more")
    built = sum(1 for j in jobs.values() if not j.get("decision"))
    print(f"check-jobs: {len(jobs)} declared ({built} built, {len(jobs) - built} open); "
          f"{'FAIL ' + str(len(bad)) + ' finding(s)' if bad else 'pass'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
