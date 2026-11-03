namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// The tenants this cell serves, by host (<c>resolveTenantHost</c>: a <c>TenantDomain</c>'s
/// <c>hostname</c>, <c>tenantId</c> and <c>cellId</c>). Installed staff apps name their tenant by host
/// too; there is no tenant header.
/// </summary>
public interface ITenantDirectory
{
    /// <summary>The tenant <paramref name="host"/> belongs to, or null when this cell serves no tenant there.</summary>
    ValueTask<TenantRoute?> FindByHostAsync(string host, CancellationToken cancellationToken);
}

/// <param name="TenantId">The tenant.</param>
/// <param name="RootScopePath">Its root scope path (ltree text).</param>
public sealed record TenantRoute(Guid TenantId, string RootScopePath);
