#!/usr/bin/env python3
"""A feature ticket's screens and operations, and what each of its frontend tickets is scoped to (CHG-SWP-001).

**14 October 2026** (batch SWP, the sweep after #27741). A developer's agent stopped on AM-IDENTITY-SECURITY-P02
(#27741, Identity & Security on the guest app): the feature listed `searchGuests` and the three wishlist operations,
which none of its screens (GST-010, GST-042, GST-073) calls, and `searchGuests` is a staff operation on a guest
ticket. Both are read off handoff/service-docs/plan-tasks.csv by the same few rules, so they live here once:

  features(rows, screens)   {feature key: Feature} for every Feature row with at least one screen: the screens its
                            tasks build, the operations its tasks build, its block and its platforms
  scope(task, sid, ...)     the operations a frontend task of screen `sid` is answerable for: the screen's, or its
                            setup slice ("In the slice: ..."), or the rest of the screen after the sibling's slice

**The ticket #27741 itself is not baselined.** Batch GAP fixes it (and the composition rule in
build-service-docs.py) in parallel; its findings are `strict` in the guards that use this (audit_guard.Guard.add),
so they fail until the fix lands and can never be written into the baseline.

Imported, no main.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

import ticket_done as td

# The feature tickets whose findings may not be baselined: the case that raised the class, fixed by its own batch.
UNBASELINED = {
    "AM-IDENTITY-SECURITY-P02": "#27741, the case that raised the class; batch GAP fixes it on 14 October 2026",
}
SLICE = re.compile(r"In the slice:\s*([A-Za-z0-9, ]+?)(?:\)|\.|;|$)")


@dataclass
class Feature:
    key: str
    block: str
    subject: str
    screens: set = field(default_factory=set)          # screen ids its tasks build
    ops: dict = field(default_factory=dict)            # operationId -> the task key that builds it
    frontend: list = field(default_factory=list)       # [(task row, screen id)] its frontend tasks
    platforms: set = field(default_factory=set)        # P01, P02 ... of its screens


def plan_rows(root: Path) -> list:
    """Every plan row but the per-part rows (a key with '#'), from handoff/service-docs/plan-tasks.csv."""
    plan = Path(root) / "handoff" / "service-docs" / "plan-tasks.csv"
    if not plan.exists():
        return []
    with plan.open(encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh) if "#" not in r["key"]]


def screen_ops(s: dict) -> set:
    return {a["operationId"] for a in s.get("apis") or [] if isinstance(a, dict) and a.get("operationId")}


def slice_of(r: dict | None):
    m = SLICE.search((r or {}).get("description") or "")
    return {x.strip() for x in m.group(1).split(",") if x.strip()} if m else None


def scope(task: dict, sid: str, screens: dict, by_key: dict) -> set:
    """The operations a frontend task of `sid` builds against: a setup task its slice, a rest-of-the-screen task the
    screen's other operations, any other task every operation the screen binds."""
    ops = screen_ops(screens[sid])
    sl = slice_of(task)
    if sl is not None:
        return ops & sl
    if task["key"].endswith("-REST"):
        return ops - (slice_of(by_key.get(task["key"][:-len("-REST")])) or set())
    return ops


def builders(rows) -> dict:
    """operationId -> {task keys that build it} (tests build nothing; a 'Builds:' lead names the contract too)."""
    out: dict = {}
    for r in rows:
        if r.get("type") != "Task" or r.get("track") == "Test":
            continue
        for b in td.builds_of(r, "", {}):
            kind, _, name = b.partition(" ")
            if kind == "operation":
                out.setdefault(name.split("#")[-1], set()).add(r["key"])
    return out


def features(rows, screens: dict, platform_of: dict) -> dict:
    """{feature key: Feature} for every Feature whose tasks build at least one screen. `screens` is {id: screen}
    (merged bindings applied, td.merge_bindings), `platform_of` {screen id: platform code}."""
    kids: dict = {}
    for r in rows:
        kids.setdefault(r.get("parent") or "", []).append(r)
    out = {}
    for f in rows:
        if f.get("type") != "Feature":
            continue
        feat = Feature(f["key"], f.get("block") or "", f.get("subject") or "")
        for c in kids.get(f["key"], []):
            if c.get("type") != "Task" or c.get("track") == "Test":
                continue
            for b in td.builds_of(c, "", {}):
                kind, _, name = b.partition(" ")
                if kind == "screen" and name in screens:
                    feat.screens.add(name)
                    feat.platforms.add(str(platform_of.get(name) or "")[:3])
                    if c.get("track") == "Frontend":
                        feat.frontend.append((c, name))
                elif kind == "operation":
                    feat.ops.setdefault(name.split("#")[-1], c["key"])
        if feat.screens:
            out[f["key"]] = feat
    return out
