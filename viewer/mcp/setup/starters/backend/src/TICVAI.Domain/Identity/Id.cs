namespace TICVAI.Domain.Identity;

/// <summary>
/// The one id type (ADR-0056, 30 Sep 2026): every id is a <see cref="Guid"/>, stored as
/// PostgreSQL <c>uuid</c> and typed <c>format: uuid</c> in the contracts. Every new one is a
/// UUIDv7 minted here.
/// </summary>
/// <remarks>
/// <para>
/// UUIDv7 puts a 48-bit Unix-millisecond timestamp in front of the random bits, so keys arrive
/// in roughly insertion order and an index stays compact without a central allocator. Offline
/// devices mint the same format before the server has seen the record (<c>newId()</c> in
/// <c>offline-core</c>), and that id doubles as the <c>Idempotency-Key</c>.
/// </para>
/// <para>
/// PostgreSQL stays on 16, so no id is generated in SQL: the application mints every one
/// through <see cref="New()"/>. Human codes a person reads or types (order numbers, ticket
/// codes) are not ids; they are separate text columns.
/// </para>
/// <para>
/// Inside a type that has its own <c>Id</c> property (every <c>BaseEntity</c>), the property wins
/// name lookup; write <c>Identity.Id.New()</c> there.
/// </para>
/// </remarks>
public static class Id
{
    /// <summary>A new UUIDv7 for the current instant.</summary>
    public static Guid New() => Guid.CreateVersion7();

    /// <summary>A new UUIDv7 for <paramref name="timestamp"/>. For tests and replays only.</summary>
    public static Guid New(DateTimeOffset timestamp) => Guid.CreateVersion7(timestamp);

    /// <summary>
    /// True when <paramref name="value"/> is a UUIDv7 (version 7, RFC 9562 variant). An id from
    /// elsewhere may be another version and is still a valid id: validate an incoming id as a
    /// uuid, and use this only where a newly minted one is required.
    /// </summary>
    public static bool IsVersion7(Guid value) => value.Version == 7 && (value.Variant & 0xC) == 0x8;

    /// <summary>
    /// The millisecond a UUIDv7 was minted for. For tests and support triage; application logic
    /// keeps its own timestamps and treats ids as opaque.
    /// </summary>
    public static DateTimeOffset TimeOf(Guid value)
    {
        if (!IsVersion7(value))
        {
            throw new ArgumentException($"'{value}' is not a UUIDv7", nameof(value));
        }

        Span<byte> bytes = stackalloc byte[16];
        value.TryWriteBytes(bytes, bigEndian: true, out _);
        long ms = 0;
        foreach (var b in bytes[..6])
        {
            ms = (ms << 8) | b;
        }

        return DateTimeOffset.FromUnixTimeMilliseconds(ms);
    }
}
