# Five decisions from the specification read

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** decided, except where marked
>
> Taken against [specification-read-19-september](specification-read-19-september.md), which raised
> them. Each says what supersedes what, because the conflicts here are between documents of
> different rank and the losing document does not disappear.

---

## 1 — Access control: HID and Suprema. The MoM supersedes the RFP list.

| source | rank | names |
|---|---|---|
| RFP, domain 4 | 2 | Axess · Skidata · CAME · KABA · Boon Edam · *"other industry-standard systems"* |
| **MoM 24 August** | **1** | **HID or Suprema** (CF-35) |
| Hardware sheet | — | turnstile reader: HID, Axess, Suprema |

**Decision: HID and Suprema.** The 24 August minute is rank 1 and later, and per the authority rule
a later rank-1 decision supersedes. **The remaining vendors are not dropped — they are staged.**
Axess, Skidata, CAME, KABA and Boon Edam become later-stage integrations, which the RFP's own
wording already allows for: it asks for support for *"other industry-standard systems"*, not for
those five exclusively.

**Why this needs recording rather than just doing.** The narrowing went to two vendors the RFP
never names, and until today nothing in the package said so. Anyone reading the RFP alone would
conclude we had ignored the list; anyone reading the MoM alone would not know a list existed.

> *Integration happens at two levels — the turnstile itself and the reader — each producing its own
> outputs. Devices push events to TICVAI via a TCP/IP API.* — MoM 2 September

That TCP/IP event-push shape is vendor-neutral, which is what makes staging the rest cheap.

## 2 — Gaming reader: direct to hardware via the vendor's SDK. Manufacturer still open.

The hardware sheet says `China`, which reads as undecided. **The 11 September minute shows it is
not:**

> *"TICVAI will provide a physical game reader at each game/ride, with pricing, branding, and theme
> pushed from TICVAI's back end and displayed directly on the reader; tapping the reader triggers a
> dry-contact-style signal to start or stop the game, conceptually similar to a turnstile at access
> control."*

**The integration strategy is decided and it is the industry-standard one for our position:**

> *"established arcade-management vendors (e.g., Simnox, Intercard) generally refuse to integrate
> with TICVAI since they view it as a competing platform. TICVAI's intended approach is to integrate
> directly with reader hardware (via the hardware vendor's own SDK/API) rather than going through an
> intermediary gaming-management software layer — avoiding a situation where clients run two
> separate systems for ticketing and gaming."*

**What is actually open is the manufacturer**, and it is an action on us:

> *"Gaming reader hardware/SDK vendor selection — Qossai finalizing with Chinese manufacturers;
> Chinmay to check for India-market alternatives."*

**One thing to check when that action is picked up:** the minute writes *Simnox*. The arcade
vendor of that name is **Semnox**, which is India-based — so the vendor recorded as refusing to
integrate may be the same India-market option the action asks us to look for. Worth confirming the
spelling and the company before spending time searching.

`China` in the hardware sheet should read **`pending — direct SDK integration, manufacturer TBD
(MoM 11 Sep)`**. It is an open action, not an absent decision.

## 3 — Kitchen display: not a vendor question.

`Decide later` on the hardware sheet implies a procurement decision that does not exist.

> *"KDS integration only"* — MoM 31 July
>
> *"POS & device management allows configuration of receipt printers, kitchen printers and KDS
> devices per outlet/terminal… each [station] mapped to specific printers or KDS devices… fallback
> station/device if the primary one is offline or faulty."* — MoM 18 August

**Decision: commodity display, our software.** `P15 Kitchen Display — Pass and Stations` is already
a platform in this package with 10 screens. The KDS "hardware" is any touchscreen that can render
it; what matters is the station mapping, the routing rules and the offline fallback, all of which
are ours and all of which are specified in the 18 August minute. **No vendor row is needed.**

## 4 — On-premise: the same cell, on their servers. ADR proposed, not written.

The RFP requires *"Cloud, On-Premise, and Hybrid"* and the package models only in-region cells.

**Decision: on-premise is the same server topology, deployed to local servers.** A cell is already
a self-contained unit — one Postgres, in-cell hosting, in-region — so an on-premise install is that
same unit with the boundary drawn at the customer's data centre rather than at a region. The shape
does not change; the location does.

**What genuinely changes is service-to-service calls.** In-cell, services reach each other over a
network we control and can assume present. On-premise, that assumption has to be stated rather than
inherited — which is why this is worth an ADR rather than a sentence.

> **This ADR is proposed and NOT written.** ADR changes are confirmed first, every time. The
> proposal: *internal API calls are cell-local and must not assume egress*, with the deployment
> target — region cell or customer premises — as a property of the cell rather than of the service.
> **Say the word and I will draft it.**

## 5 — Dev01–03 are a deliverable, not a source. Restored out of `legacy/`.

> *"The TIAS platform will be fully owned by the client, including source code, architecture,
> documentation, and intellectual property… The vendor must provide full access to the source code
> repository and ensure the platform can be independently maintained and extended by the client or
> third-party developers."* — RFP §Intellectual Property

Ch01–Ch09 stay retired in `sources/legacy/` — they are our proposal and never scope. **Dev01–03 are
different in kind**, and now sit in `sources/specifications/handover/`:

| | |
|---|---|
| `Dev01_Engineering_Handbook` | how the platform is built |
| `Dev02_Repository_Structure_and_Contract_Pipeline` | how the repo is laid out |
| `Dev03_Local_Development_Environment` | how a new developer starts |

**They produce no screens.** Nothing in `screens/` should cite them and no coverage check should
count them. What they produce is **source code and documentation** — the artefacts the IP clause
obliges us to hand over in a state a third party can pick up. They are a checklist for the handover,
not an input to the package.

---

## 6 — Where this is all going: the matrix, not six separate checks

Functional coverage is **15%** of the evaluation. That is not an argument for drawing more screens;
it is an argument for the requirement matrix being right, because the matrix is what coverage is
scored against.

**The three sources are inputs to the matrix, not rival baselines.** Today produced three coverage
reports — RFP, Ch03, and the pack triage — each with its own lexical matcher and its own false
positives. That is three tools disagreeing about the same question.

| source | rank | what it contributes to the matrix |
|---|---|---|
| **MoMs** | 1 | what was decided, and what supersedes what |
| **RFP** | 2 | what was asked for, in the client's own words |
| **Design books** | 3 | what the screens are, board by board |

The matrix already holds 3,184 requirements across 21 domains. **Sharpening it from all three is
the next job**, and it is the same job as improving the parser — a parser that reads one category
can only ever produce a partial answer.
