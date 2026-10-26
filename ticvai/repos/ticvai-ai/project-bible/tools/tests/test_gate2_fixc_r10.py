"""Tests for the r10 gate 2 lane C tool fixes (CHG-R10GFC-004, CHG-R10GFC-006).

    python -m pytest ticvai/tools/tests/test_gate2_fixc_r10.py -q
"""
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import ticket_done as td  # noqa: E402

_spec = importlib.util.spec_from_file_location("rf_gfc", TOOLS / "check-rls-scope-fit.py")
rf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rf)

HOME = ("(platform.tenant_root_in_scope() OR EXISTS (SELECT 1 FROM platform.scope hs WHERE hs.id = home_scope_id "
        "AND platform.in_scope(hs.path)))")


def test_home_scope_write_is_a_scope_write():
    pol = {"identity.principal": ("apply_grant_holder_read_rls", f", '{HOME}'"),
           "x.root_only": ("apply_grant_holder_read_rls", ", 'platform.tenant_root_in_scope()'"),
           "x.scoped": ("apply_grant_holder_read_rls", ", 'platform.in_scope(scope_path)'")}
    cl = rf.classes(pol)
    assert cl["identity.principal"] == ("any", "scope")
    assert cl["x.root_only"] == ("any", "tenant")
    assert cl["x.scoped"] == ("any", "scope")


def _db_root(tmp_path, tenant, control):
    for db, names in (("tenant", tenant), ("control", control)):
        (tmp_path / "backend" / db).mkdir(parents=True)
        for n in names:
            (tmp_path / "backend" / db / n).write_text("-- x\n", encoding="utf-8")
    return tmp_path


TASK = {"key": "R8-DB-LOCAL-X",
        "builds": ["file backend/tenant/V0114__after_r1_20261022.sql", "file backend/tenant/V0115__names_after_r1_20261022.sql",
                   "file backend/control/V0112__after_r1_20261021.sql"],
        "detail": "The files: backend/tenant/V0114__after_r1_20261022.sql, backend/tenant/V0115__names_after_r1_20261022.sql, "
                  "backend/control/V0112__after_r1_20261021.sql. How to check: it is there. Done when: applied."}


def test_a_database_task_gains_each_newer_forward_migration(tmp_path):
    root = _db_root(tmp_path, ["V0114__after_r1_20261022.sql", "V0115__names_after_r1_20261022.sql",
                               "V0116__after_r1_20261026.sql", "V0116a__names_early_after_r1_20261026.sql"],
                    ["V0110__after_r1_20261020.sql", "V0112__after_r1_20261021.sql", "V0116__after_r1_20261026.sql"])
    got = td.db_update_task(TASK, root)
    assert got["builds"][-3:] == ["file backend/tenant/V0116__after_r1_20261026.sql",
                                  "file backend/tenant/V0116a__names_early_after_r1_20261026.sql",
                                  "file backend/control/V0116__after_r1_20261026.sql"]
    # an older file the task skipped is not added: check-ticket-builds B-DB-FILES still names it
    assert "file backend/control/V0110__after_r1_20261020.sql" not in got["builds"]
    i, j = got["detail"].find("backend/tenant/V0116__after_r1_20261026.sql"), got["detail"].find(" How to check")
    assert 0 < i < j
    assert TASK["builds"][-1] == "file backend/control/V0112__after_r1_20261021.sql"   # the input is not changed


def test_nothing_new_or_no_migration_leaves_the_task_alone(tmp_path):
    root = _db_root(tmp_path, ["V0115__names_after_r1_20261022.sql"], ["V0112__after_r1_20261021.sql"])
    assert td.db_update_task(TASK, root) is TASK
    other = {"key": "PLATFORM-OUTBOX", "builds": ["table platform.outbox"], "detail": "x"}
    root2 = _db_root(tmp_path / "b", ["V0116__after_r1_20261026.sql"], [])
    assert td.db_update_task(other, root2) is other
