/**
 * The editor beside the sign-in form. From `ui-design/AUTH.md`.
 *
 * It is an argument, not an animation. "A context layer for AI-assisted
 * development" is a sentence nobody can picture, so the page shows the thing
 * instead: a file from the package being read, and a finding falling out of
 * the end of it. Every line and every chip below is real — the illegal
 * `HELD → REFUNDED` pair is in the enum, the 192 screens really do reach no
 * operation, the six tables really are written by two services each. Nothing
 * here is lorem, because a number invented for a login screen is a promise the
 * product then has to keep.
 *
 * Two things it is careful about:
 *
 *   1. **The window never resizes.** All nine rows exist from the first frame
 *      as empty strings, the code body has a floor of 238px and the tray one
 *      of 56px. A window that grew a line at a time would walk the whole right
 *      column up and down for as long as anybody watched it.
 *   2. **Nothing that animates is rebuilt.** The caret is a `::after` on the
 *      active row rather than an element inserted into it, and a finding chip
 *      is appended once — both blink and rise over hundreds of milliseconds,
 *      and a tick every 46ms would restart them forever and neither would ever
 *      be seen.
 *
 * Colour is the stylesheet's. A line is authored as `[text, token]` and the
 * token becomes a class, so the night and day palettes are two blocks of CSS
 * over identical scene data — and a reader who changes theme mid-scene gets
 * the new palette immediately rather than whatever hex was baked in at render.
 */

import { prefersStillness } from './auth-bg.js';

const TICK_MS = 46;

/** Three at a time, not one. At this line length a character per tick reads as
 *  a machine thinking rather than a machine typing. */
const BURST = 3;

/** Six files, one per language the delivery package actually contains. */
const SCENES = [
  {
    file: 'contracts/orders.yaml', lang: 'yaml', status: 'parsing',
    lines: [
      ['openapi: 3.1.0', 'com'],
      ['info:', 'key'],
      ['  title: orders', 'val'],
      ['  x-tier: spine', 'val'],
      ['paths:', 'key'],
      ['  /orders/{id}/hold:', 'acc'],
      ['    post:', 'key'],
      ['      operationId: holdOrder', 'val'],
      ['      x-emits: [order.held]', 'warn'],
    ],
    out: [
      ['71 operations', 'ok'],
      ['9 states resolved', 'ok'],
      ['5 critical consumers', 'ok'],
      ['held → refunded not permitted', 'warn'],
    ],
  },
  {
    file: 'adrov/resolve_refs.py', lang: 'python', status: 'resolving',
    lines: [
      ['from adrov.graph import Contract, Ref', 'com'],
      ['', 'val'],
      ['def resolve(spec: dict) -> list[Ref]:', 'key'],
      ['    out = []', 'val'],
      ['    for path, ops in spec["paths"].items():', 'key'],
      ['        for verb, op in ops.items():', 'key'],
      ['            out += walk(op, path, verb)', 'acc'],
      ['    return dedupe(out)', 'key'],
      ['# 2 refs cross a contract boundary', 'warn'],
    ],
    out: [
      ['1,043 refs walked', 'ok'],
      ['2 shared contracts', 'ok'],
      ['0 cycles', 'ok'],
      ['2 boundary crossings', 'warn'],
    ],
  },
  {
    file: 'OrderStateMachine.java', lang: 'java', status: 'checking',
    lines: [
      ['public enum OrderStatus {', 'key'],
      ['    PENDING, HELD, PARTIALLY_PAID, PAID,', 'val'],
      ['    REFUNDED, VOIDED, FAILED, COMPLETED;', 'val'],
      ['', 'val'],
      ['    boolean canMoveTo(OrderStatus next) {', 'key'],
      ['        return TRANSITIONS', 'acc'],
      ['            .getOrDefault(this, Set.of())', 'acc'],
      ['            .contains(next);', 'acc'],
      ['    } // enum permits HELD → REFUNDED', 'warn'],
    ],
    out: [
      ['9 states', 'ok'],
      ['14 transitions', 'ok'],
      ['5 reversals', 'ok'],
      ['1 illegal pair in enum', 'warn'],
    ],
  },
  {
    file: 'migrations/0041_seat_holds.sql', lang: 'sql', status: 'reading',
    lines: [
      ['-- wave 2 · owned by inventory-service', 'com'],
      ['CREATE TABLE seat_holds (', 'key'],
      ['  id           uuid PRIMARY KEY,', 'val'],
      ['  performance  uuid NOT NULL,', 'val'],
      ['  expires_at   timestamptz NOT NULL,', 'val'],
      ['  channel      text NOT NULL', 'val'],
      [');', 'key'],
      ['CREATE INDEX ON seat_holds (expires_at);', 'acc'],
      ['-- written by 2 services', 'warn'],
    ],
    out: [
      ['224 tables', 'ok'],
      ['41 migrations', 'ok'],
      ['18 services', 'ok'],
      ['6 tables shared', 'warn'],
    ],
  },
  {
    file: 'client/useAvailability.ts', lang: 'typescript', status: 'linking',
    lines: [
      ['import { getAvailability } from "@adrov/orders";', 'com'],
      ['', 'val'],
      ['export function useAvailability(id: string) {', 'key'],
      ['  return useQuery({', 'acc'],
      ['    queryKey: ["availability", id],', 'val'],
      ['    queryFn: () => getAvailability(id),', 'val'],
      ['    staleTime: 0, // never cached', 'com'],
      ['  });', 'acc'],
      ['}', 'key'],
    ],
    out: [
      ['4 components', 'ok'],
      ['3 states declared', 'ok'],
      ['reaches nothing', 'warn'],
      ['192 screens the same', 'warn'],
    ],
  },
  {
    file: 'screens/WEB-002.json', lang: 'json', status: 'indexing',
    lines: [
      ['{', 'com'],
      ['  "id": "WEB-002",', 'val'],
      ['  "platform": "P01",', 'val'],
      ['  "template": "list",', 'val'],
      ['  "components": [', 'key'],
      ['    { "kind": "searchField" },', 'acc'],
      ['    { "kind": "cardList" }', 'acc'],
      ['  ],', 'key'],
      ['  "operations": []', 'warn'],
    ],
    out: [
      ['492 screens', 'ok'],
      ['15 platforms', 'ok'],
      ['478 reach an operation', 'ok'],
      ['14 reach nothing', 'warn'],
    ],
  },
];

const ROWS = SCENES[0].lines.length;

export function startSigninDemo(root) {
  if (!root) return () => {};

  const file = root.querySelector('.signin-file');
  const lang = root.querySelector('.signin-lang');
  const status = root.querySelector('.signin-status-text');
  const code = root.querySelector('.signin-code');
  const tray = root.querySelector('.signin-findings');
  if (!file || !lang || !status || !code || !tray) return () => {};

  // The nine rows, once. After this the loop only ever writes textContent and
  // a class name into them.
  const rows = [];
  for (let i = 0; i < ROWS; i += 1) {
    const gutter = document.createElement('span');
    gutter.className = 'signin-n';
    gutter.textContent = String(i + 1).padStart(2, '0');
    const line = document.createElement('span');
    line.className = 'signin-line';
    code.append(gutter, line);
    rows.push(line);
  }

  // Which file a visitor lands on is random, and so is every file after it, so
  // two people signing in a minute apart do not watch the same thing.
  const state = {
    scene: Math.floor(Math.random() * SCENES.length),
    step: 0,
    chars: 0,
    findings: 0,
  };

  function render() {
    const scene = SCENES[state.scene];
    file.textContent = scene.file;
    lang.textContent = scene.lang;
    status.textContent = state.step < scene.lines.length ? scene.status : 'done';

    scene.lines.forEach(([text, token], i) => {
      const typing = i === state.step;
      rows[i].className = `signin-line tok-${token}${typing ? ' is-typing' : ''}`;
      rows[i].textContent = i < state.step ? text : typing ? text.slice(0, state.chars) : '';
    });

    // Only ever append. The chips are cleared in one go when a scene ends,
    // which is the only moment their count goes down.
    if (state.findings < tray.childElementCount) tray.replaceChildren();
    for (let i = tray.childElementCount; i < state.findings; i += 1) {
      const [text, tone] = scene.out[i];
      const chip = document.createElement('span');
      chip.className = `signin-finding ${tone}`;
      chip.append(document.createElement('i'), document.createTextNode(text));
      tray.append(chip);
    }
  }

  // Somebody who asked for stillness gets the last scene as it ends: fully
  // typed, every finding shown, no caret and no interval.
  if (prefersStillness()) {
    state.scene = SCENES.length - 1;
    state.step = ROWS;
    state.findings = SCENES[state.scene].out.length;
    render();
    return () => {};
  }

  // One thing per tick, in this order: type, or move to the next line, or
  // reveal a finding, or start a different file.
  function tick() {
    const scene = SCENES[state.scene];
    const line = scene.lines[state.step];
    if (line) {
      if (state.chars < line[0].length) {
        state.chars = Math.min(line[0].length, state.chars + BURST);
      } else {
        state.step += 1;
        state.chars = 0;
      }
    } else if (state.findings < scene.out.length) {
      state.findings += 1;
    } else {
      let next = state.scene;
      while (SCENES.length > 1 && next === state.scene) {
        next = Math.floor(Math.random() * SCENES.length);
      }
      state.scene = next;
      state.step = 0;
      state.chars = 0;
      state.findings = 0;
    }
    render();
  }

  let timer = null;
  const play = () => { if (timer == null) timer = setInterval(tick, TICK_MS); };
  const pause = () => { if (timer != null) { clearInterval(timer); timer = null; } };
  // A hidden tab is typing to nobody, and the browser would throttle the
  // interval to once a second anyway — which on return would land mid-word.
  const onVisibility = () => (document.hidden ? pause() : play());

  render();
  document.addEventListener('visibilitychange', onVisibility);
  play();

  return function stop() {
    pause();
    document.removeEventListener('visibilitychange', onVisibility);
  };
}
