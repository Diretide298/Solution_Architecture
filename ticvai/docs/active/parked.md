
## ~~Parked 24 August — deep-link cold entry, 147 screens~~ — DONE the same day

**A screen reachable by deep link that says nothing about arriving cold.** `check-screens` warns on
all 147; none is an error and none blocks.

**Parked deliberately.** The pattern is one decision, not 147: **does a screen arriving cold fetch
its context, or refuse and send the person to a list?** Both are defensible and the answer differs
by audience — a guest opening a ticket from an email should land on the ticket; a cashier opening a
till screen from a notification should not resume a shift they have not signed into.

**Answering it once and applying it is an hour. Answering it 147 times is a week and produces 147
slightly different answers.**

**Unparked and answered 24 August. ADR-0030.**

The reasoning for parking was right — *one decision, not 147* — and the conclusion was wrong.
**It took an hour, not a week**, because the shape depends on audience rather than on the screen:
guest says what happened and offers one way onward, staff resolves or says plainly it is gone,
platform admin refuses outside its tenants, partner refuses outside its own scope, and a version
link opens read-only because **an old version is history, not an error.**

**All 147 written.  at zero on this warning.**
