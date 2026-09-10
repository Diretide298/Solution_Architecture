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

Reads `wireframes/design-manifest.json`; run `tools/derive-design-manifest.py` first.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "wireframes" / "design-manifest.json"
OUT = ROOT / "handoff" / "design-batches"
# **Inside the package since 10 September.** It had been sitting at the repository root, where the
# root ignore rule (`/*`, with `!/*/` letting the folders back in) kept it out of git entirely --
# so the one artefact every batch is measured against existed on a single machine and in no clone.
PROTOTYPE = "sources/designs/TICVAI_POS_Terminal_client_approved.html"


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def contracts() -> tuple[dict, dict]:
    """operationId -> its full definition, and every schema by name."""
    ops, schemas = {}, {}
    for f in (ROOT / "contracts").rglob("*.yaml"):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for name, sch in ((doc.get("components") or {}).get("schemas") or {}).items():
            schemas.setdefault(name, sch)
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                ops[op["operationId"]] = {
                    "method": method.upper(),
                    "path": path,
                    "contract": f.stem,
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
                }
    return ops, schemas


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
    a = ap.parse_args()

    if not MANIFEST.exists():
        print("no design-manifest.json — run tools/derive-design-manifest.py first")
        return 1
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    batches = {b["id"]: b for b in man["batches"]}

    # Which shipped app each platform belongs to, so `--app` can select on it.
    app_of = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        pl = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("platform") or {}
        app_of[pl.get("code")] = (pl.get("targetApp") or {}).get("app")

    def wanted(b: dict) -> bool:
        if a.platform and b.get("platform") != a.platform:
            return False
        if a.app and app_of.get(b.get("platform")) != a.app:
            return False
        return True

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
    if b["status"] == "locked":
        print(f"{b['id']} is locked: {b.get('lockedReason')}")
        return 1

    ops, schemas = contracts()
    wanted = set(b["screens"])
    screens, used_ops = [], set()
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        for s in doc["screens"]:
            if s["id"] not in wanted:
                continue
            s = dict(s)
            s["_platform"] = {k: v for k, v in doc["platform"].items()
                              if k in ("code", "name", "shortName", "audience", "formFactor",
                                       "app", "operator", "offlineCapable", "targetApp")}
            screens.append(s)
            used_ops |= {x.get("operationId") for x in (s.get("apis") or []) if x.get("operationId")}
            for t in ((s.get("navigation") or {}).get("transitions") or []):
                if t.get("operation"):
                    used_ops.add(t["operation"])

    op_defs = {o: ops[o] for o in sorted(used_ops) if o in ops}
    want_schemas = {v.get("requestBody") for v in op_defs.values()} | \
                   {v.get("responds") for v in op_defs.values()}
    want_schemas.discard(None)
    # one level deeper: whatever those schemas point at
    for name in list(want_schemas):
        blob = json.dumps(schemas.get(name, {}))
        for ref in set(__import__("re").findall(r'"#/components/schemas/([A-Za-z0-9_]+)"', blob)):
            want_schemas.add(ref)
    sch_defs = {n: schemas[n] for n in sorted(want_schemas) if n in schemas}

    d = OUT / b["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "screens.json").write_text(json.dumps(screens, indent=1, ensure_ascii=False),
                                    encoding="utf-8")
    (d / "operations.json").write_text(json.dumps(op_defs, indent=1, ensure_ascii=False),
                                       encoding="utf-8")
    (d / "schemas.json").write_text(json.dumps(sch_defs, indent=1, ensure_ascii=False),
                                    encoding="utf-8")

    perms = sorted({v["permission"] for v in op_defs.values() if v.get("permission")})
    offline = sorted(o for o, v in op_defs.items() if v.get("offlineCapable"))
    plat = screens[0]["_platform"] if screens else {}
    app = (plat.get("targetApp") or {}).get("app", "?")

    brief = f"""# {b['id']} — {b['label']}

**{len(screens)} screens · {len(op_defs)} operations · {len(sch_defs)} schemas · {len(perms)} permissions**

Platform {plat.get('code')} {plat.get('shortName')} · ships as **{app}** ·
{plat.get('audience')} audience · {plat.get('formFactor')} ·
{'offline-capable' if plat.get('offlineCapable') else 'online only'}

## What to build

**A working surface, not a drawing of one.** The reference is `{PROTOTYPE}` — a Claude Design
build from these same sources, and the one the client responded to. Open it and match its depth:
real state, seeded data, controls that do something. Do not describe it, read it.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** {len(perms)} permissions apply here:
  `{', '.join(perms[:12])}`{'…' if len(perms) > 12 else ''}. A control nobody can use must say so,
  not sit enabled and fail.
- **{len(offline)} of these operations work offline**{': ' + ', '.join(offline[:8]) if offline else ''}
  {'— and the rest do not. A surface that looks the same online and off is lying.' if offline else ''}
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
"""
    for s in screens:
        brief += (f"| `{s['id']}` | {s['name']} | {s.get('pattern') or '—'} | "
                  f"{len(s.get('apis') or [])} | {len(s.get('overlays') or [])} | "
                  f"{'yes' if s.get('machine') else '—'} |\n")

    thin = [s["id"] for s in screens
            if sum(len(r.get("components") or [])
                   for r in ((s.get("layout") or {}).get("regions") or [])) < 4]
    if thin:
        brief += (f"\n## Thin screens in this batch\n\n**{', '.join(thin)} declare fewer than four "
                  f"components.** There is not enough here to build them faithfully. Build what is "
                  f"declared and say what is missing — **an invented screen comes back looking "
                  f"finished**, which is worse than an honest gap.\n")

    (d / "BRIEF.md").write_text(brief, encoding="utf-8")

    # **One file, because a design session is handed a thing rather than a folder.** Four files
    # means four chances to arrive with three, and the one most likely to be dropped is
    # `schemas.json` — the one that stops a build inventing its own data. The bundle is the same
    # content in the order it should be read, so there is nothing to assemble at the other end.
    bundle = "\n".join([
        brief.rstrip(),
        "",
        "---",
        "",
        "## `screens.json`",
        "",
        "Every field of every screen in this batch. **`machine` is what a screen is in the middle "
        "of**, `overlays` is what opens over it and what closing it does, and "
        "`navigation.transitions` is how you leave, with `carries` naming the state that travels.",
        "",
        "```json",
        (d / "screens.json").read_text(encoding="utf-8").rstrip(),
        "```",
        "",
        "## `operations.json`",
        "",
        "Method, path, parameters, request and response for every operation these screens call. "
        "**Write fetches against these and do not invent an endpoint** — a screen needing "
        "something absent here is a finding worth reporting, not a gap to fill with a plausible "
        "URL.",
        "",
        "```json",
        (d / "operations.json").read_text(encoding="utf-8").rstrip(),
        "```",
        "",
        "## `schemas.json`",
        "",
        "The data those operations carry, resolved one level deep. **Seed from these.** The "
        "reference prototype hardcodes 57 models and every one corresponds to a schema here; a "
        "build that invents its own will disagree with the backend on day one.",
        "",
        "```json",
        (d / "schemas.json").read_text(encoding="utf-8").rstrip(),
        "```",
        "",
    ])
    (d / "BUNDLE.md").write_text(bundle, encoding="utf-8")

    print(f"  {b['id']} — {b['label']}")
    print(f"  {len(screens)} screens · {len(op_defs)} operations · {len(sch_defs)} schemas · "
          f"{len(perms)} permissions · {len(offline)} offline-capable")
    if thin:
        print(f"  {len(thin)} thin screen(s): {', '.join(thin)}")
    print(f"  -> {d.relative_to(ROOT)}/")
    print(f"     BUNDLE.md ({len(bundle) // 1024} KB) — the single file to hand a design session")
    print("     BRIEF.md, screens.json, operations.json, schemas.json — the same content, apart")
    return 0


if __name__ == "__main__":
    sys.exit(main())
