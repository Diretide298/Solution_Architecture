/**
 * The twenty-two tools, and where each gets its answer.
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
 * **Three are about doing the work.** `adam_pull` saves a ticket and everything
 * it is linked to as files under `.adam/` in the developer's folder, so Claude
 * reads what it needs from disk instead of holding it all in the conversation.
 * `adam_propose` works out a change to a work package — status, % done, a
 * comment — and sends nothing; `adam_apply` sends it, with the code the proposal
 * returned, after the person has said yes. The change is made as the person,
 * with their own OpenProject token. Assignees, dates and the work packages
 * themselves stay OpenProject's alone (CF-124).
 *
 * **Three are about the package being wrong.** `adam_changes` lists and reads
 * change requests; `adam_draft_change` drafts one when the package contradicts
 * itself or lacks what a ticket needs, and files nothing; `adam_raise_change`
 * files the draft after the person has said yes. Settling one is done by people
 * on ADAM's Changes page, never from here.
 *
 * **Three are about testing, and one of them is not a tool at all.** Every ten
 * tickets a person closes, the next close is refused until that batch has been
 * tested and a *teammate* has said so. `adam_testing` reads where that stands,
 * `adam_submit_batch` records what was run, `adam_check_batch` passes or fails
 * somebody else's. **The gate itself is not here** — it is in the service, on
 * the route that closes a ticket, which is the only place it can be a rule
 * rather than an instruction an agent is free to reinterpret. These three help
 * explain and clear it, and none of them can route around it.
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

import { execFile } from 'node:child_process';
import { appendFile, mkdir, readdir, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { promisify } from 'node:util';

const run = promisify(execFile);

const MAX_HITS = 25;

/**
 * What the working tree is at, if this is a repository at all.
 *
 * **The one thing this process can see that the service cannot.** ADAM has no
 * access to anybody's repository, so "you have closed five tickets without
 * committing" is only answerable because the connector runs on the machine
 * where the work happens and can ask git.
 *
 * Everything about it is best-effort. Not a repository, no git on the PATH, a
 * repository with no commits yet — all of them answer with nothing, and the
 * service simply says less. It must never be the reason an apply fails: the
 * ticket is closed either way, and a tool that refused to record that because
 * `git` was missing would be trading the important thing for the incidental one.
 */
async function treeState(dir) {
  const cwd = path.resolve(String(dir || process.env.ADAM_WORKDIR || process.cwd()));
  try {
    const [head, status] = await Promise.all([
      run('git', ['rev-parse', 'HEAD'], { cwd, timeout: 4000 }),
      run('git', ['status', '--porcelain'], { cwd, timeout: 4000 }),
    ]);
    return {
      head: head.stdout.trim(),
      // Anything at all: staged, unstaged or untracked. The question is "is
      // there work here that is not in a commit", and all three answer yes.
      dirty: status.stdout.trim().length > 0,
    };
  } catch {
    return { head: '', dirty: false };
  }
}

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

/**
 * The query string for a work call, carrying the package this connector works
 * in. Each ADAM project reads its own OpenProject project, so the accounts
 * service has to be told which one; without it, it assumes the first.
 */
async function scoped(client, extra = {}) {
  const project = await client.projectId();
  return new URLSearchParams({ ...extra, ...(project ? { project_id: project } : {}) });
}

// ---- files under .adam/ ------------------------------------------------------

/** A name that is safe as one path segment, whatever an artefact id holds. */
const safeName = (text) => String(text ?? '').replace(/[^A-Za-z0-9._-]+/g, '_')
  .replace(/^\.+/, '_').slice(0, 120) || '_';

/**
 * Where `.adam/` goes: the folder Claude is working in.
 *
 * `dir` from the call first, because Claude knows its own working folder and a
 * server started by Claude Code may not have been started in it. Then
 * ADAM_WORKDIR, which setup sets for a folder registration. Then the process's
 * own folder. Never a drive root, and never a folder that does not exist.
 */
async function workFolder(dir) {
  const chosen = path.resolve(String(dir || process.env.ADAM_WORKDIR || process.cwd()));
  if (path.parse(chosen).root === chosen) {
    throw new Error(`will not write into ${chosen} — pass dir: the folder you are working in`);
  }
  const found = await stat(chosen).catch(() => null);
  if (!found?.isDirectory()) throw new Error(`there is no folder at ${chosen}`);
  const base = path.join(chosen, '.adam');
  await mkdir(base, { recursive: true });
  // Pulled copies, not source. Kept out of git without touching the repo's own
  // .gitignore.
  await writeFile(path.join(base, '.gitignore'),
    '# Written by the ADAM connector. Local copies only - never commit them.\n*\n');
  return base;
}

// Kept across pulls: the developer's own notes and the log of applied changes.
const KEEP = new Set(['notes.md', 'log.md']);

/** Which tool answers for each kind of linked artefact, and with what. */
function lookupFor(kind, id) {
  // operation and schema ids name their contract: `access#listPasses`,
  // `access:Pass`. Without one there is nothing to aim at but a search.
  const ref = /^(.+)[#:](.+)$/.exec(String(id));
  switch (kind) {
    case 'screen': return ['adam_screen', { id }];
    case 'flow': return ['adam_journey', { id }];
    case 'contract': return ['adam_contract', { name: id }];
    case 'operation': return ref ? ['adam_contract', { name: ref[1], operation: ref[2] }] : ['adam_search', { q: id }];
    case 'schema': return ref ? ['adam_contract', { name: ref[1], schema: ref[2] }] : ['adam_search', { q: id }];
    case 'table': return ['adam_table', { name: id }];
    case 'module': return ['adam_module', { name: id }];
    case 'service': return ['adam_service', { name: id }];
    case 'adr': return ['adam_decisions', { id }];
    default: return ['adam_search', { q: id }];
  }
}

const json = (value) => `${JSON.stringify(value, null, 2)}\n`;

function ticketReadme(wp, files, missing, when, decisions = []) {
  const line = (label, value) => (value || value === 0 ? `- **${label}:** ${value}\n` : '');
  let out = `# #${wp.key} ${wp.subject}\n\n`;
  out += line('Project', wp.project) + line('Type', wp.type) + line('Status', wp.status)
    + line('Milestone', wp.version) + line('Priority', wp.priority) + line('Assignee', wp.assignee)
    + line('Start', wp.startDate) + line('Due', wp.dueDate)
    + line('% done', wp.percentDone) + line('OpenProject', wp.url);
  out += `\nPulled ${when} by the ADAM connector. Status and dates are a copy from then; `
    + 'run adam_pull again for the current ones.\n\n';
  out += `## Description\n\n${wp.description || '_No description in OpenProject._'}\n`;
  if (wp.descriptionTrimmed) out += '\n_Longer in OpenProject - open the link above for the rest._\n';
  out += `\n## What this touches (${files.length})\n\n`;
  if (files.length) {
    for (const f of files) out += `- ${f.kind} \`${f.id}\` - [${f.file}](${f.file})\n`;
  } else {
    out += 'Nothing is linked to this ticket yet. Find what it is about with adam_search, record it '
      + 'with adam_link, then run adam_pull again.\n';
  }
  if (decisions.length) {
    out += `\nDecisions linked but not pulled: ${decisions.map((d) => `\`${d}\``).join(', ')}. `
      + 'Ask adam_decisions if the build needs one.\n';
  }
  if (missing.length) {
    out += `\nLinked but not found in the package: ${missing.map((m) => `${m.kind} \`${m.id}\``).join(', ')}.\n`;
  }
  out += '\n## When you have finished\n\n'
    + 'Ask Claude to propose the change (adam_propose): the new status, % done, and a comment '
    + 'saying what was done. Check what it shows you, then say yes to apply it (adam_apply). '
    + 'Applied changes are listed in [log.md](log.md). Your own notes go in [notes.md](notes.md) - '
    + 'pulling again keeps both.\n';
  return out;
}

async function pullOne(client, key, base, when) {
  const answer = await client.service(`/api/work-packages/${encodeURIComponent(key)}?${await scoped(client)}`);
  if (answer.status === 428) return { key, needsSetup: true, error: answer.data?.detail };
  if (!answer.ok) return { key, error: answer.data?.detail ?? `HTTP ${answer.status}` };
  const { workPackage: wp, touches = [] } = answer.data;

  const folder = path.join(base, 'work', safeName(wp.key));
  await mkdir(folder, { recursive: true });
  // What an earlier pull wrote goes, so an unlinked artefact does not linger.
  for (const name of await readdir(folder)) {
    if (!KEEP.has(name)) await rm(path.join(folder, name), { recursive: true, force: true });
  }

  const files = [];
  const missing = [];
  // Decisions are not pulled: building a ticket needs the contracts and tables
  // it touches, and an ADR is background that adam_decisions answers on demand.
  const decisions = touches.filter((t) => t.kind === 'adr').map((t) => t.id);
  for (const { kind, id } of touches) {
    if (kind === 'adr') continue;
    const [toolName, args] = lookupFor(kind, id);
    const result = await BY_NAME.get(toolName).run(client, args).catch((error) => ({ found: false, error: error.message }));
    const file = `${safeName(kind)}-${safeName(id)}.json`;
    await writeFile(path.join(folder, file), json({ kind, id, from: toolName, ...result }));
    if (result.found === false) missing.push({ kind, id });
    files.push({ kind, id, file });
  }

  await writeFile(path.join(folder, 'ticket.json'), json({ pulledAt: when, workPackage: wp, touches }));
  await writeFile(path.join(folder, 'README.md'), ticketReadme(wp, files, missing, when, decisions));
  const notes = path.join(folder, 'notes.md');
  if (!(await stat(notes).catch(() => null))) {
    await writeFile(notes, `# Notes on #${wp.key}\n\nYours. adam_pull never overwrites this file.\n`);
  }
  return {
    key: wp.key, subject: wp.subject, status: wp.status, milestone: wp.version || null,
    due: wp.dueDate || null, folder, linked: files.length, notFound: missing.length,
  };
}

function boardReadme(pulled, project, when) {
  const groups = new Map();
  for (const t of pulled.filter((t) => !t.error)) {
    const name = t.milestone || 'No milestone';
    if (!groups.has(name)) groups.set(name, []);
    groups.get(name).push(t);
  }
  let out = `# My board - ${project?.name ?? 'OpenProject'}\n\nPulled ${when}. Open work assigned to you, `
    + 'grouped by milestone. Each ticket has a folder under work/ with its description and '
    + 'everything it is linked to.\n';
  for (const [name, tickets] of groups) {
    out += `\n## ${name}\n\n| Ticket | Status | Due | Linked | Folder |\n|---|---|---|---|---|\n`;
    for (const t of tickets) {
      out += `| #${t.key} ${t.subject.replace(/\|/g, '/')} | ${t.status} | ${t.due ?? ''} | ${t.linked} | [work/${safeName(t.key)}](work/${safeName(t.key)}/README.md) |\n`;
    }
  }
  const failed = pulled.filter((t) => t.error);
  if (failed.length) out += `\n## Not pulled\n\n${failed.map((t) => `- #${t.key}: ${t.error}`).join('\n')}\n`;
  return out;
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
      const answer = await client.service(`/api/board/mine?${await scoped(client)}`);
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
        // Which OpenProject project this board is read from, so "nothing
        // assigned" is never mistaken for "nothing assigned anywhere".
        ...(board.openproject ? { openprojectProject: board.openproject } : {}),
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
      const answer = await client.service(
        `/api/work-packages/${String(key).replace(/^#/, '')}?${await scoped(client)}`);
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
      const query = await scoped(client, { target_kind: String(kind).toLowerCase(), target_id: id });
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
          project_id: (await client.projectId()) ?? '',
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

  {
    name: 'adam_pull',
    description:
      'Save a ticket and everything it is linked to as files in the working folder, under '
      + '.adam/work/<ticket>/: README.md (the ticket, its milestone and description, and a list of '
      + 'the files), ticket.json, one file per linked screen, journey, contract, table, service, '
      + 'and module (linked ADRs are listed, not pulled), plus notes.md for your own notes. With no `key`, pulls '
      + 'every open ticket assigned to you and writes .adam/board.md grouped by milestone. **Use '
      + 'this at the start of work on a ticket**, then read the files you need instead of holding '
      + 'everything in the conversation. Always pass `dir`: the absolute path of the folder you are '
      + 'working in. .adam/ is git-ignored.',
    inputSchema: {
      type: 'object',
      properties: {
        key: { type: 'string', description: 'Work package number, e.g. 6046. Leave out for your whole board.' },
        dir: { type: 'string', description: 'Absolute path of the folder you are working in' },
        limit: { type: 'integer', description: 'Whole board only: at most this many tickets. Default 15, at most 30.' },
      },
    },
    async run(client, { key, dir, limit = 15 }) {
      const base = await workFolder(dir);
      const when = new Date().toISOString().replace(/\.\d+Z$/, 'Z');

      if (key) {
        const one = await pullOne(client, String(key).replace(/^#/, ''), base, when);
        if (one.needsSetup) return { found: false, needsSetup: true, error: one.error };
        if (one.error) return { found: false, error: one.error };
        return {
          found: true,
          ...one,
          read: path.join(one.folder, 'README.md'),
          next: one.linked
            ? 'Read README.md first, then the linked files it lists as you need them.'
            : 'Nothing is linked to this ticket yet. Use adam_search to find what it is about, '
              + 'adam_link to record it, then adam_pull again.',
        };
      }

      const answer = await client.service(`/api/board/mine?${await scoped(client)}`);
      if (answer.status === 428) return { found: false, needsSetup: true, error: answer.data?.detail };
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const items = (answer.data.items ?? []).slice(0, Math.max(1, Math.min(Number(limit) || 15, 30)));
      const pulled = [];
      for (const item of items) pulled.push(await pullOne(client, item.key, base, when));
      const board = path.join(base, 'board.md');
      await writeFile(board, boardReadme(pulled, answer.data.openproject, when));
      return {
        found: pulled.length > 0,
        board,
        total: answer.data.total,
        pulled: pulled.map(({ key: k, subject, status, milestone, linked, error }) =>
          ({ key: k, subject, status, milestone, linked, ...(error ? { error } : {}) })),
        ...(answer.data.total > items.length
          ? { more: `${answer.data.total - items.length} more assigned; raise limit or pull them by key` }
          : {}),
        ...(answer.data.note ? { note: answer.data.note } : {}),
      };
    },
  },

  {
    name: 'adam_propose',
    description:
      'Propose a change to one of your OpenProject work packages: a new status, a % done, and/or '
      + 'a comment saying what was done. **Changes nothing.** Returns exactly what would change and '
      + 'a `proposal` code. Then show the person the changes, ask them to confirm, and call '
      + 'adam_apply only if they clearly say yes. Call with only `key` to list the status names '
      + 'there are. Use when work on a ticket is finished or has moved on.',
    inputSchema: {
      type: 'object',
      properties: {
        key: { type: 'string', description: 'Work package number, e.g. 6046' },
        status: { type: 'string', description: 'New status by name, e.g. "In progress" or "Closed"' },
        percentDone: { type: 'integer', description: 'New % done, 0 to 100' },
        comment: { type: 'string', description: 'A comment to add: what was done, where (branch, commit, PR)' },
      },
      required: ['key'],
    },
    async run(client, { key, status, percentDone, comment }) {
      const number = String(key ?? '').replace(/^#/, '');
      if (!status && percentDone === undefined && !comment) {
        const answer = await client.service('/api/board/statuses');
        if (answer.status === 428) return { found: false, needsSetup: true, error: answer.data?.detail };
        if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
        return {
          found: true,
          statuses: answer.data.statuses.map((st) => st.name),
          next: 'Call adam_propose again with the key and a status, percentDone or comment.',
        };
      }
      const answer = await client.service(`/api/work-packages/${encodeURIComponent(number)}/proposals`, {
        method: 'POST',
        body: {
          project_id: (await client.projectId()) ?? '',
          status: status ?? '',
          percent_done: percentDone ?? null,
          comment: comment ?? '',
        },
      });
      if (answer.status === 428) return { ok: false, needsSetup: true, error: answer.data?.detail };
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      return {
        ok: true,
        changed: false,
        ...answer.data,
        next: `Show the person these changes to #${number} and ask whether to apply them. `
          + 'Only after a clear yes, call adam_apply with this key and proposal code.',
      };
    },
  },

  {
    name: 'adam_apply',
    description:
      '**Changes OpenProject.** Applies a change made by adam_propose, using its `proposal` code. '
      + 'Call it only after the person has seen that proposal\'s changes in this conversation and '
      + 'clearly said yes — never on your own initiative, and never for a proposal they have not '
      + 'seen. The change is made as the person. Codes work once and for 15 minutes. Also adds a '
      + 'line to .adam/work/<ticket>/log.md when that folder exists; pass `dir` for it.',
    inputSchema: {
      type: 'object',
      properties: {
        key: { type: 'string', description: 'Work package number, e.g. 6046' },
        proposal: { type: 'string', description: 'The proposal code adam_propose returned' },
        dir: { type: 'string', description: 'Absolute path of the folder you are working in' },
      },
      required: ['key', 'proposal'],
    },
    async run(client, { key, proposal, dir }) {
      const number = String(key ?? '').replace(/^#/, '');
      const tree = await treeState(dir);
      const answer = await client.service(
        `/api/work-packages/${encodeURIComponent(number)}/proposals/${encodeURIComponent(proposal ?? '')}/apply`,
        { method: 'POST', body: { project_id: (await client.projectId()) ?? '', ...tree } },
      );
      if (answer.status === 428) return { ok: false, needsSetup: true, error: answer.data?.detail };
      // A 409 on a closing change is usually the testing gate rather than a
      // clash, and it is the one refusal an agent must not work around: it is
      // handed back as prose for the person to read, with no retry and no
      // alternative route suggested, because there is not one.
      if (answer.status === 409) {
        return { ok: false, changed: false, blocked: true, error: answer.data?.detail,
                 next: 'Tell the person exactly this, and stop. Do not try another status '
                     + 'or another ticket to get around it.' };
      }
      if (!answer.ok) return { ok: false, changed: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };

      // The local record, when this ticket was pulled here. A failure to write
      // it is reported, never allowed to hide that OpenProject did change.
      let logged = null;
      try {
        const folder = path.join(path.resolve(String(dir || process.env.ADAM_WORKDIR || process.cwd())),
          '.adam', 'work', safeName(number));
        if (await stat(folder).catch(() => null)) {
          const when = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
          const log = path.join(folder, 'log.md');
          if (!(await stat(log).catch(() => null))) await writeFile(log, `# Changes applied to #${number}\n\n`);
          await appendFile(log, `- ${when} - ${answer.data.applied}\n`);
          logged = log;
        }
      } catch (error) {
        logged = `not written: ${error.message}`;
      }
      return { ok: true, changed: true, ...answer.data, ...(logged ? { log: logged } : {}) };
    },
  },

  {
    name: 'adam_changes',
    description:
      'The change requests raised against this ADAM project: places where the package (a contract, '
      + 'table, screen, journey or decision) was found wrong, contradictory or missing something. '
      + 'With `id` (CR-007), one in full. Otherwise a list, narrowed by `status`, `kind` + `target`, '
      + 'or `ticket`. **Check this before drafting a new one** - somebody may have raised it already - '
      + 'and before building against an artefact that has an open or accepted request.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'A change request, e.g. CR-007' },
        status: { type: 'string', description: 'open, accepted, rejected or done; comma-separated for several' },
        kind: { type: 'string', description: 'Artefact kind, e.g. operation, schema, table, screen, flow' },
        target: { type: 'string', description: 'Artefact id, e.g. identity#requestGuestCode' },
        ticket: { type: 'string', description: 'OpenProject work package number' },
      },
    },
    async run(client, { id, status, kind, target, ticket } = {}) {
      const project = (await client.projectId()) ?? '';
      if (id) {
        const answer = await client.service(
          `/api/changes/${encodeURIComponent(id)}?${new URLSearchParams({ project_id: project })}`);
        if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
        return answer.data;
      }
      const query = new URLSearchParams({ project_id: project });
      if (status) query.set('status', status);
      if (kind) query.set('target_kind', kind);
      if (target) query.set('target_id', target);
      if (ticket) query.set('ticket', String(ticket).replace(/^#/, ''));
      const answer = await client.service(`/api/changes?${query}`);
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const { items, ...rest } = answer.data;
      return {
        found: items.length > 0,
        ...rest,
        items: items.map((c) => ({
          id: c.id, status: c.status, title: c.title, target: c.target,
          blocking: c.blocking, ticket: c.ticket, raisedBy: c.raisedBy, raisedAt: c.raisedAt,
        })),
        ...(items.length ? {} : { note: 'No change requests match. Nothing has been raised for this yet.' }),
      };
    },
  },

  {
    name: 'adam_draft_change',
    description:
      'Draft a change request for the package - when the contract, table, screen or decision you are '
      + 'building from contradicts itself, is wrong, or lacks something the ticket needs. **Do not '
      + 'resolve such a thing in code; draft this instead.** Files nothing: returns the draft, a '
      + '`draft` code, and any open requests already on the same artefact. Show the person the '
      + 'draft; call adam_raise_change only if they clearly say yes. Quote the conflicting passages '
      + 'in `evidence` and give the ways it could be settled in `options`.',
    inputSchema: {
      type: 'object',
      properties: {
        kind: { type: 'string', description: 'contract, operation, schema, table, screen, flow, module, service, adr, platform, state, event or other' },
        target: { type: 'string', description: 'The artefact, e.g. identity#requestGuestCode or identity:GuestSession' },
        title: { type: 'string', description: 'One line: what is wrong' },
        problem: { type: 'string', description: 'What is wrong and why it matters for the build' },
        evidence: { type: 'string', description: 'The passages that show it, quoted, with where each is' },
        options: { type: 'array', items: { type: 'string' }, description: 'The ways it could be settled' },
        recommendation: { type: 'string', description: 'Which option you would pick and why, if any' },
        blocking: { type: 'boolean', description: 'true when the ticket cannot be finished until it is settled' },
        ticket: { type: 'string', description: 'The OpenProject work package it came up in' },
      },
      required: ['kind', 'target', 'title', 'problem'],
    },
    async run(client, args) {
      const answer = await client.service('/api/changes/drafts', {
        method: 'POST',
        body: {
          project_id: (await client.projectId()) ?? '',
          target_kind: args.kind ?? '',
          target_id: args.target ?? '',
          title: args.title ?? '',
          problem: args.problem ?? '',
          evidence: args.evidence ?? '',
          options: Array.isArray(args.options) ? args.options : [],
          recommendation: args.recommendation ?? '',
          blocking: Boolean(args.blocking),
          ticket: String(args.ticket ?? '').replace(/^#/, ''),
        },
      });
      if (!answer.ok) {
        const detail = answer.data?.detail;
        return { ok: false, filed: false, error: typeof detail === 'string' ? detail : JSON.stringify(detail ?? `HTTP ${answer.status}`) };
      }
      return {
        ok: true,
        filed: false,
        ...answer.data,
        next: answer.data.alreadyOpen?.length
          ? `Tell the person ${answer.data.alreadyOpen.map((c) => c.id).join(', ')} is already open on this; `
            + 'ask whether theirs is different before filing.'
          : 'Show the person this draft and ask whether to file it. Only after a clear yes, call '
            + 'adam_raise_change with the draft code.',
      };
    },
  },

  {
    name: 'adam_raise_change',
    description:
      '**Files a change request in ADAM**, from a draft made by adam_draft_change. Call it only after '
      + 'the person has seen that draft in this conversation and clearly said yes. Returns its id '
      + '(CR-007). If the ticket is blocked by it, offer to propose the ticket On hold with the id in '
      + 'the comment. Draft codes work once and for 30 minutes.',
    inputSchema: {
      type: 'object',
      properties: {
        draft: { type: 'string', description: 'The draft code adam_draft_change returned' },
      },
      required: ['draft'],
    },
    async run(client, { draft }) {
      const answer = await client.service(`/api/changes/drafts/${encodeURIComponent(draft ?? '')}/file`, {
        method: 'POST',
        body: { project_id: (await client.projectId()) ?? '' },
      });
      if (!answer.ok) return { ok: false, filed: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const change = answer.data.change;
      return {
        ok: true,
        filed: true,
        change,
        next: change.blocking && change.ticket
          ? `Filed as ${change.id}. Offer to propose #${change.ticket} On hold with "Blocked by ${change.id}" as the comment.`
          : `Filed as ${change.id}. It shows on ADAM's Changes page for the team to settle.`,
      };
    },
  },

  // ── testing, in batches, checked by somebody else ──────────────────
  //
  // The gate is in the service and not here — closing a ticket goes through
  // /proposals/{code}/apply, and that is where it is refused. These three tools
  // exist so the agent can *explain* the refusal and help with the part that
  // clears it, never to route around it. `adam_check_batch` deliberately cannot
  // be used on your own batch; the service refuses it and so does the text.

  {
    name: 'adam_testing',
    description:
      'Where the testing batch stands: how many tickets have been closed since the last '
      + 'tested batch, whether it is waiting on a teammate, and any batches of other '
      + 'people\'s that this person could check. Read this when a close is refused, and '
      + 'when the person asks what is blocking them.',
    inputSchema: { type: 'object', properties: {} },
    async run(client) {
      const answer = await client.service(`/api/test-batches?${await scoped(client)}`);
      if (answer.status === 428) return { ok: false, needsSetup: true, error: answer.data?.detail };
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const { mine, waiting = [], every } = answer.data;
      let next;
      if (!mine) next = `Nothing closed yet in this batch. Testing is due every ${every}.`;
      else if (mine.verdict === 'failed') {
        next = `Sent back: ${mine.checkerNote || 'no reason given'}. Deal with it and `
          + 'submit again with adam_submit_batch.';
      } else if (mine.submittedAt) {
        next = 'Submitted and waiting on a teammate. Closing is refused until they look — '
          + 'that is deliberate, and not something to work around.';
      } else if (mine.full) {
        next = `${mine.closed} of ${every} closed. Run the tests, then record what you ran `
          + 'with adam_submit_batch. Closing is refused until a teammate checks it.';
      } else {
        next = `${mine.closed} of ${every} closed. ${every - mine.closed} more before testing is due.`;
      }
      if (waiting.length) {
        next += ` ${waiting.length} batch${waiting.length === 1 ? '' : 'es'} of somebody `
          + 'else\'s is waiting to be checked — adam_check_batch.';
      }
      return { ok: true, ...answer.data, next };
    },
  },

  {
    name: 'adam_submit_batch',
    description:
      '**Records that this batch was tested.** Say what was actually run and what it showed — '
      + 'a teammate has to be able to check it, so "tested" is not enough and the service '
      + 'refuses it. Call this only after the tests have really been run and the person has '
      + 'seen the result; never to clear a refusal. Submitting does not reopen closing: a '
      + 'teammate still has to pass it.',
    inputSchema: {
      type: 'object',
      properties: {
        batch: { type: 'number', description: 'Batch id, from adam_testing' },
        notes: { type: 'string', description: 'What was run, and what it showed' },
        evidence: { type: 'string', description: 'Output worth keeping: failures, counts, timings' },
      },
      required: ['batch', 'notes'],
    },
    async run(client, { batch, notes, evidence }) {
      const answer = await client.service(`/api/test-batches/${encodeURIComponent(batch)}/submit`, {
        method: 'POST', body: { notes: notes ?? '', evidence: evidence ?? '' },
      });
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      return { ok: true, batch: answer.data.batch,
               next: 'Recorded. Ask a teammate to check it — you cannot check your own, '
                   + 'and closing stays refused until somebody does.' };
    },
  },

  {
    name: 'adam_check_batch',
    description:
      '**Passes or fails somebody else\'s tested batch.** Only after the person has read what '
      + 'the other developer submitted and said what they think — this is them vouching for '
      + 'a teammate\'s testing, not a formality. You cannot check your own batch and the '
      + 'service refuses it. Failing needs a reason.',
    inputSchema: {
      type: 'object',
      properties: {
        batch: { type: 'number', description: 'Batch id, from adam_testing' },
        verdict: { type: 'string', enum: ['passed', 'failed'] },
        note: { type: 'string', description: 'Why. Required when failing.' },
      },
      required: ['batch', 'verdict'],
    },
    async run(client, { batch, verdict, note }) {
      const answer = await client.service(`/api/test-batches/${encodeURIComponent(batch)}/check`, {
        method: 'POST', body: { verdict: verdict ?? '', note: note ?? '' },
      });
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      return { ok: true, batch: answer.data.batch,
               next: verdict === 'passed'
                 ? 'Passed. They can close tickets again.'
                 : 'Sent back. They submit again once they have dealt with it.' };
    },
  },
];

export const BY_NAME = new Map(TOOLS.map((t) => [t.name, t]));
