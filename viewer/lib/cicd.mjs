/**
 * How the package is built, shipped and run.
 *
 * **The three artefacts that decide this were in three places nothing joined.**
 * `repos/<repo>/.github/workflows/` says what a pull request has to pass,
 * `services/<name>/Dockerfile` says what a service becomes, and `deploy/` says
 * what runs where — and each was readable on its own while the disagreements
 * between them were readable nowhere. The findings at the bottom of this file
 * are all of that kind: every one of them is two files, each fine alone.
 *
 * Derived, not stated. Nothing in the package declares a toolchain, an image
 * runtime or a gate; those are read off the steps and the `FROM` line, and a
 * finding is the comparison rather than a note somebody remembered to write.
 */

import { readdir, readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import yaml from 'js-yaml';

const sha = (text) => createHash('sha256').update(text).digest('hex').slice(0, 12);

/** Directory entries, or nothing at all — a package without `repos/` is a
 *  package that has not adopted the split yet, not a broken one. */
async function dirs(root, rel) {
  const entries = await readdir(path.join(root, rel), { withFileTypes: true }).catch(() => []);
  return entries.filter((e) => e.isDirectory()).map((e) => e.name);
}

/**
 * What a workflow is built out of, read off its steps.
 *
 * A workflow never says "this is a .NET repository". It says
 * `actions/setup-dotnet`, and that is the same statement made by somebody who
 * had to make it true.
 */
function toolchainOf(steps) {
  const text = steps.map((s) => `${s.uses ?? ''} ${s.run ?? ''}`).join('\n');
  const found = new Set();
  if (/setup-dotnet|dotnet\s+(restore|build|test|nuget)/.test(text)) found.add('dotnet');
  if (/setup-python|\bpip\s|\bpytest\b|\bruff\b|\bmypy\b|twine/.test(text)) found.add('python');
  if (/setup-node|pnpm|npm\s|\bnx\b/.test(text)) found.add('node');
  return [...found];
}

/** The steps of one job, flattened to what a reader needs: what it runs, and
 *  the comment somebody left above it — which in these files is where the
 *  reasoning is. */
function stepsOf(job, lines) {
  return (job.steps ?? []).map((step) => {
    const label = step.name ?? step.uses ?? String(step.run ?? '').split('\n')[0];
    // The comment block directly above the step in the file. These workflows
    // carry their argument in comments — "Architecture tests are a build gate,
    // not a suggestion" — and dropping it would leave the gate without it.
    const at = lines.findIndex((l) => label && l.includes(label.split('\n')[0].trim()));
    const note = [];
    for (let i = at - 1; i >= 0 && at > 0; i -= 1) {
      const body = lines[i].trim();
      if (body.startsWith('#')) note.unshift(body.replace(/^#\s?/, ''));
      else break;
    }
    return {
      name: step.name ?? null,
      uses: step.uses ?? null,
      run: step.run ? String(step.run).trim() : null,
      note: note.join(' ') || null,
    };
  });
}

/**
 * What a repository is, read off the files at its root rather than off its
 * pipeline. `Ticvai.sln` beside `global.json` is a .NET repository whatever the
 * workflow happens to run, and the disagreement between the two is the point.
 */
const MARKERS = [
  [/\.sln$|^global\.json$|^Directory\.Build\.props$/, 'dotnet'],
  [/^pyproject\.toml$|^setup\.cfg$|^requirements\.txt$/, 'python'],
  [/^package\.json$|^nx\.json$|^pnpm-workspace\.yaml$/, 'node'],
  [/^Makefile$/, 'make'],
];

async function readRepoLanguage(root, repo) {
  const names = await readdir(path.join(root, 'repos', repo)).catch(() => []);
  const found = new Set();
  for (const name of names) {
    for (const [re, lang] of MARKERS) if (re.test(name)) found.add(lang);
  }
  return {
    languages: [...found],
    // Infrastructure as code is a build artefact like any other, and the only
    // one here that nothing checks.
    holds: names.filter((n) => ['terraform', 'runbooks', 'openapi', 'src', 'apps'].includes(n)),
  };
}

async function readWorkflows(root, repo) {
  const rel = `repos/${repo}/.github/workflows`;
  const names = (await readdir(path.join(root, rel)).catch(() => []))
    .filter((f) => /\.ya?ml$/i.test(f));
  const out = [];
  for (const name of names) {
    const file = `${rel}/${name}`;
    const text = await readFile(path.join(root, file), 'utf8').catch(() => null);
    if (text == null) continue;
    let doc = null;
    try { doc = yaml.load(text); } catch { doc = null; }
    if (!doc || typeof doc !== 'object') continue;
    const lines = text.split(/\r?\n/);

    // `on` is a YAML 1.1 boolean, so js-yaml hands it back as the key `true`.
    // Every workflow in the package trips this and it is silent — the triggers
    // simply come out empty.
    const on = doc.on ?? doc[true] ?? null;
    const triggers = Array.isArray(on)
      ? on
      : (on && typeof on === 'object' ? Object.keys(on) : (on ? [String(on)] : []));

    const jobs = Object.entries(doc.jobs ?? {}).map(([key, job]) => {
      const steps = stepsOf(job ?? {}, lines);
      return {
        key,
        name: job?.name ?? key,
        runsOn: job?.['runs-on'] ?? null,
        needs: job?.needs ? [].concat(job.needs) : [],
        onlyIf: job?.if ? String(job.if) : null,
        // Containers a job stands up to test against — a real postgres and a
        // real redis, which is the difference between an integration test and
        // a mock.
        services: Object.entries(job?.services ?? {})
          .map(([k, v]) => ({ name: k, image: v?.image ?? null })),
        steps,
      };
    });

    const allSteps = jobs.flatMap((j) => j.steps);
    out.push({
      repo,
      file,
      name: doc.name ?? name.replace(/\.ya?ml$/i, ''),
      triggers,
      jobs,
      toolchain: toolchainOf(allSteps),
      stepCount: allSteps.length,
      // The whole point of a gate is that it fails the build. These are the
      // steps whose own comment says so, plus the ones named like one.
      gates: allSteps
        .filter((s) => /gate|architecture tests|breaking/i.test(`${s.name ?? ''} ${s.note ?? ''}`))
        .map((s) => ({ name: s.name ?? s.uses, note: s.note })),
    });
  }
  return out;
}

async function readImages(root) {
  const names = await dirs(root, 'services');
  const images = [];
  for (const service of names) {
    const file = `services/${service}/Dockerfile`;
    const text = await readFile(path.join(root, file), 'utf8').catch(() => null);
    if (text == null) continue;
    const from = (text.match(/^\s*FROM\s+(\S+)/mi) ?? [])[1] ?? null;
    images.push({
      service,
      file,
      from,
      hash: sha(text),
      text,
      // What the container actually becomes. `CMD` is the only line that says
      // it, and it is the line that has to agree with the build.
      cmd: (text.match(/^\s*CMD\s+(.+)$/mi) ?? [])[1]?.trim() ?? null,
      runtime: /python/i.test(from ?? '') ? 'python'
        : /(node|^oven\/bun)/i.test(from ?? '') ? 'node'
          : /dotnet|aspnet/i.test(from ?? '') ? 'dotnet' : null,
    });
  }

  // One entry per distinct recipe. Sixteen identical files are one decision
  // copied sixteen times, and counting them as sixteen hides that.
  const byHash = new Map();
  for (const image of images) {
    if (!byHash.has(image.hash)) {
      byHash.set(image.hash, {
        hash: image.hash, from: image.from, cmd: image.cmd,
        runtime: image.runtime, text: image.text, services: [],
      });
    }
    byHash.get(image.hash).services.push(image.service);
  }
  return { images: images.map(({ text, ...rest }) => rest), recipes: [...byHash.values()] };
}

async function readConfigs(root) {
  const out = [];
  for (const [dir, kind] of [['deploy', 'scenario'], ['deploy/variants', 'variant']]) {
    const names = (await readdir(path.join(root, dir)).catch(() => []))
      .filter((f) => /\.ya?ml$/i.test(f));
    for (const name of names) {
      const file = `${dir}/${name}`;
      const text = await readFile(path.join(root, file), 'utf8').catch(() => null);
      if (text == null) continue;
      let doc = null;
      try { doc = yaml.load(text); } catch { doc = null; }
      const services = Object.keys(doc?.services ?? {});
      // The header comment. Every one of these files opens with the argument
      // for the shape below it, and the first sentence of that is the only
      // description the file has.
      const header = text.split(/\r?\n/)
        .slice(0, 40)
        .filter((l) => l.trim().startsWith('#'))
        .map((l) => l.trim().replace(/^#\s?/, ''))
        .join(' ')
        .trim();
      out.push({
        file,
        kind,
        name: name.replace(/\.ya?ml$/i, ''),
        services: services.length,
        serviceNames: services,
        replicas: Object.values(doc?.services ?? {})
          .reduce((sum, s) => sum + (Number(s?.deploy?.replicas) || 0), 0),
        header: header.slice(0, 400),
      });
    }
  }
  return out;
}

/**
 * What two files say that cannot both be true, and what nothing says at all.
 *
 * Every finding names the files it is between. A finding a reader cannot check
 * is an assertion, and this viewer's whole argument is that an assertion in a
 * package is worth less than the two lines it was read from.
 */
function findFindings({ workflows, images, recipes, configs, repos }) {
  const out = [];

  if (recipes.length === 1 && images.length > 1) {
    out.push({
      severity: 'warn',
      kind: 'one-recipe',
      title: `${images.length} services, one image recipe`,
      detail: `Every \`services/*/Dockerfile\` is byte-identical — ${recipes[0].from} running `
        + `\`${recipes[0].cmd ?? 'no CMD'}\`. Nothing distinguishes the service that carries the `
        + 'sale from the one that posts to the ledger, and a change to the build is a change in '
        + `${images.length} places.`,
      where: images.slice(0, 3).map((i) => i.file),
    });
  }

  // The service repository and the service image, on the same services.
  //
  // A .NET solution and a Python image are each fine on their own. What they
  // cannot both be is the thing that gets deployed — and the disagreement is
  // read off two files that never mention each other.
  const imageRuntimes = new Set(recipes.map((r) => r.runtime).filter(Boolean));
  for (const repo of repos) {
    if (!repo.languages.includes('dotnet') && !repo.languages.includes('python')) continue;
    if (!repo.holds.includes('src') && !/backend|service/i.test(repo.name)) continue;
    const clash = repo.languages.filter((l) => ['dotnet', 'python', 'node'].includes(l))
      .filter((l) => imageRuntimes.size && !imageRuntimes.has(l));
    if (!clash.length || !recipes.length) continue;
    out.push({
      severity: 'error',
      kind: 'runtime-disagreement',
      title: `${repo.name} is ${clash.join(' and ')}; every service image is `
        + `${[...imageRuntimes].join(' and ')}`,
      detail: `The repository that holds the services builds ${clash.join(', ')} — its pipeline `
        + `runs ${repo.toolchain.join(', ') || 'nothing'} and its root carries a solution file. `
        + `All ${images.length} images are \`FROM ${recipes[0].from}\` running `
        + `\`${recipes[0].cmd ?? 'no CMD'}\`. Both cannot be the service that ships: either the `
        + 'images are left over from an earlier language or the pipeline builds something the '
        + 'deployment never runs.',
      where: [`repos/${repo.name}`, ...workflows.filter((w) => w.repo === repo.name && w.toolchain.length)
        .map((w) => w.file), recipes[0].services?.[0] && `services/${recipes[0].services[0]}/Dockerfile`]
        .filter(Boolean).slice(0, 4),
    });
  }

  // Infrastructure is a build artefact and this is the one nothing checks.
  for (const repo of repos) {
    if (!repo.holds.includes('terraform')) continue;
    const runs = workflows.filter((w) => w.repo === repo.name)
      .flatMap((w) => w.jobs.flatMap((j) => j.steps))
      .some((s) => /terraform|tflint|checkov|opa/i.test(`${s.uses ?? ''} ${s.run ?? ''}`));
    if (runs) continue;
    out.push({
      severity: 'warn',
      kind: 'unchecked-infra',
      title: `${repo.name} holds the terraform and nothing plans it`,
      detail: 'No workflow in the repository runs `terraform`, `tflint` or any policy check. '
        + 'The one repository whose artefacts decide whether an environment exists is the one '
        + 'merged without a plan.',
      where: [`repos/${repo.name}/terraform`,
        ...workflows.filter((w) => w.repo === repo.name).map((w) => w.file)],
    });
  }

  // Nothing builds an image, and nothing deploys one.
  const allText = workflows.flatMap((w) => w.jobs.flatMap((j) => j.steps))
    .map((s) => `${s.uses ?? ''} ${s.run ?? ''}`).join('\n');
  if (images.length && !/docker\s+build|docker\/build-push|buildx|kaniko/i.test(allText)) {
    out.push({
      severity: 'error',
      kind: 'no-image-build',
      title: 'No pipeline builds an image',
      detail: `${images.length} Dockerfiles, and no workflow step runs \`docker build\`. `
        + 'They are never exercised by CI, so the first time one is known to work is the first '
        + 'time somebody deploys it by hand.',
      where: workflows.map((w) => w.file).slice(0, 3),
    });
  }
  if (configs.length && !/docker\s+compose|kubectl|helm|terraform|\bdeploy\b/i.test(allText)) {
    out.push({
      severity: 'error',
      kind: 'no-cd',
      title: 'There is CI, and there is no CD',
      detail: `${configs.length} deployment configurations and no workflow that applies one. `
        + 'The D in CI/CD is not partly here — nothing in the package deploys anything, so every '
        + 'environment in `states/burst-environment.yaml`, including the one a flash sale stands '
        + 'up in minutes, is stood up by a person.',
      where: configs.slice(0, 3).map((c) => c.file),
    });
  }

  // A repository whose only workflow is the documentation gate.
  for (const repo of repos) {
    const mine = workflows.filter((w) => w.repo === repo.name);
    const real = mine.filter((w) => !/bible/i.test(w.name));
    if (mine.length && !real.length) {
      out.push({
        severity: 'warn',
        kind: 'no-gate',
        title: `${repo.name} has no gate but the documentation one`,
        detail: `Its only workflow is \`${mine[0].name}\`, which checks that a copy of the docs is `
          + 'present. Whatever this repository holds is merged unlinted, unbuilt and untested.',
        where: mine.map((w) => w.file),
      });
    }
  }

  return out;
}

/**
 * @param root  the package directory
 */
export async function buildCicd(root) {
  const repoNames = await dirs(root, 'repos');
  const workflows = (await Promise.all(repoNames.map((r) => readWorkflows(root, r)))).flat();
  const { images, recipes } = await readImages(root);
  const configs = await readConfigs(root);

  const repos = await Promise.all(repoNames.map(async (name) => {
    const mine = workflows.filter((w) => w.repo === name);
    const { languages, holds } = await readRepoLanguage(root, name);
    return {
      name,
      workflows: mine.length,
      toolchain: [...new Set(mine.flatMap((w) => w.toolchain))],
      languages,
      holds,
      gates: mine.reduce((sum, w) => sum + w.gates.length, 0),
    };
  }));

  const findings = findFindings({ workflows, images, recipes, configs, repos });

  return {
    repos,
    workflows,
    images,
    recipes,
    configs,
    findings,
    stats: {
      repos: repos.length,
      workflows: workflows.length,
      jobs: workflows.reduce((sum, w) => sum + w.jobs.length, 0),
      steps: workflows.reduce((sum, w) => sum + w.stepCount, 0),
      gates: workflows.reduce((sum, w) => sum + w.gates.length, 0),
      images: images.length,
      recipes: recipes.length,
      configs: configs.length,
      errors: findings.filter((f) => f.severity === 'error').length,
    },
  };
}
