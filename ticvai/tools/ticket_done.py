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

    # an app-module feature builds what its "Builds:" lists: its screens and the operations they call, or for an
    # API-only one its operations and tables (CHG-TKT-001, CHG-TKT-004)
    if r["type"] in ("Task", "Feature") and not part and listed_builds(r.get("description")):
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

# **The control database has no row-level security** (ADR-0039; R8 blocker causes IDENTITY-C16, FOUNDATION-AI-C36,
# APPROVALS-TENANCY-C18; the lead, 20 October 2026: option A; CHG-R8MIG-005). It holds no scope tree: only the control
# plane's role reaches it, and each operation checks its PLATFORM_* permission and the tenant (an API client's
# allowedTenantIds). A ticket that builds only control tables or operations was told "under row-level security", which
# no developer could meet; it is told the rule that does hold.
CONTROL_RULE = ("checked by the operation's permission and tenant check (the control database has no row-level "
                "security: only the control plane's role reaches it, backend/MIGRATIONS.md)")
_LINEAGE: dict | None = None


def _lineage() -> dict:
    global _LINEAGE
    if _LINEAGE is None:
        import json
        from pathlib import Path
        p = Path(__file__).resolve().parents[1] / "handoff" / "api-data-lineage.json"
        try:
            _LINEAGE = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _LINEAGE = {}
    return _LINEAGE


def control_only(names, lineage: dict | None = None) -> bool:
    """True when every artefact named is in the control database: a table `control.*`, or an operation whose
    lineage reads and writes only `control.*` tables (stores such as `cache:` are not tables)."""
    lin = _lineage() if lineage is None else lineage
    seen = False
    for n in names:
        n = n.split("#", 1)[-1]
        if "." in n and " " not in n:
            if not n.startswith("control."):
                return False
            seen = True
            continue
        e = lin.get(n)
        if not isinstance(e, dict):
            return False
        tables = [t for t in (e.get("reads") or []) + (e.get("writes") or []) if "." in t and ":" not in t]
        if not tables or any(not t.startswith("control.") for t in tables):
            return False
        seen = True
    return seen


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
        guard = CONTROL_RULE if control_only(names) else "under row-level security"
        return (f"Done when {named} pass their contract tests against the contract in ADAM, including every documented "
                f"error response; each reads and writes only the tables its spec lists, {guard}; unit "
                "tests cover its rules; and a peer in the same stack has reviewed and tested it.")
    if kind == "Database" and names:
        # **How a [DB] ticket is proven** (CHG-R8MIG-008; the lead's delegate, 20 October 2026, from the ADAM
        # faster-db-tickets report, item 5 point 6): on a copy of the database as it was, twice, and ADAM's db-ticket
        # script comparing the result with the package; the full chain from empty runs daily and in every merge request.
        guard = ("columns, keys and indexes; no row-level security, which the control database does not have "
                 "(backend/MIGRATIONS.md)") if control_only(names) else "columns, keys, indexes, row-level security"
        return (f"Done when the migration for {named} applies on a copy of the database at the previous state, a "
                "second run applies nothing, and `node .claude/scripts/db-ticket.mjs <ticket>` says MATCH "
                f"({guard}); every migration from an empty database runs once a day and in the merge-request "
                "pipeline; and a peer has reviewed it.")
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


AFTER_R1_FILE = re.compile(r"^V0[1-9]\d\d[a-z]?__(?:names_(?:early_)?)?after_r1_\d{8}\.sql$")
# A block of the names file (ddl_forward.tag): `-- <table> | <kind> | <detail> [| <other table>]` (R8-MIG-001)
NAMES_TAG = re.compile(r"^-- (\w+\.\w+) \| (rename column|rename constraint|rename index|create index|drop index|"
                       r"drop foreign key|foreign key) \| (\S+(?: to \S+)?)(?: \| (\w+\.\w+))?$")
_AR1 = [
    (re.compile(r"^CREATE TABLE IF NOT EXISTS (\w+\.\w+)"), None),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) ADD COLUMN (?:IF NOT EXISTS )?(\w+)"), "column"),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) ADD CONSTRAINT (\w+)"), "constraint"),
    # a key the additive file adds guarded (ddl_forward.guard_add_constraint, CHG-R8MIG-010)
    (re.compile(r"^DO \$\$ BEGIN IF NOT EXISTS \(SELECT 1 FROM pg_constraint WHERE .*? THEN ALTER TABLE (?:ONLY )?"
                r"(\w+\.\w+) ADD CONSTRAINT (\w+)"), "constraint"),
    (re.compile(r"^CREATE (?:UNIQUE )?INDEX (?:IF NOT EXISTS )?(\w+) ON (?:ONLY )?(\w+\.\w+)"), "index"),
    (re.compile(r"^SELECT platform\.(apply_\w+)\('(\w+\.\w+)'"), "row-level security"),
    (re.compile(r"^ALTER TABLE (?:ONLY )?(\w+\.\w+) (.+?);?$"), "change"),
    # a retired column's guarded DROP NOT NULL (ddl_forward.retire_not_null, CHG-MGN-001)
    (re.compile(r"^DO \$\$ BEGIN IF EXISTS \(SELECT 1 FROM information_schema\.columns WHERE .*? THEN ALTER TABLE "
                r"(\w+\.\w+) ALTER COLUMN (\w+) DROP NOT NULL"), "column"),
]


def declared_moves(root) -> dict:
    """Every table name a declared rename or move retired -> the table's name now (tools/derive-schema-history.py
    RENAMES, chains followed). The same reading as build-service-docs.table_moves."""
    import importlib.util as _iu
    from pathlib import Path
    try:
        sp_ = _iu.spec_from_file_location("derive_schema_history", Path(root) / "tools" / "derive-schema-history.py")
        mod_ = _iu.module_from_spec(sp_)
        sp_.loader.exec_module(mod_)
        step = {r["from"]: r["to"] for r in mod_.RENAMES}
    except Exception:                       # noqa: BLE001 -- no history: nothing has moved
        step = {}
    out = {}
    for a in step:
        b, seen = step[a], {a}
        while b in step and b not in seen:
            seen.add(b)
            b = step[b]
        out[a] = b
    return out


def after_r1_changes(root) -> dict:
    """{(file path relative to the package, table): [(kind, name), ...]} for every table a frozen after-r1 file
    (backend/<db>/V01nn__after_r1_<date>.sql, derive-ddl's frozen mode) changes but does not create (CHG-R5-002, the
    lead's check of 7 October: V0101 adds three catalogue columns no migration ticket cited). A table the same file
    creates is left out: the ticket that creates it cites that file already (src_files).

    **A table is keyed by its name now** (18 October 2026, CHG-RSF-001): a forward migration names a table whose move
    is declared but not yet applied by its old name (V0105 re-applies sync.dsar_request's policy as
    platform.dsar_request, ddl_forward), while the migration ticket that creates it lists its name now (MIG-PLATFORM:
    sync.dsar_request). Keyed by the old name, no ticket was found to cite the file (check-migration-wording
    MW-AFTER-R1). The item says the name the file uses."""
    from pathlib import Path
    moves = declared_moves(root)
    out = {}
    for f in sorted((Path(root) / "backend").glob("*/V0*.sql")):
        if not AFTER_R1_FILE.match(f.name):
            continue
        rel = f.relative_to(root).as_posix()
        made, seen = set(), []
        for ln in f.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            tg = NAMES_TAG.match(ln)
            if tg:
                seen.append((tg.group(1), tg.group(2), tg.group(3)))
                if tg.group(4):   # a key names its parent too: the later of the two migrations adds it
                    seen.append((tg.group(4), tg.group(2), f"{tg.group(3)} (from {tg.group(1)})"))
                continue
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
        made |= {moves[t] for t in made if t in moves}
        for t, kind, name in seen:
            now = moves.get(t, t)
            if t in made or now in made:
                continue
            items = out.setdefault((rel, now), [])
            if now != t and ("change", f"named {t} in the file, its name before the declared move") not in items:
                items.append(("change", f"named {t} in the file, its name before the declared move"))
            items.append((kind, name))
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


def names_sentence(rel: str, changes: dict) -> str:
    """The sentence a migration ticket carries for the names file (R8-MIG-001): what the file does to its tables."""
    parts = []
    for t, items in sorted(changes.items()):
        parts.append(f"{t}: " + ", ".join(f"{k} {d}" for k, d in items))
    return (f"Source DDL after r1: {rel} (the names the contracts use: {'; '.join(parts)}); the files above create "
            "these tables with the names they had at r1, so this migration copies the blocks of that file that name "
            "its tables, after its tables are created (each block is guarded and does nothing when its table, key or "
            "index is not there). A key between this migration's table and one a later migration creates is copied "
            "by both, and takes effect in the later one.")


def baseline_wording(root) -> str:
    """The sentences MIG-BASELINE carries: its file is ours to write, and the helper functions it copies, by name."""
    fns = baseline_functions(root)
    parts = [f"from the top of {name}: {', '.join(names)}" for name, names in fns.items() if names]
    # **The helpers only an after-r1 file creates** (FOUNDATION-AI-C03): platform.drop_rls_policies, apply_read_beneath_rls,
    # apply_grant_holder_read_rls and the rest exist in V0102-V0105 alone, and the schema tickets say "call" them.
    # A function an after-r1 file defines again is copied from the latest file that defines it.
    from pathlib import Path
    have = {n for names in fns.values() for n in names}
    later = {}
    for f in sorted((Path(root) / "backend" / "tenant").glob("V0*.sql")):
        if AFTER_R1_FILE.match(f.name):
            for n in FUNCTION_DEF.findall(f.read_text(encoding="utf-8")):
                if n not in have:
                    later[n] = f.name
    by_file = {}
    for n, fname in later.items():
        by_file.setdefault(fname, []).append(n)
    parts += [f"from {fname} (created by no other file): {', '.join(names)}" for fname, names in sorted(by_file.items())]
    # no V-number here: check-ticket-text T-MIG-DONE keeps file numbers to the subject and MIGRATIONS.md
    return ("The baseline file named in the subject is one you write in our repository; the package keeps no baseline "
            "file of its own. It creates the helper functions every later migration calls, copied as they are "
            + "; ".join(parts) + " (the row-level security of each schema migration calls the platform.apply_* "
            "functions, so they come first). " + BASELINE_BODIES)


# **The baseline creates on an empty database only with function-body checks off** (CHG-R8MIG-008; ADAM faster-db-tickets
# report, package problem 2). The SQL-language helpers of 920 and 930 read platform.scope, which MIG-PLATFORM creates
# later, and PostgreSQL parses a SQL function's body when it is created unless check_function_bodies is off.
BASELINE_BODIES = ("Start the file with `SET check_function_bodies = off;`: the SQL-language helpers read "
                   "platform.scope, which the platform migration creates later, and PostgreSQL checks a function's body "
                   "against the tables that exist when it is created unless that setting is off (the body is checked "
                   "when the function first runs instead).")


# **A type the frozen DDL names and no file creates** (CHG-R8MIG-008; ADAM CR-001; the faster-db-tickets report, package
# problem 1). backend/tenant/010-pii.sql types pii.subject.kind as pii.subject_kind and pii.subject_contact.kind as
# pii.contact_kind; the schema reference has since made them text with a CHECK, but 010 is frozen at r1, so the
# migration that copies it cannot apply. Its ticket says what creates each type, with the values the schema reference
# (from the contracts) gives the column.
TYPE_USE = re.compile(r"^\s+(\w+)\s+([a-z_]+\.[a-z_0-9]+)(?:\[\])?\b", re.M)
TYPE_DEF = re.compile(r"CREATE\s+(?:TYPE|DOMAIN)\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-z_]+\.[a-z_0-9]+)", re.I)


def undefined_types(root) -> dict:
    """{table: [(type, column, [values])]} for every column of a baseline 0*.sql CREATE TABLE typed by a
    schema-qualified type no backend file creates; the values are the column's `enum` in handoff/schema-reference.json."""
    import json
    from pathlib import Path
    root = Path(root)
    files = sorted((root / "backend").rglob("*.sql"))
    defined = {n for f in files for n in TYPE_DEF.findall(f.read_text(encoding="utf-8"))}
    try:
        ref = json.loads((root / "handoff" / "schema-reference.json").read_text(encoding="utf-8")).get("cols") or {}
    except (OSError, ValueError):
        ref = {}
    out = {}
    for f in files:
        if not re.match(r"^0\d\d-", f.name):
            continue
        for m in re.finditer(r"CREATE TABLE IF NOT EXISTS (\w+\.\w+) \((.*?)\n\)", f.read_text(encoding="utf-8"), re.S):
            for col, typ in TYPE_USE.findall(m.group(2)):
                if typ in defined or typ.split(".")[0] in ("pg_catalog", "public"):
                    continue
                rec = next((c for c in ref.get(m.group(1), []) if c.get("column") == col), {})
                out.setdefault(m.group(1), []).append((typ, col, [str(v) for v in rec.get("enum") or []]))
    return out


def type_sentence(table: str, uses: list) -> str:
    """What the migration creating `table` writes first, so the frozen file it copies applies."""
    parts = []
    for typ, col, values in uses:
        vals = ", ".join("'" + v.replace("'", "''") + "'" for v in values)
        parts.append(f"`CREATE TYPE {typ} AS ENUM ({vals});` ({table}.{col})" if values else
                     f"`{typ}` ({table}.{col}: no values are recorded; ask the migration owner)")
    return ("**Create the types the copied DDL names first** (ADAM CR-001): the frozen file types these columns with "
            "enum types no package file creates, so before its CREATE TABLE write " + "; ".join(parts) + ". The values "
            "are the contracts' (handoff/schema-reference.json); a later forward migration turns the column into text "
            "with the same CHECK.")


# **A parent's row-level security waits for the parent** (CHG-R8MIG-008; the faster-db-tickets report, item 5 point 7 and
# package problem 3). A table protected through its parent row (`platform.apply_parent_rls`) reads the parent in its
# policy, so its policy cannot be created before the parent table: like a cross-schema key, it moves to the later
# migration. `policies` is {child: parent} from 920 and the after-r1 files; `made_by` is {table: migration key};
# `order` is {migration key: its file number}.
PARENT_POLICY = re.compile(r"SELECT platform\.apply_parent(?:_split)?_rls\('(\w+\.\w+)'::regclass, '\w+', "
                           r"'(\w+\.\w+)'::regclass")


def parent_policies(root) -> dict:
    """{child: parent} for every parent-row policy in the tenant and control 920 files and the after-r1 files (a
    later file's call wins: it re-applies the policy)."""
    from pathlib import Path
    out = {}
    for db in ("tenant", "control"):
        d = Path(root) / "backend" / db
        files = [d / "920-row-level-security.sql"] + sorted(f for f in d.glob("V0*.sql") if AFTER_R1_FILE.match(f.name))
        for f in files:
            if not f.exists():
                continue
            text = f.read_text(encoding="utf-8")
            for ln in text.splitlines():
                if ln.lstrip().startswith("--"):
                    continue
                for child, parent in PARENT_POLICY.findall(ln):
                    out[child] = parent
                m = re.match(r"SELECT platform\.apply_(?!parent)\w+\('(\w+\.\w+)'::regclass", ln.strip())
                if m and m.group(1) in out and f.name != "920-row-level-security.sql":
                    out.pop(m.group(1))     # a later file gave it another rule
    return out


def parent_policy_moves(policies: dict, made_by: dict, order: dict, moves: dict | None = None) -> tuple:
    """(moved, orphans): moved is {child: (its migration, the parent's later migration, parent)}; orphans is
    {child: parent} where no migration ticket creates the parent. `moves` maps a table's r1 name to its name now
    (declared_moves): 920 names inventory.item, which the migration tickets create as its name now."""
    moves = moves or {}
    moved, orphans = {}, {}
    for child, parent in sorted(policies.items()):
        child, parent = moves.get(child, child), moves.get(parent, parent)
        mc, mp = made_by.get(child), made_by.get(parent)
        if not mc:
            continue
        if not mp:
            orphans[child] = parent
        elif mp != mc and order.get(mp, 0) > order.get(mc, 0):
            moved[child] = (mc, mp, parent)
    return moved, orphans


def parent_policy_sentences(moved: dict, orphans: dict) -> dict:
    """{migration key: [sentence]} for both ends of each moved policy, and for an orphan's own migration."""
    out = {}
    for child, (mc, mp, parent) in sorted(moved.items()):
        out.setdefault(mc, []).append(
            f"**{child}'s row-level security waits for its parent**: its policy reads {parent}, which {mp} creates "
            f"later, so leave out its `platform.apply_parent_rls` call here; {mp} applies it.")
        out.setdefault(mp, []).append(
            f"**Also apply {child}'s row-level security here** (its `platform.apply_parent_rls` call, "
            f"920-row-level-security.sql, through {parent}): {mc} creates {child} before {parent} exists.")
    return out


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


# **A feature ticket lists the operations its screens call, and only those** (14 October 2026, CHG-TKT-001 and
# CHG-TKT-002; ADAM #27741, the Block A audit's S-FEATURE-OP-UNUSED and AM-TICKET-OP). An app-module's feature ticket
# listed the operations of its back-end tasks as its operations: "Identity & Security · Guest App" named seven
# marketing-crm operations -- the wishlist of GST-020, which is not on it, and searchGuests, a staff operation the
# guest app must never call -- and none of the identity, orders and consent operations its three screens call. The
# back end stays where it is planned (a pushed task keeps its operations, CHG-R6-052); what the feature says its
# screens call is this list. The audience rule is check-audience-match's (typed_props.callable_by, kept in step here
# so this module imports no checker): a guest-app screen (P01, P02, the kiosk P05) may call guest, anonymous and
# public operations (the kiosk device ones too), a staff screen staff, device, service, anonymous and public ones;
# a platform of another audience has no rule.
CALLABLE_BY = {"guest": {"guest", "anonymous", "public"},
               "staff": {"staff", "device", "service", "anonymous", "public"}}
OPERATOR_AUDIENCE = {"guest": "guest", "venue": "staff", "ticvai": "staff", "partner": "partner", "public": "public"}
DEVICE_GUEST_PLATFORMS = ("P05",)
GUEST_PLATFORMS = ("P01", "P02", "P05")


def platform_audience(platform: dict) -> set:
    """What a screen on `platform` (a screens/P*.yaml `platform` block) may call; empty = no rule declared."""
    aud = OPERATOR_AUDIENCE.get((platform or {}).get("operator"))
    code = str((platform or {}).get("code") or "")
    if aud not in CALLABLE_BY or (aud == "guest" and code not in GUEST_PLATFORMS):
        return set()
    ok = set(CALLABLE_BY[aud])
    if aud == "guest" and code in DEVICE_GUEST_PLATFORMS:
        ok.add("device")
    return ok


def screen_calls(screen: dict, platform: dict, audience_of) -> list:
    """The operations `screen` calls that a caller on its platform may call, in its `apis` order: every distinct
    operationId whose audience (`audience_of(op)` -> set, empty when the operation declares none) meets the
    platform's. An operation outside it is a wiring defect check-audience-match reports, never ticket scope."""
    ok, out = platform_audience(platform), []
    for a in screen.get("apis") or []:
        o = a.get("operationId") if isinstance(a, dict) else None
        if not o or o in out:
            continue
        aud = set(audience_of(o) or ())
        if ok and aud and not (aud & ok):
            continue
        out.append(o)
    return out


BACK_END_SENTENCE = "Back end built under it by its back-end tasks"


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
