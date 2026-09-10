#!/usr/bin/env python3
"""Derive wireframes/<platform>.dc.html from screens/P*.yaml.

`wireframes/BRIEF.md` says it plainly: **"Screen definitions — this is the specification."** The
boards are a rendering of that, and until 20 August they were hand-written — which is why 115
screens across seven platforms had no board at all, and three platforms had none whatsoever.

**A board is generated, not maintained.** Regenerating one is the whole of "delete the old board
and draw a new one", because nothing points at a board except the screen that owns it, and
`check-wireframes` refuses an anchor that does not resolve in either direction.

Follows BRIEF.md, and the six rules that matter more than the styling:

  1. **Every declared state appears on the frame.** The offline state is the most important line
     on a scanner or POS screen and a static mockup hides it.
  2. **Component `notes` are rendered.** They carry the reasoning; a board without them loses why.
  3. **Nothing is invented.** No operations declared renders `OPERATIONS · none declared`. That
     gap is real and should be visible.
  4. **Ugly on purpose.** A wireframe that looks designed invites comment on the design; one that
     looks like a wireframe invites comment on whether the right things are on the screen.
  5. Cross-platform reaches are drawn.
  6. Back-link on every board.

**Theme is by audience, not by platform** — the kiosk is venue hardware that a guest uses, so it
is white-labelled like the website rather than TICVAI-branded like the POS beside it.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
WIRE = ROOT / "wireframes"

# Theme by audience. Employee mobile is dark ground; everything else is light with the
# TICVAI gradient, and guest surfaces carry the venue navy.
DARK = {"P06"}
GUEST = {"P01", "P02", "P05"}

CSS = """
/* **The Claude Design system, applied to the generated boards on 24 August.**
   Three client packs render at 1280x700 in this system and 385 screens rendered as
   dashed-box wireframes — and **a client reviewing both reads the difference as *those screens
   are not done*.** The information is identical either way; the fidelity is what was being
   judged.

   Tokens are the packs': #0B1324 rail, #0D6EFD primary, #00B8FF accent, Manrope for UI,
   IBM Plex Mono for figures and codes. */
:root{--ink:#0B1324;--mut:#5A6577;--dim:#9AA5B6;--line:#E8ECF3;--edge:#E3E8F0;
--brand:#0D6EFD;--accent:#00B8FF;--rail:#0B1324;--paper:#FFF;--wash:#F7F9FC;
--ok:#0E9F6E;--okbg:#E8F6F0;--okline:#BFE3D2;--warn:#8A6D00;--warnbg:#FFF7E6;
--bad:#A81E1E;--badbg:#FDECEC}
*{box-sizing:border-box}
body{margin:0;background:#F2F5F9;color:var(--ink);
font-family:Manrope,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;line-height:1.55}
a{color:inherit}
.wrap{max-width:1420px;margin:0 auto;padding:22px 34px 90px}
.home{font-size:11.5px;color:var(--mut);text-decoration:none;letter-spacing:.02em}
.head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
margin:14px 0 6px;padding-bottom:16px;border-bottom:2px solid var(--ink)}
.mark{font-size:13px;font-weight:800;letter-spacing:.16em;
background:linear-gradient(90deg,var(--brand),var(--accent));-webkit-background-clip:text;
background-clip:text;color:transparent}
h1{font-size:19px;font-weight:800;letter-spacing:-.015em;margin:0}
.meta{font-size:11px;color:var(--mut);font-family:'IBM Plex Mono',ui-monospace,monospace;line-height:1.7}
.lede{font-size:12.5px;color:var(--mut);max-width:82ch;margin:16px 0 0;line-height:1.65}
.grp{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:11px;font-weight:600;
letter-spacing:.14em;color:var(--dim);text-transform:uppercase;margin:52px 0 18px;
padding-bottom:9px;border-bottom:1px solid var(--line)}
.stack{display:flex;flex-direction:column;gap:52px}
.scr{display:flex;flex-direction:column;gap:13px;scroll-margin-top:24px}
.hdr{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
.code{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#8494A8}
.ttl{font-size:16.5px;font-weight:800;letter-spacing:-.015em}
.pur{font-size:12px;color:#6B7280;margin-top:3px;max-width:96ch}
.pill{font-size:9px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
padding:2px 7px;border-radius:5px;background:#EEF3FA;color:#4A5A70}
.pill.named{background:var(--warnbg);color:var(--warn)}
.pill.off{background:var(--okbg);color:var(--ok)}

/* the frame — 1280x700, the packs' dimension */
.frame{width:1280px;height:700px;display:flex;background:var(--wash);border:1px solid var(--edge);
border-radius:14px;overflow:hidden;box-shadow:0 16px 38px rgba(12,35,64,.09)}
.rail{flex:none;width:180px;background:var(--rail);display:flex;flex-direction:column;position:relative}
.rail::before{content:'';position:absolute;inset:0;
background:radial-gradient(300px 200px at 0% 4%,rgba(0,184,255,.20),transparent 70%);pointer-events:none}
.brand{position:relative;padding:15px 14px 13px;border-bottom:1px solid rgba(255,255,255,.08)}
.brand b{display:block;font-size:14px;font-weight:800;letter-spacing:.1em;
background:linear-gradient(90deg,#4DA3FF,var(--accent));-webkit-background-clip:text;
background-clip:text;color:transparent}
.brand span{display:block;font-size:9.5px;color:#7FA3C9;margin-top:5px}
.nav{position:relative;display:flex;flex-direction:column;gap:2px;padding:11px 9px}
.nav i{display:block;padding:8px 10px;border-radius:9px;font-size:11.5px;font-style:normal;color:#8FA8C4}
.nav i.on{background:linear-gradient(90deg,rgba(13,110,253,.30),rgba(0,184,255,.10));
color:#fff;font-weight:700}
.body{flex:1;display:flex;flex-direction:column;min-width:0}
.top{flex:none;height:54px;display:flex;align-items:center;gap:12px;padding:0 18px;
background:var(--paper);border-bottom:1px solid var(--line)}
.top h2{font-size:13.5px;font-weight:800;letter-spacing:-.01em;margin:0}
.top small{display:block;font-size:10px;color:var(--dim);font-weight:500}
.acts{margin-left:auto;display:flex;gap:6px}
.chip{height:32px;display:flex;align-items:center;gap:6px;padding:0 11px;border:1px solid var(--edge);
border-radius:8px;font-size:11px;font-weight:700;color:var(--mut);background:var(--paper)}
.chip.live{background:var(--okbg);border-color:var(--okline);color:var(--ok)}
.chip.live::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--ok)}
.chip.cta{background:var(--brand);border-color:var(--brand);color:#fff}
.canvas{flex:1;display:flex;flex-direction:column;gap:12px;padding:14px 16px;min-height:0;overflow:hidden}
.kpis{flex:none;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.kpi{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:11px 13px;
display:flex;flex-direction:column;gap:4px}
.kpi b{font-size:9.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--dim)}
.kpi span{font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;letter-spacing:-.02em}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px;
display:flex;flex-direction:column;gap:8px;min-height:0}
.panel > b{font-size:11px;font-weight:800;letter-spacing:-.005em}
.panel .why{font-size:10px;color:#7C8899;font-style:italic;line-height:1.5}
.kind{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--dim);
letter-spacing:.06em;text-transform:uppercase}
.rows{display:flex;flex-direction:column;gap:6px}
.row{display:grid;grid-template-columns:1.6fr 1fr 1fr .7fr;gap:10px;align-items:center;
padding:7px 0;border-top:1px solid #F0F3F8}
.row:first-child{border-top:0;font-size:9.5px;font-weight:700;letter-spacing:.06em;
text-transform:uppercase;color:var(--dim)}
.bar{height:7px;border-radius:4px;background:#EDF1F7}
.bar i{display:block;height:100%;border-radius:4px;
background:linear-gradient(90deg,var(--brand),var(--accent))}
.side{flex:none;width:250px;display:flex;flex-direction:column;gap:10px}
.two{flex:1;display:flex;gap:12px;min-height:0}
.grow{flex:1;min-width:0}
.strip{flex:none;height:26px;display:flex;align-items:center;gap:8px;padding:0 18px;
background:var(--warnbg);color:var(--warn);font-size:10px;font-weight:700;
letter-spacing:.05em;text-transform:uppercase;border-bottom:1px solid #F0E0B8}
.dark .frame{background:#0A1524}
.dark .top{background:#0E2A4C;border-color:#1E3A5F;color:#E6F0FA}
.dark .top small{color:#7FA3C9}
.dark .canvas{background:#0A1524}
.dark .kpi,.dark .panel{background:#0E2A4C;border-color:#1E3A5F;color:#E6F0FA}
.dark .row{border-color:#193353}
.dark .chip{background:#0E2A4C;border-color:#1E3A5F;color:#9FC0E0}

.drawnb{margin-left:6px;font:600 10px/1.6 'IBM Plex Mono',monospace;color:#0F766E;background:#ECFDF5;border:1px solid #A7F3D0;padding:1px 7px;border-radius:999px}
.frame.drawn{padding:0;background:#FFF}
.wsb{margin-left:8px;font:600 10px/1.6 'IBM Plex Mono',monospace;color:#5B21B6;background:#F5F3FF;border:1px solid #DDD6FE;padding:1px 7px;border-radius:999px;white-space:nowrap}
.wsbar{position:sticky;top:0;z-index:20;display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 18px;padding:10px 14px;background:#FFF;border:1px solid #E5E7EB;border-radius:10px;font:600 12px/1.4 'IBM Plex Mono',monospace}
.wsbar label{color:#6B7280;font-weight:600}
.wsbar select{font:600 12px 'IBM Plex Mono',monospace;padding:5px 8px;border:1px solid #D1D5DB;border-radius:7px;background:#FFF;color:#111827;max-width:min(520px,60vw)}
.wsbar .n{color:#6B7280;font-weight:400}
.scr[hidden],.grp[hidden],.stack[hidden]{display:none!important}
.foot a{color:#2563EB;text-decoration:none;border-bottom:1px solid rgba(37,99,235,.3)}
.foot a:hover{border-bottom-color:#2563EB}
.foot .car{font-family:var(--mono,monospace);font-size:9.5px;color:#0F766E;background:#ECFDF5;padding:1px 5px;border-radius:4px}
.foot .dis{font-family:var(--mono,monospace);font-size:9.5px;color:#B45309}
.foot .away{font-size:9px;color:#9AA5B6}
.foot .hand{font-size:9.5px;color:#7C3AED;background:#F5F3FF;padding:1px 5px;border-radius:4px}
.foot .mac{margin-top:3px;font-size:10px;color:#4A5566;line-height:1.7}
.foot .ov{margin-top:3px;font-size:10px;color:#4A5566}
.foot{font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:10px;line-height:1.85;color:#7C8899}
.foot b{color:#4A5566;font-weight:600}
.foot .warn{color:var(--warn)}
.bottom{margin-top:64px;padding-top:16px;border-top:1px solid var(--line);
display:flex;justify-content:space-between;font-size:10.5px;color:var(--dim)}
"""


def esc(x) -> str:
    return html.escape(str(x or ""))


KPI_BY_MODULE = {
    "Sell": [("Today", "AED 48,210"), ("Orders", "312"), ("Avg basket", "AED 154"), ("Refunds", "4")],
    "Orders & Money": [("Takings", "AED 62,480"), ("Settled", "18"), ("Variance", "AED 40"), ("Open", "3")],
    "Stock & Supply": [("On hand", "AED 214k"), ("Below par", "17"), ("Expiring", "9"), ("Variance", "1.8%")],
    "Kitchen": [("On the rail", "14"), ("Oldest", "6m 20s"), ("Breaching", "2"), ("86'd", "3")],
    "Analytics": [("Revenue MTD", "AED 4.86M"), ("vs budget", "+3.1%"), ("Margin", "38.4%"), ("Alerts", "6")],
}
DEFAULT_KPIS = [("Total", "1,248"), ("Active", "978"), ("Attention", "142"), ("Offline", "12")]

# **A guest storefront was rendering a staff dashboard.** `WEB-001 Home / Landing` showed
# *TOTAL 1,248 · ACTIVE 978 · ATTENTION 142 · OFFLINE 12* above a nav reading Dashboard, Settings,
# Reports, People — **none of which a guest ever sees**, and four counts a guest has no business
# knowing.
#
# The generator had one chrome and applied it to 481 screens. **A wireframe that shows the wrong
# furniture is worse than one that shows none**: a reviewer corrects the numbers instead of
# questioning the screen.
AUDIENCE_CHROME = {
    "guest": {
        "nav": ["What's on", "My tickets", "Food & drink", "Map", "Help"],
        "kpis": None,          # a guest is shown their own things, never venue counts
        "brand": "the tenant's brand, not TICVAI",
        "actions": [("Sign in", ""), ("Basket", "cta")],
    },
    "partner": {
        "nav": ["Allocations", "Bookings", "Statements", "Support"],
        "kpis": [("Allocation", "2,400"), ("Sold", "1,860"), ("Credit", "AED 84k"),
                 ("Due", "AED 12k")],
        "brand": "TICVAI Partner",
        "actions": [("This account", ""), ("New booking", "cta")],
    },
    "staff": {
        "nav": None,           # falls through to the module nav below
        "kpis": None,
        "brand": "TICVAI",
        "actions": [("This venue &#9662;", ""), ("Live", "live"), ("Primary action", "cta")],
    },
    # **The package declares five audiences and this held three.** The lookup fell through to
    # `staff` silently, so `P09 TICVAI Web` — the console that provisions cells and ships releases
    # — drew "This venue" and a venue nav, and `P11 Accreditation Web`, a public application form,
    # drew "Live": furniture for an operator on shift. **45 screens showing chrome nobody chose
    # for them**, and the silent `.get(aud, staff)` is why it survived a rebuild.
    "platformAdmin": {
        "nav": ["Tenants", "Cells", "Releases", "Health", "Audit"],
        "kpis": [("Tenants", "184"), ("Cells", "3"), ("Incidents", "2"), ("Releases", "11")],
        "brand": "TICVAI",
        "actions": [("All tenants &#9662;", ""), ("Deploy", "cta")],
    },
    "public": {
        "nav": ["Apply", "My application", "Help"],
        "kpis": None,          # an applicant is shown their own application, never a venue count
        "brand": "the tenant's brand",
        "actions": [("Start application", "cta")],
    },
}

# **An audience with no chrome must report itself, not be absorbed.** The fallback below is a
# safety net and not a decision — a platform whose audience is missing here draws staff furniture,
# which is exactly the defect this comment exists to stop recurring.
UNCHROMED: set = set()

# **The client packs this package knows about.** A board whose name starts with none of these and
# is not `P## ` generated is a file nobody can account for — reported, never deleted, because this
# tool did not write it and has no business removing somebody else's work.
PACK_PREFIXES = ("FnB", "Retail", "POS", "Inventory", "Marketing", "Seat", "Guest Mobile",
                 "Kiosk", "Dashboards")
WRITTEN: list = []
COVERED: set = set()


def kpis(module: str, chrome: dict | None = None) -> str:
    """The strip, or nothing at all.

    **A guest is shown their own things and never a venue count.** Returning an empty string is the
    correct answer for a storefront — the alternative was four numbers a guest cannot act on
    sitting above the thing they came to buy.
    """
    if chrome is not None:
        if chrome.get("audience") == "guest":
            return ""
        if chrome.get("kpis"):
            return '<div class="kpis">' + "".join(
                f'<div class="kpi"><b>{esc(a)}</b><span>{esc(b)}</span></div>'
                for a, b in chrome["kpis"]) + "</div>"
    rows = KPI_BY_MODULE.get(module or "", DEFAULT_KPIS)
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in rows) + "</div>"


def panel(kind: str, label: str, note: str, tall: bool = False) -> str:
    """One component rendered as the thing it is, not as a dashed box.

    **The packs render a real dashboard and the generated boards rendered dashed rectangles**, and
    a client reviewing both reads the difference as *those screens are not done*. The information
    was identical; the fidelity was what was being judged.

    The note still shows. **It carries the reasoning and losing it to make the board prettier would
    be the wrong trade** — a board that looks finished and says nothing about why is a board nobody
    argues with.
    """
    body = ""
    if kind in ("dataTable", "cardList", "treeNav"):
        body = ('<div class="rows">'
                '<div class="row"><span>Name</span><span>Status</span><span>Value</span><span></span></div>'
                + "".join('<div class="row"><span>&nbsp;</span><span>&nbsp;</span>'
                          '<span>&nbsp;</span><span>&nbsp;</span></div>' for _ in range(4))
                + "</div>")
    elif kind in ("chart", "metricTile"):
        body = ('<div class="rows">' + "".join(
            f'<div class="bar"><i style="width:{w}%"></i></div>' for w in (78, 54, 92, 36, 61))
            + "</div>")
    elif kind in ("searchField", "textField", "multiSelect"):
        body = '<div class="chip">' + esc(label or "Search") + "</div>"
    elif kind in ("primaryButton", "secondaryButton"):
        body = f'<div class="chip{" cta" if kind == "primaryButton" else ""}">{esc(label or kind)}</div>'
    elif kind == "banner":
        body = '<div class="strip" style="height:auto;padding:6px 10px;border:0">notice</div>'
    else:
        body = '<div class="rows"><div class="bar"><i style="width:64%"></i></div></div>'
    why = f'<span class="why">{clip(esc(note), 170)}</span>' if note else ""
    head = f'<b>{esc(label)}</b>' if label else f'<span class="kind">{esc(kind)}</span>'
    return f'<div class="panel">{head}{body}{why}</div>'


# **Frames drawn by Claude Design, one file per screen id.** Built on first use rather than at
# import, because `derive-pack-boards` imported this module without calling `main()` and any map
# filled there arrived empty — which is how every same-platform exit once rendered as a link to
# another board.
DRAWN: dict = {}


def drawn_frame(sid: str) -> str:
    """The frame a designer drew for this screen, or an empty string."""
    if not DRAWN:
        DRAWN["_"] = ""                    # marks the map built even when the folder is empty
        d = ROOT / "wireframes" / "frames"
        if d.exists():
            for f in d.glob("*.html"):
                DRAWN[f.stem.upper()] = f.read_text(encoding="utf-8", errors="replace")
    return DRAWN.get(sid.upper(), "")


def render_screen(s: dict, dark: bool, offline_platform: bool, plat: dict) -> str:
    regions = {r.get("name"): r for r in ((s.get("layout") or {}).get("regions") or [])}
    states = s.get("states") or {}
    comps = (regions.get("contentBody") or {}).get("components") or []

    aud = plat.get("audience") or "staff"
    if aud not in AUDIENCE_CHROME:
        UNCHROMED.add(aud)
    chrome = dict(AUDIENCE_CHROME.get(aud, AUDIENCE_CHROME["staff"]))
    chrome["audience"] = aud
    chrome["brandLabel"] = "TICVAI Partner" if aud == "partner" else (
        plat.get("shortName", "TICVAI").split()[0] if aud == "guest" else "TICVAI")
    acts = "".join(
        f'<div class="chip{(" " + k) if k else ""}">{label}</div>'
        for label, k in chrome["actions"])
    nav_items = chrome["nav"] or ["Dashboard", esc(s.get("module") or "Section"), "Settings",
                                  "Reports", "People"]
    nav_items = [esc(x) for x in nav_items]
    rail = ('<aside class="rail"><div class="brand">'
            f'<b>{esc(chrome.get("brandLabel") or "TICVAI")}</b>'
            f'<span>{esc(s.get("module") or plat.get("shortName"))}</span></div>'
            '<nav class="nav">'
            + "".join(f'<i class="{"on" if n == 1 else ""}">{t}</i>'
                      for n, t in enumerate(nav_items))
            + "</nav></aside>")

    # **A board can only render what the screen declares, and 212 screens declare one component.**
    # The fidelity ceiling is the screen model, not the styling — so where a screen is thin the
    # frame shows the shape its template implies and says so, rather than rendering one lonely
    # box in a 1280px dashboard and letting a reviewer conclude the screen is empty.
    #
    # **The inferred panels are labelled `implied by template`.** A reviewer must be able to tell
    # what the screen actually says from what the board filled in, or the board becomes a source
    # of requirements nobody wrote.
    TEMPLATE_SHAPE = {
        "list": ["searchField", "dataTable"],
        "dashboard": ["chart", "dataTable"],
        "detail": ["detailPanel", "dataTable"],
        "form": ["textField", "primaryButton"],
        "board": ["cardList", "metricTile"],
        "wizard": ["textField", "primaryButton"],
        "calendar": ["timeline", "datePicker"],
    }
    tmpl = (s.get("layout") or {}).get("template", "list")
    rendered = [panel(c.get("kind", "panel"), c.get("label"), c.get("notes")) for c in comps[:3]]
    if len(rendered) < 2:
        for k in TEMPLATE_SHAPE.get(tmpl, ["dataTable"]):
            if len(rendered) >= 2:
                break
            if any(c.get("kind") == k for c in comps):
                continue
            rendered.append(panel(k, None, "Implied by the {} template — not declared on the "
                                           "screen.".format(tmpl)))
    main = "".join(rendered) or panel("panel", None, None)
    side = "".join(panel(c.get("kind", "panel"), c.get("label"), c.get("notes"))
                   for c in comps[3:5])
    side_html = f'<div class="side">{side}</div>' if side else ""

    off = "offline" in states
    strip = '<div class="strip">offline capable · works from the local journal</div>' if off else ""

    ops = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
    ops_line = " · ".join(ops[:4]) + (f" +{len(ops) - 4}" if len(ops) > 4 else "")         if ops else "none declared"
    state_names = list(states)
    exits = ((s.get("navigation") or {}).get("exitTo") or [])
    entry = "entry point · " if (s.get("navigation") or {}).get("isEntryPoint") else ""

    prov = str(s.get("provenance", ""))
    pills = []
    if "named only" in prov:
        pills.append('<span class="pill named">named only</span>')
    elif "specified" in prov:
        pills.append('<span class="pill">client board</span>')
    if off:
        pills.append('<span class="pill off">offline</span>')
    frames = s.get("boardFrames") or []
    if frames:
        pills.append(f'<span class="pill">{esc(", ".join(frames))}</span>')

    ent = s.get("entryState") or {}
    params = ", ".join(f'{p["name"]}&larr;{p["from"]}' for p in (ent.get("params") or [])[:3])

    # **Every exit is a link, and every one it has a transition for says how you make the move.**
    # This printed `exits[:5]` as text: a board that names a destination and cannot go there is a
    # diagram, not a wireframe, and the first five of thirty-four is not a navigation model.
    by_to = {}
    for t in ((s.get("navigation") or {}).get("transitions") or []):
        by_to.setdefault(str(t.get("to", "")).partition("#")[0], t)
    goes = []
    for e in exits:
        t = by_to.get(e) or {}
        bits = []
        if t.get("trigger"):
            bits.append(f'<i>{esc(clip(t["trigger"], 44))}</i>')
        if t.get("carries"):
            bits.append(f'<span class="car">{esc(" · ".join(t["carries"][:4]))}</span>')
        if t.get("crossesDevice"):
            bits.append('<span class="hand">handover</span>')
        tail = (" &mdash; " + " ".join(bits)) if bits else ""
        own = e in (plat.get("_ids") or ())
        bo = board_of()
        href = (f"#{e.lower()}" if own
                else (bo[e].replace(" ", "%20") + f"#{e.lower()}") if e in bo
                else f"#{e.lower()}")
        away = "" if own else '<span class="away">other board</span> '
        goes.append(f'<a href="{esc(href)}">{esc(e)}</a> {away}{tail}')
    goes_html = "<br>".join(goes) if goes else "nothing declared"

    # The step machine, where one is declared. `states` is what the screen renders; this is what
    # it is in the middle of, and no rendering state can say "the terminal charged and never
    # answered".
    mach = s.get("machine") or {}
    mach_html = ""
    if mach:
        edges = " &nbsp;".join(
            f'{esc(t.get("from"))}&rarr;<b>{esc(t.get("to"))}</b> <i>{esc(clip(t.get("on"), 26))}</i>'
            for t in (mach.get("transitions") or []))
        mach_html = (f'<div><b>MACHINE</b> &middot; <code>{esc(mach.get("key"))}</code> from '
                     f'<b>{esc(mach.get("initial"))}</b> &middot; '
                     f'{esc(" · ".join(mach.get("states") or {}))}<div class="mac">{edges}</div></div>')

    # What opens, and what closing it does. 199 overlays said the first and none said the second.
    ovs = []
    for o in (s.get("overlays") or []):
        c, d = o.get("confirm") or {}, o.get("dismiss") or {}
        parts = []
        if c:
            to = f' &rarr; <a href="#{esc(str(c.get("to","")).partition("#")[0].lower())}">{esc(c["to"])}</a>' if c.get("to") else ""
            parts.append(f'<b>{esc(c.get("label") or "confirm")}</b>{to}'
                         + (f' <span class="car">{esc(" · ".join(c.get("carries") or []))}</span>'
                            if c.get("carries") else ""))
        if d:
            parts.append(f'{esc(d.get("label") or "dismiss")}'
                         + (f' <span class="dis">discards {esc(" · ".join(d.get("discards") or []))}</span>'
                            if d.get("discards") else ""))
        ovs.append(f'<div class="ov"><b>{esc(o.get("component"))}</b> {esc(o.get("id"))} '
                   f'&middot; <i>{esc(o.get("trigger"))}</i>'
                   + (" &middot; " + " &middot; ".join(parts) if parts else "") + "</div>")
    ov_html = f'<div><b>OVERLAYS</b>{"".join(ovs)}</div>' if ovs else ""

    # **A drawn frame stands in for the generated one, and the card says which it is.**
    # A reviewer looking at ninety cards must be able to tell which have been through a
    # designer, or the board flatters itself.
    _drawn = drawn_frame(s["id"])

    # **Where the workshop put this screen, on the card rather than on a second board.**
    _ws = ws_of(s)
    ws_attr = f' data-ws="{esc(_ws[0])}"' if _ws else ""
    ws_pill = (f'<span class="wsb" title="{esc(_ws[1])}">{esc(_ws[0])} &middot; {esc(_ws[1])}</span>'
               if _ws else "")
    if _drawn:
        ws_pill += '<span class="drawnb" title="A designer drew this frame">drawn</span>'


    # **The generated frame, unless a designer drew one.** Built here rather than inside the
    # template because a nested f-string will not parse on 3.9 — and because a reader can now see
    # what the substitution actually swaps.
    generated_frame = f"""{rail}
          <div class="body">
            <div class="top">
              <div><h2>{clip(esc(s['name']), 44)}</h2>
                <small>{esc(plat.get('shortName'))} &middot; wave {esc(s.get('wave'))} &middot; {esc(s.get('density'))}</small></div>
              <div class="acts">{acts}</div>
            </div>
            {strip}
            <div class="canvas">
              {kpis(s.get('module'), chrome)}
              <div class="two"><div class="grow">{main}</div>{side_html}</div>
            </div>
          </div>"""
    frame_body = _drawn if _drawn else generated_frame

    return f"""
      <div id="{s['id'].lower()}" class="scr"{ws_attr}>
        <div>
          <div class="hdr"><span class="code">{esc(s['id'])}</span>
            <span class="ttl">{esc(s['name'])}</span>{''.join(pills)}{ws_pill}</div>
          <div class="pur">{clip(esc(s.get('purpose')), 150)}</div>
        </div>
        <div class="frame{' dark' if dark else ''}{' drawn' if _drawn else ''}">
          {frame_body}
        </div>
        <div class="foot">
          <div><b>OPERATIONS</b> &middot; {esc(ops_line)}</div>
          <div><b>STATES</b> &middot; <span class="{'warn' if off else ''}">{esc(' · '.join(state_names[:7]))}</span></div>
          {f'<div><b>ARRIVES WITH</b> &middot; {params}</div>' if params else ''}
          <div><b>GOES TO</b> &middot; {entry}{goes_html}</div>
          {mach_html}
          {ov_html}
        </div>
      </div>"""


def build(path: Path) -> tuple[str, int]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    # Screens drawn in a client pack keep their anchor; the generated board still renders them so
    # a reviewer sees the whole platform, and the card links out to the pack.
    designed_count = sum(1 for s in doc["screens"]
                         if str((s.get("wireframe") or {}).get("board", ""))
                         .startswith(DESIGNED_PREFIXES))
    p = doc["platform"]
    # **Set here, not in main().** `build` re-reads the file, so anything main() attached to its
    # own copy of the doc never reached the renderer — every same-platform exit rendered as a
    # link to another board.
    p["_ids"] = {x["id"] for x in doc["screens"]}
    code = p["code"]
    dark = code in DARK
    offline = bool(p.get("offlineCapable"))
    screens = doc["screens"]

    # Ten to a row group, matching the client's own reference boards; grouped by module so the
    # heading names what the group is for rather than counting to ten.
    groups: dict = {}
    for s in screens:
        groups.setdefault(s.get("module") or "Screens", []).append(s)

    parts = []
    for i, (mod, items) in enumerate(groups.items(), 1):
        parts.append(f'<div class="grp">{i:02d} — {esc(mod)} · {len(items)} screens</div>')
        parts.append('<div class="stack">')
        parts.extend(render_screen(s, dark, offline, p) for s in items)
        parts.append("</div>")

    # **The workshop view, without a second copy of the screen.** The client specified this work
    # as boards of ten and reviews it that way; the platform team reads it by module. Those are two
    # groupings of one set of cards, so the board offers both and draws each screen once.
    ws_here: dict = {}
    for s_ in screens:
        w = ws_of(s_)
        if w:
            ws_here.setdefault(w[0], [w[1], 0])
            ws_here[w[0]][1] += 1
    wsbar = ""
    if ws_here:
        opts = "".join(
            f'<option value="{esc(c)}">{esc(c)} &middot; {esc(lbl)} ({n})</option>'
            for c, (lbl, n) in sorted(ws_here.items()))
        wsbar = (
            '<div class="wsbar"><label for="wsf">Workshop board</label>'
            f'<select id="wsf"><option value="">All {len(screens)} screens on this platform</option>'
            f'{opts}</select>'
            f'<span class="n">{len(ws_here)} workshop board(s) &middot; '
            f'{sum(n for _, n in ws_here.values())} of {len(screens)} screens came from a pack</span>'
            '</div>'
            '<script>(function(){var f=document.getElementById("wsf");'
            'f.addEventListener("change",function(){var v=f.value;'
            'document.querySelectorAll(".scr").forEach(function(c){'
            'c.hidden=!!v&&c.dataset.ws!==v;});'
            # A module heading above nothing reads as a module with no screens.
            'document.querySelectorAll(".stack").forEach(function(st){'
            'var any=Array.prototype.some.call(st.children,function(c){return !c.hidden;});'
            'st.hidden=!any;var h=st.previousElementSibling;'
            'if(h&&h.classList.contains("grp"))h.hidden=!any;});});})();</script>')

    named = sum(1 for s in screens if "named only" in str(s.get("provenance", "")))
    lede = clip(esc(str(p.get("notes") or "")).split("\n")[0], 340)
    warn = ""
    if named:
        warn = (f' <strong>{named} of these are named in a client board and not written up in '
                f'it</strong> — the operations are real, the layout is not.')

    doc_html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(code)} {esc(p['shortName'])} — wireframe board</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <a class="home" href="TICVAI%20Wireframe%20Boards.dc.html">&larr; All boards</a>
  <div class="head">
    <div><span class="mark">TICVAI</span>
      <h1>{esc(code)} · {esc(p['name'])} <span style="font-weight:600;color:#6B7280">({len(screens)} screens)</span></h1></div>
    <div class="meta">{esc(p.get('audience'))} · {esc(p.get('formFactor'))} · {esc(p.get('app'))}</div>
  </div>
  <p class="lede">{lede}{warn}</p>
  {wsbar}
  {''.join(parts)}
  <div class="bottom">
    <span>Generated by tools/derive-wireframes.py from screens/{esc(path.name)} — do not hand-edit</span>
    <span>{esc(code)} · {len(screens)} screens · {len(groups)} groups</span>
  </div>
</div></body></html>"""
    return doc_html, len(screens)


# **Platforms whose boards come from Claude Design, not from here.** As a hi-fi pack arrives for a
# platform, its code goes in this set and the generator stops writing over it — the pack is better
# specified than anything derived from a screen file, and regenerating would replace a drawing with
# a wireframe.
#
# **Everything not listed stays generated**, which is what keeps 476 screens drawn while the packs
# arrive one domain at a time.
# **A screen pointing at a design pack is never regenerated over.** Checked per screen rather
# than per platform, because one platform holds screens from three packs and screens from none —
# P08 alone answers frames in F&B, POS and Retail.
DESIGNED_PREFIXES = ("wireframes/FnB", "wireframes/POS", "wireframes/Retail",
                     "wireframes/TICVAI Boards v2")
DESIGNED: set = set()   # whole platforms; empty now that the check is per screen

# **A cross-platform exit is still a real reach.** `POS-002` goes to `BO-045`, which lives on
# P08's board; linking it to a local `#bo-045` produced the one dead anchor on the POS board.
# Filled in by main() once every platform file has been read.
BOARD_OF: dict = {}


# **The workshop grouping, carried as metadata rather than as a second drawing.** Until
# 10 September the 728 pack screens were rendered twice — once on their platform board and once on
# a `WS##` board — and a reviewer looking at two drawings of one screen has no way to tell it is
# one screen rather than a near-duplicate nobody merged. **The grouping is information about a
# card, not a reason to draw it again.**
#
# Codes are computed exactly as `derive-pack-boards.py` computed them — `module_of` then sorted
# order — so `WS13` still names the board the client called board 1 of Approval Workflows.
WS_MAP: dict = {}


def _module_of(pack: str) -> str:
    stem = re.sub(r"\.pdf$", "", pack, flags=re.I)
    stem = re.sub(r"[_ ]*Reference$", "", stem, flags=re.I)
    stem = re.sub(r"[_ ]*Module$", "", stem, flags=re.I)
    return stem.replace("_", " ").strip() or pack


def ws_map() -> dict:
    """`(module, board)` -> `(WS code, label)`, built on first use from every platform file."""
    if WS_MAP:
        return WS_MAP
    keys = set()
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        for sc in (yaml.safe_load(f.read_text(encoding="utf-8")).get("screens") or []):
            src = sc.get("source") or {}
            if src.get("pack") and src.get("board") is not None:
                keys.add((_module_of(src["pack"]), int(src["board"])))
    for i, k in enumerate(sorted(keys), 1):
        WS_MAP[k] = ("WS%02d" % i, "%s board %d" % (k[0], k[1]))
    return WS_MAP


def ws_of(screen: dict) -> tuple:
    """The workshop board a screen came from, or `()` if it did not come from a pack."""
    src = screen.get("source") or {}
    if not src.get("pack") or src.get("board") is None:
        return ()
    return ws_map().get((_module_of(src["pack"]), int(src["board"])), ())


def board_of() -> dict:
    """Which board file holds each screen, built on first use.

    **Populated lazily rather than in `main()`** because `derive-pack-boards` imports the card
    renderer and never calls `main()` — so the map was empty there, every cross-board exit fell
    back to a local `#anchor`, and the workshop boards shipped 82 links into anchors they do not
    contain.
    """
    if not BOARD_OF:
        for f in sorted(SCREENS.glob("P*.yaml")):
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
            name = f"{d['platform']['code']} {d['platform']['shortName']}.dc.html"
            for sc in d["screens"]:
                BOARD_OF[sc["id"]] = name
    return BOARD_OF


def _utf8_stdout() -> None:
    """**The generator crashed on a Windows console after writing every board.**

    `UnicodeEncodeError` on the `→` in its own progress line — a half-succeeded run reporting a
    traceback, which reads as total failure. Fixed here rather than by asking callers to set
    `PYTHONIOENCODING`, because `refresh.sh` runs this and a tool that needs an environment
    variable to print is a tool that will crash for the next person.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



def clip(text, n: int) -> str:
    """Truncate without splitting a character.

    **A slice at a fixed index can land inside an astral character** — an emoji is two UTF-16 code
    units, and `str[:170]` can keep the first and drop the second. The result is a lone surrogate,
    which `write_text` refuses with *surrogates not allowed* and no indication of which screen
    caused it.

    **Found 31 August**, when a note containing a red circle broke the whole board generation at
    position 74368 of a file nobody had edited by hand.
    """
    t = str(text or "")
    if len(t) <= n:
        return t
    out = t[:n]
    # **Drop a trailing lone surrogate.** Python strings hold code points, but a value that arrived
    # already split stays split, and encoding is where it surfaces.
    while out and "\ud800" <= out[-1] <= "\udfff":
        out = out[:-1]
    return out


def build_app(app: str, files: list) -> tuple:
    """One document for a shipped app, with a section per platform that folds into it.

    **The shell is the heading, not a separate board.** `P05 Guest Kiosk` is not another product;
    it is the guest app in a fixed frame with no keyboard, and a reviewer needs to see that it is
    the same catalogue and the same checkout rendered for a different pair of hands.
    """
    docs = []
    for f in sorted(files):
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        d["platform"]["_ids"] = {x["id"] for x in d["screens"]}
        docs.append((f, d))

    meta = docs[0][1]["platform"].get("targetApp") or {}
    name = meta.get("name") or app
    total = sum(len(d["screens"]) for _f, d in docs)

    parts, n_groups = [], 0
    for _f, d in docs:
        p_ = d["platform"]
        dark = p_["code"] in DARK
        offline = bool(p_.get("offlineCapable"))
        shell = ((p_.get("targetApp") or {}).get("shell")) or p_.get("formFactor")
        parts.append(
            f'<div class="shell"><b>{esc(p_["code"])} &middot; {esc(p_["shortName"])}</b>'
            f' <span>{esc(shell)} shell &middot; {len(d["screens"])} screens &middot; '
            f'{esc(p_.get("audience"))} &middot; {esc(p_.get("app"))}'
            + (" &middot; offline-capable" if offline else "") + "</span></div>")
        groups: dict = {}
        for sc in d["screens"]:
            groups.setdefault(sc.get("module") or "Screens", []).append(sc)
        for mod, items in groups.items():
            n_groups += 1
            parts.append(f'<div class="grp">{n_groups:02d} &mdash; {esc(p_["code"])} '
                         f'{esc(mod)} &middot; {len(items)} screens</div>')
            parts.append('<div class="stack">')
            parts.extend(render_screen(sc, dark, offline, p_) for sc in items)
            parts.append("</div>")

    note = esc(str(meta.get("note") or ""))
    members = " &middot; ".join(f'{esc(d["platform"]["code"])} {esc(d["platform"]["shortName"])}'
                               for _f, d in docs)
    doc_html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(name)} &mdash; app board</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}
.shell{{margin:34px 0 14px;padding:11px 15px;background:#F8FAFC;border:1px solid var(--soft);
border-radius:9px;font:800 13px/1.5 Manrope,system-ui,sans-serif;letter-spacing:-.01em}}
.shell span{{font-weight:600;color:var(--mut);font-size:11.5px}}
</style></head><body>
<div class="wrap">
  <a class="home" href="TICVAI%20Wireframe%20Boards.dc.html">&larr; All boards</a>
  <div class="head">
    <div><span class="mark">TICVAI</span>
      <h1>{esc(name)} <span style="font-weight:600;color:#6B7280">({total} screens)</span></h1></div>
    <div class="meta">{members}</div>
  </div>
  <p class="lede">{note}</p>
  {''.join(parts)}
  <div class="bottom">
    <span>Generated by tools/derive-wireframes.py &mdash; one board per shipped app, composed from
      the platform files. Do not hand-edit</span>
    <span>{esc(app)} &middot; {total} screens &middot; {len(docs)} platform(s)</span>
  </div>
</div></body></html>"""
    return doc_html, total


def main() -> int:
    only = sys.argv[1:] or None
    WIRE.mkdir(exist_ok=True)
    total = 0

    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        if only and code not in only:
            continue
        if code in DESIGNED and not only:
            print(f"  {code}  skipped — its boards come from Claude Design")
            continue
        out_name = f"{code} {doc['platform']['shortName']}.dc.html"
        body, n = build(f)
        # **Final guard.** Every truncation above is surrogate-safe, and a lone surrogate can
        # still arrive from a source file edited by a tool that split one. Encoding is where it
        # surfaces, and *surrogates not allowed* names neither the screen nor the field — so it is
        # cheaper to strip here than to find it again.
        body = body.encode("utf-8", "ignore").decode("utf-8")
        (WIRE / out_name).write_text(body, encoding="utf-8")
        WRITTEN.append(out_name)
        COVERED.add(code)
        print(f"  {code}  {n:>3} screens  → wireframes/{out_name}")
        total += 1
    # **And one board per shipped app.** Fifteen boards are the development unit; five are what
    # ships, and a reviewer opening Venue Management should meet its 550 screens as sections of
    # one surface rather than as four separate files.
    if not only:
        apps: dict = {}
        for f in sorted(SCREENS.glob("P*.yaml")):
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
            key = (d["platform"].get("targetApp") or {}).get("app")
            if key:
                apps.setdefault(key, []).append(f)
        for key, files in sorted(apps.items()):
            body, n = build_app(key, files)
            body = body.encode("utf-8", "ignore").decode("utf-8")
            out_name = f"APP {key}.dc.html"
            (WIRE / out_name).write_text(body, encoding="utf-8")
            WRITTEN.append(out_name)
            print(f"  {key:20} {n:>4} screens  \u2192 wireframes/{out_name}")
        if not apps:
            print("  no platform names a targetApp - run tools/apply-target-apps.py")

    # **The index board is generated too.** It listed eight files that no longer exist the moment
    # the boards were regenerated — `check-wireframes` caught it, and a hand-maintained index over
    # generated boards is the same defect one level up.
    if not only:
        cards = []
        # **What ships, before the fifteen files it is built from.** A reviewer opening the index
        # should meet the five apps first; the platform boards are below because they are the
        # development unit, not the product.
        _apps: dict = {}
        for f in sorted(SCREENS.glob("P*.yaml")):
            _d = yaml.safe_load(f.read_text(encoding="utf-8"))
            _t = _d["platform"].get("targetApp") or {}
            if _t.get("app"):
                _a = _apps.setdefault(_t["app"], {"name": _t.get("name"), "n": 0, "codes": []})
                _a["n"] += len(_d["screens"])
                _a["codes"].append(_d["platform"]["code"])
        for _key, _a in sorted(_apps.items()):
            _href = f"APP {_key}.dc.html".replace(" ", "%20")
            cards.append(f"""
      <a class="card app" href="{_href}">
        <div class="code">APP</div>
        <div class="nm">{esc(_a['name'] or _key)}</div>
        <div class="sub">{_a['n']} screens &middot; {esc(' · '.join(sorted(_a['codes'])))}</div>
      </a>""")
        for f in sorted(SCREENS.glob("P*.yaml")):
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
            p_ = d["platform"]
            href = f"{p_['code']} {p_['shortName']}.dc.html".replace(" ", "%20")
            named = sum(1 for s_ in d["screens"]
                        if "named only" in str(s_.get("provenance", "")))
            flag = (f'<div class="warn">{named} named only</div>' if named else "")
            cards.append(f"""
      <a class="card" href="{href}">
        <div class="code">{esc(p_['code'])}</div>
        <div class="nm">{esc(p_['name'])}</div>
        <div class="sub">{len(d['screens'])} screens · {esc(p_.get('audience'))} · {esc(p_.get('formFactor'))}</div>
        {flag}
      </a>""")
        idx = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TICVAI — wireframe boards</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:18px;margin-top:28px}}
.card{{display:block;text-decoration:none;background:#FFF;border:1px solid var(--soft);
border-radius:12px;padding:18px 20px;box-shadow:0 8px 20px rgba(12,35,64,.06)}}
.card:hover{{border-color:var(--brand)}}
.card.app{{background:#F8FAFC;border-color:#C7D2E4}}
.card.app .code{{color:var(--brand);font-weight:700}}
.code{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--dim);letter-spacing:.1em}}
.nm{{font-size:15px;font-weight:800;letter-spacing:-.01em;margin:5px 0 3px}}
.sub{{font-size:11.5px;color:var(--mut)}}
.warn{{margin-top:8px;font-size:10px;color:#9A5B00;background:#FFF1E6;
display:inline-block;padding:2px 7px;border-radius:4px}}
</style></head><body>
<div class="wrap">
  <div class="head">
    <div><span class="mark">TICVAI</span><h1>Wireframe boards</h1></div>
    <div class="meta">{len(cards)} platforms</div>
  </div>
  <p class="lede">One board per platform, every screen on one scrolling page at low fidelity.
  <strong>A reviewer opens it and reads the whole surface in one pass</strong> — that is the only
  thing a board is for. Generated from the screen definitions; nothing here is hand-drawn.</p>
  <div class="cards">{''.join(cards)}</div>
  <div class="bottom">
    <span>Generated by tools/derive-wireframes.py — do not hand-edit</span>
    <span>{len(cards)} boards</span>
  </div>
</div></body></html>"""
        # **`wireframes/index.html` is the door.** The viewer opens it by name, and until
        # 26 August this package never wrote one — it wrote `TICVAI Wireframe Boards.dc.html`,
        # which the viewer does not look for. **A door nobody generates is a door that goes stale
        # the moment somebody hand-makes one**, which is what happened: a 25 August `index.html`
        # sat in the repo pointing at boards that had since been renamed.
        #
        # Two indexes exist and they are not duplicates. `TICVAI All Boards Index.dc.html` is the
        # client-facing contents page across every board including the packs; this one is the
        # generated platform index. **`index.html` is a copy of the generated one under the name
        # the viewer opens**, so the door is always current.
        (WIRE / "TICVAI Wireframe Boards.dc.html").write_text(idx, encoding="utf-8")
        (WIRE / "index.html").write_text(idx, encoding="utf-8")
        print("  index    → wireframes/TICVAI Wireframe Boards.dc.html + index.html")

        # **A rename leaves a ghost, and the ghost looks authoritative.** A dump copies and never
        # deletes, so `P08 Staff Web Back Office.dc.html` (733 KB, 25 August) outlived its
        # replacement `P08 Venue Management.dc.html` (383 KB) and anyone opening the old name got
        # an out-of-date board with no sign it was superseded.
        #
        # **The manifest is what the transfer needs.** It says what should exist; anything else in
        # the folder is a leftover, and a consumer can delete or flag it without guessing.
        # **A manifest that only lists what this tool writes cannot see a stranger.** The first
        # version listed the 15 generated boards and the indexes, so a client pack was "not
        # generated" and a board from a different product was also "not generated" — the same
        # answer for a file that belongs and a file that does not.
        #
        # **31 August**: a consumer counting `wireframes/` reported 811 unclaimed frames against a
        # real 359. The difference was eight boards superseded by a rename on 26 August and nine
        # belonging to other products entirely — `Aster *`, `Park_POS`, `Viewer Redesign`. **A
        # worklist wrong by 55% is worse than no worklist**, because somebody plans against it.
        #
        # Four categories now, and a consumer can act on each: `generated` is ours to rewrite,
        # `clientPacks` is drawn and must never be touched, `workshopBoards` is generated by
        # another tool in this package, `unrecognised` is a file this package cannot account for.
        #
        # **`workshopBoards` is a category and not an exception.** `tools/derive-pack-boards.py`
        # writes a `WS## …` board per workshop board, and without a name here all 59 would land in
        # `unrecognised` — which is the list somebody reads to find leftovers from a rename. A
        # generated file sitting in it makes the list useless for the thing it exists to catch.
        packs = sorted(f.name for f in WIRE.glob("*.dc.html")
                       if not re.match(r"^P\d\d ", f.name) and not f.name.startswith("TICVAI")
                       and f.name not in {"index.html"})
        workshop = [n for n in packs if re.match(r"^WS\d\d ", n)]
        packs = [n for n in packs if n not in set(workshop)]
        known_packs = tuple(PACK_PREFIXES)
        unrecognised = [n for n in packs if not n.startswith(known_packs)]
        packs = [n for n in packs if n.startswith(known_packs)]

        manifest = {
            "generatedBy": "tools/derive-wireframes.py",
            "entryPoint": "wireframes/index.html",
            "clientPacks": packs,
            "workshopBoards": workshop,
            "workshopBoardsNote": (
                "**One board per workshop board, written by `tools/derive-pack-boards.py`.** The "
                "same screens the platform boards render, regrouped into the 59 boards of ten the "
                "client specified — a platform is what a team owns, and a board is what the "
                "workshop wrote. Regenerated from `screens/P*.yaml`, so never hand-edited."),
            "unrecognised": unrecognised,
            "unrecognisedNote": (
                "**Files in `wireframes/` this package cannot account for.** Not generated by this "
                "tool and not matching a known client pack prefix. **Most often a board from "
                "another product, or one superseded by a rename** — a copy-based transfer never "
                "deletes, so a rename leaves both files and the old one still looks authoritative."),
            "note": ("Boards this package generates. **Anything in `wireframes/` not listed here "
                     "and not a client pack is a leftover** — most often a board renamed on one "
                     "side of a dump, since a copy never deletes."),
            "generated": sorted(WRITTEN),
            "indexes": ["index.html", "TICVAI Wireframe Boards.dc.html",
                        "TICVAI All Boards Index.dc.html"],
        }
        (WIRE / "manifest.json").write_text(
            json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"  manifest → wireframes/manifest.json ({len(manifest['generated'])} generated)")

        # **Delete the boards this generator no longer writes.** A rename used to leave both files
        # and the old one looked authoritative — `P08 Staff Web Back Office.dc.html` at 733 KB
        # against its 383 KB replacement, opening by name with nothing to say it was superseded.
        #
        # **Only files matching the generated shape are removed** — `P## Name.dc.html` where the
        # code is a platform this run covered. **A client pack is never touched**, because the
        # generator did not write it and has no business deleting it.
        known = set(manifest["generated"]) | set(manifest["indexes"])
        stale = []
        for f in sorted(WIRE.glob("*.dc.html")):
            if f.name in known:
                continue
            m = re.match(r"^(P\d\d) ", f.name)
            if m and m.group(1) in COVERED:
                stale.append(f)
        for f in stale:
            f.unlink()
            print(f"  removed  {f.name} — superseded by a rename this generator now owns")
        if stale:
            print(f"  {len(stale)} stale board(s) deleted. A copy never deletes, so a rename "
                  "leaves a ghost unless the writer clears it.")
        if UNCHROMED:
            print(f"  WARN  audiences with no chrome, drawing staff furniture: {sorted(UNCHROMED)}")

    print(f"  {total} board(s) generated")
    return 0


_utf8_stdout()

if __name__ == "__main__":
    sys.exit(main())
