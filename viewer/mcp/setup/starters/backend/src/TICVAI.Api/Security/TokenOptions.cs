namespace TICVAI.Api.Security;

/// <summary>
/// How this cell verifies tokens, bound from <c>Authentication</c>: RS256 with one key per cell, the
/// header's <c>kid</c> naming it, the previous key still verifying for 24 hours after a rotation
/// (<c>common.yaml</c> <c>bearerAuth</c>). Public keys only; the private key never leaves the Key Vault.
/// </summary>
public sealed class TokenOptions
{
    public const string SectionName = "Authentication";

    public string Issuer { get; set; } = string.Empty;

    /// <summary>The audiences this host accepts: its staff and guest audience, and <c>cell</c> for serviceAuth.</summary>
    public List<string> Audiences { get; set; } = [];

    public List<SigningKey> SigningKeys { get; set; } = [];
}

public sealed class SigningKey
{
    public string KeyId { get; set; } = string.Empty;

    /// <summary>The RSA public key, PEM (<c>-----BEGIN PUBLIC KEY-----</c>).</summary>
    public string PublicKeyPem { get; set; } = string.Empty;
}
