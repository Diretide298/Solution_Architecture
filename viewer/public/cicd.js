/**
 * CI/CD — how the package gets from a commit to a running venue.
 *
 * Three views. **Pipeline** reads `repos/`, `services/` and `deploy/` and says
 * what a change has to pass, what it becomes and where it lands — and where two
 * of those three disagree. **Flash sale** and **Shared cell** are the two
 * deployments the package simulates rather than merely configures; they were
 * `burst.html` and a standalone handoff page, and they are tabs now for the
 * reason UI/UX became tabs.
 *
 * Nothing here is transcribed. The pipeline payload is built in
 * `lib/cicd.mjs`, the flash sale is `burst.js` drawing the same JSON it always
 * drew, and the shared cell is the package's own page framed.
 */

import * as auth from '/validation.js';
import { renderBurst } from '/burst.js';

const CELL = '/handoff/Shared Cell.dc.html';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const fmt = (n) => (typeof n === 'number' ? n.toLocaleString('en-GB') : String(n ?? ''));

/**
 * `**bold**` and `` `code` `` rendered as elements, everything else as text.
 *
 * Never as HTML. The findings are built from file contents — a workflow step
 * name, a `CMD` line — and a viewer that hands package content to `innerHTML`
 * is a viewer that renders whatever a package happens to contain.
 */
function rich(raw) {
  const frag = document.createDocumentFragment();
  for (const part of String(raw ?? '').split(/(\*\*[^*]+\*\*|`[^`]+`)/g)) {
    if (!part) continue;
    if (part.startsWith('**')) frag.append(el('strong', null, part.slice(2, -2)));
    else if (part.startsWith('`')) frag.append(el('code', null, part.slice(1, -1)));
    else frag.append(document.createTextNode(part));
  }
  return frag;
}

/* ── the framed handoff pages ─────────────────────────────────────────── */

/**
 * One of the package's own standalone pages, inside a view.
 *
 * `?embed=1` asks the server to hide the page's own header and to have it
 * report its height — an iframe does not size to its content, and on the
 * deployed host this is a different origin, so nothing here can measure it.
 * Same treatment the flash-sale simulator gets; see the handoff route in
 * server.mjs.
 */
async function frameHandoff(host, file, { title, missing }) {
  // Before the URL is built, not after. `apiUrl` puts the project on a path and
  // is synchronous, so calling it before the registry has answered addresses
  // `/pkg/handoff/...` — a package path with no package in it, which 404s and
  // reads exactly like a drop that was never applied.
  await auth.ensureProject();
  const src = auth.apiUrl(`${file}?embed=1`);
  const ok = await fetch(src, { method: 'HEAD', credentials: 'include' })
    .then((res) => res.ok).catch(() => false);
  if (!ok) {
    const box = el('div', 'ci-col');
    box.append(el('p', 'ci-empty', missing));
    host.append(box);
    return false;
  }

  const frame = document.createElement('iframe');
  frame.className = 'ci-frame';
  frame.src = src;
  frame.title = title;
  // The package's own file on the package's own origin, and it needs scripts to
  // be anything at all. No navigation: a link inside it would otherwise replace
  // the viewer with a page that has no way back.
  frame.setAttribute('sandbox', 'allow-scripts allow-same-origin');
  frame.style.height = '900px';
  host.append(frame);

  const foot = el('p', 'ci-frame-foot');
  const open = el('a', null, 'Open it on its own');
  open.href = auth.apiUrl(file);
  open.target = '_blank';
  open.rel = 'noopener';
  foot.append(open);
  foot.append(document.createTextNode(` · ${file.replace(/^\//, '')}`));
  host.append(foot);

  window.addEventListener('message', (ev) => {
    if (ev.source !== frame.contentWindow) return;
    const h = Number(ev.data?.type === 'adam-handoff-height' && ev.data.height);
    if (h > 200) frame.style.height = `${Math.ceil(h)}px`;
  });
  return true;
}

/* ── the pipeline ─────────────────────────────────────────────────────── */

function renderTotals(host, data) {
  const s = data.stats;
  const strip = el('div', 'ci-totals');
  const tile = (value, of, key, note) => {
    const box = el('div', 'ci-total');
    const v = el('div', 'ci-total-v', fmt(value));
    if (of != null) v.append(el('span', 'of', ` of ${fmt(of)}`));
    box.append(v);
    box.append(el('div', 'ci-total-k', key));
    box.append(el('div', 'ci-total-n', note));
    return box;
  };
  strip.append(tile(s.workflows, null, 'workflows',
    `across ${s.repos} repositories · ${s.jobs} jobs, ${s.steps} steps`));
  strip.append(tile(s.gates, null, 'steps that fail a build',
    'the rest report; a gate is the ones that stop'));
  strip.append(tile(s.recipes, s.images, 'image recipes',
    s.recipes === 1 && s.images > 1
      ? `all ${s.images} Dockerfiles are the same file`
      : 'distinct Dockerfiles across the services'));
  strip.append(tile(s.configs, null, 'deployment configurations',
    'four scenarios and the variants that change one thing each'));
  host.append(strip);
}

/**
 * The path itself, drawn as the stages a change passes through — and it is
 * drawn as much for the stages that do not exist as for the ones that do.
 *
 * A pipeline diagram that only shows what is configured is a diagram that
 * argues everything after the last configured step is somebody else's problem.
 */
function renderPath(host, data) {
  const steps = data.workflows.flatMap((w) => w.jobs.flatMap((j) => j.steps));

  /**
   * **A step whose whole command is `echo` does not do the thing it is named
   * after.** `contracts.yml` has three of them — Publish npm, Publish NuGet,
   * Publish PyPI — each printing the command it would have run. Counting those
   * as a publish stage is the single most misleading thing this view could do,
   * because it is exactly the stage a reader would otherwise assume works.
   */
  const real = steps.filter((s) => !s.run || !/^echo\b/.test(s.run.trim()));
  const did = (re) => real.some((s) => re.test(`${s.uses ?? ''} ${s.run ?? ''}`));
  const stubbedFor = (re) => steps.filter(
    (s) => s.run && /^echo\b/.test(s.run.trim()) && re.test(s.run),
  ).length;

  const onPr = data.workflows.filter((w) => w.triggers.includes('pull_request')).length;
  const BUILDS = /docker\s+build|build-push|buildx|kaniko/i;
  const PUBLISHES = /nuget\s+push|npm\s+publish|twine\s+upload|docker\s+push/i;
  const DEPLOYS = /kubectl|helm|terraform\s+apply|docker\s+compose\s+up|ansible/i;
  const stubbed = stubbedFor(PUBLISHES);

  const STAGES = [
    { key: 'commit', name: 'Commit', have: true,
      note: `${onPr} of ${data.workflows.length} workflows run on a pull request` },
    { key: 'gate', name: 'Gates', have: data.stats.gates > 0,
      note: data.stats.gates
        ? `${data.stats.gates} steps whose own comment says they fail the build — architecture `
          + 'tests, an eval baseline, a breaking-change diff'
        : 'nothing here fails a build' },
    { key: 'image', name: 'Image', have: did(BUILDS),
      note: did(BUILDS)
        ? `${data.stats.images} Dockerfiles, built in CI`
        : `${data.stats.images} Dockerfiles, and no step builds one` },
    { key: 'registry', name: 'Publish', have: did(PUBLISHES),
      note: did(PUBLISHES)
        ? 'clients and images pushed on a tag'
        : stubbed
          ? `${stubbed} publish steps, and every one of them is an \`echo\` printing the command `
            + 'it would have run'
          : 'nothing is published anywhere' },
    { key: 'deploy', name: 'Deploy', have: did(DEPLOYS),
      note: did(DEPLOYS)
        ? 'applied from a pipeline'
        : `${data.stats.configs} configurations, and nothing applies one` },
    { key: 'run', name: 'Run', have: true,
      note: 'the two views beside this one — the only place the package shows a deployment '
        + 'running rather than configured' },
  ];

  const sec = el('section', 'ci-sec');
  sec.append(el('p', 'ci-h2', 'The path'));
  sec.append(el('h2', 'ci-h3', 'Commit to running venue'));
  const lead = el('p', 'ci-lead');
  lead.append(rich(
    `**${STAGES.filter((s) => !s.have).length} of the ${STAGES.length} stages do not exist.** `
    + 'The ones that do are thorough — a real postgres and a real redis stood up per job, '
    + 'architecture tests as a build gate, a breaking-change gate on the contracts. The path '
    + 'then stops, and everything from an image to a running environment is a person at a '
    + 'terminal.',
  ));
  sec.append(lead);

  const track = el('div', 'ci-path');
  STAGES.forEach((stage, i) => {
    if (i) track.append(el('div', `ci-path-link${stage.have ? '' : ' is-missing'}`));
    const box = el('div', `ci-stage${stage.have ? '' : ' is-missing'}`);
    box.append(el('div', 'ci-stage-name', stage.name));
    box.append(el('div', 'ci-stage-state', stage.have ? 'in the package' : 'nothing does this'));
    box.append(el('p', 'ci-stage-note', rich(stage.note)));
    track.append(box);
  });
  sec.append(track);
  host.append(sec);
}

function renderFindings(host, data) {
  if (!data.findings.length) return;
  const rank = { error: 0, warn: 1 };
  const findings = [...data.findings].sort(
    (a, b) => (rank[a.severity] ?? 9) - (rank[b.severity] ?? 9),
  );

  const sec = el('section', 'ci-sec');
  sec.append(el('p', 'ci-h2', 'What the three folders disagree about'));
  sec.append(el('h2', 'ci-h3', `${findings.length} findings`));
  const lead = el('p', 'ci-lead');
  lead.append(rich(
    '**Every one of these is two files, each fine on its own.** None of them is stated '
    + 'anywhere in the package — a workflow does not know what a Dockerfile says and neither '
    + 'knows what is in `deploy/`. They are comparisons, made here, and each names the files '
    + 'it was read from so it can be checked rather than believed.',
  ));
  sec.append(lead);

  const list = el('div', 'ci-findings');
  for (const finding of findings) {
    const card = el('div', `ci-finding is-${finding.severity}`);
    const head = el('div', 'ci-finding-head');
    head.append(el('span', `ci-sev is-${finding.severity}`, finding.severity));
    head.append(el('span', 'ci-finding-title', finding.title));
    card.append(head);
    card.append(el('p', 'ci-finding-detail', rich(finding.detail)));
    const where = el('div', 'ci-where');
    for (const file of finding.where ?? []) where.append(el('span', 'ci-file', file));
    card.append(where);
    list.append(card);
  }
  sec.append(list);
  host.append(sec);
}

function renderRepos(host, data) {
  const sec = el('section', 'ci-sec');
  sec.append(el('p', 'ci-h2', 'Section one'));
  sec.append(el('h2', 'ci-h3', 'The repositories, and what each merge has to pass'));
  const lead = el('p', 'ci-lead');
  lead.append(rich(
    `**${data.stats.repos} repositories, ${data.stats.workflows} workflows.** The language is `
    + 'read off the files at the root — a solution file is a .NET repository whatever its '
    + 'pipeline runs — and the toolchain off the steps. Where the two differ, the finding above '
    + 'says so.',
  ));
  sec.append(lead);

  const grid = el('div', 'ci-repos');
  for (const repo of data.repos) {
    const mine = data.workflows.filter((w) => w.repo === repo.name);
    const card = el('div', 'ci-repo');

    const head = el('div', 'ci-repo-head');
    head.append(el('span', 'ci-repo-name', repo.name));
    for (const lang of repo.languages) head.append(el('span', 'ci-lang', lang));
    card.append(head);

    const facts = el('div', 'ci-repo-facts');
    facts.append(el('span', null, `${mine.length} workflow${mine.length === 1 ? '' : 's'}`));
    facts.append(el('span', null, `${repo.gates} gate${repo.gates === 1 ? '' : 's'}`));
    if (repo.holds.length) facts.append(el('span', null, `holds ${repo.holds.join(', ')}`));
    card.append(facts);

    for (const wf of mine) {
      const box = el('div', `ci-wf${/bible/i.test(wf.name) ? ' is-doc' : ''}`);
      const wh = el('div', 'ci-wf-head');
      wh.append(el('span', 'ci-wf-name', wf.name));
      wh.append(el('span', 'ci-wf-on', wf.triggers.join(' · ') || 'no trigger'));
      box.append(wh);

      for (const job of wf.jobs) {
        const jb = el('div', 'ci-job');
        const jh = el('div', 'ci-job-head');
        jh.append(el('span', 'ci-job-name', job.name));
        if (job.needs.length) jh.append(el('span', 'ci-job-needs', `needs ${job.needs.join(', ')}`));
        if (job.onlyIf) jh.append(el('span', 'ci-job-if', job.onlyIf));
        jb.append(jh);

        // The containers a job stands up. A test against a real postgres and a
        // real redis is a different claim from a test against a mock, and it is
        // the only place in the package that makes it.
        if (job.services.length) {
          const svc = el('div', 'ci-job-svc');
          for (const s of job.services) {
            svc.append(el('span', 'ci-chip', `${s.name} · ${s.image ?? '?'}`));
          }
          jb.append(svc);
        }

        const steps = el('ol', 'ci-steps');
        for (const step of job.steps) {
          const li = el('li', 'ci-step');
          const label = step.name ?? step.uses ?? step.run?.split('\n')[0] ?? '';
          li.append(el('span', 'ci-step-label', label));
          if (step.uses && step.name) li.append(el('span', 'ci-step-uses', step.uses));
          if (step.run && step.name) {
            li.append(el('code', 'ci-step-run', step.run.split('\n')[0]));
          }
          // The comment above the step. In these files it is where the argument
          // is — "Architecture tests are a build gate, not a suggestion" — and a
          // gate without its argument is a step somebody will delete.
          if (step.note) li.append(el('p', 'ci-step-note', step.note));
          steps.append(li);
        }
        jb.append(steps);
        box.append(jb);
      }
      card.append(box);
    }
    grid.append(card);
  }
  sec.append(grid);
  host.append(sec);
}

function renderImages(host, data) {
  if (!data.recipes.length) return;
  const sec = el('section', 'ci-sec');
  sec.append(el('p', 'ci-h2', 'Section two'));
  sec.append(el('h2', 'ci-h3', 'What a service becomes'));
  const lead = el('p', 'ci-lead');
  lead.append(rich(
    data.stats.recipes === 1
      ? `**${data.stats.images} Dockerfiles and one recipe.** They are byte-identical, so this is `
        + 'one decision shown once rather than sixteen files shown sixteen times — and that they '
        + 'are identical is itself the finding: nothing distinguishes the service that carries '
        + 'the sale from the one that posts to the ledger.'
      : `**${data.stats.recipes} distinct recipes across ${data.stats.images} services.**`,
  ));
  sec.append(lead);

  for (const recipe of data.recipes) {
    const card = el('div', 'ci-recipe');
    const head = el('div', 'ci-recipe-head');
    head.append(el('span', 'ci-recipe-from', recipe.from ?? 'no FROM'));
    head.append(el('span', 'ci-lang', recipe.runtime ?? 'unknown runtime'));
    head.append(el('span', 'ci-recipe-n',
      `${recipe.services.length} service${recipe.services.length === 1 ? '' : 's'}`));
    card.append(head);
    if (recipe.cmd) {
      const cmd = el('div', 'ci-recipe-cmd');
      cmd.append(el('span', 'ci-recipe-cmd-k', 'CMD'));
      cmd.append(el('code', null, recipe.cmd));
      card.append(cmd);
    }
    const list = el('div', 'ci-recipe-svcs');
    for (const service of recipe.services) {
      list.append(el('span', 'ci-chip', service.replace(/Service$/, '')));
    }
    card.append(list);
    sec.append(card);
  }
  host.append(sec);
}

function renderConfigs(host, data) {
  if (!data.configs.length) return;
  const scenarios = data.configs.filter((c) => c.kind === 'scenario');
  const variants = data.configs.filter((c) => c.kind === 'variant');

  const sec = el('section', 'ci-sec');
  sec.append(el('p', 'ci-h2', 'Section three'));
  sec.append(el('h2', 'ci-h3', 'Where it runs'));
  const lead = el('p', 'ci-lead');
  lead.append(rich(
    `**${scenarios.length} scenarios and ${variants.length} variants.** A variant changes exactly `
    + 'one thing against the scenario it forks, which is what makes the two comparable — anything '
    + 'else differing invalidates the comparison. Nothing in the package applies any of them.',
  ));
  sec.append(lead);

  // What the DDL builds, said once above the cards. Every configuration below
  // provisions a database; this is the one thing that goes inside all of them,
  // and the count of what isolates one tenant from another is the number the
  // cards cannot show.
  if (data.storage?.tables) {
    const st = data.storage;
    const line = el('p', 'ci-lead');
    line.append(rich(
      `Inside every one of them, the same DDL: **${st.schemas} schemas** and `
      + `**${st.tables} tables** from \`backend/\`, with ${st.createsDatabase} \`CREATE `
      + `DATABASE\`, ${st.partitions} \`PARTITION BY\` and ${st.policies} row-level security `
      + 'policies. Those last three are the ones that would separate one tenant from another, '
      + 'and each of them is a grep rather than a reading.',
    ));
    sec.append(line);
  }

  const grid = el('div', 'ci-configs');
  for (const config of [...scenarios, ...variants]) {
    const card = el('div', `ci-config is-${config.kind}`);
    const head = el('div', 'ci-config-head');
    head.append(el('span', 'ci-config-name', config.name));
    head.append(el('span', 'ci-chip', config.kind));
    card.append(head);
    const facts = el('div', 'ci-config-facts');
    facts.append(el('span', null, `${config.services} services`));
    if (config.replicas) facts.append(el('span', null, `${config.replicas} replicas`));
    if (config.db?.maxConnections) {
      facts.append(el('span', null, `max_connections ${config.db.maxConnections}`));
    }
    if (config.db?.pooler?.maxClient) {
      facts.append(el('span', null,
        `pool ${config.db.pooler.maxClient} → ${config.db.pooler.poolSize}`));
    }
    card.append(facts);

    // **What this configuration thinks a database is.** It is the question the
    // package answers differently in different files, and it was legible in
    // none of them: a compose file states it three times — the server's
    // POSTGRES_DB, the databases created beside it, and the database at the end
    // of every DSN — and only the last of those decides anything.
    if (config.db && config.db.model !== 'no database in this config') {
      const db = el('div', 'ci-config-db');
      db.append(el('span', 'ci-config-db-k', 'database'));
      db.append(el('span', 'ci-config-db-v', config.db.model));
      if (config.db.reached.length) {
        const list = el('div', 'ci-config-db-list');
        for (const name of config.db.reached) list.append(el('span', 'ci-chip', name));
        db.append(list);
      }
      card.append(db);
    }
    // The header carries the package's own `**bold**`, and rendering it as text
    // put the asterisks on the page.
    if (config.header) card.append(el('p', 'ci-config-note', rich(config.header)));
    card.append(el('div', 'ci-where', el('span', 'ci-file', config.file)));
    grid.append(card);
  }
  sec.append(grid);
  host.append(sec);
}

async function renderPipeline(host) {
  const col = el('div', 'ci-col');
  host.append(col);

  const hero = el('section', 'ci-hero');
  hero.append(el('p', 'ci-eyebrow', 'Delivery · commit to venue'));
  hero.append(el('h1', 'ci-title', 'How this is built, shipped and run'));
  const sub = el('p', 'ci-sub');
  sub.append(rich(
    'Three folders that nothing else in the package joins. `repos/` says what a pull request '
    + 'has to pass, `services/` says what each service becomes, and `deploy/` says what runs '
    + 'where. Each is readable on its own; the disagreements between them were readable '
    + 'nowhere.',
  ));
  hero.append(sub);
  const src = el('p', 'ci-source');
  src.append(rich(
    'Read live from **repos/** · **services/** · **deploy/** — nothing here is transcribed, and '
    + 'no finding is stated by the package',
  ));
  hero.append(src);
  col.append(hero);

  let data = null;
  try {
    const res = await auth.apiFetch('/api/cicd');
    if (!res.ok) throw new Error(`/api/cicd answered ${res.status}`);
    data = await res.json();
  } catch (err) {
    col.append(el('div', 'ci-error', `Could not read the delivery payload: ${err.message}`));
    return;
  }
  if (!data) {
    col.append(el('div', 'ci-error', 'The delivery payload is empty for this package.'));
    return;
  }

  renderTotals(col, data);
  renderPath(col, data);
  renderFindings(col, data);
  renderRepos(col, data);
  renderImages(col, data);
  renderConfigs(col, data);
}

/* ── the three views ──────────────────────────────────────────────────── */

const drawn = new Map();

/**
 * Draw one of the three, once.
 *
 * Per view rather than per module: opening Pipeline should not build the flash
 * sale, which stands up a whole simulator in an iframe. `app.js` calls this
 * every time a tab is shown and this decides whether there is anything to do.
 */
export function show(mode) {
  if (drawn.has(mode)) return drawn.get(mode);
  const host = $(`view-${mode}`);
  if (!host) return Promise.resolve();

  const work = mode === 'cicd-pipeline'
    ? renderPipeline(host)
    : mode === 'cicd-burst'
      ? renderBurst(host, { hero: true })
      : frameHandoff(host, CELL, {
        title: 'Shared cell',
        missing: 'This package does not ship handoff/Shared Cell.dc.html. It arrives with the '
          + 'burst simulator drop; a package without it has not had that drop applied.',
      });

  drawn.set(mode, work.catch((err) => {
    host.append(el('div', 'ci-error', `Could not draw this view: ${err.message}`));
  }));
  return drawn.get(mode);
}
