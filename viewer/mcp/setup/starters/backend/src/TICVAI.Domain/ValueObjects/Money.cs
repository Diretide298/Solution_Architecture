using System.Globalization;
using System.Text.Json.Serialization;

namespace TICVAI.Domain.ValueObjects;

/// <summary>
/// An amount in one currency at one scale: <c>{ amount, currency, scale }</c> at every layer
/// (ADR-0008). Never a bare decimal, and never a fixed 2 decimal places: AED has 2, OMR has 3.
/// </summary>
/// <remarks>
/// <para>
/// <b>The scale travels with the value.</b> A trading-currency amount takes the scale the venue's or
/// region's settings keep (<c>currency_scale</c>, ADR-0018); any other currency takes its ISO 4217
/// minor units from <see cref="CurrencyMinorUnits"/> (<see cref="InMinorUnits"/>). An amount with
/// more decimal places than its scale is refused, so a 3-dp AED or a 5-dp amount never reaches a
/// <c>numeric(18,4)</c> column.
/// </para>
/// <para>
/// <b>On the wire the amount is a decimal string</b> (<c>common.yaml</c> <c>Money</c>:
/// <c>{"amount":"1.235","currency":"OMR","scale":3}</c>), written by <see cref="MoneyJsonConverter"/>,
/// so no client rounds a fare in transit.
/// </para>
/// </remarks>
[JsonConverter(typeof(MoneyJsonConverter))]
public readonly record struct Money
{
    /// <summary>The largest scale the contract and the <c>numeric(18,4)</c> columns hold.</summary>
    public const int MaxScale = 4;

    public decimal Amount { get; }

    /// <summary>ISO 4217, upper case: AED, OMR.</summary>
    public string Currency { get; }

    /// <summary>The decimal places this amount is kept at: 0 to 4.</summary>
    public int Scale { get; }

    public Money(decimal amount, string currency, int scale)
    {
        if (currency is not { Length: 3 } || !currency.All(char.IsAsciiLetterUpper))
        {
            throw new ArgumentException($"'{currency}' is not an ISO 4217 code", nameof(currency));
        }

        if (scale is < 0 or > MaxScale)
        {
            throw new ArgumentOutOfRangeException(nameof(scale), scale, $"A money scale is 0 to {MaxScale}");
        }

        if (decimal.Round(amount, scale) != amount)
        {
            throw new ArgumentException($"{amount} has more than {scale} decimal places for {currency}", nameof(amount));
        }

        Amount = amount;
        Currency = currency;
        Scale = scale;
    }

    /// <summary>An amount in a currency that is not the venue's trading currency, at its ISO 4217 minor units.</summary>
    public static Money InMinorUnits(decimal amount, string currency) => new(amount, currency, CurrencyMinorUnits.For(currency));

    public static Money Zero(string currency, int scale) => new(0m, currency, scale);

    /// <summary>
    /// <paramref name="amount"/> rounded to <paramref name="scale"/> places. Half away from zero unless
    /// the rule you are implementing names another mode.
    /// </summary>
    public static Money Round(decimal amount, string currency, int scale, MidpointRounding mode = MidpointRounding.AwayFromZero)
    {
        if (scale is < 0 or > MaxScale)
        {
            throw new ArgumentOutOfRangeException(nameof(scale), scale, $"A money scale is 0 to {MaxScale}");
        }

        return new(Math.Round(amount, scale, mode), currency, scale);
    }

    public static Money operator +(Money left, Money right) => new(left.Amount + Same(left, right).Amount, left.Currency, left.Scale);

    public static Money operator -(Money left, Money right) => new(left.Amount - Same(left, right).Amount, left.Currency, left.Scale);

    /// <summary>The amount times <paramref name="factor"/>, rounded back to this scale.</summary>
    public Money Multiply(decimal factor, MidpointRounding mode = MidpointRounding.AwayFromZero) => Round(Amount * factor, Currency, Scale, mode);

    /// <summary>
    /// Splits the amount across <paramref name="weights"/> so the parts add up to it exactly (ADR-0008:
    /// allocation must distribute the remainder, or the ledger will not balance). Each part is floored to
    /// the scale; the minor units left over go one each to the parts with the largest remainders, the
    /// earlier part first on a tie.
    /// </summary>
    public IReadOnlyList<Money> Allocate(IReadOnlyList<decimal> weights)
    {
        ArgumentNullException.ThrowIfNull(weights);
        if (weights.Count == 0 || weights.Any(w => w < 0) || weights.Sum() <= 0)
        {
            throw new ArgumentException("Allocate needs at least one weight, none negative, and a positive total", nameof(weights));
        }

        var unit = 1m / Pow10(Scale);
        var total = weights.Sum();
        var sign = Amount < 0 ? -1m : 1m;
        var units = Math.Abs(Amount) / unit;
        var parts = new decimal[weights.Count];
        var remainders = new (decimal Remainder, int Index)[weights.Count];
        for (var i = 0; i < weights.Count; i++)
        {
            var exact = units * weights[i] / total;
            parts[i] = decimal.Floor(exact);
            remainders[i] = (exact - parts[i], i);
        }

        var left = (int)(units - parts.Sum());
        foreach (var (_, index) in remainders.OrderByDescending(r => r.Remainder).ThenBy(r => r.Index).Take(left))
        {
            parts[index] += 1;
        }

        var (currency, scale) = (Currency, Scale);
        return parts.Select(p => new Money(sign * p * unit, currency, scale)).ToList();
    }

    /// <summary>The wire form of the amount: a decimal string with exactly <see cref="Scale"/> places.</summary>
    public string ToAmountString() => Amount.ToString("F" + Scale.ToString(CultureInfo.InvariantCulture), CultureInfo.InvariantCulture);

    public override string ToString() => $"{ToAmountString()} {Currency}";

    private static decimal Pow10(int scale)
    {
        var result = 1m;
        for (var i = 0; i < scale; i++)
        {
            result *= 10m;
        }

        return result;
    }

    private static Money Same(Money left, Money right)
    {
        if (left.Currency != right.Currency)
        {
            throw new InvalidOperationException($"Cannot combine {left.Currency} and {right.Currency}");
        }

        if (left.Scale != right.Scale)
        {
            throw new InvalidOperationException($"Cannot combine {left.Currency} at scale {left.Scale} and {right.Scale}");
        }

        return right;
    }
}
