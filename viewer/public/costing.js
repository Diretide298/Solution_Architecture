/**
 * What the delivery has cost, against what it was given, and where the pace
 * so far takes it.
 *
 * **The page opens on one sentence**: how much of the budget is spent by the
 * sprint under way, and where the spend ends up at the end of the last sprint
 * if the pace holds. Everything under it is what that sentence rests on: the
 * figures as a line of type, the cost by sprint against the budget line, and
 * then, down the rail, the people, the sprints, and the three things an
 * administrator configures here (the budget, the rates, the default rate).
 *
 * **Three facts kept apart, because adding them is how a costing page comes to
 * say something nobody can defend.** Work with no time logged, work whose time
 * this token may not read, and work by somebody with no rate set all reduce the
 * total in different ways and are fixed by different people. The page counts
 * them separately (What is missing) and says the total is a floor whenever any
 * of them is not zero.
 *
 * Money is shown to the unit and kept in the smallest unit. A rate of 4,500.50
 * is 450050 in the store and a float nowhere; all the sums are the service's,
 * in integers, and this file only divides by a hundred to print. The one
 * exception is the chart's scale, which is a picture and not a figure.
 */

import '/page-chrome.js';
import * as auth from '/validation.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, param, personLink, verdict, next, mountScope, badge, table, confirmStep,
} from '/sheet.js';

const $ = (id) => document.getElementById(id);
const SVG = 'http://www.w3.org/2000/svg';
const svg = (tag, attrs = {}, text) => {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (text !== undefined) node.textContent = text;
  return node;
};
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const state = {
  project: '',
  me: null,
  mayEdit: false,
  data: null,       // /api/costing, for the current filter
  rates: null,      // /api/rates
  budgets: null,    // /api/budget
  scope: null,      // mountScope's handle, once the facets are known
  receivedAt: 0,
  loading: 0,       // which load is the latest; an older answer is dropped
  error: '',
};

// ── money and hours ──────────────────────────────────────────────────

/** The smallest unit, spelled as money. Rupees are grouped the Indian way
 *  (₹32,97,950) whatever the browser's language, because the people reading
 *  rupees here read lakhs; other currencies follow the browser. */
function money(minor, currency, { compact = false, exact = false } = {}) {
  if (minor == null || !currency) return '—';
  try {
    return new Intl.NumberFormat(currency === 'INR' ? 'en-IN' : undefined, {
      style: 'currency', currency,
      ...(compact ? { notation: 'compact', maximumFractionDigits: 1 }
        : { minimumFractionDigits: 0, maximumFractionDigits: exact ? 2 : 0 }),
    }).format(minor / 100);
  } catch {
    return `${currency} ${fmt(Math.round(minor / 100))}`;
  }
}
const perHour = (minor, currency) => `${money(minor, currency, { exact: true })} an hour`;
const hoursOf = (h) => (h ? `${h.toLocaleString('en-IN', { maximumFractionDigits: 1 })} h` : '—');
const shortDate = (iso) => (iso ? new Date(`${iso.slice(0, 10)}T00:00:00`).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) : '');
const when = (iso) => {
  const d = new Date(iso);
  return Number.isNaN(+d) ? '' : `${d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}, ${d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}`;
};

function say(id, message) {
  $(id).textContent = message ?? '';
  $(id).hidden = !message;
}

/** A link to one of the rail's sections, which switches to it. */
function sectionLink(hash, text) {
  const a = el('a', 'sh-link', text);
  a.href = `#${hash}`;
  return a;
}

// ── what the filter is ───────────────────────────────────────────────

/** Before the facets arrive the filter is only the address, which is what
 *  the first read is asked with; after, it is the mounted filter's state. */
const filter = () => (state.scope?.state
  ?? { person: param('person'), sprint: param('sprint'), type: param('type') });
const filtered = () => Object.values(filter()).some(Boolean);

function filterSays(f) {
  if (!f.person && !f.sprint && !f.type) {
    return 'Showing everybody, every sprint and every type of ticket.';
  }
  const bits = [];
  bits.push(f.person ? `${f.person}'s hours` : 'Everybody\'s hours');
  if (f.sprint) bits.push(`in ${f.sprint}`);
  if (f.type) bits.push(`on ${f.type} tickets only`);
  return `Showing ${bits.join(' ')}. The budget is still the whole project's.`;
}

function mountFilter() {
  const facets = () => state.data?.facets ?? { people: [], sprints: [], types: [] };
  state.scope = mountScope({
    root: $('ct-scope'),
    fields: [
      { key: 'person', label: 'Person', all: 'Everybody',
        options: () => facets().people.map((n) => [n, n]) },
      { key: 'sprint', label: 'Sprint', all: 'Every sprint',
        options: () => facets().sprints.map((n) => [n, n]) },
      { key: 'type', label: 'Type', all: 'Every type',
        options: () => facets().types.map((n) => [n, n]) },
    ],
    says: filterSays,
    onChange: () => load(),
  });
}

// ── the sprint under way, and how far into it ────────────────────────

const real = () => (state.data?.bySprint ?? []).filter((s) => !s.outside);

/** The sprint the spend is "by": the one under way, else the last one over. */
function reachedSprint() {
  const rows = real();
  return rows.find((s) => s.state === 'current')
    ?? [...rows].reverse().find((s) => s.state === 'done')
    ?? [...rows].reverse().find((s) => s.hours)
    ?? null;
}

function workingDays(from, to) {
  let n = 0;
  for (let d = new Date(`${from}T00:00:00Z`); d <= new Date(`${to}T00:00:00Z`); d = new Date(+d + 86_400_000)) {
    if (d.getUTCDay() % 6) n += 1;
  }
  return n;
}

/** How much of a sprint has gone, as a fraction, for placing "so far". */
function goneOf(sprint) {
  if (!sprint?.startDate || !sprint?.endDate || sprint.state !== 'current') return 1;
  const today = state.data.today;
  const whole = workingDays(sprint.startDate, sprint.endDate) || 1;
  return Math.min(1, Math.max(0.05, workingDays(sprint.startDate, today) / whole));
}

// ── the opening ──────────────────────────────────────────────────────

function drawVerdict() {
  const d = state.data;
  const cur = d.currency;
  const budget = d.budget;
  const comparable = budget && cur && budget.currency === cur;
  const reached = reachedSprint();
  const by = reached && !d.filter.sprint ? `by ${reached.name}` : d.filter.sprint ? `in ${d.filter.sprint}` : 'so far';
  const p = d.projection ?? {};
  const unpricedPeople = d.peopleWithoutRate.filter((n) => n !== 'Nobody');
  const floor = unpricedPeople.length || d.ticketsHoursUnreadable;

  // The line above the headline: what is being read.
  const whenLine = [];
  if (reached && !d.filter.sprint) {
    whenLine.push(el('strong', '', reached.name));
    if (reached.startDate) whenLine.push(` ${shortDate(reached.startDate)} to ${shortDate(reached.endDate)}`);
    whenLine.push(reached.state === 'current' ? ' · under way' : ' · the last sprint over');
  } else {
    whenLine.push(el('strong', '', d.filter.sprint || 'The whole delivery'));
  }
  whenLine.push(d.hoursSource === 'time-entries' ? ' · hours from time entries' : ' · hours from ticket totals');

  let headline;
  let pill;
  let pace = '';
  if (d.totalCost == null) {
    if (d.currencies.length > 1) {
      headline = `Costs are in ${d.currencies.join(' and ')}, which cannot be added.`;
      pace = 'Each person\'s cost is on Per person, in their own currency. Set the rates in one currency for a total, a budget comparison and a projection.';
      pill = { tone: 'warn', text: 'No total' };
    } else if (d.totalHours) {
      headline = `${hoursOf(d.totalHours)} logged ${by}, none of it priced yet.`;
      pace = 'Hours become a cost once there is a rate for the people who logged them, or a default rate for the project.';
      pill = { tone: 'warn', text: 'Not priced' };
    } else {
      headline = filtered() ? 'No time is logged for what the filter shows.' : 'No time has been logged in this project yet.';
      pace = filtered() ? '' : 'Costing multiplies the hours logged in OpenProject by the rates set here; until somebody logs time there is nothing to multiply.';
    }
  } else if (comparable) {
    headline = filtered()
      ? `${money(d.totalCost, cur)} spent ${by}: ${Math.round((d.totalCost / budget.amount) * 100)}% of the budget.`
      : `${money(d.totalCost, cur)} of ${money(budget.amount, cur)} spent ${by}.`;
    if (d.totalCost > budget.amount) pill = { tone: 'bad', text: 'Over budget' };
    else if (p.overBudget > 0 && !filtered()) pill = { tone: 'bad', text: 'Heading over' };
    else if (p.projected != null && !filtered()) pill = { tone: 'ok', text: 'Within budget' };
    if (p.projected != null && !filtered()) {
      pace = p.finished
        ? `${p.lastSprint} has ended: this is the whole cost, ${moneyDiff(p.overBudget, cur)}.`
        : `At this pace ${money(p.projected, cur)} by the end of ${p.lastSprint}, ${moneyDiff(p.overBudget, cur)}.`;
    } else if (!filtered()) pace = p.says ?? '';
  } else {
    headline = `${!budget && !filtered() ? 'No budget set: ' : ''}${money(d.totalCost, cur)} spent ${by}.`;
    if (budget && !comparable) {
      pace = `The budget is in ${budget.currency} and the costs in ${cur}, so the two are not compared. Set one of them in the other's currency.`;
    } else if (p.projected != null && !filtered()) {
      pace = p.finished ? `${p.lastSprint} has ended: this is the whole cost.`
        : `At this pace ${money(p.projected, cur)} by the end of ${p.lastSprint}.`;
    } else if (!filtered()) pace = p.says ?? '';
  }
  if (floor && d.totalCost != null) {
    // Said as a floor whenever anything is missing, which on a real project is
    // almost always; the ledger's "no rate" figure says by how much.
    pace = [pace, `That is a floor: some hours ${unpricedPeople.length ? 'have no rate' : 'could not be read'}, so the real figure is higher.`]
      .filter(Boolean).join(' ');
  }

  const ledger = [];
  ledger.push({ label: 'Spent', value: d.totalCost != null ? money(d.totalCost, cur) : hoursOf(d.totalHours),
    title: d.costAtDefault ? `${money(d.costAtDefault, cur)} of this is at the default rate` : '' });
  ledger.push({ label: 'Budget', value: budget ? money(budget.amount, budget.currency) : 'not set' });
  if (comparable) {
    const left = budget.amount - d.totalCost;
    ledger.push(left >= 0 ? { label: 'Left', value: money(left, cur) }
      : { label: 'Over by', value: money(-left, cur), bad: true });
  }
  const est = d.estimateRemaining;
  if (est.hours) {
    ledger.push({ label: 'Estimated to finish', value: est.cost != null ? money(est.cost, est.currency) : hoursOf(est.hours),
      title: `${hoursOf(est.hours)} of open estimates, less what is already logged on them${est.unpricedHours ? `; ${hoursOf(est.unpricedHours)} of it has no rate` : ''}` });
  }
  const noOwnRate = unpricedPeople.length + d.peopleAtDefault.length;
  ledger.push({ label: 'No rate of their own', value: plural(noOwnRate, 'person', 'people'),
    bad: unpricedPeople.length > 0,
    title: d.peopleAtDefault.length ? `${d.peopleAtDefault.length} priced at the default rate` : '' });

  verdict($('ct-verdict'), {
    when: whenLine,
    headline: headlineWithLink(headline),
    headlineId: 'ct-headline',
    pill,
    pace,
    ledger,
    saying: d.costAtDefault
      ? `${money(d.costAtDefault, cur)} of the spend is at the default rate of ${perHour(d.defaultRate.hourly, d.defaultRate.currency)}, a stand-in for ${plural(d.peopleAtDefault.length, 'person', 'people')} with no rate of their own.`
      : '',
  });
  drawNext();
}

/** "No budget set:" is a link to set one, for the people who can. */
function headlineWithLink(text) {
  if (!text.startsWith('No budget set: ')) return text;
  const span = el('span');
  const a = state.mayEdit ? sectionLink('budget', 'No budget set') : el('span', '', 'No budget set');
  span.append(a, text.slice('No budget set'.length));
  return span;
}

const moneyDiff = (over, cur) => (over == null ? 'with no budget in the same currency to compare'
  : over > 0 ? `${money(over, cur)} over` : over < 0 ? `${money(-over, cur)} under` : 'exactly on budget');

/** One thing to do, named: the first of these that is true. */
function drawNext() {
  const d = state.data;
  const unpriced = d.peopleWithoutRate.filter((n) => n !== 'Nobody');
  const line = $('ct-next');
  if (unpriced.length) {
    const a = sectionLink('rates', state.mayEdit ? 'set them' : 'an administrator sets them on Rates');
    a.onclick = () => { $('ct-rate-person').value = unpriced[0]; };
    next(line, [`${plural(unpriced.length, 'person has', 'people have')} hours and no rate: `, a, '.']);
  } else if (!d.budget && state.mayEdit) {
    next(line, ['No budget is set, so nothing here can be over or under: ', sectionLink('budget', 'set one'), '.']);
  } else if (d.peopleAtDefault.length && state.mayEdit) {
    next(line, [`${plural(d.peopleAtDefault.length, 'person is', 'people are')} priced at the default: `,
      sectionLink('rates', 'give them their own rate'), '.']);
  } else if (d.hoursSource !== 'time-entries') {
    next(line, 'Hours are ticket totals, not dated: give the ADAM OpenProject account "View time entries" to see them by week and by the day they were spent.');
  } else if (d.projection?.overBudget > 0) {
    const cross = (d.projection.path ?? []).find((pt) => pt.cost > d.budget.amount);
    next(line, cross ? `At this pace the budget runs out during ${cross.name}. Look at Per person for where the hours go.`
      : 'At this pace the budget runs out before the last sprint ends.');
  } else {
    next(line, '');
  }
}

// ── the bold thing: cost by sprint against the budget ────────────────

function niceTop(v) {
  if (v <= 0) return 1;
  const p = 10 ** Math.floor(Math.log10(v));
  for (const m of [1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]) if (m * p >= v) return m * p;
  return 10 * p;
}

function drawChart() {
  const d = state.data;
  const figure = $('ct-figure');
  const rows = real();
  const inMoney = d.totalCost != null;
  if (!rows.length || d.filter.sprint || !d.totalHours) {
    figure.hidden = true;
    $('ct-hero').classList.add('is-single');
    return;
  }
  figure.hidden = false;
  $('ct-hero').classList.remove('is-single');
  const cur = d.currency;
  const before = d.bySprint.find((s) => s.outside);
  const start = before ? (inMoney ? before.cumulative : before.cumulativeHours) : 0;
  const value = (s) => (inMoney ? s.cumulative : s.cumulativeHours);
  const label = (v) => (inMoney ? money(Math.round(v), cur, { compact: true }) : `${fmt(Math.round(v))} h`);
  const p = d.projection ?? {};
  // Not for a slice: one person's spend drawn against the whole project's
  // budget is a line far above a line, and says nothing the headline's
  // percentage does not.
  const budget = inMoney && !filtered() && d.budget && d.budget.currency === cur ? d.budget.amount : null;
  const path = inMoney && !filtered() ? (p.path ?? []) : [];

  // How far the spend has got: the sprint under way, or the last with hours.
  const reached = reachedSprint();
  const upto = reached ? rows.indexOf(reached) : -1;

  const box = $('ct-plot');
  const W = Math.max(300, Math.round(box.clientWidth || 460));
  const H = 240;
  const m = { l: 56, r: 92, t: 24, b: 32 };
  const iw = W - m.l - m.r;
  const ih = H - m.t - m.b;
  const n = rows.length;
  const values = [start, ...rows.slice(0, upto + 1).map(value), ...path.map((pt) => pt.cost), budget ?? 0];
  const top = niceTop(Math.max(...values) * 1.05);
  const x = (i) => m.l + (i / n) * iw;
  const y = (v) => m.t + ih - (v / top) * ih;

  const tips = [];
  const pic = svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img' });

  for (const v of [0, top / 2, top]) {
    pic.append(svg('line', { x1: m.l, x2: m.l + iw, y1: y(v), y2: y(v), class: v ? 'sh-grid-line' : 'ct-base' }));
    pic.append(svg('text', { x: m.l - 8, y: y(v) + 4, class: 'sh-tick', 'text-anchor': 'end' }, label(v)));
  }
  // The sprint under way, as the column it occupies.
  if (reached?.state === 'current') {
    pic.append(svg('rect', { x: x(upto), y: m.t, width: x(upto + 1) - x(upto), height: ih, class: 'ct-now' }));
    pic.append(svg('text', { x: (x(upto) + x(upto + 1)) / 2, y: m.t - 8, class: 'sh-tick', 'text-anchor': 'middle' }, 'now'));
  }
  // Sprints along the bottom: the whole name where there is room, else its number.
  const roomy = iw / n >= 62;
  if (!roomy) pic.append(svg('text', { x: m.l - 8, y: H - 10, class: 'sh-tick', 'text-anchor': 'end' }, 'sprint'));
  rows.forEach((s, i) => {
    const short = roomy ? s.name : s.name.replace(/^sprint\s*/i, '');
    pic.append(svg('text', { x: (x(i) + x(i + 1)) / 2, y: H - 10, class: 'sh-tick', 'text-anchor': 'middle' }, short));
  });

  // The budget, a yardstick. Its label waits for the projection's, below:
  // the two share the right margin and are placed together.
  const margin = [];
  if (budget != null) {
    pic.append(svg('line', { x1: m.l, x2: m.l + iw, y1: y(budget), y2: y(budget), class: 'ct-budget' }));
    margin.push({ at: y(budget), word: 'budget', figure: label(budget) });
  }

  // The spend so far, to the end of each sprint over and part-way into the
  // one under way, where it stops at the share of that sprint that has gone.
  const pts = [[x(0), y(start)]];
  for (let i = 0; i <= upto; i += 1) {
    const s = rows[i];
    const at = s.state === 'current' ? i + goneOf(s) : i + 1;
    pts.push([x(at), y(value(s))]);
  }
  const [endX, endY] = pts.at(-1);
  // The projection, dashed from where the spend has got to.
  if (path.length) {
    const ppts = [[endX, endY], ...path.map((pt) => [x(rows.findIndex((s) => s.name === pt.name) + 1), y(pt.cost)])];
    pic.append(svg('polyline', { points: ppts.map((q) => q.join(',')).join(' '), class: 'ct-projected' }));
    const [px, py] = ppts.at(-1);
    pic.append(svg('circle', { cx: px, cy: py, r: 4, class: 'ct-projected-dot' }));
    margin.push({ at: py, word: 'at this pace', figure: label(path.at(-1).cost) });
    // Over the budget at the end: the gap, red, with the words beside it.
    // Above the end of the projection and left of it, which is the one place
    // the dashed line, coming up from the lower left, never runs through.
    if (budget != null && path.at(-1).cost > budget) {
      pic.append(svg('line', { x1: px, x2: px, y1: y(budget), y2: py + 5, class: 'ct-over' }));
      pic.append(svg('text', { x: px - 8, y: Math.max(m.t - 6, py - 12), class: 'sh-label is-over', 'text-anchor': 'end' },
        `${label(path.at(-1).cost - budget)} over`));
    }
  }
  // The right margin's labels, two lines each, kept 32px apart: when the pace
  // ends near the budget the two would otherwise print over each other, and
  // they are the two numbers the chart is read for.
  margin.sort((a, b) => a.at - b.at);
  for (let i = 1; i < margin.length; i += 1) {
    if (margin[i].at - margin[i - 1].at < 32) {
      const mid = (margin[i].at + margin[i - 1].at) / 2;
      margin[i - 1].at = mid - 16;
      margin[i].at = mid + 16;
    }
  }
  for (const label2 of margin) {
    pic.append(svg('text', { x: m.l + iw + 8, y: label2.at + 1, class: 'sh-label' }, label2.word));
    pic.append(svg('text', { x: m.l + iw + 8, y: label2.at + 14, class: 'sh-tick' }, label2.figure));
  }
  pic.append(svg('polyline', { points: pts.map((q) => q.join(',')).join(' '), class: 'ct-spent' }));
  pic.append(svg('circle', { cx: endX, cy: endY, r: 4.5, class: 'ct-spent-dot' }));
  const spentNow = value(rows[Math.max(0, upto)]);
  const textLeft = path.length && endX > m.l + iw * 0.55;
  // Above the dot, unless that is where the budget line runs; then below it.
  const onBudget = budget != null && Math.abs(endY - 10 - y(budget)) < 12;
  pic.append(svg('text', { x: textLeft ? endX - 10 : endX + 8, y: onBudget ? endY + 20 : endY - 10, class: 'sh-label is-strong', 'text-anchor': textLeft ? 'end' : 'start' },
    `${label(spentNow)} so far`));

  // One target per sprint, wider than any mark, saying the sprint's figures.
  const hits = svg('g');
  rows.forEach((s, i) => {
    const projected = path.find((pt) => pt.name === s.name);
    const words = `${s.name}${s.startDate ? `, ${shortDate(s.startDate)} to ${shortDate(s.endDate)}` : ''}: `
      + (s.state === 'ahead' ? 'not begun.'
        : `${inMoney ? money(s.cost, cur) : hoursOf(s.hours)} in it, ${inMoney ? money(s.cumulative, cur) : hoursOf(s.cumulativeHours)} in all by its end${s.state === 'current' ? ' so far' : ''}.`)
      + (projected ? ` At this pace ${money(projected.cost, cur)} by its end.` : '');
    const hit = svg('rect', { x: x(i), y: m.t, width: x(i + 1) - x(i), height: ih, class: 'ct-hit' });
    hit.append(svg('title', {}, words));
    hits.append(hit);
    tips.push(words);
  });
  pic.append(hits);
  pic.setAttribute('aria-label', inMoney
    ? `Cost by sprint: ${money(spentNow, cur)} spent so far${budget != null ? ` against a ${money(budget, cur)} budget` : ''}${path.length ? `; at this pace ${money(path.at(-1).cost, cur)} by the end of ${path.at(-1).name}` : ''}.`
    : `Hours logged by sprint: ${hoursOf(spentNow)} so far.`);
  box.replaceChildren(pic);

  $('ct-figure-caption').textContent = inMoney
    ? `Spent by the end of each sprint${budget != null ? ', against the budget' : ''}${path.length ? ', and where this pace takes it' : ''}`
    : 'Hours logged by the end of each sprint, before any rate (nothing is priced yet)';

  // The key, drawn as the lines it names.
  const key = el('ul', 'ct-key');
  const swatch = (cls) => {
    const s = svg('svg', { width: 22, height: 10, 'aria-hidden': 'true' });
    s.append(svg('line', { x1: 1, x2: 21, y1: 5, y2: 5, class: cls }));
    return s;
  };
  const item = (cls, words) => { const li = el('li'); li.append(swatch(cls), words); key.append(li); };
  item('ct-spent', inMoney ? 'Spent' : 'Logged');
  if (path.length) item('ct-projected', 'At this pace');
  if (budget != null) item('ct-budget', 'Budget');
  if (budget != null && path.length && path.at(-1).cost > budget) item('ct-over', 'Over the budget');
  $('ct-figure-key').replaceChildren(key);

  // The table twin, for anything not looking at the picture.
  $('ct-figure-twin').replaceChildren(table({
    caption: 'Cost by sprint, the figures the chart draws',
    srOnly: true,
    columns: sprintColumns(),
    rows: d.bySprint,
  }));
}

// ── what the overview rests on ───────────────────────────────────────

function drawRests() {
  const d = state.data;
  const list = $('ct-rests');
  list.replaceChildren();
  const li = (...parts) => { const item = el('li'); item.append(...parts); list.append(item); };

  if (d.hoursSource === 'time-entries') {
    li(el('strong', '', 'Hours'), ' are OpenProject\'s time entries: who logged each hour, and on which day. An hour counts in the sprint it was spent in.');
  } else {
    // The service's sentence says why and then what follows; the second half
    // is the line's own first half, so only the why is kept.
    const why = (d.hoursSays ?? '').replace(/,? so (for now )?hours are each ticket's total.*$/, '.');
    li(el('strong', '', 'Hours'), ` are each ticket's logged total, counted in the ticket's sprint and against whoever holds it. ${why}`);
  }
  const ownRates = (state.rates?.rates ?? []).length;
  const dr = d.defaultRate;
  li(el('strong', '', 'Rates'), ownRates ? ` are set here: ${plural(ownRates, 'person has', 'people have')} their own`
    : ' are set here, and nobody has one yet',
    dr ? `, and anybody else is priced at the default of ${perHour(dr.hourly, dr.currency)}` : (ownRates ? ', and there is no default rate' : ', nor is there a default rate'),
    '. ', sectionLink('rates', 'Rates'));
  if (d.budget) {
    // What it replaced, by amount: "it was changed" says less than "from ₹40L".
    const earlier = (state.budgets?.history ?? []).slice(1);
    li(el('strong', '', 'The budget'), ` is ${money(d.budget.amount, d.budget.currency)}, set by ${d.budget.setBy || 'an administrator'} on ${shortDate(d.budget.setAt)}`,
      earlier.length ? `, replacing ${money(earlier[0].amount, earlier[0].currency)}${earlier.length > 1 ? ` and ${plural(earlier.length - 1, 'budget')} before that` : ''}` : '',
      '. ', sectionLink('budget', 'Budget'));
  } else {
    li(el('strong', '', 'No budget'), ' is set, so nothing can be over or under. ', sectionLink('budget', 'Budget'));
  }
  const p = d.projection ?? {};
  if (p.projected != null && !p.finished && !filtered()) {
    const cur = d.currency;
    li(el('strong', '', 'The pace'), p.basis === 'working-days'
      ? ` is ${money(p.per, cur)} a working day: ${money(d.totalCost, cur)} over the ${p.elapsed} working days since the first sprint began, carried over the ${p.total - p.elapsed} left to the end of ${p.lastSprint}.`
      : ` is ${money(p.per, cur)} a sprint: ${money(d.totalCost, cur)} across ${(p.elapsed / 100).toFixed(1)} sprints so far (the one under way counted for the part that has gone), carried to all ${p.total / 100}.`);
  } else if (!filtered() && p.says) {
    li(el('strong', '', 'No projection'), `: ${p.says.replace(/^./, (c) => c.toLowerCase())}`);
  }
  const est = d.estimateRemaining;
  if (est.hours) {
    li(el('strong', '', 'Open work'), ` is estimated at ${hoursOf(est.hours)} more`,
      est.cost != null ? `, ${money(est.cost, est.currency)} at today's rates` : '',
      '. An estimate is a plan, not a cost, so it is never added to the spend.');
  }
}

// ── per person ───────────────────────────────────────────────────────

let peopleTable = null;
function drawPeople() {
  const d = state.data;
  const people = d.people.filter((p) => p.hours || p.tickets);
  const cols = [
    { key: 'person', label: 'Person', sort: (r) => r.person.toLowerCase(),
      render: (r) => (r.person === 'Nobody' ? el('em', '', 'Nobody (unassigned)') : personLink(r.person)) },
    { key: 'tickets', label: 'Tickets', num: true, sort: (r) => r.tickets },
    { key: 'hours', label: 'Hours logged', num: true, sort: (r) => r.hours, render: (r) => hoursOf(r.hours) },
    { key: 'estimated', label: 'Estimated', num: true, sort: (r) => r.estimated, render: (r) => hoursOf(r.estimated) },
    { key: 'hourly', label: 'Rate', num: true, sort: (r) => r.hourly ?? -1,
      render: (r) => {
        if (r.hourly == null) return el('span', r.hours ? 'ct-missing' : 'sh-quiet', 'no rate');
        const span = el('span', '', perHour(r.hourly, r.currency));
        if (r.atDefault) span.append(el('span', 'ct-tag', 'at the default'));
        return span;
      } },
    { key: 'cost', label: 'Cost', num: true, sort: (r) => r.cost ?? -1,
      render: (r) => {
        if (r.cost != null) return money(r.cost, r.currency);
        const dash = el('span', r.hours ? 'ct-missing' : '', '—');
        if (r.hours) dash.title = `${r.person} has logged hours and no rate is set, so none of that time is in the spend.`;
        return dash;
      } },
  ];
  if (!peopleTable) {
    // Made once and redrawn, so a sort somebody chose survives a Refresh.
    peopleTable = table({ caption: 'People', columns: cols, rows: people, sortBy: { key: 'cost', dir: -1 },
      empty: filtered() ? 'Nobody matches the filter. Show everything to see the whole team.'
        : 'Nobody has tickets in this project yet.' });
    $('ct-people').replaceChildren(peopleTable);
  } else peopleTable.redraw(people);
  peopleTable.querySelector('caption').textContent = `${plural(people.length, 'person', 'people')}, ${hoursOf(d.totalHours)} logged in all`;
}

// ── per sprint and per week ──────────────────────────────────────────

// "Ended" rather than "Over": on a money page "over" means over the budget.
const STATE_WORDS = { done: ['done', 'Ended'], current: ['going', 'Under way'], ahead: ['fresh', 'To come'] };

function sprintColumns() {
  const d = state.data;
  const cur = d.currency;
  const path = new Map((filtered() ? [] : d.projection?.path ?? []).map((pt) => [pt.name, pt.cost]));
  const cols = [
    { key: 'name', label: 'Sprint', render: (r) => (r.outside ? el('em', '', r.name) : r.name) },
    { key: 'dates', label: 'Dates', nowrap: true,
      render: (r) => (r.startDate ? `${shortDate(r.startDate)} to ${shortDate(r.endDate)}` : '') },
    { key: 'state', label: 'State', render: (r) => (STATE_WORDS[r.state] && !r.outside
      ? badge(...STATE_WORDS[r.state]) : el('span', 'sh-quiet', r.outside ? '' : 'no dates')) },
    { key: 'hours', label: 'Hours', num: true, render: (r) => hoursOf(r.hours) },
  ];
  if (d.totalCost != null) {
    cols.push(
      { key: 'cost', label: 'Spent in it', num: true, render: (r) => (r.hours ? money(r.cost, cur) : '—') },
      { key: 'cumulative', label: 'Spent by its end', num: true,
        render: (r) => (r.state === 'ahead' ? '—' : money(r.cumulative, cur)) },
      { key: 'projected', label: 'At this pace', num: true,
        render: (r) => (path.has(r.name) ? money(path.get(r.name), cur) : '') },
    );
  }
  cols.push({ key: 'unpricedHours', label: 'Hours with no rate', num: true,
    render: (r) => (r.unpricedHours ? el('span', 'ct-missing', hoursOf(r.unpricedHours)) : '—') });
  return cols;
}

function drawSprints() {
  const d = state.data;
  $('ct-sprints-note').textContent = d.hoursSource === 'time-entries'
    ? 'An hour counts in the sprint it was logged in, by the date on its time entry. Hours logged between two sprints count in the one before.'
    : 'An hour counts in the sprint its ticket is planned in, because ticket totals carry no date. Hours on tickets in no sprint are listed first.';
  $('ct-sprints').replaceChildren(table({
    caption: d.totalCost != null ? `By sprint, in ${d.currency}` : 'By sprint, in hours (nothing is priced yet)',
    columns: sprintColumns(),
    rows: d.bySprint,
    empty: 'No sprint has hours in what the filter shows.',
  }));

  const weeks = d.byWeek ?? [];
  $('ct-weeks-note').textContent = d.hoursSource === 'time-entries'
    ? 'Monday to Sunday, by the day each hour was logged against.'
    : 'Weeks need dated hours, and this OpenProject account may not read time entries. Give it "View time entries" to see them.';
  const cur = d.currency;
  $('ct-weeks').replaceChildren(weeks.length ? table({
    caption: 'By week',
    columns: [
      { key: 'week', label: 'Week of', render: (r) => shortDate(r.week), sort: (r) => r.week },
      { key: 'hours', label: 'Hours', num: true, render: (r) => hoursOf(r.hours), sort: (r) => r.hours },
      ...(d.totalCost != null ? [
        { key: 'cost', label: 'Spent in it', num: true, render: (r) => money(r.cost, cur), sort: (r) => r.cost },
        { key: 'cumulative', label: 'Spent by its end', num: true, render: (r) => money(r.cumulative, cur) },
      ] : []),
      { key: 'unpricedHours', label: 'Hours with no rate', num: true,
        render: (r) => (r.unpricedHours ? hoursOf(r.unpricedHours) : '—') },
    ],
    rows: weeks,
  }) : el('p', 'sh-empty', d.hoursSource === 'time-entries' ? 'No hours are logged in what the filter shows.' : ''));
}

// ── the budget ───────────────────────────────────────────────────────

function currencyOptions(select, chosen) {
  const choices = state.rates?.currencyChoices ?? state.budgets?.currencyChoices ?? ['INR'];
  select.replaceChildren(...choices.map((c) => new Option(c, c)));
  select.value = choices.includes(chosen) ? chosen : choices[0];
}

function drawBudget() {
  const b = state.budgets ?? { budget: null, history: [] };
  const now = $('ct-budget-now');
  now.replaceChildren();
  if (b.budget) {
    now.append(el('strong', '', money(b.budget.amount, b.budget.currency)),
      ` since ${shortDate(b.budget.setAt)}, set by ${b.budget.setBy || 'an administrator'}`,
      b.budget.note ? `: "${b.budget.note}".` : '.');
  } else {
    now.textContent = state.mayEdit
      ? 'No budget is set yet. Set one below and the overview compares the spend with it.'
      : 'No budget is set yet. An administrator sets it here.';
  }
  $('ct-budget-form').hidden = !state.mayEdit;
  $('ct-budget-readonly').hidden = state.mayEdit;
  if (state.mayEdit && !$('ct-budget-form').dataset.touched) {
    currencyOptions($('ct-budget-currency'), b.budget?.currency ?? state.data?.currency ?? 'INR');
  }
  $('ct-budget-history').replaceChildren(table({
    caption: b.history.length ? `${plural(b.history.length, 'budget')}, newest first` : '',
    columns: [
      { key: 'setAt', label: 'When', nowrap: true, render: (r) => when(r.setAt) },
      { key: 'setBy', label: 'Who', render: (r) => r.setBy || '—' },
      { key: 'from', label: 'From', num: true, render: (r) => (r.from ? money(r.from.amount, r.from.currency) : el('em', '', 'the first')) },
      { key: 'amount', label: 'To', num: true, render: (r) => money(r.amount, r.currency) },
      { key: 'note', label: 'Why', render: (r) => r.note || '' },
    ],
    rows: b.history,
    empty: 'No budget has been set for this project.',
  }));
}

// ── rates ────────────────────────────────────────────────────────────

function drawRates() {
  const rates = state.rates?.rates ?? [];
  const d = state.data;
  $('ct-rate-form').hidden = !state.mayEdit;
  $('ct-rates-readonly').hidden = state.mayEdit;

  // The names the tickets actually use, so a rate cannot be typed against
  // somebody OpenProject has never heard of. People with hours and no rate
  // first, since they are the ones the overview says to set. Redrawn on every
  // read, so a Refresh that brings a new name brings it here too.
  const picker = $('ct-rate-person');
  const keep = picker.value;
  const priced = new Map(rates.map((r) => [r.person.toLowerCase(), r]));
  const unpriced = new Set((d?.peopleWithoutRate ?? []).concat(d?.peopleAtDefault ?? []));
  const names = (d?.facets?.people ?? []).filter((n) => n && n !== 'Nobody')
    .sort((a, b) => (unpriced.has(b) - unpriced.has(a)) || a.localeCompare(b));
  picker.replaceChildren(...names.map((name) => {
    const rate = priced.get(name.toLowerCase());
    const text = rate ? `${name} (now ${perHour(rate.hourly, rate.currency)})`
      : unpriced.has(name) ? `${name} (has hours, no rate)` : name;
    return new Option(text, name);
  }));
  if (!names.length) picker.append(new Option('Nobody has tickets yet', ''));
  if (names.includes(keep)) picker.value = keep;
  if (state.mayEdit && !$('ct-rate-form').dataset.touched) {
    currencyOptions($('ct-rate-currency'), d?.currency ?? state.budgets?.budget?.currency ?? 'INR');
  }

  const used = new Set((d?.facets?.people ?? []).map((n) => n.toLowerCase()));
  const cols = [
    { key: 'person', label: 'Person', sort: (r) => r.person.toLowerCase(), render: (r) => personLink(r.person) },
    { key: 'hourly', label: 'Per hour', num: true, sort: (r) => r.hourly, render: (r) => money(r.hourly, r.currency, { exact: true }) },
    { key: 'currency', label: 'Currency' },
    { key: 'note', label: 'Note', render: (r) => r.note || '' },
    { key: 'setAt', label: 'Set', nowrap: true, render: (r) => shortDate(r.setAt) },
  ];
  // A rate against a name no ticket uses earns nothing and looks like it
  // does, so it is called out rather than listed as if it were working. Only
  // when there is one: a column saying "yes" on every row is a column to skip.
  if (rates.some((r) => !used.has(r.person.toLowerCase()))) {
    cols.push({ key: 'used', label: 'Matches', render: (r) => (used.has(r.person.toLowerCase()) ? ''
      : el('span', 'ct-missing', 'no ticket uses this name')) });
  }
  if (state.mayEdit) {
    cols.push({ key: 'remove', label: 'Remove', render: (r) => {
      const drop = el('button', 'chip', 'Remove');
      drop.type = 'button';
      drop.setAttribute('aria-label', `Remove ${r.person}'s rate`);
      drop.onclick = async () => {
        const yes = await confirmStep(drop.closest('.sh-table-wrap'), {
          say: `Remove ${r.person}'s rate of ${perHour(r.hourly, r.currency)}? Their hours ${d?.defaultRate ? 'are priced at the default' : 'stop counting in the spend'} until a new one is set.`,
          action: 'Remove the rate' });
        if (!yes) return;
        drop.disabled = true;
        try { await auth.dropRate(r.id); await reloadAll(); } catch (error) { say('ct-rate-error', `Could not remove the rate: ${error.message}`); drop.disabled = false; }
      };
      return drop;
    } });
  }
  $('ct-rates').replaceChildren(table({
    caption: rates.length ? plural(rates.length, 'rate') : '',
    columns: cols, rows: rates,
    empty: state.mayEdit ? 'No rates are set. Set one above; until then the spend has no cost, only hours.'
      : 'No rates are set yet, so the spend has no cost, only hours.',
  }));

  // The default rate.
  const dr = state.rates?.default;
  $('ct-default-now').replaceChildren();
  if (dr) {
    $('ct-default-now').append(el('strong', '', perHour(dr.hourly, dr.currency)),
      ` since ${shortDate(dr.setAt)}`, dr.note ? `: "${dr.note}".` : '.',
      d?.peopleAtDefault?.length ? ` It prices ${plural(d.peopleAtDefault.length, 'person', 'people')} now.` : ' Nobody is priced by it now.');
  } else {
    $('ct-default-now').textContent = 'No default rate. People with hours and no rate of their own are left out of the spend, and named.';
  }
  $('ct-default-form').hidden = !state.mayEdit;
  $('ct-default-drop').hidden = !dr;
  if (state.mayEdit && !$('ct-default-form').dataset.touched) {
    currencyOptions($('ct-default-currency'), dr?.currency ?? d?.currency ?? 'INR');
    if (dr) $('ct-default-hourly').value = (dr.hourly / 100).toFixed(2).replace(/\.00$/, '');
  }
}

// ── what is missing ──────────────────────────────────────────────────

function drawGaps() {
  const d = state.data;
  const unpriced = d.peopleWithoutRate.filter((n) => n !== 'Nobody');
  const rows = [
    { count: d.ticketsWithoutHours, what: 'Tickets with no time logged',
      why: 'Real work with nothing recorded against it costs nothing here.' },
    { count: d.ticketsHoursUnreadable, what: 'Tickets whose time this account cannot read',
      why: 'OpenProject shows logged time only to an account allowed to see time entries. Not the same as nobody having logged any.' },
    { count: unpriced.length, what: 'People with hours and no rate',
      why: unpriced.join(', ') || 'Everybody with hours is priced.' },
    { count: d.peopleAtDefault.length, what: 'People priced at the default rate',
      why: d.peopleAtDefault.length ? `${d.peopleAtDefault.join(', ')}. A stand-in, not what they cost.` : 'Nobody is priced at the default.' },
    { count: d.estimateRemaining.ticketsWithoutEstimate, what: 'Open tickets with no estimate',
      why: 'They are not in "estimated to finish", which is therefore a floor too.' },
  ];
  if (d.hoursSource !== 'time-entries') {
    rows.push({ count: '!', what: 'Hours without dates', why: d.hoursSays ?? 'Time entries could not be read.' });
  }
  if (d.peopleWithoutRate.includes('Nobody')) {
    rows.push({ count: '!', what: 'Hours on unassigned tickets', why: 'Logged against nobody, so there is no rate to price them at.' });
  }
  if (d.truncated) {
    rows.push({ count: '!', what: 'More tickets than were read',
      why: 'The project has more work packages than one read returns, so this is a sample.' });
  }
  $('ct-gaps').replaceChildren(table({
    caption: '',
    columns: [
      { key: 'what', label: 'What', render: (r) => r.what },
      { key: 'count', label: 'How many', num: true, render: (r) => (typeof r.count === 'number' ? fmt(r.count) : r.count) },
      { key: 'why', label: 'Why it matters', render: (r) => r.why },
    ],
    rows,
    rowClass: (r) => (r.count === 0 ? 'ct-gap-none' : ''),
  }));
}

// ── the read, and when it was made ───────────────────────────────────

function drawAsOf() {
  const d = state.data;
  if (!d?.asOf) return;
  const age = d.ageSeconds + (performance.now() - state.receivedAt) / 1000;
  const at = new Date(d.asOf).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
  const ago = age < 60 ? 'under a minute ago' : age < 5400 ? `${plural(Math.round(age / 60), 'minute')} ago`
    : `${plural(Math.round(age / 3600), 'hour')} ago`;
  const line = $('ct-asof');
  line.classList.toggle('is-failed', !d.refreshing && !!d.refreshError);
  line.title = d.refreshError ?? '';
  line.textContent = d.refreshing ? `Refreshing… (last read ${at})`
    : d.refreshError ? `Could not refresh from OpenProject. Last good read at ${at}, ${ago}.`
      : `Read from OpenProject at ${at}, ${ago}`;
}

function drawAll() {
  const d = state.data;
  if (!d) return;
  $('ct-lede').textContent = d.hoursSource === 'time-entries'
    ? 'Hours logged in OpenProject, priced at the rates set here. Nothing here is an invoice.'
    : 'Hours logged on OpenProject tickets, priced at the rates set here. Nothing here is an invoice.';
  drawAsOf();
  drawVerdict();
  drawChart();
  drawRests();
  drawPeople();
  drawSprints();
  drawBudget();
  drawRates();
  drawGaps();
  if (!state.scope) mountFilter();
  else state.scope.redraw();
}

function showFailure(error) {
  if (error.status === 401) { $('costing').hidden = true; $('signed-out').hidden = false; return true; }
  if (error.status === 403) { $('costing').hidden = true; $('denied').hidden = false; return true; }
  if (error.status === 428) {
    $('costing').hidden = true;
    $('unconnected').hidden = false;
    $('unconnected-why').textContent = error.message;
    // A missing token is fixed in your settings; a project nobody has pointed
    // at OpenProject is fixed on the admin page.
    if (/admin page|Projects/i.test(error.message)) {
      $('unconnected-go').href = '/admin.html#projects';
      $('unconnected-go').textContent = 'Go to the admin page';
    }
    return true;
  }
  return false;
}

/**
 * Ask for the costing with the page's filter. A Refresh is answered at once
 * with the read the service holds, marked `refreshing` while the new one is
 * read behind it, so this asks again every ten seconds until it is in. A
 * newer load (the filter changed) makes an older one stop drawing.
 */
async function load({ refresh = false } = {}) {
  const mine = ++state.loading;
  const button = $('ct-refresh');
  button.disabled = true;
  say('ct-error', '');
  try {
    let first = true;
    for (;;) {
      let answer;
      try {
        answer = await auth.costingSheet({ projectId: state.project, refresh: refresh && first, ...filter() });
      } catch (error) {
        if (mine !== state.loading) return;
        if (showFailure(error)) return;
        if (error.status === 503) {
          // The first read of a big project, still running on the server. It
          // goes on without this page; asking again is the whole of the fix.
          $('ct-asof').textContent = error.message;
          await sleep(10_000);
          if (mine !== state.loading) return;
          continue;
        }
        throw error;
      }
      first = false;
      if (mine !== state.loading) return;
      state.data = answer;
      state.receivedAt = performance.now();
      $('costing').hidden = false;
      drawAll();
      if (!answer.refreshing) break;
      button.textContent = 'Refreshing…';
      await sleep(10_000);
      if (mine !== state.loading) return;
    }
  } catch (error) {
    say('ct-error', `Could not read the costing: ${error.message}. Press Refresh to try again.`);
  } finally {
    if (mine === state.loading) {
      button.textContent = 'Refresh';
      button.disabled = false;
    }
  }
}

/** Rates and the budget: small reads of ADAM's own tables. */
async function loadConfig() {
  try {
    [state.rates, state.budgets] = await Promise.all([
      auth.listRates(state.project), auth.getBudget(state.project)]);
  } catch (error) {
    if (showFailure(error)) return;
    say('ct-rate-error', `Could not read the rates: ${error.message}`);
  }
}

async function reloadAll() {
  await loadConfig();
  await load();
}

// ── the forms ────────────────────────────────────────────────────────

/** Typed as money, sent as the smallest unit. Rounded here rather than relied
 *  on: 45.55 * 100 is 4554.9999999999995 in this language. */
const minorOf = (text) => Math.round(Number(text || 0) * 100);

function wireForms() {
  for (const id of ['ct-budget-form', 'ct-rate-form', 'ct-default-form']) {
    // Once somebody has chosen a currency, a redraw must not choose another.
    $(id).addEventListener('change', () => { $(id).dataset.touched = '1'; });
  }

  $('ct-budget-form').onsubmit = async (event) => {
    event.preventDefault();
    say('ct-budget-error', '');
    const amount = minorOf($('ct-budget-amount').value);
    if (amount <= 0) { say('ct-budget-error', 'Type the budget as an amount above zero.'); return; }
    try {
      state.budgets = await auth.setBudget(amount, $('ct-budget-currency').value,
        $('ct-budget-note').value, state.project);
      $('ct-budget-amount').value = '';
      $('ct-budget-note').value = '';
      delete $('ct-budget-form').dataset.touched;
      await reloadAll();
    } catch (error) { say('ct-budget-error', `The budget was not saved: ${error.message}`); }
  };

  $('ct-rate-form').onsubmit = async (event) => {
    event.preventDefault();
    say('ct-rate-error', '');
    const person = $('ct-rate-person').value;
    if (!person) { say('ct-rate-error', 'Pick whose rate this is.'); return; }
    try {
      await auth.setRate(person, minorOf($('ct-rate-hourly').value), $('ct-rate-currency').value,
        $('ct-rate-note').value, state.project);
      $('ct-rate-hourly').value = '';
      $('ct-rate-note').value = '';
      await reloadAll();
    } catch (error) { say('ct-rate-error', `The rate was not set: ${error.message}`); }
  };

  $('ct-default-form').onsubmit = async (event) => {
    event.preventDefault();
    say('ct-default-error', '');
    try {
      await auth.setDefaultRate(minorOf($('ct-default-hourly').value), $('ct-default-currency').value,
        $('ct-default-note').value, state.project);
      $('ct-default-note').value = '';
      delete $('ct-default-form').dataset.touched;
      await reloadAll();
    } catch (error) { say('ct-default-error', `The default rate was not saved: ${error.message}`); }
  };

  $('ct-default-drop').onclick = async () => {
    const dr = state.rates?.default;
    const yes = await confirmStep($('ct-default-drop'), {
      say: `Remove the default rate of ${dr ? perHour(dr.hourly, dr.currency) : ''}? Everybody it prices drops out of the spend and is named as having no rate.`,
      action: 'Remove the default' });
    if (!yes) return;
    try {
      await auth.dropDefaultRate(state.project);
      $('ct-default-hourly').value = '';
      delete $('ct-default-form').dataset.touched;
      await reloadAll();
    } catch (error) { say('ct-default-error', `The default rate was not removed: ${error.message}`); }
  };
}

// ── start ────────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) { $('signed-out').hidden = false; return; }
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';
  if (!auth.isReader(state.me)) { $('denied').hidden = false; return; }
  state.mayEdit = auth.isAdmin(state.me);
  state.project = (await auth.ensureProject()) ?? '';

  // The project picker, as on Tasks: changing project is a new page, not a
  // state of this one, because every figure and form below is that project's.
  auth.listProjects().then(({ projects }) => {
    const mine = projects.filter((p) => !state.me.projects?.length || state.me.projects.includes(p.id));
    const picker = $('ct-project');
    picker.replaceChildren(...mine.map((p) => {
      const option = new Option(p.name || p.id, p.id);
      option.selected = p.id === state.project;
      return option;
    }));
    picker.onchange = () => {
      auth.rememberProject(picker.value);
      location.search = `?project=${encodeURIComponent(picker.value)}`;
    };
    $('ct-project-field').hidden = picker.options.length < 2;
  }).catch(() => { /* the page still works for the current project */ });

  $('ct-refresh').onclick = async () => {
    // The rates and budget are ADAM's and read in a blink; asked again too, so
    // a rate another administrator set since is in the picker and the table.
    loadConfig().then(() => { if (state.data) { drawBudget(); drawRates(); drawRests(); } });
    await load({ refresh: true });
  };
  setInterval(drawAsOf, 30_000);
  wireForms();
  let resizing = 0;
  addEventListener('resize', () => { clearTimeout(resizing); resizing = setTimeout(() => state.data && drawChart(), 150); });

  await loadConfig();
  await load();
  // One section at a time, driven by the rail; see panels.js.
  mountPanels({ nav: document.querySelector('#costing .set-nav'), fallback: 'overview',
    onShow: (name) => { if (name === 'overview' && state.data) drawChart(); } });
})();
