/**
 * Domain lenses — one subject, gathered across every artefact kind.
 *
 * The package is organised by kind: contracts, states, events, screens, tables,
 * decisions. That is the right organisation, and `handoff/ai-index.md` says why
 * it must not be broken — "AI has no folder of its own, and should not … a
 * single domain folder would raise the question of why there is no finance/".
 *
 * But a reader asking "what is the AI story, and is it consistent?" has to hold
 * nine places in their head, and the file written to solve that — the index —
 * had gone stale in four ways within one dump: it said 22 operations against a
 * contract with 24, six screens against eight, four state models against five,
 * and named seven events as not existing when all seven did. Prose cannot track
 * a moving package. So the lens is derived instead.
 *
 * Membership has two sources, and the gap between them is the point:
 *
 *   DERIVED   from a seed contract, by closure over the same graph every other
 *             view resolves against — operation → schema → enum → state model →
 *             event, and operation → table, → screen, → decision.
 *   DECLARED  from `x-ticvai-domain` on an operation, or `domain:` in a state,
 *             event or flow file. Intent, written down by a person.
 *
 * Neither alone is enough, and `states/conversation.yaml` is the proof. It is
 * the assistant-to-human handover, and no rule finds it: it is not named
 * `ai-*`, it checks `marketing-crm.ConversationState`, it is owned by
 * marketing-crm, and every one of its transitions names a marketing-crm
 * operation — handoverToAgent, claimConversation, transferConversation. The
 * graph correctly sees a CRM model, because the AI part of a conversation is
 * the state it starts in, not any move anybody makes. Only a declaration finds
 * it, and the same is true of ADR-0021, which decides how AI vectors are
 * partitioned while its title says Qdrant and its summary names no operation.
 *
 * Where the two disagree, this file reports rather than picks. A derived member
 * nobody declared is usually a missing tag; a declared member nothing reaches is
 * usually an artefact that has drifted out of the graph. Both are findings.
 */

const DOMAINS = [
  {
    key: 'ai',
    label: 'AI',
    blurb:
      'Assistant, retrieval, governance, configuration assistance and map generation. ' +
      'Spread across nine places by design — this gathers them.',
    // The contract file stem the closure starts from. Everything else is reached.
    seed: ['ai'],
    // Prose that belongs to this domain and names no operation, so nothing
    // reaches it by closure. Listed because a missing page is worse than a
    // hand-maintained list of four.
    docs: [
      'docs/architecture/ai-platform.md',
      'docs/architecture/ai-credentials.md',
      'handoff/ai-index.md',
      'handoff/rag-index-sources.md',
    ],
  },
];

/** `x-ticvai-domain: ai` or `x-ticvai-domain: [ai, finance]` — both are meant. */
const declaredOn = (value) => {
  if (!value) return [];
  if (Array.isArray(value)) return value.map((v) => String(v).toLowerCase().trim()).filter(Boolean);
  return String(value)
    .split(/[,·]/)
    .map((v) => v.toLowerCase().trim())
    .filter(Boolean);
};

/**
 * One pass of closure. Kept explicit rather than generic because each hop is a
 * different join and naming them is the documentation — a reader can check the
 * chain against the package without reading the code that walks it.
 */
function derive(domain, sources) {
  const { operations, machines, events, lineage, journeys, adrs } = sources;
  const seed = new Set(domain.seed);

  // ── 1. operations, from the seed contract ────────────────────────────────
  const ops = operations.filter((o) => seed.has(stem(o.file)));
  const opNames = new Set(ops.map((o) => o.name));

  // ── 2. schemas the seed operations read or write ─────────────────────────
  const schemaIds = new Set();
  for (const o of ops) {
    for (const id of [...(o.consumes ?? []), ...(o.produces ?? [])]) schemaIds.add(id);
  }

  // ── 3. state models a seed operation moves ───────────────────────────────
  // This is the hop that finds conversation.yaml: `createAiConversation` is
  // named on one of its transitions, and nothing else about the file says AI.
  const machineHits = machines.filter((m) =>
    seed.has(m.contract ?? '') ||
    seed.has(m.owner ?? '') ||
    m.transitions.some((t) => t.operation && opNames.has(t.operation))
  );
  const machineIds = new Set(machineHits.map((m) => m.id));

  // ── 4. events those transitions publish, plus any the seed context owns ──
  const emitted = new Set();
  for (const m of machineHits) {
    for (const t of m.transitions) for (const e of t.emits ?? []) emitted.add(e);
  }
  const eventHits = events.filter(
    (e) => emitted.has(e.name) || seed.has(e.publisher ?? '')
  );

  // ── 5. tables the seed operations touch, through the lineage ─────────────
  const tables = new Map();
  for (const row of lineage?.operations ?? []) {
    if (!opNames.has(row.name)) continue;
    for (const t of row.reads ?? []) touch(tables, t, 'reads');
    for (const t of row.writes ?? []) touch(tables, t, 'writes');
  }

  // ── 6. screens that call a seed operation ────────────────────────────────
  // `operationUsage` is keyed by operation and holds { screens, flows }; the
  // flows come along for free and are worth keeping — a domain with operations
  // and no flow through them is a capability nobody has drawn a path to.
  const screenIds = new Set();
  const flowIds = new Set();
  for (const [op, usage] of Object.entries(journeys?.operationUsage ?? {})) {
    if (!opNames.has(op)) continue;
    for (const s of usage?.screens ?? []) screenIds.add(typeof s === 'string' ? s : s?.id);
    for (const f of usage?.flows ?? []) flowIds.add(typeof f === 'string' ? f : f?.id);
  }
  screenIds.delete(undefined);
  flowIds.delete(undefined);

  // ── 7. decisions that name one of the above ──────────────────────────────
  // An ADR is prose and reaches nothing, so it is matched on mention. The
  // needles are operation names and the domain key as a whole word, which is
  // specific enough that `ai` does not match `maintenance`.
  const needle = new RegExp(`\\b(${[...opNames].join('|')}|${domain.key})\\b`, 'i');
  const decisionHits = (adrs ?? []).filter((a) =>
    needle.test(`${a.title} ${a.lead ?? ''} ${a.decision ?? ''} ${a.constrains?.join(' ') ?? ''}`)
  );

  return {
    operations: ops,
    schemaIds,
    machines: machineHits,
    machineIds,
    events: eventHits,
    tables: [...tables.values()],
    screenIds,
    flowIds,
    decisions: decisionHits,
  };
}

const stem = (file) => String(file ?? '').replace(/\\/g, '/').split('/').pop().replace(/\.ya?ml$/i, '');

function touch(map, name, how) {
  if (!name) return;
  if (!map.has(name)) map.set(name, { name, reads: 0, writes: 0 });
  map.get(name)[how] += 1;
}

/**
 * What a person declared.
 *
 * The package states this in `handoff/domain-markers.json` — one sidecar file
 * keyed `kind:id`, values like `ai:seed` or `ai:reached via conversation.handedOver`.
 * That is a better home than the inline tag this module first asked for: one
 * file to regenerate rather than an edit in sixty, and it survives a dump
 * instead of being overwritten by one. STRUCTURE.md states the same rule this
 * module was written around — "directories are artefact kinds, and the domains
 * cut across them" — so the two agree by construction now rather than by luck.
 *
 * The marker carries the reason as well as the domain, and the reason is worth
 * keeping: "reached via conversation.handedOver" says more than "ai".
 *
 * Key shapes differ from the viewer's own, and are normalised here rather than
 * anywhere else: states are named with their file extension, documents by full
 * path. Inline tags are still read, so a marker added by hand to a single file
 * keeps working, but nothing in the package uses them any more.
 */
function collectDeclared(sources) {
  const { operations, machines, events, screens, adrs, markers } = sources;
  const declared = new Map();
  const put = (kind, id, keys, why) => {
    if (!keys?.length || !id) return;
    const at = declared.get(`${kind}:${id}`) ?? { keys: [], why: null };
    for (const k of keys) if (!at.keys.includes(k)) at.keys.push(k);
    at.why = at.why ?? why ?? null;
    declared.set(`${kind}:${id}`, at);
  };

  // ── the sidecar ─────────────────────────────────────────────────────
  for (const [rawKey, values] of Object.entries(markers ?? {})) {
    const [kind, ...rest] = rawKey.split(':');
    let id = rest.join(':');
    if (!kind || !id) continue;

    // `ai:seed` → domain `ai`, reason `seed`
    const keys = [];
    let why = null;
    for (const value of values ?? []) {
      const at = String(value).indexOf(':');
      keys.push((at < 0 ? value : value.slice(0, at)).trim().toLowerCase());
      if (at >= 0 && !why) why = value.slice(at + 1).trim();
    }

    if (kind === 'state') id = id.replace(/\.ya?ml$/i, '');
    if (kind === 'document') {
      // an ADR is a decision to the rest of the viewer; anything else is prose
      const adr = /(\d{4})-[^/]*\.md$/.exec(id);
      put(adr ? 'decision' : 'document', adr ? adr[1] : id, [...new Set(keys)], why);
      continue;
    }
    put(kind, id, [...new Set(keys)], why);
  }

  // ── inline tags, still honoured ─────────────────────────────────────
  for (const o of operations) put('operation', o.name, declaredOn(o.domain));
  for (const m of machines) put('state', m.id, declaredOn(m.domain));
  for (const e of events) put('event', e.name, declaredOn(e.domain));
  for (const s of screens ?? []) put('screen', s.id, declaredOn(s.domain));
  for (const a of adrs ?? []) put('decision', a.id, declaredOn(a.domains ?? a.domain));
  return declared;
}

/**
 * Derived and declared, reconciled. `members` is the union — a lens that showed
 * only the intersection would hide exactly the artefacts worth looking at.
 */
export function buildDomains(sources) {
  const declared = collectDeclared(sources);
  const lenses = [];

  for (const domain of DOMAINS) {
    const d = derive(domain, sources);

    const declaredIn = (kind, id) => (declared.get(`${kind}:${id}`)?.keys ?? []).includes(domain.key);
    const declaredWhy = (kind, id) => declared.get(`${kind}:${id}`)?.why ?? null;
    const gaps = [];

    // one row per artefact, carrying how it got here
    const member = (kind, id, label, extra0 = {}) => {
      let extra = extra0;
      const isDerived = extra.derived !== false;
      const isDeclared = declaredIn(kind, id);
      // the package's own reason beats the one derivation guessed
      const said = declaredWhy(kind, id);
      if (said) extra = { ...extra, why: said };
      if (isDerived && !isDeclared) {
        gaps.push({
          kind, id, label,
          gap: 'derived-not-declared',
          note: extra.why ?? 'reached by the graph; nothing declares it',
        });
      }
      return { kind, id, label, derived: isDerived, declared: isDeclared, ...extra };
    };

    const members = [
      ...d.operations.map((o) =>
        member('operation', o.name, o.name, {
          method: o.method, path: o.path, permission: o.permission,
          scopeLevel: o.scopeLevel, file: o.file,
          why: 'declared in the seed contract',
        })
      ),
      ...d.machines.map((m) =>
        member('state', m.id, m.entity, {
          contract: m.contract, enum: m.enum, owner: m.owner, file: m.file,
          states: m.states.length, transitions: m.transitions.length,
          // the reason this hop exists — worth carrying to the page
          why: m.transitions.some((t) => t.operation && d.operations.some((o) => o.name === t.operation))
            ? 'a seed operation moves it'
            : 'the seed contract owns it',
        })
      ),
      ...d.events.map((e) =>
        member('event', e.name, e.name, {
          publisher: e.publisher, consumers: (e.consumers ?? []).length,
          why: e.publisher && domain.seed.includes(e.publisher)
            ? 'published by the seed context'
            : 'emitted by a transition in this domain',
        })
      ),
      ...d.tables.map((t) =>
        member('table', t.name, t.name, {
          reads: t.reads, writes: t.writes,
          why: 'a seed operation reads or writes it',
        })
      ),
      ...[...d.screenIds].sort().map((id) =>
        member('screen', id, id, { why: 'calls a seed operation' })
      ),
      ...[...d.flowIds].sort().map((id) =>
        member('flow', id, id, { why: 'a step in it calls a seed operation' })
      ),
      ...d.decisions.map((a) =>
        member('decision', a.id, a.title, {
          status: a.status, file: a.file,
          why: 'names an operation in this domain',
        })
      ),
    ];

    // declared but unreachable — the other half of the disagreement
    for (const [key, entry] of declared) {
      if (!entry.keys.includes(domain.key)) continue;
      const [kind, id] = splitOnce(key);
      if (members.some((m) => m.kind === kind && m.id === id)) continue;
      members.push({
        kind, id, label: id, derived: false, declared: true,
        why: entry.why ?? 'declared only',
      });
      gaps.push({
        kind, id, label: id,
        gap: 'declared-not-derived',
        note: 'a person put it here; nothing in the graph reaches it',
      });
    }

    const byKind = {};
    for (const m of members) (byKind[m.kind] ??= []).push(m);

    lenses.push({
      key: domain.key,
      label: domain.label,
      blurb: domain.blurb,
      seed: domain.seed,
      docs: domain.docs ?? [],
      members,
      byKind,
      gaps,
      stats: {
        total: members.length,
        derived: members.filter((m) => m.derived).length,
        declared: members.filter((m) => m.declared).length,
        both: members.filter((m) => m.derived && m.declared).length,
        gaps: gaps.length,
        ...Object.fromEntries(Object.entries(byKind).map(([k, v]) => [k, v.length])),
      },
    });
  }

  return {
    present: lenses.some((l) => l.stats.total > 0),
    lenses,
    // so a tree row in any layer can ask "which lenses is this in?" in O(1)
    byArtefact: index(lenses),
  };
}

function splitOnce(key) {
  const at = key.indexOf(':');
  return [key.slice(0, at), key.slice(at + 1)];
}

function index(lenses) {
  const out = {};
  for (const lens of lenses) {
    for (const m of lens.members) {
      (out[`${m.kind}:${m.id}`] ??= []).push(lens.key);
    }
  }
  return out;
}

export { DOMAINS };
