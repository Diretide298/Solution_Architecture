// Hover tips.
//
// The viewer is dense with vocabulary that is obvious to whoever wrote the
// delivery and opaque to everyone else: `spine`, `ambient`, `dataTable`,
// `retryThenDeadLetter`, `posTerminal`, "inferred", "declared", "reversal".
// Most of it is explained *somewhere* — in `screens/_components.yaml`, in a
// contract description, in an ADR — and none of it was reachable from the thing
// on screen.
//
// So: anything can carry `data-tip`, and hovering it explains itself. Two
// sources feed it.
//
//   the delivery's own words   — a component's description from the shared
//                                library, a permission's description, a
//                                contract's summary. Always preferred: it is
//                                what the project actually says.
//   the glossary below         — the viewer's own vocabulary, and the delivery
//                                terms that are defined in prose no file holds
//                                in a field.
//
// The browser's own `title=` is not enough for this: it takes about a second to
// appear, cannot be styled, cannot hold a heading and a body, and is invisible
// on touch. It is still set on a few things as a fallback for copy-paste.

/**
 * The viewer's vocabulary, and the delivery's where no file states it.
 *
 * Keyed by the exact token that appears on screen wherever possible, so a chip
 * reading `retryThenDeadLetter` needs no mapping table at the call site.
 */
export const GLOSSARY = {
  // ── contract tiers ──────────────────────────────────────────────
  spine: {
    title: 'Spine contract',
    body:
      'One of the eight contexts everything else depends on — tenancy, identity, catalogue, ' +
      'orders, shift, access, finance, cross-cell. Frozen first. A change here needs a formal ' +
      'change request, because every satellite has pinned against it.',
  },
  satellite: {
    title: 'Satellite contract',
    body:
      'A domain that builds on the spine and can move independently. Cheaper to change, ' +
      'because nothing else has pinned against it.',
  },
  shared: {
    title: 'Shared contract',
    body:
      '`common.yaml` and `permissions.yaml` — the types and the permission vocabulary every ' +
      'other contract $refs. All 44 file-level links in the whole set point here.',
  },

  // ── how a link was established ──────────────────────────────────
  declared: {
    title: 'Declared',
    body:
      'Someone wrote this down: a $ref, a REFERENCES clause in the DDL, a screen naming its ' +
      'board. It can be wrong, but it cannot be a guess.',
  },
  inferred: {
    title: 'Inferred',
    body:
      'The viewer worked this out — usually from a column name or a file name — because ' +
      'nothing declares it. Drawn dashed and counted separately everywhere, so a guess is ' +
      'never mistaken for a fact.',
  },

  // ── the data view ───────────────────────────────────────────────
  ambient: {
    title: 'Ambient key',
    body:
      'A key to one of the four hub tables — venue, principal, subject, tenant. ' +
      '`platform.scope_node` is referenced by 64 tables and `identity.principal` by 69, so ' +
      'these edges are true of nearly every table and therefore say nothing about this one. ' +
      'Hidden by default for that reason.',
  },
  child: {
    title: 'Child relationship',
    body: 'This row belongs to that row and has no meaning without it. Drawn heaviest.',
  },
  reference: {
    title: 'Reference',
    body: 'This row points at that row. The ordinary case.',
  },

  // ── the domain layer ────────────────────────────────────────────
  reversal: {
    title: 'Reversal',
    body:
      'A transition that undoes an earlier one. Marked because reversals are where money and ' +
      'entitlements move backwards, and they carry different approval requirements.',
  },
  approval: {
    title: 'Needs approval',
    body: 'A person with the right grant has to authorise this before it happens.',
  },
  initial: {
    title: 'Initial state',
    body: 'A state an entity may be created in. Usually one; occasionally several, where a record can be created already advanced.',
  },
  terminal: {
    title: 'Terminal state',
    body:
      'Nothing leaves here. An entity in a terminal state is finished — and the check that ' +
      'every state can reach one is what catches a state that traps records.',
  },
  offline: {
    title: 'Reachable offline',
    body:
      'A terminal can enter this state with no network. Everything else needs the server. On ' +
      'a POS this is the difference between a sale that completes and one that cannot.',
  },
  critical: {
    title: 'Critical consumer',
    body:
      'The business breaks if this consumer never runs. It drives alerting: a dead-lettered ' +
      'critical event is a page, not a dashboard.',
  },
  idempotencyKey: {
    title: 'Idempotency key',
    body:
      'What makes a redelivery a duplicate. Required, because delivery is at-least-once — this ' +
      'is the difference between a correct consumer and one that works until it does not.',
  },
  retry: { title: 'On failure: retry', body: 'Keep retrying. Nothing is given up on.' },
  retryThenDeadLetter: {
    title: 'On failure: retry, then dead-letter',
    body: 'Retry a bounded number of times, then park it for a human. The usual choice for anything critical.',
  },
  deadLetterImmediately: {
    title: 'On failure: dead-letter immediately',
    body: 'Do not retry. Park it for a human on the first failure.',
  },
  ignore: { title: 'On failure: ignore', body: 'Drop it. Only defensible where the consumer is advisory.' },

  // ── transition triggers ─────────────────────────────────────────
  operation: { title: 'Trigger: operation', body: 'An API call in a contract causes this move.' },
  timer: {
    title: 'Trigger: timer',
    body: 'A clock causes this move, with nobody watching. No operation in any contract produces it, which is why it is drawn dashed.',
  },
  job: {
    title: 'Trigger: job',
    body: 'A background job causes this move. No operation in any contract produces it, which is why it is drawn dashed.',
  },
  externalEvent: { title: 'Trigger: external event', body: 'An event from another context causes this move.' },
  cascade: { title: 'Trigger: cascade', body: 'A change to a parent record causes this move.' },

  // ── the frontend layer ──────────────────────────────────────────
  loading: { title: 'Loading state', body: 'What the screen shows while it is waiting. One of the four every screen must declare.' },
  empty: {
    title: 'Empty state',
    body: 'What the screen shows with nothing to show. The one that reaches production unconsidered.',
  },
  error: { title: 'Error state', body: 'What the screen shows when the call fails, and what the person can do next.' },
  denied: { title: 'Permission-denied state', body: 'What the screen shows to someone without the grant. Not the same as empty.' },

  // ── triggers on a screen's API calls ────────────────────────────
  onLoad: { title: 'Called on load', body: 'Fires when the screen opens. These decide how fast it feels.' },
  onAction: { title: 'Called on an action', body: 'Fires when the person does something.' },
  onInterval: { title: 'Called on a timer', body: 'Polls. Worth knowing about on an offline-capable surface.' },
  background: { title: 'Called in the background', body: 'Fires without the person waiting on it.' },

  // ── backend ─────────────────────────────────────────────────────
  FORCED: {
    title: 'Row security FORCED',
    body:
      'Row-level security applies to the table owner too. Merely `ENABLED` exempts the owner, ' +
      'which is usually the application role — so `ENABLED` alone is often no protection at all.',
  },
  partitioned: { title: 'Partitioned', body: 'Split into physical child tables. The parent holds no rows of its own.' },
  generated: { title: 'Generated column', body: 'The database computes it. Nothing may write it.' },
};

/** A tip whose body is the delivery's own words rather than the glossary's. */
// ── the counts the tips quote ────────────────────────────────────────
//
// Every number these tips stated was typed into the sentence, and every one of
// them drifted: **654 operations against a live 1,023, 22 services against 16,
// 18 ADRs against 30**, and "318 of the 654 resolve to no table" against a
// lineage in which nothing is unresolved at all. `lib/lineage.mjs` had already
// written the epitaph — *"a number in a comment is a claim nothing checks"* —
// and the tips were the same claim, on screen, where a reader would believe it.
//
// So a tip writes `{operations}` and the count arrives at hover. Substituted
// in `show`, because that is the one place the two sources meet: a body set by
// `tip()` and a `data-tip=` written in index.html are the same dataset field by
// then, and a fix at either call site would have missed the other.
//
// The provider is injected rather than imported: core.js imports this module,
// and a cycle to fetch a number is a poor trade.
//
// An unknown token renders as `{token}` rather than disappearing. A visible
// placeholder is a bug report; a silently dropped one is the drift again.
let factProvider = () => ({});

/** Called once at boot with something that reads the live payload. */
export const setFactProvider = (fn) => { factProvider = fn; };

const FACT_TOKEN = /\{([A-Za-z][A-Za-z0-9]*)\}/g;

const withFacts = (text) => {
  if (!text || !text.includes('{')) return text;
  const facts = factProvider() ?? {};
  return text.replace(FACT_TOKEN, (whole, key) => {
    const value = facts[key];
    return value === undefined || value === null ? whole : String(value);
  });
};

export const tip = (element, title, body, extra) => {
  if (!element || (!title && !body)) return element;
  element.dataset.tipTitle = title ?? '';
  element.dataset.tip = body ?? '';
  if (extra) element.dataset.tipExtra = extra;
  return element;
};

/** Attach a glossary entry by key. Silently does nothing for an unknown key. */
export const tipFor = (element, key) => {
  const entry = GLOSSARY[key];
  return entry ? tip(element, entry.title, entry.body) : element;
};

/**
 * One floating panel, driven by delegation — so anything added to the DOM
 * later carries tips without being wired up individually.
 *
 * Hover is the desktop gesture and it does not exist on a phone. Tap is taken:
 * most things carrying a tip carry a click too — a tree row, a mode button, a
 * chip that navigates — so tap-to-explain would cost tap-to-go. Press and hold
 * is the one gesture nothing here already uses, so that is the touch gesture,
 * and the click it would otherwise be followed by is swallowed.
 *
 * A touch device produces no "the pointer left" event of any kind, so on that
 * path the panel is closed by the next press anywhere, by any scroll, by
 * Escape, and failing all of those by a timer. It cannot be left open.
 */
export function installTips(root = document.body) {
  const panel = document.createElement('div');
  panel.className = 'tip-panel';
  panel.hidden = true;
  document.body.append(panel);

  // read per event rather than once: a tablet gains and loses a mouse
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)');

  const LONG_PRESS = 450; // shorter reads as a slow tap; longer as a hang
  const MOVE_CANCEL = 10; // a scroll that started on a tipped row is a scroll
  const AUTO_HIDE = 6000;

  let current = null;
  let timer = null;
  let pressTimer = null;
  let expiry = null;
  let pressFrom = null;
  let swallowClick = false;

  const hide = () => {
    clearTimeout(timer);
    clearTimeout(pressTimer);
    clearTimeout(expiry);
    pressFrom = null;
    current = null;
    panel.hidden = true;
  };

  const show = (target) => {
    const title = withFacts(target.dataset.tipTitle ?? '');
    const body = withFacts(target.dataset.tip ?? '');
    const extra = withFacts(target.dataset.tipExtra ?? '');
    panel.innerHTML = '';
    if (title) {
      const head = document.createElement('div');
      head.className = 'tip-title';
      head.textContent = title;
      panel.append(head);
    }
    if (body) {
      const text = document.createElement('div');
      text.className = 'tip-body';
      // the delivery writes **bold** and `code` in its descriptions
      text.innerHTML = body
        .replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c])
        .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
        .replace(/`([^`]+)`/g, '<code>$1</code>');
      panel.append(text);
    }
    if (extra) {
      const note = document.createElement('div');
      note.className = 'tip-extra';
      note.textContent = extra;
      panel.append(note);
    }
    panel.hidden = false;
    position(target);
  };

  const position = (target) => {
    const box = target.getBoundingClientRect();
    const tipBox = panel.getBoundingClientRect();
    const margin = 10;
    // prefer below; flip above when there is no room, and never leave the window
    let top = box.bottom + 8;
    if (top + tipBox.height > window.innerHeight - margin) top = box.top - tipBox.height - 8;
    top = Math.max(margin, top);
    let left = box.left;
    if (left + tipBox.width > window.innerWidth - margin) {
      left = window.innerWidth - tipBox.width - margin;
    }
    panel.style.top = `${Math.round(top)}px`;
    panel.style.left = `${Math.round(Math.max(margin, left))}px`;
  };

  root.addEventListener(
    'mouseover',
    (event) => {
      // a tap synthesises mouseover and then never a matching mouseout, which
      // is exactly how a panel gets stuck open
      if (!canHover.matches) return;
      const target = event.target.closest?.('[data-tip], [data-tip-title]');
      if (!target || target === current) return;
      current = target;
      clearTimeout(timer);
      // short enough not to feel like waiting, long enough that sweeping the
      // pointer across a row of chips does not flash six panels
      timer = setTimeout(() => show(target), 220);
    },
    true
  );

  root.addEventListener(
    'mouseout',
    (event) => {
      const target = event.target.closest?.('[data-tip], [data-tip-title]');
      if (target && target === current) hide();
    },
    true
  );

  // ── press and hold, on anything that is not a mouse ────────────────
  root.addEventListener(
    'pointerdown',
    (event) => {
      // the mouse path is hover's, and a mousedown that closed the tip would
      // be a change to how this already behaves on a desktop
      if (event.pointerType === 'mouse') return;
      // a new gesture: whatever else this press turns out to be it closes the
      // open panel, and any swallow the last one armed and never spent is stale
      swallowClick = false;
      hide();
      const target = event.target.closest?.('[data-tip], [data-tip-title]');
      if (!target) return;
      pressFrom = { x: event.clientX, y: event.clientY };
      pressTimer = setTimeout(() => {
        current = target;
        swallowClick = true;
        show(target);
        expiry = setTimeout(hide, AUTO_HIDE);
      }, LONG_PRESS);
    },
    true
  );

  root.addEventListener(
    'pointermove',
    (event) => {
      if (!pressFrom) return;
      if (Math.hypot(event.clientX - pressFrom.x, event.clientY - pressFrom.y) > MOVE_CANCEL) {
        clearTimeout(pressTimer);
        pressFrom = null;
      }
    },
    true
  );

  const endPress = () => {
    clearTimeout(pressTimer);
    pressFrom = null;
  };
  root.addEventListener('pointerup', endPress, true);
  root.addEventListener('pointercancel', () => { endPress(); hide(); }, true);

  // holding a row asked for the explanation, not for the row's own action
  root.addEventListener(
    'click',
    (event) => {
      if (!swallowClick) return;
      swallowClick = false;
      event.stopPropagation();
      event.preventDefault();
    },
    true
  );

  // the platform's own long-press menu would land on top of the panel
  root.addEventListener('contextmenu', (event) => {
    if (pressFrom || current) event.preventDefault();
  });

  // a tip pinned to something that has scrolled away is worse than no tip
  window.addEventListener('scroll', hide, true);
  window.addEventListener('keydown', (e) => e.key === 'Escape' && hide());
  return { hide };
}
