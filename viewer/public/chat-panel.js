/**
 * The chat panel the mascot opens.
 *
 * **A panel, not a page.** Clicking him used to navigate to `/chat.html`, which
 * answers the question and loses where you were: you came to ask about the thing
 * on screen, and asking took the thing off screen. This opens over the viewer
 * and closes again, and the full page is one button away for a long
 * conversation.
 *
 * It asks the same way the page does — `gather()` from `chat-core.js` — so the
 * two cannot drift into giving different answers to the same words.
 *
 * **It does not hold a key form.** Setting a provider key is a setup step with
 * its own checks and its own copy about whose bill the questions are on; a
 * second copy of it in a 380px panel is a second thing to keep right. With no
 * key, the panel says so and sends you to the page that does it.
 */

import * as auth from '/validation.js';
import { gather } from '/chat-core.js';

const MODEL_KEY = 'adam-chat-model';

const SUGGESTIONS = [
  'Which operations write to orders.sales_order?',
  'What does the guest app do offline?',
  'Which services own the payments tables?',
];

const HTML = `
<div class="cp-rim" id="cp-panel" hidden>
  <div class="cp-body">
    <header class="cp-head">
      <span class="cp-title">Ask about the package</span>
      <a class="cp-icon" id="cp-full" href="/chat.html" title="Open the full chat"
         aria-label="Open the full chat">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M9.5 2.5h4v4M13.5 2.5 9 7M6.5 13.5h-4v-4M2.5 13.5 7 9" /></svg>
      </a>
      <button class="cp-icon" id="cp-close" type="button" title="Close" aria-label="Close">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8" /></svg>
      </button>
    </header>

    <div class="cp-log" id="cp-log"></div>

    <p class="cp-note" id="cp-note" hidden></p>

    <div class="cp-foot">
      <label class="cp-model">
        <span>Model</span>
        <input id="cp-model" type="text" spellcheck="false" placeholder="claude-opus-5" />
      </label>
      <div class="cp-rim cp-askrim">
        <div class="cp-ask">
          <input id="cp-q" type="text" placeholder="Ask about the package…"
                 aria-label="Ask about the package" />
          <button id="cp-send" type="button" aria-label="Ask">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"
                 stroke-linecap="round" stroke-linejoin="round">
              <path d="M8 13V3M3.5 7.5 8 3l4.5 4.5" /></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</div>`;

const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};

const state = { provider: null, turns: [], busy: false, built: false };

function say(text, bad = false) {
  const note = $('cp-note');
  note.textContent = text ?? '';
  note.hidden = !text;
  note.dataset.bad = bad ? '1' : '';
}

function drawEmpty() {
  const log = $('cp-log');
  log.replaceChildren();
  const intro = el('p', 'cp-empty',
    'Answers come from this package and nothing else. If the package looks wrong, '
    + 'say so on the full page and it becomes a change request.');
  log.append(intro);
  SUGGESTIONS.forEach((q, i) => {
    const b = el('button', 'cp-suggest');
    b.type = 'button';
    b.append(el('span', 'cp-n', String(i + 1)), el('span', null, q));
    b.onclick = () => { $('cp-q').value = q; ask(); };
    log.append(b);
  });
}

function drawTurn({ role, text, label, sources }) {
  const log = $('cp-log');
  const wrap = el('div', `cp-turn cp-${role}`);
  if (label) wrap.append(el('div', 'cp-label', label));
  wrap.append(el('div', 'cp-bubble', text));
  if (sources?.length) {
    const chips = el('div', 'cp-chips');
    // Capped, because twelve excerpts is a wall of chips and the point is to
    // show what it read, not to list it.
    for (const s of sources.slice(0, 6)) chips.append(el('span', 'cp-chip', s));
    if (sources.length > 6) chips.append(el('span', 'cp-chip', `+${sources.length - 6}`));
    wrap.append(chips);
  }
  log.append(wrap);
  log.scrollTop = log.scrollHeight;
}

async function loadProviders() {
  const answer = await auth.chatProviders();
  const providers = answer?.providers ?? [];
  state.provider = providers.find((p) => p.configured) ?? providers[0] ?? null;
  if (!state.provider) {
    say('No provider is available on this ADAM.');
    return;
  }
  if (!state.provider.configured) {
    // The panel is deliberately not a setup screen; see the header comment.
    say(`${state.provider.label} needs a key. Open the full chat to add one.`);
    $('cp-send').disabled = true;
    return;
  }
  say('');
  $('cp-send').disabled = false;
  let remembered = '';
  try { remembered = localStorage.getItem(`${MODEL_KEY}:${state.provider.id}`) ?? ''; } catch { /* fine */ }
  $('cp-model').value = remembered || state.provider.suggested || '';
}

async function ask() {
  if (state.busy) return;
  const question = $('cp-q').value.trim();
  if (!question) return;
  const model = $('cp-model').value.trim();
  if (!model) { say('Type a model first.', true); return; }
  if (!state.provider?.configured) return;

  state.busy = true;
  $('cp-send').disabled = true;
  $('cp-q').value = '';
  if (!state.turns.length) $('cp-log').replaceChildren();
  state.turns.push({ role: 'user', text: question });
  drawTurn({ role: 'user', text: question });
  say('Reading the package…');

  try {
    const context = await gather(question);
    say(`Asking ${model}…`);
    const said = await auth.askAdam({
      question,
      provider: state.provider.id,
      model,
      context,
      history: state.turns.slice(0, -1),
    });
    state.turns.push({ role: 'assistant', text: said.answer });
    drawTurn({
      role: 'assistant',
      text: said.answer,
      label: `${state.provider.label} · ${said.model}`,
      sources: context.map((c) => c.title),
    });
    try { localStorage.setItem(`${MODEL_KEY}:${state.provider.id}`, model); } catch { /* fine */ }
    say('');
  } catch (error) {
    // The question goes back in the box rather than being lost: the usual causes
    // are a bad key or a quota, and it is still the question they wanted to ask.
    state.turns.pop();
    $('cp-q').value = question;
    say(error.message, true);
    if (error.status === 428) await loadProviders().catch(() => {});
  } finally {
    state.busy = false;
    $('cp-send').disabled = !state.provider?.configured;
  }
}

function build() {
  if (state.built) return;
  document.body.insertAdjacentHTML('beforeend', HTML);
  state.built = true;

  $('cp-close').onclick = () => closeChatPanel();
  $('cp-send').onclick = ask;
  $('cp-q').addEventListener('keydown', (e) => { if (e.key === 'Enter') ask(); });
  // Escape closes it, because a panel over the page that only closes by mouse is
  // a panel somebody has to go and find the corner of.
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !$('cp-panel').hidden) closeChatPanel();
  });
  drawEmpty();
  loadProviders().catch((error) => say(error.message, true));
}

export function openChatPanel() {
  build();
  $('cp-panel').hidden = false;
  document.body.dataset.chatPanel = 'open';
  $('cp-q').focus();
}

export function closeChatPanel() {
  if (!state.built) return;
  $('cp-panel').hidden = true;
  delete document.body.dataset.chatPanel;
}

export function toggleChatPanel() {
  if (state.built && !$('cp-panel').hidden) closeChatPanel();
  else openChatPanel();
}
