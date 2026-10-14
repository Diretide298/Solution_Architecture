#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A client-approved screen's visible content does not change without a recorded client approval.

**14 October 2026** (the Block A audit, batch GRD, CHG-GRD-002). The lead: "the UI is fixed. approved by client so
dont change that". The client approved the screens' UI (the client prototypes, the design-r1 frames, the
wireframes), and that night eleven audit batches edited screens/ in parallel to fix permissions, bindings, purposes
and reads. Every one was told to leave what a user sees alone; nothing checked that they did, and nothing would check
the next batch. This compares every screen in screens/P*.yaml with the approved snapshot,
`handoff/approved-ui.json`, field by field:

    AU-SCREEN    a screen the snapshot has is gone, or a screen it does not have was added (screen existence)
    AU-FIELD     a visible field differs from the snapshot: the screen's name; its layout (template, pattern,
                 density, the order of its regions by slot); the regions of each slot, compared as a multiset of
                 their visible content and never by their internal `name` (CHG-GRD-004): components and controls
                 (kind, label, tab, the fields of a table's columns, nested components, in order); a state's text (loading,
                 error, empty, no access, offline, banners and every other state); an overlay (its component, its
                 trigger, its confirm and dismiss labels and where they go); the navigation the user sees (each
                 transition's target and trigger, the exits); a step machine's steps
    AU-APPROVAL  an entry in docs/active/approved-ui-changes.yaml with no client approval reference, no `to` hash, or
                 a screen or field that is not in the package or the snapshot

A difference passes only when docs/active/approved-ui-changes.yaml lists it (screen, field, the client approval
reference, and `to`: the hash of the approved content as this check prints it, or `removed`), so an approval
approves that content and not whatever the field says next. Every finding is strict: never baselined.

**Invisible metadata is not compared**: permissions, bindings (`bindsTo`, `operation`, `apis`, their purposes and
triggers, onLoad and poll reads), purposes, entry state and carried ids, wireframe and board links, the component
path and route (`implementation`), gaps, notes, provenance, `derived`/`impliedBy`, open questions, an overlay's
generated `body` and `discards`, waves and modules. A column is compared by its field, not the schema that carries
it, so a schema rename is not a UI change.

    python3 tools/check-approved-ui.py                    # compare screens/ with handoff/approved-ui.json
    python3 tools/check-approved-ui.py --all              # also print every finding's old and new text
    python3 tools/check-approved-ui.py --snapshot <ref>   # write handoff/approved-ui.json from screens/ at <ref>

`--snapshot` is an act, like `--update-baseline`: the approved UI moves only when the client approves a new one, in
a reviewed commit that says which approval. The self-tests run first, every time.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

SNAPSHOT = g.ROOT / "handoff" / "approved-ui.json"
APPROVALS = g.ROOT / "docs" / "active" / "approved-ui-changes.yaml"

RULES = {
    "AU-SCREEN": "a client-approved screen was removed, or a screen was added, with no recorded client approval",
    "AU-FIELD": "a visible field of a client-approved screen changed with no recorded client approval",
    "AU-APPROVAL": "an approved-ui-changes.yaml entry lacks its approval reference or `to`, or names nothing",
}


# ------------------------------------------------------------------------------------------------- visible content
def _component(c: dict, depth: int = 0) -> list:
    """The lines a user sees of one component: kind, label, tab, columns by field, nested components."""
    pad = "  " * depth
    line = f"{pad}{c.get('kind')}"
    if c.get("label") not in (None, ""):
        line += f": {c.get('label')}"
    if c.get("tab") not in (None, ""):
        line += f" [tab {c.get('tab')}]"
    out = [line]
    cols = c.get("columns")
    if isinstance(cols, list) and cols:
        out.append(f"{pad}  columns: " + ", ".join(str(x).rsplit(".", 1)[-1] if isinstance(x, str) else
                                                    json.dumps(x, sort_keys=True, ensure_ascii=False) for x in cols))
    for k, v in c.items():
        if isinstance(v, list) and v and all(isinstance(x, dict) and "kind" in x for x in v):
            out.append(f"{pad}  {k}:")
            for x in v:
                out += _component(x, depth + 2)
    return out


def visible(s: dict) -> dict:
    """field -> text: everything a user sees of one screen. Field names are stable ids (`state:loading`)."""
    out = {"name": str(s.get("name") or "")}
    lay = s.get("layout") or {}
    regions = [r for r in lay.get("regions") or [] if isinstance(r, dict)]
    # **A region is what it shows, not what it is called** (CHG-GRD-004): a region's `name` is an internal id (EMP-005's
    # second `contextPanel` became `partsPanel`, S-DUP-REGION, and nothing on screen moved). Regions are compared by
    # slot, as a multiset of their visible content: field `region:<slot>` holds every region in that slot, sorted, so a
    # rename is no change and two regions sharing a name are both kept. The layout keeps their order by slot.
    out["layout"] = "\n".join([f"template: {lay.get('template')}", f"pattern: {s.get('pattern')}",
                               f"density: {s.get('density')}",
                               "regions: " + ", ".join(str(r.get("slot") or "-") for r in regions)])
    by_slot: dict = {}
    for r in regions:
        lines = []
        for c in r.get("components") or []:
            if isinstance(c, dict):
                lines += _component(c)
        by_slot.setdefault(str(r.get("slot") or "-"), []).append("\n".join(lines) or "(empty)")
    for slot, texts in by_slot.items():
        out[f"region:{slot}"] = "\n--\n".join(sorted(texts))
    for k, v in (s.get("states") or {}).items():
        out[f"state:{k}"] = v if isinstance(v, str) else json.dumps(v, sort_keys=True, ensure_ascii=False)
    for o in s.get("overlays") or []:
        if not isinstance(o, dict):
            continue
        lines = [f"component: {o.get('component')}", f"trigger: {o.get('trigger')}"]
        for side in ("confirm", "dismiss"):
            b = o.get(side)
            # only the label and the target are seen; `operation`, `discards` and `carries` are bindings (CHG-GRD-004:
            # EMP-009's existing Confirm gained `operation: suspendShift` and was reported as `confirm: None`)
            if isinstance(b, dict) and (b.get("label") not in (None, "") or b.get("to")):
                lines.append(f"{side}: {b.get('label')}" + (f" -> {b.get('to')}" if b.get("to") else ""))
        out[f"overlay:{o.get('id')}"] = "\n".join(lines)
    nav = s.get("navigation") or {}
    tr = sorted({f"{t.get('to')} | {t.get('trigger')}" for t in nav.get("transitions") or [] if isinstance(t, dict)})
    ex = sorted({str(x) for x in nav.get("exitTo") or []})
    if tr or ex:
        out["navigation"] = "\n".join([f"to {x}" for x in tr] + ["exits: " + ", ".join(ex)])
    m = s.get("machine")
    if isinstance(m, dict):
        out["machine"] = "\n".join([f"key: {m.get('key')}", f"initial: {m.get('initial')}",
                                    "steps: " + ", ".join(str(k) for k in (m.get("states") or {}))])
    return out


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def snapshot_of(screens: list) -> dict:
    """{screen id: {platform, fields: {field: {hash, text}}}} for [(platform stem, screen)]."""
    out = {}
    for stem, s in screens:
        out[s["id"]] = {"platform": stem, "fields": {f: {"hash": digest(t), "text": t}
                                                     for f, t in sorted(visible(s).items())}}
    return out


# ------------------------------------------------------------------------------------------------- the comparison
def compare(approved: dict, now: dict, approvals: list) -> list:
    """[(rule, key, message)] for the current snapshot `now` against `approved`, less the recorded approvals."""
    out = []
    ok = {}
    for i, a in enumerate(approvals):
        where = f"approved-ui-changes.yaml entry {i + 1}"
        if not isinstance(a, dict):
            out.append(("AU-APPROVAL", f"entry {i + 1}", f"{where} is not a mapping"))
            continue
        sid, field = str(a.get("screen") or ""), str(a.get("field") or "")
        key = f"{sid} {field}"
        if not str(a.get("approval") or "").strip():
            out.append(("AU-APPROVAL", key, f"{where} ({key}) names no client approval reference"))
            continue
        if not str(a.get("to") or "").strip():
            out.append(("AU-APPROVAL", key, f"{where} ({key}) has no `to`: the hash of the approved content, or "
                                            f"`removed`"))
            continue
        if sid not in approved and sid not in now:
            out.append(("AU-APPROVAL", key, f"{where} names screen {sid}, which neither the snapshot nor screens/ has"))
            continue
        if field != "screen" and field not in ((approved.get(sid) or {}).get("fields") or {}) and \
                field not in ((now.get(sid) or {}).get("fields") or {}):
            out.append(("AU-APPROVAL", key, f"{where} names field {field}, which screen {sid} has neither in the "
                                            f"snapshot nor now"))
            continue
        ok[(sid, field)] = str(a.get("to")).strip()

    def approved_to(sid, field, to):
        return ok.get((sid, field)) == to

    for sid in sorted(set(approved) | set(now)):
        a, n = approved.get(sid), now.get(sid)
        if a and not n:
            if not approved_to(sid, "screen", "removed"):
                out.append(("AU-SCREEN", f"{sid} removed",
                            f"{sid} ({a['platform']}, \"{a['fields'].get('name', {}).get('text', '')}\") is in the "
                            f"approved UI and no longer in screens/ (approve with field: screen, to: removed)"))
            continue
        if n and not a:
            h = digest(json.dumps(n["fields"], sort_keys=True, ensure_ascii=False))
            if not approved_to(sid, "screen", h):
                out.append(("AU-SCREEN", f"{sid} added",
                            f"{sid} ({n['platform']}, \"{n['fields'].get('name', {}).get('text', '')}\") is not in "
                            f"the approved UI (approve with field: screen, to: {h})"))
            continue
        af, nf = a["fields"], n["fields"]
        for f in sorted(set(af) | set(nf)):
            old, new = af.get(f), nf.get(f)
            if old and new and old["hash"] == new["hash"]:
                continue
            to = new["hash"] if new else "removed"
            if approved_to(sid, f, to):
                continue
            what = "removed" if not new else ("added" if not old else "changed")
            a_t, n_t = ((x["text"] if x else "").replace("\n", " / ") for x in (old, new))
            i = next((j for j, (p, q) in enumerate(zip(a_t, n_t)) if p != q), min(len(a_t), len(n_t)))
            cut = max(0, i - 40)        # from just before the first difference, so a long field shows what changed
            show = lambda t: ("..." if cut else "") + t[cut:cut + 140] + ("..." if len(t) > cut + 140 else "")  # noqa: E731
            out.append(("AU-FIELD", f"{sid} {f}",
                        f"{sid} {f} {what} (to: {to}): was \"{show(a_t)}\", now \"{show(n_t)}\""))
    return out


def stale_approvals(approved: dict, now: dict, approvals: list) -> list:
    """Approvals whose field no longer differs from the snapshot: a new snapshot has taken them in."""
    out = []
    for a in approvals:
        if not isinstance(a, dict):
            continue
        sid, field = str(a.get("screen") or ""), str(a.get("field") or "")
        if field == "screen":
            if (sid in approved) == (sid in now):
                out.append(f"{sid} {field}")
            continue
        o = ((approved.get(sid) or {}).get("fields") or {}).get(field)
        n = ((now.get(sid) or {}).get("fields") or {}).get(field)
        if o and n and o["hash"] == n["hash"]:
            out.append(f"{sid} {field}")
    return out


# ------------------------------------------------------------------------------------------------- inputs
def screens_at(ref: str) -> list:
    """[(platform stem, screen)] from screens/P*.yaml as committed at `ref`."""
    names = subprocess.run(["git", "ls-tree", "--name-only", ref, "screens/"], cwd=g.ROOT, capture_output=True,
                           text=True, encoding="utf-8", check=True).stdout.split()
    out = []
    for name in sorted(n for n in names if Path(n).name.startswith("P") and n.endswith(".yaml")):
        text = subprocess.run(["git", "show", f"{ref}:./{name}"], cwd=g.ROOT, capture_output=True, text=True,
                              encoding="utf-8", check=True).stdout
        try:
            doc = yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader)) or {}
        except Exception:
            doc = yaml.load(text, Loader=yaml.SafeLoader) or {}
        for s in doc.get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                out.append((Path(name).stem, s))
    return out


def write_snapshot(ref: str) -> int:
    sha = subprocess.run(["git", "rev-parse", ref], cwd=g.ROOT, capture_output=True, text=True,
                         check=True).stdout.strip()
    snap = snapshot_of(screens_at(sha))
    doc = {
        "_about": ("The client-approved UI: per screen, a hash and the text of every visible field (name, layout, "
                   "regions and their components, state text, overlays, navigation, step machines), taken from "
                   "screens/ at `ref` by `python3 tools/check-approved-ui.py --snapshot <ref>`. tools/check-approved-"
                   "ui.py fails on a difference that docs/active/approved-ui-changes.yaml does not approve. An "
                   "authored baseline: re-take it only when the client approves a new UI, in a reviewed commit."),
        "ref": sha,
        "taken": datetime.date.today().isoformat(),
        "screens": snap,
    }
    with SNAPSHOT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("{\n")
        head = [f"{json.dumps(k)}: {json.dumps(doc[k], ensure_ascii=False)}" for k in ("_about", "ref", "taken")]
        fh.write(",\n".join(head) + ',\n"screens": {\n')
        fh.write(",\n".join(f"{json.dumps(sid)}: {json.dumps(snap[sid], ensure_ascii=False, sort_keys=True)}"
                            for sid in sorted(snap)))
        fh.write("\n}\n}\n")
    print(f"approved UI written: {len(snap)} screens, "
          f"{sum(len(v['fields']) for v in snap.values())} visible fields, from {sha[:8]} "
          f"-> {SNAPSHOT.relative_to(g.ROOT).as_posix()}")
    return 0


# ------------------------------------------------------------------------------------------------- self-tests
def self_test() -> list:
    """Each rule against made-up screens it must pass and fail. Returns the failures."""
    fails = []
    base = {"id": "BO-1", "name": "Parking", "pattern": "listDetail", "density": "compact",
            "purpose": "Set up car parks", "permission": "PARKING_CONFIGURE",
            "implementation": {"component": "src/routes/a.tsx", "route": "/parking"},
            "layout": {"template": "split", "regions": [
                {"name": "contentBody", "slot": "collection", "components": [
                    {"kind": "dataTable", "label": "Every car park", "bindsTo": "ParkingFacility",
                     "columns": ["ParkingFacility.name", "ParkingFacility.mode"], "operation": "listParking",
                     "provenance": "contract"}]},
                {"name": "actionBar", "slot": "rowActions", "components": [
                    {"kind": "secondaryButton", "label": "Save", "operation": "setParking", "permission": "X"}]}]},
            "states": {"loading": "The parking list.", "emptyNoAccess": "Names PARKING_CONFIGURE."},
            "apis": [{"operationId": "listParking", "purpose": "Car parks", "trigger": "onLoad"}],
            "overlays": [{"id": "formSet", "component": "modal", "trigger": "Save", "body": "Collects name.",
                          "confirm": {"label": "Save", "operation": "setParking"},
                          "dismiss": {"label": "Cancel", "discards": ["name"]}}],
            "navigation": {"exitTo": ["BO-2"], "transitions": [{"to": "BO-2", "trigger": "Open", "carries": ["id"]}]},
            "entryState": {"params": ["id"]}, "wireframe": {"board": "x.html#bo-1"}, "gaps": []}
    approved = snapshot_of([("P08", base)])

    def with_(**changes):
        s = json.loads(json.dumps(base))
        for path, v in changes.items():
            cur = s
            keys = path.split("__")
            for k in keys[:-1]:
                cur = cur[int(k)] if isinstance(cur, list) else cur[k]
            last = keys[-1]
            if isinstance(cur, list):
                cur[int(last)] = v
            else:
                cur[last] = v
        return s

    # invisible changes pass
    quiet = with_(purpose="Changed purpose", permission="OTHER", implementation={"component": "src/b.tsx"},
                  apis=[], gaps=[{"operation": "x"}], entryState={}, wireframe={"board": "y.html"})
    quiet["layout"]["regions"][0]["components"][0]["operation"] = "listParkingFacilities"
    quiet["layout"]["regions"][0]["components"][0]["bindsTo"] = "ParkingSite"
    quiet["layout"]["regions"][0]["components"][0]["columns"] = ["ParkingSite.name", "ParkingSite.mode"]
    quiet["overlays"][0]["body"] = "Collects name and mode."
    quiet["navigation"]["transitions"][0]["carries"] = ["facilityId"]
    quiet["overlays"][0]["confirm"]["operation"] = "setParkingFacility"
    quiet["overlays"].append({"id": "confirmGone", "component": "confirmDialog", "trigger": "Delete"})
    quiet["layout"]["regions"][1]["name"] = "buttons"                # a region renamed: an internal id
    got = compare(snapshot_of([("P08", with_(overlays=base["overlays"] + [
        {"id": "confirmGone", "component": "confirmDialog", "trigger": "Delete"}]))]),
        snapshot_of([("P08", quiet)]), [])
    if got:
        fails.append(f"an invisible change was reported: {got[:2]}")
    # an existing confirm gaining its operation binding (EMP-009) is not a change
    bound = json.loads(json.dumps(quiet))
    bound["overlays"][1]["confirm"] = {"operation": "deleteParking"}
    got = compare(snapshot_of([("P08", quiet)]), snapshot_of([("P08", bound)]), [])
    if got:
        fails.append(f"a confirm gaining its operation was reported: {got[:2]}")
    # two regions sharing a name are both kept; renaming the second (EMP-005, S-DUP-REGION) is no change
    dup = with_()
    dup["layout"]["regions"].append({"name": "contentBody", "slot": "selection", "components": [
        {"kind": "dataTable", "label": "Parts reserved", "columns": ["Part.itemId"]}]})
    ren = json.loads(json.dumps(dup))
    ren["layout"]["regions"][2]["name"] = "partsPanel"
    if compare(snapshot_of([("P08", dup)]), snapshot_of([("P08", ren)]), []):
        fails.append("a renamed duplicate region was reported")
    gone = json.loads(json.dumps(dup))
    gone["layout"]["regions"][2]["components"] = []
    got = [k for _, k, _ in compare(snapshot_of([("P08", dup)]), snapshot_of([("P08", gone)]), [])]
    if got != ["BO-1 region:selection"]:
        fails.append(f"emptying the second of two same-named regions gave {got}")
    # visible changes fail, each in its field
    cases = {
        "state:loading": with_(states={"loading": "Loading car parks.", "emptyNoAccess": "Names PARKING_CONFIGURE."}),
        "name": with_(name="Car parks"),
        "region:rowActions": with_(**{"layout__regions__1__components": []}),
        "overlay:formSet": with_(**{"overlays__0__confirm": {"label": "Save car park", "operation": "setParking"}}),
        "navigation": with_(navigation={"exitTo": ["BO-3"], "transitions": [{"to": "BO-3", "trigger": "Open"}]}),
        "layout": with_(density="comfortable"),
    }
    for field, s in cases.items():
        got = compare(approved, snapshot_of([("P08", s)]), [])
        keys = [k for _, k, _ in got]
        if keys != [f"BO-1 {field}"]:
            fails.append(f"a visible change to {field} gave {keys}")
    col = with_()
    col["layout"]["regions"][0]["components"][0]["columns"] = ["ParkingFacility.name"]
    if [k for _, k, _ in compare(approved, snapshot_of([("P08", col)]), [])] != ["BO-1 region:collection"]:
        fails.append("a dropped table column was not reported")
    # an approval with its reference and hash passes; one without either, or for other content, does not
    changed = snapshot_of([("P08", cases["name"])])
    h = changed["BO-1"]["fields"]["name"]["hash"]
    if compare(approved, changed, [{"screen": "BO-1", "field": "name", "approval": "Client sign-off 20 Oct", "to": h}]):
        fails.append("an approved change was still reported")
    got = compare(approved, changed, [{"screen": "BO-1", "field": "name", "approval": "", "to": h}])
    if sorted(r for r, _, _ in got) != ["AU-APPROVAL", "AU-FIELD"]:
        fails.append(f"an approval with no reference passed: {got}")
    got = compare(approved, changed, [{"screen": "BO-1", "field": "name", "approval": "Sign-off", "to": "0" * 16}])
    if [r for r, _, _ in got] != ["AU-FIELD"]:
        fails.append("an approval of other content passed this content")
    # screens added and removed
    got = compare(approved, {}, [])
    if [k for _, k, _ in got] != ["BO-1 removed"]:
        fails.append(f"a removed screen gave {got}")
    if compare(approved, {}, [{"screen": "BO-1", "field": "screen", "approval": "Sign-off", "to": "removed"}]):
        fails.append("an approved removal was still reported")
    two = snapshot_of([("P08", base), ("P08", with_(id="BO-9"))])
    got = compare(approved, two, [])
    if [k for _, k, _ in got] != ["BO-9 added"]:
        fails.append(f"an added screen gave {got}")
    if stale_approvals(approved, approved, [{"screen": "BO-1", "field": "name"}]) != ["BO-1 name"]:
        fails.append("an approval the snapshot already holds was not noted")
    return fails


def main() -> int:
    g.force_utf8()
    args = sys.argv[1:]
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    if "--snapshot" in args:
        i = args.index("--snapshot")
        if i + 1 >= len(args):
            print("check-approved-ui: --snapshot needs a git ref (the commit whose screens the client approved)")
            return 2
        return write_snapshot(args[i + 1])
    guard = g.Guard("check-approved-ui", RULES)
    snap = g.load_json(SNAPSHOT, None)
    if not snap or not snap.get("screens"):
        print(f"FAIL - {SNAPSHOT.relative_to(g.ROOT).as_posix()} is missing: take it with --snapshot <ref>")
        return 1
    approvals = []
    if APPROVALS.exists():
        approvals = (yaml.safe_load(APPROVALS.read_text(encoding="utf-8")) or {}).get("changes") or []
    now = snapshot_of(g.screens())
    found = compare(snap["screens"], now, approvals)
    for rule, key, msg in found:
        guard.add(rule, key, msg, strict=True)
    if guard.show_all:
        for rule, key, _ in found:
            if rule != "AU-FIELD":
                continue
            sid, field = key.split(" ", 1)
            old = ((snap["screens"].get(sid) or {}).get("fields") or {}).get(field)
            new = ((now.get(sid) or {}).get("fields") or {}).get(field)
            guard.note(f"{key}\n    approved: {(old or {}).get('text', '(none)')}\n    now:      "
                       f"{(new or {}).get('text', '(none)')}")
    guard.note(f"{len(now)} screens against the approved UI of {str(snap.get('ref'))[:8]} ({len(snap['screens'])} "
               f"screens, {sum(len(v['fields']) for v in snap['screens'].values())} visible fields); "
               f"{len(approvals)} recorded approval(s); the self-tests pass")
    stale = stale_approvals(snap["screens"], now, approvals)
    if stale:
        guard.note(f"{len(stale)} approval(s) the snapshot already holds (re-taken since): {', '.join(stale[:8])}")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
