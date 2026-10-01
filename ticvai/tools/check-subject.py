#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A staff screen acting for a guest calls the operation that names the guest, never the caller's own.

**Council of 2 October 2026** (typed properties, `docs/active/council/council-report-2026-10-02-opus.html`). A POS v2 follow-up
(commit 0d59727e) found that POS-002, the till, reads `getLoyaltyPosition`: the caller's own loyalty
position, with no parameter naming whose. Called from a till it returns the cashier's loyalty, not the
guest's in front of them. The till's operation is `getGuestLoyalty` (staff, the guest named in the path).
Whether an operation acts on the caller or on a named customer is a property; this checks it.

An operation **acts on the caller** when it is
  - declared so: `x-ticvai-self-scoped: subject` with no permission (the guest's own record only), or
  - undeclared, but says so in words: no permission, no self-scope, a user session (bearer or guest), not
    public, no parameter or path segment naming whose record (`subjectId`, `guestId`, ...), and its name
    (`getMy...`) or its summary or description ("the caller's own", "their own") says it is the caller's.
    `getLoyaltyPosition` is this case: contracts/README.md says a null permission must be explained by
    `x-ticvai-self-scoped`, `x-ticvai-auth: service` or `security: []`, and it carries none.

A staff screen **acts for a named guest** when it is opened with one (an entry parameter `subjectId`,
`guestId`, `customerId` or `memberId` not from the session) or binds an operation that takes one.

    SUB-CALLER-ON-STAFF     such a screen (operator venue or ticvai) binds a declared caller-scoped operation
    SUB-UNDECLARED-ON-STAFF such a screen binds an operation that acts on the caller without declaring it:
                            declare `x-ticvai-self-scoped`, or bind the operation that names the guest

A staff screen binding a guest-only operation with no guest in view is an audience mismatch, reported by
check-audience-match (AM-STAFF-OP).

`x-ticvai-self-scoped: principal` (the caller's own session, MFA, password) is right on any screen and is
not reported.
Nor is a cart (`/carts/...`): a till's cart is the workstation session's own and the guest is attached to
it (decided 2 October 2026, CHG-SEED-013; contracts/spine/orders.yaml `getCart`, `addCartLine`).

**Report-only until the guest fixes land**; the lead then baselines it and makes it gate.

    python3 tools/check-subject.py [--all] [--update-baseline]
"""
import collections
import sys

import audit_guard as g
import typed_props as tp

RULES = {
    "SUB-CALLER-ON-STAFF": "staff screen acting for a guest binds an operation declared to act on the caller",
    "SUB-UNDECLARED-ON-STAFF": "staff screen acting for a guest binds an operation that acts on the caller without saying so",
}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-subject", RULES)
    ops = tp.operations()
    per_op = collections.Counter()
    undeclared_ops = {o for o in ops if tp.acts_on(o) == "caller-undeclared"}
    n_named = 0
    for code, aud, s in tp.screens():
        if aud != "staff" or not tp.names_a_guest(s):
            continue
        n_named += 1
        sid = s["id"]
        seen = set()
        for op, where, _trig, _why in tp.bindings(s):
            if op in seen or op not in ops:
                continue
            seen.add(op)
            kind = tp.acts_on(op)
            if kind == "named":
                continue
            rule = "SUB-CALLER-ON-STAFF" if kind == "caller-declared" else "SUB-UNDECLARED-ON-STAFF"
            guard.add(rule, f"{sid}:{op}",
                      f"{code} {sid} {s.get('name', '')[:40]}: {op} ({where}) acts on the caller "
                      f"({'declared' if kind == 'caller-declared' else 'undeclared'}; audience "
                      f"{', '.join(sorted(tp.audience(op))) or 'none'})")
            per_op[op] += 1
    guard.note(f"{n_named} staff screen(s) act for a named guest (an entry parameter or a bound operation names one)")
    guard.note(f"{len(undeclared_ops)} operation(s) in the contracts act on the caller without declaring it "
               "(null permission, no self-scope, no subject parameter)")
    if per_op:
        guard.note("operations most often bound on staff screens: "
                   + ", ".join(f"{o} ({n})" for o, n in per_op.most_common(10)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
