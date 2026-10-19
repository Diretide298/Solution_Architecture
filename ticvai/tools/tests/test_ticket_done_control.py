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


# ---- what a migration needs that the copied DDL does not give it (CHG-R8MIG-008) ----------------------------------

def test_a_parent_policy_moves_to_the_later_migration_that_creates_its_parent():
    policies = {"pii.subject_biometric": "access.entitlement", "sync.rejection": "platform.workstation",
                "inventory.movement": "inventory.item", "orders.order_line": "orders.order"}
    made_by = {"pii.subject_biometric": "MIG-PII", "access.entitlement": "MIG-ACCESS",
               "sync.rejection": "MIG-SYNC", "inventory.movement": "MIG-INVENTORY",
               "inventory.inventory_item": "MIG-INVENTORY", "orders.order_line": "MIG-ORDERS",
               "orders.order": "MIG-ORDERS"}
    order = {"MIG-PII": 7, "MIG-ACCESS": 27, "MIG-SYNC": 12, "MIG-INVENTORY": 20, "MIG-ORDERS": 30}
    moved, orphans = td.parent_policy_moves(policies, made_by, order, {"inventory.item": "inventory.inventory_item"})
    assert moved == {"pii.subject_biometric": ("MIG-PII", "MIG-ACCESS", "access.entitlement")}
    assert orphans == {"sync.rejection": "platform.workstation"}       # no ticket creates the parent
    words = td.parent_policy_sentences(moved, orphans)
    assert "leave out" in words["MIG-PII"][0] and "MIG-ACCESS applies it" in words["MIG-PII"][0]
    assert "Also apply pii.subject_biometric" in words["MIG-ACCESS"][0]
    assert not any(c.isdigit() and "V0" in w for ws in words.values() for w in ws for c in w)   # no V-number


def test_a_type_no_file_creates_is_given_to_the_ticket_with_its_values():
    s = td.type_sentence("pii.subject", [("pii.subject_kind", "kind", ["guest", "employee"])])
    assert "CREATE TYPE pii.subject_kind AS ENUM ('guest', 'employee');" in s and "pii.subject.kind" in s


def test_the_baseline_says_function_bodies_are_not_checked():
    assert "SET check_function_bodies = off" in td.BASELINE_BODIES


def test_a_db_ticket_is_done_on_a_copy_twice_and_by_the_db_ticket_script(monkeypatch):
    monkeypatch.setattr(td, "_LINEAGE", LIN)
    db = {"type": "Task", "track": "Database", "key": "MIG-X", "description": ""}
    text = td.done_when(db, "", ["table platform.outbox"])
    assert "applies on a copy of the database at the previous state" in text
    assert "a second run applies nothing" in text and "db-ticket.mjs <ticket>` says MATCH" in text
    assert "runs once a day and in the merge-request pipeline" in text and "a peer has reviewed it" in text
    assert "previous release" not in text


def test_only_an_ai_engine_task_says_its_operations_are_served_by_the_ai_gateway():
    ai = td.claimed_ops_sentence(["askConcierge"], True)
    assert "served by ticvai-ai behind the AI gateway" in ai and "no back-end task builds them" in ai
    other = td.claimed_ops_sentence(["createProduct", "updateProduct"], False)
    assert "AI gateway" not in other and "ticvai-ai" not in other
    assert "are built by this task" in other and "no other back-end task builds them" in other
