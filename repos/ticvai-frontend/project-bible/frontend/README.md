# Frontend linkage

**Screens declare which app implements them. Everything else is derived.**

    ../screens/P*.yaml       the source — each screen carries an `implementation` block
    web-b2c.yaml             per-app manifest, generated
    ../tools/link-frontend.py
    ../tools/check-frontend.py

## What a screen declares

```yaml
implementation:
  app: web-b2c
  route: /discovery-and-browse/home-landing
  component: apps/web-b2c/src/routes/discovery-and-browse/HomeLandingDashboard.tsx
  status: notStarted
```

Route and component path are conventional, derived from the module and screen name. A file
can be found from a screen id and a screen id from a file, without either side maintaining
a lookup table.

## What the app manifest gives you

Per app: which platforms it serves, which packages it depends on, **which contracts it
consumes**, screen count by wave, and every route.

`contracts` is the useful one. `web-b2c` touches eight — catalogue, identity, marketing-crm,
orders, promotions, retail, seating, white-label. That is the api-client generation scope for
that app, and it comes from the screens rather than from someone's memory.

## What the check catches

| | |
|---|---|
| **App does not exist** | 73 screens are assigned to four apps nobody has scaffolded |
| **Route collision** | Two screens on one route surfaces as "sometimes the wrong page loads" |
| **Component path off convention** | Breaks the find-one-from-the-other property |
| **Offline app without offline-core** | An app that queues writes without it does not queue them anywhere |

## The finding

**Six apps exist. Nine platforms need one.**

| App | Screens | |
|---|---|---|
| web-b2c | 29 | scaffolded |
| **platform-admin** | **36** | **not scaffolded** |
| **partner-portal** | **21** | **not scaffolded** |
| **support-console** | 8 | **not scaffolded** |
| **accreditation** | 8 | **not scaffolded** |

Two of the four were always in the proposal — the partner portal and the platform console.
They were missed because they have no UI/UX board, and the boards were what the frontend plan
was built from.

The other 203 screens on P02, P04, P06, P07, P08 and P13 have no screen definitions yet, so
their apps show zero here. That is a gap in the definitions, not in the apps — those six are
scaffolded and the definitions are the next step.
