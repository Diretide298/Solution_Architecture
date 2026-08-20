/**
 * A signed-in `fetch` for the Node side of a check.
 *
 * The gate (V-05) covers every `/api/*` the viewer serves, so a bare `fetch`
 * from a check gets 401 and a body with no `nodes` in it — which surfaces as
 * `Cannot read properties of undefined (reading 'filter')` twenty lines later,
 * naming neither auth nor the endpoint. These checks were written before the
 * gate and had been failing that way rather than reporting it.
 *
 * Page-side requests are unaffected: puppeteer carries the cookie once the
 * harness has signed in through the browser.
 */
const VIEWER = process.env.TICVAI_VIEWER ?? 'http://localhost:4173';
const API = process.env.TICVAI_API ?? 'http://localhost:8787';

let cookie = null;

async function session() {
  if (cookie) return cookie;
  const answer = await fetch(`${API}/api/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      email: process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
      password: process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase',
    }),
  });
  if (!answer.ok) {
    throw new Error(
      `the harness could not sign in (${answer.status}). The checks need an admin account — `
      + `create one with: python -m api.cli admin harness.admin@softlabsgroup.com`,
    );
  }
  // Just the name=value pair; the attributes are for a browser, not for us.
  cookie = (answer.headers.getSetCookie?.() ?? [])
    .map((c) => c.split(';')[0]).join('; ');
  if (!cookie) throw new Error('signed in but the server set no cookie');
  return cookie;
}

/** Same signature as `fetch`, with the session attached. */
export async function authed(url, options = {}) {
  const jar = await session();
  return fetch(url, { ...options, headers: { ...(options.headers ?? {}), cookie: jar } });
}

/** `authed`, parsed, and loud about a non-200 rather than silently undefined. */
export async function authedJson(url, options = {}) {
  const answer = await authed(url, options);
  if (!answer.ok) throw new Error(`${url} answered ${answer.status}`);
  return answer.json();
}

export { VIEWER, API };
