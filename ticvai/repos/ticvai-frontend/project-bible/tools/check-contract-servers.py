#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every contract is served from its host's one server definition, and its info.version is the URL version.

**3 November 2026** (the r13 system review, finding B-12; the lead, "All four, one release"; CHG-R14J-020; ADR-0026,
amended 3 November 2026). Contracts disagreed on host and base path: payments, wallet, rental, resources, venue-map,
accreditation and public-api were served from `https://api.ticvai.com/v1`, a global host that cannot know a tenant's
cell, although their data is in it (ADR-0038); workforce, approvals and ai from `https://api.{region}.ticvai.com/<module>/v1`,
the module's name in the base; the rest from `{cellHost}` or `{controlPlaneHost}` under `/api/v1`. Generated clients got
three base-URL schemes, and `info.version` was 0.1.0 on 17 contracts and 1.0.0 on 18 with no rule. No check read
`servers` or `info.version` at all. This one does:

    SV-HOSTS         info.x-ticvai-hosts is missing or names a host contracts/shared/common.yaml x-ticvai-servers does
                     not define (a device contract names `device`)
    SV-SERVERS       the servers block is not the declared hosts' definitions, in that order (url and variables; a
                     description is free)
    SV-HOST-SERVICE  the declared hosts leave out the host the contract's service implies
                     (handoff/service-decomposition.json: the service that owns the `control` schema is the Control
                     Plane, deployable `ticvai-ai` is the AI runtime, every other service is the cell)
    SV-VERSION       info.version is not `<N>.0.0`, N the `v<N>` its servers' base path ends in
    SV-DEVICE        a device contract (info.x-ticvai-tier device: a localhost API beside a device, not a TICVAI
                     server) declares servers

Read-only. Exit 1 on a finding not in handoff/audit-baseline.json (tools/audit_guard.py).

    python tools/check-contract-servers.py [--all] [--self-test]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SV-HOSTS": "a contract names its hosts in info.x-ticvai-hosts, each defined in common.yaml x-ticvai-servers "
                "(ADR-0026 amended 3 November 2026, B-12, CHG-R14J-020)",
    "SV-SERVERS": "a contract's servers block is its hosts' definitions from common.yaml, in order (B-12)",
    "SV-HOST-SERVICE": "a contract is served from the host its module's data lives on (B-12)",
    "SV-VERSION": "info.version is <N>.0.0, N the URL version of its servers (ADR-0026 amended, B-12)",
    "SV-DEVICE": "a device contract (a localhost API) declares no servers (B-12)",
}
ROOT = g.ROOT
COMMON = ROOT / "contracts" / "shared" / "common.yaml"
DECOMP = ROOT / "handoff" / "service-decomposition.json"
DEVICE = "device"


def implied_hosts(decomp: dict) -> dict:
    """contract stem -> the host its service implies."""
    out = {}
    for svc in (decomp.get("services") or {}).values():
        if "control" in (svc.get("schemas") or []):
            host = "controlPlane"
        elif svc.get("deployable") == "ticvai-ai":
            host = "ai"
        else:
            host = "cell"
        for c in svc.get("contracts") or []:
            out[str(c)] = host
    return out


def norm_server(s: dict) -> tuple:
    if not isinstance(s, dict):
        return (str(s), ())
    variables = s.get("variables") or {}
    return (str(s.get("url")), tuple(sorted((k, json.dumps(v, sort_keys=True)) for k, v in variables.items())))


def findings(contracts: dict, defs: dict, implied: dict) -> list:
    """[(rule, contract, message)]. contracts: stem -> parsed contract (those with paths)."""
    out = []
    for stem, c in sorted(contracts.items()):
        info = c.get("info") or {}
        servers = c.get("servers") or []
        hosts = info.get("x-ticvai-hosts")
        device = info.get("x-ticvai-tier") == DEVICE
        if device:
            if hosts != [DEVICE]:
                out.append(("SV-HOSTS", stem, f"a device contract says x-ticvai-hosts: [{DEVICE}], not {hosts!r}"))
            if servers:
                out.append(("SV-DEVICE", stem, "a device's localhost API declares servers; the device host's local "
                                               "settings name its port, and it is no TICVAI server"))
            continue
        if not isinstance(hosts, list) or not hosts or any(h not in defs for h in hosts):
            out.append(("SV-HOSTS", stem, f"info.x-ticvai-hosts is {hosts!r}; it lists hosts of common.yaml "
                                          f"x-ticvai-servers ({', '.join(sorted(defs))})"))
            continue
        want = [norm_server(defs[h]) for h in hosts]
        got = [norm_server(s) for s in servers]
        if got != want:
            out.append(("SV-SERVERS", stem, f"servers are {[u for u, _ in got]}; the definitions of {hosts} are "
                                            f"{[u for u, _ in want]} (url and variables as common.yaml writes them)"))
        need = implied.get(stem)
        if need and need not in hosts:
            out.append(("SV-HOST-SERVICE", stem, f"served from {hosts}; its service implies {need} (where its "
                                                 "module's data lives)"))
        majors = {m.group(1) for s in servers if isinstance(s, dict)
                  for m in [re.search(r"/v(\d+)/?$", str(s.get("url") or ""))] if m}
        ver = str(info.get("version") or "")
        if len(majors) != 1 or ver != f"{next(iter(majors))}.0.0":
            out.append(("SV-VERSION", stem, f"info.version is {ver!r}; it is <N>.0.0 with N the URL version of its "
                                            f"servers ({sorted(majors) or 'none'})"))
    return out


def self_test() -> int:
    defs = {"cell": {"url": "https://{cellHost}/api/v1", "variables": {"cellHost": {"default": "cell.ticvai.local"}}},
            "controlPlane": {"url": "https://{controlPlaneHost}/api/v1",
                             "variables": {"controlPlaneHost": {"default": "control.ticvai.local"}}}}
    implied = {"orders": "cell", "subscription": "controlPlane"}
    cell = [dict(defs["cell"], description="free text")]

    def c(hosts, servers, version="1.0.0", tier=None):
        info = {"version": version, "x-ticvai-hosts": hosts}
        if tier:
            info["x-ticvai-tier"] = tier
        return {"info": info, "servers": servers, "paths": {"/x": {}}}

    cases = [
        ("the shared definition passes", {"orders": c(["cell"], cell)}, []),
        ("a global host fails", {"orders": c(["cell"], [{"url": "https://api.ticvai.com/v1"}])}, ["SV-SERVERS"]),
        ("a module name in the base fails",
         {"orders": c(["cell"], [{"url": "https://{cellHost}/orders/v1", "variables": defs["cell"]["variables"]}])},
         ["SV-SERVERS"]),
        ("no hosts declared fails", {"orders": c(None, cell)}, ["SV-HOSTS"]),
        ("a cell module served from the control plane fails",
         {"orders": c(["controlPlane"], [defs["controlPlane"]])}, ["SV-HOST-SERVICE"]),
        ("a control-plane contract on the control plane passes",
         {"subscription": c(["controlPlane"], [defs["controlPlane"]])}, []),
        ("version 0.1.0 fails", {"orders": c(["cell"], cell, "0.1.0")}, ["SV-VERSION"]),
        ("a minor version fails", {"orders": c(["cell"], cell, "1.2.0")}, ["SV-VERSION"]),
        ("a device contract with no servers passes", {"printer": c(["device"], [], "3.1.4", DEVICE)}, []),
        ("a device contract with servers fails", {"printer": c(["device"], cell, "1.0.0", DEVICE)}, ["SV-DEVICE"]),
    ]
    fails = []
    for name, contracts, want in cases:
        got = sorted(r for r, _, _ in findings(contracts, defs, implied))
        if got != sorted(want):
            fails.append(f"{name}: got {got}, expected {sorted(want)}")
    for f in fails:
        print("  FAIL", f)
    print(f"check-contract-servers self-test: {len(cases) - len(fails)} of {len(cases)} passed")
    return 1 if fails else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if self_test():
        print("FAIL - the self-test failed; the rule is not trusted on the package")
        return 1
    guard = g.Guard("check-contract-servers", RULES)
    common = yaml.safe_load(COMMON.read_text(encoding="utf-8")) or {}
    defs = common.get("x-ticvai-servers") or {}
    if not defs:
        guard.add("SV-HOSTS", "contracts/shared/common.yaml", "common.yaml defines no x-ticvai-servers")
        return guard.finish()
    decomp = json.loads(DECOMP.read_text(encoding="utf-8")) if DECOMP.exists() else {}
    contracts = {}
    for f in sorted(ROOT.glob("contracts/*/*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if isinstance(d, dict) and d.get("paths"):
            contracts[f.stem] = d
    for rule, stem, msg in findings(contracts, defs, implied_hosts(decomp)):
        guard.add(rule, stem, f"{stem}: {msg}")
    named = ", ".join(f"{k} {v.get('url')}" for k, v in sorted(defs.items()))
    guard.note(f"{len(contracts)} contract(s) with paths against {len(defs)} host definition(s): {named}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
