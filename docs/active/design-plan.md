# Design plan

**Derived from the three references the client has delivered**, and from the 180 screen
definitions. Written to be picked up in Claude Design rather than to be admired here.

| Reference | Boards | Screens | Language |
|---|---|---|---|
| `TICVAI_White_Label_Guest_App_UI_Reference` | 6 | ~60 | **Light.** Navy `#0C2340`, white cards, grey field |
| `TICVAI_Employee_App_UI_Reference` | 5 | ~50 | **Dark.** Navy ground, cyan accent, raised centre action |
| `Park_POS_dc.html` | — | 6 | **Light.** Manrope, `#0D6EFD → #00B8FF` gradient |

---

## The finding that comes from reading them together

**Three visual languages exist and nobody has reconciled them.**

That is not a criticism of any one of them — each is coherent, and the split between a light
guest surface and a dark employee surface is a legitimate decision that many operators make
deliberately. The problem is that no document says it *is* a decision, so three teams will
implement three systems and the fourth surface will pick whichever it saw last.

**This needs settling before a designer opens a file**, because it determines whether
`design-tokens` is one package or three themes of one package. My reading:

| | |
|---|---|
| **One token set, three themes** | Light guest · dark staff · light POS |
| Shared | Type scale, spacing, radii, component anatomy, status vocabulary |
| Themed | Surface, ink, accent ramps only |

The alternative — three independent systems — costs three times the maintenance and guarantees
that a shared component like a status pill drifts.

## The client's own presentation format

Both references use the same shape, and we should match it rather than invent one: **one A4
landscape board, ten numbered screens, a title bar and a footer status strip.**

    TICVAI logo          BOARD n: TITLE (10 SCREENS)          context · actions
    ───────────────────────────────────────────────────────────────────────────
    ① screen   ② screen   ③ screen   ④ screen   ⑤ screen
    ⑥ screen   ⑦ screen   ⑧ screen   ⑨ screen   ⑩ screen
    ───────────────────────────────────────────────────────────────────────────
    reassurance          tenant · environment          help · primary action

Matching it means a review meeting runs the way the client already runs one.

## What the references already settle

**The employee bottom nav is Home · Tasks · Scan · AI · More**, with Scan as a raised centre
action. That is CF-41 in a picture: the AI tab is in the shell, and the shell cannot ship
without deciding what sits behind it.

**Status vocabulary is consistent across both references** — Published, Draft, Scheduled,
Active, Inactive, Expired, On Duty, Critical, Action Required. Adopt it rather than inventing
per-screen wording; it maps closely to the state models already written.

**The live-preview device frame recurs** on every white-label screen. It is a component, not a
one-off, and it must toggle platform, theme and direction — RTL preview is not optional
(CF-42).

---

## Board plan — 32 boards

316 screens at ten to a board. **The order is by what unblocks build, not by platform number.**

### Exists as a reference — 11 boards

| | Boards | State |
|---|---|---|
| Guest app / White Label Builder | 6 | Delivered |
| Employee app | 5 | Delivered |

**These do not need redesigning.** They need extracting into components and reconciling with the
token set, which is a different and smaller job.

### Defined, undesigned — 12 boards

| | Screens | Boards | Why this order |
|---|---|---|---|
| **Staff POS** | 10 | 1 | Six exist as mockups. Highest revenue risk, and the offline states are invisible in a static frame |
| **Guest Web** | 29 | 3 | The purchase path. F01 and F02 run through it end to end |
| **Admin Web** | 36 | 4 | Largest single set, and entirely unseen by the client |
| **Partner Web** | 21 | 2 | Partners integrate against it, so it changes least often once shipped |
| **Support console** | 8 | 1 | Small, and it is where a bad day gets handled |
| **Accreditation** | 8 | 1 | Workshop-blocked. Design last, or design twice |

### Undefined — 9 boards, and they need screens before they need pixels

| | Screens | Boards | Blocker |
|---|---|---|---|
| Staff Web — venue back office | 67 | 7 | **Only 6 of 73 defined.** CF-53 |
| White-Label CMS | 20 | 2 | Not defined |
| **Guest Kiosk** | ? | ? | **Not even inventoried.** White-label, guest-facing |
| **Staff Scanner** | ? | ? | **Not inventoried, and Wave 1** |

**The scanner is the one to worry about.** It is a Wave 1 surface with no inventory, no screen
definitions and no design, and it is the surface where offline behaviour matters most.

---

## What to do in Claude Design

The wireframes in `wireframes/` are structure — regions, real field names from the contracts,
and every declared state. They are the input, not the output.

**Board 1 first, and only board 1.** Staff POS, ten screens, against the delivered mockup. It
is the smallest complete surface, it has an existing reference to converge on, and it forces
the token reconciliation immediately because the POS language differs from both references.

Once one board is right, the rest is repetition rather than decision.

**Take into it, per screen:**

| From | What |
|---|---|
| `wireframes/screens/<id>.html` | Regions, components, real field names |
| The screen YAML | Every declared state, including offline |
| `tooltips.json` | Why the screen exists, in one line |
| The reference boards | Type, colour, component anatomy, status pills |

**Design the states, not just the screen.** A POS payment screen has seven terminal states and
the one that matters is `unknown` — a card charged with no response returned. A design showing
only `approved` is a design that has not met the problem.

---

## Order of work

| | | Why |
|---|---|---|
| 1 | **Settle one-system-three-themes** | Determines whether `design-tokens` is one package. Blocks everything |
| 2 | Extract components from the two references | They are already designed; nobody has named them |
| 3 | **Board 1 — Staff POS** in Claude Design | Smallest complete surface with a reference to converge on |
| 4 | Guest Web, 3 boards | The purchase path |
| 5 | Admin Web, 4 boards | Largest, entirely unseen |
| — | **Define Staff Web, Kiosk and Scanner screens** | In parallel. **Design cannot start on a screen nobody has specified**, and that is 136 of 316 |

## One thing to resist

The references are good enough to make a full set of boards look achievable quickly. **The
constraint is not design capacity, it is that 136 screens have no definition** — no purpose, no
operations, no states. Designing those from a name produces a picture that the contract will
contradict, and the contradiction surfaces in build.

Definition first, design second, on the surfaces where neither exists.


---

# Forms — 43 screens, and a third of them should not be separate

Every screen that is a `form` or `wizard` template, or carries two or more input components.

## The state of them

| | |
|---|---|
| Forms with a real field list | **9** |
| **Forms declaring a single placeholder field** | **26** |
| Wizards with no fields declared yet | 4 |

**Twenty-six forms exist as a template and a stub.** `ADM-008 Subscription & Plan Management`
is a `form` with one `textField`. So are fifteen other Admin screens. They are named, they are
counted, and nobody has said what is on them.

**That is the finding, and it precedes any design work.** A designer handed sixteen screens
called "management" with one field each will invent sixteen layouts, and the contracts will
contradict all of them.

## The nine that are actually specified

| | Screen | Fields |
|---|---|---|
| BO-002 | Queue Configuration | Name · attraction · capacity per call · guest join toggle · redemption window |
| BO-003 | Queue Integration Setup | Source · endpoint · credential ref · interval · enabled |
| WEB-011 | Guest Details | Full name · email · mobile · consent |
| POS-001 | Begin Shift | Denomination count · notes |
| POS-005 | Payment | Method · amount received |
| WEB-002 | Event Listing | Search · category · date |
| POS-002 | Ticket Catalogue | Search · sort · filters |
| POS-003 | Timed Entry | Date picker |
| WEB-006 | Date & Session | Date picker |

---

## What should combine

### 1. Payment — five screens, one job

`WEB-012` · `GST-009` · `GST-041` · `PTR-012` · `POS-005`

Four platforms, one flow: choose a method, capture, handle the outcome. **The seven terminal
states are identical**, and `unknown` — a card charged with no response — is the same problem
on all five.

**Design once as a component with platform variants**, not five screens. The differences are
real but narrow: POS adds cash tendering and change, partner adds charge-to-account, guest
surfaces add wallet. Everything else is the same, including the failure that matters.

### 2. Shift open and close — one counter, two directions

`POS-001` · `POS-007`

The same denomination grid, the same regional denominations, the same total. They differ in one
respect and it is important: **close is a blind count** — the expected figure is withheld until
submission, because a counter who can see the expected total reconciles to it rather than to
the drawer.

**One component, a `blind` flag.** Two designs would let the blind rule get lost in the second.

### 3. Platform configuration — ten screens of "set a policy"

`ADM-008` · `ADM-011` · `ADM-014` · `ADM-015` · `ADM-017` · `ADM-019` · `ADM-021` · `ADM-030` ·
`ADM-032` · `SUP-003`

All the same shape: a scoped settings form with a save, an audit of what changed, and an
inheritance indicator. **ADR-0018 makes the inheritance indicator mandatory** — a value must say
whether it is the venue's own, the region's or the tenant's, or a manager changes it, nothing
happens, and they conclude the system is broken.

**One settings template, ten configurations of it.** Not ten screens.

### 4. Release management — five screens, one workflow

`ADM-022` · `ADM-023` · `ADM-024` · `ADM-025` · `ADM-026`

Draft → staged → promoted → notified → scheduled → end-of-support. That is one pipeline with
stages, and the state model for it already exists (`ReleaseStatus`, `RolloutStatus`).

**One pipeline screen with stage detail**, in the shape of the Publishing Status stepper the
client already uses on the white-label board — Draft · Review · Preview · Publish. Reuse their
component rather than inventing a fifth pattern.

### 5. Queue setup — three screens, one object

`BO-002` · `BO-003` · `BO-004`

Configure the queue, connect its source, and enter a wait by hand. **The third is not a
configuration screen at all** — manual entry runs during trading, by a duty manager, on a
different cadence.

**Combine 002 and 003** into a two-tab setup. **Keep 004 separate**: it is the fallback when a
feed dies, and burying it inside a settings screen puts it two clicks from someone who needs it
now.

### 6. Identity capture — two screens, one pattern

`WEB-011` · `ACC-002`

Name, contact, consent. Accreditation adds documents and a photo, guest checkout adds attendee
repetition.

**One field group with an extension slot.** Consent in particular must be the same component
everywhere — a `consentBlock` with `requiresRenewal`, because silently honouring a consent given
against a superseded notice is the compliance failure.

---

## What should not combine

**`BO-004` Manual Wait Time Entry.** Above — operational, not configuration.

**`POS-005` and the guest payment screens must stay separable at build time** even though they
share a design. POS is offline-capable and the guest surfaces are not: cash completes locally
and journals, card does not, because an offline card approval the acquirer never saw is a sale
that vanishes at settlement. **One design, two offline contracts.**

**`ADM-016` White-Label Branding** looks like the other Admin settings and is not. It is the
tenant-facing builder the client has already designed across six boards — reuse those, do not
redesign it as a settings form.

---

## What this changes in the board plan

| | Before | After |
|---|---|---|
| Form screens to design | 43 | **~22 distinct** |
| Admin Web boards | 4 | **3** |
| New shared components | — | **6** — payment, denomination counter, scoped settings, pipeline stepper, identity capture, consent block |

**Six components carry most of it.** That is the argument for designing Board 1 first and
properly: the payment component and the scoped-settings template appear on four platforms each,
and getting them right once removes a third of the remaining work.

## And the caveat that outranks all of it

**26 of the 43 are stubs.** Combining a stub with another stub produces a combined stub.

The order is: **specify the 26, then combine, then design.** Specifying is cheap — each is a
contract operation with a request body already written, so the fields exist and simply have not
been transcribed onto the screen.
