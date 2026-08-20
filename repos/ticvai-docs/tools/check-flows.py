#!/usr/bin/env python3
"""
Validate user flows against the screens and contracts they claim to use.

Three checks, and the third is the one worth having:

  1. Every screen a flow references exists in a platform file.
  2. Every operation a flow references exists in the contracts.
  3. **A step's operations are declared on the screen it runs from.** A flow saying
     "WEB-006 calls getAvailability" while WEB-006 declares no such call means one of the
     two is wrong — and until they are compared, nobody finds out which.

Also enforces the branch rule: a flow with no unhappy path describes a demo, not a product.

Run: python3 tools/check-flows.py
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FLOWS = ROOT / "flows"
SCREENS = ROOT / "screens"
# The shipped `contracts/` is authoritative. Until 17 August these pointed at a sibling repo
# outside the package, so every validator passed for whoever had that repo checked out and read
# nothing for anyone working from the zip — which is the worst failure a checker can have, because
# it is silent and it looks like success.
CONTRACTS = ROOT / "contracts"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def load_screens() -> tuple[set[str], dict[str, set[str]], set[tuple[str, str]], set[str]]:
    """Screen ids, their declared operations, the navigation graph, and which edges are inferred."""
    ids: set[str] = set()
    apis: dict[str, set[str]] = {}
    edges: set[tuple[str, str]] = set()
    inferred: set[str] = set()
    for f in SCREENS.glob("P*.yaml"):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            sid = s["id"]
            ids.add(sid)
            apis[sid] = {a["operationId"] for a in (s.get("apis") or [])
                         if a.get("operationId") not in (None, "TODO")}
            nav = s.get("navigation") or {}
            if nav.get("inferred"):
                inferred.add(sid)
            for t in nav.get("exitTo", []) or []:
                edges.add((sid, t))
            for t in nav.get("entryFrom", []) or []:
                edges.add((t, sid))
    return ids, apis, edges, inferred


def load_operations() -> set[str]:
    ops: set[str] = set()
    if not CONTRACTS.exists():
        return ops
    for f in CONTRACTS.rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for item in (doc.get("paths") or {}).values():
            if isinstance(item, dict):
                for verb, op in item.items():
                    if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                        if oid := op.get("operationId"):
                            ops.add(oid)
    return ops


SCREEN_WAVE: dict[str, int] = {}


def main() -> int:
    global SCREEN_WAVE
    for f in SCREENS.glob("P*.yaml"):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            SCREEN_WAVE[s["id"]] = s.get("wave")
    files = sorted(FLOWS.glob("F*.yaml"))
    if not files:
        print("no flows found", file=sys.stderr)
        return 1

    screen_ids, screen_apis, edges, inferred = load_screens()
    ops = load_operations()

    print(f"checking {len(files)} flow(s) against {len(screen_ids)} screens "
          f"and {len(ops)} operations\n")

    for f in files:
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        name = f.name
        steps = doc.get("steps", [])
        branches = doc.get("branches", [])

        if not branches:
            ERRORS.append(f"{name}: no branches. A flow with only a happy path describes a demo")

        step_screens = set()
        for st in steps:
            sid = st.get("screen")
            step_screens.add(sid)
            if sid not in screen_ids:
                ERRORS.append(f"{name}: step {st.get('step')} references unknown screen {sid}")
                continue
            for oid in st.get("operations", []) or []:
                if ops and oid not in ops:
                    ERRORS.append(f"{name}: step {st.get('step')} references unknown operation '{oid}'")
                elif oid not in screen_apis.get(sid, set()):
                    ERRORS.append(
                        f"{name}: step {st.get('step')} calls '{oid}' from {sid}, "
                        f"but {sid} does not declare it")

        flow_wave = doc.get("wave")
        for st in steps:
            sid = st.get("screen")
            if not sid or flow_wave is None:
                continue
            sw = SCREEN_WAVE.get(sid)
            if sw is not None and sw > flow_wave:
                # An error, not a warning. CF-101 recorded this as enforced on 17 August while it
                # appended to WARNINGS and the run exited 0 — a claim of enforcement that enforced
                # nothing, which is worse than no rule because the register says it is covered.
                ERRORS.append(f"{name}: step {sid} is wave {sw} and this flow is wave {flow_wave} — "
                                "the journey cannot run until the later screen exists")

        for b in branches:
            # resolvedBy names *who* resolves it — a role, or "Automatic". It was checked against
            # screens and operations, which is the wrong vocabulary: "Duty manager" is the correct
            # answer and produced a warning on every branch that had one.
            if not b.get("resolvedBy"):
                WARNINGS.append(f"{name}: a branch says nothing about who resolves it")
            if b.get("at") and not any(s.get("step") == b["at"] for s in steps):
                ERRORS.append(f"{name}: branch at step {b['at']}, which does not exist")

        # Do the flow and the screens agree on what leads to what?
        #
        # A flow can route A -> B while the screens declare no such edge. Nothing caught
        # that until now, and it is the disagreement most likely to survive review: both
        # documents look right on their own.
        ordered = [st.get("screen") for st in steps if st.get("screen")]
        for a, b in zip(ordered, ordered[1:]):
            if a == b or a not in screen_ids or b not in screen_ids:
                continue
            if (a, b) not in edges:
                if a in inferred or b in inferred:
                    WARNINGS.append(
                        f"{name}: step {a} -> {b} is not in the navigation graph, but one of "
                        "them has inferred navigation. The flow is probably right and the "
                        "inference incomplete")
                else:
                    ERRORS.append(
                        f"{name}: step {a} -> {b} is not declared in either screen's navigation")

        entry = (doc.get("trigger") or {}).get("entryScreen")
        if entry and entry not in screen_ids:
            ERRORS.append(f"{name}: entryScreen {entry} does not exist")

        off = any(True for _ in [1]) and doc.get("offlineBehaviour")
        if not off:
            WARNINGS.append(f"{name}: no offlineBehaviour stated")

        print(f"  {doc['id']}  {doc['name'][:40]:42}{len(steps)} steps, {len(branches)} branches")

    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
