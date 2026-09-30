namespace TICVAI.Infrastructure.Messaging;

/// <summary>
/// When the relay's loop for one tenant database polls next (ADR-0058, amended 1 October 2026).
/// </summary>
/// <remarks>
/// <b>A full batch means there is more: poll again at once.</b> Waiting the busy interval after a
/// full batch caps a tenant at <c>BatchSize / BusyInterval</c> (200 rows / 100 ms = 2,000 events a
/// second), below a single-tenant flash sale. Draining removes that cap; the ceiling becomes the
/// time one poll-publish-commit cycle takes.
/// </remarks>
public static class RelayPacing
{
    /// <summary>
    /// The wait before the next poll, given how many rows the last one read and the wait before it.
    /// A full batch: none. Some rows: the busy interval. None: double the last wait, from the busy
    /// interval up to the idle interval.
    /// </summary>
    public static TimeSpan NextDelay(int rowsRead, TimeSpan previousDelay, RelayOptions options)
    {
        ArgumentNullException.ThrowIfNull(options);
        ArgumentOutOfRangeException.ThrowIfNegative(rowsRead);
        ArgumentOutOfRangeException.ThrowIfLessThan(options.BatchSize, 1, nameof(options));
        ArgumentOutOfRangeException.ThrowIfGreaterThan(options.BatchSize, RelayOptions.MaxBatchSize, nameof(options));

        if (rowsRead >= options.BatchSize)
        {
            return TimeSpan.Zero;
        }

        if (rowsRead > 0)
        {
            return options.BusyInterval;
        }

        var backedOff = previousDelay < options.BusyInterval ? options.BusyInterval : previousDelay * 2;
        return backedOff > options.IdleInterval ? options.IdleInterval : backedOff;
    }
}
