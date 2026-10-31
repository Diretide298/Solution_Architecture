#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A database's schema against the package's intended state, object by object, both ways (CHG-R12LV-001).

**Why** (30 October 2026). Live's schema was compared with the package's r11 by hand-run scripts: schema-only dumps,
a reference built from backend/, one line per object on both sides, every difference sorted into a bucket. It found
r11 missing on live outside five modules, 27 hand changes still open and 13 objects live had that the package never
recorded. The lead: "Yes, both": make it a package tool that every release runs, so a database drifting from the
package (either way) is found by a tool and not by a developer; and run it on a second dump, of a database the
developers' Migrator builds from their repository's db/ folder alone. This is that tool. It takes any target dump.

**The intended state** is the package's built SQL (backend/<db>/*.sql) PLUS the changes derive-ddl leaves for a
person (handoff/migration-review.md: derive-ddl writes additive changes only). So every review row is judged on the
target (done / open / table not built ...), and a difference that rides on a done hand change (a dropped column's key
and index, a retyped column's new foreign key or check, the composite venue keys behind a hand-added unique key) is
counted as done, not drift.

**Lessons already paid for, each held by the self-test:**
  - Postgres `name` concatenated with `name` is `name` (63 characters): every key is built from `::text` casts, or
    long keys are cut and look like collisions (the 30 October "57 collisions" were this).
  - A key the package creates NOT VALID and the target has validated is the same key: counted, never a difference.
  - Function bodies are compared by md5 of pg_get_functiondef.
  - Both sides go through the same snapshot query, on the same Postgres major as the target (live is 17).
  - The reference is built the way a cell is provisioned: control's files in initdb's order, then
    backend/provision-tenant.sh itself, from a staged copy of backend/.
  - Tables the target lacks are classified by their ticket (MIGRATIONS.md: table -> task; pms-map.json: task -> work
    package; adam-links.json, or the tickets file given: work package -> status): a later block's task not on the
    board, on the board and not started, no migration creates it, or STARTED OR CLOSED (only the last is a gap).

**The one documented adjustment** (CHG-R6-001). The frozen r1 010-pii.sql types pii.subject.kind and
pii.subject_contact.kind with enum types no file creates, so provision-tenant.sh stops there. CHG-R6-001 decided both
are text NOT NULL with subject_kind_chk / subject_contact_kind_chk, and migration-review.md carries that as a
`column changed` row. The build applies a review row's target text to a column only when the column is typed with a
`<schema>.<type>` no package file creates (`undefined_type_adjustments`), so it switches itself off the day the
package provisions cleanly. An undefined type with no decided review row stops the build. The report names every
adjustment it made.

**Its findings are never baselined.** There is no baseline, acknowledgement or exemption file: each run judges the
dumps it is given from scratch, and the report goes to the lead (docs/active/release-runbook.md, step 6a).

    python tools/check-schema-drift.py                       # self-test, then the package inputs parse (run-checks)
    python tools/check-schema-drift.py --self-test           # the self-test alone (no Docker)
    python tools/check-schema-drift.py run --label live --tenant-dump live-tenant.sql --control-dump live-control.sql \\
        --out DIR [--tickets FILE] [--prefix NAME-] [--keep]  # everything below, in one throwaway container
    python tools/check-schema-drift.py reference --out DIR   # build the package reference and snapshot it
    python tools/check-schema-drift.py snapshot --dump FILE --out FILE.tsv   # restore a schema-only dump, snapshot it
    python tools/check-schema-drift.py diagnose --reference DIR --target-tenant T.tsv --target-control C.tsv \\
        --label live --out DIR [--tickets FILE]               # no Docker: the JSON and the markdown report
    python tools/check-schema-drift.py report --json DIR/drift-live.json      # the markdown again, from the JSON

A dump is `pg_dump --schema-only` of one database, plain SQL or custom format (-Fc), from any server; the container
image is pgvector/pgvector:pg<major>, the major read from the dump's header (or --pg-major). Docker is needed only
for run, reference and snapshot.
"""
import argparse
import collections
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
REVIEW = ROOT / "handoff" / "migration-review.md"
MIGRATIONS_MD = ROOT / "handoff" / "service-docs" / "backend" / "MIGRATIONS.md"
PMS_MAP = ROOT / "handoff" / "service-docs" / "pms-map.json"
ADAM_LINKS = ROOT / "handoff" / "service-docs" / "adam-links.json"
DATABASES = ("tenant", "control")
IMAGE = "pgvector/pgvector:pg{major}"
PGUSER = "ticvai"
REF_DB = {"tenant": "ref_tenant", "control": "ref_control"}

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from audit_guard import NOT_STARTED   # one meaning of "started" in the package (CHG-CRF-001)
except Exception:                          # audit_guard needs PyYAML; the statuses are the same three
    NOT_STARTED = ("New", "On hold", "Rejected")

# =====================================================================================================================
# The snapshot: one line per schema object, "kind<TAB>key<TAB>definition", the same query on both sides.
# Every key is concatenated from ::text casts (a `name || name` is a `name` and is cut at 63 characters).
# =====================================================================================================================
SNAPSHOT_SQL = r"""
\pset format unaligned
\pset tuples_only on
\pset fieldsep '\t'
\pset footer off
WITH s AS (
  SELECT oid, nspname::text AS nsp FROM pg_namespace
   WHERE nspname NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
     AND nspname NOT LIKE 'pg_temp%' AND nspname NOT LIKE 'pg_toast_temp%'
)
SELECT kind, key, regexp_replace(def, '[[:space:]]+', ' ', 'g') FROM (
  SELECT 'schema', s.nsp, '' FROM s
UNION ALL
  SELECT 'extension', extname::text, '' FROM pg_extension WHERE extname <> 'plpgsql'
UNION ALL
  SELECT CASE c.relkind WHEN 'r' THEN 'table' WHEN 'p' THEN 'table' WHEN 'v' THEN 'view'
                        WHEN 'm' THEN 'matview' WHEN 'S' THEN 'sequence' END,
         s.nsp || '.' || c.relname::text,
         CASE WHEN c.relkind = 'p' THEN 'partitioned ' || pg_get_partkeydef(c.oid)
              WHEN c.relkind IN ('v', 'm') THEN md5(pg_get_viewdef(c.oid)) ELSE '' END
    FROM pg_class c JOIN s ON s.oid = c.relnamespace
   WHERE c.relkind IN ('r', 'p', 'v', 'm', 'S') AND NOT c.relispartition
UNION ALL
  SELECT 'column', s.nsp || '.' || c.relname::text || '.' || a.attname::text,
         format_type(a.atttypid, a.atttypmod)
         || CASE WHEN a.attnotnull THEN ' not null' ELSE '' END
         || COALESCE(' default ' || pg_get_expr(d.adbin, d.adrelid), '')
         || CASE WHEN a.attgenerated = 's' THEN ' generated' ELSE '' END
    FROM pg_attribute a
    JOIN pg_class c ON c.oid = a.attrelid JOIN s ON s.oid = c.relnamespace
    LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
   WHERE c.relkind IN ('r', 'p', 'v', 'm') AND NOT c.relispartition AND a.attnum > 0 AND NOT a.attisdropped
UNION ALL
  SELECT 'constraint', s.nsp || '.' || c.relname::text || '.' || k.conname::text, pg_get_constraintdef(k.oid)
    FROM pg_constraint k JOIN pg_class c ON c.oid = k.conrelid JOIN s ON s.oid = c.relnamespace
   WHERE NOT c.relispartition AND k.contype <> 'n'
UNION ALL
  SELECT 'index', s.nsp || '.' || i.relname::text,
         regexp_replace(pg_get_indexdef(i.oid), '^CREATE (UNIQUE )?INDEX \S+ ON (ONLY )?', 'CREATE \1INDEX ON ')
    FROM pg_index x JOIN pg_class i ON i.oid = x.indexrelid JOIN pg_class c ON c.oid = x.indrelid
    JOIN s ON s.oid = i.relnamespace
   WHERE NOT c.relispartition AND NOT EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conindid = x.indexrelid
                                              AND k.contype IN ('p', 'u', 'x'))
UNION ALL
  SELECT 'rls', s.nsp || '.' || c.relname::text,
         CASE WHEN c.relrowsecurity THEN 'enabled' ELSE 'off' END
         || CASE WHEN c.relforcerowsecurity THEN ' forced' ELSE '' END
    FROM pg_class c JOIN s ON s.oid = c.relnamespace
   WHERE c.relkind IN ('r', 'p') AND NOT c.relispartition
UNION ALL
  SELECT 'policy', s.nsp || '.' || c.relname::text || '.' || p.polname::text,
         p.polcmd::text || ' ' || COALESCE(pg_get_expr(p.polqual, p.polrelid), '') || ' | '
         || COALESCE(pg_get_expr(p.polwithcheck, p.polrelid), '')
    FROM pg_policy p JOIN pg_class c ON c.oid = p.polrelid JOIN s ON s.oid = c.relnamespace
UNION ALL
  SELECT 'function', s.nsp || '.' || p.proname::text || '(' || pg_get_function_identity_arguments(p.oid) || ')',
         md5(pg_get_functiondef(p.oid))
    FROM pg_proc p JOIN s ON s.oid = p.pronamespace
   WHERE p.prokind IN ('f', 'p')
     AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid = p.oid AND d.deptype = 'e')
UNION ALL
  SELECT 'trigger', s.nsp || '.' || c.relname::text || '.' || t.tgname::text,
         regexp_replace(pg_get_triggerdef(t.oid), '^CREATE (CONSTRAINT )?TRIGGER \S+ ', '')
    FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid JOIN s ON s.oid = c.relnamespace
   WHERE NOT t.tgisinternal AND NOT c.relispartition
UNION ALL
  SELECT 'type', s.nsp || '.' || t.typname::text,
         t.typtype::text || COALESCE(' ' || (SELECT string_agg(e.enumlabel::text, ',' ORDER BY e.enumsortorder)
                                               FROM pg_enum e WHERE e.enumtypid = t.oid), '')
         || CASE WHEN t.typtype = 'd' THEN ' ' || format_type(t.typbasetype, t.typtypmod) ELSE '' END
    FROM pg_type t JOIN s ON s.oid = t.typnamespace
   WHERE t.typtype IN ('e', 'd', 'c') AND NOT EXISTS (SELECT 1 FROM pg_class c WHERE c.oid = t.typrelid
                                                      AND c.relkind <> 'c')
     AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid = t.oid AND d.deptype = 'e')
) o(kind, key, def)
WHERE kind IS NOT NULL
ORDER BY 1, 2;
"""

NAME_COLUMNS = ("nspname", "relname", "conname", "attname", "polname", "tgname", "typname", "proname", "extname")


# =====================================================================================================================
# The package's own inputs: provisioning order, statements per file, review rows, table -> ticket.
# =====================================================================================================================
def provision_order(names):
    """The order a cell applies a database's files: provision-tenant.sh's `for f in tenant/*.sql` and initdb's
    `/docker-entrypoint-initdb.d/*` are shell globs, sorted bytewise in the C locale (V0103__ before V0103a__)."""
    return sorted((n for n in names if n.endswith(".sql")), key=lambda n: n.encode("utf-8"))


def strip_comments(text):
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("--"))


def split_statements(text):
    return [st for st in re.split(r";\s*\n(?=\S)", strip_comments(text)) if st.strip()]


def is_forward(fname):
    return bool(re.match(r"V\d{4}", fname))


def read_backend(backend=BACKEND):
    """{db: [(file name, text)]} in provisioning order."""
    out = {}
    for db in DATABASES:
        d = backend / db
        names = provision_order(p.name for p in d.glob("*.sql")) if d.is_dir() else []
        out[db] = [(n, (d / n).read_text(encoding="utf-8")) for n in names]
    return out


def table_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def review_rows(text):
    """migration-review.md's table: kind, database, object, change, what a person does."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or line.startswith("| Kind") or line.startswith("|---"):
            continue
        cells = table_cells(line)
        if len(cells) >= 5:
            rows.append({"kind": cells[0], "db": cells[1], "object": cells[2].strip("`"),
                         "change": cells[3], "todo": cells[4]})
    return rows


def migration_tasks(text):
    """MIGRATIONS.md: {table: task} from Tables and Forward migrations; {table: why} from Tables no migration creates."""
    tasks, nomig, section = {}, {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = table_cells(line)
        if section == "Tables" and len(cells) > 2 and cells[0].startswith(("MIG", "VM")):
            tasks.setdefault(cells[1].strip("`"), cells[0])
        elif section and section.startswith("Forward migrations") and len(cells) > 6 and cells[2] != "Task":
            for t in cells[6].split(","):
                if t.strip():
                    tasks.setdefault(t.strip().strip("`"), cells[2])
        elif section and section.startswith("Tables no migration") and cells[0] != "Table" and len(cells) > 3:
            nomig[cells[0].strip("`")] = cells[3]
    return tasks, nomig


def load_ticket_status(path=None):
    """{work package id (str): status}. adam-links.json (the statuses read at the last release) unless a tickets file
    is given: adam-links.json's shape, {id: status}, or an OpenProject snapshot ({packages: {id: {_links: {status}}}})."""
    p = Path(path) if path else ADAM_LINKS
    if not p.exists():
        return {}, f"{p} (missing)"
    d = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    if isinstance(d, dict) and isinstance(d.get("links"), list):
        for r in d["links"]:
            if r.get("key") and r.get("status"):
                out[str(r["key"])] = r["status"]
        read = d.get("statusReadAt", "")
    elif isinstance(d, dict) and isinstance(d.get("packages"), dict):
        for i, w in d["packages"].items():
            st = (((w or {}).get("_links") or {}).get("status") or {}).get("title")
            if st:
                out[str(i)] = st
        read = d.get("readAt", "")
    elif isinstance(d, dict):
        out = {str(k): v for k, v in d.items() if isinstance(v, str)}
        read = ""
    else:
        raise SystemExit(f"check-schema-drift: {p}: not a tickets file this tool reads")
    try:
        shown = p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        shown = str(p)
    return out, f"{shown}" + (f" (statuses read {read})" if read else "")


# =====================================================================================================================
# The one documented adjustment (CHG-R6-001), keyed so it switches itself off.
# =====================================================================================================================
COL_LINE = re.compile(r"^(?P<indent>\s+)(?P<col>[a-z_][a-z0-9_]*)\s+(?P<type>[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*)"
                      r"(?P<rest>[^,\n]*)(?P<end>,?)\s*$", re.M)
CREATE_TABLE = re.compile(r"CREATE TABLE (?:IF NOT EXISTS )?([a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*)\s*\(", re.I)


def undefined_type_adjustments(files, rows):
    """[(file, line before, line after, review object)] for every column typed `<schema>.<type>` that no package file
    creates (CREATE TYPE / CREATE DOMAIN), rewritten to its `column changed` review row's target. Empty once the
    package provisions cleanly. Raises ValueError for an undefined type no review row decides."""
    created = set()
    for _f, text in files:
        for m in re.finditer(r"CREATE\s+(?:TYPE|DOMAIN)\s+(?:IF NOT EXISTS\s+)?([a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*)",
                             strip_comments(text), re.I):
            created.add(m.group(1).lower())
    decided = {r["object"]: r for r in rows if r["kind"] == "column changed"}
    out, undecided = [], []
    for fname, text in files:
        spans = []
        for m in CREATE_TABLE.finditer(text):
            end = text.find("\n);", m.end())
            spans.append((m.end(), end if end >= 0 else len(text), m.group(1)))
        for m in COL_LINE.finditer(text):
            ty = m.group("type").lower()
            if ty in created or ty.split(".")[0] in ("pg_catalog", "public"):
                continue
            owner = [t for a, b, t in spans if a <= m.start() < b]
            if not owner:
                continue                         # not a column of a CREATE TABLE (a function body, a comment)
            obj = f"{owner[-1]}.{m.group('col')}"
            row = decided.get(obj)
            target = None
            if row:
                parts = [p.strip().strip("`") for p in row["change"].split("->")]
                if len(parts) == 2 and ty in parts[0].lower():
                    target = parts[1]
            if not target:
                undecided.append(f"{fname}: {obj} {ty}")
                continue
            before = m.group(0).rstrip("\n")
            after = f"{m.group('indent')}{target}{m.group('end')}"
            out.append((fname, before, after, obj))
    if undecided:
        raise ValueError("a column is typed with a type no package file creates and no review row decides it: "
                         + "; ".join(undecided))
    return out


def provisioned_first(db, backend=BACKEND):
    """[(name, text)] of what provisioning runs before a database's own files: provision-tenant.sh creates the types the
    frozen tenant baseline names (CHG-R12DB-001), so a type it creates is created (CHG-R12INT-002)."""
    sh = Path(backend) / "provision-tenant.sh"
    return [(sh.name, sh.read_text(encoding="utf-8"))] if db == "tenant" and sh.exists() else []


def stage_backend(dst, backend=BACKEND, rows=None):
    """Copy backend/ to dst (the files provisioning reads) and apply the adjustments. Returns them."""
    rows = rows if rows is not None else review_rows(REVIEW.read_text(encoding="utf-8"))
    dst = Path(dst)
    for db in DATABASES:
        (dst / db).mkdir(parents=True, exist_ok=True)
        for p in (backend / db).glob("*.sql"):
            shutil.copyfile(p, dst / db / p.name)
    for sh in ("provision-tenant.sh",):
        # bash in the container reads LF only; a Windows checkout may carry CRLF
        (dst / sh).write_bytes((backend / sh).read_bytes().replace(b"\r\n", b"\n"))
    adjustments = []
    for db in DATABASES:
        files = [(n, (dst / db / n).read_text(encoding="utf-8")) for n in provision_order(
            p.name for p in (dst / db).glob("*.sql"))]
        for fname, before, after, obj in undefined_type_adjustments(provisioned_first(db, dst) + files,
                                                                    [r for r in rows if r["db"] in (db, "both")]):
            p = dst / db / fname
            text = p.read_text(encoding="utf-8")
            p.write_bytes(text.replace(before, after, 1).encode("utf-8"))
            adjustments.append({"db": db, "file": fname, "object": obj, "before": before.strip(),
                                "after": after.strip(), "decision": "CHG-R6-001"})
    return adjustments


# =====================================================================================================================
# Snapshots on disk
# =====================================================================================================================
def parse_snapshot(lines):
    """{(kind, key): def} and the (kind, key) pairs seen twice. With ::text keys there are none; if one appears it is
    reported, and both are kept apart by their definition (NOT VALID left out, so the two sides still meet)."""
    rows = [l.rstrip("\n").split("\t") for l in lines if l.strip() and not l.startswith("#")]
    rows = [r for r in rows if len(r) == 3]
    seen = collections.Counter((k, n) for k, n, _ in rows)
    out = {}
    for kind, key, d in rows:
        if seen[(kind, key)] > 1:
            key = f"{key} ~ {d.replace(' NOT VALID', '')}"
        out[(kind, key)] = d
    return out, sorted(f"{k} {n}" for (k, n), c in seen.items() if c > 1)


def read_snapshot(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    meta = {}
    for l in lines:
        if l.startswith("#") and ":" in l:
            k, _, v = l[1:].partition(":")
            meta[k.strip()] = v.strip()
    rows, coll = parse_snapshot(lines)
    return rows, coll, meta


def write_snapshot(path, text, meta):
    head = "".join(f"# {k}: {v}\n" for k, v in meta.items())
    Path(path).write_bytes((head + text.replace("\r\n", "\n")).encode("utf-8"))


# =====================================================================================================================
# The diagnosis
# =====================================================================================================================
def same_but_valid(a, b):
    return a.replace(" NOT VALID", "") == b.replace(" NOT VALID", "")


def table_of(kind, key, d):
    if kind == "index":
        m = re.search(r" ON (?:ONLY )?(\S+) ", d)
        return m.group(1) if m else None
    if kind in ("table", "rls"):
        return key
    if kind in ("column", "constraint", "policy", "trigger"):
        return ".".join(key.split(" ~ ")[0].split(".")[:2])
    return None


def leaf(kind, key):
    k = key.split(" ~ ")[0]
    if kind == "function":
        return k.split("(")[0].split(".")[-1]
    return k.split(".")[-1]


IDENT = re.compile(r'"?([a-z_][a-z0-9_]*)"?')


def columns_named(kind, key, d, table_cols):
    """The table's columns an object names: the column itself; a key's or index's own columns (a foreign key's local
    side only); any column a check, exclusion, policy or trigger expression mentions."""
    if kind == "column":
        return {leaf(kind, key)}
    text = d
    if kind == "constraint" and "REFERENCES" in d:
        text = d.split("REFERENCES")[0]
    elif kind == "index":
        text = d.split(" USING ", 1)[-1]
    return {w for w in IDENT.findall(text)} & table_cols


def fk_target(d):
    m = re.search(r"REFERENCES ([\w.]+)\(([^)]*)\)", d)
    if not m:
        return None
    return m.group(1), tuple(c.strip().strip('"') for c in m.group(2).split(","))


def key_columns(d):
    m = re.match(r"(?:UNIQUE|PRIMARY KEY) \(([^)]*)\)", d)
    return tuple(c.strip().strip('"') for c in m.group(1).split(",")) if m else None


TYPE_ALIASES = {"timestamptz": "timestamp with time zone", "timestamp": "timestamp without time zone",
                "int": "integer", "int4": "integer", "int8": "bigint", "int2": "smallint", "bool": "boolean",
                "float8": "double precision", "float4": "real", "varchar": "character varying", "char": "character",
                "timetz": "time with time zone", "decimal": "numeric"}


def norm_type(t):
    t = t.strip().lower()
    arr = ""
    while t.endswith("[]"):
        arr, t = arr + "[]", t[:-2]
    m = re.match(r"([a-z_ .]+?)\s*(\(.*\))?$", t)
    base, mod = (m.group(1), m.group(2) or "") if m else (t, "")
    base = TYPE_ALIASES.get(base.strip(), base.strip())
    return f"{base}{mod.replace(' ', '')}{arr}"


def parse_column_text(text):
    """`name type [NOT NULL] [DEFAULT x] [CONSTRAINT n CHECK (...)]` -> (name, type, not null, default, check name)."""
    m = re.match(r"(\w+)\s+(.+?)(?=\s+NOT NULL|\s+DEFAULT|\s+CONSTRAINT|\s+REFERENCES|\s*$)(.*)$", text.strip(), re.S)
    if not m:
        return None
    rest = m.group(3)
    dflt = re.search(r"DEFAULT\s+('(?:[^']|'')*'|[^\s]+)", rest)
    chk = re.search(r"CONSTRAINT (\w+) CHECK", rest)
    return {"name": m.group(1), "type": norm_type(m.group(2)), "notnull": "NOT NULL" in rest,
            "default": dflt.group(1) if dflt else None, "check": chk.group(1) if chk else None}


def snapshot_column(d):
    """A snapshot column definition -> (type, not null, default without its casts)."""
    m = re.match(r"(.*?)( not null)?( default (.*?))?( generated)?$", d)
    dflt = m.group(4)
    if dflt is not None:
        dflt = re.sub(r"::[a-z ]+(\[\])?", "", dflt).strip()
    return norm_type(m.group(1)), bool(m.group(2)), dflt


class Sides:
    def __init__(self, P, T):
        self.P, self.T = P, T
        self.ptab = {k[1] for k in P if k[0] == "table"}
        self.ttab = {k[1] for k in T if k[0] == "table"}
        self.cols = collections.defaultdict(set)
        for side in (P, T):
            for (kind, key) in side:
                if kind == "column":
                    t, c = key.rsplit(".", 1)
                    self.cols[t].add(c)


def judge_review(row, S):
    """One hand change on the target: (status, keys it explains). status is one of
    done, open, kept, decision, table not built, column not built, for a person, unjudged."""
    kind, obj, T = row["kind"], row["object"], S.T
    explains = set()
    if kind == "file changed":
        return "for a person", explains
    if kind == "statement dropped":
        tabs = [t.strip() for t in obj.split(",")]
        return ("table not built" if any(t not in S.ttab for t in tabs) else "for a person"), explains
    if kind == "table dropped":
        return ("done" if obj not in S.ttab else "open"), explains
    if kind == "index duplicates a unique index":
        d = S.P.get(("index", obj)) or T.get(("index", obj)) or ""
        t = table_of("index", obj, d)
        if t and t not in S.ttab:
            return "table not built", explains
        explains.add(("index", obj))
        return ("done" if ("index", obj) not in T else "decision"), explains
    if kind in ("constraint added", "constraint dropped"):
        tbl, _, name = obj.partition(" ")
        if tbl not in S.ttab:
            return "table not built", explains
        k = ("constraint", f"{tbl}.{name}")
        explains.add(k)
        there = k in T
        if kind == "constraint added" and not there:
            want = row["change"].split(f"ADD CONSTRAINT {name} ", 1)[-1].strip().strip("`")
            there = any(kk[0] == "constraint" and kk[1].startswith(tbl + ".") and same_but_valid(v, want)
                        for kk, v in T.items())
        return (("done" if there else "open") if kind == "constraint added" else ("done" if not there else "open")), \
            explains
    t, _, c = obj.rpartition(".")
    if t not in S.ttab:
        return ("done" if kind in ("column dropped", "column retired") and t not in S.ptab else "table not built"), \
            explains
    k = ("column", obj)
    explains.add(k)
    have = T.get(k)
    if kind in ("column dropped", "column retired"):
        if have is None:
            return "done", explains
        return ("kept" if kind == "column retired" else "open"), explains
    if have is None:
        return "column not built", explains
    if kind == "not null":
        return ("done" if " not null" in have else "open"), explains
    if kind == "column changed":
        parts = [p.strip().strip("`") for p in row["change"].split("->")]
        before = parse_column_text(parts[0]) if len(parts) == 2 else None
        want = parse_column_text(parts[1]) if len(parts) == 2 else None
        if not want:
            return "unjudged", explains
        for side in (before, want):
            if side and side["check"]:
                explains.add(("constraint", f"{t}.{side['check']}"))
        ty, nn, dflt = snapshot_column(have)
        ok = ty == want["type"] and nn == want["notnull"]
        if want["default"] is not None:
            ok = ok and dflt is not None and dflt.strip("()") == want["default"]
        if want["check"]:
            ok = ok and ("constraint", f"{t}.{want['check']}") in T
        return ("done" if ok else "open"), explains
    return "unjudged", explains


REVIEW_KINDS = ("not null", "column changed", "column dropped", "column retired", "constraint added",
                "constraint dropped", "table dropped", "index duplicates a unique index", "statement dropped",
                "file changed")


def names(word, st):
    return bool(word) and re.search(rf"(?<![\w.]){re.escape(word)}(?!\w)", st) is not None


def source_file(stmts, kind, key, d):
    """The last package file whose statement brings the object: it names the object's table and the object (a policy:
    its table and a row-security call or POLICY; a function: its name)."""
    t, lf = table_of(kind, key, d), leaf(kind, key)
    hit = None
    for fname, st in stmts:
        if kind == "function":
            ok = re.search(rf"\b{re.escape(lf)}\s*\(", st) and re.search(r"FUNCTION", st, re.I)
        elif kind == "policy":
            ok = names(t, st) and (names(lf, st) or "rls" in st.lower() or "POLICY" in st.upper())
        elif t:
            ok = names(t, st) and re.search(rf"\b{re.escape(lf)}\b", st)
        else:
            ok = re.search(rf"\b{re.escape(lf)}\b", st)
        if ok:
            hit = fname
    return hit


def dropped_by(stmts, kind, key, d):
    """The forward file whose statement drops a target-only object, if one does."""
    t, lf = table_of(kind, key, d), leaf(kind, key)
    hit = None
    for fname, st in stmts:
        if not is_forward(fname):
            continue
        u = st.upper()
        if kind == "index":
            ok = "DROP INDEX" in u and re.search(rf"\b{re.escape(lf)}\b", st)
        elif kind == "constraint":
            ok = "DROP CONSTRAINT" in u and names(t, st) and re.search(rf"\b{re.escape(lf)}\b", st)
        elif kind == "policy":
            ok = t and ((f"drop_rls_policies('{t}'" in st) or
                        ("DROP POLICY" in u and re.search(rf"\b{re.escape(lf)}\b", st) and names(t, st)))
        elif kind == "function":
            ok = "DROP FUNCTION" in u and re.search(rf"\b{re.escape(lf)}\b", st)
        elif kind == "column":
            ok = "DROP COLUMN" in u and names(t, st) and re.search(rf"\b{re.escape(lf)}\b", st)
        else:
            ok = False
        if ok:
            hit = fname
    return hit


def classify_table(t, tasks, nomig, pms, status):
    """Why the target lacks a table the package has. gap is True only for a started or closed ticket, or no task."""
    if t in nomig:
        return {"why": "no migration creates it", "reason": nomig[t], "gap": False, "bucket": "storage only"}
    task = tasks.get(t)
    if not task:
        return {"why": "no migration task names it", "gap": True, "bucket": "no task"}
    for key in (f"{task}#{t}", task):
        if key in pms:
            wp = str(pms[key])
            st = status.get(wp)
            info = {"task": task, "ticketKey": key, "workPackage": int(wp), "status": st}
            if st is None:
                return {**info, "why": "on the board, status not read", "gap": True, "bucket": "status unknown"}
            if st in NOT_STARTED:
                return {**info, "why": f"on the board and {st}", "gap": False, "bucket": "not started"}
            return {**info, "why": f"its ticket is {st}: a gap", "gap": True, "bucket": "started or closed"}
    return {"task": task, "why": "a later block's task, not on the board yet", "gap": False, "bucket": "later block"}


def diagnose_db(db, P, T, rows, stmts, file_release, tasks, nomig, pms, status):
    S = Sides(P, T)
    rows = [r for r in rows if r["db"] in (db, "both")]
    out = {"tables": {"reference": len(S.ptab), "target": len(S.ttab)},
           "objects": {"reference": len(P), "target": len(T)},
           "matching": 0, "notValidSame": 0, "review": [], "notBuilt": [], "targetOnlyTables": [],
           "behind": [], "drops": [], "handDone": [], "handOpen": [], "moot": [], "waitsForTarget": [],
           "targetOnly": [], "different": []}

    # 1. the hand changes, judged on the target
    explained = {}
    for row in rows:
        st, keys = judge_review(row, S)
        out["review"].append({**row, "status": st})
        if st in ("done", "open", "decision", "kept"):       # only a judged change claims its objects
            for k in keys:
                explained[k] = (st, row)
    done_cols, open_cols = collections.defaultdict(set), collections.defaultdict(set)
    done_unique, retiring, dropped_done = set(), set(), set()
    # A dropped, retired or retyped column carries its keys, indexes and checks with it; a NOT NULL only itself
    # (the column, which `explained` holds).
    for r in out["review"]:
        kind, obj, st = r["kind"], r["object"], r["status"]
        if kind in ("column dropped", "column retired", "column changed") and "." in obj:
            t, c = obj.rsplit(".", 1)
            if st == "done":
                done_cols[t].add(c)
            elif st == "open":
                open_cols[t].add(c)
        elif kind == "constraint added" and st == "done":
            tbl, _, name = obj.partition(" ")
            cols = key_columns(r["change"].split(f"ADD CONSTRAINT {name} ", 1)[-1].strip("` "))
            if cols:
                done_unique.add((tbl, cols))
        elif kind == "table dropped":
            (retiring if st == "open" else dropped_done).add(obj)

    # 2. tables
    missing = S.ptab - S.ttab
    for t in sorted(missing):
        n = sum(1 for k in P if k[0] != "table" and table_of(k[0], k[1], P[k]) == t)
        if t in dropped_done:                    # the package retires it and the target has not got it: done
            out["notBuilt"].append({"table": t, "objects": n, "why": "the package retires it (a done `table dropped`)",
                                    "gap": False, "bucket": "retired"})
            continue
        out["notBuilt"].append({"table": t, "objects": n, **classify_table(t, tasks, nomig, pms, status)})
    for t in sorted(S.ttab - S.ptab):
        n = sum(1 for k in T if k[0] != "table" and table_of(k[0], k[1], T[k]) == t)
        out["targetOnlyTables"].append({"table": t, "objects": n,
                                        "note": "the package retires it" if t in retiring or t in dropped_done
                                        else ""})
    extra = S.ttab - S.ptab

    def rides(kind, key, d, cols_by_table):
        t = table_of(kind, key, d)
        if kind not in ("column", "constraint", "index"):
            return False                         # a policy or trigger that names the column is its own change
        return bool(t and columns_named(kind, key, d, S.cols.get(t, set())) & cols_by_table.get(t, set()))

    def item(kind, key, **kw):
        return {"kind": kind, "name": key, **kw}

    # 3. objects, both ways
    for k in sorted(set(P) | set(T)):
        kind, key = k
        if kind == "table":
            continue
        p, v = P.get(k), T.get(k)
        d = p if p is not None else v
        t = table_of(kind, key, d)
        if t in missing and v is None:
            continue                            # counted with its table
        if t in extra and p is None:
            continue                            # counted with its table
        if p is not None and v is not None:
            if p == v:
                out["matching"] += 1
                continue
            if same_but_valid(p, v):
                out["notValidSame"] += 1
                continue
        side = "different" if (p is not None and v is not None) else ("reference" if v is None else "target")
        rec = item(kind, key, reference=p, target=v)
        if k in explained:
            st, row = explained[k]
            bucket = "handDone" if st == "done" else "handOpen"
            out[bucket].append({**rec, "change": f"{row['kind']}: {row['object']}", "status": st})
            continue
        if rides(kind, key, d, done_cols):
            out["handDone"].append({**rec, "change": "rides on a done column change"})
            continue
        tgt = fk_target(d) if kind == "constraint" else None
        if tgt and (tgt[0], tgt[1]) in done_unique:
            out["handDone"].append({**rec, "change": f"rides on the hand-added unique key of {tgt[0]}"})
            continue
        if rides(kind, key, d, open_cols):
            out["handOpen"].append({**rec, "change": "rides on an open column change"})
            continue
        if side == "target":
            f = dropped_by(stmts, kind, key, d)
            if f:
                out["drops"].append({**rec, "file": f, "release": file_release.get(f, "unreleased")})
            else:
                out["targetOnly"].append({**rec, "note": "on a table the package retires" if t in retiring else ""})
            continue
        if t in retiring:
            out["moot"].append({**rec, "why": "on a table the package retires (an open `table dropped`)"})
            continue
        if side == "reference" and tgt and tgt[0] not in S.ttab:
            out["waitsForTarget"].append({**rec, "why": f"{tgt[0]} is not built on the target"})
            continue
        f = source_file(stmts, kind, key, p)
        if f and is_forward(f):
            out["behind"].append({**rec, "file": f, "release": file_release.get(f, "unreleased"),
                                  "change": "add" if side == "reference" else "change"})
        else:
            out["different"].append({**rec, "file": f})
    return out


def release_of_files(root=ROOT):
    """{file name: the first release tag (r<N>) whose tree has it}, from git; {} where git is not there."""
    try:
        tags = subprocess.run(["git", "-C", str(root), "tag", "--list", "r*"], capture_output=True, text=True,
                              timeout=60).stdout.split()
    except Exception:
        return {}
    tags = sorted((t for t in tags if re.fullmatch(r"r\d+", t)), key=lambda t: int(t[1:]))
    first = {}
    for tag in tags:
        try:
            names = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", tag, "--", "backend/"],
                                   capture_output=True, text=True, timeout=60).stdout.split()
        except Exception:
            continue
        for n in names:
            first.setdefault(n.rsplit("/", 1)[-1], tag)
    return first


def package_state(root=ROOT):
    def git(*a):
        try:
            return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True,
                                  timeout=60).stdout.strip()
        except Exception:
            return ""
    return {"commit": git("rev-parse", "--short=8", "HEAD"), "describe": git("describe", "--tags", "--always")}


def diagnose(ref, tgt, label, tickets=None, ref_meta=None, tgt_meta=None, backend=BACKEND):
    """ref, tgt: {db: snapshot rows}. Returns the JSON document."""
    rows = review_rows(REVIEW.read_text(encoding="utf-8"))
    tasks, nomig = migration_tasks(MIGRATIONS_MD.read_text(encoding="utf-8"))
    pms = {k: v for k, v in json.loads(PMS_MAP.read_text(encoding="utf-8")).items() if isinstance(v, int)}
    status, status_src = load_ticket_status(tickets)
    files = read_backend(backend)
    rel = release_of_files()
    doc = {"tool": "tools/check-schema-drift.py", "change": "CHG-R12LV-001", "label": label,
           "generatedAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "package": package_state(), "tickets": status_src, "reference": ref_meta or {}, "target": tgt_meta or {},
           "latestRelease": max(set(rel.values()), key=lambda t: int(t[1:])) if rel else None,
           "databases": {}}
    for db in DATABASES:
        if db not in ref or db not in tgt:
            continue
        stmts = [(f, st) for f, text in files[db] for st in split_statements(text)]
        doc["databases"][db] = diagnose_db(db, ref[db], tgt[db], rows, stmts, rel, tasks, nomig, pms, status)
    doc["summary"] = summarise(doc)
    return doc


def summarise(doc):
    s = collections.Counter()
    latest = doc.get("latestRelease")
    for db, r in doc["databases"].items():
        s["releaseBehind"] += sum(1 for x in r["behind"] if x["release"] == latest)
        s["releaseDrops"] += sum(1 for x in r["drops"] if x["release"] == latest)
        s["olderBehind"] += sum(1 for x in r["behind"] if x["release"] not in (latest, "unreleased"))
        s["olderDrops"] += sum(1 for x in r["drops"] if x["release"] not in (latest, "unreleased"))
        s["unreleasedBehind"] += sum(1 for x in r["behind"] if x["release"] == "unreleased")
        s["unreleasedDrops"] += sum(1 for x in r["drops"] if x["release"] == "unreleased")
        s["handOpen"] += sum(1 for x in r["review"] if x["status"] == "open")
        s["handDone"] += sum(1 for x in r["review"] if x["status"] == "done")
        s["handDecision"] += sum(1 for x in r["review"] if x["status"] == "decision")
        s["targetOnly"] += len(r["targetOnly"]) + sum(1 + x["objects"] for x in r["targetOnlyTables"])
        s["notBuilt"] += len(r["notBuilt"])
        s["notBuiltGaps"] += sum(1 for x in r["notBuilt"] if x["gap"])
        s["different"] += len(r["different"])
        s["notValidSame"] += r["notValidSame"]
        s["waitsForTarget"] += len(r["waitsForTarget"])
        s["moot"] += len(r["moot"])
        s["collisions"] += len(doc.get("collisions", {}).get(db, []))
    s["findings"] = (s["releaseBehind"] + s["releaseDrops"] + s["olderBehind"] + s["olderDrops"]
                     + s["unreleasedBehind"] + s["unreleasedDrops"] + s["handOpen"]
                     + s["handDecision"] + s["targetOnly"] + s["notBuiltGaps"] + s["different"])
    return dict(s)


# =====================================================================================================================
# The markdown report
# =====================================================================================================================
def md_report(doc):
    L, s, lab = [], doc["summary"], doc["label"]
    latest = doc.get("latestRelease") or "the latest release"
    pk = doc.get("package", {})
    L.append(f"# Schema drift: {lab} against the package ({pk.get('describe') or pk.get('commit')})\n")
    L.append(f"Written by `tools/check-schema-drift.py` ({doc['change']}) at {doc['generatedAt']}. Every object of "
             f"{lab}'s schema-only dumps against the package's intended state: its built SQL plus the hand changes "
             "in handoff/migration-review.md. **Findings are never baselined**: this run judged the dumps from "
             "scratch.\n")
    ref, tgt = doc.get("reference", {}), doc.get("target", {})
    if tgt:
        L.append("- " + lab + ": " + "; ".join(f"{k} {v}" for k, v in sorted(tgt.items())))
    if ref:
        L.append("- reference: " + "; ".join(f"{k} {v}" for k, v in sorted(ref.items()) if k != "adjustments"))
        adj = ref.get("adjustments") or []
        L.append("- adjustments to the package's files for the build: " + (
            "; ".join(f"{a['db']} {a['file']} `{a['object']}` -> `{a['after']}` ({a['decision']})" for a in adj)
            if adj else "none (the package provisions as shipped)"))
    L.append(f"- ticket statuses: {doc.get('tickets')}\n")

    L.append("## Verdict\n")
    L.append(f"- **{s.get('releaseBehind', 0)} + {s.get('releaseDrops', 0)} {latest} objects**: "
             f"{s.get('releaseBehind', 0)} to add or change and {s.get('releaseDrops', 0)} old ones to drop, from "
             f"{latest}'s forward files")
    if s.get("unreleasedBehind") or s.get("unreleasedDrops"):
        L.append(f"- **{s.get('unreleasedBehind', 0)} + {s.get('unreleasedDrops', 0)} objects from forward files no "
                 "release has shipped yet**")
    if s.get("olderBehind") or s.get("olderDrops"):
        L.append(f"- **{s.get('olderBehind', 0)} + {s.get('olderDrops', 0)} objects from older releases' forward "
                 "files** that differ on the target")
    L.append(f"- **{s.get('handOpen', 0)} hand changes open** (migration-review.md); {s.get('handDone', 0)} done"
             + (f", {s['handDecision']} waiting on a decision" if s.get("handDecision") else ""))
    L.append(f"- **{s.get('targetOnly', 0)} objects on {lab} that the package never recorded**")
    L.append(f"- **{s.get('notBuiltGaps', 0)} missing tables that are a gap** ({s.get('notBuilt', 0)} not built in "
             "all; a gap is a table whose ticket is started or closed, or that no task names)")
    L.append(f"- **{s.get('different', 0)} objects defined differently** outside any forward file, for a person")
    L.append(f"- not gaps: {s.get('notValidSame', 0)} keys the target validated that the package creates NOT VALID; "
             f"{s.get('waitsForTarget', 0)} keys waiting for their target table; {s.get('moot', 0)} objects on a "
             "table the package retires")
    if s.get("collisions"):
        L.append(f"- **{s['collisions']} snapshot keys seen twice**: the snapshot query is cutting names")
    L.append("")
    L.append("| | " + " | ".join(f"reference {db} | {lab} {db}" for db in doc["databases"]) + " |")
    L.append("|---|" + "---:|---:|" * len(doc["databases"]))
    L.append("| Tables | " + " | ".join(f"{r['tables']['reference']:,} | {r['tables']['target']:,}"
                                         for r in doc["databases"].values()) + " |")
    L.append("| All objects | " + " | ".join(f"{r['objects']['reference']:,} | {r['objects']['target']:,}"
                                              for r in doc["databases"].values()) + " |")
    L.append("")

    for db, r in doc["databases"].items():
        L.append(f"## {db}\n")
        by_rel = collections.defaultdict(list)
        for x in r["behind"]:
            by_rel[x["release"]].append(x)
        drops = collections.defaultdict(list)
        for x in r["drops"]:
            drops[x["release"]].append(x)
        for rel in sorted(set(by_rel) | set(drops), key=lambda t: -int(t[1:]) if t[1:].isdigit() else -10 ** 6):
            L.append(f"### From {rel}'s forward files: {len(by_rel[rel])} to add or change, {len(drops[rel])} to drop\n")
            mods = collections.Counter(x["name"].split(".")[0] for x in by_rel[rel])
            if mods:
                L.append("| Schema | Objects |\n|---|---:|")
                for m, n in mods.most_common():
                    L.append(f"| {m} | {n} |")
                L.append("")
            for x in by_rel[rel]:
                L.append(f"- {x['change']} {x['kind']} `{x['name']}` ({x['file']})")
            for x in drops[rel]:
                L.append(f"- drop {x['kind']} `{x['name']}` ({x['file']})")
            L.append("")
        opn = [x for x in r["review"] if x["status"] in ("open", "decision")]
        nd = sum(1 for x in opn if x["status"] == "decision")
        L.append(f"### Hand changes open: {len(opn) - nd}" + (f", and {nd} waiting on a decision" if nd else "")
                 + "\n")
        for kind in REVIEW_KINDS:
            names = [x["object"] for x in opn if x["kind"] == kind]
            if names:
                L.append(f"- {kind}: " + ", ".join(f"`{n}`" for n in names))
        ride = [x for x in r["handOpen"]]
        if ride:
            L.append(f"- differences on the target that belong to these open changes: "
                     + ", ".join(f"{x['kind']} `{x['name']}`" for x in ride))
        st = collections.Counter(x["status"] for x in r["review"])
        L.append(f"- all rows: " + ", ".join(f"{k} {v}" for k, v in sorted(st.items())))
        L.append("")
        L.append(f"### On {lab}, not in the package: {len(r['targetOnly']) + len(r['targetOnlyTables'])}\n")
        for x in r["targetOnlyTables"]:
            L.append(f"- table `{x['table']}` with its {x['objects']} objects" + (f" ({x['note']})" if x["note"] else ""))
        for x in r["targetOnly"]:
            L.append(f"- {x['kind']} `{x['name']}`: {(x['target'] or '')[:160]}" + (f" ({x['note']})" if x["note"] else ""))
        L.append("")
        L.append(f"### Tables the package has and {lab} has not built: {len(r['notBuilt'])}\n")
        b = collections.Counter(x["bucket"] for x in r["notBuilt"])
        L.append("| Why | Tables |\n|---|---:|")
        for k in ("later block", "not started", "storage only", "retired", "started or closed", "no task",
                  "status unknown"):
            L.append(f"| {k} | {b.get(k, 0)} |")
        L.append("")
        for x in r["notBuilt"]:
            if x["gap"]:
                L.append(f"- **gap** `{x['table']}`: {x['why']}" + (f" (#{x['workPackage']})" if x.get("workPackage")
                                                                    else ""))
        if r["different"]:
            L.append(f"\n### Defined differently, outside any forward file: {len(r['different'])}\n")
            for x in r["different"]:
                L.append(f"- {x['kind']} `{x['name']}` ({x.get('file') or 'no package file named'})\n"
                         f"  - package: {(x['reference'] or '')[:300]}\n  - {lab}: {(x['target'] or '')[:300]}")
        L.append(f"\n### Not gaps\n")
        L.append(f"- {r['notValidSame']} keys {lab} validated that the package creates NOT VALID (the same key)")
        L.append(f"- {len(r['handDone'])} differences that are hand changes {lab} has made (the package's build "
                 "cannot show them)")
        for x in r["waitsForTarget"]:
            L.append(f"- waits for its target table: {x['kind']} `{x['name']}` ({x['why']})")
        for x in r["moot"]:
            L.append(f"- moot: {x['kind']} `{x['name']}` ({x['why']})")
        L.append("")
    return "\n".join(L) + "\n"


# =====================================================================================================================
# Docker: one throwaway container per run
# =====================================================================================================================
class Pg:
    def __init__(self, name, major, log):
        self.name, self.major, self.log = name, major, log

    def sh(self, args, input=None, check=True, env=None):
        cmd = ["docker", "exec", "-i", "-e", "PGCLIENTENCODING=UTF8", "-e", "PGHOST=/var/run/postgresql",
               "-e", f"PGUSER={PGUSER}"]
        for k, v in (env or {}).items():
            cmd += ["-e", f"{k}={v}"]
        p = subprocess.run(cmd + [self.name] + args, input=input.encode("utf-8") if input is not None else None,
                           capture_output=True)
        out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
        if check and p.returncode != 0:
            raise RuntimeError(f"{' '.join(args)[:200]}: exit {p.returncode}: {err.strip()[:2000]}")
        return p.returncode, out, err

    def start(self):
        subprocess.run(["docker", "rm", "-f", self.name], capture_output=True)
        image = IMAGE.format(major=self.major)
        p = subprocess.run(["docker", "run", "-d", "--name", self.name, "-e", f"POSTGRES_USER={PGUSER}",
                            "-e", "POSTGRES_PASSWORD=drift", "-e", "POSTGRES_DB=postgres", image],
                           capture_output=True, text=True)
        if p.returncode:
            raise RuntimeError(f"docker run {image}: {p.stderr.strip()}")
        for _ in range(120):
            logs = subprocess.run(["docker", "logs", self.name], capture_output=True, text=True)
            if "init process complete" in (logs.stdout + logs.stderr):
                rc, _o, _e = self.sh(["pg_isready", "-q"], check=False)
                if rc == 0:
                    rc, o, _e = self.sh(["psql", "-XAtc", "SHOW server_version", "-d", "postgres"], check=False)
                    if rc == 0:
                        self.version = o.strip()
                        self.log(f"container {self.name}: {image}, server {self.version}")
                        return
            time.sleep(1)
        raise RuntimeError(f"{self.name}: the server did not come up")

    def cp(self, src, dst):
        subprocess.run(["docker", "exec", self.name, "mkdir", "-p", dst.rsplit("/", 1)[0]], check=True,
                       capture_output=True)
        p = subprocess.run(["docker", "cp", str(src), f"{self.name}:{dst}"], capture_output=True, text=True)
        if p.returncode:
            raise RuntimeError(f"docker cp {src}: {p.stderr.strip()}")

    def stop(self):
        subprocess.run(["docker", "rm", "-f", self.name], capture_output=True)


def build_reference(pg, log, workdir):
    """Stage backend/, apply the adjustments, then provision as a cell does: control's files in initdb's order,
    then provision-tenant.sh. Returns {db: snapshot text}, metadata."""
    staged = Path(workdir) / "backend"
    if staged.exists():
        shutil.rmtree(staged)
    adjustments = stage_backend(staged)
    for a in adjustments:
        log(f"adjustment ({a['decision']}): {a['db']} {a['file']} {a['object']}: {a['before']} -> {a['after']}")
    pg.cp(staged, "/work/backend")
    pg.sh(["createdb", REF_DB["control"]])
    for f in provision_order(p.name for p in (staged / "control").glob("*.sql")):
        rc, _o, err = pg.sh(["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-d", REF_DB["control"], "-f",
                             f"/work/backend/control/{f}"], check=False)
        log(f"{'ok  ' if rc == 0 else 'FAIL'} control {f}" + ("" if rc == 0 else f": {err.strip()[:600]}"))
        if rc:
            raise RuntimeError(f"the package's control file {f} does not apply: {err.strip()[:600]}")
    rc, out, err = pg.sh(["bash", "/work/backend/provision-tenant.sh", REF_DB["tenant"]], check=False,
                         env={"CONTROL_DB": REF_DB["control"]})
    log(f"{'ok  ' if rc == 0 else 'FAIL'} provision-tenant.sh {REF_DB['tenant']}: {(out + err).strip()[:600]}")
    if rc:
        raise RuntimeError(f"provision-tenant.sh does not provision a tenant from the package: {err.strip()[:600]}")
    snaps = {db: snapshot_db(pg, REF_DB[db]) for db in DATABASES}
    meta = {"server": pg.version, "built": "control in initdb order, tenant by backend/provision-tenant.sh",
            "package": package_state().get("describe", ""), "adjustments": adjustments}
    return snaps, meta


def snapshot_db(pg, dbname):
    _rc, out, _err = pg.sh(["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-d", dbname, "-f", "-"], input=SNAPSHOT_SQL)
    return out


def dump_major(path):
    """The source server's major version from a dump's header (plain or custom format)."""
    head = Path(path).open("rb").read(4096)
    m = re.search(rb"Dumped from database version (\d+)", head)
    if m:
        return int(m.group(1))
    if head.startswith(b"PGDMP"):
        m = re.search(rb"(\d{2})\.\d+ \(", head)
        if m:
            return int(m.group(1))
    return None


def restore_dump(pg, path, dbname, log, workdir):
    """Restore a schema-only dump into a fresh database; a role the dump names that the container lacks is created
    (NOLOGIN) and the restore run again, so every remaining error is a real one and stops the run."""
    src = Path(path)
    custom = src.open("rb").read(5) == b"PGDMP"
    staged = Path(workdir) / f"{dbname}.dump"
    if custom:
        shutil.copyfile(src, staged)
    else:
        # \restrict / \unrestrict guard a replay into a live server; a throwaway container needs neither, and a
        # psql older than 17.6 does not know them.
        text = src.read_bytes().decode("utf-8")
        text = "\n".join(l for l in text.split("\n") if not re.match(r"\\(un)?restrict\b", l))
        staged.write_bytes(text.encode("utf-8"))
    pg.cp(staged, f"/work/dumps/{dbname}.dump")
    for attempt in range(1, 6):
        pg.sh(["dropdb", "--if-exists", dbname])
        pg.sh(["createdb", dbname])
        if custom:
            args = ["pg_restore", "--no-owner", "--no-privileges", "--exit-on-error", "-d", dbname,
                    f"/work/dumps/{dbname}.dump"]
        else:
            args = ["psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-d", dbname, "-f", f"/work/dumps/{dbname}.dump"]
        rc, _o, err = pg.sh(args, check=False)
        if rc == 0:
            log(f"ok   restored {src.name} into {dbname}" + (f" (attempt {attempt})" if attempt > 1 else ""))
            return
        roles = set(re.findall(r'role "([^"]+)" does not exist', err))
        if not roles:
            raise RuntimeError(f"{src.name} does not restore: {err.strip()[:1500]}")
        for r in sorted(roles):
            log(f"     {src.name} names role {r}; created NOLOGIN for the restore")
            pg.sh(["psql", "-X", "-q", "-d", "postgres", "-c", f'CREATE ROLE "{r}" NOLOGIN'])
    raise RuntimeError(f"{src.name} does not restore after creating its roles")


# =====================================================================================================================
# The self-test: small fixture snapshots, one per bucket and lesson; no Docker, no package files
# =====================================================================================================================
def self_test():
    fails = []

    def expect(cond, what):
        if not cond:
            fails.append(what)

    # The snapshot query: every name concatenation is cast to text; function bodies by md5; same SQL both sides.
    for col in NAME_COLUMNS:
        expect(not re.search(rf"\b{col}\s*\|\|", SNAPSHOT_SQL), f"snapshot: `{col} ||` is a name concatenation")
        expect(not re.search(rf"\|\|\s*[a-z]\.{col}\b(?!::text)", SNAPSHOT_SQL),
               f"snapshot: `|| x.{col}` without ::text cuts keys at 63 characters")
    expect("md5(pg_get_functiondef(p.oid))" in SNAPSHOT_SQL, "snapshot: function bodies are compared by md5")
    long_key = "promotions.promotion_channel_publication.promotion_channel_publication_venue_id_promotion_id_fkey"
    rows, coll = parse_snapshot([f"constraint\t{long_key}\tFOREIGN KEY (venue_id) REFERENCES x(id)",
                                 f"constraint\t{long_key[:63]}\tA", f"constraint\t{long_key[:63]}\tB"])
    expect(coll == [f"constraint {long_key[:63]}"] and len(rows) == 3, "parse_snapshot: a repeated key is reported")

    # Provisioning order: the shell glob's bytewise order.
    expect(provision_order(["V0103a__x.sql", "V0103__y.sql", "900-fk.sql", "010-a.sql", "notes.md"]) ==
           ["010-a.sql", "900-fk.sql", "V0103__y.sql", "V0103a__x.sql"], "provision_order: not the glob order")

    # The CHG-R6-001 adjustment: applied to an undefined type with a decided row; off once the type exists or the
    # column is text; an undecided undefined type stops the build.
    pii = ("CREATE TABLE IF NOT EXISTS pii.subject (\n    id uuid PRIMARY KEY NOT NULL,\n"
           "    kind                              pii.subject_kind NOT NULL,\n    display_name text\n);\n")
    row = {"kind": "column changed", "db": "tenant", "object": "pii.subject.kind",
           "change": "`kind pii.subject_kind NOT NULL` -> `kind text NOT NULL CONSTRAINT subject_kind_chk CHECK "
                     "(kind IN ('guest', 'employee'))`", "todo": ""}
    adj = undefined_type_adjustments([("010-pii.sql", pii)], [row])
    expect(len(adj) == 1 and adj[0][2].strip().startswith("kind text NOT NULL CONSTRAINT subject_kind_chk")
           and adj[0][2].endswith(","), f"adjustment: not applied as decided: {adj}")
    expect(undefined_type_adjustments([("000-types.sql", "CREATE TYPE pii.subject_kind AS ENUM ('guest');"),
                                       ("010-pii.sql", pii)], [row]) == [], "adjustment: on although the type exists")
    expect(undefined_type_adjustments([("provision-tenant.sh", "psql <<'SQL'\nCREATE DOMAIN pii.subject_kind AS text;\nSQL\n"),
                                       ("010-pii.sql", pii)], []) == [],
           "adjustment: on although provision-tenant.sh creates the type")
    expect(undefined_type_adjustments([("010-pii.sql", pii.replace("pii.subject_kind", "text"))], [row]) == [],
           "adjustment: on although the column is text")
    try:
        undefined_type_adjustments([("010-pii.sql", pii)], [])
        fails.append("adjustment: an undecided undefined type did not stop the build")
    except ValueError:
        pass

    # Review rows, judged.
    rv = review_rows("| Kind | Database | Object | Change | What |\n|---|---|---|---|---|\n"
                     "| not null | tenant | `a.t.c` | x | y |\n")
    expect(rv == [{"kind": "not null", "db": "tenant", "object": "a.t.c", "change": "x", "todo": "y"}],
           "review_rows: the table does not parse")
    expect(parse_column_text("status text NOT NULL DEFAULT 'queued' CONSTRAINT s_chk CHECK (status IN ('a'))") ==
           {"name": "status", "type": "text", "notnull": True, "default": "'queued'", "check": "s_chk"},
           "parse_column_text")
    expect(snapshot_column("numeric(18,4) not null default 'x'::text") == ("numeric(18,4)", True, "'x'"),
           "snapshot_column")
    expect(norm_type("timestamptz") == "timestamp with time zone" and norm_type("numeric(18, 4)") == "numeric(18,4)",
           "norm_type")

    # One fixture pair covering every bucket.
    P = {
        ("table", "m.keep"): "", ("column", "m.keep.id"): "uuid not null",
        ("column", "m.keep.code"): "text",                                  # same both sides
        ("constraint", "m.keep.keep_parent_fkey"): "FOREIGN KEY (parent_id) REFERENCES m.parent(id) NOT VALID",
        ("column", "m.keep.parent_id"): "uuid",
        ("column", "m.keep.old_id"): "uuid",                                # dropped by a done hand change
        ("constraint", "m.keep.keep_old_id_fkey"): "FOREIGN KEY (old_id) REFERENCES m.parent(id)",
        ("index", "m.keep_old_id_idx"): "CREATE INDEX ON m.keep USING btree (old_id)",
        ("column", "m.keep.device_id"): "text not null",                    # retyped by a done hand change
        ("constraint", "m.keep.keep_device_id_chk"): "CHECK ((char_length(device_id) <= 200))",
        ("column", "m.keep.note"): "text not null",                         # open hand change (column dropped)
        ("column", "m.keep.version"): "integer",                            # open not null
        ("column", "m.keep.prefix"): "text",                                # from the latest release's file
        ("policy", "m.keep.keep_read"): "r platform.in_scope(scope_path) | ",
        ("constraint", "m.keep.keep_rate_fkey"): "FOREIGN KEY (rate_id) REFERENCES m.rate(id) NOT VALID",
        ("column", "m.keep.rate_id"): "uuid",
        ("column", "m.keep.legacy"): "text",                                # baseline object the target lacks
        ("table", "m.parent"): "", ("column", "m.parent.id"): "uuid not null",
        ("column", "m.parent.venue_id"): "uuid",
        ("table", "m.child"): "", ("column", "m.child.venue_id"): "uuid", ("column", "m.child.parent_id"): "uuid",
        ("table", "m.retire"): "", ("column", "m.retire.flag_new"): "boolean",
        ("table", "m.later"): "", ("column", "m.later.id"): "uuid",
        ("table", "m.newt"): "", ("table", "m.storage"): "", ("table", "m.started"): "", ("table", "m.closed"): "",
        ("table", "m.orphan"): "",
        ("function", "platform.f(x int)"): "abc",
    }
    T = {k: v for k, v in P.items() if k[1].split(".")[1] not in ("later", "newt", "storage", "started", "closed",
                                                                   "orphan")}
    for k in [("column", "m.keep.old_id"), ("constraint", "m.keep.keep_old_id_fkey"), ("index", "m.keep_old_id_idx"),
              ("constraint", "m.keep.keep_device_id_chk"), ("column", "m.keep.prefix"),
              ("constraint", "m.keep.keep_rate_fkey"), ("column", "m.keep.legacy"),
              ("column", "m.retire.flag_new")]:
        T.pop(k)
    T.update({
        ("constraint", "m.keep.keep_parent_fkey"): "FOREIGN KEY (parent_id) REFERENCES m.parent(id)",   # validated
        ("column", "m.keep.device_id"): "uuid not null",
        ("constraint", "m.keep.keep_device_id_fkey"): "FOREIGN KEY (device_id) REFERENCES m.parent(id)",
        ("column", "m.keep.note"): "text",                                  # nullable: the four-step drop started
        ("policy", "m.keep.keep_scope"): "* platform.tenant_root_in_scope() | platform.tenant_root_in_scope()",
        ("constraint", "m.parent.parent_venue_id_id_uniq"): "UNIQUE (venue_id, id)",
        ("constraint", "m.child.child_venue_id_parent_id_fkey"):
            "FOREIGN KEY (venue_id, parent_id) REFERENCES m.parent(venue_id, id)",
        ("function", "platform.extra()"): "def",
        ("column", "m.retire.flag_old"): "boolean",
        ("function", "platform.f(x int)"): "abd",                           # body differs: md5 differs
    })
    rows = [
        {"kind": "column dropped", "db": "tenant", "object": "m.keep.old_id", "change": "", "todo": ""},
        {"kind": "column changed", "db": "tenant", "object": "m.keep.device_id",
         "change": "`device_id text NOT NULL CONSTRAINT keep_device_id_chk CHECK (char_length(device_id) <= 200)` -> "
                   "`device_id uuid NOT NULL`", "todo": ""},
        {"kind": "column dropped", "db": "tenant", "object": "m.keep.note", "change": "", "todo": ""},
        {"kind": "not null", "db": "tenant", "object": "m.keep.version", "change": "", "todo": ""},
        {"kind": "constraint added", "db": "tenant", "object": "m.parent parent_venue_id_id_uniq",
         "change": "`ALTER TABLE m.parent ADD CONSTRAINT parent_venue_id_id_uniq UNIQUE (venue_id, id)`", "todo": ""},
        {"kind": "table dropped", "db": "tenant", "object": "m.retire", "change": "", "todo": ""},
        {"kind": "not null", "db": "tenant", "object": "m.later.id", "change": "", "todo": ""},
        {"kind": "file changed", "db": "both", "object": "990-x.sql", "change": "", "todo": ""},
    ]
    stmts = [("010-m.sql", "CREATE TABLE m.keep (legacy text, code text)"),
             ("010-m.sql", "CREATE FUNCTION platform.f(x int) RETURNS int"),
             ("V0110__a.sql", "SELECT platform.apply_tenant_rls('m.keep'::regclass)"),
             ("V0118__b.sql", "ALTER TABLE m.keep ADD COLUMN IF NOT EXISTS prefix text"),
             ("V0118__b.sql", "PERFORM platform.drop_rls_policies('m.keep'::regclass); "
                              "PERFORM platform.apply_split_rls('m.keep'::regclass, 'x')")]
    rel = {"010-m.sql": "r1", "V0110__a.sql": "r9", "V0118__b.sql": "r11"}
    tasks = {"m.later": "MIG-M-9", "m.newt": "MIG-M", "m.started": "MIG-M-2", "m.closed": "MIG-M-3"}
    pms = {"MIG-M#m.newt": 1, "MIG-M-2": 2, "MIG-M-3": 3}
    status = {"1": "New", "2": "In progress", "3": "Closed"}
    r = diagnose_db("tenant", P, T, rows, stmts, rel, tasks, {"m.storage": "storage only"}, pms, status)
    names = lambda b: sorted(x["name"] for x in r[b])
    st = {x["object"]: x["status"] for x in r["review"]}
    expect(st == {"m.keep.old_id": "done", "m.keep.device_id": "done", "m.keep.note": "open", "m.keep.version": "open",
                  "m.parent parent_venue_id_id_uniq": "done", "m.retire": "open", "m.later.id": "table not built",
                  "990-x.sql": "for a person"}, f"review judged: {st}")
    expect(r["notValidSame"] == 1, f"NOT VALID on one side is the same key: {r['notValidSame']}")
    expect(names("handDone") == sorted(["m.keep.old_id", "m.keep.keep_old_id_fkey", "m.keep_old_id_idx",
                                        "m.keep.device_id", "m.keep.keep_device_id_chk", "m.keep.keep_device_id_fkey",
        "m.parent.parent_venue_id_id_uniq", "m.child.child_venue_id_parent_id_fkey"]),
        f"hand changes done (dropped column's key and index, retyped column's key, venue keys): {names('handDone')}")
    expect(names("handOpen") == ["m.keep.note"], f"open hand change: {names('handOpen')}")
    expect([(x["name"], x["release"]) for x in r["behind"]] == [("m.keep.prefix", "r11")],
           f"behind from the latest release: {r['behind']}")
    expect([(x["name"], x["release"]) for x in r["drops"]] == [("m.keep.keep_scope", "r11")],
           f"dropped by a forward file: {r['drops']}")
    expect(names("waitsForTarget") == ["m.keep.keep_rate_fkey"], f"waits for its target: {names('waitsForTarget')}")
    expect(names("moot") == ["m.retire.flag_new"], f"moot on a retiring table: {names('moot')}")
    expect(names("targetOnly") == ["m.retire.flag_old", "platform.extra()"], f"target only: {names('targetOnly')}")
    expect(names("different") == ["m.keep.legacy", "platform.f(x int)"], f"defined differently: {names('different')}")
    nb = {x["table"]: x["bucket"] for x in r["notBuilt"]}
    expect(nb == {"m.later": "later block", "m.newt": "not started", "m.storage": "storage only",
                  "m.started": "started or closed", "m.closed": "started or closed", "m.orphan": "no task"},
           f"tables not built, by ticket: {nb}")
    expect({x["table"] for x in r["notBuilt"] if x["gap"]} == {"m.started", "m.closed", "m.orphan"},
           "only a started or closed ticket (or no task) is a gap")
    doc = {"label": "fixture", "change": "CHG-R12LV-001", "generatedAt": "now", "latestRelease": "r11",
           "databases": {"tenant": r}}
    doc["summary"] = summarise(doc)
    expect(doc["summary"]["releaseBehind"] == 1 and doc["summary"]["releaseDrops"] == 1
           and doc["summary"]["handOpen"] == 3 and doc["summary"]["notBuiltGaps"] == 3, f"summary: {doc['summary']}")
    expect("# Schema drift" in md_report(doc), "md_report")
    return fails


def check_package():
    """The package inputs this tool reads still parse, and every review kind has a rule (run-checks' bare run)."""
    fails = []
    rows = review_rows(REVIEW.read_text(encoding="utf-8")) if REVIEW.exists() else []
    if not rows:
        fails.append(f"{REVIEW.relative_to(ROOT)}: no review rows parsed")
    unknown = sorted({r["kind"] for r in rows} - set(REVIEW_KINDS))
    if unknown:
        fails.append(f"handoff/migration-review.md: kinds with no judging rule here: {', '.join(unknown)}")
    tasks, nomig = migration_tasks(MIGRATIONS_MD.read_text(encoding="utf-8")) if MIGRATIONS_MD.exists() else ({}, {})
    if not tasks or not nomig:
        fails.append("handoff/service-docs/backend/MIGRATIONS.md: the table -> task sections did not parse")
    files = read_backend()
    adj = []
    for db in DATABASES:
        if not files[db]:
            fails.append(f"backend/{db}: no SQL files")
        try:
            adj += [a[3] for a in undefined_type_adjustments(provisioned_first(db) + files[db],
                                                             [r for r in rows if r["db"] in (db, "both")])]
        except ValueError as e:
            fails.append(f"backend/{db}: {e}")
    return fails, len(rows), len(tasks), adj


# =====================================================================================================================
# The commands
# =====================================================================================================================
def _logger(path):
    fh = open(path, "a", encoding="utf-8")

    def log(msg):
        line = f"{datetime.datetime.now().strftime('%H:%M:%S')} {msg}"
        print(line, flush=True)
        fh.write(line + "\n")
        fh.flush()
    return log


def _major(args, dumps):
    majors = {m for m in (dump_major(d) for d in dumps if d) if m}
    if args.pg_major:
        return args.pg_major
    if len(majors) != 1:
        raise SystemExit(f"check-schema-drift: the dumps' Postgres major is {sorted(majors) or 'unknown'}: "
                         "give --pg-major")
    return majors.pop()


def write_outputs(doc, out, label):
    out = Path(out)
    (out / f"drift-{label}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / f"drift-{label}.md").write_text(md_report(doc), encoding="utf-8")
    s = doc["summary"]
    latest = doc.get("latestRelease")
    print(f"check-schema-drift: {label}: {s.get('releaseBehind', 0)} + {s.get('releaseDrops', 0)} {latest} objects, "
          f"{s.get('olderBehind', 0)} + {s.get('olderDrops', 0)} older, {s.get('handOpen', 0)} hand changes open "
          f"({s.get('handDone', 0)} done), {s.get('targetOnly', 0)} only on {label}, {s.get('notBuilt', 0)} tables "
          f"not built ({s.get('notBuiltGaps', 0)} gaps), {s.get('different', 0)} defined differently, "
          f"{s.get('notValidSame', 0)} NOT VALID only -> {out / f'drift-{label}.md'}")


def cmd_run(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = _logger(out / "build.log")
    dumps = {"tenant": a.tenant_dump, "control": a.control_dump}
    dumps = {k: v for k, v in dumps.items() if v}
    if not dumps:
        raise SystemExit("check-schema-drift run: give --tenant-dump and/or --control-dump")
    major = _major(a, dumps.values())
    pg = Pg(f"{a.prefix}pg", major, log)
    work = Path(tempfile.mkdtemp(prefix="schema-drift-"))
    try:
        pg.start()
        if a.reference:
            ref = {db: read_snapshot(Path(a.reference) / f"reference-{db}.tsv")[0] for db in dumps}
            ref_meta = read_snapshot(Path(a.reference) / f"reference-{next(iter(dumps))}.tsv")[2]
            here = package_state().get("describe", "")
            if ref_meta.get("package") != here:
                raise RuntimeError(f"the reference in {a.reference} was built from {ref_meta.get('package')}, the "
                                   f"package is at {here}: build it again (leave out --reference)")
        else:
            snaps, ref_meta = build_reference(pg, log, work)
            for db, text in snaps.items():
                write_snapshot(out / f"reference-{db}.tsv", text, {"side": f"reference {db}", "server": pg.version,
                                                                   "package": ref_meta["package"]})
            ref = {db: parse_snapshot(snaps[db].splitlines())[0] for db in dumps}
        tgt, coll = {}, {}
        for db, path in dumps.items():
            name = f"tgt_{db}"
            restore_dump(pg, path, name, log, work)
            text = snapshot_db(pg, name)
            write_snapshot(out / f"{a.label}-{db}.tsv", text, {"side": f"{a.label} {db}", "dump": Path(path).name,
                                                               "server": pg.version})
            tgt[db], coll[db] = parse_snapshot(text.splitlines())
        tmeta = {"dumps": ", ".join(f"{db} {Path(p).name}" for db, p in dumps.items()),
                 "dumped from": f"Postgres {major}"}
        doc = diagnose(ref, tgt, a.label, a.tickets, ref_meta=ref_meta, tgt_meta=tmeta)
        doc["collisions"] = coll
        doc["summary"] = summarise(doc)
        write_outputs(doc, out, a.label)
    finally:
        if not a.keep:
            pg.stop()
        shutil.rmtree(work, ignore_errors=True)
    return 0


def cmd_reference(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = _logger(out / "build.log")
    pg = Pg(f"{a.prefix}pg", a.pg_major or 17, log)
    work = Path(tempfile.mkdtemp(prefix="schema-drift-"))
    try:
        pg.start()
        snaps, meta = build_reference(pg, log, work)
        for db, text in snaps.items():
            write_snapshot(out / f"reference-{db}.tsv", text, {"side": f"reference {db}", "server": pg.version,
                                                               "package": meta["package"]})
        (out / "reference.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    finally:
        if not a.keep:
            pg.stop()
        shutil.rmtree(work, ignore_errors=True)
    return 0


def cmd_snapshot(a):
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    log = _logger(out.parent / "build.log")
    pg = Pg(f"{a.prefix}pg", _major(a, [a.dump]), log)
    work = Path(tempfile.mkdtemp(prefix="schema-drift-"))
    try:
        pg.start()
        restore_dump(pg, a.dump, "tgt", log, work)
        write_snapshot(out, snapshot_db(pg, "tgt"), {"side": Path(a.dump).name, "server": pg.version})
    finally:
        if not a.keep:
            pg.stop()
        shutil.rmtree(work, ignore_errors=True)
    return 0


def cmd_diagnose(a):
    ref, tgt, coll, rmeta = {}, {}, {}, {}
    for db, path in (("tenant", a.target_tenant), ("control", a.target_control)):
        if not path:
            continue
        rows, c, _m = read_snapshot(path)
        tgt[db], coll[db] = rows, c
        ref[db], _c, rmeta = read_snapshot(Path(a.reference) / f"reference-{db}.tsv")
    refjson = Path(a.reference) / "reference.json"
    if refjson.exists():
        rmeta = {**rmeta, **json.loads(refjson.read_text(encoding="utf-8"))}
    doc = diagnose(ref, tgt, a.label, a.tickets, ref_meta=rmeta,
                   tgt_meta={"snapshots": ", ".join(str(p) for p in (a.target_tenant, a.target_control) if p)})
    doc["collisions"] = coll
    doc["summary"] = summarise(doc)
    Path(a.out).mkdir(parents=True, exist_ok=True)
    write_outputs(doc, a.out, a.label)
    return 0


def cmd_report(a):
    doc = json.loads(Path(a.json).read_text(encoding="utf-8"))
    p = Path(a.json).with_suffix(".md")
    p.write_text(md_report(doc), encoding="utf-8")
    print(f"check-schema-drift: wrote {p}")
    return 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true", help="the self-test alone")
    sub = ap.add_subparsers(dest="cmd")

    def docker_opts(p):
        p.add_argument("--prefix", default="ticvai-drift-", help="container name prefix (default ticvai-drift-)")
        p.add_argument("--pg-major", type=int, help="Postgres major, when the dump's header does not say")
        p.add_argument("--keep", action="store_true", help="leave the container running")

    p = sub.add_parser("run", help="reference + restore + snapshot + diagnose + report, one container")
    p.add_argument("--label", required=True, help="the target's name in the report: live, db, ...")
    p.add_argument("--tenant-dump")
    p.add_argument("--control-dump")
    p.add_argument("--out", required=True)
    p.add_argument("--tickets", help="ticket statuses (default handoff/service-docs/adam-links.json)")
    p.add_argument("--reference", help="reuse reference-<db>.tsv from an earlier run's folder")
    docker_opts(p)
    p = sub.add_parser("reference", help="build the package reference and snapshot it")
    p.add_argument("--out", required=True)
    docker_opts(p)
    p = sub.add_parser("snapshot", help="restore a schema-only dump and snapshot it")
    p.add_argument("--dump", required=True)
    p.add_argument("--out", required=True)
    docker_opts(p)
    p = sub.add_parser("diagnose", help="the JSON and markdown from snapshots (no Docker)")
    p.add_argument("--reference", required=True, help="folder holding reference-tenant.tsv / reference-control.tsv")
    p.add_argument("--target-tenant")
    p.add_argument("--target-control")
    p.add_argument("--label", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--tickets")
    p = sub.add_parser("report", help="the markdown again from a drift JSON")
    p.add_argument("--json", required=True)
    a = ap.parse_args()

    fails = self_test()
    if fails or a.self_test:
        for f in fails:
            print("  SELF-TEST FAIL  " + f)
        print("check-schema-drift: %s - %d self-test(s) failed" % ("FAIL" if fails else "PASS", len(fails)))
        return 1 if fails else 0
    if not a.cmd:
        pf, nrows, ntasks, adj = check_package()
        for f in pf:
            print("  FAIL  " + f)
        print("check-schema-drift: %s - self-test passes; %d review rows, %d tables with a migration task; the build "
              "adjusts %s" % ("FAIL" if pf else "PASS", nrows, ntasks,
                              ", ".join(adj) + " (CHG-R6-001)" if adj else "nothing (the package provisions as "
                                                                          "shipped)"))
        return 1 if pf else 0
    try:
        return {"run": cmd_run, "reference": cmd_reference, "snapshot": cmd_snapshot, "diagnose": cmd_diagnose,
                "report": cmd_report}[a.cmd](a)
    except RuntimeError as e:
        print(f"check-schema-drift: FAIL - {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
