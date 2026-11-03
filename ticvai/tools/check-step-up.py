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

- **SU-RULE: a rule-dependent step-up** (20 October 2026, r8 cause APPROVALS-TENANCY-C46, CHG-R8GEN-004). An
  operation whose second factor is demanded only where the matched approval rule (`requires_mfa`) or the tenant's
  step-up policy asks for it declares `x-ticvai-step-up: rule-dependent` rather than a fixed strength: it is no
  floor (the policy raises it, nothing lowers it), so it is not ordered with `pin` and `mfa`. It still needs its
  reason and a carrier, and its carrier is the session (an MFA factor verified on the caller's session) or the
  body; the reason must say which rule or policy demands it.

- **SU-MFA-REFUSAL: an MFA step-up with no way to say it is missing or stale** (ADAM CR-375, Chinmay, 31 October
  2026; CHG-CR375-001). The step-up action is the operation's `operationId`, a verified step-up counts for 5 minutes
  from `verifiedAt`, and the operation consumes it in its own transaction (identity `verifyMfaChallenge`). Every
  operation that declares `x-ticvai-step-up: mfa` therefore lists both `step-up-token-missing` and
  `step-up-token-expired` on its `403`; on 31 October none of the 20 did, so the refusal had no type.

- **SU-PLATFORM-STEP-UP: a platform caller's step-up read from a tenant session** (r13, CHG-R13ID-001; ADR-0072 point
  4, ADAM CR-175 and CR-375). CR-375 gave every MFA operation the same 403 text, "the caller's session has no
  verified, unconsumed MFA step-up ... by the rule in identity `verifyMfaChallenge`", and three operations whose
  caller is a platform operator (`x-ticvai-permission` `PLATFORM_*`: openPlatformStaffGrant and two
  PLATFORM_CELL_MANAGE operations in subscription.yaml) took it, against their own text and ADR-0072: a platform
  caller's step-up is read from the Control Plane token (`ticvai_step_up` {action, at} within 5 minutes, `amr`
  includes `mfa`), never from a tenant session or an `identity.mfa_challenge` row. Such an operation's 403 names
  `ticvai_step_up` and never `verifyMfaChallenge`.

- **SU-OFFLINE: an offline-capable step-up that does not say what happens offline** (decided 3 November 2026,
  Chinmay, on system review finding F-01: "Offline verifier" (the till keeps a verifier, re-checked at sync); ADR-0013
  amendment of 3 November 2026; CHG-R14V-001). At r13 `voidOrder`, `recordNoSale` and `withdrawFromDepositBox` were
  offline-capable with a PIN only the server could check, and the contracts gave two contradictory answers. Every
  operation with `x-ticvai-step-up` and `x-ticvai-offline-capable: true` now declares `x-ticvai-offline-step-up`:
  `verifier` (the till checks the PIN against its offline verifier and the server re-checks it at sync) or `refused`
  (the act needs a connection, and its `x-ticvai-offline-note` says so). `verifier` is for a `pin` step-up only (an
  MFA or rule-dependent factor is checked by the server), and needs everything the verifier path stands on: a body
  carrier that is a `SupervisorStepUp`, the `identity#verifySupervisorStepUp` read-via, the
  `X-Ticvai-Step-Up-Verdict` header on its success response, its permission named in identity
  `getOfflineStepUpPackage` (a witness step-up, `witnessStepUp`, needs `witness` there), that operation under
  `deviceAuth`, `SupervisorStepUp.offline`, and the `offline` state of the `supervisorPinPrompt` component. The
  declaration on an operation that is not an offline-capable step-up is refused too, so it cannot linger.

**And what it reports without refusing:** a screen calling a step-up operation that declares no way
to present the challenge. That is authoring work on real screens rather than a defect in the
contract, and failing the package for it would only teach people to run the pipeline less.

    python3 tools/check-step-up.py [--verbose] [--self-test]
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
# Not a strength and not ordered with them: the matched rule or the step-up policy decides (SU-RULE, CHG-R8GEN-004).
RULE_DEPENDENT = "rule-dependent"

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
        if op.get("x-ticvai-step-up") not in ("mfa", RULE_DEPENDENT):
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


MFA_REFUSALS = ("step-up-token-missing", "step-up-token-expired")


def mfa_refusal_problems(oid: str, op: dict) -> list:
    """SU-MFA-REFUSAL: an `x-ticvai-step-up: mfa` operation's 403 names both step-up refusals (ADAM CR-375)."""
    if op.get("x-ticvai-step-up") != "mfa":
        return []
    r403 = (op.get("responses") or {}).get("403") or {}
    types = set(r403.get("x-ticvai-problem-types") or [])
    missing = [t for t in MFA_REFUSALS if t not in types]
    if not missing:
        return []
    return [f"{oid}: SU-MFA-REFUSAL demands an MFA step-up and its 403 does not list {', '.join(missing)} -- the "
            "refusal for an absent or stale step-up has no type (ADAM CR-375, CHG-CR375-001)"]


def platform_step_up_problems(oid: str, op: dict) -> list:
    """SU-PLATFORM-STEP-UP: a platform caller's MFA 403 reads the token's ticvai_step_up (ADR-0072 point 4)."""
    if op.get("x-ticvai-step-up") != "mfa" or not str(op.get("x-ticvai-permission") or "").startswith("PLATFORM_"):
        return []
    text = str(((op.get("responses") or {}).get("403") or {}).get("description") or "")
    if "ticvai_step_up" in text and "verifyMfaChallenge" not in text:
        return []
    return [f"{oid}: SU-PLATFORM-STEP-UP a platform caller's step-up is read from the Control Plane token "
            "(ticvai_step_up, amr), never from a tenant session or verifyMfaChallenge; its 403 must say so "
            "(ADR-0072 point 4; CHG-R13ID-001)"]


OFFLINE_STEP_UP = ("verifier", "refused")
VERDICT_HEADER = "X-Ticvai-Step-Up-Verdict"
PACKAGE_OP = "getOfflineStepUpPackage"


def _offline_capable(op: dict) -> bool:
    return op.get("x-ticvai-offline-capable") in (True, "true")


def _carrier_schema(op: dict, doc: dict) -> dict:
    """The request-body property the step-up travels in (`body:<prop>`), as written (not resolved)."""
    kind, _, prop = str(op.get("x-ticvai-step-up-carrier") or "").partition(":")
    if kind != "body":
        return {}
    schema = (((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}).get("schema") or {}
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
        schema = ((doc.get("components") or {}).get("schemas") or {}).get(ref.rsplit("/", 1)[1]) or {}
    return (schema.get("properties") or {}).get(prop) or {}


def _is_supervisor_step_up(node: dict) -> bool:
    refs = [node.get("$ref")] + [p.get("$ref") for p in node.get("allOf") or [] if isinstance(p, dict)]
    return any(str(r or "").endswith("/SupervisorStepUp") for r in refs)


def offline_problems(oid: str, op: dict, doc: dict, ctx: dict) -> list:
    """SU-OFFLINE: an offline-capable step-up declares its offline behaviour, and `verifier` has what it stands on
    (CHG-R14V-001). `ctx`: {"package": the getOfflineStepUpPackage operation or None, "offline_prop": bool,
    "prompt_offline": bool}."""
    decl = op.get("x-ticvai-offline-step-up")
    stepped = bool(op.get("x-ticvai-step-up"))
    if not (stepped and _offline_capable(op)):
        if decl is not None:
            return [f"{oid}: SU-OFFLINE declares x-ticvai-offline-step-up but is not an offline-capable step-up "
                    "operation -- the declaration says nothing true (CHG-R14V-001)"]
        return []
    if decl not in OFFLINE_STEP_UP:
        return [f"{oid}: SU-OFFLINE is offline-capable and demands a step-up, and does not say what happens offline "
                f"(x-ticvai-offline-step-up: verifier or refused; got {decl!r}) -- a till cannot be built safely "
                "on a PIN nothing can check (system review F-01, CHG-R14V-001)"]
    if decl == "refused":
        if not str(op.get("x-ticvai-offline-note") or "").strip():
            return [f"{oid}: SU-OFFLINE refuses its step-up offline and its x-ticvai-offline-note does not say so"]
        return []
    out = []
    if op.get("x-ticvai-step-up") != "pin":
        out.append(f"{oid}: SU-OFFLINE an offline verifier checks a PIN; a {op.get('x-ticvai-step-up')} step-up is "
                   "checked by the server, so it can only be `refused` offline")
    carrier = _carrier_schema(op, doc)
    if not _is_supervisor_step_up(carrier):
        out.append(f"{oid}: SU-OFFLINE `verifier` needs a body carrier that is a SupervisorStepUp (the offline "
                   "evidence travels in it)")
    vias = {str(v.get("query")) for v in op.get("x-ticvai-read-via") or [] if isinstance(v, dict)}
    if "identity#verifySupervisorStepUp" not in vias:
        out.append(f"{oid}: SU-OFFLINE `verifier` is re-checked at sync by identity#verifySupervisorStepUp, which its "
                   "x-ticvai-read-via does not name")
    ok = [r for c, r in (op.get("responses") or {}).items() if str(c).startswith("2") and isinstance(r, dict)]
    if not ok or not all(VERDICT_HEADER in (r.get("headers") or {}) for r in ok):
        out.append(f"{oid}: SU-OFFLINE `verifier` must answer its success with {VERDICT_HEADER} (common.yaml "
                   "StepUpVerdict), how the till learns a step-up was refused at sync")
    pkg = ctx.get("package")
    if not pkg:
        out.append(f"{oid}: SU-OFFLINE `verifier` and identity has no {PACKAGE_OP} to give the till its verifiers")
    else:
        text = " ".join(str(pkg.get("description") or "").split())
        prop = str(op.get("x-ticvai-step-up-carrier") or "").partition(":")[2]
        need = "witness" if prop == "witnessStepUp" else str(op.get("x-ticvai-permission") or "")
        if need and f"`{need}`" not in text:
            out.append(f"{oid}: SU-OFFLINE `verifier` and {PACKAGE_OP}'s description does not name `{need}`, so its "
                       "signers are not in the till's package")
        if (pkg.get("security") or []) != [{"deviceAuth": []}]:
            out.append(f"{oid}: SU-OFFLINE {PACKAGE_OP} must be under deviceAuth alone: verifiers go to a registered "
                       "device, never to a person's session")
    if not ctx.get("offline_prop"):
        out.append(f"{oid}: SU-OFFLINE `verifier` and common.yaml SupervisorStepUp has no `offline` evidence")
    if not ctx.get("prompt_offline"):
        out.append(f"{oid}: SU-OFFLINE `verifier` and screens/_components.yaml supervisorPinPrompt has no `offline` "
                   "state")
    return out


def _offline_context() -> dict:
    """What SU-OFFLINE's `verifier` stands on, read from the package (CHG-R14V-001)."""
    ctx = {"package": None, "offline_prop": False, "prompt_offline": False}
    try:
        ident = yaml.safe_load((ROOT / "contracts" / "spine" / "identity.yaml").read_text(encoding="utf-8")) or {}
        for item in (ident.get("paths") or {}).values():
            for op in (item or {}).values() if isinstance(item, dict) else []:
                if isinstance(op, dict) and op.get("operationId") == PACKAGE_OP:
                    ctx["package"] = op
        common = yaml.safe_load((ROOT / "contracts" / "shared" / "common.yaml").read_text(encoding="utf-8")) or {}
        sus = ((common.get("components") or {}).get("schemas") or {}).get("SupervisorStepUp") or {}
        ctx["offline_prop"] = "offline" in (sus.get("properties") or {})
        comps = yaml.safe_load((ROOT / "screens" / "_components.yaml").read_text(encoding="utf-8")) or {}
        for c in comps.get("components") or []:
            if isinstance(c, dict) and c.get("kind") == "supervisorPinPrompt":
                ctx["prompt_offline"] = "offline" in (c.get("states") or [])
    except (OSError, yaml.YAMLError):
        pass
    return ctx


def _self_test_offline() -> bool:
    good_pkg = {"security": [{"deviceAuth": []}], "description": "today `ORDER_VOID` (`voidOrder`) and `witness`"}
    ctx = {"package": good_pkg, "offline_prop": True, "prompt_offline": True}
    body = {"content": {"application/json": {"schema": {"properties": {"supervisorStepUp": {
        "allOf": [{"$ref": "../shared/common.yaml#/components/schemas/SupervisorStepUp"}]}}}}}}
    good = {"x-ticvai-step-up": "pin", "x-ticvai-offline-capable": True, "x-ticvai-permission": "ORDER_VOID",
            "x-ticvai-step-up-carrier": "body:supervisorStepUp", "x-ticvai-offline-step-up": "verifier",
            "requestBody": body,
            "x-ticvai-read-via": [{"query": "identity#verifySupervisorStepUp"}],
            "responses": {"200": {"headers": {VERDICT_HEADER: {"$ref": "x"}}}, "403": {}}}
    d = {}
    cases = [
        (good, ctx, 0),
        (dict(good, **{"x-ticvai-offline-step-up": None}), ctx, 1),          # r13's three operations
        (dict(good, **{"x-ticvai-offline-step-up": "maybe"}), ctx, 1),
        (dict(good, responses={"200": {}}), ctx, 1),                         # no verdict header
        (dict(good, **{"x-ticvai-read-via": []}), ctx, 1),                   # nothing re-checks at sync
        (dict(good, **{"x-ticvai-step-up": "mfa"}), ctx, 1),                 # an MFA factor cannot be checked offline
        (dict(good, **{"x-ticvai-permission": "CASH_NO_SALE"}), ctx, 1),     # not in the package
        (good, dict(ctx, package=None), 1),
        (good, dict(ctx, package=dict(good_pkg, security=[{"bearerAuth": []}])), 1),
        (good, dict(ctx, prompt_offline=False), 1),
        (good, dict(ctx, offline_prop=False), 1),
        (dict(good, **{"x-ticvai-offline-step-up": "refused"}), ctx, 1),     # refused with no note
        (dict(good, **{"x-ticvai-offline-step-up": "refused", "x-ticvai-offline-note": "needs a connection"}), ctx, 0),
        (dict(good, **{"x-ticvai-offline-capable": False}), ctx, 1),         # a stale declaration
        (dict(good, **{"x-ticvai-offline-capable": False, "x-ticvai-offline-step-up": None}), ctx, 0),
    ]
    for i, (op, c, want) in enumerate(cases):
        got = len(offline_problems(f"case{i}", op, d, c))
        if got != want:
            print(f"self-test FAIL (SU-OFFLINE case {i}: {got} problem(s), wanted {want})")
            return False
    return True


def _self_test() -> int:
    if not _self_test_offline():
        return 1
    plat = {"x-ticvai-step-up": "mfa", "x-ticvai-permission": "PLATFORM_CELL_MANAGE"}
    ok_plat = (platform_step_up_problems("p1", dict(plat, responses={"403": {
                   "description": "the caller's session ... by the rule in identity `verifyMfaChallenge`"}}))
               and not platform_step_up_problems("p2", dict(plat, responses={"403": {
                   "description": "read from the token's `ticvai_step_up`"}}))
               and not platform_step_up_problems("p3", {"x-ticvai-step-up": "mfa", "x-ticvai-permission": "APPROVAL_DECIDE",
                                                        "responses": {"403": {"description": "verifyMfaChallenge"}}}))
    if not ok_plat:
        print("self-test FAIL (SU-PLATFORM-STEP-UP)")
        return 1
    ok = (not mfa_refusal_problems("a", {"x-ticvai-step-up": "pin"})
          and mfa_refusal_problems("b", {"x-ticvai-step-up": "mfa", "responses": {"403": {"$ref": "x"}}})
          and len(mfa_refusal_problems("c", {"x-ticvai-step-up": "mfa", "responses": {"403": {
              "x-ticvai-problem-types": ["forbidden", "step-up-token-missing"]}}})) == 1
          and not mfa_refusal_problems("d", {"x-ticvai-step-up": "mfa", "responses": {"403": {
              "x-ticvai-problem-types": ["forbidden", "step-up-token-missing", "step-up-token-expired"]}}}))
    print("self-test " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    _utf8()
    verbose = "--verbose" in sys.argv
    if "--self-test" in sys.argv:
        return _self_test()

    guarded: dict = {}          # operationId -> (strength, reason, scopeLevel, file)
    policy_ops: dict = {}       # operationId -> config-scope
    carrier_errors: list = []   # SU-CARRIER (CHG-RUL-014)
    offline_ctx = _offline_context()
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
                carrier_errors += offline_problems(oid, op, doc, offline_ctx)
                if op.get("x-ticvai-step-up"):
                    guarded[oid] = (op["x-ticvai-step-up"],
                                    op.get("x-ticvai-step-up-reason"),
                                    op.get("x-ticvai-scope-level"), f.name)
                    carrier_errors += carrier_problems(oid, op, doc, item.get("parameters") or [])
                    carrier_errors += mfa_refusal_problems(oid, op)
                    carrier_errors += platform_step_up_problems(oid, op)
                if oid in ("listStepUpPolicies", "setStepUpPolicy"):
                    policy_ops[oid] = op.get("x-ticvai-config-scope")

    errors, warnings = [], []
    errors += carrier_errors

    for oid, (strength, reason, level, fname) in sorted(guarded.items()):
        if strength == RULE_DEPENDENT:
            if reason and not any(w in str(reason).lower() for w in ("rule", "policy")):
                errors.append(f"{oid}: SU-RULE a rule-dependent step-up whose reason names no rule or policy that "
                              "demands it (CHG-R8GEN-004)")
        elif strength not in STRENGTH:
            errors.append(f"{oid}: step-up {strength!r} is not one of {', '.join(STRENGTH)} or {RULE_DEPENDENT}")
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
