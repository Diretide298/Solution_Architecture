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

/** `**bold**` is the package's emphasis; a title attribute cannot render it. */
const stripEmphasis = (text) => String(text ?? '').replace(/\*\*/g, '').trim();

/**
 * @param host  where the section goes
 * @param burst the parsed burst-scope.json
 * @param io    { file(path), api(route) } — this file does no auth of its own.
 *              Two fetchers because it needs one package file, the compose, and
 *              one already-parsed payload, the state machine behind /api/domain.
 */
export async function renderDeployMap(host, burst, io) {
  const section = el('section', 'bd');
  host.append(section);

  const head = el('div', 'bd-head');
  head.append(el('h2', 'bu-h2', 'The environment, and how it expands'));
  section.append(head);

  let compose;
  let raw;
  try {
    raw = await io.file(COMPOSE);
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

  head.append(el('p', 'bd-sub',
    `${t.deployed.length} clusters · ${COMPOSE} and handoff/burst-scope.json for the machine, `
    + 'states/burst-environment.yaml for the lifecycle, ADR-0031 to 0035 for the rules'));

  // ── the lifecycle ─────────────────────────────────────────────────────────
  // **Read from the package, not written here.** `states/burst-environment.yaml`
  // is the state model and the server has already parsed it — `/api/domain`
  // carries all 125 machines with their guards. Retyping nine states into this
  // file would be a second copy to disagree with the first the day somebody
  // adds one.
  //
  // Parsing it here was the alternative and it was rejected after trying: the
  // compose subset is regular enough to hand-parse and was checked against
  // js-yaml on all four configs, but the state files use multi-line quoted
  // scalars and a hand-rolled reader silently returned the first line of every
  // guard. A parser that is quietly wrong is worse than no parser.
  let machine = null;
  try {
    const domain = await io.api('domain');
    machine = (domain?.machines ?? []).find((m) => m.id === 'burst-environment') ?? null;
  } catch { machine = null; }

  // The happy path, walked rather than listed: from the initial state, take the
  // transition that is not into a terminal failure, until there is nowhere left
  // to go. A state added to the model appears here without an edit.
  const phases = [];
  if (machine) {
    const terminalFail = new Set((machine.terminal ?? []).filter((x) => x === 'failed'));
    const out = new Map();
    for (const tr of machine.transitions ?? []) {
      if (!out.has(tr.from)) out.set(tr.from, []);
      out.get(tr.from).push(tr);
    }
    let at = (machine.initial ?? [])[0] ?? null;
    const seen = new Set();
    while (at && !seen.has(at)) {
      seen.add(at);
      phases.push({ name: at, into: null });
      const next = (out.get(at) ?? []).find((tr) => !terminalFail.has(tr.to) && !seen.has(tr.to));
      if (!next) break;
      phases[phases.length - 1].into = next;
      at = next.to;
    }
  }
  // No machine, no lifecycle — the map still draws, it just does not step.
  const hasPhases = phases.length > 1;

  /**
   * How each state looks. A lookup with a default rather than a required
   * entry per state: the phases come from the package, so a state this file
   * has never heard of must still draw as something reasonable.
   */
  const LOOK = {
    requested: { infra: 0, replicas: 0, flow: 0, arriving: false },
    provisioning: { infra: 1, replicas: 0, flow: 0, arriving: false },
    warming: { infra: 1, replicas: 'min', flow: 0.2, arriving: false },
    live: { infra: 1, replicas: 'ramp', flow: 1, arriving: true },
    draining: { infra: 1, replicas: 'max', flow: 0.3, arriving: false },
    reconciling: { infra: 1, replicas: 'min', flow: 0.15, arriving: false, replay: true },
    reconciled: { infra: 1, replicas: 0, flow: 0, arriving: false },
    decommissioned: { infra: 0, replicas: 0, flow: 0, arriving: false },
  };
  const lookOf = (name) => LOOK[name] ?? { infra: 1, replicas: 'min', flow: 0.3, arriving: false };

  // ── controls ──────────────────────────────────────────────────────────────
  const bar = el('div', 'bd-bar');
  const play = el('button', 'bd-play', hasPhases ? 'Run the sale' : 'Expand');
  play.type = 'button';
  const range = document.createElement('input');
  range.type = 'range';
  range.className = 'bd-range';
  range.min = '0';
  range.max = '1000';
  range.value = '0';
  range.setAttribute('aria-label', hasPhases
    ? 'Move through the environment lifecycle'
    : 'Scale between minimum and maximum replicas');
  bar.append(play, el('div', 'bd-slide', range));
  section.append(bar);

  const steps = el('div', 'bd-steps');
  const stepNodes = phases.map((phase, n) => {
    const node = el('button', 'bd-step');
    node.type = 'button';
    node.append(el('span', 'bd-step-dot'));
    node.append(el('span', 'bd-step-name', phase.name));
    node.title = phase.into?.guard
      ? stripEmphasis(phase.into.guard)
      : `${phase.name} — from states/burst-environment.yaml`;
    node.onclick = () => seek(n / Math.max(1, phases.length - 1));
    steps.append(node);
    return node;
  });
  if (hasPhases) section.append(steps);

  const guard = el('p', 'bd-guard');
  if (hasPhases) section.append(guard);

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
    preserveAspectRatio: 'xMidYMid meet',
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
    return { service, box, cells, count, node: g };
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

  // ── the write path ────────────────────────────────────────────────────────
  // ADR-0033. Drawn because "how does it hold up" and "what happens to the
  // writes" are the same question at 5,000 RPS, and the second is the half a
  // topology diagram normally leaves out.
  const wp = el('div', 'bd-panel bd-writes');
  wp.append(el('h3', 'bd-risk-h', 'What happens to a write'));
  wp.append(el('p', 'bd-risk-p',
    'The state change and its outbox row commit in one transaction, or neither '
    + 'does — a broker acknowledging a publish that then rolls back is the '
    + 'exactly-once problem restated. A relay publishes from the outbox at least '
    + 'once, and every consumer is idempotent because every write already carries '
    + 'an idempotency key. ADR-0033.'));

  const WP_W = 940;
  const WP_H = 180;
  const wsvg = svgEl('svg', {
    viewBox: `0 0 ${WP_W} ${WP_H}`,
    preserveAspectRatio: 'xMidYMid meet',
    class: 'bd-wsvg',
    role: 'img',
    'aria-label': 'A write commits with its outbox row, a relay publishes it, and a delivery '
      + 'that keeps failing dead-letters after five attempts',
  });
  const wstage = el('div', 'bd-stage bd-stage-flat');
  wstage.append(wsvg);
  wp.append(wstage);

  const wbox = (x, y, w, h, title, sub, cls) => {
    const g = svgEl('g', { class: `bd-node ${cls ?? ''}` });
    g.append(svgEl('rect', { x, y, width: w, height: h, rx: 8 }));
    const a = svgEl('text', {
      x: x + w / 2, y: y + (sub ? 25 : h / 2 + 4), class: 'bd-t-title bd-t-mid',
    });
    a.textContent = title;
    g.append(a);
    if (sub) {
      const b = svgEl('text', { x: x + w / 2, y: y + 42, class: 'bd-t-small bd-t-mid' });
      b.textContent = sub;
      g.append(b);
    }
    wsvg.append(g);
    return g;
  };

  const wline = (d, cls) => {
    wsvg.append(svgEl('path', { d, class: `bd-edge ${cls ?? ''}` }));
  };

  // one transaction, drawn as one box around two writes
  const txn = svgEl('g', { class: 'bd-node bd-txn' });
  txn.append(svgEl('rect', { x: 14, y: 22, width: 226, height: 100, rx: 10 }));
  const txnLabel = svgEl('text', { x: 127, y: 40, class: 'bd-t-small bd-t-mid' });
  txnLabel.textContent = 'one transaction';
  txn.append(txnLabel);
  wsvg.append(txn);
  wbox(28, 50, 92, 58, 'row', 'the change', 'bd-w-row');
  wbox(138, 50, 92, 58, 'outbox', 'the event', 'bd-w-outbox');

  wbox(278, 50, 116, 58, 'relay', 'reads, publishes', 'bd-w-relay');
  wbox(444, 50, 116, 58, 'broker', 'at least once', 'bd-w-broker');
  wbox(610, 50, 132, 58, 'consumer', 'idempotent', 'bd-w-consumer');
  wbox(596, 126, 160, 40, 'retry x5', 'exponential, jittered', 'bd-w-retry');
  wbox(790, 50, 136, 58, 'dead_letter', 'a row somebody works', 'bd-w-dead');

  wline('M 240 79 H 278');
  wline('M 394 79 H 444');
  wline('M 560 79 H 610');
  wline('M 676 108 V 126', 'bd-edge-warn');
  wline('M 756 146 H 858 V 108', 'bd-edge-warn');

  const wdot = svgEl('circle', { r: 4.5, cx: 28, cy: 79, class: 'bd-wdot', opacity: '0' });
  wsvg.append(wdot);

  wp.append(el('p', 'bd-risk-n',
    'Two things are never dead-lettered. ledger.journal_entry, because a failed '
    + 'financial posting is an incident rather than a queue item, and '
    + 'platform.dsar_request, because it carries a legal clock. Both halt and alert — '
    + 'the distinction is whether silent accumulation is acceptable, and for those '
    + 'two it never is. ADR-0033.'));
  wp.append(el('p', 'bd-risk-n',
    'synchronous_commit is off on this database. A crash loses the last few '
    + 'milliseconds of commits, traded for fifty seconds of throughput. ADR-0035 '
    + 'calls that a decision rather than a setting, and a data-loss bug if it is '
    + 'copied from a tuning guide.'));
  section.append(wp);

  // ── the part expansion does not help ──────────────────────────────────────
  if (t.contended.length) {
    const risk = el('div', 'bd-panel bd-risk');
    risk.append(el('h3', 'bd-risk-h', 'Where adding replicas stops helping'));
    risk.append(el('p', 'bd-risk-p',
      `${t.contended.length} of the ${(burst.tables ?? []).length} tables carry `
      + 'contended: true. Every buyer wants the same rows, the lease path serialises, '
      + 'and a cluster four times the size is four times the contention for them. '
      + 'ADR-0031 takes a row lock on exactly four operations and nowhere else, because '
      + 'optimistic retry under contention is worse than a lock: at 5,000 RPS every '
      + 'retry is another read, and the retry storm is the outage.'));
    for (const table of t.contended) {
      const row = el('div', 'bd-risk-row');
      row.append(el('code', 'bd-risk-t', table.table));
      const locks = t.locks.filter((op) => (op.writes ?? []).includes(table.table));
      const holders = el('div', 'bd-risk-ops');
      for (const op of locks) {
        const chip = el('span', 'bd-lock');
        chip.append(el('strong', null, op.operationId), document.createTextNode(` ${op.lock}`));
        chip.title = /SKIP LOCKED/.test(op.lock)
          ? 'SKIP LOCKED turns contention into throughput where the caller does not care '
            + 'which row it gets: a buyer who cannot have seat 14 gets seat 15 in the '
            + 'same query rather than failing and retrying. ADR-0031.'
          : 'Plain FOR UPDATE, where the caller does care. Somebody choosing seat 14 '
            + 'waits or is told no; they must not silently receive seat 15. ADR-0031.';
        holders.append(chip);
      }
      if (!locks.length) holders.append(el('span', 'bd-lock bd-lock-none', 'no lock stated'));
      row.append(holders);
      if (table.note) row.append(el('p', 'bd-risk-n', table.note));
      risk.append(row);
    }
    risk.append(el('p', 'bd-risk-n',
      'A lease expires and a lock does not, which is the property CF-115 chose. A held '
      + 'seat whose holder closes the browser is free again in ten minutes, and the lock '
      + 'is held for the length of the statement rather than the length of the decision.'));
    section.append(risk);
  }

  // ── thresholds ────────────────────────────────────────────────────────────
  // ADR-0032, split into what this page computes from the compose file and what
  // the ADR states as a rule. The two are not equally checkable, and a panel
  // that mixes them invites a reader to trust both the same amount.
  const thr = el('div', 'bd-panel bd-thr');
  thr.append(el('h3', 'bd-risk-h', 'The thresholds, and what trips them'));
  const thrList = el('div', 'bd-thr-list');
  const rule = (name, value, note, computed) => {
    const row = el('div', `bd-thr-row${computed ? ' bd-thr-computed' : ''}`);
    row.append(el('span', 'bd-thr-n', name));
    row.append(el('span', 'bd-thr-v', value));
    row.append(el('span', 'bd-thr-note', note));
    thrList.append(row);
    return row;
  };
  const poolRow = t.bouncer
    ? rule('pooler ceiling', `${t.bouncer.maxClient.toLocaleString('en-GB')} clients`,
      'MAX_CLIENT_CONN. Fully expanded the three clusters ask for 1,560, so the pooler '
      + 'is not the limit here. The funnel is deliberate rather than incidental.', true)
    : null;
  if (t.bouncer) {
    rule('server connections', String(t.bouncer.poolSize),
      `DEFAULT_POOL_SIZE, ${t.bouncer.mode} mode. Session mode holds a server connection `
      + 'for the life of a client one and buys nothing; transaction mode returns it at '
      + 'commit. That is what forbids session-scoped state, and why ADR-0031 takes its '
      + 'singleton lock inside one transaction.', true);
  }
  if (t.postgres?.maxConnections) {
    rule('primary ceiling', `${t.postgres.maxConnections} connections`,
      'What the pooler protects. Services connect to the pooler and never to the '
      + 'primary. ADR-0032.', true);
  }
  rule('backpressure', '429 + Retry-After',
    'Every service declares a concurrency limit and refuses early rather than queueing '
    + 'until it dies. The package states the rule and gives no number, so none is shown '
    + 'here. Retry-After is jittered: a fixed value synchronises every client into one '
    + 'retry instant, which is the thundering herd wearing a different hat. ADR-0032.');
  rule('shed order', 'guest, public, then staff, service',
    'Shed by audience rather than uniformly — a staff till completing a sale outranks a '
    + 'guest browsing a catalogue, and x-ticvai-audience already says which is which. '
    + 'ADR-0032.');
  rule('circuit breaker', '5 in a row, or 50% of 20',
    'Open on five consecutive failures or a half error rate over twenty calls; half-open '
    + 'after thirty seconds. An open breaker makes the error arrive in ten milliseconds '
    + 'instead of at a thirty-second timeout. ADR-0032.');
  rule('cache TTL', 'plus or minus 10%',
    'Entries written together must not expire together. With single-flight, and '
    + 'stale-while-revalidate on cache:resolution, which is read on every authorised '
    + 'call — when it expires at 5,000 RPS every request goes to the database at the '
    + 'same instant. ADR-0032.');
  rule('outbox retry', '5 attempts, from 1s',
    'Exponential and jittered, then dead-letter. A replay is recorded as a new attempt '
    + 'rather than resetting the count, so an operator retrying the same poison message '
    + 'forty times can see that they did. ADR-0033.');
  thr.append(thrList);
  thr.append(el('p', 'bd-risk-n',
    'The highlighted rows are computed from the compose file on this page. The rest are '
    + 'rules the ADRs state, shown as stated — where the package declares a limit '
    + 'without giving it a value, no value is invented here.'));
  section.append(thr);

  // ── reconciliation ────────────────────────────────────────────────────────
  const rec = el('div', 'bd-panel bd-rec');
  rec.append(el('h3', 'bd-risk-h', 'Merging back, which is the edge that matters'));
  rec.append(el('p', 'bd-risk-p',
    'The other cell kinds are places data lives; this one is a place data passes '
    + 'through, so every order taken here has to reach the permanent platform. '
    + 'decommissioned is reachable only through reconciled, and '
    + 'decommissionBurstEnvironment returns 409 otherwise. An environment torn down '
    + 'before its orders land has lost real money and real tickets, and no path in the '
    + 'state model allows it. ADR-0035.'));

  const recBar = el('div', 'bd-recbar');
  const recFill = el('div', 'bd-recfill');
  recBar.append(recFill);
  rec.append(recBar);
  const recNote = el('p', 'bd-rec-note', 'idle');
  rec.append(recNote);

  const props = el('div', 'bd-thr-list');
  const prop = (name, note) => {
    const row = el('div', 'bd-thr-row');
    row.append(el('span', 'bd-thr-n', name));
    row.append(el('span', 'bd-thr-note', note));
    props.append(row);
  };
  prop('environment id', 'in place of the device id syncOrders uses one layer down — the '
    + 'shape already existed for an offline till journal');
  prop('monotonic sequence', 'what orders the replay');
  prop('idempotent replay', 'the same property every write in the platform already has');
  prop('sync.rejection', 'what will not apply is kept and reported. Thirty thousand '
    + 'silently lost sales is worse than thirty thousand reported ones');
  prop('resumable', 'which is what the self-transition on reconciling is for: interrupted '
    + 'at order 18,000 of 30,000, it continues from 18,000 rather than starting again');
  rec.append(props);
  rec.append(el('p', 'bd-open',
    'Open, and deliberately. The catalogue here is a snapshot rather than a replica, so '
    + 'if the permanent platform changes a price during the sale, reconciliation has to '
    + 'decide which one the guest paid. priceDivergencePolicy names honourSnapshot, '
    + 'honourCurrent and reject, and has no default — somebody chooses per sale, because '
    + 'the answer depends on how large the divergence is and who the venue would rather '
    + 'disappoint.'));
  section.append(rec);

  // ── what is not in the picture ────────────────────────────────────────────
  if (t.absent.length) {
    const off = el('div', 'bd-panel bd-absent');
    const onPath = t.absent.filter((x) => x.onBurstPath);
    off.append(el('h3', 'bd-risk-h', `${t.absent.length} services are not in this drawing`));
    off.append(el('p', 'bd-risk-p',
      `${onPath.length} of them are on the burst path and answered by the shared cell — `
      + 'absent from the environment is not absent from the sale. The rest see no part of '
      + 'a ticket sale at all.'));
    const strip = el('div', 'bd-strip');
    for (const x of t.absent) {
      const chip = el('span', `bd-off${x.onBurstPath ? ' bd-off-path' : ''}`);
      chip.append(el('strong', null, x.name.replace(/Service$/, '')));
      chip.title = x.reason ?? '';
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
  const totalMin = t.deployed.reduce((a, x) => a + x.min, 0);
  const totalMax = t.deployed.reduce((a, x) => a + x.max, 0);
  const stillness = window.matchMedia('(prefers-reduced-motion: reduce)');
  const replayAt = phases.findIndex((x) => lookOf(x.name).replay);

  let p = 0;
  let playing = false;
  let last = 0;

  const phaseAt = (u) => {
    if (!hasPhases) return { index: 0, name: 'live', within: u };
    const span = 1 / phases.length;
    const index = Math.min(phases.length - 1, Math.floor(u / span));
    return { index, name: phases[index].name, within: Math.min(1, (u - index * span) / span) };
  };

  const apply = () => {
    const at = phaseAt(p);
    const look = lookOf(at.name);
    // Only `live` ramps. Every other state holds a fixed size, so stepping back
    // to warming shows the environment small again rather than leaving it at
    // whatever the last phase grew it to.
    const u = look.replicas === 'ramp' ? at.within : look.replicas === 'max' ? 1 : 0;
    const running = look.replicas !== 0;

    let replicas = 0;
    let client = 0;
    for (const c of clusters) {
      const n = running ? Math.round(c.service.min + (c.service.max - c.service.min) * u) : 0;
      replicas += n;
      client += n * c.service.poolMax;
      c.cells.forEach((cell, k) => cell.classList.toggle('on', k < n));
      c.count.textContent = running
        ? `${n} of ${c.service.max} replicas`
          + (c.service.poolMax ? ` · ${n * c.service.poolMax} connections` : '')
        : 'not running';
      c.node.classList.toggle('bd-quiet', !running);
    }

    const server = t.bouncer?.poolSize ?? 0;
    outReplicas.textContent = String(replicas);
    outClient.textContent = client ? client.toLocaleString('en-GB') : '—';
    outServer.textContent = running && server ? String(server) : '—';
    outRatio.textContent = server && client ? `${(client / server).toFixed(1)} : 1` : '—';
    const over = t.bouncer?.maxClient ? client > t.bouncer.maxClient : false;
    outClient.classList.toggle('bd-over', over);
    if (poolRow) poolRow.classList.toggle('bd-thr-hot', over);

    section.style.setProperty('--bd-infra', String(look.infra));
    ingress.classList.toggle('bd-quiet', !look.arriving);

    if (hasPhases) {
      stepNodes.forEach((node, n) => {
        node.classList.toggle('bd-step-on', n === at.index);
        node.classList.toggle('bd-step-done', n < at.index);
      });
      const into = phases[at.index]?.into;
      guard.textContent = into?.guard
        ? stripEmphasis(into.guard)
        : `${at.name} — a terminal state of the model`;
    }

    // the write path runs while the sale does
    const writing = look.flow > 0.5;
    wp.classList.toggle('bd-idle', !writing);
    if (!stillness.matches && writing) {
      const cycle = (performance.now() / 2600) % 1;
      wdot.setAttribute('cx', String(28 + cycle * 870));
      wdot.setAttribute('opacity', '1');
    } else {
      wdot.setAttribute('opacity', '0');
    }

    // reconciliation runs in its own phase and nowhere else
    if (look.replay) {
      const done = Math.round(at.within * 100);
      recFill.style.width = `${done}%`;
      recNote.textContent = `replaying in sequence · ${done}% · resumable, so an `
        + 'interruption here continues from where it stopped rather than restarting';
      rec.classList.remove('bd-idle');
    } else {
      const past = replayAt >= 0 && at.index > replayAt;
      recFill.style.width = past ? '100%' : '0%';
      recNote.textContent = past
        ? 'reconciled — and only now may the environment be torn down'
        : 'idle';
      rec.classList.add('bd-idle');
    }

    if (!stillness.matches) {
      const now = performance.now();
      for (const f of flow) {
        f.path.style.strokeOpacity = String(0.1 + 0.5 * look.flow);
        f.path.style.strokeDashoffset =
          String(-((now / (24 - 16 * u)) * (0.2 + f.weight / 100)) % 1000);
      }
    }
  };

  const seek = (v) => {
    playing = false;
    play.textContent = hasPhases ? 'Run the sale' : 'Expand';
    p = Math.max(0, Math.min(1, v));
    range.value = String(Math.round(p * 1000));
  };

  const frame = (now) => {
    if (playing) {
      const dt = last ? Math.min(64, now - last) : 16;
      // The sale is the part worth watching, so it gets the time. Provisioning
      // takes minutes and the sale takes seconds, which is the ADR's point and
      // the reverse of what is useful to sit through.
      const pace = lookOf(phaseAt(p).name).replicas === 'ramp' ? 7000 : 2200;
      p = Math.min(1, p + dt / pace);
      range.value = String(Math.round(p * 1000));
      if (p >= 1) { playing = false; play.textContent = 'Again'; }
    }
    last = now;
    apply();
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  play.onclick = () => {
    if (p >= 1) { p = 0; range.value = '0'; }
    playing = !playing;
    play.textContent = playing ? 'Pause' : (hasPhases ? 'Run the sale' : 'Expand');
  };
  range.oninput = () => { seek(Number(range.value) / 1000); };

  head.append(el('p', 'bd-sub bd-sub-fine',
    `At rest ${totalMin} containers, fully expanded ${totalMax}. `
    + (hasPhases
      ? `${phases.length} phases, walked from states/burst-environment.yaml — the line `
        + 'under the strip is the package’s own guard for that step. '
      : '')
    + 'The requests-per-second figures the scenario quotes are prose in the compose '
    + 'header, not structured data, so they are shown there rather than animated here.'));
}
