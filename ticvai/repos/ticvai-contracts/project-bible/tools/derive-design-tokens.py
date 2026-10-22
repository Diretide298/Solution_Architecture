#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The guest apps' design tokens, taken from the CSS variables of their client-approved prototypes.

**21 October 2026, CHG-R9UI-001** (the lead: "I wanna get all of those changes out now.."). `screens/_design-tokens.yaml`
was written down on 9 September from the Claude Design boards and the client's POS file: Manrope, the till's palette.
It is the till's system, and it was the only token file the package had, so a guest screen built "to the tokens" was
built to look like the till (WEB-007, 21 October). The guest web and guest app prototypes the client approved carry
their own system: Archivo with IBM Plex Sans, a `--brand` colour per venue, a radius, a density and a surface style,
every one a CSS variable set on the page root from the venue's palette. This writes that system down, from the
prototype files themselves, so the app shell (SETUP-SHELL-GUEST-WEB, SETUP-SHELL-GUEST-APP) applies it and nobody
types a colour.

Writes, per guest app (the till keeps screens/_design-tokens.yaml):

  handoff/design-tokens/guest-web.yaml   from TICVAI Guest Booking v2 (30 September): every variable theme() and its
                                         helpers set on the root, with its rule (the expression), its default (the
                                         fallback the markup gives it most often) and how often the markup uses it;
                                         the font pairs, the named palettes and the venue palettes
  handoff/design-tokens/guest-app.yaml   from TICVAI Mobile App v4 (30 September) and Guest Booking Mobile v2
                                         (28 September): the variables each sets on its root element, with the same
                                         three facts, and v4's skins per venue kind

Both say how the tokens are applied: from `getPublishedTenantConfig` (PublishedTenantConfig.theme and .fonts), the
mapping below. Derived; a second run writes the same bytes.

    python3 tools/derive-design-tokens.py [--check]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "handoff" / "design-tokens"
WEB = "sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html"
APP_V4 = "sources/designs/guest-rev3-30-september/TICVAI Mobile App v4.dc.html"
APP_V2 = "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html"

# How a tenant's published theme reaches the variables (contracts/satellite/white-label.yaml, Theme and
# PublishedTenantConfig). The prototype's palette fields are the contract's colours; the rest of its variables are
# derived from them by the rules written beside each variable.
APPLIED_FROM = {
    "operation": "white-label#getPublishedTenantConfig (loaded once by the app shell; screens read it, never refetch)",
    "theme.primaryColour": "the palette's brand: --brand (web), --br (app)",
    "theme.secondaryColour": "the palette's brand2: --brand-2 (web)",
    "theme.accentColour": "the palette's accent: --accent",
    "theme.backgroundColour": "the palette's bg: --bg",
    "theme.textColour": "the ink the rules derive (--ink, --ink-2, --ink-3) when it is not set",
    "theme.darkMode": "the palette's dark: which way the ink, line and shadow rules mix",
    "theme.cornerRadius": "--r and --r-sm (web), --rk (app, a scale on the base radii)",
    "theme.surfaceStyle": "Glass or Solid: --surface, --surface-2, --line (web, data-glass on the root)",
    "theme.buttonStyle": "Solid, Outline or Pill: --btn-bg, --btn-fg, --btn-bd, --btn-r (web)",
    "fonts": "the heading and body pair: --font-h and --font-b (web), --fh and --fb (app)",
    "direction": "dir=rtl on the root when the guest's language is Arabic; every token is direction-free",
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def method_body(src: str, name: str) -> str:
    """The text of a class method `name() {` ... to its matching brace."""
    m = re.search(r"^\s{2}" + re.escape(name) + r"\([^)]*\)\s*\{", src, re.M)
    if not m:
        return ""
    i, depth = m.end(), 1
    while i < len(src) and depth:
        c = src[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return src[m.end():i - 1]


def object_entries(body: str) -> dict:
    """'--name': expression pairs at the top level of the returned object of a method body."""
    out = {}
    for m in re.finditer(r"'(--[a-z0-9-]+)'\s*:\s*", body):
        i, depth, j = m.end(), 0, m.end()
        while j < len(body):
            c = body[j]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                break
            elif c in "'\"":
                q, j = c, j + 1
                while j < len(body) and body[j] != q:
                    j += 2 if body[j] == "\\" else 1
            j += 1
        out.setdefault(m.group(1), " ".join(body[i:j].split()))
    return out


def var_uses(src: str) -> tuple:
    """(uses, fallbacks): how often the markup reads each variable, and the fallbacks it gives it."""
    uses, falls = Counter(), {}
    for m in re.finditer(r"var\((--[A-Za-z0-9-]+)", src):
        name = m.group(1)
        uses[name] += 1
        j, depth = m.end(), 0
        if j < len(src) and src[j] == ",":
            k = j + 1
            while k < len(src):
                c = src[k]
                if c == "(":
                    depth += 1
                elif c == ")":
                    if depth == 0:
                        break
                    depth -= 1
                k += 1
            fb = " ".join(src[j + 1:k].split())
            if fb and "{{" not in fb:
                falls.setdefault(name, Counter())[fb] += 1
    return uses, falls


def default_of(falls: dict, name: str):
    c = falls.get(name)
    if not c:
        return None
    return sorted(c.items(), key=lambda x: (-x[1], x[0]))[0][0]


def root_bindings(src: str, marker: str) -> dict:
    """The custom properties a root element binds in its style attribute (`--x:{{ expr }}`)."""
    i = src.find(marker)
    if i < 0:
        return {}
    m = re.compile(r'style="([^"]*)"').search(src, src.rfind("<", 0, i + 1))
    if not m:
        return {}
    return {k: " ".join(v.split()) for k, v in re.findall(r"(--[A-Za-z0-9-]+)\s*:\s*\{\{\s*(.*?)\s*\}\}", m.group(1))}


def palette_table(src: str, lo: int, hi: int) -> dict:
    out = {}
    for ln in src.splitlines()[lo - 1:hi]:
        m = re.match(r"\s*'([^']+)'\s*:\s*\{\s*(brand:.*?)\}\s*,?\s*$", ln.encode().decode("unicode_escape")
                     if "\\u" in ln else ln)
        if m:
            out[m.group(1)] = {k: (v == "true") if v in ("true", "false") else unquote(v)
                               for k, v in re.findall(r"(\w+):\s*('[^']*'|true|false|\[[^\]]*\])", m.group(2))
                               if k != "swatches"}
    return out


def unquote(v: str) -> str:
    """One pair of outer quotes off a JS literal ("'Archivo',sans-serif" keeps its inner quotes)."""
    v = v.strip()
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"" else v


def line_of(src: str, needle: str) -> int:
    i = src.find(needle)
    return src.count("\n", 0, i) + 1 if i >= 0 else 0


def web_tokens() -> dict:
    src = read(WEB)
    uses, falls = var_uses(src)
    tokens = {}
    for meth in ("theme", "skinVars", "cartVars", "catVars"):
        for k, rule in object_entries(method_body(src, meth)).items():
            tokens.setdefault(k, {"rule": rule, "setBy": f"{meth}()", "default": default_of(falls, k),
                                  "uses": uses.get(k, 0)})
    theme = method_body(src, "theme")
    pairs = {k: [a, b] for k, a, b in re.findall(r"'([^']+)':\s*\[\"([^\"]+)\",\s*\"([^\"]+)\"\]", theme)}
    pal_lo = line_of(src, "  palettes() {")
    return {
        "app": "guest-web", "repository": "ticvai-guest-web", "platforms": ["P01"],
        "source": {"file": WEB, "rev": "rev 3, 30 September 2026 build", "theme": f"theme() at line {line_of(src, '  theme() {')}",
                   "apply": f"apply() at line {line_of(src, '  apply() {')}: every variable set on document.documentElement"},
        "appliedFrom": APPLIED_FROM,
        "fonts": {"pairs": pairs, "default": "Archivo / IBM Plex Sans",
                  "headingFallback": default_of(falls, "--font-h"), "bodyFallback": default_of(falls, "--font-b")},
        "tokens": dict(sorted(tokens.items())),
        "palettes": palette_table(src, pal_lo - 40 if pal_lo > 40 else 1, pal_lo + 8),
        "notes": ["A variable's `default` is what the markup falls back to before the theme is applied (the prototype's "
                  "own default venue): build the shell so it is never seen, by applying the tenant's theme first.",
                  "Colours are mixed by the rules (`mix`, `rgba`, `inkOn`, `onColor` in the prototype); the shell "
                  "implements the same functions, so a tenant's two or three colours give every variable."],
    }


def app_tokens() -> dict:
    v4, v2 = read(APP_V4), read(APP_V2)
    out = {"app": "guest-app", "repository": "ticvai-guest-app", "platforms": ["P02"], "appliedFrom": APPLIED_FROM,
           "sources": []}
    for rel, src, marker, rev in ((APP_V4, v4, 'data-lux="1"', "Mobile App v4, 30 September 2026 build"),
                                  (APP_V2, v2, '<div style="--bg:{{ t.bg }}', "Guest Booking Mobile v2, 28 September 2026 build")):
        uses, falls = var_uses(src)
        root = root_bindings(src, marker)
        out["sources"].append({
            "file": rel, "rev": rev, "root": f"the root element at line {line_of(src, marker)}",
            "tokens": {k: {"binding": v, "default": default_of(falls, k), "uses": uses.get(k, 0)}
                       for k, v in sorted(root.items())}})
    body = method_body(v4, "skin")
    skins = {}
    for k, inner in re.findall(r"^\s{6}(\w+):\s*(?:Object\.assign\(\{\},\s*L,\s*)?\{([^\n]*)", body, re.M):
        if k in skins:          # the first definition is the skin; a later line of the same name is a nested object
            continue
        skins[k] = {a: unquote(b) for a, b in re.findall(r"(\w+):\s*('[^']*'|\"[^\"]*\"|[0-9.]+)", inner)
                    if a in ("bg", "sf", "ink", "ink2", "ink3", "ln", "ln2", "deep", "rk", "fh", "fb")}
    base = re.search(r"const L = \{([^}]*)\}", body)
    out["skins"] = {"base": {a: unquote(b) for a, b in re.findall(r"(\w+):\s*('[^']*')", base.group(1))} if base else {},
                    "byVenueKind": skins,
                    "source": f"skin() at line {line_of(v4, '  skin(k) {')} of {APP_V4}"}
    out["notes"] = ["The two app prototypes name their variables differently (v4: --br, --sf, --ln, --rk, --fh, --fb; "
                    "v2: --brand, --surface, --line, --r, --font-h, --font-b). They are one system: the shell keeps "
                    "one set of names and maps both to it; a screen takes the names of the prototype its view is in.",
                    "A variable's `default` is the prototype's fallback before the venue's skin is applied."]
    return out


HEAD = ("# Generated by tools/derive-design-tokens.py from the client-approved prototype (CHG-R9UI-001). Do not edit.\n"
        "# The app shell applies these tokens; screens never hard-code a colour, font or radius.\n")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if a file would change; write nothing")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, doc in (("guest-web.yaml", web_tokens()), ("guest-app.yaml", app_tokens())):
        text = HEAD + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=110)
        f = OUT / name
        n = len(doc.get("tokens") or {}) or sum(len(s["tokens"]) for s in doc.get("sources") or [])
        if f.exists() and f.read_text(encoding="utf-8") == text:
            print(f"  unchanged  {f.relative_to(ROOT).as_posix()} ({n} tokens)")
            continue
        stale.append(f)
        if not a.check:
            f.write_text(text, encoding="utf-8")
        print(f"  {'would write' if a.check else 'written'}  {f.relative_to(ROOT).as_posix()} ({n} tokens)")
    return 1 if (a.check and stale) else 0


if __name__ == "__main__":
    raise SystemExit(main())
