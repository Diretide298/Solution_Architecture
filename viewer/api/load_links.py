#!/usr/bin/env python3
"""Load ticket-to-artefact links into ADAM's database in one go, on the ADAM server.

The file comes from `ticvai/tools/adam-links.py`: every OpenProject ticket and what it touches (operations,
services, tables, screens), built from the package. `POST /api/links` would do the same one row at a time, fetching
each ticket from OpenProject first (about 1 s each, ~5 hours for 18,000); here the tickets were already read in
bulk when the file was built, so the rows go straight in.

Safe to run again: the table's UNIQUE (project, kind, id, system, key) turns a repeat into a no-op, and a link
someone made by hand is never touched. Dry run unless --apply. Stop the ADAM API first or not; SQLite waits for it.

A link already there gets the file's cached ticket columns (subject, status, type, assignee) when the file carries
them, so a plan change such as a new assignee reaches ADAM's link lists too. --remove takes a JSON file whose
"tickets" object is keyed by OpenProject ids (tools/op-delete-rejected.rb's rejected.json): every OpenProject link
to those tickets is removed, because the tickets no longer exist.

  python3 load_links.py adam-links.json --email you@example.com             # dry run
  python3 load_links.py adam-links.json --email you@example.com --apply
  python3 load_links.py adam-links.json --email you@example.com --remove rejected.json --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--email", required=True, help="the ADAM account the links are recorded as made by")
    ap.add_argument("--db", default=os.environ.get("TICVAI_DB", str(Path(__file__).parent / "ticvai.db")))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--remove", help="JSON file with a 'tickets' object keyed by OpenProject ids whose links go")
    ap.add_argument("--prune", action="store_true",
                    help="for every ticket in the file, remove the bulk-loaded links (made by --email) the file no "
                         "longer has: a release's links replace the last release's instead of piling up")
    a = ap.parse_args()

    data = json.loads(Path(a.file).read_text(encoding="utf-8"))
    if not Path(a.db).exists():
        print(f"no database at {a.db}; pass --db or set TICVAI_DB")
        return 1
    conn = sqlite3.connect(a.db, timeout=30)
    project = conn.execute("SELECT id, name FROM project WHERE id = ?", (data["project"],)).fetchone()
    if not project:
        print(f"project '{data['project']}' is not in this ADAM database")
        return 1
    account = conn.execute("SELECT id, name FROM account WHERE email_folded = ?", (a.email.strip().lower(),)).fetchone()
    if not account:
        print(f"no ADAM account for {a.email}")
        return 1

    before = conn.execute("SELECT COUNT(*) FROM artefact_link WHERE project_id = ?", (project[0],)).fetchone()[0]
    existing = set(conn.execute("SELECT target_kind, target_id, external_key FROM artefact_link "
                                "WHERE project_id = ? AND external_system = 'openproject'", (project[0],)))
    new = [l for l in data["links"] if (l["kind"], l["id"], l["key"]) not in existing]
    cached = data.get("cached")
    old = [l for l in data["links"] if cached and (l["kind"], l["id"], l["key"]) in existing]
    gone = sorted(json.loads(Path(a.remove).read_text(encoding="utf-8"))["tickets"]) if a.remove else []
    drop = conn.execute(
        f"SELECT COUNT(*) FROM artefact_link WHERE project_id = ? AND external_system = 'openproject' "
        f"AND external_key IN ({','.join('?' * len(gone))})", (project[0], *gone)).fetchone()[0] if gone else 0
    want = {(l["kind"], l["id"], l["key"]) for l in data["links"]}
    in_file = {l["key"] for l in data["links"]}
    stale = [r for r in conn.execute(
        "SELECT id, target_kind, target_id, external_key FROM artefact_link WHERE project_id = ? "
        "AND external_system = 'openproject' AND created_by = ?", (project[0], account[0]))
        if r[3] in in_file and (r[1], r[2], r[3]) not in want] if a.prune else []
    print(f"prune: {len(stale)} links the file no longer has, on tickets it lists (made by this account)" if a.prune else "")
    print(f"ADAM project {project[0]} ({project[1]}), as {account[1] or a.email}: {len(data['links'])} links in the "
          f"file, {len(data['links']) - len(new)} already there, {len(new)} to add ({before} links in the project now)"
          f"; cached ticket columns refreshed on {len(old)}; {drop} links to {len(gone)} deleted tickets to remove"
          f"; database {a.db}")
    if not a.apply:
        print("dry run: nothing written. Add --apply to load.")
        return 0

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with conn:
        conn.executemany(
            "INSERT OR IGNORE INTO artefact_link (project_id, target_kind, target_id, external_system, external_key, "
            "url, cached_subject, cached_status, cached_type, cached_assignee, synced_at, created_at, created_by) "
            "VALUES (?, ?, ?, 'openproject', ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(project[0], l["kind"], l["id"], l["key"], l.get("url", ""), l.get("subject", ""), l.get("status", ""),
              l.get("type", ""), l.get("assignee", ""), now if data.get("cached") else "", now, account[0])
             for l in new])
        conn.executemany(
            "UPDATE artefact_link SET cached_subject = ?, cached_status = ?, cached_type = ?, cached_assignee = ?, "
            "synced_at = ? WHERE project_id = ? AND target_kind = ? AND target_id = ? "
            "AND external_system = 'openproject' AND external_key = ?",
            [(l.get("subject", ""), l.get("status", ""), l.get("type", ""), l.get("assignee", ""), now,
              project[0], l["kind"], l["id"], l["key"]) for l in old])
        if stale:
            conn.executemany("DELETE FROM artefact_link WHERE id = ?", [(r[0],) for r in stale])
        if gone:
            conn.execute(f"DELETE FROM artefact_link WHERE project_id = ? AND external_system = 'openproject' "
                         f"AND external_key IN ({','.join('?' * len(gone))})", (project[0], *gone))
    after = conn.execute("SELECT COUNT(*) FROM artefact_link WHERE project_id = ?", (project[0],)).fetchone()[0]
    print(f"done: {len(new)} links added, {len(old)} refreshed, {drop + len(stale)} removed; {after} in the project")
    return 0


if __name__ == "__main__":
    sys.exit(main())
