#!/usr/bin/env python3
"""What a ticket builds is real, a module test names what it tests, and a setup ticket links only its own part.

**3 October 2026, CHG-RONEP-003** (the r1 gate: an AI judge of 119 tickets on the fixed package). A ticket's builds
(`tools/ticket_done.py` builds_of: the ids op-release.py writes into the pointer and ADAM indexes) and its links
(`tools/adam-links.py`) are what a developer pulls. The judge found three ways they misled:

  G1  a module test (TEST-AM-*) named nothing to test: no builds, no links, "every screen state its YAML lists"
  G2  hand-written tasks built ids that do not exist: PLATFORM-SAGA-PAID "operation the saga proven end to end",
      OFFLINE-JOURNAL "operation record", the AI engine tasks nothing at all
  G4  APP-SETUP-BO-1162 said "2 of its 6 operations" and linked all 6

**What fails** (handoff/service-docs/plan-tasks.csv against contracts/, screens/, handoff/schema-reference.json,
handoff/service-decomposition.json and docs/adr/):

  B-UNRESOLVED    an id in a ticket's builds is no operation, screen, table, service or ADR of the package
  B-AI-EMPTY      a Block A AI engine task (AI-ENGINE-*, docs/active/block-a-extra-tasks.json) builds nothing: the
                  operations it serves or implements, its tables and ADRs go in the task's `operations` and `builds`
  B-HOSTED-MODEL  a task's text plans an LLM we host (gpt-oss in the cell, a Qwen3Guard host, vLLM, a self-hosted LLM or
                  guard, an LLM on our GPU): "We are not hosting anything unless the client asks" (Chinmay, 3 October,
                  CHG-RONEP-004). The embedding model, its reranker, Presidio and the Arabic NER on the AI GPU node
                  pool in the cell are ours and allowed (Chinmay, 4 October, CHG-R11-001, reversing CHG-RONEP-008)
  B-MODULE-TEST   a module test builds nothing although its app-module's tasks build something, or its done-when
                  names none of what it builds
  B-SETUP-LINKS   a setup ticket links an operation outside its slice, or a rest-of-the-screen ticket links one of
                  the setup operations

**4 October 2026, CHG-FXP-001 to -006** (the Sprint 1-2 judging: 1,030 tickets read as pulled, 121 not buildable):

  B-SCOPE-NAMED   a setup or rest-of-the-screen ticket of a split screen has no "Scope:" sentence naming exactly its
                  operations and the sibling ticket with the rest (BO-857-REST: "3 of its 7 operations", never which)
  B-NOT-BUILT     a task builds a screen the spec says is not built (merged into another, listed in
                  block-a-extra-tasks.json `screensNotBuilt`, or binding an operation not built), or an operations
                  task builds an operation its contract marks provisional, a stub ("the shape below is a proposal")
                  or deprecated (VM-BO-669, WEB-027, claimTableSession)
  B-DEFINE-WAIT   a Block A or A2 task builds a screen whose spec says it needs a person before it is built, with no
                  wait for its definition (`notBefore` and the "Waits for its definition:" line; ADM-506-REST)
  B-BARE-TASK     a hand-written task (block-a-extra-tasks.json, AI engine tasks aside) links only ADRs or nothing,
                  so its pull carries no file (OFFLINE-JOURNAL, PLATFORM-RLS); exempt only with the task's
                  `linksNothingBecause` (infrastructure, tooling), printed on every run

**21 October 2026, CHG-R8INT-035** (r8: the database update tasks missed V0107, V0110 and V0111, found only by the
upgrade test from r7, and V0112 came with the re-walk fixes; Chinmay, 20 October: "fix the source so that next gen can
clear those out by default"):

  B-DB-FILES      a database update task (a hand-written task building `file backend/<db>/V01xx__*.sql`) skips a
                  forward migration of that database the last release tag (r<N>) did not have, in its `builds` or in
                  its text

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-ticket-builds.py [--all]
"""
import csv
import re
import subprocess
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import ticket_done as td  # noqa: E402

RULES = {
    "B-UNRESOLVED": "a ticket builds an id that is no operation, screen, table, service or ADR (r1 gate G2, CHG-RONEP-003)",
    "B-DB-FILES": "a database update task skips a forward migration its database gained since the last release (CHG-R8INT-035)",
    "B-AI-EMPTY": "a Block A AI engine task names no operation, table or ADR it builds (r1 gate G2, CHG-RONEP-003)",
    "B-HOSTED-MODEL": "a task plans an LLM we host, against Chinmay's 3 October decision (CHG-RONEP-004; embeddings are ours, CHG-R11-001)",
    "B-MODULE-TEST": "a module test names nothing it tests, in its builds or its done-when (r1 gate G1, CHG-RONEP-003)",
    "B-SETUP-LINKS": "a setup or rest-of-the-screen ticket links operations outside its part (r1 gate G4, CHG-RONEP-003)",
    "B-SCOPE-NAMED": "a split screen's ticket does not name exactly its operations and the ticket with the rest (CHG-FXP-001)",
    "B-NOT-BUILT": "a ticket builds a screen or operation the spec says is not built: merged, listed, stub, deprecated (CHG-FXP-002, -003)",
    "B-DEFINE-WAIT": "a build of a screen that needs a person starts before its definition or does not say it waits (CHG-FXP-004)",
    "B-BARE-TASK": "a hand-written task links nothing a pull carries: no operation, table, screen or service (CHG-FXP-005)",
    "B-KERNEL-STORAGE": "a kernel ticket's mechanism needs a table, column, field, grant or file the package does not "
                        "have (CR-152, CR-163, CR-164, CR-166; CHG-CRA-005)",
}
# **The kernel tickets name a mechanism; the package must hold what it needs** (class 15 of the 18 October triage,
# CHG-CRA-005). Hrushikant Patkar found each gap building the kernel: no outbox in the control database for
# tenant.suspended (CR-152), no root scope path in control for the migrator (CR-163), no app-module map and no field
# telling the apps which modules are dark (CR-164), no per-aggregate sequence that survives a partition leaving and
# no occurred_at on the outbox (CR-166). Each need is stated once here, by the ticket that needs it; a need the
# package loses fails. `table` and `column` are found in the schema reference or in a contract schema persisted to
# the table, so the rule holds between a contract change and the release derive.
KERNEL_NEEDS = {
    "PLATFORM-OUTBOX": [
        ("column", "platform.outbox.occurred_at", "the envelope's occurredAt (CR-166)"),
        ("table", "platform.outbox_sequence", "the per-aggregate counter that survives partitions leaving (CR-166)"),
        ("index", "platform-ops.OutboxEntry:aggregateId,sequence", "the per-aggregate index (CR-166)"),
        ("grant", "platform.outbox_sequence", "every host allocates a sequence in its writing transaction (CR-166)"),
        ("table", "control.outbox", "the control database's outbox, for tenant.suspended (CR-152)"),
    ],
    "PLATFORM-KERNEL": [
        ("column", "control.cell_tenant.root_scope_path", "the tenant database's root scope path (CR-163)"),
    ],
    "PLATFORM-FLAGS": [
        ("field", "white-label.TenantAppStatus.darkAppModules", "the apps learn which modules are dark (CR-164)"),
        ("file", "handoff/release-flags.json", "the app-module to screens and operations map (CR-164)"),
    ],
}


def kernel_storage(guard, tables: set) -> None:
    """B-KERNEL-STORAGE: every need in KERNEL_NEEDS is in the package."""
    import yaml
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    cols = {t: {c.get("column") for c in cs} for t, cs in (ref.get("cols") or {}).items()}
    by, _ = g.schemas()
    persisted: dict = {}
    for (stem, name), s in by.items():
        tag = str((s or {}).get("x-ticvai-persistence") or "").strip().strip('"')
        for t in re.findall(r"\b([a-z_]+\.[a-z_0-9]+)\b", tag) if tag and not tag.lower().startswith("none") else []:
            persisted.setdefault(t, []).append((stem, name, s))

    def props(s):
        out = dict((s or {}).get("properties") or {})
        for b in (s or {}).get("allOf") or []:
            if isinstance(b, dict):
                out.update(b.get("properties") or {})
        return out

    kernel = ((yaml.safe_load((g.ROOT / "docs" / "active" / "cross-deployable-writes.yaml").read_text(encoding="utf-8"))
               or {}).get("kernel") or [])
    granted = {str(k.get("table")) for k in kernel if isinstance(k, dict)}
    for key, needs in sorted(KERNEL_NEEDS.items()):
        for kind, what, why in needs:
            ok = True
            if kind == "table":
                ok = what in tables or what in persisted
            elif kind == "column":
                t, c = what.rsplit(".", 1)
                ok = c in cols.get(t, set()) or any(g.snake(p) == c or (ps or {}).get("x-ticvai-column") == c
                                                    for _st, _n, s in persisted.get(t, []) for p, ps in props(s).items())
            elif kind == "index":
                sch, want = what.split(":")
                stem, name = sch.split(".")
                marks = (by.get((stem, name)) or {}).get("x-ticvai-index") or []
                ok = want.split(",") in [list(m) for m in marks if isinstance(m, list)]
            elif kind == "grant":
                ok = what in granted
            elif kind == "field":
                stem, name, field = what.split(".")
                ok = field in props(by.get((stem, name)) or {})
            elif kind == "file":
                ok = (g.ROOT / what).exists()
            if not ok:
                guard.add("B-KERNEL-STORAGE", f"{key}:{kind}:{what}",
                          f"{key} needs {kind} {what}: {why}, and the package does not have it")


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-ticket-builds", RULES)
    plan = g.ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
    if not plan.exists():
        guard.note("handoff/service-docs/plan-tasks.csv missing - run tools/build-service-docs.py")
        return guard.finish()
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = {r["key"]: r for r in csv.DictReader(fh) if "#" not in r["key"]}
    lineage = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    ops = set(g.operations())
    screens = {s["id"]: s for _, s in g.screens()}
    tables = set((g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    for f in (g.ROOT / "backend").glob("*/*.sql"):         # the runner's own tables (platform.schema_version) too
        tables |= {m.lower() for m in re.findall(
            r"CREATE TABLE (?:IF NOT EXISTS )?([A-Za-z_]+\.[A-Za-z_]+)", f.read_text(encoding="utf-8", errors="replace"))}
    services = set(((g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services")) or {})
    adrs = {"ADR-" + f.name[:4] for f in (g.ROOT / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")}

    def real(b):
        kind, _, name = b.partition(" ")
        if kind == "operation":
            return name.split("#")[-1] in ops
        if kind == "file":      # a package file ADAM links and pulls (CHG-R8INT-032's migration files; CHG-R8INT-034)
            return (g.ROOT / name).is_file()
        return {"screen": name in screens, "table": name in tables, "service": name in services,
                "adr": name in adrs}.get(kind, False)

    builds = {k: td.builds_of(r, "", lineage) for k, r in rows.items()}
    n = 0
    for k, bl in sorted(builds.items()):
        for b in bl:
            n += 1
            if not real(b):
                guard.add("B-UNRESOLVED", f"{k}:{b}", f"{k} builds `{b}`, which is no operation, screen, table, "
                                                      "service or ADR of the package")

    extra = g.load_json(g.ROOT / "docs" / "active" / "block-a-extra-tasks.json", {}) or {}
    for t in extra.get("tasks") or []:
        if t["key"].startswith("AI-ENGINE-") and str(t.get("block") or "A") == "A" and t["key"] in rows                 and not builds.get(t["key"]):
            guard.add("B-AI-EMPTY", t["key"], f"{t['key']} builds nothing: name its operations, tables and ADRs in "
                                              "block-a-extra-tasks.json `operations` / `builds`")

    # 4 October (CHG-R11-001): the embedding model (BGE-M3), its reranker, Presidio and the Arabic NER are ours, on the
    # AI GPU node pool in the cell, so BGE-M3, a GPU pool and a self-hosted embedder are no longer refused; an LLM still is.
    hosted = re.compile(r"gpt-oss|Qwen3Guard|vLLM|in-cell (?:open model|LLM)|self-hosted (?:guard|LLM|open model|chat model)"
                        r"|(?:LLM|language model|chat model)[^.;]{0,30}\bon (?:our|the) GPU", re.I)
    # A negated mention is the decision itself, not a plan: "no in-cell model: we host none" (CHG-R1S-002 in
    # AI-ENGINE-GATEWAY) failed the r1 merge refresh until this (CHG-GTRB-003).
    negated = re.compile(r"\b(?:no|not|never|without|nor)\s+(?:an?\s+|any\s+)?$", re.I)

    def plans_hosting(text):
        return next((m for m in hosted.finditer(text) if not negated.search(text[max(0, m.start() - 20):m.start()])),
                    None)

    for k, r in sorted(rows.items()):
        m = plans_hosting(r.get("description") or "") if r["type"] == "Task" else None
        if m:
            guard.add("B-HOSTED-MODEL", k, f"{k} plans '{m.group(0)}': the AI goes through providers (Core42 Compass, "
                                           "OpenAI UAE, BYOK) and the guard is the provider's safety service")

    # B-MODULE-TEST: a module test names its app-module's artefacts
    kids = defaultdict(list)
    for k, r in rows.items():
        if r["type"] == "Task" and r["parent"]:
            kids[r["parent"]].append(k)
    n_tests = 0
    for k, r in sorted(rows.items()):
        if r["type"] != "Task" or not k.startswith("TEST-AM-"):
            continue
        n_tests += 1
        theirs = {b for x in kids.get(r["parent"], []) if x != k for b in builds.get(x, [])
                  if not b.startswith(("service ", "adr "))}
        mine = builds.get(k) or []
        if theirs and not mine:
            guard.add("B-MODULE-TEST", k, f"{k} builds nothing, while its app-module {r['parent']} builds "
                                          f"{len(theirs)} artefacts ({', '.join(sorted(theirs)[:3])} ...)")
            continue
        done = td.DONE_WHEN.search(r["description"] or "")
        if mine and not (done and any(f"`{b.split(' ', 1)[1]}`" in done.group(1) for b in mine)):
            guard.add("B-MODULE-TEST", k, f"{k}: its done-when names none of the {len(mine)} artefacts it builds")

    # B-SETUP-LINKS: the links adam-links.py writes for a setup ticket and its rest
    spec = importlib.util.spec_from_file_location("adam_links", g.ROOT / "tools" / "adam-links.py")
    al = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(al)
    td.merge_bindings(screens)      # a merged screen's operations are built on its target (CHG-FXP-002)
    screen_ops = {sid: [a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]
                  for sid, s in screens.items()}
    touches = al.touches_from(rows, lineage, screen_ops)
    n_setup = 0
    for k, r in sorted(rows.items()):
        if r["type"] != "Task" or r["track"] != "Frontend" or not k.startswith("APP-SETUP-"):
            continue
        linked = {i.split("#")[-1] for kind, i in touches(k) if kind == "operation"}
        if k.endswith("-REST"):
            m = al.REST_OF.search(r["description"] or "")
            setup = {x.strip() for x in m.group(1).split(",")} if m else set()
            bad = sorted(linked & setup)
            what = "setup operations Block A built"
        else:
            m = al.SLICE.search(r["description"] or "")
            if not m:
                continue
            bad = sorted(linked - {x.strip() for x in m.group(1).split(",")})
            what = "operations outside its slice"
        n_setup += 1
        if bad:
            guard.add("B-SETUP-LINKS", k, f"{k} links {len(bad)} {what}: {', '.join(bad[:6])}")
    # B-SCOPE-NAMED (CHG-FXP-001): "BO-857 (the rest of the screen: 3 of its 7 operations)" never said which three
    for k, r in sorted(rows.items()):
        if r["type"] != "Task" or r["track"] != "Frontend" or not k.startswith("APP-SETUP-"):
            continue
        m = re.search(r"\(setup: (\d+) of its (\d+) operations\)|\(the rest of the screen: (\d+) of its (\d+) operations\)",
                      r["subject"])
        if not m:
            continue
        mine_n = int(m.group(1) or m.group(3))
        sc = td.scope_of(r)
        ms = re.match(r"Scope: (.+?), (\d+) of [A-Z]+-\d+'s (\d+) operations(?:; .*?\(([^)]*)\) (?:is|are) ([A-Z0-9-]+|not planned yet))?",
                      sc)
        sib = k[:-len("-REST")] if k.endswith("-REST") else k + "-REST"
        if not ms:
            guard.add("B-SCOPE-NAMED", k, f"{k}: '{r['subject'][5:70]}' has no Scope sentence naming its operations")
            continue
        named = [x.strip() for x in re.split(r", | and ", ms.group(1))]
        if len(named) != mine_n or int(ms.group(2)) != mine_n:
            guard.add("B-SCOPE-NAMED", k, f"{k}: its title says {mine_n} operations, its Scope names {len(named)}")
        if ms.group(5) and ms.group(5) != "not planned yet" and ms.group(5) != sib:
            guard.add("B-SCOPE-NAMED", k, f"{k}: its Scope sends the rest to {ms.group(5)}, not {sib}")
        if ms.group(5) == "not planned yet" and sib in rows:
            guard.add("B-SCOPE-NAMED", k, f"{k}: its Scope says the rest is not planned, but {sib} is")

    # B-NOT-BUILT (CHG-FXP-002, -003) and B-DEFINE-WAIT (CHG-FXP-004)
    op_hold, scr_hold, raw_screens = td.load_holds(g.ROOT)
    blocks = g.load_json(g.ROOT / "handoff" / "service-docs" / "block-a-schedule.json", {}) or {}
    starts, blk = blocks.get("start") or {}, blocks.get("block") or {}
    rest_out = td.rest_held(extra.get("screensNotBuilt") or {})
    for k, bl in sorted(builds.items()):
        r = rows[k]
        if r["type"] != "Task" or k.startswith("TEST-"):
            continue
        m_rest = re.match(r"^APP-SETUP-([A-Z]+-\d{3,4})-REST$", k)
        if m_rest and m_rest.group(1) in rest_out:
            guard.add("B-NOT-BUILT", k, f"{k} builds the rest of {m_rest.group(1)}, which is held: {rest_out[m_rest.group(1)]}")
        for b in bl:
            kind, _, name = b.partition(" ")
            if kind == "screen" and name in scr_hold:
                guard.add("B-NOT-BUILT", f"{k}:{name}", f"{k} builds screen {name}, which is not built: {scr_hold[name][2]}")
            if kind == "operation" and name.split("#")[-1] in op_hold and not k.startswith("AI-ENGINE-")                     and k.startswith(("SVC-", "VM-")):
                guard.add("B-NOT-BUILT", f"{k}:{name}", f"{k} builds {name}, which its contract marks "
                                                        f"{op_hold[name.split('#')[-1]]}")
        und = [b.split(" ", 1)[1] for b in bl if b.startswith("screen ")
               and b.split(" ", 1)[1] in raw_screens and td.define_needed(raw_screens[b.split(" ", 1)[1]])]
        if und and blk.get(k) in ("A", "A2"):
            if "Waits for its definition:" not in (r["description"] or "") or float(r.get("notBefore") or 0) < 1:
                guard.add("B-DEFINE-WAIT", k, f"{k} builds {und[0]}, whose spec needs a person, with no wait for its "
                                              "definition")

    # B-BARE-TASK (CHG-FXP-005): OFFLINE-JOURNAL and PLATFORM-RLS built only ADRs, which a pull does not carry
    for t in extra.get("tasks") or []:
        k = t["key"]
        if k not in rows or k.startswith("AI-ENGINE-"):
            continue
        if t.get("linksNothingBecause"):
            guard.note(f"B-BARE-TASK exempt: {k}: {t['linksNothingBecause']}")
            continue
        if not [b for b in builds.get(k) or [] if not b.startswith("adr ")]:
            guard.add("B-BARE-TASK", k, f"{k} links only ADRs or nothing: name the operations, tables or screens it "
                                        "builds in block-a-extra-tasks.json `builds`")
    # B-DB-FILES (CHG-R8INT-035): a database update task names every forward migration its database gained since the
    # last release tag (the tasks say "every file since r7"), in `builds` and in its text, so the next derived V01xx
    # cannot be left off it again
    fwd = re.compile(r"^V(01\d\d)([a-z]?)__.+\.sql$")
    order = lambda f: (int(fwd.match(f).group(1)), fwd.match(f).group(2))  # noqa: E731
    on_disk = defaultdict(set)
    for f in (g.ROOT / "backend").glob("*/V*.sql"):
        if fwd.match(f.name):
            on_disk[f.parent.name].add(f.name)
    shipped, last = set(), None
    try:
        tags = subprocess.run(["git", "tag", "--merged", "HEAD"], cwd=g.ROOT, capture_output=True, text=True,
                              check=True).stdout.split()
        nums = [int(x[1:]) for x in tags if re.fullmatch(r"r\d+", x)]
        if nums:
            last = f"r{max(nums)}"
            shipped = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", last, "--", "backend"], cwd=g.ROOT,
                                         capture_output=True, text=True, check=True).stdout.split())
    except (OSError, subprocess.CalledProcessError) as exc:
        guard.note(f"B-DB-FILES: no release tag to compare with ({exc}); every forward migration counts as new")
    for t in extra.get("tasks") or []:
        named = defaultdict(set)
        for b in t.get("builds") or []:
            kind, _, name = b.partition(" ")
            parts = name.split("/")
            if kind == "file" and len(parts) == 3 and parts[0] == "backend" and fwd.match(parts[2]):
                named[parts[1]].add(parts[2])
        for db, files in sorted(named.items()):
            for f in sorted(on_disk[db], key=order):
                if f"backend/{db}/{f}" in shipped:
                    continue
                if f not in files:
                    guard.add("B-DB-FILES", f"{t['key']}:{db}/{f}", f"{t['key']} updates the {db} database but does "
                              f"not build `file backend/{db}/{f}`, new since {last or 'the first release'}: add it to "
                              "`builds` and to the task's file list")
                elif f"backend/{db}/{f}" not in (t.get("detail") or ""):
                    guard.add("B-DB-FILES", f"{t['key']}:{db}/{f}:text", f"{t['key']} builds backend/{db}/{f} but its "
                              "text does not name it among the files to apply")
    guard.note(f"{n} build ids on {sum(1 for b in builds.values() if b)} tickets, {n_tests} module tests, "
               f"{n_setup} setup and rest tickets checked")
    kernel_storage(guard, tables)
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
