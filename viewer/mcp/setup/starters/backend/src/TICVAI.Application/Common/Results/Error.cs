namespace TICVAI.Application.Common.Results;

/// <summary>
/// A failure the caller can act on. Code is the contract's problem code; Field names the input at
/// fault for a validation error.
/// </summary>
public sealed record Error(
    string Code,
    string Message,
    string? Field = null)
{
    public static readonly Error None = new(string.Empty, string.Empty);

    public static Error Validation(string field, string message) => new("validation", message, field);

    public static Error NotFound(string what) => new("not-found", $"{what} was not found");

    public static Error Conflict(string code, string message) => new(code, message);

    public static Error Forbidden(string permission) => new("forbidden", $"Requires {permission}");
}
