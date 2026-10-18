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


# **Only a parent in another deployable is asked through the function** (decision D9 as the lead ruled it, 18 October
# 2026): the per-row call measured far more than twice the r6 check on 100,000 rows, so a child whose parent is in
# its own deployable keeps r6's EXISTS, which its host's grants can read.
BY_PARENT = [("fnb.menu", "outlet_id", "platform.outlet", "id"), ("fnb.menu_section", "menu_id", "fnb.menu", "id")]


def test_a_child_across_deployables_asks_the_function_and_one_within_keeps_the_r6_check():
    out = ddl.rls_file("tenant", [], [], BY_PARENT, [], 2, False, across={"fnb.menu"})
    assert "CREATE OR REPLACE FUNCTION platform.parent_visible(" in out
    assert "IF parent = 'platform.outlet'::regclass THEN" in out
    assert "IF parent = 'fnb.menu'::regclass THEN" not in out           # only the parents across are answered
    assert ("SELECT platform.apply_parent_across_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, "
            "'id');") in out
    assert ("SELECT platform.apply_parent_rls('fnb.menu_section'::regclass, 'menu_id', 'fnb.menu'::regclass, "
            "'id');") in out
    assert "PERFORM platform.parent_visible_owner(parent);" in out


def test_the_r6_helpers_are_unchanged_and_the_across_helpers_ask_the_function():
    assert "EXISTS (SELECT 1 FROM %s parent_row WHERE parent_row.%I = %s.%I)" in ddl.RLS_PARENT
    assert "parent_row WHERE %s AND (%s)" in ddl.RLS_SPLIT
    sql = ddl.parent_visible_sql({"platform.outlet": None})
    assert "FUNCTION platform.apply_parent_across_rls(" in sql
    assert "FUNCTION platform.apply_parent_split_across_rls(" in sql
    assert "platform.parent_visible(%L::regclass, %I)" in sql
    assert "platform.parent_visible(%L::regclass, %I, true)" in sql


def test_no_parent_across_writes_no_function():
    out = ddl.rls_file("tenant", [], [], BY_PARENT[1:], [], 1, False, across=set())
    assert "FUNCTION platform.parent_visible" not in out and "apply_parent_across_rls('" not in out
