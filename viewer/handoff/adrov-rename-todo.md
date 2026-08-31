# Adrov: what the rename could not do from here

The product is Adrov. The viewer says so everywhere a reader can see it — titles,
alt text, the sign-in copy, the loading curtain, the brand files. Four kinds of
"aster" were left alone on purpose, and three of them need a decision from you
rather than an edit from anyone.

---

## 1 · The hostnames, and the certificates behind them

These are live DNS names with Let's Encrypt certificates issued against them.
Editing a file does not move a record or reissue a certificate; it only makes
the file disagree with the server.

```
aster.ainfinite.ai      →  :4173   the package, and the gate
asterapi.ainfinite.ai   →  :8787   accounts, invites, verdicts, /docs
```

They are still spelled `aster` in:

| where | what it is |
| --- | --- |
| `deploy/nginx/aster.ainfinite.ai` | filename **and** `server_name`, `ssl_certificate` paths |
| `deploy/nginx/asterapi.ainfinite.ai` | the same, for the API |
| `deploy/deploy.sh` | `PUBLIC_ORIGIN` default, and the `NGINX_SITE` path it greps |
| `deploy/README.md`, `HANDOFF.md` | the install instructions, which must match the filenames |
| `api/main.py` | CORS allow-list |
| `server.mjs` | `ALLOWED_ORIGINS` |
| `public/validation.js` | `API_DEPLOYED`, the deployed accounts-service base |

Two of those are lists, so both spellings are named in them already —
`https://adrov.ainfinite.ai` sits beside `https://aster.ainfinite.ai` in
`api/main.py` and `server.mjs`. An origin that does not resolve is inert, so
this costs nothing now and means the front end works the moment the name does.

`API_DEPLOYED` in `public/validation.js` is a single value, not a list, and
deliberately so — the comment above it explains why an address that can be
argued out of being itself goes wrong quietly. It has to be changed in one
commit, at the same time as the DNS.

**To finish the move, in this order:**

1. Add `A` records for `adrov.ainfinite.ai` and `adrovapi.ainfinite.ai`.
2. `certbot --nginx -d adrov.ainfinite.ai -d adrovapi.ainfinite.ai`.
3. Copy `deploy/nginx/aster.ainfinite.ai` → `deploy/nginx/adrov.ainfinite.ai`
   and the same for the API block; put both names in `server_name` while the
   alias lasts, so nothing in flight breaks.
4. Change `PUBLIC_ORIGIN` and `NGINX_SITE` in `deploy/deploy.sh`, and
   `API_DEPLOYED` in `public/validation.js`, together.
5. `HANDOFF.md` (~line 137) is the thing to re-read before step 3: route names
   live in **two** files while an alias lasts — `server.mjs` owns them and the
   API's nginx block forwards them — and `deploy.sh` greps both and dies when
   they disagree. A second server block is a second place that list can drift.
6. Retire the `aster` names only once nothing has called them for a while.

Until step 6, `aster.ainfinite.ai` is the address that answers. Do not delete
the old server blocks to tidy up.

---

## 2 · The localStorage keys, kept

Four keys keep their old spelling, and they are the only `aster` left in
`public/`:

```
aster-canvas-moved:<platform>:<journey|board>   public/canvas.js
aster-canvas-platform                           public/canvas.js
aster-uiux-view                                 public/uiux.js
aster-project                                   public/validation.js
```

A storage key is not a name a reader ever sees. It is a name their browser
already holds a value under, and renaming one throws that value away in silence
— the canvas one is the worst of the four, because it holds nodes somebody
dragged into place by hand. The alternative, renaming and reading the old key
once as a fallback, buys a tidier grep and costs a permanent migration branch in
four files. Not worth it.

If they are ever renamed, do it with a one-shot read of the old key, not a
straight swap. `public/validation.js` carries the note in the source; the two in
`canvas.js` and `uiux.js` do not, only because another writer held those files
open when this landed.

---

## 3 · Brand files: what exists now

`public/brand/` holds, after the rename:

| file | size | used by |
| --- | --- | --- |
| `adrov-lockup-day.png` | 13 KB | the dark-ink lockup, on pale grounds |
| `adrov-lockup-night.png` | 12 KB | the white-ink lockup, and the chrome in both themes |
| `adrov-mark.png` | 31 KB | the favicon on all eight pages |
| `adrov-mark-night.png` | 29 KB | the white-ink mark, no caller yet |
| `adrov-mark-day.svg`, `adrov-mark-night.svg` | 3 KB | the geometry `styles.css` inlines for the loading curtain |
| `adrov_light.png`, `adrov_dark.png` | 546 / 874 KB | the two supplied renders, kept as the source of record |
| `softlabs-logo.webp` | 11 KB | a different company's logo — not ours |

There is no Adrov wordmark-only cut. The old set had one and nothing referenced
it, so it was not regenerated. If a page ever needs the word without the ring,
it can be cut from `adrov_light.png` the same way.

---

## 4 · Not renamed, and not ours

`aster/ticvai` in prose became `adrov/ticvai`, but the delivery package itself
is under a one-writer protocol and was not touched. Anything the package needs
belongs in a diff in `viewer/handoff/`, not in an edit.
