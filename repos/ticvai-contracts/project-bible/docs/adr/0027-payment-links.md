# ADR-0027: A payment link is a credential, and payment converts the reservation

**Status:** Accepted
**Date:** 20 August 2026
**Closes:** BL-072
**Related:** [ADR-0004](0004-single-session-per-user.md) sessions · [ADR-0022](0022-conflict-policy.md) conflict policy · CF-131 payment providers

---

## Context

A booking taken at a till cannot be paid at the till. A guest rings up, an operator holds seats,
and the money has to arrive later — from a person who is not standing there, may have no account,
and quite possibly does not want one.

`createPaymentLink` was contracted on 18 August. **It had no schema behind it and no guest-facing
path**, and `WEB-014 Payment Link Landing` declared `getCart` and `checkoutCart` while
`createPaymentLink` takes an `orderId`. **The screen was looking for a cart that was never
created**, and its entry state resolved `cartId` from the session — which a guest arriving from an
email does not have.

Three things had to be decided, and none of them was.

---

## Decision

### The link is the credential, not a session

**A guest holding a link is anonymous.** Not signed in, and not necessarily registered — **a phone
booking is exactly the case where they have not registered**, and requiring an account before
taking money is how a paid booking becomes an abandoned one.

The token grants **read of one order and payment against it**. Nothing else. It is not a session,
it does not authenticate a person, and it does not survive the payment.

**Scoped to one order deliberately.** A token that can read a second order is a token that read
somebody else's booking.

**This does not weaken ADR-0004.** A session is a token with a validity window carrying a principal
and a role; a payment link carries neither and can do exactly two things.

### Payment converts the reservation

**On success, the reservation becomes an order.** Server-side, immediately, with no staff member
involved — because there is none. The guest is paying at 11pm from an email.

**A paid reservation that is still a reservation is inventory the venue thinks it can sell.** That
is the failure this prevents, and it is worse than the alternative it costs: an order appearing in
the POS overnight with nobody at the till.

**Recorded because it was assumed.** `convertReservation` is staff-only and nothing said what fires
it in this path. An assumption that reaches production is a defect nobody can attribute.

### Expiry releases the hold

**Not just the link.** An unpaid link holding inventory is inventory nobody can sell, and a link
that outlives its hold sells a seat twice.

`releaseHoldOnExpiry` defaults true and is a field rather than a constant, because a high-value
booking a venue is chasing by phone is a case where somebody may reasonably choose otherwise.

### A resend supersedes

**Two live links against one order is two guests paying for one booking**, and the second payment
is a refund somebody has to make.

The old token answers `410 superseded` — **never 404**. A guest holding the first email needs to
know why it stopped working, not whether it was ever real.

---

## Consequences

**Four states a guest can land in, and three of them are not errors.** Expired, already paid, and
superseded each need their own message: *the hold is released, book again* is a different
conversation from *here are your tickets* and from *we sent you a newer link*.

**404 is never returned for a real token.** Telling somebody their booking does not exist when it
expired is how a support call starts.

**An anonymous caller now exists in the audience vocabulary for a money operation.** `payByLink`
is `[guest, anonymous]`, which is the first write path open to an unauthenticated caller. The
mitigation is scope: one order, one action, one token, and the card never reaches the platform
(CF-131).

**A partly-lost hold is answered rather than failed.** A link near expiry and a guest reading
slowly is rare and real; the `409` names what is no longer available rather than failing the whole
basket, because **part of a booking is usually still worth having.**

---

## Alternatives considered

**Require an account before paying.** Cleaner authentication, one fewer principal kind, and
**it loses the sale.** The guest booked by phone precisely because they were not going to sit at a
website, and a registration wall between them and a payment is a wall in the wrong place.

**Send a one-time code rather than a link.** Stronger, and it asks a guest to type a code from an
SMS into a website they were not on. **The link is the journey; the code is a second journey
bolted to it.**

**Hold the money and convert manually.** Safer for the venue and it means somebody has to be
watching. **A paid booking sitting unconverted overnight is the case that generates the phone call
this feature exists to avoid.**

---

## Provenance

**Found on 20 August by walking the journey rather than the contract.** Every part existed —
`createPaymentLink`, `createReservation`, `convertReservation`, `createPayment`, a landing screen —
and no two of them joined. **The contract audit passed it; the journey did not.**
