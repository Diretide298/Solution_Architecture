#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every Block A ticket links something ADAM pulls, and every link ADAM loads resolves to an artefact HEAD has.

**14 October 2026** (the Block A audit, batch GRD, CHG-GRD-001; lead: "With the pattern of errors we need to get them
updated"). The pull of every Block A ticket on r5 (`audit/ticvai/runs/audit-1014/`, classes `adam-pull/feature:
nothing linked`, `adam-pull/task: nothing linked`, `adam-pull/links ADAM cannot resolve`) found 123 features and 29
tasks that reached developers with nothing linked, and 55 tickets whose links ADAM could not find (a table a rename
retired, a lineage view, `platform.schema_version`, a sub-task's part read as an operation). Batch TKT fixed the
generator (tools/adam-links.py, CHG-TKT-004..006); nothing failed the gate when it happened, so nothing would fail it
the next time. This reads what ADAM loads at the release, `handoff/service-docs/adam-links.json` (one row per
OpenProject id, kind and id; viewer/api/load_links.py), against the plan and the package:

    TL-NOTHING-LINKED  a Block A feature or task (the plan's Feature and Task rows under BLOCK-A, tasks.csv, and the
                       ones the last release bundle cut there, op-release.json, that are still in the plan) has no
                       link ADAM pulls. An `adr` link alone is nothing: adam_pull lists decisions and pulls no file
                       for them (viewer/mcp/tools.mjs pullOne), so the pull says `linked: 0`.
    TL-DEAD-LINK       a link resolves to nothing at HEAD: an operation `contract#operationId` no contract has, a
                       table neither in the schema reference nor a read view the lineage declares
                       (audit_guard.read_views), a screen not in screens/, an ADR with no docs/adr file, a `file`
                       git does not track, a service service-decomposition.json does not have, or a kind ADAM has
                       no lookup for.
    TL-REHEARSAL       docs/active/release-runbook.md section 4 does not hold the rehearsal pull as the gate step
                       before the tag (CHG-GRD-003; audit plan step 11a): a local ADAM on `r<N>-rc` with the stand-in
                       OpenProject, every block ticket pulled with the shipped connector, compared with the last live
                       pull, passing only with 0 pull errors, `r<N>` on every ticket, 0 tickets with nothing linked
                       and 0 dead links. The checks read the package; only a pull reads what a developer gets.

Every finding is strict: it fails whether or not the baseline lists it, and is never written into it. A planned Block
A ticket with no OpenProject id yet (made at the next apply) and a pushed one the plan no longer has (op-retire
closes or parks it) are notes, not findings: ADAM serves neither as Block A work today.

Read-only. Run `tools/build-service-docs.py` and `tools/adam-links.py` first: adam-links.json is derived from the
plan, and a stale one says nothing about HEAD. The self-tests run first, every time.

    python3 tools/check-ticket-links.py [--all]
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

DOCS = g.ROOT / "handoff" / "service-docs"
BLOCK = "BLOCK-A"
TICKET_TYPES = ("Feature", "Task")
# Kinds adam_pull pulls as a file (lookupFor in viewer/mcp/tools.mjs). `adr` is listed, never pulled.
PULLED = {"screen", "flow", "contract", "operation", "schema", "table", "module", "service", "file"}

RULES = {
    "TL-NOTHING-LINKED": "a Block A feature or task has no link adam_pull pulls (an ADR alone is nothing)",
    "TL-DEAD-LINK": "a link in adam-links.json names an operation, table, screen, ADR, file or service HEAD lacks",
    "TL-REHEARSAL": "the release runbook does not gate the tag on a rehearsal pull with its four zero criteria",
}

# What the runbook's section 4 must say about the rehearsal pull (CHG-GRD-003): each phrase, whitespace collapsed.
REHEARSAL = {
    "the step": "rehearsal pull",
    "before the tag": "before the tag",
    "the candidate tag": "r<N>-rc",
    "the stand-in OpenProject": "viewer/api/fake-openproject.mjs",
    "the shipped connector": "shipped connector",
    "the last live pull": "last live pull",
    "0 pull errors": "0 pull errors",
    "r<N> on every ticket": "release `r<N>` on every ticket",
    "0 tickets with nothing linked": "0 tickets with nothing linked",
    "0 dead links": "0 dead links",
}


# ------------------------------------------------------------------------------------------------- the rules
def resolves(kind: str, target: str, idx: dict) -> bool:
    """Whether HEAD has what a (kind, id) link names, as ADAM looks it up."""
    target = str(target)
    if kind == "operation":
        return target in idx["ops"]
    if kind == "table":
        return target in idx["tables"] or target in idx["views"]
    if kind == "screen":
        return target in idx["screens"]
    if kind == "adr":
        return target in idx["adrs"]
    if kind == "file":
        return target in idx["files"]
    if kind == "service":
        return target in idx["services"]
    if kind == "contract":
        return target in idx["contracts"]
    if kind == "flow":
        return target in idx.get("flows", set())
    return False


def findings(block: dict, ids: dict, links: list, idx: dict) -> list:
    """[(rule, key, message)]. `block`: Block A key -> type; `ids`: key -> OpenProject id; `links`: adam-links rows."""
    out = []
    by_wp = defaultdict(list)
    for ln in links:
        by_wp[str(ln.get("key"))].append(ln)
    key_of = {str(v): k for k, v in ids.items()}
    for key in sorted(block):
        wp = ids.get(key)
        if wp is None:
            continue
        pulled = [ln for ln in by_wp.get(str(wp), []) if ln.get("kind") in PULLED]
        if not pulled:
            had = sorted({f"{ln.get('kind')} {ln.get('id')}" for ln in by_wp.get(str(wp), [])})
            out.append(("TL-NOTHING-LINKED", f"#{wp} {key}",
                        f"#{wp} {key} ({block[key]}): nothing adam_pull pulls is linked"
                        + (f" (only {', '.join(had[:3])})" if had else "")))
    seen = set()
    for ln in links:
        kind, target, wp = str(ln.get("kind")), str(ln.get("id")), str(ln.get("key"))
        k = f"#{wp} {kind} {target}"
        if k in seen:
            continue
        seen.add(k)
        if not resolves(kind, target, idx):
            out.append(("TL-DEAD-LINK", k, f"#{wp} {key_of.get(wp, '?')}: {kind} `{target}` is not in the package "
                                           f"at HEAD"))
    return out


def rehearsal_findings(text: str) -> list:
    """TL-REHEARSAL on the release runbook: its section 4 (the gates) holds the rehearsal pull and its criteria."""
    m = re.search(r"^## 4\.[^\n]*\n(.*?)(?=^## \d|\Z)", text, re.M | re.S)
    sec = re.sub(r"\s+", " ", m.group(1)) if m else ""
    return [("TL-REHEARSAL", f"runbook:4:{what}", f"docs/active/release-runbook.md section 4 does not say {what} "
                                                   f"(\"{phrase}\") of the rehearsal pull before the tag")
            for what, phrase in REHEARSAL.items() if phrase not in sec]


def block_tickets(rows: dict, bundle: dict | None) -> tuple:
    """(Block A key -> type, pushed Block A keys the plan no longer has). Block A is every Feature and Task whose
    top ancestor is BLOCK-A, in the plan now (tasks.csv) and in the last release bundle (op-release.json)."""
    def top(par, k):
        seen = set()
        while par.get(k) and k not in seen:
            seen.add(k)
            k = par[k]
        return k

    par = {k: r.get("parent") or "" for k, r in rows.items()}
    block = {k: r["type"] for k, r in rows.items() if r.get("type") in TICKET_TYPES and top(par, k) == BLOCK}
    gone = []
    if bundle:
        bpar = {t["key"]: t.get("parent") or "" for t in bundle.get("tickets") or []}
        for t in bundle.get("tickets") or []:
            if t.get("type") in TICKET_TYPES and top(bpar, t["key"]) == BLOCK and t["key"] not in block:
                if t["key"] in rows:        # moved to another block: the plan decides
                    continue
                gone.append(t["key"])
    return block, sorted(gone)


# ------------------------------------------------------------------------------------------------- the package
def package_index() -> dict:
    ops, contracts = set(), set()
    for stem, _rel, doc in g.contracts():
        contracts.add(stem)
        for item in (doc.get("paths") or {}).values():
            if not isinstance(item, dict):
                continue
            for m in g.VERBS:
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    ops.add(f"{stem}#{op['operationId']}")
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    tables = {t for t in (ref.get("cols") or {})}
    known = {t for t in set(ref.get("cols") or {}) | set(ref.get("storage") or {}) if "." in t and ":" not in t}
    lineage = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    views = set(g.read_views(lineage, known))
    files = set((subprocess.run(["git", "ls-files", "-z"], cwd=g.ROOT, capture_output=True, text=True,
                                encoding="utf-8").stdout or "").split("\0")) - {""}
    if not files:       # an export of a commit (git archive), outside git: what it holds is what the commit tracks
        files = {p.relative_to(g.ROOT).as_posix() for p in g.ROOT.rglob("*") if p.is_file()}
    adrs = {f"ADR-{p.split('/')[-1][:4]}" for p in files
            if p.startswith("docs/adr/") and p.split("/")[-1][:4].isdigit() and p.endswith(".md")}
    dec = g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}
    flows = {p.rsplit("/", 1)[-1].rsplit(".", 1)[0] for p in files if p.startswith("flows/") and p.endswith(".yaml")}
    return {"ops": ops, "contracts": contracts, "tables": tables, "views": views, "screens": {s["id"] for _, s in
            g.screens()}, "adrs": adrs, "files": files, "services": set(dec.get("services") or {}), "flows": flows}


# ------------------------------------------------------------------------------------------------- self-tests
def self_test() -> list:
    """Each rule against made-up rows it must pass and fail. Returns the failures."""
    fails = []
    idx = {"ops": {"access#listPasses"}, "contracts": {"access"}, "tables": {"access.pass"},
           "views": {"access.pass_for_orders"}, "screens": {"BO-001"}, "adrs": {"ADR-0055"},
           "files": {"repos/ticvai-docs/setup/README.md", "docs/adr/0055-hosts.md"}, "services": {"AccessService"},
           "flows": set()}
    block = {"AM-A": "Feature", "AM-B": "Feature", "T-C": "Task", "T-D": "Task", "T-E": "Task"}
    ids = {"AM-A": 1, "AM-B": 2, "T-C": 3, "T-D": 4, "T-E": 5}
    links = [
        {"key": "1", "kind": "screen", "id": "BO-001"},
        {"key": "2", "kind": "adr", "id": "ADR-0055"},                      # an ADR alone: nothing pulled
        {"key": "3", "kind": "service", "id": "AccessService"},
        {"key": "3", "kind": "table", "id": "access.pass_for_orders"},      # a declared read view resolves
        {"key": "4", "kind": "file", "id": "repos/ticvai-docs/setup/README.md"},
        {"key": "4", "kind": "operation", "id": "SETUP-HOSTS#commerce"},     # a sub-task part read as an operation
        {"key": "4", "kind": "table", "id": "catalogue.inventory_hold"},     # a table a rename retired
        {"key": "4", "kind": "file", "id": "docs/untracked.md"},
        {"key": "4", "kind": "adr", "id": "ADR-9999"},
        {"key": "4", "kind": "service", "id": "GhostService"},
        {"key": "4", "kind": "decision", "id": "DEC-1"},                     # a kind ADAM has no lookup for
        {"key": "1", "kind": "operation", "id": "access#listPasses"},
        {"key": "1", "kind": "operation", "id": "access#listPasses"},        # a repeat is one finding at most
    ]
    got = findings(block, ids, links, idx)
    nothing = sorted(k for r, k, _ in got if r == "TL-NOTHING-LINKED")
    dead = sorted(k for r, k, _ in got if r == "TL-DEAD-LINK")
    if nothing != ["#2 AM-B", "#5 T-E"]:
        fails.append(f"TL-NOTHING-LINKED found {nothing}, expected the ADR-only feature and the bare task")
    want = sorted(["#4 operation SETUP-HOSTS#commerce", "#4 table catalogue.inventory_hold",
                   "#4 file docs/untracked.md", "#4 adr ADR-9999", "#4 service GhostService", "#4 decision DEC-1"])
    if dead != want:
        fails.append(f"TL-DEAD-LINK found {dead}, expected {want}")
    if findings(block, {k: v for k, v in ids.items() if k in ("AM-A", "T-C")}, links[:1] + links[2:4], idx):
        fails.append("a ticket with no OpenProject id, or one linked well, was reported")
    rows = {"BLOCK-A": {"type": "Epic", "parent": ""}, "AM-A": {"type": "Feature", "parent": "BLOCK-A"},
            "T-C": {"type": "Task", "parent": "AM-A"}, "S-1": {"type": "Sub Task", "parent": "T-C"},
            "BLOCK-B": {"type": "Epic", "parent": ""}, "AM-X": {"type": "Feature", "parent": "BLOCK-B"},
            "T-MOVED": {"type": "Task", "parent": "AM-X"}}
    bundle = {"tickets": [{"key": "AM-A", "type": "Feature", "parent": "BLOCK-A"},
                          {"key": "T-GONE", "type": "Task", "parent": "AM-A"},
                          {"key": "T-MOVED", "type": "Task", "parent": "AM-A"}]}
    blk, gone = block_tickets(rows, bundle)
    if blk != {"AM-A": "Feature", "T-C": "Task"} or gone != ["T-GONE"]:
        fails.append(f"block_tickets gave {blk} and gone {gone}")
    good = ("## 4. Gates\n### The rehearsal pull: before the tag\nTag `r<N>-rc`; viewer/api/fake-openproject.mjs; the "
            "shipped connector; compare with the last live pull. 0 pull errors; release `r<N>` on every\nticket; 0 "
            "tickets with nothing linked; 0 dead links.\n## 5. Tag\n")
    if rehearsal_findings(good):
        fails.append(f"TL-REHEARSAL refused a runbook that holds the step: {rehearsal_findings(good)}")
    outside = "## 4. Gates\nNothing.\n## 5. Tag\n" + good.split("## 4. Gates\n", 1)[1].replace("## 5. Tag\n", "")
    if len(rehearsal_findings(outside)) != len(REHEARSAL):
        fails.append("TL-REHEARSAL passed a runbook whose rehearsal pull is outside the gates")
    return fails


def main() -> int:
    g.force_utf8()
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    guard = g.Guard("check-ticket-links", RULES)
    tasks = DOCS / "tasks.csv"
    links_file = DOCS / "adam-links.json"
    if not tasks.exists() or not links_file.exists():
        print("FAIL - handoff/service-docs/tasks.csv or adam-links.json is missing: run build-service-docs.py and "
              "adam-links.py")
        return 1
    rows = {r["key"]: r for r in csv.DictReader(tasks.open(encoding="utf-8"))}
    bundle = g.load_json(DOCS / "op-release.json", None)
    ids = {k: v for k, v in (g.load_json(DOCS / "pms-map.json", {}) or {}).items()
           if not k.startswith(("_", "VERSION")) and isinstance(v, int)}
    for k, v in ((bundle or {}).get("ids") or {}).items():
        if isinstance(v, int):
            ids.setdefault(k, v)
    links = (g.load_json(links_file, {}) or {}).get("links") or []
    block, gone = block_tickets(rows, bundle)
    for rule, key, msg in findings(block, ids, links, package_index()):
        guard.add(rule, key, msg, strict=True)
    book = g.ROOT / "docs" / "active" / "release-runbook.md"
    for rule, key, msg in rehearsal_findings(book.read_text(encoding="utf-8") if book.is_file() else ""):
        guard.add(rule, key, msg, strict=True)
    unpushed = sorted(k for k in block if k not in ids)
    kinds = defaultdict(int)
    for k in block:
        kinds[block[k]] += 1
    guard.note(f"{len(block)} Block A tickets ({', '.join(f'{n} {t.lower()}s' for t, n in sorted(kinds.items()))}), "
               f"{len(links)} links; the self-tests pass")
    if unpushed:
        guard.note(f"{len(unpushed)} planned Block A ticket(s) have no OpenProject id yet (made at the next apply, "
                   f"linked by adam-links.py after it): {', '.join(unpushed[:8])}")
    if gone:
        guard.note(f"{len(gone)} ticket(s) the last release cut in Block A are no longer in the plan (op-retire "
                   f"closes or parks them): {', '.join(gone[:8])}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
