#!/usr/bin/env python3
"""Unpack a Claude Design `.dc.html` bundle into an editable document plus its assets.

**The client-approved POS terminal is 5.67 MB and only 20 KB of that is reachable.** The build
itself -- 210 `sc-for`, 230 `sc-if`, 1,351 divs -- is not markup in the file at all: it is a
JSON-escaped string on a single line inside `<script type="__bundler/template">`, with 4.67 MB of
base64 assets on another single line above it. Opened in an editor the file looks like three
enormous lines and nothing you can change. Diffed, it reports the whole build as one modified
line. Handed to a design session whole it costs a million tokens to say very little.

So "extend the approved build rather than start again" was not something anybody could act on,
and the reason was purely mechanical. This unpacks it:

    <script type="__bundler/manifest">        uuid -> {mime, base64 data, compressed}
    <script type="__bundler/ext_resources">   placeholder id <-> uuid
    <script type="__bundler/template">        the document, as a JSON string

and writes the document out with `src="<uuid>"` rewritten to the file that uuid actually holds,
so the result opens, renders and diffs line by line.

**Read-only on the source.** The bundle is the artefact the client approved; nothing here writes
back to it. Repacking an edited document is a separate job and deliberately not this one.

Run: `python3 tools/extract-design-document.py <bundle.dc.html> --out <dir> [--apply]`
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import re
import sys
import zlib
from pathlib import Path

# What a bundle names its three blocks. The document is the point; the other two exist to
# make the document render.
BLOCKS = ("manifest", "ext_resources", "template")

EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/avif": ".avif",
       "font/woff2": ".woff2", "font/woff": ".woff", "text/javascript": ".js",
       "text/css": ".css", "image/svg+xml": ".svg"}


def safe(name: str) -> str:
    """A filename for a placeholder id. **Some ids are whole CDN URLs** -- the POS build vendors
    `https://unpkg.com/react@18.3.1/umd/react.production.min.js` and thirteen fonts the same way --
    and a URL used as a path makes directories out of `https:` and `unpkg.com`, which Windows
    refuses outright. Keeping the tail and flattening the rest stays readable and stays a file."""
    name = str(name).split("?")[0].rstrip("/")
    if "//" in name:
        name = name.split("//", 1)[1]
    name = name.rsplit("/", 1)[-1] if "/" in name else name
    return re.sub(r"[^A-Za-z0-9._@-]", "-", name) or "asset"


def blocks(text: str) -> dict:
    """The three bundler blocks, by name. Each one's payload is the line after its tag."""
    out = {}
    lines = text.split("\n")
    for i, line in enumerate(lines):
        m = re.search(r'<script type="__bundler/([a-z_]+)">', line)
        if m and m.group(1) in BLOCKS and i + 1 < len(lines):
            out[m.group(1)] = lines[i + 1]
    return out


def decode(entry: dict) -> bytes:
    """An asset's bytes. **`compressed` is a flag on 4 of the 48 and silently wrong to ignore** --
    the JS assets carry it, and writing the raw base64 for those produces a file that is not
    JavaScript and fails without saying why."""
    raw = base64.b64decode(entry.get("data") or "")
    if not entry.get("compressed"):
        return raw
    for attempt in (lambda b: gzip.decompress(b),
                    lambda b: zlib.decompress(b),
                    lambda b: zlib.decompress(b, -zlib.MAX_WBITS)):
        try:
            return attempt(raw)
        except Exception:
            continue
    # Better a file that is obviously the wrong shape than a silent half-write.
    print("     ! could not decompress; wrote the raw bytes", file=sys.stderr)
    return raw


def filename(uuid: str, entry: dict, name_of: dict) -> str:
    """The one place an asset's filename is decided, so the document's references and the files
    on disk cannot drift apart."""
    stem = safe(name_of.get(uuid, uuid))
    ext = EXT.get(entry.get("mime"), "")
    return stem if stem.endswith(ext) and ext else stem + ext


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--out", default=None, help="directory to write into (default: <stem>-unpacked)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    src = Path(a.bundle)
    if not src.exists():
        print("no such bundle: %s" % src, file=sys.stderr)
        return 1
    text = src.read_text(encoding="utf-8", errors="replace")
    found = blocks(text)
    missing = [b for b in BLOCKS if b not in found]
    if "template" in missing:
        print("no __bundler/template block -- this is not a Claude Design bundle", file=sys.stderr)
        return 1

    doc = json.loads(found["template"])
    manifest = json.loads(found["manifest"]) if "manifest" in found else {}
    ext = json.loads(found["ext_resources"]) if "ext_resources" in found else []
    name_of = {e["uuid"]: e["id"] for e in ext if isinstance(e, dict) and e.get("uuid")}

    out = Path(a.out) if a.out else src.parent / (src.stem + "-unpacked")
    print("%s  %.2f MB" % (src.name, src.stat().st_size / 1e6))
    print("  document   %.2f MB   %d sc-for, %d sc-if" %
          (len(doc) / 1e6, doc.count("sc-for"), doc.count("sc-if")))
    print("  assets     %d  (%d named by ext_resources, %d referenced by uuid only)" %
          (len(manifest), len(name_of), len(manifest) - len(name_of)))
    for b in missing:
        print("  no %s block" % b)

    # **Rewrite before writing, so the document on disk is the one that renders.** The bundle
    # points every image at a bare uuid, which resolves against the manifest and nothing else --
    # extracted without this the document is complete and every picture in it is broken.
    rewritten = 0
    for uuid, entry in manifest.items():
        target = "assets/" + filename(uuid, entry, name_of)
        if uuid in doc:
            doc = doc.replace(uuid, target)
            rewritten += 1
    print("  rewrote    %d uuid reference(s) to assets/" % rewritten)

    # **The other 29 never mention a uuid, and rewriting alone leaves them broken.** Images the
    # build reaches through `_P('ph20', 'photos/lemonade.jpg')` resolve against
    # `window.__resources`, which the bundler wrapper populates and an extracted document has no
    # way to know about -- so every one of them silently falls back to a `photos/...` path that
    # does not exist. The map is small, it is derivable here, and injecting it is the difference
    # between a document that renders and one that looks subtly empty.
    res = {name_of[u]: "assets/" + filename(u, manifest[u], name_of)
           for u in manifest if u in name_of}
    if res:
        inject = "<script>window.__resources=%s;</script>" % json.dumps(res, sort_keys=True)
        if "<head>" in doc:
            doc = doc.replace("<head>", "<head>" + chr(10) + inject, 1)
            print("  injected   window.__resources with %d placeholder(s)" % len(res))
        else:
            print("  ! no <head> to inject window.__resources into; %d image(s) will fall back"
                  % len(res))

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0

    (out / "assets").mkdir(parents=True, exist_ok=True)
    (out / (src.stem + ".html")).write_text(doc, encoding="utf-8")
    for uuid, entry in manifest.items():
        (out / "assets" / filename(uuid, entry, name_of)).write_bytes(decode(entry))
    print("  -> %s/%s.html  + %d asset(s)" % (out, src.stem, len(manifest)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
