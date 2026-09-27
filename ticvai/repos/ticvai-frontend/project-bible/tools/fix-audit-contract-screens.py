#!/usr/bin/env python3
"""Carry the 27 September audit fixes onto the screens `generate-screens-from-contracts.py` built.

**The generator is not on the refresh** (`refresh.sh` lists it under `_EXCLUDED`, "author screens").
It ran once, on 9 September, and the 493 screens it stamped have been edited since — operations
added to `apis[]`, overlays given `confirm` and `dismiss` from the minutes, transitions labelled.
Fixing the generator therefore changes nothing on disk, and re-running it would be a rebuild, not a
fix. This applies the same rules in place, **touching only what the generator itself wrote**:

  R250  states that are the generator's boilerplate are rewritten from the operations — a create
        action only where a create operation exists, a no-results state only where the list takes
        a filter (the filter components are added beside the table), the permission named from
        `x-ticvai-permission`. A state somebody wrote is never touched.
  R253  generated buttons are labelled for their operation (`Create plan version`, not `Create`
        x3); carried placeholders — `derive-components` proposals for operations already bound,
        `"Components not yet enumerated"` panels, unbound duplicates of bound buttons — are
        dropped; same-named regions are merged, because `derive-wireframes.py` keys regions by
        name and the second `contentBody` replaced the first in every wireframe.
  R256  the selection panel shows the table's entity and both are labelled from the bound schema.
  R264  every generated write button opens a form (`modal`) naming the body fields its operation
        requires, or its existing `confirmDialog` gains them; inline request bodies included.
  R273  every declared operation no component reaches gets one — a table or panel for a read, a
        button for a write or a download; what still cannot be bound keeps its gap and is listed.

Screens are keyed exactly as before: no id, operationId, overlay id or schema name changes. A
`source.sameAs` copy is re-synced from its original, keeping the one state its platform may differ
in, so `check-screens`' copy rule still holds.

Idempotent: a second run reports nothing to do.

Run:  python tools/fix-audit-contract-screens.py            # dry run: what would change
      python tools/fix-audit-contract-screens.py --apply    # write
Then re-run the refresh so wireframes, tickets and docs pick the screens up.
"""
from __future__ import annotations

import argparse
import copy
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCREENS = ROOT / "screens"
sys.path.insert(0, str(HERE))

_spec = importlib.util.spec_from_file_location("gen_contract_screens",
                                               HERE / "generate-screens-from-contracts.py")
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

MARK = "not from a workshop pack"             # the generator's apisNote
GEN = ("contract ",)                            # provenance of what the generator wrote
MINE = ("contract ", "authored — ")
INPUTS = {"textField", "numberField", "selectField", "multiSelect", "datePicker", "toggle",
          "searchField"}
COPIED = ("layout", "states", "gaps", "overlays", "entryState")
COPY_SKIP = {"P06": "offline", "P17": "emptyNoAccess"}


def gen(c: dict) -> bool:
    return str(c.get("provenance", "")).startswith(GEN)


def comps(regions):
    for r in regions:
        for c in r.get("components") or []:
            yield r, c


def fix_screen(s: dict, ops: dict, schemas: dict, log: list) -> None:
    sid = s["id"]
    known = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId") in ops]
    pattern = s.get("pattern") or "listDetail"
    states = s.get("states") or {}
    m = re.search(r"leaves the (.+?) untouched\.", str(states.get("error", "")))
    noun = m.group(1) if m else G.subject(s.get("name", ""))
    layout = s.setdefault("layout", {})
    regions = layout.setdefault("regions", [])
    overlays = s.get("overlays") or []

    def note(msg):
        log.append(f"{sid}: {msg}")

    # 1. R253 — buttons name their operation ----------------------------------------------------
    for _, c in comps(regions):
        op = c.get("operation")
        if not (gen(c) and str(c.get("kind", "")).endswith("Button") and op in ops):
            continue
        if op.startswith(G.READS) and not op.startswith("export"):
            continue
        new = G.button_label(op)
        old = c.get("label")
        if old != new:
            for o in overlays:
                if (gen(o) and o.get("trigger") == old
                        and o.get("id") in ("confirm" + op[0].upper() + op[1:],
                                            "form" + op[0].upper() + op[1:])):
                    o["trigger"] = new
            c["label"] = new
            note(f"button {old!r} -> {new!r}")

    # R264 — every write opens what collects its body -------------------------------------------
    def ensure_overlay(op, label):
        ov = G.action_overlay(ops, schemas, op, label, noun)
        if not ov:
            return
        have = next((o for o in overlays if o.get("id") == ov["id"]), None)
        if have is None:
            overlays.append(ov)
            note(f"overlay {ov['id']} ({ov['component']})")
        elif (gen(have) and have.get("component") == "confirmDialog"
              and "**Collects what" in ov["body"] and "**Collects what" not in str(have.get("body"))
              and str(have.get("body", "")).startswith(f"**Names what `{op}` changes")):
            have["body"] = str(have["body"]).rstrip() + " " + G.fields_sentence(
                op, G.body_fields(ops[op], schemas)[1])
            if ov.get("bindsTo") and not have.get("bindsTo"):
                have["bindsTo"] = ov["bindsTo"]
            note(f"overlay {have['id']} names the fields it collects")

    gaps = s.get("gaps") or []
    # 5. R273 — every declared operation reaches a component. Run before the table is chosen
    # (so a table added here is already there on the first run, as on the second) and again
    # after the forms, for what the panel rebinding released.
    def bind_unreached(skip_shape=None):
        for op in known:
            if op in G.reached_ops(regions, overlays):
                continue
            if skip_shape and op.startswith("get") and G.shape_of(ops, op) == skip_shape:
                continue          # the selection panel takes it in step 2
            if not op.startswith(G.READS):
                bar = next((r for r in regions if r.get("name") == "actionBar"), None)
                if bar is None:
                    bar = {"name": "actionBar", "slot": "rowActions", "components": []}
                    regions.append(bar)
                kind = ("destructiveButton" if G.DESTRUCTIVE.match(op) else "primaryButton"
                        if not any(x.get("kind") == "primaryButton" for x in bar["components"])
                        else "secondaryButton")
                label = G.button_label(op)
                bar["components"].append({"kind": kind, "label": label, "operation": op,
                                          "provenance": G.cite(ops, op)})
                ensure_overlay(op, label)
                note(f"button {label!r} for unreached {op}")
                continue
            bound = G.bind_read(ops, schemas, op, pattern)
            if not bound:
                continue
            name, comp = bound
            region = next((r for r in regions if r.get("name") == name), None)
            if region is None:
                region = {"name": name, "slot": "reads" if name != "actionBar" else "rowActions",
                          "components": []}
                regions.append(region)
            region["components"].append(comp)
            if comp.get("kind") in G.DATA_BEARING and not comp.get("bindsTo"):
                gp = G.inline_response_gap(ops, op)
                if not any(x.get("operation") == op and x.get("source") == gp["source"]
                           for x in gaps):
                    gaps.append(gp)
            note(f"{comp['kind']} for unreached {op}")

    _coll = next((o for o in known if o.startswith(("list", "search"))), None)
    bind_unreached(G.shape_of(ops, _coll) if _coll else None)

    # 2. R256 — the table and the panel show one entity, labelled from it -------------------------
    # **The generator's collection, and only that**: the first list the screen declares, on a
    # pattern that has one. A table this script adds for an unreached list is not the collection,
    # and treating it as one on a second run would move the filters and the panel after it.
    coll_op = next((o for o in known if o.startswith(("list", "search"))), None)
    table = next((c for _, c in comps(regions)
                  if gen(c) and c.get("kind") == "dataTable" and c.get("bindsTo")
                  and c.get("operation") == coll_op), None) \
        if pattern in ("listDetail", "approvalInbox", "commandCentre") else None
    T = table.get("bindsTo") if table else None
    if table and str(table.get("label", "")).startswith("Every "):
        want = f"Every {G.schema_noun(T)}"
        if table["label"] != want:
            note(f"table {table['label']!r} -> {want!r}")
            table["label"] = want
    detail_op = None
    for _, c in comps(regions):
        if not (gen(c) and c.get("kind") == "detailPanel"
                and str(c.get("label", "")).startswith("The selected ")):
            continue
        if table and c.get("bindsTo") != T:
            g = next((o for o in known if o.startswith("get") and G.shape_of(ops, o) == T), None)
            src = g or table["operation"]
            old_schema = c.get("bindsTo")
            note(f"panel {c.get('label')!r} on {old_schema} -> the selected {T} via {src}")
            c.update({"label": f"The selected {G.schema_noun(T)}", "bindsTo": T,
                      "columns": G.columns_for(T, schemas, limit=16), "operation": src,
                      "provenance": G.cite(ops, src)})
            ent = s.get("entryState") or {}
            if old_schema and ent.get("preloaded") == G.columns_for(old_schema, schemas, limit=5):
                ent["preloaded"] = G.columns_for(T, schemas, limit=5)
        else:
            want = (f"The selected {G.schema_noun(c.get('bindsTo'))}" if table
                    else f"The {G.schema_noun(c.get('bindsTo'))}")
            if c.get("label") != want:
                note(f"panel {c.get('label')!r} -> {want!r}")
                c["label"] = want
    if table:
        detail_op = next((o for o in known if o.startswith("get")
                          and G.shape_of(ops, o) == T), None)
    else:
        detail_op = next((c["operation"] for _, c in comps(regions)
                          if gen(c) and c.get("kind") == "detailPanel"
                          and str(c.get("operation", "")).startswith("get")), None)

    # 3. R250 — a filter where the list takes one --------------------------------------------------
    if table:
        for r in regions:
            if table in (r.get("components") or []):
                has = any(x is not table and x.get("operation") == table["operation"]
                          for x in r["components"])
                add = [] if has else G.filter_components(ops, table["operation"])
                if add:
                    i = r["components"].index(table)
                    r["components"][i:i] = add
                    note(f"filters {[a['label'] for a in add]} for {table['operation']}")

    # 4. R264 — the forms
    form_ops = {c.get("operation") for _, c in comps(regions)
                if gen(c) and c.get("kind") in INPUTS and c.get("operation")}
    form_ops |= {op for op in known for _, c in comps(regions)
                 if gen(c) and c.get("kind") in INPUTS and c.get("provenance") == G.cite(ops, op)
                 and not op.startswith(G.READS)}
    for _, c in list(comps(regions)):
        op = c.get("operation")
        if (gen(c) and str(c.get("kind", "")).endswith("Button") and op in ops
                and op in known and not op.startswith(G.READS) and op not in form_ops):
            ensure_overlay(op, c.get("label") or G.button_label(op))

    if pattern == "configEditor":
        for gp in list(gaps):
            op = gp.get("operation")
            if (op in ops and "declares no request body shape" in str(gp.get("why"))
                    and str(gp.get("source", "")).startswith(GEN)):
                fields = G.form_components(ops, schemas, op)
                if fields:
                    regions.append({"name": "contentBody", "slot": "fields", "components": fields})
                    gaps.remove(gp)
                    for o in list(overlays):
                        if o.get("id") == "form" + op[0].upper() + op[1:] and gen(o):
                            overlays.remove(o)
                    note(f"form fields for {op} from its inline body")

    bind_unreached()

    # 6. R253 — carried placeholders go --------------------------------------------------------------
    reached = G.reached_ops(regions, overlays)
    labels = {G.norm(c.get("label", "")) for _, c in comps(regions)
              if str(c.get("kind", "")).endswith("Button") and c.get("operation")}
    labels |= {G.norm(G.words(o)) for o in reached}
    controls = {str(t.get("control", "")).partition("#")[0]
                for t in ((s.get("navigation") or {}).get("transitions") or [])
                if isinstance(t, dict) and t.get("control")}
    rk = G.reaching_kinds(regions, overlays)
    for r in regions:
        keep = []
        for c in r.get("components") or []:
            if not str(c.get("provenance", "")).startswith(MINE):
                body = {k: v for k, v in c.items() if k != "notes" or G.keep_note(v)}
                others = sum(1 for _, x in comps(regions) if x.get("kind") == c.get("kind"))
                if G.is_placeholder(body, reached, labels, rk) and not (
                        c.get("kind") in controls and others == 1):
                    note(f"dropped placeholder {c.get('kind')} {c.get('label') or ''}".rstrip())
                    continue
            keep.append(c)
        r["components"] = keep

    # 7. R253 — one region per name --------------------------------------------------------------
    names = [r.get("name") for r in regions]
    merged = G.merge_regions(regions)
    if len(merged) != len(regions):
        dup = sorted({n for n in names if names.count(n) > 1})
        if dup:
            note(f"merged duplicate regions {dup}")
    layout["regions"] = merged
    regions = merged

    # 8. gaps — the generator's own unreached note, recomputed -----------------------------------
    reached = G.reached_ops(regions, overlays)
    unreached = [o for o in known if o not in reached]
    kept = [g for g in gaps if not (g.get("source") == "the screen's own declarations"
                                    and "reach no component" in str(g.get("why")))]
    if unreached:
        kept.insert(0, {"operation": unreached[0],
                        "why": (f"**{len(unreached)} declared operation"
                                f"{'s' if len(unreached) > 1 else ''} reach no component on this "
                                f"screen**: {', '.join(unreached[:8])}. Either the screen is "
                                f"missing what calls them, or the declaration is residue."),
                        "source": "the screen's own declarations"})
        UNREACHED.append((sid, unreached))
    if kept:
        s["gaps"] = kept
    elif "gaps" in s and not s["gaps"] and s["gaps"] is not None:
        s.pop("gaps")
    elif s.get("gaps"):
        s.pop("gaps")
    if overlays and overlays is not s.get("overlays"):
        s["overlays"] = overlays

    # 9. R250 — the generator's states, read off the operations ----------------------------------
    tabled = table["operation"] if table else None
    new = G.derived_states(pattern, noun, known, ops, tabled, detail_op)
    for k in G.OWNED_STATES:
        v = states.get(k)
        if not (v and G.is_own_state(v)):
            continue
        if k in new and new[k] != v:
            states[k] = new[k]
            note(f"state {k} rewritten")
        elif k not in new:
            # A list that is not the generator's collection still gets the true answer when it
            # cannot be narrowed — `check-screens` asks every list for this state.
            lister = next((c.get("operation") for _, c in comps(regions)
                           if c.get("kind") in ("dataTable", "cardList", "timeline")
                           and str(c.get("operation", "")).startswith(("list", "search"))
                           and c.get("operation") in ops), None)
            if k == "emptyNoResults" and lister and not G.filter_params(ops[lister]):
                states[k] = (f"Never shown: `{lister}` takes no filter, so an empty list is "
                             f"always the first-run state above.")
                note(f"state {k} rewritten")
                continue
            del states[k]
            note(f"state {k} removed — nothing on the screen makes it reachable")


UNREACHED: list = []


def dump_like(raw: str, doc: dict) -> str:
    """Serialise the way this file was last written, so the diff is the change and nothing else."""
    text = raw.replace("\r\n", "\n")
    head = "".join(x for x in text.splitlines(keepends=True) if x.startswith("#"))
    original = yaml.safe_load(text)
    best = None
    for w in (100, 98):
        for h in (head, head + "\n", ""):
            if h + yaml.safe_dump(original, sort_keys=False, allow_unicode=True, width=w) == text:
                best = (h, w)
                break
        if best:
            break
    h, w = best or (head, 100)
    out = h + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=w)
    return out.replace("\n", "\r\n") if "\r\n" in raw else out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="print every change, not a sample")
    args = ap.parse_args()

    ops, schemas = G.load_contracts(ROOT)
    files = sorted(SCREENS.glob("P*.yaml"))
    raws = {f: f.open(encoding="utf-8", newline="").read() for f in files}
    docs = {f: yaml.safe_load(raws[f].replace("\r\n", "\n")) for f in files}
    by_id = {}
    for f, d in docs.items():
        for s in d.get("screens") or []:
            by_id[s["id"]] = (f, d, s)

    mine = {sid for sid, (_, _, s) in by_id.items() if MARK in str(s.get("apisNote", ""))}
    log: list[str] = []
    changed_ids = set()
    for sid in sorted(mine):
        s = by_id[sid][2]
        before = json.dumps(s, sort_keys=True, default=str)
        fix_screen(s, ops, schemas, log)
        if json.dumps(s, sort_keys=True, default=str) != before:
            changed_ids.add(sid)

    # A copy stays a copy (check-screens: `source.sameAs`).
    for sid, (f, d, s) in by_id.items():
        twin = (s.get("source") or {}).get("sameAs")
        if not twin or twin not in changed_ids or twin not in by_id:
            continue
        code = d["platform"]["code"]
        src = by_id[twin][2]
        before = json.dumps(s, sort_keys=True, default=str)
        skip = COPY_SKIP.get(code)
        for k in COPIED:
            if k == "states":
                own = (s.get("states") or {}).get(skip) if skip else None
                st = {x: y for x, y in copy.deepcopy(src.get("states") or {}).items() if x != skip}
                if own is not None:
                    st[skip] = own
                s["states"] = st
            elif k in src:
                s[k] = copy.deepcopy(src[k])
            else:
                s.pop(k, None)
        if json.dumps(s, sort_keys=True, default=str) != before:
            changed_ids.add(sid)
            log.append(f"{sid}: re-synced from {twin} (source.sameAs)")

    kinds = Counter(re.sub(r"['\"].*$|\bfor unreached \w+|\d+", "", x.split(": ", 1)[1]).strip()
                    for x in log)
    print(f"{len(mine)} screens built by generate-screens-from-contracts.py; "
          f"{len(changed_ids)} would change.\n")
    for k, v in kinds.most_common(30):
        print(f"  {v:>5}  {k}")
    print()
    for line in (log if args.verbose else log[:40]):
        print("  " + line)
    if not args.verbose and len(log) > 40:
        print(f"  … {len(log) - 40} more (--verbose)")
    if UNREACHED:
        print(f"\n{len(UNREACHED)} screen(s) still declare operations nothing can bind — the "
              f"response has no shape, so the contract or the declaration has to change:")
        for sid, oids in UNREACHED:
            print(f"  {sid:<10} {', '.join(oids)}")

    touched_files = {by_id[i][0] for i in changed_ids}
    for f in sorted(touched_files):
        out = dump_like(raws[f], docs[f])
        if out == raws[f]:
            continue
        if args.apply:
            f.open("w", encoding="utf-8", newline="").write(out)
            print(f"  written  {f.name}")
        else:
            print(f"  would write  {f.name}")
    if not args.apply:
        print("\n(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
