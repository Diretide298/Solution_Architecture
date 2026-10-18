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
    "D-STUB-TABLE": "a table holding only keys (R087); one the lineage writes cannot be baselined (CHG-GEN-003, CR-078 CR-080)",
    "D-DOUBLE-KEY": "a second key to one parent for one concept, or a key named for a renamed table (R102 R160)",
    "D-DESC-CUT": "a column description that is a cut-off prefix of its contract field's (R019)",
    "D-HEADER-COUNT": "a DDL header's table count disagrees with the file (R170 R043)",
    "D-MIG-TABLES": "MIGRATIONS.md, the MIG tickets and the DDL disagree on a migration's tables (R049 R063)",
    "D-MIG-ORDER": "a MIG ticket Follows a migration that MIGRATIONS.md orders after it (R051 R056)",
    "D-NAMING": "a boolean not read as an assertion, or an index/FK name off naming-and-style 6.1 (R093 R119)",
    "D-FK-TARGET-NAME": "a declared key whose column names a different table than it references (R082)",
    "D-JSONB-TWIN": "a jsonb column and a child table holding the same data (R111)",
    "D-RENAME-RESIDUE": "a DDL comment or contract description naming a table by its pre-rename name (R160)",
    "D-UNDEFINED-TYPE": "a column typed with a schema-qualified type that no DDL file creates (CHG-R6-001, CR-001)",
    "D-CHILD-PARENT": "an item, line, amendment or media table whose key to its parent is not a NOT NULL declared "
                      "reference (CHG-R6-004..006, CR-007 CR-009 CR-010)",
    "D-SCOPE-TREE": "the scope tree without its declared parent key, one tenant root or unique paths (CHG-R6-003, CR-006)",
    "D-BANNED-NAME": "a table, column or stored enum value the derived DDL takes after r1 with a word naming-and-style "
                     "bans in DDL, not a recorded exception (3.3) (CHG-R6-012, CR-011 CR-012 CR-014)",
    "D-RENAME-APPLIED": "a table or column rename declared in derive-schema-history.py that the schema reference "
                        "does not show (CHG-R6-010)",
    "D-UNIQUE-CASE": "a unique index whose text column is compared otherwise than common.yaml says: lower() unless "
                     "the property is x-ticvai-unique-compare: exact (CHG-GEN-001, CR-079 CR-066)",
    # CHG-MGN-001 (ADAM CR-138, CR-139, CR-148, CR-149, CR-156, CR-157): what the generator hands the migration owner.
    "D-FWD-PARTITION": "the migration review changes a table's partitioning (ADR-0056: nothing points at a "
                       "partitioned table) (CHG-MGN-001, CR-138)",
    "D-FWD-KEY-NULL": "the migration review relaxes a NOT NULL key the contract does not mark nullable (CHG-MGN-001, "
                      "CR-139)",
    "D-FWD-CUT": "a statement in the migration review cut short (CHG-MGN-001, CR-148)",
    "D-FWD-CARRIED": "a unique-together index or required-when CHECK the contract declares that no baseline, forward "
                     "migration or review row carries (CHG-MGN-001, CR-156)",
    "D-FWD-RETIRED": "a column the contract retires left as 'a rename or a drop: decide' (CHG-MGN-001, CR-157)",
    "D-FWD-OWNER": "a table with two keys to one parent whose owner is not decided in derive-ddl ROW_OWNER "
                   "(CHG-MGN-001, CR-148 CR-149)",
}

REVIEW_ROW = re.compile(r"^\| (.+?) \| (\w+) \| `([^`]*)` \| (.*) \| (.*) \|$")
STATEMENT = re.compile(r"^(?:SELECT|CREATE|ALTER|DROP|UPDATE|INSERT|COMMENT)\b", re.I)


def check_forward_migration(guard, review: str, series: str, retired: dict, nullable_keys: set,
                            derived: dict) -> None:
    """D-FWD-*: what derive-ddl's frozen mode handed the migration owner, read back (CHG-MGN-001).

    `review`: handoff/migration-review.md. `series`: every baseline and forward migration under backend/, as one text.
    `retired`: table -> columns the contracts withdraw (`x-ticvai-retired-columns`). `nullable_keys`: (table, column)
    whose contract property is `nullable: true`. `derived`: the name of every unique-together index and required-when
    CHECK the contracts declare -> its table. On r6's review these rules list the class (the 18 October triage, class
    10); on a review the fixed generator writes they find nothing but tables waiting for a decision."""
    for line in review.splitlines():
        m = REVIEW_ROW.match(line.replace("\\|", "\x00"))
        if not m:
            continue
        kind, _db, obj, change, todo = (x.replace("\x00", "|") for x in m.groups())
        if kind == "table changed" and "PARTITION" in change.upper():
            guard.add("D-FWD-PARTITION", obj, f"{obj}: the review changes its partitioning ({change}); a key into "
                      "it must stay undeclared (derive-ddl UNENFORCED_KEYS) and derive-ddl must refuse it")
        if kind == "column changed" and "." in obj:
            t, c = obj.rsplit(".", 1)
            cm = re.match(r"^`(.+?)` -> `(.+?)`$", change)
            if (cm and c.endswith("_id") and re.search(r"\bNOT NULL\b", cm.group(1))
                    and not re.search(r"\bNOT NULL\b|PRIMARY KEY", cm.group(2)) and (t, c) not in nullable_keys):
                guard.add("D-FWD-KEY-NULL", obj, f"{obj}: NOT NULL in the databases and nullable in the derived DDL, "
                          "and the contract does not say nullable: a key the path supplies is required "
                          "(derive-schema path_supplied_keys) or belongs in `required`")
        for item in re.findall(r"`([^`]*)`", f"{change} {todo}"):
            if STATEMENT.match(item.strip()) and item.count("(") != item.count(")"):
                guard.add("D-FWD-CUT", obj, f"{obj}: a statement cut short in the review: {item[:80]!r}")
                break
        if kind == "column dropped" and "." in obj:
            t, c = obj.rsplit(".", 1)
            if c in (retired.get(t) or ()):
                guard.add("D-FWD-RETIRED", obj, f"{obj}: the contract retires it (x-ticvai-retired-columns) and the "
                          "review says 'decide'")
        if kind == "owner undecided":
            guard.add("D-FWD-OWNER", obj, f"{obj}: {change}; decide its owner in tools/derive-ddl.py ROW_OWNER")
    for name, t in sorted(derived.items()):
        if not re.search(r"(?<![\w])" + re.escape(name) + r"(?![\w])", series + "\n" + review):
            guard.add("D-FWD-CARRIED", name, f"{t}: {name} is declared by its contract and in no baseline, forward "
                      "migration or migration-review row")

# **Words naming-and-style bans in DDL** (CHG-R6-012, ADAM CR-011, CR-012 and CR-014, 12 October 2026). The
# derived DDL had taken Hold, Booking, Allocation and Pool, drawer, POS, plural table names and bare money names,
# all of which the standard bans, one migration ticket at a time. A name token (`_`-separated) or an enum value
# word (camelCase) in this set fails unless r1 already had it (the r1 DDL is frozen; what it holds is the
# migration's business, through handoff/migration-review.md) or 3.3 records it as an exception below.
# `hold` is not checked in enum values: `onHold` is a state, not the Reservation concept.
BANNED_NAME_WORDS = {"hold", "booking", "pool", "bucket", "quota", "allocation", "drawer", "pos", "till",
                     "terminal", "barcode", "serial", "card", "other", "misc", "extra", "organization"}
BANNED_VALUE_WORDS = {"pool", "bucket", "quota", "drawer", "pos", "till", "terminal", "barcode", "card", "other",
                      "misc", "extra"}
# A bare money name: 5.1 says `gross_amount`, `net_amount`, `list_price`..., never price, value or total alone.
BARE_MONEY = re.compile(r"^(amount|price|value|total|subtotal|balance|face_value|variance|"
                        r"\w+_(price|total|value))$")
MONEY_TYPES = ("numeric",)

# **The recorded exceptions, as naming-and-style 3.3 lists them** (CHG-R6-012). A word allowed by a row of 3.3
# is allowed here only where that row allows it. Keep the two in step: SF-DOCS-MIRROR keeps the copies of
# naming-and-style identical, and this list is the machine-readable half of its table.
NAME_EXCEPTIONS = {
    # Booking: a guest-facing noun (R145; CR-011)
    "booking": {"resources.booking", "whitelabel.booking_flow", "whitelabel.booking_flow_step",
                "*.booking_id", "*.booking_flow_id"},
    # GTIN barcode: a retail product's barcode, not a Media Code (CR-012, CR-014)
    "barcode": {"catalogue.variant.barcode", "inventory.inventory_item.barcode"},
    # Payment terminal: a card terminal, not a Workstation (CR-014): `orders.payment.terminal_id` and the keys
    # to `payments.terminal`
    "terminal": {"payments.*", "*.terminal_id"},
    # Wallet pass serial: an Apple or Google pass's serial number (CR-014)
    "serial": {"orders.wallet_pass.serial_number"},
    # Game Card, Gift Card (R220) and a payment card in payments
    "card": {"games.*", "*gift_card*", "payments.*"},
}
VALUE_EXCEPTIONS = {
    # wire values: changing one is a breaking change (CR-011, CR-012, CR-014)
    ("catalogue.channel_envelope.envelope_type", "sharedPool"),
    ("platform.device.kind", "cashDrawer"),
    ("ai.forecast_definition.subject", "posDemand"),
    ("ai.rec_decision.placement", "posBasket"),
    ("ai.rec_decline.placement", "posBasket"),
    ("wallet.exit_settlement.method", "card"),
    ("wallet.exit_settlement.method", "storedCard"),
    ("wallet.credit_type.category", "other"),
    ("seating.seat_block.reason", "other"),
    ("resources.resource.kind", "other"),
    ("*", "pos"),          # the point-of-sale sales channel, a wire value in every channel enum
    ("*", "cardScheme"),   # a payment card's scheme (CR-014)
    ("*", "rfidCard"),     # the RFID card credential, a wire value of the credential enums since r1 (r4 gate, 12 Oct)
}


def _allowed(word, table, column):
    full = f"{table}.{column}" if column else table
    for pat in NAME_EXCEPTIONS.get(word, ()):
        if pat == full or pat == table:
            return True
        if pat.endswith(".*") and table.split(".")[0] == pat[:-2]:
            return True
        if pat.startswith("*.") and column and column == pat[2:]:
            return True
        if pat.startswith("*") and pat.endswith("*") and pat.strip("*") in full:
            return True
    return False


def _value_words(v: str) -> list:
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", v)]


def _declared(name: str) -> list:
    import ast
    try:
        tree = ast.parse((g.ROOT / "tools" / "derive-schema-history.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    return []


def check_banned_names(guard, tables: dict, ref_cols: dict, by: dict) -> None:
    """D-BANNED-NAME and D-RENAME-APPLIED. `tables` is the frozen r1 DDL (table -> column -> line), `ref_cols`
    the schema reference derive-ddl writes the DDL from now."""
    renames = _declared("RENAMES")
    col_renames = _declared("COLUMN_RENAMES")
    # only the renames made after r1: an older one's old name was never in the frozen DDL
    was = {r["to"]: r["from"] for r in renames if r["from"] in tables and r["to"] not in tables}
    retired_tables = set(was.values())
    retired_cols = {(r["table"], r["from"]) for r in col_renames}
    new_of = {(r["table"], r["to"]): r["from"] for r in col_renames}

    # D-RENAME-APPLIED: a declared rename the schema reference does not show is a rename half made.
    for r in renames:
        if r["from"] in tables and r["to"] not in ref_cols:
            guard.add("D-RENAME-APPLIED", r["from"], f"{r['from']} -> {r['to']} is declared and the schema "
                      f"reference has no {r['to']}: the contract's x-ticvai-persistence was not changed")
        if r["from"] in tables and r["from"] in ref_cols:
            guard.add("D-RENAME-APPLIED", r["from"] + ":old", f"{r['from']} is declared renamed to {r['to']} and "
                      "is still in the schema reference")
    for r in col_renames:
        names = {c.get("column") for c in ref_cols.get(r["table"], [])}
        if r["to"] not in names or r["from"] in names:
            guard.add("D-RENAME-APPLIED", f"{r['table']}.{r['from']}",
                      f"{r['table']}.{r['from']} -> {r['to']} is declared and the schema reference has "
                      + ", ".join(sorted(n for n in (r["from"], r["to"]) if n in names) or ["neither"])
                      + ": give the contract field `x-ticvai-column`")

    # what r1 had, under the names it has now; a name a declared rename retired is not r1's to keep
    r1_tables = {t for t in tables if t not in retired_tables}
    r1_values = {}
    for t, cols in tables.items():
        for c, line in cols.items():
            m = re.search(r"CHECK \(\s*\"?" + re.escape(c) + r"\"?\s+IN\s*\(([^)]*)\)", line)
            if m:
                r1_values[(t, c)] = set(re.findall(r"'([^']*)'", m.group(1)))

    def r1_has_table(t):
        return t in r1_tables

    def r1_has_col(t, c):
        if (t, c) in retired_cols:
            return False
        t0 = was.get(t, t)
        if (t, c) in new_of:
            return False
        return c in tables.get(t0, {})

    def r1_values_of(t, c):
        t0 = was.get(t, t)
        return r1_values.get((t0, new_of.get((t, c), c)), set())

    for t, cols in sorted(ref_cols.items()):
        if not re.match(r"^[a-z_]+\.[a-z_0-9]+$", t):
            continue
        short = t.split(".", 1)[1]
        if not r1_has_table(t):
            for w in short.split("_"):
                if w in BANNED_NAME_WORDS and not _allowed(w, t, None):
                    guard.add("D-BANNED-NAME", t, f"table {t}: '{w}' is banned in DDL (naming-and-style 3, 7)")
            last = short.split("_")[-1]
            if last.endswith("s") and not last.endswith(("ss", "us", "is")):
                guard.add("D-BANNED-NAME", f"{t}:plural", f"table {t}: a table is a singular noun (6.1)")
        for c in cols:
            col = str(c.get("column") or "")
            if not col:
                continue
            if not r1_has_col(t, col):
                for w in col.split("_"):
                    if w in BANNED_NAME_WORDS and not _allowed(w, t, col):
                        guard.add("D-BANNED-NAME", f"{t}.{col}",
                                  f"{t}.{col}: '{w}' is banned in DDL (naming-and-style 3, 7)")
                if BARE_MONEY.match(col) and col != "list_price" and \
                        str(c.get("type") or "").startswith(MONEY_TYPES):
                    guard.add("D-BANNED-NAME", f"{t}.{col}:money",
                              f"{t}.{col}: a bare money name; 5.1 asks for list_price or *_amount")
            # the values the CHECK will hold: the column's own (storage-only) enum, else its contract field's
            # (derive-ddl checks a scalar text column only; an array's items are the application's)
            if str(c.get("type") or "") != "text":
                continue
            values = list(c.get("enum") or [])
            src = str(c.get("source") or "")
            parts = src.split(".")
            if not values and len(parts) == 3:
                spec = ((by.get((parts[0], parts[1])) or {}).get("properties") or {}).get(parts[2]) or {}
                values = list(spec.get("enum") or [])
            if not values:
                continue
            old = r1_values_of(t, col)
            for v in values:
                v = str(v)
                if v in old or (f"{t}.{col}", v) in VALUE_EXCEPTIONS or ("*", v) in VALUE_EXCEPTIONS:
                    continue
                ws = _value_words(v)
                bad = [w for i, w in enumerate(ws) if w in BANNED_VALUE_WORDS
                       and not (w == "card" and i > 0 and ws[i - 1] in ("gift", "game"))]
                if bad:
                    guard.add("D-BANNED-NAME", f"{t}.{col}={v}",
                              f"{t}.{col}: value '{v}' carries '{bad[0]}', banned in DDL; a wire value is "
                              "recorded in naming-and-style 3.3 or renamed in the contract")
def effective_tables(backend) -> dict:
    """`table -> [columns]` as the databases have them: the frozen baseline files, then each forward migration in
    order (its ADD COLUMN, DROP COLUMN, renames and new tables), read by tools/ddl_forward.py the way derive-ddl
    reads them."""
    import ddl_forward as fwd
    out = {}
    for db in ("tenant", "control"):
        d = backend / db
        if not d.exists():
            continue
        model = fwd.Model()
        for f in sorted(p for p in d.glob("*.sql") if not p.name.startswith("V")):
            model.add_file(f.read_text(encoding="utf-8"))
        for f in sorted((p for p in d.glob("V*.sql") if re.match(r"V\d+__", p.name)),
                        key=lambda p: int(re.match(r"V(\d+)", p.name).group(1))):
            model.apply_forward(re.split(r"^-- =+\n-- ROLLBACK\b", f.read_text(encoding="utf-8"), maxsplit=1,
                                         flags=re.M)[0])
        for t, tab in model.tables.items():
            out[t] = list(tab.cols)
    return out


def check_stub_tables(guard, backend) -> None:
    """D-STUB-TABLE (R087). **A table the lineage writes may not hold only keys, and that cannot be baselined**
    (CHG-GEN-003, ADAM CR-078 and CR-080, 14 October 2026). Twelve stubs (an `id` and one `*_id`) sat in the
    baseline while operations wrote them: `identity.principal_credential` was where every staff credential was to be
    stored and `platform.sale_board_tile` where every till button was, and a developer building either had nowhere
    to put a single field. A stub nothing writes is still baselined debt; a written one fails every run until it has
    its columns. Read from the tables the databases will have (baseline plus forward migrations), so a column added
    after r1 counts."""
    lineage = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    writers: dict = {}
    for op, e in lineage.items():
        for t in (e or {}).get("writes") or []:
            writers.setdefault(t, []).append(op)
    # A stub the generator no longer writes, whose drop handoff/migration-review.md lists for the migration owner
    # (derive-schema-history.py RETIRED_TABLES, CHG-STO-008), is on its way out: a note, not a finding.
    ref_tables = set(((g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}))
    review = g.ROOT / "handoff" / "migration-review.md"
    dropping = set(re.findall(r"^\| table dropped \| \w+ \| `([a-z_]+\.[a-z_0-9]+)` \|",
                              review.read_text(encoding="utf-8"), re.M)) if review.exists() else set()
    for t, names in sorted(effective_tables(backend).items()):
        if names and len(names) <= 2 and all(c == "id" or c.endswith("_id") for c in names):
            if t not in ref_tables and t in dropping:
                guard.note(f"{t}: only {', '.join(names)}; retired, its drop listed in handoff/migration-review.md")
                continue
            w = sorted(writers.get(t, []))
            if w:
                guard.add("D-STUB-TABLE", t, f"{t}: only {', '.join(names)}, and written by {', '.join(w[:4])}"
                          + (f" and {len(w) - 4} more" if len(w) > 4 else "") + " (cannot be baselined)", strict=True)
            else:
                guard.add("D-STUB-TABLE", t, f"{t}: only {', '.join(names)}")


UNIQUE_COMPARE = "x-ticvai-unique-compare"


def _exact_props(by: dict) -> set:
    """`module.Schema.property` for every property marked `x-ticvai-unique-compare: exact`, as derive-ddl reads them:
    through a local `allOf`, and from `Create<X>Request` / `Update<X>Request` onto `<X>`."""
    def props(stem, s, depth=0):
        out = {}
        if not isinstance(s, dict) or depth > 6:
            return out
        for part in s.get("allOf") or []:
            ref = str((part or {}).get("$ref") or "")
            if ref.startswith("#/components/schemas/"):
                out.update(props(stem, by.get((stem, ref.rsplit("/", 1)[-1])), depth + 1))
            else:
                out.update(props(stem, part, depth + 1))
        out.update(s.get("properties") or {})
        return out
    exact = set()
    for (stem, name), s in by.items():
        for p, spec in props(stem, s).items():
            if isinstance(spec, dict) and str(spec.get(UNIQUE_COMPARE) or "") == "exact":
                exact.add(f"{stem}.{name}.{p}")
                m = re.match(r"^(?:Create|Update)(\w+)Request$", name)
                if m:
                    exact.add(f"{stem}.{m.group(1)}.{p}")
    return exact


def check_unique_case(guard, backend, ref_cols: dict, by: dict) -> None:
    """D-UNIQUE-CASE. **One rule for uniqueness, in common.yaml and in the indexes** (CHG-GEN-001, ADAM CR-079 and
    CR-066, 14 October 2026). common.yaml said a value under `x-ticvai-unique` is compared case-insensitively and
    every derived unique index was plain, so `VIP` and `vip` were two role codes. The indexes the databases have
    (the frozen baseline, then each forward migration in order, with the DROP INDEX a person writes) are read
    back: a text column is `lower(column)` unless its contract property is `x-ticvai-unique-compare: exact`, and an
    exact one is not lowered. The r1 indexes stay plain until the forward migration a person writes from
    handoff/migration-review.md ("index changed"), so they are baselined and leave the baseline when it lands."""
    import ddl_forward as fwd
    common = (g.ROOT / "contracts" / "shared" / "common.yaml").read_text(encoding="utf-8")
    flat = " ".join(common.split())
    if "compared case-insensitively" not in flat or f"{UNIQUE_COMPARE}: exact" not in flat:
        guard.add("D-UNIQUE-CASE", "common.yaml", "contracts/shared/common.yaml no longer states the rule "
                  "(text compared case-insensitively; an opaque external id marked x-ticvai-unique-compare: exact)")
    exact_props = _exact_props(by)
    exact_cols = {(t, c.get("column")) for t, cols in ref_cols.items() for c in cols
                  if str(c.get("source") or "") in exact_props}
    for db in ("tenant", "control"):
        d = backend / db
        if not d.exists():
            continue
        files = sorted(p for p in d.glob("*.sql") if not p.name.startswith("V"))
        files += sorted((p for p in d.glob("V*.sql")), key=lambda p: int(re.match(r"V(\d+)", p.name).group(1)))
        types, uniq = {}, {}
        for f in files:
            text = re.split(r"^-- =+\n-- ROLLBACK\b", f.read_text(encoding="utf-8"), maxsplit=1, flags=re.M)[0]
            for st in fwd.split_statements(text):
                s = fwd.norm(st)
                m = re.match(r"CREATE TABLE (?:IF NOT EXISTS )?([a-z_]+\.\"?[a-z_0-9]+\"?)\s*\((.*)\)", s, re.S)
                if m:
                    t = m.group(1).replace('"', "")
                    for item in fwd.top_level_split(m.group(2)):
                        parts = item.split()
                        if len(parts) > 1 and not item.upper().startswith(fwd.TABLE_LEVEL):
                            types[(t, parts[0].replace('"', ""))] = parts[1].lower()
                    continue
                for t, c, typ in re.findall(r"ALTER TABLE ([a-z_]+\.[a-z_0-9]+) ADD COLUMN (?:IF NOT EXISTS )?"
                                            r"\"?([a-z_0-9]+)\"? (\S+)", s):
                    types[(t, c)] = typ.lower()
                m = re.match(r"CREATE UNIQUE INDEX (?:IF NOT EXISTS )?(\S+) ON (?:ONLY )?([a-z_]+\.\"?[a-z_0-9]+\"?)"
                             r"(?: USING \w+)?\s*\((.*)\)(?: WHERE .*)?$", s)
                if m:
                    uniq[m.group(1)] = (m.group(2).replace('"', ""), m.group(3))
                    continue
                m = re.match(r"DROP INDEX (?:CONCURRENTLY )?(?:IF EXISTS )?(?:[a-z_]+\.)?(\S+)", s)
                if m:
                    uniq.pop(m.group(1), None)
        for name, (t, inner) in sorted(uniq.items()):
            for member in fwd.top_level_split(inner):
                lowered = re.match(r"^lower\(\s*\"?([a-z_0-9]+)\"?\s*\)$", member)
                plain = re.match(r"^\"?([a-z_0-9]+)\"?$", member)
                col = (lowered or plain).group(1) if (lowered or plain) else None
                if not col or types.get((t, col)) != "text":
                    continue
                exact = (t, col) in exact_cols
                if plain and not exact:
                    guard.add("D-UNIQUE-CASE", f"{name}:{col}",
                              f"{name} on {t}: {col} is text and compared case-sensitively; common.yaml says "
                              "case-insensitively (lower(), or mark an opaque external id x-ticvai-unique-compare: exact)")
                elif lowered and exact:
                    guard.add("D-UNIQUE-CASE", f"{name}:{col}",
                              f"{name} on {t}: {col} is x-ticvai-unique-compare: exact and indexed lower()")


# `require_` beside `requires_`, as `allow_` beside `allows_` (CHG-GTRB-006: till_shift_policy.require_open_approval).
BOOL_OK = re.compile(r"^(is|has|can|require|requires|allows|allow|should|was|were|did|does|must|needs|include|includes|"
                     r"show|shows|auto|use|uses|supports|accepts|enable|enabled|send|notify|override)_|"
                     r"_(enabled|required|allowed|visible|active|locked|verified|confirmed|approved)$")


def reads_as_assertion(column: str) -> bool:
    """The generator's own rule (tools/derive-schema.py `bool_reads_as_assertion`, CHG-STO-009), so the check and the
    name it derives cannot disagree again; BOOL_OK above is the standard's core and stays inside that rule."""
    fn = _cache.get("bool")
    if fn is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("derive_schema", str(g.ROOT / "tools" / "derive-schema.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fn = _cache["bool"] = mod.bool_reads_as_assertion
    return bool(BOOL_OK.search(column)) or fn(column)


_cache: dict = {}
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
    # **The baseline is frozen at r1; a column added after it is in a forward migration** (CHG-TEN-001, ADAM
    # CR-080). `platform.sale_board_tile` got its columns in a V-file, and read from 010-*.sql alone it stayed a
    # stub for ever. A forward migration's `ADD COLUMN` joins its table here, so a fixed stub stops being one.
    for db in ("tenant", "control"):
        for f in sorted((backend / db).glob("V*.sql")):
            for name, col, rest in re.findall(r"ALTER TABLE ([a-z_]+\.[a-z_0-9]+) ADD COLUMN (?:IF NOT EXISTS )?"
                                              r'"?([a-z_][a-z_0-9]*)"? ([^;\n]+);', f.read_text(encoding="utf-8")):
                if name in tables:
                    tables[name].setdefault(col, f"{col} {rest}")

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
    #
    # **Read from the DDL the generator writes now, not from the frozen r1 files** (CHG-STO-005, 14 October 2026). The
    # baseline under backend/ is frozen at r1 and only a forward migration changes a table, so a key, a key's name or a
    # boolean's name read from 900 and 010 could never be fixed at its source: the contract and the generators, which
    # write the schema reference derive-ddl writes the DDL from (as check-storage-promises reads it). Where the fix to
    # an r1 table is a rename or a constraint, derive-ddl lists it in handoff/migration-review.md for the migration
    # owner, and check-migrations and check-migration-freeze hold the databases to it.
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    ref_cols = ref.get("cols") or {}
    ref_store = ref.get("store") or {}

    def _area(t):
        return "control" if t.split(".")[0] == "control" else "tenant"
    ref_fks = []
    for t, cs in sorted(ref_cols.items()):
        if "." not in t or ":" in t or ref_store.get(t, "postgres") not in ("postgres", "postgres-analytical"):
            continue
        for c in cs:
            to = c.get("references")
            if c.get("enforced") == "yes" and to in ref_cols and _area(to) == _area(t) and c.get("column") != "id":
                ref_fks.append((t, [c["column"]], to))
    renamed = {}
    for r in ((g.load_json(g.ROOT / "handoff" / "schema-history.json", {}) or {}).get("renames") or []):
        old = str(r.get("from") or "").split(".")[-1]
        if old:
            renamed[old + "_id"] = r.get("to")
    by_parent = {}
    for t, cols, target in ref_fks:
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
                                            r"replac|merged|primary|secondary|fallback|credit|debit|new|old)", c)
                                  for c in others):
                guard.add("D-DOUBLE-KEY", f"{t}->{target}",
                          f"{t}: {own} beside {', '.join(others)}, all keys to {target}")

    # **A scope_path a forward migration adds is NOT NULL once it is backfilled** (14 October 2026, CHG-R6G-002, tracker
    # F15). Frozen mode adds a new column nullable (a NOT NULL one fails on the first table with rows), so the column
    # counts as NOT NULL when a forward migration sets it (`ALTER COLUMN scope_path SET NOT NULL`, the person's
    # migration), and is waiting, not forgotten, while handoff/migration-review.md names its backfill before the NOT
    # NULL (tools/ddl_forward.py::scope_path_backfill writes it when the table holds its owning scope's key). A
    # nullable scope_path with neither still fails.
    set_nn, pending = set(), set()
    for db in ("tenant", "control"):
        for f in sorted((backend / db).glob("V*.sql")):
            set_nn |= set(re.findall(r'ALTER TABLE ([a-z_]+\.[a-z_0-9]+) ALTER COLUMN "?scope_path"? SET NOT NULL',
                                     f.read_text(encoding="utf-8")))
    review = g.ROOT / "handoff" / "migration-review.md"
    if review.exists():
        for rline in review.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\| not null \| \w+ \| `([a-z_]+\.[a-z_0-9]+)\.scope_path` \|", rline)
            fill = f"UPDATE {m.group(1)} " if m else ""
            if m and fill in rline and "SET NOT NULL" in rline and rline.find(fill) < rline.find("SET NOT NULL"):
                pending.add(m.group(1))
    for t, cols in sorted(tables.items()):
        if "scope_path" in cols:
            line = cols["scope_path"]
            if not re.match(r"scope_path\s+ltree\b", line):
                guard.add("D-SCOPE-LTREE", t, f"{t}.scope_path is not ltree: {line[:60]!r}")
            if t in rls and "NOT NULL" not in line and "shared" not in line.lower() and t not in set_nn:
                if t in pending:
                    guard.note(f"{t}.scope_path: added nullable; its backfill, then the NOT NULL, named in "
                               "handoff/migration-review.md for a person's forward migration")
                    continue
                guard.add("D-SCOPE-NOTNULL", t, f"{t}.scope_path is nullable under row-level security")
    check_stub_tables(guard, backend)

    # R019: a column description that is its contract field's description, cut.
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
        # A table renamed after r1 (derive-schema-history.py RENAMES) is created under its old name by the frozen SQL
        # and goes by its new one everywhere else, MIGRATIONS.md included (12 October 2026, CHG-R6-055).
        created |= {r["to"] for r in _declared("RENAMES") if r["from"] in created}
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

    # R093 R119: naming-and-style 6.1. A boolean's name, as the generator names it now (CHG-STO-005: an r1 column's
    # rename is a "column renamed" row in migration-review.md, declared in derive-schema-history.py COLUMN_RENAMES).
    for t, cs in sorted(ref_cols.items()):
        if "." not in t or ":" in t or ref_store.get(t, "postgres") not in ("postgres", "postgres-analytical"):
            continue
        for col in cs:
            c = str(col.get("column") or "")
            if str(col.get("type") or "").lower() == "boolean" and not reads_as_assertion(c):
                guard.add("D-NAMING", f"{t}.{c}", f"{t}.{c}: a boolean that does not read as an assertion")
    for db in ("tenant", "control"):
        for f in (backend / db).glob("*.sql"):
            for uniq, name, t in re.findall(r"CREATE (UNIQUE )?INDEX (?:IF NOT EXISTS )?(\S+) ON (?:ONLY )?"
                                            r"([a-z_]+\.[a-z_0-9]+)", f.read_text(encoding="utf-8")):
                want = "_uniq" if uniq else "_idx"
                if not name.endswith(want) and not name.endswith("_gist") and not name.endswith("_idx"):
                    guard.add("D-NAMING", f"index:{name}", f"{name} on {t}: an index name should end {want}")

    # R082: a key named for one table that references another (read from the generator's DDL, CHG-STO-005).
    for t, cols, target in ref_fks:
        # `_ref` is the package's name for a key to an asset (`imageAssetRef`, `sourceRef`): strip it like `_id`
        # (CHG-GTRB-006: maintenance.incident_media.asset_ref references assets.media_asset).
        stem = re.sub(r"_(?:ids?|refs?)$", "", cols[-1])
        tname = target.split(".")[-1]
        if stem in ("current", "previous", "next", "original", "source", "target", "replacement", "parent"):
            continue  # a role within one table's own history, not a table name
        head = stem.split("_")[-1]
        # a role in front of an aliased concept names it too (`home_region_id`, `primary_venue_id` -> platform.scope)
        akey = stem if stem in FK_ALIASES else head if FK_ALIASES.get(head) else None
        if akey:
            alias = FK_ALIASES[akey]
            if alias and alias not in tname:
                guard.add("D-FK-TARGET-NAME", f"{t}.{cols[-1]}", f"{t}.{cols[-1]} references {target}")
            continue
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

    # CHG-R6-001 (ADAM CR-001, 12 October 2026): `pii.subject.kind` was typed `pii.subject_kind`, which no file
    # creates, so 010-pii.sql could not be applied. The schema reference is what derive-ddl types columns from, so
    # it is read here rather than the frozen baseline: a type named `<schema>.<name>` must be created by a
    # CREATE TYPE or CREATE DOMAIN somewhere in backend/.
    defined = set()
    for f in backend.rglob("*.sql"):
        defined |= {n.replace('"', "") for n in re.findall(
            r"CREATE\s+(?:TYPE|DOMAIN)\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-z_]+\.[a-z_0-9]+)",
            f.read_text(encoding="utf-8"), re.I)}
    ref_cols = (ref.get("cols") or {})
    for t, cols in sorted(ref_cols.items()):
        for c in cols:
            typ = str(c.get("type") or "").strip().lower().removesuffix("[]")
            if re.match(r"^[a-z_]+\.[a-z_0-9]+$", typ) and typ not in defined:
                guard.add("D-UNDEFINED-TYPE", f"{t}.{c.get('column')}",
                          f"{t}.{c.get('column')} is typed {typ}, which no DDL file creates: give it a built-in "
                          "type (an enum is text with `enum` on the column record) or create the type")

    # CHG-R6-004..006 (ADAM CR-007, CR-009, CR-010, 12 October 2026): `workforce.attendance_amendment`,
    # `seating.seat_hold_item` and `seating.seat_block_item` pointed at their parent by convention (an index, no
    # constraint, so no parent policy and the rows sat at the tenant root), and `catalogue.product_media` had no key
    # to its product at all. A table `<schema>.<parent>_{item,line,amendment,media}` beside `<schema>.<parent>` keeps
    # its parent key as a NOT NULL declared reference (`x-ticvai-references` on the contract property, or a `+`
    # persistence tag).
    for t, cols in sorted(ref_cols.items()):
        if "." not in t:
            continue
        s, short = t.split(".", 1)
        m = re.match(r"^(.+)_(item|line|amendment|media)$", short)
        if not m or f"{s}.{m.group(1)}" not in ref_cols:
            continue
        parent, p = f"{s}.{m.group(1)}", m.group(1)
        # A key named for the parent with its module in front (`rental_agreement_id` -> `rental.agreement`) is the
        # parent key too (CHG-STO-004).
        keys = [c for c in cols if str(c.get("column", "")).endswith("_id") and c.get("column") != "id"
                and (p.endswith(c["column"][:-3]) or c["column"][:-3].startswith(p)
                     or c["column"][:-3] == f"{s}_{p}")]

        def reaches(c, depth=0):
            """A NOT NULL declared key to the parent, or to a table of the parent's that has one (a menu item sits in
            a section, the section in its menu: `fnb.menu_item.menu_section_id` -> `fnb.menu_section.menu_id`)."""
            if c.get("enforced") != "yes" or c.get("required") != "yes":
                return False
            to = c.get("references")
            if to == parent:
                return True
            return depth < 2 and str(to).startswith(parent + "_") and any(
                reaches(x, depth + 1) for x in ref_cols.get(to, []) if str(x.get("column", "")).endswith("_id"))
        if not any(reaches(c) for c in keys):
            have = ", ".join(f"{c['column']} -> {c.get('references')} ({c.get('referenceHow')})" for c in keys)
            guard.add("D-CHILD-PARENT", t, f"{t}: no NOT NULL declared key to {parent}"
                      + (f" (has {have})" if have else " (no key column)"))

    # CHG-R6-003 (ADAM CR-006, 12 October 2026): every policy resolves a grant through platform.scope by
    # `level = 'tenant'` and by `path`. Its parent key is declared, it has one tenant root, and a path names one node.
    scope_cols = {c.get("column"): c for c in ref_cols.get("platform.scope", [])}
    if scope_cols:
        pc = scope_cols.get("parent_id") or {}
        if not (pc.get("references") == "platform.scope" and pc.get("enforced") == "yes"):
            guard.add("D-SCOPE-TREE", "platform.scope.parent_id",
                      "platform.scope.parent_id is not a declared reference to platform.scope")
        series = "\n".join(f.read_text(encoding="utf-8") for f in (backend / "tenant").glob("*.sql"))
        if not re.search(r"CREATE UNIQUE INDEX[^;]*ON platform\.scope\s*\(\(true\)\)\s*WHERE level = 'tenant'", series):
            guard.add("D-SCOPE-TREE", "platform.scope:tenant-root",
                      "nothing in backend/tenant makes the tenant root of platform.scope unique")
        if not re.search(r"CREATE UNIQUE INDEX[^;]*ON platform\.scope\s*\(path\)", series):
            guard.add("D-SCOPE-TREE", "platform.scope:path", "nothing in backend/tenant makes platform.scope.path unique")

    # CHG-R6-012 (ADAM CR-011, CR-012, CR-014, 12 October 2026): banned words in what the DDL takes after r1.
    check_banned_names(guard, tables, ref_cols, by)

    # CHG-GEN-001 (ADAM CR-079, CR-066, 14 October 2026): a unique value is compared as common.yaml says.
    check_unique_case(guard, backend, ref_cols, by)

    # CHG-MGN-001 (ADAM CR-138, CR-139, CR-148, CR-149, CR-156, CR-157, 18 October 2026): the forward migration and its
    # review, read back against what the contracts declare. derive-ddl's own readers give the names and the retired
    # columns, so the check and the generator cannot disagree on them.
    import importlib.util
    spec = importlib.util.spec_from_file_location("derive_ddl", g.ROOT / "tools" / "derive-ddl.py")
    dd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dd)
    props = dd.load_contract_props({stem: doc for stem, _rel, doc in g.contracts()})
    real = [t for t in ref_cols if "." in t and ":" not in t
            and ref_store.get(t, "postgres") in ("postgres", "postgres-analytical")]
    derived = {}
    for t, mk in dd.table_marks(ref_cols, real).items():
        short = t.split(".", 1)[1]
        ao = mk.get("append_only")
        part = [ao] if ao and not ao.startswith("?") and _area(t) == "tenant" else []
        for group in mk.get("unique_together") or []:
            if not any(k.startswith("?") for k in group):
                derived[dd.obj_name(short, *group, *[x for x in part if x not in group], suffix="uniq")] = t
        for rcol, cond in mk.get("required_when") or []:
            if not rcol.startswith("?") and not any(k.startswith("?") for k in cond):
                derived[dd.obj_name(short, rcol, "when", suffix="chk")] = t
    nullable_keys = {(t, c.get("column")) for t, cs in ref_cols.items() for c in cs
                     if (props.get(str(c.get("source") or "")) or {}).get("nullable") is True}
    series = "\n".join(f.read_text(encoding="utf-8") for db in ("tenant", "control")
                       for f in sorted((backend / db).glob("*.sql")))
    check_forward_migration(guard, review.read_text(encoding="utf-8") if review.exists() else "", series,
                            dd.RETIRED, nullable_keys, derived)

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
