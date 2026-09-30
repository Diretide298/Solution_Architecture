namespace Ticvai.Shared.Kernel.Primitives;

/// <summary>
/// The one id type (ADR-0056, 30 Sep 2026): every id is a <see cref="Guid"/> stored as
/// PostgreSQL <c>uuid</c>, and every new one is a UUIDv7 minted here.
/// </summary>
/// <remarks>
/// <para>
/// UUIDv7 puts a 48-bit Unix-millisecond timestamp in front of the random bits, so keys arrive
/// in roughly insertion order and a b-tree index stays compact without a central allocator. A
/// shared sequence would be a contention point on a partitioned table, and offline clients must
/// generate ids before the server has seen the record (31 Jul 2026 offline architecture); the
/// frontend's <c>offline-core</c> mints the same format with the <c>uuid</c> package's <c>v7</c>,
/// and that id doubles as the <c>Idempotency-Key</c>.
/// </para>
/// <para>
/// PostgreSQL stays on 16, so ids are never generated in SQL (<c>uuidv7()</c> arrives in 18):
/// the application mints every one through <see cref="New()"/>. Ids are opaque; nothing reads a
/// time out of one. Human codes a person reads or types (order numbers, ticket and card codes)
/// are not ids and stay text.
/// </para>
/// <para>
/// Inside a type that has its own <c>Id</c> property, the property wins name lookup; write
/// <c>Primitives.Id.New()</c> there.
/// </para>
/// </remarks>
public static class Id
{
    /// <summary>A new UUIDv7 for the current instant.</summary>
    public static Guid New() => Guid.CreateVersion7();

    /// <summary>A new UUIDv7 for <paramref name="timestamp"/>. For tests and replays only.</summary>
    public static Guid New(DateTimeOffset timestamp) => Guid.CreateVersion7(timestamp);

    /// <summary>
    /// True when <paramref name="value"/> is a UUIDv7 (version 7, RFC 9562 variant). Ids migrated
    /// from before ADR-0056 may be other versions and are still valid ids: validate an incoming id
    /// as a uuid, and use this only where a new one is required.
    /// </summary>
    public static bool IsVersion7(Guid value) => value.Version == 7 && (value.Variant & 0xC) == 0x8;
}
