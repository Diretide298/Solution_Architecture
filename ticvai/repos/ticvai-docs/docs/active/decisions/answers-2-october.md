# Chinmay's answers to the open questions, batch 1 (2 October 2026)

> **The cited copy (2 October 2026, CHG-DOC-001).** Chinmay's answers log, copied into git from the audit
> working folder so the change entries and the decisions register (`docs/registers/decisions-2-october.md`)
> can cite it (`ticvai/CLAUDE.md` rule 12: every source cited is inside git). **Later sections override
> earlier ones.** The "Logged only, not applied" notes below describe the log as it was written; the
> decisions are applied by the CHG entries named in the register.

**Logged only, not applied.** Chinmay: "Log these for now, don't add anything. I'll answer the next batch."
They will be applied together, as CHG entries recording the decision and why, once the next batch is in.

| Ref | Question | Chinmay's answer | To apply as |
|---|---|---|---|
| POS-021 | Does every F&B order go to the kitchen before payment, or does quick service charge first? | Two configurations: one takes the bill (payment) first, the other sends first and charges after. | An outlet setting, "Payment timing": Pay first or Send first then pay. Refines R261 per outlet. |
| WEB-036 | Takeaway and delivery without an admission ticket, against DI-292 | Inside the venue, a ticket is needed. A restaurant outside the venue (standalone) can sell without one. | An outlet property, "Inside the venue (needs an admission ticket)" or "Standalone (no ticket)". |
| WEB-036 / GST-024 | Shared cart and one receipt, or the F&B order's own payment? | F&B has its own receipt. | The F&B order keeps its own payment step and receipt. DI-293's one receipt does not apply to F&B. |
| BO-045 | Who owns the F&B price — menu or catalogue? | **Corrected by Chinmay:** the split was deliberate, so the ticketing service can scale on its own. F&B prices were migrated into F&B, and the **F&B service has its own catalogue table**. The central catalogue (Venue Management) prices tickets and single-price booths; F&B outlets price from the F&B catalogue, and an outlet may set its own price. | Keep the menu's own price as F&B's catalogue price; fix the contract text that says "pricing and tax come from the catalogue variant"; record the reason (ticketing scales in isolation); check that BO-045 and the F&B screens read F&B's catalogue, not the central one. |
| POS-011 | Store credit tender | Gift card. | Store credit means a gift card issued at the refund amount (the default already). |
| CMS-005 | Dark guest app? | White label has no dark or light mode: the venue's chosen theme is applied. | Remove darkMode from the guest theme. |
| WEB-001 | Separate web and app home layouts? | We already have two wireframes the client approved. Only small changes; the rest is fixed. | The approved web and app wireframes are the layout; changes only where the spec breaks. |
| ADM-016 | May TICVAI staff publish a venue's site? | Yes if the site is hosted with us. Otherwise the venue can generate a package. | Hosted: platform staff may publish under a grant. Self-hosted: "Generate site package" (export). |
| CMS-014 | Does publishing go through the approval matrix? | A single publish: they simulate (preview), then publish, because they have the permission. Optional review steps would be good if the venue wants to set it up that way. | Simulate, then publish, for permission holders. An optional review/approval step the venue can switch on. |
| ADM-554 / ADM-508 | Who promotes AI models and publishes forecasts? | Depends on which module the AI model belongs to: whoever holds the permission. There are no default roles. When a role is created, the permissions are a checklist, with presets (all permissions, viewer, mid-level) but fully selectable. AI model publishing can be one of the checks, and the checks differ per module, so they are built for each module. | A role builder: a per-module permission checklist with presets (All, Viewer, Mid-level); a per-module "Publish AI model" permission. |
| ADM-049 | Price-list priority: does the higher or the lower number win? | Default. | "Higher number wins" (the default). |
| ADM-049 onward | Who uses the 410 workshop-pack screens on the TICVAI console (370 Commercial, 20 Catalogue lifecycle, 20 Rules and workflow)? | **They are venue screens.** | Move them to Venue Management (P08) and merge them with the venue's own screens (BO-008 product, BO-009 price matrix, BO-010 promotions, BO-011 bundles, and the rules and workflow screens), so one surface edits each record. TICVAI staff reach them only through a platform-staff grant (R098). |
| GST-055 (he wrote "GST 069") | Dynamic QR rotation step | 30 seconds. | 30 s. Confirm he meant the QR screen GST-055 and not the Face Pass screen GST-069. |

## BO-045, corrected by Chinmay (2 October)
The two prices are intentional:
- The F&B service owns its own catalogue table, so ticketing can scale as an isolated service.
- F&B prices were migrated into F&B.
- The contract's MenuItem text still says "pricing and tax come from the catalogue variant". That text is stale and gets corrected with this batch.
- The F&B process notes' correction asking to drop the menu's own price is withdrawn.

## Explanation for ADM-049 (which screens)
- 410 screens on the TICVAI Console (P09) were generated from the client's workshop packs:
  - Commercial: 370 (price list master, rate types, pricing command centre, promotions, bundles, coupons, upgrades and so on);
  - Catalogue product lifecycle: 20;
  - Platform rules and workflow: 20.
- They configure the same records the venue edits in Venue Management (P08): BO-009 price matrix, BO-010 promotions, BO-011 bundles, BO-008 product.
- The question is whether TICVAI staff use them on the console, acting for a venue, or whether they belong in Venue Management, merged with BO-008 to BO-011.

---

# Batch 2 (2 October 2026): the "next 50"
These answers are logged, not applied. Numbers refer to the list of 50 sent in chat. Anything Chinmay didn't name was answered "yes / recommended", so the default stands.

| # | Ref | Chinmay's answer | Applied as |
|---|---|---|---|
| 1 | ADM-037 (who pays for BYOK) | TICVAI keeps a selected range of models for each task. When a client brings its own key, the agent assigns the equivalent models from that provider. | With BYOK, the model is auto-mapped per task to that provider's equivalent from the curated range. Billing goes to the client's own key. |
| 2 | ADM-037 (may a client change the model) | No. A client could pick a cheaper model just because it's cheap, and that would break how the AI functions. | The client can't change the model per agent. TICVAI curates it. |
| 3 | ADM-520 | Recommended | TICVAI staff run the governance boards under a grant in release 1. |
| 4 | ADM-523 | Recommended | The contract's ten verbs, grouped under the minutes' five. |
| 5 | ADM-526 | Yes | Suggest 30 days; warn beyond 90. |
| 6 | BO-091 | The currency they select, shown with tokens. Default $. | The AI spend ceiling is in the tenant's selected currency (default USD), with tokens shown alongside. |
| 7 | BO-919 | All resource types. Models already in place improve with data. Also select the models now, with 3–4 options where available. | Forecast covers all requirement kinds. **Action:** pick 3–4 candidate models per AI task now, to form the curated range (ties to #1). |
| 8 | BO-927 | Correct | A coverage target; a person creates the shifts. |
| 9 | GST-031 | Yes | Floating button plus an entry on home. |
| 10 | GST-033 | Yes | Product detail, cart and booking detail. |
| 11 | GST-048 | Correct | Only this venue and date. |
| 12–15 | GST-054, WEB-008, WEB-044, loyalty (GST-036, WEB-043, BO-827) | Recommended | Defaults. |
| 16 | CMS-025 | "What is the cookie scanner?" | Explained below; waiting for his answer. |
| 17 | POS-027 | Yes | A banner, plus a supervisor override. |
| 18 | WEB-009 | Yes | Kept under "Past dates". |
| 19–25 | WEB-011, WEB-026, WEB-027, WEB-034, BO-020 (two), BO-021 | Recommended | Defaults. |
| 26 | BO-044 (bilingual outlet names) | Yes, where a country needs it: the local language plus English. | Outlet names in English, plus the local language where the region requires it. |
| 27–30 | BO-044, BO-048 | Yes / recommended | Defaults. |
| 31–32 | BO-065 ("B0165") | Default | Defaults. |
| 33–40 | BO-081, BO-1065, BO-110, BO-111, BO-136 | Yes / recommended | Defaults. |
| 41 | CMS-009 | Yes: three editors. Also the ability to set DNS, in case we missed it for the web app. The landing page is owned by the client, who redirects to us, but the domain should be there. Clients with no landing page can use templates we provide. | Three navigation editors. **Plus:** custom domain / DNS for the web app (already CMS-017; check it covers the guest web app). **Plus:** a landing-page template set offered to tenants without their own landing page. |
| 42–50 | EMP-058, EMP-062, GST-070 (two), KIT-005, KIT-007, KSK-017, POS-001, POS-013 | Yes / recommended | Defaults. |

## Cookie scanner (CMS-025): explanation sent to Chinmay
The cookie consent banner on the guest website has to list every cookie and tracker the site sets, by category: necessary, analytics and marketing. A cookie scanner is the tool that crawls the venue's website and finds them automatically. Ready-made scanners include Cookiebot and OneTrust.

CF-127 asked whether to buy one, build one, or have the venue upload a scan report by hand. The default drawn is the manual upload.

---

# Batch 3 (2 October 2026, by voice)
These are logged, not applied. The numbers refer to the batch-3 list of 46. Items 1–8 were answered individually; items 9–46 were then "accepted, or yes", so their defaults stand.

| # | Ref | Chinmay's answer | Applied as |
|---|---|---|---|
| 1 | POS-007 | The cashier may sign out, and the shift stays pending until the supervisor accepts. That must not stop the next cashier starting a shift. On the cashier's page it shows "Under review". At the end-of-day cash reconciliation, they go through each shift and reconcile it. | A pending shift never blocks the next shift on that till. The cashier's view shows "Under review". The daily cash reconciliation lists every shift and resolves them one by one. |
| 2 | POS-024 | Yes: mark the table out of service. | "Remove table" marks it Out of service. |
| 3 | POS-028 | Apply it now: change covers and change server. Hold table transfer until r2. | Change covers and change server in Block A; table transfer after r2. |
| 4 | POS-028 | No deposit unless the venue switches dining deposits on: good. | Default. |
| 5–8 | WEB-038, WEB-042 (×3) | That's good. | Defaults. |
| 9–46 | Finance, platform, ticketing (see the batch-3 list) | "Rest are accepted, or yes." | Defaults. ANL-023 is already decided: build all the charts. |
| 7 (batch 2) | AI/ML model selection | Not just AI/LLM models: ML models too (forecasting, analysis and the rest). Find the best-suited model for each task, plus 3–4 alternatives where they exist. | A research task (agent): a model per AI/ML task, best plus alternatives. |
| 16 (batch 2) | CMS-025 cookie scanner | Wants a cost analysis and an effectiveness analysis of building against buying. If building is better at lower cost, it's worth it. | A research task (agent). |
| 41 (batch 2) | DNS / custom domain | "Give me the options; I'll check them." Also check that CMS-017 covers the guest web app. | A research task (agent): domain/DNS options and a CMS-017 coverage check. |

## The rules branch's three decisions
| Item | Chinmay's answer | Applied as |
|---|---|---|
| CHG-SEED-005 (POS v2, "prevention: none") | No: there should be a prevention against a repeat. | Add a real prevention, e.g. a check that every difference in a wireframe candidate is either applied or has a decision ref. |
| CHG-SEED-012 (documents citing files outside git) | We can't cite anything outside git. We can have the files, but the HTML is final, and that is the input. | Copy the final council HTML reports (and ROOT-CLASSES) into git as the cited input; add check-cited-sources. |
| POS cart scope | Don't add guest-scoped cart operations. Keep the simplest. | The till's cart is the session's own cart. Correct the contract description and the check-subject rule accordingly. |

---

# Batch 4 (2 October 2026): the last Block A questions (35)
Logged, not yet applied.

| # | Ref | Chinmay's answer | Applied as |
|---|---|---|---|
| 4 | BO-188 (Face Tag retention) | Where needed, consent first, using a consent form from the venue. If we store the data, highlight or notify the venue that the client must accept a consent form. | Biometric capture and retention need the guest's consent, on the venue's own consent form. Where TICVAI stores the data, the venue gets a warning that consent is required. |
| (new) | Consent form builder | "Consent form builder in Venue Management." | **New requirement:** a consent-form builder in Venue Management, used by Face Pass/Face Tag, marketing and waivers. Check what already exists first (CMS-041 to 060 waiver form builder, CMS-022 to 024 consent configuration, BO-747) and extend or move it rather than duplicate. |
| 19 | ADM-018 | Yes: a venue can select its own language if needed. | A tenant can add or select interface languages beyond English and Arabic. |
| 23 | CMS-006 | Yes: the preview of the PDF ticket and the Apple/Google Wallet pass must be in Block A. | PDF ticket and wallet pass previews in Block A. |
| 24 | CMS-007 | All the customisation options we had in our wireframe. | Every customisation option in the approved wireframe/prototype, including the card count per section. |
| 25 | CMS-007 (scroll animations) | Same: it needs to be there. | Scroll animation (Rise, Scale, Slide, Blur, None) as a field. Contract gap, to be added. |
| 31 | CMS-104 | "Powered by TICVAI" as a configuration setting that can be toggled. | A toggle for "Powered by". Check it against the 14 August decision that "Powered by TICVAI" is shown consistently (DI-297): the toggle's default is on. |
| rest | 1–3, 5–18, 20–22, 26–30, 32–35 | "Rest yes, or default." | Defaults. |

**With this batch, every Block A question is answered.**

---

# Batch 5 (2 October 2026): selections, set 1
| Ref | Answer | Applied as |
|---|---|---|
| BO-036 | One screen (BO-036) | BO-127 is merged into BO-036 as one device register. |
| SGN-001 | Email plus one-time code | Prospect session; "Continue saved setup" signs in with a code. |
| ADM-122 | "The biggest challenge is migration or changes in the DB… suggest a better way, or the industry standard." | Industry standard (sent to Chinmay; default unless he objects): never merge or reverse-migrate production databases. Schema goes forward-only through versioned migrations, expand then contract. Configuration moves as a versioned package exported with stable keys, then a diff against production, approval, an idempotent upsert by key, and an audit record. Rollback re-applies the previous package. Secrets and environment settings never travel in it. |
| BO-1190 | No tax; an optional fee switch | Donations are untaxed; a tax or fee switch, off by default. |
| KSK-004 | **Tickets first** (not the recommended option) | The kiosk keeps tickets, then date and time, unlike the web and app. Supersedes REV3-2 for the kiosk only. |
| POS-000 | Accept all of v2 | Co-branding, recent cashiers, cashier-ID entry and the PIN/password switch become the spec (decision for check-candidate-decisions). |
| POS-003 | Accept v2 | As drawn. |
| POS-004 | Accept v2 | Section then seat; no hold extend, no recommendation, no booking-fee line. |

# Batch 5: selections, set 2
| Ref | Answer | Applied as |
|---|---|---|
| POS-012 | Accept v2 | Four order types: dine-in, quick service, takeaway and delivery (own fleet or partner). |
| POS-023 | Accept v2 | Lockers tab, refine chips and Scan; no inventory ledger on the till. |
| POS v2 file | Commit the file to git | Commit sources/designs/TICVAI_POS_Terminal_v2.html; remove it from .git/info/exclude and from the cited-sources baseline. |
| CMS-025 cookie scanner | **Buy a scanner API (hybrid)** | Our banner, runtime, registry and consent logs stay; a bought scanner API feeds recordCookieScan. **Also update the HLD/LLD** with the third-party scanner integration (Chinmay: "if we buy then the HLD or LLD will also change, note that and update those"). Redo the HLD/LLD after all the questions are answered. |
| Domains | Subdomain plus CNAME | venue.<cell>.ticvai.app for every tenant. A CNAME (tickets.venue.com) to our Front Door endpoint, with a managed certificate. A delegated subdomain as an option; the apex only on request; no path proxy. CMS-017 gains the missing DNS records, revalidation state and takeover warning, plus per-domain setup (UAE Pass redirect, Apple Pay domain, app links). |
| Foreign cash at the till | Base currency | Card and wallet refunds in the currency paid; foreign cash change and refunds in base currency (DI-282). |
| Journal reversals | Need approval | A reversal waits for a second approver. |
| CHG-FIN-006 prevention | Frontend comparison test | A test ticket compares the till, back-office and Analytics figures for the same period. |

**Sequence (Chinmay):** after ALL the questions are answered, redo the HLD/LLD (the cookie scanner and other changes), then Claude Design regenerates.

# Batch 6 (selections, set 3)

| # | Screen | Question | Answer |
|---|---|---|---|
| 171 | BO-039 | May a supervisor approve an out-of-tolerance opening float remotely from the back office, or only at the till? | Back office too |
| 172 | BO-039 | Allam asked to explore merging shift-closing and till-closing screens; is BO-039 also the place for BO-040's list? | Keep both |
| 173 | BO-040 | If no supervisor is available, may the cashier log out with the variance logged for later review? | As POS-007: cashier signs out; shift pending ('Under review'); next cashier can start |
| 174 | BO-040 | Must the variance be accepted on the same till the shift was counted on, or any till at the venue? | Any till, with supervisor PIN |
| 175 | BO-040 | The client asked that a supervisor can reject a variance so the cashier recounts and resubmits; the contract has accept only (reopen is the way back). Is reject | Add Reject + recount (DI-804) |
| 176 | BO-040 | Which screen shows the denomination breakdown of the closing count for review (no read returns the count lines)? | Add a read for the count lines |
| 177 | BO-041 | Should a lift or add be recordable from the back office at all, when the cash is at the till? | Yes: supervisor entry with mandatory reason |
| 178 | BO-042 | How does the cashier sign as witness — PIN step-up on the same device, or named only? | PIN on the same device |
| 179 | BO-042 | Where is the drawer ceiling configured, so the screen can flag boxes over it? | Add drawer limit setting (warn + offer cash lift) |

# Batch 6 (selections, set 4)

| # | Screen | Question | Answer |
|---|---|---|---|
| 180 | BO-046 | Does the back office advance tickets at all, or only watch and prioritise? And with Allam's position that Softlabs need only an integration point to an existing | Watch + prioritise only |
| 181 | BO-104 | Should the F&B hub show F&B takings rather than venue takings, and drop admissions? | F&B takings (admissions dropped) |
| 182 | BO-104 | Is BO-104 or BO-727 (F&B Command Center) the F&B landing? | BO-104 is the landing hub; BO-727 is a card on it |
| 183 | BO-109 | Is the till layout per outlet (DI-326) or per workstation (Workstation.saleBoard binds a board to a till, MATRIX 2.1.9)? Can two tills in one outlet differ? | Per outlet, with a till override |
| 184 | BO-109 | Which system functions may be placed on an F&B till grid (DI-157 lists ticket list, reservation list, transaction list, media lookup)? | F&B functions only |
| 185 | BO-112 | Is the printed prep sheet a browser print of the station view, or does it need a print operation and template? | A print template (kitchen printers and browser) |
| 186 | BO-113 | Is the commissary a kind of outlet (DI-330 outlet-level model) or a kitchen shared by outlets as FNB-1H draws ("Main Kitchen linked to 3 outlets")? | The commissary is an outlet that produces for others |
| 187 | BO-134 | Are kitchen printers in the first release, and which models? The hardware list still says "decide later" for kitchen displays and printers. | Kitchen printers in release 1 |

# Batch 6 (selections, set 5)

| # | Screen | Question | Answer |
|---|---|---|---|
| 188 | BO-134 | Can one kitchen serve several outlets (FNB-1H "Main Kitchen linked to 3 outlets") when the model is per outlet? | Yes: via a producing outlet (one kitchen outlet produces for several) |
| 189 | BO-135 | Is per-item routing with display fallback enough for r1, or do we owe category rules and a fallback station (DI-323 is client-requested)? | Item routing + category rules + fallback station (DI-323) |
| 190 | BO-135 | Where does an item with no station go - refused at Send to kitchen, or to a default station? | A default station named per outlet |
| 191 | BO-137 | Is "probable cause" (re-fires logged, trim yield, breakage) wanted in r1, and from which data? | No cause column; link to waste and production for the period |
| 192 | BO-139 | Does waste above a value need approval (FNB-5E draws AED 100 / 500 / 2,000 bands and photo evidence above AED 500)? R144 lists recounts and retail returns, not  | A waste-approval POLICY the venue can switch on or off (value bands + photo when on) |
| 193 | BO-140 | Should a temperature breach automatically 86 the dishes that depend on that unit (FNB-5J "auto-86 on safety breach")? | Suggest, don't auto: the breach banner offers '86 affected items' |
| 194 | BO-140 | Are daily counts ("6 left") with automatic 86 at zero in scope (FNB-2H "Count set")? No operation sets a count. | Yes: add daily counts; sold-out automatically at zero |
| 195 | BO-142 | Is a discount or price-override limit an amount or a percentage? | Both: the venue chooses percentage or amount per limit |

# Batch 6 (selections, set 6a)

| # | Screen | Question | Answer |
|---|---|---|---|
| 196 | BO-729 | Where are outlet type and department stored? The outlet has kind and cost centre only. | Add both fields: outlet type and department (DI-319) |
| 197 | BO-731 | How is a late-night window that crosses midnight (23:00–01:00) entered? OpeningHoursWindow states no overnight rule. | One window past midnight, marked 'ends next day' |
| 198 | EMP-003 | Which roles are the restaurant roles on the staff app (host, server, captain or supervisor), and which of the restaurant destinations does each see? | Host and Server variants; a supervisor sees both |

# Batch 6 (selections, set 6b)

| # | Screen | Question | Answer |
|---|---|---|---|
| 199 | EMP-008 | Does a server without a till get a shift summary (covers, sales, tips), and from which source? | Yes: a service summary (covers, tables, sales, tips) |
| 200 | EMP-009 | Does a server on a handheld ever hold cash (a payment taken in cash at the table on EMP-059), and if so, against whose drawer? | No cash on handhelds; cash goes to a till |
| 201 | EMP-052 | Does "Table closed" persist after payment until someone resets the table (which acts like the cleaning status DI-336 excluded), or does a paid table go straight | A short 'Table closed' state, then 'Make available' |
| 202 | EMP-052 | When does a table show Reserved, given the host normally allocates the table at seating (DI-689)? Options: only when the booking names a table, or from N minute | Reserved when a booking names the table, or N minutes (venue-set) before a pre-allocated booking |

# Covered by earlier decisions

| # | Screen | Question | Answer |
|---|---|---|---|
| 206 | KSK-016 | Are F&B kiosks only inside the gate? A kiosk outside would sell food without admission (DI-292). Do food and tickets bought together at a kiosk go on one receip | From earlier decisions: kiosks inside the venue need admission; F&B keeps its own receipt |
| 212 | ADM-619 | The 12 August minutes say monthly file reconciliation; the contract decided daily per venue. Confirm daily. | Already decided: daily per venue |

# Batch 6 (selections, set 7)

| # | Screen | Question | Answer |
|---|---|---|---|
| 203 | EMP-053 | Is the floor-plan editor meant for a phone at all, or a tablet or back office only? | Tablet (landscape) + back office; read-only on a phone |
| 204 | EMP-055 | Should a booking capture seating-area preference (indoor, terrace, majlis) and the occasion? The waitlist has seatingPreference and the reservation does not. | Add seating preference and occasion as fields |
| 205 | EMP-060 | Which restaurant measures does the client want on the staff app (turn time, no-show rate, covers, wait accuracy), and are they computed by reporting or on the d | All four (turn time, no-show, covers, wait accuracy) from reporting |
| 207 | ADM-068 | Who uses ADM-068, TICVAI staff maintaining jurisdiction templates, or tenant finance administrators? | TICVAI staff maintain country tax templates; tenants run VAT returns and invoices in VM |
| 208 | ADM-068 | The aiInsights field on the summary, is it in phase one, given AI-assisted finance reporting is phase two? | Leave the AI panel out of phase one |
| 209 | ADM-411 | Which record holds the invoiced company (billing entity) and its TRN certificate? | A new billing-entity record in the subscription contract |
| 210 | ADM-411 | Which document types are mandatory per country (trade licence, VAT certificate)? | Trade licence always; VAT certificate when a TRN is entered; configurable per country |
| 211 | ADM-619 | Whose settlements does this platform screen show, TICVAI's own payment orchestration across tenants or one tenant's? | Cross-tenant ops view: amounts per tenant, no guest data |

# Batch 6 (selections, set 8)

| # | Screen | Question | Answer |
|---|---|---|---|
| 213 | ADM-626 | Do settlement postings happen automatically after reconciliation, or through this release gate? | Automatic when fully matched; the screen shows status and held days |
| 214 | ADM-628 | Is the reconciliation simulator and AI advisor in phase one, given AI finance reporting is phase two? | Actuals now; forecast and advisor drawn but switched off |
| 215 | BO-043 | Daily per venue (R110) against the weekly or monthly runs in the 12 August minutes. Is a monthly roll-up also needed? | Daily per venue, plus a month view listing the days |
| 216 | BO-076 | POS sales recognise immediately (12 August) but rules are per product kind, not per channel. How is a POS-sold dated ticket treated? | By the product kind's rule (a dated ticket is recognised at admission) |
| 217 | BO-1081 | Is Gross sales shown excluding VAT, and are service fees inside it or a separate line? | Excluding VAT; fees on their own line with a footnote |
| 218 | BO-1081 | What is the pack's "Attraction" filter in scope terms (a scope node below venue, or a product category)? | Product category (venue + category filters) |
| 219 | BO-1081 | Does BO-1081 stay as its own P08 screen (DI-260) or become the Finance standard dashboard in P16 opened from Orders & Money (DI-721)? | One P16 [Venue Analytics] Finance dashboard; Orders & Money shows a link card |
| 220 | BO-1170 | Which wallet-specific checks join the period-close checks, and does a wallet movement summary operation get added? | Add a wallet movement summary operation and wallet pre-close checks |

# Batch 6 (selections, set 9)

| # | Screen | Question | Answer |
|---|---|---|---|
| 221 | BO-1172 | Which approval inbox does the finance approver use to decide a period close? | The approvals inbox, with a deep link to the close checks |
| 222 | PTR-014 | Does PTR-014 survive next to PTR-013, PTR-046 and PTR-017, or merge into PTR-046? | Keep as the partner's Payments summary |
| 223 | SGN-020 | Is the billing entity saved on the onboarding application (public) before verification? | Yes: saved on the application; nothing provisioned until verified |
| 224 | PTR-002 | POS-style reseller interface, website-style portal, or both per customer? | Wireframe both; decide after review |
| 225 | ANL-070 | Which operation will hold analytics governance policies (masking, export restriction, retention, sharing, AI and API access)? | Add a governance policy operation (masking, export, retention, sharing, AI/API access) |
| 226 | BO-144 | Over what period are Failed scans, Overrides and Security alerts counted - today since the venue day start, or a rolling window? | Today since the day start, with the delta against the same time last week |
| 227 | BO-146 | What are the security classification levels for a zone? | Public / Restricted / Secure / Critical (renamable) |
| 228 | BO-147 | What should an access point do when its attraction is temporarily closed - deny, offer a virtual queue return window, or refer to an operator? | Deny + reopening time + a virtual-queue return window where enabled |

# Batch 6 (selections, set 10a)

| # | Screen | Question | Answer |
|---|---|---|---|
| 229 | BO-152 | When two calendar entries overlap (a holiday inside a season, a private event on a free-entry day), which wins? | The venue sets a priority per entry |
| 230 | BO-153 | Who approves a topology publication, and must the approver differ from the author? | A policy the venue switches on/off (second-person approval when on) |
| 231 | BO-157 | Does a journey rule apply to every product, or should it name the products or admission profiles it covers? | An 'Applies to' picker: venue-wide by default, or chosen products/profiles |
| 232 | BO-159 | Do time-bound product entitlements (e.g. 60 minutes from first scan) belong to this engine? | Yes: add time-bound entitlements (validity from first scan) |

# Covered by earlier decisions (2)

| # | Screen | Question | Answer |
|---|---|---|---|
| 233 | BO-165 | Is the refresh interval in the 15-60 s range of the pack, or the 6-12 s the client mentioned for beacon-activated codes? | From GST-055: 30 s default; offer 15/30/45/60 and custom (5 s minimum) |
| 275 | BO-772 | May guests who checked out without an account receive marketing? | From WEB-011: marketing only with the ticked opt-in; nothing sent without it |
| 276 | ADM-044 | Is a guest-checkout opt-in sufficient marketing consent? | From WEB-011: the checkout opt-in, unticked by default, recorded with source checkout |
| 282 | CMS-027 | Is an opt-in ticked at guest checkout sufficient marketing consent under PDPL? | From WEB-011: as above |
| 308 | ANL-001 | Does Gross sales include VAT and fees? | From the finance decisions: excluding VAT (D-185 default) |
| 317 | ANL-008 | DI-280 says data-dependent forecasting cannot be delivered in phase one; the 29 Sep design ships a baseline-first forecast with maturity stages. Which applies t | From the 30 Sep decision: baseline-first forecast with maturity stages |
| 318 | ANL-009 | DI-278 makes AI-assisted finance reporting phase two. Should finance-ledger questions (deferred revenue, journals) be refused in phase one? | From ADM-068: AI finance reporting in phase two; ledger questions answer 'not available yet' |
| 351 | ANL-062 | Which finance KPIs ship (gross sales, net revenue, recognised and deferred revenue, refunds) and with what formulas? | From CHG-FIN-007: finance KPIs seeded with formulas (D-185 default, client sign-off pending) |
| 354 | BO-059 | Does net revenue here include VAT? | Excluding VAT |

# Critical set 1

| # | Screen | Question | Answer |
|---|---|---|---|
| 236 | BO-186 | May Face Pass be enrolled at a self-service kiosk or at the turnstile on first use, as the MoM records, or only at the app and the two counters, as the contract | App + staffed counters + self-service kiosk (consent shown); not the turnstile |
| 237 | BO-187 | Are children's faces enrolled at all, and if so with guardian consent only - and from what age is a guest a minor per jurisdiction? | Guardian consent on the venue's form; minor age per country; the venue can switch minors off (supersedes the GST-069 default) |
| 239 | BO-190 | May the reviewer see the enrolled face and the new capture side by side, or only references and the match result? | Images behind 'View images (logged)', needing a specific permission; score and references always visible |
| 240 | BO-192 | What are the lawful retention periods per data category and region? | Research UAE/GCC law and propose defaults per category, marked 'pending counsel' |
| 241 | BO-196 | Does adding an access device need an approval step and a secure enrolment code, as the 15 September minutes ask? | Secure enrolment code + pending approval |
| 245 | BO-203 | Who approves a device into production (Approved stage), and is it a separate person from the one who tested it? | Approver must differ from the tester |
| 254 | BO-229 | Which actions need supervisor or security approval (blacklist, whitelist, permanent disable)? | Second approver for permanent locks, whitelist, and releasing identity/permanent locks; none for 'until end of day' |
| 255 | BO-230 | Can a gate's direction be switched live (Entry to Exit), as the client asked on 2 Sep? | Live direction switch with permission, logged; R221 amended |
| 260 | BO-247 | Which locks need dual authorisation to release (the pack says "potentially" for high-risk locks)? | As BO-229 |
| 261 | BO-248 | May a security reviewer see the enrolment photos for a face change, or only match scores and references? | As BO-190 |
| 283 | CMS-029 | Children's biometric data - exclude entirely, or allow with a guardian-signed consent? | As BO-187: guardian consent, configurable |
| 426 | BO-471 | Is a maximum offline duration needed, after which the reader refuses offline taps? | Yes: the venue sets a maximum offline duration; readers then refuse offline taps |
| 459 | BO-629 | How long are rejected and superseded document files kept? | As BO-192: research-based defaults, pending counsel |

# Critical set 2

| # | Screen | Question | Answer |
|---|---|---|---|
| 266 | BO-336 | Which status list is authoritative for the Virtual Ticket - the pack's 13 or the entitlement model's 6 plus the suspended flag? | Map the pack's 13 names onto the model; add any missing states |
| 267 | BO-336 | DI-670 lists entitlement statuses active, reserved, consumed, transferred, expired, refunded/cancelled; the ticket lifecycle has no Reserved. Is Reserved the sa | As BO-336: Reserved maps to Pending fulfilment |
| 302 | EMP-071 | What does the handheld do offline at the rental counter? All 30 staff-app rental screens have the offline state as TODO. check-out, equipment assignment, inspec | Offline: check-out of bookings already loaded, with a cash deposit or supervisor approval; returns queue |
| 304 | EMP-078 | How is the card hold taken and linked? The check-out carries the amount and method but no authorisation reference; the booking has depositAuthorisationId with n | Pre-authorisation on the payment terminal; the reference is stored on the booking; check-out blocked until it succeeds |
| 306 | EMP-097 | On a partial group return, is part of the deposit released now, or is the whole hold kept until the last unit is back? | Hold the whole deposit until every unit is back |
| 307 | EMP-098 | Is usage beyond the paid time charged at the normal rate (DI-499 - a wheelchair paid for one hour and used for three is charged two extra hours) or at the late- | Normal rate (DI-499) |
| 457 | BO-627 | Which third-party identity or government verification services are in scope (for example UAE Pass or ICP checks)? | UAE Pass + ICP integrated in release 1 (needs client access) |
| 530 | EMP-027 | For critical incidents, may the person who completed the corrective action also close the incident (the pack's segregation of duties)? | Another supervisor must close a critical incident |
| 537 | EMP-047 | Does declaring a staff emergency also need a second person, as the guest evacuation does? | Single declarer with a typed confirmation; second person only on the guest broadcast |

# Critical set 3

| # | Screen | Question | Answer |
|---|---|---|---|
| 368 | ACC-006 | Which reviewer surface survives, the P11 reviewer screens (ACC-006, ACC-007) or the P08 board (BO-635, BO-636)? | One queue and workspace component used in both P11 and P08 |
| 397 | BO-427 | Does an all games pass cover attractions added after it was sold? | Venue configures; default yes (type-based passes cover new games) |
| 410 | BO-440 | Does the retry offer appear before the game ends (pack) or after it (DI-877), and does a retry consume an entitlement play? | Retry charged in money at the retry price; offered in the last seconds of play and a short window after |
| 461 | BO-631 | Is face matching legally enabled for accreditation duplicates? | Only where the venue enables it, with applicant consent and the venue's legal sign-off; off by default |

# Non-critical questions: defaults (Chinmay, 2 Oct: "show me only critical")
Every question not asked in the critical sets takes its drawn default: 271 on Block C and D screens. Each stays reviewable in the workbook (answer "Default (non-critical)"), and Chinmay can still overrule any of them before its block is broken into tasks.

# AI residency (Chinmay, 2 Oct): per-tenant residency class
| Class | Small tier | Strong tier | Fallback |
|---|---|---|---|
| UAE-only (the default; mandatory for government, bank and health tenants) | Core42 Compass GPT-4.1 mini, or Seraj if it wins the Arabic golden set | Compass GPT-5 | OpenAI UAE, then in-cell gpt-oss-120b |
| Global allowed (private venue opts in under PDPL Art. 23: vendor contract, DPIA and notice) | Azure gpt-5-mini Global, or the tenant's BYOK provider | Azure gpt-6-sol Global | The UAE-only chain |
| On-prem | Qwen3.5 or gpt-oss | Qwen3.5-122B; Falcon-H1 Arabic or Jais 2 | — |

Move the UAE-only Small tier to Azure UAE North PTU (spillover off) when steady traffic nears about 100,000 calls a day.

This amends AI-D02 (Compass is the provider for UAE-only tenants, through `openaiCompatible`) and adds a per-tenant residency class. It needs an ADR amendment plus HLD/LLD updates.

To get in writing before signing: Core42's terms (retention, logging, sub-processors, minimums), OpenAI UAE approval, Microsoft's PTU calculator figures, and legal advice on whether Miral and Dubai Holding count as government entities.

Source: `docs/active/research/ai-ml-model-selection-2-october.md`, section 2A (copied into git when applied, 2 October: CHG-DOC-001).

# PII scrubbing (Chinmay, 2 Oct): "we may need to scrub personal info no matter what: an offline NLP-based scrubber or censorship"
**Decision:** every LLM call, whatever the tenant's residency class, goes through an offline scrubber inside our cell first:
1. **Detection.** Microsoft Presidio (open source, offline), with custom recognisers for Emirates ID, UAE phone numbers, passports, IBANs, Luhn-checked card numbers and email, plus an Arabic NER model (e.g. CAMeL Tools) for Arabic names and places.
2. **Reversible tokens.** Detected PII is replaced by placeholders ([GUEST_1] and so on). The map stays in-cell, and replies are re-filled before they reach the user.
3. **Moderation.** An offline guard model (Qwen3Guard, which covers Arabic) runs on both input and output.

This reinforces the existing rule that the LLM never reads raw data (the AI ADRs). Apply it as an ADR amendment and in the AI gateway contract (scrubbing is mandatory, not tied to residency), the HLD/LLD and the AI tasks.

# Door follow-ups (2 Oct)
| Item | Answer | Applied as |
|---|---|---|
| selectRole for partners | Yes, add partner | Partner added to the audience of identity.selectRole (additive). |
| Session.saleBoardId required | Make it optional; log the breaking change | An entry in docs/active/breaking-changes.yaml with Chinmay's approval; only till sessions carry it. |
| Operator's own MFA and sessions | Add "My account & security" | A new console screen for a platform operator's own MFA methods and sessions. |

# Pre-apply round (2 Oct)
| Item | Answer | Applied as |
|---|---|---|
| Supervisor shift close | POS-007 plus the daily reconciliation | closeShift is declared on POS-007 (supervisor PIN, any till) and in the daily cash reconciliation. |
| Roles | "Default permission configs, so to speak. We still have checklists: if they select Viewer, for example, they can still give that viewer more permissions and rename it." | The seeded roles become preset permission configurations (All, Viewer, Mid-level, …). Picking one fills the per-module checklist, which stays editable, and the role can be renamed. No fixed default roles. |
| Theme.darkMode | Deprecate it and ignore the field | Kept for compatibility, marked deprecated, never used or drawn. |
| Compat rule `security_widened` | Approved | Adding an accepted credential is additive. |
| Console R098 (about 66 screens) | Add a tenant picker and grant | The ADM-412 pattern: pick the tenant, a time-boxed grant with step-up, a grant panel. Venue-owned screens move to VM (as ADM-049). |
| Duplicate screens | Merge as proposed | One screen per job; the merged ids are kept as anchors. |
| "Powered by TICVAI" | A toggle, default on | Shown unless the venue's licence allows switching it off. |
| listGuestMemberships | Keep it for staff and partner use | Bound to the membership admin screen as a staff-facing operation. |
| POS-025 shiftId parameter | (lead) Read the shift on load with getWorkstationShift; drop the navigation parameter | — |

# Contract follow-ups (2 Oct)
| Item | Answer | Applied as |
|---|---|---|
| New permission values | Count as additive | check-contract-compat: adding a value to the Permission enum is additive, as security_widened is. Add the 20 permissions: per-module AI publish (replacing AI_APPROVE for model publishing), BIOMETRIC_IMAGE_VIEW, ACCESS_DIRECTION_SET, REPORT_GOVERNANCE_MANAGE. |
| BYOK providers | "Why just Mistral? As long as we get an API key it can be any model; we just need to store it correctly." | BYOK accepts any provider. The key is stored in Key Vault, per tenant, encrypted and never shown again. Native adapter or OpenAI-compatible. The curated task-to-tier mapping picks that provider's equivalent model, with a compatibility test before activation. |
| Cookie scan consent state | Add now | Each finding records the consent state it was seen in, plus a platform-wide catalogue of known cookies. |
| BO-007 bulk edit | A new catalogue operation | catalogue.bulkUpdateProducts is added; the inventory one is deprecated and retired at the next major version. |
| Response enum values (spine agent) | (lead) Keep the additive fields | No breaking enum additions. |
| Workshop-pack console gaps | (lead) Defer them to the ADM-049 move | — |


# Lead decisions on the follow-up agent's questions (2 Oct)
- BC-006/BC-007 approved: per Chinmay's follow-up, model publishing moves from AI_APPROVE to the per-module AI publish permission (no tickets started).
- The platform cookie catalogue is curated under PLATFORM_PLAN_MANAGE, the permission for the platform's other catalogues.
- AI_USE stays the base permission for the publish operations; the module permission is checked on top of it.

# Lead decisions on the commercial-move questions (2 Oct)
- **Corrected by Chinmay (2 Oct): the 13 duplicate first-release setup operations are retired in r2**, not at the next major version. Their screens bind the venue screens' typed operations instead. The removals are logged as approved breaking changes against r1. Their 13 pushed tickets are retired in the r2 push, each naming the ticket that replaces it (no work has started).
- ADM-068 (country tax templates) and ADM-619 (cross-tenant payments) stay on the TICVAI console (DEC-207, DEC-211) and take the R098 pattern.
- DEC-168: a new console screen, "Configuration promotion", binds the export/diff/applyConfigPackage operations. ADM-122 stays in Venue Management for product import and export.
- CHG-MOV-004: check-screens gains a rule that a screen name carries no tab character or trailing page number.

# Flow design briefs before Claude Design (Chinmay, 2 Oct)
After the re-audit and before Claude Design, every flow gets a design brief (one agent per process, Block A first). Each brief covers:
- every input artefact, with its formats, limits, validation and errors;
- what the system does with each input;
- every output, its states and failure branches;
- what moves or animates, and how;
- its sources.

Example: the venue map takes DXF/DWG, PDF (OCR), PNG with hand-marked paths, or GLB plus pathway metadata. It animates the route line along the paths, the position dot, the camera follow and the 3D↔2D transitions.

Claude Design then works per process: the flow storyboards first, then the single navigable wireframe per app.

# Claude Design and HLD/LLD order (Chinmay, 2 Oct)
Block A first: finish ALL Block A wireframes (flow briefs, then storyboards, then the navigable wireframes for the Block A apps: Guest Web, Guest App, POS, Kitchen Display and the Block A screens of Venue Management, the CMS and the console) and the HLD/LLD first. Then Blocks B, C and D.
