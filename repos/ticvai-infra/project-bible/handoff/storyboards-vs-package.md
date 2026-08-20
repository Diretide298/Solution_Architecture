# Client storyboards against the package

**18 August 2026.** The three design PDFs in `sources/designs/` are client storyboards — 8 guest
boards and 6 employee boards, 10 screens each, roughly 140 screens in all. **They are images with
no text layer**, which is why nothing in this package had read them until now.

Reviewed: **all 8 guest boards, and employee board 1 of 6.** Employee boards 2–6 are unread.

---

## The naming is misleading and cost us something

`TICVAI_White_Label_Guest_App_UI_Reference_1.pdf` is not the guest app. **Boards 1 and 2 are the
white-label builder — the CMS.** Boards 3–8 are the guest app.

Twenty CMS screens sit in a file named for the guest app, and `P13 Venue CMS` was specified
without them.

---

## Four open items the storyboards settle

### CF-92 — the eight "unsourced" screens are all drawn

Closed on 10 August on the strength of the MoM. **The storyboards confirm it independently and in
more detail than the minutes did.**

**Board 8 carries five of them as a complete flow**: *Plan Your Adventure – Start*, *Suggested
Itineraries*, *Build Your Own Itinerary*, **AI Optimized Itinerary — labelled "Powered by
TICVAI"** and *Plan My Day – In Progress*. Plus *Accessibility Information* and *Resource
Availability (Cabana)* on the same board.

**Board 6 panel 8 is Digital Companion Mode** — the one screen I could not source at all, drawn as
*Your Visit Journey*: before, during and after the visit. `GST-038` has provenance.

### CF-14 — the guest concierge is drawn in full

**Board 6 panels 1–3 are `GST-031`, `GST-032` and `GST-033` exactly**: AI Concierge Home with
suggested questions, Chat with a voice input, and Contextual Help answering a wait-time question
in place.

**Board 2 panel 8 lists "AI Concierge Chat" as a per-tenant feature toggle**, alongside Digital
Companion Mode — which is the commercial model CF-14 asked about, drawn as a switch.

### CF-41 — AI is a primary navigation tab

**Employee board 1, panels 3 and 4.** The bottom navigation reads Home · Tasks · **AI** · More,
and *AI Assistant* appears again as a module tile. The tab is in the shell, exactly as CF-41
states.

### CF-99 — the guest side of live chat exists

**Board 6 panel 10, Help & Support**, offers *Live Chat — chat with us* beside Call Us and Email
Us. The handover's guest entry point is drawn; only the agent console was specified.

---

## 🔴 One decision I made against the matrix, and the storyboard says the opposite

**CF-91 moved multi-currency from the guest app to the web**, because 2.6.33 and 2.9.1 both name
the website and neither names the app. `WEB-035` was added and `GST-044` left alone.

**Board 7 panel 4 is "Multi-Currency & Pricing" on the guest app** — a currency selector showing
AED, USD, EUR, GBP and SAR, with *"Payment will be processed in AED"*. Board 8's header carries an
AED selector too.

**Both are client documents and they disagree.** The matrix says website; the storyboard draws it
on the app. **The reasoning I gave — that the website is where an overseas guest compares prices
before travelling — is sound and was not the client's.**

**It should be on both.** That is what CF-93 concluded for every other guest capability, and there
is no reason multi-currency is the exception. Raised as CF-111.

---

## What the storyboards show that we have not specified

| Board | Screen | |
|---|---|---|
| Guest 7.6 | **Branded Queue / Waiting Room** | **CF-48's Q2**, drawn — a branded waiting room with a queue position and an estimated wait. It is open as *"edge infrastructure, not a product contract"* and the client has drawn it as a product screen |
| Guest 7.7 · 8.10 | **Maintenance / Upgrade Page** | A branded "we'll be back shortly" with an expected return time. No screen anywhere |
| Guest 7.2 | **UAE PASS sign-in** | Drawn as a first-class option beside email and mobile OTP. `identity` has SSO providers and nothing names UAE PASS |
| Guest 3.10 · 7.5 | **Add to Wallet** | Apple Wallet on the confirmation and the ticket. `GST-018` is calendar reminders, not wallet passes |
| Guest 8.5 | **Dynamic QR with a live countdown** | `GST-055` exists. The storyboard adds the 45-second refresh as a visible element |
| Employee 1.8 | **Create Request Hub** | Nine request categories from one entry point — maintenance, IT, cleaning, security, stock, equipment, purchase, leave, other. We have requisitions and work orders; not this front door |

**The first two are the ones to act on.** A waiting room and a maintenance page are both
guest-facing, both branded, and both are what a guest sees when the platform is under strain —
which is exactly when a white-label venue cares most about what it looks like.

---

## The design references in `screens/`

**230 of 376 screens cite one of these PDFs. 146 cite nothing**, and they are not scattered:

| | Screens with a reference |
|---|---|
| P01 · P02 · P04 · P05 · P06 · P07 · P13 | **all of them** |
| P08 Venue Management | 18 of 91 |
| P09 TICVAI Web | 1 of 37 |
| P10 · P11 · P12 | **none** |

**That is not a gap in the package — it is a gap in the storyboards.** Nothing was ever drawn for
partner, accreditation, support or most of the back office. Worth knowing before design review,
because 146 screens will arrive with no client-agreed visual direction.

---

## Housekeeping

**`designs/` and `sources/designs/` hold byte-identical copies of the same three PDFs** — 7 MB
shipped twice. `screens/` cites the first; `sources/README.md` documents the second.
