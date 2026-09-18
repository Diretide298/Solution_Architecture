# ADR-0045: Every order carries a proven contact, and the gate is the checkout page

**Status:** Accepted — decided with Chinmay, 18 September 2026
**Date:** 18 September 2026
**Settles:** [CF-172](../registers/conflicts.md) — closed 17 September on the rule, reopened here on *where* the rule fires and *what happens to the profile afterwards*
**Depends on:** [ADR-0004](0004-single-session-per-user.md) — a guest session is one session; nothing here changes that

---

## Context

**The identity contract said both that an unverified guest buys and that it cannot.** CF-172 recorded
it: `verifyGuestEmail` read *"Unverified accounts still buy. Blocking purchase on verification loses
the sale"* while `registerGuest` and `GuestSession.isVerified` read *"an unverified account may
browse but not transact"*. That was settled on 17 September — no order against an unproven contact —
and written into `identity`, `orders` and `white-label`.

**Two things were got wrong, and both are visible in the requirement matrix.**

**First, the gate was put in the wrong place.** The 17 September edit sent a guest from the cart to
sign-in: `WEB-010 → WEB-016`, `GST-041 → GST-042`. The matrix puts it one step later. **2.6.1 §2.4**:
*"On the **check out page**, users can log in or manually fill in the following details: name, email,
mobile number, nationality, also choose to apply coupons"* — and §2.3 offers *"Click Add to Cart or
proceed directly to check out"*. The fork is a property of the checkout page, not a wall in front of
the cart. `WEB-011 Guest Details & Attendee Forms` **is** that page; the package already had it.

**Gating at the cart also costs something specific.** **2.6.45** requires abandoned-cart reminders
with a link to resume. A wall before the cart means the only carts that can be abandoned are ones
belonging to people already identified — which removes most of the population the requirement is
about.

**Second, nothing said what happens to the profile.** The 17 September rule covered whether an order
may be taken. It did not say that a one-time guest gets a durable profile, and it did not say what
happens when that guest returns with the same address. The matrix is explicit on both:

| | |
|---|---|
| **2.6.28** | *"Guest Checkout or Registration on the website or Login to SSO. **This should be configurable per site**"* |
| **2.6.67** | Guest Checkout · Apple ID · Google ID · UAE Pass · SSO · Registered Account |
| **2.6.29** | *"If the customers require to have access to this account, this account shall have a login and password in order to recall previous transactions"* |
| **22.2.8** | *"System shall automatically detect and merge duplicate guest records using configurable matching rules such as email, phone number, membership number…"* |
| **7.3.7** | *"Allow **authorized users** to merge profiles into a master record… maintain complete audit logs and support rollback review before final merge"* |

**2.6.29 is the load-bearing one.** It separates *having a profile* from *having access to it*. A
guest-checkout buyer has a record — the tickets have to go somewhere and the order has to belong to
something — and turning that record into an account is a later, deliberate act with a credential.

**22.2.8 and 7.3.7 disagree**, and the disagreement is real rather than a wording slip: one says the
system merges automatically, the other says a person merges with an audit log and a rollback review.

---

## Decision

### 1. Two routes to an order, and one gate

**A site offers sign-in checkout, one-time guest checkout, or both.** Which is venue configuration,
set from the configuration menu and carried by the existing `guestCheckout` feature toggle
(matrix 2.6.28). **It stays off by default** — a site that has thought about nothing gets the
stricter behaviour.

**The gate is the checkout page.** The cart is open to anyone. At checkout the guest either signs in
or supplies their details, and `checkoutCart` refuses until one of them has completed. On the web
that page is `WEB-011`; on the app it is `GST-041 Checkout Entry`, which was already built as a
fork.

```
Browse → Add to cart → Cart → CHECKOUT ┬── Sign in ────────────┐
                                       └── Guest details + code ┴→ Payment → Confirmed
```

### 2. Guest checkout proves the contact before the order is taken

**A one-time guest gives the email or mobile the tickets go to and confirms a one-time code**
(`requestGuestOtp`, purpose `verify`) before `checkoutCart` will complete. This is the *dual OTP
validation* of the reference checkout the client walked through, and it is what makes everything in
§4 safe.

**No order against an unproven contact stands unchanged** — only its position moves. Tickets go to
an address, and an unproven address is how somebody receives a stranger's tickets.

### 3. Both routes produce a profile

**A one-time guest checkout creates a durable guest profile**, the same shape a registered guest
has. It holds the contact, the order, the tickets and the consents captured at checkout.

**It carries no credential.** Per matrix 2.6.29, recalling previous transactions requires setting up
access — which is what `linkGuestCheckout` already does from the other direction, attaching prior
orders once an identifier is verified under a new account.

### 4. A returning contact attaches the order, never the access

**When a guest checkout verifies a contact the platform already holds, the new order, its tickets
and its history attach to the existing profile automatically** (matrix 22.2.8). No duplicate record
is created.

**The guest does not thereby get a session on that profile.** They see the order they just placed.
They do not see the profile's earlier orders, wallet, membership or loyalty balance until they
authenticate as its owner. **This is the whole of the security argument**: verification proves the
person controls that mailbox *today*, which is enough to route a ticket to it and not enough to open
someone's history.

**Automatic attachment is available only on a verified contact.** Any other candidate match —
passport, national id, a phone that was never proved, a fuzzy name — is a *suggested* merge and goes
to the staff review of matrix 7.3.7, with its audit log and rollback. **That is how 22.2.8 and 7.3.7
are both true**: automatic where the evidence is a code the guest just entered, reviewed where it is
an inference.

**A merge takes the narrower of two consents**, per CF-160. Attaching an order must never widen what
the platform may do with the profile it attaches to.

### 5. The kiosk is exempt

A walk-up pays at the kiosk and takes printed tickets, so there is no address to prove
(matrix 2.1.10). Unchanged from 17 September.

---

## Consequences

**Three transitions move.** `WEB-010 → WEB-016` is removed; the fork becomes `WEB-011`, which either
carries a verified session forward or runs the code step before `WEB-012`. `GST-041 → GST-042` stays,
because `GST-041 Checkout Entry` is already the checkout page rather than the cart.

**`checkoutCart`'s 403 keeps its meaning and changes its trigger.** *The contact the tickets would go
to is not proven* is still the refusal; it now fires at checkout with the cart intact, which is what
the response already promised by keeping the cart.

**One operation is missing and has to be added.** `linkGuestCheckout` attaches *past orders to a new
account*. Nothing attaches *a new order to an existing profile* — §4's direction. It needs an
identity-resolution step inside checkout, on the verified contact only.

**Abandoned-cart reminders get harder, correctly.** A cart built before identity has no address to
remind. 2.6.45 is satisfiable only for guests who reached checkout and stopped, or who were already
signed in — which is the honest scope, and should be said in the notification design rather than
discovered.

**The design handoff does not implement this.** `Guest Booking v2` runs *Fixture · Seats · Extras ·
Your details · Payment · Confirmed* with sign-in as top-bar chrome and no code step; its mobile file
has no sign-in surface at all. `Your details` is the page this ADR loads — the step exists and the
gate does not.

---

## What was considered and rejected

**Gating before the cart.** What was shipped on 17 September. Stricter, and it keeps an address
available for every abandoned cart — but it gates before anyone has committed to anything, and the
matrix describes the fork at checkout in 2.6.1 §2.4.

**Guest details with no code.** Matrix 2.6.1 §2.4 lists the fields and mentions no verification, so
this is the literal reading. Rejected: it reinstates exactly the contradiction CF-172 closed, and it
makes §4 an account-takeover route — type a stranger's address, have your order join their profile.

**Full access on a verified email.** Proving the mailbox would open the whole profile. Rejected
because mailbox control today is not proof of ownership of everything that address ever bought, and
2.6.29 asks for a credential before previous transactions are recalled.

**Staff review for every join.** Matrix 7.3.7 applied to all matches. Rejected as the default: a
guest's order would sit detached until someone actioned it. It remains the path for every match that
is not a verified contact.
