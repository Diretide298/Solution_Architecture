#!/usr/bin/env python3
"""Record which shipped app each platform becomes, decided 10 September 2026.

**Fifteen platforms are a development convenience; five apps are what ships.** Everything loads by
the permission the signed-in user holds, so a platform stops being a boundary and becomes a section
of an app. Nothing is merged on disk — the fifteen files stay, because they are the unit people
work in — and this only writes down the destination so the boards, the manifest and the design
batches can group by it.

**The grouping is not a guess.** It was tested against operation overlap, and the package already
half-agreed: P08, P13 and P16 already declared the same `app`, and so did P02 and P05.

| app | absorbs | why the data supports it |
|---|---|---|
| `guest` | P01, P02, P05 | 73–91% operation overlap. Kiosk is guest web in a fixed frame. |
| `venue-pos` | P04, P15 | The kitchen display is the same till software, signed into differently. |
| `venue-staff-mobile` | P06, P07 | 69% overlap, both offline-capable, both non-web. |
| `venue-management` | P08, P12, P13, P16 | P16 shares 75% with P08; the CMS and support desk are its other sections. |
| `ticvai-control` | P09, P10, P11, P14 | All four are TICVAI-operated, whoever signs in. |

**The turnstile is deliberately not an app.** It is an unattended gate: no operator, no screen, no
one to read a state. It is specified as a flow and a state machine instead — `F06 Guest enters the
venue` is the seed, and today it is six steps on a handheld with no beacon, no dynamic QR and no
denial path.

**What this exposes rather than fixes.** `audience` and `operator` stay per platform and still
matter: a partner signing into `ticvai-control` is not a TICVAI operator, and the permission model
has to carry that. `roles.yaml` currently holds six roles and every one of them is a POS role.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""

from __future__ import annotations

import glob
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]

APPS = {
    "guest": {
        "name": "TICVAI Guest",
        "members": ["P01", "P02", "P05"],
        "shells": {"P01": "web", "P02": "mobile", "P05": "kiosk"},
        "note": "**One guest product in three shells.** Web, mobile and kiosk share 73–91% of "
                "their operations; the kiosk is the same product in a fixed frame with no "
                "keyboard, and is deliberately narrower rather than different.",
    },
    "venue-pos": {
        "name": "TICVAI POS",
        "members": ["P04", "P15"],
        "shells": {"P04": "terminal", "P15": "display"},
        "note": "**The kitchen display is the till, signed into differently.** Same software, same "
                "outlet, same orders — what changes is who is looking and what they may do, which "
                "is a permission, not an application.",
    },
    "venue-staff-mobile": {
        "name": "TICVAI Venue Staff",
        "members": ["P06", "P07"],
        "shells": {"P06": "mobile", "P07": "handheld"},
        "note": "**Both offline-capable, both carried rather than sat at.** They cannot fold into "
                "venue management, which is online desktop web, and they share 69% with each "
                "other.",
    },
    "venue-management": {
        "name": "TICVAI Venue Management",
        "members": ["P08", "P12", "P13", "P16"],
        "shells": {"P08": "web", "P12": "web", "P13": "web", "P16": "web"},
        "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` "
                "before this decision. One tenant-level surface that filters across venues, with "
                "analytics, CMS and the support desk as sections of it.",
    },
    "ticvai-control": {
        "name": "TICVAI Control",
        "members": ["P09", "P10", "P11", "P14"],
        "shells": {"P09": "web", "P10": "web", "P11": "web", "P14": "web"},
        "note": "**TICVAI operates all four**, whoever signs in. The partner portal, the "
                "accreditation intake and the developer portal are outward faces of the control "
                "plane, not separate products — but their users are not TICVAI staff, and the "
                "permission model has to hold that line.",
    },
}

# Not an app. Recorded here so the next person does not go looking for its screens.
TURNSTILE = (
    "**The turnstile is a workflow, not an app.** An unattended gate has no operator and nobody "
    "to read a screen: the guest taps and the lane opens or does not. It is specified as a flow "
    "and a state machine — entry and exit, offline validation against locally held keys, beacon "
    "proximity for the dynamic QR, and the denial path — rather than as a platform. Its "
    "configuration surfaces already exist on venue-management (`BO-197 Turnstile & Lane "
    "Behavior`, `BO-194 Device & Gate Command Center`, `BO-168 BLE Beacon & Geofence`)."
)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    apply = "--apply" in sys.argv
    of = {m: (k, v) for k, v in APPS.items() for m in v["members"]}

    todo = []
    docs = {}
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8"))
        p = doc["platform"]
        code = p["code"]
        if code not in of:
            print(f"  ! {code} is in no app — every platform must have a destination")
            continue
        key, spec = of[code]
        block = {
            "app": key,
            "name": spec["name"],
            "shell": spec["shells"][code],
            "siblings": [m for m in spec["members"] if m != code],
            "note": spec["note"],
            "decided": "10 September 2026",
        }
        if p.get("targetApp") != block:
            todo.append(f"{code} -> {key} ({spec['shells'][code]} shell)")
            if apply:
                p["targetApp"] = block
        docs[f] = doc

    if not todo:
        print("nothing to do — every platform already names its target app")
        return 0
    for t in todo:
        print("  " + t)
    print(f"\n{len(APPS)} app(s) from {len(of)} platform(s), plus the turnstile as a workflow")

    if not apply:
        print("\nrun with --apply to write")
        return 0
    for f, doc in docs.items():
        pathlib.Path(f).write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    note = ROOT / "docs" / "active" / "five-apps-10-september.md"
    note.write_text(
        "# Five apps, decided 10 September 2026\n\n"
        + "\n".join(f"## {v['name']} (`{k}`)\n\nAbsorbs {', '.join(v['members'])}.\n\n{v['note']}\n"
                    for k, v in APPS.items())
        + "\n## The turnstile\n\n" + TURNSTILE + "\n",
        encoding="utf-8")
    print(f"written to {len(docs)} platform file(s) and {note.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
