#!/usr/bin/env python3
"""Block A completes its apps, and no artefact an earlier plan built leaves the tickets without a reason.

**3 October 2026, CHG-RONEP-001 and CHG-RONEP-002** (Chinmay's r1 additions, docs/active/decisions/answers-3-october-r1-plan.md).
Block A's setup screens were drawn whole while their other operations were planned in Blocks B to D: BO-074's
createAccount (Block C), DEV-003's requestProductionAccess (Block B), ADM-037's setAiProvider (Block D). A developer
building the screen had buttons with no back end, and the Block A test could not reach them. The plan derivation
(`tools/build-service-docs.py`, the "Every operation a Block A screen binds" closure) now takes every screen a Block A
task builds into Block A's closure; this check holds the plan that comes out to it.

The r1 gate then found the opposite slip (lead, 3 October): listPaymentMethods, setPaymentRules and three more payment
operations, ADM-031 and four marketing tables were built in Block A by r2 and by no ticket now. They had ridden into
Block A inside a four-operation task or a migration with something Block A needed, and fell out when new operations
re-cut those tasks; nothing compared the plan with the one before. So an artefact the last released plan built in a
ticketed block must still be built in one, or carry its reason in `docs/active/block-a-extra-tasks.json` `departures`.

**What fails** (handoff/service-docs/plan-tasks.csv, screens/P*.yaml, contracts/, block-a-extra-tasks.json):

  C-BOUND        an operation a Block A screen binds (`apis`: onLoad, onAction and the rest) is built by no task of the
                 drop that wires it or an earlier one: Block A ships as A1 then A2 (CHG-RONEP-007), and a setup screen
                 is wired twice, its slice by the setup task and the rest by the rest-of-the-screen task
  C-FLOW         an operation a step of a flow through a Block A app (team.json sprintPlan.blockAApps) names, or a
                 branch of it is resolved by, is built by no Block A task (F02's extendSeatHold, CHG-RONEP-002)
  C-REACH        a Block A screen is reached from its app's entry (`navigation.isEntryPoint`) only through a screen
                 outside its drop or an earlier one (EMP-003, the staff home, was in no block; CHG-RONEP-006). The plan
                 pulls in app homes only (`navHomes`, lever A, CHG-RONEP-007); a screen behind a command centre gets a
                 link from its section home (tools/applied/nav-homes-r1-plan-3-october.py)
  C-NO-PATH      no navigation from its app's entry reaches a Block A screen at all: a navigation gap in the screens,
                 which the plan cannot close (an exception is written in NO_PATH_EXEMPT with its reason)
  C-DECIDED      a decided piece of Block A is not built in Block A: a `blockAOperations` operation, a `blockAScreens`
                 screen, or an AI engine task's `operations` not built by that task
  C-GONE         an operation, table or screen the last released plan built is built by no task now, with no reason
                 in `departures`
  C-UNTICKETED   one the last released plan built in a ticketed block (team.json sprintPlan.ticketBlocks) is built
                 only in later blocks now, with no reason in `departures`

A provisional operation (x-ticvai-provisional) is held off build tickets until it is agreed (CHG-GTR-007); it is
excused from C-BOUND and C-GONE and every such excuse is printed. The last released plan is the plan-tasks.csv at the
newest tag `rN` (else `old-rN`); `--since REF` names another. Without git the two comparison rules do not run, and
the check says so.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-plan-closure.py [--all] [--since REF]
"""
import csv
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import sprint_plan as sp  # noqa: E402
import ticket_done as td  # noqa: E402

RULES = {
    "C-BOUND": "a Block A screen binds an operation no Block A task builds (CHG-RONEP-001)",
    "C-FLOW": "an operation a step or branch of a Block A app's flow needs is built by no Block A task (CHG-RONEP-002)",
    "C-REACH": "a Block A screen is reached from its app's entry only through screens outside Block A (CHG-RONEP-006)",
    "C-NO-PATH": "a Block A screen no navigation from its app's entry reaches at all (CHG-RONEP-006)",
    "C-DECIDED": "a decided Block A operation, screen or AI engine operation is not built in Block A (CHG-RONEP-001)",
    "C-GONE": "an artefact the last released plan built is built by no task, with no recorded reason (CHG-RONEP-002)",
    "C-UNTICKETED": "an artefact the last released plan built in a ticketed block left them, with no reason (CHG-RONEP-002)",
}
PLAN = Path("handoff") / "service-docs" / "plan-tasks.csv"
RANK = {b: i for i, b in enumerate(sp.BLOCKS)}                # A (A1), A2, B, C, D (CHG-RONEP-007)
FAMILY = set(sp.BLOCK_A_FAMILY)
# screen -> why no navigation from its app's entry reaching it is not a plan finding. Empty: every gap is reported.
NO_PATH_EXEMPT: dict = {}


def built(rows):
    """artefact ('operation x', 'table s.t', 'screen S') -> {block: [task keys]} over the plan's tasks."""
    out = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get("type") != "Task" or "#" in r.get("key", "") or r.get("track") == "Test":
            continue                     # a module test lists what it tests (CHG-RONEP-003); it builds none of it
        for b in td.builds_of(r, "", {}):
            kind, _, name = b.partition(" ")
            if kind == "operation":
                b = f"operation {name.split('#')[-1]}"     # a "Builds:" lead names the contract too
            elif kind == "adr":
                continue                                    # a decision record is cited, not built
            out[b][r.get("block") or "A"].append(r["key"])
    return out


def first_block(blocks):
    return min(blocks, key=lambda b: RANK.get(b, 9)) if blocks else None


def git(*args):
    p = subprocess.run(["git", *args], cwd=g.ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, p.stdout


def reference(since):
    """(ref, rows) of the last released plan, or (None, reason)."""
    if since:
        ref = since
    else:
        rc, out = git("tag", "--list", "--sort=-creatordate")
        if rc != 0:
            return None, "git is not available"
        tags = out.split()
        ref = next((t for t in tags if re.fullmatch(r"r\d+", t)), None) or \
            next((t for t in tags if re.fullmatch(r"old-r\d+", t)), None)
        if not ref:
            return None, "no release tag (rN or old-rN)"
    rc, out = git("show", f"{ref}:./{PLAN.as_posix()}")
    if rc != 0:
        return None, f"{ref} has no {PLAN.as_posix()}"
    return ref, list(csv.DictReader(io.StringIO(out)))


def main() -> int:
    g.force_utf8()
    args = sys.argv[1:]
    since = args[args.index("--since") + 1] if "--since" in args and args.index("--since") + 1 < len(args) else None
    guard = g.Guard("check-plan-closure", RULES)
    plan = g.ROOT / PLAN
    if not plan.exists():
        guard.note("handoff/service-docs/plan-tasks.csv missing - run tools/build-service-docs.py")
        return guard.finish()
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    extra = g.load_json(g.ROOT / "docs" / "active" / "block-a-extra-tasks.json", {}) or {}
    team = g.load_json(g.ROOT / "docs" / "active" / "team.json", {}) or {}
    ticketed = set(((team.get("sprintPlan") or {}).get("ticketBlocks")) or ["A", "B"])
    ops = g.operations()
    provisional = {o for o, x in ops.items() if (x.get("op") or {}).get("x-ticvai-provisional")}
    screens = {s["id"]: s for _, s in g.screens()}
    now = built(rows)

    def rank_of(where):
        return min((RANK.get(b, 9) for b in where), default=99)

    # C-BOUND: every operation a Block A screen binds is built in the screen's drop or an earlier one (A1, then A2)
    screen_block = {b.split(" ", 1)[1]: first_block(bl) for b, bl in now.items() if b.startswith("screen ")}
    a_screens = sorted(sid for sid, b in screen_block.items() if b in FAMILY)
    # a setup screen is wired in two tickets: its setup task wires the slice's operations, the rest-of-the-screen task
    # the others; each must find its operations built by its own drop or an earlier one (A1 then A2, CHG-RONEP-007)
    by_key = {r["key"]: r for r in rows if r.get("type") == "Task"}

    def wired_in(sid, o):
        setup = by_key.get(f"APP-SETUP-{sid}")
        if not setup:
            return screen_block[sid]
        m = re.search(r"In the slice: ([A-Za-z0-9, ]+?)(?:\)|\.|;|$)", setup.get("description") or "")
        sl = {x.strip() for x in m.group(1).split(",")} if m else set()
        rest = by_key.get(f"APP-SETUP-{sid}-REST")
        return (setup.get("block") or "A") if (o in sl or not rest) else (rest.get("block") or "A")
    excused = set()
    n_bound = 0
    for sid in a_screens:
        s = screens.get(sid)
        if not s:
            continue
        for o in sorted({a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")}):
            n_bound += 1
            where = now.get(f"operation {o}") or {}
            if rank_of(where) <= RANK[wired_in(sid, o)]:
                continue
            if o in provisional:
                excused.add(o)
                continue
            later = first_block(where)
            guard.add("C-BOUND", f"{sid}:{o}", f"{sid} (wired in Block {sp.block_label(wired_in(sid, o))}) binds {o}, which "
                      + (f"Block {later} builds ({', '.join(where[later][:2])})" if later else "no task builds"))
    # C-FLOW: the operations of the flows through Block A's apps (the closure build-service-docs.py takes)
    a_apps = set(((team.get("sprintPlan") or {}).get("blockAApps")) or ["P01", "P02", "P04", "P15"])
    for f in sorted((g.ROOT / "flows").glob("F*.yaml")):
        fd = g.load_yaml(f) or {}
        if not ({str(x).split()[0] for x in fd.get("platforms") or []} & a_apps):
            continue
        need = {str(o).split()[0] for st in fd.get("steps") or [] if isinstance(st, dict) for o in st.get("operations") or []}
        need |= {str(b.get("resolvedBy") or "").split(" ")[0] for b in fd.get("branches") or [] if isinstance(b, dict)}
        for o in sorted(x for x in need if x in ops):
            where = now.get(f"operation {o}") or {}
            if "A" in where:                 # a Block A app's flow runs in A1
                continue
            if o in provisional:
                excused.add(o)
                continue
            guard.add("C-FLOW", f"{fd.get('id')}:{o}", f"{fd.get('id')} runs through a Block A app and needs {o}, which "
                      + (f"Block {first_block(where)} builds" if where else "no task builds"))

    # C-REACH, C-NO-PATH: each Block A screen is reached from its app's entry through Block A screens
    plat = {s["id"]: stem.split("-")[0] for stem, s in g.screens()}
    by_plat = defaultdict(set)
    for sid in a_screens:
        if sid in screens:
            by_plat[plat[sid]].add(sid)
    for pf, theirs_all in sorted(by_plat.items()):
        app = {sid: s for sid, s in screens.items() if plat[sid] == pf}
        for drop in sp.BLOCK_A_FAMILY:               # an A1 screen is reached through A1, an A2 one through A1 or A2
            a_set = {sid for sid in a_screens if RANK[screen_block[sid]] <= RANK[drop]}
            theirs = {sid for sid in theirs_all if screen_block[sid] == drop}
            paths = sp.nav_paths(app, a_set, theirs)
            for sid in sorted(theirs):
                if sid not in paths:
                    if sid in NO_PATH_EXEMPT:
                        guard.note(f"exempt C-NO-PATH {sid}: {NO_PATH_EXEMPT[sid]}")
                        continue
                    guard.add("C-NO-PATH", sid, f"{sid} ({pf}, Block {sp.block_label(drop)}): no navigation from the app's "
                              "entry reaches it")
                    continue
                outside = [x for x in paths[sid] if x not in a_set]
                if outside:
                    guard.add("C-REACH", sid, f"{sid} ({pf}, Block {sp.block_label(drop)}) is reached only through "
                              f"{', '.join(outside)}, outside it: {' > '.join(paths[sid])}")

    for o in sorted(excused):
        guard.note(f"excused: {o} is provisional (x-ticvai-provisional), held off build tickets until agreed (CHG-GTR-007)")

    # C-DECIDED: the decided parts of Block A
    for o, why in sorted((extra.get("blockA1Operations") or {}).items()):
        where = now.get(f"operation {o}") or {}
        if o in ops and "A" not in where:
            guard.add("C-DECIDED", f"op:{o}", f"{o} is decided A1 ({why[:80]}) but is built in "
                      + (f"Block {first_block(where)}" if where else "no task"))
    for o, why in sorted((extra.get("blockAOperations") or {}).items()):
        where = now.get(f"operation {o}") or {}
        if o in ops and not FAMILY & set(where):
            guard.add("C-DECIDED", f"op:{o}", f"{o} is decided Block A ({why[:80]}) but is built in "
                      + (f"Block {first_block(where)}" if where else "no task"))
    for sid, why in sorted((extra.get("blockAScreens") or {}).items()):
        if sid in screens and not FAMILY & set(now.get(f"screen {sid}") or {}):
            guard.add("C-DECIDED", f"screen:{sid}", f"{sid} is decided Block A ({why[:80]}) but no Block A task builds it")
        rest = [r["key"] for r in rows if r.get("type") == "Task" and r["key"].endswith(f"{sid}-REST")
                and (r.get("block") or "A") not in FAMILY]
        if rest:
            guard.add("C-DECIDED", f"screen-rest:{sid}", f"{sid} is decided Block A whole, but {rest[0]} is in a later block")
    for t in extra.get("tasks") or []:
        for o in t.get("operations") or []:
            keys = [k for bl in (now.get(f"operation {o}") or {}).values() for k in bl]
            if o in ops and t["key"] not in keys:
                guard.add("C-DECIDED", f"ai:{o}", f"{o} is served by {t['key']} (block-a-extra-tasks.json) but the plan "
                          f"builds it in {', '.join(keys) or 'no task'}")
            elif o in ops and len(keys) > 1:
                guard.add("C-DECIDED", f"ai:{o}", f"{o} is served by {t['key']} and also built by "
                          f"{', '.join(k for k in keys if k != t['key'])}")

    # C-GONE, C-UNTICKETED: against the last released plan
    departures = extra.get("departures") or {}
    ref, ref_rows = reference(since)
    if ref is None:
        guard.note(f"C-GONE and C-UNTICKETED not run: {ref_rows}")
    else:
        before = built(ref_rows)
        used = set()
        for art, bl in sorted(before.items()):
            here = now.get(art) or {}
            if not here:
                name = art.split(" ", 1)[1]
                if art.startswith("operation ") and name in provisional:
                    guard.note(f"excused: {art} built by {ref}, held now as provisional (CHG-GTR-007)")
                    continue
                if art in departures:
                    used.add(art)
                    continue
                guard.add("C-GONE", art, f"{art}: {ref} built it ({', '.join(bl[first_block(bl)][:2])}); no task "
                          "builds it now and block-a-extra-tasks.json departures gives no reason")
                continue
            if set(bl) & ticketed and not set(here) & ticketed:
                if art in departures:
                    used.add(art)
                    continue
                guard.add("C-UNTICKETED", art, f"{art}: {ref} built it in Block {first_block(bl)} "
                          f"({', '.join(bl[first_block(bl)][:2])}); now only Block {first_block(here)} "
                          f"({', '.join(here[first_block(here)][:2])}), which is not ticketed, and departures gives no reason")
        for art in sorted(set(departures) - used):
            guard.note(f"departures entry not needed against {ref}: {art} (remove it once {ref} is the last release)")
        guard.note(f"compared with the plan at {ref}: {len(before)} artefacts then, {len(now)} now; "
                   f"{len(used)} departure(s) with their reason")
    guard.note(f"{len(a_screens)} Block A screens, {n_bound} bindings checked")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
