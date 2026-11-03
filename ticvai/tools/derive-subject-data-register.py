#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write `handoff/subject-data-register.json`: every table that holds a guest's data, by the module that owns it.

**Why** (20 October 2026, r8 cause IDENTITY-C65, ticket 27750, CHG-R8GEN-015). exportSubjectData promises
"everything the platform holds" about a subject, and its contract named a hand list of Marketing tables, read raw
across deployables, and missed Identity's own personal-data tables. The fix the lead took is a register: each module
that holds subject data publishes one query, `subjectDataRecords(subjectId)`, and exportSubjectData asks each in turn.
This writes the register from the schema, so the list of tables each owner's query must cover is never typed:

    {"modules": {"MarketingService": {"contract": "marketing-crm", "tables": [...], "query": "marketing-crm#subjectDataRecords" | null,
                                       "asked": true | false}, ...},
     "missingQueries": [...], "notAsked": [...]}

A table holds subject data when it has a column naming a subject: `subject_id`, a `<role>_subject_id`, or a column
referencing pii.subject (schema-reference.json), or a field kept in pii.* for one of its rows (`personal`, from
`x-ticvai-pii`), or a column of a person's data kept on the row (`dataClass: personal`). **Not only `subject_id`** (r13 review B-01; the lead, 3 November 2026, "Move the columns";
CHG-R14M-001): keyed on that one name, the register missed the holders, recipients, participants and contacts held by
name, and 11 of 12 modules were never asked. `owners` lists the tables by the contract that persists them: each
contract's job consuming identity.privacyRequestRaised writes its part of the export (reads every one) and erases
its personal fields (check-personal-data PD-MODULE-PART and PD-MODULE-ERASE gate it). `parts` names that job.

    python tools/derive-subject-data-register.py
"""
import glob
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "handoff", "subject-data-register.json")
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
QUERY = "subjectDataRecords"
EXPORT = "exportSubjectData"
EVENT_RAISED = "identity.privacyRequestRaised"


def names_subject(c: dict) -> bool:
    """A column naming a subject: subject_id, <role>_subject_id, or a declared reference to pii.subject."""
    col = str((c or {}).get("column") or "")
    return col == "subject_id" or col.endswith("_subject_id") or (c or {}).get("references") == "pii.subject"


def owning_contract(table: str, cs: list, svc_contracts: list) -> str:
    """The contract that persists a table: pii.* is Identity's; else the contract most of its columns come from."""
    if table.startswith("pii."):
        return "identity"
    count: dict = {}
    for c in cs:
        src = str((c or {}).get("source") or "")
        if src.count(".") >= 2 and not src.startswith(("storage", "relationship")):
            count[src.split(".")[0]] = count.get(src.split(".")[0], 0) + 1
    if count:
        return max(sorted(count), key=lambda k: count[k])
    return svc_contracts[0] if svc_contracts else table.split(".")[0]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    with io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8") as fh:
        cols = json.load(fh).get("cols") or {}
    with io.open(os.path.join(ROOT, "handoff", "service-decomposition.json"), encoding="utf-8") as fh:
        services = json.load(fh).get("services") or {}
    owner = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    contracts = {s: list(v.get("contracts") or []) for s, v in services.items()}
    declared, asked = set(), set()
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        stem = os.path.basename(f)[:-5]
        with io.open(f, encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=LOADER) or {}
        qs = doc.get("x-ticvai-queries") or (doc.get("info") or {}).get("x-ticvai-queries") or {}
        names = qs.keys() if isinstance(qs, dict) else [q.get("name") for q in qs if isinstance(q, dict)]
        if QUERY in names:
            declared.add("%s#%s" % (stem, QUERY))
        for _p, item in (doc.get("paths") or {}).items():
            for _v, op in (item or {}).items() if isinstance(item, dict) else []:
                if isinstance(op, dict) and op.get("operationId") == EXPORT:
                    asked |= {str(r.get("query")) for r in op.get("x-ticvai-read-via") or [] if isinstance(r, dict)}
    with io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8") as fh:
        personal = json.load(fh).get("personal") or {}
    parts = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        stem = os.path.basename(f)[:-5]
        with io.open(f, encoding="utf-8") as fh:
            doc = yaml.load(fh, Loader=LOADER) or {}
        for name, j in (doc.get("x-ticvai-jobs") or {}).items():
            if isinstance(j, dict) and EVENT_RAISED in (j.get("consumes") or []):
                parts.setdefault(stem, "%s#%s" % (stem, name))
        for _p, item in (doc.get("paths") or {}).items():
            for _v, op in (item or {}).items() if isinstance(item, dict) else []:
                if isinstance(op, dict) and EVENT_RAISED in (op.get("x-ticvai-consumes") or []):
                    parts.setdefault(stem, "%s#%s" % (stem, op.get("operationId")))
    parts.setdefault("identity", "identity#subjectExport")
    modules, owners = {}, {}
    for t, cs in sorted(cols.items()):
        if "." not in t or ":" in t or not (t in personal or any(names_subject(c) or (c or {}).get("dataClass") ==
                                                                  "personal" for c in cs)):
            continue
        svc = owner.get(t.split(".")[0])
        if not svc:
            continue
        m = modules.setdefault(svc, {"contracts": contracts.get(svc, []), "tables": []})
        m["tables"].append(t)
        owners.setdefault(owning_contract(t, cs, m["contracts"]), []).append(t)
    for svc, m in modules.items():
        q = next(("%s#%s" % (c, QUERY) for c in m["contracts"] if "%s#%s" % (c, QUERY) in declared), None)
        m["query"] = q
        m["parts"] = sorted({parts[c] for c in m["contracts"] if c in parts and c in owners})
        m["asked"] = svc == "IdentityService" or bool(m["parts"]) or (q in asked if q else False)
    doc = {
        "note": "Generated by tools/derive-subject-data-register.py from schema-reference.json (tables with a column "
                "naming a subject, or a field kept in pii.* for its rows), service-decomposition.json and the "
                "contracts. Do not edit. Each contract in `owners` writes its part of exportSubjectData and erases its "
                "personal fields from a job consuming identity.privacyRequestRaised (`parts`; r8 cause IDENTITY-C65, "
                "r13 review B-01, CHG-R14M-001).",
        "modules": {k: modules[k] for k in sorted(modules)},
        "owners": {k: sorted(v) for k, v in sorted(owners.items())},
        "parts": {k: parts.get(k) for k in sorted(owners)},
        "missingParts": sorted(k for k in owners if not parts.get(k)),
        "missingQueries": sorted(s for s, m in modules.items() if s != "IdentityService" and not m["query"]),
        "notAsked": sorted(s for s, m in modules.items() if not m["asked"]),
    }
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    old = io.open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if old != text:
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    print("  %d table(s) hold subject data across %d module(s) and %d contract(s); %d contract(s) write no part"
          % (sum(len(m["tables"]) for m in modules.values()), len(modules), len(owners), len(doc["missingParts"])))
    print("  -> handoff/subject-data-register.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
