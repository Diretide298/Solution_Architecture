using System.Globalization;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

namespace TICVAI.Domain.ValueObjects;

/// <summary>
/// The contract's wire shape of <see cref="Money"/> (<c>common.yaml</c> <c>Money</c>, ADR-0008):
/// <c>{"amount":"12.750","currency":"OMR","scale":3}</c>. The amount is a decimal string matching
/// <c>^-?\d+(\.\d{1,4})?$</c>, never a JSON number; all three fields are required.
/// </summary>
public sealed partial class MoneyJsonConverter : JsonConverter<Money>
{
    [GeneratedRegex(@"^-?\d+(\.\d{1,4})?$", RegexOptions.CultureInvariant)]
    private static partial Regex AmountPattern();

    public override Money Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        if (reader.TokenType != JsonTokenType.StartObject)
        {
            throw new JsonException("Money is an object { amount, currency, scale }");
        }

        string? amount = null, currency = null;
        int? scale = null;
        while (reader.Read() && reader.TokenType != JsonTokenType.EndObject)
        {
            var name = reader.GetString();
            reader.Read();
            switch (name)
            {
                case "amount" when reader.TokenType == JsonTokenType.String:
                    amount = reader.GetString();
                    break;
                case "amount":
                    throw new JsonException("Money.amount is a decimal string, never a number");
                case "currency":
                    currency = reader.GetString();
                    break;
                case "scale":
                    scale = reader.GetInt32();
                    break;
                default:
                    reader.Skip();
                    break;
            }
        }

        if (amount is null || currency is null || scale is null)
        {
            throw new JsonException("Money needs amount, currency and scale");
        }

        if (!AmountPattern().IsMatch(amount))
        {
            throw new JsonException($"'{amount}' is not a Money amount");
        }

        try
        {
            return new Money(decimal.Parse(amount, NumberStyles.AllowLeadingSign | NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture), currency, scale.Value);
        }
        catch (ArgumentException exception)
        {
            throw new JsonException(exception.Message, exception);
        }
    }

    public override void Write(Utf8JsonWriter writer, Money value, JsonSerializerOptions options)
    {
        writer.WriteStartObject();
        writer.WriteString("amount", value.ToAmountString());
        writer.WriteString("currency", value.Currency);
        writer.WriteNumber("scale", value.Scale);
        writer.WriteEndObject();
    }
}
