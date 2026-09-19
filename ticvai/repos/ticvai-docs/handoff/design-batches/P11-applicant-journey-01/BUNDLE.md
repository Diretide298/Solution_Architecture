# P11-applicant-journey-01 — P11 · Applicant Journey

**5 screens · 2 operations · 1 schemas · 2 permissions**

Platform P11 Accreditation Web · ships as **ticvai-control** ·
public audience · web ·
online only

## Who this is for

**public on web.** Everything below is how you know what is
true. **None of it is the subject.** The subject is the person in front of the screen and the one
thing they came to do.

## What to build

**A working surface, not a drawing of one.** Two references, both built from these same sources:

- `sources/designs/TICVAI_Mobile.dc.html` — 54 screens in one navigable file, 133 animations,
  a live seat map, a five-stage payment flow. **This is the bar for finish.**
- `sources/designs/TICVAI_POS_Terminal_client_approved.html` — the client-approved POS build. **This is the bar for operator density.**

`sources/designs/ticvai-motion-and-interaction.md` names every mechanism in them. Open them and
match their depth. Do not describe them, read them.

## The one rule that outranks the rest

**Nothing in this bundle may appear as text a user can read.** Not an operation id, not a schema
field name, not a permission key, not a screen id, not a file path, not a finding reference.

A homepage that prints `getTenantAppStatus → listProducts` under its header, or labels a column
`venueId · scopePath`, has published its own homework. It happened on `WEB-001`: four products on
sale and not a single price on the page, because the build rendered what `listProducts` returns
instead of what a guest wants — a photo, a name, a price, and a way to book.

**The test: would the person this screen is for understand every word on it?** If a line would
confuse them, it is spec leakage, not design. `bindsTo` tells you what data to invent
convincingly. It is never a caption.

## What is in this folder

| file | what it is |
|---|---|
| `screens.json` | Every field of every screen in the batch. `machine` is what a screen is *in the middle of*; `overlays` is what opens over it and what closing it does; `navigation.transitions` is how you leave, with `carries` naming the state that travels. |
| `operations.json` | Method, path, parameters, request and response schema for every operation these screens call. Write fetches against these; do not invent endpoints. |
| `schemas.json` | The data those operations carry, resolved one level deep. **Seed from these.** The prototype hardcodes 57 models and every one corresponds to a schema here — a build that invents its own will disagree with the backend on day one. |

## Rules that are not style preferences

- **Every control that can be refused must be gated.** 2 permissions apply here:
  `APPROVAL_ACT, APPROVAL_VIEW`. A control nobody can use must say so,
  not sit enabled and fail.
- **0 of these operations work offline**
  
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `ACC-001` | Landing / Programme Overview | publicPortalLanding | 0 | 0 | — |
| `ACC-002` | Registration Form | multiStepForm | 0 | 1 | — |
| `ACC-003` | Application Review & Submit | multiStepForm | 0 | 1 | — |
| `ACC-004` | Application Status Tracking | statusTracker | 0 | 1 | — |
| `ACC-005` | Accreditation Badge | credentialView | 2 | 0 | — |

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "ACC-001",
  "name": "Landing / Programme Overview",
  "module": "Applicant Journey",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "publicPortalLanding",
  "density": "compact",
  "purpose": "Explain what accreditation at this venue is, what an application needs, and how long it takes — then offer the two ways in. **The explanation is the screen**, not a preamble to it.\n",
  "apis": [],
  "apisNote": "**Zero operations is correct here and is not a gap.** The programme text is content, not data, and a landing page that fetches before it can say what it is has made an applicant wait to read a paragraph. Confirmed against the drawn frame, which reaches the same conclusion.\n",
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "introduction",
     "components": [
      {
       "kind": "detailPanel",
       "label": "What accreditation is, and is not",
       "notes": "Programme, guidelines, and **what accreditation is not** — the section that prevents most refused applications, because the common failure is applying for the wrong thing.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-001"
      },
      {
       "kind": "detailPanel",
       "label": "What you will need",
       "notes": "Press card number if held, the performances they intend to cover, and a commission letter. **Listed before the form opens**, because an applicant who discovers on step three that they need a document from an editor abandons the application.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-001"
      },
      {
       "kind": "detailPanel",
       "label": "How long it takes",
       "notes": "Time to apply, time to a decision, and the cut-off before the performance. **Three numbers, stated** — CF and MoM both record that the absence of a stated turnaround is what generates the phone calls this screen exists to prevent.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-001"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "entryActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Start an application",
       "notes": "Goes to ACC-002."
      },
      {
       "kind": "secondaryButton",
       "label": "Track an existing one",
       "notes": "**Resume is not optional.** An application abandoned partway is the common case, and `ACC-004` takes a reference rather than a login.\n"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The programme text, from the CMS bundle. Nothing is fetched per applicant.",
   "error": "**Content failed and the two actions still work.** An applicant who knows what they came to do should not be blocked by a paragraph that did not load.\n",
   "emptyNoResults": "No programme is open. Says when the next one opens rather than showing an empty page — *\"accreditation for the winter season opens 4 November\"* is an answer; a blank screen is not.\n",
   "emptyFirstRun": "No programme is open yet. Says when the next one opens rather than showing an empty page — a date is an answer, a blank screen is not."
  },
  "navigation": {
   "isEntryPoint": true,
   "exitTo": [
    "ACC-002",
    "ACC-004"
   ],
   "notes": "**Corrected 9 September.** The previous `exitTo` also listed `ACC-003`, which is the review step inside the application and cannot be reached from a landing page. Inferred navigation had made every P11 screen a child of this one.\n",
   "transitions": [
    {
     "to": "ACC-002",
     "trigger": "Registration Form",
     "provenance": "structural — ACC-001 is P11's home screen and its exits are its launcher"
    },
    {
     "to": "ACC-004",
     "trigger": "Application Status Tracking",
     "provenance": "structural — ACC-001 is P11's home screen and its exits are its launcher"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/applicant-journey/landing-programme-overview",
   "component": "apps/accreditation-web/src/routes/applicant-journey/LandingProgrammeOverviewDetail.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-001"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-002",
  "name": "Registration Form",
  "module": "Applicant Journey",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "multiStepForm",
  "density": "compact",
  "purpose": "Collect who the applicant works for, what they intend to cover, and the documents that support it — in steps, with a draft that survives leaving.\n",
  "apis": [],
  "gaps": [
   {
    "operation": "createAccreditationApplication",
    "why": "**The registration form cannot register.** The screen declared `listApprovalRequests`, which is a reviewer's read, and nothing that creates an application. Removed 9 September rather than left in place: an operation that is on a screen because it was nearby is the residue pattern this package has now found five times.\n",
    "source": "7 September workshop — accreditation form builder, categories and programme setup"
   },
   {
    "operation": "saveAccreditationDraft",
    "why": "The pattern requires a draft that autosaves. **A four-step form that loses everything to a dropped connection is a form people do not come back to**, and the drawn frame offers *\"Save and finish later\"* against nothing.\n",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-002"
   }
  ],
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Step 1 of 4 — Organisation",
       "notes": "Organisation · Coverage · Documents · Check and submit.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "fields",
     "components": [
      {
       "kind": "textField",
       "label": "Organisation",
       "notes": "Who you work for. Free text — an outlet that is not on a list is still an outlet.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      },
      {
       "kind": "selectField",
       "label": "Role",
       "notes": "Photographer, writer, broadcast, technical. **Drives what coverage may be requested.**",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      },
      {
       "kind": "textField",
       "label": "Press card number",
       "notes": "Optional, and marked so. Its absence is a reviewer's signal, not a blocker.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      },
      {
       "kind": "textField",
       "label": "Commissioning editor",
       "notes": "Who commissioned the coverage, where there is one.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      },
      {
       "kind": "fileUpload",
       "label": "Supporting documents",
       "notes": "Commission letter and badge photo. Accepted formats stated before the picker opens.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      },
      {
       "kind": "consentBlock",
       "label": "Consent",
       "notes": "**Stated once, unticked, and collected before documents rather than after.** The 2 September session recorded consent language as a live question for face data; the same principle applies to a press photograph. An accepted-by-default consent is not consent.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-002"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Continue"
      },
      {
       "kind": "secondaryButton",
       "label": "Save and finish later"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "saveAndExit",
    "component": "confirmDialog",
    "trigger": "Save and finish later",
    "body": "**Says what is kept and how to get back.** *\"Your draft is saved. Return with reference ACC-4417\"* — a dialog that says only *\"saved\"* leaves the applicant with nothing to return with.\n",
    "provenance": "authored, from pattern multiStepForm"
   }
  ],
  "states": {
   "loading": "The draft, where one exists.",
   "emptyFirstRun": "A new application. Step one, nothing prefilled except what the account knows.",
   "error": "**The draft is safe and the step is not lost.** Errors on a long form must never clear entered fields.\n",
   "denied": "The programme is closed. Says when it reopens."
  },
  "entryState": {
   "params": [
    {
     "name": "applicationRef",
     "from": "deepLink",
     "optional": true
    }
   ],
   "preloaded": [
    "programmeName"
   ],
   "coldEntry": "**Reached from the landing page, or resumed from a link in an acknowledgement email weeks later.** A reference that no longer resolves says the programme closed and offers the current one, rather than showing an empty form.\n"
  },
  "navigation": {
   "entryFrom": [
    "ACC-001"
   ],
   "exitTo": [
    "ACC-001",
    "ACC-003",
    "ACC-007"
   ],
   "transitions": [
    {
     "to": "ACC-007",
     "trigger": "A reviewer checks and approves",
     "provenance": "flow F23 step 1→2"
    },
    {
     "to": "ACC-003",
     "trigger": "Application Review & Submit",
     "carries": [
      "applicationRef"
     ],
     "provenance": "derived — ACC-003 declares entryState.params applicationRef, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/applicant-journey/registration-form",
   "component": "apps/accreditation-web/src/routes/applicant-journey/RegistrationForm.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-002"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-003",
  "name": "Application Review & Submit",
  "module": "Applicant Journey",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "multiStepForm",
  "density": "compact",
  "purpose": "Show everything the applicant entered, let them change any of it, say what happens next, and submit.\n",
  "apis": [],
  "gaps": [
   {
    "operation": "submitAccreditationApplication",
    "why": "**The submit button has nothing behind it.** The screen declared no operation at all, and submit is the one act it exists for.\n",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-003"
   }
  ],
  "layout": {
   "template": "wizard",
   "regions": [
    {
     "name": "contentBody",
     "slot": "progress",
     "components": [
      {
       "kind": "progressIndicator",
       "label": "Step 4 of 4 — Check and submit"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "review",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Organisation",
       "notes": "**Every answer, each with its own Change link back to the step that owns it.** *Change*, not *Back* — an applicant on step four wants to fix one field, not walk backwards through three.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-003"
      },
      {
       "kind": "detailPanel",
       "label": "Coverage requested",
       "notes": "Named performances and named areas — *\"stalls, pit\"*. **Coverage is specific, and that is the point**: a badge that says *press* and nothing else is a badge a steward cannot act on, which is the same decision `ACC-005` renders.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-003"
      },
      {
       "kind": "detailPanel",
       "label": "Documents",
       "notes": "Each file with its accepted-or-not state, so a rejected upload is visible before submit.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-003"
      },
      {
       "kind": "detailPanel",
       "label": "What happens next",
       "notes": "An acknowledgement immediately, a decision within a stated number of working days. **Set before submit, not after** — this is where the expectation is formed.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-003"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "submit",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Submit application"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "submitConfirm",
    "component": "confirmDialog",
    "trigger": "Submit application",
    "body": "Names what is being submitted and that it cannot be edited afterwards, only withdrawn.\n",
    "provenance": "authored, from pattern multiStepForm"
   }
  ],
  "states": {
   "loading": "The completed draft.",
   "error": "**Submission failed and nothing was lost.** The application stays a draft and the button stays available.\n",
   "denied": "The programme closed while the application was open. Says so plainly.",
   "emptyNoResults": "No draft to review. Sends the applicant to `ACC-002` rather than showing an empty summary.\n",
   "emptyFirstRun": "No draft to review. Sends the applicant to ACC-002 rather than showing an empty summary."
  },
  "entryState": {
   "params": [
    {
     "name": "applicationRef",
     "from": "ACC-002"
    }
   ],
   "preloaded": [
    "everything entered on ACC-002"
   ],
   "coldEntry": "**Cannot be reached cold and should not be.** Opened directly, it loads the draft behind the reference or says the reference is unknown.\n"
  },
  "navigation": {
   "entryFrom": [
    "ACC-002"
   ],
   "exitTo": [
    "ACC-002",
    "ACC-004"
   ],
   "transitions": [
    {
     "to": "ACC-002",
     "trigger": "Registration Form",
     "carries": [
      "applicationRef"
     ],
     "provenance": "derived — ACC-002 declares entryState.params applicationRef, so an edge into it must carry them"
    },
    {
     "to": "ACC-004",
     "trigger": "Application Status Tracking",
     "carries": [
      "applicationRef"
     ],
     "provenance": "derived — ACC-004 declares entryState.params applicationRef, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/applicant-journey/application-review-and-submit",
   "component": "apps/accreditation-web/src/routes/applicant-journey/ApplicationReviewAndSubmitWizard.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-003"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-004",
  "name": "Application Status Tracking",
  "module": "Applicant Journey",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "statusTracker",
  "density": "compact",
  "purpose": "Tell an applicant where their application is and when they will hear — **with a date, not a queue position.**\n",
  "apis": [],
  "gaps": [
   {
    "operation": "getAccreditationApplicationByReference",
    "why": "**A status screen with no status read.** The screen declared no operation. It also cannot use the reviewer's `listApprovalRequests`: an applicant is not authenticated as a principal with approval permissions, and **the reference is the credential** — which is a deliberate design decision and needs an operation shaped for it.\n",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-004"
   },
   {
    "operation": "withdrawAccreditationApplication",
    "why": "The screen offers *Withdraw this application* and nothing performs it.",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-004"
   },
   {
    "operation": "addAccreditationDocument",
    "why": "The screen offers *Add a document* — the common reviewer request — and nothing performs it.",
    "source": "frame claude-design/Accreditation Board.dc.html#acc-004"
   }
  ],
  "layout": {
   "template": "detail",
   "regions": [
    {
     "name": "contentBody",
     "slot": "state",
     "components": [
      {
       "kind": "banner",
       "label": "With a reviewer",
       "bindsTo": "ApprovalRequest.status",
       "notes": "Where it is now, and **the date a decision is due** — `ApprovalRequest.slaDueAt`. *\"Fourth in the queue\"* was considered and rejected on the frame: a position moves backwards and a date does not.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-004"
      },
      {
       "kind": "timeline",
       "label": "Where it has been",
       "bindsTo": "ApprovalRequest.decisions",
       "notes": "Received, documents checked, decision — each with its date.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-004"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "record",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Application",
       "bindsTo": "ApprovalRequest.summary",
       "notes": "The reference, the performances, and what was requested.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-004"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "actions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Add a document"
      },
      {
       "kind": "destructiveButton",
       "label": "Withdraw this application"
      }
     ]
    }
   ]
  },
  "overlays": [
   {
    "id": "confirmWithdraw",
    "component": "confirmDialog",
    "trigger": "Withdraw this application",
    "body": "**States that withdrawal is final and the programme may close before a new application can be made.** A withdrawal that can be made by accident is one the venue hears about by telephone.\n",
    "provenance": "authored, from pattern statusTracker"
   }
  ],
  "states": {
   "loading": "The application behind the reference.",
   "emptyNoResults": "**The reference is not recognised.** Says so without hinting whether it once existed — a status endpoint that distinguishes *never existed* from *withdrawn* is an enumeration oracle.\n",
   "error": "Could not load. The reference is unaffected and can be retried.",
   "denied": "The reference has expired. Applications are readable for a stated period after the season.",
   "emptyFirstRun": "No application behind this reference yet — a reference issued but not submitted. Points back at the draft."
  },
  "entryState": {
   "params": [
    {
     "name": "applicationRef",
     "from": "deepLink"
    }
   ],
   "preloaded": [],
   "coldEntry": "**This screen is always reached cold** — from an acknowledgement email, usually weeks later and often on a different device. That is the design, and it is why the reference is the only thing it takes.\n"
  },
  "navigation": {
   "entryFrom": [
    "ACC-001",
    "ACC-003"
   ],
   "exitTo": [
    "ACC-001",
    "ACC-005"
   ],
   "transitions": [
    {
     "to": "ACC-005",
     "trigger": "Accreditation Badge",
     "carries": [
      "applicationRef"
     ],
     "provenance": "derived — ACC-005 declares entryState.params applicationRef, so an edge into it must carry them"
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/applicant-journey/application-status-tracking",
   "component": "apps/accreditation-web/src/routes/applicant-journey/ApplicationStatusTrackingDetail.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-004"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "ACC-005",
  "name": "Accreditation Badge",
  "module": "Applicant Journey",
  "wave": 3,
  "requiresModule": "accreditation",
  "pattern": "credentialView",
  "density": "touchLarge",
  "densityReason": "**Held up at a stage door, at night, by somebody carrying equipment.** The same handheld that scans a ticket scans this, and the failure mode is a steward asking the holder to brighten their screen.\n",
  "purpose": "Present the issued badge so it can be scanned, and say exactly where it is valid.\n",
  "apis": [
   {
    "operationId": "listAccreditationBadges",
    "contract": "approvals",
    "purpose": "The badges issued against this application",
    "trigger": "onLoad"
   },
   {
    "operationId": "issueAccreditationBadge",
    "contract": "approvals",
    "purpose": "Issue the badge",
    "trigger": "onAction"
   }
  ],
  "gaps": [
   {
    "operation": "getAccreditationBadge",
    "why": "The screen shows one badge and the only read is a list. **A holder opening their own badge should not fetch every badge issued** — and `listAccreditationBadges` carries a reviewer's permission, which an applicant does not have.\n",
    "source": "contract approvals.yaml — listAccreditationBadges is the only badge read"
   }
  ],
  "layout": {
   "template": "fullscreen",
   "regions": [
    {
     "name": "contentBody",
     "slot": "credential",
     "components": [
      {
       "kind": "credentialDisplay",
       "label": "Your badge",
       "bindsTo": "AccreditationBadge",
       "notes": "The scannable credential, rendered large and bright. **Offline is required** — a stage door is the worst signal in the building, and the 2 September decision that a dynamic-QR ticket is redirected into the app exists for exactly this reason.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-005"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "identity",
     "components": [
      {
       "kind": "detailPanel",
       "label": "Holder",
       "bindsTo": "AccreditationBadge.holderName",
       "notes": "Name, role and outlet, as printed. Photographer · The Northern Review.",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-005"
      },
      {
       "kind": "detailPanel",
       "label": "Where it works",
       "bindsTo": "AccreditationBadge.zones",
       "notes": "**Stage door, stalls and pit, named performances — and *any other door, refused*.** The negative case is stated on the badge because the steward reads this, not a policy.\n",
       "provenance": "frame claude-design/Accreditation Board.dc.html#acc-005"
      }
     ]
    },
    {
     "name": "contentBody",
     "slot": "validity",
     "components": [
      {
       "kind": "banner",
       "label": "Valid until",
       "bindsTo": "AccreditationBadge.expiresAt",
       "notes": "**`expired` and `revoked` must be unmistakable and must not resemble `loading`.** `AccreditationBadge.state` carries both, and `revokedReason` says why.\n",
       "provenance": "contract approvals.yaml AccreditationBadge.state"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "actions",
     "components": [
      {
       "kind": "secondaryButton",
       "label": "Add to phone"
      },
      {
       "kind": "secondaryButton",
       "label": "Print"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The badge.",
   "emptyNoResults": "No badge yet — the application has not been approved. Points at `ACC-004`.",
   "error": "Could not refresh. **The cached badge still displays and says when it was last checked.**",
   "offline": "**Serves the cached badge and says so.** A badge that will not render without a network is a badge that fails at the door it was issued for.\n",
   "emptyFirstRun": "No badge issued yet. The application has not been approved; points at ACC-004."
  },
  "entryState": {
   "params": [
    {
     "name": "applicationRef",
     "from": "ACC-004",
     "optional": true
    }
   ],
   "preloaded": [
    "holderName"
   ],
   "coldEntry": "Opened from a bookmark or a wallet pass. Loads the badge behind the reference, or explains that badges are issued only after approval.\n"
  },
  "navigation": {
   "entryFrom": [
    "ACC-004",
    "ACC-007"
   ],
   "exitTo": [
    "ACC-004"
   ],
   "transitions": [
    {
     "to": "ACC-004",
     "trigger": "Application Status Tracking",
     "carries": [
      "applicationRef"
     ],
     "provenance": "derived — ACC-004 declares entryState.params applicationRef, so an edge into it must carry them"
    },
    {
     "to": "SCN-003",
     "trigger": "A steward scans it at a service gate",
     "provenance": "flow F23 step 3→4",
     "operation": "issueAccreditationBadge",
     "crossesDevice": true,
     "back": false
    }
   ]
  },
  "implementation": {
   "app": "accreditation-web",
   "route": "/applicant-journey/accreditation-badge",
   "component": "apps/accreditation-web/src/routes/applicant-journey/AccreditationBadgeDetail.tsx",
   "status": "notStarted"
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P11 Accreditation Web.dc.html#acc-005"
  },
  "resolvedQuestions": [
   "Unblocked by the 7 September workshop (TICVAI_MoM_2026-09-07_Accreditation_Entitlements_VirtualQueue), which this question said did not exist. Decided there - identity documents are OCR'd to auto-populate the form, and the extracted data is stored as structured fields rather than only the image, because expiry tracking and renewal prompts cannot read a scan; uniqueness is enforced on passport and Emirates ID and a duplicate submission is blocked; the web portal is primary with the mobile app a secondary route for individual applicants. And one decision removes screens rather than adding them - accreditation- holder monitoring is to be a filtered view inside general entitlement monitoring, not a separate system. Capability and API mapping can now be done; 74 pages of ACCREDITATION.pdf are also in the design corpus and no operation has been drafted from them yet."
  ],
  "_platform": {
   "code": "P11",
   "audience": "public",
   "formFactor": "web",
   "shortName": "Accreditation Web",
   "name": "Accreditation Web — Applications",
   "offlineCapable": false,
   "app": "accreditation-web",
   "operator": "public",
   "targetApp": {
    "app": "ticvai-control",
    "name": "TICVAI Control",
    "shell": "web",
    "siblings": [
     "P09",
     "P10",
     "P14",
     "P17"
    ],
    "note": "**TICVAI operates all five**, whoever signs in. The partner portal, the accreditation intake, the developer portal and the sign-up are outward faces of the control plane, not separate products — but their users are not TICVAI staff, and the permission model has to hold that line. **P17 added 11 September 2026**: a prospect buying TICVAI has no tenant and no cell, so the control plane is the only thing that can serve them.",
    "decided": "10 September 2026"
   }
  }
 }
]
```

## `operations.json`

Method, path, parameters, request and response for every operation these screens call. **Write fetches against these and do not invent an endpoint** — a screen needing something absent here is a finding worth reporting, not a gap to fill with a plausible URL.

```json
{
 "issueAccreditationBadge": {
  "method": "POST",
  "path": "/accreditation-badges",
  "contract": "approvals",
  "summary": "Issue a badge",
  "permission": "APPROVAL_ACT",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": "AccreditationBadge",
  "responds": "AccreditationBadge"
 },
 "listAccreditationBadges": {
  "method": "GET",
  "path": "/accreditation-badges",
  "contract": "approvals",
  "summary": "Badges issued and their state",
  "permission": "APPROVAL_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [],
  "requestBody": null,
  "responds": "AccreditationBadge"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "AccreditationBadge": {
  "type": "object",
  "x-ticvai-persistence": "approvals.accreditation_badge",
  "description": "**Drafted 4 September.** The credential an approved application produces. **Its lifetime is not the approval's** - a badge is revoked, lost or expires while the decision that authorised it still stands.",
  "required": [
   "id"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "approvalRequestId": {
    "type": "string",
    "format": "uuid"
   },
   "holderName": {
    "type": "string"
   },
   "zones": {
    "type": "array",
    "items": {
     "type": "string"
    },
    "description": "Where this badge admits, which is the whole point of it."
   },
   "state": {
    "type": "string",
    "enum": [
     "issued",
     "collected",
     "suspended",
     "revoked",
     "expired"
    ]
   },
   "issuedAt": {
    "type": "string",
    "format": "date-time"
   },
   "expiresAt": {
    "type": "string",
    "format": "date-time"
   },
   "revokedReason": {
    "type": "string"
   }
  }
 }
}
```
