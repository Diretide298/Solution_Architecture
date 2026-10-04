# Guest screens that said they read staff tenant config (part of the specs; helpers there).
# flake8: noqa

_PRELOADED = ("PublishedTenantConfig (bookingFlow and the venue-wide settings), loaded once by the app "
              "shell with getPublishedTenantConfig (WEB-001, GST-001, KSK-002)")


def _walk(o, fn):
    if isinstance(o, dict):
        return {k: _walk(v, fn) for k, v in o.items()}
    if isinstance(o, list):
        return [_walk(v, fn) for v in o]
    if isinstance(o, str):
        return fn(o)
    return o


def _guest_published_config(S, pk):
    """A guest screen reads the published tenant config, never getTenantConfig (TENANT_CONFIGURE).

    Seventeen guest screens said their booking-flow settings come from `getTenantConfig` `bookingFlow`,
    a staff operation they do not bind; the judge could not build them (GST-002, WEB-007). The guest
    app loads `getPublishedTenantConfig` once in its shell and every step reads the copy it holds
    (Pattern 4, 3 October: guests read the published config). CHG-FXS-003."""
    out = []
    for sid, s in S.items():
        if s.get("_plat") not in ("P01", "P02", "P05"):
            continue
        ops = {a["operationId"] for a in s.get("apis") or []}
        if "getTenantConfig" in ops:
            continue
        hit = False
        for k in ("notes", "purpose", "purposeNote", "apisNote", "layout", "states"):
            if k not in s:
                continue
            new = _walk(s[k], lambda t: t.replace("`getTenantConfig`", "`getPublishedTenantConfig`")
                        .replace("getTenantConfig ", "getPublishedTenantConfig "))
            if new != s[k]:
                s[k] = new
                hit = True
        if hit and "getPublishedTenantConfig" not in ops:
            es = s.setdefault("entryState", {})
            pre = es.setdefault("preloaded", [])
            if _PRELOADED not in pre:
                pre.append(_PRELOADED)
        if hit:
            out.append((sid, f"{READ} {sid}: reads the published tenant config the app shell holds"))
    return out


EDGES.append(_guest_published_config)
