"""The CR watcher sorts a future request of each r10 class into it (CHG-R10GEN-008; handoff/cr-classes.yaml).

    python -m pytest ticvai/tools/tests/test_cr_classes_r10.py -q

Each case is an r10 request's own title and the start of its problem, with every CR id taken out, so the class is
found by its words and artefact alone, as it must be for the next request of the class.
"""
import importlib.util
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("cw", TOOLS / "cr-watch.py")
cw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cw)
CLASSES = cw.load_classes()

CASES = [
    ("CR-236", "list-order", "queue#listMyWaitingGuests",
     "listMyWaitingGuests orders by estimatedCallAt, which is nullable: where an entry with no estimate sorts is not said",
     "listMyWaitingGuests is \"Ordered by estimatedCallAt, soonest first, then joinedAt\", and its keyset cursor (PageCursor) names the last item's position in that order. But WaitingGuest.estimatedCallAt is nullable and queue.entry.estimated_call_at has no NOT NULL, so an entry with no estimate (a queue whose wait time is unavailable) has no place in the order: first, last, or by some other time. The ans"),
    ("CR-206", "list-order", "shift#listShifts",
     "listShifts orders by recordedAt, which is optional on openShift and nullable on orders.pos_shift: where a shift with no recordedAt sorts is not said",
     "listShifts says \"Order. Newest first, by recordedAt descending, then by id\", and its keyset cursor (PageCursor) names the last item's position in that order. But recordedAt is optional: OpenShiftRequest does not require it, Shift.recordedAt is optional (\"When the device recorded the open. openedAt is the server's time.\"), and orders.pos_shift.recorded_at is nullable. So a shift opened online with "),
    ("CR-190", "list-order", "identity#listSsoProviders",
     "listSsoProviders names no filter on identity.sso_provider.is_active and no order, so a sign-in door may offer a switched-off provider and lists them in no stated order",
     "listSsoProviders feeds the SSO buttons on every staff and partner sign-in door (EMP-001, ADM-001, PTR-001, SUP-001; also EMP-042). Two rules the build needs are not stated."),
    ("CR-237", "state-model", "queue#overrideWaitingGuest",
     "overrideWaitingGuest admits a party, but the queue-entry state model makes the override a no-show or a return to the queue, from called only",
     "The operation and the state model describe two different actions. overrideWaitingGuest is \"Admit against a failed redemption\" (late arrival, a phone that died, a system fault), answers \"Admitted and recorded\" with outcome overridden and an admittedCount, and refuses only redeemed, cancelled and released entries - so expired and noShow entries can be overridden. states/queue-entry.yaml gives overrideWaitingGuest exactly two transitions, both from called only: called -> noShow (\"Operator recorded a no-show\") and called -> waiting (\"Returned to the queue\"), and lists redeemed, expired, noShow, cancelled and released as terminal, so nothing moves an expired or noShow entry and override never admits. The build cannot set the entry's status, choose which statuses are allowed, or decide what \"admitted\" records without picking one of the two; and neither says what status an admitted party's entry ends in."),
    ("CR-234", "money-currency", "fnb#mergeTableVisits",
     "mergeTableVisits answers Money it has no declared currency for, and does not say which visit states are closed or whether a self-merge or a cross-outlet merge is allowed",
     "mergeTableVisits answers 200 with a TableVisit, whose runningTotal and every FnbOrder's grossAmount, taxAmount, unitPrice and lineTotal are Money. fnb.table_visit and fnb.service_order(_line) store amounts only; the currency and scale resolve from the venue's frozen trading currency, which is Tenancy's data (platform.venue_settings / platform.region_settings). Tenancy runs in the commerce host and"),
    ("CR-197", "money-currency", "promotions#getGuestBundle",
     "getGuestBundle 404s draft/unpublished/withdrawn bundles, but promotions.bundle stores no such state and nothing publishes one; its venue-currency read is undeclared",
     "getGuestBundle's one rule is that a bundle in draft, unpublished or withdrawn answers 404, and getBundle carries the same rule for guest callers. Nothing records that state for a promotions bundle. promotions.bundle has no status column; createBundle and updateBundle set only is_active (\"whether the bundle is on sale\"); r8 adds variant_id, \"null until published\", but no promotions operation publis"),
    ("CR-217", "money-currency", "catalogue#createEntitlementTemplate",
     "createEntitlementTemplate writes scope_path at venue scope but no declared read gives Catalogue a venue's path; the no-venue caller and includedValue's currency read are undefined too",
     "The operation cannot write its partition key without reading another module's table, and two smaller points are unstated."),
    ("CR-235", "money-currency", "catalogue#setEntitlementTemplateBlackoutDates",
     "setEntitlementTemplateBlackoutDates answers includedValue, but a template keeps only its scope_path and no declared read gives its venue's currency; the audit row's values are unstated",
     "setEntitlementTemplateBlackoutDates is built, but two things it must do are not declared."),
    ("CR-202", "money-currency", "subscription#generateInvoice",
     "generateInvoice cannot price or number an invoice: no billing currency, no tax source, no issue/number rule, dryRun undefined",
     "generateInvoice must return a SubscriptionInvoice whose subtotal, taxAmount, total and line amounts are Money, but nothing in the package says which currency a TICVAI platform invoice is in: control.invoice stores amounts only, and control.plan, control.module_listing, control.tenant and BillingEntity carry no currency; naming-and-style 5.1 resolves currency from a venue or lists the tables that s"),
    ("CR-220", "screen-values", "venue-map#getVisitPlannerOptions",
     "GST-051's lunch and shop questions list the chosen parks' cuisineTags and retailTags, but no operation the screen declares returns them (getVisitPlannerOptions gives interestTags only)",
     "GST-051 Plan asks \"What would you like for lunch?\" with \"cuisines from the dining points of the chosen parks only (VenuePoint.cuisineTags)\", each naming the park(s) that serve it, and \"Any shops you'd like to visit?\" with \"the retailTags of the shops and retail kiosks of the chosen parks\". Its preferenceNotAtVenue state marks a cuisine or shop tag no chosen park can meet before Make my plan, and s"),
    ("CR-221", "screen-values", "catalogue:ProductMedia",
     "A guest screen cannot show a product's photo: ProductMedia carries only an assetId, and every read that turns an asset into a URL is staff-only",
     "Guest listings must show each product's own photo (23SEP-4): WEB-003's result card binds `primaryMedia` and its suggestions bind `Product.media`; WEB-002, WEB-004 and the guest app's listings do the same. But ProductMedia has no URL: assetId, kind, isPrimary, displayOrder, altText. The URL exists only on assets `MediaAsset.url` / `thumbnailUrl`, and the reads that return it (getMediaAsset, listMed"),
    ("CR-233", "screen-values", "WEB-023",
     "WEB-023 offers \"Use another card\" for a declined renewal but does not declare listPaymentTokens, so it has no saved cards to choose from",
     "WEB-023's billing statement offers \"Use another card\" on a soft decline and only that on a hard one (rev 3 DG-2), and its retry modal collects an optional `paymentTokenId` for retryMyDunningPayment (\"on a different saved card if one is given\"; \"a hard decline is never retried on the same card ... the guest must choose another\"). The guest's saved cards come from orders#listPaymentTokens (guest-callable, masked), which WEB-023 does not declare: its apis are getMyMemberships, listBillingStatements, getBillingStatement, listMyPaymentIssues and retryMyDunningPayment. So the screen cannot list the cards the guest would choose between, and a guest with a hard decline has no way forward on this screen. GST-015 (the app's memberships screen, the other consumer of retryMyDunningPayment) has the same need. Not blocking: WEB-023 builds the picker against listPaymentTokens' contract shape, marked provisional until this is settled."),
    ("CR-187", "screen-values", "WEB-007",
     "WEB-007 still binds one holdId and a Cart countdown, while seating.yaml (r8) holds one seat per hold and WEB-007 reads no cart; and maxSeatsPerGuestOrder has no source on this screen",
     "Three places where WEB-007's screen YAML disagrees with the seating contract or lacks a source, all met while building #31848. (1) Hold model. seating.yaml createSeatHold (r8 walk of tickets 28202 and 28197) says \"one hold per tap\", \"the screen keeps the holdId of each\", \"the way on to the basket ... carries the list of holdIds\", and \"a screen opened again with a holdId reads it with getSeatHold\"."),
    ("CR-186", "screen-values", "GST-043",
     "GST-043 says a signed-in guest's language choice is also saved as the profile's language, but declares no operation that writes it (only getPublishedTenantConfig)",
     "GST-043's language selectField says \"the choice is stored on the device and, for a signed-in guest, as the profile's language (GST-039)\". The only operation GST-043 declares is getPublishedTenantConfig, a public read, so as specified the screen cannot save the choice to the profile. The write that exists is marketing-crm#updateMyProfile (PATCH /guests/me/profile, optional preferredLanguage), and o"),
    ("CR-198", "guest-venue", "promotions#getGuestBundle",
     "A visitor's public read (security {}) has no scope, so venue row-level security on promotions.bundle hides every bundle; nothing says how a public guest read gets its venue scope",
     "getGuestBundle (and getBundle for guests) is public: security `{}` or guestAuth, \"a visitor browses before signing in\". promotions.bundle is under venue_isolation row-level security, which shows a row only when the caller's scope paths cover it. A visitor has no session, so the host's tenant context gives an empty scope and every bundle is invisible: the operation can only ever answer 404 to its i"),
    ("CR-189", "scope-authz", "schema:contracts/spine/identity.yaml#Session",
     "Server session seam has only the flattened effectivePermissions and all scope paths, no permissionsByScope, so listPrincipals' and createRole's scope-specific checks cannot be enforced",
     "Two operations make an authorisation decision that depends on where a permission holds, and the build has nothing to make it from."),
    ("CR-218", "read-routes", "shift#listDepositBoxes",
     "listDepositBoxes: openOnly undefined, overDrawerLimit has no reads or running expected cash, and expectedTotal/variance reach the box's own cashier",
     "listDepositBoxes (SHIFT_OPEN, the cashier-level permission; POS-015, POS-018, BO-042) cannot be built from the package without guessing three things that touch every row it returns. (1) openOnly. The operation declares a boolean openOnly but nothing defines it, and its own description says the opposite: \"Every status is returned, ended ones included (closed); a screen that shows only live rows filters on status itself.\" DepositBoxStatus has allocated, open, suspended, closing, closed and reconciled, so \"open only\" could mean status open alone, or every state before closed. (2) overDrawerLimit is \"computed on read from the box's expected cash against tenancy.Workstation.cashDrawerLimit or the venue's cashDrawerLimit\" (CHG-CSP-016). Two parts are missing: listDepositBoxes declares only identity#principalRecords, not tenancy#workstationRecords or tenancy#venueSettingsRecords, which hold those limits (allocateDepositBox and closeDepositBoxes declare them); and while a box is trading nothing holds its expected cash: orders.deposit_box.expected_amount is the close figure (\"expectedTotal\"), filled when the box is counted, and no rule says how the running figure is formed (opening float plus cash taken on the box's shift, less change and withdrawals?). Only at allocation is it the float, which is what #30804 compares. (3) The blind close. Shift.expectedCash and variance are \"null to the shift's own cashier on every read: returned only to a caller holding OVERSHORT_ACCEPT or SHIFT_CLO"),
]


@pytest.mark.parametrize("ref,cls,artefact,title,problem", CASES, ids=[c[0] for c in CASES])
def test_a_future_request_of_the_class_is_sorted_into_it(ref, cls, artefact, title, problem):
    got = cw.classify({"title": title, "problem": problem, "artefact": artefact, "ref": "CR-999"}, CLASSES, {})
    assert got and got[0][1]["id"] == cls, [(s, c["id"]) for s, c, _ in got[:3]]


def test_every_r10_class_carries_its_default_ruling_and_its_check():
    by = {c["id"]: c for c in CLASSES}
    for cid in ("money-currency", "list-order", "state-model", "screen-values", "read-routes", "guest-venue",
                "scope-authz"):
        assert "r10 pattern" in by[cid]["default_ruling"], cid
        assert by[cid]["checks"], cid
