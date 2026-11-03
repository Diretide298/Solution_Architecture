using System.Collections.Frozen;

namespace TICVAI.Domain.ValueObjects;

/// <summary>
/// The ISO 4217 minor units of every active currency: the one fixed list the contract's
/// <c>Money.scale</c> names (ADAM CR-192, CHG-R10ORD-018), held beside <see cref="Money"/> so every
/// module resolves a scale the same way and no table, query or migration holds it.
/// </summary>
/// <remarks>
/// A venue's or region's <b>trading</b> currency takes the scale its settings keep
/// (<c>currency_scale</c>, ADR-0018). This list is for any other currency: a tourist's USD cash at an
/// AED till, a guest-selected charge currency, a refund in the tender currency.
/// </remarks>
public static class CurrencyMinorUnits
{
    private static readonly FrozenDictionary<string, int> Units = Build();

    /// <summary>The minor units of <paramref name="currency"/>: AED 2, OMR 3, JPY 0.</summary>
    /// <exception cref="ArgumentException">The code is not an active ISO 4217 currency.</exception>
    public static int For(string currency) =>
        currency is not null && Units.TryGetValue(currency, out var units)
            ? units
            : throw new ArgumentException($"'{currency}' is not an active ISO 4217 currency", nameof(currency));

    /// <summary>True when <paramref name="currency"/> is on the list.</summary>
    public static bool IsKnown(string currency) => currency is not null && Units.ContainsKey(currency);

    private static FrozenDictionary<string, int> Build()
    {
        // Every active code not named below has 2 minor units.
        const string twoDecimals =
            "AED AFN ALL AMD AOA ARS AUD AWG AZN BAM BBD BDT BGN BMD BND BOB BOV BRL BSD BTN BWP BYN BZD " +
            "CAD CDF CHE CHF CHW CNY COP COU CRC CUP CVE CZK DKK DOP DZD EGP ERN ETB EUR FJD FKP GBP GEL " +
            "GHS GIP GMD GTQ GYD HKD HNL HTG HUF IDR ILS INR IRR JMD KES KGS KHR KPW KYD KZT LAK LBP LKR " +
            "LRD LSL MAD MDL MGA MKD MMK MNT MOP MRU MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR NZD " +
            "PAB PEN PGK PHP PKR PLN QAR RON RSD RUB SAR SBD SCR SDG SEK SGD SHP SLE SOS SRD SSP STN SVC " +
            "SYP SZL THB TJS TMT TOP TRY TTD TWD TZS UAH USD USN UYU UZS VED VES WST XCD XCG YER ZAR ZMW ZWG";
        const string zeroDecimals = "BIF CLP DJF GNF ISK JPY KMF KRW PYG RWF UGX UYI VND VUV XAF XOF XPF";
        const string threeDecimals = "BHD IQD JOD KWD LYD OMR TND";
        const string fourDecimals = "CLF UYW";

        var units = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var (codes, scale) in new[] { (twoDecimals, 2), (zeroDecimals, 0), (threeDecimals, 3), (fourDecimals, 4) })
        {
            foreach (var code in codes.Split(' ', StringSplitOptions.RemoveEmptyEntries))
            {
                units.Add(code, scale);
            }
        }

        return units.ToFrozenDictionary(StringComparer.Ordinal);
    }
}
