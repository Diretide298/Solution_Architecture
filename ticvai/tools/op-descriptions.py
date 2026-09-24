#!/usr/bin/env python3
"""A full task description for every OpenProject ticket, written from the package.

The push gave most tickets one line ("Build X to its contract..."). This writes what a developer needs to start
without opening five files: what to build, the contract or screen details, the tables, who uses it, when it is
done, and where it sits in the plan (build order, week, checker, what it follows, its key).

  backend task / sub-task    per operation: method and path, permission and scope, parameters, request body,
                             responses, tables read and written, routing and offline, the screens that call it
  database task / sub-task   the tables, their source DDL, rollback and row-level security
  frontend task / sub-task   the screen: purpose, module, route and component, states, the operations it calls,
                             where it leads; the sub-task says which of build / connect / tests it is
  epic / feature             its existing summary and what sits under it

Writes handoff/service-docs/op-descriptions.json ({work package id: markdown}), applied on the OpenProject server
by tools/op-descriptions.rb.

  python3 tools/op-descriptions.py --schedule <schedule.json> [--show KEY ...]
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "handoff" / "service-docs"
SCREEN = re.compile(r"([A-Z]+-\d{3})$")
FE_CHECK = ["Chitrangi Mestry", "Chinmay Patkar", "Pallavi Sawant", "Sanket Keluskar", "Pradnya Yeram"]
BE_CHECK = ["Pranay Shinde", "Tanmay Dukhande"]          # Hrushikant is never a checker
PLATFORM = {}


def contract_index():
    ops = {}
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for path, item in (doc.get("paths") or {}).items():
            for method, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (f.relative_to(ROOT).as_posix(), method.upper(), path, op)
    return ops


def ref_name(x):
    return str(x).rsplit("/", 1)[-1]


def schema_text(s):
    if not isinstance(s, dict):
        return ""
    if "$ref" in s:
        return ref_name(s["$ref"])
    if "allOf" in s:
        parts = [schema_text(p) for p in s["allOf"]]
        items = [p for p in s["allOf"] if isinstance(p, dict) and "properties" in p]
        inner = schema_text(((items[0]["properties"].get("items") or {}).get("items")) or {}) if items else ""
        return " + ".join(p for p in parts if p and p != "object") + (f" of {inner}" if inner else "")
    if s.get("type") == "array":
        return f"list of {schema_text(s.get('items') or {})}"
    return s.get("type", "") + (f" ({s['format']})" if s.get("format") else "")


def build(schedule, keys):
    """{key: markdown} for these keys: task keys, and sub-task keys spelled TASK#part. push-openproject.py calls
    this when it creates tickets, so a new ticket gets its full description from the start."""
    rows = {r["key"]: r for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8"))}
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    sched = json.loads(Path(schedule).read_text(encoding="utf-8"))
    week = {k: min(int(v // 5), 6) + 1 for k, v in sched["start"].items()}
    who = sched["assign"]
    ops = contract_index()
    screens = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for s in yaml.safe_load(f.read_text(encoding="utf-8"))["screens"]:
            screens[s["id"]] = dict(s, _platform=f.stem)
    screen_of = {k: m.group(1) for k, r in rows.items()
                 if r["type"] == "Task" and r["track"] == "Frontend" and (m := SCREEN.search(k))}
    callers = collections.defaultdict(set)
    for sid in set(screen_of.values()):
        for api in screens.get(sid, {}).get("apis") or []:
            if api.get("operationId"):
                callers[api["operationId"]].add(sid)
    children = collections.defaultdict(list)
    for k, r in rows.items():
        if r["parent"]:
            children[r["parent"]].append(k)

    def screen_label(sid):
        s = screens.get(sid, {})
        return f"{sid} {s.get('name', '')} ({s.get('_platform', '')[:3]})".strip()

    def op_block(op):
        c = ops.get(op)
        ln = lineage.get(op, {})
        if not c:
            return [f"### `{op}`", f"{ln.get('verb', '')} {ln.get('path', '')} - not found in the contracts; "
                    "check the lineage and raise it with the contract owner."]
        file, method, path, o = c
        out = [f"### `{op}` - `{method} {path}`", ""]
        out.append(o.get("summary", "") + (f". {o['description'].strip()}" if o.get("description") else ""))
        out.append("")
        out.append(f"- **Contract:** `{file}` (operationId `{op}`)")
        perm = o.get("x-ticvai-permission")
        out.append(f"- **Permission:** {perm or 'none named'}" + (f", checked at {o['x-ticvai-scope-level']} level"
                                                                   if o.get("x-ticvai-scope-level") else "")
                   + (f"; audience {', '.join(o['x-ticvai-audience'])}" if o.get("x-ticvai-audience") else ""))
        params = []
        for p in o.get("parameters") or []:
            if "$ref" in p:
                params.append(f"`{ref_name(p['$ref'])}` (shared)")
            else:
                params.append(f"`{p['name']}` ({p.get('in')}{', required' if p.get('required') else ''}"
                              f"{', ' + schema_text(p.get('schema')) if schema_text(p.get('schema')) else ''})")
        if params:
            out.append("- **Parameters:** " + ", ".join(params))
        body = ((o.get("requestBody") or {}).get("content") or {}).get("application/json", {}).get("schema")
        if body:
            out.append(f"- **Request body:** {schema_text(body)}")
        resp = []
        for code, r in (o.get("responses") or {}).items():
            if "$ref" in r:
                resp.append(f"{code} {ref_name(r['$ref'])}")
                continue
            sch = ((r.get("content") or {}).get("application/json") or {}).get("schema")
            resp.append(f"{code} {r.get('description', '')}" + (f" -> {schema_text(sch)}" if sch else ""))
        if resp:
            out.append("- **Responses:** " + "; ".join(resp))
        if ln.get("reads") or ln.get("writes"):
            out.append(f"- **Reads:** {', '.join(ln.get('reads') or []) or 'nothing'}; "
                       f"**writes:** {', '.join(ln.get('writes') or []) or 'nothing'}")
        out.append(f"- **Service:** {ln.get('service', '?')}; reads routed to {o.get('x-ticvai-read-routing', 'primary')}; "
                   f"offline-capable: {'yes' if o.get('x-ticvai-offline-capable') else 'no'}"
                   + (f"; conflicts: {o['x-ticvai-conflict-policy']}" if o.get("x-ticvai-conflict-policy") else ""))
        used = sorted(callers.get(op, ())) or [x for x in o.get("x-ticvai-consumed-by") or []]
        if used:
            out.append("- **Used by:** " + ", ".join(screen_label(s) if s in screens else s for s in used))
        return out

    def plan(key, base):
        r = rows[base]
        wk = week.get(base)
        assignee = who.get(base) or r["assignee"]
        out = ["## In the plan", "",
               f"- Build order #{r['sequence']}" + (f", {assignee}'s queue" if assignee else "")]
        if wk:
            chk = (BE_CHECK[(wk - 1) % 2] if r["track"] in ("Backend", "Database") else FE_CHECK[(wk - 1) % 5])
            out.append(f"- Planned: Block A week {wk}; checker that week: {chk}")
        if r["dependsOn"]:
            out.append("- Follows: " + ", ".join(r["dependsOn"].split()) + " (linked in OpenProject)")
        out.append(f"- Key: `{key}` - Track: {r['track']} - Points: {r['points'] or '-'}")
        return out

    DONE_BE = ["## Done when", "",
               "- [ ] Request, response and every listed error match the contract exactly (contract tests pass)",
               "- [ ] Permission and scope are enforced; tests for 401 and 403",
               "- [ ] Tests for success and for each listed error",
               "- [ ] Reads and writes only the tables listed; row-level security holds",
               "- [ ] Lint and typecheck pass; the PR is reviewed by this week's checker"]
    DONE_DB = ["## Done when", "",
               "- [ ] The migration creates the tables with their keys, indexes and row-level security",
               "- [ ] Its ROLLBACK section undoes it cleanly, tested in CI",
               "- [ ] It runs forward on an empty database and on the previous release's schema",
               "- [ ] Reviewed by this week's backend checker"]
    FE_PART = {"build": ("Build the screen", ["- [ ] Every state is built: loading, empty, error, offline, and the "
                                             "normal view", "- [ ] Runs against the mock API from the generated client",
                                             "- [ ] Matches the design and the navigation below"]),
               "wire": ("Connect the screen to the real API", ["- [ ] Calls the operations below through the "
                                                               "generated client, with its real errors handled",
                                                               "- [ ] Permissions: a user without them sees the "
                                                               "right state, not a failure",
                                                               "- [ ] Done once its backend tasks are merged"]),
               "test": ("Tests for the screen", ["- [ ] Component tests for every state",
                                                "- [ ] Tests for the main flows through the screen",
                                                "- [ ] Lint and typecheck pass"])}

    def screen_block(sid):
        s = screens.get(sid, {})
        impl = s.get("implementation") or {}
        out = [f"### {sid} {s.get('name', '')}", ""]
        if s.get("purpose"):
            out += [str(s["purpose"]).strip(), ""]
        out.append(f"- **Platform:** {s.get('_platform', '')}; module: {s.get('module', '-')}; wave {s.get('wave', '-')}")
        if impl.get("route") or impl.get("component"):
            out.append(f"- **Route:** `{impl.get('route', '-')}`; component `{impl.get('component', '-')}`")
        if s.get("permission"):
            out.append(f"- **Permission:** {s['permission']}")
        st = s.get("states")
        if st:
            names = [x.get("name", x) if isinstance(x, dict) else x for x in (st if isinstance(st, list) else st.keys())]
            out.append("- **States:** " + ", ".join(str(n) for n in names))
        apis = [x["operationId"] for x in s.get("apis") or [] if x.get("operationId")]
        if apis:
            out.append("- **Calls:** " + ", ".join(f"`{x}` ({lineage.get(x, {}).get('verb', '')} "
                                                   f"{lineage.get(x, {}).get('path', '')})" for x in apis))
        nav = (s.get("navigation") or {}).get("exitTo") or []
        if nav:
            out.append("- **Leads to:** " + ", ".join(nav[:12]))
        return out

    out = {}
    for key in keys:
        base, _, part = key.partition("#")
        r = rows[base]
        text = []
        if r["track"] == "Backend" and r["type"] == "Task":
            op_list = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
            text += [("Build this endpoint to its contract." if part else
                      f"Build these {len(op_list)} operations in {r['service']}; each has its own sub-task. "
                      + r["description"]), ""]
            for op in op_list:
                text += op_block(op) + [""]
            text += DONE_BE
        elif r["track"] == "Database" and r["type"] == "Task":
            m = re.search(r"Tables: (.+?)\. Source", r["description"])
            tables = [part] if part else (m.group(1).split(", ") if m else [])
            src = re.search(r"Source DDL: ([^.]+\.sql)", r["description"])
            text += [r["description"], ""]
            if tables:
                text += ["## Tables", ""] + [f"- `{t}`" for t in tables] + [""]
            if src:
                text += [f"Source DDL: `{src.group(1)}`; conventions in `backend/MIGRATIONS.md`.", ""]
            text += DONE_DB
        elif r["track"] == "Frontend" and base in screen_of:
            sid = screen_of[base]
            if part in FE_PART:
                title, checks = FE_PART[part]
                text += [f"{title}: {sid} {screens.get(sid, {}).get('name', '')}. One of three sub-tasks "
                         "(build / connect / tests).", ""]
                text += screen_block(sid) + ["", "## Done when", ""] + checks
            else:
                text += [r["description"], ""] + screen_block(sid) + [
                    "", "Three sub-tasks: build with every state, connect to the API, tests."]
        else:
            text += [r["description"]]
            if children.get(base):
                text += ["", f"Under this: {len(children[base])} "
                         f"{'features' if r['type'] == 'Epic' else 'tasks'}."]
        text += [""] + plan(key, base)
        out[key] = "\n".join(text).strip() + "\n"
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--schedule", required=True)
    ap.add_argument("--show", nargs="*", default=[], help="print these keys' descriptions")
    a = ap.parse_args()
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    texts = build(a.schedule, [k for k in mp if not k.startswith(("_", "VERSION"))])
    out = {str(mp[k]): t for k, t in texts.items()}
    (DOCS / "op-descriptions.json").write_text(json.dumps(out, indent=0, ensure_ascii=False), encoding="utf-8")
    print(f"{len(out)} descriptions written to {DOCS / 'op-descriptions.json'}")
    for k in a.show:
        print(f"\n=========== {k} (#{mp.get(k)}) ===========\n{out.get(str(mp.get(k)), '(no such key)')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
