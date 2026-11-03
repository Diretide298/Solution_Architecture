/**
 * In-memory SQLite for the package's tests, behind the package's own SQLiteDatabase
 * interface. Test support only: not exported from index.ts, never shipped to an app.
 *
 * Uses node:sqlite (Node 22.5+, no dependency). It is loaded at run time so the package's
 * typecheck needs no Node types. Every statement yields to the event loop first, as a native
 * async driver does, so tests see the interleavings a device sees.
 */

import type { RunResult, SQLiteDatabase } from './sqlite';

interface NodeStatement {
  run(...params: unknown[]): { changes: number | bigint; lastInsertRowid: number | bigint };
  get(...params: unknown[]): unknown;
  all(...params: unknown[]): unknown[];
}

/** The part of node:sqlite's DatabaseSync the adapter uses. */
export interface NodeDatabaseSync {
  exec(sql: string): void;
  prepare(sql: string): NodeStatement;
  close(): void;
}

export interface MemoryDatabase extends SQLiteDatabase {
  /** The synchronous handle, for a test to read rows without going through the adapter. */
  readonly raw: NodeDatabaseSync;
}

export interface MemoryDatabaseOptions {
  /**
   * true (the default): `transaction` is exclusive, as sqlite.ts asks of a driver; other
   * statements on the connection wait for it.
   * false: `transaction` just runs `work` on the connection and holds nothing off, like
   * expo-sqlite's withTransactionAsync or the review harness. The outbox must stay correct
   * on such a driver too.
   */
  exclusiveTransactions?: boolean;
}

export async function openMemoryDatabase(options: MemoryDatabaseOptions = {}): Promise<MemoryDatabase> {
  // process.getBuiltinModule (Node 22.3+), not import: vite 5 does not know node:sqlite as a
  // builtin and would try to resolve it as a file.
  const host = globalThis as unknown as { process?: { getBuiltinModule?: (id: string) => unknown } };
  const sqlite = host.process?.getBuiltinModule?.('node:sqlite') as
    | { DatabaseSync: new (path: string) => NodeDatabaseSync }
    | undefined;
  if (!sqlite) {
    throw new Error('These tests need node:sqlite: run them on Node 22.5 or later.');
  }
  const raw = new sqlite.DatabaseSync(':memory:');
  const exclusive = options.exclusiveTransactions ?? true;

  // One connection: an exclusive transaction holds this lock from BEGIN to COMMIT, and every
  // statement outside a transaction takes it for itself.
  let tail: Promise<unknown> = Promise.resolve();
  const locked = <T>(work: () => Promise<T>): Promise<T> => {
    const run = tail.then(work);
    tail = run.catch(() => undefined);
    return run;
  };

  const step = async <T>(work: () => T): Promise<T> => {
    await new Promise<void>((resolve) => setTimeout(resolve, 0));
    return work();
  };

  const statements = {
    exec: (sql: string) => step(() => void raw.exec(sql)),
    run: (sql: string, params: readonly unknown[] = []) =>
      step((): RunResult => {
        const result = raw.prepare(sql).run(...params);
        return { changes: Number(result.changes), lastInsertRowId: Number(result.lastInsertRowid) };
      }),
    get: <T>(sql: string, params: readonly unknown[] = []) =>
      step(() => (raw.prepare(sql).get(...params) as T | undefined) ?? null),
    all: <T>(sql: string, params: readonly unknown[] = []) =>
      step(() => raw.prepare(sql).all(...params) as T[]),
  };

  const inTransaction: MemoryDatabase = {
    raw,
    exec: statements.exec,
    run: statements.run,
    get: statements.get,
    all: statements.all,
    transaction: (work) => work(inTransaction),
    close: async () => raw.close(),
  };

  const db: MemoryDatabase = {
    raw,
    exec: (sql) => locked(() => statements.exec(sql)),
    run: (sql, params) => locked(() => statements.run(sql, params)),
    get: <T>(sql: string, params?: readonly unknown[]) => locked(() => statements.get<T>(sql, params)),
    all: <T>(sql: string, params?: readonly unknown[]) => locked(() => statements.all<T>(sql, params)),
    transaction: <T>(work: (tx: SQLiteDatabase) => Promise<T>): Promise<T> => {
      if (!exclusive) return work(db);
      return locked(async () => {
        await statements.exec('BEGIN IMMEDIATE');
        try {
          const result = await work(inTransaction);
          raw.exec('COMMIT');
          return result;
        } catch (error) {
          raw.exec('ROLLBACK');
          throw error;
        }
      });
    },
    close: async () => raw.close(),
  };

  return db;
}
