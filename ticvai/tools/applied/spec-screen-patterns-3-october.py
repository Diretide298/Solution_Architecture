#!/usr/bin/env python3
"""Fix the six screen patterns the Block A audit of 3 October found, across every platform.

**Decided by Chinmay on 3 October 2026: fix the specs now, refresh, cut r1 of a fresh start**
(`changes/entries/CHG-AUD-001-block-a-audit-patterns-for-r3.yaml`; the brief is the r1 spec-fix pass).
The audit judged 75 r2 tickets from their developer pulls; the zero-AI pattern scans then counted each
pattern across the package. Every one came from a generator or a move nothing checked afterwards, so
this fixes the instances and `tools/check-screen-patterns.py` keeps them fixed. The rules are
`tools/screen_patterns.py`, shared with the check and the generators.

  CHG-SPF-001  P1   forms stop asking for readOnly fields: the field leaves the form's Required /
                    Optional lists and its discards, and the form says the server sets it
  CHG-SPF-002  P2   lists and panels show the fields the screen is about: at most five on a phone or
                    handheld, plumbing and foreign ids out, a generated dump narrowed; the apisNote
                    that admitted "Columns are every field" says what was done instead
  CHG-SPF-003  P3   the no-access state names the read's permission for viewing and each action's
                    permission where the actions need more, read off the operations
  CHG-SPF-004  P5   a required entry parameter nothing carries becomes optional where the screen can
                    list and choose (or creates it), or an inbound edge that holds it carries it
  CHG-SPF-005  P7b  a screen merged into another as a section says so (`implementation.sectionOf`);
                    a screen wearing another screen's route or component gets its own, from its name
  CHG-SPF-006  P8   every Block A screen is wave 1, and notes that still say it is out of the first
                    release are rewritten as the history they are

**Screens are authored**, so nothing is regenerated: each edit finds its target and does nothing when
it is gone, and only the screens it changes are rewritten in their files (spliced, at the file's own
dump width), so a hand edit elsewhere is untouched. A second run says there is nothing to do.

    python tools/applied/spec-screen-patterns-3-october.py [--apply] [--only P1,P2,...]
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import screen_patterns as sp  # noqa: E402

DATE = "3 October 2026"


# ── the files, rewritten one screen at a time ───────────────────────────────────────────────────

class NoAliasDumper(yaml.SafeDumper):
    """One screen is written at a time, so an anchor in one could be aliased from another."""

    def ignore_aliases(self, data):
        return True


class ScreenFiles:
    """Every `screens/P*.yaml`: its text, its data, and a writer that splices only changed screens."""

    def __init__(self):
        self.text, self.doc, self.width = {}, {}, {}
        for f in sorted((ROOT / "screens").glob("P*.yaml")):
            t = f.read_text(encoding="utf-8")
            self.text[f] = t
            self.doc[f] = sp._load(str(f))
            self.width[f] = self._width(f)
        self.screens, self.where = {}, {}
        for f, d in self.doc.items():
            for s in d["screens"]:
                s["_plat"] = d["platform"]["code"]
                self.screens[s["id"]] = s
                self.where[s["id"]] = f
        self.dirty: set[str] = set()

    def blocks(self, f):
        lines = self.text[f].split("\n")
        starts = [i for i, l in enumerate(lines) if l.startswith("- id: ")]
        out = []
        for k, i in enumerate(starts):
            j = i + 1
            while j < len(lines) and not re.match(r"^(- |[A-Za-z_#])", lines[j]):
                j += 1
            while j > i + 1 and not lines[j - 1].strip():        # trailing blank lines stay put
                j -= 1
            out.append((lines[i][6:].strip().strip("'\""), i, j))
        return lines, out

    def _width(self, f):
        lines, bl = self.blocks(f)
        best, score = 100, -1
        for w in (100, 98):
            n = 0
            for (sid, i, j), s in zip(bl[:25], self.doc[f]["screens"][:25]):
                n += self.dump(s, w) == "\n".join(lines[i:j]).rstrip()
            if n > score:
                best, score = w, n
        return best

    @staticmethod
    def dump(s, width):
        clean = {k: v for k, v in s.items() if not k.startswith("_")}
        return yaml.dump([clean], Dumper=NoAliasDumper, sort_keys=False, allow_unicode=True,
                         width=width).rstrip()

    def write(self):
        changed = []
        for f in self.text:
            ids = {sid for sid in self.dirty if self.where[sid] == f}
            if not ids:
                continue
            lines, bl = self.blocks(f)
            byid = {s["id"]: s for s in self.doc[f]["screens"]}
            # **A rewritten screen is written without anchors**, so a screen elsewhere in the file
            # that aliases an anchor it defined (`*id001`) is rewritten too, with the value in place.
            text_of = {sid: "\n".join(lines[i:j]) for sid, i, j in bl}
            grew = True
            while grew:
                defined = {a for sid in ids for a in re.findall(r"&(id\d+)", text_of[sid])}
                more = {sid for sid, t in text_of.items() if sid not in ids
                        and any(f"*{a}" in t for a in defined)}
                more |= {sid for sid, t in text_of.items() if sid not in ids and any(
                    f"*{a}" in text_of[d] for d in ids for a in re.findall(r"&(id\d+)", t))}
                grew = bool(more)
                ids |= more
            out, last = [], 0
            for sid, i, j in bl:
                if sid in ids:
                    out.extend(lines[last:i])
                    out.extend(self.dump(byid[sid], self.width[f]).split("\n"))
                    last = j
            out.extend(lines[last:])
            new = "\n".join(out)
            if new != self.text[f]:
                yaml.load(new, Loader=yaml.CSafeLoader)          # it still parses, or nothing is written
                f.write_text(new, encoding="utf-8")
                changed.append(f.name)
        return changed


# ── P1 ───────────────────────────────────────────────────────────────────────────────────────────

def strip_listed(body: str, fields: set) -> str:
    """Take `field` out of the Required: / Optional: lists of a form's body, and say why."""
    def clean(seg: str) -> str:
        for f in sorted(fields):
            tok = r"`" + re.escape(f) + r"`(\s*\([^)]*\))?"
            seg = re.sub(tok + r",\s*", "", seg)
            seg = re.sub(r",?\s*(and\s+)?" + tok, "", seg)
        return seg
    m = re.search(r"(Required:)(.*?)(?=Optional:|Dismissing|$)", body, re.S)
    if m:
        seg = clean(m.group(2))
        if not re.search(r"`\w+`", seg):
            body = body[:m.start()] + "Nothing in the body is required. " + body[m.end():].lstrip()
        else:
            body = body[:m.start(2)] + seg + body[m.end(2):]
    m = re.search(r"(Optional:)(.*?)(?=Dismissing|$)", body, re.S)
    if m:
        seg = clean(m.group(2))
        if not re.search(r"`\w+`", seg):
            body = body[:m.start()] + body[m.end():].lstrip()
        else:
            body = body[:m.start(2)] + seg + body[m.end(2):]
    body = re.sub(r" +\.", ".", re.sub(r"  +", " ", body))
    note = ("Not asked, because the server sets "
            + ("it" if len(fields) == 1 else "them") + " (readOnly in the contract): "
            + ", ".join(f"`{f}`" for f in sorted(fields)) + f" ({DATE}, CHG-SPF-001).")
    if "Dismissing" in body and "readOnly in the contract" not in body:
        body = body.rstrip() + " " + note
    return body


def fix_p1(pk, s, log):
    hit = False
    for o in s.get("overlays") or []:
        if not isinstance(o, dict):
            continue
        op = (o.get("confirm") or {}).get("operation")
        sch = pk.request_schema(op) if op else None
        if not sch:
            continue
        ro = {f for f in sp.overlay_asked(o) if sp.read_only(sch, f)}
        if not ro:
            continue
        d = o.get("dismiss") or {}
        if d.get("discards"):
            d["discards"] = [x for x in d["discards"] if x not in ro]
        o["body"] = strip_listed(str(o.get("body") or ""), ro)
        log.append(f"P1 {s['id']}: {o.get('id')} stops asking for {', '.join(sorted(ro))}")
        hit = True
    for r in (s.get("layout") or {}).get("regions") or []:
        keep = []
        for c in r.get("components") or []:
            if isinstance(c, dict) and c.get("kind") in sp.INPUT_KINDS and \
                    "." in str(c.get("bindsTo") or "") and c.get("operation"):
                field = str(c["bindsTo"]).split(".", 1)[1]
                sch = pk.request_schema(c["operation"])
                if sch and field in sch["properties"] and sp.read_only(sch, field):
                    log.append(f"P1 {s['id']}: input '{c.get('label')}' ({field}) removed")
                    hit = True
                    continue
            keep.append(c)
        if len(keep) != len(r.get("components") or []):
            r["components"] = keep
    return hit


# ── P2 ───────────────────────────────────────────────────────────────────────────────────────────

NOTE_RE = re.compile(r"Columns are every field the response schema declares, plumbing aside\s*—\s*"
                     r"narrowing them to the ones that matter is work a person still owes this "
                     r"screen\.?")
NOTE_NEW = (f"Columns narrowed on {DATE} to the fields the screen is about (CHG-SPF-002): at most "
            f"five on a phone or handheld, plumbing and foreign ids left to the record itself.")


# **A guest screen never shows a staff field** (GFIX-3, 2 October): the same lists the guest fixes
# used, so a narrowed guest panel cannot pick `lifecycleState` or `requiresApprovalToCancel`.
GUEST = {"P01", "P02", "P05"}
_spec = importlib.util.spec_from_file_location(
    "guest_fixes", Path(__file__).resolve().parent / "guest-screen-fixes-2-october.py")
_gf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gf)
GUEST_STAFF, GUEST_STAFF_ON = set(_gf.STAFF), dict(_gf.STAFF_ON)


def fix_p2(pk, s, log):
    sid = s["id"]
    hit = False
    small = pk.small(sid)
    base_hints = " ".join(str(s.get(k) or "") for k in ("notes", "purpose", "purposeNote"))
    for _, c in sp.components(s):
        cols = [str(x) for x in (c.get("columns") or [])]
        kind = c.get("kind")
        if not cols or kind not in sp.COLUMN_KINDS:
            continue
        name, sch = sp.column_schema(pk, c)
        props = set((sch or {}).get("properties") or {})
        fields = {x.split(".", 1)[1].split(".")[0] for x in cols if x.startswith(name + ".")}
        dump = (small and len(cols) > sp.SMALL_MAX) or \
               (props and len(props) >= 4 and props <= fields and
                len(cols) > (sp.PICK_SMALL if small else sp.PICK_DESKTOP)[kind]) or \
               (not small and sp.generated(c) and len(cols) > sp.DESKTOP_CAP[kind])
        if not dump:
            continue
        hints = base_hints + " " + str(c.get("notes") or "") + " " + str(c.get("label") or "")
        drop = (GUEST_STAFF | GUEST_STAFF_ON.get(name, set())) if s["_plat"] in GUEST else set()
        new = sp.pick_columns(pk, c, small, hints, drop)
        if new != cols:
            c["columns"] = new
            log.append(f"P2 {sid}: {kind} '{c.get('label')}' {len(cols)} -> {len(new)} columns")
            hit = True
    note = str(s.get("apisNote") or "")
    if sp.COLUMNS_NOTE.search(note):
        new = NOTE_RE.sub(NOTE_NEW, note)
        if sp.COLUMNS_NOTE.search(new):              # a hand-wrapped variant: cut the sentence
            new = re.sub(r"Columns are every field[^.]*\.?", NOTE_NEW, note)
        s["apisNote"] = new
        log.append(f"P2 {sid}: apisNote no longer says the columns are every field")
        hit = True
    return hit


# ── P3 ───────────────────────────────────────────────────────────────────────────────────────────

STOCK_NA = re.compile(r"^Shown when the caller lacks `[A-Za-z0-9_.:-]+`, which `\w+` requires, and "
                      r"names that permission\.( \*\*Never an empty table\*\*[^\n]*)?$")
KIT_PREFIX = re.compile(r"^(This display is not assigned to a station\. \*\*Assignment is a "
                        r"back-office act\*\* — a kitchen screen does not choose what it shows\. )")
# Where the old text named a permission only as history ("was X until 29 September"), the current
# one is put in backticks so it is the one a reader (and the check) takes as named.
BACKTICK = {"BO-228": "ACCESS_OVERRIDE", "BO-232": "INCIDENT_MANAGE"}


def actions_sentence(full: str) -> str:
    i = full.find(" A caller who can see the screen")
    return full[i:] if i >= 0 else ""


def fix_p3(pk, s, log, exempt):
    sid = s["id"]
    if not sp.p3(pk, sid, s) or sid in exempt:
        return False
    st = s["states"]
    old = str(st["emptyNoAccess"]).strip()
    gen = sp.no_access_text(pk, s)
    if not gen:
        return False
    if sid in BACKTICK:
        p = BACKTICK[sid]
        new = old.replace(f"**{p}**", f"**`{p}`**")
    elif STOCK_NA.match(old):
        new = gen
    else:
        named = sp.named_permissions(old)
        _, lp, ap, act = sp.screen_perms(pk, s)
        if named - ap:
            m = KIT_PREFIX.match(old)
            new = (m.group(1) if m else "") + gen
        else:
            new = old
            if "`" not in new:              # bare names: backtick the ones the screen's operations need
                new = re.sub(r"\b([A-Z]+_[A-Z0-9_]+)\b",
                             lambda m: f"`{m.group(1)}`" if m.group(1) in ap else m.group(1), new)
            if lp and not (named & lp):
                rop = sorted((x["operationId"] for x in sp.apis(s)
                              if x.get("trigger") in sp.LOAD_TRIGGERS and pk.op_perms(x["operationId"])),
                             key=lambda o: not o.startswith(("list", "get", "search")))[0]
                rp = sorted(pk.op_perms(rop))[0]
                new = (f"Without `{rp}`, which `{rop}` requires, the screen does not load and this "
                       f"state names that permission. ") + new
            if act and not (sp.named_permissions(new) & act):
                new = new.rstrip() + actions_sentence(gen)
    if new != old:
        st["emptyNoAccess"] = new
        log.append(f"P3 {sid}: no-access rewritten")
        return True
    return False


# ── P5 ───────────────────────────────────────────────────────────────────────────────────────────

def held_by(pk, src: dict, name: str, dst: dict) -> bool:
    """Does `src` have `name` in hand to pass to `dst`? Its own params and preloads, or an operation of
    the contract `dst` reads `name` with that returns it (or returns the rows it is the id of)."""
    for p in sp.entry_params(src):
        if p["name"] == name:
            return True
    for pre in ((src.get("entryState") or {}).get("preloaded") or []):
        ent, _, field = str(pre).partition(".")
        if (field == "id" and ent and ent[0].lower() + ent[1:] + "Id" == name) or field == name:
            return True
    scope = {(pk.ops.get(x["operationId"]) or {}).get("_contract") for x in sp.apis(dst)
             if "{" + name + "}" in (pk.ops.get(x["operationId"]) or {}).get("_path", "")}
    stem = sp.stem_of(name).lower()
    for x in sp.apis(src):
        o = pk.ops.get(x["operationId"]) or {}
        if scope and o.get("_contract") not in scope:
            continue
        got = pk.response_props(x["operationId"])
        if name in got or "{" + name + "}" in o.get("_path", ""):
            return True
        if any(g.startswith("@") and g[1:].lower().endswith(stem) for g in got):
            return True                     # it lists, reads or makes the rows `name` identifies
    return False


# Decided by hand for the Block A screens the rules above could not settle (3 October).
P5_EDGE = {   # (destination, param): the screen that lists them and now links here carrying one
    ("GST-061", "outletId"): "GST-024",     # F&B browse & order -> Menu Item Detail
    ("WEB-037", "outletId"): "WEB-036",     # Where you can eat now -> Menu Item Detail
    ("GST-006", "performanceId"): "GST-005",  # What's On -> the performance
    ("BO-827", "programmeId"): "BO-833",      # lists the loyalty programmes -> a programme's rules
    ("ADM-603", "accountId"): "ADM-602",      # B2B credit accounts -> an account's payment terms
}
P5_OPTIONAL = {
    ("BO-010", "dashboardId"): "the promotions themselves load without it; the dashboard panel "
                               "shows only when a link names a saved dashboard",
    ("WEB-040", "entryId"): "opened from Home, the guest joins a queue here with `joinQueue` and "
                            "the screen follows that place; a link to a place opens it directly",
    ("GST-023", "entryId"): "opened from Home, the guest joins a queue here with `joinQueue` and "
                            "the screen follows that place; a link to a place opens it directly",
    ("ADM-016", "packageId"): "`getSitePackage` follows a package only after this screen has "
                              "generated one; the screen opens without it",
}
# A download is something a person does, not something the screen loads (CHG-SPF-004).
DOWNLOAD_ON_ACTION = {"getTaxDocumentRendition"}


def fix_p5(pk, F, sid, s, inb, log):
    hit = False
    for x in sp.apis(s):
        if x["operationId"] in DOWNLOAD_ON_ACTION and x.get("trigger") == "onLoad" and                 str(x.get("purpose", "")).lower().startswith("download"):
            x["trigger"] = "onAction"
            log.append(f"P5 {sid}: {x['operationId']} is a download, now onAction")
            hit = True
    for (dst, name), src in P5_EDGE.items():
        if dst != sid or any(name in c for _, c in inb.get(sid, [])):
            continue
        tr = F.screens[src].setdefault("navigation", {}).setdefault("transitions", [])
        if not any(str(t.get("to", "")).partition("#")[0] == sid for t in tr if isinstance(t, dict)):
            tr.append({"to": sid, "trigger": s["name"], "carries": [name],
                       "provenance": f"authored {DATE} (CHG-SPF-004): {src} lists them, and {sid} "
                                     f"cannot load without the one the user picks"})
            ex = F.screens[src]["navigation"].setdefault("exitTo", [])
            if sid not in ex:
                ex.append(sid)
            F.dirty.add(src)
            inb.setdefault(sid, []).append((src, {name}))
            log.append(f"P5 {sid}: {name} carried on a new edge from {src}")
            hit = True
    for p in sp.entry_params(s):
        if (sid, p["name"]) in P5_OPTIONAL and not p.get("optional"):
            p["optional"] = True
            p["notes"] = f"Optional ({DATE}, CHG-SPF-004): {P5_OPTIONAL[(sid, p['name'])]}."
            log.append(f"P5 {sid}: {p['name']} optional (by hand)")
            hit = True
    for p in sp.entry_params(s):
        if p.get("optional") or p.get("from") in ("session", "previousScreen"):
            continue
        name = p["name"]
        edges = inb.get(sid, [])
        if any(name in c for _, c in edges):
            continue
        own = sp.reads_itself(pk, s, name)
        if own:
            p["optional"] = True
            how = (f"the screen lists them with `{own}` and the user picks one"
                   if own.startswith(("list", "search")) else f"the screen reads it with `{own}`")
            p["notes"] = (f"Optional ({DATE}, CHG-SPF-004): opened without it, {how}; an edge "
                          f"that holds one may still carry it to open on that record.")
            log.append(f"P5 {sid}: {name} optional (finds it with {own})")
            hit = True
            continue
        made = sp.creates(pk, s, name)
        if made:
            p["optional"] = True
            p["notes"] = (f"Optional ({DATE}, CHG-SPF-004): opened without it, the screen makes "
                          f"one with `{made}`; a link or an edge that holds one opens it instead.")
            log.append(f"P5 {sid}: {name} optional (made by {made})")
            hit = True
            continue
        a = sp.apis(s)
        in_path = [x for x in a if "{" + name + "}" in (pk.ops.get(x["operationId"]) or {}).get("_path", "")]
        loads = [x for x in in_path if x.get("trigger") in sp.LOAD_TRIGGERS]
        if name in SESSION_IDS and s["_plat"] in STAFF_PLATFORMS:
            p["from"] = "session"
            p["notes"] = (f"From the session ({DATE}, CHG-SPF-004): a staff screen works in the "
                          f"{sp.stem_of(name)} its sign-in or device is scoped to; nothing navigates "
                          f"to it (the venue-scope rule).")
            log.append(f"P5 {sid}: {name} from the session")
            hit = True
        elif in_path and not loads:
            ops = ", ".join(f"`{x['operationId']}`" for x in in_path[:3])
            p["optional"] = True
            p["notes"] = (f"Optional ({DATE}, CHG-SPF-004): the screen loads without it; {ops} "
                          f"take{'s' if len(in_path) == 1 else ''} the id from the record the user "
                          f"acts on, and an edge or link that holds one only pre-selects it.")
            log.append(f"P5 {sid}: {name} optional (only actions take it)")
            hit = True
        elif not in_path and not any(isinstance(q, dict) and q.get("name") == name
                                     for x in a for q in (pk.ops.get(x["operationId"]) or {})
                                     .get("parameters") or []):
            p["optional"] = True
            p["notes"] = (f"Optional ({DATE}, CHG-SPF-004): no operation on the screen takes it; "
                          f"a link that carries it only pre-selects the record.")
            log.append(f"P5 {sid}: {name} optional (no operation takes it)")
            hit = True
        else:
            # **The load needs it**: an inbound edge whose source holds it carries it.
            carried = []
            for src, _ in edges:
                if held_by(pk, F.screens[src], name, s):
                    for t in (F.screens[src].get("navigation") or {}).get("transitions") or []:
                        if isinstance(t, dict) and str(t.get("to", "")).partition("#")[0] == sid \
                                and name not in (t.get("carries") or []):
                            t["carries"] = list(t.get("carries") or []) + [name]
                            prov = str(t.get("provenance") or "")
                            t["provenance"] = (f"authored {DATE} (CHG-SPF-004): {src} holds {name} "
                                               f"and {sid} cannot load without it, so the edge "
                                               f"carries it" + (f"; was: {prov}" if prov else ""))
                            F.dirty.add(src)
                            carried.append(src)
            if carried:
                log.append(f"P5 {sid}: {name} now carried from {', '.join(sorted(set(carried)))}")
                hit = True
    return hit


SESSION_IDS = {"tenantId", "venueId", "workstationId", "outletId", "terminalId", "shiftId",
               "deviceId", "stationId"}
STAFF_PLATFORMS = {"P04", "P06", "P07", "P08", "P09", "P12", "P15", "P16"}


# ── P7b ──────────────────────────────────────────────────────────────────────────────────────────

SUFFIXES = ("List", "Detail", "Board", "Canvas", "Form", "Wizard", "Dashboard", "Display")


def pascal(text: str) -> str:
    return "".join(w[:1].upper() + w[1:] for w in re.findall(r"[A-Za-z0-9]+", text))[:48] or "Screen"


def slug(text: str) -> str:
    return "-".join(w.lower() for w in re.findall(r"[A-Za-z0-9]+", text))[:56]


def fix_p7b(pk, F, sid, s, owners, routes, log):
    im = s.get("implementation") or {}
    comp = str(im.get("component") or "")
    if not comp:
        return False
    hit = False
    sharers = owners.get((im.get("app"), comp), [])
    host = re.search(r"Merged into ([A-Z]+-\d+)[^.]*section", str(s.get("notes") or ""))
    if len(sharers) > 1 and host and host.group(1) in sharers and host.group(1) != sid:
        if im.get("sectionOf") != host.group(1):
            im["sectionOf"] = host.group(1)
            log.append(f"P7b {sid}: a section of {host.group(1)}, rendered in its component")
            return True
        return False
    if im.get("sectionOf") or im.get("status") not in (None, "notStarted"):
        return False
    findings = sp.p7b(pk, sid, s, owners)
    name = str(s["name"]).replace("F&B", "FnB")
    folder, file_ = comp.rsplit("/", 1)
    if any("component" in d and "does not name" in d for _, _, d in findings):
        stem = file_.split(".")[0]
        suffix = "" if name.endswith("Sign In") else next((x for x in SUFFIXES if stem.endswith(x)), "")
        base = pascal(name)
        new = f"{folder}/{base}{'' if base.endswith(suffix) else suffix}.tsx"
        if (im.get("app"), new) in owners:                # the name is another screen's already
            new = f"{folder}/{base}{sid.replace('-', '')}{'' if base.endswith(suffix) else suffix}.tsx"
        if new != comp and (im.get("app"), new) not in owners:
            im["component"] = new
            log.append(f"P7b {sid}: component {file_} -> {new.rsplit('/', 1)[-1]}")
            hit = True
    if any("route" in d and "does not name" in d for _, _, d in findings):
        route = str(im.get("route") or "")
        head = route.rstrip("/").rsplit("/", 1)[0] if route.count("/") > 1 else ""
        new = f"{head}/{slug(name)}"
        if (im.get("app"), new) in routes:
            new = f"{new}-{sid.lower()}"
        if new != route and (im.get("app"), new) not in routes:
            routes.add((im.get("app"), new))
            im["route"] = new
            log.append(f"P7b {sid}: route {route} -> {new}")
            hit = True
    return hit


# ── P8 ───────────────────────────────────────────────────────────────────────────────────────────

R187_OLD = ("**Out of the first release** (decided 28 September, audit R187): the itinerary planner "
            "is deferred and this screen is `wave: 4` with a `deferred` block. Kept, not deleted, for "
            "the release that builds it.")
R187_NEW = ("**Deferred on 28 September (audit R187), and brought back the next day**: the itinerary "
            "planner was put in `wave: 4` with a `deferred` block and kept rather than deleted; the "
            "29 September re-plan below superseded that, and the screen is in Block A, wave 1 "
            f"({DATE}, CHG-SPF-006).")
GAPC3_OLD = "Had stayed in wave 4 (GAP-C3); superseded the same day by the re-plan below."
GAPC3_NEW = "Had stayed deferred (GAP-C3); superseded the same day by the re-plan below."
TEXT = {
    "BO-005": [("a Wave 1 flow cannot step through a Wave 2 screen.",
                "a flow cannot step through a screen that is built after it.")],
    "BO-074": [("so it cannot be Wave 2 while venue provisioning is Wave 1.",
                "so it cannot be built after venue provisioning.")],
    "GST-022": [("Pulled to Wave 2 (CF-101) with the queue platform F21 runs on.",
                 "Pulled forward (CF-101) with the queue platform F21 runs on; in Block A since the "
                 "1 October plan.")],
    "GST-051": [(R187_OLD, R187_NEW), (GAPC3_OLD, GAPC3_NEW),
                ("The R187 note that put the planner out of the first release (wave 4) was "
                 "superseded", "The R187 note that deferred the planner was superseded")],
    "GST-052": [(R187_OLD, R187_NEW), (GAPC3_OLD, GAPC3_NEW),
                ("the planner is deferred (R187)", "the planner was deferred (R187)")],
    "GST-053": [(R187_OLD, R187_NEW), (GAPC3_OLD, GAPC3_NEW)],
    "GST-054": [(R187_OLD, R187_NEW), (GAPC3_OLD, GAPC3_NEW),
                ("the planner is deferred (R187)", "the planner was deferred (R187)"),
                ("**The AI half is Wave 2** — the manual planner must work without it (CF-41).",
                 "**The AI half came second in the 10 August minutes** — the manual planner must "
                 "work without it (CF-41); since the 29 September re-plan (MOB-6) both are in "
                 "Block A.")],
    "GST-059": [(R187_OLD, R187_NEW), (GAPC3_OLD, GAPC3_NEW),
                ("the planner is deferred (R187)", "the planner was deferred (R187)")],
    "KSK-015": [("**Wave 2 with the rest of the kiosk.** Set to Wave 1 in error on 17 August — an "
                 "assistant that guides a guest through ticket selection and checkout cannot ship "
                 "before the screens that do the selecting and the checking out.",
                 "**Built with the kiosk's selection and checkout screens** (17 August): an "
                 "assistant that guides a guest through ticket selection and checkout cannot ship "
                 "before the screens that do the selecting and the checking out.")],
    "SUP-004": [("Pulled to Wave 2 (CF-101). **The guest concierge is Phase 1 and a handover needs "
                 "somewhere to land** — the queue and the workspace move; the rest of the console "
                 "stays Wave 3.",
                 "Pulled forward (CF-101), and in Block A since the 1 October plan: **the guest "
                 "concierge is Phase 1 and a handover needs somewhere to land** — the queue and the "
                 "workspace move; the rest of the console comes later.")],
    "SUP-005": [("Pulled to Wave 2 (CF-101) with SUP-004.",
                 "Pulled forward (CF-101) with SUP-004, into Block A.")],
    "WEB-035": [("Wave 1 against the app's Wave 2, because",
                 "First on the website, before the app, because")],
}


def fix_p8(s, block_a, log):
    sid = s["id"]
    if sid not in block_a:
        return False
    hit = False
    if str(s.get("wave")) != "1":
        log.append(f"P8 {sid}: wave {s.get('wave')} -> 1")
        s["wave"] = 1
        hit = True
    for old, new in TEXT.get(sid, []):
        for k in ("notes", "purposeNote"):
            v = s.get(k)
            if isinstance(v, str) and old in v:
                s[k] = v.replace(old, new)
                log.append(f"P8 {sid}: {k} '{old[:40]}…' rewritten")
                hit = True
    return hit


# ── run ──────────────────────────────────────────────────────────────────────────────────────────

P3_EXEMPT = {"POS-008"}     # see check-screen-patterns EXEMPT: the contract, not the screen, moves


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="P1,P2,P3,P5,P7b,P8")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--remaining", action="store_true", help="print what the rules still find")
    a = ap.parse_args()
    only = set(a.only.split(","))
    F = ScreenFiles()
    pk = sp.Package(str(ROOT), screens=F.screens)   # the rules read the very dicts this edits
    for code, f in ((d["platform"]["code"], f) for f, d in F.doc.items()):
        pk.platforms[code] = F.doc[f]["platform"]
    block_a = sp.block_a_screens(str(ROOT)) or set()
    log: list[str] = []
    inb = sp.inbound(F.screens)
    owners = sp.component_owners(F.screens)
    routes = {((s.get("implementation") or {}).get("app"), (s.get("implementation") or {}).get("route"))
              for s in F.screens.values()}
    for sid, s in F.screens.items():
        hit = False
        if "P1" in only:
            hit |= fix_p1(pk, s, log)
        if "P2" in only:
            hit |= fix_p2(pk, s, log)
        if "P3" in only:
            hit |= fix_p3(pk, s, log, P3_EXEMPT)
        if "P5" in only:
            hit |= fix_p5(pk, F, sid, s, inb, log)
        if "P7b" in only:
            hit |= fix_p7b(pk, F, sid, s, owners, routes, log)
        if "P8" in only:
            hit |= fix_p8(s, block_a, log)
        if hit:
            F.dirty.add(sid)
    c = Counter(x.split(" ", 1)[0] for x in log)
    if a.verbose:
        print("\n".join(log))
    print(f"{len(F.dirty)} screen(s) to change: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items()))
          if log else "nothing to do")
    if a.remaining:
        inb2, own2 = sp.inbound(F.screens), sp.component_owners(F.screens)
        for sid, s in F.screens.items():
            for r, _, d in ((sp.p1(pk, sid, s) if "P1" in only else [])
                            + (sp.p2(pk, sid, s) if "P2" in only else [])
                            + (sp.p3(pk, sid, s) if "P3" in only else [])
                            + (sp.p5(pk, sid, s, inb2) if "P5" in only else [])
                            + (sp.p7b(pk, sid, s, own2) if "P7b" in only else [])
                            + (sp.p8(pk, sid, s, block_a, {}) if "P8" in only else [])):
                print(f"  left {r} {sid} {d}")
    if a.apply and F.dirty:
        print("written: " + ", ".join(F.write()))
    elif F.dirty:
        print("nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
