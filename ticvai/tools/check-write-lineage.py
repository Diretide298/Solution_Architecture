#!/usr/bin/env python3
"""Every write writes something, every event goes through the outbox, every schema has an owner (CHG-R1S-005).

**Found by the HLD/LLD cross-check of 3 October 2026** (39 package inconsistencies, `CHG-R1S-005` to `-011`):
`createOrder` emitted `order.created` and did not list `platform.outbox` in its writes, though the event is
written to the outbox in the same transaction; six POSTs (`exportSitePackage`, `rejectShiftVariance`,
`sendGuestConversationMessage` among them) wrote no table at all; `shift.closed` named one of the four
operations that close a shift; `seat.sold` named an OrderService operation for a seating event; and the
`kernel` schema had no owning service. Scripted, the package had 10 emitters without the outbox and 163 write
operations writing nothing. Rules:

    W-OUTBOX    an operation that emits an event (`emittedBy` in events/, `x-ticvai-emits`) writes
                `platform.outbox`
    W-NOTABLE   a POST, PUT, PATCH or DELETE writes at least one table, or its lineage entry says
                `pure` (it computes and returns) or `storageUndecided` (an explicit, reasoned exemption),
                each printed
    W-EMITS     an operation on a state transition that emits an event is in that event's `emittedBy`,
                and every `emittedBy` names an operation that exists
    W-OWNER     every schema with a table belongs to a service in `handoff/service-decomposition.json`
    W-CACHEKEY  an operation that reads or writes `cache:resolution` records the key it fills or evicts and the
                resolvers it bumps, as `tools/resolution_cache.py` derives them (CHG-FXC-001, root class R141)
    W-CREATED   a 201 response's persisted tables are among the operation's writes (CHG-FXC-002)

    python tools/check-write-lineage.py [--list]
"""
from __future__ import annotations

import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def yl(p):
    return yaml.load(io.open(p, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    lin = json.load(io.open(os.path.join(ROOT, "handoff", "api-data-lineage.json"), encoding="utf-8"))
    ops = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        for p, item in (yl(f).get("paths") or {}).items():
            for v, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (v, op)
    events, emitted_by = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "events", "*.yaml"))):
        if os.path.basename(f).startswith("_"):
            continue
        e = yl(f)
        events[e.get("name")] = e
        emitted_by[e.get("name")] = {str(o).split(".")[-1] for o in e.get("emittedBy") or []}
    bad, exempt = [], []

    emitters = {o for s in emitted_by.values() for o in s}
    emitters |= {o for o, (_, op) in ops.items() if op.get("x-ticvai-emits")}
    for o in sorted(emitters):
        if o not in ops:
            continue
        if (lin.get(o) or {}).get("contract") == "ai":
            # **AI writes only AI stores** (ADR-0020; check-package refuses platform.outbox on an AI operation),
            # and AI consumers keep their own ai.inbox (ADR-0058). Where the AI's four emitters write their
            # events (an ai.outbox beside ai.inbox, or the platform relay) is a question for the lead (R1S report).
            exempt.append(("aiPublishPath", o, "an AI emitter: its outbox is the open AI publish-path question"))
            continue
        if "platform.outbox" not in (lin.get(o) or {}).get("writes", []):
            bad.append(("W-OUTBOX", o, "emits an event and its lineage does not write platform.outbox"))

    for o, (v, _) in sorted(ops.items()):
        if v == "get":
            continue
        e = lin.get(o)
        if e is None:
            bad.append(("W-NOTABLE", o, "a write operation with no lineage entry (run derive-lineage)"))
            continue
        if [w for w in e.get("writes", []) if ":" not in w]:
            continue
        if e.get("pure"):
            exempt.append(("pure", o, e["pure"]))
        elif e.get("storageUndecided"):
            exempt.append(("storageUndecided", o, e["storageUndecided"]))
        else:
            bad.append(("W-NOTABLE", o, f"a {v.upper()} that writes no table and is not marked pure"))

    for name, s in emitted_by.items():
        for o in sorted(s - set(ops)):
            bad.append(("W-EMITS", name, f"emittedBy names {o}, which no contract declares"))
    for f in sorted(glob.glob(os.path.join(ROOT, "states", "*.yaml"))):
        st = yl(f)
        for t in st.get("transitions") or []:
            op = t.get("operation")
            for ev in t.get("emits") or []:
                if op and ev in emitted_by and op not in emitted_by[ev]:
                    bad.append(("W-EMITS", ev, f"{os.path.basename(f)}: {t.get('from')} -> {t.get('to')} by {op} "
                                               f"emits it, and its emittedBy does not name {op}"))

    # W-CACHEKEY (4 October 2026, CHG-FXC-001): 18 Sprint 1-2 tickets stopped on "which resolution entry each
    # writer evicts is not recorded". The rule is in tools/resolution_cache.py; the entry must carry what it says.
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("resolution_cache", os.path.join(ROOT, "tools", "resolution_cache.py"))
    _rc = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_rc)
    for o, e in sorted(lin.items()):
        want = _rc.resolution_cache(o, e, lin)
        if want is None:
            continue
        if not want.get("resolvers"):
            bad.append(("W-CACHEKEY", o, "touches cache:resolution and no resolver can be named for it"))
        elif e.get("cache") != want:
            bad.append(("W-CACHEKEY", o, "touches cache:resolution and its lineage does not record the key it "
                                         "fills or evicts (run derive-lineage --apply)"))
    # W-CREATED (CHG-FXC-002): recordWriteOff answered 201 with the JournalEntry it posted and wrote only
    # ledger.posting. A 201 is a created row; its schema's persisted tables are writes.
    # A schema name is per file (`Invitation` is an orders invitation and a marketing one), and a 201 refers to its
    # own file's schema, so the persistence map is kept per contract file.
    _persist, _file_of = {}, {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        d = yl(f)
        for p_, item in (d.get("paths") or {}).items():
            for v_, op_ in (item or {}).items():
                if isinstance(op_, dict) and op_.get("operationId"):
                    _file_of[op_["operationId"]] = f
        for n, sc in ((d.get("components") or {}).get("schemas") or {}).items():
            t = str((sc or {}).get("x-ticvai-persistence") or "").strip()
            if t and not t.lower().startswith("none"):
                _persist[(f, n)] = [x.strip() for x in t.split("+") if "." in x.strip()]
    for o, (v, op) in sorted(ops.items()):
        r201 = (op.get("responses") or {}).get("201") or (op.get("responses") or {}).get(201)
        if v == "get" or not r201:
            continue
        names = set(__import__("re").findall(r"(?<![./a-z])#/components/schemas/([A-Za-z0-9_]+)", json.dumps(r201)))
        made = {t.split(" ")[0] for n in names for t in _persist.get((_file_of.get(o), n), [])}
        miss = sorted(t for t in made if t not in ((lin.get(o) or {}).get("writes") or []))
        if miss:
            bad.append(("W-CREATED", o, "answers 201 with %s and does not write it" % ", ".join(miss)))

    sref = json.load(io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8"))
    dec = json.load(io.open(os.path.join(ROOT, "handoff", "service-decomposition.json"), encoding="utf-8"))
    owned = {s for v in (dec.get("services") or {}).values() for s in v.get("schemas") or []}
    store = sref.get("store") or {}
    schemas = {t.split(".")[0] for t in sref.get("cols") or {} if "." in t and ":" not in t
               and store.get(t, "postgres") in ("postgres", "postgres-analytical")}
    for s in sorted(schemas - owned - {"control"}):
        bad.append(("W-OWNER", s, "a schema with tables that no service in service-decomposition.json owns"))

    by = {}
    for r, _, _ in bad:
        by[r] = by.get(r, 0) + 1
    kinds = {}
    for k, _, _ in exempt:
        kinds[k] = kinds.get(k, 0) + 1
    if "--list" in sys.argv:
        for k, o, why in exempt:
            print(f"  exempt {k:<16} {o:<36} {why}")
    else:
        for k, o, why in exempt:
            if k in ("storageUndecided", "aiPublishPath"):
                print(f"  exempt {k:<16} {o:<36} {why}")
        print(f"  ({kinds.get('pure', 0)} operation(s) marked pure, each with its reason: --list shows them)")
    for r, o, d in bad[:60]:
        print(f"  {r:<10} {o:<36} {d}")
    if bad:
        print("FAIL %d finding(s): %s" % (len(bad), ", ".join(f"{k} {v}" for k, v in sorted(by.items()))))
        return 1
    print(f"ok: every emitter writes the outbox, every write writes a table or says why not "
          f"({kinds.get('pure', 0)} pure, {kinds.get('storageUndecided', 0)} storage undecided), every emitted "
          f"event names its operations, every schema has an owner, every resolution-cache user names its key, "
          f"every 201 writes what it creates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
