using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// The request's <see cref="ICurrentPrincipal"/>: anonymous, with everything denied, until
/// authentication binds a validated session to it.
/// </summary>
public sealed class RequestPrincipal : ICurrentPrincipal
{
    public Guid? PrincipalId { get; private set; }

    public Guid? SubjectId { get; private set; }

    public bool IsAuthenticated { get; private set; }

    public ResolvedAuthority Authority { get; private set; } = ResolvedAuthority.None;

    /// <summary>A validated session of the request's tenant.</summary>
    public void Bind(SessionRecord session)
    {
        ArgumentNullException.ThrowIfNull(session);
        PrincipalId = session.PrincipalId;
        SubjectId = session.SubjectId;
        Authority = session.Authority;
        IsAuthenticated = true;
    }

    /// <summary>A cell-internal serviceAuth call: authenticated, no user, no grants (the permission model does not apply).</summary>
    public void BindService()
    {
        IsAuthenticated = true;
    }
}
