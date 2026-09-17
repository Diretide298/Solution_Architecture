/**
 * SQLite adapter boundary.
 *
 * Apps must never import a SQLite driver directly — the lint rule in
 * `.eslintrc.json` bans `expo-sqlite`, `react-native-sqlite-storage` and
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
   * Runs `work` inside a transaction, rolling back on throw.
   *
   * The outbox drain relies on this: marking a batch in-flight and dispatching
   * it must not interleave with an enqueue from the sale screen.
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
