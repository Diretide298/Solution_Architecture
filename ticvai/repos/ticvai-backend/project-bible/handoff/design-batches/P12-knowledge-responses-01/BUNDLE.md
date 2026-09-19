# P12-knowledge-responses-01 — P12 · Knowledge & Responses

**2 screens · 4 operations · 7 schemas · 4 permissions**

Platform P12 Venue Support · ships as **venue-management** ·
staff audience · web ·
online only

## Who this is for

**staff on web.** Everything below is how you know what is
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

- **Every control that can be refused must be gated.** 4 permissions apply here:
  `AI_CONFIGURE, MARKETING_MANAGE, MARKETING_VIEW, TENANT_CONFIGURE`. A control nobody can use must say so,
  not sit enabled and fail.
- **1 of these operations work offline**: listFaqs
  — and the rest do not. A surface that looks the same online and off is lying.
- **Do not invent an operation.** If a screen needs something `operations.json` does not have, that
  is a finding worth reporting, not a gap to fill with a plausible endpoint.
- **`entryState.params` is what the screen must be given.** A screen that renders without them is
  the empty-state bug, not the happy path.

## The screens

| id | name | pattern | ops | overlays | machine |
|---|---|---|---|---|---|
| `SUP-006` | Knowledge Base Search | listDetail | 2 | 0 | — |
| `SUP-007` | Canned Response Management | listDetail | 2 | 0 | — |

## Thin screens in this batch

**SUP-006, SUP-007 declare fewer than four components.** There is not enough here to build them faithfully. Build what is declared and say what is missing — **an invented screen comes back looking finished**, which is worse than an honest gap.

---

## `screens.json`

Every field of every screen in this batch. **`machine` is what a screen is in the middle of**, `overlays` is what opens over it and what closing it does, and `navigation.transitions` is how you leave, with `carries` naming the state that travels.

```json
[
 {
  "id": "SUP-006",
  "name": "Knowledge Base Search",
  "module": "Knowledge & Responses",
  "requiresModule": "core",
  "wave": 3,
  "capability": "C105",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/knowledge-base-search",
   "component": "apps/venue-support-web/src/routes/general/KnowledgeBaseSearchList.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "exitTo": [
    "SUP-001",
    "SUP-002",
    "SUP-003",
    "SUP-005"
   ],
   "inferred": true,
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId, so an edge into it must carry them"
    },
    {
     "to": "SUP-005",
     "trigger": "Live Chat Workspace",
     "carries": [
      "caseId",
      "conversationId"
     ],
     "provenance": "derived — SUP-005 declares entryState.params caseId, conversationId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement. **41 operations removed 24 August.** Every white-label screen across P09, P12 and P13 declared the **identical 41 operations** — a Typography screen that could create banners and a Component Preview that could set FAQs. **The worst instance of the 18 August bulk attach found so far**, and only walking the white-label journey surfaced it.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listKnowledgeCollections` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find something when the guest does not know what it is called.",
  "gaps": [
   {
    "operation": "listFaqs",
    "why": "**1 declared operation reach no component on this screen**: listFaqs. Either the screen is missing what calls them, or the declaration is residue.",
    "source": "the screen's own declarations"
   }
  ],
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every knowledge base search",
       "bindsTo": "KnowledgeCollection",
       "columns": [
        "KnowledgeCollection.id",
        "KnowledgeCollection.name",
        "KnowledgeCollection.description",
        "KnowledgeCollection.scopeLevel",
        "KnowledgeCollection.scopePath",
        "KnowledgeCollection.documentCount",
        "KnowledgeCollection.shardKey",
        "KnowledgeCollection.retrieval",
        "KnowledgeCollection.sparseModel",
        "KnowledgeCollection.idfScope",
        "KnowledgeCollection.embeddingModel",
        "KnowledgeCollection.isActive"
       ],
       "operation": "listKnowledgeCollections",
       "provenance": "contract ai.yaml GET /collections"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected knowledge base search",
       "bindsTo": "KnowledgeCollection",
       "columns": [
        "KnowledgeCollection.id",
        "KnowledgeCollection.name",
        "KnowledgeCollection.description",
        "KnowledgeCollection.scopeLevel",
        "KnowledgeCollection.scopePath",
        "KnowledgeCollection.documentCount",
        "KnowledgeCollection.shardKey",
        "KnowledgeCollection.retrieval",
        "KnowledgeCollection.sparseModel",
        "KnowledgeCollection.idfScope",
        "KnowledgeCollection.embeddingModel",
        "KnowledgeCollection.isActive"
       ],
       "operation": "listKnowledgeCollections",
       "provenance": "contract ai.yaml GET /collections"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The knowledge base search list.",
   "error": "Could not load. Names which read failed and leaves the knowledge base search untouched.",
   "emptyFirstRun": "No knowledge base search yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the knowledge base search are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listKnowledgeCollections",
    "contract": "ai",
    "purpose": "Collections an agent may search",
    "trigger": "onLoad"
   },
   {
    "operationId": "listFaqs",
    "contract": "white-label",
    "purpose": "Published answers, as the guest sees them",
    "trigger": "onLoad"
   }
  ],
  "entryState": {
   "params": [
    {
     "name": "bannerId",
     "from": "deepLink"
    },
    {
     "name": "pageId",
     "from": "deepLink"
    },
    {
     "name": "policyKind",
     "from": "deepLink"
    },
    {
     "name": "version",
     "from": "deepLink"
    }
   ],
   "coldEntry": "**A version link is expected to point at something superseded — that is what versions are for.** The screen opens the requested version read-only, says it is not current, and links to the one that is. **An old version is history, not an error.** Arrives with `bannerId`, `pageId`, `policyKind`.",
   "preloaded": [
    "KnowledgeCollection.id",
    "KnowledgeCollection.name",
    "KnowledgeCollection.description",
    "KnowledgeCollection.scopeLevel",
    "KnowledgeCollection.scopePath"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-006"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
    "decided": "10 September 2026"
   }
  }
 },
 {
  "id": "SUP-007",
  "name": "Canned Response Management",
  "module": "Knowledge & Responses",
  "requiresModule": "marketing",
  "wave": 3,
  "capability": "C60",
  "implementation": {
   "app": "venue-support-web",
   "route": "/general/canned-response-management",
   "component": "apps/venue-support-web/src/routes/general/CannedResponseManagementForm.tsx",
   "status": "notStarted"
  },
  "navigation": {
   "entryFrom": [
    "SUP-001"
   ],
   "inferred": true,
   "exitTo": [
    "SUP-001",
    "SUP-002",
    "SUP-003"
   ],
   "transitions": [
    {
     "to": "SUP-001",
     "trigger": "Agent Login",
     "carries": [
      "sessionId"
     ],
     "provenance": "derived — SUP-001 declares entryState.params sessionId, so an edge into it must carry them"
    },
    {
     "to": "SUP-002",
     "trigger": "Agent Dashboard",
     "carries": [
      "caseId"
     ],
     "provenance": "derived — SUP-002 declares entryState.params caseId, so an edge into it must carry them"
    }
   ]
  },
  "notes": "States derived from the screen pattern on 17 August, not individually considered — sound for a list, a form or a money screen, and worth revisiting where this screen is unusual. Purpose derived from the screen name and its operations on 17 August, not from a requirement.",
  "density": "compact",
  "pattern": "listDetail",
  "patternReason": "`listMessageTemplates` reads a population and nothing reads one of them; the detail is the row until a `get` exists",
  "purpose": "Find canned response management for this venue.",
  "layout": {
   "template": "split",
   "regions": [
    {
     "name": "contentBody",
     "slot": "collection",
     "components": [
      {
       "kind": "dataTable",
       "label": "Every canned response",
       "bindsTo": "MessageTemplate",
       "columns": [
        "MessageTemplate.id",
        "MessageTemplate.code",
        "MessageTemplate.name",
        "MessageTemplate.channel",
        "MessageTemplate.subjects",
        "MessageTemplate.bodies",
        "MessageTemplate.mergeFields",
        "MessageTemplate.missingLanguages",
        "MessageTemplate.providerTemplateId"
       ],
       "operation": "listMessageTemplates",
       "provenance": "contract marketing-crm.yaml GET /message-templates"
      }
     ]
    },
    {
     "name": "contextPanel",
     "slot": "selection",
     "components": [
      {
       "kind": "detailPanel",
       "label": "The selected canned response",
       "bindsTo": "MessageTemplate",
       "columns": [
        "MessageTemplate.id",
        "MessageTemplate.code",
        "MessageTemplate.name",
        "MessageTemplate.channel",
        "MessageTemplate.subjects",
        "MessageTemplate.bodies",
        "MessageTemplate.mergeFields",
        "MessageTemplate.missingLanguages",
        "MessageTemplate.providerTemplateId"
       ],
       "operation": "listMessageTemplates",
       "provenance": "contract marketing-crm.yaml GET /message-templates"
      }
     ]
    },
    {
     "name": "actionBar",
     "slot": "rowActions",
     "components": [
      {
       "kind": "primaryButton",
       "label": "Create",
       "operation": "createMessageTemplate",
       "provenance": "contract marketing-crm.yaml POST /message-templates"
      }
     ]
    }
   ]
  },
  "states": {
   "loading": "The canned response list.",
   "error": "Could not load. Names which read failed and leaves the canned response untouched.",
   "emptyFirstRun": "No canned response yet. Carries the create action; distinct from a filter that matched nothing.",
   "emptyNoResults": "The filter narrowed it and the canned response are still there. Names the active filter and offers to clear it.",
   "emptyNoAccess": "Names the missing permission. **Never an empty table** — that reads as *there is no data* and sends somebody to support with the wrong question."
  },
  "apis": [
   {
    "operationId": "listMessageTemplates",
    "contract": "marketing-crm",
    "purpose": "from page inventory",
    "trigger": "onLoad"
   },
   {
    "operationId": "createMessageTemplate",
    "contract": "marketing-crm",
    "purpose": "Create a message template",
    "trigger": "onAction",
    "invalidates": [
     "listMessageTemplates"
    ]
   }
  ],
  "entryState": {
   "preloaded": [
    "MessageTemplate.id",
    "MessageTemplate.code",
    "MessageTemplate.name",
    "MessageTemplate.channel",
    "MessageTemplate.subjects"
   ]
  },
  "wireframe": {
   "status": "notStarted",
   "provenance": "generated",
   "board": "wireframes/P12 Venue Support.dc.html#sup-007"
  },
  "apisNote": "Rebuilt 9 September 2026 from the 2 operations this screen declares, not from a workshop pack — it has none. Columns are every field the response schema declares, plumbing aside — narrowing them to the ones that matter is work a person still owes this screen.",
  "_platform": {
   "code": "P12",
   "audience": "staff",
   "formFactor": "web",
   "shortName": "Venue Support",
   "name": "Venue Support — Agent Console",
   "offlineCapable": false,
   "app": "venue-support-web",
   "operator": "venue",
   "targetApp": {
    "app": "venue-management",
    "name": "TICVAI Venue Management",
    "shell": "web",
    "siblings": [
     "P08",
     "P13",
     "P16"
    ],
    "note": "**Already one app in all but name** — P08, P13 and P16 declared the same `app` before this decision. One tenant-level surface that filters across venues, with analytics, CMS and the support desk as sections of it.",
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
 "createMessageTemplate": {
  "method": "POST",
  "path": "/message-templates",
  "contract": "marketing-crm",
  "summary": "Create a message template",
  "permission": "MARKETING_MANAGE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": "MessageTemplate",
  "responds": "MessageTemplate"
 },
 "listFaqs": {
  "method": "GET",
  "path": "/tenant-config/faqs",
  "contract": "white-label",
  "summary": "List FAQs",
  "permission": "TENANT_CONFIGURE",
  "offlineCapable": true,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "FaqCategory"
 },
 "listKnowledgeCollections": {
  "method": "GET",
  "path": "/collections",
  "contract": "ai",
  "summary": "Collections available to this tenant",
  "permission": "AI_CONFIGURE",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "tenant",
  "parameters": [],
  "requestBody": null,
  "responds": "KnowledgeCollection"
 },
 "listMessageTemplates": {
  "method": "GET",
  "path": "/message-templates",
  "contract": "marketing-crm",
  "summary": "List message templates",
  "permission": "MARKETING_VIEW",
  "offlineCapable": false,
  "conflictPolicy": "serverWins",
  "scopeLevel": "venue",
  "parameters": [
   {
    "name": "channel",
    "in": "query",
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   },
   {
    "name": null,
    "in": null,
    "required": null
   }
  ],
  "requestBody": null,
  "responds": "Page"
 }
}
```

## `schemas.json`

The data those operations carry, resolved one level deep. **Seed from these.** The reference prototype hardcodes 57 models and every one corresponds to a schema here; a build that invents its own will disagree with the backend on day one.

```json
{
 "FaqCategory": {
  "x-ticvai-persistence": "whitelabel.faq_category + whitelabel.faq_entry",
  "type": "object",
  "required": [
   "code",
   "name",
   "entries"
  ],
  "properties": {
   "code": {
    "type": "string"
   },
   "name": {
    "$ref": "#/components/schemas/LocalisedText"
   },
   "sortOrder": {
    "type": "integer"
   },
   "entries": {
    "type": "array",
    "items": {
     "type": "object",
     "required": [
      "id",
      "question",
      "answer"
     ],
     "properties": {
      "id": {
       "type": "string",
       "format": "uuid"
      },
      "question": {
       "$ref": "#/components/schemas/LocalisedText"
      },
      "answer": {
       "$ref": "#/components/schemas/LocalisedRichText"
      },
      "sortOrder": {
       "type": "integer"
      },
      "isPublished": {
       "type": "boolean"
      }
     }
    }
   },
   "scopePath": {
    "type": "string",
    "description": "**The partition key** (ADR-0005). Added 31 August: the operations that write this table declare a scope and the table carried no column for it — **49 tables were in that state**, so a row could be written at venue scope and then read by anything that could reach the table.\n\n**`scope_path` rather than a specific id** because it is prefix-comparable: `uae.dubai` contains `uae.dubai.marina`, and one index answers every level of the walk.\n\n**Operations write it at `tenant` scope.**"
   }
  }
 },
 "KnowledgeCollection": {
  "type": "object",
  "x-ticvai-persistence": "ai.knowledge_collection",
  "required": [
   "name",
   "scopeLevel"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid",
    "readOnly": true
   },
   "name": {
    "type": "string"
   },
   "description": {
    "type": "string"
   },
   "scopeLevel": {
    "type": "string",
    "enum": [
     "tenant",
     "region",
     "venue"
    ]
   },
   "scopePath": {
    "type": "string",
    "readOnly": true
   },
   "documentCount": {
    "type": "integer",
    "readOnly": true
   },
   "shardKey": {
    "type": "string",
    "readOnly": true,
    "description": "**The tenant boundary on shared placement** (ADR-0021). A collection is shared by every tenant using the same embedding model, and the shard separates them — set at provisioning from the tenant, never from a request.\nOn dedicated placement there is one shard and this is still populated, because a tenant moving from shared to dedicated moves a shard rather than being re-indexed.\n"
   },
   "retrieval": {
    "type": "string",
    "enum": [
     "dense",
     "hybrid"
    ],
    "default": "hybrid",
    "description": "**Set at creation and not changeable.** A collection created dense-only cannot gain a sparse index without a full rebuild, which is why this is a creation decision rather than a query one.\nHybrid is the default because **a venue corpus is mostly proper nouns** — Yas Waterworld, Bronze Annual Pass, a menu item name. Dense retrieval is good at meaning and poor at exact tokens, and half our queries are exact tokens.\n"
   },
   "sparseModel": {
    "type": "string",
    "nullable": true,
    "description": "The sparse signal, where `retrieval` is `hybrid`. BM25 unless a tenant needs otherwise."
   },
   "idfScope": {
    "type": "string",
    "enum": [
     "shard",
     "tenant",
     "venue"
    ],
    "default": "tenant",
    "description": "**Which population the sparse score measures rarity against** (ADR-0021). Qdrant computes IDF statistics shard-wide by default, so a term common at one venue and rare at another gets one score for both. Shard-per-tenant fixes the cross-tenant case; **inside a dedicated cell the shard is the whole tenant and venues share it**, which is what this narrows.\n"
   },
   "embeddingModel": {
    "type": "string",
    "readOnly": true,
    "description": "**This is what decides how many collections exist** (ADR-0021). A collection carries its own vector configuration and a shard cannot, so vectors from two models cannot share one. A tenant that residency forces onto a local model therefore has its own collection — forced by the model, not chosen for isolation.\nRead-only because **changing it invalidates every embedding in the collection**, and a collection silently searched with mismatched vectors returns plausible nonsense.\n"
   },
   "isActive": {
    "type": "boolean"
   }
  }
 },
 "LocalisedRichText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "description": "Keyed by language code. Values are sanitised HTML.",
  "additionalProperties": {
   "type": "string"
  }
 },
 "LocalisedText": {
  "x-ticvai-persistence": "none — jsonb column",
  "type": "object",
  "additionalProperties": {
   "type": "string"
  }
 },
 "MessageChannel": {
  "type": "string",
  "enum": [
   "email",
   "sms",
   "whatsapp",
   "push",
   "inApp",
   "post"
  ]
 },
 "MessageTemplate": {
  "x-ticvai-persistence": "marketing.message_template",
  "type": "object",
  "required": [
   "id",
   "code",
   "name",
   "channel",
   "bodies"
  ],
  "properties": {
   "id": {
    "type": "string",
    "format": "uuid"
   },
   "code": {
    "type": "string",
    "maxLength": 64
   },
   "name": {
    "type": "string",
    "maxLength": 200
   },
   "channel": {
    "$ref": "#/components/schemas/MessageChannel"
   },
   "subjects": {
    "type": "object",
    "description": "Per language. Email only.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "bodies": {
    "type": "object",
    "description": "Per language, keyed by ISO 639-1 code.",
    "additionalProperties": {
     "type": "string"
    }
   },
   "mergeFields": {
    "type": "array",
    "items": {
     "type": "string"
    }
   },
   "missingLanguages": {
    "type": "array",
    "readOnly": true,
    "description": "Enabled languages without a body. Flagged rather than silently falling back — a guest receiving English when they chose Arabic is a defect.\n",
    "items": {
     "type": "string"
    }
   },
   "providerTemplateId": {
    "type": "string",
    "nullable": true,
    "description": "Required for WhatsApp, where templates are pre-approved by the provider."
   }
  }
 },
 "Page": {
  "type": "object",
  "required": [
   "items",
   "hasMore"
  ],
  "properties": {
   "items": {
    "type": "array",
    "items": {}
   },
   "nextCursor": {
    "type": "string"
   },
   "hasMore": {
    "type": "boolean"
   }
  }
 }
}
```
