/**
 * Handing a team lead a platform.
 *
 * `scope` is the third axis of the role model — `account.role` says what
 * somebody may do anywhere, `account_project` says which packages they may
 * open, and this says which slice of one is theirs. The reasoning about why
 * those are three questions rather than one is in `api/db.py`, above the table.
 *
 * **What a grant decides is narrow, and the panel says so out loud.** A team
 * lead reads every change request on the project whether or not they own a
 * platform — a lead who cannot see what is coming cannot prepare for it. The
 * slice decides which ones reach their bell, which they may take on, and which
 * they may settle. People reasonably assume a permission control is about
 * *seeing*, and here it is not.
 *
 * The owner's, and nobody else's. An admin reads this panel and cannot change
 * it; the service refuses them either way, because a hidden control is still a
 * POST away for anybody who opens devtools.
 */

import {
  listScopes, listAccounts, grantScope, revokeScope, project, isOwner, account,
  roleLabel,
} from '/validation.js';
import { el, table, confirmStep, personLink } from '/sheet.js';

/** Which platforms exist, from the package rather than from a list kept here.
 *
 *  The accounts service deliberately cannot answer this — it does not read the
 *  packages, and teaching it to would be a second reader of the same files — so
 *  it validates the *shape* of a platform code and not its existence. That
 *  leaves the page as the only place that can offer a real list, which is why
 *  this fetch is here and why a failure is survivable: the control falls back
 *  to a text box, and a typo shows up as a scope that matches nothing.
 */
async function platformsOf(projectId) {
  // No project, no list. The admin page carries no `?project=`, so `project()`
  // can be empty here — and `/pkg//platforms` is a 404 that looks like a broken
  // page rather than the absence of an answer. The id comes from the service's
  // own reply instead; see draw() below.
  if (!projectId) return [];
  try {
    const res = await fetch(`/pkg/${encodeURIComponent(projectId)}/platforms`,
      { credentials: 'include' });
    if (!res.ok) return [];
    const data = await res.json();
    return (data.platforms ?? [])
      .filter((p) => p.code)
      .map((p) => ({ code: p.code, name: p.shortName || p.name || p.code }));
  } catch {
    return [];
  }
}

const SIDES = [['frontend', 'Frontend'], ['backend', 'Backend']];

/**
 * Draws the platforms section. `onChange` is told after a grant or a
 * revoke, so the page's "needs you" list can stop naming somebody who now
 * holds one.
 *
 * `me` is the account the page signed in with. It is handed in rather than
 * read from `account()`, because that is filled by whichever other module
 * asked the service first, and on this page nothing had always asked by the
 * time this ran: the System Architect was shown the read-only list.
 */
export async function mountPlatforms({ me, onChange } = {}) {
  const $ = (id) => document.getElementById(id);
  const host = $('platforms-list');
  if (!host) return;

  const error = $('platforms-error');
  const say = (message) => {
    error.textContent = message;
    error.hidden = !message;
  };

  const mayEdit = isOwner(me ?? account());
  // Which project, decided by the service rather than by the address. This page
  // names none, and asking for scopes with an empty id is how the service is
  // told "the one this account reads", so the id comes back with the answer
  // and everything after it can be specific.
  let projectId = project() ?? '';
  let platforms = null;

  async function draw() {
    say('');
    let scopes = [];
    let people = [];
    try {
      const [mine, roster] = await Promise.all([listScopes(projectId), listAccounts()]);
      scopes = mine.scopes ?? [];
      projectId = mine.project ?? projectId;
      people = roster.accounts ?? [];
    } catch (failure) {
      say(`Could not read who holds which platform: ${failure.message}. Reload the page to try again.`);
      return;
    }
    // Once, after the project is known. A failure here is survivable: the
    // control falls back to "all platforms" only, and the service validates the
    // shape of anything typed anyway.
    if (platforms === null) platforms = await platformsOf(projectId);

    // Only the roles a slice means anything for. A System Architect, an admin
    // and a pm are whole rather than scoped, and the service refuses a grant on
    // one, so listing them here would be listing rows whose every control is a
    // refusal.
    const scopable = people.filter((p) => ['lead', 'dev'].includes(p.role) && p.active);
    const held = new Map();
    for (const s of scopes) {
      if (!held.has(s.account.id)) held.set(s.account.id, []);
      held.get(s.account.id).push(s);
    }

    host.replaceChildren(table({
      caption: 'Every active team lead and developer, and the platforms they own',
      columns: [
        {
          key: 'name', label: 'Person',
          render: (p) => (p.name ? personLink(p.name) : el('span', '', p.email)),
          sort: (p) => (p.name || p.email).toLowerCase(),
        },
        { key: 'role', label: 'Role', render: (p) => roleLabel(p.role), sort: (p) => p.role },
        { key: 'holds', label: 'Owns', render: (p) => chips(p, held.get(p.id) ?? []) },
        ...(mayEdit ? [{ key: 'give', label: 'Give another', render: (p) => giver(p) }] : []),
      ],
      rows: scopable,
      empty: 'Nobody holds a team lead or developer role yet. Set one under Accounts, '
        + 'and they can be given a platform here.',
    }));
  }

  /** What somebody owns, each with a way to take it back. Taking one back
   *  asks first: it moves their change requests out of their bell, and they
   *  may stop being allowed to settle ones they had started on. */
  function chips(person, mine) {
    const box = el('div', 'platform-chips');
    if (!mine.length) box.append(el('span', 'platform-none', 'No platform yet'));
    const who = person.name || person.email;
    for (const s of mine) {
      const chip = el('span', 'platform-chip', s.says);
      if (mayEdit) {
        const drop = el('button', 'platform-drop', '×');
        drop.type = 'button';
        drop.title = `Take back ${s.says}`;
        drop.setAttribute('aria-label', `Take ${s.says} back from ${who}`);
        drop.onclick = async () => {
          const yes = await confirmStep(box, {
            say: `Take ${s.says} back from ${who}? Its change requests stop reaching their bell, `
              + 'and they can no longer settle them.',
            action: 'Take it back',
          });
          if (!yes) return;
          drop.disabled = true;
          try { await revokeScope(s.id); await draw(); onChange?.(); }
          catch (failure) { say(`${who} still owns ${s.says}: ${failure.message}`); drop.disabled = false; }
        };
        chip.append(drop);
      }
      box.append(chip);
    }
    return box;
  }

  /** Side, platform, Give. Giving is not asked twice: it adds to somebody's
   *  bell, and taking it back is one press away in the cell beside it. */
  function giver(person) {
    const who = person.name || person.email;
    const box = el('div', 'platform-give');
    const side = el('select', 'scope-select');
    side.setAttribute('aria-label', `Side to give ${who}`);
    for (const [value, label] of SIDES) side.append(new Option(label, value));
    const where = el('select', 'scope-select');
    where.setAttribute('aria-label', `Platform to give ${who}`);
    // "All platforms" first and selected, because it is the grant that does
    // not go stale: a lead who owns the whole side owns the platform added
    // next month without anybody remembering to come back here.
    where.append(new Option('All platforms', ''));
    for (const p of platforms) where.append(new Option(`${p.code}: ${p.name}`, p.code));
    const add = el('button', 'chip', 'Give');
    add.type = 'button';
    add.setAttribute('aria-label', `Give ${who} the chosen platform`);
    add.onclick = async () => {
      add.disabled = true;
      try { await grantScope(person.id, projectId, side.value, where.value); await draw(); onChange?.(); }
      catch (failure) { say(`${who} was not given it: ${failure.message}`); }
      finally { add.disabled = false; }
    };
    box.append(side, where, add);
    return box;
  }

  await draw();
}
