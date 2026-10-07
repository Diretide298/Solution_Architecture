# -*- coding: utf-8 -*-
"""The sprint plan's shared ground (1 October 2026): calendar, two-week sprints, the team, app-modules, the scheduler.

Imported by the three plan generators so they cannot disagree:

  tools/build-service-docs.py     forms the tasks, the app-modules and the blocks (tasks.csv, plan-tasks.csv)
  tools/derive-block-a-schedule.py  times every task of every block on its owner (block-a-schedule.json)
  tools/build-plan-deck.py        the deck, the build-plan workbook and "TICVAI - Sprint Plan.xlsx"

**The replan of 1 October** (PM call, Chinmay: "Sprint 2 weeks. Block A and Block B changes. We need module wise
completion for each platform so each block can be completely tested. Block B is too huge so a step in between.
Modules completed - tickets for web, tickets for app."):

- **Two-week sprints.** Sprint 1 is Monday 5 October to Friday 16 October 2026; Sprint 13 is 22 March to 2 April
  2027. Every weekday is a working day (no holidays, below).
- **App-modules.** A business module is split by the app it lands in: "Ticketing · Guest Web" (P01), "Ticketing ·
  Guest App" (P02), "Ticketing · POS" (P04), "Ticketing · Venue Management" (P08). The back end an app-module
  needs (operations, tables) is attached to it; shared back end goes with the first app-module that needs it and
  the later ones wait on it. A large one is cut into parts small enough to finish in one to three sprints.
- **Blocks are sets of complete app-modules**, each testable end to end, each ending on a sprint boundary:
  A (the first release, ticketed already), then B, C and D (the old B1-B3, with "a step in between").
"""
from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------------------------- calendar
START = dt.date(2026, 10, 5)            # Monday; Block A starts (decided 29 September)
PLAN_END = dt.date(2027, 4, 2)          # end of the six months
# **No holidays: every weekday is a working day** (Chinmay, 4 October 2026, CHG-RFM-013: "No holidays at all"; "1-3
# are not holidays"; leave is handled when it comes up). Until then 1-3 December, 1 January and 9-11 March 2027 were
# taken off as UAE public holidays. The dict stays so a decided day off can be entered here, with its decision.
HOLIDAYS: dict = {}
HOURS_PER_DAY = 8
# Points per developer per working day: Block A as sized on 23 September (3,018 points, 35 days, 9 developers).
# Replaced by the measured pace after the first sprints (re-run, not re-estimate).
PLAN_PACE = 3018 / 35 / 9
SPRINT_DAYS = 14                        # calendar days: Monday of week 1 to the Sunday after week 2
INTERFACES_DAY = 3.0                    # the platform interfaces are published by day 3 (soft platform waits)
SOFT_PLATFORM = {"PLATFORM-KERNEL", "PLATFORM-IDEMPOTENCY", "PLATFORM-OUTBOX"}


def workdays(a, b):
    """Working days from a to b inclusive."""
    d, out = a, []
    while d <= b:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


DAYS = workdays(START, dt.date(2027, 12, 31))          # long past the end, so an overrun shows as one
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}


def day(i):
    """The working day a (fractional) day index falls on."""
    i = int(i // 1)
    return DAYS[min(max(i, 0), len(DAYS) - 1)]


def index_of(d):
    """Day index of the first working day on or after d."""
    return next(i for i, x in enumerate(DAYS) if x >= d)


def _sprints():
    out, n, s = [], 1, START
    while s + dt.timedelta(days=11) <= DAYS[-1]:
        e = s + dt.timedelta(days=11)                       # the Friday of week 2
        wd = workdays(s, e)
        out.append({"n": n, "name": f"Sprint {n}", "start": s, "end": e, "days": len(wd),
                    "first": DAY_INDEX[wd[0]] if wd else None, "last": DAY_INDEX[wd[-1]] if wd else None,
                    "inPlan": e <= PLAN_END})
        s += dt.timedelta(days=SPRINT_DAYS)
        n += 1
    return out


SPRINTS_ALL = _sprints()
SPRINTS = [s for s in SPRINTS_ALL if s["inPlan"]]      # Sprint 1-13: 5 Oct 2026 to 2 Apr 2027
LAST_SPRINT = SPRINTS[-1]["n"]


def sprint_of_index(i):
    """The sprint a (fractional) working-day index falls in."""
    d = day(i)
    return sprint_of_date(d)


def sprint_of_date(d):
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    for sp in SPRINTS_ALL:
        if sp["start"] <= d <= sp["start"] + dt.timedelta(days=SPRINT_DAYS - 1):
            return sp["n"]
    return 1 if d < START else SPRINTS_ALL[-1]["n"]


def sprint_end_index(n):
    """Day index just after the last working day of sprint n (a task ending at or before it is in the sprint)."""
    sp = SPRINTS_ALL[n - 1]
    return sp["last"] + 1


# ---------------------------------------------------------------------------------------------- modules
MODULE_OF_CONTRACT = {
    "identity": "Identity, Roles & Security", "tenancy": "Tenancy, Venues & Devices",
    "cross-region": "Platform Operations", "platform-ops": "Platform Operations",
    "subscription": "Subscription & Licensing", "approvals": "Approval Workflows",
    "public-api": "Developer Portal & Public API", "assets": "Digital Asset Management",
    "catalogue": "Ticketing Catalogue & Products", "orders": "Orders & Reservations",
    "payments": "Payments", "wallet": "Wallet & Cashless", "promotions": "Pricing, Promotions & Bundles",
    "seating": "Seat Management & Venue Maps", "venue-map": "Seat Management & Venue Maps",
    "white-label": "White Label & CMS", "queue": "Virtual Queue",
    "fnb": "Food & Beverage", "shift": "Food & Beverage", "retail": "Retail",
    "inventory": "Inventory & Procurement", "rental": "Rentals",
    "access": "Admission & Access Control", "accreditation": "Accreditation",
    "resources": "Resources & Capacity", "workforce": "Workforce & Staff",
    "maintenance": "Maintenance & Safety", "games": "Games & Rides", "transport": "Transport",
    "finance": "Finance, Ledger & Tax", "reporting": "Reporting & Analytics",
    "marketing-crm": "Marketing & CRM", "ai": "AI & Intelligence",
}
FOUNDATION = "Foundation & Setup"
PACKAGES = [
    ("Platform Foundation", "Everything the apps stand on: sign-in, tenants and venues, devices, licensing, approvals, the public API.",
     [FOUNDATION, "Identity, Roles & Security", "Tenancy, Venues & Devices", "Platform Operations",
      "Subscription & Licensing", "Approval Workflows", "Developer Portal & Public API", "Digital Asset Management"]),
    ("Ticketing & Guest Commerce", "What a guest buys and how: catalogue, pricing, seats and maps, orders, payments, wallet, the branded storefront and app.",
     ["Ticketing Catalogue & Products", "Pricing, Promotions & Bundles", "Seat Management & Venue Maps",
      "Orders & Reservations", "Payments", "Wallet & Cashless", "White Label & CMS", "Transport"]),
    ("Food, Beverage & Retail", "Selling at the venue: F&B with the kitchen display, retail, rentals, stock and purchasing.",
     ["Food & Beverage", "Retail", "Rentals", "Inventory & Procurement"]),
    ("Venue Operations", "Running the venue day to day: gates and access, accreditation, capacity, staff, maintenance, rides, queues.",
     ["Admission & Access Control", "Accreditation", "Resources & Capacity", "Workforce & Staff",
      "Maintenance & Safety", "Games & Rides", "Virtual Queue"]),
    ("Finance & Insights", "The money and the numbers: ledger, VAT and e-invoicing, reports and analytics.",
     ["Finance, Ledger & Tax", "Reporting & Analytics"]),
    ("Customer & Marketing", "Knowing and reaching the guest: CRM, segments, campaigns, loyalty, support.",
     ["Marketing & CRM"]),
    ("AI & Intelligence", "The AI gateway and governance, the guest concierge, Help me choose, translations, the planner agent; forecasting, fraud and recommendations rules-first.",
     ["AI & Intelligence"]),
]
PACKAGE_OF = {m: p for p, _, ms in PACKAGES for m in ms}
MODULES = [m for _, _, ms in PACKAGES for m in ms]
# One build order from start to end (30 September): 1 foundation, 2 commerce, 3 operations, 4 engagement, 5 reporting.
MODULE_PHASE = {
    FOUNDATION: 1, "Identity, Roles & Security": 1, "Tenancy, Venues & Devices": 1, "Platform Operations": 1,
    "Subscription & Licensing": 1, "Approval Workflows": 1, "Developer Portal & Public API": 1,
    "Digital Asset Management": 1, "White Label & CMS": 1,
    "Ticketing Catalogue & Products": 2, "Pricing, Promotions & Bundles": 2, "Seat Management & Venue Maps": 2,
    "Orders & Reservations": 2, "Payments": 2, "Wallet & Cashless": 2, "Admission & Access Control": 2,
    "Finance, Ledger & Tax": 2,
    "Food & Beverage": 3, "Retail": 3, "Rentals": 3, "Inventory & Procurement": 3, "Transport": 3,
    "Accreditation": 3, "Resources & Capacity": 3, "Workforce & Staff": 3, "Maintenance & Safety": 3,
    "Games & Rides": 3, "Virtual Queue": 3,
    "Marketing & CRM": 4, "AI & Intelligence": 4,
    "Reporting & Analytics": 5,
}
PHASE_NAME = {0: "Plumbing", 1: "Foundation", 2: "Commerce", 3: "Operations", 4: "Engagement", 5: "Reporting"}
# The short name an app-module carries ("Ticketing · Guest Web").
MODULE_SHORT = {
    FOUNDATION: "Foundation", "Identity, Roles & Security": "Identity & Security",
    "Tenancy, Venues & Devices": "Tenancy & Venues", "Platform Operations": "Platform Operations",
    "Subscription & Licensing": "Subscription & Licensing", "Approval Workflows": "Approvals",
    "Developer Portal & Public API": "Public API", "Digital Asset Management": "Digital Assets",
    "Ticketing Catalogue & Products": "Ticketing", "Pricing, Promotions & Bundles": "Pricing & Promotions",
    "Seat Management & Venue Maps": "Seating & Maps", "Orders & Reservations": "Orders & Reservations",
    "Payments": "Payments", "Wallet & Cashless": "Wallet & Cashless", "White Label & CMS": "White Label",
    "Transport": "Transport", "Food & Beverage": "Food & Beverage", "Retail": "Retail", "Rentals": "Rentals",
    "Inventory & Procurement": "Inventory", "Admission & Access Control": "Admission & Access",
    "Accreditation": "Accreditation", "Resources & Capacity": "Resources & Capacity",
    "Workforce & Staff": "Workforce", "Maintenance & Safety": "Maintenance & Safety",
    "Games & Rides": "Games & Rides", "Virtual Queue": "Virtual Queue", "Finance, Ledger & Tax": "Finance & Tax",
    "Reporting & Analytics": "Reporting", "Marketing & CRM": "Marketing & CRM", "AI & Intelligence": "AI",
}
MODULE_CODE = {m: re.sub(r"[^A-Z0-9]+", "-", s.upper()).strip("-") for m, s in MODULE_SHORT.items()}
# A screen that names no operation belongs to its app's main module.
PLATFORM_MODULE = {
    "P01": "White Label & CMS", "P02": "White Label & CMS", "P04": "Food & Beverage", "P05": "Orders & Reservations",
    "P06": "Workforce & Staff", "P07": "Admission & Access Control", "P08": "Tenancy, Venues & Devices",
    "P09": "Platform Operations", "P10": "Orders & Reservations", "P11": "Accreditation", "P12": "Marketing & CRM",
    "P13": "White Label & CMS", "P14": "Developer Portal & Public API", "P15": "Food & Beverage",
    "P16": "Reporting & Analytics", "P17": "Subscription & Licensing",
}
# The app (platform) half of an app-module's name, in the order apps are built inside a module.
PLATFORM_NAME = {
    "P01": "Guest Web", "P02": "Guest App", "P04": "POS", "P15": "Kitchen Display", "P05": "Kiosk",
    "P06": "Staff App", "P07": "Scanner", "P08": "Venue Management", "P13": "CMS", "P16": "Analytics",
    "P12": "Support Console", "P11": "Accreditation Web", "P09": "TICVAI Console", "P17": "Sign-up",
    "P10": "Partner Portal", "P14": "Developer Portal", "API": "API only",
}
PLATFORM_ORDER = list(PLATFORM_NAME)
# Key prefix of a screen task, by platform. Block A's own keys stay as they are (APP-POS covers the Kitchen
# Display, APP-SETUP the setup slice of a back-office screen, VM- the Venue Management waves): the screen id is
# a task's identity, so the prefix is metadata (build-service-docs.py reconcile_keys).
SCREEN_PREFIX = {
    "P01": "APP-WEB", "P02": "APP-MOB", "P04": "APP-POS", "P15": "APP-POS", "P05": "APP-KIOSK",
    "P06": "APP-STAFF", "P07": "APP-SCANNER", "P08": "VM", "P09": "APP-CONSOLE", "P10": "APP-PARTNER",
    "P11": "APP-ACCRED", "P12": "APP-SUPPORT", "P13": "APP-CMS", "P14": "APP-DEVPORTAL", "P16": "APP-ANALYTICS",
    "P17": "APP-SIGNUP",
}
# The pool a screen's work is drawn from: mobile runtimes, the POS runtimes, or web.
POOL_OF_PLATFORM = {"P02": "mob", "P05": "mob", "P06": "mob", "P07": "mob", "P04": "pos", "P15": "pos"}
SCHEMA_CONTRACT = {"pii": "identity", "ledger": "finance", "control": "tenancy", "venuemap": "venue-map",
                   "whitelabel": "white-label", "marketing": "marketing-crm", "subscription": "subscription",
                   "platform": "platform-ops", "baseline": None, "seating": "seating"}
# **Block A ships in two drops** (Chinmay, 3 October 2026, CHG-RONEP-007): A (A1, the first release by 27 November)
# and A2 (the completion work that does not fit in it, right after and ahead of Block B). A2 sorts after A and before
# B everywhere a block is ranked; its tickets keep their keys.
BLOCKS = ["A", "A2", "B", "C", "D"]
BLOCK_A_FAMILY = ("A", "A2")
LATER_BLOCKS = ["B", "C", "D"]


def block_label(b):
    """'A1' for Block A (its first drop, key BLOCK-A), else the block's own code."""
    return "A1" if b == "A" else b


def am_name(module, platform, part=None, parts=1, variant=""):
    """'Ticketing · Guest Web', 'Ticketing · Venue Management 2 of 4', 'Ticketing · Venue Management (setup)'."""
    name = f"{MODULE_SHORT.get(module, module)} · {PLATFORM_NAME.get(platform, platform)}"
    if variant:
        name += f" ({variant})"
    if parts > 1 and part:
        name += f" {part} of {parts}"
    return name


def am_key(module, platform, part=None, variant=""):
    k = f"AM-{MODULE_CODE.get(module, 'X')}-{platform}"
    if variant:
        k += "-" + re.sub(r"[^A-Z0-9]+", "-", variant.upper()).strip("-")
    if part and part > 1:
        k += f"-{part}"
    return k


def am_order(module, platform, part=0, variant=""):
    """The order app-modules are built in: build phase, then package order, then the app, then the part."""
    return (MODULE_PHASE.get(module, 3), MODULES.index(module) if module in MODULES else 99,
            PLATFORM_ORDER.index(platform) if platform in PLATFORM_ORDER else 99, 0 if variant else 1, part or 0)


# ---------------------------------------------------------------------------------------------- team
def load_team(team=None):
    """The roster and its rules from docs/active/team.json: [{name, role, pools, pace, from, fromIndex}], caps."""
    team = team or json.loads((ROOT / "docs" / "active" / "team.json").read_text(encoding="utf-8"))
    pace = team.get("pace") or {}
    people = []
    for p in team.get("people") or []:
        frm = dt.date.fromisoformat(p.get("from") or START.isoformat())
        people.append({"name": p["name"], "role": p.get("role", ""), "pools": list(p.get("pools") or []),
                       "pace": float(pace.get(p["name"], 1.0)), "from": frm, "fromIndex": float(index_of(frm))})
    caps = defaultdict(dict)                     # pool -> person -> largest task (points) they take there
    for who, cap in (team.get("backendHelpers") or {}).items():
        caps["be"][who] = cap
    for area, per in (team.get("caps") or {}).items():
        pool = {"MOB": "mob", "WEB": "web", "POS": "pos"}.get(area, area.lower())
        caps[pool].update(per)
    return people, dict(caps), team


def sprint_settings(team):
    sp = team.get("sprintPlan") or {}
    targets = {b["block"]: int(b["endSprint"]) for b in sp.get("blocks") or []}
    for b, n in {"A": 4, "A2": 5, "B": 7, "C": 10, "D": 13}.items():
        targets.setdefault(b, n)
    return {"targets": targets, "ticketBlocks": list(sp.get("ticketBlocks") or ["A", "B"]),
            "fePointsPerAppModule": int(sp.get("fePointsPerAppModule") or 45),
            "stableOwnersSince": (sp.get("stableOwners") or {}).get("since", "r2"),
            # the apps Block A completes all the functionality of (Chinmay, 1 October)
            "blockAApps": list(sp.get("blockAApps") or ["P01", "P02", "P04", "P15"]),
            # a block whose end is decided (Block A: 40 working days, Sprint 4): its test sits in its target sprint
            # whatever the work at normal hours says; the overtime to get there is reported
            "fixed": {b["block"] for b in sp.get("blocks") or [] if b.get("fixed")},
            "pace": dict(sp.get("pace") or {}),
            # sprints after the last block's target: buffer (Claude Design returns, defects, change requests, AI help)
            "bufferSprints": [int(x) for x in sp.get("bufferSprints") or []]}


def pace_model(team, items):
    """Points per developer per working day as a function of the day index, and a line saying what it is.

    Default (team.json sprintPlan.pace.tasksPerDevDay null): PLAN_PACE, Block A's plan of record, every sprint.
    A scenario (Chinmay, 1 October: "5 tasks per day ... ramp up towards the next block ... 2x by Block D"):
    tasksPerDevDay x the average points of a non-AI task in the plan, held through Sprint rampFromSprint - 1,
    then rising linearly sprint by sprint to rampTo x that at Sprint rampFullSprint, and held. Per-person pace
    (Surendra 60%) still applies on top; AI engine tasks are sized in days and are not affected.

    **Block A at 6 tasks a day** (Chinmay, 3 October, CHG-RONEP-009): `tasksPerDevDayBlockA` replaces tasksPerDevDay in the
    sprints before the ramp (Sprints 1-4); the ramp after them still starts from tasksPerDevDay, so it is unchanged. A
    task-a-day is per developer: N average tasks (the average points of a non-AI task) a working day, each."""
    cfg = sprint_settings(team)["pace"]
    tpd = cfg.get("tasksPerDevDay")
    if not tpd:
        return (lambda i: PLAN_PACE), f"{PLAN_PACE:.2f} points per developer per day (Block A's plan of record)", PLAN_PACE
    # a task of a decided app-module scheduled after a block (`paceExclude`, CHG-R4-003) does not re-pace the work already
    # pushed: the average a developer-day is measured on the plan without it
    pts = [float(it.get("points") or 0) for it in items if it.get("track") != "AI" and not it.get("paceExclude")]
    avg = sum(pts) / max(len(pts), 1)
    base = float(tpd) * avg
    to, a, b = float(cfg.get("rampTo") or 1.0), int(cfg.get("rampFromSprint") or 5), int(cfg.get("rampFullSprint") or 11)

    early = float(cfg.get("tasksPerDevDayBlockA") or tpd) / float(tpd)

    def factor(n):
        if n < a:
            return early
        if n >= b:
            return to
        return 1.0 + (to - 1.0) * (n - a + 1) / (b - a + 1)

    by_sprint = {sp_["n"]: base * factor(sp_["n"]) for sp_ in SPRINTS_ALL}

    def at(i):
        return by_sprint.get(sprint_of_index(max(i, 0.0)), base * to)
    return at, (f"{tpd * early:g} tasks per developer per day x {avg:.2f} points a task = {base * early:.1f} points, through "
                f"Sprint {a - 1}; from Sprint {a} the ramp from {tpd:g} ({base:.1f}) rises to {to:g}x ({base * to:.1f}) by "
                f"Sprint {b}, then held"), base


def release_number(tag):
    m = re.match(r"r(\d+)$", str(tag or ""))
    return int(m.group(1)) if m else 0


def pinned_owners(team, rebalance=False, bundle_path=None):
    """**Stable owners** (plan item L2, 1 October): once a ticket is pushed its owner is kept by the plan; only
    new work is placed. The owners are the ones the last release pushed (handoff/service-docs/op-release.json,
    the bundle committed with that tag; OpenProject names mapped back to the plan's). A started ticket is also
    kept server-side: op-release.rb changes assignee and sprint on New tickets only.

    The rule takes effect for bundles from `sprintPlan.stableOwners.since` on (r2): the replan of 1 October moves
    New tickets on purpose. `--rebalance` (derive-block-a-schedule.py, build-service-docs.py) turns it off for a
    deliberate move; op-release.rb still leaves started tickets where they are."""
    if rebalance:
        return {}, "rebalance: owners of pushed tickets may move (started tickets are still kept by op-release.rb)"
    since = sprint_settings(team)["stableOwnersSince"]
    path = Path(bundle_path) if bundle_path else ROOT / "handoff" / "service-docs" / "op-release.json"
    if not path.exists():
        return {}, "no release bundle: nothing pinned"
    try:
        b = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}, "release bundle unreadable: nothing pinned"
    rel = b.get("release")
    if release_number(rel) < release_number(since):
        return {}, f"last bundle is {rel}, before {since}: owners are placed afresh (the replan moves New tickets)"
    back = {v: k for k, v in (b.get("aliases") or {}).items()}
    # **Pushed is what OpenProject holds** (CHG-R4-003, 5 October): the bundle's `ids` are pms-map.json as it was when
    # the bundle was built, so the r1 bundle, built before its own push, names none of the 7,967 tickets it created;
    # pms-map.json, written back by the push, does.
    pushed = set(b.get("ids") or {})
    kmap = path.parent / "pms-map.json"
    if kmap.exists():
        try:
            pushed |= {k for k in json.loads(kmap.read_text(encoding="utf-8")) if "#" not in k}
        except Exception:
            pass
    pins = {}
    for t in b.get("tickets") or []:
        if t.get("type") == "Task" and t.get("assignee") and t["key"] in pushed:
            pins[t["key"]] = back.get(t["assignee"], t["assignee"])
    return pins, f"{len(pins)} pushed tickets keep the owner release {rel} gave them"


def migration_owner(team):
    """(owner, compiled key pattern) of team.json `migrations` (CHG-R5-001, 7 October): every task whose key matches
    is that person's, with its table sub-tasks, whoever the plan or a pin would give it -- a rule on the key, so a
    migration the plan makes later is theirs too. (None, None) when team.json has no such rule."""
    m = team.get("migrations") or {}
    if not m.get("owner"):
        return None, None
    return m["owner"], re.compile(m.get("keys") or r"^MIG-")


def never_testers(team):
    """The people team.json `neverTests` keeps off every module test (CHG-R5-004, 7 October: Hrushikant Patkar, never a
    checker)."""
    return set(team.get("neverTests") or [])


def no_test_takeover(team):
    """The people team.json `noTestTakeover` keeps off the module tests a `neverTests` person gives up (CHG-R5-005,
    7 October: Surendra)."""
    return set(team.get("noTestTakeover") or [])


def owner_moves(extra):
    """{task key: (from, to)} of block-a-extra-tasks.json `ownerMoves` (CHG-R5-003, 7 October): the lead's moves of
    pushed or planned tasks, applied over the pin while `from` still holds the task."""
    return {k: (v.get("from"), v.get("to")) for k, v in (extra.get("ownerMoves") or {}).items()
            if isinstance(v, dict) and v.get("from") and v.get("to")}


def is_migration_of(rx, key):
    """True for a task key the migration rule covers; a sub-task (KEY#schema.table) by its task's key."""
    return bool(rx and rx.search(str(key or "").partition("#")[0]))


# ---------------------------------------------------------------------------------------------- testing
# **The test strategy** (decided 1 October, docs/active/block-test-strategy.md): one module test per app-module
# (about 10% of its points, at least 2, by a peer in its stack who is not its main builder, right after its last
# ticket), and one block test per block in the last three working days of the block's final sprint, by a back-end
# and front-end pair rotating per block, led by Chinmay Parab. No new feature work starts in those three days; people
# not on the block test fix its defects (unassigned slack) or take ready next-block work that does not build on the
# block under test.
TEST_SHARE = 0.10
TEST_MIN_POINTS = 2
BLOCK_TEST_DAYS = 3


def test_settings(team):
    bt = (team.get("sprintPlan") or {}).get("blockTests") or {}
    pairs = bt.get("pairs") or [["Pranay Shinde", "Chitrangi Mestry"], ["Tanmay Dukhande", "Chinmay Patkar"],
                                ["Pranay Shinde", "Pallavi Sawant"], ["Tanmay Dukhande", "Pradnya Yeram"]]
    return {"days": float(bt.get("days") or BLOCK_TEST_DAYS), "pairs": pairs, "lead": bt.get("lead") or "Chinmay Parab",
            "share": float(bt.get("moduleTestShare") or TEST_SHARE),
            "minPoints": int(bt.get("moduleTestMinPoints") or TEST_MIN_POINTS)}


def test_pair(b, tests):
    """The block-test pair of a block, rotating over A, B, C and D as before A2 existed; A2 keeps Block A's pair."""
    order = ["A", "B", "C", "D"]
    return tests["pairs"][order.index("A" if b == "A2" else b) % len(tests["pairs"])]


def window_of(n, days=BLOCK_TEST_DAYS):
    """The block-test window of sprint n: its last `days` working days, as (start index, end index)."""
    end = sprint_end_index(n)
    return float(end - days), float(end)


def final_sprint(last_end, days=BLOCK_TEST_DAYS, at_least=1):
    """The first sprint (from `at_least`) whose block-test window starts after the block's work has ended."""
    n = max(at_least, 1)
    while window_of(n, days)[0] < last_end - 1e-6:
        n += 1
    return n


def flow_claims(flows, screen_block, op_block):
    """For each flow (flows/F*.yaml): the block that completes it -- every screen and operation in its steps and
    branches built by then -- and the first block from which some of its steps can run (a step whose screen and
    operations are built). A flow needing a screen or operation the plan does not build is complete in no block.
    Returns {id: {"name", "criticality", "complete": block or "", "partlyFrom": block or "", "missing": [...]}}."""
    rank = {b: i for i, b in enumerate(BLOCKS)}
    out = {}
    for f in flows:
        steps = list(f.get("steps") or [])
        for br in f.get("branches") or []:
            # a branch is resolved on a screen (resolvedBy); that screen is part of the flow's test too
            if isinstance(br, dict) and re.match(r"^[A-Z]+-\d{3,}[A-Z]?$", str(br.get("resolvedBy") or "")):
                steps.append({"screen": br["resolvedBy"]})
        need, step_blocks, missing = [], [], []
        for st in steps:
            if not isinstance(st, dict):
                continue
            here = []
            scr = st.get("screen")
            if scr:
                here.append(screen_block.get(scr))
                if scr not in screen_block:
                    missing.append(scr)
            for o in st.get("operations") or []:
                o = str(o).split()[0] if o else o
                here.append(op_block.get(o))
                if o not in op_block:
                    missing.append(o)
            if here:
                need += here
                step_blocks.append(None if None in here else max(here, key=lambda b: rank[b]))
        complete = "" if (not need or None in need) else max(need, key=lambda b: rank[b])
        partly = [b for b in step_blocks if b]
        first = min(partly, key=lambda b: rank[b]) if partly else ""
        out[f["id"]] = {"name": f.get("name", ""), "criticality": f.get("criticality", ""), "complete": complete,
                        "partlyFrom": first if first and first != complete else "",
                        "missing": sorted(set(missing))}
    return out


# The operations that open a session: a screen calling one is a door, where its app starts (check-doors, CHG-DOOR-004).
DOOR_OPS = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}


def is_entry(s):
    """Where an app starts: `navigation.isEntryPoint`, or a door (a screen calling an operation that opens a session)."""
    return bool((s.get("navigation") or {}).get("isEntryPoint")
                or {a.get("operationId") for a in s.get("apis") or [] if isinstance(a, dict)} & DOOR_OPS)


def nav_exits(s):
    """The screens a screen leads to: `navigation.exitTo` and `navigation.transitions[].to`."""
    nav = s.get("navigation") or {}
    out = [x if isinstance(x, str) else (x or {}).get("to") for x in nav.get("exitTo") or []]
    out += [t.get("to") for t in nav.get("transitions") or [] if isinstance(t, dict)]
    return [x for x in out if x]


def nav_paths(app_screens, a_set, targets):
    """**How a Block A screen is reached** (CHG-RONEP-006, 3 October). Over one app's screens ({id: screen}), from its
    entries (`navigation.isEntryPoint`, and every door: a screen calling an operation that opens a session), the path to each target that passes the fewest screens outside `a_set` (a 0-1
    shortest path: a screen in `a_set` costs nothing). Returns {target: [entry, ..., target]} for every target with a path;
    a target with none is left out. Shared by build-service-docs.py (which pulls the screens on these paths into Block A)
    and check-plan-closure.py (C-REACH)."""
    import heapq
    entries = sorted(sid for sid, s in app_screens.items() if is_entry(s))
    dist, prev, pq = {}, {}, []
    for e in entries:
        c = 0 if e in a_set else 1
        if c < dist.get(e, 1e9):
            dist[e] = c
            heapq.heappush(pq, (c, e))
    while pq:
        c, u = heapq.heappop(pq)
        if c > dist.get(u, 1e9):
            continue
        for v in nav_exits(app_screens[u]):
            if v not in app_screens:
                continue
            nc = c + (0 if v in a_set else 1)
            if nc < dist.get(v, 1e9):
                dist[v], prev[v] = nc, u
                heapq.heappush(pq, (nc, v))
    out = {}
    for t in targets:
        if t not in dist:
            continue
        path, x = [t], prev.get(t)
        while x is not None:
            path.append(x)
            x = prev.get(x)
        out[t] = path[::-1]
    return out


# ---------------------------------------------------------------------------------------------- scheduler
def _gap(slots, ready, dur, forbid=()):
    """The first start at or after `ready` where `dur` fits between the busy slots (sorted) and that is not inside a
    window where this task may not start (a block test's three days)."""
    s = ready
    while True:
        for b0, b1 in slots:
            if s + dur <= b0 + 1e-9:
                break
            if s < b1:
                s = b1
        bad = next((w for w in forbid if w[0] - 1e-9 <= s < w[1] - 1e-9), None)
        if not bad:
            return s
        s = bad[1]


def is_soft(item, dep):
    """A wait that holds the finish but not the start (30 September): a screen on its back end (built against the
    mock server); a service on the platform kernel, idempotency and the outbox (written against interfaces published
    in week 1); another service's task whose data a back-end task reads (built against seeded data); the kernel on
    sign-in setup. Setup, migrations and the AI engine's setup stay hard; a test waits for all it tests."""
    tr, k = item["track"], item["key"]
    if tr == "Frontend":
        return dep["track"] in ("Backend", "Database")
    if tr == "Backend":
        if dep["key"] in SOFT_PLATFORM:
            return True
        return (dep["track"] == "Backend" and dep.get("service") and dep.get("service") != item.get("service")
                and not dep["key"].startswith(("PLATFORM-", "KERNEL-", "SETUP-", "MIG-")))
    return k == "PLATFORM-KERNEL" and dep["key"] == "SETUP-AUTH"


def duration(item, pace_of, pace_at=None, at=0.0):
    if item.get("days"):
        return float(item["days"])
    pts = float(item.get("points") or 0)
    pace = pace_at(at) if pace_at else PLAN_PACE
    return pts / (pace * pace_of.get(item["who"], 1.0)) if pts else 0.25


def schedule(items, people, caps=None, svc_owner=None, backend_owners=(), helper_share=None, choose=True,
             freeze=None, open_blocks=(), pace_at=None):
    """A list scheduler over working days from Monday 5 October 2026, for every task of every block.

    Items come in build order (each after everything it waits on). Each is placed in its person's first free gap
    that starts after it is ready -- so a person whose next ticket waits takes the next one that is ready (30
    September) -- at the plan's pace times the person's pace. Waits are hard (start after) or soft (finish after,
    `is_soft`); a back-end task with a soft platform wait starts no earlier than INTERFACES_DAY.

    An item with `who` keeps it. One without is given, when `choose`, to whoever in its pool can start it
    earliest: a person outside their home pool only when it saves two days, a back-end owner on another owner's
    service only when it saves one, a helper within their cap (team.json backendHelpers, caps) and a helper with
    a share (helperShare, Deep) only while their back-end load stays under that share of an owner's. A module test
    (`peerOf`: the keys it tests) never goes to the person who built most of them.

    `freeze` {block: (start, end)}: the block-test windows. Inside block X's window no task starts except a test,
    or later-block work none of whose waits is a task of block X (items carry `block`).

    Returns {key: {"start", "end", "who"}} in working days from 5 October (fractions of a day)."""
    caps = caps or {}
    svc_owner = svc_owner or {}
    helper_share = helper_share or {}
    freeze = freeze or {}
    rank_b = {b: i for i, b in enumerate(BLOCKS)}
    pace_of = {p["name"]: p["pace"] for p in people}
    rank = defaultdict(dict)
    for p in people:
        for i, pool in enumerate(p["pools"]):
            rank[pool][p["name"]] = i
    busy = {p["name"]: ([(0.0, p["fromIndex"])] if p["fromIndex"] > 0 else []) for p in people}
    be_load = Counter()
    by_key = {it["key"]: it for it in items}
    start, end, who_of, dur_of = {}, {}, {}, {}

    def forbidden(it):
        if it["track"] == "Test" or not freeze:
            return ()
        b = it.get("block") or "A"
        dep_blocks = {(by_key[d].get("block") or "A") for d in it.get("deps") or () if d in by_key}
        # a block whose end is decided (open_blocks) keeps working in its own window at normal hours: that work is
        # the overtime the plan reports, not something the window can stop
        return sorted(w for x, w in freeze.items()
                      if not (rank_b.get(b, 0) > rank_b.get(x, 0) and x not in dep_blocks)
                      and not (x == b and x in open_blocks))

    def place(slots, ready, it_, forbid):
        d = duration(it_, pace_of, pace_at, ready)
        s = _gap(slots, ready, d, forbid)
        if pace_at:
            d2 = duration(it_, pace_of, pace_at, s)
            if abs(d2 - d) > 1e-9:
                d = d2
                s = _gap(slots, ready, d, forbid)
        return s, d

    for it in items:
        k = it["key"]
        deps = [d for d in it.get("deps") or () if d in end]
        hard = [d for d in deps if not is_soft(it, by_key[d])]
        ready = max([end[d] for d in hard] or [0.0])
        if len(hard) < len(deps) and it["track"] != "Frontend":
            ready = max(ready, INTERFACES_DAY)
        ready = max(ready, float(it.get("notBefore") or 0.0))
        wire = max([end[d] for d in deps if d not in hard] or [0.0])
        if it.get("client") or (not it.get("who") and not choose):
            start[k], end[k] = 0.0, 0.0
            continue
        forbid = forbidden(it)
        who = it.get("who")
        if not who:
            pool = it.get("pool") or "web"
            pts = float(it.get("points") or 0)
            best = None
            owners_be = [be_load[o] for o in backend_owners] or [0]
            skip = set()
            if it.get("peerOf"):
                made = Counter()
                for x in it["peerOf"]:
                    if who_of.get(x):
                        made[who_of[x]] += float(by_key[x].get("points") or 0) or float(by_key[x].get("days") or 0)
                if made:
                    skip.add(made.most_common(1)[0][0])
            # a module test may fall back to the neighbouring stacks when its own has no peer (POS: one developer)
            cands = {}
            for j, pl in enumerate([pool] + [x for x in (it.get("fallback") or ()) if x != pool]):
                for name, r in rank.get(pl, {}).items():
                    cands.setdefault(name, (r, j))
            for name, (r, j) in sorted(cands.items()):
                if name in skip:
                    continue
                cap = (caps.get(pool) or {}).get(name)
                if cap is not None and pts > cap:
                    continue
                if pool == "be" and name in helper_share and \
                        be_load[name] + pts > helper_share[name] * (sum(owners_be) / len(owners_be)):
                    continue
                it_ = dict(it, who=name)
                s, _ = place(busy[name], ready, it_, forbid)
                score = s + (2 if r else 0) + 2 * j
                if pool == "be" and name in backend_owners and svc_owner.get(it.get("service")) not in (None, name):
                    score += 1
                if best is None or score < best[0] - 1e-9:
                    best = (score, name)
            who = best[1] if best else (sorted(set(cands) - skip) or [None])[0]
            if who is None:
                start[k], end[k] = 0.0, 0.0
                continue
        it_ = dict(it, who=who)
        slots = busy.setdefault(who, [])
        s, dur = place(slots, ready, it_, forbid)
        dur_of[k] = dur
        slots.append((s, s + dur))
        slots.sort()
        start[k], end[k], who_of[k] = s, max(s + dur, wire), who
        if it.get("pool") == "be" or it["track"] in ("Backend", "Database"):
            be_load[who] += float(it.get("points") or 0)
    return {k: {"start": start[k], "end": end[k], "who": who_of.get(k), "dur": dur_of.get(k, 0.0)} for k in start}
