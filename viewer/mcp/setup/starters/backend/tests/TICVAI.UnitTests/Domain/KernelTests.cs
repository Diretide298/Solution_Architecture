using System.Text.Json;
using TICVAI.Domain.Identity;
using TICVAI.Domain.ValueObjects;

namespace TICVAI.UnitTests.Domain;

/// <summary>ADR-0008 and common.yaml Money, run on both fixture currencies: AED (2 dp) and OMR (3 dp).</summary>
public class MoneyTests
{
    [Fact]
    public void Adds_amounts_in_the_same_currency()
    {
        var total = new Money(10.50m, "AED", 2) + new Money(2.25m, "AED", 2);
        Assert.Equal(new Money(12.75m, "AED", 2), total);
    }

    [Fact]
    public void Refuses_to_combine_two_currencies()
    {
        Assert.Throws<InvalidOperationException>(() => new Money(1m, "AED", 2) + new Money(1m, "OMR", 3));
    }

    [Fact]
    public void Refuses_to_combine_two_scales()
    {
        Assert.Throws<InvalidOperationException>(() => new Money(1m, "AED", 2) + new Money(1m, "AED", 3));
    }

    [Theory]
    [InlineData("aed")]
    [InlineData("AE")]
    [InlineData("")]
    public void Refuses_a_currency_that_is_not_iso_4217(string currency)
    {
        Assert.Throws<ArgumentException>(() => new Money(1m, currency, 2));
    }

    [Theory]
    [InlineData(10.123, "AED", 2)]
    [InlineData(1.2345, "OMR", 3)]
    [InlineData(10.12345, "AED", 4)]
    public void Refuses_more_decimal_places_than_its_scale(double amount, string currency, int scale)
    {
        Assert.Throws<ArgumentException>(() => new Money((decimal)amount, currency, scale));
    }

    [Theory]
    [InlineData(-1)]
    [InlineData(5)]
    public void Refuses_a_scale_outside_0_to_4(int scale)
    {
        Assert.Throws<ArgumentOutOfRangeException>(() => new Money(1m, "AED", scale));
    }

    [Fact]
    public void Takes_the_iso_4217_minor_units_for_a_currency_other_than_the_trading_one()
    {
        Assert.Equal(2, Money.InMinorUnits(10m, "AED").Scale);
        Assert.Equal(3, Money.InMinorUnits(1.235m, "OMR").Scale);
        Assert.Equal(0, CurrencyMinorUnits.For("JPY"));
        Assert.Throws<ArgumentException>(() => CurrencyMinorUnits.For("XYZ"));
    }

    [Fact]
    public void Rounds_to_its_scale()
    {
        Assert.Equal(1.235m, Money.Round(1.2345m, "OMR", 3).Amount);
        Assert.Equal(1.24m, Money.Round(1.235m, "AED", 2).Amount);
        Assert.Equal(new Money(3.333m, "OMR", 3), new Money(10m, "OMR", 3).Multiply(1m / 3m));
    }

    [Theory]
    [InlineData(100, "AED", 2, "33.34,33.33,33.33")]
    [InlineData(10, "OMR", 3, "3.334,3.333,3.333")]
    [InlineData(-10, "OMR", 3, "-3.334,-3.333,-3.333")]
    public void Allocates_every_minor_unit(int amount, string currency, int scale, string expected)
    {
        var parts = new Money(amount, currency, scale).Allocate([1m, 1m, 1m]);

        Assert.Equal(expected, string.Join(",", parts.Select(p => p.ToAmountString())));
        Assert.Equal(amount, parts.Sum(p => p.Amount));
    }

    [Fact]
    public void Allocates_by_weight_with_the_remainder_to_the_largest_remainders()
    {
        var parts = new Money(0.05m, "AED", 2).Allocate([3m, 1m]);

        Assert.Equal(["0.04", "0.01"], parts.Select(p => p.ToAmountString()));
    }

    [Theory]
    [InlineData(12.75, "AED", 2, """{"amount":"12.75","currency":"AED","scale":2}""")]
    [InlineData(12.75, "OMR", 3, """{"amount":"12.750","currency":"OMR","scale":3}""")]
    [InlineData(1.235, "OMR", 3, """{"amount":"1.235","currency":"OMR","scale":3}""")]
    public void Goes_on_the_wire_as_a_decimal_string_with_currency_and_scale(double amount, string currency, int scale, string json)
    {
        var money = new Money((decimal)amount, currency, scale);

        Assert.Equal(json, JsonSerializer.Serialize(money));
        Assert.Equal(money, JsonSerializer.Deserialize<Money>(json));
    }

    [Theory]
    [InlineData("""{"amount":12.75,"currency":"AED","scale":2}""")]
    [InlineData("""{"amount":"12.75","currency":"AED"}""")]
    [InlineData("""{"amount":"12.755","currency":"AED","scale":2}""")]
    [InlineData("""{"amount":"1e3","currency":"AED","scale":2}""")]
    public void Refuses_a_wire_amount_the_contract_does_not_allow(string json)
    {
        Assert.Throws<JsonException>(() => JsonSerializer.Deserialize<Money>(json));
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
