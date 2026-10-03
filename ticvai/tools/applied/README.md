# Applied and retired tools

**These have finished their work.** Each ran, wrote what it was written to write, and now reports nothing to do — or has been superseded by something better. They are here rather than deleted because **each one carries the reasoning for a decision that is now baked into the data and recorded nowhere else.**

They remain runnable: `ROOT` is repointed one level up to account for the move. Running one should say *nothing to do*; if it does not, something has regressed and the tool is the record of what it should be.

Retired 10 September 2026.

## `apply-guest-parity.py`

Gave guest mobile the twenty-three operations only guest web could call — including the whole cart-editing surface and `createOrder`, without which the app could start a checkout and never produce an order. Applied 10 September.

## `guest-scoping-3-october.py`

Declared how a guest calls the staff-permission operations the guest screens bind, decided 3 October (Chinmay's answers to the Block A audit, "Pattern 4", all as recommended; CHG-GCF-001 to -005). The audit found 184 guest-screen bindings of 49 operations carrying a staff permission with neither `x-ticvai-guest-callable` nor `x-ticvai-self-scoped`. Writes the flag and one description paragraph per operation at its own lines: twenty catalogue reads guest-callable with published data only, fifteen of the guest's own records and the three assistant-conversation operations self-scoped, seven purchase actions guest-callable within the guest's own session, `reprintOrder` self-scoped and kiosk-callable as a device, and a note on `sendConversationMessage` and `listAnalyticsProviders`, which stay staff operations. The new `sendGuestConversationMessage`, `getGuestConversation` and `PublishedTenantConfig.analyticsProviders` were written by hand. `check-audience-match` (AM-GUEST-PERMISSION) fails a guest screen that binds such an operation again. Applied 3 October; a second run says there is nothing to do.

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

## `move-adm049-2-october.py` and `move-adm049-design-notes-2-october.py`

Moved the workshop-pack console screens to Venue Management, decided 2 October (Chinmay, DEC-100: "they are venue screens"; CHG-MOV-001 to -010). **Unlike the subscription placement, the ids are kept**: 25 of these screens already had pushed APP-SETUP tickets, and a pushed key names the screen id, so a renumbering would have made second tickets (check-key-stability). 408 of the 410 moved to the end of P08; ADM-068 and ADM-619 stay on the console because later answers of the same day give them to TICVAI staff (DEC-207, DEC-211). Merged 32 duplicates with the venue's own screens — five as full anchors with no operations (the five that declared exactly a venue screen's operations), twenty-seven as sections that keep the first-release slice's operations until the lead retires the duplicate writers (CHG-MOV-008). Repointed the moved screens' sources in the design notes and the 41 static workshop boards, renamed the flows' platform and the contracts' consumed-by lines, and marked the Block A and B design-note corrections fixed, withdrawn or logged. Applied 2 October; a second run says there is nothing to move.

## `repoint-workshop-board-links-2-october.py`

Re-pointed the static workshop boards' links at the board that now renders each screen (CHG-GTB-009). The approvals, communication and partner move of 2 October (`move-approvals-comms-partner-2-october.py`) moved screens from P09 and P10 to P08 but, unlike the ADM-049 move, left the nine `WS31`-`WS41` boards linking to P09 and P10 — 181 links that `check-wireframes` failed on the r2 full refresh. Looks each linked id up in `screens/P*.yaml` and writes its platform's `wireframeBoard`. **Run it after any move of screens between platforms**; a second run says there is nothing to re-point. Applied 2 October.

## `ai-engine-tasks-3-october.py`

Filled the text of the ten Block A AI engine tasks and DB-ROLES in `docs/active/block-a-extra-tasks.json` (CHG-TBF-006, CHG-TBF-007), decided 3 October (Chinmay, Block A audit business rules: "AI engine tickets: What and done-when filled from docs/architecture/ai-system-design.md and the 2 Oct AI decisions; gaps become questions later"). The audit on live r2 found them a line or two long with no Done-when. Each text comes from the design (sections 3.3 to 3.13, 4.4, 5.8, 7) and the decisions of 2 October: the per-tenant residency class with Core42 Compass the UAE-only default (ADR-0009 amended), the mandatory offline Presidio scrubber and Qwen3Guard guard (ADR-0020 amended), BYOK of any provider (CHG-FUP-008); DB-ROLES from ADR-0055 and ADR-0020. Only `detail` changes; days, owners and dependencies stay as planned, and the engineer-days come before "Done when" because the ticket's done-when line is everything after it. Applied 3 October; a second run says there is nothing to do.
## `spec-screen-patterns-3-october.py`

Fixed the six screen patterns the Block A audit on live r2 found (CHG-AUD-001; Chinmay, 3 October: fix the specs, refresh, cut r1), on every platform, as CHG-SPF-001 to -006: forms stop asking for `readOnly` fields (P1); lists and panels keep the fields the screen is about, at most five on a phone or handheld, and the "Columns are every field" apisNote goes (P2); the no-access state names the read's permission and each action's (P3); a required entry parameter nothing carried becomes optional where the screen lists, reads or makes the id, or comes from the session on a staff screen, or is carried by an inbound edge whose source holds it (P5); the 27 screens merged into a venue screen as sections say so in `implementation.sectionOf`, and the 13 screens wearing another screen's route or component get their own (P7b); every Block A screen is wave 1 and its stale "Wave 2" and "out of the first release" notes read as the history they are (P8). The rules are `tools/screen_patterns.py`, shared with `tools/check-screen-patterns.py` and the generators, so the screens cannot drift back. Screens are spliced back one at a time at the file's own dump width (with anchors expanded where a rewritten screen defined one), so nothing else in a file moves. Applied 3 October; a second run says there is nothing to do.

## `screen-decisions-3-october.py`

Applied Chinmay's 3 October answers that change a screen (CHG-SPF-007 to -013): `listAnalyticsProviders` off GST-001 and WEB-001; KIT-007 a read-only guest board; BO-056 self clock-in only; BO-078 one `approveRequisition` decision (and flows F92 and F15); ANL-023's first Save creates; POS-000's session management behind a supervisor PIN; GST-055's 30-second QR; GST-053's add-on change kinds and signed-out planning; and, by the agreed names of operations other agents add, the guest chat's `sendGuestConversationMessage` with streamed answers, GST-070's own reservations and bookable restaurants, and EMP-026's photos and person involved. `check-screen-patterns` (DEC) keeps each decision made. Applied 3 October; a second run says there is nothing to do.

## `screen-reads-3-october.py`

Gave every Block A screen that shows or edits data a read that returns it (CHG-R1S-004), after the r1 gate of 3 October found ADM-069 editing a tax profile it could not read, POS-024's "86 an item" picker with nothing to list, GST-077 never reading its departure and WEB-033's guest projection without the `variantId` that `addCartLine` needs. Adds 18 reads beside their writes on the writes' own paths (each list ordered and paged), binds them or existing reads on the 41 screens the READ rule of `tools/screen_patterns.py` found, gives each a component that reaches it (a card list where the screen already shows another entity), and makes the three contract facts additive (`GuestMerchandiseItem.variantId`, `GuestMenu`'s tables, POS-024's picker). `check-screen-patterns` (READ) holds Block A at zero and the rest to a falling ceiling. Applied 3 October; a second run says there is nothing to do.

## `lineage-writes-3-october.py`

Every write operation writes a table or says why not, and every event emitter writes `platform.outbox` (CHG-R1S-005), after the HLD/LLD cross-check of 3 October found `createOrder` emitting without the outbox and six POSTs writing nothing. Gives 108 writes their table, marks 48 `pure` with a reason and 7 generated workspace writes `storageUndecided`, and adds the outbox to every emitter outside the AI contract (AI writes only AI stores, ADR-0020; its publish path is an open question). `tools/derive-lineage.py` now adds the outbox for emitters; `tools/check-write-lineage.py` holds the rest. Applied 3 October; a second run says there is nothing to do.

## `problem-types-3-october.py`

Named the problem types of the 28 Sprint 1 error responses whose descriptions already named their causes in backticks (CHG-R1S-021), after the r1 gate could not contract-test errors with no `type`. A backticked property, parameter, operation, status value or single word is not a cause and is skipped; the 71 Sprint 1 responses with no named cause are left on the falling ceiling of `tools/check-problem-types.py`. Applied 3 October.

## `guest-kiosk-3-october.py`

The lead's guest and kiosk design cross-check of 3 October (CHG-R1S-022, CHG-R1S-023): binds what flow steps call (WEB-005 and KSK-015 `addCartLine`, WEB-011 `extendSeatHold`, made guest-callable within the guest's own session, KSK-014 `getTenantAppStatus`, KSK-013 `handoverToAgent`), applies the eleven open kiosk corrections of the process notes and marks them `status: fixed`, and gives `GuestMenu` items `allergenDetail`. Applied 3 October; a second run says there is nothing to do.
