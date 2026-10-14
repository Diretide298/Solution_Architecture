/**
 * The sheet's behaviour: the parts of the Tasks page other pages are built
 * from. Read `sheet.css` first; this is the half of it that needs code.
 *
 * **What a page gets.**
 *   el(tag, className, text)        the one element helper
 *   verdict(root, {...})             the opening: when, headline, pill, pace,
 *                                    ledger, saying, next
 *   mountScope({...})                one filter for the whole page, kept in the
 *                                    address, with a sentence saying what it
 *                                    shows and "Show everything"
 *   legend(items)                    a key, every swatch with its word
 *   table({...})                     a real <table>, sortable, which is also
 *                                    every chart's twin
 *   personLink(name)                 a name that leads to that person's page
 *                                    on Tasks
 *   badge(kind, text), confirmStep() the state word, and the second press a
 *                                    destructive action needs
 *   param / setParams                the address as the page's state
 *
 * **Why the address holds the state.** A link somebody sends has to open on
 * what they were looking at. Tasks learned this with `?person=`; every page
 * that filters does the same now, with `replaceState`, so a change of filter
 * is not a step the back button has to walk.
 */

export const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined && text !== null) node.textContent = String(text);
  return node;
};

export const fmt = (n) => (Number.isFinite(n) ? n.toLocaleString('en-IN') : '—');
export const plural = (n, one, many = `${one}s`) => `${fmt(n)} ${n === 1 ? one : many}`;

/** Whole days between an ISO time and now, never negative. */
export const daysSince = (iso) => {
  const t = Date.parse(iso ?? '');
  if (!Number.isFinite(t)) return null;
  return Math.max(0, Math.floor((Date.now() - t) / 86_400_000));
};

/** "today", "yesterday", "3 days ago", or the date past a fortnight. */
export const ago = (iso) => {
  const d = daysSince(iso);
  if (d === null) return '';
  if (d === 0) return 'today';
  if (d === 1) return 'yesterday';
  if (d < 15) return `${d} days ago`;
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
};

// ── the address ─────────────────────────────────────────────────────
export const param = (name) => new URLSearchParams(location.search).get(name) ?? '';

/** Set or clear query parameters, keeping the hash. Empty values are removed. */
export function setParams(values) {
  const params = new URLSearchParams(location.search);
  for (const [key, value] of Object.entries(values)) {
    if (value === '' || value === null || value === undefined || value === false) params.delete(key);
    else params.set(key, String(value));
  }
  const query = params.toString();
  history.replaceState(null, '', `${location.pathname}${query ? `?${query}` : ''}${location.hash}`);
}

// ── people ──────────────────────────────────────────────────────────
/** The page on Tasks that is everything about one person. */
export const personHref = (name) => `/tasks.html?person=${encodeURIComponent(name)}#person`;

export function personLink(name, className = 'sh-link') {
  if (!name) return el('span', 'sh-quiet', 'nobody');
  const a = el('a', className, name);
  a.href = personHref(name);
  a.title = `Everything about ${name}, on Tasks`;
  return a;
}

// ── the verdict ─────────────────────────────────────────────────────
/**
 * Fill a `.sh-verdict` with the page's opening. Every field is optional; an
 * absent one draws nothing rather than an empty box.
 *
 * @param {Element} root
 * @param {object} v
 * @param {string|Node} [v.when]      the line above: what is being read
 * @param {string|Node} v.headline     one sentence, the answer
 * @param {{tone:'ok'|'warn'|'bad', text:string, glyph?:string}} [v.pill]
 * @param {string|Node} [v.pace]       the sentence under it
 * @param {Array<{label:string, value:any, unit?:string, swatch?:string, bad?:boolean, title?:string}>} [v.ledger]
 * @param {string|Node} [v.saying]     a quieter line under the figures
 */
export function verdict(root, v) {
  root.replaceChildren();
  if (v.when) root.append(fill(el('p', 'sh-when'), v.when));
  const h = el('h2', 'sh-headline');
  if (v.headlineId) h.id = v.headlineId;
  h.append(fill(el('span'), v.headline ?? ''));
  if (v.pill) {
    const pill = el('span', `sh-pill is-${v.pill.tone}`);
    const glyph = el('span', 'sh-pill-glyph', v.pill.glyph ?? { ok: '✓', warn: '!', bad: '!' }[v.pill.tone] ?? '·');
    glyph.setAttribute('aria-hidden', 'true');
    pill.append(glyph, v.pill.text);
    h.append(pill);
  }
  root.append(h);
  if (v.pace) root.append(fill(el('p', 'sh-pace'), v.pace));
  if (v.ledger?.length) {
    const dl = el('dl', 'sh-ledger');
    for (const item of v.ledger) {
      const box = el('div', `sh-ledger-item${item.bad ? ' is-bad' : ''}`);
      if (item.title) box.title = item.title;
      const dt = el('dt');
      if (item.swatch) {
        const sw = el('span', `sh-swatch sh-fill-${item.swatch}`);
        sw.setAttribute('aria-hidden', 'true');
        dt.append(sw);
      }
      dt.append(item.label);
      const dd = el('dd');
      dd.append(typeof item.value === 'number' ? fmt(item.value) : (item.value ?? '—'));
      if (item.unit) dd.append(el('small', '', item.unit));
      box.append(dt, dd);
      dl.append(box);
    }
    root.append(dl);
  }
  if (v.saying) root.append(fill(el('p', 'sh-saying'), v.saying));
}

/** The "next" line under a sheet's opening: one thing to do, named. */
export function next(root, content) {
  root.replaceChildren();
  if (!content) return;
  root.append(el('span', 'sh-next-label', 'Next'));
  fill(root, content, true);
}

function fill(node, content, append = false) {
  if (!append) node.replaceChildren();
  if (content instanceof Node) node.append(content);
  else if (Array.isArray(content)) node.append(...content);
  else node.append(String(content));
  return node;
}

// ── the page's filter ───────────────────────────────────────────────
/**
 * One filter for the whole page, kept in the address.
 *
 * @param {object} o
 * @param {Element} o.root         the `.sh-scope` element to draw into
 * @param {Array<{key:string, label:string, options:Array<[string,string]>|(() => Array<[string,string]>), all?:string, kind?:'select'|'switch'|'search'|'check'}>} o.fields
 *        options are [value, label]; the first is the default unless `all`
 *        names an "everything" choice, which is then value ''.
 * @param {(state:object) => string} o.says   the sentence for the current filter
 * @param {(state:object) => void} o.onChange
 * @returns {{state:object, redraw:() => void, set:(patch:object) => void}}
 */
export function mountScope({ root, fields, says, onChange }) {
  const state = {};
  for (const f of fields) {
    const fromUrl = param(f.key);
    state[f.key] = f.kind === 'check' ? fromUrl === '1' : fromUrl;
  }
  const saysLine = el('p', 'sh-says');
  saysLine.setAttribute('aria-live', 'polite');
  const clear = el('button', 'chip sh-clear', 'Show everything');
  clear.type = 'button';

  const controls = new Map();
  const draw = () => {
    root.replaceChildren();
    for (const f of fields) {
      const options = typeof f.options === 'function' ? f.options() : (f.options ?? []);
      if (f.kind === 'switch') {
        const wrap = el('div', 'sh-field');
        const label = el('span', '', f.label);
        label.id = `sh-${f.key}-label`;
        const group = el('div', 'sh-switch');
        group.setAttribute('role', 'group');
        group.setAttribute('aria-labelledby', label.id);
        const current = state[f.key] || options[0]?.[0] || '';
        for (const [value, text] of options) {
          const b = el('button', '', text);
          b.type = 'button';
          b.setAttribute('aria-pressed', String(value === current));
          b.onclick = () => change(f.key, value === options[0][0] ? '' : value);
          group.append(b);
        }
        wrap.append(label, group);
        root.append(wrap);
        controls.set(f.key, group);
      } else if (f.kind === 'search') {
        const label = el('label', 'sh-field');
        const input = el('input', 'sh-input');
        input.type = 'search';
        input.value = state[f.key];
        input.placeholder = f.placeholder ?? '';
        let t;
        input.oninput = () => { clearTimeout(t); t = setTimeout(() => change(f.key, input.value.trim(), true), 180); };
        label.append(el('span', '', f.label), input);
        root.append(label);
        controls.set(f.key, input);
      } else if (f.kind === 'check') {
        const label = el('label', 'sh-field-inline');
        const input = el('input');
        input.type = 'checkbox';
        input.checked = !!state[f.key];
        input.onchange = () => change(f.key, input.checked);
        label.append(input, f.label);
        root.append(label);
        controls.set(f.key, input);
      } else {
        const label = el('label', 'sh-field');
        const select = el('select', 'scope-select');
        if (f.all !== undefined) select.append(new Option(f.all, ''));
        for (const [value, text] of options) select.append(new Option(text, value));
        select.value = state[f.key];
        if (select.value !== state[f.key]) { state[f.key] = ''; select.value = ''; }
        select.onchange = () => change(f.key, select.value);
        label.append(el('span', '', f.label), select);
        root.append(label);
        controls.set(f.key, select);
      }
    }
    root.append(clear, saysLine);
    const any = fields.some((f) => !!state[f.key] && !f.sticky);
    clear.hidden = !any;
    saysLine.textContent = says ? says(state) : '';
  };

  const change = (key, value, keepFocus = false) => {
    state[key] = value;
    setParams({ [key]: value === true ? '1' : value });
    if (keepFocus) {
      // Redrawing would take the caret away from somebody typing.
      const any = fields.some((f) => !!state[f.key] && !f.sticky);
      clear.hidden = !any;
      saysLine.textContent = says ? says(state) : '';
    } else draw();
    onChange?.(state);
  };

  clear.onclick = () => {
    const patch = {};
    for (const f of fields) if (!f.sticky) { state[f.key] = f.kind === 'check' ? false : ''; patch[f.key] = ''; }
    setParams(patch);
    draw();
    onChange?.(state);
  };

  draw();
  return {
    state,
    redraw: draw,
    set(patch) {
      Object.assign(state, patch);
      setParams(Object.fromEntries(Object.entries(patch).map(([k, v]) => [k, v === true ? '1' : v])));
      draw();
      onChange?.(state);
    },
  };
}

// ── keys and states ─────────────────────────────────────────────────
/** @param {Array<{kind:string, label:string, value?:any}>} items */
export function legend(items, className = '') {
  const ul = el('ul', `sh-legend ${className}`.trim());
  for (const item of items) {
    const li = el('li', 'sh-legend-item');
    const sw = el('span', `sh-swatch sh-fill-${item.kind}`);
    sw.setAttribute('aria-hidden', 'true');
    li.append(sw, item.label);
    if (item.value !== undefined) li.append(el('span', 'sh-legend-value', typeof item.value === 'number' ? fmt(item.value) : item.value));
    ul.append(li);
  }
  return ul;
}

export const badge = (kind, text) => el('span', `sh-badge sh-badge-${kind}`, text);

/** A stacked bar; parts are {kind, value, label}. Title carries the words. */
export function stack(parts, hero = false) {
  const total = parts.reduce((s, p) => s + (p.value || 0), 0);
  const bar = el('span', `sh-stack${hero ? ' is-hero' : ''}`);
  bar.setAttribute('role', 'img');
  bar.setAttribute('aria-label', parts.filter((p) => p.value).map((p) => `${p.label} ${fmt(p.value)}`).join(', ') || 'nothing');
  for (const p of parts) {
    if (!p.value) continue;
    const seg = el('span', `sh-fill-${p.kind}`);
    seg.style.flex = `${p.value} 1 0`;
    seg.title = `${p.label}: ${fmt(p.value)}${total ? ` of ${fmt(total)}` : ''}`;
    bar.append(seg);
  }
  return bar;
}

// ── tables ──────────────────────────────────────────────────────────
/**
 * A real table. Columns: {key, label, num?, render?(row) => Node|string,
 * sort?(row) => comparable, nowrap?}. Sorting is by header button, with
 * aria-sort, and is the reader's, not kept in the address.
 *
 * @returns {HTMLElement} the wrapper; `.redraw(rows)` replaces the rows.
 */
export function table({ caption, columns, rows, empty = 'Nothing here.', srOnly = false, rowClass, sortBy }) {
  const wrap = el('div', srOnly ? 'sh-sr' : 'sh-table-wrap');
  const t = el('table', 'sh-table');
  if (caption) t.append(el('caption', '', caption));
  const thead = el('thead');
  const hr = el('tr');
  let sort = sortBy ?? null;
  const ths = columns.map((c) => {
    const th = el('th', c.num ? 'is-num' : '');
    th.scope = 'col';
    if (c.sort && !srOnly) {
      const b = el('button', 'sh-sort', c.label);
      b.type = 'button';
      b.onclick = () => {
        sort = sort?.key === c.key ? { key: c.key, dir: -sort.dir } : { key: c.key, dir: c.num ? -1 : 1 };
        body(current);
      };
      th.append(b);
    } else th.textContent = c.label;
    hr.append(th);
    return th;
  });
  thead.append(hr);
  const tbody = el('tbody');
  t.append(thead, tbody);
  wrap.append(t);

  let current = rows ?? [];
  const body = (list) => {
    current = list;
    let sorted = list;
    if (sort) {
      const col = columns.find((c) => c.key === sort.key);
      if (col?.sort) {
        sorted = [...list].sort((a, b) => {
          const x = col.sort(a), y = col.sort(b);
          return (x > y ? 1 : x < y ? -1 : 0) * sort.dir;
        });
      }
    }
    columns.forEach((c, i) => {
      if (sort?.key === c.key) ths[i].setAttribute('aria-sort', sort.dir > 0 ? 'ascending' : 'descending');
      else ths[i].removeAttribute('aria-sort');
    });
    tbody.replaceChildren();
    if (!sorted.length) {
      const tr = el('tr');
      const td = el('td', 'sh-empty', empty);
      td.colSpan = columns.length;
      tr.append(td);
      tbody.append(tr);
      return;
    }
    for (const row of sorted) {
      const tr = el('tr', rowClass ? rowClass(row) : '');
      columns.forEach((c, i) => {
        const cell = el(i === 0 ? 'th' : 'td', [c.num ? 'is-num' : '', c.nowrap ? 'is-nowrap' : '', c.cellClass ? c.cellClass(row) : ''].filter(Boolean).join(' '));
        if (i === 0) cell.scope = 'row';
        const v = c.render ? c.render(row) : row[c.key];
        if (v instanceof Node) cell.append(v);
        else cell.textContent = typeof v === 'number' ? fmt(v) : (v ?? '');
        tr.append(cell);
      });
      tbody.append(tr);
    }
  };
  body(current);
  wrap.redraw = body;
  return wrap;
}

// ── a second press ──────────────────────────────────────────────────
/**
 * Put a confirm strip after `anchor`: the sentence says what will happen and
 * the button says the action again. Resolves true on confirm, false on cancel.
 * Used for anything that cannot be undone from the same screen.
 */
export function confirmStep(anchor, { say, action, cancel = 'Cancel' }) {
  anchor.parentElement?.querySelector(':scope > .sh-confirm')?.remove();
  return new Promise((resolve) => {
    const box = el('div', 'sh-confirm');
    box.setAttribute('role', 'alertdialog');
    box.setAttribute('aria-label', action);
    const p = el('span', '', say);
    const yes = el('button', 'chip', action);
    yes.type = 'button';
    const no = el('button', 'chip', cancel);
    no.type = 'button';
    const done = (answer) => { box.remove(); anchor.focus?.(); resolve(answer); };
    yes.onclick = () => done(true);
    no.onclick = () => done(false);
    box.addEventListener('keydown', (e) => { if (e.key === 'Escape') done(false); });
    box.append(p, yes, no);
    anchor.insertAdjacentElement('afterend', box);
    no.focus();
  });
}
