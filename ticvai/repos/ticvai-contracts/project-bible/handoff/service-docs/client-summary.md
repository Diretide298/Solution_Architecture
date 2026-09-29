# TICVAI first release: what is being built

This summary describes the four parts of the first release and the back-end services behind them. It is generated from the same specification the development team builds from.

## The four parts

### Point of Sale

40 screens: 27 in wave 1, 13 in wave 2.

Areas covered: Kitchen, Payment, Reports, Sell, Shift.

### Guest App - Web

50 screens: 22 in wave 1, 21 in wave 2, 7 in wave 3.

Areas covered: Account & Self-Service, Booking & Selection, Cart & Checkout, Discovery & Browse, Engagement & Support, High-Demand Access, In-venue Services, Membership, Loyalty & Value, Promotions, Retail, Support, System States, Ticketing, Transport.

### Guest App - Mobile

77 screens: 25 in wave 1, 35 in wave 2, 17 in wave 3.

Areas covered: Account & Self-Service, Booking & Selection, Cart & Checkout, Discovery, Discovery & Browse, Engagement & Support, High-Demand Access, In-Venue Experience, In-venue Services, Marketing, Membership, Loyalty & Value, Promotions, Retail, Support, System States, Ticketing, Transport.

### White Labelling

26 screens: 3 in wave 1, 23 in wave 2.

Areas covered: Branding & Localisation, White Label.

## The services behind them

The four parts share 16 back-end services. Each looks after one area of the business and owns its own area of the data. They run separately, so most can be unavailable without stopping the others; the table says what happens if each one is.

| Service | What it looks after | If it is unavailable |
|---|---|---|
| Organisation and settings | Your organisation, regions, venues, outlets and tills, and the settings each one uses. | Nothing can find its venue or settings, so everything stops. |
| Sign-in and people | Staff and guest accounts, sign-in, roles and permissions, and personal-data requests. | Nobody can sign in, so everything stops. |
| Sales and payments | Baskets, orders, payments, refunds, and opening and closing cashier shifts. | No new sales can be taken. This service has the highest availability target. |
| Products and pricing | What is sold, at what price and when: products, events and sessions, price lists, promotions, bundles and seating. | Tills keep selling from their last published catalogue; changes wait. |
| Entry and admission | Tickets and passes at the gate, admission rules and entry validation. | Gates fall back to their local copy of what is valid. |
| Wallets and credit | Guest wallets, stored credit, gift cards and membership credit. | Wallet balances cannot be spent until it returns. |
| Finance | The financial record of every sale, refund and payment, and currency rates. | Finance postings wait until it returns; trading is not affected. |
| Venue operations | Queues and wait times, maintenance, bookable resources, the venue map and media. | Venue operations degrade; selling and entry continue. |
| Food and beverage | Menus, table service, kitchen screens and food orders. | Kitchens fall back to printed tickets. |
| Stock | Stock levels, counting and purchasing. | Receiving and counting pause; selling continues. |
| Retail | Merchandise, shop sales, returns and shop-and-drop. | The shop stops; gates and restaurants do not. |
| Guests and marketing | Guest profiles, consent, loyalty, campaigns, forms and support. | Campaigns and guest look-up pause; trading continues. |
| AI assistance | Suggestions and the guest concierge. | Suggestions stop; nothing that takes money depends on it. |
| Subscription and platform | Your subscription, licensed modules and platform administration. | Provisioning and administration pause; trading continues. |
| Reporting | Dashboards, reports and alerts. | Dashboards pause; nothing operational depends on them. |
| Branding | Your brand, theme, pages, navigation and content in the guest web and mobile app. | Guests keep seeing the last published version. |

## How the work grows

Each service is built first for what these four parts need, then published as a fixed version. Later releases add to it without changing what has already been delivered, so the four parts keep working while the platform grows.
