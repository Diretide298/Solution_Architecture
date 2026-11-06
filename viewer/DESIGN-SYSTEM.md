# ADAM's design system

One system for the phone and the desktop, so the two look like one product. The tokens are in
`public/design-tokens.css`; the first page built on them is `/decide` (`public/decide.html`, `.css` and `.js`), and every
component below is drawn there in a working form. Open `/decide?demo=1` to see it with invented data, and add `&app=1` to
see the parts that only appear inside the phone app.

The other pages are not on this system yet. They move one at a time, following PHONE-INVENTORY.md, and when a page moves it
loads `design-tokens.css` before its own stylesheet and uses only `--ds-` names.

## The idea

**The frame is dark in both themes, and only the page inside it changes.** ADAM's chrome has always worked this way. On the
phone, the frame is the app bar at the top and the bottom bar under your thumb. Between them sits the page, which is white
by day and near-black by night. Anything that floats over the page (the toast, a menu) takes the frame colour, so it reads
the same over either theme.

**Each page spends its boldness in one place.** That place is one headline sentence in large type that answers the question
the page is opened for (on Decide: "9 blocking of 17"). Everything else stays quiet: rows separated by lines rather than
shadows, colour used only as a signal, and one primary button per screen.

**Thumb first.** On a phone, the actions you take most sit in the bottom third of the screen, and every target is at least
44 px. On a wide screen the same parts rearrange themselves: the bottom bar becomes a rail on the left, the list and the open
item sit side by side, and sheets become centred dialogs. No feature is missing from either size.

## Tokens

Every name starts with `--ds-`, so the file can sit beside `styles.css` without changing any page that does not use it.
Day is the bare `:root`, and night is `:root[data-theme="dark"]` (stamped by `theme.js`, with night as the default).

| Family | Names | Use |
|---|---|---|
| Frame | `--ds-frame`, `-raised`, `-line`, `-ink`, `-ink-2`, `-accent` | App bar, bottom bar or rail, toast. Dark in both themes. |
| Page | `--ds-bg`, `--ds-surface`, `--ds-surface-2`, `--ds-surface-press` | The ground, the things on it, a tinted step, the pressed state. |
| Lines | `--ds-line`, `--ds-line-strong`, `--ds-line-control` | A divider; a stronger divider; the edge of a control (3:1 against its surface). |
| Ink | `--ds-ink`, `--ds-ink-2`, `--ds-ink-3` | Body and titles; secondary text; the quietest text, still 4.5:1. |
| Accent | `--ds-accent`, `-fill`, `-on`, `-soft`, `-line` | ADAM's teal: links, the primary action, focus, and "needs you". |
| Signals | `--ds-danger*`, `--ds-warn*` | Danger means blocking, reject or failed. Warn means waiting on someone else, or paused. Always pair them with words. |
| Type | `--ds-font-sans`, `--ds-font-mono`, `--ds-text-xs` to `-2xl` (13, 14, 16, 20, 25, 31 px), `--ds-leading-*`, `--ds-weight-*` | One family for reading. Mono only for code, `file:line` references and hashes. Body text is never under 16 px on a phone. |
| Space | `--ds-space-1` to `-12` (4 px grid), `--ds-gutter` (16 px on a phone, 24 px from 720 px) | Steps 1 to 4 inside a component, 4 to 6 between components, 8 and up between sections. |
| Radius | `--ds-radius-xs` 6, `-sm` 10, `-md` 14, `-lg` 22, `-pill` | Chips; buttons and fields; rows and cards; sheets. An outer radius equals the inner radius plus the padding. |
| Elevation | `--ds-shadow-1` to `-3` | Only for things that float: the toast, sheets, the settle dock. Rows and cards use lines. |
| Motion | `--ds-dur-instant` 80, `-fast` 160, `-normal` 280, `-slow` 420 ms; `--ds-ease-out`, `-in`, `-sheet`, `-spring`; `--ds-press-scale` | Tap feedback is fast; sheets and pushed screens are normal. Exits are quicker than entrances. |
| Touch | `--ds-touch-min` 44, `--ds-touch-comfy` 48, `--ds-touch-gap` 8 | 44 px is the minimum for anything tappable; 48 px for the primary action and the bars. |
| Layout | `--ds-bar-top` 56, `--ds-bar-bottom` 64, `--ds-safe-*`, `--ds-content-read`, `--ds-content-list` | Bar heights, safe areas (notch, gesture bar) and reading widths. |
| Stacking | `--ds-z-bar`, `--ds-z-sheet`, `--ds-z-toast` | A toast is never under a sheet. |

Breakpoints are fixed values, because custom properties cannot be used inside media queries. A phone is under 720 px, a
tablet is 720 to 1079 px, and a desktop is 1080 px and up. From 960 px, a page with a list and a detail shows both side by
side.

Under `prefers-reduced-motion`, the durations collapse to a short fade and `--ds-press-scale` becomes 1. Each page also
removes its own transforms under the same query (slides, springs and the shimmer).

## Components

Each component has the same two shapes on every page: the phone version and the desktop version.

### App bar

The page's name, how fresh the data is, and one or two icon buttons, on the frame colour.

- **Phone:** sticky at the top, at 56 px plus the safe-area inset. It shows the mark, the title, and a second line that
  says how fresh the data is ("Updated 2 min ago", or "Offline. List from 13:20" in warn colour). The icon buttons are
  48 px. On a screen pushed in from the right (an open request), the bar shows Back, the item's id, and previous/next
  buttons.
- **Desktop:** the same bar, starting to the right of the rail. A page that has the viewer's layer tabs keeps them here.
- **Rules:** one line of title. Freshness is plain text in a polite live region. A full-width banner directly under the bar
  (sticky with it) reports anything true of the whole page: offline, a pause, or the demo.

### Bottom bar (rail on desktop)

Top-level sections only, with at most five. Decide has three: Inbox, Decided and Health.

- **Phone:** fixed to the bottom on the frame colour, 64 px plus the safe area. Each item shows an icon above a label. The
  current item gets a pill behind its icon and the accent colour on the icon. A count badge sits at the icon's top right
  (white for a plain count, teal for "waiting on you"), and a status dot means "look here" (red for failed, amber for a
  warning).
- **Desktop:** the same items become a 96 px rail down the left edge.
- **Rules:** each item is a `button` with `aria-current="page"` on the current one, and an `aria-label` that includes the
  count ("Decided, 3 requests to settle"). On a phone, the bar is inert while a pushed screen is open.

### List row with chips

One item to decide or open. Rows sit in one surface with lines between them, not as a stack of cards.

- **Phone:** the first line is the id plus how long the item has waited (right-aligned, tabular figures, red once it is
  overdue). Below that come the title, clamped to two lines, then a meta line with the ticket and the person, then chips.
  A 3 px stripe on the left edge repeats the most urgent chip's colour, so the list can be scanned by shape alone.
  - **Swipe right** to take the primary action. On Decide that is Approve: the row slides off a teal field, and a toast
    offers Undo.
  - **Swipe left** to open the row.
  - Touches that start within 24 px of either screen edge are left to Android's back gesture.
  - The first group shows a one-line hint about swiping until the first swipe.
- **Desktop:** the same row in the list pane. The open row is tinted `--ds-accent-soft`. `j` and `k` move between rows,
  `Enter` opens one, and `a` approves.
- **Chips** are 24 px tall and 13 px semibold, with a dot, in sentence case: "Blocking" (danger), "Needs you" (accent),
  "Needs the client" (warn). A chip states a fact; it is never a button.
- **Rules:** the row is a real `button` that opens the item. A second button inside the row ("Approve CR-598") is invisible
  until it gets keyboard focus, so the swipe always has a keyboard and screen-reader alternative. Rows that newly arrive
  get a 280 ms entrance; nothing else animates on load.

### Card

A small, separate fact: a status, a figure or a setting.

- **Phone:** full width, or two side by side for short pairs (Last run and Errors). It has a 14 px radius, a 1 px line,
  16 px padding, a small grey title, the value in 20 px bold, and an optional note. A meter (10 px, `scaleX` fill) shows a
  share of a limit: accent, then warn from 80 %, then danger at 100 %.
- **Desktop:** the same cards in a column of at most 760 px. Do not stretch them across the screen.
- **Rules:** no card inside a card, and no shadow. A card that reports a failure takes the danger border and says what
  failed, in words.

### Sheet and drawer

A short step taken on top of the page: a reason for a reject, a list to confirm, or the dry run before settling.

- **Phone:** a bottom sheet with 22 px top corners, a grip, a title that asks the question ("Reject the draft for
  CR-618?"), one sentence on what will happen, the fields, then a sticky action row with a secondary button on the left and
  the primary on the right. Drag it down or tap the scrim to close it. A full-screen view (an open request) is a pushed
  screen that slides in from the right, not a sheet.
- **Desktop:** the sheet becomes a centred dialog, 560 px wide. A pushed screen becomes the right-hand pane beside the
  list.
- **Rules:** `role="dialog"` and `aria-modal`. The page behind it is `inert`, and focus moves to the first field and stays
  inside the sheet. `Esc` closes it, and focus returns to whatever opened it. While a sheet is open, the toast moves to the
  top of the screen so it never covers a field.

### Buttons

| Kind | Look | Use |
|---|---|---|
| Primary | `--ds-accent-fill`, `--ds-accent-on` text, 48 px | The one action a screen exists for. One per screen. |
| Danger | `--ds-danger-fill` | The action that discards or refuses (Reject the draft). Placed away from the primary. |
| Secondary | `--ds-surface-2` | Not now, Keep it, Cancel. |
| Line | Surface with `--ds-line-control` border | Try again, Go to Change requests. |
| Ghost | Accent text, no fill | Optional bulk actions ("Approve the 9 that need nobody"). |
| Action bar | 56 px, icon over label | A phone's bottom action bar: Reject, Change, Ask on the left, and the wide primary Approve on the right, under the thumb. On desktop the icon sits beside the label and the bar aligns right. |

Pressing scales a button to 0.97 in 160 ms. While a button is working, its label is replaced by a spinner and it is
disabled. Disabled buttons show at 45 % opacity with the `disabled` attribute. Labels say exactly what will happen
("Settle 3", "Save the change", "Reject the draft"), and the toast that follows uses the same verb ("Settled 3 requests").

### Text field

- **Phone:** a visible label above the field (14 px semibold), and the field itself at 48 px or more with 16 px text (so
  iOS does not zoom in). The border uses `--ds-line-control`. Help text sits under the field; an error replaces nothing
  and appears under the help in danger colour, linked with `aria-describedby` and `aria-invalid`. A text area starts at
  132 px tall. A compose box (Ask) starts one line tall, grows up to 160 px, and has its send button beside it.
- **Desktop:** the same field, capped at the reading width.
- **Rules:** never use a placeholder as the only label. Validate on submit, put the error at the field, and move focus to
  the field.

### Toast with undo

The receipt for something that just happened, with one way to take it back.

- **Phone:** frame colour and 14 px radius, floating 12 px above the bottom bar (or above the action bar on a pushed
  screen). It shows a bold line, an optional sub-line, and one text button (Undo, Open or Try again). A 3 px bar along the
  bottom drains over the undo window (5 s on Decide); the action is sent only when the window closes, or immediately if the
  page is left. An error toast has a danger border.
- **Desktop:** bottom right, 420 px wide.
- **Rules:** `role="status"`, polite, and it never takes focus. Undo restores the item exactly where it was. Only one toast
  shows at a time; an earlier action still in its window can be undone from its row in Decided. Under reduced motion the
  draining bar is dropped and the toast fades.

### Empty and error states

Every list has all four states, and each says what happened and what to do next.

- **Empty:** a 56 px tinted square holding an icon, a title that states the fact ("You are up to date"), one sentence on
  why and when that changes, and the next action if there is one ("Go to Decided").
- **Error:** the same shape in danger colour. The title names the failure ("ADAM cannot be reached", "The watcher is not
  set up on this server"), the sentence gives the cause and the fix, and the button retries ("Try again", "Check again").
- **Permission:** a lock icon and "This page is for the lead", plus who you are signed in as and a link to the page you can
  use.
- **Loading:** skeleton rows in the shape of the real rows (shimmer, or still under reduced motion), not a spinner. The
  headline reads "Loading the requests" to a screen reader.
- **Partial or offline:** keep showing what was cached, say so in the app bar's second line and the banner, and accept
  actions into an outbox that sends when the connection returns. The outbox stays bound to what each action was made on.
- **Phone and desktop:** identical. On desktop, the empty right-hand pane says what will appear there and lists the
  keyboard keys.

## Writing

- Use sentence case everywhere. No all-caps labels, and no eyebrow text above headings.
- Use plain verbs that name the outcome. The button, the toast and the record use the same word.
- Do not use acronyms or batch codes in labels. Name the thing.
- Errors say what happened, then how to fix it. They never apologise.
- Never use emoji as icons. Icons are 24 px line icons with a 1.8 stroke, and an icon beside a word is `aria-hidden`.

## Checks before a page moves onto the system

1. Screenshots at 390 × 844 and 360 × 780 in day and night, plus one at 1440 × 900.
2. Every tappable thing is 44 px or more, with at least 8 px between neighbours.
3. Text contrast is 4.5:1 and control edges 3:1, in both themes. The token pairs above were measured; a new pair is
   measured before it is used.
4. Everything works from a keyboard with a visible focus ring. Swipes and drags have a button alternative.
5. Reduced motion is checked: nothing slides, and nothing important is lost.
6. The loading, empty, error, permission and offline states are each seen once.
