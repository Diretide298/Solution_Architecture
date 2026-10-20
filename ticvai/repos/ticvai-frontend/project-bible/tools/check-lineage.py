#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check `handoff/api-data-lineage.json` against the contracts, the schema and the services.

**Twenty-plus tools read the lineage as authoritative and nothing checked it.** It is the
first thing `refresh.sh` runs and the input to `check-package`, `check-screens`,
`derive-relationships`, both workbooks and the viewer — and it is written by a tool that
**adds and never updates**, which is correct for preserving hand judgements and wrong for
anything that moves.

That is not hypothetical. On 19 September, in one day:

  * seven `release*` entries survived a rename to `relinquish*` on 8 September, so the
    lineage claimed 1,981 operations against 1,974 that exist;
  * fifteen operations moved from `retail.yaml` and `games.yaml` into `wallet.yaml` and
    their entries went on naming `retail`, and therefore `RetailService`;
  * twenty-six entries still listed `retail.wallet` in `reads` and `writes` after that
    table became `wallet.wallet`, and **every refresh rebuilt the dropped table from
    them** — through `derive-schema`, which reads the relationship graph, which
    `derive-relationships` rebuilds from the schema the lineage repopulated.

`check-package` caught the first of those. Nothing caught the other two, because no check
compared an entry against the contract that defines it.

## What it checks

  1. Every lineage entry names an operation some contract declares.
  2. Every operation a contract declares has a lineage entry.
  3. The `contract` on an entry is the file that actually defines the operation.
  4. The `service` is the one `service-decomposition.json` names for that contract.
  5. No entry has a null service — `derive-diagrams` sorts on it and raises on `None`.
  6. Every table in `reads`/`writes` exists in `schema-reference.json`.
  7. Every postgres table belongs to exactly one service.

  8. LN-TEXT (warning): a table the operation's own text names and its entry does not list.
  9. LN-DERIVED: the lineage is what `tools/derive-lineage.py` derives from the contracts and the override list
     (20 October 2026, CHG-R8GEN-001): reads, writes, readVia, writeVia and the contract facts of every entry.
 10. LN-OVERRIDE: every entry of `handoff/api-data-lineage-overrides.json` names an operation a contract declares,
     tables that exist, and a reason; the entries carried from the hand-kept lineage may only fall (carriedCeiling).
     An override the contract now derives is a warning (remove it).

    python tools/check-lineage.py [--quiet] [--text]    (the self-tests run first, every time)

**Coverage is reported, never failed.** A third of operations reach no table, and most of
that is correct — a service-to-service call, a computed projection, a health probe. It is
printed because it is worth watching, not because a number is wrong.
"""
import collections
import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
VERBS = ("get", "post", "put", "patch", "delete")
ERRORS, WARNINGS = [], []
_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load_json(name, required=True):
    p = os.path.join(H, name)
    if not os.path.exists(p):
        if required:
            ERRORS.append("handoff/%s is missing" % name)
        return {}
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception as e:
        ERRORS.append("handoff/%s is unreadable: %s" % (name, e))
        return {}


def contract_operations():
    """operationId -> contract name, read off the file that declares it."""
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        name = os.path.basename(f)[:-5]
        try:
            d = yaml.load(io.open(f, encoding="utf-8"), Loader=_LOADER) or {}
        except yaml.YAMLError as e:
            ERRORS.append("%s does not parse: %s" % (name, e))
            continue
        for _p, m in (d.get("paths") or {}).items():
            if not isinstance(m, dict):
                continue
            for v, op in m.items():
                if v in VERBS and isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = name
    return out


def _derive_lineage():
    import importlib.util
    spec = importlib.util.spec_from_file_location("derive_lineage", os.path.join(ROOT, "tools", "derive-lineage.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def override_findings(overrides, ops, cols, fresh=None, view=None):
    """LN-OVERRIDE: (errors, warnings) for the override list. `ops` is operationId -> contract, `cols` the
    schema reference's tables, `fresh` (optional) operationId -> {reads, writes} as the contracts derive them,
    `view` (optional) (table, operationId) -> True for a read view the operation may read (rule 6)."""
    errs, warns = [], []
    entries = overrides.get("operations") or {}
    for o, v in sorted(entries.items()):
        if o not in ops:
            errs.append("LN-OVERRIDE %s: an override for an operation no contract declares" % o)
            continue
        if not str(v.get("reason") or "").strip():
            errs.append("LN-OVERRIDE %s: an override with no reason" % o)
        for k in ("reads", "writes", "notReads", "notWrites"):
            for tb in v.get(k) or []:
                if ":" not in tb and tb not in cols and not (k == "reads" and view and view(tb, o)):
                    errs.append("LN-OVERRIDE %s: %s names '%s', which is in no schema" % (o, k, tb))
        if fresh and o in fresh:
            red = sorted(set(v.get("reads") or []) & set(fresh[o].get("reads") or [])) +                 sorted(set(v.get("writes") or []) & set(fresh[o].get("writes") or []))
            if red:
                warns.append("LN-OVERRIDE %s: the contract now derives %s; remove it from the override"
                             % (o, ", ".join(red)))
    carried = sum(1 for v in entries.values() if v.get("carried"))
    ceiling = overrides.get("carriedCeiling")
    if ceiling is not None and carried > int(ceiling):
        errs.append("LN-OVERRIDE %d carried entries against a ceiling of %s: a carried entry is never added; state "
                    "the read or write in the contract, or add an override with its own reason" % (carried, ceiling))
    return errs, warns


def self_test():
    """The override rules on a made-up list; a failure here means the check is broken, not the package."""
    fails = []
    ops = {"getA": "a", "setA": "a"}
    cols = {"a.t": [], "a.u": []}
    good = {"carriedCeiling": 1, "operations": {"getA": {"reads": ["a.u"], "reason": "why", "carried": True}}}
    if override_findings(good, ops, cols) != ([], []):
        fails.append("a good override list is reported")
    bad = {"carriedCeiling": 0, "operations": {
        "gone": {"reads": ["a.t"], "reason": "x"},
        "getA": {"reads": ["a.nope"], "reason": "", "carried": True},
        "setA": {"writes": ["a.t"], "reason": "y"}}}
    errs, warns = override_findings(bad, ops, cols, {"setA": {"reads": [], "writes": ["a.t"]}})
    for want in ("gone: an override for an operation", "getA: an override with no reason", "'a.nope'",
                 "1 carried entries against a ceiling of 0"):
        if not any(want in e for e in errs):
            fails.append("not reported: " + want)
    if not any("setA: the contract now derives a.t" in w for w in warns):
        fails.append("a redundant override is not reported")
    return fails


def main():
    fails = self_test()
    if fails:
        for f in fails:
            print("  SELF-TEST FAIL  %s" % f)
        print("FAIL - %d self-test(s)" % len(fails))
        return 1
    quiet = "--quiet" in sys.argv
    lin = load_json("api-data-lineage.json")
    ref = load_json("schema-reference.json")
    dec = load_json("service-decomposition.json", required=False)
    if not lin:
        print("FAIL - no lineage to check")
        return 1

    ops = contract_operations()
    cols = ref.get("cols") or {}
    svc_of_contract, schema_owner = {}, collections.defaultdict(list)
    for name, s in (dec.get("services") or {}).items():
        for c in (s.get("contracts") or []):
            svc_of_contract[c] = name
        for sch in (s.get("schemas") or []):
            schema_owner[sch].append(name)

    # 1 + 2 — the two sets must be the same set.
    ghosts = sorted(set(lin) - set(ops))
    absent = sorted(set(ops) - set(lin))
    for g in ghosts:
        ERRORS.append("lineage has '%s', which no contract defines — `--apply` never "
                      "removes, so a renamed operation stays forever" % g)
    for a in absent:
        ERRORS.append("'%s' is in a contract and not in the lineage — run "
                      "tools/derive-lineage.py --apply" % a)

    # 3 + 4 + 5 — attribution.
    wrong_contract = wrong_service = null_service = 0
    for o, e in sorted(lin.items()):
        if o not in ops:
            continue
        if e.get("contract") != ops[o]:
            wrong_contract += 1
            ERRORS.append("%s: lineage says contract '%s', it is declared in '%s'"
                          % (o, e.get("contract"), ops[o]))
        if not e.get("service"):
            null_service += 1
            ERRORS.append("%s: no service — derive-diagrams sorts on this and raises on None"
                          % o)
        elif svc_of_contract and ops[o] in svc_of_contract \
                and e["service"] != svc_of_contract[ops[o]]:
            wrong_service += 1
            ERRORS.append("%s: lineage says %s, service-decomposition puts '%s' in %s"
                          % (o, e["service"], ops[o], svc_of_contract[ops[o]]))

    # 6 — a table an operation claims to touch has to exist.
    # **A read view is not a table** (14 October 2026, CHG-R6G-007). DB-READ-VIEWS publishes `<table>_for_<reader>` over
    # an owner's table for bulk reads within one deployable (ADR-0055 rule 2), and the lineage names such a read by the
    # view (check-cross-module-reads accepts it). It exists when its table does and the reader is the operation's own
    # module; it is read, never written.
    names_of = {}
    for name, s in (dec.get("services") or {}).items():
        names_of[name] = {name[:-len("Service")].lower() if name.endswith("Service") else name.lower()} | {
            x.replace("-", "_") for x in (s.get("contracts") or []) + (s.get("schemas") or [])}
    view = re.compile(r"^(\w+)\.(\w+)_for_([a-z0-9_]+)$")

    def read_view(t, service):
        m = view.match(t)
        return bool(m) and f"{m.group(1)}.{m.group(2)}" in cols and m.group(3) in names_of.get(service, set())

    unknown = collections.Counter()
    for o, e in lin.items():
        for kind in ("reads", "writes"):
            for t in e.get(kind) or []:
                if ":" in t:          # cache:idempotency, qdrant:knowledge — not postgres
                    continue
                if t not in cols and not (kind == "reads" and read_view(t, e.get("service"))):
                    unknown[t] += 1
    for t, n in unknown.most_common():
        ERRORS.append("%d operation(s) read or write '%s', which is in no schema — a table "
                      "that does not exist is rebuilt by derive-schema from these entries"
                      % (n, t))

    # 7 — ownership.
    orphan_tables = [t for t in cols
                     if ":" not in t and not schema_owner.get(t.split(".")[0])]
    if orphan_tables and dec:
        WARNINGS.append("%d table(s) belong to no service — %s%s"
                        % (len(orphan_tables), ", ".join(sorted(orphan_tables)[:5]),
                           "…" if len(orphan_tables) > 5 else ""))
    for sch, owners in sorted(schema_owner.items()):
        if len(owners) > 1:
            ERRORS.append("schema '%s' is claimed by %s — a service that shares a schema is "
                          "not separately deployable" % (sch, " and ".join(owners)))

    # 8 — LN-TEXT (r8, CHG-R8LIN-001): the lineage is the build boundary ("reads only the tables its spec lists"),
    # so a table the operation's own description names and the lineage lists nowhere is a gap the developer meets as a
    # refusal they cannot build (r8 walk of Sprint 1 and 2: IDENTITY-C10, ORDERS-MONEY-C18, APPROVALS-TENANCY-C03 ...).
    # Reported as a warning with the count, `--text` lists every one; a mention may be a deliberate "not X", so it is
    # never a failure. Fix the lineage entry (hand-maintained) or reword the text.
    text_gaps = []
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        try:
            d = yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}
        except yaml.YAMLError:
            continue
        for _p, m in (d.get("paths") or {}).items():
            if not isinstance(m, dict):
                continue
            for v, op in m.items():
                if v not in VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                e = lin.get(op["operationId"])
                if not e:
                    continue
                said = set(re.findall(r"([a-z][a-z_]*\.[a-z][a-z_]*)",
                                      str(op.get("summary") or "") + " " + str(op.get("description") or ""))) & set(cols)
                gone = sorted(t for t in said if t not in (e.get("reads") or []) and t not in (e.get("writes") or []))
                if gone:
                    text_gaps.append((op["operationId"], gone))
    if text_gaps:
        WARNINGS.append("LN-TEXT: %d operation(s) name a table in their own text that their lineage entry neither reads "
                        "nor writes (--text lists them)" % len(text_gaps))
    if "--text" in sys.argv:
        for o, g in text_gaps:
            print("  LN-TEXT  %-36s %s" % (o, ", ".join(g)))

    # 9 + 10 -- LN-DERIVED and LN-OVERRIDE (20 October 2026, CHG-R8GEN-001). The lineage is derived from the contracts
    # and the override list; a hand edit to the lineage, or a contract changed without the derive, shows here.
    dl = _derive_lineage()
    overrides = dl.load_overrides()
    fresh = dl.derive(lin)
    oerrs, owarns = override_findings(overrides, ops, cols, fresh,
                                      lambda tb, o: read_view(tb, (lin.get(o) or {}).get("service")))
    ERRORS.extend(oerrs)
    WARNINGS.extend(owarns[:20])
    if len(owarns) > 20:
        WARNINGS.append("LN-OVERRIDE %d more redundant override(s)" % (len(owarns) - 20))
    want = dl.expected(lin, fresh, overrides)
    drift = 0
    for o in sorted(set(want) & set(lin)):
        bad = [k for k in ("reads", "writes") + dl.CONTRACT_FIELDS if not dl._same(want[o].get(k), lin[o].get(k))]
        bad += [k for k in ("readVia", "writeVia") if want[o].get(k) != lin[o].get(k)]
        if bad:
            drift += 1
            if drift <= 25:
                ERRORS.append("LN-DERIVED %s: %s differ from what the contract and the override list give -- run "
                              "tools/derive-lineage.py --apply (never edit the lineage by hand; an override goes in "
                              "handoff/api-data-lineage-overrides.json with its reason)" % (o, ", ".join(bad)))
    if drift > 25:
        ERRORS.append("LN-DERIVED %d more entr(ies) differ" % (drift - 25))

    # Coverage — reported, never failed.
    #
    # **An operation with `service` or `device` as its only audience is complete without a
    # screen.** `accrueLoyaltyPoints` is called when an order completes, `submitQueueReading`
    # by a sensor, `getSignageQueueBoard` by a display on a wall. Counting them as unwired
    # makes the wiring figure permanently unreachable and hides the operations that really
    # are missing a surface, so they are reported as their own number rather than folded into
    # either side.
    no_table = [o for o, e in lin.items() if not (e.get("reads") or e.get("writes"))]
    by_service = collections.Counter(e.get("service") for e in lin.values())

    screened = set()
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        try:
            d = yaml.load(io.open(f, encoding="utf-8"), Loader=_LOADER) or {}
        except yaml.YAMLError:
            continue
        for s in (d.get("screens") or []):
            for a in (s.get("apis") or []):
                if a.get("operationId"):
                    screened.add(a["operationId"])
    machine = set()
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        try:
            d = yaml.load(io.open(f, encoding="utf-8"), Loader=_LOADER) or {}
        except yaml.YAMLError:
            continue
        for _p, m in (d.get("paths") or {}).items():
            if not isinstance(m, dict):
                continue
            for v, op in m.items():
                if v not in VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                aud = set(op.get("x-ticvai-audience") or [])
                if aud and aud <= {"service", "device"}:
                    machine.add(op["operationId"])
    total = len(ops)
    wired = len(set(ops) & screened)
    auto = len(machine - screened)
    gap = total - wired - auto

    if not quiet:
        print("  %d lineage entries · %d contract operations · %d tables"
              % (len(lin), len(ops), len(cols)))
        print("  %d service(s) · %d operation(s) reach no table (%.0f%%)"
              % (len(by_service), len(no_table), 100.0 * len(no_table) / max(1, len(lin))))
        print()
        print("  surfaced by a screen   %5d  %5.1f%%" % (wired, 100.0 * wired / max(1, total)))
        print("  machine-called, no UI  %5d  %5.1f%%   service/device audience — complete"
              % (auto, 100.0 * auto / max(1, total)))
        print("  ----------------------------------")
        print("  accounted for          %5d  %5.1f%%" % (wired + auto,
                                                         100.0 * (wired + auto) / max(1, total)))
        print("  no surface yet         %5d  %5.1f%%" % (gap, 100.0 * gap / max(1, total)))
        print()
        for e in ERRORS[:40]:
            print("  FAIL  %s" % e)
        if len(ERRORS) > 40:
            print("  ... and %d more" % (len(ERRORS) - 40))
        for w in WARNINGS:
            print("  WARN  %s" % w)
        if ERRORS:
            print()

    print("%s — %d error(s), %d warning(s)"
          % ("FAIL" if ERRORS else "PASS", len(ERRORS), len(WARNINGS)))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
