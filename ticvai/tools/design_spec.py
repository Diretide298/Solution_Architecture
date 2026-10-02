#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The screen-by-screen specification every Claude Design batch carries. Imported, no main.

**Chinmay, 1 October: "Make them as detailed as possible for each screen. Reference all the
material, mom, matrix assisted task. How input should be how output. Especially the website white
label and so on."** Until then a batch's BUNDLE.md was three raw JSON dumps and the meeting inputs:
everything a designer needed was in there, and a designer had to assemble each screen from five
places to find it -- the screen's components, the operation a button calls, the request schema
behind that operation, the enum that schema names, the meeting where the client asked for it.

This assembles it, per screen, from the package and nothing else:

     1  header        id, app, module, block (tasks.csv), who, purpose, device, offline, entry;
                      from the process notes: the summary, the corrections by status (pending,
                      contract gap logged, fixed) and the decisions taken on the screen
     2  inputs        every control: label, type, required, default, limits, allowed values with
                      labels, conditions, mask, helper text, errors -- from the request schemas
                      in contracts/ and the screen's own components; where each comes from
     3  outputs       every displayed field with its format; every action: what it calls, sends,
                      returns, raises and emits; every transition with what it carries
     4  states        every declared state with its copy, plus offline and validation
     5  permissions   per operation, with the tier (roles-by-app.yaml) and what a refused user sees
     6  requirements  matrix rows traced to the screen's operations and data (traceability.json),
                      with the requirement text from the matrix workbook
     7  meetings      the client's design inputs scoped to this screen (build-design-inputs.py)
     8  tracker       workshop tracker rows about this screen (task-tracker-index.json)
     9  white label   what the tenant configures here, or what this CMS screen configures
                      (white-label-map.json, tools/build-white-label-map.py)
    10  references    wireframe frame and provenance, prototype view, flows and steps, ADRs
    11  acceptance    a checklist derived from all of the above

**Nothing here is authored per screen.** Three small tables are authored in this file, each
marked: how a control is drawn from a schema type, how a value is formatted, and which tracker
keywords reach which screens. Everything else is read.

Used by `tools/export-design-batch.py`.
"""
from __future__ import annotations

import collections
import csv
import importlib.util
import json
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
H = ROOT / "handoff"
DI_DIR = H / "design-inputs"
TRACKER_INDEX = DI_DIR / "task-tracker-index.json"
WL_MAP = DI_DIR / "white-label-map.json"
TRACE = H / "traceability.json"
MATRIX = ROOT / "sources" / "requirements" / "Ticvai_matrix_20260621_2.xlsx"
TASKS = H / "service-docs" / "tasks.csv"
PLAN_TASKS = H / "service-docs" / "plan-tasks.csv"
PMS = H / "service-docs" / "pms-map.json"
ROLES_BY_APP = ROOT / "roles-by-app.yaml"
APPS = H / "design-batches" / "apps"
ADR_DIR = ROOT / "docs" / "adr"
FLOWS = ROOT / "flows"
WHITE_LABEL_DOC = "handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md"

GUEST_PLATFORMS = ("P01", "P02", "P05")
INPUT_KINDS = {"selectField", "textField", "toggle", "numberField", "datePicker", "multiSelect",
               "searchField", "fileUpload", "consentBlock", "scanTarget", "seatMap"}
ACTION_KINDS = {"primaryButton", "secondaryButton", "destructiveButton", "iconButton", "publishGate",
                "confirmDialog"}
# Request parameters a person never types: transport, paging and concurrency.
PLUMBING_PARAMS = {"Idempotency-Key", "If-Match", "Prefer", "X-Consistency-Token", "X-Admission-Token",
                   "pageSize", "cursor", "pageCursor", "X-Request-Id"}
PLUMBING_FIELDS = {"tenantId", "scopePath", "contentHash", "createdByPrincipalId", "updatedByPrincipalId",
                   "createdAt", "updatedAt", "version", "etag", "isDraft"}
MAX_FIELDS = 45          # per request schema; the rest are named and left to schemas.json
MAX_DEPTH = 2            # nested objects expanded this deep
MAX_REQS = 12            # requirement rows shown per screen
MAX_TRACKER = 6          # keyword-matched tracker rows per screen


# ---------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------

_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def load_yaml(text: str):
    """libyaml when it is installed: the screens and contracts are 40 MB of YAML, and the pure-Python
    loader spent a minute on them for every export."""
    return yaml.load(text, Loader=_LOADER)


def _sane(x):
    if isinstance(x, str):
        if any("\ud800" <= c <= "\udfff" for c in x):
            return x.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
        return x
    if isinstance(x, dict):
        return {_sane(k): _sane(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_sane(v) for v in x]
    return x


def _flat(s, limit: int | None = None) -> str:
    """One line, markdown emphasis kept, table-safe."""
    t = " ".join(str(s or "").split()).replace("|", "/")
    if limit and len(t) > limit:
        cut = t[:limit].rsplit(" ", 1)[0]
        t = cut.rstrip(",;:") + " …"
    return t


def _first(s, limit: int = 220) -> str:
    """The first sentence or two of a description, without the bold."""
    t = " ".join(str(s or "").replace("**", "").split())
    if not t:
        return ""
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    out = m.group(1) if m else t
    if len(out) < 80 and m and len(t) > len(out):
        m2 = re.match(r"(.+?[.!?]\s.+?[.!?])(\s|$)", t)
        if m2:
            out = m2.group(1)
    return _flat(out, limit)


ACRONYMS = {"id": "ID", "pos": "POS", "qr": "QR", "url": "URL", "uri": "URI", "rtl": "RTL", "ltr": "LTR",
            "pin": "PIN", "sku": "SKU", "vat": "VAT", "ai": "AI", "sms": "SMS", "otp": "OTP", "nfc": "NFC",
            "rfid": "RFID", "kyc": "KYC", "api": "API", "fx": "FX", "plu": "PLU", "seo": "SEO", "faq": "FAQ",
            "faqs": "FAQs", "cta": "CTA", "ga": "GA", "iban": "IBAN", "b2b": "B2B", "b2c": "B2C", "2d": "2D",
            "3d": "3D", "kds": "KDS", "uom": "UOM", "rls": "RLS", "mfa": "MFA", "eta": "ETA"}


def humanize(name) -> str:
    """`primaryColour` -> 'Primary colour'; `slideInRight` -> 'Slide in right'; `2d` -> '2D'."""
    s = str(name)
    if s in ("", "None"):
        return "None"
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    s = s.replace("_", " ").replace("-", " ")
    words = s.split()
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if lw in ACRONYMS:
            out.append(ACRONYMS[lw])
        elif w.isupper() and len(w) > 1:
            out.append(w)
        else:
            out.append(lw if i else lw[:1].upper() + lw[1:])
    return " ".join(out)


def field_label(name: str) -> str:
    """What a person reads beside the control: `venueId` -> 'Venue', `logoAssetRef` -> 'Logo image'."""
    n = str(name)
    for suf, word in (("AssetRefs", " images"), ("AssetRef", " image"), ("AssetId", " image")):
        if n.endswith(suf):
            base = humanize(n[:-len(suf)])
            return base if base.lower().endswith(("image", "images", "video", "logo", "icon")) else base + word
    if n.endswith("Ids") and len(n) > 3:
        return humanize(n[:-3]) + "s"
    if n.endswith("Id") and len(n) > 2:
        return humanize(n[:-2])
    return humanize(n)


def _when(d: str) -> str:
    import datetime
    try:
        x = datetime.date.fromisoformat(str(d))
        return f"{x.day} {x:%b %Y}"
    except ValueError:
        return str(d or "")


# ---------------------------------------------------------------------------------------------
# the package, read once per run
# ---------------------------------------------------------------------------------------------

class Package:
    """Everything the specification reads, loaded lazily and once."""

    def __init__(self):
        self._c = {}

    def _get(self, key, fn):
        if key not in self._c:
            self._c[key] = fn()
        return self._c[key]

    # -- design inputs (tools/build-design-inputs.py) --------------------------------------------
    @property
    def di(self):
        def load():
            spec = importlib.util.spec_from_file_location("design_inputs", ROOT / "tools" / "build-design-inputs.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        return self._get("di", load)

    # -- screens ----------------------------------------------------------------------------------
    @property
    def screens(self) -> dict:
        def load():
            out = {}
            docs = []
            for f in sorted((ROOT / "screens").glob("P*.yaml")):
                doc = _sane(load_yaml(f.read_text(encoding="utf-8"))) or {}
                docs.append(doc)
                for s in doc.get("screens") or []:
                    out[s["id"]] = (s, doc.get("platform") or {})
            self._c["screen_docs"] = docs
            return out
        return self._get("screens", load)

    @property
    def screen_docs(self) -> list:
        """The screen files as read, in file order (export-design-batch.py reuses them)."""
        self.screens
        return self._c["screen_docs"]

    def name_of(self, sid: str) -> str:
        x = self.screens.get(sid)
        return x[0].get("name", "") if x else ""

    # -- contracts --------------------------------------------------------------------------------
    @property
    def contracts(self) -> dict:
        def load():
            ops, schemas, params, resps = {}, {}, {}, {}
            for f in sorted((ROOT / "contracts").rglob("*.yaml")):
                try:
                    doc = _sane(load_yaml(f.read_text(encoding="utf-8"))) or {}
                except Exception:
                    continue
                comp = doc.get("components") or {}
                for n, s in (comp.get("schemas") or {}).items():
                    schemas.setdefault(n, s)
                for n, s in (comp.get("parameters") or {}).items():
                    params.setdefault(n, s)
                for n, s in (comp.get("responses") or {}).items():
                    resps.setdefault(n, s)
                for path, item in (doc.get("paths") or {}).items():
                    if not isinstance(item, dict):
                        continue
                    for method, op in item.items():
                        if isinstance(op, dict) and op.get("operationId"):
                            ops[op["operationId"]] = {"method": method.upper(), "path": path,
                                                      "contract": f.stem, "op": op}
            return {"ops": ops, "schemas": schemas, "params": params, "responses": resps}
        return self._get("contracts", load)

    @property
    def ops(self) -> dict:
        return self.contracts["ops"]

    @property
    def schemas(self) -> dict:
        return self.contracts["schemas"]

    # -- traceability and the matrix ---------------------------------------------------------------
    @property
    def trace(self) -> dict:
        """evidence token (operation or schema) -> [row]; and xlsx row -> requirement text."""
        def load():
            by_ev = collections.defaultdict(list)
            if TRACE.exists():
                for r in json.loads(TRACE.read_text(encoding="utf-8")).get("rows") or []:
                    if r.get("evidence"):
                        by_ev[r["evidence"]].append(r)
            text = {}
            if MATRIX.exists():
                try:
                    import openpyxl
                    ws = openpyxl.load_workbook(MATRIX, read_only=True, data_only=True)["Funactionality "]
                    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                        if len(row) > 5 and row[5]:
                            text[i] = " ".join(str(row[5]).split())
                except Exception:
                    pass
            return {"by_ev": by_ev, "text": text}
        return self._get("trace", load)

    # -- task trackers ------------------------------------------------------------------------------
    @property
    def tracker(self) -> list:
        def load():
            if not TRACKER_INDEX.exists():
                return []
            return json.loads(TRACKER_INDEX.read_text(encoding="utf-8")).get("rows") or []
        return self._get("tracker", load)

    # -- white label --------------------------------------------------------------------------------
    @property
    def wl(self) -> dict:
        def load():
            if not WL_MAP.exists():
                return {}
            return json.loads(WL_MAP.read_text(encoding="utf-8"))
        return self._get("wl", load)

    # -- plan: block and ticket ---------------------------------------------------------------------
    @property
    def blocks(self) -> dict:
        """screen id -> (block, task key). plan-tasks.csv when the package has it (every block);
        otherwise tasks.csv, which holds the ticketed Block A screens."""
        def load():
            out = {}
            src = PLAN_TASKS if PLAN_TASKS.exists() else TASKS
            if not src.exists():
                return out
            with src.open(encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    m = re.match(r"^APP-[A-Z]+-([A-Z]{2,4}-\d{3})$", r.get("key") or "")
                    if m:
                        out[m.group(1)] = ((r.get("block") or "A") if src == PLAN_TASKS else "A", r["key"])
            return out
        return self._get("blocks", load)

    @property
    def tickets(self) -> dict:
        def load():
            return json.loads(PMS.read_text(encoding="utf-8")) if PMS.exists() else {}
        return self._get("tickets", load)

    # -- roles --------------------------------------------------------------------------------------
    @property
    def tiers(self) -> dict:
        """permission key -> tier (read / operate / configure), from roles-by-app.yaml."""
        def load():
            out = {}
            if not ROLES_BY_APP.exists():
                return out
            doc = load_yaml(ROLES_BY_APP.read_text(encoding="utf-8")) or {}
            for app in (doc.get("apps") or {}).values():
                for tier, keys in (app.get("tiers") or {}).items():
                    for k in keys or []:
                        out.setdefault(k, tier)
            return out
        return self._get("tiers", load)

    # -- flows and ADRs ----------------------------------------------------------------------------
    @property
    def flows(self) -> dict:
        """screen id -> [(flow id, flow name, actor, step dict)] and -> [(flow id, branch)]."""
        def load():
            steps, branches, texts = collections.defaultdict(list), collections.defaultdict(list), {}
            for f in sorted(FLOWS.glob("F*.yaml")):
                try:
                    d = _sane(load_yaml(f.read_text(encoding="utf-8"))) or {}
                except Exception:
                    continue
                fid = d.get("id")
                at = {}
                for s in d.get("steps") or []:
                    if s.get("screen"):
                        steps[s["screen"]].append((fid, d.get("name"), d.get("actor"), s))
                        at[s.get("step")] = s["screen"]
                for b in d.get("branches") or []:
                    who = {b.get("resolvedBy"), at.get(b.get("at"))} - {None}
                    for scr in who:
                        branches[scr].append((fid, b))
                texts[fid] = (d.get("name"), str(f.relative_to(ROOT)).replace("\\", "/"))
            return {"steps": steps, "branches": branches, "names": texts}
        return self._get("flows", load)

    @property
    def adrs(self) -> dict:
        def load():
            out = {}
            for f in sorted(ADR_DIR.glob("0*.md")):
                head = f.read_text(encoding="utf-8").splitlines()[0] if f.stat().st_size else ""
                m = re.match(r"#\s*ADR-(\d{4}):?\s*(.*)", head)
                if m:
                    out[f"ADR-{m.group(1)}"] = (m.group(2).strip(), str(f.relative_to(ROOT)).replace("\\", "/"))
            return out
        return self._get("adrs", load)

    # -- the app guides: reference designs and the device sentence per platform ------------------------
    @property
    def guides(self) -> dict:
        """platform -> {"guide": path, "refs": [bullet], "device": sentence}."""
        def load():
            out = {}
            for f in sorted(APPS.glob("*/README.md")):
                txt = f.read_text(encoding="utf-8")
                parts = re.split(r"(?m)^## (P\d\d)\b.*$", txt)
                for i in range(1, len(parts) - 1, 2):
                    code, body = parts[i], parts[i + 1]
                    refs = []
                    m = re.search(r"### Reference design to match\n(.*?)(?=\n### |\Z)", body, re.S)
                    if m:
                        refs = [ln[2:].strip() for ln in m.group(1).splitlines() if ln.startswith("- ")]
                    dev = ""
                    m = re.search(r"### The prompt.*?```\n(.*?)```", body, re.S)
                    if m:
                        d = re.search(r"(This is [^.]*\.)", m.group(1))
                        dev = d.group(1) if d else ""
                    out[code] = {"guide": str(f.relative_to(ROOT)).replace("\\", "/"), "refs": refs, "device": dev}
            return out
        return self._get("guides", load)


PKG = Package()


# ---------------------------------------------------------------------------------------------
# the process design notes (handoff/design-notes/<process>.yaml), authored by the process owners
# ---------------------------------------------------------------------------------------------
#
# **Chinmay, 1 October: "a dedicated agent for each process, so it is correctly refined in the
# handoff."** Nine processes each keep one authored file of what a designer must get right that the
# contracts do not say: the business rule behind a field, the edge case to draw, the correction the
# package still owes, realistic sample data. This reads them; it never writes them. A notes folder
# that is absent or empty changes nothing: every screen renders from the package alone.

NOTES_DIR = H / "design-notes"


def set_notes_dir(path) -> None:
    """Point at another notes folder (a trial export); drops what was read."""
    global NOTES_DIR
    NOTES_DIR = pathlib.Path(path).resolve()
    PKG._c.pop("notes", None)


def notes() -> dict:
    """{"processes": {name: doc}, "byScreen": {screen id: [(name, title, entry)]}}."""
    def load():
        procs, by = {}, collections.defaultdict(list)
        if NOTES_DIR.is_dir():
            for f in sorted(NOTES_DIR.glob("*.yaml")):
                try:
                    doc = _sane(load_yaml(f.read_text(encoding="utf-8"))) or {}
                except Exception:
                    continue
                if not isinstance(doc, dict):
                    continue
                name = str(doc.get("process") or f.stem)
                procs[name] = doc
                for sid, entry in (doc.get("screens") or {}).items():
                    if isinstance(entry, dict):
                        by[str(sid)].append((name, doc.get("title") or name, entry))
        return {"processes": procs, "byScreen": by}
    return PKG._get("notes", load)


def _src(x) -> str:
    if x is None or x == "":
        return ""
    if isinstance(x, (list, tuple)):
        return "; ".join(str(v) for v in x if v not in (None, ""))
    return str(x)


def _items(x) -> list:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    if isinstance(x, dict):
        return [{"field": k, "rule": v} if not isinstance(v, dict) else {"field": k, **v} for k, v in x.items()]
    return [x]


def _note_line(it, keys: tuple, rest: tuple = ()) -> str:
    """One authored item as a bullet: its subject in bold, its rule, its source in italics."""
    if not isinstance(it, dict):
        return f"- {_flat(it, 600)}"
    head = next((it[k] for k in keys if it.get(k)), "")
    body = " ".join(_flat(it[k], 700) for k in rest if it.get(k))
    src = _src(it.get("source"))
    return f"- **{_flat(head, 120)}**" + (f": {body}" if body else "") + (f" *(source: {_flat(src, 200)})*" if src else "")


def notes_for(sid: str) -> list[tuple[str, str, dict]]:
    return notes()["byScreen"].get(sid, [])


def _status(c) -> str:
    """A correction's status: '' while it is open, else fixed | logged | withdrawn (design-notes README)."""
    return str(c.get("status") or "").strip().lower() if isinstance(c, dict) else ""


def open_corrections(sid: str) -> list[tuple[str, object]]:
    """[(process title, correction)] still open on this screen: no `status` yet."""
    return [(title, c) for _, title, e in notes_for(sid) for c in _items(e.get("corrections")) if not _status(c)]


def screen_decisions(sid: str) -> list[tuple[str, dict]]:
    """[(process title, decision)]: the screen's answered questions (design-notes `decisions`)."""
    return [(title, d) for _, title, e in notes_for(sid) for d in _items(e.get("decisions")) if isinstance(d, dict)]


def _chg(c: dict) -> str:
    by = _src(c.get("by"))
    return f" ({_flat(by, 80)})" if by else ""


def render_notes_summary(sid: str) -> list[str]:
    """The process summary, then the corrections by status, then the decisions taken on the screen.

    **Only an open correction is pending** (2 October, CHG-EXP-001): main has fixed 947 of the notes'
    corrections and logged 161 as contract gaps (CHG-NOTE-*, CHG-WIR-*), and a bundle that still listed them
    as "pending" sent a design session to redraw a fix the package already carries. A fixed correction is one
    line with its change id; a logged one says the contract gap is open; a withdrawn one is left out."""
    L = []
    for name, title, e in notes_for(sid):
        if e.get("summary"):
            L += [f"**From the {_flat(title)} process.** {_flat(e['summary'], 1200)}", ""]
    for name, title, e in notes_for(sid):
        cs = _items(e.get("corrections"))
        pend = [c for c in cs if not _status(c)]
        if pend:
            L += ["**Known correction pending (do not draw the wrong version)**", ""]
            for c in pend:
                if isinstance(c, dict):
                    L.append(f"- **{_flat(c.get('what'), 300)}**" + (f" Why: {_flat(c.get('why'), 400)}" if c.get("why") else "")
                             + (f" *(source: {_flat(_src(c.get('source')), 200)}; {title})*" if c.get("source") else f" *({title})*"))
                else:
                    L.append(f"- {_flat(c, 500)}")
            L.append("")
        logged = [c for c in cs if _status(c) == "logged"]
        if logged:
            L += ["**Contract gap logged** (the fix needs an operation or field the contracts do not have yet; draw the "
                  "corrected version and mark what waits on the contract, as the open change entry says)", ""]
            L += [f"- {_flat(c.get('what'), 220)}{_chg(c)}" for c in logged] + [""]
        fixed = [c for c in cs if _status(c) == "fixed"]
        if fixed:
            L += ["**Fixed on main** (the package already carries these; draw what it says): "
                  + "; ".join(f"{_flat(c.get('what'), 140)}{_chg(c)}" for c in fixed) + ".", ""]
    L += render_notes_decisions(sid)
    return L


def render_notes_decisions(sid: str) -> list[str]:
    """**Decided** (2 October, CHG-EXP-001): each answered question on the screen, with who decided it and when.
    A decision wins over the generated tables below and over the screen's own text where they differ;
    a `reviewable` one is a default the lead may still overrule before its block is tasked, so it is drawn
    as decided and flagged in the review, not left open."""
    ds = screen_decisions(sid)
    if not ds:
        return []
    L = ["#### Decided on this screen", "",
         "Answered questions: draw the decision, not the old default. Where a decision and the tables below "
         "differ, the decision wins.", ""]
    for title, d in ds:
        by = d.get("decidedBy") or d.get("by") or "not recorded"
        flag = (" **Reviewable:** a default the lead may still overrule before the block is tasked."
                if d.get("reviewable") else "")
        L.append(f"- **{_flat(d.get('question'), 300)}** → {_flat(d.get('decision'), 600) or 'not stated'} "
                 f"*(decided by {_flat(by, 40)}, {_flat(d.get('date'), 20) or 'date not recorded'}"
                 + (f"; {_flat(_src(d.get('source')), 120)}" if d.get("source") else "") + ")*" + flag)
    L.append("")
    return L


def render_notes_section(sid: str, key: str) -> list[str]:
    """inputs / outputs / actions refinements, merged after the generated tables."""
    spec = {"inputs": (("field", "element", "name"), ("rule", "format", "note"), "Rules for these inputs"),
            "outputs": (("element", "field", "name"), ("rule", "format", "note"), "Rules for what is shown"),
            "actions": (("action", "name"), ("result", "rule", "confirmation", "failure", "note"), "What each action does")}
    keys, rest, head = spec[key]
    L = []
    for name, title, e in notes_for(sid):
        its = _items(e.get(key))
        if its:
            L += [f"**{head}** (from the {_flat(title)} process; these refine the tables above and win where they differ)", ""]
            L += [_note_line(it, keys, rest) for it in its] + [""]
    return L


def render_notes_tail(sid: str) -> list[str]:
    """Edge cases, consistency, sample data and open questions from the notes."""
    L = []
    edge, cons, samples, qs = [], [], [], []
    for name, title, e in notes_for(sid):
        edge += [(title, x) for x in _items(e.get("edgeCases"))]
        cons += [(title, x) for x in _items(e.get("consistency"))]
        if e.get("sampleData"):
            samples.append((title, e["sampleData"]))
        qs += [(title, x) for x in _items(e.get("openQuestions"))]
    if edge:
        L += ["#### Edge cases to draw", ""]
        for t, x in edge:
            L.append(_note_line(x, ("case", "name"), ("expected", "rule", "note")))
        L.append("")
    if cons:
        L += ["#### Consistency with other screens", ""]
        for t, x in cons:
            if isinstance(x, dict):
                w = x.get("with")
                w = ", ".join(f"`{v}`" for v in w) if isinstance(w, list) else f"`{w}`" if w else ""
                L.append(f"- {('Match ' + w + ': ') if w else ''}{_flat(x.get('note') or x.get('rule'), 500)}"
                         + (f" *(source: {_flat(_src(x.get('source')), 160)})*" if x.get("source") else ""))
            else:
                L.append(f"- {_flat(x, 500)}")
        L.append("")
    if samples:
        L += ["#### Sample data for the mock-up", "",
              "Seed the screen with these (realistic, in the venue's world). They outrank invented data; the schema "
              "outranks them where a value would not validate.", ""]
        for t, sd in samples:
            txt = yaml.safe_dump(sd, allow_unicode=True, sort_keys=False, width=110).rstrip()
            if len(txt) > 4000:
                txt = txt[:4000].rsplit("\n", 1)[0] + "\n# … (truncated; the full set is in handoff/design-notes/)"
            L += ["```yaml", txt, "```", ""]
    if qs:
        L += ["#### Open questions on this screen", "", "Draw the default until it is answered.", ""]
        for t, x in qs:
            if isinstance(x, dict):
                L.append(f"- **{_flat(x.get('question'), 300)}** Default: {_flat(x.get('default'), 300) or 'not stated'}"
                         + (f" *(source: {_flat(_src(x.get('source')), 160)})*" if x.get("source") else ""))
            else:
                L.append(f"- {_flat(x, 400)}")
        L.append("")
    return L


def render_process_brief(sids: list[str]) -> str:
    """For BRIEF.md: the summary and vocabulary of every process this batch's screens belong to."""
    procs = notes()["processes"]
    mine = []
    for sid in sids:
        for name, _, _ in notes_for(sid):
            if name not in mine:
                mine.append(name)
    if not mine:
        return ""
    L = ["## The processes these screens belong to", "",
         "Written by the owner of each process (`handoff/design-notes/`). Read before any screen: it says how the "
         "process runs end to end and which words the screens must use.", ""]
    for name in mine:
        d = procs.get(name) or {}
        L += [f"### {_flat(d.get('title') or name)}", ""]
        ps = d.get("processSummary")
        if isinstance(ps, dict):
            L += [_flat(ps.get("text") or ps.get("summary") or "", 3000)]
            if ps.get("source"):
                L.append(f"*(source: {_flat(_src(ps.get('source')), 300)})*")
        elif ps:
            L += [_flat(ps, 3000)]
        if d.get("processSummarySource") or d.get("source"):
            L.append(f"*(source: {_flat(_src(d.get('processSummarySource') or d.get('source')), 300)})*")
        L.append("")
        voc = _items(d.get("vocabulary"))
        if voc:
            L += ["| Say | Meaning | Never say | Source |", "|---|---|---|---|"]
            for v in voc:
                if not isinstance(v, dict):
                    continue
                avoid = v.get("avoid")
                avoid = ", ".join(map(str, avoid)) if isinstance(avoid, list) else (avoid or "")
                L.append(f"| {_flat(v.get('term'), 60)} | {_flat(v.get('meaning'), 240)} | {_flat(avoid, 120) or '—'} | "
                         f"{_flat(_src(v.get('source')), 80) or '—'} |")
            L.append("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------------------------------------
# schemas: resolving, flattening, and how a field is drawn
# ---------------------------------------------------------------------------------------------

def _refname(ref: str) -> str:
    return str(ref).rsplit("/", 1)[-1]


def resolve(node, depth: int = 0) -> tuple[dict, str | None]:
    """A schema node with `$ref` followed and `allOf` merged. Returns (schema, name it came from).

    An OpenAPI 3.1 type list (`type: [string, 'null']`) comes back as its one non-null type with
    `nullable: true`, so every reader can treat `type` as a string (check-binding-ratchet crashed on a
    list concatenated to a string in describe())."""
    s, name = _resolve(node, depth)
    t = s.get("type")
    if isinstance(t, list):
        ts = [x for x in t if x not in (None, "null")]
        s = {**s, "type": str(ts[0]) if ts else ""}
        if len(ts) < len(t):
            s["nullable"] = True
    return s, name


def _resolve(node, depth: int = 0) -> tuple[dict, str | None]:
    if not isinstance(node, dict) or depth > 8:
        return {}, None
    meta = {k: node[k] for k in ("description", "default", "readOnly", "nullable", "example")
            if k in node}
    if "$ref" in node:
        name = _refname(node["$ref"])
        s, _ = resolve(PKG.schemas.get(name, {}), depth + 1)
        return ({**s, **meta} if meta else s), name
    if "allOf" in node:
        parts = [p for p in node["allOf"] if isinstance(p, dict)]
        if len(parts) == 1 and not node.get("properties"):
            s, name = resolve(parts[0], depth + 1)
            return {**s, **meta}, name
        props, req, name, base = {}, set(), None, {}
        for p in parts:
            s, n = resolve(p, depth + 1)
            name = name or n
            props.update(s.get("properties") or {})
            req |= set(s.get("required") or [])
            for k in ("type", "description", "enum"):
                if k in s and k not in base:
                    base[k] = s[k]
        props.update(node.get("properties") or {})
        req |= set(node.get("required") or [])
        out = {**base, "type": "object", "properties": props, "required": sorted(req), **meta}
        return out, name
    for k in ("oneOf", "anyOf"):
        if k in node and node[k]:
            s, name = resolve(node[k][0], depth + 1)
            variants = [(_refname(p["$ref"]) if isinstance(p, dict) and "$ref" in p else "inline")
                        for p in node[k]]
            return {**s, **meta, "_variants": variants}, name
    return node, None


def _enum(s: dict) -> list | None:
    if s.get("enum"):
        return [v for v in s["enum"] if v is not None]
    return None


PHONE = re.compile(r"(phone|mobile|msisdn)", re.I)


def control_for(name: str, s: dict, ref: str | None) -> tuple[str, str]:
    """(control, format or mask). **Authored rule**: how a field of each type is drawn."""
    t, f, pat = s.get("type"), s.get("format"), str(s.get("pattern") or "")
    if ref == "Money":
        return "money field", "AED, 2 decimals shown (up to 4 accepted), currency from the venue's region"
    if ref in ("LocalisedText",):
        return "text, one per language", "English and Arabic (Arabic right to left)"
    if ref in ("LocalisedRichText",):
        return "rich text, one per language", "English and Arabic (Arabic right to left)"
    en = _enum(s)
    if en is not None:
        return ("segmented control" if len(en) <= 3 else "radio group" if len(en) <= 5 else "select"), ""
    if t == "boolean":
        return "toggle", ""
    if t == "array":
        it, iref = resolve(s.get("items") or {})
        if _enum(it):
            return "multi-select chips", ""
        if it.get("format") == "uuid":
            if re.search(r"Asset", name):
                return "media picker (several)", "PNG, JPG, SVG or MP4 from the media library"
            return f"multi-picker: choose {field_label(name).lower()}", ""
        if it.get("type") == "object" or it.get("properties"):
            return "repeatable rows", ""
        return "list of values (chips)", ""
    if t == "object" or s.get("properties"):
        if s.get("additionalProperties") and not s.get("properties"):
            return "key and value settings", ""
        return "group", ""
    if f == "binary":
        return "file upload", ""
    if re.search(r"(assetRef|assetId|mediaAsset|mediaId|mediaAssetId)$", name, re.I):
        return "upload, or pick from the media library", "PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4"
    if f == "uuid":
        what = field_label(name).lower()
        return f"picker: choose {'an' if what[:1] in 'aeiou' else 'a'} {what}", "shows names, sends the id"
    if f == "date":
        return "date picker", "1 Oct 2026 (dd MMM yyyy)"
    if f == "date-time":
        return "date and time picker", "1 Oct 2026, 14:30 (venue time zone)"
    if f == "time" or pat.startswith("^([01][0-9]|2[0-3])"):
        return "time picker", "HH:mm, 24-hour"
    if f == "email":
        return "email field", "name@example.ae"
    if f in ("uri", "url"):
        return "URL field", "https://"
    if "#[0-9A-Fa-f]{6}" in pat:
        return "colour picker", "#RRGGBB"
    if PHONE.search(name) and t == "string":
        return "phone field", "+971 5X XXX XXXX (E.164)"
    if pat == "^[a-z]{2}$":
        return "language picker", "ISO 639-1 code, shown as the language name"
    if t in ("integer", "number"):
        unit = " (%)" if re.search(r"percent|Pct|Rate$", name) else \
            " (minutes)" if re.search(r"Minutes|Mins$", name) else \
            " (seconds)" if re.search(r"Seconds|Secs$", name) else \
            " (hours)" if name.endswith("Hours") else " (days)" if name.endswith("Days") else ""
        lo, hi = s.get("minimum"), s.get("maximum")
        if lo is not None and hi is not None and (hi - lo) <= 100:
            return "stepper or slider" + unit, ""
        return "number field" + unit, ""
    if t == "string":
        if (s.get("maxLength") or 0) > 255 or name in ("description", "notes", "note", "body", "message",
                                                        "reason", "comment", "comments", "text"):
            return "text area", ""
        return "text field", ""
    return "field", ""


def display_for(name: str, s: dict, ref: str | None) -> str:
    """How a value is shown. **Authored rule**, applied to every output field."""
    t, f = s.get("type"), s.get("format")
    if ref == "Money":
        return "AED 1,234.50"
    if ref in ("LocalisedText", "LocalisedRichText"):
        return "in the reader's language"
    if _enum(s) is not None:
        return "chip: " + ", ".join(humanize(v) for v in _enum(s)[:6]) + ("…" if len(_enum(s)) > 6 else "")
    if t == "boolean":
        return "yes / no (icon or chip)"
    if f == "date":
        return "1 Oct 2026"
    if f == "date-time":
        return "1 Oct 2026, 14:30"
    if re.search(r"(assetRef|assetId)$", name, re.I):
        return "the image or video"
    if f == "uuid":
        return "the name it points at, never the id"
    if "#[0-9A-Fa-f]{6}" in str(s.get("pattern") or ""):
        return "colour swatch"
    if t == "integer":
        return "1,234"
    if t == "number":
        return "12.5%" if re.search(r"percent|Pct|Rate$", name) else "1,234.5"
    if t == "array":
        return "list or chips (count when long)"
    if t == "object" or s.get("properties"):
        return "grouped details"
    if f == "email":
        return "email, tap to write"
    if PHONE.search(name):
        return "+971 50 123 4567"
    return "text"


def _limits(s: dict, name: str) -> list[str]:
    out = []
    for k, label in (("minimum", "min"), ("maximum", "max"), ("minLength", "min length"),
                     ("maxLength", "max length"), ("minItems", "at least"), ("maxItems", "at most")):
        if s.get(k) is not None:
            out.append(f"{label} {s[k]}")
    if s.get("exclusiveMinimum") is not None:
        out.append(f"more than {s['exclusiveMinimum']}")
    if s.get("uniqueItems"):
        out.append("no duplicates")
    pat = str(s.get("pattern") or "")
    if pat and "#[0-9A-Fa-f]{6}" not in pat and not pat.startswith("^([01][0-9]|2[0-3])") and pat != "^[a-z]{2}$":
        out.append(f"pattern `{pat}`")
    return out


CONDITION = re.compile(r"[^.]*\b(required when|required whenever|only when|only where|only for|read only "
                       r"(for|where|by)|needs `|must include|anything but|or 400|is refused|must be earlier|"
                       r"at most|cannot be)\b[^.]*\.", re.I)


def describe(name: str, node: dict, required: bool, prefix: str = "") -> dict:
    s, ref = resolve(node)
    en = _enum(s)
    if en is None and s.get("type") == "array":
        it, _ = resolve(s.get("items") or {})
        en = _enum(it)
    ctrl, mask = control_for(name, s, ref)
    desc = " ".join(str(s.get("description") or node.get("description") or "").replace("**", "").split())
    conds = [m.group(0).strip() for m in CONDITION.finditer(desc)][:2]
    default = s.get("default", node.get("default"))
    return {
        "path": prefix + name, "name": name, "label": field_label(name), "control": ctrl, "mask": mask,
        "type": (s.get("type") or ("object" if s.get("properties") else "")) + (f" ({s['format']})" if s.get("format") else ""),
        "ref": ref, "required": required, "default": default, "enum": en,
        "limits": _limits(s, name), "help": _first(desc), "conditions": [_flat(c, 200) for c in conds],
        "readOnly": bool(s.get("readOnly") or node.get("readOnly")), "nullable": bool(s.get("nullable")),
        "deprecated": bool(s.get("deprecated") or node.get("deprecated")),
        "display": display_for(name, s, ref),
    }


def flatten(node, prefix: str = "", depth: int = 0, inputs: bool = True, out: list | None = None) -> list[dict]:
    """Every field of a schema, nested objects expanded to MAX_DEPTH. Inputs skip read-only fields.

    **A deprecated field is never drawn** (Chinmay, 2 October: `Theme.darkMode` is "kept for compatibility,
    marked deprecated, never used or drawn"; CHG-CSA-035, CHG-EXP-003): it is left out of every form, every
    output table and the white-label map, with whatever it nests."""
    out = [] if out is None else out
    s, ref = resolve(node)
    if s.get("type") == "array" and not s.get("properties"):
        s, ref = resolve(s.get("items") or {})
    req = set(s.get("required") or [])
    for k, v in (s.get("properties") or {}).items():
        rec = describe(k, v if isinstance(v, dict) else {}, k in req, prefix)
        if rec["deprecated"]:
            continue
        if inputs and rec["readOnly"]:
            continue
        if not inputs and k in PLUMBING_FIELDS:
            continue
        out.append(rec)
        if rec["ref"] in ("Money", "LocalisedText", "LocalisedRichText") or depth >= MAX_DEPTH:
            continue
        sub, _ = resolve(v if isinstance(v, dict) else {})
        if sub.get("properties"):
            flatten(sub, f"{prefix}{k}.", depth + 1, inputs, out)
        elif sub.get("type") == "array":
            it, iref = resolve(sub.get("items") or {})
            if it.get("properties") and iref not in ("Money", "LocalisedText"):
                flatten(it, f"{prefix}{k}[].", depth + 1, inputs, out)
    return out


def field_at(schema_name: str, path: str) -> dict | None:
    """The field `Schema.a.b` names, described for display."""
    s, _ = resolve({"$ref": f"#/components/schemas/{schema_name}"})
    parts = [p for p in path.replace("[]", "").split(".") if p]
    node = None
    for i, p in enumerate(parts):
        props = s.get("properties") or {}
        if p not in props:
            return None
        node = props[p]
        if i < len(parts) - 1:
            s, _ = resolve(node)
            if s.get("type") == "array":
                s, _ = resolve(s.get("items") or {})
    return describe(parts[-1], node, False) if node is not None and parts else None


# ---------------------------------------------------------------------------------------------
# operations
# ---------------------------------------------------------------------------------------------

def _param(p: dict) -> dict:
    if "$ref" in p:
        return PKG.contracts["params"].get(_refname(p["$ref"]), {})
    return p


def op_params(op_id: str, where=("query",)) -> list[dict]:
    o = PKG.ops.get(op_id)
    if not o:
        return []
    out = []
    for p in o["op"].get("parameters") or []:
        p = _param(p if isinstance(p, dict) else {})
        if p.get("in") not in where or p.get("name") in PLUMBING_PARAMS:
            continue
        rec = describe(p["name"], {**(p.get("schema") or {}), **({"description": p["description"]}
                                                                  if p.get("description") else {})},
                       bool(p.get("required")))
        rec["in"] = p.get("in")
        out.append(rec)
    return out


def request_schema(op_id: str):
    o = PKG.ops.get(op_id)
    rb = (o or {}).get("op", {}).get("requestBody") or {}
    if "$ref" in rb:
        rb = PKG.contracts["responses"].get(_refname(rb["$ref"]), {})
    for media in (rb.get("content") or {}).values():
        if isinstance(media, dict) and media.get("schema"):
            return media["schema"]
    return None


def response_schema(op_id: str):
    o = PKG.ops.get(op_id)
    resps = (o or {}).get("op", {}).get("responses") or {}
    for code in ("200", "201", "202"):
        r = resps.get(code)
        if not isinstance(r, dict):
            continue
        if "$ref" in r:
            r = PKG.contracts["responses"].get(_refname(r["$ref"]), {})
        for media in (r.get("content") or {}).values():
            if isinstance(media, dict) and media.get("schema"):
                return media["schema"], code
        return None, code
    return None, None


def op_errors(op_id: str) -> list[str]:
    o = PKG.ops.get(op_id)
    out = []
    for code, r in sorted(((o or {}).get("op", {}).get("responses") or {}).items()):
        if not str(code).startswith("4") or str(code) in ("401", "429"):
            continue
        if isinstance(r, dict) and "$ref" in r:
            name = _refname(r["$ref"])
            r = PKG.contracts["responses"].get(name, {})
        desc = _first((r or {}).get("description"), 160) if isinstance(r, dict) else ""
        shape = ""
        for media in ((r or {}).get("content") or {}).values() if isinstance(r, dict) else []:
            sch = (media or {}).get("schema") or {}
            if "$ref" in sch and _refname(sch["$ref"]) != "Problem":
                shape = f" ({_refname(sch['$ref'])})"
        out.append(f"{code} {desc}{shape}".strip())
    return out


def _schema_name_of(node) -> str:
    if not isinstance(node, dict):
        return ""
    if "$ref" in node:
        return _refname(node["$ref"])
    if node.get("items") and "$ref" in node["items"]:
        return _refname(node["items"]["$ref"]) + "[]"
    for k in ("allOf", "oneOf", "anyOf"):
        for p in node.get(k) or []:
            if isinstance(p, dict) and "$ref" in p and _refname(p["$ref"]) != "Page":
                return _refname(p["$ref"])
            if isinstance(p, dict) and (p.get("properties") or {}).get("items", {}).get("items", {}).get("$ref"):
                return _refname(p["properties"]["items"]["items"]["$ref"]) + " (paged)"
    return "inline"


# ---------------------------------------------------------------------------------------------
# rendering helpers
# ---------------------------------------------------------------------------------------------

def _allowed(rec: dict) -> str:
    bits = []
    if rec["enum"]:
        bits.append(" · ".join(f"{humanize(v)}" for v in rec["enum"][:12]) + (" …" if len(rec["enum"]) > 12 else ""))
    bits += rec["limits"]
    bits += rec["conditions"]
    return _flat("; ".join(bits), 260) or "—"


def _default(rec: dict) -> str:
    d = rec["default"]
    if d is None or d == [] or d == {}:
        return "—"
    if isinstance(d, bool):
        return "on" if d else "off"
    if isinstance(d, list):
        return ", ".join(humanize(x) for x in d)
    if rec["enum"]:
        return humanize(d)
    return _flat(str(d), 40)


def _field_rows(recs: list[dict], source: str) -> list[str]:
    rows = ["| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |",
            "|---|---|---|---|---|---|---|---|"]
    for r in recs[:MAX_FIELDS]:
        rows.append(f"| {r['label']} `{r['path']}` | {r['control']} | {'required' if r['required'] else 'optional'} | "
                    f"{_default(r)} | {_allowed(r)} | {_flat(r['mask'], 60) or '—'} | {_flat(r['help'], 180) or '—'} | {source} |")
    if len(recs) > MAX_FIELDS:
        rows.append(f"| … {len(recs) - MAX_FIELDS} more | | | | | | the rest are in `schemas.json` | {source} |")
    return rows


# ---------------------------------------------------------------------------------------------
# the screen's material
# ---------------------------------------------------------------------------------------------

def _components(s: dict) -> list[tuple[str, dict]]:
    out = []
    for r in (s.get("layout") or {}).get("regions") or []:
        for c in r.get("components") or []:
            out.append((r.get("name") or "", c))
    return out


def _screen_ops(s: dict) -> list[str]:
    ops = [a.get("operationId") for a in s.get("apis") or [] if a.get("operationId")]
    for _, c in _components(s):
        if c.get("operation"):
            ops.append(c["operation"])
    for o in s.get("overlays") or []:
        if (o.get("confirm") or {}).get("operation"):
            ops.append(o["confirm"]["operation"])
    for t in (s.get("navigation") or {}).get("transitions") or []:
        if t.get("operation"):
            ops.append(t["operation"])
    seen, out = set(), []
    for o in ops:
        if o not in seen:
            seen.add(o)
            out.append(o)
    return out


def _bound_schemas(s: dict) -> set:
    out = set()
    for _, c in _components(s):
        b = str(c.get("bindsTo") or "").split(".")[0]
        if b:
            out.add(b)
    for o in s.get("overlays") or []:
        if o.get("bindsTo"):
            out.add(str(o["bindsTo"]).split(".")[0])
    return out


def requirements_for(s: dict) -> list[tuple[dict, str]]:
    """Matrix rows whose evidence is one of this screen's operations (strong) or a schema it binds (data)."""
    by_ev = PKG.trace["by_ev"]
    seen, out = set(), []
    for o in _screen_ops(s):
        for r in by_ev.get(o, []):
            k = (r["packageRef"], r["xlsxRow"])
            if k not in seen:
                seen.add(k)
                out.append((r, f"`{o}`"))
    for b in sorted(_bound_schemas(s)):
        for r in by_ev.get(b, []):
            k = (r["packageRef"], r["xlsxRow"])
            if k not in seen:
                seen.add(k)
                out.append((r, f"data `{b}`"))
    return out


# **Authored rule: which tracker keywords reach which screens.** A tracker row reaches a screen
# when it names the screen's id, or when its text matches the left pattern and the screen's name
# (or platform, where a platform is given) matches the right. Kept narrow on purpose: a row that
# matches nothing here still reaches the batch through its platform, never a wrong screen.
TRACKER_RULES = [
    (r"seat map|seat-map|seating|seat selection|seat inventory|seat assignment|best-seat", r"\bseat"),
    (r"waiver", r"waiver"),
    (r"cookie|consent banner|consent (?:&|and) data|privacy", r"cookie|consent|privacy"),
    (r"loyalty", r"loyalty"),
    (r"wallet|stored value|gift card", r"wallet|gift card|stored value"),
    (r"virtual queue|wait[- ]time", r"queue|wait time"),
    (r"accreditation", r"accreditation"),
    (r"resale", r"resale"),
    (r"table management|floor (?:/ ?table )?map|table map|table status", r"\btable|floor plan|floor map"),
    (r"menu builder|menu & product|recipe", r"\bmenu|recipe"),
    (r"product creation wizard|product (?:config|identity)|ticket type", r"product (setup|creation|wizard|config|master|detail)|ticket type"),
    (r"promo(?:tion)? (?:code|engine)|coupon|voucher", r"promo|coupon|voucher"),
    (r"refund", r"refund"),
    (r"\bshift\b|till|cash[- ]?(?:out|drawer|up)", r"\bshift|\btill\b|cash"),
    (r"preventive maintenance|work order|asset maintenance", r"maintenance|work order"),
    (r"procurement|purchase order|item master|stock transfer", r"stock|inventory|purchase|procure|supplier"),
    (r"rental|locker", r"rental|locker"),
    (r"parking", r"parking"),
    (r"itinerary|plan your (?:adventure|visit)|visit planner|trip planner", r"plan your|planner|itinerar"),
    (r"face (?:pass|enrol)|facial recognition|biometric", r"face|biometric"),
    (r"kitchen|\bKDS\b", r"kitchen"),
    (r"approval workflow|multi-stage approval", r"approval"),
    (r"role-permission|permission matrix|roles-comparison|\bRBAC\b", r"\brole|permission"),
    (r"white[- ]?label|\bCMS\b|branding palette|page builder", r"brand|theme|typograph|logo|page builder|navigation & menus|site settings|site builder|content blocks|publishing"),
    (r"booking flow|checkout journey|step indicator|B2C checkout|ticket-booking UX|cart", r"booking|checkout|cart|ticket type selection|date & performance"),
    (r"segment(?:ation)?|journey builder|campaign", r"segment|journey|campaign"),
    (r"duplicate[- ]account|profile[- ]merge|duplicate merge", r"duplicate|merge"),
    (r"FX[- ]rate|multi-currency|foreign currency", r"currency|\bfx\b"),
    (r"games?|gaming|arcade", r"\bgame|arcade"),
    (r"transport|shuttle|station", r"transport|shuttle|station"),
]
# Rows that reach a whole platform (shown once per batch, never per screen).
TRACKER_PLATFORM = [
    (r"guest web|website|\bB2C\b|ticket-booking UX|guest (?:web/)?mobile", ("P01", "P02")),
    (r"guest (?:mobile )?app|mobile app(?! builder)", ("P02",)),
    (r"kiosk", ("P05",)),
    (r"\bPOS\b|point of sale|counter app", ("P04",)),
    (r"kitchen display|\bKDS\b", ("P15",)),
    (r"employee app|staff (?:operations )?app", ("P06",)),
    (r"scanner|ticket-validation app|handheld", ("P07",)),
    (r"back[- ]office|venue management|backend config(?:uration)? wireframes", ("P08",)),
    (r"white[- ]?label|\bCMS\b", ("P13",)),
    (r"accreditation", ("P11",)),
    (r"B2B|reseller|corporate", ("P10",)),
]


def _tracker_status(r: dict) -> str:
    st = r.get("status") or "—"
    if r.get("statusNow"):
        st += f" → 30 Sep: {r['statusNow']}" + (f", {r['whereNow']}" if r.get("whereNow") else "")
    return st


def tracker_line(r: dict, why: str = "") -> str:
    bits = [x for x in (r.get("owner"), r.get("priority"), _tracker_status(r),
                        (f"due {r['due']}" if r.get("due") else ""), _when(r.get("date") or "")) if x]
    src = "workshop tracker" if r["id"][0] in "AC" else "30 Sep tracker"
    return (f"- **{r['id']}** {_flat(r['text'], 220)} *({' · '.join(bits)} · {src}"
            + (f" · {why}" if why else "") + ")*")


def tracker_for(s: dict, plat: str) -> list[tuple[dict, str]]:
    sid, name = s["id"], s.get("name") or ""
    out, seen = [], set()
    for r in PKG.tracker:
        if sid in (r.get("screens") or []):
            out.append((r, "names this screen"))
            seen.add(r["id"])
    kw = []
    for r in PKG.tracker:
        if r["id"] in seen:
            continue
        for pat, scr in TRACKER_RULES:
            if re.search(pat, r.get("text") or "", re.I) and re.search(scr, name, re.I):
                m = re.search(pat, r["text"], re.I)
                kw.append((r, f"keyword '{m.group(0).lower()}'"))
                break

    def rank(x):
        r = x[0]
        open_ = 0 if (r.get("statusNow") or r.get("status") or "").lower() not in ("closed", "done") else 1
        return (open_, "" if not r.get("date") else "~" + r["date"])
    kw.sort(key=rank)
    return out + kw[:MAX_TRACKER]


def tracker_for_platforms(plats: set) -> dict:
    out = collections.defaultdict(list)
    for r in PKG.tracker:
        for pat, ps in TRACKER_PLATFORM:
            if re.search(pat, r.get("text") or "", re.I):
                for p in ps:
                    if p in plats:
                        out[p].append(r)
                break
    return out


def adrs_for(s: dict) -> list[str]:
    blob = json.dumps(s, ensure_ascii=False, default=str)
    for o in _screen_ops(s):
        op = PKG.ops.get(o)
        if op:
            blob += json.dumps({k: v for k, v in op["op"].items() if k in ("description",) or k.startswith("x-ticvai")},
                               ensure_ascii=False, default=str)
    for fid, _, _, st in PKG.flows["steps"].get(s["id"], []):
        blob += json.dumps(st, ensure_ascii=False, default=str)
    found = collections.Counter(re.findall(r"ADR-(\d{4})", blob))
    return [f"ADR-{n}" for n, _ in found.most_common(8)]


# ---------------------------------------------------------------------------------------------
# rendering one screen
# ---------------------------------------------------------------------------------------------

STATE_LABEL = {"loading": "Loading", "error": "Error", "emptyFirstRun": "Empty, first run",
               "emptyNoResults": "Empty, no results", "emptyNoAccess": "Permission denied",
               "offline": "Offline", "denied": "Denied"}


def render_screen(s: dict, plat: dict, stats: dict | None = None) -> str:
    sid = s["id"]
    code = plat.get("code")
    ops = _screen_ops(s)
    L: list[str] = []
    stats = stats if stats is not None else {}
    stats.setdefault("unresolved", [])

    # ---------------------------------------------------------------- 1. header
    L += [f"### `{sid}` {s.get('name')}", ""]
    if s.get("purpose"):
        L += [f"**{_flat(s['purpose'])}**", ""]
    blk = PKG.blocks.get(sid)
    if blk:
        tk = PKG.tickets.get(blk[1])
        block = f"Block {blk[0]}" + (f" · ticket #{tk} ({blk[1]})" if tk else f" · task {blk[1]}")
    else:
        block = "after Block A (B to D: set per app-module by the sprint plan)"
    actors = sorted({(fid, a) for fid, _, a, _ in PKG.flows["steps"].get(sid, []) if a})
    who = f"{plat.get('operator') or plat.get('audience')}"
    perms = sorted({(PKG.ops[o]["op"].get("x-ticvai-permission")) for o in ops
                    if o in PKG.ops and PKG.ops[o]["op"].get("x-ticvai-permission")})
    if plat.get("audience") == "guest":
        who = "a guest, signed in or not (a guest holds no permission; ADR-0025)"
    elif perms:
        tiers = collections.Counter(PKG.tiers.get(p, "?") for p in perms)
        who += " staff holding " + ", ".join(f"`{p}`" for p in perms[:6]) + ("…" if len(perms) > 6 else "") + \
            " (" + ", ".join(f"{n} {t}" for t, n in tiers.items()) + ")"
    if actors:
        acts = sorted({a for _, a in actors})
        who += "; in the flows as " + ", ".join(humanize(a).lower() for a in acts[:5])
    guide = PKG.guides.get(code) or {}
    device = guide.get("device") or f"{plat.get('formFactor')}"
    dirs = " and ".join(d.upper() for d in plat.get("directions") or ["ltr"])
    themes = ", ".join(plat.get("themes") or []) or "light"
    if code in GUEST_PLATFORMS:
        # **White label has no dark or light mode** (Chinmay, 2 October, workbook Q150 and the pre-apply
        # round; CHG-CSA-035, CHG-EXP-003): a guest screen is drawn in the venue's theme on every device
        # setting, whatever a platform file still lists.
        themes = "the venue's"
    if s.get("offline"):
        offline = _flat(json.dumps(s["offline"], ensure_ascii=False) if not isinstance(s["offline"], str) else s["offline"], 300)
    elif (s.get("states") or {}).get("offline"):
        offline = _flat((s["states"])["offline"], 300)
    elif plat.get("offlineCapable"):
        off_ops = [o for o in ops if o in PKG.ops and PKG.ops[o]["op"].get("x-ticvai-offline-capable")]
        offline = (f"works offline for {', '.join('`' + o + '`' for o in off_ops)}; the rest wait for the connection"
                   if off_ops else "this screen's operations need the connection; it says so rather than failing")
    else:
        ban = (plat.get("offlineBanner") or {}).get("message")
        offline = f"online only; offline it shows the banner \"{ban}\"" if ban else "online only"
    entry = s.get("entryState") or {}
    params = ", ".join(f"`{p.get('name')}` ({p.get('from')})" for p in entry.get("params") or [])
    L += ["| | |", "|---|---|",
          f"| App · platform | {plat.get('targetApp', {}).get('name', '')} · {code} {plat.get('shortName') or plat.get('name')} "
          f"({(plat.get('targetApp') or {}).get('shell', plat.get('formFactor'))}) |",
          f"| Module | {s.get('module')} · wave {s.get('wave')} · needs the `{s.get('requiresModule')}` module |",
          f"| Block | {block} |",
          f"| Who uses it | {_flat(who, 400)} |",
          f"| Device and orientation | {_flat(device, 200)} · {dirs} · {themes} theme |",
          f"| Pattern | {s.get('pattern')} ({s.get('density')} density): {_flat(s.get('patternReason'), 200)} |",
          f"| Offline | {offline} |",
          f"| Opens with | {params or 'nothing: it opens on its own'}" + (f" · cold entry: {_flat(entry.get('coldEntry'), 160)}" if entry.get('coldEntry') else "") + " |",
          f"| Route | `{(s.get('implementation') or {}).get('route', '')}` |", ""]
    if s.get("notes"):
        L += ["**What the spec says about it.** " + _flat(s["notes"], 1600), ""]
    gaps = [g for g in s.get("gaps") or [] if isinstance(g, dict)]
    if gaps or s.get("openQuestions"):
        L += ["**Known gaps.** " + " ".join(_flat(g.get("why"), 200) for g in gaps[:3])
              + (" Open: " + " ".join(_flat(q, 200) for q in s.get("openQuestions")[:3]) if s.get("openQuestions") else ""), ""]
    L += render_notes_summary(sid)
    stats["notes"] = len(notes_for(sid))

    # ---------------------------------------------------------------- 2. inputs
    L += ["#### Inputs: what the user enters or picks", ""]
    n_in, n_in_res = 0, 0
    covered_query = set()
    # (a) controls in the layout
    ctrl_rows = []
    for region, c in _components(s):
        if c.get("kind") not in INPUT_KINDS:
            continue
        n_in += 1
        rec, src = None, ""
        b = str(c.get("bindsTo") or "")
        notes = str(c.get("notes") or "")
        qm = re.search(r"Sends `\?(\w+)=` to `(\w+)`", notes)
        qop, qname = (qm.group(2), qm.group(1)) if qm else (None, None)
        if not qm:
            # "Narrows `listProducts?categoryId=`": the same thing said the other way round.
            qm2 = re.search(r"`(\w+)\?(\w+)=", notes)
            if qm2 and qm2.group(1) in PKG.ops:
                qop, qname, qm = qm2.group(1), qm2.group(2), qm2
        if qm:
            covered_query.add((qop, qname))
            for p in op_params(qop, ("query", "path")):
                if p["name"] == qname:
                    rec = p
            src = f"`{qop}` ?{qname}"
        elif "." in b:
            sch, path = b.split(".", 1)
            rec = field_at(sch, path)
            src = f"`{b}`"
        elif c.get("operation") and c.get("kind") in ("searchField",):
            src = f"`{c['operation']}`"
        if rec:
            n_in_res += 1
        else:
            stats["unresolved"].append((sid, c.get("label"), "no schema field: authored label only"
                                        if not b and not qm else f"{b or qm.group(0)} not found in contracts"))
        kind = humanize(c.get("kind")).lower()
        ctrl = rec["control"] if rec else kind
        if c.get("kind") == "textField" and rec and rec["control"].startswith("picker"):
            ctrl = rec["control"] + " (drawn as a picker, not a text box)"
        if rec and rec.get("deprecated"):
            ctrl = "**do not draw**: the field is deprecated and ignored"
        ctrl_rows.append(f"| {_flat(c.get('label'))} | {ctrl} | {('required' if rec['required'] else 'optional') if rec else '—'} | "
                         f"{_default(rec) if rec else '—'} | {_allowed(rec) if rec else '—'} | "
                         f"{_flat(rec['mask'], 60) if rec and rec['mask'] else '—'} | "
                         f"{_flat(notes or (rec or {}).get('help'), 200) or '—'} | {src or '—'} |")
    if ctrl_rows:
        L += ["**On the screen**", "",
              "| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |",
              "|---|---|---|---|---|---|---|---|"] + ctrl_rows + [""]
    # (b) filters a list read takes that the layout does not draw
    extra = []
    for a in s.get("apis") or []:
        o = a.get("operationId")
        if a.get("trigger") != "onLoad" or o not in PKG.ops or PKG.ops[o]["method"] != "GET":
            continue
        for p in op_params(o, ("query",)):
            if (o, p["name"]) in covered_query or p["name"] in ("venueId", "tenantId"):
                continue
            extra.append((o, p))
    if extra:
        L += ["**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)", ""]
        L += ["| Filter | Drawn as | Default | Allowed values, rules | Source |", "|---|---|---|---|---|"]
        for o, p in extra[:16]:
            L.append(f"| {p['label']} | {p['control']} | {_default(p)} | {_allowed(p)} | `{o}` ?{p['name']} |")
        if len(extra) > 16:
            L.append(f"| … {len(extra) - 16} more | | | | `operations.json` |")
        L.append("")
    # (c) forms: overlays that collect a request body, and actions that send one
    formed = set()
    for ov in s.get("overlays") or []:
        op = (ov.get("confirm") or {}).get("operation")
        if not op:
            continue
        formed.add(op)
        rs = request_schema(op)
        L += [f"**Form: {_flat(ov.get('trigger'))}** ({ov.get('component')}, opened by *{_flat(ov.get('trigger'))}*; "
              f"*{_flat((ov.get('confirm') or {}).get('label'))}* calls `{op}`, *{_flat((ov.get('dismiss') or {}).get('label') or 'Cancel')}* sends nothing)", ""]
        if ov.get("body"):
            L += [_flat(ov["body"], 700), ""]
        if rs:
            recs = flatten(rs)
            n_in += len(recs)
            n_in_res += len(recs)
            path_params = [p for p in op_params(op, ("path",))]
            if recs:
                L += _field_rows(recs, f"`{op}` body") + [""]
            if path_params:
                L += ["Carried, not typed: " + ", ".join(f"`{p['name']}`" for p in path_params), ""]
        else:
            qp = op_params(op, ("query",))
            if qp:
                n_in += len(qp)
                n_in_res += len(qp)
                L += _field_rows(qp, f"`{op}` query") + [""]
            elif op not in PKG.ops:
                stats["unresolved"].append((sid, ov.get("trigger"), f"form calls `{op}`, which no contract defines"))
                L += [f"`{op}` is not in any contract: draw the form greyed and list it in FINDINGS.md.", ""]
            else:
                L += ["Sends no fields: a confirmation, not a form.", ""]
        errs = op_errors(op)
        if errs:
            L += ["Errors to draw in the form: " + "; ".join(_flat(e, 200) for e in errs[:5]), ""]
    for region, c in _components(s):
        op = c.get("operation")
        if c.get("kind") not in ACTION_KINDS or not op or op in formed or op not in PKG.ops:
            continue
        if PKG.ops[op]["method"] == "GET":
            continue
        rs = request_schema(op)
        if not rs:
            continue
        recs = flatten(rs)
        if not recs:
            continue
        formed.add(op)
        n_in += len(recs)
        n_in_res += len(recs)
        L += [f"**Sent by *{_flat(c.get('label'))}*** (`{op}`; no form is declared, so these are filled from the screen "
              "or collected inline)", ""] + _field_rows(recs, f"`{op}` body") + [""]
    if n_in == 0:
        L += ["Nothing to enter: the screen reads and acts, and every action sends what the screen already holds.", ""]
    stats["inputs"] = n_in
    stats["inputs_resolved"] = n_in_res
    L += render_notes_section(sid, "inputs")

    # ---------------------------------------------------------------- 3. outputs
    L += ["#### Outputs: what the screen shows and produces", ""]
    n_out, n_out_res = 0, 0
    shown = []
    for region, c in _components(s):
        k = c.get("kind")
        if k in INPUT_KINDS or k in ACTION_KINDS:
            continue
        cols = c.get("columns") or []
        bind = str(c.get("bindsTo") or "")
        recs = []
        for col in cols:
            col = str(col)
            if "." in col:
                sch, path = col.split(".", 1)
                r = field_at(sch, path)
            else:
                r = field_at(bind, col) if bind else None
            n_out += 1
            if r:
                n_out_res += 1
                recs.append((col, r))
            else:
                recs.append((col, None))
        if not cols and c.get("operation") and c["operation"] in PKG.ops:
            rsch, _ = response_schema(c["operation"])
            if rsch:
                for r in flatten(rsch, inputs=False)[:20]:
                    n_out += 1
                    n_out_res += 1
                    recs.append((r["path"], r))
        head = f"**{_flat(c.get('label') or humanize(k))}** ({humanize(k).lower()}" + \
               (f", from `{c['operation']}`" if c.get("operation") else "") + ")"
        body = [head + (": " + _flat(c.get("notes"), 400) if c.get("notes") else "")]
        if recs:
            body.append("")
            body.append("| Shows | Format | Notes |")
            body.append("|---|---|---|")
            for col, r in recs[:30]:
                if r:
                    body.append(f"| {r['label']} | {_flat(r['display'], 90)} | {_flat(r['help'], 140) or '—'} |")
                else:
                    body.append(f"| {humanize(col.split('.')[-1])} | text | not in the schema: `{col}` |")
            if len(recs) > 30:
                body.append(f"| … {len(recs) - 30} more | | `schemas.json` |")
        shown.append("\n".join(body))
    if shown:
        L += ["**Shown**", ""] + sum([[x, ""] for x in shown], [])
    stats["outputs"] = n_out
    stats["outputs_resolved"] = n_out_res

    acts = []
    for region, c in _components(s):
        if c.get("kind") not in ACTION_KINDS:
            continue
        op = c.get("operation")
        o = PKG.ops.get(op) if op else None
        if not o:
            acts.append(f"| {_flat(c.get('label'))} ({humanize(c['kind']).lower()}) | {('`' + op + '` (not in any contract)') if op else 'navigation or local'} | — | — | — | — |")
            continue
        rsch, code_ = response_schema(op)
        res = _schema_name_of(rsch) if rsch else ("no body" if code_ else "—")
        x = o["op"]
        notes = []
        if x.get("x-ticvai-step-up"):
            notes.append(f"step-up: {x['x-ticvai-step-up']} ({_flat(x.get('x-ticvai-step-up-reason'), 120)})")
        if x.get("x-ticvai-emits"):
            notes.append("emits " + ", ".join(f"`{e}`" for e in x["x-ticvai-emits"]))
        if x.get("x-ticvai-offline-capable") and plat.get("offlineCapable"):
            notes.append("works offline")
        if c.get("permission"):
            notes.append(f"gated `{c['permission']}`")
        ov = next((v for v in s.get("overlays") or [] if (v.get("confirm") or {}).get("operation") == op), None)
        if ov:
            notes.append(f"opens {ov.get('component')} first")
        if re.search(r"receipt|print|e-?mail|pdf|wallet pass|ticket", f"{op} {x.get('summary')}", re.I):
            notes.append("produces a document or message: " + _flat(x.get("summary"), 80))
        errs = op_errors(op)
        acts.append(f"| {_flat(c.get('label'))} ({humanize(c['kind']).lower()}) | `{op}` {o['method']} `{o['path']}` | "
                    f"{_schema_name_of(request_schema(op)) if request_schema(op) else '—'} | {res} | "
                    f"{_flat('; '.join(errs[:3]), 220) or '—'} | {_flat('; '.join(notes), 260) or '—'} |")
    if acts:
        L += ["**Actions and what each produces**", "",
              "| Action | Calls | Sends | On success returns | Errors to show | Notes |", "|---|---|---|---|---|---|"] + acts + [""]
    L += render_notes_section(sid, "outputs")
    L += render_notes_section(sid, "actions")
    reads = [a for a in s.get("apis") or [] if a.get("trigger") in ("onLoad", "onInterval", "background")]
    if reads:
        L += ["**Data it reads**: " + "; ".join(
            f"`{a['operationId']}` ({a.get('trigger')}{', ' + _flat(a.get('purpose'), 60) if a.get('purpose') else ''})"
            for a in reads[:12]), ""]
    tr = (s.get("navigation") or {}).get("transitions") or []
    if tr:
        L += ["**Where the user goes next**", ""]
        for t in tr:
            L.append(f"- → `{t.get('to')}` {PKG.name_of(t.get('to'))}: *{_flat(t.get('trigger'), 120)}*"
                     + (f"; carries {', '.join('`' + x + '`' for x in t['carries'])}" if t.get("carries") else "")
                     + (f"; only when {_flat(t['precondition'], 120)}" if t.get("precondition") else "")
                     + (f"; calls `{t['operation']}`" if t.get("operation") else ""))
        L.append("")
    other_ov = [o for o in s.get("overlays") or [] if not (o.get("confirm") or {}).get("operation")]
    if other_ov:
        L += ["**What opens over it**", ""] + [
            f"- {o.get('component')} *{_flat(o.get('trigger'), 80)}*: {_flat(o.get('body'), 300)}" for o in other_ov[:8]] + [""]

    # ---------------------------------------------------------------- 4. states
    L += ["#### States", "", "| State | What it shows |", "|---|---|"]
    states = dict(s.get("states") or {})
    if "offline" not in states:
        states["offline"] = offline
    for k, v in states.items():
        L.append(f"| {STATE_LABEL.get(k, humanize(k))} (`?state={k}`) | {_flat(v, 500)} |")
    val = sorted({e for o in ops for e in op_errors(o) if e.startswith("400") or e.startswith("409") or e.startswith("422")})
    if val:
        L.append(f"| Validation and conflict | the form keeps what was entered and marks the problem: {_flat('; '.join(val[:4]), 400)} |")
    m = s.get("machine")
    if isinstance(m, dict) and m.get("states"):
        L.append(f"| In progress (`{m.get('key')}`) | starts at *{m.get('initial')}*; " + "; ".join(
            f"*{k}*: {_flat((v or {}).get('note'), 120)}" for k, v in list(m["states"].items())[:8]) + " |")
    L.append("")
    stats["states"] = len(states)
    L += render_notes_tail(sid)

    # ---------------------------------------------------------------- 5. permissions
    L += ["#### Permissions", ""]
    prow = []
    for o in ops:
        x = (PKG.ops.get(o) or {}).get("op")
        if not x:
            continue
        p = x.get("x-ticvai-permission")
        aud = ", ".join(x.get("x-ticvai-audience") or [])
        prow.append(f"`{o}` → {('`' + p + '` (' + PKG.tiers.get(p, 'tier not set') + ')') if p else 'no permission'}"
                    f" · {aud or 'audience not set'}" + (f" · step-up {x['x-ticvai-step-up']}" if x.get("x-ticvai-step-up") else ""))
    if prow:
        L += ["- " + "\n- ".join(prow), ""]
    deny = (s.get("states") or {}).get("emptyNoAccess") or (s.get("states") or {}).get("denied")
    if deny:
        L += [f"**A refused user sees:** {_flat(deny, 500)}", ""]
    if s.get("permission"):
        L += [f"Screen guard: `{_flat(s['permission'], 120)}`", ""]

    # ---------------------------------------------------------------- 6. requirements
    reqs = requirements_for(s)
    stats["requirements"] = len(reqs)
    L += ["#### Requirements it meets", ""]
    if reqs:
        L += [f"{len(reqs)} rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) "
              "trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; "
              "the screen's block is its delivery priority.", "",
              "| Ref | Requirement (shortened) | Domain | Verdict | Via |", "|---|---|---|---|---|"]
        for r, via in reqs[:MAX_REQS]:
            txt = PKG.trace["text"].get(r.get("xlsxRow")) or r.get("note") or ""
            L.append(f"| {r['matrixRef']} | {_flat(txt, 200)} | {r.get('domain', '')} | {r['verdict']} | {via} |")
        if len(reqs) > MAX_REQS:
            L.append(f"| … {len(reqs) - MAX_REQS} more | | | | `traceability.json` |")
        L.append("")
    else:
        L += ["No matrix row traces to this screen's operations or data.", ""]

    # ---------------------------------------------------------------- 7. client meeting inputs
    sel = PKG.di.for_screens([(sid, code, s.get("module"))])
    mine = sel["screen"].get(sid, [])
    stats["mom"] = len(mine)
    stats["mom_wider"] = len(sel["global"]) + sum(map(len, sel["platform"].values())) + sum(map(len, sel["module"].values()))
    L += ["#### Client meeting inputs", ""]
    if mine:
        L += ["For this screen, newest first. An **Open question** is built to the default it states."
              " Where an item disagrees with the fields above, the item wins.", ""]
        L += [PKG.di.line(e) for e in mine] + [""]
    else:
        L += ["None names this screen.", ""]
    wider = []
    if sel["module"]:
        wider.append(f"{sum(map(len, sel['module'].values()))} for {code} · {s.get('module')}")
    if sel["platform"]:
        wider.append(f"{sum(map(len, sel['platform'].values()))} for all of {code}")
    if sel["global"]:
        wider.append(f"{len(sel['global'])} for every app")
    if wider:
        L += ["Also apply: " + ", ".join(wider) + " (section *Design inputs from the client meetings* below).", ""]

    # ---------------------------------------------------------------- 8. tracker
    trk = tracker_for(s, code)
    stats["tracker"] = len(trk)
    L += ["#### Workshop task tracker", ""]
    if trk:
        L += [tracker_line(r, why) for r, why in trk] + [""]
    else:
        L += ["No tracker row concerns this screen; the rows for its platform are listed once, below.", ""]

    # ---------------------------------------------------------------- 9. white label
    wl = PKG.wl
    if wl:
        g = (wl.get("guestScreens") or {}).get(sid)
        c = (wl.get("configScreens") or {}).get(sid)
        if g is not None:
            els = {e["id"]: e for e in wl.get("elements") or []}
            specific = [els[i] for i in g.get("specific", []) if i in els]
            L += ["#### Configurable by the tenant", "",
                  f"This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the "
                  f"*Powered by TICVAI* credit, a tenant toggle that is on by default: `brand.showPoweredBy`). It has "
                  f"no dark or light mode: the venue's theme applies on every device setting. Draw it with the "
                  f"**default theme**, and on the key screens one **alternate tenant theme** (`{WHITE_LABEL_DOC}`).", "",
                  f"**Shell-wide, on every guest screen:** " + "; ".join(
                      f"{p['label']} ({p['count']}, {', '.join(p['screens'])})" for p in wl.get("shellParts") or []) +
                  f". Each element, its CMS field, allowed values and default: `{WHITE_LABEL_DOC}`.", ""]
            if specific:
                L += ["**Specific to this screen** (the tenant's setting is the input; the right column is what it "
                      "changes here). Draw each with its default, and the alternate where the alternate theme sets one.", ""]
                L += _wl_specific(specific)
            stats["whiteLabel"] = len(specific)
        elif c is not None:
            els = {e["id"]: e for e in wl.get("elements") or []}
            mine_ = [els[i] for i in c if i in els]
            L += ["#### What this screen configures on the guest surfaces", "",
                  "Each field here is an **input** a tenant sets; the right column is the **output** a guest sees "
                  f"once it is published (CMS-014). The full map: `{WHITE_LABEL_DOC}`.", "",
                  "| Field | Allowed values | Default | Reaches | What it changes |", "|---|---|---|---|---|"]
            for e in mine_[:60]:
                L.append(f"| {e['label']} (`{e['id']}`) | {_flat(e.get('allowed'), 200) or '—'} | {_flat(e.get('default'), 40) or '—'} | "
                         f"{_flat(e.get('reachesText'), 160)} | {_flat(e.get('effect') or e.get('help'), 220) or '—'} |")
            if len(mine_) > 60:
                L.append(f"| … {len(mine_) - 60} more | | | | `WHITE-LABEL.md` |")
            L.append("")
            stats["whiteLabel"] = len(mine_)

    # ---------------------------------------------------------------- 10. references
    L += ["#### References", ""]
    w = s.get("wireframe") or {}
    refs = []
    if w:
        refs.append(f"Wireframe frame: `{w.get('board')}` · status **{w.get('status')}** · provenance {w.get('provenance') or '—'}"
                    + (f" · {_flat(w.get('note'), 200)}" if w.get("note") else ""))
        p = w.get("prototype")
        if isinstance(p, dict):
            refs.append(f"Prototype ({p.get('rev', '')}, verified {p.get('verified', '—')}, match {p.get('match', '—')}): "
                        f"`{p.get('file')}`, view *{_flat(p.get('view'), 160)}*"
                        + (f". Differences: {_flat(p.get('differences'), 500)}" if p.get("differences") else ""))
        cnd = w.get("candidate")
        if isinstance(cnd, dict):
            refs.append(f"Candidate (not client-approved): `{cnd.get('file')}` ({_flat(cnd.get('rev'), 80)}), view *{_flat(cnd.get('view'), 160)}*"
                        + (f", capture `{cnd.get('capture')}`" if cnd.get("capture") else "")
                        + (f". Differences: {_flat(cnd.get('differences'), 400)}" if cnd.get("differences") else ""))
        if w.get("workshopBoard"):
            refs.append(f"Client workshop board: `{w['workshopBoard']}`")
        if w.get("derivedFrom"):
            refs.append(f"Derived from `{w['derivedFrom']}`")
        if w.get("source"):
            refs.append(f"Drawn by: {_flat(w['source'], 160)}")
    if s.get("boardFrames"):
        refs.append("Client design-board frames: " + ", ".join(f"`{b}`" for b in s["boardFrames"][:6]))
    src = s.get("source")
    if isinstance(src, dict) and (src.get("pack") or src.get("board")):
        refs.append(f"Workshop pack: {_flat(src.get('pack'), 80)} {('board ' + str(src.get('board'))) if src.get('board') else ''}".rstrip())
    for fid, fname, actor, st in PKG.flows["steps"].get(sid, [])[:8]:
        refs.append(f"Flow {fid} *{_flat(fname, 80)}*, step {st.get('step')}: {_flat(st.get('action'), 120)} → {_flat(st.get('outcome'), 200)}")
    if len(PKG.flows["steps"].get(sid, [])) > 8:
        refs.append(f"… and {len(PKG.flows['steps'][sid]) - 8} more flow steps (`flows/`)")
    for fid, b in PKG.flows["branches"].get(sid, [])[:5]:
        refs.append(f"Flow {fid} branch at step {b.get('at')} ({b.get('severity')}): when {_flat(b.get('condition'), 120)}, {_flat(b.get('behaviour'), 200)}")
    for a in adrs_for(s):
        t = PKG.adrs.get(a)
        if t:
            refs.append(f"{a} *{t[0]}* (`{t[1]}`)")
    L += [f"- {r}" for r in refs] + [""] if refs else ["None recorded.", ""]

    # ---------------------------------------------------------------- 11. acceptance
    st_names = list(states)
    targets = [t.get("to") for t in tr]
    act_labels = [_flat(c.get("label"), 40) for _, c in _components(s) if c.get("kind") in ACTION_KINDS]
    errs_all = sorted({e.split(" ")[0] for o in ops for e in op_errors(o)})
    L += ["#### Acceptance for the design", "",
          f"- [ ] Every input above is drawn ({stats['inputs']}), with its required mark, default, format and its "
          f"error state{(' (' + ', '.join(errs_all) + ')') if errs_all else ''}.",
          f"- [ ] Every output is drawn ({stats['outputs']} fields) with realistic seeded data in the format given (AED, dates, names, never ids).",
          f"- [ ] Every state opens from `#{sid}?state=<state>`: {', '.join(st_names)}.",
          (f"- [ ] Every action is wired with its success and its failure: {', '.join(act_labels)}." if act_labels else
           "- [ ] The screen has no action of its own; nothing is drawn as a button that does nothing."),
          (f"- [ ] Every transition is wired: {', '.join('`' + x + '`' for x in targets if x)}." if targets else
           "- [ ] No transition is declared; back returns where the user came from."),
          ("- [ ] Every gated control is gated: " + ", ".join(f"`{p}`" for p in perms[:8]) + "." if perms and plat.get('audience') != 'guest'
           else "- [ ] Sign-in is asked only where the spec asks for it."),
          (f"- [ ] The {len(mine)} client meeting input(s) for this screen are applied; open questions are built to their default." if mine
           else "- [ ] The module and platform inputs below are applied."),
          ]
    if wl and (wl.get("guestScreens") or {}).get(sid) is not None:
        L.append("- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.")
    if wl and (wl.get("configScreens") or {}).get(sid) is not None:
        L.append("- [ ] Every field shows its allowed values and default, and a live preview shows the output on the guest screen it reaches.")
    n_edge = sum(len(_items(e.get("edgeCases"))) for _, _, e in notes_for(sid))
    n_corr = len(open_corrections(sid))
    n_dec = len(screen_decisions(sid))
    if n_edge:
        L.append(f"- [ ] The {n_edge} edge case(s) from the process notes are drawn.")
    if n_corr:
        L.append(f"- [ ] The {n_corr} pending correction(s) are respected: the corrected version is drawn, never the one the package still shows.")
    if n_dec:
        L.append(f"- [ ] The {n_dec} decision(s) taken on this screen are drawn as decided, not as the old default.")
    L += ["- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).", ""]
    return "\n".join(L)


def _wl_meaningful(e: dict) -> bool:
    """An element worth a row of its own: it has a choice, a default or a stated effect."""
    return bool(e.get("effect") or (e.get("allowed") and e["allowed"] != "—") or (e.get("default") and e["default"] != "—"))


def _wl_specific(els: list[dict]) -> list[str]:
    """Per part: a table of the elements with a choice or a default, then the plain fields in one line."""
    L = []
    by = collections.OrderedDict()
    for e in els:
        by.setdefault(e["part"], []).append(e)
    for part, xs in by.items():
        where = ", ".join(f"`{x['screen']}` {x['name']}" for x in xs[0].get("configuredOn") or []) or "no CMS screen yet"
        L += [f"*{xs[0]['partLabel']}*, set in {where}:", ""]
        rich = [e for e in xs if _wl_meaningful(e)]
        plain = [e for e in xs if not _wl_meaningful(e)]
        if rich:
            L += ["| Setting | Allowed values | Default | What it changes here |", "|---|---|---|---|"]
            for e in rich[:24]:
                L.append(f"| {e['label']} (`{e['id']}`) | {_flat(e.get('allowed'), 200) or '—'} | "
                         f"{_flat(e.get('default'), 40) or '—'} | {_flat(e.get('effect') or e.get('help'), 220) or '—'} |")
            if len(rich) > 24:
                L.append(f"| … {len(rich) - 24} more | | | `WHITE-LABEL.md` |")
            L.append("")
        if plain:
            L += ["Also set there, as content the tenant writes: " + ", ".join(
                f"{e['label'].lower()}" for e in plain[:30]) + (" …" if len(plain) > 30 else "") + ".", ""]
    return L


def screen_index_row(s: dict, plat: dict, st: dict) -> str:
    sid = s["id"]
    blk = PKG.blocks.get(sid)
    w = (s.get("wireframe") or {})
    wl = PKG.wl
    wlm = "guest" if (wl.get("guestScreens") or {}).get(sid) is not None else \
        "configures" if (wl.get("configScreens") or {}).get(sid) is not None else "—"
    return (f"| `{sid}` | {s.get('name')} | {blk[0] if blk else 'B–D'} | {st.get('inputs', 0)} | {st.get('outputs', 0)} | "
            f"{st.get('states', 0)} | {st.get('requirements', 0)} | {st.get('mom', 0)} | {st.get('tracker', 0)} | {wlm} | "
            f"{w.get('status', '—')} ({w.get('provenance') or '—'}) |")


def batch_tenant_section(screens: list[tuple[dict, dict]]) -> str:
    """Once per batch: the shell-wide tenant configuration, for batches with a guest screen."""
    wl = PKG.wl
    if not wl or not any((wl.get("guestScreens") or {}).get(s["id"]) is not None for s, _ in screens):
        return ""
    els = {e["id"]: e for e in wl.get("elements") or []}
    L = ["## Tenant configuration on every guest screen", "",
         "Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply "
         "to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the "
         "default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is "
         f"configuration, not paint. The full map, with the input-to-output examples: `{WHITE_LABEL_DOC}`.", "",
         "| Element | Configured in | Allowed values | Default | What it changes |", "|---|---|---|---|---|"]
    for i in wl.get("shell") or []:
        e = els.get(i)
        if not e:
            continue
        where = ", ".join(f"`{x['screen']}`" for x in e.get("configuredOn") or []) or "—"
        L.append(f"| {e['label']} (`{e['id']}`) | {where} | {_flat(e.get('allowed'), 160) or '—'} | "
                 f"{_flat(e.get('default'), 30) or '—'} | {_flat(e.get('effect') or e.get('help'), 180) or '—'} |")
    alt = wl.get("alternateTheme") or {}
    if alt:
        L += ["", f"**The alternate tenant theme ({alt.get('name')})**: " + "; ".join(
            f"{k} {v}" for k, v in (alt.get("values") or {}).items()) + ".",
            "**Key screens to show in it:** " + ", ".join(f"`{x}`" for x in alt.get("keyScreens") or []) + "."]
    dec = wl.get("decided") or []
    if dec:
        L += ["", "**Decided for every guest screen:** " + " ".join(_flat(x, 300) for x in dec)]
    fixed = wl.get("fixed") or []
    if fixed:
        L += ["", "**Never configurable:** " + " ".join(_flat(x, 240) for x in fixed)]
    return "\n".join(L) + "\n"


def batch_references(plats: set) -> str:
    L = ["## Reference designs and the trackers for this platform", ""]
    for p in sorted(plats):
        g = PKG.guides.get(p) or {}
        if g.get("refs"):
            L += [f"**{p} reference designs** (from `{g['guide']}`)", ""] + [f"- {r}" for r in g["refs"]] + [""]
    vb = [e for e in PKG.di.active() if "vision_book" in str((e.get("source") or {}).get("file", "")).lower()
          and any(str(t) == "global" or str(t) in plats for t in e.get("scope") or [])]
    if vb:
        L += [f"**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): "
              + ", ".join(e["id"] for e in vb) + " (each is in the design inputs below).", ""]
    tp = tracker_for_platforms(plats)
    for p in sorted(tp):
        rows = tp[p]
        open_ = [r for r in rows if (r.get("statusNow") or r.get("status") or "").lower() not in ("closed", "done")]
        closed = len(rows) - len(open_)
        L += [f"**Workshop tracker rows about {p} as a whole** ({len(rows)}: {len(open_)} open, {closed} closed). "
              "Open first; a closed row says where it went on 30 September.", ""]
        L += [tracker_line(r) for r in (open_ + [r for r in rows if r not in open_])[:14]]
        if len(rows) > 14:
            L.append(f"- … {len(rows) - 14} more in `handoff/design-inputs/task-tracker-index.json`")
        L.append("")
    return "\n".join(L)
