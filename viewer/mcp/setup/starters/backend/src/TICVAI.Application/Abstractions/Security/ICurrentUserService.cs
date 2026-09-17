namespace TICVAI.Application.Abstractions.Security;

/// <summary>The person making the current request.</summary>
public interface ICurrentUserService
{
    string? UserId { get; }

    bool IsAuthenticated { get; }
}
