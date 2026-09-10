#!/usr/bin/env python3
"""Every app that reads a session must have a screen that creates one.

**Screens across the package declare `entryState.params` with `from: session`** -- `tenantId`,
`venueId`, `workstationId`, `boxId`. That is the right shape: a screen says what it must be given
and where it comes from, and `Session.scope` is resolved once at login rather than recomputed by
every client. But it only works if something in the same application actually signs the operator
in, and on 10 September three of the five shipped apps consumed a session that nothing in them
produced.

**`venue-pos` was the worst of them and is the client-approved app.** `POS-001 Begin Shift` reads
`workstationId` and `boxId` from the session and calls `openShift` and `selectRole` -- it opens a
till for an operator who was never authenticated. A note written on POS-025 the same day called
POS-001 "the sign-in", which it is not, and that is exactly how a missing screen survives review:
somebody names a neighbouring screen as the one that does the job.

**Measured against the app, not the platform.** Fifteen platform files ship as five applications,
so P15 needs no login of its own -- it is the till, signed into differently. The question is
whether the *app* has a door, and P15's app did not.

**What this refuses**

- An app whose screens read `from: session` and where no screen calls an operation that creates
  one. That is a session consumed and never produced.
- A platform where every screen requires an identity the session has already issued. There is then
  no cold path in at all: every way in assumes you are already inside. **Measured on what a screen
  needs, not on `entryFrom`** -- `ADM-001 Platform Login / MFA` lists `ADM-002` because signing out
  returns you to it, and reading that as an interior screen mistakes the door for a room.

Reported, never repaired -- which screen should own the login is a design decision, and a tool that
invented one would be inventing the front door of an application.

    python3 tools/check-session-entry.py [--verbose]
"""

from __future__ import annotations

import collections
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

# **Operations that mint a session.** `refreshToken` renews one and cannot start it; `getCurrentSession`
# and `getGuestSession` read it. Only these four turn an anonymous caller into a known one.
CREATORS = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}

# **What a door issues, and therefore what its absence proves.** A screen asking for one of these
# cannot be the way in. Kept in step with the same set in `derive-entrystate-params.py`, which
# refuses to write them onto a screen that mints a session.
ISSUED = {"sessionId", "principalId", "operatorId"}


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    _utf8()
    verbose = "--verbose" in sys.argv

    creates = collections.defaultdict(list)     # app -> [(code, sid, name, op)]
    consumes = collections.defaultdict(list)    # app -> [(code, sid, param)]
    platforms = collections.defaultdict(list)   # app -> [code]
    cold = []                                   # platforms whose every entry needs a session

    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        plat = doc.get("platform") or {}
        code = plat.get("code") or f.name.split("-")[0]
        app = (plat.get("targetApp") or {}).get("app")
        if not app:
            continue
        platforms[app].append(code)

        entries, entries_needing = [], []
        for sc in (doc.get("screens") or []):
            ops = {a["operationId"] for a in (sc.get("apis") or []) if isinstance(a, dict)}
            for oid in sorted(ops & CREATORS):
                creates[app].append((code, sc["id"], sc.get("name"), oid))

            params = ((sc.get("entryState") or {}).get("params") or [])
            from_session = [p.get("name") for p in params
                            if isinstance(p, dict) and p.get("from") == "session"]
            for name in from_session:
                consumes[app].append((code, sc["id"], name))

            # **Can you get in from nothing?** A screen is a cold entry if it needs no
            # session-issued identity to render -- either because it mints one, or because it
            # asks for nothing the session has to supply. Measuring `entryFrom` instead was
            # wrong: `ADM-001 Platform Login / MFA` lists `ADM-002` because signing out returns
            # you to it, which makes the login look like an interior screen when it is the door.
            if not (set(from_session) & ISSUED):
                entries.append(sc["id"])
            else:
                entries_needing.append(sc["id"])

        if not entries:
            cold.append((code, app, entries_needing))

    errors, warnings = [], []
    for app in sorted(platforms):
        if consumes[app] and not creates[app]:
            errors.append(
                f"{app}: {len(consumes[app])} screen parameter(s) read `from: session` and no "
                f"screen in {', '.join(sorted(set(platforms[app])))} creates one -- "
                f"the app has no door")

    for code, app, needing in cold:
        warnings.append(
            f"{code}: no screen can be reached without a session already issued "
            f"({len(needing)} screen(s) all require one) -- nothing opens {app} from cold")

    print(f"{len(platforms)} app(s) across "
          f"{sum(len(v) for v in platforms.values())} platform(s)\n")
    for app in sorted(platforms):
        made = creates[app]
        mark = "OK  " if made else "GAP "
        who = ", ".join(f"{c} {s}" for c, s, _n, _o in made[:3]) or "nothing signs anybody in"
        print(f"  {mark}{app:22} {len(consumes[app]):>4} session param(s) - {who}")
        if verbose and made:
            for c, s, n, o in made:
                print(f"          {c} {s} {str(n)[:34]:36} {o}")

    for e in errors:
        print(f"\n  ERROR  {e}")
    for w in warnings:
        print(f"  WARN   {w}")

    print(f"\n{'FAIL' if errors else 'PASS'} - {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
