"""Which open blocking CRs affect a ticket, on stand-in data, with no service and no store (CHG-ADM-004).

The board and the pull carry `blockedBy` from `api/blockers.py`; this holds the matching itself:
a CR blocks while it is blocking and open, or accepted and not yet in a release ADAM serves; it
affects a ticket raised from it (but not its own child task), a ticket linked to one of its
artefacts, and a ticket whose operation reads or writes a table it names (the lineage).

Run:  python api/blockers-check.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import blockers as b  # noqa: E402

LINEAGE = {"borrowbook": {"lending.loan", "lending.book"}, "getmember": {"lending.member"}}


def cr(number, **kw):
    base = {"number": number, "title": f"CR {number}", "status": "open", "blocking": True, "external_key": "",
            "child_key": "", "target_kind": "screen", "target_id": "NONE-000", "artefact_ids": [], "resolved_ref": ""}
    base.update(kw)
    return base


CRS = [
    cr(1, target_kind="screen", target_id="WEB-001"),                          # a screen
    cr(2, target_kind="table", target_id="lending.loan"),                      # a table an operation writes
    cr(3, target_kind="other", target_id="x", artefact_ids=["operation:lending#getMember"]),  # listed artefact
    cr(4, target_kind="screen", target_id="WEB-001", blocking=False),          # not blocking
    cr(5, target_kind="screen", target_id="WEB-001", status="done"),           # settled
    cr(6, target_kind="screen", target_id="WEB-001", status="accepted", resolved_ref="r2"),   # released at r2
    cr(7, target_kind="screen", target_id="WEB-009", status="accepted", resolved_ref="r3"),   # not yet released
    cr(8, external_key="7008"),                                                # raised from the ticket
    cr(9, target_kind="screen", target_id="WEB-002", child_key="7009"),        # 7009 is its own child task
]

TICKETS = {
    "7001": [{"kind": "screen", "id": "WEB-001"}],
    "7002": [{"kind": "operation", "id": "lending#borrowBook"}],
    "7003": [{"kind": "operation", "id": "getMember"}],
    "7004": [{"kind": "screen", "id": "WEB-404"}],
    "7007": [{"kind": "screen", "id": "WEB-009"}],
    "7008": [],
    "7009": [{"kind": "screen", "id": "WEB-002"}],
}

WANT = {
    "7001": ["CR-001"],            # 4 not blocking, 5 done, 6 released at r2 <= r2
    "7002": ["CR-002"],            # via the lineage
    "7003": ["CR-003"],            # operation listed in artefact_ids, compared by operationId
    "7004": [],
    "7007": ["CR-007"],            # accepted, r3 not served yet
    "7008": ["CR-008"],
    "7009": [],                    # its own CR does not block the child task that settles it
}

failed = 0
for key, links in TICKETS.items():
    got = [x["id"] for x in b.affecting(key, links, CRS, LINEAGE, served_tag="r2")]
    ok = got == WANT[key]
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  #{key}: {got}" + ("" if ok else f" (want {WANT[key]})"))

via = b.affecting("7002", TICKETS["7002"], CRS, LINEAGE, "r2")[0]["via"]
ok = "lending.loan" in via and "borrowBook" in via
failed += not ok
print(f"{'PASS' if ok else 'FAIL'}  the lineage match says how: {via}")

ok = [x["id"] for x in b.affecting("7001", TICKETS["7001"], CRS, LINEAGE, served_tag="r1")] == ["CR-001", "CR-006"]
failed += not ok
print(f"{'PASS' if ok else 'FAIL'}  while r1 is served, a CR released at r2 still blocks")

ok = b.affecting("7002", TICKETS["7002"], CRS, {}, "r2") == []
failed += not ok
print(f"{'PASS' if ok else 'FAIL'}  without a lineage there is no table-level match, and nothing is invented")

total = len(TICKETS) + 3
print(f"\n{total - failed} passed, {failed} failed")
sys.exit(1 if failed else 0)
