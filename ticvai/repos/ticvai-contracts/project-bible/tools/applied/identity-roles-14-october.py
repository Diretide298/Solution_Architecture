#!/usr/bin/env python3
"""The lineage half of the r6 identity settlement (14 October 2026, batch IDR: ADAM CR-076, CR-077, CR-079).

**Found by the audit of the CRs raised on 14 October** (developer of ticket 27764, SVC-IDENTITY-ADMINISTRATION-1): the
contract says what an operation returns and the lineage did not list the tables it takes it from, so a developer
building `listPrincipals` to its lineage could not fill `Principal.roles`, and `createPrincipal.roleIds` landed nowhere.
The contracts were edited by hand in the same commits (contracts/spine/identity.yaml, tenancy.yaml, shared/common.yaml);
this one-off gives `handoff/api-data-lineage.json` the reads, writes and scope those edits declare, the way
`contracts-s12-4-october.py` did for CHG-FXC-004. `derive-lineage --apply` adds and never updates, so an existing
entry only changes through a tool like this one.

* CHG-IDR-001 (CR-076): `createRole` and `updateRole` are called at the tenant scope (BC-076, BC-077); their entries'
  `scope` follows the contract.
* CHG-IDR-002 (CR-077): `listPrincipals` and `getPrincipal` read the live role grants and the roles (`Principal.roles`)
  and the home scope's node (`platform.scope`); `listRoles` counts live grants (`principalCount`, `grantCount`, computed
  under RLS); `createPrincipal` writes one `identity.delegated_access` row per `roleIds` entry at the home scope.
* CHG-IDR-003 (CR-079): `createRole` writes `platform.audit_record`; every operation that runs the segregation check
  reads `identity.segregation_rule` and the permission sets it compares.

    python tools/applied/identity-roles-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# op: (reads to add, writes to add, writes to remove, reads to remove, why)
LINEAGE = {
    "listPrincipals": (["identity.delegated_access", "identity.role", "platform.scope"], [], [], [],
                       "Principal.roles from the live role grants joined to the role; the home scope's path filters "
                       "the list (CHG-IDR-001, CHG-IDR-002)"),
    "getPrincipal": (["identity.delegated_access", "identity.role", "platform.scope"], [], [], [],
                     "Principal.roles from the live role grants joined to the role; the home scope decides "
                     "visibility (CHG-IDR-001, CHG-IDR-002)"),
    "listRoles": (["identity.delegated_access"], [], [], [],
                  "principalCount and grantCount counted from the live grants under RLS (CHG-IDR-002)"),
    "createPrincipal": (["identity.role", "identity.role_permission", "identity.segregation_rule",
                         "identity.delegated_access", "platform.scope"],
                        ["identity.delegated_access", "cache:resolution"], [], [],
                        "each roleIds entry becomes one delegated_access row at the home scope, under the "
                        "segregation check, and evicts the permissions resolution as createDelegatedAccess does "
                        "(CHG-IDR-002, CHG-IDR-003)"),
    "createRole": ([], ["platform.audit_record"], [], [],
                   "the create is audited, as setRolePermissions is (CHG-IDR-003)"),
    "createDelegatedAccess": (["identity.role", "identity.role_permission", "identity.segregation_rule",
                               "identity.module_access"], [], [], [],
                              "the grant-time segregation check over everything the principal would hold "
                              "(CHG-IDR-003)"),
    "setPrincipalModuleAccess": (["identity.delegated_access", "identity.role_permission",
                                  "identity.segregation_rule"], [], [], [],
                                 "the grant-time segregation check over everything the principal would hold "
                                 "(CHG-IDR-003)"),
}
# op: the scope level its contract now declares (BC-076, BC-077)
SCOPE = {"createRole": "tenant", "updateRole": "tenant"}


def apply_lineage(apply: bool) -> int:
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    lin = json.load(io.open(path, encoding="utf-8"))
    sref = json.load(io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8"))["cols"]
    n = 0
    for op, (r_add, w_add, w_del, r_del, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:
            raise SystemExit("%s: no lineage entry" % op)
        for t in r_add + w_add:
            if t not in sref and ":" not in t:
                raise SystemExit("%s: %s is not a table" % (op, t))
        reads = (set(e.get("reads") or []) | set(r_add)) - set(r_del)
        writes = (set(e.get("writes") or []) | set(w_add)) - set(w_del)
        if sorted(reads) != sorted(e.get("reads") or []) or sorted(writes) != sorted(e.get("writes") or []):
            e["reads"], e["writes"] = sorted(reads), sorted(writes)
            note = "14 October 2026 (ADAM CR-076/077/079): " + why
            e["fixNote"] = (e["fixNote"] + "; " + note) if e.get("fixNote") else note  # an earlier note is kept
            n += 1
    for op, level in SCOPE.items():
        e = lin.get(op)
        if e is not None and e.get("scope") != level:
            e["scope"] = level
            n += 1
    # The `cache` record of an entry that now touches cache:resolution, by the one rule derive-lineage applies
    # (tools/resolution_cache.py, CHG-FXC-001), so check-write-lineage W-CACHEKEY holds before the next refresh.
    import importlib.util as _ilu
    spec = _ilu.spec_from_file_location("resolution_cache", os.path.join(ROOT, "tools", "resolution_cache.py"))
    rc = _ilu.module_from_spec(spec)
    spec.loader.exec_module(rc)
    for op in LINEAGE:
        want = rc.resolution_cache(op, lin[op], lin)
        if want and lin[op].get("cache") != want:
            lin[op]["cache"] = want
            n += 1
    if apply and n:
        io.open(path, "w", encoding="utf-8").write(json.dumps(lin, indent=1, ensure_ascii=False))
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    n = apply_lineage(a.apply)
    print("lineage entries %s: %d%s" % ("changed" if a.apply else "to change", n,
                                        "" if a.apply else "; pass --apply"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
