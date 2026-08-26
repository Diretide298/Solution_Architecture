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
  return readCookies(header, name)[0] ?? null;
}

/**
 * Every value sent under one cookie name, in the order the browser sent them.
 *
 * There is normally one. There are two for anybody who signed in while the
 * front end and the accounts service shared an origin and has signed in again
 * since they stopped: the old cookie is host-only to the front end's name, the
 * new one is scoped to the parent domain, both are called `ticvai_session`, and
 * a browser sends both. Cookies carry no attributes on the way back, so the two
 * are indistinguishable here — the header is `ticvai_session=a; ticvai_session=b`
 * and nothing in it says which is which.
 *
 * Taking the first was the bug. The browser sends the older one first, so the
 * stale value won every time, the gate called a signed-in reader a stranger and
 * sent them to the sign-in door, which asked the accounts service — reachable
 * on the *other* name, where only the good cookie applies — was told yes, and
 * sent them back. Neither half was wrong on its own.
 */
export function readCookies(header, name = COOKIE) {
  if (!header) return [];
  const out = [];
  for (const part of header.split(';')) {
    const at = part.indexOf('=');
    if (at < 0) continue;
    if (part.slice(0, at).trim() === name) out.push(decodeURIComponent(part.slice(at + 1).trim()));
  }
  return out;
}

/**
 * Deletes a host-only `ticvai_session` — no Domain attribute, so it matches the
 * cookie the front end's own name once set and leaves the parent-domain one
 * alone. Sent when a request arrives holding a token that resolves to nobody,
 * which is exactly the shape of the stale duplicate above.
 *
 * Path and name must match the cookie being deleted or the browser keeps it.
 */
const CLEAR_STALE = `${COOKIE}=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax`;

/**
 * Resolves the account behind a request, or null.
 *
 * Every `ticvai_session` on the request is tried, not just the first, and the
 * first one that names somebody wins. One dead cookie sitting in front of a
 * live one is a transitional state with a long tail — it lasts until the reader
 * clears it, and a reader who cannot get in cannot be told to — so this stops
 * depending on the order the browser happens to send them in.
 *
 * Ordinary requests carry one cookie and cost one call, unchanged.
 */
export async function whoIs(req, apiBase) {
  for (const token of readCookies(req.headers.cookie)) {
    const account = await resolveToken(token, apiBase);
    if (account) return account;
  }
  return null;
}

/**
 * `apiBase` is where the accounts service lives — same host in every
 * deployment, so this is a loopback call and not a trip over the network.
 */
async function resolveToken(token, apiBase) {
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
      // The projects sit beside the account rather than inside it, because they
      // are not a property of the person -- they are the grants. Carried onto
      // the object anyway, so everything downstream has one thing to hold, and
      // cached with it: they change when somebody is granted a package, which
      // is exactly as often as the rest of this is allowed to be stale.
      if (account && Array.isArray(body.projects)) account.projects = body.projects;
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
/**
 * What an embedded preview gets instead of the sign-in page.
 *
 * Drawn on white and inline, because the frames it replaces are: this lands
 * inside a board stage that has no stylesheet of its own and does not inherit
 * the viewer's theme.
 */
const EMBED_REFUSAL =
  '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
  '<title>Session ended</title><style>' +
  'html,body{margin:0;background:#fff;height:100%}' +
  'body{display:flex;align-items:center;justify-content:center;' +
  'font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#1f2937;padding:24px}' +
  '.box{max-width:32em;text-align:center;line-height:1.5}' +
  'b{display:block;font-size:15px;margin-bottom:6px}' +
  'p{margin:0;font-size:13px;color:#6b7280}' +
  '</style></head><body><div class="box">' +
  '<b>This preview could not be loaded.</b>' +
  '<p>The sign-in behind it has ended, so the board it draws from was refused. ' +
  'Reload the page to sign in again — nothing you were looking at has moved.</p>' +
  '</div></body></html>';

export async function gate(req, res, url, apiBase) {
  if (isPublic(url.pathname)) return { answered: false, role: null, projects: null };

  const account = await whoIs(req, apiBase);
  if (account) {
    return {
      answered: false,
      role: account.role ?? 'reviewer',
      // Which packages this account may read, and as what. Null where the
      // accounts service is older than the projects tables \u2014 the caller treats
      // that as "cannot tell" rather than as "none", so an upgrade in the wrong
      // order does not lock everybody out of everything.
      projects: Array.isArray(account.projects) ? account.projects : null,
    };
  }

  // A token that names nobody is worth taking off the reader on the way past.
  // It is either expired, revoked or the stale host-only duplicate described
  // above, and in every one of those cases the browser is holding something it
  // will keep presenting forever otherwise. Only sent when there was one to
  // begin with, so an ordinary signed-out visitor gets no Set-Cookie at all.
  const stale = readCookies(req.headers.cookie).length > 0;
  const headers = { 'Cache-Control': 'no-store', ...(stale ? { 'Set-Cookie': CLEAR_STALE } : {}) };

  if (url.pathname.startsWith('/api/')) {
    res.writeHead(401, { ...headers, 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'not signed in' }));
    return { answered: true, role: null };
  }

  // An <iframe> handed a 302 to the sign-in page renders the sign-in page —
  // scaled down, inside a preview box, under a caption saying "from the
  // platform board". It reads as the viewer having loaded the wrong file, and
  // it is the most confusing possible way to say "your session ended": the SPA
  // shell keeps working off data it already fetched, so the *only* symptom is
  // a wireframe panel showing somebody a login form. The board previews load
  // lazily, which means this can surface an hour after the page did.
  //
  // `Sec-Fetch-Dest` separates the two cases and every browser that can render
  // an iframe sends it. Somebody opening a board full size in a new tab is
  // `document` and still wants the door. An embed wants to be told, in the box,
  // what actually happened.
  const dest = req.headers['sec-fetch-dest'];
  if (dest === 'iframe' || dest === 'frame' || dest === 'embed' || dest === 'object') {
    res.writeHead(401, { ...headers, 'Content-Type': 'text/html; charset=utf-8' });
    res.end(EMBED_REFUSAL);
    return { answered: true, role: null };
  }

  res.writeHead(302, { ...headers, Location: '/login.html' });
  res.end();
  return { answered: true, role: null };
}
