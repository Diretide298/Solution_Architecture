#!/usr/bin/env python3
"""A setup ticket's title says how many operations its screen has, and that count is the screen's.

**3 October 2026, CHG-TBF-005** (Block A audit on live r2, pattern 7: "ticket scope out of step with its screen
after the 2 October moves"; `changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`). A Block A setup
screen is built only as far as the first release needs (its setup operations); the rest of the screen is a
later ticket. The title said "BO-009 Pricing Rules (setup: 5 operations)" on an 11-operation screen, so a
reader took it for the whole screen, and 94 Block A titles disagreed with their screens. The title now reads
"(setup: 5 of its 11 operations)" and the later one "(the rest of the screen: 6 of its 11 operations)"
(`tools/build-service-docs.py` setup_scope / rest_scope).

**What fails** (from handoff/service-docs/plan-tasks.csv against screens/P*.yaml):

  S-SCREEN-COUNT    the title's "of its N" (or "all N") is not the number of distinct operations the screen binds
  S-SETUP-COUNT     a setup title's K is not the number of its listed setup operations the screen binds, or a
                    title still in the old form "(setup: N operations)", which does not say the screen's size
  S-SETUP-OP-GONE   a setup ticket lists an operation the screen no longer binds (moved on 2 October)
  S-REST-COUNT      a rest-of-the-screen title's K is not N minus the setup operations on the screen

**14 October 2026, CHG-SWP-001** (the sweep after #27741, AM-IDENTITY-SECURITY-P02 on the guest app: the feature
listed searchGuests and the wishlist operations, which none of its three screens calls). A feature ticket and its
frontend tickets are read against the screens they build (tools/ticket_features.py), in every block:

  S-FEATURE-OP-UNUSED  a feature that builds screens lists (builds) an operation none of those screens calls
  S-SCREEN-OP-UNBUILT  a frontend ticket's screen calls an operation in the ticket's scope that neither its feature
                       nor any ticket it depends on builds, so it can start before its back end exists

The feature #27741 itself is not baselined (ticket_features.UNBASELINED): its findings are always strict.

**14 October 2026, CHG-TKT-001 and CHG-TKT-003** (the Block A audit: 741 S-FEATURE-OP-UNUSED, 6 S-SCREEN-OP-UNBUILT).
A feature now lists, in its own "Builds:", the operations its screens call (build-service-docs.py); its back-end
tasks' operations are a sentence of their own. S-FEATURE-OP-UNUSED reads that list (ticket_features.Feature.ops);
S-SCREEN-OP-UNBUILT still asks whether a task under the feature, or one the frontend ticket depends on, builds the
operation (Feature.built).

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py).

    python3 tools/check-ticket-scope.py [--all]
"""
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402
import ticket_done as td  # noqa: E402  (merge_bindings, CHG-FXP-002)
import ticket_features as tf  # noqa: E402  (CHG-SWP-001)

RULES = {
    "S-SCREEN-COUNT": "a ticket title's screen operation count is not the screen's (CHG-TBF-005)",
    "S-SETUP-COUNT": "a setup title's operation count is not its setup operations on the screen (CHG-TBF-005)",
    "S-SETUP-OP-GONE": "a setup ticket lists an operation its screen no longer binds (CHG-TBF-005)",
    "S-REST-COUNT": "a rest-of-the-screen title's count is not the screen's other operations (CHG-TBF-005)",
    "S-FEATURE-OP-UNUSED": "a feature ticket lists an operation none of its screens calls (#27741, CHG-SWP-001)",
    "S-SCREEN-OP-UNBUILT": "a frontend ticket's screen calls an operation neither its feature nor its dependencies "
                           "build (CHG-SWP-001)",
}
SETUP = re.compile(r"\(setup: (?:(\d+) of its (\d+)|all (\d+)) operations\)")
OLD = re.compile(r"\(setup: \d+ operations?\)")
REST = re.compile(r"\(the rest of the screen: (\d+) of its (\d+) operations\)")


def op_ids(s: dict) -> set:
    """The same count build-service-docs.py puts in the title (screen_op_ids)."""
    return {a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")}


def listed(text: str, head: str) -> set:
    m = re.search(re.escape(head) + r"\s*([A-Za-z0-9, ]+?)(?:\)|\.|;|$)", text or "")
    return {x.strip() for x in m.group(1).split(",") if x.strip()} if m else set()


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-ticket-scope", RULES)
    plan = g.ROOT / "handoff" / "service-docs" / "plan-tasks.csv"
    if not plan.exists():
        guard.note("handoff/service-docs/plan-tasks.csv missing - run tools/build-service-docs.py")
        return guard.finish()
    screens = {s["id"]: s for _, s in g.screens()}
    td.merge_bindings(screens)        # a merged screen's operations are built on its target (CHG-FXP-002), as the plan does
    with plan.open(encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["type"] == "Task" and r["track"] == "Frontend"
                and "#" not in r["key"]]
    n_checked = 0
    for r in rows:
        subj = r["subject"]
        m_sid = re.match(r"^\[FE\] ([A-Z]+-\d+[A-Z]?) ", subj)
        if not m_sid or not (SETUP.search(subj) or OLD.search(subj) or REST.search(subj)):
            continue
        sid, key = m_sid.group(1), r["key"]
        s = screens.get(sid)
        if not s:
            continue
        n_checked += 1
        ops = op_ids(s)
        if OLD.search(subj):
            guard.add("S-SETUP-COUNT", key, f"{key}: '{subj[:90]}' does not say how many operations {sid} has "
                                            f"({len(ops)})")
            continue
        m = SETUP.search(subj)
        if m:
            k, n = (int(m.group(1)), int(m.group(2))) if m.group(1) else (int(m.group(3)), int(m.group(3)))
            setup = listed(r["description"], "In the slice:")
            if n != len(ops):
                guard.add("S-SCREEN-COUNT", key, f"{key}: title says {sid} has {n} operations, the screen binds "
                                                 f"{len(ops)}")
            if k != len(setup & ops):
                guard.add("S-SETUP-COUNT", key, f"{key}: title says {k} setup operations, {len(setup & ops)} of "
                                                f"its listed ones are on {sid}")
            gone = setup - ops
            if gone:
                guard.add("S-SETUP-OP-GONE", key, f"{key}: lists {', '.join(sorted(gone))}, which {sid} no longer "
                                                  "binds")
            continue
        m = REST.search(subj)
        k, n = int(m.group(1)), int(m.group(2))
        setup = listed(r["description"], "Block A built only its setup operations (")
        if n != len(ops):
            guard.add("S-SCREEN-COUNT", key, f"{key}: title says {sid} has {n} operations, the screen binds "
                                             f"{len(ops)}")
        if k != len(ops) - len(setup & ops):
            guard.add("S-REST-COUNT", key, f"{key}: title says {k} more operations, {sid} has "
                                           f"{len(ops) - len(setup & ops)} beyond its setup ones")
    guard.note(f"{n_checked} setup and rest-of-the-screen ticket(s) checked against their screens")
    feature_ops(guard, screens)
    return guard.finish()


def feature_ops(guard, screens: dict) -> None:
    """CHG-SWP-001: a feature's operations against its screens', and each frontend ticket's against its builders."""
    rows = tf.plan_rows(g.ROOT)
    by_key = {r["key"]: r for r in rows}
    platform_of = {s["id"]: stem[:3] for stem, s in g.screens()}
    ops = g.operations()
    built = tf.builders(rows)
    feats = tf.features(rows, screens, platform_of)
    per = {}
    for fk, f in sorted(feats.items()):
        strict = fk in tf.UNBASELINED
        app = "/".join(sorted(f.platforms))
        called = set().union(*(tf.screen_ops(screens[s]) for s in f.screens))
        for o in sorted(set(f.ops) - called):
            guard.add("S-FEATURE-OP-UNUSED", f"{fk}:{o}",
                      f"{fk} ({app}, block {f.block}): lists {o} ({f.ops[o]}), which none of "
                      f"{', '.join(sorted(f.screens))} calls", strict=strict)
            per[(app, f.block, "unused")] = per.get((app, f.block, "unused"), 0) + 1
        for task, sid in f.frontend:
            dep = set((task.get("dependsOn") or "").split())
            for o in sorted(tf.scope(task, sid, screens, by_key)):
                if o in f.built or o not in ops or built.get(o, set()) & dep:
                    continue
                where = ", ".join(sorted(built.get(o) or [])[:3]) or "no ticket"
                guard.add("S-SCREEN-OP-UNBUILT", f"{task['key']}:{o}",
                          f"{task['key']} ({app}, block {f.block}): {sid} calls {o}; built by {where}, which "
                          f"neither {fk} nor its dependsOn holds", strict=strict)
                per[(app, f.block, "unbuilt")] = per.get((app, f.block, "unbuilt"), 0) + 1
    guard.note(f"{len(feats)} feature ticket(s) with screens read against their screens (CHG-SWP-001)")
    if per:
        guard.note("by app and block: " + ", ".join(f"{a} {b} {k} {n}" for (a, b, k), n in sorted(per.items())))


if __name__ == "__main__":
    sys.exit(main())
