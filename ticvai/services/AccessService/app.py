"""AccessService — generated skeleton for topology benchmarking.

**Not the product.** Every route executes the reads and writes its operation declares against the
real schema, and returns. There is no business logic, no validation beyond the path, and no
correctness guarantee — **this exists to measure what a deployment topology costs**, and the
database work is the part that varies with topology.

177 operations · 20 tables touched · scope levels: tenant, venue, workstation
"""
from __future__ import annotations

import os
import time

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, Request, Response

from queries import READS, WRITES, CACHE

app = FastAPI(title="AccessService", docs_url="/_docs")

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
    return {"service": "AccessService", "operations": 177,
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



@app.post("/blacklist")
async def add_blacklist_entry(request: Request) -> dict:
    """Blacklist a media code

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("addBlacklistEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/manual-override-supervisor")
async def approve_manual_override_supervisor(request: Request) -> dict:
    """Manual Override & Supervisor Approval

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("approveManualOverrideSupervisor", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/multi-media-preview")
async def approve_multi_media_preview(request: Request) -> dict:
    """Multi-Media Preview, Testing, Approval & Publication

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("approveMultiMediaPreview", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access-points")
async def create_access_point(request: Request) -> dict:
    """Create an access point

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("createAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/admission-rules")
async def create_admission_rules(request: Request) -> dict:
    """Create an admission profile

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("createAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/parking-entitlements")
async def create_parking_entitlement(request: Request) -> dict:
    """A guest bought parking

    scope: venue · permission: - · offline: False
    """
    return await run("createParkingEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/face-pass/enrolments")
async def enrol_face_pass(request: Request) -> dict:
    """Register a facial profile against an entitlement

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("enrolFacePass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-points/{accessPointId}")
async def get_access_point(request: Request) -> dict:
    """Read an access point

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("getAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}")
async def get_entitlement(request: Request) -> dict:
    """One entitlement, with what remains on it

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("getEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}/credential")
async def get_entitlement_credential(request: Request) -> dict:
    """The thing that gets scanned

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getEntitlementCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlements/{entitlementId}/history")
async def get_entitlement_history(request: Request) -> dict:
    """Every scan, freeze, share and reissue against it

    scope: venue · permission: ORDER_VIEW · offline: False
    """
    return await run("getEntitlementHistory", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/face-pass/enrolments/{enrolmentId}")
async def get_face_pass_enrolment(request: Request) -> dict:
    """Whether a pass has a face registered, and when

    scope: venue · permission: GUEST_VIEW · offline: False
    """
    return await run("getFacePassEnrolment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/offline-package")
async def get_offline_package(request: Request) -> dict:
    """Entitlement and rule set for offline validation

    scope: workstation · permission: ACCESS_VALIDATE · offline: False
    """
    return await run("getOfflinePackage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access")
async def list_access(request: Request) -> dict:
    """Access Control Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-attribute-catalog")
async def list_access_attribute_catalog(request: Request) -> dict:
    """Access Attribute Catalog

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessAttributeCatalog", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-executive-insight")
async def list_access_executive_insight(request: Request) -> dict:
    """AI Access Intelligence, Forecasting & Executive Insights

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessExecutiveInsight", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-location-grouping")
async def list_access_location_grouping(request: Request) -> dict:
    """Access Location Grouping

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessLocationGrouping", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-monitoring")
async def list_access_monitoring(request: Request) -> dict:
    """Access Monitoring & Analytics Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessMonitoring", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-points")
async def list_access_points(request: Request) -> dict:
    """List access points

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listAccessPoints", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-report-scheduled")
async def list_access_report_scheduled(request: Request) -> dict:
    """Access Reports, Scheduled Reporting & Data Export

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessReportScheduled", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-risk-scoring")
async def list_access_risk_scoring(request: Request) -> dict:
    """Access Risk Scoring & Decision Engine

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessRiskScoring", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-rule")
async def list_access_rule(request: Request) -> dict:
    """Access Rule Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-security-fraud")
async def list_access_security_fraud(request: Request) -> dict:
    """Access Security & Fraud Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessSecurityFraud", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access-validity-time")
async def list_access_validity_time(request: Request) -> dict:
    """Access Validity & Time Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAccessValidityTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/admission-rules")
async def list_admission_rules(request: Request) -> dict:
    """List admission profiles

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/anti-passback-journey")
async def list_anti_passback_journey(request: Request) -> dict:
    """Anti-Passback & Journey Sequence

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAntiPassbackJourney", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/attendance-admission")
async def list_attendance_admission(request: Request) -> dict:
    """Attendance & Admission Analytics

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAttendanceAdmission", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/authorization-governance-temporary")
async def list_authorization_governance_temporary(request: Request) -> dict:
    """Authorization Governance & Temporary Access

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listAuthorizationGovernanceTemporary", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric")
async def list_biometric(request: Request) -> dict:
    """Biometric Simulation, Audit & Publication

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometric", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric-access")
async def list_biometric_access(request: Request) -> dict:
    """Biometric Access Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometricAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric-consent-guardian")
async def list_biometric_consent_guardian(request: Request) -> dict:
    """Biometric Consent & Guardian Management

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometricConsentGuardian", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric-identity-integrity")
async def list_biometric_identity_integrity(request: Request) -> dict:
    """Biometric & Identity Integrity Monitoring

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometricIdentityIntegrity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric-lifecycle-retention")
async def list_biometric_lifecycle_retention(request: Request) -> dict:
    """Biometric Lifecycle, Retention & Deletion

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometricLifecycleRetention", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/biometric-validation-gate")
async def list_biometric_validation_gate(request: Request) -> dict:
    """Biometric Validation at Gate

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBiometricValidationGate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/blacklist")
async def list_blacklist(request: Request) -> dict:
    """List blacklisted media

    scope: venue · permission: SCOPE_VIEW · offline: True
    """
    return await run("listBlacklist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/branding-localization-template")
async def list_branding_localization_template(request: Request) -> dict:
    """Branding, Localization & Template Inheritance

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listBrandingLocalizationTemplate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/connectivity-failure-degraded")
async def list_connectivity_failure_degraded(request: Request) -> dict:
    """Connectivity Failure & Degraded Mode Policy

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listConnectivityFailureDegraded", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential")
async def list_credential(request: Request) -> dict:
    """Credential Operations Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-activation-display")
async def list_credential_activation_display(request: Request) -> dict:
    """Credential Activation & Display Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialActivationDisplay", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-delivery-distribution")
async def list_credential_delivery_distribution(request: Request) -> dict:
    """Credential Delivery & Distribution Operations

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialDeliveryDistribution", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-disable-blacklist")
async def list_credential_disable_blacklist(request: Request) -> dict:
    """Credential Disable, Blacklist & Whitelist Operations

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialDisableBlacklist", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-generation-issuance")
async def list_credential_generation_issuance(request: Request) -> dict:
    """Credential Generation & Issuance Monitor

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialGenerationIssuance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-identity-token")
async def list_credential_identity_token(request: Request) -> dict:
    """Credential Identity, Token & Reference Mapping

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialIdentityToken", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-replacement-reissue")
async def list_credential_replacement_reissue(request: Request) -> dict:
    """Credential Replacement, Reissue, Revocation & Recovery

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialReplacementReissue", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-revocation-lifecycle")
async def list_credential_revocation_lifecycle(request: Request) -> dict:
    """Credential Revocation & Lifecycle Events

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialRevocationLifecycle", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-security")
async def list_credential_security(request: Request) -> dict:
    """Credential Security Simulation, Audit & Publication

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialSecurity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-security-operational")
async def list_credential_security_operational(request: Request) -> dict:
    """Credential Security, Audit & Operational Evidence

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialSecurityOperational", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-sharing-concurrent")
async def list_credential_sharing_concurrent(request: Request) -> dict:
    """Credential Sharing & Concurrent Usage Detection

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialSharingConcurrent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-transfer-rebinding")
async def list_credential_transfer_rebinding(request: Request) -> dict:
    """Credential Transfer & Rebinding

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialTransferRebinding", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/credential-usage-cross")
async def list_credential_usage_cross(request: Request) -> dict:
    """Credential Usage & Cross-Media Traceability

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listCredentialUsageCross", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/device-binding-session")
async def list_device_binding_session(request: Request) -> dict:
    """Device Binding & Session Security

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listDeviceBindingSession", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/device-gate")
async def list_device_gate(request: Request) -> dict:
    """Device & Gate Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listDeviceGate", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/device-type-hardware")
async def list_device_type_hardware(request: Request) -> dict:
    """Device Type & Hardware Library

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listDeviceTypeHardware", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/digital-credential-security")
async def list_digital_credential_security(request: Request) -> dict:
    """Digital Credential Security Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listDigitalCredentialSecurity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/dynamic-access-policy")
async def list_dynamic_access_policy(request: Request) -> dict:
    """Dynamic Access Policy Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listDynamicAccessPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/edge-package-data")
async def list_edge_package_data(request: Request) -> dict:
    """Edge Package & Data Distribution

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEdgePackageData", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/edge-security-deployment")
async def list_edge_security_deployment(request: Request) -> dict:
    """Edge Security, Audit & Deployment

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEdgeSecurityDeployment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlement-consumption")
async def list_entitlement_consumption(request: Request) -> dict:
    """Entitlement Consumption Engine

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEntitlementConsumption", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entitlement-cross-media")
async def list_entitlement_cross_media(request: Request) -> dict:
    """Entitlement & Cross-Media Synchronization Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEntitlementCrossMedia", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/my/entitlements/all")
async def list_entitlements(request: Request) -> dict:
    """Every entitlement this guest holds, including expired

    scope: tenant · permission: - · offline: False
    """
    return await run("listEntitlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entry-exit-crossover")
async def list_entry_exit_crossover(request: Request) -> dict:
    """Entry, Exit, Re-entry & Crossover Analytics

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEntryExitCrossover", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entry-exit-rule")
async def list_entry_exit_rule(request: Request) -> dict:
    """Entry, Exit & Re-entry Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEntryExitRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/entry-temporary-exit")
async def list_entry_temporary_exit(request: Request) -> dict:
    """Re-entry & Temporary Exit Journey

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listEntryTemporaryExit", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/external-partner-credential")
async def list_external_partner_credential(request: Request) -> dict:
    """External & Partner Credential Mapping

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listExternalPartnerCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/face-change-enrollment")
async def list_face_change_enrollment(request: Request) -> dict:
    """Face Change, Re-enrollment & Identity Protection

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFaceChangeEnrollment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/face-matching-verification")
async def list_face_matching_verification(request: Request) -> dict:
    """Face Matching & Verification Thresholds

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFaceMatchingVerification", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/face-tag-temporary")
async def list_face_tag_temporary(request: Request) -> dict:
    """Face Tag Temporary Enrollment

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFaceTagTemporary", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/failed-generation-delivery")
async def list_failed_generation_delivery(request: Request) -> dict:
    """Failed Generation, Delivery & Credential Exception Management

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFailedGenerationDelivery", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/family-child-pod")
async def list_family_child_pod(request: Request) -> dict:
    """Family, Child, POD & Companion Journey

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFamilyChildPod", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fast-pass-attraction")
async def list_fast_pass_attraction(request: Request) -> dict:
    """Fast Pass & Attraction Access Journey

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFastPassAttraction", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/fraud-detection-rule")
async def list_fraud_detection_rule(request: Request) -> dict:
    """Fraud Detection Rule & Signal Library

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listFraudDetectionRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/gate-mode-free")
async def list_gate_mode_free(request: Request) -> dict:
    """Gate Modes, Free Spin & Emergency Controls

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGateModeFree", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/graphical-access-map")
async def list_graphical_access_map(request: Request) -> dict:
    """Graphical Access Map & Live Gate Performance

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGraphicalAccessMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-admission-quantity")
async def list_group_admission_quantity(request: Request) -> dict:
    """Group Admission & Quantity Validation

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGroupAdmissionQuantity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-attendance-partial")
async def list_group_attendance_partial(request: Request) -> dict:
    """Group Attendance & Partial Entry Manager

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGroupAttendancePartial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/group-leader-fast")
async def list_group_leader_fast(request: Request) -> dict:
    """Group Leader & Fast B2B Validation

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGroupLeaderFast", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-companion-eligibility")
async def list_guest_companion_eligibility(request: Request) -> dict:
    """Guest, Companion & Eligibility Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGuestCompanionEligibility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-dwell-time")
async def list_guest_dwell_time(request: Request) -> dict:
    """Guest Dwell Time, Length of Stay & Attraction Flow

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGuestDwellTime", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guest-journey")
async def list_guest_journey(request: Request) -> dict:
    """Guest Journey Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listGuestJourney", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/hardware-compatibility-health")
async def list_hardware_compatibility_health(request: Request) -> dict:
    """Hardware Compatibility, Health, Testing & Deployment

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listHardwareCompatibilityHealth", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/hotel-wallet-external")
async def list_hotel_wallet_external(request: Request) -> dict:
    """Hotel, Wallet & External Media Integration

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listHotelWalletExternal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/identity-membership-accreditation")
async def list_identity_membership_accreditation(request: Request) -> dict:
    """Identity, Membership & Accreditation Policies

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listIdentityMembershipAccreditation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/live-access")
async def list_live_access(request: Request) -> dict:
    """Live Access Operations Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listLiveAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/live-gate-mode")
async def list_live_gate_mode(request: Request) -> dict:
    """Live Gate Mode & Lane Control

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listLiveGateMode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/live-venue-occupancy")
async def list_live_venue_occupancy(request: Request) -> dict:
    """Live Venue Occupancy & People Counting

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listLiveVenueOccupancy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-activation-priority")
async def list_media_activation_priority(request: Request) -> dict:
    """Media Activation, Priority & Fallback Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaActivationPriority", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-credential")
async def list_media_credential(request: Request) -> dict:
    """Media & Credential Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-design")
async def list_media_design(request: Request) -> dict:
    """Media Design Studio Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaDesign", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-issuance-encoding")
async def list_media_issuance_encoding(request: Request) -> dict:
    """Media Issuance & Encoding Profile

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaIssuanceEncoding", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-replacement-revocation")
async def list_media_replacement_revocation(request: Request) -> dict:
    """Media Replacement, Revocation & Rebinding Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaReplacementRevocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-swap-replacement")
async def list_media_swap_replacement(request: Request) -> dict:
    """Media Swap & Replacement

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaSwapReplacement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-type-credential")
async def list_media_type_credential(request: Request) -> dict:
    """Media Type & Credential Technology Registry

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaTypeCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/media-type-technology")
async def list_media_type_technology(request: Request) -> dict:
    """Media Type & Technology Library

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMediaTypeTechnology", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/multi-media-binding")
async def list_multi_media_binding(request: Request) -> dict:
    """Multi-Media Binding & Association Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMultiMediaBinding", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/multi-park-crossover")
async def list_multi_park_crossover(request: Request) -> dict:
    """Multi-Park & Crossover Rules

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMultiParkCrossover", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/multi-park-crossover")
async def list_multi_park_crossover2(request: Request) -> dict:
    """Multi-Park & Crossover Journey Orchestrator

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listMultiParkCrossover2", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/guests/me/entitlements")
async def list_my_entitlements(request: Request) -> dict:
    """Every ticket, pass and membership this guest holds

    scope: venue · permission: ORDER_VIEW · offline: True
    """
    return await run("listMyEntitlements", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/offline-credential-revocation")
async def list_offline_credential_revocation(request: Request) -> dict:
    """Offline Credential & Revocation Cache

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOfflineCredentialRevocation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/offline-cryptographic-validation")
async def list_offline_cryptographic_validation(request: Request) -> dict:
    """Offline Cryptographic Validation Profile

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOfflineCryptographicValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/offline-edge")
async def list_offline_edge(request: Request) -> dict:
    """Offline & Edge Operations Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOfflineEdge", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/offline-entitlement-usage")
async def list_offline_entitlement_usage(request: Request) -> dict:
    """Offline Entitlement & Usage Ledger

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOfflineEntitlementUsage", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/operating-calendar-special")
async def list_operating_calendar_special(request: Request) -> dict:
    """Operating Calendar & Special Access Days

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listOperatingCalendarSpecial", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/parking-facilities")
async def list_parking_facilities(request: Request) -> dict:
    """Car parks at a venue, and how each integrates

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: True
    """
    return await run("listParkingFacilities", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/physical-device-registration")
async def list_physical_device_registration(request: Request) -> dict:
    """Physical Device Registration & Provisioning

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listPhysicalDeviceRegistration", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/podium-console")
async def list_podium_console(request: Request) -> dict:
    """Podium Operations Console

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listPodiumConsole", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/policy-evaluation-architecture")
async def list_policy_evaluation_architecture(request: Request) -> dict:
    """Policy Evaluation Architecture & Offline Distribution

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listPolicyEvaluationArchitecture", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/policy-scope-hierarchy")
async def list_policy_scope_hierarchy(request: Request) -> dict:
    """Policy Scope, Hierarchy & Inheritance

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listPolicyScopeHierarchy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/queue-throughput-lane")
async def list_queue_throughput_lane(request: Request) -> dict:
    """Queue, Throughput & Lane Optimization

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listQueueThroughputLane", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/reconnection-synchronization-conflict")
async def list_reconnection_synchronization_conflict(request: Request) -> dict:
    """Reconnection, Synchronization & Conflict Resolution

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listReconnectionSynchronizationConflict", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/relationship-companion-fraud")
async def list_relationship_companion_fraud(request: Request) -> dict:
    """Relationship & Companion Fraud Monitoring

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listRelationshipCompanionFraud", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/scans")
async def list_scans(request: Request) -> dict:
    """List scan events

    scope: venue · permission: REPORT_VIEW_VENUE · offline: False
    """
    return await run("listScans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/security-detection-governance")
async def list_security_detection_governance(request: Request) -> dict:
    """Security Analytics, AI Detection & Governance

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listSecurityDetectionGovernance", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/shift-handover-summary")
async def list_shift_handover_summary(request: Request) -> dict:
    """Operations Audit, Shift Handover & Control Summary

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listShiftHandoverSummary", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/special-event-free")
async def list_special_event_free(request: Request) -> dict:
    """Special Event, Free View & Alternative Admission

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listSpecialEventFree", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/throughput-queue-validation")
async def list_throughput_queue_validation(request: Request) -> dict:
    """Throughput, Queue & Validation Performance Analytics

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listThroughputQueueValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ticket-credential-investigation")
async def list_ticket_credential_investigation(request: Request) -> dict:
    """Ticket & Credential Investigation Console

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listTicketCredentialInvestigation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/ticket-media")
async def list_ticket_media(request: Request) -> dict:
    """Ticket Media Analytics & AI Operations Intelligence

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listTicketMedia", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/unified-identity-credential")
async def list_unified_identity_credential(request: Request) -> dict:
    """Unified Identity & Credential Lock Manager

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listUnifiedIdentityCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/validation-exception-reason")
async def list_validation_exception_reason(request: Request) -> dict:
    """Validation Exception & Reason Code Manager

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listValidationExceptionReason", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/validation-outcome-rejection")
async def list_validation_outcome_rejection(request: Request) -> dict:
    """Validation Outcome & Rejection Analytics

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listValidationOutcomeRejection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/venue-park-access")
async def list_venue_park_access(request: Request) -> dict:
    """Venue & Park Access Structure

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVenueParkAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/verification-method-selection")
async def list_verification_method_selection(request: Request) -> dict:
    """Verification Method Selection & Locking

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVerificationMethodSelection", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/virtual-credential-media")
async def list_virtual_credential_media(request: Request) -> dict:
    """Virtual Credential & Media Association

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVirtualCredentialMedia", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/virtual-ticket")
async def list_virtual_ticket(request: Request) -> dict:
    """Virtual Ticket Command Center

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVirtualTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/virtual-ticket-architecture")
async def list_virtual_ticket_architecture(request: Request) -> dict:
    """Virtual Ticket Architecture Testing, Governance & Audit

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVirtualTicketArchitecture", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/virtual-ticket-statu")
async def list_virtual_ticket_status(request: Request) -> dict:
    """Virtual Ticket Status & Lifecycle Model

    scope: venue · permission: SCOPE_VIEW · offline: False
    """
    return await run("listVirtualTicketStatus", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.get("/access/lookup")
async def lookup_ticket(request: Request) -> dict:
    """Read-only validity check without admitting

    scope: venue · permission: TICKET_LOOKUP · offline: True
    """
    return await run("lookupTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/override")
async def override_access(request: Request) -> dict:
    """Admit against a failed validation

    scope: venue · permission: ACCESS_OVERRIDE · offline: True
    """
    return await run("overrideAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/media-compatibility-testing")
async def publish_media_compatibility_testing(request: Request) -> dict:
    """Media Compatibility, Testing & Publication

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("publishMediaCompatibilityTesting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/rule-conflict-check")
async def publish_rule_conflict_check(request: Request) -> dict:
    """Rule Simulation, Conflict Check & Publication

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("publishRuleConflictCheck", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/topology-validation")
async def publish_topology_validation(request: Request) -> dict:
    """Topology Validation & Publication

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("publishTopologyValidation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/blacklist/{mediaCode}")
async def remove_blacklist_entry(request: Request) -> dict:
    """Remove a blacklist entry

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("removeBlacklistEntry", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.delete("/face-pass/enrolments/{enrolmentId}")
async def revoke_face_pass(request: Request) -> dict:
    """Remove a facial profile

    scope: venue · permission: GUEST_MANAGE · offline: False
    """
    return await run("revokeFacePass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-area-zone")
async def set_access_area_zone(request: Request) -> dict:
    """Access Area & Zone Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAccessAreaZone", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-graphical-map")
async def set_access_graphical_map(request: Request) -> dict:
    """Access Control Graphical Map Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAccessGraphicalMap", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-points/{accessPointId}/geofence")
async def set_access_point_geofence(request: Request) -> dict:
    """Set a geofence for handheld validation

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAccessPointGeofence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/apple-wallet-pass")
async def set_apple_wallet_pass(request: Request) -> dict:
    """Apple Wallet Pass Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAppleWalletPass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/attraction-access")
async def set_attraction_access(request: Request) -> dict:
    """Attraction Access Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setAttractionAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/biometric-verification-profile")
async def set_biometric_verification_profile(request: Request) -> dict:
    """Biometric Verification Profile Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setBiometricVerificationProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/ble-beacon-geofence")
async def set_ble_beacon_geofence(request: Request) -> dict:
    """BLE Beacon & Geofence Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setBleBeaconGeofence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/context-time-event")
async def set_context_time_event(request: Request) -> dict:
    """Context, Time, Event & Capacity Policy Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setContextTimeEvent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/device-software-content")
async def set_device_software_content(request: Request) -> dict:
    """Device Software, Content & Remote Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setDeviceSoftwareContent", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/digital-barcode-ticket")
async def set_digital_barcode_ticket(request: Request) -> dict:
    """Digital QR & Barcode Ticket Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setDigitalBarcodeTicket", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/digital-card-membership")
async def set_digital_card_membership(request: Request) -> dict:
    """Digital Card, Membership & Wearable Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setDigitalCardMembership", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/dynamic-field-data")
async def set_dynamic_field_data(request: Request) -> dict:
    """Dynamic Fields, Data Mapping & Content Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setDynamicFieldData", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/dynamic-security-profile")
async def set_dynamic_security_profile(request: Request) -> dict:
    """Dynamic QR Security Profile Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setDynamicSecurityProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/edge-node-local")
async def set_edge_node_local(request: Request) -> dict:
    """Edge Node & Local Processing Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setEdgeNodeLocal", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/embedded-entitlement-payload")
async def set_embedded_entitlement_payload(request: Request) -> dict:
    """Embedded Entitlement Payload Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setEmbeddedEntitlementPayload", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/face-pass-enrollment")
async def set_face_pass_enrollment(request: Request) -> dict:
    """Face Pass Enrollment Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setFacePassEnrollment", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/gate-lane")
async def set_gate_lane(request: Request) -> dict:
    """Gate & Lane Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setGateLane", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/google-wallet-pass")
async def set_google_wallet_pass(request: Request) -> dict:
    """Google Wallet Pass Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setGoogleWalletPass", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/group-admission-profile")
async def set_group_admission_profile(request: Request) -> dict:
    """Group & B2B Admission Profile Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setGroupAdmissionProfile", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/handheld-mobile-access")
async def set_handheld_mobile_access(request: Request) -> dict:
    """Handheld & Mobile Access Device Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setHandheldMobileAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/media-binding-activation")
async def set_media_binding_activation(request: Request) -> dict:
    """Media Binding, Activation & Assignment Operations

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setMediaBindingActivation", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/operational-incident-exception")
async def set_operational_incident_exception(request: Request) -> dict:
    """Operational Incident & Exception Workspace

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setOperationalIncidentException", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/parking-facilities")
async def set_parking_facility(request: Request) -> dict:
    """Configure a car park and its integration

    scope: venue · permission: PARKING_CONFIGURE · offline: False
    """
    return await run("setParkingFacility", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/pdf-printable-pos")
async def set_pdf_printable_pos(request: Request) -> dict:
    """PDF, Printable & POS Ticket Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setPdfPrintablePos", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/reader-scanner-peripheral")
async def set_reader_scanner_peripheral(request: Request) -> dict:
    """Reader, Scanner & Peripheral Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setReaderScannerPeripheral", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/real-time-security")
async def set_real_time_security(request: Request) -> dict:
    """Real-Time Security Response & Playbook Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setRealTimeSecurity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/rfid-nfc")
async def set_rfid_nfc(request: Request) -> dict:
    """RFID & NFC Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setRfidNfc", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/rfid-nfc-card")
async def set_rfid_nfc_card(request: Request) -> dict:
    """RFID, NFC, Card & Wristband Media Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setRfidNfcCard", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/security-investigation-evidence")
async def set_security_investigation_evidence(request: Request) -> dict:
    """Security Investigation & Evidence Workspace

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setSecurityInvestigationEvidence", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/turnstile-lane-behavior")
async def set_turnstile_lane_behavior(request: Request) -> dict:
    """Turnstile & Lane Behavior Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setTurnstileLaneBehavior", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/access-points/{accessPointId}/mode")
async def set_turnstile_mode(request: Request) -> dict:
    """Set the operating mode of an access point

    scope: venue · permission: TURNSTILE_MODE_SET · offline: True
    """
    return await run("setTurnstileMode", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/validation-outcome-guest")
async def set_validation_outcome_guest(request: Request) -> dict:
    """Validation Outcome & Guest Feedback Designer

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setValidationOutcomeGuest", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/virtual-ticket-credential")
async def set_virtual_ticket_credential(request: Request) -> dict:
    """Virtual Ticket & Credential 360° Workspace

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setVirtualTicketCredential", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/virtual-ticket-identity")
async def set_virtual_ticket_identity(request: Request) -> dict:
    """Virtual Ticket Identity & Master Record Configuration

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setVirtualTicketIdentity", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/visual-access-rule")
async def set_visual_access_rule(request: Request) -> dict:
    """Visual Access Rule Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setVisualAccessRule", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/visual-dynamic-policy")
async def set_visual_dynamic_policy(request: Request) -> dict:
    """Visual Dynamic Policy Builder

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("setVisualDynamicPolicy", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/offline-resilience-testing")
async def simulate_offline_resilience_testing(request: Request) -> dict:
    """Offline Simulation & Resilience Testing

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("simulateOfflineResilienceTesting", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/policy-conflict-impact")
async def simulate_policy_conflict_impact(request: Request) -> dict:
    """Policy Simulation, Conflict & Impact Analysis

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("simulatePolicyConflictImpact", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/scans")
async def sync_scans(request: Request) -> dict:
    """Replay scans recorded offline

    scope: workstation · permission: ACCESS_VALIDATE · offline: False
    """
    return await run("syncScans", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/access-points/{accessPointId}")
async def update_access_point(request: Request) -> dict:
    """Update an access point

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("updateAccessPoint", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.put("/admission-rules/{profileId}")
async def update_admission_rules(request: Request) -> dict:
    """Update an admission profile

    scope: venue · permission: ACCESS_POINT_CONFIGURE · offline: False
    """
    return await run("updateAdmissionRules", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.patch("/parking-entitlements/{entitlementId}")
async def update_parking_entitlement(request: Request) -> dict:
    """Change the plate, or revoke

    scope: venue · permission: - · offline: False
    """
    return await run("updateParkingEntitlement", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/validate")
async def validate_access(request: Request) -> dict:
    """Validate media at an access point and admit or deny

    scope: workstation · permission: ACCESS_VALIDATE · offline: True
    """
    return await run("validateAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))


@app.post("/access/group-validate")
async def validate_group_access(request: Request) -> dict:
    """Admit a group on one read

    scope: workstation · permission: ACCESS_VALIDATE · offline: True
    """
    return await run("validateGroupAccess", request.headers.get("x-scope-path", "uae"),
                     request.headers.get(TENANT_HEADER))

