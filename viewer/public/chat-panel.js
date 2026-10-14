/**
 * The chat panel the mascot opens.
 *
 * **A panel, not a page.** Clicking him used to navigate to `/chat.html`, which
 * answers the question and loses where you were: you came to ask about the thing
 * on screen, and asking took the thing off screen. This opens over the viewer
 * and closes again, and the full page is one button away for a long
 * conversation; that button carries the conversation with it.
 *
 * **One state with the page.** Which provider and model to ask, what to send
 * with a question, the questions to start from, how an answer is drawn and how
 * its sources link back: all from `chat-core.js`, so the panel cannot drift into
 * asking a different model, or answering differently, from the page. It used
 * to read a `suggested` model the service never sent, so the first question
 * stopped at "Type a model first"; the service sends one now, and the shared
 * choice falls back to the provider's own list besides.
 *
 * **It does not hold a key form.** Setting a provider key is a setup step with
 * its own checks and its own copy about whose bill the questions are on, and it
 * lives in Settings, AI answers. With no key, the panel says so and links there.
 *
 * **A dialog, and it gives focus back.** It is announced as one, takes focus
 * into its question box when it opens and returns it to whatever opened it when
 * it closes, so a keyboard reader is not left at the top of the page.
 */

import * as auth from '/validation.js';
import {
  gather, starters, choose, remember, handThread, renderAnswer, sourceList,
} from '/chat-core.js';

const HTML = `
<div class="cp-rim" id="cp-panel" role="dialog" aria-modal="false" aria-labelledby="cp-title" hidden>
  <div class="cp-body">
    <header class="cp-head">
      <h2 class="cp-title" id="cp-title">Ask about the package</h2>
      <a class="cp-icon" id="cp-full" href="/chat.html" title="Open the full chat, with this conversation"
         aria-label="Open the full chat, with this conversation">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
             stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M9.5 2.5h4v4M13.5 2.5 9 7M6.5 13.5h-4v-4M2.5 13.5 7 9" /></svg>
      </a>
      <button class="cp-icon" id="cp-close" type="button" title="Close" aria-label="Close">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"
             stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" /></svg>
      </button>
    </header>

    <div class="cp-log" id="cp-log" role="log" aria-live="polite" aria-label="The conversation"></div>

    <p class="cp-note" id="cp-note" role="status" hidden></p>

    <div class="cp-foot">
      <label class="cp-model" for="cp-model">
        <span>Model</span>
        <input id="cp-model" type="text" spellcheck="false" autocomplete="off" list="cp-models" />
        <datalist id="cp-models"></datalist>
      </label>
      <div class="cp-rim cp-askrim">
        <div class="cp-ask">
          <label class="cp-sr" for="cp-q">Your question</label>
          <input id="cp-q" type="text" placeholder="Ask about the package" />
          <button id="cp-send" type="button" aria-label="Ask">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"
                 stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
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

const state = {
  providers: [], provider: null,
  turns: [],          // whole turns, so the page can draw them again
  busy: false, built: false, opener: null,
};

function say(content, bad = false) {
  const note = $('cp-note');
  note.replaceChildren();
  if (content instanceof Node) note.append(content);
  else note.textContent = content ?? '';
  note.hidden = !content;
  note.dataset.bad = bad ? '1' : '';
}

async function drawEmpty() {
  const log = $('cp-log');
  log.replaceChildren(el('p', 'cp-empty',
    'Answers come from this package and nothing else, with the parts they were read from listed '
    + 'under each. If the package looks wrong, open the full chat and raise a change request from the answer.'));
  let questions = [];
  try { questions = await starters(); } catch { /* the box works without them */ }
  if (state.turns.length) return;
  questions.forEach((q, i) => {
    const b = el('button', 'cp-suggest');
    b.type = 'button';
    b.append(el('span', 'cp-n', String(i + 1)), el('span', null, q));
    b.onclick = () => { $('cp-q').value = q; ask(); };
    log.append(b);
  });
}

function drawTurn(turn) {
  const log = $('cp-log');
  const wrap = el('div', `cp-turn cp-${turn.role}`);
  if (turn.label) wrap.append(el('div', 'cp-label', turn.label));
  const bubble = el('div', 'cp-bubble');
  if (turn.role === 'assistant') bubble.append(renderAnswer(turn.text));
  else bubble.textContent = turn.text;
  wrap.append(bubble);
  // Capped, because twelve sources in a 380px panel is a wall; the full chat
  // lists them all.
  const sources = turn.role === 'assistant' ? sourceList(turn.sources, { max: 4 }) : null;
  if (sources) wrap.append(sources);
  log.append(wrap);
  log.scrollTop = log.scrollHeight;
  return wrap;
}

async function loadProviders() {
  const answer = await auth.chatProviders();
  state.providers = answer?.providers ?? [];
  // The same choice the page makes, from the same remembered pick, so a model
  // chosen on the page is the one the panel asks.
  const pick = choose(state.providers);
  state.provider = pick.provider;
  if (!state.provider) {
    say('No AI provider is available on this ADAM.', true);
    $('cp-send').disabled = true;
    return;
  }
  if (!state.provider.configured) {
    const go = el('a', 'cp-link', 'Settings, AI answers');
    go.href = '/settings.html#ai';
    const line = el('span', null, 'No AI key yet. Add one in ');
    line.append(go, ', then ask here.');
    say(line);
    $('cp-send').disabled = true;
    return;
  }
  say('');
  $('cp-send').disabled = false;
  $('cp-models').replaceChildren(...(state.provider.models ?? []).map((m) => new Option(m, m)));
  $('cp-model').value = pick.model;
}

async function ask() {
  if (state.busy) return;
  const question = $('cp-q').value.trim();
  if (!question) return;
  const model = $('cp-model').value.trim();
  if (!state.provider?.configured) return;
  if (!model) { say('Choose a model in the Model box first.', true); $('cp-model').focus(); return; }

  state.busy = true;
  $('cp-send').disabled = true;
  $('cp-q').value = '';
  if (!state.turns.length) $('cp-log').replaceChildren();
  const asked = { role: 'user', text: question };
  state.turns.push(asked);
  const mine = drawTurn(asked);
  say('Reading the package…');

  try {
    const { context, sources } = await gather(question);
    say(`Asking ${model}…`);
    const said = await auth.askAdam({
      question,
      provider: state.provider.id,
      model,
      context,
      history: state.turns.slice(0, -1),
    });
    const turn = {
      role: 'assistant', text: said.answer, about: question, sources,
      label: `${state.provider.label}, ${said.model}, answered`,
    };
    state.turns.push(turn);
    drawTurn(turn);
    remember(state.provider.id, model);
    say('');
  } catch (error) {
    // The question comes off the page and goes back in the box: the usual
    // causes are a key or a quota, and it is still the question they wanted.
    state.turns.pop();
    mine.remove();
    if (!state.turns.length) drawEmpty();
    $('cp-q').value = question;
    say(`That was not answered: ${error.message}`, true);
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
  $('cp-q').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); ask(); }
  });
  $('cp-model').addEventListener('change', () => {
    const model = $('cp-model').value.trim();
    if (model && state.provider) remember(state.provider.id, model);
  });
  // The conversation goes with the reader to the full page, so "open the full
  // chat" continues it rather than starting again.
  $('cp-full').addEventListener('click', () => handThread(state.turns));
  // Escape closes it, because a panel over the page that only closes by mouse
  // is a panel somebody has to go and find the corner of.
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !$('cp-panel').hidden) closeChatPanel();
  });
  drawEmpty();
  loadProviders().catch((error) => say(`ADAM could not say which AI keys you have: ${error.message}`, true));
}

export function openChatPanel() {
  state.opener = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  build();
  $('cp-panel').hidden = false;
  document.body.dataset.chatPanel = 'open';
  $('cp-q').focus();
}

export function closeChatPanel() {
  if (!state.built) return;
  $('cp-panel').hidden = true;
  delete document.body.dataset.chatPanel;
  // Back to what opened it, so the keyboard picks up where it left off.
  if (state.opener?.isConnected) state.opener.focus();
  state.opener = null;
}

export function toggleChatPanel() {
  if (state.built && !$('cp-panel').hidden) closeChatPanel();
  else openChatPanel();
}
