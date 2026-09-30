namespace TICVAI.Infrastructure.Messaging;

/// <summary>
/// How the outbox relay polls one tenant database (ADR-0058, amended 1 October 2026). Bound from
/// the <c>Relay</c> configuration section, so an environment changes it without a build.
/// </summary>
public sealed class RelayOptions
{
    public const string SectionName = "Relay";

    /// <summary>
    /// Rows read and published per poll. 200 in a shared cell; the flash-sale burst environment
    /// sets 1,000 (ADR-0058: one tenant's on-sale produces 2,270-2,850 events a second).
    /// </summary>
    public int BatchSize { get; set; } = 200;

    /// <summary>The wait after a batch that was not full: rows are arriving, but slower than we read.</summary>
    public TimeSpan BusyInterval { get; set; } = TimeSpan.FromMilliseconds(100);

    /// <summary>The longest wait when a tenant has nothing to relay. An idle tenant costs one indexed query this often.</summary>
    public TimeSpan IdleInterval { get; set; } = TimeSpan.FromSeconds(2);

    /// <summary>The largest batch any environment may set: a batch is one transaction holding row locks.</summary>
    public const int MaxBatchSize = 5_000;
}
