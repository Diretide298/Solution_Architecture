using System.Security.Claims;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// <b>The token's tenant is the request's tenant</b> (r13 review C-05; <c>common.yaml</c>
/// <c>bearerAuth</c>, <c>guestAuth</c> and <c>serviceAuth</c>). One key signs every tenant's tokens in a
/// cell, so a valid signature proves the cell, never the tenant. After the signature, and before any
/// permission, scope or row is looked at, a token is refused (<c>401 unauthenticated</c>) when:
/// <list type="bullet">
/// <item>its <c>tenant</c> claim (<c>tid</c> on a serviceAuth token) is missing or is not the tenant the host resolved to;</item>
/// <item>a staff or guest token has no <c>sid</c>, or its <c>sid</c> names no live session;</item>
/// <item>the session was opened for another tenant.</item>
/// </list>
/// No tenant header or body field is read, here or anywhere.
/// </summary>
public static class TenantBinding
{
    public const string TenantClaim = "tenant";
    public const string ServiceTenantClaim = "tid";
    public const string SessionClaim = "sid";

    /// <summary>Applies the rule, and binds the caller's context when it holds.</summary>
    /// <returns>Null when the token may proceed; otherwise why it is refused.</returns>
    public static async ValueTask<string?> BindAsync(
        ClaimsPrincipal token,
        RequestTenantContext tenant,
        RequestPrincipal principal,
        ISessionRegistry sessions,
        CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(token);
        ArgumentNullException.ThrowIfNull(tenant);
        ArgumentNullException.ThrowIfNull(principal);
        ArgumentNullException.ThrowIfNull(sessions);
        if (!tenant.IsResolved)
        {
            return "the request's host resolved to no tenant";
        }

        var isService = token.FindAll("aud").Any(a => a.Value is "cell" or "control-plane");
        var claimed = token.FindFirst(isService ? ServiceTenantClaim : TenantClaim)?.Value;
        if (!Guid.TryParse(claimed, out var tokenTenant) || tokenTenant != tenant.TenantId)
        {
            return "the token's tenant is not the tenant this host serves";
        }

        if (isService)
        {
            // serviceAuth: no user; the tenant root, audited as the calling cell (MIGRATIONS.md, the connection context).
            tenant.Bind([tenant.TenantRootPath], principalId: null, subjectId: null);
            principal.BindService();
            return null;
        }

        var sessionId = token.FindFirst(SessionClaim)?.Value;
        if (string.IsNullOrEmpty(sessionId))
        {
            return "the token names no session";
        }

        var session = await sessions.FindAsync(sessionId, cancellationToken).ConfigureAwait(false);
        if (session is null)
        {
            return "the token's session is not live";
        }

        if (session.TenantId != tenant.TenantId)
        {
            return "the token's session belongs to another tenant";
        }

        tenant.Bind(session.ScopePaths, session.PrincipalId, session.SubjectId, workstationId: session.WorkstationId);
        principal.Bind(session);
        return null;
    }
}
