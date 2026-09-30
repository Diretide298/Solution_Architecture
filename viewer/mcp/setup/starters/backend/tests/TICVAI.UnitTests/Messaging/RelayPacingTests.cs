using TICVAI.Infrastructure.Messaging;

namespace TICVAI.UnitTests.Messaging;

public class RelayPacingTests
{
    private static readonly RelayOptions Options = new();

    [Fact]
    public void Polls_again_at_once_after_a_full_batch()
    {
        Assert.Equal(TimeSpan.Zero, RelayPacing.NextDelay(200, TimeSpan.FromSeconds(2), Options));
    }

    [Fact]
    public void Drains_at_the_batch_size_an_environment_sets()
    {
        var burst = new RelayOptions { BatchSize = 1_000 };

        Assert.Equal(TimeSpan.Zero, RelayPacing.NextDelay(1_000, TimeSpan.Zero, burst));
        Assert.Equal(burst.BusyInterval, RelayPacing.NextDelay(999, TimeSpan.Zero, burst));
    }

    [Fact]
    public void Waits_the_busy_interval_after_a_partial_batch()
    {
        Assert.Equal(TimeSpan.FromMilliseconds(100), RelayPacing.NextDelay(37, TimeSpan.Zero, Options));
    }

    [Fact]
    public void Backs_off_to_the_idle_interval_when_nothing_is_there()
    {
        var delay = TimeSpan.Zero;
        var seen = new List<TimeSpan>();
        for (var i = 0; i < 8; i++)
        {
            delay = RelayPacing.NextDelay(0, delay, Options);
            seen.Add(delay);
        }

        Assert.Equal(TimeSpan.FromMilliseconds(100), seen[0]);
        Assert.Equal(TimeSpan.FromMilliseconds(200), seen[1]);
        Assert.Equal(TimeSpan.FromSeconds(2), seen[^1]);
        Assert.All(seen, d => Assert.True(d <= Options.IdleInterval));
    }

    [Theory]
    [InlineData(0)]
    [InlineData(RelayOptions.MaxBatchSize + 1)]
    public void Refuses_a_batch_size_outside_the_limits(int batchSize)
    {
        Assert.Throws<ArgumentOutOfRangeException>(
            () => RelayPacing.NextDelay(0, TimeSpan.Zero, new RelayOptions { BatchSize = batchSize }));
    }
}
