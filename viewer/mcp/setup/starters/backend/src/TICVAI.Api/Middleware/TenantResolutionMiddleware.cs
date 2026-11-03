using Microsoft.AspNetCore.Mvc;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.Api.Middleware;

/// <summary>
/// <b>The request's tenant is the one its host resolves to</b> (<c>resolveTenantHost</c>; ADR-0038).
/// Runs before authentication, so the token can be checked against it. No tenant header or body field
/// is read: a client cannot pick its tenant. A host this cell serves no tenant at is <c>404</c>.
/// </summary>
public sealed class TenantResolutionMiddleware(RequestDelegate next)
{
    /// <summary>Paths answered without a tenant: the process's own health.</summary>
    private static readonly PathString[] TenantFree = [new("/health")];

    public async Task InvokeAsync(HttpContext context, ITenantDirectory directory, RequestTenantContext tenant)
    {
        if (TenantFree.Any(p => context.Request.Path.StartsWithSegments(p)))
        {
            await next(context);
            return;
        }

        var route = await directory.FindByHostAsync(context.Request.Host.Host, context.RequestAborted);
        if (route is null)
        {
            context.Response.StatusCode = StatusCodes.Status404NotFound;
            context.Response.ContentType = "application/problem+json";
            await context.Response.WriteAsJsonAsync(new ProblemDetails
            {
                Type = "not-found",
                Status = StatusCodes.Status404NotFound,
                Title = "No tenant is served at this host",
                Instance = context.Request.Path,
            });
            return;
        }

        tenant.Resolve(route);
        await next(context);
    }
}
