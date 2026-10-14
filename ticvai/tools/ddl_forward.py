#!/usr/bin/env python3
"""The difference between the frozen baseline DDL and what `derive-ddl.py` would write now.

**Used by `derive-ddl.py` in frozen mode** (plan item 1C, C3): once `r1` exists the baseline files
under `backend/` are never rewritten, and a change to the schema reference reaches the databases as
the next forward migration, `backend/<area>/V<nnnn>__after_r1_<yyyymmdd>.sql`.

**Additive only.** What is written: a new table (with its keys, indexes, row-level security and
partitions), a new column, a new index, a new schema or function, and a constraint that touches only
new columns. What is not: a dropped or renamed table or column, a changed column type, default,
nullability or check, a changed or dropped index, constraint or function, and a constraint added to
columns that already hold data. **Those are listed for a person** in `handoff/migration-review.md`,
because each one has a data question behind it (backfill, rewrite, which rows survive) that a
generator cannot answer. `backend/MIGRATIONS.md`: *additive first -- add column, backfill, switch
reads, drop old -- four migrations, not one.*

**A row-level-security policy change on an existing table is written too** (CHG-GEN-004, 14 October 2026):
`SELECT platform.drop_rls_policies(t)` and then the table's generated `SELECT platform.apply_*_rls(t, ...)`
call, with the old call as its rollback. It touches no row and can be run twice, so it has no data question
for a person; listed for one instead, CR-005's append-only audit policies stayed off the databases while the
review row was read as done. The old call it replaces is not listed as dropped.

**A NOT NULL column without a default is added nullable** and listed: added as NOT NULL it fails on
the first table that already has rows. Setting NOT NULL after the backfill is the person's migration.

**The comparison is statement by statement, not line by line.** Comments are removed and whitespace
collapsed, so a reworded explanation in a generated header is not a schema change. The old side is
the baseline at r1 plus every forward migration already in `backend/<area>/`, so a change is written
once and not again on the next run. A destructive change a person has already written by hand
(`DROP COLUMN`, `DROP TABLE`, `DROP INDEX`, `DROP CONSTRAINT`, `ALTER COLUMN`, `RENAME COLUMN`) is
recognised in those files and stops being listed.

**A declared rename is a rename, not a drop and a create** (CHG-R6-010, ADAM CR-011, 12 October 2026). Without
this a table renamed in `derive-schema-history.py` (`RENAMES`) reached the forward migration as a new, empty
`CREATE TABLE` beside the old one, and a column renamed by `x-ticvai-column` as `ADD COLUMN` beside the old one,
with the old name listed as "dropped". `diff(..., renames=...)` takes the declared table renames and column
renames (`COLUMN_RENAMES`): the new table, its keys, indexes, constraints and policies, and an index or
constraint on a renamed column, are not generated; one "table renamed" or "column renamed" row tells the person
the `ALTER TABLE ... RENAME` to write, and what follows from it. A foreign key that differs only because the
table it points at was renamed is not listed: Postgres follows a renamed table. `ALTER TABLE ... RENAME TO` and
`ALTER INDEX ... RENAME TO` written by hand in a forward migration are recognised, like `RENAME COLUMN`.

This is not a SQL parser. It understands the statements `derive-ddl.py` emits and the handful a
person writes in a forward migration; anything else it cannot place is listed for review rather than
guessed at.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

NAME = r'(?:"[^"]+"|\w+)'
QNAME = rf"{NAME}\.{NAME}"
TABLE_LEVEL = ("CONSTRAINT ", "PRIMARY KEY", "UNIQUE ", "UNIQUE(", "CHECK ", "CHECK(", "FOREIGN KEY",
               "EXCLUDE ")


def split_statements(sql: str) -> list[str]:
    """Statements without comments. Aware of '...' literals, "..." identifiers and $tag$ bodies, so the
    semicolons inside a function body do not end it."""
    out, buf, i, n = [], [], 0, len(sql)
    while i < n:
        c = sql[i]
        if c == "-" and sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "'\"":
            j = i + 1
            while j < n:
                if sql[j] == c:
                    if j + 1 < n and sql[j + 1] == c:
                        j += 2
                        continue
                    break
                j += 1
            buf.append(sql[i:j + 1])
            i = j + 1
            continue
        if c == "$":
            m = re.match(r"\$(\w*)\$", sql[i:])
            if m:
                tag = m.group(0)
                j = sql.find(tag, i + len(tag))
                j = n if j < 0 else j + len(tag)
                buf.append(sql[i:j])
                i = j
                continue
        if c == ";":
            s = "".join(buf).strip()
            if s:
                out.append(s)
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    s = "".join(buf).strip()
    if s:
        out.append(s)
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def unq(name: str) -> str:
    return name.replace('"', "")


def key_of(stmt: str) -> tuple:
    s = norm(stmt)
    m = re.match(rf"CREATE TABLE (?:IF NOT EXISTS )?({QNAME})", s, re.I)
    if m:
        return ("table", unq(m.group(1)))
    m = re.match(rf"CREATE (?:UNIQUE )?INDEX (?:CONCURRENTLY )?(?:IF NOT EXISTS )?({NAME}) ON (?:ONLY )?({QNAME})", s, re.I)
    if m:
        return ("index", unq(m.group(2)).split(".")[0] + "." + unq(m.group(1)))
    m = re.match(rf"ALTER TABLE (?:ONLY )?(?:IF EXISTS )?({QNAME}) ADD CONSTRAINT ({NAME})", s, re.I)
    if m:
        return ("constraint", unq(m.group(1)), unq(m.group(2)))
    m = re.match(r"CREATE (?:OR REPLACE )?FUNCTION ([\w.\"]+\s*\([^)]*\))", s, re.I)
    if m:
        return ("function", norm(unq(m.group(1))))
    return ("stmt", s)


def balanced(s: str, start: int) -> int:
    """Index of the parenthesis closing the one at `start`, quotes respected."""
    depth, i, q = 0, start, None
    while i < len(s):
        c = s[i]
        if q:
            if c == q:
                q = None
        elif c in "'\"":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def top_level_split(s: str) -> list[str]:
    parts, depth, q, buf = [], 0, None, []
    for c in s:
        if q:
            if c == q:
                q = None
        elif c in "'\"":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(norm("".join(buf)))
            buf = []
            continue
        buf.append(c)
    if norm("".join(buf)):
        parts.append(norm("".join(buf)))
    return parts


@dataclass
class Table:
    cols: dict = field(default_factory=dict)       # column -> normalized definition, name included
    constraints: set = field(default_factory=set)  # table-level constraint clauses
    tail: str = ""                                 # after the column list: PARTITION BY, PARTITION OF


def parse_table(stmt: str) -> Table:
    s = norm(stmt)
    m = re.match(rf"CREATE TABLE (?:IF NOT EXISTS )?{QNAME}\s*", s, re.I)
    rest = s[m.end():] if m else s
    t = Table()
    if not rest.startswith("("):
        t.tail = rest                              # CREATE TABLE x PARTITION OF y DEFAULT
        return t
    end = balanced(rest, 0)
    for item in top_level_split(rest[1:end]):
        if item.upper().startswith(TABLE_LEVEL):
            t.constraints.add(item)
        else:
            t.cols[unq(item.split()[0])] = item
    t.tail = norm(rest[end + 1:])
    # **A key column is NOT NULL whether or not it says so** (PostgreSQL makes every primary-key
    # column NOT NULL). derive-schema marks key columns required since 3 October (CHG-TBF-001), so the
    # generator now writes `id uuid PRIMARY KEY NOT NULL` where r1 has `id uuid PRIMARY KEY`. They are
    # the same column; compared as text they listed hundreds of "column changed" reviews that a person
    # could do nothing about.
    keys = set()
    for c in t.constraints:
        m = re.search(r"PRIMARY KEY\s*\(([^)]*)\)", c, re.I)
        if m:
            keys |= {unq(x.strip()) for x in m.group(1).split(",")}
    for name, d in list(t.cols.items()):
        if name in keys or re.search(r"\bPRIMARY KEY\b", d, re.I):
            t.cols[name] = norm(re.sub(r"\s+NOT NULL\b", "", d, flags=re.I))
    return t


def relaxed(coldef: str) -> str:
    """A column definition as frozen mode adds it to a table that already has rows."""
    if " DEFAULT " in f" {coldef.upper()} " or "PRIMARY KEY" in coldef.upper():
        return coldef
    return norm(re.sub(r"\bNOT NULL\b", "", coldef, flags=re.I))


# **The backfill a new scope_path needs, written out** (14 October 2026, CHG-R6G-002, tracker F15). The review row
# for a scope_path added to a table that already has rows said "backfill each row's owning path", which left the
# person to work out where the path comes from, and check-ddl-conventions D-SCOPE-NOTNULL could not tell a column on
# its way to NOT NULL from one forgotten. A table that holds the key of its owning scope node (every `org_unit_id`,
# `scope_id` and `region_id` in the package references platform.scope) takes the path of that node; a row with no
# owner takes the tenant root's path (naming-and-style 5.3), and only then is the column set NOT NULL. A table with
# none of these keeps the general row, and the check keeps failing until a person writes the backfill.
SCOPE_OWNER_KEYS = ("org_unit_id", "scope_id", "region_id")


def scope_path_backfill(t: str, cols) -> str | None:
    """The statements that fill and then close a scope_path added nullable to `t`, or None when the owner is unknown."""
    owner = next((c for c in SCOPE_OWNER_KEYS if c in cols), None)
    if not owner:
        return None
    return (f"UPDATE {t} x SET scope_path = s.path FROM platform.scope s WHERE s.id = x.{owner} AND x.scope_path IS "
            f"NULL; UPDATE {t} SET scope_path = (SELECT path FROM platform.scope WHERE level = 'tenant') WHERE "
            f"scope_path IS NULL; ALTER TABLE {t} ALTER COLUMN scope_path SET NOT NULL")


class Model:
    """Every statement of one database's DDL, keyed so that the same object in two versions pairs up."""

    def __init__(self):
        self.order: list[tuple] = []     # (key, original statement) in apply order
        self.stmts: dict = {}            # key -> normalized statement
        self.tables: dict[str, Table] = {}
        self.handled: set = set()        # (table, column) a person altered by hand in a forward migration

    def add(self, stmt: str) -> None:
        k = key_of(stmt)
        if k not in self.stmts:
            self.order.append((k, stmt))
        self.stmts[k] = norm(stmt)
        if k[0] == "table":
            self.tables[k[1]] = parse_table(stmt)

    def add_file(self, sql: str) -> None:
        for s in split_statements(sql):
            self.add(s)

    def rename_table(self, old: str, new: str) -> None:
        """`ALTER TABLE old RENAME TO new`, written by hand: the table, its constraints and every statement
        naming it follow (index names do not change on a table rename; `ALTER INDEX ... RENAME` moves those)."""
        self.tables[new] = self.tables.pop(old)
        pat = re.compile(r"(?<![\w.])" + re.escape(old) + r"(?![\w])")
        stmts, order = {}, []
        for k, st in self.order:
            nk = k
            if k[0] in ("table", "constraint") and k[1] == old:
                nk = (k[0], new) + k[2:]
            elif k[0] == "stmt":
                nk = ("stmt", pat.sub(new, k[1]))
            stmts[nk] = pat.sub(new, self.stmts[k])
            order.append((nk, pat.sub(new, st)))
        self.stmts, self.order = stmts, order

    def drop(self, pred) -> None:
        for k in [k for k in self.stmts if pred(k)]:
            del self.stmts[k]
        self.order = [(k, s) for k, s in self.order if k in self.stmts]

    def apply_forward(self, sql: str) -> None:
        """A forward migration already written: fold its additions and hand-written drops into the model."""
        for stmt in split_statements(sql):
            s = norm(stmt)
            if re.match(r"INSERT INTO platform\.schema_version\b", s, re.I):
                continue
            m = re.match(rf"ALTER TABLE (?:ONLY )?(?:IF EXISTS )?({QNAME}) RENAME TO ({NAME})$", s, re.I)
            if m and unq(m.group(1)) in self.tables:
                self.rename_table(unq(m.group(1)), unq(m.group(1)).split(".")[0] + "." + unq(m.group(2)))
                continue
            m = re.match(rf"ALTER INDEX (?:IF EXISTS )?({QNAME}|{NAME}) RENAME TO ({NAME})$", s, re.I)
            if m:
                name, to = unq(m.group(1)), unq(m.group(2))
                for k in [k for k in self.stmts if k[0] == "index" and (k[1] == name or k[1].split(".", 1)[1] == name)]:
                    nk = ("index", k[1].split(".")[0] + "." + to)
                    self.stmts[nk] = self.stmts.pop(k)
                    self.order = [(nk if ok == k else ok, st) for ok, st in self.order]
                continue
            m = re.match(rf"ALTER TABLE (?:ONLY )?(?:IF EXISTS )?({QNAME}) (.*)$", s, re.I)
            if m and unq(m.group(1)) in self.tables:
                t, tab = unq(m.group(1)), self.tables[unq(m.group(1))]
                handled = False
                for action in top_level_split(m.group(2)):
                    a = re.match(r"ADD COLUMN (?:IF NOT EXISTS )?(.*)$", action, re.I)
                    if a:
                        tab.cols[unq(a.group(1).split()[0])] = norm(a.group(1))
                        handled = True
                        continue
                    a = re.match(rf"DROP COLUMN (?:IF EXISTS )?({NAME})", action, re.I)
                    if a:
                        tab.cols.pop(unq(a.group(1)), None)
                        handled = True
                        continue
                    a = re.match(rf"ALTER COLUMN ({NAME})", action, re.I)
                    if a:
                        self.handled.add((t, unq(a.group(1))))
                        handled = True
                        continue
                    a = re.match(rf"RENAME COLUMN ({NAME}) TO ({NAME})", action, re.I)
                    if a and unq(a.group(1)) in tab.cols:
                        old = tab.cols.pop(unq(a.group(1)))
                        tab.cols[unq(a.group(2))] = norm(unq(a.group(2)) + " " + old.split(" ", 1)[1])
                        self.handled.add((t, unq(a.group(2))))
                        handled = True
                        continue
                    a = re.match(rf"DROP CONSTRAINT (?:IF EXISTS )?({NAME})", action, re.I)
                    if a:
                        self.drop(lambda k: k[0] == "constraint" and k[1] == t and k[2] == unq(a.group(1)))
                        tab.constraints = {c for c in tab.constraints
                                           if not c.upper().startswith(f"CONSTRAINT {unq(a.group(1)).upper()} ")}
                        handled = True
                if handled:
                    continue
            m = re.match(r"DROP TABLE (?:IF EXISTS )?(.+?)(?: CASCADE| RESTRICT)?$", s, re.I)
            if m:
                for t in (unq(x.strip()) for x in m.group(1).split(",")):
                    self.tables.pop(t, None)
                    self.drop(lambda k, t=t: k[0] in ("table", "constraint") and k[1] == t)
                continue
            m = re.match(rf"DROP INDEX (?:CONCURRENTLY )?(?:IF EXISTS )?({QNAME}|{NAME})", s, re.I)
            if m:
                name = unq(m.group(1))
                self.drop(lambda k: k[0] == "index" and (k[1] == name or k[1].split(".", 1)[1] == name))
                continue
            self.add(stmt)


RLS_CALL = re.compile(r"^SELECT platform\.(apply_\w*rls|drop_rls_policies)\('([^']+)'::regclass", re.I)


def rls_call(stmt: str):
    """`(helper, table)` for a generated row-level-security call (`SELECT platform.apply_*_rls('t'::regclass ...)`),
    else None."""
    m = RLS_CALL.match(norm(stmt))
    return (m.group(1).lower(), unq(m.group(2)), m.group(2)) if m else None


def tables_named(stmt: str, known: set) -> set:
    return {unq(x) for x in re.findall(rf"(?<![\w.]){QNAME}(?![\w(])", stmt)} & known


def constraint_columns(stmt: str) -> set | None:
    m = re.search(r"ADD CONSTRAINT \S+ (?:FOREIGN KEY|UNIQUE|PRIMARY KEY) \(([^)]*)\)", norm(stmt), re.I)
    return {unq(c.strip()) for c in m.group(1).split(",")} if m else None


@dataclass
class Plan:
    """One database's forward migration: what is written, how to reverse it, what a person decides."""
    area: str
    statements: list = field(default_factory=list)
    rollback: list = field(default_factory=list)
    review: list = field(default_factory=list)    # (kind, object, change, what a person does)
    counts: dict = field(default_factory=lambda: {"tables": 0, "columns": 0, "indexes": 0, "other": 0})


def _cols_in_parens(stmt: str) -> set:
    m = re.search(r"\(([^)]*)\)", norm(stmt).split(" ON ", 1)[-1])
    return {unq(x.strip().split()[0]) for x in m.group(1).split(",") if x.strip()} if m else set()


def diff(area: str, old: Model, new: Model, renames: dict | None = None) -> Plan:
    """`renames`: {"tables": {old: new}, "columns": {(table as named now, old column): new column}}, the
    declared renames (CHG-R6-010). Only a table that exists on the old side under its old name and on the new
    side under its new one is treated as renamed; likewise a column."""
    p = Plan(area)
    renames = renames or {}
    known = set(old.tables) | set(new.tables)
    # new name -> old name, for the tables renamed since the old side
    rt = {n: o for o, n in (renames.get("tables") or {}).items()
          if o in old.tables and o not in new.tables and n in new.tables and n not in old.tables}
    # (table now, new column) -> old column, where the old side still has the old column
    rc = {}
    for (t, oc), nc in (renames.get("columns") or {}).items():
        was = old.tables.get(rt.get(t, t))
        if was is not None and oc in was.cols and nc != oc and t in new.tables and nc in new.tables[t].cols:
            rc[(t, nc)] = oc
    old_renamed = {(t, oc) for (t, _n), oc in rc.items()}
    new_tables = set(new.tables) - set(old.tables) - set(rt)
    new_cols: dict[str, set] = {}
    follows: dict[str, list] = {t: [] for t in rt}   # renamed table -> generated objects named for it
    qual = [(re.compile(r"(?<![\w.])" + re.escape(o) + r"(?![\w])"), n) for n, o in rt.items()]

    def subst(st: str) -> str:
        for pat, n in qual:
            st = pat.sub(n, st)
        return st

    def review(kind, obj, change, todo):
        p.review.append((kind, obj, change, todo))

    def on_renamed_col(t, cols) -> bool:
        return bool(cols) and any((t, c) in rc for c in cols)

    def same_but_name(new_name, old_def, new_def) -> bool:
        """The same definition under a new column name. An inline CHECK is named for its table and column
        (`<table>_<column>_chk`), so its name and the column inside it move with a rename and are not a change."""
        old_name = old_def.split(" ", 1)[0]
        was = re.sub(r"(?<![\w])" + re.escape(old_name) + r"(?![\w])", new_name, old_def)
        strip = lambda d: norm(re.sub(r"(?<![\w])CONSTRAINT \S+ ", "", d))
        return strip(was) == strip(new_def)

    for t in sorted(rt):
        o = rt[t]
        cr = sorted((oc, nc) for (tt, nc), oc in rc.items() if tt == t)
        review("table renamed", f"{o} -> {t}", "declared rename (derive-schema-history.py RENAMES)",
               f"ALTER TABLE {o} RENAME TO {t.split('.', 1)[1]}"
               + "".join(f"; ALTER TABLE {t} RENAME COLUMN {oc} TO {nc}" for oc, nc in cr)
               + "; then rename its key, indexes, constraints and policies to the generated names and apply its "
                 "row-level security again (the \"after rename\" row for it)")

    for k, stmt in new.order:
        kind = k[0]
        if k in old.stmts and old.stmts[k] == new.stmts[k]:
            continue
        if kind == "table":
            t = k[1]
            if t in rt:
                a, b = old.tables[rt[t]], new.tables[t]
                for c, d in b.cols.items():
                    oc = rc.get((t, c), c)
                    if oc not in a.cols:
                        review("column added", f"{t}.{c}", f"`{d}`, on a renamed table",
                               "after the rename: ALTER TABLE ... ADD COLUMN in a forward migration")
                    elif not same_but_name(c, a.cols[oc], d):
                        review("column changed", f"{t}.{c}", f"`{a.cols[oc]}` -> `{d}`",
                               "after the rename: write the ALTER COLUMN (and any data rewrite) by hand")
                    else:
                        # an inline CHECK is named for its table: its new name follows the rename
                        follows[t] += [n for n in re.findall(r"CONSTRAINT (\S+) ", d)
                                       if n not in re.findall(r"CONSTRAINT (\S+) ", a.cols[oc])]
                for c in a.cols:
                    if c not in b.cols and (t, c) not in old_renamed:
                        review("column dropped", f"{t}.{c}", "no longer in the schema reference",
                               "a rename or a drop: decide, then RENAME COLUMN or the four-step drop by hand")
                continue
            if t in new_tables:
                p.statements.append(stmt)
                p.rollback.append(f"DROP TABLE IF EXISTS {t};")
                p.counts["tables"] += 1
                continue
            a, b = old.tables[t], new.tables[t]
            for c, d in b.cols.items():
                if (t, c) in rc:
                    oc = rc[(t, c)]
                    same = same_but_name(c, a.cols[oc], d)
                    review("column renamed", f"{t}.{oc} -> {c}",
                           "declared rename (derive-schema-history.py COLUMN_RENAMES)"
                           + ("" if same else f"; the definition changes too: `{a.cols[oc]}` -> `{d}`"),
                           f"ALTER TABLE {t} RENAME COLUMN {oc} TO {c}"
                           + ("" if same else "; then the ALTER COLUMN (and any data rewrite)")
                           + "; rename the indexes and constraints on it to the generated names")
                    continue
                if c not in a.cols:
                    add = relaxed(d)
                    p.statements.append(f"ALTER TABLE {t} ADD COLUMN IF NOT EXISTS {add}")
                    p.rollback.append(f"ALTER TABLE {t} DROP COLUMN IF EXISTS {c};")
                    p.counts["columns"] += 1
                    new_cols.setdefault(t, set()).add(c)
                    if add != d and c == "scope_path":
                        # CHG-GEN-008: a row with no scope_path is invisible to every grant once the table's policy reads
                        # it, so the backfill is due in the same release as the column, not later. CHG-R6G-002: the
                        # backfill is named when the table holds its owning scope's key, before the NOT NULL.
                        fill = scope_path_backfill(t, b.cols)
                        review("not null", f"{t}.{c}", "added nullable; the schema reference says NOT NULL, and row-"
                               "level security reads it",
                               (f"in the forward migration that adds it, backfill first, then the NOT NULL: {fill}"
                                if fill else
                                "backfill each row's owning path in the forward migration that adds it (a row with "
                                "a null scope_path is invisible to every grant), then ALTER COLUMN ... SET NOT NULL"))
                    elif add != d:
                        review("not null", f"{t}.{c}", "added nullable; the schema reference says NOT NULL",
                               "backfill, then ALTER COLUMN ... SET NOT NULL in a forward migration")
                elif a.cols[c] != d and (t, c) not in old.handled:
                    if a.cols[c] == relaxed(d):
                        review("not null", f"{t}.{c}", "still nullable in the databases; the schema reference "
                               "says NOT NULL", "backfill, then ALTER COLUMN ... SET NOT NULL")
                    else:
                        review("column changed", f"{t}.{c}", f"`{a.cols[c]}` -> `{d}`",
                               "type, default, nullability or check changed: write the ALTER COLUMN (and any "
                               "data rewrite) by hand")
            for c in a.cols:
                if c not in b.cols and (t, c) not in old_renamed:
                    review("column dropped", f"{t}.{c}", "no longer in the schema reference",
                           "a rename or a drop: decide, then RENAME COLUMN or the four-step drop by hand")
            for c in sorted(b.constraints - a.constraints):
                review("constraint added", t, f"`{c}`", "existing rows may violate it: validate, then add by hand")
            for c in sorted(a.constraints - b.constraints):
                review("constraint dropped", t, f"`{c}`", "drop by hand if intended")
            if a.tail != b.tail:
                review("table changed", t, f"`{a.tail or '(none)'}` -> `{b.tail or '(none)'}`",
                       "partitioning changed: a table rewrite, planned by hand")
            continue
        if kind == "index":
            on = tables_named(stmt, known)
            if on & set(rt):
                for t in on & set(rt):
                    follows[t].append(k[1].split(".", 1)[1])
                continue
            if any(on_renamed_col(t, _cols_in_parens(stmt)) for t in on):
                review("index after rename", k[1], f"`{new.stmts[k]}`",
                       "names a renamed column: rename the old index to this name (ALTER INDEX ... RENAME TO) "
                       "after the RENAME COLUMN")
                continue
            if k not in old.stmts:
                p.statements.append(stmt)
                p.rollback.append(f"DROP INDEX IF EXISTS {k[1]};")
                p.counts["indexes"] += 1
            elif re.sub(r"lower\(\s*(\"?\w+\"?)\s*\)", r"\1", new.stmts[k]) == old.stmts[k]:
                # **A unique index made case-insensitive is written** (CHG-GEN-006, ADAM CR-066 and CR-079): the same
                # index on lower(column), as common.yaml promises. It touches no row; if two rows differ only in case
                # the CREATE fails and the migration's transaction rolls back, which is the person's signal to merge
                # them. Rollback puts the case-sensitive index back.
                p.statements.append(f"DROP INDEX IF EXISTS {k[1]}")
                p.statements.append(stmt)
                p.rollback.append(f"DROP INDEX IF EXISTS {k[1]}; {old.stmts[k].rstrip(';')};")
                p.counts["indexes"] += 1
            else:
                review("index changed", k[1], f"`{old.stmts[k]}` -> `{new.stmts[k]}`",
                       "DROP INDEX and CREATE INDEX by hand (CONCURRENTLY on a live table)")
            continue
        if kind == "constraint":
            t, name = k[1], k[2]
            cols = constraint_columns(stmt)
            if t in rt:
                follows[t].append(name)
                continue
            if on_renamed_col(t, cols):
                review("constraint after rename", f"{t} {name}", f"`{new.stmts[k]}`",
                       "names a renamed column: rename the old constraint to this name (ALTER TABLE ... RENAME "
                       "CONSTRAINT) after the RENAME COLUMN")
                continue
            if k in old.stmts and subst(old.stmts[k]) == new.stmts[k]:
                continue   # a key to a renamed table: Postgres follows the rename
            if k not in old.stmts and (t in new_tables or (cols and cols <= new_cols.get(t, set()))):
                p.statements.append(stmt)
                if t not in new_tables:
                    p.rollback.append(f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name};")
                p.counts["other"] += 1
            elif k not in old.stmts:
                review("constraint added", f"{t} {name}", f"`{new.stmts[k]}`",
                       "existing rows may violate it: validate, then add by hand (NOT VALID, then VALIDATE)")
            else:
                review("constraint changed", f"{t} {name}", f"`{old.stmts[k]}` -> `{new.stmts[k]}`",
                       "drop and re-add by hand")
            continue
        if kind == "function":
            if k not in old.stmts:
                p.statements.append(stmt)
                p.counts["other"] += 1
            else:
                review("function changed", k[1], "body or signature changed",
                       "CREATE OR REPLACE is not additive when a policy or trigger depends on it: review, then "
                       "write it into a forward migration by hand")
            continue
        s = new.stmts[k]
        m = re.match(rf"CREATE SCHEMA (?:IF NOT EXISTS )?({NAME})", s, re.I)
        if m:
            p.statements.append(stmt)
            p.rollback.append(f"DROP SCHEMA IF EXISTS {m.group(1)};")
            p.counts["other"] += 1
            continue
        if re.match(r"CREATE EXTENSION IF NOT EXISTS\b", s, re.I):
            p.statements.append(stmt)
            p.counts["other"] += 1
            continue
        refs = tables_named(s, known)
        if refs & set(rt):
            for t in refs & set(rt):
                follows[t].append(s[:70])
            continue
        if refs and refs <= new_tables:
            p.statements.append(stmt)
            p.counts["other"] += 1
            continue
        rc_ = rls_call(s)
        if rc_ and rc_[0] != "drop_rls_policies" and rc_[1] in old.tables:
            # **A policy change on a table that already exists is written, not listed** (CHG-GEN-004). The call is
            # the generated helper the baseline used for every table: it drops what was there and creates the
            # policy again, so it is idempotent and touches no row. Listing it for a person is how CR-005's
            # policies stayed off the databases: the review row was read as done, and 920 still said tenant root.
            t = rc_[1]
            was = [old.stmts[k] for k in old.stmts if k[0] == "stmt" and (rls_call(old.stmts[k]) or ("", "", ""))[1] == t
                   and rls_call(old.stmts[k])[0] != "drop_rls_policies"]
            p.statements.append(f"SELECT platform.drop_rls_policies('{rc_[2]}'::regclass)")
            p.statements.append(stmt)
            p.rollback.append(f"SELECT platform.drop_rls_policies('{rc_[2]}'::regclass); "
                              + " ".join(w.rstrip(";") + ";" for w in was))
            p.counts["policies"] = p.counts.get("policies", 0) + 1
            continue
        else:
            review("statement added", ", ".join(sorted(refs)) or "(database)", f"`{s[:160]}`",
                   "touches objects that already exist: write it into a forward migration by hand")

    removed_tables = set(old.tables) - set(new.tables)
    renamed_away = set(rt.values())
    for t, objs in sorted(follows.items()):
        if objs:
            review("after rename", t, f"{len(objs)} generated object(s) for the renamed table: "
                   + ", ".join(f"`{x}`" for x in objs),
                   "in the forward migration that renames the table: rename its old indexes and constraints to "
                   "these names (ALTER INDEX / ALTER TABLE ... RENAME CONSTRAINT) and apply its row-level "
                   "security again")
    renamed_new_stmts = {new.stmts[nk] for nk in new.stmts}
    # Tables the new side applies a policy to: their old policy call is replaced, not dropped (CHG-GEN-004).
    reapplied = {c[1] for c in (rls_call(new.stmts[nk]) for nk in new.stmts if nk[0] == "stmt") if c}
    for k in old.stmts:
        if k in new.stmts:
            continue
        kind = k[0]
        old_call = rls_call(old.stmts[k]) if kind == "stmt" else None
        if old_call and (old_call[0] == "drop_rls_policies" or old_call[1] in reapplied):
            continue
        if kind == "table" and k[1] in renamed_away:
            continue
        if kind in ("constraint", "stmt") and subst(old.stmts[k]) in renamed_new_stmts:
            continue   # unchanged but for a renamed table it names
        if kind == "constraint" and (constraint_columns(old.stmts[k]) or set()) & {oc for (tt, oc) in old_renamed
                                                                                   if tt == k[1]}:
            continue   # on a renamed column: the "column renamed" row covers it
        if kind == "index" and any((t, c) in old_renamed for t in tables_named(old.stmts[k], known)
                                   for c in _cols_in_parens(old.stmts[k])):
            continue
        if kind == "table":
            review("table dropped", k[1], "no longer in the schema reference",
                   "a rename or a drop: decide, then ALTER TABLE ... RENAME or DROP TABLE by hand")
        elif kind in ("index",):
            if not any(k[1].split(".", 1)[1].startswith(t.split(".", 1)[1] + "_") for t in removed_tables):
                review("index dropped", k[1], "no longer generated", "DROP INDEX by hand if intended")
        elif kind == "constraint":
            if k[1] not in removed_tables:
                review("constraint dropped", f"{k[1]} {k[2]}", "no longer generated",
                       "ALTER TABLE ... DROP CONSTRAINT by hand if intended")
        elif kind == "function":
            review("function dropped", k[1], "no longer generated", "DROP FUNCTION by hand if intended")
        else:
            refs = tables_named(old.stmts[k], known)
            if not (refs and refs <= removed_tables):
                review("statement dropped", ", ".join(sorted(refs)) or "(database)", f"`{old.stmts[k][:160]}`",
                       "undo it by hand if intended")
    return p


def render(p: Plan, version: str, baseline: str, stamp: str) -> str:
    """The forward migration file for one database."""
    body = "\n\n".join(s.rstrip().rstrip(";") + ";" for s in p.statements)
    checksum = hashlib.sha256(body.encode("utf-8")).hexdigest()
    what = (f"{p.counts['tables']} table(s), {p.counts['columns']} column(s), {p.counts['indexes']} index(es), "
            f"{p.counts['other']} other statement(s)"
            + (f", {p.counts['policies']} row-level security polic(ies) re-applied" if p.counts.get("policies") else ""))
    desc = f"after {baseline}: {what}"
    lines = [
        f"-- {version} -- {p.area} database, after {baseline} ({stamp}).",
        "-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**",
        "--",
        f"-- The baseline under backend/{p.area}/ is frozen at {baseline}, so the change to the schema reference",
        "-- since then is written here instead: additive only. Changes that are not additive (drops, renames,",
        "-- type changes) are not generated; they are listed for a person in handoff/migration-review.md.",
        f"-- {what}.",
        "",
        body,
        "",
        "INSERT INTO platform.schema_version (version, description, checksum)",
        f"VALUES ('{version}', '{desc}', '{checksum}')",
        "ON CONFLICT (version) DO NOTHING;",
        "",
        "-- ============================================================================",
        "-- ROLLBACK",
        "-- ============================================================================",
        "-- Commented out so that applying this file never runs it: the rollback is run by removing the",
        "-- leading `-- `, and is tested in CI against a restored snapshot (backend/MIGRATIONS.md).",
    ] + [f"-- {r}" for r in reversed(p.rollback)] + [
        f"-- DELETE FROM platform.schema_version WHERE version = '{version}';",
        "",
    ]
    return "\n".join(lines)


def render_review(plans: list[Plan], baseline: str, stamp: str, extra: list | None = None) -> str:
    rows = [(p.area,) + r for p in plans for r in p.review] + list(extra or [])
    out = [
        "# Migration changes for a person",
        "",
        f"**Written by `tools/derive-ddl.py` in frozen mode ({stamp}). Do not edit; it is rewritten on every run.**",
        "",
        f"The baseline migrations under `backend/` are frozen at `{baseline}` (`tools/check-migration-freeze.py`). "
        "`derive-ddl.py` writes additive changes (new tables, columns and indexes) as the next forward migration, "
        "`backend/<area>/V<nnnn>__*.sql`. **The changes below it does not write**, because each has a data "
        "question behind it: which rows survive a drop, what fills a new NOT NULL column, whether a rename is a "
        "rename. Write each as a forward migration by hand; once a forward migration carries it, it leaves this "
        "list.",
        "",
    ]
    if not rows:
        out.append("Nothing waits for a person: every change since the baseline is additive and generated.")
        return "\n".join(out) + "\n"
    out += [f"**{len(rows)} change(s).**", "",
            "| Kind | Database | Object | Change | What a person does |", "|---|---|---|---|---|"]
    for area, kind, obj, change, todo in rows:
        cell = lambda x: str(x).replace("|", "\\|")
        out.append(f"| {cell(kind)} | {cell(area)} | `{cell(obj)}` | {cell(change)} | {cell(todo)} |")
    return "\n".join(out) + "\n"
