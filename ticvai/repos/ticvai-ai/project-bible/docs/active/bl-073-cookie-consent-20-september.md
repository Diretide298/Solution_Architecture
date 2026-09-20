# BL-073 — cookie consent: what to buy, what to build, what is ours either way

> **20 September 2026 · decision paper for Qossai · CF-127**
>
> **The buy-versus-build call is the client's and is not made here.** Section 5 gives a
> recommendation and the one reason behind it. Sections 3 and 4 are the same whichever way it
> goes, and they are the part that cannot wait for the answer.
>
> **No contract, register or handoff artefact is edited by this paper.** The YAML in section 4 is
> a proposal in a fenced block.

---

## 1. The seventeen requirements, and which of them a bought platform already answers

**CF-127 says fifteen; BL-073 carries seventeen.** The `refs` array in
`handoff/contract-backlog.json` holds 2.6.51–2.6.65 — fifteen consecutive rows — plus **22.10.29**
and **22.13.10**, which CF-127 does not mention. Both are counted here. The fifteen were read from
`sources/requirements/Ticvai_matrix_20260621_2.xlsx`, sheet `Funactionality `, matching on the
`Requirement ID` column; the two domain-22 rows came from the same sheet.

Each row was then classed by hand against what Cookiebot, OneTrust, Didomi and Usercentrics ship
in a standard cookie-consent subscription. **Eleven of the fifteen are standard product; four are
not; both domain-22 rows fall outside a browser tag's reach entirely.**

### Standard in any bought consent platform — 11 rows

| Ref | What it asks |
|---|---|
| 2.6.51 | A cookie-policy management solution for GDPR, ePrivacy, CCPA/CPRA and other regional laws |
| 2.6.52 | Banner on first visit; configurable layout (top, bottom, pop-up, modal); multi-language; responsive; accept all / reject non-essential / customise |
| 2.6.53 | Five categories — strictly necessary, functional, analytics, marketing, preference |
| 2.6.54 | Preference centre with per-cookie name, provider, purpose, expiry, first/third party |
| 2.6.55 | Consent record: status, date and time, user identifier or session id, IP where legally permitted, consent version, withdrawal at any time |
| 2.6.56 | Audit trail — initial consent, preference updates, withdrawals, compliance reports |
| 2.6.57 | Automatic site scanning for new cookies, third-party cookies, tracking technologies, pixel tags, local-storage items, with an administrator alert |
| 2.6.58 | Blocking analytics scripts, marketing tags and advertising trackers until consent |
| 2.6.62 | Multi-domain — consent shared across related domains, centrally administered |
| 2.6.63 | Acceptance rate, rejection rate, preference selection by category, geographic statistics, compliance audit reports |
| 2.6.64 | Administration portal — categories, banner design, translations, consent logs, reports, scan schedules |

**2.6.62 is in this list with an asterisk.** A vendor shares consent across domains *inside one
account*. TICVAI is multi-tenant and `claimCustomDomain` gives every tenant its own domain, so
"related domains" is related *per tenant* and needs a vendor account per tenant. That is a pricing
fact, not a capability gap — section 2.

### Not standard, or only half-covered — 4 rows

| Ref | Why a vendor does not close it |
|---|---|
| **2.6.59** | Policy content, versioning, automatic publication, historical versions. **`setPolicy` already does this** — `Policy` is versioned, never overwritten, and `PolicyKind.cookie` is one of five kinds. A CMP generates a cookie *declaration*; it does not hold the tenant's policy corpus, its approval workflow (CMS-028 `listPrivacyNoticePolicy`) or its `requiresReconsent` flag. Buying a second policy store here would duplicate the one that works. |
| **2.6.60** | Names GDPR, ePrivacy, CCPA, CPRA, LGPD and **PDPL (UAE and Saudi Arabia)**. Vendors ship frameworks for the first five. **There is no UAE cookie framework to ship** — section 6. PDPL support is configuration and a legal position, not a product feature, and the vendor will not supply it. |
| **2.6.61** | Review history, change preferences, withdraw, *"request data deletion (if integrated with privacy management)"*. Deletion is `deleteGuestAccount` and ADR-0047; a vendor's consent history is browser-scoped and cannot answer a DSAR against a person. The parenthesis in the requirement is the integration back to us. |
| **2.6.65** | Encryption, RBAC, one-second banner load, millions of records, 99.9%, and integration with *"CMS platforms, Google Analytics, Google Tag Manager, CRM systems, Customer Data Platforms, Identity and Access Management"*. If bought these are the vendor's SLA and our integration bill; if built they are ours. Either way the **CRM/CDP/IAM integration is work on our side that no vendor performs.** |

### Outside a browser tag altogether — the 2 rows CF-127 omits

**22.13.10 — Cookie & Tracking Consent.** *"Websites **and mobile applications** shall support
configurable cookie consent management, tracking permissions, analytics consent, advertising
consent, and personalization preferences."* A browser tag does not run in a native app. The
package ships P02 (guest mobile) and a kiosk shell; the tracking registry already declares
`mobileApp` and `embeddedCheckout` as governed channels. **Grepped across all 32 contracts,
22.13.10 has no citation anywhere** — it is uncovered today.

**22.10.29 — Analytics Integration.** *"CMS shall integrate with analytics platforms and provide
insights on page performance, engagement, conversions, and visitor behavior."* This is the
injection point, which is to say the thing that must be blocked. **`white-label.yaml` contains no
analytics or tag-injection operation** — zero matches for `tag manager`, `gtm` or `google
analytics` across the file — so 22.10.29 has no home either. That matters for the estimate and is
taken up in section 2.

---

## 2. The case each way

### What already exists, which is more than CF-127 records

CF-127 says *"the package has one trace: `PolicyKind.cookie`"*. **That was true on 18 August and
is not true now.** Parsing `contracts/satellite/marketing-crm.yaml` for operations citing
`P13 CMS-021` through `CMS-039` returns **19 operations, 18 of them
`x-ticvai-provisional: true`** — the client's own *Privacy, Consent & Preference Management*
workshop pack, read off the PDF and drafted in. Three are cookie consent directly:

    listCookieTrackingDigital    CMS-025  36 properties  Cookie, Tracking & Digital
                                                          Technology Registry
    listCookieBannerPreference   CMS-026  21 properties  Cookie Banner & Preference
                                                          Center Designer
    setConsentCapturePoint       CMS-027  28 properties  Consent Capture Point &
                                                          Customer Journey Configuration

They are provisional — shapes read from a workshop pack, agreed with nobody, persistence tagged
`none — projection`. **But they are the client's own sentences**, and CMS-026 asks for a *no-code
designer for privacy/cookie interfaces*, which is a thing the client expects to configure inside
TICVAI rather than inside a vendor console. That changes the framing of the question: the client
has already drawn the administration portal of 2.6.64 as one of our screens.

`CookieTrackingDigitalTechnologyRegistryView` also names the governed surfaces:
`b2cWebsite`, `customerPortal`, `mobileApp`, `embeddedCheckout`, `whiteLabelSites`,
`partnerMicrosites` — **six channels, of which two are not browsers.**

### Buy

**Licence cost is per domain or per traffic, and this platform multiplies both.**
Cookiebot's published 2026 tiers are €15 / €30 / €50 / €90 per domain per month by subpage count,
with a four-domain minimum; business and multi-domain tiers are quoted. OneTrust's published
minimum for cookie consent is **$10,000 per year**, median reported spend around $11,500–11,800,
with implementation fees of **$10,000–50,000** on top and renewal increases of 20–40% reported.
([Cookiebot/OneTrust pricing comparison](https://www.enzuzo.com/blog/onetrust-vs-cookiebot),
[OneTrust pricing](https://www.consentstack.io/blog/onetrust-pricing))

Against a platform where `claimCustomDomain` gives **each tenant its own domain**, per-domain
pricing is a per-tenant cost of sale, and a traffic-metered contract is a variable cost that
scales with the tenants' success rather than ours. Neither is fatal; both have to be priced into
the tenant subscription before the contract is signed, not after.

**What buying actually removes from our build:** the banner, the preference centre, the category
model, script blocking on `b2cWebsite` and `whiteLabelSites`, scanning, the cookie database,
consent analytics and the vendor's own admin console — items 2.6.52–2.6.58 and 2.6.63–2.6.64 as
they apply to browser surfaces.

**What buying does not remove:**

- The consent record in `marketing` and the merge rule — **section 3, and it is not negotiable.**
- `mobileApp` and `embeddedCheckout`. A tag does not reach either.
- 2.6.59, 2.6.60, 2.6.61, 2.6.65's integration list.
- A **cross-border transfer position**. A CMP stores consent records and IP addresses in the
  vendor's cloud. Under ADR-0009 that is Article 22 territory — adequacy, SCCs or explicit
  consent, with a transfer risk assessment documented before the flow starts. One vendor,
  assessed once, for every tenant.
- The per-tenant onboarding: a vendor account, a domain verification, a scan schedule and a
  category mapping **per tenant**, which is operational work that recurs on every new tenant for
  the life of the platform.

### Build — what each of the six named pieces actually costs

CF-127 names six. They do not cost the same and the difference is the whole decision.

| Piece | Cost | Why |
|---|---|---|
| **Banner** | Low | The shape is already drafted at 21 properties (CMS-026), and `getTheme`/`setTheme`, `LocalisedRichText`, the translations screen (CMS-011) and RTL preview (CMS-012) all exist. It is a themed component plus a config screen against machinery the storefront already has. |
| **Category model** | Low | Five values. The registry draft already enumerates `strictlyNecessary`, `functional`, `analytics`, `personalization`, `advertisingMarketing` and an `otherOrganizationDefinedCategories` escape. It is an enum and a mapping. |
| **Script blocking** | **Low — and this is the surprise** | Blocking is expensive when you do not control the page. **We ship the page.** And `white-label.yaml` has no tag-injection operation at all today, so 22.10.29 has to be built regardless. Building the injection point consent-gated costs close to nothing more than building it ungated; building it ungated first and retrofitting a gate costs a great deal more. |
| **Multi-domain preference sharing** | Low | Free as a consequence of section 4. If the consent key is issued by us and the runtime endpoint is ours, every domain a tenant owns reads the same key from the same tenant-scoped endpoint. A vendor cannot do this *across tenants* at all, because each tenant would be a separate account. |
| **Consent analytics** | Low | Five figures — acceptance, rejection, preference by category, geography, audit export — over a table we hold either way. |
| **Site scanning** | **High, and it never stops** | A headless crawler per tenant domain on a schedule, plus a maintained attribution database mapping cookie name → provider → purpose → duration → first/third party. **The crawler is a week; the database is forever.** Third-party tags change without telling anyone, and a registry that is six months stale is worse than no registry because it is evidence of a control that was not operating. |

**Five of the six are cheap because of what the package already is. The sixth is the entire
standing commitment CF-127 warns about, and CF-127 is right about it.**

---

## 3. What we must own regardless of the answer

**This is the section that does not depend on the decision.**

### The rule

**A consent record that carries a `subjectId` is ours. A consent decision that carries only a
browser may live in a vendor.**

The line is not a preference. Four things force it:

1. **`recordConsent` already answers the question.** It is append-only, captures purpose,
   decision, channels, `noticeVersion`, `source` and `recordedAt`, names
   `recordedByPrincipalId` when an agent acts by proxy, and is `x-ticvai-self-scoped: subject`
   with `x-ticvai-conflict-policy: append`. A second store with its own answer is two answers.
2. **CF-160's merge rule has to keep working.** `identity.yaml` states it in the guest-checkout
   path — *"A merge takes the narrower of two consents (CF-160)"* — `marketing-crm.yaml` states
   it at the merge operation — *"Consent is the one thing that does not merge. Two records with
   different marketing consents produce the narrower of the two — inheriting the more permissive
   consent is how a merge becomes a breach"* — and ADR-0045 restates it for order attachment.
   **A vendor store is keyed on a browser, and the merge is keyed on a person.** One guest on
   three devices and two guests on one shared kiosk browser both break it in opposite directions.
   Concretely: a guest rejects marketing on their phone and accepts it on a kiosk; the merge must
   yield *withdrawn*, and a vendor that holds only one of those two decisions will never produce
   that answer.
3. **ADR-0023.** Four `pii.*` tables, zero operations touching both `pii.*` and `ledger.posting`,
   verified 17 August. 2.6.55 asks us to store an IP address and a session identifier against a
   consent. **Those are personal data and they belong in `pii`, not in `marketing`** — otherwise
   erasure has to reach into the consent evidence, which is exactly what the separation exists to
   prevent.
4. **ADR-0047.** Retention, archive and erasure are stage transitions over stores we operate.
   A consent record held by a vendor is outside all three: it does not archive with the tenant's
   cell, it does not purge at archive, and `deleteGuestAccount` cannot tombstone it.

### Where each record lives, precisely

    marketing.consent_record     the decision, once a subject exists.
                                 MUST be ours. recordConsent writes it,
                                 getConsentHistory proves it, the merge reads it,
                                 ADR-0047 ages it.

    marketing.device_consent     the pre-identity decision, keyed by an opaque
                                 consentKey the banner issues. SHOULD be ours even
                                 when the banner is bought -- it is the input to the
                                 claim in section 4, and a claim cannot run against
                                 a store we cannot read.

    pii.consent_identifier       IP address and device/session reference, keyed by
                                 the consent record. MUST be ours and MUST be in pii,
                                 per ADR-0023 -- these are the only personal data in
                                 the consent path, and putting them in `marketing`
                                 would put personal data outside the erasable store.

    vendor                       MAY hold: the cookie catalogue, scan results and
                                 scan schedules; the banner's own rendering state;
                                 the per-browser consent string it sets as its own
                                 cookie. None of these is a fact about a known
                                 person and none is an input to a merge.

    vendor, never alone          the consent record for an identified guest; anything
                                 a DSAR must answer; anything a campaign send-time
                                 check reads. A bought CMP may hold a copy. It may
                                 not hold the only copy.

**The one-line test to give the vendor's solution architect:** *can `getConsentHistory` return it,
can the merge narrow it, and does `deleteGuestAccount` erase it?* Three yeses or it is in the
wrong place.

### Two gaps this exposes that are ours whichever way the decision goes

**`ConsentRecord` carries no `scopePath`.** `Suppression` gained one on 31 August when 49 tables
were found writing at a declared scope with no column for it. The consent path was not in that
sweep because `recordConsent` is `subject`-scoped, and for the guest's own decision that is
correct. **A device consent has no subject**, so it has to be tenant-scoped and needs the column —
noted in the proposal below rather than assumed.

**ADR-0047's retention table has no class for a consent given by a browser.** Every other class in
it is anchored to a person or a ticket. A device consent is anchored to neither, and the working
convention across CMPs is a twelve-month expiry. `ConsentPurposeConfig.expiresAfterMonths` already
exists and is the right mechanism; **the number is not set and ADR-0047 should be amended to carry
the class.** That is a one-row amendment, not a redesign.

---

## 4. The contract design for our side

**Two contracts, because the split is real.** Configuration, the registry and the banner go to
`white-label` — it owns the storefront, `claimCustomDomain`, `setTheme`, `setPolicy` and
`PolicyKind.cookie`, and `white-label` is BL-073's declared `candidateHome`. The consent record
goes to `marketing-crm`, beside `recordConsent`, because section 3 says it cannot go anywhere
else.

**Every operation below is written so that buying changes who calls `recordCookieScan` and nothing
else.** That is deliberate: the contract should not encode the decision Qossai has not made.

### 4a. `white-label.yaml` — the registry, the banner and the runtime

```yaml
    CookieCategory:
      type: string
      enum:
      - strictlyNecessary
      - functional
      - analytics
      - personalisation
      - marketing
      description: '2.6.53. **Five, and `personalisation` rather than `personalization`** — the
        CMS-025 draft carries the American spelling and `ConsentPurpose` carries the British one,
        and two spellings of one category is two categories.

        **Not the same axis as `ConsentPurpose`.** A category is a class of technology on a page;
        a purpose is a lawful basis for processing a person. `setCookieCategoryMapping` maps the
        first onto the second and the mapping is the tenant''s, because only the tenant knows
        what its own analytics tag is actually for.

        '

    TrackingTechnology:
      x-ticvai-persistence: whitelabel.tracking_technology
      type: object
      required:
      - technologyId
      - name
      - provider
      - category
      - isThirdParty
      - channel
      - status
      - scopePath
      properties:
        technologyId:
          type: string
          readOnly: true
        name:
          type: string
          description: The cookie, SDK, pixel or storage key as it appears on the device.
        provider:
          type: string
        purpose:
          type: string
        dataCollected:
          type: string
          nullable: true
        durationDays:
          type: integer
          nullable: true
          description: 'Null for session storage, which has no duration. **A number rather than
            the draft''s free-text `duration`** — 2.6.54 shows it to a guest and a guest comparing
            "1 year" against "12 months" is comparing two strings.

            '
        isThirdParty:
          type: boolean
        category:
          $ref: '#/components/schemas/CookieCategory'
        channel:
          type: string
          enum:
          - b2cWebsite
          - customerPortal
          - mobileApp
          - embeddedCheckout
          - whiteLabelSite
          - partnerMicrosite
          description: 'The six surfaces CMS-025 names. **`mobileApp` and `embeddedCheckout` are
            in the enum because they are governed, not because a browser tag can reach them** —
            a bought CMP leaves both rows to be maintained by hand.

            '
        status:
          type: string
          enum:
          - detected
          - approved
          - blocked
          - retired
          description: '**`detected` is the state a scan writes and no scan may leave.** A
            technology found by a scan is not thereby permitted; an administrator approves it into
            a category (2.6.57''s alert) and until they do it is treated as `blocked`.

            '
        firstDetectedAt:
          type: string
          format: date-time
          nullable: true
        lastSeenAt:
          type: string
          format: date-time
          nullable: true
          description: 'A technology not seen by the last two scans is a candidate for `retired`.
            **Retired rather than deleted** — the registry is evidence of what the site did on a
            date, and 2.6.56''s audit report reads it backwards.

            '
        scopePath:
          type: string
          description: The partition key (ADR-0005), tenant-scoped.

    CookieBannerConfig:
      x-ticvai-persistence: whitelabel.cookie_banner
      type: object
      required:
      - position
      - rejectIsOneClick
      - noticeVersion
      - languages
      properties:
        position:
          type: string
          enum: [top, bottom, popup, modal]
        title:
          $ref: '#/components/schemas/LocalisedRichText'
        body:
          $ref: '#/components/schemas/LocalisedRichText'
        categoryDescriptions:
          type: array
          items:
            type: object
            required: [category, description]
            properties:
              category:
                $ref: '#/components/schemas/CookieCategory'
              description:
                $ref: '#/components/schemas/LocalisedRichText'
        rejectIsOneClick:
          type: boolean
          description: '**Not configurable to false, and it is a boolean anyway so the contract
            can say so.** 2.6.52 asks for "reject non-essential" as a first-class action; a reject
            that takes three clicks when accept takes one is the pattern regulators name.
            Defaults true and `setCookieBanner` rejects false with a 400.

            '
        noticeVersion:
          type: string
          description: 'Moves with `PolicyKind.cookie` via `setPolicy`. **A consent is against a
            version or it is against nothing** — the same rule `Policy.version` already states.

            '
        languages:
          type: array
          items:
            type: string
          description: 'Must include every language the tenant''s storefront serves. RTL is not a
            flag here because `LocalisedRichText` and CMS-012 already handle it.

            '
        theme:
          type: string
          nullable: true
          description: Null inherits the storefront theme, which is the answer in almost all cases.
```

```yaml
  /tenant-config/cookies/technologies:
    get:
      operationId: listTrackingTechnologies
      x-ticvai-consumed-by:
        - "P13 CMS-025 Cookie, Tracking & Digital Technology Registry"
      x-ticvai-audience:
      - staff
      summary: The cookie and tracking registry
      description: '2.6.54 and 2.6.57. **The registry is the tenant''s, whether a vendor or our own
        crawler fills it** — the preference centre reads it, the audit report reads it backwards,
        and neither should have to ask a third party at render time.

        '
      tags:
      - content
      x-ticvai-permission: TENANT_CONFIGURE
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Registry
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/TrackingTechnology'
    post:
      operationId: recordCookieScan
      x-ticvai-consumed-by:
        - "P13 CMS-025 Cookie, Tracking & Digital Technology Registry"
      x-ticvai-audience:
      - staff
      - partner
      summary: Record the result of a site scan
      description: '2.6.57. **This is the one operation the buy-or-build decision changes, and it
        changes only who calls it.** A bought scanner posts its findings here through a partner
        credential; our own crawler posts the same payload. Everything downstream — the registry,
        the preference centre, the audit report, the administrator alert — is identical either way.

        **New technologies land as `detected`, never as `approved`.** A scan reports what the site
        does; it does not decide what the site may do.

        '
      tags:
      - content
      x-ticvai-permission: TENANT_CONFIGURE
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [scannedAt, channel, findings]
              properties:
                scannedAt: {type: string, format: date-time}
                channel: {type: string}
                scannerRef:
                  type: string
                  nullable: true
                  description: The vendor and scan id where bought. Null where ours.
                findings:
                  type: array
                  items:
                    $ref: '#/components/schemas/TrackingTechnology'
      responses:
        '202':
          description: 'Accepted. Returns the count of newly `detected` rows, which is what the
            2.6.57 alert is raised from.'

  /tenant-config/cookies/banner:
    put:
      operationId: setCookieBanner
      x-ticvai-consumed-by:
        - "P13 CMS-026 Cookie Banner & Preference Center Designer"
      x-ticvai-audience:
      - staff
      x-ticvai-config-scope: tenant
      summary: Configure the consent banner and preference centre
      description: '2.6.52, 2.6.54 and 2.6.64. **Tenant, not venue** — a cookie is set by a domain
        and a domain belongs to a tenant, so a per-venue banner would be a banner nobody could
        honour.

        '
      tags:
      - content
      x-ticvai-permission: TENANT_CONFIGURE
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CookieBannerConfig'
      responses:
        '200':
          description: Banner configuration
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CookieBannerConfig'
        '400':
          description: '`rejectIsOneClick` false, or a language the storefront does not serve.'

  /storefront/cookie-runtime:
    get:
      operationId: getCookieRuntime
      x-ticvai-audience:
      - anonymous
      security: []
      summary: What the page must render and what it must not load
      description: '2.6.52 and 2.6.58, and the reason script blocking is not expensive here. **The
        storefront asks this before it injects anything**, and 22.10.29''s analytics injection is
        built against the answer rather than retrofitted behind it.

        Returns the banner configuration, the approved technologies grouped by category, and — if
        the caller presents a `consentKey` — the decision already recorded against it, so a
        returning visitor is not asked twice.

        **Anonymous and unauthenticated by necessity**: the caller has not consented yet, so
        requiring a token would be setting state before consent to set state. It is cacheable at
        the edge per tenant and notice version, which is how 2.6.65''s one-second budget is met.

        '
      tags:
      - content
      x-ticvai-permission: null
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      x-ticvai-read-routing: replica
      parameters:
      - name: consentKey
        in: query
        required: false
        schema: {type: string}
      responses:
        '200':
          description: Runtime
          content:
            application/json:
              schema:
                type: object
                required: [banner, technologies, noticeVersion]
                properties:
                  banner:
                    $ref: '#/components/schemas/CookieBannerConfig'
                  technologies:
                    type: array
                    items:
                      $ref: '#/components/schemas/TrackingTechnology'
                  noticeVersion: {type: string}
                  decision:
                    type: object
                    nullable: true
                    description: Present only where a known `consentKey` was presented.
```

### 4b. `marketing-crm.yaml` — the record, the claim and the merge

```yaml
    DeviceConsent:
      x-ticvai-persistence: marketing.device_consent
      type: object
      required:
      - consentKey
      - categories
      - noticeVersion
      - decidedAt
      - scopePath
      properties:
        consentKey:
          type: string
          description: '**Opaque, issued by us, and not a device fingerprint.** 2.6.55 asks for a
            "user identifier/session id"; a value we mint and the browser stores is the narrowest
            thing that answers it, and it is the join key the claim below needs. A vendor-minted
            key would make the claim depend on a vendor read.

            '
        categories:
          type: array
          items:
            type: object
            required: [category, decision]
            properties:
              category:
                $ref: '../white-label.yaml#/components/schemas/CookieCategory'
              decision:
                $ref: '#/components/schemas/ConsentDecision'
        noticeVersion:
          type: string
        decidedAt:
          type: string
          format: date-time
        expiresAt:
          type: string
          format: date-time
          description: '**A device consent expires and a subject consent does not.** ADR-0047
            anchors every retention class to a person or a ticket and this has neither.
            `ConsentPurposeConfig.expiresAfterMonths` is the mechanism; the number needs
            ADR-0047 amending to carry the class.

            '
        claimedBySubjectId:
          type: string
          format: uuid
          nullable: true
          readOnly: true
          description: Set once, by claimDeviceConsent. Never cleared.
        scopePath:
          type: string
          description: '**Tenant-scoped, and the column is here because `ConsentRecord` has not
            got one.** `recordConsent` is `subject`-scoped and correctly needs no partition key;
            a consent with no subject does.

            '

    ConsentIdentifier:
      x-ticvai-persistence: pii.consent_identifier
      type: object
      required:
      - consentRecordRef
      properties:
        consentRecordRef:
          type: string
          description: The `marketing.consent_record` id or the `consentKey`.
        ipAddress:
          type: string
          nullable: true
          description: '2.6.55, *"if legally permitted"*. **In `pii` rather than beside the
            decision, because it is the only personal datum in the consent path** — ADR-0023 holds
            zero operations touching both stores, and putting an IP in `marketing` would put
            personal data outside the erasable store for the sake of one column.

            '
        userAgent:
          type: string
          nullable: true
        capturedAt:
          type: string
          format: date-time
```

```yaml
  /consent/device:
    post:
      operationId: recordDeviceConsent
      x-ticvai-consumed-by:
        - "P01 WEB-024 Devices, Wishlist & Consent"
      x-ticvai-audience:
      - anonymous
      - guest
      security: []
      summary: Record a banner decision, before anyone is known
      description: '2.6.52 and 2.6.55. **Append-only, like `recordConsent`** — a change of mind is
        a new record. Mints a `consentKey` where none is presented and returns it for the browser
        to store; that cookie is strictly necessary and needs no consent to set, which is the only
        reason this operation can exist at all.

        **Tenant-scoped, so one tenant''s domains share one key** — that is 2.6.62, and it is free
        because we issue the key. **Not shared across tenants**: two tenants are two controllers
        and one guest''s consent to one is not consent to the other.

        '
      tags:
      - consent
      x-ticvai-permission: null
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: append
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeviceConsent'
      responses:
        '201':
          description: Recorded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeviceConsent'
        '400':
          description: Notice version unknown, or a category not configured for the tenant.

  /guests/{subjectId}/consents/claim-device:
    post:
      operationId: claimDeviceConsent
      x-ticvai-consumed-by:
        - "P01 WEB-016 Login / Register"
        - "P01 WEB-024 Devices, Wishlist & Consent"
        - "P02 GST-042 Simple Registration & OTP"
      x-ticvai-audience:
      - guest
      security:
      - guestAuth: []
      - bearerAuth: []
      x-ticvai-self-scoped: subject
      summary: Attach a browser''s consent to the person who turned out to own it
      description: '**The operation the whole design exists for.** At login or registration the
        browser holds a decision and the platform gains a subject; this joins them and is where
        CF-160 runs.

        **The result is the narrower of the two, per category.** A guest who rejected analytics on
        this browser and has `granted` on their profile ends `withdrawn` here; the reverse also
        ends `withdrawn`. **Inheriting the more permissive answer is how a merge becomes a
        breach** — `mergeGuestProfiles` already says so, and a device claim is a merge with one
        side anonymous.

        **`claimedBySubjectId` is set once and never cleared**, so a shared kiosk browser cannot
        later hand one guest''s decision to the next. A second claim against a claimed key is a
        409, not a silent overwrite.

        Writes a `ConsentRecord` per affected purpose through the existing path, so
        `getConsentHistory` shows the claim as the evidence it is.

        '
      tags:
      - consent
      x-ticvai-permission: null
      x-ticvai-scope-level: subject
      x-ticvai-config-scope: subject
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: append
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [consentKey]
              properties:
                consentKey: {type: string}
      responses:
        '200':
          description: The narrowed state
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConsentState'
        '409':
          description: The key is already claimed by another subject.

  /consent/cookie-analytics:
    get:
      operationId: getCookieConsentAnalytics
      x-ticvai-consumed-by:
        - "P13 CMS-039 Privacy Audit, Evidence & Compliance Reporting"
      x-ticvai-audience:
      - staff
      summary: Acceptance, rejection and category selection
      description: '2.6.63. **In `marketing-crm` rather than `reporting`, because it counts rows
        in `marketing.device_consent` at the moment it is asked.** `reporting` reads a warehouse;
        a compliance question asked about today cannot wait for a load.

        Geography is derived from the cell the consent was recorded in, not from the IP —
        **an IP in `pii` that a report has to join is an IP the report has to justify holding.**

        '
      tags:
      - consent
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-scope-level: tenant
      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Consent analytics
```

**One enum value changes on an existing schema:** `ConsentSource` gains `cookieBanner`. It holds
`guestApp`, `website`, `kiosk`, `pos`, `callCentre`, `import`, `agentRecorded` today, and
`website` would conflate a banner decision with a form submission — which is precisely the
distinction 2.6.56's audit trail has to be able to draw.

---

## 5. Recommendation

**Buy the scanner. Build the rest.** That is not a fudge between two answers; it is what section 2
produces when the six pieces are priced separately instead of together.

**The one reason:** of the six things "build" means, **five are cheap because the package already
ships the storefront, the theme, the translations, the policy versioning and the consent
register — and one, the cookie attribution database behind scanning, can never be built once.**
Everything else is a week's work against machinery that exists. The database is a subscription to
somebody else's ongoing labour, and that is exactly the thing worth paying for.

**What that looks like commercially:** a scanning-only or entry-tier subscription posting into
`recordCookieScan`, priced per tenant domain, instead of a full CMP licence per tenant storefront.
Cookiebot's per-domain tiers start at €15/month; OneTrust's cookie-consent floor is $10,000/year
plus implementation. The gap between those two numbers is the gap between buying a scanner and
buying a platform.

**What would change the recommendation:**

- **If the client wants a named vendor on the page for assurance reasons**, buy the platform. That
  is a procurement and comfort argument, not a technical one, and it is a legitimate one.
- **If P02 and the kiosk are descoped from 22.13.10**, the browser-only case gets stronger and a
  full CMP covers more of the surface.
- **If the client will not staff a registry owner**, buy the platform — a registry nobody
  maintains is worse than no registry, and that risk is identical whether we built the table or
  bought it.

**Drop is not available.** CF-127 says dropping requires that no tenant storefront sets a
non-essential cookie; 22.10.29 asks the CMS to integrate with analytics platforms, and 2.6.50's
AI-generated white-label site is a site somebody will measure.

**Sections 3 and 4 do not wait for this decision.** They are the same work under every answer,
they are startable now, and the longest-lead item in the whole of BL-073 is not the banner — it is
the `claimDeviceConsent` path, because it touches login, registration and the merge.

---

## 6. The UAE angle, and why it does not reduce the estimate

**The UAE has no equivalent to the ePrivacy Directive, and that is the material difference.**

> *"While there is no specific law regulating the use of cookies in the processing of personal
> data, existing personal data protection laws apply to their collection and use."*
> — [Chambers, *Data Protection & Privacy 2026: UAE*](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/uae/trends-and-developments)

The consequence is precise. **ePrivacy Article 5(3) regulates storage on a device as such** —
consent is required to store or access information on terminal equipment *whether or not that
information is personal data*, which the EDPB's Guidelines 2/2023 confirm covers identifiers,
local storage and tracking techniques well beyond cookies
([EDPB Guidelines 2/2023](https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf),
[Article 5(3) text and scope](https://deceptive.design/laws/eprivacy-directive-article-5-3/)).
**UAE PDPL regulates the processing of personal data.** A cookie that processes no personal data
is inside ePrivacy and outside PDPL. *Prior blocking of everything non-essential is an EU
obligation, not a UAE one.*

**Where a cookie does process personal data, the UAE standard is arguably tighter than GDPR in one
respect.** PDPL Article 4 opens with a prohibition on processing without consent and then lists a
closed set of exceptions. **There is no general legitimate-interests basis comparable to GDPR
Article 6(1)(f)**, and the list cannot be extended until the Executive Regulations do so
([DLA Piper, UAE](https://www.dlapiperdataprotection.com/countries/uae-general/law.html),
[Chambers 2026](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/uae/trends-and-developments)).
So the common European argument that first-party analytics rides on legitimate interests has no
UAE analogue — under UAE law it is consent or an enumerated exception.

Consent itself must be **free, specific, informed and unambiguous, obtainable in writing or
electronically, and withdrawable at any time**, with the method of withdrawal explained and easy;
silence, inactivity and pre-ticked boxes do not qualify
([CookieYes, UAE PDPL](https://www.cookieyes.com/blog/uae-data-protection-law-pdpl/),
[Secure Privacy, UAE PDPL](https://secureprivacy.ai/laws/uae-pdpl)). **That is the same banner we
would build for GDPR.** The design does not change; only the set of technologies it must gate
does.

**The federal regime is not yet fully operative.** The Executive Regulations to Federal Decree-Law
45/2021 remain unissued in 2026 — *"The Implementing Regulations, intended to clarify key aspects
of the law, have yet to be issued"* — organisations get **six further months from issuance** to
comply, no administrative penalties have been specified, and the mainland Data Office has not
become fully operational, with the TDRA acting as the point of contact in the interim
([Chambers 2026](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/uae/trends-and-developments),
[DLA Piper](https://www.dlapiperdataprotection.com/countries/uae-general/law.html)).

**What does bite now, and is not the federal PDPL:**

| Regime | Status |
|---|---|
| **DIFC Law 5/2020** | GDPR-aligned and enforced. July 2025 amendments gave data subjects a **private right of action** in the DIFC courts. Applies to entities licensed in the DIFC only. |
| **ADGM** | Separate regime, GDPR-aligned; September 2025 rules on special-category processing. |
| **Saudi PDPL** | Named in 2.6.60 and **the strictest live obligation of the set.** Enforceable since September 2023, grace ended September 2024, **Implementing Regulations in force**, SDAIA reported 48 enforcement decisions by early 2026, and opt-in consent with Arabic-language notices is expected for advertising and analytics cookies ([Baker McKenzie, KSA](https://resourcehub.bakermckenzie.com/en/resources/global-data-and-cyber-handbook/emea/saudi-arabia/topics/cookies-online-tracking-and-direct-marketing), [Chambers 2026, KSA](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/saudi-arabia)). |
| **TDRA / Cabinet Decision 56/2024** | Unsolicited electronic communications and telemarketing — consent before marketing messages. Touches `ConsentPurpose.marketing`, not cookies. |

### What this does to the estimate

**Nothing, unless the client changes 2.6.60.** The requirement names GDPR, the ePrivacy Directive,
CCPA, CPRA, LGPD and PDPL **by name**, and a contractual scope is not reduced by a legal finding.
The honest statement to Qossai is:

**If the storefronts serve EU visitors, ePrivacy sets the bar and the full build is required.** If
they serve UAE and KSA only, the *legal* floor is lower — consent for cookies that process
personal data, on the Saudi rather than the Emirati clock — **but the contractual floor is
unchanged.** Effort falls only if the client agrees to narrow 2.6.60, and that is an amendment to
the requirement, not a research result.

**One thing the UAE position does change:** the 2.6.60 vendor question. CMPs ship configurable
frameworks for GDPR, ePrivacy, CCPA, CPRA and LGPD. **There is no UAE cookie framework for a
vendor to ship, because there is no UAE cookie rule.** Whoever is asked to demonstrate PDPL
compliance on 2.6.60 will be demonstrating a position we wrote, against a register we hold —
which is section 3 again, arriving from the legal side.

---

## Derivations

| Number | How it was obtained |
|---|---|
| 17 requirement refs | `refs` array of BL-073 in `handoff/contract-backlog.json` — 15 in 2.6.x, plus 22.10.29 and 22.13.10 |
| The 15 requirement texts | `sources/requirements/Ticvai_matrix_20260621_2.xlsx`, sheet `Funactionality `, rows matched on `Requirement ID` 2.6.51–2.6.65, columns `Requirement` and `Additional Details` (all 15 `Additional Details` are empty) |
| 11 covered / 4 not | Each of the 15 classed by hand against standard CMP feature sets; the classification is in the two tables in section 1 and is the part to challenge |
| 19 privacy operations, 18 provisional | `contracts/satellite/marketing-crm.yaml` parsed; operations whose `x-ticvai-consumed-by` cites `P13 CMS-021` … `CMS-039`. `setConsentPurposes` (CMS-023) is the one that is not provisional |
| 36 / 21 / 28 properties | Property counts of `CookieTrackingDigitalTechnologyRegistryView`, `CookieBannerPreferenceCenterDesignerView`, `ConsentCapturePointCustomerJourneyConfigurationInput` |
| 577 provisional operations package-wide | All 32 contracts parsed for `x-ticvai-provisional: true`; matches the figure ADR-0047 cites |
| Six governed channels | The last six properties of `CookieTrackingDigitalTechnologyRegistryView` |
| No tag injection in `white-label` | Case-insensitive search of `contracts/satellite/white-label.yaml` for `tag manager`, `gtm`, `google analytics` — zero matches |
| 22.13.10 uncovered | Searched for the literal ref across all `.yaml` and `.md` in the package — zero occurrences outside the backlog's `refs` array |
| Vendor pricing | Published 2026 figures, cited inline in section 2. Cookiebot per-domain tiers and OneTrust's floor, median and implementation range |
| UAE and KSA positions | Cited inline in section 6 |

**Not derived, and deliberately not invented:** a person-week figure. The package has never used
one — `build-plan-20-september.md` sizes work in operations, schemas and decisions — and section 2
is priced the same way. **A day count invented here would be the only number in this paper without
a source.**
