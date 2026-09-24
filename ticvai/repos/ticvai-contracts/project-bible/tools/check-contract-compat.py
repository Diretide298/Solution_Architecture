#!/usr/bin/env python3
"""Hold a frozen contract to additive change.

**Services are built to a slice, published at 1.0.0, then extended** (decided 23 September). The
extending is only safe if nothing already built can break, and that is a rule a reviewer will miss
on the four-hundredth operation. This checks it.

Freezing is an act, not a version number. `1.0.0` in `info.version` today means the contract was
written carefully, not that anything has been built against it, so this does not freeze every
contract at 1.0.0. A contract is frozen when somebody runs

    python3 tools/check-contract-compat.py --freeze <contract>

which records its operations and field shapes in `contracts/frozen/<contract>.json`. From then on,
while the major version is unchanged:

  allowed   a new operation, a new optional request field or parameter, a new response field,
            a new enum value on a request field
  refused   an operation removed or moved (method or path), a parameter or field removed, a type
            changed, anything newly required in a request, a response field no longer required,
            an enum value removed

A breaking change goes out as a new major version: bump `info.version`, and the check says the
baseline needs re-freezing instead of failing.

Run: python3 tools/check-contract-compat.py            (gate; passes when nothing is frozen)
     python3 tools/check-contract-compat.py --freeze orders
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "contracts" / "frozen"

_spec = importlib.util.spec_from_file_location("sd", ROOT / "tools" / "build-service-docs.py")
sd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sd)


def kind(node, base: Path) -> tuple[str, list]:
    """(type without enum values, enum values). Enum values are compared separately, as sets."""
    n, b, name = sd.resolve(node, base)
    if not isinstance(n, dict):
        return "any", []
    if "enum" in n:
        return f"enum:{name or n.get('type', '')}", sorted(str(v) for v in n["enum"])
    if n.get("type") == "array":
        t, e = kind(n.get("items", {}), b)
        return f"array<{t}>", e
    for k in ("oneOf", "anyOf"):
        if k in n:
            return k + "<" + ",".join(sorted(sd.resolve(a, b)[2] or kind(a, b)[0] for a in n[k])) + ">", []
    t = n.get("type")
    if isinstance(t, list):
        t = "/".join(x for x in t if x != "null")
    return f"{t or 'object'}{':' + n['format'] if n.get('format') else ''}", []


def fields(node, base: Path, prefix="", depth=0, seen=frozenset()) -> dict:
    out = {}
    _, _, name = sd.resolve(node, base)
    if name and name in seen:
        return out
    seen = seen | ({name} if name else set())
    props, req, _ = sd.merged(node, base, seen)
    for k, (v, b) in props.items():
        vr, vb, vname = sd.resolve(v, b)
        if not isinstance(vr, dict):
            continue
        t, e = kind(v, b)
        out[prefix + k] = {"type": t, "required": k in req, "enum": e}
        if depth + 1 >= 4:
            continue
        if vr.get("type") == "array":
            it, _, iname = sd.resolve(vr.get("items", {}), vb)
            if isinstance(it, dict) and (it.get("properties") or it.get("allOf")) and iname not in seen:
                out.update(fields(vr["items"], vb, prefix + k + "[].", depth + 1, seen))
        elif (vr.get("properties") or vr.get("allOf")) and vname not in seen:
            out.update(fields(v, b, prefix + k + ".", depth + 1, seen))
    return out


def shape(contract_name: str) -> dict:
    f = next(ROOT.glob(f"contracts/*/{contract_name}.yaml"), None)
    if f is None:
        raise SystemExit(f"no contract named {contract_name}")
    c = sd.contract(f)
    ops = {}
    for path, item in (c.get("paths") or {}).items():
        shared = item.get("parameters") or []
        for verb, op in item.items():
            if not isinstance(op, dict) or "operationId" not in op:
                continue
            params = {}
            for p in shared + (op.get("parameters") or []):
                pr, pb, _ = sd.resolve(p, f)
                t, e = kind(pr.get("schema", {}), pb)
                params[f"{pr.get('in')}:{pr.get('name')}"] = {"type": t, "required": bool(pr.get("required")), "enum": e}
            req = {}
            rb = op.get("requestBody")
            if rb:
                rbr, rbb, _ = sd.resolve(rb, f)
                sch = ((rbr.get("content") or {}).get("application/json") or {}).get("schema")
                if sch:
                    req = fields(sch, rbb)
            resp = {}
            for code, r in (op.get("responses") or {}).items():
                if str(code).startswith("2"):
                    rr, rbase, _ = sd.resolve(r, f)
                    sch = next((v.get("schema") for v in (rr.get("content") or {}).values() if v.get("schema")), None)
                    if sch:
                        resp = fields(sch, rbase)
                    break
            ops[op["operationId"]] = {"verb": verb.upper(), "path": path, "params": params,
                                      "request": req, "response": resp}
    return {"contract": contract_name, "version": str((c.get("info") or {}).get("version", "")),
            "operations": ops}


def major(v: str) -> int:
    try:
        return int(v.split(".")[0])
    except ValueError:
        return 0


def compare(old: dict, new: dict) -> list[str]:
    bad = []
    for o, a in old["operations"].items():
        b = new["operations"].get(o)
        if b is None:
            bad.append(f"{o}: operation removed")
            continue
        if (a["verb"], a["path"]) != (b["verb"], b["path"]):
            bad.append(f"{o}: moved from {a['verb']} {a['path']} to {b['verb']} {b['path']}")
        for where, inbound in (("params", True), ("request", True), ("response", False)):
            fa, fb = a[where], b[where]
            for k, x in fa.items():
                y = fb.get(k)
                if y is None:
                    bad.append(f"{o}: {where} `{k}` removed")
                    continue
                if x["type"] != y["type"]:
                    bad.append(f"{o}: {where} `{k}` type {x['type']} -> {y['type']}")
                if inbound and y["required"] and not x["required"]:
                    bad.append(f"{o}: {where} `{k}` is now required")
                if not inbound and x["required"] and not y["required"]:
                    bad.append(f"{o}: response `{k}` is no longer guaranteed")
                gone = set(x["enum"]) - set(y["enum"])
                if gone:
                    bad.append(f"{o}: {where} `{k}` lost enum value(s) {sorted(gone)}")
                if not inbound and set(y["enum"]) - set(x["enum"]):
                    pass  # a new response enum value is additive; clients must tolerate unknowns
            if inbound:
                for k, y in fb.items():
                    if k not in fa and y["required"]:
                        bad.append(f"{o}: new required {where} `{k}`")
    return bad


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "--freeze":
        FROZEN.mkdir(parents=True, exist_ok=True)
        for name in sys.argv[2:]:
            s = shape(name)
            (FROZEN / f"{name}.json").write_text(json.dumps(s, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            print(f"froze {name} at {s['version']}: {len(s['operations'])} operations")
        return 0

    baselines = sorted(FROZEN.glob("*.json")) if FROZEN.exists() else []
    if not baselines:
        print("PASS - no contract is frozen yet; freeze one with --freeze <contract>")
        return 0
    failures, refreeze = 0, []
    for f in baselines:
        old = json.loads(f.read_text(encoding="utf-8"))
        new = shape(old["contract"])
        if major(new["version"]) > major(old["version"]):
            refreeze.append(f"{old['contract']} {old['version']} -> {new['version']}")
            continue
        bad = compare(old, new)
        added = len(set(new["operations"]) - set(old["operations"]))
        if bad:
            failures += len(bad)
            print(f"  FAIL  {old['contract']} (frozen at {old['version']}): {len(bad)} breaking change(s)")
            for b in bad:
                print(f"        {b}")
        else:
            print(f"  ok    {old['contract']} (frozen at {old['version']}): additive only, {added} operation(s) added")
    for r in refreeze:
        print(f"  NOTE  {r}: new major version, re-freeze with --freeze")
    if failures:
        print(f"FAIL - {failures} breaking change(s) in frozen contracts. Make it additive, or bump the major version.")
        return 1
    print(f"PASS - {len(baselines)} frozen contract(s) changed additively or not at all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
