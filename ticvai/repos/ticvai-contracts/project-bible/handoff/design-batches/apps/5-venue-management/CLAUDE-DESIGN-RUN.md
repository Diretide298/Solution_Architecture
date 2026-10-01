# Venue Management in Claude Design: one clickable app, built 4 screens at a time

> **For:** Chinmay, running Claude Design. **Decided 1 October:** one session, run sequentially, 4 screens at a time, without stopping. The result is one clickable app, like the Guest web app (Guest Booking v2) and the Mobile App v4: a single board with real navigation, not loose frames.
> **Scope:** the complete Venue Management app, 1,395 screens in 159 batches:
> - P08 back office: 1,186 screens
> - P13 CMS: 103
> - P16 analytics: 70
> - P12 support console: 28
> - P11 accreditation web: 8
>
> Block A batches come first.

## Link in Claude Design
Link **one folder: `D:\Chinmay\adam\ticvai`**. Every path in the prompt is relative to it; nothing else needs attaching.
(The Guest Booking v2 reference was copied into it on 1 October: `sources/designs/TICVAI_Guest_Booking_v2_single_file.html`.)

## The prompt (paste once)

```
Build the TICVAI Venue Management web app as ONE clickable prototype, the way "TICVAI Guest Booking v2" is built: a single file, an app shell, and working navigation between screens. Not a board of loose frames.

The app shell (build it first, before any screen):
- Left sidebar with the sections and their modules: Back office (P08, grouped by its modules), CMS (P13), Analytics (P16), Support (P12), Accreditation (P11).
- A top bar with the venue switcher, search, notifications and the signed-in user.
- A home screen (the Venue Home hub, BO-100) that links into every module.
- Routing inside the file, so any screen can be opened from the sidebar, from a link, or by its screen id.

The screens come from the batch folders in handoff/design-batches. The order is in handoff/design-batches/apps/5-venue-management/README.md: section by section, Block A batches first, then the rest.
For each screen, open its batch's BUNDLE.md and screens.json. Build:
- its layout, regions and components;
- every state it lists (loading, empty, error, and the others named);
- its overlays;
- its navigation. Every navigation.transitions / exitTo entry becomes a working link or button to the target screen, carrying the values named in "carries". A target not built yet gets a placeholder page naming the screen id, replaced when you reach it.

Match these references in the linked folder: sources/designs/TICVAI_POS_Terminal_client_approved.html for density and components, sources/designs/TICVAI_Mobile.dc.html for finish and motion, and sources/designs/TICVAI_Guest_Booking_v2_single_file.html for how one clickable app with an app shell and working navigation is built. Keep one design system across all 1,395 screens: the same components, spacing, tables, forms, filters and empty states.

Work 4 screens at a time:
1. Build the next 4 screens in the order.
2. Wire their navigation into the app.
3. Save the file.
4. Continue with the next 4.

Never stop to ask questions. Where a brief is unclear, choose the most reasonable option, add a small "assumption" note on that screen, and carry on. Keep going until every screen in every batch is built.

Save to the linked folder, always as the same file:
handoff/design-batches/apps/5-venue-management/return/TICVAI Venue Management.dc.html

If the file becomes too large to keep working in, start a second file with the SAME shell and design system: "TICVAI Venue Management - part 2.dc.html". Its sidebar links back to the first file's sections, and the first file's sidebar links forward to it. Keep one app.

After every batch, append one line to handoff/design-batches/apps/5-venue-management/return/PROGRESS.md: the batch id, the screen ids built, and any assumptions. That lets a new session continue where this one stopped.
```

## If the session stops
Open a new session, link `D:\Chinmay\adam\ticvai` again, and paste:
```
Continue building the TICVAI Venue Management prototype. Read handoff/design-batches/apps/5-venue-management/return/PROGRESS.md for what is done. Open the working file(s) in that return folder, and continue with the next screens in the README order, 4 at a time, following the same rules. Do not rebuild what is done.
```

## When it comes back
Tell Claude Code "VM design return". Claude Code reads PROGRESS.md, captures each screen as a frame, and imports it. Every screen is marked not client-verified until TICVAI signs it off, and each lands in the next Tuesday/Friday release.
