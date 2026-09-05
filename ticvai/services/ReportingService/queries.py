"""Generated. The declared reads and writes of each operation."""

READS = {
 "acknowledgeAlert": [
  "SELECT * FROM identity.principal LIMIT 50",
  "SELECT * FROM reporting.alert WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "askReportingQuestion": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_column LIMIT 50",
  "SELECT * FROM reporting.report_filter LIMIT 50"
 ],
 "cancelReportExecution": [
  "SELECT * FROM reporting.execution LIMIT 50"
 ],
 "createDashboard": [
  "SELECT * FROM reporting.dashboard LIMIT 50",
  "SELECT * FROM reporting.dashboard_tile LIMIT 50"
 ],
 "createReport": [
  "SELECT * FROM reporting.report_column LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_filter LIMIT 50",
  "SELECT * FROM reporting.report_parameter LIMIT 50"
 ],
 "createReportSchedule": [
  "SELECT * FROM reporting.schedule LIMIT 50",
  "SELECT * FROM reporting.schedule_recipient LIMIT 50"
 ],
 "deleteReport": [
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "deleteReportSchedule": [
  "SELECT * FROM reporting.schedule LIMIT 50"
 ],
 "exportReportResult": [
  "SELECT * FROM reporting.export LIMIT 50"
 ],
 "getDashboard": [
  "SELECT * FROM reporting.dashboard LIMIT 50",
  "SELECT * FROM reporting.dashboard_tile LIMIT 50"
 ],
 "getReport": [
  "SELECT * FROM reporting.report_column LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_filter LIMIT 50",
  "SELECT * FROM reporting.report_parameter LIMIT 50"
 ],
 "getReportExecution": [
  "SELECT * FROM reporting.execution LIMIT 50"
 ],
 "getReportExport": [
  "SELECT * FROM reporting.export LIMIT 50"
 ],
 "getReportResult": [
  "SELECT * FROM reporting.execution LIMIT 50"
 ],
 "getSupplierPerformance": [
  "SELECT * FROM inventory.goods_receipt LIMIT 50",
  "SELECT * FROM inventory.movement LIMIT 50",
  "SELECT * FROM inventory.purchase_order WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM inventory.supplier WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAlertRules": [
  "SELECT * FROM reporting.alert_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAlerts": [
  "SELECT * FROM reporting.alert WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.alert_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listDashboards": [
  "SELECT * FROM reporting.dashboard LIMIT 50",
  "SELECT * FROM reporting.dashboard_tile LIMIT 50"
 ],
 "listReportExecutions": [
  "SELECT * FROM reporting.execution LIMIT 50"
 ],
 "listReportFields": [
  "SELECT * FROM reporting.report_field LIMIT 50"
 ],
 "listReportSchedules": [
  "SELECT * FROM reporting.schedule LIMIT 50"
 ],
 "listReports": [
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listSeededReports": [
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "runReport": [
  "SELECT * FROM reporting.execution LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_parameter LIMIT 50"
 ],
 "saveNaturalLanguageQuery": [
  "SELECT * FROM ai.policy LIMIT 50",
  "SELECT * FROM ai.provider WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_column LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_filter LIMIT 50",
  "SELECT * FROM reporting.report_parameter LIMIT 50"
 ],
 "setAlertRule": [
  "SELECT * FROM identity.role LIMIT 50",
  "SELECT * FROM reporting.alert_rule WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "updateDashboard": [
  "SELECT * FROM reporting.dashboard LIMIT 50",
  "SELECT * FROM reporting.dashboard_tile LIMIT 50"
 ],
 "updateReport": [
  "SELECT * FROM reporting.report_column LIMIT 50",
  "SELECT * FROM reporting.report_definition WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM reporting.report_filter LIMIT 50",
  "SELECT * FROM reporting.report_parameter LIMIT 50"
 ],
 "updateReportSchedule": [
  "SELECT * FROM reporting.schedule LIMIT 50",
  "SELECT * FROM reporting.schedule_recipient LIMIT 50"
 ]
}

WRITES = {
 "acknowledgeAlert": [
  "SELECT id FROM reporting.alert WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "askReportingQuestion": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.report_column ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "cancelReportExecution": [
  "SELECT id FROM reporting.execution ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createDashboard": [
  "SELECT id FROM reporting.dashboard ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.dashboard_tile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createReport": [
  "SELECT id FROM reporting.report_column ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.report_definition WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createReportSchedule": [
  "SELECT id FROM reporting.schedule ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.schedule_recipient ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteReport": [
  "SELECT id FROM reporting.report_definition WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "deleteReportSchedule": [
  "SELECT id FROM reporting.schedule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "exportReportResult": [
  "SELECT id FROM reporting.export ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "runReport": [
  "SELECT id FROM reporting.execution ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "saveNaturalLanguageQuery": [
  "SELECT id FROM ai.interaction WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.report_column ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAlertRule": [
  "SELECT id FROM reporting.alert_rule WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateDashboard": [
  "SELECT id FROM reporting.dashboard ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.dashboard_tile ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateReport": [
  "SELECT id FROM reporting.report_column ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.report_definition WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateReportSchedule": [
  "SELECT id FROM reporting.schedule ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM reporting.schedule_recipient ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "acknowledgeAlert": [
  "cache:idempotency:bench"
 ],
 "askReportingQuestion": [
  "cache:idempotency:bench"
 ],
 "cancelReportExecution": [
  "cache:idempotency:bench"
 ],
 "createDashboard": [
  "cache:idempotency:bench"
 ],
 "createReport": [
  "cache:idempotency:bench"
 ],
 "createReportSchedule": [
  "cache:idempotency:bench"
 ],
 "deleteReport": [
  "cache:idempotency:bench"
 ],
 "deleteReportSchedule": [
  "cache:idempotency:bench"
 ],
 "exportReportResult": [
  "cache:idempotency:bench"
 ],
 "runReport": [
  "cache:idempotency:bench"
 ],
 "saveNaturalLanguageQuery": [
  "cache:idempotency:bench"
 ],
 "setAlertRule": [
  "cache:idempotency:bench"
 ],
 "updateDashboard": [
  "cache:idempotency:bench"
 ],
 "updateReport": [
  "cache:idempotency:bench"
 ],
 "updateReportSchedule": [
  "cache:idempotency:bench"
 ]
}
