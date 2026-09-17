/**
 * Change requests: where the package was found wrong.
 *
 * Raised by the team - often by a developer's Claude while building, after the
 * developer agreed - and settled here by an admin or a reviewer on the project.
 * The list is the project's own; switching project is a reload with ?project=.
 * Everything shown can be exported as CSV, filters applied.
 */
import * as auth from '/validation.js';
import { hideLoader } from '/loader.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const STATUS = { open: 'Open', accepted: 'Accepted', rejected: 'Rejected', done: 'Done' };
const KINDS = {
  operation: 'Operation', schema: 'Schema', contract: 'Contract', table: 'Table',
  screen: 'Screen', flow: 'Journey', module: 'Module', service: 'Service', adr: 'Decision',
  platform: 'Platform', state: 'State model', event: 'Event', other: 'Other',
};

const state = {
  project: null,
  items: [],
  counts: {},
  mayResolve: false,
  me: null,
  filter: { status: 'open,accepted', blocking: false, text: '' },
};

const fmt = (iso) => (iso ? new Date(iso).toLocaleString(undefined,
  { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '');

function showError(message) {
  $('cr-error').textContent = message;
  $('cr-error').hidden = !message;
}

// ── reading ──────────────────────────────────────────────────────────

async function load() {
  try {
    const data = await auth.listChanges(state.project);
    state.items = data.items ?? [];
    state.counts = data.counts ?? {};
    state.mayResolve = Boolean(data.mayResolve);
    showError('');
  } catch (error) {
    state.items = [];
    showError(error.status === 403
      ? 'Change requests are for the delivery team; this account cannot see them.'
      : `Could not read the change requests: ${error.message}`);
  }
  draw();
}

function shown() {
  const f = state.filter;
  const wanted = f.status ? f.status.split(',') : null;
  const needle = f.text.trim().toLowerCase();
  return state.items.filter((c) => {
    if (wanted && !wanted.includes(c.status)) return false;
    if (f.blocking && !c.blocking) return false;
    if (needle) {
      const hay = [c.id, c.title, c.target.kind, c.target.id, c.ticket, c.raisedBy, c.problem,
        c.resolution].join(' ').toLowerCase();
      if (!hay.includes(needle)) return false;
    }
    return true;
  });
}

// ── drawing ──────────────────────────────────────────────────────────

function drawHeadline() {
  const box = $('cr-headline');
  box.innerHTML = '';
  const stat = (value, label, hint) => {
    const card = el('div', 'stat-card');
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };
  const blocking = state.items.filter((c) => c.blocking && ['open', 'accepted'].includes(c.status)).length;
  box.append(stat(state.counts.open ?? 0, 'open', 'waiting for a decision'));
  box.append(stat(state.counts.accepted ?? 0, 'accepted', 'the package needs fixing'));
  box.append(stat(blocking, 'blocking work', blocking ? 'tickets are waiting on these' : 'nothing is held up'));
  box.append(stat(state.counts.done ?? 0, 'done', 'fixed in the package'));
  box.append(stat(state.counts.rejected ?? 0, 'rejected', 'the package was right'));
}

function drawStatusSeg() {
  const host = $('cr-status');
  host.innerHTML = '';
  const options = [
    ['open,accepted', 'Needs action'], ['open', 'Open'], ['accepted', 'Accepted'],
    ['done', 'Done'], ['rejected', 'Rejected'], ['', 'All'],
  ];
  for (const [value, label] of options) {
    const b = el('button', null, label);
    b.type = 'button';
    if (state.filter.status === value) b.classList.add('active');
    b.onclick = () => { state.filter.status = value; draw(); };
    host.append(b);
  }
}

function block(label, text, pre = false) {
  if (!text) return null;
  const wrap = el('div', 'cr-block');
  wrap.append(el('div', 'cr-label', label));
  wrap.append(el(pre ? 'pre' : 'p', pre ? 'cr-pre' : 'cr-text', text));
  return wrap;
}

function actions(c) {
  const bar = el('div', 'cr-actions');
  if (!state.mayResolve) return bar;
  const mine = state.me && c.raisedBy && [state.me.name, state.me.email].includes(c.raisedBy);
  const admin = state.me?.role === 'admin';
  const note = el('input', 'auth-input cr-note');
  note.placeholder = 'Why, or what was decided';
  const ref = el('input', 'auth-input cr-ref');
  ref.placeholder = 'Fixed by (commit, ADR, contract version)';
  const act = async (status) => {
    try {
      await auth.resolveChange(state.project, c.id, status, note.value, ref.value);
      await load();
    } catch (error) {
      showError(`${c.id}: ${error.message}`);
    }
  };
  const button = (label, status, cls = '') => {
    const b = el('button', `chip ${cls}`.trim(), label);
    b.type = 'button';
    b.onclick = () => act(status);
    return b;
  };
  if (c.status === 'open') {
    // Somebody else has to agree the package is wrong - the server says so too.
    if (!mine || admin) {
      bar.append(note, button('Accept', 'accepted', 'cr-accept'), button('Reject', 'rejected', 'cr-reject'));
    } else {
      bar.append(el('span', 'cr-hint', 'Somebody else on the team accepts or rejects this.'));
    }
  } else if (c.status === 'accepted') {
    bar.append(ref, note, button('Mark done', 'done', 'cr-accept'), button('Reopen', 'open'));
  } else {
    bar.append(note, button('Reopen', 'open'));
  }
  return bar;
}

function card(c) {
  const box = el('details', `cr-card cr-${c.status}`);
  const summary = el('summary', 'cr-summary');
  summary.append(el('span', 'cr-id', c.id));
  summary.append(el('span', `cr-badge cr-badge-${c.status}`, STATUS[c.status] ?? c.status));
  if (c.blocking && ['open', 'accepted'].includes(c.status)) summary.append(el('span', 'cr-badge cr-badge-blocking', 'Blocking'));
  summary.append(el('span', 'cr-title', c.title));
  const meta = el('span', 'cr-meta');
  meta.append(el('code', null, `${KINDS[c.target.kind] ?? c.target.kind} ${c.target.id}`));
  if (c.ticket) meta.append(` · #${c.ticket}`);
  meta.append(` · ${c.raisedBy}${c.raisedVia === 'claude' ? ' via Claude' : ''} · ${fmt(c.raisedAt)}`);
  summary.append(meta);
  box.append(summary);

  const body = el('div', 'cr-body');
  for (const part of [
    block('Problem', c.problem),
    block('Evidence', c.evidence, true),
    c.options?.length ? (() => {
      const wrap = el('div', 'cr-block');
      wrap.append(el('div', 'cr-label', 'Options'));
      const list = el('ol', 'cr-options');
      for (const o of c.options) list.append(el('li', null, o));
      wrap.append(list);
      return wrap;
    })() : null,
    block('Recommendation', c.recommendation),
    c.resolvedAt ? block(`${STATUS[c.status] ?? 'Settled'} by ${c.resolvedBy ?? '?'} · ${fmt(c.resolvedAt)}`,
      [c.resolution, c.resolvedRef && `Fixed by: ${c.resolvedRef}`].filter(Boolean).join('\n') || '-') : null,
  ]) if (part) body.append(part);
  body.append(actions(c));
  box.append(body);
  return box;
}

function draw() {
  drawHeadline();
  drawStatusSeg();
  const list = $('cr-list');
  list.innerHTML = '';
  const rows = shown();
  if (!rows.length) {
    list.append(el('p', 'cr-empty', state.items.length
      ? 'Nothing matches these filters.'
      : 'No change requests in this project yet.'));
    return;
  }
  for (const c of rows) list.append(card(c));
}

// ── export ───────────────────────────────────────────────────────────

function exportCsv() {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const rows = shown();
  const lines = [
    ['id', 'status', 'blocking', 'title', 'kind', 'artefact', 'ticket', 'raised by', 'raised via',
      'raised at', 'problem', 'evidence', 'options', 'recommendation', 'settled by', 'settled at',
      'resolution', 'fixed by'].join(','),
    ...rows.map((c) => [
      c.id, STATUS[c.status] ?? c.status, c.blocking ? 'yes' : 'no', c.title,
      KINDS[c.target.kind] ?? c.target.kind, c.target.id, c.ticket, c.raisedBy, c.raisedVia,
      c.raisedAt, c.problem, c.evidence, (c.options ?? []).join(' | '), c.recommendation,
      c.resolvedBy ?? '', c.resolvedAt ?? '', c.resolution, c.resolvedRef,
    ].map(esc).join(',')),
  ].join('\r\n');
  // A BOM, so Excel on Windows reads the dashes and quotes as written.
  const url = URL.createObjectURL(new Blob(['﻿' + lines], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  const narrowed = state.filter.status || state.filter.blocking || state.filter.text.trim();
  a.download = `${state.project}-change-requests${narrowed ? '-filtered' : ''}-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

// ── raising ──────────────────────────────────────────────────────────

function wireForm() {
  const form = $('cr-form');
  const kind = $('cr-f-kind');
  for (const [value, label] of Object.entries(KINDS)) {
    const o = el('option', null, label);
    o.value = value;
    kind.append(o);
  }
  $('cr-new-toggle').onclick = () => { form.hidden = !form.hidden; };
  $('cr-f-cancel').onclick = () => { form.hidden = true; };
  form.onsubmit = async (event) => {
    event.preventDefault();
    try {
      const made = await auth.raiseChange(state.project, {
        target_kind: kind.value,
        target_id: $('cr-f-target').value,
        title: $('cr-f-title').value,
        problem: $('cr-f-problem').value,
        evidence: $('cr-f-evidence').value,
        options: $('cr-f-options').value.split('\n').map((s) => s.trim()).filter(Boolean),
        recommendation: $('cr-f-recommendation').value,
        blocking: $('cr-f-blocking').checked,
        ticket: $('cr-f-ticket').value.trim(),
      });
      form.reset();
      form.hidden = true;
      state.filter.status = 'open,accepted';
      await load();
      showError('');
      $('cr-error').hidden = true;
      document.title = `Adam — ${made.change.id} raised`;
    } catch (error) {
      showError(`Not raised: ${Array.isArray(error.message) ? JSON.stringify(error.message) : error.message}`);
    }
  };
}

// ── start ────────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${state.me.role}` : '';
  state.project = await auth.ensureProject();

  // The projects this account may open, by name, for the switcher.
  const picker = $('cr-project');
  try {
    const registry = await auth.listProjects();
    const names = Object.fromEntries((registry.projects ?? []).map((p) => [p.id, p.name || p.id]));
    const mine = (state.me?.projects ?? []).map((p) => p.id);
    for (const id of (mine.length ? mine : Object.keys(names))) {
      const o = el('option', null, names[id] ?? id);
      o.value = id;
      if (id === state.project) o.selected = true;
      picker.append(o);
    }
  } catch { /* the page still works for the current project */ }
  picker.onchange = () => {
    auth.rememberProject(picker.value);
    location.search = `?project=${encodeURIComponent(picker.value)}`;
  };

  drawStatusSeg();
  $('cr-blocking').onchange = (e) => { state.filter.blocking = e.target.checked; draw(); };
  $('cr-text').oninput = (e) => { state.filter.text = e.target.value; draw(); };
  $('cr-export').onclick = exportCsv;
  wireForm();
  await load();
  hideLoader();
})();
