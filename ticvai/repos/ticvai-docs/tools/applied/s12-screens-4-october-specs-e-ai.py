# AI governance, decision trace and forecast setup screens (part of s12-screens-4-october-specs.py).
# flake8: noqa


def trace(sid, depth, what, comps):
    F(sid, DEF, pattern="detail", template="split", drop_gaps=("person",),
      patternReason=f"One AI decision's {what}, read from its trace at depth {depth} (defined 4 "
                    "October 2026 from AiDecisionTrace, CHG-FXS-001).",
      apis_set={"getAiDecisionTrace": dict(purpose=f"The decision's trace at depth {depth} (query "
                                                    f"depth={depth}): {what}")},
      regions=[("contentBody", GRANT + [
          c("detailPanel", "Decision", "AiDecisionRecord", "getAiDecisionTrace",
            cols("AiDecisionRecord", "capabilityKey", "task", "subjectKind", "subjectRef", "outcome", "createdAt")),
      ] + comps)],
      states=dict(loading="The decision header first, then the trace.",
                  error="Could not load the trace. Names the decision record id; nothing else changes.",
                  emptyFirstRun="Not used: the screen always opens on one decision (decisionRecordId)."),
      note=f"Defined 4 October 2026 from AiDecisionTrace at depth {depth}: {what}")


trace("ADM-541", "business", "a business-readable explanation", [
    c("detailPanel", "Explanation", "AiDecisionTrace.explanation", "getAiDecisionTrace",
      notes="Plain language, written for the business user; the reliability and the evidence it rests "
            "on follow."),
    c("dataTable", "What it was based on", "AiDecisionRecord.evidence", "getAiDecisionTrace",
      cols("AiEvidenceItem", "label", "name", "value", "observedAt"),
      notes="Each item labelled source, derived or model-inferred (AIC-197)."),
    c("detailPanel", "Model and versions", "AiDecisionRecord", "getAiDecisionTrace",
      cols("AiDecisionRecord", "producer", "modelVersion", "promptTemplateVersion", "policyVersion")),
    c("detailPanel", "Human decision", "AiDecisionRecord.humanDecision", "getAiDecisionTrace"),
])

trace("ADM-542", "technical", "which data and evidence contributed and where each came from", [
    c("dataTable", "Evidence and provenance", "AiDecisionRecord.evidence", "getAiDecisionTrace",
      cols("AiEvidenceItem", "label", "kind", "name", "ref", "value", "observedAt"),
      notes="label is the origin (source system, derived by a rule or feature, inferred by a model); "
            "ref points at the record it was read from."),
    c("detailPanel", "Inputs and versions", "AiDecisionRecord", "getAiDecisionTrace",
      cols("AiDecisionRecord", "inputsRef", "featureSetVersion", "knowledgeVersion", "ruleVersions",
           "modelVersion")),
    c("dataTable", "Model calls", "AiDecisionTrace.activity", "getAiDecisionTrace",
      cols("AiInteraction", "capability", "provider", "model", "sources", "maskedFieldCount", "createdAt"),
      notes="sources are the retrieved passages each call answered from."),
    c("detailPanel", "Chain verified", "AiDecisionTrace.chainVerified", "getAiDecisionTrace",
      notes="Whether the record's hash chain verifies; a break is shown as a red banner."),
])

trace("ADM-545", "governance", "the governance and human decisions around it", [
    c("detailPanel", "Governance", "AiDecisionRecord", "getAiDecisionTrace",
      cols("AiDecisionRecord", "governanceOutcome", "policyVersion", "approvals", "humanDecision",
           "executionResult")),
    c("dataTable", "Interventions", "AiDecisionTrace.interventions", "getAiDecisionTrace",
      cols("AiIntervention", "kind", "targetKind", "reason", "principalId", "createdAt"),
      notes="Overrides, pauses, retries and rollbacks by a person, oldest first."),
    c("detailPanel", "Chain verified", "AiDecisionTrace.chainVerified", "getAiDecisionTrace"),
])

# Filled screens whose generator gap still says a person must define them.
for _sid in ("ADM-527", "ADM-528", "ADM-554", "BO-151", "BO-166", "BO-696", "BO-716", "BO-877",
             "BO-1062", "BO-1065", "BO-1066", "CMS-025", "ANL-047", "ADM-077", "ADM-570", "BO-155"):
    pass  # each gets its own entry below or in its area's file when it needs more than the note

for _sid in ("ADM-527", "ADM-528", "ADM-554"):
    F(_sid, STALE, drop_gaps=("person",),
      note="The generator's 'needs a person' gap removed 4 October 2026: the screen's content is "
           "defined (tables, panels and actions bound to its operations)")

F("ADM-342", STALE, drop_gaps=("person", "setPasswordPolicy"),
  comp_set={"Guest identity verification": dict(bindsTo="IdentityGuestVerificationPolicy",
                                                operation="getGuestVerificationPolicy")},
  note="Stale gaps removed 4 October 2026: the content is defined and getPasswordPolicy is bound, "
       "so setPasswordPolicy saves what was read. The step-up table is bound to StepUpPolicy")


def _adm342(S, pk):
    s = S.get("ADM-342")
    out = []
    if not s:
        return out
    for _, cc in sp.components(s):
        if cc.get("kind") == "dataTable" and cc.get("impliedBy") == "listStepUpPolicies" and not cc.get("bindsTo"):
            cc.update(label="Step-up per action", bindsTo="StepUpPolicy", operation="listStepUpPolicies",
                      columns=cols("StepUpPolicy", "operationId", "required", "contractFloor", "scopeLevel", "reason"),
                      notes="Query effective=true. Raising one sends setStepUpPolicy for that action; "
                            "never below contractFloor.",
                      provenance="contract approvals.yaml StepUpPolicy (4 October 2026, CHG-FXS-005)")
            cc.pop("derived", None)
            cc.pop("impliedBy", None)
            out.append(("ADM-342", "CHG-FXS-005 ADM-342: step-up table bound to StepUpPolicy"))
    return out


EDGES.append(_adm342)

F("ADM-523", BIND, drop_gaps=("person",),
  comp_drop=["Actions the rule covers"],
  add_comps=[
      ("contentBody", c("textField", "Policy name", "AiGovernancePolicy.name", "createAiGovernancePolicyDraft")),
      ("contentBody", c("selectField", "Policy kind", "AiGovernancePolicy.kind", "createAiGovernancePolicyDraft")),
      ("contentBody", c("dataTable", "Rules", "AiGovernancePolicyVersion.rules", "createAiGovernancePolicyDraft",
                        cols("AiGovernanceRule", "effect", "capabilityKeys", "actions", "dataCategories", "roleIds"),
                        notes="At least one rule. Conflicts resolve to the more restrictive (AIC-161).")),
      ("contentBody", c("selectField", "Effect", "AiGovernanceRule.effect", "createAiGovernancePolicyDraft",
                        notes="An AiGovernanceOutcome value; block is an answer, not an error.")),
      ("contentBody", c("multiSelect", "Capabilities", "AiGovernanceRule.capabilityKeys", "createAiGovernancePolicyDraft")),
      ("contentBody", c("multiSelect", "Actions the rule covers", "AiGovernanceRule.actions", "createAiGovernancePolicyDraft",
                        notes="Options are the tools' actions from listAiTools.")),
      ("contentBody", c("multiSelect", "Data categories", "AiGovernanceRule.dataCategories", "createAiGovernancePolicyDraft")),
      ("contentBody", c("multiSelect", "Roles", "AiGovernanceRule.roleIds", "createAiGovernancePolicyDraft")),
      ("contentBody", c("textField", "Change note", "AiGovernancePolicyVersion.changeNote", "createAiGovernancePolicyDraft")),
  ],
  note="Rule fields bound 4 October 2026 to AiGovernanceRule (effect, capabilities, actions, data "
       "categories, roles); effect is required on every rule")

F("BO-919", FCST,
  apis_add=[A("listForecastDefinitions", "onLoad", "The attendance forecast definitions; the picked "
                                                   "one's definitionKey is what getForecast reads")],
  add_comps=[
      ("contentBody", c("selectField", "Forecast", "AiForecastDefinition.definitionKey", "listForecastDefinitions",
                        cols("AiForecastDefinition", "name", "grain", "horizonDays"),
                        notes="Query subject attendance; the first active definition by default.")),
      ("contentBody", c("datePicker", "Event from", "AiForecastPoint.targetStart", "getForecast",
                        notes="The event's first day; getForecast `from` and listOperationalRequirements `from`.")),
      ("contentBody", c("datePicker", "Event to", "AiForecastPoint.targetEnd", "getForecast",
                        notes="The event's last day; `to` on both reads.")),
  ],
  note="The forecast definition and the event's dates are picked on the screen 4 October 2026: "
       "getForecast reads definitionKey with from and to set to the event's days, and "
       "listOperationalRequirements the same window (Event carries no dates, so the window is the "
       "event's days as the planner enters them)")
