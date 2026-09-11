# Running Claude Design overnight

**163 batches, 19 done.** P04 is locked as the client-approved prototype. P01 came back on
10 September: 46 frames, nothing refused on import, 45 of the 46 carrying seeded values rather
than blank rows. **That dump is the proof the loop works, and it is now the house style.**

---

## The loop, one round

```bash
cd ~/Desktop/adam/ticvai

# 1. The bundle already exists. If it does not:
python tools/export-design-batch.py <BATCH-ID>

# 2. ... the design session builds, saving frames to
#        wireframes/incoming/<BATCH-ID>/<screen-id>.html

# 3. Take the work back. Refuses anything that is not what was asked for.
python tools/import-design-frames.py <BATCH-ID> wireframes/incoming/<BATCH-ID> --apply

# 4. Put it on the boards and re-count what is left.
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

**Step 4 is what advances the loop.** The manifest reads frames off disk, so a batch stops being
pending the moment its frames are imported.

**`handoff/design-batches/QUEUE.md` is the order.** 191 batches, shipped app by shipped app,
cheapest platforms first. A session that picks its own scope is a session whose progress nothing
can count.

---

## The standing prompt

```
OVERNIGHT RUN. Work continuously. Do not stop to ask.

THE QUEUE

handoff/design-batches/QUEUE.md lists the batches in order. Work top to bottom.
For each: open handoff/design-batches/<BATCH-ID>/BUNDLE.md, build every screen it
lists, save frames to wireframes/incoming/<BATCH-ID>/, append findings to
wireframes/incoming/BATCH-LOG.md, and go straight to the next line.
Say "DONE <BATCH-ID>" and continue. No summaries between batches.

THE 46 FRAMES IN wireframes/frames/ ARE THE HOUSE STYLE

They are your own accepted P01 work. Match them: same components, same density, same
seeding conventions, the same way of showing a disabled control or an empty state.
Read two or three before starting a new platform.

This outranks every other instruction here. 191 batches that each re-derive the look
produce a second product, not more of this one.

wireframes/design-base/pos-terminal/ is the fidelity bar for operator screens.
sources/designs/ticvai-booking-archetypes.md governs anything on the booking spine.

WHERE YOU MUST BE CREATIVE, AND WHERE YOU MUST NOT

1,292 of the 7,679 component labels in this package are scaffolding a generator wrote
because nobody had named the thing: 593 read "Every <screen name>" and 663 read
"The selected <screen name>". A table on the Gate mode screen is labelled "Every gate
mode". **Replace them.** Name the column what an operator would call it, write the
empty state as a sentence a person would read, give a button the verb it actually
performs. Setting "Every gate mode" in type publishes a generator's shrug.

The other 83% of labels were written by a person. Keep those exactly.

Be creative about: naming, copy, hierarchy, what deserves emphasis, what an empty
state says, how a long list is made scannable, what a busy screen puts behind a
disclosure, how density serves the operator standing at a gate versus the analyst
reading a report.

Do not be creative about: which operations exist, what a schema contains, what a
screen is for, which states it declares, what an exit carries. Those are decided.

SEED IT WITH REAL CONTENT

This is what made P01 work. Real values, no blank padding. Prices in AED, real
ticket names, real dates, real counts, seeded from schemas.json. A table of empty
rows communicates nothing and reads as unfinished. Empty cells are the failure mode.

FRAGMENT RULES — all 46 P01 frames passed, keep passing

  <screen-id>.html in lower case, in wireframes/incoming/<BATCH-ID>/
  no <html>, <head> or <body>       the board renders around it
  no <script>                       a board is read, not run
  root element carries id="<screen-id>" in lower case
  over 200 bytes
  logo and photo slots empty, naming the source file

The import refuses; it does not salvage.

WHEN THE SPEC RUNS OUT

468 screens declare fewer than four components and 54 declare none. The brief names
them. Build what is specified, keep the rest visibly minimal, and log what was
missing. Naming a table well is creativity. Inventing an operation, a requirement or
a rule is not — that is a specification gap, and drawing over it hides it.

THE LAST 73 BATCHES ARE DIFFERENT

WS01-WS73 are workshop boards, not platform modules. Their screens already live on a
platform. Draw the surface the board describes; never invent a new screen id.

NEVER

  - re-report a finding already in BATCH-LOG.md
  - read anything under _dump/ — it is retired work
  - go looking for wireframe boards; frames are the deliverable
```

---

## What the importer refuses, and what to do about it

| refused | why | what to do |
|---|---|---|
| a screen not in the batch | a session that drifts onto neighbours has lost the plot | re-run that screen in its own batch |
| `<html>`, `<head>`, `<body>` | a page was returned, not a frame | ask for a fragment |
| `<script>` | a board is read, not run | interactivity belongs in the app build |
| no `id="<screen-id>"` | the board cannot link to it | add the anchor |
| under 200 bytes | a placeholder would count as drawn | it is a stub, not a frame |

**A refused frame is not a failed batch.** The accepted ones are already in; fix what was named
and import again. The import is idempotent.

---

## Watching it without babysitting it

```bash
python tools/derive-design-manifest.py | tail -5     # where the job stands
ls wireframes/frames/*.html | wc -l                  # frames on disk
cat wireframes/incoming/BATCH-LOG.md                 # what the sessions could not do
```

---

## Three things worth knowing

**The bundle is built from the YAML, never from a board.** It carries every field of every screen
-- `bindsTo`, `columns`, the operation behind each component, the states, the transitions and what
each carries. The boards are an output. The 22 stale renders were deleted on 10 September precisely
so that a session with local folder access could not anchor on a generator's placeholder.

**A bundle takes about 41 seconds to write** and the heavy platforms are slower. Generate them
ahead of the run; a queue that stalls at 2am on a missing bundle costs a whole night.

**Batch ids written from Python on Windows carry a trailing `\r`.** Every one of them then matches
no batch and the loop reports `FAIL` on work that succeeds when you type it by hand. `tr -d '\r'`.
