#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The known findings by artefact: handoff/known-findings.json, which ADAM's pull reads (r14 lane k, CHG-R14PUL-001).

    python3 tools/build-known-findings.py            # writes handoff/known-findings.json
    python3 tools/build-known-findings.py --check    # exits 1 when the file is not what this would write

**Why** (the lead, 3 November 2026: "a ticket's pull lists the package checks it already fails, so developers stop
raising change requests for gaps we already know about"). The gate's checks already know many gaps: findings kept in
their baselines (check-screen-wiring alone says "4529 known (baseline)"). A developer's pull never showed them, so a
developer met a known gap, raised a change request, and a round went on settling something already on the list.
This writes every known finding with the artefacts it is about, in ADAM's link vocabulary (`operation:<contract>#<op>`,
`table:<schema.table>`, `screen:<id>`, `file:<path>`, `adr:<id>`), so the pull can list the ones a ticket links.

**What counts as known** (this only shows what the baselines already hold; it baselines, acknowledges and exempts
nothing, and changes no check's verdict):

  1. every audit-class guard with entries in handoff/audit-baseline.json (tools/audit_guard.py), run once with
     TICVAI_KNOWN_FINDINGS_OUT: its findings that are baselined AND still found, with the guard's own message. A
     baseline entry no longer found is counted as gone, never listed (it is not a gap any more); a strict finding is
     never known;
  2. every gating checker tools/refresh-safe-baseline.json lets fail on named lines: the error lines its `known`
     patterns match, exactly as refresh-safe.sh's judge matches them (check-screen-patterns' accepted line is a
     count, so its finding lines are read below it, in LINE_MAP);
  3. checks/baseline.json (check-binding-ratchet) is not indexed: it holds counts per app, block and kind, which
     name no artefact (`sources` says so).

**Where a key names its artefact.** RULE_MAP says, for every check, how its keys are read; this is the one place.
A rule a baseline holds that RULE_MAP does not name, and a finding whose key resolves to no artefact of the package,
go to `unmapped` by name, and tools/check-known-findings.py fails on them unless NOT_AN_ARTEFACT gives the reason
(a count over a ceiling). A schema or field (`stem.Schema.field`) is mapped to the tables built from it
(schema-reference `cols` sources) and to the operations whose request, parameters or responses reach it through any
number of $refs: the work that would meet the gap; a schema neither reaches is mapped to the contract file defining
it. ADR-0015's device classes (check-device-tiers) are mapped to the decision.

Deterministic (no dates): a regenerated tree carries the same file for the same inputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import audit_guard as g  # noqa: E402

OUT = ROOT / "handoff" / "known-findings.json"
AUDIT_BASELINE = ROOT / "handoff" / "audit-baseline.json"
SAFE_BASELINE = ROOT / "tools" / "refresh-safe-baseline.json"
BINDING_BASELINE = ROOT / "checks" / "baseline.json"
PAIRS = ROOT / "screens" / "_guest-pairs.yaml"
JOBS = 6

# check -> rule -> how its keys are read ("*": every rule of the check). Resolvers below; one table, so a new rule's
# key shape is decided here and nowhere else.
#   tokens     split on ':' and '|'; each token is a screen, an operation, a table, `op.field`, `op.schema.table`,
#              `stem.Schema[.field]` (its tables and operations) or a package file
#   cited-doc  `doc|cited`: the document that cites (the cited path is the missing thing)
#   guest-pair a group of screens/_guest-pairs.yaml: its web and app screens
#   adr:<id>   about the decision itself (ADR-0015's device classes)
RULE_MAP = {
    "check-cited-sources": {"*": "cited-doc"},
    "check-contract-shapes": {"*": "tokens"},
    "check-cross-module-reads": {"*": "tokens"},
    "check-ddl-conventions": {"*": "tokens"},
    "check-device-tiers": {"D-TIER-A-UNPLANNED": "adr:ADR-0015"},
    "check-error-sources": {"*": "tokens"},
    "check-glossary-terms": {"*": "tokens"},
    "check-navigation": {"N-TWIN-OPS": "guest-pair", "N-TWIN-WAVE": "guest-pair", "*": "tokens"},
    "check-parameter-columns": {"*": "tokens"},
    "check-plan-closure": {"*": "tokens"},
    "check-request-fields-stored": {"*": "tokens"},
    "check-rls-scope-fit": {"*": "tokens"},
    "check-screen-wiring": {"*": "tokens"},
    "check-stored-request-fields": {"*": "tokens"},
    "check-wireframe-coverage": {"*": "tokens"},
    # refresh-safe-baseline.json checkers: keys are written by LINE_MAP below
    "check-screen-permissions": {"*": "tokens"},
    "check-screen-patterns": {"*": "tokens"},
    "check-authored-inputs": {"*": "tokens"},
}

# (check, rule) -> why its findings name no artefact a ticket links. Listed by name in the index; never a failure.
NOT_AN_ARTEFACT = {
    ("check-screen-patterns", "NP"): "a count of later-sprint screens over a ceiling, about no one screen",
}

ERR = re.compile(r"^\s*(FAIL|STALE|ISSUE)\s+(.*\S)\s*$", re.M)   # refresh-safe.sh's judge, verbatim


def _sp_lines(out: str, accepted: list) -> list:
    """check-screen-patterns: the accepted line is its count ("28 finding(s): NP 1, P8 20, READ 7"); the findings
    are the lines above it, `  <rule> <screen> <message>`, less the exempt ones."""
    if not accepted:
        return []
    rows = []
    for m in re.finditer(r"^  (NP|READ|P\d+)\s+(\S+)\s+(.*\S)\s*$", out, re.M):
        rule, screen, msg = m.groups()
        rows.append((rule, screen if screen != "-" else f"{rule}-ceiling", f"{screen}: {msg}" if screen != "-" else msg))
    return rows


def _sp_perm(line: str):
    m = re.match(r"^(SP-[A-Z-]+)\s+\S+\.yaml\s+([A-Z]+-\d+):\s*(.*)$", line)
    return (m.group(1), m.group(2), f"{m.group(2)}: {m.group(3)}") if m else None


def _authored(line: str):
    m = re.match(r"^(\S+)\s+(.*)$", line)
    return ("STALE", m.group(1), f"{m.group(1)}: {m.group(2)}") if m else None


# refresh-safe-baseline.json checker -> how its accepted lines become (rule, key, message): per line, or (for a
# checker whose accepted line is a count) from its whole output.
LINE_MAP = {
    "check-screen-permissions": {"line": _sp_perm},
    "check-authored-inputs": {"line": _authored},
    "check-screen-patterns": {"output": _sp_lines},
}


def sha(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def run_tool(name: str, env_extra: dict | None = None) -> tuple:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", **(env_extra or {}))
    p = subprocess.run([sys.executable, str(ROOT / "tools" / f"{name}.py")], cwd=ROOT, env=env, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def guard_known(name: str) -> dict:
    """One guard's export (audit_guard.Guard.export_known), or {"error": ...}."""
    with tempfile.TemporaryDirectory(prefix="known-findings-") as tmp:
        out = Path(tmp) / "known.json"
        rc, text = run_tool(name, {"TICVAI_KNOWN_FINDINGS_OUT": str(out)})
        if not out.exists():
            return {"error": f"{name} wrote no export (rc={rc}): {text.strip().splitlines()[-1:] or ['no output']}"}
        return json.loads(out.read_text(encoding="utf-8"))


def line_known(name: str, patterns: list) -> dict:
    """A refresh-safe-baseline checker's accepted findings: {"known": [...], "error"?}."""
    how = LINE_MAP.get(name)
    rc, out = run_tool(name)
    errs = [m.group(2).strip() for m in ERR.finditer(out) if not m.group(2).startswith("-")]
    accepted = [e for e in errs if any(re.search(p, e) for p in patterns)]
    if how is None:
        return {"known": [{"rule": "-", "key": e, "message": e} for e in accepted], "unread": True}
    rows = []
    if "line" in how:
        for e in accepted:
            r = how["line"](e)
            rows.append(r if r else ("-", e, e))
    else:
        rows = how["output"](out, accepted)
    return {"known": [{"rule": r, "key": k, "message": m} for r, k, m in rows]}


class Package:
    """What a key can name: screens, operations, tables, schemas and files, in ADAM's link vocabulary."""

    files = None    # a set of package paths in tests; None: the package's own files on disk

    @classmethod
    def of(cls, **parts):
        """A package from parts (the self-test): ops (operationId -> "<contract>#<op>"), screens, tables,
        schema_tables, schema_ops, schema_file, groups, files."""
        pkg = cls.__new__(cls)
        pkg.root = ROOT
        for name in ("screens", "tables", "files"):
            setattr(pkg, name, set(parts.get(name) or ()))
        for name in ("ops", "schema_tables", "schema_ops", "schema_file", "groups"):
            setattr(pkg, name, dict(parts.get(name) or {}))
        return pkg

    def __init__(self, root: Path = ROOT):
        self.root = root
        self.ops = {oid: f"{v['contract']}#{oid}" for oid, v in g.operations().items()}
        self.screens = {s["id"] for _, s in g.screens()}
        ref = g.load_json(root / "handoff" / "schema-reference.json", {}) or {}
        self.tables = set(ref.get("cols") or {})
        # "stem.Schema" -> tables with a column built from it
        self.schema_tables: dict = {}
        for t, cols in (ref.get("cols") or {}).items():
            for c in cols or []:
                src = str(c.get("source") or "")
                parts = src.split(".")
                if len(parts) >= 2:
                    self.schema_tables.setdefault(".".join(parts[:2]), set()).add(t)
        for t, sch in (ref.get("origin") or {}).items():
            self.schema_tables.setdefault(str(sch), set()).add(t)
        self.schema_ops = self._schema_ops()
        by, _names = g.schemas()
        files = {stem: rel for stem, rel, _doc in g.contracts()}
        # "stem.Schema" -> its contract file, for a schema no table is built from and no operation reaches
        self.schema_file = {f"{stem}.{name}": files[stem] for stem, name in by if stem in files}
        pairs = g.load_yaml(PAIRS) if PAIRS.exists() else {}
        self.groups = {str(x.get("key")): [*(x.get("web") or []), *(x.get("app") or [])]
                       for x in (pairs or {}).get("groups") or [] if isinstance(x, dict) and x.get("key")}

    def _schema_ops(self) -> dict:
        """"stem.Schema" -> the operations whose parameters, request or responses reach it, through any number of
        $refs (measured 3 November 2026: the widest known schema finding reaches 23 operations)."""
        by, _names = g.schemas()
        refs = re.compile(r"""\$ref['"]?\s*:\s*['"]?([^'"\s,}]+)""")

        def refs_of(obj, stem):
            out = set()
            for r in refs.findall(json.dumps(obj)):
                m = re.search(r"([\w-]+)\.ya?ml", r)
                out.add((m.group(1) if m else stem, g.ref_name(r)))
            return out

        direct: dict = {}
        out: dict = {}
        for oid, v in g.operations().items():
            op = v["op"]
            frontier = refs_of({k: op.get(k) for k in ("parameters", "requestBody", "responses")}, v["contract"])
            seen = set(frontier)
            while frontier:
                nxt = set()
                for s in frontier:
                    if s not in direct:
                        direct[s] = refs_of(by.get(s) or {}, s[0])
                    nxt |= direct[s]
                frontier = nxt - seen
                seen |= frontier
            for s in seen:
                out.setdefault(f"{s[0]}.{s[1]}", set()).add(self.ops[oid])
        return out

        out: dict = {}
        for oid, v in g.operations().items():
            stem = v["contract"]
            op = v["op"]
            first = refs_of({k: op.get(k) for k in ("parameters", "requestBody", "responses")}, stem)
            seen = set(first)
            for s in first:
                body = by.get(s)
                if body:
                    seen |= refs_of(body, s[0])
            for s in seen:
                out.setdefault(f"{s[0]}.{s[1]}", set()).add(self.ops[oid])
        return out

    def token(self, tok: str) -> set:
        tok = tok.strip()
        if not tok:
            return set()
        if tok in self.screens:
            return {f"screen:{tok}"}
        if "#" in tok and tok.split("#", 1)[1] in self.ops and self.ops[tok.split("#", 1)[1]] == tok:
            return {f"operation:{tok}"}
        if tok in self.ops:
            return {f"operation:{self.ops[tok]}"}
        if tok in self.tables:
            return {f"table:{tok}"}
        if "/" in tok and (tok in self.files if self.files is not None else (self.root / tok).is_file()):
            return {f"file:{tok}"}
        if "." in tok:
            head, rest = tok.split(".", 1)
            if head in self.ops:                                   # op.field, op.schema.table
                out = {f"operation:{self.ops[head]}"}
                if rest in self.tables:
                    out.add(f"table:{rest}")
                return out
            parts = tok.split(".")
            schema = ".".join(parts[:2])                           # stem.Schema[.field]
            out = ({f"table:{t}" for t in self.schema_tables.get(schema, ())}
                   | {f"operation:{o}" for o in self.schema_ops.get(schema, ())})
            if not out and schema in self.schema_file:             # reached by nothing: the contract defining it
                out = {f"file:{self.schema_file[schema]}"}
            return out
        return set()

    def resolve(self, how: str, key: str) -> set:
        if how.startswith("adr:"):
            return {how}
        if how == "cited-doc":
            return self.token(key.split("|", 1)[0])
        if how == "guest-pair":
            return {f"screen:{s}" for s in self.groups.get(key, []) if s in self.screens}
        if how == "tokens":
            out = set()
            for tok in re.split(r"[:|]", key):
                out |= self.token(tok)
            return out
        return set()


def how_for(check: str, rule: str):
    m = RULE_MAP.get(check)
    if m is None:
        return None
    return m.get(rule) or m.get("*")


def build(pkg: Package | None = None, runners: dict | None = None, audit: dict | None = None,
          safe: dict | None = None) -> dict:
    """The index. Tests pass `runners` ({"guard": fn(name) -> export, "lines": fn(name, patterns) -> {"known": [...]}}),
    the package (Package.of) and the two baselines; bare, it reads and runs the package's own."""
    runners = runners or {}
    guard_fn = runners.get("guard", guard_known)
    lines_fn = runners.get("lines", line_known)
    pkg = pkg or Package()
    audit = (g.load_json(AUDIT_BASELINE, {}) or {}) if audit is None else audit
    safe = (g.load_json(SAFE_BASELINE, {}) or {}) if safe is None else safe
    guards = sorted(k for k, v in audit.items() if k != "_about" and isinstance(v, dict)
                    and any((v.get("rules") or {}).values()))
    liners = sorted(k for k, v in (safe.get("checkers") or {}).items() if (v or {}).get("known"))

    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        gf = {n: ex.submit(guard_fn, n) for n in guards}
        lf = {n: ex.submit(lines_fn, n, safe["checkers"][n]["known"]) for n in liners}
        exports = {n: f.result() for n, f in gf.items()}
        lines = {n: f.result() for n, f in lf.items()}

    findings, unmapped, rules, by_check, gone_keys = [], [], {}, {}, {}

    def take(check: str, rows: list, gone: int, source: str):
        stat = by_check.setdefault(check, {"source": source, "known": 0, "mapped": 0, "unmapped": 0, "gone": gone})
        for r in rows:
            rule, key, msg = str(r.get("rule")), str(r.get("key")), str(r.get("message") or "")
            stat["known"] += 1
            how = how_for(check, rule)
            arts = sorted(pkg.resolve(how, key)) if how else []
            if arts:
                stat["mapped"] += 1
                findings.append({"check": check, "rule": rule, "key": key, "message": msg, "artefacts": arts})
                continue
            stat["unmapped"] += 1
            why = NOT_AN_ARTEFACT.get((check, rule))
            unmapped.append({"check": check, "rule": rule, "key": key, "message": msg,
                             "why": why or ("its rule is not in build-known-findings.py RULE_MAP" if not how
                                            else "its key names nothing in the package (RULE_MAP " + how + ")"),
                             "excused": bool(why)})

    for n in guards:
        e = exports[n]
        if "error" in e:
            unmapped.append({"check": n, "rule": "-", "key": "-", "message": e["error"],
                             "why": "the guard did not export its findings", "excused": False})
            by_check[n] = {"source": "handoff/audit-baseline.json", "known": 0, "mapped": 0, "unmapped": 1, "gone": 0}
            continue
        rules[n] = e.get("rules") or {}
        gone_keys[n] = sorted(f"{r}|{k}" for r, ks in (e.get("gone") or {}).items() for k in ks)
        take(n, e.get("known") or [], sum(len(v) for v in (e.get("gone") or {}).values()), "handoff/audit-baseline.json")
    for n in liners:
        e = lines[n]
        take(n, e.get("known") or [], 0, "tools/refresh-safe-baseline.json")
        if e.get("unread"):
            for u in unmapped:
                if u["check"] == n and not u["excused"]:
                    u["why"] = "its checker is not in build-known-findings.py LINE_MAP"

    findings.sort(key=lambda f: (f["check"], f["rule"], f["key"]))
    unmapped.sort(key=lambda f: (f["check"], f["rule"], f["key"]))
    return {
        "_about": ("Every known finding of the gate's checks (baselined and still found) with the artefacts it is "
                   "about, in ADAM's link vocabulary. ADAM's pull lists the ones a ticket links as gaps already on "
                   "the list. Written by tools/build-known-findings.py; never edited by hand "
                   "(CHG-R14PUL-001). tools/check-known-findings.py holds it complete and current."),
        "sources": {
            "handoff/audit-baseline.json": {"sha256": sha(AUDIT_BASELINE), "checks": guards},
            "tools/refresh-safe-baseline.json": {"sha256": sha(SAFE_BASELINE), "checks": liners},
            "checks/baseline.json": {"indexed": False, "why": "check-binding-ratchet's counts per app, block and "
                                     "kind name no artefact"},
        },
        "counts": {"findings": len(findings), "unmapped": len(unmapped),
                   "excused": sum(1 for u in unmapped if u["excused"]), "byCheck": dict(sorted(by_check.items()))},
        "rules": dict(sorted(rules.items())),
        # Baseline entries no longer found, by check: counted, never shown on a pull (they are not gaps any more).
        "gone": {k: v for k, v in sorted(gone_keys.items()) if v},
        "unmapped": unmapped,
        "findings": findings,
    }


def dump(doc: dict) -> str:
    """The head readable, then one row per line: smaller to serve, and a diff names the findings that moved."""
    def line(v):
        return json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    head = {k: v for k, v in doc.items() if k not in ("gone", "unmapped", "findings")}
    out = json.dumps(head, indent=1, ensure_ascii=False)[:-2] + ",\n"
    out += ' "gone": {' + ",".join(f"\n  {line(k)}: {line(v)}" for k, v in doc["gone"].items()) + "\n },\n"
    for name in ("unmapped", "findings"):
        rows = ",".join(f"\n  {line(r)}" for r in doc[name])
        out += f' "{name}": [{rows}\n ]' + (",\n" if name == "unmapped" else "\n")
    return out + "}\n"


def main() -> int:
    g.force_utf8()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 when the file is not what this would write")
    a = ap.parse_args()
    doc = build()
    text = dump(doc)
    c = doc["counts"]
    if a.check:
        same = OUT.exists() and OUT.read_text(encoding="utf-8") == text   # universal newlines: a CRLF checkout agrees
        print(f"build-known-findings --check: {'current' if same else 'STALE'} ({c['findings']} findings)")
        return 0 if same else 1
    OUT.write_bytes(text.encode("utf-8"))
    per = ", ".join(f"{k} {v['mapped']}" for k, v in c["byCheck"].items())
    print(f"build-known-findings: {c['findings']} known finding(s) by artefact in {OUT.relative_to(ROOT).as_posix()} "
          f"({per}); {c['unmapped']} not mapped ({c['excused']} name no artefact by rule)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
