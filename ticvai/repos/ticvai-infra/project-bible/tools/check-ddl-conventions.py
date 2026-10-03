#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The derived DDL, read back against the conventions it was derived to hold.

**Audit class A-DDL-DERIVATION (docs/active/root-classes.md).** `derive-schema.py` and
`derive-ddl.py` produce `backend/*/010-*.sql`, `900-foreign-keys.sql` and `910-indexes.sql`. The
26 September pull audit found what they got wrong and nothing failed on: foreign keys with no index
(R090), `scope_path` typed text (R092) or nullable under forced row-level security (R180), a column
name and type run together (R247), tables that are an id and one key under a comment promising
more (R087), two keys to one parent (R102), column descriptions cut at 220 characters (R019), and
headers and migration lists whose counts disagree with the files (R170, R043, R049, R063).
`check-migrations.py` holds RLS, partitions, FK targets, money and id types; this holds the rest.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-ddl-conventions.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "D-FK-INDEX": "a declared foreign key column with no index leading on it (R090)",
    "D-SCOPE-LTREE": "scope_path not typed ltree (R092)",
    "D-SCOPE-NOTNULL": "scope_path nullable on a table under row-level security (R180)",
    "D-RUN-TOGETHER": "a column line whose name and type run together (R247)",
    "D-STUB-TABLE": "a table holding only keys (R087)",
    "D-DOUBLE-KEY": "a second key to one parent for one concept, or a key named for a renamed table (R102 R160)",
    "D-DESC-CUT": "a column description that is a cut-off prefix of its contract field's (R019)",
    "D-HEADER-COUNT": "a DDL header's table count disagrees with the file (R170 R043)",
    "D-MIG-TABLES": "MIGRATIONS.md, the MIG tickets and the DDL disagree on a migration's tables (R049 R063)",
    "D-MIG-ORDER": "a MIG ticket Follows a migration that MIGRATIONS.md orders after it (R051 R056)",
    "D-NAMING": "a boolean not read as an assertion, or an index/FK name off naming-and-style 6.1 (R093 R119)",
    "D-FK-TARGET-NAME": "a declared key whose column names a different table than it references (R082)",
    "D-JSONB-TWIN": "a jsonb column and a child table holding the same data (R111)",
    "D-RENAME-RESIDUE": "a DDL comment or contract description naming a table by its pre-rename name (R160)",
}
BOOL_OK = re.compile(r"^(is|has|can|requires|allows|allow|should|was|were|did|does|must|needs|include|includes|"
                     r"show|shows|auto|use|uses|supports|accepts|enable|enabled|send|notify|override)_|"
                     r"_(enabled|required|allowed|visible|active|locked|verified|confirmed|approved)$")
# A key may name its target's concept rather than its table (ADR-0056 venue keys, principal actors).
FK_ALIASES = {"venue": "scope", "region": "scope", "department": "scope", "org_unit": "scope",
              "scope": "scope", "parent": "", "principal": "principal", "subject": "subject"}

TYPES = r"(uuid|text|integer|bigint|smallint|numeric|boolean|timestamptz|timestamp|date|time|jsonb|json|" \
        r"ltree|bytea|interval|inet|char|varchar|character|double|real|serial|bigserial|citext|point|" \
        r"tsvector|vector|[a-z_]+\.[a-z_]+)"
CREATE = re.compile(r'CREATE TABLE IF NOT EXISTS ([a-z_]+\.(?:"[a-z_0-9]+"|[a-z_0-9]+))\s*\((.*?)\n\)'
                    r'(?:\s*PARTITION[^;]*)?;', re.S)
FK = re.compile(r"ALTER TABLE ([a-z_]+\.[a-z_0-9]+) ADD CONSTRAINT \S+ FOREIGN KEY \(([^)]+)\) "
                r"REFERENCES ([a-z_]+\.[a-z_0-9]+)\s*\(")
INDEX = re.compile(r"CREATE (?:UNIQUE )?INDEX (?:IF NOT EXISTS )?\S+ ON (?:ONLY )?([a-z_]+\.[a-z_0-9]+)"
                   r"(?: USING \w+)?\s*\(([^)]+)\)")
ACTOR = re.compile(r"(principal|by|actor|user|owner|operator|approver|author|reviewer|agent)")


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-ddl-conventions", RULES)
    backend = g.ROOT / "backend"
    tables = {}          # table -> {col: line}
    pk = {}
    for db in ("tenant", "control"):
        for f in sorted((backend / db).glob("010-*.sql")):
            text = f.read_text(encoding="utf-8")
            found = CREATE.findall(text)
            head = re.search(r"^-- [a-z_]+ — (\d+) tables", text, re.M)
            if head and int(head.group(1)) != len(found):
                guard.add("D-HEADER-COUNT", f.relative_to(g.ROOT).as_posix(),
                          f"{f.relative_to(g.ROOT).as_posix()}: header says {head.group(1)} tables, "
                          f"the file creates {len(found)}")
            for name, body in found:
                name = name.replace('"', "")
                cols = {}
                for raw in body.split("\n"):
                    line = raw.strip().rstrip(",")
                    if not line or line.startswith("--") or re.match(r"(CONSTRAINT|PRIMARY KEY|UNIQUE|"
                                                                     r"CHECK|FOREIGN KEY|EXCLUDE)\b", line):
                        if line.startswith("PRIMARY KEY"):
                            pk[name] = [c.strip() for c in re.findall(r"\(([^)]+)\)", line)[0].split(",")]
                        continue
                    m = re.match(r'"?([a-z_][a-z_0-9]*)"?\s+(\S+)', line)
                    if not m:
                        tok = line.split()[0]
                        guard.add("D-RUN-TOGETHER", f"{name}.{tok}", f"{name}: column line {line[:50]!r} has no type")
                        continue
                    col, typ = m.group(1), m.group(2)
                    if not re.match(TYPES, typ.lower()):
                        guard.add("D-RUN-TOGETHER", f"{name}.{col}", f"{name}: {col!r} has type {typ!r}")
                    cols[col] = line
                    if "PRIMARY KEY" in line:
                        pk.setdefault(name, [col])
                tables[name] = cols

    fks = []
    indexed = {}
    for db in ("tenant", "control"):
        fk_file = backend / db / "900-foreign-keys.sql"
        if fk_file.exists():
            for t, cols, target in FK.findall(fk_file.read_text(encoding="utf-8")):
                fks.append((t, [c.strip() for c in cols.split(",")], target))
        for f in (backend / db).glob("*.sql"):
            for t, cols in INDEX.findall(f.read_text(encoding="utf-8")):
                indexed.setdefault(t, []).append([c.strip().split()[0] for c in cols.split(",")])
    rls = set()
    for db in ("tenant", "control"):
        f = backend / db / "920-row-level-security.sql"
        if f.exists():
            text = f.read_text(encoding="utf-8")
            rls |= set(re.findall(r"ALTER TABLE ([a-z_]+\.[a-z_0-9]+) (?:FORCE|ENABLE) ROW LEVEL SECURITY", text))
            rls |= set(re.findall(r"apply_\w*rls\('([a-z_]+\.[a-z_0-9]+)'", text))

    for t, cols, target in fks:
        lead = cols[0]
        idx = indexed.get(t, []) + ([pk[t]] if t in pk else [])
        cols_line = tables.get(t, {})
        unique_inline = lead in cols_line and "UNIQUE" in cols_line[lead]
        if not any(i and i[0] == lead for i in idx) and not unique_inline:
            guard.add("D-FK-INDEX", f"{t}.{','.join(cols)}", f"{t}({', '.join(cols)}) -> {target} has no index")
    # R102: a second key to the same parent for the same concept. Two keys to one parent are normal
    # when each names a role (debit/credit, from/to, sandbox/production, venue/department of a
    # scope); what the audit found was a key named after the parent itself beside the contract's
    # own key, or a key named after a table the schema history says was renamed (R160).
    renamed = {}
    for r in ((g.load_json(g.ROOT / "handoff" / "schema-history.json", {}) or {}).get("renames") or []):
        old = str(r.get("from") or "").split(".")[-1]
        if old:
            renamed[old + "_id"] = r.get("to")
    by_parent = {}
    for t, cols, target in fks:
        by_parent.setdefault((t, target), []).append(cols[-1])
    for (t, target), cols in sorted(by_parent.items()):
        for c in cols:
            # A wire name kept after a rename is fine alone; beside another key to the same parent it
            # is the same concept stored twice.
            if c in renamed and len(cols) > 1:
                guard.add("D-DOUBLE-KEY", f"{t}.{c}",
                          f"{t}.{c} is named for a table renamed to {renamed[c]} and sits beside "
                          f"{', '.join(x for x in cols if x != c)}, all keys to {target}")
        own = target.split(".")[-1] + "_id"
        if own in cols and target != t:
            others = [c for c in cols if c != own and not ACTOR.search(c)]
            if others and not all(re.search(r"(from|to|source|target|parent|previous|next|original|"
                                            r"replac|merged|primary|secondary|credit|debit|new|old)", c)
                                  for c in others):
                guard.add("D-DOUBLE-KEY", f"{t}->{target}",
                          f"{t}: {own} beside {', '.join(others)}, all keys to {target}")

    for t, cols in sorted(tables.items()):
        if "scope_path" in cols:
            line = cols["scope_path"]
            if not re.match(r"scope_path\s+ltree\b", line):
                guard.add("D-SCOPE-LTREE", t, f"{t}.scope_path is not ltree: {line[:60]!r}")
            if t in rls and "NOT NULL" not in line and "shared" not in line.lower():
                guard.add("D-SCOPE-NOTNULL", t, f"{t}.scope_path is nullable under row-level security")
        names = list(cols)
        if names and len(names) <= 2 and all(c == "id" or c.endswith("_id") for c in names):
            guard.add("D-STUB-TABLE", t, f"{t}: only {', '.join(names)}")

    # R019: a column description that is its contract field's description, cut.
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    by, _ = g.schemas()
    for t, cols in (ref.get("cols") or {}).items():
        for c in cols:
            desc = " ".join(str(c.get("description") or "").split())
            src = str(c.get("source") or "")
            parts = src.split(".")
            if not desc or len(parts) != 3:
                continue
            s = by.get((parts[0], parts[1])) or {}
            full = " ".join(str(((s.get("properties") or {}).get(parts[2]) or {}).get("description") or "").split())
            if full and len(desc) < len(full) and full.startswith(desc) and len(desc) >= 60:
                guard.add("D-DESC-CUT", f"{t}.{c.get('column')}",
                          f"{t}.{c.get('column')}: description stops at {len(desc)} of {len(full)} characters")

    # R049 / R063: MIGRATIONS.md against the DDL and the MIG tickets.
    mig = g.ROOT / "handoff" / "service-docs" / "backend" / "MIGRATIONS.md"
    if mig.exists():
        # **The first-release sections only** (3 October, CHG-TBF-002): the forward migrations after them have their
        # own table, which tools/check-migration-tickets.py reads; its rows share this table's first columns.
        text = mig.read_text(encoding="utf-8").split("\n## Forward migrations", 1)[0]
        # A table created after r1 is in a forward file derive-ddl wrote (backend/<db>/V01nn__after_r1_*.sql), not in
        # 010-<schema>.sql, and a first-release migration can take it from there.
        created = set(tables)
        for db in ("tenant", "control"):
            for f in sorted((backend / db).glob("V*.sql")):
                created |= {n.replace('"', "") for n, _ in CREATE.findall(f.read_text(encoding="utf-8"))}
        listed = {}
        for task, table in re.findall(r"^\| (MIG-[A-Z-]+) \| `([a-z_]+\.[a-z_0-9]+)` \|", text, re.M):
            listed.setdefault(task, set()).add(table)
            if table not in created:
                guard.add("D-MIG-TABLES", f"{task}:{table}", f"MIGRATIONS.md: {task} lists {table}, which no DDL creates")
        seen = {}
        for task, ts in listed.items():
            for t in ts:
                if t in seen:
                    guard.add("D-MIG-TABLES", f"dup:{t}", f"MIGRATIONS.md: {t} is in {seen[t]} and {task}")
                seen[t] = task
        for task, count in re.findall(r"^\| \d+ \| `[^`]+` \| (MIG-[A-Z-]+) \| \w+ \| [^|]+ \| (\d+) \|", text, re.M):
            if int(count) != len(listed.get(task, ())):
                guard.add("D-MIG-TABLES", f"count:{task}",
                          f"MIGRATIONS.md: {task} says {count} tables and lists {len(listed.get(task, ()))}")
        pms = g.load_json(g.ROOT / "handoff" / "service-docs" / "pms-map.json", {}) or {}
        desc = g.load_json(g.ROOT / "handoff" / "service-docs" / "op-descriptions.json", {}) or {}
        for task, ts in sorted(listed.items()):
            body = desc.get(str(pms.get(task, task)), "")   # a ticket not pushed yet is keyed by its plan key
            if not body or "## Tables" not in body:
                continue
            seg = body.split("## Tables", 1)[1].split("\n## ", 1)[0]
            on_ticket = set(re.findall(r"`([a-z_]+\.[a-z_0-9]+)`", seg)) - {""}
            on_ticket = {x for x in on_ticket if not x.endswith(".sql")}
            if on_ticket != ts:
                guard.add("D-MIG-TABLES", f"ticket:{task}",
                          f"{task}: ticket lists {len(on_ticket)} tables, MIGRATIONS.md {len(ts)} "
                          f"(only on ticket: {', '.join(sorted(on_ticket - ts)[:3])}; "
                          f"only in MIGRATIONS.md: {', '.join(sorted(ts - on_ticket)[:3])})")
        # R051: a migration follows only migrations ordered before it.
        order = {task: int(n) for n, task in re.findall(r"^\| (\d+) \| `[^`]+` \| (MIG-[A-Z-]+) \|", text, re.M)}
        for task, n in sorted(order.items()):
            body = desc.get(str(pms.get(task, task)), "")   # a ticket not pushed yet is keyed by its plan key
            follows = re.search(r"^- Follows: (.*)$", body, re.M)
            for dep in re.findall(r"MIG-[A-Z-]+", follows.group(1) if follows else ""):
                if dep in order and order[dep] >= n:
                    guard.add("D-MIG-ORDER", f"{task}->{dep}",
                              f"{task} (#{n}) follows {dep}, which MIGRATIONS.md orders #{order[dep]}")
        base = desc.get(str(pms.get("MIG-BASELINE", "")), "")
        if base and not all(w in base.lower() for w in ("schema", "ltree", "row-level security")):
            guard.add("D-MIG-ORDER", "MIG-BASELINE:contents",
                      "MIG-BASELINE does not say it creates the schemas, the ltree extension and the "
                      "row-level security helpers every later migration assumes (R056)")

    # R093 R119: naming-and-style 6.1.
    for t, cols in sorted(tables.items()):
        for c, line in cols.items():
            parts = line.split()
            if len(parts) > 1 and parts[1].lower() == "boolean" and not BOOL_OK.search(c):
                guard.add("D-NAMING", f"{t}.{c}", f"{t}.{c}: a boolean that does not read as an assertion")
    for db in ("tenant", "control"):
        for f in (backend / db).glob("*.sql"):
            for uniq, name, t in re.findall(r"CREATE (UNIQUE )?INDEX (?:IF NOT EXISTS )?(\S+) ON (?:ONLY )?"
                                            r"([a-z_]+\.[a-z_0-9]+)", f.read_text(encoding="utf-8")):
                want = "_uniq" if uniq else "_idx"
                if not name.endswith(want) and not name.endswith("_gist") and not name.endswith("_idx"):
                    guard.add("D-NAMING", f"index:{name}", f"{name} on {t}: an index name should end {want}")

    # R082: a key named for one table that references another.
    for t, cols, target in fks:
        stem = re.sub(r"_ids?$", "", cols[-1])
        tname = target.split(".")[-1]
        if stem in ("current", "previous", "next", "original", "source", "target", "replacement", "parent"):
            continue  # a role within one table's own history, not a table name
        if stem in FK_ALIASES:
            alias = FK_ALIASES[stem]
            if alias and alias not in tname:
                guard.add("D-FK-TARGET-NAME", f"{t}.{cols[-1]}", f"{t}.{cols[-1]} references {target}")
            continue
        head = stem.split("_")[-1]
        if not (tname.endswith(stem) or stem.endswith(tname) or head in tname.split("_") or tname in stem
                or ACTOR.search(stem)):
            guard.add("D-FK-TARGET-NAME", f"{t}.{cols[-1]}", f"{t}.{cols[-1]} references {target}")

    # R111: the same data in a jsonb column and in a child table.
    for t, cols in sorted(tables.items()):
        for c, line in cols.items():
            parts = line.split()
            if len(parts) > 1 and parts[1].lower().startswith("jsonb"):
                sing = c[:-3] + "y" if c.endswith("ies") else (c[:-1] if c.endswith("s") else c)
                for child in (f"{t}_{sing}", f"{t}_{c}"):
                    if child in tables and any(k.startswith(t.split(".")[-1]) for k in tables[child]):
                        guard.add("D-JSONB-TWIN", f"{t}.{c}", f"{t}.{c} is jsonb and {child} holds the same rows")

    # R160: a renamed table's old name left in DDL comments and contract prose.
    renames = [(str(r.get("from")), str(r.get("to"))) for r in
               ((g.load_json(g.ROOT / "handoff" / "schema-history.json", {}) or {}).get("renames") or [])
               if r.get("from") and r.get("to")]
    live = set(tables)
    for db in ("tenant", "control"):
        for f in (backend / db).glob("*.sql"):
            text = f.read_text(encoding="utf-8")
            for old, new in renames:
                if old in live:
                    continue
                for m in re.finditer(r"(?<![\w.])" + re.escape(old) + r"(?![\w])", text):
                    line = text[text.rfind("\n", 0, m.start()) + 1:text.find("\n", m.end())]
                    if re.search(r"renamed|was |formerly|previously|history", line, re.I):
                        continue
                    guard.add("D-RENAME-RESIDUE", f"{f.name}:{old}",
                              f"{f.relative_to(g.ROOT).as_posix()} names {old}, renamed to {new}")
                    break
    for stem, rel, doc in g.contracts():
        raw = (g.ROOT / rel).read_text(encoding="utf-8")
        for old, new in renames:
            if old in live:
                continue
            for m in re.finditer(r"(?<![\w.])" + re.escape(old) + r"(?![\w])", raw):
                line = raw[raw.rfind("\n", 0, m.start()) + 1:raw.find("\n", m.end())]
                if re.search(r"renamed|was |formerly|previously|history", line, re.I):
                    continue
                guard.add("D-RENAME-RESIDUE", f"{rel}:{old}", f"{rel} names {old}, renamed to {new}")
                break
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
