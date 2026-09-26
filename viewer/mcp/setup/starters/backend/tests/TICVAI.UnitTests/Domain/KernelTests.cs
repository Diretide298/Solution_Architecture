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

public class UlidTests
{
    [Fact]
    public void Matches_the_contract_pattern()
    {
        var id = Ulid.New();
        Assert.Matches("^[0-9A-HJKMNP-TV-Z]{26}$", id);
        Assert.True(Ulid.IsValid(id));
    }

    [Fact]
    public void Carries_its_creation_time()
    {
        var at = new DateTimeOffset(2026, 9, 27, 10, 30, 0, TimeSpan.Zero);
        Assert.Equal(at, Ulid.TimeOf(Ulid.New(at)));
    }

    [Fact]
    public void Sorts_by_creation_time()
    {
        var earlier = Ulid.New(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
        var later = Ulid.New(new DateTimeOffset(2026, 1, 1, 0, 0, 1, TimeSpan.Zero));
        Assert.True(string.CompareOrdinal(earlier, later) < 0);
    }
}
