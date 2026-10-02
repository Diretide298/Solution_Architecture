#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The client's design inputs from the meetings, checked, and carried to every design session.

**The wireframes Claude Design built were missing what the client said in the room** (1 October).
The batch bundles carried the screens, the operations, the schemas and the permissions, and none of
the design statements in the minutes: "the video plays without a loader", "a planner per venue",
"the group size is typed", the POS density asked for on 3 August. A session cannot apply a
requirement it was never handed.

**`handoff/design-inputs/mom-design-inputs.yaml` is authored, not derived.** One entry per design
input, each with its source (file, date, section), a short faithful text, the scope it applies to,
its status and what it supersedes. People add to it when a new MoM arrives; nothing regenerates it.
This tool only reads it:

1. **Validates it** -- ids unique, required fields present, status known, every `supersedes` naming
   an entry that exists, and every scope naming something real: `global`, a platform (`P02`), a
   module (`P02/Booking & Selection`, spelled as in `screens/P*.yaml`) or a screen id. A scope that
   names a retired screen fails the run, because an input that reaches no batch is an input lost.
2. **Writes `handoff/design-inputs/README.md`**, the readable copy: counts, sources, open
   questions, every input grouped by where it applies, and the superseded ones apart.
3. **Fills the generated blocks in the per-app guides** (`handoff/design-batches/apps/*/README.md`
   and `CLAUDE-DESIGN-RUN.md`) between `<!-- design-inputs:KEY -->` and `<!-- /design-inputs:KEY -->`,
   where KEY is `global` or a platform code. A guide with no markers is left alone.

`tools/export-design-batch.py` imports `for_screens()` and `render_batch()` from here, so every
batch's BRIEF.md and BUNDLE.md carry the inputs for its platform(s), module(s) and screens -- the
latest only: an entry another one supersedes is left out.

    python3 tools/build-design-inputs.py            # validate, write the README and the guide blocks
    python3 tools/build-design-inputs.py --check    # validate only; exit 1 on an error

Run by `tools/refresh.sh`, before `export-design-batch.py --all`.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "handoff" / "design-inputs" / "mom-design-inputs.yaml"
README = ROOT / "handoff" / "design-inputs" / "README.md"
APPS = ROOT / "handoff" / "design-batches" / "apps"

STATUSES = ("agreed", "client-requested", "open-question")
TOPICS = ("layout", "navigation", "components", "branding", "configurability", "flow", "states",
          "copy", "accessibility", "rtl", "offline", "devices", "motion", "density", "data-display",
          "hardware", "reporting", "other")
ID_RE = re.compile(r"^DI-\d{3,4}$")


# ---------------------------------------------------------------------------------------------
# reading
# ---------------------------------------------------------------------------------------------

_CACHE: dict = {}
# libyaml when installed: the screen files are large, and this module is imported by every export.
_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load() -> list[dict]:
    """The inputs, as authored."""
    if "inputs" not in _CACHE:
        doc = yaml.load(INDEX.read_text(encoding="utf-8"), Loader=_LOADER) or {}
        _CACHE["inputs"] = list(doc.get("inputs") or [])
    return _CACHE["inputs"]


def screen_index() -> tuple[dict, dict, set]:
    """screen id -> (platform, module, name); platform -> short name; every `Pxx/Module`."""
    if "screens" not in _CACHE:
        screens, plats, mods = {}, {}, set()
        for f in sorted((ROOT / "screens").glob("P*.yaml")):
            doc = yaml.load(f.read_text(encoding="utf-8"), Loader=_LOADER) or {}
            p = doc.get("platform") or {}
            code = p.get("code")
            plats[code] = p.get("shortName") or p.get("name") or code
            for s in doc.get("screens") or []:
                screens[s["id"]] = (code, s.get("module"), s.get("name"))
                if s.get("module"):
                    mods.add(f"{code}/{s['module']}")
        _CACHE["screens"] = (screens, plats, mods)
    return _CACHE["screens"]


def superseded_ids(inputs: list[dict]) -> dict:
    """id -> the id of the entry that supersedes it, or the decision that did (`superseded_by`)."""
    out = {}
    for e in inputs:
        for old in e.get("supersedes") or []:
            out[old] = e["id"]
    # **A decision can supersede a meeting input with no later meeting to say so** (2 October 2026, CHG-CLN-012):
    # the 19 September kitchen display decision superseded DI-077, ADR-0051 superseded DI-280. The entry then
    # carries `superseded_by: {ref, note}`, where ref is an ADR, a decision (DEC-), a change entry (CHG-) or a DI.
    for e in inputs:
        sb = e.get("superseded_by")
        if isinstance(sb, dict) and sb.get("ref") and e["id"] not in out:
            out[e["id"]] = str(sb["ref"])
    return out


SUPERSEDED_BY_REF = re.compile(r"^(DI-\d{3,4}|ADR-\d{4}|DEC-\d+|CHG-[A-Z]{2,6}-\d{3})$")


def active(inputs: list[dict] | None = None) -> list[dict]:
    """Every entry no later entry supersedes."""
    inputs = load() if inputs is None else inputs
    gone = superseded_ids(inputs)
    return [e for e in inputs if e["id"] not in gone]


# ---------------------------------------------------------------------------------------------
# validating
# ---------------------------------------------------------------------------------------------

def validate(inputs: list[dict]) -> list[str]:
    screens, plats, mods = screen_index()
    errs, seen = [], set()
    ids = {e.get("id") for e in inputs}
    for n, e in enumerate(inputs, 1):
        i = e.get("id") or f"entry {n}"
        if not ID_RE.match(str(e.get("id") or "")):
            errs.append(f"{i}: id must look like DI-001")
        if i in seen:
            errs.append(f"{i}: duplicate id")
        seen.add(i)
        src = e.get("source") or {}
        for k in ("file", "date"):
            if not src.get(k):
                errs.append(f"{i}: source.{k} missing")
        if src.get("date"):
            try:
                datetime.date.fromisoformat(str(src["date"]))
            except ValueError:
                errs.append(f"{i}: source.date {src['date']!r} is not YYYY-MM-DD")
        if src.get("file") and not (ROOT / src["file"]).exists():
            errs.append(f"{i}: source.file {src['file']} not found (paths are relative to ticvai/)")
        if not str(e.get("text") or "").strip():
            errs.append(f"{i}: text missing")
        if e.get("status") not in STATUSES:
            errs.append(f"{i}: status {e.get('status')!r} is not one of {', '.join(STATUSES)}")
        for t in e.get("topic") or []:
            if t not in TOPICS:
                errs.append(f"{i}: topic {t!r} unknown")
        scope = e.get("scope")
        if not scope or not isinstance(scope, list):
            errs.append(f"{i}: scope must be a non-empty list")
            scope = []
        for s in scope:
            s = str(s)
            if s == "global" or s in plats or s in mods or s in screens:
                continue
            if "/" in s:
                errs.append(f"{i}: module {s!r} does not exist (spell it as in screens/P*.yaml)")
            elif re.match(r"^P\d\d$", s):
                errs.append(f"{i}: platform {s!r} does not exist")
            else:
                errs.append(f"{i}: screen {s!r} does not exist")
        if "global" in scope and len(scope) > 1:
            errs.append(f"{i}: 'global' cannot be combined with a narrower scope")
        for old in e.get("supersedes") or []:
            if old not in ids:
                errs.append(f"{i}: supersedes {old}, which does not exist")
            elif old == e.get("id"):
                errs.append(f"{i}: supersedes itself")
        sb = e.get("superseded_by")
        if sb is not None:
            if not isinstance(sb, dict) or not str(sb.get("note") or "").strip():
                errs.append(f"{i}: superseded_by needs a ref and a note saying what replaced it")
            elif not SUPERSEDED_BY_REF.match(str(sb.get("ref") or "")):
                errs.append(f"{i}: superseded_by.ref {sb.get('ref')!r} is not a DI, ADR, DEC or CHG id")
            else:
                ref = str(sb["ref"])
                if ref.startswith("DI-") and ref not in ids:
                    errs.append(f"{i}: superseded_by {ref}, which does not exist")
                if ref.startswith("ADR-") and not list((ROOT / "docs" / "adr").glob(f"{ref[4:]}-*.md")):
                    errs.append(f"{i}: superseded_by {ref}, which has no file in docs/adr/")
                if ref.startswith("CHG-") and not list((ROOT / "changes" / "entries").glob(f"{ref}-*.yaml")):
                    errs.append(f"{i}: superseded_by {ref}, which is not a change entry")
    # **A chain must end.** A supersedes B supersedes A would drop both from every bundle.
    nxt = superseded_ids(inputs)
    for start in nxt:
        cur, hops = start, 0
        while cur in nxt and hops <= len(nxt):
            cur, hops = nxt[cur], hops + 1
        if hops > len(nxt):
            errs.append(f"{start}: supersedes chain loops")
    return errs


# ---------------------------------------------------------------------------------------------
# selecting and rendering
# ---------------------------------------------------------------------------------------------

def _level(tok: str) -> str:
    return "global" if tok == "global" else "platform" if re.match(r"^P\d\d$", tok) else \
        "module" if "/" in tok else "screen"


def for_screens(screens: list[tuple[str, str, str]]) -> dict:
    """The active inputs that apply to a set of screens, each at the broadest level it reaches.

    `screens` is [(screen id, platform code, module)]. Returns
    {"global": [...], "platform": {code: [...]}, "module": {"P02/X": [...]}, "screen": {id: [...]}}
    with each list newest first, and an entry appearing once only."""
    plats = {p for _, p, _ in screens}
    mods = {f"{p}/{m}" for _, p, m in screens if m}
    ids = {s for s, _, _ in screens}
    out = {"global": [], "platform": collections.defaultdict(list),
           "module": collections.defaultdict(list), "screen": collections.defaultdict(list)}
    for e in active():
        toks = [str(t) for t in e.get("scope") or []]
        if "global" in toks:
            out["global"].append(e)
            continue
        hit = [t for t in toks if t in plats]
        if hit:
            for t in hit:
                out["platform"][t].append(e)
            continue
        hit = [t for t in toks if t in mods]
        if hit:
            for t in hit:
                out["module"][t].append(e)
            continue
        for t in toks:
            if t in ids:
                out["screen"][t].append(e)

    def newest(xs):
        return sorted(xs, key=lambda e: (str((e.get("source") or {}).get("date") or ""), e["id"]),
                      reverse=True)
    out["global"] = newest(out["global"])
    for k in ("platform", "module", "screen"):
        out[k] = {key: newest(v) for key, v in out[k].items()}
    return out


def _when(e: dict) -> str:
    d = str((e.get("source") or {}).get("date") or "")
    try:
        x = datetime.date.fromisoformat(d)
        return f"{x.day} {x:%b %Y}"
    except ValueError:
        return d


def source_label(e: dict) -> str:
    """'MoM 3 Aug 2026, 2. POS walkthrough' -- for traceability, never for the screen."""
    src = e.get("source") or {}
    f = str(src.get("file") or "")
    low = f.lower()
    if src.get("label"):
        kind = src["label"]
    elif "vision_book" in low:
        kind = "Design Vision Book"
    elif "decisions register" in low:
        kind = "Decisions Register"
    elif "client-response-rev3" in low:
        kind = "rev 3 design review"
    elif "/designs/" in low or "client-response" in low:
        kind = "design review"
    elif low.startswith("screens/"):
        kind = "screen note"
    elif "mom" in low or "/mom/" in low:
        kind = "MoM"
    else:
        kind = pathlib.Path(f).stem
    sec = str(src.get("section") or "").strip()
    return f"{kind} {_when(e)}" + (f", {sec}" if sec else "")


def line(e: dict) -> str:
    text = " ".join(str(e.get("text") or "").split())
    st = e.get("status")
    head = "**Open question.** " if st == "open-question" else ""
    tag = {"agreed": "agreed", "client-requested": "client request", "open-question": "open"}.get(st, st)
    return f"- {head}{text} *({tag} · {source_label(e)} · {e['id']})*"


INTRO = (
    "**What the client asked for in the meetings and design reviews, for these screens.** Apply "
    "every item. They are the client's own requirements and they are later than the reference "
    "files: where a reference design or a screen's fields disagree with an item here, the item wins. "
    "Newest first; where two items disagree, the newer one wins (anything a later meeting replaced "
    "is already left out). An **Open question** is not settled: build the default it states and "
    "keep it easy to change. The text in brackets is for traceability and, like everything else in "
    "this bundle, never appears on a screen.")


def render_batch(screens: list[tuple[str, str, str, str]], plat_names: dict | None = None,
                 screens_inline: bool = False) -> str:
    """The 'Design inputs from the client meetings' section of a BRIEF.md.

    `screens` is [(screen id, platform code, module, screen name)]. `screens_inline`: the
    screen-specific inputs are already in each screen's block (BUNDLE.md's screen-by-screen
    specification, tools/design_spec.py), so they are counted here rather than repeated."""
    sel = for_screens([(s, p, m) for s, p, m, _ in screens])
    _, plats, _ = screen_index()
    plat_names = plat_names or plats
    name = {s: n for s, _, _, n in screens}
    n = (len(sel["global"]) + sum(map(len, sel["platform"].values()))
         + sum(map(len, sel["module"].values())) + sum(map(len, sel["screen"].values())))
    out = ["## Design inputs from the client meetings", ""]
    if not n:
        out += ["No client meeting has said anything specific to these screens yet. The rules above "
                "and the reference designs stand.", ""]
        return "\n".join(out)
    out += [INTRO, ""]
    if sel["global"]:
        out += ["### Everywhere, on every app", ""] + [line(e) for e in sel["global"]] + [""]
    for p, xs in sorted(sel["platform"].items()):
        out += [f"### Across {p} {plat_names.get(p, '')}".rstrip(), ""] + [line(e) for e in xs] + [""]
    for m, xs in sorted(sel["module"].items()):
        p, mod = m.split("/", 1)
        out += [f"### In {p} · {mod}", ""] + [line(e) for e in xs] + [""]
    if sel["screen"] and screens_inline:
        out += [f"**{sum(map(len, sel['screen'].values()))} more name particular screens** and are in each "
                "screen's block above (*Client meeting inputs*).", ""]
    elif sel["screen"]:
        out += ["### Screen by screen", ""]
        for s in [x for x, _, _, _ in screens if x in sel["screen"]]:
            out += [f"**`{s}` {name.get(s, '')}**".rstrip(), ""] + [line(e) for e in sel["screen"][s]] + [""]
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# the README and the app-guide blocks
# ---------------------------------------------------------------------------------------------

HOW_TO_ADD = """## How to add an input

The index is authored. When a new MoM, workshop output or design review arrives:

1. Open `handoff/design-inputs/mom-design-inputs.yaml` and append one entry per design statement
   (layout, navigation, components, branding, configurability, flow, states, copy, accessibility,
   Arabic/RTL, offline, device size, motion, density, what a screen must show). Skip backend,
   hosting and commercial points that change nothing a user sees.
2. Give it the next free id (`DI-` and a number; never reuse one), its `source` (`file` relative to
   `ticvai/`, `date`, `section`), a short faithful `text`, its `topic`s and the narrowest true
   `scope`: `global`, a platform (`P04`), a module (`P02/Booking & Selection`, spelled as in
   `screens/P*.yaml`) or screen ids (`GST-004`).
3. `status`: `agreed`, `client-requested` (asked for, not yet confirmed) or `open-question` (state
   the question and the default to build).
4. If it changes an earlier input, list the old id under `supersedes`. The old entry stays in the
   index as history and drops out of every bundle.
5. Run `python3 tools/build-design-inputs.py` (it validates every scope against the screens and
   rewrites this README and the app-guide blocks), then `python3 tools/export-design-batch.py
   <BATCH>` for the batches it touches, or let `tools/refresh.sh` do both.
"""


def _counts(inputs: list[dict]) -> dict:
    act = active(inputs)
    lv = collections.Counter()
    for e in act:
        toks = [str(t) for t in e.get("scope") or []]
        lv[min((_level(t) for t in toks), key=["global", "platform", "module", "screen"].index)] += 1
    return {"all": len(inputs), "active": len(act), "superseded": len(inputs) - len(act),
            "status": collections.Counter(e.get("status") for e in act), "level": lv}


def write_readme(inputs: list[dict]) -> None:
    screens, plats, _ = screen_index()
    act = active(inputs)
    gone = superseded_ids(inputs)
    c = _counts(inputs)
    L = ["# Design inputs from the client meetings", "",
         "> **Generated** by `tools/build-design-inputs.py` from `mom-design-inputs.yaml` in this folder. "
         "Edit the index, never this file.", "",
         "Every design-relevant statement the client made in the minutes, the workshops and the design "
         "reviews, with where it was said and what it applies to. **Each batch's `BRIEF.md` and `BUNDLE.md` "
         "carries the ones for its platform, modules and screens** (section *Design inputs from the client "
         "meetings*), and each app guide in `handoff/design-batches/apps/` lists the app-wide ones, so a "
         "Claude Design session is handed them rather than left to guess.", "",
         f"**{c['all']} inputs: {c['active']} in force, {c['superseded']} superseded by a later meeting.** "
         f"In force: {c['status']['agreed']} agreed, {c['status']['client-requested']} requested by the "
         f"client and not yet confirmed, {c['status']['open-question']} open questions. By reach: "
         f"{c['level']['global']} global, {c['level']['platform']} platform-wide, "
         f"{c['level']['module']} module, {c['level']['screen']} screen-specific.", "",
         HOW_TO_ADD, "## Sources", "", "| source | date | inputs |", "|---|---|---:|"]
    by_src = collections.Counter((str(e["source"]["file"]), str(e["source"]["date"])) for e in inputs)
    for (f, d), n in sorted(by_src.items(), key=lambda x: (x[0][1], x[0][0])):
        L.append(f"| `{f}` | {d} | {n} |")
    L.append("")
    opens = [e for e in act if e.get("status") == "open-question"]
    if opens:
        L += ["## Open questions", "", "Built to the stated default until answered.", ""]
        L += [line(e) + f" — scope: {', '.join(map(str, e['scope']))}" for e in opens] + [""]

    def by_date(xs):
        return sorted(xs, key=lambda e: (str(e["source"]["date"]), e["id"]), reverse=True)

    L += ["## Global: every app", ""] + [line(e) for e in by_date(
        [e for e in act if "global" in map(str, e["scope"])])] + [""]
    for p in sorted(plats):
        here = [e for e in act if "global" not in map(str, e["scope"]) and any(
            str(t) == p or str(t).startswith(p + "/") or screens.get(str(t), ("",))[0] == p
            for t in e["scope"])]
        if not here:
            continue
        L += [f"## {p} {plats[p]}", ""]
        wide = [e for e in here if p in map(str, e["scope"])]
        if wide:
            L += ["**Platform-wide**", ""] + [line(e) for e in by_date(wide)] + [""]
        mods = collections.defaultdict(list)
        for e in here:
            if e in wide:
                continue
            for t in map(str, e["scope"]):
                if t.startswith(p + "/"):
                    mods[t].append(e)
        for m in sorted(mods):
            L += [f"**{m.split('/', 1)[1]}**", ""] + [line(e) for e in by_date(mods[m])] + [""]
        per = collections.defaultdict(list)
        for e in here:
            if e in wide or any(str(t).startswith(p + "/") for t in e["scope"]):
                continue
            for t in map(str, e["scope"]):
                if screens.get(t, ("",))[0] == p:
                    per[t].append(e)
        if per:
            L += ["**Screen by screen**", ""]
            for s in sorted(per):
                L += [f"`{s}` {screens[s][2]}", ""] + [line(e) for e in by_date(per[s])] + [""]
    old = [e for e in inputs if e["id"] in gone]
    if old:
        L += ["## Superseded", "", "Kept as history; left out of every bundle.", ""]
        L += [f"{line(e)} — superseded by {gone[e['id']]}" for e in old] + [""]
    README.parent.mkdir(parents=True, exist_ok=True)
    README.write_text("\n".join(L), encoding="utf-8")


BLOCK = re.compile(r"(<!-- design-inputs:(?P<key>[A-Za-z0-9]+) -->\n)(?P<body>.*?)(<!-- /design-inputs:(?P=key) -->)",
                   re.S)


def block_body(key: str, inputs: list[dict]) -> str:
    """The generated text between a guide's markers: `global`, or one platform's wide inputs."""
    screens, plats, _ = screen_index()
    act = active(inputs)
    if key == "global":
        xs = [e for e in act if "global" in map(str, e["scope"])]
        head = (f"*{len(xs)} inputs apply to every app. Generated from "
                "`handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*")
    else:
        xs = [e for e in act if key in map(str, e["scope"])]
        nmod = sum(1 for e in act if key not in map(str, e["scope"]) and "global" not in map(str, e["scope"])
                   and any(str(t).startswith(key + "/") or screens.get(str(t), ("",))[0] == key
                           for t in e["scope"]))
        head = (f"*{len(xs)} inputs apply to all of {key}; {nmod} more apply to particular modules or "
                "screens and are in each batch's BUNDLE.md. Generated from "
                "`handoff/design-inputs/mom-design-inputs.yaml`; edit the index, not this block.*")
    xs = sorted(xs, key=lambda e: (str(e["source"]["date"]), e["id"]), reverse=True)
    return "\n".join([head, ""] + [line(e) for e in xs] + [""]) + "\n"


def write_guides(inputs: list[dict]) -> list[str]:
    done = []
    for f in sorted(APPS.glob("*/*.md")):
        txt = f.read_text(encoding="utf-8")
        if "<!-- design-inputs:" not in txt:
            continue
        new = BLOCK.sub(lambda m: m.group(1) + block_body(m.group("key"), inputs) + m.group(4), txt)
        if new != txt:
            f.write_text(new, encoding="utf-8")
            done.append(str(f.relative_to(ROOT)).replace("\\", "/"))
    return done


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only")
    a = ap.parse_args()
    inputs = load()
    errs = validate(inputs)
    if errs:
        print(f"design inputs: {len(errs)} error(s) in {INDEX.relative_to(ROOT)}")
        for e in errs:
            print(f"  {e}")
        return 1
    c = _counts(inputs)
    if not a.check:
        write_readme(inputs)
        guides = write_guides(inputs)
        print(f"  design inputs: README written; {len(guides)} app guide(s) updated")
    print(f"design inputs: {c['all']} ({c['active']} in force, {c['superseded']} superseded) — "
          f"{c['level']['global']} global, {c['level']['platform']} platform, {c['level']['module']} module, "
          f"{c['level']['screen']} screen; {c['status']['open-question']} open question(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
