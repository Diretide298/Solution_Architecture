namespace TICVAI.Domain.ValueObjects;

/// <summary>
/// An amount in one currency. Never a bare decimal: the package stores money as an amount plus
/// an ISO 4217 code, and a sum across currencies is a bug, not a conversion.
/// </summary>
public readonly record struct Money
{
    public decimal Amount { get; }

    /// <summary>ISO 4217, upper case: AED, OMR.</summary>
    public string Currency { get; }

    public Money(decimal amount, string currency)
    {
        if (currency is not { Length: 3 } || !currency.All(char.IsAsciiLetterUpper))
        {
            throw new ArgumentException($"'{currency}' is not an ISO 4217 code", nameof(currency));
        }

        Amount = amount;
        Currency = currency;
    }

    public static Money Zero(string currency) => new(0m, currency);

    public static Money operator +(Money left, Money right) => new(left.Amount + SameCurrency(left, right).Amount, left.Currency);

    public static Money operator -(Money left, Money right) => new(left.Amount - SameCurrency(left, right).Amount, left.Currency);

    public Money Multiply(decimal factor) => new(Amount * factor, Currency);

    /// <summary>Rounded to the currency's minor units (AED 2, OMR 3), half away from zero.</summary>
    public Money Round(int minorUnits) => new(Math.Round(Amount, minorUnits, MidpointRounding.AwayFromZero), Currency);

    private static Money SameCurrency(Money left, Money right) => left.Currency == right.Currency
        ? right
        : throw new InvalidOperationException($"Cannot combine {left.Currency} and {right.Currency}");

    public override string ToString() => $"{Amount} {Currency}";
}
