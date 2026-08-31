# Adam: what the rename could not do from here

The product is Adam. The viewer says so everywhere a reader can see it — titles,
alt text, the sign-in copy, the loading curtain, the brand files — and the
deployment says so everywhere a file can say it: both nginx blocks, `deploy.sh`,
the CORS lists and the install instructions.

What is left is the part no edit reaches. A hostname is a DNS record and a
certificate, not a string in a repository, so the two live names still answer
and the two new ones do not exist yet. Section 1 is the order to fix that in.
The storage keys below are a separate decision and a smaller one.

---

## 1 · The hostnames, and the certificates behind them

The files are done and aliased. **What is left is DNS and one certbot run**, and
neither of those is an edit anybody can make from here.

```
aster.ainfinite.ai      →  :4173   the package, and the gate
asterapi.ainfinite.ai   →  :8787   accounts, invites, verdicts, /docs
```

Those two are live DNS with Let's Encrypt certificates issued against them, and
they are still the names that answer. `adam.ainfinite.ai` and
`adamapi.ainfinite.ai` have no record, no certificate and no traffic.

### What the tree already says

| where | state |
| --- | --- |
| `deploy/nginx/adam.ainfinite.ai` | renamed; `server_name adam… aster…`, both |
| `deploy/nginx/adamapi.ainfinite.ai` | renamed; `server_name adamapi… asterapi…`, both |
| `deploy/deploy.sh` | `NGINX_SITE` points at the renamed file; `PUBLIC_ORIGIN` carries both origins |
| `api/main.py`, `server.mjs` | both origins in the CORS list and in `ALLOWED_ORIGINS` |
| `deploy/README.md`, `HANDOFF.md` | the adam names, and the install lines that remove the old symlink |
| `public/validation.js` | **still `asterapi`** — one value, not a list, and it moves with the DNS |

**The `ssl_certificate` lines in both blocks still name aster, deliberately.**
They name the certificate that exists. Point a server block at a cert that is
not on disk and nginx refuses to start — it does not fall back, and it takes
every other site on the box down with it. Certbot rewrites those lines itself.

### The order, and it matters

1. **A records** for `adam.ainfinite.ai` and `adamapi.ainfinite.ai`, pointing at
   the same address as the aster pair. Wait for them to resolve.
2. **Install the renamed blocks and drop the old symlinks** — the filenames
   changed, so a plain `cp` leaves the old ones enabled and nginx then has two
   blocks claiming the same `server_name`:
   ```
   sudo cp deploy/nginx/adam.ainfinite.ai deploy/nginx/adamapi.ainfinite.ai      /etc/nginx/sites-available/
   sudo rm -f /etc/nginx/sites-enabled/aster.ainfinite.ai               /etc/nginx/sites-enabled/asterapi.ainfinite.ai
   sudo ln -sf /etc/nginx/sites-available/adam.ainfinite.ai /etc/nginx/sites-enabled/
   sudo ln -sf /etc/nginx/sites-available/adamapi.ainfinite.ai /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```
   At this point adam answers on **:80 only** — the https block is still on the
   aster certificate, which does not cover the new name, so an https request to
   adam gets a name-mismatch warning. That is expected and step 3 ends it.
3. **Expand the certificates rather than issuing new ones**, so there is never a
   moment when a name that resolves has no certificate:
   ```
   sudo certbot --nginx --cert-name aster.ainfinite.ai      -d aster.ainfinite.ai -d adam.ainfinite.ai
   sudo certbot --nginx --cert-name asterapi.ainfinite.ai      -d asterapi.ainfinite.ai -d adamapi.ainfinite.ai
   ```
   `--cert-name` keeps the existing lineage, so the `ssl_certificate` paths in
   the blocks stay correct and the renewal timer needs nothing.
4. **Point the browser at the new name**, and only now. Two values, one commit,
   because they are the same fact written twice:
   - `TICVAI_API_PUBLIC` in `/srv/ticvai/ecosystem.config.cjs` →
     `https://adamapi.ainfinite.ai`
   - `API_DEPLOYED` in `public/validation.js` → the same
   Then `pm2 restart ticvai-viewer ticvai-api --update-env` and a deploy.
5. **Re-read `HANDOFF.md` (~line 137) before touching routes.** Route names live
   in **two** files while an alias lasts — `server.mjs` owns them and the API's
   nginx block forwards them — and `deploy.sh` greps both and dies when they
   disagree.
6. **Retire the aster names last**, once nothing has called them for a while:
   drop them from `server_name`, from `PUBLIC_ORIGIN`, from the two CORS lists,
   and re-run certbot without them.

Until step 6, aster is a name that answers. Do not tidy it away early.

---

## 2 · The localStorage keys, kept

Four keys keep their old spelling. With `API_DEPLOYED` above them they are all
the `aster` left in `public/` — the rest of what a grep finds there is
`asterisks` and `faster`:

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
| `adam-lockup-day.png` | 12 KB | the dark-ink lockup, on pale grounds |
| `adam-lockup-night.png` | 12 KB | the white-ink lockup, and the chrome in both themes |
| `adam-mark.png` | 27 KB | the favicon on all eight pages |
| `adam-mark-night.png` | 28 KB | the white-ink mark, no caller yet |
| `adam-mark-day.svg`, `adam-mark-night.svg` | 3 KB | the geometry `styles.css` inlines for the loading curtain |
| `adam_light.png`, `adam_dark.png` | 754 / 849 KB | the two supplied renders, kept as the source of record |
| `softlabs-logo.webp` | 11 KB | a different company's logo — not ours |

There is no Adam wordmark-only cut. The old set had one and nothing referenced
it, so it was not regenerated. If a page ever needs the word without the ring,
it can be cut from `adam_light.png` the same way.

---

## 4 · Not renamed, and not ours

`aster/ticvai` in prose became `adam/ticvai`, but the delivery package itself
is under a one-writer protocol and was not touched. Anything the package needs
belongs in a diff in `viewer/handoff/`, not in an edit.
