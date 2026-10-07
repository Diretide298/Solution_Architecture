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
  plan-tasks.csv             every task of every block, ticketed or not (the schedule and the deck read it)

**The sprint plan** (1 October, the PM's replan; tools/sprint_plan.py): the tickets are grouped Epic = Block (A,
B, C, D), Feature = app-module (a business module on one app: "Ticketing · Guest Web", with the back end it needs),
Task = the work, under the keys it was pushed with. Block A is the first release; B, C and D take the rest of the
package in build order, each a set of complete, testable app-modules ending on a sprint boundary. Blocks named in
team.json `sprintPlan.ticketBlocks` (A and B) are ticketed task by task; the others are ticketed as features until
they are planned (their tasks are in plan-tasks.csv, with the keys they will have).

    python3 tools/build-service-docs.py [--rebalance]

--rebalance: a pushed ticket's owner may move (plan item L2); without it, owners of tickets pushed from release
`sprintPlan.stableOwners.since` on are kept, and only new work is placed.

**The task sheet is an input to OpenProject, not a second plan** (CF-124). Keys are local; the
`parent` and `dependsOn` columns name other keys in the same file, so a person or ADAM's bridge
creates parents first and links children to them. No dates and no estimates: OpenProject owns both.

Run: python3 tools/build-service-docs.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import re
import sys
import heapq
from collections import Counter, defaultdict
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ticket_done  # noqa: E402  (what finishes a ticket: shared with op-release.py, CHG-GTR-002)
import sprint_plan as sp  # noqa: E402  (the calendar, app-modules and scheduler the plan generators share)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"
OUT = HANDOFF / "service-docs"
TEAM = ROOT / "docs" / "active" / "team.json"
EXTRA = ROOT / "docs" / "active" / "block-a-extra-tasks.json"
MAX_DEPTH = 3
# The working day (from Monday 5 October 2026) a screen that still needs a person may start being built: the first
# day of Sprint 3, Monday 2 November (CHG-RFM-008). Until 4 October it was day 5 (CHG-FXP-004), inside Sprint 1, while
# check-screen-patterns NP fails any such screen a Sprint 1 or 2 task builds; the plan now holds what the check refuses.
DEFINE_DAY = 20.0


def block_a_decisions() -> dict:
    """**Block A completes its apps** (Chinmay, 3 October 2026, CHG-RONEP-001; docs/active/decisions/answers-3-october-r1-plan.md).
    The decided parts of Block A's scope that no screen binding derives, from block-a-extra-tasks.json:

      aiEngineOperations  operation -> the AI engine task that serves it (a task's `operations`: AI-ENGINE-GATEWAY,
                          AI-ENGINE-CONCIERGE); built in ticvai-ai by the AI engineers, so no back-end task builds it
      blockA1Operations   operation -> why Block A's first drop (A1) needs it although no Block A screen binds it
                          (the payment configuration guests cannot pay without)
      blockAOperations    operation -> why Block A builds it although no Block A screen binds it in this tree
                          (completion work: A1 if it fits, else A2; CHG-RONEP-007)
      navHomes            screen -> why it is an app's home (a section home): the only screens besides an app's entry
                          the navigation closure pulls into Block A (lever A, CHG-RONEP-007)
      blockAScreens       screen -> why Block A builds the whole screen (its setup part and the rest)
      screenNotes         screen -> a sentence its Block A tasks carry (BO-1065: the AI residency section)
      screenModules       screen -> {module, why}: the business module a screen's tasks are grouped under when its
                          operations' majority would put it elsewhere (CHG-RFM-006: ADM-503/504/505 stay in Identity, Roles
                          & Security, Block B, as r2 had them, after binding listForecastDefinitions made them AI's)
      appModules          [{key, name, module, platform, block, operations, screens, wiring, tasks}]: an app-module the lead
                          decided as one piece of work in a named block (CHG-R4-003, 5 October: the kiosk customisation in
                          Block A2), built as written and never moved by the block filling

    tools/check-plan-closure.py reads the same file and checks that the plan holds them."""
    if not EXTRA.exists():
        return {"aiEngineOperations": {}, "blockA1Operations": {}, "blockAOperations": {}, "blockAScreens": {},
                "screenNotes": {}, "navHomes": {}, "screensNotBuilt": {}, "screenModules": {}, "appModules": []}
    ex = json.loads(EXTRA.read_text(encoding="utf-8"))
    ai = {o: t["key"] for t in ex.get("tasks") or [] for o in t.get("operations") or []}
    return {"aiEngineOperations": ai, "blockA1Operations": dict(ex.get("blockA1Operations") or {}),
            "blockAOperations": dict(ex.get("blockAOperations") or {}),
            "blockAScreens": dict(ex.get("blockAScreens") or {}), "screenNotes": dict(ex.get("screenNotes") or {}),
            "navHomes": dict(ex.get("navHomes") or {}),
            # screen -> {kind, into, why}: a replaced page or a screen nobody could define, given no build task
            # (CHG-FXP-002, ticket_done.screen_hold)
            "screensNotBuilt": dict(ex.get("screensNotBuilt") or {}),
            "screenModules": {k: v["module"] for k, v in (ex.get("screenModules") or {}).items()},
            # a decided app-module: its operations, whole screens and wiring tasks, in its block (CHG-R4-003)
            "appModules": list(ex.get("appModules") or [])}

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
                    # **held**: provisional, a stub whose shape is a proposal, or deprecated (CHG-FXP-003): not put on
                    # a build ticket. `provisional` stays the name every rule below reads.
                    "provisional": ticket_done.operation_hold(op) is not None,
                    "hold": ticket_done.operation_hold(op),
                    # what only the client can unblock (sandbox credentials ...): a module test says it waits on it
                    "makeOrBreak": op.get("x-ticvai-make-or-break"),
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

# A forward migration derive-ddl writes after r1 (`V0100__after_r1_20261002.sql`); the same pattern as derive-ddl's.
FORWARD_FILE = re.compile(r"^V(\d{4})__[\w.-]+\.sql$")
# The row-level policy each `platform.apply_<kind>_rls` gives a table (backend/<db>/920-row-level-security.sql), as the
# documents name it (CHG-TBF-004). **`tenant` is not a missing tenant_id**: a tenant database holds one tenant
# (ADR-0038), so the tenant-root policy is platform.tenant_root_in_scope() and needs no tenant column.
POLICY_LABEL = {
    "scope": "scope_path",
    "venue": "venue_id",
    "subject": "subject",
    "parent": "through its owner",
    "tenant": "tenant root (one tenant per database; no tenant_id by design)",
}


# **Tables the kernel writes and no operation does** (ADR-0058), so lineage never reaches them: they are created
# with the first release because PLATFORM-OUTBOX and MIG-PARTITIONS run on them (CHG-TBF-003).
# `platform.schema_version` is not here: it is in 002-migration-register.sql, which MIG-BASELINE applies.
MACHINERY_TABLES = {
    "kernel.inbox": "kernel machinery: the inbox per tenant database (ADR-0058; PLATFORM-OUTBOX, MIG-PARTITIONS)",
    "ai.inbox": "kernel machinery: the AI consumers' inbox, since only AI writes AI tables (ADR-0058, ADR-0020)",
    "control.outbox_relay": "kernel machinery: the relay lease per tenant database (ADR-0058; PLATFORM-OUTBOX)",
}
# **Forward migration file numbers** (CHG-TBF-002). V0001 is the baseline and V0002-V0099 the first release, in
# schema order; V0100-V0999 belong to derive-ddl's frozen-mode files (backend/<db>/V01xx__after_r1_<date>.sql);
# every later forward migration (VM-MIG-*, MIG-<SCHEMA>-<n>) takes V1000 upwards in build order and keeps the
# number it was planned with on the next run, so a refresh never renumbers a ticket somebody may have started.
FORWARD_TICKET_FIRST = 1000
MIG_FILE = re.compile(r"\b(V(\d{4})[a-z]?__[\w.-]+\.sql)\b")


def prior_migration_files() -> dict[str, str]:
    """{task key: migration file} from the plan this run replaces (handoff/service-docs/plan-tasks.csv)."""
    p = OUT / "plan-tasks.csv"
    out = {}
    if not p.exists():
        return out
    with p.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            m = MIG_FILE.search(r.get("subject") or "")
            if m and r.get("track") == "Database" and "#" not in (r.get("key") or ""):
                out[r["key"]] = m.group(1)
    return out


def src_files(ddl: dict, ts) -> str:
    """The DDL files a migration's tables come from: the baseline 010-<schema>.sql and, for a table created after
    r1, the forward file derive-ddl wrote it into (CHG-TBF-002)."""
    files = sorted({ddl[t]["file"] for t in ts}, key=lambda f: (f.rsplit("/", 1)[-1].startswith("V"), f))
    return " and ".join(files)


def screen_op_ids(s: dict) -> set:
    """The operations a screen record binds: every distinct `operationId` in its `apis`. The count a setup
    ticket's title gives is this one (tools/check-ticket-scope.py)."""
    return {a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")}


def setup_scope(s: dict, setup_ops) -> str:
    """`setup: 5 of its 11 operations`. **The title says how much of the screen the ticket builds and how big the screen
    is** (3 October, CHG-TBF-005; Block A audit pattern 7): "setup: 5 operations" on BO-009, an 11-operation screen,
    read as the whole screen and the ticket was judged out of step with it."""
    n, k = len(screen_op_ids(s)), len(set(setup_ops))
    return f"setup: all {n} operations" if k >= n else f"setup: {k} of its {n} operations"


def rest_scope(s: dict, setup_ops) -> str:
    """`the rest of the screen: 6 of its 11 operations`, the other half of setup_scope."""
    n = len(screen_op_ids(s))
    return f"the rest of the screen: {n - len(set(setup_ops) & screen_op_ids(s))} of its {n} operations"


def read_ddl() -> dict[str, dict]:
    """Every table in backend/, from the derived SQL: which file declares it, its columns, and the
    tables its foreign keys point at. The SQL is the storage truth (backend/MIGRATIONS.md), so the
    migration plan is read from it rather than from the contracts' persistence notes."""
    tables: dict[str, dict] = {}
    for db in ("tenant", "control"):
        # **The forward migrations after r1 are DDL too** (3 October, CHG-TBF-002). Since the baseline froze,
        # derive-ddl writes a new table into `backend/<db>/V<nnnn>__after_r1_<date>.sql`, not into 010-<schema>.sql.
        # Reading only the 010 files left the 17 tables V0101 created (ai.spend_ceiling, whitelabel.site_package,
        # access.hardware_certification ...) out of every migration ticket although operations read and write
        # them; their columns added after r1 were missing from the counts as well.
        fwd = sorted((p for p in (ROOT / "backend" / db).glob("V*.sql") if FORWARD_FILE.match(p.name)),
                     key=lambda p: int(FORWARD_FILE.match(p.name).group(1)))
        for f in sorted((ROOT / "backend" / db).glob("010-*.sql")) + fwd:
            name, cols_ = None, []
            for line in f.read_text(encoding="utf-8").splitlines():
                m = re.match(r'ALTER TABLE (\w+\.\w+) ADD COLUMN IF NOT EXISTS (\w+)\s+(.+?);?$', line)
                if m and m.group(1) in tables:
                    have = {c for c, _ in tables[m.group(1)]["columns"]}
                    if m.group(2) not in have:
                        tables[m.group(1)]["columns"].append((m.group(2), m.group(3)))
                    continue
                m = re.match(r'CREATE TABLE IF NOT EXISTS (\w+)\."?(\w+)"? \(', line)
                if m:
                    name, cols_ = f"{m.group(1)}.{m.group(2)}", []
                    continue
                # **A partitioned table closes with `) PARTITION BY RANGE (col);`** (ADR-0056), not
                # `);`, and its key is a table constraint rather than a column.
                if name and line.startswith(")"):
                    pm = re.search(r"PARTITION BY \w+ \((\w+)\)", line)
                    if name not in tables:
                        tables[name] = {"db": db, "file": f.relative_to(ROOT).as_posix(), "columns": cols_,
                                        "fks": set(), "partition_by": pm.group(1) if pm else ""}
                    name = None
                    continue
                if name and line.strip().startswith("CONSTRAINT "):
                    continue
                m = re.match(r"\s+(\w+)\s+(.+?),?$", line)
                if name and m:
                    cols_.append((m.group(1), m.group(2).rstrip(",")))
        policy = {}
        for f in [ROOT / "backend" / db / "900-foreign-keys.sql",
                  ROOT / "backend" / db / "920-row-level-security.sql"] + fwd:
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8").replace('"', "")
            text = re.sub(r"--[^\n]*", "", text)
            # `(venue_id, x)` as well as `(x)`: a composite venue key (ADR-0056) is still a key.
            for m in re.finditer(r"ALTER TABLE (\w+\.\w+) ADD CONSTRAINT \w+ FOREIGN KEY \([\w, ]+\) "
                                 r"REFERENCES (\w+\.\w+)", text):
                if m.group(1) in tables:
                    tables[m.group(1)]["fks"].add(m.group(2))
            for m in re.finditer(r"platform\.apply_(\w+?)_rls\('(\w+\.\w+)'::regclass", text):
                policy[m.group(2)] = m.group(1)
        for t, kind in policy.items():
            if t in tables:
                tables[t]["policy"] = kind
    for t in tables.values():
        names = {c for c, _ in t["columns"]}
        t["rls"] = ("scope_path" if "scope_path" in names else
                    "venue_id" if "venue_id" in names else "")
        # **What the row-level policy actually is**, for the documents (CHG-TBF-004). `rls` above only says
        # which scope column a table carries and still sizes the migration tasks; a table with neither column is
        # not unprotected. `tenant` is the tenant-root policy: one tenant per database, so the policy is
        # platform.tenant_root_in_scope() and the table has no tenant_id column, by design (ADR-0038).
        t["policy_label"] = POLICY_LABEL.get(t.get("policy", ""), "none")
        # ADR-0056 (amends ADR-0044): release 1 partitions by month, and the SQL says which tables.
        t["partitioned"] = bool(t.get("partition_by"))
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


# ---- key stability ------------------------------------------------------------------------------
# **Once a key has an OpenProject ticket, the same work keeps that key** (30 September). The keys below
# are formed from where work sits in the plan -- `APP-SETUP-` or `VM-` for a screen, the n-th chunk of
# four operations for a backend task -- so a plan change that moved work re-keyed it, and the push
# treated the new key as new work: 25 duplicates when screens moved between Block A setup and Venue
# Management and operations between SVC- and VM-, and SVC-WALLET-RETAIL-1 matched to the wrong half
# when a split re-numbered its parts. So the plan is formed exactly as before and then reconciled
# against pms-map.json before anything is written. Only the key changes: phase, track, tier, build
# order and dependencies were already computed from the key the plan formed, and stay.
#
# The identity of the work, by kind:
#   screen  the screen id. APP-<platform>-, APP-SETUP- and VM- are the same screen.
#   ops     the operations, within one service group (SVC-X-G-n and VM-X-G-n are one family);
#           pms-map records each pushed operation as a KEY#operation sub-task.
#   tables  the tables, within one schema (MIG-S and VM-MIG-S); sub-tasks are KEY#schema.table.

SCREEN_KEY = re.compile(r"(?:APP-[A-Z]+|VM)-([A-Z]+-\d{3,}[A-Z]?)")
# MIG-<SCHEMA>-<n> (1 October): a forward migration a later app-module adds to a schema the first release created
# (the baseline is frozen at r1); the schema is still its family.
TABLES_KEY = re.compile(r"(?:VM-)?MIG-([A-Z0-9_]+)(?:-\d+)?")
OPS_KEY = re.compile(r"(?:SVC|VM)-(.+)-(\d+)")


def key_identity(key: str):
    """(kind, family) for a key whose work has an identity, else None. Screens first: VM-BO-005 would
    also read as an operations key."""
    m = SCREEN_KEY.fullmatch(key)
    if m:
        return "screen", m.group(1)
    m = TABLES_KEY.fullmatch(key)
    if m and m.group(1) not in ("BASELINE",):
        return "tables", m.group(1).lower()
    m = OPS_KEY.fullmatch(key)
    if m:
        return "ops", m.group(1)
    return None


def pushed_items(mp: dict) -> dict[str, set]:
    """Every pushed task key -> the work its sub-tasks record (operations, tables or the screen id)."""
    items = {k: set() for k in mp if "#" not in k and not k.startswith(("_", "VERSION"))}
    for k in mp:
        if "#" in k:
            head, _, part = k.partition("#")
            if head in items and part not in ("build", "wire", "test"):
                items[head].add(part)
    for k in items:
        ident = key_identity(k)
        if ident and ident[0] == "screen":
            items[k] = {ident[1]}
    return items


def reconcile_keys(plan: dict[str, set], fixed: set, mp: dict, closed: frozenset = frozenset()):
    """Map every planned key to the key it is written under. `plan` is natural key -> its work (see above);
    `fixed` the planned keys with no such identity (epics, features, setup), which never move. `closed`
    are pushed keys closed by tools/op-retire.py: never given to other work, and a planned key that is
    closed gives way to an open ticket carrying the same work.

    A pushed key goes to the planned task whose work overlaps it most (ties: its own key first, then the
    open ticket, then the lower key), so a split keeps each ticket on the half it was made for. A task
    that matches nothing keeps its key if nobody has pushed it; one whose key was pushed for other work is
    genuinely new and takes the next number nobody has pushed. Returns ({natural: final}, [notes])."""
    pitems = pushed_items(mp)
    fam = defaultdict(list)
    for k in pitems:
        ident = key_identity(k)
        if ident:
            fam[ident].append(k)
    naturals = set(plan) | set(fixed)
    # **A pushed ticket that left the plan keeps its operations under another family too** (1 October): an
    # operation whose contract tag changed (setReaderScannerPeripheral: pushed as SVC-ACCESS-DRAFTED-1, now in the
    # ACCESS group) is the same work, so the planned task that builds it is written under the pushed key.
    by_op = defaultdict(set)
    for k, its in pitems.items():
        ident = key_identity(k)
        if ident and ident[0] == "ops" and k not in naturals:
            for o in its:
                by_op[o].add(k)
    pairs = []
    for t, work in plan.items():
        ident = key_identity(t)
        cands = list(fam.get(ident, ()))
        if ident[0] == "ops":
            cands += sorted({k for o in work for k in by_op.get(o, ())} - set(cands))
        for k in cands:
            # A closed key is never given to other work; one whose pushed work is exactly this task's is the same
            # ticket (CHG-R4-010, 6 October: op-retire.py closes SVC-CATALOGUE-DRAFTED-3 for the work it had before
            # the fresh r1, and the fresh r1 pushed it again for listBundleCombo, listPackageBundleAdd,
            # listPromotionLifecycleStatus and setProductServicePrice; once the catalogue chunks were numbered
            # from 45, that work took SVC-CATALOGUE-DRAFTED-46 and the pushed key left the plan).
            if k in fixed or (k in closed and k != t and not (pitems.get(k) and work == pitems[k])):
                continue
            if k != t and k in naturals and ident[0] == "screen":
                continue
            ov = 1 if ident[0] == "screen" else len(work & pitems[k])
            if ov == 0:
                if k != t and k in naturals:
                    continue          # another planned task's key, and none of this work is on it
                if pitems[k] and ident[0] == "ops":
                    continue          # pushed for other operations: not this work
            pairs.append((-ov, k in closed, k != t, k, t))
    final, taken = {k: k for k in fixed}, set(fixed)
    for _, _, _, k, t in sorted(pairs):
        if t not in final and k not in taken:
            final[t] = k
            taken.add(k)
    # **Greedy can strand a pushed key** (1 October): the waiting-room operations entered the slice, the
    # four-operation chunks of catalogue/event shifted, and the new second chunk overlapped pushed
    # SVC-CATALOGUE-EVENT-1 most (3) -- so it took that key, and SVC-CATALOGUE-EVENT-2, whose work
    # (updateEvent, updatePerformance) was on that same chunk, left the plan: a renamed key. A pushed key
    # left unmatched while it overlaps planned work is given back by an augmenting path (planned task ->
    # its key -> another planned task with no key yet that overlaps it), so every pushed key that can keep
    # its work does. It changes nothing where greedy already matched every overlapping pushed key.
    adj = defaultdict(list)                      # pushed key -> planned tasks overlapping it, best first
    for ov, _, _, k, t in sorted(pairs):
        if ov < 0:
            adj[k].append(t)
    owner = {k: t for t, k in final.items() if t not in fixed}

    def augment(k, seen):
        for t in adj[k]:
            if t in seen or t in fixed:
                continue
            seen.add(t)
            cur = final.get(t)
            if cur is None or (cur in adj and augment(cur, seen)):
                final[t] = k
                owner[k] = t
                return True
        return False

    for k in sorted(adj):
        if k not in taken and augment(k, set()):
            taken.add(k)
    notes = []
    for t in sorted(plan):
        if t not in final and t not in pitems and t not in taken:
            final[t] = t
            taken.add(t)
    # Every other key is settled now, so a new number only has to avoid the pushed keys and the settled
    # ones; a key its own task gave up (a split's renamed half) is free.
    for t in sorted(plan):
        if t in final:
            continue
        ident = key_identity(t)
        if ident and ident[0] == "ops":
            stem = t[:t.rfind("-")]
            n = 1
            while f"{stem}-{n}" in pitems or f"{stem}-{n}" in taken:
                n += 1
            final[t] = f"{stem}-{n}"
            notes.append(f"{t}: pushed for other work, so this work is new and takes {final[t]}")
        elif ident and ident[0] == "tables" and t in taken:
            # **Its own key already went to other work** (2 October 2026, CHG-CLN-015): the greedy pass gave the
            # pushed VM-MIG-FNB to MIG-FNB-4, which overlapped it most, and VM-MIG-FNB itself was then written under
            # the same key -- two tasks, one key, and the assertion below stopped every refresh. A migration task whose
            # key is taken takes the next number nobody has pushed (MIG-X-n), as an operations task does.
            stem = re.sub(r"-\d+$", "", t)
            n = 1
            while f"{stem}-{n}" in pitems or f"{stem}-{n}" in taken:
                n += 1
            final[t] = f"{stem}-{n}"
            notes.append(f"{t}: its key went to other work, so this work is new and takes {final[t]}")
        else:
            final[t] = t
            notes.append(f"{t}: keeps its key, which was pushed for other work")
        taken.add(final[t])
    for t, k in sorted(final.items()):
        if k != t and k in mp:
            notes.append(f"{t} -> {k}: the same work is already ticket #{mp.get(k)}")
    assert len(set(final.values())) == len(final), "key reconciliation gave two tasks one key"
    return final, notes


def closed_keys() -> frozenset:
    """Pushed keys tools/op-retire.py closes as merged into another ticket (Rejected in OpenProject)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("op_retire", ROOT / "tools" / "op-retire.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        return frozenset()
    return frozenset([k for k, (kind, _, _) in mod.OTHER.items() if kind == "merge"]
                     + list(getattr(mod, "REPLACED", {})) + list(getattr(mod, "MERGED_R2", {})))


def replaced_screens() -> frozenset:
    """**Screens whose pushed ticket op-retire.py closes as replaced** (r2, CHG-CLN-002): the 13 section screens whose
    duplicate writer was removed from the contract. Each renders inside its venue screen's component, and that
    screen's ticket builds it, so it gets no task of its own; planned, its pushed key would have carried on as a
    later-block task and the "replaced by" note would never be sent."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("op_retire", ROOT / "tools" / "op-retire.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception:
        return frozenset()
    out = set()
    for k in getattr(mod, "REPLACED", {}):
        ident = key_identity(k)
        if ident and ident[0] == "screen":
            out.add(ident[1])
    return frozenset(out)


# **Only an operation that can create a row makes a table non-empty** (2 October, CHG-GTB-012; audit R064).
# The slice adds every setup writer of a table the release reads, so `updatePerformance`, `updateMenu`,
# `updateRotaAssignment` and `deleteReport` were labelled as making their tables non-empty, which only a create
# (or a PUT upsert) can do. The same rule check-ticket-text (T-NONEMPTY-LABEL) applies; the slice is unchanged.
_CHANGES_ONLY = re.compile(r"(update|approve|reject|escalate|cancel|delete|remove|archive|close|suspend|resume|"
                           r"acknowledge|withdraw|revoke|disable|deactivate)")

def _enables_label(op: str, verb: str, enables) -> str:
    if not enables:
        return ""
    tables = ", ".join("`" + t + "`" for t in enables)
    if str(verb).upper() in ("PATCH", "DELETE") or _CHANGES_ONLY.match(op):
        return f", changes rows of {tables} that another operation creates"
    return f", makes {tables} non-empty"


def main() -> int:
    # Read before anything is written: the file names the last run gave the forward migrations (CHG-TBF-002).
    prior_files = {} if "--renumber-migrations" in sys.argv[1:] else prior_migration_files()
    sl = json.loads((HANDOFF / "delivery-slice.json").read_text(encoding="utf-8"))
    lineage = json.loads((HANDOFF / "api-data-lineage.json").read_text(encoding="utf-8"))
    decomp = json.loads((HANDOFF / "service-decomposition.json").read_text(encoding="utf-8"))
    ref = json.loads((HANDOFF / "schema-reference.json").read_text(encoding="utf-8"))
    cols = ref["cols"]
    services = decomp["services"]
    tiers = decomp["tiers"]
    ops = read_operations()
    screens = all_screens()
    merged_in = ticket_done.merge_bindings(screens)     # a merged screen's operations are its target's (CHG-FXP-002)
    # **A decided app-module's wiring is not the wired screen's ticket** (CHG-R4-003, 5 October): the kiosk configuration
    # read is wired into KSK-001 (an A1 screen) and five later kiosk screens, and the kiosk assignment into ADM-582, by
    # the Block A2 app-module's own tasks. Taken off those screens here, in memory, so their tickets keep the scope,
    # points and waits they were pushed with; the wiring tasks are made with the app-module below.
    decided_ams = block_a_decisions()["appModules"]
    wired_off = ticket_done.strip_wiring(screens, decided_ams)
    print(f"operations a decided app-module wires into screens other tickets build: "
          f"{sum(len(v['ops']) for v in wired_off.values())} on {len(wired_off)} screens")
    print(f"operations a merged screen brings to the screen it is merged into: {sum(map(len, merged_in.values()))} "
          f"on {len(merged_in)} screens")
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
                         ["Part of slice", so["part"] + _enables_label(o, x["verb"], so["enables"])],
                         ["Wave", wave[o]], ["Offline", "yes" if x["offline"] else "no"]]
                for label, key in (("Config scope", "configScope"), ("Conflict policy", "conflict"),
                                   ("Read routing", "routing"), ("Step-up auth", "stepUp"),
                                   ("Lock", "lock"), ("Guest callable", "guestCallable"),
                                   ("Offline note", "offlineNote")):
                    if x.get(key):
                        facts.append([label, first_sentence(x[key], 300) if key == "offlineNote" else x[key]])
                if x["provisional"]:
                    facts.append(["Status", {"stub": "**Stub**: its shape is a proposal; do not build until confirmed",
                                             "deprecated": "**Deprecated**: superseded; do not build"}.get(
                        x.get("hold"), "**Provisional**: not yet agreed; do not build")])
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
    PACE = team.get("pace") or {}
    HELPER_SHARE = team.get("helperShare") or {}
    areas = team.get("areas") or {}
    # **Every migration is one person's** (team.json `migrations`, CHG-R5-001, 7 October): a task whose key matches the
    # rule is given to its owner after the pins of the last release, so a pushed migration moves to them too, and the
    # final schedule times it on them; its table sub-tasks follow it (op-release.py). Not earlier: the passes that
    # split Block A into A1 and A2 and fill Blocks B-D keep the owners they had, so moving the migrations moves no
    # app-module into another block (measured 7 October: giving them to one person before those passes took seven
    # apps' completion work out of A1, which the pushed tickets would have followed).
    MIG_OWNER, MIG_RX = sp.migration_owner(team)
    tasks = []

    # **Frontend or backend is on every task, and in its OpenProject subject**, so a board, a filter or a
    # person scanning a list can tell them apart without opening the ticket.
    PREFIX = {"Frontend": "[FE]", "Backend": "[BE]", "Database": "[DB]", "DevOps": "[DevOps]",
              "Onboarding": "[Onboarding]", "Full stack": "[FE+BE]", "Setup": "[Setup]",
              "AI": "[AI]", "Test": "[Test]"}

    def track_of(key, area):
        if key.startswith(("MIG", "VM-MIG", "VM-DB")):
            return "Database"
        if key == "SETUP":
            return "Setup"
        if key == "VM":
            return "Full stack"
        if area == "VM":
            return "Frontend" if key.startswith(("VM-BO-", "VM-FE")) else "Backend"
        return {"devops": "DevOps", "onboard": "Onboarding", "backend": "Backend",
                "ai": "AI", "test": "Test"}.get(area, "Frontend")

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
    # one-line description sent people to guess both. The provider is decided (28 September, audit
    # R057): Azure in a UAE region, Terraform `azurerm`, CI on GitHub Actions, secrets in Azure Key
    # Vault per cell, dependencies per setup/dependencies.md -- so the tasks name it rather than
    # leave CF-64 open in the plan. The seed is the reference fixture every test
    # runs against (quality-gates 8), not a single demo venue (R034). The migration runner applies
    # the derived DDL forward and records each file; there is no ROLLBACK section to run (R046).
    SETUP = [
        ("SETUP-CI", "CI pipelines for the backend and frontend repositories", 3, [],
         "In **ticvai-backend** and **ticvai-frontend** (the repositories the setup zip creates). CI is GitHub "
         "Actions (decided 28 September, audit R057). Done when: every merge request runs build, tests and lint "
         "in both, a red run blocks the merge, and a failing test on a branch shows in the MR. Tool versions per "
         "setup/dependencies.md."),
        ("SETUP-ENV", "Dev and staging environments (Terraform, ADR-0007 infra repository)", 5, [],
         "In **ticvai-infra** (ADR-0007: one parameterised `cell` module, one tfvars per environment). The "
         "provider is Azure in a UAE region, Terraform `azurerm`, with each cell's secrets in its Azure Key Vault "
         "(decided 28 September, audit R057). Done when: `terraform plan` and `apply` build dev and staging from "
         "nothing, state is remote and locked, and the cell mapping and Azure region are written in the infra "
         "README."),
        ("SETUP-DB", "PostgreSQL (tenant and control databases) and a forward-only migration runner that applies the MIG epic in order", 5, ["SETUP-ENV"],
         "In **ticvai-backend**: `SqlMigrationRunner` (in the starter) applies `db/tenant` and `db/control` - the "
         "package's derived DDL - in file order and records each file with its checksum in "
         "`platform.schema_version`. The databases run on Azure in the UAE region, connection strings from the "
         "cell's Key Vault (audit R057). Done when: both databases exist in dev, the runner applies every MIG file "
         "to an empty database, and a second run applies nothing."),
        ("SETUP-SEED", "Seed data: the reference fixture (two brands, three regions, AED and OMR) every test runs against", 5, ["SETUP-DB"],
         "In **ticvai-backend** `db/seed`: the reference fixture quality-gates 8 requires - two brands, three regions "
         "across two countries, AED and OMR - with products, prices, events, tills, staff, roles and "
         "denominations, so apps can be built before the Back Office setup screens exist. The denominations and "
         "roles seed from docs/active/seed-data-proposal.md (proposed, client to correct - audit R229). Done when: "
         "it loads on a migrated database, integration tests run against it, and the frontend mock server serves "
         "the same data."),
        ("SETUP-CLIENTS", "Generate the typed API clients from contracts/ for the frontend workspace", 3, ["SETUP-CI"],
         "In **ticvai-frontend** `packages/api-client`: generated from the package's `contracts/`, re-generated by "
         "one command and checked in CI on GitHub Actions (audit R057). Done when: every in-release operation has "
         "a typed call, the build fails if the contracts change without a re-generate, and screen tickets stop "
         "stubbing calls."),
        ("SETUP-AUTH", "Sign-in working end to end against IdentityService", 5, ["SETUP-DB"],
         # **Names the operations it wires** (4 October, the Sprint 1-2 judging; CHG-FXP-005): "the identity sign-in
         # operations" named none and the pull linked nothing, so request, response and the permission set were unknown.
         "Builds: `operation login`, `operation refreshToken`, `operation logout`, `operation getCurrentSession`. "
         "The staff sign-in path of contracts/spine/identity.yaml: `login` issues the session and refresh token, "
         "`getCurrentSession` returns the Session with `effectivePermissions` and `permissionsByScope` (the effective "
         "permissions the done-when reads), `refreshToken` and `logout` end the loop; the operations themselves are "
         "built on their IdentityService tickets, this task wires them through the host. "
         "In **ticvai-backend** and **ticvai-frontend**: the identity sign-in operations, `ICurrentPrincipal` and "
         "`ITenantContext` filled from the session, signing keys from the cell's Azure Key Vault (audit R057). "
         "Done when: a seeded staff member signs in from a web app and an app, gets their effective permissions, "
         "and a request without a session gets 401."),
        ("SETUP-OBS", "Logging and monitoring basics", 2, ["SETUP-ENV"],
         # Concrete from what it stands on (3 October, CHG-TBF-007): docs/architecture/observability.md (the layers
         # and the no-PII rule), R057 (Azure UAE, Key Vault per cell), ADR-0055 (the five deployables), ADR-0009 (logs
         # PII-free by construction). The tenant and venue attributes and the dashboards are PLATFORM-OBSERVE's; the
         # relay-lag alert ADR-0058 asks for and the SLO dashboards of ADR-0060 come after it.
         "In **ticvai-infra** (Terraform, in the `cell` module) and **ticvai-backend**: the OpenTelemetry SDK (already "
         "referenced by the starter) in each of the five deployables of ADR-0055 (commerce, access, operations, workers "
         "and ticvai-ai), exporting traces, metrics and logs over OTLP to an OpenTelemetry Collector in the cell, which "
         "writes them to the cell's Log Analytics workspace in Azure UAE North (audit R057; nothing leaves the region). "
         "Logs are structured, never concatenated, and carry the trace and correlation ids; they never hold guest "
         "names, emails, phone numbers, document numbers, card data or biometric templates, only the opaque subject "
         "id (docs/architecture/observability.md; ADR-0009: PII-free by construction, not by filtering). Metrics are "
         "Prometheus-compatible. One alert rule to start with (the 5xx rate of each host) goes to an Azure Monitor "
         "action group that emails the on-call person (DevOps until a rota exists). Dev and staging only; production is built "
         "before the first live tenant. Done when: a request to a dev host can be followed from its log line to its "
         "trace by the correlation id; a deliberate 500 on a dev host raises an alert the on-call person receives "
         "within five minutes; and a search of a day's dev logs after the seeded test run finds no email address, "
         "phone number or card number."),
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

    # --- client-side prerequisites (audit R065, R252) were tickets here until 30 September. They are
    # the client's to answer, not work anyone on the team can pull, so they moved to the sheet the
    # client answers: "For you to answer" in handoff/TICVAI - Decisions Register.xlsx
    # (tools/build-decisions-workbook.py). Acceptance that waits on them says so in its own text.

    # --- backend: one epic per service, a feature per tag, and tasks of at most four operations,
    # because a 30-operation feature cannot be estimated, started or finished as one thing.
    svc_key = {n: "SVC-" + re.sub(r"Service$", "", n).upper() for n in by_service}
    op_task: dict[str, str] = {}
    svc_points = defaultdict(int)
    chunks = []
    # **An operation the AI engine serves is built by its AI engine task** (CHG-RONEP-001, 3 October): sendGuestConversationMessage
    # and getGuestConversation by AI-ENGINE-CONCIERGE, setAiProvider and setAiCredential by AI-ENGINE-GATEWAY
    # (block-a-extra-tasks.json `operations`). They take no back-end chunk; the task is created with the extra tasks below.
    decided = block_a_decisions()
    # **A screen the spec says is not built gets no task** (4 October, the Sprint 1-2 judging; CHG-FXP-002, -003):
    # merged into another screen ("**Merged into BO-666**": VM-BO-669 was planned in Sprint 2), listed in
    # block-a-extra-tasks.json `screensNotBuilt` (a replaced page, a screen nobody could define), or binding an
    # operation that is not built (provisional, a stub whose shape is a proposal, deprecated: WEB-027 was planned on
    # getMarketingSubscription and setMarketingSubscription). Its pushed ticket gets its reason from op-retire.py.
    held_screen = ticket_done.screen_holds(screens, {o: x["hold"] for o, x in ops.items() if x.get("hold")},
                                           decided["screensNotBuilt"])
    print(f"screens given no build task (merged, listed or binding a held operation): {len(held_screen)}")
    ai_ops = {o: k for o, k in decided["aiEngineOperations"].items() if o in ops}
    for n, olist in sorted(by_service.items()):
        groups = defaultdict(list)
        for o in olist:
            if o in ai_ops:
                continue
            # a slice operation the contract marks a stub, provisional or deprecated is not put on a build ticket
            # either (CHG-FXP-003: SVC-MARKETING-MARKETING-2 built getMarketingSubscription, a proposal)
            if ops[o]["provisional"]:
                continue
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
    op_task.update(ai_ops)
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
    # **Machinery no operation reads or writes is still storage the first release runs on** (CHG-TBF-003). The
    # inbox and the relay lease are written by the kernel (ADR-0058), so no lineage reaches them and they were in no
    # migration, while PLATFORM-OUTBOX and MIG-PARTITIONS in the same sprint stand on them.
    for t, reason in MACHINERY_TABLES.items():
        if t in ddl and t not in rel:
            rel.add(t)
            why[t] = reason
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
    task("MIG-BASELINE", "MIG", "Task", "Migration V0001__baseline.sql: schemas, extensions, migration register, "
         "RLS helper functions and the monthly partition helpers (ADR-0056)",
         # `platform.schema_version` is the one table the baseline creates (CHG-TBF-003): named, so it is not a table
         # with no migration.
         "Tables: platform.schema_version. Source DDL: backend/tenant/000-schemas.sql, 001-extensions.sql, 002-migration-register.sql, the helper "
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
             f"{g[0].capitalize()} database. Tables: " + ", ".join(ts) + f". Source DDL: {src_files(ddl, ts)} and the "
             f"matching rows of 900-foreign-keys, 910-indexes and 920-row-level-security. "
             + (f"Its keys into schemas created later ({deferred[g]}) go in MIG-FOREIGN-KEYS. " if g in deferred else "")
             + "Applied forward by SqlMigrationRunner; test that it applies to a database with its Follows applied and that a second run applies nothing.", 1, service=svc, pts=pts, area="backend", assignee=who,
             depends=["MIG-BASELINE"] + back)
        migrations.append([i - 1, mig_key[g], fname, g[0], g[1], len(ts), n_cols,
                           ", ".join(r.replace("MIG-", "").lower() for r in refs),
                           MIG_OWNER if MIG_OWNER and sp.is_migration_of(MIG_RX, mig_key[g]) else who, pts, svc])
    if deferred:
        n_def = sum(deferred.values())
        # **The ticket names its keys and links their tables** (4 October, the Sprint 1-2 judging; CHG-FXP-005): it said
        # "From 900-foreign-keys.sql." and linked nothing, so the 35 keys were in no file the developer pulled. Each
        # key is named (table, column, referenced table, constraint) and each table it alters is a build, whose table
        # record carries the key's full DDL. "Builds:", not "Tables:": the tables are created by their own migrations.
        pos_ = {g: i for i, g in enumerate(mig_order)}
        fk_rows = []
        for db_ in ("tenant", "control"):
            f_ = ROOT / "backend" / db_ / "900-foreign-keys.sql"
            for ln_ in (f_.read_text(encoding="utf-8").splitlines() if f_.exists() else []):
                m_ = re.match(r"ALTER TABLE (\w+\.\w+) ADD CONSTRAINT (\w+) FOREIGN KEY \(([^)]*)\) REFERENCES (\w+\.\w+)", ln_)
                if not m_ or m_.group(1) not in rel or m_.group(4) not in rel:
                    continue
                ga_, gb_ = (db_, m_.group(1).split(".")[0]), (db_, m_.group(4).split(".")[0])
                if ga_ in pos_ and gb_ in pos_ and pos_[gb_] > pos_[ga_]:
                    fk_rows.append((m_.group(1), m_.group(3).replace(" ", ""), m_.group(4), m_.group(2), db_))
        fk_tables = sorted({r_[0] for r_ in fk_rows})
        task("MIG-FOREIGN-KEYS", "MIG", "Task", f"Migration V{len(mig_order) + 2:04d}__cross_schema_foreign_keys.sql "
             f"({n_def} keys)", ("Builds: " + ", ".join(f"`table {t_}`" for t_ in fk_tables) + ". " if fk_tables else "")
             + "The foreign keys that point from a schema into one created after it: "
             + ", ".join(f"{g[1]} ({n})" for g, n in sorted(deferred.items())) + ". Each is the ALTER TABLE ... ADD "
             "CONSTRAINT line of backend/<db>/900-foreign-keys.sql with that constraint name, unchanged (each linked "
             "table's record lists its keys with ON DELETE): "
             + "; ".join(f"{a_}({c_}) -> {b_} as {n_}" for a_, c_, b_, n_, _ in sorted(fk_rows)) + ". Done when: "
             "after every schema migration, this one adds exactly these keys on an empty database and on the previous "
             "release's schema, a second run applies nothing, and a row pointing at a missing parent is refused.",
             1, pts=points_of(1 + n_def / 10), area="backend", assignee=devops,
             depends=[mig_key[g] for g in groups])
        migrations.append([len(mig_order) + 1, "MIG-FOREIGN-KEYS",
                           f"V{len(mig_order) + 2:04d}__cross_schema_foreign_keys.sql", "tenant", "(cross-schema)",
                           0, 0, "", devops, points_of(1 + n_def / 10), ""])
    MIG_COLS = ["Order", "File", "Task", "Database", "Schema", "Tables", "Columns", "References", "Assignee",
                "Points"]
    tables_rows = []
    for t in sorted(rel, key=lambda x: (mig_order.index((ddl[x]["db"], x.split(".")[0])), x)):
        tables_rows.append([table_mig[t], t, ddl[t]["db"], len(ddl[t]["columns"]), ddl[t]["policy_label"],
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
            if sid in held_screen:
                continue
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
    uncovered = {o for o, d in slice_ops.items() if d["part"] == "setup" and not ops[o]["provisional"]}
    hosts = defaultdict(set)
    for o in uncovered:
        for sid in slice_ops[o]["screens"]:
            # a merged screen's operation is set up on the screen it renders inside (CHG-FXP-002: ADM-243's
            # setApprovalMatrix on BO-087)
            if (held_screen.get(sid) or ("",))[0] == "merged" and held_screen[sid][1] in screens:
                sid = held_screen[sid][1]
            if sid not in first_release and sid not in held_screen:
                hosts[sid].add(o)
    no_screen = sorted(o for o in uncovered if not any(o in v for v in hosts.values()))
    uncovered -= set(no_screen)
    setup_screens = {}
    # **A pushed setup screen stays the host** (4 October, CHG-FXP-002): taking a merged screen out of the hosts
    # (ADM-243) re-ran the greedy cover and moved createAiGovernancePolicyDraft from ADM-523, a Sprint 2 ticket, to
    # ADM-530. A screen whose APP-SETUP ticket is pushed is preferred while it still hosts something uncovered.
    _mp = OUT / "pms-map.json"
    pushed_hosts = ({k[len("APP-SETUP-"):] for k in json.loads(_mp.read_text(encoding="utf-8"))
                     if k.startswith("APP-SETUP-") and "#" not in k and not k.endswith("-REST")} if _mp.exists() else set())
    # **A planned setup screen stays the host too** (4 October, CHG-RFM-006). After the fix round a tie in the cover
    # (explainMetricChange, hosted by ADM-505 and ADM-506 alike) went to the first in id order, so ADM-506 left Block A
    # for Block D and ADM-505, reached only through a screen outside Block A, came in (C-REACH, C-UNTICKETED). The
    # plan this run replaces (plan-tasks.csv) names its hosts; one still hosting something uncovered is preferred
    # after a pushed one and before the count.
    _pt = OUT / "plan-tasks.csv"
    planned_hosts = set()
    if _pt.exists():
        with _pt.open(encoding="utf-8", newline="") as fh:
            planned_hosts = {r["key"][len("APP-SETUP-"):] for r in csv.DictReader(fh)
                             if r["key"].startswith("APP-SETUP-") and not r["key"].endswith("-REST")
                             and r.get("type") == "Task"}
    while uncovered:
        sid = max(sorted(hosts), key=lambda x: (bool(hosts[x] & uncovered) and x in pushed_hosts,
                                                bool(hosts[x] & uncovered) and x in planned_hosts,
                                                len(hosts[x] & uncovered), x.startswith("BO")))
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
            task(f"APP-SETUP-{sid}", "APP-SETUP", "Task", f"{sid} {s['name']} ({setup_scope(s, so)})",
                 "In the slice: " + ", ".join(so), min(wave[o] for o in so),
                 platform=s["_platform"].get("shortName", ""), depends={op_task[o] for o in so},
                 pts=sizes[sid], area="SETUP", assignee=assign("SETUP", sizes[sid]))
    # --- Venue Management, full stack (team.json "venueManagement"): the back-office screens of the named
    # waves whose operations are all agreed (not provisional) and specified (have lineage), minus the ones
    # APP-SETUP already builds. Their operations beyond the slice are new backend, sized and chunked the
    # same way as the slice's, and the tables those reach beyond the slice get migrations of their own.
    vm = team.get("venueManagement") or {}
    vm_rows = []
    vm_mig, vm_op_task = {}, {}
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
            if not sid.startswith("BO-") or s_.get("wave") not in vm["waves"] or sid in setup_screens                     or sid in held_screen:
                continue
            if any(sid in (a.get("screens") or []) for a in decided_ams):
                continue                 # built by its decided app-module, in its block (CHG-R4-003)
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
            task(k, "VM-DB", "Task", f"Forward migration: {sch} for Venue Management ({len(ts)} tables)",
                 "Tables: " + ", ".join(ts) + f". Source DDL: {src_files(ddl, ts)}. Additive to the first release; "
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
            # **Load is compared at each person's pace** (team.json "pace", 30 September): Surendra at
            # about 60% takes about 60% of an equal share.
            who = min(vm_team, key=lambda x: (load[x] / PACE.get(x, 1.0), x))
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
    # **Block A is balanced on Block A's own load** (1 October): the Venue Management waves 1-2 are planned with
    # Block B onwards now, so a first-release task is shared out against first-release loads only; otherwise a
    # helper with Venue Management screens takes no first-release back end while the owners run past Sprint 4.
    vm_load = Counter()
    for x in tasks:
        if x["type"] == "Task" and x["phase"] == 2 and x["assignee"]:
            vm_load[x["assignee"]] += int(x["points"] or 0)

    for t_ in sorted((x for x in tasks if x["type"] == "Task" and x["track"] == "Backend" and x["points"]),
                     key=lambda x: (x["phase"], int(x["wave"] or 9), step_of(x["key"]), x["key"])):
        pts, owner = int(t_["points"]), t_["assignee"]
        able = [h for h, cap in helpers.items() if pts <= cap and h != owner]
        if not able:
            continue

        def L(x):
            return load[x] - (vm_load[x] if t_["phase"] == 1 else 0)
        # **A helper's share is proportional to their rating** (team.json "helperShare", 30 September):
        # Deep at .NET 2 against owners at 3-4 carries about 55% of an owner's load, not an equal share. The
        # helpers are tried in turn (least helper work first), so one at their share passes the task to the next.
        def fits(h):
            share = HELPER_SHARE.get(h)
            return (L(h) + pts <= share * (L(owner) - pts)) if share else (L(h) + pts <= L(owner) - pts)
        h = next((x for x in sorted(able, key=lambda x: (taken[x], L(x), x)) if fits(x)), None)
        if h:
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
            who = min(vm_team_, key=lambda y: (load[y] / PACE.get(y, 1.0), y))
            x["assignee"] = who
            load[who] += int(x["points"] or 0)

    def extra_lead(t_):
        """**What a hand-written task builds leads its text** (CHG-RONEP-001, CHG-RONEP-003): the operations an AI engine task
        serves (`operations`) and the artefacts it lists (`builds`: operation, table, screen, service or adr ids), in the
        "Builds:" form ticket_done.builds_of reads. Without it the task's title was read as operations (r1 gate, G2)."""
        served = sorted(o for o in t_.get("operations") or [] if o in ops)
        items = [f"operation {ops[o]['contract']}#{o}" for o in served]
        for b in t_.get("builds") or []:
            kind, _, name = b.partition(" ")
            b = f"operation {ops[name]['contract']}#{name}" if kind == "operation" and name in ops else b
            if b not in items:
                items.append(b)
        if not items:
            return ""
        lead = "Builds: " + ", ".join(f"`{b}`" for b in items) + ". "
        if served:
            lead += (f"{', '.join(served)} {'is' if len(served) == 1 else 'are'} served by ticvai-ai behind the AI gateway, "
                     "to their contracts at the release tag in ADAM; no back-end task builds them. ")
        return lead

    # **Tasks no screen or operation implies** (docs/active/block-a-extra-tasks.json, 30 September): the
    # platform kernel and offline machinery the system-design review found unticketed (SD-047, SD-063), and
    # the AI engine work the two AI engineers carry. Backend-pool tasks go to the least-loaded owner, as
    # services do; AI engine tasks carry no points, because the AI engineers' capacity is separate.
    if EXTRA.exists():
        ex = json.loads(EXTRA.read_text(encoding="utf-8"))
        backend_ = areas.get("backend") or []
        for e in ex.get("epics") or []:
            task(e["key"], "", "Epic", e["subject"], e["detail"], 1, area=e.get("area", "backend"))
        for t_ in ex.get("tasks") or []:
            # **A task for a later block is recorded, not ticketed** (1 October): the ADRs of that day name
            # build work for B1 (the waiting room, the admission rule evaluators), kept beside the Block A
            # tasks so it is not lost, and cut into tickets when that block is planned.
            if str(t_.get("block") or "A") != "A":
                continue
            is_ai = t_["epic"] == "AI-ENGINE"
            pts = "" if is_ai else int(t_["points"])
            who = t_.get("assignee") or (min(backend_, key=lambda x: load[x]) if backend_ else "")
            if not is_ai and who:
                load[who] += pts
            task(t_["key"], t_["epic"], "Task", t_["subject"], t_["subject"] + ". " + extra_lead(t_) + t_["detail"], 1,
                 pts=pts, area="ai" if is_ai else "backend", assignee=who, depends=t_.get("depends") or ())

    # ================================================================ the rest of the package (1 October)
    # **Every block is planned task by task now**, not only Block A: the PM's replan wants module-wise completion
    # per app, in blocks that can each be tested end to end. Block A is the work above (the first release and its
    # platform, AI engine and Venue Management waves 1-2 tickets). Everything else the package specifies is formed
    # here with Block A's own formulas: one task per screen (the screen formula), the operations a screen needs in
    # tasks of at most four by service and group (the operation formula), and a forward migration per schema for the
    # tables they reach that no earlier migration creates. Which app-module and block each lands in is decided
    # below (the sprint plan); the keys follow the same rules as Block A's, so a ticket keeps its key once pushed.
    kmap_early = json.loads((OUT / "pms-map.json").read_text(encoding="utf-8")) if (OUT / "pms-map.json").exists() else {}
    op_module = {o: sp.MODULE_OF_CONTRACT.get(x["contract"], "Platform Operations") for o, x in ops.items()}

    def screen_module(sid):
        if sid in decided["screenModules"]:
            m_ = decided["screenModules"][sid]
            if m_ not in sp.MODULE_PHASE:          # a display name ("Identity & Security") made an AM-X app-module
                raise SystemExit(f"block-a-extra-tasks.json screenModules {sid}: {m_!r} is not a module of sprint_plan")
            return m_
        s_ = screens[sid]
        mods = Counter(op_module[a["operationId"]] for a in s_.get("apis") or []
                       if isinstance(a, dict) and a.get("operationId") in op_module)
        return mods.most_common(1)[0][0] if mods else sp.PLATFORM_MODULE.get(s_["_platform"]["code"], sp.FOUNDATION)

    def plat_of(sid):
        return screens[sid]["_platform"]["code"]

    def screen_ops(sid):
        return [a["operationId"] for a in screens[sid].get("apis") or []
                if isinstance(a, dict) and a.get("operationId") in ops]

    def nav_hubs(a_set):
        """The entries and app homes outside `a_set` on the shortest paths (fewest screens outside it) from each app's
        entry to its screens in `a_set`; repeated until nothing more is added. tools/check-plan-closure.py's C-REACH
        checks the result."""
        added = set()
        while True:
            hubs = set()
            for pf, theirs in sorted(screens_by_plat(a_set | added).items()):
                for path in shortest_paths(pf, a_set | added, theirs).values():
                    # **app homes only** (lever A, Chinmay, 3 October, CHG-RONEP-007): an entry or a section home
                    # (block-a-extra-tasks.json `navHomes`); a screen reached only through another hub (a command
                    # centre) gets a link from its section home in the screens instead (C-REACH reports it until then)
                    hubs |= {x for x in path if x not in a_set and x not in added
                             and (sp.is_entry(screens[x]) or x in decided["navHomes"])}
            if not hubs:
                return added
            added |= hubs

    def screens_by_plat(sids):
        out = defaultdict(set)
        for sid in sids:
            if sid in screens:
                out[plat_of(sid)].add(sid)
        return out

    def shortest_paths(pf, a_set, targets):
        return sp.nav_paths({sid: s_ for sid, s_ in screens.items() if plat_of(sid) == pf}, a_set, targets)

    built_screen = {}
    for t_ in tasks:
        ident = key_identity(t_["key"]) if t_["type"] == "Task" and t_["track"] == "Frontend" else None
        if ident and ident[0] == "screen":
            built_screen[ident[1]] = t_["key"]
    mig_of = dict(table_mig)
    mig_of.update(vm_mig)
    later_op_task, later_mig, later_items = {}, {}, []      # later_items: (key, module, platform, kind) per screen
    later_ams = {}                                          # (module, platform) -> [(sid, key, pts, kind)]
    decided_screen = {sid: am["key"] for am in decided_ams for sid in am.get("screens") or [] if sid in screens}
    decided_op = {o: am["key"] for am in decided_ams for o in am.get("operations") or [] if o in ops}
    fam_used = defaultdict(set)                             # ops family -> numbers planned or pushed

    def note_family(k):
        m = OPS_KEY.fullmatch(k)
        if m and not SCREEN_KEY.fullmatch(k):
            fam_used[m.group(1)].add(int(m.group(2)))

    for k in list(by_key) + [k for k in kmap_early if "#" not in k]:
        note_family(k)
    planned_ops = set(op_task) | set(vm_op_task)
    setup_sizes = {sid: points_of(1 + 0.6 * len(v)) for sid, v in setup_screens.items()}
    # **Block A completes all the functionality of its apps** (Chinmay, 1 October): Guest Web, Guest App, POS and
    # the Kitchen Display (team.json sprintPlan.blockAApps). So Block A is the first-release slice plus its closure:
    # every screen of those apps, every operation they bind to, and every screen and operation in the steps (and
    # the screens resolving the branches) of any flow that runs through one of them -- Venue Management setup, Staff
    # App or Kiosk screens included -- with the back end and tables they need. Work outside the slice that the
    # closure takes is cut out of its module-on-an-app into a "(Block A)" part, under the keys it already has.
    a_apps = set(sp.sprint_settings(team)["blockAApps"])
    need_screens = {sid for sid in screens if plat_of(sid) in a_apps and str(screens[sid].get("wave")) != "4"}
    need_ops, a_flows = set(), []
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        fd = load_yaml(f) or {}
        if not ({str(x).split()[0] for x in fd.get("platforms") or []} & a_apps):
            continue
        a_flows.append(fd.get("id"))
        for st in fd.get("steps") or []:
            if not isinstance(st, dict):
                continue
            if st.get("screen") in screens:
                need_screens.add(st["screen"])
            need_ops |= {str(o).split()[0] for o in st.get("operations") or [] if str(o).split()[0] in ops}
        for br in fd.get("branches") or []:
            if isinstance(br, dict) and br.get("resolvedBy") in screens:
                need_screens.add(br["resolvedBy"])
            # a branch resolved by an operation needs it too (CHG-RONEP-002): F02's hold-expiry branches are resolved by
            # extendSeatHold, which r2 built in Block A only by riding along and the fresh plan dropped to Block C
            elif isinstance(br, dict) and str(br.get("resolvedBy") or "").split(" ")[0] in ops:
                need_ops.add(str(br["resolvedBy"]).split(" ")[0])
    # **Block A takes the door of every app it puts a screen in** (CHG-DOOR-004, Chinmay, 2 October 2026: fix
    # the Block A blockers now). Block A's Venue Management screens (BO-084, BO-085, BO-124 and the setup
    # screens) were planned with SUP-001, the only way into Venue Management, in Block B: nothing in this
    # closure reaches a door, because no flow step and no slice operation names it. A screen nobody can sign in
    # to cannot be tested end to end. So for every screen of Block A -- the closure above and the setup screens
    # the slice builds -- the door of its own platform comes too, or, where its platform has none (P08, P13,
    # P16, P14), every door of its shipped app (`platform.targetApp.app`). A door is a screen calling an
    # operation that opens a session, the same test tools/check-session-entry.py and tools/check-doors.py use.
    # **Every operation a Block A screen binds is built in Block A or earlier** (Chinmay, 3 October 2026: "Block A
    # completes its apps"; CHG-RONEP-001, docs/active/decisions/answers-3-october-r1-plan.md). The closure above took the
    # screens of the Block A apps and of their flows, but not the other screens Block A builds: the setup screens
    # (APP-SETUP-*, built "only as far as the slice needs") and the slice's own screens on other apps. A setup screen is
    # drawn whole in Block A, so its Create, Edit and list buttons reached the Block A design and the tickets while
    # their operations were planned in Blocks B to D: BO-074's createAccount, DEV-003's requestProductionAccess,
    # ADM-037's setAiProvider. So every screen a Block A task builds is in the closure -- its whole binding set (`apis`,
    # onLoad and onAction alike), and the rest of the screen with it, in Block A -- and so are the screens and
    # operations Chinmay decided on although nothing in this tree binds them yet (block-a-extra-tasks.json
    # `blockAScreens`, `blockAOperations`). tools/check-plan-closure.py checks the plan that comes out.
    #
    # **Block A ships in two drops** (Chinmay, 3 October, CHG-RONEP-007): A1 by 27 November is the closure of 1 October
    # (the Block A apps, their flows -- branches resolved by an operation included -- the slice's own screens and their
    # doors) and the payment configuration (`blockA1Operations`); the completion work this rule adds (the rest of the
    # setup screens, the decided screens and operations, the app homes) is planned in app-modules of its own, marked
    # `completion`, which go to A1 app by app while A1 still ends by its window, and to A2 otherwise (below).
    door_ops = {"login", "verifyGuestOtp", "guestSocialLogin", "guestUaePassLogin"}
    doors_of_plat, doors_of_app = defaultdict(set), defaultdict(set)
    for sid_, s_ in screens.items():
        if str(s_.get("wave")) != "4" and set(screen_ops(sid_)) & door_ops:
            doors_of_plat[plat_of(sid_)].add(sid_)
            doors_of_app[((s_["_platform"].get("targetApp") or {}).get("app"))].add(sid_)
    def add_doors():
        for sid_ in sorted(need_screens | set(setup_screens)):
            app_ = (screens[sid_]["_platform"].get("targetApp") or {}).get("app")
            need_screens.update(doors_of_plat.get(plat_of(sid_)) or doors_of_app.get(app_) or set())

    need_screens |= {sid for sid, k in built_screen.items() if by_key[k]["phase"] == 1 and not k.startswith("APP-SETUP-")}
    add_doors()
    # the homes an A1 screen is reached through are A1 too (CHG-RONEP-006, -007): the screens A1 builds are the core
    # and the setup screens (their setup part)
    need_screens |= nav_hubs(need_screens | set(setup_screens))
    add_doors()
    core_screens = set(need_screens)
    core_ops = set(need_ops) | {o for o in decided["blockA1Operations"] if o in ops}
    for sid in core_screens:
        core_ops |= set(screen_ops(sid))
    need_screens |= {sid for sid, k in built_screen.items() if by_key[k]["phase"] == 1}
    need_screens |= set(decided["blockAScreens"]) & set(screens)
    need_ops |= core_ops | {o for o in decided["blockAOperations"] if o in ops}
    # **Every Block A screen is reachable from its app's entry through Block A screens** (CHG-RONEP-006, 3 October; the
    # lead, from the design batches: eight of the nine Block A staff-app screens were reachable only through EMP-003, the
    # home on duty, in no block, and EMP-002 in Block B). From each app's entry (`navigation.isEntryPoint`), the path to
    # every Block A screen that passes the fewest screens outside Block A is found (0-1 shortest path over `exitTo` and
    # `transitions`), and those screens -- the homes and hubs -- join Block A with their bindings. A screen with no path at
    # all is a navigation gap, reported by tools/check-plan-closure.py (C-REACH), not something the plan can fix.
    need_screens |= nav_hubs(need_screens)
    add_doors()
    need_screens -= set(held_screen)       # not built (CHG-FXP-002): its operations are not Block A's for its sake
    for sid in need_screens:
        need_ops |= set(screen_ops(sid))
    print(f"Block A closure: {len(core_screens)} screens and {len(core_ops)} operations in its core (A1), "
          f"{len(need_screens - core_screens)} screens and {len(need_ops - core_ops)} operations of completion work")
    gone_screens = replaced_screens()
    for sid in sorted(screens):
        s_ = screens[sid]
        if str(s_.get("wave")) == "4" and sid not in need_screens:
            continue
        if sid in gone_screens or sid in held_screen:
            continue                     # built inside its venue screen (CHG-CLN-002), or not built (CHG-FXP-002)
        if sid in decided_screen:
            continue                     # built by its decided app-module (CHG-R4-003), placed below
        have = built_screen.get(sid)
        if have and not have.startswith("APP-SETUP-"):
            if have.startswith("VM-"):           # Venue Management waves 1-2: ticketed, planned with the rest of P08
                later_ams.setdefault((screen_module(sid), plat_of(sid)), []).append(
                    (sid, have, int(by_key[have]["points"] or 0), "ticketed"))
            continue
        if have:
            # **A setup screen is built in Block A only as far as the slice needs** (its setup operations); the rest
            # of the screen comes with its app-module, as one more task on the same screen -- in Block A since
            # CHG-RONEP-001, as the closure above holds it. The rest is every operation beyond the setup ones, also those
            # another task builds: until 3 October it was only the unplanned ones, so a screen whose other operations
            # were all planned elsewhere (BO-1065: listDenominations, getRegionSettings) had nobody wiring them.
            rest = [o for o in screen_ops(sid) if o not in setup_screens.get(sid, ())]
            if not rest or sid in ticket_done.rest_held(decided["screensNotBuilt"]):
                continue                 # nothing more, or the rest cannot be defined yet (CHG-FXP-004)
            pts = max(1, points_of(screen_raw(s_)) - setup_sizes.get(sid, 1))
            later_ams.setdefault((screen_module(sid), plat_of(sid)), []).append((sid, f"{have}-REST", pts, "rest"))
            continue
        pre = sp.SCREEN_PREFIX.get(plat_of(sid), "APP-" + plat_of(sid))
        later_ams.setdefault((screen_module(sid), plat_of(sid)), []).append(
            (sid, f"{pre}-{sid}", points_of(screen_raw(s_)), "new"))

    # **App-modules small enough to finish in one to three sprints**: a module on one app whose screens add up to
    # more than team.json `sprintPlan.fePointsPerAppModule` is cut into parts, in wave order and then by the
    # screen's section, so Venue Management's ticketed waves 1-2 come first.
    settings = sp.sprint_settings(team)
    cap = settings["fePointsPerAppModule"]
    am_of, am_info = {}, {}

    def add_am(module, platform, part, parts, variant="", block=None, name=None, order=None, key=None):
        k = key or sp.am_key(module, platform, part, variant)
        if k not in am_info:
            am_info[k] = {"key": k, "module": module, "platform": platform, "part": part, "parts": parts,
                          "variant": variant, "block": block,
                          "name": name or sp.am_name(module, platform, part, parts, variant),
                          "order": order or sp.am_order(module, platform, part, variant)}
        return k

    def setup_am(sid, rest=False):
        """Block A's setup screens (only their setup operations) are one app-module per package and app:
        "Ticketing & Guest Commerce · Venue Management (setup)", not one per module (often one screen). The rest of
        those screens (CHG-RONEP-001) is completion work in an app-module of its own beside it, "... (setup, the rest
        of the screens)", so it can ship in A1 or A2 (CHG-RONEP-007)."""
        mod, pf = screen_module(sid), plat_of(sid)
        pkg = sp.PACKAGE_OF.get(mod, "Platform Foundation")
        pi = [x[0] for x in sp.PACKAGES].index(pkg)
        code = re.sub(r"[^A-Z0-9]+", "-", pkg.upper()).strip("-")
        k = add_am(pkg, pf, None, 1, block="A", key=f"AM-SETUP-{code}-{pf}" + ("-REST" if rest else ""),
                   name=f"{pkg} · {sp.PLATFORM_NAME.get(pf, pf)} (setup" + (", the rest of the screens)" if rest else ")"),
                   order=(min(sp.MODULE_PHASE.get(m, 3) for m in sp.PACKAGES[pi][2]), 50 + pi,
                          sp.PLATFORM_ORDER.index(pf) if pf in sp.PLATFORM_ORDER else 99, 0, 1 if rest else 0))
        if rest:
            am_info[k]["completion"] = True
        return k

    def comp_am(module, platform):
        """A Block A completion app-module (CHG-RONEP-007): "<module> · <app> (Block A completion)"."""
        k = add_am(module, platform, None, 1, variant="Block A completion", block="A")
        am_info[k]["completion"] = True
        return k

    # **The decided app-modules** (CHG-R4-003): made as written, in their block, with their whole screens under the keys
    # those screens would have anywhere (the screen id is the key's identity), never cut into parts.
    for am in decided_ams:
        k = add_am(am["module"], am["platform"], None, 1, key=am["key"], name=am["name"], block=am["block"],
                   order=sp.am_order(am["module"], am["platform"], 9, "decided"))
        am_info[k]["decided"] = True
        if am.get("scheduleAfter"):
            am_info[k]["scheduleAfter"] = am["scheduleAfter"]
        for sid in am.get("screens") or []:
            if sid not in screens:
                raise SystemExit(f"block-a-extra-tasks.json appModules {k}: no screen {sid}")
            if built_screen.get(sid):
                raise SystemExit(f"block-a-extra-tasks.json appModules {k}: {sid} is already built by {built_screen[sid]}")
            pre = sp.SCREEN_PREFIX.get(plat_of(sid), "APP-" + plat_of(sid))
            later_items.append((f"{pre}-{sid}", sid, k, "new", points_of(screen_raw(screens[sid]))))
    a_plain = set()           # (module, platform) with a Block A app-module of the same name
    parts_total = {}          # (module, platform) -> how many parts it has, Block A's included
    for t_ in tasks:
        if t_["type"] == "Task" and t_["track"] == "Frontend" and t_["phase"] == 1:
            ident = key_identity(t_["key"])
            if ident and ident[0] == "screen" and not t_["key"].startswith("APP-SETUP-"):
                a_plain.add((screen_module(ident[1]), plat_of(ident[1])))
    for (module, platform), lst in sorted(later_ams.items(), key=lambda x: sp.am_order(*x[0])):
        lst.sort(key=lambda x: (int(screens[x[0]].get("wave") or 9), str(screens[x[0]].get("module") or ""), x[0]))
        # the part Block A's closure needs: with Block A's own app-module of this module on this app if it has
        # one, else a "(Block A)" part of its own
        mine = [x for x in lst if x[0] in need_screens]
        lst = [x for x in lst if x[0] not in need_screens]
        # completion work (CHG-RONEP-007): the rest of a setup screen beside its setup part, the decided screens and
        # app homes in "(Block A completion)"; the core keeps its place below
        for sid, key, pts, kind in [x for x in mine if x[0] not in core_screens]:
            later_items.append((key, sid, setup_am(sid, rest=True) if kind == "rest" else comp_am(module, platform),
                                kind, pts))
        mine = [x for x in mine if x[0] in core_screens]
        if mine:
            if (module, platform) in a_plain:
                ka = sp.am_key(module, platform, 1)
                if ka not in am_info:
                    am_info[ka] = None                      # named below, once the parts are counted
            else:
                ka = add_am(module, platform, None, 1, variant="Block A", block="A")
            for sid, key, pts, kind in mine:
                later_items.append((key, sid, ka, kind, pts))
        if not lst:
            if (module, platform) in a_plain:
                parts_total[(module, platform)] = 1
            continue
        parts, cur, run = [], [], 0
        for item in lst:
            if cur and run + item[2] > cap:
                parts.append(cur)
                cur, run = [], 0
            cur.append(item)
            run += item[2]
        if cur:
            parts.append(cur)
        first = 2 if (module, platform) in a_plain else 1
        total = len(parts) + first - 1
        parts_total[(module, platform)] = total
        for i, part in enumerate(parts, first):
            k = add_am(module, platform, i, total)
            for sid, key, pts, kind in part:
                later_items.append((key, sid, k, kind, pts))
    for (module, platform) in sorted(a_plain, key=lambda x: sp.am_order(*x)):
        ka = sp.am_key(module, platform, 1)
        if am_info.get(ka, 1) is None:
            del am_info[ka]
            add_am(module, platform, 1, parts_total.get((module, platform), 1), block="A")

    # the operations no earlier task builds, each with the first later app-module whose screens call it
    callers = defaultdict(set)
    for key, sid, k, kind, _ in later_items:
        for o in screen_ops(sid):
            if o not in planned_ops:
                callers[o].add(k)
    home = {}
    for k, a in sorted(am_info.items(), key=lambda x: x[1]["order"]):
        if a.get("completion") or a.get("decided"):
            continue                     # an operation no screen calls is no completion work (CHG-RONEP-007), and a
            #                              decided app-module holds what it was decided with only (CHG-R4-003)
        if a["platform"] == "P08":
            home.setdefault((a["module"], "P08"), k)
        home.setdefault((a["module"], "*"), k)
    am_ops = defaultdict(list)
    # **A provisional operation is not put on a build ticket** (audit R061; CHG-GTR-007, 3 October). The later blocks
    # planned every operation no earlier task builds, provisional or not, so the r1 refresh put
    # listBiometricConsentGuardian (x-ticvai-provisional) on SVC-ACCESS-DRAFTED-2 and check-ticket-text failed
    # (T-PROVISIONAL). The Venue Management slice already took agreed operations only (agreed() above). Such an
    # operation is planned by the first refresh after it is agreed (the flag removed).
    held = sorted(o for o in ops if o not in planned_ops and ops[o]["provisional"])
    print(f"provisional operations held out of the later blocks until agreed: {len(held)}"
          + (f" ({', '.join(held[:6])}{' ...' if len(held) > 6 else ''})" if held else ""))
    for o in sorted(ops):
        if o in planned_ops or ops[o]["provisional"]:
            continue
        if o in decided_op:                  # a decided app-module's operation is built there (CHG-R4-003)
            am_ops[decided_op[o]].append(o)
            continue
        # **An operation Block A needs is planned with a Block A app-module** (CHG-RONEP-001), so the four-operation
        # tasks it is cut into hold only Block A work. Until 3 October it went with its first caller in build order
        # and the closure pulled that whole task into Block A, three other operations riding along: when new
        # operations re-cut the chunks, listPaymentMethods and setPaymentRules (r2: SVC-ORDER-PAYMENTS-8 and -9, Block A)
        # fell to Block C with nobody deciding it.
        # a core operation goes with a core Block A app-module, completion work with a completion one (CHG-RONEP-007)
        comp_ = o not in core_ops
        a_callers = [x for x in callers.get(o, ()) if am_info[x]["block"] == "A"
                     and bool(am_info[x].get("completion")) == comp_] if o in need_ops else []
        a_home = [a["key"] for a in am_info.values() if a["block"] == "A" and a["module"] == op_module[o]
                  and a["platform"] != "AI" and not a["key"].startswith("AM-SETUP-")
                  and bool(a.get("completion")) == comp_] if o in need_ops else []
        if a_callers:
            k = min(a_callers, key=lambda x: am_info[x]["order"])
        elif o in need_ops:
            k = (min(a_home, key=lambda x: am_info[x]["order"]) if a_home
                 else comp_am(op_module[o], "API") if comp_
                 else add_am(op_module[o], "API", None, 1, variant="Block A", block="A"))
        elif callers.get(o):
            k = min(callers[o], key=lambda x: am_info[x]["order"])
        else:
            m_ = op_module[o]
            k = home.get((m_, "P08")) or home.get((m_, "*")) or add_am(m_, "API", None, 1)
        am_ops[k].append(o)

    # migrations, then back end, app-module by app-module in build order (the first that needs a table creates it)
    def fresh_mig_key(schema):
        n = 2
        while True:
            k = f"MIG-{schema.upper()}-{n}"
            if k not in by_key and k not in kmap_early:
                return k
            n += 1

    for k in sorted(am_ops, key=lambda x: am_info[x]["order"]):
        olist = am_ops[k]
        need = {t for o in olist for kk in ("reads", "writes") for t in (lineage.get(o) or {}).get(kk) or []
                if t in ddl and t not in mig_of}
        frontier = list(need)
        while frontier:
            t = frontier.pop()
            for x in sorted(ddl[t]["fks"]):
                if x in ddl and x not in mig_of and x not in need:
                    need.add(x)
                    frontier.append(x)
        for sch in sorted({t.split(".")[0] for t in need}):
            ts = sorted(t for t in need if t.split(".")[0] == sch)
            mk = fresh_mig_key(sch)
            n_cols = sum(len(ddl[t]["columns"]) for t in ts)
            pts = points_of(1 + 0.5 * len(ts) + n_cols / 40 + 0.3 * sum(1 for t in ts if ddl[t]["rls"])
                            + 0.5 * sum(ddl[t]["partitioned"] for t in ts))
            # A forward migration waits for the baseline, the first-release migration of its schema (if any) and the
            # migrations that create what its keys point into; two forward migrations of one schema with no key
            # between them do not wait on each other (their file numbers are given when they merge).
            prior = sorted({m for t, m in mig_of.items() if t.split(".")[0] == sch and m not in later_mig.values()})
            fk_into = sorted({mig_of[x] for t in ts for x in ddl[t]["fks"] if x in mig_of and x.split(".")[0] != sch})
            task(mk, k, "Task", f"Forward migration: {sch} for {am_info[k]['name']} ({len(ts)} tables)",
                 "Tables: " + ", ".join(ts) + f". Source DDL: {src_files(ddl, ts)} and the matching rows of "
                 "900-foreign-keys, 910-indexes and 920-row-level-security. A forward migration after the r1 baseline "
                 "(frozen, check-migration-freeze); applied forward by SqlMigrationRunner, and a second run applies "
                 "nothing.", 3, service=schema_owner.get(sch, ""), pts=pts, area="backend",
                 depends=["MIG-BASELINE"] + prior + fk_into)
            for t in ts:
                mig_of[t] = mk
                later_mig[t] = mk
        groups_ = defaultdict(list)
        for o in olist:
            groups_[((lineage.get(o) or {}).get("service") or "PlatformService", ops[o]["tag"])].append(o)
        for (n, g), gl in sorted(groups_.items()):
            gl = sorted(gl)
            fam = f"{re.sub(r'Service$', '', n).upper()}-{slug(g).upper()}"
            for i in range(0, len(gl), 4):
                part = gl[i:i + 4]
                num = 1
                while num in fam_used[fam]:
                    num += 1
                fam_used[fam].add(num)
                tk = f"SVC-{fam}-{num}"
                deps = {mig_of.get(t) for o in part for kk in ("reads", "writes")
                        for t in (lineage.get(o) or {}).get(kk) or []} - {None}
                task(tk, k, "Task", f"{n}: " + ", ".join(part),
                     "Operations: " + ", ".join(part) + f". Spec: contracts ({', '.join(sorted({ops[o]['contract'] for o in part}))}) "
                     f"at the release tag, served by ADAM. Built for {am_info[k]['name']}; additive to {n}, whose "
                     f"first-release owner ({svc_owner.get(n) or 'its owner'}) reviews.", 3, service=n,
                     pts=points_of(sum(op_raw(o) for o in part if o in lineage)), area="backend",
                     depends=deps or {"MIG-BASELINE"})
                for o in part:
                    later_op_task[o] = tk
    # the screens, each waiting on the tasks that build its operations (soft: built against the mock server)
    for key, sid, k, kind, pts in later_items:
        if kind == "ticketed":
            am_of[key] = k
            continue
        s_ = screens[sid]
        deps = {op_task.get(o) or vm_op_task.get(o) or later_op_task.get(o) for o in screen_ops(sid)} - {None}
        area = "SETUP" if kind == "rest" else {"P08": "VM", "P01": "WEB", "P02": "MOB", "P04": "POS",
                                                "P15": "POS"}.get(plat_of(sid), plat_of(sid))
        what = (f"The rest of {sid}: Block A built only its setup operations ({', '.join(sorted(setup_screens.get(sid, ())))}); "
                f"this task adds the others. " if kind == "rest" else "")
        task(key, k, "Task", f"{sid} {s_['name']}" + (f" ({rest_scope(s_, setup_screens.get(sid, ()))})"
                                                       if kind == "rest" else ""),
             what + f"{s_.get('purpose') or ''} Module: {s_.get('module')}. App: {sp.PLATFORM_NAME.get(plat_of(sid))}.",
             s_.get("wave") or "", platform=s_["_platform"].get("shortName", ""), depends=deps | {"SETUP-CLIENTS"},
             pts=pts, area=area)
        am_of[key] = k
    # **A decided app-module's wiring tasks** (CHG-R4-003, 5 October): one front-end task per `wiring` entry, wiring its
    # operations into screens other tickets build (the operations strip_wiring took off them). It builds the operations
    # it wires, so ADAM links their contract, and names the screens and their tickets in its scope; it waits on the
    # back-end tasks that build those operations. Sized like a screen's share: one point of setup, 0.4 an operation a
    # screen binds, a sixth of a point a component.
    for am in decided_ams:
        for w in am.get("wiring") or []:
            sids = [x for x in w.get("screens") or [] if x in wired_off]
            if not sids:
                raise SystemExit(f"block-a-extra-tasks.json appModules {am['key']}: wiring {w['key']} wires no screen")
            w_ops = sorted({o for x in sids for o in wired_off[x]["ops"]})
            raw_ = 1 + sum(0.4 * len(wired_off[x]["ops"]) + wired_off[x]["components"] / 6 for x in sids)
            pf = w.get("platform") or plat_of(sids[0])
            deps = {op_task.get(o) or vm_op_task.get(o) or later_op_task.get(o) for o in w_ops} - {None}
            owners_ = sorted({k_ for x in sids for k_, t_ in by_key.items() if t_["type"] == "Task"
                              and not k_.startswith("TEST-") and (key_identity(k_) or (None, None)) == ("screen", x)})
            task(w["key"], am["key"], "Task", w["subject"],
                 "Builds: " + ", ".join(f"`operation {ops[o]['contract']}#{o}`" for o in w_ops) + ". "
                 + w["detail"].rstrip(".") + ". Scope: " + ", ".join(w_ops) + " on " + ", ".join(sids)
                 + "; the rest of each screen is its own ticket (" + ", ".join(owners_) + "). "
                 f"Decided by {am['decided'].split(' (')[0]} ({am['key']}, CHG-R4-003). "
                 f"Done when {', '.join(sids)} call{'s' if len(sids) == 1 else ''} {', '.join(w_ops)} as "
                 f"{'its spec says' if len(sids) == 1 else 'their specs say'} (every state the wired components list, "
                 "the cached answer offline where the spec says so, every refusal the contract documents), the rest "
                 f"of {'the screen' if len(sids) == 1 else 'each screen'} still passes its own ticket's done-when, and "
                 "a peer in the same stack has reviewed it.",
                 1, platform=sp.PLATFORM_NAME.get(pf, pf), depends=deps | {"SETUP-CLIENTS"}, pts=points_of(raw_),
                 area={"P08": "VM", "P01": "WEB", "P02": "MOB", "P04": "POS", "P15": "POS"}.get(pf, pf))
            by_key[w["key"]]["pool"] = sp.POOL_OF_PLATFORM.get(pf, "web")
            am_of[w["key"]] = am["key"]
    # **A screen whose spec says a person must define it is built only after its definition** (4 October, the Sprint
    # 1-2 judging; CHG-FXP-004). ADM-506's table had no operation and its columns were sample values ("92% / High"):
    # the screen's gaps say "it needs a person before it is built", and the plan gave it a build task in Sprint 2 anyway.
    # Its build task now waits for the definition: it starts no earlier than DEFINE_DAY, and its text says why. The
    # screens a person cannot define in time leave Block A by name (block-a-extra-tasks.json `screensNotBuilt`).
    define_wait = set()
    for t_ in tasks:
        if t_["type"] != "Task" or t_["key"].startswith("TEST-"):
            continue
        sids_ = [b_.split(" ", 1)[1] for b_ in ticket_done.builds_of(t_, "", lineage) if b_.startswith("screen ")]
        if any(x in screens and ticket_done.define_needed(screens[x]) for x in sids_):
            t_["notBefore"] = max(float(t_.get("notBefore") or 0), DEFINE_DAY)
            define_wait.add(t_["key"])
    print(f"screen tasks waiting for their screen's definition (day {DEFINE_DAY:g}): {len(define_wait)}")
    # **The AI engine beyond Block A** (docs/active/ai-functions-review-30-september.json): each capability is an
    # app-module of its own; its extra back-end weeks (the review's `backendWeeksExtra`) are cut into tasks of at most 8
    # points, and the review's sprint for a capability (its own three-week sprints) is the earliest they start. A
    # capability the review puts in Block A (the planner agent, translations) is Block A's AI-ENGINE tasks already.
    # **Phase 1 by 2 April, phase 2 after** (Chinmay, 4 October, CHG-AIPH-001; docs/active/ai-phase-plan.json): the
    # AI-engineer weeks are no longer cut into "n of N" chunks of ten days with one description. Each is one task per
    # completable unit, with its build items, AI-days, dependencies and done-when. Phase 1 (what works on day one:
    # rules, priors, the LLM over the venue's own data) goes to the AI engineer the file names, in benefit order; its
    # module test also waits on the owner-side operations and the screens it needs (`needs`, resolved below), so the
    # unit is complete when the test passes. Phase 2 (what learns from tenant data) starts after 2 April, has no owner
    # and is not ticketed. A capability the phase plan does not list keeps the old chunks (none at present).
    later_ai = []
    ai_phase = {"modules": []}
    ai_unit = {}                  # task key -> its unit in ai-phase-plan.json
    ai_phase2 = set()             # phase 2 keys: app-modules and tasks, never ticketed for r1
    ai_needs = {}                 # app-module -> the operations, screens and tasks its module test also waits on
    ai_cut_day = sp.index_of(sp.PLAN_END) + 1
    phase_file = ROOT / "docs" / "active" / "ai-phase-plan.json"
    if phase_file.exists():
        ai_phase = json.loads(phase_file.read_text(encoding="utf-8"))
    phase_mods = defaultdict(list)
    for m_ in ai_phase.get("modules") or []:
        phase_mods[m_["capability"]].append(m_)

    def ai_unit_text(m_, u_):
        items = "; ".join(f"({i + 1}) {x['text']}" for i, x in enumerate(u_["items"]))
        weeks = sum(float(x.get("aiWeeks") or 0) for x in u_["items"])
        need = u_.get("needs") or {}
        need_txt = "; ".join(x for x in (
            ("operations " + ", ".join(need.get("operations") or [])) if need.get("operations") else "",
            ("screens " + ", ".join(need.get("screens") or [])) if need.get("screens") else "",
            ("tasks " + ", ".join(need.get("tasks") or [])) if need.get("tasks") else "") if x)
        if m_["phase"] == 1:
            lead = (f"Phase 1 of the AI engine (by 2 April 2027; Chinmay, 4 October, CHG-AIPH-001), benefit rank "
                    f"{u_['rank']}" + (" (Block B, already assigned)" if not u_["rank"] else "") + ". ")
        else:
            lead = ("Phase 2 of the AI engine (after 2 April 2027; Chinmay, 4 October, CHG-AIPH-001): it learns from "
                    "tenant data, which no tenant has before go-live; not ticketed for r1. ")
        return (lead + f"{u_['subject']}. Build items: {items}. AI-days: {float(u_['days']):g} ({weeks:g} AI-weeks x 5). "
                + f"Waits on: {', '.join(u_.get('dependsOn') or ['AI-ENGINE-GATEWAY'])}. "
                + (f"Back end and owner side: {u_['backEndNote']}. " if u_.get("backEndNote") else "")
                + (f"Its module test also waits on what it cannot be accepted without: {need_txt}. " if need_txt else "")
                + f"Why: {u_['why']} "
                + f"Done when {u_['doneWhen']}; it answers through the AI gateway with the scrubber and the guard on, its "
                "evaluation set passes the gate of docs/architecture/ai-system-design.md 3.5, it degrades as 3.7 says "
                "when its provider is down, and a peer AI engineer has reviewed it.")

    rev = ROOT / "docs" / "active" / "ai-functions-review-30-september.json"
    if rev.exists():
        for c in json.loads(rev.read_text(encoding="utf-8")).get("capabilities") or []:
            b_ = c.get("build") or {}
            if "(Block A)" in str(c.get("sprint") or ""):
                continue
            cid = re.sub(r"[^A-Z0-9]+", "-", str(c.get("id") or c["name"]).upper()).strip("-")
            m_ = re.search(r"S(\d)", str(c.get("sprint") or ""))
            nb = sp.index_of(sp.START + dt.timedelta(days=21 * (int(m_.group(1)) - 1))) if m_ else 0
            short = re.split(r" \(|,", c["name"])[0].strip()[:48]
            mods = phase_mods.get(str(c.get("id") or ""))
            if mods:
                for pm in mods:
                    p2 = pm["phase"] == 2
                    rank0 = min(u_["rank"] for u_ in pm["units"])
                    k = add_am("AI & Intelligence", "AI", None, 1, variant=cid, key=pm["key"],
                               name=pm.get("name") or f"AI engine · {short}" + (" (phase 2, after 2 April)" if p2 else ""),
                               order=(4, sp.MODULES.index("AI & Intelligence"), 98, 0,
                                      pm.get("order", (100 if p2 else 0) + rank0)))
                    if p2:
                        ai_phase2.add(k)
                    ai_needs[k] = {"operations": [], "screens": [], "tasks": []}
                    for u_ in pm["units"]:
                        tk = u_["key"]
                        task(tk, k, "Task", f"AI engine: {u_['subject']}" + (" (phase 2, after 2 April)" if p2 else ""),
                             ai_unit_text(pm, u_), 3, area="ai", assignee="" if p2 else u_.get("assignee") or "",
                             depends=u_.get("dependsOn") or ["AI-ENGINE-GATEWAY"])
                        by_key[tk]["days"] = float(u_["days"])
                        if p2:
                            by_key[tk]["notBefore"] = ai_cut_day
                            ai_phase2.add(tk)
                        ai_unit[tk] = dict(u_, phase=pm["phase"], module=k)
                        later_ai.append(tk)
                        am_of[tk] = k
                        for kind_ in ("operations", "screens", "tasks"):
                            ai_needs[k][kind_] += [x for x in (u_.get("needs") or {}).get(kind_) or []
                                                   if x not in ai_needs[k][kind_]]
                # the review's back-end weeks go with the capability's phase 1 app-module, unless the phase plan says
                # they are built elsewhere already (`reviewBackEnd: false`, its doubleCount)
                be_mod = next((pm for pm in mods if pm["phase"] == 1 and pm.get("reviewBackEnd", True)), None) \
                    or next((pm for pm in mods if pm.get("reviewBackEnd", True)), None)
                if not be_mod:
                    continue
                k = be_mod["key"]
                be_note = f" {be_mod['backEndNote']}." if be_mod.get("backEndNote") else ""
            else:
                be_note = ""
                k = add_am("AI & Intelligence", "AI", None, 1, variant=cid, key=f"AM-AI-ENGINE-{cid}",
                           name=f"AI engine · {short}", order=(4, sp.MODULES.index("AI & Intelligence"), 98, 0, nb))
                days = float(b_.get("aiEngineerWeeksTotal") or 0) * 5
                n_ = 0
                while days > 1e-6:
                    d_ = min(10.0, days)
                    n_ += 1
                    tk = f"AI-ENGINE-{cid}-{n_}"
                    task(tk, k, "Task", f"AI engine: {short} ({n_} of {math.ceil(float(b_.get('aiEngineerWeeksTotal') or 0) * 5 / 10)})",
                         f"{c['name']}. " + " ".join(f"- {x}" for x in (b_.get("items") or [])[:6]) +
                         " Sized by the AI review in engineer-weeks; built by the two AI engineers, baseline first, learning "
                         "per tenant (ADR-0051, ADR-0059).", 3, area="ai", depends=["AI-ENGINE-GATEWAY"])
                    by_key[tk]["days"] = d_
                    later_ai.append(tk)
                    am_of[tk] = k
                    days -= d_
            pts_be = float(b_.get("backendWeeksExtra") or 0) * 48
            n_ = 0
            while pts_be > 1e-6:
                p_ = int(min(8, round(pts_be)))
                n_ += 1
                tk = f"AI-BE-{cid}-{n_}"
                task(tk, k, "Task", f"AI back end: {short} (part {n_})",
                     f"The back-end work the AI review names for {c['name']} beyond the AI engineers' own "
                     "(validate-only tool operations, semantic-spec compile, historical import). Additive to AiService "
                     "and the owning services; their owners review." + be_note, 3, service="AiService", pts=p_, area="backend",
                     depends=["PLATFORM-KERNEL"])
                by_key[tk]["notBefore"] = nb
                am_of[tk] = k
                pts_be -= p_
    # **The later-block tasks block-a-extra-tasks.json records** (EDGE-WAITING-ROOM and its load test, the admission
    # rule evaluator: ADRs of 1 October, plan item L9) are planned now, under the app-module they name.
    if EXTRA.exists():
        for t_ in json.loads(EXTRA.read_text(encoding="utf-8")).get("tasks") or []:
            if str(t_.get("block") or "A") == "A" or t_["key"] in by_key:
                continue
            m_ = t_.get("module") or sp.FOUNDATION
            pf = t_.get("platform") or "API"
            # a task a decided app-module lists goes there, in its block (CHG-R4-003: DEVICE-BOCA-FGL in Block A2)
            dec_ = next((a["key"] for a in decided_ams if t_["key"] in (a.get("tasks") or [])), None)
            k = dec_ or add_am(m_, pf, None, 1, variant="" if pf != "API" else "platform",
                               name=None if pf != "API" else f"{sp.MODULE_SHORT.get(m_, m_)} · platform (later blocks)")
            task(t_["key"], k, "Task", t_["subject"], t_["subject"] + ". " + extra_lead(t_) + t_["detail"], 3,
                 pts=int(t_["points"]), area="backend", assignee=t_.get("assignee") or "", depends=t_.get("depends") or ())
            am_of[t_["key"]] = k
    later_keys = set(am_of) | set(later_op_task.values()) | set(later_mig.values())
    for t_ in tasks:
        if t_["key"] in later_keys:
            t_["phase"] = 2
    for o, k in later_op_task.items():
        am_of.setdefault(k, by_key[k]["parent"])
    for t, k in later_mig.items():
        am_of.setdefault(k, by_key[k]["parent"])

    # **Services stand on the platform** (30 September). A service task used to wait only for its
    # migration, so the build order put 60-odd service tasks in front of the kernel they run on (tenant
    # routing, scope, auth) and every sale-path write in front of idempotency and the outbox. Now:
    # every backend service task waits for PLATFORM-KERNEL; one whose operations write a table also
    # waits for PLATFORM-IDEMPOTENCY; one that publishes an event (writes platform.outbox) also waits
    # for PLATFORM-OUTBOX. The platform tasks themselves are exempt, so nothing waits on itself.
    ops_of = defaultdict(set)
    for o, k in list(op_task.items()) + list(vm_op_task.items()) + list(later_op_task.items()):
        ops_of[k].add(o)
    platform_keys = {"PLATFORM-KERNEL", "PLATFORM-IDEMPOTENCY", "PLATFORM-OUTBOX"}
    if platform_keys <= set(by_key):
        for k, found in ops_of.items():
            t_ = by_key.get(k)
            if not t_ or t_["type"] != "Task" or t_["track"] != "Backend":
                continue
            need = {"PLATFORM-KERNEL"}
            writes = {w for o in found for w in (lineage.get(o) or {}).get("writes") or []
                      if not w.startswith(("cache:", "qdrant"))}
            if writes:
                need.add("PLATFORM-IDEMPOTENCY")
            if "platform.outbox" in writes:
                need.add("PLATFORM-OUTBOX")
            t_["dependsOn"] = " ".join(sorted(set(t_["dependsOn"].split()) | need))

    # **A report waits for the data it reports on** (30 September, Chinmay). A backend task whose
    # operations only read (reports, dashboards, analytics, exports) and read tables another task
    # writes now waits for those writer tasks: a sales report built before orders exist has nothing
    # to show and nothing to test against. Readers write nothing, so this can never close a loop.
    writers_of = defaultdict(set)
    for k, found in ops_of.items():
        if k in by_key and by_key[k]["track"] != "Backend":
            continue                     # an AI engine task serving operations (CHG-RONEP-001) holds no report back
        for o in found:
            for w in (lineage.get(o) or {}).get("writes") or []:
                if not w.startswith(("cache:", "qdrant")):
                    writers_of[w].add(k)
    for k, found in ops_of.items():
        t_ = by_key.get(k)
        if not t_ or t_["type"] != "Task" or t_["track"] != "Backend":
            continue
        writes = {w for o in found for w in (lineage.get(o) or {}).get("writes") or []
                  if not w.startswith(("cache:", "qdrant"))}
        if writes:
            continue
        reads = {r for o in found for r in (lineage.get(o) or {}).get("reads") or []
                 if not r.startswith(("cache:", "qdrant"))}
        feeds = {w for r in reads for w in writers_of.get(r, ())} - {k}
        # Same phase only: a first-release report never waits on Venue Management work.
        feeds = {w for w in feeds if by_key[w]["phase"] <= t_["phase"]}
        if feeds:
            t_["dependsOn"] = " ".join(sorted(set(t_["dependsOn"].split()) | feeds))

    # **Generating a report waits for the services it reports on** (30 September, Chinmay). The report
    # operations read only report definitions; the figures come from the other services' data through the
    # semantic layer at run time, so the lineage above cannot connect them. The rule is explicit instead:
    # a Reporting task that produces figures waits for every task that writes the business data -- orders,
    # money, catalogue, admissions, food and drink, stock, retail, wallets -- in its phase or earlier.
    REPORT_RUNS = {"runReport", "getDashboard", "askReportingQuestion", "getKpiValues", "createReportSchedule",
                   "listAlerts"}
    REPORT_SOURCES = {"OrderService", "LedgerService", "CatalogueService", "AccessService", "FnbService",
                      "InventoryService", "RetailService", "WalletService"}
    source_writers = [k for k, found in ops_of.items()
                      if by_key.get(k) and by_key[k]["type"] == "Task" and by_key[k]["service"] in REPORT_SOURCES
                      and any(w for o in found for w in (lineage.get(o) or {}).get("writes") or []
                              if not w.startswith(("cache:", "qdrant")))]
    for k, found in ops_of.items():
        t_ = by_key.get(k)
        if not t_ or t_["type"] != "Task" or t_["service"] != "ReportingService" or not (found & REPORT_RUNS):
            continue
        feeds = {w for w in source_writers if by_key[w]["phase"] <= t_["phase"]}
        t_["dependsOn"] = " ".join(sorted(set(t_["dependsOn"].split()) | feeds))

    # **Acceptance that waits on the client** (audit R065): the payment sandbox. It is the client's to
    # deliver, so it is a question in the Decisions Register rather than a ticket, and the tickets whose
    # testing needs its credentials say so. Wired here, after every ticket exists, so the note survives
    # however those keys are generated.
    for k in ("APP-WEB-WEB-012", "SVC-ORDER-PAYMENT-1"):
        if k in by_key:
            by_key[k]["description"] = (by_key[k]["description"].rstrip() + " Acceptance of the declined, "
                                        "unknown and reconcile paths waits on the client's payment sandbox "
                                        "credentials: see the client's answer in the Decisions Register.")

    # **Chronology.** Every task gets its place in the order work can happen: block, then app-module (a module on
    # one app, in build-phase order), then build phase, wave, how many tasks stand in front of it, and database
    # before backend before frontend. `queue` is the same order within one person's list, so each developer's
    # board reads top to bottom as the order to work in.
    TRACK_ORDER = {"Setup": 0, "DevOps": 1, "Onboarding": 1, "Database": 2, "Backend": 3,
                   "AI": 3, "Full stack": 4, "Frontend": 5}

    # **Services are built in phases** (30 September, Chinmay): plumbing, then the services everything
    # reads, then the sale path, then the per-module operations, then engagement, then reporting. The
    # package's own reasoning: nothing runs without a scope (Tenancy, Identity); order, payment, entitlement
    # and ledger commit in one transaction (ADR-0055); nothing that takes money depends on marketing or AI.
    # WhiteLabel and Platform sit in phase 1 because Block A's white-label screens and tenant provisioning
    # need them. A screen task takes the phase of the service it calls most, so a module is built when its
    # main service is, and the extras it also touches (an AI suggestion, a report tile) connect as their
    # service lands. The phase is a sort key inside a topological order: a task never comes before
    # anything it waits on, whatever its phase.
    SERVICE_PHASE = {"TenancyService": 1, "IdentityService": 1, "PlatformService": 1, "WhiteLabelService": 1,
                     "CatalogueService": 2, "OrderService": 2, "LedgerService": 2, "AccessService": 2,
                     "WalletService": 2, "VenueOpsService": 3, "FnbService": 3, "InventoryService": 3,
                     "RetailService": 3, "MarketingService": 4, "AiService": 4, "ReportingService": 5,
                     "CrossRegionService": 5}

    def tier(t_):
        if t_["type"] != "Task" or t_["track"] in ("Setup", "DevOps", "Onboarding", "Database", "AI"):
            return 0
        if t_["key"].startswith(("PLATFORM-", "KERNEL-", "ARCH-", "DB-", "OFFLINE-", "SETUP-", "MIG-", "POS-KDS")):
            return 0
        if t_["track"] == "Backend":
            return SERVICE_PHASE.get(t_["service"], 3)
        calls = Counter(by_key[d]["service"] for d in t_["dependsOn"].split()
                        if d in by_key and by_key[d]["service"])
        return SERVICE_PHASE.get(calls.most_common(1)[0][0], 3) if calls else 0

    # ================================================================ the sprint plan (1 October)
    # **Every task belongs to an app-module, every app-module to a block.** Block A's screens go to the app-module
    # of their module on their app; its setup screens to "<module> · Venue Management (setup)"; the platform, setup,
    # database, offline and AI engine work to the Foundation and AI engine app-modules. A back-end task goes with the
    # first app-module whose tasks wait on it, and a migration with the first whose back end needs its tables.
    for i, (code, title) in enumerate((("SETUP", "Setup and environments"), ("DATABASE", "Database migrations"),
                                       ("PLATFORM", "Platform kernel"),
                                       ("OFFLINE", "Offline: POS, Kitchen Display and scanner"))):
        add_am(sp.FOUNDATION, "", None, 1, key=f"AM-FOUNDATION-{code}", name=f"Foundation · {title}", block="A",
               order=(0, i, 0, 0, 0))
    # **The Block A AI chain split across both AI engineers** (Chinmay, 1 October): two app-modules, one per engineer,
    # whose halves run side by side (block-a-extra-tasks.json `appModule`); each is module-tested by the other.
    add_am("AI & Intelligence", "AI", None, 1, key="AM-AI-ENGINE-A", block="A", order=(0, 9, 0, 0, 0),
           name="AI engine · Block A: gateway and guest AI (concierge, Help me choose, translations, planner)")
    add_am("AI & Intelligence", "AI", None, 1, key="AM-AI-ENGINE-A-BASELINE", block="A", order=(0, 10, 0, 0, 0),
           name="AI engine · Block A: baseline layer, day-one suggestions, Qdrant tenancy, evaluation")
    ai_part, ai_drop = {}, {}
    if EXTRA.exists():
        ai_part = {e["key"]: e.get("appModule") for e in json.loads(EXTRA.read_text(encoding="utf-8")).get("tasks") or []}
        # **AI engine work moved to A2** (Chinmay, 3 October, CHG-RONEP-010): a Block A AI engine task marked `drop: A2`
        # is built in "AI engine · Block A2", so the two AI engineers end their A1 work before 24 November
        ai_drop = {e["key"]: e.get("drop") for e in json.loads(EXTRA.read_text(encoding="utf-8")).get("tasks") or []}
    if "A2" in ai_drop.values():
        add_am("AI & Intelligence", "AI", None, 1, key="AM-AI-ENGINE-A2", block="A2", order=(0, 11, 0, 0, 0),
               name="AI engine · Block A2: the AI work moved out of A1 (" + ", ".join(
                   sorted(k.replace("AI-ENGINE-", "").lower() for k, v in ai_drop.items() if v == "A2")) + ")")

    def foundation_am(k):
        if k.startswith("SETUP-"):
            return "AM-FOUNDATION-SETUP"
        if k in ("MIG-BASELINE", "MIG-FOREIGN-KEYS", "MIG-PARTITIONS") or k.startswith("DB-"):
            return "AM-FOUNDATION-DATABASE"
        if k.startswith(("OFFLINE-", "POS-KDS")):
            return "AM-FOUNDATION-OFFLINE"
        if k.startswith("AI-ENGINE-"):
            if ai_drop.get(k) == "A2":
                return "AM-AI-ENGINE-A2"
            return "AM-AI-ENGINE-A-BASELINE" if ai_part.get(k) == "baseline" else "AM-AI-ENGINE-A"
        if k.startswith(("PLATFORM-", "KERNEL-", "ARCH-", "OBS-", "EDGE-")):
            return "AM-FOUNDATION-PLATFORM"
        return None

    leaf = [t_ for t_ in tasks if t_["type"] == "Task"]
    dependents = defaultdict(set)
    for t_ in leaf:
        for d in t_["dependsOn"].split():
            dependents[d].add(t_["key"])
    for t_ in leaf:
        k = t_["key"]
        if k in am_of or t_["phase"] != 1:
            continue
        f_ = foundation_am(k)
        if f_:
            am_of[k] = f_
        elif t_["track"] == "Frontend":
            sid = key_identity(k)[1]
            mod, pf = screen_module(sid), plat_of(sid)
            if k.startswith("APP-SETUP-"):
                am_of[k] = setup_am(sid)
            else:
                am_of[k] = add_am(mod, pf, 1, parts_total.get((mod, pf), 1), block="A")
    a_keys = {t_["key"] for t_ in leaf if t_["phase"] == 1}
    later_set = {t_["key"] for t_ in leaf} - a_keys
    for _ in range(12):
        moved = False
        for t_ in leaf:
            k = t_["key"]
            if k in am_of:
                continue
            same = a_keys if k in a_keys else later_set
            # seed data and sign-in wait on every migration; they are not the app-module a table is built for
            cand = {am_of[d] for d in dependents[k] if d in am_of and d in same and am_of[d] != "AM-FOUNDATION-SETUP"}
            if cand:
                am_of[k] = min(cand, key=lambda x: am_info[x]["order"])
                moved = True
        if not moved:
            break
    for t_ in leaf:                                        # nothing waits on it: its module's first app-module
        k = t_["key"]
        if k in am_of:
            continue
        mods = Counter(op_module[o] for o in ops_of.get(k, ()) if o in op_module)
        mod = mods.most_common(1)[0][0] if mods else None
        pool_ams = [a for a in am_info.values() if (a["block"] == "A") == (k in a_keys)]
        home_a = "AM-FOUNDATION-DATABASE" if t_["track"] == "Database" else "AM-FOUNDATION-PLATFORM"
        cand = [a for a in pool_ams if a["module"] == mod] or (
            [a for a in pool_ams if a["key"] == home_a] if k in a_keys else pool_ams)
        am_of[k] = min(cand, key=lambda a: a["order"])["key"]
    # **Block A's closure, back end** (1 October): a task that builds an operation Block A's apps or flows need goes
    # into Block A -- with the Block A app-module that waits on it, else one of its module, else "<module> · API
    # only (Block A)"; the migrations and same-service work it needs follow it (pull, below).
    for t_ in leaf:
        k = t_["key"]
        comp_ = not (ops_of.get(k, set()) & core_ops)          # completion work only (CHG-RONEP-007)
        if k in a_keys or not (ops_of.get(k, set()) & need_ops) or (
                am_info[am_of[k]]["block"] == "A" and (comp_ or not am_info[am_of[k]].get("completion"))):
            continue
        users = [am_info[am_of[d]] for d in dependents[k] if d in am_of and am_info[am_of[d]]["block"] == "A"
                 and bool(am_info[am_of[d]].get("completion")) == comp_]
        mods = Counter(op_module[o] for o in ops_of.get(k, ()) if o in op_module)
        mod = mods.most_common(1)[0][0] if mods else sp.FOUNDATION
        cand = users or [a for a in am_info.values() if a["block"] == "A" and a["module"] == mod
                         and bool(a.get("completion")) == comp_]
        am_of[k] = (min(cand, key=lambda a: a["order"])["key"] if cand
                    else comp_am(mod, "API") if comp_ else add_am(mod, "API", None, 1, variant="Block A", block="A"))
    for t_ in leaf:
        t_["tier"] = tier(t_)
    step.clear()
    for t_ in leaf:
        step_of(t_["key"])

    people, pool_caps, _ = sp.load_team(team)
    days_ex = {}
    if EXTRA.exists():
        days_ex = {e["key"]: float(e["days"]) for e in json.loads(EXTRA.read_text(encoding="utf-8")).get("tasks") or []
                   if e.get("days")}

    def pool_of(t_):
        if t_["track"] == "AI":
            return "ai"
        if t_["track"] == "Frontend":
            ident = key_identity(t_["key"]) or (None, None)
            sid = ident[1] if ident[0] == "screen" else re.sub(r"-REST$", "", t_["key"]).split("-", 2)[-1]
            return sp.POOL_OF_PLATFORM.get(plat_of(sid), "web") if sid in screens else "web"
        if t_["track"] == "Onboarding":
            return "web"
        return "be"

    def topo(prio_of):
        keys = {t_["key"] for t_ in leaf}
        waits = {t_["key"]: {d for d in t_["dependsOn"].split() if d in keys and d != t_["key"]} for t_ in leaf}
        freed = defaultdict(set)
        for k, ds in waits.items():
            for d in ds:
                freed[d].add(k)
        left = {k: len(ds) for k, ds in waits.items()}
        pr = {t_["key"]: prio_of(t_) for t_ in leaf}
        ready = [pr[k] for k, n in left.items() if n == 0]
        heapq.heapify(ready)
        out, done = [], set()
        while ready:
            k = heapq.heappop(ready)[-1]
            done.add(k)
            out.append(by_key[k])
            for n in freed[k]:
                left[n] -= 1
                if left[n] == 0:
                    heapq.heappush(ready, pr[n])
        # A loop in the waits would strand its tasks; they follow in priority order rather than vanish.
        return out + sorted((t_ for t_ in leaf if t_["key"] not in done), key=lambda t_: pr[t_["key"]])

    def block_of_task(k):
        a_ = am_info.get(am_of.get(k)) if am_of.get(k) else None
        return a_["block"] if a_ else by_key[k].get("block") or "A"

    def items_of(order):
        return [{"key": t_["key"], "who": t_["assignee"] or None, "pool": t_.get("pool") or pool_of(t_),
                 "track": t_["track"], "service": t_["service"], "points": int(t_["points"] or 0),
                 "days": t_.get("days") or days_ex.get(t_["key"]), "notBefore": t_.get("notBefore") or 0,
                 "deps": t_["dependsOn"].split(), "client": t_["area"] == "client",
                 "block": block_of_task(t_["key"]), "peerOf": t_.get("peerOf"),
                 "paceExclude": bool(am_of.get(t_["key"]) and (am_info.get(am_of[t_["key"]]) or {}).get("scheduleAfter")),
                 "fallback": {"pos": ("mob", "web"), "mob": ("web",)}.get(t_.get("pool")) if t_.get("peerOf") else None}
                for t_ in order]

    windows = {}

    def run_schedule(order):
        its = items_of(order)
        # the pace (team.json sprintPlan.pace; default Block A's plan of record), from the tasks being scheduled
        pace_at, _, _ = sp.pace_model(team, its)
        return sp.schedule(its, people, caps=pool_caps, svc_owner=svc_owner,
                           backend_owners=areas.get("backend") or [], helper_share=HELPER_SHARE, freeze=windows,
                           open_blocks=settings["fixed"], pace_at=pace_at)

    BRANK = {b: i for i, b in enumerate(sp.BLOCKS)}
    targets = settings["targets"]
    tests = sp.test_settings(team)

    # **Block A ships in two drops: A1 by 27 November, A2 right after** (Chinmay, 3 October, CHG-RONEP-007). The
    # completion app-modules start in A2. Then, app by app in the order below, an app's completion work moves into A1
    # if A1 still ends by its block-test window with no more overtime than the plan already carries or team.json
    # `acceptedOvertimeHours` (43 h, accepted 3 October), whichever is more -- so every app in A1 works end to end.
    # Overtime is the developers' hours of A1 work (and of what it waits on, which pull() brings into A1) still
    # running when Block A's window opens, the measure of build-plan-deck.py.
    comp_ams = {k for k, a in am_info.items() if a and a.get("completion")}
    for k in comp_ams:
        am_info[k]["block"] = "A2"
    leaf_by = {t_["key"]: t_ for t_ in leaf}
    a_cut = sp.window_of(targets["A"], tests["days"])[0]
    accepted = float(next((b_.get("acceptedOvertimeHours") for b_ in (team.get("sprintPlan") or {}).get("blocks") or []
                           if b_.get("block") == "A"), 0) or 0)

    def a1_closure():
        base = {k for k in leaf_by if am_of.get(k) and am_info[am_of[k]]["block"] == "A"}
        stack = list(base)
        while stack:
            for d in leaf_by[stack.pop()]["dependsOn"].split():
                if d in leaf_by and d not in base:
                    base.add(d)
                    stack.append(d)
        return base

    def a1_overtime():
        a1 = a1_closure()
        res = run_schedule(topo(lambda t_: (0 if t_["key"] in a1 else
                                            1 if am_info[am_of[t_["key"]]]["block"] == "A2" else 2,
                                            am_info[am_of[t_["key"]]]["order"], t_["tier"], int(t_["wave"] or 9),
                                            step[t_["key"]], TRACK_ORDER[t_["track"]], t_["key"])))
        h = 0.0
        for k in a1:
            r_ = res.get(k)
            if not r_ or leaf_by[k]["track"] == "AI" or r_["end"] <= a_cut or not r_.get("dur"):
                continue
            h += r_["dur"] * sp.HOURS_PER_DAY * (r_["end"] - max(r_["start"], a_cut)) / max(r_["end"] - r_["start"], 1e-6)
        return h

    APP_PRIORITY = ["P01", "P02", "P04", "P15", "P05", "P06", "P07", "P13", "P12", "P10", "P11", "P17", "P14", "P16",
                    "P09", "P08", "API"]
    groups = defaultdict(list)
    for k in comp_ams:
        groups[am_info[k]["platform"] or "API"].append(k)
    base_ot = a1_overtime() if comp_ams else 0.0
    allow = max(base_ot, accepted) + 1.0
    a1_apps = []
    for pf in sorted(groups, key=lambda x: (APP_PRIORITY.index(x) if x in APP_PRIORITY else 99, x)):
        for k in groups[pf]:
            am_info[k]["block"] = "A"
        ot = a1_overtime()
        if ot <= allow:
            a1_apps.append(pf)
            base_ot = max(base_ot, ot)
        else:
            for k in groups[pf]:
                am_info[k]["block"] = "A2"
    print(f"Block A in two drops: completion work of {', '.join(a1_apps) or 'no app'} in A1 "
          f"({base_ot:.0f} h of developer overtime to end A1 by its window, {accepted:g} h accepted); "
          f"A2 takes {', '.join(sorted(pf for pf in groups if pf not in a1_apps)) or 'nothing'}")

    # **Pass 1: where each later app-module finishes**, with Block A first and the rest in build order. B, C and D
    # are then the app-modules that finish by each block's target sprint (team.json sprintPlan.blocks).
    # a decided app-module scheduled after a block (CHG-R4-003) goes last here, so it moves no other app-module's finish
    first_run = run_schedule(topo(lambda t_: (3 if am_info[am_of[t_["key"]]].get("scheduleAfter")
                                              else BRANK[am_info[am_of[t_["key"]]]["block"]]
                                              if am_info[am_of[t_["key"]]]["block"] in sp.BLOCK_A_FAMILY else 2,
                                              am_info[am_of[t_["key"]]]["order"],
                                              t_["tier"], int(t_["wave"] or 9), step[t_["key"]],
                                              TRACK_ORDER[t_["track"]], t_["key"])))
    am_end = defaultdict(float)
    for k, r_ in first_run.items():
        am_end[am_of[k]] = max(am_end[am_of[k]], r_["end"])
    def earliest_block(k):
        # the first later block (B, C, D) whose test window starts after the app-module is done
        return next((sp.BLOCKS.index(b) for b in sp.LATER_BLOCKS
                     if sp.window_of(targets[b], tests["days"])[0] >= am_end.get(k, 0.0) - 1e-6), len(sp.BLOCKS) - 1)

    # **Blocks are filled to their target sprints in build order** (Chinmay, 1 October: "similar sizes"): B, C and D
    # take consecutive runs of app-modules in the order they are built, each up to where its work no longer finishes
    # by the block's target -- not "everything that happens to finish by then", which made the blocks lopsided. An
    # AI engine capability runs on the AI engineers' own calendar and is placed by where it finishes; it never holds
    # its block open (it is accepted on its own module test).
    # The measure is work, not finish dates: the developer points the first pass completes before each block's test
    # window (whatever block they belong to) is how much that block, with the ones before it, can hold.
    dev_pts = {t_["key"]: float(t_["points"] or 0) for t_ in leaf if t_["track"] != "AI"}
    done_by = {}
    for b_ in sp.LATER_BLOCKS:
        cut = sp.window_of(targets[b_], tests["days"])[0]
        tot = 0.0
        for k, r_ in first_run.items():
            pts = dev_pts.get(k, 0.0)
            if not pts or r_["start"] >= cut:
                continue
            span = max(r_["end"] - r_["start"], 1e-6)
            tot += pts * min(1.0, (cut - r_["start"]) / span)
        done_by[b_] = tot
    am_pts = defaultdict(float)
    for t_ in leaf:
        am_pts[am_of[t_["key"]]] += dev_pts.get(t_["key"], 0.0)
    run = sum(v for k, v in am_pts.items() if am_info[k]["block"] in sp.BLOCK_A_FAMILY)
    # **Comparable sizes** (Chinmay, 1 October): B, C and D each take about a third of the work after Block A, never
    # more than the team completes by the block's target (so each still ends on it); D takes what is left.
    rest = sum(v for k, v in am_pts.items() if am_info[k]["block"] not in sp.BLOCK_A_FAMILY
               and am_info[k]["platform"] != "AI")
    later_b = sp.LATER_BLOCKS
    budget = {b_: min(done_by[b_], run + rest * (i + 1) / len(later_b)) for i, b_ in enumerate(later_b)}
    cur = sp.BLOCKS.index("B")
    for k, a in sorted(am_info.items(), key=lambda x: x[1]["order"]):
        if a["block"] in sp.BLOCK_A_FAMILY:
            continue
        if a["platform"] == "AI":
            a["block"] = sp.BLOCKS[earliest_block(k)]
            continue
        run += am_pts.get(k, 0.0)
        while cur < len(sp.BLOCKS) - 1 and run > budget[sp.BLOCKS[cur]] + 1e-6:
            cur += 1
        a["block"] = sp.BLOCKS[cur]
    # **Each block is complete and testable on its own.** What an app-module's tasks wait on to be finished -- the
    # back end a screen is wired to, the migration a service writes into, the migration a key points into, a task
    # of the same service -- must be in its block or an earlier one. Shared back end and migrations are pulled into
    # the earliest block that needs them (they go with the first app-module that needs them; the later ones wait on
    # them). A report or read-only task waiting on another service's writers is not pulled: it is tested on seeded
    # data.
    later_leaf = [t_ for t_ in leaf if t_["key"] in later_set]

    def binds(t_, d):
        """Whether waiting on d ties t_'s block to d's."""
        dt_ = by_key[d]
        if t_["track"] == "Frontend":
            return dt_["track"] in ("Backend", "Database")
        if t_["track"] in ("Backend", "Database"):
            # a read waiting on its own service's writer does not tie the blocks either (lever B, CHG-RONEP-007)
            return dt_["track"] == "Database" or (dt_["track"] == "Backend" and dt_["service"] == t_["service"]
                                                  and not reads_only(t_))
        return False

    def reads_only(t_):
        """A back-end task none of whose operations writes a table: a list, a report, a lookup."""
        return t_["track"] == "Backend" and bool(ops_of.get(t_["key"])) and not any(
            not w.startswith(("cache:", "qdrant")) for o in ops_of[t_["key"]] for w in (lineage.get(o) or {}).get("writes") or [])

    def pull():
        for _ in range(40):
            changed = False
            for t_ in later_leaf:
                if not am_of.get(t_["key"]):
                    continue
                mine = am_info[am_of[t_["key"]]]
                for d in t_["dependsOn"].split():
                    if not am_of.get(d) or d not in later_set or not binds(t_, d):
                        continue
                    theirs = am_info[am_of[d]]
                    if BRANK[theirs["block"]] <= BRANK[mine["block"]]:
                        continue
                    if by_key[d]["track"] in ("Backend", "Database"):
                        am_of[d] = mine["key"]                 # pull the shared back end into the earlier block
                    else:
                        mine["block"] = theirs["block"]
                    changed = True
            if not changed:
                break

    pull()

    def prune_reads():
        """**A read is not a reason to wait for a later block** (1 October). A back-end task waits on another
        service's writer only to have data to read (a report, a dashboard, a read-only list); when that writer is in
        a later block, the read is built and tested on seeded data in its own block and reports more as the later
        module lands, so the wait is dropped -- otherwise one report pulled into Block A waits for Block D.
        **Inside one service too** (lever B, Chinmay, 3 October, CHG-RONEP-007: "don't pull a service's writers into
        Block A just because its reads are there"): a read-only task's wait on a writer of its own service in a later
        block is dropped, and it does not pull that writer (binds)."""
        for t_ in leaf:
            if t_["track"] != "Backend" or not am_of.get(t_["key"]):
                continue
            mine = BRANK[am_info[am_of[t_["key"]]]["block"]]
            keep = []
            for d in t_["dependsOn"].split():
                dt_ = by_key.get(d)
                if (dt_ and am_of.get(d) and dt_["track"] == "Backend"
                        and (dt_["service"] != t_["service"] or reads_only(t_))
                        and not d.startswith(("PLATFORM-", "KERNEL-", "SETUP-", "MIG-"))
                        and BRANK[am_info[am_of[d]]["block"]] > mine):
                    continue
                keep.append(d)
            t_["dependsOn"] = " ".join(keep)

    prune_reads()

    # **The test strategy** (decided 1 October, docs/active/block-test-strategy.md). A module test per app-module:
    # about 10% of its points (at least 2), by a peer in its stack who is not its main builder (the scheduler skips
    # whoever built most of it), waiting on every ticket in it, so it lands right after the last one. A block test
    # per block: a back-end and a front-end tester (a pair rotating per block, team.json sprintPlan.blockTests), led
    # by Chinmay Parab, in the last three working days of the block's final sprint, waiting on its module tests.
    # In those three days no new feature task starts (sprint_plan.schedule `freeze`).
    TRACK_ORDER["Test"] = 6
    am_tasks = defaultdict(list)
    for t_ in leaf:
        am_tasks[am_of[t_["key"]]].append(t_)

    # AM-AI-ENGINE-A2 (CHG-RONEP-010) is AI engine work like a later capability: accepted on its own module test, it
    # does not hold Block A2 open
    A_AI = {"AM-AI-ENGINE-A", "AM-AI-ENGINE-A-BASELINE"}

    def is_ai_engine(k):
        return am_info[k]["platform"] == "AI" and k not in A_AI

    # **What a phase 1 AI unit cannot be accepted without** (CHG-AIPH-001): ai-phase-plan.json `needs` names operations,
    # screens and tasks; each resolves to the leaf tasks that build it (an operation's back-end task, a screen's tasks,
    # its setup and rest-of-the-screen parts included), and the unit's module test waits on them.
    leaf_keys = {t_["key"] for t_ in leaf}
    op_builders = defaultdict(set)
    for k_, os_ in ops_of.items():
        for o in os_:
            if k_ in leaf_keys:
                op_builders[o].add(k_)
    ai_need_missing = defaultdict(list)

    def ai_need_keys(k):
        need = ai_needs.get(k) or {}
        out = set()
        for o in need.get("operations") or []:
            if op_builders.get(o):
                out |= op_builders[o]
            else:
                ai_need_missing[k].append(f"operation {o}")
        for s_ in need.get("screens") or []:
            hit = {x for x in leaf_keys if re.search(rf"(?:^|-){re.escape(s_)}(?:-REST)?$", x)
                   and not x.startswith("TEST-")}
            if hit:
                out |= hit
            else:
                ai_need_missing[k].append(f"screen {s_}")
        for x in need.get("tasks") or []:
            if x in leaf_keys:
                out.add(x)
            else:
                ai_need_missing[k].append(f"task {x}")
        return sorted(out - {x["key"] for x in am_tasks.get(k, ())})

    for k, ch in sorted(am_tasks.items()):
        pts = sum(int(x["points"] or 0) for x in ch)
        days = sum(float(x.get("days") or days_ex.get(x["key"]) or 0) for x in ch)
        pools = Counter()
        for x in ch:
            pools[pool_of(x)] += int(x["points"] or 0) or float(x.get("days") or days_ex.get(x["key"]) or 0)
        pool = pools.most_common(1)[0][0] if pools else "be"
        if am_info[k]["platform"] == "AI":
            pool = "ai"                                  # an AI capability is tested by the other AI engineer
        tk = f"TEST-{k}"
        a = am_info[k]
        is_a = a["block"] == "A"
        # **A module test names what it tests** (r1 gate G1, CHG-RONEP-003): the screens, operations and tables its
        # app-module's tasks build, as its builds (so ADAM links them) and in its done-when. It said "every screen state
        # its YAML lists" and named no screen, so the judge could not tell what to test.
        arts = []
        for x in sorted(ch, key=lambda x: (TRACK_ORDER.get(x["track"], 9), x["key"])):
            for b_ in ticket_done.builds_of(x, "", lineage):
                if b_ not in arts and not b_.startswith(("service ", "adr ")):
                    arts.append(b_)
        # **A module test tests what its app reaches** (4 October, the Sprint 1-2 judging; CHG-FXP-006): an app-module
        # with screens tests those screens and the operations they call; an operation that rides in the module for
        # another app (TEST-AM-RESOURCES-CAPACITY-P01 named four staff-only Venue Management operations WEB-047 never
        # calls) is proven by its own ticket's contract tests, not by this module's.
        scr_ = [b_.split(" ", 1)[1] for b_ in arts if b_.startswith("screen ")]
        if scr_ and am_info[k]["platform"] != "AI":
            called_ = {o for x in scr_ if x in screens for o in screen_ops(x)}
            arts = [b_ for b_ in arts if not b_.startswith("operation ") or b_.split(" ", 1)[1].split("#")[-1] in called_]
        arts.sort(key=lambda b_: ({"screen": 0, "operation": 1, "table": 2}.get(b_.split(" ")[0], 3), b_))
        names_ = [b_.split(" ", 1)[1] for b_ in arts]
        named = (", ".join(f"`{n_}`" for n_ in names_[:12]) + (f" and {len(names_) - 12} more" if len(names_) > 12 else "")
                 if names_ else "")
        kinds_ = {b_.split(" ")[0] for b_ in arts}
        # **What the test does follows what the module holds** (CHG-FXP-006): screen and API wording on a module of
        # migrations (TEST-AM-FOUNDATION-DATABASE) or of setup tickets with nothing to link (TEST-AM-FOUNDATION-SETUP)
        # gave the tester nothing to run.
        if am_info[k]["platform"] == "AI":     # the AI engine's module tests keep their words (branch r1-ai-phase owns them)
            what_ = ("every screen state its YAML lists, every navigation link, every permission (an allowed and a refused "
                     "user), every operation's error responses, and for an offline app its offline behaviour with the network "
                     "cut. ")
            done_ = "Done when it passes " + (f"for {named} " if named else "") + "with no open severity 1 or 2 defect. "
        elif not arts:
            what_ = ("re-run, on the integration environment, the done-when of each of its tickets ("
                     + ", ".join(sorted(x["key"] for x in ch)) + "), as a peer who did not do them, and record the "
                     "evidence each asks for. ")
            done_ = "Done when every one of those done-whens holds on the integration environment with no open severity 1 or 2 defect. "
        elif kinds_ == {"table"}:
            what_ = ("the migrations of its tickets, in plan order, on an empty database and on the previous release's "
                     "schema: each applies once and a second run applies nothing, every table matches its record in ADAM "
                     "(columns, keys, indexes, row-level security forced), a row in another tenant's or venue's scope is "
                     "not visible under a scoped session, and a row pointing at a missing parent is refused. ")
            done_ = f"Done when it passes for {named} with no open severity 1 or 2 defect. "
        else:
            what_ = ("every screen state its YAML lists, every navigation link, every permission (an allowed and a refused "
                     "user), every operation's error responses, and, where its tickets build an offline path, that path "
                     "with the network cut (a part a ticket leaves to an open decision is tested as that ticket's "
                     "done-when says, no further). ")
            done_ = f"Done when it passes for {named} with no open severity 1 or 2 defect. "
        bare_ = sorted(x["key"] for x in ch if not [b_ for b_ in ticket_done.builds_of(x, "", lineage)
                                                    if not b_.startswith(("service ", "adr "))])
        if arts and bare_ and am_info[k]["platform"] != "AI":
            what_ += ("It also re-runs the done-when of each of its tickets that builds no artefact ("
                      + ", ".join(bare_) + ") and records the evidence each asks for. ")
        waits_ = sorted({o for o in (n_.split("#")[-1] for n_ in names_) if (ops.get(o) or {}).get("makeOrBreak")}
                        ) if am_info[k]["platform"] != "AI" else []
        if waits_:
            done_ += ("Waiting on the client: " + ", ".join(f"`{o}` ({first_sentence(ops[o]['makeOrBreak'], 160).rstrip('.')})"
                                                            for o in waits_)
                      + "; until it arrives each is tested against the provider's documented test payloads with a "
                      "locally generated secret, and its live-sandbox run is accepted when it arrives. ")
        task(tk, k, "Task", f"Module test: {a['name']}",
             (("Builds: " + ", ".join(f"`{b_}`" for b_ in arts) + ". ") if arts else "") +
             f"The module test of {a['name']} on the integration environment (docs/active/block-test-strategy.md): "
             + what_ + done_ +
             f"By a peer in the module's stack who did not build most of it. {len(ch)} tickets, {pts} points"
             + (f", {days:g} AI-engineer days" if days else "") + ".",
             min((int(x["wave"]) for x in ch if str(x["wave"]).isdigit()), default=3), area="test",
             pts=max(tests["minPoints"], round(tests["share"] * pts)) if pts else "",
             depends=[x["key"] for x in ch] + ai_need_keys(k))
        t_ = by_key[tk]
        t_["track"], t_["subject"] = "Test", f"[Test] Module test: {a['name']}"
        t_["phase"] = 1 if is_a else 2
        t_["pool"] = pool
        t_["peerOf"] = [x["key"] for x in ch]
        if pool == "ai":
            t_["points"] = ""
            t_["days"] = max(1.0, round(tests["share"] * (days + pts / sp.PLAN_PACE), 1))
        elif not pts:
            t_["days"] = max(1.0, round(tests["share"] * days, 1))
        t_["tier"] = 0
        step[tk] = 1 + max((step.get(x, 0) for x in t_["dependsOn"].split()), default=0)
        if k in ai_phase2:
            ai_phase2.add(tk)
        am_of[tk] = k
        leaf.append(t_)
        later_set.add(tk) if not is_a else a_keys.add(tk)
    block_tests = {}
    for i, b in enumerate(sp.BLOCKS):
        be_, fe_ = sp.test_pair(b, tests)
        for side, who in (("BE", be_), ("FE", fe_)):
            tk = f"TEST-BLOCK-{b}-{side}"
            task(tk, f"BLOCK-{b}", "Task", f"Block {b} test ({'back end' if side == 'BE' else 'front end'})",
                 f"The block test of Block {b} (docs/active/block-test-strategy.md), led by {tests['lead']}: every flow "
                 f"the block claims end to end on the integration environment, the offline runs, and the load run where "
                 f"the block adds a purchase or admission path; then the client's acceptance session. Pair: {be_} (back "
                 f"end) and {fe_} (front end). In the last {tests['days']:g} working days of the block's final sprint; no "
                 "new feature work starts in them.", 3, area="test", assignee=who)
            t_ = by_key[tk]
            t_["track"], t_["subject"] = "Test", t_["subject"].replace("[FE]", "[Test]")
            t_["phase"] = 1 if b == "A" else 2
            t_["days"] = tests["days"]
            t_["block"] = b
            t_["tier"] = 0
            t_["pool"] = "be" if side == "BE" else "web"
            step[tk] = 999
            am_of[tk] = None
            block_tests[tk] = b
            leaf.append(t_)

    # **An AI engine task another AI engine task of its block waits on goes first in its engineer's queue** (CHG-RONEP-010):
    # the second AI engineer built the 15-day baseline before Qdrant tenancy, so the concierge waited until day 31 and
    # the A1 AI work ran past 24 November.
    ai_waiters = Counter()
    for t_ in leaf:
        if t_["track"] == "AI" and am_of.get(t_["key"]):
            for d in t_["dependsOn"].split():
                if d in by_key and by_key[d]["track"] == "AI" and am_of.get(d)                         and am_info[am_of[d]]["block"] == am_info[am_of[t_["key"]]]["block"]:
                    ai_waiters[d] += 1

    def block_first(t_):
        if t_["key"] in block_tests:
            return (BRANK[block_tests[t_["key"]]], (9, 99, 99, 9, 99), (9, 0), 9, 999, 7, t_["key"])
        a_ = am_info[am_of[t_["key"]]]
        if t_["track"] == "Test" and t_.get("pool") == "ai":
            # an AI engine module test is placed after every AI engine task of its block, so the peer engineer
            # finishes their own block's work (the evaluation harness) before testing the other's (CHG-RONEP-010).
            # A phase 1 unit's test in a block not ticketed yet also waits on its back end and screens (CHG-AIPH-001):
            # it goes after every AI engine unit, so a one-day test placed early cannot split the gap a long unit needs
            # (the configuration assistant's 25 days waited behind lower-ranked units until it did).
            late_ = am_of[t_["key"]] in ai_needs and a_["block"] not in settings["ticketBlocks"]
            return (len(sp.BLOCKS) if late_ else BRANK[a_["block"]], (8, 99, 99, 9, 99), (9, 0), 9, step[t_["key"]], 6,
                    t_["key"])
        # **A decided app-module added after its block's tickets were pushed is scheduled after them** (CHG-R4-003,
        # 5 October): `scheduleAfter: B` places its tasks behind every Block B task in the build order, so the work
        # already pushed keeps its owners and sprints, and the new work takes the capacity left (its block is unchanged)
        rank_ = BRANK[a_["block"]] if not a_.get("scheduleAfter") else BRANK[a_["scheduleAfter"]] + 0.5
        return (rank_, a_["order"], (t_["tier"], -ai_waiters.get(t_["key"], 0)), int(t_["wave"] or 9),
                step[t_["key"]], TRACK_ORDER[t_["track"]], t_["key"])

    # **Pass 2: each block on a sprint boundary, its test in the last three days.** Scheduled block first, with each
    # block's test window frozen. An app-module of B or C that still finishes after its block's target window opens,
    # and that nothing in its block or an earlier one waits on, moves to the next block (D takes what is left). A
    # block's final sprint is the first, from its target, whose window opens after the block's work (its tickets
    # and module tests) is done; Block A's is wherever that falls.
    final = {b: targets[b] for b in sp.BLOCKS}
    seen_finals = []
    prune_reads()
    for _round in range(10):
        for tk, b in block_tests.items():
            # the AI engine's module tests may overlap the block test (Chinmay, 1 October): they do not gate it
            # a decided app-module scheduled after a block (CHG-R4-003) is tested in its block test, and does not hold the
            # block test's window: its module test ending before the window is checked below, not waited on
            mods = [f"TEST-{k}" for k, a in am_info.items() if a["block"] == b and k in am_tasks
                    and a["platform"] != "AI" and not a.get("scheduleAfter")]
            by_key[tk]["dependsOn"] = " ".join(sorted(mods))
            w0, w1 = sp.window_of(final[b], tests["days"])
            by_key[tk]["notBefore"] = w0
            windows[b] = (w0, w1)
        res_ = run_schedule(topo(block_first))
        fin = defaultdict(float)
        for k, r_ in res_.items():
            if k not in block_tests:
                fin[am_of[k]] = max(fin[am_of[k]], r_["end"])
        moved = 0
        for b in sp.LATER_BLOCKS[:-1]:
            limit = sp.window_of(targets[b], tests["days"])[0]
            late = {k for k, a in am_info.items() if a["block"] == b and fin.get(k, 0.0) > limit + 1e-6}
            if not late:
                continue
            # the late app-modules move to the next block; the back end an app-module left in this block still
            # needs is pulled back into it (it goes with the first app-module that needs it)
            nxt = sp.BLOCKS[sp.BLOCKS.index(b) + 1]
            for k in late:
                am_info[k]["block"] = nxt
                moved += 1
        if moved:
            pull()
        new_final = {}
        for b in sp.BLOCKS:
            last = max([v for k, v in fin.items() if k and am_info[k]["block"] == b and not is_ai_engine(k)] or [0.0])
            new_final[b] = sp.final_sprint(last, tests["days"], at_least=targets[b] if b != "A" else 1)
            if b in settings["fixed"]:
                # decided (Block A: 40 working days, Sprint 4): its test sits in its target sprint; the work still
                # running at normal hours is the overtime the deck reports
                new_final[b] = targets[b]
        if moved:
            prune_reads()
        if not moved and new_final == final:
            break
        if not moved and new_final in seen_finals:
            # a window that moves the work it is computed from can flip between two sprints: take the later one
            final = {b: max(f_[b] for f_ in seen_finals + [new_final, final]) for b in sp.BLOCKS}
            break
        seen_finals.append(dict(new_final))
        final = new_final
    block_final = dict(final)
    for tk, b in block_tests.items():                     # the windows of the final sprints (the last round's or later)
        w0, w1 = sp.window_of(block_final[b], tests["days"])
        by_key[tk]["notBefore"] = w0
        windows[b] = (w0, w1)
    for k, a in am_info.items():                          # CHG-R4-003: a late-added module must still end before its window
        if a and a.get("scheduleAfter") and k in fin and a["block"] in windows and fin[k] > windows[a["block"]][0] + 1e-6:
            print(f"WARNING: {k} (scheduled after Block {a['scheduleAfter']}) ends on day {fin[k]:.1f}, after Block "
                  f"{a['block']}'s test window opens (day {windows[a['block']][0]:g}); its block test will not cover it")

    # **The hierarchy** (1 October): Epic = Block, Feature = app-module, Task = the work under its pushed key. The
    # service and app epics and their group features of 23-30 September leave the plan; op-release.py closes them
    # once their tickets have moved (re-parenting is allowed, renaming is not). A block test sits on its epic.
    tasks[:] = leaf
    by_key = {t_["key"]: t_ for t_ in tasks}
    used_ams = {am_of[t_["key"]] for t_ in tasks if am_of[t_["key"]]}
    for t_ in tasks:
        if t_["key"] in block_tests:
            t_["parent"] = f"BLOCK-{block_tests[t_['key']]}"
            continue
        t_["parent"] = am_of[t_["key"]]
        t_["block"] = am_info[t_["parent"]]["block"]
    order_ = topo(block_first)
    struct = {}
    for b in sp.BLOCKS:
        if any(am_info[k]["block"] == b for k in used_ams):
            struct[f"BLOCK-{b}"] = {"key": f"BLOCK-{b}", "parent": "", "type": "Epic", "track": "", "phase": "",
                                    "subject": f"Block {b}", "wave": "", "points": "", "assignee": "", "area": "",
                                    "platform": "", "service": "", "dependsOn": "", "description": "", "tier": "",
                                    "block": b, "step": ""}
    for k in used_ams:
        a = am_info[k]
        struct[k] = {"key": k, "parent": f"BLOCK-{a['block']}", "type": "Feature", "track": "", "phase": "",
                     "subject": a["name"], "wave": "", "points": "", "assignee": "", "area": "",
                     "platform": sp.PLATFORM_NAME.get(a["platform"], ""), "service": "", "dependsOn": "",
                     "description": "", "tier": "", "block": a["block"], "step": ""}
    seq, out_ = 0, []
    for t_ in order_:
        for p in (f"BLOCK-{t_['block']}", t_["parent"]):
            if p in struct and "sequence" not in struct[p]:
                seq += 1
                struct[p]["sequence"] = seq
                out_.append(struct[p])
        seq += 1
        t_["sequence"] = seq
        t_["step"] = step[t_["key"]]
        out_.append(t_)
    tasks[:] = out_
    by_key = {t_["key"]: t_ for t_ in tasks}

    # **Key stability** (30 September): the work on a pushed ticket keeps that ticket's key (see
    # reconcile_keys). Applied last, so the plan above -- phase, track, tier, order, links -- is formed from
    # the keys exactly as before and only the names change. With today's plan it renames nothing.
    work = defaultdict(set)
    for o, k in list(op_task.items()) + list(vm_op_task.items()) + list(later_op_task.items()):
        work[k].add(o)
    for t, k in list(table_mig.items()) + list(vm_mig.items()) + list(later_mig.items()):
        if k != "MIG-BASELINE":
            work[k].add(t)
    for t_ in tasks:
        ident = key_identity(t_["key"])
        if t_["type"] == "Task" and ident and ident[0] == "screen":
            work[t_["key"]] = {ident[1]}
    kmap_path = OUT / "pms-map.json"
    kmap = json.loads(kmap_path.read_text(encoding="utf-8")) if kmap_path.exists() else {}
    stable, notes = reconcile_keys({k: v for k, v in work.items() if k in by_key and key_identity(k)},
                                   {t_["key"] for t_ in tasks if t_["key"] not in work or not key_identity(t_["key"])},
                                   kmap, closed_keys())
    renamed = {k: v for k, v in stable.items() if k != v}
    if renamed:
        def rk(k):
            return renamed.get(k, k)

        for t_ in tasks:
            t_["key"], t_["parent"] = rk(t_["key"]), rk(t_["parent"])
            t_["dependsOn"] = " ".join(sorted(rk(d) for d in t_["dependsOn"].split()))
        by_key = {t_["key"]: t_ for t_ in tasks}
        step = {rk(k): v for k, v in step.items()}
        op_task = {o: rk(k) for o, k in op_task.items()}
        for rows_, col in ((migrations, 1), (tables_rows, 0), (vm_rows, 1)):
            for r_ in rows_:
                r_[col] = rk(r_[col])
        mig_md = OUT / "backend" / "MIGRATIONS.md"
        text = mig_md.read_text(encoding="utf-8")
        for k, v in renamed.items():
            text = re.sub(rf"(?<![\w-]){re.escape(k)}(?![\w-])", v, text)
        mig_md.write_text(text, encoding="utf-8")
    for n_ in notes:
        print(f"key stability: {n_}")
    print(f"key stability: {len(renamed)} planned keys written under the key their work was pushed as")

    # **Every forward migration names its file** (3 October, CHG-TBF-002; Block A audit pattern 6). Until now only the
    # first release's migrations had a file name (V0002-V0099, in schema order) and the 135 forward migrations of the
    # Venue Management waves and the later app-modules said their numbers would be "given when they merge", so two
    # developers could merge the same number and nothing in the plan said which file a ticket was. They take V1000
    # upwards in build order: V0100-V0999 are derive-ddl's frozen-mode files (backend/<db>/V01xx__after_r1_*.sql), and
    # a file number is never reused. **A number, once planned, is kept** (from the plan this run replaces), so a refresh
    # never renumbers a ticket somebody may have started; `--renumber-migrations` drops the pins before a first push.
    # Applied after key stability, so the pins are read under the keys the tickets were pushed with.
    fwd_head = re.compile(r"^(\[DB\] )Forward migration: (\w+) for ")
    fwd_tasks = [t_ for t_ in tasks if t_["type"] == "Task" and fwd_head.match(t_["subject"])]
    taken, fname_of = set(), {}
    for t_ in fwd_tasks:
        sch = fwd_head.match(t_["subject"]).group(2)
        m = MIG_FILE.search(prior_files.get(t_["key"], ""))
        if m and int(m.group(2)) >= FORWARD_TICKET_FIRST and int(m.group(2)) not in taken                 and m.group(1).endswith(f"__{sch}.sql"):
            taken.add(int(m.group(2)))
            fname_of[t_["key"]] = m.group(1)
    nxt = max(taken | {FORWARD_TICKET_FIRST - 1}) + 1
    # **A new migration runs before the kept ones that wait on it** (4 October, CHG-RFM-005). VM-MIG-WALLET first
    # appeared after the fix round's contracts (a Venue Management screen reached a new wallet table) and took V1196,
    # after MIG-WALLET-2..6 (V1128-V1194), which depend on it: they would have run first (M-FILE-ORDER). A migration
    # with no kept number takes the next one only if every kept migration depending on it is numbered after that;
    # otherwise the lowest free number between its own dependencies and its first dependent (the numbers retired
    # tickets left). Kept numbers never move.
    num_of_ = {}
    for t_ in tasks:
        m_ = MIG_FILE.search(t_["subject"])
        if m_:
            num_of_[t_["key"]] = int(m_.group(2))
    for k_, f_ in fname_of.items():
        num_of_[k_] = int(MIG_FILE.search(f_).group(2))
    dependents_ = defaultdict(set)
    for t_ in tasks:
        for d_ in (t_.get("dependsOn") or "").split():
            dependents_[d_].add(t_["key"])
    for t_ in fwd_tasks:
        if t_["key"] in fname_of:
            continue
        upper = min((num_of_[x] for x in dependents_[t_["key"]] if x in fname_of), default=None)
        n_ = nxt
        if upper is not None and nxt >= upper:
            lower = max([num_of_[d_] for d_ in (t_.get("dependsOn") or "").split() if d_ in num_of_]
                        + [FORWARD_TICKET_FIRST - 1])
            free = [x for x in range(lower + 1, upper) if x not in taken]
            if free:
                n_ = free[0]
        if n_ == nxt:
            nxt += 1
        taken.add(n_)
        num_of_[t_["key"]] = n_
        fname_of[t_["key"]] = f"V{n_:04d}__{fwd_head.match(t_['subject']).group(2)}.sql"
    fwd_rows = []
    for t_ in fwd_tasks:
        f_ = fname_of[t_["key"]]
        t_["subject"] = fwd_head.sub(lambda m: f"{m.group(1)}Forward migration {f_}: {m.group(2)} for ", t_["subject"],
                                     count=1)[:255]
        ts_ = (re.search(r"Tables: (.+?)\. Source", t_["description"]) or [None, ""])[1].split(", ")
        ts_ = [x for x in ts_ if x]
        fwd_rows.append([int(MIG_FILE.search(f_).group(2)), f_, t_["key"],
                         (ddl.get(ts_[0]) or {}).get("db", "") if ts_ else "", f_.split("__", 1)[1][:-4], len(ts_),
                         ", ".join(ts_)])
    fwd_rows.sort()
    print(f"forward migrations: {len(fwd_rows)} named V{FORWARD_TICKET_FIRST:04d} upwards, "
          f"{sum(1 for k in fname_of if MIG_FILE.search(prior_files.get(k, '')))} kept from the last plan")

    # **Every table is in a migration or says why not** (CHG-TBF-003). The tables nothing reaches are storage the
    # contracts describe and no operation reads or writes yet; they are listed with that reason rather than
    # migrated (a table no code touches is a migration nobody can test), and the one an operation does reach is a
    # gap tools/check-migration-tickets.py fails on.
    assigned = set(table_mig) | set(vm_mig) | set(later_mig)
    reached = defaultdict(set)
    for o, x in lineage.items():
        for kk in ("reads", "writes"):
            for t in (x or {}).get(kk) or []:
                reached[t].add(o)
    storage_only = []
    for t in sorted(set(ddl) - assigned):
        if reached.get(t) and all((ops.get(o) or {}).get("hold") for o in reached[t]):
            # only operations the plan holds out reach it (CHG-FXP-003): its migration comes with them
            storage_only.append((t, "held: only operations not built until their contract is agreed reach it ("
                                 + ", ".join(f"{o}: {ops[o]['hold']}" for o in sorted(reached[t])[:4])
                                 + "); its forward migration is planned with them"))
        elif reached.get(t):
            storage_only.append((t, "GAP: read or written by " + ", ".join(sorted(reached[t])[:4])
                                 + " but in no migration"))
        else:
            storage_only.append((t, "storage only: no operation reads or writes it and no task names it; its "
                                    "forward migration is planned when an operation first reaches it"))
    M2 = ["", "## Forward migrations after the first release", "",
          f"**{len(fwd_rows)} forward migrations**, V{FORWARD_TICKET_FIRST:04d} upwards in build order (the Venue "
          "Management waves, then each later app-module). V0100-V0999 are derive-ddl's frozen-mode files in "
          "`backend/<db>/`; a number is never reused, and a planned number is kept on the next refresh. "
          "The ticket's subject names the same file.", ""]
    M2 += table(["Number", "File", "Task", "Database", "Schema", "Tables", "Which tables"],
                [[r[0], f"`{r[1]}`", r[2], r[3], r[4], r[5], r[6]] for r in fwd_rows])
    M2 += ["", "## Tables no migration creates", "",
           f"**{len(storage_only)} tables** in `backend/` that no migration above creates, each with the reason. "
           "Row-level security on a table with no `tenant_id` is the tenant-root policy, by design: one tenant per "
           "database (ADR-0038), `platform.tenant_root_in_scope()`.", ""]
    M2 += table(["Table", "Database", "Source DDL", "Why"],
                [[f"`{t}`", ddl[t]["db"], ddl[t]["file"], why_] for t, why_ in storage_only])
    mig_md, NL = OUT / "backend" / "MIGRATIONS.md", chr(10)
    mig_md.write_text(mig_md.read_text(encoding="utf-8").rstrip(NL) + NL + NL.join(M2) + NL, encoding="utf-8")
    print(f"tables no migration creates: {len(storage_only)} "
          f"({sum(1 for _, w in storage_only if w.startswith('GAP'))} reached by an operation)")

    # **Owners** (plan item L2, 1 October). A pushed ticket keeps the owner its last release gave it, from release
    # `sprintPlan.stableOwners.since` on, unless --rebalance; started tickets are kept by op-release.rb in any case.
    # Then pass 2: every task without an owner (the later blocks' new work) goes to whoever in its pool can start it
    # first, in build order -- the same placement derive-block-a-schedule.py reproduces for the dates.
    pins, pin_note = sp.pinned_owners(team, rebalance="--rebalance" in sys.argv[1:])
    for t_ in tasks:
        if t_["type"] == "Task" and t_["key"] in pins and t_["key"] in kmap:
            t_["assignee"] = pins[t_["key"]]
    print(f"owners: {pin_note}")
    # **The migration rule wins over the pin** (CHG-R5-001): a pushed migration goes to the migration owner, so the
    # release bundle reassigns it and its table sub-tasks (op-release.rb moves New tickets; the lead moved the started
    # ones in OpenProject on 7 October).
    if MIG_OWNER:
        mig_moved = [t_["key"] for t_ in tasks if t_["type"] == "Task" and sp.is_migration_of(MIG_RX, t_["key"])
                     and t_["assignee"] != MIG_OWNER]
        for t_ in tasks:
            if t_["type"] == "Task" and sp.is_migration_of(MIG_RX, t_["key"]):
                t_["assignee"] = MIG_OWNER
        print(f"migrations: every task matching {MIG_RX.pattern} is {MIG_OWNER}'s (CHG-R5-001); "
              f"{len(mig_moved)} moved from the pin or the plan")
    leaf = [t_ for t_ in tasks if t_["type"] == "Task"]
    # **Phase 2 of the AI engine has no owner** (CHG-AIPH-001, docs/active/ai-phase-plan.json; CHG-R4-006): its AI units,
    # its module tests and its app-modules stay unassigned until the AI developers join after 2 April.
    for t_ in leaf:
        if t_["key"] in ai_phase2 and t_["area"] in ("ai", "test"):
            t_["assignee"] = ""
    second = run_schedule(leaf)
    for t_ in leaf:
        r_ = second.get(t_["key"])
        if not t_["assignee"] and r_ and r_["who"] and not (t_["key"] in ai_phase2 and t_["area"] in ("ai", "test")):
            t_["assignee"] = r_["who"]
    # **The AI engine past 2 April** (Chinmay, 1 October): every task is created, and those the two AI engineers
    # cannot finish by the end of the six months stay unassigned for the AI developers joining later.
    ai_cut = sp.index_of(sp.PLAN_END) + 1
    # A phase 2 unit (CHG-AIPH-001) is past 2 April by its notBefore and has no owner by design; its text says so.
    for t_ in leaf:
        if t_["key"] in ai_phase2 and t_["area"] == "ai":
            t_["assignee"] = ""
    ai_open = [t_ for t_ in leaf if t_["area"] == "ai" and t_["key"] not in kmap and t_["key"] not in ai_phase2
               and (second.get(t_["key"]) or {}).get("end", 0) > ai_cut]
    for t_ in ai_open:
        t_["assignee"] = ""
        t_["description"] = (t_["description"].rstrip() + " Unassigned (1 October): past what the two AI engineers "
                             "finish by 2 April; for the AI developers joining.")
    print(f"AI engine: {len(ai_open)} task(s) of phase 1 past 2 April left unassigned (should be none), "
          f"{sum(1 for k in ai_phase2 if k in ai_unit)} phase 2 unit(s) after 2 April, unassigned and not ticketed")
    # **The completion check of every phase 1 unit** (CHG-AIPH-001, "do not pick trails that we cannot complete"): the
    # unit's own work, its module test and everything the test waits on (its back end, the owner-side operations,
    # its screens) end by 2 April. Printed on every run; written into the unit's description.
    ai_completion = {}

    def fmt_day(i):
        if i is None:
            return "unscheduled"
        d_ = sp.day(max(i - 1e-6, 0))
        return f"{d_.strftime('%a')} {d_.day} {d_.strftime('%b %Y')}"

    for tk, u_ in sorted(ai_unit.items(), key=lambda x: (x[1]["phase"], x[1]["rank"])):
        if u_["phase"] != 1:
            continue
        test_k = f"TEST-{u_['module']}"
        own = second.get(tk) or {}
        tst = second.get(test_k) or {}
        waits = [d for d in by_key[test_k]["dependsOn"].split() if d != tk] if test_k in by_key else []
        last = max(waits, key=lambda d: (second.get(d) or {}).get("end", 0.0), default=None)
        last_end = (second.get(last) or {}).get("end", 0.0) if last else 0.0
        ok = own.get("end", 1e9) <= ai_cut + 1e-6 and tst.get("end", 1e9) <= ai_cut + 1e-6 and last_end <= ai_cut + 1e-6
        ai_completion[tk] = {"start": own.get("start"), "end": own.get("end"), "test": test_k,
                             "testEnd": tst.get("end"), "lastNeed": last, "lastNeedEnd": last_end, "ok": ok,
                             "missing": ai_need_missing.get(u_["module"], [])}
        print(f"  AI phase 1 #{u_['rank']} {tk} ({by_key[tk]['assignee'] or 'unassigned'}): "
              f"{sp.day(own.get('start', 0)).isoformat()} to {sp.day(max(own.get('end', 0) - 1e-6, 0)).isoformat()}; "
              f"its needs land by {sp.day(max(last_end - 1e-6, 0)).isoformat()} ({last}); module test ends "
              f"{sp.day(max(tst.get('end', 0) - 1e-6, 0)).isoformat()} -> {'OK' if ok else 'PAST 2 APRIL'}"
              + (f"; not found in the plan: {', '.join(ai_completion[tk]['missing'])}" if ai_completion[tk]["missing"] else ""))
        if not ok:
            print(f"WARNING: AI phase 1 unit {tk} does not complete by 2 April: move a dependency or the unit to phase 2")
        by_key[tk]["description"] = by_key[tk]["description"].replace(
            "Done when ", f"Completion check (derived): its work ends {fmt_day(own.get('end'))}, what its module test "
            f"waits on lands by {fmt_day(last_end)}, the module test ends {fmt_day(tst.get('end'))}"
            f"{', inside the six months' if ok else ', PAST 2 April'}. Done when ", 1)
    queue_n = defaultdict(int)
    for t_ in tasks:
        if t_["type"] == "Task" and t_["assignee"]:
            queue_n[t_["assignee"]] += 1
            t_["queue"] = queue_n[t_["assignee"]]
        else:
            t_["queue"] = ""
    # **Accountable** is written on the row (it was read from the service epics, which are gone): a service's
    # owner for its back end and migrations, the area lead for a first-release screen, the app-module's lead else.
    LEAD_AREA = {"POS": "Pradnya Yeram", "MOB": "Chitrangi Mestry", "WEB": "Chinmay Patkar", "WL": "Chinmay Patkar",
                 "SETUP": "Pallavi Sawant", "VM": "Pallavi Sawant"}
    ai_lead = ((team.get("ai") or {}).get("who") or [""])[0]
    kids = defaultdict(list)
    for t_ in tasks:
        if t_["parent"]:
            kids[t_["parent"]].append(t_)
    lead_of = {}
    for k, ch in kids.items():
        c_ = Counter()
        for x in ch:
            if x["type"] == "Task" and x["assignee"]:
                c_[x["assignee"]] += float(x["points"] or 0) or float(x.get("days") or 0) * sp.PLAN_PACE
        lead_of[k] = c_.most_common(1)[0][0] if c_ else ""
    for t_ in tasks:
        if t_["type"] != "Task":
            continue
        if t_["key"] in block_tests:
            t_["accountable"] = tests["lead"]
        elif t_["track"] in ("Backend", "Database", "DevOps", "Setup", "Onboarding"):
            t_["accountable"] = svc_owner.get(t_["service"]) or devops
        elif t_["track"] == "AI":
            t_["accountable"] = ai_lead
        else:
            t_["accountable"] = LEAD_AREA.get(t_["area"]) or lead_of.get(t_["parent"]) or t_["assignee"]
    sched_of = {k: v for k, v in second.items()}

    def span(keys_):
        ss = [sched_of[k]["start"] for k in keys_ if k in sched_of]
        ee = [sched_of[k]["end"] for k in keys_ if k in sched_of]
        if not ss:
            return None
        return sp.sprint_of_index(min(ss)), sp.sprint_of_index(max(max(ee) - 1e-6, 0.0)), max(ee)

    def fmt(d):
        return f"{d.strftime('%a')} {d.day} {d.strftime('%b %Y')}"

    lineage_c = {o: (lineage.get(o) or {}).get("contract") or ops.get(o, {}).get("contract") for o in ops}
    block_end = {}
    for t_ in tasks:
        if t_["type"] != "Feature":
            continue
        ch = [x for x in kids[t_["key"]] if x["type"] == "Task"]
        a = am_info[t_["key"]]
        scr = sorted({key_identity(x["key"])[1] for x in ch if x["track"] == "Frontend" and key_identity(x["key"])}
                     | {re.sub(r"^.*?-([A-Z]+-\d{3,}[A-Z]?)-REST$", r"\1", x["key"]) for x in ch if x["key"].endswith("-REST")})
        opl = sorted({o for x in ch for o in ops_of.get(x["key"], ())})
        tbl = sorted({tt for x in ch if x["track"] == "Database"
                      for tt in (re.search(r"Tables: (.+?)\. Source", x["description"]) or [None, ""])[1].split(", ") if tt})
        pts = sum(int(x["points"] or 0) for x in ch)
        sp_ = span([x["key"] for x in ch])
        t_["points"] = pts
        t_["assignee"] = "" if t_["key"] in ai_phase2 else lead_of.get(t_["key"], "")   # phase 2: no lead (CHG-R4-006)
        t_["accountable"] = t_["assignee"]
        t_["area"] = {"P08": "VM", "P01": "WEB", "P02": "MOB", "P04": "POS", "P15": "POS"}.get(a["platform"], a["platform"])
        when = (f"planned Sprint {sp_[0]}" + (f" to Sprint {sp_[1]}" if sp_[1] != sp_[0] else "")
                + f", done by {fmt(sp.day(max(sp_[2] - 1e-6, 0)))}") if sp_ else "not scheduled"
        builds = ([f"screen {s_}" for s_ in scr] + [f"operation {lineage_c.get(o) or '?'}#{o}" for o in opl]
                  + [f"table {x}" for x in tbl])
        ticketed = a["block"] in settings["ticketBlocks"]
        t_["description"] = (
            f"{a['name']}: {a['module']} on {sp.PLATFORM_NAME.get(a['platform'], 'the platform')}. Block {a['block']}, "
            f"{when}. "
            f"Scope: {len(scr)} screens, {len(opl)} operations, {len(tbl)} tables, {pts} points"
            + (f", {sum(float(x.get('days') or 0) for x in ch):g} AI-engineer days" if any(x.get('days') for x in ch) else "")
            + "." + ("" if ticketed else
                     f" Phase 2 of the AI engine (after 2 April 2027; Chinmay, 4 October, CHG-AIPH-001): not ticketed for "
                     f"r1, and its {len(ch)} tasks are in plan-tasks.csv with the keys they will have." if t_["key"] in ai_phase2
                     else f" Block {a['block']} is ticketed at this level until it is planned; its "
                     f"{len(ch)} tasks are in plan-tasks.csv with the keys they will have.")
            + " Builds: " + ", ".join(builds) + "."
            # Last, so the pointer's done-when (ticket_done.done_when reads "Done when" to the end) is this sentence
            # alone: a Block C or D app-module is the ticket a developer works from until its tasks are ticketed, and
            # "Complete when" was no done-when to check-ticket-text (T-DONE-WHEN; CHG-GTR-002).
            + " Done when every screen, its back end and its tests are done and its module test passes end to end on "
            "the integration environment with no open severity 1 or 2 defect (block-test-strategy).")
        if sp_:
            block_end[a["block"]] = max(block_end.get(a["block"], 0.0), sp_[2])
    for t_ in tasks:
        if t_["type"] != "Epic":
            continue
        b = t_["block"]
        feats = [x for x in kids[t_["key"]] if x["type"] == "Feature"]
        apps = Counter(am_info[x["key"]]["platform"] for x in feats)
        end_sp = block_final[b]
        # where a tenth of the block's hours have started (front ends run ahead against the mock server)
        its = sorted((y for x in feats for y in kids[x["key"]] if y["key"] in sched_of),
                     key=lambda y: sched_of[y["key"]]["start"])
        tot = sum(float(y["points"] or 0) or float(y.get("days") or 0) * sp.PLAN_PACE for y in its) or 1.0
        run, first_sp = 0.0, 1
        for y in its:
            run += float(y["points"] or 0) or float(y.get("days") or 0) * sp.PLAN_PACE
            if run >= 0.1 * tot:
                first_sp = sp.sprint_of_index(sched_of[y["key"]]["start"])
                break
        w0, w1 = windows[b]
        ai_late = [x for x in feats if is_ai_engine(x["key"])]
        t_["subject"] = (f"Block A1: the first release, first drop (Sprints {first_sp}-{end_sp})" if b == "A"
                         else f"Block A2: the rest of Block A, its second drop (Sprints {first_sp}-{end_sp})"
                         if b == "A2" else f"Block {b} (Sprints {first_sp}-{end_sp})")
        t_["points"] = sum(int(x["points"] or 0) for x in feats)
        t_["accountable"] = tests["lead"]
        t_["description"] = (
            f"Block {sp.block_label(b)}: {len(feats)} app-modules, each complete and testable end to end (screens, back end, module "
            f"test done), ending Friday {fmt(sp.SPRINTS_ALL[end_sp - 1]['end'])}, the end of Sprint {end_sp} (target: "
            f"Sprint {settings['targets'][b]}). Block test {fmt(sp.day(w0))} to {fmt(sp.day(w1 - 1))}: no new feature "
            "work starts in those days. Apps: " + ", ".join(f"{sp.PLATFORM_NAME.get(p_, p_ or 'platform')} ({n})"
                                                          for p_, n in apps.most_common()) + "."
            + (f" The AI engine capabilities in it ({len(ai_late)}) are accepted on their own module tests, by the two "
               "AI engineers' calendar (docs/active/ai-functions-review-30-september.json)." if ai_late else ""))

    # **A split screen's two tickets each name what they build and who builds the rest** (4 October, the Sprint 1-2
    # judging; CHG-FXP-001). "BO-857 (the rest of the screen: 3 of its 7 operations)" linked all seven in the pull and
    # never said which three; its done-when "calls only its bound operations" could not be tested. The sentence goes
    # after the slice list (check-ticket-scope reads "In the slice: a, b" up to its full stop) and op-release.py puts it
    # in the pointer.
    for t_ in tasks:
        if t_["type"] != "Task" or not t_["key"].startswith("APP-SETUP-") or ticket_done.scope_of(t_):
            continue
        m_ = ticket_done.SCREEN.search(t_["key"])
        sid_ = m_.group(1) if m_ else None
        if sid_ not in setup_screens:
            continue
        all_ = sorted(set(screen_ops(sid_)) | set(setup_screens[sid_]))
        mine_ = set(setup_screens[sid_])
        if len(mine_) >= len(all_):
            continue
        d_ = t_["description"] or ""
        if t_["key"].endswith("-REST"):
            sib_ = t_["key"][:-len("-REST")]
            sent_ = ticket_done.scope_sentence(sid_, set(all_) - mine_, all_, sib_ if sib_ in by_key else None, False)
            cut_ = d_.find("this task adds the others. ")
            cut_ = cut_ + len("this task adds the others. ") if cut_ >= 0 else 0
        else:
            sib_ = t_["key"] + "-REST"
            sent_ = ticket_done.scope_sentence(sid_, mine_, all_, sib_ if sib_ in by_key else None, True)
            m2_ = re.match(r"In the slice: [A-Za-z0-9, ]+", d_)
            cut_ = m2_.end() if m2_ else 0
            if m2_:
                d_ = d_[:cut_] + "." + d_[cut_:].lstrip(".")
                cut_ += 1
        t_["description"] = (d_[:cut_].rstrip() + " " + sent_ + " " + d_[cut_:].lstrip()).strip()
    # **A wired screen's own ticket says what it leaves to the wiring task** (CHG-R4-003): its scope is the screen's other
    # operations, and the wired ones are named with the task that wires them, as a split screen's two tickets do
    # (CHG-FXP-001).
    for t_ in tasks:
        if t_["type"] != "Task" or t_["key"].startswith("TEST-") or ticket_done.scope_of(t_):
            continue
        ident = key_identity(t_["key"])
        if not ident or ident[0] != "screen" or ident[1] not in wired_off:
            continue
        w_ = wired_off[ident[1]]
        mine_ = set(w_["all"]) - set(w_["ops"])
        if not mine_ or w_["key"] not in by_key:
            continue
        sent_ = ticket_done.scope_sentence(ident[1], mine_, w_["all"], w_["key"], True).replace(
            " is " + w_["key"], f" is wired by {w_['key']}").replace(" are " + w_["key"], f" are wired by {w_['key']}")
        d_ = (t_["description"] or "").rstrip()
        t_["description"] = (d_ + ("" if not d_ or d_[-1] in ".!?" else ".") + " " + sent_).strip()
    # The build of a screen that needs a person says so (CHG-FXP-004; the wait itself is `notBefore` above).
    for t_ in tasks:
        if t_["type"] != "Task" or t_["key"].startswith("TEST-") or "Waits for its definition:" in (t_["description"] or ""):
            continue
        sids_ = [b_.split(" ", 1)[1] for b_ in ticket_done.builds_of(t_, "", lineage) if b_.startswith("screen ")]
        und_ = [x for x in sids_ if x in screens and ticket_done.define_needed(screens[x])]
        if und_:
            d_ = (t_["description"] or "").rstrip()
            t_["description"] = (d_ + ("" if not d_ or d_[-1] in ".!?" else ".") + " " + ticket_done.define_sentence(
                und_[0], DEFINE_DAY, ticket_done.define_reason(screens[und_[0]]))).strip()

    # **Every task says what finishes it** (CHG-GTR-002, 3 October). op-release.py wrote a done-when into each pointer
    # (CHG-REL-003) while the plan row ADAM indexes, and op-descriptions.py turns into ticket text, had none: after the
    # spec merges of 3 October check-ticket-text found 29 tasks with no Done-when (T-DONE-WHEN). The plan's own
    # "Done when" stays; any other Task gets ticket_done.done_when(), the function op-release.py uses, so the plan
    # row and the pointer say the same thing. Written last, after every edit to the descriptions above, and after a
    # full stop: a setup task's "In the slice: a, b" ended the text, and check-ticket-scope reads that list up to
    # the first full stop (S-SETUP-COUNT read none of them in the first refresh with this rule).
    # A decided sentence a screen's tasks carry comes just before it (block-a-extra-tasks.json `screenNotes`, CHG-RONEP-001:
    # BO-1065's AI residency section is drawn and built in Block A).
    for t_ in tasks:
        m_ = ticket_done.SCREEN.search(t_["key"]) if t_["type"] == "Task" and t_["track"] == "Frontend" else None
        note_ = decided["screenNotes"].get(m_.group(1)) if m_ else None
        if note_ and note_ not in (t_["description"] or ""):
            d_ = (t_["description"] or "").rstrip()
            t_["description"] = (d_ + ("" if not d_ or d_[-1] in ".!?" else ".") + " " + note_).strip()
    for t_ in tasks:
        if t_["type"] == "Task" and not ticket_done.DONE_WHEN.search(t_["description"] or ""):
            d_ = (t_["description"] or "").rstrip()
            if d_ and d_[-1] not in ".!?":
                d_ += "."
            t_["description"] = (d_ + " " + ticket_done.done_when(t_, "", ticket_done.builds_of(t_, "", lineage))).strip()
    COLS = ["sequence", "queue", "key", "parent", "type", "track", "subject", "phase", "wave", "step", "points",
            "assignee", "area", "platform", "service", "dependsOn", "description",
            # the build phase (0 plumbing, 1 foundation, 2 commerce, 3 operations, 4 engagement, 5 reporting)
            "tier",
            # the sprint plan (1 October): its block, who answers for it, AI-engineer days (no points)
            "block", "accountable", "days"]
    # **What is ticketed** (1 October): every row of a block in team.json `sprintPlan.ticketBlocks`, every pushed
    # ticket wherever it is planned, and every block and app-module. plan-tasks.csv holds all of it.
    # **A module test is never its app-module's main builder** (block-test-strategy, 1 October; CHG-R4-005, 6 October).
    # Checked on the final owners, after every other owner is set, with the app-module's tasks (`parent`) as
    # check-plan-owners counts them (tools/ticket_done.py main_builder: the most points, AI work by its days; a tie has
    # no main builder, except AI work, where the AI lead is). Such a test goes to the peer in its stack who built the
    # next most of the app-module (for AI work the other AI engineer), else to the first other person in its stack.
    # A module test already in OpenProject keeps its owner unless block-a-extra-tasks.json `moduleTestPeers` names it
    # with the owner it leaves (the lead moved TEST-AM-AI-ENGINE-A2 from Kalpita Mejari and TEST-AM-APPROVALS-P08-BLOCK-A
    # from Hrushikant Patkar, and kept every other owner); the pushed ones still tested by their main builder are
    # check-plan-owners' known findings (handoff/audit-baseline.json), the lead's call.
    kids_f = defaultdict(list)
    for t_ in tasks:
        if t_["type"] == "Task":
            kids_f[t_["parent"]].append(t_)
    peers_ok = dict(json.loads(EXTRA.read_text(encoding="utf-8")).get("moduleTestPeers") or {}) \
        if EXTRA.exists() else {}
    pools_of = {p_["name"]: set(p_["pools"]) for p_ in people}
    for t_ in [x for x in tasks if x["type"] == "Task"]:
        if not (t_["key"].startswith("TEST-AM-") and t_["assignee"]) or t_["key"] in ai_phase2 \
                or t_["parent"] in ai_phase2:
            continue
        ch_ = [x for x in kids_f[t_["parent"]] if not x["key"].startswith("TEST-")]
        b_ = ticket_done.main_builder(ch_, sp.PLAN_PACE, ai_lead, days_ex)
        if t_["key"] in kmap:
            if peers_ok.get(t_["key"]) != t_["assignee"]:
                continue
        elif not b_ or t_["assignee"] != b_:
            continue
        ai_ = all(x["area"] == "ai" or x["track"] == "AI" for x in ch_)
        pool_ = "ai" if ai_ else (t_.get("pool") or "be")
        stack_ = [n for n, ps in sorted(pools_of.items()) if pool_ in ps and n not in (b_, t_["assignee"])]
        c_ = Counter()
        for x in ch_:
            if x["assignee"] in stack_:
                c_[x["assignee"]] += float(x["points"] or 0) or float(x.get("days") or days_ex.get(x["key"]) or 0)
        peer_ = sorted(c_.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if c_ else (stack_[0] if stack_ else "")
        why_ = f"{b_} built most of it" if b_ == t_["assignee"] else f"the lead moved it from {t_['assignee']}"
        print(f"  module test {t_['key']}: {why_}; {peer_ or 'nobody'} tests it (CHG-R4-005)")
        t_["assignee"] = peer_
    ticket_blocks = set(settings["ticketBlocks"])
    for t_ in tasks:
        t_["ticketed"] = "yes" if (t_["type"] != "Task" or t_["block"] in ticket_blocks or t_["key"] in kmap) else "no"
        if t_["key"] in ai_phase2 and t_["key"] not in kmap:
            t_["ticketed"] = "no"            # phase 2 of the AI engine, its app-modules too (CHG-AIPH-001)
        t_["sprint"] = (sp.sprint_of_index(sched_of[t_["key"]]["start"]) if t_["key"] in sched_of else "")
    # A follows link exists only between two tickets: a ticketed task keeps, in tasks.csv, its waits on ticketed
    # tasks; its waits on work of a block not ticketed yet are in plan-tasks.csv and become links when it is.
    ticketed_keys = {t_["key"] for t_ in tasks if t_["ticketed"] == "yes"}
    with (OUT / "tasks.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(dict(t_, dependsOn=" ".join(d for d in t_["dependsOn"].split() if d in ticketed_keys))
                    for t_ in tasks if t_["ticketed"] == "yes")
    with (OUT / "plan-tasks.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS + ["notBefore", "ticketed", "sprint"], extrasaction="ignore")
        w.writeheader()
        w.writerows(tasks)
    n_t = Counter((t_["block"], t_["ticketed"]) for t_ in tasks if t_["type"] == "Task")
    print("sprint plan: " + "; ".join(
        f"Block {b} {sum(1 for x in tasks if x['type'] == 'Feature' and x['block'] == b)} app-modules, "
        f"{n_t[(b, 'yes')]} tasks ticketed" + (f" + {n_t[(b, 'no')]} planned" if n_t[(b, 'no')] else "")
        for b in sp.BLOCKS))

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
    TAB_HEAD = ["Migration", "Table", "Database", "Columns", "Row-level security", "Partitioned by month",
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
                                                       or (t["area"] == "VM" and t["track"] != "Frontend"))]
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
