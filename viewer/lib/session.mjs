/**
 * The gate on the reading server.
 *
 * Until now `server.mjs` served the whole delivery package to anyone who could
 * reach port 4173. On a workstation that was merely untidy. On a public address
 * it means the contracts, the schema, every screen and `/api/file` — which
 * returns any .yaml, .md, .json or .csv in the tree — are readable by whoever
 * finds the IP. Hiding the client code does nothing about it, because the API
 * is reachable without the client.
 *
 * Who is signed in is the accounts service's question, not this one's. Rather
 * than open the SQLite file behind its back and duplicate the schema, this asks
 * it — forwarding the session cookie to `/api/auth/me` — and believes the
 * answer. One boundary, one owner.
 *
 * The cost is an HTTP hop per request, so a valid token is cached for a minute.
 * A revoked session therefore survives up to 60 seconds; sign-out is not a
 * containment measure and does not need to be instant. Failures are cached too,
 * briefly, so a burst of unauthenticated requests cannot be used to hammer the
 * accounts service.
 */

const COOKIE = 'ticvai_session';
const TTL_OK_MS = 60_000;
const TTL_FAIL_MS = 5_000;

const cache = new Map(); // token -> { account, until }

/** Only the pages a signed-out visitor must be able to reach to sign in. */
const PUBLIC = new Set([
  '/login.html',
  '/invite.html',
  '/validation.js',
  '/auth-bg.js',
  '/login-demo.js',
  '/favicon.ico',
  '/api/health',
]);

/**
 * The brand, which both signed-out pages draw.
 *
 * Kept as a prefix rather than a list of filenames: the mark comes in a light
 * and a night cut and gained a third file the week it was added, and a
 * per-file allowlist is a thing that silently falls behind and leaves a broken
 * image on the first page anybody ever sees. The extension check is what keeps
 * it a brand directory and not an open one.
 */
const isBrandAsset = (pathname) =>
  pathname.startsWith('/brand/')
  && !pathname.includes('..')
  && /\.(svg|png|webp)$/i.test(pathname);

/**
 * Every stylesheet, rather than the five that happened to be needed.
 *
 * This list has fallen behind five separate times — the brand assets, the
 * partner logo, auth-bg.js, then auth.css — and each time the symptom was the
 * same: a 302 where a file should be, on the one page whose entire audience is
 * signed out, so nobody with an account could reproduce it. The last one cost
 * an afternoon because a missing stylesheet let the background canvas fall back
 * to its intrinsic 300x150 and the bug presented as "the animation is stuck".
 *
 * A stylesheet carries no package data. styles.css and layers.css — which hold
 * every rule the viewer has — were already public, so admitting the rest leaks
 * nothing that was not already out. Scripts stay named one by one, because a
 * script can read and send, and that is a different bargain.
 */
const isStylesheet = (pathname) =>
  pathname.endsWith('.css')
  && !pathname.includes('..')
  && pathname.lastIndexOf('/') === 0;

export function isPublic(pathname) {
  return PUBLIC.has(pathname) || isBrandAsset(pathname) || isStylesheet(pathname);
}

export function readCookie(header, name = COOKIE) {
  if (!header) return null;
  for (const part of header.split(';')) {
    const at = part.indexOf('=');
    if (at < 0) continue;
    if (part.slice(0, at).trim() === name) return decodeURIComponent(part.slice(at + 1).trim());
  }
  return null;
}

/**
 * Resolves the account behind a request, or null.
 *
 * `apiBase` is where the accounts service lives — same host in every
 * deployment, so this is a loopback call and not a trip over the network.
 */
export async function whoIs(req, apiBase) {
  const token = readCookie(req.headers.cookie);
  if (!token) return null;

  const hit = cache.get(token);
  if (hit && hit.until > Date.now()) return hit.account;

  let account = null;
  try {
    const res = await fetch(`${apiBase}/api/auth/me`, {
      headers: { cookie: `${COOKIE}=${encodeURIComponent(token)}` },
      signal: AbortSignal.timeout(4000),
    });
    if (res.ok) {
      const body = await res.json().catch(() => null);
      // /api/auth/me answers 200 with signedIn:false rather than 401, so the
      // status alone is not the answer — the body is.
      account = body?.signedIn ? (body.account ?? null) : null;
    }
  } catch {
    // The accounts service being unreachable must not open the door. A reader
    // who cannot be identified is not admitted, which is the whole point.
    account = null;
  }

  cache.set(token, { account, until: Date.now() + (account ? TTL_OK_MS : TTL_FAIL_MS) });
  if (cache.size > 4096) {
    for (const [k, v] of cache) if (v.until <= Date.now()) cache.delete(k);
  }
  return account;
}

/**
 * The gate. Returns `{ answered, role }`.
 *
 * `answered: true` means it has already written a response and the caller must
 * stop. Otherwise `role` says who this is, which is what the payload filter
 * needs — the question is never only "are they in" but "which of them is this".
 *
 * An API path gets 401 and JSON, because something is reading it. A page gets a
 * redirect to the sign-in door, because somebody is.
 */
export async function gate(req, res, url, apiBase) {
  if (isPublic(url.pathname)) return { answered: false, role: null };

  const account = await whoIs(req, apiBase);
  if (account) return { answered: false, role: account.role ?? 'reviewer' };

  if (url.pathname.startsWith('/api/')) {
    res.writeHead(401, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
    res.end(JSON.stringify({ error: 'not signed in' }));
    return { answered: true, role: null };
  }
  res.writeHead(302, { Location: '/login.html', 'Cache-Control': 'no-store' });
  res.end();
  return { answered: true, role: null };
}
