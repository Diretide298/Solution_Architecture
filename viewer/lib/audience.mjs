/**
 * What a client is allowed to read.
 *
 * A client is somebody outside the company who has been given a login to read
 * the package. The rule is **everything except the decisions**: they see the
 * product, the interface, the data model and the state machines — the whole
 * deliverable — and not the arguments that produced it.
 *
 *   sees      Frontend   screens, journeys, apps, waves
 *             Contracts  the API they will build against
 *             Domain     state models and events
 *             Backend    the data model, migrations, routing
 *             Services   what ships together, and in what order
 *
 *   does not  Decisions  the ADRs, the registers, the conflict log
 *
 * Services is on the first list for the same reason the other four are: it
 * describes what is being built. It names ADR-0028 as the decision behind it,
 * which is a path rather than the prose — and a client asking /api/file for
 * anything under docs/adr/ is refused by the rule below, so the reference is
 * inert for them and real for everyone else.
 *
 * Why that one and nothing else: an ADR records the options that were rejected,
 * what they would have cost, which vendor lost and why, and what has since been
 * superseded. That is deliberation, and a reader who takes a rejected option
 * for a current one is reading something that was never meant to be a
 * statement. The rest of the package is a description of what is being built,
 * which is the thing a client is entitled to.
 *
 * The rule this file exists to enforce: **a client's payload must not contain
 * the branch at all**, rather than contain it and have the browser decline to
 * draw it. A client handed a login can open devtools and fetch whatever the
 * server will answer. Hiding a tab in `app.js` is decoration; this is the
 * access control.
 *
 * Named `client` and not `guest` because the package already has a guest — its
 * own word for a venue visitor, on 96 operations in `x-ticvai-audience`.
 */

/**
 * Routes a client may not call. Everything else is theirs.
 *
 * Bare route names, not paths. The same route is reachable as
 * `/pkg/<project>/decisions` and — until the client moves — `/api/decisions`,
 * and a deny list spelled as a path would have started silently allowing the
 * first of those. A permission check that fails open on a rename is the worst
 * kind to leave lying around, so it is given the one name the server resolves
 * both spellings to.
 */
const CLIENT_DENIED = new Set(['decisions']);

export function clientMayCall(route) {
  return !CLIENT_DENIED.has(route);
}

/**
 * Files a client may not read through /api/file or /api/tree.
 *
 * This is the leak that makes the endpoint list insufficient on its own:
 * /api/file will return any .md in the tree, and the ADRs are .md files. Refuse
 * /api/decisions and leave the endpoint open, and a client reads every ADR one
 * path at a time.
 *
 * The list is derived from the decisions payload rather than hardcoded, so it
 * is exactly what the Decisions layer serves and stays right as the package
 * changes. A new register appears in `docs/registers/` and it is covered
 * without anybody remembering to add it here.
 */
export function decisionFiles(decisions) {
  const files = new Set();
  for (const adr of decisions?.adrs ?? []) if (adr.file) files.add(adr.file);
  for (const doc of decisions?.documents ?? []) if (doc.file) files.add(doc.file);
  // The normative spec the Decisions layer executes, which names it in prose.
  files.add('docs/architecture/specs/permission-vectors.json');
  return files;
}

/**
 * True when this path is part of the Decisions layer.
 *
 * Compared with the path normalised the way /api/file receives it — forward
 * slashes, no leading ./ — because a Windows-authored path and a URL parameter
 * have to agree here or the check silently passes everything.
 */
export function isDecisionFile(rel, files) {
  const norm = String(rel).replace(/\\/g, '/').replace(/^\.\//, '');
  if (files.has(norm)) return true;
  // Every ADR, including one added since the payload was built.
  return /^docs\/adr\//i.test(norm);
}

/**
 * The layers a role may open, in the order the tab strip draws them. The client
 * reads this rather than deciding for itself, so the tabs and the payload can
 * never disagree — the browser is told what it has, not asked to guess.
 */
export function layersFor(role) {
  return role === 'client'
    ? ['frontend', 'contracts', 'domain', 'backend', 'services']
    : ['frontend', 'contracts', 'domain', 'backend', 'services', 'decisions'];
}

/** null means "whatever the layer normally offers". A client gets every mode
 *  of every layer they can open, including Audit: they see the package as it
 *  is, and a defect count is part of how it is. */
export function modesFor() {
  return null;
}

// There is deliberately no per-endpoint payload filter. A client either may
// call an endpoint or may not, and on the ones they may they receive exactly
// what a reviewer receives. A filter that hollows out a payload is a second
// place for the rule to live, and the second place is the one that drifts.
