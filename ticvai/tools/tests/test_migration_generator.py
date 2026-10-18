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
