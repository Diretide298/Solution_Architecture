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
