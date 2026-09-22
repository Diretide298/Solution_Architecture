/**
 * Limiting Adam to particular networks, and the log that tells you which.
 *
 * **The page is arranged in the order the decision is actually made**, which is
 * not the order the data model suggests. A rules table at the top with a switch
 * next to it invites somebody to type what they think their office range is and
 * turn it on, and the first thing they learn is that they were wrong about it.
 * So: what is happening now, then the rules, then *who this would lock out* —
 * worked out from where people have really signed in — and only then the log
 * it was worked out from.
 *
 * Every control here is the super admin's, and the service refuses everybody
 * else including admins. The `denied` panel exists because being shown an empty
 * page is worse than being told why.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

/** "3 days ago", for a stamp. Exact dates are for the title attribute: the
 *  question a log answers is how stale something is, and a date makes the
 *  reader do the subtraction. */
function ago(stamp) {
  if (!stamp) return '—';
  const then = new Date(stamp);
  if (Number.isNaN(then.getTime())) return '—';
  const seconds = Math.max(0, (Date.now() - then.getTime()) / 1000);
  if (seconds < 90) return 'just now';
  const minutes = seconds / 60;
  if (minutes < 90) return `${Math.round(minutes)} min ago`;
  const hours = minutes / 60;
  if (hours < 36) return `${Math.round(hours)} h ago`;
  const days = Math.round(hours / 24);
  return days === 1 ? 'yesterday' : `${days} days ago`;
}

const state = { policy: null, seen: [], filter: '', uncoveredOnly: false };

function say(message) {
  $('ip-error').textContent = message ?? '';
  $('ip-error').hidden = !message;
}

// ── status ───────────────────────────────────────────────────────────

function drawStatus() {
  const p = state.policy ?? {};
  const host = $('ip-state');
  host.innerHTML = '';
  host.classList.toggle('is-armed', Boolean(p.armed));

  const headline = el('div', 'ip-headline');
  headline.append(el('span', `ip-dot ${p.armed ? 'on' : 'off'}`));
  headline.append(el('span', 'ip-headline-text',
    p.armed ? 'Adam is limited to the networks below'
      : 'Every address is allowed'));
  host.append(headline);

  const facts = el('dl', 'set-facts');
  const fact = (term, value, title) => {
    facts.append(el('dt', null, term));
    const dd = el('dd', null, value);
    if (title) dd.title = title;
    facts.append(dd);
  };
  fact('You are at', p.you || 'an address this service cannot work out');
  fact('Covered by a rule',
    p.you ? (p.youAreCovered ? 'Yes' : 'No') : 'Cannot tell');
  fact('Rules', String((p.rules ?? []).length));
  fact('Addresses seen', `${p.addresses ?? 0} across ${p.sightings ?? 0} account-address pairs`);
  if (p.changedAt) {
    fact('Last changed', `${ago(p.changedAt)}${p.changedBy ? ` by ${p.changedBy}` : ''}`,
      p.changedAt);
  }
  host.append(facts);

  // Loopback, which is either completely normal or the most dangerous thing
  // this page can be showing, and only the reader knows which.
  //
  // On a workstation the browser really is on the same machine. On a server it
  // means the proxy in front is not passing X-Real-IP, so *every* colleague
  // resolves to this one address — the log would be one row, and arming would
  // allow everybody or, after somebody "tidied" the rule, nobody. It is worth
  // saying here because the number looks like an answer either way.
  const loopback = p.you === '127.0.0.1' || p.you === '::1';
  $('ip-loopback').hidden = !loopback;

  $('ip-override').hidden = !p.overridden;

  // The arming control, and the reason it is not simply a toggle. Everything
  // that would refuse the request is said here first, so the button is the last
  // step rather than the way you find out.
  const armable = !p.armed && (p.rules ?? []).length > 0 && p.youAreCovered;
  $('ip-arm').hidden = Boolean(p.armed);
  $('ip-confirm-label').hidden = Boolean(p.armed) || !armable;
  $('ip-disarm').hidden = !p.armed;
  $('ip-arm').disabled = !armable;
  $('ip-arm').title = p.armed ? ''
    : !(p.rules ?? []).length
      ? 'Add at least one network first, or this would refuse everybody including you.'
      : !p.youAreCovered
        ? `No rule covers ${p.you || 'where you are'}, so this would refuse you first.`
        : '';
}

// ── rules ────────────────────────────────────────────────────────────

function drawRules() {
  const rules = state.policy?.rules ?? [];
  $('ip-rules-count').textContent = rules.length ? String(rules.length) : '';
  const host = $('ip-rules');
  host.innerHTML = '';
  if (!rules.length) {
    host.append(el('p', 'auth-note auth-fine',
      'No networks yet, so nothing is being refused. Look at the log below '
      + 'first — the addresses people already sign in from are the list.'));
    return;
  }
  for (const rule of rules) {
    const row = el('div', 'admin-row ip-row');
    const cidr = el('span', 'ip-cidr', rule.cidr);
    if (state.policy?.you && rule.cidr && state.policy.youAreCovered) {
      // Only a hint, and only when it is certainly true: the page does not do
      // containment arithmetic, so it says nothing rather than something it
      // would have to get right twice.
      if (rule.cidr === `${state.policy.you}/32`) cidr.append(el('span', 'ip-here', 'you'));
    }
    row.append(cidr);
    row.append(el('span', 'ip-label', rule.label || '—'));
    row.append(el('span', 'invite-who', `added ${ago(rule.addedAt)} by ${rule.addedBy}`));
    const drop = el('button', 'chip chip-quiet', 'Remove');
    drop.type = 'button';
    drop.onclick = async () => {
      drop.disabled = true;
      try { await auth.dropIpRule(rule.id); await load(); }
      catch (failure) { say(failure.message); drop.disabled = false; }
    };
    row.append(drop);
    host.append(row);
  }
}

// ── the dry run ──────────────────────────────────────────────────────

function drawDryRun(dry) {
  const out = dry?.wouldBeLockedOut ?? [];
  const unseen = dry?.unseen ?? [];
  $('ip-dry-count').textContent = out.length || unseen.length
    ? String(out.length + unseen.length) : '';
  const host = $('ip-dry');
  host.innerHTML = '';

  if (!dry?.rules) {
    host.append(el('p', 'auth-note auth-fine',
      'Nothing to work out yet: with no rules, switching on is refused anyway.'));
    return;
  }
  if (!out.length && !unseen.length) {
    host.append(el('p', 'auth-note auth-fine',
      'Everybody active has signed in from an address one of these rules covers. '
      + 'Switching on would strand nobody.'));
    return;
  }

  for (const person of out) {
    const row = el('div', 'admin-row ip-row ip-row-bad');
    row.append(el('span', 'account-name', person.name));
    row.append(el('span', 'invite-who', `${person.email} · ${person.role}`));
    row.append(el('span', 'ip-where',
      person.stranded.map((s) => s.ip).join(', ')));
    row.append(el('span', 'ip-verdict', 'no covered address'));
    host.append(row);
  }
  for (const person of unseen) {
    const row = el('div', 'admin-row ip-row ip-row-unknown');
    row.append(el('span', 'account-name', person.name));
    row.append(el('span', 'invite-who', `${person.email} · ${person.role}`));
    row.append(el('span', 'ip-where', '—'));
    row.append(el('span', 'ip-verdict', 'never seen anywhere'));
    host.append(row);
  }
}

// ── the log ──────────────────────────────────────────────────────────

function drawSightings() {
  const text = state.filter.trim().toLowerCase();
  const rows = state.seen.filter((item) => {
    if (state.uncoveredOnly && item.covered) return false;
    if (!text) return true;
    return [item.account.name, item.account.email, item.account.role, item.ip]
      .join(' ').toLowerCase().includes(text);
  });
  $('ip-seen-count').textContent = state.seen.length
    ? (rows.length === state.seen.length ? String(state.seen.length)
      : `${rows.length} of ${state.seen.length}`)
    : '';

  const host = $('ip-seen');
  host.innerHTML = '';
  if (!state.seen.length) {
    host.append(el('p', 'auth-note auth-fine',
      'Nothing yet. A row appears the first time somebody makes a request '
      + 'while signed in.'));
    return;
  }
  if (!rows.length) {
    host.append(el('p', 'auth-note auth-fine', 'Nothing matches that.'));
    return;
  }
  for (const item of rows) {
    const row = el('div', `admin-row ip-row${item.covered ? '' : ' ip-row-uncovered'}`);
    row.append(el('span', 'account-name', item.account.name));
    row.append(el('span', 'invite-who', `${item.account.email} · ${item.account.role}`));
    row.append(el('span', 'ip-cidr', item.ip));
    const when = el('span', 'ip-when', `${ago(item.lastSeen)} · ${item.hits} request${item.hits === 1 ? '' : 's'}`);
    when.title = `First seen ${item.firstSeen}\nLast seen ${item.lastSeen}`
      + (item.agent ? `\n${item.agent}` : '');
    row.append(when);
    row.append(el('span', `ip-verdict ${item.covered ? 'ok' : 'bad'}`,
      item.covered ? 'covered' : 'no rule'));
    host.append(row);
  }
}

function drawRefusals(refusals) {
  const rows = refusals?.items ?? [];
  $('ip-refused-count').textContent = rows.length ? String(rows.length) : '';
  const host = $('ip-refused');
  host.innerHTML = '';
  if (!rows.length) {
    host.append(el('p', 'auth-note auth-fine', 'Nobody has been turned away.'));
    return;
  }
  for (const row of rows) {
    const line = el('div', `admin-row ip-row${row.armed ? ' ip-row-bad' : ''}`);
    line.append(el('span', 'ip-cidr', row.ip));
    line.append(el('span', 'account-name', row.who));
    line.append(el('span', 'ip-where', row.path || '—'));
    const when = el('span', 'ip-when', ago(row.at));
    when.title = row.at;
    line.append(when);
    line.append(el('span', `ip-verdict ${row.armed ? 'bad' : ''}`,
      row.armed ? 'refused' : 'would have been'));
    host.append(line);
  }
}

// ── loading ──────────────────────────────────────────────────────────

async function load() {
  say('');
  // All five together. They are five reads of one store and the page is
  // meaningless with a subset — a dry run drawn against yesterday's rules is
  // worse than no dry run.
  const [policy, seen, dry, refusals] = await Promise.all([
    auth.allowlist(), auth.ipSightings(), auth.ipDryRun(), auth.ipRefusals(),
  ]);
  state.policy = policy;
  state.seen = seen.items ?? [];
  drawStatus();
  drawRules();
  drawDryRun(dry);
  drawSightings();
  drawRefusals(refusals);
}

// ── start ────────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';
  if (!auth.isOwner(me)) { $('denied').hidden = false; return; }
  $('ips').hidden = false;

  $('ip-add').onsubmit = async (event) => {
    event.preventDefault();
    say('');
    try {
      const made = await auth.addIpRule($('ip-cidr').value, $('ip-label').value);
      $('ip-cidr').value = '';
      $('ip-label').value = '';
      await load();
      // Said only when the two differ, which is when somebody typed a host
      // address with a prefix and got the range. Discovering that from who can
      // sign in tomorrow is the bad version.
      if (made.note) say(made.note);
    } catch (failure) { say(failure.message); }
  };

  $('ip-use-mine').onclick = () => {
    $('ip-cidr').value = state.policy?.you ?? '';
    $('ip-label').value = $('ip-label').value || 'Where I am now';
    $('ip-cidr').focus();
  };

  $('ip-arm').onclick = async () => {
    say('');
    try {
      await auth.armAllowlist($('ip-confirm').value);
      $('ip-confirm').value = '';
      await load();
    } catch (failure) { say(failure.message); }
  };

  $('ip-disarm').onclick = async () => {
    say('');
    try { await auth.disarmAllowlist(); await load(); }
    catch (failure) { say(failure.message); }
  };

  $('ip-seen-filter').oninput = (e) => { state.filter = e.target.value; drawSightings(); };
  $('ip-seen-uncovered').onchange = (e) => {
    state.uncoveredOnly = e.target.checked;
    drawSightings();
  };

  try { await load(); } catch (failure) { say(failure.message); }
})();
