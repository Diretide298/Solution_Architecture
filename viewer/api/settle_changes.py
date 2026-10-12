#!/usr/bin/env python3
"""Settle change requests in ADAM and tell their tickets in OpenProject, from one decisions file, over the APIs.

Runs anywhere with network access (no server login): ADAM through its HTTP API as the account in ADAM_EMAIL and
ADAM_PASSWORD, OpenProject through its REST API with TICVAI_OP_TOKEN. For each decision:

  1. ADAM: POST /api/changes/<n>/resolve (status, resolution, ref) -- what the developer reads in ADAM.
  2. OpenProject: one comment on the ticket the request was raised from, headed "ADAM CR-011 · accepted", so the
     ticket's history says what was decided without opening ADAM.
  3. Optionally, files attached to that ticket (from disk, or `git show <ref>:<path>` so the file is the one the
     release tag holds), e.g. a derived file a developer's build needs.

**Dry run unless --apply**, and safe to run again: a request already at that status with that resolution is not
resolved twice, a ticket that already has the comment's heading is not commented twice, and a file already attached
under that name is not attached twice. OpenProject mail is off unless --notify.

Decisions file (JSON):

  {"project": "ticvai", "ref": "r4",
   "items": [
     {"cr": "CR-005", "status": "done", "resolution": "Option B: ...", "ref": "r4"},
     {"cr": "CR-008", "status": "rejected", "resolution": "Not in the package: ..."},
     {"cr": "CR-003", "status": "done", "resolution": "...",
      "attach": [{"git": "r4:ticvai/handoff/api-data-lineage.json"}, {"path": "notes.md", "name": "notes.md"}]},
     {"cr": "CR-011", "status": "accepted", "resolution": "...", "comment": false}
   ]}

  status: open | accepted | rejected | done. `ref` (per item, else the file's) is recorded on the request as what
  settled it. `comment: false` skips the OpenProject comment for that item.

  python3 settle_changes.py decisions.json            # dry run: what would change
  python3 settle_changes.py decisions.json --apply
"""
from __future__ import annotations

import argparse
import base64
import http.cookiejar
import json
import mimetypes
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

STATUSES = ("open", "accepted", "rejected", "done")
UA = "curl/8.0"  # the OpenProject host's firewall refuses Python's default agent


def die(msg: str) -> None:
    print(f"settle_changes: {msg}", file=sys.stderr)
    sys.exit(2)


class Adam:
    def __init__(self, base: str, email: str, password: str):
        self.base = base.rstrip("/")
        self.http = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self._post("/api/auth/login", {"email": email, "password": password})

    def _req(self, method: str, path: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method,
                                     headers={"content-type": "application/json", "user-agent": UA})
        try:
            with self.http.open(req, timeout=60) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            raise RuntimeError(f"ADAM {method} {path}: {e.code} {detail}") from None

    def _post(self, path, body):
        return self._req("POST", path, body)

    def changes(self, project: str) -> dict:
        got = self._req("GET", f"/api/changes?project_id={urllib.parse.quote(project)}")
        return {c["id"]: c for c in (got.get("items") or got.get("changes") or [])}

    def resolve(self, project: str, number: int, status: str, resolution: str, ref: str) -> dict:
        return self._post(f"/api/changes/{number}/resolve",
                          {"project_id": project, "status": status, "resolution": resolution, "ref": ref})


class OpenProject:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/") + "/api/v3"
        self.auth = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()

    def _req(self, method: str, path: str, data=None, ctype="application/json"):
        req = urllib.request.Request(self.base + path, data=data, method=method,
                                     headers={"authorization": self.auth, "user-agent": UA, "content-type": ctype})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            raise RuntimeError(f"OpenProject {method} {path}: {e.code} {detail}") from None

    def comments(self, wp: str) -> list:
        got = self._req("GET", f"/work_packages/{wp}/activities")
        return [((a.get("comment") or {}).get("raw") or "") for a in got["_embedded"]["elements"]]

    def comment(self, wp: str, text: str, notify: bool) -> None:
        self._req("POST", f"/work_packages/{wp}/activities?notify={'true' if notify else 'false'}",
                  json.dumps({"comment": {"raw": text}}).encode())

    def attachment_names(self, wp: str) -> set:
        got = self._req("GET", f"/work_packages/{wp}/attachments")
        return {a.get("fileName") for a in got["_embedded"]["elements"]}

    def attach(self, wp: str, name: str, blob: bytes) -> None:
        b = uuid.uuid4().hex
        ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
        meta = json.dumps({"fileName": name}).encode()
        body = (f"--{b}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
                f"Content-Type: application/json\r\n\r\n").encode() + meta + \
               (f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode() + blob + f"\r\n--{b}--\r\n".encode()
        self._req("POST", f"/work_packages/{wp}/attachments", body, f"multipart/form-data; boundary={b}")


def read_attachment(spec: dict, repo: Path) -> tuple[str, bytes]:
    if spec.get("git"):
        ref, _, path = spec["git"].partition(":")
        out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=repo, capture_output=True)
        if out.returncode:
            raise RuntimeError(f"git show {spec['git']}: {out.stderr.decode().strip()}")
        return spec.get("name") or Path(path).name, out.stdout
    p = Path(spec["path"])
    return spec.get("name") or p.name, p.read_bytes()


def heading(cr: str, status: str) -> str:
    return f"**ADAM {cr} · {status}**"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("decisions")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--notify", action="store_true", help="let OpenProject mail the comment")
    ap.add_argument("--adam", default=os.environ.get("ADAM_VIEWER_URL", "https://adam.ainfinite.ai"))
    ap.add_argument("--pms", default=os.environ.get("TICVAI_PMS_URL", "https://pms.softlabsgroup.in"))
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]), help="git checkout for `git:` files")
    a = ap.parse_args()

    spec = json.loads(Path(a.decisions).read_text(encoding="utf-8"))
    project, default_ref = spec.get("project") or "ticvai", spec.get("ref") or ""
    for need in ("ADAM_EMAIL", "ADAM_PASSWORD", "TICVAI_OP_TOKEN"):
        if not os.environ.get(need):
            die(f"{need} is not set")
    adam = Adam(a.adam, os.environ["ADAM_EMAIL"], os.environ["ADAM_PASSWORD"])
    op = OpenProject(a.pms, os.environ["TICVAI_OP_TOKEN"])
    current = adam.changes(project)

    mode = "APPLY" if a.apply else "dry run (--apply to change)"
    print(f"settle_changes: {len(spec['items'])} decision(s) for {project}; {mode}")
    failed = 0
    for it in spec["items"]:
        cr = it["cr"].upper()
        status = it["status"].strip().lower()
        resolution = (it.get("resolution") or "").strip()
        ref = (it.get("ref") or default_ref).strip()
        if status not in STATUSES:
            print(f"  {cr}: status {status!r} is not one of {', '.join(STATUSES)}"); failed += 1; continue
        row = current.get(cr)
        if not row:
            print(f"  {cr}: not in ADAM's {project} requests"); failed += 1; continue
        wp = str(row.get("ticket") or "").lstrip("#")
        try:
            # 1. ADAM
            same = (row["status"] == status and (row.get("resolution") or "").strip() == resolution
                    and (status == "open" or (row.get("resolvedRef") or "") == ref))
            print(f"  {cr} ({row['title'][:60]}): ADAM {row['status']} -> {status}"
                  + (" (already)" if same else ""))
            if not same and a.apply:
                adam.resolve(project, row["number"], status, resolution, ref)
            # 2. OpenProject comment
            if wp and it.get("comment", True):
                head = heading(cr, status)
                there = any(c.startswith(head) for c in op.comments(wp))
                print(f"      #{wp}: comment" + (" (already there)" if there else ""))
                if not there and a.apply:
                    text = (f"{head}\n\n{resolution}\n\n"
                            + (f"Settled at release `{ref}`. " if ref and status == "done" else "")
                            + f"Pull it again in ADAM: `/ticket {wp}`.")
                    op.comment(wp, text, a.notify)
            # 3. attachments
            for att in it.get("attach") or []:
                name, blob = read_attachment(att, Path(a.repo))
                there = name in op.attachment_names(wp) if wp else True
                print(f"      #{wp}: attach {name} ({len(blob) // 1024} KB)" + (" (already there)" if there else ""))
                if not there and a.apply:
                    op.attach(wp, name, blob)
        except Exception as e:  # one bad request must not stop the rest
            print(f"      FAILED: {e}"); failed += 1
    print(f"settle_changes: {'done' if a.apply else 'nothing changed'}; {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
