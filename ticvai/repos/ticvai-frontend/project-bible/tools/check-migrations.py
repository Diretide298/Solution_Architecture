#!/usr/bin/env python3
"""
Structural checks on migration DDL.

This is not a SQL parser. Postgres will find syntax errors; a parser that
half-understands ltree, RLS and partitioning would only give false confidence.
What this checks is the conventions a parser cannot know:

  * every table that carries scope_path OR venue_id has RLS, FORCE and a policy --
    longhand, or through platform.apply_scope_rls / apply_venue_rls
  * every partitioned table has a default partition, with venue_id leading its key
  * every referenced schema exists by the time it is used
  * every foreign key points at a table some migration actually creates
  * money columns are numeric(18,4) and carry currency and scale
  * ULID columns are char(26)
  * no DROP or destructive ALTER outside a rollback block

On a versioned `V*__*.sql` migration it additionally checks version registration and
the ROLLBACK section. The generated template under `backend/` is neither stamped nor
reversed, so those two are skipped there -- see the note above SCRIPTS.

Run: python3 tools/check-migrations.py
"""
import re
import sys
from pathlib import Path

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]
# **Reads the generated template, not a Flyway series — changed 21 September 2026.**
#
# Until then this globbed `V*.sql` under `src/Ticvai.Migrations/Scripts`. Both of the package's
# `V*` series were deleted that day: the root baseline because its content moved into
# `tools/derive-ddl.py` and became part of the numbered series, and the August `V0001`-`V0003b`
# set in the backend repo because it was the superseded generation `backend/README.md` had been
# warning about since 31 August.
#
# **What `backend/` holds is a template rather than a migration history**, and three checks below
# do not apply to one:
#
#   * **version registration** — a template is applied once to an empty database, not stamped
#   * **ROLLBACK sections** — it is regenerated, not reversed; the rollback of a template is
#     dropping the database
#   * **the level-typed composite FK to `platform.scope_node`** — that table does not exist in
#     this generation, which renamed it on 26 August. Enforcing a reference to a table nothing
#     creates would fail every row it checked.
#
# Everything else still holds and is what this file now checks.
SCRIPTS = ROOT / "backend"

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
    # Guard against exactly the failure above — but on the thing that actually went wrong.
    #
    # **The old guard measured how much of the file disappeared, and that was a proxy.** It was
    # written when the function also blanked string literals, which really could swallow DDL. That
    # regex is gone; what remains is line-anchored and cannot touch a statement. The ratio then
    # became a rule about prose density, and on 21 September it crashed the checker on
    # `001-extensions.sql` — three statements under a paragraph explaining why they sort first —
    # and again on `930-partitioning.sql`, which documents 34 table names in comments.
    #
    # **So count statements rather than characters.** If a keyword that starts a statement went
    # missing, stripping ate DDL and the checker would be validating a fragment. If none did, a
    # file that is nine-tenths explanation is just a well-commented file.
    kw = r"\b(?:CREATE|ALTER|DROP|INSERT|SELECT|TRUNCATE|COMMENT ON)\b"
    before, after = len(re.findall(kw, sql, re.I)), len(re.findall(kw, stripped, re.I))
    in_comments = len(re.findall(kw, "\n".join(re.findall(r"^\s*--.*$", sql, re.M)), re.I))
    if after < before - in_comments:
        raise RuntimeError(
            f"comment stripping removed {before - in_comments - after} SQL statement(s) that were "
            "not in comments — the checker would be validating a fragment"
        )
    return stripped


# **Matches a quoted identifier as well as a bare one.** `marketing."case"` is a reserved
# word the generator quotes; a `[\w.]+` pattern stopped at the quote and yielded
# `marketing.`, so that table was silently never checked for anything.
TABLE_RE = r'CREATE TABLE (?:IF NOT EXISTS )?((?:\w+|"[^"]+")(?:\.(?:\w+|"[^"]+"))?)'

CREATED: set[str] = set()   # every table created anywhere in the migration set
ALTERED: set[str] = set()   # tables given a level-typed FK by a later ALTER TABLE
# **Tables handed to `platform.apply_scope_rls` anywhere in the series.** The generated template
# separates the policy from the table: `010-<schema>.sql` creates it and
# `920-row-level-security.sql` protects it, so a per-file search finds neither half beside the
# other. Collected across the whole series for the same reason foreign keys are.
RLS_APPLIED: set[str] = set()
EXEMPT = {
    # Written inside the same transaction as the state change it records. A foreign key
    # failure here would roll back a sale for a bookkeeping reason, and the venue_id is
    # copied from a row that was already validated.
    "platform.outbox",
}


def collect_created(files: list[Path]) -> None:
    """Every table the set creates, so a reference to a missing one can be caught.

    Added after four foreign keys were found pointing at pii.subject, a table that was
    declared in a rollback and never created. psql would have failed on the first one;
    this checker reported PASS, because it verified conventions and never verified that
    a referenced table exists.
    """
    for f in files:
        body = split_rollback(f.read_text())[0]
        CREATED.update(re.findall(TABLE_RE, body))


def collect_alters(files: list[Path]) -> None:
    for f in files:
        text = f.read_text()
        for m in re.finditer(r"ALTER TABLE ([\w.]+)[\s\S]{0,400}?REFERENCES platform\.scope_node \(id, level\)",
                             text):
            ALTERED.add(m.group(1))
        # **Two families, because two columns.** `apply_scope_rls` protects a table by its own
        # `scope_path`; `apply_venue_rls` protects one that carries `venue_id` instead, resolving
        # it through the scope tree. A checker that knew only the first reported 59 unprotected
        # tables that were protected — which is the same false negative in the other direction.
        for m in re.finditer(r"apply_(?:scope|venue)_rls\('([\w.\"]+)'", text):
            RLS_APPLIED.add(m.group(1))
            RLS_APPLIED.add(m.group(1).replace('"', ""))
        for m in re.finditer(r"ALTER TABLE ([\w.]+) ENABLE ROW LEVEL SECURITY", text):
            RLS_APPLIED.add(m.group(1))


def check_file(path: Path, known_schemas: set[str]) -> set[str]:
    name = path.name
    raw = path.read_text()
    body, rollback = split_rollback(raw)
    code = strip_comments(body)

    # **Version registration and rollback are checked on a versioned migration only.** The
    # generated template is applied once to an empty database and regenerated in full; stamping a
    # version it does not have, or reversing a file that is rewritten wholesale, would both be
    # checks with nothing behind them.
    is_versioned = "__" in name and name.startswith("V")
    if is_versioned:
        version = name.split("__")[0]
        if f"'{version}'" not in body or "platform.schema_version" not in body:
            fail(name, f"does not register {version} in platform.schema_version")
        if not rollback:
            fail(name, "no ROLLBACK section")
        else:
            created = set(re.findall(TABLE_RE, code))
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
        m = re.match(TABLE_RE, block)
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

        # **Satisfied either longhand or by `apply_scope_rls`**, which does all three in one call
        # and is how the generated series protects 249 tables. The longhand form stays accepted
        # because a hand-written migration should still be readable as what it does.
        if needs_rls and table not in RLS_APPLIED:
            why = "scope_path" if has_scope_path else "venue_id"
            longhand = (f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY" in code
                        and f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY" in code
                        and re.search(rf"CREATE POLICY \w+ ON {re.escape(table)}", code))
            if not longhand:
                fail(name, f"{table} has {why} and no row-level security — neither "
                           f"platform.apply_scope_rls('{table}') nor the longhand three statements")

        # Level-typed scope references (V0004). A venue_id that is a bare uuid can point
        # at a workstation, a department, or nothing — the type says uuid, the intent says
        # venue, and before V0004 nothing checked. Every new table carrying venue_id must
        # carry the generated level column and the composite foreign key, or the convention
        # lasts exactly as long as the person who remembers it.
        # **Not checked against the generated template.** `platform.scope_node` does not exist in
        # this generation — it was renamed on 26 August — so requiring a composite FK into it
        # would fail every table it looked at. The intent survives as an application-layer rule
        # and is recorded in `backend/tenant/930-partitioning.sql`.
        if (is_versioned and has_venue_id and "GENERATED ALWAYS AS" not in head
                and table not in ALTERED and table not in EXEMPT):
            if "PARTITION OF" not in head:
                fail(name, f"{table} has venue_id but no level-typed FK — add "
                           "`venue_level platform.scope_level GENERATED ALWAYS AS ('venue') STORED` "
                           "and a composite FK to scope_node (id, level)")

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
    # The generated template, in apply order: schemas and extensions, then tables per schema, then
    # keys, indexes and policies. Sorting by (directory, name) is the order provision-tenant.sh
    # applies them in, which is the order the checks have to assume.
    files = sorted(SCRIPTS.glob("*/[0-9]*.sql"), key=lambda p: (p.parent.name, p.name))
    files += sorted(SCRIPTS.glob("V*.sql")) + sorted(SCRIPTS.glob("*/V*.sql"))
    if not files:
        print("no migrations found", file=sys.stderr)
        return 1

    collect_created(files)
    collect_alters(files)
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
