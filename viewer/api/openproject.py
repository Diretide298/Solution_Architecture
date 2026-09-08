"""
Reading OpenProject, as whoever is asking.

**Every call here is made with the caller's own stored token, never a service
account.** That is the whole reason the settings page exists: a shared
credential would attribute every read — and later every write — to one robot,
and the audit trail is most of what a PMS is for.

Read-through and nothing else, for now. The bridge does not mint work package
ids, does not create work packages, and does not own status. OpenProject holds
the schedule — 23 epics, 444 features, 2,173 tasks in the delivery plan — and
this service holds the one thing OpenProject cannot express: which artefact a
work package is about. See `artefact_link` in db.py.

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


def call(endpoint: str, token: str, path: str,
         params: Optional[dict] = None) -> Any:
    """
    One GET against an OpenProject instance, as `token`.

    `path` is relative to `/api/v3`. The answer is parsed JSON; anything else
    raises rather than being handed on as a string that a caller will index into
    and get a character from.
    """
    url = f"{endpoint.rstrip('/')}/api/v3/{path.lstrip('/')}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    auth = base64.b64encode(f"apikey:{token}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    })

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as answer:
            return json.loads(answer.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:400]
        except Exception:  # noqa: BLE001 — a body that will not read is not the story
            pass
        if _looks_like_an_edge(body):
            raise Blocked(
                f"{endpoint} is behind a proxy that refused this service before "
                f"OpenProject saw the request. No credential was tested."
            ) from exc
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
        "startDate": work_package.get("startDate"),
        "dueDate": work_package.get("dueDate"),
        "percentDone": work_package.get("percentageDone"),
        "updatedAt": work_package.get("updatedAt"),
        # The address a person opens. Built rather than taken from `_links.self`,
        # which is the API path and not the page.
        "url": f"{endpoint.rstrip('/')}/work_packages/{key}" if key else "",
    }


def work_package(endpoint: str, token: str, key: str) -> dict:
    """One, summarised."""
    return summarise(call(endpoint, token, f"work_packages/{key}"), endpoint)


def mine(endpoint: str, token: str, limit: int = 100) -> list:
    """
    What is assigned to the owner of this token and still open.

    `assignee = me` is an OpenProject filter operator rather than an id, which
    is what makes this answer correctly without the caller knowing their own
    user id. `status: o` is the built-in "open" set — asking for every status
    would return the closed ones too, and a board of finished work is not a
    board.
    """
    filters = json.dumps([
        {"assignee": {"operator": "=", "values": ["me"]}},
        {"status": {"operator": "o", "values": [""]}},
    ])
    page = call(endpoint, token, "work_packages", {
        "filters": filters,
        "pageSize": max(1, min(limit, 200)),
        "sortBy": json.dumps([["updatedAt", "desc"]]),
    })
    elements = page.get("_embedded", {}).get("elements", [])
    return [summarise(wp, endpoint) for wp in elements]
