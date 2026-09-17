"""MarketingService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

166 operations · 53 tables touched · scope levels: tenant, venue
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="MarketingService", docs_url="/_docs")

# **Pool size is the number the benchmark is for.** A per-venue topology multiplies this by the
# venue count against one primary; a shared topology does not. Set it from the environment so the
# same image runs in all three.
POOL_MIN = int(os.getenv("PG_POOL_MIN", "2"))
POOL_MAX = int(os.getenv("PG_POOL_MAX", "10"))
REDIS = os.getenv("REDIS_URL", "redis://redis:6379/0")

# **One service, many tenant databases** (ADR-0038). The instance is the region and the database
# is the tenant, so a service is not deployed per tenant — it is shared, scaled on traffic, and
# routed per request to a tenant database by tenant id.
#
# **Which makes the pool numbers above per tenant rather than per service**, and that is the whole
# of ADR-0032's amendment: `PG_POOL_MAX` of 20 across 25 concurrent tenants is 500 server
# connections, which is `max_connections` exactly. The benchmark measures this on purpose.
CONTROL_DSN = os.getenv("PG_CONTROL_DSN", "postgres://ticvai:ticvai@pgbouncer:6432/control")
TENANT_DSN = os.getenv("PG_TENANT_DSN_TEMPLATE",
                       "postgres://ticvai:ticvai@pgbouncer:6432/{database}")
TENANT_HEADER = os.getenv("TENANT_HEADER", "x-ticvai-tenant")

# **A request with no tenant is a bug, not a default** — except in the benchmark, which drives
# every operation without an authenticated caller. Named so the fallback is visible in the logs
# rather than looking like a tenant.
DEFAULT_TENANT = os.getenv("DEFAULT_TENANT", "")

class _Rollback(Exception):
    """Raised to undo a benchmark write. **Never escapes `run`.**"""


# **A pool per tenant database, made on first use and kept.** Sixteen services times two
# hundred tenants is not a connection budget anybody has, so the pool is opened when a tenant
# first arrives and the size is what `PG_POOL_MIN/MAX` say. This is the cost ADR-0038 accepted
# and it belongs in the artefact rather than in the ADR alone.
control_pool: asyncpg.Pool | None = None
pools: dict[str, asyncpg.Pool] = {}
databases: dict[str, str] = {}
cache = None


async def database_for(tenant: str) -> str:
    """The tenant's database name in this cell, from `control.cell_tenant`.

    **The control plane is asked, not the name guessed.** ADR-0039 keeps the mapping in a table
    precisely so a tenant can be moved, suspended or renamed without every service agreeing on a
    naming convention first.
    """
    if tenant in databases:
        return databases[tenant]
    async with control_pool.acquire() as con:
        row = await con.fetchrow(
            "SELECT database_name FROM control.cell_tenant "
            " WHERE tenant_id = $1 AND status = 'live' LIMIT 1", tenant)
    # **No row is not the same as no database.** A tenant the control plane does not place here
    # is a tenant in another region, and answering from a fallback would read that region's
    # request against this region's data.
    if not row:
        raise KeyError(tenant)
    databases[tenant] = row["database_name"]
    return databases[tenant]


async def pool_for(tenant: str) -> asyncpg.Pool:
    if tenant not in pools:
        dsn = TENANT_DSN.format(database=await database_for(tenant))
        pools[tenant] = await asyncpg.create_pool(dsn, min_size=POOL_MIN, max_size=POOL_MAX)
    return pools[tenant]


@app.on_event("startup")
async def _start() -> None:
    global control_pool, cache
    # **Cold start is one of the twenty metrics.** Timed here rather than inferred from the
    # orchestrator, because a pool that fills lazily makes the first request the slow one and the
    # container look healthy.
    #
    # **Only the control pool is opened at startup.** A tenant pool is opened on that tenant's
    # first request, so cold start is now a per-tenant number as well as a per-container one —
    # which is a real consequence of ADR-0038 and worth measuring rather than hiding.
    t0 = time.perf_counter()
    control_pool = await asyncpg.create_pool(CONTROL_DSN, min_size=1, max_size=4)
    cache = aioredis.from_url(REDIS, decode_responses=True)
    app.state.cold_start_ms = round((time.perf_counter() - t0) * 1000, 1)


@app.get("/_health")
async def health() -> dict:
    # **Reported per tenant and in total.** One number across every tenant database is the
    # number that made `max_connections` look comfortable while a Saturday evening was not.
    return {"service": "MarketingService", "operations": 166,
            "coldStartMs": getattr(app.state, "cold_start_ms", None),
            "tenantPools": len(pools),
            "poolSize": sum(p.get_size() for p in pools.values()),
            "poolIdle": sum(p.get_idle_size() for p in pools.values()),
            "controlPoolSize": control_pool.get_size() if control_pool else 0}


async def run(op: str, scope: str | None, tenant: str | None = None) -> dict:
    """Execute one operation's declared database work, against one tenant's database.

    **Scope is passed as a parameter, not as a deployment.** A venue-scoped operation filters on
    `scope_path`; that is true whether the service is shared or per-venue, and it is the whole
    point of the comparison.

    **Tenant is a connection, not a parameter.** ADR-0038 put a database around each tenant, so
    the query does not filter on `tenant_id` inside a tenant database — a column that says which
    tenant you are while you are inside that tenant's database is a column that will eventually
    disagree with the database it is in.
    """
    t0 = time.perf_counter()
    rows = 0
    pool = await pool_for(tenant or DEFAULT_TENANT)
    async with pool.acquire() as con:
        for sql in READS.get(op, ()):
            rows += len(await con.fetch(sql, *( (scope + "%",) if "$1" in sql else () )))
        # **Wrapped in a transaction that always rolls back.** A benchmark that leaves rows
        # changes the table it is measuring against, so the second run is not the first. The
        # assignment that used to sit here — `raise_rollback = True` — did nothing: asyncpg
        # commits unless the block raises, so every write was being kept.
        if WRITES.get(op):
            try:
                async with con.transaction():
                    for sql in WRITES[op]:
                        await con.fetch(sql, *( (scope + "%",) if "$1" in sql else () ))
                    raise _Rollback()
            except _Rollback:
                pass
    for key in CACHE.get(op, ()):
        await cache.get(key)
    return {"op": op, "rows": rows, "ms": round((time.perf_counter() - t0) * 1000, 2)}



@app.post("/loyalty/accruals")
async def accrue_loyalty_points(request: Request) -> dict:
    """Award points for a completed order

    scope: venue · permission: LOYALTY_ACCRUE · offline: False
    """
    return await run("accrueLoyaltyPoints", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journeys/{journeyId}/activate")
async def activate_journey(request: Request) -> dict:
    """Start it, or stop it

    scope: venue · permission: MARKETING_SEND · offline: False
    """
    return await run("activateJourney", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cases/{caseId}/messages")
async def add_case_message(request: Request) -> dict:
    """Add a message or internal note

    scope: venue · permission: CASE_MANAGE · offline: True
    """
    return await run("addCaseMessage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/notes")
async def add_guest_note(request: Request) -> dict:
    """What the floor needs to know about this table

    scope: venue · permission: GUEST_MANAGE · offline: True
    """
    return await run("addGuestNote", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/consent/suppression-list")
async def add_suppression(request: Request) -> dict:
    """Suppress an address

    scope: tenant · permission: GUEST_MANAGE · offline: False
    """
    return await run("addSuppression", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/wishlist")
async def add_to_wishlist(request: Request) -> dict:
    """Save an item

    scope: venue · permission: - · offline: False
    """
    return await run("addToWishlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/loyalty/adjust")
async def adjust_loyalty_points(request: Request) -> dict:
    """Manually adjust points

    scope: venue · permission: LEDGER_POST · offline: False
    """
    return await run("adjustLoyaltyPoints", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/privacy-testing")
async def approve_privacy_testing(request: Request) -> dict:
    """Privacy Configuration Testing, Approval & Publication

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("approvePrivacyTesting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/waiver-testing")
async def approve_waiver_testing(request: Request) -> dict:
    """Waiver Approval, Testing & Publication Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("approveWaiverTesting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/claim")
async def claim_conversation(request: Request) -> dict:
    """An agent takes it

    scope: tenant · permission: CASE_MANAGE · offline: False
    """
    return await run("claimConversation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/close")
async def close_conversation(request: Request) -> dict:
    """End it

    scope: tenant · permission: CASE_MANAGE · offline: False
    """
    return await run("closeConversation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns")
async def create_campaign(request: Request) -> dict:
    """Create a campaign

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cases")
async def create_case(request: Request) -> dict:
    """Raise a service case

    scope: venue · permission: CASE_MANAGE · offline: True
    """
    return await run("createCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/case-classification-intelligent")
async def create_case_classification_intelligent(request: Request) -> dict:
    """Case Creation, Classification & Intelligent Routing

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createCaseClassificationIntelligent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/challenges")
async def create_challenge(request: Request) -> dict:
    """Define a challenge, mission or streak

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createChallenge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/forms")
async def create_form(request: Request) -> dict:
    """Define a waiver, survey or capture form

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createForm", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invitation-campaigns")
async def create_invitation_campaign(request: Request) -> dict:
    """A quota-bounded, addressed invitation

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createInvitationCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/journeys")
async def create_journey(request: Request) -> dict:
    """Define an automated journey

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createJourney", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/loyalty/programmes")
async def create_loyalty_programme(request: Request) -> dict:
    """Create a loyalty programme

    scope: tenant · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createLoyaltyProgramme", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/message-templates")
async def create_message_template(request: Request) -> dict:
    """Create a message template

    scope: tenant · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createMessageTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/referrals")
async def create_referral(request: Request) -> dict:
    """Issue a referral code

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createReferral", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/segments")
async def create_segment(request: Request) -> dict:
    """Create a segment

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createSegment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/seo-redirects")
async def create_url_redirect(request: Request) -> dict:
    """301, 302 and custom redirects

    scope: tenant · permission: MARKETING_MANAGE · offline: False
    """
    return await run("createUrlRedirect", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kiosk-assists/{sessionId}/end")
async def end_kiosk_assist(request: Request) -> dict:
    """Stop assisting

    scope: venue · permission: - · offline: False
    """
    return await run("endKioskAssist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cases/{caseId}/escalate")
async def escalate_case(request: Request) -> dict:
    """Escalate a case

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("escalateCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaigns/{campaignId}")
async def get_campaign(request: Request) -> dict:
    """Read a campaign with performance

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("getCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaigns/{campaignId}/performance")
async def get_campaign_performance(request: Request) -> dict:
    """Delivery and engagement

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("getCampaignPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cases/{caseId}")
async def get_case(request: Request) -> dict:
    """Read a case with its thread

    scope: venue · permission: CASE_VIEW · offline: False
    """
    return await run("getCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/consents/history")
async def get_consent_history(request: Request) -> dict:
    """Full consent history

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getConsentHistory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/conversations/{conversationId}")
async def get_conversation(request: Request) -> dict:
    """One conversation and everything before it

    scope: tenant · permission: CASE_VIEW · offline: False
    """
    return await run("getConversation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/consents")
async def get_guest_consents(request: Request) -> dict:
    """Read a guest's consent state

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getGuestConsents", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/loyalty")
async def get_guest_loyalty(request: Request) -> dict:
    """A guest's loyalty position

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getGuestLoyalty", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}")
async def get_guest_profile(request: Request) -> dict:
    """Read a guest profile

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getGuestProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/journeys/{journeyId}/performance")
async def get_journey_performance(request: Request) -> dict:
    """Entrants, completions, goals reached

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("getJourneyPerformance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/lost-items/{itemId}/matches")
async def get_lost_item_matches(request: Request) -> dict:
    """Candidate matches, scored

    scope: venue · permission: CASE_VIEW · offline: False
    """
    return await run("getLostItemMatches", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/loyalty/position")
async def get_loyalty_position(request: Request) -> dict:
    """A guest's points, tier and what is within reach

    scope: tenant · permission: - · offline: False
    """
    return await run("getLoyaltyPosition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/marketing-subscriptions")
async def get_marketing_subscription(request: Request) -> dict:
    """What this guest has opted into

    scope: tenant · permission: MARKETING_VIEW · offline: False
    """
    return await run("getMarketingSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/messages/{messageId}")
async def get_message_status(request: Request) -> dict:
    """Delivery status of one message

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getMessageStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/me/challenges")
async def get_my_challenges(request: Request) -> dict:
    """Active challenges and how far along I am

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("getMyChallenges", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/consent/suppression-list")
async def get_suppression_list(request: Request) -> dict:
    """Addresses suppressed from all sending

    scope: tenant · permission: GUEST_VIEW · offline: False
    """
    return await run("getSuppressionList", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/waiver-status")
async def get_waiver_status(request: Request) -> dict:
    """Whether this guest may be issued a ticket that requires a waiver

    scope: venue · permission: GUEST_VIEW · offline: True
    """
    return await run("getWaiverStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/wishlist")
async def get_wishlist(request: Request) -> dict:
    """Read a guest's saved items

    scope: venue · permission: - · offline: False
    """
    return await run("getWishlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/handover")
async def handover_to_agent(request: Request) -> dict:
    """Pass an assistant conversation to a person

    scope: tenant · permission: - · offline: False
    """
    return await run("handoverToAgent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/identify")
async def identify_guest(request: Request) -> dict:
    """Resolve any identifier to a guest

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("identifyGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns/{campaignId}/launch")
async def launch_campaign(request: Request) -> dict:
    """Launch or schedule a campaign

    scope: venue · permission: MARKETING_SEND · offline: False
    """
    return await run("launchCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/agent-workload-availability")
async def list_agent_workload_availability(request: Request) -> dict:
    """Agent Workload, Availability & Workforce Control

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listAgentWorkloadAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/business-event-notification")
async def list_business_event_notification(request: Request) -> dict:
    """Business Event & Notification Trigger Mapping

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listBusinessEventNotification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/campaigns")
async def list_campaigns(request: Request) -> dict:
    """List campaigns

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCampaigns", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/case-resolution-closure")
async def list_case_resolution_closure(request: Request) -> dict:
    """Case Resolution, Closure & Customer Feedback

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCaseResolutionClosure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cases")
async def list_cases(request: Request) -> dict:
    """List service cases

    scope: venue · permission: CASE_VIEW · offline: False
    """
    return await run("listCases", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/communication-service")
async def list_communication_service(request: Request) -> dict:
    """Communication Service Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCommunicationService", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/compliance-evidence-waiver")
async def list_compliance_evidence_waiver(request: Request) -> dict:
    """Compliance Evidence, Audit & Waiver Repository

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listComplianceEvidenceWaiver", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/consent-evidence-withdrawal")
async def list_consent_evidence_withdrawal(request: Request) -> dict:
    """Consent Evidence, History & Withdrawal Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listConsentEvidenceWithdrawal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/consent-preference-communication")
async def list_consent_preference_communication(request: Request) -> dict:
    """Consent, Preference & Communication Policy Enforcement

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listConsentPreferenceCommunication", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/consent-purposes")
async def list_consent_purposes(request: Request) -> dict:
    """Configured consent purposes

    scope: tenant · permission: GUEST_VIEW · offline: True
    """
    return await run("listConsentPurposes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/contact")
async def list_contact(request: Request) -> dict:
    """Contact Center Operations Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listContact", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/contact-automation")
async def list_contact_automation(request: Request) -> dict:
    """AI Contact Center Intelligence & Automation Studio

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listContactAutomation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/conversations")
async def list_conversations(request: Request) -> dict:
    """The omnichannel inbox

    scope: tenant · permission: CASE_VIEW · offline: False
    """
    return await run("listConversations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cookie-banner-preference")
async def list_cookie_banner_preference(request: Request) -> dict:
    """Cookie Banner & Preference Center Designer

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCookieBannerPreference", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/cookie-tracking-digital")
async def list_cookie_tracking_digital(request: Request) -> dict:
    """Cookie, Tracking & Digital Technology Registry

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCookieTrackingDigital", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-privacy-consent")
async def list_customer_privacy_consent(request: Request) -> dict:
    """Customer Privacy, Consent & Preference 360°

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCustomerPrivacyConsent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-satisfaction-feedback")
async def list_customer_satisfaction_feedback(request: Request) -> dict:
    """Customer Satisfaction, Feedback & Voice of Customer

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCustomerSatisfactionFeedback", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-service")
async def list_customer_service(request: Request) -> dict:
    """Customer Service Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCustomerService", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/customer-service-profile")
async def list_customer_service_profile(request: Request) -> dict:
    """Customer 360° Service Profile

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listCustomerServiceProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/data-processing-purpose")
async def list_data_processing_purpose(request: Request) -> dict:
    """Data Processing Purpose & Lawful Basis Registry

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDataProcessingPurpose", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/data-retention-expiry")
async def list_data_retention_expiry(request: Request) -> dict:
    """Data Retention, Expiry & Legal Hold Operations

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDataRetentionExpiry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/data-subject-customer")
async def list_data_subject_customer(request: Request) -> dict:
    """Data Subject / Customer Privacy Request Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDataSubjectCustomer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/deletion-anonymization-restriction")
async def list_deletion_anonymization_restriction(request: Request) -> dict:
    """Deletion, Anonymization & Restriction Operations

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDeletionAnonymizationRestriction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/delivery-communication-platform")
async def list_delivery_communication_platform(request: Request) -> dict:
    """AI Delivery Optimization & Communication Platform Diagnostics

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDeliveryCommunicationPlatform", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/delivery-queue-failure")
async def list_delivery_queue_failure(request: Request) -> dict:
    """Delivery Queue, Failure & Retry Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDeliveryQueueFailure", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/digital-signing-collection")
async def list_digital_signing_collection(request: Request) -> dict:
    """Digital Signing & Collection Operations

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDigitalSigningCollection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-field-question")
async def list_dynamic_field_question(request: Request) -> dict:
    """Dynamic Fields, Questions & Conditional Logic

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listDynamicFieldQuestion", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/escalation-collaboration-internal")
async def list_escalation_collaboration_internal(request: Request) -> dict:
    """Escalation, Collaboration & Internal Resolution

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listEscalationCollaborationInternal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/escalation-critical-case")
async def list_escalation_critical_case(request: Request) -> dict:
    """Escalation & Critical Case Monitor

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listEscalationCriticalCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/devices")
async def list_guest_devices(request: Request) -> dict:
    """A guest's registered devices

    scope: tenant · permission: - · offline: False
    """
    return await run("listGuestDevices", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/journeys")
async def list_journeys(request: Request) -> dict:
    """Automated journeys

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listJourneys", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/lost-items")
async def list_lost_items(request: Request) -> dict:
    """Reported and found, with suggested matches

    scope: venue · permission: CASE_VIEW · offline: False
    """
    return await run("listLostItems", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/loyalty/programmes")
async def list_loyalty_programmes(request: Request) -> dict:
    """List loyalty programmes

    scope: venue · permission: MARKETING_VIEW · offline: True
    """
    return await run("listLoyaltyProgrammes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/message-templates")
async def list_message_templates(request: Request) -> dict:
    """List message templates

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listMessageTemplates", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/message-triggers")
async def list_message_triggers(request: Request) -> dict:
    """What fires a message, and when

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listMessageTriggers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/minor-guardian-group")
async def list_minor_guardian_group(request: Request) -> dict:
    """Minor, Guardian & Group Consent Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listMinorGuardianGroup", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/missing-expired-invalid")
async def list_missing_expired_invalid(request: Request) -> dict:
    """Missing, Expired & Invalid Waiver Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listMissingExpiredInvalid", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/my/cases")
async def list_my_cases(request: Request) -> dict:
    """The cases this guest raised

    scope: tenant · permission: - · offline: False
    """
    return await run("listMyCases", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/participant-waiver-statu")
async def list_participant_waiver_status(request: Request) -> dict:
    """Participant Waiver Status & Tracking

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listParticipantWaiverStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/privacy")
async def list_privacy(request: Request) -> dict:
    """Privacy Operations Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listPrivacy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/privacy-compliance")
async def list_privacy_compliance(request: Request) -> dict:
    """Privacy Analytics & AI Compliance Intelligence

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listPrivacyCompliance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/privacy-consent")
async def list_privacy_consent(request: Request) -> dict:
    """Privacy & Consent Configuration Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listPrivacyConsent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/privacy-evidence-compliance")
async def list_privacy_evidence_compliance(request: Request) -> dict:
    """Privacy Audit, Evidence & Compliance Reporting

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listPrivacyEvidenceCompliance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/privacy-notice-policy")
async def list_privacy_notice_policy(request: Request) -> dict:
    """Privacy Notice, Policy & Terms Version Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listPrivacyNoticePolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/product-event-experience")
async def list_product_event_experience(request: Request) -> dict:
    """Product, Event & Experience Association

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listProductEventExperience", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/provider-health-usage")
async def list_provider_health_usage(request: Request) -> dict:
    """Provider Health, Usage & Cost Monitoring

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listProviderHealthUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/quality-agent-evaluation")
async def list_quality_agent_evaluation(request: Request) -> dict:
    """Quality Management & Agent Evaluation

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listQualityAgentEvaluation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reviews")
async def list_reviews(request: Request) -> dict:
    """List guest reviews and ratings

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listReviews", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/routing-priority-throttling")
async def list_routing_priority_throttling(request: Request) -> dict:
    """Routing, Priority, Throttling & Fallback Rules

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listRoutingPriorityThrottling", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/segments/{segmentId}/members")
async def list_segment_members(request: Request) -> dict:
    """List guests currently matching a segment

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listSegmentMembers", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/segments")
async def list_segments(request: Request) -> dict:
    """List segments

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listSegments", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/service-root-cause")
async def list_service_root_cause(request: Request) -> dict:
    """Service Analytics & Root-Cause Intelligence

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listServiceRootCause", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/site-waiver-exception")
async def list_site_waiver_exception(request: Request) -> dict:
    """On-Site Waiver & Exception Handling

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listSiteWaiverException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/sla-policy-service")
async def list_sla_policy_service(request: Request) -> dict:
    """SLA Policy & Service-Level Management

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listSlaPolicyService", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/system-transactional-template")
async def list_system_transactional_template(request: Request) -> dict:
    """System Transactional Template Registry

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listSystemTransactionalTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/unified-interaction-communication")
async def list_unified_interaction_communication(request: Request) -> dict:
    """Unified Interaction & Communication History

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listUnifiedInteractionCommunication", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/versioning-effective-date")
async def list_versioning_effective_date(request: Request) -> dict:
    """Versioning, Effective Dates & Legal Change Control

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listVersioningEffectiveDate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver")
async def list_waiver(request: Request) -> dict:
    """Waiver Operations Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiver", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver-compliance-operational")
async def list_waiver_compliance_operational(request: Request) -> dict:
    """Waiver Analytics, Compliance & Operational Insights

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiverComplianceOperational", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver-compliance-risk")
async def list_waiver_compliance_risk(request: Request) -> dict:
    """AI Waiver Compliance & Risk Intelligence Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiverComplianceRisk", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver-consent")
async def list_waiver_consent(request: Request) -> dict:
    """Waiver & Consent Command Center

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiverConsent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver-template-master")
async def list_waiver_template_master(request: Request) -> dict:
    """Waiver Template Library & Master Setup

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiverTemplateMaster", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/waiver-trigger-eligibility")
async def list_waiver_trigger_eligibility(request: Request) -> dict:
    """Waiver Trigger, Eligibility & Completion Rules

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("listWaiverTriggerEligibility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/match")
async def match_guest(request: Request) -> dict:
    """Is this the same person we already have?

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("matchGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/lost-items/{itemId}/match")
async def match_lost_item(request: Request) -> dict:
    """Tie a report to a found item, or hand it back

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("matchLostItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/merge")
async def merge_guest_profiles(request: Request) -> dict:
    """Merge a duplicate profile into this one

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("mergeGuestProfiles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/merge")
async def merge_guests(request: Request) -> dict:
    """Two records, one person

    scope: tenant · permission: GUEST_MANAGE · offline: False
    """
    return await run("mergeGuests", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns/{campaignId}/pause")
async def pause_campaign(request: Request) -> dict:
    """Pause a campaign mid-send

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("pauseCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/segments/{segmentId}/preview")
async def preview_segment(request: Request) -> dict:
    """Estimate segment size and reachability

    scope: venue · permission: MARKETING_VIEW · offline: False
    """
    return await run("previewSegment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/my/cases")
async def raise_my_case(request: Request) -> dict:
    """Report something — lost property, a complaint, a question

    scope: tenant · permission: - · offline: True
    """
    return await run("raiseMyCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/consents")
async def record_consent(request: Request) -> dict:
    """Record a consent decision

    scope: venue · permission: - · offline: False
    """
    return await run("recordConsent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/lost-items")
async def record_lost_item(request: Request) -> dict:
    """Report something lost, or hand something in

    scope: venue · permission: CASE_MANAGE · offline: True
    """
    return await run("recordLostItem", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/privacy-incidents")
async def record_privacy_incident(request: Request) -> dict:
    """Log a personal-data breach and start the clock

    scope: tenant · permission: GUEST_MANAGE · offline: False
    """
    return await run("recordPrivacyIncident", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/attribution/touches")
async def record_touch_point(request: Request) -> dict:
    """Record a marketing touch

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("recordTouchPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/loyalty/redemptions")
async def redeem_loyalty_points(request: Request) -> dict:
    """Spend points

    scope: venue · permission: LOYALTY_REDEEM · offline: False
    """
    return await run("redeemLoyaltyPoints", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/devices")
async def register_guest_device(request: Request) -> dict:
    """Register a device for push

    scope: tenant · permission: - · offline: False
    """
    return await run("registerGuestDevice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/guests/{subjectId}/wishlist/{itemId}")
async def remove_from_wishlist(request: Request) -> dict:
    """Remove a saved item

    scope: venue · permission: - · offline: False
    """
    return await run("removeFromWishlist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/cases/{caseId}/reopen")
async def reopen_case(request: Request) -> dict:
    """Reopen a resolved case

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("reopenCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/my/cases/{caseId}/messages")
async def reply_to_my_case(request: Request) -> dict:
    """Reply on a case the guest raised

    scope: tenant · permission: - · offline: False
    """
    return await run("replyToMyCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/invitations/{token}/respond")
async def respond_to_invitation(request: Request) -> dict:
    """Accept or decline

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("respondToInvitation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reviews/{reviewId}/respond")
async def respond_to_review(request: Request) -> dict:
    """Respond to a review

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("respondToReview", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/message-dispatches/{dispatchId}/retry")
async def retry_message_dispatch(request: Request) -> dict:
    """Send it again, or by another channel

    scope: venue · permission: MARKETING_SEND · offline: False
    """
    return await run("retryMessageDispatch", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/guests/{subjectId}/devices/{deviceId}")
async def revoke_guest_device(request: Request) -> dict:
    """Revoke a device registration

    scope: tenant · permission: - · offline: False
    """
    return await run("revokeGuestDevice", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests")
async def search_guests(request: Request) -> dict:
    """Search guest profiles

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("searchGuests", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/messages")
async def send_conversation_message(request: Request) -> dict:
    """Say something, as a guest or an agent

    scope: tenant · permission: CASE_MANAGE · offline: False
    """
    return await run("sendConversationMessage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/messages")
async def send_transactional_message(request: Request) -> dict:
    """Send a transactional message

    scope: venue · permission: - · offline: False
    """
    return await run("sendTransactionalMessage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/agent-availability")
async def set_agent_availability(request: Request) -> dict:
    """An agent goes available, away or offline

    scope: tenant · permission: CASE_MANAGE · offline: False
    """
    return await run("setAgentAvailability", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/disposition")
async def set_call_disposition(request: Request) -> dict:
    """Why the conversation ended, and any callback

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("setCallDisposition", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/case-investigation-resolution")
async def set_case_investigation_resolution(request: Request) -> dict:
    """Case Investigation & Resolution Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setCaseInvestigationResolution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/channel-provider")
async def set_channel_provider(request: Request) -> dict:
    """Channel & Provider Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setChannelProvider", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/communication-preference-marketing")
async def set_communication_preference_marketing(request: Request) -> dict:
    """Communication Preference & Marketing Permission Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setCommunicationPreferenceMarketing", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/consent-capture-point")
async def set_consent_capture_point(request: Request) -> dict:
    """Consent Capture Point & Customer Journey Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setConsentCapturePoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/consent-purposes")
async def set_consent_purposes(request: Request) -> dict:
    """Configure consent purposes

    scope: tenant · permission: GUEST_MANAGE · offline: False
    """
    return await run("setConsentPurposes", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/customer-service-copilot")
async def set_customer_service_copilot(request: Request) -> dict:
    """AI Customer Service Copilot & Knowledge Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setCustomerServiceCopilot", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/data-discovery-access")
async def set_data_discovery_access(request: Request) -> dict:
    """Data Discovery, Access, Export & Correction Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setDataDiscoveryAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/digital-waiver-form")
async def set_digital_waiver_form(request: Request) -> dict:
    """Digital Waiver & Form Builder

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setDigitalWaiverForm", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/intelligent-routing-skill")
async def set_intelligent_routing_skill(request: Request) -> dict:
    """Intelligent Routing, Skills & Assignment Engine

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setIntelligentRoutingSkill", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/localization-branding-customer")
async def set_localization_branding_customer(request: Request) -> dict:
    """Localization, Branding & Customer Experience Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setLocalizationBrandingCustomer", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/marketing-subscriptions")
async def set_marketing_subscription(request: Request) -> dict:
    """Subscribe or unsubscribe

    scope: tenant · permission: MARKETING_VIEW · offline: False
    """
    return await run("setMarketingSubscription", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/message-triggers")
async def set_message_trigger(request: Request) -> dict:
    """Fire a message from a platform event

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setMessageTrigger", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/minor-guardian-age")
async def set_minor_guardian_age(request: Request) -> dict:
    """Minor, Guardian & Age-Based Privacy Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setMinorGuardianAge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/order-booking-ticket")
async def set_order_booking_ticket(request: Request) -> dict:
    """Order, Booking & Ticket Service Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setOrderBookingTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/privacy-compliance-exception")
async def set_privacy_compliance_exception(request: Request) -> dict:
    """Privacy Compliance, Exception & Investigation Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setPrivacyComplianceException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/refund-compensation-service")
async def set_refund_compensation_service(request: Request) -> dict:
    """Refund, Compensation & Service Exception Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setRefundCompensationService", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/sender-identity-domain")
async def set_sender_identity_domain(request: Request) -> dict:
    """Sender Identity, Domain & Brand Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setSenderIdentityDomain", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/seo-metadata")
async def set_seo_metadata(request: Request) -> dict:
    """Titles, descriptions, canonicals and hreflang

    scope: tenant · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setSeoMetadata", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/signatory-signature-guardian")
async def set_signatory_signature_guardian(request: Request) -> dict:
    """Signatory, Signature & Guardian Rule Configuration

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setSignatorySignatureGuardian", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/waiver-verification-validation")
async def set_waiver_verification_validation(request: Request) -> dict:
    """Waiver Verification & Validation Workspace

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("setWaiverVerificationValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/kiosk-assists")
async def start_kiosk_assist(request: Request) -> dict:
    """A staff member helps a guest at a kiosk, remotely

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("startKioskAssist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns/{campaignId}/stop")
async def stop_campaign(request: Request) -> dict:
    """Stop a campaign mid-send

    scope: venue · permission: MARKETING_SEND · offline: False
    """
    return await run("stopCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/form-submissions")
async def submit_form(request: Request) -> dict:
    """Sign a waiver, answer a survey, capture details

    scope: venue · permission: GUEST_VIEW · offline: True
    """
    return await run("submitForm", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/reviews")
async def submit_review(request: Request) -> dict:
    """Submit a review

    scope: venue · permission: - · offline: False
    """
    return await run("submitReview", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns/{campaignId}/test-send")
async def test_send_campaign(request: Request) -> dict:
    """Send a test to named recipients

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("testSendCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/conversations/{conversationId}/transfer")
async def transfer_conversation(request: Request) -> dict:
    """Pass it to another agent or queue

    scope: tenant · permission: CASE_MANAGE · offline: False
    """
    return await run("transferConversation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/campaigns/{campaignId}/unschedule")
async def unschedule_campaign(request: Request) -> dict:
    """Pull a scheduled campaign before it sends

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("unscheduleCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/campaigns/{campaignId}")
async def update_campaign(request: Request) -> dict:
    """Amend, pause or resume a campaign

    scope: venue · permission: MARKETING_MANAGE · offline: False
    """
    return await run("updateCampaign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/cases/{caseId}")
async def update_case(request: Request) -> dict:
    """Assign, reprioritise or resolve a case

    scope: venue · permission: CASE_MANAGE · offline: False
    """
    return await run("updateCase", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/guests/{subjectId}/preferences")
async def update_guest_preferences(request: Request) -> dict:
    """The things a regular should not have to say twice

    scope: tenant · permission: GUEST_MANAGE · offline: False
    """
    return await run("updateGuestPreferences", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/guests/{subjectId}")
async def update_guest_profile(request: Request) -> dict:
    """Amend a guest profile

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("updateGuestProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/guests/me/profile")
async def update_my_profile(request: Request) -> dict:
    """A guest correcting their own details

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("updateMyProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guest-documents")
async def upload_guest_document(request: Request) -> dict:
    """Store a guest photo, ID or signed document

    scope: venue · permission: GUEST_VIEW_PII · offline: False
    """
    return await run("uploadGuestDocument", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

