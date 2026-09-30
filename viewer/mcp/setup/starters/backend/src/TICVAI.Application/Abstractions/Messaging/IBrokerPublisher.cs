namespace TICVAI.Application.Abstractions.Messaging;

/// <summary>
/// Sends outbox rows to the event broker. <b>The relay's interface, not a module's</b>: modules
/// publish through <see cref="IOutbox"/> and never see the broker (ADR-0057, ADR-0058).
/// </summary>
/// <remarks>
/// <para>
/// One adapter per broker (RabbitMQ; Kafka if the client chooses it) implements it, and only the
/// adapter knows the broker. It exposes only what both brokers can do: publish a batch with an
/// ordering key. No priorities, no per-message TTL, no broker-side replay.
/// </para>
/// <para>
/// Republishing from the outbox (a lost broker, a DR failover) goes through this same interface:
/// the relay reads the rows again and publishes them; each consumer's inbox absorbs the duplicates.
/// </para>
/// </remarks>
public interface IBrokerPublisher
{
    /// <summary>
    /// Publishes the batch in order, each message keyed by <see cref="EventEnvelope.OrderingKey"/>,
    /// and returns once the broker has confirmed every message. Confirms are awaited for the batch
    /// together, not one round trip per message. If any message is not confirmed it throws: the
    /// relay leaves the whole batch unpublished and sends it again.
    /// </summary>
    Task PublishBatchAsync(IReadOnlyList<EventEnvelope> batch, CancellationToken cancellationToken);
}
