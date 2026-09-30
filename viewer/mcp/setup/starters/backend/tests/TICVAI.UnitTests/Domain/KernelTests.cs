using TICVAI.Domain.Identity;
using TICVAI.Domain.ValueObjects;

namespace TICVAI.UnitTests.Domain;

public class MoneyTests
{
    [Fact]
    public void Adds_amounts_in_the_same_currency()
    {
        var total = new Money(10.50m, "AED") + new Money(2.25m, "AED");
        Assert.Equal(new Money(12.75m, "AED"), total);
    }

    [Fact]
    public void Refuses_to_combine_two_currencies()
    {
        Assert.Throws<InvalidOperationException>(() => new Money(1m, "AED") + new Money(1m, "OMR"));
    }

    [Theory]
    [InlineData("aed")]
    [InlineData("AE")]
    [InlineData("")]
    public void Refuses_a_currency_that_is_not_iso_4217(string currency)
    {
        Assert.Throws<ArgumentException>(() => new Money(1m, currency));
    }

    [Fact]
    public void Rounds_to_the_currency_minor_units()
    {
        Assert.Equal(1.235m, new Money(1.2345m, "OMR").Round(3).Amount);
        Assert.Equal(1.24m, new Money(1.235m, "AED").Round(2).Amount);
    }
}

public class IdTests
{
    [Fact]
    public void Generates_version_7_ids()
    {
        var id = Id.New();
        Assert.Equal(7, id.Version);
        Assert.True(Id.IsVersion7(id));
        Assert.NotEqual(id, Id.New());
    }

    [Fact]
    public void Does_not_take_a_version_4_id_for_a_new_one()
    {
        Assert.False(Id.IsVersion7(Guid.Parse("3f2504e0-4f89-41d3-9a0c-0305e82c3301")));
    }

    [Fact]
    public void Carries_the_time_it_was_minted_for_to_the_millisecond()
    {
        var at = new DateTimeOffset(2026, 9, 30, 10, 30, 0, 123, TimeSpan.Zero);
        Assert.Equal(at, Id.TimeOf(Id.New(at)));
    }

    [Fact]
    public void Sorts_by_the_time_it_was_minted_for()
    {
        var earlier = Id.New(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
        var later = Id.New(new DateTimeOffset(2026, 1, 1, 0, 0, 0, 1, TimeSpan.Zero));
        Assert.True(string.CompareOrdinal(earlier.ToString(), later.ToString()) < 0);
    }
}
