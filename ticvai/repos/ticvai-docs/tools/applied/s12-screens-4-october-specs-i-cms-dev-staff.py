# CMS, developer portal and staff app screens (part of s12-screens-4-october-specs.py).
# flake8: noqa

F("CMS-011", READ, drop_gaps=("proposeTranslations",),
  apis_add=[A("proposeTranslations", "onAction",
              "Start machine translation of what a language is missing; its translationJobId is what "
              "getTranslationProposals follows (R288 is answered by that read, CHG-CSA-045)")],
  apis_set={"getTranslationProposals": dict(trigger="onInterval",
                                            purpose="Follow the job started here (every 3 s until "
                                                    "completed or failed) and review its drafts")},
  add_comps=[
      ("contentBody", c("selectField", "Translate into", "TranslationProposals.targetLocale",
                        "proposeTranslations", notes="An enabled language with gaps.")),
      ("contentBody", c("secondaryButton", "Translate missing text", op="proposeTranslations",
                        notes="scope allGaps; the job id is kept on the screen (and in the URL as "
                              "translationJobId so a reload resumes it).")),
  ],
  comp_set={"Proposed translations": dict(kind="cardList", bindsTo="TranslationProposals.drafts",
                                          notes="Each draft is accepted into the language or discarded; "
                                                "nothing is published until accepted.")},
  note="proposeTranslations bound again 4 October 2026: it was removed because nothing could follow the "
       "202 job (R288); getTranslationProposals now does, so the screen starts the job and follows it by "
       "the translationJobId it returns")

F("CMS-086", STALE, drop_gaps=("person",),
  apis_add=[A("listRoles", "onLoad", "The roles a policy applies to (appliesToRoleIds), by name")],
  comp_set={"Roles and asset actions": dict(bindsTo="AuthorisationPolicy", operation="listAuthorisationPolicies",
                                            columns=cols("AuthorisationPolicy", "name", "effect",
                                                         "permissions", "appliesToRoleIds", "effectiveTo"),
                                            notes="One row per policy; role ids shown by the role's "
                                                  "name from listRoles.")},
  add_comps=[
      ("contentBody", c("multiSelect", "Roles", "AuthorisationPolicy.appliesToRoleIds", "listRoles",
                        notes="Options from listRoles, by name.")),
      ("contentBody", c("multiSelect", "Asset actions", "AuthorisationPolicy.permissions", "createAuthorisationPolicy",
                        notes="ASSET_LIBRARY_VIEW, ASSET_LIBRARY_SHARE, ASSET_LIBRARY_APPROVE, ASSET_LIBRARY_MANAGE, "
                              "ASSET_VIEW and ASSET_MANAGE (the permission vocabulary).")),
      ("contentBody", c("textField", "Policy name", "AuthorisationPolicy.name", "createAuthorisationPolicy")),
      ("contentBody", c("textField", "Policy code", "AuthorisationPolicy.code", "createAuthorisationPolicy")),
      ("contentBody", c("selectField", "Effect", "AuthorisationPolicy.effect", "createAuthorisationPolicy")),
  ],
  note="The generator's 'needs a person' gaps removed 4 October 2026 (the screen is filled); the roles "
       "come from listRoles so a policy's appliesToRoleIds can be picked by name")

F("DEV-001", READ,
  comp_set={None: {}},
  note="The reference content is the published OpenAPI document of the selected version, a static file "
       "built from the release's public contract and served with the portal "
       "(`/reference/{version}/openapi.json`); listApiVersions picks the version and listApiScopes groups "
       "the operations (ApiScope.operations). The operation panel, code samples and search read that "
       "file, so no API call returns them (default taken 4 October 2026, Chinmay to review)")
FIXES[-1].pop("comp_set")
FIXES[-1]["comp_set"] = {
    "Search operations": dict(notes="Searches operation ids, paths and summaries in the selected "
                                    "version's OpenAPI file."),
}


def _dev001(S, pk):
    s = S.get("DEV-001")
    out = []
    if not s:
        return out
    for _, cc in sp.components(s):
        if cc.get("kind") == "detailPanel" and cc.get("bindsTo") == "operation":
            cc.update(label="Operation", bindsTo=None,
                      notes="Method, path, summary, scopes, request and response schemas and error codes "
                            "of the operation picked in the tree, read from the version's OpenAPI file.",
                      provenance="defined 4 October 2026 (CHG-FXS-003)")
            out.append(("DEV-001", "CHG-FXS-003 DEV-001: operation panel reads the OpenAPI file"))
        if cc.get("kind") == "codeBlock" and not cc.get("notes"):
            cc.update(label="Code samples", notes="curl, JavaScript and C# samples generated from the "
                                                  "operation in the OpenAPI file.",
                      provenance="defined 4 October 2026 (CHG-FXS-003)")
        if cc.get("kind") == "primaryButton" and cc.get("label") == "Try it" and not cc.get("notes"):
            cc["notes"] = ("Sends the request to the developer's sandbox with their sandbox token; "
                           "disabled until they sign in.")
    return out


EDGES.append(_dev001)

F("EMP-002", READ,
  entry_set={"preloaded": ["LoginResponse.availableRoles"]},
  add_comps=[
      ("contentBody", c("cardList", "Choose your role for today", "LoginResponse.availableRoles", None,
                        cols("RoleSummary", "name", "code", "isPrimary"),
                        notes="Handed over by EMP-001 from the login response (requiresRoleSelection "
                              "true); nothing is fetched. The primary role is first. The venue is the "
                              "role's scope, shown on the session after selectRole.")),
  ],
  note="Roles come from the login response EMP-001 holds (LoginResponse.availableRoles, preloaded) 4 "
       "October 2026; selectRole sends the picked roleId. A role carries its venue scope, so there is no "
       "separate venue pick")
carry("EMP-001", "EMP-002", ["availableRoles"], trigger="Several roles: choose one")
