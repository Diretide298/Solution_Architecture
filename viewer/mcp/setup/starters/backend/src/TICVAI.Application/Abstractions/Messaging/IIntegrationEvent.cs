namespace TICVAI.Application.Abstractions.Messaging;

/// <summary>
/// A fact one module publishes and others consume, as the event catalogue (<c>events/*.yaml</c>)
/// names it. A module hands it to <see cref="IOutbox"/>; it reaches the broker only through the
/// relay (ADR-0033, ADR-0058).
/// </summary>
/// <remarks>
/// These members are the envelope of ADR-0058 and the columns of <c>platform.outbox</c>. The event
/// type's own public properties are the payload the catalogue lists.
/// </remarks>
public interface IIntegrationEvent
{
    /// <summary>
    /// The event's id and the outbox row's id: a UUIDv7 from <c>Identity.Id.New()</c>. Consumers
    /// de-duplicate on it through their inbox, so a retried publish is never a second effect.
    /// </summary>
    Guid EventId { get; }

    /// <summary>The catalogue name, for example <c>order.paid</c>.</summary>
    string EventName { get; }

    /// <summary>The catalogue <c>version</c>. A new shape is a new version (api-conventions 6).</summary>
    int EventVersion { get; }

    /// <summary>The catalogue <c>aggregate</c>, for example <c>order</c>.</summary>
    string AggregateType { get; }

    /// <summary>
    /// The aggregate the event is about. It is the broker's ordering key: one aggregate's events
    /// arrive in order, and nothing is ordered across aggregates (ADR-0057).
    /// </summary>
    Guid AggregateId { get; }

    /// <summary>
    /// The aggregate's version after this change, 1 for its first event, one higher for each event
    /// after. Assigned in the transaction that changes the aggregate, so a consumer that sees a gap
    /// knows an earlier event is still on its way and retries later (ADR-0058).
    /// </summary>
    int Sequence { get; }

    /// <summary>The tenant whose database the outbox row is in.</summary>
    Guid TenantId { get; }

    /// <summary>
    /// The scope-tree path (ltree text) of the aggregate, as in <see cref="Security.ITenantContext.ScopePaths"/>.
    /// Consumers and row-level security scope the event by it.
    /// </summary>
    string ScopePath { get; }

    /// <summary>When the change happened, UTC.</summary>
    DateTimeOffset OccurredAt { get; }
}
