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

A door is a screen calling an operation that opens a session: `login`, `verifyGuestOtp`,
`guestSocialLogin`, `guestUaePassLogin` (the same set as check-session-entry and the Block A closure in
build-service-docs). A staff or partner door is one calling `login`; a browser door is one on a
`reactWeb` platform. Read-only; baseline-aware through tools/audit_guard.py (there is no baseline:
every finding fails).

    python3 tools/check-doors.py [--all] [--update-baseline]
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
}

OPENS_SESSION = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}

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


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-doors", RULES)
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
