> Copied into the package on 21 October 2026 from the r9 investigation of the WEB-007 seat page (the lead's "ui-pull" findings), so the change entries CHG-R9UI-001 to -004 can cite it inside git (ticvai/CLAUDE.md rule 12). Unchanged below this note; the paths it names are where the evidence was on the day.

# Why WEB-007 was not built to the approved design (21 October 2026)

This was a read-only investigation. Nothing was edited.

## Screen and tickets

- **Screen: WEB-007, Interactive Seat Selection.**
  - Platform: P01 Guest Web. Route: `/booking-and-selection/seat-map-selection`. Repository: **ticvai-guest-web**.
  - Defined in `ticvai/screens/P01-guest-web-storefront.yaml:1806-2111` and `frontend/guest-web.yaml:111-117`.
- **Tickets.** The parent is **#28197** (`APP-WEB-WEB-007`). It has three sub-tasks:
  - **#31848**, build;
  - **#31849**, connect;
  - **#31850**, tests.

  All are Chitrangi Mestry's, in Block A week 2.
- **GST-043 is a different ticket:** Arabic / RTL experience, P02 guest app (React Native), #27892.
- **Check the repository with her.** This route belongs to guest web. The guest app is React Native, not Next.js. Either the repository was named wrong, or WEB-007 was built in the wrong one.

## 1. What the wireframe and the prototype show

**The board frame** (`wireframes/P01 Guest Web.dc.html:272-292`) is one image, `frames/img/web-007.png`, 1440×900.
- It comes from prototype build 28 Sep. The YAML names build 30 Sep.
- It shows the populated stadium view on the dark Union Arena theme:
  - the header and navigation;
  - section chips, Sport/Concert and 2D/3D toggles, a zone-pricing strip and the 3D bowl;
  - the "Your seats" basket;
  - the Sahli button.
- **No state is drawn.** The footer only names them: loading, error, emptyFirstRun, emptyNoAccess, offline, emptyNoResults. All 50 boards are built the same way, with one frame each and no state frames.

**The prototype** (`sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`) does draw the seat step:
- the theatre plan at lines 1713-1790;
- the stadium bowl at 1835-1950;
- the view model around 10000-10080.

Per state:
- **Waiting:** a dashed note, "Choose … to see the seats." (1718).
- **Loading:** a turnstile loader with the Sahli mascot and a progress bar (4950-4962).
- **Error:** nothing on the seat step. The only illustrated error is **WEB-029**, "Error / Sold out / Maintenance" (4746-4782, `frames/img/web-029.png`):
  - a tinted warning circle, the kicker "ERROR" and "Something went wrong on our side";
  - "Your basket is safe…" and a "Wait a minute" pill;
  - **Try again** and **Back to home**, and a reference number;
  - the full header and footer.

  The developer's page is a bare version of this card.
- **Empty:** only the empty-basket text.

**The screen YAML says nothing about the look.**
- Its states are one-line text from the generator (`tools/generate-screens-from-contracts.py:281`).
- Its layout (`detail` / `statusTracker` / `detailPanel`) is not the bowl.
- A third, generated frame styled like the till is attached (`wireframes/incoming/P01-booking-selection-01/web-007.html`, Manrope, "Aqua Park Gate A").
- `_design-tokens.yaml` was taken from the till (Manrope), not from the guest prototype (Archivo, a `--brand` colour per venue).

## 2. Can the prototype be cut per view?

**Not as static markup.**
- It is an `<x-dc>` template with `sc-if` / `sc-for` bindings over one state, and the view model is in JavaScript.
- It needs 5 or more sibling scripts, Leaflet and Google Fonts.
- The seat view is spread over 6 or more regions, and the bowl is a three.js canvas.

**It can be cut by rendering it.**
- `tools/capture-prototype.mjs` already drives a view by plan steps and saves a PNG.
- Playwright could also save the rendered region's markup, with computed styles and the resolved colour and font settings.
- Two gaps:
  - `tools/capture-plans/guest-web-v2.json` covers only 11 web screens, and neither WEB-007 nor WEB-029.
  - The per-state routes (`#WEB-007?state=error`) asked for in `design-r1/apps/guest-web/BOARD.md` were never built.

## 3. Causes beyond the missing wireframe

1. **The ticket text never asks for identical UI.**
   - The build sub-task says only "Matches the design", with no design named (`tools/op-descriptions.py:412-414`).
   - The state checklist is cut to "State error: Could not load." (`op-descriptions.py:490-491`).
   - Only 22 of 8,443 descriptions mention a prototype or wireframe.
2. **The workspace rules push the agent toward a placeholder.** The frontend starter CLAUDE.md says:
   - a wireframe from anywhere else "is not the spec" (lines 42-50);
   - "build exactly what the ticket… describe[s]" (109);
   - use a placeholder layout unless the wireframe came through ADAM (130-132).

   `/ticket` step 4 says the same. None of them mention the look.
3. **The spec page names no design.** `handoff/service-docs/frontend/WEB.md:428-488` has no prototype, view or design tokens.
4. **No state has a visual pattern.** Nothing maps error to the WEB-029 card, loading to the turnstile loader, or waiting to the dashed note.
5. **The YAML layout and the generated frame contradict the approved view.**
6. **No app shell or design system is planned.**
   - No ticket builds the guest web shell: header, navigation, footer, progress bar, basket, loader, status card, offline banner.
   - No ticket builds the `design-tokens` or `ui` packages.
   - ADAM's setup copies only the coding standards (`setup.ps1:383-395`).
7. **There is no mock API in week 2.** The frontend mock server belongs to SETUP-SEED (#27684), Block A week 5. So the page opens in its error state, which is what the lead judged.

## Proposed fixes

The wireframe-in-pull fix is with the ADAM lane.

1. **Ticket templates.** Add a section "Design (client-approved, build identical)" that names the prototype view and the pulled frames. Replace "Matches the design" with "the visual check passes for every state". Sources: `op-descriptions.py`, `op-release.py`, `build-service-docs.py`.
2. **The starter CLAUDE.md and `/ticket`.**
   - A client-verified screen is built to look identical to the pulled frames.
   - Frames written by `adam_pull` count as "through ADAM".
   - The placeholder applies only when no frame was pulled.
3. **Screen YAML.**
   - Add a view for each state: WEB-007's error state uses the WEB-029 card, loading the turnstile loader, waiting the dashed note.
   - Add a check that fails when a client-verified screen has a state with no view.
   - Copy for states the client never saw goes to the lead as client-approved UI, not invented.
4. **Plan.** Add a week-1 shell and design-tokens ticket for each frontend repository (for example `APP-WEB-SHELL`), with the tokens taken from the prototype's CSS. Every screen ticket comes after it. Replace the till-derived tokens file with one for guest.
5. **Layout.**
   - Label the generated layout and the board frames "structure only, not the look".
   - Never hand out the till-styled generated frame as the design.
6. **Captures.**
   - Extend `capture-plans/guest-web-v2.json` to every screen with a prototype view (WEB-007's three flows, and WEB-029) and to every state that can be drawn.
   - Build the per-state routes.
   - Capture the rendered markup and the design tokens beside each PNG.
7. **Mock API.** Move a frontend mock (MSW or Prism, built from the published contracts, with data that mirrors the prototype's sample venues) to week 1.
8. **Repository.** Confirm where WEB-007 was built.

## 4. A "built identical" check

- **Reference.** Capture each screen and state with `capture-prototype.mjs`:
  - at 1440×900 and 390×844;
  - left-to-right and right-to-left;
  - for each venue the view names.

  A state with no view of its own uses its mapped pattern, such as WEB-029.
- **Candidate.** Playwright opens the built route against the mock and forces each state:
  - a normal response;
  - an error;
  - a delay, for loading;
  - offline;
  - an empty list.
- **Compare:**
  - a screenshot difference within a tolerance, masking data-driven regions;
  - the shell is present;
  - the computed font and brand colours equal the prototype's design tokens;
  - every approved label is there;
  - the right-to-left mirror is correct.
- **Gate.** The build sub-task is done when "the visual check passes per state". The side-by-side and difference images go into the Ready-for-QA comment.

## Evidence

- `D:\wt\r8-rehearsal-pull\work-4\direct\workspace\.adam\work\28197\` (the README and `screen-WEB-007.json`)
- `viewer/mcp/tools.mjs:253-270, 565-634`: there is no design kind in the pull. Lines 1670-1711: the 400-line, 60 KB read window.
- `viewer/server.mjs:1543-1553`: the 415 that refuses `.html`.
- `viewer/mcp/setup/starters/frontend/CLAUDE.md:42-50, 109, 130-132` and `.claude/commands/ticket.md:28`.
- `ticvai/wireframes/P01 Guest Web.dc.html:272-292`, `frames/img/web-007.png` and `web-029.png`.
- `ticvai/tools/capture-prototype.mjs` and `tools/capture-plans/guest-web-v2.json`.
