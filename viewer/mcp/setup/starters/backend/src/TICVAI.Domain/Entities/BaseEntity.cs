namespace TICVAI.Domain.Entities;

/// <summary>
/// Every entity has an id, and the caller decides what kind: a UUID v4 for configuration rows
/// (Guid.NewGuid() where the row is created) or the ULID an edge device created. The base class
/// does not mint one, so an entity loaded from the database or created offline keeps the id it
/// arrived with.
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
