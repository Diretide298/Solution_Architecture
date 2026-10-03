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
- **SU-CARRIER: a step-up with nowhere to travel** (Chinmay, 3 October 2026, Block A business rules;
  CHG-RUL-014). `rejectShiftVariance` demanded a supervisor's PIN and its body had no field for it,
  so the till had no way to send one. Every step-up operation now says where the step-up travels,
  `x-ticvai-step-up-carrier`: `body:<property>` (a `SupervisorStepUp` or a step-up token in the
  request body), `header:<Name>[,<Name>]` (a GET, which has no body) or `session` (an MFA factor
  verified on the caller's own session). The named property or header must exist. An undeclared
  operation whose body has `supervisorStepUp` or `stepUpToken` counts as carrying it there. An
  operation whose `security` admits `{}` (no session) can only carry it in the body or a header,
  and says so with `x-ticvai-step-up-when: sessionless`. Operations found without a carrier on
  3 October that no rule named are listed in `CARRIER_EXEMPT`, each with its reason; a new one
  is not exempt. Since CHG-RUL-019 and CHG-RUL-020 there are none: every PIN step-up travels in the
  body or a header and every MFA step-up on the session (`verifyMfaChallenge` says how), and a
  `session` carrier on a PIN step-up is refused.

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

# **SU-CARRIER exemptions.** None since 3 October 2026 (CHG-RUL-019, CHG-RUL-020): the 23 operations found without a
# carrier on CHG-RUL-014 now declare one (supervisor and witness PINs in the body, MFA step-ups on the session). An
# exemption added here needs its reason beside it; a new operation is never exempt by default.
CARRIER_EXEMPT: dict = {}
INFERRED_BODY = ("supervisorStepUp", "stepUpToken")


def _body_props(op: dict, doc: dict) -> set:
    schema = (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {}

    def walk(node, depth=0):
        if not isinstance(node, dict) or depth > 4:
            return set()
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            node = ((doc.get("components") or {}).get("schemas") or {}).get(ref.rsplit("/", 1)[1]) or {}
        out = set((node.get("properties") or {}).keys())
        for part in node.get("allOf") or []:
            out |= walk(part, depth + 1)
        return out
    return walk(schema)


def carrier_problems(oid: str, op: dict, doc: dict, path_params: list) -> list:
    """SU-CARRIER: where the step-up travels, and that it exists (CHG-RUL-014)."""
    carrier = op.get("x-ticvai-step-up-carrier")
    body = _body_props(op, doc)
    sessionless = {} in (op.get("security") or [])
    if not carrier:
        inferred = [b for b in INFERRED_BODY if b in body]
        if inferred and not sessionless:
            return []
        if oid in CARRIER_EXEMPT:
            return []
        return [f"{oid}: demands a step-up and says nowhere it travels (x-ticvai-step-up-carrier) -- "
                "a till cannot send a PIN the request has no field for (CHG-RUL-014)"]
    out = []
    kind, _, rest = str(carrier).partition(":")
    if kind == "body":
        if rest not in body:
            out.append(f"{oid}: step-up carrier body:{rest} is not a property of its request body")
    elif kind == "header":
        names = {p.get("name") for p in (op.get("parameters") or []) + path_params
                 if isinstance(p, dict) and p.get("in") == "header"}
        for h in [h for h in rest.split(",") if h]:
            if h not in names:
                out.append(f"{oid}: step-up carrier header {h} is not a header parameter of the operation")
    elif kind == "session":
        if op.get("x-ticvai-step-up") != "mfa":
            out.append(f"{oid}: carries a {op.get('x-ticvai-step-up')} step-up on the session -- only an MFA factor "
                       "verified on the caller's session travels there; a PIN travels in the body (CHG-RUL-020)")
        if sessionless:
            out.append(f"{oid}: admits a call with no session ({{}}) and carries its step-up in the session")
    else:
        out.append(f"{oid}: step-up carrier {carrier!r} is not body:<property>, header:<Name> or session")
    when = op.get("x-ticvai-step-up-when", "always")
    if when not in ("always", "sessionless"):
        out.append(f"{oid}: x-ticvai-step-up-when {when!r} is not always or sessionless")
    if sessionless and when != "sessionless":
        out.append(f"{oid}: admits a call with no session and does not say the step-up is what authorises it "
                   "(x-ticvai-step-up-when: sessionless)")
    return out


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
    carrier_errors: list = []   # SU-CARRIER (CHG-RUL-014)
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
                    carrier_errors += carrier_problems(oid, op, doc, item.get("parameters") or [])
                if oid in ("listStepUpPolicies", "setStepUpPolicy"):
                    policy_ops[oid] = op.get("x-ticvai-config-scope")

    errors, warnings = [], []
    errors += carrier_errors

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

    print(f"\n  SU-CARRIER: {len(guarded) - len([o for o in guarded if o in CARRIER_EXEMPT])} carry their "
          f"step-up; {len([o for o in guarded if o in CARRIER_EXEMPT])} exempt with a reason (CHG-RUL-014)")
    for e in errors:
        print(f"\n  ERROR  {e}")
    print(f"\n{'FAIL' if errors else 'PASS'} - {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
