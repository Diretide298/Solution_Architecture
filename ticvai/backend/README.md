# backend/ — the versioned SQL

**Empty, and that is the state of the project rather than an omission.** 379 tables specified, none
written as DDL. **This folder filling up is the milestone.**

Blocked by CF-64 (cloud provider) and **CF-161** — a 24 August workshop decision that databases are
segregated per service from day one, contradicting ADR-0005 and ADR-0028. **Writing DDL against an
undecided topology is writing it twice.**
