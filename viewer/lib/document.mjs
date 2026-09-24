/**
 * The delivery package as one document somebody can read end to end.
 *
 * **Built from the same payloads the viewer draws**, not from the files again.
 * A second reader of the contracts is a second answer to every question the
 * first one answers, and the two drift the first time a field is renamed — so
 * this takes `pkg.index`, `pkg.journeys`, `pkg.backend` and the rest exactly as
 * the layer routes serve them. If a screen is missing here it is missing on the
 * screens tab too, which is the right failure: one bug, not two.
 *
 * **Markdown, because the destination is somebody else's tooling.** It pastes
 * into Confluence, opens in Word, renders on GitHub, prints from a browser and
 * survives being mailed. A PDF would be none of those and would need a
 * rendering dependency this server does not have.
 *
 * **It never invents prose.** Every sentence is a heading, a count, or text
 * that was already written in the package. A generator that padded the gaps
 * with "This service is responsible for…" would produce something that reads as
 * documentation and is not, and the first person to notice would be a client
 * who had already relied on it. Where the package says nothing, this says
 * nothing — and the counts of what is undescribed are in the document, because
 * that absence is itself a fact about the delivery.
 *
 * Every field below was read off the real payloads rather than assumed. The
 * first draft of this file guessed, and guessed wrong in four places at once:
 * `backend.columns` is an object keyed by table and not a list, `module.tables`
 * is a count and not an array, index nodes carry `type` and not `kind`, and a
 * service's prose is under `why`. It threw on the first request.
 *
 * What a client may read is decided by the caller — the audience rules live in
 * `audience.mjs` and this file is handed the list of sections it may build, so
 * there is one place that decides and it is not this one.
 */

/** Sections, in the order they are written. Each names the payload it needs, so
 *  a layer that has not been built yet is skipped rather than drawn empty. */
export const SECTIONS = [
  { id: 'overview', title: 'Overview', needs: null },
  { id: 'frontend', title: 'Screens and journeys', needs: 'journeys' },
  { id: 'contracts', title: 'Contracts and operations', needs: 'index' },
  { id: 'domain', title: 'State models and events', needs: 'domain' },
  { id: 'backend', title: 'Data model', needs: 'backend' },
  { id: 'services', title: 'Services', needs: 'diagrams' },
  { id: 'decisions', title: 'Decisions', needs: 'decisions' },
];

const esc = (s) => String(s ?? '').replace(/\r/g, '');

/** A table cell. Pipes and newlines are the two characters that break a
 *  Markdown table, and package prose is full of both — `storageReason` runs to
 *  25,000 characters of markdown in places. */
function cell(value) {
  if (value == null || value === '') return '—';
  return esc(value).replace(/\|/g, '\\|').replace(/\s*\n+\s*/g, ' ').trim() || '—';
}

function table(headers, rows) {
  if (!rows.length) return '';
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map((r) => `| ${r.map(cell).join(' | ')} |`),
  ].join('\n');
}

/** Prose from the package, trimmed for a listing and never rewritten: if the
 *  description is one word, one word is what it says. */
function brief(text, at = 300) {
  const s = esc(text).replace(/\s*\n+\s*/g, ' ').trim();
  if (!s) return '';
  if (s.length <= at) return s;
  const cut = s.lastIndexOf('. ', at);
  return `${s.slice(0, cut > at * 0.5 ? cut + 1 : at).trimEnd()}…`;
}

const count = (n) => (typeof n === 'number' ? n.toLocaleString() : '—');

// ── the sections ─────────────────────────────────────────────────────

function overview(pkg, meta) {
  const ix = pkg.index?.stats ?? {};
  const rows = [
    ['Contracts', ix.files],
    ['Operations', ix.operations],
    ['Schemas', ix.schemas],
    ['Permissions', ix.permissions],
    ['Screens', pkg.journeys?.screens?.length],
    ['Journeys', pkg.journeys?.flows?.length],
    ['Platforms', pkg.journeys?.platforms?.length],
    ['Modules', pkg.backend?.modules?.length],
    ['Tables', pkg.backend?.tables?.length],
    ['State models', pkg.domain?.machines?.length],
    ['Events', pkg.domain?.events?.length],
    ['Services', pkg.diagrams?.services?.length],
    ['Decisions', pkg.decisions?.adrs?.length],
  ].filter(([, n]) => typeof n === 'number');

  return [
    `# ${esc(meta.name ?? meta.id)}`,
    '',
    `Generated from the delivery package by ADAM on ${meta.on}.`,
    '',
    // Said at the top, because a generated document that does not announce
    // itself gets edited by hand and then regenerated over.
    '> **This document is generated.** Every figure and every line of prose in '
    + 'it comes from the delivery package; nothing here was written for the '
    + 'document. Editing it by hand will be lost the next time it is generated '
    + '— change the package instead.',
    '',
    '## What is in the package',
    '',
    // Named rather than left blank. An unheaded column renders, and a
    // document with a nameless column in its first table sets the tone.
    table(['What', 'How many'], rows.map(([label, n]) => [label, count(n)])),
  ].join('\n');
}

function frontend(pkg) {
  const screens = pkg.journeys?.screens ?? [];
  const flows = pkg.journeys?.flows ?? [];
  const platforms = pkg.journeys?.platforms ?? [];
  const out = ['## Screens and journeys', ''];

  if (platforms.length) {
    out.push(`### Platforms (${platforms.length})`, '');
    out.push(table(['Code', 'Name', 'Surface', 'Runtime', 'Works offline', 'Screens'],
      platforms.map((p) => [p.code, p.shortName || p.name, p.surface, p.runtime,
        p.offlineCapable ? 'yes' : 'no',
        count(screens.filter((s) => s.platform === p.code).length)])), '');
  }

  if (flows.length) {
    out.push(`### Journeys (${flows.length})`, '');
    out.push(table(['Id', 'Journey', 'Actor', 'Wave', 'How critical', 'Steps'],
      flows.map((f) => [f.id, f.name, f.actor, f.wave, f.criticality,
        count((f.steps ?? []).length)])), '');
  }

  if (screens.length) {
    // By platform, because 2,427 screens in one table is a table nobody opens
    // twice — and the platform is how anybody actually looks for one.
    out.push(`### Screens (${screens.length})`, '');
    const byPlatform = new Map();
    for (const s of screens) {
      const key = s.platformName || s.platform || 'No platform';
      if (!byPlatform.has(key)) byPlatform.set(key, []);
      byPlatform.get(key).push(s);
    }
    for (const [name, mine] of [...byPlatform.entries()].sort((a, b) => b[1].length - a[1].length)) {
      out.push(`#### ${esc(name)} (${mine.length})`, '');
      out.push(table(['Id', 'Screen', 'Module', 'Wave', 'What it is for'],
        mine.map((s) => [s.id, s.name, s.module, s.wave, brief(s.purpose, 160)])), '');
    }
  }
  return out.join('\n');
}

function contracts(pkg) {
  const nodes = pkg.index?.nodes ?? [];
  const files = nodes.filter((n) => n.type === 'file');
  const operations = nodes.filter((n) => n.type === 'operation');
  const out = ['## Contracts and operations', '',
    `${files.length} contracts carrying ${operations.length} operations.`, ''];

  for (const file of [...files].sort((a, b) => String(a.name).localeCompare(String(b.name)))) {
    out.push(`### ${esc(file.title || file.name)}`, '');
    out.push(`\`${esc(file.file)}\`${file.tier ? ` · ${esc(file.tier)}` : ''}`, '');
    if (file.description) out.push(brief(file.description, 700), '');
    const mine = operations.filter((op) => op.file === file.file);
    if (mine.length) {
      out.push(table(['Operation', 'Method', 'Path', 'Permission', 'Offline', 'What it does'],
        mine.map((op) => [op.name, (op.method || '').toUpperCase(), op.path, op.permission,
          op.offlineCapable ? 'yes' : '', brief(op.title || op.description, 140)])), '');
    }
  }
  return out.join('\n');
}

function domain(pkg) {
  const machines = pkg.domain?.machines ?? [];
  const events = pkg.domain?.events ?? [];
  const out = ['## State models and events', '',
    `${machines.length} state models and ${events.length} events.`, ''];

  if (machines.length) {
    out.push(`### State models (${machines.length})`, '');
    out.push(table(['Entity', 'Owner', 'Starts at', 'Ends at', 'States', 'Transitions'],
      machines.map((m) => [m.entity || m.id, m.owner,
        m.initial, (m.terminal ?? []).join(', '),
        count((m.states ?? []).length), count((m.transitions ?? []).length)])), '');

    // Every move, per model. This is the part somebody building against the
    // package actually needs and cannot get from a diagram in an email.
    for (const m of machines) {
      const moves = m.transitions ?? [];
      if (!moves.length) continue;
      out.push(`#### ${esc(m.entity || m.id)}`, '');
      out.push(table(['From', 'To', 'By', 'Only when', 'Needs approval', 'Emits'],
        moves.map((t) => [t.from, t.to, t.operation || t.trigger, brief(t.guard, 120),
          t.requiresApproval ? 'yes' : '', (t.emits ?? []).join(', ')])), '');
    }
  }

  if (events.length) {
    out.push(`### Events (${events.length})`, '');
    out.push(table(['Event', 'Published by', 'When', 'Consumed by'],
      // `context` is the field. `name` is not one, so this printed a row of
      // bare commas -- six consumers, none of them named.
      events.map((e) => [e.name || e.id, e.publisher, brief(e.emittedWhen, 140),
        (e.consumers ?? []).map((c) => (typeof c === 'string' ? c
          : c.context ?? c.name ?? c.service ?? '')).filter(Boolean).join(', ')])), '');
  }
  return out.join('\n');
}

function backend(pkg) {
  const modules = pkg.backend?.modules ?? [];
  const tables = pkg.backend?.tables ?? [];
  // An object keyed by table name, not a list. Guessing otherwise is what
  // threw `columns is not iterable` on the first request this file ever saw.
  const columns = pkg.backend?.columns ?? {};
  const out = ['## Data model', '',
    `${tables.length} tables in ${modules.length} modules.`, ''];

  // Counted rather than glossed over. A table with no description is a real
  // fact about the package, and a document that hid it would be the wrong kind
  // of tidy.
  const undescribed = tables.filter((t) => t.storageOnly).length;
  if (undescribed) {
    out.push(`${undescribed} of them are storage-only — the package records what they hold `
      + 'and not why they exist.', '');
  }

  for (const module of [...modules].sort((a, b) => String(a.name).localeCompare(String(b.name)))) {
    const mine = tables.filter((t) => t.module === module.name);
    out.push(`### ${esc(module.name)} (${mine.length} tables)`, '');
    if (module.what) out.push(brief(module.what, 500), '');
    if (module.why) out.push(`**Why it exists.** ${brief(module.why, 500)}`, '');

    for (const t of mine) {
      out.push(`#### \`${esc(t.name)}\``, '');
      if (t.storageReason && !t.storageOnly) out.push(brief(t.storageReason, 400), '');
      const cols = columns[t.name] ?? [];
      if (cols.length) {
        out.push(table(['Column', 'Type', 'Required', 'From', 'Notes'],
          cols.map((c) => [c.name, c.type, c.required ? 'yes' : '', c.source,
            brief(c.description, 120)])), '');
      }
    }
  }
  return out.join('\n');
}

function services(pkg) {
  const list = pkg.diagrams?.services ?? [];
  const tiers = pkg.diagrams?.tiers ?? [];
  const out = ['## Services', '', `${list.length} services.`, ''];

  if (tiers.length) {
    out.push(table(['Tier', 'What it means', 'Services'],
      tiers.map((t) => [t.tier, brief(t.meaning, 200), (t.services ?? []).length])), '');
  }

  out.push(table(['Service', 'Tier', 'Operations', 'Tables'],
    list.map((s) => [s.name, s.tier, count(s.operations), count(s.tables)])), '');

  for (const s of list) {
    out.push(`### ${esc(s.name)}`, '');
    if (s.why) out.push(brief(s.why, 600), '');
    if (s.ifDown) out.push(`**If it is down.** ${brief(s.ifDown, 300)}`, '');
    if ((s.schemas ?? []).length) {
      out.push(`Owns: ${s.schemas.map((x) => `\`${esc(x)}\``).join(', ')}`, '');
    }
  }
  return out.join('\n');
}

function decisions(pkg) {
  const adrs = pkg.decisions?.adrs ?? [];
  const docs = pkg.decisions?.documents ?? [];
  const out = ['## Decisions', '', `${adrs.length} architecture decision records.`, ''];
  out.push(table(['Id', 'Title', 'Status', 'Verdict', 'Date', 'Superseded by'],
    [...adrs].sort((a, b) => Number(a.number) - Number(b.number))
      .map((a) => [a.id, a.title, a.status, a.verdict, a.date, a.supersededBy])), '');
  if (docs.length) {
    out.push(`### Registers and supporting documents (${docs.length})`, '');
    out.push(table(['Document', 'Group', 'Rows'],
      docs.map((d) => [d.title || d.id, d.group, count(d.rows)])), '');
  }
  return out.join('\n');
}

const BUILDERS = { overview, frontend, contracts, domain, backend, services, decisions };

/**
 * One document, as Markdown.
 *
 * `allowed` is the set of section ids the caller may have — worked out from the
 * audience rules by whoever calls this, never here. A section whose layer has
 * not been built is skipped rather than drawn, because an empty "Data model"
 * heading reads as a package with no tables.
 */
export function buildDocument(pkg, meta, wanted, allowed) {
  const parts = [];
  const included = [];
  const skipped = [];
  for (const section of SECTIONS) {
    if (!wanted.includes(section.id)) continue;
    if (allowed && !allowed.includes(section.id)) { skipped.push(section.id); continue; }
    if (section.needs && !pkg[section.needs]) { skipped.push(section.id); continue; }
    let text = '';
    try {
      text = BUILDERS[section.id](pkg, meta);
    } catch (error) {
      // One section that cannot be built must not take the document with it.
      // The reader gets the rest and is told which one failed, rather than a
      // 500 that names nothing.
      skipped.push(`${section.id} (${error.message})`);
      continue;
    }
    if (!text.trim()) { skipped.push(section.id); continue; }
    parts.push(text);
    included.push(section.id);
  }
  const markdown = parts.join('\n\n');
  return {
    markdown,
    sections: included,
    skipped,
    // Counted here so the page can say how big the thing it is about to
    // download is, without downloading it to find out.
    words: markdown.split(/\s+/).filter(Boolean).length,
  };
}
