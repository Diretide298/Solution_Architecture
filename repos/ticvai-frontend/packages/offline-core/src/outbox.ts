/**
 * Offline outbox.
 *
 * Every mutating operation on POS, scanner and employee apps is written here
 * first, then drained to the server. This is the single implementation for all
 * six apps — six copies of a sync engine is six divergent bug surfaces, which is
 * the reason the frontend is a monorepo while the runtimes are not.
 *
 * Guarantees, from the 31 Jul 2026 offline architecture decision:
 *   - sequential per device, preserving order
 *   - both recorded and synced timestamps retained
 *   - idempotent on the server via a client-generated ULID
 *   - automatic mode detection, automatic flush on reconnect
 */

import type { SQLiteDatabase } from './sqlite';
import { newUlid } from './ulid';

export type OutboxStatus = 'pending' | 'inFlight' | 'synced' | 'failed' | 'rejected';

/** Declared per entity. There is no global default — see `ConflictPolicy` notes. */
export type ConflictPolicy =
  /** Sales and scans: never conflict, the server appends. */
  | 'append'
  /** Configuration: the server's version wins, the local change is discarded. */
  | 'serverWins'
  /** Requires human resolution; surfaced in the UI rather than resolved silently. */
  | 'manual';

export interface OutboxEntry {
  /** Client-generated ULID. Also the server-side idempotency key. */
  id: string;
  /** Monotonic per device. Preserves ordering across a batch. */
  sequence: number;
  entity: string;
  operation: 'create' | 'update' | 'delete';
  endpoint: string;
  method: 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  payload: unknown;
  conflictPolicy: ConflictPolicy;
  status: OutboxStatus;
  /** When the device recorded it. Not when the server received it. */
  recordedAt: string;
  syncedAt: string | null;
  attempts: number;
  lastError: string | null;
  /** Denormalised for scoping and for surfacing failures per venue. */
  venueId: string;
  workstationId: string;
}

export interface EnqueueRequest {
  entity: string;
  operation: OutboxEntry['operation'];
  endpoint: string;
  method: OutboxEntry['method'];
  payload: unknown;
  conflictPolicy: ConflictPolicy;
  venueId: string;
  workstationId: string;
}

const MAX_ATTEMPTS = 8;

export class Outbox {
  constructor(private readonly db: SQLiteDatabase) {}

  async initialise(): Promise<void> {
    await this.db.exec(`
      CREATE TABLE IF NOT EXISTS outbox (
        id              TEXT PRIMARY KEY,
        sequence        INTEGER NOT NULL,
        entity          TEXT NOT NULL,
        operation       TEXT NOT NULL,
        endpoint        TEXT NOT NULL,
        method          TEXT NOT NULL,
        payload         TEXT NOT NULL,
        conflict_policy TEXT NOT NULL,
        status          TEXT NOT NULL,
        recorded_at     TEXT NOT NULL,
        synced_at       TEXT,
        attempts        INTEGER NOT NULL DEFAULT 0,
        last_error      TEXT,
        venue_id        TEXT NOT NULL,
        workstation_id  TEXT NOT NULL
      );

      CREATE INDEX IF NOT EXISTS outbox_pending
        ON outbox (status, sequence)
        WHERE status IN ('pending', 'failed');

      CREATE TABLE IF NOT EXISTS outbox_sequence (
        id       INTEGER PRIMARY KEY CHECK (id = 1),
        next_val INTEGER NOT NULL
      );

      INSERT OR IGNORE INTO outbox_sequence (id, next_val) VALUES (1, 1);
    `);
  }

  /**
   * Writes an operation to the outbox. Returns immediately — the caller does not
   * wait on the network. The UI treats the local write as authoritative and
   * reconciles later, which is what makes offline selling feel instantaneous.
   */
  async enqueue(request: EnqueueRequest): Promise<OutboxEntry> {
    const id = newUlid();
    const sequence = await this.nextSequence();
    const recordedAt = new Date().toISOString();

    const entry: OutboxEntry = {
      id,
      sequence,
      entity: request.entity,
      operation: request.operation,
      endpoint: request.endpoint,
      method: request.method,
      payload: request.payload,
      conflictPolicy: request.conflictPolicy,
      status: 'pending',
      recordedAt,
      syncedAt: null,
      attempts: 0,
      lastError: null,
      venueId: request.venueId,
      workstationId: request.workstationId,
    };

    await this.db.run(
      `INSERT INTO outbox (
         id, sequence, entity, operation, endpoint, method, payload,
         conflict_policy, status, recorded_at, attempts, venue_id, workstation_id
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        id,
        sequence,
        entry.entity,
        entry.operation,
        entry.endpoint,
        entry.method,
        JSON.stringify(entry.payload),
        entry.conflictPolicy,
        entry.status,
        recordedAt,
        0,
        entry.venueId,
        entry.workstationId,
      ],
    );

    return entry;
  }

  /**
   * Next batch to drain, in strict sequence order.
   *
   * Ordering is not an optimisation. A void that reaches the server before the
   * sale it voids will be rejected, and the device will retry forever.
   */
  async peekBatch(limit = 50): Promise<OutboxEntry[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM outbox
        WHERE status IN ('pending', 'failed')
          AND attempts < ?
        ORDER BY sequence ASC
        LIMIT ?`,
      [MAX_ATTEMPTS, limit],
    );

    return rows.map(toEntry);
  }

  async markInFlight(ids: readonly string[]): Promise<void> {
    if (ids.length === 0) return;
    const placeholders = ids.map(() => '?').join(',');
    await this.db.run(
      `UPDATE outbox SET status = 'inFlight' WHERE id IN (${placeholders})`,
      [...ids],
    );
  }

  async markSynced(id: string, syncedAt: string): Promise<void> {
    await this.db.run(
      `UPDATE outbox SET status = 'synced', synced_at = ?, last_error = NULL WHERE id = ?`,
      [syncedAt, id],
    );
  }

  /**
   * Records a transient failure. Entries past MAX_ATTEMPTS stop retrying and are
   * surfaced to the operator — silently retrying forever hides a real problem
   * behind an "all synced" indicator.
   */
  async markFailed(id: string, error: string): Promise<void> {
    await this.db.run(
      `UPDATE outbox
          SET status = CASE WHEN attempts + 1 >= ? THEN 'rejected' ELSE 'failed' END,
              attempts = attempts + 1,
              last_error = ?
        WHERE id = ?`,
      [MAX_ATTEMPTS, error, id],
    );
  }

  /** Permanent server rejection — a 4xx that retrying cannot fix. */
  async markRejected(id: string, error: string): Promise<void> {
    await this.db.run(
      `UPDATE outbox SET status = 'rejected', last_error = ? WHERE id = ?`,
      [error, id],
    );
  }

  async pendingCount(): Promise<number> {
    const row = await this.db.get<{ count: number }>(
      `SELECT COUNT(*) AS count FROM outbox WHERE status IN ('pending', 'failed', 'inFlight')`,
    );
    return row?.count ?? 0;
  }

  /** Entries needing operator attention. Surfaced in the sync status UI. */
  async rejected(): Promise<OutboxEntry[]> {
    const rows = await this.db.all<Record<string, unknown>>(
      `SELECT * FROM outbox WHERE status = 'rejected' ORDER BY sequence ASC`,
    );
    return rows.map(toEntry);
  }

  /** Retains synced entries briefly for audit and support before pruning. */
  async pruneSynced(olderThan: Date): Promise<number> {
    const result = await this.db.run(
      `DELETE FROM outbox WHERE status = 'synced' AND synced_at < ?`,
      [olderThan.toISOString()],
    );
    return result.changes;
  }

  /**
   * Recovers entries stranded in `inFlight` by a crash or a kill mid-drain.
   * Safe to replay because the server deduplicates on the entry's ULID.
   */
  async recoverInFlight(): Promise<number> {
    const result = await this.db.run(
      `UPDATE outbox SET status = 'pending' WHERE status = 'inFlight'`,
    );
    return result.changes;
  }

  private async nextSequence(): Promise<number> {
    await this.db.run(`UPDATE outbox_sequence SET next_val = next_val + 1 WHERE id = 1`);
    const row = await this.db.get<{ next_val: number }>(
      `SELECT next_val FROM outbox_sequence WHERE id = 1`,
    );

    if (!row) {
      throw new Error('Outbox sequence row missing. Call initialise() first.');
    }

    return row.next_val - 1;
  }
}

function toEntry(row: Record<string, unknown>): OutboxEntry {
  return {
    id: row.id as string,
    sequence: row.sequence as number,
    entity: row.entity as string,
    operation: row.operation as OutboxEntry['operation'],
    endpoint: row.endpoint as string,
    method: row.method as OutboxEntry['method'],
    payload: JSON.parse(row.payload as string),
    conflictPolicy: row.conflict_policy as ConflictPolicy,
    status: row.status as OutboxStatus,
    recordedAt: row.recorded_at as string,
    syncedAt: (row.synced_at as string | null) ?? null,
    attempts: row.attempts as number,
    lastError: (row.last_error as string | null) ?? null,
    venueId: row.venue_id as string,
    workstationId: row.workstation_id as string,
  };
}
