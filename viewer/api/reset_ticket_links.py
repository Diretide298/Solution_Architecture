#!/usr/bin/env python3
"""Clear a project's OpenProject ticket links and per-person release pins, on the ADAM server, before a fresh push.

Used when the tickets themselves are replaced (3 October 2026: TICVAI moved to a fresh OpenProject project, so every
ticket number changed). Links made to the old numbers and the pins people hold on them point at tickets that no
longer carry the work. Links to other systems, change requests and the pin history (ticket_pin_log) are kept.
Dry run unless --apply. Back the database up first.

  python3 reset_ticket_links.py --project ticvai --db /srv/ticvai/viewer/api/ticvai.db            # dry run
  python3 reset_ticket_links.py --project ticvai --db /srv/ticvai/viewer/api/ticvai.db --apply
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not Path(a.db).exists():
        print(f"no database at {a.db}")
        return 1
    conn = sqlite3.connect(a.db, timeout=30)
    if not conn.execute("SELECT 1 FROM project WHERE id = ?", (a.project,)).fetchone():
        print(f"project '{a.project}' is not in this ADAM database")
        return 1
    links = conn.execute("SELECT COUNT(*) FROM artefact_link WHERE project_id = ? AND external_system = 'openproject'",
                         (a.project,)).fetchone()[0]
    pins = conn.execute("SELECT COUNT(*) FROM ticket_pin WHERE project_id = ?", (a.project,)).fetchone()[0]
    print(f"project {a.project}: {links} OpenProject ticket links and {pins} release pins to clear "
          f"(other links, change requests and the pin history are kept); database {a.db}")
    if not a.apply:
        print("dry run: nothing written. Add --apply to clear.")
        return 0
    with conn:
        conn.execute("DELETE FROM artefact_link WHERE project_id = ? AND external_system = 'openproject'", (a.project,))
        conn.execute("DELETE FROM ticket_pin WHERE project_id = ?", (a.project,))
    print(f"done: {links} links and {pins} pins cleared")
    return 0


if __name__ == "__main__":
    sys.exit(main())
