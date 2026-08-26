#!/usr/bin/env python3
"""Check the contract backlog.

    python3 tools/check-backlog.py

`handoff/contract-backlog.json` holds every contract edit the requirement walk found and did
not make immediately. **The reason it needs a checker is that this package has already lost a
finding exactly once**: `handoff/requirement-count.md` named the 22.3 reference collision on
18 August, said in its own text that it was worth raising because it would be raised at
sign-off otherwise, and it never became a CF. A queue nobody validates becomes the same thing
at three hundred times the size.

What is checked:

  1. Ids are unique and sequential — a gap means an entry was deleted rather than withdrawn,
     and a withdrawn entry has to say why it went.
  2. Every entry names a lane, a status and a section, all from their closed sets.
  3. Every contract named exists. A backlog pointing at a contract that was renamed is a
     backlog nobody can action.
  4. `deferred` entries name what they are blocked on. Deferral without a trigger is deletion
     with extra steps.
  5. `settled` entries do **not** name a blocker, and do name a fix. That is what settled means.
  6. `decision` entries name a CF, and that CF exists in the register. This is the specific
     failure the file exists to prevent.
  7. Nothing sits `open` in the `settled` lane once its section is closed — settled edits are
     made at section close, so an open one after that is an edit that was promised and skipped.
     **Only during the reconciliation phase.** The walk runs discovery first: all 146 sections
     verdicted, nothing fixed, because the discriminator cannot be applied honestly from two
     sections — four of the ten entries open on 18 August were blocked on sections not yet
     reached. Under discovery a settled entry is meant to stay open.

Exit is non-zero on any error. Warnings do not fail the run.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "handoff" / "contract-backlog.json"
CONTRACTS = ROOT / "contracts"
REGISTER = ROOT / "docs" / "registers" / "conflicts.md"
TRACE = ROOT / "handoff" / "traceability.json"

LANES = {"settled", "deferred", "decision"}
STATUSES = {"open", "done", "withdrawn"}

ERRORS: list[str] = []
WARNINGS: list[str] = []


def main() -> int:
    if not BACKLOG.exists():
        print("no backlog — nothing to check")
        return 0

    doc = json.loads(BACKLOG.read_text(encoding="utf-8"))
    entries = doc.get("entries") or []

    contracts = {p.stem for p in CONTRACTS.rglob("*.yaml")}
    cfs = set(re.findall(r"CF-\d+[a-z]?", REGISTER.read_text(encoding="utf-8"))) \
        if REGISTER.exists() else set()

    # 1. Ids unique and sequential.
    ids = [e.get("id", "") for e in entries]
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        ERRORS.append(f"{i}: id used more than once")
    nums = sorted(int(m.group(1)) for i in ids if (m := re.fullmatch(r"BL-(\d+)", i)))
    if nums:
        for n in range(1, max(nums) + 1):
            if n not in nums:
                ERRORS.append(f"BL-{n:03d} is missing — withdraw an entry, never delete it, "
                              "because a gap does not say what happened to the edit")

    for e in entries:
        eid = e.get("id", "?")
        lane, status = e.get("lane"), e.get("status")

        # 2. Closed sets.
        if lane not in LANES:
            ERRORS.append(f"{eid}: lane {lane!r} is not one of {sorted(LANES)}")
        if status not in STATUSES:
            ERRORS.append(f"{eid}: status {status!r} is not one of {sorted(STATUSES)}")
        if not e.get("section"):
            ERRORS.append(f"{eid}: no section — an edit with no origin cannot be re-verified")
        if not e.get("refs"):
            ERRORS.append(f"{eid}: no refs — the requirement that found this must be named")

        # 3. Contracts exist.
        named = list(e.get("contracts") or []) + list(e.get("candidateHomes") or [])
        for c in named:
            if c not in contracts:
                ERRORS.append(f"{eid}: names contract {c!r}, which does not exist")
        if not named:
            ERRORS.append(f"{eid}: names no contract")

        if status != "open":
            continue

        # 4, 5. Lane obligations. **`blockedOn` was one free-text string until 18 August**, and
        # eleven entries named a section that had already closed — the check verified a blocker
        # was present and never that it was outstanding. It is now three checked lists plus a
        # prose note, and a satisfied blocker is an error rather than a lie.
        blockers = (list(e.get("blockedOnSections") or []) +
                    list(e.get("blockedOnConflicts") or []) +
                    list(e.get("blockedOnDomains") or []) +
                    ([e["blockedOnPhase"]] if e.get("blockedOnPhase") else []))
        if lane == "deferred" and not blockers:
            WARNINGS.append(f"{eid}: deferred and nothing blocks it — ready to work, or the "
                            "blocker was satisfied and never cleared")
        if lane == "settled" and blockers:
            ERRORS.append(f"{eid}: settled but blocked on {blockers} — if it is blocked it is "
                          "deferred")
            if not e.get("fix"):
                ERRORS.append(f"{eid}: settled with no fix written — settled means the edit is "
                              "known, not that it is easy")

        # 6. Decisions reach the register.
        if lane == "decision":
            cf = e.get("cf")
            if not cf:
                ERRORS.append(f"{eid}: decision lane with no CF — this is the exact failure this "
                              "file exists to prevent")
            elif cf not in cfs:
                ERRORS.append(f"{eid}: names {cf}, which is not in the conflict register")

    # 6b. A blocker must still be outstanding. A section that has closed, or a conflict that
    # has, no longer blocks anything — and an entry that says otherwise is the specific decay
    # this file was written to catch.
    closed_sections = set()
    if TRACE.exists():
        closed_sections = set(json.loads(TRACE.read_text(encoding="utf-8"))
                              .get("closedSections") or [])
    for e in entries:
        if e.get("status") != "open":
            continue
        for sec in e.get("blockedOnSections") or []:
            if sec in closed_sections:
                ERRORS.append(f"{e.get('id')}: blocked on section {sec}, which is closed — "
                              "clear the blocker or say what actually blocks it")
        for dom in e.get("blockedOnDomains") or []:
            walked = {s.split(".")[0] for s in closed_sections}
            remaining = [s for s in closed_sections if s.startswith(f"{dom}.")]
            if dom in walked and len(remaining) >= 1 and dom == "1":
                ERRORS.append(f"{e.get('id')}: blocked on domain {dom}, which is fully walked")

    # 7. Settled edits are made at section close. **Gated on the reconciliation phase.**
    # During discovery nothing is fixed by design, so every settled entry is legitimately open
    # in a closed section — firing here would report correct behaviour as a failure, and a
    # checker that cries wolf is one nobody reads.
    if doc.get("phase") == "reconciliation" and TRACE.exists():
        closed = set((json.loads(TRACE.read_text(encoding="utf-8")).get("closedSections") or []))
        for e in entries:
            if e.get("lane") == "settled" and e.get("status") == "open" \
                    and e.get("section") in closed:
                ERRORS.append(f"{e.get('id')}: settled and still open, but section "
                              f"{e.get('section')} is closed — the edit was promised and skipped")

    by_lane = {ln: sum(1 for e in entries if e.get("lane") == ln and e.get("status") == "open")
               for ln in sorted(LANES)}
    print(f"{len(entries)} entries · open: " +
          " · ".join(f"{k} {v}" for k, v in by_lane.items()))
    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    # Every row that names an entry must appear in that entry's refs.
    #
    # **The two artefacts were individually valid and collectively wrong.** A traceability row named
    # its entry, the entry named some refs, and neither was incorrect on its own terms — so nothing
    # failed while `BL-013` listed one reference and answered 35.
    #
    # The hazard is estimation, not routing. **Anyone scoping from the backlog alone understated the
    # work by roughly half**, and 754 rows were absent from the entries that answer them until
    # 18 August.
    tr = ROOT / "handoff" / "traceability.json"
    if tr.exists():
        cite: dict[str, set] = {}
        for r in json.loads(tr.read_text(encoding="utf-8"))["rows"]:
            if r.get("backlog"):
                cite.setdefault(r["backlog"], set()).add(str(r["packageRef"]))
        for eid, refs in sorted(cite.items()):
            e = next((x for x in entries if x.get("id") == eid), None)
            if not e:
                ERRORS.append(f"{eid}: named by a traceability row and not in the backlog")
                continue
            missing = refs - {str(x) for x in (e.get("refs") or [])}
            if missing:
                ERRORS.append(f"{eid}: refs array omits {len(missing)} row(s) that cite it — "
                              "an entry sized from its own refs is sized wrong")

    # A blocker must point at an OPEN conflict.
    #
    # **This happened twice on 18 August**: five entries held on CF-73, CF-118 and CF-124 after those
    # closed, and then fifteen more held on eleven conflicts closed the same afternoon — 145 rows
    # sitting behind decisions that had already been taken.
    #
    # The register check verified a blocker *existed* and never that it was outstanding, which is
    # the backlog decaying in exactly the way this apparatus exists to prevent.
    reg = ROOT / "docs" / "registers" / "conflicts.md"
    if reg.exists():
        section = ""
        closed_cfs: set = set()
        for line in reg.read_text(encoding="utf-8").split("\n"):
            if line.startswith(("## ", "### ")):
                section = line.lstrip("# ").strip()
            mm = re.match(r"^\| \*\*(CF-\d+)\*\* \|", line)
            if mm and not section.lower().startswith("open"):
                closed_cfs.add(mm.group(1))
        for e in entries:
            if e.get("status") != "open":
                continue
            for cf in (e.get("blockedOnConflicts") or []):
                if cf in closed_cfs:
                    ERRORS.append(f"{e.get('id')}: blocked on {cf}, which is closed — a blocker that "
                                  "outlives its conflict hides work that is ready")

    for x in ERRORS:
        print(f"  FAIL  {x}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
