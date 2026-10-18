"""Tests for platform.visible_parent_ids in tools/derive-ddl.py (ADAM CR-108; CHG-RSF-001).

    python -m pytest ticvai/tools/tests/test_parent_visible_generator.py -q

Fix round 1 (18 October 2026), as the controller ruled: the function is set-based. A child across deployables reads
`<fk> IN (SELECT platform.visible_parent_ids(parent))`, so the parent's own policy runs once per query, not once per
child row (12 ms against 10-19 s on 100,000 rows). Its owner never bypasses row security: the migration gives it a
dedicated owner where it may create one, and refuses where it may not (D5 forbids refusing at run time only). The
dedicated owner reads every table the parent's own policy reads, up the chain. EXECUTE is the deployable roles' only.
"""
import importlib.util
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ddl", TOOLS / "derive-ddl.py")
ddl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ddl)

WRITE = "platform.in_scope(parent_row.scope_path)"
CHAIN_WRITE = ("EXISTS (SELECT 1 FROM approvals.matrix p1 WHERE p1.id = parent_row.matrix_id AND "
               "(platform.in_scope(p1.scope_path)))")


def test_one_branch_per_parent_returning_its_visible_ids_and_a_write_branch_only_for_split_parents():
    sql = ddl.visible_parent_ids_sql({"platform.outlet": None, "approvals.matrix": WRITE}, [])
    # public is on the path because ltree lives there (001-extensions.sql); without it in_scope fails inside
    assert "SECURITY DEFINER" in sql and "SET search_path = pg_catalog, public, pg_temp" in sql
    assert "FUNCTION platform.visible_parent_ids(parent regclass, for_write boolean DEFAULT false)" in sql
    assert "RETURNS SETOF uuid" in sql
    assert "IF parent = 'platform.outlet'::regclass THEN" in sql
    assert "RETURN QUERY SELECT parent_row.id FROM platform.outlet parent_row;" in sql
    assert sql.count("IF for_write THEN") == 1
    assert f"RETURN QUERY SELECT parent_row.id FROM approvals.matrix parent_row WHERE ({WRITE});" in sql
    assert "is not a parent a policy names" in sql
    assert "EXECUTE format" not in sql.split("FUNCTION platform.visible_parent_ids_setup")[0]   # no dynamic SQL


def test_the_owner_never_bypasses_row_security_and_the_migration_refuses_where_it_cannot_fix_that():
    sql = ddl.visible_parent_ids_sql({"platform.outlet": None}, [])
    assert "CREATE ROLE ticvai_parent_visible NOLOGIN NOSUPERUSER NOBYPASSRLS" in sql
    assert "OWNER TO ticvai_parent_visible" in sql
    setup = sql.split("FUNCTION platform.visible_parent_ids_setup")[1]
    assert "RAISE EXCEPTION 'platform.visible_parent_ids is owned by %, which bypasses row-level security" in setup
    assert "RAISE WARNING" not in setup


def test_execute_is_the_deployable_roles_only():
    sql = ddl.visible_parent_ids_sql({"platform.outlet": None}, [])
    assert "REVOKE EXECUTE ON FUNCTION platform.visible_parent_ids(regclass, boolean) FROM PUBLIC" in sql
    assert "ARRAY['commerce', 'access', 'operations', 'workers', 'ticvai_ai']" in sql


def test_the_dedicated_owner_reads_every_table_up_each_parents_chain():
    by_parent = [("resources.participant", "performance_id", "catalogue.performance", "id"),
                 ("catalogue.performance", "event_id", "catalogue.event", "id"),
                 ("approvals.rule", "matrix_id", "approvals.matrix", "id", WRITE),
                 ("approvals.step", "rule_id", "approvals.rule", "id", CHAIN_WRITE)]
    assert ddl.owner_reads({"catalogue.performance": None}, by_parent) == [
        "catalogue.event", "catalogue.performance", "platform.scope"]
    # a split parent's write check names a table too
    assert ddl.owner_reads({"approvals.rule": CHAIN_WRITE}, by_parent) == [
        "approvals.matrix", "approvals.rule", "platform.scope"]
    sql = ddl.visible_parent_ids_sql({"catalogue.performance": None}, ddl.owner_reads(
        {"catalogue.performance": None}, by_parent))
    assert "ARRAY['catalogue.event', 'catalogue.performance', 'platform.scope']" in sql


def test_reserved_words_are_quoted():
    sql = ddl.visible_parent_ids_sql({"marketing.case": None}, [])
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
# 2026): a child whose parent is in its own deployable keeps r6's EXISTS, which its host's grants can read.
BY_PARENT = [("fnb.menu", "outlet_id", "platform.outlet", "id"), ("fnb.menu_section", "menu_id", "fnb.menu", "id")]


def test_a_child_across_deployables_asks_the_function_and_one_within_keeps_the_r6_check():
    out = ddl.rls_file("tenant", [], [], BY_PARENT, [], 2, False, across={"fnb.menu"})
    assert "CREATE OR REPLACE FUNCTION platform.visible_parent_ids(" in out
    assert "IF parent = 'platform.outlet'::regclass THEN" in out
    assert "IF parent = 'fnb.menu'::regclass THEN" not in out           # only the parents across are answered
    assert ("SELECT platform.apply_parent_across_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, "
            "'id');") in out
    assert ("SELECT platform.apply_parent_rls('fnb.menu_section'::regclass, 'menu_id', 'fnb.menu'::regclass, "
            "'id');") in out
    assert "PERFORM platform.visible_parent_ids_setup();" in out


def test_the_r6_helpers_are_unchanged_and_the_across_helpers_ask_the_function_once_per_query():
    assert "EXISTS (SELECT 1 FROM %s parent_row WHERE parent_row.%I = %s.%I)" in ddl.RLS_PARENT
    assert "parent_row WHERE %s AND (%s)" in ddl.RLS_SPLIT
    sql = ddl.visible_parent_ids_sql({"platform.outlet": None}, [])
    assert "FUNCTION platform.apply_parent_across_rls(" in sql
    assert "FUNCTION platform.apply_parent_split_across_rls(" in sql
    assert "'%I IN (SELECT platform.visible_parent_ids(%L::regclass))'" in sql
    assert "'%I IN (SELECT platform.visible_parent_ids(%L::regclass, true))'" in sql


def test_no_parent_across_writes_no_function():
    out = ddl.rls_file("tenant", [], [], BY_PARENT[1:], [], 1, False, across=set())
    assert "FUNCTION platform.visible_parent_ids" not in out and "apply_parent_across_rls('" not in out
