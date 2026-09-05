#!/usr/bin/env python3
"""Derive `handoff/platform-deployment.md` from `screens/`.

**It was hand-maintained and it had twelve rows against fifteen platforms.** P14 Developer, P15
Kitchen Display and P16 Venue Analytics were never added — and `lib/boards.mjs` in the viewer had
written a comment around the wrong number, so the drift travelled.

**The same shape as `platform-P01.md` claiming 35 screens against a live 46**, and as the viewer's
"654 operations" in 25 places: a figure typed once, correct once, and never checked again.

**Nothing generated this file and `check-package` read it.** A checker reading a hand-typed table is
a checker that validates against a claim rather than against the package.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "handoff" / "platform-deployment.md"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    rows = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        drawn = sum(1 for s in doc["screens"]
                    if (s.get("wireframe") or {}).get("status") == "designed")
        rows.append({
            "code": p["code"],
            "short": p.get("shortName", ""),
            "purpose": (p.get("purpose") or p.get("name", ""))[:38],
            "audience": p.get("audience", ""),
            "form": p.get("formFactor", ""),
            "app": p.get("app", ""),
            "offline": "yes" if p.get("offlineCapable") else "no",
            "screens": len(doc["screens"]),
            "drawn": drawn,
        })

    head = [
        "# Platform deployment",
        "",
        "**Derived from `screens/` by `tools/derive-platform-deployment.py`. Do not hand-edit.**",
        "",
        "This table was maintained by hand until 26 August and held **twelve rows against fifteen "
        "platforms** — P14, P15 and P16 were never added. The viewer's `lib/boards.mjs` had "
        "written a comment around that number, so the gap travelled into a second repo before "
        "anybody counted.",
        "",
        "**A figure typed once is correct once.** `platform-P01.md` claimed 35 screens against a "
        "live 46; the viewer carried *654 operations* in 25 places against a live 1,023. This file "
        "is now derived for the same reason both of those were fixed.",
        "",
        f"**{len(rows)} platforms · {sum(r['screens'] for r in rows)} screens · "
        f"{sum(r['drawn'] for r in rows)} drawn.**",
        "",
        "| | Short | Purpose | Audience | Form factor | App | Offline | Screens | Drawn |",
        "|---|---|---|---|---|---|---|---:|---:|",
    ]
    body = [
        f"| {r['code']} | **{r['short']}** | {r['purpose']} | {r['audience']} | {r['form']} | "
        f"`{r['app']}` | {r['offline']} | {r['screens']} | {r['drawn']} |"
        for r in rows
    ]
    tail = [
        "",
        "## What the columns mean",
        "",
        "**Offline** is the platform's own flag. It is not the same claim as an operation's "
        "`x-ticvai-offline-capable` — **the two disagreed on 37 screens until 25 August**, and "
        "`check-screens` now compares a screen's offline prose against the operations it loads.",
        "",
        "**Drawn** counts screens whose `wireframe.status` is `designed` — a board a person drew, "
        "not one this package generated. **It sits on three platforms only**: P04, P06 and P08, "
        "the three with client packs. Twelve platforms are wholly generated.",
        "",
        "**App** is the installable, and it is deliberately not one per platform. `guest-app` "
        "serves P02 and P05; a kiosk is the guest app with no person holding it.",
    ]
    OUT.write_text("\n".join(head + body + tail) + "\n", encoding="utf-8")
    print(f"  {len(rows)} platforms → handoff/platform-deployment.md")
    print(f"    {sum(r['screens'] for r in rows)} screens, {sum(r['drawn'] for r in rows)} drawn")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
