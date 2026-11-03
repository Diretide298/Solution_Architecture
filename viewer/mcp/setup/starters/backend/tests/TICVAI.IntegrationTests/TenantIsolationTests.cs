using System.Net;
using System.Net.Http.Headers;
using System.Text.Json;

namespace TICVAI.IntegrationTests;

/// <summary>
/// Through the real pipeline: the host picks the tenant (ADR-0038, <c>resolveTenantHost</c>), and a
/// token is accepted only by the tenant it names, with a session of that tenant (r13 review C-05).
/// </summary>
public class TenantIsolationTests(TicvaiApiFactory factory) : IClassFixture<TicvaiApiFactory>
{
    [Fact]
    public async Task A_token_at_its_own_tenants_host_gets_its_session_scope()
    {
        var response = await Send(TicvaiApiFactory.HostA, factory.StaffToken(TicvaiApiFactory.TenantA, "sid-a"));

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        using var body = JsonDocument.Parse(await response.Content.ReadAsStringAsync());
        Assert.Equal(TicvaiApiFactory.TenantA, body.RootElement.GetProperty("tenantId").GetGuid());
        Assert.Equal("t_a.v_1", body.RootElement.GetProperty("scopePaths")[0].GetString());
        Assert.True(body.RootElement.GetProperty("mayCreateOrderAtVenue1").GetBoolean());
    }

    [Fact]
    public async Task A_token_of_another_tenant_in_the_same_cell_is_refused()
    {
        var response = await Send(TicvaiApiFactory.HostA, factory.StaffToken(TicvaiApiFactory.TenantB, "sid-b"));

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task A_tenant_header_does_not_choose_the_tenant()
    {
        var response = await Send(TicvaiApiFactory.HostA, factory.StaffToken(TicvaiApiFactory.TenantB, "sid-b"),
            ("X-Ticvai-Tenant", TicvaiApiFactory.TenantB.ToString()), ("X-Tenant-Id", TicvaiApiFactory.TenantB.ToString()));

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task A_token_naming_this_tenant_with_another_tenants_session_is_refused()
    {
        var response = await Send(TicvaiApiFactory.HostA, factory.StaffToken(TicvaiApiFactory.TenantA, "sid-b"));

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task A_request_without_a_token_is_refused()
    {
        var response = await Send(TicvaiApiFactory.HostA, token: null);

        Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
    }

    [Fact]
    public async Task A_host_this_cell_serves_no_tenant_at_is_not_found()
    {
        var response = await Send("unknown.tenants.test", factory.StaffToken(TicvaiApiFactory.TenantA, "sid-a"));

        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }

    [Fact]
    public async Task Health_is_unhealthy_when_a_tenant_database_does_not_answer()
    {
        var response = await factory.CreateClient().GetAsync(new Uri("/health", UriKind.Relative));

        Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode);
    }

    private async Task<HttpResponseMessage> Send(string host, string? token, params (string Name, string Value)[] headers)
    {
        using var request = new HttpRequestMessage(HttpMethod.Get, new Uri("/probe", UriKind.Relative));
        request.Headers.Host = host;
        if (token is not null)
        {
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        }

        foreach (var (name, value) in headers)
        {
            request.Headers.Add(name, value);
        }

        return await factory.CreateClient().SendAsync(request);
    }
}
