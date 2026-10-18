#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared plumbing for the audit-class guards (plan item 1F, C12; docs/active/root-classes.md).

The 26 September pull audit found 293 root issues. Each belongs to a class of mistake, and a class
is closed only when something fails the next time it happens. The `check-*.py` guards written for
that read the package, never write it, and are **baseline-aware**: where a class still has members
today, the known ones are listed in `handoff/audit-baseline.json` and only a NEW member fails.

    python3 tools/check-<name>.py                    # exit 1 on a finding not in the baseline
    python3 tools/check-<name>.py --all              # list every finding, known ones too
    python3 tools/check-<name>.py --update-baseline  # record today's findings as known (an act,
                                                     # like --freeze: do it in a reviewed commit)

A baseline entry that no longer occurs is reported as `gone`, so the list only ever shrinks: run
`--update-baseline` after a fix to tighten it. Adding entries by hand to silence a new finding is
the thing this file exists to prevent; the commit that does it must say why.
"""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "handoff" / "audit-baseline.json"
CONTRACTS = ROOT / "contracts"
SCREENS = ROOT / "screens"
VERBS = ("get", "post", "put", "patch", "delete")
LINKS = ROOT / "handoff" / "service-docs" / "adam-links.json"
# **A baselined finding fails once its ticket starts** (18 October 2026, post-r6 plan item 9, CHG-CRF-001). A ticket
# has started once OpenProject moves it off these (op-release.json `statuses`: new, on_hold, rejected). In progress,
# Ready for QA, Closed and any status added later all count, so a new status name cannot hide a started ticket.
NOT_STARTED = ("New", "On hold", "Rejected")
# A feature or an epic is the parent of the tasks that build it and links what they link: only the work counts.
PARENT_TYPES = ("Epic", "Feature")
# What a baselined finding names that a ticket builds.
STARTED_KINDS = ("operation", "table")
# An acknowledgement names the request or change that will fix what was built, as check-changelog's `why` does, or
# the follow-up row on the tracker sheet (`F<n>`) when no request is raised for it (controller ruling 7, 18 October).
CITES = re.compile(r"\bCR-\d+\b|\bCHG-[A-Z][A-Z0-9]{1,5}-\d{3}\b|\bF\d+\b")
# Older than this, the note says the cached ticket status should be read again.
STALE_DAYS = 7

_CACHE: dict = {}


def load_yaml(path):
    """YAML with the C loader where it can; the pure loader where a file defeats it (surrogate
    escapes in subscription.yaml do)."""
    path = Path(path)
    key = str(path)
    if key in _CACHE:
        return _CACHE[key]
    text = path.read_text(encoding="utf-8")
    try:
        doc = yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        doc = yaml.load(text, Loader=yaml.SafeLoader)
    _CACHE[key] = doc
    return doc


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def contract_files():
    return sorted(p for p in CONTRACTS.glob("*/*.yaml"))


def contracts():
    """[(stem, relpath, doc)] for every contract file."""
    out = []
    for f in contract_files():
        doc = load_yaml(f) or {}
        out.append((f.stem, f.relative_to(ROOT).as_posix(), doc))
    return out


def operations():
    """operationId -> {contract, file, method, path, op, item}."""
    key = "__ops__"
    if key in _CACHE:
        return _CACHE[key]
    out = {}
    for stem, rel, doc in contracts():
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for m in VERBS:
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = {"contract": stem, "file": rel, "method": m,
                                              "path": path, "op": op, "item": item}
    _CACHE[key] = out
    return out


def schemas():
    """(contract stem, schema name) -> schema dict, plus a name -> [stem] index."""
    key = "__schemas__"
    if key in _CACHE:
        return _CACHE[key]
    by = {}
    names: dict = {}
    for stem, rel, doc in contracts():
        for n, s in (((doc.get("components") or {}).get("schemas")) or {}).items():
            if isinstance(s, dict):
                by[(stem, n)] = s
                names.setdefault(n, []).append(stem)
    _CACHE[key] = (by, names)
    return by, names


def screens():
    """[(platform file stem, screen dict)] for every screen in screens/P*.yaml."""
    key = "__screens__"
    if key in _CACHE:
        return _CACHE[key]
    out = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = load_yaml(f) or {}
        for s in doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                out.append((f.stem, s))
    _CACHE[key] = out
    return out


def platforms():
    out = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = load_yaml(f) or {}
        out[f.stem] = doc.get("platform") or {}
    return out


def snake(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", str(name))
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    return s.lower()


def viewed_table(name, known):
    """The table a DB-READ-VIEWS read view `<table>_for_<reader>` reads, if `known` has it; else None.

    **A read through a view is a read of its table** (14 October 2026, CHG-R6G-007, CHG-GTE-001). DB-READ-VIEWS
    publishes one view per (reader module, owned table) for bulk reads within one deployable, and the lineage names
    such a read by the view (`publishBundle` reads `platform.sale_board_for_catalogue`). Every check that resolves a
    lineage table against the schema asks this one question, so a new reader of the lineage cannot miss it again.
    Each `_for_` split is tried, so a table whose own name holds `_for_` still resolves. Reads only: a view is never
    written. tools/check-lineage.py additionally checks the reader is the operation's own module.
    """
    name = str(name)
    i = name.find("_for_")
    while i > 0:
        if name[:i] in known:
            return name[:i]
        i = name.find("_for_", i + 1)
    return None


def read_views(lin, known):
    """Every DB-READ-VIEWS view the lineage reads: view -> {table, reader, operations, columns}.

    **The schema reference lists the views the lineage reads** (14 October 2026, CHG-GTE-001, tracker F27). The lineage
    names a read through a view by the view (`publishBundle` reads `platform.sale_board_for_catalogue`, CHG-R6G-007),
    and `check-package` failed it because the schema reference had no such name. `build-schema-workbook.py` writes
    these on its `Read views` sheet, so the name a developer meets in the lineage is one they can look up, with the
    table beneath it, the module it is for and the columns its readers read (`readColumns`; none: every column).
    """
    out: dict = {}
    for oid, v in (lin or {}).items():
        rc = v.get("readColumns") or {}
        for t in v.get("reads") or []:
            base = viewed_table(t, known) if ":" not in str(t) and t not in known else None
            if not base:
                continue
            x = out.setdefault(t, {"table": base, "reader": str(t)[len(base) + len("_for_"):],
                                   "operations": set(), "columns": set(), "every": False})
            x["operations"].add(oid)
            cs = rc.get(t) or rc.get(base)
            if cs:
                x["columns"].update(cs)
            else:
                x["every"] = True
    return out


def ref_name(ref: str) -> str:
    return str(ref).rsplit("/", 1)[-1]


def head_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip()
    except Exception:
        return ""


def _rel(path) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def link_index(path=None) -> dict:
    """What handoff/service-docs/adam-links.json says each artefact's tickets are, offline (CHG-CRF-001).

    adam-links.py writes one row per (ticket, kind, id) and, with TICVAI_OP_TOKEN, each ticket's subject, status, type
    and assignee as OpenProject had them (`statusReadAt`). Returns
      {"exists", "cached", "readAt",
       "ops":     operationId -> {"<service>#<operationId>", ...},
       "tables":  {schema.table}, "screens": {screen id},
       "tickets": (kind, id) -> [{"wp", "status", "type", "assignee", "subject"}],
       "wps":     wp -> the same row for that ticket}
    """
    path = Path(path or LINKS)
    key = "__links__" + str(path)
    if key in _CACHE:
        return _CACHE[key]
    doc = load_json(path, {}) or {}
    idx = {"exists": path.exists(), "cached": bool(doc.get("cached")), "readAt": doc.get("statusReadAt") or "",
           "ops": {}, "tables": set(), "screens": set(), "tickets": {}, "wps": {}}
    for ln in doc.get("links") or []:
        kind, ident = ln.get("kind"), str(ln.get("id") or "")
        if kind == "operation" and "#" in ident:
            idx["ops"].setdefault(ident.split("#", 1)[1], set()).add(ident)
        elif kind == "table":
            idx["tables"].add(ident)
        elif kind == "screen":
            idx["screens"].add(ident)
        try:
            wp = int(ln.get("key"))
        except (TypeError, ValueError):
            continue
        row = {"wp": wp, "status": ln.get("status") or "", "type": ln.get("type") or "",
               "assignee": ln.get("assignee") or "", "subject": ln.get("subject") or ""}
        idx["wps"].setdefault(wp, row)
        rows = idx["tickets"].setdefault((kind, ident), [])
        if all(r["wp"] != wp for r in rows):
            rows.append(row)
    _CACHE[key] = idx
    return idx


def finding_artefacts(key: str, idx: dict) -> set:
    """The operations and tables a finding's key names, as adam-links names them: {(kind, id)}.

    Keys join ids with ':' or '|' ('exportSubjectData:marketing.consent_record', 'linkGuestCheckout|403'), or an
    operation and a field or a table with '.' ('addIncidentPerson.pii.subject'). A token is an operation when
    adam-links has `<service>#<token>` (or is that id itself), a table when adam-links has the table. Anything else (a
    screen, a schema field, a file) names nothing this rule judges."""
    out = set()
    for tok in re.split(r"[:|]", str(key)):
        tok = tok.strip()
        if not tok:
            continue
        if "#" in tok and tok in idx["ops"].get(tok.split("#", 1)[1], ()):
            out.add(("operation", tok))
        elif tok in idx["ops"]:
            out |= {("operation", o) for o in idx["ops"][tok]}
        elif tok in idx["tables"]:
            out.add(("table", tok))
        elif "." in tok:
            head, rest = tok.split(".", 1)
            if head in idx["ops"]:
                out |= {("operation", o) for o in idx["ops"][head]}
            if rest in idx["tables"]:
                out.add(("table", rest))
    return {a for a in out if a[0] in STARTED_KINDS}


def started_tickets(artefacts, idx: dict) -> list:
    """The started tickets that build any of `artefacts`, by id: [{"wp", "status", "type", "assignee", "subject",
    "on"}]. Started: a status not in NOT_STARTED, on a ticket that is not an epic or a feature."""
    seen: dict = {}
    for a in sorted(artefacts):
        for t in idx["tickets"].get(a, []):
            if t["status"] and t["status"] not in NOT_STARTED and t["type"] not in PARENT_TYPES:
                seen.setdefault(t["wp"], dict(t, on=f"{a[0]} {a[1]}"))
    return [seen[w] for w in sorted(seen)]


def tickets_text(tickets: list, most: int = 4) -> str:
    shown = [f"#{t['wp']} {t['status']}" + (f" ({t['assignee']})" if t.get("assignee") else "")
             for t in tickets[:most]]
    more = f" and {len(tickets) - most} more" if len(tickets) > most else ""
    return ", ".join(shown) + more


def _days_since(iso: str):
    try:
        then = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return None
    if then.tzinfo is None:
        then = then.replace(tzinfo=datetime.timezone.utc)
    return (datetime.datetime.now(datetime.timezone.utc) - then).days


class Guard:
    """Collects findings by rule, compares them with the baseline, prints, and sets the exit code.

    A finding is (rule, key, message). The key is what the baseline stores, so it must be stable
    across runs: an id, never a line number.
    """

    def __init__(self, name: str, rules: dict):
        self.name = name
        self.rules = rules          # rule id -> one line: what it catches and the roots it closes
        self.found: dict = {r: {} for r in rules}
        self.notes: list = []
        # (rule, key) findings that can never be baselined: they fail whether or not the baseline lists them,
        # and --update-baseline leaves them out (CHG-GEN-003: a stub table the lineage writes).
        self.strict: set = set()
        args = sys.argv[1:]
        self.show_all = "--all" in args
        self.update = "--update-baseline" in args

    def add(self, rule: str, key: str, message: str, strict: bool = False):
        """`strict`: this finding fails even when the baseline lists it, and is never written into the baseline
        (CHG-GEN-003). For a member of a class whose debt may not wait: a written table that holds only keys."""
        self.found.setdefault(rule, {})[str(key)] = message
        if strict:
            self.strict.add((rule, str(key)))

    def note(self, text: str):
        self.notes.append(text)

    def _baseline(self) -> dict:
        data = load_json(BASELINE, {}) or {}
        return ((data.get(self.name) or {}).get("rules")) or {}

    def _write_baseline(self):
        data = load_json(BASELINE, {}) or {}
        data.setdefault("_about", (
            "Known members of the audit classes (docs/active/root-classes.md) still present when a "
            "guard was baselined. A guard fails only on a finding not listed here. Written by "
            "`python3 tools/check-<name>.py --update-baseline`; never add an entry by hand to "
            "silence a new finding."))
        data[self.name] = {
            "updated": datetime.date.today().isoformat(),
            "commit": head_commit(),
            "rules": {r: sorted(x for x in k if (r, x) not in self.strict)
                      for r, k in sorted(self.found.items()) if any((r, x) not in self.strict for x in k)},
        }
        ordered = {"_about": data["_about"]}
        for k in sorted(k for k in data if k != "_about"):
            ordered[k] = data[k]
        BASELINE.write_text(json.dumps(ordered, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    def finish(self, limit: int = 12) -> int:
        base = self._baseline()
        total_new = 0
        total_known = 0
        gone_total = 0
        new_rules = []
        print(f"{self.name}: {len(self.rules)} rule(s)")
        for rule, desc in self.rules.items():
            cur = self.found.get(rule) or {}
            known = set(base.get(rule) or [])
            new = sorted(k for k in cur if k not in known or (rule, k) in self.strict)
            gone = sorted(k for k in known if k not in cur)
            total_new += len(new)
            total_known += len(cur) - len(new)
            gone_total += len(gone)
            mark = "FAIL" if new else "ok  "
            print(f"  {mark} {rule:<22} {len(cur):>5} found, {len(new):>4} new, "
                  f"{len(gone):>4} gone  - {desc}")
            if new:
                new_rules.append(rule)
            shown = sorted(cur) if self.show_all else new
            for k in shown[:limit if not self.show_all else None]:
                tag = ("NEW*" if (rule, k) in self.strict else "NEW ") if k in new else "    "
                print(f"       {tag}{cur[k]}")
            if not self.show_all and len(new) > limit:
                print(f"       ... and {len(new) - limit} more new (--all lists every one)")
        for n in self.notes:
            print(f"  note: {n}")
        if self.update:
            self._write_baseline()
            print(f"baseline written: {sum(len(v) for v in self.found.values())} known finding(s) "
                  f"in {BASELINE.relative_to(ROOT).as_posix()}")
            return 0
        tail = (f"; {gone_total} baseline entr{'y' if gone_total == 1 else 'ies'} gone - run "
                f"--update-baseline to tighten") if gone_total else ""
        if total_new:
            print(f"FAIL - {total_new} new finding(s) in {', '.join(new_rules)}; "
                  f"{total_known} known{tail}")
            return 1
        print(f"PASS - 0 new, {total_known} known (baseline){tail}")
        return 0


def force_utf8():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
