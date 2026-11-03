using System.Security.Claims;
using Npgsql;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Persistence;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.UnitTests.Security;

/// <summary>The token's tenant is the request's tenant (r13 review C-05), and the context row security reads.</summary>
public class TenantBindingTests
{
    private static readonly Guid TenantA = Guid.Parse("01920000-0000-7000-8000-00000000000a");
    private static readonly Guid TenantB = Guid.Parse("01920000-0000-7000-8000-00000000000b");
    private static readonly Guid Principal = Guid.Parse("01920000-0000-7000-8000-0000000000c1");

    [Fact]
    public async Task A_token_of_the_host_tenant_with_its_live_session_binds_the_session_scope()
    {
        var (tenant, principal) = AtHostOf(TenantA);

        var refused = await TenantBinding.BindAsync(Token(TenantA, "sid-1"), tenant, principal, Sessions(Session("sid-1", TenantA)), default);

        Assert.Null(refused);
        Assert.Equal(["t_a.v_1"], tenant.ScopePaths);
        Assert.Equal(Principal, tenant.PrincipalId);
        Assert.True(principal.IsAuthenticated);
        Assert.True(((ICurrentPrincipal)principal).Permits("ORDER_CREATE", "t_a.v_1"));
    }

    [Fact]
    public async Task A_token_naming_another_tenant_is_refused_and_binds_nothing()
    {
        var (tenant, principal) = AtHostOf(TenantA);

        var refused = await TenantBinding.BindAsync(Token(TenantB, "sid-1"), tenant, principal, Sessions(Session("sid-1", TenantB)), default);

        Assert.NotNull(refused);
        Assert.Empty(tenant.ScopePaths);
        Assert.False(principal.IsAuthenticated);
        Assert.False(((ICurrentPrincipal)principal).Permits("ORDER_CREATE", "t_a.v_1"));
    }

    [Fact]
    public async Task A_session_opened_for_another_tenant_is_refused()
    {
        var (tenant, principal) = AtHostOf(TenantA);

        var refused = await TenantBinding.BindAsync(Token(TenantA, "sid-1"), tenant, principal, Sessions(Session("sid-1", TenantB)), default);

        Assert.NotNull(refused);
        Assert.False(principal.IsAuthenticated);
    }

    [Fact]
    public async Task A_token_with_no_live_session_is_refused()
    {
        var (tenant, principal) = AtHostOf(TenantA);

        Assert.NotNull(await TenantBinding.BindAsync(Token(TenantA, "sid-gone"), tenant, principal, new NoSessionRegistry(), default));
        Assert.NotNull(await TenantBinding.BindAsync(Token(TenantA, sid: null), tenant, principal, Sessions(Session("sid-1", TenantA)), default));
    }

    [Fact]
    public async Task A_service_token_takes_its_tenant_from_tid_and_runs_at_the_tenant_root()
    {
        var (tenant, principal) = AtHostOf(TenantA);
        var service = new ClaimsPrincipal(new ClaimsIdentity([new Claim("aud", "cell"), new Claim("tid", TenantA.ToString()), new Claim("sub", "cell-ref-north")], "Bearer"));

        Assert.Null(await TenantBinding.BindAsync(service, tenant, principal, new NoSessionRegistry(), default));
        Assert.Equal(["t_a"], tenant.ScopePaths);
        Assert.Null(tenant.PrincipalId);
    }

    [Fact]
    public async Task A_service_token_for_another_tenant_is_refused()
    {
        var (tenant, principal) = AtHostOf(TenantA);
        var service = new ClaimsPrincipal(new ClaimsIdentity([new Claim("aud", "cell"), new Claim("tid", TenantB.ToString())], "Bearer"));

        Assert.NotNull(await TenantBinding.BindAsync(service, tenant, principal, new NoSessionRegistry(), default));
    }

    [Fact]
    public void Every_transaction_sets_the_three_settings_transaction_locally()
    {
        var (tenant, _) = AtHostOf(TenantA);
        tenant.Bind(["t_a.v_1", "t_a.v_2"], Principal, subjectId: null);

        using var connection = new NpgsqlConnection();
        using var command = ScopeContextInterceptor.Build(connection, null!, tenant);

        // set_config(name, value, true) is SET LOCAL: it ends with the transaction (backend/MIGRATIONS.md).
        Assert.Equal(3, System.Text.RegularExpressions.Regex.Matches(command.CommandText, @"set_config\('ticvai\.\w+', @\w+, true\)").Count);
        Assert.Contains("ticvai.scope_paths", command.CommandText);
        Assert.Contains("ticvai.subject_id", command.CommandText);
        Assert.Contains("ticvai.principal_id", command.CommandText);
        Assert.DoesNotContain(", false)", command.CommandText);
        Assert.Equal("t_a.v_1,t_a.v_2", command.Parameters["scope_paths"].Value);
        Assert.Equal(Principal.ToString(), command.Parameters["principal_id"].Value);
        Assert.Equal(string.Empty, command.Parameters["subject_id"].Value);
    }

    [Fact]
    public void An_unbound_request_sets_an_empty_scope_so_row_security_shows_nothing()
    {
        var (tenant, _) = AtHostOf(TenantA);

        Assert.Equal(string.Empty, ScopeContextInterceptor.Values(tenant).Single(v => v.Name == "scope_paths").Value);
    }

    private static (RequestTenantContext Tenant, RequestPrincipal Principal) AtHostOf(Guid tenantId)
    {
        var tenant = new RequestTenantContext();
        tenant.Resolve(new TenantRoute(tenantId, tenantId == TenantA ? "t_a" : "t_b"));
        return (tenant, new RequestPrincipal());
    }

    private static ClaimsPrincipal Token(Guid tenantId, string? sid)
    {
        var claims = new List<Claim> { new("aud", "staff"), new("tenant", tenantId.ToString()), new("sub", Principal.ToString()) };
        if (sid is not null)
        {
            claims.Add(new Claim("sid", sid));
        }

        return new ClaimsPrincipal(new ClaimsIdentity(claims, "Bearer"));
    }

    private static SessionRecord Session(string sid, Guid tenantId) => new(
        sid, tenantId, Principal, null,
        new ResolvedAuthority([new Grant("ORDER_CREATE", "t_a.v_1", GrantEffect.Allow)], DateTimeOffset.UnixEpoch),
        ["t_a.v_1"]);

    private static ISessionRegistry Sessions(params SessionRecord[] sessions) => new FixedSessions(sessions);

    private sealed class FixedSessions(SessionRecord[] sessions) : ISessionRegistry
    {
        public ValueTask<SessionRecord?> FindAsync(string sessionId, CancellationToken cancellationToken) =>
            ValueTask.FromResult(sessions.FirstOrDefault(s => s.SessionId == sessionId));
    }
}
