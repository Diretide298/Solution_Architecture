TICVAI Guest Booking — handoff
Exported 29 September 2026 (web + mobile v4 + visit planner, with the 29 Sep audit fixes)

READ FIRST

  CLIENT-RESPONSE-REV3-25SEP.md       answer to every point in the rev 3.0 (25 Sep)
                                      feedback, with where to see it and which
                                      Config setting controls it
  CLIENT-RESPONSE-FEEDBACK-23SEP.md   answer to every point in the 23 Sep feedback
  DESIGN-GAP-RESPONSE-23SEP.md        what was drawn for Softlabs' gap response,
                                      plus the card-layout options they asked for
  BUILD-YOUR-EXPERIENCE.md            how a venue sets up "Build your experience"

WHAT TO OPEN

  TICVAI Guest Booking v2 (single file).html   the website
  TICVAI Mobile App v4 (single file).html      the mobile app (keep it in the same
                                               folder as the website file: booking
                                               inside the app runs the website engine)
  TICVAI Visit Planner (single file).html      the visit planner

  AUDIT-29SEP.md    mobile vs web audit, with what was fixed and where to see it
  STATUS-29SEP.md   status against the 29 September MoM

  Editable sources: TICVAI Guest Booking v2.dc.html, TICVAI Mobile App v4.dc.html,
  TICVAI Visit Planner.dc.html. They need the sibling files in this folder:
  support.js, seatzoom.js, venueplan.js, stadium3d.js, venuemap3d.js,
  ticvai-ar*.js, images/, logos/.

  Online only: the street map tiles, fonts and the Pexels intro videos.
  Browsers stop one local file from reading another, so booking inside the
  mobile single file works when both files are served from a web address
  (any static host). Everything else in the app works from the desktop.

FOLDER CONTENTS

  images/            all photography, mascot art, tier art and clips
  images/lib/        the venue photo library (park, water, stadium,
                     theatre, dining, kids)
  images/shop/       square product shots for extras and retail
  logos/             white-label client logos
  support.js         the component runtime
  venueplan.js       2D venue plan renderer
  venuemap3d.js      3D venue map
  stadium3d.js       3D stadium bowl and seat picker

THE FETCHED PHOTO SET

  The design is already wired to a second, larger photo set — around 50
  library photos, 16 shop squares and 13 clips — under the same
  images/lib, images/shop and images/clips paths. Those files are not in
  this zip because they have not been sourced yet.

  Until they exist, every slot falls back to the photography included here,
  so nothing is broken. Once the files are dropped in, switch on
  "Use fetched photo set" at the top of MARKETING LAYER in the
  configuration drawer and the design picks them up with no code changes.

ALSO INCLUDED

  TICVAI Engine Controls Manual.dc.html   every Config / Tweaks control explained
  ASSETS-NEEDED.md                        photos and media still to supply
                                          (incl. images/lib/stadium-football.jpg)
  ticvai-ar.js                            Arabic interface layer used by the
                                          language switch (web + mobile)
  ticvai-ar-29sep.js                      Arabic for strings added on 29 Sep
