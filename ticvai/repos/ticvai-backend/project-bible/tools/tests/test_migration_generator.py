"""Tests for the forward-migration generator: what derive-schema, derive-ddl and ddl_forward hand the migration owner
(class 10 of the 18 October triage: ADAM CR-138, CR-139, CR-148, CR-149, CR-156, CR-157; CHG-MGN-001).

    python -m pytest ticvai/tools/tests/test_migration_generator.py -q

Every test builds its DDL or contract in memory; nothing reads or writes the package's derived files.
"""
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import ddl_forward as fwd  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, TOOLS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def model(sql: str) -> "fwd.Model":
    m = fwd.Model()
    m.add_file(sql)
    return m


def rows(plan, kind=None):
    return [r for r in plan.review if kind is None or r[0] == kind]


def ran(stmts):
    """What the forward migration's statements run: a guarded block read as the statement inside it (CHG-R9MIG-002)."""
    return [x for s in stmts for x in fwd.inner(s)]


# ---- 3. every statement whole (CR-148) ----------------------------------------------------------------------------

PARENT = "CREATE TABLE IF NOT EXISTS inventory.inventory_item (id uuid PRIMARY KEY);\n"
LONG_POLICY = ("SELECT platform.apply_parent_rls('fnb.ingredient_substitute'::regclass, 'from_inventory_item_id', "
               "'inventory.inventory_item'::regclass, 'id');\n")


def test_after_rename_row_holds_every_statement_whole():
    old = model(PARENT + "CREATE TABLE IF NOT EXISTS fnb.ingredient_swap (id uuid PRIMARY KEY, "
                         "from_inventory_item_id uuid NOT NULL);\n"
                         "SELECT platform.apply_tenant_rls('fnb.ingredient_swap'::regclass);\n")
    new = model(PARENT + "CREATE TABLE IF NOT EXISTS fnb.ingredient_substitute (id uuid PRIMARY KEY, "
                         "from_inventory_item_id uuid NOT NULL);\n" + LONG_POLICY)
    p = fwd.diff("tenant", old, new, {"tables": {"fnb.ingredient_swap": "fnb.ingredient_substitute"}})
    after = rows(p, "after rename")
    assert after, p.review
    assert fwd.norm(LONG_POLICY.rstrip().rstrip(";")) in after[0][2]


def test_statement_added_row_is_whole():
    tail = "x" * 200
    old = model(PARENT)
    new = model(PARENT + f"COMMENT ON TABLE inventory.inventory_item IS '{tail}';\n")
    p = fwd.diff("tenant", old, new)
    added = rows(p, "statement added")
    assert added and tail in added[0][2]


# ---- 5. a column the contract retires is a drop, not "decide" (CR-157) ---------------------------------------------

WS_OLD = ("CREATE TABLE IF NOT EXISTS platform.scope (id uuid PRIMARY KEY);\n"
          "CREATE TABLE IF NOT EXISTS platform.workstation (id uuid PRIMARY KEY, venue_id uuid NOT NULL, "
          "org_unit_id uuid NOT NULL);\n"
          "ALTER TABLE platform.workstation ADD CONSTRAINT workstation_org_unit_id_fkey FOREIGN KEY (org_unit_id) "
          "REFERENCES platform.scope(id);\n"
          "CREATE INDEX IF NOT EXISTS workstation_org_unit_id_idx ON platform.workstation (org_unit_id);\n")
WS_NEW = ("CREATE TABLE IF NOT EXISTS platform.scope (id uuid PRIMARY KEY);\n"
          "CREATE TABLE IF NOT EXISTS platform.workstation (id uuid PRIMARY KEY, venue_id uuid NOT NULL);\n")
RETIRED = {"platform.workstation": {"org_unit_id"}}


def fold(old_sql: str, plan) -> "fwd.Model":
    """The old side once the plan's forward migration has been written (what derive-ddl's next run reads)."""
    m = model(old_sql)
    m.apply_forward(";\n".join(plan.statements) + ";\n")
    return m


def test_retired_column_is_worded_as_a_drop_and_names_its_key_and_index():
    p = fwd.diff("tenant", model(WS_OLD), model(WS_NEW), retired=RETIRED)
    assert not [r for r in p.review if "decide" in r[3] and "org_unit_id" in r[1]], p.review
    row = [r for r in p.review if r[0] == "column retired"]
    assert row and row[0][1] == "platform.workstation.org_unit_id"
    assert "x-ticvai-retired-columns" in row[0][2]
    assert "four-step drop" in row[0][3]
    assert "workstation_org_unit_id_fkey" in row[0][3] and "workstation_org_unit_id_idx" in row[0][3]
    # its key and index are named in that row, not listed again as separate drops
    assert not [r for r in p.review if r[0] in ("constraint dropped", "index dropped")], p.review


def test_retired_column_loses_not_null_in_the_forward_migration_once():
    p = fwd.diff("tenant", model(WS_OLD), model(WS_NEW), retired=RETIRED)
    stmt = [s for s in p.statements if "DROP NOT NULL" in s]
    assert len(stmt) == 1
    # guarded: applies on a database where a person already dropped the column (CR-157's four-step drop)
    assert "information_schema.columns" in stmt[0] and "'org_unit_id'" in stmt[0]
    assert any("SET NOT NULL" in r for r in p.rollback)
    again = fwd.diff("tenant", fold(WS_OLD, p), model(WS_NEW), retired=RETIRED)
    assert not again.statements, again.statements
    assert [r for r in again.review if r[0] == "column retired"]


def test_a_dropped_column_the_contract_does_not_retire_is_still_a_decision():
    p = fwd.diff("tenant", model(WS_OLD), model(WS_NEW))
    assert [r for r in p.review if r[0] == "column dropped" and "decide" in r[3]]
    assert not [s for s in p.statements if "DROP NOT NULL" in s]


def test_derive_ddl_reads_retired_columns_as_derive_schema_does():
    dd = _load("derive_ddl_t5", "derive-ddl.py")
    dd.RETIRED.clear()
    dd.retired_columns({"x-ticvai-persistence": "platform.workstation", "x-ticvai-retired-columns": ["org_unit_id"]})
    dd.retired_columns({"allOf": [{"$ref": "#/x"}, {"x-ticvai-persistence": "platform.venue_settings + platform.x",
                                                   "x-ticvai-retired-columns": ["org_unit_id",
                                                                                "whitelabel.navigation_item.item_id"]}]})
    assert dd.RETIRED == {"platform.workstation": {"org_unit_id"}, "platform.venue_settings": {"org_unit_id"},
                          "whitelabel.navigation_item": {"item_id"}}


# ---- 4. a table CHECK and a composite unique index reach the migration (CR-156) -----------------------------------

def test_table_marks_resolve_a_table_whose_parent_key_names_a_nested_inline_array():
    """platform.sale_board_tile: its parent key's source is `tenancy.SaleBoard.pages[].tiles` (pages' items are
    inline, so they resolve to no schema) and every other column's is `tenancy.SaleBoardTile.*`."""
    dd = _load("derive_ddl_t4", "derive-ddl.py")
    dd.SCHEMA_MARKS.clear(); dd.ITEM_SCHEMA.clear(); dd.ARRAY_PROPS.clear()
    dd.SCHEMA_MARKS["tenancy.SaleBoardTile"] = {
        "x-ticvai-unique-together": [["sale_board_page_id", "position"]],
        "x-ticvai-required-when": {"variantId": {"kind": "product"}}}
    dd.SCHEMA_MARKS["tenancy.SaleBoard"] = {}
    dd.ARRAY_PROPS.add("tenancy.SaleBoard.pages")
    cols = {"platform.sale_board_tile": [
        {"column": "sale_board_page_id", "source": "tenancy.SaleBoard.pages[].tiles"},
        {"column": "position", "source": "tenancy.SaleBoardTile.position"},
        {"column": "kind", "source": "tenancy.SaleBoardTile.kind"},
        {"column": "variant_id", "source": "tenancy.SaleBoardTile.variantId"},
        {"column": "id", "source": "derive-schema.py (surrogate)"}]}
    m = dd.table_marks(cols, cols)["platform.sale_board_tile"]
    assert m["schema"] == "tenancy.SaleBoardTile"
    assert m["unique_together"] == [["sale_board_page_id", "position"]]
    assert m["required_when"] == [("variant_id", {"kind": "product"})]


def test_a_parent_array_key_does_not_vote_for_the_parent_schema():
    """CHG-CRD-001's case stays right: a child whose item columns resolve takes the item schema, and a key whose
    source is the parent's array never makes a table the parent's."""
    dd = _load("derive_ddl_t4b", "derive-ddl.py")
    dd.SCHEMA_MARKS.clear(); dd.ITEM_SCHEMA.clear(); dd.ARRAY_PROPS.clear()
    dd.SCHEMA_MARKS["identity.PrincipalCredential"] = {"x-ticvai-unique-together": [["principal_id"]]}
    dd.SCHEMA_MARKS["identity.CredentialHistoryEntry"] = {"x-ticvai-append-only": "changedAt"}
    dd.ITEM_SCHEMA["identity.PrincipalCredential.history"] = "identity.CredentialHistoryEntry"
    dd.ARRAY_PROPS.add("identity.PrincipalCredential.history")
    cols = {"identity.principal_credential_history": [
        {"column": "principal_credential_id", "source": "identity.PrincipalCredential.history"},
        {"column": "changed_at", "source": "identity.PrincipalCredential.history[].changedAt"}]}
    m = dd.table_marks(cols, cols)["identity.principal_credential_history"]
    assert m["schema"] == "identity.CredentialHistoryEntry" and "unique_together" not in m
    cols2 = {"x.child": [{"column": "parent_id", "source": "x.Parent.lines"},
                         {"column": "qty", "source": "x.Parent.lines[].qty"}]}
    dd.SCHEMA_MARKS["x.Parent"] = {"x-ticvai-unique-together": [["qty"]]}
    dd.ARRAY_PROPS.add("x.Parent.lines")
    assert "x.child" not in dd.table_marks(cols2, cols2)


TILE_OLD = ("CREATE TABLE IF NOT EXISTS platform.sale_board_tile (id uuid PRIMARY KEY, page_id uuid, "
            "position integer, kind text, variant_id uuid);\n"
            "CREATE INDEX IF NOT EXISTS sale_board_tile_page_id_idx ON platform.sale_board_tile (page_id);\n")
CHK = ("CONSTRAINT sale_board_tile_variant_id_when_chk CHECK (kind IS DISTINCT FROM 'product' OR "
       "variant_id IS NOT NULL)")
TILE_NEW = ("CREATE TABLE IF NOT EXISTS platform.sale_board_tile (sale_board_page_id uuid NOT NULL, position integer, "
            "kind text, variant_id uuid, id uuid PRIMARY KEY,\n    " + CHK + ");\n"
            "CREATE INDEX IF NOT EXISTS sale_board_tile_sale_board_page_id_idx ON platform.sale_board_tile "
            "(sale_board_page_id);\n"
            "CREATE UNIQUE INDEX IF NOT EXISTS sale_board_tile_sale_board_page_id_position_uniq ON "
            "platform.sale_board_tile (sale_board_page_id, position);\n")
TILE_RENAMES = {"columns": {("platform.sale_board_tile", "page_id"): "sale_board_page_id"}}


def test_a_table_check_on_an_existing_table_is_written_not_valid_then_validated():
    p = fwd.diff("tenant", model(TILE_OLD), model(TILE_NEW), TILE_RENAMES)
    body = ran(p.statements)
    name = "sale_board_tile_variant_id_when_chk"
    assert f"ALTER TABLE platform.sale_board_tile DROP CONSTRAINT IF EXISTS {name}" in body
    add = [s for s in body if s.startswith(f"ALTER TABLE platform.sale_board_tile ADD CONSTRAINT {name} CHECK")]
    assert add and add[0].endswith("NOT VALID")
    assert f"ALTER TABLE platform.sale_board_tile VALIDATE CONSTRAINT {name}" in body
    assert body.index(add[0]) < body.index(f"ALTER TABLE platform.sale_board_tile VALIDATE CONSTRAINT {name}")
    assert not [r for r in p.review if r[0] == "constraint added" and name in r[2]], p.review
    assert any(name in r for r in p.rollback)
    again = fwd.diff("tenant", fold(TILE_OLD, p), model(TILE_NEW), TILE_RENAMES)
    assert not [s for s in again.statements if name in s], again.statements


def test_a_new_unique_index_on_a_renamed_column_is_written_after_the_rename():
    # the rename adds a NOT NULL: the rename is still written, the NOT NULL stays its own review row
    p = fwd.diff("tenant", model(TILE_OLD), model(TILE_NEW), TILE_RENAMES)
    text = chr(10).join(p.recon)
    assert "CREATE UNIQUE INDEX IF NOT EXISTS sale_board_tile_sale_board_page_id_position_uniq" in text
    assert text.index("RENAME COLUMN page_id") < text.index("sale_board_page_id_position_uniq")
    assert "ALTER INDEX platform.sale_board_tile_page_id_idx RENAME TO sale_board_tile_sale_board_page_id_idx" in text
    assert [r for r in p.review if r[0] == "not null" and "sale_board_page_id" in r[1]], p.review


def test_a_rename_a_frozen_file_depends_on_goes_in_the_early_file():
    p = fwd.diff("tenant", model(TILE_OLD), model(TILE_NEW), TILE_RENAMES)
    frozen = {"V0104__after_r1_x.sql": "SELECT platform.apply_parent_rls('platform.sale_board_tile'::regclass, "
                                       "'sale_board_page_id', 'platform.sale_board_page'::regclass, 'id');"}
    early, rest, first = fwd.split_early(p, frozen)
    assert first == "V0104__after_r1_x.sql" and len(early[0]) == 1 and "RENAME COLUMN page_id" in early[0][0]
    assert not [s for s in rest[0] if "RENAME COLUMN page_id" in s]
    assert fwd.split_early(p, {})[0] == ([], [])


def test_the_early_file_takes_a_letter_and_sorts_between_the_two_frozen_files():
    # CHG-R8MIG-003: V01035 sorted before V0103 and read as 1035 (the plan's V1035__fnb.sql); a letter does neither
    ev = fwd.early_version("V0104__after_r1_20261015.sql", {"V0100", "V0103", "V0104", "V0105", "V0107"})
    assert ev == "V0103a"
    names = ["V0103__after_r1_20261013.sql", f"{ev}__names_early_after_r1_20261020.sql", "V0104__after_r1_20261015.sql",
             "V0105__after_r1_20261018.sql", "V0107__names_after_r1_20261020.sql"]
    assert sorted(names) == names                                   # ordinal, as SqlMigrationRunner sorts
    assert fwd.early_version("V0104__x.sql", {"V0103a"}) == "V0103b"  # a letter already taken is not reused
    import ticket_done as td
    assert td.AFTER_R1_FILE.match(names[1])
    dd = _load("derive_ddl_early", "derive-ddl.py")
    assert dd.FORWARD_FILE.match(names[1]), "derive-ddl must read the early file back, or a second run writes it again"


def test_the_early_file_says_which_file_it_runs_before():
    p = fwd.diff("tenant", model(TILE_OLD), model(TILE_NEW), TILE_RENAMES)
    early, rest, first = fwd.split_early(p, {"V0104__after_r1_x.sql": "SELECT platform.apply_parent_rls("
                                             "'platform.sale_board_tile'::regclass, 'sale_board_page_id', 'x'::regclass, 'id');"})
    import dataclasses
    ep = dataclasses.replace(p, recon=early[0], recon_rollback=early[1],
                             recon_counts={"renames": len(early[0]), "keys": 0, "indexes": 0})
    text = fwd.render_recon(ep, "V0103a", "r1", "20261020", before=first, rest="V0107")
    assert "runs before V0104__after_r1_x.sql" in text and "VALUES ('V0103a'" in text and "are in V0107" in text
    assert "RENAME COLUMN page_id TO sale_board_page_id" in text


def test_a_table_check_naming_a_renamed_column_waits_for_the_rename_whole():
    chk = "CONSTRAINT sale_board_tile_sale_board_page_id_when_chk CHECK (kind IS DISTINCT FROM 'x' OR " \
          "sale_board_page_id IS NOT NULL)"
    new = TILE_NEW.replace(CHK, CHK + ",\n    " + chk)
    p = fwd.diff("tenant", model(TILE_OLD), model(new), TILE_RENAMES)
    assert not [s for s in p.statements if "sale_board_page_id_when_chk" in s]
    row = [r for r in p.review if "sale_board_page_id_when_chk" in r[2] or "sale_board_page_id_when_chk" in r[3]]
    assert row and row[0][0] == "constraint after rename" and "IS NOT NULL" in row[0][3]


# ---- 1. a declared key never turns partitioning off (CR-138) ------------------------------------------------------

def test_an_inbound_key_into_a_partitioned_table_is_refused_not_declined():
    dd = _load("derive_ddl_t1", "derive-ddl.py")
    marks = {"marketing.message_dispatch": {"append_only": "queued_at"},
             "marketing.scan": {"append_only": "scanned_at"},
             "marketing.odd": {"append_only": "?when"}}
    inbound = {"marketing.message_dispatch": {"marketing.message_dispatch_attempt.message_dispatch_id"}}
    partitioned, declined, refused = dd.partition_plan(marks, inbound)
    assert partitioned == {"marketing.scan": "scanned_at"}
    assert refused == [("marketing.message_dispatch", ["marketing.message_dispatch_attempt.message_dispatch_id"])]
    assert [t for t, _ in declined] == ["marketing.odd"]


def test_a_key_into_a_partitioned_table_stays_an_index_not_a_constraint():
    dd = _load("derive_ddl_t1b", "derive-ddl.py")
    assert dd.UNENFORCED_KEYS[("marketing.message_dispatch_attempt", "message_dispatch_id")] == \
        "marketing.message_dispatch"
    cols = {"marketing.message_dispatch_attempt": [{"column": "message_dispatch_id", "type": "uuid"}]}
    dd.apply_unenforced_keys(cols)
    c = cols["marketing.message_dispatch_attempt"][0]
    assert (c["references"], c["enforced"], c["referenceHow"]) == ("marketing.message_dispatch", "no", "convention")


# ---- 2. a key the request path supplies is NOT NULL (CR-139) ------------------------------------------------------

def _catalogue(**over):
    alloc = {"x-ticvai-persistence": "catalogue.channel_envelope", "type": "object", "required": ["channel"],
             "properties": {
                 "channel": {"type": "string"},
                 "channelCapacityId": {"type": "string", "format": "uuid", "readOnly": True,
                                       "x-ticvai-references": "catalogue.channel_capacity"},
                 "salesChannelId": {"type": "string", "format": "uuid", "readOnly": True, "nullable": True,
                                    "x-ticvai-references": "catalogue.sales_channel"},
                 "venueId": {"type": "string", "format": "uuid", "x-ticvai-references": "platform.venue"}}}
    alloc["properties"].update(over)
    return {"catalogue": ("spine", {
        "paths": {"/channel-capacities/{channelCapacityId}/channel-allocations": {
                      "put": {"operationId": "setChannelAllocations",
                              "responses": {"200": {"content": {"application/json": {"schema": {
                                  "$ref": "#/components/schemas/ChannelAllocationSet"}}}}}}},
                  "/venues/{venueId}/sales-channels/{salesChannelId}": {
                      "get": {"operationId": "x", "responses": {"200": {"content": {"application/json": {
                          "schema": {"$ref": "#/components/schemas/ChannelAllocation"}}}}}}}},
        "components": {"schemas": {
            "ChannelAllocationSet": {"type": "object", "properties": {"allocations": {
                "type": "array", "items": {"$ref": "#/components/schemas/ChannelAllocation"}}}},
            "ChannelAllocation": alloc}}})}


def test_a_read_only_declared_key_the_path_supplies_is_required():
    ds = _load("derive_schema_t2", "derive-schema.py")
    cat = _catalogue()
    cat["catalogue"][1]["paths"]["/channel-capacities/{channelCapacityId}/channel-allocations"]["put"]["requestBody"] = {
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ChannelAllocation"}}}}
    keys = ds.path_supplied_keys(cat)
    assert ("ChannelAllocation", "channelCapacityId") in keys
    # nullable (an association, not an owner) and writable (the caller sends it) keys are not
    assert ("ChannelAllocation", "salesChannelId") not in keys
    assert ("ChannelAllocation", "venueId") not in keys


def test_a_key_named_none_or_on_no_carrying_path_is_not_required():
    ds = _load("derive_schema_t2b", "derive-schema.py")
    keys = ds.path_supplied_keys(_catalogue(channelCapacityId={"type": "string", "readOnly": True,
                                                               "x-ticvai-references": "none"}))
    assert ("ChannelAllocation", "channelCapacityId") not in keys
    cat = _catalogue()
    cat["catalogue"][1]["paths"].pop("/channel-capacities/{channelCapacityId}/channel-allocations")
    assert ("ChannelAllocation", "channelCapacityId") not in ds.path_supplied_keys(cat)


# ---- 6. two keys to one parent are a decision, not the alphabet (CR-148, CR-149) ---------------------------------

def test_two_keys_to_one_parent_are_reported_undecided_and_kept_provisionally():
    dd = _load("derive_ddl_t6", "derive-ddl.py")
    cands = [("sale_id", "retail.sale", "id"), ("new_sale_id", "retail.sale", "id")]
    pick, undecided = dd.pick_owner("retail.exchange", cands)
    assert pick == ("new_sale_id", "retail.sale", "id")      # unchanged until decided: no policy moves
    assert undecided == ["new_sale_id", "sale_id"]
    one = dd.pick_owner("retail.sale_line", [("sale_id", "retail.sale", "id")])
    assert one == (("sale_id", "retail.sale", "id"), [])
    two_parents = dd.pick_owner("x.y", [("a_id", "x.a", "id"), ("b_id", "x.b", "id")])
    assert two_parents == (None, [])


def test_the_published_answers_decide_two_of_the_two_key_tables():
    dd = _load("derive_ddl_t6b", "derive-ddl.py")
    assert dd.ROW_OWNER["fnb.ingredient_substitute"] == "from_inventory_item_id"      # CR-148
    assert dd.ROW_OWNER["ledger.inter_entity_obligation"] == "from_legal_entity_id"   # CR-149 (writes)


# ---- 7. the prevention: check-ddl-conventions reads what the generator handed the migration owner -----------------

class FakeGuard:
    def __init__(self):
        self.found = {}

    def add(self, rule, key, message, strict=False):
        self.found.setdefault(rule, {})[key] = message

    def note(self, text):
        pass


REVIEW_R6 = "\n".join([
    "| Kind | Database | Object | Change | What a person does |", "|---|---|---|---|---|",
    "| table changed | tenant | `marketing.message_dispatch` | `PARTITION BY RANGE (queued_at)` -> `(none)` | "
    "partitioning changed: a table rewrite, planned by hand |",
    "| column changed | tenant | `catalogue.channel_envelope.channel_capacity_id` | `envelope_id uuid NOT NULL` -> "
    "`channel_capacity_id uuid` | after the rename: write the ALTER COLUMN (and any data rewrite) by hand |",
    "| column changed | tenant | `identity.otp_challenge.subject_id` | `subject_id uuid NOT NULL` -> `subject_id uuid` "
    "| type, default, nullability or check changed: write the ALTER COLUMN (and any data rewrite) by hand |",
    "| after rename | tenant | `fnb.ingredient_substitute` | 2 generated object(s) for the renamed table: "
    "`ingredient_substitute_x_idx`, `SELECT platform.apply_parent_rls('fnb.ingredient_substitute'::regclass, 'from_inv` "
    "| in the forward migration that renames the table |",
    "| column dropped | tenant | `platform.workstation.org_unit_id` | no longer in the schema reference | a rename or a "
    "drop: decide, then RENAME COLUMN or the four-step drop by hand |",
    "| column dropped | tenant | `identity.role.grant_count` | no longer in the schema reference | a rename or a drop: "
    "decide, then RENAME COLUMN or the four-step drop by hand |",
    "| owner undecided | tenant | `retail.exchange` | two NOT NULL keys to retail.sale (new_sale_id, sale_id) | decide |",
])


def test_the_check_finds_every_defect_of_the_class_on_r6s_review():
    cdc = _load("check_ddl_conventions_t7", "check-ddl-conventions.py")
    guard = FakeGuard()
    cdc.check_forward_migration(
        guard, REVIEW_R6, series="CREATE TABLE platform.sale_board_tile (id uuid);",
        retired={"platform.workstation": {"org_unit_id"}},
        nullable_keys={("identity.otp_challenge", "subject_id")},
        derived={"sale_board_tile_variant_id_when_chk": "platform.sale_board_tile",
                 "sale_board_tile_sale_board_page_id_position_uniq": "platform.sale_board_tile"})
    f = guard.found
    assert set(f["D-FWD-PARTITION"]) == {"marketing.message_dispatch"}
    assert set(f["D-FWD-KEY-NULL"]) == {"catalogue.channel_envelope.channel_capacity_id"}   # otp is nullable: true
    assert set(f["D-FWD-CUT"]) == {"fnb.ingredient_substitute"}
    assert set(f["D-FWD-RETIRED"]) == {"platform.workstation.org_unit_id"}                # grant_count is not retired
    assert set(f["D-FWD-CARRIED"]) == {"sale_board_tile_variant_id_when_chk",
                                       "sale_board_tile_sale_board_page_id_position_uniq"}
    assert set(f["D-FWD-OWNER"]) == {"retail.exchange"}


def test_the_check_passes_what_the_fixed_generator_writes():
    cdc = _load("check_ddl_conventions_t7b", "check-ddl-conventions.py")
    guard = FakeGuard()
    review = "\n".join([
        "| column retired | tenant | `platform.workstation.org_unit_id` | retired by the contract | drop it |",
        "| after rename | tenant | `fnb.ingredient_substitute` | 1 generated object(s) for the renamed table: "
        "`SELECT platform.apply_parent_rls('fnb.ingredient_substitute'::regclass, 'from_inventory_item_id', "
        "'inventory.inventory_item'::regclass, 'id')` | rename |",
        "| index added after rename | tenant | `platform.sale_board_tile_sale_board_page_id_position_uniq` | new | after "
        "the RENAME COLUMN, create it: CREATE UNIQUE INDEX IF NOT EXISTS sale_board_tile_sale_board_page_id_position_uniq "
        "ON platform.sale_board_tile (sale_board_page_id, position) |"])
    series = ("ALTER TABLE platform.sale_board_tile ADD CONSTRAINT sale_board_tile_variant_id_when_chk CHECK "
              "(kind IS DISTINCT FROM 'product' OR variant_id IS NOT NULL) NOT VALID;")
    cdc.check_forward_migration(
        guard, review, series=series, retired={"platform.workstation": {"org_unit_id"}}, nullable_keys=set(),
        derived={"sale_board_tile_variant_id_when_chk": "platform.sale_board_tile",
                 "sale_board_tile_sale_board_page_id_position_uniq": "platform.sale_board_tile"})
    assert not any(guard.found.values()), guard.found


def test_a_retired_columns_guarded_statement_names_its_table_for_the_migration_ticket():
    """ticket_done.after_r1_changes reads the forward migration for the tables it changes, so the migration ticket that
    creates the table cites the file (check-migration-wording MW-AFTER-R1)."""
    import tempfile
    import ticket_done as td
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / "backend" / "tenant"
        d.mkdir(parents=True)
        (d / "V0105__after_r1_20261018.sql").write_text(
            fwd.retire_not_null("platform.workstation", "org_unit_id") + ";\n", encoding="utf-8")
        got = td.after_r1_changes(root)
    assert got == {("backend/tenant/V0105__after_r1_20261018.sql", "platform.workstation"): [("column", "org_unit_id")]}


def test_a_table_the_file_names_before_its_declared_move_is_keyed_by_its_name_now():
    """V0105 re-applies sync.dsar_request's policy as platform.dsar_request (its move is declared, not applied); the
    migration ticket lists sync.dsar_request, so the change is keyed by that name and says the name the file uses
    (check-migration-wording MW-AFTER-R1, CHG-RSF-001)."""
    import tempfile
    import ticket_done as td
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tools").mkdir()
        (root / "tools" / "derive-schema-history.py").write_text(
            'RENAMES = [{"from": "platform.dsar_request", "to": "sync.dsar_request"}]\n', encoding="utf-8")
        d = root / "backend" / "tenant"
        d.mkdir(parents=True)
        (d / "V0105__after_r1_20261018.sql").write_text(
            "SELECT platform.drop_rls_policies('platform.dsar_request'::regclass);\n"
            "SELECT platform.apply_parent_across_rls('platform.dsar_request'::regclass, 'request_id', "
            "'approvals.request'::regclass, 'id');\n", encoding="utf-8")
        got = td.after_r1_changes(root)
    assert got == {("backend/tenant/V0105__after_r1_20261018.sql", "sync.dsar_request"): [
        ("change", "named platform.dsar_request in the file, its name before the declared move"),
        ("row-level security", "apply_parent_across_rls")]}


# ---- 2, fix round 1: only what the operation itself takes or returns counts, and every key the rule adds is printed

def _queue(required=("id",)):
    return {"queue": ("satellite", {
        "paths": {
            "/queue-feeds/{feedId}/test": {"post": {"operationId": "testQueueFeed", "responses": {"200": {"content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/FeedTestResult"}}}}}}},
            "/queues/{queueId}/readings": {"get": {"operationId": "listQueueReadings", "responses": {"200": {
                "content": {"application/json": {"schema": {"type": "array", "items": {
                    "$ref": "#/components/schemas/QueueReading"}}}}}}}}},
        "components": {"schemas": {
            "FeedTestResult": {"type": "object", "properties": {
                "sample": {"$ref": "#/components/schemas/QueueReading"}}},
            "QueueReading": {"x-ticvai-persistence": "queue.reading", "type": "object", "required": list(required),
                             "properties": {
                                 "feedId": {"type": "string", "readOnly": True, "x-ticvai-references": "queue.feed"},
                                 "queueId": {"type": "string", "readOnly": True,
                                             "x-ticvai-references": "queue.queue"}}}}}})}


def test_a_matching_name_in_a_nested_sample_schema_does_not_make_a_column_not_null():
    ds = _load("derive_schema_f1", "derive-schema.py")
    keys = ds.path_supplied_keys(_queue())
    # testQueueFeed's response holds a sample reading two levels down: {feedId} does not supply the reading's feed
    assert ("QueueReading", "feedId") not in keys
    # listQueueReadings returns an array of readings at the top level: {queueId} is the path's
    assert keys[("QueueReading", "queueId")] == ("listQueueReadings", "/queues/{queueId}/readings", "queueId")


def test_the_wrapper_set_is_not_the_row_but_the_request_body_is():
    ds = _load("derive_schema_f1b", "derive-schema.py")
    cat = _catalogue()
    keys = ds.path_supplied_keys(cat)
    assert ("ChannelAllocation", "channelCapacityId") not in keys   # only inside ChannelAllocationSet.allocations
    put = cat["catalogue"][1]["paths"]["/channel-capacities/{channelCapacityId}/channel-allocations"]["put"]
    put["requestBody"] = {"content": {"application/json": {"schema": {
        "type": "array", "items": {"$ref": "#/components/schemas/ChannelAllocation"}}}}}
    assert ("ChannelAllocation", "channelCapacityId") in ds.path_supplied_keys(cat)


def test_every_key_the_rule_adds_is_printed():
    ds = _load("derive_schema_f1c", "derive-schema.py")
    keys = ds.path_supplied_keys(_queue())
    lines = ds.path_key_lines(keys, {"QueueReading": "queue.reading"},
                              lambda table, prop: {"queueId": "queue_id", "feedId": "feed_id"}[prop])
    assert len(lines) == len(keys) == 1
    assert "queue.reading.queue_id" in lines[0] and "listQueueReadings" in lines[0] and "{queueId}" in lines[0]


# ---- R8-MIG-001: renames, keys and dropped indexes are written, guarded, and a second run writes nothing -----------

REN_OLD = ("CREATE TABLE IF NOT EXISTS wallet.gift_card (id uuid PRIMARY KEY, face_value numeric(18,4), "
           "owner_id uuid, note text);\n"
           "CREATE TABLE IF NOT EXISTS wallet.owner (id uuid PRIMARY KEY);\n"
           "CREATE TABLE IF NOT EXISTS wallet.ledger_line (id uuid, gift_card_id uuid) PARTITION BY RANGE (id);\n"
           "CREATE INDEX IF NOT EXISTS gift_card_face_value_idx ON wallet.gift_card (face_value);\n"
           "CREATE INDEX IF NOT EXISTS gift_card_note_idx ON wallet.gift_card (note);\n")
REN_NEW = ("CREATE TABLE IF NOT EXISTS wallet.gift_card (id uuid PRIMARY KEY, face_value_amount numeric(18,4), "
           "owner_id uuid, note text);\n"
           "CREATE TABLE IF NOT EXISTS wallet.owner (id uuid PRIMARY KEY);\n"
           "CREATE TABLE IF NOT EXISTS wallet.ledger_line (id uuid, gift_card_id uuid) PARTITION BY RANGE (id);\n"
           "CREATE INDEX IF NOT EXISTS gift_card_face_value_amount_idx ON wallet.gift_card (face_value_amount);\n"
           "ALTER TABLE wallet.gift_card ADD CONSTRAINT gift_card_owner_id_fkey FOREIGN KEY (owner_id) "
           "REFERENCES wallet.owner(id);\n"
           "ALTER TABLE wallet.ledger_line ADD CONSTRAINT ledger_line_gift_card_id_fkey FOREIGN KEY (gift_card_id) "
           "REFERENCES wallet.gift_card(id);\n")
REN_RENAMES = {"columns": {("wallet.gift_card", "face_value_amount"): "face_value"}}
REN_RENAMES = {"columns": {("wallet.gift_card", "face_value_amount"): "face_value"}}


def test_a_pure_column_rename_is_written_guarded_and_is_not_a_review_row():
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    assert p.recon_counts["renames"] == 1
    first = p.recon[0]
    assert "DO $$ BEGIN IF EXISTS" in first and first.startswith("-- wallet.gift_card | rename column | face_value to face_value_amount") and "RENAME COLUMN face_value TO face_value_amount" in first
    assert "NOT EXISTS" in first          # does nothing when the new name is already there
    assert not rows(p, "column renamed"), p.review
    assert any("RENAME COLUMN face_value_amount TO face_value" in r for r in p.recon_rollback)


def test_the_index_on_a_renamed_column_follows_the_rename_and_comes_after_it():
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    text = "\n".join(p.recon)
    assert "ALTER INDEX wallet.gift_card_face_value_idx RENAME TO gift_card_face_value_amount_idx" in text
    assert text.index("RENAME COLUMN") < text.index("ALTER INDEX")
    assert text.index("ALTER INDEX") < text.index("ADD CONSTRAINT"), "keys after the renames they may name"


def test_a_foreign_key_is_added_not_valid_and_guarded_but_a_partitioned_table_takes_it_checked():
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    owner = [s for s in p.recon if "gift_card_owner_id_fkey" in s and "ADD CONSTRAINT" in s][0]
    assert owner.rstrip().endswith("NOT VALID; END IF; END $$") and "to_regclass('wallet.owner') IS NOT NULL" in owner
    assert "AND NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'gift_card_owner_id_fkey'" in owner
    part = [s for s in p.recon if "ledger_line_gift_card_id_fkey" in s and "ADD CONSTRAINT" in s][0]
    assert "NOT VALID" not in part, "PostgreSQL refuses NOT VALID on a partitioned table"
    assert not rows(p, "constraint added"), p.review


def test_an_index_no_longer_generated_is_dropped_guarded_and_the_rollback_makes_it_again():
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    drop = [s for s in p.recon if "DROP INDEX wallet.gift_card_note_idx" in s]
    assert drop and "to_regclass('wallet.gift_card_note_idx') IS NOT NULL" in drop[0]
    assert any("CREATE INDEX IF NOT EXISTS gift_card_note_idx" in r for r in p.recon_rollback)
    assert not rows(p, "index dropped"), p.review


def test_once_the_file_is_in_the_old_side_a_second_diff_writes_nothing():
    ren = {"columns": {("wallet.gift_card", "face_value"): "face_value_amount"}}
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), ren)
    old = model(REN_OLD)
    old.apply_forward(";\n".join(p.recon) + ";\n")
    again = fwd.diff("tenant", old, model(REN_NEW), ren)
    assert not again.recon and not again.statements, (again.recon, again.statements)
    assert not again.review, again.review


def test_a_rename_that_also_changes_the_type_stays_a_decision_for_a_person():
    new = REN_NEW.replace("face_value_amount numeric(18,4)", "face_value_amount integer")
    p = fwd.diff("tenant", model(REN_OLD), model(new), {"columns": {("wallet.gift_card", "face_value"):
                                                                      "face_value_amount"}})
    assert p.recon_counts["renames"] == 0
    assert rows(p, "column renamed"), p.review
    assert not [s for s in p.recon if "ALTER INDEX" in s], "an index follows a rename only when the rename is written"


def test_the_rendered_file_has_a_checksum_a_rollback_and_its_own_version():
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    text = fwd.render_recon(p, "V0107", "r1 (9cec72d)", "20261019")
    assert "VALUES ('V0107'" in text and "-- ROLLBACK" in text and "-- ALTER TABLE wallet.gift_card RENAME COLUMN" in text


def test_a_migration_ticket_lists_what_the_names_file_does_to_its_tables():
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as d:
        _names_ticket(Path(d))


def _names_ticket(tmp_path):
    import ticket_done as td
    (tmp_path / "backend" / "tenant").mkdir(parents=True)
    p = fwd.diff("tenant", model(REN_OLD), model(REN_NEW), {"columns": {("wallet.gift_card", "face_value"):
                                                                          "face_value_amount"}})
    f = tmp_path / "backend" / "tenant" / "V0107__names_after_r1_20261019.sql"
    f.write_text(fwd.render_recon(p, "V0107", "r1", "20261019"), encoding="utf-8")
    ch = td.after_r1_changes(tmp_path)
    rel = "backend/tenant/V0107__names_after_r1_20261019.sql"
    assert ("rename column", "face_value to face_value_amount") in ch[(rel, "wallet.gift_card")]
    # a key is on the child's ticket and on its parent's
    assert any(k == "foreign key" for k, _ in ch[(rel, "wallet.owner")])
    text = td.names_sentence(rel, {"wallet.gift_card": ch[(rel, "wallet.gift_card")]})
    assert text.startswith(f"Source DDL after r1: {rel}") and "rename column face_value to face_value_amount" in text


# ---- R8 second round: a column the contract makes optional (CHG-R8MIG-004) ----------------------------------------

AR_OLD = ("CREATE TABLE IF NOT EXISTS platform.audit_read (id uuid PRIMARY KEY NOT NULL, principal_id uuid NOT NULL, "
          "subject_id uuid NOT NULL);\n")
AR_NEW = ("CREATE TABLE IF NOT EXISTS platform.audit_read (id uuid PRIMARY KEY NOT NULL, principal_id uuid NOT NULL, "
          "subject_id uuid);\n")


def test_a_column_the_contract_makes_optional_loses_not_null_guarded_and_once():
    p = fwd.diff("tenant", model(AR_OLD), model(AR_NEW))
    stmt = [s for s in p.statements if "DROP NOT NULL" in s]
    assert len(stmt) == 1 and "'subject_id'" in stmt[0] and "information_schema.columns" in stmt[0]
    assert any("SET NOT NULL" in r and "subject_id" in r for r in p.rollback)
    assert not [r for r in p.review if r[0] == "column changed"], p.review
    again = fwd.diff("tenant", fold(AR_OLD, p), model(AR_NEW))
    assert not again.statements and not again.review, (again.statements, again.review)


def test_a_type_change_with_the_not_null_dropped_is_still_a_decision():
    new = AR_NEW.replace("subject_id uuid", "subject_id text")
    p = fwd.diff("tenant", model(AR_OLD), model(new))
    assert not [s for s in p.statements if "DROP NOT NULL" in s]
    assert [r for r in p.review if r[0] == "column changed"]


CH_OLD = ("CREATE TABLE IF NOT EXISTS control.tenant_domain (id uuid PRIMARY KEY NOT NULL, channel text CONSTRAINT "
          "tenant_domain_channel_chk CHECK (channel IN ('guestWeb', 'backOffice')));\n")
CH_NEW = CH_OLD.replace("'backOffice')", "'backOffice', 'staffApp')")


def test_a_column_check_that_only_gains_values_is_written_not_valid_then_validated_once():
    p = fwd.diff("control", model(CH_OLD), model(CH_NEW))
    body = ran(p.statements)
    assert any("DROP CONSTRAINT IF EXISTS tenant_domain_channel_chk" in s for s in body), body
    add = [s for s in body if " ADD CONSTRAINT tenant_domain_channel_chk" in s]
    assert add and "'staffApp'" in add[0] and add[0].endswith("NOT VALID")
    assert any("VALIDATE CONSTRAINT tenant_domain_channel_chk" in s for s in body)
    assert not [r for r in p.review if r[0] == "column changed"], p.review
    again = fwd.diff("control", fold(CH_OLD, p), model(CH_NEW))
    assert not again.statements and not again.review, (again.statements, again.review)


def test_a_column_check_that_loses_a_value_is_added_not_valid_and_left_to_validate():
    p = fwd.diff("control", model(CH_NEW), model(CH_OLD))
    assert not [s for s in p.statements if "VALIDATE CONSTRAINT tenant_domain_channel_chk" in s]
    assert [r for r in p.review if r[0] == "column changed" and "VALIDATE CONSTRAINT" in r[3]]


PSG = ("CREATE TABLE IF NOT EXISTS identity.principal (id uuid PRIMARY KEY NOT NULL);\n"
       "CREATE TABLE IF NOT EXISTS identity.platform_staff_grant (id uuid PRIMARY KEY NOT NULL, "
       "operator_principal_id uuid NOT NULL);\n")
PSG_FK = ("ALTER TABLE identity.platform_staff_grant ADD CONSTRAINT platform_staff_grant_operator_principal_id_fkey "
          "FOREIGN KEY (operator_principal_id) REFERENCES identity.principal(id);\n")


def test_a_foreign_key_the_contract_withdraws_is_dropped_guarded_in_the_names_file():
    p = fwd.diff("tenant", model(PSG + PSG_FK), model(PSG))
    drop = [s for s in p.recon if "DROP CONSTRAINT platform_staff_grant_operator_principal_id_fkey" in s]
    assert drop and "pg_constraint" in drop[0] and "| drop foreign key |" in drop[0]
    assert any("ADD CONSTRAINT platform_staff_grant_operator_principal_id_fkey" in r for r in p.recon_rollback)
    assert not [r for r in p.review if r[0] == "constraint dropped"], p.review
    folded = model(PSG + PSG_FK)
    folded.apply_forward(";\n".join(s.split("\n", 1)[1] for s in p.recon) + ";\n")
    again = fwd.diff("tenant", folded, model(PSG))
    assert not again.recon and not again.review, (again.recon, again.review)


AP_OLD = ("CREATE TABLE IF NOT EXISTS access.access_area (id uuid PRIMARY KEY NOT NULL);\n"
          "CREATE TABLE IF NOT EXISTS access.access_point (id uuid PRIMARY KEY NOT NULL);\n")
AP_NEW = ("CREATE TABLE IF NOT EXISTS access.access_area (id uuid PRIMARY KEY NOT NULL);\n"
          "CREATE TABLE IF NOT EXISTS access.access_point (id uuid PRIMARY KEY NOT NULL, zone_id uuid);\n"
          "ALTER TABLE access.access_point ADD CONSTRAINT access_point_zone_id_fkey FOREIGN KEY (zone_id) "
          "REFERENCES access.access_area(id);\n")


def test_a_key_on_a_new_column_is_added_guarded_so_the_file_applies_twice():
    p = fwd.diff("tenant", model(AP_OLD), model(AP_NEW))
    fk = [s for s in p.statements if "access_point_zone_id_fkey" in s]
    # guarded on both tables, the key's column and the key not being there yet (CHG-R8MIG-010, CHG-R9MIG-002)
    assert len(fk) == 1 and fk[0].startswith("DO $$ BEGIN IF to_regclass(")
    assert "NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'access_point_zone_id_fkey'" in fk[0]
    assert "NOT VALID" not in fk[0]
    again = fwd.diff("tenant", fold(AP_OLD, p), model(AP_NEW))
    assert not again.statements and not again.review, (again.statements, again.review)


CB_OLD = "CREATE TABLE IF NOT EXISTS marketing.customer_badge (id uuid PRIMARY KEY NOT NULL, status text);\n"
CB_NEW = ("CREATE TABLE IF NOT EXISTS marketing.customer_badge (id uuid PRIMARY KEY NOT NULL, status text CONSTRAINT "
          "customer_badge_status_chk CHECK (status IN ('awarded', 'expired', 'revoked')));\n")


def test_a_check_added_to_an_existing_column_is_written_not_valid_and_validation_is_a_review_row():
    p = fwd.diff("tenant", model(CB_OLD), model(CB_NEW))
    add = [s for s in ran(p.statements) if "ADD CONSTRAINT customer_badge_status_chk" in s]
    assert add and add[0].endswith("NOT VALID")
    assert not [s for s in p.statements if "VALIDATE" in s]
    assert [r for r in p.review if r[0] == "column changed" and "VALIDATE CONSTRAINT" in r[3] and "NOT VALID" in r[2]]
    again = fwd.diff("tenant", fold(CB_OLD, p), model(CB_NEW))
    assert not again.statements and not again.review, (again.statements, again.review)


def test_a_narrowed_check_is_written_not_valid_too():
    narrow = CB_NEW.replace(", 'revoked'", "")
    p = fwd.diff("tenant", model(CB_NEW), model(narrow))
    assert [s for s in p.statements if "ADD CONSTRAINT customer_badge_status_chk" in s and "'revoked'" not in s]
    assert [r for r in p.review if r[0] == "column changed" and "VALIDATE CONSTRAINT" in r[3]]


CP_OLD = ("CREATE TABLE IF NOT EXISTS platform.configuration_profile (id uuid PRIMARY KEY NOT NULL, "
          "version integer NOT NULL);\n")
CP_NEW = ("CREATE TABLE IF NOT EXISTS platform.configuration_profile (id uuid NOT NULL, version integer NOT NULL, "
          "CONSTRAINT configuration_profile_pkey PRIMARY KEY (id, version));\n")


def test_a_column_a_new_composite_key_covers_is_not_relaxed():
    p = fwd.diff("tenant", model(CP_OLD), model(CP_NEW))
    assert not [s for s in p.statements if "DROP NOT NULL" in s], p.statements
    assert not [r for r in p.review if r[1] == "platform.configuration_profile.version"], p.review
    assert [r for r in p.review if r[0] == "constraint added" and "PRIMARY KEY (id, version)" in r[2]]


# ---- declared renames written (CHG-R8WFM-001, r8 sample walk) -------------------------------------------------------

WFM_OLD = ("CREATE TABLE IF NOT EXISTS wallet.hold (id uuid PRIMARY KEY, wallet_hold_amount numeric(18,4) NOT NULL, "
           "status text NOT NULL CONSTRAINT hold_status_chk CHECK (status IN ('held', 'released')));\n"
           "CREATE INDEX IF NOT EXISTS hold_status_idx ON wallet.hold (status);\n"
           "SELECT platform.apply_tenant_rls('wallet.hold'::regclass);\n")
WFM_NEW = ("CREATE TABLE IF NOT EXISTS wallet.fund_reservation (id uuid PRIMARY KEY, reserved_amount numeric(18,4) NOT NULL, "
           "status text NOT NULL CONSTRAINT fund_reservation_status_chk CHECK (status IN ('held', 'released', 'sold')));\n"
           "CREATE INDEX IF NOT EXISTS fund_reservation_status_idx ON wallet.fund_reservation (status);\n"
           "SELECT platform.apply_tenant_rls('wallet.fund_reservation'::regclass);\n")
WFM_REN = {"tables": {"wallet.hold": "wallet.fund_reservation"},
       "columns": {("wallet.fund_reservation", "wallet_hold_amount"): "reserved_amount"}}


def test_a_declared_table_rename_is_written_with_its_names_guarded():
    items = fwd.declared_rename_items(model(WFM_OLD), model(WFM_NEW), WFM_REN)
    kinds = [(i["kind"], i["stmt"].splitlines()[0]) for i in items]
    assert kinds[0] == ("rename table", "-- wallet.fund_reservation | rename table | wallet.hold to fund_reservation")
    body = "\n".join(i["stmt"] for i in items)
    assert "to_regclass('wallet.hold') IS NOT NULL AND to_regclass('wallet.fund_reservation') IS NULL" in body
    assert "RENAME COLUMN wallet_hold_amount TO reserved_amount" in body
    assert "ALTER INDEX wallet.hold_status_idx RENAME TO fund_reservation_status_idx" in body
    assert "RENAME CONSTRAINT hold_status_chk TO fund_reservation_status_chk" in body
    assert "RENAME CONSTRAINT hold_pkey TO fund_reservation_pkey" in body
    assert any(i["kind"] == "rename policy" for i in items)


def test_once_the_early_file_is_folded_the_diff_sees_one_table_and_widens_its_check():
    items = fwd.declared_rename_items(model(WFM_OLD), model(WFM_NEW), WFM_REN)
    early = fwd.render_recon(fwd.early_plan("tenant", items), "V0103a", "r1", "20261020", before="V0104__x.sql", rest="V0109")
    old = model(WFM_OLD)
    old.apply_forward(early)
    assert fwd.declared_rename_items(old, model(WFM_NEW), WFM_REN) == []
    p = fwd.diff("tenant", old, model(WFM_NEW), WFM_REN)
    assert not [r for r in p.review if r[0] in ("table renamed", "after rename", "table dropped")]
    assert any("fund_reservation_status_chk CHECK (status IN ('held', 'released', 'sold')) NOT VALID" in s
               for s in p.statements)
    assert not p.recon


def test_a_move_runs_after_the_last_frozen_file_that_names_its_old_name():
    old = model("CREATE TABLE IF NOT EXISTS platform.dsar_request (id uuid PRIMARY KEY);\n")
    new = model("CREATE TABLE IF NOT EXISTS sync.dsar_request (id uuid PRIMARY KEY);\n")
    items = fwd.declared_rename_items(old, new, {"tables": {"platform.dsar_request": "sync.dsar_request"}})
    assert items[0]["kind"] == "move table"
    frozen = {"V0103__a.sql": "SELECT 1;", "V0104__b.sql": "SELECT 1;",
              "V0105__c.sql": "SELECT platform.drop_rls_policies('platform.dsar_request'::regclass);",
              "V0107__d.sql": "SELECT 1;"}
    placed, unplaced = fwd.place_renames(items, frozen, {"V0103", "V0104", "V0105", "V0107"})
    assert not unplaced and all(after >= "V0105__c.sql" for after, _ in placed.values())
    frozen["V0104__b.sql"] = "SELECT platform.apply_parent_rls('x.y'::regclass, 'new_col', 'x.z'::regclass, 'id');"
    other = {"group": ("column", "x.y", "new_col"), "kind": "rename column", "stmt": "-- x.y | rename column | a to new_col SELECT 1",
             "back": "", "olds": [], "news": [__import__("re").compile(r"'x\.y'::regclass, 'new_col'")]}
    placed, unplaced = fwd.place_renames(items + [other], frozen, {"V0103", "V0104", "V0105", "V0107"})
    assert sorted(placed) == ["V0103a", "V0105a"] and not unplaced


def test_a_rename_both_a_later_and_an_earlier_frozen_file_need_is_not_placed():
    old = model("CREATE TABLE IF NOT EXISTS wallet.hold (id uuid PRIMARY KEY);\n")
    new = model("CREATE TABLE IF NOT EXISTS wallet.fund_reservation (id uuid PRIMARY KEY);\n")
    items = fwd.declared_rename_items(old, new, {"tables": {"wallet.hold": "wallet.fund_reservation"}})
    frozen = {"V0104__a.sql": "SELECT platform.apply_tenant_rls('wallet.fund_reservation'::regclass);",
              "V0105__b.sql": "SELECT platform.apply_tenant_rls('wallet.hold'::regclass);"}
    placed, unplaced = fwd.place_renames(items, frozen, set())
    assert not placed and unplaced


# ---- CHG-R9MIG-001: a table that takes no scope loses the one a forward migration gave it (ADAM CR-166) -------------

OS_OLD = ("CREATE TABLE IF NOT EXISTS platform.outbox_sequence (aggregate_id uuid PRIMARY KEY NOT NULL, "
          "last_sequence bigint NOT NULL, scope_path ltree NOT NULL);\n"
          "CREATE INDEX IF NOT EXISTS outbox_sequence_scope_path_idx ON platform.outbox_sequence USING gist "
          "(scope_path);\n"
          "SELECT platform.apply_scope_rls('platform.outbox_sequence'::regclass);\n")
ANY = "'cardinality(platform.current_scope_paths()) > 0'"
OS_NEW = ("CREATE TABLE IF NOT EXISTS platform.outbox_sequence (aggregate_id uuid PRIMARY KEY NOT NULL, "
          "last_sequence bigint NOT NULL);\n"
          f"SELECT platform.apply_split_rls('platform.outbox_sequence'::regclass, {ANY}, {ANY});\n"
          "DROP POLICY IF EXISTS outbox_sequence_delete ON platform.outbox_sequence;\n")
OS = {"platform.outbox_sequence"}


def test_a_declared_unscoped_table_loses_its_scope_in_one_block_guarded_on_the_column():
    p = fwd.diff("tenant", model(OS_OLD), model(OS_NEW), descoped=OS)
    assert len(p.statements) == 1, p.statements
    block = p.statements[0]
    assert "| scope removed |" in block
    assert ("DO $$ BEGIN IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'platform' AND "
            "table_name = 'outbox_sequence' AND column_name = 'scope_path') THEN") in block
    assert ran(p.statements) == [
        "SELECT platform.drop_rls_policies('platform.outbox_sequence'::regclass)",
        "DROP INDEX IF EXISTS platform.outbox_sequence_scope_path_idx",
        "ALTER TABLE platform.outbox_sequence DROP COLUMN IF EXISTS scope_path",
        f"SELECT platform.apply_split_rls('platform.outbox_sequence'::regclass, {ANY}, {ANY})",
        "DROP POLICY IF EXISTS outbox_sequence_delete ON platform.outbox_sequence"]
    assert not p.review and not p.recon, (p.review, p.recon)
    assert any("ADD COLUMN IF NOT EXISTS scope_path ltree" in r and "apply_scope_rls" in r for r in p.rollback)
    # folded, the next run writes nothing and lists nothing (regenerate-twice)
    again = fwd.diff("tenant", fold(OS_OLD, p), model(OS_NEW), descoped=OS)
    assert not again.statements and not again.review and not again.recon, (again.statements, again.review)


def test_a_scope_path_dropped_without_the_declaration_is_still_a_decision():
    p = fwd.diff("tenant", model(OS_OLD), model(OS_NEW))
    assert [r for r in p.review if r[0] == "column dropped" and r[1] == "platform.outbox_sequence.scope_path"]
    assert not [s for s in p.statements if "DROP COLUMN" in s]


def test_the_rendered_descope_file_says_what_it_does_and_is_the_same_every_run():
    p = fwd.diff("tenant", model(OS_OLD), model(OS_NEW), descoped=OS)
    q = fwd.diff("tenant", model(OS_OLD), model(OS_NEW), descoped=OS)
    a, b = fwd.render(p, "V0113", "r1 (x)", "20261021"), fwd.render(q, "V0113", "r1 (x)", "20261021")
    assert a == b
    assert "x-ticvai-scope: none" in a and "CHG-R9MIG-002" in a


def test_derive_ddl_reads_the_scope_mark_and_the_counter_policy_mark():
    dd = _load("derive_ddl_r9", "derive-ddl.py")
    assert "any-grant-no-delete" in dd.RLS_MARKS
    dd.SCHEMA_MARKS.clear()
    dd.SCHEMA_MARKS["platform-ops.OutboxSequence"] = {"x-ticvai-scope": "none", "x-ticvai-rls": "any-grant-no-delete"}
    cols = {"platform.outbox_sequence": [
        {"column": "aggregate_id", "source": "platform-ops.OutboxSequence.aggregateId"},
        {"column": "last_sequence", "source": "platform-ops.OutboxSequence.lastSequence"}]}
    marks = dd.table_marks(cols, ["platform.outbox_sequence"])
    assert marks["platform.outbox_sequence"]["scope"] == "none"
    assert marks["platform.outbox_sequence"]["rls"] == "any-grant-no-delete"


# ---- CHG-R9MIG-002: every statement guarded, so no file needs a hand retry --------------------------------------------

PE_OLD = ("CREATE TABLE IF NOT EXISTS marketing.privacy_exception (id uuid PRIMARY KEY NOT NULL, system text CONSTRAINT "
          "privacy_exception_system_chk CHECK (system IN ('core', 'ticketing')));\n"
          "CREATE TABLE IF NOT EXISTS orders.cart (id uuid PRIMARY KEY NOT NULL, venue_id uuid NOT NULL);\n"
          "CREATE TABLE IF NOT EXISTS platform.scope (id uuid PRIMARY KEY NOT NULL);\n"
          "CREATE TABLE IF NOT EXISTS control.onboarding_application (id uuid PRIMARY KEY NOT NULL, status text);\n"
          "SELECT platform.apply_venue_rls('orders.cart'::regclass);\n")
PE_NEW = ("CREATE TABLE IF NOT EXISTS marketing.privacy_exception (id uuid PRIMARY KEY NOT NULL, system text CONSTRAINT "
          "privacy_exception_system_chk CHECK (system IN ('core', 'ticketing', 'access')));\n"
          "CREATE TABLE IF NOT EXISTS orders.cart (id uuid PRIMARY KEY NOT NULL, venue_id uuid NOT NULL, "
          "scope_path ltree NOT NULL, session_id uuid);\n"
          "CREATE TABLE IF NOT EXISTS platform.scope (id uuid PRIMARY KEY NOT NULL);\n"
          "CREATE TABLE IF NOT EXISTS control.onboarding_application (id uuid PRIMARY KEY NOT NULL, status text);\n"
          "CREATE INDEX IF NOT EXISTS onboarding_application_status_idx ON control.onboarding_application (status);\n"
          "ALTER TABLE orders.cart ADD CONSTRAINT cart_session_id_fkey FOREIGN KEY (session_id) REFERENCES "
          "platform.scope (id);\n"
          "SELECT platform.apply_scope_rls('orders.cart'::regclass);\n")


def test_every_statement_that_needs_a_table_is_guarded_on_it_and_on_the_columns_it_names():
    p = fwd.diff("tenant", model(PE_OLD), model(PE_NEW))
    assert p.statements
    for s in p.statements:
        assert s.startswith("DO $$ BEGIN IF "), s
        assert s.count("\n") >= 2, s                     # the statement on a line of its own
    text = "\n".join(p.statements)
    # the widened CHECK: its DROP, ADD and VALIDATE all take the table and the column
    chk = [s for s in p.statements if "privacy_exception_system_chk" in s]
    assert len(chk) == 3 and all("to_regclass('marketing.privacy_exception') IS NOT NULL" in s
                                 and "column_name = 'system'" in s for s in chk), chk
    # the new column: its table
    add = [s for s in p.statements if "ADD COLUMN IF NOT EXISTS session_id" in s]
    assert add and "to_regclass('orders.cart') IS NOT NULL" in add[0]
    # the index on a table a database may not have yet (control V0110's): the table and its column
    idx = [s for s in p.statements if "onboarding_application_status_idx" in s]
    assert idx and "to_regclass('control.onboarding_application') IS NOT NULL" in idx[0] \
        and "column_name = 'status'" in idx[0]
    # the key: both tables, its column, and the key not there yet
    fk = [s for s in p.statements if "cart_session_id_fkey" in s]
    assert fk and "to_regclass('platform.scope') IS NOT NULL" in fk[0] and "column_name = 'session_id'" in fk[0] \
        and "NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'cart_session_id_fkey'" in fk[0]
    # the policy change is one block: dropped and applied together, and only where scope_path is there
    pol = [s for s in p.statements if "drop_rls_policies('orders.cart'" in s]
    assert len(pol) == 1 and "PERFORM platform.apply_scope_rls('orders.cart'::regclass);" in pol[0] \
        and "column_name = 'scope_path'" in pol[0], pol
    assert "SELECT platform." not in text                # a SELECT inside a DO block is written PERFORM


def test_guarded_statements_fold_back_so_the_next_run_writes_nothing():
    p = fwd.diff("tenant", model(PE_OLD), model(PE_NEW))
    again = fwd.diff("tenant", fold(PE_OLD, p), model(PE_NEW))
    assert not again.statements, again.statements


def test_a_guarded_policy_call_is_read_where_its_table_is_named():
    """ticket_done reads the call on its own line (PERFORM), so the migration ticket still cites the file; and
    check-rls-scope-fit reads it through unguard."""
    import tempfile
    import ticket_done as td
    p = fwd.diff("tenant", model(PE_OLD), model(PE_NEW))
    pol = [s for s in p.statements if "drop_rls_policies('orders.cart'" in s][0]
    assert [x for x in fwd.unguard(pol) if x.startswith("SELECT platform.apply_scope_rls('orders.cart'")]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        d = root / "backend" / "tenant"
        d.mkdir(parents=True)
        (d / "V0113__after_r1_20261021.sql").write_text(pol + ";\n", encoding="utf-8")
        got = td.after_r1_changes(root)
    assert got == {("backend/tenant/V0113__after_r1_20261021.sql", "orders.cart"): [
        ("row-level security", "apply_scope_rls")]}


def test_check_migrations_lets_only_the_descope_blocks_drop_column_through():
    """check-migrations refuses DROP COLUMN in a body (the four-step drop), but not the generated descope block of a
    table whose contract says x-ticvai-scope: none (CHG-R9MIG-001)."""
    cm = _load("check_migrations_r9", "check-migrations.py")
    cm._CACHE["_scope_none"] = {"platform.outbox_sequence"}
    p = fwd.diff("tenant", model(OS_OLD), model(OS_NEW), descoped=OS)
    code = cm.strip_comments(fwd.render(p, "V0113", "r1", "x").split("-- ROLLBACK")[0])
    assert cm.descope_drops(code) == {("platform.outbox_sequence", "scope_path")}
    assert not cm.descope_drops(code.replace("column_name = 'scope_path'", "column_name = 'other'"))
    cm._CACHE["_scope_none"] = set()
    assert not cm.descope_drops(code)
