#!/usr/bin/env python3
"""Write handoff/board-panel-map.json — every board read panel against the operation that serves it.

**86 of the 210 operations the client F&B pack names are reads**, and building them as written
would give the contract an endpoint per panel. **A board panel is not an endpoint**: `getKitchenLoad`,
`getKitchenSla` and `listKitchenExceptions` are three panels on one screen, and one
`listKitchenTickets` with a filter and an aggregate answers all three.

**This file is the deliverable instead of that code.** A frontend team building `FNB-3A` has four
operation names on the board and no way to know which real endpoint serves each — this says.

Three shapes, and the distinction is the point:

  **`filter`** — an existing list with parameters. `listActiveOrders` is `listFnbOrders` with a
  status filter. Cheapest, and most of the 86.

  **`report`** — `runReport` or `getDashboard` with a definition. Every Board 6 analytics panel.
  **A report definition is data, not code**, which is why twenty analytics panels need no
  operations at all.

  **`derive`** — computed at read time from something already stored. `getRecipeCost` is a recipe
  joined to current ingredient prices; nothing stores it because **a stored cost is a cost that
  goes stale the moment a supplier changes.**

Where a panel needs something genuinely new the entry says `build` — and after this pass there are
five, all in Board 2's three newest frames.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# panel -> (shape, operation, note)
MAP = {
# ── The AI cluster. **One operation, seventeen panels.** The boards drew each as its own
    # endpoint; `requestSuggestion(kind=…)` answers all of them, and the reason is the swap:
    # six endpoints is six places to change when a model changes.
    "suggestPrice": ("suggestion", "requestSuggestion", "`kind=price`."),
    "suggestReplenishment": ("suggestion", "requestSuggestion", "`kind=replenishment`."),
    "forecastDemand": ("suggestion", "requestSuggestion", "`kind=demandForecast`."),
    "forecastKitchenDemand": ("suggestion", "requestSuggestion",
        "`kind=demandForecast` scoped to a kitchen. **The scope is a parameter, not an operation.**"),
    "publishDemandPlan": ("suggestion", "requestSuggestion",
        "`kind=demandForecast`, then `recordSuggestionOutcome` when the venue commits to it — "
        "**publishing a plan is accepting a suggestion**, and that is the label a model trains on."),
    "simulateScenario": ("suggestion", "requestSuggestion", "`kind=scenario` with the change in `context`."),
    "simulateSlaPolicy": ("suggestion", "requestSuggestion", "`kind=slaTarget`."),
    "classifyMenuItems": ("suggestion", "requestSuggestion", "`kind=menuEngineering`."),
    "listRecommendations": ("suggestion", "requestSuggestion", "Open suggestions for this scope."),
    "listKitchenRecommendations": ("suggestion", "requestSuggestion", "The same, scoped to a kitchen."),
    "listTableRecommendations": ("suggestion", "requestSuggestion", "The same, scoped to the floor."),
    "listExecutiveInsights": ("suggestion", "requestSuggestion", "`kind=anomaly` across the venue."),
    "getScenarioAssumptions": ("suggestion", "requestSuggestion",
        "**`Suggestion.inputs`.** Recorded so the answer can be reproduced — which is exactly what "
        "an assumptions panel shows."),
    "getForecastDrivers": ("suggestion", "requestSuggestion",
        "**`Suggestion.explanation`.** Plain words, always present, whatever the basis."),
    "getForecastAccuracy": ("report", "runReport",
        "Suggested against actual over `ai.suggestion_outcome`. **The table built so this panel "
        "could exist** — and so a model could be trained later."),
    "getAnswerSources": ("filter", "sendAiMessage",
        "`AiMessage.sources`. Already returned with every AI answer."),
    "queueAction": ("filter", "decideProposedAction",
        "**A suggestion becomes a proposed action and the queue is already there.** One queue, not "
        "one per domain."),

    # ── Board 3 — kitchen. One rail, several views of it.
    "getKitchenLoad": ("filter", "listKitchenTickets",
        "Count and age of open tickets by station. **The rail already holds it** — a load figure is "
        "the rail counted, not a second source."),
    "listKitchenExceptions": ("filter", "listKitchenTickets",
        "Tickets past their SLA. `?breachingSla=true` over the same rail — **an exception is a "
        "ticket, not a different kind of thing.**"),
    "getKitchenSla": ("filter", "getVenueSettings",
        "The target, not a measurement. Set by `setKitchenSla` and read from venue settings."),
    "listActiveOrders": ("filter", "listFnbOrders", "`?status=accepted,inPreparation`."),
    "listExpoOrders": ("filter", "listKitchenTickets",
        "`?status=readyForAssembly`. **The expeditor sees the same rail filtered**, which is why no "
        "expeditor role was modelled."),
    "listCollectionQueue": ("filter", "listKitchenTickets",
        "`?status=ready&serviceMode=collection`. Ordered by ready-at, oldest first — **food under a "
        "lamp is a clock nobody is watching.**"),
    "getOrderCourses": ("filter", "getFnbOrder",
        "Courses are on the ticket. `KitchenTicket.coursing` plus its lines grouped by course."),
    "listOrderLog": ("filter", "listFnbOrders", "`?includeHistory=true` with the audit trail."),
    "getStationPerformance": ("report", "runReport",
        "Definition over `fnb.kitchen_ticket_line` by station. **Board 6 and Board 3 draw the same "
        "numbers at different depths** — one definition, two dashboards."),
    "getKitchenPerformance": ("report", "runReport", "As above, rolled to the outlet."),
    "getStationBottlenecks": ("report", "runReport",
        "The same definition ranked by wait rather than by throughput. **A bottleneck is a sort "
        "order, not a metric.**"),
    "getOnTimeByChannel": ("report", "runReport", "Ticket age against SLA, grouped by service mode."),

    # ── Board 4 — floor. Tables and their state.
    "listTables": ("filter", "getTableMap",
        "**The map is the list.** A table map returns every table with its state; a separate list "
        "endpoint is the same rows without the geometry."),
    "getFloorPlan": ("filter", "getTableMap", "Same call. The plan is the map with its layout."),
    "listSeatedTables": ("filter", "getTableMap", "`?state=occupied`."),
    "getServiceOverview": ("filter", "getTableMap",
        "Covers, turns and stage counts — **all derivable from the map plus open visits**, and a "
        "separate overview endpoint is a second thing to keep in step."),
    "getTableTimeline": ("filter", "getTableVisit",
        "`?includeHistory=true`. Seated, ordered, courses fired, paid — **the stage transitions "
        "`setServiceStage` records.**"),
    "getTableCheck": ("filter", "getBill", "The bill for the visit on that table."),
    "listWaitlist": ("filter", "joinRestaurantWaitlist",
        "The list is a GET on the same resource. `?status=waiting,notified`."),
    "getReservationTimeline": ("filter", "listTableReservations",
        "`?date=&groupBy=slot`. **A timeline is a list with a time axis**, and the conflict view "
        "sits on `resolveBookingConflict` beside it."),
    "getGuest": ("filter", "getGuestProfile", "Guest-callable and already there."),
    "listGuestVisits": ("filter", "listOrders", "`?subjectId=`. A visit is an order at a venue."),
    "getTablePerformance": ("report", "runReport", "Turn time and covers by table."),
    "getReservationMetrics": ("report", "runReport", "Booked, seated, no-show, walk-in conversion."),
    "getRevpash": ("report", "runReport",
        "Revenue per available seat hour. **A definition over covers, seats and revenue** — three "
        "things already stored, and the metric that tells a restaurant more than any other."),

    # ── Board 5 — stock. Movements and counts.
    "getStockOverview": ("filter", "getStockPositions", "Positions rolled to the outlet."),
    "listOutletStock": ("filter", "getStockPositions", "`?locationId=`."),
    "getIngredientCoverage": ("derive", "getStockPositions",
        "On-hand divided by forecast usage. **Days of cover is arithmetic over two things already "
        "held**, and storing it makes it wrong within the hour."),
    "listWastage": ("filter", "listStockMovements", "`?reason=waste`. Waste is a movement kind."),
    "getWastageByReason": ("report", "runReport", "The same movements grouped."),
    "getWasteByOrigin": ("report", "runReport", "Grouped by station and by stage instead."),
    "listStockAlerts": ("filter", "listAlerts", "`?domain=inventory`. One alert mechanism, filtered."),
    "getCountHistory": ("filter", "listStockCounts", "`?itemId=&includeLines=true`."),
    "getVarianceSummary": ("filter", "getCountVariance", "Already returns it. Rolled to the count."),
    "getVarianceReasons": ("filter", "getCountVariance", "`?groupBy=reason`."),
    "getVarianceTrend": ("report", "runReport", "Variance across counts over time."),
    "getTheoreticalUsage": ("derive", "listRecipes",
        "Recipes multiplied by items sold. **The theoretical side of a variance** — computed, never "
        "stored, because a recipe change would silently rewrite last month."),
    "getActualUsage": ("filter", "listStockMovements", "`?reason=consumption`."),
    "listTransfers": ("filter", "listStockTransfers", "Already exists."),
    "listProductionBatches": ("filter", "listProductionRuns", "Already exists."),
    "createBatch": ("filter", "planProductionRun", "A batch is a planned run."),
    "getBatchYield": ("derive", "getProductionRun",
        "Planned against actual output. **`completeProductionRun` records what was made**; yield is "
        "the two compared."),
    "getBatchYieldSummary": ("report", "runReport", "Yield across runs, by product and by period."),

    # ── Board 2 — menu and product.
    "listCombos": ("filter", "listProducts", "`?kind=combo`. Combos are products with slots."),
    "getComboCost": ("derive", "listRecipes",
        "Slot options costed through their recipes. **The cheapest and dearest combination both "
        "matter** — a meal deal priced against its cheapest option loses money on every other."),
    "getRecipe": ("filter", "listRecipes", "`?itemId=`. Singular of an existing list."),
    "getRecipeCost": ("derive", "listRecipes",
        "Recipe joined to current ingredient prices. **Never stored: a stored cost goes stale the "
        "moment a supplier changes**, and a stale food cost is worse than none."),
    "listCostHistory": ("report", "runReport", "Recipe cost over time as prices moved."),
    "listPriceHistory": ("filter", "listPrices", "`?includeHistory=true`. Price rows are versioned."),
    "getMenuDiff": ("derive", "getMenu",
        "Two menu versions compared. **`publishMenu` versions them and `rollbackMenu` depends on "
        "it** — the diff is the two read together."),
    "listAvailability": ("filter", "setItemAvailability",
        "GET on the same resource. `?outletId=`, with the 86 history beside it."),
    "getMenuPerformance": ("report", "runReport", "Units, margin and attach rate by item."),
    "getModifierUplift": ("report", "runReport",
        "Revenue added by modifiers. **The number that justifies maintaining them** — a venue with "
        "forty modifier groups and no uplift figure is maintaining forty groups on faith."),
    "getSectionRevenue": ("report", "runReport", "Revenue by menu section."),
    "getProductPerformance": ("report", "runReport", "The cross-domain version, on P16."),
    "getCategoryMargin": ("report", "runReport", "Margin by category."),

    # ── Board 6 — analytics. Every one a report definition.
    "getExecutiveSummary": ("report", "getDashboard", "The seeded executive dashboard."),
    "getRevenueVsBudget": ("report", "runReport", "Actual against plan. **Budget is an input the venue supplies.**"),
    "getMarginBridge": ("report", "runReport",
        "Margin movement decomposed — price, mix, cost, waste. **A bridge is a definition, not an "
        "endpoint**, and every domain wants one."),
    "getFoodCostBridge": ("report", "runReport", "The same bridge scoped to food cost."),
    "getOutletFoodCost": ("report", "runReport", "Food cost percentage by outlet."),
    "getIngredientInflation": ("report", "runReport", "Purchase price movement by ingredient."),
    "getProfitability": ("report", "runReport", "Contribution by outlet, by daypart, by channel."),
    "getChannelRevenue": ("report", "runReport", "Revenue by sales channel."),
    "getChannelContribution": ("report", "runReport", "The same, after channel cost."),
    "getDaypartRevenue": ("report", "runReport", "Revenue by daypart."),
    "getPaymentMix": ("report", "runReport", "Tender split."),
    "getGuestMix": ("report", "runReport", "New against returning, by segment."),
    "getServiceMetrics": ("report", "runReport", "Wait, turn, and time to first course."),
    "getOutletPerformance": ("report", "runReport", "The outlet scorecard."),
    "getCapacityUtilisation": ("report", "runReport", "Seats and kitchen capacity against demand."),
    "getLostSales": ("derive", "list86Events",
        "**`refusedOrderCount` on the 86 event is the figure.** Built 24 August precisely so this "
        "panel had a source — *off for ninety minutes* is a note; *and eleven guests asked* is a "
        "purchasing decision."),
    "listComplaintThemes": ("report", "runReport", "Cases grouped by category, over `marketing.case`."),
    "listActionQueue": ("filter", "listProposedActions",
        "**Already the AI action queue.** `decideProposedAction` clears it — one queue, not one per "
        "domain."),

    # ── Board 2's three newest frames. Four genuinely new, one derived.
    "getProductAllergens": ("filter", "getMenu",
        "Allergens are on the item. `?includeAllergens=true` — **contains and mayContain are "
        "different claims** and both are already modelled."),
    "verifyAllergens": ("build", None,
        "**Genuinely new, and the one that matters in this frame.** A substituted ingredient changes "
        "the allergen claim, and BL-127 built allergens without linking substitution. **A dish "
        "declared nut-free after a substitution nobody checked is the failure this prevents.**"),
    "setSubstitutionRules": ("build", None,
        "**Genuinely new.** What may replace what, and under what conditions — and it is the input "
        "`verifyAllergens` checks against."),
    "recalculateNutrition": ("derive", "setRecipe",
        "Nutrition summed from ingredients. **Recomputed on recipe change, not stored** — a stored "
        "figure survives a recipe edit and becomes a false label."),
    "buildProductionPlan": ("build", None,
        "**Genuinely new.** Forecast demand against recipes to produce a prep list. Sits on "
        "`requestSuggestion(kind=prepPlan)` for the forecast and needs a plan artefact to hold it."),
    "getPrepRequirements": ("filter", "getProductionRun", "The plan's lines."),
    "releaseProductionPlan": ("build", None,
        "**Genuinely new.** A plan becomes production runs. **Separate from building it because a "
        "plan is edited before it is released**, and a plan that creates runs as it is drafted "
        "creates runs nobody asked for."),
    "printPrepSheets": ("filter", "getProductionRun",
        "A render of the plan. **Not an endpoint** — the same rule that made `printOrderLabel` the "
        "exception, and it is the exception because of allergens."),
    "consolidateOutletDemand": ("derive", "listRequisitions",
        "Outlet requisitions summed for the commissary. **The consolidation is the read**, and "
        "storing it would fix a number that moves every time an outlet edits a line."),
    "scheduleCommissaryRun": ("filter", "planProductionRun",
        "A commissary run is a production run at a central kitchen. `?locationKind=commissary`."),
    "allocateToOutlets": ("filter", "createStockTransfer",
        "Allocation is a transfer per outlet. **One mechanism** — a commissary allocating and a "
        "store transferring are the same movement."),
    "getMakeVsBuyCost": ("derive", "listRecipes",
        "Recipe cost against supplier price for the same item. **The decision a commissary exists "
        "to make**, and both sides are already held."),
}


def main() -> int:
    boards = json.loads((ROOT / "handoff" / "board-panel-map.json").read_text(encoding="utf-8")) \
        if (ROOT / "handoff" / "board-panel-map.json").exists() else {}
    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    frames = json.loads(Path("/tmp/reads.json").read_text(encoding="utf-8"))

    out = {
        "note": (
            "Every read panel the client F&B boards name, against the operation that serves it. "
            "**A board panel is not an endpoint** — `getKitchenLoad`, `getKitchenSla` and "
            "`listKitchenExceptions` are three panels on one screen and one `listKitchenTickets` "
            "answers all three. Building them as written would give the contract an endpoint per "
            "panel, and a contract with an endpoint per panel changes every time a panel moves."),
        "shapes": {
            "filter": "An existing operation with parameters. Cheapest, and most of these.",
            "report": ("`runReport` or `getDashboard` with a definition. **A report definition is "
                       "data, not code** — which is why twenty analytics panels need no operations."),
            "derive": ("Computed at read time from something already stored. **A stored derivation "
                       "is one that goes stale**, which is the same rule that made "
                       "`inventory.stock_level` derived."),
                "suggestion": ("`requestSuggestion` with a `kind`. **Seventeen panels, one operation** "
                           "— the boards drew each as its own endpoint, and six endpoints is six "
                           "places to change when a model changes."),
            "build": "Genuinely new. Four, all in Board 2's three newest frames.",
        },
        "generated": "24 August 2026",
        "panels": {},
    }

    counts = {"filter": 0, "report": 0, "derive": 0, "suggestion": 0, "build": 0, "unmapped": 0}
    for panel, board_frames in sorted(frames.items()):
        entry = MAP.get(panel)
        if not entry:
            counts["unmapped"] += 1
            out["panels"][panel] = {"shape": "unmapped", "frames": board_frames}
            continue
        shape, op, note = entry
        counts[shape] += 1
        rec = {"shape": shape, "frames": board_frames, "note": note}
        if op:
            rec["servedBy"] = op
            rec["exists"] = op in lin
        out["panels"][panel] = rec

    out["summary"] = counts
    (ROOT / "handoff" / "board-panel-map.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8")

    print(f"  {sum(counts.values())} panels mapped")
    for k, v in counts.items():
        print(f"    {v:>3}  {k}")
    bad = [p for p, r in out["panels"].items()
           if r.get("servedBy") and not r.get("exists")]
    if bad:
        print(f"  ** {len(bad)} name an operation that does not exist: {bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
