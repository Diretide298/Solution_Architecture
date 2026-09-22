/**
 * Asking ADAM about the package, on whoever's key and whichever model.
 *
 * **The page gathers the context; the service holds the key.** ADAM's accounts
 * service cannot read a delivery package — that is the viewer's job — so this
 * searches the package for what the question is about, sends those excerpts
 * with it, and the service composes the call. Neither half has both, which is
 * also why no key is ever sent back to this page.
 *
 * **The picker is part of asking, not a setting.** Provider and model sit above
 * the question rather than in a preferences page, because trying a cheaper
 * model on a long question should cost one dropdown. The model field is a
 * combo: the list comes from the provider itself, and anything can be typed
 * into it, so a model released this morning needs no deploy here.
 *
 * What it will not do is file a change request by itself. When the answer says
 * the package is wrong, the page offers to draft one — through the same
 * draft-then-confirm flow the Claude connector uses, and with the same rule:
 * somebody reads it before it is filed.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const state = {
  providers: [],
  provider: null,
  turns: [],          // { role, text } — what is sent back as history
  search: null,       // the package's search index, fetched once
};

/** Which provider and model were last used, per browser. Not a server-side
 *  preference: two tabs on two packages may reasonably want different ones, and
 *  a stored default would have the second quietly retune the first. */
const REMEMBERED = 'adam-chat-pick';
const remember = (provider, model) => {
  try { localStorage.setItem(REMEMBERED, JSON.stringify({ provider, model })); } catch { /* fine */ }
};
const recall = () => {
  try { return JSON.parse(localStorage.getItem(REMEMBERED) ?? '{}'); } catch { return {}; }
};

function say(id, message) {
  $(id).textContent = message ?? '';
  if ($(id).hasAttribute('hidden') || message === '') $(id).hidden = !message;
}

// ── the picker ───────────────────────────────────────────────────────

function drawPicker() {
  const picker = $('ch-provider');
  picker.replaceChildren(...state.providers.map((p) => {
    const option = el('option', null, p.configured ? p.label : `${p.label} — no key`);
    option.value = p.id;
    return option;
  }));
  if (state.provider) picker.value = state.provider.id;
  drawProvider();
}

function drawProvider() {
  const p = state.provider;
  if (!p) return;
  $('ch-provider').value = p.id;

  const models = $('ch-models');
  models.replaceChildren(...p.models.map((m) => {
    const option = el('option');
    option.value = m;
    return option;
  }));
  const last = recall();
  const wanted = (last.provider === p.id && last.model) || p.models[0] || '';
  $('ch-model').value = wanted;
  $('ch-model').placeholder = p.models.length
    ? `${p.models.length} available, or type a name`
    : 'type a model name';

  $('ch-nokey').hidden = p.configured;
  $('ch-nokey-who').textContent = p.label;
  $('ch-endpoint').hidden = !p.needsEndpoint;
  if (p.needsEndpoint) $('ch-endpoint').value = p.endpoint ?? '';
  $('ch-keys-at').hidden = !p.keysAt;
  if (p.keysAt) $('ch-keys-at').href = p.keysAt;

  $('ch-keynote').textContent = p.configured
    ? `key ${p.hint} · ${p.endpoint}`
    : 'no key yet';
  $('ch-send').disabled = !p.configured;
}

// ── context: what the question is about ──────────────────────────────

/**
 * The package's own search index, fetched once.
 *
 * Every entry carries a `terms` string the viewer's search already matches on,
 * so this is the same index the search box uses rather than a second one with
 * its own idea of what a screen is called.
 */
async function index() {
  if (state.search) return state.search;
  const res = await auth.apiFetch('/api/search');
  if (!res.ok) throw new Error(`could not read the package (${res.status})`);
  state.search = (await res.json()).entries ?? [];
  return state.search;
}

/** The words worth matching on. Short ones and the obvious question words carry
 *  no signal and would match half the package. */
const STOP = new Set(['what', 'which', 'where', 'when', 'does', 'this', 'that', 'with',
  'from', 'into', 'have', 'has', 'the', 'and', 'for', 'are', 'how', 'why', 'who',
  'can', 'does', 'is', 'to', 'of', 'in', 'on', 'a', 'an', 'it', 'do', 'me']);

function terms(question) {
  return [...new Set(String(question).toLowerCase().match(/[a-z0-9_.]{3,}/g) ?? [])]
    .filter((w) => !STOP.has(w));
}

/**
 * The excerpts to send with a question.
 *
 * Scored rather than filtered: an entry matching three of the question's words
 * beats one matching one, which is the difference between the right table and
 * the first table alphabetically. Capped at a handful, because the service caps
 * the total anyway and a bigger pile is somebody's money.
 */
async function gather(question) {
  const words = terms(question);
  if (!words.length) return [];
  const entries = await index();
  const scored = [];
  for (const entry of entries) {
    const hay = `${entry.id} ${entry.name} ${entry.sub ?? ''} ${entry.terms ?? ''}`.toLowerCase();
    let score = 0;
    for (const word of words) if (hay.includes(word)) score += 1;
    // An exact id match is worth more than three loose word hits: somebody who
    // types POS-002 means that screen.
    if (words.includes(String(entry.id).toLowerCase())) score += 4;
    if (score) scored.push([score, entry]);
  }
  scored.sort((a, b) => b[0] - a[0]);

  const picked = scored.slice(0, 12).map(([, e]) => e);
  const bits = [];
  for (const entry of picked) {
    const lines = [
      `kind: ${entry.kind}`,
      `id: ${entry.id}`,
      entry.name && entry.name !== entry.id ? `name: ${entry.name}` : '',
      entry.sub ? `about: ${entry.sub}` : '',
      entry.file ? `file: ${entry.file}${entry.line ? `:${entry.line}` : ''}` : '',
      entry.terms ? `\n${entry.terms}` : '',
    ].filter(Boolean);
    bits.push({ title: `${entry.kind} ${entry.id}`, text: lines.join('\n') });
  }
  return bits;
}

// ── the conversation ─────────────────────────────────────────────────

function drawTurn(turn) {
  const box = el('div', `chat-turn chat-${turn.role}`);
  box.append(el('div', 'chat-who', turn.role === 'user' ? 'You' : (turn.label ?? 'ADAM')));
  box.append(el('div', 'chat-text', turn.text));
  if (turn.meta) box.append(el('div', 'chat-meta', turn.meta));

  // Offered on every answer rather than only when the model says the package is
  // wrong: whether something is a defect is the reader's call, and a button
  // that appeared only when the model volunteered it would be the model
  // deciding what counts as a problem.
  if (turn.role === 'assistant') {
    const bar = el('div', 'chat-actions');
    const raise = el('button', 'chip', 'Raise a change request from this');
    raise.type = 'button';
    raise.onclick = () => draft(turn);
    bar.append(raise);
    box.append(bar);
  }
  $('ch-log').append(box);
  box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  return box;
}

/**
 * Draft a change request from an answer, and show it before anything is filed.
 *
 * The same two-step the connector uses, and the same reason: a change request
 * is a claim that somebody else's work is wrong, and it goes out under the name
 * of whoever pressed the button.
 */
async function draft(turn) {
  say('ch-error', '');
  const asked = turn.about ?? '';
  try {
    const made = await auth.draftChange(auth.project(), {
      target_kind: 'other',
      target_id: 'from the chat',
      title: asked.slice(0, 120) || 'Raised from a question about the package',
      problem: `Asked: ${asked}\n\nADAM answered:\n\n${turn.text}`,
      evidence: (turn.excerpts ?? []).join(', '),
    });
    showDraft(made);
  } catch (error) {
    say('ch-error', error.message);
  }
}

function showDraft(made) {
  const box = el('div', 'chat-draft');
  box.append(el('div', 'chat-who', 'Nothing has been filed yet'));
  box.append(el('div', 'chat-text',
    'Check this, and change what it says before filing. It goes out under your name.'));

  const title = el('input', 'auth-input');
  title.value = made.preview.title ?? '';
  const problem = el('textarea', 'auth-input');
  problem.rows = 5;
  problem.value = made.preview.problem ?? '';
  box.append(el('div', 'auth-label', 'Title'), title,
    el('div', 'auth-label', 'What is wrong'), problem);

  if ((made.alreadyOpen ?? []).length) {
    box.append(el('p', 'chat-warn',
      `Already open on the same thing: ${made.alreadyOpen.map((c) => c.id).join(', ')}. `
      + 'Add to one of those instead if it says the same thing.'));
  }

  const bar = el('div', 'chat-actions');
  const file = el('button', 'chip cr-accept', 'File it');
  file.type = 'button';
  const drop = el('button', 'chip', 'Cancel');
  drop.type = 'button';
  drop.onclick = () => box.remove();
  const said = el('span', 'chat-meta');
  file.onclick = async () => {
    file.disabled = true;
    try {
      // Re-drafted when either field was touched, so what is filed is what the
      // person last read rather than what the first draft held.
      let code = made.draft;
      if (title.value !== made.preview.title || problem.value !== made.preview.problem) {
        const redone = await auth.draftChange(auth.project(), {
          ...made.preview, title: title.value, problem: problem.value,
        });
        code = redone.draft;
      }
      const filed = await auth.fileDraft(auth.project(), code);
      box.replaceChildren(el('div', 'chat-who', 'Filed'));
      const link = el('a', 'chat-link', `${filed.change.id} — ${filed.change.title}`);
      link.href = `/changes.html?project=${encodeURIComponent(auth.project() ?? '')}`;
      box.append(link);
    } catch (error) {
      said.textContent = error.message;
      file.disabled = false;
    }
  };
  bar.append(file, drop, said);
  box.append(bar);
  $('ch-log').append(box);
  box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}

async function ask(question) {
  const provider = state.provider;
  const model = $('ch-model').value.trim();
  if (!model) { say('ch-error', 'Choose or type a model.'); return; }
  remember(provider.id, model);

  state.turns.push({ role: 'user', text: question });
  drawTurn({ role: 'user', text: question });
  $('ch-says').textContent = 'Reading the package…';
  $('ch-send').disabled = true;

  try {
    const context = await gather(question);
    $('ch-says').textContent = `Asking ${model}…`;
    const said = await auth.askAdam({
      question, provider: provider.id, model, context,
      history: state.turns.slice(0, -1),
    });
    state.turns.push({ role: 'assistant', text: said.answer });
    drawTurn({
      role: 'assistant', text: said.answer, label: `${provider.label} · ${said.model}`,
      about: question,
      excerpts: context.map((c) => c.title),
      meta: `${said.excerpts} excerpt${said.excerpts === 1 ? '' : 's'} sent`
        + (said.droppedExcerpts ? `, ${said.droppedExcerpts} too long to send` : '')
        + ` · ${said.usage.in.toLocaleString()} in, ${said.usage.out.toLocaleString()} out`,
    });
    say('ch-error', '');
  } catch (error) {
    // The last turn goes back on the box rather than being lost, because the
    // usual reason to fail is a bad key or a quota and the question is still
    // the one they wanted to ask.
    state.turns.pop();
    $('ch-question').value = question;
    say('ch-error', error.message);
    if (error.status === 428) { await loadProviders(); }
  } finally {
    $('ch-says').textContent = '';
    $('ch-send').disabled = !state.provider?.configured;
  }
}

// ── loading ──────────────────────────────────────────────────────────

async function loadProviders() {
  const { providers } = await auth.chatProviders();
  state.providers = providers ?? [];
  const last = recall();
  state.provider =
    state.providers.find((p) => p.id === last.provider)
    ?? state.providers.find((p) => p.configured)
    ?? state.providers[0];
  drawPicker();
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';

  try { await loadProviders(); }
  catch (error) { say('ch-error', error.message); return; }

  $('ch-provider').onchange = (e) => {
    state.provider = state.providers.find((p) => p.id === e.target.value);
    drawProvider();
  };

  $('ch-keyform').onsubmit = async (event) => {
    event.preventDefault();
    $('ch-key-says').textContent = 'Checking…';
    try {
      const said = await auth.setLlmKey(state.provider.id, $('ch-key').value,
        $('ch-endpoint').value);
      $('ch-key').value = '';
      $('ch-key-says').textContent = `Saved — ${said.checked}.`;
      await loadProviders();
    } catch (error) {
      $('ch-key-says').textContent = error.message;
    }
  };

  $('ch-ask').onsubmit = (event) => {
    event.preventDefault();
    const question = $('ch-question').value.trim();
    if (!question) return;
    $('ch-question').value = '';
    ask(question);
  };

  // Enter sends, shift+Enter is a newline. A textarea that only sends on a
  // button is a textarea people stop using.
  $('ch-question').onkeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      $('ch-ask').requestSubmit();
    }
  };

  $('ch-clear').onclick = () => {
    state.turns = [];
    $('ch-log').replaceChildren();
    say('ch-error', '');
  };
})();
