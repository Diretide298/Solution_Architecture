// Renders manual.html to PDF. Run capture.mjs first if the app has changed.
//
//   node manual/build.mjs   →  manual/TICVAI-Viewer-Manual.pdf

import puppeteer from 'puppeteer-core';
import { readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const SOURCE = path.join(here, 'manual.html');
const OUTPUT = path.join(here, 'TICVAI-Viewer-Manual.pdf');

const CANDIDATES = [
  process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean);
const EXE = CANDIDATES.find((p) => existsSync(p));
if (!EXE) {
  console.error('No Chrome found. Set CHROME=/path/to/chrome and re-run.');
  process.exit(1);
}

const browser = await puppeteer.launch({ executablePath: EXE, headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();

const missing = [];
page.on('requestfailed', (r) => missing.push(r.url()));
page.on('pageerror', (e) => missing.push(`pageerror: ${e.message}`));

await page.goto(pathToFileURL(SOURCE).href, { waitUntil: 'networkidle0' });

// a figure whose <img> never loaded would print as an empty box — refuse that
const broken = await page.$$eval('img', (imgs) =>
  imgs.filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.getAttribute('src'))
);
if (broken.length) {
  console.error(`\n${broken.length} figure(s) did not load:`);
  for (const src of broken) console.error(`  ${src}`);
  console.error('\nRun `node manual/capture.mjs` first.');
  await browser.close();
  process.exit(1);
}

const figures = await page.$$eval('figure img', (i) => i.length);

const grey = 'color:#8b8b9c; font-family:"Segoe UI",sans-serif; font-size:7pt; width:100%;';
await page.pdf({
  path: OUTPUT,
  format: 'A4',
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: `<div style="${grey} padding:0 14mm;">
      <span style="float:left">TICVAI Architecture Viewer</span>
      <span style="float:right">Team manual</span>
    </div>`,
  footerTemplate: `<div style="${grey} padding:0 14mm;">
      <span style="float:left">Figures captured from the running application</span>
      <span style="float:right">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </span>
    </div>`,
  margin: { top: '18mm', bottom: '16mm', left: '14mm', right: '14mm' },
});

await browser.close();

const { size } = await stat(OUTPUT);
const shots = (await readdir(path.join(here, 'shots'))).filter((f) => f.endsWith('.png'));
console.log(`\n${path.relative(process.cwd(), OUTPUT)}`);
console.log(`  ${figures} figures from ${shots.length} captures · ${(size / 1024 / 1024).toFixed(1)} MB`);
if (missing.length) {
  console.log(`\n  ${missing.length} resource problem(s):`);
  for (const m of missing.slice(0, 5)) console.log(`    ${m}`);
}
