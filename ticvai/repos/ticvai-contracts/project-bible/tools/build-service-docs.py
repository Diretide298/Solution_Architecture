#!/usr/bin/env python3
"""Build the first-release documentation and task sheet from the delivery slice.

**Generated, never written.** Services are built to a slice and then extended additively, so this
document will be out of date the first time somebody adds an operation, unless re-running a
script is all it takes to update it. Everything here is read from the contracts, the screens,
the lineage and `handoff/delivery-slice.json`; the only authored text is the headings.

Writes, under handoff/service-docs/:

  README.md                  architecture: apps, services, and the platform x service matrix
  frontend/<platform>.md     every screen: purpose, states, entry, the operations it calls
  backend/<Service>.md       every in-slice operation to field level, the tables behind it
  backend/MIGRATIONS.md      the first release's tables and the migrations that create them, in order
  client-summary.md          the same, in plain language, with no field-level detail
  TICVAI_First_Release.xlsx  Services, Operations, Fields, Screens, Tasks, Migrations, Tables, Gaps
  TICVAI_First_Release_Client.xlsx  Platforms, Services, Screens, in plain language
  TICVAI_Backend_Build_Plan.xlsx  build plan, migrations, tables, services, APIs, API schemas, fields
  tasks.csv                  one row per work package, keyed for ADAM's OpenProject create()

**The task sheet is an input to OpenProject, not a second plan** (CF-124). Keys are local; the
`parent` and `dependsOn` columns name other keys in the same file, so a person or ADAM's bridge
creates parents first and links children to them. No dates and no estimates: OpenProject owns both.

Run: python3 tools/build-service-docs.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"
OUT = HANDOFF / "service-docs"
TEAM = ROOT / "docs" / "active" / "team.json"
MAX_DEPTH = 3

# **The one authored table in this file.** The decomposition explains each service to an architect
# ("platform.org_unit is reached by 304 of 379 tables"); a client needs what it does for the venue.
# A service missing from here fails the run rather than falling back to the architect's sentence.
CLIENT_TEXT = {
    "IdentityService": ("Sign-in and people", "Staff and guest accounts, sign-in, roles and permissions, and personal-data requests.",
                        "Nobody can sign in, so everything stops."),
    "TenancyService": ("Organisation and settings", "Your organisation, regions, venues, outlets and tills, and the settings each one uses.",
                       "Nothing can find its venue or settings, so everything stops."),
    "CatalogueService": ("Products and pricing", "What is sold, at what price and when: products, events and sessions, price lists, "
                         "promotions, bundles and seating.", "Tills keep selling from their last published catalogue; changes wait."),
    "OrderService": ("Sales and payments", "Baskets, orders, payments, refunds, and opening and closing cashier shifts.",
                     "No new sales can be taken. This service has the highest availability target."),
    "AccessService": ("Entry and admission", "Tickets and passes at the gate, admission rules and entry validation.",
                      "Gates fall back to their local copy of what is valid."),
    "LedgerService": ("Finance", "The financial record of every sale, refund and payment, and currency rates.",
                      "Finance postings wait until it returns; trading is not affected."),
    "WalletService": ("Wallets and credit", "Guest wallets, stored credit, gift cards and membership credit.",
                      "Wallet balances cannot be spent until it returns."),
    "InventoryService": ("Stock", "Stock levels, counting and purchasing.", "Receiving and counting pause; selling continues."),
    "FnbService": ("Food and beverage", "Menus, table service, kitchen screens and food orders.",
                   "Kitchens fall back to printed tickets."),
    "VenueOpsService": ("Venue operations", "Queues and wait times, maintenance, bookable resources, the venue map and media.",
                        "Venue operations degrade; selling and entry continue."),
    "RetailService": ("Retail", "Merchandise, shop sales, returns and shop-and-drop.", "The shop stops; gates and restaurants do not."),
    "MarketingService": ("Guests and marketing", "Guest profiles, consent, loyalty, campaigns, forms and support.",
                         "Campaigns and guest look-up pause; trading continues."),
    "AiService": ("AI assistance", "Suggestions and the guest concierge.", "Suggestions stop; nothing that takes money depends on it."),
    "PlatformService": ("Subscription and platform", "Your subscription, licensed modules and platform administration.",
                        "Provisioning and administration pause; trading continues."),
    "WhiteLabelService": ("Branding", "Your brand, theme, pages, navigation and content in the guest web and mobile app.",
                          "Guests keep seeing the last published version."),
    "ReportingService": ("Reporting", "Dashboards, reports and alerts.", "Dashboards pause; nothing operational depends on them."),
    "CrossRegionService": ("Cross-region", "Entitlements that work across regions.", "Each region continues on its own."),
}



def points_of(raw: float) -> int:
    """Relative size, 1-2-3-5-8. The thresholds are the one tunable in the scorer; change them here only."""
    for p, lim in ((1, 2.5), (2, 4.5), (3, 7), (5, 11)):
        if raw <= lim:
            return p
    return 8

# ---- loading ------------------------------------------------------------------------------------

def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


CONTRACTS: dict[Path, dict] = {}


def contract(p: Path) -> dict:
    p = p.resolve()
    if p not in CONTRACTS:
        CONTRACTS[p] = load_yaml(p)
    return CONTRACTS[p]


def resolve(node, base: Path):
    """Follow a $ref (local or cross-file) to (node, file it lives in, name)."""
    name = None
    hops = 0
    while isinstance(node, dict) and "$ref" in node and hops < 8:
        ref = node["$ref"]
        file_part, _, frag = ref.partition("#")
        target = (base.parent / file_part).resolve() if file_part else base.resolve()
        cur = contract(target)
        for part in frag.strip("/").split("/"):
            cur = cur[part]
        node, base, name = cur, target, frag.rsplit("/", 1)[-1]
        hops += 1
    return node, base, name


def first_sentence(text, limit=200) -> str:
    if not text:
        return ""
    t = re.sub(r"\*\*|`", "", str(text)).replace("\n", " ").strip()
    t = re.sub(r"\s+", " ", t)
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    t = m.group(1) if m else t
    return t if len(t) <= limit else t[: limit - 1].rstrip() + "…"


def cell(text) -> str:
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


# ---- schemas to field rows ----------------------------------------------------------------------

def type_of(node, base: Path) -> str:
    node_r, _, name = resolve(node, base)
    if not isinstance(node_r, dict):
        return "any"
    if "enum" in node_r:
        vals = [str(v) for v in node_r["enum"]]
        shown = ", ".join(vals[:8]) + (", …" if len(vals) > 8 else "")
        return f"{name + ': ' if name else ''}enum ({shown})"
    for k in ("oneOf", "anyOf"):
        if k in node_r:
            alts = [resolve(a, base)[2] or type_of(a, base) for a in node_r[k]]
            return " or ".join(a for a in alts if a)
    t = node_r.get("type")
    if isinstance(t, list):
        t = "/".join(x for x in t if x != "null")
    if t == "array":
        return f"array of {type_of(node_r.get('items', {}), base)}"
    if name and (t == "object" or "properties" in node_r or "allOf" in node_r):
        return name
    fmt = node_r.get("format")
    return f"{t or 'object'}{' (' + fmt + ')' if fmt else ''}"


def constraints(n: dict) -> str:
    bits = []
    for k, label in (("minimum", "min"), ("maximum", "max"), ("minLength", "min length"),
                     ("maxLength", "max length"), ("minItems", "min items"), ("maxItems", "max items"),
                     ("pattern", "pattern"), ("default", "default")):
        if k in n:
            bits.append(f"{label} {n[k]}")
    if n.get("readOnly"):
        bits.append("read-only")
    if n.get("nullable") or (isinstance(n.get("type"), list) and "null" in n["type"]):
        bits.append("nullable")
    return "; ".join(bits)


def merged(node, base: Path, seen: frozenset):
    """Properties and required set of an object, with allOf flattened."""
    node, base, _ = resolve(node, base)
    props, req = {}, set()
    if not isinstance(node, dict):
        return props, req, base
    for part in node.get("allOf") or []:
        p2, r2, _ = merged(part, base, seen)
        props.update({k: (v, b) for k, (v, b) in p2.items()})
        req |= r2
    for k, v in (node.get("properties") or {}).items():
        props[k] = (v, base)
    req |= set(node.get("required") or [])
    return props, req, base


def field_rows(node, base: Path, prefix="", depth=0, seen=frozenset()) -> list[tuple]:
    rows = []
    _, _, name = resolve(node, base)
    if name and name in seen:
        return rows
    seen = seen | ({name} if name else set())
    props, req, _ = merged(node, base, seen)
    for k, (v, b) in props.items():
        vr, vb, vname = resolve(v, b)
        if not isinstance(vr, dict):
            continue
        full = prefix + k
        rows.append((full, type_of(v, b), "yes" if k in req else "",
                     " ".join(x for x in (first_sentence(vr.get("description") or (v.get("description") if isinstance(v, dict) else "")),
                                           f"({constraints(vr)})" if constraints(vr) else "") if x)))
        if depth + 1 >= MAX_DEPTH:
            continue
        if vr.get("type") == "array":
            it, ib, iname = resolve(vr.get("items", {}), vb)
            if isinstance(it, dict) and (it.get("properties") or it.get("allOf")) and iname not in seen:
                rows += field_rows(vr["items"], vb, full + "[].", depth + 1, seen)
        elif (vr.get("properties") or vr.get("allOf")) and vname not in seen:
            rows += field_rows(v, b, full + ".", depth + 1, seen)
    return rows


# ---- contracts to operations --------------------------------------------------------------------

def read_operations() -> dict[str, dict]:
    ops = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        c = contract(f)
        tag_desc = {t["name"]: t.get("description", "") for t in c.get("tags") or []}
        for path, item in (c.get("paths") or {}).items():
            shared_params = item.get("parameters") or []
            for verb, op in item.items():
                if not isinstance(op, dict) or "operationId" not in op:
                    continue
                params = []
                for p in shared_params + (op.get("parameters") or []):
                    pr, pb, _ = resolve(p, f)
                    params.append((pr.get("name"), pr.get("in"), "yes" if pr.get("required") else "",
                                   type_of(pr.get("schema", {}), pb), first_sentence(pr.get("description"))))
                body = []
                rb = op.get("requestBody")
                if rb:
                    rbr, rbb, _ = resolve(rb, f)
                    sch = ((rbr.get("content") or {}).get("application/json") or {}).get("schema")
                    if sch:
                        body = field_rows(sch, rbb)
                        body_type = resolve(sch, rbb)[2]
                    else:
                        body_type = next(iter(rbr.get("content") or {}), "")
                else:
                    body_type = ""
                responses, success = [], []
                success_type, success_schema = "", None
                for code, r in (op.get("responses") or {}).items():
                    rr, rbase, rname = resolve(r, f)
                    responses.append((str(code), rname or "", first_sentence(rr.get("description"))))
                    if str(code).startswith("2") and not success:
                        content = rr.get("content") or {}
                        sch = next((v.get("schema") for v in content.values() if v.get("schema")), None)
                        if sch:
                            success = field_rows(sch, rbase)
                            success_type = resolve(sch, rbase)[2] or type_of(sch, rbase)
                            success_schema = (sch, rbase)
                tag = (op.get("tags") or ["general"])[0]
                ops[op["operationId"]] = {
                    "contract": f.stem, "file": f.relative_to(ROOT).as_posix(),
                    "verb": verb.upper(), "path": path, "tag": tag,
                    "tagDescription": first_sentence(tag_desc.get(tag)),
                    "summary": op.get("summary", ""),
                    "description": (op.get("description") or "").strip(),
                    "permission": op.get("x-ticvai-permission"),
                    "scopeLevel": op.get("x-ticvai-scope-level"),
                    "configScope": op.get("x-ticvai-config-scope"),
                    "offline": op.get("x-ticvai-offline-capable"),
                    "offlineNote": op.get("x-ticvai-offline-note"),
                    "conflict": op.get("x-ticvai-conflict-policy"),
                    "routing": op.get("x-ticvai-read-routing"),
                    "stepUp": op.get("x-ticvai-step-up"),
                    "lock": op.get("x-ticvai-lock"),
                    "guestCallable": op.get("x-ticvai-guest-callable"),
                    "provisional": bool(op.get("x-ticvai-provisional")),
                    "params": params, "body": body, "bodyType": body_type,
                    "responses": responses, "success": success, "successType": success_type,
                    "successSchema": success_schema,
                    "creates": any(c == "201" for c, _, _ in responses),
                }
    return ops


# ---- state models -------------------------------------------------------------------------------
# Audit R181: the status a create starts in lives in states/*.yaml, and nothing a developer reads from
# the slice showed it, so "what status does a new asset start in" went unanswered even where the
# package answers it. Each operation's page now says which state model it touches, the state a create
# starts in and the moves it makes, and a create that the model also lists as a move out of its initial
# state is logged as a gap, because the status it returns is then not settled.

def read_state_models() -> dict[tuple[str, str], dict]:
    """Every states/*.yaml, keyed by (contract, enum): enum is a schema name for a named enum and
    Schema.property for one declared inline, as tools/check-states.py keys them."""
    models = {}
    for f in sorted((ROOT / "states").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        d = load_yaml(f) or {}
        if d.get("contract") and d.get("enum"):
            d["_file"] = f.relative_to(ROOT).as_posix()
            models[(d["contract"], str(d["enum"]))] = d
    return models


def enum_named(node, base: Path):
    """(contract, schema name) of the named enum a property points at, through $ref or a one-ref allOf."""
    if not isinstance(node, dict):
        return None
    if "$ref" in node:
        r, rb, name = resolve(node, base)
        if isinstance(r, dict) and "enum" in r and name:
            return rb.stem, name
        return None
    for part in node.get("allOf") or []:
        hit = enum_named(part, base)
        if hit:
            return hit
    return None


def entity_models(x: dict, models: dict) -> list[dict]:
    """State models whose status field sits at the top level of the operation's success response,
    that is, the models of the entity the operation returns."""
    if not x.get("successSchema"):
        return []
    sch, base = x["successSchema"]
    _, sbase, sname = resolve(sch, base)
    props, _, _ = merged(sch, base, frozenset())
    out = []
    for pname, (v, b) in props.items():
        hit = enum_named(v, b)
        if hit and hit in models:
            out.append(models[hit])
            continue
        vr, _, _ = resolve(v, b)
        if sname and isinstance(vr, dict) and "enum" in vr and (sbase.stem, f"{sname}.{pname}") in models:
            out.append(models[(sbase.stem, f"{sname}.{pname}")])
    return out


def state_facts(o: str, x: dict, models: dict, by_op: dict) -> tuple[list[str], list[str]]:
    """What the operation's page says about state (one line per model), and the state-model gaps it shows."""
    lines, gaps = [], []
    touched = {m["_file"]: m for m in by_op.get(o, [])}
    created = {m["_file"]: m for m in entity_models(x, models)} if x.get("creates") else {}
    for f in sorted(set(touched) | set(created)):
        m = touched.get(f) or created[f]
        initial = [str(v) for v in m.get("initial") or []]
        moves = [t for t in m.get("transitions") or [] if t.get("operation") == o]
        bits = []
        ambiguous = False
        if f in created:
            bits.append("created as " + " or ".join(f"`{v}`" for v in initial) if initial else
                        "created, but the model names no initial state")
            # A move into another initial state is a record created already advanced (the model allows
            # several initial states for that); a move out to a non-initial state leaves the result open.
            out_of_initial = [t for t in moves if t.get("from") in initial and t.get("to") not in initial]
            if out_of_initial:
                ambiguous = True
                gaps.append(f"creates {m.get('entity')} in {', '.join(initial)}, but {f} also makes it the "
                            + ", ".join(f"{t['from']} -> {t['to']}" for t in out_of_initial)
                            + " transition, so the status it returns is not settled")
        if moves:
            bits.append("moves " + ", ".join(f"`{t.get('from')}` -> `{t.get('to')}`" for t in moves))
        lines.append(f"{m.get('entity')} ([{f}](../../../{f})): " + "; ".join(bits)
                     + (" **(not settled: see the Gaps sheet)**" if ambiguous else ""))
    return lines, gaps


# ---- DDL to migrations --------------------------------------------------------------------------

def read_ddl() -> dict[str, dict]:
    """Every table in backend/, from the derived SQL: which file declares it, its columns, and the
    tables its foreign keys point at. The SQL is the storage truth (backend/MIGRATIONS.md), so the
    migration plan is read from it rather than from the contracts' persistence notes."""
    tables: dict[str, dict] = {}
    for db in ("tenant", "control"):
        for f in sorted((ROOT / "backend" / db).glob("010-*.sql")):
            name, cols_ = None, []
            for line in f.read_text(encoding="utf-8").splitlines():
                m = re.match(r'CREATE TABLE IF NOT EXISTS (\w+)\."?(\w+)"? \(', line)
                if m:
                    name, cols_ = f"{m.group(1)}.{m.group(2)}", []
                    continue
                if name and line.startswith(");"):
                    tables[name] = {"db": db, "file": f.relative_to(ROOT).as_posix(), "columns": cols_,
                                    "fks": set()}
                    name = None
                    continue
                m = re.match(r"\s+(\w+)\s+(.+?),?$", line)
                if name and m:
                    cols_.append((m.group(1), m.group(2).rstrip(",")))
        fk = ROOT / "backend" / db / "900-foreign-keys.sql"
        if fk.exists():
            text = fk.read_text(encoding="utf-8").replace('"', "")
            for m in re.finditer(r"ALTER TABLE (\w+\.\w+) ADD CONSTRAINT \w+ FOREIGN KEY \(\w+\) "
                                 r"REFERENCES (\w+\.\w+)", text):
                if m.group(1) in tables:
                    tables[m.group(1)]["fks"].add(m.group(2))
    for t in tables.values():
        names = {c for c, _ in t["columns"]}
        t["rls"] = ("scope_path" if "scope_path" in names else
                    "venue_id" if "venue_id" in names else "")
        # ADR-0044: a NOT NULL venue_id is what makes a table partition by venue.
        t["partitioned"] = any(c == "venue_id" and "NOT NULL" in d for c, d in t["columns"])
    return tables


def schema_order(edges: dict[str, dict[str, int]]) -> tuple[list[str], dict[str, int]]:
    """Schemas in the order their migrations run. `edges[a][b]` is how many foreign keys in schema a
    point into schema b. Each step takes the schema with the fewest keys into schemas not yet created
    (ties: the one most referenced by what is left, so anchors such as platform go early). Keys into a
    schema created later cannot be declared in the same migration; they are counted per schema and
    added in one last migration, the way backend/tenant/900-foreign-keys.sql adds them after the tables."""
    left, done, order, deferred = set(edges), set(), [], {}
    while left:
        def unmet(s):
            return sum(n for t, n in edges[s].items() if t != s and t not in done)

        def wanted(s):
            return sum(edges[o].get(s, 0) for o in left if o != s)
        s = min(sorted(left), key=lambda x: (unmet(x), -wanted(x)))
        if unmet(s):
            deferred[s] = unmet(s)
        order.append(s)
        done.add(s)
        left.discard(s)
    return order, deferred


# ---- screens ------------------------------------------------------------------------------------

def screen_file(code: str):
    f = next((ROOT / "screens").glob(f"{code}-*.yaml"))
    return load_yaml(f)


def all_screens() -> dict[str, dict]:
    out = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = load_yaml(f)
        for s in doc["screens"]:
            s["_platform"] = doc["platform"]
            out[s["id"]] = s
    return out


# ---- writing ------------------------------------------------------------------------------------

def table(head: list[str], rows: list) -> list[str]:
    if not rows:
        return []
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return out


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> int:
    sl = json.loads((HANDOFF / "delivery-slice.json").read_text(encoding="utf-8"))
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    decomp = json.loads((HANDOFF / "service-decomposition.json").read_text(encoding="utf-8"))
    ref = json.loads((HANDOFF / "schema-reference.json").read_text(encoding="utf-8"))
    cols = ref["cols"]
    services = decomp["services"]
    tiers = decomp["tiers"]
    ops = read_operations()
    screens = all_screens()
    state_models = read_state_models()
    models_by_op: dict[str, list[dict]] = defaultdict(list)
    for m in state_models.values():
        for o in sorted({t.get("operation") for t in m.get("transitions") or [] if t.get("operation")}):
            models_by_op[o].append(m)
    state_gaps: list[tuple[str, str]] = []
    slice_ops = sl["operations"]
    plat = sl["platforms"]

    missing = [o for o in slice_ops if o not in ops]
    if missing:
        print(f"ERROR: slice names {len(missing)} operations no contract declares: {missing[:5]}")
        return 1

    schema_owner = {s: n for n, d in services.items() for s in d.get("schemas") or []}

    def owner_of(table_name: str) -> str | None:
        return schema_owner.get(table_name.split(".")[0])

    # Wave of an operation = earliest first-release screen that calls it. A setup operation takes
    # the wave of the earliest core operation that reads a table it makes non-empty.
    screen_wave = {sid: screens[sid].get("wave") for k in plat for sid in plat[k]["screens"]}
    wave: dict[str, int] = {}
    for o, d in slice_ops.items():
        ws = [screen_wave[s] for s in d["screens"] if screen_wave.get(s)]
        if d["part"] == "core" and ws:
            wave[o] = min(ws)
    readers = defaultdict(set)
    for o in slice_ops:
        for t in lineage[o].get("reads") or []:
            readers[t].add(o)
    for _ in range(4):
        for o, d in slice_ops.items():
            if o in wave:
                continue
            cand = [wave[r] for t in d["enables"] for r in readers[t] if r in wave]
            if cand:
                wave[o] = min(cand)
    for o in slice_ops:
        wave.setdefault(o, 1)

    by_service: dict[str, list[str]] = defaultdict(list)
    for o, d in sorted(slice_ops.items()):
        by_service[d["service"]].append(o)

    OUT.mkdir(exist_ok=True)
    (OUT / "frontend").mkdir(exist_ok=True)
    (OUT / "backend").mkdir(exist_ok=True)

    # ---------------------------------------------------------------- README (architecture)
    matrix = defaultdict(lambda: defaultdict(int))
    for o, d in slice_ops.items():
        for p in d["platforms"]:
            matrix[d["service"]][p] += 1
    keys = list(plat)
    L = ["# TICVAI first release: architecture, frontend and backend", "",
         "> Generated by `tools/build-service-docs.py` from the contracts, screens and "
         "`handoff/delivery-slice.json`. **Do not edit.** Re-run after any contract or screen change.", "",
         f"The first release is four platforms, {sum(len(p['screens']) for p in plat.values())} screens "
         f"and **{len(slice_ops)} of {sl['counts']['allOperations']} operations** across "
         f"{len(by_service)} services. {sl['counts']['core']} operations are called by a first-release "
         f"screen (core). {sl['counts']['setup']} are Back Office and Admin operations that create the "
         "data those screens read (setup).", "",
         "## How it fits together", "",
         "```mermaid", "flowchart LR"]
    for k, p in plat.items():
        L.append(f'  {k}["{p["name"]}<br/>{len(p["screens"])} screens"]')
    for tier in tiers:
        L.append(f'  subgraph {tier}')
        for n, d in services.items():
            if d.get("tier") == tier and n in by_service:
                L.append(f'    {n}["{n}<br/>{len(by_service[n])} ops"]')
        L.append("  end")
    for n in by_service:
        for k in keys:
            if matrix[n][k]:
                L.append(f"  {k} --> {n}")
    L += ["```", "",
          "Every app talks only to services. Services own their tables (one PostgreSQL schema each) and "
          "read another service's data only through its operations or its published events.", "",
          "## Platform x service", "",
          "Operations each platform calls, by the service that owns them. Setup operations are counted "
          "separately because no first-release screen calls them.", ""]
    rows = []
    for n in sorted(by_service, key=lambda n: -len(by_service[n])):
        setup = sum(1 for o in by_service[n] if slice_ops[o]["part"] == "setup")
        rows.append([f"[{n}](backend/{n}.md)", services[n].get("tier", "")] +
                    [matrix[n][k] or "" for k in keys] + [setup or "", len(by_service[n]),
                                                          sl["services"][n]["total"]])
    L += table(["Service", "Tier"] + [plat[k]["name"] for k in keys] +
               ["Setup", "In slice", "All operations"], rows)
    L += ["", "## Tiers", ""]
    L += table(["Tier", "What it means"], [[t, d] for t, d in tiers.items()])
    L += ["", "## Frontend", ""]
    L += table(["Platform", "Screens", "Runtime", "Offline"],
               [[f"[{p['name']}](frontend/{k}.md)", len(p["screens"]),
                 screens[p["screens"][0]]["_platform"].get("runtime", ""),
                 "yes" if screens[p["screens"][0]]["_platform"].get("offlineCapable") else "no"]
                for k, p in plat.items()])
    L += ["", "## Backend build plan and migrations", "",
          "The database migrations, in the order they run, and every table the first release needs are in "
          "[backend/MIGRATIONS.md](backend/MIGRATIONS.md). The whole backend plan (tasks in build order, "
          "services, operations, API schemas, tables and migrations) is `TICVAI_Backend_Build_Plan.xlsx`.", ""]
    L += ["", "## Services are frozen at 1.0.0, then extended", "",
          "A service is finished for the first release when every operation in its slice is built and "
          "its contract is published at `1.0.0`. After that:", "",
          "- **Additive, 1.x:** a new operation, a new optional field, a new table with a new migration. Nothing already built changes.",
          "- **Breaking, 2.0.0:** renaming or removing a field, or making an optional field required. Needs a deprecation window.",
          "", "Each backend page lists what is *not* in the slice, which is what later releases add.", "",
          "## Known gaps in the slice", "",
          f"**Read but written only by another platform's trading ({len(sl['fedElsewhere'])} tables).** "
          "The screen ships and shows an empty state until that platform exists.", ""]
    L += table(["Table", "Written by"], [[f"`{t}`", ", ".join(f"`{w}`" for w in ws[:5])]
                                         for t, ws in sl["fedElsewhere"].items()])
    L += ["", f"**Read but written by no operation ({len(sl['noWriter'])} tables).** Most are child rows "
          "written inside their parent's operation and missing from the lineage. Four are real contract "
          "gaps, logged as L1-L4 in `docs/active/action-register-22-september.md`.", "",
          ", ".join(f"`{t}`" for t in sl["noWriter"]), ""]
    # Audit R174: setup operations no screen lists in its apis. The backend pages used to say "setup
    # through Back Office" for operations no Back Office screen calls.
    screenless = sorted(o for o, d in slice_ops.items() if d["part"] == "setup" and not d["screens"])
    if screenless:
        L += [f"**Setup operations no screen calls ({len(screenless)}).** No screen lists them in its apis and "
              "no contract marks them consumed, so they are reachable only by API or import. Each needs a screen "
              "that binds it, or its contract to say it is API-only.", ""]
        L += table(["Operation", "Service", "Makes non-empty"],
                   [[f"[`{o}`](backend/{slice_ops[o]['service']}.md#{o.lower()})", slice_ops[o]["service"],
                     ", ".join(f"`{t}`" for t in slice_ops[o]["enables"])] for o in screenless])
        L += [""]
    (OUT / "README.md").write_text("\n".join(L), encoding="utf-8")

    # ---------------------------------------------------------------- frontend
    for k, p in plat.items():
        pf = screens[p["screens"][0]]["_platform"]
        L = [f"# {p['name']}: screens", "",
             "> Generated by `tools/build-service-docs.py`. **Do not edit.**", ""]
        dep = pf.get("deployment") or {}
        L += table(["", ""], [["Audience", pf.get("audience", "")], ["Runtime", pf.get("runtime", "")],
                              ["App", pf.get("app", "")], ["Offline", "yes" if pf.get("offlineCapable") else "no"],
                              ["Themes", ", ".join(pf.get("themes") or [])],
                              ["Directions", ", ".join(pf.get("directions") or [])],
                              ["Packages", ", ".join(pf.get("packages") or [])]] +
                   [[k2, v] for k2, v in dep.items() if isinstance(v, (str, int, bool))])
        if k == "WL":
            L += ["", "White Labelling is a module, not an app. Its screens live in the CMS (P13) and "
                  "the Platform Admin Console (P09)."]
        L += ["", "## Screens", ""]
        L += table(["ID", "Screen", "Module", "Wave", "Operations"],
                   [[f"[{sid}](#{slug(sid + ' ' + screens[sid]['name'])})", screens[sid]["name"],
                     screens[sid].get("module", ""), screens[sid].get("wave", ""),
                     len([a for a in screens[sid].get("apis") or [] if a.get("operationId")])]
                    for sid in sorted(p["screens"], key=lambda s: (screens[s].get("wave") or 9, s))])
        for sid in sorted(p["screens"], key=lambda s: (screens[s].get("wave") or 9, s)):
            s = screens[sid]
            L += ["", f"## {sid} {s['name']}", "",
                  f"**{s.get('purpose') or ''}**", ""]
            imp = s.get("implementation") or {}
            L += table(["", ""], [["Module", s.get("module", "")], ["Wave", s.get("wave", "")],
                                  ["Licensed module", s.get("requiresModule", "")],
                                  ["Route", f"`{imp.get('route', '')}`"],
                                  ["Component", f"`{imp.get('component', '')}`"],
                                  ["Pattern", s.get("pattern", "")]])
            es = s.get("entryState") or {}
            if es.get("params"):
                L += ["", "**Entry parameters**", ""]
                L += table(["Parameter", "From"], [[x.get("name"), x.get("from")] for x in es["params"]])
            apis = [a for a in s.get("apis") or [] if a.get("operationId")]
            if apis:
                L += ["", "**Operations**", ""]
                L += table(["Operation", "Service", "When", "Purpose", "Permission"],
                           [[f"`{a['operationId']}`",
                             f"[{lineage.get(a['operationId'], {}).get('service', '')}](../backend/"
                             f"{lineage.get(a['operationId'], {}).get('service', '')}.md#{a['operationId'].lower()})",
                             a.get("trigger", ""), a.get("purpose", ""),
                             f"`{ops.get(a['operationId'], {}).get('permission', '')}`"] for a in apis])
            st = s.get("states") or {}
            if st:
                L += ["", "**States**", ""]
                L += table(["State", "Behaviour"], [[n, re.sub(r"\*\*", "", str(v))] for n, v in st.items()])
            nav = (s.get("navigation") or {}).get("transitions") or []
            if nav:
                L += ["", "**Goes to**", ""]
                L += table(["To", "Trigger", "Carries", "Guard"],
                           [[t.get("to"), t.get("trigger", ""), ", ".join(t.get("carries") or []),
                             t.get("guard") or t.get("precondition") or ""] for t in nav])
        (OUT / "frontend" / f"{k}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- backend
    for n, olist in by_service.items():
        d = services[n]
        L = [f"# {n}", "", "> Generated by `tools/build-service-docs.py`. **Do not edit.**", ""]
        L += table(["", ""], [["Tier", f"{d.get('tier')}: {tiers.get(d.get('tier'), '')}"],
                              ["Contracts", ", ".join(f"`{c}`" for c in d.get("contracts") or [])],
                              ["Schemas owned", ", ".join(f"`{s}`" for s in d.get("schemas") or [])],
                              ["Operations in the slice", f"{len(olist)} of {sl['services'][n]['total']}"],
                              ["Scale", re.sub(r"\*\*", "", d.get("scale", ""))],
                              ["If it is down", re.sub(r"\*\*", "", d.get("risk", ""))]])
        L += ["", "## Why this is a service", "", d.get("why", ""), ""]
        own_tables = sorted({t for o in olist for t in (lineage[o].get("reads") or []) + (lineage[o].get("writes") or [])
                             if not t.startswith("cache:") and owner_of(t) == n})
        foreign = defaultdict(set)
        for o in olist:
            for t in lineage[o].get("reads") or []:
                ow = owner_of(t)
                if ow and ow != n and not t.startswith("cache:"):
                    foreign[ow].add(t)
        L += ["## Depends on", ""]
        L += table(["Service", "Tables it reads"], [[f"[{s}]({s}.md)", ", ".join(f"`{t}`" for t in sorted(ts))]
                                                    for s, ts in sorted(foreign.items())]) or ["Nothing outside itself."]
        groups = defaultdict(list)
        for o in olist:
            groups[ops[o]["tag"]].append(o)
        L += ["", "## Operations in the first release", ""]
        L += table(["Group", "Operation", "Method", "Path", "Part", "Wave", "Called by"],
                   [[g, f"[`{o}`](#{o.lower()})", ops[o]["verb"], f"`{ops[o]['path']}`",
                     slice_ops[o]["part"], wave[o], ", ".join(slice_ops[o]["screens"][:6]) +
                     (" …" if len(slice_ops[o]["screens"]) > 6 else "")]
                    for g in sorted(groups) for o in sorted(groups[g])])
        for g in sorted(groups):
            L += ["", f"## Group: {g}", ""]
            if ops[groups[g][0]]["tagDescription"]:
                L += [ops[groups[g][0]]["tagDescription"], ""]
            for o in sorted(groups[g]):
                x, lin, so = ops[o], lineage[o], slice_ops[o]
                L += [f"### {o}", "", f"**`{x['verb']} {x['path']}`**: {x['summary']}", ""]
                if x["description"]:
                    L += [x["description"], ""]
                facts = [["Permission", f"`{x['permission']}`"], ["Scope level", x["scopeLevel"]],
                         ["Part of slice", so["part"] + (f", makes {', '.join('`' + t + '`' for t in so['enables'])} non-empty"
                                                          if so["enables"] else "")],
                         ["Wave", wave[o]], ["Offline", "yes" if x["offline"] else "no"]]
                for label, key in (("Config scope", "configScope"), ("Conflict policy", "conflict"),
                                   ("Read routing", "routing"), ("Step-up auth", "stepUp"),
                                   ("Lock", "lock"), ("Guest callable", "guestCallable"),
                                   ("Offline note", "offlineNote")):
                    if x.get(key):
                        facts.append([label, first_sentence(x[key], 300) if key == "offlineNote" else x[key]])
                if x["provisional"]:
                    facts.append(["Status", "**Provisional**: not yet agreed; do not build"])
                facts.append(["Reads", ", ".join(f"`{t}`" for t in lin.get("reads") or []) or "-"])
                facts.append(["Writes", ", ".join(f"`{t}`" for t in lin.get("writes") or []) or "-"])
                # Audit R174: an operation no screen lists in its apis has no Back Office screen to set it up
                # through either, so the page says what is true until a screen binds it.
                facts.append(["Called by", ", ".join(so["screens"]) or
                              "**no screen**: no screen lists it in its apis, so it is reachable only by API or "
                              "import until one does (README, Known gaps)"])
                st_lines, st_gaps = state_facts(o, x, state_models, models_by_op)
                if st_lines:
                    facts.append(["State model", "<br/>".join(st_lines)])
                state_gaps += [(o, g) for g in st_gaps]
                L += table(["", ""], facts)
                if x["params"]:
                    L += ["", "**Parameters**", ""]
                    L += table(["Name", "In", "Required", "Type", "Notes"], x["params"])
                if x["body"]:
                    L += ["", f"**Request body**{': `' + x['bodyType'] + '`' if x['bodyType'] else ''}", ""]
                    L += table(["Field", "Type", "Required", "Notes"], x["body"])
                if x["success"]:
                    L += ["", f"**Response**{': `' + x['successType'] + '`' if x['successType'] else ''}", ""]
                    L += table(["Field", "Type", "Required", "Notes"], x["success"])
                L += ["", "**Responses**", ""]
                L += table(["Code", "Shape", "Meaning"], x["responses"])
                L += [""]
        if own_tables:
            L += ["## Tables", "", "Every table this service owns that the slice reads or writes, with "
                  "its columns as derived into `backend/tenant/*.sql`.", ""]
            for t in own_tables:
                c = cols.get(t) or []
                L += [f"### `{t}`", ""]
                L += table(["Column", "Type", "Required", "Notes"],
                           [[x["column"], x["type"], x["required"], first_sentence(x.get("description"))] for x in c]) or ["Columns not derived."]
                L += [""]
        later = sorted(o for o, lin in lineage.items() if lin.get("service") == n and o not in slice_ops)
        L += ["## Not in the first release", "",
              f"{len(later)} operations, added to this service in later releases without changing any of the above.", ""]
        lg = defaultdict(list)
        for o in later:
            lg[ops[o]["tag"] if o in ops else "other"].append(o)
        L += table(["Group", "Operations"], [[g, ", ".join(f"`{o}`" for o in v)] for g, v in sorted(lg.items())])
        (OUT / "backend" / f"{n}.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------------------------------------------------------------- client summary
    C = ["# TICVAI first release: what is being built", "",
         "This summary describes the four parts of the first release and the back-end services behind "
         "them. It is generated from the same specification the development team builds from.", "",
         "## The four parts", ""]
    for k, p in plat.items():
        waves = defaultdict(int)
        for sid in p["screens"]:
            waves[screens[sid].get("wave")] += 1
        mods = sorted({screens[sid].get("module") for sid in p["screens"] if screens[sid].get("module")})
        C += [f"### {p['name']}", "",
              f"{len(p['screens'])} screens: " + ", ".join(f"{v} in wave {w}" for w, v in sorted(waves.items(), key=lambda x: x[0] or 9)) + ".", "",
              "Areas covered: " + ", ".join(mods) + ".", ""]
    C += ["## The services behind them", "",
          f"The four parts share {len(by_service)} back-end services. Each looks after one area of the "
          "business and owns its own area of the data. They run separately, so most can be unavailable "
          "without stopping the others; the table says what happens if each one is.", ""]
    unknown = sorted(set(by_service) - set(CLIENT_TEXT))
    if unknown:
        print(f"ERROR: no client description for {unknown}; add them to CLIENT_TEXT")
        return 1
    order = sorted(by_service, key=lambda n: list(tiers).index(services[n].get("tier", "platform")))
    C += table(["Service", "What it looks after", "If it is unavailable"],
               [[CLIENT_TEXT[n][0], CLIENT_TEXT[n][1], CLIENT_TEXT[n][2]] for n in order])
    C += ["", "## How the work grows", "",
          "Each service is built first for what these four parts need, then published as a fixed version. "
          "Later releases add to it without changing what has already been delivered, so the four parts "
          "keep working while the platform grows.", ""]
    (OUT / "client-summary.md").write_text("\n".join(C), encoding="utf-8")

    # ---------------------------------------------------------------- tasks
    # **Points, not hours.** Nobody has timed this team on this code, so a task carries a relative size
    # computed from the spec, and hours come later from what the first fortnight actually took
    # (docs/active/developer-assignment-plan-23-september.md). One formula for every task, so two
    # tasks of the same points are comparable whoever scored them.
    team = json.loads(TEAM.read_text(encoding="utf-8")) if TEAM.exists() else {"areas": {}, "onboard": {}}
    areas = team.get("areas") or {}
    tasks = []

    # **Frontend or backend is on every task, and in its OpenProject subject**, so a board, a filter or a
    # person scanning a list can tell them apart without opening the ticket.
    PREFIX = {"Frontend": "[FE]", "Backend": "[BE]", "Database": "[DB]", "DevOps": "[DevOps]",
              "Onboarding": "[Onboarding]", "Full stack": "[FE+BE]", "Setup": "[Setup]"}

    def track_of(key, area):
        if key.startswith(("MIG", "VM-MIG", "VM-DB")):
            return "Database"
        if key == "SETUP":
            return "Setup"
        if key == "VM":
            return "Full stack"
        if area == "VM":
            return "Frontend" if key.startswith(("VM-BO-", "VM-FE")) else "Backend"
        return {"devops": "DevOps", "onboard": "Onboarding", "backend": "Backend"}.get(area, "Frontend")

    by_key: dict[str, dict] = {}

    def task(key, parent, typ, subject, desc, wave_, platform="", service="", depends=(), pts="",
             area="", assignee=""):
        tr = track_of(key, area)
        t_ = {"key": key, "parent": parent, "type": typ, "track": tr,
              "subject": f"{PREFIX[tr]} {subject}"[:255],
              "wave": wave_, "points": pts, "assignee": assignee, "area": area,
              "platform": platform, "service": service,
              "dependsOn": " ".join(sorted(set(depends))), "description": desc,
              "phase": 2 if key == "VM" or key.startswith("VM-") else 1}
        tasks.append(t_)
        by_key[key] = t_

    step: dict[str, int] = {}

    def step_of(k, seen=()):
        """How many tasks stand in front of this one along its longest dependency chain."""
        if k in step:
            return step[k]
        if k not in by_key:
            return 0
        deps = [d for d in (by_key[k]["dependsOn"] or "").split() if d in by_key and d not in seen]
        step[k] = 1 + max((step_of(d, seen + (k,)) for d in deps), default=0)
        return step[k]

    def deps_step(deps):
        return 1 + max((step_of(d) for d in deps), default=0)

    def op_raw(o):
        x, lin = ops[o], lineage[o]
        fields = len(x["body"]) + len(x["success"]) + len(x["params"])
        writes = [t for t in lin.get("writes") or [] if not t.startswith("cache:")]
        cross = {owner_of(t) for t in lin.get("reads") or []
                 if not t.startswith("cache:") and owner_of(t) not in (None, lin.get("service"))}
        return (1 + min(fields, 60) / 20 + 0.5 * len(writes) + 0.5 * len(cross)
                + (1 if x["lock"] else 0) + (1 if x["offline"] else 0) + (0.5 if x["stepUp"] else 0))

    def screen_raw(s):
        comps = sum(len(r.get("components") or []) for r in (s.get("layout") or {}).get("regions") or [])
        apis_ = [a for a in s.get("apis") or [] if a.get("operationId")]
        nav = len((s.get("navigation") or {}).get("transitions") or [])
        return (1 + 0.4 * len(apis_) + min(comps, 30) / 6 + len(s.get("states") or {}) / 4
                + min(nav, 12) / 5 + (1 if (s.get("_platform") or {}).get("offlineCapable") else 0))

    # --- setup: what every other task stands on. The per-developer environment comes from
    # adam-connector-setup.zip, so each person's task is running it; the shared tasks are what it does
    # not do.
    devops = (areas.get("devops") or [""])[0]
    # Each setup task names the repository it lands in and what "done" means (audit R002, R059): a
    # one-line description sent people to guess both. The seed is the reference fixture every test
    # runs against (quality-gates 8), not a single demo venue (R034). The migration runner applies
    # the derived DDL forward and records each file; there is no ROLLBACK section to run (R046).
    SETUP = [
        ("SETUP-CI", "CI pipelines for the backend and frontend repositories", 3, [],
         "In **ticvai-backend** and **ticvai-frontend** (the repositories the setup zip creates). Done when: every "
         "merge request runs build, tests and lint in both, a red run blocks the merge, and a failing test on a "
         "branch shows in the MR."),
        ("SETUP-ENV", "Dev and staging environments (Terraform, ADR-0007 infra repository)", 5, [],
         "In **ticvai-infra** (ADR-0007: one parameterised `cell` module, one tfvars per environment). Done when: "
         "`terraform plan` and `apply` build dev and staging from nothing, state is remote and locked, and the "
         "cell mapping and region are written in the infra README."),
        ("SETUP-DB", "PostgreSQL (tenant and control databases) and a forward-only migration runner that applies the MIG epic in order", 5, ["SETUP-ENV"],
         "In **ticvai-backend**: `SqlMigrationRunner` (in the starter) applies `db/tenant` and `db/control` - the "
         "package's derived DDL - in file order and records each file with its checksum in "
         "`platform.schema_version`. Done when: both databases exist in dev, the runner applies every MIG file "
         "to an empty database, and a second run applies nothing."),
        ("SETUP-SEED", "Seed data: the reference fixture (two brands, three regions, AED and OMR) every test runs against", 5, ["SETUP-DB"],
         "In **ticvai-backend** `db/seed`: the reference fixture quality-gates 8 requires - two brands, three regions "
         "across two countries, AED and OMR - with products, prices, events, tills, staff, roles and "
         "denominations, so apps can be built before the Back Office setup screens exist. Done when: it loads on a "
         "migrated database, integration tests run against it, and the frontend mock server serves the same data."),
        ("SETUP-CLIENTS", "Generate the typed API clients from contracts/ for the frontend workspace", 3, ["SETUP-CI"],
         "In **ticvai-frontend** `packages/api-client`: generated from the package's `contracts/`, re-generated by "
         "one command. Done when: every in-release operation has a typed call, the build fails if the contracts "
         "change without a re-generate, and screen tickets stop stubbing calls."),
        ("SETUP-AUTH", "Sign-in working end to end against IdentityService", 5, ["SETUP-DB"],
         "In **ticvai-backend** and **ticvai-frontend**: the identity sign-in operations, `ICurrentPrincipal` and "
         "`ITenantContext` filled from the session. Done when: a seeded staff member signs in from a web app and "
         "an app, gets their effective permissions, and a request without a session gets 401."),
        ("SETUP-OBS", "Logging and monitoring basics", 2, ["SETUP-ENV"],
         "In **ticvai-backend** and **ticvai-infra**: structured logs and traces (OpenTelemetry, already referenced by "
         "the starter) shipped from dev and staging. Done when: a request can be followed from the API log to "
         "its trace, and an error raises an alert someone receives."),
    ]
    task("SETUP", "", "Epic", "Setup: environments, pipelines, database, seed data and sign-in",
         "Everything else depends on this epic.", 1, area="devops")
    for who, kind in sorted((team.get("onboard") or {}).items()):
        # Where the zip comes from and what done looks like (audit R001, R053). By the time this ticket can be
        # pulled, the connector it installs is already answering - so the evidence is that answer.
        roles = "once for backend and once for frontend" if "full" in str(kind) else f"once, for {kind}"
        task(f"SETUP-ONBOARD-{slug(who).upper()}", "SETUP", "Task", f"Onboard {who}: run adam-setup ({kind})",
             f"Get adam-connector-setup.zip from your lead (it is built from the ADAM repository and handed out; it is "
             f"not in any repo). Unzip it and run setup.cmd {roles}, answering Yes to the connection test. Done when "
             "the test prints 'N of N checks passed' and asking Claude Code 'What's on my board?' lists your "
             "tickets; paste both into the Ready for QA comment.", 1, pts=1, area="onboard", assignee=who)
    for k, subj, p, dep, detail in SETUP:
        task(k, "SETUP", "Task", subj, subj + ". " + detail, 1, pts=p, area="devops", assignee=devops, depends=dep)

    # --- backend: one epic per service, a feature per tag, and tasks of at most four operations,
    # because a 30-operation feature cannot be estimated, started or finished as one thing.
    svc_key = {n: "SVC-" + re.sub(r"Service$", "", n).upper() for n in by_service}
    op_task: dict[str, str] = {}
    svc_points = defaultdict(int)
    chunks = []
    for n, olist in sorted(by_service.items()):
        groups = defaultdict(list)
        for o in olist:
            groups[ops[o]["tag"]].append(o)
        for g, gl in sorted(groups.items()):
            gl = sorted(gl)
            for i in range(0, len(gl), 4):
                part = gl[i:i + 4]
                tk = f"{svc_key[n]}-{slug(g).upper()}-{i // 4 + 1}"
                pts = points_of(sum(op_raw(o) for o in part))
                for o in part:
                    op_task[o] = tk
                svc_points[n] += pts
                chunks.append((n, g, tk, part, pts))
    # **A service has one owner**, so its tasks stay in one head; whole services are balanced across
    # the backend developers, largest first, counting the DevOps load already carried.
    load = defaultdict(int)
    load[devops] += sum(p for _, _, p, _, _ in SETUP)
    svc_owner = {}
    backend = areas.get("backend") or []
    for n in sorted(svc_points, key=lambda n: -svc_points[n]):
        who = min(backend, key=lambda x: load[x]) if backend else ""
        svc_owner[n] = who
        load[who] += svc_points[n]
    # **A helper takes the small tasks inside services somebody else owns.** The owner keeps the service
    # and reviews the helper's work, so a service still has one head; the helper's cap is their rating.
    # Helpers are applied once every task exists (below), because a full-stack helper's frontend load
    # has to count before any backend is handed to them.
    helper_of = {}
    # --- migrations: the tables the slice reads or writes, plus every table their foreign keys reach,
    # one migration per schema in an order where each one's keys point backwards. The DDL already
    # exists (backend/, derived); the work is turning the slice's part of it into forward-only
    # migrations with a tested ROLLBACK section (backend/MIGRATIONS.md), not writing tables anew.
    ddl = read_ddl()
    used = defaultdict(lambda: {"reads": set(), "writes": set()})
    for o in slice_ops:
        for k in ("reads", "writes"):
            for t in lineage[o].get(k) or []:
                used[t][k].add(o)
    not_tables = sorted(t for t in used if t not in ddl and ":" not in t)
    rel = {t for t in used if t in ddl}
    why = {t: "used by the first release" for t in rel}
    frontier = list(rel)
    while frontier:
        t = frontier.pop()
        for x in sorted(ddl[t]["fks"]):
            if x in ddl and x not in rel:
                rel.add(x)
                why[x] = f"referenced by {t}"
                frontier.append(x)
    # The control plane is its own database, so its migrations are their own series and never
    # reference a tenant table by key (backend/990-cross-database-references.sql).
    groups = defaultdict(list)
    for t in sorted(rel):
        groups[(ddl[t]["db"], t.split(".")[0])].append(t)
    edges = {g: defaultdict(int) for g in groups}
    for g, ts in groups.items():
        for t in ts:
            for x in ddl[t]["fks"]:
                if x in rel and ddl[x]["db"] == g[0]:
                    edges[g][(g[0], x.split(".")[0])] += 1
    mig_order, deferred = [], {}
    for db in ("control", "tenant"):
        sub = {g: {h: n for h, n in e.items()} for g, e in edges.items() if g[0] == db}
        o_, d_ = schema_order(sub)
        mig_order += o_
        deferred.update(d_)
    mig_key = {g: f"MIG-{g[1].upper()}" for g in groups}
    table_mig = {t: mig_key[g] for g, ts in groups.items() for t in ts}
    migrations = []
    task("MIG", "", "Epic", f"Database migrations for the first release ({len(rel)} tables, {len(groups)} schemas)",
         "One forward-only migration per schema, applied forward by SqlMigrationRunner, which records each file and its checksum (handoff/service-docs/backend/MIGRATIONS.md). "
         "The tables, columns, keys, indexes and row-level security are already written in backend/ as derived DDL; "
         "each migration takes its schema's first-release tables from there. Order matters: each migration only "
         "references tables created by the ones before it.", 1, area="backend")
    task("MIG-BASELINE", "MIG", "Task", "Migration baseline: schemas, extensions, migration register, RLS helper "
         "functions and the venue partition helper",
         "From backend/tenant/000-schemas.sql, 001-extensions.sql, 002-migration-register.sql, the helper "
         "functions at the top of 920-row-level-security.sql and 930-partitioning.sql; the control database's "
         "own 000-002. Everything else in the MIG epic runs after this.", 1, pts=3, area="backend",
         assignee=devops, depends=["SETUP-DB"])
    load[devops] += 3
    migrations.append([0, "MIG-BASELINE", "V0001__baseline.sql", "both", "(baseline)", 0, 0, "", devops, 3, ""])
    for i, g in enumerate(mig_order, 2):
        ts = groups[g]
        n_cols = sum(len(ddl[t]["columns"]) for t in ts)
        refs = sorted({mig_key[(g[0], x.split(".")[0])] for t in ts for x in ddl[t]["fks"]
                       if x in rel and ddl[x]["db"] == g[0]} - {mig_key[g]})
        back = [r for r in refs if mig_order.index(next(h for h in groups if mig_key[h] == r)) < mig_order.index(g)]
        svc = schema_owner.get(g[1], "")
        who = svc_owner.get(svc) or (min(backend, key=lambda x: load[x]) if backend else "")
        pts = points_of(1 + 0.5 * len(ts) + n_cols / 40
                        + 0.3 * sum(1 for t in ts if ddl[t]["rls"]) + 0.5 * sum(ddl[t]["partitioned"] for t in ts))
        load[who] += pts
        fname = f"V{i:04d}__{g[1]}.sql"
        task(mig_key[g], "MIG", "Task", f"Migration {fname}: {g[1]} ({len(ts)} tables)",
             f"{g[0].capitalize()} database. Tables: " + ", ".join(ts) + f". Source DDL: {ddl[ts[0]]['file']} and the "
             f"matching rows of 900-foreign-keys, 910-indexes and 920-row-level-security. "
             + (f"Its keys into schemas created later ({deferred[g]}) go in MIG-FOREIGN-KEYS. " if g in deferred else "")
             + "Applied forward by SqlMigrationRunner; test that it applies to a database with its Follows applied and that a second run applies nothing.", 1, service=svc, pts=pts, area="backend", assignee=who,
             depends=["MIG-BASELINE"] + back)
        migrations.append([i - 1, mig_key[g], fname, g[0], g[1], len(ts), n_cols,
                           ", ".join(r.replace("MIG-", "").lower() for r in refs), who, pts, svc])
    if deferred:
        n_def = sum(deferred.values())
        task("MIG-FOREIGN-KEYS", "MIG", "Task", f"Migration V{len(mig_order) + 2:04d}__cross_schema_foreign_keys.sql "
             f"({n_def} keys)", "The foreign keys that point from a schema into one created after it: "
             + ", ".join(f"{g[1]} ({n})" for g, n in sorted(deferred.items())) + ". From 900-foreign-keys.sql.",
             1, pts=points_of(1 + n_def / 10), area="backend", assignee=devops,
             depends=[mig_key[g] for g in groups])
        migrations.append([len(mig_order) + 1, "MIG-FOREIGN-KEYS",
                           f"V{len(mig_order) + 2:04d}__cross_schema_foreign_keys.sql", "tenant", "(cross-schema)",
                           0, 0, "", devops, points_of(1 + n_def / 10), ""])
    MIG_COLS = ["Order", "File", "Task", "Database", "Schema", "Tables", "Columns", "References", "Assignee",
                "Points"]
    tables_rows = []
    for t in sorted(rel, key=lambda x: (mig_order.index((ddl[x]["db"], x.split(".")[0])), x)):
        tables_rows.append([table_mig[t], t, ddl[t]["db"], len(ddl[t]["columns"]), ddl[t]["rls"] or "none",
                            "yes" if ddl[t]["partitioned"] else "", len(used[t]["reads"]), len(used[t]["writes"]),
                            ", ".join(sorted(x for x in ddl[t]["fks"] if x in rel)), why[t],
                            schema_owner.get(t.split(".")[0], ""), ddl[t]["file"]])

    # Seed data and sign-in need tables, so they wait for the migrations rather than the empty database.
    all_migs = [m[1] for m in migrations]
    for t_ in tasks:
        if t_["key"] == "SETUP-SEED":
            t_["dependsOn"] = " ".join(sorted(set(all_migs)))
        elif t_["key"] == "SETUP-AUTH":
            t_["dependsOn"] = " ".join(sorted({"MIG-BASELINE"} | {mig_key[g] for g in groups
                                                                 if g[1] in ("identity", "pii", "platform")}))

    M = ["# Database migrations for the first release", "",
         f"**{len(rel)} tables in {len(migrations)} migrations.** Every table the first release reads or writes, "
         "plus every table their foreign keys reach. The DDL for all of them already exists in `backend/`; each "
         "migration takes its schema's tables from there, with the matching foreign keys, indexes and row-level "
         "security, and a ROLLBACK section tested in CI (`backend/MIGRATIONS.md`). Generated; do not edit.", "",
         "Each migration only references tables created by the ones above it. Keys that would point forward "
         "are added by the last migration.", "", "## Order", ""]
    M += table(MIG_COLS, [[m[0], f"`{m[2]}`", m[1], m[3], m[4], m[5], m[6], m[7], m[8], m[9]] for m in migrations])
    M += ["", "## Tables", ""]
    M += table(["Migration", "Table", "Columns", "Row-level security", "Partitioned", "Read by", "Written by",
                "Why"], [[r[0], f"`{r[1]}`", r[3], r[4], r[5], r[6], r[7], r[9]] for r in tables_rows])
    if not_tables:
        M += ["", "## Used by the release but not a table", ""]
        M += [f"- `{t}`: " + (ref.get("storage") or {}).get(t, "").replace("**", "")[:160] for t in not_tables]
    (OUT / "backend" / "MIGRATIONS.md").write_text("\n".join(M) + "\n", encoding="utf-8")

    def migs_for(olist):
        return {table_mig[t] for o in olist for k in ("reads", "writes") for t in lineage[o].get(k) or []
                if t in table_mig}

    for n, olist in sorted(by_service.items()):
        task(svc_key[n], "", "Epic", f"{n}: first-release slice ({len(olist)} operations) to 1.0.0",
             f"Build every operation below and publish the contract at 1.0.0. "
             f"Spec: handoff/service-docs/backend/{n}.md", min(wave[o] for o in olist), service=n,
             pts=svc_points[n], area="backend", assignee=svc_owner.get(n, ""))
        for g in sorted({c[1] for c in chunks if c[0] == n}):
            gk = f"{svc_key[n]}-{slug(g).upper()}"
            mine = [c for c in chunks if c[0] == n and c[1] == g]
            task(gk, svc_key[n], "Feature", f"{n} / {g}", f"Spec: handoff/service-docs/backend/{n}.md#group-{slug(g)}",
                 min(wave[o] for c in mine for o in c[3]), service=n, pts=sum(c[4] for c in mine),
                 area="backend", assignee=svc_owner.get(n, ""))
            for _, _, tk, part, pts in mine:
                task(tk, gk, "Task", f"{n}: " + ", ".join(part),
                     "Operations: " + ", ".join(part) + f". Spec: handoff/service-docs/backend/{n}.md#group-{slug(g)}",
                     min(wave[o] for o in part), service=n, pts=pts, area="backend",
                     assignee=helper_of.get(tk) or svc_owner.get(n, ""),
                     depends=migs_for(part) or {"MIG-BASELINE"})

    # --- screens: the owner of each area from docs/active/team.json; two owners split by load.
    caps = team.get("caps") or {}

    def assign(area, pts):
        people = areas.get(area) or []
        # A cap is the largest task a person takes in that area, from their rating in its stack.
        able = [x for x in people if pts <= (caps.get(area) or {}).get(x, 8)] or people
        if not able:
            return ""
        who = min(able, key=lambda x: load[x])
        load[who] += pts
        return who

    for k, p in plat.items():
        pk = f"APP-{k}"
        rows = []
        for sid in sorted(p["screens"]):
            s = screens[sid]
            deps = {op_task[a["operationId"]] for a in s.get("apis") or [] if a.get("operationId") in op_task}
            rows.append((sid, s, deps, points_of(screen_raw(s))))
        task(pk, "", "Epic", f"{p['name']}: {len(p['screens'])} screens", f"Spec: handoff/service-docs/frontend/{k}.md",
             min(screens[s].get("wave") or 1 for s in p["screens"]), platform=p["name"],
             pts=sum(r[3] for r in rows), area=k)
        for sid, s, deps, pts in sorted(rows, key=lambda r: (r[1].get("wave") or 9, deps_step(r[2]), -r[3], r[0])):
            task(f"{pk}-{sid}", pk, "Task", f"{sid} {s['name']}",
                 f"{s.get('purpose') or ''} Spec: handoff/service-docs/frontend/{k}.md#{slug(sid + ' ' + s['name'])}",
                 s.get("wave") or "", platform=p["name"], depends=deps | {"SETUP-CLIENTS"}, pts=pts, area=k,
                 assignee=assign(k, pts))

    # The Back Office screens that host the setup operations: built only as far as the slice needs.
    # **The fewest screens that cover every setup operation**, not every screen that declares one:
    # `createProduct` is declared on a dozen Back Office screens and needs building on one.
    first_release = {sid for p in plat.values() for sid in p["screens"]}
    uncovered = {o for o, d in slice_ops.items() if d["part"] == "setup"}
    hosts = defaultdict(set)
    for o in uncovered:
        for sid in slice_ops[o]["screens"]:
            if sid not in first_release:
                hosts[sid].add(o)
    no_screen = sorted(o for o in uncovered if not any(o in v for v in hosts.values()))
    uncovered -= set(no_screen)
    setup_screens = {}
    while uncovered:
        sid = max(sorted(hosts), key=lambda x: (len(hosts[x] & uncovered), x.startswith("BO")))
        setup_screens[sid] = hosts[sid] & uncovered
        uncovered -= hosts[sid]
    if setup_screens:
        # Only the setup operations of each screen are in the release, so a screen is sized by those.
        sizes = {sid: points_of(1 + 0.6 * len(v)) for sid, v in setup_screens.items()}
        task("APP-SETUP", "", "Epic", f"Back Office and Admin setup screens ({len(setup_screens)}), slice only",
             "Only the setup operations each screen hosts are in the first release; the rest of the screen "
             "follows later.", 1, platform="Back Office / Admin", pts=sum(sizes.values()), area="SETUP")
        for sid in sorted(setup_screens, key=lambda x: (min(wave[o] for o in setup_screens[x]),
                                                         deps_step({op_task[o] for o in setup_screens[x]}), x)):
            s = screens[sid]
            so = sorted(setup_screens[sid])
            task(f"APP-SETUP-{sid}", "APP-SETUP", "Task", f"{sid} {s['name']} (setup: {len(so)} operations)",
                 "In the slice: " + ", ".join(so), min(wave[o] for o in so),
                 platform=s["_platform"].get("shortName", ""), depends={op_task[o] for o in so},
                 pts=sizes[sid], area="SETUP", assignee=assign("SETUP", sizes[sid]))
    # --- Venue Management, full stack (team.json "venueManagement"): the back-office screens of the named
    # waves whose operations are all agreed (not provisional) and specified (have lineage), minus the ones
    # APP-SETUP already builds. Their operations beyond the slice are new backend, sized and chunked the
    # same way as the slice's, and the tables those reach beyond the slice get migrations of their own.
    vm = team.get("venueManagement") or {}
    vm_rows = []
    if vm:
        # One person or several; the first leads the epic, screens go to whoever is least loaded.
        vm_team = vm["who"] if isinstance(vm["who"], list) else [vm["who"]]
        who_vm = vm_team[0]
        first_batch = set(vm.get("firstBatch") or [])

        def agreed(o):
            return o in ops and not ops[o]["provisional"] and (lineage.get(o, {}).get("reads")
                                                               or lineage.get(o, {}).get("writes"))

        cand = []
        for sid, s_ in sorted(screens.items()):
            if not sid.startswith("BO-") or s_.get("wave") not in vm["waves"] or sid in setup_screens:
                continue
            ol = [a["operationId"] for a in s_.get("apis") or [] if a.get("operationId")]
            if ol and all(agreed(o) for o in ol):
                cand.append((sid, s_, ol))
        new_ops = sorted({o for _, _, ol in cand for o in ol if o not in slice_ops})
        new_tables = sorted({t for o in new_ops for k in ("reads", "writes") for t in lineage[o].get(k) or []
                             if t in ddl and t not in rel})
        task("VM", "", "Epic", f"Venue Management, waves {'-'.join(map(str, vm['waves']))}: {len(cand)} screens and "
             f"{len(new_ops)} operations beyond the first release (full stack)",
             "Back-office screens whose every operation is agreed and specified, with the backend they need that the "
             "first release does not build. Starts after " + vm.get("after", "") + ". Each service's owner reviews "
             "the backend added to it. Provisional and wave-3 screens are not here.",
             min(s_.get("wave") or 2 for _, s_, _ in cand) if cand else 2, platform="Venue Management",
             area="VM", assignee=who_vm)
        helpers = team.get("backendHelpers") or {}

        def vm_backend_owner(n, pts):
            owner = svc_owner.get(n) or (min(backend, key=lambda x: load[x]) if backend else "")
            load[owner] += pts
            return owner

        task("VM-DB", "VM", "Feature", "Venue Management: database migrations",
             "Tables the Venue Management backend needs that the first release does not create.", 2, area="VM")
        vm_mig = {}
        for sch in sorted({t.split(".")[0] for t in new_tables}):
            ts = [t for t in new_tables if t.split(".")[0] == sch]
            k = f"VM-MIG-{sch.upper()}"
            prior = [m[1] for m in migrations if m[4] == sch]
            n_cols = sum(len(ddl[t]["columns"]) for t in ts)
            pts = points_of(1 + 0.5 * len(ts) + n_cols / 40)
            task(k, "VM-DB", "Task", f"Migration: {sch} for Venue Management ({len(ts)} tables)",
                 "Tables: " + ", ".join(ts) + f". Source DDL: {ddl[ts[0]]['file']}. Additive to the first release; "
                 "applied forward by SqlMigrationRunner, and a second run applies nothing.", 2, pts=pts, area="VM",
                 assignee=vm_backend_owner(schema_owner.get(sch, ""), pts),
                 depends=prior or ["MIG-BASELINE"])
            for t in ts:
                vm_mig[t] = k
            vm_rows.append(["migration", k, f"{sch} ({len(ts)} tables)", "", pts])
        vm_op_task = {}
        groups_vm = defaultdict(list)
        for o in new_ops:
            groups_vm[(lineage[o]["service"], ops[o]["tag"])].append(o)
        for n in sorted({n for n, _ in groups_vm}):
            task(f"VM-BE-{re.sub(r'Service$', '', n).upper()}", "VM", "Feature",
                 f"Venue Management backend: {n}", f"Additive to {n}; its owner builds or reviews it.", 2,
                 service=n, area="VM")
        for (n, g), gl in sorted(groups_vm.items(), key=lambda x: (x[0][0], x[0][1])):
            for i in range(0, len(gl), 4):
                part = gl[i:i + 4]
                k = f"VM-{re.sub(r'Service$', '', n).upper()}-{slug(g).upper()}-{i // 4 + 1}"
                pts = points_of(sum(op_raw(o) for o in part))
                deps = {vm_mig.get(t) or table_mig.get(t) for o in part for kk in ("reads", "writes")
                        for t in lineage[o].get(kk) or []} - {None}
                task(k, f"VM-BE-{re.sub(r'Service$', '', n).upper()}", "Task", f"{n}: " + ", ".join(part),
                     "Operations beyond the first release: " + ", ".join(part)
                     + f". Additive to {n}; its first-release owner ({svc_owner.get(n) or 'unassigned'}) reviews.",
                     2, service=n, pts=pts, area="VM", assignee=vm_backend_owner(n, pts),
                     depends=deps or {"MIG-BASELINE"})
                for o in part:
                    vm_op_task[o] = k
                vm_rows.append(["backend", k, ", ".join(part), n, pts])
        for mod in sorted({c[1].get("module") or "Other" for c in cand}):
            task(f"VM-FE-{slug(mod).upper()}", "VM", "Feature", f"Venue Management screens: {mod}",
                 f"Back-office screens in {mod}.", 2, platform="Venue Management", area="VM", assignee=who_vm)

        def vm_assign(pts):
            who = min(vm_team, key=lambda x: (load[x], x))
            load[who] += pts
            return who

        def vm_deps(ol):
            return {op_task.get(o) or vm_op_task.get(o) for o in ol} - {None}

        for sid, s_, ol in sorted(cand, key=lambda c: (c[0] not in first_batch, c[1].get("wave") or 9,
                                                        deps_step(vm_deps(c[2])), c[0])):
            pts = points_of(screen_raw(s_))
            deps = vm_deps(ol)
            task(f"VM-{sid}", f"VM-FE-{slug(s_.get('module') or 'Other').upper()}", "Task", f"{sid} {s_['name']}" + (" (first batch)" if sid in first_batch else ""),
                 f"{s_.get('purpose') or ''} Module: {s_.get('module')}.", s_.get("wave") or "",
                 platform="Venue Management", depends=deps | {"SETUP-CLIENTS"}, pts=pts, area="VM",
                 assignee=vm_assign(pts))
            vm_rows.append(["screen", f"VM-{sid}", f"{sid} {s_['name']}", s_.get("module"), pts])
        epic = next(t_ for t_ in tasks if t_["key"] == "VM")
        epic["points"] = sum(r[4] for r in vm_rows)
        for f_ in [t_ for t_ in tasks if t_["type"] == "Feature" and t_["key"].startswith("VM-")]:
            f_["points"] = sum(int(c["points"] or 0) for c in tasks if c["parent"] == f_["key"])
        epic["assignee"] = ""

    # **Helpers take the small backend tasks, in the order the work can start**, from whichever owner is
    # most loaded, and only while the move leaves the helper lighter than the owner. The owner keeps the
    # service and reviews. Full-stack helpers already carry their frontend here, so they are not overfilled.
    helpers = team.get("backendHelpers") or {}
    taken = defaultdict(int)  # helper points so far: the helper work is shared, not given to the lightest
    for t_ in sorted((x for x in tasks if x["type"] == "Task" and x["track"] == "Backend" and x["points"]),
                     key=lambda x: (x["phase"], int(x["wave"] or 9), step_of(x["key"]), x["key"])):
        pts, owner = int(t_["points"]), t_["assignee"]
        able = [h for h, cap in helpers.items() if pts <= cap and h != owner]
        if not able:
            continue
        h = min(able, key=lambda x: (taken[x], load[x], x))
        if load[h] + pts <= load[owner] - pts:
            t_["assignee"] = h
            taken[h] += pts
            t_["description"] += f" Helper task: {owner} owns the service and reviews."
            load[h] += pts
            load[owner] -= pts

    # Venue Management screens are re-shared once helper backend is known, so a full-stack member of the
    # screen team is not given a full share of screens on top of backend handed over after the split.
    if vm:
        vm_team_ = vm["who"] if isinstance(vm["who"], list) else [vm["who"]]
        vm_screens = [x for x in tasks if x["key"].startswith("VM-BO-")]
        for x in vm_screens:
            load[x["assignee"]] -= int(x["points"] or 0)
        for x in sorted(vm_screens, key=lambda x: (0 if "(first batch)" in x["subject"] else 1, int(x["wave"] or 9),
                                                   step_of(x["key"]), x["key"])):
            who = min(vm_team_, key=lambda y: (load[y], y))
            x["assignee"] = who
            load[who] += int(x["points"] or 0)

    # **Chronology.** Every task gets its place in the order work can happen: the first release before
    # Venue Management, then wave, then how many tasks stand in front of it, then database before
    # backend before frontend. `queue` is the same order within one person's list, so each developer's
    # board reads top to bottom as the order to work in.
    TRACK_ORDER = {"Setup": 0, "DevOps": 1, "Onboarding": 1, "Database": 2, "Backend": 3, "Full stack": 4,
                   "Frontend": 5}
    for t_ in tasks:
        step_of(t_["key"])
    ordered = sorted(tasks, key=lambda t_: (t_["phase"], int(t_["wave"] or 9), step[t_["key"]],
                                            TRACK_ORDER[t_["track"]], t_["key"]))
    queue_n = defaultdict(int)
    for i, t_ in enumerate(ordered, 1):
        t_["sequence"] = i
        t_["step"] = step[t_["key"]]
        if t_["type"] == "Task" and t_["assignee"]:
            queue_n[t_["assignee"]] += 1
            t_["queue"] = queue_n[t_["assignee"]]
        else:
            t_["queue"] = ""
    tasks.sort(key=lambda t_: t_["sequence"])
    # Parents before children, whatever their sequence, so OpenProject can link each one on creation.
    placed, out_ = set(), []

    def place(t_):
        if t_["key"] in placed:
            return
        if t_["parent"] and t_["parent"] in by_key:
            place(by_key[t_["parent"]])
        placed.add(t_["key"])
        out_.append(t_)

    for t_ in tasks:
        place(t_)
    tasks[:] = out_

    COLS = ["sequence", "queue", "key", "parent", "type", "track", "subject", "phase", "wave", "step", "points",
            "assignee", "area", "platform", "service", "dependsOn", "description"]
    with (OUT / "tasks.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(tasks)

    # Occupancy: points on leaf tasks only, so an epic's roll-up is not counted twice.
    leaves = [t for t in tasks if t["type"] == "Task"]
    occ = defaultdict(lambda: defaultdict(int))
    occ_n = defaultdict(int)
    for t in leaves:
        occ[t["assignee"] or "(unassigned)"][t["area"]] += int(t["points"] or 0)
        occ_n[t["assignee"] or "(unassigned)"] += 1
    total_pts = sum(sum(v.values()) for v in occ.values())
    occupancy = sorted(([who, occ_n[who], sum(v.values()), f"{round(100 * sum(v.values()) / total_pts)}%",
                         ", ".join(f"{a} {p}" for a, p in sorted(v.items(), key=lambda x: -x[1]))]
                        for who, v in occ.items()), key=lambda r: -r[2])
    for who, why in (team.get("notAssigned") or {}).items():
        occupancy.append([who, 0, 0, "0%", why])

    # ---------------------------------------------------------------- workbook
    wb = Workbook()
    head_fill = PatternFill("solid", fgColor="1F3864")

    def sheet(title, head, rows, widths):
        ws = wb.create_sheet(title)
        ws.append(head)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = head_fill
        for r in rows:
            ws.append([("" if v is None else v) for v in r])
        for i, wdt in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = wdt
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        return ws

    wb.remove(wb.active)
    sheet("Services", ["Service", "Tier", "Core", "Setup", "In slice", "All operations", "Later", "Scale", "If down"],
          [[n, services[n].get("tier"), sl["services"][n]["core"], sl["services"][n]["setup"], len(by_service[n]),
            sl["services"][n]["total"], sl["services"][n]["total"] - len(by_service[n]),
            re.sub(r"\*\*", "", services[n].get("scale", "")), re.sub(r"\*\*", "", services[n].get("risk", ""))]
           for n in sorted(by_service)], [22, 12, 8, 8, 9, 12, 8, 50, 50])
    sheet("Operations", ["Service", "Group", "Operation", "Method", "Path", "Permission", "Scope", "Offline",
                         "Part", "Wave", "Platforms", "Screens", "Reads", "Writes", "Summary"],
          [[d["service"], ops[o]["tag"], o, ops[o]["verb"], ops[o]["path"], ops[o]["permission"],
            ops[o]["scopeLevel"], "yes" if ops[o]["offline"] else "", d["part"], wave[o],
            ", ".join(d["platforms"]), ", ".join(d["screens"]), ", ".join(lineage[o].get("reads") or []),
            ", ".join(lineage[o].get("writes") or []), ops[o]["summary"]]
           for o, d in sorted(slice_ops.items(), key=lambda x: (x[1]["service"], ops[x[0]]["tag"], x[0]))],
          [20, 18, 30, 8, 36, 24, 12, 8, 8, 6, 14, 30, 40, 40, 44])
    frows = []
    for o in sorted(slice_ops):
        for where, rows in (("request", ops[o]["body"]), ("response", ops[o]["success"])):
            for r in rows:
                frows.append([slice_ops[o]["service"], o, where, *r])
        for r in ops[o]["params"]:
            frows.append([slice_ops[o]["service"], o, f"param ({r[1]})", r[0], r[3], r[2], r[4]])
    sheet("Fields", ["Service", "Operation", "Where", "Field", "Type", "Required", "Notes"], frows,
          [20, 30, 12, 36, 34, 9, 60])
    sheet("Screens", ["Platform", "Screen", "Name", "Module", "Wave", "Route", "Operations", "Purpose"],
          [[plat[k]["name"], sid, screens[sid]["name"], screens[sid].get("module"), screens[sid].get("wave"),
            (screens[sid].get("implementation") or {}).get("route"),
            ", ".join(a["operationId"] for a in screens[sid].get("apis") or [] if a.get("operationId")),
            screens[sid].get("purpose")]
           for k in plat for sid in sorted(plat[k]["screens"])], [20, 10, 30, 18, 6, 30, 60, 50])
    sheet("Tasks", ["Sequence", "Queue", "Key", "Parent", "Type", "Track", "Subject", "Phase", "Wave", "Step",
                    "Points", "Assignee", "Area", "Platform", "Service", "Depends on", "Description"],
          [[t["sequence"], t["queue"], t["key"], t["parent"], t["type"], t["track"], t["subject"], t["phase"],
            t["wave"], t["step"], t["points"], t["assignee"], t["area"], t["platform"], t["service"],
            t["dependsOn"], t["description"]] for t in tasks],
          [9, 7, 26, 18, 9, 10, 60, 6, 6, 6, 7, 20, 9, 18, 18, 40, 70])
    sheet("Occupancy", ["Person", "Tasks", "Points", "Share", "By area"], occupancy, [22, 8, 8, 8, 70])
    MIG_HEAD = ["Order", "Task", "Migration file", "Database", "Schema", "Tables", "Columns",
                "References (created earlier or deferred)", "Assignee", "Points", "Owning service"]
    MIG_W = [6, 22, 40, 10, 16, 8, 9, 40, 20, 7, 20]
    TAB_HEAD = ["Migration", "Table", "Database", "Columns", "Row-level security", "Partitioned by venue",
                "Operations reading", "Operations writing", "Foreign keys to", "Why it is in the release",
                "Owning service", "Source DDL"]
    TAB_W = [20, 36, 10, 9, 14, 12, 10, 10, 50, 40, 20, 34]
    sheet("Migrations", MIG_HEAD, migrations, MIG_W)
    sheet("Tables", TAB_HEAD, tables_rows, TAB_W)
    gaps = [["fed elsewhere", t, ", ".join(w)] for t, w in sl["fedElsewhere"].items()]
    gaps += [["not a table", t, (ref.get("storage") or {}).get(t, "").replace("**", "")[:200]] for t in not_tables]
    gaps += [["no writer", t, ""] for t in sl["noWriter"]]
    gaps += [["setup operation, no screen", o, f"{slice_ops[o]['service']}: makes "
              + ", ".join(slice_ops[o]["enables"]) + " non-empty; reachable only by API or import"] for o in no_screen]
    gaps += [["state model", o, g] for o, g in state_gaps]
    sheet("Gaps", ["Kind", "Table", "Written by"], gaps, [16, 34, 80])
    wb.save(OUT / "TICVAI_First_Release.xlsx")

    cw = Workbook()
    wb = cw
    wb.remove(wb.active)
    sheet("Platforms", ["Platform", "Screens", "Wave 1", "Wave 2", "Wave 3", "Areas covered"],
          [[p["name"], len(p["screens"])] + [sum(1 for s_ in p["screens"] if screens[s_].get("wave") == w) or "" for w in (1, 2, 3)]
           + [", ".join(sorted({screens[s_].get("module") for s_ in p["screens"] if screens[s_].get("module")}))]
           for p in plat.values()], [24, 9, 8, 8, 8, 90])
    sheet("Services", ["Service", "What it looks after", "If it is unavailable"] + [p["name"] for p in plat.values()],
          [[CLIENT_TEXT[n][0], CLIENT_TEXT[n][1], CLIENT_TEXT[n][2]] + ["yes" if matrix[n][k] else "" for k in plat]
           for n in order], [24, 60, 50, 12, 12, 12, 12])
    sheet("Screens", ["Platform", "Screen", "Area", "Wave", "What it does"],
          [[plat[k]["name"], screens[sid]["name"], screens[sid].get("module"), screens[sid].get("wave"),
            screens[sid].get("purpose")] for k in plat
           for sid in sorted(plat[k]["screens"], key=lambda x: (screens[x].get("wave") or 9, x))],
          [22, 34, 24, 6, 70])
    cw.save(OUT / "TICVAI_First_Release_Client.xlsx")

    # ---------------------------------------------------------------- backend build plan
    # **One workbook a backend developer opens first**: what services, which operations, which API
    # schemas, which tables and migrations, and in what order the tasks can start. Everything is the
    # same data as above, cut for the backend and ordered by what has to exist first.
    comp = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        for name, node in (((contract(f).get("components") or {}).get("schemas")) or {}).items():
            if isinstance(node, dict):
                comp[name] = {"contract": f.stem, "persistence": node.get("x-ticvai-persistence") or "",
                              "fields": len(merged(node, f, frozenset())[0]),
                              "description": first_sentence(node.get("description"))}
    uses = defaultdict(lambda: {"request": set(), "response": set()})
    for o in slice_ops:
        if ops[o]["bodyType"] in comp:
            uses[ops[o]["bodyType"]]["request"].add(o)
        st = re.sub(r"^array of ", "", ops[o]["successType"] or "")
        if st in comp:
            uses[st]["response"].add(o)
    schema_rows = [[comp[nm]["contract"], nm, comp[nm]["fields"], str(comp[nm]["persistence"]).replace("**", ""),
                    len(u["request"]), len(u["response"]), ", ".join(sorted(u["request"] | u["response"])[:12])
                    + (" …" if len(u["request"] | u["response"]) > 12 else ""), comp[nm]["description"]]
                   for nm, u in sorted(uses.items(), key=lambda x: (comp[x[0]]["contract"], x[0]))]

    be = [t for t in tasks if t["type"] == "Task" and (t["area"] in ("backend", "devops")
                                                       or (t["area"] == "VM" and not t["key"].startswith("VM-BO-")))]
    plan_rows = [[step[t["key"]], t["wave"], t["key"], t["parent"], t["subject"], t["points"], t["assignee"],
                  t["service"], t["dependsOn"], t["description"]]
                 for t in sorted(be, key=lambda t: t["sequence"])]
    be_occ = defaultdict(lambda: [0, 0])
    for t in be:
        be_occ[t["assignee"] or "(unassigned)"][0] += 1
        be_occ[t["assignee"] or "(unassigned)"][1] += int(t["points"] or 0)

    bw = Workbook()
    wb = bw
    wb.remove(wb.active)
    ov = wb.create_sheet("Read me")
    n_be_ops = sum(len(v) for v in by_service.values())
    for r in [
        ["TICVAI backend build plan: first release (POS, Guest App web and mobile, White Labelling)"],
        [],
        ["Services", len(by_service)],
        ["Operations (APIs) to build", n_be_ops],
        ["API schemas they send or return", len(schema_rows)],
        ["Tables", len(rel)],
        ["Migrations", len(migrations)],
        ["Backend and DevOps tasks", len(be)],
        ["Points", sum(int(t["points"] or 0) for t in be)],
        [],
        ["How to read it"],
        ["Build plan", "Every backend and DevOps task. Step 1 can start now; a task at step N waits for at least one task at step N-1. Wave is when the screens need it."],
        ["Migrations", "One forward-only migration per database schema, in the order they run. Each only references tables created before it; keys that would point forward are added by the last migration."],
        ["Tables", "Every table the first release reads or writes, plus the tables their foreign keys reach, with the migration that creates each."],
        ["Services / APIs / API schemas", "What each service builds, every operation to build, and the request and response schemas those operations use, with where each is stored."],
        ["Assignees", "From docs/active/team.json, balanced by points. Points are relative size (1, 2, 3, 5, 8), not hours."],
        [],
        ["Generated by tools/build-service-docs.py from the contracts, the delivery slice, the lineage and the DDL in backend/. Re-run it; do not edit this file."],
    ]:
        ov.append(r)
    ov["A1"].font = Font(bold=True, size=13)
    ov["A11"].font = Font(bold=True)
    ov.column_dimensions["A"].width = 34
    ov.column_dimensions["B"].width = 120
    sheet("Build plan", ["Step", "Wave", "Key", "Parent", "Task", "Points", "Assignee", "Service", "Depends on",
                         "Description"], plan_rows, [6, 6, 26, 18, 60, 7, 20, 18, 40, 70])
    sheet("Migrations", MIG_HEAD, migrations, MIG_W)
    sheet("Tables", TAB_HEAD, tables_rows, TAB_W)
    sheet("Services", ["Service", "Owner", "Tier", "Operations in release", "All operations", "Tables it owns in release",
                       "Points", "If down"],
          [[n, svc_owner.get(n, ""), services[n].get("tier"), len(by_service[n]), sl["services"][n]["total"],
            sum(1 for t in rel if schema_owner.get(t.split(".")[0]) == n), svc_points[n],
            re.sub(r"\*\*", "", services[n].get("risk", ""))] for n in sorted(by_service)],
          [22, 20, 12, 12, 12, 14, 8, 60])
    sheet("APIs", ["Service", "Group", "Operation", "Method", "Path", "Request schema", "Response schema",
                   "Permission", "Part", "Wave", "Task", "Reads", "Writes", "Summary"],
          [[d["service"], ops[o]["tag"], o, ops[o]["verb"], ops[o]["path"], ops[o]["bodyType"], ops[o]["successType"],
            ops[o]["permission"], d["part"], wave[o], op_task.get(o, ""), ", ".join(lineage[o].get("reads") or []),
            ", ".join(lineage[o].get("writes") or []), ops[o]["summary"]]
           for o, d in sorted(slice_ops.items(), key=lambda x: (x[1]["service"], ops[x[0]]["tag"], x[0]))],
          [20, 18, 30, 8, 36, 26, 26, 24, 8, 6, 26, 40, 40, 44])
    sheet("API schemas", ["Contract", "Schema", "Fields", "Stored as", "Used as request", "Used as response",
                          "Operations", "Description"], schema_rows, [16, 30, 8, 40, 10, 10, 60, 60])
    sheet("Fields", ["Service", "Operation", "Where", "Field", "Type", "Required", "Notes"], frows,
          [20, 30, 12, 36, 34, 9, 60])
    sheet("Occupancy", ["Person", "Backend and DevOps tasks", "Points"],
          sorted(([w, n, p] for w, (n, p) in be_occ.items()), key=lambda r: -r[2]), [22, 12, 10])
    bw.save(OUT / "TICVAI_Backend_Build_Plan.xlsx")

    fields = sum(len(ops[o]["body"]) + len(ops[o]["success"]) + len(ops[o]["params"]) for o in slice_ops)
    print(f"{len(slice_ops)} operations, {fields} fields, {sum(len(p['screens']) for p in plat.values())} screens, "
          f"{len(by_service)} services, {len(tasks)} tasks ({len(setup_screens)} setup screens, "
          f"{len(no_screen)} setup operations with no screen)")
    for r in occupancy:
        print(f"  {r[0]:20} {r[1]:4} tasks {r[2]:5} pts {r[3]:>4}  {r[4]}")
    print(f"-> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
