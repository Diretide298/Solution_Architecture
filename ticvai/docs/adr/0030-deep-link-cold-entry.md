# ADR-0030: A deep link is a pointer, not authorisation

**Status:** Accepted
**Date:** 24 August 2026
**Related:** [ADR-0002](0002-user-driven-authorisation.md) · [ADR-0018](0018-configuration-scope.md) (amended — the scope walk it defines is what a link may not shortcut, and that part stands)

---

## Context

**147 screens are reachable cold by deep link and none said what they show when the target is
gone.** A shared ticket, a forwarded confirmation, a push notification opened three weeks late, a
link in an alert email — every one of these arrives at a screen with an identifier and no history.

**`check-screens` warned on all 147 and I parked them, wrongly.** The reasoning at the time — *"one
decision, not 147"* — was right; the conclusion that it needed a week of frontend consultation was
not. **The decision takes an hour and the shape depends on audience, not on the screen.**

---

## Decision

**A link identifies a thing. It never grants access to it, and it never moves the holder's scope.**

Four shapes, chosen by the audience of the surface rather than by the screen:

### Guest — say what happened and offer one way onward

**Never a 404.** A guest holding a link did nothing wrong: somebody shared a ticket that has since
been used, or forwarded a confirmation for a cancelled event.

The screen **names the thing, says whether it is expired, cancelled or withdrawn, and offers the
list it came from.** A silent 404 on a shared link is a support call.

### Staff — resolve it or say plainly that it is gone

**No silent redirect.** A supervisor following a link from an alert needs to know whether the record
moved, closed, or never existed — **those are three different next actions**, and a redirect to a
list answers none of them.

**Scope resolves from the session, never from the link.** A link cannot move somebody to a venue
they do not hold.

### Platform admin — refuse outside the operator's tenants

A link carries a tenant. **If the operator does not hold that tenant, the screen refuses** — and if
the target is gone it says so and returns to the directory.

**An admin console that silently shows the wrong tenant is worse than one that shows nothing.**

### Partner — resolve within the partner's own scope

A forwarded link between partners **must not open another partner's record.**

### And one exception that is not about failure

**A version link is expected to point at something superseded — that is what versions are for.** The
screen opens the requested version read-only, says it is not current, and links to the one that is.
**An old version is history, not an error.**

---

## Consequences

**147 screens now declare their cold-entry behaviour** and `check-screens` is at zero on this
warning. Every future screen with a `deepLink` parameter inherits one of five answers rather than
inventing a sixth.

**The scope rule is the one with teeth.** *Resolve from the session, never from the link* is what
stops a forwarded URL becoming a lateral move between venues, tenants or partners — and it is
consistent with ADR-0002, which already makes authority a property of the person rather than the
device.

**A guest screen and a staff screen now behave differently on the same failure**, deliberately. A
guest is a member of the public holding a link somebody sent them; a member of staff is following a
link from a system that should know what it pointed at.

---

## Alternatives considered

**Fetch and redirect silently.** One rule, no per-audience branching, and it is what most systems
do. **Rejected because it destroys the information the person needed** — a supervisor cannot tell a
closed record from a moved one, and a guest cannot tell a cancelled event from a typo.

**Refuse all cold entry and require navigation.** Safe and it makes every shared link useless. **A
ticket in an email that cannot be opened from the email is not a ticket.**

**Answer per screen.** The parked position. **It would have produced 147 slightly different
answers**, which is worse than one wrong answer applied consistently — a reader can correct a
pattern and cannot correct a hundred and forty-seven decisions nobody recorded.
