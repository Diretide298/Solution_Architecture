/**
 * Before/after screenshots compared pixel by pixel, in a headless Chrome (no
 * image library needed). For each file name in both folders: the share of
 * pixels that differ by more than a small tolerance, and the box they fall in.
 *
 *   node checks/shot-diff.mjs <before dir> <after dir>
 */
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const [a, b] = process.argv.slice(2);
const names = readdirSync(a).filter((n) => n.endsWith('.png') && existsSync(path.join(b, n)));
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const page = await browser.newPage();
await page.setContent('<canvas id=c></canvas>');
for (const n of names) {
  const one = `data:image/png;base64,${readFileSync(path.join(a, n)).toString('base64')}`;
  const two = `data:image/png;base64,${readFileSync(path.join(b, n)).toString('base64')}`;
  const r = await page.evaluate(async ([one, two]) => {
    const load = (src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = src; });
    const [x, y] = await Promise.all([load(one), load(two)]);
    if (x.width !== y.width || x.height !== y.height) return { size: `${x.width}x${x.height} vs ${y.width}x${y.height}` };
    const c = document.createElement('canvas'); c.width = x.width; c.height = x.height;
    const g = c.getContext('2d');
    g.drawImage(x, 0, 0); const p = g.getImageData(0, 0, c.width, c.height).data;
    g.drawImage(y, 0, 0); const q = g.getImageData(0, 0, c.width, c.height).data;
    let diff = 0, x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
    for (let i = 0; i < p.length; i += 4) {
      if (Math.abs(p[i] - q[i]) + Math.abs(p[i + 1] - q[i + 1]) + Math.abs(p[i + 2] - q[i + 2]) > 24) {
        diff++;
        const px = (i / 4) % c.width, py = Math.floor(i / 4 / c.width);
        x0 = Math.min(x0, px); y0 = Math.min(y0, py); x1 = Math.max(x1, px); y1 = Math.max(y1, py);
      }
    }
    return { share: diff / (c.width * c.height), box: diff ? `${x0},${y0}-${x1},${y1}` : '' };
  }, [one, two]);
  console.log(`${r.size ? 'SIZE ' : r.share > 0.001 ? 'DIFF ' : 'same '}${n}${r.size ? ` ${r.size}` : ` ${(r.share * 100).toFixed(2)}%${r.box ? ` in ${r.box}` : ''}`}`);
}
await browser.close();
