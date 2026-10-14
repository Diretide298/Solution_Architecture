"""What a settled change request tells the ticket it was raised from (CHG-ADM-002).

**The lead's rule, 14 October 2026** (Chinmay): "whenever we have a cr we should create new tickets if ticket is
closed. if not then add comment for the AI agent when he pulls". So a request settled as accepted, done or
rejected reaches its ticket one of two ways:

- **The ticket is still open** (OpenProject's status is not a closing one): one comment on it, written for the AI
  agent that pulls it next. `adam_pull` puts the comment thread and a "Change requests on this ticket" section
  into README.md, so the agent reads it before it builds.
- **The ticket is closed**: nobody will pull it again, so the change becomes a CHILD TASK of the closed one
  ("we create child tasks for CR remember that", Chinmay, 14 October), carrying the request, the decision and
  the release (`/api/changes/{n}/ticket/...`, `_ticket_text`). At most one per request:
  `change_request.child_key` is the guard. It is filed before the request is marked Done (ADAM refuses a
  ticket for a Done request). Once a request has its child task, later settlements comment on that one.
- Migration work a request causes is a child task of the affected MIG-* ticket, assigned to the migration
  owner (ticvai/docs/active/team.json `migrations.owner`). Not filed from here: the lead files it.

A rejection on a closed ticket gets a comment, not a ticket: there is nothing to build.

Never the ticket's own text: a started ticket's OpenProject description is never rewritten (ticvai/CLAUDE.md).

Pure functions, no I/O, so the two places that settle requests say the same words and decide the same way:
`main.py` (the resolve route and the CSV bulk settle) and `settle_changes.py` (a workstation script, which
imports this file from beside it).
"""
from __future__ import annotations

SETTLED = ("accepted", "done", "rejected")


def heading(cr: str, status: str) -> str:
    """The comment's first line. Its prefix up to the status is what makes a second run a no-op."""
    return f"**ADAM {cr} · {status} — read before building**"


def already_told(comments, cr: str, status: str) -> bool:
    """Whether the thread already has this request's comment for this status.

    Matched on `**ADAM CR-nnn · <status>`, without the rest of the heading, so the shorter heading
    settle_changes.py wrote before 14 October ("**ADAM CR-011 · accepted**") also counts and the
    ticket is never told the same thing twice.
    """
    prefix = f"**ADAM {cr} · {status}"
    for c in comments or []:
        text = c.get("text", "") if isinstance(c, dict) else str(c or "")
        if text.strip().startswith(prefix):
            return True
    return False


def plan(status: str, ticket: str, child: str, closed) -> dict:
    """What a settlement does to OpenProject: `{"action": "ticket" | "comment" | "none", "key", "why"}`.

    `ticket` is the work package the request was raised from, `child` the one already filed from it
    (blank when none), `closed` whether the work package being told (the child when there is one,
    otherwise the ticket) is closed in OpenProject: True, False, or None when unknown.
    """
    status = (status or "").strip().lower()
    target = (child or ticket or "").strip().lstrip("#")
    if status not in SETTLED:
        return {"action": "none", "key": target, "why": "not settled (open): a ticket is told when it is settled"}
    if not target:
        return {"action": "none", "key": "", "why": "raised from no ticket, so there is none to tell"}
    if closed is None:
        return {"action": "none", "key": target, "why": f"could not read whether #{target} is closed"}
    if closed and not child and status in ("accepted", "done"):
        return {"action": "ticket", "key": target,
                "why": f"#{target} is closed: the change is new work, so it gets a new ticket under it"}
    if closed and child:
        why = f"#{target} (the ticket already filed for this request) is closed; one request, one ticket"
    elif closed:
        why = f"#{target} is closed and the request was rejected: nothing to build, so a comment only"
    else:
        why = f"#{target} is open: the agent that pulls it reads the comment"
    return {"action": "comment", "key": target, "why": why}


def _release_line(status: str, ref: str, served: str) -> str:
    if status == "rejected":
        return "Nothing in the package changes."
    if ref:
        return (f"The package change is in release `{ref}`. ADAM always serves the latest release"
                f"{f' (now `{served}`)' if served else ''}, so your next pull already has it: README.md lists "
                "this request under \"Change requests on this ticket\", and spec-diff.md shows what moved "
                "since your previous pull.")
    return ("The package change lands in the next release. Until it does, the decision above is what to "
            "build to; your next pull after that release shows the change in spec-diff.md.")


def comment_text(cr: str, title: str, status: str, resolution: str, ref: str, ticket: str,
                 served: str = "", artefacts=None) -> str:
    """The comment on an open ticket, written for the AI agent that pulls it next."""
    status = (status or "").strip().lower()
    lines = [heading(cr, status), "",
             f"For the AI agent that pulls #{ticket} (and the developer): ADAM change request {cr}, "
             f"\"{(title or '').strip()}\", raised from this ticket, was **{status}**.", "",
             f"**What was decided:** {(resolution or '').strip() or '(no note was given)'}", "",
             f"**What changed, and where:** {_release_line(status, ref, served)}"]
    if artefacts:
        lines += ["", "**Artefacts it touches:** " + ", ".join(f"`{a}`" for a in artefacts)]
    if status == "rejected":
        todo = ("Build as this ticket and its linked files say. Do not work around it in code; if it still "
                "blocks you, raise a new change request with what is new.")
    elif status == "accepted":
        todo = ("Build to the decision above. Where this ticket's description says otherwise, the decision "
                "wins (a started ticket's description is never rewritten). If the package change has not "
                "reached a release yet, build the rest and leave the changed part to the release that "
                "carries it.")
    else:
        todo = ("Build to the decision above. Where this ticket's description says otherwise, the decision "
                "wins (a started ticket's description is never rewritten).")
    lines += ["", f"**What to do now:** pull the ticket again (`/ticket {ticket}`), then: {todo}"]
    return "\n".join(lines)


def ticket_section(cr: str, status: str, resolution: str, ref: str, closed_key: str) -> str:
    """The part of a new ticket's description that says why it exists and what was decided."""
    parts = [f"**Decision ({cr} · {status})**", "", (resolution or "").strip() or "(no note was given)"]
    if ref:
        parts += ["", f"Carried by release `{ref}`. Build against the latest release ADAM serves."]
    if closed_key:
        parts += ["", f"Opened because #{closed_key}, which this request was raised from, is closed: the "
                      "change is new work and is built here, not by reopening it."]
    return "\n".join(parts)
