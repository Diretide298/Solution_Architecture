using System.Text.Json;
using Microsoft.Extensions.Logging;
using StackExchange.Redis;
using Ticvai.Shared.Kernel.Primitives;

namespace Ticvai.Modules.Identity.Infrastructure;

public sealed record SessionRecord
{
    public required Guid SessionId { get; init; }
    public required Guid PrincipalId { get; init; }
    public required Guid TenantId { get; init; }
    public required Guid RoleId { get; init; }
    public required Guid WorkstationId { get; init; }
    public required Guid VenueId { get; init; }
    public required IReadOnlyList<string> Permissions { get; init; }
    public required IReadOnlyDictionary<string, string[]> PermissionsByScope { get; init; }
    public required DateTimeOffset OpenedAt { get; init; }
    public required DateTimeOffset ExpiresAt { get; init; }
    public string? DeviceFingerprint { get; init; }
}

public enum SessionOpenOutcome
{
    Opened,
    RejectedExistingSession
}

public sealed record SessionOpenResult(
    SessionOpenOutcome Outcome,
    SessionRecord? Session,
    SessionRecord? ExistingSession);

/// <summary>
/// Tracks live sessions and enforces the single-session rule.
/// </summary>
/// <remarks>
/// <para>
/// Project Direction §3.1.3: one session per user. A second login is <b>rejected</b>,
/// not auto-terminating the first — auto-terminate can orphan an open cart or an
/// unclosed cash drawer, which is worse than a refused login.
/// </para>
/// <para>
/// This registry exists because single-session cannot be enforced with stateless
/// JWT alone: a valid token stays valid until expiry, so there is no way to
/// invalidate device A when the user appears on device B. The JWT carries a
/// <c>sid</c> claim validated against this registry on every request.
/// </para>
/// </remarks>
public interface ISessionRegistry
{
    Task<SessionOpenResult> OpenAsync(SessionRecord session, CancellationToken cancellationToken = default);
    Task<SessionRecord?> GetAsync(Guid sessionId, CancellationToken cancellationToken = default);
    Task<SessionRecord?> GetByPrincipalAsync(Guid principalId, CancellationToken cancellationToken = default);
    Task<bool> CloseAsync(Guid sessionId, CancellationToken cancellationToken = default);
    Task<Result<bool>> ForceLogoutAsync(Guid sessionId, Guid actingPrincipalId, string reason, CancellationToken cancellationToken = default);
    Task<bool> TouchAsync(Guid sessionId, TimeSpan extendBy, CancellationToken cancellationToken = default);
}

public sealed class RedisSessionRegistry(
    IConnectionMultiplexer redis,
    ILogger<RedisSessionRegistry> logger) : ISessionRegistry
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    private static string SessionKey(Guid sessionId) => $"session:{sessionId:N}";
    private static string PrincipalKey(Guid principalId) => $"principal-session:{principalId:N}";

    public async Task<SessionOpenResult> OpenAsync(SessionRecord session, CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(session);
        cancellationToken.ThrowIfCancellationRequested();

        var db = redis.GetDatabase();
        var ttl = session.ExpiresAt - DateTimeOffset.UtcNow;

        if (ttl <= TimeSpan.Zero)
        {
            throw new ArgumentException("Session already expired.", nameof(session));
        }

        // Claim the principal slot atomically. NX means the first login wins and
        // any concurrent second login sees the existing holder.
        var claimed = await db.StringSetAsync(
            PrincipalKey(session.PrincipalId),
            session.SessionId.ToString("N"),
            ttl,
            When.NotExists).ConfigureAwait(false);

        if (!claimed)
        {
            var existing = await GetByPrincipalAsync(session.PrincipalId, cancellationToken).ConfigureAwait(false);

            if (existing is not null)
            {
                logger.LogInformation(
                    "Login rejected for principal {PrincipalId}: session {ExistingSessionId} is active on workstation {WorkstationId}",
                    session.PrincipalId, existing.SessionId, existing.WorkstationId);

                return new SessionOpenResult(SessionOpenOutcome.RejectedExistingSession, null, existing);
            }

            // Pointer existed but the record had expired — a torn state. Reclaim it.
            logger.LogWarning(
                "Stale principal pointer for {PrincipalId} with no session record. Reclaiming.",
                session.PrincipalId);

            await db.StringSetAsync(
                PrincipalKey(session.PrincipalId),
                session.SessionId.ToString("N"),
                ttl).ConfigureAwait(false);
        }

        await db.StringSetAsync(
            SessionKey(session.SessionId),
            JsonSerializer.Serialize(session, JsonOptions),
            ttl).ConfigureAwait(false);

        logger.LogInformation(
            "Session {SessionId} opened for principal {PrincipalId} on workstation {WorkstationId}",
            session.SessionId, session.PrincipalId, session.WorkstationId);

        return new SessionOpenResult(SessionOpenOutcome.Opened, session, null);
    }

    public async Task<SessionRecord?> GetAsync(Guid sessionId, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var value = await redis.GetDatabase().StringGetAsync(SessionKey(sessionId)).ConfigureAwait(false);
        return value.HasValue ? JsonSerializer.Deserialize<SessionRecord>(value!, JsonOptions) : null;
    }

    public async Task<SessionRecord?> GetByPrincipalAsync(Guid principalId, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();

        var pointer = await redis.GetDatabase().StringGetAsync(PrincipalKey(principalId)).ConfigureAwait(false);

        if (!pointer.HasValue || !Guid.TryParse(pointer!, out var sessionId))
        {
            return null;
        }

        return await GetAsync(sessionId, cancellationToken).ConfigureAwait(false);
    }

    public async Task<bool> CloseAsync(Guid sessionId, CancellationToken cancellationToken = default)
    {
        var session = await GetAsync(sessionId, cancellationToken).ConfigureAwait(false);
        if (session is null) return false;

        var db = redis.GetDatabase();
        var batch = db.CreateBatch();

        var removeSession = batch.KeyDeleteAsync(SessionKey(sessionId));
        var removePointer = batch.KeyDeleteAsync(PrincipalKey(session.PrincipalId));

        batch.Execute();
        await Task.WhenAll(removeSession, removePointer).ConfigureAwait(false);

        logger.LogInformation("Session {SessionId} closed", sessionId);
        return true;
    }

    /// <summary>
    /// Supervisor termination of an abandoned session. Exists precisely because
    /// <see cref="OpenAsync"/> rejects rather than displaces — an operator who went
    /// home still logged in would otherwise be locked out until token expiry.
    /// The caller is responsible for verifying SESSION_FORCE_LOGOUT before calling.
    /// </summary>
    public async Task<Result<bool>> ForceLogoutAsync(
        Guid sessionId,
        Guid actingPrincipalId,
        string reason,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(reason))
        {
            return Result<bool>.Failure(Error.Validation("reason", "A reason is required and is retained for audit."));
        }

        var session = await GetAsync(sessionId, cancellationToken).ConfigureAwait(false);

        if (session is null)
        {
            return Result<bool>.Failure(Error.NotFound("Session"));
        }

        await CloseAsync(sessionId, cancellationToken).ConfigureAwait(false);

        logger.LogWarning(
            "Session {SessionId} for principal {PrincipalId} force-closed by {ActingPrincipalId}. Reason: {Reason}",
            sessionId, session.PrincipalId, actingPrincipalId, reason);

        return Result<bool>.Success(true);
    }

    public async Task<bool> TouchAsync(Guid sessionId, TimeSpan extendBy, CancellationToken cancellationToken = default)
    {
        var session = await GetAsync(sessionId, cancellationToken).ConfigureAwait(false);
        if (session is null) return false;

        var db = redis.GetDatabase();
        var batch = db.CreateBatch();

        var expireSession = batch.KeyExpireAsync(SessionKey(sessionId), extendBy);
        var expirePointer = batch.KeyExpireAsync(PrincipalKey(session.PrincipalId), extendBy);

        batch.Execute();
        var results = await Task.WhenAll(expireSession, expirePointer).ConfigureAwait(false);

        return results.All(r => r);
    }
}
