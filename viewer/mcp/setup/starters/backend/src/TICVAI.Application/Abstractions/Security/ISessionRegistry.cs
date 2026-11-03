namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// The server-side session registry a staff or guest token's <c>sid</c> is validated against
/// (ADR-0004; <c>common.yaml</c> <c>bearerAuth</c>). The session holds what was resolved at login:
/// the selected role's grants (R6, R7) and the caller's scope.
/// </summary>
/// <remarks>
/// The starter registers a registry with no sessions, so every token is refused until sign-in builds
/// the real one (Redis, one session per principal). A session opened for another tenant is refused
/// like a token naming another tenant (r13 review C-05).
/// </remarks>
public interface ISessionRegistry
{
    /// <summary>The live session <paramref name="sessionId"/> names, or null when there is none.</summary>
    ValueTask<SessionRecord?> FindAsync(string sessionId, CancellationToken cancellationToken);
}

/// <param name="SessionId">The <c>sid</c>.</param>
/// <param name="TenantId">The tenant the session was opened in.</param>
/// <param name="PrincipalId">The staff principal; null for a guest.</param>
/// <param name="SubjectId">The guest subject; null for staff.</param>
/// <param name="Authority">The selected role's resolved grants.</param>
/// <param name="ScopePaths">The paths the session's grants reach, for <c>ticvai.scope_paths</c>.</param>
/// <param name="WorkstationId">The workstation the session is on, if any (a scope target, never a permission source: R5).</param>
public sealed record SessionRecord(
    string SessionId,
    Guid TenantId,
    Guid? PrincipalId,
    Guid? SubjectId,
    ResolvedAuthority Authority,
    IReadOnlyList<string> ScopePaths,
    string? WorkstationId = null);
