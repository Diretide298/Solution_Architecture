/**
 * People and projects: who holds an account, which projects they can open,
 * which OpenProject project each ADAM project reads, and the registers out to
 * a spreadsheet and back.
 *
 * **A tool page, so it opens on what needs an administrator rather than on a
 * chart.** There is nothing here to read for its own sake: the page is opened
 * to do something. So the first section is the short list of things waiting
 * for somebody with this page's powers — an invite about to lapse, an account
 * nobody has used in a month, a project reading no work, a developer or team
 * lead with no platform — each naming the section that fixes it, and saying
 * plainly when there is nothing.
 *
 * **Every action that cannot be taken back asks first, in a sentence that
 * names the person and what happens to them.** Disabling an account signs it
 * out of every browser; changing a role changes what somebody may do
 * everywhere; taking a project away stops them opening it. Each of these was
 * one press, and the role picker applied on change, so arrowing through it
 * with the keyboard moved somebody through every role on the way. The second
 * press is `confirmStep`, in a row under the person it is about.
 *
 * Nothing here is the access rule. The service refuses every route on this
 * page to anybody but an administrator, and has to, because a hidden control
 * is still a request away for anybody who opens devtools. Drawing the page
 * only for an administrator is so that nobody is shown a control that will
 * only tell them no.
 */
// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer.
import '/page-chrome.js';
import {
  authState, listAccounts, setAccountActive, setAccountRole,
  createInvite, listInvites, revokeInvite, logoutAccount, makeReset,
  listPmsProjects, availablePmsProjects, setPmsProject, clearPmsProject,
  listScopes, grantProject, revokeProject,
  isAdmin, isOwner, roleLabel, project as currentProject,
} from '/validation.js';
import { attachSubSearch } from '/subsearch.js';
import { mountPanels } from '/panels.js';
import '/theme.js';                      // the saved day/night choice
import { hideLoader } from '/loader.js'; // and the curtain over the wait
import {
  el, fmt, plural, ago, daysSince, verdict, next, table, badge, confirmStep,
  personLink, param, setParams,
} from '/sheet.js';
// The CSV export talks to the service without validation.js, because a file is
// a body to be saved rather than JSON to be read; the reasoning is in its file.
import { mountExport } from '/admin-export.js';
// And its other end: two registers, one machine, two presses.
import { mountDecisions, mountChangeImport } from '/admin-decisions.js';
// Who owns which platform. Reads the package for the platform list, which
// nothing else on this page does.
import { mountPlatforms } from '/admin-platforms.js';

const $ = (id) => document.getElementById(id);

const date = (iso) => {
  if (!iso) return '—';
  const d = new Date(iso);
  return Number.isNaN(+d) ? iso : d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
};
/** Whole days until an ISO time, never negative. */
const daysUntil = (iso) => {
  const t = Date.parse(iso ?? '');
  return Number.isFinite(t) ? Math.max(0, Math.ceil((t - Date.now()) / 86_400_000)) : null;
};
/** Not seen in thirty days, counting from creation for somebody who has never
 *  signed in. */
const isStale = (a) => daysSince(a.last_seen_at ?? a.created_at) >= 30;
const inDays = (n) => (n === 0 ? 'today' : n === 1 ? 'tomorrow' : `in ${n} days`);

/** Every role the service will accept from this page, in the order people are
 *  most often invited as. The System Architect is absent on purpose: the
 *  service refuses that role in both directions, and offering it would be
 *  offering a refusal. It is set on the machine, with
 *  `python -m api.cli owner <address>`. */
const ROLES = ['reviewer', 'dev', 'lead', 'pm', 'admin', 'client'];

/** What a role is for, said under the invite form so nobody has to guess what
 *  "Team Lead" can do before they hand it out. The source is the comment over
 *  ROLES in api/security.py. */
const ROLE_SAYS = {
  reviewer: 'A reviewer records verdicts on the package.',
  dev: 'A developer works their own tickets through ADAM and sees their own agent activity.',
  lead: 'A team lead sees all activity and every change request, and acts on the platforms given to them under Platforms.',
  pm: 'A project manager reads everything an administrator can and writes nothing: no verdicts, no settlements.',
  admin: 'An administrator invites, resets and manages every account and project, as you do.',
  client: '',
};

/** What a change of role does to somebody, for the confirm. Only the moves
 *  with a consequence worth stopping for get a sentence of their own. */
function roleConsequence(from, to) {
  if (to === 'admin') return 'They will be able to invite, reset and disable accounts, and open every project.';
  if (from === 'admin') return 'They lose this page and every project they were not given by name.';
  if (to === 'client') return 'They stop seeing Decisions, and their verdicts count as the client review.';
  if (from === 'client') return 'Their verdicts count as the team’s review from now on.';
  if (to === 'pm') return 'They will read everything and be able to record nothing.';
  return ROLE_SAYS[to] ?? '';
}

const state = {
  me: null,
  accounts: [],
  invites: [],
  projects: [],
  scopes: [],
  // Which of these four reads answered, so "needs you" does not claim a
  // clean bill from a list it never received.
  read: { accounts: false, invites: false, projects: false, scopes: false },
};

// ── where an old link lands ─────────────────────────────────────────
//
// The reviews page links at #close-from-sheet and the changes page at
// #settle-from-sheet, from before the two uploads were one section. Sent to
// that section with the right register picked, before the rail reads the hash.
const LEGACY = {
  'close-from-sheet': ['upload', 'verdicts'],
  'settle-from-sheet': ['upload', 'changes'],
  invite: ['invites'],
  password: ['attention'],
};
function rewriteLegacyHash() {
  const was = location.hash.slice(1);
  const to = LEGACY[was];
  if (!to) return;
  if (to[1]) setParams({ register: to[1] === 'verdicts' ? '' : to[1] });
  history.replaceState(null, '', `${location.pathname}${location.search}#${to[0]}`);
}

// ── the page ────────────────────────────────────────────────────────

const signedIn = await authState().catch(() => null);
if (!signedIn || !signedIn.signedIn) {
  // Lowered before the navigation, not after: a curtain left up over a
  // redirect reads as the redirect having stalled.
  hideLoader();
  location.href = `/login.html?next=${encodeURIComponent('/admin.html')}`;
} else if (!isAdmin(signedIn.account)) {
  $('denied').hidden = false;
  $('whoami').textContent = signedIn.account.email;
  hideLoader();
} else {
  state.me = signedIn.account;
  // The role, not the word "admin": a System Architect reading this page is
  // not an admin and should not be told they are.
  $('whoami').textContent = `${state.me.name || state.me.email} · ${roleLabel(state.me.role)}`;
  $('admin').hidden = false;
  rewriteLegacyHash();
  addEventListener('hashchange', rewriteLegacyHash);
  mountPanels({ nav: document.querySelector('#admin .set-nav'), fallback: 'attention' });

  // Wired before the lists are fetched, because none of them needs a list:
  // each asks the service for its own rows when it is pressed.
  mountExport();
  mountDecisions();
  mountChangeImport();
  mountRegisterPicker();
  mountInviteForm();
  $('platforms-readonly').hidden = isOwner(state.me);
  // Reads on its own and redraws itself; told when a grant changes, so the
  // "needs you" list can stop naming somebody who now holds a platform.
  mountPlatforms({ me: state.me, onChange: () => refreshScopes() });

  attachSubSearch(
    $('subsearch'),
    [{ box: $('accounts'), rows: '.account-row' }],
    { count: $('subsearch-count'), noun: 'accounts', onEmpty: 'No account matches that. Clear the box to see everybody.' },
  );

  // allSettled rather than all, so one failing still shows the page it failed
  // on rather than leaving the curtain up over it. The projects wait on
  // nothing slow themselves (the OpenProject choices are read after), so they
  // are part of the first draw.
  Promise.allSettled([refreshInvites(), refreshAccounts(), refreshProjects(), refreshScopes()])
    .then(() => { drawAttention(); hideLoader(); });
}

// ── needs you ───────────────────────────────────────────────────────

function drawAttention() {
  const { accounts, invites, projects, scopes, read } = state;
  const needs = [];

  // An open invite that lapses inside a week. Somebody was expected and has
  // not arrived; once it lapses the link is dead and they have to ask again.
  const soon = invites.filter((i) => i.state === 'open' && daysUntil(i.expires_at) <= 7)
    .sort((a, b) => Date.parse(a.expires_at) - Date.parse(b.expires_at));
  if (soon.length) {
    needs.push({
      section: 'invites', go: 'Invite someone',
      says: `${plural(soon.length, 'invite')} ${soon.length === 1 ? 'lapses' : 'lapse'} this week: `
        + soon.map((i) => `${i.email} ${inDays(daysUntil(i.expires_at))}`).join(', ') + '.',
      next: `Check ${soon[0].email} has their link before it lapses ${inDays(daysUntil(soon[0].expires_at))}; make another if it was lost.`,
    });
  }

  // An active account nobody has used in thirty days. Either somebody has
  // left and still has a way in, or somebody never got started.
  // Never signed in counts from the day the account was made: an account
  // redeemed yesterday has not gone quiet, it has not started yet.
  const stale = accounts.filter((a) => a.active && a.id !== state.me.id && isStale(a));
  if (stale.length) {
    const never = stale.filter((a) => !a.last_seen_at).length;
    needs.push({
      section: 'people', go: 'Accounts',
      says: `${plural(stale.length, 'active account')} not seen in 30 days or more`
        + `${never ? ` (${fmt(never)} never signed in)` : ''}: `
        + stale.slice(0, 5).map((a) => a.name || a.email).join(', ')
        + (stale.length > 5 ? `, and ${fmt(stale.length - 5)} more` : '') + '.',
      next: 'Disable the accounts of anybody who has left; the verdicts they gave keep their name.',
    });
  }

  // A project that reads no OpenProject project shows no work at all, which
  // looks like an empty project rather than an unconnected one.
  const unmapped = projects.filter((p) => p.active && !p.openproject);
  if (unmapped.length) {
    needs.push({
      section: 'projects', go: 'Projects',
      says: `${unmapped.map((p) => p.name || p.id).join(', ')} ${unmapped.length === 1 ? 'reads' : 'read'} `
        + 'no OpenProject project, so '
        + `${unmapped.length === 1 ? 'its boards are' : 'their boards are'} empty.`,
      next: `Choose the OpenProject project ${unmapped[0].name || unmapped[0].id} reads.`,
    });
  }

  // A developer or team lead with no platform gets no change request in
  // their bell and may settle none, which nobody notices until one is missed.
  const holders = new Set(scopes.map((s) => s.account?.id));
  const bare = accounts.filter((a) => a.active && ['dev', 'lead'].includes(a.role) && !holders.has(a.id));
  if (read.scopes && bare.length) {
    needs.push({
      section: 'platforms', go: 'Platforms',
      says: `${plural(bare.length, 'developer or team lead', 'developers and team leads')} `
        + `${bare.length === 1 ? 'holds' : 'hold'} no platform: `
        + bare.slice(0, 5).map((a) => a.name || a.email).join(', ')
        + (bare.length > 5 ? `, and ${fmt(bare.length - 5)} more` : '') + '. '
        + 'No change request reaches their bell.',
      next: isOwner(state.me)
        ? `Give ${bare[0].name || bare[0].email} a platform.`
        : `Ask the System Architect to give ${bare[0].name || bare[0].email} a platform; only they hand them out.`,
    });
  }

  const missing = Object.entries(read).filter(([, ok]) => !ok).map(([what]) => what);
  const live = accounts.filter((a) => a.active).length;
  const open = invites.filter((i) => i.state === 'open').length;
  const mapped = projects.filter((p) => p.active && p.openproject).length;
  const activeProjects = projects.filter((p) => p.active).length;
  const scopable = accounts.filter((a) => a.active && ['dev', 'lead'].includes(a.role));

  verdict($('ad-verdict'), {
    when: 'What is waiting for an administrator',
    headline: needs.length
      ? `${plural(needs.length, 'thing')} ${needs.length === 1 ? 'needs' : 'need'} you.`
      : missing.length ? 'Nothing that could be read needs you.' : 'Nothing needs you.',
    headlineId: 'ad-headline',
    pace: needs.length
      ? 'Each one names the section where it is dealt with.'
      : missing.length
        ? `The ${missing.join(' and ')} could not be read, so this is not the whole answer. Reload the page to try again.`
        : 'No invite lapses this week, everybody active has signed in this month, every project '
          + 'reads OpenProject and every developer and team lead holds a platform.',
    ledger: [
      { label: 'Active accounts', value: `${fmt(live)}`, unit: `of ${fmt(accounts.length)}` },
      { label: 'Open invites', value: open },
      { label: 'Projects reading OpenProject', value: `${fmt(mapped)}`, unit: `of ${fmt(activeProjects)}`, bad: mapped < activeProjects },
      ...(read.scopes ? [{
        label: 'Developers and leads with a platform',
        value: `${fmt(scopable.length - bare.length)}`, unit: `of ${fmt(scopable.length)}`,
      }] : []),
    ],
  });

  const list = $('ad-needs');
  list.replaceChildren();
  for (const need of needs) {
    const li = el('li', 'ad-need');
    li.append(el('span', 'ad-need-says', need.says));
    const go = el('a', 'sh-link ad-need-go', need.go);
    go.href = `#${need.section}`;
    li.append(go);
    list.append(li);
  }
  list.hidden = !needs.length;
  next($('ad-next'), needs[0]?.next ?? '');
}

// ── accounts ────────────────────────────────────────────────────────

async function refreshAccounts() {
  const box = $('accounts');
  try {
    ({ accounts: state.accounts } = await listAccounts());
    state.read.accounts = true;
  } catch (error) {
    state.read.accounts = false;
    box.replaceChildren(el('p', 'auth-error', `Could not read the accounts: ${error.message}. Reload the page to try again.`));
    return;
  }
  drawAccounts();
}

/** One detail row under a person's row, for a confirm, a link or a result.
 *  One at a time per person: opening a second replaces the first, so a row
 *  never carries two questions at once. */
function detailRow(tr, columns) {
  const below = tr.nextElementSibling;
  if (below?.classList.contains('ad-detail')) below.remove();
  const row = el('tr', 'ad-detail');
  const td = el('td');
  td.colSpan = columns;
  row.append(td);
  tr.after(row);
  return { row, td };
}

/** Ask, under the row, and resolve true or false. The strip says what will
 *  happen in a sentence that names the person; the button says the action. */
async function askUnder(tr, columns, say, action) {
  const { row, td } = detailRow(tr, columns);
  const anchor = el('span', 'ad-anchor');
  td.append(anchor);
  const yes = await confirmStep(anchor, { say, action });
  row.remove();
  return yes;
}

/** A sentence under the row afterwards: what happened, in the row it
 *  happened to. */
function sayUnder(tr, columns, nodes) {
  const { td } = detailRow(tr, columns);
  const p = el('p', 'ad-said');
  p.append(...[].concat(nodes));
  td.append(p);
  return td;
}

function accountError(message) {
  $('account-error').textContent = message ?? '';
  $('account-error').hidden = !message;
}

function drawAccounts() {
  const { accounts, me } = state;
  const live = accounts.filter((a) => a.active).length;
  $('account-count').textContent = `${fmt(live)} active of ${fmt(accounts.length)}`;
  const openProjects = state.projects.filter((p) => p.active);
  const COLS = 7;
  const nameOf = (p) => p.name || p.email;

  $('accounts').replaceChildren(table({
    caption: 'Every account, oldest first. A name opens that person on Tasks.',
    rowClass: (p) => `account-row${p.active ? '' : ' disabled'}`,
    columns: [
      {
        key: 'name', label: 'Person', sort: (p) => nameOf(p).toLowerCase(),
        render: (p) => {
          const cell = el('span', 'ad-person');
          cell.append(p.name ? personLink(p.name) : el('span', '', p.email));
          if (p.id === me.id) cell.append(el('span', 'sh-quiet', ' (you)'));
          // A break offered at the @, so a long address wraps between its two
          // halves rather than wherever the column runs out.
          const email = el('span', 'ad-email');
          const at = p.email.indexOf('@');
          if (at > 0) email.append(p.email.slice(0, at), document.createElement('wbr'), p.email.slice(at));
          else email.textContent = p.email;
          cell.append(email);
          if (!p.active) cell.append(badge('quiet', 'Disabled'));
          return cell;
        },
      },
      { key: 'role', label: 'Role', sort: (p) => roleLabel(p.role), render: (p) => roleControl(p) },
      { key: 'projects', label: 'Projects', render: (p) => projectsControl(p, openProjects, COLS) },
      {
        key: 'last_seen_at', label: 'Last seen', nowrap: true,
        sort: (p) => p.last_seen_at ?? '',
        cellClass: (p) => (p.active && isStale(p) ? 'ad-stale' : ''),
        render: (p) => {
          const span = el('span', '', p.last_seen_at ? ago(p.last_seen_at) : 'never');
          if (p.last_seen_at) span.title = new Date(p.last_seen_at).toLocaleString('en-GB');
          return span;
        },
      },
      { key: 'created_at', label: 'Created', nowrap: true, sort: (p) => p.created_at ?? '', render: (p) => date(p.created_at) },
      { key: 'verdicts', label: 'Verdicts', num: true, sort: (p) => p.verdicts },
      { key: 'actions', label: 'Actions', render: (p) => actionsControl(p, COLS) },
    ],
    rows: accounts,
    empty: 'No accounts yet. Invite somebody from Invite someone.',
  }));
}

/**
 * The role, as a picker that asks before it acts.
 *
 * It used to apply on change, which made the keyboard a hazard: arrowing
 * through a focused select fires `change` at every option, so looking at the
 * choices moved somebody through all of them. Now a change opens the
 * confirm under the row, naming the person, the role they hold and the one
 * picked, and Cancel puts the picker back.
 */
function roleControl(person) {
  const role = el('select', 'scope-select ad-role');
  role.setAttribute('aria-label', `Role for ${person.name || person.email}`);
  // Each option's words in `label` rather than in its text. The account filter
  // matches on a row's text, and a select's text is every option it has, so
  // "Admin" in the filter matched every row. The role held is said once,
  // out of sight, for the filter alone.
  const option = (value) => {
    const o = new Option('', value, false, person.role === value);
    o.label = roleLabel(value);
    return o;
  };
  for (const value of ROLES) role.append(option(value));
  // The System Architect's row shows the role and offers nothing, rather than
  // a picker whose every option is a 403.
  if (isOwner(person)) role.replaceChildren(option('owner'));
  role.disabled = person.id === state.me.id || isOwner(person);
  if (role.disabled) role.title = person.id === state.me.id
    ? 'Your own role is changed by another administrator.'
    : 'The System Architect is set on the machine, not here.';
  role.onchange = async () => {
    const tr = role.closest('tr');
    const to = role.value;
    const who = person.name || person.email;
    const yes = await askUnder(tr, 7,
      `Change ${who} from ${roleLabel(person.role)} to ${roleLabel(to)}? ${roleConsequence(person.role, to)}`,
      `Make them ${roleLabel(to)}`);
    if (!yes) { role.value = person.role; return; }
    accountError('');
    try {
      await setAccountRole(person.id, to);
    } catch (error) {
      accountError(`${who} is still ${roleLabel(person.role)}: ${error.message}`);
      role.value = person.role;
      return;
    }
    await refreshAccounts();
    drawAttention();
  };
  const cell = el('span', 'ad-role-cell');
  const words = el('span', 'sh-sr', roleLabel(person.role));
  words.setAttribute('aria-hidden', 'true');
  cell.append(role, words);
  return cell;
}

/** The projects somebody can open: each one with a way to take it away, and
 *  a picker to give another. An administrator opens every project whatever
 *  is stored, so their cell says that instead of offering controls that would
 *  change nothing. */
function projectsControl(person, openProjects, cols) {
  const cell = el('div', 'ad-projects');
  if (isAdmin(person)) {
    cell.append(el('span', 'sh-quiet', 'Every project'));
    return cell;
  }
  const who = person.name || person.email;
  const held = person.projects ?? [];
  if (!held.length) cell.append(el('span', 'ad-none', 'None: they can open nothing'));
  for (const p of held) {
    const chip = el('span', 'ad-chip', p.name || p.id);
    const drop = el('button', 'ad-chip-drop', '×');
    drop.type = 'button';
    drop.setAttribute('aria-label', `Take ${p.name || p.id} away from ${who}`);
    drop.title = `Take ${p.name || p.id} away`;
    drop.onclick = async () => {
      const tr = drop.closest('tr');
      const last = held.length === 1;
      const yes = await askUnder(tr, cols,
        `Take ${p.name || p.id} away from ${who}? They stop being able to open it; what they recorded on it keeps their name.`
        + (last ? ' It is the only project they can open, so they will see nothing until given another.' : ''),
        `Take ${p.name || p.id} away`);
      if (!yes) return;
      accountError('');
      try { await revokeProject(person.id, p.id); }
      catch (error) { accountError(`${who} can still open ${p.name || p.id}: ${error.message}`); return; }
      await refreshAccounts();
    };
    chip.append(drop);
    cell.append(chip);
  }
  // Giving opens under the row rather than sitting in it: a picker in every
  // row is a second column of controls, and its options are words the
  // account filter would match on every row at once.
  const left = openProjects.filter((o) => !held.some((h) => h.id === o.id));
  if (left.length && person.active) {
    const add = el('button', 'ad-add', 'Add a project');
    add.type = 'button';
    add.setAttribute('aria-label', `Give ${who} another project`);
    add.onclick = () => {
      const tr = add.closest('tr');
      const { row, td } = detailRow(tr, cols);
      const form = el('div', 'ad-give');
      const label = el('label', 'sh-field-inline');
      const pick = el('select', 'scope-select ad-give-pick');
      for (const o of left) pick.append(new Option(o.name || o.id, o.id));
      label.append(`Give ${who}`, pick);
      const go = el('button', 'chip', 'Give it');
      go.type = 'button';
      const cancel = el('button', 'chip', 'Cancel');
      cancel.type = 'button';
      cancel.onclick = () => { row.remove(); add.focus(); };
      go.onclick = async () => {
        go.disabled = true;
        accountError('');
        const name = pick.selectedOptions[0]?.textContent ?? pick.value;
        try { await grantProject(person.id, pick.value); }
        catch (error) { accountError(`${who} was not given ${name}: ${error.message}`); go.disabled = false; return; }
        await refreshAccounts();
      };
      form.append(label, go, cancel);
      if (person.role === 'client') form.append(el('span', 'sh-quiet', 'They see it as a client, as they do everywhere.'));
      td.append(form);
      pick.focus();
    };
    cell.append(add);
  }
  return cell;
}

/** "The 3 verdicts they gave keep their name. ", or nothing for somebody who
 *  has given none: "the 0 verdicts" is a sentence about nothing. */
const kept = (person) => (!person.verdicts ? ''
  : person.verdicts === 1 ? 'The verdict they gave keeps their name. '
    : `The ${fmt(person.verdicts)} verdicts they gave keep their name. `);

/** Reset password, End sessions and Disable or Enable, in that order: the
 *  cheap ones first, and the one that takes an account away last. */
function actionsControl(person, cols) {
  const cell = el('div', 'ad-actions');
  const who = person.name || person.email;
  const me = person.id === state.me.id;

  // Shown for every row including your own: losing your own password is the
  // ordinary case, and a second administrator making you a link is exactly
  // the route the sign-in page tells people to ask for. The administrator
  // never learns the password; the person chooses it behind the link.
  const reset = el('button', 'chip', 'Reset password');
  reset.type = 'button';
  reset.title = 'Make a link that lets them set a new password';
  reset.onclick = async () => {
    reset.disabled = true;
    accountError('');
    try {
      const made = await makeReset(person.id);
      // Joined to this page's own origin rather than sent whole by the
      // service, which is reachable on more than one name.
      const url = `${location.origin}${made.link}`;
      const td = sayUnder(reset.closest('tr'), cols, []);
      td.replaceChildren();
      const box = el('div', 'account-reset-link');
      const field = el('input', 'auth-input');
      field.readOnly = true;
      field.value = url;
      field.setAttribute('aria-label', `Password reset link for ${who}`);
      const copy = el('button', 'chip', 'Copy');
      copy.type = 'button';
      copy.onclick = async () => {
        field.select();
        try { await navigator.clipboard.writeText(url); copy.textContent = 'Copied'; }
        catch { copy.textContent = 'Press Ctrl+C'; }
        setTimeout(() => { copy.textContent = 'Copy'; }, 1600);
      };
      box.append(field, copy, el('p', 'sh-quiet',
        `Send this to ${person.email} however you already talk to them. It works once, expires in a day, `
        + 'and ends every session they have open when they use it. Making another link withdraws this one.'));
      td.append(box);
    } catch (error) {
      accountError(`No link was made for ${who}: ${error.message}`);
    } finally {
      reset.disabled = false;
    }
  };
  cell.append(reset);

  // Your own row gets neither of the other two. Ending your own sessions from
  // here would take the session this page runs on without clearing its cookie,
  // and the service refuses disabling yourself.
  if (me) return cell;

  const end = el('button', 'chip', 'End sessions');
  end.type = 'button';
  end.title = 'Sign them out of every browser, without touching the account';
  end.onclick = async () => {
    const tr = end.closest('tr');
    const yes = await askUnder(tr, cols,
      `Sign ${who} out of every browser and device? The account stays enabled, so they can sign straight `
      + `back in. ${kept(person)}This is not Disable.`,
      'End their sessions');
    if (!yes) return;
    accountError('');
    try {
      const { dropped } = await logoutAccount(person.id);
      sayUnder(tr, cols, dropped
        ? `Ended ${plural(dropped, 'session')} for ${who}. The account is untouched.`
        : `${who} had no sessions open. Nothing was ended.`);
    } catch (error) {
      accountError(`${who}'s sessions were not ended: ${error.message}`);
    }
  };
  cell.append(end);

  // The System Architect is not disabled from here (the service refuses it,
  // and says to use the CLI), so the row does not offer it.
  if (isOwner(person)) return cell;

  const toggle = el('button', `chip${person.active ? ' ad-danger' : ''}`, person.active ? 'Disable' : 'Enable');
  toggle.type = 'button';
  toggle.onclick = async () => {
    const tr = toggle.closest('tr');
    if (person.active) {
      // Disabling drops every session as well as the next sign-in, which is
      // why it asks and End sessions is the cheaper control beside it.
      const yes = await askUnder(tr, cols,
        `Disable ${who}? They are signed out of every browser now and cannot sign in again until an `
        + `administrator enables the account. ${kept(person)}`.trim(),
        `Disable ${who}`);
      if (!yes) return;
    }
    toggle.disabled = true;
    accountError('');
    try { await setAccountActive(person.id, !person.active); }
    catch (error) {
      accountError(`${who} was not ${person.active ? 'disabled' : 'enabled'}: ${error.message}`);
      toggle.disabled = false;
      return;
    }
    await refreshAccounts();
    drawAttention();
  };
  cell.append(toggle);
  return cell;
}

// ── invites ─────────────────────────────────────────────────────────

/** An invite's state as a word and the state colour it means: open is in
 *  progress, used is done, lapsed is late, withdrawn is struck through. */
const INVITE_STATE = {
  open: ['going', 'Open'],
  redeemed: ['done', 'Used'],
  expired: ['late', 'Lapsed'],
  revoked: ['quiet', 'Withdrawn'],
};

async function refreshInvites() {
  const box = $('invites-list');
  try {
    ({ invites: state.invites } = await listInvites());
    state.read.invites = true;
  } catch (error) {
    state.read.invites = false;
    box.replaceChildren(el('p', 'auth-error', `Could not read the invites: ${error.message}. Reload the page to try again.`));
    return;
  }
  const { invites } = state;
  const open = invites.filter((i) => i.state === 'open').length;
  $('invite-count').textContent = invites.length ? `${fmt(open)} open of ${fmt(invites.length)}` : '';
  box.replaceChildren(table({
    caption: 'Every invite, newest first',
    rowClass: (i) => `invite-row-item ${i.state}`,
    columns: [
      { key: 'email', label: 'Address', render: (i) => el('span', 'ad-email-strong', i.email) },
      {
        key: 'state', label: 'State',
        render: (i) => { const [kind, word] = INVITE_STATE[i.state] ?? ['fresh', i.state]; return badge(kind, word); },
      },
      { key: 'role', label: 'Role', render: (i) => roleLabel(i.role) },
      { key: 'project', label: 'Project', render: (i) => i.project_name || i.project_id || '—' },
      {
        key: 'when', label: 'When', nowrap: true,
        render: (i) => (i.state === 'open'
          ? `lapses ${inDays(daysUntil(i.expires_at))}`
          : i.redeemed_at ? `used ${date(i.redeemed_at)}`
            : i.revoked_at ? `withdrawn ${date(i.revoked_at)}`
              : `lapsed ${date(i.expires_at)}`),
      },
      {
        key: 'act', label: 'Actions',
        render: (i) => {
          if (i.state !== 'open') return '';
          const revoke = el('button', 'chip', 'Withdraw');
          revoke.type = 'button';
          revoke.setAttribute('aria-label', `Withdraw the invite to ${i.email}`);
          revoke.onclick = async () => {
            const yes = await askUnder(revoke.closest('tr'), 6,
              `Withdraw the invite to ${i.email}? The link stops working at once. You can make another.`,
              'Withdraw it');
            if (!yes) return;
            revoke.disabled = true;
            try { await revokeInvite(i.id); }
            catch (error) { $('invite-error').textContent = `The invite to ${i.email} was not withdrawn: ${error.message}`; $('invite-error').hidden = false; }
            await refreshInvites();
            drawAttention();
          };
          return revoke;
        },
      },
    ],
    rows: invites,
    empty: 'Nobody has been invited yet. Make a link with the form above.',
  }));
}

function mountInviteForm() {
  const role = $('invite-role');
  for (const value of ROLES) role.append(new Option(roleLabel(value), value));
  role.value = 'reviewer';
  // The placeholder and the note follow the role, because the address rule is
  // the thing that changes and an @softlabsgroup.com placeholder above a
  // client invite reads as a refusal waiting to happen.
  const follow = () => {
    const client = role.value === 'client';
    $('invite-client-note').hidden = !client;
    $('invite-email').placeholder = client ? 'them@theircompany.com' : 'them@softlabsgroup.com';
    $('invite-role-note').textContent = ROLE_SAYS[role.value] ?? '';
    $('invite-role-note').hidden = client || !ROLE_SAYS[role.value];
  };
  role.onchange = follow;
  follow();

  $('invite-create').onclick = async () => {
    $('invite-error').hidden = true;
    $('invite-result').hidden = true;
    const email = $('invite-email').value.trim();
    if (!email) {
      $('invite-error').textContent = 'Type their e-mail address first.';
      $('invite-error').hidden = false;
      $('invite-email').focus();
      return;
    }
    $('invite-create').disabled = true;
    try {
      const invite = await createInvite(email, role.value, Number($('invite-days').value), $('invite-project').value);
      $('invite-link').value = `${location.origin}${invite.link}`;
      $('invite-result').hidden = false;
      $('invite-email').value = '';
      await refreshInvites();
      drawAttention();
    } catch (error) {
      $('invite-error').textContent = `No link was made: ${error.message}`;
      $('invite-error').hidden = false;
    } finally {
      $('invite-create').disabled = false;
    }
  };

  $('invite-copy').onclick = async () => {
    $('invite-link').select();
    try {
      await navigator.clipboard.writeText($('invite-link').value);
      $('invite-copy').textContent = 'Copied';
    } catch {
      $('invite-copy').textContent = 'Press Ctrl+C';
    }
    setTimeout(() => { $('invite-copy').textContent = 'Copy'; }, 1600);
  };
}

/** The invite form's project picker. Open projects only; the choice made
 *  before a refresh is kept. */
function fillInviteProjects(projects) {
  const pick = $('invite-project');
  const was = pick.value;
  pick.replaceChildren();
  const open = projects.filter((p) => p.active);
  for (const project of open) pick.append(new Option(project.name || project.id, project.id));
  // Otherwise the project the rest of ADAM is reading, or failing that the
  // first one that reads any work; alphabetical order put a demo first.
  const reading = currentProject();
  const fallback = open.find((p) => p.id === reading) ?? open.find((p) => p.openproject) ?? open[0];
  pick.value = was && open.some((p) => p.id === was) ? was : (fallback?.id ?? '');
}

// ── projects ────────────────────────────────────────────────────────

function projectSay(id, text) {
  $(id).textContent = text;
  $(id).hidden = !text;
}

async function refreshProjects() {
  const box = $('projects-list');
  projectSay('project-error', '');
  try {
    ({ projects: state.projects } = await listPmsProjects());
    state.read.projects = true;
  } catch (error) {
    state.read.projects = false;
    box.replaceChildren(el('p', 'auth-error', `Could not read the projects: ${error.message}. Reload the page to try again.`));
    return;
  }
  const { projects } = state;
  fillInviteProjects(projects);
  if (state.read.accounts) drawAccounts();
  const chosen = projects.filter((p) => p.openproject).length;
  $('project-count').textContent = `${fmt(chosen)} of ${fmt(projects.length)} reading OpenProject`;
  drawProjects(null);
  // The choices come from OpenProject, which is slower than this service and
  // may refuse; the rows are drawn first and the pickers join them after. A
  // missing token is a thing to go and fix, not a failure.
  availablePmsProjects()
    .then(({ projects: options }) => drawProjects(options))
    .catch((error) => projectSay('project-error', error.status === 428
      ? 'Store your OpenProject token on your settings page to choose projects here.'
      : `Could not read the OpenProject projects: ${error.message}. The rows show what is chosen today.`));
}

function drawProjects(options) {
  const COLS = 4;
  $('projects-list').replaceChildren(table({
    caption: 'Every ADAM project and the OpenProject project it reads',
    rowClass: (p) => `project-row${p.active ? '' : ' disabled'}`,
    columns: [
      {
        key: 'name', label: 'ADAM project',
        render: (p) => { const s = el('span', 'ad-person'); s.append(el('b', '', p.name || p.id), el('span', 'ad-email', p.id)); return s; },
      },
      {
        key: 'openproject', label: 'Reads',
        render: (p) => {
          if (!p.openproject) return badge('stalled', 'Nothing chosen');
          const a = el('a', 'sh-link', `${p.openproject.name} (${p.openproject.identifier})`);
          a.href = p.openproject.url;
          a.target = '_blank';
          a.rel = 'noopener';
          return a;
        },
      },
      {
        key: 'set', label: 'Chosen',
        // The startup migration fills in TICVAI's first choice with a time and
        // nobody's name; a project nobody has ever chosen for has neither.
        render: (p) => (!p.setAt ? el('span', 'sh-quiet', 'never')
          : p.setBy ? `${date(p.setAt)} by ${p.setBy}` : `${date(p.setAt)}, when ADAM was first set up`),
      },
      { key: 'change', label: 'Change', render: (p) => projectControl(p, options, COLS) },
    ],
    rows: state.projects,
    empty: 'No ADAM projects exist yet.',
  }));
}

function projectControl(project, options, cols) {
  const cell = el('div', 'ad-actions');
  const name = project.name || project.id;
  if (options) {
    const pick = el('select', 'scope-select ad-project-pick');
    pick.setAttribute('aria-label', `OpenProject project for ${name}`);
    pick.append(new Option('Choose an OpenProject project', ''));
    for (const option of options) {
      pick.append(new Option(`${option.name} (${option.identifier})`, String(option.id), false, option.id === project.openproject?.id));
    }
    const save = el('button', 'chip', 'Save');
    save.type = 'button';
    save.setAttribute('aria-label', `Save the OpenProject project for ${name}`);
    save.onclick = async () => {
      if (!pick.value) { projectSay('project-error', `Choose an OpenProject project for ${name} first.`); return; }
      save.disabled = true;
      projectSay('project-error', ''); projectSay('project-ok', '');
      try {
        const { project: saved } = await setPmsProject(project.id, Number(pick.value));
        projectSay('project-ok', `${saved.name || saved.id} now reads ${saved.openproject.name}.`);
        await refreshProjects();
        drawAttention();
      } catch (error) {
        projectSay('project-error', `${name} was not changed: ${error.message}`);
        save.disabled = false;
      }
    };
    cell.append(pick, save);
  }
  if (project.openproject) {
    const clear = el('button', 'chip ad-danger', 'Clear');
    clear.type = 'button';
    clear.setAttribute('aria-label', `Stop ${name} reading OpenProject`);
    clear.onclick = async () => {
      const yes = await askUnder(clear.closest('tr'), cols,
        `Stop ${name} reading ${project.openproject.name}? Every board and ticket lookup on it goes empty until a project is chosen again.`,
        `Stop ${name} reading it`);
      if (!yes) return;
      try {
        await clearPmsProject(project.id);
        projectSay('project-ok', `${name} reads no OpenProject project now.`);
      } catch (error) {
        projectSay('project-error', `${name} still reads ${project.openproject.name}: ${error.message}`);
      }
      await refreshProjects();
      drawAttention();
    };
    cell.append(clear);
  }
  return cell;
}

// ── platforms, for the "needs you" list ─────────────────────────────

async function refreshScopes() {
  try {
    ({ scopes: state.scopes } = await listScopes(''));
    state.read.scopes = true;
  } catch {
    state.read.scopes = false;
  }
  if (state.read.accounts) drawAttention();
}

// ── which register a sheet is from ──────────────────────────────────

/** The two uploads share a section, and this picks which one is showing. In
 *  the address as `?register=changes`, so the changes page's link opens on
 *  its own register. Pressed is the one in force. */
function mountRegisterPicker() {
  const buttons = [...document.querySelectorAll('#upload [data-register]')].filter((b) => b.tagName === 'BUTTON');
  const panels = [...document.querySelectorAll('#upload .ad-register-panel')];
  const show = (which) => {
    for (const b of buttons) b.setAttribute('aria-pressed', String(b.dataset.register === which));
    for (const p of panels) p.hidden = p.dataset.register !== which;
  };
  for (const b of buttons) {
    b.onclick = () => {
      setParams({ register: b.dataset.register === 'verdicts' ? '' : b.dataset.register });
      show(b.dataset.register);
    };
  }
  show(param('register') === 'changes' ? 'changes' : 'verdicts');
  addEventListener('hashchange', () => show(param('register') === 'changes' ? 'changes' : 'verdicts'));
}
