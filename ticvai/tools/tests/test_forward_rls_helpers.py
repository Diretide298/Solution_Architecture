"""Tests for generated RLS helpers and SCOPE_FOLLOWS in tools/ddl_forward.py (ADAM CR-095, CR-108; CHG-RSF-001).

    python -m pytest ticvai/tools/tests/test_forward_rls_helpers.py -q
"""
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import ddl_forward as fwd  # noqa: E402

TABLES = ("CREATE TABLE platform.outlet (id uuid PRIMARY KEY);\n"
          "CREATE TABLE fnb.menu (id uuid PRIMARY KEY, outlet_id uuid NOT NULL);\n")
OLD_HELPER = """CREATE OR REPLACE FUNCTION platform.apply_parent_rls(target regclass, fk_column text,
                                                     parent regclass, parent_key text)
    RETURNS void
    LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('CREATE POLICY p ON %s USING (EXISTS (SELECT 1 FROM %s parent_row))', target, parent);
END
$$;
"""
NEW_HELPER = OLD_HELPER.replace("EXISTS (SELECT 1 FROM %s parent_row)", "%I IN (SELECT platform.visible_parent_ids(%L::regclass))")
CALL = "SELECT platform.apply_parent_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');\n"
PV = ("CREATE OR REPLACE FUNCTION platform.visible_parent_ids(parent regclass, for_write boolean DEFAULT "
      "false) RETURNS boolean LANGUAGE plpgsql STABLE SECURITY DEFINER AS $$ BEGIN RETURN false; END $$;\n")


def model(sql):
    m = fwd.Model()
    m.add_file(sql)
    return m


def flat(stmts):
    return [fwd.norm(s).rstrip(";") for s in stmts]


def test_a_changed_rls_helper_is_replaced_and_every_table_using_it_reapplied():
    p = fwd.diff("tenant", model(TABLES + OLD_HELPER + CALL), model(TABLES + NEW_HELPER + CALL))
    st = flat(p.statements)
    i = next(n for n, s in enumerate(st) if s.startswith("CREATE OR REPLACE FUNCTION platform.apply_parent_rls"))
    assert st[i + 1:] == ["SELECT platform.drop_rls_policies('fnb.menu'::regclass)", fwd.norm(CALL).rstrip(";")]
    assert not [r for r in p.review if r[0] == "function changed"]
    assert p.counts.get("policies") == 1
    rb = list(reversed(p.rollback))           # the rollback runs reversed
    assert rb[0].startswith("CREATE OR REPLACE FUNCTION platform.apply_parent_rls") and "EXISTS (SELECT 1" in rb[0]
    assert "apply_parent_rls('fnb.menu'" in rb[1]


def test_visible_parent_ids_is_added_then_replaced_without_reapplying():
    first = fwd.diff("tenant", model(TABLES + NEW_HELPER + CALL), model(TABLES + NEW_HELPER + PV + CALL))
    assert flat(first.statements) == [fwd.norm(PV).rstrip(";")]
    again = fwd.diff("tenant", model(TABLES + NEW_HELPER + PV + CALL),
                     model(TABLES + NEW_HELPER + PV.replace("RETURN false", "RETURN true") + CALL))
    st = flat(again.statements)
    assert len(st) == 1 and st[0].startswith("CREATE OR REPLACE FUNCTION platform.visible_parent_ids")
    assert not again.review


def test_the_owner_function_is_replaced_too():
    f = ("CREATE OR REPLACE FUNCTION platform.visible_parent_ids_setup() RETURNS void "
         "LANGUAGE plpgsql AS $$ BEGIN RETURN; END $$;\n")
    p = fwd.diff("tenant", model(TABLES + f), model(TABLES + f.replace("RETURN;", "NULL;")))
    assert len(p.statements) == 1 and not p.review


def test_any_other_function_change_is_still_for_a_person():
    f = ("CREATE OR REPLACE FUNCTION platform.in_scope(row_scope_path ltree) RETURNS boolean LANGUAGE sql "
         "AS $$ SELECT true $$;\n")
    p = fwd.diff("tenant", model(f), model(f.replace("SELECT true", "SELECT false")))
    assert [r[0] for r in p.review] == ["function changed"] and not p.statements


def test_a_device_takes_its_workstations_path():
    assert fwd.SCOPE_FOLLOWS["platform.device"] == ("workstation_id", "platform.workstation", "workstation")
    sql = fwd.scope_path_backfill("platform.device", {"workstation_id": "uuid", "scope_path": "ltree"})
    assert ("UPDATE platform.device x SET scope_path = p.scope_path FROM platform.workstation p WHERE "
            "p.id = x.workstation_id AND x.scope_path IS DISTINCT FROM p.scope_path") in sql
    assert "WHERE scope_path IS NULL" in sql and sql.endswith("ALTER COLUMN scope_path SET NOT NULL")


def test_a_renamed_tables_old_policy_call_is_not_listed_as_dropped_when_its_helper_changes():
    # sync.dsar_request was platform.dsar_request (CHG-XDW-001); its parent call becomes apply_parent_across_rls
    # (CHG-RSF-001). The "after rename" row already tells the person to apply its policy again; the old call is
    # replaced, not dropped.
    old = model("CREATE TABLE approvals.request (id uuid PRIMARY KEY);\n"
                "CREATE TABLE platform.dsar_request (id uuid PRIMARY KEY, request_id uuid NOT NULL);\n"
                "SELECT platform.apply_parent_rls('platform.dsar_request'::regclass, 'request_id', "
                "'approvals.request'::regclass, 'id');\n")
    new = model("CREATE TABLE approvals.request (id uuid PRIMARY KEY);\n"
                "CREATE TABLE sync.dsar_request (id uuid PRIMARY KEY, request_id uuid NOT NULL);\n"
                "SELECT platform.apply_parent_across_rls('sync.dsar_request'::regclass, 'request_id', "
                "'approvals.request'::regclass, 'id');\n")
    p = fwd.diff("tenant", old, new, renames={"tables": {"platform.dsar_request": "sync.dsar_request"}})
    assert not [r for r in p.review if r[0] == "statement dropped"]
    assert [r[0] for r in p.review] == ["table renamed", "after rename"]
    # fix round 1: the across policy reaches the database by a generated statement, under the table's current name;
    # a policy belongs to the table, so it moves with SET SCHEMA when the person renames it
    assert flat(p.statements) == [
        "SELECT platform.drop_rls_policies('platform.dsar_request'::regclass)",
        "SELECT platform.apply_parent_across_rls('platform.dsar_request'::regclass, 'request_id', "
        "'approvals.request'::regclass, 'id')"]
    assert p.counts.get("policies") == 1
    assert "apply_parent_rls('platform.dsar_request'" in p.rollback[0]
    # and the after-rename row names the whole call, parent included
    after = [r for r in p.review if r[0] == "after rename"][0]
    assert "'approvals.request'::regclass, 'id')" in after[2]


def test_a_renamed_tables_policy_under_an_r6_helper_still_waits_for_the_person():
    old = model("CREATE TABLE a.p (id uuid PRIMARY KEY);\n"
                "CREATE TABLE a.old (id uuid PRIMARY KEY, p_id uuid NOT NULL);\n"
                "SELECT platform.apply_parent_rls('a.old'::regclass, 'p_id', 'a.p'::regclass, 'id');\n")
    new = model("CREATE TABLE a.p (id uuid PRIMARY KEY);\n"
                "CREATE TABLE a.new (id uuid PRIMARY KEY, p_id uuid NOT NULL);\n"
                "SELECT platform.apply_tenant_rls('a.new'::regclass);\n")
    p = fwd.diff("tenant", old, new, renames={"tables": {"a.old": "a.new"}})
    assert p.statements == []


def test_a_scope_path_replacing_the_venue_policy_backfills_the_venue_then_the_tenant_root():
    # ledger.account_mapping (ADAM CR-168, CHG-CRA-007) moved from apply_venue_rls to read-beneath with a scope_path;
    # venue_in_scope showed a row at its venue's platform.scope row, and a null venue_id at the tenant root, so the
    # backfill gives each row that same place before the NOT NULL (r8 gate residue, CHG-R8RES-001).
    t = ("CREATE TABLE ledger.account_mapping (id uuid PRIMARY KEY, venue_id uuid, event_type text NOT NULL);\n")
    old = model(t + "SELECT platform.apply_venue_rls('ledger.account_mapping'::regclass);\n")
    assert fwd.was_venue_rls(old, "ledger.account_mapping") and not fwd.was_tenant_root(old, "ledger.account_mapping")
    sql = fwd.scope_path_backfill("ledger.account_mapping", {"id": "uuid", "venue_id": "uuid", "scope_path": "ltree"},
                                  False, True)
    assert ("UPDATE ledger.account_mapping x SET scope_path = s.path FROM platform.scope s WHERE s.id = x.venue_id "
            "AND x.scope_path IS NULL") in sql
    assert "WHERE level = 'tenant') WHERE scope_path IS NULL" in sql and sql.endswith("SET NOT NULL")
    # without the venue policy, a venue_id alone names no owner: the person decides, as before
    assert fwd.scope_path_backfill("ledger.account_mapping", {"venue_id": "uuid", "scope_path": "ltree"}) is None
    # the policy in force is the last call: a table moved off the venue policy earlier is not read as venue-owned
    later = model(t + "SELECT platform.apply_venue_rls('ledger.account_mapping'::regclass);\n"
                  "SELECT platform.drop_rls_policies('ledger.account_mapping'::regclass);\n"
                  "SELECT platform.apply_tenant_rls('ledger.account_mapping'::regclass);\n")
    assert not fwd.was_venue_rls(later, "ledger.account_mapping")
