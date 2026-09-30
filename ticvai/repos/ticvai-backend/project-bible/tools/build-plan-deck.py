# -*- coding: utf-8 -*-
"""The complete build plan, for the presentation of 30 September 2026: module by module and package by package, in 3-week sprints.

Reads what the package already says -- the Block A task sheet (tasks, points, assignees, weeks),
the screens (points by the same formula as Block A), the contracts (operations), the trace
(requirements per module) and the team -- and writes:

  handoff/build-plan.json                    the plan as data (for the page and the deck)
  handoff/TICVAI - Build Plan.xlsx           the workbook: modules, packages, sprints, Gantt, people
  docs/active/build-plan-presentation.md     slide-by-slide source for the presentation

**Nothing here is estimated by hand.** Block A is the task sheet as scheduled. Block B is sized with
Block A's own formula (screens) and Block A's measured points per operation (back end), and is then
placed on people by a list scheduler over working days, holidays skipped. The pace is Block A's
planned pace, and it is replaced by the measured pace after sprint 1 (23 October).
"""
import csv, datetime as dt, glob, io, json, math, os, re, sys, collections
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.environ.get("PLAN_OUT") or "."
os.chdir(ROOT)

# ---------------------------------------------------------------- calendar
START = dt.date(2026, 10, 5)          # Block A, Monday (decided 29 September)
BLOCK_A_END = dt.date(2026, 11, 20)   # 35 working days
PLAN_END = dt.date(2027, 4, 2)        # end of the six months
HOLIDAYS = {                          # UAE public holidays; Eid dates move with the moon, to be confirmed
    dt.date(2026, 12, 1): "Commemoration Day", dt.date(2026, 12, 2): "National Day",
    dt.date(2026, 12, 3): "National Day", dt.date(2027, 1, 1): "New Year",
    dt.date(2027, 3, 9): "Eid al-Fitr", dt.date(2027, 3, 10): "Eid al-Fitr",
    dt.date(2027, 3, 11): "Eid al-Fitr",
}
HOURS_PER_DAY = 8
PLAN_PACE = 3018 / 35 / 9   # points per developer per working day, Block A as sized on 23 September


def workdays(a, b):
    """Working days from a to b inclusive."""
    d, out = a, []
    while d <= b:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


DAYS = workdays(START, dt.date(2027, 6, 30))       # past the end, so overruns show as overruns
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}

SPRINTS = []
s = START
n = 1
while s <= PLAN_END:
    e = min(s + dt.timedelta(days=18), PLAN_END)   # Monday + 18 days = the third Friday
    SPRINTS.append({"n": n, "name": f"Sprint {n}", "start": s, "end": e, "days": len(workdays(s, e))})
    s += dt.timedelta(days=21)
    n += 1


def sprint_of(d):
    for sp in SPRINTS:
        if sp["start"] <= d <= sp["end"] + dt.timedelta(days=2):
            return sp["n"]
    return SPRINTS[-1]["n"] + 1 + (d - SPRINTS[-1]["end"]).days // 21


# ---------------------------------------------------------------- modules and packages
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
# **One build order from start to end** (30 September, Chinmay): the same service phases as the Block A tickets
# (tools/build-service-docs.py SERVICE_PHASE). 1 Foundation: what everything reads, plus white label and
# platform control, which Block A's storefront and tenant provisioning need. 2 Commerce: the sale path.
# 3 Operations: licensed per module, plugged in after commerce. 4 Engagement: nothing that takes money
# depends on it. 5 Reporting: it reports on everything else. Inside each block window, work runs in this order.
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
PHASE_NAME = {1: "Foundation", 2: "Commerce", 3: "Operations", 4: "Engagement", 5: "Reporting"}


def module_rank(m):
    return (MODULE_PHASE.get(m, 3), MODULES.index(m) if m in MODULES else 99)
MODULES = [m for _, _, ms in PACKAGES for m in ms]
PLATFORM_MODULE = {  # a screen that names no operation belongs to its app's main module
    "P01": "White Label & CMS", "P02": "White Label & CMS", "P04": "Food & Beverage", "P05": "Orders & Reservations",
    "P06": "Workforce & Staff", "P07": "Admission & Access Control", "P08": "Tenancy, Venues & Devices",
    "P09": "Platform Operations", "P10": "Orders & Reservations", "P11": "Accreditation", "P12": "Marketing & CRM",
    "P13": "White Label & CMS", "P14": "Developer Portal & Public API", "P15": "Food & Beverage",
    "P16": "Reporting & Analytics", "P17": "Subscription & Licensing",
}
SCHEMA_CONTRACT = {"pii": "identity", "ledger": "finance", "control": "tenancy", "venuemap": "venue-map",
                   "whitelabel": "white-label", "marketing": "marketing-crm", "subscription": "subscription",
                   "platform": "platform-ops", "baseline": None, "seating": "seating"}

# AI after month 6 (decided 29 September): the configuration assistant, the analytics explainer, anomaly
# detection, trained models. Help me choose (suggestGuidedChoice) and the concierge's chat stay in.
PHASE2_AI_WAS = {"proposeSeatMapChanges", "startConfigurationSession", "listConfigurationSessions",
             "answerConfigurationQuestion", "attachConfigurationSource", "listConfigurationSources",
             "getConfigurationBlueprint", "decideBlueprintRecommendation", "buildConfigurationPlan",
             "explainMetricChange", "configureAnomalyDetector", "listAnomalyDetectors"}
# **Reversed the same evening**: data-driven AI is built now and learns with the tenant's data (Chinmay,
# 29 September: "we still have to build it right, it just gets more accurate with time"). Nothing is deferred.
PHASE2_AI = set()
AI_REVIEW = ["docs/active/ai-functions-review-30-september.json"]
AI_POINTS_PER_WEEK = 48

# ---------------------------------------------------------------- people
# pace = share of Block A's planned per-developer pace; from = first working day on this plan.
PEOPLE = [
    # name, role, pools (first = home), pace, from
    ("Hrushikant Patkar", "Back end and DevOps", ["be"], 1.0, START),
    ("Pranay Shinde", "Back end", ["be"], 1.0, START),
    ("Tanmay Dukhande", "Back end", ["be"], 1.0, START),
    ("Deep Khanvilkar", "Back end", ["be"], 1.0, START),
    ("Pallavi Sawant", "Full stack (Venue Management)", ["web", "be"], 1.0, START),
    ("Sanket Keluskar", "Full stack (Venue Management)", ["web", "be"], 1.0, START),
    ("Chinmay Patkar", "Full stack (guest web, white label)", ["web", "mob", "be"], 1.0, START),
    ("Chitrangi Mestry", "Front end (guest app, web)", ["mob", "web"], 1.0, START),
    ("Pradnya Yeram", "Front end (POS, guest app)", ["pos", "mob", "web"], 1.0, START),
    ("Surendra", "Full stack (Venue Management)", ["web", "be"], 0.6, START),
    ("New full-stack developer 1", "Full stack (to hire)", ["web", "be"], 1.0, dt.date(2026, 11, 23)),
    ("New full-stack developer 2", "Full stack (to hire)", ["web", "be"], 1.0, dt.date(2026, 11, 23)),
    ("Kalpita Mejari", "AI engineer", ["ai"], 1.0, START),
    # **Starts Monday 5 October with Block A** (Chinmay, 30 September). No third AI engineer: every AI function,
    # baseline first and learning per tenant, is finished inside the six months by these two.
    ("Second AI engineer", "AI engineer", ["ai"], 1.0, START),
]
NOT_COUNTED = "Chinmay Parab (lead) is not counted in capacity."


def load_yaml(p):
    return yaml.safe_load(io.open(p, encoding="utf-8")) or {}


def points_of(raw):
    for p, lim in ((1, 2.5), (2, 4.5), (3, 7), (5, 11)):
        if raw <= lim:
            return p
    return 8


def screen_raw(s, offline):
    comps = sum(len(r.get("components") or []) for r in (s.get("layout") or {}).get("regions") or [])
    apis_ = [a for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]
    nav = len((s.get("navigation") or {}).get("transitions") or [])
    return (1 + 0.4 * len(apis_) + min(comps, 30) / 6 + len(s.get("states") or {}) / 4
            + min(nav, 12) / 5 + (1 if offline else 0))


def main():
    # operations
    op_contract = {}
    for f in glob.glob("contracts/*/*.yaml"):
        c = os.path.basename(f)[:-5]
        for it in (load_yaml(f).get("paths") or {}).values():
            for o in (it or {}).values():
                if isinstance(o, dict) and o.get("operationId"):
                    op_contract[o["operationId"]] = c
    op_module = {o: MODULE_OF_CONTRACT.get(c, "Platform Operations") for o, c in op_contract.items()}

    # screens
    screens = {}
    platforms = {}
    for f in sorted(glob.glob("screens/P*.yaml")):
        d = load_yaml(f)
        code, off = d["platform"]["code"], bool(d["platform"].get("offlineCapable"))
        platforms[code] = re.sub(r"\s*[–—-]\s*", " - ", d["platform"]["name"]).replace("�", "-")
        for s in d["screens"]:
            ops = [a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]
            mods = collections.Counter(op_module[o] for o in ops if o in op_module)
            screens[s["id"]] = {"id": s["id"], "platform": code, "title": s.get("title") or s.get("name") or s["id"],
                                "wave": str(s.get("wave")), "ops": ops, "points": points_of(screen_raw(s, off)),
                                "module": mods.most_common(1)[0][0] if mods else PLATFORM_MODULE.get(code, FOUNDATION)}

    # requirements per module (the trace names a contract on each covered row)
    trace = json.load(io.open("handoff/traceability.json", encoding="utf-8"))["rows"]
    req = collections.Counter()
    req_left = collections.Counter()
    for r in trace:
        m = MODULE_OF_CONTRACT.get(r.get("contract") or "")
        if not m:
            continue
        if r.get("verdict") in ("CONTRACTED", "CONTRACTED_PARTIAL"):
            req[m] += 1
        if r.get("verdict") == "CONTRACTED_PARTIAL":
            req_left[m] += 1

    # Block A: the task sheet as scheduled
    tasks = [r for r in csv.DictReader(io.open("handoff/service-docs/tasks.csv", encoding="utf-8")) if r["type"] == "Task"]
    sched = json.load(io.open("handoff/service-docs/block-a-schedule.json", encoding="utf-8"))
    a_ops = set(json.load(io.open("handoff/delivery-slice.json", encoding="utf-8"))["operations"])
    a_backend_pts = sum(int(r["points"] or 0) for r in tasks if r["area"] == "backend")
    per_op = a_backend_pts / max(len(a_ops), 1)
    a_total = sum(int(r["points"] or 0) for r in tasks)
    a_devs = len({r["assignee"] for r in tasks if r["assignee"] and r["area"] not in ("client",)})
    a_days = len(workdays(START, BLOCK_A_END))
    # **The pace is Block A's plan of record, not this sheet divided by 35 days.** Dividing the current sheet
    # by the calendar would make any sheet "fit" by construction and hide the points added since. 3,018
    # points in 35 days for nine developers was what Block A was sized on (23 September).
    pace = PLAN_PACE
    hours_per_point = HOURS_PER_DAY / pace

    a_screens = set()
    a_items = []
    for r in tasks:
        pts = int(r["points"] or 0)
        key = r["key"]
        mod = FOUNDATION
        m = re.search(r"([A-Z]{2,4}-\d{3,4})$", key)
        if key.startswith("APP-") and m and m.group(1) in screens:
            a_screens.add(m.group(1))
            mod = screens[m.group(1)]["module"]
        elif key.startswith("SVC-"):
            ops = re.findall(r"[a-z][A-Za-z0-9]+", (r["description"].split("Operations:", 1)[-1].split("Spec:")[0]
                                                    if "Operations:" in r["description"] else ""))
            mods = collections.Counter(op_module[o] for o in ops if o in op_module)
            if mods:
                mod = mods.most_common(1)[0][0]
        elif key.startswith("MIG-"):
            schema = key[4:].lower()
            c = SCHEMA_CONTRACT.get(schema, schema)
            mod = MODULE_OF_CONTRACT.get(c or "", FOUNDATION)
        a_items.append({"key": key, "subject": r["subject"], "module": mod, "points": pts, "area": r["area"],
                        "tier": int(r.get("tier") or 0), "track": r["track"],
                        "who": r["assignee"] or "client", "week": int(sched["start"].get(key, 0)) // 5,
                        "start": float(sched["start"].get(key, 0)),
                        "seq": int(r["sequence"] or 0)})
    # Each person's Block A tasks, laid end to end at their pace in the order the schedule gives
    # (week first, then the sheet's sequence). A person whose sheet is longer than 35 days runs over;
    # that overrun is the Block A overtime, and it is reported rather than hidden.
    # **Block A's dates are the schedule's** (30 September): each task starts on the day
    # derive-block-a-schedule.py gives it (build order, soft platform waits, and a waiting person taking their
    # next ready ticket), with the same length the schedule uses: points at the person's pace, or the
    # engineer-days an AI engine task names. One source of dates, so the deck and the tickets agree.
    pace_of = {p[0]: p[3] for p in PEOPLE}
    extra = json.load(io.open("docs/active/block-a-extra-tasks.json", encoding="utf-8"))
    days_of = {t["key"]: float(t["days"]) for t in extra["tasks"] if t.get("days")}
    a_cursor = collections.Counter()
    for it in sorted(a_items, key=lambda x: (x["start"], x["seq"])):
        who = it["who"]
        s0 = it["start"]
        if it["key"] in days_of:
            dur = days_of[it["key"]]
        else:
            dur = it["points"] / (pace * pace_of.get(who, 1.0)) if it["points"] else 0.2
        it["s"], it["e"] = s0, s0 + dur
        a_cursor[who] = max(a_cursor[who], s0 + dur)
        it["startIdx"], it["endIdx"] = int(s0), int(max(s0, s0 + dur - 1e-6))

    # Block B: everything else, sized with Block A's formulas
    phase_of_platform = {"P07": "B1", "P05": "B1", "P17": "B1", "P13": "B1", "P10": "B2", "P12": "B2", "P11": "B2",
                         "P14": "B2", "P16": "B3"}
    pool_of_platform = {"P02": "mob", "P06": "mob", "P07": "mob", "P05": "mob", "P04": "pos", "P15": "pos"}

    def b_phase(sc):
        p, w = sc["platform"], sc["wave"]
        if p in phase_of_platform:
            return phase_of_platform[p]
        if p == "P06":
            return "B1" if w in ("1", "2") else "B2"
        if p in ("P08", "P09"):
            return "B1" if w in ("1", "2") else "W3"      # wave 3 is spread over B1-B3 below
        return "B1"

    wps = collections.OrderedDict()

    def add(phase, module, pool, kind, pts, count, what):
        k = (phase, module, pool, kind)
        w = wps.setdefault(k, {"phase": phase, "module": module, "pool": pool, "kind": kind, "points": 0, "count": 0, "what": set()})
        w["points"] += pts
        w["count"] += count
        w["what"].add(what)

    deferred = {"screens": [], "ops": []}
    op_first_phase = {}
    order = {"B1": 1, "B2": 2, "W3": 3, "B3": 4}
    for sid, sc in screens.items():
        if sid in a_screens:
            continue
        if sc["wave"] == "4" or (sc["ops"] and all(o in PHASE2_AI for o in sc["ops"])):
            deferred["screens"].append(sid)
            continue
        ph = b_phase(sc)
        # AI screens and AI endpoints are built by developers like any other module; the AI engineers
        # carry the engine work (Chinmay, 30 September: two AI engineers, done inside six months).
        pool = pool_of_platform.get(sc["platform"], "web")
        add(ph, sc["module"], pool, "screens", sc["points"], 1, platforms[sc["platform"]])
        for o in sc["ops"]:
            if o not in op_first_phase or order[ph] < order[op_first_phase[o]]:
                op_first_phase[o] = ph
    for o, c in op_contract.items():
        if o in a_ops:
            continue
        if o in PHASE2_AI:
            deferred["ops"].append(o)
            continue
        ph = op_first_phase.get(o, "B3")
        add(ph, op_module[o], "be", "operations", per_op, 1, c)

    # AI engine work: models, pipelines, backtests and the baseline-then-learn layer. The per-operation
    # measure prices endpoints, not engines, so the AI review sizes this in AI-engineer weeks per capability.
    ai_review = next((json.load(io.open(pth, encoding="utf-8")) for pth in AI_REVIEW if os.path.exists(pth)), None)
    engine = []
    if ai_review:
        for c in ai_review["capabilities"]:
            b_ = c.get("build") or {}
            m_ = re.search(r"S(\d)", str(c.get("sprint") or ""))
            nb = SPRINTS[int(m_.group(1)) - 1]["start"] if m_ else BLOCK_A_END
            for pool, pts in (("ai", float(b_.get("aiEngineerWeeksTotal") or 0) * AI_POINTS_PER_WEEK),
                              ("be", float(b_.get("backendWeeksExtra") or 0) * AI_POINTS_PER_WEEK)):
                if pts:
                    engine.append({"phase": "B1", "module": "AI & Intelligence", "pool": pool, "kind": "engine",
                                   "points": pts, "count": 0, "what": {c["name"]}, "notBefore": nb})

    # wave 3 of Venue Management and the console: first modules in B1, then B2, the rest B3, in package order
    w3 = [k for k in wps if k[0] == "W3"]
    w3.sort(key=lambda k: module_rank(k[1]))
    total_w3 = sum(wps[k]["points"] for k in w3)
    run = 0
    for k in w3:
        w = wps.pop(k)
        share = run / max(total_w3, 1)
        ph = "B1" if share < 0.22 else ("B2" if share < 0.6 else "B3")
        run += w["points"]
        w["phase"] = ph
        kk = (ph,) + k[1:]
        if kk in wps:
            wps[kk]["points"] += w["points"]; wps[kk]["count"] += w["count"]; wps[kk]["what"] |= w["what"]
        else:
            wps[kk] = w
    # the hardening allowance the plan counts in B3: 5% of Block B
    b_pts = sum(w["points"] for w in wps.values()) + sum(e["points"] for e in engine)

    # ---------------------------------------------------------- the scheduler
    # Block A load per person, in points per day index, from the task sheet
    cursor = {}
    for name, role, pools, pc, frm in PEOPLE:
        cursor[name] = max(DAY_INDEX.get(frm, 0), 0)
    a_load = collections.Counter()
    for it in a_items:
        # Onboarding is an hour on day one, not Block A work; the AI engineers' Block A engine tasks carry no
        # points (their work is sized in the AI review), so neither holds a person back from Block B work.
        if it["area"] not in ("onboard", "ai"):
            a_load[it["who"]] += it["points"]
    # everyone on the Block A sheet is busy until Block A ends; Surendra and the AI engineers start on B work
    # (Surendra's Block A setup screens are part of the task sheet once re-derived)
    a_end_idx = DAY_INDEX[max(d for d in DAYS if d <= BLOCK_A_END)] + 1
    for name, role, pools, pc, frm in PEOPLE:
        if a_load.get(name):
            # Block B starts after Block A for everyone on the Block A sheet, or later if their sheet overruns
            cursor[name] = max(cursor[name], a_end_idx, a_cursor[name])
    # Blocks B1-B3 are date windows the work lands in, not gates: priority order sequences the work.
    phase_start = {}
    people = {p[0]: p for p in PEOPLE}
    pool_members = collections.defaultdict(list)
    for name, role, pools, pc, frm in PEOPLE:
        for i, pl in enumerate(pools):
            pool_members[pl].append((i, name))
    CHUNK = 60   # points: about a week of one person's work; work packages are cut into these
    placed = []
    work = sorted(list(wps.values()) + engine,
                  key=lambda w: (DAY_INDEX.get(w.get("notBefore"), 0) if w.get("notBefore") else 0, order[w["phase"]],
                                 module_rank(w["module"]), w["pool"] == "be"))
    for w in work:
        left = w["points"]
        w["people"] = collections.Counter()
        w["startIdx"], w["endIdx"] = None, None
        while left > 0.01:
            chunk = min(CHUNK, left)
            best = None
            for rank, name in pool_members[w["pool"]]:
                # The AI engineers pull engine work forward as soon as they are free; the review's sprint
                # placement orders their queue but does not hold them idle.
                nb_ = w.get("notBefore") if w["pool"] != "ai" else None
                c = max(cursor[name], phase_start.get(w["phase"], 0),
                        DAY_INDEX[min((d for d in DAYS if d >= nb_), default=DAYS[-1])] if nb_ else 0)
                # a person outside their home pool takes work only when it saves at least two days
                score = c + (2 if rank else 0)
                if best is None or score < best[0]:
                    best = (score, c, name)
            _, c, name = best
            days = chunk / (pace * people[name][3])
            s_idx, e_idx = c, c + days
            cursor[name] = e_idx
            w["people"][name] += chunk
            w["startIdx"] = s_idx if w["startIdx"] is None else min(w["startIdx"], s_idx)
            w["endIdx"] = e_idx if w["endIdx"] is None else max(w["endIdx"], e_idx)
            placed.append({"who": name, "module": w["module"], "phase": w["phase"], "pool": w["pool"], "points": chunk,
                           "s": s_idx, "e": e_idx})
            left -= chunk

    def day(i):
        i = int(math.floor(i))
        return DAYS[min(max(i, 0), len(DAYS) - 1)]

    # ---------------------------------------------------------- roll up
    mods = collections.OrderedDict((m, {"module": m, "package": PACKAGE_OF[m], "requirements": req.get(m, 0),
                                        "requirementsWaiting": req_left.get(m, 0),
                                        "aPoints": 0, "bPoints": 0, "aScreens": 0, "bScreens": 0, "aOps": 0, "bOps": 0,
                                        "people": collections.Counter(), "bars": []}) for m in MODULES)
    for o in op_contract:
        m = mods[op_module[o]]
        if o in a_ops:
            m["aOps"] += 1
        elif o not in PHASE2_AI:
            m["bOps"] += 1
    for sid, sc in screens.items():
        if sid in a_screens:
            mods[sc["module"]]["aScreens"] += 1
        elif sid not in deferred["screens"]:
            mods[sc["module"]]["bScreens"] += 1
    a_span = collections.defaultdict(lambda: [10 ** 9, -1])
    for it in a_items:
        m = mods[it["module"]]
        m["aPoints"] += it["points"]
        if it["who"] != "client":
            m["people"][it["who"]] += it["points"]
        sp = a_span[it["module"]]
        sp[0] = min(sp[0], it["startIdx"]); sp[1] = max(sp[1], it["endIdx"])
    for mname, (s_, e_) in a_span.items():
        if e_ >= 0:
            mods[mname]["bars"].append({"block": "A", "start": day(s_), "end": day(e_)})
    b_span = collections.defaultdict(lambda: [10 ** 9, -1])
    for w in list(wps.values()) + engine:
        m = mods[w["module"]]
        m["bPoints"] += w["points"]
        m["people"].update(w["people"])
        sp = b_span[w["module"]]
        sp[0] = min(sp[0], w["startIdx"]); sp[1] = max(sp[1], w["endIdx"])
    for mname, (s_, e_) in b_span.items():
        if e_ >= 0:
            mods[mname]["bars"].append({"block": "B", "start": day(s_), "end": day(e_)})
    for m in mods.values():
        m["points"] = round(m["aPoints"] + m["bPoints"])
        m["hours"] = round(m["points"] * hours_per_point)
        m["aHours"] = round(m["aPoints"] * hours_per_point)
        m["bHours"] = round(m["bPoints"] * hours_per_point)
        ends = [b["end"] for b in m["bars"]]
        starts = [b["start"] for b in m["bars"]]
        m["start"] = min(starts) if starts else None
        m["end"] = max(ends) if ends else None
        m["sprints"] = f"{sprint_of(m['start'])}-{sprint_of(m['end'])}" if starts else ""
        top = m["people"].most_common()
        m["lead"] = top[0][0] if top else ""
        m["team"] = [n for n, _ in top[:6]]
        m["aPoints"] = round(m["aPoints"]); m["bPoints"] = round(m["bPoints"])

    pk = []
    for name, why, ms in PACKAGES:
        rows = [mods[m] for m in ms]
        starts = [r["start"] for r in rows if r["start"]]
        ends = [r["end"] for r in rows if r["end"]]
        ppl = collections.Counter()
        for r in rows:
            ppl.update(r["people"])
        pk.append({"package": name, "why": why, "modules": ms, "points": sum(r["points"] for r in rows),
                   "hours": sum(r["hours"] for r in rows), "aHours": sum(r["aHours"] for r in rows),
                   "bHours": sum(r["bHours"] for r in rows), "requirements": sum(r["requirements"] for r in rows),
                   "screens": sum(r["aScreens"] + r["bScreens"] for r in rows), "ops": sum(r["aOps"] + r["bOps"] for r in rows),
                   "start": min(starts) if starts else None, "end": max(ends) if ends else None,
                   "lead": ppl.most_common(1)[0][0] if ppl else "", "team": [n for n, _ in ppl.most_common(8)]})

    # per person per sprint, hours
    load = collections.defaultdict(lambda: collections.Counter())
    for it in a_items:
        if it["who"] == "client":
            continue
        for i in range(it["startIdx"], it["endIdx"] + 1):
            load[it["who"]][sprint_of(day(i))] += it["points"] / (it["endIdx"] - it["startIdx"] + 1) * hours_per_point
    for p in placed:
        s_, e_ = p["s"], p["e"]
        span = max(e_ - s_, 1e-6)
        i = s_
        while i < e_:
            j = min(math.floor(i) + 1, e_)
            load[p["who"]][sprint_of(day(i))] += p["points"] * (j - i) / span * hours_per_point
            i = j
    people_rows = []
    for name, role, pools, pc, frm in PEOPLE:
        cap = {sp["n"]: len([d for d in workdays(max(sp["start"], frm), sp["end"])]) * HOURS_PER_DAY * pc for sp in SPRINTS}
        people_rows.append({"name": name, "role": role, "pace": pc, "from": frm, "capacity": cap,
                            "planned": {k: round(v) for k, v in load[name].items()},
                            "modules": [m for m, r in mods.items() if name in r["people"]][:8],
                            "lastDay": day(cursor[name]) if cursor[name] else None,
                            "blockAPoints": a_load.get(name, 0),
                            "hoursAfterPlanEnd": round(sum(v for k, v in load[name].items() if int(k) > len(SPRINTS))
                                                       + max(0.0, cursor[name] - DAY_INDEX[max(d for d in DAYS if d <= PLAN_END)] - 1)
                                                       * 0),
                            "overtimeHoursPerWeek": round(max(0.0, cursor[name] - DAY_INDEX[max(d for d in DAYS if d <= PLAN_END)] - 1)
                                                          * HOURS_PER_DAY * pc / max(1, (len([d for d in DAYS if frm <= d <= PLAN_END]) / 5)), 1),
                            "blockAEnd": day(a_cursor[name]) if a_cursor.get(name) else None,
                            "blockAOvertimeHours": round(max(0.0, a_cursor.get(name, 0) - a_days) * HOURS_PER_DAY * pc)})
    finish = max(day(p["e"]) for p in placed) if placed else BLOCK_A_END

    sprints = []
    for sp in SPRINTS:
        a_h = sum(it["points"] * hours_per_point for it in a_items if it["who"] != "client"
                  and sprint_of(day(it["startIdx"])) == sp["n"])
        sprints.append(dict(sp, capacity=round(sum(r["capacity"][sp["n"]] for r in people_rows)),
                            planned=round(sum(r["planned"].get(sp["n"], 0) for r in people_rows)),
                            modules=sorted({p["module"] for p in placed if sprint_of(day(p["s"])) == sp["n"]}
                                           | {it["module"] for it in a_items if sprint_of(day(it["startIdx"])) == sp["n"]},
                                           key=lambda m: MODULES.index(m) if m in MODULES else 99),
                            blocks=("A" if sp["start"] <= BLOCK_A_END else "") + ("B" if sp["end"] > BLOCK_A_END else "")))

    # **The build phases, end to end** (30 September): the same phases in Block A (the tickets' tier) and in
    # B1 to B3 (the module's phase), split into back end and front end, so one table reads from 5 October to
    # the last day of planned work.
    BACK = ("Backend", "Database", "DevOps", "Setup", "AI")
    ph_rows = collections.OrderedDict()
    for ph in range(0, 6):
        for side in ("back end", "front end"):
            ph_rows[(ph, side)] = {"phase": ph, "name": "Plumbing" if ph == 0 else PHASE_NAME[ph], "side": side,
                                   "points": 0.0, "s": None, "e": None, "modules": collections.Counter(),
                                   "people": collections.Counter(), "aPoints": 0.0, "bPoints": 0.0}

    def put(ph, side, module, who, pts, s_, e_, blk):
        r = ph_rows[(ph, side)]
        r["points"] += pts
        r["aPoints" if blk == "A" else "bPoints"] += pts
        r["s"] = s_ if r["s"] is None else min(r["s"], s_)
        r["e"] = e_ if r["e"] is None else max(r["e"], e_)
        r["modules"][module] += pts
        if who and who != "client":
            r["people"][who] += pts

    for it in a_items:
        if it["area"] == "onboard":
            continue
        side = "back end" if it["track"] in BACK else "front end"
        put(it["tier"], side, it["module"], it["who"], it["points"], it["startIdx"], it["endIdx"], "A")
    for p in placed:
        side = "back end" if p.get("pool") in ("be", "ai") else "front end"
        put(MODULE_PHASE.get(p["module"], 3), side, p["module"], p["who"], p["points"], p["s"], p["e"], "B")
    phases = []
    for (ph, side), r in ph_rows.items():
        if not r["points"]:
            continue
        phases.append({"phase": ph, "name": r["name"], "side": side, "hours": round(r["points"] * hours_per_point),
                       "aHours": round(r["aPoints"] * hours_per_point), "bHours": round(r["bPoints"] * hours_per_point),
                       "start": day(r["s"]).isoformat(), "end": day(r["e"]).isoformat(),
                       "modules": [m for m, _ in r["modules"].most_common(8)],
                       "people": [n for n, _ in r["people"].most_common(6)]})

    out = {
        "phases": phases,
        "generatedBy": "tools/build-plan-deck.py", "generated": dt.date.today().isoformat(),
        "basis": {"blockATaskPoints": a_total, "blockADevelopers": a_devs, "blockADays": a_days,
                  "pacePointsPerDeveloperDay": round(pace, 2), "hoursPerPoint": round(hours_per_point, 3),
                  "pointsPerOperation": round(per_op, 2), "blockBPoints": round(b_pts),
                  "totalPoints": round(a_total + b_pts), "totalHours": round((a_total + b_pts) * hours_per_point),
                  "forecastFinish": finish.isoformat(), "planEnd": PLAN_END.isoformat(),
                  "notCounted": NOT_COUNTED},
        "calendar": {"start": START.isoformat(), "blockAEnd": BLOCK_A_END.isoformat(), "planEnd": PLAN_END.isoformat(),
                     "holidays": {d.isoformat(): n for d, n in HOLIDAYS.items()}},
        "sprints": sprints, "packages": pk, "modules": list(mods.values()), "people": people_rows,
        "aiEngine": {"points": round(sum(e["points"] for e in engine)), "source": next((p_ for p_ in AI_REVIEW if os.path.exists(p_)), None)},
        "deferred": {"screens": len(deferred["screens"]), "operations": len(deferred["ops"]),
                     "aiOperations": sorted(o for o in deferred["ops"] if o in PHASE2_AI)},
        "platforms": platforms,
    }
    return out


def jsonable(o):
    if isinstance(o, (dt.date,)):
        return o.isoformat()
    if isinstance(o, collections.Counter):
        return dict(o)
    if isinstance(o, set):
        return sorted(o)
    raise TypeError(type(o))


# ---------------------------------------------------------------- outputs
def _d(x):
    if not x:
        return ""
    if isinstance(x, str):
        x = dt.date.fromisoformat(x)
    return x.strftime("%d %b %Y").lstrip("0")


def _pp(n):
    return f"{int(round(n)):,}"


def write_xlsx(plan, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    HEAD = PatternFill("solid", fgColor="1F3864")
    SUB = PatternFill("solid", fgColor="D9E1F2")
    A = PatternFill("solid", fgColor="2E75B6")
    B = PatternFill("solid", fgColor="70AD47")
    OVER = PatternFill("solid", fgColor="F4B084")
    HOL = PatternFill("solid", fgColor="E7E6E6")
    WHITE = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="BFBFBF")
    wb = Workbook()

    def sheet(title, header, rows, widths=None, first=False):
        ws = wb.active if first else wb.create_sheet()
        ws.title = title
        ws.append(header)
        for c in ws[1]:
            c.fill, c.font = HEAD, WHITE
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows:
            ws.append(r)
        for i, w in enumerate(widths or [], 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A2"
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        return ws

    b = plan["basis"]
    ws = sheet("Summary", ["What", "Value", "How it is worked out"], [
        ["Start", _d(plan["calendar"]["start"]), "Block A starts Monday 5 October 2026 (decided 29 September)."],
        ["Block A ends", _d(plan["calendar"]["blockAEnd"]), "35 working days: POS with Kitchen Display, Guest Web, Guest App, white label, Venue Management setup, AI that needs no history."],
        ["End of the six months", _d(plan["calendar"]["planEnd"]), "Blocks B1, B2 and B3 run from 23 November to 2 April."],
        ["Forecast finish", _d(b["forecastFinish"]), "Where the scheduler places the last piece of work, with the team and pace below."],
        ["Sprints", f"{len(plan['sprints'])} sprints of 3 weeks", "The last sprint is 2 weeks, ending on 2 April."],
        ["Total effort", f"{_pp(b['totalPoints'])} points = {_pp(b['totalHours'])} hours", "Block A from its task sheet; Block B sized with Block A's formulas."],
        ["Block A", f"{_pp(b['blockATaskPoints'])} points = {_pp(b['blockATaskPoints'] * b['hoursPerPoint'])} hours", "The Block A task sheet as it stands."],
        ["Block B", f"{_pp(b['blockBPoints'])} points = {_pp(b['blockBPoints'] * b['hoursPerPoint'])} hours", "Screens by the Block A formula; back end at Block A's points per operation."],
        ["Pace", f"{b['pacePointsPerDeveloperDay']} points per developer per day", "Block A's plan of record: 3,018 points, 35 days, 9 developers. Replaced by the measured pace on 23 October."],
        ["Hours per point", f"{b['hoursPerPoint']}", "8 hours a day divided by the pace."],
        ["Points per back-end operation", f"{b['pointsPerOperation']}", "Block A's back-end points divided by its operations."],
        ["Team", f"{len(plan['people'])} people", b["notCounted"]],
        ["After month 6", f"{plan['deferred']['screens']} screens", "Only the wave-4 screens still marked deferred. Every AI function is built inside the six months (30 September); a trained model goes live per tenant after a season of its data."],
        ["Overtime to finish by 2 April", f"{_pp(sum(p_.get('hoursAfterPlanEnd', 0) for p_ in plan['people']))} hours", "Work each person has past 2 April at normal hours; see People for hours per week."],
    ], [26, 34, 100], first=True)

    rows = []
    for sp in plan["sprints"]:
        hol = [f"{_d(d)} {n}" for d, n in plan["calendar"]["holidays"].items() if sp["start"] <= d <= sp["end"]]
        rows.append([sp["name"], _d(sp["start"]), _d(sp["end"]), sp["days"], "Block A" if sp["blocks"] == "A" else ("Block A ends, B1 starts" if sp["blocks"] == "AB" else "Block B"),
                     sp["capacity"], sp["planned"], f"{sp['planned'] / max(sp['capacity'], 1):.0%}", "; ".join(hol), ", ".join(sp["modules"][:14])])
    sheet("Sprints", ["Sprint", "Starts", "Ends", "Working days", "Block", "Capacity (hours)", "Planned (hours)", "Used", "Holidays", "Modules worked on"],
          rows, [10, 13, 13, 9, 22, 11, 11, 8, 30, 90])

    rows = []
    for p in plan["packages"]:
        rows.append([p["package"], p["why"], len(p["modules"]), p["requirements"], p["screens"], p["ops"], p["points"], p["hours"],
                     p["aHours"], p["bHours"], _d(p["start"]), _d(p["end"]), p["lead"], ", ".join(p["team"])])
    sheet("Packages", ["Package", "What it is", "Modules", "Requirements covered", "Screens", "Operations", "Points", "Hours",
                       "Block A hours", "Block B hours", "Starts", "Expected completion", "Lead", "Team"], rows,
          [26, 60, 8, 12, 9, 10, 9, 9, 10, 10, 13, 13, 22, 70])

    rows = []
    for m in plan["modules"]:
        rows.append([m["package"], m["module"], m["requirements"], m["requirementsWaiting"], m["aScreens"], m["bScreens"], m["aOps"], m["bOps"],
                     m["aHours"], m["bHours"], m["hours"], _d(m["start"]), _d(m["end"]), m["sprints"], m["lead"], ", ".join(m["team"])])
    sheet("Modules", ["Package", "Module", "Requirements covered", "Waiting on the client", "Screens in A", "Screens in B", "Operations in A",
                      "Operations in B", "Block A hours", "Block B hours", "Total hours", "Starts", "Expected completion", "Sprints", "Lead", "Team"],
          rows, [24, 32, 11, 10, 8, 8, 10, 10, 10, 10, 10, 13, 13, 9, 22, 70])

    rows = [[f"{r['phase']} {r['name']}", r["side"], _d(r["start"]), _d(r["end"]), r["aHours"], r["bHours"],
             r["hours"], ", ".join(r["modules"]), ", ".join(r["people"])] for r in plan["phases"]]
    sheet("Build phases", ["Phase", "Side", "Starts", "Ends", "Block A hours", "Block B hours", "Hours",
                           "Main modules", "People"], rows, [16, 10, 13, 13, 11, 11, 9, 80, 60])

    # Gantt: one row per package then its modules, one column per week
    ws = wb.create_sheet("Gantt")
    weeks = []
    d = dt.date.fromisoformat(plan["calendar"]["start"]) if isinstance(plan["calendar"]["start"], str) else plan["calendar"]["start"]
    end = max(dt.date.fromisoformat(b["forecastFinish"]), dt.date.fromisoformat(plan["calendar"]["planEnd"]))
    while d <= end:
        weeks.append(d)
        d += dt.timedelta(days=7)
    fixed = ["Package / module", "Lead", "Hours", "Completion"]
    ws.append(fixed + [""] * len(weeks))
    ws.append(["", "", "", ""] + [w.strftime("%d %b") for w in weeks])
    for i, w in enumerate(weeks):
        sp = next((s for s in plan["sprints"] if s["start"] <= w.isoformat() <= s["end"]), None)
        c = ws.cell(row=1, column=5 + i, value=(f"S{sp['n']}" if sp and sp["start"] == w.isoformat() else ""))
    for c in ws[1] + ws[2]:
        c.fill, c.font = HEAD, WHITE
        c.alignment = Alignment(horizontal="center", text_rotation=90 if c.row == 2 and c.column > 4 else 0)
    r = 3
    mods = {m["module"]: m for m in plan["modules"]}
    plan_end = dt.date.fromisoformat(plan["calendar"]["planEnd"])

    def bar(row, bars):
        for bb in bars:
            s0, e0 = dt.date.fromisoformat(bb["start"]), dt.date.fromisoformat(bb["end"])
            for i, w in enumerate(weeks):
                if w <= e0 and w + dt.timedelta(days=4) >= s0:
                    c = ws.cell(row=row, column=5 + i)
                    c.fill = OVER if w > plan_end else (A if bb["block"] == "A" else B)
                    c.border = Border(top=thin, bottom=thin)
    for p in plan["packages"]:
        ws.cell(row=r, column=1, value=p["package"]).font = Font(bold=True)
        ws.cell(row=r, column=2, value=p["lead"]); ws.cell(row=r, column=3, value=p["hours"]); ws.cell(row=r, column=4, value=_d(p["end"]))
        for c in range(1, 5 + len(weeks)):
            ws.cell(row=r, column=c).fill = SUB
        bar(r, [bb for mm in p["modules"] for bb in mods[mm]["bars"]])
        r += 1
        for mm in p["modules"]:
            m = mods[mm]
            if not m["hours"]:
                continue
            ws.cell(row=r, column=1, value="   " + mm); ws.cell(row=r, column=2, value=m["lead"])
            ws.cell(row=r, column=3, value=m["hours"]); ws.cell(row=r, column=4, value=_d(m["end"]))
            bar(r, m["bars"])
            r += 1
    r += 1
    for fill, text in ((A, "Block A (task sheet)"), (B, "Block B (scheduled)"), (OVER, "After 2 April")):
        ws.cell(row=r, column=1, value=text); ws.cell(row=r, column=2).fill = fill; r += 1
    ws.column_dimensions["A"].width = 36; ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 8; ws.column_dimensions["D"].width = 12
    for i in range(len(weeks)):
        ws.column_dimensions[get_column_letter(5 + i)].width = 3.2
    ws.freeze_panes = "E3"

    rows = []
    for pe in plan["people"]:
        rows.append([pe["name"], pe["role"], f"{pe['pace']:.0%}", _d(pe["from"]), pe["blockAPoints"], _d(pe["blockAEnd"]),
                     pe["blockAOvertimeHours"]] + [pe["planned"].get(str(s["n"]), pe["planned"].get(s["n"], 0)) for s in plan["sprints"]]
                    + [_d(pe["lastDay"]), pe.get("hoursAfterPlanEnd", 0), pe.get("overtimeHoursPerWeek", 0), ", ".join(pe["modules"])])
    ws = sheet("People", ["Name", "Role", "Pace", "From", "Block A points", "Block A work ends", "Block A hours past 20 Nov"]
               + [s["name"] + " hours" for s in plan["sprints"]] + ["Last day at normal hours", "Hours past 2 Apr", "Overtime h/week to finish", "Modules"], rows,
               [26, 30, 7, 12, 9, 13, 11] + [8] * len(plan["sprints"]) + [13, 10, 11, 80])
    for row in ws.iter_rows(min_row=2):
        for i, s in enumerate(plan["sprints"]):
            c = row[7 + i]
            cap = 15 * 8 if s["days"] >= 15 else s["days"] * 8
            if isinstance(c.value, (int, float)) and c.value > cap * 1.02:
                c.fill = OVER

    sheet("Release checklist", ["When", "Step", "Check", "Owner"], [[a, b_, c, d_] for a, b_, c, d_ in RELEASE_CHECKLIST], [22, 14, 90, 22])
    sheet("Decisions", ["Decision", "Status", "What was decided", "Why", "What it costs"], [list(x) for x in ARCH_DECISIONS], [34, 10, 60, 60, 50])
    sheet("Risks", ["Risk", "Signal", "What we do"], [list(x) for x in RISKS], [40, 50, 70])
    wb.save(path)


RELEASE_CHECKLIST = [
    ("Every sprint (Friday of week 3)", "Before", "Every ticket in the sprint is Ready for QA or moved to the next sprint with a reason in the ticket.", "Scrum lead"),
    ("Every sprint", "Before", "CI green on main: unit, contract (the OpenAPI checks) and migration tests.", "Hrushikant Patkar"),
    ("Every sprint", "Before", "Database migrations run forward on a copy of staging data; the rollback script runs back cleanly.", "Back-end owner of the service"),
    ("Every sprint", "Before", "Feature flags set per tenant for anything half-built; nothing unfinished is visible to a venue.", "Lead of the package"),
    ("Every sprint", "Deploy", "Deploy to staging; run the smoke flows of the apps touched (buy a ticket, pay, scan, POS sale, KDS bump).", "QA"),
    ("Every sprint", "Deploy", "Demo to the client from staging; record accepted and rejected items in OpenProject.", "Chinmay Parab"),
    ("Every sprint", "After", "Measured pace per person recorded; the plan workbook regenerated with the real pace.", "Chinmay Parab"),
    ("Block A go-live (20 Nov 2026)", "Before", "The client has signed off every Block A wireframe batch (3 working days each, audit R252).", "Client design reviewer"),
    ("Block A go-live", "Before", "Payment sandbox credentials in place and a full sale-refund-settlement cycle passes (the client's answer in the Decisions Register).", "Client, then Tanmay Dukhande"),
    ("Block A go-live", "Before", "Offline: the POS sells and the scanner admits with the network cut, and reconcile when it returns.", "Pradnya Yeram"),
    ("Block A go-live", "Before", "Tax invoice, credit note and VAT fields checked against the client's answers (make-or-break items).", "Pranay Shinde"),
    ("Block A go-live", "Before", "Load test at the burst mix (ticket on-sale) and the venue-day mix; replicas as sized in handoff/sizing.json.", "Hrushikant Patkar"),
    ("Block A go-live", "Before", "Backups restore into a clean environment; the restore time is written down.", "Hrushikant Patkar"),
    ("Block A go-live", "Before", "Security: role grants reviewed per module, secrets in the vault, no test credentials in production.", "Hrushikant Patkar"),
    ("Block A go-live", "Deploy", "Production deploy in a quiet window; canary tenant first, then the pilot venue.", "Hrushikant Patkar"),
    ("Block A go-live", "Deploy", "Watch error rate and latency for the first hour of trading; the rollback is rehearsed beforehand.", "On-call back end"),
    ("Block A go-live", "Rollback if", "Payment failures above 2% of attempts, POS sale p95 above 2 seconds, or any failed gate admission not explained by the ticket.", "Chinmay Parab decides"),
    ("Block A go-live", "After", "Release notes to the client; tickets closed; the hypercare rota for the first two weeks.", "Chinmay Parab"),
    ("End of six months (2 Apr 2027)", "Before", "Every module's acceptance signed; open defects triaged into the phase-2 backlog.", "Chinmay Parab and the client"),
]

ARCH_DECISIONS = [
    ("One package, services by contract", "Accepted", "Each business module is one OpenAPI contract owned by one service; screens bind to operations, never to tables.",
     "Work can be split by module and checked by machine (34 checkers) before anyone builds.", "A change crosses contract, screen and ticket; the refresh keeps them in step."),
    ("Build in two blocks", "Accepted", "Block A ships the selling apps first (POS, KDS, guest web and app, white label, Venue Management setup); Block B the back office, console, partner, support and analytics.",
     "Revenue-facing apps reach the client in 7 weeks; the long tail of back-office screens follows.", "Back-office screens wait until B1-B3."),
    ("Size by formula, schedule by measured pace", "Accepted", "Points come from each screen's specification and each operation; the pace is replaced by the measured pace after sprint 1.",
     "No hand estimates; a re-plan is a rerun.", "The first forecast is only as good as Block A's planned pace until 23 October."),
    ("AI that needs no history in Block A", "Accepted", "Gateway and governance, concierge, Help me choose, translations and the planner agent ship in Block A; rules stand in for upsell and fraud.",
     "Guests get AI from day one without waiting for data.", "Data-driven AI is scheduled in Block B; see the AI review."),
    ("Every AI function inside six months, baseline first", "Accepted 30 Sep", "Forecasting, fraud, recommendations, anomaly detection and both assistants ship with a working baseline on day one and learn from the tenant's own data; a trained model replaces the baseline only when it beats it and an admin approves.",
     "Customers never hear 'later, when you have data'; accuracy grows with use.", "About 2,800 points of AI engine work; a trained model goes live per tenant only after a season of its data."),
    ("Two AI engineers from 5 October", "Accepted 30 Sep", "Kalpita and the second AI engineer carry the engine work from Block A onwards; no third engineer. Developers build the AI endpoints and screens like any other module.",
     "AI engineers spend their time on what only they can build.", "The AI engineers are fully loaded; about 3-4 overtime hours a week each."),
    ("CMS as a flow builder", "Accepted", "Operators pick their booking flows, see required and optional steps, set their own order, then finish in a configuration panel.",
     "One engine serves every venue type the prototypes show.", "The step library has to be complete before operators can compose."),
    ("Per-tenant data and models", "Accepted", "Models train per tenant; the LLM never reads raw data (scrubbed aggregates or code it writes); retention is tenant configuration.",
     "Meets PDPL and client expectations on data isolation.", "No pooled training; cold start relies on baselines and priors."),
    ("Load follows skill", "Accepted", "Tasks are assigned by skill rating and experience, not evenly; helpers take a share proportional to their ratings.",
     "Hard work goes to people rated for it.", "Back-end owners are the Block A constraint; shown as overtime, not hidden."),
]

RISKS = [
    ("Back-end owners overloaded in Block A", "Their Block A work runs past 20 November (People sheet).", "Deep takes a larger proportional share; the two new developers take back-end tasks from their first day; Block B start slides for the three owners only."),
    ("Pace below plan", "Measured pace on 23 October under 9.6 points per developer per day.", "Rerun the plan with the measured pace; use the wave-3 deferral list on 18 December."),
    ("Hiring the two developers slips", "Not confirmed by 23 October.", "Block B finish moves out by the scheduler's figure; the PM decides scope or date."),
    ("Client inputs late", "Wireframe sign-off over 3 working days; sandbox credentials; stations and fares; cabana numbering; real photos.", "Those tickets wait in 'Waiting on client' and do not count against the team's pace."),
    ("Make-or-break answers", "Tax invoice fields, e-invoicing provider, VAT 201 layout, face capture consent, ID-verification provider.", "Defaults are built; a different answer is a change request."),
    ("Second AI engineer not in place on 5 October", "No start date confirmed this week.", "Kalpita starts the Block A AI alone; the baseline layer moves one sprint and the AI engine work needs more overtime."),
    ("AI engine estimates are rough", "The AI review sized the engines in engineer-weeks from the design.", "Re-base on the measured pace on 23 October; the trained models are the part to move if the AI engineers fall behind."),
]


def write_md(plan, path):
    b = plan["basis"]
    L = []
    w = L.append
    w("# TICVAI complete build plan: presentation source")
    w("")
    w(f"> **For:** the build-plan presentation on 30 September 2026. **Generated by** `tools/build-plan-deck.py` from the package; rerun it after any change. The workbook with every table and the Gantt is `handoff/TICVAI - Build Plan.xlsx`.")
    w("")
    w("Each `##` below is one slide. Numbers come from the package, not from estimates.")
    w("")
    w("## 1. The plan in one line")
    w("")
    w(f"We build TICVAI from **{_d(plan['calendar']['start'])} to {_d(plan['calendar']['planEnd'])}** in **{len(plan['sprints'])} three-week sprints**: "
      f"about **{_pp(b['totalHours'])} hours** of development across **{len(plan['modules'])} modules** in **{len(plan['packages'])} packages**, "
      f"with a team of {len(plan['people'])}. The forecast finish is **{_d(b['forecastFinish'])}**.")
    w("")
    w("## 2. How the plan is measured")
    w("")
    w("- **Points** come from each screen's specification (operations, components, states, navigation, offline) and from each back-end operation.")
    w(f"- **Pace** is Block A's plan of record: {b['pacePointsPerDeveloperDay']} points per developer per day, so one point is about {b['hoursPerPoint']:.2f} hours.")
    w("- **Hours** are points times that figure. After sprint 1 (23 October) the measured pace replaces it and the plan is regenerated.")
    w("- **Names** come from the task sheet for Block A, and from the scheduler for Block B, which places work on people by skill.")
    w("")
    w("## 3. Sprints")
    w("")
    w("| Sprint | Dates | Block | Capacity (h) | Planned (h) |")
    w("|---|---|---|---|---|")
    for sp in plan["sprints"]:
        blk = {"A": "A", "AB": "A ends 20 Nov, B1 starts", "B": "B"}[sp["blocks"]]
        w(f"| {sp['n']} | {_d(sp['start'])} – {_d(sp['end'])} | {blk} | {_pp(sp['capacity'])} | {_pp(sp['planned'])} |")
    w("")
    w("Holidays counted: " + "; ".join(f"{_d(d)} {n}" for d, n in plan["calendar"]["holidays"].items()) + ". Eid dates are to be confirmed.")
    w("")
    w("## 4. Packages")
    w("")
    w("| Package | Modules | Requirements | Screens | Operations | Hours | Completion | Lead |")
    w("|---|---|---|---|---|---|---|---|")
    for p in plan["packages"]:
        w(f"| **{p['package']}** | {len(p['modules'])} | {_pp(p['requirements'])} | {_pp(p['screens'])} | {_pp(p['ops'])} | {_pp(p['hours'])} | {_d(p['end'])} | {p['lead']} |")
    w("")
    w("## 5. Gantt by package")
    w("")
    w("```mermaid")
    w("gantt")
    w("  dateFormat YYYY-MM-DD")
    w("  axisFormat %d %b")
    w("  title TICVAI build, 5 Oct 2026 to 2 Apr 2027")
    for p in plan["packages"]:
        w(f"  section {p['package']}")
        mods = {m["module"]: m for m in plan["modules"]}
        for mm in p["modules"]:
            m = mods[mm]
            for i, bb in enumerate(m["bars"]):
                tag = "active, " if bb["block"] == "A" else ""
                w(f"  {mm} ({bb['block']}) :{tag}{bb['start']}, {bb['end']}")
    w("```")
    w("")
    w("## 6. Build phases, end to end")
    w("")
    w("One order from 5 October to the end: plumbing, then the foundation everything reads, the sale path, the "
      "per-module operations, engagement, and reporting last. Block A takes it from the tickets (each ticket's phase), "
      "B1 to B3 from each module's phase. A screen is built against the mock server and connected as its services land.")
    w("")
    for side in ("back end", "front end"):
        w(f"**{side.capitalize()}**")
        w("")
        w("| Phase | Starts | Ends | Hours (A / B) | Main modules | People |")
        w("|---|---|---|---|---|---|")
        for r in plan["phases"]:
            if r["side"] != side:
                continue
            w(f"| {r['phase']} {r['name']} | {_d(r['start'])} | {_d(r['end'])} | {_pp(r['aHours'])} / {_pp(r['bHours'])} | "
              f"{', '.join(r['modules'][:5])} | {', '.join(r['people'][:4])} |")
        w("")
    mods = {m["module"]: m for m in plan["modules"]}
    for n, p in enumerate(plan["packages"], 7):
        w(f"## {n}. {p['package']}")
        w("")
        w(p["why"])
        w("")
        w("| Module | Requirements | Screens A / B | Operations A / B | Hours A / B | Sprints | Completion | Lead | Team |")
        w("|---|---|---|---|---|---|---|---|---|")
        for mm in p["modules"]:
            m = mods[mm]
            if not m["hours"]:
                continue
            w(f"| {mm} | {m['requirements']} | {m['aScreens']} / {m['bScreens']} | {m['aOps']} / {m['bOps']} | {_pp(m['aHours'])} / {_pp(m['bHours'])} | "
              f"{m['sprints']} | {_d(m['end'])} | {m['lead']} | {', '.join(m['team'][:4])} |")
        w("")
    n = 7 + len(plan["packages"])
    w(f"## {n}. The team")
    w("")
    w("| Name | Role | Block A points | Block A work ends | Last day of planned work |")
    w("|---|---|---|---|---|")
    for pe in plan["people"]:
        w(f"| {pe['name']} | {pe['role']} | {pe['blockAPoints'] or '–'} | {_d(pe['blockAEnd']) or '–'} | {_d(pe['lastDay'])} |")
    w("")
    w(b["notCounted"] + " Loads are uneven on purpose: they follow skill and experience.")
    w("")
    n += 1
    w(f"## {n}. AI: built now, more accurate with time")
    w("")
    w("- **Every AI function ships inside the six months** (decided 30 September): forecasting, staffing, suggestions, wait times, anomaly detection, fraud and risk, recommendations, marketing AI, pricing suggestions, the configuration assistant, the analytics assistant, seat-map generation, translations and the planner agent.")
    w("- **Day one works with no history:** a venue profile entered at onboarding, a starting pattern for the venue type, the UAE calendar and weather, and the venue's own imported history.")
    w("- **Stages a venue sees:** Starting (day one) → Learning (about 4 weeks) → Established (about 3 months) → a trained model, promoted by an admin when it beats the current answer (after about a season).")
    w("- **Team:** Kalpita and the second AI engineer from 5 October. No third engineer. Developers build the AI endpoints and screens.")
    w(f"- **Size:** about {_pp(plan.get('aiEngine', {}).get('points', 0) * b['hoursPerPoint'])} hours of AI engine work on top of the endpoints and screens.")
    w("")
    n += 1
    w(f"## {n}. Finishing by 2 April: overtime")
    w("")
    w("| Name | Last day at normal hours | Hours past 2 April | Overtime per week to finish on time |")
    w("|---|---|---|---|")
    tot = 0
    for pe in plan["people"]:
        tot += pe.get("hoursAfterPlanEnd", 0)
        w(f"| {pe['name']} | {_d(pe['lastDay'])} | {pe.get('hoursAfterPlanEnd', 0)} | {pe.get('overtimeHoursPerWeek', 0)} |")
    w("")
    w(f"In total about {_pp(tot)} hours past 2 April at normal hours, spread as overtime across the build. Rerun after the measured pace on 23 October.")
    w("")
    n += 1
    w(f"## {n}. Architecture decisions the plan rests on")
    w("")
    for x in ARCH_DECISIONS:
        w(f"- **{x[0]}** ({x[1]}). {x[2]}")
    w("")
    n += 1
    w(f"## {n}. Release checklist")
    w("")
    cur = None
    for when, step, check, owner in RELEASE_CHECKLIST:
        if when != cur:
            w(f"**{when}**")
            w("")
            cur = when
        w(f"- [ ] *{step}:* {check} ({owner})")
    w("")
    n += 1
    w(f"## {n}. Risks and checkpoints")
    w("")
    for r_ in RISKS:
        w(f"- **{r_[0]}.** Signal: {r_[1]} Action: {r_[2]}")
    w("")
    w("Checkpoints: 23 October (measured pace, hiring confirmed), 20 November (Block A done), 18 December (deferral decision, only if needed), 2 April 2027 (end of six months).")
    w("")
    io.open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    plan = json.loads(json.dumps(main(), default=jsonable, ensure_ascii=False))
    def o(rel):
        return os.path.join(OUT, rel) if OUT != "." else rel
    io.open(o("handoff/build-plan.json"), "w", encoding="utf-8").write(json.dumps(plan, indent=1, ensure_ascii=False))
    write_xlsx(plan, o("handoff/TICVAI - Build Plan.xlsx"))
    write_md(plan, o("docs/active/build-plan-presentation.md"))
    b = plan["basis"]
    print(f"  pace {b['pacePointsPerDeveloperDay']} pts/dev-day, {b['hoursPerPoint']} h/pt; total {b['totalPoints']} pts = {b['totalHours']} h; finish {b['forecastFinish']}")
    print("  -> handoff/build-plan.json, handoff/TICVAI - Build Plan.xlsx, docs/active/build-plan-presentation.md")
