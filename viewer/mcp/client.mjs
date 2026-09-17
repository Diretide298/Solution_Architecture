/**
 * The MCP's half of the conversation with the viewer.
 *
 * Two things live here that are easy to get wrong somewhere else.
 *
 * **This is a selector, not a proxy.** The viewer's read routes are bulk
 * payloads — `/api/journeys` returns every flow and every screen, `/api/backend`
 * the whole data model, `/api/search` the entire corpus. They were built for a
 * browser that loads a layer once and holds it, and there is no
 * `/api/screen?id=BO-102` to proxy to. So a layer is fetched whole, held, and
 * indexed into. A tool call costs no HTTP after the first.
 *
 * **The cache asks the server whether what it holds is still current.** Never a
 * timer: a TTL here would be a second opinion about freshness, and the wrong
 * one — a cache that quietly serves last week's screen is worse than no cache.
 *
 * Two ways to ask, and the good one is tried first.
 *
 * `If-None-Match`, against the ETag `sendCachedJson` now emits. One conditional
 * request settles it: a 304 with no body, or the new payload. This did not work
 * at first — the route answered `no-store` with no validator at all, so the
 * revalidation never fired and every tool call re-downloaded the whole layer,
 * 1.9 MB of index to look up one contract. Silent, too: the answers were right
 * and only slow. Fixed in the viewer as V-46.
 *
 * `/api/summary`.`generatedAt` is the fallback, for a deployed viewer that
 * predates that fix. A few hundred bytes, but a second round trip per read.
 * Both are kept because a developer points their MCP at whichever viewer is
 * deployed, and that is not always this one.
 *
 * Auth is a cookie and only a cookie: `lib/session.mjs` reads
 * `req.headers.cookie` and has no bearer path. The viewer proxies
 * `/api/auth/*` to the accounts service on :8787 and forwards Set-Cookie back,
 * so one base URL covers both halves.
 */

const COOKIE = 'ticvai_session';

/** A refusal by the audience filter, kept distinct from a transport failure.
 *  `lib/audience.mjs` denies a client account the `decisions` route; the honest
 *  answer is to say so, not to return an empty result that reads as "nothing
 *  there". */
export class Forbidden extends Error {
  constructor(route, detail) {
    super(`the signed-in account may not read "${route}"${detail ? ` — ${detail}` : ''}`);
    this.name = 'Forbidden';
    this.route = route;
  }
}

export class ViewerClient {
  #token = null;
  #signingIn = null;
  #defaultProject = null;
  #cache = new Map(); // key -> { etag, stamp, body }

  constructor({ base, project, email, password } = {}) {
    this.base = (base ?? 'http://127.0.0.1:4173').replace(/\/+$/, '');
    this.project = project ?? null;
    this.email = email;
    this.password = password;
  }

  /**
   * `/pkg/<id>/…` by preference, bare `/api/…` only as a fallback.
   *
   * Both spellings resolve to the same route name, which is what the audience
   * filter checks, so access is identical. What differs is the deployment:
   * `deploy/nginx/adamapi.ainfinite.ai` forwards `location /pkg/` wholesale but
   * names the `/api/*` routes one by one — and that list is **already missing
   * `cicd`**, tolerated because the `/pkg/` rule covers it. A client on the bare
   * spelling therefore works locally and 404s in production on whichever route
   * nobody remembered to add. The prefixed spelling cannot drift.
   */
  url(route, params) {
    const id = this.project ?? this.#defaultProject;
    const path = id ? `/pkg/${id}/${route}` : `/api/${route}`;
    const qs = params ? `?${new URLSearchParams(params)}` : '';
    return `${this.base}${path}${qs}`;
  }

  /**
   * Which package to read, asked once.
   *
   * `/api/projects` sits outside the prefix — it is what a caller reads *before*
   * it can name a project — and is in the nginx list on both hosts. It answers
   * only the packages this account may open, so a `default` coming back here is
   * one we are already allowed to read.
   */
  async #resolveProject() {
    if (this.project || this.#defaultProject) return;
    try {
      const answer = await this.#send(`${this.base}/api/projects`, 'projects');
      if (!answer.ok) return;
      const body = await answer.json();
      this.#defaultProject = body.default ?? body.projects?.[0]?.id ?? null;
    } catch {
      // Leave it null and use the bare spelling. An older viewer predating the
      // projects registry has no /pkg/ routes at all, and refusing to read it
      // would be worse than the drift this avoids.
    }
  }

  /**
   * The package this connector works in: ADAM_PROJECT when setup chose one,
   * otherwise the account's default. The accounts service scopes the board,
   * work packages and links by it, each package to its own OpenProject project.
   */
  async projectId() {
    await this.#resolveProject();
    return this.project ?? this.#defaultProject;
  }

  async login() {
    if (!this.email || !this.password) {
      throw new Error('set ADAM_EMAIL and ADAM_PASSWORD — the viewer has no anonymous read');
    }
    const answer = await fetch(`${this.base}/api/auth/login`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: this.email, password: this.password }),
      redirect: 'manual',
    });
    if (!answer.ok) {
      const detail = await answer.text().catch(() => '');
      throw new Error(`sign-in failed (${answer.status}) ${detail.slice(0, 200)}`);
    }
    // getSetCookie keeps the headers separate. A joined string cannot be split
    // safely — an Expires date contains a comma.
    const raw = answer.headers.getSetCookie?.() ?? [];
    for (const line of raw) {
      const match = new RegExp(`^${COOKIE}=([^;]+)`).exec(line);
      if (match) this.#token = decodeURIComponent(match[1]);
    }
    if (!this.#token) throw new Error('signed in but no session cookie came back');
    return this.#token;
  }

  /** One request, signing in first if there is no session and once more if the
   *  one we hold has expired underneath us. Sessions last 14 days, so the
   *  retry fires rarely — but a long-lived MCP process will outlive one. */
  async #send(href, route, retry = true, etag = null) {
    // One sign-in even when several tools start at once. Without this the first
    // burst of calls each sees no token and logs in separately, leaving a pile
    // of live sessions behind for one process.
    if (!this.#token) {
      this.#signingIn ??= this.login().finally(() => { this.#signingIn = null; });
      await this.#signingIn;
    }
    const headers = { cookie: `${COOKIE}=${encodeURIComponent(this.#token)}` };
    if (etag) headers['if-none-match'] = etag;

    const answer = await fetch(href, { headers, redirect: 'manual' });

    // The gate answers a dead session with a redirect to the sign-in page
    // rather than a 401, because its usual caller is a browser.
    if ((answer.status === 401 || answer.status === 302) && retry) {
      this.#token = null;
      return this.#send(href, route, false, etag);
    }
    if (answer.status === 403) {
      const detail = await answer.json().catch(() => null);
      throw new Forbidden(route, detail?.error);
    }
    return answer;
  }

  /**
   * When the package was last built. A few hundred bytes, so it is cheap enough
   * to ask before every layer read; everything held is keyed on the answer.
   *
   * A summary that will not load is not a reason to refuse the read — the layer
   * routes are independent of it — so a failure here degrades to "cannot tell",
   * which drops the cache and fetches. Slow beats wrong.
   */
  async #stamp() {
    try {
      const answer = await this.#send(this.url('summary'), 'summary');
      if (!answer.ok) return null;
      return (await answer.json()).generatedAt ?? null;
    } catch {
      return null;
    }
  }

  /**
   * `build` is a thunk, not a string: the project is resolved here, and a URL
   * built before that ran would carry the fallback spelling for the life of the
   * process.
   *
   * Two ways to ask "is what I hold still current", and the good one is tried
   * first. **A viewer with the V-46 fix answers `ETag`**, so one conditional
   * request either returns 304 with no body or the new payload — no second
   * round trip. A viewer without it answers no validator at all, and the
   * fallback is `/api/summary`.`generatedAt`, which costs a small extra request
   * per read. Both are kept because a developer's MCP is pointed at whichever
   * viewer happens to be deployed, and that is not always this one.
   */
  async #cached(key, build) {
    await this.#resolveProject();
    const held = this.#cache.get(key);

    // No validator on what we hold — an older viewer. Ask the package instead,
    // and only then decide whether to fetch.
    if (held && !held.etag) {
      const stamp = await this.#stamp();
      if (stamp && held.stamp === stamp) return held.body;
    }

    const answer = await this.#send(build(), key, true, held?.etag ?? null);
    if (answer.status === 304) return held.body;
    if (!answer.ok) throw new Error(`GET ${key} → ${answer.status}`);

    const body = await answer.json();
    const etag = answer.headers.get('etag');
    // The stamp is only fetched when there is no ETag to lean on.
    this.#cache.set(key, { etag, stamp: etag ? null : await this.#stamp(), body });
    return body;
  }

  /** A whole layer, held against the package stamp. */
  layer(route) {
    return this.#cached(route, () => this.url(route));
  }

  /** The `description` and `properties` held back from /api/index, for one
   *  contract file. Held under its own key so one contract's detail does not
   *  evict another's. */
  detail(file) {
    return this.#cached(`detail:${file}`, () => this.url('detail', { file }));
  }

  /**
   * One low-level diagram, by set and name — `services`, `platforms`,
   * `contracts`, `lifecycles`.
   *
   * Held like a layer, because the service files are 28 KB apiece and a caller
   * reading one usually reads it twice: once for the summary and once for the
   * operations.
   */
  diagram(set, name) {
    return this.#cached(`diagram:${set}:${name}`,
      () => this.url('diagrams/detail', { set, name }));
  }

  /**
   * The accounts service, which is a different animal from the package routes.
   *
   * Not cached, ever. Those routes serve a package that changes when somebody
   * runs a derivation; these serve coordination, which changes while you are
   * looking at it. A board held for even a minute is a board that is wrong, and
   * wrong in the direction that matters — it shows work as unstarted after
   * somebody has started it.
   *
   * Never prefixed with `/pkg/<id>/` either: the accounts service is one
   * service across every package, and `project_id` is a field in its payloads
   * rather than a segment of its paths.
   *
   * **This is the only method here that writes**, and the write is a row saying
   * a work package is about an artefact. Nothing in this file can change a work
   * package, a status or an assignee — OpenProject owns all three, and the
   * bridge owning any of them would be a second plan over the same work.
   */
  async service(path, { method = 'GET', body } = {}) {
    if (!this.#token) {
      this.#signingIn ??= this.login().finally(() => { this.#signingIn = null; });
      await this.#signingIn;
    }
    const send = (token) => fetch(`${this.base}${path}`, {
      method,
      headers: {
        cookie: `${COOKIE}=${encodeURIComponent(token)}`,
        ...(body === undefined ? {} : { 'content-type': 'application/json' }),
      },
      body: body === undefined ? undefined : JSON.stringify(body),
      redirect: 'manual',
    });

    let answer = await send(this.#token);
    if (answer.status === 401 || answer.status === 302) {
      this.#token = null;
      await this.login();
      answer = await send(this.#token);
    }

    let data = null;
    try { data = await answer.json(); } catch { /* an empty body is an answer */ }
    // The status comes back rather than being thrown on, because these routes
    // use it to say things: 428 means "connect OpenProject first", 409 means
    // "already said". Both are answers a tool should relay, not failures.
    return { status: answer.status, ok: answer.ok, data };
  }

  /**
   * One file's source, as text. `/api/file` answers prose, not JSON.
   *
   * Not held: files are small and there are thousands, so caching them would
   * grow without bound to save a request that was never the expensive one. The
   * layers are the 1.9 MB reads worth holding.
   *
   * The status comes back with the text because `/api/file` distinguishes 400
   * for a name that is not one, 404 for a name that is and is not there, and
   * 403 for a decision file a client may not read — and sending somebody to
   * hunt a typo in a correct name is its own wrong answer.
   */
  async file(path) {
    await this.#resolveProject();
    const answer = await this.#send(this.url('file', { path }), 'file');
    const text = await answer.text();
    return { ok: answer.ok, status: answer.status, text };
  }
}
