TICVAI Guest Booking — handoff
Exported 27 September 2026 (complete handoff: web + mobile + docs, incl. rev 3 feedback)

READ FIRST

  CLIENT-RESPONSE-REV3-25SEP.md       answer to every point in the rev 3.0 (25 Sep)
                                      feedback, with where to see it and which
                                      Config setting controls it
  CLIENT-RESPONSE-FEEDBACK-23SEP.md   answer to every point in the 23 Sep feedback
  DESIGN-GAP-RESPONSE-23SEP.md        what was drawn for Softlabs' gap response,
                                      plus the card-layout options they asked for
  BUILD-YOUR-EXPERIENCE.md            how a venue sets up "Build your experience"

WHAT TO OPEN

  TICVAI Guest Booking v2 (single file).html
  TICVAI Guest Booking Mobile v2 (single file).html
      The rev 3 versions, self-contained. New settings are under
      Config -> Booking rules (Rev 3). New venues: Tidewater Museum,
      House of Pages (rooms and experiences), Emirates Link (transport).
      Mobile rev 3 screens: Account -> All screens -> Rev 3 feedback.

  TICVAI Guest Booking v2.dc.html / TICVAI Guest Booking Mobile v2.dc.html
      Editable rev 3 sources (same sibling files as below).

  The editable sources need the sibling files in this folder to run:
  support.js, venueplan.js, stadium3d.js, venuemap3d.js, MobileTabBar.dc.html,
  images/, logos/. The single-file versions need nothing else.

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
