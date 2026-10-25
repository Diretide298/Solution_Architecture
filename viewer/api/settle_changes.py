#!/usr/bin/env python3
"""Settle change requests in ADAM and tell their tickets in OpenProject, from one decisions file, over the APIs.

Runs anywhere with network access (no server login): ADAM through its HTTP API as the account in ADAM_EMAIL and
ADAM_PASSWORD, OpenProject through its REST API with TICVAI_OP_TOKEN. For each decision:

  1. ADAM: POST /api/changes/<n>/resolve (status, resolution, ref) -- what the developer reads in ADAM. Sent with
     tell_ticket false, so this script tells the ticket itself and its dry run shows that first.
  2. The ticket the request was raised from is told (cr_notice.py, CHG-ADM-002; Chinmay, 14 October 2026: "whenever
     we have a cr we should create new tickets if ticket is closed. if not then add comment for the AI agent when
     he pulls"):
       - **still open** in OpenProject: one comment, headed "ADAM CR-011 · accepted — read before building",
         written for the AI agent that pulls it next (what was decided, which release carries it, what to do now).
         adam_pull puts it, and a "Change requests on this ticket" section, in the ticket's README.md;
       - **closed**: a CHILD TASK of the closed ticket for the change ("we create child tasks for CR remember
         that", Chinmay, 14 October), through ADAM's own /api/changes/<n>/ticket/preview and /apply (so ADAM
         records it as the request's child_key, and the description is ADAM's _ticket_text: the request, the
         decision and the release). That uses the OpenProject token ADAM_EMAIL connected in ADAM. ADAM refuses a
         ticket for a Done request, so the request is first settled as accepted with its decision, the child is
         filed, and only then is it marked done. The same comment goes on the child task. A rejection on a
         closed ticket gets the comment only: there is nothing to build;
       - once a request has its child task, later settlements tell that task instead.
     Step 2 runs before step 1's final write, for that reason. The ticket's own description is never rewritten.
     Migration work a request causes is a child task of the affected MIG-* ticket, assigned to the migration
     owner (ticvai/docs/active/team.json `migrations.owner`); this script does not file it (one child per
     request is ADAM's guard), the lead does, and the decision should name it.
  3. Optionally, files attached to that ticket (from disk, or `git show <ref>:<path>` so the file is the one the
     release tag holds), e.g. a derived file a developer's build needs.

**Dry run unless --apply**, and safe to run again: a request already at that status with that resolution is not
resolved twice, a ticket whose thread already starts a comment for that request and status is not commented twice
(the shorter heading written before 14 October counts too), a request that has a ticket never gets a second one,
and a file already attached under that name is not attached twice. OpenProject mail is off unless --notify.

Decisions file (JSON):

  {"project": "ticvai", "ref": "r4",
   "items": [
     {"cr": "CR-005", "status": "done", "resolution": "Option B: ...", "ref": "r4"},
     {"cr": "CR-008", "status": "rejected", "resolution": "Not in the package: ..."},
     {"cr": "CR-003", "status": "done", "resolution": "...",
      "attach": [{"git": "r4:ticvai/handoff/api-data-lineage.json"}, {"path": "notes.md", "name": "notes.md"}]},
     {"cr": "CR-011", "status": "accepted", "resolution": "...", "comment": false},
     {"raise": {"match": "CHG-R4-017", "target_kind": "other", "target_id": "CHG-R4-017",
                "title": "CHG-R4-017: ...", "problem": "...", "source": "audit", "source_ref": "..."},
      "status": "done", "resolution": "...", "ref": "r2", "comment": false}
   ]}

  status: open | accepted | rejected | done. `ref` (per item, else the file's) is recorded on the request as what
  settled it, and is the release the comment names. `comment: false` skips telling the ticket for that item (no
  comment and no new ticket). An item with `raise` instead of `cr` files the request first (POST /api/changes, the
  fields of ChangeIn) unless one whose title starts with `match` is already there -- the way a decision made
  outside ADAM gets its ADAM record -- and then settles it.

  `"release": false` (per item, else the file's) is a decision no release will carry (Chinmay, 25 October
  2026: "we dont need a Release for these"): the comment tells the agent the decision is the whole change and
  to build it in the ticket now, instead of leaving the changed part to a release. Give no `ref` with it.

  python3 settle_changes.py decisions.json            # dry run: what would change
  python3 settle_changes.py decisions.json --apply
  python3 settle_changes.py decisions.json --link-existing [--apply]
      # a closed ticket's child task made on the server (tools/op-create.rb, subject "[CR-nnn] ...") is linked
      # in ADAM (POST /api/changes/<n>/ticket/link, admin only) instead of a second one being made (CHG-ADM-003)

The branches are tested without a network by ticvai/tools/check-adam-cr-settlement.py (in run-checks.py).
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

# The wording and the decision are shared with ADAM's resolve route (main.py), from the file beside this one.
# Added explicitly because `python -I` leaves the script's own folder off sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cr_notice  # noqa: E402

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

    def served(self, project: str) -> str:
        """The release tag ADAM serves, so a comment says "your next pull already has it" only when it does
        (cr_notice._release_line; 15 October 2026). Blank when ADAM serves its working tree or cannot say."""
        if not hasattr(self, "_served"):
            try:
                got = self._req("GET", f"/api/board/mine?project_id={urllib.parse.quote(project)}") or {}
                self._served = (got.get("release") or {}).get("tag") or ""
            except RuntimeError:
                self._served = ""
        return self._served

    def changes(self, project: str) -> dict:
        got = self._req("GET", f"/api/changes?project_id={urllib.parse.quote(project)}")
        return {c["id"]: c for c in (got.get("items") or got.get("changes") or [])}

    def raise_change(self, project: str, fields: dict) -> dict:
        body = {k: v for k, v in fields.items() if k != "match"}
        body["project_id"] = project
        return self._post("/api/changes", body)

    def resolve(self, project: str, number: int, status: str, resolution: str, ref: str) -> dict:
        return self._post(f"/api/changes/{number}/resolve",
                          {"project_id": project, "status": status, "resolution": resolution, "ref": ref,
                           "tell_ticket": False})

    def link_ticket(self, project: str, number: int, key: str) -> dict:
        """Record a work package that already exists as the request's child task (admin only, CHG-ADM-003)."""
        return self._post(f"/api/changes/{number}/ticket/link", {"project_id": project, "key": str(key)})

    def new_ticket(self, project: str, number: int) -> dict:
        """The request's ticket, through ADAM's own preview and apply: ADAM records it as the child."""
        shown = self._post(f"/api/changes/{number}/ticket/preview", {"project_id": project})
        made = self._post(f"/api/changes/{number}/ticket/{shown['proposal']}/apply", {"project_id": project})
        return made["ticket"]


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

    def children(self, wp: str) -> list:
        """The work packages directly under `wp`, as (key, subject), from its children links."""
        got = self._req("GET", f"/work_packages/{wp}")
        out = []
        for c in ((got.get("_links") or {}).get("children") or []):
            key = str(c.get("href") or "").rstrip("/").rsplit("/", 1)[-1]
            if key.isdigit():
                out.append((key, c.get("title") or ""))
        return out

    def is_closed(self, wp: str) -> bool:
        """By OpenProject's own isClosed, never by the status's name."""
        got = self._req("GET", f"/work_packages/{wp}")
        embedded = (got.get("_embedded") or {}).get("status") or {}
        if "isClosed" in embedded:
            return bool(embedded["isClosed"])
        href = (((got.get("_links") or {}).get("status")) or {}).get("href") or ""
        sid = href.rstrip("/").rsplit("/", 1)[-1]
        return bool(self._req("GET", f"/statuses/{sid}").get("isClosed")) if sid.isdigit() else False

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
    return cr_notice.heading(cr, status)


def tell_ticket(adam, op, project: str, row: dict, cr: str, status: str, resolution: str, ref: str,
                apply: bool, notify: bool, prepare=None, link_existing: bool = False, release: bool = True) -> list:
    """Step 2 for one request: the lines to print. Changes nothing unless `apply`. Raises on a failure.

    `prepare` runs just before a child task is filed: it settles the request as accepted with its
    decision, so the child's description carries the decision and the request is not yet Done when
    ADAM files it (ADAM refuses a ticket for a Done request)."""
    ticket = str(row.get("ticket") or "").lstrip("#")
    child = str(row.get("childTicket") or "").lstrip("#")
    step = cr_notice.plan(status, ticket, child, closed=False)
    if step["action"] == "none":
        return [f"      ticket: nothing to tell ({step['why']})"]
    step = cr_notice.plan(status, ticket, child, op.is_closed(step["key"]))
    text = lambda key: cr_notice.comment_text(  # noqa: E731
        cr, row.get("title") or "", status, resolution, ref, key, (adam.served(project) if hasattr(adam, "served") else ""),
        row.get("artefacts") or [], release)

    if step["action"] == "ticket":
        if link_existing:
            # A child task made outside ADAM (tools/op-create.rb, subject "[CR-nnn] ...") is linked, not made again.
            there = next((k for k, subject in op.children(ticket) if subject.strip().startswith(f"[{cr}]")), None)
            if there:
                if not apply:
                    return [f"      #{ticket}: closed -> its child task #{there} ([{cr}] ...) would be linked in ADAM"]
                # No prepare(): ADAM records an existing child whatever the request's status.
                adam.link_ticket(project, row["number"], there)
                if not cr_notice.already_told(op.comments(there), cr, status):
                    op.comment(there, text(there), notify)
                return [f"      #{ticket}: closed -> child task #{there} linked in ADAM (commented)"]
        if not apply:
            return [f"      #{ticket}: closed -> a child task under it, with the request, the decision and the release"]
        if prepare:
            prepare()
        made = adam.new_ticket(project, row["number"])
        op.comment(str(made["key"]), text(str(made["key"])), notify)
        return [f"      #{ticket}: closed -> child task #{made['key']} under it (commented)"]

    there = cr_notice.already_told(op.comments(step["key"]), cr, status)
    lines = [f"      #{step['key']}: comment for the agent" + (" (already there)" if there else "")
             + f" -- {step['why']}"]
    if not there and apply:
        op.comment(step["key"], text(step["key"]), notify)
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("decisions")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--notify", action="store_true", help="let OpenProject mail the comment")
    ap.add_argument("--link-existing", action="store_true",
                    help="before filing a child task, link a child of the source ticket whose subject starts "
                         "\"[CR-nnn]\" (made on the server with tools/op-create.rb) instead of creating one")
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
    return settle(adam, op, spec, project, default_ref, a.apply, a.notify, Path(a.repo), a.link_existing)


def settle(adam, op, spec: dict, project: str, default_ref: str, apply: bool, notify: bool, repo: Path,
           link_existing: bool = False) -> int:
    current = adam.changes(project)
    mode = "APPLY" if apply else "dry run (--apply to change)"
    print(f"settle_changes: {len(spec['items'])} decision(s) for {project}; {mode}")
    failed = 0
    for it in spec["items"]:
        if it.get("raise") and not it.get("cr"):
            want = it["raise"]
            found = [c for c in current.values() if c["title"].startswith(want["match"])]
            if found:
                it = dict(it, cr=found[0]["id"])
            elif apply:
                made = adam.raise_change(project, want)
                row = made.get("change") or made
                current[row["id"]] = row
                print(f"  raised {row['id']}: {want['title'][:70]}")
                it = dict(it, cr=row["id"])
            else:
                print(f"  (new) {want['title'][:70]}: would be raised, then {it['status']}")
                continue
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
            same = (row["status"] == status and (row.get("resolution") or "").strip() == resolution
                    and (status == "open" or (row.get("resolvedRef") or "") == ref))
            print(f"  {cr} ({row['title'][:60]}): ADAM {row['status']} -> {status}"
                  + (" (already)" if same else ""))
            settled = {"done": same}

            def prepare(row=row, status=status, resolution=resolution, ref=ref, settled=settled):
                # Before a child task is filed: the request says what was decided and is not Done yet.
                if (row["status"] == "accepted" and (row.get("resolution") or "").strip() == resolution
                        and (row.get("resolvedRef") or "") == ref):
                    return
                adam.resolve(project, row["number"], "accepted", resolution, ref)
                # Accepted is where it ends, or a step on the way to done (even when it was done already).
                settled["done"] = status == "accepted"

            # 2 first, then 1: the ticket is told (a comment for the agent when it is open, a child task
            # when it is closed) before the request is written as settled, so a child task is filed while
            # the request is not yet Done. A failure here is reported and the request is still settled.
            if it.get("comment", True):
                try:
                    for line in tell_ticket(adam, op, project, row, cr, status, resolution, ref, apply, notify,
                                            prepare=prepare if status in ("accepted", "done") else None,
                                            link_existing=link_existing,
                                            release=it.get("release", spec.get("release", True))):
                        print(line)
                except Exception as e:  # noqa: BLE001
                    print(f"      ticket FAILED: {e}"); failed += 1
            # 1. ADAM
            if not settled["done"] and apply:
                adam.resolve(project, row["number"], status, resolution, ref)
            # 3. attachments
            for att in it.get("attach") or []:
                name, blob = read_attachment(att, repo)
                there = name in op.attachment_names(wp) if wp else True
                print(f"      #{wp}: attach {name} ({len(blob) // 1024} KB)" + (" (already there)" if there else ""))
                if not there and apply:
                    op.attach(wp, name, blob)
        except Exception as e:  # one bad request must not stop the rest
            print(f"      FAILED: {e}"); failed += 1
    print(f"settle_changes: {'done' if apply else 'nothing changed'}; {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
