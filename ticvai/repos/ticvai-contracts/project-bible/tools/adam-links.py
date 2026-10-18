#!/usr/bin/env python3
"""What each OpenProject ticket touches, for ADAM: the rows `adam_pull` reads to fill a ticket's folder.

ADAM keeps its ticket-to-artefact links in its own table (artefact_link on the ADAM server), not in OpenProject,
so tickets pushed straight into OpenProject arrive with none and every pull says "nothing is linked". This builds
them from the package:

  backend task or sub-task   its operations (contract#operationId), its service, the tables they read or write,
                             and the screens in this plan that call them
  database task / sub-task   its tables
  frontend task / sub-task   its screen and the operations the screen calls
  app-module feature         what its Builds list: its screens and the operations they call (CHG-TKT-004)
  a task building none       the files its description names and, for setup work, the setup standards (CHG-TKT-005)
  service epic or feature    its service

Writes handoff/service-docs/adam-links.json, loaded on the ADAM server by viewer/api/load_links.py. With
TICVAI_OP_TOKEN set it also reads each ticket's subject, status, type and assignee from OpenProject, the cached
columns ADAM shows on a board (a copy, labelled as one; OpenProject stays the truth). The gate reads the same
columns, offline, to fail a baselined finding once a ticket building it has started (tools/audit_guard.py,
CHG-CRF-001), so they carry when they were read (`statusReadAt`), and a run without the token keeps the last file's
columns rather than dropping them.

  python3 tools/adam-links.py                  # links from the package; ticket columns read or carried
  python3 tools/adam-links.py --status-only    # ticket columns read again, links untouched (TICVAI_OP_TOKEN)
"""
from __future__ import annotations

import base64
import collections
import csv
import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
PMS = "https://pms.softlabsgroup.in"
PROJECT = 153
sys.path.insert(0, str(ROOT / "tools"))
import ticket_done  # noqa: E402  (what a ticket builds: shared with op-release.py and build-service-docs.py)

# A screen task's key ends in its screen id, three or four digits, "-REST" on the rest of a setup screen (CHG-RONEP-003:
# the three-digit pattern gave BO-1065 and the other four-digit setup screens no links at all).
SCREEN = ticket_done.SCREEN
SLICE = re.compile(r"In the slice: ([A-Za-z0-9, ]+?)(?:\)|\.|;|$)")
REST_OF = re.compile(r"Block A built only its setup operations \(([A-Za-z0-9, ]+?)\)")


def snapshot(token):
    """Subject, status, type and assignee of every work package in the project: three paged reads."""
    auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()
    flt = urllib.parse.quote(json.dumps([{"status": {"operator": "*", "values": []}}]))
    out, off = {}, 1
    while True:
        req = urllib.request.Request(f"{PMS}/api/v3/projects/{PROJECT}/work_packages?pageSize=1000&offset={off}"
                                     f"&filters={flt}", headers={"Authorization": auth, "User-Agent": "curl/8.0"})
        d = json.load(urllib.request.urlopen(req, timeout=600))
        for e in d["_embedded"]["elements"]:
            ln = e["_links"]
            out[e["id"]] = {"subject": e["subject"], "status": ln["status"]["title"], "type": ln["type"]["title"],
                            "assignee": (ln.get("assignee") or {}).get("title") or ""}
        if len(out) >= d["total"] or not d["_embedded"]["elements"]:
            return out
        off += 1


COLUMNS = ("subject", "status", "type", "assignee")


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def carried_status(previous: dict) -> tuple:
    """The cached columns of an earlier adam-links.json by work package id, and when they were read (CHG-CRF-001).
    A run without TICVAI_OP_TOKEN keeps them, so the gate's started-ticket rule never loses them silently."""
    snap = {}
    for ln in (previous or {}).get("links") or []:
        if not ln.get("status"):
            continue
        try:
            wp = int(ln.get("key"))
        except (TypeError, ValueError):
            continue
        snap.setdefault(wp, {k: ln.get(k) or "" for k in COLUMNS})
    read_at = ((previous or {}).get("statusReadAt") or "") if snap else ""
    return snap, read_at


def status_source(token: str, previous: dict) -> tuple:
    """(cached columns by work package id, when they were read, how) for this run: OpenProject when the token is
    set, else the last file's."""
    if token:
        return snapshot(token), _now(), "read from OpenProject"
    snap, read_at = carried_status(previous)
    if snap:
        return snap, read_at, (f"carried from the last adam-links.json, read {read_at or 'at an earlier release'} "
                               f"(no TICVAI_OP_TOKEN)")
    return {}, "", "none (no TICVAI_OP_TOKEN and no earlier file)"


def restatus(doc: dict, snap: dict, read_at: str) -> dict:
    """`doc` with each link's cached columns taken from `snap`; which tickets link what is left as it is."""
    links = []
    for ln in doc.get("links") or []:
        row = {k: v for k, v in ln.items() if k not in COLUMNS}
        try:
            row.update(snap.get(int(ln.get("key")), {}))
        except (TypeError, ValueError):
            pass
        links.append(row)
    out = {k: v for k, v in doc.items() if k not in ("cached", "statusReadAt", "links")}
    out.update({"cached": bool(snap), "statusReadAt": read_at if snap else "", "links": links})
    return out


def status_only() -> int:
    """Read every ticket's status again and rewrite only the cached columns of adam-links.json (CHG-CRF-001): before
    a gate between releases, so the started-ticket rule judges today's statuses. Never writes on a failed read."""
    path = DOCS / "adam-links.json"
    token = os.environ.get("TICVAI_OP_TOKEN", "")
    if not token:
        print("adam-links --status-only: TICVAI_OP_TOKEN is not set; nothing read, nothing written")
        return 2
    if not path.exists():
        print(f"adam-links --status-only: {path} is missing; run tools/adam-links.py first")
        return 2
    try:
        snap = snapshot(token)
    except Exception as e:  # network, HTTP or JSON: say so and keep the file
        print(f"adam-links --status-only: OpenProject could not be read ({e.__class__.__name__}: {e}); "
              f"adam-links.json left as it was")
        return 2
    if not snap:
        print("adam-links --status-only: OpenProject returned no work packages; adam-links.json left as it was")
        return 2
    doc = json.loads(path.read_text(encoding="utf-8"))
    before = {(ln.get("key"), ln.get("kind"), ln.get("id")): ln.get("status") for ln in doc.get("links") or []}
    out = restatus(doc, snap, _now())
    moved = sum(1 for ln in out["links"]
                if before.get((ln.get("key"), ln.get("kind"), ln.get("id"))) != ln.get("status"))
    path.write_text(json.dumps(out, indent=0), encoding="utf-8")
    print(f"ticket status read for {len(snap)} work packages at {out['statusReadAt']}; {moved} of "
          f"{len(out['links'])} link rows changed status; which tickets link what is unchanged")
    return 0


def main() -> int:
    if "--status-only" in sys.argv[1:]:
        return status_only()
    rows = {r["key"]: r for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8"))}
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))

    screens = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            screens[s["id"]] = s
    ticket_done.merge_bindings(screens)     # a merged screen's operations are built on its target (CHG-FXP-002)
    screen_ops = {sid: [a["operationId"] for a in s.get("apis") or [] if a.get("operationId")]
                  for sid, s in screens.items()}
    known = package_index(screens)
    touches = touches_from(rows, lineage, screen_ops, known)
    path = DOCS / "adam-links.json"
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    snap, read_at, how = status_source(os.environ.get("TICVAI_OP_TOKEN", ""), previous)
    links, per_kind, bare, bare_keys = [], collections.Counter(), 0, []
    for key, wp in mp.items():
        if key.startswith(("_", "VERSION")):
            continue
        seen = set()
        got = [t for t in touches(key) if not (t in seen or seen.add(t))]
        bare += not got
        if not got and "#" not in key and key in rows:
            bare_keys.append(key)
        for kind, target in got:
            per_kind[kind] += 1
            links.append({"key": str(wp), "kind": kind, "id": target, "url": f"{PMS}/work_packages/{wp}",
                          **snap.get(wp, {})})
    out = {"project": "ticvai", "openproject": PMS, "cached": bool(snap), "statusReadAt": read_at if snap else "",
           "links": links}
    path.write_text(json.dumps(out, indent=0), encoding="utf-8")
    tickets = len([k for k in mp if not k.startswith(("_", "VERSION"))])
    print(f"{len(links)} links for {tickets - bare} of {tickets} tickets ({bare} with nothing to link: out of the "
          f"plan or sub-tasks of such); {dict(per_kind)}; cached columns: {how}")
    print(f"repointed to a table's name now: {sum(known['repointed'].values())} link(s) "
          f"({', '.join(f'{a} -> {b}' for a, b in sorted(known['repointed'])[:8])}); dropped as not in the package: "
          f"{sum(known['dropped'].values())} ({', '.join(f'{k} {i}' for k, i in sorted(known['dropped'])[:12])})")
    if bare_keys:
        print(f"planned tickets with nothing to link: {len(bare_keys)} ({', '.join(sorted(bare_keys)[:12])})")
    return 0


# **Every link resolves, and every ticket links something** (14 October 2026, CHG-TKT-004, CHG-TKT-005, CHG-TKT-006;
# the Block A pull of 14 October: 123 features and 29 tasks reached developers with nothing linked, and 55 tickets
# carried links ADAM could not find). A table a declared rename or move retired (tools/derive-schema-history.py
# RENAMES: catalogue.inventory_hold is catalogue.inventory_reservation) is linked under its name now; an id that is no
# operation, table or screen of the package (a pushed sub-task's part "SETUP-HOSTS#commerce", a lineage view such as
# platform.sale_board_for_catalogue, platform.schema_version, which the migration runner owns) is dropped, never
# linked. An ADR a ticket builds is linked as its file too, because ADAM pulls files and not decisions; and a task
# that builds no operation, table or screen links the package files its description names (a contract, a doc, a
# setup standard) and, for a setup, DevOps or onboarding task, the setup standards it is built to
# (repos/ticvai-docs/setup/, project-bible/setup/ in every repository). ADAM serves `file` links through adam_file
# (viewer/mcp/tools.mjs lookupFor, same change).
SETUP_DOCS = "repos/ticvai-docs/setup"
FILE_REF = re.compile(r"(?<![\w/.-])((?:contracts|docs|handoff|screens|flows|states|events|setup|backend|"
                      r"repos/ticvai-docs)/[\w./-]+\.(?:ya?ml|md|json|csv|sql))")
STARTER = {"Onboarding": ["README.md", "quickstart.md"], "DevOps": ["README.md", "dependencies.md"],
           "Setup": ["README.md", "dependencies.md"]}


def package_index(screens: dict) -> dict:
    """What ADAM can resolve: operations (contract#operationId), tables (the schema reference, the names ADAM's
    adam_table knows), screens, ADR files; and the table renames, chains followed."""
    ops = set()
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        for item in ((d or {}).get("paths") or {}).values() if isinstance(d, dict) else []:
            for op in (item or {}).values() if isinstance(item, dict) else []:
                if isinstance(op, dict) and op.get("operationId"):
                    ops.add(f"{f.stem}#{op['operationId']}")
    ref = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    renames = {}
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("derive_schema_history", ROOT / "tools" / "derive-schema-history.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        step = {r["from"]: r["to"] for r in mod.RENAMES}
    except Exception:                            # noqa: BLE001 -- no history: nothing was renamed
        step = {}
    for a in step:
        b, seen = step[a], {a}
        while b in step and b not in seen:
            seen.add(b)
            b = step[b]
        renames[a] = b
    adrs = {}
    for f in sorted((ROOT / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")):
        adrs.setdefault(f"ADR-{f.name[:4]}", f.relative_to(ROOT).as_posix())
    return {"ops": ops, "tables": set(ref.get("cols") or {}), "renames": renames, "screens": set(screens),
            "adrs": adrs, "repointed": collections.Counter(), "dropped": collections.Counter()}


def resolve(t, known):
    """(kind, id) as ADAM can find it, or None to drop it (counted in `known`)."""
    kind, target = t
    if known is None:
        return t
    if kind == "table":
        now = known["renames"].get(target, target)
        if now != target:
            known["repointed"][(target, now)] += 1
        target = now
        ok = target in known["tables"]
    elif kind == "operation":
        ok = target in known["ops"]
    elif kind == "screen":
        ok = target in known["screens"]
    elif kind == "file":
        ok = (ROOT / target).is_file()
    else:
        ok = True
    if not ok:
        known["dropped"][(kind, target)] += 1
        return None
    return kind, target


def touches_from(rows, lineage, screen_ops, known=None):
    """key -> [(kind, id)] for a ticket (a task, or "TASK#part" a sub-task). Imported by tools/check-ticket-builds.py.
    With `known` (package_index) every link is resolved: repointed to a table's name now, or dropped."""
    inner = _touches_from(rows, lineage, screen_ops, known)
    kids = collections.defaultdict(list)
    for k_, r_ in rows.items():
        if r_.get("type") == "Task" and r_.get("parent"):
            kids[r_["parent"]].append(k_)

    def touches(key):
        out = [x for x in (resolve(t, known) for t in inner(key)) if x]
        r = rows.get(key.partition("#")[0])
        if known is None or not r or "#" in key:
            return out
        # a feature whose Builds name nothing (its tasks are hand-written: the foundation, the AI engine) links what
        # its tasks link, as a feature with screens links what they call: CHG-TKT-004
        if r["type"] == "Feature" and not any(k in ("operation", "table", "screen") for k, _ in out):
            for c in kids.get(r["key"], []):
                out += [x for x in touches(c) if x not in out and x[0] != "service"]
        # an ADR is pulled as its file (ADAM pulls files, not decisions): CHG-TKT-005
        out += [("file", known["adrs"][i]) for k, i in out if k == "adr" and i in known["adrs"]
                and ("file", known["adrs"][i]) not in out]
        if r["type"] == "Task" and not any(k in ("operation", "table", "screen") for k, _ in out):
            named = []
            for p in FILE_REF.findall(r.get("description") or ""):
                p = p.rstrip(".")
                if p.startswith("setup/"):
                    p = f"{SETUP_DOCS}/{p[len('setup/'):]}"
                named.append(p)
            named += [f"{SETUP_DOCS}/{n}" for n in STARTER.get(r.get("track") or "", [])]
            out += [x for x in (resolve(("file", p), known) for p in named) if x]
        return out

    return touches


def _touches_from(rows, lineage, screen_ops, known=None):
    screen_of = {k: m.group(1) for k, r in rows.items()
                 if r["type"] == "Task" and r["track"] == "Frontend" and (m := SCREEN.search(k))}
    planned = set(screen_of.values())
    callers = collections.defaultdict(set)          # operation -> screens in this plan that call it
    for sid in planned:
        for op in screen_ops.get(sid, []):
            callers[op].add(sid)

    def op_id(op):
        c = lineage.get(op, {}).get("contract")
        return f"{c}#{op}" if c else op

    def backend(ops):
        out = []
        for op in ops:
            ln = lineage.get(op, {})
            out.append(("operation", op_id(op)))
            if ln.get("service"):
                out.append(("service", ln["service"]))
            # `cache:idempotency` and the like are Redis keys, not tables adam_table can find
            out += [("table", t) for t in ln.get("reads", []) + ln.get("writes", []) if ":" not in t]
            out += [("screen", s) for s in sorted(callers.get(op, ()))]
        return out

    def listed(rx, text):
        m = rx.search(text or "")
        return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else None

    def touches(key):
        base, _, part = key.partition("#")
        if base not in rows:  # out of the plan (tools/op-retire.py closes or parks it): nothing to link
            return []
        r = rows[base]
        if r["track"] == "Frontend" and base in screen_of:
            sid, ops = screen_of[base], list(screen_ops.get(screen_of[base], []))
            # **A setup ticket links only its slice's operations, the rest-of-the-screen ticket the others**
            # (r1 gate G4, CHG-RONEP-003): APP-SETUP-BO-1162 said "2 of its 6 operations" and linked all 6.
            if base.startswith("APP-SETUP-") and not base.endswith("-REST"):
                sl = listed(SLICE, r["description"])
                ops = [o for o in ops if o in sl] if sl is not None else ops
            elif base.endswith("-REST"):
                done = listed(REST_OF, r["description"]) or []
                ops = [o for o in ops if o not in done]
            return [("screen", sid)] + [("operation", op_id(op)) for op in ops]
        if r["type"] == "Feature":
            # an app-module links what its Builds list: its screens and the operations they call, or for an API-only
            # one its operations and tables (CHG-TKT-004): before, it linked nothing, and an agent read the back-end
            # tasks' operations as its scope (#27741)
            return [tuple(b.split(" ", 1)) for b in ticket_done.builds_of(r, part, lineage) if " " in b]
        out = []
        for b in ticket_done.builds_of(r, part, lineage):
            kind, _, name = b.partition(" ")
            if kind == "operation":
                out += backend([name.split("#")[-1]])
            else:
                out.append((kind, name))
        return out

    return touches


if __name__ == "__main__":
    sys.exit(main())
