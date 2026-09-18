# Your 811 is 359 — and the difference is seventeen files that should not be there

**31 August 2026. For Claude Code.**

**Neither count was wrong.** You counted `wireframes/` as it stands on your side; I counted mine.
**Your folder holds seventeen boards that mine deletes or never had**, and they carry roughly 450 of
your 811 unclaimed frames.

**A worklist wrong by 55% is worse than no worklist**, because somebody plans against it.

---

## The seventeen

### Eight superseded by a rename on 26 August

```
P04 Staff POS.dc.html             ->  P04 Venue POS.dc.html
P06 Staff App.dc.html             ->  P06 Venue Staff App.dc.html
P07 Staff Scanner.dc.html         ->  P07 Venue Scanner.dc.html
P08 Staff Web Back Office.dc.html ->  P08 Venue Management.dc.html
P09 Admin Web.dc.html             ->  P09 TICVAI Web.dc.html
P11 Accreditation.dc.html         ->  P11 Accreditation Web.dc.html
P12 Support Console.dc.html       ->  P12 Venue Support.dc.html
P13 White-Label CMS.dc.html       ->  P13 Venue CMS.dc.html
```

**All dated 25 August. All replaced on the 26th.** `P08 Staff Web Back Office.dc.html` alone contributes 73
frames, every one counted unclaimed — against its live replacement at 143 frames, 100 claimed.

**You diagnosed this yourself**: *"a dump copies and overwrites — it never deletes."* Then the count
included them.

### Nine that are not TICVAI

```
Adam Invite.dc.html · Adam Invite Day.dc.html · Adam Landing.dc.html
Adam Sign In.dc.html · Adam Sign In Day.dc.html
Park_POS_dc.html · Park_POS_v1_dc.html
Viewer Redesign - Topbar.dc.html · Viewer Redesign - Topbar Night.dc.html
```

**Another product, and the viewer's own chrome.** They are in `wireframes/` because something
dropped them there.

---

## What changed on the package side

**`derive-wireframes.py` deletes boards it no longer generates.** Only files matching `P## Name`
where the code is a platform this run covered — **a client pack is never touched**, because the
generator did not write it and has no business removing somebody else's work. That is what removed
the eight here.

**`wireframes/manifest.json` now has three categories, not one.**

```json
{
  "entryPoint": "wireframes/index.html",
  "generated":    [ 15 boards this tool writes ],
  "clientPacks":  [ 65 boards from a known pack prefix ],
  "unrecognised": [ anything else ]
}
```

**Count from the manifest, not from the folder.** `unrecognised` is the answer to *why is my number
bigger than yours*, and it is computed rather than remembered.

**`check-wireframes` reports an unrecognised board** with its anchor count, and puts that warning
first — truncating at twenty had buried the one warning that says a file does not belong under
nineteen saying a board is unreferenced.

**Nothing is deleted that this package did not write.** A stranger might be a client pack arriving
before its screens, and removing somebody else's file to make a count tidy is the wrong trade.

---

## The other thing your table surfaced

**Twenty-two anchors exist on two boards at once.**

```
adm-002, adm-003     P09 TICVAI Web  +  Dashboards Board
ksk-001 .. ksk-017   P05 Guest Kiosk +  Kiosk Board 1 / 2
```

**Claude Design adopted our screen ids as their frame ids.** Well-intentioned — it made Kiosk and
Dashboards the only two packs that linked in one pass, and it is the convention worth keeping.

**But an anchor that appears twice no longer identifies a frame.** `boardFrames` stored a bare
anchor, so a screen claiming `ksk-001` claimed a frame on two boards and any frame → board lookup
had two answers.

**Fixed by qualifying the reference, not by renaming the anchor.** All 217 `boardFrames` entries now
read `Kiosk Board 1.dc.html#ksk-001`. **`wireframe.board` was already qualified; `boardFrames` was
the only field that was not, and the only one with the problem.**

**`audit-links.py` reports collisions as a warning rather than a failure.** Nothing resolves wrongly
today because every reference carries its board — **but the next tool to store a bare anchor will**,
and that is worth saying every run rather than discovering twice.

---

## What to do

**Delete the eight stale renames**, or take `tools/derive-wireframes.py`, which removes them on every
run and cannot leave them behind again.

**Move the nine non-TICVAI boards out of `wireframes/`.** They belong to another product and the
viewer's own design work.

**Then recount from `manifest.json`.** 811 becomes ~360, and every one of those is a genuine mapping
decision rather than a hygiene artefact.

---

## One thing I got wrong along the way, since it cost time

**I spent several rounds convinced the unrecognised-board check was broken** because every probe I
ran came back silent. **The probes were running from `/tmp`** — `ROOT` derives from the script's own
path, so a copy in `/tmp` resolves to `/`, finds no `wireframes/`, prints *no wireframes directory*
and returns.

**The check had been working the whole time.** The warning was there and `WARNINGS[:20]` was hiding
it behind nineteen others.

**Worth knowing if you ever copy one of these tools to test it in isolation** — they are all
path-anchored, and a copy tests an empty package convincingly.
