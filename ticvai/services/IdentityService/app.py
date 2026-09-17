"""IdentityService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

44 operations · 25 tables touched · scope levels: tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="IdentityService", docs_url="/_docs")

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
    return {"service": "IdentityService", "operations": 44,
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



@app.post("/auth/sso/{providerId}/callback")
async def complete_sso_authorization(request: Request) -> dict:
    """Exchange an SSO code for a session

    scope: tenant · permission: - · offline: False
    """
    return await run("completeSsoAuthorization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/delegated-access")
async def create_delegated_access(request: Request) -> dict:
    """Assign a grant

    scope: venue · permission: PERMISSION_GRANT · offline: False
    """
    return await run("createDelegatedAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/mfa/challenge")
async def create_mfa_challenge(request: Request) -> dict:
    """Step-up authentication for a sensitive action

    scope: tenant · permission: - · offline: False
    """
    return await run("createMfaChallenge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/principals")
async def create_principal(request: Request) -> dict:
    """Create a principal

    scope: venue · permission: USER_MANAGE · offline: False
    """
    return await run("createPrincipal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/roles")
async def create_role(request: Request) -> dict:
    """Create a role

    scope: venue · permission: ROLE_MANAGE · offline: False
    """
    return await run("createRole", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/delegated-access/{delegatedAccessId}")
async def delete_delegated_access(request: Request) -> dict:
    """Remove a grant

    scope: venue · permission: PERMISSION_GRANT · offline: False
    """
    return await run("deleteDelegatedAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/auth/guest/account")
async def delete_guest_account(request: Request) -> dict:
    """Self-service account deletion

    scope: tenant · permission: - · offline: False
    """
    return await run("deleteGuestAccount", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/mfa/methods")
async def enrol_mfa_method(request: Request) -> dict:
    """Enrol an MFA method

    scope: tenant · permission: - · offline: False
    """
    return await run("enrolMfaMethod", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/data-export")
async def export_subject_data(request: Request) -> dict:
    """Everything the platform holds about one guest

    scope: tenant · permission: GUEST_VIEW_PII · offline: False
    """
    return await run("exportSubjectData", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/sessions/{sessionId}/force-logout")
async def force_logout(request: Request) -> dict:
    """Supervisor termination of an abandoned session

    scope: venue · permission: SESSION_FORCE_LOGOUT · offline: False
    """
    return await run("forceLogout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/session")
async def get_current_session(request: Request) -> dict:
    """Current session and effective permissions

    scope: workstation · permission: - · offline: True
    """
    return await run("getCurrentSession", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/guest/session")
async def get_guest_session(request: Request) -> dict:
    """Read the current guest session

    scope: tenant · permission: - · offline: True
    """
    return await run("getGuestSession", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/principals/{principalId}")
async def get_principal(request: Request) -> dict:
    """Read a principal

    scope: venue · permission: USER_MANAGE · offline: False
    """
    return await run("getPrincipal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/tenants/sso-config")
async def get_sso_config(request: Request) -> dict:
    """Read SSO configuration

    scope: tenant · permission: USER_MANAGE · offline: False
    """
    return await run("getSsoConfig", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/guests/{subjectId}/delegations")
async def grant_delegation(request: Request) -> dict:
    """Let one guest act for another

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("grantDelegation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/auth/guest/session")
async def guest_logout(request: Request) -> dict:
    """End a guest session

    scope: tenant · permission: - · offline: False
    """
    return await run("guestLogout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/social")
async def guest_social_login(request: Request) -> dict:
    """Sign in with Apple or Google

    scope: tenant · permission: - · offline: False
    """
    return await run("guestSocialLogin", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/uae-pass")
async def guest_uae_pass_login(request: Request) -> dict:
    """Sign in with a national identity provider

    scope: tenant · permission: - · offline: False
    """
    return await run("guestUaePassLogin", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/link-checkout")
async def link_guest_checkout(request: Request) -> dict:
    """Attach a guest checkout to an account

    scope: venue · permission: - · offline: False
    """
    return await run("linkGuestCheckout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/sessions")
async def list_active_sessions(request: Request) -> dict:
    """List active sessions

    scope: venue · permission: SESSION_FORCE_LOGOUT · offline: False
    """
    return await run("listActiveSessions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/delegated-access")
async def list_delegated_access(request: Request) -> dict:
    """List grants for a principal or role

    scope: venue · permission: PERMISSION_VIEW · offline: False
    """
    return await run("listDelegatedAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/{subjectId}/delegations")
async def list_delegations(request: Request) -> dict:
    """Who may act for this guest, and for whom they may act

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("listDelegations", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/mfa/methods")
async def list_mfa_methods(request: Request) -> dict:
    """Enrolled MFA methods

    scope: tenant · permission: - · offline: False
    """
    return await run("listMfaMethods", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/principals")
async def list_principals(request: Request) -> dict:
    """List principals

    scope: venue · permission: USER_MANAGE · offline: False
    """
    return await run("listPrincipals", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/roles")
async def list_roles(request: Request) -> dict:
    """List roles

    scope: venue · permission: ROLE_MANAGE · offline: True
    """
    return await run("listRoles", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/sso/providers")
async def list_sso_providers(request: Request) -> dict:
    """Identity providers configured for this tenant

    scope: tenant · permission: - · offline: False
    """
    return await run("listSsoProviders", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/login")
async def login(request: Request) -> dict:
    """Authenticate and open a session

    scope: tenant · permission: - · offline: False
    """
    return await run("login", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/logout")
async def logout(request: Request) -> dict:
    """Close the current session

    scope: workstation · permission: - · offline: True
    """
    return await run("logout", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/refresh")
async def refresh_token(request: Request) -> dict:
    """Rotate the access token

    scope: tenant · permission: - · offline: False
    """
    return await run("refreshToken", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/register")
async def register_guest(request: Request) -> dict:
    """Create a guest account

    scope: tenant · permission: - · offline: False
    """
    return await run("registerGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/auth/mfa/methods/{methodId}")
async def remove_mfa_method(request: Request) -> dict:
    """Remove an MFA method

    scope: tenant · permission: - · offline: False
    """
    return await run("removeMfaMethod", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/otp")
async def request_guest_otp(request: Request) -> dict:
    """Request a one-time code

    scope: tenant · permission: - · offline: False
    """
    return await run("requestGuestOtp", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/permissions/resolve")
async def resolve_permissions(request: Request) -> dict:
    """Simulate a principal's effective permissions

    scope: venue · permission: PERMISSION_VIEW · offline: False
    """
    return await run("resolvePermissions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/sessions/revoke-all")
async def revoke_all_sessions(request: Request) -> dict:
    """Revoke every session in scope

    scope: venue · permission: SESSION_FORCE_LOGOUT · offline: False
    """
    return await run("revokeAllSessions", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/select-role")
async def select_role(request: Request) -> dict:
    """Choose a role for a multi-role session

    scope: tenant · permission: - · offline: False
    """
    return await run("selectRole", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/password-policy")
async def set_password_policy(request: Request) -> dict:
    """Length, breach check, lockout and step-up

    scope: tenant · permission: TENANT_CONFIGURE · offline: False
    """
    return await run("setPasswordPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/segregation-rules")
async def set_segregation_rules(request: Request) -> dict:
    """Which permissions may not be held together

    scope: tenant · permission: ROLE_MANAGE · offline: False
    """
    return await run("setSegregationRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/tenants/sso-config")
async def set_sso_config(request: Request) -> dict:
    """Configure an identity provider

    scope: tenant · permission: USER_MANAGE · offline: False
    """
    return await run("setSsoConfig", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/auth/sso/{providerId}/authorize")
async def start_sso_authorization(request: Request) -> dict:
    """Begin an SSO flow

    scope: tenant · permission: - · offline: False
    """
    return await run("startSsoAuthorization", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/principals/{principalId}")
async def update_principal(request: Request) -> dict:
    """Update or deactivate a principal

    scope: venue · permission: USER_MANAGE · offline: False
    """
    return await run("updatePrincipal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/verify-email")
async def verify_guest_email(request: Request) -> dict:
    """Send a verification link, or consume one

    scope: tenant · permission: GUEST_VIEW · offline: False
    """
    return await run("verifyGuestEmail", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/guest/otp/verify")
async def verify_guest_otp(request: Request) -> dict:
    """Verify a one-time code and issue a session

    scope: tenant · permission: - · offline: False
    """
    return await run("verifyGuestOtp", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/mfa/challenge/{challengeId}/verify")
async def verify_mfa_challenge(request: Request) -> dict:
    """Complete a step-up challenge

    scope: tenant · permission: - · offline: False
    """
    return await run("verifyMfaChallenge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/auth/mfa/methods/{methodId}")
async def verify_mfa_enrolment(request: Request) -> dict:
    """Complete enrolment

    scope: tenant · permission: - · offline: False
    """
    return await run("verifyMfaEnrolment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

