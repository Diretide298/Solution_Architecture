"""Tests for the contract marks derive-ddl reads for today's CR answers (18 October 2026, lane H).

    python -m pytest ticvai/tools/tests/test_cr_answers_generator.py -q

Synthetic only: a schema's marks and a table's columns in memory, the SQL the generator writes for them. The real
package is checked by running `tools/derive-ddl.py` and reading the forward migration (the change entries say what
it held).

- `x-ticvai-exactly-one-of` (ADAM CR-158; CHG-CRA-002): a grant names exactly one of a permission or a role.
"""
import importlib.util
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("derive_ddl", TOOLS / "derive-ddl.py")
ddl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ddl)


def _cols(table, schema, props):
    return {table: [{"column": col, "source": f"{schema}.{prop}"} for prop, col in props.items()]}


def _marks(schema, marks, cols, table):
    ddl.SCHEMA_MARKS.clear()
    ddl.SCHEMA_MARKS[schema] = marks
    return ddl.table_marks(cols, [table]).get(table) or {}


def test_exactly_one_of_names_columns():
    cols = _cols("identity.delegated_access", "identity.DelegatedAccess",
                 {"id": "id", "permission": "permission", "roleId": "role_id"})
    entry = _marks("identity.DelegatedAccess", {"x-ticvai-exactly-one-of": [["permission", "roleId"]]},
                   cols, "identity.delegated_access")
    assert entry.get("exactly_one_of") == [["permission", "role_id"]]


def test_exactly_one_of_unknown_property_is_marked_missing():
    cols = _cols("identity.delegated_access", "identity.DelegatedAccess", {"id": "id", "permission": "permission"})
    entry = _marks("identity.DelegatedAccess", {"x-ticvai-exactly-one-of": [["permission", "roleId"]]},
                   cols, "identity.delegated_access")
    assert entry.get("exactly_one_of") == [["permission", "?roleId"]]


def test_exactly_one_of_check_sql():
    line = ddl.exactly_one_sql("delegated_access", ["permission", "role_id"])
    assert line.strip() == ("CONSTRAINT delegated_access_permission_role_id_one_chk CHECK "
                            "(num_nonnulls(permission, role_id) = 1)")
