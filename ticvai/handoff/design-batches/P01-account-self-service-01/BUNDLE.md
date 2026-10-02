# P01-account-self-service-01 — P01 · Account & Self-Service

**5 screens · 46 operations · 47 schemas · 7 permissions**

Platform P01 Guest Web · ships as **guest** ·
guest audience · web ·
online only

## Who this is for

**guest on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `BUNDLE.md` | **The one file to hand a design session.** This brief; then **Screen by screen**, a full specification of each screen (what the user enters and picks, what it shows and produces, every state, who may do what, the requirements it meets, what the client said about it in the meetings, the tracker items, what the tenant configures, the references and an acceptance checklist); then what applies to the whole batch; then the raw data. |
| `screens.json` | Every field of every screen in the batch, as the package holds it. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 7 permissions apply here:
  `GUEST_MANAGE, GUEST_VIEW, LEDGER_POST, LEDGER_VIEW, MARKETING_VIEW, ORDER_MODIFY, ORDER_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **This shell is online only.** None of these operations is served offline here, whatever it can do on a shell that keeps a store. Offline, a screen shows what was already loaded, under the banner below.
- **Offline, every screen shows one banner, the same on web and app:** *"You're offline. Connect to the internet to book, pay, order or join a queue."* The moment the connection drops, on every screen, above the screen's own content. By itself as soon as the connection is back, with a short "Back online" confirmation. **It never** Covers what is already on screen, or appears for a server error — that is the screen's own error state, and a guest told they are offline when the venue is down reconnects for nothing. Each screen's `states.offline` says what stays on screen and what waits.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.
- **How input should be, how output should be.** Each screen's block in `BUNDLE.md` says, field by
  field, the control, whether it is required, its default, its limits and allowed values, its format
  and its error; and, element by element, what is shown and in what format, what each action
  produces and where the user goes next. Draw exactly that.

## The screens

Each has a full block in `BUNDLE.md` (*Screen by screen*). Inputs and outputs count fields; requirements are matrix rows; meeting inputs are the ones naming the screen (the module and platform ones are below); white label says whether the tenant's brand reaches it (guest) or it sets the brand (configures).

| id | name | block | inputs | outputs | states | requirements | meeting inputs | tracker | white label | wireframe |
|---|---|---|---|---|---|---|---|---|---|---|
| `WEB-016` | Login / Register | A | 36 | 6 | 6 | 15 | 11 | 0 | guest | review (client-verified) |
| `WEB-017` | My Account Dashboard | A | 17 | 42 | 6 | 31 | 1 | 0 | guest | review (client-verified) |
| `WEB-018` | My Tickets | A | 11 | 55 | 6 | 8 | 8 | 0 | guest | review (client-verified) |
| `WEB-019` | Order History | A | 4 | 16 | 6 | 15 | 2 | 0 | guest | review (client-verified) |
| `WEB-020` | Profile & Preferences | A | 20 | 47 | 6 | 18 | 0 | 0 | guest | review (client-verified) |

---

## Screen by screen

**One block per screen, in the order to build them.** Each says what the user enters (every control, with its rules), what the screen shows and produces (every field, with its format; every action, with what it returns and the errors to draw), every state, who may do what, the requirements it meets, what the client said about it, the tracker items, what the tenant configures, the references, and an acceptance checklist. **Everything in a block is for you, never for the screen**: no id, field name, operation or permission key may appear as text.

### `WEB-016` Login / Register

**Get a guest into the site, fast, on a device that may be shared: a one-time code to the email or mobile, a password, Apple or Google, or UAE Pass, or register a new account. **No enterprise SSO for guests** (decided 28 September, audit R167, first part). **A second factor only where the venue enabled guest two-step verification** (decided 29 September, rev 3 GAP-B1, per venue, superseding the second part of R167).**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17990 (APP-WEB-WEB-016) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025); in the flows as guest |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | form (compact density): **A sign-in form, not a list.** Four ways in (a one-time code, a password, Apple or Google, UAE Pass) and a way to register; `getGuestSession` is the one piece of context. Rebuilt 28 September: the … |
| Offline | **Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server. |
| Opens with | `cartId` (session), `challengeId` (navigation), `subjectId` (navigation) · cold entry: **Needs nothing.** A guest arriving cold signs in and goes to My Account; one sent from the cart carries `cartId` and goes back to it. The SSO deep-link … |
| Route | `/account-and-self-service/login-register` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Corrected 24 August**: removed getCurrentSession, logout, selectRole. **A guest surface has no roles to select and its own logout** — `selectRole` is ADR-0002 staff authorisation and `getCurrentSession` is the staff session. `guestLogout` and `getGuestSession` are the equivalents and both already existed. **The screen was calling the staff identity surface because nothing checked that a guest platform only calls guest operations.** **Rebuilt 28 September as a guest sign-in form** (decided 28 September, audit R167, R073 (a)): removed `login`, `startSsoAuthorization`, `completeSsoAuthorization`, `listSsoProviders` and the six MFA operations — guests have no enterprise SSO. **The second factor came back on 29 September, per venue** (see below). Password sign-in is `guestPasswordLogin`. **Rev 3 (decided 29 September).** **Guest two-step verification is a per-venue setting, off by default** (GAP-B1, per venue, `VenueSettings.identity.guestTwoStep`; supersedes the second part of audit R167, *no guest MFA*; the first part, no enterprise SSO for guests, stands). The prompt appears only when the guest signs in at, or acts at, a venue that has it on; enrolment is on the guest's account (WEB-024). **Sign-in gate (REV3-3):** this screen is where WEB-008 (after add-ons) or WEB-012 (at payment) sends a guest who is not signed in, and it returns them to the cart with the basket kept; a guest code is offered instead when guest checkout is on (`FeatureToggle guestCheckout`, off by default; match …

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Email or mobile number | text field | — | — | — | — | **Guest checkout asks only the configured fields** (W1): `BookingFlowSettings.guestContactFields` (email, mobile, name). | — |
| Code | text field | — | — | — | — | Shown once a code has been sent; `verifyGuestOtp` returns the `GuestSession`. | — |
| Password | text field | — | — | — | — | **Password sign-in** (decided 28 September, audit R073 (a)): sends `identifier`, `password` and the device's `deviceId` to `guestPasswordLogin`, which returns the same `GuestSession`. A wrong … | — |
| Verification code | text field | — | — | — | — | **Only when the returned `GuestSession` has `requiresMfa`**, which happens only at a venue whose `VenueSettings.identity.guestTwoStep.enabled` is on and only for a guest who enrolled a method (the … | — |

**Form: Create an account** (modal, opened by *Create an account*; *Register guest* calls `registerGuest`, *Cancel* sends nothing)

**Collects what `registerGuest` sends before it is called.** Required: `identifier`, `channel`. Optional: `displayName`, `password`, `preferredLanguage`, `consents`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | Email address or mobile number in E.164. | `registerGuest` body |
| Channel `channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `registerGuest` body |
| Display name `displayName` | text field | optional | — | max length 200 | — | — | `registerGuest` body |
| Password `password` | text area | optional | — | min length 8; max length 256 | — | Optional. OTP-only accounts are supported and are the default. | `registerGuest` body |
| Preferred language `preferredLanguage` | language picker | optional | — | — | ISO 639-1 code, shown as the language name | — | `registerGuest` body |
| Consents `consents` | repeatable rows | optional | — | — | — | Consent captured at registration, recorded with the notice version. | `registerGuest` body |
| Purpose `consents[].purpose` | text field | optional | — | — | — | — | `registerGuest` body |
| Granted `consents[].granted` | toggle | optional | — | — | — | — | `registerGuest` body |
| Notice version `consents[].noticeVersion` | text field | optional | — | — | — | — | `registerGuest` body |

Errors to draw in the form: 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account …

**Form: Sign in with password** (modal, opened by *Sign in with password*; *Sign in* calls `guestPasswordLogin`, *Cancel* sends nothing)

**Collects what `guestPasswordLogin` sends before it is called.** Required: `identifier`, `password`. Optional: `deviceId` (sent by the client, not typed). A 401 is one message whatever the cause; a 429 or a locked account says to try again later or use a one-time code instead (decided 28 September, audit R073 (a)). Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | The email address or E.164 mobile number the account was registered with. | `guestPasswordLogin` body |
| Password `password` | text area | required | — | min length 8; max length 256 | — | — | `guestPasswordLogin` body |
| Device `deviceId` | text field | optional | — | — | — | Names the device; a new sign-in here ends the previous session on it. | `guestPasswordLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestPasswordLogin` body |

Errors to draw in the form: 400 Validation failed

**Form: Continue with Apple or Google** (modal, opened by *Continue with Apple or Google*; *Guest social login* calls `guestSocialLogin`, *Cancel* sends nothing)

**Collects what `guestSocialLogin` sends before it is called.** Required: `provider`, `idToken`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Provider `provider` | segmented control | required | — | Apple · Google | — | — | `guestSocialLogin` body |
| ID token `idToken` | text field | required | — | — | — | — | `guestSocialLogin` body |
| Device `deviceId` | text field | optional | — | — | — | — | `guestSocialLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestSocialLogin` body |

**Form: Continue with UAE Pass** (modal, opened by *Continue with UAE Pass*; *Guest uae pass login* calls `guestUaePassLogin`, *Cancel* sends nothing)

**Collects what `guestUaePassLogin` sends before it is called.** Required: `code`, `redirectUri`. Optional: `state`, `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Code `code` | text field | required | — | — | — | — | `guestUaePassLogin` body |
| Redirect URI `redirectUri` | text field | required | — | — | — | — | `guestUaePassLogin` body |
| State `state` | text field | optional | — | — | — | — | `guestUaePassLogin` body |
| Device `deviceId` | text field | optional | — | — | — | — | `guestUaePassLogin` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `guestUaePassLogin` body |

**Form: Link an order I placed as a guest** (modal, opened by *Link an order I placed as a guest*; *Link guest checkout* calls `linkGuestCheckout`, *Cancel* sends nothing)

**Collects what `linkGuestCheckout` sends before it is called.** Required: `orderReference`. Optional: `verificationCode`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order reference `orderReference` | text field | required | — | — | — | — | `linkGuestCheckout` body |
| Verification code `verificationCode` | text field | optional | — | — | — | From the booking confirmation. Proves possession of the booking. | `linkGuestCheckout` body |

Errors to draw in the form: 403 Contact detail on the order does not match the verified identifier

**Form: Refresh token** (modal, opened by *Refresh token*; *Refresh token* calls `refreshToken`, *Cancel* sends nothing)

**Collects what `refreshToken` sends before it is called.** Required: `refreshToken`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Refresh token `refreshToken` | text field | required | — | — | — | — | `refreshToken` body |

**Form: Send me a code** (modal, opened by *Send me a code*; *Request guest OTP* calls `requestGuestOtp`, *Cancel* sends nothing)

**Collects what `requestGuestOtp` sends before it is called.** Required: `identifier`, `channel`. Optional: `purpose`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text area | required | — | max length 256 | — | — | `requestGuestOtp` body |
| Channel `channel` | segmented control | required | — | Whatsapp · SMS · Email | — | — | `requestGuestOtp` body |
| Purpose `purpose` | radio group | optional | Login | Login · Register · Verify · Password reset · Step up | — | — | `requestGuestOtp` body |

**Form: Sign in with the code** (modal, opened by *Sign in with the code*; *Verify guest OTP* calls `verifyGuestOtp`, *Cancel* sends nothing)

**Collects what `verifyGuestOtp` sends before it is called.** Required: `identifier`, `code`. Optional: `deviceId`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Identifier `identifier` | text field | required | — | — | — | — | `verifyGuestOtp` body |
| Code `code` | text field | required | — | min length 4; max length 10 | — | — | `verifyGuestOtp` body |
| Device `deviceId` | text field | optional | — | — | — | — | `verifyGuestOtp` body |
| Venue `venueId` | picker: choose a venue | optional | — | — | shows names, sends the id | The venue the guest app or booking is in. Identity reads that venue's `VenueSettings.identity.guestTwoStep` to decide whether a second factor is asked (decided 29 September, rev 3 … | `verifyGuestOtp` body |

#### Outputs: what the screen shows and produces

**Shown**

**Who is signed in on this device** (detail panel, from `getGuestSession`): Shown only when a guest session already exists on this device, with a way to sign out so a shared device is handed over clean.

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Display name | text | — |
| Is verified | yes / no (icon or chip) | False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact … |
| Identity providers | list or chips (count when long) | Linked providers. Several may resolve to one account. |
| Preferred language | text | — |
| Expires at | 1 Oct 2026, 14:30 | 30 days, sliding (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Send me a code (primary button) | `requestGuestOtp` POST `/auth/guest/otp` | inline | inline | — | opens modal first |
| Sign in with the code (primary button) | `verifyGuestOtp` POST `/auth/guest/otp/verify` | inline | GuestSession | — | opens modal first |
| Sign in with password (secondary button) | `guestPasswordLogin` POST `/auth/guest/password` | inline | GuestSession | 400 Validation failed | opens modal first; produces a document or message: Sign in with an email or mobile and a password |
| Continue with Apple or Google (secondary button) | `guestSocialLogin` POST `/auth/guest/social` | inline | GuestSession | — | opens modal first |
| Continue with UAE Pass (secondary button) | `guestUaePassLogin` POST `/auth/guest/uae-pass` | inline | GuestSession | — | opens modal first |
| Create an account (secondary button) | `registerGuest` POST `/auth/guest/register` | RegisterGuestRequest | GuestSession | 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account … | opens modal first |
| Sign out (secondary button) | `guestLogout` DELETE `/auth/guest/session` | — | — | — | — |
| Link an order I placed as a guest (secondary button) | `linkGuestCheckout` POST `/auth/guest/link-checkout` | inline | inline | 403 Contact detail on the order does not match the verified identifier | opens modal first |
| Keep my cart (secondary button) | `claimCart` POST `/carts/{cartId}/claim` | — | CartMergeResult | — | — |
| Refresh token (secondary button) | `refreshToken` POST `/auth/refresh` | inline | TokenPair | — | opens modal first |

**Data it reads**: `getGuestSession` (onLoad, Read the current guest session Only when signed in (decided …)

**Where the user goes next**

- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*
- → `WEB-019` Order History: *Order History*
- → `WEB-010` Shopping Cart: *Signed in and verified — back to the cart*; carries `cartId`; only when arrived from the cart
- → `WEB-011` Guest Details & Attendee Forms: *Guest Details & Attendee Forms*
- → `WEB-012` Checkout — Payment: *Checkout — Payment*
- → `GST-039` Profile: *They set a profile*; carries `subjectId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Checking whether this device already holds a guest session. The sign-in form stays visible. |
| Error (`?state=error`) | Identity could not be reached. **Says so rather than saying the password or code is wrong**, and keeps what was typed. |
| Empty, first run (`?state=emptyFirstRun`) | **Nobody signed in on this device** — the normal state. The form offers a code, a password, Apple or Google and UAE Pass, and Create an account (`registerGuest`). |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in. |
| Sign in refused (`?state=signInRefused`) | **One message for every refusal of a password sign-in**: `guestPasswordLogin` answers 401 alike for a wrong password, an unknown identifier, an account with no password and a locked account, and the screen never says which. Too many attempts (429, or the lockout after `PasswordPolicy.lockoutAfterAttempts`) says to try again later and offers **Send me a code** instead (decided 28 September, audit R073 (a)). |
| Offline (`?state=offline`) | **Not available, and the offline banner says why.** Signing in, registering and verifying a code need the server. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Validation failed; 409 Identifier already registered. Deliberately indistinguishable in timing from success — a registration endpoint that reveals which addresses exist is an account …; 409 The key is already claimed by another subject (`already-claimed`) |

#### Permissions

- `registerGuest` → no permission · anonymous
- `getGuestSession` → no permission · guest
- `guestLogout` → no permission · guest
- `guestPasswordLogin` → no permission · anonymous
- `guestSocialLogin` → no permission · anonymous
- `guestUaePassLogin` → no permission · anonymous
- `linkGuestCheckout` → no permission · guest
- `refreshToken` → no permission · staff, partner, guest
- `requestGuestOtp` → no permission · anonymous
- `verifyGuestOtp` → no permission · anonymous
- `claimCart` → no permission · guest
- `createMfaChallenge` → no permission · staff, partner, guest
- `verifyMfaChallenge` → no permission · staff, partner, guest
- `claimDeviceConsent` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025), and this is the screen a guest who is not signed in is sent to, so it has no no-access case of its own. A session that has expired lands here with the screen it came from kept, and returns to it after sign-in.

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.1 | User Registration - System shall support user registration. | Guest Mobile App & Branding | CONTRACTED | `registerGuest` |
| 2.6.20 | - Single Sign On Registration | Ticketing Sales | CONTRACTED | `registerGuest` |
| 2.6.28 | A online sale can be done using Guest Checkout or Registration on the website or Login to SSO. This should be configurable per site based on the client requirements. | Ticketing Sales | CONTRACTED | `registerGuest` |
| 19.2.2 | User Login - System shall support user login. | Guest Mobile App & Branding | CONTRACTED | `getGuestSession` |
| 2.6.29 | If the customers require to have access to this account, this account shall have a login and password in order to recall previous transactions. | Ticketing Sales | CONTRACTED | `getGuestSession` |
| 19.2.3 | Social Login - System shall support social login. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 19.2.4 | Apple Login - System shall support Apple Sign-In. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 19.2.5 | Google Login - System shall support Google Sign-In. | Guest Mobile App & Branding | CONTRACTED | `guestSocialLogin` |
| 5.3.6 | The system should allow linking of guest accounts with social media logins. | F&B & Guest Management | CONTRACTED | `guestSocialLogin` |
| 2.6.66 | Customer should be able to login through UAE Pass and all the customer details should be captured and saved as profile information | Ticketing Sales | CONTRACTED | `guestUaePassLogin` |
| 2.6.67 | B2C Ticketing website should support the following: - Guest Checkout - Loing through Apple ID - Login through Google ID - Login through UAE Pass - Login through SSO - Login through Registered Account | Ticketing Sales | CONTRACTED | `guestUaePassLogin` |
| 5.3.3 | The system should be able to accept checkout for guests that do not wish to create an account in order to complete an order. Minimum required information as configured (e.g. email address) will still … | F&B & Guest Management | CONTRACTED | `linkGuestCheckout` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Guest two-step verification is a per-venue setting, off by default. Enrolment lives on the guest's tenant-wide account; the second factor is asked only when signing in or acting at a venue that enables it. Guests never see enterprise SSO. *(agreed · design review 29 Sep 2026, GAP-B1 · B. Login: set up two-step verification; C. Security & Sign-in (step-up auth) · DI-1072)*
- Sign-in (or the guest code when guest checkout is on) is asked when the guest leaves the Add-ons step; the basket is kept. Setting "Ask to sign in": After add-ons (default) or At payment. *(agreed · rev 3 design review 29 Sep 2026, REV3-3 · 3. The sign-in screen should appear after Add-ons · DI-1043)*
- After the code, a match prompt shows what matched (e.g. 4 past orders, first order 12 Mar 2024, profile type), never the other profile's name or details, with "Use this profile" / "Not me – keep separate". Expired state: "This match has expired – continue as a new guest." *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1035)*
- Guest checkout is a venue toggle, off by default: off = sign-in screen at payment ("This venue requires an account for checkout. Your basket is kept."), guest button hidden. On = "Continue as guest" with email or mobile (per "Match returning guests by") and a code; only exactly six digits accepted, copy says six. *(agreed · design review 29 Sep 2026, 1. Guest checkout, code proof, profile matching (WEB-012) · DI-1034)*
- The guest-checkout email pop-up collects only the fields configured in the back end (email, phone and/or name). After the code is verified, do not ask for name/email/phone again: go straight to T&Cs and complete the booking; profile is created and can be completed later (Platinumlist pattern). *(agreed · MoM 29 Sep 2026, 1. Website (B2C) — review of Rev 3, W1 Guest checkout · DI-1002)*
- At checkout guests can sign in, register (with a visible loyalty-points incentive) or continue as guest; terms acceptance is implied by proceeding to payment, with no separate checkbox. *(client request · MoM 31 Aug 2026, 4.13 UX Reference Walkthrough (Little Explorer) · DI-588)*
- Decision: at least one of e-mail or mobile number is mandatory at profile creation (not both — some customers decline e-mail); the system supports conditional "either/or" mandatory-field rules. *(agreed · MoM 20 Aug 2026, 4.1 CRM; 5. Key Decisions · DI-372)*
- Sign-up by phone number or email, verified by OTP (WhatsApp or SMS/email as configured), then minimal profile (first/last name). *(client request · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-209)*
- UAE Pass login: customer enters mobile number, approves a push notification, confirms with biometrics; verified personal details are pulled into the booking automatically and a linked account is created. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-123)*
- Checkout supports guest checkout, registered-account checkout, and single sign-on (e.g. Okta, Azure AD, a ticketing-specific SSO). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-121)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Booking settings (tenant, with per-venue overrides)*, set in `CMS-016` Site Settings:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Guest contact fields (`bookingFlow.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |
| Settings: guest contact fields (`bookingFlow.venueOverrides[].settings.guestContactFields`) | Email · Mobile · Name; at least 1; at most 3; no duplicates; Must include the contact the guest's code is sent to and matched on (identity `GuestMatchPolicy.; matchBy`), or 400. | Email | What the guest-checkout pop-up asks, and nothing else (decided 29 September, W1). |

*Cookie banner*, set in `CMS-026` Cookie Banner & Preference Center Designer:

| Setting | Allowed values | Default | What it changes here |
|---|---|---|---|
| Buttons: action (`cookieBanner.buttons[].action`) | Accept all · Reject non essential · Manage preferences · Save preferences · Do not sell or share | — | — |

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-016` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Header profile icon (signed out), or automatically when leaving Add-ons / at payment*. Differences: No password sign-in and no mobile-number OTP (YAML has guestPasswordLogin and 'Email or mobile number'); it is a modal, not a page. Account → Security still shows 'Two-step verification' and passkeys, which the YAML ruled out for guests (R167). Guest checkout route belongs to WEB-012 in the prototype.
- Flow F56 *A guest registers, verifies and sets preferences*, step 3: A guest who checked out anonymously links their order. → **This is the operation that stops duplicates.** A guest who bought without an account and registers afterwards is one person — and without this they are two, which is what `mergeGuests` then has to …
- Flow F01 branch at step 4 (recoverable): when The guest is not signed in and leaves the ticket step (or Add-ons, where the booking has one), With the published flow's `settings.signInAt` `afterAddOns` (the default; read with `getPublishedBookingFlow`, W12) the guest is asked to sign in, or for a guest code when guest checkout is on …
- Flow F01 branch at step 4 (recoverable): when The guest checks out as a guest (guest checkout on for the venue), The pop-up asks only `BookingFlowSettings.guestContactFields` (email, and name or mobile where configured), then the six-digit code. After the code nothing is asked again: the cart goes to WEB-012 …
- Flow F56 branch at step 3 (high): when The anonymous order cannot be matched., **Left unlinked rather than guessed.** Linking the wrong order gives a stranger somebody else’s ticket.
- ADR-0002 *Authorisation is user-driven, not workstation-driven* (`docs/adr/0002-authorisation-is-user-driven-not-workstation-driven.md`)
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (36), with its required mark, default, format and its error state (400, 403, 404, 409).
- [ ] Every output is drawn (6 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-016?state=<state>`: loading, error, emptyFirstRun, emptyNoAccess, signInRefused, offline.
- [ ] Every action is wired with its success and its failure: Send me a code, Sign in with the code, Sign in with password, Continue with Apple or Google, Continue with UAE Pass, Create an account, Sign out, Link an order I placed as a guest, Keep my cart, Refresh token.
- [ ] Every transition is wired: `WEB-017`, `WEB-018`, `WEB-019`, `WEB-010`, `WEB-011`, `WEB-012`, `GST-039`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 11 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-017` My Account Dashboard

**The screen this app sits on. Everything else is entered from here and returns to it.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #17991 (APP-WEB-WEB-017) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listGuestDevices` reads the population and `getWishlist` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `deviceId` (deepLink), `itemId` (deepLink), `subjectId` (session), `token` (deepLink) · cold entry: **A guest arriving cold on a link that no longer resolves is shown what happened and one way onward — never a 404.** A shared ticket, a forwarded confirmation … |
| Route | `/account-and-self-service/my-account-dashboard` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **Drawn 26 August** — `Dashboards Board` frame `web-017`. **One board draws five dashboards across five platforms** — platform admin, partner, support, guest web and cross-tenant health. A dashboard is a shape rather than a domain, and the pack recognised that before the package did.

#### Inputs: what the user enters or picks

**Form: Respond to invitation** (modal, opened by *Respond to invitation*; *Respond to invitation* calls `respondToInvitation`, *Cancel* sends nothing)

**Collects what `respondToInvitation` sends before it is called.** Required: `response`. Optional: `plusOnes`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Response `response` | segmented control | required | — | Accept · Decline | — | — | `respondToInvitation` body |
| Plus ones `plusOnes` | number field | optional | 0 | — | — | — | `respondToInvitation` body |

Errors to draw in the form: 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem)

**Form: Add to wishlist** (modal, opened by *Add to wishlist*; *Add to wishlist* calls `addToWishlist`, *Cancel* sends nothing)

**Collects what `addToWishlist` sends before it is called.** Required: `variantId`. Optional: `performanceId`, `note`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Variant `variantId` | picker: choose a variant | required | — | — | shows names, sends the id | — | `addToWishlist` body |
| Performance `performanceId` | picker: choose a performance | optional | — | — | shows names, sends the id | Saving a specific date rather than the product generally. | `addToWishlist` body |
| Note `note` | text area | optional | — | max length 200 | — | — | `addToWishlist` body |

Errors to draw in the form: 404 Variant not found or not sellable in this venue

**Form: Record consent** (modal, opened by *Record consent*; *Record consent* calls `recordConsent`, *Cancel* sends nothing)

**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purpose `purpose` | select | required | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `recordConsent` body |
| Decision `decision` | segmented control | required | — | Granted · Withdrawn · Not asked | — | — | `recordConsent` body |
| Channels `channels` | multi-select chips | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Omit to apply to every channel the purpose covers. | `recordConsent` body |
| Notice version `noticeVersion` | text field | required | — | — | — | — | `recordConsent` body |
| Source `source` | select | required | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | — | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents` … | `recordConsent` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordConsent` body |

Errors to draw in the form: 400 Notice version unknown, or the purpose is not configured

**Form: Register guest device** (modal, opened by *Register guest device*; *Register guest device* calls `registerGuestDevice`, *Cancel* sends nothing)

**Collects what `registerGuestDevice` sends before it is called.** Required: `platform`, `token`. Optional: `appVersion`, `osVersion`, `deviceModel`, `locale`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Platform `platform` | segmented control | required | — | Ios · Android · Web | — | — | `registerGuestDevice` body |
| Token `token` | text area | required | — | max length 512 | — | — | `registerGuestDevice` body |
| App version `appVersion` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Os version `osVersion` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Device model `deviceModel` | text field | optional | — | — | — | — | `registerGuestDevice` body |
| Locale `locale` | text field | optional | — | — | — | — | `registerGuestDevice` body |

#### Outputs: what the screen shows and produces

**Shown**

**Every guest device** (data table, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| App version | text | — |
| Os version | text | — |
| Device model | text | — |
| Locale | text | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |

**The selected guest device** (detail panel, from `listGuestDevices`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Subject | the name it points at, never the id | — |
| Platform | chip: Ios, Android, Web | — |
| Token fingerprint | text | Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support … |
| Token ref | text | A vault reference to the push token, written by the server from `registerGuestDevice.token` — the same pattern as … |
| App version | text | — |
| Os version | text | — |
| Device model | text | — |
| Locale | text | — |
| Status | chip: Active, Revoked, Failed | — |
| Failure count | 1,234 | Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is … |
| Registered at | 1 Oct 2026, 14:30 | — |
| Last seen at | 1 Oct 2026, 14:30 | — |
| Revoked at | 1 Oct 2026, 14:30 | — |

**The challenge** (detail panel, from `getMyChallenges`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | — |
| Name | text | — |
| Kind | chip: Visit, Spend, Ride, Collection, Streak, Referral… | What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)) … |
| Scope | chip: Individual, Family, Group, Team | 22.6.7 and 22.6.8. A family challenge is not a per-person challenge counted twice — members contribute toward one shared goal, and a school … |
| Goal | grouped details | What completes it. |
| Event | the name it points at, never the id | — |
| Reward kind | chip: Badge, Loyalty points, Wallet credit, Voucher, Entitlement, None | 22.6.13. A reward that issues wallet credit is money, and it goes through the same stored-value mechanism as everything else rather than a … |
| Reward value | 1,234 | Points, for `rewardKind: loyaltyPoints` only. A count, not an amount — a money reward is `rewardAmount`, never this. |
| Reward amount | AED 1,234.50 | The credit, for `rewardKind: walletCredit` only. The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the … |
| Badge image | the image or video | — |
| Starts at | 1 Oct 2026, 14:30 | — |
| Ends at | 1 Oct 2026, 14:30 | — |
| Status | chip: Draft, Active, Paused, Ended, Archived | — |
| Scope path | text | The partition key (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it … |

**The wishlist** (detail panel, from `getWishlist`)

| Shows | Format | Notes |
|---|---|---|
| Subject | the name it points at, never the id | — |
| Items | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Add to wishlist (primary button) | `addToWishlist` POST `/guests/{subjectId}/wishlist` | inline | Wishlist | 404 Variant not found or not sellable in this venue | opens modal first |
| Record consent (secondary button) | `recordConsent` POST `/guests/{subjectId}/consents` | RecordConsentRequest | ConsentState | 400 Notice version unknown, or the purpose is not configured | opens modal first |
| Register guest device (secondary button) | `registerGuestDevice` POST `/guests/{subjectId}/devices` | inline | GuestDevice | — | opens modal first |
| Remove from wishlist (destructive button) | `removeFromWishlist` DELETE `/guests/{subjectId}/wishlist/{itemId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Revoke guest device (destructive button) | `revokeGuestDevice` DELETE `/guests/{subjectId}/devices/{deviceId}` | — | — | 404 The resource does not exist, or is outside the caller's scope. This includes a parent in the path. | — |
| Respond to invitation (secondary button) | `respondToInvitation` POST `/invitations/{token}/respond` | inline | Invitation | 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem) | opens modal first |

**Data it reads**: `getWishlist` (onLoad, Read a guest's saved items); `listGuestDevices` (onLoad, A guest's registered devices); `getMyChallenges` (onLoad, Outstanding security challenges)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `challengeId`, `subjectId`
- → `WEB-018` My Tickets: *My Tickets*
- → `WEB-019` Order History: *Order History*

**What opens over it**

- confirmDialog *Remove from wishlist*: **Names what `removeFromWishlist` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.
- confirmDialog *Revoke guest device*: **Names what `revokeGuestDevice` changes and what it leaves alone**, in the consequence rather than the verb. A account this affects should be identified in the dialog, not just counted.

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tiles skeleton |
| Error (`?state=error`) | Partial. Each tile fails independently |
| Empty, first run (`?state=emptyFirstRun`) | A new account with no orders — offers what to do next |
| Empty, no results (`?state=emptyNoResults`) | Never shown: `listGuestDevices` takes no filter, so an empty list is always the first-run state above. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Notice version unknown, or the purpose is not configured; 409 Already answered, expired or revoked — the token is single-use — or an acceptance when the campaign's `quota` of places is taken. (InvitationResponseProblem) |

#### Permissions

- `addToWishlist` → no permission · guest
- `getWishlist` → no permission · guest
- `listGuestDevices` → no permission · guest
- `recordConsent` → no permission · guest
- `registerGuestDevice` → no permission · guest
- `removeFromWishlist` → no permission · guest
- `revokeGuestDevice` → no permission · guest
- `getMyChallenges` → `MARKETING_VIEW` (read) · staff, guest
- `respondToInvitation` → `GUEST_VIEW` (read) · guest, public

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

31 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 2.6.44 | System shall allow guests to save tickets, memberships, events, packages, add-ons, F&B items, retail products, and experiences to a wishlist for future purchase. Wishlist items shall remain linked to … | Ticketing Sales | CONTRACTED | `addToWishlist` |
| 5.3.9 | The system should allow the guest to explicitly opt in to receive any information from venue or its partners. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 5.3.18 | Maintain auditable consent records for Email, SMS, WhatsApp, Push Notifications, Marketing Communications, Privacy Policies, Terms & Conditions, and GDPR compliance. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 7.3.9 | Store and manage customer consent preferences for email, SMS, WhatsApp, push notifications and third-party marketing. Record consent status, source, timestamp, IP address and revocation history. … | F&B POS | CONTRACTED | `recordConsent` |
| 22.2.18 | Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.4.5 | Subscription Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.1 | Consent Management Framework | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.2 | Marketing Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.3 | Channel-Specific Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.4 | Consent Capture Workflows | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.13.9 | Data Processing Consent | Marketing & CRM | CONTRACTED | `recordConsent` |
| 19.2.73 | Gamification - System shall support gamification features. | Guest Mobile App & Branding | CONTRACTED | data `Challenge` |
| … 19 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web account gets device management and "sign out a lost device" (WEB-024). Face Pass stays mobile-only until the facial-reader vendor SDK supports web capture. *(agreed · design review 29 Sep 2026, GAP-D1 · D. Mobile-only features get web equivalents · DI-1077)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Footer*, set in `CMS-007` Page Builder:

Also set there, as content the tenant writes: social links: platform.

*SEO metadata*, set in `CMS-013` SEO & Metadata:

Also set there, as content the tenant writes: locale.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-017` · status **review** · provenance client-verified · **Drawn by Claude Design on `Dashboards Board.dc.html`, archived 9 September 2026 to `_dump/wireframes-3-september/`.** The frame it points at now is the generated one. This screen has been designed …
- Prototype (rev 3, verified 2026-09-28, match exact): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Sign in → avatar menu → 'Account overview'*. Differences: Prototype makes the account a single page with section panes; most YAML account screens (019–024, 026, 027, 030, 031, 034) are panes of it. Groups & invitations (respondToInvitation, getMyChallenges, referral code) sits here. Signed-out state 'Sign in to see your account' is drawn.
- Derived from `wireframes/reference/Dashboards Board.dc.html`
- Client design-board frames: `Dashboards Board.dc.html#web-017`
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (17), with its required mark, default, format and its error state (400, 404, 409).
- [ ] Every output is drawn (42 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-017?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Add to wishlist, Record consent, Register guest device, Remove from wishlist, Revoke guest device, Respond to invitation.
- [ ] Every transition is wired: `WEB-016`, `WEB-018`, `WEB-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 1 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-018` My Tickets

**Find my tickets for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `access` module |
| Block | Block A · ticket #17992 (APP-WEB-WEB-018) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listMyEntitlements` reads the population and `getEntitlement` reads one of them — list, select, act |
| Offline | **The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection. |
| Opens with | `subjectId` (session), `entitlementId` (deepLink), `orderId` (deepLink) · cold entry: **A ticket link opened after the event.** Shows the entitlement with its status — expired, used, transferred — because *not found* to somebody holding a ticket … |
| Route | `/account-and-self-service/my-tickets` |

**What the spec says about it.** Dynamic QR with a visible countdown: a rotating code derived in the page from the `rotation` seed that `getEntitlementCredential` returns, with the seconds to the next step shown (audit R230). **No screenshot blocking on the web** — a browser cannot enforce it, so the page promises none (decided 28 September, audit R077 (c)). Purpose derived from the screen name and its operations on 17 August, not from a requirement. The read surface Deep asked for. **All four were missing and the table itself did not exist until 18 August.** **Rewired on the 20 August review.** **`listEntitlements` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added transferOrderTickets. **The same screen on web and app was calling different operations** — one side could do something the other could not, and nothing recorded the difference as deliberate.

**Known gaps.** **`getEntitlementCredential` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape. **`getEntitlementHistory` declares its response inline**, so the component that shows it names fields but binds to no schema. The contract should name the shape.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| State | radio group | optional | Usable now | Usable now · Upcoming · Expired · All | — | Sends `?state=` to `listMyEntitlements`. | `listMyEntitlements` ?state |
| Include shared | toggle | optional | on | — | — | Sends `?includeShared=` to `listMyEntitlements`. | `listMyEntitlements` ?includeShared |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Rotate | toggle | off | — | `getEntitlementCredential` ?rotate |
| Include expired | toggle | on | — | `listEntitlements` ?includeExpired |

**Form: Issue wallet pass** (modal, opened by *Issue wallet pass*; *Issue wallet pass* calls `issueWalletPass`, *Cancel* sends nothing)

**Collects what `issueWalletPass` sends before it is called.** Required: `entitlementId`, `platform`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Entitlement `entitlementId` | picker: choose an entitlement | required | — | — | shows names, sends the id | — | `issueWalletPass` body |
| Platform `platform` | segmented control | required | — | Apple · Google | — | — | `issueWalletPass` body |

**Form: Share entitlement** (modal, opened by *Share entitlement*; *Share entitlement* calls `shareEntitlement`, *Cancel* sends nothing)

**Collects what `shareEntitlement` sends before it is called.** Required: `toSubjectId`. Optional: `validUntil`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| To subject `toSubjectId` | picker: choose a to subject | required | — | — | shows names, sends the id | — | `shareEntitlement` body |
| Valid until `validUntil` | date and time picker | optional | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `shareEntitlement` body |

Errors to draw in the form: 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem)

**Form: Transfer order tickets** (modal, opened by *Transfer order tickets*; *Transfer order tickets* calls `transferOrderTickets`, *Cancel* sends nothing)

**Collects what `transferOrderTickets` sends before it is called.** Required: `ticketIds`, `recipient`. Optional: `message`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Tickets `ticketIds` | multi-picker: choose tickets | required | — | at least 1 | — | The entitlements to hand over. A ticket is an entitlement, so each value is an `Entitlement.id` on this order — the ids in `OrderLine.entitlementIds`. | `transferOrderTickets` body |
| Recipient `recipient` | group | required | — | — | — | — | `transferOrderTickets` body |
| Channel `recipient.channel` | segmented control | required | — | Email · SMS · Whatsapp | — | — | `transferOrderTickets` body |
| Address `recipient.address` | text field | required | — | — | — | — | `transferOrderTickets` body |
| Message `message` | text area | optional | — | max length 500 | — | — | `transferOrderTickets` body |

Errors to draw in the form: 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem)

#### Outputs: what the screen shows and produces

**Shown**

**Every entitlement** (data table, from `listMyEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | A UUIDv7, matching `TicketStatus.ticketId` — stable for the life of the ticket and independent of the media carrying it. |
| Template | the name it points at, never the id | The definition it was issued against. Pinned at issue — a template edited next month must not change what this guest bought. |
| Product | the name it points at, never the id | — |
| Order | the name it points at, never the id | The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). |
| Order line | the name it points at, never the id | — |
| Subject | the name it points at, never the id | Who holds it. Null is legitimate — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |

**Entitlement history** (data table, from `getEntitlementHistory`): Shows `at`, `kind`, `accessPointName`, `denyReason`, `byPrincipalName` from `getEntitlementHistory`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one.

| Shows | Format | Notes |
|---|---|---|
| At | 1 Oct 2026, 14:30 | — |
| Kind | chip: Issued, Scanned, Denied, Frozen, Unfrozen, Shared… | — |
| Access point name | text | — |
| Deny reason | text | — |
| By principal name | text | — |

**Every entitlement** (data table, from `listEntitlements`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | A UUIDv7, matching `TicketStatus.ticketId` — stable for the life of the ticket and independent of the media carrying it. |
| Template | the name it points at, never the id | The definition it was issued against. Pinned at issue — a template edited next month must not change what this guest bought. |
| Product | the name it points at, never the id | — |
| Order | the name it points at, never the id | The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). |
| Order line | the name it points at, never the id | — |
| Subject | the name it points at, never the id | Who holds it. Null is legitimate — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |

**The selected entitlement** (detail panel, from `getEntitlement`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | A UUIDv7, matching `TicketStatus.ticketId` — stable for the life of the ticket and independent of the media carrying it. |
| Template | the name it points at, never the id | The definition it was issued against. Pinned at issue — a template edited next month must not change what this guest bought. |
| Product | the name it points at, never the id | — |
| Order | the name it points at, never the id | The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). |
| Order line | the name it points at, never the id | — |
| Subject | the name it points at, never the id | Who holds it. Null is legitimate — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is … |
| Venue | the name it points at, never the id | — |
| Scope path | text | — |
| Media code | text | What is scanned — a QR payload, a wristband serial, a card number. Rotatable without reissuing, because a guest whose wristband broke … |
| Status | chip: Issued, Partially consumed, Fully consumed, Expired, Cancelled, Surrendered | What the storage layer holds, and what a guest is shown. `MediaEntitlements` carried only `isValid` and a reason string — a boolean cannot … |
| Status note | text | Not `TicketStatus` — that is a validation result with a misleading name, computed at scan time and carrying `isValid` and `isInsideVenue`. |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | Resolved at issue from the template, then owned here. A freeze extends it, a reissue replaces it, and neither reaches back to the template. |
| Entries used | 1,234 | The number `validateAccess` decrements and nothing was decrementing. A ten-entry pass with no counter is a ten-entry pass that admits … |
| Entries allowed | 1,234 | — |
| Last entry at | 1 Oct 2026, 14:30 | `recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. |

**Entitlement credential** (detail panel, from `getEntitlementCredential`): Shows `mediaCode`, `payload`, `expiresAt` from `getEntitlementCredential`'s inline response. **The response has no named schema**, so this cannot bind until the contract names one. **A rotating code derived on the device** (decided 28 September, audit R230): while online the screen fetches `rotation` (secret, `timeStepSeconds`, `digits`, `algorithm`, valid `validFrom` to `validTo`) and computes …

| Shows | Format | Notes |
|---|---|---|
| Media code | text | — |
| Payload | text | — |
| Expires at | 1 Oct 2026, 14:30 | — |
| Rotation | grouped details | The time-based seed the rotating code is derived from (audit R230). Null for a credential that does not rotate (a wristband serial, a … |
| Secret | text | Base32 shared secret. Held on the device and in the gates' offline package; replaced by `rotate=true`. |
| Time step seconds | 1,234 | — |
| Digits | 1,234 | — |
| Algorithm | chip: SHA1, SHA256, SHA512 | — |
| Valid from | 1 Oct 2026, 14:30 | — |
| Valid to | 1 Oct 2026, 14:30 | The seed stops verifying after this. The app fetches a fresh one whenever it is online before then. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Transfer order tickets (primary button) | `transferOrderTickets` POST `/orders/{orderId}/transfer` | inline | TicketTransfer | 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) | opens modal first; produces a document or message: Transfer tickets to another guest |
| Issue wallet pass (secondary button) | `issueWalletPass` POST `/wallet-passes` | inline | WalletPass | — | opens modal first; produces a document or message: Generate an Apple or Google wallet pass |
| Share entitlement (secondary button) | `shareEntitlement` POST `/entitlements/{entitlementId}/share` | inline | EntitlementShare | 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem) | opens modal first |

**Data it reads**: `listMyEntitlements` (onLoad, Every ticket, pass and membership this guest holds); `getEntitlement` (onLoad, One entitlement, with what remains on it); `getEntitlementCredential` (onLoad, The thing that gets scanned — with the `rotation` seed the …); `getEntitlementHistory` (onLoad, Every scan, freeze, share and reissue against it); `listEntitlements` (onLoad, Every entitlement this guest holds, including expired)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-019` Order History: *Order History*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Tickets load |
| Error (`?state=error`) | Could not load |
| Empty, first run (`?state=emptyFirstRun`) | No tickets — distinguishes never bought from all past |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** Tickets already loaded stay visible with their age, and a ticket's rotating code is derived on the device from its seed, so it changes with no signal (decided 28 September, audit R230). Sharing, transferring and adding to a phone wallet need the connection. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 Not shareable, and the reason says which: the entitlement's template does not allow sharing (`sharingNotAllowed`, `EntitlementTemplate.canShareMedia` false) … (EntitlementRefusedProblem); 409 Ticket already redeemed (`alreadyRedeemed`), already offered (`alreadyOffered`), or the product forbids transfer (`transferNotAllowed`). (TicketTransferProblem) |

#### Permissions

- `listMyEntitlements` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlement` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementCredential` → `ORDER_VIEW` (read) · staff, guest
- `getEntitlementHistory` → `ORDER_VIEW` (read) · staff, guest
- `listEntitlements` → no permission · guest
- `transferOrderTickets` → no permission · guest
- `issueWalletPass` → `ORDER_VIEW` (read) · staff, guest
- `shareEntitlement` → `ORDER_MODIFY` (operate) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

8 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.13 | Ticket Transfer - System shall support ticket transfers. | Guest Mobile App & Branding | CONTRACTED | `transferOrderTickets` |
| 1.1.27 | System shall support ticket ownership transfer between guests according to configurable policies, fees and approval workflows. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 1.6.17 | System shall expose marketplace functionality through APIs for websites, mobile applications, partner platforms, and third-party integrations. | Ticketing Catalogue | CONTRACTED | `transferOrderTickets` |
| 2.6.39 | Customer should have the ability to view the order transactions with all the details for the logged in users and should be able to resend the tickets / Transfer Tickets to Friend / Download tickets | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 2.13.37 | Ticket Transfer & Reassignment | Ticketing Sales | CONTRACTED | `transferOrderTickets` |
| 19.2.14 | Ticket Sharing - System shall support ticket sharing. | Guest Mobile App & Branding | CONTRACTED | `shareEntitlement` |
| 2.14.10 | Manage entitlement balances and usage limits. | Ticketing Sales | CONTRACTED | data `Entitlement` |
| 2.16.15 | The system shall support replacement of lost, damaged, or stolen media while automatically disabling previous media and preserving entitlement history. | Ticketing Sales | CONTRACTED | data `Entitlement` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Web screens carry: cart promo code (valid/invalid/expired) and empty basket with confirm; interrupted-payment recovery ("we are checking with your bank" → success/failed/unknown); reprint/resend tickets; UAE Pass sign-in, link guest checkout, sign out; support cases and Sahli handoff; FX rates with timestamp; remaining entitlements. *(agreed · design review 29 Sep 2026, GAP-B3 · B. Web — missing functions on existing screens · DI-1074)*
- Entitlements portfolio is used both by the guest (mobile app) and by customer service: one view of restrictions, wallet balance and all entitlements; a unified list across a visit (e.g. four admissions, two fast passes, a meal package, a parking entitlement). *(client request · MoM 7 Sep 2026, 4.9 Entitlements Portfolio - Structure, Family/Group & Assignment · DI-667)*
- Any online purchase for a dynamic-QR event must be linked to the mobile app to show the working code; web/desktop purchases are redirected into the app for activation, not exempted. *(agreed · MoM 2 Sep 2026, 4.7 Confirmed (Pradnya's question) · DI-635)*
- Upgrades must be available in the guest mobile/web app: guests view eligible upgrade options and complete the upgrade online without visiting on-site. *(agreed · MoM 1 Sep 2026, 4.9 / 5. Key Decisions · DI-606)*
- Staff can upgrade multiple tickets in one action. "Quick upgrade" is a direct single-path upgrade (gold > platinum); "flexible upgrade" lets the guest choose among several eligible targets. *(client request · MoM 1 Sep 2026, 4.9 Ticket Upgrade & Downgrade Configuration · DI-605)*
- Qossai: where a waiver is required before entry, an incomplete waiver can block ticket download, activation, check-in or access; ticket and scan screens need a waiver-incomplete state. *(agreed · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-574)*
- Decision (raised by Chinmay): date-change/reschedule is a product-level on/off setting with its own policy rules (e.g. allowed up to 24 hours before the visit, denied within 24 hours), not a separate screen. Typically off for special-day tickets (e.g. New Year, 1 January only), on for standard GA. *(agreed · MoM 25 Aug 2026, 4.3 Ticket Type Deep-Dive; 5. Key Decisions · DI-446)*
- Decision: deferred seat assignment — sale confirmed at purchase as section + quantity; seats allocated internally; closer to the event ops/admin trigger a bulk e-mail issuing QR tickets with final seats. Immediate seat assignment remains for venues that need it. *(agreed · MoM 21 Aug 2026, 4.7 Deferred Seat Assignment Model; 5. Key Decisions · DI-423)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

**Specific to this screen** (the tenant's setting is the input; the right column is what it changes here). Draw each with its default, and the alternate where the alternate theme sets one.

*Footer*, set in `CMS-007` Page Builder:

Also set there, as content the tenant writes: social links: platform.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-018` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Header 'My tickets' → a ticket → 'Manage' (ticket sheet)*. Differences: QR is static — no rotating code with a visible countdown (YAML R230). Prototype adds reschedule, add guests, refund, resale and cancel on the ticket sheet (YAML routes refunds to WEB-019 and transfers to WEB-030).
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (11), with its required mark, default, format and its error state (404, 409).
- [ ] Every output is drawn (55 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-018?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Transfer order tickets, Issue wallet pass, Share entitlement.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-019`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 8 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-019` Order History

**Find order history for this venue.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `ticketing` module |
| Block | Block A · ticket #17923 (APP-WEB-WEB-019) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listMyOrders` reads the population and `getOrder` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session), `orderId` (deepLink), `documentId` (navigation), `invoiceId` (navigation) · cold entry: **A guest opening an order link weeks later.** Shows the order if it still resolves; if it was refunded or the performance passed, says which and offers the … |
| Route | `/account-and-self-service/order-history` |

**What the spec says about it.** Purpose derived from the screen name and its operations on 17 August, not from a requirement. **`listMyOrders` wired 24 August, raised in review.** The staff-scoped list was on this guest screen — **a guest-facing list must be scoped to the caller, not filtered by a subject parameter**, or a guest is one parameter away from somebody else’s. **Cross-surface parity, 31 August**: added getOrder, listOrders. **A guest does not know which surface they are on** — the same named screen on web and app now calls the same guest-callable operations.

**Known gaps.** The staff-scoped order list; a guest screen lists the caller's own orders with `listMyOrders` (removed from guest screens on 24 August, back with the 31 August parity pass). Transfer is WEB-030's; order history views, downloads and refunds.

#### Inputs: what the user enters or picks

**On the screen**

| Control | Drawn as | Required | Default | Allowed values, rules | Format | Notes | Source |
|---|---|---|---|---|---|---|---|
| Since | date picker | optional | — | — | 1 Oct 2026 (dd MMM yyyy) | Sends `?since=` to `listMyOrders`. | `listMyOrders` ?since |

**Filters and search the reads accept** (draw the ones a person would use; the rest are set by the screen)

| Filter | Drawn as | Default | Allowed values, rules | Source |
|---|---|---|---|---|
| Order | picker: choose an order | — | — | `listTaxInvoices` ?orderId |
| Legal entity | picker: choose a legal entity | — | — | `listTaxInvoices` ?legalEntityId |
| Invoice type | segmented control | — | Simplified · Full · Consolidated | `listTaxInvoices` ?invoiceType |
| Status | radio group | — | Issued · Partially credited · Fully credited · Superseded | `listTaxInvoices` ?status |
| Issued from | date picker | — | — | `listTaxInvoices` ?issuedFrom |
| Issued to | date picker | — | — | `listTaxInvoices` ?issuedTo |
| Tax invoice | picker: choose a tax invoice | — | — | `listCreditMemos` ?taxInvoiceId |
| Refund | picker: choose a refund | — | — | `listCreditMemos` ?refundId |
| Legal entity | picker: choose a legal entity | — | — | `listCreditMemos` ?legalEntityId |
| Issued from | date picker | — | — | `listCreditMemos` ?issuedFrom |
| Issued to | date picker | — | — | `listCreditMemos` ?issuedTo |
| Language | text field | — | pattern `^[a-z]{2}(-[A-Z]{2})?$` | `getTaxDocumentRendition` ?language |

**Form: Ask for a refund** (modal, opened by *Ask for a refund*; *Create refund request* calls `createRefundRequest`, *Cancel* sends nothing)

**Collects what `createRefundRequest` sends before it is called.** Required: `orderId`, `reason`. Optional: `lineIds`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Order `orderId` | picker: choose an order | required | — | — | shows names, sends the id | — | `createRefundRequest` body |
| Lines `lineIds` | multi-picker: choose lines | optional | — | — | — | — | `createRefundRequest` body |
| Reason `reason` | text area | required | — | min length 3; max length 1000 | — | — | `createRefundRequest` body |

Errors to draw in the form: 403 Authenticated but not permitted at the requested scope

#### Outputs: what the screen shows and produces

**Shown**

**Your orders** (card list, from `listMyOrders`): Was the generated table 'Every order'; staff and plumbing columns removed (decided by Chinmay, fix before Block A starts, 2 October 2026 (GFIX-3)).

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Lines | list or chips (count when long) | — |
| Created at | 1 Oct 2026, 14:30 | — |

**The selected order** (detail panel, from `getOrder`)

| Shows | Format | Notes |
|---|---|---|
| Order number | text | The number a guest reads and a cashier types. Server-assigned: the venue prefix and a sequence per venue, for example `DXB1-000123` … |
| Channel | chip: POS, Kiosk, Guest app, Guest web, Call centre, Partner… | Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for … |
| Status | chip: Pending, Held, Paid, Partially paid, Completed, Voided… | `held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that … |
| Currency | text | Resolved from the region, not stored (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and … |
| Gross amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Tax amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Net amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Refunded amount | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Lines | list or chips (count when long) | — |
| Payments | list or chips (count when long) | — |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Ask for a refund (secondary button) | `createRefundRequest` POST `/refund-requests` | inline | inline | 403 Authenticated but not permitted at the requested scope | opens modal first |

**Data it reads**: `listMyOrders` (onLoad, The orders this guest placed); `listTaxInvoices` (onLoad, List tax invoices); `getTaxInvoice` (onLoad, Show a tax invoice); `listCreditMemos` (onLoad, List credit memos); `getTaxDocumentRendition` (onLoad, Download the invoice / credit memo PDF)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `subjectId`
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*; carries `orderId`

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | The order history list. |
| Error (`?state=error`) | Could not load. Names which read failed and leaves the order history untouched. |
| Empty, first run (`?state=emptyFirstRun`) | No order history yet. Offers Create refund request (`createRefundRequest`); distinct from a filter that matched nothing. |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the filter on since and the order history are still there. Names the active filter and offers to clear it. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 409 An order is not paid, is already on a tax invoice of the same or a wider kind (`order-already-invoiced`), or the legal entity has no active template for the …; 422 A `full` or `consolidated` invoice without a recipient name and address, a `consolidated` invoice whose orders span buyers, legal entities or currencies, more … |

#### Permissions

- `listMyOrders` → no permission · guest
- `getOrder` → `ORDER_VIEW` (read) · staff, guest, partner
- `createRefundRequest` → no permission · guest
- `listTaxInvoices` → `LEDGER_VIEW` (read) · staff, guest
- `issueTaxInvoice` → `LEDGER_POST` (operate) · staff, guest, service
- `getTaxInvoice` → `LEDGER_VIEW` (read) · staff, guest
- `listCreditMemos` → `LEDGER_VIEW` (read) · staff, guest
- `getTaxDocumentRendition` → `LEDGER_VIEW` (read) · staff, guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

15 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 19.2.12 | Ticket Viewing - System shall display ticket details. | Guest Mobile App & Branding | CONTRACTED | `getOrder` |
| 2.6.2 | Post-order service 1) On the order details page, users can view the order number, amount, time, payment method, user information, refund/change policies, and the QR code of the e-ticket 2) During the … | Ticketing Sales | CONTRACTED | `getOrder` |
| 2.12.27 | All orders can be finalized for payment registration or modified or even cancelled at the Guest Service or any reservation PC. | Ticketing Sales | CONTRACTED | `getOrder` |
| 5.7.8 | The system should be able to use of a unique Order or Reference number (PNR) for each transaction, which can be communicated to the Payment Gateway, Acquiring Bank and the ERP system for … | F&B & Guest Management | CONTRACTED | `getOrder` |
| 19.2.15 | Ticket Cancellation - System shall support ticket cancellation. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 19.2.82 | Self-Service Refund Requests - System shall support self-service refund requests. | Guest Mobile App & Branding | CONTRACTED | `createRefundRequest` |
| 2.6.42 | Customer should be able to intiate refund tickets from the online portal | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.12 | The system should allow amendment and refunds (full or partial) based on ticket status (available, expired, etc.). This should be configurable. | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.15 | The system should be able to refund in different and multiple payment methods (example: System to allow refunds in cash for the tickets/bookings purchased through credit card). | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 2.12.18 | The system should provide the option to issue refund in the original mode of payment used by the guest or a different method of payment with supervisor override. Refund can also be offered as credits … | Ticketing Sales | CONTRACTED | `createRefundRequest` |
| 4.2.2 | The system should be able to refund transactions that contain promotions and ensure discounted amount is not refunded | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| 4.6.10 | The system to be able to refund in different and multiple payment methods. For example, system to allow refunds in cash or original payment methods. | Bundles and Promotions | CONTRACTED | `createRefundRequest` |
| … 3 more | | | | `traceability.json` |

#### Client meeting inputs

For this screen, newest first. An **Open question** is built to the default it states. Where an item disagrees with the fields above, the item wins.

- Online/app returns: customer submits a return request with a reason (and photo if applicable) → approval team → courier pickup → refund after verified receipt. Confirmed: an item bought at the POS can also be returned via the web portal, subject to approval. *(agreed · MoM 19 Aug 2026, 4.7 Returns, Refunds & Exchanges — In-Store and Online; 5. Key Decisions · DI-367)*
- Guests can request a refund from their account/profile; operations are notified and can approve, reject or ask for more information. *(agreed · MoM 12 Aug 2026, 9. Refund Ledger Sequencing and Refund Policy · DI-254)*

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-019` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Order history'*. Differences: A list pane with toast-only actions; no order detail view. Refund request and transfer are rows, not flows.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (4), with its required mark, default, format and its error state (403, 404, 409, 422).
- [ ] Every output is drawn (16 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-019?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Ask for a refund.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-018`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The 2 client meeting input(s) for this screen are applied; open questions are built to their default.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

### `WEB-020` Profile & Preferences

**Change how profile behaves here, and see which level the current value came from.**

| | |
|---|---|
| App · platform | TICVAI Guest · P01 Guest Web (web) |
| Module | Account & Self-Service · wave 1 · needs the `marketing` module |
| Block | Block A · ticket #17993 (APP-WEB-WEB-020) |
| Who uses it | a guest, signed in or not (a guest holds no permission; ADR-0025) |
| Device and orientation | This is the guest website, responsive: 1440 desktop and 390 phone widths, in the venue's brand. · LTR and RTL · light theme |
| Pattern | listDetail (compact density): `listConsentPurposes` reads the population and `getGuestProfile` reads one of them — list, select, act |
| Offline | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Opens with | `subjectId` (session) · cold entry: Resolves from the session; a cold arrival is the ordinary case. |
| Route | `/account-and-self-service/profile-and-preferences` |

**What the spec says about it.** Consent withdrawal must be as easy as granting it. Same screen, same number of clicks. Purpose derived from the screen name and its operations on 17 August, not from a requirement. Profile and Preferences. **Wishlist and device operations removed; profile, consent and email verification added.** Deep listed exactly these. **Rewired on the 20 August review.** **29 September (W1).** *Complete your details* for a profile created by guest checkout.

#### Inputs: what the user enters or picks

**Form: Save guest preferences** (modal, opened by *Save guest preferences*; *Save guest preferences* calls `updateGuestPreferences`, *Cancel* sends nothing)

**Collects what `updateGuestPreferences` sends before it is called.** Nothing in the body is required. Optional: `id`, `subjectId`, `seatingPreference`, `drinkPreferences`, `dietary`, `accessibility`, `preferredChannel`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Seating preference `seatingPreference` | text field | optional | — | max length 200 | — | — | `updateGuestPreferences` body |
| Drink preferences `drinkPreferences` | list of values (chips) | optional | — | — | — | — | `updateGuestPreferences` body |
| Dietary `dietary` | list of values (chips) | optional | — | — | — | Also written by `updateMyProfile`. | `updateGuestPreferences` body |
| Accessibility `accessibility` | list of values (chips) | optional | — | — | — | Also written by `updateMyProfile`. | `updateGuestPreferences` body |
| Preferred channel `preferredChannel` | select | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Stored on the profile (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest. | `updateGuestPreferences` body |

**Form: Save my profile** (modal, opened by *Save my profile*; *Save my profile* calls `updateMyProfile`, *Cancel* sends nothing)

**Collects what `updateMyProfile` sends before it is called.** Nothing in the body is required. Optional: `displayName`, `email`, `phone`, `preferredLanguage`, `preferredChannel`, `dietary`, `accessibility`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Display name `displayName` | text field | optional | — | — | — | — | `updateMyProfile` body |
| Email `email` | email field | optional | — | — | name@example.ae | — | `updateMyProfile` body |
| Phone `phone` | phone field | optional | — | — | +971 5X XXX XXXX (E.164) | — | `updateMyProfile` body |
| Preferred language `preferredLanguage` | text field | optional | — | — | — | — | `updateMyProfile` body |
| Preferred channel `preferredChannel` | radio group | optional | — | Email · SMS · Whatsapp · Push · None | — | — | `updateMyProfile` body |
| Dietary `dietary` | list of values (chips) | optional | — | — | — | Health-adjacent personal data, kept structured rather than as a tag (BL-134). `GuestProfile.tags` carries VIP-style markers adequately and is the wrong home for a nut allergy — … | `updateMyProfile` body |
| Accessibility `accessibility` | list of values (chips) | optional | — | — | — | Same treatment, same reason. Stored as `GuestPreferences.accessibility`. | `updateMyProfile` body |

**Form: Record consent** (modal, opened by *Record consent*; *Record consent* calls `recordConsent`, *Cancel* sends nothing)

**Collects what `recordConsent` sends before it is called.** Required: `purpose`, `decision`, `noticeVersion`, `source`, `recordedAt`. Optional: `channels`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Purpose `purpose` | select | required | — | Marketing · Personalisation · Profiling · Third party sharing · AI processing · Transactional | — | — | `recordConsent` body |
| Decision `decision` | segmented control | required | — | Granted · Withdrawn · Not asked | — | — | `recordConsent` body |
| Channels `channels` | multi-select chips | optional | — | Email · SMS · Whatsapp · Push · In app · Post | — | Omit to apply to every channel the purpose covers. | `recordConsent` body |
| Notice version `noticeVersion` | text field | required | — | — | — | — | `recordConsent` body |
| Source `source` | select | required | — | Guest app · Website · Kiosk · POS · Call centre · Import · Agent recorded · Cookie banner · Checkout | — | `checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents` … | `recordConsent` body |
| Recorded at `recordedAt` | date and time picker | required | — | — | 1 Oct 2026, 14:30 (venue time zone) | — | `recordConsent` body |

Errors to draw in the form: 400 Notice version unknown, or the purpose is not configured

**Form: Verify guest email** (modal, opened by *Verify guest email*; *Verify guest email* calls `verifyGuestEmail`, *Cancel* sends nothing)

**Collects what `verifyGuestEmail` sends before it is called.** Required: `mode`. Optional: `token`. Dismissing sends nothing; the screen behind is unchanged.

| Field | Control | Required | Default | Allowed values, rules and conditions | Format | Helper text | Source |
|---|---|---|---|---|---|---|---|
| Mode `mode` | segmented control | required | — | Send · Confirm | — | — | `verifyGuestEmail` body |
| Token `token` | text field | optional | — | — | — | For `confirm`. Single use and short-lived — a verification link that works forever is a verification link in an old inbox. | `verifyGuestEmail` body |

Errors to draw in the form: 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are …

#### Outputs: what the screen shows and produces

**Shown**

**Every consent purpose config** (data table, from `listConsentPurposes`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |

**Complete your details** (banner, from `updateMyProfile`): For a profile created by guest checkout (W1): asks for what the pop-up did not; never blocks.

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |
| Merged at | 1 Oct 2026, 14:30 | — |

**The selected consent purpose config** (detail panel, from `listConsentPurposes`)

| Shows | Format | Notes |
|---|---|---|
| Purpose | chip: Marketing, Personalisation, Profiling, Third party sharing, AI processing … | — |
| Display name | text | — |
| Description | text | — |
| Channels | list or chips (count when long) | — |
| Notice version | text | Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured. |
| Is required for service | yes / no (icon or chip) | True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently. |
| Expires after months | 1,234 | — |

**The guest profile** (detail panel, from `getGuestProfile`)

| Shows | Format | Notes |
|---|---|---|
| ID | the name it points at, never the id | Added 20 August. The schema reference derives table columns from API response schemas, and a response is not a table — this one returned … |
| Subject | the name it points at, never the id | Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger. |
| Display name | text | — |
| Email | text | — |
| Phone | +971 50 123 4567 | — |
| Preferred language | text | — |
| Preferred channel | chip: Email, SMS, Whatsapp, Push, In app, Post | — |
| Guest link | text | Present where the guest is linked across cells. Marketing acts locally. |
| Tags | list or chips (count when long) | — |
| Engagement score | 1,234 | 22.2.20 and 22.2.21. `lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not. |
| Engagement tier | chip: New, Active, Occasional, Lapsing, Lapsed, Dormant | 5.3.19. Automatic classification, computed rather than assigned. |
| Lifetime value | AED 1,234.50 | On the wire this is three fields; in the database it is one column. 24 August. |
| Visit count | 1,234 | — |
| Last visit at | 1 Oct 2026, 14:30 | — |
| Is active | yes / no (icon or chip) | — |
| Merged into subject | the name it points at, never the id | Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`, which retain it as a redirect rather than deleting it. |

**Actions and what each produces**

| Action | Calls | Sends | On success returns | Errors to show | Notes |
|---|---|---|---|---|---|
| Save my profile (primary button) | `updateMyProfile` PATCH `/guests/me/profile` | inline | GuestProfile | — | opens modal first |
| Record consent (secondary button) | `recordConsent` POST `/guests/{subjectId}/consents` | RecordConsentRequest | ConsentState | 400 Notice version unknown, or the purpose is not configured | opens modal first |
| Verify guest email (secondary button) | `verifyGuestEmail` POST `/auth/guest/verify-email` | inline | inline | 410 The token expired or was already used. Distinct from an invalid one — a guest who clicked an old link should be offered a new one rather than told they are … | opens modal first; produces a document or message: Send a verification link, or consume one |
| Save guest preferences (secondary button) | `updateGuestPreferences` PUT `/guests/{subjectId}/preferences` | GuestPreferences | GuestPreferences | — | opens modal first |

**Data it reads**: `getGuestProfile` (onLoad, Read a guest profile); `listConsentPurposes` (onLoad, Configured consent purposes); `getMyIdentityVerification` (onLoad, Show the guest's ID verification status)

**Where the user goes next**

- → `WEB-016` Login / Register: *Login / Register*; carries `subjectId`
- → `WEB-017` My Account Dashboard: *My Account Dashboard*
- → `WEB-018` My Tickets: *My Tickets*

#### States

| State | What it shows |
|---|---|
| Loading (`?state=loading`) | Profile and consents |
| Error (`?state=error`) | **Save failed and the form keeps what was typed.** A consent change that silently did not save is a compliance failure, so the screen states it rather than showing success |
| Empty, first run (`?state=emptyFirstRun`) | — |
| Empty, no results (`?state=emptyNoResults`) | Nothing matches the current filters. **The filters are named and clearable from here** — an empty list with the filter state hidden elsewhere is a person who thinks the data is gone. **Added 25 August with the derived list component**: a screen that lists has to say what it shows when the list is empty, and this screen gained the list before it gained the sentence. |
| Permission denied (`?state=emptyNoAccess`) | **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the … |
| Offline (`?state=offline`) | **The offline banner shows.** What was already loaded stays on screen, marked with its age. Anything that spends money, holds capacity or changes the account waits for the connection, and its button says so rather than failing. |
| Validation and conflict | the form keeps what was entered and marks the problem: 400 Notice version unknown, or the purpose is not configured; 409 A verification is already pending for this guest; 422 The document has expired, or its kind is not accepted by the tenant's policy |

#### Permissions

- `getGuestProfile` → `GUEST_VIEW` (read) · staff, guest
- `updateMyProfile` → `GUEST_VIEW` (read) · guest
- `recordConsent` → no permission · guest
- `listConsentPurposes` → `GUEST_VIEW` (read) · staff, guest
- `verifyGuestEmail` → `GUEST_VIEW` (read) · guest, anonymous
- `updateGuestPreferences` → `GUEST_MANAGE` (configure) · staff, guest
- `getMyIdentityVerification` → no permission · guest
- `submitGuestIdentityDocument` → no permission · guest

**A refused user sees:** **There is no permission to name — a guest holds none** (ADR-0025: `x-ticvai-permission` is what a staff caller must hold; a guest call resolves to the guest's own data). No access here means one of two things, told apart by the response: not signed in, where the guest is offered sign-in and brought back to this screen, or a record that is not theirs, which says so without saying whose it is. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the …

#### Requirements it meets

18 rows of the client's requirements matrix (`sources/requirements/Ticvai_matrix_20260621_2.xlsx`) trace to this screen's operations or data (`handoff/traceability.json`). The matrix carries no priority; the screen's block is its delivery priority.

| Ref | Requirement (shortened) | Domain | Verdict | Via |
|---|---|---|---|---|
| 13.3.8 | APIs shall support guest profile creation, updates, segmentation, communication preferences and activity history retrieval. | Developer & API Management | CONTRACTED | `getGuestProfile` |
| 22.2.27 | CRM APIs | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 22.2.28 | CRM Audit Trail | Marketing & CRM | CONTRACTED | `getGuestProfile` |
| 19.2.7 | Profile Management - System shall support profile management. | Guest Mobile App & Branding | CONTRACTED | `updateMyProfile` |
| 2.6.40 | Customer should be able to view and amend user profile | Ticketing Sales | CONTRACTED | `updateMyProfile` |
| 5.3.5 | The system should allow user to amend account contact details (postal address, email address, telephone number, newsletter opt-in, SMS opt-in, etc.) | F&B & Guest Management | CONTRACTED | `updateMyProfile` |
| 22.13.13 | Right to Rectification | Marketing & CRM | CONTRACTED | `updateMyProfile` |
| 5.3.9 | The system should allow the guest to explicitly opt in to receive any information from venue or its partners. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 5.3.18 | Maintain auditable consent records for Email, SMS, WhatsApp, Push Notifications, Marketing Communications, Privacy Policies, Terms & Conditions, and GDPR compliance. | F&B & Guest Management | CONTRACTED | `recordConsent` |
| 7.3.9 | Store and manage customer consent preferences for email, SMS, WhatsApp, push notifications and third-party marketing. Record consent status, source, timestamp, IP address and revocation history. … | F&B POS | CONTRACTED | `recordConsent` |
| 22.2.18 | Consent Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| 22.4.5 | Subscription Management | Marketing & CRM | CONTRACTED | `recordConsent` |
| … 6 more | | | | `traceability.json` |

#### Client meeting inputs

None names this screen.

Also apply: 1 for P01 · Account & Self-Service, 39 for all of P01, 29 for every app (section *Design inputs from the client meetings* below).

#### Workshop task tracker

No tracker row concerns this screen; the rows for its platform are listed once, below.

#### Configurable by the tenant

This is a white-label guest screen: it is drawn in the venue's brand, never TICVAI's (except the fixed *Powered by TICVAI* credit). Draw it with the **default theme**, and on the key screens one **alternate tenant theme** (`handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`).

**Shell-wide, on every guest screen:** Brand (10, CMS-002, CMS-004, ADM-016); Theme (31, CMS-005, CMS-003, ADM-016); Fonts (5, CMS-003); Header (5, CMS-007); Navigation (17, CMS-009); Footer (website) (15, CMS-007); Languages and right-to-left (2, CMS-011, ADM-018); Modules shown to guests (3, CMS-001); Features (3, CMS-001); Custom domain (website) (3, CMS-017, ADM-017); SEO metadata (website) (13, CMS-013). Each element, its CMS field, allowed values and default: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

#### References

- Wireframe frame: `wireframes/P01 Guest Web.dc.html#web-020` · status **review** · provenance client-verified
- Prototype (rev 3, verified 2026-09-28, match partial): `sources/designs/guest-rev3-28-september/TICVAI Guest Booking v2.dc.html`, view *Account → 'Personal details', 'Notifications', 'Accessibility'*. Differences: Split over three panes; fields are read-only with a 'Save changes' toast. No 'which level the current value came from' (YAML purpose). Consent purposes appear as two marketing toggles rather than the configured purpose list.
- ADR-0025 *— One field says who may call an operation* (`docs/adr/0025-one-audience-field.md`)
- ADR-0045 *Every order carries a proven contact, and the gate is the checkout page* (`docs/adr/0045-every-order-carries-a-proven-contact.md`)

#### Acceptance for the design

- [ ] Every input above is drawn (20), with its required mark, default, format and its error state (400, 404, 409, 410, 422).
- [ ] Every output is drawn (47 fields) with realistic seeded data in the format given (AED, dates, names, never ids).
- [ ] Every state opens from `#WEB-020?state=<state>`: loading, error, emptyFirstRun, emptyNoResults, emptyNoAccess, offline.
- [ ] Every action is wired with its success and its failure: Save my profile, Record consent, Verify guest email, Save guest preferences.
- [ ] Every transition is wired: `WEB-016`, `WEB-017`, `WEB-018`.
- [ ] Sign-in is asked only where the spec asks for it.
- [ ] The module and platform inputs below are applied.
- [ ] Drawn in the default theme; on a key screen also in the alternate tenant theme; nothing hard-codes a brand colour, logo or font.
- [ ] Nothing in this specification appears on the screen as text (no ids, field names or permission keys).

---

## Tenant configuration on every guest screen

Every guest screen in this batch is white-label. These elements are set by the tenant in the CMS and apply to every screen of the guest app (each screen's block lists the ones particular to it). **Draw with the default theme; on the key screens add one alternate tenant theme** (below), so a reviewer sees the brand is configuration, not paint. The full map, with the input-to-output examples: `handoff/design-batches/apps/1-guest-app/WHITE-LABEL.md`.

| Element | Configured in | Allowed values | Default | What it changes |
|---|---|---|---|---|
| Logo (`brand.logoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo in the header or nav bar, the splash and the footer |
| Logo dark image (`brand.logoDarkAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the logo on dark backgrounds (falls back to the primary logo) |
| Logo variant (`brand.logoVariant`) | `CMS-002`, `CMS-004`, `ADM-016` | Light · Dark · Duotone | Light | which logo lockup sits in the nav bar, and whose colours drive the theme |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Splash image (`brand.splashImageAssetRefs`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG, JPG, SVG or MP4 from the media library | — | Splash images, shown in order. Build-time on the native apps (`splashChangeScope`); immediate on web, reaching guests with the publish (audit R163). |
| Splash duration seconds (`brand.splashDurationSeconds`) | `CMS-002`, `CMS-004`, `ADM-016` | min 0; max 10 | 3 | — |
| Splash background colour (`brand.splashBackgroundColour`) | `CMS-002`, `CMS-004`, `ADM-016` | #RRGGBB | — | — |
| Show loading indicator (`brand.showLoadingIndicator`) | `CMS-002`, `CMS-004`, `ADM-016` | — | on | — |
| Intro video (`brand.introVideoAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | The optional intro video (decided 29 September, MOB-5). A video `MediaAsset` from the media library (CMS-010). |
| Intro video mode (`brand.introVideoMode`) | `CMS-002`, `CMS-004`, `ADM-016` | Off · First launch · Every launch; Anything but `off` needs `introVideoAssetRef`, or 400. | Off | When GST-001 plays it full screen. "Skip introduction" is always shown. |
| Primary colour (`theme.primaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the brand colour (the `accentSolid` token): primary buttons (Book, Continue, Add to cart, Pay), the active step of the step indicator, selected date and time chips, focus rings |
| Secondary colour (`theme.secondaryColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | secondary buttons and secondary emphasis: unselected chips, secondary tabs |
| Accent colour (`theme.accentColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | highlights: badges (LIMITED, NEW, BESTSELLER), availability counts, sale prices |
| Background colour (`theme.backgroundColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | the page background behind every screen (the `ground` token) |
| Text colour (`theme.textColour`) | `CMS-005`, `CMS-003`, `ADM-016` | #RRGGBB | — | body text on the background |
| Dark mode (`theme.darkMode`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the dark variant on a device in dark mode (mobile app); derived from the light theme when absent |
| Corner radius (`theme.cornerRadius`) | `CMS-005`, `CMS-003`, `ADM-016` | min 0; max 32 | — | the corners of cards, buttons, inputs, sheets and the cart (0 square to 22 the prototype's roundest) |
| Surface style (`theme.surfaceStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Glass · Solid | Glass | cards and panels: frosted glass (default) or opaque (the `surfaceRaised` token) |
| Button style (`theme.buttonStyle`) | `CMS-005`, `CMS-003`, `ADM-016` | Solid · Outline · Pill | Solid | every button's shape: solid fill, outline, or pill |
| Component colours (`theme.componentColours`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | Colours for single interactive elements (decided 17 September, M17-11). Each is optional and falls back to the theme colours. |
| Primary latin (`fonts.primaryLatin`) | `CMS-003` | — | — | headings and body text in English |
| Primary arabic (`fonts.primaryArabic`) | `CMS-003` | Required when `ar` is among the tenant's languages (audit R163). | — | headings and body text in Arabic |
| Secondary latin (`fonts.secondaryLatin`) | `CMS-003` | — | — | the secondary face (eyebrows, numbers) in English |
| Secondary arabic (`fonts.secondaryArabic`) | `CMS-003` | Required whenever `secondaryLatin` is set and `ar` is among the tenant's languages (decided 28 September, audit R163). | — | the secondary face in Arabic |
| Custom font images (`fonts.customFontAssetRefs`) | `CMS-003` | PNG, JPG, SVG or MP4 from the media library | — | Uploaded font files, as `MediaAsset` ids. |
| Header layout (`header.layout`) | `CMS-007` | Logo left · Logo centre · Logo with menu | — | the header: logo left, logo centred, or logo with the menu |
| Show logo (`header.showLogo`) | `CMS-007` | — | on | — |
| Show menu (`header.showMenu`) | `CMS-007` | — | on | — |
| Show notifications (`header.showNotifications`) | `CMS-007` | — | on | — |
| Background colour (`header.backgroundColour`) | `CMS-007` | #RRGGBB | — | — |
| Navigation kind (`navigation.kind`) | `CMS-009` | Bottom navigation · Drawer · Tabs | — | the main navigation: bottom tab bar, drawer, or tabs |
| Navigation items (`navigation.items`) | `CMS-009` | at most 12 | — | — |
| Buy button (`navigation.buyButton`) | `CMS-009` | — | — | The persistent Buy tickets button (decided 29 September, MOB-2). On every screen of the mobile app except the booking and checkout steps; it opens GST-003. |
| Footer columns (`footer.columns`) | `CMS-007` | — | — | — |
| Legal links (`footer.legalLinks`) | `CMS-007` | — | — | Required links, held separately from the free-form columns — a tenant reorganising their footer must not be able to remove the privacy notice by accident. |
| Copyright text (`footer.copyrightText`) | `CMS-007` | — | — | — |
| Social links (`footer.socialLinks`) | `CMS-007` | — | — | — |
| Languages (`languages.languages`) | `CMS-011`, `ADM-018` | at least 1 | — | the language button in the header; Arabic flips every screen right to left |
| Default language (`languages.defaultLanguage`) | `CMS-011`, `ADM-018` | ISO 639-1 code, shown as the language name | — | the language a first visit opens in |
| Modules (`modules.modules`) | `CMS-001` | — | — | — |
| Features (`features.features`) | `CMS-001` | — | — | — |
| Custom domain hostname (`domains.hostname`) | `CMS-017`, `ADM-017` | — | — | — |
| Custom domain kind (`domains.kind`) | `CMS-017`, `ADM-017` | Guest web · Guest app · Partner portal · Developer portal | — | — |
| Verification method (`domains.verificationMethod`) | `CMS-017`, `ADM-017` | Dns txt · Cname · Http file | Dns txt | — |
| Entity kind (`seo.entityKind`) | `CMS-013` | Content page · Product · Event · Performance · Membership · Promotion · Venue | — | — |
| Entity (`seo.entityId`) | `CMS-013` | shows names, sends the id | — | — |
| Locale (`seo.locale`) | `CMS-013` | — | — | — |
| SEO metadata title (`seo.title`) | `CMS-013` | — | — | — |
| Meta description (`seo.metaDescription`) | `CMS-013` | — | — | — |
| Keywords (`seo.keywords`) | `CMS-013` | — | — | — |
| Canonical URL (`seo.canonicalUrl`) | `CMS-013` | — | — | — |
| Slug (`seo.slug`) | `CMS-013` | — | — | 22.11.6. Human-readable, and changing one is a redirect rather than an edit — a slug that changes without a 301 is a page that was ranking and now is not. |
| Hreflang (`seo.hreflang`) | `CMS-013` | — | — | 22.11.11. Which URL serves which language, and getting this wrong on a bilingual venue site splits its own ranking between two versions of the same page. |
| Schema org type (`seo.schemaOrgType`) | `CMS-013` | — | — | — |
| Open graph (`seo.openGraph`) | `CMS-013` | — | — | — |
| Is auto generated (`seo.isAutoGenerated`) | `CMS-013` | — | on | 22.11.2. Generated by default and overridable. |
| No index (`seo.noIndex`) | `CMS-013` | — | off | — |
| Favicon (`brand.faviconAssetRef`) | `CMS-002`, `CMS-004`, `ADM-016` | PNG or SVG ≤ 2 MB for logos; images ≥ 1600 px; video MP4 | — | the browser tab icon (website only) |
| Component colours: primary CTA (`theme.componentColours.primaryCta`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the one main call to action on each screen, when it should differ from the brand colour |
| Component colours: pay button (`theme.componentColours.payButton`) | `CMS-005`, `CMS-003`, `ADM-016` | — | — | the Pay button at checkout |
| Buy button: style (`navigation.buyButton.style`) | `CMS-009` | Raised · Floating · Flat · Hidden | Raised | the Buy tickets button in the tab bar: raised (default), floating, flat, or hidden |

**The alternate tenant theme (Coastal Aqua)**: Primary colour #0077B6; Secondary colour #023E8A; Accent colour #FFB703; Background colour #F5FAFC; Text colour #0B1324; Corner radius 18; Surface style Solid; Button style Pill; Logo variant Duotone; Header layout Logo centre; Step indicator Dots; Card layout Cards across; Card size Standard; Cart layout Floating icon; Fonts Poppins / Tajawal.
**Key screens to show in it:** `WEB-001`, `WEB-005`, `WEB-006`, `WEB-010`, `WEB-012`, `GST-001`, `GST-007`, `GST-041`, `KSK-002`, `KSK-003`.

**Never configurable:** The *Powered by TICVAI* credit in the footer is fixed and never client-editable (MoM 3 Aug, DI-111; MoM 12 Aug, DI-250). Semantic colour pairs (success, warning, danger, neutral) are not overridable: a tenant who recolours danger to their brand green has made a destructive confirmation look like a success (`screens/_design-tokens.yaml` whiteLabel). Site structure and the navigation flow are fixed and adapt to the product configuration (MoM 3 Aug, DI-119); a guest always books a product or package, never a resource (DI-502). A colour pair that fails 4.5:1 contrast is refused by the CMS, not warned (setTheme 400 ContrastProblem, audit R139).

## Reference designs and the trackers for this platform

**P01 reference designs** (from `handoff/design-batches/apps/1-guest-app/README.md`)

- `sources/designs/guest-rev3-30-september/TICVAI Guest Booking v2.dc.html`: the website. Rev 3 with the 29 September fixes and the 30 September feedback (group booking with a headcount, multi-park counters, surf session tickets, the swim-ability answer, transport stations and departures, popular route cards; `CLIENT-RESPONSE-30SEP.md` beside it). The client approved it for development once W1 to W10 are in.
- `sources/designs/guest-rev3-30-september/TICVAI Visit Planner.dc.html`: the visit planner. WEB-050 Plan Your Visit is this file.

**Design Vision Book rules that apply** (`sources/designs/Ticvai_Design_Vision_Book_v1_1.pdf`): DI-021, DI-022, DI-023, DI-024, DI-025, DI-026, DI-027, DI-029, DI-032, DI-033, DI-034, DI-036, DI-038, DI-040, DI-042, DI-044, DI-045, DI-048, DI-049, DI-050, DI-051 (each is in the design inputs below).

**Workshop tracker rows about P01 as a whole** (23: 3 open, 20 closed). Open first; a closed row says where it went on 30 September.

- **S3** Guest web (B2C) design steps for CRM, CMS and seat management *(Softlabs Design Team · In progress · 30 Sep 2026 · 30 Sep tracker)*
- **S9** Final UI/UX for the website and the mobile app *(Chinmay Parab · In progress · due Fri 2 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **T1** Feedback on the revised website and mobile wireframes *(Allam / Qossai · Open · due 1 Oct · 30 Sep 2026 · 30 Sep tracker)*
- **A27** Research current market best practices for ticket-booking UX (web and mobile) *(Softlabs Design Team · Medium · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A28** Review the 'Viva Ticket' website as a reference for ticket-flow variations *(Softlabs Design Team · Low · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · workshop tracker)*
- **A29** Collate design references/inspiration and share with TICVAI, organized by mobile app, website, and admin/back-office pages *(Softlabs (Sahil & Aishwarya) · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A55** Implement per-tenant module visibility toggles (e.g., hide Dining, Retail, or other services) configurable independently for the guest website and mobile app *(Softlabs Design Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A57** Design integration to consume each venue's live attraction wait-time feed (from entry-counting sensors/cameras) via API, and surface wait times in the guest mobile app *(Softlabs Team · Medium · Done → 30 Sep: Closed, Done (as recorded earlier) · workshop tracker)*
- **A98** Design CMS multi-site / white-label configuration (branding palette, fonts, GA IDs, prod/staging, page builder, full-site vs B2C-embedded mode) *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 21 Aug 2026 · workshop tracker)*
- **A100** Design the B2C checkout journey as a 3–4 step flow (step indicator, in-page ticket browsing, optional add-ons step, dual-OTP guest checkout, per-person name capture, deferred profile completion) *(Softlabs Design Team · High · Ongoing → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 21 Aug 2026 · workshop tracker)*
- **A115** Apply HA selectively to revenue-critical components (ticketing, POS, B2C) same-region, with multi-region DR as an optional add-on *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Moved to OpenProject (S13: build) · 24 Aug 2026 · workshop tracker)*
- **A118** Commission the third-party penetration test before go-live (ticketing, B2C, B2B, mobile apps) and resolve all severities *(Softlabs Team · High · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 24 Aug 2026 · workshop tracker)*
- **A125** Extend the preview/publish step to render PDF ticket and Apple/Google Wallet formats, not only the B2C web preview *(Softlabs Team · Medium · Not started → 30 Sep: Closed, Rolled into S10 (decision log, for TICVAI's review) · 25 Aug 2026 · workshop tracker)*
- **A174** Cross-check the six previously-scoped wallet types against Allam's documentation and deliver the three wireframe flows (ticketing, F&B, retail) plus the revised B2C flow *(Chinmay Parab / Pradnya Yeram / Allam · High · Partial → 30 Sep: Closed, Rolled into S9 (final UI/UX) · 9 Sep 2026 · workshop tracker)*
- … 9 more in `handoff/design-inputs/task-tracker-index.json`

## Design inputs from the client meetings

**What the client asked for in the meetings and design reviews, for these screens.** Apply every item. They are the client's own requirements and they are later than the reference files: where a reference design or a screen's fields disagree with an item here, the item wins. Newest first; where two items disagree, the newer one wins (anything a later meeting replaced is already left out). An **Open question** is not settled: build the default it states and keep it easy to change. The text in brackets is for traceability and, like everything else in this bundle, never appears on a screen.

### Everywhere, on every app

- Allam (platform-wide requirement): every calendar throughout the platform, not just maintenance, must support day, week and month views, with the day view further broken down by hour from a defined start hour through the day. *(agreed · MoM 17 Sep 2026, 4.2 Preventive Maintenance Planning · DI-907)*
- Minimise the number of separate screens an end user navigates: consolidate related information wherever it can reasonably be shown together, rather than mirroring every workshop board as its own screen. *(agreed · MoM 7 Sep 2026, 4.10 Screen consolidation / 5. Key Decisions · DI-671)*
- Region-configurable tax on pre-discount price (e.g. Egypt: AED 100 ticket with 20% off is paid at AED 80 but taxed on AED 100). Rounding must support up to three decimal places without dropping the third decimal where the currency requires it. *(agreed · MoM 1 Sep 2026, 4.5 Taxes, Fees & Price Calculation · DI-598)*
- "Powered by TICVAI" is shown consistently across staff and guest-facing surfaces. *(agreed · MoM 14 Aug 2026, 8. POS / Kiosk Branding · DI-297)*
- Full multi-language support (Arabic and others such as Chinese) consistent with the agreed i18n/RTL architecture. *(agreed · MoM 10 Aug 2026, 4.7 Account Creation, Localisation & Multi-Currency · DI-210)*
- The reference system is a functional reference only: its dated UI/UX is not to be replicated; TICVAI delivers equivalent depth with a modern, AI-friendly, easy-to-configure experience. *(agreed · MoM 7 Aug 2026, 23. Reference System Access & Documentation · DI-186)*
- Direction: modern, minimalistic, spacious, cross-device designs that still convey a sense of place (venue or park); Softlabs proposes two to three enhanced visual concepts for TICVAI to steer. *(agreed · MoM 3 Aug 2026, 11. Design Alignment & Team Input · DI-126)*
- Languages: English and Arabic at minimum, with Russian, Spanish and Mandarin. *(agreed · MoM 31 Jul 2026, 13. Internationalization & Localization · DI-080)*
- Clarity first; reduce cognitive load (simple layouts, familiar patterns); consistency ("Use the system. Do not recreate."); accessibility; hierarchy (guide attention with contrast, spacing and visual weight); feedback (every action has a clear response). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Design Principles in Action · DI-051)*
- Standard components: search bar with Cmd+K; tabs (Overview, Events, Sales, Reports); pagination; badges (New, Pending, Sold Out, Completed); toggle (Off/On); dropdown; removable chip ("VIP x"). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - Example UI Components · DI-050)*
- Spacing on an 8px base grid: 4, 8, 12, 16, 24, 32, 40, 48, 64, 80. Border radius scale 4, 8, 12, 16, 24px, consistent across the platform. Soft shadows: sm 0 1px 2px rgba(0,0,0,.05); md 0 4px 6px rgba(0,0,0,.08); lg 0 10px 15px rgba(0,0,0,.10); xl 0 20px 40px rgba(0,0,0,.14). *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 6. Spacing / 7. Border Radius / 8. Shadows · DI-049)*
- Icons: line style, outline, 2px stroke, round corners, clean and consistent. *(agreed · Design Vision Book 29 Jul 2026, 08 Design System (p8) - 5. Icons · DI-048)*
- Component principles: clarity first; consistent spacing on an 8px grid; meaningful colour (colours communicate status and guide the user); accessible by design; mobile ready (components adapt across all screen sizes). Components are consistent, flexible, accessible and composable. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Component principles · DI-045)*
- Empty states have a title, one explanatory line and one action: "No events yet / Create your first event to get started / Create Event"; "No data available / We couldn't find anything to show here / Refresh". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Empty States · DI-044)*
- Notification list: status icon, title, one-line detail and relative time (e.g. "Payment received ... 2m ago", "High demand detected ... 10m ago"), with "View all notifications". *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Notifications · DI-042)*
- Forms: label above field; text input, select ("Choose an option"), date picker, toggle, checkbox. Input states: Default, Focused, Filled, Disabled and Error with inline message (e.g. "This field is required"). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Forms; 08 Design System (p8) - 4. Inputs · DI-040)*
- Card types: event card (title, date and time, venue, "From 120.00 AED"); KPI card (label, value, delta, "vs last 7 days"); onboarding checklist card ("3 of 6 completed": Create Event, Add Staff, Configure Seating, Connect Payment). *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Cards · DI-038)*
- Button hierarchy Primary, Secondary, Tertiary (text) and Icon buttons, each with Default, Hover, Pressed and Disabled states. *(agreed · Design Vision Book 29 Jul 2026, 06 Component Direction (p6) - Buttons; 08 Design System (p8) - 3. Buttons · DI-036)*
- Regardless of the module a user is working in, the experience should feel like one product, not a collection of separate applications. *(agreed · Design Vision Book 29 Jul 2026, 07 Modules Overview (p7) · DI-034)*
- DO: focus on clarity and hierarchy, use clear simple interactive elements, give relevant information at a glance (card example: "Annual Membership / All Venues / 4.4 (388) / BESTSELLER"). DON'T: clutter and overload (e.g. "-10% NEW PROMO AED 450.00 !!! BOOK NOW!!!"), complex forms and flows, hard-to-read data visualisations. *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - DO / DON'T · DI-033)*
- Eight principles on every screen: User-Centric, AI-First, Simple & Clear (clean layouts, clear hierarchy, minimal noise), Fast & Efficient (optimised for quick actions), Reliable & Secure (permissions, data protection), Data-Driven (data visual, actionable, easy to understand), Scalable, Consistent (same patterns, components and interactions across the ecosystem). *(agreed · Design Vision Book 29 Jul 2026, 05 Design Principles (p5) - Our Design Principles · DI-032)*
- Accessibility: high contrast, readable text, keyboard navigation and inclusive components throughout; WCAG AA standards minimum ("Design for everyone"). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - Better Accessibility; 06 Component principles (p6); 08 Design principles in action (p8) · DI-029)*
- AI everywhere: AI insights, recommendations and smart assistance are embedded across the platform, not hidden. AI is not an add-on: it assists, predicts, recommends and automates. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - How TICVAI improves this concept; 05 Design Principles (p5) - 2. AI-First · DI-027)*
- Global Search: prominent, AI-powered search that finds anything, in the top bar with a Cmd+K shortcut (placeholder e.g. "Search events, customers, orders, venues or ask AI..."). *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, item 1; 08 Design System (p8) - Search Bar · DI-025)*
- Visual direction: Purposeful (every element has a clear purpose), Consistent (one visual system across all modules and devices), Clear (easy to scan, understand and act on), Modern. Key takeaway: clean, modern, product-first layout with clear hierarchy and minimal visual noise; deep, modern, trustworthy; built for enterprise scale. *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) · DI-024)*
- The brand is presented consistently across Web Platform, Mobile App and Admin Portal (and print). Ticvai identity, colours and typography are applied consistently across all screens and devices. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand in action; 03 Visual Direction (p3) - Consistent Branding · DI-023)*
- Copy is Professional, Friendly, Clear, Confident, Concise and Helpful. Avoid jargon, overly technical language, clutter, outdated language and complexity. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand voice · DI-022)*
- Brand personality: Modern, AI-First, Enterprise, Premium, Reliable, Minimal, Scalable, Human-Centred. Visual essence: intelligent and forward-thinking, clean and minimal, trustworthy and secure, modern and timeless, scalable and flexible. *(agreed · Design Vision Book 29 Jul 2026, 02 Brand Identity (p2) - Brand personality / Visual essence · DI-021)*
- Arabic is a core requirement, not later localisation: full Arabic RTL across web, mobile, POS, reports, emails, WhatsApp, SMS, notifications, tickets and receipts, and administrative interfaces. *(agreed · MoM 28 Jul 2026, 27. Internationalisation and Arabic Support · DI-019)*

### Across P01 Guest Web

- Step-indicator style is configurable, the same as on the web: bars, dots, counters or step names. *(agreed · MoM 30 Sep 2026, 4.6 Mobile App — Booking Flow & Checkout · DI-1093)*
- **Open question.** Real venue photos, clips and logos are still to come from the client; designs use stand-ins. Slots expected: a photo per ticket card and clip per card, a square shot per extra/shop item, one landscape poster per venue for the single-event page. Photos ≥1600 px, clips mp4 6–12 s, no audio. *(open · design review 29 Sep 2026, Asset list — TICVAI Guest Booking · DI-1080)*
- The tenant picks which logo lockup sits in the nav bar and a logo variant (Light, Dark, Duotone) whose colours drive the theme. *(agreed · design review 29 Sep 2026, CFG-4 · Brand logo + Logo palette (Light/Dark/Duotone) · DI-1068)*
- Theme settings: surface style Glass (default) or Solid cards; button style Solid (default), Outline or Pill. *(agreed · design review 29 Sep 2026, CFG-3 · Surfaces (Glass/Solid) and Buttons (Solid/Outline/Pill) · DI-1067)*
- Venue branding offers named palettes, font pairs, background tones and a 0–22 px corner radius. *(agreed · design review 29 Sep 2026, CFG-2 · Brand: Palette, Typeface; Shape: Background, Corner radius · DI-1066)*
- Guest-facing copy may say "session" (surf sessions, timed sessions) as a glossary exception, like "Booking". *(agreed · design review 29 Sep 2026, CFG-10 · 'Sessions can be added, edited or closed from Config -> Sessions' · DI-1064)*
- Never ask the same thing twice: table zone is picked on the table map (no zone step before it); height is asked once (height bands on the water-park day pass are the eligibility check); party/school summaries prefill headcount, child's name and age from the earlier form. *(agreed · rev 3 design review 28 Sep 2026, Flow review (28 Sep): repeated steps removed · DI-1000)*
- Confirmed final: cart sliding in from the right or bottom, card size options, and cart-sidebar placement left or right; Qossai specifically liked the compact card size. No further changes requested. *(agreed · MoM 24 Sep 2026, 4.10 Guest Web App — Card Layout & Cart Configuration Confirmed · DI-991)*
- Headers are reserved for standard elements only (venue image, category tabs, language bar, profile icon), applied consistently; date/availability selection belongs in the main content below the header, never in the header. Header/layout patterns must be adapted for mobile, which looks and behaves differently. *(agreed · MoM 24 Sep 2026, 4.9 Guest Web App — Specific UX Feedback (Header/Date Placement Standardization) · DI-990)*
- A language button (EN / العربية) sits in the header next to the profile icon, web and mobile. Arabic flips the whole layout right-to-left and switches interface text (navigation, buttons, booking steps, ticket names and tags, cart, seat map, checkout, account). Venue, show and dish names stay as written. *(client request · design review 23 Sep 2026, Header 2. Language icon in the header · DI-975)*
- Replace "Sign in / Create account" in the header with a single profile icon. It opens one screen with Log in and Register tabs; signed-in guests get their account menu from the same icon. *(client request · design review 23 Sep 2026, Header 1. One profile icon in the header that opens login / register · DI-974)*
- Allam's model reference: a simple card-based family-entertainment-centre site with minimal clicks, a right-side cart drawer, "help me choose", clear categories, video that autoplays when a guest taps "read more", adapting seamlessly between desktop and mobile. Allam and Qossai want this simplicity to guide the guest experience. *(client request · MoM 18 Sep 2026, 4.14 Guest Website UX Review — Upsell/Cross-Sell Placement & Reference Sites · DI-952)*
- **Open question.** Allam expects a large volume of feedback on the guest web/mobile prototype; detailed feedback goes to a separate dedicated session with Qossai and Allam. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-888)*
- The reviewed prototype is the actual guest-facing B2C site customers browse and book from, not a CMS tool. A separate, more limited white-label interface lets a client adjust colours, fonts and layout from a menu of options; not yet built in the prototype. *(agreed · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-887)*
- **Open question.** Product card-layout options shown in the prototype: stacked, staggered, horizontal. Choice/feedback pending the dedicated review. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-886)*
- **Open question.** Prototype's white-label panel previews the guest site under theme presets (e.g. "stadium", "theatre"), alternative layouts and brand colour palettes. Shown by Chinmay; client feedback deferred to a dedicated session. *(open · MoM 15 Sep 2026, 4.1 Guest Web/Mobile App Prototype Review - White-Labeling Configuration & Flows · DI-885)*
- Qossai is dissatisfied with the current B2C guest platform build and wants a separate vision session; references: the "Little Explorer" site and Six Flags. Six Flags cues: single-page flow. *(client request · MoM 8 Sep 2026, 4.20 Planning & Next Steps · DI-736)*
- Allam: most guests book from a smartphone, so the mobile version of the booking flows is the higher priority to validate (only desktop shown). *(client request · MoM 7 Sep 2026, 4.18 Guest Booking Flow Prototype Walkthrough · DI-684)*
- Face enrollment via mobile app, website, POS, self-service kiosk, or at the turnstile itself (scan the ticket, then look at the reader on first use), covering e.g. B2B/reseller tickets. Re-enrollment and fallback to QR/RFID if face fails at the gate. *(agreed · MoM 2 Sep 2026, 4.10 Facial Recognition - Face Pass, Face Tag & Enrollment · DI-641)*
- Configurable cookie consent banner (accept/reject) per website; some cookies flagged mandatory (non-rejectable), others optional; templated and configurable in the system. *(client request · MoM 1 Sep 2026, 4.13 Privacy Consent & Cookie Policy · DI-617)*
- Waiver versioning, a mobile-optimised guest waiver view, approval/testing/publication flow, and access to the form via a QR code that opens it directly. *(client request · MoM 31 Aug 2026, 4.9 Waiver / Consent Form Configuration · DI-575)*
- Confirmed: a guest always books a product or package — never a resource (a specific room, vehicle or instructor by itself) directly — on every sales channel, including the guest/mobile app; the product's configuration determines which resources are booked behind the scenes. *(agreed · MoM 26 Aug 2026, 4.10 Guest-Facing Behaviour & Configuration Q&A; 5. Key Decisions · DI-502)*
- Six Flags Kidiya reference: fixed header with configurable navigation (logo, Explore/Tickets/Passes, sub-menus), every item toggleable via the CMS. *(client request · MoM 21 Aug 2026, 4.8 B2C Checkout Journey Review — Six Flags Kidiya Reference Walkthrough · DI-424)*
- Allam: the venue's main website is fully venue-managed; after "Book Now" the white-label B2C flow keeps the venue's header/footer branding while product selection, cart and checkout are TICVAI-managed. Header/footer links to non-checkout pages redirect to the main venue site. *(client request · MoM 20 Aug 2026, 4.10 CMS & White-Label Website / Mobile App Configuration · DI-397)*
- Ticketing, F&B and retail share one cart and checkout, one unified receipt and one QR/wristband per customer — no separate receipts or wristbands per product line. *(agreed · MoM 14 Aug 2026, 7. Retail — Cart and Inventory · DI-293)*
- Guest website and app share one CMS/publishing and the same branding, look and feel, but differ in function: the app is the full tenant experience (venue info, services, profile, purchase); a client's own website usually just links ("Buy Tickets") to a TICVAI-hosted checkout. *(agreed · MoM 14 Aug 2026, 3. Guest Website vs. Guest Mobile App · DI-284)*
- Qossai: the TICVAI name must always remain visible to end users of a client-branded guest app (e.g. a "Made by TICVAI" credit) and cannot be removed by the client. *(agreed · MoM 12 Aug 2026, 5. Guest Application Publishing and White-Labelling · DI-250)*
- Qossai: present products with video rather than static images (as Talabat-style apps do); see benchmark app "222" for further inspiration. *(client request · MoM 10 Aug 2026, 4.10 Bundle Packages · DI-222)*
- Qossai shared reference apps (Al Qadiya / Six Flags Saudi Arabia, and "The District" by Zomato) and cited their use of video over static images as design inspiration. *(client request · MoM 5 Aug 2026, 13. Mobile / POS App Design References · DI-146)*
- A single cart/order must take mixed purchases (e.g. family tickets plus gift vouchers) with one unified checkout and identity capture. *(agreed · MoM 5 Aug 2026, 7. Sales Channels, Pricing & Cart · DI-141)*
- Base ticket-booking UX (web and mobile) on current market best practice rather than the demoed references as-is; Allam recommends the "Viva Ticket" website as a reference for the flow variations. *(agreed · MoM 3 Aug 2026, 10. Reference Material & Design Research · DI-125)*
- A multi-language toggle switches the entire site's content. *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-120)*
- Allam: banner, header, footer and background color are CMS-configurable per client, but site structure and navigation flow are fixed and adapt automatically to product configuration (dated, non-dated, seated, membership products surface the right fields). *(agreed · MoM 3 Aug 2026, 9. Website Structure, Localization & Authentication · DI-119)*
- All sites are fully mobile-responsive; e.g. the desktop calendar view collapses into a mobile-optimized layout. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-113)*
- A "powered by [platform]" footer credit is fixed and not client-editable. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-111)*
- One client can run multiple branded sites from the same setup, e.g. two brands sharing a footer but with distinct headers and hero banners. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-110)*
- White-label sites share one platform/template but each is configured independently: header, footer, logo, colors, fonts and hero banner are client-editable from the backend. *(agreed · MoM 3 Aug 2026, 6. B2C/B2B Website Walkthrough (Multi-Site, White-Label) · DI-108)*
- Selling reference layout: clean top navigation; category tabs with counts (All Events 32, Exhibitions, Guided Tours ...); sort and type chips (Price, Rating, Popular; General, Seated, Multipass, Scheduled, Rental); content cards with large image, type badge, rating, tags (LIMITED, NEW, BESTSELLER), availability ("180 available", "11 left") and "from" price; persistent cart on the right with member discount, totals and "Checkout Securely". *(agreed · Design Vision Book 29 Jul 2026, 03 Visual Direction (p3) - UI inspiration reference, items 2-5 · DI-026)*
- Preliminary perceived-performance targets: web pages load in under about 3 seconds, mobile app loads in under about 2 seconds, ticket validation responds in under 500 milliseconds. *(agreed · MoM 28 Jul 2026, 18. Performance and Scalability · DI-015)*

### In P01 · Account & Self-Service

- Decision: profiles are never merged automatically. Likely duplicates are notified to the customer (push or e-mail) and merge only on the customer's confirmation; an admin review queue tracks flagged duplicates independently of the customer's response. *(agreed · MoM 20 Aug 2026, 4.2 Duplicate Detection; 5. Key Decisions · DI-377)*

**22 more name particular screens** and are in each screen's block above (*Client meeting inputs*).

---

## Raw data

The same package data the blocks above are built from. `screens.json` is in the folder and not repeated here: every field of it is in the blocks.

### `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
"addToWishlist": {"method":"POST","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Save an item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Wishlist"},
"claimCart": {"method":"POST","path":"/carts/{cartId}/claim","contract":"orders","summary":"Attach an anonymous cart to a guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"CartMergeResult"},
"claimDeviceConsent": {"method":"POST","path":"/guests/{subjectId}/consents/claim-device","contract":"marketing-crm","summary":"Attach a browser's cookie decision to the guest who turned out to own it","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"ClaimDeviceConsentRequest","responds":"ConsentState"},
"createMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge","contract":"identity","summary":"Second factor at staff sign-in, and step-up for a sensitive action","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"createRefundRequest": {"method":"POST","path":"/refund-requests","contract":"orders","summary":"Guest-initiated refund request","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"getEntitlement": {"method":"GET","path":"/entitlements/{entitlementId}","contract":"access","summary":"One entitlement, with what remains on it","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"Entitlement"},
"getEntitlementCredential": {"method":"GET","path":"/entitlements/{entitlementId}/credential","contract":"access","summary":"The thing that gets scanned","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":"rotate","in":"query","required":null}],"requestBody":null,"responds":null},
"getEntitlementHistory": {"method":"GET","path":"/entitlements/{entitlementId}/history","contract":"access","summary":"Every scan, freeze, share and reissue against it","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getGuestProfile": {"method":"GET","path":"/guests/{subjectId}","contract":"marketing-crm","summary":"Read a guest profile","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":"GuestProfileDetail"},
"getGuestSession": {"method":"GET","path":"/auth/guest/session","contract":"identity","summary":"Read the current guest session","permission":null,"offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"GuestSession"},
"getMyChallenges": {"method":"GET","path":"/guests/me/challenges","contract":"marketing-crm","summary":"Active challenges and how far along I am","permission":"MARKETING_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[],"requestBody":null,"responds":null},
"getMyIdentityVerification": {"method":"GET","path":"/auth/guest/identity-verifications/current","contract":"identity","summary":"The guest's own latest identity verification","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[],"requestBody":null,"responds":"IdentityGuestVerification"},
"getOrder": {"method":"GET","path":"/orders/{orderId}","contract":"orders","summary":"Read an order","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Order"},
"getTaxDocumentRendition": {"method":"GET","path":"/tax-documents/{documentId}/rendition","contract":"finance","summary":"The PDF of a tax invoice or credit memo, in a language","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"language","in":"query","required":null}],"requestBody":null,"responds":"FinTaxDocumentRendition"},
"getTaxInvoice": {"method":"GET","path":"/tax-invoices/{invoiceId}","contract":"finance","summary":"One tax invoice, with its lines, VAT per rate and credit memos","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[],"requestBody":null,"responds":"FinTaxInvoice"},
"getWishlist": {"method":"GET","path":"/guests/{subjectId}/wishlist","contract":"marketing-crm","summary":"Read a guest's saved items","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[],"requestBody":null,"responds":"Wishlist"},
"guestLogout": {"method":"DELETE","path":"/auth/guest/session","contract":"identity","summary":"End a guest session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"allDevices","in":"query","required":null}],"requestBody":null,"responds":null},
"guestPasswordLogin": {"method":"POST","path":"/auth/guest/password","contract":"identity","summary":"Sign in with an email or mobile and a password","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"guestSocialLogin": {"method":"POST","path":"/auth/guest/social","contract":"identity","summary":"Sign in with Apple or Google","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"guestUaePassLogin": {"method":"POST","path":"/auth/guest/uae-pass","contract":"identity","summary":"Sign in with a national identity provider","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"issueTaxInvoice": {"method":"POST","path":"/tax-invoices","contract":"finance","summary":"Issue a tax invoice for one or more paid orders","permission":"LEDGER_POST","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"FinIssueTaxInvoiceRequest","responds":"FinTaxInvoice"},
"issueWalletPass": {"method":"POST","path":"/wallet-passes","contract":"orders","summary":"Generate an Apple or Google wallet pass","permission":"ORDER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"WalletPass"},
"linkGuestCheckout": {"method":"POST","path":"/auth/guest/link-checkout","contract":"identity","summary":"Attach a guest checkout to an account","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"listConsentPurposes": {"method":"GET","path":"/consent-purposes","contract":"marketing-crm","summary":"Configured consent purposes","permission":"GUEST_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listCreditMemos": {"method":"GET","path":"/credit-memos","contract":"finance","summary":"Credit memos issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"taxInvoiceId","in":"query","required":null},{"name":"refundId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listEntitlements": {"method":"GET","path":"/my/entitlements/all","contract":"access","summary":"Every entitlement this guest holds, including expired","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"includeExpired","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listGuestDevices": {"method":"GET","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"A guest's registered devices","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyEntitlements": {"method":"GET","path":"/guests/me/entitlements","contract":"access","summary":"Every ticket, pass and membership this guest holds","permission":"ORDER_VIEW","offlineCapable":true,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null},{"name":"state","in":"query","required":null},{"name":"includeShared","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listMyOrders": {"method":"GET","path":"/my/orders","contract":"orders","summary":"The orders this guest placed","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null},{"name":"since","in":"query","required":false},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"listTaxInvoices": {"method":"GET","path":"/tax-invoices","contract":"finance","summary":"Tax invoices issued, newest first","permission":"LEDGER_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"region","parameters":[{"name":"orderId","in":"query","required":null},{"name":"legalEntityId","in":"query","required":null},{"name":"invoiceType","in":"query","required":null},{"name":"status","in":"query","required":null},{"name":"issuedFrom","in":"query","required":null},{"name":"issuedTo","in":"query","required":null},{"name":null,"in":null,"required":null},{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Page"},
"recordConsent": {"method":"POST","path":"/guests/{subjectId}/consents","contract":"marketing-crm","summary":"Record a consent decision","permission":null,"offlineCapable":false,"conflictPolicy":"append","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RecordConsentRequest","responds":"ConsentState"},
"refreshToken": {"method":"POST","path":"/auth/refresh","contract":"identity","summary":"Rotate the access token","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"TokenPair"},
"registerGuest": {"method":"POST","path":"/auth/guest/register","contract":"identity","summary":"Create a guest account","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"RegisterGuestRequest","responds":"GuestSession"},
"registerGuestDevice": {"method":"POST","path":"/guests/{subjectId}/devices","contract":"marketing-crm","summary":"Register a device for push","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestDevice"},
"removeFromWishlist": {"method":"DELETE","path":"/guests/{subjectId}/wishlist/{itemId}","contract":"marketing-crm","summary":"Remove a saved item","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"requestGuestOtp": {"method":"POST","path":"/auth/guest/otp","contract":"identity","summary":"Request a one-time code","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"respondToInvitation": {"method":"POST","path":"/invitations/{token}/respond","contract":"marketing-crm","summary":"Accept or decline","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"Invitation"},
"revokeGuestDevice": {"method":"DELETE","path":"/guests/{subjectId}/devices/{deviceId}","contract":"marketing-crm","summary":"Revoke a device registration","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"shareEntitlement": {"method":"POST","path":"/entitlements/{entitlementId}/share","contract":"orders","summary":"Let somebody else use this, without giving it away","permission":"ORDER_MODIFY","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"EntitlementShare"},
"submitGuestIdentityDocument": {"method":"POST","path":"/auth/guest/identity-verifications","contract":"identity","summary":"Submit an identity document for verification","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"IdentityGuestDocumentSubmission","responds":"IdentityGuestVerification"},
"transferOrderTickets": {"method":"POST","path":"/orders/{orderId}/transfer","contract":"orders","summary":"Transfer tickets to another guest","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"venue","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"updateGuestPreferences": {"method":"PUT","path":"/guests/{subjectId}/preferences","contract":"marketing-crm","summary":"The things a regular should not have to say twice","permission":"GUEST_MANAGE","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":"GuestPreferences","responds":"GuestPreferences"},
"updateMyProfile": {"method":"PATCH","path":"/guests/me/profile","contract":"marketing-crm","summary":"A guest correcting their own details","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"lastWriterWins","scopeLevel":"subject","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestProfile"},
"verifyGuestEmail": {"method":"POST","path":"/auth/guest/verify-email","contract":"identity","summary":"Send a verification link, or consume one","permission":"GUEST_VIEW","offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null},
"verifyGuestOtp": {"method":"POST","path":"/auth/guest/otp/verify","contract":"identity","summary":"Verify a one-time code and issue a session","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":"GuestSession"},
"verifyMfaChallenge": {"method":"POST","path":"/auth/mfa/challenge/{challengeId}/verify","contract":"identity","summary":"Complete a sign-in or step-up challenge","permission":null,"offlineCapable":false,"conflictPolicy":"serverWins","scopeLevel":"tenant","parameters":[{"name":null,"in":null,"required":null}],"requestBody":null,"responds":null}
}
```

### `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
"Cart": {"type":"object","x-ticvai-persistence":"orders.cart","required":["id","venueId","channel","status","lines"],"properties":{"id":{"type":"string","format":"uuid"},"token":{"type":"string","readOnly":true,"description":"**How an anonymous guest returns to their cart**, including from a recovery email. Rotated on claim, so a link shared before signing in does not reach the account after.\n"},"venueId":{"type":"string","format":"uuid"},"channel":{"$ref":"../shared/common.yaml#/components/schemas/SalesChannel"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Null while anonymous. Set by `claimCart`."},"status":{"$ref":"#/components/schemas/CartStatus"},"lines":{"type":"array","items":{"$ref":"#/components/schemas/CartLine"}},"conflicts":{"type":"array","items":{"$ref":"#/components/schemas/CartConflict"}},"consentQuestions":{"type":"array","readOnly":true,"description":"**The consent questions this cart's products and flow ask** (decided 29 September, rev 3 REV3-26), computed on read at their current version as **the union of each line's published booking flow's `white-label.BookingFlow.settings.consentQuestionIds`** (the flow `getPublishedBookingFlow` resolves for the line's product: product, then category, then the venue's flow for the kind; moved from `BookingFlowConfig`, 29 September W12) **and every line's `catalogue.Product.consentQuestionIds`, each question once**: the flow's first, in its order, then each product's in cart-line order, a question already listed not repeated (its `lineIds` gain the line). The client asks them, in the order given, and sends the answers to `marketing.recordConsentAnswers`; `answered` then turns true. One or several, as the venue chose. `checkoutCart` refuses while a required one is unanswered.\n","items":{"allOf":[{"$ref":"../satellite/marketing-crm.yaml#/components/schemas/ConsentQuestion"},{"type":"object","properties":{"lineIds":{"type":"array","description":"The cart lines that ask it. Empty for a question the flow asks.","items":{"type":"string","format":"uuid"}},"answered":{"type":"boolean","description":"Every person (for `perPerson`) or the booking (for `perBooking`) has an answer."}}}]}},"subtotal":{"x-ticvai-column":"net_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"discountTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxTotal":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"total":{"x-ticvai-column":"gross_amount","$ref":"../shared/common.yaml#/components/schemas/Money"},"appliedPromotionIds":{"type":"array","description":"**Re-evaluated on every read.** A promotion that expired while the cart sat must not still be applied at checkout, and a promotion that became applicable should be.\n","items":{"type":"string","format":"uuid"}},"couponCodes":{"type":"array","readOnly":true,"description":"The promo codes the guest entered through `applyCartPromoCode` (decided 28 September, audit R073 (e)). **Sent as `couponCodes` on every promotions evaluation of this cart**, so a code is re-checked on each read like any promotion; a code that stops qualifying stays listed here and its promotion drops out of `appliedPromotionIds`.\n","items":{"type":"string","maxLength":100}},"expiresAt":{"type":"string","format":"date-time","description":"The earliest lease expiry in the cart, or the cart's own window where it holds none."},"extensionsUsed":{"type":"integer","readOnly":true},"maxExtensions":{"type":"integer","readOnly":true},"locale":{"type":"string"},"createdAt":{"type":"string","format":"date-time"},"updatedAt":{"type":"string","format":"date-time"}}},
"CartMergeResult": {"type":"object","x-ticvai-persistence":"none — computed","required":["cart"],"properties":{"cart":{"$ref":"#/components/schemas/Cart"},"mergedLineCount":{"type":"integer"},"droppedLines":{"type":"array","description":"**Reported, never silent.** Lines that could not be re-leased on merge are named, so a guest signing in is told what they lost rather than discovering it at checkout.\n","items":{"type":"object","properties":{"productName":{"type":"string"},"reason":{"type":"string","enum":["noCapacity","expired","notSellableOnChannel","duplicate"]}}}}}},
"Challenge": {"type":"object","x-ticvai-persistence":"marketing.challenge","description":"BL-022, CF-137. **Section 22.6 is twenty requirements and 19.2.73–75 three more** — checked against the matrix on 18 August rather than assumed. It is asked for explicitly.\n**Gamification is not loyalty.** Loyalty pays for spend; a challenge pays for behaviour the venue wants and spend does not produce — a second visit, a quiet Tuesday, a ride nobody rides. **A challenge that only rewards spending is a loyalty programme with worse arithmetic.**\n","required":["id","name","kind","goal","status"],"properties":{"id":{"readOnly":true,"type":"string","format":"uuid"},"name":{"type":"string"},"kind":{"type":"string","description":"What an entrant does to progress. `scan`, `activity` and `purchase` were added from the BO-825 pack (decided 28 September, audit R275 (c)): `scan` counts scans of a named code or point (a trail marker, a stand), `activity` counts completions of a named attraction or activity that is not a ride, and `purchase` counts purchases of named products or categories. **`purchase` is not `spend`**: `spend` counts money, whatever was bought; `purchase` counts items bought.\n","enum":["visit","spend","ride","collection","streak","referral","survey","social","milestone","scan","activity","purchase"]},"scope":{"type":"string","enum":["individual","family","group","team"],"default":"individual","description":"22.6.7 and 22.6.8. **A family challenge is not a per-person challenge counted twice** — members contribute toward one shared goal, and a school competing against another school is a group scoring against a group.\n**This is the field that needs the portfolio work** (CF-132): a family challenge without a family is an individual challenge with a label.\n"},"goal":{"type":"object","description":"What completes it.","properties":{"metric":{"type":"string"},"target":{"type":"number"},"withinDays":{"type":"integer","nullable":true}}},"eventId":{"type":"string","format":"uuid","nullable":true},"rewardKind":{"type":"string","enum":["badge","loyaltyPoints","walletCredit","voucher","entitlement","none"],"description":"22.6.13. **A reward that issues wallet credit is money**, and it goes through the same stored-value mechanism as everything else rather than a parallel one.\n"},"rewardValue":{"type":"integer","nullable":true,"minimum":1,"description":"**Points, for `rewardKind: loyaltyPoints` only.** A count, not an amount — a money reward is `rewardAmount`, never this.\n"},"rewardAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"nullable":true,"description":"**The credit, for `rewardKind: walletCredit` only.** The shared `Money`, stored as `numeric(18,4)` with currency and scale resolved from the region, because a wallet credit is money and naming-and-style 5.1 forbids money as a bare number.\n"},"badgeAssetId":{"type":"string","format":"uuid","nullable":true},"startsAt":{"type":"string","format":"date-time"},"endsAt":{"type":"string","format":"date-time","nullable":true},"status":{"readOnly":true,"type":"string","enum":["draft","active","paused","ended","archived"]},"scopePath":{"readOnly":true,"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"ChallengeProgress": {"type":"object","x-ticvai-persistence":"marketing.challenge_progress","description":"22.6.15. **Progress is shown, not just the outcome.** A guest two visits from a reward behaves differently from one who does not know how close they are, which is the entire mechanism.\n","required":["id","challengeId","subjectId","current","target"],"properties":{"id":{"type":"string","format":"uuid"},"challengeId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"portfolioId":{"type":"string","format":"uuid","nullable":true,"description":"For a family or group challenge — where the shared progress accrues."},"current":{"type":"number"},"target":{"type":"number"},"streakCount":{"type":"integer","nullable":true},"completedAt":{"type":"string","format":"date-time","nullable":true},"rewardIssuedAt":{"type":"string","format":"date-time","nullable":true}}},
"ClaimDeviceConsentRequest": {"type":"object","x-ticvai-persistence":"none — request only","required":["consentKey"],"properties":{"consentKey":{"type":"string","maxLength":64}}},
"ConsentDecision": {"type":"string","enum":["granted","withdrawn","notAsked"]},
"ConsentPurpose": {"type":"string","enum":["marketing","personalisation","profiling","thirdPartySharing","aiProcessing","transactional"]},
"ConsentPurposeConfig": {"x-ticvai-persistence":"marketing.consent_purpose + marketing.consent_purpose_channel","type":"object","required":["purpose","channels","noticeVersion","isRequiredForService"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"displayName":{"type":"string"},"description":{"type":"string"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","description":"Current version of the notice. A consent against a superseded version is reported as requiring renewal rather than silently honoured.\n"},"isRequiredForService":{"type":"boolean","description":"True for transactional. Withdrawing it means the service cannot be delivered, so it is presented differently.\n"},"expiresAfterMonths":{"type":"integer","nullable":true}}},
"ConsentSource": {"type":"string","enum":["guestApp","website","kiosk","pos","callCentre","import","agentRecorded","cookieBanner","checkout"],"description":"`checkout` (30 September, M18-15): an opt-in ticked beside the terms at checkout, carried on orders `checkoutCart` `marketingConsents[]` and recorded by `recordCheckoutConsents`, bound to the order and the verified contact. `cookieBanner` (29 September, build; BL-073 §4b): a decision made on the cookie banner or preference centre and moved onto the guest by `claimDeviceConsent`. Kept apart from `website`, a form submission, because the audit trail (2.6.56) has to tell the two apart."},
"ConsentState": {"x-ticvai-persistence":"none — projection over consent_record","type":"object","required":["subjectId","purposes"],"properties":{"subjectId":{"type":"string","format":"uuid"},"purposes":{"type":"array","items":{"type":"object","required":["purpose","decision","requiresRenewal"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string","nullable":true},"requiresRenewal":{"type":"boolean","description":"True where the notice has been superseded since consent was given."},"decidedAt":{"type":"string","format":"date-time","nullable":true}}}}}},
"Entitlement": {"type":"object","x-ticvai-persistence":"access.entitlement","description":"**What a guest actually holds.** Found missing on 18 August by the schema audit — 33 tables in `orders`, seven in `access`, and none of them stored an issued ticket.\nThe package sold products, defined `EntitlementTemplate`, recorded `ScanEvent.ticketId`, transferred `ticket_transfer.ticketIds` and issued `wallet_pass.entitlementId` — **five artefacts referring to a thing that did not exist.** `validateAccess` read the *template* and never the instance, and `suspendEntitlement` suspended the template, **which would have suspended it for every guest who held one.**\n**The template is the definition and this is the instance.** A template says *an annual pass admits once a day for a year*; this says *this guest's annual pass, bought on 3 March, used eleven times, frozen for two weeks in July, valid until 2 March.*\n","required":["id","templateId","productId","orderId","subjectId","status","validFrom","validTo"],"properties":{"id":{"type":"string","format":"uuid","description":"A UUIDv7, matching `TicketStatus.ticketId` — **stable for the life of the ticket and independent of the media carrying it.** A guest whose wristband broke keeps the same entitlement with a new `mediaCode`.\n**This is the ticket id.** Wherever an operation takes a `ticketId` or `ticketIds` — `lookupTicket`, `listScans`, `ScanEvent`, the offline package and `transferOrderTickets` — it is this value. An order line's `entitlementIds` are the ticket ids of that line.\n"},"templateId":{"type":"string","format":"uuid","description":"The definition it was issued against. **Pinned at issue** — a template edited next month must not change what this guest bought.\n"},"productId":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid","description":"The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`)."},"orderLineId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true,"description":"Who holds it. **Null is legitimate** — a ticket bought as a gift or sold at a till to somebody who gave no details has no subject until it is claimed.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"mediaCode":{"type":"string","description":"What is scanned — a QR payload, a wristband serial, a card number. **Rotatable without reissuing**, because a guest whose wristband broke should not need a new ticket.\n"},"status":{"$ref":"../spine/orders.yaml#/components/schemas/EntitlementStatus"},"statusNote":{"type":"string","nullable":true,"description":"**Not `TicketStatus` — that is a validation result with a misleading name**, computed at scan time and carrying `isValid` and `isInsideVenue`. The lifecycle is `orders.EntitlementStatus`, and `states/entitlement-status.yaml` has modelled it since before this table existed.\n**Which is the finding in one line: the package had the lifecycle, the state model and the validation result, and no row to hang them on.**\n"},"validFrom":{"type":"string","format":"date-time"},"validTo":{"type":"string","format":"date-time","description":"**Resolved at issue from the template, then owned here.** A freeze extends it, a reissue replaces it, and neither reaches back to the template.\n**What the pre-expiry notice is measured from** (29 September, build pass, group G2; 5.5.30). A daily run in access publishes `entitlement.expiringSoon` once per entitlement and `validTo` when an entitlement in `issued` or `partiallyConsumed` comes within its template's `expiryNoticeDays` (`catalogue.EntitlementTemplate`), and not for one bought inside that window. Marketing turns it into the reminder (a `MessageTrigger` on the event, or a triggered campaign on `entitlementExpiring`); access only says the date is near. A freeze or renewal that moves `validTo` raises the next notice once.\n"},"entriesUsed":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"**The number `validateAccess` decrements and nothing was decrementing.** A ten-entry pass with no counter is a ten-entry pass that admits forever.\n**Maintained on write**, in the same transaction as the admitting `access.scan_event` row: by `validateAccess`, `validateGroupAccess` (by the count admitted) and `syncScans` for each replayed admission the server accepts. A replayed scan the server downgrades to `denied` does not count.\n"},"entriesAllowed":{"type":"integer","nullable":true},"lastEntryAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"x-ticvai-derived":"onWrite","description":"`recordedAt` of the latest admission counted in `entriesUsed`, written by the same writes. A scan replayed late with an earlier `recordedAt` does not move it back.\n"},"frozenDays":{"type":"integer","default":0,"readOnly":true,"x-ticvai-derived":"onWrite","description":"Days added by a freeze. **Maintained on write** by the freeze operation (`freezeEntitlement`), in the same write that extends `validTo` by those days. **Held here rather than computed from a freeze log**, because a gate has to answer in under 300ms and cannot replay a history to decide validity.\n"},"suspendedReason":{"type":"string","nullable":true},"freezeReason":{"type":"string","nullable":true,"enum":["travelling","injury","personal","seasonal","other"],"description":"The `reason` of the latest `freezeEntitlement` (audit R222). Null when never frozen."},"freezeNote":{"type":"string","nullable":true,"maxLength":500,"description":"The `note` the latest `freezeEntitlement` took, required there when `reason` is `other` (decided 28 September, audit R222). Kept so the quarterly review of `other` notes has something to read."},"isNameBound":{"type":"boolean","default":false},"holderName":{"type":"string","nullable":true},"sharedWithSubjectIds":{"type":"array","description":"`shareEntitlement`. **The owner keeps it and a second person may present it** — the asymmetry that stops a shared family pass becoming a resale chain.\n","items":{"type":"string","format":"uuid"}},"issuedVia":{"type":"string","enum":["sale","invitation","reissue","transfer","resale","membership","groupBooking"],"description":"**How it came to exist, and it matters to finance.** A sold entitlement carries deferred revenue; an invitation carries a marketing cost; a reissue carries neither.\n"},"supersedesEntitlementId":{"type":"string","format":"uuid","nullable":true,"description":"For a reissue or a resale. **The chain is traceable** — a ticket appearing from nowhere is indistinguishable from a fraudulent one.\n"},"walletValueId":{"type":"string","format":"uuid","nullable":true,"description":"Where the template carries stored value. **A `retail.Wallet` bound to the entitlement, not a balance on it** (CF-126).\n"},"facePassEnrolmentId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"x-ticvai-persisted":false,"x-ticvai-derived":"onRead","description":"The active `facePass` enrolment on this entitlement (`FacePassEnrolment.id`), or null when none is. **Computed on read from `pii.subject_biometric` and not stored here** — the PII split keeps the biometric on its own side, and this carries only its id. It is how a screen holding a pass finds the enrolment `getFacePassEnrolment` and `revokeFacePass` take.\n"}}},
"EntitlementShare": {"type":"object","x-ticvai-persistence":"none — a view of the identity.delegated_access row shareEntitlement writes","description":"**A second person's right to present an entitlement the owner still holds.** Returned by `shareEntitlement` and `revokeEntitlementShare`; its `id` is the delegated-access row the share is.\n","required":["id","entitlementId","toSubjectId","status"],"properties":{"id":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid"},"toSubjectId":{"type":"string","format":"uuid","description":"The guest it is shared with. They may present it; they may not share or transfer it on."},"validFrom":{"type":"string","format":"date-time"},"validUntil":{"type":"string","format":"date-time","nullable":true,"description":"Null means until revoked or until the entitlement itself ends."},"revokedAt":{"type":"string","format":"date-time","nullable":true},"status":{"type":"string","enum":["active","revoked","expired"]}}},
"FinCreditMemo": {"x-ticvai-persistence":"ledger.credit_memo + ledger.credit_memo_line","type":"object","description":"5.7.94. **A tax credit note against one tax invoice**, with its own series. Never edited.","required":["id","creditMemoNumber","taxInvoiceId","kind","reason","legalEntityId","issuedAt","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"creditMemoNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's credit memo series, in sequence without gaps."},"taxInvoiceId":{"type":"string","format":"uuid"},"taxInvoiceNumber":{"type":"string","readOnly":true},"kind":{"type":"string","enum":["full","partial"]},"reason":{"type":"string","enum":["refund","cancellation","priceAdjustment","returnOfGoods","billingError","other"]},"refundId":{"type":"string","format":"uuid","nullable":true},"cancelledOrderId":{"type":"string","format":"uuid","nullable":true},"legalEntityId":{"type":"string","format":"uuid"},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"note":{"type":"string","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinCreditMemoLine"}},"scopePath":{"type":"string","readOnly":true}}},
"FinCreditMemoLine": {"type":"object","required":["invoiceLineNumber","netAmount","taxAmount","grossAmount"],"properties":{"invoiceLineNumber":{"type":"integer","minimum":1},"description":{"type":"string","maxLength":500},"quantity":{"type":"number","nullable":true},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxRate":{"type":"number"},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinEInvoiceTransmissionStatus": {"type":"string","description":"6.1.1. `notRequired` where the legal entity's provider is `disabled` or absent.","enum":["notRequired","queued","sent","accepted","rejected","failed"]},
"FinIssueTaxInvoiceRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["invoiceType","orderIds"],"properties":{"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"orderIds":{"type":"array","minItems":1,"description":"One order for `simplified` and `full`; one or more for `consolidated`. Every order must be paid, of one buyer, one legal entity and one currency.","items":{"type":"string","format":"uuid"}},"recipient":{"$ref":"#/components/schemas/FinTaxInvoiceRecipient"},"languages":{"type":"array","description":"Overrides the template's languages for this document, within those the template offers.","items":{"type":"string","pattern":"^[a-z]{2}(-[A-Z]{2})?$"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true,"description":"A simplified invoice this full invoice replaces for the same supply. Refused unless the law allows it (make-or-break on issueTaxInvoice)."},"deliverToEmail":{"type":"string","format":"email","nullable":true,"description":"Sends the PDF on issue as well as returning it."}}},
"FinTaxCategory": {"type":"string","description":"How a line is treated for VAT. Taken from the tax code the line was posted with.","enum":["standardRated","zeroRated","exempt","outOfScope","reverseCharge"]},
"FinTaxDocumentRendition": {"x-ticvai-persistence":"none — a signed link to the stored PDF","type":"object","required":["documentId","documentKind","url","expiresAt"],"properties":{"documentId":{"type":"string","format":"uuid"},"documentKind":{"type":"string","enum":["taxInvoice","creditMemo"]},"documentNumber":{"type":"string"},"language":{"type":"string","nullable":true},"contentType":{"type":"string","default":"application/pdf"},"url":{"type":"string","format":"uri"},"expiresAt":{"type":"string","format":"date-time"}}},
"FinTaxInvoice": {"x-ticvai-persistence":"ledger.tax_invoice + ledger.tax_invoice_line","type":"object","description":"5.7.93, 5.10.3. **A guest tax invoice, as issued, never edited.** Corrections are credit memos. The supplier block is a snapshot of the legal entity at issue, so a later change of address does not change a document already given to a guest.","required":["id","invoiceNumber","invoiceType","status","legalEntityId","issuedAt","supplyDate","currency","netAmount","taxAmount","grossAmount","lines"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"invoiceNumber":{"type":"string","readOnly":true,"description":"Server-assigned from the legal entity's series for the document kind, in sequence and without gaps, e.g. `INV-2026-000123`. Never reused."},"invoiceType":{"$ref":"#/components/schemas/FinTaxInvoiceType"},"status":{"$ref":"#/components/schemas/FinTaxInvoiceStatus"},"legalEntityId":{"type":"string","format":"uuid"},"templateId":{"type":"string","format":"uuid","nullable":true},"venueId":{"type":"string","format":"uuid","nullable":true},"orderIds":{"type":"array","items":{"type":"string","format":"uuid"}},"supplierName":{"type":"string"},"supplierAddress":{"type":"string","nullable":true},"supplierTaxRegistrationNumber":{"type":"string","nullable":true},"buyerSubjectId":{"type":"string","format":"uuid","nullable":true,"description":"The guest the orders belong to; the key a guest's own reads filter on."},"buyerName":{"type":"string","nullable":true},"buyerAddress":{"type":"string","nullable":true},"buyerCountryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"buyerTaxRegistrationNumber":{"type":"string","nullable":true},"customerAccountId":{"type":"string","format":"uuid","nullable":true},"issuedAt":{"type":"string","format":"date-time"},"supplyDate":{"type":"string","format":"date","description":"The date of supply where it differs from the issue date (the latest order's payment date on a consolidated invoice). A day in the region's time zone."},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmountInLegalCurrency":{"$ref":"../shared/common.yaml#/components/schemas/Money","description":"The tax in the legal entity's currency (AED in the UAE) where the invoice currency differs, at the rate the orders were stored at."},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"languages":{"type":"array","items":{"type":"string"}},"supersedesInvoiceId":{"type":"string","format":"uuid","nullable":true},"renditionAssetId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"The PDF rendered at issue; read through getTaxDocumentRendition."},"eInvoiceStatus":{"$ref":"#/components/schemas/FinEInvoiceTransmissionStatus"},"issuedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"Null where the platform issued it."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/FinTaxInvoiceLine"}},"taxSummary":{"type":"array","x-ticvai-persisted":false,"description":"VAT per rate and category, summed from the lines for the response.","items":{"type":"object","properties":{"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxRate":{"type":"number"},"taxableAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}}},"scopePath":{"type":"string","readOnly":true,"description":"**The partition key** (ADR-0005). Written at the scope of the venue the orders were sold at, or the region for a consolidated invoice across venues."}}},
"FinTaxInvoiceLine": {"type":"object","description":"One line as it was sold and taxed. Amounts are in the invoice currency.","required":["lineNumber","description","quantity","netAmount","taxAmount","grossAmount","taxCategory"],"properties":{"lineNumber":{"type":"integer","minimum":1},"orderId":{"type":"string","format":"uuid"},"orderLineId":{"type":"string","format":"uuid","nullable":true},"description":{"type":"string","maxLength":500},"quantity":{"type":"number"},"unitPrice":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"discountAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxCodeId":{"type":"string","format":"uuid","nullable":true},"taxRate":{"type":"number","minimum":0,"maximum":100},"taxCategory":{"$ref":"#/components/schemas/FinTaxCategory"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"creditedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"}}},
"FinTaxInvoiceRecipient": {"x-ticvai-persistence":"none — copied onto the invoice as buyer columns","type":"object","description":"Who the invoice is addressed to. Required for `full` and `consolidated`.","required":["name"],"properties":{"name":{"type":"string","maxLength":300},"address":{"type":"string","maxLength":1000,"nullable":true},"countryCode":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"taxRegistrationNumber":{"type":"string","maxLength":30,"nullable":true,"description":"The recipient's TRN where they are VAT-registered."},"customerAccountId":{"type":"string","format":"uuid","nullable":true,"description":"The B2B credit account (payments `B2bCreditAccount`) where a company is invoiced."}}},
"FinTaxInvoiceStatus": {"type":"string","description":"`issued` until a credit memo is issued against it; `superseded` where a full invoice replaced a simplified one for the same supply (only if the law allows it; see issueTaxInvoice).","enum":["issued","partiallyCredited","fullyCredited","superseded"]},
"FinTaxInvoiceType": {"type":"string","description":"5.7.93. `simplified` for one order with no recipient details, `full` for one order with them, `consolidated` for several paid orders of one buyer on one invoice.","enum":["simplified","full","consolidated"]},
"GuestDevice": {"type":"object","x-ticvai-persistence":"marketing.guest_device","required":["id","subjectId","platform","status","registeredAt"],"properties":{"id":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["ios","android","web"]},"tokenFingerprint":{"type":"string","description":"Hash of the token, not the token. The token itself is write-only — returning it would put a push credential in every response a support agent can read.\n"},"tokenRef":{"type":"string","writeOnly":true,"description":"**A vault reference to the push token**, written by the server from `registerGuestDevice.token` — the same pattern as `PaymentProvider.credentialRef`. Never the token and never returned; the sender resolves it at send time. Without it a registered device could not be sent to.\n"},"appVersion":{"type":"string","nullable":true},"osVersion":{"type":"string","nullable":true},"deviceModel":{"type":"string","nullable":true},"locale":{"type":"string","nullable":true},"status":{"type":"string","enum":["active","revoked","failed"]},"failureCount":{"type":"integer","description":"Consecutive delivery failures. Past the threshold the device is marked failed and stops being targeted — a dead token retried forever is wasted quota and a misleading delivery rate.\n"},"registeredAt":{"type":"string","format":"date-time"},"lastSeenAt":{"type":"string","format":"date-time","nullable":true},"revokedAt":{"type":"string","format":"date-time","nullable":true}}},
"GuestPreferences": {"type":"object","x-ticvai-persistence":"marketing.guest_preference","description":"**What the guest likes, kept apart from what they permit** (consent) and from who they are (the profile). One row per subject. `dietary` and `accessibility` are here rather than as tags because BL-134 gives them their own consent purpose and retention.\n","properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid","readOnly":true},"seatingPreference":{"type":"string","nullable":true,"maxLength":200},"drinkPreferences":{"type":"array","items":{"type":"string"}},"dietary":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"accessibility":{"type":"array","description":"Also written by `updateMyProfile`.","items":{"type":"string"}},"preferredChannel":{"allOf":[{"$ref":"#/components/schemas/MessageChannel"}],"x-ticvai-persisted":false,"description":"**Stored on the profile** (`GuestProfile.preferredChannel`) — carried here because the preference screen edits it beside the rest.\n"},"updatedAt":{"type":"string","format":"date-time","readOnly":true}}},
"GuestProfile": {"x-ticvai-persistence":"marketing.guest_profile","type":"object","required":["subjectId","isActive"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"subjectId":{"type":"string","format":"uuid","description":"Opaque reference. Personal data lives in the separately erasable store, which is what makes erasure possible against an append-only ledger.\n"},"displayName":{"type":"string","nullable":true},"email":{"type":"string","nullable":true},"phone":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"preferredChannel":{"$ref":"#/components/schemas/MessageChannel"},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells. Marketing acts locally."},"tags":{"type":"array","items":{"type":"string"}},"engagementScore":{"type":"integer","nullable":true,"minimum":0,"maximum":100,"description":"22.2.20 and 22.2.21. **`lifetimeValue` and `visitCount` existed, so value was a stored figure and engagement was not.** They are different questions: a guest who spent a lot once and a guest who visits monthly have the same LTV and need opposite treatment.\n**Recency, frequency and breadth, not spend** — spend is already `lifetimeValue`, and folding it in here would make one number twice.\n"},"engagementTier":{"type":"string","nullable":true,"enum":["new","active","occasional","lapsing","lapsed","dormant"],"description":"5.3.19. **Automatic classification, computed rather than assigned.** `lapsing` is the tier the whole field exists for — **a guest who has not been for a while and still might is the only one marketing can change**, and lumping them with `lapsed` wastes the window.\n"},"lifetimeValue":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"visitCount":{"type":"integer"},"lastVisitAt":{"type":"string","format":"date-time","nullable":true},"isActive":{"type":"boolean"},"mergedIntoSubjectId":{"type":"string","format":"uuid","nullable":true,"readOnly":true,"description":"**Set on the absorbed profile by `mergeGuestProfiles` and `mergeGuests`**, which retain it as a redirect rather than deleting it. A read that lands here follows it; a second merge of a profile that has one is refused as `alreadyMerged`.\n"},"mergedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true}}},
"GuestProfileDetail": {"x-ticvai-persistence":"marketing.guest_profile","allOf":[{"$ref":"#/components/schemas/GuestProfile"},{"type":"object","properties":{"id":{"type":"string","format":"uuid","readOnly":true,"description":"**Added 20 August.** The schema reference derives table columns from API response schemas, and a response is not a table — this one returned everything a caller needs and not the row's own identity, so the table had no key and no row could be addressed, updated or deleted. Found by an audit of all 365 tables, not by a reader.\n"},"consents":{"$ref":"#/components/schemas/ConsentState"},"loyalty":{"$ref":"#/components/schemas/LoyaltyPosition"},"openCaseCount":{"type":"integer"},"recentOrderIds":{"type":"array","items":{"type":"string"}},"membershipIds":{"type":"array","items":{"type":"string","format":"uuid"}},"notes":{"type":"string","nullable":true}}}]},
"GuestSession": {"x-ticvai-persistence":"none — Redis session registry","type":"object","required":["subjectId","tokens","isVerified","expiresAt"],"properties":{"subjectId":{"type":"string","format":"uuid"},"displayName":{"type":"string","nullable":true},"tokens":{"$ref":"#/components/schemas/TokenPair"},"isVerified":{"type":"boolean","description":"False until an OTP or a verified provider identity confirms ownership. An unverified account may browse and fill a cart but not transact: the gate is the checkout page (ADR-0045), where `checkoutCart` refuses it until the guest verifies or proves the contact by code. UAE Pass returns a verified identity, so it starts true. Rule on `verifyGuestEmail`, decided 17 September 2026.\n"},"identityProviders":{"type":"array","description":"Linked providers. Several may resolve to one account.","items":{"type":"string","enum":["password","otp","apple","google","uaePass"]}},"guestLinkId":{"type":"string","nullable":true,"description":"Present where the guest is linked across cells (ADR-0010)."},"requiresMfa":{"type":"boolean","default":false,"description":"True only where the sign-in venue enabled guest two-step verification (`VenueSettings.identity.guestTwoStep`, in tenancy) and this guest has an active method (decided 29 September, rev 3 GAP-B1, per venue). The session is then not usable until `verifyMfaChallenge` succeeds on a `signIn` challenge. Always false for a UAE Pass sign-in, which is already a verified two-factor identity (proposed, client to correct).\n"},"mfaMethods":{"type":"array","description":"The guest's active methods, so the client can offer the right one. Empty when `requiresMfa` is false.","items":{"$ref":"#/components/schemas/MfaMethod"}},"homeCellName":{"type":"string","nullable":true},"preferredLanguage":{"type":"string","nullable":true},"expiresAt":{"type":"string","format":"date-time","description":"**30 days, sliding** (decided 28 September, audit R126 (2)): each use of the session moves this to 30 days from now, and 30 days unused ends it. **One session per device**: a guest may be signed in on a phone and a laptop at once, and a new sign-in on the same `deviceId` ends that device's previous session.\n"}}},
"IdentityGuestDocumentSubmission": {"type":"object","x-ticvai-persistence":"none — request only; the document goes to pii.subject_document and the verification to identity.guest_identity_verification","required":["documentKind","documentNumber","documentAssetId"],"properties":{"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"],"description":"The vocabulary of `pii.subject_document.kind`."},"documentNumber":{"type":"string","format":"password","writeOnly":true,"maxLength":64,"description":"**Write-only, never returned.** Hashed on arrival; only the last four are kept in clear."},"issuingCountry":{"type":"string","pattern":"^[A-Z]{2}$","nullable":true},"expiresOn":{"type":"string","format":"date","nullable":true},"documentAssetId":{"type":"string","format":"uuid","description":"The uploaded scan or photo of the document."},"selfieAssetId":{"type":"string","format":"uuid","nullable":true,"description":"A live photo for the reviewer to compare, where the policy asks for one. Deleted with the scan."},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"],"default":"policyRequired","description":"What the guest is verifying for; the review queue shows it."}}},
"IdentityGuestVerification": {"type":"object","x-ticvai-persistence":"identity.guest_identity_verification","description":"**One guest identity-document verification** (5.3.21; decided 29 September, build pass): the document it checks, its status, the method and who decided. The document itself is `pii.subject_document`; this row holds no document number.","required":["id","subjectId","status","submittedAt"],"properties":{"id":{"type":"string","format":"uuid","readOnly":true},"subjectId":{"type":"string","format":"uuid"},"subjectDocumentId":{"type":"string","format":"uuid","description":"The `pii.subject_document` row submitted."},"documentKind":{"type":"string","enum":["passport","emiratesId","nationalId","drivingLicence","residencePermit","other"]},"documentNumberLast4":{"type":"string","maxLength":4,"nullable":true,"readOnly":true},"reason":{"type":"string","enum":["policyRequired","ageRestrictedPurchase","residentPricing","accountRecovery"]},"status":{"type":"string","enum":["pending","verified","rejected","resubmissionRequested"],"readOnly":true},"method":{"type":"string","enum":["manualReview","documentScanner","provider"],"nullable":true,"readOnly":true},"decisionReason":{"type":"string","maxLength":300,"nullable":true,"readOnly":true},"decidedByPrincipalId":{"type":"string","format":"uuid","nullable":true,"readOnly":true},"submittedAt":{"type":"string","format":"date-time","readOnly":true},"decidedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true},"documentImageDeletedAt":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When the scan (and any selfie) was deleted under the policy's retention."}}},
"Invitation": {"type":"object","x-ticvai-persistence":"marketing.invitation","description":"**Addressed and tokenised.** A guest accepting an invitation is claiming a specific place, not buying one.\n","required":["id","campaignId","token","status"],"properties":{"id":{"type":"string","format":"uuid"},"campaignId":{"type":"string","format":"uuid"},"subjectId":{"type":"string","format":"uuid","nullable":true},"recipientEmail":{"type":"string","format":"email","nullable":true},"token":{"type":"string","description":"**Single-use and unguessable.** An invitation link forwarded to a group chat is the failure mode, and a token that survives its first use is one that ends up there.\n"},"plusOnes":{"type":"integer","default":0},"status":{"type":"string","enum":["issued","viewed","accepted","declined","expired","revoked"]},"entitlementIds":{"type":"array","items":{"type":"string","format":"uuid"}},"respondedAt":{"type":"string","format":"date-time","nullable":true},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"LoyaltyPosition": {"x-ticvai-persistence":"marketing.loyalty_position","type":"object","required":["subjectId","programmeId","pointsBalance","tierCode"],"properties":{"leaderboardNickname":{"type":"string","nullable":true,"maxLength":24,"description":"BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever they reach the board and changeable afterwards; `setLeaderboardNickname` is the only thing that writes it.\n**Null means the guest has not chosen one yet, and the board shows a generated `Player-4821` in its place** — never `pii.subject.display_name`, which would disclose silently on the day a guest first placed and is the case this field exists to prevent.\n**The generated name is computed at read time and not stored here.** Writing it would make *\"has this guest chosen a name\"* unanswerable, and that flag is what the prompt-on-reaching-the-board depends on.\n"},"subjectId":{"type":"string","format":"uuid"},"programmeId":{"type":"string","format":"uuid"},"pointsBalance":{"type":"integer"},"lifetimePoints":{"type":"integer"},"tierId":{"type":"string","format":"uuid","nullable":true,"description":"**The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September with `marketing.programme_tier`: the two strings were a cache of something that did not exist, and a cache with no source cannot be rebuilt or audited.\n"},"tierCode":{"type":"string"},"tierName":{"type":"string"},"pointsToNextTier":{"type":"integer","nullable":true},"nextExpiryPoints":{"type":"integer","nullable":true},"nextExpiryAt":{"type":"string","format":"date-time","nullable":true}}},
"MessageChannel": {"type":"string","enum":["email","sms","whatsapp","push","inApp","post"]},
"MfaMethod": {"x-ticvai-persistence":"identity.mfa_method","type":"object","required":["id","kind","isActive","enrolledAt"],"properties":{"id":{"type":"string","format":"uuid"},"kind":{"$ref":"#/components/schemas/MfaKind"},"label":{"type":"string","nullable":true},"maskedTarget":{"type":"string","nullable":true,"description":"Partially masked destination, so a person can tell two methods apart."},"isActive":{"type":"boolean"},"isPrimary":{"type":"boolean"},"enrolledAt":{"type":"string","format":"date-time"},"lastUsedAt":{"type":"string","format":"date-time","nullable":true}}},
"Order": {"x-ticvai-persistence":"orders.sales_order + orders.order_line","type":"object","required":["id","venueId","scopePath","channel","status","currency","currencyScale","grossAmount","taxAmount","netAmount","lines","createdAt","recordedAt"],"properties":{"id":{"type":"string","format":"uuid","description":"The client UUIDv7 from `CreateOrderRequest.id`."},"orderNumber":{"type":"string","readOnly":true,"description":"The number a guest reads and a cashier types. **Server-assigned: the venue prefix and a sequence per venue**, for example `DXB1-000123` (decided 28 September, audit R152). A till holds a reserved range of the venue sequence, so an order taken offline gets its number on the till and keeps it through `syncOrders`. **Not gapless**: an unused reserved range leaves a gap, and that is allowed. Only tax invoices are gapless, per legal entity. The receipt carries this number.\n"},"channel":{"allOf":[{"$ref":"#/components/schemas/OrderChannel"}],"description":"Where it came from. Drives revenue attribution, promotion eligibility and the self-service adoption figures the operator will ask for within a month of launch.\n"},"venueId":{"type":"string","format":"uuid"},"scopePath":{"type":"string"},"status":{"$ref":"#/components/schemas/OrderStatus"},"currency":{"type":"string","pattern":"^[A-Z]{3}$","x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else. **Kept on the wire , removed from the table** — a client should not walk a hierarchy to read a figure, and the  database should not hold nine million copies of AED. Four tables genuinely differ from their\n region and keep a stored currency: `orders.payment.tender_currency`, `inventory.supplier`, \n`ledger.account`, `control.partner_agreement`.\n"},"currencyScale":{"type":"integer","minimum":0,"maximum":4,"x-ticvai-persisted":false,"description":"**Resolved from the region, not stored** (ADR-0018, 24 August). Region-scoped and not overri dable below, so a row in a UAE region is AED and cannot be anything else — storing it per ro w is a copy of a fact that cannot differ. **Kept on the wire, removed from the table**: a cl ient reading a figure should not walk a hierarchy to know what it means, and the database sh ould not hold nine million copies of AED. Four tables genuinely differ from their region and\n keep a stored currency — `orders.payment.tender_currency`, `inventory.supplier`, `ledger.ac\ncount`, `control.partner_agreement`. **A guest paying USD at an AED venue is a real row; a w orkstation with its own currency is a misconfiguration.**\n"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"refundedAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"droppedPromotions":{"type":"array","readOnly":true,"x-ticvai-persisted":false,"description":"**Promotions left off this order at checkout because their budget cap would have been exceeded** (decided 28 September, audit R101 (8)). Empty when none was dropped. Returned by `checkoutCart` and `createOrder`, not stored.\n","items":{"type":"object","required":["promotionId"],"properties":{"promotionId":{"type":"string","format":"uuid"},"name":{"type":"string"},"reason":{"type":"string","enum":["budgetCapReached"]}}}},"totalPriceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Sum across lines. Zero on a normal order."},"lines":{"type":"array","items":{"$ref":"#/components/schemas/OrderLine"}},"payments":{"type":"array","items":{"$ref":"#/components/schemas/Payment"}},"principalId":{"type":"string","format":"uuid"},"workstationId":{"type":"string","format":"uuid"},"shiftId":{"type":"string","format":"uuid","nullable":true},"subjectId":{"type":"string","format":"uuid","nullable":true},"holdLabel":{"type":"string","maxLength":60,"nullable":true,"readOnly":true,"description":"The `label` a cashier gave when parking it with `holdOrder` — how they find it again. Null on an order never held."},"heldUntil":{"type":"string","format":"date-time","nullable":true,"readOnly":true,"description":"When a held order expires and is voided (states/order.yaml), from `holdOrder`'s `holdUntil`. Null on an order not currently held."},"createdAt":{"type":"string","format":"date-time"},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"OrderChannel": {"type":"string","description":"Where the order originated. Added when guest self-ordering was contracted — an order a guest placed on their own phone is commercially and operationally different from one a cashier typed, and reporting that cannot separate them cannot answer whether self-ordering is working.\n","enum":["pos","kiosk","guestApp","guestWeb","callCentre","partner","api","backOffice"]},
"OrderLine": {"x-ticvai-persistence":"orders.order_line + orders.order_line_eligibility + orders.order_line_discount","x-ticvai-retired-columns":["promotion_id","name","reason"],"allOf":[{"$ref":"#/components/schemas/CreateOrderLine"},{"type":"object","required":["serverUnitPrice","taxAmount","netAmount","grossAmount"],"properties":{"serverUnitPrice":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"What the server computed on ingest."},"priceVariance":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"Server minus quoted. Non-zero means the quoted price was honoured and the difference posted to the variance account.\n"},"taxAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"netAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"grossAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"entitlementIds":{"type":"array","description":"The entitlements this line issued. **These are the ticket ids** — `transferOrderTickets.ticketIds` and `reprintOrder.reissuedTicketIds` take and return them.","items":{"type":"string","format":"uuid"}},"crossRegionRightIds":{"type":"array","items":{"type":"string"},"description":"Redemption rights propagated to other cells for this line."},"reprintCount":{"type":"integer","minimum":0,"default":0,"readOnly":true,"description":"How many times this line's tickets were reprinted or resent. `reprintOrder` increments it; repeated reprints are the signal worth surfacing."},"venueId":{"type":"string","format":"uuid","readOnly":true,"description":"The order's venue, copied onto the line (ADR-0044's own example; system-design review SD-008, 29 September) so a line is scoped and partitionable without its order."},"discounts":{"type":"array","readOnly":true,"description":"**The discounts applied to this line, one row each** (system-design review SD-008, 29 September). Until then a discount object was flattened into the line as `promotion_id NOT NULL`, so a line with no promotion could not be inserted. A line with no discount has none.","items":{"$ref":"#/components/schemas/OrderLineDiscount"}}}}]},
"OrderStatus": {"type":"string","enum":["pending","held","paid","partiallyPaid","completed","voided","refunded","partiallyRefunded","failed"],"description":"`held` is a parked sale — the cashier freed the till and the guest will return. It holds no inventory and expires, because a till that accumulates parked sales across a shift cannot be closed.\n"},
"Page": {"type":"object","required":["items","hasMore"],"properties":{"items":{"type":"array","items":{}},"nextCursor":{"type":"string"},"hasMore":{"type":"boolean"}}},
"Payment": {"x-ticvai-persistence":"orders.payment","type":"object","required":["id","orderId","tender","amount","status","recordedAt"],"properties":{"id":{"type":"string","format":"uuid"},"orderId":{"type":"string","format":"uuid"},"tender":{"$ref":"#/components/schemas/TenderKind"},"tenderCurrency":{"type":"string","pattern":"^[A-Z]{3}$","description":"4.6.11. **What the guest actually handed over**, which is not always what the venue books. A tourist paying USD cash at a till is a foreign tender; the sale is still recorded in base currency.\nEqual to the base currency for almost every payment. **Present on all of them so the foreign-tender report has a source** — `getForeignTenderReport` promised *what was taken in which currency* and nothing recorded it until 18 August.\n"},"tenderAmount":{"allOf":[{"$ref":"../shared/common.yaml#/components/schemas/Money"}],"description":"The amount in `tenderCurrency`, at that currency's own scale."},"fxRate":{"allOf":[{"$ref":"#/components/schemas/ExchangeRateDecimal"}],"nullable":true,"description":"The rate applied, **stored on the payment rather than looked up later** (CF-37). A payment reconciled next month is reconciled at the rate of the day it was taken.\n"},"fxRateSource":{"type":"string","nullable":true,"enum":["manual","feed","cardScheme"],"description":"4.2.8. Manual or fed on a schedule. **`cardScheme` is where the terminal did the conversion and told us** — dynamic currency conversion, the scheme's rate rather than ours.\n"},"changeCurrency":{"type":"string","pattern":"^[A-Z]{3}$","nullable":true,"description":"4.6.11 is deliberately asymmetric: **accept foreign currency, refund in local.** A till giving change in five currencies needs five floats and five counts, and the variance becomes unattributable.\n"},"amount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"changeAmount":{"$ref":"../shared/common.yaml#/components/schemas/Money"},"status":{"type":"string","enum":["authorised","captured","pendingConfirmation","declined","failed","voided","refunded"]},"providerName":{"type":"string","nullable":true},"providerReference":{"type":"string","nullable":true,"description":"The provider's own id for the charge (Stripe PaymentIntent, NI order reference). What `payments.receivePaymentProviderWebhook` matches an incoming event on (SD-034)."},"providerIdempotencyKey":{"type":"string","nullable":true,"readOnly":true,"description":"The idempotency key sent to the provider, which is this payment's `id` (SD-034, 29 September). A retried provider call cannot charge twice."},"terminalId":{"type":"string","format":"uuid","nullable":true,"description":"The card terminal a till payment ran on (ECR flow, SD-034)."},"nextAction":{"type":"object","nullable":true,"x-ticvai-persisted":false,"description":"**What the caller does while the payment is `pendingConfirmation`** (SD-034, 29 September). `redirect`: send the browser to `url` (3-D Secure challenge or hosted page); the provider returns the guest to `returnUrl` and the result arrives by webhook. `terminal`: the card terminal has been instructed; wait for its result. Null once the payment has an outcome.","properties":{"kind":{"type":"string","enum":["redirect","terminal"]},"url":{"type":"string","format":"uri","nullable":true},"expiresAt":{"type":"string","format":"date-time","nullable":true}}},"lastInquiryAt":{"type":"string","format":"date-time","nullable":true},"recordedAt":{"type":"string","format":"date-time"},"syncedAt":{"type":"string","format":"date-time","nullable":true}}},
"RecordConsentRequest": {"x-ticvai-persistence":"none — request only","type":"object","required":["purpose","decision","noticeVersion","source","recordedAt"],"properties":{"purpose":{"$ref":"#/components/schemas/ConsentPurpose"},"decision":{"$ref":"#/components/schemas/ConsentDecision"},"channels":{"type":"array","description":"Omit to apply to every channel the purpose covers.","items":{"$ref":"#/components/schemas/MessageChannel"}},"noticeVersion":{"type":"string"},"source":{"$ref":"#/components/schemas/ConsentSource"},"recordedAt":{"type":"string","format":"date-time"}}},
"RegisterGuestRequest": {"type":"object","required":["identifier","channel"],"properties":{"identifier":{"type":"string","maxLength":256,"description":"Email address or mobile number in E.164."},"channel":{"type":"string","enum":["email","sms","whatsapp"]},"displayName":{"type":"string","maxLength":200},"password":{"type":"string","minLength":8,"maxLength":256,"writeOnly":true,"description":"Optional. OTP-only accounts are supported and are the default."},"preferredLanguage":{"type":"string","pattern":"^[a-z]{2}$"},"consents":{"type":"array","description":"Consent captured at registration, recorded with the notice version.","items":{"type":"object","properties":{"purpose":{"type":"string"},"granted":{"type":"boolean"},"noticeVersion":{"type":"string"}}}}}},
"Session": {"type":"object","required":["sessionId","principalId","roleId","scope","effectivePermissions","saleBoardId"],"properties":{"sessionId":{"type":"string","format":"uuid"},"principalId":{"type":"string","format":"uuid"},"roleId":{"type":"string","format":"uuid"},"displayName":{"type":"string"},"scope":{"type":"array","description":"Scope nodes this session may act within, resolved once at login from the ltree hierarchy with deny-overrides-allow. Clients filter navigation against this — they never compute it.\n","items":{"$ref":"../shared/common.yaml#/components/schemas/ScopeRef"}},"effectivePermissions":{"allOf":[{"$ref":"../shared/permissions.yaml#/components/schemas/PermissionSet"}],"description":"Flattened set across all granted scopes, after deny resolution. Convenience for coarse checks. Anything scope-sensitive must use `permissionsByScope`.\n"},"permissionsByScope":{"type":"array","description":"Permissions effective at each granted scope path. Clients filter navigation on this and never compute permissions themselves.\n","items":{"$ref":"../shared/permissions.yaml#/components/schemas/ScopedPermissions"}},"saleBoardId":{"type":"string","format":"uuid","description":"Landing surface, derived from the WORKSTATION, not the role (12 Aug 2026 §3). Ticketing, F&B or Retail board.\n"},"workstation":{"$ref":"#/components/schemas/WorkstationContext"},"openedAt":{"type":"string","format":"date-time"},"expiresAt":{"type":"string","format":"date-time"}}},
"TokenPair": {"x-ticvai-persistence":"none — transient","type":"object","required":["accessToken","refreshToken","expiresIn"],"properties":{"accessToken":{"type":"string","description":"JWT carrying `sid`, validated per request against the session registry."},"refreshToken":{"type":"string"},"expiresIn":{"type":"integer","description":"Seconds"}}},
"WalletPass": {"type":"object","x-ticvai-persistence":"orders.wallet_pass","description":"BL-029. **`appleWallet` and `googlePay` are feature toggles on the native apps** — there is no pass generation, no update push, no serial and no authentication token.\n**A wallet pass is a live object, not a download.** The value over a PDF is that it updates: a changed gate, a cancelled performance, a time that moved. **A pass that cannot be pushed to is a screenshot with better rounding.**\n","required":["id","entitlementId","platform","serialNumber","status"],"properties":{"id":{"type":"string","format":"uuid"},"entitlementId":{"type":"string","format":"uuid"},"platform":{"type":"string","enum":["apple","google"]},"serialNumber":{"type":"string"},"authenticationToken":{"type":"string","format":"password","writeOnly":true,"description":"**Write-only.** How the device proves it may fetch an update, and the reason a leaked serial alone is not enough to read somebody's ticket.\n"},"status":{"type":"string","enum":["issued","updated","voided","expired"]},"lastPushedAt":{"type":"string","format":"date-time","nullable":true},"deviceRegistrations":{"type":"integer","description":"How many devices hold it. **A guest with the pass on a phone and a watch is one entitlement and two registrations**, and both need the update.\n"},"scopePath":{"type":"string","description":"**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `venue` scope.**"}}},
"Wishlist": {"type":"object","required":["subjectId","items"],"x-ticvai-persistence":"none — wrapper. The items are the table, keyed by subject","properties":{"subjectId":{"type":"string","format":"uuid"},"items":{"type":"array","x-ticvai-persistence":"marketing.wishlist_item","items":{"type":"object","required":["id","variantId","addedAt","isAvailable"],"properties":{"id":{"type":"string","format":"uuid"},"variantId":{"type":"string","format":"uuid"},"productName":{"type":"string"},"performanceId":{"type":"string","format":"uuid","nullable":true},"performanceStartsAt":{"type":"string","format":"date-time","nullable":true},"price":{"x-ticvai-column":"list_price","$ref":"../shared/common.yaml#/components/schemas/Money","description":"The variant's current list price when the wishlist is read. Stored as `list_price` (naming-and-style 5.1 bans a bare `price` column); the wire keeps `price`."},"imageAssetRef":{"type":"string","nullable":true},"isAvailable":{"type":"boolean","description":"False where the product has been withdrawn or the performance has passed. Returned rather than dropped — a guest who saved something and finds it silently gone assumes the feature is broken.\n"},"unavailableReason":{"type":"string","nullable":true},"note":{"type":"string","nullable":true},"addedAt":{"type":"string","format":"date-time"}}}}}},
"WorkstationContext": {"type":"object","required":["id","code","venueId","regionId"],"properties":{"id":{"type":"string","format":"uuid"},"code":{"type":"string"},"venueId":{"type":"string","format":"uuid"},"regionId":{"type":"string","format":"uuid"},"accessPointId":{"type":"string","format":"uuid","description":"Inherited from the workstation, never selected by the operator."},"devices":{"type":"array","items":{"type":"object","required":["kind","driver"],"properties":{"kind":{"type":"string","enum":["receiptPrinter","ticketPrinter","cashDrawer","barcodeScanner","rfidReader","paymentTerminal","customerDisplay"]},"driver":{"type":"string"},"identifier":{"type":"string"}}}},"currency":{"type":"string","pattern":"^[A-Z]{3}$"},"currencyScale":{"type":"integer","minimum":0,"maximum":4},"timezone":{"type":"string"},"cellName":{"type":"string","description":"The cell serving this workstation's region. One cell per tenant per region (ADR-0014). A client uses this only for diagnostics and telemetry tagging — never for routing, which the Control Plane resolves.\n"},"deploymentProfile":{"type":"string","enum":["terminalLocal","venueEdge","thin"],"description":"Whether this surface reads catalogue locally (ADR-0013). Determines which flows the client enables offline.\n"}}}
}
```
