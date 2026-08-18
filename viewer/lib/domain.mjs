// states/ and events/ — the two artefacts that check each other.
//
// Thirty-eight enums in the contracts declare what states exist. None of them
// declares which moves between those states are allowed, so nothing catches an
// order going from `held` to `refunded` without ever being paid: the enum
// permits it, the business does not, and no artefact said so. states/ is where
// that is said.
//
// events/ is the other half. `platform.outbox` has always existed and has
// always been correct; what never existed was a description of what it carries.
// An event without a written consumer is a contract between two services that
// neither one wrote down.
//
// They are worth reading together because each one checks the other:
//
//   a transition claims to emit `order.paid`  ->  is that in the catalogue?
//   an event claims to be emitted on paid     ->  is there a transition that does?
//
// tools/check-states.py runs the same checks from the command line. It is
// currently reporting five errors that are not real — its CONTRACTS path points
// at a sibling directory that does not exist here, so it loads zero enums and
// every lookup fails. This module resolves against the contracts the viewer has
// already indexed, so it cannot go looking in the wrong place.

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';

const STATES_DIR = 'states';
const EVENTS_DIR = 'events';

/**
 * A publishing or consuming context, as an event names it, is a bounded context
 * — which is also what a contract is. Most match on the name; these two do not,
 * and guessing would be worse than saying so.
 */
const CONTEXT_ALIASES = {
  ledger: 'finance',
  marketing: 'marketing-crm',
};

async function readYamlDir(root, dir) {
  const out = [];
  let entries;
  try {
    entries = await readdir(path.join(root, dir), { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    if (!entry.isFile() || !/\.ya?ml$/i.test(entry.name)) continue;
    if (entry.name.startsWith('_')) continue; // _schema.yaml describes the shape
    const rel = `${dir}/${entry.name}`;
    try {
      out.push({ rel, doc: yaml.load(await readFile(path.join(root, rel), 'utf8')) });
    } catch (err) {
      out.push({ rel, error: err.message });
    }
  }
  out.sort((a, b) => a.rel.localeCompare(b.rel));
  return out;
}

const list = (x) => (Array.isArray(x) ? x : []);

/**
 * Longest distance from an initial state, over transitions that move forward.
 *
 * Reversals are excluded from the depth walk on purpose: refunded is reached
 * from paid, and letting that edge set the depth would drag the whole tail of
 * the machine back to the left. They are still drawn — they are just not what
 * decides where a state sits.
 */
function computeDepths(stateNames, transitions, initial) {
  const depth = new Map(stateNames.map((s) => [s, 0]));
  const forward = transitions.filter((t) => !t.isReversal);
  const seeds = initial.length ? initial : stateNames.slice(0, 1);
  for (const s of seeds) depth.set(s, 0);

  // relax repeatedly; |V| passes settle any DAG, and the guard stops a cycle
  for (let pass = 0; pass < stateNames.length + 1; pass++) {
    let moved = false;
    for (const t of forward) {
      if (!depth.has(t.from) || !depth.has(t.to)) continue;
      const next = depth.get(t.from) + 1;
      if (next > depth.get(t.to) && next <= stateNames.length) {
        depth.set(t.to, next);
        moved = true;
      }
    }
    if (!moved) break;
  }

  // a state no forward edge reaches sits at 0, which would file it beside the
  // initial state; push it just past whatever does reach it instead
  for (const s of stateNames) {
    if (initial.includes(s) || depth.get(s) > 0) continue;
    const from = transitions.filter((t) => t.to === s).map((t) => depth.get(t.from) ?? 0);
    if (from.length) depth.set(s, Math.max(...from) + 1);
  }
  return depth;
}

/** Everything reachable from `seeds` following `edges` in the given direction. */
function reachable(seeds, transitions, direction = 'forward') {
  const out = new Set(seeds);
  const queue = [...seeds];
  while (queue.length) {
    const at = queue.shift();
    for (const t of transitions) {
      const [from, to] = direction === 'forward' ? [t.from, t.to] : [t.to, t.from];
      if (from === at && !out.has(to)) {
        out.add(to);
        queue.push(to);
      }
    }
  }
  return out;
}

/**
 * @param root         project root
 * @param contracts    { schemas, operationIds, files } from the contract index,
 *                     so every cross-check resolves against what is really there
 */
export async function buildDomain(root, contracts = {}) {
  const problems = [];
  const schemas = list(contracts.schemas);
  const operationIds = contracts.operationIds ?? new Set();
  const contractFiles = list(contracts.files);

  // schema lookup keyed by the two things a state model names: contract + enum.
  // Every schema goes in, not only the ones carrying an enum, so a model that
  // names a schema which turns out to be an object can be told apart from one
  // that names nothing at all. The difference matters: the first is a model
  // anchored to the wrong thing, the second is a typo.
  const schemasByContract = new Map();
  for (const schema of schemas) {
    const contract = path.basename(schema.file ?? '', '.yaml');
    if (!schemasByContract.has(contract)) schemasByContract.set(contract, new Map());
    schemasByContract.get(contract).set(schema.name, schema);
  }

  // context name -> the contract that owns it
  const byBasename = new Map(
    contractFiles.map((f) => [path.basename(f.file ?? f, '.yaml'), f.file ?? f])
  );
  const resolveContext = (name) => {
    if (!name) return null;
    const direct = byBasename.get(name);
    if (direct) return direct;
    const alias = byBasename.get(CONTEXT_ALIASES[name] ?? '');
    if (alias) return alias;
    const prefixed = [...byBasename.keys()].filter((k) => k.startsWith(`${name}-`));
    return prefixed.length === 1 ? byBasename.get(prefixed[0]) : null;
  };

  // ---- events, read first so the state models can be checked against them ---
  const eventFiles = await readYamlDir(root, EVENTS_DIR);
  const events = [];
  for (const { rel, doc, error } of eventFiles) {
    if (error) {
      problems.push({ severity: 'error', kind: 'parse-error', file: rel, message: error });
      continue;
    }
    if (!doc?.name) continue;

    const consumers = list(doc.consumers).map((c) => ({
      context: c?.context ?? '',
      purpose: c?.purpose ?? '',
      idempotencyKey: c?.idempotencyKey ?? null,
      onFailure: c?.onFailure ?? null,
      isCritical: Boolean(c?.isCritical),
      contract: resolveContext(c?.context),
    }));

    // The rule the catalogue exists to enforce. An event nobody consumes is a
    // write nobody reads: either the consumer was never built, or the event
    // should not be published.
    if (!consumers.length) {
      problems.push({
        severity: 'error',
        kind: 'event-no-consumer',
        file: rel,
        message:
          `${doc.name} has no consumer. An event nobody consumes is a write nobody reads — ` +
          `either the consumer was never built, or the event should not be published.`,
      });
    }
    for (const consumer of consumers) {
      if (!consumer.idempotencyKey) {
        problems.push({
          severity: 'error',
          kind: 'event-no-idempotency-key',
          file: rel,
          message:
            `${doc.name} → ${consumer.context} declares no idempotencyKey. Delivery is ` +
            `at-least-once, so this consumer will process a duplicate, and the second time ` +
            `will be a Saturday.`,
        });
      }
      if (consumer.context && !consumer.contract) {
        problems.push({
          severity: 'warning',
          kind: 'event-unknown-context',
          file: rel,
          message: `${doc.name} is consumed by "${consumer.context}", which is not a contract`,
        });
      }
    }

    const publisherContract = resolveContext(doc.publisher);
    if (doc.publisher && !publisherContract) {
      problems.push({
        severity: 'warning',
        kind: 'event-unknown-context',
        file: rel,
        message: `${doc.name} is published by "${doc.publisher}", which is not a contract`,
      });
    }

    events.push({
      id: doc.name,
      name: doc.name,
      version: doc.version ?? 1,
      publisher: doc.publisher ?? null,
      publisherContract,
      domain: doc.domain ?? null,
      description: doc.description ?? '',
      aggregate: doc.aggregate ?? null,
      emittedWhen: doc.emittedWhen ?? null,
      payload: list(doc.payload).map((p) => ({
        field: p?.field ?? '',
        type: p?.type ?? '',
        required: p?.required !== false,
        notes: p?.notes ?? null,
      })),
      consumers,
      retention: doc.retention ?? null,
      notes: doc.notes ?? null,
      file: rel,
      emittedBy: [], // filled in from the state models below
      critical: consumers.filter((c) => c.isCritical).length,
    });
  }

  const eventsByName = new Map(events.map((e) => [e.name, e]));

  // ---- state models --------------------------------------------------------
  const stateFiles = await readYamlDir(root, STATES_DIR);
  const machines = [];

  for (const { rel, doc, error } of stateFiles) {
    if (error) {
      problems.push({ severity: 'error', kind: 'parse-error', file: rel, message: error });
      continue;
    }
    if (!doc?.entity) continue;

    const initial = list(doc.initial);
    const terminal = list(doc.terminal);
    const offline = list(doc.offlineReachable);

    const transitions = list(doc.transitions).map((t, i) => ({
      index: i,
      from: t?.from ?? '',
      to: t?.to ?? '',
      operation: t?.operation ?? null,
      trigger: t?.trigger ?? (t?.operation ? 'operation' : null),
      guard: t?.guard ?? '',
      isReversal: Boolean(t?.isReversal),
      requiresApproval: Boolean(t?.requiresApproval),
      emits: list(t?.emits),
    }));

    // every state the model mentions, in a stable order: initial first, then
    // as transitions introduce them, then terminal
    const names = [];
    const see = (s) => { if (s && !names.includes(s)) names.push(s); };
    initial.forEach(see);
    for (const t of transitions) { see(t.from); see(t.to); }
    terminal.forEach(see);

    // ---- against the contract enum ----------------------------------------
    // Two anchor shapes. The original names a top-level schema — `enum:
    // OrderStatus`. The 31 models written to close CF-88's inline-enum backlog
    // name a property inside one — `enum: Wallet.status` — because the values
    // live on the property, not on a schema of their own. Reading only the
    // first shape turned 31 correct models into errors saying they were
    // "checked against nothing", which is both false and the exact accusation
    // the file exists to make about real drift. describeProperties already
    // captures the values, so the fix is a lookup, not new data.
    const byName = schemasByContract.get(doc.contract ?? '');
    let schema = byName?.get(doc.enumSchema ?? doc.enum ?? '') ?? null;
    let enumValues = Array.isArray(schema?.enumValues) ? schema.enumValues : null;

    // An inline anchor points at a property, not a schema — the values live on
    // `Wallet.status`, not on a `WalletStatus` of its own. The package states
    // which it is (`enumKind: inline` with `enumSchema` and `enumProperty`), so
    // that is read first; the dotted string is parsed only as a fallback, for
    // the models written before the vocabulary existed.
    const inlineProperty =
      doc.enumProperty ??
      (doc.enumKind === 'inline' && doc.enum?.includes('.')
        ? doc.enum.slice(doc.enum.lastIndexOf('.') + 1)
        : null);

    if (inlineProperty) {
      const parent =
        byName?.get(doc.enumSchema ?? doc.enum.slice(0, doc.enum.lastIndexOf('.'))) ?? null;
      const property = (parent?.properties ?? []).find((p) => p.name === inlineProperty);
      if (property) {
        schema = { ...parent, inlineOn: property.name, dataType: property.type ?? null };
        enumValues = Array.isArray(property.enumValues) ? property.enumValues : null;
      } else {
        schema = null;
        enumValues = null;
      }
    }
    if (doc.enum && schemasByContract.size && !schema) {
      problems.push({
        severity: 'error',
        kind: 'state-unknown-enum',
        file: rel,
        message:
          `${doc.entity} models ${doc.contract}.${doc.enum}, which that contract does not declare. ` +
          `The model is unanchored: nothing stops it and the contract drifting apart.`,
      });
    } else if (schema && !enumValues) {
      problems.push({
        severity: 'error',
        kind: 'state-enum-is-not-an-enum',
        file: rel,
        message:
          `${doc.entity} models ${doc.contract}.${doc.enum}, but that schema is ` +
          `${schema.dataType ? `an ${schema.dataType}` : 'not an enum'} — it declares no values. ` +
          `Its ${names.length} states are checked against nothing, which is the one thing ` +
          `this file exists to prevent.`,
      });
    }
    if (enumValues) {
      for (const s of names) {
        if (!enumValues.includes(s)) {
          problems.push({
            severity: 'error',
            kind: 'state-not-in-enum',
            file: rel,
            message: `${doc.entity} moves through "${s}", which ${doc.contract}.${doc.enum} does not declare`,
          });
        }
      }
      for (const value of enumValues) {
        if (!names.includes(value)) {
          problems.push({
            severity: 'error',
            kind: 'enum-not-modelled',
            file: rel,
            message:
              `${doc.contract}.${doc.enum} declares "${value}" and the model never reaches it. ` +
              `A state in the enum and not the model is one nobody has thought about.`,
          });
        }
      }
    }

    // ---- reachability ------------------------------------------------------
    const fromInitial = reachable(initial, transitions, 'forward');
    const toTerminal = reachable(terminal, transitions, 'backward');
    for (const s of names) {
      if (!fromInitial.has(s)) {
        problems.push({
          severity: 'error',
          kind: 'state-unreachable',
          file: rel,
          message: `${doc.entity} can never reach "${s}" from ${initial.join(' or ') || 'any initial state'}`,
        });
      }
      if (terminal.length && !toTerminal.has(s)) {
        problems.push({
          severity: 'error',
          kind: 'state-traps',
          file: rel,
          message: `${doc.entity} in "${s}" can never reach a terminal state — records stop there`,
        });
      }
    }
    for (const s of offline) {
      if (!names.includes(s)) {
        problems.push({
          severity: 'error',
          kind: 'state-offline-unknown',
          file: rel,
          message: `${doc.entity} lists "${s}" as offline-reachable, but has no such state`,
        });
      }
    }

    // ---- transitions against the contracts and the catalogue ---------------
    for (const t of transitions) {
      t.operationKnown = !t.operation || !operationIds.size || operationIds.has(t.operation);
      if (!t.operationKnown) {
        problems.push({
          severity: 'error',
          kind: 'transition-unknown-operation',
          file: rel,
          message: `${doc.entity} ${t.from} → ${t.to} is caused by ${t.operation}, which no contract declares`,
        });
      }
      t.emitsKnown = [];
      for (const name of t.emits) {
        const known = eventsByName.has(name);
        t.emitsKnown.push({ name, known });
        if (!known) {
          problems.push({
            severity: 'error',
            kind: 'transition-unknown-event',
            file: rel,
            message:
              `${doc.entity} ${t.from} → ${t.to} publishes ${name}, which the event catalogue ` +
              `does not have. A consumer is waiting for a message that never arrives.`,
          });
        } else {
          eventsByName.get(name).emittedBy.push({
            entity: doc.entity,
            file: rel,
            from: t.from,
            to: t.to,
            operation: t.operation,
          });
        }
      }
    }

    const depth = computeDepths(names, transitions, initial);
    const outDegree = new Map(names.map((s) => [s, 0]));
    const inDegree = new Map(names.map((s) => [s, 0]));
    for (const t of transitions) {
      outDegree.set(t.from, (outDegree.get(t.from) ?? 0) + 1);
      inDegree.set(t.to, (inDegree.get(t.to) ?? 0) + 1);
    }

    const states = names.map((name) => ({
      name,
      initial: initial.includes(name),
      terminal: terminal.includes(name),
      offline: offline.includes(name),
      inEnum: !enumValues || enumValues.includes(name),
      unreachable: !fromInitial.has(name),
      traps: Boolean(terminal.length) && !toTerminal.has(name),
      depth: depth.get(name) ?? 0,
      out: outDegree.get(name) ?? 0,
      in: inDegree.get(name) ?? 0,
    }));

    machines.push({
      id: path.basename(rel, path.extname(rel)),
      entity: doc.entity,
      contract: doc.contract ?? null,
      contractFile: byBasename.get(doc.contract ?? '') ?? null,
      enum: doc.enum ?? null,
      enumId: schema?.id ?? null,
      enumValues,
      owner: doc.owner ?? null,
      ownerContract: resolveContext(doc.owner),
      // a domain lens this model is declared into, where the graph would miss it
      domain: doc.domain ?? null,
      file: rel,
      initial,
      terminal,
      offlineReachable: offline,
      states,
      transitions,
      notes: doc.notes ?? null,
      openQuestions: list(doc.openQuestions),
      stats: {
        states: states.length,
        transitions: transitions.length,
        reversals: transitions.filter((t) => t.isReversal).length,
        approvals: transitions.filter((t) => t.requiresApproval).length,
        emits: transitions.reduce((a, t) => a + t.emits.length, 0),
        automatic: transitions.filter((t) => t.trigger && t.trigger !== 'operation').length,
        offline: offline.length,
      },
    });
  }

  // an event nothing emits is the other half of the pairing — the catalogue
  // claims a fact that no state model produces
  for (const event of events) {
    if (event.emittedBy.length || !machines.length) continue;
    problems.push({
      severity: 'warning',
      kind: 'event-no-publisher',
      file: event.file,
      message:
        `${event.name} is catalogued and no state model emits it. Either the transition that ` +
        `publishes it is not written down, or it is published from somewhere the models do not cover.`,
    });
  }

  // ---- contexts ------------------------------------------------------------
  // The reason this is worth building: the contracts do not $ref each other at
  // all — every one of the 44 file-level links points at shared/. The real
  // coupling between bounded contexts runs through the outbox, and until now
  // there was nothing to draw it from.
  const contexts = new Map();
  const context = (name) => {
    if (!contexts.has(name)) {
      contexts.set(name, {
        name,
        contract: resolveContext(name),
        publishes: [],
        consumes: [],
        criticalIn: 0,
      });
    }
    return contexts.get(name);
  };

  const contextEdges = [];
  for (const event of events) {
    if (event.publisher) context(event.publisher).publishes.push(event.name);
    for (const consumer of event.consumers) {
      if (!consumer.context) continue;
      const target = context(consumer.context);
      target.consumes.push(event.name);
      if (consumer.isCritical) target.criticalIn += 1;
      if (!event.publisher || event.publisher === consumer.context) continue;
      contextEdges.push({
        from: event.publisher,
        to: consumer.context,
        fromContract: event.publisherContract,
        toContract: consumer.contract,
        event: event.name,
        critical: consumer.isCritical,
        onFailure: consumer.onFailure,
      });
    }
  }

  events.sort((a, b) => b.consumers.length - a.consumers.length || a.name.localeCompare(b.name));
  machines.sort((a, b) => b.transitions.length - a.transitions.length);

  // How many status enums exist across the contracts, against how many have a
  // model. The gap is the whole argument for states/ — quoting the count from
  // the schema's own prose would go stale the first time a contract changes.
  const statusEnums = [];
  for (const [contract, byName] of schemasByContract) {
    for (const [name, schema] of byName) {
      if (!Array.isArray(schema.enumValues) || !/(Status|State)$/.test(name)) continue;
      statusEnums.push({
        contract,
        name,
        values: schema.enumValues.length,
        modelled: machines.some((m) => m.contract === contract && m.enum === name),
      });
    }
  }
  statusEnums.sort((a, b) => b.values - a.values);

  const consumerCount = events.reduce((a, e) => a + e.consumers.length, 0);
  return {
    present: Boolean(machines.length || events.length),
    machines,
    events,
    contexts: [...contexts.values()].sort((a, b) => a.name.localeCompare(b.name)),
    contextEdges,
    statusEnums,
    problems,
    stats: {
      machines: machines.length,
      statusEnums: statusEnums.length,
      statusEnumsModelled: statusEnums.filter((e) => e.modelled).length,
      states: machines.reduce((a, m) => a + m.states.length, 0),
      transitions: machines.reduce((a, m) => a + m.transitions.length, 0),
      reversals: machines.reduce((a, m) => a + m.stats.reversals, 0),
      approvals: machines.reduce((a, m) => a + m.stats.approvals, 0),
      events: events.length,
      consumers: consumerCount,
      criticalConsumers: events.reduce((a, e) => a + e.critical, 0),
      contexts: contexts.size,
      contextEdges: contextEdges.length,
      emitted: events.filter((e) => e.emittedBy.length).length,
      payloadFields: events.reduce((a, e) => a + e.payload.length, 0),
    },
  };
}
