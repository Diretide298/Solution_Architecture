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

**A changed generated helper is written too** (CHG-RSF-001, 18 October 2026): `platform.apply_*_rls`,
`platform.visible_parent_ids` and `platform.visible_parent_ids_setup` are replaced with CREATE OR REPLACE, and every table
whose policy an `apply_*_rls` helper built is applied again; any other changed function is still listed.

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
**A rename into another schema is a move** (CHG-XDW-001, 14 October 2026: CrossRegionService's four records left
`platform` for `sync`): its row says `ALTER TABLE ... SET SCHEMA` (then `RENAME TO` only if the name changes too),
and a hand-written `ALTER TABLE ... SET SCHEMA` is recognised like `RENAME TO`. Postgres moves the table's
indexes and constraints with it.

**What the generator derived reaches the migration owner whole** (CHG-MGN-001, ADAM CR-138, CR-139, CR-148, CR-156,
CR-157, 18 October 2026). A review row carries every statement in full, never a prefix. A column the contract retires
(`x-ticvai-retired-columns`, passed as `retired=`) is a drop, not "a rename or a drop: decide": its row names the
four-step drop with its key and indexes, and the forward migration drops its NOT NULL at once (guarded, so a database
where the column is already gone applies it). A table CHECK added to an existing table is written (NOT VALID, then
VALIDATE, after dropping one of the same name a person may have added), and a new index on a renamed column is
listed whole to create after the rename.

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


# **A table whose rows followed a parent's policy before they had a scope_path of their own takes the parent's path**
# (CHG-STO-011, 14 October 2026): `orders.invitation` was read through its product (apply_parent_rls on product_id)
# until the contract's `Invitation.scopePath` reached it (Marketing's invitation had taken its name, so Orders' fields
# never did); an existing invitation belongs where its product does. table -> (key column, parent table).
SCOPE_FILL_FROM = {
    "orders.invitation": ("product_id", "catalogue.product"),
}

# **A row whose path is its parent's while it is bound** (ADAM CR-095, 18 October 2026; CHG-RSF-001). A device bound
# to a workstation carries that workstation's path, set by the server when it is bound and moved when it is bound
# elsewhere, so the device's own session, scoped to the workstation, can write its heartbeat. table -> (key column,
# parent table, the level its rows then sit at). check-rls-scope-fit reads it (RF-DEVICE-ABOVE); the backfill below
# moves existing rows.
SCOPE_FOLLOWS = {
    "platform.device": ("workstation_id", "platform.workstation", "workstation"),
}

# **A generated row-level-security helper is the generator's own** (ADAM CR-108, 18 October 2026; CHG-RSF-001). No
# policy depends on an `apply_*_rls` helper: a policy stores the predicate the helper built when it ran, so a changed
# helper is written with CREATE OR REPLACE and every table that uses it is applied again. `platform.visible_parent_ids`,
# which policies do call, keeps its OID through CREATE OR REPLACE and needs no re-apply; `visible_parent_ids_setup` is
# called only by the helpers. Any other changed function is still listed for a person.
REPLACEABLE = re.compile(r"^platform\.(apply_\w+_rls|visible_parent_ids|visible_parent_ids_setup)\s*\(", re.I)
# The helpers that ask platform.visible_parent_ids: a renamed table's policy under one of them is written under the
# table's current name (CHG-RSF-001, fix round 1); a policy belongs to the table and moves with its rename.
ACROSS_HELPERS = ("apply_parent_across_rls", "apply_parent_split_across_rls")




# **A table that was the tenant root's alone has rows only the tenant root wrote** (MOD audit, 14 October 2026,
# CHG-MOD-007). Until its scope_path arrives, its policy (`apply_tenant_rls`) let no other connection insert a row, so
# every row it holds sits at the tenant root by construction: the backfill is the tenant root's path, then NOT NULL.
def scope_path_backfill(t: str, cols, was_tenant_root: bool = False) -> str | None:
    """The statements that fill and then close a scope_path added nullable to `t`, or None when the owner is unknown.
    `was_tenant_root`: the table's policy before this migration was the tenant root's alone."""
    if t in SCOPE_FOLLOWS and SCOPE_FOLLOWS[t][0] in cols:
        key, parent, _level = SCOPE_FOLLOWS[t]
        return (f"UPDATE {t} x SET scope_path = p.scope_path FROM {parent} p WHERE p.id = x.{key} AND x.scope_path IS "
                f"DISTINCT FROM p.scope_path; UPDATE {t} SET scope_path = (SELECT path FROM platform.scope WHERE level "
                f"= 'tenant') WHERE scope_path IS NULL; ALTER TABLE {t} ALTER COLUMN scope_path SET NOT NULL")
    if t in SCOPE_FILL_FROM and SCOPE_FILL_FROM[t][0] in cols:
        key, parent = SCOPE_FILL_FROM[t]
        return (f"UPDATE {t} x SET scope_path = p.scope_path FROM {parent} p WHERE p.id = x.{key} AND x.scope_path IS "
                f"NULL; UPDATE {t} SET scope_path = (SELECT path FROM platform.scope WHERE level = 'tenant') WHERE "
                f"scope_path IS NULL; ALTER TABLE {t} ALTER COLUMN scope_path SET NOT NULL")
    owner = next((c for c in SCOPE_OWNER_KEYS if c in cols), None)
    if not owner and was_tenant_root:
        return (f"UPDATE {t} SET scope_path = (SELECT path FROM platform.scope WHERE level = 'tenant') WHERE "
                f"scope_path IS NULL; ALTER TABLE {t} ALTER COLUMN scope_path SET NOT NULL")
    if not owner:
        return None
    return (f"UPDATE {t} x SET scope_path = s.path FROM platform.scope s WHERE s.id = x.{owner} AND x.scope_path IS "
            f"NULL; UPDATE {t} SET scope_path = (SELECT path FROM platform.scope WHERE level = 'tenant') WHERE "
            f"scope_path IS NULL; ALTER TABLE {t} ALTER COLUMN scope_path SET NOT NULL")


# **A column the contract retires loses its NOT NULL at once** (CHG-MGN-001, ADAM CR-157, 18 October 2026). The
# contract withdraws it (`x-ticvai-retired-columns`), so no code writes it any more, and an insert that leaves it out
# must not fail. Dropping NOT NULL touches no row. **Guarded**, because the migration owner may already have dropped
# the column by hand (the four-step drop): the statement then does nothing rather than failing the migration.
RETIRE_GUARD = re.compile(
    r"^DO \$\$ BEGIN IF EXISTS \(SELECT 1 FROM information_schema\.columns WHERE table_schema = '(\w+)' AND "
    r"table_name = '(\w+)' AND column_name = '(\w+)' AND is_nullable = 'NO'\) THEN ALTER TABLE \S+ ALTER COLUMN "
    r"\S+ DROP NOT NULL; END IF; END \$\$$", re.I)


def retire_not_null(t: str, c: str) -> str:
    """The guarded `ALTER COLUMN ... DROP NOT NULL` for a retired column (recognised again by RETIRE_GUARD)."""
    sch, name = t.split(".", 1)
    return (f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = '{unq(sch)}' AND "
            f"table_name = '{unq(name)}' AND column_name = '{unq(c)}' AND is_nullable = 'NO') THEN ALTER TABLE {t} "
            f"ALTER COLUMN {c} DROP NOT NULL; END IF; END $$")


def _inline_check(coldef: str):
    """(name, the whole `CONSTRAINT <name> CHECK (...)` text, the expression inside) of a column's inline CHECK."""
    m = re.search(r"CONSTRAINT (\S+) CHECK \(", coldef, re.I)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    for j in range(i, len(coldef)):
        depth += {"(": 1, ")": -1}.get(coldef[j], 0)
        if depth == 0:
            return m.group(1), coldef[m.start():j + 1], coldef[i + 1:j]
    return None


IN_LIST = re.compile(r"^(\w+) IN \((.*)\)$", re.S)


def widened_check(old_def: str, new_def: str):
    """**A column CHECK that only gained values** (CHG-R8MIG-006): the same column but for an inline
    `CHECK (col IN (...))` whose new list holds every old value and more. Returns (constraint name, the new
    `CONSTRAINT ... CHECK (...)` clause), else None. Widening refuses no row that was valid, so it is additive."""
    o, n = _inline_check(old_def), _inline_check(new_def)
    if not o or not n or o[0] != n[0]:
        return None
    if norm(old_def.replace(o[1], "")) != norm(new_def.replace(n[1], "")):
        return None
    mo, mn = IN_LIST.match(o[2].strip()), IN_LIST.match(n[2].strip())
    if not mo or not mn or mo.group(1) != mn.group(1):
        return None
    vals = lambda s: {v.strip() for v in re.findall(r"'(?:[^']|'')*'", s)}
    old_v, new_v = vals(mo.group(2)), vals(mn.group(2))
    if not old_v or not old_v < new_v:
        return None
    return n[0], n[1]


def changed_check_only(old_def: str, new_def: str):
    """(name, the new `CONSTRAINT ... CHECK (...)` clause) when the column changes only by gaining an inline CHECK or
    by a CHECK of the same name that is not a widening (CHG-R8MIG-011); else None."""
    n = _inline_check(new_def)
    if not n:
        return None
    o = _inline_check(old_def)
    if o and o[0] != n[0]:
        return None
    if norm(old_def.replace(o[1], "") if o else old_def) != norm(new_def.replace(n[1], "")):
        return None
    return n[0], n[1]


def guard_add_constraint(t: str, name: str, stmt: str) -> str:
    """`stmt` (an ALTER TABLE ... ADD CONSTRAINT) only when the constraint is not there yet (CHG-R8MIG-010)."""
    return (f"DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = '{name}' AND conrelid = "
            f"to_regclass('{t}')) THEN {norm(stmt).rstrip(';')}; END IF; END $$")


def guard_drop_constraint(t: str, name: str) -> str:
    return (f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = '{name}' AND conrelid = "
            f"to_regclass('{t}')) THEN ALTER TABLE {t} DROP CONSTRAINT {name}; END IF; END $$")


def only_not_null_dropped(old_def: str, new_def: str) -> bool:
    """`new_def` is `old_def` with its NOT NULL taken off and nothing else changed (not a key column)."""
    if "PRIMARY KEY" in old_def.upper() or not re.search(r"\bNOT NULL\b", old_def, re.I):
        return False
    return norm(re.sub(r"\s+NOT NULL\b", "", old_def, flags=re.I)) == norm(new_def)


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

    def rename_column(self, t: str, a: str, b: str) -> None:
        """`RENAME COLUMN a TO b` on `t`: the indexes, keys and policy calls that name the column follow, as
        PostgreSQL rewrites them. A foreign key from another table follows only inside `REFERENCES t (...)`."""
        word = re.compile(r"(?<![\w.])" + re.escape(a) + r"(?![\w])")
        tab = self.tables[t]
        if a in tab.cols:
            d = word.sub(b, tab.cols.pop(a))
            tab.cols[b] = d
        tab.constraints = {word.sub(b, c) if not re.search(r"REFERENCES", c, re.I)
                           else self._ref_sub(word, b, c, t) for c in tab.constraints}
        qt = re.compile(r"(?<![\w.])" + re.escape(t) + r"(?![\w])")

        def fix(k, st):
            if k[0] == "index" and qt.search(st):
                head, _, rest = st.partition(" ON ")
                return head + " ON " + word.sub(b, rest)
            if k[0] == "constraint":
                return self._ref_sub(word, b, st, t, only_target=k[1] != t)
            if k[0] == "stmt":
                c = rls_call(st)
                if c and c[1] == t:
                    return st.replace(f"'{a}'", f"'{b}'")
            return st

        new_stmts, new_order = {}, []
        for k, st in self.order:
            new_order.append((k, fix(k, st)))
        for k, st in self.stmts.items():
            new_stmts[k] = fix(k, st)
        self.stmts, self.order = new_stmts, new_order

    @staticmethod
    def _ref_sub(word, b, st, t, only_target: bool = False) -> str:
        """Substitute a column name in a foreign key: the key's own columns (the table is `t`) and, when the key
        points at `t`, the target list. Spacing is kept as written."""
        m = re.search(r"REFERENCES", st, re.I)
        if not m:
            return st if only_target else word.sub(b, st)
        head, tail = st[:m.start()], st[m.start():]
        mm = re.match(r"(REFERENCES\s+(\S+?)\s*)(\([^)]*\))", tail, re.I)
        if mm and unq(mm.group(2)) == t:
            tail = tail[:mm.start(3)] + word.sub(b, mm.group(3)) + tail[mm.end(3):]
        if not only_target:
            head = word.sub(b, head)
        return head + tail

    def rename_constraint(self, t: str, old: str, new: str) -> None:
        tab = self.tables.get(t)
        if tab is not None:
            for c, d in list(tab.cols.items()):
                tab.cols[c] = d.replace(f"CONSTRAINT {old} ", f"CONSTRAINT {new} ")
            tab.constraints = {c.replace(f"CONSTRAINT {old} ", f"CONSTRAINT {new} ") for c in tab.constraints}
        k = ("constraint", t, old)
        if k in self.stmts:
            nk = ("constraint", t, new)
            self.stmts[nk] = self.stmts.pop(k).replace(f"ADD CONSTRAINT {old} ", f"ADD CONSTRAINT {new} ")
            self.order = [(nk if ok == k else ok, st.replace(f"ADD CONSTRAINT {old} ", f"ADD CONSTRAINT {new} ")
                           if ok == k else st) for ok, st in self.order]

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
            g = None if RETIRE_GUARD.match(s) else GUARD.match(s)
            from_guard = bool(g)
            if g:
                # a guarded rename, key or dropped index (R8-MIG-001): fold in the one change it makes
                stmt = s = re.sub(r" NOT VALID$", "", norm(g.group("body")), flags=re.I)
            m = RETIRE_GUARD.match(s)
            if m and f"{m.group(1)}.{m.group(2)}" in self.tables:
                t, c = f"{m.group(1)}.{m.group(2)}", m.group(3)
                tab = self.tables[t]
                if c in tab.cols:
                    tab.cols[c] = norm(re.sub(r"\s+NOT NULL\b", "", tab.cols[c], flags=re.I))
                self.handled.add((t, c))
                continue
            m = re.match(rf"ALTER TABLE (?:ONLY )?(?:IF EXISTS )?({QNAME}) RENAME TO ({NAME})$", s, re.I)
            if m and unq(m.group(1)) in self.tables:
                self.rename_table(unq(m.group(1)), unq(m.group(1)).split(".")[0] + "." + unq(m.group(2)))
                continue
            m = re.match(rf"ALTER TABLE (?:ONLY )?(?:IF EXISTS )?({QNAME}) SET SCHEMA ({NAME})$", s, re.I)
            if m and unq(m.group(1)) in self.tables:
                self.rename_table(unq(m.group(1)), unq(m.group(2)) + "." + unq(m.group(1)).split(".", 1)[1])
                continue
            m = re.match(rf"ALTER INDEX (?:IF EXISTS )?({QNAME}|{NAME}) RENAME TO ({NAME})$", s, re.I)
            if m:
                name, to = unq(m.group(1)), unq(m.group(2))
                for k in [k for k in self.stmts if k[0] == "index" and (k[1] == name or k[1].split(".", 1)[1] == name)]:
                    nk = ("index", k[1].split(".")[0] + "." + to)
                    ren = lambda x, o=k[1].split(".", 1)[1]: re.sub(
                        rf"(INDEX (?:IF NOT EXISTS )?){re.escape(o)}\b", rf"\g<1>{to}", x, count=1)
                    self.stmts[nk] = ren(self.stmts.pop(k))
                    self.order = [(nk, ren(st)) if ok == k else (ok, st) for ok, st in self.order]
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
                        self.rename_column(t, unq(a.group(1)), unq(a.group(2)))
                        if not from_guard:   # a written rename leaves the column's other differences listed
                            self.handled.add((t, unq(a.group(2))))
                        handled = True
                        continue
                    a = re.match(rf"RENAME CONSTRAINT ({NAME}) TO ({NAME})", action, re.I)
                    if a:
                        self.rename_constraint(t, unq(a.group(1)), unq(a.group(2)))
                        handled = True
                        continue
                    # A table CHECK a forward migration added (NOT VALID, then VALIDATE; CHG-MGN-001) is the table's
                    # constraint, as it is in the generated CREATE TABLE, so the next diff does not write it again.
                    a = re.match(rf"ADD (CONSTRAINT {NAME} CHECK .*?)(?: NOT VALID)?$", action, re.I)
                    if a:
                        # a column CHECK widened in place (CHG-R8MIG-006) replaces the column's inline CHECK
                        added = norm(a.group(1))
                        nm = _inline_check(added)
                        inline = [c_ for c_, d_ in tab.cols.items()
                                  if nm and (_inline_check(d_) or ("",))[0] == nm[0]]
                        # a CHECK added to a column that had none (CHG-R8MIG-011): named `<table>_<column>_chk`
                        bare = [c_ for c_, d_ in tab.cols.items() if nm and not _inline_check(d_)
                                and nm[0] == f"{t.split('.', 1)[1]}_{c_}_chk"]
                        if inline:
                            d_ = tab.cols[inline[0]]
                            tab.cols[inline[0]] = norm(d_.replace(_inline_check(d_)[1], added))
                        elif bare:
                            tab.cols[bare[0]] = norm(tab.cols[bare[0]] + " " + added)
                        else:
                            tab.constraints.add(added)
                        handled = True
                        continue
                    if re.match(rf"VALIDATE CONSTRAINT {NAME}$", action, re.I):
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


# **Renames, keys and dropped indexes are written, guarded** (R8-MIG-001, cause ORDERS-MONEY-C23, 19 October 2026).
# Until now every pure column rename (254 of them), every foreign key declared since r1 and every index that is no
# longer generated sat in handoff/migration-review.md "for a person", and no migration ticket carried them, so the
# DDL a developer copies had the old names. They go into a second forward file (the "reconcile" file). Each statement
# is a `DO $$ ... IF <guard> THEN <one change>; END IF; END $$` block, because the databases it runs on were built
# from the old DDL by migrations written before this file existed, and some tables are created by migrations that
# come after it (V1000 upwards, copied from the same DDL): a block whose objects are not there yet does nothing, and
# the migration that creates them copies the block for its own tables (the ticket says so). Applying the file twice
# changes nothing. A `DO` block is recognised again by `unwrap_guard`, so the next run sees the change as done.
GUARD = re.compile(r"^DO \$\$ BEGIN IF (?P<guard>.*?) THEN (?P<body>(?:ALTER TABLE|ALTER INDEX|DROP INDEX|CREATE (?:UNIQUE )?INDEX) .*?); "
                   r"END IF; END \$\$$", re.I | re.S)


def _col_exists(sch: str, tab: str, col: str) -> str:
    return (f"EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = '{sch}' AND "
            f"table_name = '{tab}' AND column_name = '{col}')")


def _split_t(t: str) -> tuple:
    sch, name = unq(t).split(".", 1)
    return sch, name


def tag(table: str, kind: str, detail: str, stmt: str, other: str = "") -> str:
    """A one-line comment before a block, `-- <table> | <kind> | <detail> [| <other table>]`, so the migration ticket of
    the table can list what the block does to it (ticket_done.names_changes). Comments are not statements."""
    return f"-- {table} | {kind} | {detail}" + (f" | {other}" if other else "") + "\n" + stmt


def guard_rename_column(t: str, old: str, new: str) -> str:
    sch, name = _split_t(t)
    return (f"DO $$ BEGIN IF {_col_exists(sch, name, old)} AND NOT {_col_exists(sch, name, new)} THEN "
            f"ALTER TABLE {t} RENAME COLUMN {old} TO {new}; END IF; END $$")


def guard_rename_index(t: str, old: str, new: str) -> str:
    sch, _ = _split_t(t)
    return (f"DO $$ BEGIN IF to_regclass('{sch}.{old}') IS NOT NULL AND to_regclass('{sch}.{new}') IS NULL THEN "
            f"ALTER INDEX {sch}.{old} RENAME TO {new}; END IF; END $$")


def guard_rename_constraint(t: str, old: str, new: str) -> str:
    return (f"DO $$ BEGIN IF EXISTS (SELECT 1 FROM pg_constraint WHERE conname = '{old}' AND conrelid = "
            f"to_regclass('{t}')) AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = '{new}' AND conrelid = "
            f"to_regclass('{t}')) THEN ALTER TABLE {t} RENAME CONSTRAINT {old} TO {new}; END IF; END $$")


def guard_create_index(t: str, stmt: str, cols) -> str:
    sch, name = _split_t(t)
    have = " AND ".join(_col_exists(sch, name, c) for c in sorted(cols))
    return f"DO $$ BEGIN IF {have} THEN {norm(stmt).rstrip(';')}; END IF; END $$"


def guard_drop_index(idx: str) -> str:
    return f"DO $$ BEGIN IF to_regclass('{idx}') IS NOT NULL THEN DROP INDEX {idx}; END IF; END $$"


FK = re.compile(rf"^ALTER TABLE (?:ONLY )?({QNAME}) ADD CONSTRAINT ({NAME}) FOREIGN KEY \(([^)]*)\) REFERENCES "
                rf"({QNAME})\s*\(([^)]*)\)(.*)$", re.I)


def parse_fk(stmt: str):
    m = FK.match(norm(stmt))
    if not m:
        return None
    cols = [unq(x.strip()) for x in m.group(3).split(",")]
    pcols = [unq(x.strip()) for x in m.group(5).split(",")]
    return unq(m.group(1)), unq(m.group(2)), cols, unq(m.group(4)), pcols, m.group(6).strip()


def guard_foreign_key(stmt: str, not_valid: bool = True) -> str | None:
    """The foreign key, added NOT VALID when both tables exist, its columns exist and have the same type, the
    parent's columns are a unique key, and the constraint is not there. NOT VALID: it enforces every new write and
    takes no scan of the rows already there, so a database holding a row that breaks it still applies this file;
    `VALIDATE CONSTRAINT` is the owner's, when the data is clean. **A partitioned table cannot take a NOT VALID key**
    (PostgreSQL 12 to 17: "cannot add NOT VALID foreign key on partitioned table"), so its key is added checked,
    which scans the rows already there; on the partitioned tables of the first release that is a few rows."""
    f = parse_fk(stmt)
    if not f:
        return None
    t, name, cols, parent, pcols, tail = f
    if "NOT VALID" in tail.upper():
        return None
    (tsch, tn), (psch, pn) = _split_t(t), _split_t(parent)
    exist = " AND ".join([f"to_regclass('{t}') IS NOT NULL", f"to_regclass('{parent}') IS NOT NULL",
                          f"NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = '{name}' AND conrelid = "
                          f"to_regclass('{t}'))"])
    same_type = " AND ".join(
        f"(SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('{t}') AND attname = '{c}') = "
        f"(SELECT atttypid FROM pg_attribute WHERE attrelid = to_regclass('{parent}') AND attname = '{pc}')"
        for c, pc in zip(cols, pcols))
    arr = "ARRAY[" + ", ".join(f"'{c}'" for c in sorted(pcols)) + "]"
    unique = (f"EXISTS (SELECT 1 FROM pg_index i WHERE i.indrelid = to_regclass('{parent}') AND i.indisunique AND "
              f"i.indpred IS NULL AND i.indexprs IS NULL AND (SELECT array_agg(a.attname::text ORDER BY a.attname) "
              f"FROM pg_attribute a WHERE a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey)) = {arr})")
    body = norm(stmt).rstrip(";") + (" NOT VALID" if not_valid else "")
    return f"DO $$ BEGIN IF {exist} AND {same_type} AND {unique} THEN {body}; END IF; END $$"


RLS_CALL = re.compile(r"^SELECT platform\.(apply_\w*rls|drop_rls_policies)\('([^']+)'::regclass", re.I)


def rls_call(stmt: str):
    """`(helper, table)` for a generated row-level-security call (`SELECT platform.apply_*_rls('t'::regclass ...)`),
    else None."""
    m = RLS_CALL.match(norm(stmt))
    return (m.group(1).lower(), unq(m.group(2)), m.group(2)) if m else None


def was_tenant_root(model, t: str) -> bool:
    """`t` had the tenant root's policy alone in `model` before any scope policy: every row it held then was written by
    the tenant root, so its scope_path backfill is the tenant root's path (CHG-MOD-007)."""
    for _k, st in model.order:
        rc = rls_call(st)
        if rc and rc[1] == t and rc[0] != "drop_rls_policies":
            return rc[0] == "apply_tenant_rls"
    return False


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
    # The second forward file (R8-MIG-001): what the first release's generated schema differs from the baseline by
    # NAME, not by shape, written so a database built from the old DDL ends up with the names the contracts use.
    recon: list = field(default_factory=list)
    recon_rollback: list = field(default_factory=list)
    recon_counts: dict = field(default_factory=lambda: {"renames": 0, "keys": 0, "indexes": 0})


def _cols_in_parens(stmt: str) -> set:
    m = re.search(r"\(([^)]*)\)", norm(stmt).split(" ON ", 1)[-1])
    return {unq(x.strip().split()[0]) for x in m.group(1).split(",") if x.strip()} if m else set()


def move_sql(old: str, new: str) -> str:
    """The SQL for a declared table rename: `RENAME TO` within a schema; `SET SCHEMA`, then `RENAME TO` if the
    name changes too, into another (CHG-XDW-001)."""
    os_, on = old.split(".", 1)
    ns, nn = new.split(".", 1)
    if os_ == ns:
        return f"ALTER TABLE {old} RENAME TO {nn}"
    sql = f"ALTER TABLE {old} SET SCHEMA {ns}"
    return sql + (f"; ALTER TABLE {ns}.{on} RENAME TO {nn}" if on != nn else "")


def _renamed_name(new_name: str, rc: dict, tables) -> str:
    """The name an index had before its column was renamed: the new name with each old column put back."""
    out = new_name
    for (t, nc), oc in rc.items():
        if t in tables:
            out = re.sub(r"(?<![a-z0-9])" + re.escape(nc) + r"(?![a-z0-9])", oc, out)
    return out


def diff(area: str, old: Model, new: Model, renames: dict | None = None, retired: dict | None = None) -> Plan:
    """`renames`: {"tables": {old: new}, "columns": {(table as named now, old column): new column}}, the
    declared renames (CHG-R6-010). Only a table that exists on the old side under its old name and on the new
    side under its new one is treated as renamed; likewise a column. `retired`: {table: {column}}, the columns the
    contracts withdraw (`x-ticvai-retired-columns`, CHG-MGN-001)."""
    p = Plan(area)
    recon_cols, recon_names, recon_fk, recon_drop = [], [], [], []   # (statement, rollback), in the order they run
    renames = renames or {}
    retired = retired or {}
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
    retired_objs: set = set()                        # (table, index or constraint) named in a retired column's row
    qual = [(re.compile(r"(?<![\w.])" + re.escape(o) + r"(?![\w])"), n) for n, o in rt.items()]

    def subst(st: str) -> str:
        for pat, n in qual:
            st = pat.sub(n, st)
        return st

    def review(kind, obj, change, todo):
        p.review.append((kind, obj, change, todo))

    def on_col(st: str, t: str, c: str) -> bool:
        """An old index or constraint statement on `t` whose columns include `c`."""
        cols = constraint_columns(st) if re.match(r"ALTER TABLE", st, re.I) else _cols_in_parens(st)
        return bool(cols) and c in cols and t in tables_named(st, known)

    def retired_row(t: str, c: str, was_table: str, write: bool) -> None:
        """A column the contract retires: a drop, worded with what goes with it (CR-157). `write`: the table exists
        under this name on the old side, so its NOT NULL is dropped in this forward migration."""
        objs = sorted((k[2] if k[0] == "constraint" else k[1].split(".", 1)[1]) for k, st in old.stmts.items()
                      if k[0] in ("constraint", "index") and on_col(st, was_table, c))
        retired_objs.update((was_table, o) for o in objs)
        coldef = (old.tables.get(was_table) or Table()).cols.get(c, "")
        has_nn = bool(re.search(r"\bNOT NULL\b", coldef, re.I) and not re.search(r"PRIMARY KEY", coldef, re.I))
        drop_nn = write and has_nn
        if drop_nn:
            p.statements.append(retire_not_null(t, c))
            p.rollback.append(f"ALTER TABLE {t} ALTER COLUMN {c} SET NOT NULL;")
            p.counts["other"] += 1
        review("column retired", f"{t}.{c}", "retired by the contract (x-ticvai-retired-columns): no code writes or "
               "reads it", "drop it, the four-step drop: "
               + ("this forward migration already drops its NOT NULL; " if drop_nn else
                  "after the rename, drop its NOT NULL; " if has_nn else "")
               + "stop every read, "
               + (f"drop {', '.join(objs)}, " if objs else "")
               + f"then ALTER TABLE {t} DROP COLUMN {c} in a later forward migration")

    def add_fk(k, t, name) -> bool:
        """A foreign key added since the old side: written guarded, NOT VALID (R8-MIG-001). Not for a table or a
        parent that is renamed, which still has its old name in the databases: those wait with the rename."""
        fk = parse_fk(new.stmts[k])
        partitioned = bool(fk) and "PARTITION BY" in ((new.tables.get(t) or Table()).tail or "").upper()
        g = guard_foreign_key(new.stmts[k], not_valid=not partitioned) if fk else None
        if g and t in old.tables and t not in rt and fk[3] not in rt and fk[3] in known:
            recon_fk.append((tag(t, "foreign key", name, g, fk[3]), f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name};"))
            p.recon_counts["keys"] += 1
            return True
        return False

    def on_renamed_col(t, cols) -> bool:
        return bool(cols) and any((t, c) in rc for c in cols)

    def same_but_name(new_name, old_def, new_def) -> bool:
        """The same definition under a new column name. An inline CHECK is named for its table and column
        (`<table>_<column>_chk`), so its name and the column inside it move with a rename and are not a change."""
        old_name = old_def.split(" ", 1)[0]
        was = re.sub(r"(?<![\w])" + re.escape(old_name) + r"(?![\w])", new_name, old_def)
        strip = lambda d: norm(re.sub(r"(?<![\w])CONSTRAINT \S+ ", "", d))
        return strip(was) == strip(new_def)

    def pure_rename(t, c) -> bool:
        """The renamed column `t.c` changes nothing but its name, so this file renames it (R8-MIG-001)."""
        oc = rc.get((t, c))
        if oc is None or t in rt:
            return False
        was, now = old.tables[t].cols[oc], new.tables[t].cols[c]
        return same_but_name(c, was, now) or same_but_name(c, was, relaxed(now))

    def all_pure(t, cols) -> bool:
        return all(pure_rename(t, c) for c in (cols or ()) if (t, c) in rc)

    for t in sorted(rt):
        o = rt[t]
        cr = sorted((oc, nc) for (tt, nc), oc in rc.items() if tt == t)
        review("table renamed", f"{o} -> {t}", "declared rename (derive-schema-history.py RENAMES)",
               move_sql(o, t)
               + "".join(f"; ALTER TABLE {t} RENAME COLUMN {oc} TO {nc}" for oc, nc in cr)
               + "; then rename its key, indexes, constraints and policies to the generated names and apply its "
                 "row-level security again (the \"after rename\" row for it)")

    restore, replaced_helpers = [], set()
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
                        if c in retired.get(t, ()) or c in retired.get(rt[t], ()):
                            retired_row(t, c, rt[t], write=False)
                            continue
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
                    if same or same_but_name(c, a.cols[oc], relaxed(d)):
                        # (a NOT NULL the new column adds is its own "not null" row, listed after this rename)
                        if not same:
                            review("not null", f"{t}.{c}", "renamed by the names file; the schema reference says NOT NULL",
                                   "backfill, then ALTER COLUMN ... SET NOT NULL")
                        # **A pure rename is written** (R8-MIG-001): no type, default or data question behind it.
                        recon_cols.append((tag(t, "rename column", f"{oc} to {c}", guard_rename_column(t, oc, c)), f"ALTER TABLE {t} RENAME COLUMN {c} TO {oc};"))
                        p.recon_counts["renames"] += 1
                        # an inline CHECK is named for its table and column: its name moves with the column
                        for on_, nn_ in zip(re.findall(r"CONSTRAINT (\S+) ", a.cols[oc]),
                                            re.findall(r"CONSTRAINT (\S+) ", d)):
                            if on_ != nn_:
                                recon_names.append((tag(t, "rename constraint", f"{on_} to {nn_}", guard_rename_constraint(t, on_, nn_)),
                                                    f"ALTER TABLE {t} RENAME CONSTRAINT {nn_} TO {on_};"))
                        continue
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
                        fill = scope_path_backfill(t, b.cols, was_tenant_root(old, t))
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
                    fill = scope_path_backfill(t, b.cols, was_tenant_root(old, t)) if c == "scope_path" else None
                    if a.cols[c] == relaxed(d) and fill:
                        # **A scope_path an earlier forward migration added keeps its named backfill** (MOD audit,
                        # 14 October 2026, CHG-MOD-007). Once that migration is in the old side, the column is "still
                        # nullable", and this row used to drop the backfill CHG-R6G-002 names, so
                        # check-ddl-conventions D-SCOPE-NOTNULL failed on the next derive (region_settings,
                        # upsell_rule) for a column nobody had changed.
                        review("not null", f"{t}.{c}", "still nullable in the databases; the schema reference says "
                               "NOT NULL, and row-level security reads it",
                               f"in a forward migration, backfill first, then the NOT NULL: {fill}")
                    elif a.cols[c] == relaxed(d):
                        review("not null", f"{t}.{c}", "still nullable in the databases; the schema reference "
                               "says NOT NULL", "backfill, then ALTER COLUMN ... SET NOT NULL")
                    elif widened_check(a.cols[c], d):
                        # **A column CHECK that only gained values is written** (CHG-R8MIG-006: an enum value the
                        # contract adds, TenantDomain.channel staffApp): dropped and added again NOT VALID, then
                        # VALIDATE, as a new table CHECK is; apply_forward folds it into the column, so once.
                        name, clause = widened_check(a.cols[c], d)
                        p.statements += [f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name}",
                                         f"ALTER TABLE {t} ADD {clause} NOT VALID",
                                         f"ALTER TABLE {t} VALIDATE CONSTRAINT {name}"]
                        old_clause = _inline_check(a.cols[c])[1]
                        p.rollback.append(f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name}; "
                                          f"ALTER TABLE {t} ADD {old_clause} NOT VALID;")
                        p.counts["other"] += 1
                    elif changed_check_only(a.cols[c], d):
                        # **A column CHECK added or narrowed is written NOT VALID** (CHG-R8MIG-011; the storage-sat
                        # lane's request 3: marketing.customer_badge.source_type and status became enums). It binds
                        # every new write at once; the rows already there are the migration owner's to check, so
                        # VALIDATE is a review row, not a statement that could fail the migration.
                        name, clause = changed_check_only(a.cols[c], d)
                        p.statements += [f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name}",
                                         f"ALTER TABLE {t} ADD {clause} NOT VALID"]
                        old_ic = _inline_check(a.cols[c])
                        p.rollback.append(f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name};"
                                          + (f" ALTER TABLE {t} ADD {old_ic[1]} NOT VALID;" if old_ic else ""))
                        p.counts["other"] += 1
                        review("constraint not validated", f"{t} {name}", f"`{clause}`, added NOT VALID",
                               f"check the rows, then ALTER TABLE {t} VALIDATE CONSTRAINT {name}")
                    elif only_not_null_dropped(a.cols[c], d):
                        # **A column the contract makes optional loses its NOT NULL here** (CHG-R8MIG-004, R8 blockers
                        # APPROVALS-TENANCY-C09, ORDERS-MONEY-C35, IDENTITY-C12): relaxing NOT NULL touches no row and
                        # no reader, so it is additive. Guarded like a retired column's, and folded back the same way
                        # (RETIRE_GUARD), so the next run writes nothing.
                        p.statements.append(retire_not_null(t, c))
                        p.rollback.append(f"ALTER TABLE {t} ALTER COLUMN {c} SET NOT NULL;")
                        p.counts["other"] += 1
                    else:
                        review("column changed", f"{t}.{c}", f"`{a.cols[c]}` -> `{d}`",
                               "type, default, nullability or check changed: write the ALTER COLUMN (and any "
                               "data rewrite) by hand")
            for c in a.cols:
                if c not in b.cols and (t, c) not in old_renamed:
                    if c in retired.get(t, ()):
                        retired_row(t, c, t, write=True)
                        continue
                    review("column dropped", f"{t}.{c}", "no longer in the schema reference",
                           "a rename or a drop: decide, then RENAME COLUMN or the four-step drop by hand")
            old_names = {re.match(r"CONSTRAINT (\S+) ", x).group(1) for x in a.constraints
                         if re.match(r"CONSTRAINT (\S+) ", x)}
            for c in sorted(b.constraints - a.constraints):
                chk = re.match(r"CONSTRAINT (\S+) CHECK\b", c, re.I)
                if chk and chk.group(1) not in old_names:
                    # **A new table CHECK is written** (CHG-MGN-001, ADAM CR-156): NOT VALID, so adding it takes no
                    # long lock, then VALIDATE, which fails the migration's transaction if a row breaks it (the
                    # person's signal, as CHG-GEN-006's case-insensitive index). One of the same name a person added by
                    # hand is dropped first, so the statements apply either way. A CHECK naming a renamed column waits
                    # for the RENAME COLUMN, whole.
                    name = chk.group(1)
                    named = set(re.findall(r"\b(\w+)\b", c)) & set(b.cols)
                    add = f"ALTER TABLE {t} ADD {c} NOT VALID"
                    if any((t, x) in rc for x in named):
                        review("constraint after rename", f"{t} {name}", f"`{c}`",
                               f"names a renamed column: after the RENAME COLUMN, {add}; ALTER TABLE {t} VALIDATE "
                               f"CONSTRAINT {name}")
                        continue
                    p.statements += [f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name}", add,
                                     f"ALTER TABLE {t} VALIDATE CONSTRAINT {name}"]
                    p.rollback.append(f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name};")
                    p.counts["other"] += 1
                    continue
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
                # **Only an index that replaces an old one is renamed** (CHG-MGN-001, ADAM CR-156): one whose columns,
                # under their old names, an old index on the table already covers. A new one (sale_board_tile's unique
                # page and position) has nothing to rename: it is created after the RENAME COLUMN, and listed whole.
                was = [{rc.get((t, c), c) for c in _cols_in_parens(stmt)} for t in on]
                replaces = any(ok[0] == "index" and ok not in new.stmts and _cols_in_parens(ost) in was
                               and on & tables_named(ost, known) for ok, ost in old.stmts.items())
                if replaces:
                    sch = k[1].split(".", 1)[0]
                    new_name = k[1].split(".", 1)[1]
                    cands = [ok for ok, ost in old.stmts.items()
                             if ok[0] == "index" and ok not in new.stmts and _cols_in_parens(ost) in was
                             and on & tables_named(ost, known) and ok[1].split(".", 1)[0] == sch]
                    if len(cands) > 1:
                        exact = [ok for ok in cands if ok[1].split(".", 1)[1] == _renamed_name(new_name, rc, on)]
                        cands = exact or cands
                    if len(cands) == 1 and all(all_pure(t, _cols_in_parens(stmt)) for t in on):
                        old_name = cands[0][1].split(".", 1)[1]
                        tt = sorted(on)[0]
                        recon_names.append((tag(tt, "rename index", f"{old_name} to {new_name}", guard_rename_index(tt, old_name, new_name)),
                                            f"ALTER INDEX {sch}.{new_name} RENAME TO {old_name};"))
                        p.recon_counts["indexes"] += 1
                        continue
                    review("index after rename", k[1], f"`{new.stmts[k]}`",
                           "names a renamed column: rename the old index to this name (ALTER INDEX ... RENAME TO) "
                           "after the RENAME COLUMN")
                elif all(all_pure(t, _cols_in_parens(stmt)) for t in on) and len(on) == 1:
                    tt = next(iter(on))
                    recon_names.append((tag(tt, "create index", k[1].split(".", 1)[1], guard_create_index(tt, new.stmts[k], _cols_in_parens(stmt))),
                                        f"DROP INDEX IF EXISTS {k[1]};"))
                    p.recon_counts["indexes"] += 1
                else:
                    review("index added after rename", k[1], "a new index on a renamed column",
                           f"after the RENAME COLUMN, create it: {new.stmts[k]}")
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
                back = {nc: oc for (tt, nc), oc in rc.items() if tt == t}
                nf = parse_fk(new.stmts[k])
                cands = []
                for ok, ost in old.stmts.items():
                    if ok[0] != "constraint" or ok[1] != t or ok in new.stmts or not nf:
                        continue
                    of = parse_fk(ost)
                    if of and {back.get(c, c) for c in nf[2]} == set(of[2]) and (of[3] == nf[3] or rt.get(nf[3]) == of[3]):
                        cands.append(ok[2])
                if len(cands) == 1 and cands[0] != name and all_pure(t, cols):
                    recon_names.append((tag(t, "rename constraint", f"{cands[0]} to {name}", guard_rename_constraint(t, cands[0], name)),
                                        f"ALTER TABLE {t} RENAME CONSTRAINT {name} TO {cands[0]};"))
                    p.recon_counts["keys"] += 1
                    continue
                if not cands and k not in old.stmts and all_pure(t, cols) and add_fk(k, t, name):
                    continue   # a key that is new, on a column renamed in this file: added after the rename
                review("constraint after rename", f"{t} {name}", f"`{new.stmts[k]}`",
                       "names a renamed column: rename the old constraint to this name (ALTER TABLE ... RENAME "
                       "CONSTRAINT) after the RENAME COLUMN")
                continue
            if k in old.stmts and subst(old.stmts[k]) == new.stmts[k]:
                continue   # a key to a renamed table: Postgres follows the rename
            if k not in old.stmts and (t in new_tables or (cols and cols <= new_cols.get(t, set()))):
                # **Guarded, so the file applies twice** (CHG-R8MIG-010, the storage-sat lane's request): every other
                # statement of the file is IF [NOT] EXISTS, and ADD CONSTRAINT has no such form, so a second run
                # stopped at the first key. Checked, not NOT VALID: the column is new, so no row can break it.
                p.statements.append(guard_add_constraint(t, name, stmt) if parse_fk(stmt) else stmt)
                if t not in new_tables:
                    p.rollback.append(f"ALTER TABLE {t} DROP CONSTRAINT IF EXISTS {name};")
                p.counts["other"] += 1
            elif k not in old.stmts:
                if add_fk(k, t, name):
                    continue
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
            elif REPLACEABLE.match(k[1]):
                p.statements.append(stmt)
                restore.append(old.stmts[k])
                p.counts["other"] += 1
                name = REPLACEABLE.match(k[1]).group(1).lower()
                if name.startswith("apply_"):
                    replaced_helpers.add(name)
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
            rc_ = rls_call(s)
            for t in refs & set(rt):
                # **Whole, never cut** (CHG-MGN-001, ADAM CR-148): `s[:70]` cut 19 of the 26 policy calls in these rows
                # before their key or parent, so the person could not tell which parent the table follows.
                follows[t].append(s)
            fk = re.match(r"^SELECT platform\.\w+\('[^']+'::regclass,\s*'([^']+)'", s)
            if rc_ and rc_[0] in ACROSS_HELPERS and rc_[1] in rt and fk \
                    and fk.group(1) in old.tables[rt[rc_[1]]].cols:
                # **A renamed table whose parent is now across deployables gets its policy now** (CHG-RSF-001, fix
                # round 1): sync.dsar_request is still platform.dsar_request in the databases; its policy is applied
                # under that name, and the person's SET SCHEMA moves it with the table.
                was_name = rt[rc_[1]]
                now = stmt.replace(f"'{rc_[2]}'::regclass", f"'{was_name}'::regclass", 1)
                was = [old.stmts[k2] for k2 in old.stmts if k2[0] == "stmt"
                       and (rls_call(old.stmts[k2]) or ("", "", ""))[1] == was_name
                       and rls_call(old.stmts[k2])[0] != "drop_rls_policies"]
                if norm(now) not in was:
                    p.statements.append(f"SELECT platform.drop_rls_policies('{was_name}'::regclass)")
                    p.statements.append(now)
                    p.rollback.append(f"SELECT platform.drop_rls_policies('{was_name}'::regclass); "
                                      + " ".join(w.rstrip(";") + ";" for w in was))
                    p.counts["policies"] = p.counts.get("policies", 0) + 1
            continue
        if refs and refs <= new_tables:
            p.statements.append(stmt)
            p.counts["other"] += 1
            continue
        rc_ = rls_call(s)
        if rc_ and rc_[0] != "drop_rls_policies" and rc_[1] in new_tables:
            # **A new table's policy is written with the table** (CHG-STO-003, 14 October 2026). A parent policy names
            # its parent too (`apply_parent_rls(child, 'outlet_id', 'platform.outlet', 'id')`), so the "every table it
            # names is new" rule above missed it: `platform.outlet_opening_hour` was created by V0104 with no policy at
            # all, listed as "statement added" for a person, and the next run wrote the policy into a V0105 because by
            # then the table existed. A forward migration that grows on a second run is not one migration.
            p.statements.append(stmt)
            p.counts["other"] += 1
            continue
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
            review("statement added", ", ".join(sorted(refs)) or "(database)", f"`{s}`",
                   "touches objects that already exist: write it into a forward migration by hand")

    # Every table a replaced helper applied its policy to gets it again (CHG-RSF-001), once, after the helpers.
    if replaced_helpers:
        done = {c[1] for c in (rls_call(s) for s in p.statements) if c and c[0] != "drop_rls_policies"}
        for k, stmt in new.order:
            c = rls_call(stmt) if k[0] == "stmt" else None
            if not c or c[0] not in replaced_helpers or c[1] not in old.tables or c[1] in done:
                continue
            p.statements.append(f"SELECT platform.drop_rls_policies('{c[2]}'::regclass)")
            p.statements.append(stmt)
            p.rollback.append(f"SELECT platform.drop_rls_policies('{c[2]}'::regclass); {norm(stmt).rstrip(';')};")
            p.counts["policies"] = p.counts.get("policies", 0) + 1
            done.add(c[1])
    # The old helpers come back first when the rollback runs (it runs in reverse), then each policy is applied again.
    p.rollback += [r.rstrip().rstrip(";") + ";" for r in restore]

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
        if old_call and any(o == old_call[1] and n in reapplied for n, o in rt.items()):
            continue   # a renamed table's policy: the "after rename" row applies it again (CHG-RSF-001)
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
        if kind in ("index", "constraint") and any(
                (k[2] if kind == "constraint" else k[1].split(".", 1)[1]) == o and rt_t in tables_named(old.stmts[k], known)
                for rt_t, o in retired_objs):
            continue   # named in its retired column's row (CHG-MGN-001)
        if kind == "table":
            review("table dropped", k[1], "no longer in the schema reference",
                   "a rename or a drop: decide, then ALTER TABLE ... RENAME or DROP TABLE by hand")
        elif kind in ("index",):
            if not any(k[1].split(".", 1)[1].startswith(t.split(".", 1)[1] + "_") for t in removed_tables):
                on_ = tables_named(old.stmts[k], known)
                if on_ and not (on_ & renamed_away) and not (on_ & removed_tables):
                    # **An index the schema reference no longer asks for is dropped** (R8-MIG-001): it is an index on
                    # a column that is not a foreign key any more. Guarded, and the rollback creates it again.
                    recon_drop.append((tag(sorted(on_)[0], "drop index", k[1].split(".", 1)[1], guard_drop_index(k[1])), old.stmts[k].rstrip().rstrip(";") + ";"))
                    p.recon_counts["indexes"] += 1
                    continue
                review("index dropped", k[1], "no longer generated", "DROP INDEX by hand if intended")
        elif kind == "constraint":
            fk_ = parse_fk(old.stmts[k])
            nt_ = new.tables.get(k[1])
            if (fk_ and k[1] not in removed_tables and k[1] not in renamed_away and nt_ is not None
                    and all(c_ in nt_.cols for c_ in fk_[2])):
                # **A foreign key the contract withdraws is dropped** (CHG-R8MIG-006, R8 blocker IDENTITY-C20:
                # `x-ticvai-references: none` on PlatformStaffGrant.operatorPrincipalId). Its column stays; dropping a
                # key refuses no write. Guarded, and the rollback adds it again.
                recon_drop.append((tag(k[1], "drop foreign key", k[2], guard_drop_constraint(k[1], k[2]), fk_[3]),
                                   old.stmts[k].rstrip().rstrip(";") + " NOT VALID;"))
                p.recon_counts["keys"] += 1
                continue
            if k[1] not in removed_tables:
                review("constraint dropped", f"{k[1]} {k[2]}", "no longer generated",
                       "ALTER TABLE ... DROP CONSTRAINT by hand if intended")
        elif kind == "function":
            review("function dropped", k[1], "no longer generated", "DROP FUNCTION by hand if intended")
        else:
            refs = tables_named(old.stmts[k], known)
            if not (refs and refs <= removed_tables):
                review("statement dropped", ", ".join(sorted(refs)) or "(database)", f"`{old.stmts[k]}`",
                       "undo it by hand if intended")
    # Renames first (a key or an index below names the new column), then the keys, then the drops.
    for stmt_, back_ in recon_cols + recon_names + recon_fk + recon_drop:
        p.recon.append(stmt_)
        p.recon_rollback.append(back_)
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


def split_early(p: Plan, frozen: dict) -> tuple:
    """(early, rest): the renames a frozen forward file already depends on, and everything else (R8-MIG-001).
    `frozen` = {file name: text} of the forward files written before the names file. V0104 calls
    `apply_parent_rls('t'::regclass, 'new_name', ...)` for four columns that exist under their old names until renamed,
    so on a fresh database V0104 stops unless the rename comes first. A rename is *early* when a frozen file names
    `'<table>'::regclass, '<new column>'`. Returns the first frozen file that needs one (or None) as well."""
    early, rest, first = ([], []), ([], []), None
    for stmt, back in zip(p.recon, p.recon_rollback):
        m = re.match(r"-- (\S+) \| rename column \| (\S+) to (\S+)\n", stmt)
        need = None
        if m:
            pat = f"'{m.group(1)}'::regclass, '{m.group(3)}'"
            need = next((n for n, txt in sorted(frozen.items()) if pat in txt), None)
        tgt = early if need else rest
        tgt[0].append(stmt)
        tgt[1].append(back)
        if need and (first is None or need < first):
            first = need
    return early, rest, first


def early_version(first: str, taken: set) -> str:
    """The version of the file that runs just before the frozen file `first` (R8-MIG-001, CHG-R8MIG-003): the number
    before it and the first letter not taken, `V0103a` for `V0104__...`. By name (SqlMigrationRunner sorts ordinal)
    `V0103__` < `V0103a__` < `V0104__`, since `_` sorts before every lower-case letter. A longer number does not do it:
    V01035 sorts before V0103 (`5` < `_`), reads as 1035, the plan's V1035__fnb.sql, and no check reads five digits."""
    n = int(re.match(r"V(\d+)", first).group(1)) - 1
    for letter in "abcdefghijklmnopqrstuvwxyz":
        if f"V{n:04d}{letter}" not in taken:
            return f"V{n:04d}{letter}"
    raise ValueError(f"no free letter after V{n:04d}")


def render_recon(p: Plan, version: str, baseline: str, stamp: str, before: str = "", rest: str = "") -> str:
    """The second forward file for one database: the renames, keys and dropped indexes (R8-MIG-001). With `before`,
    the early file: the renames the frozen file `before` names by their new names, the rest in `rest`."""
    import hashlib as _h
    body = "\n\n".join(x.rstrip().rstrip(";") + ";" for x in p.recon)
    checksum = _h.sha256(body.encode("utf-8")).hexdigest()
    c = p.recon_counts
    what = (f"{c['renames']} column rename(s), {c['keys']} key(s) added, renamed or dropped, {c['indexes']} index(es) "
            "renamed or dropped")
    desc = f"after {baseline}, names the contracts use: {what}"
    lines = [
        f"-- {version} -- {p.area} database, after {baseline} ({stamp}): the names the contracts use.",
        "-- **Written by tools/derive-ddl.py in frozen mode. Do not edit after merge; a mistake is a new migration.**",
        "--",
        f"-- The baseline under backend/{p.area}/ is frozen at {baseline}, but the schema reference has renamed columns,",
        "-- added foreign keys and stopped generating some indexes since. Migrations written from the baseline DDL",
        "-- create the old names; this file brings a database built from them to the names the contracts use.",
        "-- Every statement is a guarded block: it does nothing when its table, key or index is not there yet, or is",
        "-- there already under the new name, so the file can be applied twice and in any database. A table created",
        "-- by a migration that runs after this one copies the blocks that name it (ticket text: 'Changes this file",
        "-- makes to your tables'). A foreign key is added NOT VALID: it checks every new write, and the owner runs",
        "-- ALTER TABLE ... VALIDATE CONSTRAINT when the rows already there are known to be clean.",
        f"-- {what}.",
    ] + ([
        "--",
        f"-- **This file runs before {before}**, which applies row-level security on these columns by their new",
        f"-- names: without it a database built from the files in name order stops at {before}. The other renames,",
        f"-- with the keys and indexes that follow them, are in {rest}; its blocks for these columns find them renamed",
        "-- and do nothing.",
    ] if before else []) + [
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
    ] + [f"-- {r}" for r in reversed(p.recon_rollback)] + [
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
