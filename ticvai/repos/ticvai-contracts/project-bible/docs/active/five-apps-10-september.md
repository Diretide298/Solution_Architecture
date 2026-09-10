# Five apps, decided 10 September 2026

## TICVAI Guest (`guest`)

Absorbs P01, P02, P05.

**One guest product in three shells.** Web, mobile and kiosk share 73–91% of their operations; the kiosk is the same product in a fixed frame with no keyboard, and is deliberately narrower rather than different.

## TICVAI POS (`venue-pos`)

Absorbs P04, P15.

**The kitchen display is the till, signed into differently.** Same software, same outlet, same orders — what changes is who is looking and what they may do, which is a permission, not an application.

## TICVAI Venue Staff (`venue-staff-mobile`)

Absorbs P06, P07.

**Both offline-capable, both carried rather than sat at.** They cannot fold into venue management, which is online desktop web, and they share 69% with each other.

## TICVAI Venue Management (`venue-management`)

Absorbs P08, P12, P13, P16.

**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.

## TICVAI Control (`ticvai-control`)

Absorbs P09, P10, P11, P14.

**TICVAI operates all four**, whoever signs in. The partner portal, the accreditation intake and the developer portal are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line.

## The turnstile

**The turnstile is a workflow, not an app.** An unattended gate has no operator and nobody to read a screen: the guest taps and the lane opens or does not. It is specified as a flow and a state machine — entry and exit, offline validation against locally held keys, beacon proximity for the dynamic QR, and the denial path — rather than as a platform. Its configuration surfaces already exist on venue-management (`BO-197 Turnstile & Lane Behavior`, `BO-194 Device & Gate Command Center`, `BO-168 BLE Beacon & Geofence`).
