#!/usr/bin/env python3
"""
Structural checks on migration DDL.

This is not a SQL parser. Postgres will find syntax errors; a parser that
half-understands ltree, RLS and partitioning would only give false confidence.
What this checks is the conventions a parser cannot know:

  * every table that carries scope_path OR venue_id has RLS, FORCE and a policy
  * every partitioned table has a default partition
  * every migration registers itself in platform.schema_version
  * every migration has a ROLLBACK section
  * every referenced schema exists by the time it is used
  * money columns are numeric(18,4) and carry currency and scale
  * ULID columns are char(26)
  * no DROP or destructive ALTER outside a rollback block

Run: python3 tools/check-migrations.py
"""
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "src/Ticvai.Migrations/Scripts"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(f: str, msg: str) -> None:
    ERRORS.append(f"{f}: {msg}")


def warn(f: str, msg: str) -> None:
    WARNINGS.append(f"{f}: {msg}")


def split_rollback(sql: str) -> tuple[str, str]:
    """Body and rollback. The marker is the banner, not any mention of the word."""
    # Banner then ROLLBACK. Explanatory prose may follow before the closing rule.
    marker = re.search(r"^-- =+\n-- ROLLBACK\b", sql, re.M)
    if not marker:
        return sql, ""
    return sql[: marker.start()], sql[marker.start():]


def strip_comments(sql: str) -> str:
    """Remove -- line comments only.

    An earlier version also blanked string literals with
    `'(?:[^']|'')*'` under re.S. That regex spans from one apostrophe to the
    next across statement boundaries — on V0002 it removed 69% of the file and
    the checker happily reported PASS on the fragment that survived, missing a
    table with no RLS. Line comments are safe to strip because they are
    line-anchored; literals are not, so they stay.
    """
    stripped = re.sub(r"^\s*--.*$", "", sql, flags=re.M)
    # Guard against exactly the failure above: stripping should remove comments,
    # not most of the file.
    if len(stripped) < len(sql) * 0.25:
        raise RuntimeError(
            f"comment stripping removed {100 - 100*len(stripped)//len(sql)}% of the source — "
            "the checker would be validating a fragment"
        )
    return stripped


def check_file(path: Path, known_schemas: set[str]) -> set[str]:
    name = path.name
    raw = path.read_text()
    body, rollback = split_rollback(raw)
    code = strip_comments(body)

    # --- version registration -------------------------------------------------
    version = name.split("__")[0]
    if f"'{version}'" not in body or "platform.schema_version" not in body:
        fail(name, f"does not register {version} in platform.schema_version")

    # --- rollback -------------------------------------------------------------
    if not rollback:
        fail(name, "no ROLLBACK section")
    else:
        created = set(re.findall(r"CREATE TABLE (?:IF NOT EXISTS )?([\w.]+)", code))
        for t in created:
            if f"DROP TABLE IF EXISTS {t}" not in rollback:
                fail(name, f"ROLLBACK does not drop {t}")
        if version not in rollback:
            warn(name, "ROLLBACK does not remove its schema_version row")

    # --- destructive statements outside rollback ------------------------------
    for stmt in re.findall(r"^\s*(DROP TABLE|DROP SCHEMA|TRUNCATE)\b", code, re.M):
        fail(name, f"destructive statement in migration body: {stmt}")
    for col in re.findall(r"ALTER TABLE [\w.]+\s+DROP COLUMN", code):
        fail(name, "DROP COLUMN in body — use the additive four-step instead")

    # --- schemas used exist ---------------------------------------------------
    declared = set(re.findall(r"CREATE SCHEMA (?:IF NOT EXISTS )?(\w+)", code))
    known = known_schemas | declared
    for qualified in re.findall(r"CREATE TABLE (?:IF NOT EXISTS )?(\w+)\.", code):
        if qualified not in known:
            fail(name, f"table created in undeclared schema '{qualified}'")

    # --- per-table conventions ------------------------------------------------
    # Split on CREATE TABLE so each block is examined against its own DDL.
    blocks = re.split(r"(?=CREATE TABLE )", code)
    for block in blocks:
        m = re.match(r"CREATE TABLE (?:IF NOT EXISTS )?([\w.]+)", block)
        if not m:
            continue
        table = m.group(1)
        # the column list is the first balanced paren group
        head = block[: block.find(";") + 1] if ";" in block else block

        is_partitioned = "PARTITION BY" in head
        # RLS is required on anything tenant-scoped. Checking only scope_path missed 41
        # tables that carry venue_id instead — they would have passed with no policy at all,
        # which is the same class of hole as a checker validating a truncated file.
        has_scope_path = re.search(r"^\s+scope_path\s", head, re.M) is not None
        has_venue_id = re.search(r"^\s+venue_id\s", head, re.M) is not None
        needs_rls = has_scope_path or has_venue_id

        if needs_rls:
            why = "scope_path" if has_scope_path else "venue_id"
            if f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY" not in code:
                fail(name, f"{table} has {why} but no ENABLE ROW LEVEL SECURITY")
            if f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY" not in code:
                fail(name, f"{table} has {why} but no FORCE ROW LEVEL SECURITY")
            if not re.search(rf"CREATE POLICY \w+ ON {re.escape(table)}", code):
                fail(name, f"{table} has {why} but no policy")

        if is_partitioned:
            if not re.search(rf"PARTITION OF {re.escape(table)} DEFAULT", code):
                fail(name, f"{table} is partitioned but has no DEFAULT partition")
            if "PRIMARY KEY (" in head and "venue_id" not in head.split("PRIMARY KEY (")[1].split(")")[0]:
                fail(name, f"{table} partitions by venue_id but venue_id is not in the primary key")

        # money columns
        for col in re.findall(r"^\s+(\w*(?:amount|price|cost|total|balance)\w*)\s+([\w()., ]+)", head, re.M | re.I):
            cname, ctype = col[0], col[1].strip()
            if ctype.startswith("numeric") and "numeric(18,4)" not in ctype:
                fail(name, f"{table}.{cname} is {ctype}, expected numeric(18,4)")
        if re.search(r"numeric\(18,4\)", head):
            if "currency_code" not in head and "currency" not in head:
                warn(name, f"{table} has money columns but no currency column")

        # ULID keys
        for col in re.findall(r"^\s+(id|\w+_id)\s+(char\(\d+\)|uuid|text)", head, re.M):
            cname, ctype = col
            if ctype.startswith("char(") and ctype != "char(26)":
                fail(name, f"{table}.{cname} is {ctype} — ULIDs are char(26)")

    return known


def main() -> int:
    files = sorted(SCRIPTS.glob("V*.sql"))
    if not files:
        print("no migrations found", file=sys.stderr)
        return 1

    known: set[str] = set()
    print(f"checking {len(files)} migration(s) in {SCRIPTS}\n")
    for f in files:
        known = check_file(f, known)
        tables = len(re.findall(r"CREATE TABLE ", f.read_text()))
        print(f"  {f.name:28} {tables:>3} tables")

    print()
    for w in WARNINGS:
        print(f"  WARN  {w}")
    for e in ERRORS:
        print(f"  FAIL  {e}")

    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
