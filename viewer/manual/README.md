# Team manual

`TICVAI-Viewer-Manual.pdf` — 55 pages, 44 figures, written for the rest of the team. Hand it to
anyone who has to read the delivery package and has not used the viewer.

Every figure is a photograph of the running application, taken by driving a real browser through
every view. There are no mock-ups, so a figure cannot quietly drift from what the app does.

## Regenerating

```bash
cd viewer
npm start                  # in one terminal — the capture needs the app running
node manual/capture.mjs    # re-shoots all 45 captures into manual/shots/
node manual/build.mjs      # re-renders the PDF
```

`capture.mjs` fails loudly rather than producing a manual with a blank figure in it: it reports any
console error the app raised while being photographed, and `build.mjs` refuses to print if an image
did not load. Both find Chrome or Edge automatically; set `CHROME=/path/to/chrome` if yours is
somewhere unusual, and `VIEWER_URL` if the viewer is not on `:4173`.

Both scripts need `puppeteer-core`, which is a devDependency of the viewer — `npm install` gets it.
It brings no browser of its own, so nothing is downloaded.

## Changing it

| Want to | Edit |
|---|---|
| Add or reword a section | `manual.html` — plain HTML with print CSS at the top |
| Add a figure | One entry in the capture sequence in `capture.mjs`, then a `<figure>` in `manual.html` |
| Move a callout number on Figure 1 | The `.pin` spans in `manual.html`; positions are percentages of the screenshot |
| Change page size, header or footer | `build.mjs` — the `page.pdf()` options |

`shots/layout.json` records where each region of the window actually was when the figure was taken,
which is what the callout percentages are derived from.

**Figure numbers are a CSS counter, not typed in.** Insert a figure anywhere and everything after it
renumbers itself — write `<b class="figno"></b>` and the number appears. The figures cannot drift
from the app; the numbering should not be the one part that does.

## What is in it

1. Running it · 2. The window (and the hover tips) · 3. The four layers · 4. Contracts layer ·
5. Frontend layer · 6. Domain layer · 7. Backend layer · 8. Tracing across layers · 9. Search ·
10. The audit · 11. Reading the colours · 12. Keyboard shortcuts · 13. Keeping it current ·
14. Known gaps · 15. Troubleshooting · 16. Glossary

Chapter 4 explains why the contracts graph opens on **Spine**; chapter 5 covers the 180 wireframes
and how they differ from the design boards; chapter 6 is the state models and the event catalogue.
