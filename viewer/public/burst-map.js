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
// The platform the burst sits beside, so the two can be drawn to the same
// scale and the merge back has somewhere to land.
const PERMANENT = 'deploy/b-shared-platform.yml';

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


/** `**bold**` is the package's emphasis; a title attribute cannot render it. */
const stripEmphasis = (text) => String(text ?? '').replace(/\*\*/g, '').trim();

/**
/**
 * What the burst costs, and the rate it costs it at.
 *
 * **The four totals are ADR-0035's, quoted.** The split across containers is
 * not: the ADR prices the environment and says nothing about which part of it
 * is which. So the rate is anchored on the ADR — the month figure, $8,587 over
 * 720 hours, being the longest-run of the four and therefore the least
 * sensitive to rounding — and apportioned across containers by the `cpus`
 * limits the compose file already declares.
 *
 * That apportionment is a model and it is labelled as one on the page. What it
 * buys is the thing a flat hourly rate cannot show: **a half-expanded
 * environment costs less than a full one**, which is the whole argument for a
 * threshold you can move.
 */
const COST_POINTS = [
  { hours: 2, usd: 24, label: 'a two-hour sale' },
  { hours: 6, usd: 71, label: 'six hours' },
  { hours: 24, usd: 282, label: 'a day' },
  { hours: 720, usd: 8587, label: 'a month left running' },
];
const RATE_PER_HOUR = 8587 / 720;

/** `32G` -> 32, `512M` -> 0.5. Compose states memory as a limit string. */
const gigs = (value) => {
  const hit = String(value ?? '').match(/^([\d.]+)\s*([GMK])?/i);
  if (!hit) return 0;
  const n = Number(hit[1]);
  const unit = (hit[2] ?? 'G').toUpperCase();
  return unit === 'M' ? n / 1024 : unit === 'K' ? n / 1048576 : n;
};

/**
 * Indicative list rates for serverless container compute, per vCPU-hour and
 * per GB-hour.
 *
 * **These are not the package's numbers, and there is no provider to make them
 * the package's.** CF-64 — the cloud provider — is open, owned by Dinesh and
 * Qossai, and the brief records the shortlist as *AWS or Azure, pending DESC*.
 * Everything above that line in the package is provider-neutral and, as the
 * brief puts it, nothing below it can be: managed Postgres, the Redis tier,
 * Qdrant hosting, the CDN and the secret store all follow from the choice.
 *
 * Azure is here because it is the other candidate. GCP is here because it was
 * asked for, and it is worth knowing that it is not on the shortlist.
 *
 * They price container compute and nothing else — no managed-database premium,
 * no storage, no IO, no egress, no support plan — which is most of why they
 * land under ADR-0035's own figure. Check them before quoting them.
 */
const PROVIDERS = [
  { key: 'aws', name: 'AWS Fargate', region: 'us-east-1', vcpu: 0.04048, gb: 0.004445 },
  { key: 'gcp', name: 'Google Cloud Run', region: 'us-central1', vcpu: 0.0456, gb: 0.0050 },
  { key: 'azure', name: 'Azure Container Apps', region: 'East US', vcpu: 0.0432, gb: 0.0054 },
];

const money = (usd) => (usd < 10
  ? `$${usd.toFixed(2)}`
  : `$${Math.round(usd).toLocaleString('en-GB')}`);

const clock = (minutes) => {
  const h = Math.floor(minutes / 60);
  const m = Math.floor(minutes % 60);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
};

// ── geometry ────────────────────────────────────────────────────────────────
const W = 1200;
const H = 640;
const CELL = 22;
const CELL_GAP = 5;
const PER_ROW = 5;

/**
 * @param host  where the section goes
 * @param burst the parsed burst-scope.json
 * @param io    { file(path), api(route) } — this file does no auth of its own.
 */
export async function renderDeployMap(host, burst, io) {
  const section = el('section', 'bd');
  host.append(section);

  const head = el('div', 'bd-head');
  head.append(el('h2', 'bu-h2', 'The environment, and how it expands'));
  section.append(head);

  let compose;
  let permanent = null;
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
  // The platform the burst sits beside. Optional: if it is not there the burst
  // still draws, it just draws alone.
  try { permanent = parseYaml(await io.file(PERMANENT)); } catch { permanent = null; }

  const t = topology(burst, compose);
  if (!t.deployed.length) {
    section.append(el('p', 'bu-error',
      'No service in burst-scope.json is marked deployed, so there is no cluster to draw.'));
    return;
  }

  head.append(el('p', 'bd-sub',
    `${t.deployed.length} clusters beside the permanent platform · ${COMPOSE} and `
    + `${PERMANENT} for the machines, handoff/burst-scope.json for the shape, `
    + 'states/burst-environment.yaml for the lifecycle, ADR-0031 to 0035 for the rules'));

  // ── the lifecycle ─────────────────────────────────────────────────────────
  // Read from the package, not written here. /api/domain carries all 125 parsed
  // machines, so retyping nine states into a viewer file would be a second copy
  // to disagree with the first the day somebody adds one.
  let machine = null;
  try {
    const domain = await io.api('domain');
    machine = (domain?.machines ?? []).find((m) => m.id === 'burst-environment') ?? null;
  } catch { machine = null; }

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
  const hasPhases = phases.length > 1;

  /** How each state looks. A lookup with a default: the phases come from the
   *  package, so a state this file has never heard of must still draw. */
  const LOOK = {
    requested: { infra: 0, load: 0, arriving: false, billing: false },
    provisioning: { infra: 1, load: 0, arriving: false, billing: true },
    warming: { infra: 1, load: 0.05, arriving: false, billing: true },
    live: { infra: 1, load: 'ramp', arriving: true, billing: true },
    draining: { infra: 1, load: 0.25, arriving: false, billing: true },
    reconciling: { infra: 1, load: 0.08, arriving: false, billing: true, replay: true },
    reconciled: { infra: 1, load: 0, arriving: false, billing: true },
    decommissioned: { infra: 0, load: 0, arriving: false, billing: false },
  };
  const lookOf = (name) => LOOK[name] ?? { infra: 1, load: 0.2, arriving: false, billing: true };

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
  range.setAttribute('aria-label', 'Move through the environment lifecycle');
  bar.append(play, el('div', 'bd-slide', range));
  section.append(bar);

  // The threshold. **Yours, not the package's** — b-shared-platform.yml says
  // "Catalogue and Order autoscale on RPS" and burst-scope says "replicates on
  // RPS", and neither says at what. Rather than invent a number and present it
  // as the package's, it is a control: the number is the reader's to choose and
  // the consequences are drawn.
  const thrBar = el('div', 'bd-bar bd-bar-thr');
  const thrRange = document.createElement('input');
  thrRange.type = 'range';
  thrRange.className = 'bd-range';
  thrRange.min = '40';
  thrRange.max = '100';
  thrRange.value = '70';
  thrRange.setAttribute('aria-label', 'Target utilisation per replica');
  const thrLabel = el('span', 'bd-thr-live', '70%');
  thrBar.append(
    el('span', 'bd-bar-label', 'add a replica above'),
    el('div', 'bd-slide', thrRange),
    thrLabel,
    el('span', 'bd-bar-note', 'utilisation per replica — the package says these autoscale on '
      + 'RPS and never says at what, so this one is yours'),
  );
  section.append(thrBar);

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
  const readout = (label, hint, cls) => {
    const cell = el('div', `bd-read ${cls ?? ''}`);
    const v = el('div', 'bd-read-v', '—');
    cell.append(v, el('div', 'bd-read-l', label));
    if (hint) cell.append(el('div', 'bd-read-h', hint));
    reads.append(cell);
    return v;
  };
  const outClockV = readout('elapsed', 'one second of yours is a minute of the sale');
  const outSpend = readout('spent so far', 'apportioned by cpu limits', 'bd-read-cost');
  const outRate = readout('burn rate', 'per hour at this size');
  const outReplicas = readout('containers running', 'across the three clusters');
  const outClient = readout('client connections asked for', 'replicas × PG_POOL_MAX');
  const outRatio = readout('per server connection', `${t.bouncer?.poolSize ?? '—'} in the pool`);
  section.append(reads);

  const capped = el('p', 'bd-capped');
  capped.hidden = true;
  section.append(capped);

  // ── stage ─────────────────────────────────────────────────────────────────
  const stage = el('div', 'bd-stage');
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    preserveAspectRatio: 'xMidYMid meet',
    class: 'bd-svg',
    role: 'img',
    'aria-label': 'The permanent platform on the left, the burst environment on the right, '
      + 'and the reconciliation that merges one back into the other',
  });
  stage.append(svg);
  section.append(stage);

  const edges = svgEl('g', { class: 'bd-edges' });
  const bodies = svgEl('g');
  svg.append(edges, bodies);

  const box = (parent, x, y, w, h, cls) => {
    const g = svgEl('g', { class: `bd-node ${cls ?? ''}` });
    g.append(svgEl('rect', { x, y, width: w, height: h, rx: 9 }));
    parent.append(g);
    return g;
  };
  const text = (parent, x, y, cls, value) => {
    const node = svgEl('text', { x, y, class: cls });
    node.textContent = value;
    parent.append(node);
    return node;
  };
  const label = (parent, x, y, value) => text(parent, x, y, 'bd-t-label', value);

  // ── left: the permanent platform ──────────────────────────────────────────
  const perm = svgEl('g', { class: 'bd-perm' });
  bodies.append(perm);
  perm.append(svgEl('rect', { x: 14, y: 36, width: 536, height: 480, rx: 12, class: 'bd-frame' }));
  text(perm, 30, 60, 'bd-t-head', 'the permanent platform');
  text(perm, 30, 78, 'bd-t-small', 'scenario (b) — where the data lives');

  label(perm, 30, 104, 'one database per tenant');
  const tenants = ['tenant A', 'tenant B', 'tenant C'];
  tenants.forEach((name, n) => {
    const x = 30 + n * 172;
    const g = box(perm, x, 114, 160, 74, 'bd-tenant');
    text(g, x + 12, 134, 'bd-t-title', name);
    // ADR-0005: venues inside a tenant are list partitions on venue_id, and
    // database-per-venue was rejected — five cross-venue features become
    // distributed transactions. Drawn as ticks inside the one box, because
    // three boxes here would be the rejected design.
    for (let k = 0; k < 4; k += 1) {
      g.append(svgEl('rect', {
        x: x + 12 + k * 26, y: 146, width: 20, height: 12, rx: 2, class: 'bd-part',
      }));
    }
    text(g, x + 12, 176, 'bd-t-tiny', 'venues: partitions on venue_id');
  });

  label(perm, 30, 212, 'one cell: a primary, a pooler, and the shared tier');
  const permPg = box(perm, 30, 222, 232, 62, 'bd-pg');
  text(permPg, 42, 244, 'bd-t-title', 'postgres primary');
  text(permPg, 42, 264, 'bd-t-small',
    permanent?.services?.postgres
      ? `max_connections ${pgFlag(permanent.services.postgres.command, 'max_connections') ?? '—'}`
      : 'the transaction store');
  const permPool = box(perm, 274, 222, 228, 62, 'bd-pool-flat');
  text(permPool, 286, 244, 'bd-t-title', 'pgbouncer');
  text(permPool, 286, 264, 'bd-t-small',
    permanent?.services?.pgbouncer
      ? `${permanent.services.pgbouncer.environment?.MAX_CLIENT_CONN ?? '—'} clients → `
        + `${permanent.services.pgbouncer.environment?.DEFAULT_POOL_SIZE ?? '—'}`
      : 'transaction pooling');

  // The three that are not the transaction store. Drawn apart because they are
  // apart: a replica you may not write to, a vector store with no database
  // above its collections, and an append-only record.
  label(perm, 30, 312, 'not the transaction store, and not interchangeable with it');
  const aside = [
    {
      x: 30, w: 152, cls: 'bd-reporting', title: 'reporting replica',
      lines: ['analytical · minutes', 'never the primary', 'in-cell, in-region'],
      tip: 'ADR-0016. Analytical reads are served from the replica and cannot fall back to '
        + 'the primary even when it is unavailable — they fail with a lag error instead. '
        + 'Cross-cell reporting comes from the central warehouse, because no cell may read '
        + 'another for reporting: that is data residency, not performance.',
    },
    {
      x: 194, w: 152, cls: 'bd-qdrant', title: 'qdrant',
      lines: ['one collection per', 'embedding model', 'one shard per tenant'],
      tip: 'ADR-0021. A collection is Qdrant’s only top-level container and each one holds '
        + 'a single vector configuration, so the split is by embedding model and nothing else. '
        + 'Tenant is the shard key on every placement, so a tenant moving between placements '
        + 'does not reshape the store.',
    },
    {
      x: 358, w: 144, cls: 'bd-audit', title: 'audit',
      lines: ['platform.audit_record', 'platform.audit_read', 'identity.authz_audit'],
      tip: 'Append-only. A failed financial posting is an incident rather than a queue item '
        + '(ADR-0033), and the read log exists because who looked is itself a fact somebody '
        + 'has to be able to answer for.',
    },
  ];
  for (const item of aside) {
    const g = box(perm, item.x, 322, item.w, 96, item.cls);
    text(g, item.x + 12, 344, 'bd-t-title', item.title);
    item.lines.forEach((line, k) => text(g, item.x + 12, 366 + k * 16, 'bd-t-tiny', line));
    const tip = svgEl('title');
    tip.textContent = item.tip;
    g.append(tip);
  }

  label(perm, 30, 444, 'the shared tier, and the venue services that sit at the venue');
  const permServices = Object.keys(permanent?.services ?? {})
    .filter((n) => /service/i.test(n));
  const shared = permServices.filter((n) => !/-v\d+$/.test(n));
  const venue = [...new Set(permServices.filter((n) => /-v\d+$/.test(n))
    .map((n) => n.replace(/-v\d+$/, '')))];
  let cx = 30;
  let cy = 456;
  const chip = (name, cls) => {
    const w = Math.max(46, name.length * 5.6 + 14);
    if (cx + w > 508) { cx = 30; cy += 22; }
    const g = svgEl('g', { class: `bd-chip ${cls}` });
    g.append(svgEl('rect', { x: cx, y: cy, width: w, height: 17, rx: 4 }));
    text(g, cx + w / 2, cy + 12, 'bd-t-tiny bd-t-mid', name);
    perm.append(g);
    cx += w + 5;
  };
  for (const name of shared) chip(name.replace(/service$/i, ''), 'bd-chip-shared');
  for (const name of venue) chip(`${name.replace(/service$/i, '')} ×3`, 'bd-chip-venue');
  if (!permServices.length) text(perm, 30, 468, 'bd-t-tiny', `${PERMANENT} not readable`);

  // ── right: the burst environment ──────────────────────────────────────────
  const bx = 596;
  const burstG = svgEl('g', { class: 'bd-burst' });
  bodies.append(burstG);
  burstG.append(svgEl('rect', {
    x: bx, y: 36, width: W - bx - 14, height: 480, rx: 12, class: 'bd-frame bd-frame-burst',
  }));
  text(burstG, bx + 16, 60, 'bd-t-head', 'the burst environment');
  text(burstG, bx + 16, 78, 'bd-t-small', 'scenario (c) — where data passes through');

  const ingress = svgEl('g', { class: 'bd-node bd-ingress' });
  ingress.append(svgEl('rect', { x: bx + 16, y: 96, width: 118, height: 58, rx: 9 }));
  text(ingress, bx + 75, 120, 'bd-t-title bd-t-mid', 'buyers');
  text(ingress, bx + 75, 138, 'bd-t-tiny bd-t-mid', 'one event, one moment');
  burstG.append(ingress);

  const clusters = t.deployed.map((service, n) => {
    const rows = Math.ceil(service.max / PER_ROW);
    const y = 174 + n * 112;
    const x = bx + 16;
    const w = 320;
    const h = 42 + rows * (CELL + CELL_GAP);
    const g = box(burstG, x, y, w, h, 'bd-cluster');
    text(g, x + 12, y + 22, 'bd-t-title', service.short);
    text(g, x + w - 12, y + 22, 'bd-t-tiny', `${service.share}%`).setAttribute('text-anchor', 'end');
    const count = text(g, x + 12, y + 38, 'bd-t-tiny', '');
    const cells = [];
    for (let k = 0; k < service.max; k += 1) {
      const cell = svgEl('rect', {
        x: x + 12 + (k % PER_ROW) * (CELL + CELL_GAP),
        y: y + 46 + Math.floor(k / PER_ROW) * (CELL + CELL_GAP),
        width: CELL, height: CELL, rx: 3, class: 'bd-cell',
      });
      cells.push(cell);
      g.append(cell);
    }
    return { service, x, y, w, h, cells, count, node: g };
  });

  const poolX = bx + 366;
  const poolY = 250;
  const pool = svgEl('g', { class: 'bd-node bd-pool' });
  pool.append(svgEl('path', {
    d: `M ${poolX} ${poolY - 74} L ${poolX + 92} ${poolY - 26}`
      + ` L ${poolX + 92} ${poolY + 26} L ${poolX} ${poolY + 74} Z`,
  }));
  text(pool, poolX + 34, poolY - 2, 'bd-t-title bd-t-mid', 'pgbouncer');
  text(pool, poolX + 34, poolY + 16, 'bd-t-tiny bd-t-mid', t.bouncer?.mode ?? '');
  burstG.append(pool);

  const hotG = box(burstG, bx + 366, 340, 190, 92, 'bd-pg');
  text(hotG, bx + 380, 362, 'bd-t-title', 'postgres-hot');
  [`max_connections ${t.postgres?.maxConnections ?? '—'}`,
    `${t.postgres?.cpus ?? '—'} cpu · ${t.postgres?.memory ?? '—'}`,
    t.postgres?.synchronousCommit === 'off' ? 'synchronous_commit off' : '']
    .filter(Boolean)
    .forEach((line, k) => text(hotG, bx + 380, 384 + k * 16, 'bd-t-tiny', line));

  const redisG = box(burstG, bx + 366, 444, 190, 56, 'bd-redis');
  text(redisG, bx + 380, 466, 'bd-t-title', 'redis');
  text(redisG, bx + 380, 486, 'bd-t-tiny', `${t.redis?.cpus ?? '—'} cpu · ${t.redis?.memory ?? '—'}`);

  // flows inside the burst
  const flow = [];
  const addEdge = (d, weight, cls) => {
    const path = svgEl('path', { d, class: `bd-edge ${cls ?? ''}` });
    edges.append(path);
    flow.push({ path, weight });
    return path;
  };
  for (const c of clusters) {
    const midY = c.y + c.h / 2;
    addEdge(`M ${bx + 134} 125 C ${bx + 150} 125, ${bx + 150} ${midY}, ${c.x} ${midY}`,
      c.service.share);
    addEdge(`M ${c.x + c.w} ${midY} C ${c.x + c.w + 20} ${midY},`
      + ` ${poolX - 24} ${poolY}, ${poolX + 2} ${poolY}`, c.service.share);
  }
  addEdge(`M ${poolX + 92} ${poolY} L ${bx + 366} 386`, 100);
  addEdge(`M ${poolX + 92} ${poolY} L ${bx + 366} 472`, 20);

  // ── the merge back ────────────────────────────────────────────────────────
  // Drawn as its own lane under both panels, because it is the one edge that
  // joins them and the reason the environment cannot simply be switched off.
  const mergePath = svgEl('path', {
    d: `M ${bx + 40} 528 C ${bx - 60} 600, 300 600, 148 546`,
    class: 'bd-merge',
  });
  edges.append(mergePath);
  const mergeLabel = text(bodies, 470, 596, 'bd-t-merge',
    'reconcile — environment id, monotonic sequence, idempotent replay');
  mergeLabel.setAttribute('text-anchor', 'middle');

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
    // `details` and not `box`: there is an SVG `box()` helper in this scope and
    // shadowing it here would read as a call to it.
    const details = el('details', 'bd-note');
    details.append(el('summary', null, `Why this scenario exists — the header of ${COMPOSE}`));
    details.append(el('pre', 'bd-note-body', note));
    section.append(details);
  }

  // ── the result of the run ─────────────────────────────────────────────────
  // Hidden until a run finishes, and cleared by a scrub, because a number
  // sitting under a diagram somebody dragged is a number about nothing.
  const result = el('div', 'bd-panel bd-result');
  result.hidden = true;
  section.append(result);

  const showResult = () => {
    result.replaceChildren();
    result.hidden = false;
    result.append(el('h3', 'bd-risk-h', 'The run'));

    const facts = el('div', 'bd-thr-list');
    const fact = (name, value, note) => {
      const row = el('div', 'bd-thr-row');
      row.append(el('span', 'bd-thr-n', name));
      row.append(el('span', 'bd-thr-v', value));
      row.append(el('span', 'bd-thr-note', note));
      facts.append(row);
    };
    fact('simulated', clock(simMinutes),
      `${phases.length} phases, ${Math.round(totalMinutes)} minutes of sale time`);
    fact('target utilisation', `${Math.round(threshold * 100)}%`,
      everCapped
        ? 'the file could not always provide enough replicas to hold it — utilisation '
          + 'ran above target and ADR-0032 sheds rather than queues'
        : 'held throughout, within the replica ceiling the compose file sets');
    fact('peak containers', String(peakContainers),
      `of ${t.deployed.reduce((a, x) => a + x.max, 0)} the file allows`);
    fact('peak connections', peakClient.toLocaleString('en-GB'),
      t.bouncer
        ? `against MAX_CLIENT_CONN ${t.bouncer.maxClient.toLocaleString('en-GB')}, `
          + `answered from ${t.bouncer.poolSize} server connections`
        : 'no pooler in the file');
    fact('resources', `${cpuHours.toFixed(1)} cpu-h · ${gbHours.toFixed(0)} GB-h`,
      'integrated across the run, which is what the prices below are applied to');
    fact('at the ADR rate', money(spent),
      `${money(RATE_PER_HOUR)} an hour at full expansion, apportioned by cpu`);
    result.append(facts);

    result.append(el('p', 'bd-result-h', 'The same run, priced at list container compute'));
    const grid = el('div', 'bd-prices');
    for (const provider of PROVIDERS) {
      const cost2 = cpuHours * provider.vcpu + gbHours * provider.gb;
      const card = el('div', `bd-price bd-price-${provider.key}`);
      card.append(el('div', 'bd-price-v', money(cost2)));
      card.append(el('div', 'bd-price-n', provider.name));
      card.append(el('div', 'bd-price-h',
        `$${provider.vcpu.toFixed(5)}/vCPU-h · $${provider.gb.toFixed(6)}/GB-h · ${provider.region}`));
      if (provider.key === 'gcp') card.append(el('div', 'bd-price-tag', 'not on the shortlist'));
      if (provider.key !== 'gcp') card.append(el('div', 'bd-price-tag', 'CF-64 candidate'));
      grid.append(card);
    }
    result.append(grid);

    result.append(el('p', 'bd-open',
      'CF-64 is open: the cloud provider is AWS or Azure, pending DESC, owned by Dinesh '
      + 'and Qossai. GCP is priced here because it was asked for and it is not one of the '
      + 'two. Everything in the package above that decision is provider-neutral, and as '
      + 'the brief puts it nothing below it can be — managed Postgres, the Redis tier, '
      + 'Qdrant hosting, the CDN and the secret store all follow from the choice. CF-64 '
      + 'also carries the RPO and RTO targets, which are stated nowhere else.'));
    result.append(el('p', 'bd-risk-n',
      'These three rates are mine and not the package’s, and they price container '
      + 'compute only — no managed-database premium, no storage, no IO, no egress, no '
      + 'support plan. That is most of why they land under ADR-0035’s own figure for '
      + 'the same environment, and it is why they are a sanity check on the order of '
      + 'magnitude rather than a quote. Check them before they go in front of a client.'));
  };

  // ── the animation ─────────────────────────────────────────────────────────
  const stillness = window.matchMedia('(prefers-reduced-motion: reduce)');
  const replayAt = phases.findIndex((x) => lookOf(x.name).replay);

  // Cost is apportioned by cpu, so the weights come off the compose file. A
  // container with no declared limit weighs nothing and says so rather than
  // being guessed at — pgbouncer declares none in this file.
  const baseCpu = num(t.postgres?.cpus) + num(t.redis?.cpus);
  const baseGb = gigs(t.postgres?.memory) + gigs(t.redis?.memory);
  const peakCpu = baseCpu
    + t.deployed.reduce((a, s) => a + num(s.cpus) * s.max, 0);
  const perCpuHour = peakCpu > 0 ? RATE_PER_HOUR / peakCpu : 0;

  // How long the whole run represents. The lifecycle is not two hours of
  // wall-clock in equal parts — provisioning takes minutes and the sale takes
  // seconds — so each phase carries its own share of the simulated clock.
  const PHASE_MINUTES = {
    requested: 0, provisioning: 8, warming: 6, live: 120,
    draining: 15, reconciling: 20, reconciled: 2, decommissioned: 0,
  };
  const minutesOf = (name) => PHASE_MINUTES[name] ?? 10;
  const totalMinutes = phases.reduce((a, x) => a + minutesOf(x.name), 0) || 120;

  let p = 0;
  let playing = false;
  let last = 0;
  let spent = 0;
  let simMinutes = 0;
  let threshold = 0.7;
  // Integrated once and priced three ways at the end. Pricing per frame would
  // tie the answer to the frame rate.
  let cpuHours = 0;
  let gbHours = 0;
  let peakContainers = 0;
  let peakClient = 0;
  let everCapped = false;

  const phaseAt = (u) => {
    if (!hasPhases) return { index: 0, name: 'live', within: u };
    const span = 1 / phases.length;
    const index = Math.min(phases.length - 1, Math.floor(u / span));
    return { index, name: phases[index].name, within: Math.min(1, (u - index * span) / span) };
  };

  /**
   * How many replicas a cluster runs at this demand and this threshold.
   *
   * Capacity per replica is taken as peak ÷ max, because `max` is what the
   * compose file provisions for the peak. Holding utilisation at or under the
   * threshold then needs demand × max ÷ threshold replicas — which is why a
   * lower threshold buys headroom and costs money, and why at a low enough one
   * the answer exceeds what the file allows. That case is drawn rather than
   * clamped away silently.
   */
  const wantedFor = (service, demand) => Math.ceil((demand * service.max) / threshold);

  const apply = () => {
    const at = phaseAt(p);
    const look = lookOf(at.name);
    const demand = look.load === 'ramp' ? at.within : Number(look.load) || 0;
    const running = look.infra > 0 && demand > 0;

    let replicas = 0;
    let client = 0;
    let liveCpu = look.infra > 0 ? baseCpu : 0;
    const short = [];

    for (const c of clusters) {
      const want = running ? Math.max(c.service.min, wantedFor(c.service, demand)) : 0;
      const n = Math.min(c.service.max, want);
      if (want > c.service.max) short.push(`${c.service.short} wants ${want}`);
      replicas += n;
      client += n * c.service.poolMax;
      liveCpu += num(c.service.cpus) * n;
      c.cells.forEach((cell, k) => cell.classList.toggle('on', k < n));
      c.count.textContent = running
        ? `${n} of ${c.service.max}${want > c.service.max ? ` · wants ${want}` : ''}`
          + (c.service.poolMax ? ` · ${n * c.service.poolMax} conns` : '')
        : 'not running';
      c.node.classList.toggle('bd-quiet', !running);
      c.node.classList.toggle('bd-capped', want > c.service.max);
    }

    // The honest consequence of a low threshold, said rather than hidden: the
    // compose file caps replicas, so below some target the environment simply
    // cannot hold utilisation there.
    peakContainers = Math.max(peakContainers, replicas);
    peakClient = Math.max(peakClient, client);
    if (short.length && running) {
      everCapped = true;
      capped.hidden = false;
      capped.textContent = `At ${Math.round(threshold * 100)}% the file does not allow enough `
        + `replicas — ${short.join(', ')}. deploy/c-flash-sale.yml caps them, so utilisation `
        + 'runs above the target rather than more containers appearing.';
    } else {
      capped.hidden = true;
    }

    const server = t.bouncer?.poolSize ?? 0;
    outReplicas.textContent = String(replicas);
    outClient.textContent = client ? client.toLocaleString('en-GB') : '—';
    outRatio.textContent = server && client ? `${(client / server).toFixed(1)} : 1` : '—';
    const over = t.bouncer?.maxClient ? client > t.bouncer.maxClient : false;
    outClient.classList.toggle('bd-over', over);
    if (poolRow) poolRow.classList.toggle('bd-thr-hot', over);

    const rate = look.billing ? liveCpu * perCpuHour : 0;
    outRate.textContent = rate ? `${money(rate)}/h` : '—';
    outSpend.textContent = money(spent);
    outClockV.textContent = clock(simMinutes);

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

    const writing = demand > 0.2;
    wp.classList.toggle('bd-idle', !writing);
    if (!stillness.matches && writing) {
      wdot.setAttribute('cx', String(28 + ((performance.now() / 2600) % 1) * 870));
      wdot.setAttribute('opacity', '1');
    } else {
      wdot.setAttribute('opacity', '0');
    }

    // the merge lane lights only while it is actually happening
    mergePath.classList.toggle('bd-merge-on', Boolean(look.replay));
    mergeLabel.classList.toggle('bd-merge-on', Boolean(look.replay));

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
        f.path.style.strokeOpacity = String(0.1 + 0.5 * demand);
        f.path.style.strokeDashoffset =
          String(-((now / (24 - 16 * demand)) * (0.2 + f.weight / 100)) % 1000);
      }
    }
  };

  const seek = (v) => {
    playing = false;
    play.textContent = hasPhases ? 'Run the sale' : 'Expand';
    p = Math.max(0, Math.min(1, v));
    range.value = String(Math.round(p * 1000));
    // Scrubbing is not spending. The clock and the meter follow the position
    // rather than accumulating, or dragging back and forth would run the bill
    // up without any of it having happened.
    simMinutes = 0;
    spent = 0;
    cpuHours = 0;
    gbHours = 0;
    result.hidden = true;
    const at = phaseAt(p);
    for (let n = 0; n < at.index; n += 1) simMinutes += minutesOf(phases[n]?.name);
    simMinutes += minutesOf(at.name) * at.within;
  };

  const frame = (now) => {
    const dt = last ? Math.min(64, now - last) : 16;
    last = now;
    if (playing) {
      // One second of yours is a minute of the sale.
      const step = dt / 1000;
      simMinutes += step;
      p = Math.min(1, simMinutes / totalMinutes);
      range.value = String(Math.round(p * 1000));
      const look = lookOf(phaseAt(p).name);
      if (look.billing) {
        const at = phaseAt(p);
        const demand = look.load === 'ramp' ? at.within : Number(look.load) || 0;
        let cpu = look.infra > 0 ? baseCpu : 0;
        let gb = look.infra > 0 ? baseGb : 0;
        for (const c of clusters) {
          if (look.infra > 0 && demand > 0) {
            const n = Math.min(c.service.max,
              Math.max(c.service.min, wantedFor(c.service, demand)));
            cpu += num(c.service.cpus) * n;
            gb += gigs(c.service.memory) * n;
          }
        }
        const hours = step / 60;
        spent += cpu * perCpuHour * hours;
        cpuHours += cpu * hours;
        gbHours += gb * hours;
      }
      if (p >= 1) { playing = false; play.textContent = 'Again'; showResult(); }
    }
    apply();
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  play.onclick = () => {
    if (p >= 1) {
      p = 0; simMinutes = 0; spent = 0; range.value = '0';
      cpuHours = 0; gbHours = 0; peakContainers = 0; peakClient = 0; everCapped = false;
      result.hidden = true;
    }
    playing = !playing;
    play.textContent = playing ? 'Pause' : (hasPhases ? 'Run the sale' : 'Expand');
  };
  range.oninput = () => { seek(Number(range.value) / 1000); };
  thrRange.oninput = () => {
    threshold = Number(thrRange.value) / 100;
    thrLabel.textContent = `${thrRange.value}%`;
  };

  // ── the cost ladder ───────────────────────────────────────────────────────
  const cost = el('div', 'bd-panel bd-cost');
  cost.append(el('h3', 'bd-risk-h', 'What it costs, and why teardown is wired to the calendar'));
  cost.append(el('p', 'bd-risk-p',
    'ADR-0035 prices the environment at four durations. The risk it names is not the '
    + 'cost but forgetting: a month of forgetting costs more than the platform the '
    + 'environment was protecting, which is why teardown is tied to '
    + 'catalogue.performance.onSaleTo rather than to somebody’s calendar, and why '
    + 'listBurstEnvironments exists at all — an environment nobody is looking at is '
    + 'the one left running for a month.'));
  const ladder = el('div', 'bd-thr-list');
  for (const point of COST_POINTS) {
    const row = el('div', 'bd-thr-row');
    row.append(el('span', 'bd-thr-n', point.label));
    row.append(el('span', 'bd-thr-v', money(point.usd)));
    row.append(el('span', 'bd-thr-note',
      `${point.hours} hour${point.hours === 1 ? '' : 's'} · `
      + `${money(point.usd / point.hours)} an hour at full expansion`));
    ladder.append(row);
  }
  cost.append(ladder);
  cost.append(el('p', 'bd-risk-n',
    `The four totals are the ADR’s, quoted. The meter above is anchored on the month `
    + `figure — ${money(RATE_PER_HOUR)} an hour, the longest run of the four and so the `
    + 'least sensitive to rounding — and split across containers by the cpu limits the '
    + `compose file declares: ${peakCpu} cpu fully expanded, ${baseCpu} for the database `
    + 'and cache alone. That split is a model, not a quote. pgbouncer declares no cpu '
    + 'limit in this file and so weighs nothing in it.'));
  section.append(cost);

  head.append(el('p', 'bd-sub bd-sub-fine',
    `${t.deployed.reduce((a, x) => a + x.min, 0)} containers at rest, `
    + `${t.deployed.reduce((a, x) => a + x.max, 0)} fully expanded. `
    + (hasPhases
      ? `${phases.length} phases, walked from states/burst-environment.yaml — the line `
        + 'under the strip is the package’s own guard for that step. '
      : '')
    + 'The requests-per-second figures the scenario quotes are prose in the compose '
    + 'header, not structured data, so they are shown there rather than animated here.'));
}
