/**
 * The twenty-four tools, and where each gets its answer.
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
 * **Five are about scheduled work**, and they go to the accounts service rather
 * than the package — uncached, because coordination changes while you are
 * looking at it. `adam_board` and `adam_work` read OpenProject live as the
 * caller; `adam_team` reads a teammate's tickets, or what everybody has
 * started, the same way (read-only, and only what the caller's own
 * OpenProject account can see). `adam_links` and `adam_link` read and write the one thing neither
 * system can hold on its own: which artefact a work package is about.
 *
 * **Four are about doing the work.** `adam_pull` saves a ticket and everything
 * it is linked to as files under `.adam/` in the developer's folder, so Claude
 * reads what it needs from disk instead of holding it all in the conversation.
 * Every pull is at the latest release ADAM serves (r1, r2, …; CHG-ADM-001):
 * the pin moves with it, and when the release moved since the ticket's previous
 * pull, README.md says what changed and spec-diff.md has the diffs. Nobody
 * chooses a release. `adam_repin` stays for older instructions and is never
 * needed. README.md also lists the change requests raised from the ticket and
 * what was decided on them (CHG-ADM-002).
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
 * What an agent does when the package blocks its ticket (CHG-ADM-004; Chinmay,
 * 14 October 2026: "if there is blocker we log it as CR always. and than scour
 * for next tasks that can be completed and if existing blockers effect it").
 * One sentence, said the same way wherever an agent meets a blocker.
 */
export const BLOCKER_RULE = 'When the package blocks the ticket (a contradiction, missing storage, an undefined '
  + 'rule), always raise a change request with blocking: true (adam_draft_change, show the person, '
  + 'adam_raise_change only after they say yes) and propose the ticket On hold naming the CR (adam_propose, '
  + 'applied only after a yes). Never work around a blocker and never build a guess. Then find the next ticket '
  + 'you can finish: adam_board with only: "workable" lists, in board order, the tickets no open blocking CR '
  + 'affects; propose the first, and say which CR holds back each ticket you skip.';

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
/**
 * A linked record as a ticket needs it. A service answer lists every screen and table in
 * the service - 520 screens, ~45 KB - and was written whole into each ticket touching it
 * (audit R016). Long lists keep their first 40 and say how many there are and how to get
 * the rest.
 */
function trimForPull(record, cap = 40) {
  const out = {};
  for (const [key, value] of Object.entries(record)) {
    if (Array.isArray(value) && value.length > cap && typeof value[0] === 'object') {
      out[key] = value.slice(0, cap);
      out[`${key}Total`] = value.length;
      out[`${key}Note`] = `first ${cap} of ${value.length}; ask ${record.from} for the rest`;
    } else out[key] = value;
  }
  return out;
}

/**
 * What to do when a ticket links nothing. For a setup, onboarding or DevOps ticket that is
 * normal - there is no contract or screen to link - and telling the agent to search and
 * link sent it looking for artefacts that do not exist (audit R021).
 */
function unlinkedHint(wp) {
  if (/^\[(Onboarding|DevOps|Setup)\]/i.test(String(wp?.subject ?? ''))) {
    return 'This is a setup ticket: it is about tooling and environments, not a package artefact, so '
      + 'nothing needs linking. Work from its description and the standards in project-bible/setup/.';
  }
  return 'Nothing is linked to this ticket yet. Find what it is about with adam_search, record it '
    + 'with adam_link, then run adam_pull again.';
}

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

/** Which tool answers for each kind of linked artefact, and with what. Exported
 *  for lib/release-diff.mjs, which asks the same tools about an older release. */
export function lookupFor(kind, id) {
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
    // A package file a ticket is built to: an ADR's text, a setup standard, a doc its description names
    // (TICVAI CHG-TKT-005, 14 October 2026: 29 Block A tasks arrived with nothing linked).
    case 'file': return ['adam_file', { path: id }];
    default: return ['adam_search', { q: id }];
  }
}

const json = (value) => `${JSON.stringify(value, null, 2)}\n`;

/**
 * The ticket's comment thread, oldest first, so the newest - often QA saying
 * why it came back - is the last thing read before the work starts.
 * `undefined` is an ADAM server that does not send comments yet; `null` is a
 * thread it could not read. Neither is shown as "no comments".
 */
function commentsSection(comments) {
  if (comments === undefined) return '';
  if (comments === null) {
    return '\n## Comments\n\n_Could not be read from OpenProject - open the link above before starting._\n';
  }
  let out = `\n## Comments (${comments.length})\n\n`;
  if (!comments.length) return `${out}_None._\n`;
  for (const c of comments) {
    const at = String(c.at ?? '').replace('T', ' ').replace(/:\d\dZ$/, ' UTC');
    out += `### ${c.author || 'Unknown'} - ${at}\n\n${c.text}\n\n`;
  }
  return out;
}

/** One line naming the release a pull is from, for the README's header. */
function releaseLine(release) {
  if (!release?.available) return '';
  if (!release.current) return 'none yet - ADAM is serving the package\'s working tree';
  if (release.previous) return `${release.current}, the latest release (this pull moved the ticket from ${release.previous})`;
  return `${release.current}, the latest release`;
}

/**
 * What changed since the ticket's previous pull, when the release moved in
 * between (CHG-ADM-001). Said, not asked: the files below are already the
 * latest release, and nobody chooses between releases. The whole diff goes in
 * spec-diff.md.
 */
function releaseSection(release) {
  if (!release?.previous) return '';
  const { previous, current, diff } = release;
  let out = `\n## What changed since your previous pull (${previous} -> ${current})\n\n`
    + `You are always on the latest release (${current}): this pull moved the ticket from ${previous}, and `
    + `every file below is ${current}. Build against them.\n\n`;
  if (!diff) {
    return `${out}What changed could not be read (${release.diffError ?? 'no answer'}); read the linked files `
      + 'again before going on, and tell whoever runs ADAM.\n';
  }
  const breaking = diff.breaking ?? [];
  if (breaking.length) {
    out += `${breaking.length === 1 ? 'A breaking contract change' : `${breaking.length} breaking contract changes`} `
      + `in ${current} ${breaking.length === 1 ? 'touches' : 'touch'} this ticket. The producer and the consumer of `
      + `an operation both build against ${current}, so code written before this pull may need changing:\n\n`;
    for (const b of breaking) {
      out += `- **${b.id || 'unnamed'}**: \`${b.contract ? `${b.contract}#` : ''}${b.operation}\` - ${b.reason || 'no reason given'}`
        + `${b.approvedBy ? ` (approved by ${b.approvedBy})` : ''}. This ticket is the **${b.role}**, via ${b.via}.\n`;
    }
    out += '\n';
  }
  const changed = (diff.artefacts ?? []).filter((a) => ['changed', 'added', 'removed'].includes(a.status));
  const same = (diff.artefacts ?? []).filter((a) => a.status === 'unchanged').length;
  if (changed.length) {
    out += `What changed (${changed.length}):\n\n`;
    for (const a of changed) {
      out += `- ${a.kind} \`${a.id}\`: ${a.status === 'changed' ? `+${a.added} -${a.removed} lines`
        : a.status === 'added' ? `new in ${current} (not in ${previous})` : `gone from ${current}`}\n`;
    }
    out += `\n${same} unchanged. Every diff is in [spec-diff.md](spec-diff.md).\n`;
  } else {
    out += `None of the artefacts this ticket is linked to changed between ${previous} and ${current}`
      + `${breaking.length ? ', but the breaking change above still applies' : ''}.\n`;
  }
  out += '\nIf a change is wrong for this ticket, raise a change request (adam_draft_change, source developer) '
    + 'and build the rest against the files as they are.\n';
  return out;
}

function specDiff(wp, release, when) {
  const { previous, current, diff } = release;
  let out = `# #${wp.key}: what changed between ${previous} and ${current}\n\nWritten ${when} by adam_pull. `
    + `You are always on the latest release (${current}); this is what moved since the ticket's previous pull. `
    + 'Each diff is of the record ADAM hands you for that artefact (the file beside this one), '
    + `${previous} on the minus side and ${current} on the plus side.\n`;
  for (const b of diff.breaking ?? []) {
    out += `\n> **Breaking:** ${b.id || 'unnamed'} \`${b.contract ? `${b.contract}#` : ''}${b.operation}\`: `
      + `${b.reason || 'no reason given'}${b.approvedBy ? ` (approved by ${b.approvedBy})` : ''}; this ticket is the ${b.role}, via ${b.via}.\n`;
  }
  for (const a of diff.artefacts ?? []) {
    out += `\n## ${a.kind} \`${a.id}\` - ${a.status}\n\n`;
    if (a.status === 'changed') out += `\`\`\`diff\n${a.diff}\n\`\`\`\n`;
    else if (a.status === 'not-compared') out += `${a.note ?? 'Not compared.'}\n`;
    else if (a.status === 'unchanged') out += 'No change.\n';
    else if (a.status === 'added') out += `Not in ${previous}; the file is ${current}.\n`;
    else if (a.status === 'removed') out += `In ${previous}, gone from ${current}.\n`;
    else out += `Found in neither release.\n`;
  }
  return out;
}

/**
 * Every change request raised from this ticket, near the top of README.md
 * (CHG-ADM-002). The settlement is also a comment in the thread below; this
 * makes it unmissable, and says what to do with each: follow a settled
 * decision, wait on an open one.
 */
function changeSection(changes) {
  if (changes === undefined) return '';
  if (changes === null) {
    return '\n## Change requests on this ticket\n\n_Could not be read from ADAM - run adam_changes with this '
      + 'ticket before building._\n';
  }
  if (!changes.length) return '';
  let out = `\n## Change requests on this ticket (${changes.length})\n\n`
    + '**Read these before building.** A settled decision overrides this ticket\'s description where they '
    + 'differ (a started ticket\'s description is never rewritten); an open request is not decided yet.\n\n';
  for (const c of changes) {
    const release = c.resolvedRef || (c.status === 'open' ? 'not settled yet'
      : c.status === 'rejected' ? 'none (rejected)' : 'the next release');
    out += `### ${c.id} · ${c.status} - ${String(c.title ?? '').trim()}\n\n`
      + `- **Decision:** ${String(c.resolution ?? '').trim() || (c.status === 'open' ? '_none yet_' : '_no note given_')}\n`
      + `- **Release that carries it:** ${release}\n`
      + (c.childTicket ? `- **Its own ticket:** #${c.childTicket}${c.childUrl ? ` (${c.childUrl})` : ''}\n` : '')
      + `- **What to do:** ${c.status === 'open' && c.blocking
        ? 'it blocks this ticket: do not build it or work around it; the ticket goes On hold naming it, and you '
          + 'move to the next ticket you can finish (adam_board with only: "workable")'
        : c.status === 'open'
        ? 'wait on the part it covers: build the rest, and say this part waits on it'
        : c.status === 'rejected'
          ? 'build as the ticket and its linked files say; the request changes nothing'
          : c.childTicket
            ? `build it in #${c.childTicket}, not here`
            : 'follow the decision above'}.\n\n`;
  }
  return out;
}

/**
 * The open blocking change requests that affect this ticket (CHG-ADM-004),
 * from the service's lookup: above "Change requests on this ticket", because
 * it decides whether the ticket can be built at all right now.
 */
function blockedSection(blockedBy) {
  if (!Array.isArray(blockedBy) || !blockedBy.length) return '';
  let out = `\n## Blocked by (${blockedBy.length})\n\n`
    + '**Do not build the blocked part, and do not work around it.** These open blocking change requests '
    + 'affect this ticket:\n\n';
  for (const c of blockedBy) out += `- **${c.id}** (${c.status}) ${String(c.title ?? '').trim()} - via ${c.via}\n`;
  out += `\n${BLOCKER_RULE}\n`;
  return out;
}

/**
 * The ticket this one hangs under, for the header's "Part of" line (CHG-ADM-006): its number and subject, then its
 * status and holder, or "could not be read" when ADAM could only name it. '' when it hangs under nothing.
 */
function partOfText(partOf) {
  if (!partOf?.key) return '';
  const about = partOf.read === false ? 'could not be read'
    : `${partOf.status || 'no status'}, ${partOf.assignee || 'unassigned'}`;
  return `#${partOf.key} ${String(partOf.subject ?? '').trim()} (${about})`;
}

/**
 * The work under this ticket, at every depth, in the order ADAM gives (the board's order), never re-sorted here
 * (CHG-ADM-006). Read by the service from OpenProject for this ticket, not from the held project read. `undefined`
 * is an ADAM from before sub-tasks (no section); `null` a read that failed, which is said rather than shown as none.
 */
function subtaskSection(subtasks) {
  if (subtasks === undefined) return '';
  if (subtasks === null) {
    return '\n## Sub-tasks\n\n_Could not be read from OpenProject. Open the ticket\'s link above to see them, '
      + 'and pull again later._\n';
  }
  if (!subtasks.length) return '';
  let out = `\n## Sub-tasks (${subtasks.length})\n\n`
    + 'The work under this ticket, in the order it is done. Pull one (adam_pull with its number) before you work on it.\n\n';
  for (const s of subtasks) {
    out += `- #${s.key} ${String(s.subject ?? '').trim()} - ${s.status || 'no status'}, ${s.assignee || 'unassigned'}`
      + `${s.depth > 1 && s.parent ? ` (under #${s.parent})` : ''}\n`;
  }
  return out;
}

function ticketReadme(wp, files, missing, when, decisions = [], release = null, changes = undefined, blockedBy = [],
  tree = {}, db = null) {
  const line = (label, value) => (value || value === 0 ? `- **${label}:** ${value}\n` : '');
  let out = `# #${wp.key} ${wp.subject}\n\n`;
  out += line('Project', wp.project) + line('Type', wp.type) + line('Part of', partOfText(tree.partOf))
    + line('Status', wp.status)
    + line('Milestone', wp.version) + line('Priority', wp.priority) + line('Assignee', wp.assignee)
    + line('Start', wp.startDate) + line('Due', wp.dueDate)
    + line('% done', wp.percentDone) + line('OpenProject', wp.url)
    + line('Release', releaseLine(release));
  out += `\nPulled ${when} by the ADAM connector. Status and dates are a copy from then; `
    + 'run adam_pull again for the current ones.';
  if (release?.current) {
    out += ` You are always on the latest release (${release.current}): every pull serves it, so there is no `
      + 'release to choose and nothing to re-pin.';
  }
  out += '\n';
  out += blockedSection(blockedBy);
  out += changeSection(changes);
  out += releaseSection(release);
  out += subtaskSection(tree.subtasks);
  out += '\n';
  out += `## Description\n\n${wp.description || '_No description in OpenProject._'}\n`;
  if (wp.descriptionTrimmed) out += '\n_Longer in OpenProject - open the link above for the rest._\n';
  out += commentsSection(wp.comments);
  out += `\n## What this touches (${files.length})\n\n`;
  if (files.length) {
    for (const f of files) out += `- ${f.kind} \`${f.id}\` - [${f.file}](${f.file})\n`;
  } else {
    out += `${unlinkedHint(wp)}\n`;
  }
  if (decisions.length) {
    out += `\nDecisions linked but not pulled: ${decisions.map((d) => `\`${d}\``).join(', ')}. `
      + 'Ask adam_decisions if the build needs one.\n';
  }
  if (missing.length) {
    out += `\nLinked but not found in the package: ${missing.map((m) => `${m.kind} \`${m.id}\``).join(', ')}.\n`;
  }
  // The files above are summaries. On #20354 (24 September) an agent read them as the whole truth and
  // reported three gaps that were not there - parameters, the item schema and row-level security - and
  // proposed a change request for them. A gap is only a gap once the source says so.
  out += '\n## Before you report a gap\n\n'
    + 'The files above are ADAM\'s summaries of the package, not the package. Before telling anyone '
    + 'something is missing, wrong or needs a change request, check the source yourself and say what you '
    + 'checked:\n\n'
    + '- **An operation:** `adam_contract` with `operation` lists its parameters, responses and request body. '
    + 'If one still looks missing, read the YAML with `adam_file` at the contract path and line it gives. '
    + '**Shared errors are implicit:** every operation may return 400, 401, 403, 404, 429 and 5xx from '
    + '`contracts/shared/common.yaml` without listing them, so an operation listing no errors is not a gap '
    + '(api-conventions section 5).\n'
    + '- **Scope:** a venue-scoped list does not include tenant-level rows (venue_id null); that is the rule, '
    + 'not a gap (naming-and-style 5.3).\n'
    + '- **A table:** `adam_table` gives its migration; read the DDL with `adam_file`, including '
    + '`900-foreign-keys.sql`, `910-indexes.sql` and `920-row-level-security.sql`, before saying a key, index '
    + 'or policy is absent.\n'
    + '- **A standard:** quote the rule and its file (e.g. `project-bible/setup/naming-and-style.md`). If the '
    + 'same drift is in many tables, it is one package-wide change request, not this ticket\'s.\n\n'
    + 'Report only what survives the check, and keep what you ruled out to one line. A real gap in the '
    + 'contract is a change request (adam_draft_change); a question the contract cannot answer is for '
    + 'whoever owns the ticket.\n';
  out += databaseSection(db, wp.key);
  out += '\n## When you have finished\n\n'
    + 'Ask Claude to propose the change (adam_propose): the new status, % done, and a comment '
    + 'saying what was done. Check what it shows you, then say yes to apply it (adam_apply). '
    + 'Applied changes are listed in [log.md](log.md). Your own notes go in [notes.md](notes.md) - '
    + 'pulling again keeps both.\n';
  return out;
}

/**
 * The release side of a pull (council C2 and C9; CHG-ADM-001 from 14 October).
 *
 * Every pull is at the latest release ADAM serves. The service records the pin
 * on a first pull and, when the pin is behind, moves it to the latest release
 * itself and answers with `movedFrom` (logged as `auto`). Against a service from
 * before that, which leaves the pin behind and answers `stale`, this moves it
 * (reason `accept`), so the answer is the same either way. When the release
 * moved, asks the viewer what changed in the ticket's artefacts between the
 * previous pull's release and this one. Asked in slices, so a ticket linked to
 * a hundred screens does not become one URL longer than a proxy will take.
 *
 * Never the reason a pull fails: an ADAM without releases answers 404 here, and
 * the pull goes on exactly as it did before, saying nothing about releases.
 */
async function releaseFor(client, key, touches) {
  const project = (await client.projectId()) ?? '';
  const route = `/api/work-packages/${encodeURIComponent(key)}/pin`;
  let pinned = await client.service(route, { method: 'POST', body: { project_id: project, reason: 'pull' } });
  if (!pinned.ok) {
    return { available: false, why: pinned.data?.detail ?? `HTTP ${pinned.status}` };
  }
  let previous = pinned.data?.movedFrom || null;
  if (pinned.data?.stale) {
    previous = pinned.data.pin?.tag ?? null;
    const moved = await client.service(route, {
      method: 'POST', body: { project_id: project, reason: 'accept', note: 'auto: every pull is at the latest release' },
    });
    if (moved.ok) pinned = moved;
  }
  const state = pinned.data ?? {};
  const release = {
    available: true,
    pin: state.pin?.tag ?? null,
    current: state.current?.tag ?? null,
    recorded: Boolean(state.recorded),
    previous: previous && previous !== (state.current?.tag ?? null) ? previous : null,
  };
  if (!release.previous || !release.current) return release;

  const compared = touches.filter((t) => t.kind !== 'adr');
  const merged = { artefacts: [], breaking: [] };
  const seen = new Map();
  for (let at = 0; at < Math.max(compared.length, 1); at += 40) {
    const slice = compared.slice(at, at + 40);
    const answer = await client.packageJson('release-diff', [
      ['from', release.previous], ['to', release.current],
      ...slice.map((t) => ['touch', `${t.kind}:${t.id}`]),
    ]).catch((error) => ({ ok: false, status: 0, data: { error: error.message } }));
    if (!answer.ok) {
      release.diffError = answer.data?.error ?? `HTTP ${answer.status}`;
      return release;
    }
    merged.artefacts.push(...(answer.data.artefacts ?? []));
    // Every slice sees every breaking entry; a consumer found in any slice wins.
    for (const b of answer.data.breaking ?? []) {
      const k = b.id || `${b.contract}#${b.operation}`;
      if (!seen.has(k) || (b.role === 'consumer' && seen.get(k).role !== 'consumer')) seen.set(k, b);
    }
    if (answer.data.breakingFileError) merged.breakingFileError = answer.data.breakingFileError;
  }
  merged.breaking = [...seen.values()];
  release.diff = merged;
  return release;
}

/**
 * The change requests raised from a ticket (CHG-ADM-002), oldest first, for its
 * README. `undefined` is an ADAM that could not be asked (the section is left
 * out, as before); `null` a list that would not read, which the README says.
 */
async function changesFor(client, key) {
  const query = new URLSearchParams({ project_id: (await client.projectId()) ?? '', ticket: String(key) });
  const answer = await client.service(`/api/changes?${query}`).catch(() => null);
  // An ADAM without the route, or a reader it refuses, gets no section; a failure says so.
  if (!answer || (answer.status === 0 || answer.status >= 500)) return answer ? null : undefined;
  if (!answer.ok) return undefined;
  return [...(answer.data?.items ?? [])].sort((a, b) => (a.number ?? 0) - (b.number ?? 0));
}

// ---- a database ticket's expected end state ---------------------------------
//
// **Why the connector writes it** (Chinmay, 20 October 2026). A [DB] ticket's agent rebuilt every
// migration from an empty database, reasoned about the effect by itself and ran the whole dotnet
// suite, on every ticket. The decided way: apply only the ticket's file to a copy of the database at
// the previous state, and compare it with the package. expected-schema.json carries two things from
// the package's derived DDL (backend/<database>/: the 010 file that creates each table, then 900
// keys, 910 indexes, 920 row-level security, 930 partitions and the V01nn after-r1 files):
//   - the package statements that make the ticket's tables, in package order. The project's
//     `.claude/scripts/db-ticket.mjs` applies them to a second copy and lets PostgreSQL compare the
//     two databases whole (review of 20 October: a parsed shape passed a changed CHECK body, a changed
//     index WHERE and a weakened policy, and said nothing about other tables);
//   - the tables' shape as parsed here, for the person and the agent to read.
//
// The parser reads the subset of DDL derive-ddl writes and says what it did not understand
// (`notModelled`) instead of guessing. `db-ticket-check.mjs --package` holds both to the real thing.

/** Statements of a SQL file: comments dropped, strings and dollar-quoted bodies kept whole. */
export function sqlStatements(text) {
  const s = String(text ?? '');
  const out = [];
  let cur = '';
  const push = () => { const t = cur.trim(); if (t) out.push(t); cur = ''; };
  for (let i = 0; i < s.length;) {
    const ch = s[i];
    const two = s.slice(i, i + 2);
    if (two === '--') { const end = s.indexOf('\n', i); i = end < 0 ? s.length : end; if (!cur.endsWith(' ')) cur += ' '; continue; }
    if (two === '/*') { const end = s.indexOf('*/', i + 2); i = end < 0 ? s.length : end + 2; if (!cur.endsWith(' ')) cur += ' '; continue; }
    if (ch === "'" || ch === '"') {
      let j = i + 1;
      while (j < s.length && !(s[j] === ch && s[j + 1] !== ch)) j += s[j] === ch ? 2 : 1;
      cur += s.slice(i, j + 1);
      i = j + 1;
      continue;
    }
    if (ch === '$') {
      const tag = /^\$(?:[A-Za-z_]\w*)?\$/.exec(s.slice(i, i + 64))?.[0];
      if (tag) {
        const end = s.indexOf(tag, i + tag.length);
        const stop = end < 0 ? s.length : end + tag.length;
        cur += s.slice(i, stop);
        i = stop;
        continue;
      }
    }
    if (ch === ';') { push(); i++; continue; }
    if (/\s/.test(ch)) { if (cur && !cur.endsWith(' ')) cur += ' '; i++; continue; }
    cur += ch;
    i++;
  }
  push();
  return out;
}

/** Where each top-level separator or keyword starts: outside quotes and parentheses. */
function topLevel(text, test) {
  const hits = [];
  let depth = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (ch === "'" || ch === '"') {
      let j = i + 1;
      while (j < text.length && !(text[j] === ch && text[j + 1] !== ch)) j += text[j] === ch ? 2 : 1;
      i = j;
      continue;
    }
    if (ch === '(') depth++;
    else if (ch === ')') depth--;
    else if (depth === 0) {
      // A keyword test answers with its length, so NULL inside NOT NULL is not a second hit.
      const hit = test(text, i);
      if (hit) { hits.push(i); if (typeof hit === 'number') i += hit - 1; }
    }
  }
  return hits;
}

function splitTop(text, sep = ',') {
  const at = topLevel(text, (t, i) => t[i] === sep);
  const out = [];
  let from = 0;
  for (const i of at) { out.push(text.slice(from, i)); from = i + 1; }
  out.push(text.slice(from));
  return out.map((p) => p.trim()).filter(Boolean);
}

/** The text inside the parenthesis that opens at or after `from`, and where it ends. */
function group(text, from = 0) {
  const open = text.indexOf('(', from);
  if (open < 0) return null;
  let depth = 0;
  for (let i = open; i < text.length; i++) {
    const ch = text[i];
    if (ch === "'" || ch === '"') {
      let j = i + 1;
      while (j < text.length && !(text[j] === ch && text[j + 1] !== ch)) j += text[j] === ch ? 2 : 1;
      i = j;
      continue;
    }
    if (ch === '(') depth++;
    else if (ch === ')' && --depth === 0) return { inner: text.slice(open + 1, i), start: open, end: i + 1 };
  }
  return null;
}

const ident = (name) => String(name ?? '').trim().replace(/"/g, '').toLowerCase();
const qualified = (name, schema) => (ident(name).includes('.') ? ident(name) : `${schema}.${ident(name)}`);
const columnsOf = (text) => splitTop(text).map(ident);
const shortName = (table) => table.split('.').pop();

// The clauses a column definition can carry after its type, in any order.
const COLUMN_CLAUSE = /^(NOT\s+NULL|NULL|DEFAULT|CONSTRAINT|PRIMARY\s+KEY|UNIQUE|REFERENCES|CHECK|GENERATED|COLLATE)\b/i;
const atClause = (rx) => (t, i) => ((i === 0 || /[\s)]/.test(t[i - 1])) && rx.exec(t.slice(i))?.[0].length) || 0;

function newTable(name, file) {
  return {
    name, file, columns: [], primaryKey: null, unique: [], foreignKeys: [], checks: [], indexes: [],
    rls: { enabled: false, forced: false, policies: [] }, partitionBy: null, defaultPartition: false,
  };
}

/** `REFERENCES t (c) ON DELETE x` from `text`, the clause starting at its first word. */
function references(text, schema) {
  const m = /^REFERENCES\s+([\w".]+)\s*/i.exec(text);
  if (!m) return null;
  const rest = text.slice(m[0].length);
  const cols = rest.startsWith('(') ? group(rest) : null;
  return {
    references: qualified(m[1], schema),
    refColumns: cols ? columnsOf(cols.inner) : [],
    onDelete: (/ON\s+DELETE\s+(SET\s+NULL|SET\s+DEFAULT|NO\s+ACTION|CASCADE|RESTRICT)/i.exec(rest)?.[1] ?? null)
      ?.toUpperCase().replace(/\s+/g, ' ') ?? null,
  };
}

function addConstraint(table, name, body, schema) {
  const key = /^(PRIMARY\s+KEY|UNIQUE|FOREIGN\s+KEY|CHECK|EXCLUDE)\b/i.exec(body)?.[1]?.toUpperCase().replace(/\s+/g, ' ');
  if (key === 'PRIMARY KEY') {
    table.primaryKey = { name, columns: columnsOf(group(body).inner) };
    for (const c of table.primaryKey.columns) {
      const col = table.columns.find((x) => x.name === c);
      if (col) col.notNull = true;
    }
  } else if (key === 'UNIQUE') {
    table.unique.push({ name, columns: columnsOf(group(body).inner) });
  } else if (key === 'FOREIGN KEY') {
    const cols = group(body);
    const ref = references(body.slice(cols.end).trim(), schema);
    table.foreignKeys.push({ name, columns: columnsOf(cols.inner), ...ref });
  } else if (key === 'CHECK') {
    table.checks.push({ name });
  } else {
    return false;
  }
  return true;
}

/** One column definition, with the constraints written on it. */
function parseColumn(table, def, schema) {
  const m = /^("(?:[^"]|"")+"|[\w]+)\s+([\s\S]*)$/.exec(def.trim());
  if (!m) return null;
  const name = ident(m[1]);
  const rest = m[2];
  const at = topLevel(rest, atClause(COLUMN_CLAUSE));
  const column = { name, type: (at.length ? rest.slice(0, at[0]) : rest).trim(), notNull: false };
  let pending = null;
  at.forEach((start, n) => {
    const clause = rest.slice(start, n + 1 < at.length ? at[n + 1] : undefined).trim();
    const word = COLUMN_CLAUSE.exec(clause)[1].toUpperCase().replace(/\s+/g, ' ');
    if (word === 'NOT NULL') column.notNull = true;
    else if (word === 'NULL') column.notNull = false;
    else if (word === 'DEFAULT') column.default = clause.slice(7).trim();
    else if (word === 'CONSTRAINT') { pending = ident(clause.split(/\s+/)[1]); return; }
    else if (word === 'PRIMARY KEY') { table.primaryKey = { name: pending, columns: [name] }; column.notNull = true; }
    else if (word === 'UNIQUE') table.unique.push({ name: pending, columns: [name] });
    else if (word === 'REFERENCES') table.foreignKeys.push({ name: pending, columns: [name], ...references(clause, schema) });
    else if (word === 'CHECK') table.checks.push({ name: pending ?? `${shortName(table.name)}_${name}_check` });
    else if (word === 'GENERATED') column.generated = true;
    pending = null;
  });
  return column;
}

function createTable(model, stmt, file, notModelled) {
  const head = /^CREATE\s+(?:UNLOGGED\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w".]+)\s*/i.exec(stmt);
  const name = ident(head[1]);
  const schema = name.split('.')[0];
  const rest = stmt.slice(head[0].length);
  const partOf = /^PARTITION\s+OF\s+([\w".]+)\s*([\s\S]*)$/i.exec(rest);
  if (partOf) {
    const parent = model.get(qualified(partOf[1], schema));
    // A month's partition depends on the day it was made; only the default one is a fixed fact.
    if (parent && /^DEFAULT\b/i.test(partOf[2].trim())) parent.defaultPartition = true;
    return;
  }
  if (model.has(name)) return; // IF NOT EXISTS: the first definition stands
  const body = group(rest);
  if (!body) { notModelled.push({ file, statement: stmt.slice(0, 200) }); return; }
  const table = newTable(name, file);
  for (const item of splitTop(body.inner)) {
    const named = /^CONSTRAINT\s+([\w"]+)\s+([\s\S]*)$/i.exec(item);
    if (named) { addConstraint(table, ident(named[1]), named[2], schema); continue; }
    if (/^(PRIMARY\s+KEY|UNIQUE|FOREIGN\s+KEY|CHECK|EXCLUDE)\b/i.test(item)) { addConstraint(table, null, item, schema); continue; }
    if (/^LIKE\b/i.test(item)) { notModelled.push({ file, table: name, statement: item.slice(0, 200) }); continue; }
    const column = parseColumn(table, item, schema);
    if (column) table.columns.push(column);
  }
  const after = rest.slice(body.end).trim();
  const part = /^PARTITION\s+BY\s+([\s\S]+)$/i.exec(after);
  if (part) table.partitionBy = part[1].trim();
  model.set(name, table);
}

function alterTable(model, stmt, file, notModelled) {
  const head = /^ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?([\w".]+)\s*/i.exec(stmt);
  const name = ident(head[1]);
  const schema = name.split('.')[0];
  const table = model.get(name);
  if (!table) return;
  const rest = stmt.slice(head[0].length);
  const renamed = /^RENAME\s+TO\s+([\w"]+)$/i.exec(rest);
  if (renamed) {
    model.delete(name);
    table.name = `${schema}.${ident(renamed[1])}`;
    model.set(table.name, table);
    return;
  }
  for (const action of splitTop(rest)) {
    let m;
    if ((m = /^ADD\s+CONSTRAINT\s+([\w"]+)\s+([\s\S]*)$/i.exec(action))) {
      if (!addConstraint(table, ident(m[1]), m[2], schema)) notModelled.push({ file, table: name, statement: action.slice(0, 200) });
    } else if (/^ADD\s+(PRIMARY\s+KEY|UNIQUE|FOREIGN\s+KEY|CHECK|EXCLUDE)\b/i.test(action)) {
      if (!addConstraint(table, null, action.replace(/^ADD\s+/i, ''), schema)) notModelled.push({ file, table: name, statement: action.slice(0, 200) });
    } else if ((m = /^ADD\s+(?:COLUMN\s+)?(IF\s+NOT\s+EXISTS\s+)?([\s\S]*)$/i.exec(action))) {
      const before = { pk: table.primaryKey, checks: table.checks.length, unique: table.unique.length, fks: table.foreignKeys.length };
      const column = parseColumn(table, m[2], schema);
      if (!column) { notModelled.push({ file, table: name, statement: action.slice(0, 200) }); continue; }
      if (table.columns.some((c) => c.name === column.name)) {
        // ADD COLUMN IF NOT EXISTS on a column already there does nothing, constraints included.
        table.primaryKey = before.pk;
        table.checks.length = before.checks;
        table.unique.length = before.unique;
        table.foreignKeys.length = before.fks;
        continue;
      }
      table.columns.push(column);
    } else if ((m = /^DROP\s+COLUMN\s+(?:IF\s+EXISTS\s+)?([\w"]+)/i.exec(action))) {
      const col = ident(m[1]);
      table.columns = table.columns.filter((c) => c.name !== col);
    } else if ((m = /^DROP\s+CONSTRAINT\s+(?:IF\s+EXISTS\s+)?([\w"]+)/i.exec(action))) {
      const con = ident(m[1]);
      if (table.primaryKey?.name === con) table.primaryKey = null;
      for (const k of ['unique', 'foreignKeys', 'checks']) table[k] = table[k].filter((c) => c.name !== con);
    } else if ((m = /^ALTER\s+(?:COLUMN\s+)?([\w"]+)\s+([\s\S]*)$/i.exec(action))) {
      const col = table.columns.find((c) => c.name === ident(m[1]));
      const what = m[2];
      if (!col) continue;
      if (/^SET\s+NOT\s+NULL$/i.test(what)) col.notNull = true;
      else if (/^DROP\s+NOT\s+NULL$/i.test(what)) col.notNull = false;
      else if (/^SET\s+DEFAULT\s+/i.test(what)) col.default = what.replace(/^SET\s+DEFAULT\s+/i, '').trim();
      else if (/^DROP\s+DEFAULT$/i.test(what)) delete col.default;
      else if (/^(SET\s+DATA\s+)?TYPE\s+/i.test(what)) col.type = what.replace(/^(SET\s+DATA\s+)?TYPE\s+/i, '').replace(/\s+USING\s+[\s\S]*$/i, '').trim();
      else notModelled.push({ file, table: name, statement: action.slice(0, 200) });
    } else if ((m = /^RENAME\s+CONSTRAINT\s+([\w"]+)\s+TO\s+([\w"]+)$/i.exec(action))) {
      for (const k of [table.primaryKey, ...table.unique, ...table.foreignKeys, ...table.checks]) {
        if (k && k.name === ident(m[1])) k.name = ident(m[2]);
      }
    } else if ((m = /^RENAME\s+(?:COLUMN\s+)?([\w"]+)\s+TO\s+([\w"]+)$/i.exec(action))) {
      const col = table.columns.find((c) => c.name === ident(m[1]));
      if (col) col.name = ident(m[2]);
    } else if (/^ENABLE\s+ROW\s+LEVEL\s+SECURITY$/i.test(action)) table.rls.enabled = true;
    else if (/^DISABLE\s+ROW\s+LEVEL\s+SECURITY$/i.test(action)) table.rls.enabled = false;
    else if (/^FORCE\s+ROW\s+LEVEL\s+SECURITY$/i.test(action)) table.rls.forced = true;
    else if (/^NO\s+FORCE\s+ROW\s+LEVEL\s+SECURITY$/i.test(action)) table.rls.forced = false;
    else if (/^(OWNER\s+TO|SET\s*\(|RESET\s*\(|ATTACH\s+PARTITION|DETACH\s+PARTITION|VALIDATE\s+CONSTRAINT)\b/i.test(action)) { /* not part of the shape */ }
    else notModelled.push({ file, table: name, statement: action.slice(0, 200) });
  }
}

function createIndex(model, stmt) {
  const m = /^CREATE\s+(UNIQUE\s+)?INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+NOT\s+EXISTS\s+)?(?!ON\s)([\w"]+)?\s*ON\s+(?:ONLY\s+)?([\w".]+)\s*(?:USING\s+(\w+)\s*)?/i.exec(stmt);
  if (!m) return false;
  const table = model.get(ident(m[3]));
  if (!table) return true;
  const keys = group(stmt, m[0].length - 1);
  const after = stmt.slice(keys.end);
  const name = m[2] ? ident(m[2]) : null;
  if (name && table.indexes.some((i) => i.name === name)) return true; // IF NOT EXISTS
  table.indexes.push({
    name,
    unique: Boolean(m[1]),
    method: (m[4] ?? 'btree').toLowerCase(),
    keys: keys.inner.trim(),
    ...(/\bWHERE\b/i.test(after) ? { where: after.replace(/^[\s\S]*?\bWHERE\s+/i, '').trim() } : {}),
  });
  return true;
}

// What each of 920's helpers puts in the policy's USING expression, so the compare can tell a scope
// policy from a venue one under the same name. The name is the helper's: platform.rls_policy_name.
const RLS_MARKER = {
  scope: () => 'in_scope(scope_path)',
  shared_scope: () => 'in_scope(scope_path)',
  venue: () => 'venue_in_scope(venue_id)',
  tenant: () => 'tenant_root_in_scope()',
  subject: () => 'subject_in_scope(subject_id)',
  parent: (args) => ident(String(args[2] ?? '').replace(/::regclass$/i, '').replace(/'/g, '')),
};

// The r8 helpers that split a table's policy in four (read, append, update, delete), named after the
// first 55 characters of the table: apply_split_rls and the ones that call it, and append_audit.
const SPLIT_RLS = new Set(['split', 'read_beneath', 'grant_holder_read', 'grant_holder_subject_read', 'parent_split', 'append_audit']);

function applyRls(model, stmt) {
  const m = /^SELECT\s+platform\.apply_(\w+?)_rls\s*\(([\s\S]*)\)$/i.exec(stmt);
  if (!m) return false;
  const args = splitTop(m[2]);
  const target = ident(args[0].replace(/::regclass$/i, '').replace(/'/g, ''));
  const table = model.get(target);
  if (!table) return true;
  const kind = m[1].toLowerCase();
  table.rls.enabled = true;
  table.rls.forced = true;
  if (SPLIT_RLS.has(kind)) {
    const base = shortName(target).slice(0, 55);
    const four = ['read', 'append', 'update', 'delete'].map((s) => `${base}_${s}`);
    const keep = kind === 'append_audit'
      ? table.rls.policies.filter((p) => p.name !== `${shortName(target).slice(0, 57)}_scope` && !four.includes(p.name))
      : [];
    table.rls.policies = [...keep, ...four.map((name) => ({ name }))];
    return true;
  }
  const policy = `${shortName(target).slice(0, 57)}_scope`;
  table.rls.policies = table.rls.policies.filter((p) => p.name !== policy && !/^(scope|venue)_isolation$/.test(p.name));
  const marker = RLS_MARKER[kind];
  table.rls.policies.push({ name: policy, ...(marker ? { uses: marker(args) } : {}) });
  return true;
}

/**
 * The ALTER TABLE and ALTER INDEX statements inside a DO block (r8's guarded renames and keys:
 * `DO $$ BEGIN IF <the old name is there> THEN ALTER TABLE ... RENAME COLUMN ...; END IF; END $$`).
 */
export function doInner(stmt) {
  const m = /^DO\s+(\$\w*\$)([\s\S]*)\1\s*$/i.exec(String(stmt));
  if (!m) return [];
  return m[2].split(';').map((p) => /\b((?:ALTER\s+(?:TABLE|INDEX)|DROP\s+INDEX|CREATE\s+(?:UNIQUE\s+)?INDEX)\b[\s\S]*)$/i.exec(p)?.[1]?.trim()).filter(Boolean);
}

const INDEX_RENAME = /^ALTER\s+INDEX\s+(?:IF\s+EXISTS\s+)?([\w".]+)\s+RENAME\s+TO\s+([\w"]+)/i;

function renameIndex(model, from, to) {
  const name = ident(from).split('.').pop();
  for (const t of model.values()) {
    const index = t.indexes.find((i) => i.name === name);
    if (index) index.name = ident(to);
  }
}

/**
 * Every table the files create, as it stands after all of them: `files` is [{ name, text }] for
 * one database, in the order the package applies them. Returns { tables: Map, notModelled }.
 */
export function schemaModel(files) {
  const model = new Map();
  const notModelled = [];
  const ordered = [...files].sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
  for (const { name: file, text } of ordered) {
    for (const stmt of sqlStatements(text)) {
      let m;
      if (/^DO\b/i.test(stmt)) {
        // The block runs its statement only when its condition holds, which this cannot know: renames
        // and drops are followed (their condition is "the old name is still there"); a key it adds is
        // left out of the shape, so the shape never claims more than PostgreSQL will have.
        for (const one of doInner(stmt)) {
          if (/^ALTER\s+TABLE\b/i.test(one) && !/\bADD\s+CONSTRAINT\b/i.test(one)) alterTable(model, one, file, notModelled);
          else if ((m = INDEX_RENAME.exec(one))) renameIndex(model, m[1], m[2]);
          else if ((m = /^DROP\s+INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+EXISTS\s+)?([\w".]+)/i.exec(one))) {
            const index = ident(m[1]).split('.').pop();
            for (const t of model.values()) t.indexes = t.indexes.filter((i) => i.name !== index);
          }
        }
        continue;
      }
      if (/^CREATE\s+(?:UNLOGGED\s+)?TABLE\b/i.test(stmt)) createTable(model, stmt, file, notModelled);
      else if (/^ALTER\s+TABLE\b/i.test(stmt)) alterTable(model, stmt, file, notModelled);
      else if ((m = INDEX_RENAME.exec(stmt))) renameIndex(model, m[1], m[2]);
      else if (/^CREATE\s+(UNIQUE\s+)?INDEX\b/i.test(stmt)) createIndex(model, stmt);
      else if (/^SELECT\s+platform\.apply_\w+_rls\b/i.test(stmt)) applyRls(model, stmt);
      else if ((m = /^SELECT\s+platform\.drop_rls_policies\s*\(\s*'([\w".]+)'/i.exec(stmt))) {
        const table = model.get(ident(m[1]));
        if (table) table.rls.policies = [];
      }
      else if ((m = /^CREATE\s+POLICY\s+([\w"]+)\s+ON\s+([\w".]+)/i.exec(stmt))) {
        const table = model.get(ident(m[2]));
        if (table && !table.rls.policies.some((p) => p.name === ident(m[1]))) table.rls.policies.push({ name: ident(m[1]) });
      } else if ((m = /^DROP\s+POLICY\s+(?:IF\s+EXISTS\s+)?([\w"]+)\s+ON\s+([\w".]+)/i.exec(stmt))) {
        const table = model.get(ident(m[2]));
        if (table) table.rls.policies = table.rls.policies.filter((p) => p.name !== ident(m[1]));
      } else if ((m = /^DROP\s+INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+EXISTS\s+)?([\w".]+)/i.exec(stmt))) {
        const index = ident(m[1]).split('.').pop();
        for (const t of model.values()) t.indexes = t.indexes.filter((i) => i.name !== index);
      } else if ((m = /^DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?([\w".]+)/i.exec(stmt))) {
        model.delete(ident(m[1]));
      }
      // CREATE SCHEMA, EXTENSION, FUNCTION, TYPE, COMMENT ON, INSERT, and SELECT of the partition
      // helpers: not the shape of a table.
    }
  }
  return { tables: model, notModelled };
}


/**
 * A [DB] ticket's migration: the numbered file its subject names (`V0027__access.sql`), the
 * database it is in, the tables it links, and what kind of migration it is:
 *   tables        creates or changes the tables it links (nearly all of them);
 *   baseline      V0001: schemas, extensions, the register and the helper functions, in both databases;
 *   foreign-keys  the cross-schema keys added last; the constraint names come from the description.
 * Null for a ticket that is not a [DB] migration - a [BE] ticket that only reads tables, or a [DB]
 * task with no migration file (monthly partitions).
 */
export function databaseTicket(wp, touches) {
  const tables = [...new Set((touches ?? []).filter((t) => t.kind === 'table').map((t) => String(t.id)))];
  const subject = String(wp?.subject ?? '');
  const description = String(wp?.description ?? '');
  const migration = /\b(V\d{4,}[A-Za-z]?__[\w.-]+?\.sql)\b/.exec(subject)?.[1]
    ?? /\b(V\d{4,}[A-Za-z]?__[\w.-]+?\.sql)\b/.exec(description)?.[1];
  if (!migration || !/^\s*\[DB\]/i.test(subject)) return null;
  const database = /\bcontrol database\b/i.test(description) ? 'control'
    : /\btenant database\b/i.test(description) ? 'tenant' : null;
  if (/^V0*1__/i.test(migration) || /\bbaseline\b/i.test(migration)) {
    return { kind: 'baseline', migration, tables, database: null };
  }
  if (/foreign.?keys/i.test(migration)) {
    const constraints = [...new Set([...description.matchAll(/\bas\s+(\w+_fkey)\b/g)].map((m) => m[1]))];
    return { kind: 'foreign-keys', migration, tables: [], constraints, database: database ?? 'tenant' };
  }
  // A forward migration (V1000 and later) also owns the keys that point into its tables from tables
  // made before it: no cross-schema keys ticket comes after it to add them (promotions.voucher's
  // voucher_batch_id_fkey: voucher is made in V1017, voucher_batch in V1114).
  const forward = Number(/^V(\d+)/i.exec(migration)?.[1] ?? 0) >= 1000;
  return { kind: 'tables', migration, tables, database, ...(forward ? { forward: true } : {}) };
}

/**
 * The table a package statement makes or changes, or null for one that is not about a table.
 * `indexes` (index name -> table) answers for DROP INDEX and ALTER INDEX, which name only the index.
 */
export function statementTarget(stmt, indexes = null) {
  const s = String(stmt);
  let m;
  if (/^DO\b/i.test(s)) {
    for (const one of doInner(s)) {
      const target = statementTarget(one, indexes);
      if (target) return target;
    }
    return null;
  }
  if ((m = /^DROP\s+INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+EXISTS\s+)?([\w".]+)/i.exec(s))) return indexes?.get(ident(m[1]).split('.').pop()) ?? null;
  if ((m = INDEX_RENAME.exec(s))) return indexes?.get(ident(m[1]).split('.').pop()) ?? null;
  if (/^SELECT\s+platform\.ensure_month_partitions\b/i.test(s)) return null; // a month: depends on the day
  if ((m = /^SELECT\s+platform\.\w+\s*\(\s*'([\w".]+)'\s*::\s*regclass/i.exec(s))) return ident(m[1]);
  if ((m = /^CREATE\s+(?:UNLOGGED\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w".]+)\s+PARTITION\s+OF\s+([\w".]+)\s+DEFAULT\b/i.exec(s))) return ident(m[2]);
  if (/^CREATE\s+(?:UNLOGGED\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[\w".]+\s+PARTITION\s+OF\b/i.test(s)) return null; // a month: depends on the day
  if ((m = /^CREATE\s+(?:UNLOGGED\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\w".]+)/i.exec(s))) return ident(m[1]);
  if ((m = /^ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?([\w".]+)/i.exec(s))) return ident(m[1]);
  if ((m = /^CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+NOT\s+EXISTS\s+)?(?:(?!ON\s)[\w"]+\s+)?ON\s+(?:ONLY\s+)?([\w".]+)/i.exec(s))) return ident(m[1]);
  if ((m = /^SELECT\s+platform\.apply_\w+?_rls\s*\(\s*'([\w".]+)'/i.exec(s))) return ident(m[1]);
  if ((m = /^(?:CREATE|DROP)\s+POLICY\s+(?:IF\s+EXISTS\s+)?[\w"]+\s+ON\s+([\w".]+)/i.exec(s))) return ident(m[1]);
  return null;
}

/** A foreign key statement's guard: the script applies it only when both tables exist and the key does not. */
function keyGuard(stmt) {
  const m = /^ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:ONLY\s+)?([\w".]+)\s+ADD\s+CONSTRAINT\s+([\w"]+)\s+FOREIGN\s+KEY\s*\(([^)]*)\)\s*REFERENCES\s+([\w".]+)/i.exec(stmt);
  if (!m) return null;
  return { table: ident(m[1]), constraint: ident(m[2]), columns: m[3].split(',').map(ident), references: ident(m[4]) };
}

/**
 * The package statements a ticket's file must reproduce, in the order the package applies them.
 * `files` is [{ name, text }] for one database. The script applies these to a copy of the previous
 * state and lets PostgreSQL say what the result is, so nothing here has to normalise SQL.
 */
export function ticketStatements(files, ticket) {
  const ordered = [...files].sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
  const want = new Set(ticket.tables.map(ident));
  const keys = new Set((ticket.constraints ?? []).map(ident));
  const out = [];
  const helpers = []; // after-r1 functions, kept in place until we know whether a picked statement calls one
  const indexes = new Map();
  for (const { name: file, text } of ordered) {
    for (const sql of sqlStatements(text)) {
      const fn = /^CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+([\w".]+)/i.exec(sql)?.[1];
      if (ticket.kind === 'baseline') {
        // 000-002 whole; the helper functions every later migration calls: those at the top of 920
        // and 930, and any an after-r1 file adds (V0102 adds platform.apply_append_audit_rls).
        if (/^00[0-2]-/.test(file) || (fn && /^(9[23]0-|V\d)/.test(file))) out.push({ file, sql });
        continue;
      }
      const guard = keyGuard(sql);
      if (ticket.kind === 'foreign-keys') {
        if (guard && keys.has(guard.constraint)) out.push({ file, sql, guard });
        continue;
      }
      if (fn && /^V\d/.test(file)) {
        const entry = { file, sql, helper: ident(fn) };
        helpers.push(entry);
        out.push(entry);
        continue;
      }
      const target = statementTarget(sql, indexes);
      // Which table each index is on, for a later DROP INDEX or ALTER INDEX that names only the index.
      const made = /^CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:CONCURRENTLY\s+)?(?:IF\s+NOT\s+EXISTS\s+)?((?!ON\s)[\w"]+)\s+ON\b/i.exec(sql);
      if (made && target) indexes.set(ident(made[1]), target);
      for (const one of /^DO\b/i.test(sql) ? doInner(sql) : [sql]) {
        const renamed = INDEX_RENAME.exec(one);
        if (renamed && indexes.has(ident(renamed[1]).split('.').pop())) indexes.set(ident(renamed[2]), indexes.get(ident(renamed[1]).split('.').pop()));
      }
      if (target && want.has(target)) out.push({ file, sql, ...(guard ? { guard } : {}) });
      else if (ticket.forward && guard && want.has(guard.references)) out.push({ file, sql, guard: { ...guard, incoming: true } });
    }
  }
  // An after-r1 helper goes with a table only when one of the table's statements calls it; the
  // baseline carries it otherwise.
  const called = (h) => out.some((s) => !s.helper && s.sql.toLowerCase().includes(`${h.helper}(`));
  return out.filter((s) => !s.helper || called(s)).map(({ helper: _h, ...s }) => s);
}

/** One database's check for expected-schema.json: the tables' shape and the statements behind it. */
export function expectedCheck(model, ticket, statements, { database, sources = [] } = {}) {
  const out = {};
  const absent = [];
  for (const name of ticket.tables) {
    const t = model.tables.get(ident(name));
    if (!t) { absent.push(name); continue; }
    const { name: _n, ...shape } = t;
    out[t.name] = shape;
  }
  const touched = new Set(Object.keys(out));
  const keysFound = new Set(statements.map((s) => s.guard?.constraint).filter(Boolean));
  const keysMissing = (ticket.constraints ?? []).filter((c) => !keysFound.has(ident(c)));
  return {
    database,
    migration: ticket.migration,
    kind: ticket.kind,
    sources,
    tables: out,
    statements,
    ...(absent.length ? { notInPackageDdl: absent } : {}),
    ...(keysMissing.length ? { keysNotInPackageDdl: keysMissing } : {}),
    ...(model.notModelled.some((n) => touched.has(n.table))
      ? { notModelled: model.notModelled.filter((n) => touched.has(n.table)) } : {}),
  };
}

/** Kept for the parser's own check: the shape of `tables` alone, as expected-schema.json had it. */
export function expectedSchema(model, tables, { database, migration } = {}) {
  return expectedCheck(model, { kind: 'tables', migration, tables }, [], { database });
}

// Package files are the same for every ticket in one pull of a whole board; held for a minute.
const ddlCache = new Map();
async function packageText(client, file) {
  const hit = ddlCache.get(file);
  if (hit && Date.now() - hit.at < 60_000) return hit.text;
  const answer = await client.file(file);
  if (!answer.ok) return null; // a failed read is not held: the next pull asks again
  ddlCache.set(file, { at: Date.now(), text: answer.text });
  return answer.text;
}

/** Forget the held package files (for the checks, which change what the stand-in serves). */
export function forgetPackageFiles() {
  ddlCache.clear();
}

/**
 * Writes expected-schema.json into a [DB] ticket's folder. Returns what README.md says about it,
 * or null for a ticket that is not a database migration. Never the reason a pull fails: a package
 * without the DDL, or a file that will not read, is said in README.md instead. The pull has already
 * removed the previous pull's copy, so a failure here never leaves an old one behind.
 */
async function writeExpectedSchema(client, wp, touches, folder, release) {
  const ticket = databaseTicket(wp, touches);
  if (!ticket) return null;
  try {
    if (ticket.kind === 'tables' && !ticket.tables.length) {
      throw new Error('the ticket links no tables, so there is nothing to compare');
    }
    const backend = await client.layer('backend');
    const files = (backend?.migrations?.files ?? []).map((f) => f.name);
    const where = backend?.migrations?.tables ?? {};
    const dbOf = (t) => String(where[ident(t)]?.file ?? '').split('/')[0] || null;
    const databases = ticket.kind === 'baseline'
      ? ['tenant', 'control'].filter((d) => files.some((f) => f.startsWith(`${d}/`)))
      : [ticket.database ?? ticket.tables.map(dbOf).find(Boolean) ?? 'tenant'];
    const checks = [];
    for (const database of databases) {
      const mine = files.filter((f) => f.split('/')[0] === database && f.split('/')[1]);
      // The baseline reads 000-002 and the helpers in 920, 930 and the V01nn files; the others read every file of their
      // database, since a table's statements are spread over its 010 file, 900-930 and the V01nn files.
      const wanted = ticket.kind === 'baseline' ? mine.filter((f) => /^((00[0-2]|9[23]0)-|V\d)/.test(f.split('/')[1])) : mine;
      const texts = [];
      for (const f of wanted) {
        const text = await packageText(client, `backend/${f}`);
        if (text === null) throw new Error(`backend/${f} would not read`);
        texts.push({ name: f.split('/')[1], text });
      }
      if (!texts.length) throw new Error(`no DDL for ${database} in this package`);
      const statements = ticketStatements(texts, ticket);
      const used = [...new Set(statements.map((s) => s.file))].map((f) => `backend/${database}/${f}`);
      checks.push(expectedCheck(schemaModel(texts), ticket, statements, { database, sources: used }));
    }
    const body = {
      about: 'What this ticket\'s migration must leave behind, from the package DDL: the tables\' end state, and '
        + 'the package statements that make it. node .claude/scripts/db-ticket.mjs <ticket> applies those statements '
        + 'to a copy of the previous state and compares the result with the ticket\'s file. Written by adam_pull; do not edit.',
      ...(release?.current ? { release: release.current } : {}),
      checks,
    };
    await writeFile(path.join(folder, 'expected-schema.json'), json(body));
    return {
      ...ticket, written: true, databases,
      tables: Object.keys(checks[0]?.tables ?? {}).length,
      statements: checks.reduce((n, c) => n + c.statements.length, 0),
      absent: checks.flatMap((c) => [...(c.notInPackageDdl ?? []), ...(c.keysNotInPackageDdl ?? [])]),
    };
  } catch (error) {
    return { ...ticket, written: false, error: error.message };
  }
}

function databaseSection(db, key) {
  if (!db) return '';
  let out = '\n## Checking this migration\n\n';
  if (!db.written) {
    return `${out}The expected end state could not be written (${db.error}), so \`db-ticket.mjs\` cannot check this `
      + 'ticket. Check the file by hand against `adam_table` and the package DDL, run '
      + '`node .claude/scripts/db-ticket.mjs --full <database>` before the merge request, and say both in the comment.\n';
  }
  const what = db.kind === 'baseline' ? 'the schemas, extensions, register and helper functions'
    : db.kind === 'foreign-keys' ? `the ${db.statements} cross-schema keys`
      : `${db.tables} table${db.tables === 1 ? '' : 's'}`;
  out += `The file is ${db.databases.map((d) => `\`db/${d}/${db.migration}\``).join(' and ')}. `
    + `[expected-schema.json](expected-schema.json) holds what it must leave behind (${what}), from the package DDL.\n\n`
    + '```\n'
    + `node .claude/scripts/db-ticket.mjs ${key}\n`
    + '```\n\n'
    + 'It applies only this file to a copy of the database at the previous state, then applies it a second time '
    + '(not recorded), which must succeed and change nothing, so every statement must be safe to run twice. It '
    + 'applies the package\'s own statements to another copy and compares the two: every table, column, constraint, '
    + 'index, policy, function, type, privilege, owner and comment must be the same, and nothing outside this ticket '
    + 'may change, rows included. **MATCH is the evidence for done**: quote its result lines in the comment. Anything '
    + 'else names what differs; fix the file and run it again. A foreign key "left for a later migration" is not a '
    + 'difference. The first run can take minutes (it builds a template of the earlier files): give the command a '
    + 'timeout of 10 minutes.\n\n'
    + '**This replaces older instructions for a [DB] ticket**: the "empty database" or "previous release\'s schema" '
    + 'line in the ticket\'s Done when, and any local CLAUDE.md, `/ticket`, `/done`, `project-bible/setup/backend-patterns.md` '
    + 'or `project-bible/setup/quickstart.md` that says to rebuild every migration or run `dotnet build` and `dotnet test`. '
    + 'Do not rebuild the other migrations, and do not run dotnet unless this ticket changes C#. Before opening the merge '
    + `request, run ${db.databases.map((d) => `\`node .claude/scripts/db-ticket.mjs --full ${d}\``).join(' and ')} once: `
    + 'every migration applied once, in order, to an empty database, as SqlMigrationRunner does.\n\n'
    + 'No `.claude/scripts/db-ticket.mjs` in this folder? Run ADAM\'s setup on it again: it adds the files that '
    + 'are missing and changes nothing else.\n';
  if (db.absent.length) {
    out += `\nNot in the package DDL, so the check cannot pass until it is (a change request): ${db.absent.map((t) => `\`${t}\``).join(', ')}.\n`;
  }
  return out;
}


async function pullOne(client, key, base, when) {
  const answer = await client.service(`/api/work-packages/${encodeURIComponent(key)}?${await scoped(client)}`);
  if (answer.status === 428) return { key, needsSetup: true, error: answer.data?.detail };
  if (!answer.ok) return { key, error: answer.data?.detail ?? `HTTP ${answer.status}` };
  // `subtasks` and `partOf` from an ADAM with CHG-ADM-006; an older one sends neither and the README has neither.
  const { workPackage: wp, touches = [], blockedBy = [], subtasks, partOf = null } = answer.data;
  const release = await releaseFor(client, wp.key, touches)
    .catch((error) => ({ available: false, why: error.message }));
  const changes = await changesFor(client, wp.key).catch(() => null);

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
    const file = `${safeName(kind)}-${safeName(id)}.json`;
    // Always the latest release: what ADAM serves now.
    const [toolName, args] = lookupFor(kind, id);
    const result = await BY_NAME.get(toolName).run(client, args).catch((error) => ({ found: false, error: error.message }));
    const record = { kind, id, from: toolName, ...(release.current ? { release: release.current } : {}), ...result };
    await writeFile(path.join(folder, file), json(trimForPull(record)));
    if (record.found === false) missing.push({ kind, id });
    files.push({ kind, id, file });
  }

  if (release.previous && release.diff) {
    await writeFile(path.join(folder, 'spec-diff.md'), specDiff(wp, release, when));
  }
  await writeFile(path.join(folder, 'ticket.json'), json({
    pulledAt: when, workPackage: wp, touches,
    ...(release.available ? { release: { current: release.current, previous: release.previous } } : {}),
    ...(Array.isArray(changes) ? { changeRequests: changes } : {}),
    ...(blockedBy.length ? { blockedBy } : {}),
    ...(subtasks !== undefined ? { subtasks } : {}),
    ...(partOf ? { partOf } : {}),
  }));
  const db = await writeExpectedSchema(client, wp, touches, folder, release);
  await writeFile(path.join(folder, 'README.md'),
    ticketReadme(wp, files, missing, when, decisions, release, changes, blockedBy, { subtasks, partOf }, db));
  const notes = path.join(folder, 'notes.md');
  if (!(await stat(notes).catch(() => null))) {
    await writeFile(notes, `# Notes on #${wp.key}\n\nYours. adam_pull never overwrites this file.\n`);
  }
  const settled = (changes ?? []).filter((c) => c.status !== 'open');
  return {
    key: wp.key, subject: wp.subject, status: wp.status, milestone: wp.version || null,
    due: wp.dueDate || null, folder, linked: files.length, notFound: missing.length,
    ...(Array.isArray(wp.comments) ? { comments: wp.comments.length } : {}),
    ...(release.available ? { release: {
      current: release.current,
      latest: true,
      ...(release.previous ? { movedFrom: release.previous } : {}),
      ...(release.diff ? {
        changed: (release.diff.artefacts ?? []).filter((a) => ['changed', 'added', 'removed'].includes(a.status)).length,
        breaking: release.diff.breaking.map((b) => `${b.id || b.operation} (${b.role})`),
      } : {}),
      ...(release.diffError ? { diffError: release.diffError } : {}),
    } } : {}),
    ...(blockedBy.length ? { blockedBy: blockedBy.map((c) => ({ id: c.id, status: c.status, title: c.title, via: c.via })) } : {}),
    ...(Array.isArray(subtasks) && subtasks.length ? { subtasks: subtasks.length } : {}),
    ...(subtasks === null ? { subtasks: 'could not be read' } : {}),
    ...(partOf?.key ? { partOf: partOf.key } : {}),
    ...(db ? { database: db.written
      ? { migration: db.databases.map((d) => `db/${d}/${db.migration}`).join(' and '), kind: db.kind,
        expected: path.join(folder, 'expected-schema.json'), tables: db.tables, statements: db.statements }
      : { migration: db.migration, error: db.error } } : {}),
    ...(Array.isArray(changes) && changes.length ? { changeRequests: {
      total: changes.length,
      open: changes.filter((c) => c.status === 'open').map((c) => c.id),
      settled: settled.map((c) => `${c.id} ${c.status}`),
    } } : {}),
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
    + 'grouped by milestone, in the order the work is finished in: what you have started, then the '
    + "plan's build order. Each ticket has a folder under work/ with its description and "
    + 'everything it is linked to, at the latest release ADAM serves.\n';
  for (const [name, tickets] of groups) {
    out += `\n## ${name}\n\n| Ticket | Status | Due | Linked | Release | Blocked by | Folder |\n|---|---|---|---|---|---|---|\n`;
    for (const t of tickets) {
      const r = t.release;
      const tag = !r ? '' : r.movedFrom ? `${r.current} (moved from ${r.movedFrom}; see README.md)` : (r.current ?? '');
      out += `| #${t.key} ${t.subject.replace(/\|/g, '/')} | ${t.status} | ${t.due ?? ''} | ${t.linked} | ${tag} | ${(t.blockedBy ?? []).map((c) => c.id).join(', ')} | [work/${safeName(t.key)}](work/${safeName(t.key)}/README.md) |\n`;
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
      // A trailing path too - "shared/common" for contracts/shared/common.yaml - which a
      // README hands out and the stem-only match turned away (audit R016).
      const tail = (f) => fold(String(f).replace(/\.(ya?ml|json)$/i, ''));
      const file = files.find((f) => fold(f) === want) ?? files.find((f) => stem(f) === want)
        ?? files.find((f) => tail(f).endsWith(want) && String(name).includes('/'));
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
        // Both asked for, both answered: `operation` used to be dropped without a word
        // whenever `schema` came with it (audit R016).
        const op = wantOperation ? operations.find((n) => fold(n.name) === fold(wantOperation)) : null;
        return {
          found: true, contract: file, schema: { ...hit, ...(detail[hit.id] ?? {}) },
          ...(op ? { operation: { ...op, ...(detail[op.id] ?? {}) } } : {}),
          ...(wantOperation && !op ? { note: `no operation ${wantOperation} in ${file}` } : {}),
        };
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
      // Word by word: folding the whole query into one run of letters meant "order
      // transfer" only matched text containing "ordertransfer" (audit R022). Every word
      // must appear; where it appears decides the rank.
      const words = String(q).split(/[\s,/]+/).map(fold).filter(Boolean);
      const hits = [];
      for (const e of pool) {
        const id = fold(e.id);
        const name = fold(e.name);
        const hay = `${id} ${name} ${fold(e.terms ?? '')}`;
        if (!words.every((w) => hay.includes(w))) continue;
        // An exact id beats an exact name beats every word in the id or name beats prose.
        const rank = id === want ? 0 : name === want ? 1
          : words.every((w) => id.includes(w) || name.includes(w)) ? 2 : 3;
        hits.push([rank, e]);
      }
      hits.sort((a, b) => a[0] - b[0] || String(a[1].id).length - String(b[1].id).length);
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

      // **Kept short per table, because the count is what grows.** Marketing
      // reached 130 tables and 60 KB with no essay in it — every row was ~470
      // characters of which the service name, nulls and a 300-character reason
      // were most. The service is said once when every table shares it, empty
      // fields are left out, and the reason is cut to its opening; adam_table
      // has the whole of it.
      const services = [...new Set(mine.map((t) => t.service).filter(Boolean))];
      const shared = services.length === 1 ? services[0] : null;

      return {
        found: true,
        module: hit,
        ...(shared ? { service: shared } : {}),
        tables: mine.map((t) => ({
          name: t.name,
          columns: t.columns,
          ...(t.derivedFrom ? { derivedFrom: t.derivedFrom } : {}),
          ...(!shared && t.service ? { service: t.service } : {}),
          ...(t.migration ? { migration: t.migration } : {}),
          ...(t.storageOnly
            ? { storageOnly: true, storageReason: trim(String(t.storageReason ?? '').replace(/^storage only\s*—\s*/i, ''), 120) }
            : {}),
        })),
        next: 'pass one of those names to adam_table for its columns, keys and the whole reason',
      };
    },
  },

  {
    name: 'adam_board',
    description:
      'What is open and assigned to you in OpenProject, as a table of tasks and the epic or '
      + 'module each one comes from. Use at the start of a session to see what you are meant to '
      + 'be doing, or when a branch name or a ticket number turns up and you need the context '
      + 'behind it. Subtasks and the artefacts each ticket touches come back with it and are '
      + 'held rather than shown — ask for them by ticket when you want them. Each row says which open '
      + 'blocking change requests affect it (`blocked`: the CR ids; blank is workable). '
      + '`startHere` is where to start when the person asks to work without naming a ticket (a /ticket with no '
      + 'number): the first ticket they can finish, or its first open sub-task that is theirs. Start it and say '
      + 'which and why; never ask for a number. A subtasks count of ? (with `subtaskNote`) means the sub-tasks '
      + 'could not be read, not that there are none. '
      + BLOCKER_RULE,
    inputSchema: {
      type: 'object',
      properties: {
        only: {
          type: 'string',
          enum: ['workable', 'blocked'],
          description: '"workable": only the tickets no open blocking change request affects - the ones you can '
            + 'finish now, in board order. "blocked": only the ones one does. Leave out for the whole board.',
        },
        subtasks: {
          type: 'boolean',
          description:
            'Show the subtasks rather than only counting them. They are fetched either way; '
            + 'this decides whether they are put in front of the person.',
        },
        limit: {
          type: 'number',
          description:
            'How many tickets to show, from the top of the build order (default 30, at most 50). '
            + '`total` always says how many there are.',
        },
      },
    },
    async run(client, args = {}) {
      const only = ['workable', 'blocked'].includes(args?.only) ? args.only : '';
      const answer = await client.service(`/api/board/mine?${await scoped(client, only ? { only } : {})}`);
      // 428 is "connect OpenProject first" — a thing to go and do, not a
      // failure. Relayed as the sentence the server wrote rather than flattened
      // into "the tool failed".
      if (answer.status === 428) {
        return { found: false, needsSetup: true, error: answer.data?.detail };
      }
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };

      const board = answer.data;
      // **The top of the order, not the whole of it.** Once the plan was assigned, one person held
      // hundreds of tickets and the board came back at 364 KB — three times the ceiling, so the
      // answer was a refusal. The order is the build order, so the first rows are the ones to do
      // next; the rest are counted, not dropped silently.
      const limit = Math.min(Math.max(Math.trunc(Number(args?.limit)) || 30, 1), 50);
      const all = board.items ?? [];
      const items = all.slice(0, limit);

      // **The table is the answer, and it is deliberately five columns.** The
      // board used to hand back every field OpenProject knows about every
      // ticket — lock versions, timestamps, spent hours, the lot — which is a
      // page of JSON to answer "what am I doing today". What is kept is what
      // somebody reads down a list: which ticket, what it is, what it is part
      // of, where it has got to, when it is due.
      // In the order the server gives, which is the order the work is finished in: what you have
      // started, then the plan's build order (see /api/board/mine). Never re-sorted here.
      // The release column only once there is a release. `r1 -> r2` is a ticket
      // last pulled at r1 while ADAM serves r2: the next pull is at r2 (every
      // pull is at the latest release) and says what changed.
      const served = board.release?.tag ?? null;
      // False only from an ADAM whose project read failed: the counts are then unknown, shown as ?, never 0.
      const subtasksKnown = board.subtasksKnown !== false;
      const rows = items.map((t) => ({
        order: t.buildOrder ?? '',
        ticket: t.key,
        task: t.subject,
        module: t.module ? `${t.module.key} — ${t.module.subject}` : '—',
        status: t.status,
        due: t.dueDate ?? '',
        percent: t.percentDone ?? 0,
        subtasks: subtasksKnown ? (t.subtasks ?? []).length : '?',
        ...(served ? { release: t.pin ? (t.pinStale ? `${t.pin} -> ${served}` : t.pin) : '' } : {}),
        // The open blocking CRs that affect it (CHG-ADM-004). Blank is workable now.
        blocked: (t.blockedBy ?? []).map((c) => c.id).join(', '),
      }));
      const blockedNotes = {};
      for (const t of items) {
        if ((t.blockedBy ?? []).length) {
          blockedNotes[t.key] = t.blockedBy.map((c) => `${c.id} (${c.status}) "${c.title}" - via ${c.via}`);
        }
      }
      const firstWorkable = items.find((t) => !(t.blockedBy ?? []).length) ?? null;

      // Held back rather than left out. Fetching them costs nothing extra —
      // they come from the same project read — so the choice is only about
      // what goes on screen, and a board answer buried in forty subtask rows
      // is not a board answer.
      const held = {};
      for (const t of items) {
        if ((t.subtasks ?? []).length) held[t.key] = t.subtasks;
      }
      const touching = {};
      for (const t of items) {
        if ((t.touches ?? []).length) touching[t.key] = t.touches;
      }

      const wanted = args?.subtasks === true;
      return {
        found: board.total > 0,
        total: board.total,
        shown: items.length,
        ...(all.length > items.length
          ? { more: `${all.length - items.length} more after these in the build order`
              + (limit < 50 ? '; pass a larger `limit` (up to 50) to see more of them' : '') }
          : {}),
        // Kept, because an empty board reads as "nothing assigned to me" and
        // the truth may be "nothing has been loaded into the project yet".
        ...(board.note ? { note: board.note } : {}),
        // Which OpenProject project this board is read from, so "nothing
        // assigned" is never mistaken for "nothing assigned anywhere".
        ...(board.openproject ? { openprojectProject: board.openproject } : {}),
        // `subtasks` is the column /board and the display text below have always named (CHG-ADM-006).
        columns: served
          ? ['order', 'ticket', 'task', 'module', 'status', 'due', 'subtasks', 'release', 'blocked']
          : ['order', 'ticket', 'task', 'module', 'status', 'due', 'subtasks', 'blocked'],
        // How many of the whole board no open blocking CR affects, and how many one does (CHG-ADM-004).
        ...(board.workable !== undefined ? { workable: board.workable, blockedCount: board.blocked } : {}),
        ...(only ? { only } : {}),
        ...(Object.keys(blockedNotes).length ? { blockedBy: blockedNotes } : {}),
        ...(firstWorkable ? { firstWorkable: firstWorkable.key } : {}),
        // Where /ticket with no number starts: ADAM's answer over the whole board (CHG-ADM-006).
        ...(board.startHere ? { startHere: board.startHere } : {}),
        ...(subtasksKnown ? {} : {
          subtaskNote: 'Sub-tasks could not be read from OpenProject, so the subtasks column shows ? (not known), '
            + 'not 0. Ask again in a minute.',
        }),
        ...(served ? {
          release: served,
          releaseNote: `You are always on the latest release (${served}). A release like r1 -> ${served} means the `
            + `ticket was last pulled at r1; the next pull (adam_pull) is at ${served} and says what changed. `
            + 'Nothing to choose. Blank is not pulled yet.',
        } : {}),
        orderedBy: "what you have started first, then the plan's build order; the same every time",
        rows,
        // Said when it is false, so a column of dashes is read as "could not
        // ask" rather than as "these belong to nothing".
        ...(board.modulesKnown === false
          ? { moduleNote: 'The project tree could not be read, so no module could be named.' }
          : {}),
        ...(wanted ? { subtasks: held } : {}),
        ...(wanted ? {} : { subtasksHeld: Object.keys(held).length }),
        touches: touching,
        display: wanted
          ? 'Show `rows` as a markdown table using `columns`, then the subtasks under their ticket; if `subtaskNote` is '
            + 'present, say it in one line. '
            + 'If `more` is present, say it in one line under the table.'
          : 'Show `rows` as a markdown table using `columns`; if `subtaskNote` is present, say it in one line; if `more` is present say it in one '
            + 'line under the table; if any `release` reads "rN -> rM", say in one line that the next pull of '
            + 'those tickets is at the latest release and shows what changed; if any `blocked` is filled, say in '
            + 'one line that those wait on the CRs named (`blockedBy` says how each is affected) and that '
            + '`firstWorkable` is the first ticket that can be finished now; nothing else. Do not list the '
            + 'subtasks or the touched artefacts, and do not summarise them — the `subtasks` '
            + 'column already gives the count. Call this tool again with subtasks: true if the '
            + 'person asks to see them.',
      };
    },
  },

  {
    name: 'adam_team',
    description:
      "Read-only: what your teammates are working on in OpenProject. Use for questions like 'what is "
      + "Hrushikant working on', 'what has Deep got open', 'what's everyone doing', 'who is busy / who is "
      + "free', or 'who is on the module ticket N is in' (read ticket N with adam_work first for its parent, "
      + 'then look for that parent here). With `person` (a name; a first name or the start of one is '
      + "enough, any case) it gives that person's open tickets (in progress first, then stalled, awaiting QA "
      + 'and New) and what they finished in the last 14 days (or `days`, up to 60): closed or moved to Ready '
      + 'for QA, each with its status, type, date and parent. Without it, it gives everybody on the project: '
      + 'per person, how many tickets are in progress, awaiting QA, stalled (on hold or blocked), open, and '
      + 'finished lately, and what each has in progress. Your own work is adam_board. Read as you, '
      + 'with your OpenProject token, so it shows only what your OpenProject account can see.',
    inputSchema: {
      type: 'object',
      properties: {
        person: {
          type: 'string',
          description:
            'A teammate\'s name, e.g. "Hrushikant", "hrushi" or "Patkar". Leave out for the whole team. '
            + 'If it matches nobody or more than one person, the answer lists the names to choose from.',
        },
        limit: {
          type: 'number',
          description: 'How many ticket rows to show (default 30, at most 80). Counts always cover all of them.',
        },
        days: {
          type: 'number',
          description: 'With `person`: how far back the finished list reaches, in days (default 14, at most 60).',
        },
        refresh: {
          type: 'boolean',
          description: 'Whole team only: read OpenProject again rather than the copy held for two minutes.',
        },
      },
    },
    async run(client, args = {}) {
      const limit = Math.min(Math.max(Math.trunc(Number(args?.limit)) || 30, 1), 80);
      const person = String(args?.person ?? '').trim();
      const days = Math.min(Math.max(Math.trunc(Number(args?.days)) || 14, 1), 60);
      const answer = person
        ? await client.service(`/api/board/person?${await scoped(client, { who: person, days: String(days) })}`)
        : await client.service(`/api/board/team?${await scoped(client, args?.refresh ? { refresh: '1' } : {})}`);
      if (answer.status === 428) return { found: false, needsSetup: true, error: answer.data?.detail };
      if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const data = answer.data;
      const partOf = (t) => (t.parent ? `${t.parent}${t.parentSubject ? ` — ${t.parentSubject}` : ''}` : '—');
      const day = (stamp) => String(stamp ?? '').slice(0, 10);

      if (person) {
        if (!data.person) {
          return {
            found: false,
            [data.match === 'ambiguous' ? 'ambiguous' : 'unknown']: true,
            asked: person,
            candidates: (data.candidates ?? []).map((c) => c.name),
            note: data.note,
            display: 'Say in one line that the name was ambiguous or not found, list `candidates`, and ask '
              + 'which one they meant (or call adam_team again with the full name).',
          };
        }
        const all = data.items ?? [];
        const rows = all.slice(0, limit).map((t) => ({
          ticket: t.key,
          task: t.subject,
          partOf: partOf(t),
          status: t.status,
          due: t.dueDate ?? '',
          order: t.buildOrder ?? '',
        }));
        // Most recent first, as the service sends them: closed, and moved to an awaiting-QA status, in
        // the window. `lastChanged` is OpenProject's updatedAt (see finishedNote).
        const doneAll = data.finished ?? [];
        const finished = doneAll.slice(0, limit).map((t) => ({
          ticket: t.key,
          task: t.subject,
          type: t.type ?? '',
          status: t.status,
          lastChanged: day(t.lastChangedAt ?? t.updatedAt),
          partOf: partOf(t),
        }));
        return {
          found: true,
          person: data.person.name,
          ...(data.match === 'partial' ? { matchedFrom: person } : {}),
          open: data.total,
          inProgress: data.inProgress,
          awaitingQA: data.awaitingQA,
          stalled: data.stalled,
          shown: rows.length,
          ...(all.length > rows.length
            ? { more: `${all.length - rows.length} more open after these; pass a larger \`limit\` (up to 80) to see them` }
            : {}),
          columns: ['ticket', 'task', 'partOf', 'status', 'due', 'order'],
          rows,
          finishedWindowDays: data.windowDays,
          finishedTotal: data.finishedTotal ?? doneAll.length,
          finishedColumns: ['ticket', 'task', 'type', 'status', 'lastChanged', 'partOf'],
          finished,
          ...(doneAll.length > finished.length
            ? { moreFinished: `${doneAll.length - finished.length} more finished in the window after these; pass a larger \`limit\`` }
            : {}),
          finishedNote: 'Finished means closed, or moved to a QA/review status, in the window; `status` says which. '
            + '`lastChanged` is when OpenProject last changed the ticket (updatedAt): there is no separate '
            + 'closing date, so a later edit moves it too.',
          ...(data.note ? { note: data.note } : {}),
          orderedBy: 'in progress, then stalled, then awaiting QA, then New; within each the build order, priority, due date',
          display: `Say "${data.person.name}: N open (a in progress, b awaiting QA, c stalled); K finished in the last `
            + `${data.windowDays} days" in one line, then show \`rows\` as a markdown table using \`columns\`, in the `
            + 'order given. Then a heading "Finished in the last N days" and `finished` as a second table using '
            + '`finishedColumns`, most recent first, with one line under it saying the date is the last change in '
            + 'OpenProject; or "nothing finished in the last N days". If `more` or `moreFinished` is present, say '
            + 'it in one line. Nothing else.',
        };
      }

      const people = data.people ?? [];
      const row = (p) => {
        const current = p.current ?? [];
        const named = current.slice(0, 3).map((t) => `#${t.key} ${trim(t.subject, 48)}`);
        return {
          person: p.name,
          inProgress: p.inProgress,
          awaitingQA: p.awaitingQA,
          stalled: p.stalled,
          open: p.open ?? '?',
          finished14d: p.finishedRecently,
          workingOn: named.length
            ? named.join('; ') + (current.length > 3 ? `; +${current.length - 3} more` : '')
            : '—',
        };
      };
      const busy = (p) => p.inProgress || p.awaitingQA || p.stalled || p.open || p.finishedRecently;
      const rows = people
        .filter(busy)
        .sort((a, b) => (b.inProgress - a.inProgress) || (b.awaitingQA - a.awaitingQA)
          || ((b.open ?? 0) - (a.open ?? 0)) || a.name.localeCompare(b.name))
        .map(row);
      const idle = people.filter((p) => !busy(p)).map((p) => p.name);
      const tickets = people.flatMap((p) => (p.current ?? []).map((t) => ({
        person: p.name, ticket: t.key, task: t.subject, partOf: partOf(t), status: t.status, due: t.dueDate ?? '',
      })));
      const unassigned = data.unassigned ?? {};
      return {
        found: people.length > 0,
        windowDays: data.windowDays,
        asOf: data.asOf,
        ...(data.fromCache ? { heldFor: `${data.ageSeconds}s (refresh: true reads again)` } : {}),
        statusesMean: {
          inProgress: (data.inProgressStatuses ?? []).join(', ') || 'none on this instance',
          awaitingQA: (data.awaitingQAStatuses ?? []).join(', ') || 'none on this instance',
          stalled: (data.stalledStatuses ?? []).join(', ') || 'none on this instance',
          finished14d: data.finishedMeans,
        },
        columns: ['person', 'inProgress', 'awaitingQA', 'stalled', 'open', 'finished14d', 'workingOn'],
        rows,
        ...(idle.length ? { nothingAssigned: idle } : {}),
        ...((unassigned.inProgress || unassigned.awaitingQA || unassigned.stalled || unassigned.open)
          ? { unassigned: { open: unassigned.open ?? '?', inProgress: unassigned.inProgress,
            awaitingQA: unassigned.awaitingQA, stalled: unassigned.stalled } } : {}),
        ticketColumns: ['person', 'ticket', 'task', 'partOf', 'status', 'due'],
        tickets: tickets.slice(0, limit),
        ...(tickets.length > limit ? { moreTickets: `${tickets.length - limit} more in-progress tickets; pass a larger \`limit\`` } : {}),
        ...(data.note ? { note: data.note } : {}),
        display: 'Show `rows` as a markdown table using `columns`, busiest first, and if `nothingAssigned` is '
          + 'present say those names in one line. Show `tickets` (a table using `ticketColumns`) only when the '
          + 'person asked about specific tickets, a module or what someone is doing in detail. For one '
          + 'person in depth, call adam_team again with `person`. Nothing else.',
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
        find: {
          type: 'string',
          description: 'Jump to a section instead of paging: a heading anchor as a ticket links it '
            + '(e.g. "#gst-043-arabic-rtl-experience"), or any text. Returns the window starting at '
            + 'the first match and the line numbers of every other match.',
        },
      },
      required: ['path'],
    },
    /**
     * Windowed, because a contract is 756 KB and the result ceiling is 120 KB.
     * A file that arrives as a refusal teaches nothing; one that arrives as its
     * first 400 lines with a note saying how many there are lets the caller ask
     * for the part it wants.
     */
    async run(client, { path, from = 1, lines = 400, find }) {
      const answer = await client.file(path);
      if (!answer.ok) {
        return {
          found: false,
          status: answer.status,
          // The server now says what is wrong - no such file, a folder, or a kind it does not
          // serve - instead of one 403 that read as a permission problem (audit R013).
          error: answer.status === 404 ? `no file at "${path}"`
            : answer.status === 400 || answer.status === 415 ? (answer.text || `"${path}" is not a readable file`).slice(0, 300)
            : answer.text.slice(0, 300),
        };
      }
      // CRLF too: the package's files are Windows line endings, and a `\r` left on each line stops
      // `.` matching in the heading test below, so no anchor was ever found.
      const all = answer.text.split(/\r?\n/);
      let start = Math.max(1, Number(from) || 1);
      let matches;
      if (find) {
        // A ticket links a spec section by anchor; a 6,000-line generated doc could only be
        // paged blind to reach it (audit R009). Match the heading the anchor was made from
        // (lower-cased, punctuation dropped, spaces as hyphens), else the text itself.
        const slug = (t) => t.toLowerCase().replace(/[^\w\s-]/g, '').trim().replace(/\s+/g, '-');
        const anchor = find.startsWith('#') ? find.slice(1).toLowerCase() : null;
        const needle = find.toLowerCase();
        matches = [];
        all.forEach((line, i) => {
          const heading = line.match(/^#{1,6}\s+(.*)$/);
          if (anchor ? heading && slug(heading[1]) === anchor : line.toLowerCase().includes(needle)) matches.push(i + 1);
        });
        if (!matches.length) return { found: true, path, totalLines: all.length, matches: [], note: `nothing matches "${find}"` };
        start = matches[0];
      }
      const count = Math.max(1, Math.min(Number(lines) || 400, 2000));
      // Lines and bytes both: a window of 400 long lines can still overflow the tool
      // result, and then nothing arrives at all (audit R011). Stop at ~60 KB and say where.
      const slice = [];
      let size = 0;
      for (const line of all.slice(start - 1, start - 1 + count)) {
        if (slice.length && size + line.length > 60000) break;
        slice.push(line.length > 20000 ? `${line.slice(0, 20000)} … [line cut at 20,000 of ${line.length} characters]` : line);
        size += Math.min(line.length, 20000) + 1;
      }
      const end = start + slice.length - 1;

      return {
        found: true,
        path,
        totalLines: all.length,
        showing: `${start}-${end}`,
        ...(matches && matches.length > 1 ? { otherMatches: matches.slice(1, 50) } : {}),
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
      + 'the files, then the comment thread, oldest first), ticket.json, one file per linked screen, journey, contract, table, service, '
      + 'and module (linked ADRs are listed, not pulled), plus notes.md for your own notes. A [DB] ticket whose '
      + 'subject names its migration file also gets expected-schema.json, the end state of its tables and the statements that make it, from the '
      + 'package DDL, which `node .claude/scripts/db-ticket.mjs <ticket>` compares a database with. You are always on '
      + 'the latest release: every pull serves the release ADAM serves now (r1, r2, …), and when that release is '
      + 'newer than the ticket\'s previous pull, README.md says what changed and spec-diff.md has the diffs. There '
      + 'is no release to choose and nothing to ask about it. README.md also lists, near the top, every change '
      + 'request raised from the ticket with its decision and the release that carries it, and above them a '
      + '"Blocked by" section naming the open blocking change requests that affect the ticket (`blockedBy`). '
      + 'A blocked ticket is not built: always raise a CR for a new blocker, propose the ticket On hold naming '
      + 'the CR, and move to the next ticket you can finish (adam_board with only: "workable"). README.md lists the '
      + 'ticket\'s sub-tasks at every depth under "Sub-tasks" (status and who holds each, in the order they are '
      + 'done), and a sub-task\'s README names its parent on a "Part of" line. With no `key`, pulls '
      + 'every open ticket assigned to you and writes .adam/board.md grouped by milestone; to start work without a '
      + 'ticket number, do not pull the whole board: adam_board\'s `startHere` is the ticket to start. **Use '
      + 'this at the start of work on a ticket**, then read the files you need instead of holding '
      + 'everything in the conversation. Always pass `dir`: the absolute path of the folder you are '
      + 'working in. .adam/ is git-ignored, so Grep skips it unless you pass --no-ignore; Read works as usual.',
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
        const r = one.release;
        let next = one.linked
          ? 'Read README.md first, then the linked files it lists as you need them.'
          : unlinkedHint({ subject: one.subject });
        if (r?.movedFrom && r.diffError) {
          next = `You are always on the latest release (${r.current}); this pull moved the ticket from `
            + `${r.movedFrom}, but what changed could not be read (${r.diffError}). Say so in one line. ${next}`;
        } else if (r?.movedFrom) {
          next = `You are always on the latest release (${r.current}); this pull moved the ticket from `
            + `${r.movedFrom}. Tell the person in one line what changed since the previous pull: `
            + `${r.changed ?? 0} linked artefact${r.changed === 1 ? '' : 's'} changed`
            + `${r.breaking?.length ? `, including breaking change ${r.breaking.join(', ')}` : ''} `
            + '(README.md lists them; spec-diff.md has the diffs). Then build against the files as they are. '
            + `${next}`;
        } else if (r?.current) {
          next = `You are always on the latest release (${r.current}). ${next}`;
        }
        const crs = one.changeRequests;
        if (crs) {
          next += ` README.md lists ${crs.total} change request${crs.total === 1 ? '' : 's'} raised from this ticket`
            + ' under "Change requests on this ticket": follow the settled decisions'
            + `${crs.open.length ? `, and wait on the part ${crs.open.join(', ')} cover${crs.open.length === 1 ? 's' : ''}` : ''}.`;
        }
        if (typeof one.subtasks === 'number') {
          next += ` It has ${one.subtasks} sub-task${one.subtasks === 1 ? '' : 's'}, listed under "Sub-tasks" in `
            + 'README.md in the order they are done; pull one before working on it.';
        } else if (one.subtasks === 'could not be read') {
          next += ' Its sub-tasks could not be read from OpenProject: say so in one line.';
        }
        if (one.partOf) next += ` It is part of #${one.partOf} (the "Part of" line in README.md).`;
        if (one.blockedBy?.length) {
          next = `Blocked: ${one.blockedBy.map((c) => `${c.id} (${c.status}, via ${c.via})`).join('; ')}. `
            + 'Read the "Blocked by" section of README.md. Do not build the blocked part and do not work around it: '
            + 'propose the ticket On hold naming the CR (adam_propose, applied only after the person says yes), then '
            + 'find the next ticket you can finish with adam_board only: "workable". ' + next;
        }
        if (one.database?.expected) {
          next += ` A database ticket: write ${one.database.migration}, then check it with `
            + `\`node .claude/scripts/db-ticket.mjs ${one.key}\` (README.md, "Checking this migration"). MATCH is the `
            + 'evidence for done; it replaces older [DB] instructions, and there is no dotnet build or dotnet test '
            + 'unless the ticket changes C#.';
        }
        if (r?.current) {
          next += ' Older /ticket instructions that mention re-pinning are out of date: there is nothing to re-pin.';
        }
        return {
          found: true,
          ...one,
          read: path.join(one.folder, 'README.md'),
          next,
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
        pulled: pulled.map(({ key: k, subject, status, milestone, linked, blockedBy, error }) =>
          ({ key: k, subject, status, milestone, linked,
            ...(blockedBy?.length ? { blockedBy: blockedBy.map((c) => c.id) } : {}), ...(error ? { error } : {}) })),
        ...(answer.data.total > items.length
          ? { more: `${answer.data.total - items.length} more assigned; raise limit or pull them by key` }
          : {}),
        ...(answer.data.note ? { note: answer.data.note } : {}),
        // For an older /ticket that, given no number, called this with no key: where to start (CHG-ADM-006).
        ...(answer.data.startHere ? {
          startHere: answer.data.startHere,
          next: `If the person asked to start work without naming a ticket, start #${answer.data.startHere.key}; `
            + 'do not ask for a number.',
        } : {}),
      };
    },
  },

  {
    name: 'adam_repin',
    description:
      'Not needed: you are always on the latest release, because every adam_pull serves the release ADAM '
      + 'serves and moves the ticket to it by itself. Kept only so older instructions that name it still '
      + 'work: it moves the ticket to the latest release and, with `dir`, pulls it again. Prefer adam_pull. '
      + 'Changes nothing in OpenProject.',
    inputSchema: {
      type: 'object',
      properties: {
        key: { type: 'string', description: 'Work package number, e.g. 6046' },
        dir: { type: 'string', description: 'Absolute path of the folder you are working in, to pull it again' },
        breaking: {
          type: 'boolean',
          description: 'Kept for older instructions; recorded in the history and changes nothing else',
        },
        note: { type: 'string', description: 'Optional: why, in a line - kept in the pin history' },
      },
      required: ['key'],
    },
    async run(client, { key, dir, breaking = false, note = '' }) {
      const number = String(key ?? '').replace(/^#/, '');
      const answer = await client.service(`/api/work-packages/${encodeURIComponent(number)}/pin`, {
        method: 'POST',
        body: { project_id: (await client.projectId()) ?? '', reason: breaking ? 'breaking' : 'accept', note },
      });
      if (!answer.ok) return { ok: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
      const state = answer.data;
      const was = state.log?.[0]?.from || null;
      const result = {
        ok: true,
        moved: Boolean(state.recorded),
        pinned: state.pin?.tag ?? null,
        ...(state.recorded && was ? { from: was } : {}),
        ...(state.note ? { note: state.note } : {}),
      };
      if (!state.recorded || !dir) {
        return {
          ...result,
          next: `You are always on the latest release${result.pinned ? ` (${result.pinned})` : ''}; adam_pull keeps `
            + 'it there by itself, so this tool is never needed. Pull the ticket (adam_pull) for its files.',
        };
      }
      const base = await workFolder(dir);
      const when = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
      const again = await pullOne(client, number, base, when);
      return {
        ...result,
        pulled: again.error ? { error: again.error } : { folder: again.folder, linked: again.linked, release: again.release },
        next: `You are always on the latest release (${result.pinned}); the files under .adam/work/${number}/ are `
          + 'that release. Read README.md again before going on. Next time adam_pull alone does this.',
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
      + 'or `ticket`. With `from` and/or `to` (release tags), the release notes: what was settled between '
      + 'two releases, with a markdown note. **Check this before drafting a new one** - somebody may have raised it already - '
      + 'and before building against an artefact that has an open or accepted request.',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'A change request, e.g. CR-007' },
        status: { type: 'string', description: 'open, accepted, rejected or done; comma-separated for several' },
        kind: { type: 'string', description: 'Artefact kind, e.g. operation, schema, table, screen, flow' },
        target: { type: 'string', description: 'Artefact id, e.g. identity#requestGuestCode' },
        ticket: { type: 'string', description: 'OpenProject work package number' },
        from: {
          type: 'string',
          description: 'Release notes: the change requests settled (accepted or done) after this release tag, e.g. r1',
        },
        to: {
          type: 'string',
          description: 'Release notes: up to this release tag; default the one ADAM serves',
        },
      },
    },
    async run(client, { id, status, kind, target, ticket, from, to } = {}) {
      const project = (await client.projectId()) ?? '';
      if (from || to) {
        const query = new URLSearchParams({ project_id: project });
        if (from) query.set('from', from);
        if (to) query.set('to', to);
        const answer = await client.service(`/api/changes/release-notes?${query}`);
        if (!answer.ok) return { found: false, error: answer.data?.detail ?? `HTTP ${answer.status}` };
        const notes = answer.data;
        return {
          found: notes.total > 0,
          from: notes.from, to: notes.to, basis: notes.basis, total: notes.total,
          items: notes.items.map((c) => ({
            id: c.id, status: c.status, title: c.title, target: c.target, source: c.source,
            sourceRef: c.sourceRef, triage: c.triage, contractImpact: c.contractImpact,
            effortPoints: c.effortPoints, resolvedAt: c.resolvedAt, resolvedRef: c.resolvedRef,
          })),
          markdown: notes.markdown,
        };
      }
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
          ...(c.source ? { source: c.source } : {}),
          ...(c.triage ? { triage: c.triage } : {}),
          ...(c.contractImpact ? { contractImpact: c.contractImpact } : {}),
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
      + 'in `evidence` and give the ways it could be settled in `options`. ' + BLOCKER_RULE,
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
        // ---- intake (C8) ----
        source: {
          type: 'string', enum: ['developer', 'minutes', 'answer', 'design', 'audit'],
          description: 'Where the change came from. Default developer: a gap found while building a ticket.',
        },
        sourceRef: {
          type: 'string',
          description: 'The line that finds the source again: "MoM 30 Sep, item 4", a question id, an audit '
            + 'finding. For a developer gap it defaults to the ticket.',
        },
        approver: { type: 'string', description: 'Who agreed the change should be made. Required when contractImpact is breaking.' },
        triage: { type: 'string', enum: ['clarification', 'scope', 'defect'], description: 'What kind of change it is, if known' },
        when: { type: 'string', enum: ['now', 'later'], description: 'Whether it is needed for the current release or can wait' },
        artefacts: { type: 'array', items: { type: 'string' }, description: 'Every other artefact id it touches, beyond target' },
        contractImpact: {
          type: 'string', enum: ['none', 'additive', 'breaking'],
          description: 'What it does to a contract: nothing, a compatible addition, or a breaking change',
        },
        effortPoints: { type: 'number', description: 'Change in effort, in points, signed (3, -1, 0.5)' },
        clientSignoff: {
          type: 'string',
          description: 'Who on the client side signed it off, and where. Required when source is minutes.',
        },
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
          // A developer's connector files a developer's gap unless told otherwise.
          source: args.source ?? 'developer',
          source_ref: args.sourceRef ?? '',
          approver: args.approver ?? '',
          triage: args.triage ?? '',
          when: args.when ?? '',
          artefacts: Array.isArray(args.artefacts) ? args.artefacts.map(String) : [],
          contract_impact: args.contractImpact ?? '',
          effort_points: typeof args.effortPoints === 'number' ? args.effortPoints : null,
          client_signoff: args.clientSignoff ?? '',
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
      + '(CR-007). If the ticket is blocked by it, propose the ticket On hold with the id in the comment '
      + '(applied only after a yes), never work around it, and then find the next ticket you can finish '
      + '(adam_board with only: "workable"). Draft codes work once and for 30 minutes.',
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
          ? `Filed as ${change.id}. Propose #${change.ticket} On hold with "Blocked by ${change.id}" as the comment `
            + '(adam_propose; apply only after the person says yes). Do not build the blocked part and do not work '
            + 'around it. Then find the next ticket you can finish: adam_board with only: "workable", and propose '
            + 'the first one it lists.'
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
