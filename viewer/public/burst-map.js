/**
 * The burst environment as a topology: the clusters, and how they expand.
 *
 * **What the slider moves is the replica count, and nothing else.** Every
 * scenario document talks in requests per second — 2.9 a second on an ordinary
 * day, five thousand at the peak — but those numbers live in a comment at the
 * top of `deploy/c-flash-sale.yml`, in prose, and this file will not read a
 * number out of a sentence and then animate it as though it were a measurement.
 * `replicas` is structured data and `min`/`max` are stated per service in
 * `handoff/burst-scope.json`, so the ramp between them is a fact the package
 * holds. The RPS figures appear on the page as the quote they are.
 *
 * **The connection arithmetic is computed here and it is the point of the
 * drawing.** Each service declares `PG_POOL_MAX` in the compose file, so a
 * cluster at n replicas asks for n × PG_POOL_MAX client connections. At full
 * expansion that is 1,560 across the three services. pgbouncer accepts them —
 * `MAX_CLIENT_CONN` is 5,000 — and answers them from `DEFAULT_POOL_SIZE`
 * server connections in transaction mode. Eighty. The funnel is the
 * architecture, and it is the reason the database is not the thing that falls
 * over when the cluster triples.
 *
 * **What expanding does not fix is drawn separately.** Two tables carry
 * `contended: true`, and the operations that touch them carry a lock. Twenty
 * Catalogue replicas are twenty contenders for the same rows of
 * `catalogue.inventory_hold`; the lease path serialises and the slider makes
 * that worse rather than better. A scale-out diagram that only grows is a
 * diagram that argues scaling always works.
 *
 * Both sources are read through `/api/file`, for the reason burst.js gives: a
 * route of its own would have to be added to server.mjs *and* to the location
 * regex in `deploy/nginx/adamapi.ainfinite.ai`.
 */

const COMPOSE = 'deploy/c-flash-sale.yml';

const SVG = 'http://www.w3.org/2000/svg';

const svgEl = (tag, attrs = {}) => {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) if (v != null) node.setAttribute(k, String(v));
  return node;
};

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

/**
 * The docker-compose subset, parsed here because js-yaml is a server
 * dependency and this page is static.
 *
 * **Anchors and aliases are supported because leaving them out was silently
 * wrong.** Only `c-flash-sale.yml` is drawn, and it has none — but
 * `d-venue-local-offline.yml` reuses one environment block across thirty
 * services with `&id001`/`*id001`, and an earlier version of this parser read
 * the anchor as the string `"&id001"` and dropped every service after it
 * without erroring. Checked against js-yaml on all four deploy configs.
 */
export function parseYaml(text) {
  const lines = text.split(/\r?\n/)
    .map((l) => ({ indent: l.match(/^ */)[0].length, body: l.trim() }))
    .filter((l) => l.body && !l.body.startsWith('#'));
  const anchors = new Map();
  let i = 0;

  const scalar = (s) => {
    if (/^".*"$/.test(s) || /^'.*'$/.test(s)) return s.slice(1, -1);
    if (/^-?\d+$/.test(s)) return Number(s);
    if (/^-?\d*\.\d+$/.test(s)) return Number(s);
    if (s === 'true') return true;
    if (s === 'false') return false;
    if (s === 'null' || s === '~') return null;
    return s;
  };

  const value = (rest, indent, anchor) => {
    if (rest.startsWith('*')) return anchors.get(rest.slice(1).trim()) ?? null;
    if (rest) return scalar(rest);
    const next = lines[i];
    const nested = next
      && (next.indent > indent || (next.indent === indent && next.body.startsWith('- ')));
    const out = nested ? block(next.indent) : null;
    if (anchor) anchors.set(anchor, out);
    return out;
  };

  const block = (indent) => {
    if (lines[i] && lines[i].indent === indent && lines[i].body.startsWith('- ')) {
      const arr = [];
      while (lines[i] && lines[i].indent === indent && lines[i].body.startsWith('- ')) {
        const body = lines[i].body.slice(2).trim();
        i += 1;
        arr.push(body.startsWith('*') ? anchors.get(body.slice(1).trim()) ?? null : scalar(body));
      }
      return arr;
    }
    const map = {};
    while (lines[i] && lines[i].indent === indent && !lines[i].body.startsWith('- ')) {
      const at = lines[i].body.indexOf(':');
      if (at < 0) { i += 1; continue; }
      const key = lines[i].body.slice(0, at).trim();
      let rest = lines[i].body.slice(at + 1).trim();
      i += 1;
      let anchor = null;
      const mark = rest.match(/^&(\S+)\s*(.*)$/);
      if (mark) { anchor = mark[1]; rest = mark[2].trim(); }
      map[key] = value(rest, indent, anchor);
      if (anchor && rest) anchors.set(anchor, map[key]);
    }
    return map;
  };

  return lines.length ? block(lines[0].indent) : {};
}

/** The leading comment block, which is where the scenario states its case. */
function leadingNote(text) {
  const out = [];
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith('#')) break;
    out.push(line.replace(/^#\s?/, ''));
  }
  return out.join('\n').trim();
}

/** `-c max_connections=800` out of a postgres command line. */
const pgFlag = (command, name) => {
  const hit = String(command ?? '').match(new RegExp(`-c\\s+${name}=(\\S+)`));
  return hit ? hit[1] : null;
};

const num = (v, fallback = 0) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : fallback;
};

/**
 * Join the two sources. burst-scope owns the ramp (`replicas.min`/`max`, the
 * weighted share, the reason); the compose file owns the machine (pool sizes,
 * cpu and memory limits, what each service depends on).
 */
function topology(burst, compose) {
  const services = compose?.services ?? {};
  const byCompose = new Map(Object.entries(services));
  // orderservice ← OrderService. The compose keys are lowercased service names.
  const composeFor = (name) => byCompose.get(String(name).toLowerCase()) ?? null;

  const deployed = (burst.services ?? [])
    .filter((s) => s.deployed)
    .map((s) => {
      const spec = composeFor(s.name);
      const min = num(s.replicas?.min, 1);
      const max = num(s.replicas?.max, Math.max(min, num(spec?.deploy?.replicas, min)));
      return {
        name: s.name,
        short: s.name.replace(/Service$/, ''),
        tier: s.tier,
        share: num(s.weightedShare),
        reason: s.reason ?? '',
        min,
        max,
        // Per replica. The pool is what a single container opens, so the
        // demand on pgbouncer is this multiplied by however many are up.
        poolMax: num(spec?.environment?.PG_POOL_MAX, 0),
        poolMin: num(spec?.environment?.PG_POOL_MIN, 0),
        cpus: spec?.deploy?.resources?.limits?.cpus ?? null,
        memory: spec?.deploy?.resources?.limits?.memory ?? null,
        depends: spec?.depends_on ?? [],
      };
    })
    .sort((a, b) => b.share - a.share);

  const bouncer = services.pgbouncer ?? null;
  const postgres = services['postgres-hot'] ?? services.postgres ?? null;
  const redis = services.redis ?? null;

  return {
    deployed,
    absent: (burst.services ?? []).filter((s) => !s.deployed),
    bouncer: bouncer && {
      maxClient: num(bouncer.environment?.MAX_CLIENT_CONN),
      poolSize: num(bouncer.environment?.DEFAULT_POOL_SIZE),
      mode: bouncer.environment?.POOL_MODE ?? null,
    },
    postgres: postgres && {
      image: postgres.image,
      maxConnections: num(pgFlag(postgres.command, 'max_connections')),
      sharedBuffers: pgFlag(postgres.command, 'shared_buffers'),
      // The trade the scenario calls deliberate, so it is named rather than
      // left in a command string nobody reads.
      synchronousCommit: pgFlag(postgres.command, 'synchronous_commit'),
      cpus: postgres.deploy?.resources?.limits?.cpus ?? null,
      memory: postgres.deploy?.resources?.limits?.memory ?? null,
    },
    redis: redis && {
      image: redis.image,
      cpus: redis.deploy?.resources?.limits?.cpus ?? null,
      memory: redis.deploy?.resources?.limits?.memory ?? null,
    },
    contended: (burst.tables ?? []).filter((t) => t.contended),
    locks: (burst.operations ?? []).filter((op) => op.lock),
  };
}

// ── geometry ────────────────────────────────────────────────────────────────
// One coordinate space, scaled by the viewBox, so the drawing is the same
// shape at every width and there is no measuring to do on resize.
const W = 1000;
const H = 540;
const CELL = 15;
const CELL_GAP = 5;
const PER_ROW = 5;

function layout(deployedCount, maxes) {
  const heights = maxes.map((m) => {
    const rows = Math.ceil(m / PER_ROW);
    return 46 + rows * (CELL + CELL_GAP);
  });
  const total = heights.reduce((a, b) => a + b, 0) + (deployedCount - 1) * 22;
  let y = (H - total) / 2;
  return heights.map((h) => {
    const box = { x: 196, y, w: 250, h };
    y += h + 22;
    return box;
  });
}

/**
 * @param host  where the section goes
 * @param burst the parsed burst-scope.json
 * @param fetchFile (path) => Promise<string>, so this file does no auth of its own
 */
export async function renderDeployMap(host, burst, fetchFile) {
  const section = el('section', 'bd');
  host.append(section);

  const head = el('div', 'bd-head');
  head.append(el('h2', 'bu-h2', 'The environment, and how it expands'));
  section.append(head);

  let compose;
  let raw;
  try {
    raw = await fetchFile(COMPOSE);
    compose = parseYaml(raw);
  } catch (err) {
    section.append(el('p', 'bu-error',
      `Could not read ${COMPOSE}: ${err.message}. The map draws the compose file, `
      + 'so there is nothing to draw without it.'));
    return;
  }

  const t = topology(burst, compose);
  if (!t.deployed.length) {
    section.append(el('p', 'bu-error',
      'No service in burst-scope.json is marked deployed, so there is no cluster to draw.'));
    return;
  }

  head.append(el('p', 'bd-sub', `${t.deployed.length} clusters · read from ${COMPOSE} `
    + 'and handoff/burst-scope.json · the slider moves replicas, which is the one '
    + 'thing both files state as a number'));

  // ── controls ──────────────────────────────────────────────────────────────
  const bar = el('div', 'bd-bar');
  const play = el('button', 'bd-play', 'Expand');
  play.type = 'button';
  const range = document.createElement('input');
  range.type = 'range';
  range.className = 'bd-range';
  range.min = '0';
  range.max = '1000';
  range.value = '0';
  range.setAttribute('aria-label', 'Scale between minimum and maximum replicas');
  const ends = el('div', 'bd-ends');
  ends.append(el('span', null, 'at rest'), el('span', null, 'fully expanded'));
  bar.append(play, el('div', 'bd-slide', range), ends);
  section.append(bar);

  // ── readouts ──────────────────────────────────────────────────────────────
  const reads = el('div', 'bd-reads');
  const readout = (label, hint) => {
    const cell = el('div', 'bd-read');
    const v = el('div', 'bd-read-v', '—');
    cell.append(v, el('div', 'bd-read-l', label));
    if (hint) cell.append(el('div', 'bd-read-h', hint));
    reads.append(cell);
    return v;
  };
  const outReplicas = readout('containers running', 'across the three clusters');
  const outClient = readout('client connections asked for', 'replicas × PG_POOL_MAX');
  const outServer = readout('server connections to postgres',
    t.bouncer ? `pgbouncer DEFAULT_POOL_SIZE, ${t.bouncer.mode} mode` : 'no pgbouncer in the file');
  const outRatio = readout('connections per server connection', 'what the pooler absorbs');
  section.append(reads);

  // ── stage ─────────────────────────────────────────────────────────────────
  const stage = el('div', 'bd-stage');
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    class: 'bd-svg',
    role: 'img',
    'aria-label': 'The flash-sale environment: three service clusters behind a connection pooler',
  });
  stage.append(svg);
  section.append(stage);

  const edges = svgEl('g', { class: 'bd-edges' });
  const bodies = svgEl('g');
  svg.append(edges, bodies);

  const boxes = layout(t.deployed.length, t.deployed.map((s) => s.max));

  // buyers
  const ingressY = H / 2;
  const ingress = svgEl('g', { class: 'bd-node bd-ingress' });
  ingress.append(svgEl('rect', { x: 24, y: ingressY - 40, width: 116, height: 80, rx: 10 }));
  const ingressLabel = svgEl('text', { x: 82, y: ingressY - 8, class: 'bd-t-title' });
  ingressLabel.textContent = 'buyers';
  const ingressSub = svgEl('text', { x: 82, y: ingressY + 14, class: 'bd-t-small' });
  ingressSub.textContent = 'one event, one moment';
  ingress.append(ingressLabel, ingressSub);
  bodies.append(ingress);

  // clusters
  const clusters = t.deployed.map((service, n) => {
    const box = boxes[n];
    const g = svgEl('g', { class: 'bd-node bd-cluster' });
    g.append(svgEl('rect', { x: box.x, y: box.y, width: box.w, height: box.h, rx: 10 }));
    const title = svgEl('text', { x: box.x + 14, y: box.y + 24, class: 'bd-t-title' });
    title.textContent = service.short;
    const share = svgEl('text', {
      x: box.x + box.w - 14, y: box.y + 24, class: 'bd-t-small', 'text-anchor': 'end',
    });
    share.textContent = `${service.share}% of the burst`;
    const count = svgEl('text', { x: box.x + 14, y: box.y + 40, class: 'bd-t-small' });
    g.append(title, share, count);

    const cells = [];
    for (let k = 0; k < service.max; k += 1) {
      const col = k % PER_ROW;
      const row = Math.floor(k / PER_ROW);
      const cell = svgEl('rect', {
        x: box.x + 14 + col * (CELL + CELL_GAP),
        y: box.y + 50 + row * (CELL + CELL_GAP),
        width: CELL,
        height: CELL,
        rx: 3,
        class: 'bd-cell',
      });
      cells.push(cell);
      g.append(cell);
    }
    bodies.append(g);
    return { service, box, cells, count };
  });

  // pooler and stores
  const poolX = 560;
  const poolY = H / 2;
  const pool = svgEl('g', { class: 'bd-node bd-pool' });
  pool.append(svgEl('path', {
    // a funnel: wide where the clients arrive, narrow where the pool leaves
    d: `M ${poolX} ${poolY - 92} L ${poolX + 118} ${poolY - 34}`
      + ` L ${poolX + 118} ${poolY + 34} L ${poolX} ${poolY + 92} Z`,
    rx: 8,
  }));
  const poolTitle = svgEl('text', { x: poolX + 40, y: poolY - 6, class: 'bd-t-title' });
  poolTitle.textContent = 'pgbouncer';
  const poolSub = svgEl('text', { x: poolX + 40, y: poolY + 14, class: 'bd-t-small' });
  poolSub.textContent = t.bouncer ? `${t.bouncer.mode} pooling` : '';
  pool.append(poolTitle, poolSub);
  bodies.append(pool);

  const store = (x, y, w, h, title, lines, cls) => {
    const g = svgEl('g', { class: `bd-node ${cls}` });
    g.append(svgEl('rect', { x, y, width: w, height: h, rx: 10 }));
    const tt = svgEl('text', { x: x + 16, y: y + 26, class: 'bd-t-title' });
    tt.textContent = title;
    g.append(tt);
    lines.forEach((line, k) => {
      const node = svgEl('text', { x: x + 16, y: y + 48 + k * 16, class: 'bd-t-small' });
      node.textContent = line;
      g.append(node);
    });
    bodies.append(g);
    return g;
  };

  if (t.postgres) {
    store(772, poolY - 116, 204, 132, 'postgres-hot', [
      `max_connections ${t.postgres.maxConnections}`,
      `shared_buffers ${t.postgres.sharedBuffers ?? '—'}`,
      `${t.postgres.cpus ?? '—'} cpu · ${t.postgres.memory ?? '—'}`,
      t.postgres.synchronousCommit === 'off' ? 'synchronous_commit off' : '',
    ].filter(Boolean), 'bd-pg');
  }
  if (t.redis) {
    store(772, poolY + 40, 204, 78, 'redis', [
      `${t.redis.cpus ?? '—'} cpu · ${t.redis.memory ?? '—'}`,
    ], 'bd-redis');
  }

  // edges: buyers → each cluster → pooler → postgres
  const flow = [];
  const addEdge = (d, weight) => {
    const path = svgEl('path', { d, class: 'bd-edge' });
    edges.append(path);
    flow.push({ path, weight });
    return path;
  };
  for (const c of clusters) {
    const midY = c.box.y + c.box.h / 2;
    addEdge(`M 140 ${ingressY} C 168 ${ingressY}, 168 ${midY}, ${c.box.x} ${midY}`, c.service.share);
    addEdge(
      `M ${c.box.x + c.box.w} ${midY} C ${c.box.x + c.box.w + 40} ${midY},`
      + ` ${poolX - 40} ${poolY}, ${poolX + 4} ${poolY}`,
      c.service.share,
    );
  }
  if (t.postgres) addEdge(`M ${poolX + 118} ${poolY} L 772 ${poolY - 50}`, 100);
  if (t.redis) addEdge(`M ${poolX + 118} ${poolY} L 772 ${poolY + 79}`, 20);

  // ── the part expansion does not help ──────────────────────────────────────
  if (t.contended.length) {
    const risk = el('div', 'bd-risk');
    risk.append(el('h3', 'bd-risk-h', 'Where adding replicas stops helping'));
    risk.append(el('p', 'bd-risk-p',
      `${t.contended.length} of the ${(burst.tables ?? []).length} tables carry `
      + 'contended: true. Every buyer wants the same rows, the lease path serialises, '
      + 'and a cluster three times the size is three times the contention for them. '
      + 'The slider above makes this worse, not better.'));
    for (const table of t.contended) {
      const row = el('div', 'bd-risk-row');
      row.append(el('code', 'bd-risk-t', table.table));
      const locks = t.locks.filter((op) => (op.writes ?? []).includes(table.table));
      const holders = el('div', 'bd-risk-ops');
      for (const op of locks) {
        const chip = el('span', 'bd-lock');
        chip.append(el('strong', null, op.operationId), document.createTextNode(` ${op.lock}`));
        holders.append(chip);
      }
      if (!locks.length) holders.append(el('span', 'bd-lock bd-lock-none', 'no lock stated'));
      row.append(holders);
      if (table.note) row.append(el('p', 'bd-risk-n', table.note));
      risk.append(row);
    }
    section.append(risk);
  }

  // ── what is not in the picture ────────────────────────────────────────────
  if (t.absent.length) {
    const off = el('div', 'bd-absent');
    const onPath = t.absent.filter((s) => s.onBurstPath);
    off.append(el('h3', 'bd-risk-h',
      `${t.absent.length} services are not in this drawing`));
    off.append(el('p', 'bd-risk-p',
      `${onPath.length} of them are on the burst path and answered by the shared cell — `
      + 'absent from the environment is not absent from the sale. The rest see no part '
      + 'of a ticket sale at all.'));
    const strip = el('div', 'bd-strip');
    for (const s of t.absent) {
      const chip = el('span', `bd-off${s.onBurstPath ? ' bd-off-path' : ''}`);
      chip.append(el('strong', null, s.name.replace(/Service$/, '')));
      chip.title = s.reason ?? '';
      strip.append(chip);
    }
    off.append(strip);
    section.append(off);
  }

  // ── the scenario, in its own words ────────────────────────────────────────
  const note = leadingNote(raw);
  if (note) {
    const box = el('details', 'bd-note');
    box.append(el('summary', null, `Why this scenario exists — the header of ${COMPOSE}`));
    box.append(el('pre', 'bd-note-body', note));
    section.append(box);
  }

  // ── the animation ─────────────────────────────────────────────────────────
  const totalMin = t.deployed.reduce((a, s) => a + s.min, 0);
  const totalMax = t.deployed.reduce((a, s) => a + s.max, 0);

  const apply = (u) => {
    let replicas = 0;
    let client = 0;
    for (const c of clusters) {
      const n = Math.round(c.service.min + (c.service.max - c.service.min) * u);
      replicas += n;
      client += n * c.service.poolMax;
      c.cells.forEach((cell, k) => cell.classList.toggle('on', k < n));
      c.count.textContent = `${n} of ${c.service.max} replicas`
        + (c.service.poolMax ? ` · ${n * c.service.poolMax} connections` : '');
    }
    const server = t.bouncer?.poolSize ?? 0;
    outReplicas.textContent = String(replicas);
    outClient.textContent = client ? client.toLocaleString('en-GB') : '—';
    outServer.textContent = server ? String(server) : '—';
    outRatio.textContent = server && client ? `${(client / server).toFixed(1)} : 1` : '—';
    // Over the pooler's own ceiling is worth saying, and it is stated in the
    // file rather than guessed: MAX_CLIENT_CONN is what pgbouncer will accept.
    const over = t.bouncer?.maxClient ? client > t.bouncer.maxClient : false;
    outClient.classList.toggle('bd-over', over);
    // Traffic moves faster as the cluster grows, and weight is the service's
    // share of the burst, so the Catalogue lane visibly carries most of it.
    // Skipped outright when the reader has asked for less motion — the
    // drawing still reads without it, which is why the dashes are decoration
    // and the cell fills are not.
    if (!stillness.matches) {
      const now = performance.now();
      for (const f of flow) {
        f.path.style.strokeDashoffset =
          String(-((now / (24 - 16 * u)) * (0.2 + f.weight / 100)) % 1000);
      }
    }
    section.style.setProperty('--bd-u', String(u));
  };

  const stillness = window.matchMedia('(prefers-reduced-motion: reduce)');

  let u = 0;
  let playing = false;
  let last = 0;

  const frame = (now) => {
    if (playing) {
      const dt = last ? Math.min(64, now - last) : 16;
      u = Math.min(1, u + dt / 2600);
      range.value = String(Math.round(u * 1000));
      if (u >= 1) { playing = false; play.textContent = 'Reset'; }
    }
    last = now;
    apply(u);
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  play.onclick = () => {
    if (u >= 1) { u = 0; range.value = '0'; playing = true; play.textContent = 'Pause'; return; }
    playing = !playing;
    play.textContent = playing ? 'Pause' : 'Expand';
  };
  range.oninput = () => {
    playing = false;
    play.textContent = 'Expand';
    u = Number(range.value) / 1000;
  };

  head.append(el('p', 'bd-sub bd-sub-fine',
    `At rest ${totalMin} containers, fully expanded ${totalMax}. `
    + 'The requests-per-second figures the scenario quotes are prose in the compose '
    + 'header, not structured data, so they are shown there rather than animated here.'));
}
