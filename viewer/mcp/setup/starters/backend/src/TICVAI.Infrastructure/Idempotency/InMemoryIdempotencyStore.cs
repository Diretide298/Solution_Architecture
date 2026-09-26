using System.Collections.Concurrent;
using TICVAI.Application.Abstractions.Persistence;

namespace TICVAI.Infrastructure.Idempotency;

/// <summary>
/// One process, in memory: enough for development and tests. Production keeps keys in Redis so
/// every API instance sees them - replace the registration, not the interface.
/// </summary>
public sealed class InMemoryIdempotencyStore(TimeProvider clock) : IIdempotencyStore
{
    private readonly ConcurrentDictionary<string, (string Hash, IdempotentResponse Response, DateTimeOffset Until)> _entries = new();

    public Task<IdempotentResponse?> FindAsync(string key, string requestHash, CancellationToken cancellationToken)
    {
        if (_entries.TryGetValue(key, out var entry) && entry.Until > clock.GetUtcNow() && entry.Hash == requestHash)
        {
            return Task.FromResult<IdempotentResponse?>(entry.Response);
        }

        return Task.FromResult<IdempotentResponse?>(null);
    }

    public Task SaveAsync(string key, string requestHash, IdempotentResponse response, TimeSpan keepFor, CancellationToken cancellationToken)
    {
        _entries[key] = (requestHash, response, clock.GetUtcNow().Add(keepFor));
        return Task.CompletedTask;
    }
}
