# Client email draft, 30 September 2026

> **Status:** Draft for Chinmay to review and send. Attach `TICVAI - Build Readiness.xlsx` and `TICVAI - Decisions Register.xlsx`. No points or internal names go to the client.

---

**Subject:** TICVAI: 29 September changes applied, and the questions we need answered

Dear Muhamed, dear Qossai,

Thank you for yesterday's session. Everything we agreed is now in the specification, and development starts on Monday 5 October.

**What we applied from 29 September**
- Website W1 to W12: guest checkout asks only the fields you configure, seat maps open by section, view-only products show "contact sales", Help me choose filters the products, surf and workshop flows put the right step first, and meeting rooms check date, start time and duration together with a configurable cleaning buffer.
- The mobile app redesign: Home, Explore, Plan and Tickets, with Buy tickets on every screen, item pages with the map and the right product, an optional intro video, and the trip planner in the first release.
- The content system becomes step-based: a venue picks its booking flows, sees which steps are required, sets its own order, and finishes with header, footer, logos, banners and theme.
- Every AI feature is built within the six months. Each works from the first day and becomes more accurate as the venue's own data grows.

**What we need from you**
1. E-invoicing: your accredited provider, the date your mandate applies, whether B2C invoices are in the first phase, and the VAT 201 layout you file.
2. Guest checkout: whether ticking marketing consent during a guest checkout counts as consent for you. Until you confirm, the box is shown unticked.
3. Availability: which services the 99.99% commitment covers.
4. Biometrics: where face templates may be stored and how long they are kept (for your data protection officer).
5. App stores: an Apple Developer account (with a D-U-N-S number) and a Google Play account for each client.
6. Still open from earlier: intercity stations, fares and timetable; cabana numbering and prices; real venue photos and videos; the Stripe and Network International sandbox credentials with the name of your finance or payments owner; and the name of your design reviewer, who signs off each wireframe batch within 3 working days.
7. The B2B portal: we are drawing both options (POS-style and website-style) and will share them for your choice.
8. The cloud event broker: RabbitMQ or Kafka. Every sale reaches ticketing, the ledger and stock through it, so it must keep each order's events in sequence, set aside messages that fail, and run in the UAE. We recommend RabbitMQ, ideally as a managed service in the Azure UAE North region if one is available: it fits this workload, it is simpler to run, and venues on their own premises use it anyway. Kafka is the better choice only if you want to replay past events from the broker itself. We are building on RabbitMQ behind one interface, so either answer works; we need it by 12 October so the first purchase can be proven end to end by 23 October.
9. Hardware and suppliers your lists do not name yet. The most urgent, because the first release needs them: the POS terminal (make, model and operating system), the kitchen display screens and printers, the card payment terminals, and the SMS and email senders that deliver tickets. Also: the NFC readers and wristband chip type, the devices for the staff app and the flying POS, the accounting system that receives postings, UAE Pass registration, the Apple and Google Wallet certificates, any tourism-authority reporting, and whether parking, sensors, game readers, lockers, signage and the named services (Digonex, Go City, Gantner, Metra) are in scope. Each is in the Decisions Register with what we build until you answer.

The attached Decisions Register lists every decision we took and how, with our default for each open question. Where you agree with the default, no reply is needed.

Kind regards,
Chinmay
