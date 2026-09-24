// Settings, one section at a time.
//
// The page was rebuilt from a side nav beside a long scroll into a tab strip,
// and the risk in that is not the look: it is that every control on it is wired
// by id from settings.js, and a section that quietly stops being rendered takes
// its controls with it without anything throwing. So this walks every tab and
// asserts the section is the only one showing, that it has content in it, and
// that each control the page binds is still present.
//
// It also guards a collision that had already happened once: `.set-link` is an
// existing navigation row in this codebase, and the flow connectors were briefly
// given the same class -- which handed them its border, its padding and its
// chevron, and then a careless rename took the class off the real rows.
//
//   node server.mjs                     # the viewer
//   node checks/settings-check.mjs
import puppeteer from 'puppeteer-core';
const V = process.env.VIEWER ?? 'http://localhost:4173';
const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox'] });
const p = await b.newPage();
await p.setViewport({ width: 1400, height: 950 });
const bad = [];
p.on('console', (m) => { if (m.type() === 'error') bad.push(m.text().slice(0, 130)); });
p.on('pageerror', (e) => bad.push(String(e).slice(0, 170)));
await p.evaluateOnNewDocument((api) => { try { localStorage.setItem('ticvai-api', api); } catch {} }, V);
await p.goto(`${V}/login.html`, { waitUntil: 'domcontentloaded' });
await p.evaluate(async () => (await fetch('/api/auth/login', { method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'harness.boss@softlabsgroup.com', password: 'a-long-enough-passphrase' }) })).ok);
await p.goto(`${V}/settings.html`, { waitUntil: 'domcontentloaded' });
await p.goto(`${V}/settings.html`, { waitUntil: 'domcontentloaded' });
await p.waitForSelector('#set-tabs button', { timeout: 20000 });
await new Promise((r) => setTimeout(r, 2500));

let fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); if (!ok) fail++; };

for (const tab of ['account','password','openproject','git','connector','agents','sessions']) {
  await p.click(`#set-tabs button[data-tab="${tab}"]`);
  await new Promise((r) => setTimeout(r, 450));
  const r = await p.evaluate((t) => {
    const vis = [...document.querySelectorAll('.set-section')].filter(s => !s.hidden).map(s => s.id);
    const sec = document.getElementById(t);
    return { vis, height: Math.round(sec.getBoundingClientRect().height), hash: location.hash };
  }, tab);
  check(`${tab}: exactly that section, with content`,
    r.vis.length === 1 && r.vis[0] === tab && r.height > 80 && r.hash === `#${tab}`,
    `${r.vis.join(',')} h=${r.height} ${r.hash}`);
}

// The controls settings.js wires must still be there.
const controls = await p.evaluate(() => ({
  pw: !!document.getElementById('pw-new'), op: !!document.getElementById('op-token'),
  git: !!document.getElementById('git-email'), mcp: !!document.getElementById('mcp-line'),
  fleet: !!document.getElementById('fleet-list'), out: !!document.getElementById('sess-all-go'),
  oldLinks: document.querySelectorAll('.set-link').length,
}));
check('every control settings.js binds is present', Object.entries(controls).filter(([k]) => k !== 'oldLinks').every(([, v]) => v), JSON.stringify(controls));
check('the original .set-link rows survived the rename', controls.oldLinks > 0, `${controls.oldLinks} rows`);

// A deep link still opens its tab.
await p.goto(`${V}/settings.html#sessions`, { waitUntil: 'domcontentloaded' });
await new Promise((r) => setTimeout(r, 2000));
const deep = await p.evaluate(() => [...document.querySelectorAll('.set-section')].filter(s => !s.hidden).map(s => s.id));
check('a #sessions link opens that tab', deep.length === 1 && deep[0] === 'sessions', deep.join(','));

check('nothing shouted on the way', bad.length === 0, bad.slice(0, 2).join(' | '));
await b.close();
console.log(fail ? `\n${fail} failed` : '\nall good');
process.exit(fail ? 1 : 0);
