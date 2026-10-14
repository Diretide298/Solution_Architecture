/**
 * ADAM's own release notes.
 *
 * The content is a markdown file in this folder rather than rows in a database,
 * and that is the whole design. Release notes are written by a person, reviewed
 * in a diff alongside the change they describe, and deployed with it — so the
 * note and the thing it describes cannot drift apart, and nobody has to
 * remember to go and type it in somewhere afterwards.
 *
 * It is behind the same gate as every other page: what has changed in ADAM says
 * a good deal about what is being built and for whom.
 */

// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer. It also stamps the saved theme.
import '/page-chrome.js';
import { requireSignIn, servedBuild, connectorFleet } from '/validation.js';
import { markdownBlock } from '/core.js';
import { markUpdatesSeen } from '/account-drawer.js';
import { el, badge, ago } from '/sheet.js';

const $ = (id) => document.getElementById(id);

/**
 * One line: is the connector on your own machines the one ADAM serves?
 *
 * **Yours, not everybody's.** An administrator's fleet answer holds every
 * install in the team, and "LAPTOP-7 is behind" about somebody else's laptop is
 * a line the reader cannot act on. Settings, Claude connector, Builds is the
 * whole fleet; this is the reader's own machines, so the instruction in it is
 * one they can follow.
 *
 * **One instruction, always `/update-adam`.** It is the command every install
 * has: a zip install updates itself with it, and a plugin install is told by it
 * which marketplace command to run (mcp/update.mjs). Two commands on this page
 * would leave the reader working out which kind of install they have, which is
 * exactly what the updater already knows.
 *
 * Compared against `latest` (the whole connector, from `/connector/version`),
 * the number Settings compares against, so the two pages cannot disagree. Each
 * machine is counted once, at the build it last reported.
 */
async function drawFleet() {
  const line = $('up-fleet');
  const [serving, fleet] = await Promise.all([
    servedBuild().catch(() => ''),
    connectorFleet().catch(() => null),
  ]);
  line.replaceChildren();
  if (!serving) {
    // Nothing to compare against. Saying "current" here would be a guess.
    line.textContent = 'This ADAM does not serve a connector build, so there is nothing to compare yours with.';
    return;
  }
  if (!fleet) {
    line.textContent = `ADAM serves connector build ${serving}. It could not say which build your `
      + 'machines run; Settings, Claude connector, has the list.';
    return;
  }

  const seen = new Map();
  for (const install of (fleet.installs ?? []).filter((i) => i.mine)) {
    // Newest first from the service, so the first row per host is its build now.
    if (!seen.has(install.host)) seen.set(install.host, install);
  }
  const mine = [...seen.values()];
  if (!mine.length) {
    line.append(`ADAM serves connector build ${serving}. None of your machines has reported a `
      + 'build yet: a connector reports when Claude Code starts. ');
    const how = el('a', 'sh-link', 'How to install it');
    how.href = '/settings.html#connector';
    line.append(how, '.');
    return;
  }

  // Where every machine is listed, said once at the end of either answer. The
  // top bar's own "Your connector" chip went: this line is that link now, with
  // the answer in front of it.
  const listed = () => {
    const a = el('a', 'sh-link', 'Settings, Claude connector');
    a.href = '/settings.html#connector';
    return [' Every machine is listed in ', a, '.'];
  };

  const behind = mine.filter((i) => i.build !== serving);
  if (!behind.length) {
    line.append(badge('done', 'Current'), mine.length === 1
      ? `You're current: ${mine[0].host} runs build ${serving}, the one ADAM serves.`
      : `You're current: all ${mine.length} of your machines run build ${serving}, the one ADAM serves.`,
    ...listed());
    return;
  }
  const said = behind.map((i) => `${i.host} is behind (${i.build || 'no build'} vs ${serving})`);
  line.append(badge('stalled', 'Behind'), `${said.join('; ')}: run `, el('code', '', '/update-adam'),
    ' in Claude Code and restart it.');
  const when = ago(behind[0].at);
  if (when) line.append(el('span', 'up-fleet-when', ` ${behind.length === 1 ? 'It' : 'The first'} last reported ${when}.`));
  line.append(...listed());
}

if (await requireSignIn()) {
  $('updates').hidden = false;

  // First and separately: the one line on this page that is a fact about right
  // now. Its failure is not the page's failure (the notes are worth reading on
  // an ADAM too old to answer), so it degrades to nothing rather than an error.
  drawFleet().catch(() => { $('up-fleet').textContent = ''; });

  try {
    const answer = await fetch('/updates.md', { headers: { accept: 'text/markdown' } });
    if (!answer.ok) throw new Error(`the server answered ${answer.status}`);
    const text = await answer.text();

    // `adrLinks: false` — the renderer otherwise turns anything shaped like a
    // decision reference into a link into the package, and prose here mentions
    // things like `1.10` that are not decisions and would 404.
    const body = markdownBlock(text, { adrLinks: false });
    $('up-body').replaceChildren(body);

    // Read, so stop announcing them. Marked only once the notes are actually on
    // the page: marking on navigation would clear the chip for somebody whose
    // request failed, and they would never be told again.
    try {
      const stamped = await fetch('/updates/stamp', { headers: { accept: 'application/json' } });
      if (stamped.ok) markUpdatesSeen((await stamped.json()).stamp ?? '');
    } catch { /* the notes were read either way; the chip can wait */ }
  } catch (error) {
    $('up-body').replaceChildren();
    $('up-error').hidden = false;
    $('up-error').textContent = `The release notes could not be read (${error.message}). `
      + 'Reload the page; if it keeps happening, the file viewer/public/updates.md is missing from this ADAM.';
  }
} else {
  $('signed-out').hidden = false;
}
