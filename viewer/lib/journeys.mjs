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
        })),
        states: screen.states ?? null,
        navigation: screen.navigation ?? null,
        regions: (screen.layout?.regions ?? []).map((r) => ({
          name: r?.name ?? '',
          components: (r?.components ?? []).map((c) => ({
            kind: c?.kind ?? '',
            label: c?.label ?? '',
            permission: c?.permission ?? null,
          })),
        })),
      });
    }
  }

  return { screens, platforms };
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

  // screens whose declared apis point at an operation the contracts do not have
  for (const screen of screens.values()) {
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

  return {
    flows,
    platforms,
    screens: [...screens.values()],
    operationUsage: Object.fromEntries(operationUsage),
    problems,
    stats: {
      flows: flows.length,
      steps: flows.reduce((a, f) => a + f.steps.length, 0),
      branches: flows.reduce((a, f) => a + f.branches.length, 0),
      screens: screens.size,
      platforms: platforms.length,
      operationsCovered: operationUsage.size,
    },
  };
}
