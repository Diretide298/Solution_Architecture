# Claude Design hand-off: start here

> **Updated:** 30 September 2026, after the 29 September pass.
> **Return route (decided 30 September): one working file per app.** Each app folder under `apps/` has `return/<app>.dc.html`; every batch of that app extends the same file. Claude Code captures the screens from it as frames. The B2B options (two files, one per option) and the demo site are separate, because they are not apps.
>
> **What is here:** one folder per design batch (`BRIEF.md` and `BUNDLE.md`), one folder per app under `apps/` (seven apps: Guest App, POS, Scanner, Staff App, Venue Management, TICVAI main controller, Partner Portal; each README covers the screen sets that make up the app), and three special folders.
> **How a session runs:** `VENUE-MANAGEMENT.md` (one session per batch) and `docs/active/claude-design-runbook.md` (the standing prompt and the import).

## Where to start for each app

Each platform folder says what the app is, who uses it, the reference design to match, its batches in order, how many screens have client-verified frames, and the prompt to paste.

| platform | folder | screens | Block A screens | frames | client-verified |
|---|---|---|---|---|---|
| P01 Guest web | [`apps/1-guest-app`](apps/1-guest-app/README.md) | 50 | 50 | 49 | 48 |
| P02 Guest app, mobile | [`apps/1-guest-app`](apps/1-guest-app/README.md) | 77 | 77 | 77 | 77, but on the old Mobile v2 build |
| P04 POS + P15 kitchen display | [`apps/2-pos`](apps/2-pos/README.md) | 40 | 40 | 30 | 23 |
| P05 Guest kiosk | [`apps/1-guest-app`](apps/1-guest-app/README.md) | 17 | 0 | 0 | 0 |
| P06 Venue staff app | [`apps/4-staff-app`](apps/4-staff-app/README.md) | 96 | 3 | 0 | 0 |
| P07 Venue scanner | [`apps/3-scanner`](apps/3-scanner/README.md) | 11 | 0 | 0 | 0 |
| P08 Venue management | [`apps/5-venue-management`](apps/5-venue-management/README.md) | 1,186 | 66 | 0 | 0 |
| P09 TICVAI web console | [`apps/6-ticvai-controller`](apps/6-ticvai-controller/README.md) | 676 | 44 | 0 | 0 |
| P10 Partner reseller portal | [`apps/7-partner-portal`](apps/7-partner-portal/README.md) | 51 | 0 | 0 | 0 |
| P11 Accreditation web | [`apps/5-venue-management`](apps/5-venue-management/README.md) | 8 | 0 | 0 | 0 |
| P12 Venue support | [`apps/5-venue-management`](apps/5-venue-management/README.md) | 28 | 1 | 0 | 0 |
| P13 Venue CMS | [`apps/5-venue-management`](apps/5-venue-management/README.md) | 103 | 25 | 0 | 0 |
| P14 Developer portal | [`apps/6-ticvai-controller`](apps/6-ticvai-controller/README.md) | 8 | 3 | 0 | 0 |
| P16 Venue analytics | [`apps/5-venue-management`](apps/5-venue-management/README.md) | 70 | 4 | 0 | 0 |
| P17 TICVAI sign-up | [`apps/6-ticvai-controller`](apps/6-ticvai-controller/README.md) | 24 | 0 | 0 | 0 |

"Block A" is the first 35 working days of the build, from Monday 5 October: the screens with a front-end task in phase 1 of `handoff/service-docs/tasks.csv`. "Client-verified" means the frame is a capture of a client-approved prototype.

## The order

Run top to bottom. Within a platform, its README gives the batch order.

### 1. Block A

1. **P13 CMS flow builder**: [`CMS-FLOW-BUILDER/`](CMS-FLOW-BUILDER/BRIEF.md). CMS-101 to CMS-104 as one flow, with the step screens they open. Then the P13 Block A batches: `P13-white-label-03`, `-01`, `-02`, `WS41`.
2. **P02 Mobile v4 changes**: see [`apps/1-guest-app`](apps/1-guest-app/README.md). First re-capture the 17 screens that are views in Mobile App v4 (a capture job, not a design batch). Then draw the 19 changed screens v4 has no view for, in the v4 look.
3. **P01 WEB-050 and the changed screens**: [`P01-discovery-browse-01`](P01-discovery-browse-01/) (WEB-050 Plan Your Visit, from the Visit Planner), then the P01 batches with changed screens. See [`apps/1-guest-app`](apps/1-guest-app/README.md).
4. **P15 kitchen display**: [`P15-kitchen-01`](P15-kitchen-01/). P04 is locked; the client-approved terminal is its design.
5. **P08 set-up screens**: the 38 P08 Block A batches, set-up screens first. See [`apps/5-venue-management`](apps/5-venue-management/README.md).
6. **The rest of Block A**: P09 (23 batches), P16 (3), P06 (2), P12 (1), P14 (1). Each platform README lists them.

### 2. B2B options

[`B2B-OPTIONS/`](B2B-OPTIONS/BRIEF.md). The reseller portal drawn two ways, POS-style and website-style, with a one-page comparison. The client chooses (MoM 29 September, section 3). The chosen file becomes the start of the Partner Portal's working file ([`apps/7-partner-portal`](apps/7-partner-portal/README.md)), and the P10 batches wait for that choice.

### 3. Demo site

[`DEMO-SITE/`](DEMO-SITE/BRIEF.md). The TICVAI marketing site's product demos: POS, kiosk, mobile app, guest web booking, kitchen display, menu management and the CMS flow builder, each with a self-running simulation.

### 4. The rest, by platform

In this order: P13, P01, P02, P05, P06, P07, P10 (after the choice), P12, P16, P14, P11, P17, P08, P09. Each platform README lists its remaining batches in the manifest order (fully specified first, thin last).

`QUEUE.md` is the older overnight queue of 191 batches, from before the 29 September pass. It still works as a list, but this order replaces it.

## Refreshing

```bash
python tools/derive-design-manifest.py        # what is drawn, off the disk
python tools/export-design-batch.py --list    # what is pending
python tools/export-design-batch.py <BATCH ID>
```

The platform READMEs were written on 30 September from `wireframes/design-manifest.json`. Their batch statuses do not refresh by themselves; the manifest is the live count.
