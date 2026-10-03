"""Tests for tools/op-release.py, the release bundle for the OpenProject push (C6, C7).

    python -m pytest ticvai/tools/tests/test_op_release.py -q

The synthetic tests build a small plan in memory; the last test builds the real bundle from the package (no
network, nothing written) and checks the invariants the server script relies on.
"""
import csv
import importlib.util
import json
import re
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
DOCS = ROOT / "handoff" / "service-docs"

_spec = importlib.util.spec_from_file_location("op_release", TOOLS / "op-release.py")
rel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rel)


def row(key, typ, parent="", track="Backend", subject="", deps="", seq="1", assignee="", service="", area="",
        description="", wave="1"):
    return {"sequence": seq, "queue": "", "key": key, "parent": parent, "type": typ, "track": track,
            "subject": subject or f"[BE] {key}", "phase": "1", "wave": wave, "step": "1", "points": "2",
            "assignee": assignee, "area": area, "platform": "", "service": service, "dependsOn": deps,
            "description": description, "tier": "0"}


LINEAGE = {"createThing": {"contract": "things", "verb": "POST", "path": "/things"},
           "getThing": {"contract": "things", "verb": "GET", "path": "/things/{id}"}}


def plan():
    return [
        row("SVC-THING", "Epic", service="ThingService", assignee="Pranay Shinde", seq="1"),
        row("SVC-THING-CORE", "Feature", "SVC-THING", service="ThingService", seq="2"),
        row("MIG-THING", "Task", "SVC-THING-CORE", track="Database", seq="3", subject="[DB] Migration: things",
            description="Things. Tables: thing.thing, thing.part. Source DDL: backend/thing.sql."),
        row("SVC-THING-CORE-1", "Task", "SVC-THING-CORE", seq="4", deps="MIG-THING", service="ThingService",
            subject="[BE] ThingService: createThing, getThing"),
        row("APP-MOB-GST-001", "Task", "SVC-THING-CORE", track="Frontend", seq="5",
            deps="SVC-THING-CORE-1 MIG-THING", subject="[FE] GST-001 Thing Screen", area="MOB"),
    ]


SCHED = {"assign": {"MIG-THING": "Hrushikant Patkar", "SVC-THING-CORE-1": "Surendra",
                    "APP-MOB-GST-001": "Chitrangi Mestry"},
         "start": {"MIG-THING": 0.0, "SVC-THING-CORE-1": 6.0, "APP-MOB-GST-001": 60.0}}


def mapped(**extra):
    mp = {f"VERSION-W{n}": 69 + n for n in range(1, 8)}
    mp.update({f"VERSION-S{n}": 200 + n for n in range(1, 14)})
    mp.update({"_relations": [], "SVC-THING": 100, "SVC-THING-CORE": 101, "MIG-THING": 102,
               "MIG-THING#thing.thing": 103})
    mp.update(extra)
    return mp


def build(rows=None, mp=None, retire=(), unexplained=(), release="r1"):
    return rel.build(rows or plan(), mp or mapped(), SCHED, LINEAGE, list(retire), list(unexplained), release)


def by_key(bundle):
    return {t["key"]: t for t in bundle["tickets"]}


def test_pushed_keys_are_never_created_and_new_ones_come_parents_first():
    b, errors = build()
    assert errors == []
    create = b["create"]
    assert not set(create) & set(b["ids"])
    assert "MIG-THING#thing.part" in create and "MIG-THING#thing.thing" not in create
    known = set(b["ids"])
    tickets = by_key(b)
    for k in create:
        parent = tickets[k]["parent"]
        assert parent is None or parent in known, f"{k} comes before its parent {parent}"
        known.add(k)
    assert create.index("SVC-THING-CORE-1") < create.index("SVC-THING-CORE-1#createThing")


def test_sub_tasks_follow_push_openproject():
    b, _ = build()
    subs = sorted(k for k in by_key(b) if "#" in k)
    assert subs == sorted(["MIG-THING#thing.thing", "MIG-THING#thing.part", "SVC-THING-CORE-1#createThing",
                           "SVC-THING-CORE-1#getThing", "APP-MOB-GST-001#build", "APP-MOB-GST-001#wire",
                           "APP-MOB-GST-001#test"])
    assert by_key(b)["SVC-THING-CORE-1#createThing"]["subject"] == "[BE] createThing: POST /things"


def test_pointer_body_holds_summary_key_artefacts_adam_pull_and_release():
    b, _ = build(release="r3")
    t = by_key(b)["SVC-THING-CORE-1"]
    p = t["pointer"]
    assert p.splitlines()[0] == "**ThingService: createThing, getThing**"
    assert "- Key: `SVC-THING-CORE-1`" in p
    assert "`operation things#createThing`" in p and "`operation things#getThing`" in p
    assert f"- {rel.POINTER_PREFIX} `/ticket %ID%`" in p
    assert f"{rel.RELEASE_PREFIX}`r3`" in p
    assert by_key(b)["MIG-THING"]["builds"] == ["table thing.thing", "table thing.part"]
    assert by_key(b)["MIG-THING#thing.part"]["builds"] == ["table thing.part"]
    assert by_key(b)["APP-MOB-GST-001#wire"]["builds"] == ["screen GST-001"]
    assert by_key(b)["SVC-THING"]["builds"] == ["service ThingService"]


def test_pointer_differs_between_releases_only_on_the_release_line():
    """op-release.rb does not rewrite a New ticket whose pointer differs only by the release it was written at."""
    one = by_key(build(release="r1")[0])["SVC-THING-CORE-1"]["pointer"]
    two = by_key(build(release="r2")[0])["SVC-THING-CORE-1"]["pointer"]

    def norm(text):   # what op-release.rb's norm lambda does
        return "\n".join(l for l in text.replace("\r\n", "\n").split("\n")
                         if not l.startswith(rel.RELEASE_PREFIX)).strip()

    assert one != two and norm(one) == norm(two)


def test_long_artefact_lists_are_capped():
    tables = ", ".join(f"s.t{i}" for i in range(rel.MAX_BUILDS + 5))
    rows = plan()
    rows[2] = dict(rows[2], description=f"Big. Tables: {tables}. Source DDL: x.sql.")
    p = by_key(build(rows=rows)[0])["MIG-THING"]["pointer"]
    assert "and 5 more (all listed in ADAM)" in p and "`table s.t64`" not in p


def test_comment_is_marked_and_filled_on_the_server():
    b, _ = build()
    assert rel.COMMENT_MARKER in b["comment"] and "%ID%" in b["comment"] and "%KEY%" in b["comment"]
    assert "release r1" in b["comment"]
    assert b["markers"] == {"pointer": rel.POINTER_PREFIX, "release": rel.RELEASE_PREFIX,
                            "comment": rel.COMMENT_MARKER}


def test_assignee_alias_sprint_version_and_accountable():
    t = by_key(build()[0])
    assert t["SVC-THING-CORE-1"]["assignee"] == "Surendra Loke"          # OP_NAME alias
    assert t["SVC-THING-CORE-1"]["responsible"] == "Pranay Shinde"       # the service epic's owner
    # two-week sprints (1 October): day 6 is Sprint 1, day 60 Sprint 7; the version is "Sprint n"
    assert t["SVC-THING-CORE-1"]["sprint"] == 1 and t["SVC-THING-CORE-1"]["version"] == 201
    assert t["SVC-THING-CORE-1"]["version_key"] == "VERSION-S1"
    assert t["APP-MOB-GST-001"]["sprint"] == 7 and t["APP-MOB-GST-001"]["version"] == 207
    assert t["SVC-THING-CORE-1#getThing"]["assignee"] == "Surendra Loke"  # a sub-task takes its task's
    assert t["SVC-THING-CORE-1#getThing"]["set_version"] is True
    assert t["SVC-THING"]["set_version"] is False and t["SVC-THING"]["version"] is None
    assert t["SVC-THING-CORE-1#getThing"]["sequence"] == 4


def test_links_are_reduced_and_edges_kept_whole():
    b, _ = build()
    assert ["APP-MOB-GST-001", "MIG-THING"] in b["edges"]
    assert ["APP-MOB-GST-001", "MIG-THING"] not in b["links"]            # implied through SVC-THING-CORE-1
    assert sorted(b["links"]) == [["APP-MOB-GST-001", "SVC-THING-CORE-1"], ["SVC-THING-CORE-1", "MIG-THING"]]
    assert b["tasks"] == ["MIG-THING", "SVC-THING-CORE-1", "APP-MOB-GST-001"]


def test_two_keys_on_one_id_are_refused():
    _, errors = build(mp=mapped(**{"SVC-THING-CORE-1": 102}))
    assert any("id #102 is mapped to 2 keys" in e for e in errors)


def test_a_new_ticket_whose_parent_is_nowhere_is_refused():
    rows = plan() + [row("ORPHAN-1", "Task", "NO-SUCH-FEATURE", seq="9")]
    _, errors = build(rows=rows)
    assert any("ORPHAN-1: its parent NO-SUCH-FEATURE" in e for e in errors)


def test_a_cycle_is_refused():
    rows = plan()
    rows[2] = dict(rows[2], dependsOn="APP-MOB-GST-001")
    b, errors = build(rows=rows)
    assert any("cycle" in e for e in errors) and b["links"] == []


def test_retire_and_unexplained():
    mp = mapped(**{"SVC-OLD": 200, "SVC-OLD#x": 201, "SVC-GONE": 202,
                   "SVC-THING-CORE-1#getThing": 300,          # pushed and still planned
                   "MIG-THING#thing.old": 301,                # stale: its table left the plan
                   "SVC-THING-CORE-2#createThing": 302})      # a sub-task whose task key was never mapped
    retire = [("SVC-OLD", "defer", "on hold because"), ("SVC-OLD#x", "defer", "on hold because"),
              ("NEVER-PUSHED", "merge", "not in the map, dropped")]
    b, errors = build(mp=mp, retire=retire, unexplained=["SVC-GONE"])
    assert errors == []
    assert [(r["key"], r["id"], r["action"]) for r in b["retire"]] == [("SVC-OLD", 200, "defer"),
                                                                        ("SVC-OLD#x", 201, "defer")]
    why = {u["key"]: u["why"] for u in b["unexplained"]}
    assert why["SVC-GONE"].startswith("out of tasks.csv")
    assert why["MIG-THING#thing.old"] == "sub-task stale: its operation or table is no longer in the plan"
    assert "SVC-THING-CORE-2#createThing" in why and "work is on SVC-THING-CORE-1#createThing (new)" in \
        why["SVC-THING-CORE-2#createThing"]
    assert rel.unexplained_kind({"why": why["MIG-THING#thing.old"]}) == "stale sub-task, work left the plan"


def test_a_planned_key_in_the_retire_list_is_refused():
    _, errors = build(retire=[("MIG-THING", "defer", "x")])
    assert any("in the plan and in the retire list" in e for e in errors)


def test_summary_line_strips_the_track_tag_and_stays_one_line():
    assert rel.summary_line("[FE] GST-001  Thing\nScreen") == "GST-001 Thing Screen"
    assert len(rel.summary_line("[BE] " + "x" * 400)) == 200


def test_release_tag_shape():
    assert rel.TAG.match("r1") and rel.TAG.match("r12") and not rel.TAG.match("v1") and not rel.TAG.match("r1a")


@pytest.mark.skipif(not (DOCS / "tasks.csv").exists(), reason="package data not present")
def test_real_bundle_invariants():
    rows = list(csv.DictReader((DOCS / "tasks.csv").open(encoding="utf-8")))
    mp = json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))
    sched = json.loads((DOCS / "block-a-schedule.json").read_text(encoding="utf-8"))
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    _, retire_plan, unexplained = rel._load("op_retire_t", "op-retire.py").build_plan()
    b, errors = rel.build(rows, mp, sched, lineage, retire_plan, unexplained, "r1")
    assert errors == []
    ids = b["ids"]
    assert len(set(ids.values())) == len(ids)                                   # guard
    tickets = by_key(b)
    assert len(tickets) == len(b["tickets"])                                    # one entry per key
    known = set(ids)
    for k in b["create"]:
        assert k not in ids
        assert tickets[k]["parent"] is None or tickets[k]["parent"] in known
        known.add(k)
    for a, d in b["links"] + b["edges"]:
        assert a in tickets and d in tickets
    assert set(map(tuple, b["links"])) <= set(map(tuple, b["edges"]))
    for t in b["tickets"]:
        assert f"`{t['key']}`" in t["pointer"] and "`/ticket %ID%`" in t["pointer"]
        assert len(t["subject"]) <= 255
    planned = set(tickets)
    left = {r["key"] for r in b["retire"]} | {u["key"] for u in b["unexplained"]}
    assert not planned & left
    pushed_keys = {k for k in mp if not k.startswith(("_", "VERSION")) and isinstance(mp[k], int)}
    assert pushed_keys <= planned | left                                        # every pushed ticket is accounted for
    json.dumps(b)                                                               # serialisable as is


@pytest.mark.skipif(not (DOCS / "tasks.csv").exists(), reason="package data not present")
def test_main_records_the_git_blob_of_each_input(tmp_path, monkeypatch):
    """op-release-server.sh refuses a bundle whose inputs differ from the files at the tag."""
    import subprocess
    import sys
    out = tmp_path / "bundle.json"
    monkeypatch.setattr(sys, "argv", ["op-release.py", "--release", "r1", "--out", str(out), "--no-key-check",
                                      "--project", "999"])
    assert rel.main() == 0
    b = json.loads(out.read_text(encoding="utf-8"))
    assert list(b)[:4] == ["release", "built_from", "built_at", "inputs"]
    for f in rel.INPUTS:
        blob = subprocess.run(["git", "hash-object", f"handoff/service-docs/{f}"], cwd=ROOT, capture_output=True,
                              check=True).stdout.decode().strip()
        assert re.fullmatch(r"[0-9a-f]{40}", b["inputs"][f]) and b["inputs"][f] == blob
    # the server greps these lines out of the file as written
    text = out.read_text(encoding="utf-8")
    assert '"release": "r1"' in text and f'"tasks.csv": "{b["inputs"]["tasks.csv"]}"' in text


def test_main_refuses_an_empty_map_against_the_archived_project(tmp_path, monkeypatch):
    """Fresh start (3 October, CHG-GTR-001): with no pushed ticket, project 153 would get every ticket twice."""
    import sys
    if rel.pushed(json.loads((DOCS / "pms-map.json").read_text(encoding="utf-8"))):
        pytest.skip("pms-map.json holds pushed tickets")
    monkeypatch.setattr(sys, "argv", ["op-release.py", "--release", "r1", "--out", str(tmp_path / "b.json"),
                                      "--no-key-check"])
    assert rel.main() == 1 and not (tmp_path / "b.json").exists()


def test_main_refuses_a_non_release_tag(monkeypatch):
    import sys
    monkeypatch.setattr(sys, "argv", ["op-release.py", "--release", "v1"])
    assert rel.main() == 2


def test_sprint_from_the_schedule_wins_and_is_capped_at_13():
    sched = dict(SCHED, sprint={"SVC-THING-CORE-1": 3, "APP-MOB-GST-001": 15})
    b, _ = rel.build(plan(), mapped(), sched, LINEAGE, [], [], "r2")
    t = by_key(b)
    assert t["SVC-THING-CORE-1"]["sprint"] == 3 and t["SVC-THING-CORE-1"]["version"] == 203
    assert t["APP-MOB-GST-001"]["sprint"] == 13                         # past 2 April: planned into Sprint 13
    assert [v["name"] for v in b["sprint_versions"]][:2] == ["Sprint 1", "Sprint 2"] and len(b["sprint_versions"]) == 13


def test_accountable_written_on_the_row_wins():
    rows = plan()
    rows[3] = dict(rows[3], accountable="Tanmay Dukhande")
    t = by_key(build(rows=rows)[0])
    assert t["SVC-THING-CORE-1"]["responsible"] == "Tanmay Dukhande"


def test_old_epics_and_features_are_regrouped_not_unexplained():
    rows = [r for r in plan()]
    retire, unexp = rel.regroup(rows, mapped(), [], ["SVC-OLD", "SVC-OLD-GROUP", "SVC-GONE-1"], "r2",
                                structure={"SVC-OLD", "SVC-OLD-GROUP"})
    assert [(k, a) for k, a, _ in retire] == [("SVC-OLD", "regroup"), ("SVC-OLD-GROUP", "regroup")]
    assert unexp == ["SVC-GONE-1"]                                      # a task with no reason stays unexplained
