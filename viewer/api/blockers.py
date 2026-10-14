"""Which open blocking change requests affect a ticket (CHG-ADM-004).

**The lead's rule, 14 October 2026** (Chinmay): "if there is blocker we log it as CR always. and than scour for
next tasks that can be completed and if existing blockers effect it". An agent that hits a blocker raises a CR with
`blocking` set and proposes the ticket On hold; then it looks down the board for the next ticket it can finish. This
makes "can it finish this one" a lookup rather than a guess.

A CR **blocks** while it is `blocking` and either open, or accepted and not yet in a release ADAM serves (its
`resolved_ref` is not a release tag at or below the one served). Done and rejected requests block nothing.

A CR **affects** a ticket when:
  - it was raised from that ticket (and the ticket is not the CR's own child task, which is the work that settles it);
  - or one of its artefacts (its target, and every `kind:id` in `artefact_ids`) is one the ticket is linked to:
    the same operation (compared by operationId, so `lending#borrowBook` and `borrowBook` agree), table, schema,
    screen, journey or service;
  - or it names a table that an operation the ticket is linked to reads or writes, by the package's lineage
    (`handoff/api-data-lineage.json` of the release ADAM serves).

The matching is pure (`affecting`), so a check can run it on stand-in data; the reads around it are cached
(the lineage by file and modification time) and cost one query per board.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from . import db, releases

_LINEAGE: dict = {}


def _norm(kind: str, ident: str):
    kind = (kind or "").strip().lower()
    ident = (ident or "").strip()
    if not kind or not ident:
        return None
    if kind == "operation":
        ident = ident.split("#")[-1]
    return kind, ident.lower()


def cr_artefacts(target_kind: str, target_id: str, artefact_ids) -> set:
    """Every artefact a CR names, normalised: its target and each `kind:id` it lists."""
    out = set()
    first = _norm(target_kind, target_id)
    if first:
        out.add(first)
    for item in artefact_ids or []:
        kind, _, ident = str(item).partition(":")
        found = _norm(kind, ident) if ident else None
        if found:
            out.add(found)
    return out


def ticket_artefacts(links, lineage: dict) -> dict:
    """What a ticket touches, normalised, each with how: its links, and the tables its operations read or write."""
    out: dict = {}
    for link in links or []:
        found = _norm(link.get("kind", ""), link.get("id", ""))
        if not found:
            continue
        out.setdefault(found, f"{link['kind']} {link['id']}")
        if found[0] == "operation":
            for table in (lineage or {}).get(found[1], ()):
                out.setdefault(("table", table), f"table {table}, which {link['id']} reads or writes")
    return out


def blocks(status: str, blocking, resolved_ref: str, served_tag: str) -> bool:
    """Whether a CR still blocks: blocking, and open or accepted-not-yet-released."""
    if not blocking:
        return False
    if status == "open":
        return True
    if status != "accepted":
        return False
    released = releases.tag_number(resolved_ref or "")
    return not (released and released <= releases.tag_number(served_tag or ""))


def affecting(key: str, links, crs, lineage: dict, served_tag: str = "") -> list:
    """The blocking CRs that affect ticket `key`, as `{id, number, title, status, via}`, oldest first.

    `crs` are dicts with number, title, status, blocking, external_key, child_key, target_kind, target_id,
    artefact_ids (a list), resolved_ref; `links` the ticket's `{kind, id}`; `lineage` operationId (lower case)
    -> the tables it reads or writes.
    """
    key = str(key or "").lstrip("#")
    touches = ticket_artefacts(links, lineage)
    out = []
    for cr in sorted(crs, key=lambda c: c["number"]):
        if not blocks(cr["status"], cr["blocking"], cr.get("resolved_ref", ""), served_tag):
            continue
        if key and str(cr.get("child_key") or "") == key:
            continue
        via = ""
        if key and str(cr.get("external_key") or "") == key:
            via = "raised from this ticket"
        else:
            for art in sorted(cr_artefacts(cr["target_kind"], cr["target_id"], cr.get("artefact_ids"))):
                if art in touches:
                    via = touches[art]
                    break
        if via:
            out.append({"id": f"CR-{cr['number']:03d}", "number": cr["number"], "title": cr["title"],
                        "status": cr["status"], "via": via})
    return out


# ── the reads around it ──────────────────────────────────────────────

def package_dir(project_id: str) -> Optional[Path]:
    """The tree ADAM serves for a project: the served tag's export, else the project's root."""
    served = releases.served(project_id)
    if served:
        return releases.releases_dir(project_id) / served["tag"]
    try:
        doc = json.loads(Path(db.PROJECTS_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for item in doc.get("projects") or []:
        if isinstance(item, dict) and item.get("id") == project_id and item.get("root"):
            return (Path(db.PROJECTS_PATH).parent / item["root"]).resolve()
    return None


def lineage(project_id: str) -> dict:
    """operationId (lower case) -> the tables it reads or writes, from the served tree's lineage. Cached by file and
    modification time; empty when there is none, which only means no table-level matches."""
    base = package_dir(project_id)
    path = base / "handoff" / "api-data-lineage.json" if base else None
    try:
        stamp = path.stat().st_mtime_ns if path else None
    except OSError:
        stamp = None
    if not stamp:
        return {}
    held = _LINEAGE.get(str(path))
    if held and held[0] == stamp:
        return held[1]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    table = re.compile(r"^[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*$")
    out = {}
    for op, entry in (doc.items() if isinstance(doc, dict) else []):
        if not isinstance(entry, dict):
            continue
        tables = {t.lower() for t in (entry.get("reads") or []) + (entry.get("writes") or [])
                  if isinstance(t, str) and table.match(t.lower())}
        if tables:
            out[str(op).lower()] = tables
    _LINEAGE.clear()
    _LINEAGE[str(path)] = (stamp, out)
    return out


def blocking_crs(project_id: str) -> list:
    """The project's CRs that could block anything: blocking, open or accepted. One query."""
    rows = db.all_rows(
        "SELECT number, title, status, blocking, external_key, child_key, target_kind, target_id, "
        "artefact_ids, resolved_ref FROM change_request WHERE project_id = ? AND blocking = 1 "
        "AND status IN ('open', 'accepted')", (project_id,))
    out = []
    for r in rows:
        try:
            arts = json.loads(r["artefact_ids"] or "[]")
        except ValueError:
            arts = []
        out.append({"number": r["number"], "title": r["title"], "status": r["status"], "blocking": bool(r["blocking"]),
                    "external_key": r["external_key"] or "", "child_key": r["child_key"] or "",
                    "target_kind": r["target_kind"], "target_id": r["target_id"],
                    "artefact_ids": arts if isinstance(arts, list) else [], "resolved_ref": r["resolved_ref"] or ""})
    return out


class Board:
    """One board's worth of the lookup: the CRs, the lineage and the served tag read once."""

    def __init__(self, project_id: str):
        self.crs = blocking_crs(project_id)
        self.lineage = lineage(project_id) if self.crs else {}
        served = releases.served(project_id) if self.crs else None
        self.served = served["tag"] if served else ""

    def of(self, key: str, links) -> list:
        return affecting(key, links, self.crs, self.lineage, self.served) if self.crs else []
