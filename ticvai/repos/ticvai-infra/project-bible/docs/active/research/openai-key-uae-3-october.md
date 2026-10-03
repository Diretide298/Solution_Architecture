# TICVAI: can a tenant use its own OpenAI key (global, not UAE-hosted)?

Date: 3 October 2026. Builds on `ai-ml-model-selection-2-october.md` §2A (UAE routes, S-numbers below refer to its
source list) and `answers-2-oct-batch1.md` (AI residency classes, BYOK, the mandatory offline scrubber, and the
3 Oct hosting decision: no self-hosted models; Compass default, OpenAI UAE fallback, BYOK; Presidio stays mandatory).

> **This is legal interpretation for engineering planning, not legal advice.** The PDPL Executive Regulations are
> still unpublished, so several points below are open questions. A UAE-qualified lawyer should confirm the rows
> marked *interpretation* before a tenant is enabled.

## Short answer

**Yes, for a non-government, onshore private tenant that opts in as data controller. No for government entities and
government-related entities (GREs) without their own written approval, or for regulated sectors.** The scrubber
reduces risk, but it does not take the traffic out of the PDPL. A tokenised prompt is still *pseudonymised* personal
data. Presidio also has residual misses. So every call to a global OpenAI endpoint is a cross-border transfer that
needs an Art. 23 basis. Two more points:

- An OpenAI key does not have to mean global processing. An OpenAI API project in the **UAE region**
  (`ae.api.openai.com`) runs the listed models in the UAE.
- Azure OpenAI in UAE North (Standard or Regional PTU) runs OpenAI models in the UAE with Microsoft as the processor.

## 1. UAE PDPL (Federal Decree-Law 45/2021) as it stands

| Point | Finding | Source |
|---|---|---|
| Personal data | "Any data relating to an identified natural person, or one who can be identified directly or indirectly by way of linking data…" | [W1], [W2] |
| Pseudonymisation is defined, and it is not an exit | Art. 1 defines pseudonymisation as processing after which the data "can no longer be linked … without the use of additional information, as long as such additional information is kept separately and safely". Arts. 7 and 20 list pseudonymisation as a **security measure** the controller must apply. Only *anonymisation* (no identification "in any way whatsoever") falls outside. | [W1] |
| Reading for TICVAI (*interpretation*) | Our reversible token map is exactly "additional information kept separately", so the outbound prompt is pseudonymised personal data and stays in scope. EU comparator: in CJEU C-413/23 P *EDPS v SRB* (4 Sep 2025), pseudonymised data may fall outside the definition *for a recipient* that cannot reasonably re-identify. The controller's duties, including notice of recipients, still apply. That ruling is persuasive at most in the UAE, and residual scrubber misses defeat the argument anyway. | [W1], [W9], [W10] |
| Sensitive personal data | Covers data revealing family, racial origin, political or philosophical opinions, religious beliefs, criminal records, **biometric data** and **health** data. Venue examples: allergies and dietary needs, accessibility needs, face images for passes. | [W2] |
| Scope exclusions (Art. 2(2)) | The PDPL does **not** apply to government data, government authorities processing personal data, security and judicial authorities, health and banking data under their own laws, or free zones with their own law (DIFC, ADGM). Government tenants therefore fall under emirate and federal government rules, not the Art. 23 route. | [W1], [W2], [W4] |
| Art. 22 (adequacy) | Transfers are allowed to a country with data-protection law covering the main PDPL controls, or with a bilateral or multilateral agreement. **No adequacy list has been published.** | [W1], [W4] |
| Art. 23 (no adequacy) | Transfers are allowed (a) under a contract binding the foreign recipient to the PDPL's provisions, controls and requirements; (b) with the data subject's express consent, where this does not conflict with State security or the public interest; (c) where needed for contract performance between the controller and the data subject; and (d) for legal claims, judicial cooperation or the public interest. Art. 23(2) leaves the detailed controls to the Executive Regulations. | [W1], [W3] |
| DPIA (Art. 21) | Required before high-risk processing with new technology, including systematic automated assessment. LLM processing of guest data fits this. | [W1] |
| Executive Regulations | **Still not issued.** The legislation portal listed none on 23 Sep 2026. Chambers (Mar 2026), Kayrouz (Feb 2026) and GLA (Jun 2026) agree. One secondary site claims "Cabinet Resolution 33 of 2024" issued them; that is **not corroborated** and should be treated as wrong. | [W3], [W4], [W5], [W6], [W8] |
| New regulator (2025–2026) | The **Federal Authority for Artificial Intelligence and Data** was announced on 14 Jun 2026. It absorbs the AI Office, TDRA's Digital Government sector and the **UAE Data Office**, and reports to the Cabinet. Its enforcement instruments are not yet defined. Expect transfer rules to tighten, not loosen. | [W6], [W7] |

## 2. Sector and emirate rules

| Regime | Applies to | Effect on a global OpenAI key | Source |
|---|---|---|---|
| Abu Dhabi Government (DGE) | Abu Dhabi government entities | The Digital Strategy 2025–27 commits to "100 per cent sovereign cloud adoption". ADISS binds entities **and their contractors** for storage and transmission of government information. TAMM runs on Azure OpenAI with G42 Compass. Global OpenAI: **no**. | [W11], [W12], S117 |
| Dubai Government (DESC) | Dubai government and semi-government entities | "Government and semi-government organizations in Dubai must ensure that any CSP they're using complies with" the DESC CSP standard. The DESC ISR also applies. Dubai Law 26/2015 makes such entities "Data Providers" with confidentiality duties. Global OpenAI: **no** in practice. The exact Dubai localisation instrument is still UNCONFIRMED (as on 2 Oct). | [W13], [W14] |
| Dubai AI Seal (DCAI) | Vendors | Required to partner on UAE or Dubai government AI projects. This is a **TICVAI vendor certification**, not a model list. | [W15] |
| Federal: TDRA Information Assurance Regulation | Federal government and TDRA-designated critical entities; voluntary for others | Its controls cover processing, storage and transmission. Global OpenAI for such entities: **no** without the entity's own approval. | [W16] |
| National Cloud Security Policy (Cyber Security Council) | Cloud consumers and providers in the UAE | Requires transparency on where data is "stored, processed, and managed from", and operational sovereignty for sovereign clouds. It is not a ban on private use. | [W17] |
| Health data law (Federal Law 2/2019, Art. 13; MD 51/2021) | Data from health services delivered in the UAE (for example a park clinic or first-aid record) | Storage and processing outside the UAE are prohibited unless an exception applies. Keep such data out of all prompts. | [W18] |
| CBUAE | Bank and payment licensees | Localisation applies. Venues are normally not licensees, but their PSP's data is not ours to send. | S132 |
| DIFC / ADGM | Tenants established there | Their own transfer regimes apply (SCCs). The PDPL does not apply to them. | S130, S131, [W4] |
| UAE AI Charter (2024), AI Ethics Guide, AI Adoption Guideline for Government | Guidance | These documents are non-binding. The u.ae AI resources page lists **no approved model or provider list**. | [W19], [W20] |

**What "UAE-approved LLM" means in practice.** No formal federal list of approved models was found. The term works as
shorthand for four things:

1. Hosting on a sovereign or certified in-country cloud: CSC-certified (du National Hypercloud, e& with AWS), DESC-certified
   for Dubai, or Abu Dhabi sovereign cloud (S115, S136).
2. A UAE vendor wrapper such as G42/Core42 Compass (S117, S118).
3. UAE-built models (Falcon, Jais, K2), which official pages promote but do not mandate ([W20]).
4. For Dubai, a vendor holding the Dubai AI Seal ([W15]).

Approval is given per entity, by its CISO or data office, and recorded in the procurement contract.

## 3. OpenAI and Azure OpenAI data terms

| Item | Finding | Source |
|---|---|---|
| Training | API data is not used to train OpenAI models (since 1 Mar 2023). | [W21] |
| Default retention | Abuse-monitoring logs are kept for up to **30 days** for all API usage. | [W21] |
| ZDR / Modified Abuse Monitoring | These require approval and can be set per organisation or per project. Eligible endpoints include `/v1/chat/completions` and `/v1/responses` (with limitations: use `store=false`), plus embeddings and audio. **Not eligible:** `/v1/assistants`, `/v1/threads`, `/v1/conversations`. | [W21] |
| Data residency regions | US, EU, **UAE (`ae.api.openai.com`, storage and regional processing)**, UK, Japan, India, Singapore, Korea, Australia and Canada. Non-US regions require abuse-monitoring-control approval and a **Modified Retention amendment**. | [W21] |
| UAE regional processing | Available only for `gpt-5.6-luna`, `gpt-5.5-2026-04-23`, `gpt-5.2-2025-12-11` and `text-embedding-3-large`. There is a +10% uplift on models released on or after 5 Mar 2026. Approval is through sales. | [W21] |
| ChatGPT (not API) | UAE inference residency for ChatGPT Enterprise and Edu went live in Aug 2026. This is not the API. | [W22], S107 |
| Stargate UAE / OpenAI for Countries | Announced 22 May 2025: a 1 GW Abu Dhabi cluster with G42, Oracle, Nvidia, Cisco and SoftBank, with 200 MW expected in 2026. It is the first "OpenAI for Countries" deal. No source says the API UAE region runs on it, and it creates no API rights for tenants. | [W23] |
| DPA | OpenAI offers a DPA (openai.com/policies/data-processing-addendum). The page was **not reachable** from this session (403), so it is unverified. Check whether it binds OpenAI to the *PDPL*, not only to the GDPR, as Art. 23(1)(a) requires; a PDPL rider may be needed. | — |
| Azure OpenAI, in-country | **Standard** and **Regional Provisioned** process "within the customer-specified Azure geography". **Global** "may be processed in any Azure region". Data Zones exist only for US, EU and APAC; **there is no Middle East data zone**. Data at rest, including the abuse store, stays in the resource's geography. Models "do NOT interact with any services operated by … OpenAI". UAE North chat models in-region: Regional PTU only (2 Oct finding, S01). | [W24], [W25], S01 |

## 4. Bottom line: when a tenant's OpenAI key is lawful (*interpretation*)

**Lawful (class `globalAllowed`, `api.openai.com`), if all of these hold:**

1. The tenant is an onshore private company within the PDPL. It is not a government authority, not a GRE whose
   policies forbid offshore processing, not a CBUAE licensee, not a health-service provider, and not in DIFC or ADGM
   (those tenants follow their own SCC route).
2. The tenant, as data **controller**, gives a written instruction to enable the route. TICVAI is the processor.
   OpenAI is the tenant's own sub-processor under the tenant's own OpenAI contract and DPA. The tenant records its
   Art. 23 basis: a (a) contract binding OpenAI to PDPL-level duties, preferably plus (c) contract necessity for the
   guest-facing feature. Consent (b) is a fallback for optional features only.
3. The tenant holds a DPIA (Art. 21) and a privacy notice that names AI processing, the provider and the countries.
4. The scrubber is on, and no sensitive personal data enters prompts. Health, allergy and accessibility data,
   biometrics, religion, children's identity data, card data and Emirates ID images are excluded by field.
5. Recommended, not strictly required: OpenAI ZDR or Modified Abuse Monitoring is approved for the tenant's project,
   only stateless endpoints are used, and `store=false` is set.

**In-country alternative (class `uaeOnly`-eligible).** The tenant's key belongs to a **UAE-region** OpenAI project, the
base URL is `ae.api.openai.com`, and the model is on the UAE regional-processing list. This route is not a
cross-border transfer for inference. Before relying on it, verify in writing that system data and abuse logs also
stay in the UAE.

**Not lawful, or not without the entity's own written approval:**

- Federal, Abu Dhabi or Dubai government entities, and semi-government entities that must use certified providers.
- Any prompt with unscrubbed fields, or any call made while the scrubber has failed.
- Sensitive data, including health data under Law 2/2019.
- Images, audio or files, because the scrubber is text-only.
- OpenAI stateful features (Assistants, Threads, Conversations, file stores), and fine-tuning on tenant data.

## What this means for TICVAI

| # | Item | Decision / enforcement | Where |
|---|---|---|---|
| 1 | Residency class gate | `api.openai.com`, or any non-UAE endpoint, is selectable only when the tenant class is `globalAllowed`. `uaeOnly` accepts a BYOK OpenAI key only with `ae.api.openai.com` and a model from the UAE regional list. `onPrem` accepts none. | AI gateway, `setAiProvider` / `setAiCredential` |
| 2 | Tenant category | Staff record the tenant type (private, GRE, government, bank, health, DIFC, ADGM). `globalAllowed` cannot be set for any type except private. A GRE needs an uploaded written approval from the entity. | Tenant config, BO-1065 residency section |
| 3 | Enablement evidence | Store, before activation: the tenant's signed opt-in, the Art. 23 basis, the DPIA reference, the privacy-notice confirmation, and ZDR/MAM evidence (optional). Write all of it to the ADR-0009 §3 transfer register. | `setAiByokEnablement`, transfer register |
| 4 | Scrubber cannot be bypassed | Provider adapters accept only a scrubbed envelope signed by the scrubber step, never raw text. No flag, role or tenant setting turns scrubbing off. | Gateway contract (mandatory, already decided 2 Oct) |
| 5 | Fail closed | A scrubber error, timeout or missing recogniser blocks the call with no provider fallback. A residual pattern check after scrubbing (Emirates ID `784-…`, +971 phones, Luhn cards, IBAN, email) hard-blocks any hit. | Gateway |
| 6 | Field allow-list | Only allow-listed fields enter prompts. Sensitive fields (health, allergy, accessibility, biometric, religion, payment) are never sent to a global endpoint. Images, audio and files are blocked for `globalAllowed`. | Prompt builders per task |
| 7 | Token map stays in-cell | The map lives per request, with a short TTL, and is never logged in clear. Re-identification happens in-cell only. | Scrubber |
| 8 | Stateless calls only | No Assistants, Threads or Conversations, `store=false` on Responses, no file uploads, no fine-tuning with tenant data on global routes. | OpenAI adapter |
| 9 | Audit log | Each call records tenant, class, endpoint and region, model, scrubber version, entity counts by type (never values), the block or allow decision, and an outbound payload hash. The log can be exported to the tenant as controller. | Gateway, audit store |
| 10 | Failover never widens residency | `uaeOnly` never fails over to a global route (ADR-0034 `residencyRefused`). `globalAllowed` may fall back to the UAE chain. | Breaker |
| 11 | Instant revoke | The tenant can drop to `uaeOnly` at once and delete the key from Key Vault. | Admin |
| 12 | Vendor and legal to-dos | Read OpenAI's DPA for PDPL coverage and draft a PDPL rider. Get UAE regional processing details in writing (are system data and abuse logs kept in the UAE?). Apply for the Dubai AI Seal if Dubai government work is targeted. Get counsel on GRE status (Miral, Dubai Holding), already open from 2 Oct. Note that Presidio is now community-maintained (Data Privacy Stack), so pin the version and track releases. | Chinmay / legal |

Presidio's own documentation says "there is no guarantee that Presidio will find all sensitive information.
Consequently, additional systems and protections should be employed" ([W26]). Rows 5 and 6 are those additional
protections. Without them, the claim that personal data never leaves the UAE in clear cannot be made.

## Sources (read 3 October 2026 unless stated)

- [W1] PDPL English text (Arts. 1, 2, 4, 7, 20–23), LegalAdviceME mirror: https://legaladviceme.com/legislation/166/uae-federal-decree-law-45-2021-protection-personal-data. The official portal https://uaelegislation.gov.ae/en/legislations/1972 returned 403 to this session.
- [W2] DLA Piper, UAE data protection (last modified 27 Jan 2025): https://www.dlapiperdataprotection.com/countries/uae-general/law.html
- [W3] itsecnow, PDPL Executive Regulations status (checked 23 Sep 2026): https://itsecnow.com/regulators/pdpl-executive-regulations-2026
- [W4] Kayrouz & Associates, cross-border transfers under UAE law in 2026 (3 Feb 2026): https://www.kayrouzandassociates.com/insights/cross-border-data-transfers-under-uae-law-in-2026
- [W5] Chambers, Data Protection & Privacy 2026, UAE (10 Mar 2026): https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/uae/trends-and-developments
- [W6] GLA & Company, UAE AI and Data Authority (14 Jun 2026): https://www.glaco.com/blog/the-uae-artificial-intelligence-and-data-authority-what-it-means-for-ai-data-and-digital-governance/
- [W7] Eversheds Sutherland (Jun 2026): https://www.eversheds-sutherland.com/en/global/insights/uae-establishesthe-federal-artificial-intelligence-and-data-authority-june-2026 ; Dubai Media Office: https://x.com/DXBMediaOffice/status/2066082818187468975
- [W8] (uncorroborated claim, not relied on) https://orbit.reconn.io/uae-pdpl-complete-guide/
- [W9] A&O Shearman on CJEU C-413/23 P: https://www.aoshearman.com/en/insights/ao-shearman-on-data/cjeu-clarifies-concept-of-personal-data-for-a-transfer-of-pseudonymised-data-to-third-parties
- [W10] Clifford Chance, pseudonymised data after EDPS v SRB (Sep 2025): https://www.cliffordchance.com/insights/resources/blogs/talking-tech/en/articles/2025/09/pseudonymized-data-after-edps-v-srb.html
- [W11] DGE, Abu Dhabi Government Digital Strategy 2025–2027 (30 Sep 2025): https://www.dge.gov.ae/en/news/adg-digital-strategy-update-2025
- [W12] ADISS overview (scope incl. contractors): https://www.ampcuscyber.com/middle-east/uae/abu-dhabi-information-security-standards-controls/
- [W13] AWS, DESC CSP Security Standard: https://aws.amazon.com/compliance/desc_csp_security_standard/
- [W14] Dubai Law No. 26 of 2015 (Dubai Legislation Portal): https://dlp.dubai.gov.ae/Legislation%20Reference/2015/Law%20No.%20(26)%20of%202015.html
- [W15] Dubai AI Seal (DCAI), WAM: https://www.wam.ae/article/bhs9w8p-dubai-centre-for-artificial-intelligence-launches ; Gulf News "AI Seal now mandatory for UAE, Dubai government partnerships": https://gulfnews.com/amp/story/business%2Fmarkets%2Fai-seal-now-mandatory-for-uae-dubai-government-partnerships-1.500019234
- [W16] AWS, UAE Information Assurance Regulation: https://aws.amazon.com/compliance/UAE_IAR/ ; u.ae IAR page: https://u.ae/en/information-and-services/justice-safety-and-the-law/cyber-safety-and-digital-security/uae-information-assurance-regulation
- [W17] u.ae, National Cloud Security Policy (updated 18 Jun 2026): https://u.ae/en/about-the-uae/strategies-initiatives-and-awards/policies/cyber-activities/National-Cloud-Security-Policy
- [W18] Baker McKenzie, UAE Health Data Law permitted transfers: https://insightplus.bakermckenzie.com/bm/data-technology/united-arab-emirates-health-data-law-permitted-transfers-of-health-data
- [W19] UAE Charter for the Development and Use of AI (2024): https://ai.gov.ae/wp-content/uploads/2024/07/UAEAI-Methaq-EN2-3.pdf
- [W20] u.ae AI resources (23 Sep 2026): https://u.ae/en/about-the-uae/digital-uae/digital-technology/artificial-intelligence/ai-resources
- [W21] OpenAI, data controls in the OpenAI platform: https://developers.openai.com/api/docs/guides/your-data
- [W22] Middle East AI News, OpenAI UAE inference residency (12 Aug 2026): https://www.middleeastainews.com/p/openai-now-offers-inference-residency
- [W23] TechCrunch, Stargate UAE (22 May 2025): https://techcrunch.com/2025/05/22/openai-teams-up-with-cisco-oracle-to-build-uae-data-center
- [W24] Microsoft Learn, data, privacy and security for models sold by Azure (18 May 2026): https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy
- [W25] Microsoft Learn, deployment types (updated 12 Aug 2026): https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types
- [W26] Presidio documentation (now Data Privacy Stack): https://presidio.dataprivacystack.org/
