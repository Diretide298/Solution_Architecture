#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every app has a sign-in door, and every door is a sign-in, not a list.

**On 2 October 2026 no browser could sign in** (CHG-DOOR-001..006; Chinmay: "fix the Block A blockers
now"). `LoginRequest.workstationId` was required on every login, so the TICVAI Console (ADM-001), the
Venue Management door (SUP-001) and the partner portal (PTR-001) could not be used from a desk; the SSO
operations existed and no door declared them; five staff and partner doors had been generated as lists
of sessions, MFA methods and SSO providers with Force logout on the sign-in screen, one with partner
credit operations and one simulating permissions; the guest doors asked a guest to type an idToken,
a UAE Pass code and a refresh token; and the till home read its shift under SHIFT_OPEN, so a supervisor
covering the till could not load it. `check-session-entry` asked only whether an app had *some* screen
that opens a session. This asks whether that screen is a door somebody can walk through.

  D-APP-NO-DOOR        an app (platform.targetApp.app) with screens and no screen that opens a session
  D-LOGIN-WORKSTATION  LoginRequest requires workstationId, so no browser can sign in
  D-DOOR-PATTERN       a staff or partner door that is not a form
  D-DOOR-FOREIGN-OP    a staff or partner door declares an operation that is not part of signing in
  D-DOOR-MFA           a staff or partner door cannot ask for the second factor (audit R135, R126)
  D-DOOR-ROLE          a staff or partner door has no role prompt, on it or one step on (ADR-0003)
  D-DOOR-SSO           a browser staff or partner door does not offer the tenant's SSO
  D-DOOR-WORKSTATION   a browser door asks for a workstationId
  D-RAW-TOKEN          a form collects an idToken, refresh token or redirect URI as if a person typed it
  D-LANDING-READ       a screen a door lands on loads a read gated by an action permission
  D-DEVICE-DOOR        an operation that takes a workstation with no staff session (it names `workstationId` and
                       its security admits a call with no credential or a device's) and acts on it (opens a
                       session, carries a step-up or a permission), or that declares `x-ticvai-step-up-when:
                       sessionless`, and does not authenticate the device: it lists no `deviceAuth`, does not say
                       `x-ticvai-workstation-from: device`, or admits a session-less step-up by `{}`
  D-DEVICE-KINDS       an operation a device credential reaches (`deviceAuth`, or `apiKeyAuth` with audience
                       `device`) that does not list the device kinds it accepts (`x-ticvai-device-kinds`: DeviceKind
                       values, or `all` alone), or lists one that is not a DeviceKind
  D-DEVICE-MONEY       a device-audience operation that writes stored value (orders.stored_value_*, wallet.*,
                       ledger.*, payments.*, games.play, games.credit_ledger) and admits a device key (`apiKeyAuth`)
                       instead of authenticating the device (`deviceAuth`)

**The device rules, 3 November 2026** (r14 review C-04, CHG-R14H-001; the lead: "All four, one release"). `login`
said the device bounds a PIN, but the device was a `workstationId` the caller typed, and the till's session-less
supervisor step-up (`listActiveSessions`, `forceLogout`) admitted `{}`: a PIN oracle and a lockout switch open to the
internet. `captureStoredValue` took money from any device key, a signage display's included. `deviceAuth` existed
(CHG-R8SPN-030) and two operations used it.

A door is a screen calling an operation that opens a session: `login`, `verifyGuestOtp`,
`guestSocialLogin`, `guestUaePassLogin` (the same set as check-session-entry and the Block A closure in
build-service-docs). A staff or partner door is one calling `login`; a browser door is one on a
`reactWeb` platform. Read-only; baseline-aware through tools/audit_guard.py (there is no baseline:
every finding fails).

    python3 tools/check-doors.py [--all] [--update-baseline] [--self-test]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "D-APP-NO-DOOR": "an app with screens and no screen that opens a session",
    "D-LOGIN-WORKSTATION": "LoginRequest requires workstationId, so no browser can sign in (CHG-DOOR-001)",
    "D-DOOR-PATTERN": "a staff or partner door that is not a form (CHG-DOOR-003)",
    "D-DOOR-FOREIGN-OP": "a staff or partner door declares an operation that is not part of signing in (CHG-DOOR-003)",
    "D-DOOR-MFA": "a staff or partner door cannot ask for the second factor (R135 R126)",
    "D-DOOR-ROLE": "a staff or partner door has no role prompt on it or one step on (ADR-0003)",
    "D-DOOR-SSO": "a browser staff or partner door does not offer SSO (CHG-DOOR-002)",
    "D-DOOR-WORKSTATION": "a browser door asks for a workstationId (CHG-DOOR-001)",
    "D-RAW-TOKEN": "a form collects an idToken, refresh token or redirect URI (CHG-DOOR-006)",
    "D-LANDING-READ": "a door's landing loads a read gated by an action permission (CHG-DOOR-005)",
    "D-DEVICE-DOOR": "an operation takes a workstation with no staff session and does not authenticate the device "
                     "(deviceAuth, x-ticvai-workstation-from: device; r14 review C-04, CHG-R14H-001)",
    "D-DEVICE-KINDS": "an operation a device credential reaches lists no x-ticvai-device-kinds, or a kind that is not "
                      "a DeviceKind (r14 review C-04, CHG-R14H-001)",
    "D-DEVICE-MONEY": "a device writes stored value under a device key instead of deviceAuth (r14 review C-04, "
                      "CHG-R14H-001)",
}

OPENS_SESSION = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}
# Staff sign-ins that may come from a device door (they take a workstationId) (CHG-R14H-001).
STAFF_SIGN_IN = {"login", "completeSsoAuthorization"}
# Tables that hold stored value: a device writing one is moving money (CHG-R14H-001).
STORED_VALUE = re.compile(r"^(wallet|ledger|payments)\.|^orders\.stored_value_|^games\.(play|credit_ledger)$")

# **What signing in is.** Credentials, the organisation's SSO, the second factor and its first enrolment,
# the role prompt, replacing a temporary credential, reading the session just opened, signing out.
SIGN_IN = {"login", "listSsoProviders", "startSsoAuthorization", "completeSsoAuthorization",
           "createMfaChallenge", "verifyMfaChallenge", "enrolMfaMethod", "verifyMfaEnrolment",
           "selectRole", "changeOwnCredential", "getCurrentSession", "refreshToken", "logout"}
# **A shared till may be taken over in place** (audit R184, POS-000): a supervisor sees who holds the
# device and ends that session there. Only on a device door; a browser has nothing to take over.
DEVICE_TAKEOVER = {"listActiveSessions", "forceLogout"}
SSO = {"listSsoProviders", "startSsoAuthorization", "completeSsoAuthorization"}
MFA = {"createMfaChallenge", "verifyMfaChallenge"}

# Fields no person types: they come from a provider SDK, a redirect, or the client's token store.
RAW = ("idToken", "refreshToken", "redirectUri")
RAW_BODY = re.compile(r"Collects what `\w+` sends.*?`(%s)`" % "|".join(RAW), re.S)

# Permissions that authorise an act. A read gated by one refuses everybody who may only look.
ACTION_PERMISSION = re.compile(r"_(OPEN|CLOSE|CLOSE_OTHER|SUSPEND|REOPEN|LIFT|ADD|NO_SALE|POST|VOID|REFUND|"
                               r"OVERRIDE|APPROVE\w*|CREATE|MODIFY\w*)$")
# **Reads that are the screen's own act.** Begin Shift opens the shift, so reading the current one under
# the right to open it is that screen's business, not a covering supervisor's.
LANDING_EXEMPT = {
    ("POS-001", "getCurrentShift"): "Begin Shift is where the shift is opened; SHIFT_OPEN is its own act",
    ("POS-001", "listDenominations"): "the opening float is counted by denomination on Begin Shift, its own act",
}


def _schemes(sec) -> set:
    return {k for x in (sec or []) if isinstance(x, dict) for k in x}


def _admits_nobody(sec) -> bool:
    """The security admits a call that carries no credential: `[]`, or a `{}` alternative."""
    return sec == [] or any(isinstance(x, dict) and not x for x in (sec or []))


def _names(node, schemas_of, depth=0) -> set:
    """Property names of a request body schema, through local and cross-contract refs and allOf."""
    if not isinstance(node, dict) or depth > 6:
        return set()
    ref = node.get("$ref")
    if isinstance(ref, str):
        node = schemas_of(ref) or {}
    out = set((node.get("properties") or {}).keys()) if isinstance(node, dict) else set()
    for part in (node.get("allOf") or []) if isinstance(node, dict) else []:
        out |= _names(part, schemas_of, depth + 1)
    return out


def device_door_problems(oid: str, op: dict, sec, names: set, kinds_enum: set, audience: set,
                         writes: list) -> list:
    """(rule, key, message) for one operation's device rules (CHG-R14H-001)."""
    out = []
    schemes = _schemes(sec)
    sessionless = _admits_nobody(sec) or "deviceAuth" in schemes
    acts = oid in STAFF_SIGN_IN or bool(op.get("x-ticvai-step-up")) or op.get("x-ticvai-permission") is not None
    when = op.get("x-ticvai-step-up-when")
    if (sessionless and "workstationId" in names and acts) or when == "sessionless":
        why = []
        if "deviceAuth" not in schemes:
            why.append("lists no deviceAuth")
        if op.get("x-ticvai-workstation-from") != "device" and "workstationId" in names:
            why.append("does not say x-ticvai-workstation-from: device")
        if when == "sessionless" and _admits_nobody(sec):
            why.append("admits its session-less step-up by {} (no credential at all)")
        if why:
            out.append(("D-DEVICE-DOOR", oid, f"{oid}: takes a workstation with no staff session and "
                        + ", ".join(why) + ": the device must be authenticated, not named (C-04)"))
    if op.get("x-ticvai-workstation-from") is not None and op.get("x-ticvai-workstation-from") != "device":
        out.append(("D-DEVICE-DOOR", f"{oid}:from", f"{oid}: x-ticvai-workstation-from "
                    f"{op.get('x-ticvai-workstation-from')!r} is not device"))
    if op.get("x-ticvai-workstation-from") == "device" and "deviceAuth" not in schemes:
        out.append(("D-DEVICE-DOOR", f"{oid}:from", f"{oid}: says x-ticvai-workstation-from: device and lists no "
                    "deviceAuth"))
    reached = "deviceAuth" in schemes or ("apiKeyAuth" in schemes and "device" in audience)
    kinds = op.get("x-ticvai-device-kinds")
    if reached:
        if not isinstance(kinds, list) or not kinds:
            out.append(("D-DEVICE-KINDS", oid, f"{oid}: a device credential reaches it "
                        f"({', '.join(sorted(schemes & {'deviceAuth', 'apiKeyAuth'}))}) and it lists no "
                        "x-ticvai-device-kinds: any device kind could call it"))
        else:
            bad = [k for k in kinds if str(k) not in kinds_enum and k != "all"]
            if bad or ("all" in kinds and len(kinds) > 1):
                out.append(("D-DEVICE-KINDS", f"{oid}:kinds", f"{oid}: x-ticvai-device-kinds {kinds}: "
                            + (f"{bad} are not DeviceKind values" if bad else "`all` stands alone")))
    elif kinds is not None:
        out.append(("D-DEVICE-KINDS", f"{oid}:kinds", f"{oid}: lists x-ticvai-device-kinds and no device credential "
                    "reaches it"))
    if "device" in audience and "apiKeyAuth" in schemes and any(STORED_VALUE.search(str(w)) for w in writes):
        out.append(("D-DEVICE-MONEY", oid, f"{oid}: a device writes stored value here "
                    f"({', '.join(sorted(str(w) for w in writes if STORED_VALUE.search(str(w))))}) under a device key "
                    "(apiKeyAuth): it authenticates the device (deviceAuth)"))
    return out


def _self_test() -> int:
    kinds = {"cardReader", "signageDisplay", "workstationTerminal"}
    bad = 0
    cases = [
        # the r13 forceLogout: a session-less step-up admitted by {}
        ("forceLogout", {"x-ticvai-step-up": "pin", "x-ticvai-step-up-when": "sessionless",
                         "x-ticvai-permission": "SESSION_FORCE_LOGOUT"},
         [{"bearerAuth": []}, {}], {"workstationId"}, {"staff"}, [], {"D-DEVICE-DOOR"}),
        # the r13 login: a workstation named in the body, no device credential
        ("login", {"x-ticvai-permission": None}, [], {"workstationId", "method"}, {"anonymous"}, [],
         {"D-DEVICE-DOOR"}),
        # fixed
        ("login", {"x-ticvai-permission": None, "x-ticvai-workstation-from": "device",
                   "x-ticvai-device-kinds": ["workstationTerminal"]},
         [{}, {"deviceAuth": []}], {"workstationId"}, {"anonymous"}, [], set()),
        # a kind list missing, a bad kind
        ("getSignage", {}, [{"apiKeyAuth": []}], set(), {"device"}, [], {"D-DEVICE-KINDS"}),
        ("getSignage", {"x-ticvai-device-kinds": ["toaster"]}, [{"apiKeyAuth": []}], set(), {"device"}, [],
         {"D-DEVICE-KINDS"}),
        # stored value under a device key
        ("captureStoredValue", {"x-ticvai-device-kinds": ["cardReader"]}, [{"apiKeyAuth": []}], set(),
         {"device", "staff"}, ["orders.stored_value_authorisation"], {"D-DEVICE-MONEY"}),
        ("captureStoredValue", {"x-ticvai-device-kinds": ["cardReader"]}, [{"deviceAuth": []}], set(),
         {"device", "staff"}, ["orders.stored_value_authorisation"], set()),
        # a published read naming a kiosk is not a door
        ("getPublishedKioskConfig", {"x-ticvai-permission": None}, [{}], {"workstationId"}, {"anonymous"}, [], set()),
    ]
    for oid, op, sec, names, aud, writes, want in cases:
        got = {r for r, _k, _m in device_door_problems(oid, op, sec, names, kinds, aud, writes)}
        if got != want:
            print(f"SELF-TEST FAIL {oid} {op} {sec}: got {sorted(got)}, want {sorted(want)}")
            bad += 1
    print("check-doors self-test: " + ("PASS" if not bad else f"{bad} FAIL"))
    return 1 if bad else 0


def device_rules(guard) -> None:
    """D-DEVICE-DOOR, D-DEVICE-KINDS and D-DEVICE-MONEY over every operation (CHG-R14H-001)."""
    import json
    by_schema, _ = g.schemas()
    kinds_enum = {str(v) for v in ((by_schema.get(("tenancy", "DeviceKind")) or {}).get("enum") or [])}
    lin_path = g.ROOT / "handoff" / "api-data-lineage.json"
    lineage = json.loads(lin_path.read_text(encoding="utf-8")) if lin_path.exists() else {}
    docs = {stem: doc for stem, _rel, doc in g.contracts()}

    for oid, f in sorted(g.operations().items()):
        op = f["op"]
        stem = f["contract"]
        sec = op["security"] if "security" in op else docs.get(stem, {}).get("security")

        def schemas_of(ref, stem=stem):
            fpart, _, frag = ref.partition("#")
            st = fpart.rsplit("/", 1)[-1].rsplit(".", 1)[0] if fpart else stem
            name = frag.rsplit("/", 1)[-1]
            return by_schema.get((st, name))

        body = ((((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {})
                .get("schema") or {})
        names = _names(body, schemas_of)
        names |= {str(p.get("name")) for p in list(f["item"].get("parameters") or []) + list(op.get("parameters") or [])
                  if isinstance(p, dict) and p.get("name")}
        aud = op.get("x-ticvai-audience") or []
        aud = {aud} if isinstance(aud, str) else {str(a) for a in aud}
        writes = [w if isinstance(w, str) else (w or {}).get("table") for w in (lineage.get(oid) or {}).get("writes") or []]
        for rule, key, msg in device_door_problems(oid, op, sec, names, kinds_enum, aud, writes):
            guard.add(rule, key, msg)


def main() -> int:
    if "--self-test" in sys.argv:
        return _self_test()
    g.force_utf8()
    guard = g.Guard("check-doors", RULES)
    if _self_test():
        return 1
    device_rules(guard)
    ops = g.operations()
    plats = g.platforms()
    by_id, plat_of = {}, {}
    apps = {}
    for stem, s in g.screens():
        by_id[s["id"]] = s
        plat_of[s["id"]] = stem
        app = ((plats.get(stem) or {}).get("targetApp") or {}).get("app")
        if app:
            apps.setdefault(app, []).append(s["id"])

    def apis(s):
        return {a["operationId"] for a in (s.get("apis") or []) if isinstance(a, dict) and a.get("operationId")}

    # --- the contract ------------------------------------------------------------------------------
    by_schema, _ = g.schemas()
    login_req = by_schema.get(("identity", "LoginRequest")) or {}
    if "workstationId" in (login_req.get("required") or []):
        guard.add("D-LOGIN-WORKSTATION", "identity:LoginRequest",
                  "LoginRequest.required names workstationId: a browser door has none to send")

    # --- every app has a door ----------------------------------------------------------------------
    doors = {sid for sid, s in by_id.items() if apis(s) & OPENS_SESSION and str(s.get("wave")) != "4"}
    for app, sids in sorted(apps.items()):
        if not any(x in doors for x in sids):
            guard.add("D-APP-NO-DOOR", app, f"{app}: {len(sids)} screen(s) and no screen opens a session")

    # --- staff and partner doors -------------------------------------------------------------------
    for sid in sorted(doors):
        s = by_id[sid]
        a = apis(s)
        stem = plat_of[sid]
        browser = (plats.get(stem) or {}).get("runtime") == "reactWeb"
        staff = "login" in a
        overlays = [o for o in (s.get("overlays") or []) if isinstance(o, dict)]
        comps = [c for r in ((s.get("layout") or {}).get("regions") or []) for c in (r.get("components") or [])
                 if isinstance(c, dict)]
        # raw provider and token fields, on any door
        for o in overlays:
            discards = {str(x) for x in ((o.get("dismiss") or {}).get("discards") or [])}
            hit = sorted(discards & set(RAW))
            m = RAW_BODY.search(str(o.get("body") or ""))
            if hit or m:
                guard.add("D-RAW-TOKEN", f"{sid}:{o.get('id')}",
                          f"{sid}: overlay {o.get('id')} collects {', '.join(hit) or m.group(1)}, which no person types")
        if not staff:
            continue
        if s.get("pattern") != "form":
            guard.add("D-DOOR-PATTERN", sid, f"{sid}: a door with pattern {s.get('pattern')!r}, not a sign-in form")
        allowed = SIGN_IN | (set() if browser else DEVICE_TAKEOVER)
        for o in sorted(a - allowed):
            guard.add("D-DOOR-FOREIGN-OP", f"{sid}:{o}", f"{sid}: declares {o}, which is not part of signing in")
        if not MFA <= a:
            guard.add("D-DOOR-MFA", sid, f"{sid}: lacks {', '.join(sorted(MFA - a))}; MFA is asked by permission (R135)")
        nxt = {t.get("to") for t in ((s.get("navigation") or {}).get("transitions") or []) if isinstance(t, dict)}
        if "selectRole" not in a and not any("selectRole" in apis(by_id[x]) for x in nxt if x in by_id):
            guard.add("D-DOOR-ROLE", sid, f"{sid}: no selectRole on the door or on a screen it leads to")
        if browser and not SSO <= a:
            guard.add("D-DOOR-SSO", sid, f"{sid}: a browser door without {', '.join(sorted(SSO - a))}")
        if browser:
            asks = [o.get("id") for o in overlays
                    if "workstationId" in {str(x) for x in ((o.get("dismiss") or {}).get("discards") or [])}]
            asks += [c.get("label") for c in comps if re.search(r"workstation id", str(c.get("label") or ""), re.I)]
            for what in asks:
                guard.add("D-DOOR-WORKSTATION", f"{sid}:{what}", f"{sid}: {what} asks a browser for a workstationId")
        # --- where the door lands ------------------------------------------------------------------
        for t in sorted(x for x in nxt if x in by_id and x not in doors):
            for api in by_id[t].get("apis") or []:
                if not isinstance(api, dict) or api.get("trigger") != "onLoad":
                    continue
                f = ops.get(api.get("operationId"))
                if not f or f["method"] != "get":
                    continue
                perm = str(f["op"].get("x-ticvai-permission") or "")
                if perm and ACTION_PERMISSION.search(perm) and (t, api["operationId"]) not in LANDING_EXEMPT:
                    guard.add("D-LANDING-READ", f"{t}:{api['operationId']}",
                              f"{t} (from {sid}): loads {api['operationId']} under {perm}, a right to act, "
                              f"so a person who may only look cannot open it")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
