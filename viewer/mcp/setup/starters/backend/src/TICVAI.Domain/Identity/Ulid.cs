using System.Security.Cryptography;

namespace TICVAI.Domain.Identity;

/// <summary>
/// ULIDs for ids created at the edge (a device, an offline write): 26 Crockford base32
/// characters, time-ordered, matching the contracts' pattern ^[0-9A-HJKMNP-TV-Z]{26}$.
/// Configuration rows keep UUID v4 (naming-and-style 4); this is only for edge-created ids.
/// </summary>
public static class Ulid
{
    private const string Alphabet = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

    public static string New(DateTimeOffset? at = null)
    {
        var time = (ulong)(at ?? DateTimeOffset.UtcNow).ToUnixTimeMilliseconds();
        Span<byte> bytes = stackalloc byte[16];
        for (var i = 5; i >= 0; i--)
        {
            bytes[i] = (byte)(time & 0xFF);
            time >>= 8;
        }

        RandomNumberGenerator.Fill(bytes[6..]);
        return Encode(bytes);
    }

    public static bool IsValid(string? value) =>
        value is { Length: 26 } && value[0] <= '7' && value.All(c => Alphabet.Contains(c));

    /// <summary>The creation time a ULID carries in its first 10 characters.</summary>
    public static DateTimeOffset TimeOf(string ulid)
    {
        if (!IsValid(ulid))
        {
            throw new ArgumentException($"'{ulid}' is not a ULID", nameof(ulid));
        }

        ulong ms = 0;
        foreach (var c in ulid[..10])
        {
            ms = (ms << 5) | (uint)Alphabet.IndexOf(c);
        }

        return DateTimeOffset.FromUnixTimeMilliseconds((long)ms);
    }

    private static string Encode(ReadOnlySpan<byte> bytes)
    {
        var value = new UInt128(
            System.Buffers.Binary.BinaryPrimitives.ReadUInt64BigEndian(bytes[..8]),
            System.Buffers.Binary.BinaryPrimitives.ReadUInt64BigEndian(bytes[8..]));
        Span<char> chars = stackalloc char[26];
        for (var i = 25; i >= 0; i--)
        {
            chars[i] = Alphabet[(int)(value & 31)];
            value >>= 5;
        }

        return new string(chars);
    }
}
