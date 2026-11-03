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
    /// The selected role's grants, resolved at login (R6, R7) and read from the session registry;
    /// <see cref="ResolvedAuthority.None"/> (everything denied) when there is no session.
    /// </summary>
    ResolvedAuthority Authority { get; }

    /// <summary>
    /// <b>The permission check for an operation</b>: is the contract's <c>x-ticvai-permission</c>
    /// permitted at the scope the operation acts on (spec 7.2)? Pass the venue, workstation or other
    /// node the request acts on, or the tenant root for a tenant-level operation.
    /// </summary>
    bool Permits(string permission, string scopePath) => Authority.Permits(permission, scopePath);

    /// <summary>
    /// Permissions held at one scope at least. Coarse checks only; never decides an operation
    /// (spec 7.2: a permission at venue A and anything at venue B puts it here).
    /// </summary>
    IReadOnlySet<string> EffectivePermissions => Authority.EffectivePermissions;
}
