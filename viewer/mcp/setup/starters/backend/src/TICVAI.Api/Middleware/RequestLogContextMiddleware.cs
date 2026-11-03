using System.Diagnostics;
using Serilog.Context;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Api.Middleware;

/// <summary>
/// Every log line and span of a request carries <c>tenant_id</c>, <c>region_id</c> and <c>venue_id</c>
/// (quality-gates 2: "the tenant is slow" is otherwise unactionable). Runs after authentication, so the
/// caller's region and venue are known; an absent one is logged empty.
/// </summary>
public sealed class RequestLogContextMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext context, ITenantContext tenant)
    {
        var tenantId = tenant.IsResolved ? tenant.TenantId.ToString() : string.Empty;
        var regionId = tenant.RegionId?.ToString() ?? string.Empty;
        var venueId = tenant.VenueId?.ToString() ?? string.Empty;
        Activity.Current?.SetTag("tenant_id", tenantId).SetTag("region_id", regionId).SetTag("venue_id", venueId);
        using (LogContext.PushProperty("tenant_id", tenantId))
        using (LogContext.PushProperty("region_id", regionId))
        using (LogContext.PushProperty("venue_id", venueId))
        {
            await next(context);
        }
    }
}
