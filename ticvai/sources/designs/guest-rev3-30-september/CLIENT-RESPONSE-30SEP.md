# Response to Website Feedback, 30 September

Each point from the feedback document, what changed, and where to see it. The changes are on the website and in the mobile app.

## 1. Group booking: product missing, enter the number of people
- **Theme park → Group / school booking** now starts with four group tickets: School, Corporate, Tour operator and Community. Each shows a per-person price and a minimum group size.
- After choosing a ticket, **How many people** has a number box. Guests can type the headcount (for example 45) or use − and +. Supervisors are listed separately and are free. The enquiry panel shows the estimate as *School group · Guests × 45*.
- **Water park → Group booking** works the same way: pick a session, then enter the number of swimmers and supervisors. The Group size dropdown has been removed on both.
- On mobile the stepper has a +10 button for large groups.
- We couldn't open the Etihad Museum link from here, so the layout follows the ticket-then-headcount pattern your note describes. Please send a screenshot if something from that page is missing.

## 2. Multi-park ticket adds an extra adult line
- The guest counters now take their price from the park ticket you pick. Choosing *2 park ticket* with 3 adults gives one line: **2 park ticket · Adult × 3 = AED 1,425**. The separate *Adult × 3* line is gone.
- Child and senior prices scale from the chosen ticket. Infants stay free.

## 3. Surfing session added to the cart straight away
- Picking a session no longer adds anything to the cart.
- Once a session is chosen, **Tickets for Intermediate surf · 19:30** appears with Surfer (the session price), Junior surfer 10–15, and Spectator (AED 35). Items only reach the cart when a quantity is set.
- Before a session is chosen, the ticket panel says *Choose a session above to see its tickets and prices.*

## 4. Swim ability and height gate: the answer changed nothing
- **All of us:** the full ride list at standard prices.
- **Some of us:** the ride notes change, and a *Swim vests needed* counter appears so the vests are ready at the gate.
- **None of us:** the tickets switch to a *splash and river pass* at lower prices (Adult AED 175, Junior AED 135, Child AED 125, Senior AED 135). Slides are removed from the ride notes.
- The "Are you able to swim?" pop-up no longer appears on this flow, because the question is already on the page.

## 5. Transport: route already chosen, but stations were empty
- Each route flow now opens with its stations filled in. For example, *Abu Dhabi – Al Ain · E201* starts from Abu Dhabi Central Bus Station to Al Ain Central Bus Station. Guests can still change or swap them.
- Departures show straight away, with no need to tap Search Trips. The time period buttons now act as a filter; tap one again to show all departures.
- **Passengers only appear after a departure is chosen** (performance first, then tickets).

## 6. Proposed UI: route cards with a Book button
- New flow: **Transport → Popular routes · card view**. It has cards for Dubai to Abu Dhabi, Sharjah to Dubai, Abu Dhabi to Al Ain and Dubai to Fujairah, styled like the dated ticket cards. Each shows the *from* fare and a **Book** button.
- Book → pick the date → departures for that route → passengers.
- On mobile it is the first transport product, *Popular routes*.

## Files
- `TICVAI Guest Booking v2 (single file).html` and `TICVAI Mobile App v4 (single file).html` have been rebuilt with these changes.
- Arabic for the new labels is in `ticvai-ar-29sep.js`.
