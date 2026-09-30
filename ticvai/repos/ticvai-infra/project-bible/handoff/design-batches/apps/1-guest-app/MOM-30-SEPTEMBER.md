# Claude Design session: the 30 September meeting changes (guest app, web twins, one back-office field)

> **For:** Chinmay, running Claude Design. **From:** the client meeting of 30 September (MoM 4.7, 4.8), applied to the package the same day.
> Three changes over the v4 views: the planner uses only what each park has, ride videos play with no loader, and in-park 3D navigation (ADR-0069).

## Attach
1. `handoff/design-batches/apps/1-guest-app/return/TICVAI Guest App.dc.html` (the one working file; keep drawing in it)
2. `handoff/design-batches/P02-engagement-support-01/BRIEF.md` (GST-051, GST-053, GST-054: the planner)
3. `handoff/design-batches/P02-discovery-browse-01/BRIEF.md` (GST-004: ride detail)
4. `handoff/design-batches/P02-in-venue-services-01/BRIEF.md` (GST-021, GST-038: map and at the venue)
5. `handoff/design-batches/P01-discovery-browse-01/BRIEF.md` (WEB-050, WEB-004: the web twins)
6. `docs/adr/0069-in-park-3d-navigation-is-built-natively.md`
7. Separate session, for the back office: `handoff/design-batches/P08-access-venue-02/BRIEF.md` (BO-094) with the Venue Management working file

## Prompt (paste into Claude Design)

```
Update the TICVAI Guest App working file (attached) with three changes the client agreed on 30 September. Keep the v4 look and layout of every screen; change only what is listed. Use the attached BRIEFs for each screen's fields, states and copy. Draw every new state as its own frame, named <screen id> · <state>.

1. Trip planner, multi-venue (GST-051 set-up, GST-053 the plan, GST-054 assistant; web twin WEB-050).
   - After the dates, add "Which park each day?": one park per day, chosen from the tenant's parks.
   - Each day holds only that park's rides, dining AND retail. Shops and kiosks are now plan stops beside meals (a "shop" stop with its own icon).
   - Add "Any shops you'd like to visit?" beside the cuisine choices. Only cuisines and shops that exist at the chosen parks are offered.
   - If a preference is not at the chosen park(s): before planning, the chip reads "Not at the parks you chose"; on the plan, a day shows a "Not at this park" banner naming the park that has it. Draw this as state preferenceNotAtVenue on GST-051 and GST-053.
   - The day tab and timeline show the day's park. Swap only offers alternatives from the same park. The assistant (GST-054) only suggests what the day's park has and says so when it can't.

2. Ride and attraction detail video (GST-004; web twin WEB-004).
   - The info button reveals the details and plays the video in place. No loader or loading screen in front of the video, ever.
   - State videoBuffering: the poster frame stays visible while it buffers (no spinner over it).
   - State videoUnavailable: the poster stays, with no error screen.
   - Remove any spinner the v4 capture draws over the video.

3. In-park navigation in 3D (GST-021 interactive map, GST-038 at the venue), per the attached ADR-0069.
   - A 2D/3D toggle on the map. 3D shows the park model with the walking route drawn on the paths and a live position dot; turn-by-turn walking guidance to a chosen point (e.g. the nearest food outlet).
   - State map3dUnavailable: a park without a 3D model shows the 2D map with the same route and live position (the default until the venue supplies its model). No message is needed beyond the toggle being hidden.
   - State weakGps: an approximate position ring and "Position approximate" when GPS is weak or indoors.

Return the updated working file, and list every frame you added or changed.
```

## Back office (separate session, Venue Management file)
```
On BO-094 (venue point editor, attached BRIEF), add a "Retail" field under the existing cuisine field: multi-select tags for what a shop or kiosk sells (e.g. souvenirs, toys, apparel, snacks). It is only shown for points of kind shop or retail kiosk. Same style as the cuisine field. Draw the editor with the field filled for a kiosk.
```

## After the session
Save the returned file over `return/TICVAI Guest App.dc.html` and tell Claude "design return 30 Sep". The new frames get imported the usual way, marked not client-verified until TICVAI signs them off.
