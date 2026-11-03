/**
 * SQLite adapter boundary.
 *
 * Apps must never import a SQLite driver directly — the lint rule in
 * `.eslintrc.cjs` bans `expo-sqlite`, `react-native-sqlite-storage` and
 * `@op-engineering/op-sqlite` from app code. Everything goes through this
 * interface so the driver can be swapped once, in one place.
 */

export interface RunResult {
  /** Rows affected. */
  changes: number;
  lastInsertRowId: number | null;
}

export interface SQLiteDatabase {
  exec(sql: string): Promise<void>;
  run(sql: string, params?: readonly unknown[]): Promise<RunResult>;
  get<T>(sql: string, params?: readonly unknown[]): Promise<T | null>;
  all<T>(sql: string, params?: readonly unknown[]): Promise<T[]>;
  /**
   * Runs `work` inside a transaction, rolling back on throw. Statements on `tx` are the
   * transaction's; implement it exclusively (expo-sqlite's withExclusiveTransactionAsync,
   * not withTransactionAsync), so another statement on the connection waits for it.
   *
   * The outbox relies on this: `enqueue` allocates an entry's sequence and inserts the
   * entry in one transaction, so two enqueues never share a sequence (the outbox's
   * UNIQUE(sequence) index turns a race that gets through into an error, not a duplicate).
   */
  transaction<T>(work: (tx: SQLiteDatabase) => Promise<T>): Promise<T>;
  close(): Promise<void>;
}

export interface SQLiteDriver {
  open(name: string): Promise<SQLiteDatabase>;
}

let registered: SQLiteDriver | null = null;

/** Called once at app bootstrap with the platform driver. */
export function registerDriver(driver: SQLiteDriver): void {
  registered = driver;
}

export async function openDatabase(name: string): Promise<SQLiteDatabase> {
  if (!registered) {
    throw new Error(
      'No SQLite driver registered. Call registerDriver() during app bootstrap ' +
        'before opening the offline database.',
    );
  }
  return registered.open(name);
}
