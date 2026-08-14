#!/usr/bin/env python3
"""
Render low-fidelity wireframes from the screen definitions.

180 screens are specified and 9 have an approved wireframe. The other 171 have a template, a
set of regions, a component list and their states written down — which is enough to draw the
structure, and structure is what a client validates before pixels.

**These are deliberately ugly.** Grey boxes and labels, no colour, no type choices, no spacing
decisions. A wireframe that looks designed invites comment on the design; one that looks like a
wireframe invites comment on whether the right things are on the screen, which is the only
question worth asking at this stage.

What is drawn comes from the definition and nothing else. Where a screen declares an offline
state, it is shown — the offline states are the most important lines in the POS and scanner
definitions and they are invisible in a static mockup otherwise.

Output: wireframes/index.html, one page per platform, one per flow, one per screen.
"""
import html
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"
if not CONTRACTS.exists():
    CONTRACTS = ROOT / "contracts"
SCREENS = ROOT / "screens"
FLOWS = ROOT / "flows"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "wireframes"

# How each component kind draws. Height is a hint, not a design.
SHAPE = {
    "dataTable": ("table", 150), "cardList": ("cards", 130), "detailPanel": ("fields", 110),
    "metricTile": ("tiles", 70), "chart": ("chart", 120), "timeline": ("timeline", 110),
    "emptyState": ("empty", 90), "textField": ("field", 40), "numberField": ("field", 40),
    "selectField": ("field", 40), "multiSelect": ("field", 40), "datePicker": ("field", 40),
    "toggle": ("toggle", 32), "searchField": ("search", 38), "fileUpload": ("upload", 70),
    "signaturePad": ("box", 80), "primaryButton": ("btn-primary", 38),
    "secondaryButton": ("btn", 38), "destructiveButton": ("btn-danger", 38),
    "iconButton": ("btn-icon", 38), "banner": ("banner", 44), "toast": ("banner", 36),
    "modal": ("box", 90), "confirmDialog": ("box", 80), "progressIndicator": ("bar", 26),
    "scanTarget": ("scan", 150), "seatMap": ("seatmap", 180), "saleBoard": ("board", 170),
    "cartPanel": ("cart", 170), "paymentTerminal": ("terminal", 120),
    "queuePosition": ("box", 70), "assetTag": ("tag", 44), "consentBlock": ("fields", 90),
    "livePreview": ("preview", 160),
}
REGION_ORDER = ["statusStrip", "appHeader", "sideNav", "contentBody", "contextPanel",
                "actionBar", "bottomNav"]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#f4f4f5;color:#18181b;
     font:13px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
a{color:#18181b}
.wrap{max-width:1180px;margin:0 auto;padding:28px 22px 60px}
h1{font-size:20px;margin:0 0 4px;font-weight:650}
h2{font-size:15px;margin:34px 0 10px;font-weight:650}
.sub{color:#71717a;margin:0 0 22px;max-width:70ch}
.note{background:#fff;border:1px solid #e4e4e7;border-left:3px solid #a1a1aa;
      padding:10px 13px;margin:0 0 22px;max-width:74ch;color:#3f3f46}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{background:#fff;border:1px solid #e4e4e7;padding:13px;text-decoration:none;display:block}
.card:hover{border-color:#a1a1aa}
.card h3{margin:0 0 3px;font-size:13px;font-weight:650}
.card .m{color:#71717a;font-size:11px}

/* the frame */
.frame{background:#fff;border:1px solid #d4d4d8;margin:0 0 26px}
.frame .bar{background:#fafafa;border-bottom:1px solid #e4e4e7;padding:7px 11px;
            font-size:11px;color:#52525b;display:flex;justify-content:space-between}
.frame .body{padding:0}
.rg{border-bottom:1px dashed #e4e4e7;padding:11px 13px}
.rg:last-child{border-bottom:none}
.rg-l{font-size:9px;letter-spacing:.09em;text-transform:uppercase;color:#a1a1aa;margin-bottom:7px}
.row{display:flex;gap:9px;flex-wrap:wrap;align-items:flex-start}
.el{background:#f4f4f5;border:1px solid #e4e4e7;flex:1;min-width:150px;
    display:flex;align-items:center;justify-content:center;color:#71717a;font-size:11px;
    text-align:center;padding:5px}
.el.sm{flex:0 0 auto;min-width:104px}
.el.btn-primary{background:#3f3f46;color:#fff;border-color:#3f3f46}
.el.btn-danger{background:#fff;border-color:#a1a1aa;color:#52525b}
.el.banner{background:#fafafa;border-style:dashed}
.el.scan,.el.seatmap,.el.board,.el.preview{background:repeating-linear-gradient(45deg,#fafafa,#fafafa 7px,#f4f4f5 7px,#f4f4f5 14px)}
.tip{color:#71717a;font-size:10.5px;margin:4px 0 0;max-width:66ch;font-style:italic}
.el-full{flex:1 1 100%;min-width:0}
table.wf{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e4e4e7}
table.wf th{background:#fafafa;font-size:10px;letter-spacing:.05em;text-transform:uppercase;
            color:#71717a;text-align:left;padding:6px 8px;border-bottom:1px solid #e4e4e7;font-weight:600}
table.wf td{padding:6px 8px;border-bottom:1px solid #f4f4f5;color:#52525b;font-size:11.5px}
.src{font-size:10px;color:#a1a1aa;margin:4px 0 0}
.fields{background:#fff;border:1px solid #e4e4e7}
.fld{display:flex;justify-content:space-between;padding:6px 9px;border-bottom:1px solid #f4f4f5;font-size:11.5px}
.fld:last-child{border-bottom:none}
.fld span{color:#71717a}.fld i{font-style:normal;color:#3f3f46}
.fld.tot{background:#fafafa;font-weight:650}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px}
.cardbox{background:#fff;border:1px solid #e4e4e7}
.el.tile{flex:1 1 130px;min-width:130px;flex-direction:column;gap:2px;padding:11px;min-height:64px}
.el.tile b{font-size:19px;color:#3f3f46;font-weight:650}
.el.tile span{font-size:10px;color:#a1a1aa}
.el.field{justify-content:space-between;padding:9px 11px}
.el.field i{font-style:normal;color:#a1a1aa;font-size:10.5px}
.board{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:7px}
.tilebox{background:#fff;border:1px solid #e4e4e7;padding:15px 8px;text-align:center;
         font-size:11px;color:#52525b}

table.st{border-collapse:collapse;width:100%;background:#fff;border:1px solid #e4e4e7;margin:0 0 22px}
table.st td,table.st th{border:1px solid #e4e4e7;padding:6px 9px;text-align:left;vertical-align:top;font-size:12px}
table.st th{background:#fafafa;font-weight:650;width:104px;color:#52525b}
.pill{display:inline-block;background:#f4f4f5;border:1px solid #e4e4e7;padding:1px 7px;
      font-size:10.5px;color:#52525b;margin:0 4px 4px 0}
.pill.off{background:#3f3f46;color:#fff;border-color:#3f3f46}
.crumb{font-size:11px;color:#71717a;margin:0 0 16px}
.flowstep{display:flex;gap:11px;align-items:flex-start;margin:0 0 9px}
.flowstep .n{background:#3f3f46;color:#fff;width:21px;height:21px;flex:0 0 21px;
             display:flex;align-items:center;justify-content:center;font-size:11px}
.br{color:#71717a;font-size:11.5px;margin:2px 0 0 32px}
"""


OPSCHEMA: dict = {}


def load_schemas() -> None:
    """Resolve each operation to the fields its response actually carries.

    A wireframe drawing a box labelled "dataTable" tells a reviewer nothing. One drawing
    `orderNumber · status · grossAmount · channel` lets them say the channel column is missing,
    which is the comment worth having.

    566 of 642 operations resolve. The rest return no schema — 204s, redirects, and the
    handful whose response is a plain array of strings.
    """
    docs = {}
    for sub in ("spine", "satellite", "shared"):
        for f in (CONTRACTS / sub).glob("*.yaml"):
            docs[f.stem] = yaml.safe_load(f.read_text())

    def props(ctx, name, depth=0):
        d = docs.get(ctx, {})
        sch = ((d.get("components") or {}).get("schemas") or {}).get(name)
        if not sch or depth > 2:
            return []
        if "allOf" in sch:
            out = []
            for part in sch["allOf"]:
                if "$ref" in part:
                    m = re.search(r"([\w-]+)\.yaml#/components/schemas/(\w+)|#/components/schemas/(\w+)",
                                  part["$ref"])
                    if m:
                        out += props(m.group(1) or ctx, m.group(2) or m.group(3), depth + 1)
                else:
                    out += list((part.get("properties") or {}).items())
            return out
        return list((sch.get("properties") or {}).items())

    for ctx, d in docs.items():
        for path, item in (d.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb not in ("get", "post", "put", "patch", "delete") or not isinstance(op, dict):
                    continue
                r = op.get("responses") or {}
                ok = next((r[k] for k in ("200", "201", "202") if k in r), None)
                if not ok:
                    continue
                sch = ((ok.get("content") or {}).get("application/json") or {}).get("schema") or {}
                ref = sch.get("$ref") or ((sch.get("items") or {}).get("$ref")) or ""
                if not ref:
                    for part in sch.get("allOf", []):
                        for pk, pv in (part.get("properties") or {}).items():
                            if pk == "items":
                                ref = (pv.get("items") or {}).get("$ref", "")
                m = re.search(r"([\w-]+)\.yaml#/components/schemas/(\w+)|#/components/schemas/(\w+)",
                              ref or "")
                if not m:
                    continue
                pl = props(m.group(1) or ctx, m.group(2) or m.group(3))
                if pl:
                    OPSCHEMA[op["operationId"]] = {
                        "schema": m.group(2) or m.group(3),
                        "fields": [k for k, _ in pl][:14],
                        "enums": {k: v["enum"][:6] for k, v in pl
                                  if isinstance(v, dict) and "enum" in v},
                    }


# A login response and a tenant config are not screen content. Rendering them as a table of
# rows produced a sign-in page listing access tokens.
NOT_CONTENT = {"LoginResponse", "TenantConfig", "TenantAppStatus", "Session", "Problem",
               "RefreshResponse", "TokenResponse"}


def screen_fields(s: dict, prefer: str = "list") -> dict:
    """Which operation supplies a component's content.

    Not simply the screen's first API. A storefront calls `getTenantConfig` before
    `listProducts`, and the products are the content — so a collection component prefers a
    `list*` operation and a detail panel prefers a `get*` one.
    """
    cands = [a.get("operationId") for a in (s.get("apis") or [])
             if a.get("operationId") in OPSCHEMA
             and OPSCHEMA[a["operationId"]]["schema"] not in NOT_CONTENT]
    if not cands:
        return {}
    ordered = ([c for c in cands if c.startswith(prefer)]
               + [c for c in cands if c.startswith(("list", "get")) and not c.startswith(prefer)]
               + cands)
    return OPSCHEMA[ordered[0]]


def esc(x) -> str:
    return html.escape(str(x or ""))


def slug(x: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(x).lower()).strip("-")


def page(title: str, body: str, depth: int = 0) -> str:
    up = "../" * depth
    return (f"<!doctype html><meta charset=utf-8><title>{esc(title)}</title>"
            f"<style>{CSS}</style><div class=wrap>{body}"
            f"<p class=crumb style='margin-top:40px'><a href='{up}index.html'>index</a></p></div>")


SAMPLE = {
    "id": "01J8F…", "orderNumber": "DXB-24019", "status": "paid", "channel": "pos",
    "grossAmount": "AED 213.75", "refundedAmount": "AED 0.00", "lineCount": "3",
    "name": "Aquarium Entry", "code": "AQ-ADULT", "displayName": "J. Doe",
    "quantity": "2", "unitPrice": "AED 80.00", "total": "AED 160.00",
    "createdAt": "09:41", "updatedAt": "09:44", "recordedAt": "09:41",
    "venueId": "Aquarium", "mediaCode": "QR-4F2A…", "isValid": "yes",
    "principalDisplayName": "John Doe", "workstationId": "POS-01",
}


def cell(field: str) -> str:
    return SAMPLE.get(field, "—")


def draw_component(c: dict, sch: dict) -> str:
    """Populate from the schema the screen's own operation returns.

    A box labelled `dataTable` tells a reviewer nothing. `orderNumber · status · grossAmount`
    lets them say the channel column is missing, which is the comment worth having.
    """
    kind = c.get("kind", "box")
    cls, h = SHAPE.get(kind, ("box", 60))
    label = c.get("label") or kind
    fields = sch.get("fields") or []

    if kind == "dataTable" and fields:
        cols = fields[:6]
        head = "".join(f"<th>{esc(f)}</th>" for f in cols)
        rows = "".join("<tr>" + "".join(f"<td>{esc(cell(f))}</td>" for f in cols) + "</tr>"
                       for _ in range(3))
        return (f"<div class=el-full><table class=wf><thead><tr>{head}</tr></thead>"
                f"<tbody>{rows}</tbody></table>"
                f"<p class=src>{esc(sch.get('schema',''))}</p></div>")

    if kind in ("detailPanel", "consentBlock") and fields:
        rows = "".join(f"<div class=fld><span>{esc(f)}</span><i>{esc(cell(f))}</i></div>"
                       for f in fields[:8])
        return (f"<div class=el-full><div class=fields>{rows}</div>"
                f"<p class=src>{esc(sch.get('schema',''))}</p></div>")

    if kind == "cardList" and fields:
        one = "".join(f"<div class=fld><span>{esc(f)}</span><i>{esc(cell(f))}</i></div>"
                      for f in fields[:4])
        return ("<div class=el-full><div class=cards>"
                + "".join(f"<div class=cardbox>{one}</div>" for _ in range(3))
                + f"</div><p class=src>{esc(sch.get('schema',''))}</p></div>")

    if kind == "metricTile":
        names = [f for f in fields if any(k in f.lower() for k in
                 ("count", "total", "amount", "gross", "net", "sum"))][:4] or \
                ["gross", "transactions", "average", "refunds"]
        return "".join(f"<div class='el tile'><b>—</b><span>{esc(n)}</span></div>" for n in names)

    if kind in ("selectField", "multiSelect"):
        opts = next(iter((sch.get("enums") or {}).values()), None)
        val = " / ".join(opts[:3]) if opts else "…"
        return f"<div class='el field'>{esc(label)}<i>{esc(val)}</i></div>"

    if kind == "cartPanel":
        lines = "".join("<div class=fld><span>Aquarium Entry · Adult ×2</span><i>AED 160.00</i></div>"
                        "<div class=fld><span>Audio Guide · ×1</span><i>AED 15.00</i></div>"
                        "<div class=fld><span>Member discount</span><i>−AED 11.25</i></div>"
                        "<div class='fld tot'><span>Total</span><i>AED 213.75</i></div>" for _ in [0])
        return f"<div class=el-full><div class=fields>{lines}</div></div>"

    if kind == "saleBoard":
        tiles = ["All", "Exhibitions", "Experiences", "Guided tours", "Packages", "Food",
                 "Rentals", "Add-ons"]
        return ("<div class=el-full><div class=board>"
                + "".join(f"<div class=tilebox>{esc(t)}</div>" for t in tiles) + "</div></div>")

    if kind == "paymentTerminal":
        return ("<div class=el-full><div class=fields>"
                "<div class=fld><span>Total payable</span><i>AED 213.75</i></div>"
                "<div class=fld><span>Terminal</span><i>awaitingCard</i></div>"
                "<div class=fld><span>Provider</span><i>networkInternational</i></div>"
                "</div><p class=src>Payment · states include <b>unknown</b></p></div>")

    if kind in ("chart", "seatMap", "scanTarget", "livePreview", "timeline"):
        return f"<div class='el {cls}' style='min-height:{h}px'>{esc(label)}</div>"

    sm = " sm" if cls.startswith("btn") or cls in ("toggle", "tag") else ""
    return f"<div class='el {cls}{sm}' style='min-height:{h}px'>{esc(label)}</div>"


COLLECTION = {"dataTable", "cardList"}


def draw_screen(s: dict, platform: dict) -> str:
    layout = s.get("layout") or {}
    regions = {r["name"]: r for r in (layout.get("regions") or [])}
    order = [r for r in REGION_ORDER if r in regions] + \
            [r for r in regions if r not in REGION_ORDER]
    rows = []
    for name in order:
        comps = regions[name].get("components") or []
        inner = "".join(
            draw_component(c, screen_fields(s, "list" if c.get("kind") in COLLECTION else "get"))
            for c in comps) or \
                "<div class='el' style='min-height:44px'>—</div>"
        tips = "".join(f"<p class=tip>{esc(c['notes'])}</p>"
                       for c in comps if c.get("notes"))
        rows.append(f"<div class=rg><div class=rg-l>{esc(name)}</div>"
                    f"<div class=row>{inner}</div>{tips}</div>")
    tmpl = layout.get("template", "detail")
    return (f"<div class=frame><div class=bar><span>{esc(s['id'])} · {esc(s['name'])}</span>"
            f"<span>{esc(platform['shortName'])} · {esc(tmpl)}</span></div>"
            f"<div class=body>{''.join(rows)}</div></div>")


def screen_page(s: dict, platform: dict, depth: int) -> str:
    st = s.get("states") or {}
    rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in st.items())
    apis = "".join(f"<span class=pill>{esc(a.get('operationId'))}</span>"
                   for a in (s.get("apis") or []))
    nav = s.get("navigation") or {}
    links = "".join(f"<span class=pill>{esc(x)}</span>" for x in (nav.get("exitTo") or []))
    wf = (s.get("wireframe") or {}).get("status", "notStarted")
    body = [
        f"<p class=crumb><a href='{'../'*depth}index.html'>index</a> · "
        f"<a href='{'../'*(depth-1)}{slug(platform['code'])}.html'>{esc(platform['shortName'])}</a></p>",
        f"<h1>{esc(s['id'])} — {esc(s['name'])}</h1>",
        f"<p class=sub>{esc(s.get('purpose'))}</p>",
        "<p class=note><b>Structure only.</b> Drawn from the screen definition — template, "
        "regions and component kinds. Nothing here is a design decision.</p>",
        draw_screen(s, platform),
        "<h2>States</h2>",
        f"<table class=st>{rows}</table>" if rows else "<p class=sub>None declared.</p>",
    ]
    if apis:
        body += ["<h2>Operations</h2>", f"<p>{apis}</p>"]
    if links:
        body += ["<h2>Goes to</h2>", f"<p>{links}</p>"]
    body += [f"<h2>Design status</h2><p><span class='pill{' off' if wf=='approved' else ''}'>"
             f"{esc(wf)}</span> · module {esc(s.get('module'))} · wave {esc(s.get('wave'))}</p>"]
    if s.get("notes"):
        body += [f"<p class=note>{esc(s['notes'])}</p>"]
    return page(f"{s['id']} {s['name']}", "".join(body), depth)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "screens").mkdir(exist_ok=True)
    load_schemas()
    platforms = {}
    screens = {}
    for f in sorted(SCREENS.glob("P*.yaml")):
        d = yaml.safe_load(f.read_text())
        p = d["platform"]
        platforms[p["code"]] = p
        screens[p["code"]] = d["screens"]

    n = 0
    for code, ss in screens.items():
        p = platforms[code]
        cards = []
        for s in ss:
            fn = OUT / "screens" / f"{slug(s['id'])}.html"
            fn.write_text(screen_page(s, p, 2))
            n += 1
            wf = (s.get("wireframe") or {}).get("status", "notStarted")
            cards.append(
                f"<a class=card href='screens/{slug(s['id'])}.html'><h3>{esc(s['id'])} "
                f"{esc(s['name'])}</h3><div class=m>{esc(s.get('module'))} · wave "
                f"{esc(s.get('wave'))} · {esc(wf)}</div></a>")
        body = (f"<p class=crumb><a href='index.html'>index</a></p>"
                f"<h1>{esc(p['name'])}</h1>"
                f"<p class=sub>{esc(p['audience'])} on {esc(p['formFactor'])}, app "
                f"<code>{esc(p['app'])}</code>. {len(ss)} screens."
                + (" <b>Offline-capable.</b>" if p.get("offlineCapable") else "") + "</p>"
                f"<div class=grid>{''.join(cards)}</div>")
        (OUT / f"{slug(code)}.html").write_text(page(p["name"], body, 0))

    # flows
    flow_cards = []
    for f in sorted(FLOWS.glob("F*.yaml")):
        d = yaml.safe_load(f.read_text())
        steps = []
        for i, st in enumerate(d.get("steps") or [], 1):
            sid = st.get("screen") or ""
            link = (f"<a href='screens/{slug(sid)}.html'>{esc(sid)}</a>" if sid else "—")
            steps.append(f"<div class=flowstep><div class=n>{i}</div><div>"
                         f"<b>{esc(st.get('action') or st.get('name'))}</b><br>"
                         f"<span class=m>{link}</span></div></div>")
        branches = "".join(f"<p class=br>↳ {esc(b.get('when'))} → {esc(b.get('then'))}</p>"
                           for b in (d.get("branches") or []))
        body = (f"<p class=crumb><a href='index.html'>index</a></p>"
                f"<h1>{esc(d.get('name'))}</h1>"
                f"<p class=sub>{esc(d.get('description') or '')}</p>"
                "<p class=note><b>The unhappy paths are the point.</b> A flow that only shows "
                "the happy path is a diagram; the branches below are where the screens get "
                "decided.</p>"
                f"{''.join(steps)}<h2>Branches</h2>{branches or '<p class=sub>None.</p>'}")
        (OUT / f"flow-{slug(d.get('id', f.stem))}.html").write_text(page(d.get("name", f.stem), body, 0))
        flow_cards.append(f"<a class=card href='flow-{slug(d.get('id', f.stem))}.html'>"
                          f"<h3>{esc(d.get('id'))} {esc(d.get('name'))}</h3>"
                          f"<div class=m>{len(d.get('steps') or [])} steps · "
                          f"{len(d.get('branches') or [])} branches</div></a>")

    pcards = "".join(
        f"<a class=card href='{slug(c)}.html'><h3>{esc(p['shortName'])}</h3>"
        f"<div class=m>{esc(p['name'].split('— ')[-1])} · {len(screens[c])} screens · "
        f"{esc(p['formFactor'])}</div></a>" for c, p in sorted(platforms.items()))
    approved = sum(1 for ss in screens.values() for s in ss
                   if (s.get("wireframe") or {}).get("status") == "approved")
    idx = (f"<h1>TICVAI — structural wireframes</h1>"
           f"<p class=sub>{n} screens across {len(platforms)} platforms, drawn from the screen "
           f"definitions. {approved} have an approved design; the rest are structure only.</p>"
           "<p class=note><b>Deliberately ugly.</b> Grey boxes and labels, no colour and no "
           "type choices. A wireframe that looks designed invites comment on the design; one "
           "that looks like a wireframe invites comment on whether the right things are on the "
           "screen — which is the only question worth asking before a designer starts.<br><br>"
           "Everything drawn comes from the definition and nothing else. Where a screen "
           "declares an offline state it is listed, because those are the most important lines "
           "in the POS and scanner definitions and a static mockup hides them.</p>"
           f"<h2>Platforms</h2><div class=grid>{pcards}</div>"
           f"<h2>Flows</h2><div class=grid>{''.join(flow_cards)}</div>")
    (OUT / "index.html").write_text(page("TICVAI wireframes", idx, 0))
    print(f"{n} screen pages, {len(platforms)} platforms, {len(flow_cards)} flows -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
