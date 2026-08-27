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

// Resolved once, then reused: `{ cookie }` when the sign-in worked, `{ why }`
// when it did not. Not throwing at this point is deliberate — see below.
let signIn = null;

async function session() {
  if (signIn) return signIn;

  let answer;
  try {
    answer = await fetch(`${API}/api/auth/login`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        email: process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
        password: process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase',
      }),
    });
  } catch (e) {
    // No accounts service listening at all.
    signIn = { why: `the accounts service at ${API} did not answer (${e.message})` };
    return signIn;
  }

  if (!answer.ok) {
    signIn = { why: `the harness could not sign in (${answer.status})` };
    return signIn;
  }

  // Just the name=value pair; the attributes are for a browser, not for us.
  const cookie = (answer.headers.getSetCookie?.() ?? [])
    .map((c) => c.split(';')[0]).join('; ');
  signIn = cookie ? { cookie } : { why: 'signed in but the server set no cookie' };
  return signIn;
}

/**
 * Same signature as `fetch`, with the session attached when there is one.
 *
 * **A failed sign-in is not fatal here, and used to be.** Against a throwaway
 * `TICVAI_NO_GATE=1` viewer the reads answer without a session, and this threw
 * before the first one — so a check that needed no account could not run
 * without one.
 *
 * `TICVAI_NO_GATE=1` is **not** enough for the browser half, which is worth
 * knowing before reaching for it: the gate stops refusing, but the page still
 * asks who it is talking to and redirects itself to `/login.html`, so a harness
 * that drives a browser needs a real accounts service either way. Point one at
 * a scratch store on a spare port rather than signing in against the real one.
 *
 * The diagnostic is not lost: it is held and raised by `authedJson` below, but
 * only when a read actually comes back 401 — which is the point at which the
 * missing session is genuinely the problem rather than a guess about it.
 */
export async function authed(url, options = {}) {
  const { cookie } = await session();
  const headers = { ...(options.headers ?? {}) };
  if (cookie) headers.cookie = cookie;
  return fetch(url, { ...options, headers });
}

/** `authed`, parsed, and loud about a non-200 rather than silently undefined. */
export async function authedJson(url, options = {}) {
  const answer = await authed(url, options);
  if (answer.status === 401 || answer.status === 403) {
    const { why } = await session();
    throw new Error(
      `${url} answered ${answer.status}. ${why ?? 'The session was refused.'} — the checks `
      + 'need an admin account: python -m api.cli admin harness.admin@softlabsgroup.com',
    );
  }
  if (!answer.ok) throw new Error(`${url} answered ${answer.status}`);
  return answer.json();
}

export { VIEWER, API };
