#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A screen a guest reaches before signing in must load without a session.

**Council of 2 October 2026** (typed properties, `docs/active/council-2-october.md`). The white-label
process agent found that the storefront cannot load the tenant's theme before sign-in: WEB-001 calls
`getTenantConfig` on load, and `getTenantConfig` requires `guestAuth` or `bearerAuth`. Every guest
arrives signed out, so the home page of every tenant renders unbranded or not at all. Guests could not
read a policy for the same reason. "Needs a session" is a declared property (the operation's effective
`security`), and "reachable before sign-in" is a declared property of the screen (`entryState`), so the
pair is checkable on every screen.

**Before sign-in** means a guest-platform screen (P01, P02, P05) that takes no session-issued identity
(`subjectId`, `sessionId`, `principalId`, `operatorId` `from: session`; the same set as
`check-session-entry.py`), or the sign-in screen itself. **A load** is an `apis` entry with trigger
`onLoad`, `onInterval` or `background`: an action may ask the guest to sign in first, a load cannot.

    PS-LOAD-NEEDS-SESSION  a pre-sign-in screen loads an operation that needs a session (not `[]`, no `{}`
                           alternative), and the operation is not the guest's own record
    PS-UNDECLARED-SIGNIN   a pre-sign-in screen loads the guest's own record (a `listMy...`/`getMy...`
                           operation, or one acting on the caller): the screen is behind sign-in and does
                           not say so (add `subjectId from: session`), or the load is conditional and the
                           purpose does not say "when signed in"

An `apis` purpose that says the load runs only when signed in ("signed in", "signed-in") is skipped.

**Report-only until the guest fixes land**; the lead then baselines it and makes it gate.

    python3 tools/check-preauth-session.py [--all] [--update-baseline]
"""
import collections
import re
import sys

import audit_guard as g
import typed_props as tp

RULES = {
    "PS-LOAD-NEEDS-SESSION": "pre-sign-in screen loads an operation that needs a session",
    "PS-UNDECLARED-SIGNIN": "pre-sign-in screen loads the guest's own record without declaring sign-in",
}
SIGNED_IN = re.compile(r"signed[- ]in|when (the guest is )?logged in|after sign-?in", re.I)
OWN = re.compile(r"^(list|get|update|delete|create)My[A-Z]|Mine$")


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-preauth-session", RULES)
    ops = tp.operations()
    per_screen = collections.Counter()
    per_op = collections.Counter()
    n_pre = 0
    for code, aud, s in tp.screens():
        if code not in tp.GUEST_PLATFORMS or not tp.is_preauth(s):
            continue
        n_pre += 1
        sid = s["id"]
        seen = set()
        for op, where, trig, why in tp.bindings(s):
            if where != "apis" or trig not in tp.LOAD_TRIGGERS or op in seen or op not in ops:
                continue
            seen.add(op)
            if op in tp.SESSION_CREATORS:
                continue
            need, schemes = tp.needs_session(op)
            if not need or SIGNED_IN.search(why):
                continue
            own = bool(OWN.search(op)) or tp.acts_on(op).startswith("caller") \
                or ops[op]["op"].get("x-ticvai-self-scoped")
            rule = "PS-UNDECLARED-SIGNIN" if own else "PS-LOAD-NEEDS-SESSION"
            guard.add(rule, f"{sid}:{op}",
                      f"{code} {sid} {s.get('name', '')[:40]}: loads {op} ({trig}), which needs {schemes}")
            per_screen[(code, sid)] += 1
            if rule == "PS-LOAD-NEEDS-SESSION":
                per_op[op] += 1
    guard.note(f"{n_pre} guest screen(s) are reachable before sign-in")
    if per_op:
        guard.note("operations most often loaded before sign-in that need a session: "
                   + ", ".join(f"{o} ({n})" for o, n in per_op.most_common(10)))
    if per_screen:
        guard.note("most findings: " + ", ".join(f"{c} {sid} ({n})" for (c, sid), n in per_screen.most_common(10)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
