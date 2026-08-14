namespace Ticvai.Shared.Kernel.Tenancy;

/// <summary>
/// Ambient tenant and scope for the current request. Resolved once by
/// <c>TenantResolutionMiddleware</c> and immutable thereafter.
/// </summary>
/// <remarks>
/// Deliberately not settable after construction. Every data access path reads
/// from it, and a mutable tenant context is a cross-tenant data leak waiting for
/// a concurrency bug.
/// </remarks>
public sealed record TenantContext
{
    public required Guid TenantId { get; init; }

    /// <summary>
    /// Jurisdiction this cell serves. A cell never spans jurisdictions
    /// (Project Direction §3.3.1).
    /// </summary>
    public required string Jurisdiction { get; init; }

    public required Guid RegionId { get; init; }

    /// <summary>Base currency, inherited from the region.</summary>
    public required string Currency { get; init; }

    /// <summary>Decimal places for <see cref="Currency"/>. OMR is 3, AED is 2.</summary>
    public required int CurrencyScale { get; init; }

    public required string TimeZone { get; init; }

    /// <summary>Materialised ltree path of the tenant root, e.g. <c>t_miral</c>.</summary>
    public required string ScopePath { get; init; }

    /// <summary>Named connection for this tenant's database within the cell.</summary>
    public required string ConnectionStringName { get; init; }
}

/// <summary>Accessor for the ambient <see cref="TenantContext"/>.</summary>
public interface ITenantContextAccessor
{
    /// <summary>Null outside a tenant-scoped request, such as control-plane paths.</summary>
    TenantContext? Current { get; }

    /// <summary>Throws when no tenant is in scope. Use this in data access paths.</summary>
    TenantContext Require();
}

public sealed class TenantContextAccessor : ITenantContextAccessor
{
    private static readonly AsyncLocal<TenantContext?> Ambient = new();

    public TenantContext? Current => Ambient.Value;

    public TenantContext Require() =>
        Ambient.Value ?? throw new InvalidOperationException(
            "No tenant in scope. This code path must run inside a tenant-resolved request.");

    /// <summary>Pushes a tenant onto the ambient scope for the lifetime of the returned handle.</summary>
    public static IDisposable Push(TenantContext context)
    {
        ArgumentNullException.ThrowIfNull(context);
        var previous = Ambient.Value;
        Ambient.Value = context;
        return new Scope(previous);
    }

    private sealed class Scope(TenantContext? previous) : IDisposable
    {
        private bool _disposed;

        public void Dispose()
        {
            if (_disposed) return;
            Ambient.Value = previous;
            _disposed = true;
        }
    }
}
