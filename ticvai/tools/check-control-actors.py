#!/usr/bin/env python3
"""A Control Plane actor is a platform operator, never a tenant principal (r14, CHG-R14J-011).

**Why** (the r13 system review, finding A-13, 3 November 2026). ADR-0072 made the person who acts in the Control
Plane a `control.platform_operator`, "never a tenant `identity.principal`". The contracts' field naming
(`*ByPrincipalId`) still mapped every Control Plane actor to `identity.principal` by convention, and
backend/990-cross-database-references.sql told the caller to keep that rule: code validating
`control.migration_run.started_by_principal_id` or `control.rollout.approved_by_principal_id` against
`identity.principal` (a table in a tenant's database) rejects every operator, or looks in the wrong database. The
fix is in the contracts (`x-ticvai-references: control.platform_operator` on the actor fields); this keeps it:

  CA-OPERATOR   a control-schema column that references `identity.principal` (declared or by the name rule) on a
                table every writing operation of which is a staff operation (`x-ticvai-audience: [staff]`) needing a
                `PLATFORM_*` permission: only a platform operator holds one (ADR-0072 2, R203), so the actor is a
                `control.platform_operator` and the field says so with `x-ticvai-references: control.platform_operator`.
                A partner- or prospect-facing writer carrying a PLATFORM_* permission is review finding F-02's
                (non-staff surfaces with platform permissions), not judged here

A column written by a tenant or partner operation (`control.partner_user.principal_id`, a partner's own users in the
tenant's identity) is not judged here: its actor is a tenant principal and the cross-database rule is real.

Reads handoff/schema-reference.json (the columns and their references), handoff/api-data-lineage.json (which
operations write a table) and the contracts (each operation's `x-ticvai-permission`).

    python tools/check-control-actors.py [--self-test]      (the self-test runs first, every time)

Read-only. Exit 1 on a finding.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

ROOT = g.ROOT
RULES = {"CA-OPERATOR": "a Control Plane actor column references identity.principal on a table only PLATFORM_* "
                        "operations write: the actor is a control.platform_operator (ADR-0072; review A-13)"}
OPERATOR = "control.platform_operator"


def findings(cols: dict, writers: dict, permission: dict) -> list:
    """[(table.column, message)]. cols: table -> [column rows]; writers: table -> [operationId];
    permission: operationId -> {"permission": x-ticvai-permission, "audience": x-ticvai-audience}."""
    out = []
    for t, rows in sorted(cols.items()):
        if not t.startswith("control."):
            continue
        ws = sorted(writers.get(t) or [])
        if not ws or not all(str((permission.get(w) or {}).get("permission") or "").startswith("PLATFORM_")
                             and set((permission.get(w) or {}).get("audience") or ["staff"]) <= {"staff"}
                             for w in ws):
            continue
        for c in rows:
            if c.get("references") == "identity.principal":
                out.append((f"{t}.{c['column']}",
                            f"{t}.{c['column']} references identity.principal, and every operation that writes {t} "
                            f"({', '.join(ws[:4])}{' and more' if len(ws) > 4 else ''}) is a staff operation "
                            f"needing a PLATFORM_* permission: mark its contract field (source {c.get('source')}) "
                            f"x-ticvai-references: {OPERATOR} (ADR-0072)"))
    return out


def self_test() -> int:
    cols = {"control.rollout": [{"column": "started_by_principal_id", "references": "identity.principal",
                                 "source": "platform-ops.Rollout.startedByPrincipalId"}],
            "control.partner_user": [{"column": "principal_id", "references": "identity.principal"}],
            "control.release": [{"column": "created_by_principal_id", "references": OPERATOR}],
            "orders.order": [{"column": "created_by_principal_id", "references": "identity.principal"}]}
    writers = {"control.rollout": ["startRollout"], "control.partner_user": ["createPartnerUser"],
               "control.release": ["createRelease"], "orders.order": ["createOrder"]}
    perm = {"startRollout": {"permission": "PLATFORM_RELEASE_PROMOTE", "audience": ["staff"]},
            "createPartnerUser": {"permission": "PARTNER_MANAGE", "audience": ["staff", "partner"]},
            "createRelease": {"permission": "PLATFORM_RELEASE_MANAGE", "audience": ["staff"]},
            "createOrder": {"permission": "ORDER_CREATE", "audience": ["staff"]},
            "partnerAsks": {"permission": "PLATFORM_CELL_MANAGE", "audience": ["partner"]}}
    cases = [("an operator's column naming identity.principal fails", [k for k, _ in findings(cols, writers, perm)],
              ["control.rollout.started_by_principal_id"]),
             ("a mixed writer set is not judged", [k for k, _ in findings(
                 cols, dict(writers, **{"control.rollout": ["startRollout", "createPartnerUser"]}), perm)], []),
             ("a table nothing writes is not judged", [k for k, _ in findings(cols, {}, perm)], []),
             ("a partner-facing writer is not judged, whatever its permission", [k for k, _ in findings(
                 cols, dict(writers, **{"control.rollout": ["partnerAsks"]}), perm)], [])]
    fails = [f"{n}: got {got!r}, expected {want!r}" for n, got, want in cases if got != want]
    for f in fails:
        print("  FAIL", f)
    print(f"check-control-actors self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def load_permissions() -> dict:
    out = {}
    for p in sorted((ROOT / "contracts").glob("*/*.yaml")):
        if p.parent.name == "shared":
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for pi in (d.get("paths") or {}).values():
            for o in (pi or {}).values():
                if isinstance(o, dict) and o.get("operationId"):
                    out[o["operationId"]] = {"permission": o.get("x-ticvai-permission"),
                                             "audience": o.get("x-ticvai-audience")}
    return out


def main() -> int:
    g.force_utf8()
    if self_test():
        print("FAIL - the self-test failed")
        return 1
    if "--self-test" in sys.argv[1:]:
        return 0
    guard = g.Guard("check-control-actors", RULES)
    sr = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    writers = defaultdict(list)
    for op, v in lineage.items():
        for t in (v or {}).get("writes") or []:
            writers[t].append(op)
    found = findings(sr.get("cols") or {}, writers, load_permissions())
    for key, msg in found:
        guard.add("CA-OPERATOR", key, msg)
    n = sum(1 for t, rows in (sr.get("cols") or {}).items() if t.startswith("control.")
            for c in rows if c.get("references") == OPERATOR)
    guard.note(f"{n} control column(s) reference {OPERATOR}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
