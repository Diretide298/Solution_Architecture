/**
 * The thirteen tools, and where each gets its answer.
 *
 * **Nine read the package.** They are selectors over bulk payloads, not
 * proxies: there is no `/api/screen?id=BO-102`, so a layer is fetched whole,
 * held against its ETag, and indexed into.
 *
 * | tool           | source                                                  |
 * |----------------|---------------------------------------------------------|
 * | adam_screen    | /api/journeys .screens                                   |
 * | adam_journey   | /api/journeys .flows                                     |
 * | adam_contract  | /api/index .nodes, then /api/detail?file= for the prose   |
 * | adam_table     | /api/backend .tables + .columns                          |
 * | adam_module    | /api/backend .modules + .tables                          |
 * | adam_service   | /api/diagrams .services, deepened by diagrams/detail      |
 * | adam_decisions | /api/decisions .adrs + .documents                        |
 * | adam_file      | /api/file, windowed by line                              |
 * | adam_search    | /api/search .entries                                     |
 *
 * **Four are about scheduled work**, and they go to the accounts service rather
 * than the package — uncached, because coordination changes while you are
 * looking at it. `adam_board` and `adam_work` read OpenProject live as the
 * caller. `adam_links` and `adam_link` read and write the one thing neither
 * system can hold on its own: which artefact a work package is about.
 *
 * **`adam_link` is the only tool here that writes**, and all it can write is
 * that row. Nothing here can change a work package, a status or an assignee —
 * OpenProject owns those, and a bridge that owned any of them would be the
 * second plan over the same work that CF-124 is already open about.
 *
 * Screens come from `journeys`, not from `uiux`. `/api/uiux` is about design
 * boards and frames — how much of the product is drawn — and holds no screen
 * records at all, so reading it for a screen returns nothing and presents as a
 * missing screen. That mistake cost a draft of the handoff.
 *
 * Every tool answers a miss with near names rather than a bare "not found". A
 * wrong id is nearly always a wrong *spelling* of a right id, and an agent
 * handed the candidates fixes it in the same turn instead of asking.
 */

const MAX_HITS = 25;

/** Case- and separator-insensitive: BO-102, bo102 and bo_102 are one name. */
const fold = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '');

/**
 * Ids that share a prefix with what was asked for, longest agreement first.
 *
 * Cheap, and on identifier-shaped names it beats an edit distance: BO-10 for
 * BO-102 is a truncation rather than a typo, and truncation is what an agent
 * working from a half-remembered id actually produces.
 */
function near(want, ids, limit = 8) {
  const w = fold(want);
  if (!w) return ids.slice(0, limit);
  const scored = [];
  for (const id of ids) {
    const f = fold(id);
    if (f.includes(w) || w.includes(f)) { scored.push([100, id]); continue; }
    let n = 0;
    while (n < f.length && n < w.length && f[n] === w[n]) n += 1;
    if (n >= 2) scored.push([n, id]);
  }
  return scored.sort((a, b) => b[0] - a[0]).slice(0, limit).map(([, id]) => id);
}

/**
 * Prose, shortened for a listing.
 *
 * `storageReason` explains why a table exists with no contract schema behind
 * it, and the package answers that at length: **160 fields across the 395
 * tables are over 2 KB, and every one of them is a storageReason** — the
 * largest, `access.entitlement`, is 25,450 characters. Returned whole in a list
 * of a module's tables they are the entire payload; one module came back at
 * 59 KB for eight tables.
 *
 * So a listing trims and says it has, and the single-record lookup that a
 * caller reached for on purpose keeps the whole thing.
 */
function trim(text, at = 300) {
  const s = String(text ?? '');
  if (s.length <= at) return s;
  // On a sentence end where there is one near the cut, so the fragment reads.
  const cut = s.lastIndexOf('. ', at);
  return `${s.slice(0, cut > at * 0.6 ? cut + 1 : at).trimEnd()} […${s.length - at} more characters]`;
}

function miss(what, want, ids) {
  const candidates = near(want, ids);
  return {
    found: false,
    error: `no ${what} called "${want}"`,
    ...(candidates.length ? { didYouMean: candidates } : { known: ids.length }),
  };
}

export const TOOLS = [
  {
    name: 'adam_screen',
    description:
      'One screen from the TICVAI package by id (e.g. BO-102, WEB-001): its module, purpose, '
      + 'platform, wave, permission, the API operations it calls, its states and navigation, and '
      + 'which journeys walk through it. Use when a screen id appears in a ticket, a contract or a '
      + 'conversation and you need to know what it actually is before writing code against it.',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string', description: 'Screen id, e.g. BO-102' } },
      required: ['id'],
    },
    async run(client, { id }) {
      const journeys = await client.layer('journeys');
      const screens = journeys.screens ?? [];
      const want = fold(id);
      const hit = screens.find((s) => fold(s.id) === want);
      if (!hit) return miss('screen', id, screens.map((s) => s.id));

      // Which flows walk through it. The screen record does not carry this —
      // the relationship is declared on the flow — and "what breaks if I change
      // this" is the first thing anybody asks about a screen.
      const usedByFlows = (journeys.flows ?? [])
        .filter((f) => (f.steps ?? []).some((step) => fold(step.screenId) === want))
        .map((f) => ({ id: f.id, name: f.name }));

      return { found: true, screen: hit, usedByFlows };
    },
  },

  {
    name: 'adam_journey',
    description:
      'One user journey / flow by id (e.g. F06): its actor, trigger, criticality, wave, the '
      + 'ordered steps with the screens and operations each touches, its branches and exit states, '
      + 'and any open questions recorded against it. Use to understand the path a change sits on '
      + 'rather than only the single screen in front of you.',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string', description: 'Flow id, e.g. F06' } },
      required: ['id'],
    },
    async run(client, { id }) {
      const journeys = await client.layer('journeys');
      const flows = journeys.flows ?? [];
      const hit = flows.find((f) => fold(f.id) === fold(id));
      if (!hit) return miss('journey', id, flows.map((f) => f.id));
      return { found: true, journey: hit };
    },
  },

  {
    name: 'adam_contract',
    description:
      'One OpenAPI contract by name (e.g. access, orders, catalogue). By default returns the map: '
      + 'title, version, every operation with its method and path, and the names of its schemas. '
      + 'Pass `schema` to get one schema in full with its properties, or `operation` for one '
      + 'operation with its description. Use before writing a client or a handler against a TICVAI '
      + 'API, so the operation ids and shapes are the real ones rather than remembered ones.',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Contract name or file, e.g. access or contracts/spine/access.yaml',
        },
        schema: {
          type: 'string',
          description: 'Optional: one schema by name, returned in full with its properties',
        },
        operation: {
          type: 'string',
          description: 'Optional: one operationId, returned with its full description',
        },
      },
      required: ['name'],
    },
    /**
     * Names by default, bodies on request.
     *
     * `contracts/spine/access.yaml` is 756 KB on disk. An earlier draft of this
     * tool returned every schema with its properties merged in and defaulted
     * that to on, which is a single tool result large enough to fill a context
     * window — the caller wanted one operation id and got the whole contract.
     * So the default answer is the map, and a second call fetches the one thing
     * the map named.
     */
    async run(client, { name, schema: wantSchema, operation: wantOperation }) {
      const index = await client.layer('index');
      const nodes = index.nodes ?? [];
      const files = [...new Set(nodes.map((n) => n.file).filter(Boolean))];

      const want = fold(name);
      // Whole path first, then the basename without its extension, so both
      // "access" and "contracts/spine/access.yaml" land on the same file.
      const stem = (f) => fold(String(f).split('/').pop().replace(/\.(ya?ml|json)$/i, ''));
      const file = files.find((f) => fold(f) === want) ?? files.find((f) => stem(f) === want);
      if (!file) return miss('contract', name, files.map((f) => String(f).split('/').pop()));

      const mine = nodes.filter((n) => n.file === file);
      const operations = mine.filter((n) => n.type === 'operation');
      const schemas = mine.filter((n) => n.type === 'schema');
      const self = mine.find((n) => n.type === 'file');

      // Detail is a nicety, not the answer: an enum-only contract has nothing
      // held back, and a failure to fetch it should not lose the operations.
      // Only fetched when something is being returned in full — on the map path
      // it would be a megabyte read whose result is thrown away.
      const wantOne = wantSchema || wantOperation;
      const detail = wantOne ? await client.detail(file).catch(() => ({})) : {};

      if (wantSchema) {
        const hit = schemas.find((n) => fold(n.name) === fold(wantSchema));
        if (!hit) return miss(`schema in ${file}`, wantSchema, schemas.map((n) => n.name));
        return { found: true, contract: file, schema: { ...hit, ...(detail[hit.id] ?? {}) } };
      }

      if (wantOperation) {
        const hit = operations.find((n) => fold(n.name) === fold(wantOperation));
        if (!hit) return miss(`operation in ${file}`, wantOperation, operations.map((n) => n.name));
        return { found: true, contract: file, operation: { ...hit, ...(detail[hit.id] ?? {}) } };
      }

      return {
        found: true,
        contract: {
          file,
          title: self?.title ?? null,
          version: self?.version ?? null,
          // Operations carry a one-line summary and are the thing callers come
          // for, so they come back whole. Their prose does not — that is what
          // `operation` is for.
          operations: operations.map((o) => ({
            operationId: o.name,
            method: o.method,
            path: o.path,
            summary: o.title,
          })),
          schemaNames: schemas.map((n) => n.name),
        },
        next: 'pass `schema` or `operation` with one of the names above to see it in full',
      };
    },
  },

  {
    name: 'adam_table',
    description:
      'One database table by name (e.g. access.entitlement or entitlement): its module, the '
      + 'contract schema it was derived from, its columns, its foreign keys, the migration that '
      + 'creates it and the service that owns it. Use before writing a query or a migration '
      + 'against the TICVAI data model.',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Table name, with or without its module prefix',
        },
      },
      required: ['name'],
    },
    async run(client, { name }) {
      const backend = await client.layer('backend');
      const tables = backend.tables ?? [];
      if (!tables.length) {
        return { found: false, error: 'the backend workbook is not present in this package' };
      }
      // `name` already carries its schema — the record is
      // { module: 'access', name: 'access.entitlement' } — so the two must
      // never be joined. An earlier draft offered `${t.module}.${t.name}` as
      // the candidate spelling and printed `access.access.entitlement`, a name
      // that exists nowhere and that a caller would then paste back.
      const want = fold(name);
      // The last dot-segment, so `entitlement` finds `access.entitlement`.
      // Taken off the raw name, because `fold` has already eaten the dots by
      // the time a regex could look for one — which is exactly how the previous
      // attempt at this became dead code that always missed.
      const tail = (s) => fold(String(s).split('.').pop());

      const exact = tables.find((t) => fold(t.name) === want);
      if (!exact) {
        const byTail = tables.filter((t) => tail(t.name) === want);
        // One module's `entitlement` is not another's. Guessing between them
        // would hand back a column list for the wrong table, which is worse
        // than asking.
        if (byTail.length > 1) {
          return {
            found: false,
            error: `"${name}" names ${byTail.length} tables — say which`,
            didYouMean: byTail.map((t) => t.name),
          };
        }
        if (!byTail.length) return miss('table', name, tables.map((t) => t.name));
        return { found: true, table: byTail[0], columns: (backend.columns ?? {})[byTail[0].name] ?? [] };
      }

      // `columns` is keyed by the table's own `name`, prefix and all.
      return {
        found: true,
        table: exact,
        columns: (backend.columns ?? {})[exact.name] ?? [],
      };
    },
  },

  {
    name: 'adam_search',
    description:
      'Search the whole package at once — screens, flows, contracts, operations, schemas, tables, '
      + 'state machines, decisions — by name or id fragment. Returns each hit with its kind and the '
      + 'file and line it lives at. Use first when you have a name and do not yet know what kind of '
      + 'thing it is.',
    inputSchema: {
      type: 'object',
      properties: {
        q: { type: 'string', description: 'What to look for' },
        kind: {
          type: 'string',
          description: 'Optional: restrict to one kind, e.g. screen, flow, table',
        },
        limit: { type: 'integer', description: `Max hits to return, default ${MAX_HITS}` },
      },
      required: ['q'],
    },
    async run(client, { q, kind, limit }) {
      const search = await client.layer('search');
      const entries = search.entries ?? [];
      const want = fold(q);
      if (!want) return { found: false, error: 'give me something to look for' };

      const pool = kind ? entries.filter((e) => fold(e.kind) === fold(kind)) : entries;
      const hits = [];
      for (const e of pool) {
        const hay = fold(`${e.id} ${e.name} ${e.terms ?? ''}`);
        if (!hay.includes(want)) continue;
        // An exact id beats an exact name beats a substring of somebody's prose.
        hits.push([fold(e.id) === want ? 0 : fold(e.name) === want ? 1 : 2, e]);
      }
      hits.sort((a, b) => a[0] - b[0]);
      const cap = Math.max(1, Math.min(Number(limit) || MAX_HITS, 100));

      // How many hits of each kind, across the whole result and not just the
      // page being returned. An earlier draft put the *corpus* vocabulary in a
      // field called `kinds`, which reads as a description of the hits and is
      // not one: a caller could see `table` there, ask for the first table in
      // the list, and find none — because the tables were all past the cap.
      const byKind = {};
      for (const [, e] of hits) byKind[e.kind] = (byKind[e.kind] ?? 0) + 1;

      return {
        found: hits.length > 0,
        total: hits.length,
        showing: Math.min(hits.length, cap),
        kinds: byKind,
        ...(hits.length > cap
          ? { note: 'more hits than shown — raise `limit`, or narrow with `kind`' }
          : {}),
        // The vocabulary, offered only when nothing matched: that is the moment
        // a caller needs to know what kinds exist rather than guess again.
        ...(hits.length ? {} : { kindsAvailable: [...new Set(entries.map((e) => e.kind))].sort() }),
        hits: hits.slice(0, cap).map(([, e]) => ({
          kind: e.kind,
          id: e.id,
          name: e.name,
          sub: e.sub,
          layer: e.layer,
          file: e.file,
          line: e.line,
        })),
      };
    },
  },
  {
    name: 'adam_service',
    description:
      'What ships together. With no argument, lists all 16 deployable services with their tier, '
      + 'operation and table counts, and flow coverage. Pass `name` for one service in depth — the '
      + 'schemas it owns, why it is its own service, how it scales, what happens when it is down, '
      + 'and its operations by contract. Add `operations: true` for the full operation list with '
      + 'verbs, paths, permissions and offline flags. Use before deciding where a change belongs.',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Service name, e.g. FnbService or fnb' },
        operations: {
          type: 'boolean',
          description: 'Include every operation in full. Default false — the list is long.',
        },
      },
    },
    /**
     * Two sources, deliberately. `/api/diagrams` carries a 16-row summary that
     * is enough to choose between services; `diagrams/detail` carries the one
     * file, which is 28 KB of YAML for the largest. Listing from the first and
     * deepening from the second keeps the common call small.
     */
    async run(client, { name, operations = false }) {
      const diagrams = await client.layer('diagrams');
      const services = diagrams.services ?? [];
      if (!services.length) return { found: false, error: 'this package describes no services' };

      if (!name) {
        return {
          found: true,
          total: services.length,
          tiers: diagrams.tiers ?? null,
          services: services.map((s) => ({
            name: s.name,
            tier: s.tier,
            operations: s.operations,
            tables: s.tables,
            schemas: s.schemas,
            flowCoverage: s.flowCoverage,
          })),
          next: 'pass `name` for one service in depth',
        };
      }

      const want = fold(name);
      const hit = services.find((s) => fold(s.name) === want)
        ?? services.find((s) => fold(s.key) === want)
        // `fnb` for `FnbService`, which is how people say it out loud.
        ?? services.find((s) => fold(s.name) === `${want}service`);
      if (!hit) return miss('service', name, services.map((s) => s.name));

      // The low-level file. Absent is not an error — the summary is a real
      // answer on its own, and a package mid-derivation can have one and not
      // the other.
      const lld = await client.diagram('services', hit.name).catch(() => null);
      const doc = lld?.doc ?? lld?.body ?? lld ?? null;

      const byContract = (doc?.operationsByContract ?? []).map((c) => ({
        contract: c.contract,
        count: c.count,
        ...(operations ? { operations: c.operations } : {}),
      }));

      return {
        found: true,
        service: {
          ...hit,
          why: doc?.why ?? hit.why ?? null,
          scale: doc?.scale ?? hit.scale ?? null,
          ifDown: doc?.ifDown ?? hit.ifDown ?? null,
          coverage: doc?.coverage ?? null,
          schemas: doc?.schemas ?? hit.schemas ?? null,
          operationsByContract: byContract,
        },
        ...(operations ? {} : { next: 'add `operations: true` for the full operation list' }),
      };
    },
  },

  {
    name: 'adam_module',
    description:
      'A data-model module — a schema and the tables in it. With no argument, lists every module '
      + 'with its table and column counts, its tier, which contract defines it and which service '
      + 'owns it. Pass `name` for one, with its tables. Use to find out what a schema holds before '
      + 'writing against it, or which service owns a piece of data.',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Module name, e.g. access or fnb' },
      },
    },
    /**
     * No new server route. The handoff listed `module` as missing; it is not —
     * `/api/backend` has carried `modules` all along, and its records are richer
     * than `handoff/modules.json` (they add `writtenTables`, `migration` and
     * `status`). Building a second source for it would have been a second answer
     * to a question the package had already answered.
     */
    async run(client, { name }) {
      const backend = await client.layer('backend');
      const modules = backend.modules ?? [];
      if (!modules.length) {
        return { found: false, error: 'the backend workbook is not present in this package' };
      }

      if (!name) {
        return {
          found: true,
          total: modules.length,
          modules: modules.map((m) => ({
            name: m.name,
            tier: m.tier,
            tables: m.tables,
            columns: m.columns,
            contract: m.contract,
            what: m.what,
          })),
          next: 'pass `name` for one module and its tables',
        };
      }

      const want = fold(name);
      const hit = modules.find((m) => fold(m.name) === want);
      if (!hit) return miss('module', name, modules.map((m) => m.name));

      // Its tables, by the prefix they carry. A table's `name` is already
      // `access.entitlement` — module and name are never joined, for the reason
      // written on adam_table.
      const mine = (backend.tables ?? []).filter((t) => t.module === hit.name);

      return {
        found: true,
        module: hit,
        tables: mine.map((t) => ({
          name: t.name,
          columns: t.columns,
          derivedFrom: t.derivedFrom,
          service: t.service,
          migration: t.migration,
          ...(t.storageOnly
            ? { storageOnly: true, storageReason: trim(t.storageReason) }
            : {}),
        })),
        next: 'pass one of those names to adam_table for its columns, keys and the whole reason',
      };
    },
  },

  {
    name: 'adam_board',
    description:
      'What is open and assigned to you in OpenProject, and which package artefacts each item '
      + 'touches. Use at the start of a session to see what you are meant to be doing, or when a '
      + 'branch name or a ticket number turns up and you need the context behind it.',
    inputSchema: { type: 'object', properties: {} },
    async run(client) {
      const answer = await client.service('/api/board/mine');
      // 428 is "connect OpenProject first" — a thing to go and do, not a
      // failure. Relayed as the sentence the server wrote rather than flattened
      // into "the tool failed".
      if (answer.status === 428) {
        return { found: false, needsSetup: true, error: answer.data?.detail };
      }
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };

      const board = answer.data;
      return {
        found: board.total > 0,
        total: board.total,
        // Kept, because an empty board reads as "nothing assigned to me" and
        // the truth may be "nothing has been loaded into the project yet".
        ...(board.note ? { note: board.note } : {}),
        items: board.items,
      };
    },
  },

  {
    name: 'adam_work',
    description:
      'One OpenProject work package by number, read live, with the package artefacts it is '
      + 'recorded as touching. Use when a ticket number appears in a branch, a commit or a '
      + 'conversation and you need to know what it is about — including which screens, tables and '
      + 'services it involves, which OpenProject itself cannot tell you.',
    inputSchema: {
      type: 'object',
      properties: {
        key: { type: 'string', description: 'Work package number, e.g. 6046 or #6046' },
      },
      required: ['key'],
    },
    async run(client, { key }) {
      const answer = await client.service(`/api/work-packages/${String(key).replace(/^#/, '')}`);
      if (answer.status === 428) {
        return { found: false, needsSetup: true, error: answer.data?.detail };
      }
      if (answer.status === 404) return { found: false, error: `no work package #${key}` };
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      return { found: true, ...answer.data };
    },
  },

  {
    name: 'adam_links',
    description:
      'What work is scheduled against one package artefact — the OpenProject work packages '
      + 'recorded as being about this screen, table, contract or service. Use before changing an '
      + 'artefact, to see whether somebody already has a ticket open on it.',
    inputSchema: {
      type: 'object',
      properties: {
        kind: {
          type: 'string',
          description: 'screen, flow, contract, operation, schema, table, module, service, adr, platform',
        },
        id: { type: 'string', description: 'The artefact id, e.g. BO-102 or access.entitlement' },
      },
      required: ['kind', 'id'],
    },
    async run(client, { kind, id }) {
      const query = new URLSearchParams({ target_kind: String(kind).toLowerCase(), target_id: id });
      const answer = await client.service(`/api/links?${query}`);
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };

      const { total, links } = answer.data;
      return {
        found: total > 0,
        total,
        // Not "nothing is happening" — nobody has *said* anything is. The
        // difference matters when an agent is deciding whether to open a ticket.
        ...(total ? {} : { note: `Nothing is recorded against ${kind} ${id}. That means nobody has linked one, not that no work exists.` }),
        // Every status here is a copy of what OpenProject said at syncedAt.
        // Labelled, so a stale one is never read as current.
        links: links.map((l) => ({
          workPackage: l.key,
          url: l.url,
          asOfLastSync: l.cached,
          linkId: l.id,
        })),
      };
    },
  },

  {
    name: 'adam_link',
    description:
      'Record that an OpenProject work package is about a package artefact — a screen, table, '
      + 'contract, service or ADR. **This writes.** Use when you have worked out what a ticket '
      + 'actually touches and that knowledge would otherwise be lost: OpenProject cannot express '
      + 'it, and the package does not know the schedule. Set `remove: true` with a `linkId` from '
      + 'adam_links to take one back.',
    inputSchema: {
      type: 'object',
      properties: {
        kind: {
          type: 'string',
          description: 'screen, flow, contract, operation, schema, table, module, service, adr, platform',
        },
        id: { type: 'string', description: 'The artefact id, e.g. BO-102' },
        key: { type: 'string', description: 'Work package number, e.g. 6046' },
        remove: { type: 'boolean', description: 'Remove a link instead. Needs `linkId`.' },
        linkId: { type: 'integer', description: 'From adam_links, when removing' },
      },
    },
    /**
     * The first tool here that changes anything, and the change is deliberately
     * small: a row saying two things are about each other. It cannot alter a
     * work package, a status or an assignee — OpenProject owns those, and a
     * bridge that owned any of them would be the second plan over the same work
     * that `delivery-plan-vs-package.md` already has open as CF-124.
     */
    async run(client, { kind, id, key, remove = false, linkId }) {
      if (remove) {
        if (!linkId) return { found: false, error: 'give me the linkId to remove — adam_links has them' };
        const gone = await client.service(`/api/links/${linkId}`, { method: 'DELETE' });
        if (!gone.ok) return { found: false, error: gone.data?.detail ?? `HTTP ${gone.status}` };
        return { ok: true, ...gone.data };
      }

      if (!kind || !id || !key) {
        return { found: false, error: 'linking needs a kind, an artefact id and a work package number' };
      }

      const answer = await client.service('/api/links', {
        method: 'POST',
        body: {
          target_kind: String(kind).toLowerCase(),
          target_id: id,
          external_key: String(key).replace(/^#/, ''),
        },
      });

      if (answer.status === 428) {
        return { ok: false, needsSetup: true, error: answer.data?.detail };
      }
      // Already said. The state asked for is the state that exists, so this is
      // reported as done rather than as a failure to be retried.
      if (answer.status === 409) {
        return { ok: true, alreadyLinked: true, note: answer.data?.detail };
      }
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };

      return {
        ok: true,
        linked: answer.data.linked,
        workPackage: answer.data.workPackage,
      };
    },
  },

  {
    name: 'adam_decisions',
    description:
      'The architecture decisions behind TICVAI — the ADRs, the registers and the conflict log. '
      + 'With no argument, lists every ADR with its status and what superseded it. Pass `id` '
      + '(e.g. ADR-0038 or 0038) for one in full, or `q` to search titles and subjects. '
      + '**Read this before proposing an architectural change**: an ADR records the options that '
      + 'were rejected and why, and contradicting one already decided is the most expensive '
      + 'mistake available here.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'One ADR, e.g. ADR-0038 or 0038' },
        q: { type: 'string', description: 'Search ADR titles and what they constrain' },
      },
    },
    async run(client, { id, q }) {
      // A client account is refused this route by lib/audience.mjs, and that
      // refusal arrives here as Forbidden and is reported as such — deliberately
      // not softened into an empty list, which would read as "no decisions".
      const decisions = await client.layer('decisions');
      const adrs = decisions.adrs ?? [];
      if (!adrs.length) return { found: false, error: 'this package records no decisions' };

      const label = (a) => `ADR-${String(a.id).padStart(4, '0')}`;

      if (id) {
        const want = fold(id).replace(/^adr/, '');
        const hit = adrs.find((a) => fold(String(a.id)).replace(/^0+/, '') === want.replace(/^0+/, ''));
        if (!hit) return miss('ADR', id, adrs.map(label));
        return {
          found: true,
          adr: hit,
          // The record carries the fields, not the argument. The reasoning is
          // the prose, and the prose is a file.
          fullText: `call adam_file with path "${hit.file}" to read the reasoning`,
        };
      }

      const listing = adrs
        .filter((a) => !q || fold(`${a.id} ${a.title} ${(a.constrains ?? []).join(' ')}`).includes(fold(q)))
        .map((a) => ({
          id: label(a),
          title: a.title,
          status: a.status,
          date: a.date,
          // The case that misleads: Accepted *and* partly superseded reads as
          // current in a list and is not current in the part that matters.
          ...(a.supersededBy ? { supersededBy: a.supersededBy } : {}),
          ...(a.partlySuperseded ? { partlySuperseded: true } : {}),
        }));

      return {
        found: listing.length > 0,
        ...(q ? { matching: q } : {}),
        total: listing.length,
        adrs: listing,
        registers: (decisions.documents ?? [])
          .filter((d) => d.group === 'register')
          .map((d) => ({ id: d.id, title: d.title, file: d.file, rows: d.rows })),
        next: 'pass `id` for one ADR, or adam_file with its path for the reasoning',
      };
    },
  },

  {
    name: 'adam_file',
    description:
      'One file from the package as source — a contract YAML, an ADR, a register, a handoff note. '
      + 'Use when you want what was written rather than what was derived from it: the argument in '
      + 'an ADR, or the exact YAML behind a contract. Paths come from the other tools, which return '
      + 'a `file` on nearly every record.',
    inputSchema: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: 'Path within the package, e.g. docs/adr/0038-....md or contracts/spine/access.yaml',
        },
        from: { type: 'integer', description: 'First line to return, 1-based. Default 1.' },
        lines: { type: 'integer', description: 'How many lines. Default 400.' },
      },
      required: ['path'],
    },
    /**
     * Windowed, because a contract is 756 KB and the result ceiling is 120 KB.
     * A file that arrives as a refusal teaches nothing; one that arrives as its
     * first 400 lines with a note saying how many there are lets the caller ask
     * for the part it wants.
     */
    async run(client, { path, from = 1, lines = 400 }) {
      const answer = await client.file(path);
      if (!answer.ok) {
        return {
          found: false,
          status: answer.status,
          error: answer.status === 404 ? `no file at "${path}"`
            : answer.status === 400 ? `"${path}" is not a readable kind — .yaml .md .json .csv .sql only`
            : answer.text.slice(0, 300),
        };
      }
      const all = answer.text.split('\n');
      const start = Math.max(1, Number(from) || 1);
      const count = Math.max(1, Math.min(Number(lines) || 400, 2000));
      const slice = all.slice(start - 1, start - 1 + count);
      const end = start + slice.length - 1;

      return {
        found: true,
        path,
        totalLines: all.length,
        showing: `${start}-${end}`,
        ...(end < all.length
          ? { more: `${all.length - end} lines below — call again with from: ${end + 1}` }
          : {}),
        text: slice.join('\n'),
      };
    },
  },
];

export const BY_NAME = new Map(TOOLS.map((t) => [t.name, t]));
