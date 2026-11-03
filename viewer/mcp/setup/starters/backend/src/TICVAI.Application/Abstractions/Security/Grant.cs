namespace TICVAI.Application.Abstractions.Security;

/// <summary>Whether a grant allows or denies (permission-resolution spec, section 1).</summary>
public enum GrantEffect
{
    Allow,
    Deny,
}

/// <summary>
/// One grant of the principal's <b>selected role</b> (R6): a permission, or <c>*</c> for a wildcard
/// deny (R4), at a scope path (ltree text), allowing or denying, until <paramref name="ValidTo"/> if
/// it expires (R10). A workstation is never a grant input (R5); it may be the scope a query targets.
/// </summary>
public sealed record Grant(string Permission, string ScopePath, GrantEffect Effect, DateTimeOffset? ValidTo = null)
{
    /// <summary>The permission a wildcard deny names. A wildcard allow matches nothing (R4).</summary>
    public const string Wildcard = "*";
}
