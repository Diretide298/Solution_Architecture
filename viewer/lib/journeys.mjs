// Reads flows/ and screens/ and resolves the links between them.
//
// A flow is one job a person came to do, traced across screens. Each step names
// a screen and the operations it calls, so this joins three layers:
//   flow step -> screen -> operationId -> contract operation
//
// Nothing here is inferred. Every edge is declared in the YAML; the checks below
// only report where a declaration points at something that does not exist.

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';

async function readYamlDir(root, dir, filter) {
  const out = [];
  let entries;
  try {
    entries = await readdir(path.join(root, dir), { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    if (!entry.isFile() || !/\.ya?ml$/i.test(entry.name)) continue;
    if (filter && !filter(entry.name)) continue;
    const rel = `${dir}/${entry.name}`;
    try {
      const text = await readFile(path.join(root, rel), 'utf8');
      out.push({ rel, doc: yaml.load(text) });
    } catch (err) {
      out.push({ rel, error: err.message });
    }
  }
  return out;
}

/** Every screen across every platform file, keyed by screen id. */
function indexScreens(files, problems) {
  const screens = new Map();
  const platforms = [];

  for (const { rel, doc, error } of files) {
    if (error) {
      problems.push({ severity: 'error', kind: 'parse-error', file: rel, message: error });
      continue;
    }
    const platform = doc?.platform ?? {};
    const list = Array.isArray(doc?.screens) ? doc.screens : [];
    platforms.push({
      code: platform.code ?? rel,
      name: platform.name ?? rel,
      surface: platform.surface ?? null,
      runtime: platform.runtime ?? null,
      offlineCapable: Boolean(platform.offlineCapable),
      app: platform.app ?? null,
      appStatus: platform.appStatus ?? null,
      packages: Array.isArray(platform.packages) ? platform.packages : [],
      deployment: platform.deployment ?? null,
      file: rel,
      screenCount: list.length,
    });

    for (const screen of list) {
      if (!screen?.id) continue;
      if (screens.has(screen.id)) {
        problems.push({
          severity: 'error',
          kind: 'duplicate-screen',
          file: rel,
          message: `Screen id ${screen.id} is defined in two places`,
        });
        continue;
      }
      screens.set(screen.id, {
        id: screen.id,
        name: screen.name ?? screen.id,
        module: screen.module ?? null,
        purpose: screen.purpose ?? '',
        capability: screen.capability ?? null,
        requirements: Array.isArray(screen.requirements) ? screen.requirements : [],
        wave: screen.wave ?? null,
        permission: screen.permission ?? null,
        platform: platform.code ?? null,
        platformName: platform.name ?? null,
        offlineCapable: Boolean(platform.offlineCapable),
        file: rel,
        apis: (Array.isArray(screen.apis) ? screen.apis : []).map((a) => ({
          operationId: a?.operationId ?? '',
          purpose: a?.purpose ?? '',
          trigger: a?.trigger ?? null,
          contract: a?.contract ?? null,
        })),
        states: screen.states ?? null,
        navigation: screen.navigation ?? null,
        // 92 of 102 navigation blocks are derived rather than declared, so
        // the viewer has to say which — a sitemap that looks authoritative
        // while being mostly guessed is worse than no sitemap
        navigationInferred: Boolean(screen.navigation?.inferred),
        deployment: platform.deployment ?? null,
        accessibility: screen.accessibility ?? null,
        wireframe: screen.wireframe ?? null,
        implementation: screen.implementation ?? null,
        openQuestions: Array.isArray(screen.openQuestions) ? screen.openQuestions : [],
        notes: screen.notes ?? null,
        template: screen.layout?.template ?? null,
        regions: (screen.layout?.regions ?? []).map((r) => ({
          name: r?.name ?? '',
          ref: r?.ref ?? null,
          components: (r?.components ?? []).map((c) => ({
            kind: c?.kind ?? '',
            label: c?.label ?? '',
            bindsTo: c?.bindsTo ?? null,
            permission: c?.permission ?? null,
            notes: c?.notes ?? null,
          })),
        })),
      });
    }
  }

  return { screens, platforms };
}

/**
 * The shared vocabulary a screen's `kind` and region `ref` must draw from.
 * A component that is not in here is either the wrong one or needs adding
 * deliberately — which is the whole reason the file exists.
 */
async function readComponentVocabulary(root) {
  const empty = { regions: new Set(), components: new Set(), patterns: new Set() };
  let doc;
  try {
    doc = yaml.load(await readFile(path.join(root, 'screens', '_components.yaml'), 'utf8'));
  } catch {
    return empty; // no vocabulary file means the check simply does not run
  }
  // regions and patterns are keyed by `id`, components by `kind`
  const ids = (list, key) =>
    new Set((Array.isArray(list) ? list : []).map((x) => x?.[key]).filter(Boolean));
  return {
    regions: ids(doc?.regions, 'id'),
    components: new Set([...ids(doc?.components, 'kind'), ...ids(doc?.patterns, 'id')]),
    patterns: ids(doc?.patterns, 'id'),
  };
}

/**
 * @param contractOperationIds  every operationId the contracts declare, so a
 *                              screen or step pointing at a missing one shows up
 */
export async function buildJourneys(root, contractOperationIds = new Set()) {
  const problems = [];

  const screenFiles = await readYamlDir(root, 'screens', (n) => !n.startsWith('_'));
  const flowFiles = await readYamlDir(root, 'flows', (n) => !n.startsWith('_'));
  const { screens, platforms } = indexScreens(screenFiles, problems);
  const vocabulary = await readComponentVocabulary(root);

  for (const screen of screens.values()) {
    // apis pointing at an operation the contracts do not have
    for (const api of screen.apis) {
      if (api.operationId && contractOperationIds.size && !contractOperationIds.has(api.operationId)) {
        problems.push({
          severity: 'error',
          kind: 'screen-unknown-operation',
          file: screen.file,
          message: `Screen ${screen.id} calls ${api.operationId}, which no contract declares`,
        });
      }
    }

    // the four states rule — offline only where the platform is offline-capable
    const required = ['loading', 'empty', 'error'];
    if (screen.offlineCapable) required.push('offline');
    const missing = required.filter((state) => !screen.states?.[state]);
    if (missing.length) {
      problems.push({
        severity: 'warning',
        kind: 'screen-missing-state',
        file: screen.file,
        message:
          `Screen ${screen.id} declares no ${missing.join(', ')} state` +
          `${missing.length > 1 ? 's' : ''} — the empty state is the one that reaches production unconsidered`,
      });
    }

    // component kinds must exist in the shared vocabulary, and regions too
    for (const region of screen.regions) {
      if (region.ref && vocabulary.regions.size && !vocabulary.regions.has(region.ref)) {
        problems.push({
          severity: 'error',
          kind: 'screen-unknown-region',
          file: screen.file,
          message: `Screen ${screen.id} uses region ${region.ref}, which _components.yaml does not define`,
        });
      }
      for (const component of region.components) {
        if (component.kind && vocabulary.components.size && !vocabulary.components.has(component.kind)) {
          problems.push({
            severity: 'error',
            kind: 'screen-unknown-component',
            file: screen.file,
            message: `Screen ${screen.id} uses component ${component.kind}, which _components.yaml does not define`,
          });
        }
      }
    }
  }

  // navigation has to resolve, or a route leads somewhere that does not exist
  for (const screen of screens.values()) {
    for (const [direction, list] of [
      ['entryFrom', screen.navigation?.entryFrom],
      ['exitTo', screen.navigation?.exitTo],
    ]) {
      for (const target of Array.isArray(list) ? list : []) {
        if (!screens.has(target)) {
          problems.push({
            severity: 'error',
            kind: 'screen-unknown-navigation',
            file: screen.file,
            message: `Screen ${screen.id} ${direction} ${target}, which no platform file defines`,
          });
        }
      }
    }
  }

  const flows = [];
  for (const { rel, doc, error } of flowFiles) {
    if (error) {
      problems.push({ severity: 'error', kind: 'parse-error', file: rel, message: error });
      continue;
    }
    if (!doc?.id) continue;

    const steps = (Array.isArray(doc.steps) ? doc.steps : []).map((step) => {
      const screen = screens.get(step?.screen) ?? null;
      if (step?.screen && !screen) {
        problems.push({
          severity: 'error',
          kind: 'flow-unknown-screen',
          file: rel,
          message: `${doc.id} step ${step.step} runs on screen ${step.screen}, which no platform file defines`,
        });
      }

      const operations = (Array.isArray(step?.operations) ? step.operations : []).map((id) => {
        // the useful check: the step calls something its own screen never declares
        const onScreen = screen ? screen.apis.some((a) => a.operationId === id) : false;
        if (screen && !onScreen) {
          problems.push({
            severity: 'error',
            kind: 'flow-operation-not-on-screen',
            file: rel,
            message:
              `${doc.id} step ${step.step} calls ${id} from ${screen.id}, ` +
              `but that screen does not declare it`,
          });
        }
        const known = !contractOperationIds.size || contractOperationIds.has(id);
        if (!known) {
          problems.push({
            severity: 'error',
            kind: 'flow-unknown-operation',
            file: rel,
            message: `${doc.id} step ${step.step} calls ${id}, which no contract declares`,
          });
        }
        return { operationId: id, onScreen, known };
      });

      return {
        step: step?.step ?? 0,
        screenId: step?.screen ?? null,
        screenName: screen?.name ?? null,
        platform: screen?.platform ?? null,
        module: screen?.module ?? null,
        action: step?.action ?? '',
        outcome: step?.outcome ?? '',
        duration: step?.duration ?? null,
        operations,
      };
    });

    const branches = (Array.isArray(doc.branches) ? doc.branches : []).map((b) => ({
      at: b?.at ?? null,
      condition: b?.condition ?? '',
      behaviour: b?.behaviour ?? '',
      severity: b?.severity ?? null,
      resolvedBy: b?.resolvedBy ?? null,
    }));

    if (!branches.length) {
      problems.push({
        severity: 'warning',
        kind: 'flow-no-branches',
        file: rel,
        message: `${doc.id} declares no branches — a flow with only a happy path describes a demo`,
      });
    }

    flows.push({
      id: doc.id,
      name: doc.name ?? doc.id,
      file: rel,
      actor: doc.actor ?? null,
      capability: doc.capability ?? null,
      wave: doc.wave ?? null,
      frequency: doc.frequency ?? null,
      criticality: doc.criticality ?? null,
      platforms: Array.isArray(doc.platforms) ? doc.platforms : [],
      offlineBehaviour: doc.offlineBehaviour ?? null,
      trigger: doc.trigger ?? null,
      steps,
      branches,
      exitStates: Array.isArray(doc.exitStates) ? doc.exitStates : [],
      openQuestions: Array.isArray(doc.openQuestions) ? doc.openQuestions : [],
    });
  }

  flows.sort((a, b) => String(a.id).localeCompare(String(b.id)));

  // which screens / flows touch a given operation — the traceability index
  const operationUsage = new Map();
  const note = (id, entry) => {
    if (!id) return;
    if (!operationUsage.has(id)) operationUsage.set(id, { screens: [], flows: [] });
    const bucket = operationUsage.get(id);
    if (entry.screen && !bucket.screens.includes(entry.screen)) bucket.screens.push(entry.screen);
    if (entry.flow && !bucket.flows.includes(entry.flow)) bucket.flows.push(entry.flow);
  };
  for (const screen of screens.values()) {
    for (const api of screen.apis) note(api.operationId, { screen: screen.id });
  }
  for (const flow of flows) {
    for (const step of flow.steps) {
      for (const op of step.operations) note(op.operationId, { flow: flow.id });
    }
  }

  const apps = await readApps(root, screens, problems);

  return {
    flows,
    platforms,
    apps,
    screens: [...screens.values()],
    operationUsage: Object.fromEntries(operationUsage),
    problems,
    stats: {
      flows: flows.length,
      steps: flows.reduce((a, f) => a + f.steps.length, 0),
      branches: flows.reduce((a, f) => a + f.branches.length, 0),
      screens: screens.size,
      screensWithNavigation: [...screens.values()].filter((s) => s.navigation).length,
      navigationInferred: [...screens.values()].filter((s) => s.navigationInferred).length,
      platforms: platforms.length,
      apps: apps.length,
      scaffolded: apps.filter((a) => a.status === 'scaffolded').length,
      operationsCovered: operationUsage.size,
    },
  };
}

/**
 * The per-app manifests in frontend/. Generated from screens/, so the check
 * worth making here is whether the two still agree.
 */
async function readApps(root, screens, problems) {
  const files = await readYamlDir(root, 'frontend');
  const apps = [];

  for (const { rel, doc, error } of files) {
    if (error) {
      problems.push({ severity: 'error', kind: 'parse-error', file: rel, message: error });
      continue;
    }
    if (!doc?.app) continue;

    const list = Array.isArray(doc.screens) ? doc.screens : [];
    const routes = new Map();
    for (const screen of list) {
      if (!screen?.route) continue;
      if (routes.has(screen.route)) {
        problems.push({
          severity: 'error',
          kind: 'app-route-collision',
          file: rel,
          message:
            `${doc.app} maps ${routes.get(screen.route)} and ${screen.id} to ${screen.route} — ` +
            `two screens on one route surfaces as "sometimes the wrong page loads"`,
        });
      } else {
        routes.set(screen.route, screen.id);
      }
      if (screen.id && !screens.has(screen.id)) {
        problems.push({
          severity: 'warning',
          kind: 'app-unknown-screen',
          file: rel,
          message: `${doc.app} lists ${screen.id}, which no platform file defines`,
        });
      }
    }

    // an app that queues writes needs somewhere to queue them
    if (doc.offlineCapable && !(doc.packages ?? []).some((p) => /offline/i.test(p))) {
      problems.push({
        severity: 'warning',
        kind: 'app-offline-without-core',
        file: rel,
        message: `${doc.app} is offline-capable but depends on no offline package`,
      });
    }

    apps.push({
      app: doc.app,
      file: rel,
      status: doc.status ?? null,
      runtime: doc.runtime ?? null,
      offlineCapable: Boolean(doc.offlineCapable),
      directions: Array.isArray(doc.directions) ? doc.directions : [],
      platforms: Array.isArray(doc.platforms) ? doc.platforms : [],
      packages: Array.isArray(doc.packages) ? doc.packages : [],
      contracts: Array.isArray(doc.contracts) ? doc.contracts : [],
      screenCount: doc.screenCount ?? list.length,
      byWave: doc.byWave ?? null,
      screens: list.map((s) => ({
        id: s?.id ?? '',
        name: s?.name ?? '',
        route: s?.route ?? '',
        component: s?.component ?? '',
        wave: s?.wave ?? null,
        status: s?.status ?? null,
      })),
    });
  }

  apps.sort((a, b) => b.screenCount - a.screenCount);
  return apps;
}
