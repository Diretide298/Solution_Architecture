# Claude Design hand-off: start here

> **Updated:** 30 September 2026, after the 29 September pass.
> **What is here:** one folder per design batch (`BRIEF.md` and `BUNDLE.md`), one folder per platform under `platforms/`, and three special folders.
> **How a session runs:** `VENUE-MANAGEMENT.md` (one session per batch) and `docs/active/claude-design-runbook.md` (the standing prompt and the import).

## Where to start for each app

Each platform folder says what the app is, who uses it, the reference design to match, its batches in order, how many screens have client-verified frames, and the prompt to paste.

| platform | folder | screens | Block A screens | frames | client-verified |
|---|---|---|---|---|---|
| P01 Guest web | [`platforms/P01-guest-web`](platforms/P01-guest-web/README.md) | 50 | 50 | 49 | 48 |
| P02 Guest app, mobile | [`platforms/P02-guest-app-mobile`](platforms/P02-guest-app-mobile/README.md) | 77 | 77 | 77 | 77, but on the old Mobile v2 build |
| P04 POS + P15 kitchen display | [`platforms/P04-P15-pos-and-kds`](platforms/P04-P15-pos-and-kds/README.md) | 40 | 40 | 30 | 23 |
| P05 Guest kiosk | [`platforms/P05-guest-kiosk`](platforms/P05-guest-kiosk/README.md) | 17 | 0 | 0 | 0 |
| P06 Venue staff app | [`platforms/P06-venue-staff-app`](platforms/P06-venue-staff-app/README.md) | 96 | 3 | 0 | 0 |
| P07 Venue scanner | [`platforms/P07-venue-scanner`](platforms/P07-venue-scanner/README.md) | 11 | 0 | 0 | 0 |
| P08 Venue management | [`platforms/P08-venue-management`](platforms/P08-venue-management/README.md) | 1,186 | 66 | 0 | 0 |
| P09 TICVAI web console | [`platforms/P09-ticvai-web-console`](platforms/P09-ticvai-web-console/README.md) | 676 | 44 | 0 | 0 |
| P10 Partner reseller portal | [`platforms/P10-partner-reseller-portal`](platforms/P10-partner-reseller-portal/README.md) | 51 | 0 | 0 | 0 |
| P11 Accreditation web | [`platforms/P11-accreditation-web`](platforms/P11-accreditation-web/README.md) | 8 | 0 | 0 | 0 |
| P12 Venue support | [`platforms/P12-venue-support`](platforms/P12-venue-support/README.md) | 28 | 1 | 0 | 0 |
| P13 Venue CMS | [`platforms/P13-venue-cms`](platforms/P13-venue-cms/README.md) | 103 | 25 | 0 | 0 |
| P14 Developer portal | [`platforms/P14-developer-portal`](platforms/P14-developer-portal/README.md) | 8 | 3 | 0 | 0 |
| P16 Venue analytics | [`platforms/P16-venue-analytics`](platforms/P16-venue-analytics/README.md) | 70 | 4 | 0 | 0 |
| P17 TICVAI sign-up | [`platforms/P17-ticvai-signup`](platforms/P17-ticvai-signup/README.md) | 24 | 0 | 0 | 0 |

"Block A" is the first 35 working days of the build, from Monday 5 October: the screens with a front-end task in phase 1 of `handoff/service-docs/tasks.csv`. "Client-verified" means the frame is a capture of a client-approved prototype.

## The order

Run top to bottom. Within a platform, its README gives the batch order.

### 1. Block A

1. **P13 CMS flow builder**: [`CMS-FLOW-BUILDER/`](CMS-FLOW-BUILDER/BRIEF.md). CMS-101 to CMS-104 as one flow, with the step screens they open. Then the P13 Block A batches: `P13-white-label-03`, `-01`, `-02`, `WS41`.
2. **P02 Mobile v4 changes**: see [`platforms/P02-guest-app-mobile`](platforms/P02-guest-app-mobile/README.md). First re-capture the 17 screens that are views in Mobile App v4 (a capture job, not a design batch). Then draw the 19 changed screens v4 has no view for, in the v4 look.
3. **P01 WEB-050 and the changed screens**: [`P01-discovery-browse-01`](P01-discovery-browse-01/) (WEB-050 Plan Your Visit, from the Visit Planner), then the P01 batches with changed screens. See [`platforms/P01-guest-web`](platforms/P01-guest-web/README.md).
4. **P15 kitchen display**: [`P15-kitchen-01`](P15-kitchen-01/). P04 is locked; the client-approved terminal is its design.
5. **P08 set-up screens**: the 38 P08 Block A batches, set-up screens first. See [`platforms/P08-venue-management`](platforms/P08-venue-management/README.md).
6. **The rest of Block A**: P09 (23 batches), P16 (3), P06 (2), P12 (1), P14 (1). Each platform README lists them.

### 2. B2B options

[`B2B-OPTIONS/`](B2B-OPTIONS/BRIEF.md). The reseller portal drawn two ways, POS-style and website-style, with a one-page comparison. The client chooses (MoM 29 September, section 3). The P10 batches wait for that choice.

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
