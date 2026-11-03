using TICVAI.Api.Middleware;

namespace TICVAI.Api.Extensions;

public static class ApplicationBuilderExtensions
{
    /// <summary>
    /// The order matters: the host resolves the tenant before authentication, so a token is checked
    /// against the tenant it is presented to (r13 review C-05); the log context is pushed once the
    /// caller is known; authorisation runs last.
    /// </summary>
    public static WebApplication UseTicvaiPipeline(
        this WebApplication app)
    {
        app.UseMiddleware<ExceptionHandlingMiddleware>();

        app.UseHttpsRedirection();

        app.UseMiddleware<TenantResolutionMiddleware>();

        app.UseAuthentication();

        app.UseMiddleware<RequestLogContextMiddleware>();

        app.UseAuthorization();

        app.MapControllers();

        app.MapHealthChecks("/health");

        return app;
    }
}
