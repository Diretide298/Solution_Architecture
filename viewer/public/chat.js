/**
 * Asking ADAM about the package, on whoever's key and whichever model.
 *
 * **The page gathers the context; the service holds the key.** ADAM's accounts
 * service cannot read a delivery package — that is the viewer's job — so this
 * searches the package for what the question is about, sends those excerpts
 * (the contract's own prose where there is some, not only names) with it, and
 * the service composes the call. Neither half has both, which is also why no
 * key is ever sent back to this page.
 *
 * **It opens on the question.** The box, then questions drawn from this
 * package, and one line saying which model will answer, with "Change" beside
 * it. Keys are a setup step and live in Settings, AI answers; this page only
 * says when one is missing and where to add it.
 *
 * **An answer says where it came from.** The parts of the package sent with a
 * question are listed under its answer as links into the viewer, so a reader
 * can check the answer against the package instead of trusting it.
 *
 * **One question at a time.** Enter used to send a second question while the
 * first was in flight, and a failed question was drawn again on every retry.
 * There is one busy flag now, and a failure takes its own turn back off the
 * page along with putting the words back in the box.
 *
 * What it will not do is file a change request by itself. When the answer says
 * the package is wrong, the page offers to draft one — through the same
 * draft-then-confirm flow the Claude connector uses, and with the same rule:
 * somebody reads it before it is filed.
 */

// The viewer's top bar on a page that is not the viewer, and the saved theme.
import '/page-chrome.js';
import * as auth from '/validation.js';
import {
  gather, starters, choose, remember, takeThread, renderAnswer, sourceList,
} from '/chat-core.js';
import { el, confirmStep } from '/sheet.js';

const $ = (id) => document.getElementById(id);

const state = {
  providers: [],
  provider: null,
  model: '',
  turns: [],          // { role, text } — what is sent back as history
  busy: false,
};

function fail(message) {
  $('ch-error').textContent = message ?? '';
  $('ch-error').hidden = !message;
}

// ── which model answers ──────────────────────────────────────────────

function drawModelLine() {
  const line = $('ch-model-line');
  const p = state.provider;
  line.replaceChildren();
  $('ch-change').hidden = !state.providers.some((x) => x.configured);
  if (!p || !p.configured) {
    // A setup step, not a failure, so it is said here rather than as an error.
    const go = el('a', 'sh-link', 'Settings, AI answers');
    go.href = '/settings.html#ai';
    line.append('No AI key yet. ADAM asks on your own key, never a shared one: add one in ', go,
      ', then come back.');
    $('ch-send').disabled = true;
    return;
  }
  line.append('Answering with ', el('strong', '', state.model || 'no model chosen'),
    ` from ${p.label}`, el('span', 'chat-model-hint', ` · key ${p.hint}`));
  $('ch-send').disabled = state.busy || !state.model;
}

function drawPicker() {
  const picker = $('ch-provider');
  // Only providers with a key: choosing one without a key here could only
  // fail, and adding a key is Settings' job.
  const usable = state.providers.filter((p) => p.configured);
  picker.replaceChildren(...usable.map((p) => new Option(p.label, p.id)));
  if (state.provider) picker.value = state.provider.id;
  const models = $('ch-models');
  models.replaceChildren(...(state.provider?.models ?? []).map((m) => new Option(m, m)));
  $('ch-model').value = state.model;
}

async function loadProviders() {
  const { providers } = await auth.chatProviders();
  state.providers = providers ?? [];
  const pick = choose(state.providers);
  state.provider = pick.provider;
  state.model = pick.model;
  drawPicker();
  drawModelLine();
}

// ── the conversation ─────────────────────────────────────────────────

function drawTurn(turn) {
  const box = el('article', `chat-turn chat-${turn.role}`);
  box.append(el('h2', 'chat-who', turn.role === 'user' ? 'You asked' : (turn.label ?? 'ADAM answered')));
  if (turn.role === 'assistant') box.append(renderAnswer(turn.text));
  else box.append(el('p', 'chat-text', turn.text));

  if (turn.role === 'assistant') {
    const sources = sourceList(turn.sources);
    if (sources) box.append(sources);
    if (turn.meta) box.append(el('p', 'chat-meta', turn.meta));
    // Offered on every answer rather than only when the model says the package
    // is wrong: whether something is a defect is the reader's call, and a
    // button that appeared only when the model volunteered it would be the
    // model deciding what counts as a problem.
    const bar = el('div', 'chat-actions');
    const raise = el('button', 'chip', 'Raise a change request from this');
    raise.type = 'button';
    raise.onclick = () => draft(turn, box, raise);
    bar.append(raise);
    box.append(bar);
  }
  $('ch-log').append(box);
  $('ch-clear').hidden = false;
  $('ch-starters').hidden = true;
  box.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  return box;
}

/** What a change request drafted from an answer is about: the first thing the
 *  answer was given, in the change register's own kinds. */
const CR_KIND = {
  operation: 'operation', schema: 'schema', contract: 'contract', table: 'table',
  screen: 'screen', flow: 'flow', state: 'state', event: 'event', adr: 'adr', platform: 'platform',
};

/**
 * Draft a change request from an answer, and show it before anything is filed.
 *
 * The same two-step the connector uses, and the same reason: a change request
 * is a claim that somebody else's work is wrong, and it goes out under the name
 * of whoever pressed the button.
 */
async function draft(turn, after, button) {
  fail('');
  button.disabled = true;
  const asked = turn.about ?? '';
  const first = (turn.sources ?? []).find((s) => CR_KIND[s.kind]);
  try {
    const made = await auth.draftChange(auth.project(), {
      // What it is about, when the answer was about something the register
      // knows; "other" with the question's own words when it was not. It used
      // to be the literal "from the chat", which named nothing.
      target_kind: first ? CR_KIND[first.kind] : 'other',
      target_id: first ? first.id : (asked.slice(0, 120) || 'the package'),
      title: asked.slice(0, 120) || 'Raised from a question about the package',
      problem: `Asked: ${asked}\n\nADAM answered:\n\n${turn.text}`,
      evidence: (turn.sources ?? []).map((s) => `${s.kind} ${s.id}${s.file ? ` (${s.file}${s.line ? `:${s.line}` : ''})` : ''}`).join(', '),
    });
    showDraft(made, after);
  } catch (error) {
    fail(`The change request could not be drafted: ${error.message}. Try again.`);
  } finally {
    button.disabled = false;
  }
}

let drafts = 0;
function showDraft(made, after) {
  drafts += 1;
  const id = `ch-draft-${drafts}`;
  const box = el('section', 'chat-draft');
  box.setAttribute('aria-labelledby', `${id}-head`);
  const head = el('h2', 'chat-who', 'A change request, not filed yet');
  head.id = `${id}-head`;
  box.append(head, el('p', 'chat-text',
    'Check it and change what it says before filing. It goes out under your name.'));

  const titleLabel = el('label', 'chat-field-label', 'Title');
  titleLabel.htmlFor = `${id}-title`;
  const title = el('input', 'sh-input');
  title.id = `${id}-title`;
  title.value = made.preview.title ?? '';
  const problemLabel = el('label', 'chat-field-label', 'What is wrong');
  problemLabel.htmlFor = `${id}-problem`;
  const problem = el('textarea', 'sh-input');
  problem.id = `${id}-problem`;
  problem.rows = 6;
  problem.value = made.preview.problem ?? '';
  box.append(titleLabel, title, problemLabel, problem);

  if ((made.alreadyOpen ?? []).length) {
    const warn = el('p', 'chat-warn', 'Already open on the same thing: ');
    made.alreadyOpen.forEach((c, i) => {
      const a = el('a', 'sh-link', c.id);
      a.href = `/changes.html?cr=${encodeURIComponent(c.id)}`;
      warn.append(i ? ', ' : '', a);
    });
    warn.append('. Add to one of those instead if it says the same thing.');
    box.append(warn);
  }

  const bar = el('div', 'chat-actions');
  const file = el('button', 'auth-button chat-file', 'File it');
  file.type = 'button';
  const drop = el('button', 'chip', 'Discard the draft');
  drop.type = 'button';
  drop.onclick = () => box.remove();
  const said = el('p', 'set-state');
  said.setAttribute('role', 'status');
  file.onclick = async () => {
    file.disabled = true;
    said.textContent = 'Filing…';
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
      box.replaceChildren(el('h2', 'chat-who', 'Filed'));
      // To the request itself, not to the bare list it would have to be found in.
      const link = el('a', 'sh-link', `${filed.change.id}: ${filed.change.title}`);
      link.href = `/changes.html?cr=${encodeURIComponent(filed.change.id)}`
        + `${auth.project() ? `&project=${encodeURIComponent(auth.project())}` : ''}`;
      box.append(el('p', 'chat-text', 'It is on Change requests: '), link);
      link.focus();
    } catch (error) {
      said.textContent = `It was not filed: ${error.message}. Change nothing and press File it again.`;
      file.disabled = false;
    }
  };
  bar.append(file, drop, said);
  box.append(bar);
  after.after(box);
  title.focus();
}

async function ask(question) {
  if (state.busy) return;
  const provider = state.provider;
  const model = state.model.trim();
  if (!provider?.configured) { fail('Add an AI key in Settings, AI answers, first.'); return; }
  if (!model) { fail('Choose a model first: press Change beside "Answering with".'); return; }
  remember(provider.id, model);

  state.busy = true;
  fail('');
  $('ch-send').disabled = true;
  $('ch-question').value = '';
  state.turns.push({ role: 'user', text: question });
  const mine = drawTurn({ role: 'user', text: question });
  $('ch-says').textContent = 'Reading the package…';

  try {
    const { context, sources } = await gather(question);
    $('ch-says').textContent = `Asking ${model}…`;
    const said = await auth.askAdam({
      question, provider: provider.id, model, context,
      history: state.turns.slice(0, -1),
    });
    const turn = {
      role: 'assistant', text: said.answer, label: `${provider.label}, ${said.model}, answered`,
      about: question, sources,
      meta: `${said.excerpts} part${said.excerpts === 1 ? '' : 's'} of the package sent`
        + (said.droppedExcerpts ? `, ${said.droppedExcerpts} left out as too long` : '')
        + ` · ${said.usage.in.toLocaleString()} tokens in, ${said.usage.out.toLocaleString()} out, on your key`,
    };
    state.turns.push({ role: 'assistant', text: said.answer });
    drawTurn(turn);
  } catch (error) {
    // The turn comes off the page as well as out of the history, and the words
    // go back in the box: the usual reason to fail is a key or a quota, and it
    // is still the question they wanted to ask. Leaving the drawn turn was how
    // a retry showed the same question twice.
    state.turns.pop();
    mine.remove();
    if (!state.turns.length) { $('ch-clear').hidden = true; $('ch-starters').hidden = false; }
    $('ch-question').value = question;
    fail(`That was not answered: ${error.message}`);
    if (error.status === 428) await loadProviders().catch(() => {});
  } finally {
    state.busy = false;
    $('ch-says').textContent = '';
    drawModelLine();
  }
}

// ── loading ──────────────────────────────────────────────────────────

async function drawStarters() {
  const list = $('ch-starter-list');
  let questions = [];
  try { questions = await starters(); } catch { /* the box works without them */ }
  list.replaceChildren(...questions.map((q) => {
    const b = el('button', 'chat-starter', q);
    b.type = 'button';
    b.onclick = () => { if (!state.busy && !$('ch-send').disabled) ask(q); else $('ch-question').value = q; };
    return b;
  }));
  $('ch-starters').hidden = !questions.length || state.turns.length > 0;
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';

  auth.ensureProject().then(async (id) => {
    let name = id ?? '';
    try { name = ((await auth.listProjects())?.projects ?? []).find((p) => p.id === id)?.name ?? name; } catch { /* the id will do */ }
    if (name) $('ch-project').textContent = name;
  });

  // A thread the side panel handed over with "Open the full chat".
  for (const turn of takeThread()) {
    state.turns.push({ role: turn.role, text: turn.text });
    drawTurn(turn);
  }
  drawStarters();

  try { await loadProviders(); } catch (error) {
    $('ch-model-line').textContent = '';
    fail(`ADAM could not say which AI providers you have a key for (${error.message}). Reload the page to try again.`);
  }

  $('ch-change').onclick = () => {
    const open = $('ch-picker').hidden;
    $('ch-picker').hidden = !open;
    $('ch-change').setAttribute('aria-expanded', String(open));
    $('ch-change').textContent = open ? 'Done' : 'Change';
    if (open) $('ch-provider').focus();
  };
  $('ch-provider').onchange = (e) => {
    const pick = choose(state.providers, { provider: e.target.value });
    state.provider = pick.provider;
    state.model = pick.model;
    drawPicker();
    drawModelLine();
  };
  $('ch-model').oninput = (e) => {
    state.model = e.target.value.trim();
    if (state.model) remember(state.provider.id, state.model);
    drawModelLine();
  };

  $('ch-ask').onsubmit = (event) => {
    event.preventDefault();
    const question = $('ch-question').value.trim();
    if (question) ask(question);
  };

  // Enter sends, Shift+Enter is a newline. A textarea that only sends on a
  // button is a textarea people stop using. Ignored while a question is in
  // flight, which is the busy guard's other half.
  $('ch-question').onkeydown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      if (!state.busy) $('ch-ask').requestSubmit();
    }
  };

  // The conversation is not kept anywhere, so clearing it cannot be undone.
  $('ch-clear').onclick = async () => {
    const sure = await confirmStep($('ch-clear').parentElement, {
      say: 'This clears the conversation from the page. It is not kept anywhere, so it cannot be brought back.',
      action: 'Clear the conversation',
    });
    if (!sure) return;
    state.turns = [];
    $('ch-log').replaceChildren();
    $('ch-clear').hidden = true;
    $('ch-starters').hidden = !$('ch-starter-list').childElementCount;
    fail('');
    $('ch-question').focus();
  };
})();
