#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw the state frames the client-approved prototypes never drew, in each app's approved look (r9).

**21 October 2026, CHG-R9UI-005.** The r9 UI lane mapped every state of the 158 client-verified screens to what the
approved prototypes draw (screens/_state-patterns.yaml) and found 290 states the prototypes never drew, which it put on
the left-out list as questions for the client. The lead: "290 of them were ingested and never built we need to built
them for r9." So the package draws them: one frame per platform and state class, in that platform's approved visual
language -- its prototype's CSS variables (handoff/design-tokens/guest-web.yaml, guest-app.yaml; the till's root
variables), type, colours, spacing, components and copy tone -- reusing the components the prototypes do draw (the
WEB-029 status card, the paused action button, the guest app's dashed note and mascot, the till's toast, its hardware
alert panel with Retry and Report, its supervisor PIN cells, its shimmer).

Each frame is honest about what it is: **drawn by the package from the approved design (r9), not yet seen by the
client**. The lead decided to build them; they go to the client at the next review all the same. Copy reuses the
approved copy where the prototype has it and follows the app's tone where it does not; nothing on an approved screen
changes (these are states the approved screens never showed).

Writes three companion boards under wireframes/states/, one per platform, in the frame structure the boards use
(`<section id="<anchor>">` per frame; the board's one <style> block carries the tokens and components, so
viewer/lib/wireframes.mjs frameDocument lifts a frame whole). Self-contained: inline CSS, the mascots embedded,
fonts named with local fallbacks, no network. Guest web is drawn at 1440 x 900 and 390 x 844 (and the phone again
right to left), the guest app at 390 x 844 (and right to left), the till at 1620 x 1080. Layout uses logical
properties, so `dir="rtl"` mirrors every frame.

Run by hand when a frame changes (it is a drawing, reviewed like one; refresh.sh excuses it). Deterministic: the same
inputs give the same bytes. screens/_state-patterns.yaml points each state at its frame; tools/derive-state-views.py
then writes the screens' wireframe.stateViews and handoff/design-frames.json.

    python3 tools/draw-state-frames.py
"""
from __future__ import annotations

import base64
import html
import io
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "wireframes" / "states"
IMG = ROOT / "sources" / "designs" / "guest-rev3-28-september" / "images"
STATUS = "drawn by the package from the approved design (r9), not yet seen by the client"


def esc(s):
    return html.escape(str(s), quote=True)


def mascot(name, height=132):
    """A prototype mascot, scaled down and embedded (no network, no file beside the board)."""
    from PIL import Image
    im = Image.open(IMG / name).convert("RGBA")
    w = max(1, round(im.width * height / im.height))
    im = im.resize((w, height), getattr(Image, "Resampling", Image).LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=False)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def tokens_of(rel):
    return yaml.safe_load((ROOT / rel).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------- the board shell
BOARD_CSS = """
*{box-sizing:border-box}
body{margin:0;background:#EEF0F3;color:#1a1917;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;font-size:13px}
.board{padding:28px 34px 80px;max-width:none}
.board>h1{font:600 22px/1.2 system-ui,sans-serif;margin:0 0 6px}
.board>p.lede{max-width:980px;margin:0 0 26px;color:#4b4b4b;line-height:1.55}
.state-frame{margin:0 0 56px;padding:20px 22px 26px;background:#fff;border:1px solid #dcdfe4;border-radius:14px}
.state-frame>header{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:baseline;margin:0 0 6px}
.state-frame>header h2{font:600 17px/1.25 system-ui,sans-serif;margin:0}
.state-frame>header code{font:12px ui-monospace,monospace;color:#5a6577;background:#f2f4f7;padding:2px 7px;border-radius:6px}
.state-frame .status{display:inline-block;font:600 11px/1 system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;
  color:#8A6D00;background:#FFF7E6;border:1px solid #F1D9A6;padding:5px 8px;border-radius:6px}
.state-frame .note{margin:6px 0 16px;max-width:1100px;color:#4b4b4b;line-height:1.55;font-size:13px}
.arts{display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start}
.art{flex:0 0 auto;position:relative;overflow:hidden;border:1px solid #d5d8de;box-shadow:0 18px 40px -24px rgba(0,0,0,.35)}
.art-cap{font:600 11px/1 system-ui,sans-serif;color:#6b7280;letter-spacing:.04em;margin:0 0 8px}
"""


def board(title, lede, css, frames, lang="en"):
    body = "".join(frames)
    return ("<!doctype html>\n<html lang=\"" + lang + "\"><head><meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{esc(title)}</title>\n<style>{BOARD_CSS}{css}</style></head>\n"
            f"<body><div class=\"board\"><h1>{esc(title)}</h1><p class=\"lede\">{lede}</p>\n{body}</div></body></html>\n")


def frame(anchor, pattern, title, states, based, note, arts):
    cells = "".join(f'<div><div class="art-cap">{esc(cap)}</div>{a}</div>' for cap, a in arts)
    return (f'<section id="{anchor}" class="state-frame" data-pattern="{esc(pattern)}" data-states="{esc(" ".join(states))}" '
            f'data-status="{esc(STATUS)}">\n<header><h2>{esc(title)}</h2><code>{esc(pattern)}</code>'
            f'<code>states: {esc(", ".join(states))}</code><span class="status">{esc(STATUS)}</span></header>\n'
            f'<p class="note"><b>Built from:</b> {based} {note}</p>\n<div class="arts">{cells}</div>\n</section>\n')


# ================================================================================================= P01 guest web
def web_css(t):
    v = lambda k: t["tokens"][k]["default"]  # noqa: E731
    return f"""
.gw{{--brand:{v('--brand')};--accent:{v('--accent')};--bg:{v('--bg')};--surface:{v('--surface')};--surface-2:{v('--surface-2')};
  --ink:{v('--ink')};--ink-2:{v('--ink-2')};--ink-3:{v('--ink-3')};--line:{v('--line')};--tint:rgba(192,124,30,.1);--r:{v('--r')};
  --r-sm:{v('--r-sm')};--btn-r:{v('--btn-r')};--sh-md:{v('--sh-md')};--sp3:24px;--sp4:36px;--bad:#c0392b;--badtint:rgba(192,57,43,.08);
  --font-h:'Archivo','IBM Plex Sans',system-ui,sans-serif;--font-b:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  background:var(--bg);color:var(--ink);font-family:var(--font-b);font-size:15px;line-height:1.5;display:flex;flex-direction:column}}
.gw .hdr{{flex:0 0 auto;display:flex;align-items:center;gap:22px;padding:14px 28px;background:var(--surface);border-block-end:1px solid var(--line)}}
.gw .mark{{display:flex;align-items:center;gap:10px}}
.gw .mark i{{width:32px;height:32px;border-radius:6px;background:var(--brand);color:#fff;display:grid;place-items:center;font:700 15px var(--font-h);font-style:normal}}
.gw .mark b{{font:600 16px var(--font-h);letter-spacing:-.01em}}
.gw .nav{{display:flex;gap:6px}}
.gw .nav span{{padding:8px 13px;border-radius:999px;color:var(--ink-2);font-weight:500;font-size:14px}}
.gw .nav span.on{{background:var(--tint);color:var(--brand)}}
.gw .tools{{margin-inline-start:auto;display:flex;align-items:center;gap:10px}}
.gw .pill{{height:40px;padding:0 13px;display:flex;align-items:center;gap:6px;border-radius:999px;border:1.5px solid var(--line);font-weight:600;font-size:12.5px}}
.gw .acct{{width:40px;height:40px;border-radius:999px;background:var(--brand);color:#fff;display:grid;place-items:center}}
.gw .menu{{width:40px;height:40px;border-radius:10px;border:1.5px solid var(--line);display:grid;place-items:center}}
.gw main{{flex:1 1 auto;padding:var(--sp4) var(--sp3) 48px;overflow:hidden}}
.gw .col{{max-width:640px;margin:0 auto;display:flex;flex-direction:column;gap:var(--sp3)}}
.gw .wide{{max-width:1040px;margin:0 auto;display:flex;flex-direction:column;gap:20px}}
.gw .ftr{{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:8px 22px;padding:18px 28px;border-block-start:1px solid var(--line);background:var(--surface);color:var(--ink-2);font-size:13px}}
.gw .ftr b{{color:var(--ink)}}
.gw .card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:var(--sp4) var(--sp3);text-align:center;display:flex;flex-direction:column;align-items:center;gap:14px;box-shadow:var(--sh-md)}}
.gw .ring{{width:60px;height:60px;border-radius:999px;background:var(--tint);display:grid;place-items:center}}
.gw .kick{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--brand);font-weight:700}}
.gw h1,.gw h2,.gw h3{{font-family:var(--font-h);font-weight:600;letter-spacing:-.02em;margin:0}}
.gw h1{{font-size:30px}} .gw h2{{font-size:26px}} .gw h3{{font-size:17px;letter-spacing:-.01em}}
.gw .body{{margin:0;max-width:46ch;color:var(--ink-2);font-size:14.5px;line-height:1.6}}
.gw .advice{{width:100%;background:var(--surface-2);border-radius:var(--r-sm);padding:13px 15px;display:flex;flex-wrap:wrap;align-items:center;gap:10px;text-align:start}}
.gw .advice b{{flex:0 0 auto;white-space:nowrap;padding:5px 11px;border-radius:999px;background:var(--brand);color:#fff;font-size:12px}}
.gw .advice span{{flex:1 1 220px;font-size:13px;color:var(--ink-2)}}
.gw .btns{{display:flex;flex-wrap:wrap;gap:9px;justify-content:center}}
.gw .btn{{padding:12px 22px;border-radius:var(--btn-r);background:var(--brand);color:#fff;border:1.5px solid var(--brand);font-weight:600;font-size:14px}}
.gw .btn.ghost{{background:transparent;color:var(--ink);border-color:var(--line)}}
.gw .btn.off{{background:var(--surface-2);color:var(--ink-3);border-color:var(--line)}}
.gw .ref{{font:11.5px ui-monospace,monospace;color:var(--ink-3)}}
.gw .alert{{display:flex;gap:12px;align-items:flex-start;text-align:start;padding:13px 15px;border-radius:var(--r-sm);border:1.5px solid var(--bad);background:var(--badtint)}}
.gw .alert i{{flex:0 0 auto;width:22px;height:22px;border-radius:999px;background:var(--bad);color:#fff;display:grid;place-items:center;font:700 13px var(--font-h);font-style:normal}}
.gw .alert p{{margin:0;font-size:13.5px;color:var(--ink)}}
.gw .alert p small{{display:block;color:var(--ink-2);font-size:12.5px;margin-top:3px}}
.gw .field{{display:flex;flex-direction:column;gap:6px;text-align:start}}
.gw .field label{{font-size:12.5px;font-weight:600;color:var(--ink-2)}}
.gw .field div{{height:46px;border-radius:var(--r-sm);border:1.5px solid var(--line);background:var(--surface);padding:0 14px;display:flex;align-items:center;color:var(--ink-2)}}
.gw .field.bad div{{border-color:var(--bad)}}
.gw .chips{{display:flex;flex-wrap:wrap;gap:8px}}
.gw .chip{{padding:8px 13px;border-radius:999px;border:1.5px solid var(--line);background:var(--surface);font-size:13px;font-weight:600;color:var(--ink-2)}}
.gw .chip.on{{background:var(--brand);border-color:var(--brand);color:#fff}}
.gw .chip.full{{border-style:dashed;color:var(--ink-3)}}
.gw .chip small{{display:block;font-weight:500;font-size:11px}}
.gw .banner{{flex:0 0 auto;display:flex;align-items:center;gap:12px;padding:11px 28px;background:var(--ink);color:#fff;font-size:13.5px}}
.gw .banner i{{width:8px;height:8px;border-radius:999px;background:#E0A82E;flex:0 0 auto}}
.gw .banner small{{margin-inline-start:auto;color:rgba(255,255,255,.7)}}
.gw .tile{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px 20px;display:flex;flex-direction:column;gap:10px;text-align:start}}
.gw .stale{{font-size:12px;color:var(--ink-3)}}
.gw .note{{padding:13px 16px;border:1.5px dashed var(--line);border-radius:var(--r);font-size:13.5px;color:var(--ink-2);text-align:start}}
.gw .notice{{display:flex;gap:12px;align-items:flex-start;padding:14px 16px;border-radius:var(--r);background:var(--tint);border:1px solid var(--brand);text-align:start}}
.gw .notice b{{display:block;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--brand);margin-bottom:4px}}
.gw .notice p{{margin:0;font-size:13.5px;color:var(--ink)}}
.gw .row{{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-block-end:1px solid var(--line);font-size:14px}}
.gw .row:last-child{{border:0}}
.gw .muted{{color:var(--ink-3)}}
"""


GUEST_NAV = ["Discover", "What's on", "Book", "At the venue", "My tickets", "Help"]


def web_page(content, mobile=False, active=None, banner="", rtl=False):
    w, h = (390, 844) if mobile else (1440, 900)
    nav = "" if mobile else '<div class="nav">' + "".join(
        f'<span class="{"on" if n == active else ""}">{esc(n)}</span>' for n in GUEST_NAV) + "</div>"
    tools = ('<div class="tools"><div class="menu">' + ICON["menu"] + '</div></div>' if mobile else
             '<div class="tools"><div class="pill">' + ICON["globe"] + 'العربية</div><div class="acct">'
             + ICON["user"] + '</div></div>')
    ftr = ("" if mobile else '<div class="ftr"><b>Summit Peaks</b><span>Contact &amp; venue info</span>'
           '<span>Accessibility</span><span>Terms of sale</span><span>Privacy</span><span>Service status</span></div>')
    return (f'<div class="art gw" dir="{"rtl" if rtl else "ltr"}" style="width:{w}px;height:{h}px">'
            f'<div class="hdr"><div class="mark"><i>S</i><b>Summit Peaks</b></div>{nav}{tools}</div>'
            f'{banner}<main>{content}</main>{ftr}</div>')


ICON = {
    "menu": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "globe": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20a15 15 0 0 1 0-20Z"/></svg>',
    "user": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
    "clock": '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="var(--brand,#c07c1e)" stroke-width="2.1" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "car": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 17h14l-1.5-6.5A2 2 0 0 0 15.6 9H8.4a2 2 0 0 0-1.9 1.5Z"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/></svg>',
    "wifi-off": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 3l18 18"/><path d="M5 12a9 9 0 0 1 12-3M8 16a5 5 0 0 1 6-1"/><path d="M12 20h.01"/></svg>',
    "pin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 22s7-7.5 7-13a7 7 0 0 0-14 0c0 5.5 7 13 7 13Z"/><circle cx="12" cy="9" r="2.5"/></svg>',
    "lock": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>',
    "alert": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>',
    "download": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>',
}


def web_frames(t):
    f = []
    # 1. closed: the WEB-029 status card, its fourth variant
    def closed(mobile):
        card = ('<div class="col"><div class="card"><span class="ring">' + ICON["clock"] + '</span>'
                '<div class="kick">Closed</div><h1 style="font-size:' + ('24px' if mobile else '30px') + '">Summit Peaks is closed today</h1>'
                '<p class="body">We are not open on Monday 5 October. Tickets for other days still work, and you can book any open day.</p>'
                '<div class="advice"><b>Opens tomorrow</b><span>Tuesday 10:00 to 20:00. Gates open 30 minutes earlier.</span></div>'
                '<div class="btns"><span class="btn">See opening times</span><span class="btn ghost">Back to home</span></div>'
                '<span class="ref">Ref TCV-STATUS-CLOSED-0510</span></div></div>')
        return web_page(card, mobile)
    f.append(frame("web-state-closed", "P01/state-closed", "Venue closed (WEB-029, the status card's closed variant)",
                   ["closed"], "the WEB-029 status card (prototype lines 4746-4782, frame #web-029): the same card, ring, "
                   "kicker, title, body, advice row with its pill, two buttons and reference; the clock icon in the ring.",
                   "The title and body carry the tenant's availabilityMessage; the advice row gives the opening hours "
                   "from the venue's contact (getTenantAppStatus, decided 28 September, audit R073 (f)).",
                   [("1440 x 900", closed(False)), ("390 x 844", closed(True))]))

    # 2. preference not at venue: the Visit Planner day with its banner
    def pref(mobile):
        chips = ('<div class="chips"><span class="chip on">Family rides</span><span class="chip on">Shows</span>'
                 '<span class="chip full">Seafood<small>Not at the parks you chose · at Coastal Aqua</small></span>'
                 '<span class="chip">Shopping</span></div>')
        day = ('<div class="tile"><div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px">'
               '<h3>Saturday · Summit Peaks</h3><span class="muted" style="font-size:13px">10:00 to 18:00</span></div>'
               '<div class="notice"><span style="flex:0 0 auto;color:var(--brand)">' + ICON["pin"] + '</span><div><b>Not at this park</b>'
               '<p>Seafood is not served at Summit Peaks, so it is not in this day. Coastal Aqua has it: move this day there to bring it in.</p></div></div>'
               '<div class="row"><span>10:15 · Junior Circuit</span><span class="muted">5 min queue</span></div>'
               '<div class="row"><span>12:30 · Lunch at The Crater Grill</span><span class="muted">Grill</span></div>'
               '<div class="row"><span>14:00 · Falcon Drop</span><span class="muted">From 1.20 m</span></div>'
               '<div class="btns" style="justify-content:flex-start"><span class="btn">Change answers</span><span class="btn ghost">Book this plan</span></div></div>')
        return web_page('<div class="wide"><div><div class="kick">Plan your visit</div><h2>Your plan</h2></div>' + chips + day + '</div>',
                        mobile, active="Book")
    f.append(frame("web-state-preference-not-at-venue", "P01/state-preference-not-at-venue",
                   "A preference the day's park cannot meet (WEB-050 Plan Your Visit)", ["preferenceNotAtVenue"],
                   "the Visit Planner's plan view (TICVAI Visit Planner.dc.html, frame #web-050): its day card, rows and "
                   "Change answers / Book this plan buttons; the chip row and the tinted notice of the booking engine "
                   "(prototype line 619, the existing-guest notice).",
                   "Before Make my plan the chip says Not at the parks you chose and names the park that has it; after it, "
                   "the day shows the Not at this park notice and nothing from another park is placed (MoM 30 September, 4.7).",
                   [("1440 x 900", pref(False)), ("390 x 844", pref(True))]))

    # 3. sign-in refused: one message for every refusal, then too many attempts
    def refused(mobile, locked=False):
        alert = ('<div class="alert"><i>!</i><p>Too many attempts. Try again in 15 minutes, or sign in with a code instead.'
                 '<small>We sent nothing yet: choose Send me a code.</small></p></div>' if locked else
                 '<div class="alert"><i>!</i><p>That did not work. Check your email and password and try again.'
                 '<small>Forgotten your password? Sign in with a code instead.</small></p></div>')
        form = ('<div class="col"><div class="card" style="text-align:start;align-items:stretch"><h2 style="font-size:24px">'
                'Sign in to book faster</h2>' + alert +
                '<div class="field' + ('' if locked else ' bad') + '"><label>Email</label><div>layla@example.com</div></div>'
                '<div class="field' + ('' if locked else ' bad') + '"><label>Password</label><div>••••••••••</div></div>'
                '<div class="btns" style="justify-content:flex-start">' +
                ('<span class="btn">Send me a code</span><span class="btn off">Sign in</span>' if locked else
                 '<span class="btn">Sign in</span><span class="btn ghost">Send me a code</span>') +
                '</div></div></div>')
        return web_page(form, mobile)
    f.append(frame("web-state-sign-in-refused", "P01/state-sign-in-refused", "Sign-in refused (WEB-016 Login / Register)",
                   ["signInRefused"], "the prototype's sign-in sheet (title \"Sign in to book faster\", line 10557) and its "
                   "declined-payment notice (the ! glyph on #c0392b, lines 6550-6552), on the status card's surface.",
                   "One message for every refusal: the screen never says whether the password, the identifier or the "
                   "account was wrong. Too many attempts says to try later and offers Send me a code (decided 28 September, "
                   "audit R073 (a)).",
                   [("1440 x 900 · a refusal", refused(False)), ("390 x 844 · too many attempts", refused(True, True))]))

    # 4. parking sold out for the day
    def parking(mobile):
        days = ('<div class="chips"><span class="chip">Fri 2</span><span class="chip on">Sat 3<small>Full</small></span>'
                '<span class="chip">Sun 4</span><span class="chip">Mon 5</span></div>')
        body = ('<div class="wide" style="max-width:720px"><div><div class="kick">At the venue</div><h2>Parking: reserve and pay</h2></div>'
                '<div class="tile"><div style="display:flex;gap:10px;align-items:center">' + ICON["car"] +
                '<h3>Car park East · four minutes from Gate C</h3></div>' + days +
                '<div class="alert"><i>!</i><p>The car park is full on Sat 3 Oct.<small>Choose another day for parking. '
                'Your tickets are not affected.</small></p></div>'
                '<div class="btns" style="justify-content:flex-start"><span class="btn off">Reserve and pay</span>'
                '<span class="btn ghost">Choose another day</span></div></div></div>')
        return web_page(body, mobile, active="At the venue")
    f.append(frame("web-state-sold-out-for-day", "P01/state-sold-out-for-day", "Parking full for the chosen day (WEB-041)",
                   ["soldOutForDay"], "the Parking module of At the venue (WEB-041, frame #web-041): its tile, the day "
                   "chips of the booking engine, the Reserve and pay button; the refusal notice of the sign-in frame.",
                   "Shown only when addCartLine refuses the line with soldOutForDay: there is no live space count in the "
                   "first release, so no other day is promised spaces (decided 28 September, audit R166).",
                   [("1440 x 900", parking(False)), ("390 x 844", parking(True))]))

    # 5. offline: the banner the prototype words and never drew, with the paused buttons it draws
    banner = ('<div class="banner"><i></i>' + ICON["wifi-off"] + '<span>You\'re offline. Connect to the internet to book, '
              'pay, order or join a queue.</span><small>Showing what loaded at 10:42</small></div>')

    def offline(mobile, rtl=False):
        body = ('<div class="wide" style="max-width:720px"><div><div class="kick">Union Arena · Round 4</div><h2>Choose your seats</h2>'
                '<span class="stale">Seat availability as of 10:42</span></div>'
                '<div class="tile"><div class="row"><span>Lower Tier · Row F · Seats 12-13</span><span>AED 490</span></div>'
                '<div class="row"><span>Held for you until 10:51</span><span class="muted">2 seats</span></div>'
                '<div class="btns" style="justify-content:flex-start"><span class="btn off">Offline — booking is paused</span></div></div>'
                '<div class="note">Seats are held for six minutes once selected. Your hold is kept while you reconnect.</div></div>')
        return web_page(body, mobile, active="Book", banner=banner, rtl=rtl)
    f.append(frame("web-state-offline", "P01/state-offline", "Offline: the banner, and the paused actions",
                   ["offline"], "the prototype's offline message, word for word (\"You're offline. Connect to the internet "
                   "to book, pay, order or join a queue.\", line 6522, which no markup drew), set as a dark bar under the "
                   "header in the ink colour; the paused action button the prototype draws (\"Offline — booking is "
                   "paused\", line 6227).",
                   "What was already loaded stays, marked with its age; anything that spends money, holds capacity or "
                   "changes the account waits, and its button says so. The banner is the part the prototype never drew.",
                   [("1440 x 900", offline(False)), ("390 x 844", offline(True)), ("390 x 844 · right to left", offline(True, True))]))
    return f


# ================================================================================================= P02 guest app
def app_css(t, sad, thinking):
    v = {k: x["default"] for k, x in t["sources"][0]["tokens"].items()}
    return f"""
.ga{{--bg:{v['--bg']};--sf:{v['--sf']};--ink:{v['--ink']};--ink2:{v['--ink2']};--ink3:{v['--ink3']};--ln:{v['--ln']};--ln2:{v['--ln2']};
  --deep:{v['--deep']};--br:{v['--br']};--rk:1;--bad:#c0392b;--badtint:rgba(192,57,43,.08);
  --fh:'Archivo','IBM Plex Sans',system-ui,sans-serif;--fb:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  width:390px;height:844px;border-radius:44px;background:var(--bg);color:var(--ink);font-family:var(--fb);font-size:14px;
  display:flex;flex-direction:column;border:1px solid #e3def0}}
.ga .sb{{flex:0 0 auto;height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;font:600 14px var(--fb)}}
.ga .top{{flex:0 0 auto;display:flex;align-items:center;gap:12px;padding:6px 18px 12px}}
.ga .top i{{width:38px;height:38px;border-radius:calc(var(--rk)*12px);background:var(--sf);border:1px solid var(--ln);display:grid;place-items:center;font-style:normal}}
.ga .top b{{font:600 19px var(--fh);letter-spacing:-.015em}}
.ga .scroll{{flex:1 1 auto;overflow:hidden;padding:4px 18px 18px;display:flex;flex-direction:column;gap:14px}}
.ga .tabs{{flex:0 0 auto;height:84px;display:flex;justify-content:space-around;align-items:flex-start;padding-top:12px;background:var(--sf);border-block-start:1px solid var(--ln);font-size:11px;color:var(--ink3);font-weight:600}}
.ga .tabs span{{display:flex;flex-direction:column;align-items:center;gap:5px}}
.ga .tabs span::before{{content:"";width:22px;height:22px;border-radius:7px;background:var(--ln)}}
.ga .tabs span.on{{color:var(--br)}} .ga .tabs span.on::before{{background:var(--br)}}
.ga h2,.ga h3{{font-family:var(--fh);font-weight:600;letter-spacing:-.015em;margin:0}} .ga h2{{font-size:22px}} .ga h3{{font-size:16px}}
.ga p{{margin:0}}
.ga .card{{background:var(--sf);border:1px solid var(--ln);border-radius:calc(var(--rk)*18px);padding:16px;display:flex;flex-direction:column;gap:10px}}
.ga .dash{{padding:16px;border-radius:calc(var(--rk)*16px);background:var(--sf);border:1.5px dashed var(--ln);color:var(--ink2);font-size:13.5px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}}
.ga .mascot{{width:96px;height:96px;background-size:contain;background-repeat:no-repeat;background-position:center bottom}}
.ga .m-sad{{background-image:url({sad})}} .ga .m-think{{background-image:url({thinking})}}
.ga .btn{{min-height:48px;border-radius:calc(var(--rk)*14px);background:var(--br);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:15px;padding:0 18px}}
.ga .btn.deep{{background:var(--deep)}} .ga .btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid var(--ln)}}
.ga .btn.off{{background:var(--ln2);color:var(--ink3)}}
.ga .muted{{color:var(--ink3);font-size:12.5px}}
.ga .alert{{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border-radius:calc(var(--rk)*14px);border:1.5px solid var(--bad);background:var(--badtint);font-size:13.5px}}
.ga .alert i{{flex:0 0 auto;width:22px;height:22px;border-radius:999px;background:var(--bad);color:#fff;display:grid;place-items:center;font:700 13px var(--fh);font-style:normal}}
.ga .alert small{{display:block;color:var(--ink2);font-size:12.5px;margin-top:3px}}
.ga .field{{display:flex;flex-direction:column;gap:6px}} .ga .field label{{font-size:12.5px;font-weight:600;color:var(--ink2)}}
.ga .field div{{height:48px;border-radius:calc(var(--rk)*14px);border:1.5px solid var(--ln);background:var(--sf);padding:0 14px;display:flex;align-items:center;color:var(--ink2)}}
.ga .field.bad div{{border-color:var(--bad)}}
.ga .chips{{display:flex;flex-wrap:wrap;gap:8px}}
.ga .chip{{padding:8px 12px;border-radius:999px;background:var(--sf);border:1.5px solid var(--ln);font-size:12.5px;font-weight:600;color:var(--ink2)}}
.ga .chip.on{{background:var(--br);border-color:var(--br);color:#fff}} .ga .chip.out{{border-style:dashed;color:var(--ink3)}}
.ga .chip small{{display:block;font-weight:500;font-size:10.5px}}
.ga .offbar{{margin:0 18px 6px;display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:calc(var(--rk)*14px);background:var(--deep);color:#fff;font-size:12.5px}}
.ga .offbar i{{width:8px;height:8px;border-radius:999px;background:#E0A82E}}
.ga .row{{display:flex;justify-content:space-between;gap:10px;padding:9px 0;border-block-end:1px solid var(--ln2);font-size:13.5px}} .ga .row:last-child{{border:0}}
.ga .note{{display:flex;gap:10px;align-items:center;padding:12px 14px;border-radius:calc(var(--rk)*16px);background:var(--ln2);font-size:13px;color:var(--ink2)}}
.ga .hero{{border-radius:calc(var(--rk)*20px);background:var(--deep);color:#fff;padding:22px 18px;display:flex;flex-direction:column;gap:8px}}
.ga .hero small{{color:#c8b8ff;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700}}
.ga .map{{position:relative;height:430px;border-radius:calc(var(--rk)*20px);overflow:hidden;background:#eef1e8;border:1px solid var(--ln)}}
"""


APP_TABS = ["Home", "Explore", "Buy", "Plan", "Tickets"]


def phone(title, content, tab=None, rtl=False, back=True, pre=""):
    tabs = '<div class="tabs">' + "".join(f'<span class="{"on" if x == tab else ""}">{esc(x)}</span>' for x in APP_TABS) + "</div>"
    top = (f'<div class="top">{"<i>‹</i>" if back else ""}<b>{esc(title)}</b></div>' if title else "")
    return (f'<div class="art ga" dir="{"rtl" if rtl else "ltr"}"><div class="sb"><span>9:41</span><span>●●● ▮</span></div>'
            f'{pre}{top}<div class="scroll">{content}</div>{tabs}</div>')


def app_frames(t):
    f = []
    # 1. error
    def err(rtl=False):
        c = ('<div class="dash" style="margin-top:40px;padding:26px 18px"><div class="mascot m-sad"></div>'
             '<h3>We couldn\'t load what\'s on</h3><p>Something went wrong on our side. Your bag is safe and nothing was charged.</p>'
             '<span class="muted">Problems like this usually clear within a minute.</span></div>'
             '<span class="btn">Try again</span><span class="muted" style="text-align:center;font-family:ui-monospace,monospace">Ref TCV-GA-7F3A-1042</span>')
        return phone("Buy tickets", c, "Buy", rtl)
    f.append(frame("gst-state-error", "P02/state-error", "A read failed (every guest app screen)", ["error"],
                   "the app's dashed empty note with the mascot (Mobile App v4 lines 909 and 2604, \"Nothing saved yet\"), "
                   "the mascot's sad pose (mascot2-sad), the primary button; the web status card's copy (\"Your basket is "
                   "safe and nothing was charged\", \"Problems like this usually clear within a minute\") in the app's words.",
                   "The title names the read that failed (here, what's on); what was on screen stays; one way onward.",
                   [("390 x 844", err()), ("390 x 844 · right to left", err(True))]))

    # 2. offline
    def off(rtl=False):
        pre = '<div class="offbar"><i></i><span>You\'re offline · showing what was saved at 10:42</span></div>'
        c = ('<div class="card"><h3>Day pass · Summit Peaks</h3><span class="muted">Prices as of 10:42</span>'
             '<div class="row"><span>Adult</span><span>AED 325</span></div><div class="row"><span>Junior</span><span>AED 265</span></div></div>'
             '<div class="note">Your tickets and QR codes still work at the gate without a signal.</div>'
             '<span class="btn off">Offline — booking is paused</span>')
        return phone("Buy tickets", c, "Buy", rtl, pre=pre)
    f.append(frame("gst-state-offline", "P02/state-offline", "Offline (every guest app screen)", ["offline"],
                   "the web prototype's offline message and paused button, in the app's deep colour and radius; the "
                   "Booking Mobile v2 note \"Works without a signal\" (line 1191) for what still works.",
                   "What was loaded stays, marked with its age; booking, paying and changing the account wait, and their "
                   "buttons say so.", [("390 x 844", off()), ("390 x 844 · right to left", off(True))]))

    # 3. GST-047: sold out today, closed, update required
    def unavailable(kind):
        if kind == "sold":
            c = ('<div class="hero"><small>Sold out</small><h2 style="color:#fff">Sold out today</h2><p>Every session on Sat 3 Oct '
                 'has gone. Returned tickets are released as they come in.</p></div><span class="btn">Choose another day</span>'
                 '<div class="note">Already have tickets? They still work at the gate.</div>')
        elif kind == "closed":
            c = ('<div class="hero"><small>Closed</small><h2 style="color:#fff">Closed today</h2><p>Summit Peaks is not open on '
                 'Monday 5 October.</p></div><div class="card"><h3>Opening hours</h3><div class="row"><span>Tue to Thu</span>'
                 '<span>10:00 to 20:00</span></div><div class="row"><span>Fri to Sun</span><span>10:00 to 22:00</span></div></div>')
        else:
            c = ('<div class="hero"><small>Update required</small><h2 style="color:#fff">Update TICVAI to keep booking</h2>'
                 '<p>This version is too old to book or pay safely.</p></div><span class="btn deep">' + ICON["download"] +
                 '&nbsp;Open the App Store</span>')
        return phone("", c, None, back=False)
    f.append(frame("gst-state-unavailable", "P02/state-unavailable", "Sold out today, closed, update required (GST-047)",
                   ["soldOut", "closed", "forcedUpgrade"], "GST-047's approved maintenance page (Booking Mobile v2 line 1175, "
                   "frame #gst-047): the hero block with its kicker, title and line, and the note under it; the web status "
                   "card's sold-out copy.",
                   "Each from getTenantAppStatus: soldOut and closed carry the tenant's availabilityMessage (and closed the "
                   "opening hours), and offer another day; update required offers only the store link (decided 28 "
                   "September, audit R073 (b), (f)).",
                   [("390 x 844 · sold out", unavailable("sold")), ("390 x 844 · closed", unavailable("closed")),
                    ("390 x 844 · update required", unavailable("upgrade"))]))

    # 4. map: 2D fallback, approximate position
    def mapview(weak):
        svg = ('<svg width="354" height="430" viewBox="0 0 354 430"><rect width="354" height="430" fill="#eef1e8"/>'
               '<path d="M20 380 C 90 330, 120 260, 180 240 S 300 150, 330 40" fill="none" stroke="#cfd8c4" stroke-width="22" stroke-linecap="round"/>'
               '<path d="M60 360 C 110 320, 140 270, 190 250 S 280 170, 300 110" fill="none" stroke="#6a3fd4" stroke-width="6" stroke-linecap="round" stroke-dasharray="1 0"/>'
               '<circle cx="300" cy="110" r="9" fill="#171425"/><text x="312" y="104" font-size="12" font-family="IBM Plex Sans,system-ui" fill="#171425">Falcon Drop</text>'
               + ('<circle cx="120" cy="310" r="42" fill="rgba(106,63,212,.10)" stroke="#6a3fd4" stroke-dasharray="4 4"/>'
                  '<circle cx="120" cy="310" r="8" fill="#6a3fd4" opacity=".45"/>'
                  '<rect x="64" y="252" width="130" height="24" rx="12" fill="#171425"/><text x="129" y="268" text-anchor="middle" font-size="11.5" font-family="IBM Plex Sans,system-ui" fill="#fff">Position approximate</text>'
                  if weak else '<circle cx="120" cy="310" r="12" fill="rgba(106,63,212,.18)"/><circle cx="120" cy="310" r="7" fill="#6a3fd4" stroke="#fff" stroke-width="2.5"/>')
               + '</svg>')
        c = (f'<div class="map">{svg}</div><div class="card"><div class="row"><span>Turn left at Wadi Rapids</span><span>120 m</span></div>'
             '<div class="row"><span>Falcon Drop on your right</span><span>4 min</span></div></div>'
             + ('<span class="btn ghost">I am at…</span>' if weak else ''))
        return phone("Map", c, "Home")
    f.append(frame("gst-state-map-fallback", "P02/state-map-fallback", "The map without 3D, and an approximate position "
                   "(GST-021, GST-038)", ["map3dUnavailable", "weakGps"],
                   "the v4 Interactive Map's walking-navigation view (frame #gst-021): the route in the brand colour, the "
                   "position dot, the turn list; drawn in 2D.",
                   "No 3D model, a phone that fails the 3D check or a slow render: the 2D map shows the same route and dot, "
                   "the 2D/3D toggle is hidden and nothing else is said. Weak GPS: the dot dims, a ring labelled Position "
                   "approximate is drawn round the last confident position, the turn list stays, and I am at… re-anchors "
                   "(ADR-0069).", [("390 x 844 · no 3D", mapview(False)), ("390 x 844 · weak GPS", mapview(True))]))

    # 5. preference not at venue (Plan)
    def pref():
        c = ('<h2>What do you like?</h2><div class="chips"><span class="chip on">Family rides</span><span class="chip on">Shows</span>'
             '<span class="chip out">Seafood<small>Not at the parks you chose · at Coastal Aqua</small></span>'
             '<span class="chip">Shopping</span></div>'
             '<div class="note">Your plan is made without seafood. Choose Coastal Aqua for a day to bring it in.</div>'
             '<span class="btn">Make my plan</span>')
        return phone("Plan", c, "Plan")
    f.append(frame("gst-state-preference-not-at-venue", "P02/state-preference-not-at-venue",
                   "A preference no chosen park can meet (GST-051, GST-053)", ["preferenceNotAtVenue"],
                   "the v4 Plan screen (frame #gst-051): its question, chip row and Make my plan button; the app's note style.",
                   "The chip is marked Not at the parks you chose and names the park that has it; the plan is made without "
                   "it, never with a place from a park the party is not visiting (MoM 30 September, 4.7).",
                   [("390 x 844", pref())]))

    # 6. AI unavailable
    def ai():
        c = ('<div class="note"><div class="mascot m-think" style="width:56px;height:56px;flex:0 0 56px"></div><span>Sahli can\'t '
             'help with the plan right now. Here is the plan from your answers: you can still change it.</span></div>'
             '<div class="card"><h3>Saturday · Summit Peaks</h3><div class="row"><span>10:15 Junior Circuit</span><span class="muted">5 min</span></div>'
             '<div class="row"><span>12:30 Lunch · The Crater Grill</span><span class="muted">Grill</span></div>'
             '<div class="row"><span>14:00 Falcon Drop</span><span class="muted">From 1.20 m</span></div></div><span class="btn">Edit my plan</span>')
        return phone("AI planner", c, "Plan")
    f.append(frame("gst-state-ai-unavailable", "P02/state-ai-unavailable", "The AI planner is unavailable (GST-054)",
                   ["aiUnavailable"], "the v4 Your plan view (frame #gst-053): the day card and its rows; the app's note "
                   "with the mascot's thinking pose (mascot2-thinking).",
                   "Falls back to the rules plan, never to an error: the plan from getVisitPlan stays with a short note and "
                   "the guest carries on editing it (MOB-6).", [("390 x 844", ai())]))

    # 7. sign-in refused
    def refused(locked):
        alert = ('<div class="alert"><i>!</i><div>Too many attempts. Try again in 15 minutes, or sign in with a code.'
                 '<small>Choose Send me a code.</small></div></div>' if locked else
                 '<div class="alert"><i>!</i><div>That did not work. Check your email and password and try again.</div></div>')
        c = ('<h2>Sign in</h2>' + alert + '<div class="field' + ('' if locked else ' bad') + '"><label>Email</label><div>layla@example.com</div></div>'
             '<div class="field' + ('' if locked else ' bad') + '"><label>Password</label><div>••••••••••</div></div>'
             + ('<span class="btn">Send me a code</span>' if locked else '<span class="btn">Sign in</span><span class="btn ghost">Send me a code</span>'))
        return phone("", c, "Tickets", back=False)
    f.append(frame("gst-state-sign-in-refused", "P02/state-sign-in-refused", "Sign-in refused (GST-042)", ["signInRefused"],
                   "the app's sign-in (v4 lines 1054-1058, the deep sign-in row and the Apple and Google buttons) as a form "
                   "with the app's fields, and the refusal notice of the web frame.",
                   "One message for every refusal; too many attempts says to try later and offers Send me a code (decided "
                   "28 September, audit R073 (a)).",
                   [("390 x 844 · a refusal", refused(False)), ("390 x 844 · too many attempts", refused(True))]))

    # 8. face pass: subject not linked
    def face():
        c = ('<div class="alert"><i>!</i><div>Yusuf is not linked to your account.<small>You can add Face Pass for yourself or a '
             'child linked to you.</small></div></div><h3>Who is this for?</h3>'
             '<div class="card"><div class="row"><span>Layla (you)</span><span class="muted">Ready</span></div>'
             '<div class="row"><span>Omar · 9</span><span class="muted">Linked child</span></div></div><span class="btn">Continue</span>')
        return phone("Face Pass", c, "Tickets")
    f.append(frame("gst-state-face-pass-not-linked", "P02/state-face-pass-not-linked", "Face Pass: that person is not linked "
                   "to you (GST-069)", ["subjectNotLinked"],
                   "the Face Pass view (Booking Mobile v2 line 1187, frame #gst-069): its card list and button; the refusal notice.",
                   "403 subject-not-linked: a guest enrols only themselves or a child linked to them; the screen says so and "
                   "returns to Who is this for, refreshed (decided 28 September, audit R205).", [("390 x 844", face())]))

    # 9. parking full for the day
    def park():
        c = ('<h2>Parking</h2><div class="chips"><span class="chip">Fri 2</span><span class="chip on">Sat 3<small>Full</small></span>'
             '<span class="chip">Sun 4</span></div><div class="alert"><i>!</i><div>The car park is full on Sat 3 Oct.'
             '<small>Choose another day for parking. Your tickets are not affected.</small></div></div>'
             '<div class="card"><h3>Car park East</h3><span class="muted">Four minutes from Gate C</span></div>'
             '<span class="btn off">Reserve and pay</span>')
        return phone("Parking", c, "Home")
    f.append(frame("gst-state-sold-out-for-day", "P02/state-sold-out-for-day", "Parking full for the chosen day (GST-027)",
                   ["soldOutForDay"], "the parking view (Booking Mobile v2, frame #gst-027): its day chips, card and button; "
                   "the refusal notice.", "Shown only when addCartLine refuses the line with soldOutForDay; no other day is "
                   "promised spaces (audit R166).", [("390 x 844", park())]))
    return f


# ================================================================================================= P04 till
POS_CSS = """
.pt{--acc:#0E7C86;--acc2:#6BC2C0;--ink:#0E1116;--mid:#4C555C;--line:#E6E8EB;--paper:#F4F5F7;--warn:#7A4E0C;--warntint:#FEF6E7;
  --bad:#B42318;--badtint:#FBECEC;--fh:'Inter Tight','Inter',system-ui,sans-serif;--fb:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;
  width:1620px;height:1080px;background:var(--paper);color:var(--ink);font-family:var(--fb);font-size:15px;display:flex;flex-direction:column;border-radius:18px}
.pt .hd{flex:0 0 70px;height:70px;background:#fff;border-block-end:1px solid var(--line);display:flex;align-items:center;gap:16px;padding:0 26px}
.pt .hd b{display:block;font:600 17px var(--fh);letter-spacing:-.01em} .pt .hd small{font-size:14px;color:var(--mid)}
.pt .srch{flex:1;max-width:400px;margin-inline-start:22px;height:44px;border-radius:12px;background:var(--paper);border:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:0 14px;color:#6B747C}
.pt .net{margin-inline-start:auto;display:flex;align-items:center;gap:8px;padding:9px 13px;border-radius:999px;background:#E9F7EF;border:1px solid #BFE3D2;font-size:15px;font-weight:600;color:#166534}
.pt .net i{width:6px;height:6px;border-radius:50%;background:#16A34A}
.pt .op{display:flex;align-items:center;gap:10px;padding:6px 14px 6px 6px;border-radius:999px;background:var(--paper);border:1px solid var(--line)}
.pt .op i{width:32px;height:32px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font:600 15px var(--fh);font-style:normal}
.pt .bd{flex:1 1 auto;display:flex;min-height:0}
.pt .rail{flex:0 0 92px;background:#121418;display:flex;flex-direction:column;align-items:center;gap:18px;padding-top:22px}
.pt .rail span{width:52px;height:52px;border-radius:14px;background:#22262C}
.pt .rail span.on{background:var(--acc)}
.pt .main{flex:1 1 auto;padding:22px 26px;display:flex;flex-direction:column;gap:16px;min-width:0}
.pt .cart{flex:0 0 420px;background:#fff;border-inline-start:1px solid var(--line);display:flex;flex-direction:column}
.pt .cart .ttl{padding:18px 20px;border-block-end:1px solid var(--line);font:600 17px var(--fh)}
.pt .cart .lines{flex:1;padding:14px 18px;display:flex;flex-direction:column;gap:9px}
.pt .cart .line{display:flex;justify-content:space-between;padding:12px 14px;border-radius:12px;background:var(--paper);font-size:15px}
.pt .cart .pay{margin:16px;height:60px;border-radius:15px;background:var(--acc);color:#fff;display:flex;align-items:center;justify-content:center;font:600 18px var(--fh)}
.pt .tabs{display:flex;gap:8px}
.pt .tabs span{padding:10px 16px;border-radius:11px;background:#fff;border:1px solid var(--line);font-weight:600;color:var(--mid)}
.pt .tabs span.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.pt .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.pt .tile{height:150px;border-radius:16px;background:#fff;border:1px solid var(--line);padding:16px;display:flex;flex-direction:column;justify-content:space-between}
.pt .sk{position:relative;overflow:hidden;background:#E9ECEF;border-radius:8px}
.pt .sk::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);animation:shimmer 1.4s ease-in-out infinite}
@keyframes shimmer{0%{transform:translateX(-120%)}100%{transform:translateX(220%)}}
.pt .panel{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px 24px;display:flex;flex-direction:column;gap:10px;max-width:720px}
.pt .panel.warn{background:var(--warntint);border-color:#F1D9A6} .pt .panel.bad{background:var(--badtint);border-color:#F3C1BC}
.pt .panel h3{margin:0;font:600 18px var(--fh)} .pt .panel p{margin:0;color:var(--mid);line-height:1.5}
.pt .kick{font-size:14px;letter-spacing:.14em;font-weight:600;color:var(--acc)}
.pt .perm{display:inline-block;font:600 13px ui-monospace,monospace;background:var(--paper);border:1px solid var(--line);padding:3px 8px;border-radius:7px;color:var(--ink)}
.pt .acts{display:flex;gap:9px;margin-top:6px}
.pt .b{height:44px;padding:0 16px;border-radius:11px;background:#fff;border:1px solid var(--line);display:flex;align-items:center;font-weight:600}
.pt .b.pri{background:var(--acc);border-color:var(--acc);color:#fff}
.pt .toast{position:absolute;bottom:28px;inset-inline-start:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;padding:15px 22px;border-radius:14px;background:var(--warn);color:#F2F4F6;box-shadow:0 24px 44px -22px rgba(12,20,24,.75);font-size:16px;font-weight:500}
.pt .modal{position:absolute;inset:0;background:rgba(12,20,24,.55);display:flex;align-items:center;justify-content:center}
.pt .sheet{width:640px;background:#fff;border-radius:20px;padding:28px 30px;box-shadow:0 40px 80px -30px rgba(12,20,24,.75)}
.pt .cells{display:flex;gap:10px;margin-top:12px}
.pt .cells span{width:56px;height:64px;border-radius:11px;border:1px solid var(--line);display:grid;place-items:center;font:500 26px var(--fh)}
.pt .cells span.f{border-color:var(--acc)}
.pt .zones{display:flex;flex-direction:column;gap:10px;max-width:760px}
.pt .zone{display:flex;justify-content:space-between;align-items:center;padding:16px 18px;border-radius:14px;background:#fff;border:1px solid var(--line);font-weight:600}
.pt .zone.out{background:var(--paper);color:#9AA3AB;text-decoration:line-through}
.pt .zone.out em{font-style:normal;text-decoration:none;display:inline-block;padding:4px 9px;border-radius:8px;background:var(--badtint);color:var(--bad);font-size:13px}
"""


def till(title, sub, main, cart=None, overlay="", net=("Online · synced", ""), who=("AM", "A. Mansouri", "Cashier")):
    lines = cart if cart is not None else ['<div class="line"><span>Adult day pass × 2</span><span>AED 650.00</span></div>']
    return (f'<div class="art pt" dir="ltr"><div class="hd"><div><b>{esc(title)}</b><small>{esc(sub)}</small></div>'
            f'<div class="srch">{ICON["search"]}Search tickets, guests, orders</div>'
            f'<div class="net"><i></i>{esc(net[0])}</div><div class="op"><i>{esc(who[0])}</i><div><b style="font-size:15px">{esc(who[1])}</b>'
            f'<small>{esc(who[2])}</small></div></div></div>'
            f'<div class="bd"><div class="rail"><span class="on"></span><span></span><span></span><span></span></div>'
            f'<div class="main">{main}</div><div class="cart"><div class="ttl">Current sale</div><div class="lines">{"".join(lines)}</div>'
            f'<div class="pay">Proceed to payment</div></div></div>{overlay}</div>')


def pos_frames():
    f = []
    tabs = '<div class="tabs"><span class="on">Tickets</span><span>Food &amp; drink</span><span>Merchandise</span><span>Memberships</span></div>'
    # 1. loading
    sk = '<div class="tile"><div class="sk" style="height:18px;width:70%"></div><div class="sk" style="height:14px;width:40%"></div><div class="sk" style="height:24px;width:50%"></div></div>'
    f.append(frame("pos-state-loading", "P04/state-loading", "Loading (every till screen)", ["loading"],
                   "the terminal's own shimmer (its @keyframes shimmer) on the catalogue tiles' shape, the header, rail and "
                   "cart as they are; the keypad and cart stay usable where the screen says so (POS-000: the keypad stays "
                   "visible and disabled).", "The tiles hold their place while the read is out; nothing jumps when it lands.",
                   [("1620 x 1080", till("Sell · Tickets", "Summit Peaks · Gate A · Till 3", tabs + '<div class="grid">' + sk * 8 + "</div>"))]))
    # 2. error
    err = ('<div class="panel bad"><div class="kick" style="color:var(--bad)">COULD NOT LOAD</div><h3>The ticket catalogue did not load</h3>'
           '<p>The catalogue service did not answer. Your sale is kept; try again, or report it if it keeps happening.</p>'
           '<div class="acts"><span class="b pri">Retry</span><span class="b">Report</span></div></div>'
           '<div class="panel warn"><div class="kick" style="color:var(--warn)">SIGN-IN · POS-000</div><h3>Can\'t reach sign-in</h3>'
           '<p>Your PIN was not checked: the network did not answer. Try again in a moment, or sign in from the cached operator list.</p></div>')
    f.append(frame("pos-state-error", "P04/state-error", "A read failed (every till screen; POS-000's Identity unreachable)",
                   ["error"], "the terminal's hardware alert panel (its title, line, note and the Retry and Report buttons) "
                   "in the place of what did not load; its warning colours.",
                   "Names which read failed and keeps the sale; sign-in says the network failed, never that the PIN was "
                   "wrong.", [("1620 x 1080", till("Sell · Tickets", "Summit Peaks · Gate A · Till 3", tabs + err))]))
    # 3. empty search
    nores = ('<div class="panel" style="align-self:flex-start"><h3>Nothing matches “cabana” in Tickets</h3>'
             '<p>The catalogue is still there: the filter is what narrowed it.</p><div class="acts"><span class="b pri">Clear filter</span></div></div>')
    f.append(frame("pos-state-no-results", "P04/state-no-results", "Nothing matches the filter (every till list)",
                   ["emptyNoResults"], "the terminal's panel and buttons, and the web prototype's wording for the same state "
                   "(\"the filter is what narrowed it\") in the till's tone.",
                   "Names the active filter and offers to clear it.",
                   [("1620 x 1080", till("Sell · Tickets", "Summit Peaks · Gate A · Till 3", tabs + nores))]))
    # 4. no access
    noacc = ('<div class="panel" style="align-self:flex-start"><div style="color:var(--mid)">' + ICON["lock"] + '</div>'
             '<h3>You can\'t open the ticket catalogue</h3><p>It needs <span class="perm">PRODUCT_VIEW</span>. Ask a supervisor '
             'to sign in on this till, or switch user.</p><div class="acts"><span class="b pri">Switch user</span></div></div>')
    f.append(frame("pos-state-no-access", "P04/state-no-access", "No access to the screen (every till screen)",
                   ["emptyNoAccess"], "the terminal's panel, its supervisor wording (\"needs a Supervisor role or above\") "
                   "and the operator chip.",
                   "Names the permission the screen's read needs; never an empty table.",
                   [("1620 x 1080", till("Sell · Tickets", "Summit Peaks · Gate A · Till 3", noacc, cart=[]))]))
    # 5. MFA
    mfa = ('<div class="modal"><div class="sheet"><div class="kick">SECOND STEP</div><div style="font:600 22px var(--fh);margin-top:8px">'
           'Enter the code from your authenticator app</div><div style="margin-top:14px;padding:15px 17px;border-radius:12px;'
           'background:var(--paper);color:#3C444C;line-height:1.55">Your role can approve money and staff changes, so this '
           'sign-in needs a second step.</div><div class="cells"><span class="f">4</span><span class="f">7</span><span class="f">1</span>'
           '<span></span><span></span><span></span></div><div class="acts" style="margin-top:20px"><span class="b pri">Verify</span>'
           '<span class="b">Email me a code instead</span></div><div style="margin-top:12px;font-size:14px;color:#9AA3AB">Five wrong '
           'codes lock this step for 15 minutes.</div></div></div>')
    f.append(frame("pos-state-mfa", "P04/state-mfa", "Second factor after sign-in (POS-000)", ["mfaRequired"],
                   "the terminal's supervisor PIN modal (its kicker, title, detail box and PIN cells), for an authenticator "
                   "code of six digits.",
                   "After login, a principal whose permissions need MFA enters the authenticator code; Email me a code "
                   "instead is the fallback; five wrong codes lock it (audit R135, R126). A cashier never sees it.",
                   [("1620 x 1080", till("Sign in", "Summit Peaks · Gate A · Till 3", '<div></div>', cart=[], overlay=mfa, who=("RK", "R. Khan", "Duty manager")))]))
    # 6. zone sold out while choosing
    zones = ('<div class="zones"><div class="zone"><span>VIP Box</span><span>AED 650</span></div>'
             '<div class="zone out"><span>Lower Tier</span><em>Sold out</em></div>'
             '<div class="zone"><span>Upper Tier</span><span>AED 165</span></div><div class="zone"><span>Family Stand</span><span>AED 95</span></div></div>')
    toast = ('<div class="toast">' + ICON["alert"] + 'Lower Tier sold out while you were choosing. The cart is unchanged.</div>')
    f.append(frame("pos-state-zone-unavailable", "P04/state-zone-unavailable", "A zone sold out while choosing (POS-004)",
                   ["zoneUnavailable"], "the terminal's zone list and its warning toast (the warn toast, #7A4E0C); the "
                   "struck-out zone uses its sold-out badge.",
                   "The board refuses the zone, not the sale: the seat map reloads with the zone struck out and the cart intact.",
                   [("1620 x 1080", till("Sell · Seat map", "Union Arena · Round 4 · Till 3", '<h3 style="margin:0;font:600 18px var(--fh)">Choose a zone</h3>' + zones,
                                         cart=['<div class="line"><span>Upper Tier × 2</span><span>AED 330.00</span></div>'], overlay=toast))]))
    return f


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    OUT.mkdir(parents=True, exist_ok=True)
    web = tokens_of("handoff/design-tokens/guest-web.yaml")
    app = tokens_of("handoff/design-tokens/guest-app.yaml")
    lede = ("<b>Drawn by the package from the approved design (r9), not yet seen by the client.</b> The states the client-"
            "approved prototype never drew, one frame per state class, in its look: its CSS variables, type, colours, "
            "spacing, components and tone (tools/draw-state-frames.py, CHG-R9UI-005). Each frame names what it is built "
            "from. They go to the client at the next review.")
    boards = {
        "P01 Guest Web states.dc.html": board("P01 Guest Web: state frames (r9)", lede, web_css(web), web_frames(web)),
        "P02 Guest App states.dc.html": board("P02 Guest App: state frames (r9)", lede,
                                              app_css(app, mascot("mascot2-sad.png"), mascot("mascot2-thinking.png")),
                                              app_frames(app)),
        "P04 Venue POS states.dc.html": board("P04 Venue POS: state frames (r9)", lede, POS_CSS, pos_frames()),
    }
    for name, text in boards.items():
        f = OUT / name
        old = f.read_text(encoding="utf-8") if f.exists() else None
        if old != text:
            f.write_text(text, encoding="utf-8")
        n = text.count('class="state-frame"')
        print(f"  {'unchanged' if old == text else 'written'}  wireframes/states/{name} ({len(text) // 1024} KB, {n} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
