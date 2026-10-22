#!/usr/bin/env node
// What adam_pull writes so a developer's agent can build exactly what was approved (21 October 2026):
//
//   - a screen ticket's wireframe frame, as one self-contained file (#31848, WEB-007: the agent was told the
//     board "opens in the ADAM viewer", built the page from the record's text, and it looked nothing like the
//     design the client verified);
//   - a ticket's runnable files whole, byte for byte, checked against ADAM's checksum (#36194: the read tool's
//     400-line window gave the agent 341 lines of a 2,736-line migration it had to run).
//
//   node viewer/mcp/pull-files-check.mjs           1-3 (no services), then 4 (its own viewer, no sign-in)
//   node viewer/mcp/pull-files-check.mjs --keep    and leave the pulled folders, for a look
//   node viewer/mcp/pull-files-check.mjs --live    also 5: the real stack - a stand-in OpenProject, the accounts
//                                                  service and a signed-in viewer - pulling #31848 and #36194 as
//                                                  the developer, and a client account reading a frame
//
//   1. a frame lifted out of a board, made self-contained: no <base>, no script, image or stylesheet by address,
//      the board's image inline as the same bytes; support.js left out of a frame with no design component and
//      inlined into one with; a link to another board kept as data-adam-href; what cannot be inlined, said;
//   2. README.md for a screen ticket (a stand-in client over this repository's ticvai/): the wireframe's status, the
//      file, the prototype and its views, "build the page to match ... exactly", every state, "structure only, not
//      the look" for wireframes/incoming/, a frame that cannot be written, and a generated frame;
//   3. files a ticket runs: which are runnable, written whole with ADAM's checksum, a mismatch writes nothing, an
//      ADAM without the checksum is said as "not checked", an older client without bytes still pulls;
//   4. its own viewer on 8894 serving the latest release tag, no sign-in (TICVAI_NO_GATE=1; the accounts service's
//      answers are a stand-in): the 415 that now names adam_file with a frame, the checksum header, a pull of
//      #31848 and #36194 through the real ViewerClient, the files byte for byte the served export's, and, with
//      Chrome, the pulled frame opened offline drawing the same pixels as the viewer's /frame;
//   5. (--live) the same pulls through the sign-in, and a client account: the frame it can see in the viewer, and
//      still not a decision file.
//
// Ports 8894-8897; never 4173, 8787 or 8798. Nothing leaves 127.0.0.1: the browser in 4 is offline for the
// pulled file and blocks everything but 127.0.0.1 for the viewer's frame.

import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const VIEWER_DIR = path.resolve(HERE, '..');
const PACKAGE = path.resolve(VIEWER_DIR, '..', 'ticvai');
const LIVE = process.argv.includes('--live');
// --keep leaves the temporary folder (the pulled .adam/ folders) for a look, and says where.
const KEEP = process.argv.includes('--keep');
const PORTS = { viewer: 8894, pms: 8895, api: 8896, gated: 8897 };
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const tools = await import(pathToFileURL(path.join(HERE, 'tools.mjs')).href);
const { BY_NAME, selfContainedFrame, externalRefs, boardRef, runnableFiles, writeWhole } = tools;
const { ViewerClient } = await import(pathToFileURL(path.join(HERE, 'client.mjs')).href);
const { frameDocument } = await import(pathToFileURL(path.join(VIEWER_DIR, 'lib', 'wireframes.mjs')).href);
const require = createRequire(path.join(VIEWER_DIR, 'package.json'));
const yaml = require('js-yaml');

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${String(detail).slice(0, 900)}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};
const skip = (name, why) => console.log(`skip  ${name} - ${why}`);
const section = (name) => console.log(`\n${name}`);
const T = mkdtempSync(path.join(tmpdir(), 'adam-pull-files-'));
const sha = (b) => createHash('sha256').update(b).digest('hex');
const children = [];

const board = (name) => readFileSync(path.join(PACKAGE, 'wireframes', name), 'utf8');
const fromDisk = (root) => async (rel) => {
  const full = path.join(root, ...rel.split('/'));
  return existsSync(full) ? { ok: true, status: 200, type: '', bytes: readFileSync(full) } : { ok: false, status: 404, bytes: Buffer.from('not found') };
};
const read = (dir, key, ...f) => { const p = path.join(dir, '.adam', 'work', key, ...f); return existsSync(p) ? readFileSync(p, 'utf8') : null; };

/** The screen records as the package writes them, by id. */
const SCREENS = new Map();
for (const f of readdirSync(path.join(PACKAGE, 'screens')).filter((n) => /^P\d.*\.ya?ml$/.test(n))) {
  const doc = yaml.load(readFileSync(path.join(PACKAGE, 'screens', f), 'utf8'));
  for (const s of (Array.isArray(doc) ? doc : doc?.screens ?? [])) if (s?.id) SCREENS.set(s.id, s);
}

/**
 * A client over this repository's ticvai/ with the connector's `raw`: /frame from frameDocument, wireframes/ and
 * files from disk. `checksum` decides the file answer's header: 'right', 'wrong' or 'none' (an older ADAM).
 */
function standIn(tickets, { checksum = 'right', screens = {}, bytes = true } = {}) {
  const client = {
    async projectId() { return 'ticvai'; },
    async layer(route) {
      return route === 'journeys' ? { screens: [...SCREENS.values(), ...Object.values(screens)], flows: [] } : {};
    },
    async file(p) {
      const full = path.join(PACKAGE, p);
      return existsSync(full) ? { ok: true, status: 200, text: readFileSync(full, 'utf8') } : { ok: false, status: 404, text: '' };
    },
    async service(route) {
      const m = /^\/api\/work-packages\/(\d+)(\/pin)?/.exec(route);
      if (m?.[2]) return { ok: true, status: 200, data: { pin: { tag: 'r8' }, current: { tag: 'r8' }, recorded: true } };
      if (m && tickets[m[1]]) return { ok: true, status: 200, data: tickets[m[1]] };
      return { ok: false, status: 404, data: { detail: 'not in the stand-in' } };
    },
  };
  if (bytes) {
    client.raw = async (route, params) => {
      if (route === 'frame') {
        const doc = frameDocument(board(params.board), params.anchor);
        return doc ? { ok: true, status: 200, type: 'text/html', bytes: Buffer.from(doc) }
          : { ok: false, status: 404, bytes: Buffer.from(`${params.board} has no frame #${params.anchor}`) };
      }
      if (route === 'file') {
        const got = await fromDisk(PACKAGE)(params.path);
        if (!got.ok) return { ...got, sha256: null };
        return { ...got, sha256: checksum === 'none' ? null : checksum === 'wrong' ? sha(Buffer.from('another file')) : sha(got.bytes) };
      }
      return fromDisk(PACKAGE)(route.split('/').map(decodeURIComponent).join('/'));
    };
  }
  return client;
}

/** The live tickets as adam-links.json records them: subject, links. */
const LINKS = JSON.parse(readFileSync(path.join(PACKAGE, 'handoff', 'service-docs', 'adam-links.json'), 'utf8')).links;
function liveTicket(key, description = '') {
  const mine = LINKS.filter((l) => String(l.key) === key);
  return {
    workPackage: { key, subject: mine[0]?.subject ?? `#${key}`, status: 'New', type: mine[0]?.type ?? 'Task', description, comments: [] },
    touches: mine.map((l) => ({ kind: l.kind, id: l.id })),
  };
}
const DB_TEXT = '- Key: `R8-DB-LOCAL-SANKET-KELUSKAR`\n\nThe files, in this order: apply any of them your database\'s '
  + 'platform.schema_version does not list yet, in name order, and skip none.';

try {
  // ── 1. a frame, self-contained ─────────────────────────────────────
  section('1. a frame lifted out of a board, made self-contained');
  {
    const doc = frameDocument(board('P01 Guest Web.dc.html'), 'web-007');
    check('the viewer\'s /frame document leans on the viewer: a <base>, support.js and the image by path',
      /<base href="wireframes\/">/.test(doc) && /<script src="support\.js">/.test(doc) && /src="frames\/img\/web-007\.png"/.test(doc),
      externalRefs(doc).join(' | '));
    const made = await selfContainedFrame(doc, fromDisk(PACKAGE));
    check('**made self-contained, it names nothing outside itself** (no <base>, no src or href by address, no url())',
      externalRefs(made.html).length === 0 && !/<base\b/i.test(made.html) && !/\bsrc="(?!data:)/i.test(made.html)
        && !/<script\b[^>]*\bsrc=/i.test(made.html) && !/<link\b/i.test(made.html), externalRefs(made.html).join(' | '));
    const png = readFileSync(path.join(PACKAGE, 'wireframes', 'frames', 'img', 'web-007.png'));
    const inline = /src="data:image\/png;base64,([^"]+)"/.exec(made.html)?.[1];
    check('**the board\'s image is inline as the same bytes** (frames/img/web-007.png)',
      inline && Buffer.from(inline, 'base64').equals(png) && made.inlined.join() === 'wireframes/frames/img/web-007.png', made.inlined.join());
    check('support.js is left out of a frame with no design component, and says why',
      !/dc-runtime/.test(made.html) && /support\.js \(the board runtime\) left out/.test(made.html) && !made.needsNetwork);
    check('the frame\'s own styles and the board\'s stylesheet are kept', /\.scr\{/.test(made.html) && /class="scr"/.test(made.html));

    const p08 = await selfContainedFrame(frameDocument(board('P08 Venue Management.dc.html'), 'adm-069'), fromDisk(PACKAGE));
    check('a link to another board is kept as data-adam-href, not a link out of the file',
      externalRefs(p08.html).length === 0 && /data-adam-href="/.test(p08.html), externalRefs(p08.html).slice(0, 3).join(' | '));

    // Every way a document can reach for something, on one made-up frame.
    const synthetic = '<!doctype html><html><head><base href="wireframes/"><script src="support.js"></script>'
      + '<link rel="stylesheet" href="frames/x.css"><link rel="stylesheet" href="https://fonts.example/a.css">'
      + '<style>@import url("frames/y.css"); .a{background:url(frames/img/web-007.png)}</style></head><body>'
      + '<x-dc></x-dc><div style="background-image:url(\'frames/img/web-007.png\')"></div>'
      + '<img srcset="frames/img/web-007.png 1x, frames/img/web-007.png 2x"><img src="https://cdn.example/a.png">'
      + '<img src="../outside.png"><img src="frames/img/none.png"><svg><image href="frames/img/web-007.png"/></svg>'
      + '<a href="#web-001">here</a><a href="P02%20Guest%20App.dc.html#gst-001">there</a></body></html>';
    const files = { 'wireframes/support.js': 'console.log("dc-runtime"); var s = "</script>";', 'wireframes/frames/x.css': '.x{background:url(img/web-007.png)}' };
    const all = await selfContainedFrame(synthetic, async (rel) => (files[rel] ? { ok: true, bytes: Buffer.from(files[rel]) }
      : fromDisk(PACKAGE)(rel)));
    check('**every kind of reference goes: script, stylesheet (and its own url()), url() in a style block and attribute, '
      + 'srcset, an SVG image**', externalRefs(all.html).length === 0, externalRefs(all.html).join(' | '));
    check('a frame with a design component gets support.js inline (its "</script>" escaped), and says React comes from '
      + 'the internet', /dc-runtime/.test(all.html) && /<\\\/script/.test(all.html) && all.needsNetwork);
    check('a stylesheet beside the board is inlined with its own images', /\.x\{background:url\("data:image\/png;base64,/.test(all.html));
    const why = Object.fromEntries(all.left.map((l) => [l.ref, l.why]));
    check('what cannot be inlined is said, not left in: an address outside ADAM, a path out of wireframes/, a missing '
      + 'image, an @import', /outside ADAM/.test(why['https://cdn.example/a.png']) && /outside wireframes/.test(why['../outside.png'])
        && /404/.test(why['frames/img/none.png']) && Object.keys(why).some((k) => k.startsWith('@import'))
        && /outside ADAM/.test(why['https://fonts.example/a.css']), JSON.stringify(all.left));
    check('a fragment link stays; a link to another board becomes data-adam-href',
      /<a href="#web-001">/.test(all.html) && /<a data-adam-href="P02%20Guest%20App\.dc\.html#gst-001">/.test(all.html));
    check('boardRef reads a record\'s wireframe.board, and nothing else',
      JSON.stringify(boardRef('wireframes/P01 Guest Web.dc.html#web-007')) === '{"board":"P01 Guest Web.dc.html","anchor":"web-007"}'
        && JSON.stringify(boardRef('P08 Venue Management.dc.html#BO-100')) === '{"board":"P08 Venue Management.dc.html","anchor":"bo-100"}'
        && boardRef('wireframes/P01 Guest Web.dc.html') === null && boardRef('contracts/x.yaml') === null);
  }

  // ── 2. README.md for a screen ticket ───────────────────────────────
  section('2. README.md for a screen ticket');
  const dir2 = path.join(T, 'two');
  {
    mkdirSync(dir2, { recursive: true });
    const tickets = {
      31848: liveTicket('31848'),
      9101: { workPackage: { key: '9101', subject: '[FE] GST-001 Home', status: 'New', description: '' }, touches: [{ kind: 'screen', id: 'GST-001' }] },
      9102: { workPackage: { key: '9102', subject: '[FE] XX-001 A screen whose frame is gone', status: 'New', description: '' },
        touches: [{ kind: 'screen', id: 'XX-001' }] },
      9103: { workPackage: { key: '9103', subject: '[FE] BO-100', status: 'New', description: '' }, touches: [{ kind: 'screen', id: 'BO-100' }] },
      9100: { workPackage: { key: '9100', subject: '[BE] Build getPlan', status: 'New', description: 'Builds getPlan.' },
        touches: [{ kind: 'table', id: 'subscription.plan' }] },
    };
    const screens = { 'XX-001': { id: 'XX-001', name: 'Gone', wireframe: { status: 'review', provenance: 'client-verified',
      board: 'wireframes/P01 Guest Web.dc.html#web-999' } } };
    const client = standIn(tickets, { screens });
    const pull = BY_NAME.get('adam_pull');
    const one = await pull.run(client, { key: '31848', dir: dir2 });
    const readme = read(dir2, '31848', 'README.md');
    const look = readme?.split('## How WEB-007 Interactive Seat Selection must look')[1]?.split('## Before you report a gap')[0] ?? '';
    check('the pull writes wireframe-web-007.html beside the screen record', Boolean(read(dir2, '31848', 'wireframe-web-007.html'))
      && Boolean(read(dir2, '31848', 'screen-WEB-007.json')), readdirSync(path.join(dir2, '.adam', 'work', '31848')).join(', '));
    check('**and it is self-contained**', externalRefs(read(dir2, '31848', 'wireframe-web-007.html')).length === 0);
    check('README.md has "How WEB-007 Interactive Seat Selection must look"', look.length > 0, readme?.slice(0, 400));
    check('**it says the wireframe\'s status: client-verified, review, and that the design is fixed**',
      look.includes('**Wireframe status:** client-verified, review - the client verified this design; it is fixed.'), look.slice(0, 300));
    check('it links the file and names the frame and board',
      look.includes('[wireframe-web-007.html](wireframe-web-007.html), frame `#web-007` of `wireframes/P01 Guest Web.dc.html`'));
    check('it says the frame is the client\'s prototype, captured, at which view',
      look.includes('This frame is the client\'s prototype, captured as an image: Client prototype rev 3 (28 Sep 2026) · Book → Union Arena'));
    check('**it names the approved prototype file, its rev, verification and the views, and why it is not written**',
      look.includes('`sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`')
        && look.includes('verified 2026-09-29') && look.includes("**Views:** Union Arena → 'Flow 1 · Fixed date → zone → seat map'")
        && look.includes('Grand Playhouse → Flow 1 / Flow 2') && /no view can be cut out of it/.test(look)
        && /ask the person to open that file at the views named/.test(look));
    check('**"Build the page to match the wireframe and the prototype view exactly", with every state the board lists**',
      look.includes('**Build the page to match the wireframe and the prototype view exactly**: layout, components, copy, imagery, '
        + 'and every state (loading · error · emptyFirstRun · emptyNoAccess · offline · emptyNoResults)'), look.slice(look.indexOf('**Build'), look.indexOf('**Build') + 300));
    check('**the record gives the behaviour and bindings; the wireframe the look; the prototype wins where it has a view**',
      look.includes('gives the behaviour and the bindings; the wireframe gives the look')
        && look.includes('where the prototype has a view, the prototype wins for the look'));
    check('**every state in the frame\'s visual language, never a plain heading, sentence and button**',
      look.includes('build every state in the same visual language as the frame') && look.includes('never a plain heading, a plain sentence and a plain button'));
    check('the answer points at the file and the look', one.wireframes?.[0]?.drawn === true
      && /wireframe-web-007\.html and build the page to look exactly like it/.test(one.next), one.next);

    await pull.run(client, { key: '9101', dir: dir2 });
    const gst = read(dir2, '9101', 'README.md');
    check('**a record naming wireframes/incoming/ gets "structure only, not the look" for it**, and the board frame as the design',
      gst.includes('`wireframes/incoming/P02-mobile-v4/gst-001.html` (named in the record): **structure only, not the look**')
        && gst.includes('[wireframe-gst-001.html](wireframe-gst-001.html)'), gst.split('must look')[1]?.slice(0, 600));
    await pull.run(client, { key: '9102', dir: dir2 });
    const gone = read(dir2, '9102', 'README.md');
    check('a frame that cannot be written is said, with the adam_file call that asks again, and no file is left',
      /`wireframes\/P01 Guest Web\.dc\.html#web-999` could not be written \(ADAM answered 404/.test(gone)
        && gone.includes('adam_file, path `wireframes/P01 Guest Web.dc.html#web-999`') && !read(dir2, '9102', 'wireframe-web-999.html'),
      gone.split('must look')[1]?.slice(0, 400));
    await pull.run(client, { key: '9103', dir: dir2 });
    const gen = read(dir2, '9103', 'README.md');
    check('a generated frame is said to give the structure, not the look',
      /the screen record rendered as boxes by the package's generator, not a drawing: it gives the structure/.test(gen)
        && /This screen's frame is generated, not drawn/.test(gen), gen.split('must look')[1]?.slice(0, 500));
    // A ticket with no screen and nothing to run: README.md is what it was before this change.
    await pull.run(client, { key: '9100', dir: dir2 });
    const be = read(dir2, '9100', 'README.md');
    check('a ticket with no screen and nothing to run has neither section', !/must look|Files to run/.test(be));
  }

  // ── 3. files a ticket runs ─────────────────────────────────────────
  section('3. files a ticket runs, whole');
  {
    const touches = [
      { kind: 'file', id: 'backend/tenant/V0107__names_after_r1_20261019.sql' },
      { kind: 'file', id: 'backend/control/V0108__after_r1_20261020.sql' },
      { kind: 'file', id: 'backend/tenant/010-access.sql' },
      { kind: 'file', id: 'repos/ticvai-docs/setup/backend-patterns.md' },
      { kind: 'table', id: 'access.pass' },
    ];
    check('**the linked forward migrations are runnable; the 010 DDL and a standard are not**',
      JSON.stringify(runnableFiles(touches, '')) === JSON.stringify(['backend/tenant/V0107__names_after_r1_20261019.sql', 'backend/control/V0108__after_r1_20261020.sql']),
      JSON.stringify(runnableFiles(touches, '')));
    check('a file the ticket\'s text says to run or apply is runnable too; one it only mentions is not',
      JSON.stringify(runnableFiles([], 'Read docs/x.sql first. Then run `tools/seed.sql` and apply backend/tenant/V0110__after_r1_20261020.sql.'))
        === JSON.stringify(['tools/seed.sql', 'backend/tenant/V0110__after_r1_20261020.sql']));

    const dir3 = path.join(T, 'three');
    mkdirSync(dir3, { recursive: true });
    const folder = path.join(dir3, 'f');
    const right = await writeWhole(standIn({}), 'backend/tenant/V0107__names_after_r1_20261019.sql', folder);
    const pkgBytes = readFileSync(path.join(PACKAGE, 'backend', 'tenant', 'V0107__names_after_r1_20261019.sql'));
    const written = readFileSync(path.join(folder, 'run', 'backend', 'tenant', 'V0107__names_after_r1_20261019.sql'));
    check('**written whole: the same bytes, the same checksum, every line** (tenant V0107)',
      written.equals(pkgBytes) && right.sha256 === sha(pkgBytes) && right.checked === 'match' && right.lines > 2000,
      JSON.stringify({ ...right, sha256: right.sha256?.slice(0, 12) }));
    const wrong = await writeWhole(standIn({}, { checksum: 'wrong' }), 'backend/control/V0108__after_r1_20261020.sql', folder);
    check('**bytes that do not match ADAM\'s checksum are not written**',
      /do not match ADAM's checksum/.test(wrong.error ?? '') && !existsSync(path.join(folder, 'run', 'backend', 'control', 'V0108__after_r1_20261020.sql')), JSON.stringify(wrong));
    const none = await writeWhole(standIn({}, { checksum: 'none' }), 'backend/control/V0108__after_r1_20261020.sql', folder);
    check('an ADAM that sends no checksum: written, and said as not checked', none.checked === 'unchecked' && !none.error);
    const older = await writeWhole(standIn({}, { bytes: false }), 'backend/control/V0108__after_r1_20261020.sql', folder);
    check('an older client with no bytes still writes the file, not checked', older.checked === 'unchecked' && older.bytes > 0);

    const tickets = { 36194: liveTicket('36194', DB_TEXT) };
    const pulled = await BY_NAME.get('adam_pull').run(standIn(tickets), { key: '36194', dir: dir3 });
    const readme = read(dir3, '36194', 'README.md');
    const links = LINKS.filter((l) => String(l.key) === '36194' && /\.sql$/.test(l.id)).map((l) => l.id);
    const same = links.every((rel) => {
      const p = path.join(dir3, '.adam', 'work', '36194', 'run', ...rel.split('/'));
      return existsSync(p) && readFileSync(p).equals(readFileSync(path.join(PACKAGE, ...rel.split('/'))));
    });
    check(`**#36194: all ${links.length} migrations under run/, byte for byte the package's**`, links.length === 13 && same, links.join(', '));
    const sums = read(dir3, '36194', 'run', 'SHA256SUMS') ?? '';
    check('run/SHA256SUMS lists each, in sha256sum\'s own format', links.every((rel) => sums.includes(`${sha(readFileSync(path.join(PACKAGE, ...rel.split('/'))))}  ${rel}\n`)));
    check('**README.md: "Files to run, whole (13 of 13)", run these, never a window**',
      readme.includes('## Files to run, whole (13 of 13)') && readme.includes('**Run these files, as they are, in the order the ticket gives.**')
        && readme.includes('never run, copy or rebuild a file from its window') && (readme.match(/matches ADAM's copy/g) ?? []).length === 13,
      readme.split('## Files to run')[1]?.slice(0, 600));
    check('What this touches lists the whole files, not windows; the standard stays a summary',
      readme.includes('- file `backend/tenant/V0107__names_after_r1_20261019.sql` - [run/backend/tenant/V0107__names_after_r1_20261019.sql]')
        && !existsSync(path.join(dir3, '.adam', 'work', '36194', 'file-backend_tenant_V0107__names_after_r1_20261019.sql.json'))
        && Boolean(read(dir3, '36194', 'file-repos_ticvai-docs_setup_backend-patterns.md.json')));
    check('the answer says it runs 13 files, written whole', pulled.run?.length === 13 && /It runs 13 files, written whole/.test(pulled.next), pulled.next);
    const window = await BY_NAME.get('adam_file').run(standIn({}), { path: 'backend/tenant/V0107__names_after_r1_20261019.sql' });
    check('adam_file keeps its window for reading, and says a window is never run',
      /^1-\d+$/.test(window.showing) && window.totalLines > Number(window.showing.split('-')[1])
        && /never run or copy a file from it/.test(window.more), JSON.stringify({ showing: window.showing, more: window.more }));
  }

  // ── 4. its own viewer, no sign-in ──────────────────────────────────
  section('4. its own viewer on 8894 (the latest release tag, no sign-in)');
  {
    const viewer = spawn(process.execPath, ['server.mjs', '--port', String(PORTS.viewer), '--host', '127.0.0.1'],
      { cwd: VIEWER_DIR, env: { ...process.env, TICVAI_NO_GATE: '1' }, windowsHide: true });
    let log = '';
    viewer.stdout.on('data', (x) => { log += x; });
    viewer.stderr.on('data', (x) => { log += x; });
    children.push(viewer);
    const base = `http://127.0.0.1:${PORTS.viewer}`;
    await waitFor(`${base}/pkg/ticvai/summary`);
    const release = await (await fetch(`${base}/pkg/ticvai/release`)).json();
    const served = release.mode === 'tag' ? path.join(VIEWER_DIR, '.releases', 'ticvai', release.tag) : PACKAGE;
    check('the viewer serves a release', Boolean(release.tag) && existsSync(served), JSON.stringify(release).slice(0, 200));

    const asked = await fetch(`${base}/pkg/ticvai/file?path=${encodeURIComponent('wireframes/P01 Guest Web.dc.html')}`);
    const said = await asked.text();
    check('**a board through /api/file is a 415 that names adam_file with a frame, not "open the ADAM viewer"**',
      asked.status === 415 && said.includes('adam_file with path "wireframes/<board>.dc.html#<anchor>"') && !/open in the ADAM viewer/.test(said), said);
    const frameAsked = await fetch(`${base}/pkg/ticvai/file?path=${encodeURIComponent('wireframes/P01 Guest Web.dc.html#web-007')}`);
    const frameSaid = await frameAsked.text();
    check('a board#anchor from an older connector is a 415 naming the same call and /update-adam',
      frameAsked.status === 415 && /is a frame of a wireframe board, not a file/.test(frameSaid) && /\/update-adam/.test(frameSaid), frameSaid);
    const proto = await fetch(`${base}/pkg/ticvai/file?path=${encodeURIComponent('sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html')}`);
    const protoSaid = await proto.text();
    check('a client prototype is a 415 that says ADAM serves none and names the frame call instead',
      proto.status === 415 && /A client prototype is not served by ADAM/.test(protoSaid) && protoSaid.includes('adam_file with path'), protoSaid);
    const other = await fetch(`${base}/pkg/ticvai/file?path=README.md`);
    check('any other file is answered as before, now with its checksum', other.status === 200
      && (await other.text()).length > 0 && /^[0-9a-f]{64}$/.test(other.headers.get('x-ticvai-sha256') ?? ''));

    const rel = 'backend/tenant/V0107__names_after_r1_20261019.sql';
    const got = await fetch(`${base}/pkg/ticvai/file?path=${encodeURIComponent(rel)}`);
    const body = Buffer.from(await got.arrayBuffer());
    const disk = readFileSync(path.join(served, ...rel.split('/')));
    check('**/api/file sends the served file\'s bytes and their sha256 (X-Ticvai-Sha256)**',
      body.equals(disk) && got.headers.get('x-ticvai-sha256') === sha(disk), `${got.headers.get('x-ticvai-sha256')} vs ${sha(disk)}`);

    const client = new ViewerClient({ base, project: 'ticvai', email: 'nobody', password: 'nothing' });
    client.login = async () => 'no sign-in on this viewer';
    const tickets = { 31848: liveTicket('31848'), 36194: liveTicket('36194', DB_TEXT) };
    client.service = async (route) => standIn(tickets).service(route);
    const dir4 = path.join(T, 'four');
    mkdirSync(dir4, { recursive: true });
    const pull = BY_NAME.get('adam_pull');
    const fe = await pull.run(client, { key: '31848', dir: dir4 });
    const frameFile = path.join(dir4, '.adam', 'work', '31848', 'wireframe-web-007.html');
    const html = existsSync(frameFile) ? readFileSync(frameFile, 'utf8') : '';
    check('**#31848 through the real client: wireframe-web-007.html, with no external reference**',
      html.length > 100000 && externalRefs(html).length === 0 && fe.wireframes?.[0]?.drawn, `${html.length} bytes; ${externalRefs(html).join(' | ')}`);
    const viaFile = await BY_NAME.get('adam_file').run(client, { path: 'wireframes/P01 Guest Web.dc.html#web-007', key: '31848', dir: dir4 });
    check('adam_file with the record\'s wireframe.board saves the same frame', viaFile.found && viaFile.selfContained
      && viaFile.saved === frameFile && /loading · error · emptyFirstRun/.test(viaFile.states), JSON.stringify(viaFile).slice(0, 400));

    const db = await pull.run(client, { key: '36194', dir: dir4 });
    const all = (db.run ?? []).every((r) => r.checked === 'match'
      && readFileSync(r.file).equals(readFileSync(path.join(served, ...r.path.split('/')))));
    check('**#36194 through the real client: 13 migrations, each byte for byte the served export\'s, each checked against '
      + 'ADAM\'s checksum**', db.run?.length === 13 && all, JSON.stringify(db.run?.map((r) => [r.path, r.checked, r.error])));
    const v0107 = db.run?.find((r) => r.path === rel);
    check('tenant V0107 whole: 2,735 lines, not a 400-line window', v0107 && readFileSync(v0107.file).toString('utf8').split('\n').length >= 2735,
      JSON.stringify(v0107));

    // The pulled frame, opened offline, against the viewer's /frame (everything but 127.0.0.1 blocked).
    if (!existsSync(CHROME)) {
      skip('the pulled frame draws what the viewer draws', `no Chrome at ${CHROME}`);
    } else {
      const puppeteer = require('puppeteer-core');
      const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
      try {
        const shot = async (url, offline) => {
          const page = await browser.newPage();
          await page.setViewport({ width: 1400, height: 1000 });
          const asked2 = [];
          await page.setRequestInterception(true);
          page.on('request', (r) => {
            asked2.push(r.url());
            if (/^(data:|file:|http:\/\/127\.0\.0\.1:)/.test(r.url())) r.continue(); else r.abort();
          });
          if (offline) await page.setOfflineMode(true);
          await page.goto(url, { waitUntil: 'networkidle0' });
          const images = await page.evaluate(() => [...document.images].map((i) => i.naturalWidth));
          const png = await page.screenshot({ fullPage: true, encoding: 'base64' });
          await page.close();
          return { asked: asked2, images, png };
        };
        const theirs = await shot(`${base}/pkg/ticvai/frame?board=${encodeURIComponent('P01 Guest Web.dc.html')}&anchor=web-007`, false);
        const ours = await shot(pathToFileURL(frameFile).href, true);
        check('**opened offline, the pulled frame asks for nothing but itself and its image draws**',
          ours.asked.every((u) => u.startsWith('file:') || u.startsWith('data:')) && ours.images.length === 1 && ours.images[0] > 0,
          JSON.stringify({ asked: ours.asked.map((u) => u.slice(0, 60)), images: ours.images }));
        const page = await browser.newPage();
        await page.setOfflineMode(true);
        const diff = await page.evaluate(async (a, b) => {
          const load = (src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = src; });
          const [x, y] = await Promise.all([load(a), load(b)]);
          if (x.width !== y.width || x.height !== y.height) return { size: [x.width, x.height, y.width, y.height] };
          const px = (i) => { const c = document.createElement('canvas'); c.width = i.width; c.height = i.height; const g = c.getContext('2d'); g.drawImage(i, 0, 0); return g.getImageData(0, 0, i.width, i.height).data; };
          const p = px(x); const q = px(y); let n = 0;
          for (let k = 0; k < p.length; k += 4) if (p[k] !== q[k] || p[k + 1] !== q[k + 1] || p[k + 2] !== q[k + 2]) n += 1;
          return { width: x.width, height: x.height, differing: n };
        }, `data:image/png;base64,${theirs.png}`, `data:image/png;base64,${ours.png}`);
        check('**and draws the same pixels as the viewer\'s /frame**', diff.differing === 0, JSON.stringify(diff));
      } finally {
        await browser.close();
      }
    }
    await stop(viewer);
    if (fail) console.log(log.slice(-1500));
  }

  // ── 5. --live: the sign-in, the accounts service, a client account ─
  if (!LIVE) {
    skip('5. the real stack', 'run with --live');
  } else {
    section('5. the real stack: stand-in OpenProject on 8895, accounts on 8896, a signed-in viewer on 8897');
    const key = spawnSync('python', ['-c', 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'],
      { encoding: 'utf8' }).stdout.trim();
    const PMS = `http://127.0.0.1:${PORTS.pms}`;
    const API = `http://127.0.0.1:${PORTS.api}`;
    const VIEWER = `http://127.0.0.1:${PORTS.gated}`;
    const env = { ...process.env, TICVAI_DB: path.join(T, 'store.db'), TICVAI_SECRET_KEY: key, TICVAI_AUTH: API };
    delete env.TICVAI_NO_GATE;
    const start = (cmd, args, extra = {}) => {
      const child = spawn(cmd, args, { cwd: VIEWER_DIR, env: { ...env, ...extra }, windowsHide: true });
      child.out = '';
      child.stdout.on('data', (x) => { child.out += x; });
      child.stderr.on('data', (x) => { child.out += x; });
      children.push(child);
      return child;
    };
    start('node', ['api/fake-openproject.mjs'], { PORT: String(PORTS.pms) });
    const api = start('python', ['-m', 'uvicorn', 'api.main:app', '--port', String(PORTS.api)]);
    const gated = start(process.execPath, ['server.mjs', '--port', String(PORTS.gated), '--host', '127.0.0.1']);
    await waitFor(`${PMS}/_created`);
    await waitFor(`${API}/api/health`);
    await waitFor(`${VIEWER}/login.html`);
    const jars = new Map();
    const as = async (who, method, route, body) => {
      const res = await fetch(`${API}${route}`, { method, headers: { 'content-type': 'application/json', ...(jars.get(who) ? { cookie: jars.get(who) } : {}) },
        body: body === undefined ? undefined : JSON.stringify(body) });
      const set = res.headers.get('set-cookie');
      if (set) jars.set(who, set.split(';')[0]);
      let data = null;
      try { data = await res.json(); } catch { /* empty */ }
      return { status: res.status, data };
    };
    const PASSWORD = 'a-long-enough-passphrase';
    const ADMIN = 'harness.pull@softlabsgroup.com';
    check('an admin exists', (await as('admin', 'POST', '/api/auth/bootstrap', { email: ADMIN, name: 'Harness Pull', password: PASSWORD })).status === 200);
    check('connected to the stand-in OpenProject', (await as('admin', 'PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS })).status === 200);
    check('TICVAI reads the harness project', (await as('admin', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);
    // The links go in as they do on the server, through load_links.py: POST /api/links takes no `file` kind,
    // and #36194's thirteen migrations are file links.
    const mine = LINKS.filter((l) => ['31848', '36194'].includes(String(l.key)));
    const linksFile = path.join(T, 'links.json');
    writeFileSync(linksFile, JSON.stringify({ project: 'ticvai', links: mine }));
    const loaded = spawnSync('python', ['api/load_links.py', linksFile, '--email', ADMIN, '--db', env.TICVAI_DB, '--apply'],
      { cwd: VIEWER_DIR, encoding: 'utf8', env });
    check(`the ${mine.length} links of #31848 and #36194 load as on the server (load_links.py)`, loaded.status === 0, loaded.stdout + loaded.stderr);
    for (const [k, text] of [['31848', ''], ['36194', DB_TEXT]]) {
      const t = liveTicket(k, text);
      const made = await (await fetch(`${PMS}/_make?${new URLSearchParams({ id: k, subject: t.workPackage.subject, description: text })}`)).json();
      check(`#${k} is in the stand-in OpenProject under its live number`, made.id === Number(k), JSON.stringify(made));
    }
    const admin = new ViewerClient({ base: VIEWER, project: 'ticvai', email: ADMIN, password: PASSWORD });
    const dir5 = path.join(T, 'five');
    mkdirSync(dir5, { recursive: true });
    const fe = await BY_NAME.get('adam_pull').run(admin, { key: '31848', dir: dir5 });
    const html = read(dir5, '31848', 'wireframe-web-007.html') ?? '';
    check('**signed in: #31848 writes wireframe-web-007.html, self-contained, and README.md says how it must look**',
      fe.found && html.length > 100000 && externalRefs(html).length === 0 && /## How WEB-007 Interactive Seat Selection must look/.test(read(dir5, '31848', 'README.md') ?? ''),
      JSON.stringify(fe).slice(0, 500));
    const db = await BY_NAME.get('adam_pull').run(admin, { key: '36194', dir: dir5 });
    const release = await (await fetch(`${VIEWER}/pkg/ticvai/release`, { headers: { cookie: `ticvai_session=${encodeURIComponent(await admin.login())}` } })).json();
    const served = path.join(VIEWER_DIR, '.releases', 'ticvai', release.tag ?? 'none');
    check('**signed in: #36194 writes its 13 migrations whole, byte for byte the served release\'s, checked**',
      db.found && db.release?.current === release.tag && db.run?.length === 13 && db.run.every((r) => r.checked === 'match'
        && readFileSync(r.file).equals(readFileSync(path.join(served, ...r.path.split('/'))))),
      JSON.stringify({ release: db.release, run: db.run?.map((r) => [r.path, r.checked, r.error]) }));

    // A client account: what it reads in the viewer, and no more.
    const invite = await as('admin', 'POST', '/api/invites', { email: 'someone@client-company.example', role: 'client' });
    const token = (invite.data?.link ?? '').split('#')[1];
    const redeemed = await as('client', 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: 'Harness Client' });
    check('a client account signs up', invite.status === 200 && redeemed.status === 200, `${invite.status} ${redeemed.status}`);
    const client = new ViewerClient({ base: VIEWER, project: 'ticvai', email: 'someone@client-company.example', password: PASSWORD });
    const seen = await BY_NAME.get('adam_file').run(client, { path: 'wireframes/P01 Guest Web.dc.html#web-007', dir: dir5 });
    check('**a client saves the frame it can open in the viewer**', seen.found && seen.selfContained, JSON.stringify(seen).slice(0, 300));
    const adr = readdirSync(path.join(PACKAGE, 'docs', 'adr')).find((f) => f.endsWith('.md'));
    const refused = await BY_NAME.get('adam_file').run(client, { path: `docs/adr/${adr}` }).then(() => null, (e) => e);
    check('**and is still refused a decision file**', refused?.name === 'Forbidden', String(refused));
    if (fail) console.log(api.out.slice(-1500), gated.out.slice(-1500));
  }
} catch (error) {
  check('the check ran to the end', false, error.stack);
} finally {
  for (const child of children) await stop(child);
  if (KEEP) console.log(`
kept: ${T}`);
  else rmSync(T, { recursive: true, force: true });
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

async function waitFor(url) {
  for (let i = 0; i < 600; i += 1) {
    try { if ((await fetch(url)).status < 500) return; } catch { /* not yet */ }
    await new Promise((r) => { setTimeout(r, 250); });
  }
  throw new Error(`nothing answered at ${url}`);
}

async function stop(child) {
  if (!child || child.exitCode !== null || child.signalCode !== null) return;
  const gone = new Promise((resolve) => { child.once('exit', resolve); });
  // The whole tree on Windows: `python` can be a launcher with the interpreter under it.
  if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true });
  else child.kill();
  await Promise.race([gone, new Promise((resolve) => { setTimeout(resolve, 5000); })]);
}
