# Segments and campaigns (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

F("BO-755", DEF, pattern="listDetail", template="split",
  drop_gaps=("person", "~declares no operation that writes", "~No preview of unsaved criteria"),
  patternReason="The saved segments beside a rule builder with a live count (defined 4 October 2026 "
                "from CreateSegmentRequest and SegmentRuleGroup, CHG-FXS-001).",
  entry=[P("segmentId", "navigation", True,
           "Opened with one, the builder starts from a copy of that segment's rules; saving creates a "
           "new segment (segments are definitions evaluated when used; there is no edit in place).")],
  overlays_drop=["formCreateSegment"],
  regions=[
      ("contentBody", [
          c("searchField", "Find a segment", "Segment.name", "listSegments", notes="Query `search`."),
          c("dataTable", "Segments", "Segment", "listSegments",
            cols("Segment", "name", "match", "lastEvaluatedSize", "lastEvaluatedAt", "effectiveTo")),
      ]),
      ("contextPanel", [
          c("textField", "Name", "CreateSegmentRequest.name", "createSegment"),
          c("textField", "Description", "CreateSegmentRequest.description", "createSegment"),
          c("selectField", "Match", "CreateSegmentRequest.match", "createSegment",
            notes="All or any, for the top-level criteria."),
          c("selectField", "Attribute", "SegmentCriterion.attribute", "createSegment",
            notes="Profile, visits, spend, products bought, membership, tier, wallet, language, wishlist "
                  "and behaviour. Dietary, accessibility and minors' data are refused for marketing "
                  "segments, with the reason shown (R205)."),
          c("selectField", "Operator", "SegmentCriterion.operator", "createSegment"),
          c("textField", "Value", "SegmentCriterion.value", "createSegment",
            notes="Two values for between; a list for in and not in; none for exists."),
          c("selectField", "Group logic", "SegmentRuleGroup.operator", "createSegment",
            notes="AND, OR or NOT over the group's criteria and child groups; groups nest."),
          c("secondaryButton", "Add rule", notes="Adds a criterion row to the current group."),
          c("secondaryButton", "Add group", notes="Adds a nested SegmentRuleGroup."),
          c("multiSelect", "Exclude segments", "CreateSegmentRequest.excludeSegmentIds", "createSegment",
            notes="Options from listSegments."),
          c("datePicker", "Effective from", "CreateSegmentRequest.effectiveFrom", "createSegment"),
          c("datePicker", "Effective to", "CreateSegmentRequest.effectiveTo", "createSegment"),
          c("toggle", "Needs approval before use", "CreateSegmentRequest.requiresApproval", "createSegment"),
          c("metricTile", "Matching guests", "SegmentDraftPreview.matchingCount", "previewSegmentDraft",
            notes="Recounted 1 s after the rules stop changing. Zero shows the rule that removed the "
                  "most guests, not an empty preview."),
          c("metricTile", "Reachable", "SegmentDraftPreview.reachable", "previewSegmentDraft",
            notes="Per channel, after consent and suppression."),
          c("primaryButton", "Save segment", op="createSegment",
            notes="Saves the definition, not a list; owner is the signed-in user."),
          c("secondaryButton", "Cancel", notes="Discards the unsaved rules; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No segments yet. The builder is open on an empty rule."),
  note="Defined 4 October 2026 from CreateSegmentRequest (criteria, nested ruleGroups, exclusions, "
       "effective dates, approval) and SegmentDraftPreview. The stale gaps are closed: the request "
       "carries rule groups, dates, owner and approval since CHG-CSA-045")

F("BO-766", DEF, pattern="listDetail", template="split",
  drop_gaps=("person", "~declares no operation that writes"),
  patternReason="The campaign library beside a builder for the selected or new campaign (defined 4 "
                "October 2026 from CreateCampaignRequest, CHG-FXS-001).",
  apis_add=[A("listSegments", "onLoad", "The audiences a campaign can target (segmentId)"),
            A("listMessageTemplates", "onLoad", "The templates a campaign's content uses (templateId)")],
  overlays_drop=["formCreateCampaign", "formTestSendCampaign"],
  regions=[
      ("contentBody", [
          c("selectField", "Status", "Campaign.status", "listCampaigns", notes="Filter; All by default."),
          c("dataTable", "Campaigns", "Campaign", "listCampaigns",
            cols("Campaign", "name", "kind", "channel", "status", "scheduledFor", "sentCount")),
          c("primaryButton", "New campaign", notes="Opens the builder empty."),
      ]),
      ("contextPanel", [
          c("textField", "Name", "CreateCampaignRequest.name", "createCampaign"),
          c("selectField", "Kind", "CreateCampaignRequest.kind", "createCampaign"),
          c("selectField", "Channel", "CreateCampaignRequest.channel", "createCampaign"),
          c("selectField", "Audience", "CreateCampaignRequest.segmentId", "listSegments",
            notes="Options from listSegments, each with its last evaluated size."),
          c("selectField", "Template", "CreateCampaignRequest.content.templateId", "listMessageTemplates",
            notes="Options from listMessageTemplates on the chosen channel."),
          c("secondaryButton", "Draft with AI", op="proposeMarketingContent",
            notes="Drafts subject, body and variants within the channel's limits; a person edits and "
                  "applies. Nothing is published by AI."),
          c("selectField", "Send time", "CreateCampaignRequest.sendTimeMode", "createCampaign",
            notes="Fixed, or optimised per guest."),
          c("datePicker", "Scheduled for", "CreateCampaignRequest.scheduledFor", "createCampaign"),
          c("primaryButton", "Create campaign", op="createCampaign", notes="Saves a draft."),
          c("textField", "Test recipients", None, "testSendCampaign",
            notes="Named staff addresses only; the test is marked as a test and never counted."),
          c("secondaryButton", "Send test", op="testSendCampaign"),
          c("secondaryButton", "Launch campaign", op="launchCampaign", perm="MARKETING_SEND",
            notes="Sends confirmAudienceSize, the count the marketer saw; a grown audience is refused "
                  "and shows 'Audience changed - review again'. Consent is checked again at send."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No campaigns yet. Carries New campaign."),
  note="Defined 4 October 2026 from CreateCampaignRequest, testSendCampaign and launchCampaign, with "
       "the audiences (listSegments) and templates (listMessageTemplates) the builder picks from. A/B "
       "variants are set on BO-772")
