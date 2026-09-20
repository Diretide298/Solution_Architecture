#!/usr/bin/env python3
"""Repaint the Adam designs onto pure grounds and the logo's own cyan.

**The accent was never the logo's colour.** Every design used `#48CFCB` - hue 178, 58% saturation.
The lockup beside it is hue 187 at 83%, sampled from 6,472 neon pixels of
`brand/adam-lockup-night.png`. Eleven degrees greener and two-thirds the saturation is far enough
to read as wrong and close enough to look like a mistake rather than a choice.

**The greys were tinted toward that same teal.** `#1D2C30`, `#0E1314`, `#7E8C8D` - all of them
green-cyan. A tinted ground under a desaturated accent leaves nothing to separate the two, which
is why the gradient looked muddy and the accent looked flat. Both symptoms have one cause.

Seven designs carry 60-plus colours each, so this works by RULE rather than by lookup - a hand map
per file would be guesswork dressed as precision, and it could not say what it had missed.

  A  ground      night: anything at or below 7% lightness becomes #000000
                 day:   anything at or above 97% lightness becomes #FFFFFF
  B  accent      hue 160-200 at 20%+ saturation rotates to hue 187 and gains saturation,
                 KEEPING ITS LIGHTNESS - which is what preserves contrast on both grounds
  C  neutrals    under 20% saturation is retinted to hue 187 at a trace of it, same lightness
  D  everything else is left alone

Rule D is the important one. Amber, purple and red carry meaning in these files - amber is the
Contracts layer, which `LANDING.md` argues is the only non-cyan body *because* everything else
resolves against it - and a rule that recoloured them would delete what the design is saying.

**Rule B keeps lightness on purpose.** `#1AD3EA` on white is 1.9:1, nowhere near the 4.5:1 text
needs, so a flat "make it neon" would have broken every light-mode label. Rotating hue while
holding lightness turns the day files' `#1F8F91` into a cyan of the same weight instead.

Run: `python repalette.py [--apply] [file ...]`
"""
from __future__ import annotations

import argparse
import colorsys
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "designs"

HUE = 187.0 / 360.0        # the lockup's neon
GROUND_DARK, GROUND_LIGHT = 0.07, 0.97
BAND = (160.0 / 360.0, 200.0 / 360.0)
ACCENT_MIN_SAT = 0.20
NEUTRAL_MAX_SAT = 0.20
NEUTRAL_SAT = 0.06        # the trace of accent a neutral keeps
# **The idempotency marker is hue, with room for 8-bit rounding.** At 6% saturation a hex cannot
# hold 187 exactly - outputs land anywhere from 183 to 191 - so a tight tolerance never recognised
# this tool's own work and 111 neutrals were rewritten on every run. The old teal sat at 178, nine
# degrees away, so this window separates the two cleanly.
HUE_TOL = 0.012           # ~4.3 degrees
SAT_GAIN = 1.4
SAT_CAP = 0.95

# A file is a night file unless its own ground says otherwise; the day ones are named for it,
# except the viewer topbar, whose day variant is the unsuffixed name.
# **Matched on the name before the first dot, not `Path.stem`** - these carry two extensions, so
# `stem` yields `Adam Invite Day.dc` and every day file was being repainted as a night one.
DAY_FILES = {"Adam Invite Day", "Adam Sign In Day", "Viewer Redesign - Topbar",
             "Adam Landing Day"}


def is_day(path):
    return path.name.split(".")[0] in DAY_FILES


def to_hls(hexv: str):
    h = hexv.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)


def to_hex(h, l, s) -> str:
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02X%02X%02X" % tuple(int(round(x * 255)) for x in (r, g, b))


# The canonical accent is pinned rather than derived, so every design lands on the one value
# sampled from the lockup instead of six near-misses of it.
ACCENT = "#1AD3EA"
PINNED = {"#48CFCB": ACCENT, "#2BB3B0": "#0FA8BE"}


def remap(hexv: str, day: bool):
    """Returns (new hex, rule letter) or (hexv, None) when nothing applies."""
    if hexv.upper() in PINNED:
        return PINNED[hexv.upper()], "B"
    h, l, s = to_hls(hexv)
    # **Already repainted.** Sitting exactly on the brand hue is the marker: nothing in the
    # original files did, so this only ever catches this tool's own output. Without it rule B
    # lifts saturation by 1.4 on every run and the file drifts further from the brand each time
    # it is touched - the saturation-gated version of this guard missed the mid-tones and twelve
    # values kept moving.
    if abs(h - HUE) < HUE_TOL:
        return hexv, None
    if not day and l <= GROUND_DARK:
        return ("#000000", "A") if hexv.upper() != "#000000" else (hexv, None)
    if day and l >= GROUND_LIGHT:
        return ("#FFFFFF", "A") if hexv.upper() != "#FFFFFF" else (hexv, None)
    if BAND[0] <= h < BAND[1] and s >= ACCENT_MIN_SAT:
        return to_hex(HUE, l, min(SAT_CAP, s * SAT_GAIN)), "B"
    if 0 < s < NEUTRAL_MAX_SAT:
        target = to_hex(HUE, l, NEUTRAL_SAT)
        # **A direct fixed-point test.** Hue and saturation both quantise badly at the extremes
        # of lightness, so neither is a reliable marker on its own; asking whether this colour is
        # already what the rule would produce is exact wherever the others are approximate.
        if max(abs(int(hexv.lstrip("#")[i:i + 2], 16) - int(target.lstrip("#")[i:i + 2], 16))
               for i in (0, 2, 4)) <= 3:
            return hexv, None
        # **Retinted toward the brand, not flattened to pure grey.** The greys were the problem
        # because they leaned toward the OLD teal, not because they were tinted at all - a pure
        # mid-grey reads as unconsidered. Holding a trace of the accent hue keeps them a set.
        return target, "C"
    return hexv, None


def luminance(hexv):
    h = hexv.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def readable(hexv, ground, need=4.5):
    """The same hue and saturation, moved in lightness until it passes on that ground.

    **The neon cannot be a text colour on white.** `#1AD3EA` is 1.82:1 there, and `color:#48CFCB`
    appears six times across the three day files - a straight recolour would have made every one
    of them unreadable while the swatch sheet said the palette passed. Fills keep the neon; only
    the values written as `color:` are moved, and only as far as they have to go.
    """
    if contrast(hexv, ground) >= need:
        return hexv
    h, l, s = to_hls(hexv)
    darker = luminance(ground) > 0.5
    step = -0.02 if darker else 0.02
    for _ in range(48):
        l = min(1.0, max(0.0, l + step))
        cand = to_hex(h, l, s)
        if contrast(cand, ground) >= need:
            return cand
    return to_hex(h, 0.08 if darker else 0.95, s)


GRADIENT = re.compile(r"(?:radial|linear|conic)-gradient\([^()]*(?:\([^()]*\)[^()]*)*\)")
# A one-pixel stop is a dot-grid pattern, not a wash. It is texture and it survives.
DOT_GRID = re.compile(r"1px\s*,\s*transparent\s+1px")


def flatten_gradients(text, day):
    """Every background gradient goes. What it becomes depends on what it was doing.

    **A wash cannot become a colour.** The vignettes and scrims are `pointer-events:none` overlays
    lying across the content; giving one a solid fill would paint over the page instead of
    removing the gradient. Those become `transparent` - the element stays, so nothing below it
    shifts, and the wash is gone.

    The rest collapse: a panel background to the flat ground, a two-stop button fill to the one
    canonical accent. Over a pure ground a legibility scrim has nothing left to do anyway.
    """
    ground = "#FFFFFF" if day else "#000000"
    counts = {"wash": 0, "panel": 0, "fill": 0}

    def in_style(m):
        style = m.group(0)
        if not GRADIENT.search(style):
            return style

        def one(g):
            grad = g.group(0)
            if DOT_GRID.search(grad):
                return grad
            if "pointer-events:none" in style:
                counts["wash"] += 1
                return "transparent"
            if "135deg" in grad:
                counts["fill"] += 1
                return ACCENT
            counts["panel"] += 1
            return ground

        return GRADIENT.sub(one, style)

    text = re.sub(r'style="[^"]*"', in_style, text)
    # Anything left sits in a <style> block rather than an attribute; those are page backgrounds.
    def bare(g):
        if DOT_GRID.search(g.group(0)):
            return g.group(0)
        counts["panel"] += 1
        return ground
    text = GRADIENT.sub(bare, text)
    return text, counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    targets = [Path(f) for f in a.files] or sorted(ROOT.glob("*.dc.html"))
    grand = {"A": 0, "B": 0, "C": 0}
    for path in targets:
        text = io.open(path, encoding="utf-8").read()
        day = is_day(path)
        text, grads = flatten_gradients(text, day)

        moves, counts = {}, {"A": 0, "B": 0, "C": 0}
        for c in sorted(set(re.findall(r"#[0-9A-Fa-f]{6}", text))):
            new, rule = remap(c, day)
            if rule:
                moves[c] = (new, rule)
                counts[rule] += text.count(c)
        # **Text first, and separately.** A value used as `color:` has to clear 4.5:1 on the
        # ground; the same value used as a fill does not and keeps the neon.
        # **Only contrast this tool broke is repaired.** A `color:` that already failed against
        # the page ground is text sitting on something else - a chip, a button, an accent fill -
        # and "fixing" it against the ground makes it worse: `#111111` on a light chip in the
        # night topbar was lightened to `#757575`, which is the opposite of readable.
        ground = "#FFFFFF" if day else "#000000"
        fixed = 0
        for old in sorted(moves, key=len, reverse=True):
            new_v = moves[old][0]
            if contrast(old, ground) < 4.5:
                continue                      # it was not readable on the ground to begin with
            safe = readable(new_v, ground)
            if safe != new_v:
                fixed += text.count("color:" + old)
                text = text.replace("color:" + old, "color:" + safe)
        # Longest-first so a six-digit value is never rewritten inside a longer token.
        for old in sorted(moves, key=len, reverse=True):
            text = text.replace(old, moves[old][0])

        for k in counts:
            grand[k] += counts[k]
        print("  %-38s %-5s  ground %3d   accent %3d   neutral %3d   gradients removed %d"
              % (path.name, "day" if day else "night",
                 counts["A"], counts["B"], counts["C"],
                 grads["wash"] + grads["panel"] + grads["fill"])
              + ("   text deepened for contrast %d" % fixed if fixed else ""))
        for old, (new, rule) in sorted(moves.items(), key=lambda kv: kv[1][1]):
            if rule == "B":
                print("        %s  %s -> %s" % (rule, old, new))
        if a.apply:
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)

    print("\n%d ground, %d accent, %d neutral value(s)%s"
          % (grand["A"], grand["B"], grand["C"],
             "" if a.apply else "   nothing written - pass --apply"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
