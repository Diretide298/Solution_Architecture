# Client design packs

**The 44 reference documents the contracts were drafted from, added 8 September 2026.**

These are the source for the package's provisional operations. 577 of the 1,626 operations carry
`x-ticvai-provisional: true` and a description citing its origin as `<pack>, page N` — and until
today those packs were not in the repository, so **a reader of the package alone could not check a
single citation.** They can now.

## What the citations say, audited 8 September

| | |
|---|---|
| Provisional operations | **577** |
| Citations resolving to a pack here | **577** |
| Citing a page beyond that pack's length | **0** |
| Distinct packs cited | 17 of 44 |
| Distinct pages cited | 573 |

**Not one fabricated citation and not one page number past the end of its book.** `provisional`
means *not yet agreed with whoever has to build it* — an honest label, not a defect.

## The gap is the other direction

**27 of the 44 packs have no operation drafted from them at all — 1,815 pages against the 1,058
that were used.** Largest untouched:

```
202pp  Retail_Backend_Structure_Module_Reference_v1.0.pdf
190pp  Payment_Payment_Orchestration.pdf
183pp  Upsell,CrossSellEngine.pdf
175pp  TICVAI_Inventory_and_Procurement_Backend_Structure_Sample v1.0.pdf
169pp  Resource_Management_Configuration_Reference.pdf
130pp  F&B_Backend_Structure_Module Sample Reference v1.0.pdf
129pp  Wallet_Configuration_Backend_Structure_v1.0.pdf
123pp  TICVAI Finance Backend Structure Reference v1.0.pdf
```

**This is CF-164 and CF-125 seen from the source side.** The F&B / Retail / Procurement / Inventory
workshop outstanding in three consecutive MoMs is exactly the material nobody has drafted from —
the package built 96 F&B operations off three *dashboard* packs while the 130-page F&B backend
structure reference sat unread.

Re-run the audit with `tools/audit-pack-citations.py`.
