# UAE VAT documents and blind close: what the sources say (2 October 2026)

Research for Chinmay's finance decisions of 2 October (change log CHG-FIN-003 and CHG-FIN-011). It answers CF-133
(the legal field set of a UAE tax invoice and credit note) from the law, and states the retail practice behind the
blind close. **The law is quoted from the official English translations, which the FTA and the Ministry of Finance
publish as unofficial; the client's tax adviser confirms the Arabic wording and anything marked "to confirm".**

## 1. UAE tax invoice, simplified tax invoice, tax credit note

Sources: Federal Decree-Law No. 8 of 2017 on VAT, as amended by Decree-Laws 18 of 2022 and 16 of 2024
([FTA consolidated text](https://tax.gov.ae/Datafolder/Files/Legislation/2025/Federal-Decree-Law-No-8-of-2017-and-amendments.pdf));
its Executive Regulation, Cabinet Decision No. 52 of 2017 as amended up to Cabinet Decision No. 100 of 2024, in force
15 November 2024
([FTA consolidated text](https://tax.gov.ae/Datafolder/Files/Legislation/Executive%20Regulation%20of%20Federal%20Decree%20Law%20No%208%20of%202017%20-%20Publish%20-%2004%2010%202024.pdf)).

| Question | Answer | Where |
|---|---|---|
| Must a tax invoice be issued? | Yes. A registrant making a taxable supply issues an original tax invoice and delivers it to the recipient. | Decree-Law Art. 65(1) |
| When? | Within 14 days of the date of supply; a **simplified** tax invoice **on the date of supply**. | Decree-Law Art. 67(1); Exec. Reg. Art. 59(13)(1) |
| Full tax invoice fields | (a) the words "Tax Invoice"; (b) supplier name, address, TRN; (c) recipient name, address, TRN where registered; (d) sequential or unique number; (e) date of issue; (f) date of supply if different; (g) description; (h) per good or service the unit price, quantity, tax rate and amount payable in AED; (i) any discount; (j) gross amount payable in AED; (k) tax charged in AED **with the exchange rate applied** where converted from another currency; (l) reverse-charge statement and the Decree-Law provision where the recipient accounts for the tax. | Exec. Reg. Art. 59(1) |
| Simplified tax invoice fields | (a) the words "Tax Invoice"; (b) supplier name, address, TRN; (c) date of issue; (d) description; (e) total consideration and tax charged in AED. | Exec. Reg. Art. 59(2) |
| When a simplified invoice is allowed | Where the reverse charge does not apply and either (a) the recipient is not a registrant, or (b) the recipient is a registrant and the consideration does not exceed AED 10,000. The FTA may require a full invoice in cases it specifies. | Exec. Reg. Art. 59(5), 59(15) |
| Wholly zero-rated supply | No tax invoice needed where records establish the supply. | Exec. Reg. Art. 59(3) |
| Electronic issue | Allowed if a copy is stored securely and authenticity of origin and integrity of content are guaranteed. | Exec. Reg. Art. 59(8) |
| Foreign currency | The amounts are converted into AED at the **UAE Central Bank rate at the date of supply**. | Decree-Law Art. 69 |
| Rounding | Tax may be rounded to the nearest fils. | Exec. Reg. Art. 61 |
| Tax credit note | Issued when output tax is reduced (Decree-Law Art. 70(1)). Fields: (a) the words "Tax Credit Note"; (b) supplier name, address, TRN; (c) recipient name, address, TRN where registered; (d) date of issue; (e) the value of the supply shown on the tax invoice, the correct value, the difference, and the tax on the difference in AED (a second note on the same invoice starts from the adjusted value); (f) a brief explanation; (g) information identifying the supply. | Decree-Law Art. 70; Exec. Reg. Art. 60(1) |
| Must a VAT receipt be auto-issued? | Not as a separate "receipt": the receipt a retail guest gets **is** the simplified tax invoice, and it is owed on the date of supply for every taxable supply, so the till and the web issue it automatically on payment. Its title is "Tax Invoice", not "Receipt". | Decree-Law Art. 65(1); Exec. Reg. Art. 59(2)(a), 59(13)(1) |

**E-invoicing.** Ministerial Decisions No. 243 and 244 of 2025 (issued 29 September 2025) set the framework and the
phases: a voluntary pilot from 1 July 2026; persons with revenue of AED 50 million or more appoint an accredited service
provider by 31 July 2026 and comply from 1 January 2027; the rest appoint by 31 March 2027 and comply from 1 July 2027;
government entities from 1 October 2027. Invoices and credit notes are exchanged over Peppol through the accredited
service provider and stored in the UAE. **Supplies to consumers are outside e-invoicing**:
"There is no obligation for the supplier or the agent to issue an Electronic Invoice in relation to a supply that is
made to a consumer" — but the VAT tax invoice obligation stays (Ministry of Finance,
[UAE Electronic Invoicing Guidelines v1.1, 1 June 2026](https://mof.gov.ae/wp-content/uploads/2026/06/UAE-Electronic-Invoicing-Guidelines_V-1.1-01June2026.pdf),
section 6.2; [KPMG summary of the decisions](https://kpmg.com/us/en/taxnewsflash/news/2025/10/uae-framework-scope-implementation-e-invoicing-system.html)).
A registrant subject to e-invoicing issues tax invoices and credit notes as electronic invoices (Decree-Law Art. 65(5)),
and Cabinet Decision No. 100 of 2025 (effective 29 September 2025) disapplies parts of Art. 59 and 60 for them: the
simplified invoice is not available for an e-invoiced transaction and the e-credit note shows the credited amount and
its VAT rather than the before, after and difference
([Grant Thornton UAE](https://www.grantthornton.ae/insights/articles2/tax-alert-executive-regulation-amendments/);
the consolidated text of that decision is to confirm with the client's tax adviser).

**Applied** (CHG-FIN-011): `FinTaxInvoiceType`, `FinTaxInvoice` (legal currency, gross in AED, the Central Bank rate and
its source, the amount paid in a guest-selected currency, the reverse-charge statement), `FinTaxInvoiceLine` (amount
payable in AED), `FinCreditMemo` (invoice supply value, corrected value, supplier and buyer blocks, explanation),
`FinTaxInvoiceTemplate` (title wording; auto-issue always on for a UAE registrant; the AED 10,000 limit applies to a
registered buyer only), `issueTaxInvoice`, `issueCreditMemo`; screens POS-026, POS-005, POS-030, POS-011, BO-022,
BO-023, GST-019, WEB-019, ADM-069. A guest who paid in a currency they selected (CHG-FIN-001) gets an invoice in the
base currency with the paid amount, currency and rate as payment information, so every figure the law wants in AED is
the invoice's own.

**Open, for the client's tax adviser.** (1) Whether a guest-selected currency makes the supply a foreign-currency
supply (Art. 69: Central Bank rate) or an AED supply paid in another currency (the package's reading); the contract
records both rates. (2) The Arabic titles. (3) The UAE e-invoicing scope for B2B and partner sales (P10) from 2027.

## 2. Blind close at the till

| Practice | Source |
|---|---|
| The cashier counts before seeing the expected amount; this stops the count being adjusted to match and surfaces real overs and shorts; the supervisor oversees and records each discrepancy. | [Shopify, Balancing a cash drawer](https://www.shopify.com/blog/balancing-a-cash-drawer) ("Require staff to count the cash total before comparing it with the expected POS amount. This is called blind closing") |
| POS products implement it as a switch that hides the expected total and the over/under amount from the person counting. | [commercetools InStore, parameter `Blind_Count`](https://docs.commercetools.com/instore/customization/parameter-based-features.md): it "controls the display of Expected Total field and the Over/Under Amount (discrepancy amount) during the cash count" |
| Count by denomination; the system computes over/short. Recount allowed before the count is final. | [Oracle Retail Xstore, register close](https://docs.oracle.com/cd/E62106_01/xpos/pdf/190/html/managers_guide/register_open_close.htm) (denomination count; Xstore shows over/short to the counter, which is the non-blind configuration) |
| The expected amount is compared server-side; accountability is cleanest with one user per drawer; the over/short is computed at close. | [Microsoft Dynamics 365 Commerce, Shift and cash drawer management](https://learn.microsoft.com/en-us/dynamics365/commerce/shift-drawer-management). Note: Microsoft's "blind close" means closing a shift without counting it yet, a different thing from the blind count. |
| Variance tolerances are tiered (log small ones and watch the trend, investigate larger ones, repeated variances investigated regardless of size), and the variance goes to the manager. | Industry guidance summarised in the search results (unverified against a primary standard); the package keeps one venue threshold, `shiftVarianceThreshold`, proposed AED 20.00 (audit R094). |

**The client said the same** (MoM 12 Aug 2026 section 19, DI-271: the cashier does not see the expected total when
closing; the system flags shortage or overage for supervisor review. MoM 9 Sep 2026 4.18, DI-806, Qossai: many venues
never show the cashier the expected total, "if a cashier knew they had a small surplus, they could pocket it while still
reconciling their own count as balanced"; finance's independent count catches it).

**Applied** (CHG-FIN-003): `submitShiftCount` (the cashier's count returns no expected figure and no variance, only
closed, with the supervisor, or awaiting approval); the variance alerts supervisors holding OVERSHORT_ACCEPT;
`Shift.expectedCash` and `variance` are null to the shift's own cashier; `closeShift` is the supervisor path; the
cashier's reason and note travel with every count (DI-803) and the supervisor can ask for a blind recount (DI-804);
screens POS-001, POS-007, POS-008, POS-020, EMP-008, EMP-009, BO-040. Over and short are both exceptions.
