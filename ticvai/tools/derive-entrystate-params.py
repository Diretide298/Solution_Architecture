#!/usr/bin/env python3
"""Declare the parameters a screen's own operations need, where the screen has not.

**A screen that calls `getEntitlement(entitlementId)` and declares no `entitlementId` cannot know
which ticket it is showing.** `check-screens` has caught this since 20 August — it found 280
screens on the first run — and every time somebody adds an operation to a screen it can happen
again. It happened twice today: five new P04 screens, then thirteen screens across guest web and
guest mobile when the two were brought to parity.

**This fills blanks and never overwrites.** A parameter already declared keeps whatever `from` it
was given, because that is somebody's statement about how the screen is reached and this tool has
no better information.

**Where the parameter comes from is decided by what it is, not by guessing.** Three sources:

- **`session`** — identifiers the signed-in context already carries. A till knows its own
  `workstationId`; a guest session knows its `tenantId`. A screen does not navigate to these.
- **`deepLink`** — a `token` or `code`, which is what a link in an email or an SMS carries and
  the only thing that can arrive from outside the app.
- **`navigation`** — everything else. The screen was reached from somewhere that knew which
  record it was about, which is the ordinary case.

**What it deliberately does not do is invent a `coldEntry`.** That is the answer to *what happens
when somebody opens this URL with no history* — a real product question, different for a wallet
and a checkout, and a sentence written here would read as though somebody had decided it.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import glob
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Identifiers the signed-in context carries rather than the journey.
SESSION = {"tenantId", "venueId", "workstationId", "outletId", "terminalId", "shiftId",
           "principalId", "sessionId", "deviceId", "operatorId"}
# What a link from outside the app carries.
DEEPLINK = {"token", "code", "reference", "ref"}

# **Operations that mint a session.** A screen calling one of these is the door into an app, and a
# door cannot require the key it hands out. `refreshToken` renews a session and cannot start one;
# `getCurrentSession` reads it. Only these four turn an anonymous caller into a known one -- and it
# is their presence alongside those reads that produced the circular parameter in the first place.
CREATORS = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}

# **What a door issues, and therefore cannot ask for.** Narrower than "anything from the session"
# on purpose: `WEB-016 Login / Register` legitimately reads `cartId` from the session, because a
# guest browsing anonymously has a cart before they have an account and it has to survive the
# sign-in. Stripping every session parameter would have thrown that away. These three are the
# identity the login itself mints.
ISSUED = {"sessionId", "principalId", "operatorId"}


def op_paths() -> dict:
    out = {}
    for f in pathlib.Path(ROOT / "contracts").rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for op in item.values():
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = path
    return out


def source_of(param: str) -> str:
    if param in SESSION:
        return "session"
    if param in DEEPLINK:
        return "deepLink"
    return "navigation"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    paths = op_paths()

    docs, todo, stripped = {}, [], []
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        hit = False
        for s in doc["screens"]:
            needed: set = set()
            for api in (s.get("apis") or []):
                needed |= set(re.findall(r"\{([a-zA-Z]+)\}",
                                         paths.get(api.get("operationId"), "")))
            entry = s.get("entryState") or {}

            # **Is this screen the door?** If it mints a session, nothing it declares may be
            # sourced from one. Both halves matter: the parameter is not added below, and one
            # written by an earlier run is taken out, so the fault heals on the next refresh
            # rather than needing somebody to remember it.
            mints = any(a.get("operationId") in CREATORS
                        for a in (s.get("apis") or []) if isinstance(a, dict))
            if mints:
                kept = [p for p in (entry.get("params") or [])
                        if not (isinstance(p, dict) and p.get("from") == "session"
                                and p.get("name") in ISSUED)]
                if entry.get("params") and len(kept) != len(entry["params"]):
                    dropped = [p.get("name") for p in entry["params"]
                               if isinstance(p, dict) and p.get("from") == "session"
                               and p.get("name") in ISSUED]
                    stripped.append((doc["platform"]["code"], s["id"], dropped))
                    if apply:
                        entry["params"] = kept
                        hit = True

            declared = {p.get("name") for p in (entry.get("params") or [])}
            missing = sorted(needed - declared)
            if mints:
                missing = [m for m in missing if m not in ISSUED]
            if not missing:
                continue
            hit = True
            todo.append((doc["platform"]["code"], s["id"], missing))
            if apply:
                ent = s.setdefault("entryState", {})
                ent.setdefault("params", [])
                for m in missing:
                    ent["params"].append({"name": m, "from": source_of(m)})
        if hit:
            docs[f] = doc

    for code, sid, dropped in stripped:
        print(f"  {code}/{sid:<9} - " + ", ".join(dropped) +
              "  (this screen creates the session; it cannot require one)")

    if not todo:
        if stripped and apply:
            for f, doc in docs.items():
                pathlib.Path(f).write_text(
                    yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                    encoding="utf-8")
            print(f"\n{len(stripped)} circular parameter(s) removed")
            return 0
        if stripped:
            print(f"\n{len(stripped)} circular parameter(s) to remove")
            print("run with --apply to write")
            return 0
        print("nothing to do — every screen declares the parameters its operations need")
        return 0

    for code, sid, missing in todo[:14]:
        print(f"  {code}/{sid:<9} + " + ", ".join(f"{m} ({source_of(m)})" for m in missing))
    if len(todo) > 14:
        print(f"  … and {len(todo) - 14} more screen(s)")
    print(f"\n{sum(len(m) for _c, _s, m in todo)} parameter(s) across {len(todo)} screen(s)")

    if not apply:
        print("run with --apply to write")
        return 0
    for f, doc in docs.items():
        pathlib.Path(f).write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"written to {len(docs)} platform file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
