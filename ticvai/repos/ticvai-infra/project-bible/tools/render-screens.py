#!/usr/bin/env python3
"""Render screens as wireframe frames, from the design tokens rather than by hand.

**This is Phase 5, and it is the test of whether the regeneration was worth doing.** A screen model
rich enough to draw from is the whole claim; if the frames come out thin, the specification was
thin and the counters were flattering.

## The fidelity target is Claude Design's boards, and the reason is not vanity

`derive-wireframes.py` says it plainly and was right at the time: *"three client packs render at
1280x700 in this system and 385 screens rendered as dashed-box wireframes — and a client reviewing
both reads the difference as those screens are not done."* The information was identical; the
fidelity was what was being judged.

So this renders what Claude Design renders: a **1280×880 frame**, real application chrome, cards,
labelled fields with values in them, tables with populated rows. The difference is that theirs was
drawn per screen by a person and this is derived, which is the only way 1,091 of them exist.

## Where the sample values come from

**The pack's own `§Examples` and `§Status` sections** — 117 of P09 Commercial's 230 screens have
one. `ADM-048` supplies *Standard Retail, Venue, Attraction, Event, Membership, Group, Corporate,
B2B, Reseller, OTA* and the lifecycle *Draft / Configured / Validated / Active / Inactive /
Expired / Archived*, and those are the values its table renders.

The generator deliberately leaves worked examples in the pack rather than copying them onto the
screen, because an enum's documentation belongs in the contract. **Illustration is a different job
from specification**, and this is where illustration belongs: the renderer reads them, the screen
does not carry them.

Where a pack gives none, the value is inferred from the column's own name — a column called
`Requested date` renders a date and one called `Margin impact` renders money — and the inference is
deterministic per screen, column and row, so two runs produce identical output and a diff means a
real change.

**No value here is a claim about data.** It is a shape, so a reviewer can see whether a column is
too narrow, whether nine columns fit, and whether the screen answers the question it exists for.

## What it renders that `derive-wireframes.py` cannot

That renderer predates the pattern layer. Against a regenerated screen it takes `comps[:3]` for the
main column and `comps[3:5]` for the side — **five components, where `ADM-048` declares
twenty-five** — draws every table with the same invented `Name / Status / Value` header, renders
only `contentBody`, and has no concept of an overlay.

Here: every region is drawn where it belongs, the real columns are the table header, and **every
overlay becomes its own frame** — the screen behind it, dimmed by the `scrim` token, with the
dialog over it. The frame count is the screen count plus exactly the number of declared overlays.
Derived, never estimated.

**Nothing is invented.** `derive-wireframes.py` has a `TEMPLATE_SHAPE` fallback that adds
components a screen never declared, labelled *implied by template*, because 212 screens declared
one component and a lonely box read as an empty screen. A regenerated screen needs no such crutch,
and **a screen that genuinely has nothing draws nothing and says why** — 70 of P09's Commercial
screens are in that position and the frame states it rather than filling the space.

**What is bound is marked.** A column carrying a contract field path renders its header in the
accent colour; one carrying a source label with nothing behind it yet renders grey. That difference
is the most useful thing on the board.

## Colour comes from `_design-tokens.yaml`

Not from a palette in this file. The tokens were extracted from two independent sources that
agree — Claude Design's boards and the client's own `Park_POS_dc.html` — and a renderer carrying
its own hexes would fork the system on its first edit.

Run: python tools/render-screens.py --platform P09 --module Commercial --out _review-p09-commercial
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
PACK = ROOT / "sources" / "workshop" / "pack.json"

FRAME_W, FRAME_H = 1280, 880


def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def clip(text, n: int) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", str(text or ""))
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def tokens() -> dict:
    return yaml.safe_load((SCREENS / "_design-tokens.yaml").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------------------------
# Sample values
# --------------------------------------------------------------------------------------------

ARTEFACT = re.compile(r"Pag\s?e\b|TICVAI\s*[•?]\s*\d+|^\s*\d+\s*\|")

PEOPLE = ["Priya Raman", "J. Hale", "M. Okonkwo", "Sara Idris", "D. Whitfield", "A. Nakamura",
          "L. Ferreira", "N. Haddad"]
VENUES = ["Riverside Arts", "Dubai Parks", "Abu Dhabi Attractions", "Harbour Pavilion"]
CHANNELS = ["Web · Direct", "Mobile App", "Box Office", "OTA · Viator", "Reseller · B2B"]
MARKETS = ["UAE", "KSA", "United Kingdom", "India", "Germany"]

# Column name → the shape of the thing in it. **Order matters**: `Requested date` is a date before
# it is a request, and `Discount exposure` is money before it is a discount.
SHAPES: list[tuple[str, str]] = [
    (r"\b(status|state|stage|lifecycle)\b", "status"),
    (r"\b(date|expiry|expires|created|updated|modified|period|window|schedule|at)\b", "date"),
    (r"\b(id|code|reference|ref|sku|barcode)\b", "code"),
    (r"\b(email|mail)\b", "email"),
    (r"\b(by|owner|requester|approver|manager|seller|buyer|user|contact|agent)\b", "person"),
    (r"\b(amount|price|pricing|revenue|cost|budget|fee|fees|proceeds|value|exposure|margin|"
     r"spend|payout|settlement|commission|aed|total value)\b", "money"),
    (r"\b(percent|percentage|rate|ratio|elasticity|conversion|uplift|attach|share|%)\b", "pct"),
    (r"\b(count|total|number|qty|quantity|volume|capacity|inventory|units|redemptions|"
     r"listings|issued)\b", "int"),
    (r"\b(venue|site|park|location)\b", "venue"),
    (r"\b(channel|source)\b", "channel"),
    (r"\bcurrency\b", "currency"),
    (r"\b(market|country|region|territory)\b", "market"),
    (r"\b(risk|priority|severity|level|tier|band)\b", "level"),
]

LEVELS = ["Low", "Medium", "High", "Critical"]
DEFAULT_STATUSES = ["Active", "Draft", "Pending", "Expired", "Suspended"]

# Status word → which semantic pair it renders in. **A status chip that is always grey teaches a
# reviewer nothing**, and the packs' own vocabularies are consistent enough to colour.
STATUS_TONE = [
    (r"^(active|approved|published|live|validated|complete|settled|paid|ok)", "ok"),
    (r"^(draft|pending|awaiting|review|submitted|queued|scheduled|configured)", "warn"),
    (r"^(expired|rejected|failed|suspended|cancelled|revoked|blocked|archived|inactive)", "bad"),
]


def shape_of(column: str) -> str:
    low = f" {str(column).lower()} "
    for pattern, kind in SHAPES:
        if re.search(pattern, low):
            return kind
    return "text"


def pick(seq, *seed) -> str:
    """Deterministic choice. Two runs must produce identical HTML or a diff means nothing."""
    h = hashlib.sha1("|".join(str(s) for s in seed).encode("utf-8")).digest()
    return seq[int.from_bytes(h[:4], "big") % len(seq)]


def sample(column: str, facts: dict, sid: str, row: int) -> tuple[str, str]:
    """A plausible value for one cell, and its tone (`""`, `ok`, `warn`, `bad`, `mono`)."""
    kind = shape_of(column)
    seed = (sid, column, row)
    if kind == "status":
        return pick(facts["statuses"] or DEFAULT_STATUSES, *seed), "chip"
    if kind == "date":
        d = pick(["4 Feb 2026", "17 Mar 2026", "2 Apr 2026", "28 Apr 2026", "11 Jun 2026",
                  "3 Sep 2026", "22 Jan 2026", "9 May 2026", "30 Jul 2026", "14 Oct 2026",
                  "6 Dec 2026", "19 Aug 2026"], *seed)
        return d, "mono"
    if kind == "code":
        return pick(["PRM-4821", "PL-0937", "CHN-118", "RSL-24471", "BND-3062", "UPG-0714",
                     "PRM-4907", "PL-1142", "CHN-206", "RSL-24688", "BND-3315", "CPN-88104"],
                    *seed), "mono"
    if kind == "email":
        return pick(["j.hale@northern.example", "ops@riverside.example",
                     "p.raman@ticvai.example"], *seed), "mono"
    if kind == "person":
        return pick(PEOPLE, *seed), ""
    if kind == "money":
        return "AED " + pick(["1,240.00", "18,400.00", "96,250.00", "412.50", "7,880.00",
                              "233,900.00", "64.00", "2,915.50", "48,120.00", "310.75",
                              "1,004,600.00", "9,450.00", "725.20", "156,300.00"], *seed), "mono"
    if kind == "pct":
        return pick(["4.2%", "12.4%", "18.9%", "31.0%", "62.5%", "-3.8%", "0.9%", "7.6%",
                     "24.1%", "48.3%", "-11.2%", "88.0%"], *seed), "mono"
    if kind == "int":
        return pick(["12", "184", "1,284", "37", "9,610", "462", "3", "56", "728", "24,905",
                     "91", "1,177"], *seed), "mono"
    if kind == "venue":
        return pick(VENUES, *seed), ""
    if kind == "channel":
        return pick(CHANNELS, *seed), ""
    if kind == "currency":
        return pick(["AED", "USD", "GBP"], *seed), "mono"
    if kind == "market":
        return pick(MARKETS, *seed), ""
    if kind == "level":
        return pick(LEVELS, *seed), "chip"
    if facts["examples"]:
        return pick(facts["examples"], *seed), ""
    return pick(["Standard", "Peak season", "Weekday saver", "Group of 10+", "Member rate",
                 "Partner allocation"], *seed), ""


def tone_of(status: str) -> str:
    low = str(status).strip().lower()
    for pattern, tone in STATUS_TONE:
        if re.match(pattern, low):
            return tone
    return "neutral"


# A heading that announces a set of values, rather than one that announces actions or columns.
# `Approval can be required for` qualifies and gives `ADM-145` its real request types; `Actions`
# does not, and reading it as one put `Suspend` in a column called `Listing`.
VALUE_LIST = re.compile(r"can be\b|\btypes?$|\bkinds?$|\boptions?$|\bcategories$|"
                        r"\bincludes?$|such as|\bvalues?$|\blevels?$|\btiers?$|\bmodels?$")


def pack_facts() -> dict:
    """Per pack entry: the worked examples and the lifecycle vocabulary, for illustration only."""
    out = {}
    if not PACK.exists():
        return out
    for e in json.loads(PACK.read_text(encoding="utf-8")):
        ex, st, grp = [], [], []
        for heading, bullets in (e.get("sections") or {}).items():
            low = heading.lower()
            for b in bullets:
                if ARTEFACT.search(b):
                    continue
                if low.startswith("example"):
                    # **A value, not a sentence about values.** Four words, no terminal stop, and
                    # no modal verb — `Approval chains must be configurable.` is five words, passed
                    # the length test alone, and rendered as the name of a promotion.
                    if (len(b.split()) <= 4 and not b.rstrip().endswith((".", ":", ";"))
                            and not re.search(r"\b(must|shall|should|will|can|may|are|is)\b",
                                              b, re.I)):
                        ex.append(b)
                elif VALUE_LIST.search(low) and len(b.split()) <= 4 and                         not b.rstrip().endswith((".", ":", ";")) and                         not re.search(r"\b(must|shall|should|will|may)\b", b, re.I):
                    grp.append(b)
                if low.startswith(("status", "state")) and "/" in b:
                    st += [p.strip() for p in b.split("/") if 1 <= len(p.split()) <= 3]
        # **`§Examples` first, the pack's own detail groups behind it.** The groups carry 43% of
        # the corpus by bullet count — `New promotion`, `Discount increase`, `Budget increase` —
        # and they are far closer to real values than any generic pool.
        out[(e["source"], str(e["number"]), str(e["page"]))] = {
            "examples": [x for x in ex if x] or [x for x in grp if x],
            "statuses": [x for x in st if x]}
    return out


# --------------------------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------------------------

def css(t: dict) -> str:
    c, ty, r, sp = t["colour"], t["typography"], t["radius"], t["spacing"]
    return f"""
:root{{
 --ground:{c['ground']};--surface:{c['surface']};--sunken:{c['surfaceSunken']};--paper:{c['surfaceRaised']};
 --rail:{c['groundDark']};--railText:{c['textOnDarkMuted']};--railFaint:{c['textFaint']};
 --body:{c['textBody']};--strong:{c['textStrong']};--muted:{c['textMuted']};--faint:{c['textFaint']};
 --hair:{c['hairline']};--edge:{c['border']};--edgeStrong:{c['borderStrong']};
 --accBg:{c['accent']['bg']};--accText:{c['accent']['text']};--accSolid:{c['accentSolid']['bg']};
 --okBg:{c['success']['bg']};--okText:{c['success']['text']};--okLine:{c['successBorder']};
 --wnBg:{c['warning']['bg']};--wnText:{c['warning']['text']};--wnLine:{c['warningBorder']};
 --bdBg:{c['danger']['bg']};--bdText:{c['danger']['text']};--bdLine:{c['dangerBorder']};
 --scrim:{t['elevation']['scrim']};--mono:{ty['family']['mono']};
}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:#EEF1F6;-webkit-font-smoothing:antialiased}}
body{{color:{c['groundDark']};font:{ty['weight']['medium']} {ty['scale']['body']}/1.5 {ty['family']['ui']}}}
.wrap{{max-width:1420px;margin:0 auto;padding:26px 34px 90px}}

/* --- page head, in the boards' own idiom ----------------------------------------- */
.mast{{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;
 padding-bottom:14px;border-bottom:2px solid {c['groundDark']}}}
.mark{{font-size:12px;font-weight:800;letter-spacing:.18em;
 background:linear-gradient(90deg,{c['accentSolid']['bg']},#00B8FF);-webkit-background-clip:text;
 background-clip:text;color:transparent}}
h1{{font-size:21px;font-weight:800;letter-spacing:-.02em;margin:5px 0 0}}
h1 span{{font-weight:600;color:var(--muted)}}
.meta{{font-family:var(--mono);font-size:10.5px;color:var(--muted);text-align:right;line-height:1.7}}
.lede{{font-size:12.5px;color:var(--body);max-width:88ch;margin:16px 0 0;line-height:1.65}}
.call{{display:flex;gap:12px;padding:13px 16px;margin-top:16px;background:var(--wnBg);
 border:1px solid var(--wnLine);border-radius:12px;font-size:12px;color:var(--wnText);line-height:1.6}}
.call i{{width:3px;border-radius:2px;background:var(--wnText);flex:none;opacity:.5}}
.toc{{font-family:var(--mono);font-size:9.5px;color:var(--faint);margin:14px 0 0;line-height:2}}
.toc a{{color:var(--muted);text-decoration:none}}

/* --- one screen block ------------------------------------------------------------- */
.scr{{display:flex;flex-direction:column;gap:13px;margin:46px 0 0;scroll-margin-top:24px}}
.hd{{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}}
.hd .id{{font-family:var(--mono);font-size:12px;color:var(--muted)}}
.hd .nm{{font-size:16.5px;font-weight:800;letter-spacing:-.015em}}
.tag{{font-size:9px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;
 border-radius:5px;background:var(--sunken);color:var(--muted)}}
.tag.a{{background:var(--accBg);color:var(--accText)}}
.tag.w{{background:var(--wnBg);color:var(--wnText)}}
.tag.b{{background:var(--bdBg);color:var(--bdText)}}
.sub{{font-size:12px;color:var(--muted);margin-top:3px;max-width:100ch;line-height:1.55}}

/* --- the frame -------------------------------------------------------------------- */
.frame{{position:relative;width:{FRAME_W}px;height:{FRAME_H}px;display:flex;flex-direction:column;
 padding:20px;background:var(--paper);border:1px solid var(--edgeStrong);border-radius:16px;
 box-shadow:0 16px 38px rgba(12,35,64,.09)}}
.shell{{flex:1;min-height:0;display:flex;border:1px solid var(--edgeStrong);border-radius:12px;
 overflow:hidden;background:var(--paper)}}
.rail{{width:186px;flex:none;background:var(--rail);display:flex;flex-direction:column;padding:16px 0}}
.rail .bd{{padding:0 16px 14px}}
.rail .bd b{{display:block;color:#fff;font-size:13px;font-weight:800;letter-spacing:-.01em}}
.rail .bd s{{display:block;text-decoration:none;color:var(--railFaint);font-size:10px;
 font-family:var(--mono);margin-top:3px}}
.rail i{{display:flex;align-items:center;gap:9px;font-style:normal;padding:8px 16px;
 color:var(--railText);font-size:11.5px}}
.rail i.on{{background:rgba(255,255,255,.08);color:#fff;font-weight:700;
 box-shadow:inset 3px 0 0 var(--accSolid)}}
.rail i u{{width:6px;height:6px;border-radius:4px;background:currentColor;opacity:.45;flex:none}}
.rail .ft{{margin-top:auto;padding:12px 16px 0;color:var(--railFaint);font-family:var(--mono);
 font-size:9.5px;line-height:1.7;border-top:1px solid rgba(255,255,255,.08);margin-left:16px;
 margin-right:16px}}

.app{{flex:1;min-width:0;display:flex;flex-direction:column}}
.appbar{{flex:none;height:46px;border-bottom:1px solid var(--hair);display:flex;align-items:center;
 justify-content:space-between;padding:0 20px;background:var(--paper)}}
.appbar b{{font-size:13px;font-weight:800}}
.appbar s{{text-decoration:none;font-family:var(--mono);font-size:10.5px;color:var(--muted)}}
.canvas{{flex:1;min-height:0;display:flex;gap:18px;padding:18px 22px;background:var(--surface);
 overflow:hidden}}
.main{{flex:1;min-width:0;display:flex;flex-direction:column;gap:14px}}
.side{{width:286px;flex:none;display:flex;flex-direction:column;gap:14px}}

.card{{background:var(--paper);border:1px solid var(--edge);border-radius:12px;padding:16px 18px;
 display:flex;flex-direction:column;gap:11px;min-height:0}}
.card.g{{flex:1;overflow:hidden}}
.card h3{{margin:0;font-size:13.5px;font-weight:800;display:flex;justify-content:space-between;
 align-items:baseline;gap:10px}}
.card h3 s{{text-decoration:none;font-family:var(--mono);font-size:9.5px;color:var(--faint);
 font-weight:600}}
.hint{{padding:10px 12px;border-radius:10px;background:var(--ground);font-size:11px;
 color:var(--body);line-height:1.55}}

.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(122px,1fr));gap:10px}}
.kpi{{background:var(--paper);border:1px solid var(--edge);border-radius:10px;padding:10px 12px}}
.kpi u{{display:block;text-decoration:none;font-family:var(--mono);font-size:9px;
 letter-spacing:.09em;text-transform:uppercase;color:var(--faint);line-height:1.35;min-height:24px}}
.kpi s{{display:block;text-decoration:none;font:800 19px/1.2 var(--mono);margin-top:4px}}
.kpi.bound s{{color:var(--accText)}}

table{{width:100%;border-collapse:collapse;table-layout:fixed}}
th{{text-align:left;padding:0 8px 7px;font-family:var(--mono);font-size:9px;letter-spacing:.09em;
 text-transform:uppercase;color:var(--faint);font-weight:600;border-bottom:1px solid var(--edge);
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
th.b{{color:var(--accText)}}
td{{padding:9px 8px;border-bottom:1px solid var(--hair);font-size:11.5px;color:var(--strong);
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
td.mono{{font-family:var(--mono);font-size:11px;color:var(--body)}}
tr.sel td{{background:var(--accBg)}}
.st{{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px}}
.st.ok{{background:var(--okBg);color:var(--okText)}}
.st.warn{{background:var(--wnBg);color:var(--wnText)}}
.st.bad{{background:var(--bdBg);color:var(--bdText)}}
.st.neutral{{background:var(--sunken);color:var(--muted)}}

.fields{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.fields.one{{grid-template-columns:1fr}}
.f{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.f u{{text-decoration:none;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;
 text-transform:uppercase;color:#94A0B4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.f s{{text-decoration:none;height:36px;border-radius:9px;border:1px solid var(--edgeStrong);
 display:flex;align-items:center;padding:0 11px;font-size:12px;color:var(--strong);
 background:var(--paper);white-space:nowrap;overflow:hidden}}
.f.dim s{{color:var(--faint)}}

.filters{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}}
.search{{flex:1;min-width:180px;height:32px;border:1px solid var(--edgeStrong);border-radius:9px;
 display:flex;align-items:center;padding:0 11px;font-size:11.5px;color:var(--faint);
 background:var(--paper)}}
.fc{{font-size:10.5px;padding:5px 10px;border-radius:99px;background:var(--paper);
 border:1px solid var(--edge);color:var(--body);white-space:nowrap}}

.actbar{{flex:none;display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:11px 20px;
 border-top:1px solid var(--hair);background:var(--paper)}}
.btn{{font-size:11.5px;font-weight:700;padding:7px 13px;border-radius:9px;border:1px solid var(--edgeStrong);
 background:var(--paper);color:var(--strong);line-height:1.25}}
.btn.p{{background:var(--accSolid);border-color:transparent;color:#fff}}
.btn.d{{background:var(--bdBg);border-color:var(--bdLine);color:var(--bdText)}}
.btn.g{{background:var(--wnBg);border-color:var(--wnLine);color:var(--wnText)}}
.btn small{{display:block;font-family:var(--mono);font-size:8.5px;font-weight:600;opacity:.7;
 letter-spacing:.04em;margin-top:1px}}
.spacer{{flex:1}}

.hollow{{flex:1;display:flex;align-items:center;justify-content:center;padding:40px;
 background:var(--surface)}}
.hollow div{{max-width:58ch;text-align:center;color:var(--wnText);background:var(--wnBg);
 border:1px dashed var(--wnLine);border-radius:12px;padding:22px 26px;font-size:12px;
 line-height:1.6}}

/* --- an overlay is a frame -------------------------------------------------------- */
.scrim{{position:absolute;inset:20px;border-radius:12px;background:var(--scrim);z-index:2}}
.dlg{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:{t['overlay']['confirmDialog']['width']};
 background:var(--paper);border-radius:12px;box-shadow:{t['elevation']['overlay']};padding:20px 22px;
 z-index:3}}
.dlg b{{display:block;font-size:14px;font-weight:800;margin-bottom:8px}}
.dlg p{{margin:0 0 16px;font-size:11.5px;color:var(--body);line-height:1.6}}
.dlg .row{{display:flex;gap:8px;justify-content:flex-end}}
/* **A drawer is not a dialog and must not be drawn as one.** It enters from the edge the tokens
   name, keeps the screen behind it visible rather than blocking it, and runs full height - which
   is the entire reason the 3 August workshop chose it over full-page navigation. Rendering it
   centred would have shown a confirmation where the decision was that the cashier never leaves
   the catalogue. */
.drw{{position:absolute;top:20px;bottom:20px;{t['overlay']['drawer']['edge']}:20px;
 width:{t['overlay']['drawer']['width']};background:var(--paper);
 border-radius:12px;box-shadow:{t['elevation']['overlay']};padding:20px 22px;z-index:3;
 display:flex;flex-direction:column}}
.drw b{{display:block;font-size:14px;font-weight:800;margin-bottom:8px}}
.drw p{{margin:0 0 14px;font-size:11.5px;color:var(--body);line-height:1.6}}
.drw .step{{font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;
 color:var(--muted);margin-bottom:10px}}
.drw .row{{display:flex;gap:8px;justify-content:flex-end;margin-top:auto}}

/* --- footer under each frame ------------------------------------------------------ */
.foot{{font-family:var(--mono);font-size:10px;line-height:1.85;color:#7C8899}}
.foot b{{color:var(--strong);font-weight:600}}
.foot .none{{color:var(--bdText)}}
.foot a{{color:var(--accText);text-decoration:none}}
.gap{{display:flex;gap:11px;padding:11px 14px;background:var(--wnBg);border:1px solid var(--wnLine);
 border-radius:10px;font-size:11.5px;color:var(--wnText);line-height:1.55}}
.gap i{{width:3px;border-radius:2px;background:var(--wnText);flex:none;opacity:.5}}
"""


# --------------------------------------------------------------------------------------------
# Fragments
# --------------------------------------------------------------------------------------------

def bound(col) -> bool:
    return bool(re.match(r"^[A-Z][A-Za-z0-9]*(\[\])?\.[A-Za-z]", str(col)))


def leaf(col) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", str(col).split(".")[-1]).strip().capitalize() \
        if bound(col) else str(col)


def rail(screen: dict, plat: dict) -> str:
    module = screen.get("module") or plat.get("shortName")
    nav = ["Overview", module, "Catalogue", "Reports", "Settings"]
    items = "".join(f'<i class="{"on" if i == 1 else ""}"><u></u>{esc(clip(n, 22))}</i>'
                    for i, n in enumerate(nav))
    return (f'<aside class="rail"><div class="bd"><b>TICVAI</b>'
            f'<s>{esc(plat.get("shortName", ""))}</s></div>{items}'
            f'<div class="ft">{esc(screen.get("pattern") or "")}<br>'
            f'{esc(screen.get("density") or "")}</div></aside>')


COUNTING = re.compile(r"^(total|active|draft|open|pending|expired|all|number|count|new|"
                      r"upcoming|recently|configured|published|issued|unique)\b|"
                      r"\b(lists|items|records|products|categories|rates|codes|campaigns|"
                      r"bundles|listings|channels|rules|issues|structures|markets|currencies)$",
                      re.I)


def kpi_row(comps: list[dict], facts: dict, sid: str) -> str:
    """**A metric tile counts things unless it plainly measures money.** `Total Price Lists` matched
    the money rule on the word `price` and rendered `AED 1,240.00` as a count of price lists."""
    tiles = []
    for i, c in enumerate(comps):
        label = c.get("label") or ""
        if COUNTING.search(label.strip()):
            value, _ = sample("count", facts, sid, i)
        else:
            value, _ = sample(label, facts, sid, i)
            if shape_of(label) not in ("int", "money", "pct"):
                value, _ = sample("count " + label, facts, sid, i)
        tiles.append(f'<div class="kpi{" bound" if c.get("bindsTo") else ""}">'
                     f'<u>{esc(clip(label, 34))}</u><s>{esc(value)}</s></div>')
    return f'<div class="kpis">{"".join(tiles)}</div>' if tiles else ""


def data_table(comp: dict, facts: dict, sid: str, rows: int = 7) -> str:
    cols = (comp.get("columns") or [])[:8]
    extra = len(comp.get("columns") or []) - len(cols)
    head = "".join(f'<th class="{"b" if bound(c) else ""}" title="{esc(c)}">{esc(leaf(c))}</th>'
                   for c in cols)
    if extra > 0:
        head += f'<th>+{extra}</th>'
    body = []
    for r in range(rows):
        cells = []
        for c in cols:
            v, tone = sample(leaf(c), facts, sid, r)
            if tone == "chip":
                cells.append(f'<td><span class="st {tone_of(v)}">{esc(v)}</span></td>')
            else:
                cells.append(f'<td class="{tone}">{esc(v)}</td>')
        if extra > 0:
            cells.append("<td>…</td>")
        body.append(f'<tr class="{"sel" if r == 1 else ""}">{"".join(cells)}</tr>')
    op = comp.get("operation") or "no operation"
    return (f'<div class="card g"><h3>{esc(comp.get("label") or "Records")}'
            f'<s>{esc(op)}{" · " + esc(comp["bindsTo"]) if comp.get("bindsTo") else ""}</s></h3>'
            f'<table><tr>{head}</tr>{"".join(body)}</table>'
            + (f'<div class="hint">{esc(clip(comp["notes"], 200))}</div>'
               if comp.get("notes") else "") + "</div>")


def form_card(comps: list[dict], facts: dict, sid: str, title: str = "Configuration") -> str:
    fs = []
    for i, c in enumerate(comps[:12]):
        label = c.get("label") or c.get("kind")
        value, _ = sample(label, facts, sid, i)
        fs.append(f'<div class="f"><u>{esc(clip(label, 34))}</u><s>{esc(clip(value, 30))}</s></div>')
    src = comps[0].get("provenance", "") if comps else ""
    more = (f'<div class="hint">{len(comps) - 12} further fields the pack names for this screen '
            f'are not drawn — the frame shows the first twelve.</div>' if len(comps) > 12 else "")
    return (f'<div class="card"><h3>{esc(title)}<s>{esc(clip(src, 56))}</s></h3>'
            f'<div class="fields">{"".join(fs)}</div>{more}</div>')


def detail_card(comp: dict, facts: dict, sid: str) -> str:
    cols = (comp.get("columns") or [])[:9]
    fs = "".join(f'<div class="f"><u>{esc(clip(leaf(c), 30))}</u>'
                 f'<s>{esc(clip(sample(leaf(c), facts, sid, 1)[0], 28))}</s></div>' for c in cols)
    return (f'<div class="card g"><h3>{esc(comp.get("label") or "Selected")}'
            f'<s>{esc(comp.get("bindsTo") or "unbound")}</s></h3>'
            f'<div class="fields one">{fs}</div>'
            + (f'<div class="hint">{esc(clip(comp["notes"], 170))}</div>'
               if comp.get("notes") else "") + "</div>")


def filter_bar(comps: list[dict], facts: dict, sid: str) -> str:
    bits = []
    for c in comps:
        if c.get("kind") == "searchField":
            bits.append(f'<div class="search">{esc(c.get("label") or "Search")}</div>')
        else:
            cols = c.get("columns") or []
            for i, col in enumerate(cols[:6]):
                v, _ = sample(leaf(col), facts, sid, i)
                bits.append(f'<span class="fc">{esc(leaf(col))} · '
                            f'{esc(clip(v, 16))} ▾</span>')
            if len(cols) > 6:
                bits.append(f'<span class="fc">+{len(cols) - 6} more</span>')
    return f'<div class="filters">{"".join(bits)}</div>' if bits else ""


def action_bar(comps: list[dict]) -> str:
    left, right = [], []
    for c in comps:
        k = c.get("kind")
        if k == "banner":
            left.append(f'<span class="fc" title="{esc(clip(c.get("notes"), 300))}">'
                        f'{esc(c.get("label"))}</span>')
        elif k == "publishGate":
            right.append(f'<span class="btn g">{esc(c.get("label"))}</span>')
        else:
            cls = {"primaryButton": "p", "destructiveButton": "d"}.get(k, "")
            perm = f'<small>{esc(c["permission"])}</small>' if c.get("permission") else ""
            (right if cls == "p" else left).append(
                f'<span class="btn {cls}">{esc(c.get("label") or k)}{perm}</span>')
    if not left and not right:
        return ""
    return f'<div class="actbar">{"".join(left)}<span class="spacer"></span>{"".join(right)}</div>'


FORM_KINDS = {"selectField", "textField", "numberField", "datePicker", "toggle", "multiSelect",
              "fileUpload", "signaturePad"}


def frame(screen: dict, plat: dict, facts: dict, overlay: dict | None = None) -> str:
    regions = (screen.get("layout") or {}).get("regions") or []
    sid = screen["id"]
    noun = re.sub(r"[^A-Za-z ]", "", screen["name"]).split()[-1].lower() or "record"
    filters = [c for r in regions if r.get("slot") == "filters" for c in r["components"]]
    actions = [c for r in regions if r.get("name") == "actionBar" for c in r["components"]]
    context = [c for r in regions if r.get("name") == "contextPanel" for c in r["components"]]
    body_comps = [c for r in regions if r.get("name") == "contentBody"
                  and r.get("slot") != "filters" for c in r["components"]]

    main = []
    if filters:
        main.append(filter_bar(filters, facts, sid))
    tiles = [c for c in body_comps if c.get("kind") == "metricTile"]
    if tiles:
        main.append(kpi_row(tiles, facts, sid))
    form = [c for c in body_comps if c.get("kind") in FORM_KINDS]
    if form:
        main.append(form_card(form, facts, sid))
    for c in body_comps:
        if c.get("kind") in ("dataTable", "cardList", "timeline"):
            main.append(data_table(c, facts, sid, rows=5 if tiles else 7))
        elif c.get("kind") not in FORM_KINDS and c.get("kind") != "metricTile":
            main.append(f'<div class="card"><h3>{esc(c.get("label") or c.get("kind"))}</h3>'
                        f'<div class="hint">{esc(clip(c.get("notes"), 220))}</div></div>')

    if not main and not context:
        why = next((g["why"] for g in (screen.get("gaps") or [])
                    if "nothing that can be drawn" in g["why"]), None)
        inner = ('<div class="hollow"><div><b>Nothing to draw.</b><br>'
                 + esc(clip(why, 340) if why else "This screen declares no components.")
                 + "</div></div>")
    else:
        side = f'<div class="side">{"".join(detail_card(c, facts, sid) for c in context)}</div>' \
            if context else ""
        inner = f'<div class="canvas"><div class="main">{"".join(main)}</div>{side}</div>'

    dialog = ""
    if overlay and overlay.get("component") in ("drawer", "sheet"):
        # **The step, and the fact that the screen behind is still the screen.** A drawer in a
        # sequence has to say where in it the operator is, or a reviewer cannot tell a three-step
        # flow from three unrelated panels.
        seq = [o for o in (screen.get("overlays") or []) if o.get("component") == "drawer"]
        step = (f"step {seq.index(overlay) + 1} of {len(seq)} · stays on {screen['name']}"
                if overlay in seq and len(seq) > 1 else f"over {screen['name']}")
        dialog = (f'<div class="scrim"></div><div class="drw">'
                  f'<div class="step">{esc(clip(step, 60))}</div>'
                  f'<b>{esc(overlay.get("trigger") or overlay.get("id"))}</b>'
                  f'<p>{esc(clip(overlay.get("body"), 400))}</p><div class="row">'
                  f'<span class="btn">Close</span>'
                  f'<span class="btn p">Continue</span></div></div>')
    elif overlay:
        trigger = overlay.get("trigger") or overlay.get("id")
        # **The dismiss button cannot be called what the action is called.** `cancelPerformance`
        # gave a dialog with two buttons both reading *Cancel*, one of which cancels the dialog and
        # one of which cancels the performance. The dismissal names what it preserves instead.
        dismiss = "Cancel" if trigger.strip().lower() not in (
            "cancel", "close", "stop", "discard", "reset") else f"Keep this {noun}"
        dialog = (f'<div class="scrim"></div><div class="dlg"><b>{esc(trigger)}?</b>'
                  f'<p>{esc(clip(overlay.get("body"), 280))}</p><div class="row">'
                  f'<span class="btn">{esc(dismiss)}</span>'
                  f'<span class="btn d">{esc(trigger)}</span></div></div>')

    context_line = f"{pick(VENUES, sid)} · Season 2026"
    return (f'<div class="frame"><div class="shell">{rail(screen, plat)}'
            f'<div class="app"><div class="appbar">'
            f'<b>{esc(clip(screen["name"], 54))}</b>'
            f'<s>{esc(context_line)}</s></div>'
            f'{inner}{action_bar(actions)}</div></div>{dialog}</div>')


def block(screen: dict, plat: dict, facts_all: dict) -> str:
    src = screen.get("source") or {}
    facts = facts_all.get((src.get("pack"), str(src.get("number")), str(src.get("page"))),
                          {"examples": [], "statuses": []})
    gaps = screen.get("gaps") or []
    overlays = screen.get("overlays") or []

    tags = [f'<span class="tag a">{esc(screen.get("pattern"))}</span>']
    cols = sum(len(c.get("columns") or [])
               for r in (screen.get("layout") or {}).get("regions") or []
               for c in r.get("components") or [])
    if cols:
        tags.append(f'<span class="tag">{cols} columns</span>')
    if overlays:
        tags.append(f'<span class="tag a">{len(overlays)} overlay'
                    f'{"s" if len(overlays) > 1 else ""}</span>')
    if gaps:
        tags.append(f'<span class="tag w">{len(gaps)} gap{"s" if len(gaps) > 1 else ""}</span>')

    ops = [a.get("operationId") for a in (screen.get("apis") or []) if a.get("operationId")]
    ops_html = (" · ".join(esc(o) for o in ops) if ops
                else '<span class="none">none declared</span>')
    exits = (screen.get("navigation") or {}).get("exitTo") or []
    exits_html = (" · ".join(f'<a href="#{e.lower()}">{esc(e)}</a>' for e in exits[:8])
                  if exits else '<span class="none">nothing declared</span>')

    states_html = " &middot; ".join(esc(s) for s in (screen.get("states") or {}))
    out = [f'<div class="scr" id="{esc(screen["id"].lower())}" '
           f'data-screen-id="{esc(screen["id"])}">',
           f'<div><div class="hd"><span class="id">{esc(screen["id"])}</span>'
           f'<span class="nm">{esc(screen["name"])}</span>{"".join(tags)}</div>'
           f'<div class="sub">{esc(clip(screen.get("purpose"), 260))}</div></div>',
           frame(screen, plat, facts),
           f'<div class="foot">'
           f'<div><b>OPERATIONS</b> &middot; {ops_html}</div>'
           f'<div><b>STATES</b> &middot; {states_html}</div>'
           f'<div><b>GOES TO</b> &middot; {exits_html}</div>'
           f'<div><b>PATTERN</b> &middot; {esc(clip(screen.get("patternReason"), 190))}</div>'
           f'<div><b>SOURCE</b> &middot; {esc(src.get("pack", "—"))} p{esc(src.get("page"))}</div>'
           f'</div>']
    for g in gaps:
        out.append(f'<div class="gap"><i></i><div>{esc(clip(g["why"], 420))}</div></div>')
    for ov in overlays:
        out.append(f'<div class="hd" style="margin-top:16px">'
                   f'<span class="id">{esc(screen["id"])}</span>'
                   f'<span class="nm">{esc(screen["name"])} — {esc(ov.get("trigger"))}</span>'
                   f'<span class="tag a">overlay</span></div>'
                   f'<div class="sub">{esc(clip(ov.get("body"), 240))}</div>')
        out.append(frame(screen, plat, facts, ov))
    out.append("</div>")
    return "".join(out)


# --------------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True)
    ap.add_argument("--module")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    path = next(SCREENS.glob(f"{args.platform}-*.yaml"))
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    plat = doc["platform"]
    screens = [s for s in doc["screens"] if not args.module or s.get("module") == args.module]
    if args.limit:
        screens = screens[: args.limit]

    t = tokens()
    facts = pack_facts()
    n_ov = sum(len(s.get("overlays") or []) for s in screens)
    n_gap = sum(1 for s in screens if s.get("gaps"))
    n_hollow = sum(1 for s in screens
                   if not ((s.get("layout") or {}).get("regions") or []))
    n_bound = sum(1 for s in screens for r in (s.get("layout") or {}).get("regions") or []
                  for c in r.get("components") or [] for col in c.get("columns") or []
                  if bound(col))
    n_cols = sum(len(c.get("columns") or []) for s in screens
                 for r in (s.get("layout") or {}).get("regions") or []
                 for c in r.get("components") or [])
    toc = " &middot; ".join(f'<a href="#{s["id"].lower()}">{esc(s["id"])}</a>' for s in screens)

    body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(plat['code'])} {esc(args.module or plat['shortName'])} — generated wireframes</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css(t)}</style></head><body><div class="wrap">

<div class="mast">
  <div>
    <div class="mark">TICVAI</div>
    <h1>{esc(plat['code'])} {esc(args.module or plat['shortName'])} — generated from the specification
      <span>({len(screens)} screens &middot; {len(screens) + n_ov} frames)</span></h1>
  </div>
  <div class="meta">
    <div>{esc(plat.get('app'))} &middot; {esc(plat.get('audience'))} &middot; {esc(plat.get('formFactor'))}</div>
    <div>{FRAME_W} &times; {FRAME_H} frames &middot; tokens from screens/_design-tokens.yaml</div>
  </div>
</div>

<p class="lede"><b>Nothing on this page was drawn by hand.</b> Every frame is derived from
<code>screens/{esc(path.name)}</code> and <code>screens/_design-tokens.yaml</code> — the column
headers are the columns the screens declare, the buttons are the actions their source names, and
each of the {n_ov} overlays is drawn as its own frame over the screen that raises it. Of
{n_cols} declared columns, <b>{n_bound} resolve to a contract field</b> and render in the accent
colour; the rest are a source label with nothing behind them yet and render grey.</p>

<div class="call"><i></i><div><b>The values in the cells are illustration, not data.</b> They come
from each screen's own worked examples and lifecycle vocabulary in the workshop pack where it has
them, and from the column's name where it does not — a column called <i>Requested date</i> renders
a date, one called <i>Margin impact</i> renders money. They are deterministic, so two runs produce
identical output and a diff means a real change. <b>{n_gap} screens carry a recorded gap</b>, and
it is printed in full under the frame rather than summarised.</div></div>

<p class="toc">{toc}</p>

{"".join(block(s, plat, facts) for s in screens)}
</div></body></html>"""

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = f"{plat['code']}-{(args.module or plat['shortName']).replace(' ', '-')}-wireframes.html"
    (out / name).write_text(body.encode("utf-8", "ignore").decode("utf-8"), encoding="utf-8")
    print(f"{len(screens)} screens + {n_ov} overlay frames = {len(screens) + n_ov} frames")
    print(f"{n_bound} of {n_cols} columns render as bound")
    print(f"written: {out / name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
