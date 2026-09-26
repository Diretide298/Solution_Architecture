namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// Who is making the current request: a staff principal or a guest subject. "Principal" is the
/// package's word (identity.principal); "User" and a bare "Service" suffix are not.
/// </summary>
public interface ICurrentPrincipal
{
    /// <summary>identity.principal.id for staff; null for a guest or an anonymous call.</summary>
    Guid? PrincipalId { get; }

    /// <summary>The guest subject, when a guest is calling (ADR-0025: a guest sees only their own data).</summary>
    Guid? SubjectId { get; }

    bool IsAuthenticated { get; }

    /// <summary>
    /// The permissions resolved for this principal at this scope - the contracts'
    /// x-ticvai-permission values. Resolved on the server from roles, never taken from the client.
    /// </summary>
    IReadOnlySet<string> EffectivePermissions { get; }

    bool Has(string permission) => EffectivePermissions.Contains(permission);
}
