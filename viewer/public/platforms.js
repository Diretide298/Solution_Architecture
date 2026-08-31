/**
 * The platforms, and what is missing from each.
 *
 * A platform is an application somebody signs into — Guest Web, Venue POS, the
 * back office. It is the unit a delivery lead owns, and the question they
 * arrive with is not "how many screens are there" but **is this one buildable
 * yet, and if not, what is in the way**.
 *
 * `platforms.html` and the whole `.plat-*` half of `domains.css` shipped
 * without this file, so the page has been a static shell — a container and a
 * sort control with nothing behind them. The markup and the styling already
 * describe the intended shape, down to four gap kinds with their own classes;
 * this is that shape wired to the payload rather than a new design.
 *
 * **It refuses to be a directory.** The index already lists the platforms and a
 * second list is a second thing to keep in step. Every card answers four
 * questions instead, and each one is counted from a payload rather than typed:
 *
 *   thin?      operations against screens. P11 draws 8 screens over 3
 *              operations; P08 draws 143 over 441. **A platform drawing more
 *              than it can fetch is the number nobody currently sees.**
 *   drawn?     `wireframe.status`, which is `designed` only where a client pack
 *              exists — three platforms of fifteen. See the note on DRAWN below
 *              for why this is not the payload's own `undrawn` count.
 *   offline?   `offlineCapable` is a platform flag and also a screen flag, and
 *              nothing on any page has compared them.
 *   licensed?  the module spread — what a tenant sees when they buy less than
 *              everything.
 *
 * Two payloads. `/api/platforms` is the rollup of what the package derived —
 * `handoff/platform-<code>.json`, one per platform, with the four gap kinds
 * already computed. `/api/journeys` carries the screens themselves, which is
 * where the drawn and offline answers live. Fetched together; the alternative
 * is recomputing gaps in the browser, which is how a second source of truth
 * starts.
 */

import '/theme.js';   // the saved day/night choice, before anything paints
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const json = (path) => auth.apiFetch(path).then((r) => {
  if (!r.ok) throw new Error(`${path} answered ${r.status}`);
  return r.json();
});

/**
 * What each gap kind is called, and the order they are worth reading in.
 *
 * The keys are the package's, from `tools/derive-platform.py`. The classes are
 * `domains.css`'s, which already gives each kind its own column colour — so the
 * four are told apart by the stylesheet and named here, and neither file has to
 * know what the other calls them beyond this table.
 *
 * `head` is a sentence rather than a label because a count with no reading is a
 * number somebody has to be told the meaning of twice.
 */
const GAP_KINDS = [
  ['operationsWithNoScreen', 'plat-gap-a',
    'Operations with no screen',
    'In a contract this platform uses, callable by its audience, and reaching no screen anywhere. '
    + 'Either a screen is missing or the endpoint should not exist — and the second is worth '
    + 'considering first.'],
  ['screensNotDrawn', 'plat-gap-b',
    'Screens not drawn',
    'On paper, never seen. A screen nobody has looked at is a screen whose behaviour is still '
    + 'being imagined.'],
  ['modulesSplitAcrossWaves', 'plat-gap-c',
    'Modules split across waves',
    'Sells in one wave and cannot refund until a later one. The tenant gets half a capability '
    + 'and the gap is invisible in a screen count.'],
  ['flowsNamingAMissingScreen', 'plat-gap-d',
    'Flows naming a missing screen',
    'A journey steps through a screen that does not exist, so the journey cannot be walked.'],
];

/** At most this many rows per gap kind before the card says how many are left. */
const ROWS_SHOWN = 12;

const state = {
  platforms: [],      // the rollup, worst first
  byCode: new Map(),  // code -> { designed, generated, offlineScreens, modules, screens }
  stats: null,
  problems: [],
  open: new Set(),    // which cards are expanded
  sort: 'gaps',
  filter: '',
};

/**
 * The screen-level facts the derived pages do not carry.
 *
 * **DRAWN is read from `wireframe.status`, not from the payload's `undrawn`.**
 * That count means "has a board pointer", and every screen has one — the
 * fifteen that did not were filled in on 26 August. So it reads 0 everywhere
 * and distinguishes nothing. `status` is the fact that survives: `designed`
 * where a person drew the frame in a client pack, `generated` where
 * `derive-wireframes.py` rendered it from the screen definition. Those are
 * different claims about the same file and conflating them is the mistake that
 * put `designed` on twenty screens nobody had drawn.
 */
function screenFacts(screens) {
  const by = new Map();
  for (const s of screens ?? []) {
    const code = s.platform;
    if (!code) continue;
    if (!by.has(code)) {
      by.set(code, { designed: 0, generated: 0, offlineScreens: 0, screens: 0, modules: new Map() });
    }
    const row = by.get(code);
    row.screens += 1;
    const status = (s.wireframe ?? {}).status;
    if (status === 'designed') row.designed += 1;
    else row.generated += 1;
    if (s.offlineCapable) row.offlineScreens += 1;
    const mod = s.module || 'Unassigned';
    row.modules.set(mod, (row.modules.get(mod) ?? 0) + 1);
  }
  return by;
}

/** Operations a platform reaches, which is the denominator of "thin". */
const opCount = (p) => p.counts?.operations ?? 0;
const screenCount = (p) => p.counts?.screens ?? 0;

/**
 * The four sort orders the page shipped a control for.
 *
 * `undrawn` sorts by generated screens rather than by the payload's `undrawn`,
 * for the reason on `screenFacts` — otherwise the option would sort fifteen
 * zeroes and look broken.
 */
const SORTS = {
  gaps: (a, b) => b.gapTotal - a.gapTotal || a.code.localeCompare(b.code),
  code: (a, b) => a.code.localeCompare(b.code),
  size: (a, b) => screenCount(b) - screenCount(a) || a.code.localeCompare(b.code),
  undrawn: (a, b) => (state.byCode.get(b.code)?.generated ?? 0)
                   - (state.byCode.get(a.code)?.generated ?? 0)
                   || a.code.localeCompare(b.code),
};

function matches(p) {
  const needle = state.filter.trim().toLowerCase();
  if (!needle) return true;
  return [p.code, p.name, p.shortName, p.app, p.audience, p.formFactor]
    .filter(Boolean)
    .some((v) => String(v).toLowerCase().includes(needle));
}

/** One `label · value` fact, as the head's third and fourth columns want it. */
const facts = (parts) => parts.filter(Boolean).join(' · ');

function renderCard(p) {
  const f = state.byCode.get(p.code) ?? { designed: 0, generated: 0, offlineScreens: 0, modules: new Map() };
  const screens = screenCount(p);
  const ops = opCount(p);
  const open = state.open.has(p.code);

  const card = el('div', `plat-card${p.gapTotal ? '' : ' plat-clean'}${open ? ' open' : ''}`);

  // ---- head: the five columns domains.css lays out -------------------------
  const head = el('div', 'plat-head');
  head.tabIndex = 0;
  head.setAttribute('role', 'button');
  head.setAttribute('aria-expanded', String(open));
  head.append(
    el('span', 'plat-code', p.code),
    el('span', 'plat-name', p.shortName || p.name || p.code),
    el('span', 'plat-app', facts([p.app, p.audience, p.formFactor])),
    el('span', 'plat-counts', facts([
      `${screens} screen${screens === 1 ? '' : 's'}`,
      `${ops} op${ops === 1 ? '' : 's'}`,
      f.designed ? `${f.designed} drawn` : null,
    ])),
  );
  const badge = el('span', `plat-gap-badge${p.gapTotal ? '' : ' none'}`,
    p.gapTotal ? `${p.gapTotal} gap${p.gapTotal === 1 ? '' : 's'}` : 'no gaps');
  head.append(badge);

  const toggle = () => {
    if (state.open.has(p.code)) state.open.delete(p.code);
    else state.open.add(p.code);
    draw();
  };
  head.onclick = toggle;
  head.onkeydown = (e) => {
    // A head that answers the mouse and not the keyboard is a control half the
    // readers of this page cannot use.
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
  };
  card.append(head);

  if (!open) return card;

  // ---- body ---------------------------------------------------------------
  const body = el('div', 'plat-body');

  // **A platform with no screens must still render.** Every folder in a package
  // is optional and the Audit says what is missing rather than the server
  // failing; this page behaves the same way. A blank div would read as "fine".
  if (!screens) {
    body.append(el('p', 'plat-none',
      `${p.code} has a derived page and no screens behind it. `
      + 'Either its screen file has not been written or it should not be registered.'));
    card.append(body);
    return card;
  }

  // thin? — the ratio nobody currently sees
  const perScreen = screens ? (ops / screens) : 0;
  const thin = ops < screens;
  body.append(el('p', 'plat-none', thin
    ? `${ops} operations behind ${screens} screens — ${perScreen.toFixed(1)} per screen. `
      + 'This platform draws more than it can fetch.'
    : `${ops} operations behind ${screens} screens — ${perScreen.toFixed(1)} per screen.`));

  // drawn?
  body.append(el('p', 'plat-none', f.designed
    ? `${f.designed} of ${screens} screens drawn by hand; ${f.generated} rendered from the screen definitions.`
    : `None of ${screens} screens is drawn. Every frame is rendered from the screen definition, `
      + 'which is a wireframe rather than a design.'));

  // offline? — the platform flag against the screen flags
  if (p.offlineCapable || f.offlineScreens) {
    const agree = p.offlineCapable
      ? `${f.offlineScreens} of ${screens} screens declare an offline state.`
      : `${f.offlineScreens} screen${f.offlineScreens === 1 ? '' : 's'} declare${f.offlineScreens === 1 ? 's' : ''} `
        + 'offline behaviour on a platform not marked offline-capable — the two flags disagree.';
    body.append(el('p', 'plat-none', agree));
  }

  // licensed? — the module spread, as the wave chips the CSS already styles
  const modules = [...f.modules.entries()].sort((a, b) => b[1] - a[1]);
  if (modules.length) {
    const strip = el('div', 'plat-waves');
    strip.append(el('span', 'plat-waves-label',
      `${modules.length} module${modules.length === 1 ? '' : 's'}`));
    for (const [name, n] of modules.slice(0, 10)) {
      strip.append(el('span', 'plat-wave', `${name} ${n}`));
    }
    if (modules.length > 10) strip.append(el('span', 'plat-waves-label', `+${modules.length - 10} more`));
    body.append(strip);
  }

  // ---- the four gap kinds -------------------------------------------------
  let any = false;
  for (const [key, cls, title, why] of GAP_KINDS) {
    const rows = (p.gaps ?? {})[key] ?? [];
    if (!rows.length) continue;
    any = true;
    const block = el('div', 'plat-gap');
    block.append(el('div', 'plat-gap-head', `${title} — ${rows.length}`));
    block.append(el('p', 'plat-gap-more', why));
    const box = el('div', 'plat-gap-rows');
    for (const row of rows.slice(0, ROWS_SHOWN)) {
      const line = el('div', 'plat-gap-row');
      // The derived rows are not one shape — an operation gap names an
      // operation and a contract, a wave gap names a module and its waves. Four
      // cells, filled with whatever that kind carries, rather than four
      // renderers that would each go stale on their own.
      const cells = typeof row === 'string'
        ? [row, '', '', '']
        : [row.operationId ?? row.module ?? row.screen ?? row.id ?? row.name ?? '',
           row.contract ?? row.flow ?? row.platform ?? '',
           row.waves ? row.waves.join(', ') : (row.wave ?? ''),
           row.note ?? row.reason ?? row.purpose ?? row.title ?? ''];
      line.append(
        el('span', cls, String(cells[0])),
        el('span', 'plat-gap-b', String(cells[1])),
        el('span', 'plat-gap-c', String(cells[2])),
        el('span', 'plat-gap-d', String(cells[3])),
      );
      box.append(line);
    }
    if (rows.length > ROWS_SHOWN) {
      box.append(el('div', 'plat-gap-more', `${rows.length - ROWS_SHOWN} more not listed`));
    }
    block.append(box);
    body.append(block);
  }

  if (!any) {
    body.append(el('p', 'plat-none',
      'No gap of any of the four kinds. Every operation this platform can call reaches a screen, '
      + 'every module ships in one wave, and every flow finds the screens it names.'));
  }

  card.append(body);
  return card;
}

function draw() {
  const box = $('platforms');
  box.textContent = '';

  const rows = state.platforms.filter(matches).sort(SORTS[state.sort] ?? SORTS.gaps);

  if (!state.platforms.length) {
    box.append(el('p', 'plat-none',
      'This package registers no platforms. `screens/P*.yaml` is where they come from, and it is '
      + 'either absent or holds nothing — every folder in a package is optional.'));
    return;
  }
  if (!rows.length) {
    box.append(el('p', 'plat-none', `Nothing matches “${state.filter}”.`));
    return;
  }

  for (const p of rows) box.append(renderCard(p));
}

function renderLead() {
  const s = state.stats;
  if (!s) return;
  const drawn = [...state.byCode.values()].reduce((n, f) => n + f.designed, 0);
  const undrawnPlatforms = state.platforms
    .filter((p) => !(state.byCode.get(p.code)?.designed)).length;
  $('plat-lead').textContent =
    `${s.platforms} platforms · ${s.screens} screens · ${s.gaps} gaps across ${s.withGaps} of them, `
    + `${s.clean} clean. ${drawn} screens are drawn by hand; ${undrawnPlatforms} platforms have none. `
    + `Derived ${s.generated}.`;
}

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();

  const me = auth.account();
  // Optional: inside the viewer these views are sections of a page that
  // already says who you are, so there is no `#whoami` to fill.
  $('whoami')?.replaceChildren(me ? `${me.name || me.email} · ${me.role}` : '');

  let platforms, journeys;
  try {
    [platforms, journeys] = await Promise.all([json('/api/platforms'), json('/api/journeys')]);
  } catch (error) {
    hideLoader();
    $('plat-lead').textContent = `Could not read the package: ${error.message}`;
    return;
  }

  state.platforms = platforms.platforms ?? [];
  state.stats = platforms.stats;
  state.problems = platforms.problems ?? [];
  state.byCode = screenFacts(journeys.screens);

  // A platform whose derived page is missing is reported by `lib/platforms.mjs`
  // rather than skipped silently — absence would otherwise read as "no gaps".
  if (state.problems.length) {
    const box = $('platforms');
    for (const problem of state.problems) {
      box.append(el('p', 'plat-none', problem.message));
    }
  }

  renderLead();
  draw();
  hideLoader();

  $('plat-filter').oninput = (e) => { state.filter = e.target.value; draw(); };
  $('plat-sort').onchange = (e) => { state.sort = e.target.value; draw(); };
})();
