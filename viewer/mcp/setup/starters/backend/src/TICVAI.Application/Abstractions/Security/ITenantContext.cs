namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// Where the current request may read and write. Every data path reads it; the database enforces
/// the same thing through row-level security on scope_path and venue_id
/// (920-row-level-security.sql), so the two must agree.
/// </summary>
public interface ITenantContext
{
    /// <summary>The tenant (one per tenant database, CF-161).</summary>
    string TenantId { get; }

    /// <summary>
    /// The scope-tree paths the caller may see (ltree text). Set on the connection as the
    /// ticvai.scope_paths setting before any query; empty means the caller sees nothing.
    /// </summary>
    IReadOnlyList<string> ScopePaths { get; }

    /// <summary>The venue the request acts in, when it acts in one.</summary>
    Guid? VenueId { get; }

    /// <summary>The region, for region-scoped operations.</summary>
    Guid? RegionId { get; }

    /// <summary>The workstation (till, scanner, kiosk) a device-scoped operation runs on.</summary>
    string? WorkstationId { get; }
}
