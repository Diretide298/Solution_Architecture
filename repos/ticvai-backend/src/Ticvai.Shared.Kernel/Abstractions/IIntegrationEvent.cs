namespace Ticvai.Shared.Kernel.Abstractions;

/// <summary>
/// A fact published by one module and consumed by others. Published through the
/// transactional outbox so publication is atomic with the state change.
/// </summary>
public interface IIntegrationEvent
{
    Guid EventId { get; }
    DateTimeOffset OccurredAt { get; }
    Guid TenantId { get; }
    Guid VenueId { get; }

    /// <summary>Stable name, e.g. <c>orders.order.completed.v1</c>. Version lives in the name.</summary>
    string EventType { get; }
}

public interface IEventPublisher
{
    /// <summary>
    /// Enqueues onto the outbox within the caller's transaction. Never publishes
    /// directly to the bus — a crash between commit and publish would lose the event.
    /// </summary>
    Task PublishAsync(IIntegrationEvent @event, CancellationToken cancellationToken = default);
}
