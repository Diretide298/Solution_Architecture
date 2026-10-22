#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every state of a client-verified screen has the look its client-approved design draws, or is a listed design gap.

**21 October 2026, CHG-R9UI-003** (the lead: "I wanna get all of those changes out now.."). The seat page WEB-007
(#31848) was built with a bare error page: the screen's states were one line of generator text each, the ticket named
no design, and nothing mapped a state to what the approved prototype draws (the WEB-029 status card for an error, the
turnstile loader for loading, the dashed note for a step waiting on a choice). screens/_state-patterns.yaml now maps
each platform's states to the patterns its approved prototype or board draws, and tools/derive-state-views.py writes
them into the screens (`wireframe.stateViews`) and handoff/design-frames.json, which the ticket text reads. This fails
when that chain breaks:

  SV-NO-VIEW     a client-verified screen has a state with no view, and docs/active/left-out.yaml names no design gap
                 for that platform and state: the developer would have to invent the look
  SV-STALE       a screen's wireframe.stateViews is not what the mapping gives (derive-state-views.py not run, or the
                 field edited by hand), or handoff/design-frames.json does not match the screens
  SV-PATTERN     a pattern cites a prototype file that is not there, a `find` text the file does not hold (a bundled
                 prototype is read from its decoded template), or a board frame the board does not have; or a state
                 maps to a pattern that does not exist. A pattern must point at a real drawing: never an invented one.
                 A frame the package drew (r9, CHG-R9UI-005: `board` on wireframes/states/) proves itself on that board,
                 names the approved prototype whose look it is drawn in, and its board says it is "drawn by the package
                 from the approved design (r9), not yet seen by the client"
  SV-LEFT-OUT    a left-out item lacks a field the rule needs (id, kind, platform, what, source, reason, target, added,
                 change), an id is used twice, or a design gap names a state that has a view now (the gap is closed:
                 take the line off the list)

Every finding is strict: never baselined. Read-only.

    python3 tools/check-state-views.py [--all]
    python3 tools/check-state-views.py --probe     # shows the check failing on a client-verified state with no view
                                                   # and no left-out line (WEB-007's error), then passing on the tree
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

_spec = importlib.util.spec_from_file_location("derive_state_views", Path(__file__).resolve().parent / "derive-state-views.py")
dsv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dsv)

RULES = {
    "SV-NO-VIEW": "a client-verified screen's state has no approved look and is not a listed design gap (CHG-R9UI-003)",
    "SV-STALE": "a screen's wireframe.stateViews or handoff/design-frames.json is not what the mapping gives",
    "SV-PATTERN": "a state pattern cites a prototype, text or board frame that is not there, or no such pattern",
    "SV-LEFT-OUT": "a left-out item lacks a required field, repeats an id, or names a gap that now has a view",
}
STATUS_DRAWN = "drawn by the package from the approved design (r9), not yet seen by the client"
LEFT_OUT_FIELDS = ("id", "kind", "platform", "what", "source", "reason", "target", "added", "change")


def prototype_text(rel: str, cache: dict) -> str | None:
    """The prototype's text; a bundled prototype (a single-file bundle) adds its decoded template."""
    if rel in cache:
        return cache[rel]
    f = g.ROOT / rel
    if not f.is_file():
        cache[rel] = None
        return None
    raw = f.read_text(encoding="utf-8", errors="replace")
    parts = [raw]
    for ln in raw.split("\n"):
        if ln.startswith('"<!DOCTYPE'):
            try:
                parts.append(json.loads(ln))
            except ValueError:
                pass
    cache[rel] = "\n".join(parts)
    return cache[rel]


def board_anchors(rel: str, cache: dict) -> set:
    key = "anchors:" + rel
    if key not in cache:
        f = g.ROOT / rel
        import re
        cache[key] = set(re.findall(r'<section id="([^"]+)"', f.read_text(encoding="utf-8", errors="replace"))) \
            if f.is_file() else set()
    return cache[key]


def run(guard, screens: list, mapping: dict, items: list, frames: dict | None, cache: dict | None = None) -> dict:
    """Adds the findings to `guard`; returns counts. `screens`: [(platform code, screen dict)]."""
    cache = {} if cache is None else cache
    gaps = dsv.gap_index(items)
    plats = mapping.get("platforms") or {}
    # SV-PATTERN: every pattern points at a real drawing
    for code, p in sorted(plats.items()):
        pats = p.get("patterns") or {}
        for pid, pat in sorted(pats.items()):
            # a frame the package drew (CHG-R9UI-005) proves itself on its companion board, which must say what it is
            rel = pat.get("board") or (p.get("prototypes") or {}).get(pat.get("prototype"))
            text = prototype_text(rel, cache) if rel else None
            if pat.get("board"):
                if not (p.get("prototypes") or {}).get(pat.get("prototype")):
                    guard.add("SV-PATTERN", f"{code}/{pid}:look", f"{code}/{pid}: drawn by the package, but names no "
                              "approved prototype whose look it is drawn in", strict=True)
                if text is not None and STATUS_DRAWN not in text:
                    guard.add("SV-PATTERN", f"{code}/{pid}:status", f"{code}/{pid}: its board {rel} does not say the "
                              f"frames are {STATUS_DRAWN!r}", strict=True)
            if text is None:
                guard.add("SV-PATTERN", f"{code}/{pid}:prototype", f"{code}/{pid}: its prototype "
                          f"{pat.get('prototype')!r} ({rel}) is not a file of the package", strict=True)
                continue
            if not pat.get("find"):
                guard.add("SV-PATTERN", f"{code}/{pid}:find", f"{code}/{pid}: no `find` text proves the drawing "
                          "exists", strict=True)
            for t in pat.get("find") or []:
                if t not in text:
                    guard.add("SV-PATTERN", f"{code}/{pid}:{t}", f"{code}/{pid}: {rel} does not hold {t!r}",
                              strict=True)
            bd_ = pat.get("board") or p.get("board") or ""
            if pat.get("frame") and pat["frame"] not in board_anchors(bd_, cache):
                guard.add("SV-PATTERN", f"{code}/{pid}:frame", f"{code}/{pid}: the board {bd_} has no "
                          f"frame #{pat['frame']}", strict=True)
        for st, pid in sorted((p.get("states") or {}).items()):
            if pid not in pats:
                guard.add("SV-PATTERN", f"{code}:{st}", f"{code} state {st} maps to {pid}, no pattern of {code}",
                          strict=True)
        for sid, over in sorted((p.get("screens") or {}).items()):
            for st, pid in sorted((over or {}).items()):
                if pid not in pats:
                    guard.add("SV-PATTERN", f"{sid}:{st}", f"{sid} state {st} maps to {pid}, no pattern of {code}",
                              strict=True)
    # SV-LEFT-OUT: the list is well formed
    seen = {}
    for it in items:
        miss = [k for k in LEFT_OUT_FIELDS if not str(it.get(k) or "").strip()]
        if miss:
            guard.add("SV-LEFT-OUT", f"{it.get('id')}:fields", f"left-out item {it.get('id') or '(no id)'} has no "
                      + ", ".join(miss), strict=True)
        if it.get("id") in seen:
            guard.add("SV-LEFT-OUT", f"{it.get('id')}:dup", f"left-out id {it['id']} is used twice", strict=True)
        seen[it.get("id")] = it
    # SV-NO-VIEW and SV-STALE per screen; which gaps are used
    used, n_view, n_gap, n_cv = set(), 0, 0, 0
    for code, s in screens:
        if not dsv.client_verified(s):
            if (s.get("wireframe") or {}).get("stateViews"):
                guard.add("SV-STALE", f"{s['id']}:not-verified", f"{s['id']}: has wireframe.stateViews but is not "
                          "client-verified (derive-state-views.py removes them)", strict=True)
            continue
        n_cv += 1
        want = dsv.state_views(s, code, mapping)
        have = (s.get("wireframe") or {}).get("stateViews") or {}
        if have != want:
            guard.add("SV-STALE", s["id"], f"{s['id']}: wireframe.stateViews is not what screens/_state-patterns.yaml "
                      "gives (run tools/derive-state-views.py --apply)", strict=True)
        for st in (s.get("states") or {}):
            if st in want:
                n_view += 1
                continue
            gid = dsv.gap_of(gaps, code, st, s["id"])
            if gid:
                n_gap += 1
                used.add((code, st))
                continue
            guard.add("SV-NO-VIEW", f"{s['id']}:{st}", f"{s['id']} ({code}) state {st}: the approved design shows "
                      f"no look for it and docs/active/left-out.yaml has no design gap for {code} {st}", strict=True)
        if frames is not None:
            fe = (frames.get("screens") or {}).get(s["id"]) or {}
            if {k: v.get("pattern") for k, v in (fe.get("states") or {}).items()} != want:
                guard.add("SV-STALE", f"{s['id']}:frames", f"{s['id']}: handoff/design-frames.json does not match "
                          "its stateViews (run tools/derive-state-views.py --apply)", strict=True)
    # a design gap whose state has a view on every screen it names is closed
    for it in items:
        if it.get("kind") != "design-gap":
            continue
        for st in it.get("states") or []:
            if (str(it.get("platform")), st) not in used:
                guard.add("SV-LEFT-OUT", f"{it['id']}:{st}", f"{it['id']}: names {it.get('platform')} {st} as a "
                          "design gap, but no client-verified screen shows that state without a view now: take it "
                          "off the list", strict=True)
    return {"clientVerified": n_cv, "withView": n_view, "gaps": n_gap}


def load_all():
    screens = [(stem.split("-")[0], s) for stem, s in g.screens()]
    mapping = dsv.load_patterns()
    items = dsv.load_left_out()
    frames = g.load_json(g.ROOT / "handoff" / "design-frames.json", None)
    return screens, mapping, items, frames


def probe() -> int:
    """Remove WEB-007's error view and the platform's error mapping (nothing else draws it), with no left-out line:
    the check must fail with SV-NO-VIEW; then the real tree must pass."""
    screens, mapping, items, frames = load_all()
    m2 = copy.deepcopy(mapping)
    m2["platforms"]["P01"]["states"].pop("error", None)
    s2 = [(c, copy.deepcopy(s) if s["id"] == "WEB-007" else s) for c, s in screens]
    for c, s in s2:
        if s["id"] == "WEB-007":
            s["wireframe"].setdefault("stateViews", {}).pop("error", None)
    gp = g.Guard("check-state-views (probe)", RULES)
    run(gp, [(c, s) for c, s in s2 if s["id"] == "WEB-007"], m2, items, None)
    hit = [k for k in (gp.found.get("SV-NO-VIEW") or {}) if k == "WEB-007:error"]
    print(f"probe: WEB-007 state error with no view and no left-out line -> SV-NO-VIEW {'raised' if hit else 'NOT raised'}")
    gr = g.Guard("check-state-views", RULES)
    counts = run(gr, screens, mapping, items, frames)
    clean = not any(gr.found.values())
    print(f"probe: the real tree -> {'no finding' if clean else 'findings'} ({counts})")
    return 0 if hit and clean else 1


def main() -> int:
    g.force_utf8()
    if "--probe" in sys.argv[1:]:
        return probe()
    guard = g.Guard("check-state-views", RULES)
    screens, mapping, items, frames = load_all()
    if not mapping:
        guard.add("SV-PATTERN", "mapping", "screens/_state-patterns.yaml is missing", strict=True)
        return guard.finish()
    if frames is None:
        guard.add("SV-STALE", "design-frames", "handoff/design-frames.json is missing (run tools/derive-state-views.py "
                  "--apply)", strict=True)
    c = run(guard, screens, mapping, items, frames)
    guard.note(f"{c['clientVerified']} client-verified screens: {c['withView']} states with an approved look, "
               f"{c['gaps']} design gaps on docs/active/left-out.yaml")
    return guard.finish()


if __name__ == "__main__":
    raise SystemExit(main())
