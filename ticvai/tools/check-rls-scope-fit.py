#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A table's row-level security lets in the scope its operations run at (ADAM CR-076, CHG-GEN-010, 14 October 2026).

**The policy class and the scope level were chosen by two different things and nothing compared them.** derive-ddl
picks a table's policy by rule (scope_path, venue_id, the owning parent, subject, else the tenant root, SD-015), and
each operation's contract declares its `x-ticvai-scope-level`. listRoles, createRole and listPrincipals are
venue-level and their tables were tenant-root only, so a venue's ROLE_MANAGE read nothing and wrote nothing (CR-076);
region settings (CR-075), retail sale lines (CR-071) and every supplier and upsell rule (R183) had the same shape.
The audit of 14 October counted 520 operations below tenant touching 142 tenant-root tables, and 47 scope_path tables
written only at tenant and read below it.

The policy a table has is read from the DDL the databases get: the generated baseline, then every forward migration
in order (a later `apply_*_rls` call replaces an earlier one, as CHG-GEN-004 writes them). Derive before check: run
derive-ddl first, so a policy changed in a contract is in the forward migration this reads. A parent-owned table takes
its parent's class; a split policy (CHG-GEN-005) reads one way and writes another.

    RF-TENANT-ROOT   an operation below tenant (region, brand, venue, workstation) reads a table only the tenant root
                     may read, or writes one only the tenant root may write
    RF-OWNED-ABOVE   an operation below tenant reads a scope_path table every writer of which runs at tenant level, so
                     its rows sit at the tenant's path, above the reader, and the policy is not read-beneath

Only operations a staff or partner principal calls are judged: a guest reads its own rows by subject, and a worker
(audience `service` or `device` only) runs under the tenant root or a system scope. Today's findings are baselined in
handoff/audit-baseline.json; the tables CHG-GEN-005, CHG-GEN-007 and CHG-GEN-008 changed must pass.

    python tools/check-rls-scope-fit.py [--all] [--update-baseline]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import ddl_forward as fwd  # noqa: E402

RULES = {
    "RF-TENANT-ROOT": "an operation below tenant reads or writes a table only the tenant root may (CR-076, CHG-GEN-010)",
    "RF-OWNED-ABOVE": "an operation below tenant reads a scope_path table written only at tenant, without read-beneath "
                      "(R183, CR-076)",
}
BELOW_TENANT = {"region", "brand", "venue", "workstation"}
JUDGED_AUDIENCE = {"staff", "partner"}
CALL = re.compile(r"^SELECT platform\.(apply_\w+_rls)\('([^']+)'::regclass(.*)\)$", re.S)


def policies(backend: Path) -> dict:
    """table -> (helper, the rest of the call's arguments), the last call in apply order."""
    d = backend / "tenant"
    files = sorted(p for p in d.glob("*.sql") if not p.name.startswith("V"))
    files += sorted((p for p in d.glob("V*.sql") if re.match(r"V\d+__", p.name)),
                    key=lambda p: int(re.match(r"V(\d+)", p.name).group(1)))
    out = {}
    for f in files:
        text = re.split(r"^-- =+\n-- ROLLBACK\b", f.read_text(encoding="utf-8"), maxsplit=1, flags=re.M)[0]
        for st in fwd.split_statements(text):
            m = CALL.match(fwd.norm(st))
            if m and m.group(1) != "apply_split_rls":
                out[fwd.unq(m.group(2))] = (m.group(1), m.group(3))
    return out


def classes(pol: dict) -> dict:
    """table -> (who may read, who may write), each one of 'tenant' (the tenant root only), 'scope' (at or beneath
    the row's owner), 'above' (at, beneath or above the owner), 'any' (any grant), 'subject'."""
    memo: dict = {}

    def parent_of(args: str):
        m = re.match(r"\s*,\s*'([^']+)'\s*,\s*'([^']+)'::regclass", args)
        return fwd.unq(m.group(2)) if m else None

    def write_of(arg: str) -> str:
        if "tenant_root_in_scope" in arg:
            return "tenant"
        if "subject_in_scope" in arg:
            return "subject"
        return "scope"

    def cls(t: str, depth: int = 0):
        if t in memo:
            return memo[t]
        if t not in pol or depth > 20:
            return None
        helper, args = pol[t]
        r = None
        if helper == "apply_tenant_rls":
            r = ("tenant", "tenant")
        elif helper in ("apply_scope_rls", "apply_venue_rls", "apply_shared_scope_rls"):
            r = ("scope", "scope")
        elif helper == "apply_subject_rls":
            r = ("subject", "subject")
        elif helper == "apply_append_audit_rls":
            r = ("tenant", "any")
        elif helper == "apply_read_beneath_rls":
            r = ("above", "scope")
        elif helper == "apply_grant_holder_read_rls":
            m = re.search(r"'((?:[^']|'')*)'", args)
            r = ("any", write_of(m.group(1) if m else ""))
        elif helper == "apply_grant_holder_subject_read_rls":
            # a subject-owned table opened to staff grants, still read by its own guest (CHG-MOD-007)
            r = ("any", "subject")
        elif helper in ("apply_parent_rls", "apply_parent_split_rls"):
            p = parent_of(args)
            pc = cls(p, depth + 1) if p else None
            if pc:
                r = pc if helper == "apply_parent_rls" else (pc[0], pc[1])
        memo[t] = r
        return r

    return {t: cls(t) for t in pol}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-rls-scope-fit", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ref = (g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}
    pol = policies(g.ROOT / "backend")
    cl = classes(pol)
    has_path = {t for t, cols in ref.items() if any(c.get("column") == "scope_path" for c in cols)}
    writers: dict = {}
    for o, e in lin.items():
        for t in e.get("writes") or []:
            writers.setdefault(t, set()).add(str(e.get("scope")))
    for o, e in sorted(lin.items()):
        level = str(e.get("scope"))
        if level not in BELOW_TENANT or not (set(e.get("audience") or []) & JUDGED_AUDIENCE):
            continue
        for kind in ("reads", "writes"):
            for t in e.get(kind) or []:
                c = cl.get(t)
                if not c:
                    continue
                read, write = c
                if kind == "reads" and read in ("tenant", "subject"):
                    guard.add("RF-TENANT-ROOT", f"{o}:{t}:read", f"{o} ({level}) reads {t}, which only the tenant "
                              f"root reads ({pol[t][0]}): open its SELECT (x-ticvai-rls) or run the operation at tenant")
                if kind == "writes" and write in ("tenant", "subject"):
                    guard.add("RF-TENANT-ROOT", f"{o}:{t}:write", f"{o} ({level}) writes {t}, which only the tenant "
                              f"root writes ({pol[t][0]}): give the table a scope or run the operation at tenant")
                if kind == "reads" and read == "scope" and t in has_path and writers.get(t) \
                        and writers[t] <= {"tenant", "platform"}:
                    guard.add("RF-OWNED-ABOVE", f"{o}:{t}", f"{o} ({level}) reads {t}, written only at tenant "
                              f"({', '.join(sorted(writers[t]))}), so its rows sit above the reader: x-ticvai-rls "
                              "read-beneath, or say why the reader sees none")
    guard.note(f"{len(pol)} tenant tables with a policy; {len(lin)} operations")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
