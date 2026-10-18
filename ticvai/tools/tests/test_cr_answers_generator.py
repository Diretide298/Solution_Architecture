"""Tests for the contract marks derive-ddl reads for today's CR answers (18 October 2026, lane H).

    python -m pytest ticvai/tools/tests/test_cr_answers_generator.py -q

Synthetic only: a schema's marks and a table's columns in memory, the SQL the generator writes for them. The real
package is checked by running `tools/derive-ddl.py` and reading the forward migration (the change entries say what
it held).

- `x-ticvai-exactly-one-of` (ADAM CR-158; CHG-CRA-002): a grant names exactly one of a permission or a role.
- `x-ticvai-index` (ADAM CR-165, CR-166; CHG-CRA-004): a plain index over the columns the contract names.
- `x-ticvai-unique-when` (ADAM CR-154; CHG-CRA-004): a partial unique index, one current version per tenant.
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


# - `x-ticvai-index` (ADAM CR-165, CR-166; CHG-CRA-004): a plain index the contract names.
# - `x-ticvai-unique-when` (ADAM CR-154; CHG-CRA-004): one current version per tenant, a partial unique index.

def test_index_names_columns_and_sql():
    cols = _cols("platform.outbox", "platform-ops.OutboxEntry",
                 {"id": "id", "aggregateId": "aggregate_id", "sequence": "sequence"})
    entry = _marks("platform-ops.OutboxEntry", {"x-ticvai-index": [["aggregateId", "sequence"]]}, cols, "platform.outbox")
    assert entry.get("index") == [["aggregate_id", "sequence"]]
    sql = ddl.index_sql("platform", "outbox", "platform.outbox", ["aggregate_id", "sequence"])
    assert sql.splitlines()[-1] == ("CREATE INDEX IF NOT EXISTS outbox_aggregate_id_sequence_idx "
                                    "ON platform.outbox (aggregate_id, sequence);")


def test_unique_when_names_columns_and_sql():
    cols = _cols("whitelabel.config_version", "white-label.ConfigVersion",
                 {"version": "version", "isCurrent": "is_current", "scopePath": "scope_path"})
    entry = _marks("white-label.ConfigVersion",
                   {"x-ticvai-unique-when": [{"columns": ["scopePath"], "when": {"isCurrent": True}}]},
                   cols, "whitelabel.config_version")
    assert entry.get("unique_when") == [(["scope_path"], {"is_current": True})]
    sql = ddl.unique_when_sql("whitelabel", "config_version", "whitelabel.config_version", ["scope_path"],
                              {"is_current": True}, ["scope_path"])
    assert sql.splitlines()[-1] == ("CREATE UNIQUE INDEX IF NOT EXISTS config_version_scope_path_uniq "
                                    "ON whitelabel.config_version (scope_path) WHERE is_current;")


# - tools/derive-release-flags.py (ADAM CR-164; CHG-CRA-005): the map reads each screen's operations.
_spec_rf = importlib.util.spec_from_file_location("derive_release_flags", TOOLS / "derive-release-flags.py")
rf = importlib.util.module_from_spec(_spec_rf)
_spec_rf.loader.exec_module(rf)


def test_release_flags_reads_the_screens_operations(tmp_path):
    (tmp_path / "P99-test.yaml").write_text(
        "platform: P99\nscreens:\n- id: TST-001\n  apis:\n  - operationId: getThing\n    trigger: onLoad\n"
        "  - operationId: setThing\n    trigger: onAction\n- id: TST-002\n  apis: []\n", encoding="utf-8")
    ops = rf.screen_ops_of(tmp_path)
    assert ops == {"TST-001": ["getThing", "setThing"], "TST-002": []}


def test_release_flags_map_of_the_package_has_screen_operations():
    ops = rf.screen_ops_of(TOOLS.parent / "screens")
    assert "storePaymentToken" in ops.get("WEB-021", [])
