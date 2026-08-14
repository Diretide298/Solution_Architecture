using System.Globalization;

namespace Ticvai.Shared.Kernel.Primitives;

/// <summary>
/// A monetary amount with an explicit currency and scale.
/// </summary>
/// <remarks>
/// Scale is carried per instance because it varies by region: OMR uses three
/// decimal places, AED uses two. A fixed two-place money type silently truncates
/// every Omani transaction. The ledger is append-only (12 Aug 2026), so
/// corrections are new entries rather than edits — this must be correct before
/// any data lands.
/// </remarks>
public readonly record struct Money : IComparable<Money>
{
    public const int MaxScale = 4;

    public decimal Amount { get; }
    public string Currency { get; }
    public int Scale { get; }

    public Money(decimal amount, string currency, int scale)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(currency);

        if (currency.Length != 3 || !currency.All(char.IsAsciiLetterUpper))
        {
            throw new ArgumentException(
                $"Currency must be a 3-letter ISO 4217 code, got '{currency}'.", nameof(currency));
        }

        if (scale is < 0 or > MaxScale)
        {
            throw new ArgumentOutOfRangeException(
                nameof(scale), scale, $"Scale must be between 0 and {MaxScale}.");
        }

        Currency = currency;
        Scale = scale;
        Amount = decimal.Round(amount, scale, MidpointRounding.ToEven);
    }

    public static Money Zero(string currency, int scale) => new(0m, currency, scale);

    public Money Add(Money other)
    {
        AssertCompatible(other);
        return new Money(Amount + other.Amount, Currency, Scale);
    }

    public Money Subtract(Money other)
    {
        AssertCompatible(other);
        return new Money(Amount - other.Amount, Currency, Scale);
    }

    public Money Multiply(decimal factor) => new(Amount * factor, Currency, Scale);

    public Money Negate() => new(-Amount, Currency, Scale);

    public bool IsZero => Amount == 0m;

    public bool IsNegative => Amount < 0m;

    /// <summary>
    /// Splits an amount across weights without losing minor units. Any remainder
    /// is distributed one unit at a time, largest weight first.
    /// </summary>
    /// <remarks>
    /// Required by the revenue allocation split builder (12 Aug 2026 §16), where a
    /// combo or multi-venue pass price is divided across products or legal entities
    /// by percentage or fixed amount. Naive proportional division loses fractions of
    /// a minor unit and the ledger will not balance.
    /// </remarks>
    public IReadOnlyList<Money> Allocate(IReadOnlyList<decimal> weights)
    {
        ArgumentNullException.ThrowIfNull(weights);

        if (weights.Count == 0)
            throw new ArgumentException("At least one weight is required.", nameof(weights));

        if (weights.Any(static w => w < 0))
            throw new ArgumentException("Weights must be non-negative.", nameof(weights));

        var totalWeight = weights.Sum();
        if (totalWeight == 0m)
            throw new ArgumentException("Weights must not sum to zero.", nameof(weights));

        var unit = Pow10Negative(Scale);
        var totalUnits = (long)decimal.Round(Amount / unit, 0, MidpointRounding.ToEven);

        var allocated = new long[weights.Count];
        long assigned = 0;

        for (var i = 0; i < weights.Count; i++)
        {
            allocated[i] = (long)Math.Floor(totalUnits * weights[i] / totalWeight);
            assigned += allocated[i];
        }

        var remainder = totalUnits - assigned;
        var step = Math.Sign(remainder);

        var order = Enumerable.Range(0, weights.Count)
            .OrderByDescending(i => weights[i])
            .ToArray();

        for (var n = 0; n < Math.Abs(remainder); n++)
        {
            allocated[order[n % order.Length]] += step;
        }

        return allocated.Select(u => new Money(u * unit, Currency, Scale)).ToList();
    }

    public int CompareTo(Money other)
    {
        AssertCompatible(other);
        return Amount.CompareTo(other.Amount);
    }

    /// <summary>Wire format: a decimal string, never a float.</summary>
    public string ToWireString() => Amount.ToString($"F{Scale}", CultureInfo.InvariantCulture);

    public override string ToString() => $"{ToWireString()} {Currency}";

    private static decimal Pow10Negative(int scale) => scale switch
    {
        0 => 1m,
        1 => 0.1m,
        2 => 0.01m,
        3 => 0.001m,
        4 => 0.0001m,
        _ => throw new ArgumentOutOfRangeException(nameof(scale))
    };

    private void AssertCompatible(Money other)
    {
        if (!string.Equals(Currency, other.Currency, StringComparison.Ordinal))
        {
            throw new InvalidOperationException(
                $"Currency mismatch: {Currency} vs {other.Currency}. Convert explicitly — " +
                "transactions settle and record in the venue's base currency (10 Aug 2026).");
        }

        if (Scale != other.Scale)
        {
            throw new InvalidOperationException(
                $"Scale mismatch for {Currency}: {Scale} vs {other.Scale}.");
        }
    }
}
