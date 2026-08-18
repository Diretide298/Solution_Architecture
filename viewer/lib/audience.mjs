/**
 * What a guest is allowed to read.
 *
 * A guest is an outside client, not a contractor. The decision of 17 August is
 * that they see their product and the interface they will build against, and
 * nothing about how it was argued for or how it is stored:
 *
 *   sees      Frontend — Screen, Journey, Apps, Waves
 *             Contracts — Reader, Structure
 *
 *   does not  Decisions      rejected options, cost arguments, vendor choices
 *             Audit          a live defect count is our own quality control
 *             Backend        row-security policies, read/write routing
 *             Lineage        a candour page naming what is stale
 *             Verdicts       reviewers disagreeing, and per-person statistics
 *
 * The rule this file exists to enforce: **a guest's payload must not contain
 * the branch at all**, rather than contain it and have the browser decline to
 * draw it. A client handed a login can open devtools and fetch whatever the
 * server will answer. Hiding a tab in `app.js` is decoration; this is the
 * access control.
 */

/** Endpoints a guest may call at all. Everything else is refused outright. */
const GUEST_ENDPOINTS = new Set([
  '/api/index',
  '/api/detail',
  '/api/journeys',
  '/api/tooltips',
  '/api/events',
]);

export function guestMayCall(pathname) {
  return GUEST_ENDPOINTS.has(pathname);
}

/**
 * The layers a role may open, in the order the tab strip draws them. The client
 * reads this rather than deciding for itself, so the tabs and the payload can
 * never disagree — the browser is told what it has, not asked to guess.
 */
export function layersFor(role) {
  return role === 'guest'
    ? ['frontend', 'contracts']
    : ['frontend', 'contracts', 'domain', 'backend', 'decisions'];
}

export function modesFor(role) {
  return role === 'guest'
    ? { frontend: ['screen', 'journey', 'apps', 'waves'], contracts: ['reader', 'structure'] }
    : null; // null means "whatever the layer normally offers"
}

/**
 * The index, with everything a guest may not see taken out.
 *
 * `problems` is the one that matters most and is easiest to miss: it is the
 * audit, carried inside the index rather than fetched separately, so filtering
 * the Audit *view* would have left the defect list in the payload.
 */
export function indexForGuest(index) {
  if (!index) return index;
  const { problems, structure, ...rest } = index;
  return {
    ...rest,
    // Kept as an empty list rather than dropped, so the client renders "nothing
    // to report" instead of breaking on an absent field.
    problems: [],
    guest: true,
  };
}

/**
 * Journeys, minus the reviewer's apparatus.
 *
 * The screens themselves are the point of a guest's view, so they stay whole.
 * What goes is the commentary about how complete they are.
 */
export function journeysForGuest(journeys) {
  if (!journeys) return journeys;
  const { problems, coverage, missing, ...rest } = journeys;
  return { ...rest, problems: [], guest: true };
}

/** One place that decides, so a new endpoint cannot quietly default to open. */
export function filterFor(role, pathname, payload) {
  if (role !== 'guest') return payload;
  if (pathname === '/api/index') return indexForGuest(payload);
  if (pathname === '/api/journeys') return journeysForGuest(payload);
  return payload;
}
