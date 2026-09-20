-- Extensions, applied before any table.
-- **Derived by tools/derive-ddl.py. Do not hand-edit.**
--
-- **Numbered 001 so it sorts before 010-*.** `ltree` is used by the scope index and the
-- row-level-security predicate, so it cannot arrive after the tables that depend on it.
-- This is why the machinery could not be a `V*.sql` file living beside the numeric series:
-- digits sort before letters, and the security layer would have applied last.

-- ltree carries the scope tree. GiST indexes its containment operators, which is what makes
-- `<@` cheap enough to sit inside every policy on every table.
CREATE EXTENSION IF NOT EXISTS ltree;
CREATE EXTENSION IF NOT EXISTS btree_gist;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
