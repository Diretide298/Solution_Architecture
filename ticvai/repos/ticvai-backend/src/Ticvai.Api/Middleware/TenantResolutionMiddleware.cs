using System.Diagnostics;
using Ticvai.Shared.Kernel.Tenancy;

namespace Ticvai.Api.Middleware;

/// <summary>
/// Resolves the tenant for every request and pushes it onto the ambient scope.
/// </summary>
/// <remarks>
/// <para>
/// This runs before authentication because the tenant determines which signing
/// keys and which database apply. Resolution order is deliberate: an explicit
/// header wins (used by first-party apps that baked their tenant at build time —
/// Project Direction §3.4.8), then host mapping for white-label web domains.
/// </para>
/// <para>
/// A cell serves exactly one tenant per jurisdiction (§3.3.1), so a request whose
/// resolved tenant does not match this cell's tenant is rejected outright rather
/// than proxied. Silent cross-cell routing would defeat the residency guarantee.
/// </para>
/// </remarks>
public sealed class TenantResolutionMiddleware(
    RequestDelegate next,
    ILogger<TenantResolutionMiddleware> logger)
{
    private const string TenantHeader = "X-Ticvai-Tenant";

    public async Task InvokeAsync(HttpContext context, ITenantRegistry registry, ICellIdentity cell)
    {
        ArgumentNullException.ThrowIfNull(context);

        if (IsUnscopedPath(context.Request.Path))
        {
            await next(context).ConfigureAwait(false);
            return;
        }

        var identifier = ResolveIdentifier(context);

        if (identifier is null)
        {
            await WriteProblemAsync(context, StatusCodes.Status400BadRequest,
                "tenant_unresolved", "The request did not identify a tenant.").ConfigureAwait(false);
            return;
        }

        var tenant = await registry.FindAsync(identifier, context.RequestAborted).ConfigureAwait(false);

        if (tenant is null)
        {
            logger.LogWarning("Unknown tenant identifier {Identifier}", identifier);
            await WriteProblemAsync(context, StatusCodes.Status404NotFound,
                "tenant_not_found", "No tenant matches this request.").ConfigureAwait(false);
            return;
        }

        if (tenant.TenantId != cell.TenantId)
        {
            // Do not proxy. The caller is pointed at the wrong cell and must be
            // redirected by the Control Plane, or residency guarantees are meaningless.
            logger.LogError(
                "Tenant {Requested} routed to cell serving {Served}. Refusing to proxy across cells.",
                tenant.TenantId, cell.TenantId);

            await WriteProblemAsync(context, StatusCodes.Status421MisdirectedRequest,
                "wrong_cell", "This tenant is served by a different cell.").ConfigureAwait(false);
            return;
        }

        using var scope = TenantContextAccessor.Push(tenant);

        Activity.Current?.SetTag("tenant.id", tenant.TenantId);
        Activity.Current?.SetTag("tenant.jurisdiction", tenant.Jurisdiction);
        Activity.Current?.SetTag("region.id", tenant.RegionId);

        using (logger.BeginScope(new Dictionary<string, object>
               {
                   ["TenantId"] = tenant.TenantId,
                   ["RegionId"] = tenant.RegionId,
                   ["Jurisdiction"] = tenant.Jurisdiction
               }))
        {
            await next(context).ConfigureAwait(false);
        }
    }

    private static string? ResolveIdentifier(HttpContext context)
    {
        if (context.Request.Headers.TryGetValue(TenantHeader, out var header))
        {
            var value = header.ToString();
            if (!string.IsNullOrWhiteSpace(value)) return value;
        }

        var host = context.Request.Host.Host;
        return string.IsNullOrWhiteSpace(host) ? null : host;
    }

    private static bool IsUnscopedPath(PathString path) =>
        path.StartsWithSegments("/health") ||
        path.StartsWithSegments("/metrics") ||
        path.StartsWithSegments("/.well-known");

    private static async Task WriteProblemAsync(HttpContext context, int status, string code, string detail)
    {
        context.Response.StatusCode = status;
        context.Response.ContentType = "application/problem+json";

        await context.Response.WriteAsJsonAsync(new
        {
            type = $"https://docs.ticvai.com/errors/{code}",
            title = code,
            status,
            detail,
            traceId = Activity.Current?.TraceId.ToString()
        }).ConfigureAwait(false);
    }
}

/// <summary>Identity of the cell this process is serving. Injected from configuration at boot.</summary>
public interface ICellIdentity
{
    Guid TenantId { get; }
    string Jurisdiction { get; }
    string CellName { get; }
}

/// <summary>
/// Looks up tenant configuration. Backed by the Control Plane, cached locally —
/// a Control Plane outage must not take a cell offline.
/// </summary>
public interface ITenantRegistry
{
    Task<TenantContext?> FindAsync(string identifier, CancellationToken cancellationToken = default);
}
