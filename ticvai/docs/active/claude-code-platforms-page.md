# Build `platforms.html` — the one page in the viewer with no script

**Scope: `aster/viewer` only.** Do not touch the package. The TICVAI package is being edited in
parallel and `refresh.sh` regenerates 179 derived files from `screens/` and `contracts/` — **if both
of us run it, the loser's output is silently replaced with no error and no conflict, only a changed
count.**

---

## The state

`platforms.html` is tracked, loads `/platforms.js`, and **that file has never existed in the repo.**
The page ships a `#platforms` container and a four-option sort control with nothing to populate
them. Static shell.

**It is the last symptom in an area where the other two are now closed** — `platform-P01.md` read 35
against a live 46 and has been corrected, and the fifteen platform docs were verified against live
counts with zero drift.

---

## What the payload holds

`/pkg/<project>/index` carries the platform blocks. Fifteen of them:

```
code  name                  audience       formFactor    screens   ops
P01   Guest Web             guest          web                46   112
P02   Guest App             guest          mobileApp          63    97
P04   Venue POS             staff          posTerminal        24   118
P05   Guest Kiosk           guest          kiosk              17    22
P06   Venue Staff App       staff          mobileApp          66   180
P07   Venue Scanner         staff          handheld           11    23
P08   Venue Management      staff          web               143   441
P09   TICVAI Web            platformAdmin  web                37   110
P10   Partner Web           partner        web                21   105
P11   Accreditation Web     public         web                 8     3
P12   Venue Support         staff          web                 8    33
P13   Venue CMS             staff          web                20    77
P14   Developer             partner        web                 8    21
P15   Kitchen Display       staff          kiosk              10    24
P16   Venue Analytics       staff          web                10    20
```

Per platform the block also carries `app`, `runtime`, `offlineCapable`, `deployment`, and the
screens themselves with `requiresModule`, `wave`, `density`, `apis[]`, `wireframe.status`.

**Read it through `apiFetch`**, which now resolves the project via `ensureProject()`. Do not build a
second path to the registry.

---

## What the page should answer

**Not "list the platforms".** The index already lists them and a second list is a second thing to
keep in step.

**Four questions a reader actually arrives with**, and the sort control is the clue to the first:

**Which surfaces are thin?** `P11` has 8 screens and 3 operations; `P08` has 143 and 441. **A
platform with more screens than operations is drawing more than it can fetch** — that ratio is the
one number nobody currently sees.

**Which are drawn?** 64 of 492 screens carry `wireframe.status: designed`, and they sit on exactly
three platforms — P04, P06, P08, the three with client packs. **Twelve platforms are wholly
generated.** Show it per platform, because "12 of 15 undrawn" is the fact that decides what to
commission.

**Which are offline-capable, and does the wiring agree?** `offlineCapable` is a platform flag;
`x-ticvai-offline-capable` is an operation flag. **They disagreed on 37 screens until yesterday**
and nothing on any page compares them.

**What does each one license?** `requiresModule` spans 18 values. A platform's module spread is what
a tenant sees when they buy less than everything.

---

## Two things to get right

**Reuse the existing renderers.** The screen list, the module pill, the wave marker and the audience
chrome all exist elsewhere in `public/`. **A platform page with its own card component is a second
place to fix a rendering bug.**

**A platform with no screens must render.** Every folder in a package is optional and the Audit says
what is missing rather than the server failing — **this page should behave the same way.** A package
with one contract and no `screens/` should get an empty state that names what is absent, not a
blank div.

---

## Done means

- `/platforms.js` exists, `#platforms` fills, all four sort options work
- `pages-check.mjs` still 53 of 53 — it was 52/1 before the `validation.html` fix
- No 4xx and no page errors on a fresh profile with `aster-project` cleared, the same bar the
  project-segment fix was verified against
- No file outside `aster/viewer` modified

---

## What not to do

**Do not add the undrawn boards to this.** That is `tools/derive-wireframes.py` and `screens/*.yaml`
in the package, both upstream of `derive-diagrams`, and it is the collision described at the top.

**Do not fix `check-package`'s six mirror errors.** The `repos/` question is undecided and deleting
5,325 files to silence a check is the wrong order.
