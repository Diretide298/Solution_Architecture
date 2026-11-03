/**
 * Sync orchestrator.
 *
 * Drains the outbox to the server, in order, with backpressure and automatic
 * mode switching. This is the piece the 31 Jul 2026 decision describes: the
 * system detects connectivity loss on its own, switches to offline mode without
 * operator intervention, restores automatically and flushes pending work.
 *
 * One orchestrator drains one database. Two draining the same outbox (two tabs, two
 * processes) would each send entries and lose the per-device order.
 */

import type { SQLiteDatabase } from './sqlite';
import { Outbox, type OutboxEntry } from './outbox';

/**
 * `halted`: the server is reachable but a transient failure stopped the drain at
 * `SyncState.stoppedAtSequence`. Nothing after that entry is sent until it succeeds.
 */
export type ConnectionMode = 'online' | 'offline' | 'syncing' | 'halted';

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
  /**
   * The server's time it accepted the write, taken from the answer: the `syncedAt` a
   * resource's body carries where the server stamps it on arrival. The contracts have no
   * general server-time field (syncOrders' OrderSyncResult has none), so leave it out when
   * the answer has none; the outbox then records no syncedAt rather than the device's clock.
   */
  syncedAt?: string;
  error?: string;
}

export interface SyncState {
  mode: ConnectionMode;
  /** Entries not yet accepted: pending, failed (to retry) or in flight. */
  pending: number;
  rejected: number;
  /** The device's time of the last acceptance (the device's clock, for the indicator). */
  lastDeviceAckedAt: string | null;
  lastError: string | null;
  /**
   * The sequence of the entry a transient failure stopped the drain at; nothing after it is
   * sent until it succeeds or is rejected. Null when the drain is not held.
   */
  stoppedAtSequence: number | null;
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
  /**
   * ADR-0022 `serverWins`: the server's version stands, "the client's write is rejected and
   * the client re-reads". Called once for each `serverWins` entry the server rejects
   * permanently (a 4xx other than 408/429), after the entry is marked `rejected`. The app
   * re-reads what the entry wrote (refetch the record, refresh the local bundle) and tells
   * the user. A throw is surfaced as `lastError`; it does not stop the drain.
   */
  onServerWins?: (entry: OutboxEntry, result: SyncTransportResult) => void | Promise<void>;
}

type Listener = (state: SyncState) => void;

type Timings = Required<Omit<SyncOrchestratorOptions, 'onServerWins'>>;

const DEFAULTS: Timings = {
  batchSize: 50,
  probeIntervalMs: 5_000,
  drainIntervalMs: 1_000,
  baseBackoffMs: 500,
  maxBackoffMs: 30_000,
};

export class SyncOrchestrator {
  private readonly options: Timings;
  private readonly onServerWins: SyncOrchestratorOptions['onServerWins'];
  private readonly listeners = new Set<Listener>();

  private state: SyncState = {
    mode: 'offline',
    pending: 0,
    rejected: 0,
    lastDeviceAckedAt: null,
    lastError: null,
    stoppedAtSequence: null,
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
    const { onServerWins, ...timings } = options;
    this.options = { ...DEFAULTS, ...timings };
    this.onServerWins = onServerWins;
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
    await this.refreshCounts();
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

      // None of this orchestrator's sends is outstanding here (`draining` guards it), so an
      // entry still inFlight was stranded by a crash, a kill or a database error between
      // sending and recording the answer. Put it back first so the batch starts from it.
      await this.outbox.recoverInFlight();

      const batch = await this.outbox.peekBatch(this.options.batchSize);

      if (batch.length === 0) {
        await this.refreshCounts();
        if (this.state.pending === 0) {
          this.consecutiveFailures = 0;
          this.emit({ mode: 'online', lastError: null, stoppedAtSequence: null });
          this.schedule(this.options.probeIntervalMs);
        } else {
          // Never "online, no error" while entries wait.
          this.emit({ mode: 'halted', lastError: `${this.state.pending} entries could not be drained` });
          this.schedule(this.backoff());
        }
        return;
      }

      this.emit({ mode: 'syncing' });
      const halted = await this.drain(batch);
      await this.refreshCounts();

      // Sequential ordering is not an optimisation. A void arriving before the
      // sale it voids is rejected, and the device would retry it forever. So a
      // transient failure stops the batch rather than skipping past it, and the
      // entries after it stay pending, behind it.
      if (halted) this.emit({ mode: 'halted' });
      this.schedule(halted ? this.backoff() : this.options.drainIntervalMs);
    } catch (error) {
      // A database error mid-drain. Say so and retry; never stop scheduling silently.
      this.consecutiveFailures += 1;
      this.emit({ mode: 'halted', lastError: messageOf(error) });
      this.schedule(this.backoff());
    } finally {
      this.draining = false;
    }
  }

  /** Sends the batch in sequence order, one entry in flight at a time. Returns true on a halt. */
  private async drain(batch: readonly OutboxEntry[]): Promise<boolean> {
    for (const entry of batch) {
      if (this.stopped) return false;

      // Only the entry about to be sent is inFlight. The rest of the batch stays pending,
      // so a halt leaves it where the next drain picks it up, in order, behind this one.
      await this.outbox.markInFlight([entry.id]);

      let result: SyncTransportResult;
      try {
        result = await this.transport.send(entry);
      } catch (error) {
        result = { ok: false, error: messageOf(error) };
      }

      if (result.ok) {
        const deviceAckedAt = new Date().toISOString();
        await this.outbox.markSynced(entry.id, result.syncedAt ?? null, deviceAckedAt);
        this.consecutiveFailures = 0;

        this.emit({
          lastDeviceAckedAt: deviceAckedAt,
          stoppedAtSequence: null,
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
        // than retrying behind an "all synced" indicator, and carry on: the server
        // quarantines what depends on it (a void of a rejected sale), so a bad entry
        // never halts the till.
        await this.outbox.markRejected(entry.id, result.error ?? `HTTP ${result.status}`);
        this.emit({ lastError: result.error ?? `Rejected: HTTP ${result.status}`, stoppedAtSequence: null });
        await this.afterRejection(entry, result);
        continue;
      }

      await this.outbox.markFailed(entry.id, result.error ?? 'Transport failure');
      this.consecutiveFailures += 1;
      this.emit({ lastError: result.error ?? 'Transport failure', stoppedAtSequence: entry.sequence });
      return true;
    }

    return false;
  }

  /** What a permanent rejection means under the entry's declared policy (ADR-0022). */
  private async afterRejection(entry: OutboxEntry, result: SyncTransportResult): Promise<void> {
    const policy = entry.conflictPolicy;
    switch (policy) {
      case 'serverWins':
        // The server's version stands; the client re-reads and tells the user.
        if (!this.onServerWins) return;
        try {
          await this.onServerWins(entry, result);
        } catch (error) {
          this.emit({ lastError: `Re-read after a serverWins rejection failed: ${messageOf(error)}` });
        }
        return;
      // append: nothing is overwritten, so nothing to reconcile; the rejection is on its merits.
      // lastWriterWins: the server keeps the later recordedAt; not a conflict the client settles.
      // manualMerge: a human resolves it, from rejected() in the sync status UI.
      case 'append':
      case 'lastWriterWins':
      case 'manualMerge':
        return;
      default: {
        const unknown: never = policy;
        this.emit({ lastError: `Unknown conflict policy ${String(unknown)} on entry ${entry.id}` });
      }
    }
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

function messageOf(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}
