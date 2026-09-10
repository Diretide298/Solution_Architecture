# Running Claude Design non-stop

**163 batches pending of 169.** Six are locked: P04 is already built as the client-approved
prototype and is the fidelity reference every other batch is measured against.

The loop is four commands and one session. Nothing in it needs a decision, which is the point —
a round that needs you to think is a round that stops when you go to bed.

---

## The loop, one round

```bash
cd ~/Desktop/adam/ticvai

# 1. Cut the next pending batch. Writes handoff/design-batches/<id>/
python tools/export-design-batch.py --next

# 2. ... the Claude Design session runs, and saves frames to
#        wireframes/incoming/<id>/<screen-id>.html

# 3. Take the work back. Refuses anything that is not what was asked for.
python tools/import-design-frames.py <id> wireframes/incoming/<id> --apply

# 4. Put it on the boards and re-count what is left.
python tools/derive-wireframes.py
python tools/derive-design-manifest.py
```

**Step 4 is what advances the loop.** `--next` reads the manifest, and the manifest reads frames
off disk — so a batch stops being pending the moment its frames are imported, and the next
`--next` gives you a different one. Skip step 4 and you will cut the same batch forever.

---

## The standing prompt

**Claude Design does not cut batches and should not be asked to.** The batch is decided here, from
the manifest, and handed over whole -- that is what keeps the work list honest, because a session
choosing its own scope is a session whose progress nothing can count.

`export-design-batch.py` writes **`BUNDLE.md`**: the brief and all three JSON payloads in one file,
in the order they should be read. Upload that, then paste the prompt below. Four separate files
means four chances to arrive with three, and the one most likely to be dropped is `schemas.json` --
the one that stops a build inventing its own data.

```
The attached BUNDLE.md is one batch of screens to build. Read it top to bottom: the brief first,
then screens.json, operations.json and schemas.json.

Build every screen the brief lists, from the bundle and nothing else.

Match the depth of the reference build named in the brief: real state, seeded data, controls that
do something. Seed from schemas.json - a build that invents its own data disagrees with the
backend on day one.

Return one file per screen, named <screen-id>.html in lower case (web-005.html). Each file is a
FRAGMENT, not a page:
  - no <html>, <head> or <body> - the board renders around it
  - no <script> - a board is read, not run
  - the root element must carry id="<screen-id>" in lower case
  - over 200 bytes

Do not invent an operation. If a screen needs something operations.json does not have, say so in
your reply - that is a finding, not a gap to fill with a plausible endpoint.

When the batch is done, say only: DONE <BATCH-ID>, then list any screen you could not build and
why.
```

Save what comes back into `wireframes/incoming/<BATCH-ID>/` and run the import.

**Why the fragment rules are in the prompt and not only in the importer.** `import-design-frames`
refuses a whole document, a `<script>`, a wrong-batch screen, a missing anchor and anything under
200 bytes -- but a refusal after the work is a wasted session. The rules are stated up front so the
session does not have to be run twice.

## What the importer refuses, and what to do about it

| refused | why | what to do |
|---|---|---|
| a screen not in the batch | a session that drifts onto neighbours has lost the plot | re-run that screen in its own batch |
| `<html>`, `<head>`, `<body>` | a page was returned, not a frame | it nested a document in a board; ask for a fragment |
| `<script>` | a board is read, not run | the interactivity belongs in the app build |
| no `id="<screen-id>"` | the board cannot link to it | add the anchor; nothing else needs to change |
| under 200 bytes | a placeholder would count as drawn | it is a stub, not a frame |

**A refused frame is not a failed batch.** The accepted ones are already in; fix what was named and
import again. The import is idempotent, so re-importing an unchanged frame reports it unchanged
rather than writing it twice.

---

## Watching it without babysitting it

```bash
# where the whole job stands
python tools/derive-design-manifest.py | tail -5

# which batches are still pending
python tools/export-design-batch.py --list

# frames actually on disk
ls wireframes/frames/*.html | wc -l
```

A drawn frame shows on its board card with a green **drawn** badge, so a reviewer looking at
ninety cards can tell which have been through a designer and which are still the generator's own
work. **Without that badge a board flatters itself.**

---

## Two things worth knowing before starting

**46 of the 169 batches are fully drawable as specified.** The rest contain at least one screen
declaring fewer than four components, and a screen with almost nothing declared cannot be drawn
from what it declares — the session will invent, or it will produce something thin. Prefer the
drawable ones first; the manifest marks them.

**The frame replaces the picture and nothing else.** `derive-wireframes` renders the header, the
workshop badge, the operations, the states, the entry parameters, the exits, the machine and the
overlays *around* the frame. A session that never knew those existed cannot lose them, which is
why frames are per screen and not per board — and why the 155 whole-file boards from before
10 September had to be archived.
