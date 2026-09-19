#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The files that look derived, are read like derived, and that nothing derives.

**Nine files in `handoff/` and `wireframes/` are inputs wearing the clothes of outputs.**
They sit beside genuinely derived artefacts, they are read by the pipeline and by the
viewer, and no tool in `tools/` writes any of them. `refresh.sh` cannot help: from its
point of view they are inputs, so it reads them and says nothing.

That is ring 4 of `docs/contract-change-runbook.md`, and on 19 September it had been
silently wrong for weeks. `handoff/service-decomposition.json` still described
**28 contracts and 378 tables** when there were 32 and 556 — with `rental` and
`accreditation` absent from it entirely — while `check-package`, `derive-diagrams`,
`derive-burst-scope` and both workbooks read it to draw the service topology, and every
checker passed.

## Why this compares hashes and not timestamps

The first cut compared each file's mtime against the newest file in `contracts/`, and it
was wrong within a minute of being written. **`link-screens-contracts.py` writes
`x-ticvai-consumed-by` back into the contracts on every refresh**, so every contract is
always newer than everything else and all nine would report stale forever.

So the comparison is against **the contracts' semantic surface**: every `operationId` and
every schema name, sorted and hashed. Back-annotation does not move it; adding an
operation does. The hash each file was last blessed against lives in
`handoff/.authored-inputs.json`, which is the front-matter idea from
`docs/regenerating-authored-docs.md` kept in one place rather than nine.

After regenerating one of these by hand, record it:

    python3 tools/check-authored-inputs.py --bless handoff/api-list.md

**This never fixes anything and it cannot.** Assigning a contract to a deployable service
is a deployment decision, not a contract fact — the same reason `derive-lineage` is
additive-only. What it does is refuse to let the staleness stay invisible.

**The list is explicit on purpose.** Detecting "has no writer" by scanning the tools for
write calls was tried first and gave eight false positives, because a write six hundred
characters from the filename is still a write. A new authored input gets added here by a
person who decided it is one.

Exits non-zero when something is stale. `--quiet` prints only the summary line.
"""
import glob
import hashlib
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "handoff", ".authored-inputs.json")

# path -> (what reads it, what being stale breaks)
AUTHORED = [
    ("handoff/service-decomposition.json",
     "check-package, derive-diagrams, derive-burst-scope, both workbooks",
     "a contract absent here is absent from the service topology, the burst scope and "
     "both workbooks - while every checker passes"),
    ("handoff/contract-backlog.json",
     "build-backlog-index -> docs/registers/contract-backlog.md",
     "the backlog lists operations that now exist"),
    ("handoff/backlog-clusters.json",
     "build-cluster-index -> docs/registers/clusters.md",
     "clusters formed before the new operations were authored"),
    ("handoff/traceability.json",
     "build-status, check-traceability",
     "matrix rows answered by new operations still read as unanswered"),
    ("handoff/api-list.md",
     "viewer lib/consumers.mjs",
     "new operations have no consuming app in the viewer"),
    ("handoff/artefact-audit.md",
     "viewer lib/decisions.mjs",
     "new handoff artefacts are unclassified"),
    ("handoff/schema-viewer-notes.md",
     "viewer lib/relationships.mjs",
     "the prose explaining the schema the viewer draws"),
    ("handoff/rag-index-sources.md",
     "check-package",
     "what the RAG index was built from"),
    ("wireframes/LINKAGE.md",
     "viewer lib/wireframes.mjs, lib/lineage.mjs",
     "the board -> screen -> operation chain"),
]

VERBS = ("get", "post", "put", "patch", "delete")


def contract_files(deployable_only=False):
    """**`contracts/shared/` is not a contract.** `common.yaml` and `permissions.yaml` are
    vocabularies every contract imports, so they count toward the surface hash but never
    toward "which contracts exist" — the first cut of this tool reported `common` and
    `permissions` as contracts missing from the service decomposition, which they are
    supposed to be."""
    out = []
    for d in ("spine", "satellite") if deployable_only else ("spine", "satellite", "shared"):
        out += sorted(glob.glob(os.path.join(ROOT, "contracts", d, "*.yaml")))
    return out


def surface():
    """Every operationId and schema name, sorted. The thing a contract edit moves and a
    back-annotation does not."""
    ops, schemas = set(), set()
    for f in contract_files():
        try:
            d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        except Exception:
            continue
        for _p, m in (d.get("paths") or {}).items():
            if not isinstance(m, dict):
                continue
            for v, op in m.items():
                if v in VERBS and isinstance(op, dict) and op.get("operationId"):
                    ops.add(op["operationId"])
        for name in ((d.get("components") or {}).get("schemas") or {}):
            schemas.add("%s:%s" % (os.path.basename(f), name))
    blob = "\n".join(sorted(ops)) + "\n--\n" + "\n".join(sorted(schemas))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest(), len(ops), len(schemas)


def load_state():
    try:
        return json.load(io.open(STATE, encoding="utf-8"))
    except Exception:
        return {}


def table_count():
    """**Counted from the contracts, not from `schema-reference.json`.**

    The derived reference counts a few synthetic and projected tables, so it reports 561
    where the contracts declare 520 — and `service-decomposition.json` is written from the
    contracts. Two artefacts that each count tables their own way disagree forever, and
    the one doing the checking should count the way the one being checked does.
    """
    t = set()
    # `deployable_only`: contracts/shared/ declares one table, and the
    # decomposition counts only what a service owns.
    for f in contract_files(deployable_only=True):
        try:
            d = yaml.safe_load(io.open(f, encoding="utf-8")) or {}
        except Exception:
            continue
        for _n, sc in ((d.get("components") or {}).get("schemas") or {}).items():
            p = (sc or {}).get("x-ticvai-persistence")
            if isinstance(p, str) and "." in p and not p.startswith("none"):
                for part in p.split("+"):
                    part = part.strip()
                    if "." in part:
                        t.add(part)
    return len(t)


def check_decomposition(problems):
    """**`service-decomposition.json` states its own scope in prose, so it can be tested.**

    Its note opens "How N contracts and M tables become 16 deployable services". A file
    saying 28 when there are 32 is not a judgement call about freshness - it is wrong about
    something countable."""
    p = os.path.join(ROOT, "handoff", "service-decomposition.json")
    if not os.path.exists(p):
        return
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception as e:
        problems.append(("handoff/service-decomposition.json", "unreadable: %s" % e))
        return
    m = re.search(r"(\d+)\s+contracts?\s+and\s+(\d+)\s+tables?", str(d.get("note") or ""))
    if m:
        have_c = len(contract_files(deployable_only=True))
        have_t = table_count()
        if int(m.group(1)) != have_c:
            problems.append(("handoff/service-decomposition.json",
                             "its note says %s contracts; there are %d"
                             % (m.group(1), have_c)))
        if have_t and int(m.group(2)) != have_t:
            problems.append(("handoff/service-decomposition.json",
                             "its note says %s tables; there are %d" % (m.group(2), have_t)))

    blob = json.dumps(d).lower()
    unknown = [os.path.basename(c)[:-5]
               for c in contract_files(deployable_only=True)
               if os.path.basename(c)[:-5].lower() not in blob]
    if unknown:
        problems.append(("handoff/service-decomposition.json",
                         "no mention of %d contract(s): %s"
                         % (len(unknown), ", ".join(sorted(unknown)))))


def main():
    argv = sys.argv[1:]
    quiet = "--quiet" in argv
    h, n_ops, n_schemas = surface()
    state = load_state()

    if "--bless" in argv:
        targets = [a for a in argv[argv.index("--bless") + 1:] if not a.startswith("--")]
        known = {rel for rel, _r, _b in AUTHORED}
        for t in targets:
            t = t.replace("\\", "/")
            if t not in known:
                print("not an authored input: %s" % t)
                return 2
            state[t] = h
        io.open(STATE, "w", encoding="utf-8").write(json.dumps(state, indent=1))
        print("blessed %d file(s) against contract surface %s" % (len(targets), h[:12]))
        return 0

    stale, problems = [], []
    for rel, readers, breaks in AUTHORED:
        if not os.path.exists(os.path.join(ROOT, rel)):
            problems.append((rel, "missing"))
            continue
        was = state.get(rel)
        if was != h:
            stale.append((rel, readers, breaks, "never recorded" if not was else was[:12]))

    check_decomposition(problems)

    if not quiet:
        print("contract surface: %s  (%d operations, %d schemas, %d contracts)"
              % (h[:12], n_ops, n_schemas, len(contract_files(deployable_only=True))))
        print()
        for rel, readers, breaks, was in stale:
            print("  STALE  %-38s written against %s" % (rel, was))
            print("         read by %s" % readers)
            print("         %s" % breaks)
        for rel, why in problems:
            print("  ISSUE  %-38s %s" % (rel, why))
        if stale or problems:
            print()
            print("  These are authored. Nothing in tools/ rebuilds them and refresh.sh cannot.")
            print("  See docs/regenerating-authored-docs.md for the per-file prompts, and")
            print("  --bless <path> once a file has been brought up to date.")

    n = len(stale) + len(problems)
    print("%s - %d stale, %d issue(s), %d authored input(s) checked"
          % ("FAIL" if n else "PASS", len(stale), len(problems), len(AUTHORED)))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
