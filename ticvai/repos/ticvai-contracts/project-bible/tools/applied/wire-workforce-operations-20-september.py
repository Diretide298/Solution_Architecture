#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nineteen operations for the eleven workforce tables nothing could reach.

**`workforce.yaml` had 24 operations and eleven of its 21 tables had none.** The rota, attendance,
announcements and leave requests were fully wired; the people those things are about were not.
`workforce.employee` — 14 columns, the HR projection decision 6 accepted — could not be listed,
read, or joined to anything.

## The shape, and why it is not CRUD per table

Four of these tables are read together or not at all. An employee profile screen shows the person,
their employment record, where they are posted and what leave they have left — **four tables, one
question**. So `getEmployee` returns a composed profile and wires all four, rather than four list
endpoints a client has to fan out across.

    listEmployees          workforce.employee
    getEmployee            employee + employment + work_assignment + leave_balance + job_title
    listJobTitles/set      workforce.job_title            reference data
    listLeaveTypes/set     workforce.leave_type           reference data
    listShifts/set         workforce.shift                named patterns, distinct from
                                                          shift_template — see below
    listWorkAssignments    workforce.work_assignment
    setWorkAssignment
    listIntegrationSources workforce.integration_source   Board 10's console
    setIntegrationSource
    getFieldOwnership      workforce.field_ownership      per source, as a set
    setFieldOwnership
    listSyncRuns           workforce.sync_run
    startSync
    listSyncConflicts      workforce.sync_conflict
    resolveSyncConflict

**`workforce.employee` is read-only and that is decision 6, not an omission.** It was taken as an
externally mastered projection — *"connect TICVAI Resource Management with EXTERNAL HR"* — so
there is no `createEmployee` and no `updateEmployee`. The write path is `startSync`, and
`field_ownership` is what says which fields we are even allowed to hold an opinion about. **An
API that lets a manager edit a field the HRMS masters is the conflict this layer exists to
prevent.**

## Two tables that look like duplicates and are not

    workforce.shift             a named pattern: `start_time`, `end_time`, `break_minutes`,
                                `crosses_midnight`. "Early, 06:00-14:00"
    workforce.shift_template    a staffing slot: `starts_at`, `ends_at` as timestamps, plus
                                `required_qualifications`, `role_code`, `cost_centre`,
                                `hourly_rate`

**`crosses_midnight` is the column that settles it.** A pattern needs to say that 22:00-06:00 is
one shift; a slot with two timestamps already knows. They are a definition and an instance, and
`audit-duplicate-tables.py` correctly did not pair them.

    workforce.work_assignment   employee -> job title at a venue, `effective_from`/`to`,
                                `is_primary`. **An employment posting**
    workforce.rota_assignment   principal -> a slot, with `labour_cost` and `overtime_minutes`.
                                **A scheduled shift**

One says where somebody works, the other says when. Wiring both was necessary because the second
was wired and the first was not, which is why a roster could not be checked against a posting.

    python3 tools/applied/wire-workforce-operations-20-september.py --apply
"""
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = os.path.join(ROOT, "contracts", "satellite", "workforce.yaml")

PATHS = '''  /employees:
    get:
      operationId: listEmployees
      summary: People, as the HR system of record has them
      description: 'Resource board 3 page 45, decision 6 of the schema merge. **The employee record
        is a projection of an external system and this endpoint reads it, never writes it.** The write
        path is a synchronisation run; `field_ownership` says which fields we may hold an opinion about
        at all.

        **`workforce.employee` had no operation of any kind until 20 September** — the rota, attendance
        and leave were all wired and the people they are about were not.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      x-ticvai-offline-capable: false
      parameters:
      - name: employmentStatus
        in: query
        schema:
          type: string
      - name: jobTitleId
        in: query
        schema:
          type: string
          format: uuid
      - name: venueId
        in: query
        schema:
          type: string
          format: uuid
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Employees
          content:
            application/json:
              schema:
                allOf:
                - $ref: ../shared/common.yaml#/components/schemas/Page
                - type: object
                  properties:
                    items:
                      type: array
                      items:
                        $ref: '#/components/schemas/WorkforceEmployee'
  /employees/{employeeId}:
    get:
      operationId: getEmployee
      summary: One person, with their employment, postings and leave balances
      description: 'Four tables and one question. **A profile screen that fans out across four list
        endpoints is four round trips and four chances to show a half-loaded person**, so the
        employment record, the postings and the leave balances come back composed.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      x-ticvai-offline-capable: false
      parameters:
      - name: employeeId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceEmployeeProfile'
        '404':
          description: No such employee
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /job-titles:
    get:
      operationId: listJobTitles
      summary: The job titles a posting can name
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Job titles
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceJobTitle'
    put:
      operationId: setJobTitle
      summary: Define a job title
      description: '**Ours to configure even where the HRMS masters the people.** A venue names the
        role a posting fills; the external system names the person who fills it.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkforceJobTitle'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceJobTitle'
  /leave-types:
    get:
      operationId: listLeaveTypes
      summary: Leave types and how each accrues
      description: '**`requestLeave` existed and nothing described what could be requested.** A leave
        request carries a type; the types were a vocabulary nobody could read.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Leave types
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceLeaveType'
    put:
      operationId: setLeaveType
      summary: Define a leave type
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkforceLeaveType'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceLeaveType'
  /leave-balances:
    get:
      operationId: listLeaveBalances
      summary: What each person has left, by leave type
      description: '**A leave request that cannot be checked against a balance is a form, not a
        workflow.** `requestLeave` has existed since the contract was written and the balance it
        should refuse against had no operation.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: employeeId
        in: query
        schema:
          type: string
          format: uuid
      - name: leaveTypeId
        in: query
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Balances
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceLeaveBalance'
  /shifts:
    get:
      operationId: listShifts
      summary: Named shift patterns
      description: '**Distinct from `/shift-templates`, and the distinguishing column is
        `crossesMidnight`.** A pattern says that 22:00 to 06:00 is one shift; a template carries two
        timestamps and already knows. This is the definition, that is the instance.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Shifts
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceShift'
    put:
      operationId: setShift
      summary: Define a shift pattern and its break
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkforceShift'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceShift'
  /work-assignments:
    get:
      operationId: listWorkAssignments
      summary: Where each person is posted, and from when
      description: '**A posting is not a rota slot.** `rota_assignment` says a principal works
        Saturday 14:00 to 22:00; this says they are a Ride Operator at Venue 3, Attractions
        department, from 1 March and primary. **A roster could not be checked against a posting
        because only one of the two was wired.**

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: employeeId
        in: query
        schema:
          type: string
          format: uuid
      - name: venueId
        in: query
        schema:
          type: string
          format: uuid
      - name: activeOn
        in: query
        description: Postings in force on this date. Omit for current.
        schema:
          type: string
          format: date
      responses:
        '200':
          description: Postings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceWorkAssignment'
    put:
      operationId: setWorkAssignment
      summary: Post a person to a job title at a venue
      description: '**A posting ends by `effectiveTo`, never by deletion.** An attendance record from
        March has to resolve against the posting that was in force in March.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkforceWorkAssignment'
      responses:
        '200':
          description: Posted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceWorkAssignment'
        '409':
          description: Overlaps an existing primary posting, or the employee is terminated externally
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /integration-sources:
    get:
      operationId: listIntegrationSources
      summary: External systems that master workforce data, and their health
      description: 'Resource board 10. **The six-state display the board asks for lives on this row** —
        what is connected, when it last synchronised, and whether its credentials still work.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Sources
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceIntegrationSource'
    put:
      operationId: setIntegrationSource
      summary: Connect or reconfigure an external workforce system
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-config-scope: tenant
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WorkforceIntegrationSource'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceIntegrationSource'
  /integration-sources/{sourceId}/field-ownership:
    get:
      operationId: getFieldOwnership
      summary: Which fields this source masters
      description: 'Resource board 3, Ownership Rules: *"For every field, administrators shall determine
        ... External System Master. This prevents conflicting updates."*

        **Absent means ours**, so nothing has to be enumerated before it is decided and the set returned
        here is only what somebody has actually said.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      parameters:
      - name: sourceId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Ownership rules
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceFieldOwnership'
    put:
      operationId: setFieldOwnership
      summary: Declare who masters each field
      description: '**Set as a whole, not row by row.** Ownership is only meaningful read together —
        a screen showing nine fields owned externally and one owned here is the artefact an
        administrator is reasoning about, and applying it one row at a time leaves it inconsistent in
        the middle.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-config-scope: tenant
      parameters:
      - name: sourceId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/WorkforceFieldOwnership'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/WorkforceFieldOwnership'
  /sync-runs:
    get:
      operationId: listSyncRuns
      summary: Synchronisation history, with counts
      description: 'Resource board 10 asks the page to show successful records, failed records,
        warnings and mapping errors rather than *"integration failed"*.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: analytical
      parameters:
      - name: sourceId
        in: query
        schema:
          type: string
          format: uuid
      - name: status
        in: query
        schema:
          type: string
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Runs
          content:
            application/json:
              schema:
                allOf:
                - $ref: ../shared/common.yaml#/components/schemas/Page
                - type: object
                  properties:
                    items:
                      type: array
                      items:
                        $ref: '#/components/schemas/WorkforceSyncRun'
    post:
      operationId: startSync
      summary: Run a synchronisation now
      description: '**This is the write path for `workforce.employee`.** The projection is not edited
        through an API; it is replaced by what the system of record says, field by field, subject to
        `field_ownership`.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-singleton: true
      x-ticvai-singleton-note: 'One run per source at a time. Two concurrent runs against one HRMS
        produce conflicts that are artefacts of the runs rather than of the data.

        '
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - sourceId
              properties:
                sourceId:
                  type: string
                  format: uuid
                dryRun:
                  type: boolean
                  default: false
                  description: Report what would change without applying it.
      responses:
        '202':
          description: Started
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceSyncRun'
        '409':
          description: A run is already in progress for this source
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /sync-conflicts:
    get:
      operationId: listSyncConflicts
      summary: Disagreements a person has to settle
      description: 'Resource board 3 names the cases: an employee in HR and not here, a venue changed
        externally, a certification expired, and *"employee terminated externally but has future TICVAI
        assignments"*.

        **`affectedAssignmentIds` is a snapshot, not a live join** — what was at risk when the conflict
        was raised, which must not change when a roster does.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      parameters:
      - name: sourceId
        in: query
        schema:
          type: string
          format: uuid
      - name: status
        in: query
        schema:
          type: string
      - name: kind
        in: query
        schema:
          type: string
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Conflicts
          content:
            application/json:
              schema:
                allOf:
                - $ref: ../shared/common.yaml#/components/schemas/Page
                - type: object
                  properties:
                    items:
                      type: array
                      items:
                        $ref: '#/components/schemas/WorkforceSyncConflict'
    post:
      operationId: resolveSyncConflict
      summary: Settle a disagreement
      description: '**Board 3 requires the downstream consequence to be visible, not just the
        conflict.** Resolving a terminated-externally conflict has to say what happens to the future
        assignments it flagged, which is why the resolution names them rather than leaving a rota to
        discover it.

        '
      tags:
      - workforce
      x-ticvai-permission: WORKFORCE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ResolveSyncConflictRequest'
      responses:
        '200':
          description: Resolved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WorkforceSyncConflict'
        '409':
          description: Already resolved, or the resolution is not available for this kind
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
'''

SCHEMAS = '''    WorkforceEmployeeProfile:
      type: object
      x-ticvai-persistence: none — composed from employee and four related tables
      description: >
        **One person and everything a profile screen asks about them.** The employment record, the
        postings and the leave balances are separate tables and one question, so fanning out across
        four endpoints is four round trips and four chances to render a half-loaded person.
      required:
      - employee
      properties:
        employee:
          $ref: '#/components/schemas/WorkforceEmployee'
        employments:
          type: array
          description: >
            Most recent first. **More than one is normal** — a seasonal worker rehired each summer
            has several, and collapsing them to the current one loses the service history that
            leave accrual is calculated from.
          items:
            $ref: '#/components/schemas/WorkforceEmployment'
        assignments:
          type: array
          items:
            $ref: '#/components/schemas/WorkforceWorkAssignment'
        leaveBalances:
          type: array
          items:
            $ref: '#/components/schemas/WorkforceLeaveBalance'
        jobTitles:
          type: array
          description: >
            The titles the postings name, so a client does not have to resolve them one by one.
          items:
            $ref: '#/components/schemas/WorkforceJobTitle'
        externallyMasteredFields:
          type: array
          description: >
            **Which fields on this record the venue may not edit**, resolved from
            `field_ownership` for whichever source masters this employee. A screen that shows an
            editable input over a field the HRMS owns has promised something it cannot keep.
          items:
            type: string
    ResolveSyncConflictRequest:
      type: object
      x-ticvai-persistence: none — writes sync_conflict
      required:
      - conflictId
      - resolution
      properties:
        conflictId:
          type: string
          format: uuid
        resolution:
          type: string
          enum:
          - acceptExternal
          - keepTicvai
          - retry
          - ignore
          - escalate
        note:
          type: string
          maxLength: 1000
          nullable: true
        releaseAffectedAssignments:
          type: boolean
          default: false
          description: >
            **For a termination conflict, what happens to the shifts already rostered.** Board 3
            requires the downstream consequence to be acted on rather than reported: releasing them
            puts the shifts back on the marketplace, and leaving them means a manager has decided
            to cover them another way.
'''


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(TARGET, encoding="utf-8").read()
    if "operationId: listEmployees" in s:
        print("  already wired — nothing to do")
        return 0

    i = s.find("\ncomponents:\n")
    if i < 0:
        print("  !! no components block")
        return 1
    s = s[:i + 1] + PATHS + s[i + 1:]

    j = s.find("\n  schemas:\n")
    if j < 0:
        print("  !! no components.schemas block")
        return 1
    k = j + len("\n  schemas:\n")
    s = s[:k] + SCHEMAS + s[k:]

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1

    ops = [o.get("operationId") for p in (doc.get("paths") or {}).values()
           for o in p.values() if isinstance(o, dict) and o.get("operationId")]
    new = [o for o in ops if o in PATHS]
    print("  %d operation(s) in the contract, %d new:" % (len(ops), len(new)))
    for o in sorted(new):
        print("      %s" % o)

    # Every schema an operation names must exist, or the lineage silently derives nothing.
    have = set((doc.get("components") or {}).get("schemas") or {})
    want = ["WorkforceEmployee", "WorkforceEmployment", "WorkforceJobTitle", "WorkforceLeaveType",
            "WorkforceLeaveBalance", "WorkforceShift", "WorkforceWorkAssignment",
            "WorkforceIntegrationSource", "WorkforceFieldOwnership", "WorkforceSyncRun",
            "WorkforceSyncConflict", "WorkforceEmployeeProfile", "ResolveSyncConflictRequest"]
    missing = [w for w in want if w not in have]
    if missing:
        print("  !! schema(s) referenced and not defined: %s" % ", ".join(missing))
        return 1
    print("  all %d referenced schema(s) exist" % len(want))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TARGET, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/workforce.yaml")
    print("\n  Run tools/derive-lineage.py --apply to give them reads and writes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
