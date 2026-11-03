using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.IntegrationTests;

/// <summary>A test-only endpoint that answers with the request's tenant context and one permission check.</summary>
[ApiController]
[Authorize]
[Route("probe")]
public sealed class ProbeController(ITenantContext tenant, ICurrentPrincipal principal) : ControllerBase
{
    [HttpGet]
    public IActionResult Get() => Ok(new
    {
        tenantId = tenant.TenantId,
        scopePaths = tenant.ScopePaths,
        principalId = tenant.PrincipalId,
        mayCreateOrderAtVenue1 = principal.Permits("ORDER_CREATE", tenant.TenantRootPath + ".v_1"),
    });
}
