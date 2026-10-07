#!/usr/bin/env python3
"""What finishes a ticket, written once for the plan and the pointer (CHG-GTR-002, 3 October).

`tools/op-release.py` wrote a done-when into every OpenProject pointer (CHG-REL-003), but the plan row in
handoff/service-docs/tasks.csv -- what ADAM indexes and op-descriptions.py turns into ticket text -- still had
none, and after the spec merges of 3 October check-ticket-text failed on 135 tickets (T-DONE-WHEN): 29 tasks
and 106 Block C and D app-modules ticketed at feature level, whose "Complete when" is no done-when. The two had to agree, so the logic lives
here and both import it: build-service-docs.py writes `done_when()` into every Task description that has no
"Done when" of its own, and op-release.py then reads it back from the description, the same words.

Imported, no main.
"""
from __future__ import annotations

import re

# A screen task's key ends in its screen id: three or four digits (the Block A setup screens are BO-1094 to BO-1190),
# and "-REST" on the task that builds the rest of a screen whose setup operations Block A built (CHG-GTR-002).
SCREEN = re.compile(r"([A-Z]+-\d{3,4})(?:-REST)?$")
# A Venue Management screen is built on the backend track (P08 is VM) and is still a screen: "[BE] ADM-247 ...".
BE_SCREEN = re.compile(r"^\[BE\] ([A-Z]+-\d{3,4}) ")
# **A ticket written by hand names what it builds** (CHG-RONEP-001/003, 3 October): the tasks of block-a-extra-tasks.json
# (`operations` an AI engine task serves, `builds` any task lists) and the module tests (their app-module's artefacts)
# lead their text with "Builds: `operation ai#setAiProvider`, `table platform.outbox`, `adr ADR-0058`." Before it,
# a hand-written backend task's title was read as an operation list: PLATFORM-SAGA-PAID built "operation the saga
# proven end to end" and OFFLINE-JOURNAL "operation record" (r1 gate, G2).
BUILDS = re.compile(r"Builds: ((?:`[^`]+`(?:, )?)+)")
OP_ID = re.compile(r"^[a-z][A-Za-z0-9]+$")


def listed_builds(text):
    """The artefacts a "Builds:" lead names, as written ("operation ai#x", "table s.t", "screen S", "adr ADR-0058")."""
    m = BUILDS.search(text or "")
    return re.findall(r"`([^`]+)`", m.group(1)) if m else []


def builds_of(r, part, lineage):
    """The artefact ids a ticket builds, as ADAM names them: operation contract#operationId, table schema.name,
    screen id, service, ADR. A task whose text leads with "Builds:" builds what it lists (a hand-written task, a
    module test); setup and onboarding tasks build nothing ADAM indexes by id: their key is enough."""
    def op_id(op):
        c = lineage.get(op, {}).get("contract")
        return f"{c}#{op}" if c else op

    if r["type"] == "Task" and not part and listed_builds(r.get("description")):
        out = []
        for b in listed_builds(r.get("description")):
            kind, _, name = b.partition(" ")
            out.append(f"operation {op_id(name)}" if kind == "operation" and "#" not in name else b)
        return out
    if r["type"] == "Task" and r["track"] == "Backend" and part in ("", "build", "wire", "test"):
        m, k = BE_SCREEN.match(r["subject"] or ""), SCREEN.search(r["key"])
        if m and k and k.group(1) == m.group(1):
            return [f"screen {m.group(1)}"]
    if r["type"] == "Task" and r["track"] == "Backend":
        ops = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
        # only a generated operations task (SVC-, VM-) lists operations in its title; a hand-written one lists none
        if not part and not r["key"].startswith(("SVC-", "VM-")):
            return []
        return [f"operation {op_id(op)}" for op in ops if OP_ID.match(op)]
    if r["type"] == "Task" and r["track"] == "Database":
        if part:
            return [f"table {part}"]
        m = re.search(r"Tables: (.+?)\. Source", r["description"])
        return [f"table {t}" for t in (m.group(1).split(", ") if m else [])]
    if r["type"] == "Task" and r["track"] == "Frontend":
        m = SCREEN.search(r["key"])
        return [f"screen {m.group(1)}"] if m else []
    if r["type"] in ("Epic", "Feature") and r.get("service"):
        return [f"service {r['service']}"]
    return []


DONE_WHEN = re.compile(r"Done when[:,]?\s*(.+)", re.S | re.I)


def done_when(r, part, builds):
    """What finishes this ticket, as one line every pointer carries (CHG-REL-003). The plan's own "Done when" when the
    task has one; otherwise the test strategy's (docs/active/block-test-strategy.md) for its kind, naming what it
    builds. Before 3 October the pointer said the done-when lived in ADAM, which serves contracts, screens and
    tables but no task's done-when, so most tickets reached developers with none."""
    m = DONE_WHEN.search(r.get("description") or "")
    if m and not part:
        return "Done when " + " ".join(m.group(1).split())   # whole: a 700-character cut ended 11 pointers mid-word (CHG-RFM-016)
    names = [b.split(" ", 1)[1] for b in builds]
    named = ", ".join(f"`{n}`" for n in names[:8]) + (f" and {len(names) - 8} more" if len(names) > 8 else "")
    kind, typ = r.get("track"), r.get("type")
    # what it builds decides the words, not the track: a Venue Management screen is on the backend track
    if names and all(b.startswith("screen ") for b in builds):
        kind = "Frontend"
    if typ == "Epic":
        return ("Done when every app-module in the block is done, every flow the block claims passes end to end on the "
                "integration environment, and the client has run its acceptance session (block-test-strategy).")
    if typ == "Feature":
        return ("Done when every ticket under it is done and its module test passes on the integration environment with "
                "no open severity 1 or 2 defect (block-test-strategy).")
    if kind == "Backend" and names:
        return (f"Done when {named} pass their contract tests against the contract in ADAM, including every documented "
                "error response; each reads and writes only the tables its spec lists, under row-level security; unit "
                "tests cover its rules; and a peer in the same stack has reviewed and tested it.")
    if kind == "Database" and names:
        return (f"Done when the migration for {named} runs forward on an empty database and on the previous release's "
                "schema, every table matches its spec in ADAM (columns, keys, indexes, row-level security), and a peer "
                "has reviewed it.")
    if kind == "Frontend" and names:
        step = {"build": "the layout is built from the screen spec (and its wireframe once client-verified)",
                "wire": "every bound operation is called as the screen spec says, with its loading, empty and error states",
                "test": "a component or interaction test covers every state, navigation link and permission"}.get(part)
        if step:
            return f"Done when, for {named}: {step}."
        if scope_of(r):    # a split screen: its part, not the whole screen (CHG-FXP-001)
            return (f"Done when {named} reaches every state its spec lists for the operations in its scope, every "
                    "navigation link it owns works, an allowed and a refused user see what its permissions say, and it "
                    "calls only the operations its scope names (block-test-strategy).")
        return (f"Done when {named} reaches every state its spec lists, every navigation link works, an allowed and a "
                "refused user see what its permissions say, and it calls only its bound operations (block-test-strategy).")
    if kind == "Test":
        return ("Done when every flow the block claims passes end to end on the integration environment, every defect "
                "found is triaged with no open severity 1 or 2 defect, and the lead has signed the block test off "
                "(block-test-strategy).")
    if kind == "AI":
        return ("Done when the capability answers through the AI gateway with the scrubber and the guard on, its "
                "evaluation set passes the gate of docs/architecture/ai-system-design.md 3.5, it degrades as 3.7 says "
                "when its provider is down, and a peer AI engineer has reviewed it.")
    return ("Done when the work in the description above is built, tested and reviewed by a peer in the same stack "
            "(block-test-strategy).")


# ---- what a ticket may be planned to build (CHG-FXP-001 to -004, 4 October) -------------------------------------
# The Sprint 1-2 judging (4 October) found tickets planned for work the spec says must not be built: screens merged
# into another (BO-669 into BO-666), operations whose contract says "the shape below is a proposal ... want confirming
# before anything is built against them" (getMarketingSubscription), a deprecated operation (claimTableSession), and
# screens whose spec says "it needs a person before it is built". The rules live here so the plan
# (build-service-docs.py), the retirements (op-retire.py) and the check (check-ticket-builds.py) read them alike.

MERGED_NOTE = re.compile(r"\*\*Merged into ([A-Z]+-\d{3,4})\b")
STUB_TEXT = "The shape below is a proposal"
NEEDS_PERSON = "needs a person before it is built"


def operation_hold(op: dict):
    """Why an operation (its contract YAML node) is not put on a build ticket, or None. Provisional (the flag),
    a stub whose shape is a proposal (the text; CHG-FXP-003), or deprecated with a replacement (CHG-FXP-003)."""
    if op.get("x-ticvai-provisional"):
        return "provisional"
    if STUB_TEXT in (op.get("description") or ""):
        return "stub"
    if op.get("deprecated"):
        return "deprecated"
    return None


def screen_hold(s: dict, listed: dict | None = None):
    """(kind, into, why) when a screen gets no build task of its own, else None.

      merged    its notes lead with "**Merged into X**": X's ticket builds it (CHG-FXP-002)
      listed    block-a-extra-tasks.json `screensNotBuilt` names it (a replaced page, or a screen a person could not
                define: moved out of Block A), with `kind`, `into` and `why`
    An entry with `"part": "rest"` holds only the rest of a setup screen (rest_held): its setup part is still built.
    A screen that only needs a person is not held here: it is built after its definition (define_needed)."""
    entry = (listed or {}).get(s.get("id"))
    if entry and entry.get("part") != "rest":
        return entry.get("kind") or "listed", entry.get("into") or "", entry.get("why") or ""
    m = MERGED_NOTE.search(str(s.get("notes") or ""))
    if m:
        return "merged", m.group(1), f"merged into {m.group(1)}"
    return None


# **The same test as check-screen-patterns NP** (4 October, CHG-RFM-008): the plan waited on one phrase and on day 5,
# the check failed any Sprint 1-2 screen with any of three phrases or binding nothing, so the merged plan pulled twelve
# undefined Block B screens into Sprint 2 that the check then failed. Both read screen_patterns now.
try:
    from screen_patterns import NEEDS_PERSON_PHRASES
except ImportError:                                   # imported from outside tools/
    NEEDS_PERSON_PHRASES = (NEEDS_PERSON, "gives this screen nothing that can be drawn",
                            "no display, metric or configuration directory")


def define_reason(s: dict) -> str | None:
    """Why a screen cannot be built yet, as check-screen-patterns NP sees it: "gaps" when the spec says a person must
    define it (a gap with one of NEEDS_PERSON_PHRASES), "nothing" when it binds no operation (a command centre that
    only links is the exception), else None."""
    for g in s.get("gaps") or []:
        if isinstance(g, dict) and any(p in str(g.get("why") or "") for p in NEEDS_PERSON_PHRASES):
            return "gaps"
    if not [a for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]             and s.get("pattern") != "commandCentre":
        return "nothing"
    return None


def define_needed(s: dict) -> bool:
    """The screen cannot be built until a person defines it (define_reason): its build waits on the definition
    (CHG-FXP-004; from 4 October until Sprint 3 starts, CHG-RFM-008)."""
    return define_reason(s) is not None


# **A split screen's tickets each say exactly what they build and who builds the rest** (CHG-FXP-001). The setup ticket
# reads "In the slice: a, b. Scope: a and b, 2 of BO-772's 6 operations; the other 4 (c, d, e, f) are
# APP-SETUP-BO-772-REST." and the rest-of-the-screen ticket "Scope: c, d, e and f, 4 of BO-772's 6 operations; its
# setup operations (a, b) are APP-SETUP-BO-772." The pointer carries the sentence (op-release.py).
SCOPE = re.compile(r"Scope: ([^\n]+?\.)(?= |$)")


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def scope_sentence(sid: str, mine, all_ops, sibling: str | None, setup_side: bool) -> str:
    mine = sorted(set(mine))
    others = sorted(set(all_ops) - set(mine))
    head = f"Scope: {_and(mine)}, {len(mine)} of {sid}'s {len(set(all_ops))} operations"
    if not others:
        return head + "."
    verb = "is" if len(others) == 1 else "are"
    where = f"{verb} {sibling}" if sibling else f"{verb} not planned yet"
    if setup_side:
        n = "one" if len(others) == 1 else str(len(others))
        return head + f"; the other {n} ({', '.join(others)}) {where}."
    return head + f"; its setup operation{'s' if len(others) > 1 else ''} ({', '.join(others)}) {where}."


def scope_of(r) -> str:
    """The scope sentence of a split screen's ticket, as build-service-docs.py wrote it, else ''."""
    m = SCOPE.search(r.get("description") or "")
    return "Scope: " + m.group(1) if m else ""


def define_sentence(sid: str, day: float, why: str | None = "gaps") -> str:
    """The line a build task on a screen that needs a person carries, read back into the pointer (CHG-FXP-004)."""
    import datetime as _dt
    d, left = _dt.date(2026, 10, 5), int(day)
    while left > 0:
        d += _dt.timedelta(days=1)
        if d.weekday() < 5:
            left -= 1
    said = (f"{sid} binds no operation yet (a person must define what it loads and saves)" if why == "nothing"
            else f"{sid}'s spec says a person must define it before it is built (its gaps)")
    return (f"Waits for its definition: {said}, so "
            f"this task starts once the lead has put the definition in ADAM, no earlier than {d.day} {d.strftime('%B')} "
            f"{d.year}; until then build nothing from the default layout.")


CARRY = re.compile(r"((?:Scope|Waits for its definition): [^\n]+?\.)(?= |$)")

# **A migration is written in the developer's repository, copied from the package's SQL** (CHG-R5-002, 7 October). A
# developer's agent stopped MIG-BASELINE (#27646): the ticket names V0001__baseline.sql, which the package no longer
# holds, and points at the helpers on top of 920-row-level-security.sql and 930-partitioning.sql, files headed
# "Derived by tools/derive-ddl.py. Do not hand-edit.", so copying from them read as forbidden. Every [DB] migration
# task (MIGRATION_KEY) carries MIGRATION_WORDING (build-service-docs.py; check-migration-wording.py gates it), and
# MIG-BASELINE names the functions it copies (baseline_wording, from the files themselves).
MIGRATION_KEY = re.compile(r"^(?:VM-)?MIG-")
MIGRATION_WORDING = ("Write this migration yourself, in our repository: the package's numbered SQL files "
                     "(backend/tenant and backend/control: 000-930 and the V01nn after-r1 files) are the reference "
                     "you copy from, never run as they are. Copying functions or tables out of them, such as the "
                     "helpers at the top of 920 and 930, is expected; 'Do not hand-edit' is about the package's own "
                     "files.")
BASELINE_FILES = ("backend/tenant/920-row-level-security.sql", "backend/tenant/930-partitioning.sql")
FUNCTION_DEF = re.compile(r"^CREATE OR REPLACE FUNCTION (\w+\.\w+)\(", re.M)


def baseline_functions(root) -> dict:
    """{file name: [function, ...]} every function BASELINE_FILES define, in file order: what V0001 copies."""
    from pathlib import Path
    out = {}
    for rel in BASELINE_FILES:
        f = Path(root) / rel
        out[Path(rel).name] = FUNCTION_DEF.findall(f.read_text(encoding="utf-8")) if f.exists() else []
    return out


AFTER_R1_FILE = re.compile(r"^V0[1-9]\d\d__after_r1_\d{8}\.sql$")
_AR1 = [
    (re.compile(r"^CREATE TABLE IF NOT EXISTS (\w+\.\w+)"), None),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) ADD COLUMN (?:IF NOT EXISTS )?(\w+)"), "column"),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) ADD CONSTRAINT (\w+)"), "constraint"),
    (re.compile(r"^CREATE (?:UNIQUE )?INDEX (?:IF NOT EXISTS )?(\w+) ON (?:ONLY )?(\w+\.\w+)"), "index"),
    (re.compile(r"^SELECT platform\.(apply_\w+)\('(\w+\.\w+)'"), "row-level security"),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) (.+?);?$"), "change"),
]


def after_r1_changes(root) -> dict:
    """{(file path relative to the package, table): [(kind, name), ...]} for every table a frozen after-r1 file
    (backend/<db>/V01nn__after_r1_<date>.sql, derive-ddl's frozen mode) changes but does not create (CHG-R5-002, the
    lead's check of 7 October: V0101 adds three catalogue columns no migration ticket cited). A table the same file
    creates is left out: the ticket that creates it cites that file already (src_files)."""
    from pathlib import Path
    out = {}
    for f in sorted((Path(root) / "backend").glob("*/V0*.sql")):
        if not AFTER_R1_FILE.match(f.name):
            continue
        rel = f.relative_to(root).as_posix()
        made, seen = set(), []
        for ln in f.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            for rx, kind in _AR1:
                m = rx.match(ln)
                if not m:
                    continue
                if kind is None:
                    made.add(m.group(1))
                elif kind in ("index", "row-level security"):
                    seen.append((m.group(2), kind, m.group(1)))
                else:
                    seen.append((m.group(1), kind, m.group(2)))
                break
        for t, kind, name in seen:
            if t not in made:
                out.setdefault((rel, t), []).append((kind, name))
    return out


def after_r1_sentence(rel: str, changes: dict) -> str:
    """The sentence a migration ticket carries for a frozen after-r1 file that changes the tables it creates."""
    parts = []
    for t, items in sorted(changes.items()):
        by = {}
        for kind, name in items:
            by.setdefault(kind, []).append(name)
        parts.append(f"{t}: " + ", ".join(
            "; ".join(v) if k == "change" else
            f"{k}{'es' if k == 'index' and len(v) > 1 else 's' if len(v) > 1 and k != 'row-level security' else ''} "
            f"{', '.join(v[:-1]) + ' and ' + v[-1] if len(v) > 1 else v[0]}"
            for k, v in by.items()))
    return (f"Source DDL after r1: {rel} ({'; '.join(parts)}); the files above are frozen at r1, so this migration, "
            "which creates those tables, carries these changes too.")


def baseline_wording(root) -> str:
    """The sentences MIG-BASELINE carries: its file is ours to write, and the helper functions it copies, by name."""
    fns = baseline_functions(root)
    parts = [f"from the top of {name}: {', '.join(names)}" for name, names in fns.items() if names]
    # no V-number here: check-ticket-text T-MIG-DONE keeps file numbers to the subject and MIGRATIONS.md
    return ("The baseline file named in the subject is one you write in our repository; the package keeps no baseline "
            "file of its own. It creates the helper functions every later migration calls, copied as they are "
            + "; ".join(parts) + " (the row-level security of each schema migration calls the platform.apply_* "
            "functions, so they come first).")


def carried(r) -> list:
    """The sentences of a task's description its pointer must carry: its scope and its wait for a definition."""
    return CARRY.findall(r.get("description") or "")


def screen_holds(screens: dict, op_hold: dict, listed: dict | None = None) -> dict:
    """{screen: (kind, into, why)} for every screen that gets no build task (CHG-FXP-002, -003): screen_hold, or kind
    "waits" when it binds an operation that is not built (op_hold: operation -> provisional | stub | deprecated)."""
    out = {}
    for sid, s in screens.items():
        h = screen_hold(s, listed)
        if not h:
            held = sorted({a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict)
                           and a.get("operationId") in op_hold})
            h = ("waits", "", "binds " + ", ".join(f"{o} ({op_hold[o]})" for o in held)
                 + ", not built until agreed") if held else None
        if h:
            out[sid] = h
    return out


def load_holds(root):
    """(op_hold, screen holds) read from the package at `root`: the contracts, the screens and
    docs/active/block-a-extra-tasks.json `screensNotBuilt`. For tools that do not load the package themselves
    (op-retire.py, check-ticket-builds.py)."""
    import json
    from pathlib import Path
    import yaml
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    root = Path(root)
    op_hold = {}
    for f in sorted((root / "contracts").rglob("*.yaml")):
        d = yaml.load(f.read_text(encoding="utf-8"), Loader=loader) or {}
        for item in (d.get("paths") or {}).values():
            for o in (item or {}).values():
                if isinstance(o, dict) and o.get("operationId"):
                    h = operation_hold(o)
                    if h:
                        op_hold[o["operationId"]] = h
    screens = {}
    for f in sorted((root / "screens").glob("P*.yaml")):
        for s in (yaml.load(f.read_text(encoding="utf-8"), Loader=loader) or {}).get("screens") or []:
            screens[s["id"]] = s
    ex = root / "docs" / "active" / "block-a-extra-tasks.json"
    listed = (json.loads(ex.read_text(encoding="utf-8")).get("screensNotBuilt") or {}) if ex.exists() else {}
    return op_hold, screen_holds(screens, op_hold, listed), screens


def merge_bindings(screens: dict) -> dict:
    """**A merged screen's operations are its target's** (4 October, CHG-FXP-002). "Merged into BO-087 ... it renders
    inside BO-087's component": ADM-243 hosted the setup operation setApprovalMatrix, and once ADM-243 had no task of
    its own the operation had no screen to be set up through. Each merged screen's bindings are added to its target's
    `apis` (in memory, never written), so the target's tickets build them. Returns {target: [operations added]}."""
    added = {}
    for sid, s in screens.items():
        m = MERGED_NOTE.search(str(s.get("notes") or ""))
        into = m.group(1) if m else None
        if not into or into not in screens or into == sid:
            continue
        t = screens[into]
        have = {a.get("operationId") for a in t.get("apis") or [] if isinstance(a, dict)}
        for a in s.get("apis") or []:
            if isinstance(a, dict) and a.get("operationId") and a["operationId"] not in have:
                t.setdefault("apis", []).append(dict(a, mergedFrom=sid))
                have.add(a["operationId"])
                added.setdefault(into, []).append(a["operationId"])
    return added


def main_builder(rows, pace: float = 1.0, lead: str = "", days_of=None) -> str:
    """The person who builds most of an app-module's tasks (`rows`, its children; module tests are not counted): by
    points, an AI task (no points) by its days x `pace` (`days_of` {key: days} where the row has none). Shared by
    build-service-docs.py, derive-block-a-schedule.py and check-plan-owners.py (CHG-R4-005): a module test never goes
    to its app-module's main builder.

    A tie has no main builder (""): two people who built as much are each a peer of the other. One exception, AI work
    (every task an AI unit): `lead`, the AI lead (team.json `ai.who`, first), is its main builder when tied, so its
    module test goes to the other AI engineer (the lead's to-do list for r2, 6 October: TEST-AM-AI-ENGINE-A2, over
    AI-ENGINE-PLANNER and AI-ENGINE-SUGGESTIONS at 8 days each, was Kalpita Mejari's)."""
    from collections import Counter
    c = Counter()
    ai = True
    days_of = days_of or {}
    for r in rows:
        who = r.get("assignee") or r.get("who")
        if who and not str(r.get("key", "")).startswith("TEST-"):
            c[who] += float(r.get("points") or 0) or float(r.get("days") or days_of.get(r.get("key")) or 0) * pace
            ai = ai and (r.get("area") == "ai" or r.get("track") == "AI")
    if not c:
        return ""
    top = max(c.values())
    tied = [w for w, v in c.items() if abs(v - top) < 1e-9]
    if len(tied) == 1:
        return tied[0]
    return lead if ai and lead in tied else ""


def wiring_parts(app_modules) -> dict:
    """{(screen, operation): wiring task key} from block-a-extra-tasks.json `appModules` (CHG-R4-003, 5 October): an
    operation a decided app-module's wiring task wires into a screen another ticket builds."""
    out = {}
    for am in app_modules or []:
        for w in am.get("wiring") or []:
            for sid in w.get("screens") or []:
                for o in w.get("operations") or []:
                    out[(sid, o)] = w["key"]
    return out


def strip_wiring(screens: dict, app_modules) -> dict:
    """**A wiring task's operations are not the screen ticket's** (CHG-R4-003, 5 October: the kiosk customisation in
    Block A2 is wired into KSK-001, an A1 screen, without changing the A1 ticket's scope, points or waits). Removes, in
    memory and never written, each wired operation from its screen's `apis` and the components it fills, so the plan
    sizes, closes and orders the screen's own ticket as before; the wiring task builds the rest. Returns
    {screen: {"key": wiring task, "ops": [removed], "all": [every operation the screen binds], "components": n}}."""
    parts = wiring_parts(app_modules)
    out = {}
    for (sid, o), key in sorted(parts.items()):
        s = screens.get(sid)
        if not s:
            continue
        rec = out.setdefault(sid, {"key": key, "ops": [], "components": 0,
                                   "all": sorted({a["operationId"] for a in s.get("apis") or []
                                                  if isinstance(a, dict) and a.get("operationId")})})
        before = len(s.get("apis") or [])
        s["apis"] = [a for a in s.get("apis") or [] if not (isinstance(a, dict) and a.get("operationId") == o)]
        if len(s["apis"]) < before:
            rec["ops"].append(o)
        for r in (s.get("layout") or {}).get("regions") or []:
            comps = r.get("components") or []
            keep = [c for c in comps if not (isinstance(c, dict) and c.get("operation") == o)]
            rec["components"] += len(comps) - len(keep)
            r["components"] = keep
        regions = (s.get("layout") or {}).get("regions")
        if regions:
            s["layout"]["regions"] = [r for r in regions if r.get("components")]
    return out


def rest_held(listed: dict | None) -> dict:
    """{screen: why} for the setup screens whose rest-of-the-screen task is not built (`screensNotBuilt` entries with
    `"part": "rest"`, CHG-FXP-004): BO-1179's setup operation stays, its wallet-exception console waits for a design."""
    return {sid: e.get("why") or "" for sid, e in (listed or {}).items() if isinstance(e, dict) and e.get("part") == "rest"}
