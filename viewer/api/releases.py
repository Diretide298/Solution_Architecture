"""Which release of a package the viewer is serving, read from the files it writes.

The accounts service does not read packages; the viewer does (viewer/lib/releases.mjs).
What this service needs from that is small — which tag is in force, and when each
tag was made — and the viewer writes both beside its release exports:

    <releases>/served.json   the tag the viewer is serving right now, written on start
    <releases>/index.json    every r<N> tag with its commit and date

`<releases>` is the project's `releases` entry in projects.json, relative to that file,
and `.releases/<id>` when it has none — the same rule lib/projects.mjs applies, so the
two processes find the same folder from the same registry (TICVAI_PROJECTS for both in
a harness).

Nothing here is supplied by a caller. A ticket's pin is the tag in served.json, never a
tag somebody sends: a pin that could be set to anything would be a pin that means
nothing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from . import db

TAG = re.compile(r"^r([1-9]\d{0,5})$")


def tag_number(tag: str) -> int:
    found = TAG.match(tag or "")
    return int(found.group(1)) if found else 0


def _read(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def releases_dir(project_id: str) -> Path:
    registry = db.PROJECTS_PATH
    entry = {}
    doc = _read(Path(registry))
    for item in (doc or {}).get("projects") or []:
        if isinstance(item, dict) and item.get("id") == project_id:
            entry = item
            break
    return (Path(registry).parent / (entry.get("releases") or f".releases/{project_id}")).resolve()


def served(project_id: str) -> Optional[dict]:
    """The tag in force, or None while the working tree is served (or nothing is)."""
    doc = _read(releases_dir(project_id) / "served.json")
    if not doc or doc.get("mode") != "tag" or not TAG.match(doc.get("tag") or ""):
        return None
    return {"tag": doc["tag"], "commit": doc.get("commit") or "", "taggedAt": doc.get("taggedAt")}


def tags(project_id: str) -> list:
    """Every release tag, oldest first: {tag, commit, taggedAt}."""
    doc = _read(releases_dir(project_id) / "index.json") or {}
    out = [
        {"tag": r["tag"], "commit": r.get("commit") or "", "taggedAt": r.get("taggedAt")}
        for r in doc.get("releases") or []
        if isinstance(r, dict) and TAG.match(r.get("tag") or "")
    ]
    return sorted(out, key=lambda r: tag_number(r["tag"]))
