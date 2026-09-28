# "Help me choose" (Build your experience) — CMS setup

A short quiz that points a guest to the right product before they see the ticket list. It is live today for Kids Club.

## Where it is configured
Config drawer → **Build your experience**

- **Help me choose**
  - *Button on booking page* (default): shows a "Not sure which to pick? Help me choose" button above the products.
  - *Pop-up on arrival*: opens the quiz automatically the first time the guest lands on the booking page. If they close it, it stays closed for that session.
  - *Off*: hides it.
- **Questions**: 2 questions (default) or 1 question.

## What the venue sets up in the CMS (per venue)
1. **Questions**: the question text, up to 2 per venue.
2. **Answers**: 3 per question. Each answer has a title, a one-line description, an icon and an optional badge ("Best value").
3. **Answer → product mapping**: each answer points to one booking flow (for example Play pass, Workshop or Membership).
4. **Result card**: the title, description and image shown for each product the quiz can recommend.
5. **Placement**: the Help me choose setting above.

The guest's last answer decides the recommendation. "Use this" opens the booking flow for that product with nothing pre-selected.

## Ticket tags (related)
The tags on ticket cards (for example 1 Hour, Min 75 cm, Free adult entry) come from each ticket's `tags` field in the CMS. That field is a list of type and label pairs. The types are clock, height, free, cal and id. If a ticket has no tags, they are worked out from its duration, validity and the venue's height rule. You can switch them off under Config → Steps & cards → **Tags on tickets**.
