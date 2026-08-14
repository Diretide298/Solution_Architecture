# Privacy And Dsar

> **Purpose:** Erasure against an append-only ledger  
> **Owner:** Chinmay  
> **Status:** **Week 2**

PII lives in a separate erasable store, referenced from the ledger by an opaque subject ID.
Erasure deletes the PII record; the ledger keeps its integrity and its audit trail with an
orphaned but valid reference.

**DSAR is orchestrated from the Control Plane, fanning out across a tenant's cells** — a
guest who visited two jurisdictions exists in two cells.
