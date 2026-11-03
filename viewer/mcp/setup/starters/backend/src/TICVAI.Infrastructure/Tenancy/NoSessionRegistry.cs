using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// The registry before sign-in builds the real one: it knows no session, so every staff and guest
/// token is refused (fail closed). Replace the registration, not the interface.
/// </summary>
public sealed class NoSessionRegistry : ISessionRegistry
{
    public ValueTask<SessionRecord?> FindAsync(string sessionId, CancellationToken cancellationToken) =>
        ValueTask.FromResult<SessionRecord?>(null);
}
