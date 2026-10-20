#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every read in `handoff/api-data-lineage.json` the columns it reads (`readColumns`).

**The lineage recorded reads per table, so a read view could not be narrow** (ADAM CR-004, Hrushikant Patkar,
ticket #27654 DB-READ-VIEWS; decided 12 October "Option C now, A later", fixed in r6 on 14 October, CHG-LIN-001).
DB-READ-VIEWS publishes one view per (reader module, owned table), `<table>_for_<reader module>`, "exposing only
the columns the reader's operations read". With table-level reads the deriver had nothing to narrow by, so the
views were built over every column, `pii.subject` included: Order, Access, Marketing, VenueOps, Wallet and F&B
each saw `date_of_birth`, `nationality` and the names whether their operations used them or not.

**What it writes.** On each lineage entry, `readColumns: {"<schema>.<table>": [column, ...]}` for the reads whose
columns this can establish. A read with no list is a read whose columns nothing states; its view keeps every
column, except over `pii.*`, where `check-read-columns` fails it (a personal-data view is always narrow). The
union of the lists of a reader module's operations is that module's view.

**Where a column comes from, strongest first** (each one a fact the package states, never a guess at intent):

  schema       a 2xx response schema persisted to the table (`x-ticvai-persistence`, followed through `$ref`,
               `allOf`, arrays and the `A + B` parent/child form): each property lands on the column
               `derive-schema` gives it (`x-ticvai-column`, else the naming standard), and only a column the
               table really has (`handoff/schema-reference.json`) is kept. A property marked
               `x-ticvai-persisted: false`, or one that lands on no column, is computed and adds none.
  projection   a response schema that persists nothing and says what it is worked out from
               (`x-ticvai-persistence: none — projection over a.b, c.d`, `none — computed from ...`): its fields
               that name a column of a table it names (`derive-schema`'s naming again) are read from that table.
  named        a field named for a table the operation reads and one of its columns (`productName` on an
               operation that reads `catalogue.product` is `catalogue.product.name`). Never on a pii table.
  personal     the fields that carry personal data from the erasable store (ADR-0023) by name — `displayName`,
               `guestName`, `holderName`, `email`, `dateOfBirth`... (`PII_FIELDS`), on an operation whose lineage
               reads that `pii.*` table. The pii store is storage-only (`handoff/schema-storage-only.md`): no
               contract schema persists to `pii.subject`, so this vocabulary is the only path from the wire to it.
  reference    a `pii.*` table the operation reads only to resolve or check an id: `subjectId` (or `*SubjectId`)
               in its response, request or path, or a returned column that references the table. Its key alone.
  override     `docs/active/read-columns-override.yaml`, for reads the contract cannot show (a notification
               that reads a name and a language and returns nothing). Kept small; each row says why.

**Not reached, so no list:** a read the lineage records and the response does not carry (most are rule checks a
write makes, which ADR-0055 as amended in r6 answers with a declared query, not a view), and a table a schema
declares (`A + B`) that no field of the response holds. The deriver prints the count by source and the remainder;
`--report` lists the cross-module reads left without one.

**Added to every list a source established:** the row key `id`; the columns a path or query parameter filters on
(`check-parameter-columns`' mapping: `<x>Id` on table `x` is `id`, a column named for the parameter is that
column); and the join keys between the operation's read tables (a column of one that references another, from
`schema-reference.json`). Row-level-security columns are not added: the policy is evaluated on the owner's table
beneath the view.

Runs in `refresh.sh` after `derive-schema.py`, because it compares fields with the columns that run produced.
Refreshed in place on every run: the lists are derived, never authored (an authored list goes in the override).

    python3 tools/derive-read-columns.py [--apply] [--report]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


def _yload(src):
    """YAML with the C loader, the pure one where a file defeats it (20 October 2026, CHG-R8GEN-016): the screen files
    are 25 MB and the pure loader took most of each refresh step's minute; the loaded data is the same."""
    text = src.read() if hasattr(src, "read") else src
    try:
        return yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    except Exception:
        return yaml.safe_load(text)

ROOT = Path(__file__).resolve().parents[1]
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"
REFERENCE = ROOT / "handoff" / "schema-reference.json"
DECOMPOSITION = ROOT / "handoff" / "service-decomposition.json"
OVERRIDE = ROOT / "docs" / "active" / "read-columns-override.yaml"
VERBS = ("get", "post", "put", "patch", "delete")


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "tools" / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DS = _load("derive-schema")

# **The wire's names for the personal data the erasable store holds** (ADR-0023). Field name -> (table, columns).
# A field matches only where it is not already a column of its own row, and only on an operation whose lineage
# reads that table. `name` alone is a person's name only beside a `subjectId` (a participant, a signatory).
PII_FIELDS = {
    "displayName": ("pii.subject", ["display_name"]),
    "guestName": ("pii.subject", ["display_name"]),
    "holderName": ("pii.subject", ["display_name"]),
    "customerName": ("pii.subject", ["display_name"]),
    "ticketHolder": ("pii.subject", ["display_name"]),
    "givenName": ("pii.subject", ["given_name"]),
    "firstName": ("pii.subject", ["given_name"]),
    "familyName": ("pii.subject", ["family_name"]),
    "lastName": ("pii.subject", ["family_name"]),
    "dateOfBirth": ("pii.subject", ["date_of_birth"]),
    "nationality": ("pii.subject", ["nationality"]),
    "preferredLanguage": ("pii.subject", ["preferred_language"]),
    "email": ("pii.subject_contact", ["subject_id", "kind", "value"]),
    "phone": ("pii.subject_contact", ["subject_id", "kind", "value"]),
    "mobile": ("pii.subject_contact", ["subject_id", "kind", "value"]),
    "contact": ("pii.subject_contact", ["subject_id", "kind", "value"]),
    "contactDetails": ("pii.subject_contact", ["subject_id", "kind", "value"]),
    "hasContactPoint": ("pii.subject_contact", ["subject_id", "kind"]),
}
PERSON_NAME = ("pii.subject", ["display_name"])      # `name` beside a `subjectId`
SCOPE_IDS = {"venue", "region", "brand", "country", "scope", "org_unit", "tenant_scope"}
_PROJECTION = re.compile(r"^none\b.*\b(projection|computed|aggregated|union|composed|derived)\b", re.I | re.S)
_TABLE = re.compile(r"\b([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)\b")


def _ref_name(node) -> str | None:
    r = node.get("$ref") if isinstance(node, dict) else None
    # a local ref and a cross-contract one (`../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion`)
    # alike: schema names are registered once across every contract
    return r.rsplit("/", 1)[-1] if isinstance(r, str) and "#/components/schemas/" in r else None


class Package:
    """The contracts, the tables and their columns, read once."""

    def __init__(self):
        self.defs: dict = {}
        self.ops: dict = {}
        for c in sorted((ROOT / "contracts").rglob("*.yaml")):
            try:
                doc = _yload(c.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            for n, s in ((doc.get("components") or {}).get("schemas") or {}).items():
                prev = self.defs.get(n)
                if prev is None or (DS._is_alias(prev) and not DS._is_alias(s)):
                    self.defs[n] = s
            for path, item in (doc.get("paths") or {}).items():
                for verb, op in (item or {}).items():
                    if verb in VERBS and isinstance(op, dict) and op.get("operationId"):
                        self.ops[op["operationId"]] = (c.stem, path, verb, op)
        # schema -> its tables, split on `+` (derive-lineage's persistence_map); head table for derive-schema
        self.persist: dict = {}
        for n, s in self.defs.items():
            t = DS.persistence_of(s)
            if not isinstance(t, str):
                continue
            t = t.strip('"').strip()
            if t.lower().startswith("none"):
                continue
            parts = [x.strip() for x in t.split("+") if x.strip() and "." in x and "—" not in x]
            if parts:
                self.persist[n] = parts
        self.head = {n: ts[0] for n, ts in self.persist.items()}
        ref = json.loads(REFERENCE.read_text(encoding="utf-8")) if REFERENCE.exists() else {}
        self.cols: dict = {}
        self.refs: dict = {}
        for t, rows in (ref.get("cols") or {}).items():
            self.cols[t] = {r.get("column") for r in rows if r.get("column")}
            self.refs[t] = {r["column"]: r["references"] for r in rows if r.get("column") and r.get("references")}
        self.renamed = {(r["table"], r["from"]): r["to"] for r in DS._declared_renames("COLUMN_RENAMES")}

    # -- one property -> one column -------------------------------------------------------------------
    def column(self, table: str, prop: str, spec) -> str | None:
        """The column `prop` lands on in `table`, or None where it lands on none (computed, not stored)."""
        have = self.cols.get(table) or set()
        if isinstance(spec, dict) and spec.get("x-ticvai-persisted") is False:
            return None
        chosen = spec.get("x-ticvai-column") if isinstance(spec, dict) else None
        ptype, fk = DS.resolve_type(spec if isinstance(spec, dict) else {}, self.defs, self.head)
        s = DS.snake(prop)
        cands = [chosen] if chosen else []
        cands += [DS.conventional_name(s, ptype or "text", fk), s, s + "_id"]
        if s.endswith("_ref"):
            cands.append(s[:-4] + "_id")
        for c in cands:
            if not c:
                continue
            c = self.renamed.get((table, c), c)
            if c in have:
                return c
        return None

    def declared_children(self, schema: str) -> dict:
        """Array property -> child table for a schema persisted as `A + B (+ C)`, paired as `derive-schema` pairs
        them: the array named for the child exactly, then by prefix, then by the most letters in common."""
        tables = self.persist.get(schema) or []
        if len(tables) < 2:
            return {}
        props = DS.properties_of(self.defs.get(schema) or {}, self.defs)
        arrays = [k for k, v in props.items() if isinstance(v, dict) and v.get("type") == "array"
                  and isinstance(v.get("items"), dict) and v.get("x-ticvai-persisted") is not False
                  and _ref_name(v["items"]) not in self.persist]
        out = {}
        parent = tables[0].split(".", 1)[1]
        for child in tables[1:]:
            free = [k for k in arrays if k not in out]
            if not free:
                break
            tail = child.split(".", 1)[1].replace(parent + "_", "")
            exact = [k for k in free if DS.snake(k).rstrip("s") in (tail, tail.split("_")[-1])]
            prefix = [k for k in free if DS.snake(k).startswith(tail) or tail.startswith(DS.snake(k).rstrip("s"))]
            key = (exact or prefix or [max(free, key=lambda k: len(set(DS.snake(k)) & set(tail)))])[0]
            out[key] = child
        return out

    def child_table(self, schema: str, head: str, arr: str) -> str | None:
        """The table an array property's rows live in: a declared `A + B` half, else `<head>_<singular>`."""
        sing = DS.snake(arr)
        sing = sing[:-3] + "y" if sing.endswith("ies") else (sing[:-1] if sing.endswith("s") else sing)
        sch, name = head.split(".", 1)
        if self.persist.get(schema, [None])[0] == head:
            hit = self.declared_children(schema).get(arr)
            if hit:
                return hit
        toks = name.split("_")
        for k in range(len(toks), 0, -1):
            cand = "%s.%s_%s" % (sch, "_".join(toks[:k]), sing)
            if cand in self.cols:
                return cand
        return None


class Walk:
    """One operation's 2xx responses, walked into table -> columns, plus the fields that land on no column."""

    def __init__(self, pkg: Package):
        self.p = pkg
        self.acc: dict = defaultdict(set)        # table -> columns established by a persisted schema
        self.proj: dict = defaultdict(set)       # table -> columns established by a projection's fields
        self.loose: list = []                    # (field name, sibling names) that landed on no column
        self.fields: list = []                   # (field name, sibling names) for every field walked
        self.seen: set = set()

    def schema(self, name: str, depth: int):
        if name in self.seen or depth > 12:
            return
        self.seen.add(name)
        body = self.p.defs.get(name)
        if not isinstance(body, dict):
            return
        props = DS.properties_of(body, self.p.defs)
        if name in self.p.persist:
            head = self.p.persist[name][0]
            self.rows(name, head, props, depth)
            return
        tag = DS.persistence_of(body)
        over = []
        if isinstance(tag, str) and _PROJECTION.search(tag.strip()):
            over = [t for t in _TABLE.findall(tag) if t in self.p.cols]
        # a projection composed over a stored row (`TableState` is `TableDefinition` plus a visit) reads that row
        for part in body.get("allOf") or []:
            if _ref_name(part):
                self.schema(_ref_name(part), depth + 1)
        self.free(props, depth, over)
        for k in ("oneOf", "anyOf"):
            for part in body.get(k) or []:
                self.node(part, depth + 1)
        if isinstance(body.get("items"), dict):          # a named array (`DenominationCount` of `CashCountLine`)
            self.node(body["items"], depth + 1)

    def rows(self, schema: str, table: str, props: dict, depth: int):
        """Properties of a persisted schema: its table's columns, its children's rows, its nested refs."""
        names = set(props)
        self.fields += [(k, names) for k in props]
        for prop, spec in props.items():
            if not isinstance(spec, dict):
                continue
            if spec.get("type") == "array" and isinstance(spec.get("items"), dict):
                items = spec["items"]
                iname = _ref_name(items)
                col = self.p.column(table, prop, spec)        # a value list stored as text[] on the row
                if col:
                    self.acc[table].add(col)
                if iname and iname in self.p.persist:
                    self.schema(iname, depth + 1)
                    continue
                child = self.p.child_table(schema, table, prop)
                body = self.p.defs.get(iname) if iname else items
                iprops = DS.properties_of(body, self.p.defs) if isinstance(body, dict) else {}
                if child and iprops:
                    self.acc[child] |= {"id"} & (self.p.cols.get(child) or set())
                    self.rows(iname or schema, child, iprops, depth + 1)
                elif child:
                    # a value list held as rows (`Plan.licensedModules` in `subscription.plan_module`): the row's
                    # key and the one value column `derive-schema` names for it
                    s = DS.snake(prop)
                    self.acc[child] |= {"id", s, s.rstrip("s"), s[:-3] + "y"} & (self.p.cols.get(child) or set())
                elif not col:
                    if iname:
                        self.schema(iname, depth + 1)
                    else:
                        self.node(items, depth + 1)
                continue
            col = self.p.column(table, prop, spec)
            if col:
                self.acc[table].add(col)
            else:
                self.loose.append((prop, names))
            # an embedded object is read too: a persisted one from its own table, a value object for its refs
            sub = _ref_name(spec) or next((_ref_name(x) for x in (spec.get("allOf") or spec.get("oneOf") or [])
                                           if _ref_name(x)), None)
            if sub:
                self.schema(sub, depth + 1)
            elif spec.get("properties") or spec.get("allOf") or spec.get("oneOf"):
                self.node(spec, depth + 1)

    def free(self, props: dict, depth: int, over: list):
        """Properties of a schema that persists nothing: matched to a projected table, else loose."""
        names = set(props)
        self.fields += [(k, names) for k in props]
        for prop, spec in props.items():
            if not isinstance(spec, dict):
                continue
            hit = False
            for t in over:
                col = self.p.column(t, prop, spec)
                if col:
                    self.proj[t].add(col)
                    hit = True
            if not hit:
                self.loose.append((prop, names))
            self.node(spec, depth + 1)

    def node(self, node, depth: int):
        if not isinstance(node, dict) or depth > 12:
            return
        n = _ref_name(node)
        if n:
            self.schema(n, depth + 1)
            return
        for k in ("allOf", "oneOf", "anyOf"):
            for part in node.get(k) or []:
                self.node(part, depth + 1)
        if isinstance(node.get("items"), dict):
            self.node(node["items"], depth + 1)
        if node.get("properties"):
            self.free(node["properties"], depth + 1, [])
        for k in ("content", "schema"):
            if isinstance(node.get(k), dict):
                self.node(node[k], depth + 1)
        for k, v in node.items():
            if re.match(r"^(application|text)/", str(k)):
                self.node(v, depth + 1)


def overrides() -> dict:
    """(operation, table) -> (columns, why) from docs/active/read-columns-override.yaml."""
    if not OVERRIDE.exists():
        return {}
    doc = _yload(OVERRIDE.read_text(encoding="utf-8")) or {}
    out = {}
    for r in doc.get("reads") or []:
        if isinstance(r, dict) and r.get("operation") and r.get("table"):
            out[(str(r["operation"]), str(r["table"]))] = ([str(c) for c in r.get("columns") or []],
                                                           str(r.get("why") or ""))
    return out


def derive(pkg: Package, lin: dict, over: dict):
    """operation -> {table: sorted columns}, and operation -> {table: how} for every table read."""
    out, how = {}, {}
    for oid, e in lin.items():
        reads = [t for t in (e.get("reads") or []) if ":" not in t and "." in t]
        if not reads or oid not in pkg.ops:
            continue
        _stem, path, _verb, op = pkg.ops[oid]
        w = Walk(pkg)
        resp = {k: v for k, v in (op.get("responses") or {}).items() if str(k).startswith("2")}
        for r in resp.values():
            w.node(r, 0)
        cols, src = defaultdict(set), {}
        for t in reads:
            if w.acc.get(t):
                cols[t] |= w.acc[t]
                src[t] = "schema"
            elif w.proj.get(t):
                cols[t] |= w.proj[t]
                src[t] = "projection"
        # personal data by name, on the pii tables the operation reads: any field of the response, because a row
        # that also keeps a copy (`marketing.guest_profile.display_name`) does not make the pii read go away
        for prop, sib in w.fields:
            hit = PII_FIELDS.get(prop) or (PERSON_NAME if prop == "name" and "subjectId" in sib else None)
            if hit and hit[0] in reads:
                cols[hit[0]] |= {c for c in hit[1] if c in (pkg.cols.get(hit[0]) or ())}
                src.setdefault(hit[0], "personal")
        # a field named for a table the operation reads and one of its columns (`productName` on an operation that
        # reads `catalogue.product` is `catalogue.product.name`); never a pii table, whose fields are named above
        for t in reads:
            if t in src or t.startswith("pii."):
                continue
            have = pkg.cols.get(t) or set()
            short = t.split(".", 1)[1]
            heads = {short, short.split("_")[-1]}
            named = set()
            for prop, _sib in w.loose:
                s = DS.snake(prop)
                for h in heads:
                    if s.startswith(h + "_"):
                        rest = s[len(h) + 1:]
                        if rest != "id" and rest in have:
                            named.add(rest)
                        elif s in have and not s.endswith("_id"):
                            named.add(s)
            if named:
                cols[t] |= named
                src[t] = "named"
        # a pii table read only to resolve an id the response exposes: its key. `subjectId` is the package's
        # name for that id wherever it appears ("Opaque reference. Personal data lives in the separately erasable
        # store"), and a column that references the table says the same.
        # The id may also arrive in the request (`transferWalletBalance`'s `toSubjectId`) or the path.
        if "pii.subject" in reads and "pii.subject" not in src:
            asked = Walk(pkg)
            asked.node(op.get("requestBody"), 0)
            names = [p for p, _ in w.fields + asked.fields] + [str(p.get("name")) for p in op.get("parameters") or []
                                                              if isinstance(p, dict)] + re.findall(r"\{(\w+)\}", path)
            if any(p == "subjectId" or p.endswith("SubjectId") or p == "subjectIds" for p in names):
                src["pii.subject"] = "reference"
        for t in reads:
            if t.startswith("pii.") and t not in src:
                for t1 in list(src):
                    if any(pkg.refs.get(t1, {}).get(c) == t for c in cols[t1]):
                        src[t] = "reference"
                        break
        for t in reads:
            if (oid, t) in over:
                cols[t] |= set(over[(oid, t)][0])
                src[t] = "override" if t not in src else src[t] + "+override"
        # what every established list carries: the key, the parameters' columns, the joins between reads
        params = [p.get("name") for p in op.get("parameters") or [] if isinstance(p, dict)
                  and p.get("in") in ("path", "query")] + re.findall(r"\{(\w+)\}", path)
        for t in list(src):
            have = pkg.cols.get(t) or set()
            if "id" in have:
                cols[t].add("id")
            short = t.split(".", 1)[1]
            for n in {str(x) for x in params if x}:
                s = DS.snake(n)
                if s in have:
                    cols[t].add(s)
                elif s.endswith("_id") and (s[:-3] == short or short.endswith("_" + s[:-3])) and "id" in have:
                    cols[t].add("id")
            for c, target in (pkg.refs.get(t) or {}).items():
                if target in src and target != t and c in have:
                    cols[t].add(c)
        out[oid] = {t: sorted(cols[t]) for t in sorted(src) if cols[t]}
        how[oid] = {t: src.get(t) for t in reads}
    return out, how


def owners() -> dict:
    dec = json.loads(DECOMPOSITION.read_text(encoding="utf-8")) if DECOMPOSITION.exists() else {}
    return {sch: name for name, s in (dec.get("services") or {}).items() for sch in (s.get("schemas") or [])}


def coverage(lin: dict, how: dict) -> dict:
    """Counts of reads with a list, by source, and of reads without one, by reason; all and cross-module."""
    own = owners()
    res = {"all": Counter(), "cross": Counter(), "pii_cross": Counter()}
    for oid, e in lin.items():
        for t in (e.get("reads") or []):
            if ":" in t or "." not in t:
                continue
            k = (how.get(oid) or {}).get(t) or "none"
            res["all"][k] += 1
            o = own.get(t.split(".", 1)[0])
            if o and o != e.get("service"):
                res["cross"][k] += 1
                if t.startswith("pii."):
                    res["pii_cross"][k] += 1
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true", help="list the cross-module reads left without a list")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    lin = json.loads(LINEAGE.read_text(encoding="utf-8"))
    pkg = Package()
    over = overrides()
    got, how = derive(pkg, lin, over)
    cov = coverage(lin, how)
    for k, label in (("all", "every read"), ("cross", "cross-module reads"), ("pii_cross", "cross-module pii reads")):
        n = sum(cov[k].values())
        listed = n - cov[k]["none"]
        print("%-24s %5d  with a column list %5d (%.0f%%)  %s" % (
            label, n, listed, 100.0 * listed / max(1, n),
            ", ".join("%s %d" % (s, c) for s, c in sorted(cov[k].items()))))
    if a.report:
        own = owners()
        for oid, e in sorted(lin.items()):
            for t in e.get("reads") or []:
                o = own.get(t.split(".", 1)[0]) if "." in t else None
                if ":" not in t and o and o != e.get("service") and not (how.get(oid) or {}).get(t):
                    print("   no list  %-40s %-34s %s" % (oid, t, e.get("service")))
    changed = 0
    for oid, e in lin.items():
        want = got.get(oid) or {}
        if want and e.get("readColumns") != want:
            e["readColumns"] = want
            changed += 1
        elif not want and "readColumns" in e:
            del e["readColumns"]
            changed += 1
    if not a.apply:
        print("  %d entr(ies) would change - pass --apply" % changed)
        return 0
    if changed:
        LINEAGE.write_text(json.dumps(lin, indent=1, ensure_ascii=False), encoding="utf-8")
    print("  %d entr(ies) given or refreshed readColumns -> handoff/%s" % (changed, LINEAGE.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
