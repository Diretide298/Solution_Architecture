# POS and kitchen display in Claude Design: one clickable app, built 4 screens at a time

> **For:** Chinmay, running Claude Design. **Decided 1 October:** one session, run sequentially, 4 screens at a time, without stopping. The result is one clickable app, like the Guest web app (Guest Booking v2), not loose frames. Run it after Venue Management, or alongside it if you can.
> **Scope (updated 1 October, after the POS v2 decisions):** 17 screens in 2 batches, added to the POS app: **the 7 POS screens neither POS build draws** (batch `P04-not-in-v2-01`: POS-009 Staff Roster, POS-010 Add to Existing Ticket, POS-015 Cash Operations Dashboard, POS-017 Cash In / Cash Out, POS-018 Safe Drop & Cash Transfer, POS-019 Shift Templates & Policies, POS-024 Outlet Setup) and **the 10 kitchen display screens** (batch `P15-kitchen-01`, KIT-001 to KIT-010). The other 25 POS screens (P04) are LOCKED: they are the POS v2 build (sources/designs/TICVAI_POS_Terminal_v2.html, 1 October), our improved version of the client-approved terminal, a candidate the client has not approved yet — copy them as they are into the app so the new screens link to them; do not redesign them. That includes the two new screens, POS-030 Sales Journal and POS-031 Reservations & Group Arrivals: v2 already draws them (its sales journal and cart history, its Bookings), so **do not draw them again**. POS-009 and POS-015 build on v2's shift panel (current shift, clock in and out, shift history, the cash drawer) **without its "Expected in drawer"**: the count is blind. KIT-007 owns the customer-facing order status board and builds on v2's queue status board; the till's Queue mirrors it. Where v2 contradicts the POS v2 decisions of 1 October (docs/registers/pos-v2-decisions.md), draw the decision: no expected figure while counting, nothing encoded before payment, no "Report to facilities", no "Cancel" on queue cards. The v2 file is 9.7 MB and not in git: it is on this machine at that path.

## Link in Claude Design
Link **one folder: `D:\Chinmay\adam\ticvai`**. Every path in the prompt is relative to it.

## The prompt (paste once)

```
Build the TICVAI POS and kitchen display app as ONE clickable prototype, the way "TICVAI Guest Booking v2" is built: a single file, an app shell, and working navigation between screens. Not a board of loose frames.

The app shell (build it first, before any screen):
- Navigation: the POS as the v2 terminal (sources/designs/TICVAI_POS_Terminal_v2.html), plus a Kitchen section for the kitchen display screens.
- A top bar with the outlet, the shift and the signed-in cashier or kitchen station.
- A home screen (the POS home, the Sales board, from the v2 terminal) that links into every section.
- Routing inside the file, so any screen can be opened from the sidebar, from a link, or by its screen id.

The screens come from the batch folders in handoff/design-batches. The order is in handoff/design-batches/apps/2-pos/README.md: section by section, Block A batches first, then the rest.
For each screen, open its batch's BUNDLE.md and screens.json. Build:
- every item in the bundle's "Design inputs from the client meetings" section: the client's own requirements from the meetings, which win over the references where they differ (an open question gets its stated default);
- its layout, regions and components;
- every state it lists (loading, empty, error, and the others named);
- its overlays;
- its navigation. Every navigation.transitions / exitTo entry becomes a working link or button to the target screen, carrying the values named in "carries". A target not built yet gets a placeholder page naming the screen id, replaced when you reach it.

Build only the screens of the two batches the README lists to draw: P04-not-in-v2-01 (seven POS screens the v2 build does not draw) and P15-kitchen-01 (the kitchen display). Every other POS screen, including POS-030 Sales Journal and POS-031 Reservations & Group Arrivals, is copied from the v2 build as it is. POS-009 and POS-015 build on v2's shift panel without "Expected in drawer" (the count is blind); KIT-007 is the guest-facing order status board, in the look of v2's queue status board.

Match these references in the linked folder: sources/designs/TICVAI_POS_Terminal_v2.html (the design to match exactly; the new screens and the kitchen display take its look, and its Queue's guest status board is what the kitchen display's KIT-007 owns and the Queue mirrors), sources/designs/TICVAI_Mobile.dc.html for finish, and sources/designs/TICVAI_Guest_Booking_v2_single_file.html for how one clickable app with working navigation is built. Keep one design system across every screen: the same components, spacing, tables, forms, filters and empty states.

Before the first screen, read "Design inputs from the client meetings" in handoff/design-batches/apps/2-pos/README.md and apply the app-wide inputs to the shell and to every screen.

Work 4 screens at a time:
1. Build the next 4 screens in the order.
2. Wire their navigation into the app.
3. Save the file.
4. Continue with the next 4.

Never stop to ask questions. Where a brief is unclear, choose the most reasonable option, add a small "assumption" note on that screen, and carry on. Keep going until every screen in every batch is built.

Save to the linked folder, always as the same file:
handoff/design-batches/apps/2-pos/return/TICVAI POS.dc.html

If the file becomes too large to keep working in, start a second file with the SAME shell and design system: "TICVAI POS - part 2.dc.html". Its sidebar links back to the first file's sections, and the first file's sidebar links forward to it. Keep one app.

After every batch, append one line to handoff/design-batches/apps/2-pos/return/PROGRESS.md: the batch id, the screen ids built, and any assumptions. That lets a new session continue where this one stopped.
```

## If the session stops
Open a new session, link `D:\Chinmay\adam\ticvai` again, and paste:
```
Continue building the TICVAI POS and kitchen display prototype. Read handoff/design-batches/apps/2-pos/return/PROGRESS.md for what is done. Open the working file(s) in that return folder, and continue with the next screens in the README order, 4 at a time, following the same rules. Do not rebuild what is done.
```

## When it comes back
Tell Claude Code "POS and kitchen display design return". Claude Code reads PROGRESS.md, captures each screen as a frame, and imports it. Every screen is marked not client-verified until TICVAI signs it off, and each lands in the next Tuesday/Friday release.
