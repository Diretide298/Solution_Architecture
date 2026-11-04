#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The files that look derived, are read like derived, and that nothing derives.

**Seven files in `handoff/` are inputs wearing the clothes of outputs.** There were nine until
19 September, when `api-list.md` and `wireframes/LINKAGE.md` turned out to be pure derivations
and became `tools/build-api-list.py` and `tools/build-linkage.py`. **That is the preferred fix**:
a file that can be generated should be, and only what genuinely needs a person stays on this list.
They sit beside derived artefacts, they are read by the pipeline and by the viewer, and no tool
in `tools/` writes any of them, so `refresh.sh` reads them and says nothing (ring 4 of
`docs/contract-change-runbook.md`).

## One test per file, about what that file describes (3 November 2026, r14 lane i)

**Until r14 every file was compared with one hash of the whole contract surface** (every
operationId and schema name). Any new operation anywhere made all seven stale, so all seven were
allowlisted in `tools/refresh-safe-baseline.json` for a month while four of them really were
wrong (review E-02): `contract-backlog.json` held two entries open whose operations had existed
since 29 September, `rag-index-sources.md` named a column `marketing.case` does not have,
`schema-viewer-notes.md` described edge kinds the deriver had stopped emitting, and
`artefact-audit.md` counted 89 gap rows when there were none. **A test that is always red is
read as noise, and noise is what the four hid in.**

So each file now gets two kinds of test, and both must pass:

  computed   Rules the file can be held to mechanically: every operation, schema, table,
             column and event it names exists; every count it states as current is the count;
             every deployable contract is assigned once; no open backlog entry proposes an
             operation that already exists. These can never be blessed away.
  described  A hash of **only the part of the package the file is about** (the deployable
             contracts and the schemas they write, for the service decomposition; the IndexSource
             model, for the RAG register; the contracts the open gaps are in, for the backlog and
             the matrix). It moves when that part moves and not otherwise, and `--bless` records
             it once a person has re-read the file against the change. The diff is printed, so the
             re-read is of the operations that arrived, not of the whole file.

**A count written into authored prose must carry its date** ("on 3 November 2026", "at r13").
An undated count claims to be current, and that is the claim that went stale for a month.

    python3 tools/check-authored-inputs.py                 the check (self-tests first)
    python3 tools/check-authored-inputs.py --self-test     only the self-tests
    python3 tools/check-authored-inputs.py --bless <path>  record a re-read file's described part
    python3 tools/check-authored-inputs.py --quiet         the verdict line only

**`--bless` refuses a file whose computed tests fail.** Blessing records that a person read the
file against the change; it cannot make a wrong file right, and assigning a contract to a
deployable service is still a decision a person makes, not a fact this tool can find.

**A contract or event that does not parse is a reported problem**, never a skipped file (review
E-07: missing inputs become passes). So is a missing input any test reads.

The list is explicit on purpose. Detecting "has no writer" by scanning the tools for write calls
gave eight false positives. A new authored input is added here by a person who decided it is one.
"""
import collections
import copy
import csv
import datetime
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile

import yaml

# The C loader where PyYAML has one: the contracts are 16 MB and the pure-Python loader takes most
# of 30 seconds over them. Same safe subset either way.
YAML_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "handoff", ".authored-inputs.json")

# path -> (what reads it, what being wrong breaks)
AUTHORED = [
    ("handoff/service-decomposition.json",
     "check-package, derive-diagrams, derive-burst-scope, derive-service-counts, both workbooks",
     "a contract absent here is absent from the service topology, the burst scope and both "
     "workbooks - while every checker passes"),
    ("handoff/contract-backlog.json",
     "build-backlog-index -> docs/registers/contract-backlog.md, check-traceability",
     "the backlog lists as open gaps that operations already close"),
    ("handoff/backlog-clusters.json",
     "build-cluster-index -> docs/registers/clusters.md",
     "an entry in no cluster is missing from the register; a cluster's counts misstate it"),
    ("handoff/traceability.json",
     "build-status, check-traceability",
     "matrix rows answered by new operations still read as unanswered"),
    ("handoff/artefact-audit.md",
     "viewer lib/decisions.mjs",
     "the viewer reports artefact classes as missing that exist, and gaps that are closed"),
    ("handoff/schema-viewer-notes.md",
     "viewer lib/decisions.mjs (handoff documents)",
     "the prose explaining the schema graph the viewer draws"),
    ("handoff/rag-index-sources.md",
     "check-package",
     "what the RAG index is built from"),
]

VERBS = ("get", "post", "put", "patch", "delete")
MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|"
          "December")
DATED = re.compile(r"\b\d{1,2}\s+(?:%s)\b|\b(?:%s)\s+\d{1,2}\b|\br\d+\b|\b\d{4}-\d\d-\d\d\b"
                   % (MONTHS, MONTHS))
COUNT = re.compile(r"\b\d[\d,]*\s+(?:of\s+(?:the\s+)?[\d,]+\s+)?(?:\w+\s+)?"
                   r"(?:operations?|tables?|contracts?|edges?|events?)\b")
TICK = re.compile(r"(~~)?`([^`\n]+)`(~~)?")


def sha(lines):
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def snake(s):
    return re.sub(r"([A-Z])", lambda m: "_" + m.group(1).lower(), s)


# ---------------------------------------------------------------- facts --

class Facts(object):
    """Everything the per-file tests read, loaded once. **A file that does not parse is a
    problem in `self.problems`**, never a silent skip: before r14 `surface()` did
    `except Exception: continue`, so a broken contract shrank the surface and passed."""

    def __init__(self, root=ROOT):
        self.root = root
        self.problems = []
        self.contracts = {}          # name -> parsed doc
        self.kind = {}               # name -> deployable | vocabulary | device
        self.ops = {}                # operationId -> contract
        self.op_doc = {}             # operationId -> operation object
        self.schemas = collections.defaultdict(set)    # Schema -> contracts
        self.sprops = collections.defaultdict(set)     # Schema -> property names
        self.senum = collections.defaultdict(set)      # Schema or Schema.prop -> enum values
        self.props, self.enums, self.params = set(), set(), set()
        self.persist = collections.defaultdict(set)    # contract -> schemas it persists into
        self._raw = {}
        self.jobs = set()            # x-ticvai-jobs and x-ticvai-queries keys a contract declares
        self._contracts()
        self._compose()
        self._events()
        self._handoff()

    def _rel(self, path):
        return os.path.relpath(path, self.root).replace("\\", "/")

    def _load_yaml(self, path):
        try:
            with io.open(path, encoding="utf-8") as fh:
                return yaml.load(fh, Loader=YAML_LOADER) or {}
        except Exception as e:
            self.problems.append((self._rel(path),
                                  "does not parse: %s" % str(e).splitlines()[0][:160]))
            return None

    def _load_json(self, rel, need=True):
        p = os.path.join(self.root, rel)
        if not os.path.exists(p):
            if need:
                self.problems.append((rel, "missing - a test that reads it cannot run"))
            return None
        try:
            with io.open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception as e:
            self.problems.append((rel, "does not parse: %s" % e))
            return None

    def _walk(self, n):
        if isinstance(n, dict):
            for k, v in n.items():
                if k == "properties" and isinstance(v, dict):
                    self.props.update(v.keys())
                if k == "enum" and isinstance(v, list):
                    self.enums.update(str(x) for x in v)
                if k == "parameters" and isinstance(v, list):
                    self.params.update(p.get("name") for p in v
                                       if isinstance(p, dict) and p.get("name"))
                self._walk(v)
        elif isinstance(n, list):
            for x in n:
                self._walk(x)

    def _contracts(self):
        files = sorted(glob.glob(os.path.join(self.root, "contracts", "*", "*.yaml")))
        if not files:
            self.problems.append(("contracts/", "no contract files found"))
        for f in files:
            d = self._load_yaml(f)
            if d is None:
                continue
            folder = os.path.basename(os.path.dirname(f))
            name = os.path.basename(f)[:-5]
            tier = str((d.get("info") or {}).get("x-ticvai-tier") or "")
            if folder in ("spine", "satellite") and tier != "device":
                self.kind[name] = "deployable"
            elif folder == "shared":
                self.kind[name] = "vocabulary"
            elif folder == "devices" or tier == "device":
                # A device host's localhost API (ADAM CR-463): no tenant, no table, no service.
                self.kind[name] = "device"
            else:
                self.problems.append((self._rel(f), "a contract folder this check does not "
                                      "know - say whether it is deployable, a vocabulary or a "
                                      "device API"))
                continue
            self.contracts[name] = d
            self.jobs |= set(d.get("x-ticvai-jobs") or {}) | set(d.get("x-ticvai-queries") or {})
            for _p, m in (d.get("paths") or {}).items():
                if not isinstance(m, dict):
                    continue
                for v, op in m.items():
                    if v in VERBS and isinstance(op, dict) and op.get("operationId"):
                        self.ops[op["operationId"]] = name
                        self.op_doc[op["operationId"]] = op
            for sname, s in ((d.get("components") or {}).get("schemas") or {}).items():
                self.schemas[sname].add(name)
                self._raw.setdefault(sname, []).append(s)
                if not isinstance(s, dict):
                    continue
                if isinstance(s.get("enum"), list):
                    self.senum[sname].update(str(x) for x in s["enum"])
                for pn, pv in (s.get("properties") or {}).items():
                    self.sprops[sname].add(pn)
                    if isinstance(pv, dict) and isinstance(pv.get("enum"), list):
                        self.senum[sname + "." + pn].update(str(x) for x in pv["enum"])
                m2 = re.match(r"^([a-z_]+)\.[a-z_]+", str(s.get("x-ticvai-persistence") or ""))
                if m2:
                    self.persist[name].add(m2.group(1))
            self._walk(d)
        self.deployable = sorted(c for c, k in self.kind.items() if k == "deployable")

    def _compose(self):
        """A schema built with `allOf` (or a `$ref` to another) has the properties of its parts:
        `ReportDefinition` and `SeatMap` declare none of their own."""
        def props_of(node, seen):
            out = set()
            if not isinstance(node, dict):
                return out
            out |= set((node.get("properties") or {}).keys())
            ref = node.get("$ref")
            if isinstance(ref, str) and "#/components/schemas/" in ref:
                tgt = ref.rsplit("/", 1)[1]
                if tgt not in seen:
                    seen.add(tgt)
                    for raw in self._raw.get(tgt, []):
                        out |= props_of(raw, seen)
            for k in ("allOf", "oneOf", "anyOf"):
                for part in node.get(k) or []:
                    out |= props_of(part, seen)
            return out
        for sname, raws in self._raw.items():
            for raw in raws:
                self.sprops[sname] |= props_of(raw, {sname})

    def _events(self):
        self.events = {}             # name -> (file stem, doc)
        self.event_stems, self.event_fields = set(), set()
        files = sorted(glob.glob(os.path.join(self.root, "events", "*.yaml")))
        if not files:
            self.problems.append(("events/", "no event files found"))
        for f in files:
            if os.path.basename(f) == "_schema.yaml":
                continue
            d = self._load_yaml(f)
            if d is None:
                continue
            stem = os.path.basename(f)[:-5]
            self.event_stems.add(stem)
            if d.get("name"):
                self.events[d["name"]] = (stem, d)
            for p in d.get("payload") or []:
                if isinstance(p, dict) and p.get("field"):
                    self.event_fields.add(p["field"])

    def _handoff(self):
        S = self._load_json("handoff/schema-reference.json") or {}
        self.cols = {t: [c.get("column") for c in v] for t, v in (S.get("cols") or {}).items()}
        self.storage = set(S.get("storage") or {})
        self.stores = set(S.get("module") or {}) | set(S.get("store") or {})
        self.tables = sorted(t for t in self.cols if "." in t and ":" not in t)
        self.all_tables = set(self.cols) | self.storage
        self.colnames = {c for v in self.cols.values() for c in v}
        # The keys a column record carries (`referenceHow`, `references`) are names a document
        # about the schema reference may cite.
        self.colkeys = {k for v in (S.get("cols") or {}).values() for c in v for k in c}
        self.shortnames = {t.split(".", 1)[1] for t in self.all_tables if "." in t}
        self.lineage = self._load_json("handoff/api-data-lineage.json") or {}
        self.backlog = {e.get("id"): e for e in
                        ((self._load_json("handoff/contract-backlog.json") or {})
                         .get("entries") or [])}
        self.trace = self._load_json("handoff/traceability.json") or {}
        self.closed_classes = self._load_json("handoff/closed_classes.json") or []
        rp = os.path.join(self.root, "handoff", "relationships.csv")
        self.rels = []
        if os.path.exists(rp):
            with io.open(rp, encoding="utf-8") as fh:
                rd = csv.DictReader(fh)
                self.rels = list(rd)
                self.colkeys |= set(rd.fieldnames or [])
        else:
            self.problems.append(("handoff/relationships.csv",
                                  "missing - run tools/derive-relationships.py"))
        reg = os.path.join(self.root, "docs", "registers", "conflicts.md")
        self.cf_rows = {}
        if os.path.exists(reg):
            for line in io.open(reg, encoding="utf-8").read().splitlines():
                m = re.match(r"^\|\s*\*\*(CF-\d+[a-z]?)\*\*\s*\|", line)
                if m:
                    self.cf_rows[m.group(1)] = line
        else:
            self.problems.append(("docs/registers/conflicts.md", "missing"))

    # ---- name resolution --------------------------------------------------

    def resolves(self, tok):
        """Whether a name written in backticks is something the package has: an operation, a
        schema or one of its properties or enum values, a table or table.column, an event, an
        event's file or payload field, a contract, or `contract.<any of those>`."""
        t = tok.strip().strip(".")
        if t.endswith("()"):
            t = t[:-2]
        if not t:
            return True
        if t in self.ops or t in self.schemas or t in self.events or t in self.all_tables:
            return True
        if t in self.contracts or t in self.event_stems or t in self.stores or t in self.jobs:
            return True
        parts = t.split(".")
        if len(parts) == 1:
            return (t in self.props or t in self.enums or t in self.params or t in self.colkeys
                    or t in self.colnames or t in self.event_fields or t in self.shortnames)
        base = ".".join(parts[:2])
        if base in self.cols and len(parts) == 3:
            return parts[2] in self.cols[base] or snake(parts[2]) in self.cols[base]
        if parts[0] in self.contracts:
            rest = ".".join(parts[1:])
            # `orders.shift` is not a name because `shift` is also a contract.
            return rest not in self.contracts and self.resolves(rest)
        if parts[0] in self.event_stems:
            return all(p in self.event_fields for p in parts[1:])
        if parts[0] in self.schemas:
            if len(parts) == 2 and parts[1] in self.senum.get(parts[0], ()):
                return True
            if parts[1] in self.sprops[parts[0]]:
                if len(parts) == 2:
                    return True
                return (parts[2] in self.props or parts[2] in self.enums
                        or parts[2] in self.senum.get(parts[0] + "." + parts[1], ()))
            return False
        return False


SKIP_TOKEN = re.compile(r"^(CF|BL|CL|ADR|CHG|BO|CMS|VC|KSK|POS|AIP|AIR|AIC|DM|REV3|D)-?\d", re.I)


def names_in(text):
    """Backticked names a file asserts exist. ~~`struck`~~ marks a historical name the file
    says no longer exists, and is skipped. Paths, commands, numbers, `x-` keys, verdict words
    and register ids are not package names, nor is a bare lowercase word."""
    out = []
    for m in TICK.finditer(text or ""):
        if m.group(1) and m.group(3):
            continue
        tok = m.group(2).strip()
        if not re.match(r"^[A-Za-z_][\w.\-]*(\(\))?$", tok):
            continue
        if tok.startswith("x-") or re.match(r"^[A-Z0-9_]+$", tok) or SKIP_TOKEN.match(tok):
            continue
        if re.search(r"\.(md|json|yaml|py|sh|csv|sql|mjs|html|xlsx|txt|pdf)$", tok):
            continue
        if not re.search(r"[A-Z_.]", tok):
            continue
        out.append(tok)
    return out


def unresolved(facts, text):
    return sorted({t for t in names_in(text) if not facts.resolves(t)})


def undated_counts(text):
    """Sentences stating a count of operations, tables, contracts, edges or events with no
    date in them. Backticked spans are ignored."""
    bad = []
    plain = re.sub(r"`[^`]*`", "", text or "")
    for sent in re.split(r"(?<=[.!?])\s+|\n\n", plain):
        if COUNT.search(sent) and not DATED.search(sent):
            bad.append(sent.strip()[:110])
    return bad


def strip_md(s):
    return re.sub(r"[*`]", "", s or "").strip()


def md_tables(text):
    """Pipe tables as lists of cell lists, header first."""
    out, cur = [], []
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not all(re.match(r"^:?-+:?$", c) for c in cells if c):
                cur.append(cells)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def contract_parts(facts, names):
    """Per contract: its operations (kept verbatim, so the diff names what arrived) and its
    schema shapes (hashed)."""
    out = {}
    for c in names:
        out["ops:%s" % c] = sorted(o for o, k in facts.ops.items() if k == c)
        out["shapes:%s" % c] = sorted("%s.%s" % (s, p) for s, cs in facts.schemas.items()
                                      if c in cs for p in (facts.sprops.get(s) or [""]))
    return out


# ------------------------------------------------- service-decomposition --

def sd_described(facts, D):
    """The deployable contracts, the schemas each persists into, and every schema there is."""
    out = ["contract %s -> %s" % (c, ",".join(sorted(facts.persist.get(c, ()))))
           for c in facts.deployable]
    out += ["schema %s" % s for s in sorted({t.split(".", 1)[0] for t in facts.tables})]
    return {"set:deployables": out}


def sd_derived(facts, D):
    """Same arithmetic as tools/derive-service-counts.py, so a file that tool would restate
    fails here rather than passing until the next --apply."""
    services = D.get("services") or {}
    own_s, own_c = {}, {}
    for name, sv in services.items():
        for s in sv.get("schemas") or []:
            own_s[s] = name
        for c in sv.get("contracts") or []:
            own_c[c] = name
    ops = collections.Counter(own_c[v.get("contract")] for v in facts.lineage.values()
                              if v.get("contract") in own_c)
    tabs = collections.Counter(own_s[t.split(".", 1)[0]] for t in facts.tables
                               if t.split(".", 1)[0] in own_s)
    reads = collections.defaultdict(collections.Counter)
    writes = collections.defaultdict(collections.Counter)
    for v in facts.lineage.values():
        me = own_c.get(v.get("contract"))
        if not me:
            continue
        for key, sink in (("reads", reads), ("writes", writes)):
            hit = set()
            for t in v.get(key) or []:
                if "." not in t or ":" in t:
                    continue
                o = own_s.get(t.split(".", 1)[0])
                if o and o != me:
                    hit.add(o)
            for o in hit:
                sink[me][o] += 1
    out = []
    for name, sv in sorted(services.items()):
        if sv.get("operations") != ops[name]:
            out.append("%s operations says %s; derived %d" % (name, sv.get("operations"), ops[name]))
        if sv.get("tables") != tabs[name]:
            out.append("%s tables says %s; derived %d" % (name, sv.get("tables"), tabs[name]))
        for field, src in (("readsFrom", reads), ("writesOutside", writes)):
            if (sv.get(field) or {}) != dict(src[name]):
                out.append("%s %s disagrees with the lineage" % (name, field))
    want = ("How %d contracts and %d tables become %d modules, deployed as %d units."
            % (len(own_c), len(facts.tables), len(services), len(D.get("deployables") or {})))
    if not str(D.get("note") or "").startswith(want):
        out.append("its note does not open %r" % want)
    return ["derived fields stale (run tools/derive-service-counts.py --apply): " + o for o in out]


def sd_test(facts, D):
    out = []
    services = D.get("services") or {}
    where = collections.defaultdict(list)
    for name, sv in services.items():
        for c in sv.get("contracts") or []:
            where[c].append(name)
            if facts.kind.get(c) != "deployable":
                out.append("%s names contract %r, which is not a deployable contract" % (name, c))
        if sv.get("deployable") not in (D.get("deployables") or {}):
            out.append("%s ships in deployable %r, which `deployables` does not define"
                       % (name, sv.get("deployable")))
        if sv.get("tier") not in (D.get("tiers") or {}):
            out.append("%s has tier %r, which `tiers` does not define" % (name, sv.get("tier")))
    for c in facts.deployable:
        if not where.get(c):
            out.append("deployable contract %r is assigned to no service - a deployment decision "
                       "for a person (derive-lineage NEW_CONTRACT_SERVICE holds the working "
                       "assumption)" % c)
        elif len(where[c]) > 1:
            out.append("contract %r is assigned to %s" % (c, " and ".join(where[c])))
    owner = collections.defaultdict(list)
    for name, sv in services.items():
        for s in sv.get("schemas") or []:
            owner[s].append(name)
    for s in sorted({t.split(".", 1)[0] for t in facts.tables}):
        if not owner.get(s):
            out.append("schema %r has tables and no owning service" % s)
        elif len(owner[s]) > 1:
            out.append("schema %r is owned by %s" % (s, " and ".join(owner[s])))
    for s in owner:
        if not any(t.startswith(s + ".") for t in facts.tables) \
                and not any(x.startswith(s + ":") for x in facts.stores):
            out.append("schema %r is owned and holds no table or store" % s)
    out += sd_derived(facts, D)
    for name, sv in sorted(services.items()):
        for f, v in sorted(sv.items()):
            if isinstance(v, str) and f not in ("tier", "deployable"):
                for s in undated_counts(v):
                    out.append("%s.%s states an undated count: %r" % (name, f, s))
                for t in unresolved(facts, v):
                    out.append("%s.%s names `%s`, which does not exist" % (name, f, t))
    note = str(D.get("note") or "")
    for s in undated_counts(note.split(".", 1)[1] if "." in note else ""):
        out.append("note states an undated count: %r" % s)
    for t in unresolved(facts, note):
        out.append("note names `%s`, which does not exist" % t)
    return out


# ---------------------------------------------------- contract-backlog --

BLOCKERS = ("blockedOnSections", "blockedOnConflicts", "blockedOnDomains", "blockedOnPhase")


def delegated(e):
    return "traceability.json" in str(e.get("fix") or "")


def cb_described(facts, B):
    """The contracts the open gaps are in. An entry whose fix delegates to traceability.json
    rows is tested against those rows instead (the rows carry their own described part)."""
    return contract_parts(facts, sorted({c for e in B.get("entries") or []
                                         if e.get("status") == "open" and not delegated(e)
                                         for c in e.get("contracts") or []}))


def cb_test(facts, B):
    out = []
    rows_by = collections.defaultdict(list)
    for r in facts.trace.get("rows") or []:
        if r.get("backlog"):
            rows_by[r["backlog"]].append(r)
    for e in B.get("entries") or []:
        i, st = e.get("id"), e.get("status")
        if st not in (B.get("statuses") or ["open", "done", "withdrawn"]):
            out.append("%s has status %r" % (i, st))
        for c in e.get("contracts") or []:
            if c not in facts.contracts:
                out.append("%s names contract %r, which does not exist" % (i, c))
        if st != "open":
            continue
        for f in ("what", "why", "blockedNote"):
            for t in unresolved(facts, e.get(f)):
                out.append("%s %s names `%s`, which does not exist" % (i, f, t))
        for tok in names_in(str(e.get("fix") or "")):
            if "." not in tok and tok in facts.ops:
                out.append("%s is open and its fix proposes `%s`, which exists in %s - close "
                           "it or say what is still missing" % (i, tok, facts.ops[tok]))
            elif "." in tok and not facts.resolves(tok):
                out.append("%s fix names `%s`, which does not exist" % (i, tok))
        for tok in e.get("proposes") or []:
            if tok in facts.ops:
                out.append("%s proposes %s, which exists in %s" % (i, tok, facts.ops[tok]))
        blocked = e.get("lane") == "decision" or any(e.get(k) for k in BLOCKERS)
        rows = rows_by.get(i) or []
        if rows and not blocked and all(r.get("verdict") == "CONTRACTED" for r in rows):
            out.append("%s is open, blocked on nothing, and all %d of its matrix rows are "
                       "CONTRACTED - a closed gap still read as open" % (i, len(rows)))
        if delegated(e) and not any(r.get("verdict") in ("CONTRACTED_PARTIAL", "GAP_CONTRACT")
                                    for r in rows):
            out.append("%s delegates to traceability rows and none of them is still partial" % i)
    return out


# ---------------------------------------------------- backlog-clusters --

def bc_described(facts, C):
    """Each backlog entry's `what`: a rewritten entry may no longer belong in its cluster."""
    return {"set:entries": sorted("%s %s" % (i, sha([str(e.get("what"))])[:10])
                                  for i, e in facts.backlog.items())}


def bc_test(facts, C):
    out = []
    covered = set(C.get("unclustered") or [])
    for x in C.get("clusters") or []:
        ids = x.get("entries") or []
        for i in ids:
            if i not in facts.backlog:
                out.append("%s names %s, which is not in the backlog" % (x.get("id"), i))
        ents = [facts.backlog[i] for i in ids if i in facts.backlog]
        covered |= set(ids)
        want = {"entryCount": len(ids),
                "rowCitations": sum(len(e.get("refs") or []) for e in ents),
                "lanes": sorted({e.get("lane") for e in ents}),
                "contracts": sorted({c for e in ents for c in e.get("contracts") or []})}
        for k, v in want.items():
            if x.get(k) != v:
                out.append("%s %s says %r; its entries give %r" % (x.get("id"), k, x.get(k), v))
        for cf in re.findall(r"CF-\d+[a-z]?", str(x.get("conflicts") or "")):
            if facts.cf_rows and cf not in facts.cf_rows:
                out.append("%s names %s, which is not in the conflict register" % (x.get("id"), cf))
        for f in ("what", "why"):
            for t in unresolved(facts, x.get(f)):
                out.append("%s %s names `%s`, which does not exist" % (x.get("id"), f, t))
    for i in sorted(set(facts.backlog) - covered):
        out.append("backlog %s is in no cluster and not in `unclustered`" % i)
    for i in sorted(set(C.get("unclustered") or []) - set(facts.backlog)):
        out.append("unclustered names %s, which is not in the backlog" % i)
    return out


# ---------------------------------------------------------- traceability --

def tr_described(facts, T):
    """The contracts the rows that are not CONTRACTED are in: the only change that can answer
    one of them."""
    return contract_parts(facts, sorted({r.get("contract") for r in T.get("rows") or []
                                         if r.get("verdict") != "CONTRACTED"
                                         and r.get("contract")}))


def tr_test(facts, T):
    out = []
    syms = collections.defaultdict(set)
    for o, c in facts.ops.items():
        syms[c].add(o)
    for s, cs in facts.schemas.items():
        for c in cs:
            syms[c].add(s)
    for r in T.get("rows") or []:
        ref, v, c = r.get("packageRef"), r.get("verdict"), r.get("contract")
        if c not in facts.contracts:
            out.append("%s names contract %r, which does not exist" % (ref, c))
            continue
        if v in ("CONTRACTED", "CONTRACTED_PARTIAL") and r.get("evidence") not in syms[c]:
            out.append("%s evidence %r is not an operation or schema in %s"
                       % (ref, r.get("evidence"), c))
        if v in ("CONTRACTED_PARTIAL", "GAP_CONTRACT"):
            b = facts.backlog.get(r.get("backlog"))
            if b and b.get("status") == "done" and not r.get("cf"):
                out.append("%s is %s against %s, which is done, and names no decision that keeps "
                           "it partial - closed, or a gap with no open entry"
                           % (ref, v, r.get("backlog")))
        for t in unresolved(facts, r.get("note")):
            out.append("%s note names `%s`, which does not exist" % (ref, t))
    return out


# --------------------------------------------------------- artefact-audit --

def class_holds(facts):
    """What the package holds per artefact class, counted the way the file's 'How to re-derive'
    section says. The file's figure is dated and may be lower; it may never be higher."""
    perms = set()
    for op in facts.op_doc.values():
        p = op.get("x-ticvai-permission")
        perms.update([p] if isinstance(p, str) else [str(x) for x in (p or [])])
    states = [f for f in glob.glob(os.path.join(facts.root, "states", "*.yaml"))
              if not f.endswith("_schema.yaml")]
    vec = 0
    pv = os.path.join(facts.root, "docs", "architecture", "specs", "permission-vectors.json")
    try:
        vec = len(json.load(io.open(pv, encoding="utf-8")).get("vectors") or [])
    except Exception:
        facts.problems.append(("docs/architecture/specs/permission-vectors.json", "unreadable"))
    return {"report": sum(1 for c in facts.ops.values() if c == "reporting"),
            "permission / role": len(perms), "state model": len(states),
            "event / async": len(facts.events),
            "device / hardware": len(facts.senum.get("DeviceKind") or ()),
            "test / acceptance": vec}


def aa_described(facts, text):
    """The closed-class list and every conflict row the file cites: a CF closing or reopening
    changes what the file should say about its class."""
    return {"set:closed-classes": sorted(facts.closed_classes),
            "cfs": ["%s %s" % (cf, sha([facts.cf_rows.get(cf, "absent")])[:12])
                    for cf in sorted(set(re.findall(r"CF-\d+[a-z]?", text)))]}


def aa_test(facts, text):
    out = []
    rows = facts.trace.get("rows") or []
    by_v = collections.Counter(r.get("verdict") for r in rows)
    open_dom = collections.Counter(r.get("domain") for r in rows if r.get("verdict") != "CONTRACTED")
    seen_v, seen_dom, holds = set(), None, class_holds(facts)
    for t in md_tables(text):
        head = [h.lower() for h in t[0]]
        if head and head[0] == "verdict":
            for cells in t[1:]:
                v = strip_md(cells[0])
                seen_v.add(v)
                n = int(re.sub(r"[^\d]", "", cells[1]) or 0)
                if n != by_v.get(v, 0):
                    out.append("verdict table says %s %d; traceability has %d"
                               % (v, n, by_v.get(v, 0)))
        if head and head[0] == "domain":
            seen_dom = {strip_md(c[0]): int(re.sub(r"[^\d]", "", c[-1]) or 0) for c in t[1:]}
        if any("class" in h for h in head) and any("hold" in h for h in head):
            ci = [i for i, h in enumerate(head) if "class" in h][0]
            hi = [i for i, h in enumerate(head) if "hold" in h][0]
            for cells in t[1:]:
                k = strip_md(cells[ci]).lower()
                m = re.search(r"\*\*([\d,]+)", cells[hi])
                if k in holds and m and int(m.group(1).replace(",", "")) > holds[k]:
                    out.append("class %s says it holds %s; the package has %d"
                               % (k, m.group(1), holds[k]))
    for v in sorted(set(by_v) - seen_v):
        out.append("traceability has verdict %s, which the verdict table omits" % v)
    if seen_dom is None:
        out.append("no domain table of the rows that are not CONTRACTED")
    elif seen_dom != dict(open_dom):
        out.append("domain table says %r; traceability gives %r" % (seen_dom, dict(open_dom)))
    quoted = " ".join(l[2:] for l in text.splitlines() if l.startswith("> ") and "·" in l)
    listed = sorted(x.strip() for x in quoted.split("·") if x.strip())
    if listed != sorted(facts.closed_classes):
        out.append("its closed-class list %r is not handoff/closed_classes.json %r"
                   % (listed, sorted(facts.closed_classes)))
    for t in unresolved(facts, text):
        out.append("names `%s`, which does not exist" % t)
    return out


# ---------------------------------------------------- schema-viewer-notes --

def sv_test(facts, text):
    """Everything it says about the graph's shape, checked against relationships.csv. Its counts
    are a dated measurement; the shape it explains is tested here and must be current."""
    out = []
    R = facts.rels
    if not R:
        return ["handoff/relationships.csv is empty or missing"]
    kinds = collections.Counter(r.get("edge_kind") for r in R)
    hows = collections.Counter(r.get("how") for r in R)
    tbl = md_tables(text)

    def first_col(pred):
        for t in tbl:
            if pred([h.lower() for h in t[0]]):
                return {strip_md(c[0]) for c in t[1:]}
        return None
    k_named = first_col(lambda h: h and h[0] == "kind")
    h_named = first_col(lambda h: h and h[0] == "how")
    if k_named != set(kinds):
        out.append("edge kinds described %r; relationships.csv has %r"
                   % (sorted(k_named or []), sorted(kinds)))
    if h_named != set(hows):
        out.append("`how` values described %r; relationships.csv has %r"
                   % (sorted(h_named or []), sorted(hows)))
    if any((r.get("edge_kind") == "ambient") != (r.get("how") == "lineage") for r in R):
        out.append("it says ambient means a lineage coupling, and relationships.csv has an ambient "
                   "edge that is not lineage or a lineage edge that is not ambient")
    top = [t for t, _n in collections.Counter(r.get("to_table") for r in R).most_common(3)]
    named = re.findall(r"`([a-z_]+\.[a-z_]+)`\s+(?:is the target\s+)?of\s+\*\*[\d,]+", text)
    if named[:3] != top:
        out.append("hubs named in order %r; the three most-referenced tables are %r"
                   % (named[:3], top))
    no_cols = sorted(t for t in facts.storage if t not in facts.cols and "." in t)
    # The section opens with how many there are and names each one; it may name others too.
    sect = text.split("**Tables with no columns.**", 1)
    body = sect[1].split("\n## ", 1)[0] if len(sect) > 1 else ""
    named_t = set(re.findall(r"`([a-z_]+\.[a-z_]+)`", body))
    words = {"no": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10}
    m = re.match(r"\s*(\w+)", body)
    said = (words.get(m.group(1).lower()) if not m.group(1).isdigit() else int(m.group(1))) \
        if m else None
    if said != len(no_cols) or not set(no_cols) <= named_t:
        out.append("tables with no columns: it says %s and names %r; the schema reference has %r"
                   % (m.group(1) if m else "nothing", sorted(named_t & set(no_cols)), no_cols))
    for t in unresolved(facts, text):
        out.append("names `%s`, which does not exist" % t)
    return out


# ------------------------------------------------------- rag-index-sources --

RAG_ROW = re.compile(r"^\| `([a-z_]+\.[a-z_]+)` \| ([^|\n`]+)\|([^|\n]*)\|([^|\n]*)\|([^|\n]*)\| "
                     r"`([^`\n]+)` \|", re.M)
INDEX_OPS = ("listIndexSources", "setIndexSource", "reindexSource", "removeIndexEntry",
             "eraseSubject", "semanticSearch")


def rag_described(facts, text):
    """The IndexSource model and the indexing operations' descriptions, which its four rules
    restate."""
    src = (((facts.contracts.get("ai") or {}).get("components") or {}).get("schemas")
           or {}).get("IndexSource")
    parts = [json.dumps(src, sort_keys=True, default=str)]
    parts += [json.dumps((facts.op_doc.get(o) or {}).get("description"), default=str)
              for o in INDEX_OPS]
    return {"index-model": parts}


def rag_test(facts, text):
    out = []
    rows = RAG_ROW.findall(text)
    if not rows:
        return ["no source rows found"]
    for table, fields, _a, _b, _c, event in rows:
        if table not in facts.cols:
            out.append("source %s is not a table in the schema reference" % table)
            continue
        for f in [x.strip() for x in fields.split(",") if x.strip()]:
            if snake(f) not in facts.cols[table] and f not in facts.cols[table]:
                out.append("source %s text field %r is not a column of it" % (table, f))
        ev = facts.events.get(event)
        if not ev:
            out.append("source %s is invalidated by %s, which is not in events/" % (table, event))
        elif "ai" not in [c.get("context") for c in ev[1].get("consumers") or []]:
            out.append("%s does not list ai as a consumer, so nothing reindexes %s" % (event, table))
    declared = {r[0] for r in rows}
    indexed = {t for t in (facts.lineage.get("reindexSource") or {}).get("reads") or []
               if "." in t and ":" not in t and not t.startswith("ai.")}
    if not indexed:
        out.append("reindexSource has no lineage - the register cannot be compared with it")
    for t in sorted(indexed - declared):
        out.append("reindexSource reads %s and the register does not declare it" % t)
    for t in sorted(declared - indexed):
        out.append("the register declares %s and reindexSource does not read it" % t)
    for m in re.finditer(r"^\| `([\w.]+)` \| `events/([\w.-]+)\.yaml` \| ([\w-]+) \|", text, re.M):
        ev = facts.events.get(m.group(1))
        pub = str((ev or ("", {}))[1].get("publisher"))
        # The column names the publishing contract; the event file names its context.
        if not ev or ev[0] != m.group(2) or (pub != m.group(3)
                                             and pub not in facts.persist.get(m.group(3), ())):
            out.append("event row %s / %s / %s does not match events/" % m.groups())
    for t in unresolved(facts, text):
        out.append("names `%s`, which does not exist" % t)
    for s in undated_counts(text):
        out.append("states an undated count: %r" % s)
    return out


# ------------------------------------------------------------------ wiring --

def read(rel, root=ROOT):
    with io.open(os.path.join(root, rel), encoding="utf-8") as fh:
        raw = fh.read()
    return json.loads(raw) if rel.endswith(".json") else raw


TESTS = {
    "handoff/service-decomposition.json": (sd_test, sd_described),
    "handoff/contract-backlog.json": (cb_test, cb_described),
    "handoff/backlog-clusters.json": (bc_test, bc_described),
    "handoff/traceability.json": (tr_test, tr_described),
    "handoff/artefact-audit.md": (aa_test, aa_described),
    # Everything it says is a computed test (the shape of relationships.csv) or a dated count.
    "handoff/schema-viewer-notes.md": (sv_test, None),
    "handoff/rag-index-sources.md": (rag_test, rag_described),
}


def load_state():
    try:
        s = json.load(io.open(STATE, encoding="utf-8"))
    except Exception:
        return {}
    return s if s.get("_format") == 2 else {}


def stored(described):
    """Lists that name things are kept verbatim so a later run can say what moved; the rest is
    hashed."""
    return {k: (v if (k.startswith("set:") or k.startswith("ops:") or k == "cfs") else sha(v))
            for k, v in described.items()}


def compare(rel, described, state):
    """How the described part moved since the file was blessed; empty when it has not."""
    was = (state.get(rel) or {}).get("parts")
    if was is None:
        return ["never blessed against its described part"]
    out = []
    for k in sorted(set(described) | set(was)):
        now, then = described.get(k), was.get(k)
        if then is None:
            out.append("%s is new since the bless" % k)
        elif now is None:
            out.append("%s is gone since the bless" % k)
        elif isinstance(then, list):
            add, rem = sorted(set(now) - set(then)), sorted(set(then) - set(now))
            if add or rem:
                bits = []
                if add:
                    bits.append("+" + ", +".join(add[:10]) + (" (+%d more)" % (len(add) - 10)
                                                              if len(add) > 10 else ""))
                if rem:
                    bits.append("-" + ", -".join(rem[:10]))
                out.append("%s: %s" % (k, "  ".join(bits)))
        elif then != sha(now):
            out.append("%s changed" % k)
    return out


def run(facts, root=ROOT):
    """(computed problems, described parts) per file."""
    res = {}
    for rel, _r, _b in AUTHORED:
        test, desc = TESTS[rel]
        if not os.path.exists(os.path.join(root, rel)):
            res[rel] = (["missing"], {})
            continue
        try:
            doc = read(rel, root)
        except Exception as e:
            res[rel] = (["does not parse: %s" % e], {})
            continue
        res[rel] = (test(facts, doc), desc(facts, doc) if desc else {})
    return res


# --------------------------------------------------------------- self-test --

def self_test(facts):
    """Each per-file test must report something new on a sabotaged input. Returns the labels of
    the sabotages that went unnoticed (empty = all caught)."""
    fails, ran = [], [0]

    def expect(label, fn, base, sab, f=None):
        ran[0] += 1
        f = f or facts
        try:
            if not (set(fn(f, sab)) - set(fn(facts, base))):
                fails.append(label)
        except Exception as e:
            fails.append("%s (raised %s)" % (label, e))

    D = read("handoff/service-decomposition.json")
    svc = next(n for n, v in D["services"].items() if v.get("contracts"))
    s = copy.deepcopy(D)
    s["services"][svc]["contracts"] = s["services"][svc]["contracts"][1:]
    expect("decomposition: a deployable contract assigned to no service", sd_test, D, s)
    s = copy.deepcopy(D)
    s["services"][svc]["operations"] = -1
    expect("decomposition: a derived count wrong", sd_test, D, s)
    s = copy.deepcopy(D)
    s["services"][svc]["why"] += " It has 999 operations."
    expect("decomposition: an undated count in prose", sd_test, D, s)
    s = copy.deepcopy(D)
    s["services"][svc]["why"] += " See `noSuchOperationAnywhere`."
    expect("decomposition: a named operation that does not exist", sd_test, D, s)
    ran[0] += 1
    st = {"handoff/service-decomposition.json": {"parts": stored(sd_described(facts, D))}}
    f2 = copy.copy(facts)
    f2.persist = dict(facts.persist)
    f2.persist[facts.deployable[0]] = set(facts.persist.get(facts.deployable[0], ())) | {"zz_new"}
    if not compare("handoff/service-decomposition.json", sd_described(f2, D), st):
        fails.append("decomposition: a contract writing a new schema is not noticed")

    B = read("handoff/contract-backlog.json")
    b = copy.deepcopy(B)
    e = next(x for x in b["entries"] if x.get("status") == "open")
    e["fix"] = (e.get("fix") or "") + " Add `%s`." % sorted(facts.ops)[0]
    expect("backlog: an open entry proposing an operation that exists", cb_test, B, b)
    rows = facts.trace.get("rows") or []
    partial = {r.get("backlog") for r in rows if r.get("verdict") != "CONTRACTED"}
    cand = [x for x in B["entries"] if x.get("status") == "done" and x["id"] not in partial
            and any(r.get("backlog") == x["id"] for r in rows)]
    b = copy.deepcopy(B)
    done = next(x for x in b["entries"] if x["id"] == cand[0]["id"])
    done["status"], done["lane"] = "open", "settled"
    for k in BLOCKERS:
        done[k] = []
    expect("backlog: an open entry whose rows are all CONTRACTED", cb_test, B, b)

    C = read("handoff/backlog-clusters.json")
    c = copy.deepcopy(C)
    c["clusters"][0]["entries"] = c["clusters"][0]["entries"][1:]
    expect("clusters: an entry dropped from its cluster", bc_test, C, c)
    c = copy.deepcopy(C)
    c["unclustered"] = c["unclustered"] + ["BL-999"]
    expect("clusters: an entry that is not in the backlog", bc_test, C, c)

    T = read("handoff/traceability.json")
    t = copy.deepcopy(T)
    next(x for x in t["rows"] if x.get("verdict") == "CONTRACTED")["evidence"] = "noSuchOpAnywhere"
    expect("traceability: evidence that does not exist", tr_test, T, t)
    t = copy.deepcopy(T)
    next(x for x in t["rows"] if x.get("verdict") == "CONTRACTED")["note"] += " See `noSuchOpX`."
    expect("traceability: a note naming an operation that does not exist", tr_test, T, t)
    t = copy.deepcopy(T)
    r = next(x for x in t["rows"] if x.get("verdict") == "CONTRACTED" and not x.get("cf") and
             (facts.backlog.get(x.get("backlog")) or {}).get("status") == "done")
    r["verdict"] = "CONTRACTED_PARTIAL"
    expect("traceability: a partial row on a done entry with no decision", tr_test, T, t)

    A = read("handoff/artefact-audit.md")
    expect("artefact audit: a verdict count wrong", aa_test, A,
           re.sub(r"(\| `CONTRACTED` \| )([\d,]+)", lambda m: m.group(1) + "1", A, count=1))
    expect("artefact audit: a class holding more than the package", aa_test, A,
           re.sub(r"(\| Report \| \*\*)([\d,]+)", lambda m: m.group(1) + "99999", A, count=1))

    V = read("handoff/schema-viewer-notes.md")
    f3 = copy.copy(facts)
    f3.rels = facts.rels + [dict(facts.rels[0], how="madeUp")]
    expect("schema notes: a `how` value the file does not describe", sv_test, V, V, f3)
    expect("schema notes: hubs in the wrong order", sv_test, V,
           V.replace("`identity.principal` is the target", "`pii.subject` is the target", 1))

    G = read("handoff/rag-index-sources.md")
    m = RAG_ROW.search(G)
    expect("rag: a text field that is not a column", rag_test, G,
           G.replace(m.group(0), m.group(0).replace(m.group(2), "noSuchColumn, " + m.group(2)), 1))
    expect("rag: an invalidating event that does not exist", rag_test, G,
           G.replace("`%s` |" % m.group(6), "`noSuch.eventAnywhere` |", 1))
    f4 = copy.copy(facts)
    f4.lineage = dict(facts.lineage)
    ri = dict(facts.lineage.get("reindexSource") or {})
    extra = next(x for x in facts.tables if x not in {y[0] for y in RAG_ROW.findall(G)}
                 and not x.startswith("ai."))
    ri["reads"] = list(ri.get("reads") or []) + [extra]
    f4.lineage["reindexSource"] = ri
    expect("rag: a table reindexSource reads and the register omits", rag_test, G, G, f4)

    # E-07: a contract that does not parse is a problem, not a skip.
    ran[0] += 1
    tmp = tempfile.mkdtemp(prefix="cai-")
    try:
        os.makedirs(os.path.join(tmp, "contracts", "spine"))
        io.open(os.path.join(tmp, "contracts", "spine", "broken.yaml"), "w",
                encoding="utf-8").write("openapi: [unclosed\n  : :\n")
        fb = Facts(tmp)
        if not any("broken.yaml" in p and "does not parse" in w for p, w in fb.problems):
            fails.append("a contract that does not parse is not reported")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return fails, ran[0]


def main():
    argv = sys.argv[1:]
    quiet = "--quiet" in argv
    facts = Facts()
    fails, n_self = self_test(facts)
    if fails or "--self-test" in argv:
        for f in fails:
            print("  SELF-TEST FAIL  %s" % f)
        print("self-test: %d of %d sabotaged inputs caught" % (n_self - len(fails), n_self))
        return 1 if fails else 0

    state = load_state()
    res = run(facts)

    if "--bless" in argv:
        targets = [a.replace("\\", "/") for a in argv[argv.index("--bless") + 1:]
                   if not a.startswith("--")]
        known = {rel for rel, _r, _b in AUTHORED}
        for t in targets:
            if t not in known:
                print("not an authored input: %s" % t)
                return 2
            if res[t][0] or facts.problems:
                print("refused: %s fails its computed tests - bring it up to date first" % t)
                for p in (res[t][0] + ["%s %s" % x for x in facts.problems])[:20]:
                    print("    %s" % p)
                return 1
        for t in targets:
            state[t] = {"blessed": datetime.date.today().isoformat(),
                        "parts": stored(res[t][1])}
        out = {"_format": 2}
        out.update(sorted((k, v) for k, v in state.items() if k != "_format"))
        io.open(STATE, "w", encoding="utf-8", newline="\n").write(
            json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print("blessed %d file(s) against the part of the package each describes" % len(targets))
        return 0

    stale, problems = [], list(facts.problems)
    for rel, readers, breaks in AUTHORED:
        comp, desc = res[rel]
        problems += [(rel, c) for c in comp]
        if TESTS[rel][1]:
            moved = compare(rel, desc, state)
            if moved:
                stale.append((rel, readers, breaks, moved))

    if not quiet:
        print("%d operations, %d schemas, %d deployable contracts, %d tables, %d events; "
              "self-test %d of %d sabotaged inputs caught"
              % (len(facts.ops), len(facts.schemas), len(facts.deployable), len(facts.tables),
                 len(facts.events), n_self, n_self))
        print()
        for rel, readers, breaks, moved in stale:
            print("  STALE  %s - the part of the package it describes moved" % rel)
            for mv in moved[:8]:
                print("         %s" % mv)
            print("         read by %s; %s" % (readers, breaks))
        for rel, why in problems:
            print("  ISSUE  %-38s %s" % (rel, why))
        if stale or problems:
            print()
            print("  These are authored; nothing in tools/ rebuilds them. An ISSUE is the file being")
            print("  wrong: fix the file. A STALE file is re-read against what moved")
            print("  (docs/regenerating-authored-docs.md), then --bless <path>.")

    n = len(stale) + len(problems)
    print("%s - %d stale, %d issue(s), %d authored input(s) checked"
          % ("FAIL" if n else "PASS", len(stale), len(problems), len(AUTHORED)))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
