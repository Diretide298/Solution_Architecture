#!/usr/bin/env python3
"""Check the traceability register.

    python3 tools/check-traceability.py

`handoff/traceability.json` carries one verdict per matrix row, written during the requirement
walk. **It exists because the package could prove internal consistency and never requirement
coverage**: 778 operations all resolve, and on 18 August only 190 of 3,156 references were cited
anywhere in the contracts. The 93% in `COVERAGE.md` counted requirements whose *domain* had a
contract, which is not the same claim and was hardcoded at `build-status.py:186`.

A register asserting coverage is worth nothing unless something checks the assertions, so:

  1. Every verdict comes from the closed set.
  2. Every row names a section and a contract, and the contract exists.
  3. `CONTRACTED` and `CONTRACTED_PARTIAL` name evidence — an operationId or a schema — that
     exists in the contract they name. **This is the check that matters.** A verdict claiming
     coverage against an operation that does not exist is worse than no verdict, because it
     reads as proof.
  4. `CONTRACTED_PARTIAL` and `GAP_CONTRACT` carry a backlog entry, and it is open or done.
     A gap with no queued edit is a gap that gets lost.
  5. `GAP_DECISION` names a CF that is in the register.
  6. `ROUTED` names a class from `closed_classes.json`.
  7. `PARKED` says why.
  8. `SUPERSEDED` names a surviving reference that is itself in the register.
  9. Keys are unique on packageRef and xlsxRow together — twenty-eight references name two
     different requirements (CF-120), so the reference alone is not a key.
 10. A closed section holds a verdict for every matrix row in its range, and no row outside it.
     **Partial coverage of a section that claims to be closed is the failure this walk is for.**

Exit is non-zero on any error.
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "handoff" / "traceability.json"
BACKLOG = ROOT / "handoff" / "contract-backlog.json"
CLASSES = ROOT / "handoff" / "closed_classes.json"
REGISTER = ROOT / "docs" / "registers" / "conflicts.md"
MATRIX = ROOT / "sources" / "requirements" / "Ticvai_matrix_20260621_2.xlsx"

NEEDS_BACKLOG = {"CONTRACTED_PARTIAL", "GAP_CONTRACT"}
NEEDS_EVIDENCE = {"CONTRACTED", "CONTRACTED_PARTIAL"}

ERRORS: list[str] = []
WARNINGS: list[str] = []


def _contract_symbols() -> dict[str, set[str]]:
    """Every operationId and schema name each contract defines."""
    out: dict[str, set[str]] = {}
    for f in (ROOT / "contracts").rglob("*.yaml"):
        doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        syms = set()
        for _, methods in (doc.get("paths") or {}).items():
            for verb, op in (methods or {}).items():
                if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                    if op.get("operationId"):
                        syms.add(op["operationId"])
        syms |= set(((doc.get("components") or {}).get("schemas") or {}).keys())
        out[f.stem] = syms
    return out


def _matrix_sections() -> dict[str, set[int]]:
    """Sub-domain id to the set of xlsx rows it holds. Forward-fills the merged label columns,
    which is how the sheet is authored."""
    import openpyxl

    ws = openpyxl.load_workbook(MATRIX, data_only=True)["Funactionality "]
    out: dict[str, set[int]] = collections.defaultdict(set)
    last = ["", "", "", ""]
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        v = ["" if c is None else str(c).strip() for c in row]
        if all(x == "" for x in v):
            continue
        for k in range(4):
            if v[k] == "":
                v[k] = last[k]
            else:
                last[k] = v[k]
        if v[4]:
            out[v[2]].add(i)
    return out


def main() -> int:
    if not TRACE.exists():
        print("no traceability register — the walk has not started")
        return 0

    doc = json.loads(TRACE.read_text(encoding="utf-8"))
    rows = doc.get("rows") or []
    verdicts = set(doc.get("verdicts") or {})
    closed = set(doc.get("closedSections") or [])

    symbols = _contract_symbols()
    classes = set(json.loads(CLASSES.read_text(encoding="utf-8"))) if CLASSES.exists() else set()
    cfs = set(re.findall(r"CF-\d+[a-z]?", REGISTER.read_text(encoding="utf-8"))) \
        if REGISTER.exists() else set()
    backlog = {}
    if BACKLOG.exists():
        backlog = {e["id"]: e for e in
                   (json.loads(BACKLOG.read_text(encoding="utf-8")).get("entries") or [])}
    known_refs = {r.get("packageRef") for r in rows}

    # 9. Composite key.
    keys = [(r.get("packageRef"), r.get("xlsxRow")) for r in rows]
    for k in sorted({x for x in keys if keys.count(x) > 1}):
        ERRORS.append(f"{k[0]} row {k[1]}: appears more than once")

    for r in rows:
        ref, verdict = r.get("packageRef", "?"), r.get("verdict")
        contract = r.get("contract")

        if verdict not in verdicts:
            ERRORS.append(f"{ref}: verdict {verdict!r} is not in the closed set")
            continue
        if not r.get("section"):
            ERRORS.append(f"{ref}: no section")
        if not contract:
            ERRORS.append(f"{ref}: names no contract")
        elif contract not in symbols:
            ERRORS.append(f"{ref}: names contract {contract!r}, which does not exist")

        # 3. Evidence resolves.
        if verdict in NEEDS_EVIDENCE:
            ev = r.get("evidence")
            if not ev:
                ERRORS.append(f"{ref}: {verdict} with no evidence — a coverage claim with "
                              "nothing behind it reads as proof and is not")
            elif contract in symbols and ev not in symbols[contract]:
                ERRORS.append(f"{ref}: evidence {ev!r} is not an operation or schema in "
                              f"{contract}")

        # 4. Gaps are queued.
        if verdict in NEEDS_BACKLOG:
            bid = r.get("backlog")
            if not bid:
                ERRORS.append(f"{ref}: {verdict} with no backlog entry — a gap with no queued "
                              "edit is a gap that gets lost")
            elif bid not in backlog:
                ERRORS.append(f"{ref}: names backlog {bid}, which does not exist")
            elif backlog[bid].get("status") == "withdrawn":
                ERRORS.append(f"{ref}: {verdict} against withdrawn backlog {bid} — if the edit "
                              "was decided against, the verdict is no longer a gap")

        # 5, 6, 7, 8.
        if verdict == "GAP_DECISION":
            cf = r.get("cf")
            if not cf:
                ERRORS.append(f"{ref}: GAP_DECISION with no CF")
            elif cf not in cfs:
                ERRORS.append(f"{ref}: names {cf}, which is not in the conflict register")
        if verdict == "ROUTED":
            cls = r.get("artefactClass")
            if not cls:
                ERRORS.append(f"{ref}: ROUTED with no artefact class")
            elif classes and cls not in classes:
                ERRORS.append(f"{ref}: artefact class {cls!r} is not in closed_classes.json")
        if verdict == "PARKED" and not r.get("note"):
            ERRORS.append(f"{ref}: PARKED with no reason — parked and forgotten look identical")
        if verdict == "SUPERSEDED":
            by = r.get("supersededBy")
            if not by:
                ERRORS.append(f"{ref}: SUPERSEDED naming no surviving reference")
            elif by not in known_refs:
                ERRORS.append(f"{ref}: superseded by {by!r}, which is not in this register")

    # 10. A closed section is complete.
    if MATRIX.exists() and closed:
        try:
            sections = _matrix_sections()
        except Exception as exc:  # openpyxl absent or the sheet moved
            WARNINGS.append(f"could not read the matrix to verify section completeness: {exc}")
            sections = {}
        seen = collections.defaultdict(set)
        for r in rows:
            seen[r.get("section")].add(r.get("xlsxRow"))
        for s in sorted(closed):
            want = sections.get(s)
            if want is None:
                ERRORS.append(f"section {s} is closed but the matrix has no sub-domain {s}")
                continue
            missing, extra = want - seen[s], seen[s] - want
            if missing:
                ERRORS.append(f"section {s} is closed with {len(missing)} row(s) unwalked "
                              f"— first is xlsx {min(missing)}")
            if extra:
                ERRORS.append(f"section {s} holds {len(extra)} row(s) outside its matrix range")

    # 11. A section that was walked must have been written. **Twice on 18 August a section was
    # read, its verdicts reasoned out and reported, and never persisted** — 1.4 Product Lifecycle
    # and 2.12 Order Management both existed only as prose in a conversation until somebody
    # asked whether the domain was finished. Check 10 verifies that a *closed* section is
    # complete and says nothing about a section nobody opened, which is the harder failure to
    # see: the work was done and the artefact does not know it.
    walked = set(doc.get("walkLog") or [])
    written = {r.get("section") for r in rows}
    for sec in sorted(walked - written):
        ERRORS.append(f"section {sec} is in the walk log with no rows written — the analysis "
                      "was done and never persisted")
    for sec in sorted(written - walked):
        WARNINGS.append(f"section {sec} has rows and is not in the walk log")

    counts = collections.Counter(r.get("verdict") for r in rows)
    print(f"{len(rows)} rows walked · {len(closed)} section(s) closed")
    print("  " + " · ".join(f"{k} {v}" for k, v in counts.most_common()))
    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
