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

export async function mountPlatforms() {
  const $ = (id) => document.getElementById(id);
  const host = $('platforms-list');
  if (!host) return;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };
  const error = $('platforms-error');
  const say = (message) => {
    error.textContent = message;
    error.hidden = !message;
  };

  const mayEdit = isOwner(account());
  // Which project, decided by the service rather than by the address. This page
  // names none, and asking for scopes with an empty id is how the service is
  // told "the one this account reads" — so the id comes back with the answer
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
      say(failure.message);
      return;
    }
    // Once, after the project is known. A failure here is survivable: the
    // control falls back to "all platforms" only, and the service validates the
    // shape of anything typed anyway.
    if (platforms === null) platforms = await platformsOf(projectId);

    // Only the roles a slice means anything for. An owner, an admin and a pm
    // are whole rather than scoped, and the service refuses a grant on one —
    // so listing them here would be listing rows whose every control is a 409.
    const scopable = people.filter((p) => ['lead', 'dev'].includes(p.role) && p.active);
    const held = new Map();
    for (const s of scopes) {
      if (!held.has(s.account.id)) held.set(s.account.id, []);
      held.get(s.account.id).push(s);
    }

    host.innerHTML = '';
    if (!scopable.length) {
      host.append(el('p', 'auth-note auth-fine',
        'Nobody holds a team lead or developer role yet. Set one on the Accounts '
        + 'panel above, and they can be given a platform here.'));
      return;
    }

    for (const person of scopable) {
      const row = el('div', 'admin-row platform-row');
      row.append(el('span', 'account-name', person.name || '—'));
      row.append(el('span', 'invite-who', `${person.email} · ${roleLabel(person.role)}`));

      const chips = el('div', 'platform-chips');
      const mine = held.get(person.id) ?? [];
      if (!mine.length) {
        chips.append(el('span', 'platform-none', 'no platforms yet'));
      }
      for (const s of mine) {
        const chip = el('span', 'platform-chip', s.says);
        if (mayEdit) {
          const drop = el('button', 'platform-drop', '×');
          drop.type = 'button';
          drop.title = `Take back ${s.says}`;
          drop.onclick = async () => {
            drop.disabled = true;
            try { await revokeScope(s.id); await draw(); }
            catch (failure) { say(failure.message); drop.disabled = false; }
          };
          chip.append(drop);
        }
        chips.append(chip);
      }
      row.append(chips);

      if (mayEdit) {
        const side = el('select', 'scope-select');
        for (const [value, label] of SIDES) {
          const option = el('option', null, label);
          option.value = value;
          side.append(option);
        }
        const where = el('select', 'scope-select');
        // "All platforms" first and selected, because it is the grant that does
        // not go stale: a lead who owns the whole side owns the platform added
        // next month without anybody remembering to come back here.
        const all = el('option', null, 'All platforms');
        all.value = '';
        where.append(all);
        for (const p of platforms) {
          const option = el('option', null, `${p.code} · ${p.name}`);
          option.value = p.code;
          where.append(option);
        }
        const add = el('button', 'chip', 'Give');
        add.type = 'button';
        add.onclick = async () => {
          add.disabled = true;
          try { await grantScope(person.id, projectId, side.value, where.value); await draw(); }
          catch (failure) { say(failure.message); }
          finally { add.disabled = false; }
        };
        row.append(side, where, add);
      }

      host.append(row);
    }
  }

  await draw();
}
