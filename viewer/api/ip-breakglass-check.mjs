// Getting back in after locking yourself out.
//
// Separate from ip-check.mjs because it cannot share a process with it: the
// thing under test is an environment variable read at request time, and setting
// it means starting the service again. The store this runs against is the one
// ip-check.mjs leaves behind — **armed**, with a rule that covers exactly one
// address and refuses every other.
//
// This is the assertion the whole feature rests on. Everything else in the
// allowlist is a door; this is the fact that there is a way back in when the
// door closes on the wrong side, and it has to be reachable from a shell rather
// than from the page, because the page is the thing you have lost.
//
//   TICVAI_DB=/tmp/ip.db ADAM_IP_ALLOWLIST=off \
//     python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 node api/ip-breakglass-check.mjs

const API = process.env.API ?? 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const OFFICE = '203.0.113.7';
const STRANGER = '192.0.2.99';
const PASSWORD = 'a-long-enough-passphrase';

let cookie = '';
async function call(method, path, body, ip) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      'content-type': 'application/json', 'x-real-ip': ip,
      ...(cookie ? { cookie } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) cookie = set.split(';')[0];
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

// From the address the rules refuse, which is what being locked out means.
const back = await call('POST', '/api/auth/login',
  { email: 'harness.boss@softlabsgroup.com', password: PASSWORD }, STRANGER);
check('with the override set, a refused address can sign in again',
  back.status === 200, `${back.status} ${JSON.stringify(back.data?.detail ?? '')}`);

const state = await call('GET', '/api/ips', undefined, STRANGER);
check('and reach the page that undoes it', state.status === 200, `${state.status}`);

// The half that would be easy to get wrong: turning the override on must not
// quietly turn the policy off. Somebody restarting without the variable has to
// find the allowlist exactly as they left it.
check('the policy still reads as armed, because the override is not a switch',
  state.data?.armed === true, String(state.data?.armed));
check('and the page says out loud that it is being ignored',
  state.data?.overridden === true, String(state.data?.overridden));

// The point of getting back in.
const fix = await call('POST', '/api/ips/rules',
  { cidr: STRANGER, label: 'Where I actually am' }, STRANGER);
check('the address that was refused can be added from it',
  fix.status === 200, `${fix.status}`);

const off = await call('POST', '/api/ips/disarm', {}, STRANGER);
check('and the allowlist switched off entirely', off.data?.armed === false, `${off.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
