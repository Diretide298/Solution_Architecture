# Data & Storage

## 6. SQL & Migrations

| Rule | Detail |
|---|---|
| Forward-only, numbered, checksummed | `V0001__baseline.sql` |
| Every migration is reversible or documented as irreversible | Runs across every cell |
| **Test rollback before merge** | Not after |
| No `SELECT *` | Explicit columns |
| Every foreign key indexed | — |
| `ENABLE` **and** `FORCE ROW LEVEL SECURITY` | Without FORCE the owner bypasses every policy |
| Partition key in the primary key | Required on partitioned tables |
| Comment the non-obvious | `COMMENT ON COLUMN` for anything a newcomer would misread |

Long-running DDL uses `CONCURRENTLY` where available. A migration holding a lock on
`sales_order` during trading is an outage across every venue in the cell.

---

