/**
 * What the delivery has cost, and what the number rests on.
 *
 * **Three facts kept apart, because adding them is how a costing page comes to
 * say something nobody can defend.** Work with no time logged, work whose time
 * this token may not read, and work by somebody with no rate set all reduce the
 * total in different ways and are fixed by different people. The page counts
 * them separately and says the total is a floor rather than an answer.
 *
 * Money is shown to the digit and stored in the smallest unit. A rate of
 * 4,500.50 is 450050 in the store and a float nowhere, because a float rate
 * times a float hour count, summed, is a total that disagrees with itself
 * between two readers of the same page.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const state = { data: null, rates: null, mayEdit: false };

function say(id, message) {
  $(id).textContent = message ?? '';
  $(id).hidden = !message;
}

/** The smallest unit, spelled as money. Intl rather than toFixed, so a lakh
 *  reads as a lakh for somebody in India and as 100,000 elsewhere. */
function money(minor, currency) {
  if (minor == null) return '—';
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency', currency: currency || 'INR', maximumFractionDigits: 0,
    }).format(minor / 100);
  } catch {
    return `${(minor / 100).toFixed(2)} ${currency ?? ''}`.trim();
  }
}

const hours = (n) => (n ? `${n.toFixed(1)} h` : '—');

// ── the headline ─────────────────────────────────────────────────────

function drawStats() {
  const d = state.data ?? {};
  const box = $('ct-stats');
  box.replaceChildren();
  const stat = (value, label, hint, tone) => {
    const card = el('div', `stat-card${tone ? ` ct-stat-${tone}` : ''}`);
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };
  // Said as a floor, not as a total, whenever anything is missing — which on a
  // real project is almost always.
  const short = (d.peopleWithoutRate ?? []).length || d.ticketsHoursUnreadable;
  box.append(stat(
    d.totalCost == null ? '—' : money(d.totalCost, d.currency),
    short ? 'at least' : 'cost so far',
    d.currencies?.length > 1
      ? `${d.currencies.join(' and ')} cannot be added`
      : short ? 'some hours or rates are missing' : 'logged hours × rate',
    short ? 'warn' : ''));
  box.append(stat(hours(d.totalHours ?? 0), 'logged', 'across everybody'));
  box.append(stat((d.people ?? []).filter((p) => p.hours).length, 'people',
    'with time logged'));
  box.append(stat((d.peopleWithoutRate ?? []).length, 'without a rate',
    (d.peopleWithoutRate ?? []).length ? 'their hours cost nothing here' : 'everybody is priced',
    (d.peopleWithoutRate ?? []).length ? 'warn' : ''));
}

function drawPeople() {
  const people = (state.data?.people ?? []).filter((p) => p.hours || p.tickets);
  $('ct-people-count').textContent = people.length ? String(people.length) : '';
  const host = $('ct-people');
  host.replaceChildren();
  if (!people.length) {
    host.append(el('p', 'auth-note auth-fine', 'No tickets in this project yet.'));
    return;
  }
  for (const person of people) {
    const row = el('div', 'admin-row ct-row');
    row.append(el('span', 'account-name', person.person));
    row.append(el('span', 'invite-who',
      `${person.tickets} ticket${person.tickets === 1 ? '' : 's'}`
      + (person.withoutHours ? ` · ${person.withoutHours} with no logged time` : '')));
    row.append(el('span', 'ct-num', hours(person.hours)));
    row.append(el('span', 'ct-num ct-dim',
      person.estimated ? `est ${person.estimated.toFixed(1)} h` : ''));
    row.append(el('span', 'ct-num ct-dim',
      person.hourly == null ? 'no rate' : `${money(person.hourly, person.currency)}/h`));
    const cost = el('span', `ct-cost${person.cost == null && person.hours ? ' ct-missing' : ''}`,
      person.cost == null ? '—' : money(person.cost, person.currency));
    if (person.cost == null && person.hours) {
      cost.title = `${person.person} has logged hours and no rate is set, so none of `
        + 'that time is in the total above.';
    }
    row.append(cost);
    host.append(row);
  }
}

// ── rates ────────────────────────────────────────────────────────────

function drawRates() {
  const rates = state.rates?.rates ?? [];
  $('ct-rates-count').textContent = rates.length ? String(rates.length) : '';
  $('ct-add').hidden = !state.mayEdit;
  $('ct-readonly').hidden = state.mayEdit;

  // The names the tickets actually use, so a rate cannot be typed against
  // somebody OpenProject has never heard of.
  const picker = $('ct-person');
  const seen = (state.data?.people ?? []).map((p) => p.person)
    .filter((n) => n && n !== 'Nobody');
  const priced = new Set(rates.map((r) => r.person.toLowerCase()));
  picker.replaceChildren(...seen.map((name) => {
    const option = el('option', null, priced.has(name.toLowerCase()) ? `${name} (replace)` : name);
    option.value = name;
    return option;
  }));
  if (!seen.length) picker.append(el('option', null, 'nobody has tickets yet'));

  const host = $('ct-rates');
  host.replaceChildren();
  if (!rates.length) {
    host.append(el('p', 'auth-note auth-fine',
      'No rates set. Until one is, the cost above is zero and says so.'));
    return;
  }
  for (const rate of rates) {
    const row = el('div', 'admin-row ct-rate-row');
    row.append(el('span', 'account-name', rate.person));
    row.append(el('span', 'ct-num', `${money(rate.hourly, rate.currency)}/h`));
    row.append(el('span', 'invite-who', rate.note || ''));
    // A rate against a name no ticket uses earns nothing and looks like it
    // does, so it is called out rather than listed as if it were working.
    const used = (state.data?.people ?? [])
      .some((p) => p.person.toLowerCase() === rate.person.toLowerCase());
    row.append(el('span', `ct-num ct-dim${used ? '' : ' ct-missing'}`,
      used ? '' : 'no tickets under this name'));
    if (state.mayEdit) {
      const drop = el('button', 'chip chip-quiet', 'Remove');
      drop.type = 'button';
      drop.onclick = async () => {
        drop.disabled = true;
        try { await auth.dropRate(rate.id); await load(); }
        catch (error) { say('ct-rate-error', error.message); drop.disabled = false; }
      };
      row.append(drop);
    }
    host.append(row);
  }
}

function drawGaps() {
  const d = state.data ?? {};
  const host = $('ct-gaps');
  host.replaceChildren();
  const line = (count, what, why) => {
    const row = el('div', `admin-row ct-gap${count ? '' : ' ct-gap-none'}`);
    row.append(el('span', 'ct-num', String(count)));
    row.append(el('span', 'account-name', what));
    row.append(el('span', 'invite-who', why));
    return row;
  };
  host.append(line(d.ticketsWithoutHours ?? 0, 'tickets with no time logged',
    'Real work with nothing recorded against it costs nothing here.'));
  host.append(line(d.ticketsHoursUnreadable ?? 0, 'tickets whose time this account cannot read',
    'OpenProject only shows logged time to somebody with permission to see time entries. '
    + 'Not the same as nobody having logged any.'));
  host.append(line((d.peopleWithoutRate ?? []).length, 'people with hours and no rate',
    (d.peopleWithoutRate ?? []).join(', ') || 'Everybody with hours has a rate.'));
  if (d.truncated) {
    host.append(line('!', 'more tickets than were read',
      'The project has more work packages than one read returns, so this is a sample.'));
  }
}

// ── loading ──────────────────────────────────────────────────────────

async function load() {
  say('ct-error', '');
  say('ct-rate-error', '');
  try {
    [state.data, state.rates] = await Promise.all([auth.costing(), auth.listRates()]);
  } catch (error) {
    if (error.status === 403) { $('costing').hidden = true; $('denied').hidden = false; return; }
    if (error.status === 428) {
      $('costing').hidden = true;
      $('unconnected').hidden = false;
      $('unconnected-why').textContent = error.message;
      return;
    }
    say('ct-error', error.message);
    return;
  }
  $('costing').hidden = false;
  drawStats();
  drawPeople();
  drawRates();
  drawGaps();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';
  if (!auth.isReader(me)) { $('denied').hidden = false; return; }
  state.mayEdit = auth.isAdmin(me);

  $('ct-refresh').onclick = async () => {
    $('ct-refresh').disabled = true;
    try { state.data = await auth.costing(14, true); drawStats(); drawPeople(); drawGaps(); }
    catch (error) { say('ct-error', error.message); }
    $('ct-refresh').disabled = false;
  };

  $('ct-add').onsubmit = async (event) => {
    event.preventDefault();
    say('ct-rate-error', '');
    // Typed as money, stored as the smallest unit. Rounded here rather than
    // relied on: 45.55 * 100 is 4554.9999999999995 in this language.
    const minor = Math.round(Number($('ct-hourly').value || 0) * 100);
    try {
      await auth.setRate($('ct-person').value, minor, $('ct-currency').value, $('ct-note').value);
      $('ct-hourly').value = '';
      $('ct-note').value = '';
      await load();
    } catch (error) { say('ct-rate-error', error.message); }
  };

  await load();
})();
