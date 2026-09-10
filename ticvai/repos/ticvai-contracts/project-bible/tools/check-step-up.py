#!/usr/bin/env python3
"""Actions that demand a second factor, and whether anything can actually raise one.

**Thirty-one screens call an `approve*` operation and, on 10 September 2026, not one of them could
challenge the approver.** MFA existed only on the ten sign-in screens: it was a thing you did on
the way in, never a thing an action could demand. `ADM-342 Authentication & MFA Policy Manager` had
existed since the workshop packs with **no operations at all**, and its own `gaps` entry said so --
*the name promises authoring and the contract offers none*.

`x-ticvai-step-up` sits on the operation rather than on the screen, because the answer to *does
approving a journal entry need a second factor?* has to be one answer and not thirty-one.

**What this refuses**

- **A step-up with no reason.** An unexplained control is the one somebody removes the first time
  it is inconvenient, and the removal looks like tidying.
- **A strength outside `StepUpStrength`.** The enum is ordered weakest first, which is what makes
  *raise only* a checkable rule rather than an intention.
- **A policy operation whose `x-ticvai-config-scope` sits below the level of an operation it
  governs.** A venue that can configure away a platform-level control is not a control.

**And what it reports without refusing:** a screen calling a step-up operation that declares no way
to present the challenge. That is authoring work on real screens rather than a defect in the
contract, and failing the package for it would only teach people to run the pipeline less.

    python3 tools/check-step-up.py [--verbose]
"""

from __future__ import annotations

import collections
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Ordered weakest first. `pin` is a supervisor PIN captured in place, which `roles.yaml` already
# resolves; `mfa` is a challenge against an enrolled method.
STRENGTH = ["none", "pin", "mfa"]

# What a screen needs to be able to raise a challenge in front of somebody.
CHALLENGE = {"createMfaChallenge", "verifyMfaChallenge"}

# Where a level sits, so "below" is comparable. Widest first.
LEVELS = ["platform", "tenant", "region", "venue", "outlet"]


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    _utf8()
    verbose = "--verbose" in sys.argv

    guarded: dict = {}          # operationId -> (strength, reason, scopeLevel, file)
    policy_ops: dict = {}       # operationId -> config-scope
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for op in item.values():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                oid = op["operationId"]
                if op.get("x-ticvai-step-up"):
                    guarded[oid] = (op["x-ticvai-step-up"],
                                    op.get("x-ticvai-step-up-reason"),
                                    op.get("x-ticvai-scope-level"), f.name)
                if oid in ("listStepUpPolicies", "setStepUpPolicy"):
                    policy_ops[oid] = op.get("x-ticvai-config-scope")

    errors, warnings = [], []

    for oid, (strength, reason, level, fname) in sorted(guarded.items()):
        if strength not in STRENGTH:
            errors.append(f"{oid}: step-up {strength!r} is not one of {', '.join(STRENGTH)}")
        if not reason:
            errors.append(f"{oid} ({fname}): declares step-up and gives no reason -- "
                          "an unexplained control is the one somebody removes")

    # **The policy must not be configurable below what it governs.**
    for pol, cfg in sorted(policy_ops.items()):
        if not cfg:
            errors.append(f"{pol}: declares no x-ticvai-config-scope")
            continue
        if cfg not in LEVELS:
            continue
        for oid, (_s, _r, level, _f) in guarded.items():
            if level in LEVELS and LEVELS.index(cfg) > LEVELS.index(level):
                errors.append(
                    f"{pol}: configurable at {cfg}, which is below {oid} at {level} -- "
                    "a scope that can configure away a control above it is not a control")
                break

    # **Which screens reach a guarded action, and can any of them ask?**
    callers = collections.defaultdict(list)
    unable = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        code = (doc.get("platform") or {}).get("code") or f.name.split("-")[0]
        for sc in (doc.get("screens") or []):
            ops = {a["operationId"] for a in (sc.get("apis") or []) if isinstance(a, dict)}
            hit = sorted(ops & set(guarded))
            if not hit:
                continue
            callers[code].append(sc["id"])
            overlays = str(sc.get("overlays") or "").lower()
            if not (ops & CHALLENGE) and "mfa" not in overlays and "step" not in overlays:
                unable.append((code, sc["id"], sc.get("name"), hit))

    print(f"{len(guarded)} operation(s) demand step-up; "
          f"{sum(len(v) for v in callers.values())} screen(s) reach one\n")
    for oid, (strength, _r, level, fname) in sorted(guarded.items()):
        print(f"  {strength:4} {oid:36} {str(level):8} {fname}")
    if policy_ops:
        print("\n  policy: " + ", ".join(f"{k} (config-scope {v})"
                                         for k, v in sorted(policy_ops.items())))
    else:
        errors.append("nothing reads or writes a step-up policy -- the requirement is a constant, "
                      "not a control somebody owns")

    if unable:
        print(f"\n  {len(unable)} screen(s) call a step-up action and declare no way to raise the "
              "challenge:")
        for code, sid, name, hit in (unable if verbose else unable[:12]):
            print(f"    {code} {sid:9} {str(name)[:30]:32} {', '.join(hit)[:40]}")
        if not verbose and len(unable) > 12:
            print(f"    ... and {len(unable) - 12} more. Run with --verbose.")
        warnings.append(f"{len(unable)} screen(s) reach a step-up action with no challenge "
                        "declared")

    for e in errors:
        print(f"\n  ERROR  {e}")
    print(f"\n{'FAIL' if errors else 'PASS'} - {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
