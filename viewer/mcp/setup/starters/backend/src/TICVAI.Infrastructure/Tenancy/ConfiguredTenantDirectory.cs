using Microsoft.Extensions.Options;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// Resolves a host to its tenant, and a tenant to its database, from <see cref="TenantOptions"/>.
/// The routing every request goes through: one process serves every tenant of the cell, each request
/// on its own tenant's database (ADR-0038).
/// </summary>
public sealed class ConfiguredTenantDirectory(IOptionsMonitor<TenantOptions> options) : ITenantDirectory, ITenantConnections
{
    public ValueTask<TenantRoute?> FindByHostAsync(string host, CancellationToken cancellationToken)
    {
        var entry = options.CurrentValue.Entries.FirstOrDefault(e =>
            e.Hosts.Any(h => string.Equals(h, host, StringComparison.OrdinalIgnoreCase)));
        return ValueTask.FromResult(entry is null ? null : new TenantRoute(entry.TenantId, entry.RootScopePath));
    }

    public string ConnectionStringFor(Guid tenantId)
    {
        var entry = options.CurrentValue.Entries.FirstOrDefault(e => e.TenantId == tenantId);
        return entry is { ConnectionString.Length: > 0 }
            ? entry.ConnectionString
            : throw new InvalidOperationException($"No database is configured for tenant {tenantId}");
    }

    public IReadOnlyList<Guid> Tenants => options.CurrentValue.Entries.Select(e => e.TenantId).ToList();
}
