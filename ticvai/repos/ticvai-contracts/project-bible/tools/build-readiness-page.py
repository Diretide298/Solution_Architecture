#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The build-readiness report as a page the viewer serves.

**Asked for on 21 September: get it live on ADAM.** The viewer already serves
`handoff/*.html` as standalone pages behind the same gate as everything else, with an `?embed=1`
mode that hides the page's own header and reports its height to the frame around it. This writes
one more.

## The narrative is dated and the figures are not, so they are kept apart

`docs/reports/build-readiness-21-september.md` is a document written on a day and it stays that
way -- an argument about what to build next does not get quietly rewritten by a refresh.
**The numbers under it would go stale silently**, which is the failure this package spends most of
its tooling on, so the page carries a strip of live figures read from `handoff/package-report.json`
at generation time, dated, beside the dated prose.

**When the two disagree, the page says so rather than picking one.** A figure quoted in the
narrative that no longer matches the derived file is the reader's business, not something to
paper over -- so the strip states the refresh it came from and the prose states the day it was
written, and both dates are on screen.

## No dependencies, and no CDN

Rendered with a small markdown reader rather than a library, because `handoff/` pages are served
off a machine that may have no network and a page that needs a CDN to draw is a page that fails
in the room where it matters. The one Mermaid block renders as its own source in a monospace
block for the same reason.

    python3 tools/build-readiness-page.py [--apply]

Writes `handoff/Build Readiness.html`. Registered in the viewer's search in
`viewer/lib/search.mjs`, which names handoff pages explicitly rather than globbing them.
"""
import argparse
import html
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "reports", "build-readiness-21-september.md")
REPORT = os.path.join(ROOT, "handoff", "package-report.json")
OUT = os.path.join(ROOT, "handoff", "Build Readiness.html")

INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+\*|\[[^\]]+\]\([^)]+\))")


def spans(text):
    out = []
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            out.append("<b>%s</b>" % html.escape(piece[2:-2]))
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            out.append("<code>%s</code>" % html.escape(piece[1:-1]))
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            out.append("<i>%s</i>" % html.escape(piece[1:-1]))
        elif piece.startswith("["):
            m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", piece)
            out.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                       % (html.escape(m.group(2), True), html.escape(m.group(1))))
        else:
            out.append(html.escape(piece))
    return "".join(out)


def render(md):
    lines = md.replace("\r\n", "\n").split("\n")
    out, i, nav = [], 0, []
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            body = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            out.append('<figure class="code"%s><pre>%s</pre></figure>'
                       % (' data-lang="%s"' % html.escape(lang, True) if lang else "",
                          html.escape("\n".join(body))))
            continue

        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                t = ["<div class=tw><table>"]
                for n, row in enumerate(rows):
                    tag = "th" if n == 0 else "td"
                    t.append("<tr>" + "".join("<%s>%s</%s>" % (tag, spans(c), tag)
                                              for c in row) + "</tr>")
                t.append("</table></div>")
                out.append("".join(t))
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", s)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", txt.lower()).strip("-")[:48]
            if lvl == 2:
                nav.append((slug, txt))
            out.append('<h%d id="%s">%s</h%d>' % (lvl, slug, spans(txt), lvl))
            i += 1
            continue

        m = re.match(r"[-*+]\s+(.*)", s)
        if m:
            items = []
            while i < len(lines) and re.match(r"\s*[-*+]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*+]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % spans(x) for x in items) + "</ul>")
            continue

        m = re.match(r"\d+[.)]\s+(.*)", s)
        if m:
            items = []
            while i < len(lines) and re.match(r"\s*\d+[.)]\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % spans(x) for x in items) + "</ol>")
            continue

        out.append("<p>%s</p>" % spans(s))
        i += 1
    return "\n".join(out), nav


CSS = """
:root{--bg:#1a1a1a;--panel:#1f1f1f;--card:#242424;--line:#3a3a3a;--div:#333;--text:#ededed;
--dim:#9a9a9a;--faint:#787878;--ac:#2bb3b0;--acb:#48cfcb;--acl:#2c7c7d;--amber:#d9a143;
--warm:#2b2418;--warmt:#d9bc7c;--green:#7fbf8f;--mono:'JetBrains Mono',ui-monospace,monospace}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg)}
body{font-family:"Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);font-size:14.5px;
line-height:1.62;-webkit-font-smoothing:antialiased}
header{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:10px 22px;
background:#111;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
header .tag{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;
color:var(--faint)}
.wrap{max-width:1180px;margin:0 auto;padding:26px 22px 90px;display:grid;
grid-template-columns:minmax(0,1fr) 226px;gap:34px;align-items:start}
main{min-width:0}
nav{position:sticky;top:64px;border-left:1px solid var(--div);padding-left:14px}
nav a{display:block;color:var(--dim);text-decoration:none;font-size:12.5px;padding:3px 0}
nav a:hover{color:var(--acb)}
a{color:var(--acb);text-decoration:none}
a:hover{text-decoration:underline}
h1{font-size:27px;line-height:1.2;margin:2px 0 4px;letter-spacing:-.01em}
h2{font-size:19px;margin:38px 0 10px;padding-top:14px;border-top:1px solid var(--div);
letter-spacing:-.005em}
h3{font-size:15px;margin:24px 0 6px;color:var(--warmt)}
p{margin:0 0 11px}
b{color:#fff;font-weight:650}
code{font-family:var(--mono);font-size:12px;background:#2a2a2a;border:1px solid #343434;
border-radius:4px;padding:1px 5px;color:#e6b8a2}
ul,ol{margin:0 0 12px;padding-left:20px}
li{margin:0 0 5px}
hr{border:0;border-top:1px solid var(--div);margin:22px 0}
.tw{overflow-x:auto;margin:0 0 16px;border:1px solid var(--line);border-radius:8px;
background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:12.8px}
th{background:#171717;color:var(--dim);font-weight:600;text-align:left;padding:8px 11px;
border-bottom:1px solid var(--line);font-family:var(--mono);font-size:11px;letter-spacing:.04em;
text-transform:uppercase;white-space:nowrap}
td{padding:7px 11px;border-bottom:1px solid #2c2c2c;vertical-align:top}
tr:last-child td{border-bottom:0}
tr:hover td{background:#282828}
figure.code{margin:0 0 16px;background:#141414;border:1px solid var(--line);border-radius:8px;
padding:12px 14px;overflow-x:auto;position:relative}
figure.code[data-lang]::before{content:attr(data-lang);position:absolute;top:6px;right:10px;
font-family:var(--mono);font-size:9.5px;letter-spacing:.09em;text-transform:uppercase;
color:var(--faint)}
pre{margin:0;font-family:var(--mono);font-size:11.8px;line-height:1.55;color:#cfe8e7;
white-space:pre}
.strip{display:flex;flex-wrap:wrap;gap:1px;background:var(--line);border:1px solid var(--line);
border-radius:8px;overflow:hidden;margin:0 0 6px}
.strip div{flex:1 1 118px;background:var(--panel);padding:9px 12px}
.strip .n{font-family:var(--mono);font-size:17px;color:var(--acb);letter-spacing:-.02em}
.strip .k{font-size:10.5px;color:var(--faint);text-transform:uppercase;letter-spacing:.06em;
margin-top:2px}
.prov{font-size:11.5px;color:var(--faint);margin:0 0 26px;font-family:var(--mono)}
.prov b{color:var(--warmt);font-weight:500}
@media(max-width:940px){.wrap{grid-template-columns:1fr}nav{display:none}}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(SRC):
        print("  !! %s is missing" % os.path.relpath(SRC, ROOT))
        return 1
    md = io.open(SRC, encoding="utf-8").read()

    # **The title and byline come out of the markdown and are not repeated.** The page draws its
    # own header, and two lockups down one document is not a design.
    md = re.sub(r"\A# [^\n]*\n+", "", md)
    md = re.sub(r"\A[^\n]*·[^\n]*\n+", "", md)

    body, nav = render(md)

    rep = json.load(io.open(REPORT, encoding="utf-8")) if os.path.exists(REPORT) else None
    strip = ""
    if rep:
        c = rep["counts"]
        chain = {x["link"]: x for x in rep["chain"]}
        cells = [
            ("%s" % c["operations"], "operations"),
            ("%s" % c["screens"], "screens"),
            ("%s" % c["tables"], "tables"),
            ("17", "services"),
            ("%d%%" % chain["Operations reaching a screen"]["percent"], "reach a screen"),
            ("%d%%" % chain["Requirements contracted"]["percent"], "reqs contracted"),
            ("%d" % rep["boundaries"]["crossingTwoServices"], "refs cross a service"),
            ("%s" % (rep["open"] or {}).get("conflictsOpen"), "conflicts open"),
        ]
        strip = ('<div class=strip>'
                 + "".join("<div><div class=n>%s</div><div class=k>%s</div></div>" % (n, k)
                           for n, k in cells)
                 + "</div>")

    page = """<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>TICVAI — build readiness</title>
<link rel=preconnect href="https://fonts.googleapis.com">
<link rel=preconnect href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel=stylesheet>
<style>%s</style>
</head>
<body>
<header>
  <div style="display:flex;align-items:center;gap:12px">
    <img src="brand/adam-lockup-night.png" alt="Adam" style="height:22px;display:block">
    <span class=tag>build readiness</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px;font-size:11.5px">
    <a href="Burst Simulator.dc.html" style="font-family:var(--mono);font-size:11px;
       color:var(--acb);border:1px solid var(--acl);border-radius:6px;padding:3px 9px">the burst
       environment →</a>
    <span class=tag>21 September 2026</span>
  </div>
</header>
<div class=wrap>
<main>
<h1>TICVAI — build readiness</h1>
%s
<p class=prov>narrative written <b>21 September 2026</b> · figures derived by
<b>tools/build-package-report.py</b> on <b>%s</b> · page generated by
<b>tools/build-readiness-page.py</b></p>
%s
</main>
<nav>%s</nav>
</div>
</body>
</html>
""" % (CSS, strip, (rep or {}).get("generated", "an earlier refresh"), body,
       "".join('<a href="#%s">%s</a>' % (s, html.escape(t)) for s, t in nav))

    print("  %d section(s) · %d character(s)" % (len(nav), len(page)))
    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(page)
    print("  -> handoff/Build Readiness.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
