#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The workforce integration layer Board 3 requires and neither workbook has.

**Decision 6 declined their seven payroll tables and took their seven HR tables as an externally
mastered projection.** That was answered on the client's own sources — `Resource_Management_
Configuration_Reference.pdf` Board 3 page 45, *"connect TICVAI Resource Management with EXTERNAL
HR, workforce management, payroll, identity and employee systems"* — and the same page asks for
something neither side built.

    Ownership Rules     "For every field, administrators shall determine ... External System
                        Master ... This prevents conflicting updates."
    Integration Sources HRMS, Workforce Management, Payroll, Time & Attendance, Identity
                        Management, external staffing agencies
    Support             API, webhooks, scheduled synchronisation, manual synchronisation, file
                        import
    Display (Board 10)  connected systems, last synchronisation, successful records, failed
                        records, warnings, mapping errors, authentication status
    Conflict Handling   "Employee exists in HR but not TICVAI." "Employee venue changed
                        externally." "Certification expired." "Employee terminated externally
                        but has future TICVAI assignments." — and the system shall flag affected
                        downstream assignments

**Taking their employee tables without this takes the data and leaves the governance.** An
employee record that is mastered elsewhere, with no statement of which fields are theirs and no
record of a failed sync, is a table that will silently disagree with the system of record and
have no way to say so.

Four tables, no operations. Wiring them is the same separate phase as the other 81.

    python3 tools/applied/workforce-integration-layer-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = os.path.join(ROOT, "contracts", "satellite", "workforce.yaml")

BLOCK = '''    WorkforceIntegrationSource:
      type: object
      x-ticvai-persistence: workforce.integration_source
      description: >
        **An external system that masters some of our workforce data.** Board 3 names HRMS,
        Workforce Management, Payroll, Time & Attendance, Identity Management and external
        staffing agencies. The six-state display Board 10 asks for lives on this row: what is
        connected, when it last synchronised, and whether its credentials still work.
      required:
      - code
      - name
      - kind
      - transport
      - status
      properties:
        id:
          type: string
          format: uuid
        code:
          type: string
          maxLength: 60
        name:
          type: string
          maxLength: 150
        kind:
          type: string
          enum: [hrms, workforceManagement, payroll, timeAndAttendance, identity, staffingAgency]
        transport:
          type: string
          enum: [api, webhook, scheduled, manual, fileImport]
          description: >
            Board 3, Support. **`manual` and `fileImport` are in the list on purpose** — a
            staffing agency that sends a spreadsheet is still a system of record, and modelling
            only the API cases would leave the messiest source unmanaged.
        authenticationStatus:
          type: string
          enum: [healthy, expiring, expired, failed, notConfigured]
        lastSynchronisedAt:
          type: string
          format: date-time
          nullable: true
        status:
          type: string
          enum: [active, degraded, suspended]
        scopePath:
          type: string
          nullable: true
    WorkforceFieldOwnership:
      type: object
      x-ticvai-persistence: workforce.field_ownership
      description: >
        **Which system owns a field, which is what prevents conflicting updates.** Board 3:
        *"For every field, administrators shall determine ... External System Master."* Without
        this, an employee record mastered in HRMS and edited here disagrees with its source and
        nothing can say which answer is right.

        One row per table and column. Absent means ours, so nothing has to be enumerated before
        it is decided.
      required:
      - tableName
      - columnName
      - master
      properties:
        id:
          type: string
          format: uuid
        tableName:
          type: string
          maxLength: 120
        columnName:
          type: string
          maxLength: 120
        master:
          type: string
          enum: [ticvai, external]
        sourceId:
          type: string
          format: uuid
          nullable: true
          description: The integration source that masters it, when `master` is `external`.
        onConflict:
          type: string
          enum: [externalWins, ticvaiWins, flagForReview]
        scopePath:
          type: string
          nullable: true
    WorkforceSyncRun:
      type: object
      x-ticvai-persistence: workforce.sync_run
      description: >
        **One synchronisation, and what it did.** Board 10 asks the page to show successful
        records, failed records, warnings and mapping errors rather than *"integration failed"* —
        and to say the operational consequence: *"12 employee availability updates could not be
        synchronised. Four employees have assignments within the next 24 hours."* That sentence
        needs counts on a row, not a log line.
      required:
      - sourceId
      - startedAt
      - status
      properties:
        id:
          type: string
          format: uuid
        sourceId:
          type: string
          format: uuid
        startedAt:
          type: string
          format: date-time
        finishedAt:
          type: string
          format: date-time
          nullable: true
        status:
          type: string
          enum: [running, succeeded, partial, failed]
        recordsRead:
          type: integer
        recordsApplied:
          type: integer
        recordsFailed:
          type: integer
        warningCount:
          type: integer
        mappingErrorCount:
          type: integer
        trigger:
          type: string
          enum: [scheduled, manual, webhook, fileImport]
        scopePath:
          type: string
          nullable: true
    WorkforceSyncConflict:
      type: object
      x-ticvai-persistence: workforce.sync_conflict
      description: >
        **A disagreement a person has to settle, and the assignments it puts at risk.** Board 3
        lists the cases by name: an employee in HR and not here, a venue changed externally, a
        certification expired, and *"employee terminated externally but has future TICVAI
        assignments"* — where *"the system shall flag affected downstream assignments"*.

        `affectedAssignmentIds` is deliberately an array and deliberately an exception: it is a
        snapshot of what was at risk when the conflict was raised, not a live relationship, and
        it must not change when a roster does.
      required:
      - sourceId
      - kind
      - status
      - raisedAt
      properties:
        id:
          type: string
          format: uuid
        sourceId:
          type: string
          format: uuid
        syncRunId:
          type: string
          format: uuid
          nullable: true
        kind:
          type: string
          enum:
          - missingInTicvai
          - missingExternally
          - venueChangedExternally
          - certificationExpired
          - terminatedExternally
          - fieldDisagreement
        employeeId:
          type: string
          format: uuid
          nullable: true
        externalReference:
          type: string
          maxLength: 200
          nullable: true
        detail:
          type: string
          maxLength: 1000
          nullable: true
        affectedAssignmentIds:
          type: array
          items:
            type: string
            format: uuid
        status:
          type: string
          enum: [open, retried, reprocessed, escalated, resolved, ignored]
        raisedAt:
          type: string
          format: date-time
        resolvedAt:
          type: string
          format: date-time
          nullable: true
        resolvedByPrincipalId:
          type: string
          format: uuid
          nullable: true
        scopePath:
          type: string
          nullable: true
'''


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(TARGET, encoding="utf-8").read()
    if "workforce.integration_source" in s:
        print("  already present — nothing to do")
        return 0
    m = re.search(r"^  schemas:\n", s, re.M)
    if not m:
        print("  !! no components.schemas block in workforce.yaml")
        return 1
    out = s[:m.end()] + BLOCK + s[m.end():]
    try:
        doc = yaml.safe_load(out)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:160])
        return 1
    added = [k for k in (doc.get("components", {}).get("schemas") or {})
             if k.startswith("Workforce") and k in BLOCK]
    print("  4 schema(s) to add, file parses:")
    for t in ("workforce.integration_source", "workforce.field_ownership",
              "workforce.sync_run", "workforce.sync_conflict"):
        print("      %s" % t)
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TARGET, "w", encoding="utf-8", newline="\n").write(out)
    print("  -> contracts/satellite/workforce.yaml")
    print("\n  No operation was added, so no screen was either. Run tools/refresh.sh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
