namespace TICVAI.Application.Abstractions.Persistence;

/// <summary>
/// The durable record of a mutating request's answer, by its <c>Idempotency-Key</c> and operation
/// (<c>common.yaml</c> <c>IdempotencyKey</c>; SD-024; ADAM CR-182): <c>platform.idempotency_record</c>,
/// unique on (<c>operation_id</c>, <c>idempotency_key</c>), written <b>in the same transaction as the
/// state change</b>. Redis may cache it in front; it is never the guarantee.
/// </summary>
/// <remarks>
/// Use it through <see cref="IdempotentExecution"/>, which runs the whole rule: a replay of a completed
/// key gets the first answer, a reused key with a different request is a <c>409 idempotency-conflict</c>
/// and never applied, and two concurrent first requests apply once (the second waits on the unique
/// index, fails on it when the first commits, rolls back and replays).
/// </remarks>
public interface IIdempotencyStore
{
    /// <summary>The completed record for this key and operation, if any, inside the current transaction.</summary>
    Task<IdempotencyRecord?> FindAsync(Guid key, string operationId, CancellationToken cancellationToken);

    /// <summary>
    /// Writes the completed record in the current transaction, beside the state change. Throws
    /// <see cref="IdempotencyKeyTakenException"/> when a concurrent request committed the same key and
    /// operation first: the caller rolls back and replays.
    /// </summary>
    Task RecordAsync(IdempotencyRequest request, IdempotentResponse response, CancellationToken cancellationToken);
}

/// <param name="Key">The <c>Idempotency-Key</c> header (a uuid; an edge-created entity's client UUIDv7).</param>
/// <param name="OperationId">The contract's <c>operationId</c>.</param>
/// <param name="RequestHash">A hash of the request body (SHA-256 hex, at most 64 characters).</param>
public sealed record IdempotencyRequest(Guid Key, string OperationId, string RequestHash);

/// <summary>A stored record: the request's hash and the answer it got.</summary>
public sealed record IdempotencyRecord(string RequestHash, IdempotentResponse Response);

/// <param name="StatusCode">The HTTP status the first request answered.</param>
/// <param name="Body">The response body, as sent (JSON).</param>
public sealed record IdempotentResponse(int StatusCode, string Body);

/// <summary>A concurrent request with the same key and operation committed first.</summary>
public sealed class IdempotencyKeyTakenException(Guid key, string operationId, Exception? inner = null)
    : Exception($"Idempotency-Key {key} for {operationId} was recorded by a concurrent request", inner);
