/**
 * Every design board there is, read off the disk rather than off the screens.
 *
 * `buildWireframes` describes only the boards something already points at —
 * `for (const [lower, rel] of referenced)`. That is right for its job, which is
 * putting a frame on a screen's page. It is also why **21 of the 56 boards were
 * invisible in the viewer**: the whole Inventory pack, three F&B boards, `POS
 * Board 6`, the eight boards left behind when their platforms were renamed, and
 * `TICVAI All Boards Index.dc.html` — a hand-built catalogue of 255 frame links
 * that every one of which resolves, reachable from nothing.
 *
 * A board nobody has wired up is not a board that does not exist. It is the one
 * most worth seeing, because somebody drew it and the package cannot say what
 * it draws. So this reads the directory.
 *
 * Three folders, because they are the same kind of artefact and were split by
 * where they came from rather than by what they are:
 *
 *   wireframes/          the platform boards and the client's topic packs
 *   designs/             the design-language boards
 *   ui-design/designs/   the drawn product design — the finished treatment of
 *                        the screens the wireframes only block out
 *
 * The third was invisible for the same reason the unwired boards were, one
 * level up: this read two directory names and there were three. Seven boards —
 * sign-in, invite, landing and the topbar, each in day and night — drawn,
 * committed, and reachable from nowhere in the viewer.
 *
 * `id` and `dir` are separate here because that folder is nested. The id is
 * what the board's URL and its grouping are keyed on, so it has to stay a
 * single segment; the dir is where the files are.
 *
 * A frame's name comes from whichever source actually knows it:
 *
 *   `.ttl`     the generated boards title every frame themselves — 24 of 24 on
 *              `P04 Venue POS`, 46 of 46 on `P01 Guest Web`
 *   a screen   the client packs do not. Their `data-screen-label` is the anchor
 *              in capitals — `SEAT-3A` for `seat-3a` — which names nothing. What
 *              names those frames is the screen that points at them, which is
 *              why the mapping work matters and why an unmapped pack shows
 *              anchors and no names.
 *   the anchor last, and marked as such, so "we do not know" never renders as
 *              though it were a title.
 */

import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const FOLDERS = [
  { id: 'wireframes', dir: 'wireframes', label: 'Wireframes' },
  { id: 'designs', dir: 'designs', label: 'Design language' },
  { id: 'ui-design', dir: 'ui-design/designs', label: 'Product design' },
];

/** The same pattern `buildWireframes` matches anchors with, and for its reasons:
 *  a board is full of layout divs with ids of their own, and a set containing
 *  every id can never report a missing anchor. */
const ANCHOR = /\bid="([A-Za-z]{2,5}-\d[\dA-Za-z]{0,3})"/gi;

/**
 * What counts as a board.
 *
 * `wireframes/` holds 70 top-level HTML files and only 56 are boards; the rest
 * are `flow-f01.html` and friends, one generated render of a single flow. There
 * is a `screens/` subdirectory of the same kind, one file per screen, which is
 * not read here at all.
 *
 * The obvious test is the `<x-dc>` element, and it is wrong: **the 15 generated
 * platform boards do not have one.** `P01 Guest Web.dc.html` is plain HTML out
 * of `derive-wireframes.py`, and only the 40 client packs come from the design
 * tool. Testing for `<x-dc>` drops every platform board and keeps every pack,
 * which looks like a working filter right up until you count.
 *
 * The name is what both conventions agree on — `.dc.html` in `wireframes/`,
 * `_dc.html` in `designs/`.
 */
const IS_BOARD = /[._]dc\.html$/i;

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', '#39': "'" };
const decode = (text) =>
  String(text ?? '').replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (whole, name) => {
    const key = name.toLowerCase();
    if (ENTITIES[key]) return ENTITIES[key];
    if (key.startsWith('#x')) return String.fromCodePoint(parseInt(key.slice(2), 16));
    if (key.startsWith('#')) return String.fromCodePoint(Number(key.slice(1)));
    return whole;
  }).trim();

const titleOf = (html) => decode(/<title>([^<]*)<\/title>/i.exec(html.slice(0, 4000))?.[1] ?? '') || null;

/** `POS Board 1.dc.html` -> { name: 'POS Board 1', revision: null };
 *  `Park_POS_v1_dc.html` -> { name: 'Park POS', revision: 'v1' }. */
function nameOf(file) {
  const stem = file.replace(/\.dc\.html$/i, '').replace(/\.html?$/i, '').replace(/_dc$/i, '');
  const parts = stem.split(/[_\s]+/).filter(Boolean);
  const last = parts[parts.length - 1];
  const revision = /^v\d+(\.\d+)*$/i.test(last ?? '') ? parts.pop().toLowerCase() : null;
  return { name: parts.join(' ') || stem, revision };
}

/**
 * What kind of thing this file is, which decides how it is read and what a
 * reader should expect of it.
 *
 * Three of the four exist because "0 frames" would otherwise read as broken on
 * a file that is working exactly as intended:
 *
 *   index    `TICVAI All Boards Index` has 255 links and no frames. It is a
 *            contents page, not an empty board.
 *   single   the two `designs/` boards have no `id` attributes at all. They are
 *            one artboard each, not a board of many, so there is nothing for the
 *            anchor pattern to find and nothing missing.
 *   generated  drawn by `derive-wireframes.py` from the screen definitions, so
 *            it titles its own frames and is regenerated on every refresh.
 *   pack     drawn by hand in the design tool. The thing a reviewer means.
 */
function kindOf(file, anchorCount, linkCount) {
  if (anchorCount === 0 && linkCount > 20) return 'index';
  if (anchorCount === 0) return 'single';
  if (/^P\d{2}\b/.test(file)) return 'generated';
  return 'pack';
}

const urlFor = (folder, rel) =>
  `/${folder}/${rel.split('/').map(encodeURIComponent).join('/')}`;

/** `wireframes/POS Board 1.dc.html#pos-4a` -> { rel, anchor } */
function splitRef(ref) {
  if (typeof ref !== 'string' || !ref.trim()) return null;
  const [target, anchor = null] = ref.trim().split('#');
  const rel = target.replace(/^\.?\/*/, '').replace(/^(wireframes|designs)\//i, '');
  return rel ? { rel, anchor: anchor ? anchor.toLowerCase() : null } : null;
}

/**
 * Where each anchor sits in the file, and the `.ttl` that belongs to it.
 *
 * The title is taken from the span *before the next anchor*, not from a fixed
 * window. A fixed window is how you attach one frame's title to the frame after
 * it when the markup between them happens to be short — silently, and only on
 * some boards.
 */
function framesIn(html) {
  const hits = [...html.matchAll(ANCHOR)];
  return hits.map((m, i) => {
    const from = m.index;
    const to = i + 1 < hits.length ? hits[i + 1].index : html.length;
    const region = html.slice(from, to);
    const ttl = /<span[^>]*class="[^"]*\bttl\b[^"]*"[^>]*>([^<]*)</i.exec(region)?.[1];
    return { anchor: m[1].toLowerCase(), ttl: ttl ? decode(ttl) : null };
  });
}

async function describe(dir, folder, rel) {
  const abs = path.join(dir, rel);
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) return null;
  const html = await readFile(abs, 'utf8').catch(() => '');
  const frames = framesIn(html);
  const links = (html.match(/<a\s[^>]*href=/gi) ?? []).length;
  const { name, revision } = nameOf(rel);
  return {
    id: `${folder}/${rel}`,
    folder,
    file: rel,
    url: urlFor(folder, rel),
    name,
    revision,
    title: titleOf(html),
    kind: kindOf(rel, frames.length, links),
    bytes: info.size,
    modified: info.mtime.toISOString(),
    links,
    _frames: frames,
  };
}

/**
 * @param root     the package directory
 * @param screens  the screen list, as journeys builds it — each with
 *                 `wireframe.board` and, since 26 August, `wireframe.generatedFallback`
 */
export async function buildUiux(root, screens = []) {
  const boards = [];
  const folders = [];

  for (const folder of FOLDERS) {
    const dir = path.join(root, ...folder.dir.split('/'));
    const found = await stat(dir).catch(() => null);
    if (!found?.isDirectory()) {
      folders.push({ ...folder, present: false, count: 0 });
      continue;
    }
    const files = (await readdir(dir).catch(() => []))
      .filter((f) => IS_BOARD.test(f))
      .sort((a, b) => a.localeCompare(b));
    let count = 0;
    for (const file of files) {
      const entry = await describe(dir, folder.id, file);
      if (entry) { boards.push(entry); count += 1; }
    }
    folders.push({ ...folder, present: true, count });
  }

  // ---- what each board draws, according to the screens ----------------------
  // Two ways a screen can name a board and they mean different things, so they
  // are kept apart rather than merged into one "used by" list:
  //
  //   board              this screen is drawn here
  //   generatedFallback  it *was* drawn here, and still is by the generator, but
  //                      a client pack draws it now
  //
  // Collapsing them would report a superseded generated board as current, which
  // is the thing `generatedFallback` was added to make visible.
  const byFile = new Map(boards.map((b) => [`${b.folder}/${b.file}`.toLowerCase(), b]));
  const claims = new Map(); // board id -> claims[]
  const push = (ref, screen, via) => {
    const split = splitRef(ref);
    if (!split) return;
    for (const folder of FOLDERS) {
      const board = byFile.get(`${folder.id}/${split.rel}`.toLowerCase());
      if (!board) continue;
      if (!claims.has(board.id)) claims.set(board.id, []);
      claims.get(board.id).push({
        id: screen.id, name: screen.name ?? null,
        platform: screen.platform ?? screen.platformCode ?? null,
        anchor: split.anchor, via,
      });
      return;
    }
  };
  for (const screen of screens ?? []) {
    push(screen?.wireframe?.board, screen, 'board');
    push(screen?.wireframe?.generatedFallback, screen, 'generatedFallback');
  }

  for (const board of boards) {
    const mine = claims.get(board.id) ?? [];
    const byAnchor = new Map();
    for (const claim of mine) {
      if (!claim.anchor) continue;
      if (!byAnchor.has(claim.anchor)) byAnchor.set(claim.anchor, []);
      byAnchor.get(claim.anchor).push(claim);
    }
    board.frames = board._frames.map(({ anchor, ttl }) => {
      const owners = byAnchor.get(anchor) ?? [];
      const named = owners.find((o) => o.name);
      // A generated board titles its own frames, so `.ttl` is the board
      // speaking about itself and wins. A pack does not, and there the screen
      // is the only thing that knows.
      if (ttl) return { anchor, name: ttl, source: 'board', screens: owners.map((o) => o.id) };
      if (named) return { anchor, name: named.name, source: 'screen', screens: owners.map((o) => o.id) };
      return { anchor, name: null, source: 'unnamed', screens: owners.map((o) => o.id) };
    });
    delete board._frames;
    board.frameCount = board.frames.length;
    board.screens = mine;
    board.platforms = [...new Set(mine.map((c) => c.platform).filter(Boolean))].sort();
    board.wired = mine.length > 0;
    // Frames on the board that no screen claims. On a wired pack this is the
    // remainder of the mapping job, and it is the number that says how much of
    // one is left.
    board.unclaimedFrames = board.frames.filter((f) => f.screens.length === 0).length;
    board.namedFrames = board.frames.filter((f) => f.name).length;
  }

  const total = boards.length;
  const wired = boards.filter((b) => b.wired).length;
  const frames = boards.reduce((n, b) => n + b.frameCount, 0);
  return {
    present: total > 0,
    folders,
    boards,
    stats: {
      boards: total,
      wired,
      unwired: total - wired,
      frames,
      framesNamed: boards.reduce((n, b) => n + b.namedFrames, 0),
      framesClaimed: frames - boards.reduce((n, b) => n + b.unclaimedFrames, 0),
      // Screens a *client pack* draws, which is what anybody means by "how much
      // is drawn". Counting every `via: 'board'` claim returns all 492, because
      // the generator draws every screen on every platform and each of them
      // points at its own generated frame — a figure that is true and says
      // nothing.
      screensDrawn: new Set(
        boards.filter((b) => b.kind === 'pack')
          .flatMap((b) => b.screens.filter((s) => s.via === 'board').map((s) => s.id))
      ).size,
      screensGenerated: new Set(
        boards.filter((b) => b.kind === 'generated')
          .flatMap((b) => b.screens.filter((s) => s.via === 'board').map((s) => s.id))
      ).size,
    },
  };
}
