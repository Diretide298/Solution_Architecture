using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// The request's <see cref="ITenantContext"/>, filled in two steps: the host resolves the tenant
/// (<see cref="Resolve"/>), then authentication binds the caller's scope (<see cref="Bind"/>). Until it
/// is bound the caller's scope is empty, so row-level security shows no scoped rows.
/// </summary>
public sealed class RequestTenantContext : ITenantContext
{
    private TenantRoute? _route;

    public bool IsResolved => _route is not null;

    public Guid TenantId => _route?.TenantId ?? throw new InvalidOperationException("The request's host has not resolved to a tenant");

    public string TenantRootPath => _route?.RootScopePath ?? throw new InvalidOperationException("The request's host has not resolved to a tenant");

    public IReadOnlyList<string> ScopePaths { get; private set; } = [];

    public Guid? SubjectId { get; private set; }

    public Guid? PrincipalId { get; private set; }

    public Guid? VenueId { get; private set; }

    public Guid? RegionId { get; private set; }

    public string? WorkstationId { get; private set; }

    /// <summary>The tenant the request's host resolved to. Once per request.</summary>
    public void Resolve(TenantRoute route)
    {
        ArgumentNullException.ThrowIfNull(route);
        if (_route is not null && _route != route)
        {
            throw new InvalidOperationException("The request's tenant is already resolved");
        }

        _route = route;
    }

    /// <summary>The authenticated caller's context, from its session or a serviceAuth token.</summary>
    public void Bind(IReadOnlyList<string> scopePaths, Guid? principalId, Guid? subjectId, Guid? venueId = null, Guid? regionId = null, string? workstationId = null)
    {
        ArgumentNullException.ThrowIfNull(scopePaths);
        ScopePaths = scopePaths;
        PrincipalId = principalId;
        SubjectId = subjectId;
        VenueId = venueId;
        RegionId = regionId;
        WorkstationId = workstationId;
    }
}
