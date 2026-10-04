"""The screen fixes of the Sprint 1-2 fix round (4 October 2026), as data: one entry per screen.

Read by `s12-screens-4-october.py`. Each entry names the screen, its change entry, and what changes:
`regions` (the layout, replacing the old one), `apis_add` / `apis_drop`, `drop_gaps` ("person"
closes the generator's "needs a person" gaps; an operation name closes that operation's gap; "~text"
closes a gap whose reason contains the text), `gaps_add`, `entry` (the entry parameters), `set`
(top-level fields), `states`, `overlays`, `comp_set` (rebind a component by its label), `comp_drop`
and `note` (what was decided and from what, appended to the screen's notes with the entry id).

Operations named here that the contracts do not have yet are the names agreed in
`audit/ticvai/runs/fix-s12/LEDGER.md` with the contracts agent; each says so in its purpose.
"""

FIXES: list = []
EDGES: list = []

DEF = "CHG-FXS-001"     # "needs a person" screens defined from the package
BIND = "CHG-FXS-002"    # fields bound to the request and response schemas
READ = "CHG-FXS-003"    # the id or record a call needs, read on the screen
FCST = "CHG-FXS-004"    # forecast screens pick their forecast definition
STALE = "CHG-FXS-005"   # stale gap notes on filled screens
AGREED = "agreed with the contracts agent, runs/fix-s12/LEDGER.md, 4 October 2026"


def c(kind, label, b=None, op=None, cols=None, notes=None, perm=None):
    return dict(kind=kind, label=label, bindsTo=b, operation=op, columns=cols, notes=notes,
                permission=perm)


def A(op, trigger, purpose, contract=None):
    d = dict(operationId=op, trigger=trigger, purpose=purpose)
    if contract:
        d["contract"] = contract
    return d


def P(name, frm, optional=None, notes=None):
    d = dict(name=name, **{"from": frm})
    if optional:
        d["optional"] = True
    if notes:
        d["notes"] = notes
    return d


def F(sid, chg, **kw):
    FIXES.append(dict(sid=sid, chg=chg, **kw))


def carry(src, dst, params, trigger=None, chg="CHG-FXS-003"):
    """The edge src -> dst carries `params` (an entry parameter the destination requires)."""
    def fn(S, pk):
        s = S.get(src)
        if not s or dst not in S:
            return []
        nav = s.setdefault("navigation", {})
        tr = nav.setdefault("transitions", [])
        t = next((x for x in tr if isinstance(x, dict) and str(x.get("to")).partition("#")[0] == dst), None)
        if t is None:
            t = {"to": dst, "trigger": trigger or ("Open " + S[dst].get("name", dst)),
                 "provenance": f"defined 4 October 2026 ({chg})"}
            tr.append(t)
            if dst not in (nav.get("exitTo") or []):
                nav.setdefault("exitTo", []).append(dst)
        have = list(t.get("carries") or [])
        add = [p for p in params if p not in have]
        if not add:
            return []
        t["carries"] = have + add
        return [(src, f"{chg} {src}: edge to {dst} carries " + ", ".join(add))]
    EDGES.append(fn)


def cols(schema, *fields):
    return [f"{schema}.{f}" for f in fields]


LIST_STATES = dict(
    loading="The list skeleton, with the filters already drawn.",
    error="Could not load. Names which read failed and leaves what is on screen untouched.",
)

# ── Marketing ────────────────────────────────────────────────────────────────────────────────────

F("BO-772", DEF, pattern="configEditor", template="split", drop_gaps=("person",),
  patternReason="One campaign's A/B test edited in place beside its results and the AI's "
                "recommendations on it (defined 4 October 2026 from Campaign.variants and "
                "Campaign.abTest, CHG-FXS-001).",
  apis_add=[A("getCampaign", "onLoad", "The campaign with its variants and A/B settings, as saved"),
            A("getCampaignPerformance", "onLoad", "Results per variant, to compare and pick a winner"),
            A("listMessageTemplates", "onLoad", "The templates a variant can use"),
            A("updateCampaign", "onAction",
              "Save the variants and the A/B test, and pick the winner by hand (abTest.winnerRule "
              "manual): `variants` and `abTest` in the PATCH body, " + AGREED)],
  regions=[
      ("contentBody", [
          c("detailPanel", "Campaign", "Campaign", "getCampaign",
            cols("Campaign", "name", "channel", "status", "scheduledFor", "sendTimeMode")),
          c("dataTable", "Variants", "Campaign.variants", "getCampaign",
            cols("MarketingCampaignVariant", "label", "templateId", "splitPercent", "source", "isWinner"),
            notes="Two or more variants make an A/B test. A row is edited in place; the split "
                  "percentages add up to 100 before Save is enabled."),
          c("textField", "Variant label", "Campaign.variants.label", "updateCampaign"),
          c("selectField", "Variant template", "Campaign.variants.templateId", "listMessageTemplates",
            notes="Options from listMessageTemplates filtered to the campaign's channel."),
          c("numberField", "Variant split (%)", "Campaign.variants.splitPercent", "updateCampaign"),
          c("secondaryButton", "Add variant", notes="Adds an empty row; nothing is sent until Save."),
          c("secondaryButton", "Draft a variant with AI", op="proposeMarketingContent",
            notes="Drafts subject and body from a brief; the draft becomes a variant with source "
                  "aiDraft only when the author saves it. AI drafts, a person applies (campaigns L2)."),
          c("numberField", "Test share of the audience (%)", "Campaign.abTest.testPercent", "updateCampaign",
            notes="5 to 100, default 20; 100 splits everyone and picks no winner."),
          c("selectField", "Success metric", "Campaign.abTest.successMetric", "updateCampaign"),
          c("numberField", "Decide after (hours)", "Campaign.abTest.decideAfterHours", "updateCampaign"),
          c("selectField", "Winner rule", "Campaign.abTest.winnerRule", "updateCampaign"),
          c("numberField", "Minimum sends per variant", "Campaign.abTest.minimumSamplePerVariant",
            "updateCampaign"),
          c("primaryButton", "Save A/B test", op="updateCampaign"),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
      ("contextPanel", [
          c("dataTable", "Results by variant", "CampaignPerformance.variants", "getCampaignPerformance",
            ["CampaignPerformance.variants.label", "CampaignPerformance.variants.sent",
             "CampaignPerformance.variants.opened", "CampaignPerformance.variants.clicked",
             "CampaignPerformance.variants.attributedRevenue", "CampaignPerformance.variants.isWinner"]),
          c("selectField", "Winning variant", "Campaign.abTest.winningVariantId", "updateCampaign",
            notes="Shown when the winner rule is manual, or the automatic rule declared none because a "
                  "variant is below the minimum sends. Options are the campaign's variants."),
          c("primaryButton", "Pick winner", op="updateCampaign"),
          c("dataTable", "AI recommendations", "AiMarketingRecommendation", "listMarketingRecommendations",
            cols("AiMarketingRecommendation", "recommendation", "expectedImpact", "rationale",
                 "priority", "status"),
            notes="targetKind campaign, targetRef the campaignId. Uplift is shown as a range with its "
                  "evidence; accepting one does not change the campaign (a person applies it)."),
          c("secondaryButton", "Accept recommendation", op="decideAiInsight"),
          c("secondaryButton", "Reject recommendation", op="decideAiInsight"),
          c("secondaryButton", "Suggest a send time", op="requestSuggestion",
            notes="kind sendTime; the suggestion is shown beside the schedule and applied by a person."),
      ]),
  ],
  states=dict(loading="The campaign, its variants and results load together.",
              error="Could not load. Names which read failed (campaign, results or recommendations) "
                    "and leaves the campaign untouched.",
              emptyFirstRun="No variants yet: the campaign sends one content. Add variant starts a test.",
              emptyNoResults="No results yet: the test has not sent. Results appear after the first send."),
  note="Defined 4 October 2026 from Campaign.variants, Campaign.abTest, CampaignPerformance.variants "
       "and the AI design notes (ai.yaml BO-772): one campaign's A/B test, its results and the AI's "
       "recommendations. updateCampaign carries variants and abTest (the contract says both are "
       "written by updateCampaign; the PATCH body gains them, agreed in the ledger)")
