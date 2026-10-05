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
import re
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
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


def hours(duration: Optional[str]) -> Optional[float]:
    """An ISO 8601 duration as hours, or None.

    OpenProject reports time as `PT8H30M`, `P1DT4H`, `PT45M`. Parsed here rather
    than on the page because two readers of the same format is one too many, and
    because getting it wrong is invisible: a bad parse returns a plausible
    number, not an error.

    A day is **eight hours, not twenty-four.** OpenProject's own `P1D` on a time
    entry means a working day, and treating it as elapsed time would triple
    every cost that came from one. A week is five of those.
    """
    text = (duration or "").strip().upper()
    if not text.startswith("P"):
        return None
    total = 0.0
    number = ""
    in_time = False
    for ch in text[1:]:
        if ch == "T":
            in_time = True
            number = ""
            continue
        if ch.isdigit() or ch == ".":
            number += ch
            continue
        try:
            value = float(number) if number else 0.0
        except ValueError:
            return None
        number = ""
        if ch == "W":
            total += value * 5 * 8
        elif ch == "D":
            total += value * 8
        elif ch == "H":
            total += value
        elif ch == "M":
            # Ambiguous in ISO 8601 and unambiguous here: before the T it is
            # months and after it is minutes. Months are not a time entry, so
            # one before the T is a value this cannot use.
            if not in_time:
                return None
            total += value / 60
        elif ch == "S":
            total += value / 3600
        else:
            return None
    return round(total, 4)


def _titled(link: Optional[dict]) -> str:
    """The human name off a HAL `_links` entry. HAL gives every association an
    href and a title, and the title is the only part worth showing."""
    return (link or {}).get("title") or ""


def _id_from_href(href: Optional[str]) -> Optional[int]:
    """`/api/v3/projects/153` -> 153. None for anything else."""
    tail = (href or "").rstrip("/").rsplit("/", 1)[-1]
    return int(tail) if tail.isdigit() else None


# "Build order #123" is the line the delivery plan writes at the top of every task's description
# (ticvai/tools/push-openproject.py). It is the order the work is meant to be finished in, and the only order
# a board can be sorted by that does not change when somebody comments on a ticket.
BUILD_ORDER = re.compile(r"Build order:?\s*#(\d+)")  # "Build order: #12" (push) and "Build order #12" (rewrites)


def build_order(work_package: dict) -> Optional[int]:
    """The ticket's place in the build order, read from its description; None when it has none."""
    text = work_package.get("description")
    if isinstance(text, dict):
        text = text.get("raw")
    found = BUILD_ORDER.search(text or "")
    return int(found.group(1)) if found else None


def _build_order(work_package: dict, endpoint: str, token: Optional[str]) -> Optional[int]:
    """The number field (Priority_No.) when the project has one, else the description's line. Since release r1
    (1 October) a ticket's description is a pointer to ADAM with no "Build order #n" line, so the field is the
    only place the order is; the line stays the fallback for a project without the field."""
    if token:
        field = build_order_field(endpoint, token, work_package)
        value = work_package.get(field) if field else None
        if isinstance(value, (int, float)):
            return int(value)
    return build_order(work_package)


def summarise(work_package: dict, endpoint: str, token: Optional[str] = None) -> dict:
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
        # Where this ticket sits in the order the work is finished in. Read here, where the description
        # is at hand, so the description itself need not be carried on every list row.
        "buildOrder": _build_order(work_package, endpoint, token),
        # Whether this ticket's dates are its own. OpenProject schedules a
        # parent automatically by default: its dates are derived from its
        # children and a PATCH that sets them is refused with a 422. The plan
        # page has to know which bars are draggable before somebody drags one,
        # so this comes back on every summary rather than being discovered at
        # the moment of writing.
        "scheduleManually": bool(work_package.get("scheduleManually", False)),
        "percentDone": work_package.get("percentageDone"),
        # What a ticket cost and what it was expected to. Both are durations in
        # OpenProject and hours here; `spentTime` needs permission to view time
        # entries, so a None means "this token cannot see it" as often as it
        # means "nobody logged any", and the costing page says so rather than
        # showing a zero somebody would take for a fact.
        "spentHours": hours(work_package.get("spentTime")),
        "estimatedHours": hours(work_package.get("estimatedTime")),
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
    found = summarise(raw, endpoint, token)
    text = ((raw.get("description") or {}).get("raw") or "").strip()
    found["description"] = text[:DESCRIPTION_LIMIT]
    if len(text) > DESCRIPTION_LIMIT:
        found["descriptionTrimmed"] = True
    return found


# Enough of a thread to work from. A ticket with more has the rest at `url`.
COMMENT_LIMIT = 50


def comments(endpoint: str, token: str, key: str) -> list:
    """
    The work package's comments, oldest first, as `{author, at, text}`.

    Only `Activity::Comment` entries: the field changes around them ("status
    changed from New to In progress") are noise to somebody reading a thread.
    OpenProject 10 gives the author as an href with no title, so names are
    looked up once per person; a name that cannot be read (the token may not
    see that user) stays as the user number rather than failing the ticket.
    """
    page = call(endpoint, token, f"work_packages/{key}/activities")
    found, names = [], {}
    for act in page.get("_embedded", {}).get("elements", []):
        text = ((act.get("comment") or {}).get("raw") or "").strip()
        if act.get("_type") != "Activity::Comment" or not text:
            continue
        user = (act.get("_links") or {}).get("user") or {}
        who = user.get("title") or ""
        uid = _id_from_href(user.get("href"))
        if not who and uid is not None:
            if uid not in names:
                try:
                    names[uid] = call(endpoint, token, f"users/{uid}").get("name") or ""
                except (Refused, Blocked):
                    names[uid] = ""
            who = names[uid] or f"user {uid}"
        found.append({"author": who, "at": act.get("createdAt"), "text": text})
    return found[-COMMENT_LIMIT:]


def statuses(endpoint: str, token: str) -> list:
    """Every status on the instance, as `{id, name, isClosed}`, in OpenProject's order.
    Whether a given change is *allowed* is OpenProject's call, made when it is sent."""
    page = call(endpoint, token, "statuses")
    return [
        {"id": st.get("id"), "name": st.get("name", ""), "isClosed": bool(st.get("isClosed"))}
        for st in page.get("_embedded", {}).get("elements", [])
    ]


def update(endpoint: str, token: str, key: str, lock_version: int,
           status_id: Optional[int] = None, percent_done: Optional[int] = None,
           start_date: Optional[str] = None, due_date: Optional[str] = None) -> dict:
    """
    Change the status, % done and/or the dates, as the owner of `token`.

    `lockVersion` is the version that was read when the change was proposed. If
    anybody has touched the work package since, OpenProject answers 409 and
    nothing changes — the person agreed to a change against what they saw.

    **Dates carry `scheduleManually` with them, and they have to.** OpenProject
    schedules a parent automatically unless told otherwise: its start and finish
    are derived from its children, and a PATCH that sets them on an
    automatically scheduled ticket is refused with a 422 naming a field the
    person never touched. Sending the flag in the same PATCH is what converts
    "these dates are computed" into "these dates are stated", which is exactly
    what moving a bar on a chart means. It is sent only when a date is being
    written, so a status-only change leaves the scheduling mode alone.
    """
    body: dict = {"lockVersion": lock_version}
    if percent_done is not None:
        body["percentageDone"] = percent_done
    if start_date is not None:
        body["startDate"] = start_date or None
    if due_date is not None:
        body["dueDate"] = due_date or None
    if start_date is not None or due_date is not None:
        body["scheduleManually"] = True
    if status_id is not None:
        body["_links"] = {"status": {"href": f"/api/v3/statuses/{status_id}"}}
    raw = call(endpoint, token, f"work_packages/{key}", method="PATCH", body=body)
    return summarise(raw, endpoint, token)


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
    return summarise(raw, endpoint, token)


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


EVERYTHING_PAGE = 200
EVERYTHING_WORKERS = 3


def everything(endpoint: str, token: str, project_id: int, limit: int = 20000) -> list:
    """
    Every work package in one OpenProject project, in every state.

    The opposite end from `mine`: that answers "what am I holding", this answers
    "where is the delivery". So the status filter is `*` — the closed and the
    rejected are the whole point of an overview, and leaving them out would make
    every count a count of unfinished work wearing the name of the total.

    **Paged by id, and the pages read side by side.** OpenProject 10 takes about
    six seconds for a page of 200, and a release project holds thousands (TICVAI:
    7,967), so one page after another is minutes — past the proxy's two. The
    first page says the total; the rest are asked for three at a time, which is
    a load the instance carries and a minute instead of four. Sorted by id rather
    than by last change, because pages read at different moments must not shift
    under each other when somebody edits a ticket mid-read.

    Page 200, not bigger: a page of 1,000 takes longer than `TIMEOUT`. The
    `limit` is a ceiling on rows; past it the newest-created are kept.
    """
    filters = json.dumps([
        {"project": {"operator": "=", "values": [str(project_id)]}},
        {"status": {"operator": "*", "values": []}},
    ])

    def page_at(offset: int) -> tuple:
        page = call(endpoint, token, "work_packages", {
            "filters": filters,
            "pageSize": EVERYTHING_PAGE,
            "offset": offset,
            "sortBy": json.dumps([["id", "desc"]]),
        })
        return page.get("_embedded", {}).get("elements", []), page.get("total")

    first, total = page_at(1)
    pages = [first]
    if isinstance(total, int) and len(first) >= EVERYTHING_PAGE:
        wanted = min(total, limit)
        last = -(-wanted // EVERYTHING_PAGE)  # ceiling
        # An instance that ignores paging would hand back page 1 forty times;
        # the dedupe below makes that harmless, and the page count is bounded
        # by the total it reported rather than by what keeps arriving.
        with ThreadPoolExecutor(max_workers=EVERYTHING_WORKERS) as pool:
            pages.extend(pool.map(lambda n: page_at(n)[0], range(2, last + 1)))

    found: dict = {}
    for elements in pages:
        for raw in elements:
            summary = summarise(raw, endpoint, token)
            found[summary["key"]] = summary
    return list(found.values())[:limit]


def mine_finished(endpoint: str, token: str, project_id: Optional[int] = None,
                  limit: int = 50) -> list:
    """What this person has closed lately, newest first.

    **Filtered by status and sorted by date, never filtered by date.** A date
    operator would be the obvious way to ask for "the last week", and the
    operators for it changed shape across OpenProject versions — this instance
    is 10.0.2, from 2019. Asking for the newest closed ones and choosing the
    window in Python is one more round of sorting and cannot be wrong.

    A board that shows only what is left reads as a list of things you have not
    done. What somebody finished this week is the other half of the same board.
    """
    wanted = [
        {"assignee": {"operator": "=", "values": ["me"]}},
        {"status": {"operator": "c", "values": [""]}},
    ]
    if project_id is not None:
        wanted.append({"project": {"operator": "=", "values": [str(project_id)]}})
    page = call(endpoint, token, "work_packages", {
        "filters": json.dumps(wanted),
        "pageSize": max(1, min(limit, 200)),
        "sortBy": json.dumps([["updatedAt", "desc"]]),
    })
    return [summarise(wp, endpoint, token)
            for wp in page.get("_embedded", {}).get("elements", [])]


# The custom field that holds the build order as a number ("Priority_No." on the TICVAI project), found by name
# in the project's work package schema, once per project. The delivery plan renumbers it on every ticket when the
# plan changes; a started ticket's description is kept, so its "Build order #n" line can be stale while the field
# is not. None when the project has no such field, and the description is read instead.
BUILD_ORDER_FIELD_NAMES = {"priority_no.", "priority_no", "priority no", "build order"}
_order_field: dict = {}


def build_order_field(endpoint: str, token: str, sample: dict) -> Optional[str]:
    links = sample.get("_links", {})
    project = _id_from_href((links.get("project") or {}).get("href"))
    kind = _id_from_href((links.get("type") or {}).get("href"))
    if project is None or kind is None:
        return None
    if (endpoint, project) not in _order_field:
        found = None
        try:
            schema = call(endpoint, token, f"work_packages/schemas/{project}-{kind}")
            for field, spec in schema.items():
                if (field.startswith("customField") and isinstance(spec, dict)
                        and str(spec.get("name", "")).strip().lower() in BUILD_ORDER_FIELD_NAMES):
                    found = field
                    break
        except Exception:  # noqa: BLE001 -- no schema, no field: the description is the fallback
            found = None
        _order_field[(endpoint, project)] = found
    return _order_field[(endpoint, project)]


def mine(endpoint: str, token: str, limit: int = 2000,
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
    # **Every page, in id order.** This used to be one page of 100 sorted newest-updated first, so
    # anybody holding more than 100 tickets saw a different 100 each time a comment or a push touched
    # one, and the board changed between two asks with nothing done. Id order keeps the pages stable
    # while they are walked; the order a person reads is set by the caller (main.my_board).
    found, offset, size = {}, 1, 200
    for _ in range(50):
        page = call(endpoint, token, "work_packages", {
            "filters": filters,
            "pageSize": size,
            "offset": offset,
            "sortBy": json.dumps([["id", "asc"]]),
        })
        elements = page.get("_embedded", {}).get("elements", [])
        before = len(found)
        field = build_order_field(endpoint, token, elements[0]) if elements else None
        for raw in elements:
            summary = summarise(raw, endpoint, token)
            if field and isinstance(raw.get(field), (int, float)):
                summary["buildOrder"] = int(raw[field])
            found[summary["key"]] = summary
        total = page.get("total")
        if (len(elements) < size or len(found) == before or len(found) >= limit
                or (isinstance(total, int) and len(found) >= total)):
            break
        offset += 1
    return list(found.values())[:limit]
