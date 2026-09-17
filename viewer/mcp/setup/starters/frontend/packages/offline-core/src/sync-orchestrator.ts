/**
 * Sync orchestrator.
 *
 * Drains the outbox to the server, in order, with backpressure and automatic
 * mode switching. This is the piece the 31 Jul 2026 decision describes: the
 * system detects connectivity loss on its own, switches to offline mode without
 * operator intervention, restores automatically and flushes pending work.
 */

import type { SQLiteDatabase } from './sqlite';
import { Outbox, type OutboxEntry } from './outbox';

export type ConnectionMode = 'online' | 'offline' | 'syncing';

export interface SyncTransport {
  /**
   * Dispatches one entry. Implementations must send the entry id as the
   * `Idempotency-Key` header so a replay after a crash is a no-op server-side.
   */
  send(entry: OutboxEntry): Promise<SyncTransportResult>;
  /** Cheap liveness probe. Must not require auth — it runs while offline. */
  probe(): Promise<boolean>;
}

export interface SyncTransportResult {
  ok: boolean;
  /** HTTP status, when there was a response at all. */
  status?: number;
  /**
   * WAL LSN returned by the server on write. Carried on subsequent reads so a
   * lagging replica cannot serve stale data — a ticket sold at the gate must not
   * be refused seconds later.
   */
  consistencyToken?: string;
  error?: string;
}

export interface SyncState {
  mode: ConnectionMode;
  pending: number;
  rejected: number;
  lastSyncedAt: string | null;
  lastError: string | null;
  consistencyToken: string | null;
}

export interface SyncOrchestratorOptions {
  batchSize?: number;
  /** Probe interval while offline. */
  probeIntervalMs?: number;
  /** Drain interval while online with work outstanding. */
  drainIntervalMs?: number;
  baseBackoffMs?: number;
  maxBackoffMs?: number;
}

type Listener = (state: SyncState) => void;

const DEFAULTS: Required<SyncOrchestratorOptions> = {
  batchSize: 50,
  probeIntervalMs: 5_000,
  drainIntervalMs: 1_000,
  baseBackoffMs: 500,
  maxBackoffMs: 30_000,
};

export class SyncOrchestrator {
  private readonly options: Required<SyncOrchestratorOptions>;
  private readonly listeners = new Set<Listener>();

  private state: SyncState = {
    mode: 'offline',
    pending: 0,
    rejected: 0,
    lastSyncedAt: null,
    lastError: null,
    consistencyToken: null,
  };

  private timer: ReturnType<typeof setTimeout> | null = null;
  private draining = false;
  private stopped = true;
  private consecutiveFailures = 0;

  constructor(
    private readonly outbox: Outbox,
    private readonly transport: SyncTransport,
    options: SyncOrchestratorOptions = {},
  ) {
    this.options = { ...DEFAULTS, ...options };
  }

  static async create(
    db: SQLiteDatabase,
    transport: SyncTransport,
    options?: SyncOrchestratorOptions,
  ): Promise<SyncOrchestrator> {
    const outbox = new Outbox(db);
    await outbox.initialise();
    return new SyncOrchestrator(outbox, transport, options);
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  getState(): SyncState {
    return { ...this.state };
  }

  async start(): Promise<void> {
    if (!this.stopped) return;
    this.stopped = false;

    // Anything left in-flight belongs to a crashed or killed process. Safe to
    // replay because the server deduplicates on the entry ULID.
    const recovered = await this.outbox.recoverInFlight();
    if (recovered > 0) {
      await this.refreshCounts();
    }

    this.schedule(0);
  }

  stop(): void {
    this.stopped = true;
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
  }

  /** Forces an immediate drain — used by a manual "sync now" control. */
  async syncNow(): Promise<void> {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    await this.tick();
  }

  private schedule(delayMs: number): void {
    if (this.stopped) return;
    this.timer = setTimeout(() => {
      void this.tick();
    }, delayMs);
  }

  private async tick(): Promise<void> {
    if (this.stopped || this.draining) return;

    this.draining = true;
    try {
      const reachable = await this.probeSafely();

      if (!reachable) {
        this.emit({ mode: 'offline' });
        this.schedule(this.options.probeIntervalMs);
        return;
      }

      const batch = await this.outbox.peekBatch(this.options.batchSize);

      if (batch.length === 0) {
        this.emit({ mode: 'online', lastError: null });
        this.consecutiveFailures = 0;
        await this.refreshCounts();
        this.schedule(this.options.probeIntervalMs);
        return;
      }

      this.emit({ mode: 'syncing' });
      const halted = await this.drain(batch);
      await this.refreshCounts();

      // Sequential ordering is not an optimisation. A void arriving before the
      // sale it voids is rejected, and the device would retry it forever. So a
      // failure stops the batch rather than skipping past it.
      this.schedule(halted ? this.backoff() : this.options.drainIntervalMs);
    } finally {
      this.draining = false;
    }
  }

  private async drain(batch: readonly OutboxEntry[]): Promise<boolean> {
    await this.outbox.markInFlight(batch.map((entry) => entry.id));

    for (const entry of batch) {
      if (this.stopped) return true;

      let result: SyncTransportResult;
      try {
        result = await this.transport.send(entry);
      } catch (error) {
        result = { ok: false, error: error instanceof Error ? error.message : String(error) };
      }

      if (result.ok) {
        await this.outbox.markSynced(entry.id, new Date().toISOString());
        this.consecutiveFailures = 0;

        this.emit({
          lastSyncedAt: new Date().toISOString(),
          consistencyToken: result.consistencyToken ?? this.state.consistencyToken,
        });
        continue;
      }

      const permanent =
        result.status !== undefined &&
        result.status >= 400 &&
        result.status < 500 &&
        result.status !== 408 &&
        result.status !== 429;

      if (permanent) {
        // The server will never accept this. Surface it to the operator rather
        // than retrying behind an "all synced" indicator.
        await this.outbox.markRejected(entry.id, result.error ?? `HTTP ${result.status}`);
        this.emit({ lastError: result.error ?? `Rejected: HTTP ${result.status}` });
        continue;
      }

      await this.outbox.markFailed(entry.id, result.error ?? 'Transport failure');
      this.consecutiveFailures += 1;
      this.emit({ lastError: result.error ?? 'Transport failure' });
      return true;
    }

    return false;
  }

  private async probeSafely(): Promise<boolean> {
    try {
      return await this.transport.probe();
    } catch {
      return false;
    }
  }

  private backoff(): number {
    const exponential = this.options.baseBackoffMs * 2 ** Math.min(this.consecutiveFailures, 10);
    const capped = Math.min(exponential, this.options.maxBackoffMs);
    // Jitter prevents every terminal in a venue retrying in lockstep after a
    // network blip and re-creating the outage on recovery.
    return Math.round(capped * (0.5 + Math.random() * 0.5));
  }

  private async refreshCounts(): Promise<void> {
    const [pending, rejected] = await Promise.all([
      this.outbox.pendingCount(),
      this.outbox.rejected().then((entries) => entries.length),
    ]);
    this.emit({ pending, rejected });
  }

  private emit(patch: Partial<SyncState>): void {
    this.state = { ...this.state, ...patch };
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }
}
