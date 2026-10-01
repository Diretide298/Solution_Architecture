Subject: TICVAI guest web and mobile app: audit fixes and offline builds

Hi Muhamed, Qossai,

Following yesterday's email, we audited the mobile app against the website and fixed every gap we found. The offline single-file builds have also been rebuilt.

WEBSITE: AT THE VENUE
- Happening now: one tab for everything in progress, including food orders, virtual queues, reserved tables, shop collections and parking. The tab shows how many are active.
- Book a table: choose a restaurant, party size, a time tonight and where to sit. Parties of six or more pay a deposit, and tables can be cancelled.
- Shop: choose to collect at the gate, at the car park kiosk, or to have it delivered home. Guests get a collection code after paying.

MOBILE APP: NOW MATCHING THE WEBSITE
- Signed-in guests go straight to payment, where they tick the terms before paying.
- Add-ons have quantity buttons, and the cart can be opened during a booking.
- The website settings for how show times appear (date first, and how many times per page) now apply to the app too.
- Kids Club asks which branch first: Al Barsha, Mirdif, Yas Island or Sharjah.
- Seat maps have zoom buttons, full screen and a view-from-your-seat preview. The theatre plan can be pinched to zoom.
- Cabanas are held for 8 minutes, with a countdown.
- Transport has multi-trip cards and saved favourite routes.
- Delivery orders warn when they are under the AED 90 minimum and show how much more qualifies for free delivery.
- The venue map gives turn-by-turn walking directions.
- Membership statements and "Download my data" are now complete screens.

BOTH
- The museum's Help me choose asks who a course is for and shows only suitable courses.
- There are two more sample transport routes: Abu Dhabi – Al Ain (E201) and Dubai – Fujairah (E700).
- Seat maps are drawn the same way on web and mobile.
- Everything added in this round is available in Arabic.

OFFLINE FILES
- The website, mobile app and visit planner each come as a single file.
- The mobile file is now 23 MB. The booking engine loads only when a booking starts.
- Booking inside the mobile file uses the website file, so keep the two in the same folder. For booking to work there, both files need to be opened from a web address rather than straight from the computer. Everything else works offline, except the street map, fonts and intro videos.

STILL NEEDED FROM YOU
- Intercity station list, fares and timetable (the new routes use sample stations and fares)
- Confirmation of cabana numbering and pricing
- Real venue photos, videos and logos

The full list of fixes is in AUDIT-29SEP.md in the WebUIRev3_28thSep package. Next up are the B2B wireframes (POS style and website style) and the HLD/LLD, as agreed.

Best regards,
Chinmay
