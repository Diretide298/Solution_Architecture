# Chinmay's r1 additions (3 October 2026, afternoon)

> **The cited copy (3 October 2026, CHG-RONEC-001).** The section "r1 additions" of Chinmay's answers log of
> 3 October (the lead's working log of batch 1 onward), copied into git so the CHG-RONEC entries can cite it
> (`ticvai/CLAUDE.md` rule 12). Verbatim. "answers L435" in the flow briefs (`handoff/flow-briefs/*.yaml`)
> is the venue-map line below.

## r1 additions (Chinmay, 3 Oct afternoon, all as recommended)
- Block A completes its apps: every operation a Block A screen binds is built in Block A or earlier (a new rule); getUnifiedReconciliation, createPrincipal, requestProductionAccess, closeFiscalPeriod / listFiscalPeriods, report scheduling and the BO-074/BO-075 writes move into Block A; so do getGuestConversation and sendGuestConversationMessage (AI-ENGINE-CONCIERGE) and setAiProvider / setAiCredential (AI-ENGINE-GATEWAY). The residency section on BO-1065 is drawn and built in Block A.
- Venue map in r1: close ADR-0069's open items; the import contract accepts DXF/DWG, PDF with an OCR step, PNG/JPG with hand-marked paths (AI path proposal, accepted segment by segment) and GLB plus a pathway (navigation) file.
- F32 rewritten to the decided shift flow in r1: POS-000 sign-in, blind close, under review over the threshold, next cashier never blocked, supervisor PIN for accept / reject / close / reopen, sessions on POS-000 behind the PIN.
- Supervisor PIN clarified: the four supervisor actions (accept, reject, close, reopen a shift under review) take it; the cashier's own count never does.
- getGuestConversation is bound on WEB-044, GST-031, GST-032 (poll every 5 s, 30 s when hidden). BYOK keys are entered by TICVAI staff under the grant in Block A (no tenant self-service yet).
- Brief defaults (ticketing ~40, AI 14, platform/finance ~50): listed under each flow's `open:` in handoff/flow-briefs/*.yaml with the default used (copy text, timings, limits; e.g. booking hold 8 min with one 8-min extension at 2 min left; kiosk 90 s idle with a 10 s warning; PIN 5 attempts; variance threshold AED 20 pending the client; streamed runs at sentence or 40 tokens). Chinmay to review there.
