#!/usr/bin/env python3
"""Write everything Claude Design needs to build one batch, and nothing it has to guess.

**The target is `TICVAI POS Terminal (1) 1.html`** — a teammate's Claude Design build from these
same sources, and the artefact the client responded to. It is a working application: real state,
seeded data, eleven payment methods, six peripherals, a role→permission matrix, per-venue tax
rules. **A bundle of screen layouts cannot produce that.** It would produce a drawing of it.

So this exports the four things a builder cannot invent:

1. **The screens** — every field, including what each one is in the middle of (`machine`), what
   opens over it (`overlays`), how you leave it (`navigation.transitions`) and what travels with
   you (`carries`).
2. **The operations they call** — the real path, method, parameters and response shape from the
   contracts, so a fetch can be written rather than imagined.
3. **The data behind those operations** — the schemas, resolved one level deep. The prototype
   hardcodes 57 seeded models; every one of them corresponds to a schema this package already
   holds, and a build that invents its own will disagree with the backend on day one.
4. **The permissions** — what each operation requires, so a control can be gated rather than
   drawn as always-enabled.

**What it deliberately withholds is prose about how it should look.** The theme reference is the
prototype itself, named in the brief. Describing it in words would produce a worse copy than
reading it.

    python3 tools/export-design-batch.py --next          # the next pending batch
    python3 tools/export-design-batch.py WS13            # a named one
    python3 tools/export-design-batch.py --list          # what is pending
    python3 tools/export-design-batch.py --all           # every batch folder again (tools/refresh.sh)
    python3 tools/export-design-batch.py P04-shift-01 --force    # a locked batch, by name only

**Since 1 October the bundle leads with a screen-by-screen specification** (`tools/design_spec.py`):
for every screen its inputs and outputs field by field, states, permissions, the requirements-matrix
rows, the client's meeting inputs, the task-tracker rows, the tenant configuration
(`handoff/design-inputs/white-label-map.json`), references, the process owners' design notes
(`handoff/design-notes/`, `--notes DIR` for a trial) and an acceptance checklist. The raw JSON
follows at the end. `--all --coverage FILE` writes what each screen resolved.

Reads `wireframes/design-manifest.json`; run `tools/derive-design-manifest.py` first.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "wireframes" / "design-manifest.json"
OUT = ROOT / "handoff" / "design-batches"
# **Inside the package since 10 September.** It had been sitting at the repository root, where the
# root ignore rule (`/*`, with `!/*/` letting the folders back in) kept it out of git entirely --
# so the one artefact every batch is measured against existed on a single machine and in no clone.
PROTOTYPE = "sources/designs/TICVAI_POS_Terminal_client_approved.html"


def _design_inputs():
    """`tools/build-design-inputs.py`, imported: the client's design inputs from the meetings.

    **The bundles never carried what the client said in the room** (found 1 October): the minutes
    asked for a ride video with no loader, a planner per venue, a typed group size, and none of it
    reached a design session, which builds from this folder and nothing else. The index is authored
    (`handoff/design-inputs/mom-design-inputs.yaml`); this only selects from it, per batch."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("design_inputs", ROOT / "tools" / "build-design-inputs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sane(x):
    """PyYAML reads a `"\\uD83D\\uDD34"` escape as two lone surrogates rather than one emoji, and
    `json.dumps` then refuses to encode them -- so one stray escape in one screen file killed
    `P02-account-self-service-02` and, running unattended, showed up only as a folder that was
    empty in the morning. Recombine the pair; replace what cannot be paired."""
    if isinstance(x, str):
        if any("\ud800" <= c <= "\udfff" for c in x):
            return x.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
        return x
    if isinstance(x, dict):
        return {_sane(k): _sane(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_sane(v) for v in x]
    return x


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def contracts() -> tuple[dict, dict]:
    """operationId -> its full definition, and every schema by name.

    **Read through `tools/design_spec.py`** (1 October), which parses the contracts once per run with
    libyaml: the export had been parsing them, and the screens, two and three times over."""
    raw = _SPEC.PKG.contracts
    ops = {}
    for op_id, o in raw["ops"].items():
        op = o["op"]
        ops[op_id] = {
            "method": o["method"],
            "path": o["path"],
            "contract": o["contract"],
            "summary": op.get("summary"),
            "permission": op.get("x-ticvai-permission"),
            "offlineCapable": op.get("x-ticvai-offline-capable"),
            "conflictPolicy": op.get("x-ticvai-conflict-policy"),
            "scopeLevel": op.get("x-ticvai-scope-level"),
            "parameters": [
                {"name": p.get("name"), "in": p.get("in"), "required": p.get("required")}
                for p in (op.get("parameters") or []) if isinstance(p, dict)],
            "requestBody": _schema_ref(op.get("requestBody")),
            "responds": _schema_ref((op.get("responses") or {}).get("200")
                                    or (op.get("responses") or {}).get("201")),
            # **Every schema the request or response names, however deep.** A paged list
            # is `allOf: [Page, {items: {$ref: X}}]`, and `_schema_ref` stops at `Page` --
            # so `listBookingFlowTypes` shipped without `BookingFlowType`, the one schema
            # that holds the 16-type catalogue (found 30 September). Not written out.
            "_refs": sorted(set(re.findall(
                r"#/components/schemas/([A-Za-z0-9_]+)",
                json.dumps([op.get("requestBody"),
                            (op.get("responses") or {}).get("200"),
                            (op.get("responses") or {}).get("201")], default=str)))),
        }
    return ops, raw["schemas"]


def _schema_ref(node) -> str | None:
    """The schema name a request or response points at, if it names one."""
    if not isinstance(node, dict):
        return None
    for media in (node.get("content") or {}).values():
        sch = (media or {}).get("schema") or {}
        ref = sch.get("$ref") or ((sch.get("items") or {}).get("$ref") if sch.get("items") else None)
        if ref:
            return str(ref).rsplit("/", 1)[-1]
        for k in ("allOf", "oneOf", "anyOf"):
            for part in (sch.get(k) or []):
                if isinstance(part, dict) and part.get("$ref"):
                    return str(part["$ref"]).rsplit("/", 1)[-1]
    return None


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", nargs="?")
    ap.add_argument("--next", action="store_true")
    ap.add_argument("--list", action="store_true")
    # **Finish something before starting something else.** At roughly 18 minutes a batch the whole
    # job is about 49 hours, and taken in id order that means P08 and P09 -- 86 batches, 26 of
    # those hours, and 321 of the 468 thin screens -- land in the middle of everything else. A
    # platform or an app finished is a thing somebody can review; 40% of everything is not.
    ap.add_argument("--platform", metavar="P06", help="only batches on this platform")
    ap.add_argument("--app", metavar="venue-staff-mobile", help="only batches in this shipped app")
    # **Every exported batch again, from today's package** (30 September). A folder is what Claude
    # Design reads and nothing else, so one exported before a contract changed hands the design
    # session yesterday's fields. tools/refresh.sh runs this, so a folder is never older than the
    # package. Only folders that already exist, only batches in the manifest (the hand-written
    # special folders -- B2B-OPTIONS, CMS-FLOW-BUILDER, DEMO-SITE, apps/ -- are not batches), and
    # never a locked one.
    ap.add_argument("--all", action="store_true", help="re-export every batch that already has a folder")
    # **A trial export must not overwrite what a design session is reading** (1 October). The
    # folders under handoff/design-batches are live: Claude Design reads the current briefs. --out
    # writes the same files somewhere else, to look at before a refresh publishes them. With --all,
    # the batches are still the ones that have a folder under handoff/design-batches.
    ap.add_argument("--out", metavar="DIR", help="write the batch folder(s) here instead of handoff/design-batches")
    # **A locked batch can still be exported by name** (1 October), for a look at what its spec now
    # says; --all never touches one, and without --force a named locked batch is refused as before.
    ap.add_argument("--force", action="store_true", help="export a named batch even when it is locked")
    # **The process design notes from somewhere else** (1 October): a trial export against notes
    # that are not committed yet. Default handoff/design-notes/.
    ap.add_argument("--notes", metavar="DIR", help="read the process design notes from DIR")
    # The coverage of the screen-by-screen specification, per screen, for a person to read.
    ap.add_argument("--coverage", metavar="FILE", help="with --all: write per-screen coverage (JSON) here")
    a = ap.parse_args()
    global OUT
    live = OUT
    if a.out:
        OUT = pathlib.Path(a.out).resolve()
    if a.notes:
        _SPEC.set_notes_dir(a.notes)

    if not MANIFEST.exists():
        print("no design-manifest.json — run tools/derive-design-manifest.py first")
        return 1
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    batches = {b["id"]: b for b in man["batches"]}

    # Which shipped app each platform belongs to, so `--app` can select on it.
    app_of = {}
    for doc in _screen_docs():
        pl = doc.get("platform") or {}
        app_of[pl.get("code")] = (pl.get("targetApp") or {}).get("app")

    def wanted(b: dict) -> bool:
        if a.platform and b.get("platform") != a.platform:
            return False
        if a.app and app_of.get(b.get("platform")) != a.app:
            return False
        return True

    if a.all:
        ops, schemas = contracts()
        todo = [x for x in man["batches"]
                if wanted(x) and x["status"] != "locked" and (live / x["id"]).is_dir()]
        for x in todo:
            export(x, ops, schemas, quiet=True)
        print(f"  {len(todo)} batch folder(s) re-exported from the current package")
        _coverage_summary(a.coverage)
        return 0

    if a.list or (not a.batch and not a.next):
        scope = [b for b in man["batches"] if wanted(b)]
        pend = [b for b in scope if b["status"] in ("pending", "partial")]
        where = a.platform or a.app or "the package"
        done = len(scope) - len(pend)
        print(f"{len(pend)} batch(es) pending of {len(scope)} in {where}"
              + (f" — {done} done" if done else ""))
        # **The number that decides how to spend an evening.** 18 minutes a batch is the measured
        # rate; printing it beats everyone re-deriving it from the batch count.
        print(f"  about {len(pend) * 18 / 60:.1f} hours at 18 minutes a batch\n")
        for b in pend[:20]:
            print(f"  {b['id']:<22} {b['label'][:44]:<46} {len(b['screens'])} screens"
                  + (f", {b['thin']} thin" if b["thin"] else ""))
        if len(pend) > 20:
            print(f"  … and {len(pend) - 20} more")
        if not a.platform and not a.app:
            print("\n  --platform P06 or --app venue-staff-mobile finishes one thing at a time.")
        return 0

    if a.next:
        b = next((x for x in man["batches"]
                  if x["status"] in ("pending", "partial") and wanted(x)), None)
        if not b:
            where = a.platform or a.app
            print(f"nothing pending in {where}" if where
                  else "nothing pending — every batch has frames")
            return 0
    else:
        b = batches.get(a.batch)
        if not b:
            print(f"no batch {a.batch!r}. --list shows what there is")
            return 1
    if b["status"] == "locked" and not a.force:
        print(f"{b['id']} is locked: {b.get('lockedReason')} (--force exports it anyway)")
        return 1

    ops, schemas = contracts()
    return export(b, ops, schemas)


_DOCS: list = []
_DI = _design_inputs()


def _design_spec():
    """`tools/design_spec.py`: the screen-by-screen specification (1 October). Imported by path, as
    `build-design-inputs.py` is, because tools/ is not a package."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("design_spec", ROOT / "tools" / "design_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_SPEC = _design_spec()
_STATS: dict = {}


def _coverage_summary(path: str | None) -> None:
    """How much of each screen the specification could resolve from the package: printed every run,
    because a spec that silently resolves half its fields reads as complete."""
    if not _STATS:
        return
    st = list(_STATS.values())
    n = len(st)
    unres = [u for x in st for u in x.get("unresolved", [])]
    why = {}
    for _, _, reason in unres:
        k = "authored label only (no schema field)" if reason.startswith("no schema field") else \
            "bound field not in the contracts" if "not found" in reason else \
            "form calls an operation no contract defines" if "no contract" in reason else reason
        why[k] = why.get(k, 0) + 1
    print(f"  screen-by-screen spec: {n} screens; "
          f"{sum(1 for x in st if x.get('requirements'))} with matrix requirements, "
          f"{sum(1 for x in st if x.get('tracker'))} with tracker rows, "
          f"{sum(1 for x in st if x.get('mom'))} with screen-specific meeting inputs "
          f"({sum(1 for x in st if x.get('mom') or x.get('mom_wider'))} with any), "
          f"{sum(1 for x in st if x.get('notes'))} with process notes, "
          f"{sum(1 for x in st if x.get('whiteLabel') is not None)} white-label")
    tin = sum(x.get("inputs", 0) for x in st)
    tres = sum(x.get("inputs_resolved", 0) for x in st)
    tout = sum(x.get("outputs", 0) for x in st)
    tores = sum(x.get("outputs_resolved", 0) for x in st)
    full = sum(1 for x in st if x.get("inputs", 0) == x.get("inputs_resolved", 0)
               and x.get("outputs", 0) == x.get("outputs_resolved", 0))
    print(f"  inputs {tres}/{tin} resolved from schemas, outputs {tores}/{tout}; "
          f"{full} screens fully resolved; {sum(1 for x in st if x.get('unresolved'))} with something unresolved: "
          + ", ".join(f"{k} {v}" for k, v in sorted(why.items(), key=lambda x: -x[1])))
    if path:
        pathlib.Path(path).write_text(json.dumps(_STATS, indent=1, ensure_ascii=False, default=str), encoding="utf-8")


def _compact(defs: dict) -> str:
    """One entry per line, without the indentation: the files in the folder keep it. The raw data was
    40% whitespace, and the bundle now carries the readable specification before it."""
    return "{\n" + ",\n".join(json.dumps(k, ensure_ascii=False) + ": " +
                              json.dumps(v, ensure_ascii=False, separators=(",", ":"), default=str)
                              for k, v in defs.items()) + "\n}"


def _redraw(b: dict) -> str:
    """**A batch cut out of a locked platform says why** (1 October): the seven P04 screens neither POS
    build draws are drawn in the v2 build's look, and a session reading only this folder must know it."""
    if not b.get("redraw"):
        return ""
    look = (" The look to match is `sources/designs/TICVAI_POS_Terminal_v2.html` (its shift panel: "
            "`wireframes/incoming/P04-pos-v2/img/v2-shift.jpg`), not the approved build below."
            if b.get("platform") == "P04" else "")
    return "## Why this batch is drawn\n\n" + b["redraw"] + look + "\n\n"


def _screen_docs() -> list:
    """The screen files, read once per run: --all exports some 300 batches from the same files."""
    if not _DOCS:
        _DOCS.extend(_SPEC.PKG.screen_docs)
    return _DOCS


def export(b: dict, ops: dict, schemas: dict, quiet: bool = False) -> int:
    """Write one batch folder: screens, operations, schemas, BRIEF.md and BUNDLE.md."""
    wanted = set(b["screens"])
    screens, used_ops = [], set()
    for doc in _screen_docs():
        for s in doc["screens"]:
            if s["id"] not in wanted:
                continue
            s = dict(s)
            s["_platform"] = {k: v for k, v in doc["platform"].items()
                              if k in ("code", "name", "shortName", "audience", "formFactor",
                                       "app", "operator", "offlineCapable", "offlineBanner",
                                       "targetApp")}
            screens.append(s)
            used_ops |= {x.get("operationId") for x in (s.get("apis") or []) if x.get("operationId")}
            for t in ((s.get("navigation") or {}).get("transitions") or []):
                if t.get("operation"):
                    used_ops.add(t["operation"])

    op_defs = {o: {k: v for k, v in ops[o].items() if k != "_refs"} for o in sorted(used_ops) if o in ops}
    deep_refs = {r for o in used_ops if o in ops for r in ops[o].get("_refs", [])}
    want_schemas = {v.get("requestBody") for v in op_defs.values()} | \
                   {v.get("responds") for v in op_defs.values()}
    want_schemas |= deep_refs
    want_schemas.discard(None)
    # one level deeper: whatever those schemas point at
    for name in list(want_schemas):
        blob = json.dumps(schemas.get(name, {}), default=str)
        for ref in set(__import__("re").findall(r'"#/components/schemas/([A-Za-z0-9_]+)"', blob)):
            want_schemas.add(ref)
    sch_defs = {n: schemas[n] for n in sorted(want_schemas) if n in schemas}

    d = OUT / b["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "screens.json").write_text(json.dumps(screens, indent=1, ensure_ascii=False, default=str),
                                    encoding="utf-8")
    (d / "operations.json").write_text(json.dumps(op_defs, indent=1, ensure_ascii=False, default=str),
                                       encoding="utf-8")
    (d / "schemas.json").write_text(json.dumps(sch_defs, indent=1, ensure_ascii=False, default=str),
                                    encoding="utf-8")

    perms = sorted({v["permission"] for v in op_defs.values() if v.get("permission")})
    offline = sorted(o for o, v in op_defs.items() if v.get("offlineCapable"))
    plat = screens[0]["_platform"] if screens else {}
    app = (plat.get("targetApp") or {}).get("app", "?")
    # **The banner is drawn, not described.** Guest web and app carry one `offlineBanner` since
    # 12 September; a bundle that leaves it in `_platform` alone gets built without it.
    ban = plat.get("offlineBanner") or {}
    banner_rule = (f"- **Offline, every screen shows one banner, the same on web and app:** "
                   f"*\"{ban.get('message')}\"* {ban.get('shows', '')} {ban.get('clears', '')} "
                   f"**It never** {ban.get('never', '')} Each screen's `states.offline` says what "
                   f"stays on screen and what waits.\n") if ban.get("message") else ""
    # **An online-only bundle was told "7 of these operations work offline".** True of the
    # operation on a shell that keeps a store, false of this one — and a builder reading it draws
    # an offline mode the web cannot have.
    if plat.get("offlineCapable"):
        offline_rule = (f"- **{len(offline)} of these operations work offline**"
                        f"{': ' + ', '.join(offline[:8]) if offline else ''}\n"
                        f"  {'— and the rest do not. A surface that looks the same online and off is lying.' if offline else ''}\n")
    else:
        offline_rule = ("- **This shell is online only.** None of these operations is served offline here, "
                        "whatever it can do on a shell that keeps a store."
                        + (" Offline, a screen shows what was already loaded, under the banner below.\n"
                           if ban.get("message") else "\n"))

    brief = f"""# {b['id']} — {b['label']}

**{len(screens)} screens · {len(op_defs)} operations · {len(sch_defs)} schemas · {len(perms)} permissions**

Platform {plat.get('code')} {plat.get('shortName')} · ships as **{app}** ·
{plat.get('audience')} audience · {plat.get('formFactor')} ·
{'offline-capable' if plat.get('offlineCapable') else 'online only'}

{_redraw(b)}## Who this is for

**{plat.get('audience')} on {plat.get('formFactor')}.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `{PROTOTYPE}` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** {len(perms)} permissions apply here:
  `{', '.join(perms[:12])}`{'…' if len(perms) > 12 else ''}. A control nobody can use must say so,
  not sit enabled and fail.
{offline_rule}{banner_rule}- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.
"""
    # **The processes these screens belong to** (1 October): each process owner's summary and the
    # words the screens must use, from handoff/design-notes/. Empty until a notes file names a screen.
    proc = _SPEC.render_process_brief([s["id"] for s in screens])
    if proc:
        brief += "\n" + proc

    # **The screen-by-screen specification** (1 October, tools/design_spec.py). Built here, once,
    # so the index in BRIEF.md and the blocks in BUNDLE.md count the same things.
    specs, idx = [], []
    for s in screens:
        raw, plat_full = _SPEC.PKG.screens[s["id"]]
        st: dict = {}
        specs.append(_SPEC.render_screen(raw, plat_full, st))
        _STATS[s["id"]] = st
        idx.append(_SPEC.screen_index_row(raw, plat_full, st))
    brief += ("\n## The screens\n\n"
              "Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; "
              "requirements are matrix rows; meeting inputs are the ones naming the screen (the module and "
              "platform ones are below); white label says whether the tenant's brand reaches it (guest) or "
              "it sets the brand (configures).\n\n"
              "| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |\n"
              "|---|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(idx) + "\n")

    thin = [s["id"] for s in screens
            if sum(len(r.get("components") or [])
                   for r in ((s.get("layout") or {}).get("regions") or [])) < 4]
    if thin:
        brief += (f"\n## Thin screens in this batch\n\n**{', '.join(thin)} declare fewer than four "
                  f"components.** There is not enough here to build them faithfully. Build what is "
                  f"declared and say what is missing — **an invented screen comes back looking "
                  f"finished**, which is worse than an honest gap.\n")
    head = brief

    # **What the client said about these screens, in the brief and so in the bundle** (1 October).
    # Global inputs, the platform's and the modules', then screen by screen; the latest only.
    di_rows = [(s["id"], s["_platform"].get("code"), s.get("module"), s.get("name")) for s in screens]
    brief += "\n" + _DI.render_batch(di_rows).rstrip() + "\n"

    (d / "BRIEF.md").write_text(brief, encoding="utf-8")

    # **One file, because a design session is handed a thing rather than a folder.** Four files
    # means four chances to arrive with three, and the one most likely to be dropped is
    # `schemas.json` — the one that stops a build inventing its own data.
    #
    # **The readable specification first, the raw data last** (1 October). The bundle was three JSON
    # dumps after the brief, and a designer assembled each screen from five places. Now each screen
    # is one block; operations.json and schemas.json follow as the raw data a fetch or a seed is
    # written against. screens.json is not repeated: every field of it is in the blocks, and the
    # file stays in the folder.
    plats = {s["_platform"].get("code") for s in screens}
    bundle = "\n".join([
        head.rstrip(),
        "",
        "---",
        "",
        "## Screen by screen",
        "",
        "**One block per screen, in the order to build them.** Each says what the user enters (every "
        "control, with its rules), what the screen shows and produces (every field, with its format; "
        "every action, with what it returns and the errors to draw), every state, who may do what, the "
        "requirements it meets, what the client said about it, the tracker items, what the tenant "
        "configures, the references, and an acceptance checklist. **Everything in a block is for you, "
        "never for the screen**: no id, field name, operation or permission key may appear as text.",
        "",
        "\n\n---\n\n".join(x.rstrip() for x in specs),
        "",
        "---",
        "",
        _SPEC.batch_tenant_section([_SPEC.PKG.screens[s["id"]] for s in screens]).rstrip(),
        "",
        _SPEC.batch_references(plats).rstrip(),
        "",
        _DI.render_batch(di_rows, screens_inline=True).rstrip(),
        "",
        "---",
        "",
        "## Raw data",
        "",
        "The same package data the blocks above are built from. `screens.json` is in the folder and not "
        "repeated here: every field of it is in the blocks.",
        "",
        "### `operations.json`",
        "",
        "Method, path, parameters, request and response for every operation these screens call. "
        "**Write fetches against these and do not invent an endpoint** — a screen needing "
        "something absent here is a finding worth reporting, not a gap to fill with a plausible "
        "URL.",
        "",
        "```json",
        _compact(op_defs),
        "```",
        "",
        "### `schemas.json`",
        "",
        "The data those operations carry, resolved one level deep. **Seed from these.** The "
        "reference prototype hardcodes 57 models and every one corresponds to a schema here; a "
        "build that invents its own will disagree with the backend on day one.",
        "",
        "```json",
        _compact(sch_defs),
        "```",
        "",
    ])
    (d / "BUNDLE.md").write_text(bundle, encoding="utf-8")

    if quiet:
        return 0
    print(f"  {b['id']} — {b['label']}")
    print(f"  {len(screens)} screens · {len(op_defs)} operations · {len(sch_defs)} schemas · "
          f"{len(perms)} permissions · {len(offline)} offline-capable")
    if thin:
        print(f"  {len(thin)} thin screen(s): {', '.join(thin)}")
    print(f"  -> {d.relative_to(ROOT) if d.is_relative_to(ROOT) else d}/")
    print(f"     BUNDLE.md ({len(bundle) // 1024} KB) — the single file to hand a design session")
    print("     BRIEF.md, screens.json, operations.json, schemas.json — the same content, apart")
    return 0


if __name__ == "__main__":
    sys.exit(main())
