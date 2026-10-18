"""Tests for platform.parent_visible in tools/derive-ddl.py (ADAM CR-108; CHG-RSF-001).

    python -m pytest ticvai/tools/tests/test_parent_visible_generator.py -q

Decision D5 as the lead ruled it (18 October): the function does not refuse to answer at run time when its owner
bypasses row security (local and test databases are migrated as postgres). The migration gives it a dedicated owner
that does not, where the migration may create one; tools/tests/test_parent_visible_pg.py checks the owner.
"""
import importlib.util
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ddl", TOOLS / "derive-ddl.py")
ddl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ddl)

WRITE = "platform.in_scope(parent_row.scope_path)"


def test_one_branch_per_parent_and_a_write_branch_only_for_split_parents():
    sql = ddl.parent_visible_sql({"platform.outlet": None, "approvals.matrix": WRITE})
    # public is on the path because ltree lives there (001-extensions.sql); without it in_scope fails inside
    assert "SECURITY DEFINER" in sql and "SET search_path = pg_catalog, public, pg_temp" in sql
    assert "IF parent = 'platform.outlet'::regclass THEN" in sql
    assert "IF parent = 'approvals.matrix'::regclass THEN" in sql
    assert sql.count("IF for_write THEN") == 1
    assert f"parent_row.id = key_value AND ({WRITE})" in sql
    assert "is not a parent a policy names" in sql
    # D5 as ruled: no refusal at run time; a dedicated owner that does not bypass row security instead
    assert "bypasses row-level security, so every child row" not in sql
    assert "CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS" in sql
    assert "OWNER TO ticvai_parent_visible" in sql


def test_reserved_words_are_quoted():
    sql = ddl.parent_visible_sql({"marketing.case": None})
    assert "IF parent = 'marketing.\"case\"'::regclass THEN" in sql
    assert "FROM marketing.\"case\" parent_row" in sql


def test_parents_of_collects_each_parent_once_with_its_write_check():
    got = ddl.parents_of([("a.c", "p_id", "a.p", "id"), ("a.d", "p_id", "a.p", "id"),
                          ("a.e", "m_id", "a.m", "id", WRITE)])
    assert got == {"a.p": None, "a.m": WRITE}


def test_two_write_checks_for_one_parent_are_refused():
    with pytest.raises(ValueError):
        ddl.parents_of([("a.c", "m_id", "a.m", "id", "x"), ("a.d", "m_id", "a.m", "id", "y")])


def test_a_parent_keyed_other_than_by_id_is_refused():
    with pytest.raises(ValueError):
        ddl.parents_of([("a.c", "p_code", "a.p", "code")])


def test_the_helpers_ask_the_function_and_never_read_the_parent_themselves():
    out = ddl.rls_file("tenant", [], [], [("fnb.menu", "outlet_id", "platform.outlet", "id")], [], 1, False)
    assert "CREATE OR REPLACE FUNCTION platform.parent_visible(" in out
    assert "IF parent = 'platform.outlet'::regclass THEN" in out
    assert "platform.parent_visible(%L::regclass, %I)" in out
    assert "EXISTS (SELECT 1 FROM %s parent_row" not in out
    assert "PERFORM platform.parent_visible_owner(parent);" in ddl.RLS_PARENT
    assert "SELECT platform.apply_parent_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');" \
        in out


def test_split_children_write_through_the_function():
    assert "platform.parent_visible(%L::regclass, %I, true)" in ddl.RLS_SPLIT
    assert "parent_row WHERE %s AND (%s)" not in ddl.RLS_SPLIT
    assert "PERFORM platform.parent_visible_owner(parent);" in ddl.RLS_SPLIT
