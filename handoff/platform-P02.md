# P02 Guest App — platform

**Derived.** `python3 tools/derive-platform.py P02`. App `guest-app` · guest · mobileApp · offline-capable

| | |
|---|---|
| Screens | 63 |
| Operations | 89 |
| Contracts | 15 |
| Modules | 16 |
| Undrawn | 2 |
| Operations with no screen | 0 |
| Waves | wave1 20 · wave2 27 · wave3 16 |

## Gaps

### 6 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **catalogue** — waves 1, 2, 3
- **marketing-crm** — waves 1, 2, 3
- **orders** — waves 1, 2, 3
- **queue** — waves 1, 2, 3
- **retail** — waves 2, 3
- **white-label** — waves 1, 2, 3

### 2 screens nobody has drawn

- `GST-063` Search — wave 1
- `GST-065` Newsletter & Preferences — wave 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| orders | 16 | 1, 2, 3 |
| catalogue | 12 | 1, 2, 3 |
| fnb | 7 | 2 |
| queue | 6 | 1, 2, 3 |
| white-label | 5 | 1, 2, 3 |
| marketing-crm | 5 | 1, 2, 3 |
| retail | 2 | 2, 3 |
| access | 2 | 3 |
| cross-cell | 1 | 2 |
| games | 1 | 2 |
| ai | 1 | 2 |
| promotions | 1 | 2 |
| identity | 1 | 1 |
| TODO | 1 | 1 |
| finance | 1 | 2 |
| seating | 1 | 2 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `GST-001` | Home – Default | white-label | 1 | 1 | yes |
| `GST-002` | Explore Categories | catalogue | 1 | 1 | yes |
| `GST-003` | Attractions List | catalogue | 1 | 2 | yes |
| `GST-004` | Attraction Details | catalogue | 1 | 3 | yes |
| `GST-005` | What's On | catalogue | 1 | 2 | yes |
| `GST-006` | Event / Exhibition Details | catalogue | 1 | 2 | yes |
| `GST-007` | Select Date & Time | catalogue | 1 | 2 | yes |
| `GST-008` | Tickets & Add-ons | orders | 1 | 1 | yes |
| `GST-009` | Review & Payment | orders | 1 | 5 | yes |
| `GST-010` | Booking Confirmation | orders | 1 | 1 | yes |
| `GST-011` | Wallet Overview | retail | 2 | 2 | yes |
| `GST-012` | My Tickets | orders | 1 | 1 | yes |
| `GST-013` | Ticket Details | orders | 1 | 1 | yes |
| `GST-014` | Ticket Transfer | orders | 2 | 2 | yes |
| `GST-015` | Memberships | cross-cell | 2 | 2 | yes |
| `GST-016` | My Reservations | orders | 2 | 3 | yes |
| `GST-017` | Reservation Details | orders | 2 | 2 | yes |
| `GST-018` | Add to Calendar / Reminders | orders | 3 | 2 | yes |
| `GST-019` | Order History (Wallet) | orders | 2 | 1 | yes |
| `GST-020` | Saved Items / Wishlist | marketing-crm | 3 | 7 | yes |
| `GST-021` | Interactive Map | catalogue | 2 | 2 | yes |
| `GST-022` | Attraction Wait Times | queue | 2 | 1 | yes |
| `GST-023` | Virtual Queue / Join Queue | queue | 3 | 3 | yes |
| `GST-024` | F&B – Browse & Order | fnb | 2 | 6 | yes |
| `GST-025` | F&B – Order Tracking | fnb | 2 | 3 | yes |
| `GST-026` | Retail / Merchandise | games | 2 | 2 | yes |
| `GST-027` | Parking – Reserve & Pay | access | 3 | 2 | yes |
| `GST-028` | Parking – Reservation Confirmed | access | 3 | 2 | yes |
| `GST-029` | Venue Info & Services | fnb | 2 | 2 | yes |
| `GST-030` | In-Venue Notifications | fnb | 2 | 1 | yes |
| `GST-031` | AI Concierge – Home | fnb | 2 | 2 | yes |
| `GST-032` | AI Concierge – Chat | orders | 2 | 8 | yes |
| `GST-033` | AI Concierge – Contextual Help | ai | 2 | 1 | yes |
| `GST-034` | Lost & Found | fnb | 2 | 1 | yes |
| `GST-035` | Feedback & Ratings | marketing-crm | 3 | 1 | yes |
| `GST-036` | Loyalty & Rewards | marketing-crm | 2 | 2 | yes |
| `GST-037` | Offers & Promotions | promotions | 2 | 3 | yes |
| `GST-038` | Digital Companion Mode | white-label | 3 | 3 | yes |
| `GST-039` | Profile | marketing-crm | 1 | 1 | yes |
| `GST-040` | Help & Support | white-label | 2 | 4 | yes |
| `GST-041` | Checkout Entry | orders | 1 | 2 | yes |
| `GST-042` | Simple Registration & OTP | identity | 1 | 21 | yes |
| `GST-043` | Arabic / RTL Experience | TODO | 1 | 0 | yes |
| `GST-044` | Multi-Currency & Pricing | finance | 2 | 2 | yes |
| `GST-045` | Ticket Delivery & Sharing | orders | 2 | 1 | yes |
| `GST-046` | Branded Queue / Waiting Room | queue | 1 | 1 | yes |
| `GST-047` | Maintenance / Upgrade Page | white-label | 1 | 1 | yes |
| `GST-048` | Upsell / Cross-Sell | orders | 2 | 2 | yes |
| `GST-049` | Interactive Seat Selection | seating | 2 | 3 | yes |
| `GST-050` | Resource Booking – Cabana | catalogue | 3 | 3 | yes |
| `GST-051` | Plan Your Adventure – Start | queue | 3 | 2 | yes |
| `GST-052` | Suggested Itineraries | catalogue | 3 | 2 | yes |
| `GST-053` | Build Your Own Itinerary | orders | 3 | 4 | yes |
| `GST-054` | AI Optimized Itinerary | queue | 3 | 3 | yes |
| `GST-055` | Dynamic QR Ticket | orders | 1 | 1 | yes |
| `GST-056` | Bundle Package | catalogue | 2 | 3 | yes |
| `GST-057` | Accessibility Information | white-label | 2 | 1 | yes |
| `GST-058` | Resource Availability (Cabana) | catalogue | 3 | 2 | yes |
| `GST-059` | Plan My Day – In Progress | queue | 3 | 2 | yes |
| `GST-061` | Menu Item Detail | fnb | 2 | 1 | yes |
| `GST-062` | Shop & Drop Collection | retail | 3 | 1 | yes |
| `GST-063` | Search | catalogue | 1 | 1 | **no** |
| `GST-065` | Newsletter & Preferences | marketing-crm | 3 | 2 | **no** |

