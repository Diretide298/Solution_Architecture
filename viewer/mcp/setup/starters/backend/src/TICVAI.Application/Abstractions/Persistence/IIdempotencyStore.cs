namespace TICVAI.Application.Abstractions.Persistence;

/// <summary>
/// Remembers the answer to a mutating request by its Idempotency-Key, so a retried request gets
/// the first answer instead of doing the work twice (api-conventions: Idempotency-Key).
/// </summary>
public interface IIdempotencyStore
{
    /// <summary>The stored response for this key and request fingerprint, if any.</summary>
    Task<IdempotentResponse?> FindAsync(string key, string requestHash, CancellationToken cancellationToken);

    Task SaveAsync(string key, string requestHash, IdempotentResponse response, TimeSpan keepFor, CancellationToken cancellationToken);
}

/// <param name="StatusCode">The HTTP status the first request answered.</param>
/// <param name="Body">The response body, as sent.</param>
public sealed record IdempotentResponse(int StatusCode, string Body);
