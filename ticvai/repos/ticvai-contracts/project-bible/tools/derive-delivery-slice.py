#!/usr/bin/env python3
"""Derive the delivery slice: which operations must exist before the first four platforms work.

**Services are built to a slice, frozen at 1.0.0, then extended additively** (decided 23 September,
docs/active/service-docs-and-task-sheet-plan-23-september.md). This tool computes that slice, so it
never has to be typed.

The slice has two parts:

  core   every operation a screen of the in-scope platforms calls.
  setup  operations that write a table a core operation reads, when nothing in the slice writes it.
         A till that lists products needs something that creates products, and that screen lives in
         the Back Office. Followed to a fixpoint, since setup operations read tables too.

**A writer is setup only if it configures rather than trades.** `catalogue.product` is written by
`createProduct` (setup) and a gate's `access.scan_event` is written by `validateAccess`, which is
another platform's daily work. A guest screen showing visit history still works the day it ships;
it shows nothing until the scanner does. Those tables are reported as `fedElsewhere`, not pulled in.

Tables that no operation writes at all are reported as `noWriter`. Most are child lines
(`retail.sale_line`) written inside their parent's operation and missing from the lineage.

Run: python3 tools/derive-delivery-slice.py
Writes: handoff/delivery-slice.json
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "handoff" / "delivery-slice.json"

# The four platforms of the first release. White Labelling is a module, not a platform: the CMS
# screens in its module, and the admin-console screens that call its contract.
PLATFORMS = {
    # Kitchen Display is part of POS (Chinmay, 23 September): the pass and stations are the till's kitchen end.
    "POS": {"name": "Point of Sale", "file": ("P04", "P15"), "pick": None},
    "WEB": {"name": "Guest App - Web", "file": "P01", "pick": None},
    "MOB": {"name": "Guest App - Mobile", "file": "P02", "pick": None},
    "WL": {"name": "White Labelling", "file": ("P13", "P09"), "pick": "white-label"},
}

# Verbs that move a record through its life rather than define it. An operation named this way is
# somebody's daily work, whatever table it writes.
TRADING_VERB = re.compile(
    r"^(accept|abandon|acknowledge|activate|assign|begin|block|book|call|cancel|check|close|"
    r"collect|complete|dispose|override|pause|record|redeem|refire|reopen|report|revoke|settle|"
    r"submit|sync|validate|void|issue|remove|end|unschedule|preview|test|recordUsage)"
)
# Nouns that are an event in a venue's day even when the verb is `create` or `set`: a work order is
# a breakdown, a wait time is a reading, a path closure is a spill on a walkway.
TRADING_NOUN = re.compile(r"WorkOrder|WaitTime|QueueStatus|PathClosure")
# **Not `_APPROVE` or `_DECIDE`.** `setFxRate` carries LEDGER_APPROVE because a rate is sensitive,
# not because setting one is trading; excluding it left every multi-currency price unreadable.
TRADING_PERM = re.compile(r"_(EXECUTE|VALIDATE|BOOK|CREATE|MODIFY)$")


# **Operations Block A needs that no core screen calls** (30 September). The AI engine answers through
# the gateway on every AI call (governance decision point, usage and policy), the operator side of the
# no-data AI the Block A apps use (Help me choose question sets, CMS translations), and the map-import
# label suggestion on BO-093, a Venue Management setup screen the setup walk does not reach because it
# writes no table a core operation reads. From the AI functions review and the P29 pass.
ALSO = ["evaluateAiGovernance", "getAiUsage", "getAiPolicy", "proposeGuidedChoice", "proposeTranslations",
        "proposeVenueLabels", "getAiVenueSettings", "setAiVenueSettings", "importVenueHistory",
        "listVenueHistoryImports", "getVenueHistoryImport",
        # **The Block A AI setup screens' reads** (2 October 2026, CHG-SBO-006, applied by CHG-CLN-014): the
        # screens could write and not read what they wrote. ADM-037 (providers, BYOK, the region, the grant
        # found again after a reload), ADM-508 (forecast versions and accuracy), ADM-520 (capability registry),
        # ADM-523, 526, 527, 528 (policy versions, the effective policy, revoking an exception), ADM-536 (pause a
        # capability, override a decision), ADM-554 (alerts, evaluations, training runs), ADM-556 (incidents),
        # BO-919 and BO-927 (the forecast and the operational requirements).
        "listAiProviders", "testAiProvider", "listOwnPlatformStaffGrants", "getRegionSettings",
        "getAiByokEnablement", "listForecastVersions", "getForecastAccuracy", "listAiCapabilities",
        "listAiGovernancePolicyVersions", "getEffectiveAiPolicy", "revokeAiPolicyException", "pauseAiCapability",
        "overrideAiDecision", "listAiGovernanceAlerts", "listAiEvaluations", "listAiTrainingRuns",
        "openAiIncident", "listAiIncidents", "getForecast", "listOperationalRequirements"]


def is_deferred(s: dict) -> bool:
    """**A screen with a `deferred` block is out of the first release** (decided 28 September, audit
    R187 and R242). None is deferred today: the in-venue notifications feed GST-030 and WEB-046 came back in
    rev 3 (R242 reversed), and the itinerary planner
    GST-051..054 and GST-059 was deferred the same way and came back into Block A on 29 September (MoM
    MOB-6: the Plan tab); its `deferred` blocks were removed. Kept in the package for the release that builds them, but
    neither they nor the operations only they call may count toward Block A."""
    return bool(s.get("deferred"))


def screens(code: str) -> list[dict]:
    f = next((ROOT / "screens").glob(f"{code}-*.yaml"))
    return [s for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"] if not is_deferred(s)]


def ops_of(s: dict) -> list[str]:
    return [a["operationId"] for a in (s.get("apis") or []) if a.get("operationId")]


def platform_screens(p: dict) -> list[dict]:
    if p["pick"] is None:
        files = p["file"] if isinstance(p["file"], tuple) else (p["file"],)
        return [s for f in files for s in screens(f)]
    cms, admin = p["file"]
    return ([s for s in screens(cms) if s.get("module") == "White Label"]
            + [s for s in screens(admin)
               if any(a.get("contract") == p["pick"] for a in (s.get("apis") or []))])


def is_setup(op: str, lin: dict) -> bool:
    return (not TRADING_VERB.match(op) and not TRADING_NOUN.search(op)
            and not TRADING_PERM.search(lin.get("perm") or ""))


def main() -> int:
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))

    called_by: dict[str, set[str]] = defaultdict(set)
    deferred_screens: list[str] = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            if is_deferred(s):
                deferred_screens.append(s["id"])
                continue
            for o in ops_of(s):
                called_by[o].add(s["id"])

    core: dict[str, set[str]] = defaultdict(set)
    plat_screens = {}
    for key, p in PLATFORMS.items():
        ss = platform_screens(p)
        plat_screens[key] = [s["id"] for s in ss]
        for s in ss:
            for o in ops_of(s):
                core[o].add(key)

    missing = sorted(o for o in core if o not in lineage)
    writers: dict[str, set[str]] = defaultdict(set)
    for o, d in lineage.items():
        for t in d.get("writes") or []:
            if not t.startswith("cache:"):
                writers[t].add(o)

    for o in ALSO:
        if o in lineage:
            core.setdefault(o, set()).add("AI")
    slice_ = set(core)
    setup_for: dict[str, set[str]] = defaultdict(set)  # setup op -> tables it makes non-empty
    while True:
        read = {t for o in slice_ for t in (lineage.get(o, {}).get("reads") or [])
                if not t.startswith("cache:")}
        add = set()
        for t in read:
            if writers[t] & slice_:
                continue
            for w in writers[t]:
                if is_setup(w, lineage[w]):
                    add.add(w)
                    setup_for[w].add(t)
        add -= slice_
        if not add:
            break
        slice_ |= add

    fed_elsewhere, no_writer = {}, []
    for t in sorted(read):
        if writers[t] & slice_:
            continue
        if writers[t]:
            fed_elsewhere[t] = sorted(writers[t])
        else:
            no_writer.append(t)

    ops = {}
    for o in sorted(slice_):
        d = lineage[o]
        ops[o] = {
            "part": "core" if o in core else "setup",
            "service": d.get("service"),
            "contract": d.get("contract"),
            "verb": d.get("verb"),
            "path": d.get("path"),
            "perm": d.get("perm"),
            "platforms": sorted(core.get(o, ())),
            "screens": sorted(called_by.get(o, ())),
            "enables": sorted(setup_for.get(o, ())),
        }

    by_service: dict[str, dict[str, int]] = defaultdict(lambda: {"core": 0, "setup": 0})
    for o in ops.values():
        by_service[o["service"]][o["part"]] += 1
    total = defaultdict(int)
    for d in lineage.values():
        total[d.get("service")] += 1

    out = {
        "note": "Derived by tools/derive-delivery-slice.py. Do not hand-edit.",
        "platforms": {k: {"name": p["name"], "screens": plat_screens[k]} for k, p in PLATFORMS.items()},
        "deferredScreens": sorted(deferred_screens),
        "counts": {"core": sum(1 for o in ops.values() if o["part"] == "core"),
                   "setup": sum(1 for o in ops.values() if o["part"] == "setup"),
                   "allOperations": len(lineage)},
        "services": {s: {**c, "total": total[s]} for s, c in sorted(by_service.items())},
        "operations": ops,
        "fedElsewhere": fed_elsewhere,
        "noWriter": no_writer,
        "missingFromLineage": missing,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    c = out["counts"]
    print(f"slice: {c['core']} core + {c['setup']} setup = {c['core'] + c['setup']} of {c['allOperations']} operations")
    for s, v in out["services"].items():
        print(f"  {s:22} core {v['core']:4}  setup {v['setup']:4}  of {v['total']}")
    print(f"fed by other platforms: {len(fed_elsewhere)} tables; no writer at all: {len(no_writer)}")
    print(f"left out as deferred to a later release: {len(deferred_screens)} screens {sorted(deferred_screens)}")
    if missing:
        print(f"ERROR: {len(missing)} called operations missing from lineage: {missing[:5]}")
        return 1
    print(f"-> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
