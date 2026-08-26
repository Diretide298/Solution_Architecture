import puppeteer from 'puppeteer-core';
const V='http://localhost:4173';
const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:'new',args:['--no-sandbox']});
const p=await b.newPage(); const errs=[];
p.on('pageerror',e=>errs.push('pageerror: '+e.message));
await p.setViewport({width:1600,height:1100});
// The lens reads /api/domains from the viewer's own server, which needs no
// account — but the main page is behind a sign-in, so one is still needed to
// reach the tree. Point at whichever auth service is up.
const API = process.env.TICVAI_API ?? 'http://localhost:8787';
await p.goto(`${V}/invite.html`,{waitUntil:'domcontentloaded'});
await p.evaluate(a=>localStorage.setItem('ticvai-api',a),API);
const ok = await p.evaluate(async (a,e,pw)=>(await fetch(`${a}/api/auth/login`,{method:'POST',credentials:'include',headers:{'content-type':'application/json'},body:JSON.stringify({email:e,password:pw})})).ok,
  API, process.env.TICVAI_USER ?? 'chinmay.parab@softlabsgroup.com', process.env.TICVAI_PASS ?? 'the-first-administrator');
if (!ok) console.log('note: not signed in — the tree may not render');
await p.goto(V,{waitUntil:'domcontentloaded'});
await p.waitForSelector('#layers button',{timeout:30000});
await new Promise(r=>setTimeout(r,4500));
const wait=ms=>new Promise(r=>setTimeout(r,ms));
for (const [layer,mode] of [['frontend','screen'],['contracts','graph'],['backend','data'],['domain','states'],['decisions','decisions']]) {
  await p.evaluate(l=>document.querySelector(`#layers button[data-layer="${l}"]`).click(),layer);
  await wait(2600);
  const r=await p.evaluate(()=>({
    chip: document.querySelector('#lens-filters .lens-chip')?.textContent ?? null,
    hidden: document.getElementById('lens-filters')?.hidden,
    marks: document.querySelectorAll('.tree-file .lens-mark').length,
    rows: document.querySelectorAll('.tree-file').length,
  }));
  console.log(`${layer.padEnd(10)} chip=${String(r.chip).padEnd(6)} hidden=${String(r.hidden).padEnd(5)} marked=${String(r.marks).padEnd(4)} of ${r.rows} rows`);
  if (r.chip) {
    await p.evaluate(()=>document.querySelector('#lens-filters .lens-chip').click());
    await wait(1600);
    const f=await p.evaluate(()=>({rows:document.querySelectorAll('.tree-file').length,marked:document.querySelectorAll('.tree-file .lens-mark').length}));
    console.log(`${''.padEnd(10)}   filtered -> ${f.rows} rows, ${f.marked} marked`);
    await p.evaluate(()=>document.querySelector('#lens-filters .lens-chip').click());
    await wait(1200);
  }
}
console.log('\nerrors:',errs.length?errs.slice(0,5):'none');
await b.close();
