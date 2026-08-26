# Client boards — where each screen rests

**217 screens across four domains, and the first question is not how to build them. It is where
they go.**

The failed attempt put 60 F&B screens on a new platform without checking, created four duplicates
of screens P08 already had, and put 18 F&B operations on more than one platform. **A domain board
is not a platform boundary**, and treating it as one is what produced that.

This is the rule for deciding, and what it produces.

---

## The boards name their own axis

The client documents label their own boards, and the labels are the answer:

| Board | Retail calls it | What it is |
|---|---|---|
| 1 | *Master & control* | **Configuration** |
| 2 | *Flow* | **Configuration** |
| 3 | *Transaction flow* | **Operations** |
| 4 | *Operational flow* | **Operations** |
| 5 | *Commercial flow* | **Operations** |
| 6 | *Intelligence flow* | **Analytics** |

**Boards 1 and 2 are set up once and edited rarely. Boards 3 to 5 are used every day, at speed, by
somebody who is not sitting down. Board 6 is read on a Monday morning.**

Those are three different products, and the boards have already separated them.

---

## The placement rule

**Three questions in order. The first that gives an answer wins.**

### 1. Who operates it, and are they sitting down?

**A person standing up with a queue behind them needs a different screen from a person at a desk.**
Not a responsive layout — a different screen, with fewer choices and larger targets.

- Configuring a menu → **desk**
- Bumping a ticket on a kitchen pass → **standing, gloves, two metres**
- Counting a till at close → **standing, at the till**
- Reading last week's margin → **desk**

### 2. Does it survive the network going down?

**A screen the venue cannot lose is a screen that belongs on the device doing the work.** A kitchen
display that blanks mid-service is worse than one that says it is behind; a menu builder that
blanks is a manager waiting a minute.

**This is the test that separates operations from configuration** more reliably than any keyword.

### 3. Does another platform already do it?

**Asked last and it is the one that was skipped.** P08 already had `Menu Management` and `Kitchen
Display` before the F&B board arrived — the board did not create the need, it drew a better version
of a screen that existed.

**Where an existing screen answers a board screen, the board improves it. It does not duplicate
it.**

---

## What the rule produces

### Existing platforms absorb most of it

**P08 Venue Management — configuration and analytics.** Boards 1, 2 and 6 across all four domains.
That is roughly 120 board screens against 108 existing, and **most are improvements to a screen
that already exists rather than new ones.** P08 now has a home screen and eight sections, which is
what makes that survivable.

**P04 Venue POS — the till.** Board 2 of the POS set: cash, float, safe drop, denominations,
variance. **Eleven screens, and P04 has ten**, which is the right proportion for a device somebody
uses for one job.

**P06 Venue Staff App — the floor.** Table service, waitlist, live table management, stock counts
on a handheld. **Already 46 screens and already the right home** — these are staff walking around
with a phone.

### One new platform, and only one

**A kitchen display is not a back office at a different width.**

- It is bumped by somebody with flour on their hands
- It is read from two metres by a person who is not looking at it directly
- **It must keep working when the network does not**, because the kitchen still has to send food out
- Nobody logs into it; it is on when the kitchen is open

**That is a different runtime, a different offline story and a different input model.** Four to six
screens: the KDS itself, expeditor and assembly, station workload, and the collection screen.

**Everything else the F&B board describes is configuration a manager does at a desk**, and that is
P08.

---

## What this rejects, and why

**A platform per domain.** F&B, Retail and Inventory each getting their own would give four
back-office platforms with four navigation models, four home screens, and a manager who has to know
which one holds the supplier list. **The domain is a section, not a platform.**

**Adopting all 217.** The client named 217 and specified about half — the F&B document lists 60
screens and writes up 30. **A screen built from a heading in a contents page is a screen nobody has
designed.** Build what is specified; record the rest as named.

**Building before the scope question is answered.** These documents contain functionality the
matrix does not. **Which is the specification** is a question for Qossai, and every screen built
against the boards before it is answered is a screen whose requirement cannot be cited at sign-off.

---

## The order

**1 — Ask Qossai which document governs.** One line. Everything depends on it.

**2 — Map every board screen to an existing screen or to nothing.** Not build — map. The output is
a table saying *this board screen is BO-045 improved*, or *this board screen is new*. **That table
is the thing the failed attempt did not have.**

**3 — Build the kitchen display platform.** Small, clearly separate, and it unblocks the four F&B
screens that genuinely cannot live in a back office.

**4 — Improve P08's existing screens against the boards**, section by section. The boards are
better specified than what is there; that is a rewrite of 108 screens' detail, not 120 new ones.

**5 — Then decide about the remainder**, with a table in hand rather than a page count.

---

## Revisited 20 August: placement is a board decision, not a screen decision

**The first pass left 75 screens unresolved and that was a method failure, not an ambiguity.** It
matched screen names against existing screen names — which gave *Table & Seating Configuration →
Auto-Scaling Configuration* at 0.84 — and then against shared operations, which let `getDashboard`
link a kitchen board to a security console.

**The documents already say where each screen sits.** Every one belongs to a numbered board, each
board has a stated purpose, and **a board is homogeneous by construction**: ten screens doing one
job for one operator. Deciding once per board rather than once per screen resolves all 157.

| Domain | Board | Purpose | Lands on |
|---|---|---|---|
| F&B | 1, 2 | Outlet, menu and product | **P08** |
| F&B | 3 | Kitchen operations | **a kitchen platform** |
| F&B | 4 | Restaurant service | **P06 staff app** |
| F&B | 5 | Stock and production | **P08** |
| Retail | 1, 2 | Store, product and catalogue | **P08** |
| Retail | 3 | Transaction | **P04 POS** |
| Retail | 4 | Operational | **P06 staff app** |
| Retail | 5 | Commercial | **P08** |
| POS | 1 | Workstation and device | **P08** |
| POS | 2, 3 | Cash, till, shift and operator | **P04 POS** |
| POS | 4, 5 | POS experience, offline and sync | **P08** |
| all | 6 | Analytics and intelligence | **an analytics platform** |

**Zero unresolved.**

### And the test that changed the answer

Placing by board sent **105 screens into P08, taking it from 108 to 213** — with `Sell` at 62 and
`Venue Operations` at 46. **That is the failure the rule was written to prevent**, arrived at by
following the rule.

**The analytics boards are the reason, and they are the same six screens three times.** F&B,
Retail and POS each end with an executive command centre, a sales and revenue view, a performance
view, a forecasting view, an AI recommendation centre and an AI assistant. **26 screens that
collapse to ten shapes.**

**A domain is a filter on an analytics screen, not a copy of it.** One reporting surface with a
domain selector answers all 26, and building three sets means maintaining one screen three times
and watching them drift.

**P08 takes 79 rather than 105**, which is survivable against 108 existing — and most of the 79 are
improvements to a screen that already exists rather than additions.

### Two new platforms, both narrow

**Deliberately unnumbered.** `check-package` refuses a document naming a platform code no screen
file defines, and it refused this one — **a strategy that hands out platform numbers before the
platforms exist is a strategy that has already decided.** They get codes when they get screens.

**A kitchen platform — 10 screens.** Bumped with flour on the hands, read from two metres, and **it must
keep working when the network does not** because the kitchen still has to send food out.

**An analytics platform — 26 board screens collapsing to about 10.** Its own surface because it is read
rather than operated, it is the one screen a venue manager opens on a Monday and never during
service, and **a domain selector is cheaper than three copies.**
