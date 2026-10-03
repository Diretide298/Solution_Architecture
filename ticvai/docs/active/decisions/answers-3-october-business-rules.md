# Chinmay's Block A business rules (3 October 2026)

> **The cited copy (3 October 2026, CHG-RUL-001).** The sections "Block A audit business rules" and the list
> "Asked as questions instead of defaults" of Chinmay's answers log of 3 October (the lead's working log of batch 1 onward),
> copied into git so the CHG-RUL entries and `tools/check-business-rules.py` can cite them (`ticvai/CLAUDE.md`
> rule 12). Verbatim. The rules answer pattern 4 of the r2 Block A audit (CHG-AUD-001: contract rules that
> disagree with their screens). Applied to the contracts by CHG-RUL-001 to CHG-RUL-016.

## Block A audit business rules (Chinmay, 3 Oct)
- F&B bill split: all five methods (amount, covers, category, item, seat), one SplitBill request with a method field; an unsplit bill closes as one sub-bill (subBillId optional). Payment timing follows POS-021: pay first or send first, both configurations.
- AI concierge / chat: stream answers (server-sent events for sendAiMessage: tokens, then sources and any proposed action); the full message is stored.
- Visit planner: a signed-out guest can build and change a plan in an anonymous session; sign in to save, share or book; the plan moves to the account on sign-in.
- Purchase orders: blanket and RFQ-award orders may be raised without a requisition but go through the PO approval matrix; normal orders still need an approved requisition.
- Payment links: a second create returns the existing live link (idempotent); a paid order is refused with 409; a new link only after the old one expires or is cancelled.
- Report runs: REPORT_VIEW_VENUE sees every run in the venue scope; "mine only" is a filter; REPORT_MANAGE adds editing and scheduling.
- Attendance: self clock-in only (NOT the recommendation); supervisors correct afterwards with amendAttendance. BO-056's "Record attendance" is removed or becomes "Amend attendance".
- Kitchen guest board KIT-007: read-only, order numbers (preparing / ready) in server order, no buttons; handover stays on KIT-006.
- Asked as questions instead of defaults (Chinmay, 3 Oct, all as recommended unless marked):
  - Theme contrast: WCAG AA (text 4.5:1, large text 3:1; primary/accent and component colours 3:1).
  - Dashboards: first Save calls createDashboard, later saves updateDashboard; the refresh budget is checked on both.
  - Visit plan add-ons: updateVisitPlan gains addAddOn / removeAddOn change kinds; priced at booking.
  - Requisitions: one approveRequisition call with its decision (approve / reject / return); separate reject/return operations dropped from BO-078.
  - Work orders: cancellable until any labour time or part is recorded; then complete or close with a reason.
  - Incidents: Reported > Investigating > Escalated (optional) > Closed; reopen to Investigating with a reason; every change logged.
  - Fare tables: versioned by effectiveFrom; a future table sits beside the current one; quotes use the one in force at travel time.
  - rejectShiftVariance carries the supervisor step-up in its body, as reopenShift does.
  - POS-000: session management STAYS on the door (NOT the recommendation; reverses CHG-DOOR-003 for this): a supervisor PIN step-up authorises listActiveSessions / forceLogout there, since no one is signed in; BO-053 keeps it too.
  - AI engine tickets: What and done-when filled from docs/architecture/ai-system-design.md and the 2 Oct AI decisions; gaps become questions later.
  - GST-070 reservations: bind the guest's own reservations/waitlist list (self-scoped) and a published list of bookable restaurants.
  - EMP-026 incident form: bind media upload for photos and a 'person involved' entry (name, role, contact, optional guest lookup) stored as PII subjects; consent rules apply.
  - Unsplit bills close as one sub-bill (subBillId optional).
- QR: GST-055's admission QR rotates every 30 seconds (Chinmay's "GST-069" meant GST-055); GST-069 FacePass unchanged.
- AI spend ceiling (BO-091): default currency is the tenant's billing currency (AED for UAE tenants), not USD; tenants can change it.
- Wireframe change list: yes, built with the handoffs, one client sign-off sheet per app (changed frame, what changed, why, decision id).
