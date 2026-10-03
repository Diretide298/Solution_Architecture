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


def builds_of(r, part, lineage):
    """The artefact ids a ticket builds, as ADAM names them: operation contract#operationId, table schema.name,
    screen id, service. Setup, onboarding and AI tasks build nothing ADAM indexes by id: their key is enough."""
    def op_id(op):
        c = lineage.get(op, {}).get("contract")
        return f"{c}#{op}" if c else op

    if r["type"] == "Task" and r["track"] == "Backend" and part in ("", "build", "wire", "test"):
        m, k = BE_SCREEN.match(r["subject"] or ""), SCREEN.search(r["key"])
        if m and k and k.group(1) == m.group(1):
            return [f"screen {m.group(1)}"]
    if r["type"] == "Task" and r["track"] == "Backend":
        ops = [part] if part else (r["subject"].split(": ", 1)[1].split(", ") if ": " in r["subject"] else [])
        return [f"operation {op_id(op)}" for op in ops]
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
        return "Done when " + " ".join(m.group(1).split())[:700]
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
