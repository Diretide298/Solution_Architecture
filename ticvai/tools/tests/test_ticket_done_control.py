"""The done-when of a ticket that builds only control-database work names the rule that holds there (CHG-R8MIG-005).

    python -m pytest ticvai/tools/tests/test_ticket_done_control.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ticket_done as td  # noqa: E402

LIN = {
    "listWebhookSubscriptions": {"reads": ["control.webhook_subscription"], "writes": []},
    "suspendTenant": {"reads": ["cache:idempotency", "control.tenant"], "writes": ["approvals.request"]},
    "getTenantConfig": {"reads": ["whitelabel.config_version"], "writes": []},
}


def test_control_only_reads_tables_and_operations():
    assert td.control_only(["control.tenant", "control.cell"], LIN)
    assert not td.control_only(["control.tenant", "platform.outbox"], LIN)
    assert td.control_only(["public-api#listWebhookSubscriptions"], LIN)
    assert not td.control_only(["tenancy#suspendTenant"], LIN)          # writes a tenant table too
    assert not td.control_only(["white-label#getTenantConfig"], LIN)
    assert not td.control_only(["unknownOperation"], LIN)
    assert not td.control_only([], LIN)


def test_a_control_database_ticket_is_not_told_row_level_security(monkeypatch):
    monkeypatch.setattr(td, "_LINEAGE", LIN)
    db = {"type": "Task", "track": "Database", "key": "MIG-CONTROL", "description": ""}
    text = td.done_when(db, "", ["table control.tenant"])
    assert "no row-level security" in text and "(columns, keys, indexes, row-level security)" not in text
    tenant = td.done_when(db, "", ["table platform.outbox"])
    assert "(columns, keys, indexes, row-level security)" in tenant
    be = {"type": "Task", "track": "Backend", "key": "SVC-X", "description": ""}
    assert "under row-level security" not in td.done_when(be, "", ["operation public-api#listWebhookSubscriptions"])
    assert "under row-level security" in td.done_when(be, "", ["operation tenancy#suspendTenant"])
