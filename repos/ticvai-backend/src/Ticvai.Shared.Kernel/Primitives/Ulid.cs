using System.Security.Cryptography;

namespace Ticvai.Shared.Kernel.Primitives;

/// <summary>
/// Lexicographically sortable 128-bit identifier: 48-bit timestamp + 80-bit randomness,
/// Crockford base32 encoded.
/// </summary>
/// <remarks>
/// Used as the primary key on high-volume tables instead of <c>bigserial</c>. Two
/// reasons: a shared sequence is a contention point on a partitioned table, and
/// offline clients must generate identifiers locally before they ever reach the
/// server (31 Jul 2026 offline architecture). Time-ordering preserves index
/// locality without a central allocator.
/// </remarks>
public static class UlidGenerator
{
    private const string Alphabet = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

    public static string NewUlid() => NewUlid(DateTimeOffset.UtcNow);

    public static string NewUlid(DateTimeOffset timestamp)
    {
        Span<byte> bytes = stackalloc byte[16];

        var ms = timestamp.ToUnixTimeMilliseconds();
        for (var i = 5; i >= 0; i--)
        {
            bytes[i] = (byte)(ms & 0xFF);
            ms >>= 8;
        }

        RandomNumberGenerator.Fill(bytes[6..]);
        return Encode(bytes);
    }

    public static bool IsValid(string value)
    {
        if (string.IsNullOrEmpty(value) || value.Length != 26) return false;
        foreach (var c in value)
        {
            if (Alphabet.IndexOf(c) < 0) return false;
        }
        return true;
    }

    private static string Encode(ReadOnlySpan<byte> bytes)
    {
        Span<char> chars = stackalloc char[26];
        var bitBuffer = 0;
        var bitCount = 0;
        var index = 0;

        foreach (var b in bytes)
        {
            bitBuffer = (bitBuffer << 8) | b;
            bitCount += 8;

            while (bitCount >= 5)
            {
                bitCount -= 5;
                chars[index++] = Alphabet[(bitBuffer >> bitCount) & 0x1F];
            }
        }

        if (bitCount > 0)
        {
            chars[index] = Alphabet[(bitBuffer << (5 - bitCount)) & 0x1F];
        }

        return new string(chars);
    }
}
