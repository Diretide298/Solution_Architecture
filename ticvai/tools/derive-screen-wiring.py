#!/usr/bin/env python3
"""Derive the invisible wiring of every screen from its operations: the Block A audit's generator rules (14 October 2026).

**The screens' UI is fixed and approved by the client** (Chinmay, 14 October 2026). This deriver never adds, removes,
moves or relabels a visible component, region title, overlay or screen, and never changes copy a person reads. It
writes only what is invisible and follows from the operations a screen declares: the permission the screen is gated
on, which declared operation a control binds to, an api's `purpose`, internal region ids, and the design notes of the
rendering states where a generator's note promises something the approved screen does not have. A member it cannot
fix without a visible change is left as it is and reported as a keep ("client-approved UI").

The rules, one per audit class (`tools/check-screen-wiring.py`; evidence `audit/ticvai/runs/audit-1014/classes.json`;
change entries CHG-SCR-nnn):

  S-STATE-BOILERPLATE   The pack generator (9 September) wrote "Carries the create action", "The filter narrowed
                        it" and "Names the missing permission" on every screen, whatever it had. They are design
                        notes, not copy. Where the screen has no create operation and no visible create control, or no
                        filter, the note says what the screen has. A visible create control with nothing behind it is
                        the UI's promise and is reported, not rewritten.
  S-SCREEN-PERMISSION   A staff screen whose operations need a permission declares the one its load needs
                        (`generate-screens-from-contracts.py::screen_permission`: the read it loads with first, then
                        any read, then its writes), or the one its no-access state already names. Guest surfaces
                        declare none (ADR-0025, CHG-CLN-007).

**On the refresh, among the screen derivers** (after `derive-components`). Fills and corrects only what a generator
wrote, so a person's note or permission survives; idempotent, a second run writes nothing. Files are written as the
other screen derivers write them (PyYAML `safe_dump`, width 100), in the checkout's line endings: every screen file
round-trips byte for byte, so the diff is the change and nothing else.

    python tools/derive-screen-wiring.py [--only S-STATE-BOILERPLATE,...] [--platform P08] [--apply] [--verbose]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SCREENS = ROOT / "screens"
sys.path.insert(0, str(TOOLS))

_spec = importlib.util.spec_from_file_location("gen_contract_screens", TOOLS / "generate-screens-from-contracts.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
LF, CRLF = chr(10), chr(13) + chr(10)

# The check's own vocabulary (tools/check-screen-wiring.py), so a fix means what the check means.
FILTERS = {"searchField", "selectField", "multiSelect", "datePicker", "toggle"}
CREATE_LIKE = re.compile(r"^(create|add|register|issue|open|start|submit|raise|record|enrol|invite|"
                         r"import|upload|book|reserve|request|schedule|draft|new|clone|copy|"
                         r"generate|publish|assign|allocate|log)", re.I)
WRITES = ("post", "put", "patch", "delete")
GUEST_CODES = ("P01", "P02", "P05")


# ── the package ─────────────────────────────────────────────────────────────────────────────────

def load_ops() -> dict:
    """operationId -> {contract, file, method, path, op}."""
    out = {}
    for f in sorted((ROOT / "contracts").glob("*/*.yaml")):
        text = f.read_text(encoding="utf-8")
        try:
            doc = yaml.load(text, Loader=LOADER) or {}
        except Exception:  # noqa: BLE001
            doc = yaml.safe_load(text) or {}
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for m in ("get", "post", "put", "patch", "delete"):
                op = item.get(m)
                if isinstance(op, dict) and op.get("operationId"):
                    out[op["operationId"]] = {"contract": f.stem, "file": f.relative_to(ROOT).as_posix(),
                                              "method": m, "path": path, "op": op}
    return out


def comps(s: dict):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in (r.get("components") or []):
            if isinstance(c, dict):
                yield r, c


def apis(s: dict) -> list:
    return [a for a in (s.get("apis") or []) if isinstance(a, dict) and a.get("operationId")]


def put_after(s: dict, key: str, value, after: tuple) -> None:
    """Set `key` on the screen, placed after the first of `after` it has (the order people read the record in)."""
    if key in s:
        s[key] = value
        return
    anchor = next((k for k in after if k in s), None)
    items = list(s.items())
    s.clear()
    placed = False
    for k, v in items:
        s[k] = v
        if k == anchor and not placed:
            s[key] = value
            placed = True
    if not placed:
        s[key] = value


# ── S-STATE-BOILERPLATE ─────────────────────────────────────────────────────────────────────────

FIRST_RUN = re.compile(r"^No (?P<noun>.{1,80}?) (?P<cfg>yet|configured yet)\. Carries the create action"
                       r"(; distinct from a filter that matched nothing| and says what the platform does in "
                       r"the meantime)\.$")
NO_RESULTS = re.compile(r"^The filter narrowed it and the (?P<noun>.{1,80}?) are still there\. ")
NO_ACCESS = "Names the missing permission. **Never an empty table**"
NO_ACCESS_NONE = ("No operation on this screen requires a permission, so no permission can be missing: the state is "
                  "reached only by a caller who is not signed in, or a tenant without the screen's module, and says "
                  "which. **Never an empty table** — that reads as *there is no data* and sends somebody to support "
                  "with the wrong question.")
CREATE_BUTTON = re.compile(r"^\s*(\+\s*)?(create|add|new|register|issue|raise|record|submit|book|enrol|invite|"
                           r"upload|import)\b", re.I)


def first_run_note(noun: str, configured: bool, writer: str | None) -> str:
    """The first-run note of a screen that creates nothing (shared with `generate-screens-from-pack.py`)."""
    if configured:
        return (f"No {noun} configured. `{writer}` saves the first one; the state says what the platform does in the "
                f"meantime." if writer else f"No {noun} configured, and this screen declares nothing that saves one.")
    return (f"No {noun} yet. **Offers no create action** — this screen declares no operation that makes one — and "
            f"says so rather than showing an empty table.")


def no_results_note(lister: str | None) -> str:
    """The no-results note of a screen with no filter (shared with `generate-screens-from-pack.py`)."""
    if lister:
        return f"Never shown: this screen offers no filter, so an empty `{lister}` is always the first-run state above."
    return "Never shown: this screen has no list or filter to narrow, so nothing it shows can be filtered to empty."


def fix_states(s: dict, ops: dict, log: list, keeps: list, **_) -> None:
    sid = s["id"]
    states = s.get("states") or {}
    facts = {a["operationId"]: ops.get(a["operationId"]) for a in apis(s)}
    kinds = {c.get("kind") for _, c in comps(s)}
    creates = [o for o, f in facts.items() if f and f["method"] == "post" and CREATE_LIKE.match(o)]
    m = FIRST_RUN.match(str(states.get("emptyFirstRun") or ""))
    if m and not creates:
        visible = [c.get("label") for _, c in comps(s)
                   if "Button" in str(c.get("kind")) and CREATE_BUTTON.match(str(c.get("label") or ""))]
        if visible:
            keeps.append((sid, "S-STATE-BOILERPLATE", f"emptyFirstRun: the approved screen shows {visible[0]!r} and no "
                          f"operation on it creates; the note is the UI's promise (client-approved UI)"))
        else:
            writer = next((o for o, f in facts.items() if f and f["method"] in ("put", "patch", "post")), None)
            states["emptyFirstRun"] = first_run_note(
                m.group("noun"), m.group("cfg") == "configured yet" or s.get("pattern") == "configEditor", writer)
            log.append(f"{sid}: emptyFirstRun names no create action")
    perms = [f["op"].get("x-ticvai-permission") for f in facts.values() if f and f["op"].get("x-ticvai-permission")]
    if str(states.get("emptyNoAccess") or "").startswith(NO_ACCESS) and not perms:
        states["emptyNoAccess"] = NO_ACCESS_NONE
        log.append(f"{sid}: emptyNoAccess names no permission")
    elif states.get("emptyNoAccess") == NO_ACCESS_NONE and perms:
        # Its own note, gone stale: an operation now needs a permission, so the state names it.
        known = [o for o, f in facts.items() if f]
        new = G.no_access_state(ops, known, {a["operationId"] for a in apis(s) if a.get("trigger") == "onLoad"})
        if new:
            states["emptyNoAccess"] = new
            log.append(f"{sid}: emptyNoAccess names the permission its operations now need")
    if NO_RESULTS.match(str(states.get("emptyNoResults") or "")) and not (kinds & FILTERS):
        lister = next((o for o, f in facts.items() if f and f["method"] == "get" and o.startswith(("list", "search"))),
                      None)
        states["emptyNoResults"] = no_results_note(lister)
        log.append(f"{sid}: emptyNoResults names no filter")


# ── S-SCREEN-PERMISSION ─────────────────────────────────────────────────────────────────────────

def fix_permission(s: dict, ops: dict, log: list, keeps: list, platform: dict | None = None, **_) -> None:
    code = str((platform or {}).get("code") or "")
    if s.get("permission") or code.startswith(GUEST_CODES):
        return
    known = [a["operationId"] for a in apis(s) if a["operationId"] in ops]
    perms = {ops[o]["op"].get("x-ticvai-permission") for o in known}
    perms = {p for p in perms if isinstance(p, str) and p}
    if not perms:
        return
    named = [p for p in re.findall(r"`([A-Z][A-Z0-9_]+)`", str((s.get("states") or {}).get("emptyNoAccess") or ""))
             if p in perms]
    loads = {a["operationId"] for a in apis(s) if a.get("trigger") == "onLoad"}
    got = G.screen_permission(ops, known, loads)
    perm = named[0] if named else (got[0] if got else sorted(perms)[0])
    put_after(s, "permission", perm, ("wave", "requiresModule", "module", "name"))
    log.append(f"{s['id']}: permission {perm}")


STEPS = {
    "S-STATE-BOILERPLATE": fix_states,
    "S-SCREEN-PERMISSION": fix_permission,
}


# ── files ───────────────────────────────────────────────────────────────────────────────────────

def dump(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated class ids (default: every rule)")
    ap.add_argument("--platform", help="comma-separated platform codes (default: every platform)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    steps = [x.strip() for x in a.only.split(",")] if a.only else list(STEPS)
    unknown = [x for x in steps if x not in STEPS]
    if unknown:
        print(f"unknown rule(s): {', '.join(unknown)}; known: {', '.join(STEPS)}")
        return 2
    plats = tuple(x.strip() for x in a.platform.split(",")) if a.platform else None

    ops = load_ops()
    files = [f for f in sorted(SCREENS.glob("P*.yaml")) if not plats or f.name.startswith(plats)]
    raws = {f: f.open(encoding="utf-8", newline="").read() for f in files}
    docs = {}
    for f in files:
        d = yaml.load(raws[f], Loader=LOADER)
        if dump(d) != raws[f].replace(CRLF, LF):
            print(f"  {f.name} is not in the derivers' form (safe_dump, width 100); left alone")
            continue
        docs[f] = d

    log: list = []
    keeps: list = []
    changed: set = set()
    for step in steps:
        fn = STEPS[step]
        for f, d in docs.items():
            for s in d.get("screens") or []:
                before = json.dumps(s, sort_keys=False, default=str)
                fn(s, ops, log, keeps, platform=d.get("platform") or {}, docs=docs)
                if json.dumps(s, sort_keys=False, default=str) != before:
                    changed.add(f)
    kinds = Counter(re.sub(r"`[^`]*`|'[^']*'|\b[A-Z][A-Z0-9_]{3,}\b|\d+", "", x.split(": ", 1)[1]).strip() for x in log)
    print(f"derive-screen-wiring: {', '.join(steps)}; {len(log)} change(s) in {len(changed)} file(s)")
    for k, v in kinds.most_common(40):
        print(f"  {v:>5}  {k}")
    for line in (log if a.verbose else log[:15]):
        print("  " + line)
    if keeps:
        print(f"  {len(keeps)} keep(s), left as they are:")
        for sid, rule, why in (keeps if a.verbose else keeps[:40]):
            print(f"    KEEP {rule:<22} {sid:<9} {why}")
    for f in sorted(changed):
        out = dump(docs[f])
        if CRLF in raws[f]:
            out = out.replace(LF, CRLF)      # the checkout's line endings (core.autocrlf)
        if out == raws[f]:
            continue
        if a.apply:
            f.open("w", encoding="utf-8", newline="").write(out)
            print(f"  written  {f.name}")
        else:
            print(f"  would write  {f.name}")
    if not a.apply and changed:
        print("  (dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
