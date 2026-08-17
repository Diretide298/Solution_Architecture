# ADR-0019 — A dynamic bundle has a fixed price and a variable allocation

**Status:** Decided · 17 August 2026
**Closes:** CF-18
**Requirements:** 3.5.10, 7.4.48

---

## The question

3.5.10 asks for bundles where *"guests can select attractions, experiences, F&B items, retail
products, or services from predefined categories while maintaining bundle pricing rules."*

**What happens to the price when the guest's selection changes?** A bundle offering any three
attractions contains attractions that are not worth the same, and the requirement says the
pricing rules are maintained without saying what that means.

## What the contract could not express

`BundleComponent` names a specific `variantId` with a quantity, plus `isOptional` and
`substituteVariantIds`. That describes **a fixed bundle with swaps**. It cannot say *"pick any
three from the attractions category"*, which is what a dynamic bundle is.

So the gap was two things wearing one name: a missing shape, and an undecided pricing rule.

## Decision

**A dynamic bundle has a fixed price. The guest's selection changes what the price is allocated
to, never the price itself.**

    Family Day Pass — AED 250
      choose 3 from: Aquarium, Zoo, Planetarium, Cinema, Splash Zone
      choose 1 from: Lunch Combo, Snack Combo

The guest picks; the total stays AED 250. **Allocation across the chosen components is
proportional to their list price at the moment of sale**, and it is the allocation that varies.

### Why not compute the price from the components

Computing the total from whatever the guest picked, with a percentage off, produces a bundle
whose price moves while the guest is configuring it. That is a worse purchase experience — the
guest is being quoted a different number every time they change their mind — and it is a
revenue line nobody can forecast, because the average selling price depends on which components
prove popular.

**A venue markets a price.** "Any three attractions for AED 250" is a proposition; "about
AED 250 depending on what you choose" is not.

### Why allocation still has to be right

The guest pays one amount and the platform owes revenue to several places. A guest choosing the
Aquarium and Planetarium has bought something different from one choosing the Cinema twice, and
**the venue's attraction-level revenue must reflect what was actually consumed** — for
inter-entity settlement, for attraction P&L, and for the deferred-revenue release when each
component is redeemed.

Proportional-to-list-price is the method, computed at sale and frozen on the order line.

### What happens when a component's list price changes

**Nothing, for orders already placed.** The allocation was computed and stored at sale.

**For orders placed afterwards**, the new list price is used. The bundle price is unchanged
because the bundle price is a marketing decision, not a derived number — **a venue putting up
the price of a cinema ticket has not repriced the family pass**, and if they want to they will
say so.

### Where a choice group cannot be satisfied

A guest choosing three attractions when one has sold out for their date gets the same treatment
as any other availability failure: the option is not offered. **The bundle does not silently
substitute**, because a substitution the guest did not choose is a complaint at the gate.

Where a whole choice group becomes unsatisfiable — every option sold out — the bundle is
unavailable for that date rather than sold with a component that cannot be delivered.

## Consequences

**`BundleComponent` gains a choice-group form.** A component is either a fixed variant, as
today, or a choice of *n* from a named set. Both may appear in one bundle: the Family Day Pass
above has a fixed parking component and two choice groups.

**Allocation runs at sale, not at configuration.** `evaluatePromotions` prices the bundle;
`createOrder` computes and freezes the allocation. That ordering matters, because a lease is
acquired against the chosen components and the allocation must match what was actually held.

**Availability is checked per option, not per bundle.** A choice group's options are filtered
by what is available for the chosen date before the guest sees them.

**Reporting keeps both.** The order line carries the bundle and the chosen component, so
"which options do people actually pick" is answerable — and it is the question that tells a
venue whether the bundle is priced correctly.

## Alternatives considered

**Computed price with a bundle discount percentage.** Rejected above: unforecastable and a
worse purchase experience. It also makes the highest-value combination the one every guest
picks, which is exactly the combination the venue least wants to sell at a discount.

**Fixed price with equal allocation.** Simpler, and wrong. Allocating AED 250 equally across a
premium attraction and a cheap one misstates both attractions' revenue, and the settlement
between entities is then wrong by the same amount.

**Tiered bundles — a cheap set and a premium set.** Not rejected; **this is a legitimate way to
express the same commercial intent using fixed bundles and no new shape.** A venue that wants
price to reflect value can publish two bundles instead of one dynamic one. The choice-group form
exists because 3.5.10 asks for it, not because tiers are wrong.
