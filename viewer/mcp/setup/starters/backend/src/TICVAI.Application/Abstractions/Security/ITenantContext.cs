namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// Where the current request may read and write. Every data path reads it; the database enforces
/// the same thing through row-level security on scope_path and venue_id
/// (920-row-level-security.sql), so the two must agree.
/// </summary>
/// <remarks>
/// <b>The tenant is the one the request's host resolves to</b> (ADR-0038: a cell holds many tenants,
/// each in its own database; <c>resolveTenantHost</c>). No tenant header or body field is read, and a
/// token whose <c>tenant</c> claim (<c>tid</c> for <c>serviceAuth</c>) is not this tenant is refused
/// <c>401</c> before anything else runs (r13 review C-05). The data source is this tenant's database.
/// </remarks>
public interface ITenantContext
{
    /// <summary>True once the request's host has resolved to a tenant this cell serves.</summary>
    bool IsResolved { get; }

    /// <summary>The tenant (one database per tenant, ADR-0038). The same id type as every other id (ADR-0056).</summary>
    Guid TenantId { get; }

    /// <summary>The tenant's root scope path (ltree text): the system context and a serviceAuth call's scope.</summary>
    string TenantRootPath { get; }

    /// <summary>
    /// The scope-tree paths the caller may see (ltree text). Set with <c>SET LOCAL ticvai.scope_paths</c>
    /// at the start of <b>every transaction</b> (backend/MIGRATIONS.md, "The connection context"), never
    /// on the connection: a pooled connection would carry one request's scope into the next. Empty means
    /// the caller sees no scoped rows.
    /// </summary>
    IReadOnlyList<string> ScopePaths { get; }

    /// <summary>A guest's subject: <c>SET LOCAL ticvai.subject_id</c> (the guest's own rows).</summary>
    Guid? SubjectId { get; }

    /// <summary>The signed-in principal: <c>SET LOCAL ticvai.principal_id</c> (its credentials and second factors).</summary>
    Guid? PrincipalId { get; }

    /// <summary>The venue the request acts in, when it acts in one.</summary>
    Guid? VenueId { get; }

    /// <summary>The region, for region-scoped operations.</summary>
    Guid? RegionId { get; }

    /// <summary>The workstation (till, scanner, kiosk) a device-scoped operation runs on.</summary>
    string? WorkstationId { get; }
}
