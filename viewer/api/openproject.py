"""
Reading OpenProject, as whoever is asking.

**Every call here is made with the caller's own stored token, never a service
account.** That is the whole reason the settings page exists: a shared
credential would attribute every read — and later every write — to one robot,
and the audit trail is most of what a PMS is for.

Mostly read-through. The bridge still does not mint work package ids — every id
is OpenProject's, always — and it writes exactly four things, **each only after
the person has seen it and said yes** (see the proposals in main.py): the status,
the % done, a comment, and one new work package under an existing one.

**That last one is a reversal, and it is worth saying so.** This file used to
state plainly that the bridge does not create work packages, on the argument
that a second thing minting tickets is a second plan. The argument still holds
and the exception is narrow enough to live beside it: a change request that has
been accepted *is* work, it has to be scheduled somewhere, and the somewhere is
OpenProject. So one CR creates at most one ticket, as a child of the ticket the
CR came out of, once — `change_request.child_key` records which, and a second
attempt is refused rather than making a second ticket. What is not being built
is a way for this service to plan: there is no create that is not anchored to a
change request, and the caller cannot choose the project.

OpenProject holds the schedule — 23 epics, 444 features, 2,173 tasks in the
delivery plan — and this service holds the one thing OpenProject cannot express:
which artefact a work package is about. See `artefact_link` in db.py.

Two things bitten into this file, both from a real afternoon:

**Cloudflare refuses `Python-urllib` outright.** `pms.softlabsgroup.in` sits
behind it, and the default urllib User-Agent gets a 403 with error 1010 —
"blocked based on your browser's signature" — *before OpenProject sees the
request*. The token is never consulted. Reading that 403 as a rejected
credential accuses the one thing that was fine, so every request here names
itself and every 403 is checked for an edge signature before it is blamed on
auth.

**The instance is OpenProject 10.0.2**, which shipped September 2019. Nothing
used here is newer than that: `/api/v3/work_packages/{id}`, filters on the
collection, and HAL `_links` for the associated resources. Anything reached for
later should be checked against that version rather than the current docs.
"""

from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

# Named, so an edge does not refuse us for looking like a script. See above.
USER_AGENT = "ADAM-bridge/1.0 (+https://adam.ainfinite.ai)"

TIMEOUT = 20


class Refused(RuntimeError):
    """OpenProject said no. `status` is what it said."""

    def __init__(self, message: str, status: int = 0):
        super().__init__(message)
        self.status = status


class Blocked(RuntimeError):
    """Something in front of OpenProject refused before it was asked. Kept
    separate from `Refused` because the credential was never tested, and telling
    somebody their token is wrong when it was never tried is a wrong answer that
    costs an hour."""


def _looks_like_an_edge(body: str) -> bool:
    """A refusal from a proxy rather than from the application.

    Cloudflare's 1010 is the one seen here. The check is on the body because the
    status alone is a 403 either way, which is exactly why the first version of
    this got it wrong.
    """
    lowered = body.lower()
    return "cloudflare" in lowered or "error_code" in lowered and "1010" in lowered


def _openproject_message(body: str) -> str:
    """The sentence OpenProject put in an error body, when it put one there."""
    try:
        parsed = json.loads(body)
    except ValueError:
        return ""
    message = parsed.get("message") or ""
    # A 422 lists each field's complaint under _embedded.errors.
    for error in (parsed.get("_embedded") or {}).get("errors") or []:
        if error.get("message") and error["message"] not in message:
            message = f"{message} {error['message']}".strip()
    return message


def call(endpoint: str, token: str, path: str,
         params: Optional[dict] = None, method: str = "GET",
         body: Optional[dict] = None) -> Any:
    """
    One request against an OpenProject instance, as `token`.

    `path` is relative to `/api/v3`. The answer is parsed JSON; anything else
    raises rather than being handed on as a string that a caller will index into
    and get a character from. A GET is the normal case; `update`, `comment` and
    `create` below are the only callers that send anything else.
    """
    url = f"{endpoint.rstrip('/')}/api/v3/{path.lstrip('/')}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    auth = base64.b64encode(f"apikey:{token}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    writing = method != "GET"

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
            text = answer.read().decode("utf-8")
            # A write may answer with no body at all; that is success, not a parse error.
            return json.loads(text) if text.strip() else {}
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:4000]
        except Exception:  # noqa: BLE001 — a body that will not read is not the story
            pass
        if _looks_like_an_edge(body):
            raise Blocked(
                f"{endpoint} is behind a proxy that refused this service before "
                f"OpenProject saw the request. No credential was tested."
            ) from exc
        said = _openproject_message(body)
        # A write refused by OpenProject is about the change, not the token:
        # the same token just read the work package.
        if writing and exc.code == 403:
            raise Refused(
                f"OpenProject does not let you make that change. {said}".strip(), 403) from exc
        if writing and exc.code == 409:
            raise Refused(
                "Somebody changed this work package in OpenProject since it was read. "
                "Propose the change again.", 409) from exc
        if writing and exc.code == 422:
            raise Refused(f"OpenProject refused the change: {said or 'no reason given'}", 422) from exc
        if exc.code in (401, 403):
            raise Refused("OpenProject would not accept that token.", exc.code) from exc
        if exc.code == 404:
            raise Refused("No such work package.", 404) from exc
        raise Refused(f"OpenProject answered {exc.code}.", exc.code) from exc
    except Exception as exc:  # noqa: BLE001 — the network, in all its forms
        raise Refused(f"Could not reach {endpoint}: {exc}") from exc


def _titled(link: Optional[dict]) -> str:
    """The human name off a HAL `_links` entry. HAL gives every association an
    href and a title, and the title is the only part worth showing."""
    return (link or {}).get("title") or ""


def _id_from_href(href: Optional[str]) -> Optional[int]:
    """`/api/v3/projects/153` -> 153. None for anything else."""
    tail = (href or "").rstrip("/").rsplit("/", 1)[-1]
    return int(tail) if tail.isdigit() else None


def summarise(work_package: dict, endpoint: str) -> dict:
    """
    A work package, flattened to the fields a board or a tool actually shows.

    The HAL document is large and mostly hrefs. This keeps what a person reads —
    who it is for, what state it is in, when it is due — and the URL, because a
    row nobody can open is a row that gets ignored.
    """
    links = work_package.get("_links", {})
    key = str(work_package.get("id", ""))
    return {
        "key": key,
        "subject": work_package.get("subject", ""),
        "type": _titled(links.get("type")),
        "status": _titled(links.get("status")),
        "assignee": _titled(links.get("assignee")),
        "priority": _titled(links.get("priority")),
        # Versions are how the delivery plan's six milestones land here, so this
        # is the field that answers "which milestone is this in".
        "version": _titled(links.get("version")),
        "project": _titled(links.get("project")),
        # The number, off the end of the HAL href. What the ADAM project's
        # choice is compared against — titles can repeat, ids cannot.
        "projectId": _id_from_href((links.get("project") or {}).get("href")),
        # The ticket this one hangs under, when there is one. An epic on a
        # delivery overview is only an epic because its children say so.
        "parent": _id_from_href((links.get("parent") or {}).get("href")),
        "parentSubject": _titled(links.get("parent")),
        "startDate": work_package.get("startDate"),
        "dueDate": work_package.get("dueDate"),
        "percentDone": work_package.get("percentageDone"),
        # Both ends of the ticket's life. `createdAt` is what "how long did this
        # take" is measured from; on a closed ticket `updatedAt` is the closest
        # thing to a closing date this API offers without reading activities.
        "createdAt": work_package.get("createdAt"),
        "updatedAt": work_package.get("updatedAt"),
        # What a write has to send back, so OpenProject can refuse one made
        # against a version somebody has since changed.
        "lockVersion": work_package.get("lockVersion"),
        # The address a person opens. Built rather than taken from `_links.self`,
        # which is the API path and not the page.
        "url": f"{endpoint.rstrip('/')}/work_packages/{key}" if key else "",
    }


# A work package's description can be a whole spec. Enough to work from; the
# rest is one click away at `url`.
DESCRIPTION_LIMIT = 20_000


def work_package(endpoint: str, token: str, key: str) -> dict:
    """One, summarised, with its description — the part a developer works from.
    Lists leave the description out; one ticket keeps it."""
    raw = call(endpoint, token, f"work_packages/{key}")
    found = summarise(raw, endpoint)
    text = ((raw.get("description") or {}).get("raw") or "").strip()
    found["description"] = text[:DESCRIPTION_LIMIT]
    if len(text) > DESCRIPTION_LIMIT:
        found["descriptionTrimmed"] = True
    return found


def statuses(endpoint: str, token: str) -> list:
    """Every status on the instance, as `{id, name, isClosed}`, in OpenProject's order.
    Whether a given change is *allowed* is OpenProject's call, made when it is sent."""
    page = call(endpoint, token, "statuses")
    return [
        {"id": st.get("id"), "name": st.get("name", ""), "isClosed": bool(st.get("isClosed"))}
        for st in page.get("_embedded", {}).get("elements", [])
    ]


def update(endpoint: str, token: str, key: str, lock_version: int,
           status_id: Optional[int] = None, percent_done: Optional[int] = None) -> dict:
    """
    Change the status and/or % done, as the owner of `token`.

    `lockVersion` is the version that was read when the change was proposed. If
    anybody has touched the work package since, OpenProject answers 409 and
    nothing changes — the person agreed to a change against what they saw.
    """
    body: dict = {"lockVersion": lock_version}
    if percent_done is not None:
        body["percentageDone"] = percent_done
    if status_id is not None:
        body["_links"] = {"status": {"href": f"/api/v3/statuses/{status_id}"}}
    raw = call(endpoint, token, f"work_packages/{key}", method="PATCH", body=body)
    return summarise(raw, endpoint)


def types(endpoint: str, token: str, project_id: int) -> list:
    """The work package types this project offers, as `{id, name, isDefault}`.

    Per project rather than instance-wide: OpenProject lets a project enable a
    subset, and offering a type the project has turned off produces a 422 at
    the moment of creation — after the person has already said yes, which is
    the worst possible time to find out.
    """
    page = call(endpoint, token, f"projects/{project_id}/types")
    return [
        {"id": t.get("id"), "name": t.get("name", ""),
         "isDefault": bool(t.get("isDefault")), "isMilestone": bool(t.get("isMilestone"))}
        for t in page.get("_embedded", {}).get("elements", [])
    ]


def create(endpoint: str, token: str, project_id: int, subject: str,
           description: str = "", type_id: Optional[int] = None,
           parent_key: Optional[str] = None) -> dict:
    """Create one work package, as the owner of `token`.

    The only create in this file, and the caller does not choose the project:
    `project_id` comes from the ADAM project's mapping, so a ticket cannot be
    filed into somebody else's plan by naming a different number.

    `parent_key` is the ticket this one hangs under. Sent as a link rather than
    set afterwards, so the ticket is never briefly parentless — a top-level
    ticket that acquires a parent a second later still shows up in whatever
    read the project between the two.
    """
    body: dict = {"subject": subject.strip()[:255]}
    if description:
        body["description"] = {"raw": description}
    links: dict = {}
    if type_id is not None:
        links["type"] = {"href": f"/api/v3/types/{type_id}"}
    if parent_key:
        links["parent"] = {"href": f"/api/v3/work_packages/{parent_key}"}
    if links:
        body["_links"] = links
    raw = call(endpoint, token, f"projects/{project_id}/work_packages",
               method="POST", body=body)
    return summarise(raw, endpoint)


def comment(endpoint: str, token: str, key: str, text: str) -> None:
    """Add a comment to the work package's activity, as the owner of `token`."""
    call(endpoint, token, f"work_packages/{key}/activities",
         method="POST", body={"comment": {"raw": text}})


def projects(endpoint: str, token: str) -> list:
    """
    Every project this token can see, as `{id, identifier, name}`, by name.

    Paged by hand because nothing guarantees one page holds them all; the loop
    stops on a short page, and on a page count no real instance reaches.
    """
    found, offset, size = {}, 1, 200
    for _ in range(50):
        page = call(endpoint, token, "projects", {"pageSize": size, "offset": offset})
        elements = page.get("_embedded", {}).get("elements", [])
        before = len(found)
        for project in elements:
            found[project.get("id")] = {
                "id": project.get("id"),
                "identifier": project.get("identifier", ""),
                "name": project.get("name", ""),
            }
        total = page.get("total")
        # An instance that ignores paging hands back the same page every time;
        # a page that adds nothing new ends the walk rather than repeating it.
        if (len(elements) < size or len(found) == before
                or (isinstance(total, int) and len(found) >= total)):
            break
        offset += 1
    return sorted(found.values(), key=lambda p: (p["name"] or "").lower())


def everything(endpoint: str, token: str, project_id: int, limit: int = 2000) -> list:
    """
    Every work package in one OpenProject project, in every state.

    The opposite end from `mine`: that answers "what am I holding", this answers
    "where is the delivery". So the status filter is `*` — the closed and the
    rejected are the whole point of an overview, and leaving them out would make
    every count a count of unfinished work wearing the name of the total.

    Paged the way `projects` is, and for the same reasons: nothing promises a
    page holds them all, and an instance that ignores paging must not spin. The
    `limit` is a ceiling on rows, not on pages — a project bigger than it is cut
    off oldest-first, because the walk is newest first.
    """
    found, offset, size = {}, 1, 200
    filters = json.dumps([
        {"project": {"operator": "=", "values": [str(project_id)]}},
        {"status": {"operator": "*", "values": []}},
    ])
    for _ in range(50):
        page = call(endpoint, token, "work_packages", {
            "filters": filters,
            "pageSize": size,
            "offset": offset,
            "sortBy": json.dumps([["updatedAt", "desc"]]),
        })
        elements = page.get("_embedded", {}).get("elements", [])
        before = len(found)
        for raw in elements:
            summary = summarise(raw, endpoint)
            found[summary["key"]] = summary
        total = page.get("total")
        if (len(elements) < size or len(found) == before or len(found) >= limit
                or (isinstance(total, int) and len(found) >= total)):
            break
        offset += 1
    return list(found.values())[:limit]


def mine(endpoint: str, token: str, limit: int = 100,
         project_id: Optional[int] = None) -> list:
    """
    What is assigned to the owner of this token and still open.

    `assignee = me` is an OpenProject filter operator rather than an id, which
    is what makes this answer correctly without the caller knowing their own
    user id. `status: o` is the built-in "open" set — asking for every status
    would return the closed ones too, and a board of finished work is not a
    board.
    """
    wanted = [
        {"assignee": {"operator": "=", "values": ["me"]}},
        {"status": {"operator": "o", "values": [""]}},
    ]
    # Only the project the ADAM package is scheduled in. Without it the board
    # is everything assigned to you anywhere on the instance.
    if project_id is not None:
        wanted.append({"project": {"operator": "=", "values": [str(project_id)]}})
    filters = json.dumps(wanted)
    page = call(endpoint, token, "work_packages", {
        "filters": filters,
        "pageSize": max(1, min(limit, 200)),
        "sortBy": json.dumps([["updatedAt", "desc"]]),
    })
    elements = page.get("_embedded", {}).get("elements", [])
    return [summarise(wp, endpoint) for wp in elements]
