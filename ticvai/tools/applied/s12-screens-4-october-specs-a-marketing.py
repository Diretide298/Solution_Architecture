# Marketing and customer service screens (part of s12-screens-4-october-specs.py; helpers there).
# flake8: noqa

F("BO-785", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="A library of message templates with the selected one edited beside it (defined 4 "
                "October 2026 from MessageTemplate and the design notes, CHG-FXS-001).",
  apis_add=[A("updateMessageTemplate", "onAction",
              "Save an edit to a venue template, or apply reviewed translation drafts to it: " + AGREED,
              contract="marketing-crm"),
            A("getTranslationProposals", "onInterval",
              "The drafts of a translation job started here, polled every 3 s until it completes")],
  regions=[
      ("contentBody", [
          c("selectField", "Channel", "MessageTemplate.channel", "listMessageTemplates",
            notes="Filters the list (query `channel`); All by default."),
          c("dataTable", "Templates", "MessageTemplate", "listMessageTemplates",
            cols("MessageTemplate", "code", "name", "channel", "ownership", "missingLanguages"),
            notes="Each row shows a warning chip listing enabled languages with no body. Platform "
                  "templates (ownership platform) are listed read-only beside the venue's own."),
          c("primaryButton", "New template", notes="Opens an empty form in the side panel."),
      ]),
      ("contextPanel", [
          c("textField", "Code", "MessageTemplate.code", "createMessageTemplate",
            notes="Set at creation; read-only afterwards."),
          c("textField", "Name", "MessageTemplate.name", "createMessageTemplate"),
          c("selectField", "Template channel", "MessageTemplate.channel", "createMessageTemplate",
            notes="Email, SMS, WhatsApp, push, in-app. Set at creation."),
          c("textField", "Subject per language", "MessageTemplate.subjects", "createMessageTemplate",
            notes="Email only. English and Arabic side by side; Arabic right to left."),
          c("textField", "Body per language", "MessageTemplate.bodies", "createMessageTemplate",
            notes="English and Arabic side by side; Arabic right to left. Merge fields inserted from "
                  "the picker, never typed."),
          c("multiSelect", "Merge fields", "MessageTemplate.mergeFields", "createMessageTemplate"),
          c("textField", "Provider template id", "MessageTemplate.providerTemplateId",
            "createMessageTemplate", notes="Shown only for WhatsApp, where the provider pre-approves "
                                           "the template."),
          c("primaryButton", "Create template", op="createMessageTemplate"),
          c("primaryButton", "Save changes", op="updateMessageTemplate",
            notes="Venue templates only; a platform template has no Save. Sends the same fields as "
                  "create except code and channel."),
          c("secondaryButton", "Draft with AI", op="proposeMarketingContent",
            notes="Drafts a subject and body from a brief into the form; nothing is saved until the "
                  "author saves."),
          c("secondaryButton", "Translate missing languages", op="proposeTranslations",
            notes="scope messageTemplates; protected terms come from the glossary. Starts a job whose "
                  "translationJobId the screen keeps for getTranslationProposals."),
          c("dataTable", "Translation drafts", "TranslationProposals.drafts", "getTranslationProposals",
            notes="Each draft is reviewed and applied to the template with Save changes."),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No templates yet. Carries New template.",
              emptyNoResults="No template on this channel. Names the channel and offers All."),
  note="Defined 4 October 2026 from MessageTemplate and the customer-marketing design notes (BO-785): "
       "list, create and edit a template, draft with AI and translate. Editing needs "
       "updateMessageTemplate (agreed in the ledger; correction CHG-SBO-005 asked for it). Version, "
       "approval, clone and archive stay out until the contract has them")

F("BO-798", DEF, pattern="configEditor", template="split", drop_gaps=("person",),
  patternReason="The copilot's knowledge settings edited in one form beside the collections it "
                "answers from and the questions it could not answer (defined 4 October 2026, "
                "CHG-FXS-001).",
  set=dict(purpose="Manage what the customer-service assistant may use: the data sources and "
                   "knowledge collections it answers from, the documents in them, its tone and "
                   "channels, and the questions it could not answer, each a task for the content "
                   "owner."),
  apis_add=[A("createUpload", "onAction", "Upload a knowledge document's file before it is ingested"),
            A("completeUpload", "background", "Finish the upload once the file PUT succeeds (no tap "
                                              "of its own); the asset id is the document's sourceAssetId")],
  regions=[
      ("contentBody", [
          c("toggle", "Assistant on", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.isEnabled",
            "setCustomerServiceCopilot"),
          c("selectField", "Applies to", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.scopeLevel",
            "setCustomerServiceCopilot"),
          c("multiSelect", "Data sources", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.dataSources",
            "setCustomerServiceCopilot"),
          c("multiSelect", "Knowledge collections",
            "AiCustomerServiceCopilotKnowledgeWorkspaceInput.knowledgeCollectionIds",
            "setCustomerServiceCopilot", notes="Options from listKnowledgeCollections."),
          c("multiSelect", "Draft replies on", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.draftChannels",
            "setCustomerServiceCopilot"),
          c("multiSelect", "Send without review on", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.autoSend",
            "setCustomerServiceCopilot"),
          c("textField", "Brand tone", "AiCustomerServiceCopilotKnowledgeWorkspaceInput.brandTone",
            "setCustomerServiceCopilot"),
          c("toggle", "Reply in the guest's language",
            "AiCustomerServiceCopilotKnowledgeWorkspaceInput.replyInCustomerLanguage",
            "setCustomerServiceCopilot"),
          c("detailPanel", "In effect", "AiCustomerServiceCopilotKnowledgeWorkspaceView.effective",
            "getCustomerServiceCopilot", notes="What applies after tenant and venue settings combine; "
                                               "the form loads from `configuration`."),
          c("primaryButton", "Save", op="setCustomerServiceCopilot"),
          c("secondaryButton", "Cancel", notes="Discards unsaved edits; nothing is sent."),
      ]),
      ("contextPanel", [
          c("dataTable", "Knowledge sources", "KnowledgeCollection", "listKnowledgeCollections",
            cols("KnowledgeCollection", "name", "scopeLevel", "documentCount", "isActive")),
          c("fileUpload", "Add document", "KnowledgeDocument.sourceAssetId", "createUpload",
            notes="PDF, DOCX, HTML or TXT up to 20 MB (flow-brief default). createUpload, the file "
                  "PUT, completeUpload, then ingestKnowledgeDocument into the selected collection; the "
                  "row shows processing until indexed."),
          c("textField", "Document title", "KnowledgeDocument.title", "ingestKnowledgeDocument"),
          c("secondaryButton", "Add to collection", op="ingestKnowledgeDocument",
            notes="Ingests the uploaded asset into the selected collection."),
          c("dataTable", "Questions it could not answer", "AiKnowledgeGap", "listKnowledgeGaps",
            cols("AiKnowledgeGap", "question", "occurrences", "audience", "status", "lastAskedAt"),
            notes="Grouped and counted, newest first; each is a task for the content owner."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="No collections yet: the assistant answers nothing until one "
                                         "is added. Carries Add document."),
  note="Defined 4 October 2026 from the copilot's knowledge workspace, KnowledgeCollection, "
       "KnowledgeDocument and AiKnowledgeGap. Intents, phrases, entities and synonyms are not part of "
       "the retrieval design (the assistant answers from collections, ADR-0049) and left the purpose; "
       "an intent model is a later change request")

F("BO-799", DEF, pattern="listDetail", template="split", drop_gaps=("person",),
  patternReason="The agent's queue with the open conversation, its transcript and the guest beside "
                "it (defined 4 October 2026, CHG-FXS-001).",
  apis_add=[A("listConversations", "onInterval",
              "The agent's queue: waiting and assigned-to-me conversations, refreshed every 5 s"),
            A("getConversation", "onInterval",
              "The open conversation and its transcript, polled every 5 s while open"),
            A("getGuestProfile", "onLoad", "The guest beside the conversation (subjectId)")],
  entry=[P("conversationId", "navigation", True,
           "Opened without it, the screen shows the queue and the agent picks one (CHG-FXS-001)."),
         P("subjectId", "navigation", True,
           "The open conversation's subjectId (Conversation.subjectId); none for an anonymous guest.")],
  regions=[
      ("contentBody", [
          c("selectField", "Show", "Conversation.state", "listConversations",
            notes="Waiting for an agent / Assigned to me (`assignedToMe`)."),
          c("dataTable", "Queue", "Conversation", "listConversations",
            cols("Conversation", "channel", "state", "handoverReason", "sentiment", "estimatedWaitSeconds")),
      ]),
      ("contextPanel", [
          c("cardList", "Transcript", "Conversation.messages", "getConversation",
            cols("ConversationMessage", "sender", "body", "attachments", "sentAt"),
            notes="Oldest first; internal notes are visibly different and never reach the guest."),
          c("detailPanel", "Handover", "Conversation", "getConversation",
            cols("Conversation", "handoverReason", "handoverSummary", "intent", "locale")),
          c("secondaryButton", "Claim conversation", op="claimConversation",
            notes="Shown while the conversation is waiting; takes it from the bot."),
          c("textField", "Reply", "ConversationMessage.body", "sendConversationMessage"),
          c("primaryButton", "Send", op="sendConversationMessage",
            notes="Sent as the agent; the sender is resolved from the session."),
          c("selectField", "Outcome", "CallDisposition.outcome", "setCallDisposition"),
          c("datePicker", "Callback at", "CallDisposition.callbackAt", "setCallDisposition",
            notes="Required when the outcome is callbackScheduled."),
          c("textField", "Note", "CallDisposition.note", "setCallDisposition"),
          c("secondaryButton", "End conversation", op="setCallDisposition"),
          c("secondaryButton", "Assist at kiosk", op="startKioskAssist",
            notes="Only when the conversation came from a kiosk; deviceId is the kiosk's."),
          c("detailPanel", "Guest", "GuestProfileDetail", "getGuestProfile",
            notes="Name, contact, tier and recent orders as the profile returns them; nothing when "
                  "the guest is anonymous (no subjectId)."),
      ]),
  ],
  states=dict(LIST_STATES, emptyFirstRun="Nobody is waiting. The queue refreshes by itself.",
              emptyNoResults="Nothing assigned to you. Offers the waiting queue."),
  note="Defined 4 October 2026 from Conversation, ConversationMessage, CallDisposition and the "
       "customer-marketing design notes (BO-799): the queue (listConversations), the transcript "
       "(getConversation) and the guest (getGuestProfile) are bound reads; AI reply suggestions and "
       "canned responses wait for their operations")
