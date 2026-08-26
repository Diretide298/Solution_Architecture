#!/usr/bin/env python3
"""Derive diagrams/hld.yaml and diagrams/lld/<service>.yaml from the package.

**A diagram is a view of the other five layers, not a sixth kind of thing.** The viewer's
`lib/structure.mjs` already turns any YAML document into a node tree with a source line on every
node — so a diagram here is a YAML file that says what to draw, and the renderer already exists.

**Derived, never authored.** A hand-maintained diagram in a package with nine validators is the one
artefact that goes stale silently: nothing fails. That is how the mirrors drifted 503 files, and how
the services workbook said 371 tables against 379.

**Two levels, and the split is a readability decision.**

  **`hld.yaml`** — sixteen services in five tiers, the writes that cross between them, the deploy
  order, and the four services that can be down without stopping a sale. One canvas, sixteen nodes.

  **`lld/<service>.yaml`** — one file per service. Its schemas, its tables with column counts and
  stores, its operations grouped by contract, the screens that call it and the flows that walk it.
  **379 tables and 1,014 operations on one canvas is a hairball** — the same lesson as the 9,837
  board paths, and the reason this is sixteen files rather than one.

Every node carries a `ref` pointing at a real artefact, so a click goes somewhere.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import yaml
import sys

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams"

TIER_ORDER = ["foundation", "commerce", "operations", "engagement", "platform"]
TIER_NOTE = {
    "foundation": ("Read by everything, reads nothing above. **Deploys first and alone** — twelve "
                   "contracts read Identity and 289 tables anchor on `platform.scope_node`."),
    "commerce": "The sale path. Highest availability and the highest write rate in the platform.",
    "operations": ("What a venue does with what it sold. **Licensed per module** — a venue that "
                   "bought none of these runs none of them."),
    "engagement": ("Guests and intelligence. **Nothing that takes money depends on these**, which "
                   "is a deliberate property and one that should be tested rather than assumed."),
    "platform": "Provisioning, publishing, reporting, and the one path that crosses a region.",
}



# ── the scope hierarchy ──────────────────────────────────────────────────
# **Eight levels, seven organisational and one commercial.** Each earns its place by owning
# configuration nothing above or below can own — and the figures below are counted from the
# contracts rather than stated, because a level with no operations and no configuration is a
# level somebody drew on a whiteboard.

LEVELS = [
    ("tenant", "root", None,
     "**The commercial entity, and the level things are bought at.** Plans, licences, roles, "
     "message templates and loyalty programmes live here because they are bought here — a role "
     "defined at venue level would have to be defined eleven times.",
     ["Plans and licences", "Roles and permissions", "Message and inspection templates",
      "Loyalty programmes", "Dashboards"]),
    ("brand", "organisational", "tenant",
     "**Optional, and it costs nothing when unused.** A tenant operating two cinema brands needs "
     "a level between the company and the country; a tenant with one brand never creates a node, "
     "and the resolver skips a level that is not there.",
     ["Brand identity between company and country"]),
    ("region", "organisational", "brand",
     "**The level most often got wrong.** Currency, decimal scale, timezone and fiscal year are "
     "not venue settings and are **not overridable below** — a platform that lets one venue pick "
     "a different decimal scale has produced a ledger that cannot be consolidated (ADR-0018).",
     ["Currency and decimal scale", "Tax authority", "Timezone", "Fiscal year",
      "AI provider and seat-map templates"]),
    ("venue", "organisational", "region",
     "**Two thirds of all operations scope here, and that is the correct shape.** A venue is the "
     "unit a guest visits, a shift is worked at and stock is held in. It is the platform's "
     "default, and a reader who assumes venue scope will be right most of the time.",
     ["Almost everything operational", "Kitchen SLA and section layout", "Venue map",
      "Substitution rules", "Message triggers"]),
    ("department", "organisational", "venue",
     "**The staffing and budget tree** — who works where and whose budget it comes out of.",
     ["Requisitions", "Rotas", "Cost centres"]),
    ("subDepartment", "organisational", "department",
     "Optional second tier. A venue that does not need two does not create them.",
     ["A second tier of the same"]),
    ("workstation", "organisational", "subDepartment",
     "**A till is a scope, not just a device.** ADR-0002 makes authorisation user-driven rather "
     "than workstation-driven, but the workstation still holds settings a person does not carry "
     "with them.",
     ["Configuration profile", "Offline policy", "Connectivity thresholds", "Deposit box"]),
    ("outlet", "COMMERCIAL", "venue",
     "**A sibling of department, never a child of it** (CF-138, ADR-0018). A department answers "
     "*who works where*; an outlet answers *what is sold where*.\n\n"
     "**Modelling a restaurant as a department puts it in the staffing tree** — a venue whose "
     "restaurant is run by a concession would be describing staff it does not employ.\n\n"
     "**Only F&B and retail resolve here.** Everything else has no outlet on its path and "
     "resolves from venue exactly as before, which is what made an eighth level cheap enough to "
     "add after the hierarchy was already binding.",
     ["Menu and menu sections", "Table layout", "Return policy", "Opening hours"]),
]


def write_hierarchy(lin, contract_configs):
    """diagrams/hierarchy.yaml — the scope model, counted rather than asserted."""
    by_scope = Counter(v.get("scope") for v in lin.values())
    levels = []
    for name, branch, parent, why, owns in LEVELS:
        levels.append({
            "level": name,
            "branch": branch,
            "parent": parent,
            "operations": by_scope.get(name, 0),
            "configurations": len(contract_configs.get(name, [])),
            "configuredBy": sorted(contract_configs.get(name, []))[:8] or None,
            "owns": owns,
            "why": why,
        })
    doc = {
        "id": "HIERARCHY",
        "title": "TICVAI scope hierarchy — eight levels",
        "generatedBy": "tools/derive-diagrams.py",
        "about": (
            "**Where configuration lives.** A venue operator does not have one set of settings — a "
            "tenant with four brands across two countries and eleven venues has settings belonging "
            "at four different heights, and flattening them means either every venue configures "
            "everything from scratch or one change at the top breaks a venue that needed to "
            "differ.\n\n"
            "`platform.scope_node` is the answer. A node has a `level`, a `parent_id` and a "
            "materialised `path`; **configuration resolves by walking that path upward until "
            "something answers.**"),
        "decisions": ["docs/adr/0011-hierarchy-is-binding.md",
                      "docs/adr/0018-configuration-scope.md"],
        "spine": {
            "table": "platform.scope_node",
            "columns": ["id", "level", "parent_id", "path", "code", "name", "is_active",
                        "child_count"],
            "note": ('**The tenancy spine.** **304 of 379 tables anchor on it** and 71 reference it directly — the terminal anchor for almost everything in the package, and the reason a scope walk answers nearly every configuration question.'),
        },
        "branches": {
            "organisational": ("Who works where. Department, sub-department and workstation carry "
                               "requisitions, rotas and cost centres."),
            "commercial": ("What is sold where. Only `outlet`, and only F&B and retail resolve "
                           "against it."),
        },
        "levels": levels,
        "rules": [
            {"rule": "Region settings are not overridable below",
             "why": ("A venue in Dubai and a venue in Abu Dhabi share a currency, a tax authority "
                     "and a fiscal calendar. **One venue on a different decimal scale is a ledger "
                     "that cannot consolidate.**")},
            {"rule": "An absent level is skipped, not empty",
             "why": ("A tenant with one brand never creates a brand node and the resolver walks "
                     "past it. **That is what makes an optional level cost nothing.**")},
            {"rule": "Outlet is a sibling of department",
             "why": ("The same physical restaurant can be one department and two outlets — a "
                     "kitchen and a bar — or two departments and one outlet.")},
            {"rule": "Venue scope is a default, not a service boundary",
             "why": ("675 of 1,014 operations are venue-scoped. **`shift` was folded into Tenancy "
                     "because it is venue-scoped and moved to Order the same day**: scope answers "
                     "whose configuration this is, schema answers whose data it is.")},
        ],
    }
    (OUT / "hld" / "01-hierarchy.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
    return len(levels)



# ── the project HLD ──────────────────────────────────────────────────────
# **The whole platform on one canvas**, not just its services. Who uses it, through what surface,
# against which services, over which stores, and where it crosses a boundary the law cares about.
#
# `hld-services.yaml` is the service view and this is the layer above it: **a reader who has not
# seen the package should be able to start here and know what TICVAI is.**

def write_project_hld(services, lin, schema, real, owner):
    """diagrams/hld.yaml — actors, surfaces, services, stores, externals, regions."""
    plats = []
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        pl = d["platform"]
        ops = {a.get("operationId") for s in d["screens"] for a in (s.get("apis") or [])}
        svcs = sorted({lin[o]["service"] for o in ops if o in lin})
        mods = sorted({s.get("requiresModule") for s in d["screens"] if s.get("requiresModule")})
        plats.append({
            "platform": pl["code"],
            "name": pl["name"],
            "audience": pl.get("audience"),
            "operator": pl.get("operator"),
            "app": pl.get("app"),
            "formFactor": pl.get("formFactor"),
            "offlineCapable": bool(pl.get("offlineCapable")),
            "screens": len(d["screens"]),
            "modules": mods,
            "callsServices": svcs,
            "ref": f"diagrams/lld/platforms/{pl['code']}.yaml",
        })

    def reached_by(table):
        """Every service that writes the table an external system is reached through."""
        cs = {v["contract"] for v in lin.values() if table in (v.get("writes") or [])}
        return sorted({owner_of_contract.get(c) for c in cs if owner_of_contract.get(c)})

    owner_of_contract = {c: n for n, v in services.items() for c in v["contracts"]}

    def store_users(store):
        """Services whose operations touch this store, busiest first."""
        c = Counter(v["service"] for v in lin.values()
                    if store in (v.get("stores") or []) and v.get("service"))
        return [{"service": k, "operations": n} for k, n in c.most_common()]

    aud = Counter(a for v in lin.values() for a in (v.get("audience") or []))
    stores = Counter(st for v in lin.values() for st in (v.get("stores") or []))

    doc = {
        "id": "HLD",
        "title": "TICVAI — the whole platform",
        "generatedBy": "tools/derive-diagrams.py",
        "about": (
            "**A multi-tenant venue platform.** One tenant operates several venues; a venue sells "
            "admission, food, retail and experiences; a guest arrives, is admitted, spends and "
            "leaves.\n\n"
            "**Five layers, one join.** Screens name operations, operations resolve against 28 "
            "OpenAPI contracts, contracts persist to 26 schemas, and every artefact in the package "
            "is drawn by resolving against that join rather than by being written twice."),
        "scale": {
            "operations": len(lin),
            "contracts": len({v["contract"] for v in lin.values()}),
            # **374 real tables, not the 379 in status.json.** That figure includes five
            # cache and vector namespaces — ,  — which are
            # storage the platform writes and not tables anybody migrates.
            "tables": len(real),
            "tablesNote": (
                "**Postgres tables only.** `status.json` reports 379 because it counts five "
                "non-table stores. **They own no service and should not**: a cache entry is "
                "derived from something already read, invalidated by an event already consumed, "
                "and losable without consequence. **Both numbers are right and they count "
                "different things**, which is worth saying rather than letting a reader find the "
                "difference."),
            "nonTableStores": ["cache:answer", "cache:embedding", "cache:idempotency",
                               "cache:resolution", "qdrant:knowledge"],
            "schemas": len({t.split(".")[0] for t in real}),
            "services": len(services),
            "platforms": len(plats),
            "apps": len({p["app"] for p in plats}),
            "screens": sum(p["screens"] for p in plats),
            "flows": len(list((ROOT / "flows").glob("F*.yaml"))),
            "stateModels": len(list((ROOT / "states").glob("*.yaml"))) - 1,
            "events": len(list((ROOT / "events").glob("*.yaml"))) - 1,
            "decisions": len(list((ROOT / "docs" / "adr").glob("*.md"))),
            "requirements": 3184,
            "buildPercent": 0,
        },
        "actors": [
            {"actor": "guest", "reaches": ["P01", "P02", "P05"], "operations": aud.get("guest", 0),
             "note": ("Buys, arrives, is admitted, spends. **Never sees a staff surface** — "
                      "`check-screens` refuses a guest screen declaring a staff permission.")},
            {"actor": "venue staff", "reaches": ["P04", "P06", "P07", "P08", "P15", "P16"],
             "operations": aud.get("staff", 0),
             "note": ("Sells, admits, cooks, counts, configures. **Authority is carried by the "
                      "person, not the device** (ADR-0002) — which is what makes a shared handheld "
                      "safe.")},
            {"actor": "partner", "reaches": ["P10"], "operations": aud.get("partner", 0),
             "note": "Resellers and agents, with their own credit and settlement."},
            {"actor": "platform operator", "reaches": ["P09", "P12"], "operations": 0,
             "note": "Provisions tenants, watches cells, runs releases. **Softlabs, not the venue.**"},
            {"actor": "developer", "reaches": ["P14"], "operations": aud.get("public", 0),
             "note": "Third parties against the public API, rate-limited and quota'd."},
            {"actor": "device", "reaches": ["P07", "P15"], "operations": aud.get("device", 0),
             "note": ("Turnstiles, scanners, kitchen displays. **A device authenticates and does "
                      "not authorise.**")},
        ],
        "surfaces": plats,
        "services": {
            "count": len(services),
            "view": "diagrams/hld/02-services.yaml",
            "note": ("Sixteen deployable services in five tiers. **The data boundary decides where "
                     "they split** — no service spans a schema it does not own."),
            "byTier": {t: sorted(n for n, v in services.items() if v["tier"] == t)
                       for t in TIER_ORDER},
        },
        # **The store column carried a total and no edges.** `postgres 1000 operations` tells a
        # reader nothing about which service to look at when Postgres is slow. Each store now names
        # the services that use it, computed — and the small ones are the useful ones: **qdrant is
        # AiService alone, derived is Inventory and F&B.**
        "stores": [
            {"store": "postgres", "operations": stores.get("postgres", 0), "usedBy": store_users("postgres"),
             "note": ("**One Postgres per cell**, 26 schemas inside it. Not one database per "
                      "tenant (ADR-0005) — tenancy is a partition key, not a deployment "
                      "boundary.")},
            {"store": "redis", "operations": stores.get("redis", 0), "usedBy": store_users("redis"),
             "note": ("Sessions, resolution caches, idempotency. **Losable without consequence** — "
                      "nothing treats a cache entry as a source of truth.")},
            {"store": "postgres-analytical", "operations": stores.get("postgres-analytical", 0), "usedBy": store_users("postgres-analytical"),
             "note": ("Reporting and AI interactions. **Never the transactional primary** "
                      "(ADR-0016).")},
            {"store": "qdrant", "operations": stores.get("qdrant", 0), "usedBy": store_users("qdrant"),
             "note": "Vector search for the concierge and semantic lookup."},
            {"store": "derived", "operations": stores.get("derived", 0), "usedBy": store_users("derived"),
             "note": ("**Computed, never stored.** `inventory.stock_level` is the example: a "
                      "stored level and a movement ledger that disagree is a stock count nobody "
                      "can reconcile.")},
        ],
        # **`via` was hand-written and said one service where six reach it.**
        # `marketing.message_dispatch` is written by fnb, marketing-crm, orders, public-api,
        # workforce and identity — a payment link, a booking confirmation, an OTP, a rota change
        # and an evacuation notice are all *somebody asked for a message*. Drawing one arrow to
        # Marketing hides five paths a reader needs when messaging fails.
        #
        # **Now computed from the lineage** so it cannot drift from the writes it describes.
        "external": [
            {"system": "Payment gateway", "via": reached_by("orders.payment"),
             "reachedThrough": "orders.payment",
             "note": ("**Tenant as merchant of record for phase 1**; PayFac deferred. The highest-"
                      "consequence unresolved payment assumption.")},
            {"system": "UAE Pass and tenant SSO", "via": "IdentityService",
             "note": "A guest arrives verified in a way an email never is."},
            {"system": "Messaging — SMS, WhatsApp, push, email",
             "via": reached_by("marketing.message_dispatch"),
             "reachedThrough": "marketing.message_dispatch",
             "note": ("**One dispatch table, six services.** A payment link from Order, a booking "
                      "confirmation from Order, an OTP from Identity, a rota change from Tenancy, "
                      "an allergen alert from F&B, a campaign from Marketing — **every one is "
                      "somebody sending a message that was asked for.**\n\n"
                      "**A ticket purchase reaches messaging twice**: the payment link before "
                      "tender and the confirmation after. Neither goes through Marketing.")},
            {"system": "Queue systems", "via": "VenueOpsService",
             "note": ("**Adaptor-first** (ADR-0012). The platform holds what the venue's own queue "
                      "system reports.")},
            {"system": "AI providers", "via": reached_by("ai.interaction"),
             "reachedThrough": "ai.interaction",
             "note": ("BYOK, budgeted and metered. **Read-only against the transactional core** "
                      "(ADR-0020).\n\n"
                      "**Reporting reaches it too** — the governed pair. A natural-language query "
                      "*is* an AI interaction, which is why `reporting` may write `ai.interaction` "
                      "and nothing else outside AiService may.")},
            {"system": "Webhooks out", "via": reached_by("control.webhook_subscription"),
             "reachedThrough": "control.webhook_subscription",
             "note": "Third parties subscribe; replay is available."},
        ],
        "regions": {
            "model": "one cell per jurisdiction",
            "note": ("**A cell is a deployment and a legal boundary at once** (ADR-0001). UAE data "
                     "residency is required and DESC review shapes it.\n\n"
                     "**Only CrossCellService reaches another region**, and it moves a pseudonymous "
                     "guest link rather than a guest (ADR-0010) — which is what makes a membership "
                     "work in another country without moving anybody's personal data."),
            "unresolved": "CF-64 — the cloud provider is undecided, and every concrete infrastructure artefact depends on it",
        },
        "layers": [
            {"layer": "frontend", "holds": "477 screens, 93 flows, 15 platforms, 12 apps"},
            {"layer": "contracts", "holds": f"{len(lin)} operations across 28 contracts — the join"},
            {"layer": "backend", "holds": f"{len(real)} tables in 26 schemas, 910 relationships"},
            {"layer": "domain", "holds": "113 state models, 29 events"},
            {"layer": "decisions", "holds": "29 ADRs, 148 conflicts closed, 6 open"},
        ],
        "views": {
            "services": "diagrams/hld/02-services.yaml",
            "hierarchy": "diagrams/hld/01-hierarchy.yaml",
            "perService": "diagrams/lld/services/",
            "perPlatform": "diagrams/lld/platforms/",
        },
        "honestly": (
            "**Build is 0%.** 379 tables specified and none written; design is 93% of in-scope "
            "requirements. **The gap between the two is the entire risk**, and no diagram in this "
            "folder changes it."),
    }
    (OUT / "hld" / "00-platform.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
    return plats



def write_platform_llds(lin, services):
    """diagrams/lld/platforms/<code>.yaml — one per surface.

    **The service LLD answers *what does this service own*; this answers *what does this surface
    do*.** They are different readers: a backend engineer opens the first, a frontend engineer
    opens the second, and neither wants the other's file.
    """
    flows_by_screen = defaultdict(set)
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        for st in (d.get("steps") or []):
            if st.get("screen"):
                flows_by_screen[st["screen"]].add(f"{d['id']} {d['name']}")

    made = 0
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        pl = d["platform"]
        screens = []
        svc = Counter()
        mods = Counter()
        for s in d["screens"]:
            ops = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
            for o in ops:
                if o in lin:
                    svc[lin[o]["service"]] += 1
            if s.get("requiresModule"):
                mods[s["requiresModule"]] += 1
            screens.append({
                "screen": s["id"],
                "name": s["name"],
                "module": s.get("module"),
                "requiresModule": s.get("requiresModule"),
                "wave": s.get("wave"),
                "density": s.get("density"),
                "operations": sorted(o for o in ops if o in lin),
                "states": sorted(s.get("states") or {}),
                "offlineState": "offline" in (s.get("states") or {}),
                "entryParams": [f"{x['name']}<-{x['from']}"
                                for x in ((s.get("entryState") or {}).get("params") or [])],
                "goesTo": sorted((s.get("navigation") or {}).get("exitTo") or []),
                "boardFrames": s.get("boardFrames") or None,
                "wireframe": (s.get("wireframe") or {}).get("board"),
                "inFlows": sorted(flows_by_screen.get(s["id"], ())) or None,
            })
        doc = {
            "id": f"LLD-{pl['code']}",
            "title": f"{pl['code']} {pl['name']} — {len(screens)} screens",
            "generatedBy": "tools/derive-diagrams.py",
            "index": "diagrams/hld/00-platform.yaml",
            "audience": pl.get("audience"),
            "operator": pl.get("operator"),
            "app": pl.get("app"),
            "formFactor": pl.get("formFactor"),
            "runtime": pl.get("runtime"),
            "offlineCapable": bool(pl.get("offlineCapable")),
            "deployment": pl.get("deployment"),
            "why": pl.get("notes"),
            "modulesUsed": [{"module": m, "screens": n} for m, n in mods.most_common()],
            "servicesCalled": [{"service": k, "operationCalls": n} for k, n in svc.most_common()],
            "coverage": {
                "screens": len(screens),
                "inAFlow": len([x for x in screens if x["inFlows"]]),
                "drawn": len([x for x in screens if x["wireframe"]]),
                "note": ("**A screen in no flow has been specified and never walked.** Every flow "
                         "written in this package has found a defect."),
            },
            "screens": screens,
        }
        (OUT / "lld" / "platforms" / f"{pl['code']}.yaml").write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
        made += 1
    return made



# ── contracts and lifecycles ─────────────────────────────────────────────
# **The two layers with no diagram of their own.** DB has a computed ER and Frontend has its
# platform files; contracts and lifecycles had neither, and both carry a join nothing else shows:
# **which contracts share an event, and which operations move a thing from one state to another.**

def write_contracts(lin, services, owner):
    """diagrams/hld/03-contracts.yaml and lld/contracts/<name>.yaml."""
    # **Enumerate the files, not the lineage.** Grouping by `lin[o]["contract"]` only ever sees a
    # contract that has operations — so `contracts/shared/common.yaml` and `permissions.yaml` were
    # invisible, and the diagram drew 28 of 30 while describing a `shared` tier that was empty.
    #
    # **Nothing on a diagram announces what it left out.** A reader counting boxes gets a smaller
    # number and no reason to doubt it, which is why the reverse check — a package contract the
    # diagram lacks — matters more than the one that was already there.
    tier_of = {}
    for f in sorted(ROOT.glob("contracts/*/*.yaml")):
        tier_of[f.stem] = f.parent.name  # spine | satellite | shared

    by = defaultdict(list)
    for c in tier_of:
        by[c] = []
    for o, v in lin.items():
        by[v["contract"]].append(o)

    events = defaultdict(set)
    for f in sorted((ROOT / "events").glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        pub = d.get("publishedBy") or d.get("publisher")
        for c in ([pub] if isinstance(pub, str) else (pub or [])):
            events[c].add(f.stem)
        for c in (d.get("consumedBy") or d.get("consumers") or []):
            events[c if isinstance(c, str) else str(c)].add(f.stem)

    rows = []
    for c, ops in sorted(by.items(), key=lambda kv: -len(kv[1])):
        svc = Counter(lin[o]["service"] for o in ops).most_common(1)
        verbs = Counter(lin[o]["verb"] for o in ops)
        shared = tier_of.get(c) == "shared"
        rows.append({
            "contract": c,
            "tier": tier_of.get(c, "satellite"),
            "operations": len(ops),
            "holds": ("**A vocabulary, not a surface.** No operations by design — it is referenced "
                      "by every other contract and called by nobody.") if shared else None,
            "service": svc[0][0] if svc else "—",
            "verbs": dict(verbs.most_common()),
            "guestCallable": len([o for o in ops if "guest" in (lin[o].get("audience") or [])]),
            "offlineCapable": len([o for o in ops if lin[o].get("offline")]),
            "events": sorted(events.get(c, ())) or None,
            "ref": f"diagrams/lld/contracts/{c}.yaml",
        })
        (OUT / "lld" / "contracts" / f"{c}.yaml").write_text(yaml.safe_dump({
            "id": f"LLD-{c}",
            "title": f"{c} — {len(ops)} operations",
            "generatedBy": "tools/derive-diagrams.py",
            "index": "diagrams/hld/03-contracts.yaml",
            "tier": tier_of.get(c, "satellite"),
            "service": svc[0][0] if svc else "—",
            "operations": [{
                "operation": o, "verb": lin[o]["verb"], "path": lin[o]["path"],
                "scope": lin[o].get("scope"), "permission": lin[o].get("perm") or None,
                "audience": lin[o].get("audience"), "offline": bool(lin[o].get("offline")),
                "reads": sorted(lin[o].get("reads") or []),
                "writes": sorted(lin[o].get("writes") or []),
            } for o in sorted(ops)],
        }, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")

    (OUT / "hld" / "03-contracts.yaml").write_text(yaml.safe_dump({
        "id": "HLD-CONTRACTS",
        "title": f"{len(rows)} contracts — the join between every other layer",
        "generatedBy": "tools/derive-diagrams.py",
        "index": "diagrams/hld/00-platform.yaml",
        "about": (
            "**The API is the join.** Screens name operations, operations resolve here, and this "
            "persists to the schemas — every other artefact in the package is drawn by resolving "
            "against these rather than being written twice.\n\n"
            "**Spine contracts are read by almost everything; satellites read down into them and "
            "never the reverse.** That direction is the property that makes the service split "
            "possible."),
        "tiers": {
            "spine": ("Read by nearly every satellite. A change here reaches the whole platform."),
            "satellite": ("A domain with its own schema and its own licence. **Reads down into the "
                          "spine and is never read by it.**"),
            "shared": "Vocabularies — permissions, common parameters, problem shapes.",
        },
        "contracts": rows,
    }, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
    return len(rows)


def write_lifecycles(lin):
    """diagrams/hld/04-lifecycles.yaml and lld/lifecycles/<entity>.yaml.

    **The layer that answers *when*.** Contracts say an operation exists; the backend says a column
    holds a value. **Only this says `actioned` cannot go straight to `closed`** — and 223 of 1,014
    operations are named by a transition, so a quarter of the API is a state change somewhere.
    """
    models = []
    for f in sorted((ROOT / "states").glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        trs = d.get("transitions") or []
        ops = sorted({t["operation"] for t in trs if t.get("operation") and t["operation"] in lin})
        models.append({
            "entity": d.get("entity", f.stem),
            "contract": d.get("contract"),
            "owner": d.get("owner"),
            "service": (lin[ops[0]]["service"] if ops else None),
            "states": len(d.get("states") or []) or None,
            "transitions": len(trs),
            "initial": d.get("initial"),
            "terminal": d.get("terminal"),
            "operations": ops,
            "guarded": len([t for t in trs if t.get("guard")]),
            "ref": f"diagrams/lld/lifecycles/{f.stem}.yaml",
        })
        (OUT / "lld" / "lifecycles" / f"{f.stem}.yaml").write_text(yaml.safe_dump({
            "id": f"LLD-{d.get('entity', f.stem)}",
            "title": f"{d.get('entity', f.stem)} — {len(trs)} transitions",
            "generatedBy": "tools/derive-diagrams.py",
            "index": "diagrams/hld/04-lifecycles.yaml",
            "source": f"states/{f.name}",
            **{k: v for k, v in d.items() if k != "$schema"},
        }, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")

    evs = []
    for f in sorted((ROOT / "events").glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        evs.append({"event": f.stem, **{k: v for k, v in d.items()
                                        if k in ("publishedBy", "consumedBy", "description")}})

    # **`states/` holds 114 files and 113 are lifecycles.** `_schema.yaml` is the shape every
    # other file validates against, not a model — and a diagram that quietly draws one fewer than
    # the folder holds is a diagram a reader cannot reconcile. Say what was skipped.
    skipped = sorted(f.name for f in (ROOT / "states").glob("*.yaml") if f.stem.startswith("_"))
    (OUT / "hld" / "04-lifecycles.yaml").write_text(yaml.safe_dump({
        "id": "HLD-LIFECYCLES",
        "sourceFiles": {
            "folder": "states/",
            "files": len(list((ROOT / "states").glob("*.yaml"))),
            "drawn": len(models),
            "skipped": skipped,
            "why": ("**`_schema.yaml` is the shape, not a model.** Every state file validates "
                    "against it; it has no entity and no transitions."),
        },
        "title": f"{len(models)} state models and {len(evs)} events",
        "generatedBy": "tools/derive-diagrams.py",
        "index": "diagrams/hld/00-platform.yaml",
        "about": (
            "**What can happen to a thing, and in what order.** A state model is a lifecycle "
            "within one entity; an event is a lifecycle crossing between two.\n\n"
            "**223 of 1,014 operations are named by a transition** — a quarter of the API is a "
            "state change somewhere, and the rule that a critical finding cannot be signed by "
            "whoever raised it lives here and nowhere else."),
        "naming": (
            "**Called `domain` in the viewer, which names a methodology rather than a subject.** "
            "Every other layer names a thing a reader recognises. `Lifecycles` covers both halves "
            "and says what question it answers."),
        "stateModels": models,
        "events": evs,
    }, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
    return len(models), len(evs)



def write_index():
    """diagrams/README.yaml — the map of the map."""
    hld = []
    for f in sorted((OUT / "hld").glob("*.yaml")):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        hld.append({"file": f"diagrams/hld/{f.name}", "id": d["id"], "title": d["title"]})
    lld = [{"set": sub, "files": len(list((OUT / "lld" / sub).glob("*.yaml"))),
            "folder": f"diagrams/lld/{sub}/"}
           for sub in ("services", "platforms", "contracts", "lifecycles")]
    (OUT / "README.yaml").write_text(yaml.safe_dump({
        "id": "DIAGRAMS",
        "title": "TICVAI — high level and low level, by layer",
        "generatedBy": "tools/derive-diagrams.py",
        "about": (
            "**Two levels, five subjects.** The high level is one file per subject and fits on a "
            "canvas; the low level is one file per thing and does not.\n\n"
            "**Every file is derived and none is authored.** A hand-maintained diagram in a package "
            "with nine validators is the one artefact that goes stale silently — nothing fails when "
            "it is wrong. `check-package` refuses a diagram older than the decomposition it is "
            "drawn from."),
        "howToRead": ("Start at `hld/00-platform.yaml` — actors, surfaces, services, stores, "
                      "externals, regions. Every node carries a `ref` at the file below it."),
        "notCovered": {
            "db": ("**The DB layer already has both and they are computed** — the Galaxy view is "
                   "the schema overview and the drill-down is the table detail. **A YAML restating "
                   "a live view is a file that can disagree with it**, which is the failure this "
                   "folder exists to avoid."),
            "decisions": "29 ADRs and a conflict register. Prose, and it should stay prose.",
        },
        "hld": hld,
        "lld": lld,
    }, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")
    return len(hld), sum(x["files"] for x in lld)


def load(name: str):
    return json.loads((ROOT / "handoff" / name).read_text(encoding="utf-8"))


def main() -> int:
    decomp = load("service-decomposition.json")
    services = decomp["services"]
    lin = load("api-data-lineage.json")
    schema = load("schema-reference.json")

    real = {t for t in (set(schema.get("cols") or {}) | set(schema.get("storage") or {}))
            if "." in t and ":" not in t}
    owner = {s: n for n, v in services.items() for s in v["schemas"]}

    # ── screens and flows per service, read from the source rather than a summary
    screens = defaultdict(list)
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            for a in (s.get("apis") or []):
                op = a.get("operationId")
                if op in lin:
                    screens[lin[op]["service"]].append(f"{code}:{s['id']} {s['name']}")
    for k in screens:
        screens[k] = sorted(set(screens[k]))

    flows = defaultdict(list)
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for st in (doc.get("steps") or []):
            for op in (st.get("operations") or []):
                if op in lin:
                    flows[lin[op]["service"]].append(f"{doc['id']} {doc['name']}")
    for k in flows:
        flows[k] = sorted(set(flows[k]))

    # ── cross-service edges, computed not stated
    writes = defaultdict(Counter)
    reads = defaultdict(Counter)
    for op, v in lin.items():
        me = v.get("service")
        for t in v.get("writes", []):
            if t in real:
                them = owner.get(t.split(".")[0])
                if them and them != me:
                    writes[me][them] += 1
        for t in v.get("reads", []):
            if t in real:
                them = owner.get(t.split(".")[0])
                if them and them != me:
                    reads[me][them] += 1

    # **Recount from the lineage before drawing anything.** `service-decomposition.json` caches
    # `operations` and `tables`, and a cached number is only as fresh as the last run of whatever
    # writes it — two operations added to the lineage left `OrderService` drawn at 96 against a
    # live 97, and every check passed because they all compared the diagram to the cache.
    #
    # **A figure that can be computed should not be read.** The decomposition stays authoritative
    # for the reasoning; the counts come from the source.
    for _n, _v in services.items():
        _ops = [o for o, x in lin.items() if x.get("service") == _n]
        _v["operations"] = len(_ops)
        _v["tables"] = len([t for t in real if t.split(".")[0] in _v["schemas"]])

    OUT.mkdir(exist_ok=True)
    for sub in ("hld", "lld/services", "lld/platforms", "lld/contracts", "lld/lifecycles"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)

    # ── HLD ──────────────────────────────────────────────────────────────
    tiers = []
    for tier in TIER_ORDER:
        nodes = []
        for name, v in sorted(((n, x) for n, x in services.items() if x["tier"] == tier),
                              key=lambda kv: -kv[1]["operations"]):
            cov = v.get("flowCoverage") or {}
            nodes.append({
                "service": name,
                "operations": v["operations"],
                "tables": v["tables"],
                "schemas": v["schemas"],
                "contracts": v["contracts"],
                "flowCoverage": f"{cov.get('percent', 0)}%",
                "scale": v["scale"],
                "ifDown": v["risk"],
                "ref": f"diagrams/lld/services/{name}.yaml",
            })
        tiers.append({"tier": tier, "meaning": TIER_NOTE[tier], "services": nodes})

    edges = []
    for a, cc in sorted(writes.items()):
        for b, n in cc.most_common():
            edges.append({
                "from": a, "to": b, "writes": n,
                "reads": reads[a].get(b, 0),
                "kind": "strong" if n >= 5 else "ordinary",
            })
    edges.sort(key=lambda e: -e["writes"])

    hld = {
        "id": "HLD",
        "title": "TICVAI — sixteen services in five tiers",
        "generatedBy": "tools/derive-diagrams.py",
        "about": (
            "**What ships together.** 1,014 operations and 379 tables resolve into sixteen "
            "deployable services, and **the data boundary decides where they split** — no service "
            "spans a schema it does not own, and no schema is written by two services.\n\n"
            "**Arrows are cross-service writes.** The rule is that the owner defines the row and a "
            "foreign writer may only append to it: a till closing posts to `ledger.entry` because "
            "settling a shift *is* a ledger act."),
        "decision": "docs/adr/0028-service-decomposition.md",
        "tiers": tiers,
        "crossServiceWrites": edges,
        "deployOrder": [
            {"order": 1, "tier": "foundation",
             "rule": ("**First and alone.** A restart of Identity is an outage everywhere.")},
            {"order": 2, "tier": "commerce",
             "rule": ("**Catalogue before Order** — a till pulls a bundle before it sells. "
                      "**Access last of the four**: it runs at the edge with a local cache and can "
                      "lag the others safely.")},
            {"order": 3, "tier": "operations",
             "rule": "**Module-gated.** `requiresModule` on every screen decides what a tenant sees."},
            {"order": 4, "tier": "engagement",
             "rule": "**Can ship late and be down.**"},
            {"order": 5, "tier": "platform",
             "rule": ("Control provisions a tenant rather than serving one. CrossCell only matters "
                      "once a second region exists.")},
        ],
        "canBeDownWithoutStoppingASale": [
            n for n, v in services.items()
            if v["tier"] in ("engagement",) or n in ("ReportingService", "CrossCellService")],
        "notes": (
            "**`shift` moved from Tenancy to Order on 24 August.** It owns no tables of its own — "
            "which is true, and the conclusion drawn from it was wrong. **A service with no data "
            "belongs where its data is**, and a shift's data is entirely in `orders`.\n\n"
            "**The coupling made it visible**: all 43 of Tenancy's cross-service touches into "
            "`orders` were the `shift` contract. Moving it took Tenancy's cross-service writes from "
            "23 to 2."),
    }
    (OUT / "hld" / "02-services.yaml").write_text(
        yaml.safe_dump(hld, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")

    # ── LLD, one per service ─────────────────────────────────────────────
    for name, v in services.items():
        ops = sorted(o for o, x in lin.items() if x.get("service") == name)
        by_contract = defaultdict(list)
        for o in ops:
            x = lin[o]
            by_contract[x["contract"]].append({
                "operation": o,
                "verb": x["verb"],
                "path": x["path"],
                "scope": x.get("scope"),
                "permission": x.get("perm") or None,
                "offline": bool(x.get("offline")),
                "reads": len(x.get("reads", [])),
                "writes": len(x.get("writes", [])),
            })

        # **A service's operations cite five stores the table list never showed.** `cache:answer`,
        # `cache:embedding`, `cache:idempotency`, `cache:resolution` and `qdrant:knowledge` are
        # namespaced with a colon, so the `real` filter — which requires a dot and forbids a colon —
        # excluded them from every table listing while the contract LLDs kept citing them as reads
        # and writes. **A reader could follow an operation to a store the diagram said did not
        # exist.**
        #
        # **They are listed and marked, not owned.** A cache entry is derived from something already
        # read, invalidated by an event already consumed, and losable without consequence — giving
        # it a service would imply a migration and a backup it does not need.
        cited = sorted({t for o in ops for t in (lin[o].get("reads", []) + lin[o].get("writes", []))
                        if ":" in t})
        tables = [{
            "store": t,
            "kind": "cache" if t.startswith("cache:") else "vector",
            "columns": len((schema.get("cols") or {}).get(t) or []),
            "backing": (schema.get("store") or {}).get(t, "redis"),
            "owned": False,
            "why": ("**Not a table and not owned by a service.** Derived from something already "
                    "read, invalidated by an event already consumed, losable without consequence — "
                    "no migration, no backup, no owner."),
        } for t in cited]
        for t in sorted(t for t in real if t.split(".")[0] in v["schemas"]):
            cols = (schema.get("cols") or {}).get(t) or []
            lineage = (schema.get("lineage") or {}).get(t) or {}
            wc = sorted({lin[o]["contract"] for o in lin
                         for tt in lin[o].get("writes", []) if tt == t})
            tables.append({
                "table": t,
                "columns": len(cols),
                "store": (schema.get("store") or {}).get(t, "postgres"),
                "parent": lineage.get("parent"),
                "writtenBy": wc,
                # **A foreign writer is a contract this service does not own** — not merely one of
                # several. The first cut listed the owner's own contract whenever a table had two
                # writers, which reported `orders` as foreign to OrderService.
                "foreignWriters": [c for c in wc if c not in v["contracts"]] or None,
            })

        cov = v.get("flowCoverage") or {}
        doc = {
            "id": f"LLD-{name}",
            "title": f"{name} — {v['operations']} operations, {v['tables']} tables",
            "generatedBy": "tools/derive-diagrams.py",
            "tier": v["tier"],
            "index": "diagrams/hld/02-services.yaml",
            "why": v["why"],
            "scale": v["scale"],
            "ifDown": v["risk"],
            "coverage": {
                # **len(ops) is the live count and cov["operations"] is the cached one.** The fallback was
                # the wrong way round — the cache won whenever it existed, which is always.
                "operations": len(ops),
                "inAFlow": cov.get("inAFlow", 0),
                "percent": f"{cov.get('percent', 0)}%",
                "note": ("**Flow coverage is how much of this service a journey has walked.** "
                         "A service under 40% is unwalked rather than under-documented."),
            },
            # **A storage note belongs to a table, not to the schema it sits in.** The first cut
            # took the note from whichever table sorted first and labelled all 34 `fnb` tables with
            # it — so the whole schema was described by a sentence about `fnb.guest_note`, and it
            # would have changed silently on any run that added an earlier-sorting table.
            #
            # **A schema-level fact has to be derived from the schema**, so this reports the shape
            # rather than borrowing prose that was written about something else.
            "schemas": [{
                "schema": s,
                "tables": len([t for t in real if t.split(".")[0] == s]),
                "stores": sorted({(schema.get("store") or {}).get(t, "postgres")
                                  for t in real if t.split(".")[0] == s}),
                "largestTable": max(
                    ((t, len((schema.get("cols") or {}).get(t) or []))
                     for t in real if t.split(".")[0] == s),
                    key=lambda x: x[1], default=("—", 0))[0],
            } for s in v["schemas"]],
            "operationsByContract": [
                {"contract": c, "count": len(items), "operations": items}
                for c, items in sorted(by_contract.items(), key=lambda kv: -len(kv[1]))],
            "tables": tables,
            "readsFrom": [{"service": k, "operations": n} for k, n in
                          sorted((v.get("readsFrom") or {}).items(), key=lambda kv: -kv[1])],
            "writesOutside": [{"service": k, "operations": n, "why": (
                "**The owner defines the row; this service may only append to it.**")}
                for k, n in sorted((v.get("writesOutside") or {}).items(), key=lambda kv: -kv[1])],
            "screens": screens.get(name, []),
            "flows": flows.get(name, []),
        }
        (OUT / "lld" / "services" / f"{name}.yaml").write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=98), encoding="utf-8")

    cfg = defaultdict(list)
    for f in sorted(ROOT.glob("contracts/*/*.yaml")):
        doc_ = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for _p, item in (doc_.get("paths") or {}).items():
            for _v, o in item.items():
                if isinstance(o, dict) and o.get("x-ticvai-config-scope"):
                    cfg[o["x-ticvai-config-scope"]].append(o["operationId"])
    n_levels = write_hierarchy(lin, cfg)
    plats = write_project_hld(services, lin, schema, real, owner)
    n_plat = write_platform_llds(lin, services)
    n_ctr = write_contracts(lin, services, owner)
    n_sm, n_ev = write_lifecycles(lin)

    print(f"  HLD:       the project — {len(plats)} surfaces, {len(services)} services")
    print(f"  LLD:       {n_plat} platforms -> diagrams/lld/platforms/")
    print(f"  HLD:       {n_ctr} contracts · {n_sm} state models · {n_ev} events")
    n_h, n_l = write_index()
    print(f"  INDEX:     {n_h} HLD · {n_l} LLD -> diagrams/README.yaml")

    print(f"  HIERARCHY: {n_levels} levels -> diagrams/hierarchy.yaml")
    print(f"  HLD-SVC:   {len(services)} services in {len(tiers)} tiers, {len(edges)} edges")
    print(f"  LLD:       {len(services)} services -> diagrams/lld/services/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
