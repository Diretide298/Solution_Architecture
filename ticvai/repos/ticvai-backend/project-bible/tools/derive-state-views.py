#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give every state of a client-verified screen the look its client-approved design draws for it.

**21 October 2026, CHG-R9UI-003** (the lead: "I wanna get all of those changes out now.."). WEB-007's seat page
(#31848) was built with a bare error page while the approved guest web prototype draws its errors as the WEB-029
status card, its loading as the turnstile loader and its waiting step as a dashed note. A screen's `states` were one
line of generator text each; nothing said what a state looks like, so nothing in the ticket did either.

**What it writes.** From `screens/_state-patterns.yaml` (the patterns each platform's approved prototype or board
draws, and which pattern each state shows):

  screens/P*.yaml                 `wireframe.stateViews` on every client-verified screen: {state: "<code>/<pattern>"}
                                  for each state the approved design draws, in the screen's state order. A state it
                                  does not draw gets no entry: it is a design gap on docs/active/left-out.yaml.
                                  Invisible metadata (check-approved-ui compares no wireframe field), written the way
                                  derive-board-anchors writes (PyYAML safe_dump, width 100, the checkout's line
                                  endings) and only when a view changed, so a second run writes nothing.
  handoff/design-frames.json      per screen: the approved prototype and view, the board frame and the file
                                  `adam_pull` writes for it (`wireframe-<anchor>.html`), every state's pattern (with
                                  the frame it is drawn in, when a board draws it) or its left-out line, the design
                                  tokens, the visual check's viewports, and the generated frames under
                                  wireframes/incoming/ that are structure only, not the look. The ticket text
                                  (ticket_done.design_lines), the frontend spec pages and ADAM read this file.
  wireframes/incoming/README.md   which folders there are captures of a client-approved prototype (the look) and
                                  which are frames generated from the screen YAML (structure only, not the look).

    python3 tools/derive-state-views.py [--apply]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PATTERNS = SCREENS / "_state-patterns.yaml"
LEFT_OUT = ROOT / "docs" / "active" / "left-out.yaml"
OUT = ROOT / "handoff" / "design-frames.json"
INCOMING = ROOT / "wireframes" / "incoming"
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
LF, CRLF = chr(10), chr(13) + chr(10)
SHARED_TOKENS = "screens/_design-tokens.yaml"
STRUCTURE_ONLY = "structure only, not the look"


def dump(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def load_patterns(path: Path = PATTERNS) -> dict:
    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}


def load_left_out(path: Path = LEFT_OUT) -> list:
    return list(((yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("items") or [])) if path.exists() else []


def gap_index(items: list) -> dict:
    """{(platform, state): left-out id} for the design gaps (a screen list, when given, narrows it)."""
    out = {}
    for it in items:
        if not str(it.get("kind") or "").startswith("design-gap") or not it.get("states"):
            continue
        for st in it["states"]:
            for sid in it.get("screens") or ["*"]:
                out[(str(it.get("platform")), st, sid)] = it["id"]
    return out


def gap_of(gaps: dict, code: str, state: str, sid: str):
    return gaps.get((code, state, sid)) or gaps.get((code, state, "*"))


def view_of(platform: dict, sid: str, state: str):
    """The pattern id (without the platform) a state of a screen shows, or None when the design does not draw it."""
    own = ((platform.get("screens") or {}).get(sid) or {}).get(state)
    return own or (platform.get("states") or {}).get(state)


def client_verified(s: dict) -> bool:
    return isinstance(s.get("wireframe"), dict) and s["wireframe"].get("provenance") == "client-verified"


def state_views(s: dict, code: str, mapping: dict) -> dict:
    platform = (mapping.get("platforms") or {}).get(code) or {}
    out = {}
    for st in (s.get("states") or {}):
        v = view_of(platform, s["id"], st)
        if v:
            out[st] = f"{code}/{v}"
    return out


def incoming_folders() -> dict:
    """{folder: {"kind": "capture"|"generated", "prototype": ..., "screens": [ids]}} under wireframes/incoming/."""
    out = {}
    if not INCOMING.exists():
        return out
    for d in sorted(p for p in INCOMING.iterdir() if p.is_dir()):
        man = d / "manifest.json"
        kind, proto = "generated", None
        if man.exists():
            try:
                m = json.loads(man.read_text(encoding="utf-8"))
            except ValueError:
                m = {}
            if m.get("prototype") and m.get("captured"):
                kind, proto = "capture", m["prototype"]
        ids = sorted({re.match(r"([a-z]{2,5}-\d{3,4})", f.stem, re.I).group(1).upper()
                      for f in d.glob("*.html") if re.match(r"([a-z]{2,5}-\d{3,4})", f.stem, re.I)})
        out[d.name] = {"kind": kind, "prototype": proto, "screens": ids}
    return out


def tokens_of(code: str, mapping: dict) -> dict:
    p = (mapping.get("platforms") or {}).get(code) or {}
    if p.get("tokens"):
        return {"file": p["tokens"], "from": p.get("tokensFrom") or "", "approved": True}
    return {"file": SHARED_TOKENS, "from": "the shared tokens (no client-approved design for this app yet)",
            "approved": False}


def frames_entry(s: dict, code: str, mapping: dict, gaps: dict, folders: dict) -> dict:
    w = s.get("wireframe") or {}
    platform = (mapping.get("platforms") or {}).get(code) or {}
    board = str(w.get("board") or "")
    anchor = board.split("#", 1)[1] if "#" in board else ""
    pr = w.get("prototype") or {}
    generated = sorted(f"wireframes/incoming/{n}/{f.name}" for n, x in folders.items()
                       if x["kind"] == "generated" and s["id"] in x["screens"]
                       for f in (INCOMING / n).glob(f"{s['id'].lower()}*.html"))
    captured = sorted(f"wireframes/incoming/{n}/{s['id'].lower()}.html" for n, x in folders.items()
                      if x["kind"] == "capture" and s["id"] in x["screens"])
    e = {"platform": code, "clientVerified": client_verified(s), "tokens": tokens_of(code, mapping),
         "structureOnly": generated, "structureOnlyLabel": STRUCTURE_ONLY,
         "layoutLabel": f"the screen's layout (template, regions, pattern) is {STRUCTURE_ONLY}"}
    if not e["clientVerified"]:
        return e
    e.update({
        "prototype": {"file": pr.get("file"), "rev": pr.get("rev"), "view": " ".join(str(pr.get("view") or "").split()),
                      "match": pr.get("match"), "verified": str(pr.get("verified") or "") or None},
        "board": board, "anchor": anchor, "pulled": f"wireframe-{anchor}.html" if anchor else None,
        "captures": captured, "viewports": list(platform.get("viewports") or []), "states": {}, "gaps": {}})
    for st in (s.get("states") or {}):
        v = view_of(platform, s["id"], st)
        if v:
            pat = (platform.get("patterns") or {}).get(v) or {}
            fr_ = pat.get("frame")
            e["states"][st] = {"pattern": f"{code}/{v}", "name": pat.get("name") or v,
                               "prototype": (platform.get("prototypes") or {}).get(pat.get("prototype")),
                               "where": pat.get("where"),
                               # a frame the package drew sits on its companion board (CHG-R9UI-005)
                               "frame": f"{pat.get('board') or platform.get('board')}#{fr_}" if fr_ else None,
                               "pulled": f"wireframe-{fr_}.html" if fr_ else None}
            if pat.get("status"):
                e["states"][st]["status"] = pat["status"]
        else:
            e["gaps"][st] = gap_of(gaps, code, st, s["id"])
    return e


def readme(folders: dict) -> str:
    L = ["# wireframes/incoming: captures and generated frames", "",
         "> Generated by `tools/derive-state-views.py` (CHG-R9UI-003). **Do not edit.**", "",
         "Two kinds of frame sit here, and only one of them is the look.", "",
         "- **Captures** of a client-approved prototype (a folder whose `manifest.json` names the prototype and what was",
         "  captured): these are the approved look, view by view.",
         f"- **Generated frames**, drawn from the screen YAML for a design batch: **{STRUCTURE_ONLY}**. They are styled",
         "  with the shared tokens (Manrope, the till's palette) whatever the app; a guest screen is never built to look",
         "  like one. The look of a client-verified screen is its prototype view and board frame",
         "  (handoff/design-frames.json; the ticket's \"Design (client-approved, build identical)\" section).", "",
         "| Folder | Kind | Screens |", "|---|---|---|"]
    for n, x in folders.items():
        kind = (f"capture of `{x['prototype']}` (the look)" if x["kind"] == "capture"
                else f"generated from the screen YAML ({STRUCTURE_ONLY})")
        L.append(f"| {n} | {kind} | {', '.join(x['screens'])} |")
    return "\n".join(L) + "\n"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    mapping = load_patterns()
    gaps = gap_index(load_left_out())
    folders = incoming_folders()
    frames, changed, n_view, n_gap = {}, [], 0, 0
    for f in sorted(SCREENS.glob("P*.yaml")):
        raw = f.open(encoding="utf-8", newline="").read()
        doc = yaml.load(raw, Loader=LOADER) or {}
        code = (doc.get("platform") or {}).get("code") or f.name.split("-")[0]
        in_form = dump(doc) == raw.replace(CRLF, LF)
        touched = False
        for s in doc.get("screens") or []:
            w = s.get("wireframe")
            if client_verified(s):
                sv = state_views(s, code, mapping)
                n_view += len(sv)
                n_gap += len([x for x in (s.get("states") or {}) if x not in sv])
                if sv and w.get("stateViews") != sv:
                    w["stateViews"] = sv
                    touched = True
                elif not sv and "stateViews" in w:
                    del w["stateViews"]
                    touched = True
            elif isinstance(w, dict) and "stateViews" in w:
                del w["stateViews"]                       # only a client-verified screen has an approved look
                touched = True
            frames[s["id"]] = frames_entry(s, code, mapping, gaps, folders)
        if touched:
            # written as derive-board-anchors writes (safe_dump, width 100): a file a hand edit left out of that form
            # (P04 after CHG-R8RW-010) comes back to it, the same data
            if not in_form:
                print(f"  {f.name} was not in the derivers' form (safe_dump, width 100); written in it")
            out = dump(doc)
            if CRLF in raw:
                out = out.replace(LF, CRLF)
            if out != raw:
                changed.append(f)
                if a.apply:
                    f.open("w", encoding="utf-8", newline="").write(out)
    patterns = {f"{c}/{k}": dict(v, platform=c, prototypeFile=(p.get("prototypes") or {}).get(v.get("prototype")),
                                 frame=(f"{v.get('board') or p.get('board')}#{v['frame']}" if v.get("frame") else None))
                for c, p in (mapping.get("platforms") or {}).items() for k, v in (p.get("patterns") or {}).items()}
    body = json.dumps({"note": "Generated by tools/derive-state-views.py from screens/_state-patterns.yaml, the screens "
                               "and docs/active/left-out.yaml (CHG-R9UI-003). Do not edit.",
                       "patterns": patterns, "screens": frames}, indent=1, ensure_ascii=False, sort_keys=False) + "\n"
    print(f"derive-state-views: {n_view} state(s) with a view, {n_gap} without (design gaps) on client-verified "
          f"screens; {len(changed)} screen file(s) {'written' if a.apply else 'would change'}")
    for f in changed:
        print(f"  {'written' if a.apply else 'would write'}  {f.name}")
    if a.apply:
        OUT.write_text(body, encoding="utf-8")
        (INCOMING / "README.md").write_text(readme(folders), encoding="utf-8")
    elif changed:
        print("  (dry run: pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
