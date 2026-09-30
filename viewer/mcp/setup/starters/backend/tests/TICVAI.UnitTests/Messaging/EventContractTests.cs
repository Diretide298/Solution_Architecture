using System.Reflection;
using TICVAI.Application.Abstractions.Messaging;
using TICVAI.Domain.Identity;

namespace TICVAI.UnitTests.Messaging;

/// <summary>The two publishing roles stay apart, and the event carries the ADR-0058 envelope.</summary>
public class EventContractTests
{
    [Theory]
    [InlineData(nameof(IIntegrationEvent.EventId))]
    [InlineData(nameof(IIntegrationEvent.EventName))]
    [InlineData(nameof(IIntegrationEvent.AggregateType))]
    [InlineData(nameof(IIntegrationEvent.AggregateId))]
    [InlineData(nameof(IIntegrationEvent.Sequence))]
    [InlineData(nameof(IIntegrationEvent.TenantId))]
    [InlineData(nameof(IIntegrationEvent.ScopePath))]
    [InlineData(nameof(IIntegrationEvent.OccurredAt))]
    public void An_integration_event_carries_every_envelope_field(string member)
    {
        Assert.NotNull(typeof(IIntegrationEvent).GetProperty(member));
        Assert.NotNull(typeof(EventEnvelope).GetProperty(member));
    }

    [Fact]
    public void A_module_enqueues_and_never_sees_the_broker()
    {
        var outboxParameters = typeof(IOutbox).GetMethods()
            .SelectMany(m => m.GetParameters())
            .Select(p => p.ParameterType);

        Assert.DoesNotContain(typeof(IOutbox).GetMethods(), m => m.Name.Contains("Publish", StringComparison.Ordinal));
        Assert.DoesNotContain(typeof(EventEnvelope), outboxParameters);
        Assert.False(typeof(IBrokerPublisher).IsAssignableFrom(typeof(IOutbox)));
        Assert.False(typeof(IOutbox).IsAssignableFrom(typeof(IBrokerPublisher)));
    }

    [Fact]
    public void The_ordering_key_is_the_aggregate_id()
    {
        var aggregateId = Id.New();
        var envelope = new EventEnvelope(
            Id.New(), "order.paid", 1, "order", aggregateId, 3, Id.New(), "t1.v1",
            new DateTimeOffset(2026, 10, 1, 9, 0, 0, TimeSpan.Zero), "{}");

        Assert.Equal(aggregateId.ToString(), envelope.OrderingKey);
    }

    [Fact]
    public void The_broker_publisher_takes_a_batch()
    {
        var publish = typeof(IBrokerPublisher).GetMethod(nameof(IBrokerPublisher.PublishBatchAsync), BindingFlags.Public | BindingFlags.Instance);

        Assert.NotNull(publish);
        Assert.Equal(typeof(IReadOnlyList<EventEnvelope>), publish!.GetParameters()[0].ParameterType);
    }
}
