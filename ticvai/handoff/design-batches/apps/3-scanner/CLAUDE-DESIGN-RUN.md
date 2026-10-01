# Scanner in Claude Design: one clickable app, built 4 screens at a time

> **For:** Chinmay, running Claude Design. **Decided 1 October:** one session, run sequentially, 4 screens at a time, without stopping. The result is one clickable app, like the Guest web app (Guest Booking v2), not loose frames. Run it after Venue Management, or alongside it if you can.
> **Scope:** the complete Scanner app (P07), 11 screens in 2 batches, on a handheld scanner.

## Link in Claude Design
Link **one folder: `D:\Chinmaydam	icvai`**. Every path in the prompt is relative to it.

## The prompt (paste once)

```
Build the TICVAI Scanner app as ONE clickable prototype, the way "TICVAI Guest Booking v2" is built: a single file, an app shell, and working navigation between screens. Not a board of loose frames.

The app shell (build it first, before any screen):
- Navigation: a single-task flow: gate selection, scan, result, and the exception screens.
- A top bar with the gate, the signed-in operator and an online/offline indicator.
- A home screen (the gate selection screen) that links into every section.
- Routing inside the file, so any screen can be opened from the sidebar, from a link, or by its screen id.

The screens come from the batch folders in handoff/design-batches. The order is in handoff/design-batches/apps/3-scanner/README.md: section by section, Block A batches first, then the rest.
For each screen, open its batch's BUNDLE.md and screens.json. Build:
- every item in the bundle's "Design inputs from the client meetings" section: the client's own requirements from the meetings, which win over the references where they differ (an open question gets its stated default);
- its layout, regions and components;
- every state it lists (loading, empty, error, and the others named);
- its overlays;
- its navigation. Every navigation.transitions / exitTo entry becomes a working link or button to the target screen, carrying the values named in "carries". A target not built yet gets a placeholder page naming the screen id, replaced when you reach it.

Match these references in the linked folder: sources/designs/TICVAI_POS_Terminal_client_approved.html for components, sources/designs/TICVAI_Mobile.dc.html for finish, and sources/designs/TICVAI_Guest_Booking_v2_single_file.html for how one clickable app with working navigation is built. Keep one design system across every screen: the same components, spacing, tables, forms, filters and empty states.

Before the first screen, read "Design inputs from the client meetings" in handoff/design-batches/apps/3-scanner/README.md and apply the app-wide inputs to the shell and to every screen.

Work 4 screens at a time:
1. Build the next 4 screens in the order.
2. Wire their navigation into the app.
3. Save the file.
4. Continue with the next 4.

Never stop to ask questions. Where a brief is unclear, choose the most reasonable option, add a small "assumption" note on that screen, and carry on. Keep going until every screen in every batch is built.

Save to the linked folder, always as the same file:
handoff/design-batches/apps/3-scanner/return/TICVAI Scanner.dc.html

If the file becomes too large to keep working in, start a second file with the SAME shell and design system: "TICVAI Scanner - part 2.dc.html". Its sidebar links back to the first file's sections, and the first file's sidebar links forward to it. Keep one app.

After every batch, append one line to handoff/design-batches/apps/3-scanner/return/PROGRESS.md: the batch id, the screen ids built, and any assumptions. That lets a new session continue where this one stopped.
```

## If the session stops
Open a new session, link `D:\Chinmay\adam\ticvai` again, and paste:
```
Continue building the TICVAI Scanner prototype. Read handoff/design-batches/apps/3-scanner/return/PROGRESS.md for what is done. Open the working file(s) in that return folder, and continue with the next screens in the README order, 4 at a time, following the same rules. Do not rebuild what is done.
```

## When it comes back
Tell Claude Code "Scanner design return". Claude Code reads PROGRESS.md, captures each screen as a frame, and imports it. Every screen is marked not client-verified until TICVAI signs it off, and each lands in the next Tuesday/Friday release.
