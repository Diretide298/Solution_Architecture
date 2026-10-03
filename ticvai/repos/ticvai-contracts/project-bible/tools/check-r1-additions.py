#!/usr/bin/env python3
"""Hold Chinmay's r1 additions of 3 October 2026 in the package, so they cannot quietly come back.

The decisions are in `docs/active/decisions/answers-3-october-r1-additions.md` (the "r1 additions" section of
the answers log, verbatim); the change log is CHG-RONEC-001 to CHG-RONEC-006 (`changes/entries/CHG-RONEC-*.yaml`).
Each rule fails on the package before its change and passes after it.

  R1-VENUE-IMPORT  (CHG-RONEC-001) `venue-map.importVenueGeometry` accepts DWG, DXF, PDF, SVG, raster, a GLB and a
                   navigation file (`format`), carries `navigationFileRef`, the OCR step (`ocr`) and hand-marked
                   paths (`handMarkedPaths`), and its job reports `ocr`, `handMarkedPaths` and `model`;
                   `ai.proposeWalkways` takes `basis` (`handMarked`) and `venue-map.acceptWalkwayProposals`
                   exists; a label proposal says which scanned text it used (`ocrHint`); `assets.MediaKind` has
                   `model3d`; `VenueMap` carries `modelAssetId`, `modelTransform`, `model3dStatus`;
                   `getVenueNavigationFile` exists; the limits of ADR-0069 are stated (40 MB, 300,000
                   triangles); BO-093 declares the upload, the import, the walkway proposal and its acceptance,
                   and BO-094 the export and the guest map artwork (upload, `setVenueMapArtwork`).
  R1-ADR-0069      (CHG-RONEC-001) ADR-0069 has no open action item (`N. [ ]`) and no `$id` "to be fixed".
  R1-BLIND-CLOSE   (CHG-RONEC-002) **General, every flow.** A step that submits a cashier's count
                   (`submitShiftCount`) says the count is blind; no step or branch shows a cashier or a steward
                   the expected figure; a step that accepts, rejects, closes or reopens a shift
                   (`acceptShiftVariance`, `rejectShiftVariance`, `closeShift`, `reopenShift`) names the
                   supervisor.
  R1-F32           (CHG-RONEC-002) F32 is the decided shift flow: it starts at POS-000 with `login`; the count is
                   submitted on POS-007; the next cashier signs in again on POS-000 and opens on POS-001; a
                   supervisor accepts, rejects or closes on POS-007 and reopens on POS-025; a till held by
                   another session is taken over on POS-000 (`forceLogout`); "Under review" and "never blocks"
                   are said; POS-007's count is "Close and sign out" and lands on POS-000; POS-025 shows the
                   cashier no "takings".
  R1-CONCIERGE     (CHG-RONEC-003) WEB-044, GST-031 and GST-032 read `getGuestConversation` on an interval of 5 s,
                   30 s while hidden (`pollSeconds`, `pollSecondsHidden`). General: an `onInterval` read that
                   names `pollSecondsHidden` names `pollSeconds`, and hidden is never faster than visible.
  R1-RESIDENCY     (CHG-RONEC-004) BO-1065 reads `getRegionSettings` and writes `updateRegionSettings`, with
                   controls bound to `RegionSettings.aiResidencyClass`, `allowedAiResidencies` and
                   `aiResidencyOptIn`.
  R1-PAY-LINK      (CHG-RONEC-005) The screen that manages a payment link after it is made (ADM-593, which
                   resends it and reads its state) declares `cancelPaymentLink` with a control and a form.

    python3 tools/check-r1-additions.py
"""
from __future__ import annotations

import glob
import os
import re
import sys

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def text(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def operations():
    ops = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        for path, item in (doc.get("paths") or {}).items():
            for m, op in (item or {}).items():
                if isinstance(op, dict) and op.get("operationId"):
                    ops[op["operationId"]] = (doc, op, os.path.basename(f)[:-5])
    return ops


def screens():
    out = {}
    for f in glob.glob(os.path.join(ROOT, "screens", "P*.yaml")):
        for s in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("screens") or []:
            if isinstance(s, dict) and s.get("id"):
                out[s["id"]] = s
    return out


def body(op):
    c = ((op.get("requestBody") or {}).get("content") or {}).get("application/json") or {}
    return c.get("schema") or {}


def components(s):
    for r in ((s.get("layout") or {}).get("regions") or []):
        for c in r.get("components") or []:
            yield c


def apis(s):
    return {a.get("operationId"): a for a in (s.get("apis") or [])}


def venue_import(ops, S, err):
    R = "R1-VENUE-IMPORT"
    if "importVenueGeometry" not in ops:
        return err.append((R, "importVenueGeometry is missing"))
    doc, op, _ = ops["importVenueGeometry"]
    props = body(op).get("properties") or {}
    fmts = set(((props.get("format") or {}).get("enum")) or [])
    need = {"dwgPlan", "dxfPlan", "pdfPlan", "svgPlan", "rasterPlan", "glbModel", "navigationFile"}
    if need - fmts:
        err.append((R, f"importVenueGeometry format lacks {sorted(need - fmts)}"))
    for k in ("navigationFileRef", "ocr", "handMarkedPaths"):
        if k not in props:
            err.append((R, f"importVenueGeometry request has no `{k}`"))
    sch = (doc.get("components") or {}).get("schemas") or {}
    job = (sch.get("VenueMapImportJob") or {}).get("properties") or {}
    for k in ("ocr", "handMarkedPaths", "model"):
        if k not in job:
            err.append((R, f"VenueMapImportJob has no `{k}`"))
    vm = (sch.get("VenueMap") or {}).get("properties") or {}
    for k in ("modelAssetId", "modelTransform", "model3dStatus"):
        if k not in vm:
            err.append((R, f"VenueMap has no `{k}`"))
    if "VenueNavigationFile" not in sch:
        err.append((R, "no VenueNavigationFile schema (ADR-0069 section 2)"))
    for o in ("acceptWalkwayProposals", "proposeWalkways", "proposeVenueLabels", "getVenueNavigationFile",
              "setVenueMapArtwork"):
        if o not in ops:
            err.append((R, f"operation {o} is missing"))
    if "proposeWalkways" in ops:
        basis = ((body(ops["proposeWalkways"][1]).get("properties") or {}).get("basis") or {}).get("enum") or []
        if "handMarked" not in basis:
            err.append((R, "proposeWalkways takes no `basis: handMarked` (hand-marked paths)"))
    ai = load("contracts/satellite/ai.yaml")
    lp = ((ai.get("components") or {}).get("schemas") or {}).get("VenueLabelProposal") or {}
    if "ocrHint" not in (lp.get("properties") or {}):
        err.append((R, "VenueLabelProposal has no `ocrHint` (scanned text as a label hint)"))
    assets = load("contracts/satellite/assets.yaml")
    mk = ((assets.get("components") or {}).get("schemas") or {}).get("MediaKind") or {}
    if "model3d" not in (mk.get("enum") or []):
        err.append((R, "assets.MediaKind has no `model3d`"))
    vtxt = text("contracts/satellite/venue-map.yaml")
    for phrase in ("40 MB", "300,000 triangles"):
        if phrase not in vtxt:
            err.append((R, f"venue-map.yaml does not state ADR-0069's limit `{phrase}`"))
    for sid, want in (("BO-093", ("createUpload", "completeUpload", "importVenueGeometry", "proposeWalkways",
                                  "acceptWalkwayProposals")),
                      ("BO-094", ("getVenueNavigationFile", "createUpload", "completeUpload", "setVenueMapArtwork"))):
        a = apis(S.get(sid) or {})
        for o in want:
            if o not in a:
                err.append((R, f"{sid} does not declare {o}"))


def adr_0069(err):
    R = "R1-ADR-0069"
    p = glob.glob(os.path.join(ROOT, "docs", "adr", "0069-*.md"))
    if not p:
        return err.append((R, "ADR-0069 is missing"))
    t = open(p[0], encoding="utf-8").read()
    for m in re.finditer(r"^\d+\. \[ \] (.{0,60})", t, re.M):
        err.append((R, f"ADR-0069 action item still open: {m.group(1)}"))
    if re.search(r"`\$id` to be fixed when the\s", t) and "fixed 3 October 2026" not in t:
        err.append((R, "ADR-0069's navigation-file `$id` is still to be fixed"))


SHOWS_EXPECTED = re.compile(r"\b(cashier|steward)\b[^.]{0,80}\b(sees?|shown|see|reads?)\b[^.]{0,40}\bexpected\b"
                            r"|\bcounted against expected\b", re.I)
NEGATED = re.compile(r"\b(no|never|not|without|nothing)\b", re.I)
SUPERVISOR_ACTS = {"acceptShiftVariance", "rejectShiftVariance", "closeShift", "reopenShift"}


def blind_close(err):
    R = "R1-BLIND-CLOSE"
    for f in sorted(glob.glob(os.path.join(ROOT, "flows", "F*.yaml"))):
        fl = yaml.safe_load(open(f, encoding="utf-8")) or {}
        name = os.path.basename(f)[:4].rstrip("-")
        for st in fl.get("steps") or []:
            ops = set(st.get("operations") or [])
            words = " ".join(str(st.get(k) or "") for k in ("action", "outcome", "note"))
            if "submitShiftCount" in ops and "blind" not in words.lower():
                err.append((R, f"{name} step {st.get('step')}: submits a count and does not say it is blind"))
            if ops & SUPERVISOR_ACTS and not re.search(r"supervisor", words, re.I):
                err.append((R, f"{name} step {st.get('step')}: {sorted(ops & SUPERVISOR_ACTS)} without "
                               f"naming the supervisor (the cashier never accepts their own variance)"))
            for sent in re.split(r"(?<=[.;])\s", words):
                if SHOWS_EXPECTED.search(sent) and not NEGATED.search(sent):
                    err.append((R, f"{name} step {st.get('step')}: shows the cashier the expected figure: "
                                   f"{sent.strip()[:90]}"))
        for br in fl.get("branches") or []:
            words = str(br.get("behaviour") or "")
            for sent in re.split(r"(?<=[.;])\s", words):
                if SHOWS_EXPECTED.search(sent) and not NEGATED.search(sent):
                    err.append((R, f"{name} branch at {br.get('at')}: shows the cashier the expected figure"))


def f32(err):
    R = "R1-F32"
    p = glob.glob(os.path.join(ROOT, "flows", "F32-*.yaml"))
    if not p:
        return err.append((R, "flows/F32 is missing"))
    fl = yaml.safe_load(open(p[0], encoding="utf-8"))
    steps = fl.get("steps") or []
    if not steps or steps[0].get("screen") != "POS-000" or "login" not in (steps[0].get("operations") or []):
        err.append((R, "F32 does not start with the sign-in on POS-000 (login)"))
    if (fl.get("trigger") or {}).get("entryScreen") != "POS-000":
        err.append((R, "F32 trigger.entryScreen is not POS-000"))
    where = {}
    for st in steps:
        for o in st.get("operations") or []:
            where.setdefault(o, set()).add(st.get("screen"))
    want = {"submitShiftCount": "POS-007", "acceptShiftVariance": "POS-007", "rejectShiftVariance": "POS-007",
            "closeShift": "POS-007", "reopenShift": "POS-025"}
    for o, sid in want.items():
        if sid not in where.get(o, set()):
            err.append((R, f"F32 has no step calling {o} on {sid}"))
    logins = [i for i, st in enumerate(steps) if st.get("screen") == "POS-000" and "login" in (st.get("operations") or [])]
    count = [i for i, st in enumerate(steps) if "submitShiftCount" in (st.get("operations") or [])]
    if not (count and any(i > count[0] for i in logins)):
        err.append((R, "F32 does not show the next cashier signing in on POS-000 after the count"))
    if not any(b.get("resolvedBy") == "forceLogout" for b in fl.get("branches") or []):
        err.append((R, "F32 has no branch taking over a held till on POS-000 (forceLogout behind the PIN)"))
    t = text(os.path.relpath(p[0], ROOT))
    for phrase in ("Under review", "never blocks"):
        if phrase not in t:
            err.append((R, f"F32 does not say `{phrase}`"))


def till_screens(S, err):
    """The lead's POS design cross-check of 3 October (CHG-RONEC-002): the cashier's close signs out to the door,
    and no till home shows the cashier takings."""
    R = "R1-F32"
    s7 = S.get("POS-007") or {}
    labels = [c.get("label") for c in components(s7) if c.get("operation") == "submitShiftCount"]
    if "Close and sign out" not in labels:
        err.append((R, "POS-007's submitShiftCount control is not labelled `Close and sign out`"))
    to = [t.get("to") for t in ((s7.get("navigation") or {}).get("transitions") or [])
          if t.get("operation") == "submitShiftCount"]
    if to and set(to) != {"POS-000"}:
        err.append((R, f"POS-007's close lands on {sorted(set(to))}, not the till door POS-000"))
    for c in components(S.get("POS-025") or {}):
        if re.search(r"takings", str(c.get("label") or ""), re.I):
            err.append((R, f"POS-025 shows the cashier `{c.get('label')}` (blind close: `Sales this shift`)"))


def concierge(S, err):
    R = "R1-CONCIERGE"
    for sid in ("WEB-044", "GST-031", "GST-032"):
        a = apis(S.get(sid) or {}).get("getGuestConversation")
        if not a:
            err.append((R, f"{sid} does not declare getGuestConversation"))
            continue
        if a.get("trigger") != "onInterval" or a.get("pollSeconds") != 5 or a.get("pollSecondsHidden") != 30:
            err.append((R, f"{sid} getGuestConversation is not polled every 5 s, 30 s hidden"))
    for sid, s in sorted(S.items()):
        for a in s.get("apis") or []:
            h, v = a.get("pollSecondsHidden"), a.get("pollSeconds")
            if h is not None and (v is None or h < v):
                err.append((R, f"{sid} {a.get('operationId')}: pollSecondsHidden without pollSeconds, or faster"))


def residency(S, err):
    R = "R1-RESIDENCY"
    s = S.get("BO-1065") or {}
    a = apis(s)
    for o in ("getRegionSettings", "updateRegionSettings"):
        if o not in a:
            err.append((R, f"BO-1065 does not declare {o}"))
    bound = {c.get("bindsTo") for c in components(s) if c.get("operation") == "updateRegionSettings"}
    for f in ("RegionSettings.aiResidencyClass", "RegionSettings.allowedAiResidencies",
              "RegionSettings.aiResidencyOptIn"):
        if f not in bound:
            err.append((R, f"BO-1065 has no control bound to {f} that saves with updateRegionSettings"))


def pay_link(S, err):
    R = "R1-PAY-LINK"
    s = S.get("ADM-593") or {}
    if "cancelPaymentLink" not in apis(s):
        err.append((R, "ADM-593 (manages payment links) does not declare cancelPaymentLink"))
    if not any(c.get("operation") == "cancelPaymentLink" for c in components(s)):
        err.append((R, "ADM-593 has no control for cancelPaymentLink"))
    if not any((o.get("confirm") or {}).get("operation") == "cancelPaymentLink" for o in s.get("overlays") or []):
        err.append((R, "ADM-593 has no form collecting the cancel reason"))


def main() -> int:
    ops, S = operations(), screens()
    err: list = []
    venue_import(ops, S, err)
    adr_0069(err)
    blind_close(err)
    f32(err)
    till_screens(S, err)
    concierge(S, err)
    residency(S, err)
    pay_link(S, err)
    rules = ["R1-VENUE-IMPORT", "R1-ADR-0069", "R1-BLIND-CLOSE", "R1-F32", "R1-CONCIERGE", "R1-RESIDENCY",
             "R1-PAY-LINK"]
    for r in rules:
        n = sum(1 for e in err if e[0] == r)
        print(f"  {'ok  ' if not n else 'FAIL'}  {r}" + (f": {n} finding(s)" if n else ""))
    for r, msg in err[:60]:
        print(f"        {r}: {msg}")
    if err:
        print(f"FAIL - {len(err)} finding(s) against Chinmay's r1 additions of 3 October 2026")
        return 1
    print("PASS - the r1 additions of 3 October 2026 hold (venue-map import, ADR-0069, blind close and F32, "
          "concierge polling, BO-1065 residency, payment-link cancel)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
