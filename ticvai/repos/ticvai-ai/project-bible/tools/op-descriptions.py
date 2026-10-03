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

Writes handoff/service-docs/op-descriptions.json ({work package id: markdown}, and {plan key: markdown} for a
ticket not pushed yet), applied on the OpenProject server by tools/op-descriptions.rb (ids only).

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
# Three or four digits: the Block A setup screens of 30 September are BO-1094 to BO-1190.
SCREEN = re.compile(r"([A-Z]+-\d{3,4})$")
# An operations task (SVC-/VM-<service>-<group>-<n>), whose subject lists its operations after the colon.
# Any other backend task (SETUP-HOSTS, PLATFORM-KERNEL, ...) comes from docs/active/block-a-extra-tasks.json
# and carries its own text and Done-when; reading its subject as operations wrote "Build these 0 operations".
OPS_TASK = re.compile(r"(?:SVC|VM)-.+-\d+")
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


def one_line(x):
    """Descriptions are block scalars; a trailing newline split the Responses line in two (audit R085: '; 429')."""
    return " ".join(str(x or "").split())


class MoneyReach:
    """Does an operation's request or response carry Money, through any chain of $refs across the contracts?
    Such an operation resolves currency and scale it does not store (audit R084)."""

    def __init__(self):
        self.docs, self.memo = {}, {}

    def _doc(self, f):
        if f not in self.docs:
            try:
                self.docs[f] = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            except Exception:                  # unreadable or mid-edit: treat it as reaching nothing
                self.docs[f] = {}
        return self.docs[f]

    def _target(self, f, ref):
        file, _, ptr = str(ref).partition("#")
        tf = (f.parent / file).resolve() if file else f
        node = self._doc(tf)
        for part in [x for x in ptr.split("/") if x]:
            node = node.get(part) if isinstance(node, dict) else None
        return tf, ptr, node

    def reaches(self, f, node, seen=None):
        seen = set() if seen is None else seen
        if isinstance(node, list):
            return any(self.reaches(f, x, seen) for x in node)
        if not isinstance(node, dict):
            return False
        if "$ref" in node:
            ref = str(node["$ref"])
            if ref.endswith("/components/schemas/Money"):
                return True
            tf, ptr, target = self._target(f, ref)
            key = (str(tf), ptr)
            if key in self.memo:
                return self.memo[key]
            if key in seen:
                return False
            seen.add(key)
            self.memo[key] = hit = self.reaches(tf, target, seen)
            return hit
        return any(self.reaches(f, v, seen) for k, v in node.items() if k not in ("example", "examples"))


def emits_index():
    """{operationId: {event: [entity from -> to, ...]}} from states/*.yaml, the package's map from an operation to
    the events it publishes through platform.outbox (audit R157)."""
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in sorted((ROOT / "states").glob("*.yaml")):
        if f.name.startswith("_"):
            continue
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        for t in doc.get("transitions") or []:
            if not isinstance(t, dict) or not t.get("operation") or not t.get("emits"):
                continue
            src = t.get("from")
            src = "/".join(map(str, src)) if isinstance(src, list) else str(src)
            for e in t["emits"]:
                out[str(t["operation"])][str(e)].append(f"{doc.get('entity', f.stem)} {src} -> {t.get('to')}")
    return out


# ADR-0025: audience says who may call, permission says what a staff caller must hold. These audiences hold
# permissions; a guest or an anonymous caller never does.
HOLDS_PERMISSION = {"staff", "partner", "public", "service", "device"}
GUEST_RULE = ("a guest caller needs no permission and gets only their own data - a guest token never widens to "
              "another subject (ADR-0025; common.yaml `guestAuth`)")
MONEY_RULE = ("currency and scale are not stored on the row: they resolve from the venue's frozen trading "
              "currency in `platform.venue_settings` (default `platform.region_settings`), except amounts denominated "
              "by their own account, tender or wallet and the five stored-currency tables (ADR-0018 as amended "
              "20 September; naming-and-style 5.1). Read that source even though the list above does not name it")


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
    # **Not capped at week 7** (30 September). A back-end owner whose Block A work runs past 20 November is
    # told so: "week 9" is Block A's tail in B1, and a ticket that said "week 7" would be a promise nobody made.
    week = {k: int(v // 5) + 1 for k, v in sched["start"].items()}
    who = sched["assign"]
    # Each task's timeframe inside its planned week, without dates (asked for 28 September): the week's five
    # days are shared across that developer's tasks for the week by points, in build order. The schedule keeps
    # only the week, so this is the planned pace, not a promise; dates stay out so the text survives a slip.
    slot = {}
    queues = collections.defaultdict(list)
    for k, r in rows.items():
        if r["type"] == "Task" and week.get(k):
            queues[(who.get(k) or r["assignee"], week[k])].append(k)
    for q in queues.values():
        q.sort(key=lambda k: (int(rows[k]["sequence"] or 0), k))
        pts = [max(float(rows[k]["points"] or 0), 0.5) for k in q]
        total, done = sum(pts), 0.0
        for k, p in zip(q, pts):
            start, end = 5 * done / total, 5 * (done + p) / total
            slot[k] = (start, end, len(q))
            done += p
    ops = contract_index()
    slice_ops = set(json.loads((ROOT / "handoff" / "delivery-slice.json").read_text(encoding="utf-8"))["operations"])
    money = MoneyReach()
    emits = emits_index()
    screens = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        sdoc = yaml.safe_load(f.read_text(encoding="utf-8"))
        plat = sdoc.get("platform") if isinstance(sdoc.get("platform"), dict) else {}
        for s in sdoc["screens"]:
            screens[s["id"]] = dict(s, _platform=f.stem, _operator=plat.get("operator"))
    # **A Venue Management screen is built on the backend track** (sprint_plan SCREEN_PREFIX: P08 is VM),
    # and it is still a screen. The 2 October move put seven pushed APP-SETUP-ADM tickets on P08 as `[BE]`
    # rows, and they fell through to the epic branch: a one-line description and no Done-when
    # (T-DONE-WHEN; CHG-GTB-012). A task whose subject opens with its screen id is that screen's ticket.
    screen_of = {k: m.group(1) for k, r in rows.items()
                 if r["type"] == "Task" and (m := SCREEN.search(k))
                 and (r["track"] == "Frontend"
                      or (r["track"] == "Backend" and r.get("area") == "VM"
                          and r["subject"].startswith(f"[BE] {m.group(1)} ")))}
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
        aud = [str(x) for x in o.get("x-ticvai-audience") or []]
        holders = [x for x in aud if x in HOLDS_PERMISSION]
        line = (f"- **Permission:** {perm or 'none named'}"
                + (f" ({', '.join(holders)} callers only)" if perm and holders and len(holders) < len(aud) else "")
                + (f", checked at {o['x-ticvai-scope-level']} level" if o.get("x-ticvai-scope-level") else "")
                + (f"; audience {', '.join(aud)}" if aud else ""))
        if "guest" in aud:
            line += f"; {GUEST_RULE}"
        if "anonymous" in aud:
            line += "; an anonymous caller holds no permission"
        if perm and aud and not holders:
            # Under ADR-0025 nobody in this audience holds the permission; say so rather than build a check
            # no caller can pass (audit R072).
            line += (f". **The contract names {perm} but no caller in this audience holds permissions** - raise it "
                     "with the contract owner before building a permission check")
        out.append(line)
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
            resp.append(f"{code} {one_line(r.get('description'))}" + (f" -> {schema_text(sch)}" if sch else ""))
        if resp:
            out.append("- **Responses:** " + "; ".join(resp))
        # The lineage is approximate (audit R071, R121): derived from returned and request schemas, it misses
        # side-effect, projection and price tables. It is a starting list, not a limit.
        if ln.get("reads") or ln.get("writes"):
            out.append(f"- **Reads (from the lineage, at least):** {', '.join(ln.get('reads') or []) or 'nothing'}; "
                       f"**writes:** {', '.join(ln.get('writes') or []) or 'nothing'}")
        if money.reaches(ROOT / file, {"parameters": o.get("parameters"), "requestBody": o.get("requestBody"),
                                       "responses": o.get("responses")}):
            out.append(f"- **Money:** {MONEY_RULE}")
        if emits.get(op):
            out.append("- **Emits (through `platform.outbox`, in the same transaction):** "
                       + "; ".join(f"`{e}` on {', '.join(sorted(set(ts)))}" for e, ts in sorted(emits[op].items()))
                       + " (from states/*.yaml; the payload is in events/)")
        # Routing only where the operation declares it, and never on a write: defaulting to
        # "primary" contradicted replica-only reporting operations (audit R066).
        routing = o.get("x-ticvai-read-routing") if method == "GET" else None
        out.append(f"- **Service:** {ln.get('service', '?')}"
                   + (f"; reads routed to {routing}" if routing else "")
                   + f"; offline-capable: {'yes' if o.get('x-ticvai-offline-capable') else 'no'}"
                   + (f"; conflicts: {o['x-ticvai-conflict-policy']}" if o.get("x-ticvai-conflict-policy") else ""))
        # Every consumer the contract names, the ones built in this release first (audit R042: the
        # list used to keep only screens with a ticket and drop the rest without a word).
        declared = [str(x) for x in o.get("x-ticvai-consumed-by") or []]
        ticketed = sorted(callers.get(op, ()))
        later = [x for x in declared if not any(sid in x.split() for sid in ticketed)]
        if ticketed or later:
            # **Every one, never "..."** (2 October, CHG-GTB-012): the platform-staff grant put
            # listOwnPlatformStaffGrants on 113 console screens, and a list cut at twelve left 61 out of the
            # ticket (T-USED-BY). Past twelve, the later ones are named by screen id alone.
            if len(later) > 12:
                later = [x.split()[1] if len(x.split()) > 1 and SCREEN.fullmatch(x.split()[1]) else x for x in later]
            out.append("- **Used by:** " + (", ".join(screen_label(x) for x in ticketed) or "no screen in this release")
                       + (f"; later: {', '.join(later)}" if later else ""))
        return out

    def plan(key, base):
        r = rows[base]
        wk = week.get(base)
        assignee = who.get(base) or r["assignee"]
        out = ["## In the plan", "",
               f"- Build order #{r['sequence']}" + (f", {assignee}'s queue" if assignee else "")]
        if wk:
            # Wave is product priority; the week comes from dependency order, so the two can differ
            # without either being wrong (audit R045).
            label = (f"Block A week {wk}" if wk <= 7
                     else f"week {wk}: Block A's tail, running into B1 past 20 November")
            out.append(f"- Planned: {label}" + (f" (product wave {r['wave']}; the week follows dependency order)"
                                                if r.get("wave") else ""))
            if base in slot:
                s0, s1, n = slot[base]
                d0, d1 = int(s0) + 1, max(int(s0) + 1, -(-int(s1 * 100) // 100))
                span = f"day {d0}" if d0 == d1 else f"days {d0}-{d1}"
                size = s1 - s0
                size = ("under half a day" if size < 0.5 else "about half a day" if size < 0.75
                        else "about a day" if size < 1.25 else f"about {round(size * 2) / 2:g} days")
                out.append(f"- Timeframe: {size}, {span} of week {wk}"
                           + (f" ({n} tasks in {assignee}'s week)" if assignee else ""))
            # No reviewer on setup or onboarding tickets, and never the person who built it (R058).
            if r["track"] in ("Backend", "Database", "Frontend") and not base.startswith("SETUP"):
                pool = BE_CHECK if r["track"] in ("Backend", "Database") else FE_CHECK
                first = (wk - 1) % len(pool)
                chk = next((pool[(first + i) % len(pool)] for i in range(len(pool))
                            if pool[(first + i) % len(pool)] != assignee), None)
                if chk:
                    out.append(f"- Reviewer that week: {chk}")
        if r["dependsOn"]:
            out.append("- Follows: " + ", ".join(r["dependsOn"].split()) + " (linked in OpenProject)")
        out.append(f"- Key: `{key}` - Track: {r['track']} - Points: {r['points'] or '-'}")
        return out

    def auth_line(op_ids):
        """The 401/403 checks each operation's own auth model calls for (audit R054): no 403 test on a
        public or permission-less operation, and 'another caller's id' for self-scoped ones."""
        kinds = set()
        for op in op_ids:
            o = (ops.get(op) or (None, None, None, {}))[3]
            aud = [str(x) for x in o.get("x-ticvai-audience") or []]
            if "guest" in aud:
                kinds.add("guest")
            if isinstance(o.get("security"), list) and not o["security"]:
                kinds.add("public")
            elif o.get("x-ticvai-self-scoped"):
                kinds.add("self")
            elif o.get("x-ticvai-permission") and (not aud or any(x in HOLDS_PERMISSION for x in aud)):
                kinds.add("perm")
            else:
                kinds.add("auth")
        parts = []
        if kinds & {"perm", "self", "auth"}:
            parts.append("an unauthenticated call gets 401")
        if "perm" in kinds:
            parts.append("a caller without the permission gets 403" + (" (it applies to staff and partner callers, "
                                                                          "never to a guest)" if "guest" in kinds else ""))
        if "guest" in kinds:
            parts.append("a signed-in guest succeeds without any permission, and another guest's id gets 404 "
                         "(`not-found`: outside the caller's scope)")
        if "self" in kinds:
            parts.append("another caller's id gets 403 on self-scoped operations")
        if "public" in kinds:
            parts.append("public operations need no credential")
        return "- [ ] Access: " + "; ".join(parts) + ", each with a test"

    def done_be(op_ids):
        return ["## Done when", "",
                "- [ ] Request, response and every listed error match the contract exactly (tests assert the "
                "status codes and problem codes the contract lists)",
                auth_line(op_ids),
                "- [ ] Tests for success and for each listed error",
                # Not "only the tables listed": the lineage misses side-effect, projection, currency and price
                # tables, so a hard limit forbade what the contract requires (audit R071, R084, R121).
                "- [ ] Reads and writes at least the tables listed, plus any the contract's described behaviour "
                "needs (the list comes from api-data-lineage.json and can miss side-effect, projection, currency "
                "and price tables); the PR names every table beyond the list; row-level security holds",
                "- [ ] `dotnet build` passes with analyzers and warnings as errors, and `dotnet test` passes; "
                "the PR is reviewed"]

    def done_db(key):
        """Per ticket (audit R046): what the migration must do on the database it will actually meet,
        with nothing about a previous release or a snapshot that do not exist yet."""
        head = ["## Done when", ""]
        if key.endswith("-BASELINE"):
            return head + ["- [ ] Creates the schemas, extensions, helper functions and the migration register",
                           "- [ ] `SqlMigrationRunner` applies it to an empty database, and a second run applies nothing",
                           "- [ ] The PR is reviewed"]
        if key.endswith(("-FOREIGN-KEYS", "-INDEXES")):
            return head + ["- [ ] Applies after every table migration it follows, on a database that has them",
                           "- [ ] Every constraint or index it names exists afterwards; a second run applies nothing",
                           "- [ ] The PR is reviewed"]
        return head + ["- [ ] Creates its tables with their keys, indexes and row-level security",
                       "- [ ] Applies on a database with its Follows migrations applied, and a second run applies nothing",
                       "- [ ] The PR is reviewed"]
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

    def purpose_of(s):
        """The screen's purpose, whole. Three authored purposes were cut at 200 characters mid-word while the
        full sentence survives in notes (audit R067): finish the sentence from notes when that happens."""
        p = str(s.get("purpose") or "").strip()
        notes = str(s.get("notes") or "").strip()
        if p and not re.search(r"[.!?)\"'*`]$", p) and notes.startswith(p) and len(notes) > len(p):
            m = re.search(r"[.!?](?=\s|$)", notes[len(p):])
            p = notes[:len(p) + m.end()] if m else notes.split("\n\n", 1)[0]
        return p

    def guest_screen(sid):
        return screens.get(sid, {}).get("_operator") == "guest"

    def screen_block(sid):
        s = screens.get(sid, {})
        impl = s.get("implementation") or {}
        out = [f"### {sid} {s.get('name', '')}", ""]
        if s.get("purpose"):
            out += [purpose_of(s), ""]
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
        now = [x for x in apis if x in slice_ops]
        later = [x for x in apis if x not in slice_ops]

        def call(x):
            return f"`{x}` ({lineage.get(x, {}).get('verb', '')} {lineage.get(x, {}).get('path', '')})"

        # Built now versus later, so a ticket titled with two operations is not read as five (audit R047).
        if now:
            out.append("- **Calls, built in this ticket:** " + ", ".join(call(x) for x in now))
        if later:
            out.append("- **Calls, later (not in this release):** " + ", ".join(f"`{x}`" for x in later)
                       + ". Render their states from what this ticket does build; do not stub a backend for them.")
        nav = (s.get("navigation") or {}).get("exitTo") or []
        if nav:
            out.append("- **Leads to:** " + ", ".join(nav[:12]))
        return out

    def screen_done(sid):
        """What 'done' means for this screen, from the screen itself (audit R041): each state it declares,
        each transition's trigger and failure, and each in-release call's errors."""
        s = screens.get(sid, {})
        out = ["## Done when", ""]
        st = s.get("states")
        if isinstance(st, dict):
            for name, text in st.items():
                if name == "emptyNoAccess" and guest_screen(sid):
                    # A guest holds no permission (ADR-0025), so there is none to name (audit R072).
                    out.append("- [ ] State **emptyNoAccess**: not reachable on a guest screen - a guest caller holds "
                               "no permission (ADR-0025)")
                    continue
                first = re.split(r"(?<=[.!?])\s", re.sub(r"\*\*", "", str(text)).strip(), maxsplit=1)[0]
                out.append(f"- [ ] State **{name}**: {first}")
        for t in ((s.get("navigation") or {}).get("transitions") or [])[:8]:
            fails = ", ".join(f"{f.get('when')} -> {f.get('to')}" for f in t.get("onFailure") or [] if isinstance(f, dict))
            out.append(f"- [ ] {t.get('trigger', 'Transition')} leads to {t.get('to')}"
                       + (f" (only when {t['precondition']})" if t.get("precondition") else "")
                       + (f"; on failure: {fails}" if fails else ""))
        for x in [a["operationId"] for a in s.get("apis") or [] if a.get("operationId") in slice_ops][:8]:
            o = (ops.get(x) or (None, None, None, {}))[3]
            errs = [str(c) for c in (o.get("responses") or {}) if str(c)[:1] in "45"]
            if errs:
                out.append(f"- [ ] `{x}`: each of its errors ({', '.join(errs)}) shows the screen's error state, not a crash")
        out.append("- [ ] `pnpm lint`, `pnpm typecheck` and `pnpm test` pass")
        return out

    out = {}
    for key in keys:
        base, _, part = key.partition("#")
        if base not in rows:
            # Out of the plan since it was pushed (a decision deferred, merged or regrouped it). op-retire.py
            # moves those tickets; rewriting them here would describe work nobody is going to do.
            continue
        r = rows[base]
        text = []
        if r["track"] == "Backend" and r["type"] == "Task" and OPS_TASK.fullmatch(base) and base not in screen_of:
            op_list = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
            text += [("Build this endpoint to its contract." if part else
                      f"Build {'this operation' if len(op_list) == 1 else f'these {len(op_list)} operations'} "
                      f"in {r['service']}. " + r["description"]), ""]
            for op in op_list:
                text += op_block(op) + [""]
            text += done_be(op_list)
        elif r["track"] == "Database" and r["type"] == "Task":
            m = re.search(r"Tables: (.+?)\. Source", r["description"])
            tables = [part] if part else (m.group(1).split(", ") if m else [])
            src = re.search(r"Source DDL: ([^.]+\.sql)", r["description"])
            text += [r["description"], ""]
            if tables:
                text += ["## Tables", ""] + [f"- `{t}`" for t in tables] + [""]
            if src:
                # The generated order lives in handoff/service-docs/backend/MIGRATIONS.md; the older
                # backend/MIGRATIONS.md numbers files differently (audit R048, R051).
                text += [f"Source DDL: `{src.group(1)}`; order and numbering in "
                         "`handoff/service-docs/backend/MIGRATIONS.md`.", ""]
            text += done_db(base)
        elif base in screen_of:
            sid = screen_of[base]
            if part in FE_PART:
                title, checks = FE_PART[part]
                if part == "wire" and guest_screen(sid):
                    checks = [c if "Permissions:" not in c else
                              "- [ ] No staff permission applies on a guest screen (ADR-0025): the signed-in guest "
                              "sees only their own data"
                              for c in checks]
                text += [f"{title}: {sid} {screens.get(sid, {}).get('name', '')}. One of three sub-tasks "
                         "(build / connect / tests).", ""]
                text += screen_block(sid) + ["", "## Done when", ""] + checks
            else:
                text += [r["description"], ""] + screen_block(sid) + [""] + screen_done(sid) + [
                    "", "Sub-tasks: build (every state), connect (the real API), tests."]
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
    # **Every plan ticket, pushed or not** (fresh start, Chinmay, 3 October, CHG-GTR-001). A pushed ticket is keyed by
    # its OpenProject id, as op-descriptions.rb applies it; a ticket not pushed yet by its plan key. With r1 going into
    # a new project pms-map.json is empty, and keying by id alone wrote {} -- check-ticket-text, check-ddl-conventions
    # and check-starter-fit read this file, and every one of them would have passed on nothing.
    plan = [r["key"] for r in csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8"))]
    keys = [k for k in mp if not k.startswith(("_", "VERSION"))]
    keys += [k for k in plan if k not in mp]
    texts = build(a.schedule, keys)
    out = {str(mp[k]) if k in mp else k: t for k, t in texts.items()}
    (DOCS / "op-descriptions.json").write_text(json.dumps(out, indent=0, ensure_ascii=False), encoding="utf-8")
    print(f"{len(out)} descriptions written to {DOCS / 'op-descriptions.json'}")
    for k in a.show:
        print(f"\n=========== {k} (#{mp.get(k)}) ===========\n{out.get(str(mp.get(k)), '(no such key)')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
