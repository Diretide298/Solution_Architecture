# Design reply to "Response to the Guest Booking design gaps" (Softlabs, 23 Sep)

What the web prototype (`TICVAI Guest Booking.dc.html`) now shows. Each check opens as a panel at the step named. A dashed "Preview state" row in each panel lets reviewers jump straight to any state.

## 1. Guest checkout, code proof, profile matching (WEB-012)
- Config → Steps & cards → **Guest checkout (code proof)**. Off by default.
- **Off:** at payment, a guest who isn't signed in gets the sign-in screen: "This venue requires an account for checkout. Your basket is kept." After signing in, the booking continues on its own. The guest button is hidden.
- **On:** "Continue as guest" asks for an email or mobile (following **Match returning guests by**) and sends a code. Only exactly six digits are accepted, and the copy says six.
- After the code, the match prompt shows what matched, 4 past orders, first order 12 Mar 2024 and profile type. It never shows the other profile's name or details.
- Its buttons are "Use this profile" and "Not me – keep separate". The answer is recorded either way.
- Expired state: "This match has expired – continue as a new guest."

## 2. Billing statement and payment retry (WEB-023)
- Account → Membership → **Billing statement** shows a line-by-line statement.
- **Soft decline:** Retry now + Use another card.
- **Hard decline:** Use another card only.
- **Declined again:** Use another card, with the next automatic retry date.
- **Paid:** "Your membership continues".
- Use another card lists the saved cards and charges the new one.

## 3. Height and age check (WEB-006)
- Runs on leaving the selection step in:
  - Summit Peaks eligibility flow (Freefall Tower)
  - Coastal Aqua day pass (Tidal Drop slide)
  - Kids club play, zone, workshop and camp flows
- For each person the guest declares an age band and a height band. Toggles appear only where needed: confident swimmer, and guardian signature for ages 12–15.
- Per person it shows "Can't take part: too short, needs an adult" and similar, with **Remove this guest**. **Choose another activity** returns to the start.
- Continue stays locked until everyone qualifies.
- The kids club gate reads the age range from the chosen pass (e.g. Junior pass, ages 1–4). Adults are exempt. Under-8s need an adult in the party.

## 4. School trips and parties (WEB-031)
Runs at the payment step of Explorers → School trip / Birthday party.
- **School trip**
  - Pupil stepper.
  - One free teacher or assistant per 10 pupils.
  - Invoice estimate.
  - "Requested – quote on its way" confirmation, with the quote date two working days out and the headcount due 5 days before.
- **Party**
  - Birthday child's name and the age they're turning.
  - Title: "Pay deposit AED X now, AED Y on the day". The deposit is AED 100 per AED 400 of the total, refundable up to 24 hours before.
- **Both**
  - "More participants than the package allows": the cap is taken from "Up to N" on the package.
  - "Date no longer available".

## 5. Takeaway and delivery (WEB-036)
- Runs on leaving the menu step of Dining → Delivery / Takeaway.
- **Delivery**
  - The basket shows the delivery fee (AED 15, free from AED 200) and "Add AED X more for free delivery".
  - Below AED 90 checkout is **refused**.
  - Any emirate other than Dubai gets "We don't deliver to this address", with Change address / Switch to takeaway.
- **Open slots can close.** The first time a guest continues with the second slot, it disappears and "That time just filled" asks for another time.

## 6. Booking-flow configuration (CMS-016): card-layout options
The field doesn't need to be free text. The options are:
- **Card layout:** Stacked rows · Split rows · Cards across · Poster cards
- **Card size:** Compact · Standard · Large · Extra large
- **Category display:** Grid · Row strip
