// wireframes/ — the drawn artefacts, and the two different ways they attach.
//
// There are two kinds of file here and they are not interchangeable:
//
//   wireframes/screens/acc-001.html          a standalone wireframe for one screen
//   wireframes/P07 Staff Scanner.dc.html     a platform BOARD holding every screen
//                                            on that platform, each behind an anchor
//
// The standalone files are named for exactly the thing they draw, so matching them
// is a file-name lookup. The boards are not — one file holds 73 screens, and the
// join is the anchor:
//
//   P07 Staff Scanner.dc.html#scn-004   ->  screen SCN-004
//
// That link is *declared*, not guessed: every screen carries `wireframe.board`
// and every platform carries `platform.wireframeBoard`. So this stays inside the
// same rule as the rest of the package — boards.mjs infers, and says so; nothing
// here does.
//
// The check that matters is the one wireframes/LINKAGE.md names: a link to
// `#scn-004` in a board with no such anchor is a click that silently does
// nothing, which is worse than no link at all. Both directions are checked.

import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const DIR = 'wireframes';
const SCREEN_SUBDIR = 'screens';

/**
 * The `<title>` is the wireframe's own name for itself — "ACC-001 Landing /
 * Programme Overview".
 *
 * It is HTML, so `WEB-002 Event &amp; Attraction Listing` is the correct way to
 * write that title in the file and the wrong thing to put in a heading. The
 * viewer sets it with textContent, which escapes rather than decodes, so an
 * ampersand would reach the screen as `&amp;`.
 */
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', '#39': "'" };
function titleOf(text) {
  const match = /<title>([^<]*)<\/title>/i.exec(text.slice(0, 2000));
  if (!match) return null;
  return match[1]
    .replace(/&(#x?[0-9a-f]+|[a-z]+);/gi, (whole, name) => {
      const key = name.toLowerCase();
      if (ENTITIES[key]) return ENTITIES[key];
      if (key.startsWith('#x')) return String.fromCodePoint(parseInt(key.slice(2), 16));
      if (key.startsWith('#')) return String.fromCodePoint(Number(key.slice(1)));
      return whole;
    })
    .trim();
}

const urlFor = (rel) => `/${DIR}/${rel.split('/').map(encodeURIComponent).join('/')}`;

async function describe(dir, rel, { anchors = false } = {}) {
  const abs = path.join(dir, rel);
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) return null;
  // the standalone wireframes only need their first 2KB; a board has to be read
  // whole because the anchors are spread through all 233KB of it
  const text = await readFile(abs, 'utf8').catch(() => '');
  const entry = {
    file: `${DIR}/${rel}`,
    url: urlFor(rel),
    title: titleOf(text),
    bytes: info.size,
    modified: info.mtime.toISOString(),
  };
  if (anchors) {
    // Two conventions, both live. The platform boards number their frames after
    // the screen — `scn-004`, `pos-004`, `kit-001` — and the client's topic
    // boards letter theirs within a board: `fnb-3a` … `fnb-3k`. The pattern only
    // knew the first, so a board using the second was recorded as having no
    // anchors and every screen pointing into it was reported as broken.
    //
    // Still a pattern and not "every id on the page": a board is full of layout
    // divs with ids of their own, and a set containing everything can never
    // report a missing anchor, which is what this set is for.
    entry.anchors = new Set(
      [...text.matchAll(/\bid="([A-Za-z]{2,5}-\d[\dA-Za-z]{0,3})"/g)].map((m) => m[1].toLowerCase())
    );
  }
  return entry;
}

/**
 * One screen's frame, lifted out of the board it lives on.
 *
 * A board is 233KB holding every screen on a platform. Framing the whole thing
 * and scrolling it to an anchor shows the right screen with 28 others around it
 * and the page's own navigation on top. What is wanted on a screen's page is
 * that screen.
 *
 * Returns null rather than guessing if the anchor is not there.
 *
 * This returns the element and nothing else, which is only half a screen for
 * most boards — see `frameDocument` below, which is what the server serves.
 */
export function extractFrame(html, anchor) {
  const open = new RegExp(`<(\\w+)[^>]*\\bid="${anchor}"[^>]*>`, 'i').exec(html);
  if (!open) return null;
  const tag = open[1].toLowerCase();
  const start = open.index;

  // walk forward counting opens and closes of this tag only — the frames nest
  // divs many levels deep, so the first </div> is nowhere near the end
  const scan = new RegExp(`<${tag}\\b[^>]*>|</${tag}>`, 'gi');
  scan.lastIndex = start;
  let depth = 0;
  let match;
  while ((match = scan.exec(html))) {
    depth += match[0][1] === '/' ? -1 : 1;
    if (depth === 0) return html.slice(start, match.index + match[0].length);
  }
  return null; // unbalanced — better to show nothing than half a screen
}

/**
 * A board's own stylesheet, and the classes its frames are nested under.
 *
 * The first generation of boards inline-styled every element, so lifting one
 * `<div id="web-002">` out of the file gave you something that rendered exactly
 * as it did in place. That is no longer true and was never guaranteed: the
 * boards that arrived with the second dump are a tenth of the size precisely
 * because they moved the styling into one `<style>` block and gave the frames
 * classes — `<div id="web-002" class="scr">`. Lifting that element alone
 * produces an unstyled column of text, which is what a screen's page showed.
 *
 * So the document carries three things out of the board rather than one:
 *
 *   the <style> blocks   or the classes on the element mean nothing
 *   the ancestor classes  `.scr` gets its width from the `.grid` it sits in,
 *                         and a board with a `.dark` container styles its
 *                         frames through it. Reproducing the chain keeps every
 *                         such rule working without naming any of them here.
 *   the element itself
 *
 * Inline-styled boards land here too and are unharmed: they have no <style> to
 * copy and their ancestors carry no classes, so the wrapper collapses to what
 * it always was.
 */
const FRAME_TAGS = /<div\b[^>]*>|<\/div>/gi;

function ancestorClasses(html, upTo) {
  const open = [];
  FRAME_TAGS.lastIndex = 0;
  let match;
  while ((match = FRAME_TAGS.exec(html)) && match.index < upTo) {
    if (match[0][1] === '/') open.pop();
    else open.push(/\bclass="([^"]*)"/i.exec(match[0])?.[1] ?? '');
  }
  // Only the ones that carry a class. A bare <div> contributes no rule and
  // reproducing it just adds nesting — and on the first-generation boards,
  // where every ancestor is classless, dropping them restores exactly the
  // wrapper those boards were served with before.
  return open.filter(Boolean);
}

/** Every `<style>` block in the board, concatenated in document order. */
export function extractStyles(html) {
  return [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)]
    .map((m) => m[1])
    .join('\n');
}

/**
 * One screen's frame as a complete, standalone document.
 *
 * Returns null if the anchor is not in the board, so the caller can 404 rather
 * than serve an empty page.
 */
export function frameDocument(html, anchor) {
  const frame = extractFrame(html, anchor);
  if (!frame) return null;

  // Located by string search rather than a built regex: the anchor is
  // interpolated, and a pattern assembled around interpolated text is one
  // escaping mistake away from silently matching nothing — which here would
  // mean an empty ancestor chain and a frame that looks *nearly* right. It
  // did exactly that once already.
  const marker = html.toLowerCase().indexOf(`id="${anchor}"`);
  const at = marker < 0 ? -1 : html.lastIndexOf('<', marker);
  const chain = at >= 0 ? ancestorClasses(html, at) : [];
  const open = chain.map((cls) => `<div class="${cls}">`).join('');
  const close = '</div>'.repeat(chain.length);
  const css = extractStyles(html);

  return '<!doctype html><html><head><meta charset="utf-8">'
    + '<script src="/wireframes/support.js"></script>'
    // The board's own rules first, so what follows can correct them rather than
    // be overridden by them.
    + (css ? `<style>${css}</style>` : '')
    + '<style>'
    // A board with no stylesheet of its own is drawn on white and must not
    // inherit the viewer's theme, or half its strokes disappear. One with a
    // stylesheet has already said what it wants.
    + (css ? 'html,body{margin:0}' : 'html,body{margin:0;background:#fff;}')
    + 'body{padding:18px 20px;font-family:system-ui,sans-serif;}'
    // The grid a frame comes out of is sized for a whole platform — auto-fill
    // at 342px, which for one card means one card and two empty columns. There
    // is exactly one thing in this document, so it gets the width.
    + '.grid{grid-template-columns:minmax(0,1fr)!important;}'
    // Likewise the wrap's page padding: this document has its own.
    + '.wrap{max-width:none!important;padding:0!important;}'
    + '</style></head><body>'
    + open + frame + close
    + '</body></html>';
}

/** `wireframes/P07 Staff Scanner.dc.html#scn-004` -> { rel, anchor } */
function splitBoardRef(ref) {
  if (typeof ref !== 'string' || !ref.trim()) return null;
  const [target, anchor = null] = ref.trim().split('#');
  const rel = target.replace(/^\.?\/*/, '').replace(new RegExp(`^${DIR}/`, 'i'), '');
  return rel ? { rel, anchor: anchor ? anchor.toLowerCase() : null } : null;
}

/**
 * @param root
 * @param subjects  { screens, flows, platforms } — the ids to match against, so
 *                  a wireframe for something that no longer exists is reported
 *                  rather than silently served
 */
export async function buildWireframes(root, subjects = {}) {
  const problems = [];
  const dir = path.join(root, DIR);
  const found = await stat(dir).catch(() => null);
  if (!found?.isDirectory()) {
    return {
      present: false, dir: DIR, screens: {}, flows: {}, platforms: {}, boards: {},
      problems, stats: { total: 0 },
    };
  }

  const top = (await readdir(dir).catch(() => [])).filter((f) => /\.html?$/i.test(f));
  const inScreens = (await readdir(path.join(dir, SCREEN_SUBDIR)).catch(() => []))
    .filter((f) => /\.html?$/i.test(f));

  const stem = (f) => f.replace(/\.html?$/i, '').toLowerCase();
  const screenList = subjects.screens ?? [];

  // ---- boards --------------------------------------------------------------
  // Read every file a screen or platform actually points at, once, keeping its
  // anchors. A board nobody references is left to the unmatched check below.
  const referenced = new Map(); // lowercase rel -> real rel
  const noteRef = (ref) => {
    const split = splitBoardRef(ref);
    if (split) referenced.set(split.rel.toLowerCase(), split.rel);
  };
  for (const screen of screenList) noteRef(screen.wireframe?.board);
  for (const platform of subjects.platforms ?? []) noteRef(platform.wireframeBoard);

  const onDisk = new Map(top.map((f) => [f.toLowerCase(), f]));
  const boards = {};
  for (const [lower, rel] of referenced) {
    const real = onDisk.get(lower);
    if (!real) continue; // reported per-screen below, with the screen that asked for it
    boards[real] = await describe(dir, real, { anchors: true });
  }

  // the same boards keyed by platform, so the apps page can frame P08's actual
  // board rather than the thin p08.html render beside it
  const platformBoards = {};
  for (const platform of subjects.platforms ?? []) {
    const split = splitBoardRef(platform.wireframeBoard);
    const real = split && onDisk.get(split.rel.toLowerCase());
    if (real && boards[real]) platformBoards[platform.code] = boards[real];
  }

  // ---- screens -------------------------------------------------------------
  const screenIds = new Set(screenList.map((s) => s.id));
  const byStem = new Map([...screenIds].map((id) => [id.toLowerCase(), id]));
  const screens = {};
  const claimedAnchors = new Map(); // board file -> Set(anchor)

  for (const file of inScreens) {
    const id = byStem.get(stem(file));
    if (!id) {
      problems.push({
        severity: 'warning',
        kind: 'wireframe-orphan',
        file: `${DIR}/${SCREEN_SUBDIR}/${file}`,
        message:
          `${file} draws a screen no platform file defines. Either the screen was renamed and ` +
          `this is the old one, or it was removed and the wireframe was not.`,
      });
      continue;
    }
    const entry = await describe(dir, `${SCREEN_SUBDIR}/${file}`);
    if (entry) screens[id] = entry;
  }

  // the board link, declared by the screen itself
  for (const screen of screenList) {
    const split = splitBoardRef(screen.wireframe?.board);
    const slot = (screens[screen.id] ??= { standalone: false });
    if (!split) {
      if (!screens[screen.id].file) {
        problems.push({
          severity: 'info',
          kind: 'wireframe-missing',
          file: screen.file ?? `${DIR}/`,
          message:
            `Screen ${screen.id} names no wireframe and no board anchor, so there is nothing ` +
            `drawn for it. Every other screen has at least a board frame.`,
        });
      }
      continue;
    }
    const boardFile = onDisk.get(split.rel.toLowerCase());
    const board = boards[boardFile];
    if (!board) {
      problems.push({
        severity: 'error',
        kind: 'wireframe-board-missing',
        file: screen.file ?? `${DIR}/`,
        message:
          `Screen ${screen.id} points at board ${split.rel}, which is not in wireframes/. ` +
          `The link resolves to nothing.`,
      });
      continue;
    }
    if (split.anchor && board.anchors && !board.anchors.has(split.anchor)) {
      problems.push({
        severity: 'error',
        kind: 'wireframe-anchor-missing',
        file: screen.file ?? board.file,
        message:
          `Screen ${screen.id} links to #${split.anchor} in ${split.rel}, and that board has no ` +
          `such anchor — a click that silently does nothing, which is worse than no link.`,
      });
      continue;
    }
    if (split.anchor) {
      if (!claimedAnchors.has(board.file)) claimedAnchors.set(board.file, new Set());
      claimedAnchors.get(board.file).add(split.anchor);
    }
    slot.board = {
      file: board.file,
      url: split.anchor ? `${board.url}#${split.anchor}` : board.url,
      boardUrl: board.url,
      anchor: split.anchor,
      title: board.title,
      platform: screen.platform ?? null,
      // this screen's frame on its own, lifted out of the board — what a
      // screen's page should show, rather than the board scrolled to it
      frameUrl: split.anchor
        ? `/frame?board=${encodeURIComponent(boardFile)}&anchor=${encodeURIComponent(split.anchor)}`
        : null,
    };
  }

  // the other direction — a frame somebody drew that nobody specified
  for (const [file, board] of Object.entries(boards)) {
    const claimed = claimedAnchors.get(board.file) ?? new Set();
    const orphans = [...(board.anchors ?? [])].filter((a) => !claimed.has(a));
    if (!orphans.length) continue;
    problems.push({
      severity: 'warning',
      kind: 'board-anchor-orphan',
      file: board.file,
      message:
        `${file} draws ${orphans.length} frame${orphans.length > 1 ? 's' : ''} no screen claims ` +
        `(${orphans.slice(0, 4).join(', ')}${orphans.length > 4 ? '…' : ''}) — drawn but never specified.`,
    });
  }

  // ---- flows and platforms -------------------------------------------------
  const flows = {};
  const platforms = {};
  let index = null;

  const flowIds = new Map((subjects.flows ?? []).map((f) => [String(f.id).toLowerCase(), f.id]));
  const platformIds = new Map(
    (subjects.platforms ?? []).map((p) => [String(p.code ?? p).toLowerCase(), p.code ?? p])
  );

  for (const file of top) {
    if (boards[file]) continue; // already attached, as a board
    const key = stem(file);
    if (key === 'index' || /wireframe boards/i.test(key)) {
      // the contents page — "Open TICVAI Wireframe Boards.dc.html first"
      index ??= await describe(dir, file);
      continue;
    }
    const flowId = flowIds.get(key.replace(/^flow-/, ''));
    if (flowId) {
      flows[flowId] = await describe(dir, file);
      continue;
    }
    const platformId = platformIds.get(key);
    if (platformId) {
      platforms[platformId] = await describe(dir, file);
      continue;
    }
    problems.push({
      severity: 'info',
      kind: 'wireframe-unmatched',
      file: `${DIR}/${file}`,
      message: `${file} does not name a screen, flow or platform, so it is served but not attached to anything.`,
    });
  }

  // a flow with no drawing is a gap worth naming, now that most have one
  for (const flow of subjects.flows ?? []) {
    if (flows[flow.id]) continue;
    problems.push({
      severity: 'info',
      kind: 'flow-wireframe-missing',
      file: `${DIR}/`,
      message:
        `Flow ${flow.id} has no flow wireframe. ${Object.keys(flows).length} of ` +
        `${(subjects.flows ?? []).length} flows have one, so this is a gap rather than a policy.`,
    });
  }

  // the anchor sets were only needed for the cross-check
  const boardsOut = {};
  for (const [file, board] of Object.entries(boards)) {
    boardsOut[file] = {
      ...board,
      frames: board.anchors?.size ?? 0,
      claimed: (claimedAnchors.get(board.file) ?? new Set()).size,
      anchors: undefined,
    };
  }
  const platformBoardsOut = {};
  for (const [code, board] of Object.entries(platformBoards)) {
    platformBoardsOut[code] = boardsOut[board.file.split('/').pop()] ?? null;
  }

  const drawn = Object.values(screens).filter((s) => s.file || s.board).length;
  return {
    present: true,
    dir: DIR,
    index,
    screens,
    boards: boardsOut,
    platformBoards: platformBoardsOut,
    flows,
    platforms,
    problems,
    stats: {
      total: drawn + Object.keys(flows).length + Object.keys(platforms).length,
      screens: drawn,
      screensStandalone: Object.values(screens).filter((s) => s.file).length,
      screensOnBoard: Object.values(screens).filter((s) => s.board).length,
      screensTotal: screenIds.size,
      boards: Object.keys(boardsOut).length,
      frames: Object.values(boardsOut).reduce((n, b) => n + b.frames, 0),
      flows: Object.keys(flows).length,
      flowsTotal: (subjects.flows ?? []).length,
      platforms: Object.keys(platforms).length,
    },
  };
}
