using System.Collections.Concurrent;
using TICVAI.Application.Abstractions.Persistence;

namespace TICVAI.Infrastructure.Idempotency;

/// <summary>
/// For unit tests only: the same rule as <see cref="PostgresIdempotencyStore"/>, unique on (operation,
/// key), with no database. It is never registered by <c>AddInfrastructure</c>: the durable record in
/// the change's transaction is the guarantee (SD-024), and nothing in memory or in Redis can be.
/// </summary>
public sealed class InMemoryIdempotencyStore(TimeProvider clock) : IIdempotencyStore
{
    private readonly ConcurrentDictionary<(string OperationId, Guid Key), (IdempotencyRecord Record, DateTimeOffset Until)> _records = new();

    public Task<IdempotencyRecord?> FindAsync(Guid key, string operationId, CancellationToken cancellationToken) =>
        Task.FromResult(_records.TryGetValue((operationId, key), out var entry) && entry.Until > clock.GetUtcNow()
            ? entry.Record
            : null);

    public Task RecordAsync(IdempotencyRequest request, IdempotentResponse response, CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(request);
        var entry = (new IdempotencyRecord(request.RequestHash, response), clock.GetUtcNow().Add(PostgresIdempotencyStore.Keep));
        if (!_records.TryAdd((request.OperationId, request.Key), entry))
        {
            throw new IdempotencyKeyTakenException(request.Key, request.OperationId);
        }

        return Task.CompletedTask;
    }
}
