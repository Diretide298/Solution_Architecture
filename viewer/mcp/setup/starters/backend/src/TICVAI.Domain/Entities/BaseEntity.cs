namespace TICVAI.Domain.Entities;

/// <summary>
/// Every entity has an id: a uuid (ADR-0056). A new one is a UUIDv7, minted by the caller with
/// <c>Identity.Id.New()</c> where the row is created on the server, or by the device that created
/// it offline. The base class does not mint one, so an entity loaded from the database or created
/// offline keeps the id it arrived with.
/// </summary>
public abstract class BaseEntity<TId>
    where TId : notnull
{
    public TId Id { get; protected set; }

    protected BaseEntity(TId id)
    {
        Id = id;
    }
}
