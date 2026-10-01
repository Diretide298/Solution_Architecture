#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A screen calls only operations its audience may call, and a guest screen shows only data guests are served.

**Council of 2 October 2026** (typed properties, `docs/active/council-2-october.md`). The ticketing-guest
process agent found guest screens showing staff-only fields; the POS v2 follow-ups found the till calling
cart operations and `getGuestMenu` that declared only the guest audience (CHG-SEED-006). Each was found by
reading. Both are a mismatch between two declared properties: the platform's `operator` and the
operation's `x-ticvai-audience`. This compares them on every screen.

    AM-GUEST-OP     a guest screen (P01 guest web, P02 guest app, P05 kiosk) binds an operation whose
                    audience has none of guest, anonymous, public
    AM-GUEST-FIELD  a guest screen displays a schema that only non-guest operations send or return
                    (a staff-only shape on a guest screen)
    AM-STAFF-OP     a staff screen (operator venue or ticvai) binds an operation whose audience has none of
                    staff, device, service, public, anonymous (a guest-only or partner-only operation on a
                    till or back office)

The kiosk (P05) runs on a registered device, so `device` operations are its own.

    AM-GUEST-SECURITY an operation whose audience includes guest (or anonymous, public) while its effective
                    security admits no guest: no `guestAuth`, no `{}` alternative, not `[]`. The two
                    declarations contradict each other, and a guest screen calling it is refused
                    (listProducts declares guest and needs bearerAuth: 25 guest screens load it)

and notes, without counting, operations bound on a screen that declare no audience at all.

**Report-only until the guest fixes land** (`run-checks.py` REPORT_ONLY); the lead then records the
baseline (`--update-baseline`) and takes it out of REPORT_ONLY, and a new mismatch blocks.

    python3 tools/check-audience-match.py [--all] [--update-baseline]
"""
import collections
import sys

import audit_guard as g
import typed_props as tp

RULES = {
    "AM-GUEST-OP": "guest screen binds an operation guests may not call",
    "AM-GUEST-FIELD": "guest screen shows a schema only non-guest operations serve",
    "AM-STAFF-OP": "staff screen binds an operation staff may not call",
    "AM-GUEST-SECURITY": "operation declares a guest audience its security lets no guest call",
}


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-audience-match", RULES)
    sch_aud = tp.schema_audience()
    ops = tp.operations()
    undeclared = set()
    per_screen = collections.Counter()
    for code, aud, s in tp.screens():
        sid = s["id"]
        if aud not in ("guest", "staff"):
            continue
        if aud == "guest" and code not in tp.GUEST_PLATFORMS:
            continue
        ok = tp.callable_by(aud, code)
        seen = set()
        for op, where, _trig, _why in tp.bindings(s):
            if op in seen or op not in ops:
                continue
            seen.add(op)
            a = tp.audience(op)
            if not a:
                undeclared.add(op)
                continue
            if a & ok:
                continue
            rule = "AM-GUEST-OP" if aud == "guest" else "AM-STAFF-OP"
            guard.add(rule, f"{sid}:{op}",
                      f"{code} {sid} {s.get('name', '')[:40]}: {op} ({where}) is for {', '.join(sorted(a))}")
            per_screen[(code, sid)] += 1
        if aud == "guest":
            for sch in sorted(tp.displayed_schemas(s)):
                a = sch_aud.get(sch)
                if a and not (a & ok):
                    guard.add("AM-GUEST-FIELD", f"{sid}:{sch}",
                              f"{code} {sid} {s.get('name', '')[:40]}: shows {sch}, served only to "
                              f"{', '.join(sorted(a))}")
                    per_screen[(code, sid)] += 1
    for op in sorted(ops):
        a = tp.audience(op)
        if not a & {"guest", "anonymous", "public"}:
            continue
        need, schemes = tp.needs_session(op)
        if need and "guestAuth" not in schemes:
            guard.add("AM-GUEST-SECURITY", op, f"{op} ({ops[op]['contract']}): audience {', '.join(sorted(a))}, "
                      f"security {schemes}")
    if undeclared:
        guard.note(f"{len(undeclared)} bound operation(s) declare no x-ticvai-audience: "
                   + ", ".join(sorted(undeclared)[:8]) + (" ..." if len(undeclared) > 8 else ""))
    if per_screen:
        guard.note("most findings: " + ", ".join(f"{c} {sid} ({n})" for (c, sid), n in per_screen.most_common(10)))
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
