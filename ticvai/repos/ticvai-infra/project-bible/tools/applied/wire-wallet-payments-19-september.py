#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wire the Wallet and Payment Orchestration boards to their new contracts.

Two packs, 179 unserved screens, and the audit had attributed both to `orders` because
**one** stray wired screen in each named an `orders` operation. That is how `orders`
came to show 178 unserved board screens: Wallet's 99 plus Payment's 79, neither of
which is order-taking.

`wallet.yaml` and `payments.yaml` are new, and each stops deliberately short of what
already exists:

    retail    holds the balance and moves it — `getWallet`, `topUpWallet`,
              `adjustWallet`, `transferWalletBalance`, `listWalletTransactions`, and the
              gift-card operations. `wallet` says what kinds of account and value may
              exist, in what order value is spent, when it expires and what the unspent
              remainder is worth to the business.
    orders    takes the payment — `createPayment`, `capturePayment`, `voidPayment`,
              `createRefund`, `payByLink`, `storePaymentToken`. `payments` decides which
              provider, at what cost, and what happens when it is down.
    tenancy   owns the terminal as a device, since 19 September. `payments` puts a
              merchant account and an EMV configuration on it rather than keeping a
              second register.

**The screens on boards 6 and 7 of the wallet pack wire across all three**, which is
the test of whether the split was drawn in the right place: a refund-to-wallet screen
needs `orders` to refund, `retail` to hold the balance and `wallet` to decide which lot
it lands in, and no single contract could have served it.

Boards are ten screens each and the ids run in order, so the wiring is written per
board position against the board titles.

Idempotent. Run with no arguments to preview; `--apply` to write.
"""
import io
import sys

import yaml

FILES = ('screens/P08-venue-back-office.yaml', 'screens/P09-platform-admin-console.yaml')

W, P, R, O, T, F, A = ('wallet', 'payments', 'retail', 'orders', 'tenancy', 'finance',
                       'approvals')

# board -> first screen id number -> ten lists, one per screen on the board
WALLET_BOARDS = {
    1: (1083, [
        [('listWalletTypes', W, 'Wallet types in use', 'onLoad'),
         ('getWalletLiability', W, 'What is outstanding', 'onLoad')],
        [('listWalletTypes', W, 'The type library', 'onLoad'),
         ('createWalletType', W, 'Define a type', 'onAction')],
        [('createWalletType', W, 'Provisioning rules for a type', 'onAction'),
         ('updateWalletType', W, 'Change them', 'onAction')],
        [('getWallet', R, 'The wallet and its owner', 'onLoad'),
         ('updateWalletType', W, 'Ownership and association rules', 'onAction')],
        [('updateWalletType', W, 'Currency and monetary limits', 'onAction')],
        [('listCreditTypes', W, 'The credit type library', 'onLoad'),
         ('createCreditType', W, 'Define a credit type, without a release', 'onAction'),
         ('updateCreditType', W, 'Change one', 'onAction')],
        [('updateWalletType', W, 'Which features this wallet type has', 'onAction')],
        [('updateWalletType', W, 'Lifecycle states and transitions', 'onAction')],
        [('updateWalletType', W, 'Numbering and identity', 'onAction'),
         ('linkWalletCredential', W, 'Digital credentials', 'onAction')],
        [('publishWalletConfiguration', W, 'Validate and publish', 'onAction')],
    ]),
    2: (1093, [
        [('getWalletFundingRules', W, 'Funding rules in force', 'onLoad'),
         ('listWalletTransactions', R, 'Recent funding', 'onLoad')],
        [('setWalletFundingRules', W, 'Which methods may fund a wallet', 'onAction')],
        [('setWalletFundingRules', W, 'Amounts, presets and bonus rules', 'onAction')],
        [('setWalletFundingRules', W, 'Channel and funding-source mapping', 'onAction')],
        [('setWalletFundingRules', W, 'Auto-reload on a threshold', 'onAction')],
        [('setWalletFundingRules', W, 'Recurring funding on a date', 'onAction')],
        [('setWalletFundingRules', W, 'Approval above a threshold', 'onAction')],
        [('reverseWalletFunding', W, 'Reverse or correct a top-up', 'onAction')],
        [('setWalletFundingRules', W, 'Limits and velocity controls', 'onAction')],
        [('listWalletTransactions', R, 'The funding audit trail', 'onLoad'),
         ('getWalletReconciliation', W, 'Against the acquirer and the ledger', 'onLoad')],
    ]),
    3: (1103, [
        [('listCreditTypes', W, 'Credit types and their balances', 'onLoad'),
         ('getWalletLiability', W, 'Outstanding by type', 'onLoad')],
        [('createCreditType', W, 'Define a credit type', 'onAction'),
         ('updateCreditType', W, 'Change one', 'onAction')],
        [('updateCreditType', W, 'How this credit is issued', 'onAction')],
        [('setCreditEligibilityRules', W, 'Where it may be spent', 'onAction')],
        [('setCreditConsumptionPolicy', W, 'Which credit is spent first', 'onAction'),
         ('getCreditConsumptionPolicy', W, 'The order in force', 'onLoad')],
        [('updateCreditType', W, 'Expiry and validity', 'onAction')],
        [('listCreditLots', W, 'The lots behind a balance', 'onLoad')],
        [('setCreditConsumptionPolicy', W, 'Split tender across credit types', 'onAction'),
         ('simulateCreditConsumption', W, 'What a purchase would use', 'onAction')],
        [('expireCreditLots', W, 'Expire, extend or forfeit', 'onAction')],
        [('simulateCreditConsumption', W, 'Simulate', 'onAction'),
         ('publishWalletConfiguration', W, 'Validate and publish the rules', 'onAction')],
    ]),
    4: (1113, [
        [('listSharedWallets', W, 'Family and corporate structures', 'onLoad')],
        [('createSharedWallet', W, 'Set one up', 'onAction')],
        [('setSharedWalletMembers', W, 'Household members and roles', 'onAction')],
        [('setSharedWalletMembers', W, 'Parent and child distribution', 'onAction'),
         ('transferWalletBalance', R, 'Move value between them', 'onAction')],
        [('setSharedWalletMembers', W, 'Allowance and budget', 'onAction')],
        [('setSharedWalletMembers', W, 'Spending controls per member', 'onAction')],
        [('createSharedWallet', W, 'Corporate hierarchy', 'onAction'),
         ('listSharedWallets', W, 'Existing corporate wallets', 'onLoad')],
        [('setSharedWalletMembers', W, 'Corporate budget and policy', 'onAction')],
        [('transferWalletBalance', R, 'Reallocate balance', 'onAction')],
        [('simulateCreditConsumption', W, 'Simulate a member spend', 'onAction'),
         ('listSharedWallets', W, 'Monitor the structures', 'onLoad')],
    ]),
    5: (1123, [
        [('getWalletLiability', W, 'Gift card liability', 'onLoad')],
        [('setGiftCardProduct', W, 'Denominations and validity', 'onAction')],
        [('issueGiftCard', R, 'Issue', 'onAction'),
         ('activateGiftCard', R, 'Activate', 'onAction')],
        [('listVoucherTypes', W, 'Voucher and coupon types', 'onLoad'),
         ('createVoucherType', W, 'Define one', 'onAction')],
        [('createVoucherType', W, 'Eligibility and redemption rules', 'onAction')],
        [('listVoucherTypes', W, 'Benefits mapped to memberships', 'onLoad')],
        [('listVoucherTypes', W, 'How benefits are presented', 'onLoad')],
        [('expireCreditLots', W, 'Gift card and voucher expiry', 'onAction')],
        [('getWalletLiability', W, 'Balance, liability and breakage', 'onLoad')],
        [('publishWalletConfiguration', W, 'Validate and publish', 'onAction')],
    ]),
    6: (1133, [
        [('setWalletChannelRules', W, 'Where wallets are accepted', 'onLoad')],
        [('setWalletChannelRules', W, 'Channel configuration', 'onAction')],
        [('setWalletChannelRules', W, 'Payment and redemption policy', 'onAction')],
        [('setWalletChannelRules', W, 'Credential kinds accepted', 'onAction')],
        [('linkWalletCredential', W, 'Bind a wearable to a wallet', 'onAction')],
        [('setWalletChannelRules', W, 'NFC, RFID and QR rules', 'onAction')],
        [('setWalletChannelRules', W, 'Authentication and PIN policy', 'onAction')],
        [('setWalletChannelRules', W, 'Offline and degraded mode', 'onAction')],
        [('listPaymentTerminals', P, 'Terminals and acceptance points', 'onLoad'),
         ('setWalletChannelRules', W, 'Map acceptance points', 'onAction')],
        [('simulateCreditConsumption', W, 'Simulate a wallet transaction', 'onAction'),
         ('listWalletTransactions', R, 'Monitor and audit', 'onLoad')],
    ]),
    7: (1143, [
        [('listWalletDisputes', W, 'Open exceptions', 'onLoad'),
         ('listWalletTransactions', R, 'Recent activity', 'onLoad')],
        [('setWalletTransferRules', W, 'Whether guests may transfer', 'onAction')],
        [('setWalletTransferRules', W, 'Eligibility, limits and approval', 'onAction')],
        [('setWalletRefundPolicy', W, 'What a refund puts back, and where', 'onAction')],
        [('setWalletRefundPolicy', W, 'Restoration to the original lots', 'onAction'),
         ('createRefund', O, 'Issue the refund', 'onAction')],
        [('reverseWalletFunding', W, 'Reverse a transaction', 'onAction')],
        [('adjustWallet', R, 'Administrative adjustment', 'onAction')],
        [('setWalletRestriction', W, 'Freeze, block or restrict', 'onAction')],
        [('listWalletDisputes', W, 'The dispute queue', 'onLoad'),
         ('raiseWalletDispute', W, 'Raise one', 'onAction')],
    ]),
    8: (1153, [
        [('setWalletRiskRules', W, 'Rules in force', 'onLoad')],
        [('setWalletRiskRules', W, 'Risk policy', 'onAction')],
        [('setWalletRiskRules', W, 'Transaction scoring', 'onAction')],
        [('setWalletRiskRules', W, 'Velocity and behaviour', 'onAction')],
        [('linkWalletCredential', W, 'Credential and device security', 'onAction'),
         ('listWalletDisputes', W, 'Where it went wrong', 'onLoad')],
        [('setWalletRiskRules', W, 'Anomaly detection rules', 'onAction')],
        [('setWalletRiskRules', W, 'What an automated action does', 'onAction'),
         ('setWalletRestriction', W, 'Freeze on a hit', 'onAction')],
        [('listWalletDisputes', W, 'Fraud cases', 'onLoad')],
        [('simulateCreditConsumption', W, 'Test against a scenario', 'onAction')],
        [('publishWalletConfiguration', W, 'Publish the rules', 'onAction')],
    ]),
    9: (1163, [
        [('getWalletLiability', W, 'Liability at a glance', 'onLoad')],
        [('setWalletAccountingMapping', W, 'Credit types to ledger accounts', 'onAction')],
        [('getWalletReconciliation', W, 'Sub-ledger against the ledger', 'onLoad')],
        [('getWalletReconciliation', W, 'Three sources compared', 'onLoad')],
        [('getWalletReconciliation', W, 'Exceptions to resolve', 'onLoad'),
         ('adjustWallet', R, 'Correct one', 'onAction')],
        [('getWalletLiability', W, 'Gift card liability', 'onLoad')],
        [('setWalletAccountingMapping', W, 'Breakage recognition policy', 'onAction')],
        [('listFiscalPeriods', F, 'The period being closed', 'onLoad'),
         ('getWalletLiability', W, 'Closing balance', 'onLoad')],
        [('getWalletLiability', W, 'Management reporting', 'onLoad')],
        [('getWalletReconciliation', W, 'Validation and audit', 'onLoad')],
    ]),
    10: (1173, [
        [('publishWalletConfiguration', W, 'Configuration state', 'onLoad')],
        [('listWalletTypes', W, 'What the API exposes', 'onLoad')],
        [('setWalletChannelRules', W, 'Integration profile', 'onAction')],
        [('setWalletRiskRules', W, 'Events and notifications', 'onAction')],
        [('listAccessPolicies', 'identity', 'API access and permissions', 'onLoad')],
        [('getWalletReconciliation', W, 'Synchronisation state', 'onLoad')],
        [('listWalletDisputes', W, 'Integration exceptions', 'onLoad')],
        [('publishWalletConfiguration', W, 'Governance and version control', 'onAction')],
        [('publishWalletConfiguration', W, 'Approval and publication', 'onAction'),
         ('createApprovalRequest', A, 'Send for approval', 'onAction')],
        [('getWalletLiability', W, 'Platform health and audit', 'onLoad')],
    ]),
}

PAYMENT_BOARDS = {
    1: (559, [
        [('listPaymentMethods', P, 'Methods in use', 'onLoad'),
         ('getPaymentPerformance', P, 'How they are performing', 'onLoad')],
        [('listPaymentMethods', P, 'The catalogue', 'onLoad'),
         ('createPaymentMethod', P, 'Add a method', 'onAction')],
        [('updatePaymentMethod', P, 'Configure a method', 'onAction')],
        [('updatePaymentMethod', P, 'Per channel and touchpoint', 'onAction')],
        [('updatePaymentMethod', P, 'Per venue and business unit', 'onAction')],
        [('updatePaymentMethod', P, 'Currencies accepted', 'onAction')],
        [('updatePaymentMethod', P, 'Eligibility and availability rules', 'onAction')],
        [('updatePaymentMethod', P, 'Fees and surcharges', 'onAction')],
        [('createApprovalRequest', A, 'Send a change for approval', 'onAction'),
         ('listPaymentMethods', P, 'What is being changed', 'onLoad')],
        [('simulatePaymentConfiguration', P, 'What a guest would be offered', 'onAction')],
    ]),
    2: (569, [
        [('getPaymentProviderHealth', P, 'Provider health', 'onLoad'),
         ('listPaymentProviderConnections', P, 'Providers connected', 'onLoad')],
        [('listPaymentProviderConnections', P, 'The directory', 'onLoad'),
         ('createPaymentProviderConnection', P, 'Connect one', 'onAction')],
        [('createPaymentProviderConnection', P, 'Adapter configuration', 'onAction'),
         ('testPaymentProviderConnection', P, 'Prove it works', 'onAction')],
        [('listPaymentProviderConnections', P, 'Capability against method', 'onLoad')],
        [('setPaymentRoutingRules', P, 'Build the routing rules', 'onAction'),
         ('listPaymentRoutingRules', P, 'Rules in force', 'onLoad')],
        [('setPaymentRoutingRules', P, 'Priority and load distribution', 'onAction')],
        [('setPaymentFailoverPolicy', P, 'Retry, failover and circuit breaking', 'onAction')],
        [('getPaymentProviderHealth', P, 'Authorisation rate and latency', 'onLoad')],
        [('getPaymentProviderEconomics', P, 'What each provider costs', 'onLoad')],
        [('simulatePaymentRouting', P, 'Where would this go, and why', 'onAction')],
    ]),
    3: (579, [
        [('listPaymentTerminals', P, 'Terminals across venues', 'onLoad')],
        [('listPaymentTerminals', P, 'The inventory', 'onLoad'),
         ('listDevices', T, 'The device register behind it', 'onLoad')],
        [('enrolDevice', T, 'Provision the device', 'onAction'),
         ('setPaymentTerminalConfiguration', P, 'Its payment configuration', 'onAction')],
        [('setDeviceAssignment', T, 'Assign it to a workstation', 'onAction')],
        [('setPaymentTerminalConfiguration', P, 'EMV and card-present settings', 'onAction')],
        [('getDeviceTelemetry', T, 'Connectivity over time', 'onLoad')],
        [('listPaymentTerminals', P, 'Live card-present operations', 'onLoad')],
        [('listStoredForwardTransactions', P, 'What is held offline', 'onLoad'),
         ('setPaymentTerminalConfiguration', P, 'Store-and-forward limits', 'onAction')],
        [('getDeviceTelemetry', T, 'Terminal health', 'onLoad'),
         ('createWorkOrder', 'maintenance', 'Raise a repair', 'onAction')],
        [('testPaymentProviderConnection', P, 'Certify the terminal path', 'onAction')],
    ]),
    4: (589, [
        [('getPaymentPerformance', P, 'Digital payment performance', 'onLoad')],
        [('listPaymentMethods', P, 'Alternative methods', 'onLoad'),
         ('updatePaymentMethod', P, 'Configure one', 'onAction')],
        [('updatePaymentMethod', P, 'Digital wallet configuration', 'onAction')],
        [('createPaymentLink', O, 'Build a payment link', 'onAction')],
        [('resendPaymentLink', O, 'Distribute or resend', 'onAction'),
         ('getPaymentLink', O, 'Its state', 'onLoad')],
        [('setHostedCheckoutConfiguration', P, 'Redirect and return', 'onAction')],
        [('inquirePaymentStatus', O, 'Session and transaction state', 'onLoad')],
        [('setPaymentAuthenticationPolicy', P, '3-D Secure, tokens and mandates', 'onAction')],
        [('setHostedCheckoutConfiguration', P, 'Expiry and orphan recovery', 'onAction'),
         ('inquirePaymentStatus', O, 'Recover a session', 'onAction')],
        [('simulatePaymentConfiguration', P, 'Simulate the digital path', 'onAction')],
    ]),
    5: (599, [
        [('getMixedTenderRules', P, 'Tender rules in force', 'onLoad')],
        [('setMixedTenderRules', P, 'Which combinations are allowed', 'onAction')],
        [('setMultiPaymentSplit', O, 'Allocate a split payment', 'onAction'),
         ('setMixedTenderRules', P, 'The sequence rules', 'onAction')],
        [('listB2bCreditAccounts', P, 'On-account customers', 'onLoad'),
         ('createB2bCreditAccount', P, 'Open an account', 'onAction')],
        [('setB2bPaymentTerms', P, 'Limit, terms and billing cycle', 'onAction')],
        [('setMixedTenderRules', P, 'Stored value and voucher tenders', 'onAction'),
         ('getCreditConsumptionPolicy', W, 'The order within stored value', 'onLoad')],
        [('setMixedTenderRules', P, 'Sequence and restrictions', 'onAction')],
        [('setMixedTenderRules', P, 'Partial payment and recovery', 'onAction')],
        [('listOrderPaymentDetail', O, 'Trace the allocation', 'onLoad')],
        [('simulatePaymentConfiguration', P, 'Simulate mixed tender', 'onAction'),
         ('listB2bCreditAccounts', P, 'Credit exposure', 'onLoad')],
    ]),
    6: (609, [
        [('listOrderRefunds', O, 'Refunds in flight', 'onLoad')],
        [('createRefundRequest', O, 'Raise a refund', 'onAction'),
         ('getRefundPolicy', O, 'What is eligible', 'onLoad')],
        [('setRefundPolicy', O, 'Refund rules', 'onAction')],
        [('setWalletRefundPolicy', W, 'Refund to wallet or original tender', 'onAction')],
        [('voidPayment', O, 'Void or reverse', 'onAction')],
        [('approveRefund', O, 'Approve above threshold', 'onAction')],
        [('inquirePaymentStatus', O, 'Provider status and recovery', 'onLoad')],
        [('createRefund', O, 'Adjustment and correction', 'onAction')],
        [('listOrderPaymentDetail', O, 'Trace and investigate', 'onLoad')],
    ]),
    7: (619, [
        [('listSettlements', F, 'Settlements to date', 'onLoad'),
         ('listReconciliationSources', P, 'Feeds and their freshness', 'onLoad')],
        [('setReconciliationSource', P, 'Define a settlement feed', 'onAction'),
         ('ingestSettlementFile', F, 'Import one', 'onAction')],
        [('setReconciliationMatchingRules', P, 'How a match is made', 'onAction')],
        [('listSettlementExceptions', F, 'What did not match', 'onLoad'),
         ('resolveSettlementException', F, 'Resolve it', 'onAction')],
        [('listSettlements', F, 'Settlement and payout', 'onLoad')],
        [('getPaymentProviderEconomics', P, 'Fees, commission and FX', 'onLoad')],
        [('listMerchantAccounts', P, 'Merchant accounts and calendars', 'onLoad'),
         ('setMerchantAccount', P, 'Bind one', 'onAction')],
        [('recordSettlement', F, 'Post to the ledger', 'onAction')],
        [('getUnifiedReconciliation', F, 'Audit and evidence', 'onLoad')],
        [('getUnifiedReconciliation', F, 'Forecast and trend', 'onLoad')],
    ]),
    8: (629, [
        [('getPaymentPerformance', P, 'Risk and fraud at a glance', 'onLoad')],
        [('setPaymentRiskRules', P, 'Rules and decisions', 'onAction')],
        [('setPaymentRiskRules', P, 'Velocity and behaviour', 'onAction')],
        [('setPaymentRiskRules', P, 'Lists and signals', 'onAction')],
        [('listChargebacks', O, 'Cases to investigate', 'onLoad')],
        [('listChargebacks', O, 'Chargebacks and disputes', 'onLoad'),
         ('respondToChargeback', O, 'Respond', 'onAction')],
        [('submitChargebackEvidence', P, 'Assemble a representment', 'onAction')],
        [('getPaymentPerformance', P, 'Conversion and where sales are lost', 'onLoad')],
        [('getPaymentPerformance', P, 'Anomalies in payment behaviour', 'onLoad')],
        [('simulatePaymentConfiguration', P, 'Executive simulation', 'onAction')],
    ]),
}

INVALIDATES = {
    'createWalletType': ['listWalletTypes'],
    'updateWalletType': ['listWalletTypes'],
    'createCreditType': ['listCreditTypes'],
    'updateCreditType': ['listCreditTypes'],
    'setCreditEligibilityRules': ['listCreditTypes'],
    'setCreditConsumptionPolicy': ['getCreditConsumptionPolicy'],
    'expireCreditLots': ['listCreditLots', 'getWalletLiability'],
    'setWalletFundingRules': ['getWalletFundingRules'],
    'reverseWalletFunding': ['listWalletTransactions', 'listCreditLots'],
    'createSharedWallet': ['listSharedWallets'],
    'setSharedWalletMembers': ['listSharedWallets'],
    'createVoucherType': ['listVoucherTypes'],
    'setGiftCardProduct': ['listVoucherTypes'],
    'setWalletChannelRules': ['getWalletFundingRules'],
    'linkWalletCredential': ['getWallet'],
    'setWalletRestriction': ['getWallet'],
    'raiseWalletDispute': ['listWalletDisputes'],
    'setWalletAccountingMapping': ['getWalletLiability'],
    'publishWalletConfiguration': ['listWalletTypes', 'listCreditTypes'],
    'adjustWallet': ['getWallet', 'listWalletTransactions', 'listCreditLots'],
    'transferWalletBalance': ['getWallet', 'listWalletTransactions'],
    'createPaymentMethod': ['listPaymentMethods'],
    'updatePaymentMethod': ['listPaymentMethods'],
    'createPaymentProviderConnection': ['listPaymentProviderConnections'],
    'testPaymentProviderConnection': ['listPaymentProviderConnections'],
    'setPaymentRoutingRules': ['listPaymentRoutingRules'],
    'setPaymentFailoverPolicy': ['getPaymentProviderHealth'],
    'setPaymentTerminalConfiguration': ['listPaymentTerminals'],
    'setMixedTenderRules': ['getMixedTenderRules'],
    'createB2bCreditAccount': ['listB2bCreditAccounts'],
    'setB2bPaymentTerms': ['listB2bCreditAccounts'],
    'setReconciliationSource': ['listReconciliationSources'],
    'setMerchantAccount': ['listMerchantAccounts'],
    'submitChargebackEvidence': ['listChargebacks'],
}


def build():
    wiring = {}
    for boards, prefix in ((WALLET_BOARDS, 'BO-'), (PAYMENT_BOARDS, 'ADM-')):
        for _b, (start, rows) in boards.items():
            for i, ops in enumerate(rows):
                wiring['%s%d' % (prefix, start + i)] = ops
    return wiring


def main():
    apply = '--apply' in sys.argv
    wiring = build()
    added = 0
    touched = 0
    missing = set(wiring)
    for f in FILES:
        d = yaml.safe_load(io.open(f, encoding='utf8'))
        by_id = {s['id']: s for s in d['screens']}
        changed = False
        for sid, ops in sorted(wiring.items()):
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
                touched += 1
                changed = True
        if changed and apply:
            io.open(f, 'w', encoding='utf8').write(
                yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
            print('  -> %s' % f)

    if missing:
        print('  NOT FOUND (%d): %s' % (len(missing), ', '.join(sorted(missing)[:12])))
    print('%d reference(s) across %d screen(s)' % (added, touched))
    if not apply:
        print('\n  nothing written — pass --apply')


if __name__ == '__main__':
    main()
