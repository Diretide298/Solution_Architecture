#!/usr/bin/env node
/**
 * The join between package artefacts and OpenProject work packages.
 *
 *   node viewer/api/links-check.mjs
 *
 * Needs a stored OpenProject credential to do anything real, because every call
 * is made as the caller — there is no service account, deliberately. Set
 * TICVAI_OP_TOKEN and this stores one for the harness account, uses it, and
 * removes it again.
 *
 * **The assertions that matter are the refusals.** A link to a work package
 * nobody can open is worse than no link — it looks like coordination and is a
 * dead end — so the store must refuse a number that does not resolve, refuse a
 * kind nobody will ever query for, and refuse a duplicate. Storing a good one
 * is the easy half.
 */

const BASE = (process.env.TICVAI_VIEWER ?? 'http://127.0.0.1:4173').replace(/\/+$/, '');
const EMAIL = process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com';
const PASSWORD = process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase';
const TOKEN = process.env.TICVAI_OP_TOKEN ?? '';

const results = [];
const pass = (what) => { results.push(true); console.log(`  ok    ${what}`); };
const fail = (what, why) => { results.push(false); console.log(`  FAIL  ${what}\n        ${why}`); };
const skip = (what, why) => console.log(`  skip  ${what} — ${why}`);

let cookie = '';
async function call(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      ...(cookie ? { cookie } : {}),
      ...(body === undefined ? {} : { 'content-type': 'application/json' }),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let data = null;
  try { data = await res.json(); } catch { /* empty is fine */ }
  return { status: res.status, data };
}

console.log('\nartefact links');

const login = await fetch(`${BASE}/api/auth/login`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
});
if (!login.ok) {
  console.log(`  cannot sign in as ${EMAIL} (${login.status}).`);
  process.exit(1);
}
cookie = `ticvai_session=${decodeURIComponent(
  (login.headers.getSetCookie?.() ?? []).map((l) => /ticvai_session=([^;]+)/.exec(l)?.[1]).find(Boolean),
)}`;
pass(`signed in as ${EMAIL}`);

// ---- reading needs no credential -------------------------------------------

const empty = await call('/api/links?target_kind=screen&target_id=NOPE-999');
if (empty.status === 200 && empty.data.total === 0) pass('an artefact with no links reads as zero, not an error');
else fail('an artefact with no links reads as zero', JSON.stringify(empty));

// ---- writing needs one, and says so ----------------------------------------

// Make sure there is none, so the 428 is the real path rather than a leftover.
await call('/api/settings/openproject', { method: 'DELETE' });

const nocreds = await call('/api/links', {
  method: 'POST', body: { target_kind: 'screen', target_id: 'WEB-001', external_key: '1' },
});
// 428 Precondition Required: the request is fine, something has to be set up
// first. A 401 would say "sign in", which they have, and a 500 would say
// nothing at all.
if (nocreds.status === 428 && /Settings/i.test(nocreds.data?.detail ?? '')) {
  pass('linking without a stored credential says to connect OpenProject first');
} else fail('linking without a credential is a 428 naming the fix', JSON.stringify(nocreds));

// **Input is checked before the credential is.** The other way round, a bad
// number without a stored token answers "connect your OpenProject account",
// which sends somebody to configure a thing that was never the problem.
for (const bad of ['abc', '1?filters=x', '-1']) {
  const r = await call(`/api/work-packages/${encodeURIComponent(bad)}`);
  if (r.status === 400 && /not a work package number/i.test(r.data?.detail ?? '')) {
    pass(`"${bad}" is refused as a work package number, before any credential check`);
  } else fail(`"${bad}" is refused as a work package number`, `${r.status} ${JSON.stringify(r.data)}`);
}

if (!TOKEN) {
  skip('the rest', 'set TICVAI_OP_TOKEN — every call is made as the caller, so there is no way round it');
} else {
  const stored = await call('/api/settings/openproject', { method: 'PUT', body: { token: TOKEN } });
  if (stored.status !== 200) {
    fail('storing the harness credential', JSON.stringify(stored));
  } else {
    pass(`credential stored — ${stored.data.connectedAs}`);

    // A kind nobody will ever query for is a row lost on the day it is written.
    const badKind = await call('/api/links', {
      method: 'POST', body: { target_kind: 'sausage', target_id: 'X', external_key: '1' },
    });
    if (badKind.status === 400) pass('an unknown artefact kind is refused');
    else fail('an unknown artefact kind is refused', JSON.stringify(badKind));

    // **The one that matters.** A number nobody can open must not become a row.
    const ghost = await call('/api/links', {
      method: 'POST', body: { target_kind: 'screen', target_id: 'WEB-001', external_key: '99999999' },
    });
    if (ghost.status === 400 || ghost.status === 502) {
      pass(`a work package that does not resolve is not linked (${ghost.status})`);
    } else fail('a work package that does not resolve is not linked', JSON.stringify(ghost));

    // A real one, if the project has any. The TICVAI project was empty when
    // this was written, so this half is honest about finding nothing rather
    // than inventing a fixture.
    const board = await call('/api/board/mine');
    if (board.status === 200) {
      pass(`the board answers — ${board.data.total} open item(s) assigned to you`);
      if (board.data.total === 0 && board.data.note) {
        pass('and an empty board explains itself rather than looking like a bug');
      }
    } else fail('the board answers', JSON.stringify(board));

    const anyWp = board.data?.items?.[0]?.key;
    if (!anyWp) {
      skip('linking a real work package', 'nothing is assigned to this account in OpenProject');
    } else {
      const made = await call('/api/links', {
        method: 'POST', body: { target_kind: 'screen', target_id: 'WEB-001', external_key: anyWp },
      });
      if (made.status === 200 && made.data.workPackage?.subject) {
        pass(`linked screen WEB-001 to #${anyWp} — "${made.data.workPackage.subject}"`);
      } else fail('linking a real work package', JSON.stringify(made));

      const again = await call('/api/links', {
        method: 'POST', body: { target_kind: 'screen', target_id: 'WEB-001', external_key: anyWp },
      });
      if (again.status === 409) pass('saying it twice is a 409, not a duplicate row');
      else fail('saying it twice is a 409', JSON.stringify(again));

      const forward = await call('/api/links?target_kind=screen&target_id=WEB-001');
      if (forward.data?.total >= 1) pass('artefact → work reads back');
      else fail('artefact → work reads back', JSON.stringify(forward));

      const back = await call(`/api/work-packages/${anyWp}`);
      if (back.data?.touches?.some((t) => t.id === 'WEB-001')) pass('work → artefact reads back');
      else fail('work → artefact reads back', JSON.stringify(back));

      const id = forward.data.links[0].id;
      const gone = await call(`/api/links/${id}`, { method: 'DELETE' });
      if (gone.status === 200 && /untouched/i.test(gone.data?.note ?? '')) {
        pass('unlinking says the work package is untouched');
      } else fail('unlinking says the work package is untouched', JSON.stringify(gone));
    }

    // Put the account back as it was found.
    await call('/api/settings/openproject', { method: 'DELETE' });
    pass('harness credential removed again');
  }
}

const failed = results.filter((ok) => !ok).length;
console.log(`\n${results.length - failed} of ${results.length} checks passed`);
process.exit(failed ? 1 : 0);
