# Loyalty and gamification screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

F("BO-826", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="The badge library with the selected badge edited beside it (defined 4 October "
                "2026 from MarketingBadge, CHG-FXS-001).",
  regions=[
      ("contentBody", [
          c("dataTable", "Badges", "MarketingBadge", "listBadges",
            cols("MarketingBadge", "code", "name", "type", "isActive")),
          c("primaryButton", "New badge", notes="Opens an empty form in the side panel."),
      ]),
      ("contextPanel", [
          c("textField", "Code", "MarketingBadge.code", "setBadge", notes="Unique; read-only once saved."),
          c("textField", "Name", "MarketingBadge.name", "setBadge"),
          c("textField", "Description", "MarketingBadge.description", "setBadge",
            notes="Also the accessible alt text of the icon."),
          c("textField", "Type", "MarketingBadge.type", "setBadge",
            notes="Free text in the contract (e.g. achievement, collection, milestone)."),
          c("textField", "Icon link", "MarketingBadge.iconUrl", "setBadge",
            notes="The link of an approved image from the media library (CMS-010)."),
          c("toggle", "Active", "MarketingBadge.isActive", "setBadge"),
          c("primaryButton", "Save badge", op="setBadge",
            notes="Upsert on code; createdAt is sent unchanged for an existing badge and as now for "
                  "a new one."),
          c("secondaryButton", "Award to this guest", op="awardBadge",
            notes="Shown only when the screen was opened from a guest (customerId); sends badgeId, "
                  "status awarded and awardedAt now, sourceType manual."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No badges yet. Carries New badge."),
  note="Defined 4 October 2026 from MarketingBadge and MarketingCustomerBadge: the badge library "
       "(listBadges), a badge's form (setBadge) and a hand award to the guest the screen was opened "
       "for (awardBadge). Rarity, tiers and validity are not badge properties in the contract and "
       "left the screen")

F("BO-827", DEF, pattern="configEditor", template="split", drop_gaps=("person", "~nothing on this screen can be drawn"),
  patternReason="One programme's earning rules and bonus campaigns edited as one set (defined 4 "
                "October 2026 from LoyaltyProgramme.earnRules and LoyaltyRuleSet, CHG-FXS-001).",
  set=dict(purpose="Turn qualifying guest actions into loyalty points for one programme: the earning "
                   "rules (trigger, points, product kinds, multiplier), when points expire, and the "
                   "bonus-points campaigns that run over a window."),
  apis_add=[A("listLoyaltyProgrammes", "onLoad",
              "The programme being edited, with its earning rules (earnRules) and expiry"),
            A("updateLoyaltyProgramme", "onAction",
              "Save the programme's earning rules and points expiry: " + AGREED,
              contract="marketing-crm")],
  regions=[
      ("contentBody", [
          c("dataTable", "Earning rules", "LoyaltyProgramme.earnRules", "listLoyaltyProgrammes",
            ["LoyaltyProgramme.earnRules.trigger", "LoyaltyProgramme.earnRules.points",
             "LoyaltyProgramme.earnRules.productKinds", "LoyaltyProgramme.earnRules.multiplier"],
            notes="The programme the screen was opened for (programmeId), from listLoyaltyProgrammes. "
                  "Rows are edited in place."),
          c("selectField", "Trigger", "LoyaltyProgramme.earnRules.trigger", "updateLoyaltyProgramme"),
          c("numberField", "Points", "LoyaltyProgramme.earnRules.points", "updateLoyaltyProgramme"),
          c("multiSelect", "Product kinds", "LoyaltyProgramme.earnRules.productKinds",
            "updateLoyaltyProgramme", notes="Empty means every kind."),
          c("numberField", "Multiplier", "LoyaltyProgramme.earnRules.multiplier", "updateLoyaltyProgramme"),
          c("numberField", "Points expire after (months)", "LoyaltyProgramme.pointsExpireAfterMonths",
            "updateLoyaltyProgramme", notes="Empty means points never expire."),
          c("primaryButton", "Save earning rules", op="updateLoyaltyProgramme"),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
      ("contextPanel", [
          c("dataTable", "Bonus campaigns", "MarketingLoyaltyCampaign", "listLoyaltyCampaigns",
            cols("MarketingLoyaltyCampaign", "code", "name", "startAt", "endAt", "isActive")),
          c("textField", "Campaign code", "MarketingLoyaltyCampaign.code", "setLoyaltyCampaign"),
          c("textField", "Campaign name", "MarketingLoyaltyCampaign.name", "setLoyaltyCampaign"),
          c("datePicker", "Starts", "MarketingLoyaltyCampaign.startAt", "setLoyaltyCampaign"),
          c("datePicker", "Ends", "MarketingLoyaltyCampaign.endAt", "setLoyaltyCampaign"),
          c("toggle", "Campaign active", "MarketingLoyaltyCampaign.isActive", "setLoyaltyCampaign"),
          c("secondaryButton", "Save campaign", op="setLoyaltyCampaign",
            notes="programId is the programme being edited."),
          c("dataTable", "Campaign rules", "LoyaltyRuleSet.campaignRules", "getLoyaltyRules",
            cols("MarketingLoyaltyRule", "campaignId", "type", "bonusPoints", "multiplier", "isActive")),
          c("numberField", "Bonus points", "MarketingLoyaltyRule.bonusPoints", "setLoyaltyRules"),
          c("numberField", "Bonus multiplier", "MarketingLoyaltyRule.multiplier", "setLoyaltyRules"),
          c("secondaryButton", "Save campaign rules", op="setLoyaltyRules",
            notes="A whole-set replace: sends the tiers and redemption rules read by getLoyaltyRules "
                  "unchanged with the edited campaign rules."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No earning rules yet: nothing earns points. Carries an "
                                         "empty row to start."),
  note="Defined 4 October 2026 from LoyaltyProgramme.earnRules (trigger, points, productKinds, "
       "multiplier), LoyaltyRuleSet.campaignRules and MarketingLoyaltyCampaign. Earning rules are "
       "saved with updateLoyaltyProgramme (agreed in the ledger), since setLoyaltyRules leaves them "
       "out. Daily and monthly limits and rounding are not in the contract and left the purpose")

F("BO-828", DEF, pattern="configEditor", template="split",
  drop_gaps=("person", "createLoyaltyProgramme", "~cannot be built"),
  patternReason="One programme's milestones (its tiers) and the rewards they give, edited side by "
                "side (defined 4 October 2026 from MarketingProgrammeTier and MarketingReward, "
                "CHG-FXS-001).",
  apis_drop=["createLoyaltyProgramme"],
  apis_add=[A("getLoyaltyRules", "onLoad", "The programme's tiers (its milestones) as saved, read "
                                          "before the whole-set save"),
            A("setLoyaltyRules", "onAction", "Save the milestones: the tiers, with the campaign and "
                                             "redemption rules sent back unchanged")],
  entry=[P("programmeId", "navigation", True,
           "Opened without it, the screen lists the programmes (listLoyaltyProgrammes) and the user "
           "picks one (CHG-FXS-001).")],
  overlays_drop=["formCreateLoyaltyProgramme"],
  regions=[
      ("contentBody", [
          c("selectField", "Programme", "LoyaltyProgramme.id", "listLoyaltyProgrammes",
            cols("LoyaltyProgramme", "code", "name", "isActive")),
          c("dataTable", "Milestones", "LoyaltyRuleSet.tiers", "getLoyaltyRules",
            cols("MarketingProgrammeTier", "rank", "name", "minLifetimePoints", "earnMultiplier", "isActive"),
            notes="A milestone is a tier reached at a lifetime-points threshold, in rank order."),
          c("textField", "Milestone code", "MarketingProgrammeTier.code", "setLoyaltyRules"),
          c("textField", "Milestone name", "MarketingProgrammeTier.name", "setLoyaltyRules"),
          c("numberField", "Rank", "MarketingProgrammeTier.rank", "setLoyaltyRules"),
          c("numberField", "Reached at (lifetime points)", "MarketingProgrammeTier.minLifetimePoints",
            "setLoyaltyRules"),
          c("numberField", "Kept at (lifetime points)", "MarketingProgrammeTier.retainLifetimePoints",
            "setLoyaltyRules"),
          c("numberField", "Valid for (months)", "MarketingProgrammeTier.validityMonths", "setLoyaltyRules"),
          c("multiSelect", "Benefits", "MarketingProgrammeTier.benefits", "setLoyaltyRules",
            notes="Free entries; each is shown to the guest as written."),
          c("numberField", "Earn multiplier", "MarketingProgrammeTier.earnMultiplier", "setLoyaltyRules"),
          c("toggle", "Milestone active", "MarketingProgrammeTier.isActive", "setLoyaltyRules"),
          c("primaryButton", "Save milestones", op="setLoyaltyRules"),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
      ("contextPanel", [
          c("dataTable", "Rewards", "MarketingReward", "listRewards",
            cols("MarketingReward", "code", "name", "type", "pointsCost", "validityDays")),
          c("textField", "Reward code", "MarketingReward.code", "setReward"),
          c("textField", "Reward name", "MarketingReward.name", "setReward"),
          c("textField", "Reward type", "MarketingReward.type", "setReward"),
          c("numberField", "Points cost", "MarketingReward.pointsCost", "setReward"),
          c("numberField", "Discount value", "MarketingReward.discountValue", "setReward"),
          c("numberField", "Valid for (days)", "MarketingReward.validityDays", "setReward"),
          c("toggle", "Reward active", "MarketingReward.isActive", "setReward"),
          c("secondaryButton", "Save reward", op="setReward",
            notes="loyaltyProgramId is the selected programme."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No milestones yet. Carries an empty row to start."),
  note="Defined 4 October 2026: a milestone is a programme tier (MarketingProgrammeTier, a lifetime-"
       "points threshold), saved with setLoyaltyRules after reading getLoyaltyRules; rewards are "
       "MarketingReward through setReward. 'Save milestones and rewards' no longer calls "
       "createLoyaltyProgramme, which creates a programme (programme creation is on BO-824)")

F("BO-825", DEF, pattern="listDetail", template="split", drop_gaps=("all",),
  patternReason="Challenges listed with the selected draft built beside it and a publish gate "
                "(defined 4 October 2026 from Challenge, CHG-FXS-001).",
  overlays_drop=["formCreateChallenge"],
  regions=[
      ("contentBody", [
          c("selectField", "Status", "Challenge.status", "listChallenges", notes="Filter; Draft by default."),
          c("dataTable", "Challenges", "Challenge", "listChallenges",
            cols("Challenge", "name", "kind", "rewardKind", "startsAt", "endsAt", "status")),
          c("primaryButton", "New challenge", notes="Opens an empty draft in the side panel."),
      ]),
      ("contextPanel", [
          c("detailPanel", "The challenge", "Challenge", "getChallenge",
            cols("Challenge", "name", "kind", "goal", "rewardKind", "status")),
          c("textField", "Name", "Challenge.name", "createChallenge"),
          c("selectField", "Challenge action", "Challenge.kind", "createChallenge",
            notes="Includes scan, activity and purchase (audit R275 (c), now in the enum)."),
          c("selectField", "Who takes part", "Challenge.scope", "createChallenge"),
          c("textField", "Goal metric", "Challenge.goal.metric", "createChallenge"),
          c("numberField", "Goal target", "Challenge.goal.target", "createChallenge"),
          c("numberField", "Within (days)", "Challenge.goal.withinDays", "createChallenge",
            notes="Empty means no time limit."),
          c("selectField", "Reward", "Challenge.rewardKind", "createChallenge"),
          c("numberField", "Reward value", "Challenge.rewardValue", "createChallenge",
            notes="Points for loyaltyPoints; hidden for badge and none."),
          c("datePicker", "Starts", "Challenge.startsAt", "createChallenge"),
          c("datePicker", "Ends", "Challenge.endsAt", "createChallenge"),
          c("primaryButton", "Create challenge", op="createChallenge", notes="Saves a draft."),
          c("publishGate", "What activating changes", op="activateChallenge",
            notes="Shows the challenge as guests will see it and its window; Activate publishes it."),
          c("secondaryButton", "Activate challenge", op="activateChallenge",
            perm="MARKETING_SEND", notes="Draft challenges only."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No challenges yet. Carries New challenge."),
  note="Defined 4 October 2026 from Challenge (kind, scope, goal, reward, window) with "
       "listChallenges, getChallenge, createChallenge and activateChallenge. The stale gaps (no write, "
       "no list, kind lacking scan/activity/purchase) are closed: the contract has them since "
       "CHG-CSA-045 and R275 (c)")
