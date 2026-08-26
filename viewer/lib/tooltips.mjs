// handoff/tooltips.json — the delivery's own hover text.
//
// The viewer already had a glossary: hand-written, covering vocabulary the
// package uses without defining anywhere in a field — `spine`, `ambient`,
// `retryThenDeadLetter`. This file covers the other half, and it is the half a
// glossary cannot hold: the 230 individual tables, the 22 contracts, the 18
// ADRs. 340 entries in nine categories.
//
// The two barely overlap, so they compose rather than compete. Where they do,
// this one wins for the same reason a component description does — it is what
// the project says about itself.
//
// The README states the rule these were written to, and it is worth keeping:
//
//   "Table tips say why, not what. platform.outbox reads 'events written in the
//   same transaction as the state change' — not 'outbox table'. The column list
//   is already on screen; the hover should carry what the diagram cannot."
//
// It also says they are GENERATED — from x-ticvai-module, contract descriptions
// and ADR decision sections. Generated content goes stale silently, and a hover
// card asserting something the contract no longer says is worse than a stale
// document because nobody reads a hover card sceptically. So this does not just
// load the file: it checks every key against the thing it claims to describe,
// and reports both directions.

import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';

const FILE = path.join('handoff', 'tooltips.json');

/** Categories that can be cross-checked, and what they must resolve against. */
const CHECKED = [
  { key: 'tables', noun: 'table', subject: 'tables' },
  { key: 'contracts', noun: 'contract', subject: 'contracts' },
  { key: 'platforms', noun: 'platform', subject: 'platforms' },
  { key: 'modules', noun: 'schema module', subject: 'modules' },
  { key: 'flows', noun: 'flow', subject: 'flows' },
  { key: 'adrs', noun: 'ADR', subject: 'adrs' },
];

/**
 * A hover card holds two or three lines. Some of these tips are not that.
 *
 * The 22 contract tips are the whole of `info.description` with its newlines
 * collapsed — heading, summary, a markdown table of tier and requirements, then
 * "## How to read this file" and several hundred words more. Rendered verbatim
 * that is a wall of text with pipe characters in it.
 *
 * The author did write a summary, though: the bold sentence directly under the
 * heading. `**The highest-frequency operation in a venue. Must work with no
 * network.**` is exactly what belongs on the card, so when a tip is really a
 * document this takes that sentence and leaves the rest to the Reader.
 */
function condense(text) {
  const isDocument = /^#{1,6}\s/.test(text) || text.includes('|---');
  if (!isDocument) return text;
  const bold = /\*\*([^*]{20,400})\*\*/.exec(text);
  if (bold) return bold[1].trim();
  // no bold summary — take the first sentence after the heading instead
  const afterHeading = text.replace(/^#{1,6}\s*[^.|]*/, '').trim();
  const sentence = /^[^.|]{20,300}\./.exec(afterHeading);
  return (sentence ? sentence[0] : afterHeading.slice(0, 240)).trim();
}

/** The ADR files on disk, so a tip for a decision nobody wrote is caught. */
async function readAdrIds(root) {
  const dir = path.join(root, 'docs', 'adr');
  const files = await readdir(dir).catch(() => []);
  const ids = new Map();
  for (const file of files) {
    const match = /^(\d{4})-(.+)\.md$/i.exec(file);
    if (match) ids.set(match[1], { file: `docs/adr/${file}`, slug: match[2] });
  }
  return ids;
}

/**
 * @param root
 * @param subjects  { tables, contracts, platforms, modules, flows } — the ids each
 *                  category must resolve against. A category with no subject list
 *                  is loaded and simply not checked.
 */
export async function buildTooltips(root, subjects = {}) {
  const problems = [];
  const abs = path.join(root, FILE);
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) {
    return { present: false, file: FILE, entries: {}, problems, stats: { total: 0 } };
  }

  let doc;
  try {
    doc = JSON.parse(await readFile(abs, 'utf8'));
  } catch (err) {
    problems.push({
      severity: 'error',
      kind: 'tooltips-unreadable',
      file: FILE,
      message: `tooltips.json will not parse (${err.message}), so nothing in the viewer can explain itself from the delivery's own words.`,
    });
    return { present: false, file: FILE, entries: {}, problems, stats: { total: 0 } };
  }

  const adrs = await readAdrIds(root);
  const entries = {};
  const counts = {};
  let empty = 0;
  let restated = 0;

  for (const [category, group] of Object.entries(doc)) {
    if (!group || typeof group !== 'object') continue;
    const bucket = (entries[category] = {});
    for (const [key, value] of Object.entries(group)) {
      const tipText = typeof value === 'string' ? value : value?.tip;
      // "A missing key means no tooltip, not an empty one. An empty hover card is
      // worse than none, because it invites a second hover." Hold the file to it.
      if (!tipText || !String(tipText).trim()) {
        empty += 1;
        continue;
      }
      const text = String(tipText).trim();
      const entry = typeof value === 'string' ? { tip: text } : { ...value, tip: text };

      entry.tip = condense(entry.tip);

      // The README's own rule, applied to the README's own file: a tip reading
      // "Derived from fnb.Menu" is the same failure as an empty one wearing
      // text. It answers "where did this row come from", which the viewer
      // already shows, and not "why does this table exist", which it cannot.
      // Marked rather than dropped, so the viewer can fall back to something
      // better and the count of real coverage stays honest.
      entry.restated = /^derived from\b/i.test(entry.tip) || entry.tip.length < 25;
      if (entry.restated) restated += 1;

      bucket[key] = entry;
    }
    counts[category] = Object.keys(bucket).length;
  }

  if (restated) {
    const tables = Object.values(entries.tables ?? {});
    const weak = tables.filter((e) => e.restated).length;
    problems.push({
      severity: 'warning',
      kind: 'tooltip-restates-the-name',
      file: FILE,
      message:
        `${restated} of ${Object.values(counts).reduce((a, b) => a + b, 0)} tips say only where the row came ` +
        `from — "Derived from access.AccessPoint." — rather than why the thing exists` +
        (weak ? `, including ${weak} of the ${tables.length} table tips` : '') +
        `. tooltips-README states the rule these were written to: "a tip reading 'Derived from fnb.Menu' ` +
        `is the same failure wearing text". So the coverage table's 230 of 230 counts keys, not answers.`,
    });
  }

  if (empty) {
    problems.push({
      severity: 'warning',
      kind: 'tooltip-empty',
      file: FILE,
      message:
        `${empty} entr${empty > 1 ? 'ies have' : 'y has'} no tip text. The file's own rule is that a ` +
        `missing key means no tooltip rather than an empty one, so these are dropped rather than shown blank.`,
    });
  }

  // ---- cross-checks --------------------------------------------------------
  const known = {
    adrs: new Set(adrs.keys()),
    ...Object.fromEntries(
      Object.entries(subjects).map(([k, v]) => [k, new Set((v ?? []).map(String))])
    ),
  };

  for (const { key, noun, subject } of CHECKED) {
    const have = entries[key];
    const should = known[subject];
    if (!have || !should?.size) continue;

    const stale = Object.keys(have).filter((id) => !should.has(id));
    if (stale.length) {
      problems.push({
        severity: 'warning',
        kind: 'tooltip-stale',
        file: FILE,
        message:
          `${stale.length} ${noun} tip${stale.length > 1 ? 's describe' : ' describes'} something the package ` +
          `no longer has (${stale.slice(0, 4).join(', ')}${stale.length > 4 ? '…' : ''}). These are generated, ` +
          `so this means the generator ran against an older package.`,
      });
    }

    const uncovered = [...should].filter((id) => !have[id]);
    if (uncovered.length) {
      problems.push({
        severity: 'info',
        kind: 'tooltip-uncovered',
        file: FILE,
        message:
          `${uncovered.length} of ${should.size} ${noun}s have no tip ` +
          `(${uncovered.slice(0, 4).join(', ')}${uncovered.length > 4 ? '…' : ''}). Hovering them falls back ` +
          `to the viewer's own glossary, or to nothing.`,
      });
    }
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return {
    present: true,
    file: FILE,
    // "regenerate rather than edit" — so when it was last generated is worth showing
    modified: info.mtime.toISOString(),
    entries,
    adrFiles: Object.fromEntries(adrs),
    problems,
    stats: {
      total,
      ...counts,
      categories: Object.keys(counts).length,
      empty,
      restated,
      // the number that matters: tips that answer something the screen cannot
      substantive: total - restated,
    },
  };
}
