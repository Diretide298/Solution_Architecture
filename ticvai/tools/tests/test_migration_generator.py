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
    body = [fwd.norm(s) for s in p.statements]
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


def test_a_new_unique_index_on_a_renamed_column_is_listed_whole_to_create_after_the_rename():
    p = fwd.diff("tenant", model(TILE_OLD), model(TILE_NEW), TILE_RENAMES)
    uniq = [r for r in p.review if "sale_board_page_id_position_uniq" in r[1]]
    assert uniq and uniq[0][0] == "index added after rename", p.review
    assert "CREATE UNIQUE INDEX IF NOT EXISTS sale_board_tile_sale_board_page_id_position_uniq" in uniq[0][3]
    assert "(sale_board_page_id, position)" in uniq[0][3]
    # the index that replaces an old one is still a rename
    idx = [r for r in p.review if r[1].endswith("sale_board_tile_sale_board_page_id_idx")]
    assert idx and idx[0][0] == "index after rename"


def test_a_table_check_naming_a_renamed_column_waits_for_the_rename_whole():
    chk = "CONSTRAINT sale_board_tile_sale_board_page_id_when_chk CHECK (kind IS DISTINCT FROM 'x' OR " \
          "sale_board_page_id IS NOT NULL)"
    new = TILE_NEW.replace(CHK, CHK + ",\n    " + chk)
    p = fwd.diff("tenant", model(TILE_OLD), model(new), TILE_RENAMES)
    assert not [s for s in p.statements if "sale_board_page_id_when_chk" in s]
    row = [r for r in p.review if "sale_board_page_id_when_chk" in r[2] or "sale_board_page_id_when_chk" in r[3]]
    assert row and row[0][0] == "constraint after rename" and "IS NOT NULL" in row[0][3]
