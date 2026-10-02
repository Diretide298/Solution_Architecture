#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The white-label map: every element a tenant configures, where, and which guest screens it changes.

**Chinmay, 1 October: "How input should be how output. Especially the website white label."** The
guest website, app and kiosk are drawn in the venue's brand, and the brand is configuration: a CMS
field (`CMS-005` *Primary colour*) becomes something a guest sees (the Book button on `WEB-005`).
That path ran through four files nobody reads together -- the CMS screen, the `set*` operation it
calls, the schema behind it, and the guest screen that reads it back through `getTenantConfig` --
so each Claude Design session drew the guest screens in one fixed palette and the CMS screens as
forms that changed nothing.

This derives the map from the contracts and the screens:

- **Elements.** Every field of every configuring operation's request (`white-label.yaml`, plus the
  two marketing-crm ones a CMS screen calls), flattened, with its control, allowed values, limits
  and default from the schema.
- **Configured on.** The P13 and P09 screens whose `apis` call that operation.
- **Reaches.** The guest screens (P01, P02, P05) it changes: by the part's reach (the authored
  `PARTS` table below: the shell, the home screens, the booking steps, ...), narrowed where the
  contract or a guest screen names the field or the screen.

Writes, both derived, never edited:

    handoff/design-inputs/white-label-map.json            read by tools/design_spec.py per screen
    handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md the app-level map for design sessions

Run by `tools/refresh.sh` before `export-design-batch.py --all`.

    python3 tools/build-white-label-map.py
"""
from __future__ import annotations

import collections
import datetime
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "handoff" / "design-inputs" / "white-label-map.json"
OUT_MD = ROOT / "handoff" / "design-batches" / "apps" / "1-guest-app" / "WHITE-LABEL.md"


def _spec():
    spec = importlib.util.spec_from_file_location("design_spec", ROOT / "tools" / "design_spec.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DS = _spec()
PKG = DS.PKG

# **Authored: each part of the tenant's configuration, the operation that writes it, and how far
# it reaches on the guest surfaces.** Reach is one of:
#   shell     every guest screen on the channels it applies to (loaded once by getTenantConfig)
#   home      the guest home screens (P01/P02 screens that load the configuration)
#   booking   the booking steps (guest screens that read getPublishedBookingFlow)
#   guided    Help me choose (getPublishedGuidedChoice)        pages   content pages and policies
#   faqs      FAQ screens        status   screens that read getTenantAppStatus (and every screen in
#   maintenance)        web   every P01 screen (the address bar, search results)
#   cookie    the cookie banner (getCookieConsentRuntime)       analytics   nothing drawn
#   store     the phone's home screen and the store listing: no guest screen
PARTS = [
    ("brand", "Brand: logo, splash, intro video", ["setBrandIdentity"], "shell"),
    ("theme", "Theme: colours, shape, surfaces", ["setTheme"], "shell"),
    ("fonts", "Fonts", ["setFonts"], "shell"),
    ("header", "Header", ["setHeader"], "shell"),
    ("navigation", "Navigation: menu, tab bar, Buy tickets button", ["setNavigation"], "shell"),
    ("footer", "Footer", ["setFooter"], "web"),
    ("languages", "Languages and right-to-left", ["setLanguages"], "shell"),
    ("modules", "Modules shown to guests", ["setModuleEnablement"], "shell"),
    ("features", "Features", ["setFeatureToggles"], "shell"),
    ("bookingFlow", "Booking settings (tenant, with per-venue overrides)", ["setBookingFlowConfig"], "booking"),
    ("bookingFlows", "Booking flows: steps, their order and per-flow settings",
     ["createBookingFlowDefinition", "updateBookingFlowDefinition"], "booking"),
    ("homepage", "Homepage sections", ["setHomepageLayout"], "home"),
    ("banners", "Banners", ["createBanner", "updateBanner"], "home"),
    ("promoBlocks", "Promo blocks", ["createPromoBlock", "updatePromoBlock"], "home"),
    ("guidedChoices", "Help me choose", ["createGuidedChoice", "updateGuidedChoice"], "guided"),
    ("pages", "Content pages", ["createContentPage", "updateContentPage"], "pages"),
    ("policies", "Policies (terms, privacy, refunds)", ["setPolicy"], "pages"),
    ("faqs", "FAQs", ["setFaqs"], "faqs"),
    ("maintenance", "Availability and maintenance", ["setMaintenanceMode"], "status"),
    ("domains", "Custom domain", ["claimCustomDomain"], "web"),
    ("seo", "SEO metadata", ["setSeoMetadata"], "web"),
    ("cookieBanner", "Cookie banner", ["setCookieBannerDesign"], "cookie"),
    ("analytics", "Analytics providers", ["setAnalyticsProvider"], "analytics"),
    ("appIcons", "App icons", ["setAppIcons"], "store"),
    ("storeAccounts", "Store accounts", ["setStoreAccounts"], "store"),
    ("appBuilds", "App builds", ["requestAppBuild"], "store"),
]

# **Authored: what an element paints, where the schema's own description does not say.** Theme
# tokens follow `screens/_design-tokens.yaml` `whiteLabel` (accentSolid, surfaceRaised and the UI
# font are the only overridable tokens; semantic pairs are fixed). Correct a line here if the
# design disagrees; every bundle picks it up.
EFFECT = {
    "theme.primaryColour": "the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings",
    "theme.secondaryColour": "secondary buttons and secondary emphasis: unselected chips, secondary tabs",
    "theme.accentColour": "highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices",
    "theme.backgroundColour": "the page background behind every screen (the `ground` token)",
    "theme.textColour": "body text on the background",
    "theme.cornerRadius": "the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest)",
    "theme.surfaceStyle": "cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token)",
    "theme.buttonStyle": "every button's shape: solid fill, outline, or pill",
    "theme.componentColours.primaryCta": "the one main call to action on each screen, when it should differ from the brand colour",
    "theme.componentColours.payButton": "the Pay button at checkout",
    "theme.componentColours.addToCart": "every Add to cart button",
    "theme.componentColours.buyTicketsButton": "the persistent Buy tickets button (mobile tab bar)",
    "theme.componentColours.link": "text links",
    "theme.componentColours.badge": "badges on cards (LIMITED, NEW, 11 left)",
    "brand.logoAssetRef": "the logo in the header or nav bar, the splash and the footer",
    "brand.logoDarkAssetRef": "the logo on dark backgrounds (falls back to the primary logo)",
    "brand.logoVariant": "which logo lockup sits in the nav bar, and whose colours drive the theme",
    "brand.faviconAssetRef": "the browser tab icon (website only)",
    "brand.showPoweredBy": "the *Powered by TICVAI* credit on the launch screen, at the foot of Account and in the web footer; on by default, and switching it off needs the licence add-on (403 powered-by-locked)",
    "homepage.templateKey": "the landing-page template the home started from (listLandingPageTemplates); a tenant with no landing page of its own starts from one, and the sections it fills stay editable",
    "homepage.landingSource": "whether the storefront home is the landing page, or the tenant's own site is and links in with deep links",
    "homepage.sections[].maxItems": "how many cards the section shows, the counts the approved wireframe offers",
    "homepage.sections[].scrollAnimation": "how the section enters as the guest scrolls: rise, scale, slide, blur or none (none whenever the device asks for reduced motion)",
    "fonts.primaryLatin": "headings and body text in English",
    "fonts.primaryArabic": "headings and body text in Arabic",
    "fonts.secondaryLatin": "the secondary face (eyebrows, numbers) in English",
    "fonts.secondaryArabic": "the secondary face in Arabic",
    "header.layout": "the header: logo left, logo centred, or logo with the menu",
    "languages.languages": "the language button in the header; Arabic flips every screen right to left",
    "languages.defaultLanguage": "the language a first visit opens in",
    "bookingFlow.stepIndicator": "the step indicator above every booking step: bar, numbered, dots, segmented, breadcrumb, pills, ticks, or none",
    "bookingFlow.cartLayout": "where the cart sits: a sidebar right or left, sliding in, sliding up, a single column, or a floating basket icon",
    "bookingFlow.cartSideInRtl": "the cart's side in Arabic: kept right, or mirrored left",
    "bookingFlow.cardLayout": "ticket and product cards: stacked rows, split rows, cards across, or poster cards",
    "bookingFlow.cardSize": "card size: compact, standard, large, extra large",
    "bookingFlow.density": "spacing of the booking screens: compact, standard, roomy",
    "bookingFlow.heroBanner": "the hero banner at the top of the booking pages",
    "bookingFlow.embedMode": "full page, or embedded in the venue's own site (no hero, event page or venue header)",
    "navigation.kind": "the main navigation: bottom tab bar, drawer, or tabs",
    "navigation.buyButton.style": "the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden",
}

# **Authored: one alternate tenant, so a design shows the brand is configuration.** Coastal Aqua is
# a venue the contract itself uses as an example (BookingFlowConfig). Colour pairs pass 4.5:1.
ALTERNATE = {
    "name": "Coastal Aqua",
    "values": {
        "Primary colour": "#0077B6", "Secondary colour": "#023E8A", "Accent colour": "#FFB703",
        "Background colour": "#F5FAFC", "Text colour": "#0B1324", "Corner radius": "18",
        "Surface style": "Solid", "Button style": "Pill", "Logo variant": "Duotone",
        "Header layout": "Logo centre", "Step indicator": "Dots", "Card layout": "Cards across",
        "Card size": "Standard", "Cart layout": "Floating icon", "Fonts": "Poppins / Tajawal",
    },
    "keyScreens": ["WEB-001", "WEB-005", "WEB-006", "WEB-010", "WEB-012", "GST-001", "GST-007", "GST-041",
                   "KSK-002", "KSK-003"],
}
ALT_BY_ID = {"theme.primaryColour": "#0077B6", "theme.buttonStyle": "pill", "theme.surfaceStyle": "solid",
             "theme.cornerRadius": "18", "brand.logoVariant": "duotone", "header.layout": "logoCentre",
             "bookingFlow.stepIndicator": "dots", "bookingFlow.cardLayout": "cardsAcross",
             "bookingFlow.cartLayout": "floatingIcon", "bookingFlow.cartSideInRtl": "mirror",
             "navigation.buyButton.style": "floating", "languages.languages": "en, ar",
             "bookingFlow.cardSize": "standard", "bookingFlow.density": "roomy",
             "bookingFlow.timesPerPage": "8", "bookingFlow.seatPicker": "zonesThenSeats",
             "homepage.sections[].scrollAnimation": "slide", "homepage.sections[].maxItems": "6",
             "homepage.templateKey": "a TICVAI template, picked by its name and thumbnail",
             "brand.showPoweredBy": "off, where the licence allows it"}

# **Authored: a label or control the schema name does not give** (2 October decisions, CHG-EXP-004/005).
LABEL = {"brand.showPoweredBy": "Powered by TICVAI credit", "homepage.sections[].maxItems": "Sections: card count",
         "homepage.templateKey": "Landing-page template"}
CONTROL = {"homepage.templateKey": "template picker: name and thumbnail (listLandingPageTemplates)"}
EXAMPLES = ["theme.primaryColour", "theme.buttonStyle", "theme.surfaceStyle", "theme.cornerRadius",
            "brand.logoVariant", "header.layout", "navigation.buyButton.style", "languages.languages",
            "bookingFlow.stepIndicator", "bookingFlow.cardLayout", "bookingFlow.cardSize", "bookingFlow.cartLayout",
            "bookingFlow.cartSideInRtl", "bookingFlow.timesPerPage", "bookingFlow.seatPicker",
            "bookingFlows.steps[].enabled", "bookingFlows.settings.signInAt", "homepage.sections[].kind",
            "homepage.sections[].maxItems", "homepage.sections[].scrollAnimation", "homepage.templateKey",
            "brand.showPoweredBy"]

# **Authored: what Chinmay decided on 2 October about the white label as a whole** (workbook Q150, Q152,
# Q153, Q160, batch 2 #41, and the pre-apply round). Rendered in WHITE-LABEL.md and once per guest batch,
# so no design session draws a dark mode, a fixed credit or a fixed card count (CHG-EXP-003..005).
DECIDED = [
    "**No dark or light mode.** The venue's chosen theme applies on every device setting; `Theme.darkMode` is "
    "deprecated and ignored, never drawn, and the guest app has no Light/Dark switch (Chinmay, 2 October, Q150; "
    "CHG-CSA-035).",
    "***Powered by TICVAI* is a tenant toggle, on by default** (`brand.showPoweredBy`): shown on the launch screen, "
    "at the foot of Account and in the web footer; switching it off needs the licence add-on, or 403 "
    "`powered-by-locked` (Chinmay, 2 October, Q160; DI-297; CHG-CSA-036).",
    "**Each homepage section sets its card count and its scroll animation** (`maxItems`; `scrollAnimation` rise, "
    "scale, slide, blur or none, default rise): every customisation option of the approved wireframe "
    "(Chinmay, 2 October, Q152 and Q153; DI-1088; CHG-CSA-040).",
    "**Landing-page templates.** A tenant with no landing page of its own starts from a TICVAI template "
    "(`listLandingPageTemplates`, kept as `HomepageLayout.templateKey`); one with its own site links in with deep "
    "links (`landingSource` ownSite) (Chinmay, 2 October, batch 2 #41; CHG-CSA-037).",
]

# Names too common to mean one field when a guest screen mentions them.
GENERIC = {"layout", "label", "kind", "enabled", "style", "name", "title", "id", "items", "steps", "settings",
           "channel", "version", "language", "hostname", "message", "imageUrl", "linkTarget", "startsAt", "endsAt",
           "isEnabled", "isVisible", "sortOrder", "target", "mode", "status", "source", "state", "url", "icon",
           "preset", "density", "languages", "modules", "features", "columns", "sections", "questions", "text",
           "description", "subtitle", "placement", "behaviour"}
SCREEN = re.compile(r"\b(WEB|GST|KSK)-\d{3}\b")


def guest_screens() -> dict:
    return {sid: (s, p) for sid, (s, p) in PKG.screens.items() if p.get("code") in DS.GUEST_PLATFORMS}


def callers(op_ids: set, plats=DS.GUEST_PLATFORMS) -> list[str]:
    out = []
    for sid, (s, p) in PKG.screens.items():
        if p.get("code") not in plats:
            continue
        if {a.get("operationId") for a in s.get("apis") or []} & op_ids:
            out.append(sid)
    return sorted(out)


def reach(kind: str) -> tuple[list[str], str]:
    g = guest_screens()
    if kind == "shell":
        return sorted(g), "every guest screen (web, app and kiosk)"
    if kind == "home":
        h = [x for x in callers({"getTenantConfig"}, ("P01", "P02"))]
        return h, "the guest home screens"
    if kind == "booking":
        return callers({"getPublishedBookingFlow"}), "the booking steps"
    if kind == "guided":
        return callers({"getPublishedGuidedChoice"}), "Help me choose"
    if kind == "pages":
        return callers({"listContentPages", "listPolicies"}), "the content and policy pages"
    if kind == "faqs":
        return callers({"listFaqs"}), "the FAQ screens"
    if kind == "status":
        return callers({"getTenantAppStatus"}), "the screens that check availability (every screen shows maintenance)"
    if kind == "web":
        return sorted(x for x, (_, p) in g.items() if p.get("code") == "P01"), "every website screen"
    if kind == "cookie":
        return callers({"getCookieConsentRuntime"}), "the cookie banner"
    if kind == "analytics":
        return [], "nothing drawn: tracking only"
    return [], "no guest screen: the phone's home screen and the store listing"


def mentions() -> dict:
    """field name -> guest screens whose own text names it in backticks."""
    out = collections.defaultdict(set)
    for sid, (s, _) in guest_screens().items():
        blob = json.dumps(s, ensure_ascii=False, default=str)
        for tok in set(re.findall(r"`([^`]{2,80})`", blob)):
            for w in re.findall(r"[A-Za-z][A-Za-z0-9]+", tok):
                out[w].add(sid)
    return out


def config_screens(op_id: str) -> list[dict]:
    """The CMS (P13) screens first, then the TICVAI console (P09) ones."""
    out = []
    # The narrowest screen first: CMS-005 Theme Editor (two operations) before CMS-003 Typography,
    # which also saves the theme.
    for sid, (s, p) in sorted(PKG.screens.items(), key=lambda x: (x[1][1].get("code") != "P13",
                                                                   len(x[1][0].get("apis") or []), x[0])):
        if p.get("code") not in ("P13", "P09"):
            continue
        if op_id in {a.get("operationId") for a in s.get("apis") or []}:
            out.append({"screen": sid, "name": s.get("name"), "op": op_id})
    return out


def build() -> dict:
    g = guest_screens()
    ment = mentions()
    progress = sorted(sid for sid, (s, _) in g.items()
                      if any(c.get("kind") == "progressIndicator" for _, c in DS._components(s)))
    elements, parts_out = [], []
    for key, label, op_ids, kind in PARTS:
        ops = [o for o in op_ids if o in PKG.ops]
        if not ops:
            continue
        scope, scope_text = reach(kind)
        where = []
        for o in ops:
            where += [w for w in config_screens(o) if w["screen"] not in {x["screen"] for x in where}]
        recs, seen = [], set()
        for o in ops:
            for p in DS.op_params(o, ("path",)):
                if p["name"].endswith("Id") or p["name"] in seen:
                    continue
                seen.add(p["name"])
                recs.append(p)
            rs = DS.request_schema(o)
            if rs:
                for r in DS.flatten(rs):
                    if r["path"] not in seen:
                        seen.add(r["path"])
                        recs.append(r)
        part_ids = []
        for r in recs:
            eid = f"{key}.{r['path']}"
            desc = r["help"]
            # where the contract or a guest screen names it
            named = set(SCREEN.findall(" ".join([desc] + r["conditions"])) and
                        re.findall(r"\b(?:WEB|GST|KSK)-\d{3}\b", " ".join([desc] + r["conditions"])))
            nm = r["name"]
            # An id or a common word names every screen that carries one, not this setting.
            if nm not in GENERIC and len(nm) >= 6 and not re.search(r"Ids?$", nm) and kind not in ("analytics", "store"):
                named |= {x for x in ment.get(nm, set())}
            if nm == "stepIndicator":
                named |= set(progress)
            named &= set(g)
            # Shell parts reach every screen, so only a screen that names the field is listed apart.
            # Other parts reach their scope, plus any guest screen that names the field outside it.
            if kind in ("shell", "web"):
                specific = sorted(named)
            elif kind in ("analytics", "store"):
                specific = []          # nothing a guest screen draws
            else:
                specific = sorted(named | set(scope))
            chan = ""
            low = desc.lower()
            if re.search(r"web only|guest web app|browser tab", low):
                chan = "P01"
            elif re.search(r"every screen of the mobile app|tab bar|native app", low):
                chan = "P02"
            reaches_scr = [x for x in (specific if specific else scope) if not chan or g[x][1].get("code") == chan]
            if kind in ("shell", "web") and not named:
                reaches_text = scope_text if not chan else f"every {chan} screen"
            else:
                reaches_text = (", ".join(reaches_scr[:8]) + (f" … ({len(reaches_scr)})" if len(reaches_scr) > 8 else "")) \
                    if reaches_scr else scope_text
            change = "on publish (CMS-014): web at once, the app on its next launch"
            if kind == "store" or re.search(r"buildTime|baked into the binary|build-time", desc + " ".join(r["conditions"]), re.I):
                change = "needs an app build (CMS-104) on the native apps; the website takes it on publish"
            # A label that reads alone: `header.layout` is 'Header layout', `steps[].enabled` is 'Steps: enabled'.
            segs = [x for x in r["path"].replace("[]", "").split(".") if x]
            lab = r["label"]
            if len(segs) > 1:
                lab = f"{DS.field_label(segs[-2])}: {lab[:1].lower() + lab[1:]}"
            elif r["name"] in GENERIC and lab.lower() not in label.lower():
                lab = f"{label.split(':')[0].split(' (')[0]} {lab[:1].lower() + lab[1:]}"
            el = {
                "id": eid, "part": key, "partLabel": label, "path": r["path"], "label": LABEL.get(eid, lab),
                "control": CONTROL.get(eid, r["control"]), "mask": r["mask"], "required": r["required"],
                # With no enum or limit, the format is what is allowed (#RRGGBB, PNG or SVG ≤ 2 MB).
                "default": DS._default(r),
                "allowed": DS._allowed(r) if DS._allowed(r) != "—" else (r["mask"] or "—"), "help": desc,
                "effect": EFFECT.get(eid, ""), "configuredOn": where, "reach": kind,
                "reachesText": reaches_text, "specific": specific if (kind not in ("shell", "web") or named) else [],
                "channel": chan, "change": change,
                "venueOverride": key == "bookingFlow",
            }
            elements.append(el)
            part_ids.append(eid)
        parts_out.append({"key": key, "label": label, "ops": ops, "reach": kind, "reachText": scope_text,
                          "configuredOn": where, "elements": part_ids})
    # per screen
    guest = {sid: {"specific": []} for sid in g}
    for e in elements:
        if e["reach"] in ("shell", "web") and not e["specific"]:
            continue
        for sid in e["specific"]:
            if sid in guest:
                guest[sid]["specific"].append(e["id"])
    conf = collections.defaultdict(list)
    for e in elements:
        for w in e["configuredOn"]:
            conf[w["screen"]].append(e["id"])
    shell_ids = [e["id"] for e in elements if e["reach"] in ("shell", "web") and e["path"].count(".") == 0
                 and not e["path"].endswith("[]")] + \
                [e["id"] for e in elements if e["id"] in ("theme.componentColours.primaryCta", "theme.componentColours.payButton",
                                                         "navigation.buyButton.style", "brand.faviconAssetRef")]
    shell_parts = []
    for p in parts_out:
        if p["reach"] in ("shell", "web"):
            shell_parts.append({"label": p["label"].split(":")[0] + (" (website)" if p["reach"] == "web" else ""),
                                "count": len(p["elements"]),
                                "screens": [w["screen"] for w in p["configuredOn"]][:3] or ["—"]})
    fixed = [
        "A dark or light mode: the guest surfaces have one theme, the venue's (Chinmay, 2 October; CHG-CSA-035).",
        "Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to "
        "their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel).",
        "Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); "
        "a guest always books a product or package, never a resource (DI-502).",
        "A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).",
    ]
    keys = [k for k in ALTERNATE["keyScreens"] if k in g]
    return {
        "generatedBy": "tools/build-white-label-map.py", "generated": datetime.date.today().isoformat(),
        "note": "Derived from the configuring operations' request schemas and the screens. Never edit; rerun the tool.",
        "elements": elements, "parts": parts_out,
        "guestScreens": guest, "configScreens": dict(conf),
        "shell": shell_ids, "shellParts": shell_parts, "decided": DECIDED, "fixed": fixed,
        "alternateTheme": {**ALTERNATE, "keyScreens": keys},
    }


def _example(e: dict, els: dict) -> str:
    where = e["configuredOn"][0] if e["configuredOn"] else None
    alt = ALT_BY_ID.get(e["id"])
    if not alt:
        en = re.split(r" · ", e["allowed"]) if " · " in e["allowed"] else []
        alt = en[1] if len(en) > 1 else "on" if e["control"] == "toggle" else "a new value"
    alt_label = DS.humanize(alt) if re.match(r"^[a-z][A-Za-z0-9]*$", str(alt)) else alt
    loc = f"in `{where['screen']}` {where['name']}" if where else "in the CMS"
    eff = e["effect"] or e["help"]
    return (f"- **{e['label']}**: {loc}, the tenant sets *{e['label']}* to **{alt_label}** (default {e['default']}) "
            f"→ on {e['reachesText']}: {DS._flat(eff, 260)}.")


def _notes_section() -> list[str]:
    """The white-label process owner's model and worked examples (handoff/design-notes/white-label.yaml),
    when that file exists. Authored there; rendered here, after the generated pipeline."""
    doc = DS.notes()["processes"].get("white-label")
    if not doc:
        return []
    L = ["## The white-label model, from the process owner", "",
         f"*From `handoff/design-notes/white-label.yaml` ({DS._flat(doc.get('owner'), 80) or 'the white-label process'}). "
         "Authored; where it and the generated tables below disagree, it is the one to check first.*", ""]
    ps = doc.get("processSummary")
    if isinstance(ps, dict):
        L += [DS._flat(ps.get("text") or ps.get("summary"), 6000), ""]
        if ps.get("source"):
            L += [f"*(source: {DS._flat(DS._src(ps.get('source')), 300)})*", ""]
    elif ps:
        L += [DS._flat(ps, 6000), ""]
    io = DS._items(doc.get("inputToOutput"))
    if io:
        L += ["**Input → output, worked by the process owner**", ""]
        for x in io:
            if isinstance(x, dict):
                inp = x.get("input") or x.get("field") or x.get("example") or ""
                out = x.get("output") or x.get("result") or x.get("rule") or ""
                where = x.get("configuredOn") or x.get("where") or ""
                L.append(f"- **{DS._flat(inp, 200)}**" + (f" (in {DS._flat(DS._src(where), 80)})" if where else "")
                         + (f" → {DS._flat(DS._src(out), 400)}" if out else "")
                         + (f" *(source: {DS._flat(DS._src(x.get('source')), 160)})*" if x.get("source") else ""))
            else:
                L.append(f"- {DS._flat(x, 500)}")
        L.append("")
    return L


def write_md(m: dict) -> None:
    els = {e["id"]: e for e in m["elements"]}
    di = PKG.di
    L = ["# White label: what a tenant configures, and where a guest sees it", "",
         "> **Generated** by `tools/build-white-label-map.py` from the contracts (`contracts/satellite/white-label.yaml` "
         "and the CMS operations in `marketing-crm.yaml`) and the screens. Edit those, never this file. The same map, "
         "per screen, is in every guest and CMS batch's `BUNDLE.md`.", "",
         "**How to use it in a Claude Design session.** Draw each guest screen (web P01, app P02, kiosk P05) with the "
         "**default theme**, and show **one alternate tenant theme** on the key screens, so a reviewer can see the brand "
         "is configuration, not paint. Nothing on a guest screen may hard-code a brand colour, logo, font, card layout or "
         "step-indicator style: each comes from a field below. On a CMS screen, every field shows its allowed values and "
         "default, and the preview shows the output on the guest screen it reaches.", "",
         f"**{len(m['elements'])} configurable elements in {len(m['parts'])} parts**, set on "
         f"{len(m['configScreens'])} CMS and console screens, reaching {sum(1 for v in m['guestScreens'].values())} guest screens.", ""]
    # pipeline
    L += ["## How an input becomes an output", "",
          "1. **The tenant edits the working draft** on a CMS screen (`CMS-002` to `CMS-019`, `CMS-101` to `CMS-104`). "
          "Every `set*` call writes the draft only; nothing reaches a guest yet.",
          "2. **Previews it** (`CMS-006` Component Preview, `CMS-012` RTL Preview): the draft rendered on the guest screens, "
          "in both directions. *Arabic is a mirror, not a translation.*",
          "3. **Validates and publishes** (`CMS-014` Publishing Workflow): `validateTenantConfig` names every missing or "
          "failing part; `publishTenantConfig` makes it live. **The website takes it at once; the app on its next launch.**",
          "4. **The guest surface reads it** once per visit through `getTenantConfig` (on `WEB-001`, `GST-001`, `KSK-002`), "
          "and the booking steps read their flow through `getPublishedBookingFlow`. Booking settings are resolved for the "
          "venue the guest picked: the tenant's values with that venue's override laid over them, field by field.",
          "5. **Some changes need an app build** (`CMS-104`): app icons, and on the native apps the splash and custom font files. "
          "The website takes those on publish too.",
          "6. **Rolls back** (`CMS-015` Version History): restore copies an earlier version into the draft; it is reviewed and "
          "published like any other change, never in one click.", ""]
    for fid in ("F22", "F102", "F103"):
        name, path = PKG.flows["names"].get(fid, (None, None))
        if not name:
            continue
        steps = [(st, sid) for sid, xs in PKG.flows["steps"].items() for f_, _, _, st in xs if f_ == fid]
        steps.sort(key=lambda x: x[0].get("step") or 0)
        L += [f"**Flow {fid}, {name}** (`{path}`)", ""] + [
            f"{st.get('step')}. `{sid}` {PKG.name_of(sid)}: {DS._flat(st.get('action'), 120)} → {DS._flat(st.get('outcome'), 220)}"
            for st, sid in steps] + [""]
    L += _notes_section()
    # examples
    L += ["## Input → output, by example", "",
          "Each line: the CMS field (input), the value an alternate tenant would set, and what changes on the guest screens (output).", ""]
    L += [_example(els[i], els) for i in EXAMPLES if i in els] + [""]
    # themes
    alt = m["alternateTheme"]
    L += ["## The default theme and the alternate tenant theme", "",
          "**Default theme.** The palette, type and shapes of the reference design "
          "(`sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`, and Mobile App v4 for the app), "
          "with every setting at its default in the tables below (Glass surfaces, Solid buttons, Bar step indicator, "
          "Stacked rows, Compact cards, cart sidebar right).", "",
          f"**Alternate tenant theme: {alt['name']}.** " + "; ".join(f"{k} {v}" for k, v in alt["values"].items()) + ".", "",
          "**Show it on:** " + ", ".join(f"`{x}` {PKG.name_of(x)}" for x in alt["keyScreens"]) + ".", ""]
    # elements by part
    L += ["## Every configurable element", "",
          "Columns: the element (its id in the map), where it is set, the control, allowed values and rules, the default, "
          "the guest screens it reaches, and what it changes there.", ""]
    for p in m["parts"]:
        where = ", ".join(f"`{w['screen']}` {w['name']}" for w in p["configuredOn"]) or "no CMS screen calls it yet"
        L += [f"### {p['label']}", "",
              f"Set on {where} through {', '.join('`' + o + '`' for o in p['ops'])}. Reaches {p['reachText']}."
              + (" A venue may override any of these for itself (`venueOverrides`)." if p["key"] == "bookingFlow" else ""), "",
              "| Element | Control | Required | Allowed values and rules | Default | Reaches | What it changes | When it goes live |",
              "|---|---|---|---|---|---|---|---|"]
        for i in p["elements"]:
            e = els[i]
            L.append(f"| {e['label']} `{e['id']}` | {e['control']} | {'yes' if e['required'] else 'no'} | "
                     f"{DS._flat(e['allowed'], 220)} | {e['default']} | {DS._flat(e['reachesText'], 140)} | "
                     f"{DS._flat(e['effect'] or e['help'], 240) or '—'} | {e['change']} |")
        L.append("")
    # screens
    L += ["## Each guest screen and what it takes from the configuration", "",
          "Every guest screen takes the shell-wide parts (brand, theme, fonts, header, navigation, languages, modules, "
          "features). Listed here: what each takes beyond them.", "",
          "| Screen | Takes |", "|---|---|"]
    for sid in sorted(m["guestScreens"]):
        sp = m["guestScreens"][sid]["specific"]
        parts = collections.Counter(els[i]["partLabel"].split(":")[0] for i in sp)
        L.append(f"| `{sid}` {PKG.name_of(sid)} | " + ("; ".join(f"{k} ({n})" for k, n in parts.items()) or "the shell only") + " |")
    L += ["", "## Decided on 2 October", ""] + [f"- {x}" for x in m["decided"]] + [""]
    L += ["## Never configurable", ""] + [f"- {x}" for x in m["fixed"]] + [""]
    # client inputs
    wl_inputs = [e for e in di.active() if set(e.get("topic") or []) & {"branding", "configurability"}
                 and any(str(t) in ("global", "P01", "P02", "P05", "P13") or str(t).startswith(("P01/", "P02/", "P05/", "P13/"))
                         or re.match(r"^(WEB|GST|KSK|CMS)-", str(t)) for t in e.get("scope") or [])]
    wl_inputs.sort(key=lambda e: (str(e["source"]["date"]), e["id"]), reverse=True)
    L += ["## What the client said about white label", "",
          f"{len(wl_inputs)} design inputs from the meetings and design reviews on branding and configurability "
          "(`handoff/design-inputs/mom-design-inputs.yaml`), newest first. They win over this map where the two disagree; "
          "an open question is built to its stated default.", ""] + [di.line(e) + f" — {', '.join(map(str, e['scope']))}" for e in wl_inputs] + [""]
    L += ["## Sources", "",
          "- `contracts/satellite/white-label.yaml`: TenantConfig and every `set*` operation; `marketing-crm.yaml` for SEO and the cookie banner.",
          "- `screens/P13-white-label-cms.yaml`, `screens/P09-platform-admin-console.yaml`: where each is set.",
          "- `screens/P01-guest-web-storefront.yaml`, `P02-guest-mobile-app.yaml`, `P05-guest-kiosk.yaml`: where each is read.",
          "- `screens/_design-tokens.yaml` `whiteLabel`: which tokens a tenant may override.",
          "- `flows/F22`, `F102`, `F103`; ADR-0006 (tiered app distribution), ADR-0018 (configuration scope).",
          "- `handoff/design-inputs/white-label-map.json`: this map as data.", ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")


def main() -> int:
    global OUT_JSON, OUT_MD
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    import argparse
    ap = argparse.ArgumentParser()
    # A trial against notes not committed yet, written somewhere other than the live files.
    ap.add_argument("--notes", metavar="DIR", help="read the process design notes from DIR")
    ap.add_argument("--out", metavar="DIR", help="write white-label-map.json and WHITE-LABEL.md here instead")
    a = ap.parse_args()
    if a.notes:
        DS.set_notes_dir(a.notes)
    if a.out:
        o = pathlib.Path(a.out).resolve()
        o.mkdir(parents=True, exist_ok=True)
        OUT_JSON, OUT_MD = o / OUT_JSON.name, o / OUT_MD.name
    m = build()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    write_md(m)
    n_spec = sum(1 for v in m["guestScreens"].values() if v["specific"])
    print(f"white-label map: {len(m['elements'])} elements in {len(m['parts'])} parts; set on "
          f"{len(m['configScreens'])} screens; {n_spec} of {len(m['guestScreens'])} guest screens take more than the shell")
    return 0


if __name__ == "__main__":
    sys.exit(main())
