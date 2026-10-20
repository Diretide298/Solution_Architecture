# Minutes of Meeting: Ticketing Configuration Wireframe Review, Delivery Plan and Main Website Discussion

> Converted from `TICVAI_MoM_2026-10-16_TicketingConfig_Wireframes_Plan.docx` (beside this file) on 20 October 2026
> for citation; the .docx is the record. Text as written; the participants section of the original names the
> two teams only. Named in the text: Muhamed Allam and Qossai Alqawasmi (client), Pallavi Sawant, Chinmay Parab,
> Chitrangi Mestry (who prepared the minutes).

**Date:** 16-October-2026 · **Project:** TICVAI  
**Meeting Type:** Ticketing Configuration (Back-End) Wireframe Review; Delivery Plan and Main Website Discussion · **Prepared by:** Chitrangi Mestry  

## Primary Objective

To review the first set of back-end (venue management) wireframes, covering ticketing product configuration, presented by Pallavi, and to record Allam's feedback so the screens can be corrected before development. The session also covered the delivery plan and pace for the remaining modules, and the work needed for the TICVAI main website and UAE Pass integration.

## Participants

- TICVAI Team
- Softlabs Team

## Agenda

- Product dashboard and quick actions
- Special products category
- New product creation options and AI-assisted creation
- Ticket type simplification and categories/tags
- Basics tab, venue scope and multi-venue configuration
- Content, language and channel-specific content
- Variants, pass and membership rules, holder and ownership
- Schedule, capacity, events and performances
- Delivery plan, pace of review and module coverage
- TICVAI main website and UAE Pass integration

## 4. Detailed Discussion

### 4.1 Product Dashboard and Quick Actions

- Pallavi explained these are wireframes with demo data, not the final system. The first screen is a dashboard showing active products, draft products, products pending approval and approved products; approved products are the ones that can be sold to customers.
- Quick actions take the user straight to a new product, to creating a product by copying an existing one, or to the import file inbox. A “needs attention” list shows everything that requires action, and products are also shown by family.
- Import (Allam): import only works with a template, not any file. Before the implementation phase, TICVAI will share the template with the customer to fill in. The system should check that required fields (prices, ticket types, etc.) are present, show a preview, and create the products only after the user confirms.

### 4.2 Special Products Category

- The prototype had a separate “special products” category (e.g., corporate and school groups, with details such as a minimum of 10 people).
- Change requested (Allam): remove the special products category. Groups, memberships, dated, time-slot and other types are all just product types. “All products” should have a filter by type (group, membership, etc.) so that one list covers everything. Pallavi agreed to merge it.

### 4.3 New Product Creation Options

- Pallavi showed five ways to create a product: from blank, from a template, copy from an existing product, import from file, and AI.
- Copy from existing: all configuration is copied and the user only changes the name, price or other details; the SKU is different for each product to avoid mix-ups.
- Change requested (Allam): keep the AI and import options last in the list.

### 4.4 AI-Assisted Product Creation

- Issue noted (Allam): when he tried it earlier, the AI moved to the next step without asking for information he had not provided. The AI should not skip a question that is required to create the product.
- Agreed (Pallavi): validations will be added so the user cannot proceed without the mandatory answers.
- Additional change (Allam): if the user does not have the information yet (e.g., capacity), the AI should offer “configure later”, and the user must accept that explicitly. On the review screen the user should then clearly see which questions were not answered, update them, and only then publish and send for approval.

### 4.5 Ticket Type Simplification

- Allam asked that the number of ticket types be reduced because too many options confuse the user. He walked through each type to agree what it means.
- Open dated and dated: open dated is a ticket valid for a period from the date of sale (one day, one month, six months) with no visit date chosen. Dated is a ticket where a visit date is chosen at sale.
- Special day and multi-day: merge into dated. A special day such as New Year's Eve is just a dated product where the date is fixed in the configuration. Multi-day is a validity period (one week, one month, etc.) set under dated.
- Camp and recurring: merge into time slot. The time slot configuration should let the user pick one slot, several slots or a weekly pattern, and enforce the pattern. Example: four weeks of ski lessons at two classes per week means eight classes selected, two in each week.
- Final list agreed: open dated, dated, time slot, pass and membership, voucher (a product bought now and redeemed later, like a gift voucher) and add-on. Pallavi confirmed she will merge the types accordingly.

### 4.6 Category and Tags

- Issue (Allam): the product form had a “category” field (admission, general admission, single day, etc.) that looked like a duplicate of ticket type and was unclear.
- Change requested (Allam): categories must be user defined, not hard coded. Create them as master data in a separate place and link them to a product from a drop-down. Pallavi will do this.
- Allam used the Deep Dive website as an example: scuba diving, free diving and snorkelling are categories; under scuba diving the products (standard, premium, platinum, birthday packages) are products, not categories; and certified or non-certified is another classification. He said the system should let the user configure all of these.
- Tags (Qossai): a tag is different from a category. Tags let marketing group tickets, e.g., summer and winter tickets or outdoor and indoor tickets, so a promotion can be applied to a whole tag (e.g., 50% on all summer tickets). Two products in different categories can share a tag. Allam noted tags already exist in the POS wireframe.

### 4.7 Basics Tab: Product ID, SKU and Barcode

- Pallavi explained the product form has 12 steps; step one holds product identity (name, product ID, SKU, barcode reference, external IDs, reporting code) and classification (product family, ticket type, category, venue scope, department).
- Product ID: the “internal ID” is system generated and unique. Allam asked to rename it “Product ID” and to follow a proper naming convention rather than a random code (the sample P-1010 was only demo data). Pallavi asked Allam to suggest the logic.
- Barcode: a barcode applies to merchandise and F&B items, not tickets. The ticket media identifier (QR or other) is generated at the time of sale. Where a supplier does not provide a barcode, the system should generate one so it can be printed on labels and scanned. Pallavi agreed to note this.

### 4.8 Venue Scope and Multi-Venue Configuration

- The wireframe was designed for a single venue. Allam asked what “venue scope” is meant to achieve, and noted there is nowhere on screen to see which venue the user is working in.
- Qossai's question: for a group with several venues (e.g., Sea World and Ferrari World), can a family membership be created once and be available in both dashboards, or is it created twice? He understood the venues had separate configuration.
- Allam's answer: it is a single database and the product is created once. What differs is who can sell it. He showed the existing system's sale permissions: global (all venues in the multi-tenant setup), a particular site, an operating area (sales channel such as POS, B2C, kiosk), a workstation, a role (admin, cashier, supervisor) or a specific user, each with allow and deny options.
- Change requested (Allam): remove venue scope from the basics step and replace it with a “who can sell” permission option.
- Admin access (Allam): in the existing system, an admin with product-creation rights can create products on any site, which is a problem. The new system must support both models: one admin managing configuration for all venues, or a separate admin per venue who can only see and create products for that venue. This sits under rights and access.

### 4.9 Content and Language

- Change requested (Allam): name and description were hard coded as English and Arabic. The language must not be fixed; any language can be added (with a language code) and then appears for translation. Pallavi will remove the fixed name and description fields.
- Qossai's point: a venue may need three languages (e.g., English, Spanish and Italian) or five or six for guests from China or Russia. The product text must be translatable for B2C, kiosk and POS, and the languages chosen by the admin.
- Allam suggested Pallavi check how translation is handled in the existing ticketing system manuals when designing screens. Pallavi said she could not open the shared documents without credentials; Qossai said the manuals were shared as PDFs and need no login. Pallavi will check again.

### 4.10 Channel-Specific Content and Preview

- The content step covers images, channel-specific content for POS, website and kiosk, and a preview of how the product looks on each channel.
- Allam confirmed the POS button label can differ from the name printed on the receipt, and that the B2B partner description is what resellers see in the B2B portal and API. Pallavi said the preview does not yet show these correctly and will be improved.

### 4.11 Show Only Relevant Tabs for the Selected Ticket Type

- Key change (Allam): after choosing a membership product, he could still open the open-dated and time-slot tabs. Once a ticket type is selected, only the tabs for that type should show; the others can be disabled so they cannot be clicked. Otherwise the type selection serves no purpose and the screens confuse users (“I have worked in 20 years of ticketing and I got lost”).
- Pallavi agreed and will make the form change with the type drop-down. The groups and membership tab will be merged into pass and membership.

### 4.12 Variants and Quantities

- Issue (Allam): the sample family membership is described as two adults and two children, but nothing in the configuration says so. A description is not enough; the product needs variants (adult, child) with quantities (2 and 2). Pallavi also noticed the add-variant action was not available on that saved product.
- Why it matters (Allam): the system must know how many QR codes or barcodes to issue (four, or one pass valid for all four) and how the family enters through access control, including when only one adult or one child enters on a given day.
- Guidance (Allam): design product configuration from the sales view, the customer view, the operations view and access control together, not only from the selling point.

### 4.13 Pass and Membership Rules

- Pass behavior (Allam): monthly, annual, season, custom duration and renewable subscription were confusing. Season did not say which season or what its validity is. Renewable subscription should not be a separate behavior; it should be a flag under monthly or annual that, when enabled, lets the customer opt in to renewal (terms and conditions accepted). Pallavi will remove the separate auto-renewal option and show the flag after the behavior is chosen.
- Validity start options to configure (Allam): from the date of sale; a predefined date range (e.g., 1 to 31 December); or from the first scan, where the membership must be used within a window (e.g., three months) and is valid for one month from the scan.
- Holder and ownership: the screen listed reservation owner and ticket holder fields directly, with first and last name hard coded. Allam asked for a configurable field set (called a data mask in the existing system): create it in the configuration, design it with custom fields (text, drop-down, radio, check box), and link it to the product so the fields appear automatically at sale. Some businesses want a full name, not first and last name.
- Reservation owner vs ticket owner (Allam): the reservation owner is the buyer of the transaction. A ticket owner is needed only for tickets such as memberships and seasonal passes. If a parent buys a membership for a daughter, the parent is the reservation owner, the daughter is the ticket owner, and two profiles are created. A general admission ticket needs no ticket holder.

### 4.14 Schedule, Capacity, Events and Performances

- Pallavi said the schedule and capacity step checks that the tickets configured do not exceed the venue capacity (for example 5,000), with channel allocation controlling how many tickets each channel can sell.
- Gap noted (Allam): there is no configuration to create events and performances. Pallavi confirmed they are not covered in this wireframe set and will link to this step when added.
- Qossai's view: this step is more relevant when creating performances, with capacity and time slots, than on the product screen.
- Approach (Allam): on the product, only flag that it requires a schedule or performance selection. Create events and performances on separate screens, and define capacity at event level so performances inherit it. When a product is sold, the system then shows the performances linked to its event.
- Allam demonstrated this in the existing system with a skydive tandem product: the product points to an event, the product setting “performance selection before encoding” forces a time slot to be chosen, and time slots are generated from a start and end time, an interval and duration, and an entry window (e.g., 15 minutes before and after the start).
- The add-ons and bundles tab and the later steps (who can buy, sales channels, after-sales rules, renewal) were looked at briefly with no change requested on the call.

### 4.15 Delivery Plan and Pace of Review

- Raised (Qossai): the back-end configuration and UI/UX for each module has not yet been received, so he asked about the plan and timeline.
- Response (Chinmay): development has started on the web and guest app. As each venue management module is completed, it will be integrated and given to developers as a package. The AI modules have not been worked on yet and can be done next week.
- Qossai's request: each module should follow the same pattern as today: Softlabs shares the screens, TICVAI checks them against the matrix and boards, and a session like this one gives feedback so corrections are made directly, instead of waiting until the end. He felt progress slowed over the past couple of weeks and said October and November are the most important months for getting the configuration right; missing functionality found later would push the timeline past December.
- Agreed (Chinmay): he accepted the slowdown, will create the same layout and documents for the remaining modules, and will hold review calls as regularly as possible. He proposed covering about 80 to 90 percent of each module quickly and resolving the rest on calls. Qossai asked for a plan for next week and the week after; Chinmay will send it over the weekend.

### 4.16 TICVAI Main Website and UAE Pass Integration

- Raised (Qossai): the TICVAI main website has not been planned and needs to start. Integrations with UAE Pass (written “UE Pass” in the recording), DCT and DTCM all ask for the main website, and DCT and DTCM also want to see the solution before integration starts.
- UAE Pass requirements: Qossai emailed Allam the requirements: an authentication mock-up for the mobile app and for the website, a user journey for each, and an authentication questionnaire to answer. Qossai has a sample reply from another project (built with AI) and will share it. Allam will forward the email to Chinmay.
- Qossai also noted the employee mobile app has not been discussed in the plan yet and should be added. Chinmay agreed to go through the email and discuss alongside the module configuration or earlier.

## 5. Key Decisions & Agreements

- The special products category is removed; all product types sit under “all products” with a filter by type.
- Ticket types are simplified to six: open dated, dated (including special day and multi-day), time slot (including camp and recurring), pass and membership, voucher, and add-on.
- Categories and tags are user-defined master data linked to products from a drop-down, not hard coded.
- A product is created once, and who can sell it is set through sale permissions (site, sales channel, workstation, role, user, allow or deny). Venue scope is removed from product creation, and admin rights must be limited per venue when needed.
- Product ID is system generated and follows a naming convention; barcodes apply to merchandise and F&B, and ticket media identifiers are generated at sale.
- Languages are configurable and not hard coded to Arabic.
- Only the tabs relevant to the selected ticket type are shown or enabled.
- Variants carry quantities (e.g., 2 adults and 2 children) so the system knows how many credentials to issue and how access control counts entries.
- Renewable subscription is a flag under monthly or annual; membership validity supports date of sale, predefined dates and first scan.
- Reservation owner and ticket owner fields come from a configurable field set linked to the product.
- Events and performances get their own screens, with capacity set at event level and inherited by performances.
- AI product creation must not skip mandatory questions; unanswered items can be marked “configure later” and are shown on the review screen before publishing.
- Remaining modules will be reviewed in sessions like this one, module by module.

## 6. Open Items / Questions for Follow-Up

- Revised ticketing wireframes and a follow-up review call.
- Product ID naming convention to be defined.
- Wireframes for events and performances are not yet created.
- Whether the manual PDFs open without credentials for Pallavi.
- Plan for next week and the week after, due from Chinmay over the weekend.
- TICVAI main website, DCT and DTCM integrations, UAE Pass submission and the employee mobile app are not yet in the plan.

## 7. Action Items

| Action Item | Owner | Due | Status |
|---|---|---|---|
| Revise the ticketing configuration wireframes with all of Allam's feedback (sections 4.2 to 4.14) and share the next version | Pallavi Sawant | Next version | Open |
| Propose a product ID naming convention (auto-generated, not a random code) and agree it with Allam | Pallavi Sawant / Allam | Next version | Open |
| Add separate screens to create events and performances (including capacity at event level) and link them to the product | Pallavi Sawant | Next version | Open |
| Hold a follow-up call to go through the revised ticketing screens | Allam / Pallavi Sawant / Chinmay Parab | After revised wireframes | Open |
| Check whether the shared manual PDFs open without credentials and report back if they do not | Pallavi Sawant | Soon | Open |
| Create similar wireframes and documents for the remaining modules and schedule regular review sessions | Chinmay Parab | Ongoing | In Progress |
| Share the plan for next week and the week after | Chinmay Parab | Over the weekend | Open |
| Work on the AI modules | Chinmay Parab | Next week | Open |
| Share the UAE Pass requirements email with Chinmay | Allam | Today | Open |
| Review the UAE Pass requirements and prepare the authentication mock-ups, user journeys and questionnaire reply (Qossai's sample to be shared) | Chinmay Parab | TBC | Open |
| Add the TICVAI main website and the employee mobile app to the delivery plan | Chinmay Parab / Qossai | TBC | Open |

## 8. Next Steps

- Pallavi to share the corrected ticketing wireframes, followed by another review call.
- Chinmay to send the plan for next week and the week after over the weekend, and to continue with the venue management modules and the AI modules next week.
- Allam to forward the UAE Pass email to Chinmay; Qossai to share his sample reply.
--- End of Minutes ---
