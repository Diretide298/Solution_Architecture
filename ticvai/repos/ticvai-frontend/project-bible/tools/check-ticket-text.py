#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The ticket text a developer reads, against the package it was generated from.

**Audit classes A-TICKET-* (docs/active/root-classes.md).** The 26 September pull audit traced 29
root issues to the generated ticket text: screen tickets with no acceptance criteria beyond
"build, connect, tests" (R041), 'Used by' shorter than `x-ticvai-consumed-by` (R042), 401/403 tests
demanded where no permission applies (R054), a slice line naming fewer operations than the screen
calls (R047), onboarding tickets naming a zip with no source (R001), a reviewer who is the builder
(R058), migration Done-when that cannot hold (R046), and so on. `op-descriptions.py` and
`build-service-docs.py` were fixed in S003; nothing failed when they regressed, so this reads what
they wrote -- `handoff/service-docs/op-descriptions.json` keyed through `pms-map.json` -- and
compares it with the contracts and screens.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-ticket-text.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "T-DONE-WHEN": "a work ticket has checkable Done-when items (R041 R053 R059)",
    "T-ONBOARD-SOURCE": "onboarding says where the setup zip comes from (R001 R053)",
    "T-SETUP-REPO": "a setup task names the repository it lands in (R002 R059)",
    "T-REVIEWER": "the week's reviewer is not the builder; none on setup (R058)",
    "T-USED-BY": "'Used by' names every consumer in x-ticvai-consumed-by (R042)",
    "T-AUTH-TESTS": "no 403 test demanded where no operation has a permission (R054)",
    "T-SLICE-CALLS": "a screen ticket's Calls lines name every operation the screen calls (R047)",
    "T-WAVE": "a screen ticket's wave is the screen's wave (R045)",
    "T-PURPOSE-CUT": "a screen ticket carries the screen purpose whole, not cut (R067)",
    "T-MIG-DONE": "migration Done-when has no rollback/snapshot/V-number boilerplate (R046 R048)",
    "T-REPO-ITEMS": "backend Done-when names no frontend gate, and the reverse (R069)",
    "T-READ-ROUTING": "'reads routed to' matches x-ticvai-read-routing (R066)",
    "T-PROVISIONAL": "no provisional operation on a build ticket (R061)",
    "T-BOILERPLATE": "no sub-task/reviewer boilerplate with nothing behind it (R044)",
    "T-NONEMPTY-LABEL": "'makes <table> non-empty' only on an operation that creates rows (R064)",
    "T-SPEC-SCREEN": "a frontend spec section's route and wave match the screen record (R274)",
}

SCREEN_ID = re.compile(r"\b(?:[A-Z]{2,5})-\d{3,4}\b")
GENERIC_DONE = re.compile(r"(pnpm|dotnet|PR is reviewed|reviewed$)", re.I)


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-ticket-text", RULES)
    sd = g.ROOT / "handoff" / "service-docs"
    pms = g.load_json(sd / "pms-map.json", {}) or {}
    desc = g.load_json(sd / "op-descriptions.json", {}) or {}
    if not desc:
        guard.note("handoff/service-docs/op-descriptions.json missing - nothing to check")
        return guard.finish()
    key_of = {str(v): k for k, v in pms.items()}
    ops = g.operations()
    screens = {s["id"]: s for _, s in g.screens()}

    for oid, text in sorted(desc.items(), key=lambda kv: key_of.get(kv[0], kv[0])):
        key = key_of.get(oid, "op-" + oid)
        if "#" in key:
            # A sub-task (`KEY#build`, `KEY#<operationId>`) repeats its parent's text; the parent is
            # checked once.
            continue
        container = "\nUnder this:" in "\n" + text
        lines = text.split("\n")
        done = []
        if "## Done when" in text:
            seg = text.split("## Done when", 1)[1].split("\n## ", 1)[0]
            done = [l[6:].strip() for l in seg.split("\n") if l.startswith("- [ ]")]
        queue = re.search(r"Build order #\d+, (.+?)'s queue", text)
        builder = queue.group(1).strip() if queue else None
        reviewer = re.search(r"Reviewer that week: (.+)", text)
        reviewer = reviewer.group(1).strip() if reviewer else None
        is_setup = key.startswith("SETUP")
        is_mig = key.startswith("MIG-")
        screen_head = re.search(r"^### ([A-Z]{2,5}-\d{3,4}) ", text, re.M)
        op_heads = re.findall(r"^### `(\w+)` - `(\w+) ", text, re.M)

        # --- Done-when -------------------------------------------------------------------------
        if not container:
            specific = [d for d in done if not GENERIC_DONE.search(d)]
            has_sentence = re.search(r"\bDone when\b[:\s]", text) is not None
            if not specific and not (has_sentence and not done):
                guard.add("T-DONE-WHEN", key,
                          f"{key}: no Done-when item beyond the generic build/test/review gates")
        # --- setup and onboarding --------------------------------------------------------------
        if key.startswith("SETUP-ONBOARD"):
            if "adam-connector-setup.zip" in text and not re.search(r"(from your lead|https?://)", text):
                guard.add("T-ONBOARD-SOURCE", key, f"{key}: names adam-connector-setup.zip and not "
                                                   "where it comes from")
        elif is_setup and not container:
            if not re.search(r"\*\*ticvai-[a-z-]+\*\*|repositor", text):
                guard.add("T-SETUP-REPO", key, f"{key}: a setup task that names no repository")
        # --- reviewer -----------------------------------------------------------------------------
        if reviewer and (is_setup or (builder and reviewer == builder)):
            guard.add("T-REVIEWER", key, f"{key}: reviewer {reviewer!r} "
                      + ("on a setup ticket" if is_setup else "is the builder"))
        # --- operations on backend tickets ------------------------------------------------------
        if op_heads:
            sections = re.split(r"^### `", text, flags=re.M)[1:]
            perms = []
            for sec in sections:
                op_id = sec.split("`", 1)[0]
                facts = ops.get(op_id)
                if not facts:
                    continue
                op = facts["op"]
                perms.append(op.get("x-ticvai-permission"))
                if op.get("x-ticvai-provisional"):
                    guard.add("T-PROVISIONAL", f"{key}:{op_id}",
                              f"{key}: builds {op_id}, which is x-ticvai-provisional")
                used = re.search(r"^- \*\*Used by:\*\*(.*)$", sec, re.M)
                named = set(SCREEN_ID.findall(used.group(1))) if used else set()
                want = set()
                for entry in op.get("x-ticvai-consumed-by") or []:
                    parts = str(entry).split()
                    if len(parts) > 1 and SCREEN_ID.fullmatch(parts[1]):
                        want.add(parts[1])
                missing = sorted(want - named)
                if missing:
                    guard.add("T-USED-BY", f"{key}:{op_id}",
                              f"{key}: {op_id} 'Used by' leaves out {', '.join(missing[:6])}"
                              f"{' ...' if len(missing) > 6 else ''} ({len(missing)} of {len(want)})")
                routed = re.search(r"reads routed to (\w+)", sec)
                decl = op.get("x-ticvai-read-routing")
                if routed and decl and routed.group(1) != str(decl):
                    guard.add("T-READ-ROUTING", f"{key}:{op_id}",
                              f"{key}: {op_id} says reads routed to {routed.group(1)}; the contract "
                              f"says {decl}")
            if perms and all(p in (None, "", "null") for p in perms):
                if any("without the permission gets 403" in d for d in done):
                    guard.add("T-AUTH-TESTS", key, f"{key}: asks for a 403 test and none of its "
                                                   f"{len(perms)} operation(s) has a permission")
            for d in done:
                if re.search(r"\bpnpm\b|typecheck", d):
                    guard.add("T-REPO-ITEMS", key, f"{key}: backend Done-when names a frontend gate: {d[:80]}")
        # --- screen tickets ---------------------------------------------------------------------
        if screen_head and not container:
            sid = screen_head.group(1)
            sc = screens.get(sid)
            if sc is not None:
                calls = set()
                for l in lines:
                    if l.startswith("- **Calls"):
                        calls |= set(re.findall(r"`(\w+)`", l))
                apis = {a.get("operationId") for a in (sc.get("apis") or [])
                        if isinstance(a, dict) and a.get("operationId")}
                missing = sorted(apis - calls)
                if missing:
                    guard.add("T-SLICE-CALLS", key, f"{key}: {sid} calls {len(apis)} operations, the "
                              f"ticket names {len(apis & calls)}; missing {', '.join(missing[:5])}")
                wave = re.search(r"^- \*\*Platform:\*\*.*?; wave (\w+)", text, re.M)
                if wave and sc.get("wave") is not None and wave.group(1) != str(sc.get("wave")):
                    guard.add("T-WAVE", key, f"{key}: ticket says wave {wave.group(1)}, {sid} is "
                                             f"wave {sc.get('wave')}")
                purpose = " ".join(str(sc.get("purpose") or "").split())
                if purpose and purpose not in " ".join(text.split()):
                    guard.add("T-PURPOSE-CUT", key, f"{key}: the ticket does not carry {sid}'s "
                                                    f"purpose whole ({purpose[:60]}...)")
            for d in done:
                if re.search(r"\bdotnet\b", d):
                    guard.add("T-REPO-ITEMS", key, f"{key}: frontend Done-when names a backend gate: {d[:80]}")
        # --- migrations -------------------------------------------------------------------------
        if is_mig and not container:
            for d in done:
                if re.search(r"rollback|restored snapshot|previous release|\bV\d{3,4}\b", d, re.I):
                    guard.add("T-MIG-DONE", key, f"{key}: Done-when '{d[:80]}' cannot be held by a "
                                                 "forward-only runner")
            if re.search(r"\bV\d{3,4}(__|\b)", text):
                guard.add("T-MIG-DONE", key + ":vnumber",
                          f"{key}: names a V-number; MIGRATIONS.md numbers the files")
        # --- boilerplate ------------------------------------------------------------------------
        if re.search(r"each operation has its own sub-task", text, re.I):
            guard.add("T-BOILERPLATE", key, f"{key}: promises a sub-task per operation")

    # The spec pages the tickets link to (handoff/service-docs/backend|frontend/*.md).
    for page in sorted((sd / "backend").glob("*Service.md")):
        body = page.read_text(encoding="utf-8")
        for sec in re.split(r"^### ", body, flags=re.M)[1:]:
            op_id = sec.split("\n", 1)[0].strip().strip("`")
            f = ops.get(op_id)
            # A PUT `set*` upserts and can create the first row; an update, approval or delete cannot.
            changes_only = f and (f["method"] in ("patch", "delete") or re.match(
                r"(update|approve|reject|escalate|cancel|delete|remove|archive|close|suspend|resume|"
                r"acknowledge|withdraw|revoke|disable|deactivate)", op_id))
            if changes_only and re.search(r"makes `[^`]+` non-empty", sec):
                guard.add("T-NONEMPTY-LABEL", f"{page.name}:{op_id}",
                          f"{page.name}: {op_id} ({f['method'].upper()}) is labelled as making a table non-empty")
    for page in sorted((sd / "frontend").glob("*.md")):
        body = page.read_text(encoding="utf-8")
        for sec in re.split(r"^## ", body, flags=re.M)[1:]:
            m = re.match(r"([A-Z]{2,5}-\d{3,4}) ", sec)
            sc = screens.get(m.group(1)) if m else None
            if not sc:
                continue
            sid = m.group(1)
            route = re.search(r"^\| Route \| `([^`]*)` \|", sec, re.M)
            wave = re.search(r"^\| Wave \| (\w+) \|", sec, re.M)
            yroute = (sc.get("implementation") or {}).get("route")
            if route and yroute and route.group(1) != yroute:
                guard.add("T-SPEC-SCREEN", f"{page.name}:{sid}:route",
                          f"{page.name}: {sid} route {route.group(1)}, the screen says {yroute}")
            if wave and sc.get("wave") is not None and wave.group(1) != str(sc.get("wave")):
                guard.add("T-SPEC-SCREEN", f"{page.name}:{sid}:wave",
                          f"{page.name}: {sid} wave {wave.group(1)}, the screen says {sc.get('wave')}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
