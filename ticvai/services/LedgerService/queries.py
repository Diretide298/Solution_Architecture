"""Generated. The declared reads and writes of each operation."""

READS = {
 "abandonPeriodClose": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "approveJournalEntry": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "beginPeriodClose": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "calculateTax": [
  "SELECT * FROM ledger.tax_code LIMIT 50",
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "closeFiscalPeriod": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "createAccount": [
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "createCostCenter": [
  "SELECT * FROM ledger.cost_center LIMIT 50"
 ],
 "createJournalEntry": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "createLegalEntity": [
  "SELECT * FROM ledger.legal_entity WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "createRecognitionSchedule": [
  "SELECT * FROM ledger.recognition_schedule LIMIT 50"
 ],
 "createTaxCode": [
  "SELECT * FROM ledger.tax_code LIMIT 50"
 ],
 "createTaxExemption": [
  "SELECT * FROM ledger.tax_exemption LIMIT 50"
 ],
 "disputeObligation": [
  "SELECT * FROM ledger.inter_entity_obligation LIMIT 50"
 ],
 "getAccount": [
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "getDeferredRevenue": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getFinancialReport": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM ledger.event_budget LIMIT 50",
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "getForeignTenderReport": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM orders.shift WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getJournalEntry": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "getSettlement": [
  "SELECT * FROM ledger.settlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "getTrialBalance": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM ledger.event_budget LIMIT 50",
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "getUnifiedReconciliation": [
  "SELECT * FROM ledger.posting LIMIT 50",
  "SELECT * FROM ledger.settlement WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM orders.payment LIMIT 50",
  "SELECT * FROM retail.wallet_transaction LIMIT 50"
 ],
 "ingestFxRates": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "ingestSettlementFile": [
  "SELECT * FROM ledger.settlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listAccountMappings": [
  "SELECT * FROM ledger.account_mapping LIMIT 50"
 ],
 "listAccounts": [
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "listCostCenters": [
  "SELECT * FROM ledger.cost_center LIMIT 50"
 ],
 "listFiscalPeriods": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "listFxRates": [
  "SELECT * FROM ledger.fx_rate LIMIT 50"
 ],
 "listInterEntityObligations": [
  "SELECT * FROM ledger.inter_entity_obligation LIMIT 50"
 ],
 "listJournalEntries": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "listLedgerEntries": [
  "SELECT * FROM ledger.posting LIMIT 50"
 ],
 "listLegalEntities": [
  "SELECT * FROM ledger.legal_entity WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listPriceVariances": [
  "SELECT * FROM ledger.price_variance LIMIT 50"
 ],
 "listRecognitionSchedules": [
  "SELECT * FROM ledger.recognition_schedule LIMIT 50"
 ],
 "listSettlementExceptions": [
  "SELECT * FROM ledger.settlement_exception LIMIT 50"
 ],
 "listSettlements": [
  "SELECT * FROM ledger.settlement WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "listTaxCodes": [
  "SELECT * FROM ledger.tax_code LIMIT 50"
 ],
 "listTaxExemptions": [
  "SELECT * FROM ledger.tax_exemption LIMIT 50"
 ],
 "recordDeposit": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "recordSettlement": [
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM ledger.inter_entity_obligation LIMIT 50"
 ],
 "recordWriteOff": [
  "SELECT * FROM control.partner_agreement LIMIT 50",
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "rejectJournal": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "reopenPeriod": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50"
 ],
 "resolveObligationDispute": [
  "SELECT * FROM ledger.inter_entity_obligation LIMIT 50"
 ],
 "resolveSettlementException": [
  "SELECT * FROM ledger.settlement_exception LIMIT 50"
 ],
 "reverseJournalEntry": [
  "SELECT * FROM ledger.journal_entry LIMIT 50"
 ],
 "reviewPriceVariance": [
  "SELECT * FROM ledger.price_variance LIMIT 50"
 ],
 "runFxRevaluation": [
  "SELECT * FROM ledger.fiscal_period LIMIT 50",
  "SELECT * FROM ledger.fx_rate LIMIT 50",
  "SELECT * FROM ledger.inter_entity_obligation LIMIT 50"
 ],
 "runRecognition": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM ledger.fiscal_period LIMIT 50",
  "SELECT * FROM orders.sales_order WHERE scope_path LIKE $1 LIMIT 50"
 ],
 "setAccountMappings": [
  "SELECT * FROM ledger.account_mapping LIMIT 50"
 ],
 "setFxProvider": [
  "SELECT * FROM platform.region_settings LIMIT 50"
 ],
 "setFxRate": [
  "SELECT * FROM ledger.fx_rate LIMIT 50"
 ],
 "settleDeposit": [
  "SELECT * FROM ledger.account LIMIT 50",
  "SELECT * FROM ledger.deposit LIMIT 50"
 ],
 "updateAccount": [
  "SELECT * FROM ledger.account LIMIT 50"
 ],
 "updateTaxCode": [
  "SELECT * FROM ledger.tax_code LIMIT 50"
 ],
 "validateRecognitionSchedules": [
  "SELECT * FROM catalogue.product WHERE scope_path LIKE $1 LIMIT 50",
  "SELECT * FROM ledger.recognition_schedule LIMIT 50"
 ]
}

WRITES = {
 "abandonPeriodClose": [
  "SELECT id FROM ledger.fiscal_period ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "approveJournalEntry": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "beginPeriodClose": [
  "SELECT id FROM ledger.fiscal_period ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "closeFiscalPeriod": [
  "SELECT id FROM ledger.fiscal_period ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM platform.outbox WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createAccount": [
  "SELECT id FROM ledger.account ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createCostCenter": [
  "SELECT id FROM ledger.cost_center ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createJournalEntry": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createLegalEntity": [
  "SELECT id FROM ledger.legal_entity WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createRecognitionSchedule": [
  "SELECT id FROM ledger.recognition_schedule ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createTaxCode": [
  "SELECT id FROM ledger.tax_code ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "createTaxExemption": [
  "SELECT id FROM ledger.tax_exemption ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "disputeObligation": [
  "SELECT id FROM ledger.inter_entity_obligation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "ingestFxRates": [
  "SELECT id FROM ledger.fx_rate ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "ingestSettlementFile": [
  "SELECT id FROM ledger.settlement WHERE scope_path LIKE $1 ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordDeposit": [
  "SELECT id FROM ledger.deposit ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordSettlement": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.inter_entity_obligation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "recordWriteOff": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "rejectJournal": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reopenPeriod": [
  "SELECT id FROM ledger.fiscal_period ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resolveObligationDispute": [
  "SELECT id FROM ledger.inter_entity_obligation ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "resolveSettlementException": [
  "SELECT id FROM ledger.settlement_exception ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reverseJournalEntry": [
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "reviewPriceVariance": [
  "SELECT id FROM ledger.price_variance ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "runFxRevaluation": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "runRecognition": [
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.journal_entry ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setAccountMappings": [
  "SELECT id FROM ledger.account_mapping ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFxProvider": [
  "SELECT id FROM platform.region_settings ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "setFxRate": [
  "SELECT id FROM ledger.fx_rate ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "settleDeposit": [
  "SELECT id FROM ledger.deposit ORDER BY id LIMIT 1 FOR UPDATE",
  "SELECT id FROM ledger.posting ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateAccount": [
  "SELECT id FROM ledger.account ORDER BY id LIMIT 1 FOR UPDATE"
 ],
 "updateTaxCode": [
  "SELECT id FROM ledger.tax_code ORDER BY id LIMIT 1 FOR UPDATE"
 ]
}

CACHE = {
 "abandonPeriodClose": [
  "cache:idempotency:bench"
 ],
 "approveJournalEntry": [
  "cache:idempotency:bench"
 ],
 "beginPeriodClose": [
  "cache:idempotency:bench"
 ],
 "calculateTax": [
  "cache:idempotency:bench"
 ],
 "closeFiscalPeriod": [
  "cache:idempotency:bench"
 ],
 "createAccount": [
  "cache:idempotency:bench"
 ],
 "createCostCenter": [
  "cache:idempotency:bench"
 ],
 "createJournalEntry": [
  "cache:idempotency:bench"
 ],
 "createLegalEntity": [
  "cache:idempotency:bench"
 ],
 "createRecognitionSchedule": [
  "cache:idempotency:bench"
 ],
 "createTaxCode": [
  "cache:idempotency:bench"
 ],
 "createTaxExemption": [
  "cache:idempotency:bench"
 ],
 "disputeObligation": [
  "cache:idempotency:bench"
 ],
 "ingestFxRates": [
  "cache:idempotency:bench"
 ],
 "ingestSettlementFile": [
  "cache:idempotency:bench"
 ],
 "recordDeposit": [
  "cache:idempotency:bench"
 ],
 "recordSettlement": [
  "cache:idempotency:bench"
 ],
 "recordWriteOff": [
  "cache:idempotency:bench"
 ],
 "rejectJournal": [
  "cache:idempotency:bench"
 ],
 "reopenPeriod": [
  "cache:idempotency:bench"
 ],
 "resolveObligationDispute": [
  "cache:idempotency:bench"
 ],
 "resolveSettlementException": [
  "cache:idempotency:bench"
 ],
 "reverseJournalEntry": [
  "cache:idempotency:bench"
 ],
 "reviewPriceVariance": [
  "cache:idempotency:bench"
 ],
 "runFxRevaluation": [
  "cache:idempotency:bench"
 ],
 "runRecognition": [
  "cache:idempotency:bench"
 ],
 "setAccountMappings": [
  "cache:idempotency:bench"
 ],
 "setFxProvider": [
  "cache:idempotency:bench"
 ],
 "setFxRate": [
  "cache:idempotency:bench"
 ],
 "settleDeposit": [
  "cache:idempotency:bench"
 ],
 "updateAccount": [
  "cache:idempotency:bench"
 ],
 "updateTaxCode": [
  "cache:idempotency:bench"
 ]
}
