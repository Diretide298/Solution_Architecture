namespace TICVAI.Application.Abstractions.Messaging;

/// <summary>
/// What a module publishes through. Writes the event to <c>platform.outbox</c> in the caller's
/// transaction, beside the state change it reports, so both commit or neither does (ADR-0033).
/// </summary>
/// <remarks>
/// It never talks to the broker: a crash between commit and a direct publish would lose the event.
/// The relay reads the outbox and publishes through <see cref="IBrokerPublisher"/> (ADR-0058).
/// </remarks>
public interface IOutbox
{
    /// <summary>
    /// Adds the event to the outbox inside the current transaction. Call it before the commit,
    /// never after, and never outside a transaction that also writes the state change.
    /// </summary>
    Task EnqueueAsync(IIntegrationEvent integrationEvent, CancellationToken cancellationToken);
}
