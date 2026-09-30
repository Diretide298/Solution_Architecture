namespace TICVAI.Application.Abstractions.Messaging;

/// <summary>
/// One outbox row as the broker carries it: the ADR-0058 envelope, with the payload already
/// serialised. The relay builds it from <c>platform.outbox</c>; consumers receive it.
/// </summary>
/// <param name="EventId">The outbox row id (UUIDv7). The consumer's inbox key.</param>
/// <param name="EventName">The catalogue name, for example <c>order.paid</c>.</param>
/// <param name="EventVersion">The catalogue version.</param>
/// <param name="AggregateType">The catalogue aggregate.</param>
/// <param name="AggregateId">The aggregate; the ordering key.</param>
/// <param name="Sequence">The aggregate's version after the change; consumers check it for gaps.</param>
/// <param name="TenantId">The tenant. Also sent as a header; there is no topic or queue per tenant.</param>
/// <param name="ScopePath">The aggregate's scope-tree path (ltree text).</param>
/// <param name="OccurredAt">When the change happened, UTC.</param>
/// <param name="Payload">The event's payload as JSON.</param>
/// <param name="TraceId">The trace the change was made in, if any, so a consumer's work joins it.</param>
public sealed record EventEnvelope(
    Guid EventId,
    string EventName,
    int EventVersion,
    string AggregateType,
    Guid AggregateId,
    int Sequence,
    Guid TenantId,
    string ScopePath,
    DateTimeOffset OccurredAt,
    string Payload,
    string? TraceId = null)
{
    /// <summary>
    /// The broker's ordering key: the aggregate id. The Kafka partition key, or the RabbitMQ
    /// consistent-hash routing key (ADR-0057).
    /// </summary>
    public string OrderingKey => AggregateId.ToString();
}
