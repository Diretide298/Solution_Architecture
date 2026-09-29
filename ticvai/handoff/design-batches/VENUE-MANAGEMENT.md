# Venue Management in Claude Design: how to run it

> **Purpose:** wireframe every Venue Management (P08) and CMS (P13) screen, batch by batch  
> **Owner:** Chinmay  
> **Status:** Ready 29 September 2026. Batches exported by `tools/export-design-batch.py`

The Venue Management and CMS screens are specified: each screen binds its operations, the configuration screens bind their writes, and every screen has a purpose, a pattern and states (readiness close-out, 29 September). What they lack is a design. There are **142 batches, about 1,286 screens, up to 10 per batch**. Each batch folder here has `BRIEF.md` and a `BUNDLE.md` to hand a session. **Batch folders are named by the manifest's batch id:** `P08-<module>-NN` and `P13-<module>-NN` for module batches, and `WSnn` for the batches cut from the client's workshop boards (most of Venue Management). `wireframes/design-manifest.json` lists each batch with its platform and screens.

## One session per batch

1. In Claude Design, link the batch folder (for example `handoff/design-batches/P08-access-venue-01`) and the two references it names under `sources/designs/`: the client-approved POS terminal, and `TICVAI_Mobile.dc.html`.
2. Paste the prompt below, with the batch id filled in.
3. When it is done, put the returned files in the batch folder under `return/`, and tell Claude Code "batch <id> is back". Claude Code captures each screen as a frame, imports it with `tools/import-design-frames.py`, refreshes, and it shows in ADAM's UI/UX.

**Order:** the first-batch screens (the Venue Home hub BO-100, and BO-021, BO-039, BO-040), then the configuration batches module by module (Access & Venue, Sell, Orders & Money, Stock & Supply, People & Access Rights, Guests & Marketing, Venue Operations), then the CMS (P13). Batches that only read, such as analytics and command centres, go last.

## The prompt

```
Build batch <BATCH ID> of TICVAI Venue Management. Read BRIEF.md in this folder first, then
BUNDLE.md (screens, operations, schemas, permissions). BRIEF.md's rules outrank anything here.

Match the client-approved look: sources/designs/TICVAI_POS_Terminal_client_approved.html for operator
density and components, sources/designs/TICVAI_Mobile.dc.html for finish and motion. This is the
back office on a desktop browser (1440 wide): a left navigation rail with the module sections, a top
bar with the venue switcher, and the screen in the main area.

Return ONE self-contained file, return/<BATCH ID>.dc.html, a working surface:
- Every screen in the batch is reachable, and opens directly from the URL hash #<screen id in lower
  case> (for example #bo-144), already in its main populated state.
- The element that holds each screen carries data-screen-label="<SCREEN ID> <Screen name>".
- Every state the screen declares (loading, empty, error, offline, no access, and its own) can be
  reached from a small state switcher, and #<id>?state=<state name> opens it directly.
- Seed realistic UAE data from schemas.json (AED, venues, staff names). No lorem ipsum.
- Controls that need a permission are gated. Nothing from the bundle (operation ids, field names,
  permission keys, screen ids) appears as text a user reads, except the data-screen-label attribute.
- No external requests except Google Fonts. Images inline or omitted.
If a screen needs something the bundle does not have, draw it greyed with a short note, and list it in
return/FINDINGS.md. Do not invent endpoints.
```

## What happens to what comes back

- A capture script opens each `#<id>` in a headless browser. It checks that the `data-screen-label` is present and screenshots it, and the frame goes onto the screen's board, like the 148 client prototype frames of 29 September. Each screen's `wireframe.status` goes to `review`.
- The working file itself stays in `return/`, so a reviewer can click through a whole batch.
- `return/FINDINGS.md` is read for missing operations. Each becomes a contract change, not a guess.
