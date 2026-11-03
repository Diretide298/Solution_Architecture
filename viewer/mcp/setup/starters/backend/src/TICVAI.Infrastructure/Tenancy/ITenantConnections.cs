namespace TICVAI.Infrastructure.Tenancy;

/// <summary>Each tenant's own database (ADR-0038). Infrastructure only: no module sees a connection string.</summary>
public interface ITenantConnections
{
    /// <summary>The connection string of <paramref name="tenantId"/>'s database.</summary>
    string ConnectionStringFor(Guid tenantId);

    /// <summary>Every tenant this process serves (the health check opens each).</summary>
    IReadOnlyList<Guid> Tenants { get; }
}
