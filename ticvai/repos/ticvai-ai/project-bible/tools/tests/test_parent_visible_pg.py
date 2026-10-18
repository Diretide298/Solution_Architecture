"""platform.visible_parent_ids on a real PostgreSQL 16 (ADAM CR-108, CR-095; CHG-RSF-001).

Builds the schemas the way DB-ROLES does: a migration role (no superuser, no BYPASSRLS, no CREATEROLE) owns the
tables, and the operations role has no grant on platform.outlet or the catalogue schema. Applies the helpers derive-ddl
generates and checks what each role sees. A second database is migrated as `postgres`, as a developer's local one
is: there the function must end up owned by `ticvai_parent_visible`, which does not bypass row-level security, and
still show the caller only its own rows, also through a parent that has a parent of its own (catalogue.performance ->
catalogue.event). A third is migrated by a role with BYPASSRLS that may not create roles: the migration refuses.
Needs Docker running; it must run, not skip, before the commit.

    python -m pytest ticvai/tools/tests/test_parent_visible_pg.py -q -rs
"""
import importlib.util
import shutil
import subprocess
import time
import uuid
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ddl", TOOLS / "derive-ddl.py")
ddl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ddl)


def _docker_up():
    return bool(shutil.which("docker")) and subprocess.run(["docker", "info"], capture_output=True).returncode == 0


pytestmark = pytest.mark.skipif(not _docker_up(), reason="Docker is not running: start it; this test must run")

IDS = {n: str(uuid.uuid4()) for n in ("oA", "oB", "mA", "mB", "xA", "MT", "MV", "RT", "RV", "eA", "eB", "pA", "pB",
                                      "qA", "qB")}
WRITE = "platform.in_scope(parent_row.scope_path)"
BY_PARENT = [("fnb.menu", "outlet_id", "platform.outlet", "id"),
             ("approvals.rule", "matrix_id", "approvals.matrix", "id", WRITE),
             ("catalogue.performance", "event_id", "catalogue.event", "id"),
             ("resources.participant", "performance_id", "catalogue.performance", "id")]
ACROSS = {"fnb.menu", "approvals.rule", "resources.participant"}
SUPER = """
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE ROLE migrator LOGIN NOSUPERUSER NOBYPASSRLS NOCREATEROLE;
CREATE ROLE operations LOGIN NOSUPERUSER NOBYPASSRLS;
CREATE ROLE stranger LOGIN NOSUPERUSER NOBYPASSRLS;
CREATE ROLE bypasser LOGIN NOSUPERUSER BYPASSRLS NOCREATEROLE;
GRANT CREATE ON DATABASE postgres TO migrator;
"""


def schema_sql():
    across = [e for e in BY_PARENT if e[0] in ACROSS]
    helpers = (ddl.RLS_HEAD.replace("{n_venue}", "0") + ddl.RLS_RESET + ddl.RLS_PARENT + ddl.RLS_SPLIT
               + ddl.visible_parent_ids_sql(ddl.parents_of(across),
                                            ddl.owner_reads(ddl.parents_of(across), BY_PARENT)))
    i = IDS
    return f"""
CREATE SCHEMA platform; CREATE SCHEMA fnb; CREATE SCHEMA approvals; CREATE SCHEMA catalogue; CREATE SCHEMA resources;
CREATE TABLE platform.scope (id uuid PRIMARY KEY, level text NOT NULL, path ltree NOT NULL);
CREATE TABLE platform.outlet (id uuid PRIMARY KEY, scope_path ltree NOT NULL);
CREATE TABLE fnb.menu (id uuid PRIMARY KEY, outlet_id uuid NOT NULL);
CREATE TABLE fnb.menu_r6 (id uuid PRIMARY KEY, outlet_id uuid NOT NULL);
CREATE TABLE approvals.matrix (id uuid PRIMARY KEY, scope_path ltree NOT NULL);
CREATE TABLE approvals.rule (id uuid PRIMARY KEY, matrix_id uuid NOT NULL);
CREATE TABLE catalogue.event (id uuid PRIMARY KEY, scope_path ltree NOT NULL);
CREATE TABLE catalogue.performance (id uuid PRIMARY KEY, event_id uuid NOT NULL);
CREATE TABLE resources.participant (id uuid PRIMARY KEY, performance_id uuid NOT NULL);
{helpers}
SELECT platform.apply_scope_rls('platform.outlet'::regclass);
SELECT platform.apply_parent_across_rls('fnb.menu'::regclass, 'outlet_id', 'platform.outlet'::regclass, 'id');
SELECT platform.apply_read_beneath_rls('approvals.matrix'::regclass);
SELECT platform.apply_parent_split_across_rls('approvals.rule'::regclass, 'matrix_id', 'approvals.matrix'::regclass,
                                              'id', '{WRITE}');
SELECT platform.apply_scope_rls('catalogue.event'::regclass);
SELECT platform.apply_parent_rls('catalogue.performance'::regclass, 'event_id', 'catalogue.event'::regclass, 'id');
SELECT platform.apply_parent_across_rls('resources.participant'::regclass, 'performance_id',
                                        'catalogue.performance'::regclass, 'id');
ALTER TABLE fnb.menu_r6 ENABLE ROW LEVEL SECURITY;
ALTER TABLE fnb.menu_r6 FORCE ROW LEVEL SECURITY;
CREATE POLICY menu_r6_scope ON fnb.menu_r6
    USING (EXISTS (SELECT 1 FROM platform.outlet parent_row WHERE parent_row.id = menu_r6.outlet_id));
GRANT USAGE ON SCHEMA platform, fnb, approvals, resources TO operations, stranger;
GRANT SELECT ON platform.scope TO operations, stranger;
GRANT SELECT, INSERT ON fnb.menu, fnb.menu_r6, approvals.matrix, approvals.rule, resources.participant TO operations;
GRANT SELECT ON fnb.menu TO stranger;
SET ticvai.scope_paths = 't1';
INSERT INTO platform.outlet VALUES ('{i["oA"]}', 't1.r1.v1'), ('{i["oB"]}', 't1.r1.v2');
INSERT INTO fnb.menu VALUES ('{i["mA"]}', '{i["oA"]}'), ('{i["mB"]}', '{i["oB"]}');
INSERT INTO fnb.menu_r6 VALUES ('{i["xA"]}', '{i["oA"]}');
INSERT INTO approvals.matrix VALUES ('{i["MT"]}', 't1'), ('{i["MV"]}', 't1.r1.v1');
INSERT INTO approvals.rule VALUES ('{i["RT"]}', '{i["MT"]}'), ('{i["RV"]}', '{i["MV"]}');
INSERT INTO catalogue.event VALUES ('{i["eA"]}', 't1.r1.v1'), ('{i["eB"]}', 't1.r1.v2');
INSERT INTO catalogue.performance VALUES ('{i["pA"]}', '{i["eA"]}'), ('{i["pB"]}', '{i["eB"]}');
INSERT INTO resources.participant VALUES ('{i["qA"]}', '{i["pA"]}'), ('{i["qB"]}', '{i["pB"]}');
"""


def run(name, sql, user="postgres", db="postgres"):
    return subprocess.run(["docker", "exec", "-i", name, "psql", "-X", "-q", "-v", "ON_ERROR_STOP=1", "-At",
                           "-U", user, "-d", db], input=sql, text=True, capture_output=True)


def createdb(name, db, owner):
    r = subprocess.run(["docker", "exec", "-i", name, "psql", "-X", "-q", "-U", "postgres", "-c",
                        f"CREATE DATABASE {db} OWNER {owner}"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = run(name, "CREATE EXTENSION IF NOT EXISTS ltree;", db=db)
    assert r.returncode == 0, r.stderr


def wait(name):
    for _ in range(90):
        if run(name, "SELECT 1;").returncode == 0:
            break
        time.sleep(1)
    time.sleep(2)   # the image restarts the server once after initdb
    for _ in range(30):
        if run(name, "SELECT 1;").returncode == 0:
            return
        time.sleep(1)


@pytest.fixture(scope="module")
def pg():
    name = f"lane-f-rls-{uuid.uuid4().hex[:8]}"
    subprocess.run(["docker", "run", "-d", "--rm", "--name", name, "-e", "POSTGRES_PASSWORD=x",
                    "postgres:16-alpine"], check=True, capture_output=True)
    try:
        wait(name)
        r = run(name, SUPER)
        assert r.returncode == 0, r.stderr
        r = run(name, schema_sql(), "migrator")           # production-like: the migration role owns everything
        assert r.returncode == 0, r.stderr
        createdb(name, "localdev", "postgres")
        r = run(name, schema_sql(), "postgres", "localdev")   # a developer's local database
        assert r.returncode == 0, r.stderr
        createdb(name, "bypassdb", "bypasser")
        yield name
    finally:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)


VENUE = "SET ticvai.scope_paths = 't1.r1.v1';\n"


def rows(pg, sql, db="postgres", user="operations"):
    r = run(pg, VENUE + sql, user, db)
    assert r.returncode == 0, r.stderr
    return sorted(x for x in r.stdout.split() if x)


def owner(pg, db):
    r = run(pg, "SELECT r.rolname, r.rolsuper, r.rolbypassrls FROM pg_proc f JOIN pg_roles r ON r.oid = f.proowner "
                "WHERE f.oid = 'platform.visible_parent_ids(regclass, boolean)'::regprocedure;", db=db)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def test_the_r6_check_is_refused_to_a_role_without_the_parent_grant(pg):
    r = run(pg, VENUE + "SELECT id FROM fnb.menu_r6;", "operations")
    assert r.returncode != 0 and "permission denied for table outlet" in r.stderr


def test_the_function_shows_the_callers_venue_only(pg):
    assert rows(pg, "SELECT id FROM fnb.menu;") == [IDS["mA"]]


def test_a_write_under_another_venues_outlet_is_refused(pg):
    r = run(pg, VENUE + f"INSERT INTO fnb.menu VALUES ('{uuid.uuid4()}', '{IDS['oB']}');", "operations")
    assert r.returncode != 0 and "row-level security" in r.stderr


def test_a_venue_reads_the_matrices_it_inherits_and_writes_only_its_own(pg):
    assert rows(pg, "SELECT id FROM approvals.matrix;") == sorted([IDS["MT"], IDS["MV"]])
    assert rows(pg, "SELECT id FROM approvals.rule;") == sorted([IDS["RT"], IDS["RV"]])
    bad = run(pg, VENUE + f"INSERT INTO approvals.rule VALUES ('{uuid.uuid4()}', '{IDS['MT']}');", "operations")
    assert bad.returncode != 0 and "row-level security" in bad.stderr
    ok = run(pg, VENUE + f"INSERT INTO approvals.rule VALUES ('{uuid.uuid4()}', '{IDS['MV']}');", "operations")
    assert ok.returncode == 0, ok.stderr


def test_a_parent_with_a_parent_of_its_own_answers_through_its_chain(pg):
    for db in ("postgres", "localdev"):
        assert rows(pg, "SELECT id FROM resources.participant;", db) == [IDS["qA"]]


def test_only_declared_parents_are_answered(pg):
    r = run(pg, VENUE + "SELECT count(*) FROM platform.visible_parent_ids('fnb.menu'::regclass);", "operations")
    assert r.returncode != 0 and "is not a parent a policy names" in r.stderr


def test_execute_is_the_deployable_roles_only(pg):
    r = run(pg, VENUE + "SELECT id FROM fnb.menu;", "stranger")
    assert r.returncode != 0 and "permission denied for function visible_parent_ids" in r.stderr


def test_production_like_the_migration_role_owns_it_and_does_not_bypass_row_security(pg):
    assert owner(pg, "postgres") == "migrator|f|f"


def test_migrated_as_postgres_it_gets_an_owner_that_does_not_bypass_row_security(pg):
    assert owner(pg, "localdev") == "ticvai_parent_visible|f|f"
    assert rows(pg, "SELECT id FROM fnb.menu;", "localdev") == [IDS["mA"]]
    assert rows(pg, "SELECT id FROM approvals.rule;", "localdev") == sorted([IDS["RT"], IDS["RV"]])


def test_a_bypassing_owner_is_replaced_when_a_parent_policy_is_applied_again(pg):
    r = run(pg, "ALTER FUNCTION platform.visible_parent_ids(regclass, boolean) OWNER TO postgres;", db="localdev")
    assert r.returncode == 0, r.stderr
    leak = rows(pg, "SELECT id FROM fnb.menu;", "localdev")
    assert leak == sorted([IDS["mA"], IDS["mB"]])     # the risk D5 names: a superuser owner shows every child row
    r = run(pg, "SELECT platform.apply_parent_across_rls('fnb.menu'::regclass, 'outlet_id', "
                "'platform.outlet'::regclass, 'id');", db="localdev")
    assert r.returncode == 0, r.stderr
    assert owner(pg, "localdev") == "ticvai_parent_visible|f|f"
    assert rows(pg, "SELECT id FROM fnb.menu;", "localdev") == [IDS["mA"]]


def test_a_migration_role_that_bypasses_row_security_and_may_not_create_roles_is_refused(pg):
    r = run(pg, schema_sql(), "bypasser", "bypassdb")
    assert r.returncode != 0
    assert "bypasses row-level security" in r.stderr and "may not create a role" in r.stderr
