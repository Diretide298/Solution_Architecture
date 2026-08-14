namespace Ticvai.Shared.Kernel.Primitives;

public sealed record Error(string Code, string Message, string? Field = null)
{
    public static Error NotFound(string what) => new("not_found", $"{what} was not found.");
    public static Error Conflict(string message) => new("conflict", message);
    public static Error Validation(string field, string message) => new("validation", message, field);
    public static Error Forbidden(string message) => new("forbidden", message);
}

/// <summary>Explicit success/failure without exceptions for expected failure modes.</summary>
public readonly record struct Result<T>
{
    private readonly T? _value;

    private Result(T value)
    {
        _value = value;
        Errors = [];
        IsSuccess = true;
    }

    private Result(IReadOnlyList<Error> errors)
    {
        _value = default;
        Errors = errors;
        IsSuccess = false;
    }

    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public IReadOnlyList<Error> Errors { get; }

    public T Value => IsSuccess
        ? _value!
        : throw new InvalidOperationException($"Result is a failure: {string.Join("; ", Errors.Select(e => e.Code))}");

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(params Error[] errors) => new(errors);

    public TOut Match<TOut>(Func<T, TOut> onSuccess, Func<IReadOnlyList<Error>, TOut> onFailure) =>
        IsSuccess ? onSuccess(_value!) : onFailure(Errors);
}
