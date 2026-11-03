using System.Security.Claims;
using System.Security.Cryptography;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.IdentityModel.JsonWebTokens;
using Microsoft.IdentityModel.Tokens;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.IntegrationTests;

/// <summary>
/// The API in process, serving two tenants of one cell (ADR-0038) at two hosts, verifying tokens
/// signed with the cell's one key. Neither tenant database is reachable: nothing here needs one.
/// </summary>
public sealed class TicvaiApiFactory : WebApplicationFactory<Program>
{
    public static readonly Guid TenantA = Guid.Parse("01920000-0000-7000-8000-00000000000a");
    public static readonly Guid TenantB = Guid.Parse("01920000-0000-7000-8000-00000000000b");
    public static readonly Guid PrincipalA = Guid.Parse("01920000-0000-7000-8000-0000000000a1");
    public const string HostA = "a.tenants.test";
    public const string HostB = "b.tenants.test";
    private const string Issuer = "https://identity.cell.test";
    private const string Audience = "staff";

    private readonly RSA _cellKey = RSA.Create(2048);

    /// <summary>The live sessions: sid-a in tenant A, sid-b in tenant B.</summary>
    public static readonly SessionRecord SessionA = new(
        "sid-a", TenantA, PrincipalA, null,
        new ResolvedAuthority([new Grant("ORDER_CREATE", "t_a.v_1", GrantEffect.Allow)], DateTimeOffset.UnixEpoch),
        ["t_a.v_1"]);

    public static readonly SessionRecord SessionB = SessionA with { SessionId = "sid-b", TenantId = TenantB, ScopePaths = ["t_b.v_1"] };

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");
        builder.ConfigureAppConfiguration((_, config) => config.AddInMemoryCollection(new Dictionary<string, string?>
        {
            ["Tenants:Entries:0:TenantId"] = TenantA.ToString(),
            ["Tenants:Entries:0:Hosts:0"] = HostA,
            ["Tenants:Entries:0:RootScopePath"] = "t_a",
            ["Tenants:Entries:0:ConnectionString"] = "Host=127.0.0.1;Port=1;Database=tenant_a;Username=nobody;Timeout=1",
            ["Tenants:Entries:1:TenantId"] = TenantB.ToString(),
            ["Tenants:Entries:1:Hosts:0"] = HostB,
            ["Tenants:Entries:1:RootScopePath"] = "t_b",
            ["Tenants:Entries:1:ConnectionString"] = "Host=127.0.0.1;Port=1;Database=tenant_b;Username=nobody;Timeout=1",
            ["Authentication:Issuer"] = Issuer,
            ["Authentication:Audiences:0"] = Audience,
            ["Authentication:Audiences:1"] = "cell",
            ["Authentication:SigningKeys:0:KeyId"] = "cell-2026",
            ["Authentication:SigningKeys:0:PublicKeyPem"] = _cellKey.ExportSubjectPublicKeyInfoPem(),
        }));
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<ISessionRegistry>();
            services.AddSingleton<ISessionRegistry>(new FixedSessions([SessionA, SessionB]));
            services.AddControllers().AddApplicationPart(typeof(ProbeController).Assembly);
        });
    }

    /// <summary>A staff token signed with the cell's key.</summary>
    public string StaffToken(Guid tenant, string sid) => Sign(new Dictionary<string, object>
    {
        ["tenant"] = tenant.ToString(),
        ["sid"] = sid,
        ["sub"] = PrincipalA.ToString(),
        ["aud"] = Audience,
    });

    private string Sign(Dictionary<string, object> claims) => new JsonWebTokenHandler().CreateToken(new SecurityTokenDescriptor
    {
        Issuer = Issuer,
        Claims = claims,
        Expires = DateTime.SpecifyKind(new DateTime(2099, 1, 1), DateTimeKind.Utc),
        SigningCredentials = new SigningCredentials(new RsaSecurityKey(_cellKey) { KeyId = "cell-2026" }, SecurityAlgorithms.RsaSha256),
    });

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            _cellKey.Dispose();
        }

        base.Dispose(disposing);
    }

    private sealed class FixedSessions(SessionRecord[] sessions) : ISessionRegistry
    {
        public ValueTask<SessionRecord?> FindAsync(string sessionId, CancellationToken cancellationToken) =>
            ValueTask.FromResult(sessions.FirstOrDefault(s => s.SessionId == sessionId));
    }
}
