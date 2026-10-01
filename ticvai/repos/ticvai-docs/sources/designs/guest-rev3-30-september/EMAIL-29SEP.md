Subject: TICVAI guest web and mobile app: 29 September workshop changes

Hi Muhamed, Qossai,

Following our workshop on 29 September, here are the revised builds.

WEBSITE (Guest Booking v2)
- Guest checkout asks only the fields you configure. After the code there's just the terms, with no re-entry. Signed-in users skip the details step completely.
- Seat maps: tapping a zone zooms into it and shows its seats in place. Full screen and zoom in/out buttons are included.
- View-only products (e.g. training courses) show Call sales and Email sales instead of a Book button.
- Help me choose now filters the products. The surf assessment asks about swimming ability, interests and experience, then shows only suitable sessions.
- Surf products appear only after a time slot is chosen. Workshops ask for the workshop before the date.
- Meeting rooms are checked against date, start time and length together, with a configurable cleaning buffer: after every booking, or a set number per day.
- Cabana booking uses the real park map with all 34 huts.
- The date picker shows the next seven days, with a calendar for later dates.
- A visit planner is built into the site. "Book this plan" goes straight into booking.
- The retired "Category display" setting has been removed.

MOBILE APP (v4, rebuilt)
- Each venue opens as its own branded app with its own sign-in: colours, fonts, hero, tab style, animations and mascot.
- Tabs: Home, Explore, Map, Buy tickets and Tickets. The layout can be changed.
- The home and venue overview is photo- and video-led. Explore has search and inline video previews.
- Every web product and flow is bookable in the app, each with its own step order. It includes 2D and 3D stadium seating with zoom, the theatre plan, the cabana map and the bus route map.
- At the venue:
  - Live 3D map with walking directions, ride waits and a virtual queue.
  - Show reminders, food ordering with order tracking, and table reservations.
  - A shop with collect-at-gate, plus services (lockers, photo pass, find my car and more).
- Cart, save-and-resume bookings, and a "Happening now" panel for live orders and queues.
- Tickets have a type for each booking flow and a QR code that refreshes every 30 seconds. They can be added to a wallet or calendar, sent to someone, or refunded.
- The planner builds a day-by-day plan and lets you swap, remove and add items.
- Arabic (right to left) is available from Settings.
- A configuration panel next to the phone covers themes, sizes, layout, booking style, maps and language.

INPUTS NEEDED FROM YOU
- Intercity station list, fares and timetable
- Confirmation of cabana numbering and pricing
- Real venue photos, videos and logos to replace the stand-ins

NEXT STEPS
- Full functionality audit of mobile against web, and fixes
- At-venue additions on the website
- Offline single-file builds
- B2B wireframes (POS style and website style) and HLD/LLD, as agreed

Files are in the WebUIRev3_28thSep package. Happy to walk through it on tomorrow's tracker call.

Best regards,
Chinmay
