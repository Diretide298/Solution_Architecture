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
  B-HOSTED-MODEL  a task's text plans a model we host or a GPU pool (gpt-oss in the cell, a Qwen3Guard host, vLLM, a GPU
                  node pool, an embedding or reranking model of our own: CHG-RONEP-008): "We are not hosting anything unless the client asks" (Chinmay, 3 October, CHG-RONEP-004)
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

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-ticket-builds.py [--all]
"""
import csv
import re
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import ticket_done as td  # noqa: E402

RULES = {
    "B-UNRESOLVED": "a ticket builds an id that is no operation, screen, table, service or ADR (r1 gate G2, CHG-RONEP-003)",
    "B-AI-EMPTY": "a Block A AI engine task names no operation, table or ADR it builds (r1 gate G2, CHG-RONEP-003)",
    "B-HOSTED-MODEL": "a task plans a model or GPU pool we host, against Chinmay's 3 October decision (CHG-RONEP-004)",
    "B-MODULE-TEST": "a module test names nothing it tests, in its builds or its done-when (r1 gate G1, CHG-RONEP-003)",
    "B-SETUP-LINKS": "a setup or rest-of-the-screen ticket links operations outside its part (r1 gate G4, CHG-RONEP-003)",
    "B-SCOPE-NAMED": "a split screen's ticket does not name exactly its operations and the ticket with the rest (CHG-FXP-001)",
    "B-NOT-BUILT": "a ticket builds a screen or operation the spec says is not built: merged, listed, stub, deprecated (CHG-FXP-002, -003)",
    "B-DEFINE-WAIT": "a build of a screen that needs a person starts before its definition or does not say it waits (CHG-FXP-004)",
    "B-BARE-TASK": "a hand-written task links nothing a pull carries: no operation, table, screen or service (CHG-FXP-005)",
}


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

    hosted = re.compile(r"gpt-oss|Qwen3Guard|vLLM|GPU (?:node )?pool|in-cell (?:open )?model|self-hosted (?:guard|LLM|model)|BGE-M3|Qwen3-(?:Embedding|Reranker)|(?:embeddings?|reranking)[^.;]{0,30}self-hosted", re.I)
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
    for k, bl in sorted(builds.items()):
        r = rows[k]
        if r["type"] != "Task" or k.startswith("TEST-"):
            continue
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
    guard.note(f"{n} build ids on {sum(1 for b in builds.values() if b)} tickets, {n_tests} module tests, "
               f"{n_setup} setup and rest tickets checked")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
