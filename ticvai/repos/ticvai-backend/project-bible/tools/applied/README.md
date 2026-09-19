# Applied and retired tools

**These have finished their work.** Each ran, wrote what it was written to write, and now reports nothing to do — or has been superseded by something better. They are here rather than deleted because **each one carries the reasoning for a decision that is now baked into the data and recorded nowhere else.**

They remain runnable: `ROOT` is repointed one level up to account for the move. Running one should say *nothing to do*; if it does not, something has regressed and the tool is the record of what it should be.

Retired 10 September 2026.

## `apply-guest-parity.py`

Gave guest mobile the twenty-three operations only guest web could call — including the whole cart-editing surface and `createOrder`, without which the app could start a checkout and never produce an order. Applied 10 September.

## `apply-naming-and-navsets.py`

Collapsed ADM-321 into ADM-241, renamed BO-047 to Order Corrections & Exceptions, and defined the two P04 navigation sets — recording `posPrimaryRail` as unrealised rather than inventing a membership for it. Applied 9 September.

## `apply-p04-machines.py`

Installed the five P04 state machines, three failure states and sixteen overlay confirm/dismiss halves. **Removed from refresh.sh on 10 September because it asserts its own literal content** — it destroyed a hand edit to `payStage` on run 8. Applied.

## `apply-pos-prototype.py`

Took into P04 the five surfaces the POS Terminal prototype has and the package never drew — Till Home, Receipt & Reprint, Guest Lookup, Table Service, Order Queue — plus the device panel on Till Configuration. Not one operation was invented. Applied 10 September.

## `apply-target-apps.py`

Recorded which of the five shipped apps each of the fifteen platforms becomes, tested against operation overlap rather than decided by hand. Applied 10 September.

## `apply-uiux-workshop-decisions.py`

Recorded the UI/UX workshop decisions. Applied; reports every decision already recorded.

## `apply-web-parity.py`

The reverse: thirty-nine operations only mobile could call, including six data-subject rights that a guest without the app could not exercise. Only `enrolFacePass` stayed on the phone. Applied 10 September.

## `build-wireframes.py`

**Superseded by `derive-wireframes.py`, and stale by an order of magnitude.** Its docstring describes a package of 180 screens; there are 1,234. It writes to `ROOT.parent / wireframes`, which is outside the package entirely, and carries three separate cp1252 encoding faults. Retired rather than repaired on 10 September.

## `derive-empty-states.py`

Derived empty states across the package. Reports 0 screens outstanding.

## `derive-pack-boards.py`

Drew each pack screen a second time on its own WS## board. **Superseded 10 September**: 728 screens rendered twice meant a reviewer met two drawings of one screen. The workshop grouping is now a badge and a filter on the platform board. Its 74 files are in `_dump/wireframes-workshop-boards-10-september/`.

## `repoint-archived-boards.py`

Repointed the 133 screens whose drawn frame was archived, keeping in a note which board drew each one. A one-shot repair, never a pipeline step. Applied 10 September.

## `wire-duplicate-merge.py`

Added `matchGuest`, `mergeGuests` and the duplicate-match components to EMP-055 and EMP-057. Applied 10 September, after an idempotency guard was added — it had been appending unconditionally and a second run would have doubled everything.

## `wire-pack-boards.py`

Wired the fourteen September pack board groups, collapsed ANL-011, and gave the 140 unreachable pack screens a hub. Applied.

## `wire-pack-boards-11-september.py`

Wired the 34 boards of the four books in `Latest Docs.zip` — Digital Asset Management, Game & Ride, Rental Management, Subscription Licensing & AI Self-Service — the same hub-and-spoke way, and gave all 340 screens a route `derive-board-flows.py` could read. **A sibling rather than a re-run:** the original groups by `(platform, board)`, which would have merged Game & Ride and Rental board for board on P08, and its collapse path would have promoted a new hub now that `ANL-011` is gone. Applied 11 September.

## `apply-rental-staff-app.py`

Put Rental Management boards 6–8 — checkout, active rentals, returns — on P06 as well as P08, decided 11 September: "they can go to staff app and also in venue management". Thirty screens, `EMP-071`–`EMP-100`, one hub per board off `EMP-003`. Each names its P08 twin in `source.sameAs` instead of `source.pack`, because three tools would do the wrong thing with two claimants of one pack entry. **Unlike the others here it is meant to be re-run**: it re-copies layout, states and gaps from the twin, so after `generate-screens-from-pack.py` touches Rentals, run it again or the handheld drifts from the desk. Offline states are `TODO` on purpose. Applied 11 September.

## `apply-guest-offline-parity.py`

Made guest web and guest app say the same thing when the connection drops, decided 12 September: "make both identical for offline things add a notification banner to go online". **No web screen had an offline state and every app screen had one**, so a web guest who lost signal read *"Could not load"*. Writes one `platform.offlineBanner` onto P01 and P02 and one `states.offline` per capability group from `screens/_guest-pairs.yaml`, word for word on both shells — 117 states and 2 banners on the first run. The web stays `offlineCapable: false`; every text is written to be true on both, and a text that promises continued function is refused. **Like the Rental copier it is meant to be re-run**: `check-screens` fails a group whose members disagree, and a new guest screen in no group. Applied 12 September.

## `apply-subscription-placement.py`

Placed the Subscription book by who works each screen, decided 11 September after reading all 100. **Moved** boards 7 (AI Setup) and 8 (Go-Live) and screen 6.10 from P09 to P08, `ADM-428`–`ADM-448` → `BO-594`–`BO-614`, because they are the new customer's own admin inside their tenant; the old ids are retired and `F213`/`F214` were rewritten in place. **Created P17 TICVAI Sign-up**, a public face of TICVAI Control, with `sameAs` copies of the 24 screens a prospect sees in boards 2, 4 and 5 — P09 keeps all of them for the operator-led sale. Also rewrote the sibling list and note on P09, P10, P11 and P14. **Re-run it after `generate-screens-from-pack.py` touches Tenants & Licensing**, or P17 drifts from its twins. Applied 11 September.
