using TICVAI.Api.Middleware;

namespace TICVAI.Api.Extensions;

public static class ApplicationBuilderExtensions
{
    public static WebApplication UseTicvaiPipeline(
        this WebApplication app)
    {
        app.UseMiddleware<ExceptionHandlingMiddleware>();

        app.UseHttpsRedirection();

        app.UseAuthorization();

        app.MapControllers();

        app.MapHealthChecks("/health");

        return app;
    }
}