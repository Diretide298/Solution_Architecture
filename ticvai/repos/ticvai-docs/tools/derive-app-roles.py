#!/usr/bin/env python3
"""Write `roles-by-app.yaml` — what each shipped app's screens actually demand of a signed-in user.

**This package holds two permission vocabularies and they have never met.**

| where | keys | shape | reach |
|---|---|---|---|
| `contracts/**` as `x-ticvai-permission` | **127** | `PRODUCT_VIEW`, `ORDER_CREATE` | 1,536 of 1,626 operations |
| `roles.yaml` as role grants | **35** | `sale.create`, `payment.take` | 6 roles, all POS |

**The overlap is zero.** Not one of the 127 is granted to any role; not one of the 35 appears on any
operation. `check-screens` validates a screen's `guard` against the 35, so the only guards anybody
could write are POS ones — which is exactly what happened: **`venue-pos` declares all 7 guards in
the package and the other four apps declare none across 1,205 screens.**

**So permission-driven loading has nothing to drive it, and the reason is not that the model is
missing.** It is that the comprehensive model lives on the operations, the hand-written one lives
in `roles.yaml`, and no artefact joins them. `Session.scope` in `contracts/spine/identity.yaml`
already says how it is meant to work — *"resolved once at login from the ltree hierarchy with
deny-overrides-allow. Clients filter navigation against this — they never compute it."*

**What this derives, and what it refuses to.** For each app it collects every permission its
screens' operations require, and tiers them by what the key ends in — `_VIEW` is reading,
`_CREATE`/`_MODIFY` is operating, `_CONFIGURE`/`_MANAGE` is administering. That is a real reading
of what the app needs, taken from the contracts.

**It does not invent role names, headcounts or an approval hierarchy.** Who at a venue may
configure pricing is a client's decision, and a plausible answer written here would be read as one
they made. The tiers are named for what they permit, not for a job title.

Derived, idempotent, no arguments. Belongs in `refresh.sh`.
"""

from __future__ import annotations

import collections
import glob
import pathlib
import sys
from datetime import date

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "roles-by-app.yaml"

TIERS = [
    ("read", ("_VIEW", "_READ", "_LIST", "_SEARCH", "_EXPORT"),
     "Sees it. The floor of any signed-in session, and the tier a read-only audit or a "
     "duty manager covering an unfamiliar area sits at."),
    ("operate", ("_CREATE", "_MODIFY", "_UPDATE", "_DELETE", "_CANCEL", "_APPROVE",
                 "_ISSUE", "_REDEEM", "_REFUND", "_VOID", "_ASSIGN", "_EXECUTE", "_RUN"),
     "Does the day's work. Everything a person on shift needs and nothing that changes how "
     "the venue is set up."),
    ("configure", ("_CONFIGURE", "_MANAGE", "_ADMIN", "_PUBLISH", "_GRANT", "_REVOKE"),
     "Changes how it works for everyone else. The tier that needs a named owner, because a "
     "change here outlives the shift that made it."),
]


def tier_of(key: str) -> str:
    for name, suffixes, _ in TIERS:
        if key.endswith(suffixes):
            return name
    return "operate"


def op_permissions() -> dict:
    """operationId -> the permission the contract says it needs."""
    out = {}
    for f in pathlib.Path(ROOT / "contracts").rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for op in item.values():
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = op.get("x-ticvai-permission")
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    perms = op_permissions()
    apps: dict = collections.defaultdict(lambda: {"platforms": [], "ops": set(), "screens": 0,
                                                  "unpermissioned": set()})
    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        p = d["platform"]
        app = (p.get("targetApp") or {}).get("app")
        if not app:
            print(f"  ! {p['code']} names no targetApp — run tools/apply-target-apps.py first")
            continue
        a = apps[app]
        a["platforms"].append(p["code"])
        a["screens"] += len(d["screens"])
        a.setdefault("name", (p.get("targetApp") or {}).get("name"))
        for s in d["screens"]:
            for api in (s.get("apis") or []):
                oid = api.get("operationId")
                if not oid:
                    continue
                a["ops"].add(oid)
                key = perms.get(oid)
                if key:
                    a.setdefault("keys", set()).add(key)
                elif oid in perms:
                    a["unpermissioned"].add(oid)

    hand = yaml.safe_load((ROOT / "roles.yaml").read_text(encoding="utf-8"))
    granted = {g["key"] for v in hand["roles"].values() for g in (v.get("grants") or [])}
    declared = {k for k in perms.values() if k}

    doc = {
        "$id": "ticvai/roles-by-app.yaml",
        "title": "Permissions each shipped app requires",
        "generatedBy": "tools/derive-app-roles.py",
        "generated": date.today().isoformat(),
        "description": (
            "**Derived from what each app's screens call, not decided here.** For every app, the "
            "permissions its operations declare in `x-ticvai-permission`, tiered by what the key "
            "permits. Role names, headcounts and the approval hierarchy are deliberately absent: "
            "who at a venue may configure pricing is the client's decision and a plausible answer "
            "written here would be read as one they made."),
        "theTwoVocabularies": {
            "onOperations": len(declared),
            "inRolesYaml": len(granted),
            "shared": len(declared & granted),
            "note": (
                "**Zero shared keys.** The contracts carry %d permission keys across %d operations; "
                "`roles.yaml` grants %d, all of them POS. `check-screens` validates a screen's "
                "`guard` against `roles.yaml`, so the only guards anyone could write were POS ones "
                "— and that is what the package shows: venue-pos declares every guard in it and "
                "the other four apps declare none. **Joining these two is the work; this file is "
                "the evidence for what the join has to cover.**"
                % (len(declared), sum(1 for v in perms.values() if v), len(granted))),
        },
        "tiers": {name: note for name, _s, note in TIERS},
        "apps": {},
    }

    for app in sorted(apps):
        a = apps[app]
        keys = a.get("keys") or set()
        by_tier = collections.defaultdict(list)
        for k in sorted(keys):
            by_tier[tier_of(k)].append(k)
        doc["apps"][app] = {
            "name": a.get("name"),
            "platforms": sorted(a["platforms"]),
            "screens": a["screens"],
            "operations": len(a["ops"]),
            "permissions": len(keys),
            "tiers": {t: by_tier.get(t, []) for t, _s, _n in TIERS},
            "operationsWithNoPermission": sorted(a["unpermissioned"])[:40],
            "operationsWithNoPermissionCount": len(a["unpermissioned"]),
        }

    OUT.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                   encoding="utf-8")

    print(f"  {len(declared)} permission key(s) on operations · {len(granted)} in roles.yaml · "
          f"{len(declared & granted)} shared")
    for app, v in doc["apps"].items():
        t = v["tiers"]
        print(f"  {app:20} {v['screens']:>4} screens · {v['permissions']:>3} permissions "
              f"(read {len(t['read'])}, operate {len(t['operate'])}, configure {len(t['configure'])})"
              + (f" · {v['operationsWithNoPermissionCount']} op(s) declare none"
                 if v["operationsWithNoPermissionCount"] else ""))
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
