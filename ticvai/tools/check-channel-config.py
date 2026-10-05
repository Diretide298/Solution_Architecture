#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every guest channel's shell opens on a published configuration the white-label builder publishes.

**5 October 2026, CHG-R4-001** (Chinmay: "kiosk customisation option? ... screen saver video or photo, click to start,
head footer content, size of the card etc."; docs/active/decisions/answers-5-october.md). The guest product ships in
three shells (`targetApp.app: guest`: the web P01, the app P02, the kiosk P05). The web and the app open on a screen
that reads what the tenant published in the builder (`getPublishedTenantConfig`, published by `publishTenantConfig` on
CMS-014). The kiosk's entry, KSK-001 Attract Loop, read only the product list: the package had no kiosk configuration,
"nothing fills the loop" (CHG-R1S-022), and no check noticed that one channel of three could not be customised.

**What fails** (screens/P*.yaml, contracts/):

  CH-ENTRY-READ   no entry screen (`navigation.isEntryPoint`) of a guest shell binds a published configuration read: a
                  white-label `getPublished*` operation whose 200 response is computed from a published version
                  ("computed from the current <Version> snapshot"). A shell may have several entries (the app's Plan
                  tab, GST-051); one reading the published configuration is enough
  CH-NO-PUBLISH   such a read's version schema is returned by no `publish*` operation, so nothing publishes what the shell
                  reads
  CH-NO-BUILDER   the publishing operation is bound on no screen of the white-label builder (P13), so nobody can publish it

Read-only. Exit 1 on any finding.

    python3 tools/check-channel-config.py [--root DIR]     # DIR: another ticvai tree (to run it on an older commit)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
VERSION_OF = re.compile(r"computed from the current (\w+) snapshot")
GUEST_APP = "guest"
BUILDER = "P13"


def load(p: Path):
    return yaml.load(p.read_text(encoding="utf-8"), Loader=LOADER) or {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    root = Path(ap.parse_args().root)

    schemas, ops = {}, {}
    for f in sorted((root / "contracts").glob("*/*.yaml")):
        d = load(f)
        for n, sch in ((d.get("components") or {}).get("schemas") or {}).items():
            schemas.setdefault(n, (f.stem, sch))
        for item in (d.get("paths") or {}).values():
            for verb, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (f.stem, verb, op)

    def refs(node, out):
        if isinstance(node, dict):
            r = node.get("$ref")
            if isinstance(r, str) and "#/components/schemas/" in r:
                out.add(r.rsplit("/", 1)[-1])
            for v in node.values():
                refs(v, out)
        elif isinstance(node, list):
            for v in node:
                refs(v, out)
        return out

    def response_schemas(op, codes=("200", "201")):
        out = set()
        for c in codes:
            refs(((op.get("responses") or {}).get(c) or {}).get("content"), out)
        return out

    def version_read(o):
        """The version schema a published configuration read is computed from, else None."""
        c, verb, op = ops[o]
        if c != "white-label" or verb != "get" or not o.startswith("getPublished"):
            return None
        for n in response_schemas(op, ("200",)):
            m = VERSION_OF.search(str((schemas.get(n, (None, {}))[1] or {}).get("x-ticvai-persistence") or ""))
            if m:
                return m.group(1)
        return None

    screens, bound_on = {}, {}
    for f in sorted((root / "screens").glob("P*.yaml")):
        d = load(f)
        pf = (d.get("platform") or {})
        for s in d.get("screens") or []:
            screens[s["id"]] = (pf, s)
            for a in s.get("apis") or []:
                if isinstance(a, dict) and a.get("operationId"):
                    bound_on.setdefault(a["operationId"], set()).add((pf.get("code"), s["id"]))

    findings = []
    entries = {}
    for sid, (pf, s) in sorted(screens.items()):
        if ((pf.get("targetApp") or {}).get("app")) == GUEST_APP and (s.get("navigation") or {}).get("isEntryPoint"):
            entries.setdefault((pf.get("code"), pf.get("shortName")), []).append(sid)
    shells = len(entries)
    for (code, name), sids in sorted(entries.items()):
        reads = {}
        for sid in sids:
            for a in screens[sid][1].get("apis") or []:
                o = a.get("operationId") if isinstance(a, dict) else None
                if o in ops and version_read(o):
                    reads.setdefault(o, (sid, version_read(o)))
        if not reads:
            findings.append(("CH-ENTRY-READ", f"{code} {name}: no entry screen ({', '.join(sids)}) binds a published "
                             "configuration read, so nothing the builder publishes reaches this channel"))
            continue
        for o, (sid, v) in sorted(reads.items()):
            pubs = sorted(p for p, (c, verb, op) in ops.items() if p.startswith("publish") and v in response_schemas(op))
            if not pubs:
                findings.append(("CH-NO-PUBLISH", f"{sid} reads {o}, computed from {v}, and no publish operation returns {v}"))
                continue
            if not any(code == BUILDER for p in pubs for code, _ in bound_on.get(p, ())):
                findings.append(("CH-NO-BUILDER", f"{sid} reads {o}; {', '.join(pubs)} publish{'es' if len(pubs) == 1 else ''} "
                                 f"it and no {BUILDER} builder screen binds {'it' if len(pubs) == 1 else 'them'}"))
    print(f"check-channel-config: {shells} guest shell(s) checked, "
          f"{sum(len(v) for v in entries.values())} entry screen(s)")
    for rule, msg in findings:
        print(f"  FAIL {rule:<14} {msg}")
    if findings:
        print(f"FAIL - {len(findings)} finding(s)")
        return 1
    print("PASS - every guest shell opens on a published configuration the builder publishes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
