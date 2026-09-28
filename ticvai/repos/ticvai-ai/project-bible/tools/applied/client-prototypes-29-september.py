#!/usr/bin/env python3
"""Point every P01, P02 and P04 screen at the view that shows it in the client's own prototype.

The client approved three clickable prototypes: guest web and guest mobile at rev 3 (feedback 25 September,
handed over 28 September), and the POS terminal (client-approved, build 2026.08.14). Each screen had a
generated or Claude Design board and no link to the thing the client actually signed off, so a developer
built the layout from a board the client never saw.

For each screen the mapping (handoff/prototype-maps/map-<P>.json, one agent per prototype on 29 September,
every match cited to a component or string in the prototype source) gives the view, how good the match is,
and what the prototype does that the screen definition does not. This writes it into the screen's
`wireframe.prototype` block and sets `wireframe.provenance: client-verified` where the prototype shows the
screen. A screen the prototype does not show keeps its board and is built from its definition (decided
29 September: "if something is missing we build the rest").

`wireframe.status` is untouched: it describes the board file, not where the design came from
(check-wireframes). Idempotent: a second run writes nothing.

    python tools/applied/client-prototypes-29-september.py [--apply]
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / "handoff" / "prototype-maps"
PROTOS = {
    "P01": ("screens/P01-guest-web-storefront.yaml",
            "sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html", "rev 3", "2026-09-28"),
    "P02": ("screens/P02-guest-mobile-app.yaml",
            "sources/designs/guest-rev3-28-september/TICVAI Guest Booking Mobile v2.dc.html", "rev 3", "2026-09-28"),
    "P04": ("screens/P04-point-of-sale.yaml",
            "sources/designs/TICVAI_POS_Terminal_client_approved.html", "TICVAI OS 4.2.1, build 2026.08.14",
            "2026-09-10"),
}


def q(s):
    """A single-quoted YAML scalar on one line."""
    return "'" + re.sub(r"\s+", " ", str(s)).strip().replace("'", "''") + "'"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    for code, (yml, proto, rev, verified) in PROTOS.items():
        assert (ROOT / proto).exists(), proto
        m = json.loads((MAPS / f"map-{code}.json").read_text(encoding="utf-8"))
        by_id = {s["id"]: s for s in m["screens"]}
        path = ROOT / yml
        text = path.read_text(encoding="utf-8")
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.split(nl)
        out, cur, n_set, n_none = [], None, 0, 0
        i = 0
        while i < len(lines):
            ln = lines[i]
            mm = re.match(r"^- id: (\S+)", ln)
            if mm:
                cur = mm.group(1)
            # Drop a prototype block written by an earlier run, so a rerun rewrites it rather than doubling it.
            if ln == "    prototype:":
                i += 1
                while i < len(lines) and lines[i].startswith("      "):
                    i += 1
                continue
            s = by_id.get(cur)
            if s and ln.startswith("    provenance: ") and s["match"] in ("exact", "partial"):
                ln = "    provenance: client-verified"
            out.append(ln)
            if s and ln.startswith("    board: ") and (i + 1 >= len(lines) or not lines[i + 1].startswith("    prototype:")):
                if s["match"] == "none":
                    n_none += 1
                    block = [f"      file: {q(proto)}", f"      rev: {q(rev)}", "      match: none",
                             "      note: 'The prototype has no view for this screen. Build it from this definition "
                             "with the generated layout (decided 29 September).'"]
                else:
                    n_set += 1
                    block = [f"      file: {q(proto)}", f"      rev: {q(rev)}", f"      verified: {verified}",
                             f"      match: {s['match']}", f"      view: {q(s['view'])}"]
                    if s.get("differences"):
                        block.append(f"      differences: {q(s['differences'])}")
                out += ["    prototype:"] + block
            i += 1
        missing = [sid for sid in by_id if not re.search(rf"^- id: {re.escape(sid)}\s*$", text, re.M)]
        print(f"{code}: {n_set} screens point at a prototype view, {n_none} have none; not in the YAML: {missing}")
        new = nl.join(out)
        if a.apply and new != text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    if not a.apply:
        print("dry run; pass --apply")


if __name__ == "__main__":
    main()
