#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the BI, Approvals and Finance Backend boards.

**Both large packs turned out to be mostly joins.** `reporting` already had dashboards,
reports, schedules, exports, alerts and natural-language query; `approvals` already had
requests, decisions, matrices, delegation, escalation, step-up and workflow simulation.
What each lacked was a governance layer the boards spend a third of their screens on:

    reporting   a central KPI library, targets and thresholds, the semantic model that
                report authors build against, pipeline freshness, anomaly detection,
                subscriptions apart from schedules, delivery outcomes, usage and cost.
    approvals   dual control as distinct from segregation of duties, digital signature,
                a tamper-evident decision record, SLA policy as opposed to SLA reading,
                dated approver availability, retention, and evidence packages.

Thirteen and eight operations respectively — against 57 and 74 unserved screens. **The
ratio is the point:** authoring against a board screen count would have produced a
hundred and thirty operations, most of them duplicates of what was already there.

Boards 5 to 8 of the BI pack are wired to `reporting` reads because they are analytical
views of other contexts' data rather than new capability; the AI board (9) is wired to
what exists and its model-governance screens are left for the AI phase.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

FILES = ('screens/P16-venue-analytics.yaml', 'screens/P08-venue-back-office.yaml',
         'screens/P09-platform-admin-console.yaml')

R = 'reporting'
A = 'approvals'

WIRING = {
    # ---------------------------------------------------- BI board 1: executive
    'ANL-012': [('getKpiValues', R, 'Live operational KPIs', 'onLoad'),
                ('listAlerts', R, 'What needs attention', 'onLoad')],
    'ANL-013': [('getKpiValues', R, 'Revenue against target', 'onLoad')],
    'ANL-014': [('getKpiValues', R, 'Attendance and footfall', 'onLoad')],
    'ANL-015': [('getKpiValues', R, 'Capacity and utilisation', 'onLoad')],
    'ANL-016': [('getKpiValues', R, 'Sales by channel', 'onLoad')],
    'ANL-017': [('getKpiValues', R, 'Membership and loyalty', 'onLoad')],
    'ANL-019': [('askReportingQuestion', R, 'Ask about what moved', 'onAction'),
                ('listAnalyticsAnomalies', R, 'What moved unexpectedly', 'onLoad')],
    'ANL-020': [('getAnalyticsBenchmark', R, 'Site against site, normalised', 'onLoad')],

    # ------------------------------------------------- BI board 2: dashboards
    'ANL-021': [('listDashboards', R, 'The library', 'onLoad')],
    'ANL-022': [('createDashboard', R, 'Create one', 'onAction')],
    'ANL-023': [('updateDashboard', R, 'Lay it out', 'onAction'),
                ('getDashboard', R, 'The dashboard being edited', 'onLoad')],
    'ANL-024': [('getSemanticModel', R, 'What a widget can be bound to', 'onLoad')],
    'ANL-025': [('listKpis', R, 'KPIs already defined', 'onLoad'),
                ('createKpi', R, 'Define one, for everywhere', 'onAction')],
    'ANL-026': [('setKpiTargets', R, 'Targets and thresholds', 'onAction'),
                ('listKpis', R, 'The KPI being targeted', 'onLoad')],
    'ANL-027': [('getSemanticModel', R, 'Datasets and fields to filter on', 'onLoad'),
                ('updateDashboard', R, 'Save the filters', 'onAction')],
    'ANL-028': [('updateDashboard', R, 'Drill-down behaviour', 'onAction')],
    'ANL-029': [('updateDashboard', R, 'Publish and version', 'onAction')],
    'ANL-030': [('getDashboard', R, 'Preview', 'onLoad'),
                ('listAnalyticsPipelines', R, 'Whether its data is fresh', 'onLoad')],

    # ---------------------------------------------------- BI board 3: reports
    'ANL-031': [('listReports', R, 'The catalogue', 'onLoad'),
                ('listSeededReports', R, 'What ships with the platform', 'onLoad')],
    'ANL-032': [('createReport', R, 'Create a report', 'onAction')],
    'ANL-033': [('getSemanticModel', R, 'Domains and datasets', 'onLoad')],
    'ANL-034': [('listReportFields', R, 'Fields available here', 'onLoad')],
    'ANL-035': [('updateReport', R, 'Filters and parameters', 'onAction')],
    'ANL-036': [('updateReport', R, 'Grouping and calculations', 'onAction')],
    'ANL-037': [('getSemanticModel', R, 'How domains relate', 'onLoad'),
                ('updateReport', R, 'Compose across them', 'onAction')],
    'ANL-038': [('updateReport', R, 'Layout and formatting', 'onAction')],
    'ANL-039': [('runReport', R, 'Run it against a sample', 'onAction'),
                ('getReportExecution', R, 'How the run went', 'onLoad')],
    'ANL-040': [('runReport', R, 'Run it', 'onAction'),
                ('getReportResult', R, 'The results', 'onLoad')],

    # ------------------------------------------- BI board 4: governance of reports
    'ANL-041': [('listReportSchedules', R, 'What runs when', 'onLoad'),
                ('listReportDeliveries', R, 'What arrived and what did not', 'onLoad')],
    'ANL-042': [('listReportSchedules', R, 'Schedules', 'onLoad'),
                ('createReportSchedule', R, 'Schedule a report', 'onAction')],
    'ANL-043': [('listReportSubscriptions', R, 'Who receives what', 'onLoad'),
                ('createReportSubscription', R, 'Add a recipient', 'onAction')],
    'ANL-044': [('createReportSubscription', R, 'Channel, format and recipients', 'onAction')],
    'ANL-045': [('exportReportResult', R, 'Export', 'onAction'),
                ('getReportExport', R, 'Collect the file', 'onLoad')],
    'ANL-046': [('listReportSubscriptions', R, 'API and SFTP delivery', 'onLoad')],
    'ANL-047': [('listAccessPolicies', 'identity', 'Who may see which report', 'onLoad')],
    'ANL-048': [('listReportDeliveries', R, 'Failures and retries', 'onLoad')],
    'ANL-049': [('listReportDeliveries', R, 'What left, with what in it', 'onLoad')],
    'ANL-050': [('setApprovalRetentionPolicy', A, 'Retention and archive', 'onAction')],

    # ------------------------------------------------ BI board 9: AI analytics
    'ANL-051': [('listAnalyticsAnomalies', R, 'What the models noticed', 'onLoad')],
    'ANL-052': [('askReportingQuestion', R, 'Ask in plain language', 'onAction'),
                ('saveNaturalLanguageQuery', R, 'Keep the question', 'onAction')],
    'ANL-053': [('createDashboard', R, 'Accept a generated dashboard', 'onAction')],
    'ANL-054': [('createReport', R, 'Accept a generated report', 'onAction')],
    'ANL-055': [('listAnalyticsAnomalies', R, 'Anomalies, with severity', 'onLoad')],
    'ANL-056': [('listAnalyticsAnomalies', R, 'Candidate causes', 'onLoad'),
                ('askReportingQuestion', R, 'Follow the thread', 'onAction')],
    'ANL-057': [('getKpiValues', R, 'The series being forecast', 'onLoad')],
    'ANL-058': [('listAnalyticsAnomalies', R, 'What to act on', 'onLoad')],
    'ANL-059': [('listAnalyticsAnomalies', R, 'Past insights and their evidence', 'onLoad')],

    # -------------------------------------------- BI board 10: administration
    'ANL-061': [('getAnalyticsUsage', R, 'Estate at a glance', 'onLoad'),
                ('listAnalyticsPipelines', R, 'Data health', 'onLoad')],
    'ANL-062': [('listKpis', R, 'The enterprise library', 'onLoad'),
                ('createKpi', R, 'Add a KPI', 'onAction')],
    'ANL-063': [('setKpiTargets', R, 'Targets and scorecards', 'onAction'),
                ('getKpiValues', R, 'Where they stand', 'onLoad')],
    'ANL-064': [('getAnalyticsBenchmark', R, 'Configure the comparison basis', 'onLoad')],
    'ANL-065': [('listAnalyticsPipelines', R, 'Sources and integrations', 'onLoad')],
    'ANL-066': [('getSemanticModel', R, 'The catalogue', 'onLoad'),
                ('setSemanticModel', R, 'Publish it', 'onAction')],
    'ANL-067': [('listAnalyticsPipelines', R, 'Refresh and freshness', 'onLoad')],
    'ANL-068': [('listDashboards', R, 'Workspaces and embedding', 'onLoad')],
    'ANL-069': [('getAnalyticsUsage', R, 'Usage, runtime and cost', 'onLoad')],

    # ------------------------------------------- Approvals board 1: the queues
    'BO-364': [('getApprovalAnalytics', A, 'Volume, outcome and SLA', 'onLoad'),
               ('listApprovalRequests', A, 'What is waiting', 'onLoad')],
    'BO-365': [('listApprovalRequests', A, 'Mine to decide', 'onLoad')],
    'BO-366': [('listApprovalRequests', A, 'The shared queue', 'onLoad')],
    'BO-367': [('listApprovalRequests', A, 'The request', 'onLoad'),
               ('decideApprovalRequest', A, 'Approve or reject', 'onAction')],
    'BO-368': [('evaluateApprovalRequirement', A, 'What the rules say', 'onLoad')],
    'BO-369': [('listApprovalRequests', A, 'High priority and risk', 'onLoad')],
    'BO-370': [('listSlaEscalationBottleneck', A, 'What escalated and why', 'onLoad'),
               ('escalateApprovalRequest', A, 'Escalate', 'onAction')],
    'BO-371': [('listApprovalRequests', A, 'Completed history', 'onLoad')],
    'BO-372': [('listSlaEscalationReminder', A, 'SLA and workload', 'onLoad'),
               ('getApprovalAnalytics', A, 'Where the time goes', 'onLoad')],
    'BO-373': [('listWorkflowInstanceProcess', A, 'Activity across workflows', 'onLoad')],

    # ------------------------------------- Approvals board 4: the decision itself
    'BO-375': [('listApprovalRequests', A, 'The request and its evidence', 'onLoad')],
    'BO-376': [('getApprovalRecord', A, 'The decision chain, verified', 'onLoad')],
    'BO-377': [('decideApprovalRequest', A, 'Approve', 'onAction'),
               ('signApprovalDecision', A, 'Sign it where required', 'onAction'),
               ('listStepUpPolicies', A, 'Whether step-up is required', 'onLoad')],
    'BO-378': [('decideApprovalRequest', A, 'Reject, return or ask for more', 'onAction')],
    'BO-379': [('resubmitApprovalRequest', A, 'Amend and resubmit', 'onAction')],
    'BO-380': [('withdrawApprovalRequest', A, 'Withdraw or cancel', 'onAction')],
    'BO-381': [('listApprovalControlPolicies', A, 'Four-eyes and dual control in force',
                'onLoad')],
    'BO-382': [('listWorkflowInstanceProcess', A, 'Whether the approved action ran', 'onLoad')],
    'BO-383': [('getApprovalRecord', A, 'The immutable record, and whether it is intact',
                'onLoad')],

    # --------------------------------- Approvals board 5: delegation and escalation
    'BO-384': [('listApprovalDelegations', A, 'Delegations in force', 'onLoad'),
               ('listSlaEscalationBottleneck', A, 'Live escalations', 'onLoad')],
    'BO-386': [('setApproverAvailability', A, 'Dated, so nobody forgets to turn it off',
                'onAction'),
               ('listApprovalDelegations', A, 'Existing delegations', 'onLoad')],
    'BO-387': [('setApproverAvailability', A, 'Out of office and substitute', 'onAction')],
    'BO-388': [('setApprovalSlaPolicy', A, 'Target, reminders and breach behaviour', 'onAction')],
    'BO-389': [('setApprovalSlaPolicy', A, 'Reminder and breach rules', 'onAction')],
    'BO-390': [('setApprovalSlaPolicy', A, 'Escalation on breach', 'onAction')],
    'BO-391': [('listSlaEscalationBottleneck', A, 'What is escalating now', 'onLoad')],
    'BO-392': [('getApprovalAnalytics', A, 'SLA and escalation performance', 'onLoad')],
    'BO-393': [('getApprovalAnalytics', A, 'Where the SLA is failing', 'onLoad')],

    # ------------------------------------- Approvals board 2: workflow authoring
    'ADM-320': [('setVisualWorkflow', A, 'Create the workflow', 'onAction')],
    'ADM-322': [('setVisualWorkflow', A, 'Stages and approvers', 'onAction')],
    'ADM-323': [('setVisualBusinessRule', A, 'Conditions and decision rules', 'onAction'),
                ('listConditionDecisionLogic', A, 'Rules already defined', 'onLoad')],
    'ADM-324': [('setVisualWorkflow', A, 'Sequence and parallel routing', 'onAction')],
    'ADM-325': [('setTriggerActionCross', A, 'What happens on each outcome', 'onAction')],
    'ADM-326': [('simulateWorkflowTestingImpact', A, 'Simulate before publishing', 'onAction')],
    'ADM-327': [('listWorkflow', A, 'Workflow lifecycle', 'onLoad'),
                ('setVisualWorkflow', A, 'Publish', 'onAction')],
    'ADM-328': [('listVersioningEffectiveDate', 'marketing-crm', 'Version history', 'onLoad'),
                ('listWorkflow', A, 'The workflow being versioned', 'onLoad')],

    # ---------------------------------------- Approvals board 3: the routing matrix
    'ADM-329': [('listApprovalMatrices', A, 'Matrices in force', 'onLoad')],
    'ADM-330': [('setApprovalMatrix', A, 'Authority by role and value', 'onAction')],
    'ADM-331': [('setApprovalMatrix', A, 'Route up the hierarchy', 'onAction')],
    'ADM-332': [('setApprovalMatrix', A, 'By department', 'onAction')],
    'ADM-333': [('setApprovalMatrix', A, 'By venue and tenant', 'onAction')],
    'ADM-334': [('setApprovalMatrix', A, 'By value threshold', 'onAction')],
    'ADM-335': [('setApprovalMatrix', A, 'By risk and condition', 'onAction')],
    'ADM-336': [('setApprovalControlPolicy', A, 'Approver groups and decision policy',
                 'onAction')],
    'ADM-337': [('evaluateApprovalRequirement', A, 'Where would this route', 'onAction'),
                ('simulateWorkflowTestingImpact', A, 'Conflicts in the matrix', 'onAction')],
    'ADM-338': [('listApprovalMatrices', A, 'The matrix being advised on', 'onLoad')],

    # ----------------------------------------- Approvals board 6: governance
    'ADM-339': [('listApprovalControlPolicies', A, 'Controls in force', 'onLoad'),
                ('getApprovalAnalytics', A, 'Governance posture', 'onLoad')],
    'ADM-340': [('setSegregationRules', 'identity', 'Which roles may not be held together',
                 'onAction')],
    'ADM-341': [('setApprovalControlPolicy', A, 'Four-eyes and dual control', 'onAction'),
                ('listApprovalControlPolicies', A, 'What is already required', 'onLoad')],
    'ADM-343': [('setStepUpPolicy', A, 'Which actions need re-authentication', 'onAction'),
                ('listStepUpPolicies', A, 'Policies in force', 'onLoad')],
    'ADM-344': [('signApprovalDecision', A, 'Signature methods in use', 'onAction')],
    'ADM-345': [('getApprovalRecord', A, 'Chained records, verified on read', 'onLoad')],
    'ADM-346': [('setApprovalRetentionPolicy', A, 'How long records are kept', 'onAction')],
    'ADM-347': [('createApprovalEvidencePackage', A, 'Assemble what an auditor asked for',
                 'onAction')],
    'ADM-348': [('getApprovalAnalytics', A, 'Risk and compliance posture', 'onLoad')],

    # --------------------------------------- Approvals board 7: integration
    'ADM-349': [('listCrossModuleOrchestration', A, 'Which modules raise approvals', 'onLoad')],
    'ADM-350': [('listCrossModuleOrchestration', A, 'The integration registry', 'onLoad')],
    'ADM-351': [('listApprovalRequests', A, 'What the API exposes', 'onLoad')],
    'ADM-352': [('setTriggerActionCross', A, 'Workflow events', 'onAction')],
    'ADM-355': [('setTriggerActionCross', A, 'Map external data onto a request', 'onAction')],
    'ADM-357': [('listWorkflowExceptionFailure', A, 'Errors and retries', 'onLoad')],
    'ADM-358': [('listWorkflowProcessPerformance', A, 'Integration health', 'onLoad')],

    # ------------------------------------------- Approvals board 8: analytics
    'ADM-359': [('getApprovalAnalytics', A, 'The executive view', 'onLoad')],
    'ADM-360': [('getApprovalAnalytics', A, 'Volume and outcome', 'onLoad')],
    'ADM-361': [('getApprovalAnalytics', A, 'Processing time', 'onLoad')],
    'ADM-362': [('listSlaEscalationBottleneck', A, 'Where it backs up', 'onLoad')],
    'ADM-363': [('getApprovalAnalytics', A, 'Trend and comparison', 'onLoad')],
    'ADM-364': [('getApprovalAnalytics', A, 'By approver and team', 'onLoad')],
    'ADM-366': [('getApprovalAnalytics', A, 'What the models see', 'onLoad')],
    'ADM-367': [('simulateWorkflowTestingImpact', A, 'What-if on the workflow', 'onAction')],
    'ADM-368': [('getApprovalAnalytics', A, 'Governance for the executive', 'onLoad')],

    # ------------------------------------------------ Finance Backend, both screens
    'BO-1081': [('getKpiValues', R, 'Finance KPIs against target', 'onLoad'),
                ('getUnifiedReconciliation', 'finance', 'Where the money stands', 'onLoad')],
    'BO-1082': [('getKpiValues', R, 'Admissions revenue', 'onLoad'),
                ('runReport', R, 'The underlying report', 'onAction')],
}

INVALIDATES = {
    'createKpi': ['listKpis', 'getKpiValues'],
    'setKpiTargets': ['getKpiValues'],
    'setSemanticModel': ['getSemanticModel', 'listReportFields'],
    'createReportSubscription': ['listReportSubscriptions'],
    'createDashboard': ['listDashboards'],
    'updateDashboard': ['getDashboard', 'listDashboards'],
    'createReport': ['listReports'],
    'updateReport': ['getReport', 'listReports'],
    'createReportSchedule': ['listReportSchedules'],
    'setApprovalControlPolicy': ['listApprovalControlPolicies'],
    'setApprovalSlaPolicy': ['listSlaEscalationReminder'],
    'setApproverAvailability': ['listApprovalDelegations'],
    'setApprovalRetentionPolicy': ['getApprovalRecord'],
    'signApprovalDecision': ['getApprovalRecord'],
    'decideApprovalRequest': ['listApprovalRequests', 'getApprovalRecord',
                              'getApprovalAnalytics'],
    'escalateApprovalRequest': ['listApprovalRequests', 'listSlaEscalationBottleneck'],
    'resubmitApprovalRequest': ['listApprovalRequests'],
    'withdrawApprovalRequest': ['listApprovalRequests'],
    'setApprovalMatrix': ['listApprovalMatrices'],
    'setVisualWorkflow': ['listWorkflow'],
    'setVisualBusinessRule': ['listConditionDecisionLogic'],
    'setStepUpPolicy': ['listStepUpPolicies'],
    'setTriggerActionCross': ['listCrossModuleOrchestration'],
}


def main():
    apply = '--apply' in sys.argv
    added = 0
    touched = []
    missing = set(WIRING)
    for f in FILES:
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        by_id = {s['id']: s for s in d['screens']}
        changed = False
        for sid, ops in sorted(WIRING.items()):
            s = by_id.get(sid)
            if not s:
                continue
            missing.discard(sid)
            have = {a.get('operationId') for a in (s.get('apis') or [])}
            new = []
            for oid, contract, purpose, trigger in ops:
                if oid in have:
                    continue
                entry = {'operationId': oid, 'contract': contract,
                         'purpose': purpose, 'trigger': trigger,
                         'provenance': 'board reading, 19 September 2026'}
                if INVALIDATES.get(oid):
                    entry['invalidates'] = INVALIDATES[oid]
                new.append(entry)
            if new:
                s.setdefault('apis', []).extend(new)
                added += len(new)
                changed = True
                touched.append((sid, s['name'], [n['operationId'] for n in new]))
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)

    if missing:
        print('  NOT FOUND: %s' % ', '.join(sorted(missing)))
    print('%d reference(s) across %d screen(s)' % (added, len(touched)))
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
