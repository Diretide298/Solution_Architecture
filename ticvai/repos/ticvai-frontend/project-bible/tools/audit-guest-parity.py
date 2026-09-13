#!/usr/bin/env python3
"""Every difference between guest web and guest app, measured against the rule that they are one.

**Decided 12 September 2026: guest web (P01) and guest app (P02) should be identical.** The
10 September decision made them one product in two shells, and two scripts that day closed the
operation gap — web and app now call 154 and 155 of the same operations. **Operations were never
the whole difference.** A capability can be callable on both shells and still ship in different
waves, need a different licence, open with different parameters, appear in flows on one side only,
or be drawn by a designer on one side and generated on the other.

`screens/_guest-pairs.yaml` says which web screen is which app screen. This reads it and every
layer that describes a guest screen — the screens, flows, frontend manifests, contracts, events,
design bundles and the documents that argued for a difference — and writes:

    handoff/guest-parity-audit.md     for a person
    handoff/guest-parity-audit.json   for a tool

**Reads only.** A difference is not a defect until somebody decides it is; the report says which
ones are sanctioned and why, and ranks the rest.

Run: python3 tools/audit-guest-parity.py
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "screens"
WEB_F = S / "P01-guest-web-storefront.yaml"
APP_F = S / "P02-guest-mobile-app.yaml"
OUT_MD = ROOT / "handoff" / "guest-parity-audit.md"
OUT_JSON = ROOT / "handoff" / "guest-parity-audit.json"

# **What a shell is, and so what may differ.** Everything outside this set is compared.
SANCTIONED_PLATFORM = {
    "code": "the platform id",
    "name": "the platform name",
    "shortName": "the platform name",
    "formFactor": "web and mobileApp are the two shells",
    "runtime": "reactWeb and reactNative are how each shell is built",
    "deployment": "a CDN and an app store ship differently (ADR-0006 tiers distribution, not features)",
    "wireframeBoard": "one board file per platform",
    "wireframeBoardNote": "one board file per platform",
    "offlineCapable": "the app keeps a store across restarts and the web keeps what this visit loaded — "
                      "what the guest reads offline is identical (12 September)",
    "targetApp": "names the sibling, which necessarily differs",
    "designReferences": "compared in the design-sources finding instead",
    "screenCount": "checked against the real count instead",
    "app": "compared in the frontend-manifest finding instead",
    "appStatus": "build status",
}

SEV_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}

# **Statements that argued for a difference, checked for whether they still stand.** A finding here
# disappears when the sentence is rewritten, which is the only way this list stays honest.
STATEMENTS = [
    ("handoff/guest-surface-parity.md", "In-venue only, app by design",
     "stale", "P01 has had WEB-036–046 since 26 August"),
    ("handoff/guest-surface-parity.md", "None of these is a parity gap",
     "stale", "the eight in-venue capabilities are on the web"),
    ("docs/registers/conflicts.md", "stay app-only by design",
     "stale", "CF-93 predates WEB-036–046 and the 10 September decision"),
    ("docs/active/design-plan.md", "guest-app surfaces are not",
     "stale", "P02 is offlineCapable: true"),
    ("contracts/spine/catalogue.yaml", "browses by category and cannot search",
     "stale", "GST-063 Search exists since 17 August"),
    ("docs/active/mom-digest.md", "can differ in functionality",
     "client", "a client minute says web and app may differ — the 12 September rule says they do not; "
               "worth confirming with the client"),
]


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def js(x) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, default=str)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    web_doc, app_doc = load(WEB_F), load(APP_F)
    pairs = load(S / "_guest-pairs.yaml")
    scr = {s["id"]: s for s in web_doc["screens"] + app_doc["screens"]}
    shell = {s["id"]: "web" for s in web_doc["screens"]}
    shell.update({s["id"]: "app" for s in app_doc["screens"]})
    group_of: dict[str, str] = {}
    for g in pairs["groups"]:
        for sid in (g.get("web") or []) + (g.get("app") or []):
            group_of[sid] = g["key"]

    findings: list[dict] = []

    def add(sev, dim, where, detail, fix=""):
        findings.append(dict(severity=sev, dimension=dim, where=where, detail=detail, fix=fix))

    def ops_of(ids) -> set:
        return {a["operationId"] for i in ids if i in scr
                for a in (scr[i].get("apis") or []) if a.get("operationId")}

    web_ids = [i for i in scr if shell[i] == "web"]
    app_ids = [i for i in scr if shell[i] == "app"]
    all_ops = {"web": ops_of(web_ids), "app": ops_of(app_ids)}

    def where_on(op, sh) -> list:
        return sorted(i for i in scr if shell[i] == sh and op in ops_of([i]))

    flows = {}
    for f in sorted((ROOT / "flows").glob("F*.yaml")):
        d = load(f) or {}
        ids = {st.get("screen") for st in (d.get("steps") or []) if isinstance(st, dict)}
        flows[d.get("id") or f.stem] = dict(platforms=set(d.get("platforms") or []),
                                             screens={x for x in ids if x}, name=d.get("name"))

    def drawn(sid) -> bool:
        return (ROOT / "wireframes" / "frames" / f"{sid.lower()}.html").exists()

    # ── platform ────────────────────────────────────────────────────────────────────────────
    pw, pa = web_doc["platform"], app_doc["platform"]
    for k in sorted(set(pw) | set(pa)):
        if k in SANCTIONED_PLATFORM or js(pw.get(k)) == js(pa.get(k)):
            continue
        if k == "packages":
            only_w = sorted(set(pw.get(k) or []) - set(pa.get(k) or []))
            only_a = sorted(set(pa.get(k) or []) - set(pw.get(k) or []))
            if only_w == [] and only_a == ["offline-core"]:
                continue
            add("medium", "platform", "packages", f"web only {only_w}, app only {only_a}")
        elif k == "themes":
            add("medium", "platform", "themes",
                f"web declares {pw.get(k)}, app declares {pa.get(k)} — a guest who uses dark mode on "
                "the app gets light on the web; both boards are drawn light",
                "declare the same themes on both, or record why the web has no dark mode")
        else:
            add("medium", "platform", k, f"web {js(pw.get(k))[:120]} · app {js(pa.get(k))[:120]}")
    for doc, code in ((web_doc, "P01"), (app_doc, "P02")):
        if doc["platform"].get("screenCount") != len(doc["screens"]):
            add("low", "platform", f"{code} screenCount",
                f"declares {doc['platform'].get('screenCount')}, has {len(doc['screens'])}")

    # ── capability groups ───────────────────────────────────────────────────────────────────
    coverage = Counter(g["kind"] for g in pairs["groups"])
    for g in pairs["groups"]:
        key, kind = g["key"], g["kind"]
        W, A = g.get("web") or [], g.get("app") or []

        if kind in ("appOnly", "webOnly", "folded"):
            ids, sh = (W, "web") if W else (A, "app")
            other = "app" if sh == "web" else "web"
            missing = sorted(ops_of(ids) - all_ops[other])
            into = g.get("foldedInto") or []
            label = ", ".join(f"{i} {scr[i]['name']}" for i in ids)
            if kind == "folded":
                elsewhere = sorted(ops_of(ids) - ops_of(into) - set(missing))
                detail = f"{label} has no {other} screen; its operations are on {', '.join(into)}"
                if elsewhere:
                    detail += "; " + ", ".join(f"{o} on {'/'.join(where_on(o, other))}" for o in elsewhere)
                if missing:
                    detail += f"; **not callable on the {other} at all: {', '.join(missing)}**"
                add("high" if missing else "low", "coverage", key, detail,
                    "draw the screen on the other shell, or record the fold as the decision")
            else:
                sev = {"deliberate": "info", "gap": "high", "raise": "medium"}.get(g.get("decision"), "medium")
                detail = f"{label} — {sh} only ({g.get('decision')}). {g.get('note', '')}".strip()
                if missing:
                    detail += f" Not callable on the {other}: {', '.join(missing)}."
                fix = {"gap": f"add the screen to the {other}",
                       "raise": "ask the client whether it ships, then add it to both or remove it",
                       "deliberate": ""}.get(g.get("decision"), "")
                add(sev, "coverage", key, detail, fix)
            continue

        pair = f"{'/'.join(W)} ↔ {'/'.join(A)}"
        where = f"{key} ({pair})"

        if len(W) != len(A):
            add("low", "layout split", where,
                f"{len(W)} screen(s) on the web, {len(A)} on the app: "
                f"{'; '.join(scr[i]['name'] for i in W)} ↔ {'; '.join(scr[i]['name'] for i in A)}",
                "fine if deliberate; a builder should know it is one capability")
        elif {norm(scr[i]["name"]) for i in W} != {norm(scr[i]["name"]) for i in A}:
            add("low", "naming", where,
                f"\"{'; '.join(scr[i]['name'] for i in W)}\" ↔ \"{'; '.join(scr[i]['name'] for i in A)}\"",
                "one name for one journey (31 August rule)")

        ww, wa = min(scr[i]["wave"] for i in W), min(scr[i]["wave"] for i in A)
        if ww != wa:
            add("high", "wave", where, f"ships in wave {ww} on the web and wave {wa} on the app",
                "one wave for both, or record why one shell waits")

        rw = {scr[i].get("requiresModule") for i in W}
        ra = {scr[i].get("requiresModule") for i in A}
        if rw != ra:
            add("high", "licence", where,
                f"web requires {sorted(map(str, rw))}, app requires {sorted(map(str, ra))} — a tenant "
                "licensed for one and not the other sees it on one shell only",
                "one requiresModule for the capability")

        mw, ma = {scr[i].get("module") for i in W}, {scr[i].get("module") for i in A}
        if mw != ma:
            add("low", "section", where, f"web section {sorted(map(str, mw))}, app {sorted(map(str, ma))}")

        cw = {scr[i].get("capability") for i in W} - {None}
        ca = {scr[i].get("capability") for i in A} - {None}
        if cw != ca and (cw or ca):
            add("low", "capability code", where,
                f"web {sorted(cw) or '—'}, app {sorted(ca) or '—'} — traceability counts them as two")

        ow, oa = ops_of(W), ops_of(A)
        for sh, mine, theirs, other in (("web", ow, oa, "app"), ("app", oa, ow, "web")):
            extra = sorted(mine - theirs)
            absent = [o for o in extra if o not in all_ops[other]]
            moved = [o for o in extra if o in all_ops[other]]
            if absent:
                add("high", "operations", where,
                    f"the {sh} calls {', '.join(absent)} and the {other} cannot call it anywhere")
            if moved:
                add("medium", "operations", where,
                    f"the {sh} calls {', '.join(moved)} here; the {other} calls "
                    + "; ".join(f"{o} on {'/'.join(where_on(o, other))}" for o in moved),
                    "same operations on the same capability, so a guest finds it in the same place")

        kw = set().union(*[set((scr[i].get("states") or {})) for i in W])
        ka = set().union(*[set((scr[i].get("states") or {})) for i in A])
        if kw != ka:
            add("medium", "states", where,
                f"web only {sorted(kw - ka) or '—'}, app only {sorted(ka - kw) or '—'}")
        off = {str((scr[i].get("states") or {}).get("offline")) for i in W + A}
        if len(off) > 1:
            add("high", "offline", where, "members carry different offline states",
                "python3 tools/applied/apply-guest-offline-parity.py --apply")
        worded = sorted(k for k in (kw & ka) - {"offline"}
                        if {str(scr[i]["states"].get(k)) for i in W} != {str(scr[i]["states"].get(k)) for i in A})
        if worded:
            add("low", "state wording", where, f"{len(worded)} state(s) worded differently: {', '.join(worded)}",
                "one copy per state — the 12 September offline sync is the model")

        pw_ = {p.get("name") for i in W for p in ((scr[i].get("entryState") or {}).get("params") or [])}
        pa_ = {p.get("name") for i in A for p in ((scr[i].get("entryState") or {}).get("params") or [])}
        if pw_ != pa_:
            add("medium", "entry parameters", where,
                f"web opens with {sorted(map(str, pw_)) or '—'}, app with {sorted(map(str, pa_)) or '—'} — "
                "one shared link cannot open both",
                "one deep-link shape per capability")

        kinds_w = Counter(c.get("kind") for i in W for r in ((scr[i].get("layout") or {}).get("regions") or [])
                          for c in (r.get("components") or []))
        kinds_a = Counter(c.get("kind") for i in A for r in ((scr[i].get("layout") or {}).get("regions") or [])
                          for c in (r.get("components") or []))
        if set(kinds_w) != set(kinds_a):
            # low: components are generated from where operations sit, so this mostly restates
            # the operations finding in layout terms
            add("low", "components", where,
                f"web only {sorted(set(kinds_w) - set(kinds_a)) or '—'}, app only "
                f"{sorted(set(kinds_a) - set(kinds_w)) or '—'} ({sum(kinds_w.values())} vs "
                f"{sum(kinds_a.values())} components)")

        perm_w = {scr[i].get("permission") for i in W} - {None}
        perm_a = {scr[i].get("permission") for i in A} - {None}
        if perm_w != perm_a:
            add("medium", "permission", where, f"web {sorted(perm_w) or '—'}, app {sorted(perm_a) or '—'}")

        for fld in ("overlays", "machine"):
            if any(scr[i].get(fld) for i in W) != any(scr[i].get(fld) for i in A):
                add("medium", fld, where,
                    f"declared on the {'web' if any(scr[i].get(fld) for i in W) else 'app'} only")

        reach_w = {group_of.get(x, x) for i in W for x in ((scr[i].get("navigation") or {}).get("exitTo") or [])} - {key}
        reach_a = {group_of.get(x, x) for i in A for x in ((scr[i].get("navigation") or {}).get("exitTo") or [])} - {key}
        if reach_w != reach_a:
            # low: most of it is the launcher edges each shell's home generates, not a journey
            add("low", "navigation", where,
                f"leads on to {sorted(reach_w - reach_a) or '—'} on the web only and "
                f"{sorted(reach_a - reach_w) or '—'} on the app only")

        for i in W + A:
            for t in ((scr[i].get("navigation") or {}).get("transitions") or []):
                to = t.get("to") or ""
                if to in shell and shell[to] != shell[i]:
                    add("medium", "cross-shell handover", where,
                        f"{i} hands the guest to {to} on the {shell[to]} — \"{t.get('trigger')}\" "
                        f"({t.get('provenance')})",
                        "a twin exists on the same shell; hand over only where the device matters")

        # **Flows and drawn frames are counted once, not once per group.** Reported per group they
        # read as 26 separate gaps; they are one journey written for one shell and one design pass
        # that has reached one shell, and the sections below say so a single time each.
        if any(drawn(i) for i in A) and not any(drawn(i) for i in W):
            add("medium", "design", where, "designer-drawn frame on the app only")

    # ── operations, shell-wide ──────────────────────────────────────────────────────────────
    for sh, other in (("web", "app"), ("app", "web")):
        only = sorted(all_ops[sh] - all_ops[other])
        if only:
            add("info" if only == ["enrolFacePass"] else "high", "operations", f"{sh} only",
                f"{', '.join(only)}" + (" — camera and liveness, deliberate (apply-web-parity.py)"
                                        if only == ["enrolFacePass"] else ""))

    # ── flows ───────────────────────────────────────────────────────────────────────────────
    for fid, fl in sorted(flows.items()):
        touches = {shell[x] for x in fl["screens"] if x in shell}
        named = {"web" if "P01" in fl["platforms"] else None, "app" if "P02" in fl["platforms"] else None} - {None}
        if touches and touches != {"web", "app"}:
            sh = next(iter(touches))
            twins = sorted({group_of[x] for x in fl["screens"] if x in group_of})
            has_twin = any(next(g for g in pairs["groups"] if g["key"] == t).get("web" if sh == "app" else "app")
                           for t in twins)
            if has_twin:
                add("medium", "flows", fid,
                    f"\"{fl['name']}\" walks {sh} screens only, though its capabilities exist on the "
                    f"{'web' if sh == 'app' else 'app'} ({', '.join(twins[:6])})",
                    "name both platforms, or say why the journey is one shell's")
        if touches and named and touches - named:
            add("low", "flows", fid, f"steps on {sorted(touches)} screens, platforms lists {sorted(named)}")

    # ── frontend manifests ──────────────────────────────────────────────────────────────────
    for app_name, doc, prefix in (("guest-web", web_doc, "WEB-"), ("guest-app", app_doc, "GST-")):
        mf = ROOT / "frontend" / f"{app_name}.yaml"
        if not mf.exists():
            continue
        m = load(mf)
        listed = {x["id"]: x for x in (m.get("screens") or [])}
        actual = {s["id"]: s for s in doc["screens"]}
        missing = sorted(set(actual) - set(listed))
        ghosts = sorted(x for x in listed if x.startswith(prefix) and x not in actual)
        renamed = [f"{i} \"{listed[i].get('name')}\"→\"{actual[i]['name']}\"" for i in sorted(listed)
                   if i in actual and listed[i].get("name") != actual[i]["name"]]
        rewaved = [f"{i} {listed[i].get('wave')}→{actual[i]['wave']}" for i in sorted(listed)
                   if i in actual and listed[i].get("wave") != actual[i]["wave"]]
        if missing or ghosts or renamed or rewaved:
            add("high", "frontend manifest", f"frontend/{app_name}.yaml",
                f"lists {len(listed)} screens against {len(actual)}: missing {len(missing)} "
                f"({', '.join(missing[:12])}{'…' if len(missing) > 12 else ''}); ghosts {ghosts or '—'}; "
                f"{len(renamed)} renamed, {len(rewaved)} in another wave",
                "derive-frontend.py carries `screens`, `screenCount` and `byWave` over from the previous "
                "file (`e.setdefault` on every existing key) and never recomputes them — derive them")
        foreign = sorted({x.split('-')[0] for x in listed if not x.startswith(prefix)})
        if foreign:
            add("medium", "frontend manifest", f"frontend/{app_name}.yaml",
                f"also carries {', '.join(foreign)} screens — the kiosk (reactWeb) ships inside the "
                "reactNative guest app while the web, the app's sibling, ships separately",
                "decide whether TICVAI Guest is one codebase or three")

    # ── contracts and events ────────────────────────────────────────────────────────────────
    for f in sorted((ROOT / "contracts").rglob("*.yaml")):
        txt = f.read_text(encoding="utf-8")
        mt = re.search(r"x-ticvai-platforms:\s*(\[[^\]]*\]|(?:\n\s*-\s*[^\n]+)+)", txt)
        if not mt:
            continue
        plats = set(re.findall(r"P\d\d", mt.group(1)))
        if ("P01" in plats) != ("P02" in plats):
            line = txt[:mt.start()].count("\n") + 1
            add("medium", "contracts", f"{f.relative_to(ROOT).as_posix()}:{line}",
                f"x-ticvai-platforms names {'P02' if 'P02' in plats else 'P01'} and not "
                f"{'P01' if 'P02' in plats else 'P02'}", "name both guest shells")
    ev = ROOT / "events"
    if ev.exists():
        for f in sorted(ev.glob("*.yaml")):
            txt = f.read_text(encoding="utf-8")
            if ("guest-app" in txt) != ("guest-web" in txt):
                add("medium", "events", f.relative_to(ROOT).as_posix(),
                    f"consumed by {'guest-app' if 'guest-app' in txt else 'guest-web'} only",
                    "both guest shells render the content this event invalidates")

    # ── design bundles ──────────────────────────────────────────────────────────────────────
    manifest = json.loads((ROOT / "wireframes" / "design-manifest.json").read_text(encoding="utf-8"))
    status = Counter()
    for b in manifest.get("batches") or []:
        if b.get("platform") not in ("P01", "P02"):
            continue
        status[(b["platform"], b.get("status"))] += 1
        sj = ROOT / "handoff" / "design-batches" / b["id"] / "screens.json"
        if not sj.exists():
            add("medium", "design bundles", b["id"], "never cut")
            continue
        cut = {x["id"]: x for x in json.loads(sj.read_text(encoding="utf-8"))}
        stale = [i for i in b["screens"] if i not in cut or i not in scr or any(
            js(cut[i].get(k)) != js(scr[i].get(k)) for k in ("name", "wave", "states", "apis"))]
        if stale:
            add("medium", "design bundles", b["id"],
                f"{len(stale)} of {len(b['screens'])} screens differ from the YAML ({', '.join(stale[:8])})",
                f"python3 tools/export-design-batch.py {b['id']}")
    drawn_w = status[("P01", "drawn")]
    total_w = sum(v for (p, _), v in status.items() if p == "P01")
    drawn_a = status[("P02", "drawn")]
    total_a = sum(v for (p, _), v in status.items() if p == "P02")
    if (drawn_w, total_w) != (drawn_a, total_a):
        add("medium", "design", "Claude Design", f"web {drawn_w}/{total_w} batches drawn, app {drawn_a}/{total_a} "
            "— the web is designed and the app is generated boxes, and the only app reference "
            "(TICVAI_Mobile.dc.html) uses a different design system from the drawn web frames",
            "draw the app batches against the web's house style, or decide which system is the guest's")

    # ── statements that argued for a difference ─────────────────────────────────────────────
    for path, phrase, kind, why in STATEMENTS:
        p = ROOT / path
        if not p.exists():
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if phrase in line:
                add("medium" if kind == "client" else "low", "documents", f"{path}:{n}",
                    f"\"{phrase}\" — {why}",
                    "confirm with the client" if kind == "client" else "rewrite to the 12 September rule")

    # **A difference somebody decided is not a defect.** A group's `sanctioned` map in
    # _guest-pairs.yaml names the dimension and cites the decision; the finding stays in the report,
    # at `info`, carrying its reason — so the decision is visible and not silently absent.
    sanctioned = {g["key"]: (g.get("sanctioned") or {}) for g in pairs["groups"]}
    for x in findings:
        reason = sanctioned.get(x["where"].split(" (")[0], {}).get(x["dimension"])
        if reason:
            x["severity"], x["detail"], x["fix"] = "info", f"{x['detail']} — sanctioned: {reason}", ""

    findings.sort(key=lambda x: (SEV_ORDER[x["severity"]], x["dimension"], x["where"]))
    sev = Counter(x["severity"] for x in findings)
    by_dim = Counter((x["dimension"], x["severity"]) for x in findings)

    OUT_JSON.write_text(json.dumps(dict(
        generatedBy="tools/audit-guest-parity.py", generated=datetime.date.today().isoformat(),
        screens={"P01": len(web_ids), "P02": len(app_ids)}, groups=dict(coverage),
        severity=dict(sev), findings=findings), indent=1, ensure_ascii=False), encoding="utf-8")

    def cell(x) -> str:
        return str(x).replace("|", "\\|").replace("\n", " ")

    md = [
        "# Guest web and guest app — parity audit", "",
        f"**Derived.** `python3 tools/audit-guest-parity.py`, {datetime.date.today().isoformat()}. Reads only.", "",
        "**The rule, decided 12 September 2026: guest web (P01) and guest app (P02) are identical.** "
        "Every difference below either has a reason recorded against it or is a defect waiting for a "
        "decision. Which web screen is which app screen is `screens/_guest-pairs.yaml`.", "",
        f"| | |", "|---|---|",
        f"| Screens | P01 {len(web_ids)} · P02 {len(app_ids)} |",
        f"| Capability groups | {len(pairs['groups'])} — " + " · ".join(f"{k} {v}" for k, v in sorted(coverage.items())) + " |",
        f"| Operations | web {len(all_ops['web'])} · app {len(all_ops['app'])} · shared {len(all_ops['web'] & all_ops['app'])} |",
        f"| Findings | " + " · ".join(f"{k} {sev[k]}" for k in ("high", "medium", "low", "info") if sev[k]) + " |",
        "", "## By dimension", "", "| Dimension | high | medium | low | info |", "|---|---|---|---|---|",
    ]
    for dim in sorted({d for d, _ in by_dim}, key=lambda d: (-by_dim[(d, "high")], -by_dim[(d, "medium")], d)):
        md.append(f"| {dim} | " + " | ".join(str(by_dim[(dim, s)] or "") for s in ("high", "medium", "low", "info")) + " |")

    md += ["", "## What may differ, and why", ""]
    md += [f"- **{k}** — {v}" for k, v in SANCTIONED_PLATFORM.items() if k not in ("name", "shortName", "wireframeBoardNote")]
    md += ["- **density** — compact on the web, comfortable on the app: the input, not the product",
           "- **routes and component paths** — each shell's own codebase", ""]

    for level in ("high", "medium", "low", "info"):
        rows = [x for x in findings if x["severity"] == level]
        if not rows:
            continue
        md += [f"## {level.capitalize()} — {len(rows)}", "", "| Dimension | Where | Difference | Resolve by |", "|---|---|---|---|"]
        md += [f"| {cell(x['dimension'])} | {cell(x['where'])} | {cell(x['detail'])} | {cell(x['fix'])} |" for x in rows]
        md.append("")

    md += ["## Capability groups", "", "| Group | Kind | Web | App |", "|---|---|---|---|"]
    for g in pairs["groups"]:
        md.append(f"| {g['key']} | {g['kind']}{' · ' + g['decision'] if g.get('decision') else ''} | "
                  f"{', '.join(g.get('web') or []) or '—'} | {', '.join(g.get('app') or []) or '—'} |")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"  P01 {len(web_ids)} · P02 {len(app_ids)} screens · {len(pairs['groups'])} groups")
    print("  " + " · ".join(f"{k} {sev[k]}" for k in ("high", "medium", "low", "info") if sev[k]))
    print(f"  → {OUT_MD.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
