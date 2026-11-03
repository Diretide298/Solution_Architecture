using TICVAI.Application.Abstractions.Persistence;
using TICVAI.Infrastructure.Idempotency;

namespace TICVAI.UnitTests.Persistence;

/// <summary>
/// The Idempotency-Key rule (common.yaml IdempotencyKey; SD-024; ADAM CR-182) through
/// <see cref="IdempotentExecution"/>, over a store with the database's uniqueness and a transaction
/// runner that keeps a change's effects only when its transaction commits.
/// </summary>
public class IdempotencyTests
{
    private static readonly Guid Key = Guid.Parse("01920000-0000-7000-8000-000000000001");

    [Fact]
    public async Task A_replay_with_the_same_request_gets_the_first_answer_and_writes_nothing()
    {
        var (run, ledger) = Build();

        var first = await run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), ledger.Change("paid 10"), default);
        var again = await run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), ledger.Change("paid 10"), default);

        Assert.Equal(IdempotentOutcomeKind.Applied, first.Kind);
        Assert.Equal(IdempotentOutcomeKind.Replayed, again.Kind);
        Assert.Equal(first.Response, again.Response);
        Assert.Equal(["paid 10"], ledger.Committed);
    }

    [Fact]
    public async Task A_reused_key_with_a_different_request_is_a_conflict_and_never_applied()
    {
        var (run, ledger) = Build();

        await run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), ledger.Change("paid 10"), default);
        var other = await run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-b"), ledger.Change("paid 99"), default);

        Assert.Equal(IdempotentOutcomeKind.Conflict, other.Kind);
        Assert.Null(other.Response);
        Assert.Equal("idempotency-conflict", IdempotentOutcome.ConflictProblemType);
        Assert.Equal(["paid 10"], ledger.Committed);
    }

    [Fact]
    public async Task The_same_key_on_another_operation_is_another_request()
    {
        var (run, ledger) = Build();

        await run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), ledger.Change("paid"), default);
        var refund = await run.RunAsync(new IdempotencyRequest(Key, "createRefund", "hash-a"), ledger.Change("refunded"), default);

        Assert.Equal(IdempotentOutcomeKind.Applied, refund.Kind);
        Assert.Equal(["paid", "refunded"], ledger.Committed);
    }

    [Fact]
    public async Task Two_concurrent_first_requests_apply_once()
    {
        var (run, ledger) = Build();
        var bothInside = new Barrier(2);
        Func<CancellationToken, Task<IdempotentResponse>> change = async token =>
        {
            ledger.Pending.Value!.Add("paid 10");
            await Task.Run(() => bothInside.SignalAndWait(TimeSpan.FromSeconds(5)), token);
            return new IdempotentResponse(201, "{\"paid\":10}");
        };

        var outcomes = await Task.WhenAll(
            Task.Run(() => run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), change, default)),
            Task.Run(() => run.RunAsync(new IdempotencyRequest(Key, "createPayment", "hash-a"), change, default)));

        Assert.Equal([IdempotentOutcomeKind.Applied, IdempotentOutcomeKind.Replayed], outcomes.Select(o => o.Kind).Order());
        Assert.Equal(["paid 10"], ledger.Committed);
    }

    private static (IdempotentExecution Run, Ledger Ledger) Build()
    {
        var ledger = new Ledger();
        return (new IdempotentExecution(new InMemoryIdempotencyStore(TimeProvider.System), ledger), ledger);
    }

    /// <summary>A transaction runner whose effects are kept only on commit, like the database's.</summary>
    private sealed class Ledger : ITransactionRunner
    {
        private readonly Lock _gate = new();

        public AsyncLocal<List<string>?> Pending { get; } = new();

        public List<string> Committed { get; } = [];

        public Func<CancellationToken, Task<IdempotentResponse>> Change(string effect) => _ =>
        {
            Pending.Value!.Add(effect);
            return Task.FromResult(new IdempotentResponse(201, $"{{\"effect\":\"{effect}\"}}"));
        };

        public async Task<T> RunAsync<T>(Func<CancellationToken, Task<T>> work, CancellationToken cancellationToken)
        {
            Pending.Value = [];
            var result = await work(cancellationToken);
            lock (_gate)
            {
                Committed.AddRange(Pending.Value);
            }

            return result;
        }
    }
}
