#!/usr/bin/env python3
"""Take staff fields, staff filters, raw request forms and staff operations off the guest screens, and
bind the guest screens to the public reads added on 2 October.

**Decided by Chinmay on 2 October 2026: fix before any Block A ticket starts** (for Friday's release).
The process agents reviewing the guest screens (handoff/design-notes/white-label.yaml,
ticketing-guest.yaml and finance-insights.yaml, written 1 October) found that the guest web (P01), the
guest app (P02) and the kiosk (P05) still carried what the 9 September generator wrote for every screen:
the operation's query parameters as text fields ("Venue id", "Kind", "Is sellable", "Principal id",
"Shift id"), its response as an "Every ..." table with the plumbing columns, a modal collecting the raw
request body behind a button named after the operationId, the staff-scoped list beside the guest one,
and a no-access state naming a staff permission. A designer draws what the screen says. The register is
docs/registers/guest-fix-decisions.md (handoff/guest-fix-decisions.json, GFIX-1 to GFIX-4):

  GFIX-1  the storefront reads its theme before sign-in: `getPublishedTenantConfig` replaces
          `getTenantConfig` on WEB-001, GST-001 and KSK-002.
  GFIX-2  guests read policies, FAQs and pages without a session: `listPublishedPolicies`,
          `listPublishedFaqs` and `listPublishedContentPages` on WEB-045, GST-040, GST-057 and the
          checkout terms (WEB-012, GST-009).
  GFIX-3  staff fields, staff filters, raw tables, raw request forms and staff operations off the guest
          screens named in the notes' corrections; each screen keeps its guest behaviour.
  GFIX-4  no guest screen names a staff permission as its no-access state; help is public.

**The contract half is a root edit made by hand** (contracts/satellite/white-label.yaml, the four
`/storefront/...` reads and their four `Published*` schemas). This script does the screens and the three
flows that named an operation a screen no longer calls (F01, F07 and F75 read the published config; F55
lists the guest's own orders; F57 and F75 resend kiosk tickets with reprintOrder). Corrections in the
notes that are not about staff content (missing frames, navigation gaps, enum contradictions, operations
that do not exist yet) are left for the lead's change requests, as the notes' README says.

Idempotent: every edit finds its component by label and does nothing when it is gone. Written with the
screen files' own dump settings (width 100), so a second run writes nothing.

    python tools/applied/guest-screen-fixes-2-october.py [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FILES = {"P01": ROOT / "screens" / "P01-guest-web-storefront.yaml",
         "P02": ROOT / "screens" / "P02-guest-mobile-app.yaml",
         "P05": ROOT / "screens" / "P05-guest-kiosk.yaml"}
DATE = "2 October 2026"
WHO = "decided by Chinmay, fix before Block A starts"


def prov(ref):
    return f"{WHO}, {DATE} ({ref})"


# **Plumbing and staff fields a guest response never shows.** A column naming one of these is dropped
# from every component of a screen this script touches. Matched on the field, whatever the schema.
STAFF = {
    "id", "scopePath", "principalId", "createdByPrincipalId", "approvedByPrincipalId",
    "publishedByPrincipalId", "issuedByPrincipalId", "setByPrincipalId", "assignedToPrincipalId",
    "productOwnerPrincipalId", "responsibleDepartmentId", "venueId", "subjectId", "tenantId",
    "workstationId", "shiftId", "currencyScale", "totalPriceVariance", "isDraft", "draftVersion",
    "hasUnpublishedChanges", "activeModuleCount", "licensedModuleCount", "activePageCount",
    "recentChanges", "isSellable", "isStockTracked", "lifecycleState", "sku", "barcode", "axisValues",
    "providerReference", "providerId", "token", "consentPurposeId", "engagementScore", "engagementTier",
    "lifetimeValue", "tags", "mergedIntoSubjectId", "guestLinkId", "admissionRulesId",
    "approvalRequestId", "requiresApprovalToCancel", "seatMapId", "templateId", "inventoryItemId",
    "onHand", "requiresSerialNumber", "categoryId", "contentHash", "signatureKeyId", "sizeBytes",
    "staleAfter", "appliedByWorkstations", "publishedBy", "fetchedAt", "isReferenced", "budgetCap",
    "maxRedemptions", "precedence", "stackingGroup", "stackingMode", "credentialRef", "endpoint",
    "vendorName", "vendorSwapTargetDays", "pushLeadMinutes", "accessPointIds", "accessPointId",
    "assetId", "capacityPerCycle", "cycleMinutes", "loadBalanceWithQueueIds", "parentQueueId",
    "notifyBeforeCallMinutes", "inQueueOfferEnabled", "orderLineId", "walletHoldId", "walletId",
    "notificationBranding", "enabledPaymentMethods", "syncedAt", "escalationCount", "isSlaBreached",
    "slaPausedSeconds", "batchId", "campaignId", "assignedSubjectId", "redeemedOrderId",
}
# Fields staff-only on one schema and the guest's business on others.
STAFF_ON = {
    "Product": {"code", "kind", "isActive"},
    "ProductVariant": {"isActive"},
    "MerchandiseItem": {"isActive", "outletId", "variantId"},
    "FxRate": {"purpose", "source", "effectiveTo", "note"},
    "ParkingFacility": {"mode", "capacity", "takesPayment", "isActive"},
    "ContentPage": {"status", "isEnabled"},
    "FaqCategory": {"code"},
    "Queue": {"attractionProductId", "code"},
    "WaitTime": {"queueId", "attractionProductId", "attractionCategoryId", "source"},
    "Performance": {"eventId"},
    "Promotion": {"status", "conditions"},
    "Case": {"priority", "slaDueAt", "queueId", "membershipId", "categoryId", "channel"},
    "Cart": {"conflicts"},
}
# Kept where a staff-looking field is the guest's business: the visit-day banner suggests the ticket's venue.
KEEP = {("Entitlement", "venueId")}

NA_GUEST = ("**There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is "
            "what a staff caller must hold; a guest call resolves to the guest's own data; " + prov("GFIX-4") +
            "). No access here means one of two things, told apart by the response: not signed in, where "
            "the guest is offered sign-in and brought back to this screen, or a record that is not theirs, "
            "which says so without saying whose it is. **Never an empty table** — that reads as *there is "
            "no data* and sends somebody to support with the wrong question.")
NA_PUBLIC = ("**Nothing here needs a sign-in** (" + prov("GFIX-2") + "): the screen reads only what the "
             "tenant has published, which is public, so there is no no-access case. A host that belongs "
             "to no tenant shows the platform's neutral holding page.")
NA_KIOSK = ("**A kiosk holds no permission and needs none** (" + prov("GFIX-4") + "): it sells to whoever "
            "is standing at it, and reads what the tenant has published like any visitor. A kiosk whose "
            "device registration is revoked goes out of service (KSK-014); it never shows a sign-in or "
            "names a permission.")
PERMISSION_STATE = re.compile(r"(Shown when the caller lacks|Sign in to see this)")


class Screen:
    def __init__(self, s, log):
        self.s, self.log = s, log
        self.sid = s["id"]

    # --- components -------------------------------------------------------------------------------
    def comps(self):
        for r in (self.s.get("layout") or {}).get("regions") or []:
            for c in r.get("components") or []:
                yield r, c

    def find(self, label, kind=None, op=None):
        for r, c in self.comps():
            if c.get("label") == label and (kind is None or c.get("kind") == kind) \
                    and (op is None or c.get("operation") == op):
                return r, c
        return None, None

    def drop(self, label, kind=None, op=None, why="GFIX-3"):
        r, c = self.find(label, kind, op)
        if c is None:
            return
        r["components"].remove(c)
        if not r["components"]:
            # A region whose last component went goes with it (the kiosk payment's action bar).
            self.s["layout"]["regions"].remove(r)
        self.log.append(f"{self.sid}: removed {c.get('kind')} '{label}' ({why})")

    def edit(self, which, of_kind=None, op=None, **changes):
        label = which
        r, c = self.find(which, of_kind, op)
        if c is None:
            return None
        for k, v in changes.items():
            if v is None:
                c.pop(k, None)
            else:
                c[k] = v
        self.log.append(f"{self.sid}: changed '{label}' -> {', '.join(changes)}")
        return c

    def add(self, region, comp, after=None):
        regions = (self.s.setdefault("layout", {})).setdefault("regions", [])
        if any(c.get("label") == comp.get("label") and c.get("kind") == comp.get("kind")
               for _, c in self.comps()):
            return
        reg = next((r for r in regions if r.get("name") == region), None)
        if reg is None:
            reg = {"name": region, "components": []}
            regions.append(reg)
        comps = reg.setdefault("components", [])
        idx = len(comps)
        if after:
            for i, c in enumerate(comps):
                if c.get("label") == after:
                    idx = i + 1
        comps.insert(idx, comp)
        self.log.append(f"{self.sid}: added {comp.get('kind')} '{comp.get('label')}'")

    def card(self, label, new_label, columns=None, notes=None, bindsTo=False):
        """A generated "Every ..." table becomes the guest's card list."""
        r, c = self.find(label, "dataTable")
        if c is None:
            return
        c["kind"] = "cardList"
        c["label"] = new_label
        if columns is not None:
            c["columns"] = columns
        if bindsTo is None:
            c.pop("bindsTo", None)
        elif bindsTo:
            c["bindsTo"] = bindsTo
        c["notes"] = (notes + " " if notes else "") + \
            f"Was the generated table '{label}'; staff and plumbing columns removed ({prov('GFIX-3')})."
        c["provenance"] = prov("GFIX-3")
        self.log.append(f"{self.sid}: table '{label}' -> card list '{new_label}'")

    def strip(self):
        n = 0
        for _, c in self.comps():
            cols = c.get("columns")
            if not cols:
                continue
            keep = []
            for col in cols:
                sch, _, fld = str(col).partition(".")
                if (fld in STAFF or fld in STAFF_ON.get(sch, ())) and (sch, fld) not in KEEP:
                    n += 1
                    continue
                keep.append(col)
            if keep:
                c["columns"] = keep
            else:
                c.pop("columns")
        if n:
            self.log.append(f"{self.sid}: {n} staff or plumbing column(s) removed")

    # --- overlays and apis ------------------------------------------------------------------------
    def drop_overlay(self, oid):
        ovs = self.s.get("overlays") or []
        for o in list(ovs):
            if o.get("id") == oid:
                ovs.remove(o)
                self.log.append(f"{self.sid}: removed overlay {oid}")
        if "overlays" in self.s and not self.s["overlays"]:
            self.s.pop("overlays")

    def overlay(self, oid):
        return next((o for o in self.s.get("overlays") or [] if o.get("id") == oid), None)

    def drop_api(self, op, why, source="GFIX-3"):
        apis = self.s.get("apis") or []
        hit = [a for a in apis if a.get("operationId") == op]
        if not hit:
            return
        for a in hit:
            apis.remove(a)
        # What a write refreshed afterwards follows the read that replaced it, or goes.
        declared = {a.get("operationId") for a in apis}
        swap = "listMyOrders" if op == "listOrders" and "listMyOrders" in declared else None
        for a in apis:
            if op in (a.get("invalidates") or []):
                inv = [swap if x == op else x for x in a["invalidates"] if x != op or swap]
                inv = list(dict.fromkeys(inv))
                if inv:
                    a["invalidates"] = inv
                else:
                    a.pop("invalidates")
        gaps = self.s.setdefault("gaps", [])
        if not any(g.get("operation") == op and g.get("removed") for g in gaps):
            gaps.append({"operation": op, "removed": True, "why": why, "source": prov(source)})
        self.log.append(f"{self.sid}: took {op} off the screen")

    def rebind(self, old, new, purpose, source, contract="white-label", schema=None, why=None):
        """Replace one operation by another on the screen, keeping its trigger."""
        apis = self.s.get("apis") or []
        if any(a.get("operationId") == new for a in apis):
            return
        for a in apis:
            if a.get("operationId") == old:
                a["operationId"] = new
                a["contract"] = contract
                a["purpose"] = purpose
                a["provenance"] = prov(source)
        for _, c in self.comps():
            if c.get("operation") == old:
                c["operation"] = new
                c["provenance"] = prov(source)
                if schema and c.get("bindsTo"):
                    c["bindsTo"] = re.sub(r"^" + schema[0] + r"\b", schema[1], c["bindsTo"])
                    if c.get("columns"):
                        c["columns"] = [re.sub(r"^" + schema[0] + r"\.", schema[1] + ".", x)
                                        for x in c["columns"]]
        for o in self.s.get("overlays") or []:
            for k in ("confirm", "dismiss"):
                if isinstance(o.get(k), dict) and o[k].get("operation") == old:
                    o[k]["operation"] = new
        for a in apis:
            if old in (a.get("invalidates") or []):
                a["invalidates"] = list(dict.fromkeys(new if x == old else x for x in a["invalidates"]))
        for tr in (self.s.get("navigation") or {}).get("transitions") or []:
            if tr.get("operation") == old:
                tr["operation"] = new
        gaps = self.s.setdefault("gaps", [])
        if not any(g.get("operation") == old and g.get("removed") for g in gaps):
            gaps.append({"operation": old, "removed": True,
                         "why": why or f"Replaced by `{new}`, the guest read of the same data.",
                         "source": prov(source)})
        self.log.append(f"{self.sid}: {old} -> {new}")

    def add_api(self, op, contract, purpose, trigger, source):
        apis = self.s.setdefault("apis", [])
        if any(a.get("operationId") == op for a in apis):
            return
        apis.append({"operationId": op, "contract": contract, "purpose": purpose, "trigger": trigger,
                     "provenance": prov(source)})
        self.log.append(f"{self.sid}: added {op}")

    def state(self, key, text):
        st = self.s.setdefault("states", {})
        if st.get(key) != text:
            st[key] = text
            self.log.append(f"{self.sid}: state {key} rewritten")


FILTERS = ("textField", "toggle", "selectField", "datePicker", "numberField", "multiSelect", "searchField")


def drop_filters(sc, *labels):
    for lab in labels:
        for kind in FILTERS:
            sc.drop(lab, kind)


PRODUCT_CARD = ["Product.name", "Product.description", "Product.media", "Product.displayTags"]
ORDER_CARD = ["Order.orderNumber", "Order.status", "Order.grossAmount", "Order.currency", "Order.lines",
              "Order.createdAt"]
RESULT_NOTES = ("One card per result: name, summary, photo (`primaryMedia`), from-price (`fromPrice`), sold out "
                "shown rather than hidden (`isAvailable`), and `notBookableLabel` for an info-only product. "
                "`searchCatalogue` answers with no named schema, so the card binds none.")
SESSION_VENUE = ("The venue is the one the guest picked on Home (`venueId` from the session, audit R267), "
                 "never typed.")


# --------------------------------------------------------------------------------------------------
# GFIX-1 and GFIX-2: the public reads
# --------------------------------------------------------------------------------------------------
def published_config(sc, platform):
    sc.rebind("getTenantConfig", "getPublishedTenantConfig",
              "The published brand, theme, fonts, header, footer, navigation, homepage, booking-flow display "
              "settings and languages, read before anyone signs in (GFIX-1)", "GFIX-1",
              schema=("TenantConfig", "PublishedTenantConfig"))


def web001(sc):
    published_config(sc, "P01")
    drop_filters(sc, "Kind", "Is sellable")
    sc.card("Every product", "What's on", PRODUCT_CARD,
            "Guest cards show name, image, from-price, tags and availability only (DI-026). " + SESSION_VENUE)
    sc.drop("The selected product", "detailPanel")
    sc.drop("The tenant config", "detailPanel", why="GFIX-1: a guest reads the configuration to style the "
            "page, never to display it")
    sc.drop("The tenant app status", "detailPanel", why="GFIX-3: the CMS status fields are staff only")
    for _, c in sc.comps():
        if c.get("bindsTo") == "TenantAppStatus.maintenanceMessage" and not c.get("operation"):
            c["operation"] = "getTenantAppStatus"
        if c.get("bindsTo") == "HomepageLayout.sections" and not c.get("operation"):
            c["operation"] = "getPublishedTenantConfig"
            c["notes"] = (c.get("notes") or "") + (" The sections, their order and their styling come from "
                                                   "`getPublishedTenantConfig` `homepage`, read with no "
                                                   "session (GFIX-1).")
    sc.state("emptyNoResults", "Nothing is on sale at this venue today. Said in the tenant's voice, with "
             "**Change venue**; the homepage sections that do not list products stay.")


def gst001(sc):
    published_config(sc, "P02")
    sc.rebind("getGuestProfile", "getMyProfile",
              "The signed-in guest's own name and language for the greeting; the CRM fields stay staff only "
              "(GFIX-3)", "GFIX-3", contract="marketing-crm", schema=("GuestProfileDetail", "GuestProfile"),
              why="Replaced by `getMyProfile`, the guest's own profile; `getGuestProfile` is the staff read by "
                  "subject and returns the CRM fields (engagement score, lifetime value, tags).")
    sc.edit("The guest profile", "detailPanel", label="Your greeting",
            columns=["GuestProfile.displayName", "GuestProfile.preferredLanguage"],
            notes="Only when signed in: the greeting by name. Engagement score, lifetime value and tags are "
                  "staff CRM fields and never reach a guest (MATRIX 19.2.7; " + prov("GFIX-3") + ").")
    drop_filters(sc, "State", "Include shared")
    sc.card("Every entitlement", "Your upcoming tickets",
            ["Entitlement.productId", "Entitlement.validFrom", "Entitlement.validTo", "Entitlement.status",
             "Entitlement.entriesUsed", "Entitlement.entriesAllowed"],
            "Only when signed in: `listMyEntitlements` with `state=upcoming`, fixed by the screen.")
    sc.drop("Every money", "dataTable")
    sc.drop("The selected entitlement", "detailPanel")
    sc.drop("The tenant config", "detailPanel", why="GFIX-1")
    sc.drop("The tenant app status", "detailPanel", why="GFIX-3: the CMS status fields are staff only")
    sc.edit("Hero", "banner", bindsTo="PublishedTenantConfig.homepage")
    sc.edit("Highlights per type", "cardList",
            notes="One or two items per type (`HomepageLayout.sections[].maxItems`, 1-2, set on CMS-007); a "
                  "highlight opens Item Detail.")
    # searchCatalogue now fills the search entry rather than a raw table.
    sc.add("contentBody", {"kind": "searchField", "label": "Search the venue", "operation": "searchCatalogue",
                           "notes": "Opens Explore search (GST-063) with what was typed.",
                           "provenance": prov("GFIX-3")}, after="Sold out or closed today")
    sc.state("emptyNoResults", "Nothing is on sale at this venue today. Said in the tenant's voice, with "
             "**Change venue**; the venue overview and the type tiles stay.")


def ksk002(sc):
    sc.rebind("getTenantConfig", "getPublishedTenantConfig",
              "The published languages and branding the kiosk renders in, cached for offline (GFIX-1)",
              "GFIX-1")
    sc.drop("The tenant config", "detailPanel", why="GFIX-1")
    sc.drop("The tenant app status", "detailPanel", why="GFIX-3: the CMS status fields are staff only")
    sc.add("contentBody", {"kind": "selectField", "label": "Choose your language",
                           "bindsTo": "PublishedTenantConfig.languages", "operation": "getPublishedTenantConfig",
                           "notes": "One large button per published language (`languages`), each in its own "
                                    "script; the right-to-left ones lay the kiosk out right to left. From the "
                                    "cached configuration when the kiosk is offline.",
                           "provenance": prov("GFIX-1")})
    sc.add("contentBody", {"kind": "banner", "label": "Closed for maintenance",
                           "bindsTo": "TenantAppStatus.maintenanceMessage", "operation": "getTenantAppStatus",
                           "notes": "Only when `isInMaintenance`: the tenant's message and expected-back time, "
                                    "and nothing can be bought.",
                           "provenance": prov("GFIX-1")})
    sc.state("offline", "**From the cached configuration.** The languages the kiosk last read stay on "
             "screen; buying waits for the connection.")


def help_web(sc):
    sc.rebind("listFaqs", "listPublishedFaqs", "The published FAQs, readable before sign-in (GFIX-2)", "GFIX-2",
              schema=("FaqCategory", "PublishedFaqCategory"))
    sc.rebind("listContentPages", "listPublishedContentPages",
              "The live help and accessibility pages, readable before sign-in (GFIX-2)", "GFIX-2",
              schema=("ContentPage", "PublishedContentPage"))
    sc.add_api("listPublishedPolicies", "white-label",
               "Terms, privacy, refund, cookie and accessibility policies, readable before sign-in (GFIX-2)",
               "onLoad", "GFIX-2")


def web045(sc):
    help_web(sc)
    sc.card("Every faq category", "Questions and answers",
            ["PublishedFaqCategory.name", "PublishedFaqCategory.entries"],
            "Categories in their order, each opening to its questions.", bindsTo="PublishedFaqCategory")
    sc.card("Every content page", "Help and accessibility pages",
            ["PublishedContentPage.title", "PublishedContentPage.iconAssetRef"],
            "The accessibility statement is the page in the `accessibility` category.",
            bindsTo="PublishedContentPage")
    sc.drop("The selected faq category", "detailPanel")
    sc.add("contentBody", {"kind": "cardList", "label": "Policies", "bindsTo": "PublishedPolicy",
                           "columns": ["PublishedPolicy.title", "PublishedPolicy.version",
                                       "PublishedPolicy.effectiveFrom"],
                           "operation": "listPublishedPolicies",
                           "notes": "The current terms, privacy, refund, cookie and accessibility policies; a "
                                    "card opens the policy's `body` in the guest's language.",
                           "provenance": prov("GFIX-2")}, after="Help and accessibility pages")
    sc.state("emptyNoAccess", NA_PUBLIC)
    sc.state("emptyNoResults", "No question or page matches what was typed; the categories stay. Names the "
             "search and offers to clear it.")


def gst040(sc):
    help_web(sc)
    for lab in ("Faqs", "Content pages", "My cases"):
        sc.drop(lab, "metricTile", why="GFIX-3: counts mean nothing to a guest")
    sc.card("Every faq category", "Questions and answers",
            ["PublishedFaqCategory.name", "PublishedFaqCategory.entries"],
            "Categories in their order, each opening to its questions.", bindsTo="PublishedFaqCategory")
    sc.add("contentBody", {"kind": "cardList", "label": "Help pages", "bindsTo": "PublishedContentPage",
                           "columns": ["PublishedContentPage.title", "PublishedContentPage.iconAssetRef"],
                           "operation": "listPublishedContentPages",
                           "notes": "The live help pages; the accessibility ones open GST-057.",
                           "provenance": prov("GFIX-2")}, after="Questions and answers")
    sc.add("contentBody", {"kind": "cardList", "label": "Policies", "bindsTo": "PublishedPolicy",
                           "columns": ["PublishedPolicy.title", "PublishedPolicy.version",
                                       "PublishedPolicy.effectiveFrom"],
                           "operation": "listPublishedPolicies",
                           "notes": "The current terms, privacy, refund, cookie and accessibility policies.",
                           "provenance": prov("GFIX-2")}, after="Help pages")
    sc.add("contentBody", {"kind": "cardList", "label": "My cases", "bindsTo": "Case",
                           "columns": ["Case.caseNumber", "Case.subject", "Case.status", "Case.recordedAt"],
                           "operation": "listMyCases",
                           "notes": "Only when signed in: the cases this guest raised, newest first.",
                           "provenance": prov("GFIX-3")}, after="Policies")
    # Raising or replying to a case refreshes the guest's cases, not the FAQs (the generator's guess).
    for a in sc.s.get("apis") or []:
        if a.get("operationId") in ("raiseMyCase", "replyToMyCase") and a.get("invalidates"):
            a["invalidates"] = ["listMyCases"]
    sc.state("emptyNoResults", "Never shown: `listPublishedFaqs` takes no filter, so an empty list is always "
             "the first-run state above.")
    sc.state("emptyNoAccess", "Reading help needs no sign-in (" + prov("GFIX-2") + "). **Raising or reading a "
             "case needs a signed-in guest**: one who is not signed in is offered sign-in and brought back to "
             "this screen; the questions, pages and policies stay readable.")
    sc.state("loading", "Questions, pages and policies load in place; each list loads on its own.")


def gst057(sc):
    sc.rebind("listContentPages", "listPublishedContentPages",
              "The live accessibility pages (`categoryCode` fixed by the screen), readable before sign-in "
              "(GFIX-2)", "GFIX-2", schema=("ContentPage", "PublishedContentPage"))
    drop_filters(sc, "Status", "Category code", "Slug")
    sc.card("Every content page", "Accessibility pages",
            ["PublishedContentPage.title", "PublishedContentPage.iconAssetRef"],
            "The live pages in the `accessibility` category, a value the screen sends and the guest never "
            "types.", bindsTo="PublishedContentPage")
    sc.edit("The selected content page", "detailPanel", label="The page",
            columns=["PublishedContentPage.title", "PublishedContentPage.body"])
    sc.state("emptyNoAccess", NA_PUBLIC)
    sc.state("emptyNoResults", "Never shown: the screen sends no filter a guest chose, so an empty list is "
             "the first-run state above.")


# --------------------------------------------------------------------------------------------------
# GFIX-3: product listings, search and the item page
# --------------------------------------------------------------------------------------------------
def listing(sc, results_label="Results"):
    drop_filters(sc, "Venue id", "Kind", "Is sellable")
    has_cards = any(c.get("bindsTo") == "Product[]" for _, c in sc.comps())
    if has_cards:
        sc.drop("Every product", "dataTable")
        for _, c in sc.comps():
            if c.get("bindsTo") == "Product[]" and not c.get("operation"):
                c["operation"] = "listProducts"
    else:
        sc.card("Every product", results_label, PRODUCT_CARD, SESSION_VENUE)
    sc.drop("The selected product", "detailPanel")


def web002(sc):
    listing(sc)
    sc.drop("Every performance", "dataTable")
    sc.edit("Date", "datePicker", operation="listPerformances",
            notes="Picks a day; the listing keeps the events with a performance that day (`listPerformances`).")
    sc.drop("Every money", "dataTable")
    sc.edit("Search events and attractions", "searchField", operation="searchCatalogue")
    sc.state("emptyNoResults", "Nothing matches the search, category or date picked, and the other events are "
             "still there. Names what was picked and offers to clear it.")


def search_screen(sc):
    drop_filters(sc, "Venue id")
    sc.edit("Q", "searchField", label="Search")
    sc.card("Every money", "Results", None, RESULT_NOTES, bindsTo=None)
    for _, c in sc.comps():
        if c.get("label") == "Results":
            c.pop("columns", None)
    sc.drop("The selected money", "detailPanel")
    # listProducts stays: before a search it suggests what is on sale, and a suggestion opens WEB-004 with
    # its productId.
    sc.card("Every product", "Suggestions", PRODUCT_CARD,
            "Before the guest types: what is on sale at the venue. " + SESSION_VENUE)
    sc.state("emptyNoResults", "Nothing matches what was typed. Names the search, suggests a shorter one and "
             "offers to clear it; a sold-out match is shown as sold out, not hidden.")


def item_page(sc):
    drop_filters(sc, "From", "To")
    sc.drop("Every performance", "dataTable")
    sc.state("emptyNoResults", "No performance in the next days shown; the strip says so and offers the "
             "calendar.")


def gst003(sc):
    listing(sc, "Tickets and passes")
    sc.drop("Every performance", "dataTable")
    sc.drop("Every money", "dataTable")
    sc.add("contentBody", {"kind": "searchField", "label": "Search tickets", "operation": "searchCatalogue",
                           "notes": "Finds a ticket by name among what is on sale.",
                           "provenance": prov("GFIX-3")})
    sc.add("contentBody", {"kind": "cardList", "label": "Next times", "operation": "listPerformances",
                           "bindsTo": "Performance", "columns": ["Performance.startsAt", "Performance.language"],
                           "notes": "The next times of a dated event, on its card.",
                           "provenance": prov("GFIX-3")})
    sc.state("emptyNoResults", "Nothing matches what was typed or picked; the other tickets are still there. "
             "Names it and offers to clear it.")


def gst002(sc):
    listing(sc, "Things to do")
    sc.state("emptyNoResults", "Nothing in the category picked; the other categories are still there.")


def gst021(sc):
    drop_filters(sc, "Venue id", "Kind", "Is sellable")
    sc.card("Every product", "Points on the map", ["Product.name", "Product.media", "Product.displayTags"],
            "Pins by point category (rides, dining, shows); a pin opens Item Detail. " + SESSION_VENUE)
    sc.drop("The selected product", "detailPanel")
    sc.state("emptyNoResults", "No point of that category on this map; the other categories stay.")


def gst038(sc):
    drop_filters(sc, "Venue id", "Kind", "Is sellable")
    sc.card("Every product", "Around you now", ["Product.name", "Product.media", "Product.displayTags"],
            "What is on at the venue under the chosen tab (map, waits, food, shows, shop, services). "
            + SESSION_VENUE)
    sc.drop("The selected product", "detailPanel")
    sc.drop("The tenant app status", "detailPanel", why="GFIX-3: the CMS status fields are staff only")
    sc.add("contentBody", {"kind": "banner", "label": "Closed or sold out today",
                           "bindsTo": "TenantAppStatus.availabilityMessage", "operation": "getTenantAppStatus",
                           "notes": "From `availability` and `availabilityMessage`; nothing shows while open.",
                           "provenance": prov("GFIX-3")})
    sc.state("emptyNoResults", "Nothing under the chosen tab right now; the other tabs stay.")


def cabana(sc, label):
    drop_filters(sc, "Venue id", "Kind", "Is sellable")
    sc.card("Every product", label, ["Product.name", "Product.description", "Product.media"],
            "The venue's cabanas and other bookable spaces. " + SESSION_VENUE)
    sc.state("emptyNoResults", "Nothing free on the date picked; offers the next free date.")


def ksk003(sc):
    listing(sc, "What would you like?")
    sc.state("emptyNoResults", "Never shown: the kiosk sends no filter a guest chose; the venue is the kiosk's.")


# --------------------------------------------------------------------------------------------------
# GFIX-3: booking steps, basket and payment
# --------------------------------------------------------------------------------------------------
def promo_banner(sc):
    sc.drop("Evaluate promotions")
    sc.drop_overlay("formEvaluatePromotions")
    for _, c in sc.comps():
        if c.get("bindsTo") == "PromotionEvaluation.rejected" and not c.get("operation"):
            c["operation"] = "evaluatePromotions"
            c["notes"] = (c.get("notes") or "") + (" Promotions are evaluated by themselves on every change "
                                                   "(`evaluatePromotions`); a guest never fills a promotions "
                                                   "form (F01 step 4, GFIX-3).")


def web005(sc):
    promo_banner(sc)
    sc.drop("Every product variant", "dataTable")
    sc.drop("The selected product variant", "detailPanel")
    for _, c in sc.comps():
        if c.get("bindsTo") == "ProductVariant[]" and not c.get("operation"):
            c["operation"] = "listProductVariants"


def eligibility_panel(sc):
    sc.drop("Check booking eligibility")
    o = sc.overlay("formCheckBookingEligibility")
    if o is not None:
        o["id"] = "eligibilityDeclaration"
        o["component"] = "drawer"
        o["trigger"] = "Once, on leaving selection, when a chosen product has an eligibility rule"
        o["body"] = ("**The party's age and height, asked once per person** (DI-1037; REV3 DG-3) for the "
                     "products that set a rule, then checked with `checkBookingEligibility`. A person who does "
                     "not meet a rule is named with the product, and the guest changes the selection; never a "
                     "button, and never a form of product ids.")
        o["confirm"] = {"label": "Continue", "operation": "checkBookingEligibility"}
        o["dismiss"] = {"label": "Back", "discards": ["party"]}
        o.pop("bindsTo", None)
        o["provenance"] = prov("GFIX-3")
        sc.log.append(f"{sc.sid}: eligibility form -> once-asked declaration")


def web006(sc):
    sc.drop("Acquire inventory hold")
    sc.drop_overlay("formAcquireInventoryHold")
    sc.edit("Continue", "primaryButton", operation="addCartLine",
            notes="Adds the chosen time and quantities to the cart (`addCartLine`), which takes the hold "
                  "server-side; the guest never sees the word hold or a form. Choosing a session adds nothing "
                  "by itself (DI-1107).", provenance=prov("GFIX-3"))
    eligibility_panel(sc)


def gst007(sc):
    drop_filters(sc, "From", "To")
    sc.drop("Every performance", "dataTable")
    eligibility_panel(sc)
    sc.state("emptyNoResults", "No time matches the part of the day or the language picked, and the other "
             "times are still there. Names the filter and offers to clear it.")


def seat_step(sc):
    sc.drop("Create seat hold")
    sc.drop_overlay("formCreateSeatHold")
    seat = sc.find("Choose seats", "seatMap")[1] or {}
    if "A tap on a seat is the hold" not in str(seat.get("notes") or ""):
        sc.edit("Choose seats", "seatMap", operation="createSeatHold",
                notes=(seat.get("notes") or "") +
                " **A tap on a seat is the hold** (`createSeatHold`); its length is the server's default and "
                "never a guest input (GFIX-3).")
    o = sc.overlay("formRecommendSeats")
    if o is not None:
        o["body"] = ("**How many seats, and best available or together.** The party size is the tickets "
                     "already chosen; the guest only picks the preference, then `recommendSeats` places them.")
        o["provenance"] = prov("GFIX-3")


def web010(sc):
    sc.drop("Add cart line")
    sc.drop_overlay("formAddCartLine")
    sc.drop("Create cart")
    sc.drop_overlay("formCreateCart")
    # createCart stays on the cart, its only caller, but as the runtime's call, never a button.
    for a in sc.s.get("apis") or []:
        if a.get("operationId") == "createCart" and "(GFIX-3)" not in str(a.get("purpose") or ""):
            a["trigger"] = "background"
            a["purpose"] = ("Started by the runtime the first time a line is added, against the guest or the "
                            "anonymous cart token (2.1.31); never a button or a form (GFIX-3).")
            a["provenance"] = prov("GFIX-3")
    promo_banner(sc)
    sc.drop("Checkout cart")
    sc.drop_overlay("formCheckoutCart")
    sc.edit("Checkout", "primaryButton", operation="checkoutCart",
            notes="Checks the cart out (`checkoutCart`) and moves on to the guest details.",
            provenance=prov("GFIX-3"))
    cart_actions(sc)
    # addCartLine stays: F55 adds an add-on from the basket's suggestions.
    sc.add("contentBody", {"kind": "cardList", "label": "Add to your visit", "operation": "addCartLine",
                           "notes": "The add-ons the booking flow suggests for what is in the cart; Add puts one "
                                    "in (`addCartLine`).", "provenance": prov("GFIX-3")})


def cart_actions(sc):
    sc.drop("Save cart line")
    sc.drop_overlay("formUpdateCartLine")
    sc.add("contentBody", {"kind": "numberField", "label": "Quantity", "operation": "updateCartLine",
                           "notes": "A stepper on each line; each change saves at once (`updateCartLine`).",
                           "provenance": prov("GFIX-3")})
    sc.edit("Remove cart line", "destructiveButton", label="Remove")
    sc.edit("Extend cart", "secondaryButton", label="More time",
            notes="Beside the countdown (`Cart.expiresAt`, the one clock the guest sees); `extendCart` up to "
                  "`maxExtensions` times.")
    sc.edit("Abandon cart", "destructiveButton", label="Empty cart")
    for o in sc.s.get("overlays") or []:
        if o.get("trigger") == "Remove cart line":
            o["trigger"] = "Remove"
        if o.get("trigger") == "Abandon cart":
            o["trigger"] = "Empty cart"


def gst041(sc):
    sc.drop("Every product variant", "dataTable")
    sc.drop("Checkout cart")
    sc.drop_overlay("formCheckoutCart")
    sc.add("actionBar", {"kind": "primaryButton", "label": "Checkout", "operation": "checkoutCart",
                         "notes": "Checks the cart out (`checkoutCart`) and moves on to Review & Payment.",
                         "provenance": prov("GFIX-3")})
    cart_actions(sc)
    sc.edit("Visit date per line", "cardList", notes="Each line: the variant's name (`listProductVariants`), "
            "its visit date (`Performance.startsAt`, the match date for a fixture), quantity and price.")
    sc.add("contentBody", {"kind": "cardList", "label": "Lines", "operation": "listProductVariants",
                           "notes": "One row per line with the variant's guest name and a stepper; inactive "
                                    "variants are never shown.", "provenance": prov("GFIX-3")})
    sc.state("emptyNoResults", "Never shown: the basket has no filter; an empty basket is the first-run state.")


def terms(sc):
    sc.add_api("listPublishedPolicies", "white-label",
               "The current terms and conditions the guest ticks, with their version, readable before sign-in "
               "(GFIX-2)", "onLoad", "GFIX-2")
    sc.add("contentBody", {"kind": "detailPanel", "label": "Read the terms", "bindsTo": "PublishedPolicy",
                           "columns": ["PublishedPolicy.title", "PublishedPolicy.version",
                                       "PublishedPolicy.body"],
                           "operation": "listPublishedPolicies",
                           "notes": "`kind=termsAndConditions`, opened from the T&Cs tick; the version shown is "
                                    "the version the consent records.", "provenance": prov("GFIX-2")},
           after="Terms and conditions")


def web012(sc):
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "Transfers happen after purchase from the tickets (WEB-030); on the "
                "payment screen it offered to give away tickets not yet paid for (F55 step 4).")
    for lab in ("Create order", "Create payment", "Inquire payment status"):
        sc.drop(lab)
    sc.drop_overlay("formCreateOrder")
    sc.drop_overlay("formCreatePayment")
    sc.edit("Pay now", "primaryButton", operation="createPayment",
            notes="One Pay: creates the order (`createOrder`, with the T&Cs tick and the opt-in above) and then "
                  "the payment (`createPayment`) for card, Apple Pay, Google Pay or wallet (R080).",
            provenance=prov("GFIX-3"))
    sc.add("contentBody", {"kind": "banner", "label": "Checking your payment", "operation": "inquirePaymentStatus",
                           "notes": "Only in the unknown-outcome state: the screen asks the provider by itself "
                                    "(`inquirePaymentStatus`) and never offers to pay again.",
                           "provenance": prov("GFIX-3")})
    sc.strip()
    terms(sc)


def gst009(sc):
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "Transfer does not belong on a payment screen; it is GST-014's, after "
                "purchase.")
    for lab in ("Create payment", "Inquire payment status", "Checkout cart", "Acquire inventory hold",
                "Create order", "Pay by link"):
        sc.drop(lab)
    for oid in ("formAcquireInventoryHold", "formCreateOrder", "formPayByLink", "formCreatePayment",
                "formCheckoutCart"):
        sc.drop_overlay(oid)
    sc.drop_api("addCartLine", "The hold was taken when the lines were added on the booking steps; nothing is "
                "added on the payment step.")
    sc.add("actionBar", {"kind": "primaryButton", "label": "Pay", "operation": "createPayment",
                         "notes": "One Pay: checks the cart out (`checkoutCart`, with the T&Cs tick and the "
                                  "opt-in), creates the order (`createOrder`) and takes the payment "
                                  "(`createPayment`). The provider token comes from the gateway, never a form.",
                         "provenance": prov("GFIX-3")})
    sc.add("contentBody", {"kind": "banner", "label": "Order", "operation": "createOrder",
                           "notes": "The order number once `createOrder` has answered, shown above the payment.",
                           "provenance": prov("GFIX-3")})
    sc.add("contentBody", {"kind": "banner", "label": "Checking your payment", "operation": "inquirePaymentStatus",
                           "notes": "Only in the unknown-outcome state: the app asks the provider by itself "
                                    "(`inquirePaymentStatus`) and never offers to pay again.",
                           "provenance": prov("GFIX-3")})
    sc.add("contentBody", {"kind": "banner", "label": "Paying a link someone sent you", "operation": "payByLink",
                           "notes": "Only when the app was opened from a payment link (`getPaymentLink`): Pay "
                                    "settles the link (`payByLink`) instead of a cart.",
                           "provenance": prov("GFIX-3")})
    terms(sc)


def web014(sc):
    sc.drop("Pay by link", "primaryButton")
    sc.drop_overlay("formPayByLink")
    sc.edit("Pay now", "primaryButton", operation="payByLink",
            notes="One Pay: the gateway's card form produces the provider token and `payByLink` settles the "
                  "link; the token is never a field (GFIX-3).", provenance=prov("GFIX-3"))
    # The guest reads the link's guest view (`getPaymentLink` returns PaymentLinkView), never the staff record.
    for _, c in sc.comps():
        if c.get("bindsTo") == "PaymentLink":
            c["bindsTo"] = "PaymentLinkView"
            c["columns"] = ["PaymentLinkView.status", "PaymentLinkView.expiresAt",
                            "PaymentLinkView.releaseHoldOnExpiry"] if c.get("operation") else c.get("columns")
            if not c["columns"]:
                c.pop("columns")

def confirmation(sc):
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "The tickets are the primary action here (wallet, resend); transfer is "
                "WEB-030's, opened from My Tickets.")
    sc.edit("Reprint order", "secondaryButton", label="Resend my tickets")
    sc.add("actionBar", {"kind": "secondaryButton", "label": "Transfer tickets",
                         "notes": "Opens Ticket Transfer (WEB-030 on the web, GST-014 in the app), after the tickets.",
                         "provenance": prov("GFIX-3")})
    sc.drop("Resend confirmation", "secondaryButton")
    o = sc.overlay("formReprintOrder")
    if o is not None:
        o["trigger"] = "Resend my tickets"
        o["body"] = ("**Where to send them**: email or SMS to the contact on the order, or another address the "
                     "guest types. `reprintOrder` with `delivery` email or sms; nothing else is asked.")
        o["confirm"] = {"label": "Send", "operation": "reprintOrder"}
        o["provenance"] = prov("GFIX-3")


# --------------------------------------------------------------------------------------------------
# GFIX-3: orders, transfers, memberships, account
# --------------------------------------------------------------------------------------------------
STAFF_ORDER_FILTERS = ("Venue id", "Principal id", "Shift id", "Status", "Created from", "Created to")


def my_orders(sc, table_label="Your orders"):
    drop_filters(sc, *STAFF_ORDER_FILTERS)
    sc.drop("The selected order", "detailPanel", op="listOrders")
    why = ("The staff-scoped order list; a guest screen lists the caller's own orders with `listMyOrders` "
           "(removed from guest screens on 24 August, back with the 31 August parity pass).")
    if any(a.get("operationId") == "listMyOrders" for a in sc.s.get("apis") or []):
        # The staff-scoped list goes; the caller-scoped one stays (WEB-019 notes, 24 August).
        sc.drop("Every order", "dataTable", op="listOrders")
        sc.drop_api("listOrders", why)
    else:
        sc.rebind("listOrders", "listMyOrders", "The orders this guest placed", "GFIX-3", contract="orders",
                  schema=("OrderSummary", "Order"), why=why)
    sc.card("Every order", table_label, ORDER_CARD)


def web019(sc):
    my_orders(sc)
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "Transfer is WEB-030's; order history views, downloads and refunds.")
    sc.edit("Create refund request", "secondaryButton", label="Ask for a refund")
    o = sc.overlay("formCreateRefundRequest")
    if o is not None:
        o["trigger"] = "Ask for a refund"


def gst019(sc):
    my_orders(sc)
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "Transfer is GST-014's; order history views and downloads.")
    sc.edit("The order", "detailPanel", notes="The selected order: lines, totals, payments and status.")


def transfer_screen(sc):
    my_orders(sc, "Your orders with tickets")
    sc.drop("Claim ticket transfer")
    sc.drop_overlay("formClaimTicketTransfer")
    o = sc.overlay("formTransferOrderTickets")
    if o is not None:
        o["body"] = ("**Pick the tickets on their cards, then the friend**: a channel (email, SMS or WhatsApp) and "
                     "the address, with an optional message. `transferOrderTickets` moves ownership; the "
                     "recipient claims from the link they receive.")
        o["provenance"] = prov("GFIX-3")
    sc.edit("Transfer order tickets", "primaryButton", label="Transfer tickets")
    if o is not None:
        o["trigger"] = "Transfer tickets"
        if isinstance(o.get("confirm"), dict):
            o["confirm"]["label"] = "Transfer tickets"


def web030(sc):
    transfer_screen(sc)
    sc.drop_api("claimTicketTransfer", "The recipient claims from the link (GST-014 or a claim landing); the "
                "token is never typed on the sender's screen.")


def gst014(sc):
    transfer_screen(sc)
    # The recipient side stays on the app, but from the link, never a typed token (F55 step 5).
    sc.add("contentBody", {"kind": "banner", "label": "Tickets sent to you", "operation": "claimTicketTransfer",
                           "notes": "When the app is opened from a transfer link: Accept claims the tickets "
                                    "(`claimTicketTransfer`) with the link's token; nothing is typed.",
                           "provenance": prov("GFIX-3")})


def gst018(sc):
    drop_filters(sc, *STAFF_ORDER_FILTERS)
    sc.drop("Every order", "dataTable", op="listOrders")
    sc.drop("The selected order", "detailPanel", op="listOrders")
    sc.drop_api("listOrders", "The staff-scoped order list; the screen opens on one order (`getOrder`), not a "
                "list.")
    o = sc.overlay("formSetVisitReminder")
    if o is not None:
        o["body"] = ("**On or off, how long before, and by which channels.** `setVisitReminder` for this order; "
                     "the reminder's id and the guest are the server's.")
        o["provenance"] = prov("GFIX-3")
        if isinstance(o.get("dismiss"), dict):
            o["dismiss"]["discards"] = ["enabled", "leadTimeMinutes", "channels"]


def memberships(sc):
    drop_filters(sc, "Venue id", "Kind", "Is sellable")
    sc.drop("Every guest membership", "dataTable")
    sc.drop("Every membership", "dataTable")
    sc.drop_api("listGuestMemberships", "The staff-shaped membership list; the guest's own are "
                "`getMyMemberships`.")
    sc.edit("The guest membership", "detailPanel", label="Your membership")


def web022(sc):
    memberships(sc)
    sc.card("Every product", "Membership plans", ["Product.name", "Product.description", "Product.media"],
            "Membership products only, for the guest's venue. " + SESSION_VENUE)
    sc.edit("The selected product", "detailPanel", label="The plan")
    sc.state("emptyNoResults", "Never shown: the plans are the venue's membership products, with no filter "
             "a guest sets.")


def web023(sc):
    memberships(sc)
    sc.drop("Transfer order tickets")
    sc.drop_overlay("formTransferOrderTickets")
    sc.drop_api("transferOrderTickets", "No use on Membership Management; moving a membership to a family "
                "member is a different operation.")
    sc.edit("Retry my dunning payment", "secondaryButton", label="Retry the payment")
    o = sc.overlay("formRetryMyDunningPayment")
    if o is not None:
        o["trigger"] = "Retry the payment"
    sc.card("Every billing statement", "Statements", None)
    sc.card("Every dunning case", "Payments that need you", None)


def gst015(sc):
    memberships(sc)
    # listProducts stays (F19 step 1: where the pass is valid), as the plans, not a raw table.
    sc.card("Every product", "Membership plans", ["Product.name", "Product.description", "Product.media"],
            "The venue's membership plans, to join or upgrade. " + SESSION_VENUE)
    sc.card("Every memberships", "Family and who may use it", None)
    sc.card("Every billing statement", "Statements", None)
    sc.card("Every dunning case", "Payments that need you", None)
    sc.edit("Grant delegation", "primaryButton", label="Let a family member use it")
    sc.edit("Retry my dunning payment", "secondaryButton", label="Retry the payment")
    o = sc.overlay("formGrantDelegation")
    if o is not None:
        o["trigger"] = "Let a family member use it"
        o["body"] = ("**Pick the family member, then what they may do, in plain words** (book with it, enter "
                     "with it, see the bills), and how many times. `grantDelegation` with the person and the "
                     "permission the choice stands for; no subject id, delegation kind or permission key is "
                     "shown.")
        o["provenance"] = prov("GFIX-3")
        if isinstance(o.get("confirm"), dict):
            o["confirm"]["label"] = "Allow"
    o = sc.overlay("formRetryMyDunningPayment")
    if o is not None:
        o["trigger"] = "Retry the payment"


def reservations(sc):
    drop_filters(sc, "Status", "Expiring within minutes")
    sc.card("Every reservation", "Your reservations", None,
            "Upcoming and Past, as two tabs; each card shows when it expires.")
    sc.state("emptyNoResults", "Never shown as a filter result: an empty tab says there is nothing upcoming "
             "(or past) and offers to book.")


def web031(sc):
    sc.card("Every reservations", "Your reservations", None)
    sc.card("Every group package definition", "Group packages", None,
            "School trips, parties and corporate days, as cards.")
    sc.edit("Save table reservation", "secondaryButton", label="Change reservation")
    o = sc.overlay("formUpdateTableReservation")
    if o is not None:
        o["trigger"] = "Change reservation"
        o["body"] = ("**Party size and time, or cancel.** `updateTableReservation` with what the guest changed; "
                     "the outlet, tables, status and visit are the venue's and never shown.")
        o["confirm"] = {"label": "Save", "operation": "updateTableReservation"}
        o["dismiss"] = {"label": "Cancel", "discards": ["partySize", "startsAt"]}
        o["provenance"] = prov("GFIX-3")


def offers(sc):
    drop_filters(sc, "Venue id", "Status", "Active at")
    sc.card("Every promotion", "Offers", None, "The offers active now at the guest's venue. " + SESSION_VENUE)
    sc.state("emptyNoResults", "Never shown as a filter result: no offer is active at this venue now, said "
             "plainly.")


def fx(sc):
    drop_filters(sc, "Venue", "As at", "Purpose")
    sc.card("Every FX rate", "Currencies", ["FxRate.toCurrency", "FxRate.rate", "FxRate.effectiveFrom"],
            "Fixed by the screen: the venue from Home, as at now, purpose tender. A guest never chooses a "
            "purpose: that would let them browse internal treasury rates.")
    sc.edit("The selected FX rate", "detailPanel", label="The rate",
            columns=["FxRate.fromCurrency", "FxRate.toCurrency", "FxRate.rate", "FxRate.effectiveFrom"])
    sc.card("Every product", "Prices in your currency", ["Product.name", "Product.description"],
            "The venue's products with the price converted at the rate above; the venue's own currency stays "
            "the price charged. " + SESSION_VENUE)
    sc.state("emptyNoResults", "Never shown: the screen sends no filter a guest chose.")
    sc.state("emptyFirstRun", "Not reachable: with no other currency at the venue the screen is not linked, "
             "and prices stay in the venue's currency.")


def parking(sc):
    drop_filters(sc, "Venue id")
    sc.card("Every parking facility", "Car parks", ["ParkingFacility.name"],
            "The venue's car parks by name; no live free-bay count in the first release. " + SESSION_VENUE)
    sc.drop("Check out", "secondaryButton")
    sc.drop("Pay", "primaryButton")
    sc.drop_api("checkoutCart", "Parking goes through the basket (R166); checkout is the basket's.")
    sc.drop_api("createPayment", "Payment is the basket's, after checkout (R166).")
    sc.edit("Save parking entitlement", "secondaryButton", label="Change plate")
    o = sc.overlay("formUpdateParkingEntitlement")
    if o is not None:
        o["trigger"] = "Change plate"
        o["body"] = "**The plate only.** `updateParkingEntitlement` with the new plate; a guest never sets a status."
        o["confirm"] = {"label": "Save", "operation": "updateParkingEntitlement"}
        o["dismiss"] = {"label": "Cancel", "discards": ["plate"]}
        o["provenance"] = prov("GFIX-3")
    sc.state("emptyNoResults", "Never shown: the car parks are the venue's, with no filter a guest sets.")


def gst028(sc):
    drop_filters(sc, "Venue id")
    sc.drop("Every parking facility", "dataTable")
    sc.edit("The selected parking facility", "detailPanel", label="Your car park",
            columns=["ParkingFacility.name"])
    sc.state("emptyNoResults", "Never shown: the confirmation shows one order's parking.")


def wallet(sc):
    sc.card("Every wallet transaction", "Activity",
            ["WalletTransaction.kind", "WalletTransaction.amount", "WalletTransaction.balanceAfter",
             "WalletTransaction.reason", "WalletTransaction.recordedAt"])
    for _, c in sc.comps():
        if c.get("label") == "Activity" and "From `wallet.yaml`" not in c.get("notes", ""):
            c["notes"] = c["notes"] + " From `wallet.yaml` `listWalletTransactions`."
    sc.drop("The selected wallet transaction", "detailPanel")


def save_card(sc):
    sc.card("Every payment token", "Saved cards",
            ["PaymentToken.method", "PaymentToken.maskedIdentifier", "PaymentToken.expiresAt",
             "PaymentToken.isDefault"])
    sc.drop("The selected payment token", "detailPanel")
    sc.edit("Store payment token", "primaryButton", label="Add a card")
    o = sc.overlay("formStorePaymentToken")
    if o is not None:
        o["trigger"] = "Add a card"
        o["body"] = ("**The gateway's own card form**, hosted by the provider; it returns the token that "
                     "`storePaymentToken` saves with the guest's consent. No token, provider or consent id is "
                     "ever a field.")
        o["confirm"] = {"label": "Save card", "operation": "storePaymentToken"}
        o["dismiss"] = {"label": "Cancel", "discards": []}
        o["provenance"] = prov("GFIX-3")


def web021(sc):
    wallet(sc)
    save_card(sc)


def gst071(sc):
    save_card(sc)
    o = sc.overlay("formRedeemLoyaltyPoints")
    if o is not None:
        o["body"] = ("**How many points to spend.** The guest is the caller and the programme is the venue's; "
                     "`redeemLoyaltyPoints` is sent with both, never typed.")
        o["provenance"] = prov("GFIX-3")


def web033(sc):
    drop_filters(sc, "Outlet id", "Category id", "In stock only")
    sc.add("contentBody", {"kind": "selectField", "label": "Shop", "operation": "listMerchandise",
                           "notes": "The venue's shops by name; sends the chosen shop's `outletId`.",
                           "provenance": prov("GFIX-3")})
    sc.add("contentBody", {"kind": "selectField", "label": "Category", "operation": "listMerchandise",
                           "notes": "The shop's categories by name; sends the chosen `categoryId`.",
                           "provenance": prov("GFIX-3")})
    sc.card("Every merchandise", "Products", ["MerchandiseItem.name", "MerchandiseItem.description",
                                              "MerchandiseItem.imageAssetRef", "MerchandiseItem.price",
                                              "MerchandiseItem.isReturnable"])
    sc.drop("The selected merchandise", "detailPanel")
    sc.drop("Lookup merchandise", "primaryButton")
    # lookupMerchandise stays (F51): the price check behind a product's page, never a barcode button.
    for _, c in sc.comps():
        if c.get("impliedBy") == "lookupMerchandise" and c.get("kind") == "searchField":
            c["operation"] = "lookupMerchandise"
            c["notes"] = ("The product's current price and stock at the chosen shop when its page opens "
                          "(`lookupMerchandise`); a guest never scans a barcode.")
    sc.drop("Add cart line", "secondaryButton")
    sc.drop_overlay("formAddCartLine")
    sc.add("actionBar", {"kind": "primaryButton", "label": "Add to cart", "operation": "addCartLine",
                         "notes": "Adds the product with the quantity on its card (`addCartLine`).",
                         "provenance": prov("GFIX-3")})
    sc.state("emptyNoResults", "Nothing matches the shop, category or search picked; the other products are "
             "still there. Names it and offers to clear it.")


def web039(sc):
    drop_filters(sc, "Venue id", "Open only")
    sc.card("Every queue", "Waits", None, "Wait times by category (rides, dining). " + SESSION_VENUE)
    sc.drop("The selected queue", "detailPanel")
    sc.state("emptyNoResults", "No attraction of the category picked; the other categories stay.")


def gst032(sc):
    sc.state("emptyNoResults", "Nothing the concierge found matches the question; it says so in the "
             "conversation and offers to hand over to a person.")
    sc.drop("Create guest F&B order", "primaryButton")
    sc.drop_overlay("formCreateGuestFnbOrder")
    sc.add("contentBody", {"kind": "cardList", "label": "Order to confirm", "operation": "createGuestFnbOrder",
                           "notes": "An order the concierge proposes is a card in the conversation: items, total "
                                    "and Confirm, which places it (`createGuestFnbOrder`). No raw form.",
                           "provenance": prov("GFIX-3")})


def gst045(sc):
    sc.state("emptyNoResults", "No ticket to send: the guest holds none that can be shared. Says so and offers "
             "My Tickets.")
    sc.edit("Ticket ids", "multiSelect", kind="cardList", label="Tickets to send",
            notes="The guest's tickets as cards; ticking a card picks it.")
    sc.edit("Recipient", "textField", label="Send to",
            notes="A channel (email, SMS or WhatsApp), then the address.")
    sc.edit("Transfer order tickets", "primaryButton", label="Send tickets")


def gst056(sc):
    sc.drop("Every bundle", "dataTable")
    sc.drop("The selected bundle", "detailPanel")
    sc.drop_api("listCatalogueBundles", "The screen opens on one bundle (`bundleId` from Item Detail); the "
                "list of every bundle was the generator's.")
    sc.state("emptyNoResults", "Never shown: the screen opens on one bundle and has no filter.")
    sc.edit("Add cart line", "primaryButton", label="Add to cart")
    o = sc.overlay("formAddCartLine")
    if o is not None:
        o["trigger"] = "Add to cart"
        o["body"] = "**The choices the bundle asks for, and how many.** `addCartLine` with the bundle's variant."
        o["provenance"] = prov("GFIX-3")


def gst063(sc):
    search_screen(sc)


def gst072(sc):
    sc.drop("Create referral", "secondaryButton")
    sc.drop_overlay("formCreateReferral")
    sc.drop_api("createReferral", "Referrals are not this screen's job, and the referral write has no reader "
                "yet.")
    sc.drop("The challenge", "detailPanel")
    sc.drop_api("getMyChallenges", "Challenges are not this screen's job.")
    sc.card("Every group package definition", "Group packages", None)
    o = sc.overlay("formRequestGroupBooking")
    if o is not None:
        o["body"] = ("**Only what GST-008 did not ask**: the date wanted and a note. The kind, the package and "
                     "the expected size come from the booking already started (DI-1000: never ask twice).")
        o["provenance"] = prov("GFIX-3")


def gst050(sc):
    cabana(sc, "Cabanas")
    sc.edit("Add cart line", "primaryButton", label="Add to cart")
    o = sc.overlay("formAddCartLine")
    if o is not None:
        o["trigger"] = "Add to cart"
        o["body"] = "**Type, date and guests**, then `addCartLine`; nothing else is asked."
        o["provenance"] = prov("GFIX-3")


# --------------------------------------------------------------------------------------------------
# GFIX-3: the kiosk
# --------------------------------------------------------------------------------------------------
def ksk004(sc):
    sc.card("Every product variant", "Tickets", ["ProductVariant.name", "ProductVariant.description"],
            "Large counters per ticket type; inactive variants never shown.")


def ksk005(sc):
    sc.drop("Acquire inventory hold")
    sc.drop_overlay("formAcquireInventoryHold")
    sc.add("contentBody", {"kind": "cardList", "label": "Times", "operation": "addCartLine",
                           "notes": "A tap on a time adds the chosen tickets for it (`addCartLine`), which takes "
                                    "the hold; the guest never sees the word hold.", "provenance": prov("GFIX-3")})


def ksk006(sc):
    promo_banner(sc)
    sc.add("contentBody", {"kind": "banner", "label": "Offers applied", "operation": "evaluatePromotions",
                           "notes": "The promotions that apply and the near misses, evaluated by themselves "
                                    "(`evaluatePromotions`) and shown before payment (F75 step 4).",
                           "provenance": prov("GFIX-3")})
    sc.drop("Add cart line", "primaryButton")
    sc.drop_overlay("formAddCartLine")
    sc.add("contentBody", {"kind": "numberField", "label": "Quantity", "operation": "addCartLine",
                           "notes": "A large stepper per line; + adds one more (`addCartLine`).",
                           "provenance": prov("GFIX-3")})
    sc.drop("Checkout cart", "secondaryButton")
    sc.drop_overlay("formCheckoutCart")
    sc.add("actionBar", {"kind": "primaryButton", "label": "Pay", "operation": "checkoutCart",
                         "notes": "Checks the cart out (`checkoutCart`) and goes to payment.",
                         "provenance": prov("GFIX-3")})


def ksk007(sc):
    for lab in ("id", "orderId", "tender", "amount", "tenderedAmount", "walletAuthorisationId", "deviceId",
                "recordedAt"):
        sc.drop(lab, "textField")
    sc.drop("Create payment", "primaryButton")
    sc.add("contentBody", {"kind": "paymentTerminal", "label": "Tap, insert or scan to pay",
                           "operation": "createPayment",
                           "notes": "The amount due and the card terminal's prompt. The kiosk and the terminal "
                                    "fill the payment (`createPayment`): order, tender, amount and device are "
                                    "never typed. Card only (F75 step 5).", "provenance": prov("GFIX-3")})


def reprint(sc, label, body, reason):
    sc.rebind("transferOrderTickets", "reprintOrder", "Send the guest's own tickets again, or print them "
              "(`reprintOrder`); a kiosk changes no owner (GFIX-3)", "GFIX-3", contract="orders",
              why="A transfer changes the tickets' owner; at a kiosk the guest is resending or printing their own "
                  "tickets, which is `reprintOrder` by email, SMS or print.")
    for lab in ("Ticket ids", "Recipient", "Message"):
        sc.drop(lab)
    sc.edit("Transfer order tickets", "primaryButton", label=label)
    o = sc.overlay("formTransferOrderTickets") or sc.overlay("sendTickets")
    if o is not None:
        o["id"] = "sendTickets"
        o["trigger"] = label
        o["body"] = body
        o["confirm"] = {"label": label, "operation": "reprintOrder"}
        o["dismiss"] = {"label": "Back", "discards": ["destination"]}
        o["provenance"] = prov("GFIX-3")
    elif sc.find(label, "primaryButton")[1] is not None:
        sc.add("contentBody", {"kind": "selectField", "label": "Send to",
                               "notes": "Email or SMS, then the address on the kiosk keyboard. " + reason,
                               "operation": "reprintOrder", "provenance": prov("GFIX-3")})


def ksk009(sc):
    sc.strip()
    reprint(sc, "Send to my phone", "**Email or SMS, then the address.** `reprintOrder` with `delivery` email "
            "or sms for this order's tickets; nobody else becomes their owner.", "")


def ksk010(sc):
    reprint(sc, "Send to my phone", "", "`reprintOrder` with `reason` `printerFault`: the sale stands and the "
            "tickets go to the guest's phone.")


def ksk012(sc):
    reprint(sc, "Print my tickets", "", "`reprintOrder` with `delivery` `print`, or email or SMS: collecting is "
            "printing, not a transfer (DI-637).")


SCREENS = {
    "WEB-001": web001, "WEB-002": web002, "WEB-003": search_screen, "WEB-004": item_page, "WEB-005": web005,
    "WEB-006": web006, "WEB-007": seat_step, "WEB-010": web010, "WEB-012": web012, "WEB-013": confirmation,
    "WEB-014": web014, "WEB-019": web019, "WEB-021": web021, "WEB-022": web022, "WEB-023": web023,
    "WEB-025": lambda sc: sc.drop("The tenant app status", "detailPanel",
                                  why="GFIX-3: the CMS status fields are staff only"),
    "WEB-028": lambda sc: None, "WEB-029": lambda sc: None,
    "WEB-030": web030, "WEB-031": web031, "WEB-032": offers, "WEB-033": web033, "WEB-035": fx,
    "WEB-039": web039, "WEB-041": parking, "WEB-045": web045,
    "GST-001": gst001, "GST-002": gst002, "GST-003": gst003, "GST-004": item_page, "GST-005": lambda sc: None,
    "GST-007": gst007, "GST-009": gst009, "GST-010": confirmation, "GST-011": wallet, "GST-014": gst014,
    "GST-015": gst015, "GST-016": reservations, "GST-018": gst018, "GST-019": gst019, "GST-021": gst021,
    "GST-027": parking, "GST-028": gst028, "GST-032": gst032, "GST-037": offers, "GST-038": gst038,
    "GST-040": gst040, "GST-041": gst041, "GST-044": fx, "GST-045": gst045, "GST-047": lambda sc: None,
    "GST-049": seat_step, "GST-050": gst050, "GST-056": gst056, "GST-057": gst057,
    "GST-058": lambda sc: cabana(sc, "Cabanas"), "GST-063": gst063, "GST-071": gst071, "GST-072": gst072,
    "KSK-002": ksk002, "KSK-003": ksk003, "KSK-004": ksk004, "KSK-005": ksk005, "KSK-006": ksk006,
    "KSK-007": ksk007, "KSK-009": ksk009, "KSK-010": ksk010, "KSK-012": ksk012,
}
# Screens whose no-access state is the public one rather than the signed-in guest's.
PUBLIC = {"WEB-028", "WEB-029", "GST-047", "WEB-045", "GST-057"}

# Flows that named, on one of these screens, an operation the screen no longer declares.
FLOWS = [
    ("F01-guest-online-purchase.yaml", "WEB-001", "getTenantConfig", "getPublishedTenantConfig"),
    ("F07-guest-buys-at-a-kiosk.yaml", "KSK-002", "getTenantConfig", "getPublishedTenantConfig"),
    ("F75-a-kiosk-serves-itself-and-calls-for-help.yaml", "KSK-002", "getTenantConfig",
     "getPublishedTenantConfig"),
    ("F55-a-guest-buys-on-the-web-and-transfers-to-a-frien.yaml", "WEB-030", "listOrders", "listMyOrders"),
    ("F75-a-kiosk-serves-itself-and-calls-for-help.yaml", "KSK-009", "transferOrderTickets", "reprintOrder"),
    ("F57-a-guest-uses-a-kiosk-and-it-fails.yaml", "KSK-010", "transferOrderTickets", "reprintOrder"),
]
# Parking is paid in the basket (R166): F50's payment step moves from the car-park screen to Review & Payment.
FLOW_TEXT = [
    ("F50-a-guest-arrives-parks-and-gets-in.yaml",
     "- step: 2\n  screen: GST-027\n  action: They pay, and the parking entitlement is issued.",
     "- step: 2\n  screen: GST-009\n  action: They pay in the basket, and the parking entitlement is issued "
     "(R166; GFIX-3, 2 October)."),
]
FLOW_OUTCOME = {
    ("F75-a-kiosk-serves-itself-and-calls-for-help.yaml", "KSK-009"):
        ("`transferOrderTickets` is how a guest with no printer still\n    leaves with a ticket.",
         "`reprintOrder` by email or SMS is how a guest with no printer\n    still leaves with a ticket; "
         "nobody else becomes its owner (GFIX-3, 2 October)."),
}


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def fix_flows(apply, log):
    for name, old, new in FLOW_TEXT:
        p = ROOT / "flows" / name
        text = p.read_text(encoding="utf-8")
        if old in text:
            log.append(f"flows/{name}: rewritten step")
            if apply:
                write(p, text.replace(old, new))
    for name, sid, old, new in FLOWS:
        p = ROOT / "flows" / name
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        out, cur, changed = [], None, False
        for ln in lines:
            m = re.match(r"^  screen: (\S+)", ln)
            if m:
                cur = m.group(1)
            if cur == sid and ln.strip() == f"- {old}":
                ln = ln.replace(old, new)
                changed = True
            out.append(ln)
        text2 = "\n".join(out)
        o = FLOW_OUTCOME.get((name, sid))
        if o and o[0] in text2:
            text2 = text2.replace(o[0], o[1])
        if changed or text2 != text:
            log.append(f"flows/{name}: {sid} {old} -> {new}")
            if apply:
                write(p, text2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    log = []
    for code, f in FILES.items():
        text = f.read_text(encoding="utf-8")
        doc = yaml.safe_load(text)
        for s in doc["screens"]:
            sc = Screen(s, log)
            fn = SCREENS.get(s["id"])
            if fn:
                fn(sc)
                sc.strip()
            st = s.get("states") or {}
            na = str(st.get("emptyNoAccess") or "")
            if s["id"] in PUBLIC and "Nothing here needs a sign-in" not in na and s["id"] in SCREENS:
                sc.state("emptyNoAccess", NA_PUBLIC)
            elif PERMISSION_STATE.search(na):
                sc.state("emptyNoAccess", NA_KIOSK if code == "P05" else NA_GUEST)
        out = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100)
        if out != text:
            log.append(f"{f.name}: written" if a.apply else f"{f.name}: would change")
            if a.apply:
                write(f, out)
    fix_flows(a.apply, log)
    print("\n".join(log) if log else "nothing to do")
    if not a.apply and log:
        print("\nnothing written — pass --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
