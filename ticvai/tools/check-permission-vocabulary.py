#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One permission vocabulary: every place that names a permission names a value of the one enum.

**Why** (20 October 2026, r8 second fix round, generators lane extra item 4, CHG-R8GEN-003). The package names
permissions in five places: the `Permission` enum in `contracts/shared/permissions.yaml` (the source), each
operation's `x-ticvai-permission` and `x-ticvai-permission-escalated`, the module checklist
`x-ticvai-permission-modules` in the same file (what a role is built from), `roles.yaml`'s presets (an action key
maps to enum values with `permission:`), and two derived copies, the lineage's `perm` and `roles-by-app.yaml`. On
20 October 178 lineage entries named a permission the contract no longer required, and roles-by-app.yaml still said
the two vocabularies shared no key, written before roles.yaml's keys were mapped to the enum. This check holds all
of them to the enum in one place; the derived copies are also held to their derivation (check-lineage LN-DERIVED,
check-regenerate-twice).

    PV-OPERATION  an operation's x-ticvai-permission, x-ticvai-permission-escalated or x-ticvai-permission-by-module
                  value is not in the enum
    PV-MODULES    an enum value is in no module of x-ticvai-permission-modules, or in two; a module lists a value
                  the enum does not have
    PV-ROLES      a roles.yaml grant maps to a value the enum does not have
    PV-LINEAGE    the lineage's perm differs from the contract's x-ticvai-permission (run derive-lineage --apply)
    PV-BY-APP     roles-by-app.yaml lists a value the enum does not have (run derive-app-roles)
    unused        (reported, not failed) enum values no operation, preset or screen names: a grant a role can be
                  given that nothing checks

    python tools/check-permission-vocabulary.py [--self-test]
"""
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
VERBS = ("get", "post", "put", "patch", "delete")


def load(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    with io.open(p, encoding="utf-8") as fh:
        return json.load(fh) if p.endswith(".json") else yaml.load(fh, Loader=LOADER)


def operation_permissions(docs, ai_publish=None):
    """[(operationId, key, value)] for every permission an operation names."""
    out = []
    for _f, d in docs:
        for _p, item in ((d or {}).get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for v, op in item.items():
                if v not in VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                for key in ("x-ticvai-permission", "x-ticvai-permission-escalated"):
                    if op.get(key):
                        out.append((op["operationId"], key, str(op[key])))
                by_mod = op.get("x-ticvai-permission-by-module")
                if isinstance(by_mod, dict) and ai_publish is not None:
                    # `permissions` points at the module -> permission map in permissions.yaml; each value counts.
                    if str(by_mod.get("permissions") or "").endswith("#/x-ticvai-module-ai-publish"):
                        for x in (ai_publish or {}).values():
                            out.append((op["operationId"], "x-ticvai-permission-by-module", str(x)))
                    else:
                        out.append((op["operationId"], "x-ticvai-permission-by-module",
                                    "unresolved map %s" % by_mod.get("permissions")))
    return out


def findings(enum, op_perms, modules, roles, lineage, contract_perm, by_app):
    errs = []
    vocab = set(enum)
    for o, key, val in op_perms:
        if val not in vocab:
            errs.append("PV-OPERATION %s: %s %s is not in the Permission enum" % (o, key, val))
    seen = {}
    for mod, vals in (modules or {}).items():
        for v in vals or []:
            if v not in vocab:
                errs.append("PV-MODULES module %s lists %s, which the Permission enum does not have" % (mod, v))
            elif v in seen:
                errs.append("PV-MODULES %s is in module %s and in %s; a permission sits in exactly one" % (v, seen[v], mod))
            else:
                seen[v] = mod
    for v in enum:
        if modules is not None and v not in seen:
            errs.append("PV-MODULES %s is in no module of x-ticvai-permission-modules, so no role checklist offers it" % v)
    for role, r in ((roles or {}).get("roles") or {}).items():
        for g in (r or {}).get("grants") or []:
            ps = g.get("permission")
            for p in ([ps] if isinstance(ps, str) else (ps or [])):
                if p not in vocab:
                    errs.append("PV-ROLES roles.yaml %s grant %s maps to %s, which the Permission enum does not have"
                                % (role, g.get("key"), p))
    for o, e in sorted((lineage or {}).items()):
        if o in contract_perm and (e.get("perm") or None) != (contract_perm[o] or None):
            errs.append("PV-LINEAGE %s: the lineage says %s, the contract %s (python tools/derive-lineage.py --apply)"
                        % (o, e.get("perm"), contract_perm[o]))
    for app, a in ((by_app or {}).get("apps") or {}).items():
        for tier, vals in ((a or {}).get("tiers") or {}).items():
            for v in vals or []:
                if v not in vocab:
                    errs.append("PV-BY-APP roles-by-app.yaml %s %s lists %s, not in the enum (python "
                                "tools/derive-app-roles.py)" % (app, tier, v))
    return errs


def self_test():
    fails = []
    enum = ["A_VIEW", "A_MANAGE", "B_VIEW"]
    ok = findings(enum, [("getA", "x-ticvai-permission", "A_VIEW")], {"a": ["A_VIEW", "A_MANAGE"], "b": ["B_VIEW"]},
                  {"roles": {"r": {"grants": [{"key": "a.x", "permission": "A_MANAGE"}]}}},
                  {"getA": {"perm": "A_VIEW"}}, {"getA": "A_VIEW"}, {"apps": {"x": {"tiers": {"read": ["A_VIEW"]}}}})
    if ok:
        fails.append("a consistent vocabulary is reported: %s" % ok)
    bad = findings(enum, [("getA", "x-ticvai-permission", "A_READ")], {"a": ["A_VIEW", "A_VIEW", "Z"]},
                   {"roles": {"r": {"grants": [{"key": "a.x", "permission": "A_EDIT"}]}}},
                   {"getA": {"perm": "B_VIEW"}}, {"getA": "A_VIEW"}, {"apps": {"x": {"tiers": {"read": ["Q"]}}}})
    for want in ("PV-OPERATION getA", "lists Z", "A_VIEW is in module a and in a", "A_MANAGE is in no module",
                 "maps to A_EDIT", "PV-LINEAGE getA", "lists Q"):
        if not any(want in e for e in bad):
            fails.append("not reported: " + want)
    return fails


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    fails = self_test()
    if fails or "--self-test" in sys.argv:
        for f in fails:
            print("  SELF-TEST FAIL  " + f)
        print("%s - %d self-test(s) failed" % ("FAIL" if fails else "PASS", len(fails)))
        return 1 if fails else 0
    perms = load("contracts/shared/permissions.yaml") or {}
    enum = (((perms.get("components") or {}).get("schemas") or {}).get("Permission") or {}).get("enum") or []
    if not enum:
        print("FAIL - contracts/shared/permissions.yaml has no Permission enum")
        return 1
    modules = (perms.get("x-ticvai-permission-modules") or {}).get("modules")
    docs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        with io.open(f, encoding="utf-8") as fh:
            docs.append((f, yaml.load(fh, Loader=LOADER)))
    op_perms = operation_permissions(docs, (perms.get("x-ticvai-module-ai-publish") or {}).get("modules") or {})
    contract_perm = {}
    for _f, d in docs:
        for _p, item in ((d or {}).get("paths") or {}).items():
            for v, op in (item or {}).items() if isinstance(item, dict) else []:
                if v in VERBS and isinstance(op, dict) and op.get("operationId"):
                    contract_perm[op["operationId"]] = op.get("x-ticvai-permission")
    roles = load("roles.yaml")
    errs = findings(enum, op_perms, modules, roles, load("handoff/api-data-lineage.json"), contract_perm,
                    load("roles-by-app.yaml"))
    used = {v for _o, _k, v in op_perms}
    used |= {p for r in ((roles or {}).get("roles") or {}).values() for g in (r or {}).get("grants") or []
             for p in ([g.get("permission")] if isinstance(g.get("permission"), str) else (g.get("permission") or []))}
    screen_text = ""
    for f in sorted(glob.glob(os.path.join(ROOT, "screens", "P*.yaml"))):
        with io.open(f, encoding="utf-8") as fh:
            screen_text += fh.read()
    unused = sorted(v for v in enum if v not in used and v not in screen_text)
    print("  %d permission(s) in the enum; %d named by operations, %d by roles.yaml presets"
          % (len(enum), len({v for _o, _k, v in op_perms}), len(used - {v for _o, _k, v in op_perms})))
    if unused:
        print("  note  %d enum value(s) no operation, preset or screen names (a grant nothing checks): %s"
              % (len(unused), ", ".join(unused)))
    for e in errs[:60]:
        print("  " + e)
    if len(errs) > 60:
        print("  ... and %d more" % (len(errs) - 60))
    print("%s - %d finding(s)" % ("FAIL" if errs else "PASS", len(errs)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
