namespace TICVAI.Application.Abstractions.Persistence;

/// <summary>
/// The <c>Idempotency-Key</c> rule for a mutating operation (<c>common.yaml</c> <c>IdempotencyKey</c>,
/// SD-024, ADAM CR-182), in one place so no handler writes its own:
/// <list type="bullet">
/// <item>a completed key with the same request replays the first answer and writes nothing;</item>
/// <item>a completed key with a different request is a conflict (<c>409 idempotency-conflict</c>) and is never applied;</item>
/// <item>a new key runs the change and records the answer in the same transaction;</item>
/// <item>two concurrent first requests apply once: the second fails on the unique index when the first
/// commits, its transaction rolls back, and it replays the first answer.</item>
/// </list>
/// </summary>
public sealed class IdempotentExecution(IIdempotencyStore store, ITransactionRunner transactions)
{
    /// <summary>Runs <paramref name="change"/> at most once for <paramref name="request"/>'s key and operation.</summary>
    public async Task<IdempotentOutcome> RunAsync(
        IdempotencyRequest request,
        Func<CancellationToken, Task<IdempotentResponse>> change,
        CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(request);
        ArgumentNullException.ThrowIfNull(change);
        try
        {
            return await AttemptAsync(request, change, cancellationToken).ConfigureAwait(false);
        }
        catch (IdempotencyKeyTakenException)
        {
            // Rolled back. The concurrent request's record is committed now: this attempt replays it or
            // reports the conflict, and never runs the change.
            return await AttemptAsync(request, change, cancellationToken).ConfigureAwait(false);
        }
    }

    private Task<IdempotentOutcome> AttemptAsync(
        IdempotencyRequest request,
        Func<CancellationToken, Task<IdempotentResponse>> change,
        CancellationToken cancellationToken) =>
        transactions.RunAsync(
            async token =>
            {
                var prior = await store.FindAsync(request.Key, request.OperationId, token).ConfigureAwait(false);
                if (prior is not null)
                {
                    return string.Equals(prior.RequestHash, request.RequestHash, StringComparison.Ordinal)
                        ? IdempotentOutcome.Replayed(prior.Response)
                        : IdempotentOutcome.Conflict;
                }

                var response = await change(token).ConfigureAwait(false);
                await store.RecordAsync(request, response, token).ConfigureAwait(false);
                return IdempotentOutcome.Applied(response);
            },
            cancellationToken);
}

/// <summary>What happened to an idempotent request.</summary>
public enum IdempotentOutcomeKind
{
    /// <summary>The change ran and its answer was recorded.</summary>
    Applied,

    /// <summary>The key was completed before with the same request: the first answer, nothing written.</summary>
    Replayed,

    /// <summary>The key was completed before with a different request: answer <c>409 idempotency-conflict</c>.</summary>
    Conflict,
}

/// <param name="Kind">What happened.</param>
/// <param name="Response">The answer to send: the new one, or the first one; null for a conflict.</param>
public sealed record IdempotentOutcome(IdempotentOutcomeKind Kind, IdempotentResponse? Response)
{
    /// <summary>The shared problem type a conflict answers with.</summary>
    public const string ConflictProblemType = "idempotency-conflict";

    public static IdempotentOutcome Conflict { get; } = new(IdempotentOutcomeKind.Conflict, null);

    public static IdempotentOutcome Applied(IdempotentResponse response) => new(IdempotentOutcomeKind.Applied, response);

    public static IdempotentOutcome Replayed(IdempotentResponse response) => new(IdempotentOutcomeKind.Replayed, response);
}
