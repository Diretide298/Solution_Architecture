// Seat-level zoom view for stadium sections. Shared by the web booking page and the mobile app.
// Rows run parallel to the pitch (row A nearest it), stands are wider than deep, sold seats cluster
// naturally, and the view is framed on the chosen section's seats with its neighbours faded around it.
(function () {
  const ROWS = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
  const mix = s => { let h = 2166136261 >>> 0; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b) >>> 0; h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35) >>> 0; h ^= h >>> 16; return (h >>> 0) / 4294967296; };
  const side = s => { const cx = s.x + s.w / 2, cy = s.y + s.h / 2; if (cy < 30) return 'N'; if (cy > 70) return 'S'; return cx < 50 ? 'W' : 'E'; };
  function layout(s, perRow, rows) {
    const sd = side(s), horiz = sd === 'N' || sd === 'S', len = horiz ? s.w : s.h, dep = horiz ? s.h : s.w;
    const p = len / perRow, nCol = perRow, nRow = Math.max(3, Math.min(rows, Math.floor(dep / p)));
    const near = sd === 'S' || sd === 'E';
    return { sd, horiz, nCol, nRow, gc: p, gr: p, p, d0: near ? 0 : dep - nRow * p };
  }
  function build(o) {
    const hr = o.hr || 1, sections = (o.sections || []).map(s => Object.assign({}, s, { y: s.y * hr, h: s.h * hr, _o: s })), sel = sections.find(s => String(s.id) === String(o.selId));
    if (!sel) return null;
    const perRow = o.perRow || 18, rows = o.rows || 10, aspect = o.aspect || 0.9, picked = o.picked || [];
    const L0 = layout(sel, perRow, rows);
    const inRange = s => { const dx = Math.abs((s.x + s.w / 2) - (sel.x + sel.w / 2)), dy = Math.abs((s.y + s.h / 2) - (sel.y + sel.h / 2)); return dx < Math.max(sel.w, sel.h) * 1.6 && dy < Math.max(sel.w, sel.h) * 1.6; };
    const seats = [], labels = [], rowTags = [];
    let mnx = 1e9, mny = 1e9, mxx = -1e9, mxy = -1e9;
    sections.filter(s => s.kind !== 'blocked' && s.kind !== 'standing' && !s.zoneKind && inRange(s)).forEach(s => {
      const Lx = s === sel ? L0 : layout(s, perRow, rows), isSel = s === sel, sold = (s.sold == null ? 40 : s.sold) / 100;
      const nearFirst = Lx.sd === 'S' || Lx.sd === 'E';
      for (let r = 0; r < Lx.nRow; r++) {
        const rowIdx = nearFirst ? r : Lx.nRow - 1 - r, rowL = ROWS[rowIdx % ROWS.length];
        for (let c = 0; c < Lx.nCol; c++) {
          const a = Lx.gc * (c + 0.5), d = Lx.d0 + Lx.gr * (r + 0.5);
          const x = Lx.horiz ? s.x + a : s.x + d, y = Lx.horiz ? s.y + d : s.y + a;
          const id = s.label + '-' + rowL + (c + 1);
          const band = 0.5 + 0.45 * Math.sin((c / Lx.nCol) * Math.PI * 1.3 + mix(s.label + rowL) * 6) * (rowIdx < 3 ? 1.2 : 0.8);
          const taken = mix(id) < sold * band + (rowIdx < 2 ? 0.15 : 0);
          seats.push({ id, x, y, sec: s, row: rowL, n: c + 1, tier: s.tier, price: s.price, taken, mine: picked.indexOf(id) > -1, isSel });
          if (isSel) { mnx = Math.min(mnx, x); mxx = Math.max(mxx, x); mny = Math.min(mny, y); mxy = Math.max(mxy, y); }
        }
        if (isSel) { const off = Lx.gc * 0.15; rowTags.push({ key: s.label + rowL, t: rowL, x: Lx.horiz ? s.x - Lx.p * 0.7 : s.x + Lx.d0 + Lx.gr * (r + 0.5), y: Lx.horiz ? s.y + Lx.d0 + Lx.gr * (r + 0.5) : s.y - Lx.p * 0.7 }); }
      }
      labels.push({ key: 'l' + s.id, t: s.label, x: s.x + s.w / 2, y: s.y + s.h / 2, isSel });
    });
    const pad = L0.p * 1.6;
    let vx = mnx - pad * 1.3, vy = mny - pad, vw = (mxx - mnx) + pad * 2.3, vh = (mxy - mny) + pad * 2;
    if (vh < vw * aspect) { const e = vw * aspect - vh; vy -= e / 2; vh += e; } else { const e = vh / aspect - vw; vx -= e / 2; vw += e; }
    const sd = L0.sd, cue = { N: ['PITCH \u2193', sel.x + sel.w / 2, vy + vh - pad * 0.35], S: ['PITCH \u2191', sel.x + sel.w / 2, vy + pad * 0.45], W: ['PITCH \u2192', vx + vw - pad * 0.8, sel.y + sel.h / 2], E: ['\u2190 PITCH', vx + pad * 0.8, sel.y + sel.h / 2] }[sd];
    return { vb: [vx, vy, vw, vh].map(n => n.toFixed(2)).join(' '), r: L0.p * 0.38, sw: L0.p * 0.08, fs: L0.p * 0.55, seats, labels, rowTags, floor: [], cue: { t: cue[0], x: cue[1], y: cue[2], fs: L0.p * 0.6 },
      count: seats.filter(x => x.isSel).length, free: seats.filter(x => x.isSel && !x.taken).length };
  }
  function view(o) {
    const b = build(o); if (!b) return null; const TC = o.tierColors || {};
    const [vx, vy, vw, vh] = b.vb.split(' ').map(Number), px = x => ((x - vx) / vw * 100).toFixed(2) + '%', py = y => ((y - vy) / vh * 100).toFixed(2) + '%';
    const inF = t => t.x >= vx && t.x <= vx + vw && t.y >= vy && t.y <= vy + vh;
    return { vb: b.vb, count: b.count, free: b.free, floor: [],
      labels: b.labels.filter(l => !l.isSel && inF(l)).map(l => ({ key: l.key, t: l.t, x: px(l.x), y: py(l.y), big: true })).concat([{ key: 'cue', t: b.cue.t, x: px(b.cue.x), y: py(b.cue.y), big: false }]),
      rowTags: b.rowTags.filter(inF).map(t => ({ key: t.key, t: t.t, x: px(t.x), y: py(t.y) })),
      seats: b.seats.map(s => { const c = TC[s.tier] || '#6a3fd4'; return { key: s.id, x: s.x.toFixed(2), y: s.y.toFixed(2), r: b.r.toFixed(3), sw: (s.mine ? b.sw * 1.8 : b.sw).toFixed(3),
        fill: s.mine ? c : (s.taken ? '#d9dce2' : '#ffffff'), stroke: s.mine ? '#171425' : (s.taken ? '#d9dce2' : c), op: s.isSel ? '1' : '0.4',
        aria: 'Section ' + s.sec.label + ', row ' + s.row + ', seat ' + s.n + (s.taken ? ', taken' : ', ' + s.tier),
        tap: () => { if (!s.taken && o.onPick) o.onPick(s); } }; }) };
  }
  function dots(o) {
    const hr = o.hr || 1, b = build(Object.assign({}, o, { only: true })); if (!b) return [];
    const TC = o.tierColors || {};
    return b.seats.filter(s => s.isSel).map(s => { const c = TC[s.tier] || '#6a3fd4'; return { key: s.id, x: s.x.toFixed(3) + '%', y: (s.y / hr).toFixed(3) + '%', d: (b.r * 2).toFixed(3) + '%',
      bg: s.mine ? c : (s.taken ? '#cfd3db' : '#ffffff'), bd: s.mine ? '#171425' : (s.taken ? '#cfd3db' : c),
      aria: 'Section ' + s.sec.label + ', row ' + s.row + ', seat ' + s.n + (s.taken ? ', taken' : ', ' + s.tier),
      tap: e => { if (e && e.stopPropagation) e.stopPropagation(); if (!s.taken && o.onPick) o.onPick(Object.assign({}, s, { sec: s.sec._o || s.sec })); } }; });
  }
  function grid(o) {
    const sel = (o.sections || []).find(s => String(s.id) === String(o.selId)); if (!sel) return null;
    const TC = o.tierColors || {}, picked = o.picked || [], c = TC[sel.tier] || '#6a3fd4';
    const sd = side(sel), horiz = sd === 'N' || sd === 'S', hr = o.hr || 1;
    const wpx = sel.w, hpx = sel.h * hr, len = horiz ? wpx : hpx, dep = horiz ? hpx : wpx;
    const per = 6 + Math.floor(mix(String(sel.label)) * 5), p = len / per, nRow = Math.max(3, Math.min(9, Math.floor(dep / p)));
    const near = sd === 'S' || sd === 'E', sold = (sel.sold == null ? 40 : sel.sold) / 100;
    const cells = [];
    for (let r = 0; r < nRow; r++) { const rowIdx = near ? r : nRow - 1 - r, rowL = ROWS[rowIdx % ROWS.length];
      for (let k = 0; k < per; k++) { const id = sel.label + '-' + rowL + (k + 1), band = 0.5 + 0.45 * Math.sin((k / per) * Math.PI * 1.3 + mix(sel.label + rowL) * 6), taken = mix(id) < sold * band + (rowIdx < 2 ? 0.15 : 0), mine = picked.indexOf(id) > -1;
        cells.push({ key: id, r, k, rowL, n: k + 1, bg: mine ? '#171425' : (taken ? 'rgba(255,255,255,.28)' : '#ffffff'), bd: mine ? '#ffffff' : 'transparent', sc: mine ? '1.25' : '1', aria: 'Section ' + sel.label + ', row ' + rowL + ', seat ' + (k + 1) + (taken ? ', taken' : ''), tap: e => { if (e && e.stopPropagation) e.stopPropagation(); if (!taken && o.onPick) o.onPick({ id, sec: sel, row: rowL, n: k + 1, tier: sel.tier, price: sel.price }); } }); } }
    const cw = horiz ? len / per : dep / nRow, ch = horiz ? dep / nRow : len / per, rr = Math.min(cw, ch) * 0.33;
    cells.forEach(cc => { const col = horiz ? cc.k : (near ? cc.r : nRow - 1 - cc.r), row = horiz ? (near ? cc.r : nRow - 1 - cc.r) : cc.k; cc.cx = ((col + 0.5) * cw).toFixed(3); cc.cy = ((row + 0.5) * ch).toFixed(3); cc.rr = (cc.bd === '#ffffff' ? rr * 1.15 : rr).toFixed(3); cc.sw = (rr * 0.28).toFixed(3); });
    const order = cells;
    const blockW = wpx, blockH = hpx, bx = sel.x, byPx = sel.y * hr;
    return { x: bx.toFixed(3) + '%', y: (byPx / hr).toFixed(3) + '%', w: blockW.toFixed(3) + '%', h: (blockH / hr).toFixed(3) + '%', cols: horiz ? per : nRow, rowsN: horiz ? nRow : per, color: c, vb: '0 0 ' + wpx.toFixed(3) + ' ' + hpx.toFixed(3), cells: order };
  }
  window.TVSeatZoom = { build, view, dots, grid };
})();
