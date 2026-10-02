# Cookie scanner (build or buy) and tenant domains: research, 2 October 2026

> **Research for Chinmay. It does not make a decision, and it does not edit any contract, screen or register.**
> Part A prices the cookie scanner three ways (buy, build, hybrid) and recommends one. Part B lists the
> domain options for tenant guest web apps and says what CMS-017 is missing.
>
> **Package sources read:** `screens/P13-white-label-cms.yaml` (CMS-017, CMS-018, CMS-025), `screens/P08-*.yaml`
> (BO-835), `flows/F103-*.yaml`, `states/custom-domain.yaml`, `contracts/satellite/marketing-crm.yaml` (cookie
> registry, banner, runtime, scan intake, scan policy), `contracts/satellite/white-label.yaml` (domain operations,
> `CustomDomain`, analytics providers, site-setup presets, `embedMode`), `contracts/spine/tenancy.yaml`
> (`resolveTenantHost`, `setTenantDomainMapping`, `TenantDomain`), `contracts/spine/identity.yaml`,
> `docs/registers/conflicts.md` (CF-127), `docs/active/bl-073-cookie-consent-20-september.md`,
> `docs/active/infra-answers-30-september.md`, `handoff/hld-lld/TICVAI-HLD.md` and `TICVAI-LLD.md`, and the design notes
> `handoff/design-notes/customer-marketing.yaml` (CMS-025, CMS-026) and `white-label.yaml` (CMS-017).
>
> **Labels.** Figures marked **(est.)** are my estimates, and each one states its assumption. Vendor prices are
> list prices taken from the vendors' pages on 2 October 2026 unless another date is given. Sources are at the end.

---

## Summary

**A. Cookie scanner.** Build our own scanner, provided the client expects about 75 or more tenant domains within three
years. The platform is sized for 200 tenants. If the client expects fewer than about 50, use the hybrid and buy a
scanner API. The question is now only the scanner. The banner, runtime, registry, consent logs, scan intake and scan
schedule were all decided on 29 September as ours (`x-ticvai-requires-module: core`, "decided 29 September, build").
`recordCookieScan` is the point where either choice plugs in, so the scanner decision can be reversed cheaply.

- **Cost.** The three-year cost of building is about $66k–79k (est.) and barely changes with the number of tenants.
  Buying a full CMP such as Cookiebot costs more than building from about **30** domains. A Cookiebot-class
  scanner-only subscription costs more from about **75** domains. The cheapest scanner API (CookieScript) costs more
  only from about **275** domains. At 10 domains, building costs about $40k more than CookieScript over three years.
- **Effectiveness.** Building is more effective on TICVAI's real risk. It can walk the booking and checkout journeys,
  test each page in the three consent states (no decision, reject all, accept all) so that it proves our own blocker
  works, keep all processing in UAE North, and list the mobile SDKs. Vendor scanners crawl public links and do none of
  these. The vendors' advantage is their categorisation database. That gap is smaller here than CF-127 assumed,
  because TICVAI ships the page itself and tags arrive through only four doors. Only one of those doors, Google Tag
  Manager, is open-ended.
- **Two contract gaps either way.** A scan finding cannot record which consent state it was seen in, so a scan cannot
  prove that a cookie was set before consent. There is also no platform-level catalogue, so every tenant would
  classify `_ga` again (A9).

**B. Domains.** CMS-017 does cover the guest web app domain (`kind: guestWeb`). Its model does not match the edge that
was decided (Azure Front Door Premium):

- Front Door validates ownership only by a TXT record (`_dnsauth.<host>`). The contract offers `dnsTxt`, `cname` and
  `httpFile`.
- The tenant has to publish two or three records. The contract holds one.
- There is no state for *pending revalidation*. That state is the weekend-outage case the contract itself warns about.
- CMS-017 does not show the platform subdomain, does not mark one domain as the primary, and does not list the
  checks each domain needs before go-live: UAE Pass redirect, Apple Pay domain, app links, scan policy.

**Recommended default for domains:**

- Every tenant gets a platform subdomain under a separate registrable domain, with one stem per cell. Example:
  `coastalaqua.ae.ticvai.app`.
- A client who has a landing page publishes a subdomain of their own, such as `tickets.venue.com`, as a CNAME
  pointing straight at our Front Door endpoint. Validation is by TXT record, and Front Door manages the certificate.
- Delegating that subdomain to our name servers is an option for clients who want no DNS work.
- An apex domain only on request.
- We do not offer reverse-proxy paths (`venue.com/tickets`).

---

# Part A: Cookie scanner, build or buy

## A1. What is already decided, which narrows the question

CF-127 (18 August) framed the choice as "build, buy or drop" for the whole of cookie consent. BL-073 (20 September)
split it into six pieces and recommended **"Buy the scanner. Build the rest."** The contracts written on 29 September
did the "build the rest" part. In `marketing-crm.yaml` every cookie operation is
`x-ticvai-requires-module: core # cookie consent is the law on every storefront, licensed marketing or not
(decided 29 September, build)`:

| Piece | Operation(s) | Owner today |
|---|---|---|
| Registry (CMS-025) | `listCookieTrackingDigital`, `setTrackingTechnology` | ours, built |
| Banner and preference centre designer (CMS-026) | `listCookieBannerPreference`, `setCookieBannerDesign` | ours, built |
| Runtime the loader enforces (blocking, consent mode) | `getCookieConsentRuntime`, `listPublishedTrackingTechnologies` | ours, built |
| Device consent log, history, claim at sign-in | `recordDeviceConsent`, the evidence list, `claimDeviceConsent` | ours, built |
| Analytics injection that waits for consent | white-label `listAnalyticsProviders`, `setAnalyticsProvider` | ours, built |
| Scan intake, scan history | `recordCookieScan`, `listCookieScans` | ours. **Who calls it is CF-127's open question** |
| Scan schedule and alert recipients | `listCookieScanPolicies`, `setCookieScanPolicy` | ours |

**So only one thing is left to decide: what produces the payload that `recordCookieScan` accepts.** The contract says
so: *"Whoever scans (a bought scanner through a service credential, our own crawler, or an administrator uploading a
report) posts the same payload, so CF-127's buy-or-build answer changes who calls this and nothing downstream."*
`CookieScanRun.source` already has the enum `boughtScanner | ownCrawler | manualUpload`.

**One consequence for "buy":** buying a full CMP now means running a second banner, a second consent log and a second
blocking script beside the ones already designed, and syncing the two. BL-073 §3 already ruled that a consent record
for an identified guest *"may not hold the only copy"* in a vendor. A full CMP would therefore need integration work
on top of its licence, and it would replace parts of the work already decided. Those costs are counted below.

## A2. What the scanner has to do for TICVAI

From the matrix rows (2.6.57 automatic scanning with administrator alert, 2.6.64 scan schedules, 22.13.10 websites
and mobile apps) and from the registry's six governed channels:

| Surface | What carries tracking technology there | Can a vendor link-crawler see it? |
|---|---|---|
| Guest web (`b2cWebsite`, `whiteLabelSite`, `customerPortal`) | Our code. The four analytics providers (`googleAnalytics4`, `adobeAnalytics`, `metaPixel`, `matomo`). **Google Tag Manager containers** (anything the tenant puts in them). `embed` content blocks (YouTube, maps, social). Payment-provider scripts and 3-D Secure iframes. | Public pages, yes. **The booking flow, the cart, checkout and signed-in pages, mostly no**: crawlers follow links and do not complete a booking. |
| Embedded checkout (`embeddedCheckout`, `BookingFlowConfig.embedMode: embedded`) | As above, inside the client's page | Only if the scanner crawls the client's site |
| Mobile app (`mobileApp`, P02) | SDKs compiled into the app | **No.** No browser scanner reaches a native app |
| Partner microsites | As for guest web | Yes, public pages |

**Most of the surface is known in advance.** TICVAI renders the page, and tags enter only through four doors: our
code, a closed list of providers, GTM containers and embed blocks. GTM is the only open-ended door, and it loads only
after the visitor grants its category (`StorefrontAnalyticsProvider.consentCategory`). **A scan has to run in the
accept-all state to see what GTM injects.** The same constraint means one platform catalogue of perhaps 50–150
technologies (est.) covers most of what any tenant will ever load. This is why the *"the database is forever"*
argument in BL-073 §2 is weaker for TICVAI than for a generic website.

## A3. Buy: the vendors

| Vendor | Scanning | Auto-blocking | Categorisation | Consent logs | Multi-tenant / multi-domain licensing | Arabic / RTL | API / headless use | Data residency | List price |
|---|---|---|---|---|---|---|---|---|---|
| **Cookiebot** (Usercentrics) | Monthly automatic. Daily is an add-on (+€99/month) | Yes (auto-blocking script) | Proprietary database. Scan reports results within 24 h of adding a domain group | Yes | **Per domain.** Domain groups share one CBID. Reseller programme: wholesale (reseller owns the domain groups) or retail. 20% wholesale discount at ≤€750 MRR | Arabic among 48 template languages. RTL rendering not documented in what I found | On-page JS API. **Data API to extract cookie details per domain group.** No full provisioning REST API (per a third-party summary, unverified) | EU (Germany/Denmark) | Free (1 domain, 50 subpages). Premium Lite €7. **Small €15, Medium €30, Large €50, XLarge €90 per domain per month** (subpage tiers ≤350 / ≤3,500 / ≤7,000 / >7,000). Usercentrics Advanced: quote, billed by sessions, unlimited domains |
| **OneTrust** | Yes, with a **scan results API** (`getScanResultSummary`, detailed results) | Yes | Large proprietary database | Yes | Quote only. **Moved from per-domain to traffic metering in 2026.** ~$10k/yr minimum, median ~$11.5–11.8k, implementation $10k–50k, renewal increases of 20–40% reported. Historical per-domain $827–1,100/month (all third-party reports) | Yes (enterprise localisation) | REST APIs, mobile SDKs | **UAE hosting region exists** (`app-ae.onetrust.com`, Dubai with Abu Dhabi DR). The only vendor here with UAE residency | Quote |
| **CookieYes** | Pro: monthly, 4,000 pages per scan. Ultimate: weekly, 8,000 pages | Yes | Proprietary database | Yes (anonymised IP, country, status, time; CSV export) | Per domain. Partner discounts "up to 50%" | 30+ languages, auto-translate. RTL not confirmed | No public scan API found | EU data centres | Basic $10, **Pro $25, Ultimate $55 per domain per month** (annual: $100 / $250 / $550). 100k / 300k / unlimited pageviews |
| **Termly** | Free quarterly, Starter monthly, **Pro+ weekly** | Yes | Proprietary | Pro+ only | Per site. Agency plan from 10 domains, quote | Multi-language on Pro+ | Not found | Not stated | Starter $10, **Pro+ $15 per site per month** (annual) |
| **Osano** | Yes | Yes | Proprietary | Yes | **Plus $199/month for 3 domains, 30k visitors.** Unlimited domains on the quote-only "Basic Privacy" tier and above | Not checked | Not checked | Not stated on the plan page | Plus $199/month. Otherwise quote |
| **Didomi** | Yes | Yes | Proprietary | Yes | **Unlimited domains, billed by monthly unique visitors.** Cross-domain consent sync on Advanced | Yes (enterprise) | APIs and SDKs (enterprise) | EU | From ~€250/month, quote |
| *CookieScript* (added: the cheapest tier with an API) | Monthly (Standard and Plus), 1,000 / 3,000 pages | Yes | Proprietary | Plus only | Bought in packs of 2–200 domains | 42 languages, **documented RTL setting** | **API on Plus only** (whether it returns scan results needs checking on a trial) | EU (Lithuania) | **Plus €4.50 per domain per month** |

**Where buying fits TICVAI badly:**

- **Licensing grows with tenants.** Every tenant domain is a separate licence (or session meter), so the cost rises
  with every tenant sold. It has to be built into the tenant subscription price, as BL-073 §2 already said.
- **Each vendor account is per domain or per account, not per tenant.** Sharing consent across a tenant's own domains
  (2.6.62) works inside one account. A shared account across tenants would mix their consent configurations.
- **Residency.** A full CMP stores consent records and IP addresses in its cloud, in the EU for every vendor here
  except OneTrust. **A scanner-only subscription does not have this problem**: a scan visits public pages and returns
  cookie names. No visitor data leaves the platform.
- **Scope.** None of them scans the native app, and none walks a booking journey to checkout.

## A4. Build: our own scanner

### Scope

| # | Component | What it does | Effort (developer-weeks, est.) |
|---|---|---|---|
| 1 | **Scan worker** | Playwright with Chromium in an AKS job (a scale-to-zero pool, or spot nodes). The page set comes from the tenant's config (home page, published content pages, event and product pages, booking flow steps), plus the sitemap, plus a bounded link crawl for partner microsites and client sites. Each page loads in a fresh browser context in **three consent states**, driven through `getCookieConsentRuntime` and a test consent key. It captures every cookie, including third-party ones (CDP `Storage.getCookies`), `localStorage`/`sessionStorage`/IndexedDB keys, network requests and the scripts that started them, and `Set-Cookie` attributes. | 2–3 |
| 2 | **Journey scripts** | Scripted runs through each booking flow type to the payment step with a test product, plus sign-in and account pages. This is the part vendor crawlers do not do. | 1–2 |
| 3 | **Classifier** | Imports the Open Cookie Database (Apache-2.0, **2,266 entries**, last commit 21 August 2026, with wildcard patterns) and matches tracker domains (Disconnect list, GPLv3; **not** DuckDuckGo Tracker Radar, which is CC BY-NC-SA, non-commercial). A **platform catalogue** of approved classifications sits on top and suggests a category. Unknown findings land as `detected`, which the contract already treats as blocked. | 1.5–2 |
| 4 | **Scheduler, intake, diff, alerts** | Reads `listCookieScanPolicies` (daily, weekly, monthly or off) and posts to `recordCookieScan`. The diff ("new" findings, and anything missing from two scans in a row) and the alerts are **already in the contract**, so this is plumbing only. | 1–1.5 |
| 5 | **Pre-consent compliance check** | Fails the run and raises an alert when anything that is not strictly necessary appears in the no-decision or reject-all state. This is **also the automated test that 2.6.58 blocking needs**, and it can run in CI against the tag loader. | 0.5–1 |
| 6 | **Hardening** | Isolates the crawler's network (it runs third-party JavaScript loaded by GTM), sets timeouts and budgets, adds observability and tests. | 1–2 |
| 7 | **App SDK inventory** | At build time, reads the P02 app's dependency manifest and posts `mobileSdk` findings. Not a crawler. | 0.5–1 |
| | **Total** | | **8–12 (midpoint 10)** |

### Running cost (est.)

Assume 50 pages per domain × 3 consent states × ~5 s per page, which is about 12.5 minutes per domain per scan. At
200 domains scanned weekly that is ~42 hours of browser time per week. One D4s v5-class node, running 3–4 browsers in
parallel and only during scan windows, handles it. **About $100–300/month including storage and logs, in UAE North.**
That is $1.2k–3.6k/year. The infra note of 30 September prices a D2s v5 at about $86/month in UAE North.

### Upkeep (est.)

- About **6 developer-weeks per year** (range 5–8): Playwright and Chromium upgrades, crawler breakage, Open Cookie
  Database refreshes, journey scripts kept in step with booking-flow changes.
- **Curation** of the platform catalogue by a privacy owner, a few hours a month. This is more than a vendor would
  need. Because the catalogue is shared across tenants, the work grows with the number of distinct technologies, not
  with the number of tenants.

## A5. Hybrid: our banner and logs (already decided) plus a bought scanner through its API

An adapter pulls each scan from the vendor's API and posts it to `recordCookieScan` with `source: boughtScanner` and
`scannerRef`. The vendor banner is not used. Candidates, cheapest first:

1. **CookieScript Plus**, €4.50 per domain per month. API on Plus. Whether the API returns scan results needs a trial
   to confirm.
2. **Cookiebot Premium Small or Medium** through its data API (cookie details per domain group). **Check the licence
   terms**: the subscription may assume the banner is deployed.
3. **OneTrust scanning API**: enterprise only, quote. Worth it only if the client wants OneTrust for UAE hosting.
4. Pay-per-page crawl services (for example Apify actors at about $20 per 1,000 pages). They are not compliance
   vendors, the quality of their categorisation is unknown, and **I do not recommend them**.

**What the hybrid does not cover:** checkout and signed-in journeys, testing in each consent state (some vendors flag
cookies "set before consent"; check this on a trial), the native app, and embedded checkout on the client's own site.
Item 5 of the build (the pre-consent check) is still needed for the 2.6.58 test, so the hybrid usually ends up with a
small part of the build anyway.

## A6. Cost table (USD, est.)

**Assumptions:**

- €1 = $1.17.
- **$2,000 per developer-week** (a placeholder; replace it with the real blended rate).
- Ops at $400 per day.
- The domain count is flat from month 1. That is conservative for the vendors: a slower ramp lowers their cost.
- List prices with no vendor discount and no price increases. OneTrust renewals are reported at +20–40%.
- **Not counted in any option:** the banner, runtime, registry, device-consent log and scan intake. They are ours
  under every option and are already in the contracts.

**What each option includes:**

- **Buy (full CMP), Cookiebot Medium (€30/domain/month = $421/yr) as the reference.**
  - One-off: integration, 5 developer-weeks ($10k). That covers the vendor consent callback into
    `recordDeviceConsent`/claim, consent-mode wiring, and the per-tenant provisioning runbook. Onboarding is $200 per
    domain.
  - Yearly: the licence, plus 2 developer-weeks of integration upkeep ($4k), plus $1k curation.
- **Build.**
  - One-off: 10 developer-weeks ($20k, range $16k–24k).
  - Yearly: 6 developer-weeks of upkeep ($12k), infra ($1.2k / $1.8k / $3.6k), curation ($2k / $3k / $4k).
- **Hybrid.**
  - One-off: adapter, 2.5 developer-weeks ($5k). Onboarding is $50 per domain.
  - Yearly: the licence (CookieScript Plus $63 per domain up to Cookiebot Small $211 per domain), plus 1.5
    developer-weeks of upkeep ($3k), plus $1.5k curation.

| Option | 10 domains, year 1 | 10 domains, 3-yr TCO | 50 domains, year 1 | 50 domains, 3-yr TCO | 200 domains, year 1 | 200 domains, 3-yr TCO |
|---|---|---|---|---|---|---|
| **Buy: Cookiebot Medium (full CMP)** | $21k | $40k | $46k | $98k | $139k | $318k |
| Buy: CookieYes Pro to Ultimate (licence only) | $2.5k–5.5k | $7.5k–16.5k | $12.5k–27.5k | $37.5k–82.5k | $50k–110k | $150k–330k |
| Buy: Termly Pro+ (licence only) | $1.8k | $5.4k | $9k | $27k | $36k (agency discount likely) | $108k |
| Buy: OneTrust | ≥$20k–60k (floor plus implementation) | ≥$40k–85k | quote | quote | quote, traffic-metered | **not estimable from public data** |
| Buy: Didomi / Osano | ~$3.5k+ / $2.4k per 3 domains | quote | quote | quote | quote | quote |
| **Build (own scanner)** | $35k | **$66k** | $37k | **$70k** | $40k | **$79k** |
| **Hybrid: CookieScript Plus API** | $11k | **$21k** | $15k | **$31k** | $32k | **$66k** |
| **Hybrid: Cookiebot Small data API** | $12k | **$25k** | $23k | **$53k** | $62k | **$155k** |

The "licence only" rows leave out the $10k integration and the per-tenant onboarding that a full CMP needs. Add about
$17k–58k over three years to compare them with the other rows.

**Where build becomes cheaper (3-year TCO):**

- **Against a full CMP** (Cookiebot Medium): from about **30 domains**.
- **Against a Cookiebot-class scanner-only hybrid:** from about **75 domains**.
- **Against the cheapest scanner API** (CookieScript): from about **275 domains**.

The build line is almost flat: $66k at 10 domains, $79k at 200. Every vendor line rises in a straight line with the
number of tenants.

**Sensitivity.**

- At $1,500 per developer-week, build costs about $50k–59k over three years, and the crossover with Cookiebot-class
  scanning falls to about 50 domains.
- At $3,000 per developer-week, build costs about $98k–118k, and the crossover rises to about 125 domains.

## A7. Effectiveness table

| Criterion | Buy (full CMP) | Hybrid (scanner API) | Build (own crawler) |
|---|---|---|---|
| Public pages | Good | Good | Good |
| **Booking flow, cart, checkout, signed-in pages** | Weak (link crawl) | Weak (link crawl) | **Good** (scripted journeys) |
| **Proves nothing loads before consent** (tested in each consent state) | Partial (some vendors flag "prior consent"; check) | Partial | **Good**, and the same test serves 2.6.58 in CI |
| GTM-injected tags | Good (accept-all crawl) | Good | Good (accept-all state) |
| Mobile app SDKs (22.13.10) | No (separate app SDK product at best) | No | **Yes** (inventory taken at build time) |
| **Categorisation coverage** | **Best** (large proprietary databases) | **Best** | Moderate: Open Cookie Database (2,266 entries) plus the platform catalogue. Unknowns stay blocked until an administrator classifies them |
| **Maintenance burden on us** | Low for scanning. **High for integration**: two banners, two logs, per-tenant vendor accounts | Low (adapter and per-domain registration) | **Medium**: ~6 developer-weeks/yr plus curation |
| Data residency | Consent records and IPs held by the vendor (EU; OneTrust offers UAE) | **No personal data leaves** (scan data only) | **UAE North only** |
| Evidence for PDPL, DSAR and the CF-160 merge | Needs two-way sync. Risk that the vendor holds the only copy (BL-073 §3) | Unaffected (consent is ours) | Unaffected (consent is ours) |
| Arabic / RTL | Varies. Irrelevant if our banner is used | Irrelevant (our banner) | Irrelevant (our banner) |
| Lock-in / exit | High | **Low** (`recordCookieScan` is the seam) | None |
| Time to first scan | Days | Days | 4–6 weeks after starting |
| **Compliance risk overall** | Medium: residency and a split record | **Low–medium**: blind to checkout and the app | **Low**, *if* a registry owner is staffed. A registry nobody maintains is worse than none, under every option |

## A8. Recommendation

**Build the scanner. Keep the hybrid as the fallback, and keep the manual-upload path in either case.**

Chinmay's test was *"if building is better at lower cost, it's worth it."* Taken against that test:

- **Effectiveness.** Building is better on the surfaces where TICVAI's risk sits: checkout, the consent-state proof,
  and the app. It is weaker only on breadth of categorisation, and the constrained tag surface plus the shared
  platform catalogue limit that weakness.
- **Cost.** Building is cheaper than a full CMP from ~30 domains and cheaper than a Cookiebot-class scanner from ~75.
  The infrastructure is sized for 200 tenants, and a tenant can own more than one domain (guest web, partner portal,
  extra brands).
- **It loses on cost below ~75 domains,** and against the cheapest scanner API below ~275. At 10–50 domains a
  CookieScript-class hybrid saves about $40k over three years.

**Proposed staging:**

1. **Now, with BL-073's other work:**
   - Draw CMS-025 with the manual "upload scan report" path, as the design notes already default to.
   - Build component 5, the pre-consent check over the known routes (~1 developer-week). It is the 2.6.58 test,
     needed under every option.
2. **Before the first tenant goes live:** components 1–4 and 6 (~7–9 developer-weeks).
3. **Later:** the app SDK inventory (component 7), with P02.

**What would change this:**

- **The client's 3-year tenant forecast is below ~50 domains** → choose the hybrid with the cheapest scanner API that
  returns scan results. Run a trial first to confirm the API and the licence terms.
- **The client wants a named vendor for assurance, or UAE-hosted vendor consent records** → OneTrust (UAE region).
  This is a procurement decision. Price it, and keep our consent record as the master copy (BL-073 §3).
- **Nobody will own the registry** → buy. Under every option, a registry with no owner is the real risk.

## A9. Contract gaps found while reading (ours under every option)

1. **`RecordCookieScanRequest.findings[]` cannot record the consent state.** A finding has `name`, `provider`,
   `technologyType`, `isThirdParty`, `durationDays` and `domainApplication`. To show that a cookie was *set before
   consent*, which is the most useful compliance output of a scan, it needs:
   - `consentState` (`noDecision | rejectedAll | acceptedAll`)
   - `pageUrl`, `initiatorUrl` (the script that set it)
   - `cookieDomain`, `sameSite`, `secure`
   - `suggestedCategory`, `classificationSource` (`openCookieDatabase | vendor | platformCatalogue | none`)

   `CookieScanRun` then needs a `preConsentViolationCount`.
2. **No platform catalogue.** The registry is venue-scoped (`x-ticvai-scope-level: venue`), so `_ga` would be
   classified again by every tenant. Propose a platform-scoped `TrackingTechnologyCatalogue` (in platform-ops or
   marketing-crm) that suggests categories. Each tenant still approves its own entries.
3. **GTM is the open door.** `StorefrontAnalyticsProvider.provider: googleTagManager` lets a tenant load anything after
   consent. CMS-025 or the analytics settings should say so, and the scan policy for a channel with a GTM container
   should default to `weekly`.
4. **Scan policy is not created automatically when a domain goes live.** `setCookieScanPolicy` is keyed on
   `channel + domainApplication`. `verifyCustomDomain` should create a default policy when a guest-web domain becomes
   `active`. This ties into the CMS-017 readiness list in Part B.
5. The CMS-025 action-bar error ("Analytics Tracker", "Embedded Service", "Other tracking technology" as buttons) is
   already recorded in the design notes. Those labels are technology types; the one action is "Add technology".

---

# Part B: Custom domains for tenant guest web apps

## B1. What the package has today, and whether CMS-017 covers the guest web app

**It covers it.** `claimCustomDomain.kind` is `guestWeb | guestApp | partnerPortal | developerPortal`. CMS-017 lists,
claims, verifies and releases domains, and verification routes the hostname through tenancy `setTenantDomainMapping`
(SD-021, applied 30 September), which `resolveTenantHost` reads at the edge. BO-835 (Site, Brand & Domain Setup) was
merged into CMS-017 and CMS-002 (M24-03). Its pack text asks for *"Validate domain, certificate, branding completeness
and environment promotion before go-live"*. The design notes for CMS-017 add a **default address** (the tenant's
TICVAI subdomain, DI-283: *"small tenants run under a subdomain/subpath of the TICVAI domain; larger clients get a
dedicated URL on their own domain"*, MoM 14 August).

**F103** (*a tenant claims a domain and gets a certificate*) walks ADM-017, the platform-admin screen, rather than the
tenant's CMS-017. It has only a permission branch: none for `hostname-taken`, a DNS record that is wrong, or
revalidation. Its step 2 (branding) has nothing to do with the domain.

**What is missing or does not match the decided edge (Azure Front Door Premium with WAF, HLD):**

| # | Gap | Why it matters |
|---|---|---|
| 1 | **Verification methods do not match Front Door.** The contract offers `dnsTxt`, `cname` and `httpFile`. | Front Door validates a custom domain for a managed certificate only by a TXT record named `_dnsauth.<subdomain>` with a value Front Door generates. The exceptions are domains prevalidated by Static Web Apps, and bring-your-own certificates, which are approved when the certificate's CN/SAN matches. `cname` and `httpFile` cannot be honoured on the managed path. **Keep TXT only.** |
| 2 | **One `verificationRecord`, but the tenant must publish two or three records.** | TXT `_dnsauth.<sub>` (validation), CNAME `<host>` → `<endpoint>.z01.azurefd.net` (traffic), and sometimes CAA `0 issue digicert.com`. Needed: a list `dnsRecords[]` with `purpose`, `type`, `name`, `value`, `ttl`, `observedValue`, `status` (missing / wrong / ok). |
| 3 | **The CNAME target must be the Front Door endpoint itself.** | Front Door does **not** renew managed certificates automatically when the CNAME points elsewhere, *"points to the Azure Front Door endpoint through a chain"*, uses an A record, or is an apex using CNAME flattening. Telling tenants to CNAME to `tenant.ticvai.app`, which then CNAMEs to Front Door, silently breaks renewal. The record must name the `azurefd.net` host, so the contract needs to store which profile and endpoint serve the domain (`edgeEndpointHost`). |
| 4 | **No state for "pending revalidation".** | 45 days before a managed certificate expires on a chained or apex domain, Front Door moves to *Pending revalidation* and needs a **new** TXT value. TXT values also time out after 7 days. `states/custom-domain.yaml` jumps from `active` to `expired`, and has no state for *active, renewal needs the tenant*. That is the "expires on a Saturday" case the contract itself warns about. Front Door's states are *Pending, Approved, Pending revalidation, Rejected, Timeout, Refreshing validation token, Internal error*. Map them, and keep certificate status separate from domain status. |
| 5 | **The platform subdomain is shown but has no operation.** | It lives in `control.tenant_domain` (`kind: platformSubdomain`). `setTenantDomainMapping` is service-only, and `listCustomDomains` reads `whitelabel.custom_domain`. CMS-017 cannot read it (DI-283). It also needs a slug rule and a rename policy. |
| 6 | **No primary domain and no redirects.** | Once a custom domain is active, the platform subdomain should redirect (301) to it so search engines do not see duplicate content. Apex → `www` and `http` → `https` are also unmodelled. Releasing the primary domain should restore the subdomain. Add `isPrimary` and `redirectToPrimary`. |
| 7 | **Release does not check for dangling DNS.** | If the tenant releases a domain but leaves the CNAME, the name is open to takeover (Azure: "dangling DNS / subdomain takeover"). The release dialog should show the record to delete, and a job should flag `active` domains whose CNAME no longer resolves to us. Fresh tokens on every claim are already right ("reclaiming is a new claim"). |
| 8 | **The checks each domain needs are not modelled.** | `guestUaePassLogin` (UAE Pass) uses registered redirect URIs. Each new host needs registering, or the callback has to go through one central auth host (check against UAE Pass onboarding). Apple Pay on the web needs each merchant domain registered and verified with the PSP (`/.well-known/apple-developer-merchantid-domain-association`). `kind: guestApp` needs `apple-app-site-association` and `assetlinks.json` served on that host. CORS and CSP origins, GA4 property domains, and the cookie scan policy (A9.4) also apply. None of this exists in the contracts today: grep found no Apple Pay domain, no universal links and no well-known files. |
| 9 | **Front Door profile limits are not tracked.** | Premium allows 500 custom domains, 200 routes and 25 endpoints per profile, 500 profiles per subscription, and a composite route metric ≤ 5,000 (domains × paths per route). 200 tenants × 1–2 domains fits in one profile. Beyond that the domains have to be spread across profiles, and with point 3 that means **the tenant's CNAME target changes**. Record the profile per domain now. |
| 10 | The state machine attributes `verified → issuing → active` to `claimCustomDomain`. | It is a job (or `verifyCustomDomain`), not the claim. Minor. |

## B2. Edge facts that shape every option (Azure Front Door Standard/Premium)

- **Managed certificates**:
  - Issued by DigiCert. Free.
  - The first 100 custom domains are free, and additional ones are also free on Standard and Premium. Premium's
    base fee is $330/month and covers everything.
  - Issuance takes minutes to an hour.
  - A tenant with a CAA record must allow `digicert.com`.
  - Front Door may change any part of the certificate, so tenants must not pin it.
- **Renewal**: automatic only if the CNAME points directly at the endpoint (B1 point 3).
- **Wildcard domains** (`*.ae.ticvai.app`):
  - Managed certificates are available, but **the Front Door domain documentation says wildcard managed certificates
    are not rotated automatically**.
  - Use a bring-your-own wildcard certificate from Key Vault with the version set to "Latest". New versions deploy
    within 72 h.
  - Key Vault must be in the same subscription. RSA only: Front Door does not accept EC certificates.
- **Certificate lifetimes are getting shorter** (CA/Browser Forum): 200 days from 15 March 2026, 100 days from
  15 March 2027, 47 days by 2029. Domain-validation reuse shrinks in the same steps. **Any option that needs the
  tenant to republish TXT values at renewal gets worse every year.** That rules out apex domains and chained CNAMEs as
  defaults.
- **Front Door is global.** It decrypts at the edge nearest the user (infra answers, 30 September, point 9). This
  applies to custom domains in the same way.
- **The tenant is resolved from the Host header.** Keep the client's Host (or read `X-Forwarded-Host`) through to the
  origin so that `resolveTenantHost` works. Azure's guidance on preserving the host name applies.

## B3. The options

| # | Option | How it works | Pros | Cons | Effort for us (est.) | Azure | Certificates | SEO | Cookies / SSO |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **Platform subdomain**, e.g. `coastalaqua.ae.ticvai.app` | Wildcard per cell stem (Azure's recommended "stamp-based wildcard" pattern, scenario 3), one Front Door domain per stem. A new tenant needs no DNS or Front Door change. `resolveTenantHost` maps host → tenant → cell → database. | Works on day 1. No client involvement. Fallback and preview address for every tenant. | Our brand in the URL. The tenant cannot take the URL with them if they leave. | 1–2 developer-weeks (stems, wildcard certificate in Key Vault with rotation, slug rules, the B1.5 read) | Front Door wildcard domain per stem; Azure DNS zone for `ticvai.app` | Bring-your-own wildcard certificate (managed wildcard certificates do not auto-rotate) | Authority builds on our domain, not the client's | **Use a registrable domain separate from `ticvai.com`.** **Use host-only cookies, never `Domain=ticvai.app`**, otherwise one tenant could set cookies for another tenant's subdomain. **Consider listing `ticvai.app` on the Public Suffix List** (as `azurewebsites.net` and `github.io` are) so browsers treat each tenant as its own site. Listing takes weeks to months. |
| **2** | **Customer CNAME**, e.g. `tickets.venue.com` | Tenant publishes TXT `_dnsauth.tickets` and CNAME `tickets` → our `azurefd.net` endpoint. `verifyCustomDomain` adds the domain to Front Door through ARM, polls validation, attaches the route, then calls `setTenantDomainMapping`. | The client's brand. Certificates managed and renewed automatically. Scales to 500 domains per profile. Azure's documented vanity-domain pattern (scenario 4). | The client controls the DNS, and a CAA record or a deleted CNAME breaks it. Onboarding is asynchronous: DNS propagation, 7-day TXT timeout. | 3–5 developer-weeks (ARM automation with managed identity, polling job, state mapping, CMS-017 records/status, release check) | Front Door custom domain plus route; WAF security policy | **Managed (DigiCert), auto-rotated** while the CNAME is direct | Content sits on the client's domain. Subdomain authority is partly shared with the root | **First-party on the client's subdomain**: no problem with Safari tracking prevention or third-party-cookie rules. Keep cookies host-only (`tickets.venue.com`), never `Domain=venue.com`. Guest sign-in is our own identity on this host. **The UAE Pass redirect and the Apple Pay domain need registering per host** (B1.8). |
| **3** | **Apex**, e.g. `venue.com` | Apex cannot be a CNAME. Needs Azure DNS alias records, or another provider that supports CNAME flattening, ALIAS or ANAME. A records to Front Door IPs are forbidden: they can change. | Clean URL for a tenant whose whole site is ours (no landing page of their own). | Renewal of managed certificates **needs a new TXT value at each renewal**, and renewals get more frequent as certificate lifetimes shrink. Many DNS providers cannot flatten. Route 53 alias records cannot target Front Door. Usually conflicts with the client owning the landing page. | +1–2 developer-weeks on top of option 2 (apex detection, revalidation reminders); or option 4, or our own ACME (below) | Front Door apex domain; **Azure DNS recommended** | Managed, but **manual TXT at every renewal**; or our own certificate | Best (root domain) | As option 2, on the root |
| **4** | **Delegated subdomain**, NS for `tickets.venue.com` → our Azure DNS | Tenant adds NS records once. We create the TXT, CNAME and alias records ourselves through ARM. | **Fully automatic**, including revalidation and the zone apex (alias records). The tenant does nothing after the NS change. Fixes options 2 and 3's renewal fragility. | Client IT may refuse to delegate. We become their DNS operator for that name (uptime, DNSSEC chain if they sign). Offboarding needs the NS records removed (dangling-DNS risk again). | +2–3 developer-weeks on top of option 2 (zone per tenant, record automation, offboarding) | Azure DNS public zones: **$0.50/zone/month for the first 25, $0.10 after; queries $0.40 per million** (Azure retail prices API, 2 October 2026) | Managed, auto-rotated (we own the records) | As option 2 | As option 2 |
| **5** | **Reverse-proxy path**, e.g. `venue.com/tickets` | The client's CDN or web server proxies `/tickets/*` to our endpoint. If they are on Azure: their own Front Door or Application Gateway with our endpoint as origin. | Best for SEO (one domain). Seamless for the client's site. | **The client's site and our app share an origin**: their scripts (their own trackers, any XSS) can read our `localStorage` and non-HttpOnly cookies, and our cookie registry has to cover their tags. Our WAF and rate limits see the client's proxy IPs, and our waiting room (ADR-0066) sits behind someone else's CDN. Our SPA has to support a base path (router, assets, service-worker scope, `Path=/tickets` cookies). Every incident spans two organisations. | 3–6 developer-weeks once (base-path support), plus a per-tenant runbook and support. High ongoing cost | Their side: Front Door, App Gateway, Cloudflare, nginx. Ours: accept only their proxy (`X-Azure-FDID` check or mTLS) | **Theirs.** We cannot issue for their root | Best | Shared origin (above). Sign-in callbacks and Apple Pay use **their** domain |
| (6) | **Embedded widget**, `BookingFlowConfig.embedMode: embedded` | iframe or web component on the client's landing page | Booking visible on their page with no DNS work | In an iframe our cookies are **third-party**: Safari and Firefox block them by default, so sign-in and cart state fail unless we use partitioned cookies (CHIPS) or the Storage Access API. 3-D Secure redirects and Apple Pay in iframes need `allow="payment"` and testing. | 2–3 developer-weeks (partitioned cookies, postMessage sizing, payment hand-off) | — | Ours (the iframe host) | Content not indexed on their domain | Third-party context (above) |

**Our own ACME instead of Front Door managed certificates (a variant for options 2 and 3).** cert-manager or a Key
Vault ACME bot gets Let's Encrypt certificates (RSA) through HTTP-01 challenges that Front Door routes to our origin.
The certificates go into Key Vault, and Front Door uses them as bring-your-own with version "Latest". This works with
apex and chained CNAMEs without the tenant republishing TXT records.

- Cost: we run it, about +2–3 developer-weeks, and the up-to-72 h rollout of a new version has to fit inside the
  renewal window.
- Let's Encrypt limits: 300 new orders per account per 3 h, 50 certificates per registered domain per week (fine per
  tenant).
- Let's Encrypt lifetimes go from 90 days to 64 days on 10 February 2027 and to 45 days on 16 February 2028.
- **Hold this in reserve for apex requests.** It is not the default.

**Application Gateway** (regional, UAE North) is not a good choice for tenant hostnames. It has no managed
certificates, and its multi-site listener and certificate counts per gateway are far below Front Door's 500 domains
(check the exact figure on the limits page). Front Door is the decided single entry (HLD), and Application Gateway for
Containers is being considered only as the AKS ingress behind it (infra answers, 30 September).

## B4. Client landing pages and templates

**When the client owns the landing page** (Chinmay's case):

1. The client's site (`venue.com`) stays theirs. Their buttons link to **stable deep links** on the ticket host:
   - `https://tickets.venue.com/events/{slug}`
   - `/book/{productSlug}?date=YYYY-MM-DD`
   - UTM parameters pass through to `recordStorefrontSessionEvents` and the analytics providers.

   **We should publish a deep-link scheme and a link builder in the CMS.** No operation documents one today. The
   header logo and "back to site" link should point to the client's landing URL (`setHeader`/`setNavigation` with an
   external link; check whether external links are allowed).
2. If the client wants `venue.com/tickets` as a short URL, they **redirect** it (301) to `tickets.venue.com` on their
   own host. This gives the familiar path without the shared-origin problems of option 5.
3. **Consent on the landing page is the client's**, through their own CMP. Ours covers our host. A shared choice
   across the two (2.6.62) would need a shared cookie on `venue.com`, which we should not set. State it as a limit,
   or offer a consent hand-off by URL parameter later.
4. Cross-domain analytics (`venue.com` → `tickets.venue.com`): GA4 cross-domain measurement on both sides, which the
   tenant configures in their own GA. It loads only after consent on each host.
5. Once the custom domain is active, the platform subdomain redirects (301) to it (B1.6).

**When the client has no landing page:**

- **The site builder already has the templates.** `SiteSetupProgress.presetKey` is one of `themePark`, `waterPark`,
  `museum`, `theatreAndArena`, `singleAttraction`, `playCentre` or `multiVenue` (W12 and M24-05). It fills in the
  home-page sections, booking flows, mobile tabs and modules, about 30 minutes to a working site. CMS-007 Page Builder,
  BO-837 Page & Landing Builder and the AI-generated site (2.6.50) produce the content pages.
- So "templates we provide" means **our storefront's home page (WEB-001) is the landing page**, served on:
  - the platform subdomain (option 1) at first; then
  - `www.venue.com` (option 2), with the client's registrar forwarding the apex to `www`. Most registrars offer URL
    forwarding; option 4 or the ACME variant can serve the apex itself if they insist.

## B5. Recommended default

1. **Every tenant: a platform subdomain at provisioning (option 1).**
   - Separate registrable domain, one stem per cell (`*.ae.ticvai.app`; add `*.sa.`, `*.eg.` when those cells open,
     following ADR-0001), bring-your-own wildcard certificate in Key Vault, host-only cookies.
   - Start the Public Suffix List submission early.
2. **Clients with a domain: customer CNAME on a subdomain (option 2).**
   - The CNAME must point **straight at the Front Door endpoint**. TXT `_dnsauth` validation, Front Door-managed
     DigiCert certificate.
   - Suggested hostnames: `tickets.`, `book.`, `shop.`.
3. **Clients who prefer no DNS work: delegated subdomain (option 4)**, as a paid or enterprise choice.
4. **Apex: on request only.** Prefer `www` plus registrar forwarding. Otherwise option 4 (Azure DNS alias) or the
   ACME variant.
5. **Reverse-proxy path (option 5): not offered.** Offer the client-side 301 redirect instead.
6. **Embedded widget (6): browse and teaser only.** Checkout opens on the ticket host.

## B6. What CMS-017 must show (proposal; contracts not edited)

**Header**

- **Default address**: the platform subdomain, always working. Copy and open buttons.
- **Primary domain**: which host is canonical, and whether the others redirect to it.

**Each domain row**

| Field | Content |
|---|---|
| Hostname, kind | `tickets.venue.com`, Guest website (or app links, partner portal, developer portal) |
| Type | Subdomain / **Apex** (with the warning: *"needs a DNS provider with ALIAS or CNAME flattening, and a new TXT record at each certificate renewal"*) / Delegated |
| **DNS records to publish** | A table with one row per record, each with a copy button: **TXT** `_dnsauth.tickets` = `<Front Door value>`, TTL 3600, *validation*; **CNAME** `tickets` = `<endpoint>.z01.azurefd.net`, *traffic* (with the note "point directly at this host, not at another alias, or certificates will not renew"); **CAA** `0 issue digicert.com`, *only if you have CAA records*. For delegated domains: the **NS** records instead. Each row shows the **observed value** and **status** (missing / wrong value / ok) from the last check. |
| **Verification** | Pending (waiting for the TXT record) → Checking → **Approved**. Also **Timeout**: the token expired after 7 days, so offer "Generate new value". **Rejected** shows the reason. **Pending revalidation** names the record to add, by when (45-day window), and the consequence. |
| **Certificate** | Type (managed / own), issuer, expiry (amber within 30 days, red within 7), *auto-renews: yes / no and why* (apex, chained CNAME) |
| **Routing** | CNAME resolves to us: yes / no, last checked. A domain that is `active` and no longer points to us is flagged, because it is open to takeover |
| **Readiness checklist** (from BO-835's "validate before go-live") | Live on the edge · UAE Pass redirect registered · Apple Pay domain verified with the PSP · App links files served (guest app) · Cookie scan policy created · Analytics properties updated · Redirect from the platform subdomain on |

**Actions**

- Claim
- Check now (the job retries anyway; DNS can take hours)
- Generate new value
- Make primary
- Release. Refused while the domain is the only live one (R096). Otherwise the dialog shows *"remove these records at
  your DNS provider"* and the domain stays listed as detached.

**Contract changes this implies** (to propose; not made here):

- **`CustomDomain`:**
  - `verificationMethod` reduced to `dnsTxt`, plus `byoc` for clients who bring their own certificate.
  - `verificationRecord` replaced by `dnsRecords[]` (purpose, type, name, value, ttl, observedValue, status).
  - New fields: `domainType` (subdomain / apex / delegated), `edgeProfile` and `edgeEndpointHost`,
    `certificateType`, `certificateIssuer`, `autoRenews` and `autoRenewBlockedReason`, `validationExpiresAt`,
    `routingStatus`, `isPrimary`, `readiness{}`.
- **`states/custom-domain.yaml`:** add `pendingRevalidation` (from `active`, back to `active`) and `timedOut`.
- **New read:** the platform subdomain for the tenant (from `control.tenant_domain`).
- **New operations:** `setPrimaryDomain`, `regenerateDomainToken`.
- **F103:** a tenant-side walk through CMS-017, with branches for hostname-taken, wrong record, timeout and
  revalidation.

---

## Sources (accessed 2 October 2026 unless stated)

**Vendors**
- Cookiebot pricing: https://www.cookiebot.com/en/pricing/
- Cookiebot reseller programme: https://cookiebot.com/en/resellers ; domain groups for resellers: https://support.cookiebot.com/hc/en-us/articles/360004527633 ; data API: https://support.cookiebot.com/hc/en-us/articles/360006346473-Extracting-cookie-information-via-API (403 to automated fetch; content from search summary)
- Cookiebot languages (Arabic among 48): https://support.cookiebot.com/hc/en-us/articles/360004259374
- Usercentrics/Cookiebot EU hosting: https://europeanpurpose.com/tool/usercentrics ; https://cookiebot.com/privacy-policy/
- OneTrust pricing (third-party, 2026): https://www.pii.ai/blog/onetrust-cookie-consent-pricing-the-complete-2025-guide ; https://www.consentstack.io/blog/onetrust-pricing ; https://www.enzuzo.com/blog/onetrust-vs-cookiebot
- OneTrust hosting regions incl. UAE (page content dated mid-2023 or later): https://my.onetrust.com/articles/en_US/Knowledge/UUID-21f6bff2-1b12-8c67-e8b0-d852e36f37af
- OneTrust scan results API: https://developer.onetrust.com/onetrust/reference/getscanresultsummary.md
- CookieYes pricing: https://www.cookieyes.com/pricing/ ; languages: https://www.cookieyes.com/documentation/banner-languages/
- Termly pricing: https://termly.io/pricing/
- Osano cookie consent plans: https://www.osano.com/plans/cookie-consent
- Didomi pricing (third-party): https://www.enzuzo.com/blog/didomi-pricing ; https://frontdeskreview.com/software/consent-management-platforms/didomi/
- CookieScript pricing: https://cookie-script.com/pricing ; RTL: https://help.cookie-script.com/en/articles/30169-how-to-write-right-to-left-text-on-a-banner
- Apify cookie scanner (pay per page): https://apify.com/eliai/webpage-cookie-scanner

**Open data for build**
- Open Cookie Database (Apache-2.0; 2,266 rows counted from the CSV; last commit 21 August 2026): https://github.com/jkwakman/Open-Cookie-Database
- DuckDuckGo Tracker Radar licence (CC BY-NC-SA 4.0): https://github.com/duckduckgo/tracker-radar
- Disconnect tracking protection list (GPLv3): https://disconnect.me/trackerprotection

**Azure**
- Front Door domains, validation states, managed certificates, renewal rules (ms.date 9 July 2026, updated 12 September 2026): https://learn.microsoft.com/en-us/azure/frontdoor/domain
- Front Door apex domains (updated 30 July 2026): https://learn.microsoft.com/en-us/azure/frontdoor/apex-domain
- Front Door wildcard domains (ms.date 26 May 2026): https://learn.microsoft.com/en-us/azure/frontdoor/front-door-wildcard-domain
- Front Door in a multitenant solution, scenarios 1–5 (ms.date 29 May 2026): https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/front-door
- Domain name considerations in multitenant solutions, dangling DNS (updated 18 September 2026): https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/domain-names
- Front Door routing limits, composite 5,000 (updated 17 July 2026): https://learn.microsoft.com/en-us/azure/frontdoor/front-door-routing-limits
- Front Door Standard/Premium service limits (500 custom domains Premium, 100 Standard; include dated 14 July 2026): https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-front-door-standard-and-premium-service-limits
- Front Door pricing model (base $330 Premium; custom domains free): https://learn.microsoft.com/en-us/azure/frontdoor/understanding-pricing
- Subdomain takeover: https://learn.microsoft.com/en-us/azure/security/fundamentals/subdomain-takeover
- Azure DNS subdomain delegation: https://learn.microsoft.com/en-us/azure/dns/delegate-subdomain ; alias records: https://learn.microsoft.com/en-us/azure/dns/dns-alias
- Azure DNS prices: Azure Retail Prices API, `serviceName eq 'Azure DNS'`: https://prices.azure.com/api/retail/prices
- Host name preservation: https://learn.microsoft.com/en-us/azure/architecture/best-practices/host-name-preservation

**Certificates and browsers**
- Let's Encrypt rate limits (updated 5 August 2026): https://letsencrypt.org/docs/rate-limits/
- Let's Encrypt move to 45-day certificates: https://isrg.org/post/from-90-to-45/
- CA/Browser Forum lifetimes and validation reuse (200 / 100 / 47 days): https://www.digicert.com/faq/tls-ssl-certificate-validity ; https://www.ssl.com/guide/how-to-manage-domain-validation-under-the-200-day-dcv-reuse-policy/
- Public Suffix List: https://publicsuffix.org/
- Partitioned cookies (CHIPS): https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Privacy_sandbox/Partitioned_cookies
- Apple Pay on the web, merchant domain verification: https://developer.apple.com/documentation/apple_pay_on_the_web/configuring_your_environment
