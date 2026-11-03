using System.Security.Cryptography;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.Api.Security;

/// <summary>
/// Bearer tokens, verified and then <b>bound to the request's tenant</b> (<see cref="TenantBinding"/>,
/// r13 review C-05): the signature proves the cell; the tenant claim and the session must name the
/// tenant the host resolved to, or the request is <c>401</c> before anything else runs.
/// </summary>
public static class AuthenticationSetup
{
    public static IServiceCollection AddTicvaiAuthentication(this IServiceCollection services, IConfiguration configuration)
    {
        services.Configure<TokenOptions>(configuration.GetSection(TokenOptions.SectionName));
        services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer();
        services.AddOptions<JwtBearerOptions>(JwtBearerDefaults.AuthenticationScheme)
            .Configure<IOptions<TokenOptions>>((jwt, tokens) =>
            {
                var keys = tokens.Value.SigningKeys.Select(ToKey).ToList();
                jwt.MapInboundClaims = false;
                jwt.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuer = true,
                    ValidIssuer = tokens.Value.Issuer,
                    ValidateAudience = true,
                    ValidAudiences = tokens.Value.Audiences,
                    ValidateLifetime = true,
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKeys = keys,
                    ValidAlgorithms = [SecurityAlgorithms.RsaSha256],
                    ClockSkew = TimeSpan.FromSeconds(30),
                };
                jwt.Events = new JwtBearerEvents
                {
                    OnTokenValidated = async context =>
                    {
                        var services = context.HttpContext.RequestServices;
                        var refused = await TenantBinding.BindAsync(
                            context.Principal!,
                            services.GetRequiredService<RequestTenantContext>(),
                            services.GetRequiredService<RequestPrincipal>(),
                            services.GetRequiredService<ISessionRegistry>(),
                            context.HttpContext.RequestAborted);
                        if (refused is not null)
                        {
                            context.Fail(refused);
                        }
                    },
                };
            });
        services.AddAuthorization();
        return services;
    }

    private static RsaSecurityKey ToKey(SigningKey key)
    {
        var rsa = RSA.Create();
        rsa.ImportFromPem(key.PublicKeyPem);
        return new RsaSecurityKey(rsa) { KeyId = key.KeyId };
    }
}
