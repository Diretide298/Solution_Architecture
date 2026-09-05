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
// What one replica sustains, what share of the load each service carries, and
// the utilisation the platform sizes against. The package computes replicas
// rather than stating them.
const SIZING = 'handoff/sizing.json';

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
function topology(burst, compose, sizing, loadCeilingRps) {
  const services = compose?.services ?? {};
  const byCompose = new Map(Object.entries(services));
  // orderservice ← OrderService. The compose keys are lowercased service names.
  const composeFor = (name) => byCompose.get(String(name).toLowerCase()) ?? null;

  const deployed = (burst.services ?? [])
    .filter((s) => s.deployed)
    .map((s) => {
      const spec = composeFor(s.name);
      const min = num(s.replicas?.min, 1);
      // **`max: null` means no ceiling, and the package says so in as many
      // words**: "a cap is a cap on absorbing a peak nobody predicted, and the
      // peak is the whole reason this environment exists". So a missing max is
      // not a missing number to fill in from compose — compose's fixed
      // `replicas:` is one deployment's answer, and treating it as the ceiling
      // drew a wall the package had deliberately removed.
      //
      // A drawing still needs somewhere to stop, so `drawTo` is how many boxes
      // to lay out and `capped` says whether that is a real limit or just the
      // edge of the picture.
      const stated = s.replicas?.max;
      const uncapped = stated == null;

      // **What the calculator says, per service.** derive-sizing.py sizes
      // against the target rather than the cliff — one replica is treated as
      // carrying 60% of what it can, so the headroom a scale-out needs exists
      // before the scale-out starts. Each service has its own cliff: 400 RPS
      // for Catalogue, 250 for Order, 600 for Identity.
      const calc = sizing?.services?.[s.name] ?? null;
      const perReplica = num(calc?.rpsPerReplica, 400);
      const shareOfLoad = num(calc?.share, num(s.weightedShare));
      const target = num(calc?.targetUtilisation, 0.6);
      const absoluteMin = num(s.replicas?.absoluteMin, num(calc?.floor, min));

      // With no ceiling there is nothing to draw up to, so the picture is laid
      // out for the most the load control can ask for. The boxes then never
      // run out and never imply a cap that is not there.
      const atCeiling = perReplica > 0
        ? Math.ceil((loadCeilingRps * shareOfLoad / 100) / (perReplica * target))
        : min;
      const drawTo = uncapped
        ? Math.max(min, absoluteMin, atCeiling)
        : num(stated, min);
      return {
        name: s.name,
        short: s.name.replace(/Service$/, ''),
        tier: s.tier,
        share: num(s.weightedShare),
        reason: s.reason ?? '',
        min,
        max: drawTo,
        uncapped,
        perReplica,
        shareOfLoad,
        target,
        absoluteMin,
        scaleOutAt: num(calc?.scaleOutAt, Math.round(perReplica * target)),
        drivenBy: calc?.drivenBy ?? null,
        // What the compose file actually provisions. The cost the package
        // quotes is for the environment as configured, so that is the size the
        // hourly rate has to land on.
        specReplicas: num(spec?.deploy?.replicas, min),
        maxNote: s.replicas?.maxNote ?? null,
        derivedFrom: s.replicas?.derivedFrom ?? null,
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
// **$11.76, stated, not derived.** handoff/TICVAI_Hosting_Summary.docx prices
// the four hosting options on Amazon and Google side by side, and option 3 —
// the big sale, billed by the hour while it runs — is $11.76 an hour on Amazon.
//
// This was 8587/720 and gave $11.93. The month figure is the same document's
// Amazon column and it divides by 730, the billing month, not 720: 8587/730 is
// $11.76 exactly, and the two-, six- and twenty-four-hour figures all fall out
// of it. Deriving a rate from a total when the rate is stated one row above it
// is how a viewer ends up 1.4% away from its own source.
const RATE_PER_HOUR = 11.76;

/** `32G` -> 32, `512M` -> 0.5. Compose states memory as a limit string. */
const gigs = (value) => {
  const hit = String(value ?? '').match(/^([\d.]+)\s*([GMK])?/i);
  if (!hit) return 0;
  const n = Number(hit[1]);
  const unit = (hit[2] ?? 'G').toUpperCase();
  return unit === 'M' ? n / 1024 : unit === 'K' ? n / 1048576 : n;
};

/**
 * What the package charges for a burst environment, by the hour.
 *
 * **Stated, not estimated.** `handoff/TICVAI_Hosting_Summary.docx` prices all
 * four hosting options on Amazon and Google side by side — the header row is
 * `Option | Billed as | Amazon | Google` — and option 3, the big sale, is
 * billed by the hour while it runs.
 *
 * An earlier version of this file asserted that the package held no provider
 * figures because CF-64 is open, and invented three sets of container-compute
 * list rates instead. It holds both, they disagree with the invented ones in
 * both magnitude and direction, and the document says why: Google comes out
 * 15–18% cheaper *"mostly on database pricing"*, which is exactly what a
 * compute-only estimate leaves out.
 *
 * **The two documents do not name the same shortlist.** CF-64 in the
 * deployment brief reads *AWS or Azure, pending DESC*; the Hosting Summary
 * prices Amazon and Google and prices no Azure at all. That contradiction is
 * shown on the page rather than resolved here.
 */
const PROVIDERS = [
  { key: 'aws', name: 'Amazon', hourly: 11.76, month: 8587 },
  { key: 'gcp', name: 'Google', hourly: 9.76, month: null },
];

/**
 * Indicative list rates for serverless container compute, per vCPU-hour and
 * per GB-hour. **A cross-check on the figures above, and not a substitute.**
 *
 * These are mine. They price container compute only — no managed-database
 * premium, no storage, no IO, no egress — which is why they come out under the
 * package's own numbers, and the Hosting Summary says the gap between the two
 * providers is *"mostly on database pricing"*, exactly the part these miss. So
 * they answer one question: how much of the bill is compute.
 */
const COMPUTE_RATES = [
  { key: 'aws', vcpu: 0.04048, gb: 0.004445 },
  { key: 'gcp', vcpu: 0.0456, gb: 0.0050 },
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

  // **The sizing calculator, which is the package's answer to how many.**
  // tools/refresh.sh runs derive-sizing.py --apply at step 14, so this is a
  // normal artefact and not something this page derives. Without it the page
  // falls back to the floors burst-scope states, which is a snapshot of one
  // load rather than a function of load.
  let sizing = null;
  try { sizing = JSON.parse(await io.file(SIZING))?.sale ?? null; } catch { sizing = null; }

  // 55 requests per buyer, summed from callsPerBuyer across the 34 burst
  // operations — the package's own figure, not a ratio invented here.
  const CALLS_PER_BUYER = (burst.operations ?? [])
    .reduce((a, op) => a + num(op.callsPerBuyer), 0) || 1;
  // ADR-0035: "At 5,000 RPS the entire daily volume arrives in fifty seconds."
  const PEAK_RPS = 5000;
  const PEAK_BUYERS = Math.round(PEAK_RPS / CALLS_PER_BUYER);
  const MAX_BUYERS = PEAK_BUYERS * 2;
  // One second of yours is a minute of the sale.
  const SIM_PER_REAL = 60;

  const t = topology(burst, compose, sizing, MAX_BUYERS * CALLS_PER_BUYER);
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

  // The walk that built a fixed happy path is gone: nothing runs on a
  // timeline any more, so the transitions are read where they are needed —
  // `trigger: operation` becomes a button, `system` and `time` fire on their
  // own — and the order comes out of the model rather than out of a list.

  // ── controls ──────────────────────────────────────────────────────────────
  //
  // **The operations are the buttons, taken from the machine.** Four of the
  // twelve transitions carry `trigger: operation` and name the operation that
  // causes them; the rest are `system` or `time` and happen on their own. So
  // the controls are not a menu somebody wrote — they are the transitions the
  // model says a person causes, enabled exactly when their `from` is the state
  // the environment is in.
  //
  // Nothing here scrubs. Time runs forward once the environment is requested,
  // and what the reader controls is the load: everything else is a consequence.

  const opTransitions = (machine?.transitions ?? []).filter((tr) => tr.trigger === 'operation');
  const byOperation = new Map();
  for (const tr of opTransitions) {
    if (!byOperation.has(tr.operation)) byOperation.set(tr.operation, []);
    byOperation.get(tr.operation).push(tr);
  }

  // What each operation is for, in the words somebody would use for it. The
  // operationId is kept underneath rather than replaced: it is the package's
  // name and the thing to search for, but on its own — lowercased and stripped
  // of its suffix — it was too quiet to read as the button that starts
  // everything.
  const OP_LABEL = {
    requestBurstEnvironment: 'Stand the environment up',
    drainBurstEnvironment: 'Close the sale',
    reconcileBurstEnvironment: 'Merge back',
    decommissionBurstEnvironment: 'Tear it down',
  };
  const opBar = el('div', 'bd-ops');
  const opButtons = [...byOperation.entries()].map(([operation, list]) => {
    const node = el('button', 'bd-op');
    node.type = 'button';
    node.append(el('span', 'bd-op-t', OP_LABEL[operation] ?? operation));
    node.append(el('span', 'bd-op-id', operation));
    node.title = stripEmphasis(list[0]?.guard ?? operation);
    node.onclick = () => fire(operation);
    opBar.append(node);
    return { operation, list, node };
  });
  section.append(opBar);

  const stateLine = el('p', 'bd-state');
  section.append(stateLine);

  // What the model says no to. Shown rather than swallowed: the 409 on
  // decommission is the edge ADR-0035 exists for, and a button that quietly
  // does nothing teaches the opposite of what the ADR decided.
  const refused = el('p', 'bd-refused');
  refused.hidden = true;
  section.append(refused);

  const guard = el('p', 'bd-guard');
  section.append(guard);

  // The load. **Buyers and not requests**, because a buyer is what the scenario
  // counts and the request rate follows from it: 55 calls each, summed from the
  // package's own callsPerBuyer. Estimated rather than measured — tools/bench.py
  // replaces them when there is something to run it against — so the slider is
  // labelled in the unit the estimate is expressed in.
  const loadBar = el('div', 'bd-bar bd-bar-load');
  const loadRange = document.createElement('input');
  loadRange.type = 'range';
  loadRange.className = 'bd-range';
  loadRange.min = '0';
  loadRange.max = String(MAX_BUYERS);
  loadRange.value = '0';
  loadRange.setAttribute('aria-label', 'Buyers arriving per second');
  const loadLabel = el('span', 'bd-thr-live', '0/s');
  loadBar.append(
    el('span', 'bd-bar-label', 'buyers arriving'),
    el('div', 'bd-slide', loadRange),
    loadLabel,
    el('span', 'bd-bar-note bd-load-note', ''),
  );
  const loadNote = loadBar.querySelector('.bd-load-note');
  section.append(loadBar);

  // **Target utilisation, and it is the package's.** derive-sizing.py sets it
  // at 0.60 and says why: one replica is treated as carrying 60% of what it
  // can, so the headroom a scale-out needs exists before the scale-out starts.
  //
  // An earlier version of this control was labelled as the reader's own
  // invention, on the grounds that nothing in the package named a number. That
  // was true of burst-scope and of the compose headers and not true of the
  // calculator, which had simply never been generated in the dump on hand.
  // It moves, because seeing what a different target costs is the point of
  // having it on a slider, but it starts where the package puts it.
  const thrBar = el('div', 'bd-bar bd-bar-thr');
  const thrRange = document.createElement('input');
  thrRange.type = 'range';
  thrRange.className = 'bd-range';
  thrRange.min = '40';
  thrRange.max = '100';
  thrRange.value = String(Math.round((t.deployed[0]?.target ?? 0.6) * 100));
  thrRange.setAttribute('aria-label', 'Target utilisation per replica');
  const thrLabel = el('span', 'bd-thr-live', `${thrRange.value}%`);
  thrBar.append(
    el('span', 'bd-bar-label', 'size each replica to'),
    el('div', 'bd-slide', thrRange),
    thrLabel,
    el('span', 'bd-bar-note bd-target-note', ''),
  );
  section.append(thrBar);

  // ADR-0035's open question, made operable. The catalogue is a snapshot rather
  // than a replica, so a price that moves during the sale has to be resolved at
  // reconciliation — and `priceDivergencePolicy` names three answers with no
  // default, deliberately, because somebody chooses per sale. Both controls
  // start at the position that asks nothing: no divergence, honour what the
  // guest saw.
  const divBar = el('div', 'bd-bar bd-bar-div');
  const divRange = document.createElement('input');
  divRange.type = 'range';
  divRange.className = 'bd-range';
  divRange.min = '0';
  divRange.max = '100';
  divRange.value = '0';
  divRange.setAttribute('aria-label', 'Share of orders taken at a price that later changed');
  const divLabel = el('span', 'bd-thr-live', '0%');
  const policy = document.createElement('select');
  policy.className = 'bd-policy';
  for (const [value, text2] of [
    ['honourSnapshot', 'honourSnapshot'],
    ['honourCurrent', 'honourCurrent'],
    ['reject', 'reject'],
  ]) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text2;
    policy.append(option);
  }
  divBar.append(
    el('span', 'bd-bar-label', 'price moved for'),
    el('div', 'bd-slide', divRange),
    divLabel,
    policy,
    el('span', 'bd-bar-note bd-policy-note', ''),
  );
  const targetNote = thrBar.querySelector('.bd-target-note');
  const policyNote = divBar.querySelector('.bd-policy-note');
  section.append(divBar);

  // ── readouts ──────────────────────────────────────────────────────────────
  const reads = el('div', 'bd-reads');
  const readout = (label2, hint, cls) => {
    const cell = el('div', `bd-read ${cls ?? ''}`);
    const v = el('div', 'bd-read-v', '—');
    cell.append(v, el('div', 'bd-read-l', label2));
    if (hint) cell.append(el('div', 'bd-read-h', hint));
    reads.append(cell);
    return v;
  };
  const outClockV = readout('elapsed', 'a second of yours is a minute of the sale');
  const outRps = readout('requests a second', `${CALLS_PER_BUYER} per buyer, from the package`);
  const outOrders = readout('orders taken', 'what reconciliation has to move');
  const outReplicas = readout('containers running', 'scaling up and down with the load');
  const outSpend = readout('spent so far', 'apportioned by cpu limits', 'bd-read-cost');
  const outRate = readout('burn rate', 'per hour at this size');
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
    // 168 wide and not 160: the caption underneath ran past the edge of the
    // box at the narrower size, which read as a clipping bug rather than as a
    // caption.
    const x = 30 + n * 174;
    const g = box(perm, x, 114, 168, 74, 'bd-tenant');
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
    text(g, x + 12, 176, 'bd-t-tiny', 'venues: partitions, not databases');
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
  // Orders in flight along it. Six is enough to read as movement and few
  // enough that the lane does not turn into a solid line.
  const mergeLen = mergePath.getTotalLength ? mergePath.getTotalLength() : 0;
  const mergeDots = Array.from({ length: 6 }, () => {
    const dot = svgEl('circle', { r: 3.5, cx: -10, cy: -10, class: 'bd-mergedot', opacity: '0' });
    bodies.append(dot);
    return dot;
  });

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
  // **Read the flag, do not assert it.** This paragraph said "synchronous_commit
  // is off on this database" unconditionally while `topology()` above parsed the
  // real setting off the compose command line — so when all four configurations
  // dropped it from the server on 31 August, the box two panels up correctly
  // printed nothing and this sentence went on claiming the opposite. A viewer
  // that reads a file and then narrates a different file is worse than one that
  // never read it, because the reading is what makes it believable.
  wp.append(el('p', 'bd-risk-n', t.postgres?.synchronousCommit === 'off'
    ? 'synchronous_commit is off on this database. A crash loses the last few '
      + 'milliseconds of commits, traded for fifty seconds of throughput. ADR-0035 '
      + 'calls that a decision rather than a setting, and a data-loss bug if it is '
      + 'copied from a tuning guide.'
    : 'synchronous_commit is on at the server, and the configuration says that '
      + 'reverses an earlier decision: at a fraction of the statement ceiling it was '
      + 'buying headroom this environment already had and paying acknowledged-commit '
      + 'durability on the money path for it. It is turned off per statement instead '
      + '— SET LOCAL, never SET, because under transaction pooling a session-level '
      + 'SET leaks onto whichever connection the pooler hands out next. ADR-0035 '
      + 'still states the server-wide setting as its decision and has not been '
      + 'amended, so the ADR and the four files it governs disagree.'));
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
    fact('simulated', clock(simSeconds / 60),
      `ended in ${state}, which is the only state teardown is allowed from`);
    fact('orders taken', Math.round(orders).toLocaleString('en-GB'),
      rejected >= 1
        ? `${Math.round(replayed).toLocaleString('en-GB')} replayed, `
          + `${Math.round(rejected).toLocaleString('en-GB')} to sync.rejection under `
          + `${policy.value}`
        : 'all replayed into the permanent platform, none rejected');
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

    result.append(el('p', 'bd-result-h', 'The same run, priced'));
    const grid = el('div', 'bd-prices');
    for (const provider of PROVIDERS) {
      const hours = simSeconds / 3600;
      const card = el('div', `bd-price bd-price-${provider.key}`);
      card.append(el('div', 'bd-price-v', money(provider.hourly * hours)));
      card.append(el('div', 'bd-price-n', provider.name));
      card.append(el('div', 'bd-price-h',
        `$${provider.hourly.toFixed(2)} an hour while it runs`
        + (provider.month ? ` · $${provider.month.toLocaleString('en-GB')} a month` : '')));
      card.append(el('div', 'bd-price-tag', 'the package’s own figure'));
      grid.append(card);
    }
    result.append(grid);

    result.append(el('p', 'bd-risk-n',
      'Both rates are the package’s, from handoff/TICVAI_Hosting_Summary.docx, which prices '
      + 'all four hosting options on Amazon and Google side by side. Option 3 is the big '
      + 'sale, billed by the hour while it runs. Charged for the whole time the environment '
      + 'existed rather than only while it was serving, because that is how it is rented.'));

    // The compute share, kept small and underneath. It answers "how much of
    // this is containers" and nothing else.
    const computeLine = COMPUTE_RATES.map((r) => {
      const provider = PROVIDERS.find((x) => x.key === r.key);
      const compute = cpuHours * r.vcpu + gbHours * r.gb;
      return `${provider?.name ?? r.key} ${money(compute)}`;
    }).join(' · ');
    result.append(el('p', 'bd-risk-n',
      `Container compute alone over ${cpuHours.toFixed(1)} cpu-hours and `
      + `${gbHours.toFixed(0)} GB-hours would be ${computeLine} at list rates — mine, not the `
      + 'package’s, and short of the figures above because they exclude the managed database, '
      + 'storage, IO and egress. The Hosting Summary puts the gap between the two providers '
      + '"mostly on database pricing", which is precisely the part this leaves out.'));

    result.append(el('p', 'bd-open',
      'The package names two different shortlists for the same open decision. CF-64 in '
      + 'docs/active/deployment-and-scaling-brief.md reads "AWS or Azure, pending DESC", '
      + 'owned by Dinesh and Qossai. The Hosting Summary prices Amazon and Google, says '
      + '"we priced both", and notes Google comes out 15 to 18% cheaper — while adding that '
      + 'this is not a reason to pick it, because what matters more is which one satisfies '
      + 'the Dubai compliance guidance nobody has yet. Azure is priced nowhere. Everything '
      + 'above that decision is provider-neutral and nothing below it can be: the managed '
      + 'Postgres, the Redis tier, Qdrant hosting, the CDN and the secret store all follow '
      + 'from it, and CF-64 also carries the RPO and RTO targets, which are stated nowhere '
      + 'else.'));
  };

  // ── the simulation ────────────────────────────────────────────────────────
  const stillness = window.matchMedia('(prefers-reduced-motion: reduce)');

  const baseCpu = num(t.postgres?.cpus) + num(t.redis?.cpus);
  const baseGb = gigs(t.postgres?.memory) + gigs(t.redis?.memory);
  // **Anchored on the environment as configured, not on the widest the drawing
  // goes.** $11.76 an hour is what the Hosting Summary charges for option 3,
  // and option 3 is this compose file — so the meter has to read $11.76 when
  // the clusters are at the size that file provisions. Dividing by a drawn
  // maximum instead made the quoted configuration cost two thirds of its own
  // price.
  const specCpu = baseCpu + t.deployed.reduce((a, s) => a + num(s.cpus) * s.specReplicas, 0);
  const perCpuHour = specCpu > 0 ? RATE_PER_HOUR / specCpu : 0;

  // How long a `system` transition takes to fire, in simulated seconds. The
  // ADR says provisioning takes minutes and a sale takes seconds, and gives no
  // figures; these are this page's, and they only pace the animation.
  const DWELL = { provisioning: 240, warming: 150, reconciling: null };

  let state = machine ? (machine.initial ?? [])[0] ?? 'requested' : 'live';
  let started = false;
  let stateSince = 0;
  let simSeconds = 0;
  let last = 0;
  let buyers = 0;
  let threshold = 0.7;
  let divergence = 0;
  let orders = 0;
  let replayed = 0;
  let rejected = 0;
  let spent = 0;
  let cpuHours = 0;
  let gbHours = 0;
  let peakContainers = 0;
  let peakClient = 0;
  let everCapped = false;
  // Where each cluster actually is, as opposed to where it wants to be. Kept
  // as a float so scaling reads as a movement rather than as a jump.
  const at = new Map(clusters.map((c) => [c.service.name, 0]));

  const LOOK = {
    requested: { infra: 0, live: false, billing: false },
    provisioning: { infra: 1, live: false, billing: true },
    warming: { infra: 1, live: false, billing: true },
    live: { infra: 1, live: true, billing: true },
    draining: { infra: 1, live: true, billing: true, draining: true },
    reconciling: { infra: 1, live: false, billing: true, replay: true },
    reconciled: { infra: 1, live: false, billing: true },
    decommissioned: { infra: 0, live: false, billing: false },
  };
  const lookOf = (name) => LOOK[name] ?? { infra: 1, live: false, billing: true };

  const guardInto = (to) => (machine?.transitions ?? [])
    .find((tr) => tr.from === state && tr.to === to)?.guard ?? '';

  const enter = (next) => {
    state = next;
    stateSince = simSeconds;
    if (next === 'reconciling') { replayed = 0; rejected = 0; }
    if (next === 'decommissioned') showResult();
  };

  /**
   * An operation the reader pressed. **Refused rather than ignored when the
   * model does not allow it** — `decommissionBurstEnvironment` before
   * `reconciled` is the 409 ADR-0035 is built around, and a button that
   * silently does nothing teaches the opposite of what the ADR decided.
   */
  const fire = (operation) => {
    const allowed = (byOperation.get(operation) ?? []).find((tr) => tr.from === state);
    if (allowed) {
      started = true;
      enter(allowed.to);
      refused.hidden = true;
      return;
    }
    refused.hidden = false;
    refused.textContent = operation === 'decommissionBurstEnvironment'
      ? `409. decommissionBurstEnvironment is refused in ${state}: decommissioned is `
        + 'reachable only through reconciled, because an environment torn down before its '
        + 'orders reach the permanent platform has lost real money and real tickets. '
        + 'ADR-0035.'
      : `${operation} has no transition out of ${state} in states/burst-environment.yaml.`;
  };

  const rps = () => buyers * CALLS_PER_BUYER;
  const demand = () => Math.min(1.4, rps() / PEAK_RPS);

  /**
   * **The package's calculator, per service.** derive-sizing.py:
   *
   *   replicas = max(floor, ceil(load_rps x share / (rps_per_replica x target)))
   *
   * Each service has its own cliff — 400 RPS a replica for Catalogue, 250 for
   * Order, 600 for Identity — and its own share of the mix, so they scale
   * independently and at different loads. Catalogue adds a replica every 240
   * RPS of its own traffic, Order every 150, Identity every 360.
   *
   * The target is why one replica is sized to carry 60% of what it can rather
   * than all of it: the headroom a scale-out needs has to exist before the
   * scale-out starts. Dropping that term is what makes burst-scope's floors
   * 8/5/2 where the calculator says 14/8/2.
   *
   * There is no ceiling to clamp against, deliberately.
   */
  const wantedFor = (service, loadRps) => {
    const serviceRps = loadRps * (service.shareOfLoad / 100);
    const effective = service.perReplica * threshold;
    const need = effective > 0 && serviceRps > 0 ? Math.ceil(serviceRps / effective) : 0;
    return Math.max(service.absoluteMin, need);
  };

  const step = (dt) => {
    const look = lookOf(state);
    if (started && state !== 'decommissioned') simSeconds += dt * SIM_PER_REAL;
    const held = simSeconds - stateSince;

    // system transitions fire on their own
    const dwell = DWELL[state];
    if (dwell != null && held >= dwell) {
      const next = (machine?.transitions ?? [])
        .find((tr) => tr.from === state && tr.trigger === 'system' && tr.to !== 'failed');
      if (next) enter(next.to);
    }

    // buyers arrive only while the environment is serving them
    if (look.live && !look.draining) orders += buyers * dt * SIM_PER_REAL;

    // the merge back, at a rate that finishes a large sale in a few minutes of
    // simulated time rather than instantly — the point is that it takes long
    // enough to be interrupted, which is why it is resumable
    if (look.replay) {
      const share = divergence;
      const rate = Math.max(400, orders / 180);
      const moved = Math.min(orders - replayed - rejected, rate * dt * SIM_PER_REAL);
      // `reject` is the only policy that sends anything to sync.rejection. The
      // other two replay everything and pay for it elsewhere: honourSnapshot
      // may undercharge, honourCurrent charges a price the guest never saw.
      const toReject = policy.value === 'reject' ? moved * share : 0;
      rejected += toReject;
      replayed += moved - toReject;
      if (orders > 0 && replayed + rejected >= orders - 1) {
        const done = (machine?.transitions ?? [])
          .find((tr) => tr.from === 'reconciling' && tr.trigger === 'system');
        if (done) enter(done.to);
      } else if (orders === 0) {
        const done = (machine?.transitions ?? [])
          .find((tr) => tr.from === 'reconciling' && tr.trigger === 'system');
        if (done) enter(done.to);
      }
    }

    // autoscale: up quickly, down slowly. A cluster that follows demand down as
    // fast as it followed it up flaps on every dip, and the cooldown is why
    // real autoscalers do not.
    const d = look.live ? demand() : 0;
    const liveRps = look.live ? rps() : 0;
    let replicas = 0;
    let client = 0;
    let cpu = look.infra > 0 ? baseCpu : 0;
    let gb = look.infra > 0 ? baseGb : 0;
    const short = [];

    for (const c of clusters) {
      const running = look.infra > 0 && (look.live || look.replay || state === 'warming');
      const want = running ? wantedFor(c.service, look.live ? liveRps : 0) : 0;
      // Nothing clamps it down to a cap, because there is not one. The only
      // limit is how many boxes were drawn, and that was laid out for the most
      // the control can ask for — so this only bites if the model changes
      // under the drawing.
      const target = Math.min(c.service.max, want);
      if (want > c.service.max) { short.push(`${c.service.short} wants ${want}`); }
      const now2 = at.get(c.service.name) ?? 0;
      const pace = target > now2 ? 6 : 1.4;
      at.set(c.service.name, now2 + (target - now2) * Math.min(1, dt * pace));
      const n = Math.round(at.get(c.service.name));
      replicas += n;
      client += n * c.service.poolMax;
      cpu += num(c.service.cpus) * n;
      gb += gigs(c.service.memory) * n;
      c.cells.forEach((cell, k) => cell.classList.toggle('on', k < n));
      const svcRps = Math.round(liveRps * (c.service.shareOfLoad / 100));
      c.count.textContent = look.infra > 0
        ? `${n} replica${n === 1 ? '' : 's'}`
          + ` · ${svcRps.toLocaleString('en-GB')} rps of its own`
          + (n <= c.service.absoluteMin && svcRps === 0 ? ' · at its floor' : '')
          + (c.service.poolMax ? ` · ${n * c.service.poolMax} conns` : '')
        : 'not running';
      c.node.classList.toggle('bd-quiet', look.infra === 0);
      c.node.classList.toggle('bd-capped', want > c.service.max);
    }

    // The one number that is not a consequence: what each service adds a
    // replica for. They are different, so they scale at different moments.
    targetNote.textContent = `each replica sized to carry ${Math.round(threshold * 100)}% of `
      + `its cliff, so a replica is added every `
      + t.deployed.map((x) => `${Math.round(x.perReplica * threshold)} rps of ${x.short}`)
        .join(', ')
      + `. The package sets this at ${Math.round((t.deployed[0]?.target ?? 0.6) * 100)}% in `
      + 'tools/derive-sizing.py — one replica carries that much of what it can, so the '
      + 'headroom a scale-out needs exists before the scale-out starts.';

    if (short.length && look.live) {
      everCapped = true;
      capped.hidden = false;
      // Two different sentences, because a cluster the package caps and one it
      // deliberately does not are not the same situation. Saying "the file
      // caps them" of a service whose max is null, with a note attached
      // explaining that the absence of a cap is the point, would be inventing
      // a limit and then complaining about it.
      const anyUncapped = clusters.some((c) => c.service.uncapped);
      capped.textContent = anyUncapped
        ? `At ${Math.round(threshold * 100)}% this needs more than is drawn — `
          + `${short.join(', ')}. burst-scope.json states no ceiling for these on purpose: `
          + 'a cap is a cap on absorbing a peak nobody predicted, and the peak is the whole '
          + 'reason the environment exists. The boxes stop because the picture does.'
        : `At ${Math.round(threshold * 100)}% the file does not allow enough `
          + `replicas — ${short.join(', ')}. deploy/c-flash-sale.yml caps them, so `
          + 'utilisation runs above target and ADR-0032 sheds rather than queues: guest '
          + 'and public first, staff and service last.';
    } else {
      capped.hidden = true;
    }

    if (look.billing && started) {
      const hours = (dt * SIM_PER_REAL) / 3600;
      spent += cpu * perCpuHour * hours;
      cpuHours += cpu * hours;
      gbHours += gb * hours;
    }
    peakContainers = Math.max(peakContainers, replicas);
    peakClient = Math.max(peakClient, client);

    return { look, replicas, client, cpu, d };
  };

  const paint = ({ look, replicas, client, cpu, d }) => {
    outClockV.textContent = clock(simSeconds / 60);
    // The rate you are offering, whether or not anything is up to take it.
    // Reading '0' while the slider sat at 90 made the control look broken when
    // what was actually true was that nothing had been deployed to serve it.
    outRps.textContent = Math.round(rps()).toLocaleString('en-GB');
    outRps.classList.toggle('bd-unserved', buyers > 0 && !look.live);
    outOrders.textContent = Math.round(orders).toLocaleString('en-GB');
    outReplicas.textContent = String(replicas);
    outSpend.textContent = money(spent);
    const rate = look.billing && started ? cpu * perCpuHour : 0;
    outRate.textContent = rate ? `${money(rate)}/h` : '—';

    const over = t.bouncer?.maxClient ? client > t.bouncer.maxClient : false;
    outReplicas.classList.toggle('bd-over', over);
    if (poolRow) poolRow.classList.toggle('bd-thr-hot', over);

    const waiting = buyers > 0 && !look.live;
    stateLine.classList.toggle('bd-state-wait', waiting);
    stateLine.textContent = look.live
      ? `${state} · ${Math.round(client).toLocaleString('en-GB')} client connections into `
        + `${t.bouncer?.poolSize ?? '—'} server ones`
      : waiting
        ? `${Math.round(rps()).toLocaleString('en-GB')} requests a second are being offered `
          + `and nothing is serving them — the environment is ${state}. `
          + (started
            ? 'It is coming up; provisioning and warming take minutes.'
            : 'Press “Stand the environment up”. And note what this is showing you: '
              + 'ADR-0035 asks for it against the sale calendar rather than against '
              + 'arriving demand, because requesting it when the load appears is '
              + 'requesting it too late.')
        : started
          ? `${state} · nothing is arriving`
          : 'nothing is running yet. Stand the environment up, then set the load.';

    const next = (machine?.transitions ?? []).find((tr) => tr.from === state);
    guard.textContent = next?.guard ? stripEmphasis(next.guard) : '';

    for (const b of opButtons) {
      const allowed = b.list.some((tr) => tr.from === state);
      b.node.classList.toggle('bd-op-on', allowed);
      // Not disabled: pressing decommission early is how the 409 gets seen, and
      // that refusal is the point of the state model.
      b.node.classList.toggle('bd-op-off', !allowed);
    }

    loadLabel.textContent = `${buyers}/s`;
    loadNote.textContent =
      `${Math.round(rps()).toLocaleString('en-GB')} requests a second at ${CALLS_PER_BUYER} `
      + `per buyer · ${PEAK_BUYERS}/s is the ${PEAK_RPS.toLocaleString('en-GB')} RPS `
      + 'ADR-0035 describes, where a stadium’s whole day arrives in fifty seconds';

    section.style.setProperty('--bd-infra', String(look.infra));
    ingress.classList.toggle('bd-quiet', !look.live || look.draining);

    const writing = look.live && d > 0.02;
    wp.classList.toggle('bd-idle', !writing);
    if (!stillness.matches && writing) {
      wdot.setAttribute('cx', String(28 + ((performance.now() / 2600) % 1) * 870));
      wdot.setAttribute('opacity', '1');
    } else {
      wdot.setAttribute('opacity', '0');
    }

    // the merge lane
    mergePath.classList.toggle('bd-merge-on', Boolean(look.replay));
    mergeLabel.classList.toggle('bd-merge-on', Boolean(look.replay));
    const moving = look.replay && orders > 0;
    mergeDots.forEach((dot, k) => {
      if (!moving || stillness.matches) { dot.setAttribute('opacity', '0'); return; }
      const u = (((performance.now() / 2200) + k / mergeDots.length) % 1);
      const point = mergePath.getPointAtLength(u * mergeLen);
      dot.setAttribute('cx', String(point.x));
      dot.setAttribute('cy', String(point.y));
      dot.setAttribute('opacity', String(0.35 + 0.65 * Math.sin(u * Math.PI)));
    });

    if (look.replay) {
      const done = orders > 0 ? (replayed + rejected) / orders : 1;
      recFill.style.width = `${Math.round(done * 100)}%`;
      recNote.textContent = orders > 0
        ? `${Math.round(replayed).toLocaleString('en-GB')} replayed in sequence`
          + (rejected >= 1
            ? ` · ${Math.round(rejected).toLocaleString('en-GB')} to sync.rejection`
            : '')
          + ` of ${Math.round(orders).toLocaleString('en-GB')} · resumable, so an `
          + 'interruption continues from here rather than restarting'
        : 'nothing was sold, so there is nothing to move';
      rec.classList.remove('bd-idle');
    } else {
      const done = state === 'reconciled' || state === 'decommissioned';
      recFill.style.width = done ? '100%' : '0%';
      recNote.textContent = done
        ? `${Math.round(replayed).toLocaleString('en-GB')} orders landed`
          + (rejected >= 1 ? `, ${Math.round(rejected).toLocaleString('en-GB')} rejected` : '')
          + ' — and only now may the environment be torn down'
        : 'idle';
      rec.classList.add('bd-idle');
    }

    policyNote.textContent = divergence === 0
      ? 'no price moved during the sale, so the policy costs nothing. ADR-0035 gives '
        + 'priceDivergencePolicy no default on purpose — the answer depends on how large '
        + 'the divergence is and who the venue would rather disappoint.'
      : policy.value === 'reject'
        ? `${Math.round(divergence * 100)}% of orders reject at reconciliation and land in `
          + 'sync.rejection. Safe, and it turns a completed purchase into a support case.'
        : policy.value === 'honourCurrent'
          ? `${Math.round(divergence * 100)}% replay at the current price. Correct in the `
            + 'ledger, and it charges somebody a price they never saw.'
          : `${Math.round(divergence * 100)}% replay at the price the guest saw. What a guest `
            + 'expects, and it may undercharge.';

    if (!stillness.matches) {
      const now2 = performance.now();
      for (const f of flow) {
        f.path.style.strokeOpacity = String(0.08 + 0.55 * (look.live ? d : 0));
        f.path.style.strokeDashoffset =
          String(-((now2 / (26 - 16 * Math.min(1, d))) * (0.2 + f.weight / 100)) % 1000);
      }
    }
  };

  const frame = (now) => {
    const dt = last ? Math.min(0.064, (now - last) / 1000) : 0.016;
    last = now;
    paint(step(dt));
    requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);

  loadRange.oninput = () => { buyers = Number(loadRange.value); };
  thrRange.oninput = () => {
    threshold = Number(thrRange.value) / 100;
    thrLabel.textContent = `${thrRange.value}%`;
  };
  divRange.oninput = () => {
    divergence = Number(divRange.value) / 100;
    divLabel.textContent = `${divRange.value}%`;
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
    + `compose file declares: ${specCpu} cpu as configured, ${baseCpu} for the database `
    + 'and cache alone. That split is a model, not a quote. pgbouncer declares no cpu '
    + 'limit in this file and so weighs nothing in it.'));
  section.append(cost);

  head.append(el('p', 'bd-sub bd-sub-fine',
    `${t.deployed.reduce((a, x) => a + x.min, 0)} containers at rest, `
    + `${t.deployed.reduce((a, x) => a + x.max, 0)} fully expanded. Nothing here is on a `
    + 'timeline: the environment is requested, the clusters follow the load you set, and '
    + 'the state changes when you ask for one or when the model says it happens on its '
    + 'own. callsPerBuyer is estimated from the flow steps rather than measured — '
    + 'tools/bench.py replaces those numbers when there is something to run it against.'));
}
