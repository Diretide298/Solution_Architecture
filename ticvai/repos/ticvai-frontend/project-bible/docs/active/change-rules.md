# Change rules: what a change request must say

> **Purpose:** The rules a CR is written and reviewed against, for the classes of mistake no checker can see
> **Owner:** Chinmay
> **Status:** Authoritative from 1 October 2026 (plan item 1F, C12)

The 26 September pull audit found 293 root issues. They fall into 36 classes, listed with their
members in the audit's `ROOT-CLASSES.md`. **A class is closed when the next instance of it fails
something.** Where the mistake is mechanical, that something is a check in `tools/` (the
`check-*.py` guards, run by `run-checks.py`). Where it is a judgement a checker cannot make (a
business rule nobody wrote down, a permission that does not fit the action), the guard is a rule
below. The CR author follows it, and the reviewer refuses a CR that does not.

Each rule names the audit roots it closes, so a reviewer can read the original finding.

---

## CR-1. Say the whole behaviour, not the happy path

A CR that adds or changes an operation states, in the contract:

1. **The rule and the validation** the operation applies, in its own description. "Validates the
   request" is not a rule.
2. **Every refusal, with its status and problem `type`.** That includes the wrong-state call: which
   states allow the action, and what a call in any other state gets (409 and the reason code).
   `check-contract-shapes` fails a new POST action with no 409 and an error with no problem type.
   It cannot tell whether the list is complete.
3. **What absence returns.** For a singleton or a lookup, say whether "not set up yet" is 404 or an
   empty 200. For an unknown parent id on a list, say whether it is 404 or an empty page.
4. **Initial values and defaults.** The status a create starts in (from `states/*.yaml`), each
   default, and the format and generator of any human-readable number or code.
5. **Every "configured" value, with its setting and its default.** A limit, a window or a TTL with
   no named setting is a number the developer will invent.
6. **Time zone and day boundary** for any date filter or business day.
7. **The permission, audience and scope level, and why they fit.** The permission must be for this
   action by this actor at this level, not the nearest one in the enum. A guest read returns no
   principal ids or internal fields.
8. **A closed vocabulary** (an enum) for any field the logic branches on. `other` only beside a
   required note (decided 28 September, R222).
9. **Stored or derived.** For each denormalised counter, flag or time-based status, say who
   maintains it and when. For anything versioned, say where the previous versions live.

Closes: R083 R091 R094 R095 R096 R097 R098 R101 R104 R106 R108 R123 R125 R126 R127 R128 R129 R134
R137 R143 R144 R149 R152 R158 R163 R169 R171 R175 R181 R199 R202 R209 R213 R214 R215 R228 R270.

## CR-2. A decision only the client can make is raised as one, never assumed silently

Platform, vendor, law and policy questions: the CI system and cloud region, a payment or
face-match vendor's interface, a guardian-consent age, retention periods, seed data, account
mappings. For each of these:

- the question goes into the Decisions Register (`handoff/TICVAI - Decisions Register.xlsx`, built
  by `tools/build-decisions-workbook.py`) with our recommended default, the owner on the client
  side, and the tickets it blocks;
- the CR applies the default and marks it **client to confirm** in the text a developer reads
  (contract description, ticket, standard). It must not read as settled;
- when the client answers differently, the answer is a new CR, not an edit to the old one.

Closes: R038 R057 R065 R117 R187 R191 R203 R205 R229 R236 R241 R267 R282.

## CR-3. List the ripple, and regenerate it in the same change

An operation is read by the lineage, the DDL, state models, events, screens, flows and tickets. A
CR names every artefact it touches, and the derived files are regenerated in the same change
(derive before check). Neither is left to a later refresh.

- **Lineage:** reads, writes and emits match the described behaviour, including side-effect,
  projection, currency and price tables, and every write into another service's table (with the
  operation or event that owns it). `check-lineage` holds the lineage against the contracts. Only
  the author can hold it against the behaviour.
- **Screens and flows:** every screen that shows the data or offers the action lists the
  operation in `apis` (and `x-ticvai-consumed-by` names the screen). Every flow step's operations
  are on the screen the step runs from. A removed or renamed operation is re-pointed on every
  consumer in the same CR.
- **A need with no operation:** a screen showing a count, a picker, a report, an export or a
  job's result names the operation that supplies it. If none exists, the CR adds one or records
  the gap on the screen (`gaps`). An asynchronous 202 names the read that follows it. A file
  reference names the upload.
- **The platform's own path:** a till reads the local catalogue bundle and never uses server
  carts. A guest surface calls guest operations. A kitchen screen calls only what `fnb` provides.

`check-screen-wiring`, `check-navigation` and `check-flows` fail the mechanical half of this. The
rest is the reviewer's to check against the list.

Closes: R071 R114 R124 R139 R141 R148 R157 R161 R166 R168 R178 R184 R188 R189 R204 R206 R207
R208 R224 R225 R226 R230 R231 R232 R242 R243 R244 R245 R259 R277 R279 R280 R284 R285 R286 R290
R291 R292 (with the checks named in ROOT-CLASSES.md).

## CR-4. One concept, one name: the glossary first

A CR that introduces a domain noun either uses the glossary's term or adds a glossary entry in the
same change, marked *proposed, client to approve*. A word from a *Never say* column is never
used as a name. `check-glossary-terms` fails a new reference field or schema named with one. A
reviewer checks prose and overloaded words (Media, Bundle, Envelope, Subject) that a checker
cannot tell apart by name.

Closes: R146 R190 R193 R195 R211 R221 (with G-BANNED-NAME for R131 R145 R147 R155 R156 R165 R194 R210 R220).

## CR-5. Acceptance names what it waits for

A ticket or CR whose acceptance depends on something not yet delivered (an upstream backend, a
sandbox credential, a fixture, a predecessor migration) names what delivers it: the ticket in
**Follows**, or the client dependency from CR-2. Never "when available".

Closes: R034 R050 R065 (with SF-DONE-GATES for R027 R032).

## CR-6. A standard is changed at its source, and copied everywhere in the same change

The project-bible standards (`api-conventions`, `backend-patterns`, `frontend-patterns`,
`naming-and-style`, `quickstart` and the rest) live in the package and are copied to the repo
mirrors and to ADAM's starter `docs/`. A CR that changes one changes the source and every copy
together. A rule in a standard says where it applies (online or offline, web or native, back
office or till). A rule that cannot hold on every platform it claims is a bug in the standard.
`check-starter-fit` (SF-DOCS-MIRROR) and `check-package` rule 29 fail a copy that drifted.

Closes: R026 R028 R038.

## CR-7. A new kind of mistake gets a guard before its fix merges

A finding that fits no class in `ROOT-CLASSES.md` is a new class. The CR that fixes it also adds
the guard: a rule in one of the `check-*.py` guards, or a rule on this page. A fix with no guard
is the one that comes back.

The eleven "one-offs" root issues of 26 September (R073 R077 R080 R085 R110 R116 R120 R132 R136
R150 R219) had no shared cause and so no guard. They stay **not closed** in ROOT-CLASSES.md until a
recurrence shows their class.

## CR-8. The audit baseline only shrinks

`handoff/audit-baseline.json` lists the members of each class that were still present when a
guard was written. A guard fails only on a member not in it. The file is written by
`python3 tools/check-<name>.py --update-baseline`, in a reviewed commit, **after a fix removes
entries**. It is never edited by hand to let a new finding through. A CR that needs a new
exception says why in the CR, and the reviewer decides.
