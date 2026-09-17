using TICVAI.Application.Common.Results;

namespace TICVAI.UnitTests.Common;

public class ResultTests
{
    [Fact]
    public void Success_has_no_error()
    {
        var result = Result<int>.Success(42);

        Assert.True(result.IsSuccess);
        Assert.Equal(42, result.Value);
        Assert.Equal(Error.None, result.Error);
    }

    [Fact]
    public void Failure_hides_the_value()
    {
        var result = Result<int>.Failure(new Error("thing.not_found", "No such thing"));

        Assert.True(result.IsFailure);
        Assert.Throws<InvalidOperationException>(() => result.Value);
    }
}
