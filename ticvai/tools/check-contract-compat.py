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
            a new enum value on a request field, a `security` list that only gained alternatives
            (every scheme a client used still admits it; 2 October, GFIX-5)
  refused   an operation removed or moved (method or path), a parameter or field removed, a type
            changed, anything newly required in a request, a response field no longer required,
            an enum value removed, **a value added to a response enum**, and a change to what the
            operation means: its `x-ticvai-permission`, `x-ticvai-conflict-policy`,
            `x-ticvai-read-routing`, `security` (an alternative removed or changed) or `x-ticvai-emits`

**Semantics count, not only shapes** (system-design review SD-050 and 17 September minutes M17-14,
added 30 September). A client built against a frozen contract switches on the enum values it was
given, so a new response enum value lands in its `default` branch; and a permission, a conflict
policy, a read routing, a security scheme or an emitted event that changes under it breaks it with
every field still in place. Baselines frozen before this rule carry no `semantics` block and are
compared on shapes only until re-frozen.

`--changes <contract>` prints the diff against the frozen baseline as `ApiVersion.changes` rows
(public-api: operationId, contract, kind added/changed/removed, breaking, summary), the developer
changelog DEV-001 shows (ADR-0026).

A breaking change goes out as a new major version: bump `info.version`, and the check says the
baseline needs re-freezing instead of failing.

**Every contract against the release `r1`** (plan item 1C, council of 1 October). Once the git tag
`r1` exists, every contract is compared with its own text at r1, whether or not it was frozen with
`--freeze`, and each change is labelled additive or breaking by the rules above. A ticket pins the
release it was pulled at, so a producer and a consumer of one operation can be building against
different tags; **a breaking change is only safe when both move to the same tag**, and that is a
decision somebody has to make and record. So a breaking change fails unless it is listed in
`docs/active/breaking-changes.yaml` (authored) with its id, contract, operation, reason, who
approved it, the tag the producer and consumer tickets move to, and those tickets. A major version
bump does not excuse it here: the consumers built at r1 are still built at r1. An entry that no
longer matches any change is reported, not failed. Without the tag this passes: no baseline.

Run: python3 tools/check-contract-compat.py            (gate; passes when nothing is frozen)
     python3 tools/check-contract-compat.py --baseline HEAD   (testing: any commit-ish in place of r1)
     python3 tools/check-contract-compat.py --freeze orders
     python3 tools/check-contract-compat.py --changes orders   (ApiVersion.changes rows, JSON)
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "contracts" / "frozen"
BREAKING = ROOT / "docs" / "active" / "breaking-changes.yaml"
BREAKING_FIELDS = ("id", "contract", "operation", "reason", "approved-by", "tag", "producer-tickets",
                   "consumer-tickets")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_baseline import baseline_commit, changed_since, describe, ls_tree, show  # noqa: E402

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


SEMANTIC_KEYS = ("x-ticvai-permission", "x-ticvai-conflict-policy", "x-ticvai-read-routing", "security",
                 "x-ticvai-emits")


def security_widened(old: str | None, new: str | None) -> bool:
    """**A security list that only gained alternatives is additive** (2 October, GFIX-5). OpenAPI security is
    a list of alternatives, any one of which admits the caller: a client built against r1 presents one the
    old list accepted, and the new list still accepts it. Adding `guestAuth` or `{}` (credential optional)
    widens who may call; dropping or changing an alternative is still breaking. 84 guest-audience operations
    admitted only a staff bearer token (check-audience-match AM-GUEST-SECURITY); letting guests in must not
    read as a breaking change to the staff clients that keep working."""
    try:
        a = json.loads(old) if old else None
        b = json.loads(new) if new else None
    except (TypeError, ValueError):
        return False
    if not isinstance(a, list) or not isinstance(b, list) or not a:
        return False
    alts = lambda xs: {json.dumps(x, sort_keys=True) for x in xs}
    return alts(a) <= alts(b)


def semantics(op: dict, c: dict) -> dict:
    """What an operation means beyond its fields (SD-050). `security` falls back to the contract's own."""
    out = {}
    for k in SEMANTIC_KEYS:
        v = op.get(k, c.get("security") if k == "security" else None)
        out[k] = json.dumps(v, sort_keys=True) if v is not None else None
    return out


def shape(contract_name: str, root: Path = ROOT) -> dict:
    f = next(root.glob(f"contracts/*/{contract_name}.yaml"), None)
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
                                      "request": req, "response": resp, "semantics": semantics(op, c)}
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
                added_values = set(y["enum"]) - set(x["enum"])
                if not inbound and added_values:
                    # SD-050: breaking. A client switches on the values it was given; a new one falls
                    # into its default branch, which is a behaviour change nobody reviewed.
                    bad.append(f"{o}: response `{k}` gained enum value(s) {sorted(added_values)}")
            if inbound:
                for k, y in fb.items():
                    if k not in fa and y["required"]:
                        bad.append(f"{o}: new required {where} `{k}`")
        sa, sb = a.get("semantics"), b.get("semantics") or {}
        if sa is not None:  # baselines frozen before SD-050 carry none
            for k in SEMANTIC_KEYS:
                if sa.get(k) != sb.get(k):
                    if k == "security" and security_widened(sa.get(k), sb.get(k)):
                        continue
                    bad.append(f"{o}: {k} changed {sa.get(k)} -> {sb.get(k)}")
    return bad


def changes(old: dict, new: dict) -> list[dict]:
    """The diff as `ApiVersion.changes` rows (public-api.yaml; M17-14)."""
    rows = []
    for o in sorted(set(new["operations"]) - set(old["operations"])):
        rows.append({"operationId": o, "contract": new["contract"], "kind": "added", "breaking": False,
                     "summary": "new operation"})
    per_op: dict = {}
    for line in compare(old, new):
        o, _, why = line.partition(": ")
        per_op.setdefault(o, []).append(why)
    for o, whys in sorted(per_op.items()):
        removed = any(w == "operation removed" for w in whys)
        rows.append({"operationId": o, "contract": new["contract"], "kind": "removed" if removed else "changed",
                     "breaking": True, "summary": "; ".join(whys)})
    return rows


def additive(old: dict, new: dict) -> list[str]:
    """The changes `compare` allows, named: what a consumer built at the baseline does not notice."""
    out = [f"{o}: new operation" for o in sorted(set(new["operations"]) - set(old["operations"]))]
    for o, a in sorted(old["operations"].items()):
        b = new["operations"].get(o)
        if b is None:
            continue
        for where, inbound in (("params", True), ("request", True), ("response", False)):
            fa, fb = a[where], b[where]
            for k, y in sorted(fb.items()):
                x = fa.get(k)
                if x is None:
                    if not (inbound and y["required"]):
                        out.append(f"{o}: new {'optional ' if inbound else ''}{where} `{k}`")
                    continue
                if inbound and set(y["enum"]) - set(x["enum"]):
                    out.append(f"{o}: {where} `{k}` accepts new value(s) {sorted(set(y['enum']) - set(x['enum']))}")
                if inbound and x["required"] and not y["required"]:
                    out.append(f"{o}: {where} `{k}` is no longer required")
                if not inbound and y["required"] and not x["required"]:
                    out.append(f"{o}: response `{k}` is now always present")
    return out


def load_breaking() -> tuple[list[dict], list[str]]:
    """The approved breaking changes, and what is wrong with any entry. **An entry missing its approval
    or its tickets approves nothing**: the point of the file is that a person decided and said who
    moves."""
    if not BREAKING.exists():
        return [], []
    doc = yaml.safe_load(BREAKING.read_text(encoding="utf-8")) or {}
    entries, errors = [], []
    for i, e in enumerate(doc.get("changes") or []):
        if not isinstance(e, dict):
            errors.append(f"entry {i + 1} is not a mapping")
            continue
        missing = [f for f in BREAKING_FIELDS if not e.get(f)]
        if missing:
            errors.append(f"{e.get('id') or f'entry {i + 1}'}: missing {', '.join(missing)}; it approves nothing")
            continue
        entries.append(e)
    return entries, errors


def approval(entries: list[dict], contract: str, line: str) -> dict | None:
    """The entry that approves one breaking change: same contract, same operation, and, when the entry
    names a `change`, a change whose description contains it."""
    o, _, why = line.partition(": ")
    for e in entries:
        if str(e["contract"]) == contract and str(e["operation"]) == o and str(e.get("change") or "") in why:
            return e
    return None


def release_shapes(commit: str, names: set) -> dict:
    """Shapes of the named contracts as they were at `commit`. The contracts tree is written to a temporary
    directory, because a contract's `$ref`s are relative paths to its neighbours at the same commit."""
    tmp = Path(tempfile.mkdtemp(prefix="ticvai-contracts-"))
    try:
        for path in ls_tree(commit, "contracts"):
            if path.endswith(".yaml"):
                dest = tmp / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(show(commit, path) or b"")
        return {f.stem: shape(f.stem, tmp) for f in sorted(tmp.glob("contracts/*/*.yaml")) if f.stem in names}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def against_release(ref: str | None) -> int | None:
    """Compare every contract with the release; the number of unapproved breaking changes, or None
    when the release tag does not exist."""
    commit = baseline_commit(ref)
    if not commit:
        return None
    at = describe(ref, commit)
    entries, entry_errors = load_breaking()
    failures = len(entry_errors)
    for e in entry_errors:
        print(f"  FAIL  {BREAKING.relative_to(ROOT).as_posix()}: {e}")
    changed = [p for _, p in changed_since(commit, "contracts") if p.endswith(".yaml")]
    if not changed:
        print(f"  ok    no contract changed since {at}")
        for e in entries:
            print(f"  NOTE  {e['id']} approves {e['contract']} {e['operation']}, which has not changed since {at}")
        return failures
    # **Only what a change can reach is re-read**: the changed contracts, and every contract that refers
    # to one of them. A change to shared/ reaches everything.
    current = {f.stem: f for f in ROOT.glob("contracts/*/*.yaml")}
    names = {Path(p).stem for p in changed}
    if any(p.startswith("contracts/shared/") for p in changed):
        names |= set(current) | {Path(p).stem for p in ls_tree(commit, "contracts") if p.endswith(".yaml")}
    else:
        files = {Path(p).name for p in changed}
        names |= {n for n, f in current.items() if any(x in f.read_text(encoding="utf-8") for x in files)}
    old_shapes = release_shapes(commit, names)
    used = set()
    n_add = n_ok = 0
    for name in sorted(names):
        empty = {"contract": name, "version": "", "operations": {}}
        old = old_shapes.get(name, empty)
        new = shape(name) if name in current else empty
        bad, add = compare(old, new), additive(old, new)
        n_add += len(add)
        if not old["operations"] and not new["operations"]:
            continue
        unapproved = []
        for b in bad:
            e = approval(entries, name, b)
            if e:
                used.add(e["id"])
                print(f"  ok    {name}: {b} -- breaking, approved by {e['approved-by']} ({e['id']}); "
                      f"producer and consumer move to {e['tag']}")
            else:
                unapproved.append(b)
        if unapproved:
            failures += len(unapproved)
            print(f"  FAIL  {name}: {len(unapproved)} breaking change(s) since {at}, not in "
                  f"{BREAKING.relative_to(ROOT).as_posix()}")
            for b in unapproved:
                print(f"        {b}")
        elif add or bad:
            n_ok += 1
            print(f"  ok    {name}: {len(add)} additive change(s) since {at}"
                  + (f", {len(bad)} approved breaking" if bad else ""))
    for e in entries:
        if e["id"] not in used:
            print(f"  NOTE  {e['id']} ({e['contract']} {e['operation']}) matches no breaking change since {at}; "
                  "remove it, or check the operation and change it names")
    print(f"  {len(names)} contract(s) compared with {at}: {n_add} additive change(s), "
          f"{failures - len(entry_errors)} unapproved breaking change(s)"
          + (f", {len(entry_errors)} incomplete approval(s)" if entry_errors else ""))
    return failures

def main() -> int:
    argv = sys.argv[1:]
    ref = None
    if "--baseline" in argv:
        i = argv.index("--baseline")
        ref = argv[i + 1] if i + 1 < len(argv) else None
        del argv[i:i + 2]
        sys.argv = sys.argv[:1] + argv

    if len(sys.argv) >= 3 and sys.argv[1] == "--freeze":
        FROZEN.mkdir(parents=True, exist_ok=True)
        for name in sys.argv[2:]:
            s = shape(name)
            (FROZEN / f"{name}.json").write_text(json.dumps(s, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            print(f"froze {name} at {s['version']}: {len(s['operations'])} operations")
        return 0

    if len(sys.argv) >= 3 and sys.argv[1] == "--changes":
        rows = []
        for name in sys.argv[2:]:
            base = FROZEN / f"{name}.json"
            if not base.exists():
                raise SystemExit(f"{name} is not frozen; there is nothing to diff against")
            rows += changes(json.loads(base.read_text(encoding="utf-8")), shape(name))
        print(json.dumps(rows, indent=1))
        return 0

    release = against_release(ref)          # None: no r1 tag
    baselines = sorted(FROZEN.glob("*.json")) if FROZEN.exists() else []
    if not baselines and release is None:
        print(f"PASS - no baseline: no {ref or 'r1'} tag and no contract frozen yet "
              "(freeze one with --freeze <contract>)")
        return 0
    failures, refreeze = release or 0, []
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
        print(f"FAIL - {failures} breaking change(s) or incomplete approval(s): make a change additive, or list it in "
              f"{BREAKING.relative_to(ROOT).as_posix()} with its approval and the tag producer and consumer move to")
        return 1
    what = [f"{len(baselines)} frozen contract(s) changed additively or not at all"] if baselines else []
    if release is not None:
        what.insert(0, f"every contract compatible with {ref or 'r1'} or its breaking changes approved")
    print("PASS - " + "; ".join(what))
    return 0

if __name__ == "__main__":
    sys.exit(main())
