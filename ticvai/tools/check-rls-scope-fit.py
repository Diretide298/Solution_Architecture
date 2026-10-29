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
    RF-INHERITED     an operation below tenant reads a table whose rows are set at a chosen level (it has a
                     `scope_level` column), or a child that follows one through its parent, and the policy shows
                     the reader only its own level and below: a venue cannot read the tenant's or region's
                     approval matrix it inherits (ADAM CR-095, CHG-RSF-001). Fix: x-ticvai-rls read-beneath.
    RF-DEVICE-ABOVE  an operation a device calls below tenant writes a row an operation above its level created,
                     and the row's path does not follow the device's workstation (tools/ddl_forward.py
                     SCOPE_FOLLOWS): a venue-registered device's heartbeat failed the write check (ADAM CR-095).
    RF-PARENT-ACROSS a table checked through a parent chain that reaches another deployable's schema, where the
                     parent helper reads the parent with the caller's own grants (DB-ROLES grants a deployable
                     only its own schemas), or platform.visible_parent_ids is not SECURITY DEFINER or does not answer
                     for the parent: #27686's 21 tables (ADAM CR-108, CHG-RSF-001).

Devices are judged like staff (CHG-RSF-001): a device's operation runs at the scope its device is bound to
(recordDeviceHeartbeat: "the workstation this is scoped to is the one that device is bound to").

Only operations a staff, partner or device principal calls are judged: a guest reads its own rows by subject, and a
worker (audience `service` only) runs under the tenant root or a system scope. Today's findings are baselined in
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
    "RF-INHERITED": "an operation below tenant reads rows set at a chosen level (scope_level), or their children, "
                    "under a policy that hides the levels above it (ADAM CR-095, CHG-RSF-001)",
    "RF-DEVICE-ABOVE": "a device's operation below tenant writes a row created above its level whose path does not "
                       "follow its workstation (ADAM CR-095, CHG-RSF-001)",
    "RF-PARENT-ACROSS": "a parent chain into another deployable's schema checked with the caller's own grants, or "
                        "by a visible_parent_ids that does not answer for the parent (ADAM CR-108, CHG-RSF-001)",
}
BELOW_TENANT = {"region", "brand", "venue", "workstation"}
JUDGED_AUDIENCE = {"staff", "partner", "device"}
LEVEL = {"tenant": 1, "brand": 2, "region": 3, "venue": 4, "outlet": 5, "workstation": 6}
# Kernel tables every role writes at its own path (ADAM CR-002): never "created above" a writer.
KERNEL = {"platform.outbox", "platform.idempotency_record", "platform.audit_record", "platform.scope"}
# The tables ADAM CR-095 named, and the six with the same shape the lead marked read-beneath too (decision D3, 18
# October 2026), whose readers may never be baselined (RF-INHERITED).
STRICT_INHERITED = {"approvals.matrix", "access.policy_scope_assignment", "ai.provider", "catalogue.dynamic_pricing_control",
                    "catalogue.sales_channel", "marketing.service_copilot_config", "payments.provider"}
STRICT_DEVICE = {("recordDeviceHeartbeat", "platform.device")}
PARENT_HELPERS = ("apply_parent_rls", "apply_parent_split_rls", "apply_parent_across_rls",
                  "apply_parent_split_across_rls")
CALL = re.compile(r"^SELECT platform\.(apply_\w+_rls)\('([^']+)'::regclass(.*)\)$", re.S)
FUNC = re.compile(r"^CREATE (?:OR REPLACE )?FUNCTION platform\.(\w+)\s*\(", re.I)


def sql_files(backend: Path) -> list:
    """The tenant database's files in apply order: the baseline, then every forward migration by number."""
    d = backend / "tenant"
    files = sorted(p for p in d.glob("*.sql") if not p.name.startswith("V"))
    files += sorted((p for p in d.glob("V*.sql") if re.match(r"V\d+__", p.name)),
                    key=lambda p: int(re.match(r"V(\d+)", p.name).group(1)))
    return files


def statements(backend: Path):
    """Every statement of the tenant DDL in apply order, normalized, rollback sections left out. A guarded block of
    policy calls (ddl_forward.guard_block, CHG-R9MIG-002) is read as the calls inside it."""
    for f in sql_files(backend):
        text = re.split(r"^-- =+\n-- ROLLBACK\b", f.read_text(encoding="utf-8"), maxsplit=1, flags=re.M)[0]
        for st in fwd.split_statements(text):
            for x in fwd.unguard(st):
                yield fwd.norm(x)


def policies(backend: Path) -> dict:
    """table -> (helper, the rest of the call's arguments), the last call in apply order."""
    out = {}
    for st in statements(backend):
        m = CALL.match(st)
        if m and m.group(1) != "apply_split_rls":
            out[fwd.unq(m.group(2))] = (m.group(1), m.group(3))
    return out


def helper_bodies(backend: Path) -> dict:
    """platform function name -> its last definition in apply order (the policy helpers and visible_parent_ids)."""
    out = {}
    for st in statements(backend):
        m = FUNC.match(st)
        if m:
            out[m.group(1).lower()] = st
    return out


def parent_of(args: str):
    m = re.match(r"\s*,\s*'([^']+)'\s*,\s*'([^']+)'::regclass", args or "")
    return fwd.unq(m.group(2)) if m else None


def parent_chain(t: str, pol: dict) -> list:
    """The parents a parent-policy table is checked through, nearest first."""
    out, cur = [], t
    while cur in pol and pol[cur][0] in PARENT_HELPERS and len(out) < 20:
        p = parent_of(pol[cur][1])
        if not p or p in out:
            break
        out.append(p)
        cur = p
    return out


def classes(pol: dict) -> dict:
    """table -> (who may read, who may write), each one of 'tenant' (the tenant root only), 'scope' (at or beneath
    the row's owner), 'above' (at, beneath or above the owner), 'any' (any grant), 'subject'."""
    memo: dict = {}

    def write_of(arg: str) -> str:
        # **The tenant root OR a grant over a scope is a scope write** (r10 gate 2, 26 October 2026, CHG-R10GFC-004).
        # identity.principal's home-scope-write check (CHG-R8MIG-007, R8 blocker IDENTITY-C37, the lead's option A:
        # a venue manager creates and updates the principals homed in their venue) is
        # `(platform.tenant_root_in_scope() OR EXISTS (... platform.in_scope(hs.path)))`, and reading any mention of
        # the tenant root as "the tenant root only" reported createPrincipal, updatePrincipal and
        # resetPrincipalCredential at a venue as writes the policy refuses, which V0108 lets through.
        # Only an OR widens it: `tenant_root AND in_scope(...)` is still the tenant root only.
        widened = "tenant_root_in_scope" not in arg or \
            re.search(r"tenant_root_in_scope\(\)\s*\)?\s*OR\b", arg, re.I)
        rest = arg.replace("platform.tenant_root_in_scope()", "") if widened else ""
        if "subject_in_scope" in rest:
            return "subject"
        if "in_scope(" in rest:
            return "scope"
        if "tenant_root_in_scope" in arg:
            return "tenant"
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
        elif helper == "apply_append_audit_read_rls":
            # an append-only trail a grant reads at and beneath the row's org unit (CHG-R10TEN-006, ADAM CR-185)
            r = ("scope", "any")
        elif helper == "apply_read_beneath_rls":
            r = ("above", "scope")
        elif helper == "apply_grant_holder_read_rls":
            m = re.search(r"'((?:[^']|'')*)'", args)
            r = ("any", write_of(m.group(1) if m else ""))
        elif helper == "apply_grant_holder_subject_read_rls":
            # a subject-owned table opened to staff grants, still read by its own guest (CHG-MOD-007)
            r = ("any", "subject")
        elif helper == "apply_grant_holder_subject_rls":
            # a guest's row that belongs to no scope, read and written by any staff grant and by its own guest
            # (x-ticvai-rls grant-holder-write, CHG-R11FXC-003)
            r = ("any", "any")
        elif helper in PARENT_HELPERS:
            p = parent_of(args)
            pc = cls(p, depth + 1) if p else None
            if pc:
                r = (pc[0], pc[1])
        memo[t] = r
        return r

    return {t: cls(t) for t in pol}


def inherited_findings(lin: dict, pol: dict, cl: dict, levelled: set) -> list:
    """RF-INHERITED: [(rule, key, message, strict)]. `levelled`: tables with scope_level and scope_path columns."""
    out = []
    for o, e in sorted(lin.items()):
        level = str(e.get("scope"))
        if level not in BELOW_TENANT or not (set(e.get("audience") or []) & JUDGED_AUDIENCE):
            continue
        for t in e.get("reads") or []:
            c = cl.get(t)
            chain = parent_chain(t, pol)
            root = chain[-1] if chain else t
            if not c or c[0] != "scope" or root not in levelled:
                continue
            out.append(("RF-INHERITED", f"{o}:{t}",
                        f"{o} ({level}) reads {t}, whose rows {'follow ' + root + ', ' if root != t else ''}set at a "
                        f"chosen level (scope_level), and its policy ({pol[t][0]}) hides the levels above the reader: "
                        f"x-ticvai-rls read-beneath on {root}", root in STRICT_INHERITED))
    return out


def device_findings(lin: dict, cl: dict, has_path: set, creators: dict, follows: dict) -> list:
    """RF-DEVICE-ABOVE. `creators`: table -> the levels of the operations that create its rows (a 201 response);
    `follows`: ddl_forward.SCOPE_FOLLOWS."""
    out = []
    for o, e in sorted(lin.items()):
        level = str(e.get("scope"))
        if "device" not in (e.get("audience") or []) or level not in BELOW_TENANT:
            continue
        for t in e.get("writes") or []:
            c = cl.get(t)
            if t in KERNEL or t not in has_path or not c or c[1] != "scope":
                continue
            above = sorted(s for s in creators.get(t, set()) if s in LEVEL and LEVEL[s] < LEVEL[level])
            f = follows.get(t)
            if above and not (f and f[2] == level):
                out.append(("RF-DEVICE-ABOVE", f"{o}:{t}",
                            f"{o} ({level}, a device) writes {t}, whose rows are created at {', '.join(above)}, so "
                            f"they sit above it and the write check refuses it: the row's path follows the "
                            f"device's workstation (ddl_forward.SCOPE_FOLLOWS)", (o, t) in STRICT_DEVICE))
    return out


def parent_across_findings(pol: dict, dep_of_schema: dict, bodies: dict) -> list:
    """RF-PARENT-ACROSS. `dep_of_schema`: schema -> deployable; `bodies`: helper_bodies(). Judged hop by hop: a child
    whose parent is in another deployable needs a helper that asks platform.visible_parent_ids, SECURITY DEFINER and
    answering that parent; a hop within one deployable may read its parent with the caller's grants (decision D9).
    A table is found when any hop of its chain fails."""
    out = []
    pv = (bodies.get("visible_parent_ids") or "").replace('"', "")

    def dep(t):
        return dep_of_schema.get(t.split(".", 1)[0])

    def hop(child):
        helper, args = pol[child]
        par = parent_of(args)
        if not par or dep(child) is None or dep(par) is None or dep(child) == dep(par):
            return None
        if "visible_parent_ids" not in (bodies.get(helper) or ""):
            return par, f"{helper} on {child} reads {par} with the caller's own grants"
        if "SECURITY DEFINER" not in pv.upper():
            return par, "platform.visible_parent_ids is not SECURITY DEFINER"
        if f"'{par}'::regclass" not in pv:
            return par, f"platform.visible_parent_ids does not answer for {par}"
        return None

    for t, (helper, _args) in sorted(pol.items()):
        if helper not in PARENT_HELPERS:
            continue
        chain = parent_chain(t, pol)
        nodes = [t] + [p for p in chain if p in pol and pol[p][0] in PARENT_HELPERS]
        bad = [h for h in (hop(c) for c in nodes) if h]
        if bad:
            far, why = bad[0]
            out.append(("RF-PARENT-ACROSS", t,
                        f"{t} ({dep(t)}) is checked through {' -> '.join(chain)}, and {far} is {dep(far)}'s: {why} "
                        f"(DB-ROLES grants a deployable only its own schemas)", True))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-rls-scope-fit", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ref = (g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}
    pol = policies(g.ROOT / "backend")
    cl = classes(pol)
    has_path = {t for t, cols in ref.items() if any(c.get("column") == "scope_path" for c in cols)}
    cols = {t: {c.get("column") for c in cs} for t, cs in ref.items()}
    levelled = {t for t, c in cols.items() if {"scope_level", "scope_path"} <= c}
    ops = g.operations()
    creators: dict = {}
    for o, e in lin.items():
        if any(str(c) == "201" for c in (((ops.get(o) or {}).get("op") or {}).get("responses") or {})):
            for t in e.get("writes") or []:
                creators.setdefault(t, set()).add(str(e.get("scope")))
    services = (g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    dep_of_schema = {sc: v.get("deployable") for v in services.values() for sc in v.get("schemas") or []}
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
    for rule, key, msg, strict in (inherited_findings(lin, pol, cl, levelled)
                                   + device_findings(lin, cl, has_path, creators, fwd.SCOPE_FOLLOWS)
                                   + parent_across_findings(pol, dep_of_schema, helper_bodies(g.ROOT / "backend"))):
        guard.add(rule, key, msg, strict=strict)
    guard.note(f"{len(pol)} tenant tables with a policy; {len(lin)} operations")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
