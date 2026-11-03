import { afterEach, describe, expect, it } from 'vitest';
import { Outbox, type ConflictPolicy, type EnqueueRequest, type OutboxEntry } from './outbox';
import { SyncOrchestrator, type SyncTransportResult } from './sync-orchestrator';
import { openMemoryDatabase, type MemoryDatabase } from './memory-sqlite.test-support';

function request(entity: string, conflictPolicy: ConflictPolicy = 'append'): EnqueueRequest {
  return {
    entity,
    operation: 'create',
    endpoint: '/orders',
    method: 'POST',
    payload: { entity },
    conflictPolicy,
    venueId: 'venue-1',
    workstationId: 'till-1',
  };
}

interface Row {
  entity: string;
  sequence: number;
  status: string;
  attempts: number;
  synced_at: string | null;
  device_acked_at: string | null;
}

function rows(db: MemoryDatabase): Row[] {
  return db.raw
    .prepare('SELECT entity, sequence, status, attempts, synced_at, device_acked_at FROM outbox ORDER BY sequence')
    .all() as Row[];
}

const statusOf = (db: MemoryDatabase) => Object.fromEntries(rows(db).map((row) => [row.entity, row.status]));

/** A transport that answers each send from `answer`, recording what reached it and what was inFlight. */
function transport(db: MemoryDatabase, answer: (entry: OutboxEntry, attempt: number) => SyncTransportResult) {
  const attempts: string[] = [];
  const accepted: string[] = [];
  const inFlightDuringSend: string[][] = [];
  const counts = new Map<string, number>();
  return {
    attempts,
    accepted,
    inFlightDuringSend,
    probe: async () => true,
    send: async (entry: OutboxEntry): Promise<SyncTransportResult> => {
      inFlightDuringSend.push(
        (db.raw.prepare(`SELECT entity FROM outbox WHERE status = 'inFlight'`).all() as { entity: string }[]).map(
          (row) => row.entity,
        ),
      );
      const attempt = (counts.get(entry.entity) ?? 0) + 1;
      counts.set(entry.entity, attempt);
      attempts.push(entry.entity);
      const result = answer(entry, attempt);
      if (result.ok) accepted.push(entry.entity);
      return result;
    },
  };
}

// Timers far off: each drain is driven by syncNow, nothing runs behind the test's back.
const QUIET = { probeIntervalMs: 1e9, drainIntervalMs: 1e9, baseBackoffMs: 1e9, maxBackoffMs: 1e9 };

const running: SyncOrchestrator[] = [];
afterEach(() => {
  while (running.length) running.pop()?.stop();
});

async function setUp(
  answer: (entry: OutboxEntry, attempt: number) => SyncTransportResult,
  options: ConstructorParameters<typeof SyncOrchestrator>[2] = {},
) {
  const db = await openMemoryDatabase();
  const outbox = new Outbox(db);
  await outbox.initialise();
  const wire = transport(db, answer);
  const orchestrator = new SyncOrchestrator(outbox, wire, { ...QUIET, ...options });
  running.push(orchestrator);
  return { db, outbox, wire, orchestrator };
}

describe('SyncOrchestrator, a transient failure', () => {
  it('keeps strict sequence order: sale-A fails once, then sale-B, sale-C and void-B follow it, none skipped', async () => {
    const { db, outbox, wire, orchestrator } = await setUp((entry, attempt) =>
      entry.entity === 'sale-A' && attempt === 1 ? { ok: false, status: 503, error: 'busy' } : { ok: true },
    );
    for (const entity of ['sale-A', 'sale-B', 'sale-C']) await outbox.enqueue(request(entity));
    await orchestrator.start();

    await orchestrator.syncNow();
    expect(statusOf(db)).toEqual({ 'sale-A': 'failed', 'sale-B': 'pending', 'sale-C': 'pending' });
    const sequenceOfA = rows(db)[0]?.sequence;
    expect(orchestrator.getState()).toMatchObject({
      mode: 'halted',
      lastError: 'busy',
      stoppedAtSequence: sequenceOfA,
      pending: 3,
    });

    await outbox.enqueue(request('void-B')); // depends on sale-B
    await orchestrator.syncNow();
    await orchestrator.syncNow();

    expect(wire.attempts).toEqual(['sale-A', 'sale-A', 'sale-B', 'sale-C', 'void-B']);
    expect(wire.accepted).toEqual(['sale-A', 'sale-B', 'sale-C', 'void-B']);
    expect(statusOf(db)).toEqual({ 'sale-A': 'synced', 'sale-B': 'synced', 'sale-C': 'synced', 'void-B': 'synced' });
    expect(orchestrator.getState()).toMatchObject({ mode: 'online', lastError: null, stoppedAtSequence: null, pending: 0 });
  });

  it('treats a thrown send (no response) as transient too', async () => {
    let down = true;
    const { db, outbox, wire, orchestrator } = await setUp(() => {
      if (down) throw new Error('socket hang up');
      return { ok: true };
    });
    await outbox.enqueue(request('sale-A'));
    await outbox.enqueue(request('sale-B'));
    await orchestrator.start();

    await orchestrator.syncNow();
    expect(statusOf(db)).toEqual({ 'sale-A': 'failed', 'sale-B': 'pending' });
    expect(orchestrator.getState()).toMatchObject({ mode: 'halted', lastError: 'socket hang up' });

    down = false;
    await orchestrator.syncNow();
    expect(wire.accepted).toEqual(['sale-A', 'sale-B']);
  });

  it('never leaves the rest of the batch inFlight: one entry in flight at a time, none stranded after a halt', async () => {
    const { db, outbox, wire, orchestrator } = await setUp((entry, attempt) =>
      entry.entity === 'sale-B' && attempt === 1 ? { ok: false, status: 502 } : { ok: true },
    );
    for (const entity of ['sale-A', 'sale-B', 'sale-C', 'sale-D']) await outbox.enqueue(request(entity));
    await orchestrator.start();

    await orchestrator.syncNow();
    expect(wire.inFlightDuringSend).toEqual([['sale-A'], ['sale-B']]);
    expect(rows(db).filter((row) => row.status === 'inFlight')).toEqual([]);
    expect(statusOf(db)).toEqual({ 'sale-A': 'synced', 'sale-B': 'failed', 'sale-C': 'pending', 'sale-D': 'pending' });

    await orchestrator.syncNow();
    expect(wire.accepted).toEqual(['sale-A', 'sale-B', 'sale-C', 'sale-D']);
  });

  it('sends an entry a crash left inFlight before anything after it', async () => {
    const { db, outbox, wire, orchestrator } = await setUp(() => ({ ok: true }));
    const crashed = await outbox.enqueue(request('sale-A'));
    await outbox.enqueue(request('sale-B'));
    await outbox.markInFlight([crashed.id]); // the process died mid-send

    await orchestrator.start();
    await orchestrator.syncNow();

    expect(wire.accepted).toEqual(['sale-A', 'sale-B']);
    expect(rows(db).every((row) => row.status === 'synced')).toBe(true);
  });

  it('rejects an entry after MAX_ATTEMPTS transient failures and surfaces it, then drains past it', async () => {
    const { db, outbox, wire, orchestrator } = await setUp((entry) =>
      entry.entity === 'sale-A' ? { ok: false, status: 503 } : { ok: true },
    );
    await outbox.enqueue(request('sale-A'));
    await outbox.enqueue(request('sale-B'));
    await orchestrator.start();

    for (let i = 0; i < 8; i += 1) await orchestrator.syncNow();
    expect(wire.accepted).toEqual([]);
    expect(rows(db)[0]).toMatchObject({ entity: 'sale-A', status: 'rejected', attempts: 8 });

    await orchestrator.syncNow();
    expect(wire.accepted).toEqual(['sale-B']);
    expect(orchestrator.getState()).toMatchObject({ rejected: 1, pending: 0 });
  });
});

describe('SyncOrchestrator, a permanent failure', () => {
  it('marks the entry rejected, surfaces it, never resends it, and carries on with the next entry', async () => {
    const { db, outbox, wire, orchestrator } = await setUp((entry) =>
      entry.entity === 'sale-A' ? { ok: false, status: 422, error: 'price list closed' } : { ok: true },
    );
    await outbox.enqueue(request('sale-A'));
    await outbox.enqueue(request('sale-B'));
    await orchestrator.start();

    await orchestrator.syncNow();
    await orchestrator.syncNow();

    expect(wire.attempts).toEqual(['sale-A', 'sale-B']);
    expect(statusOf(db)).toEqual({ 'sale-A': 'rejected', 'sale-B': 'synced' });
    expect((await outbox.rejected()).map((entry) => entry.lastError)).toEqual(['price list closed']);
    expect(orchestrator.getState()).toMatchObject({ rejected: 1, pending: 0 });
  });

  it('treats 408 and 429 as transient, not permanent', async () => {
    for (const status of [408, 429]) {
      const { db, outbox, orchestrator } = await setUp((_, attempt) =>
        attempt === 1 ? { ok: false, status } : { ok: true },
      );
      await outbox.enqueue(request('sale-A'));
      await orchestrator.start();
      await orchestrator.syncNow();
      expect(statusOf(db)).toEqual({ 'sale-A': 'failed' });
      await orchestrator.syncNow();
      expect(statusOf(db)).toEqual({ 'sale-A': 'synced' });
    }
  });
});

describe('SyncOrchestrator, conflict policy (ADR-0022)', () => {
  it('calls onServerWins for a rejected serverWins entry only, so the client re-reads', async () => {
    const reread: string[] = [];
    const { outbox, wire, orchestrator } = await setUp(
      (entry) => (entry.entity.startsWith('stale') ? { ok: false, status: 409, error: 'version' } : { ok: true }),
      { onServerWins: (entry) => void reread.push(entry.entity) },
    );
    await outbox.enqueue(request('stale-price', 'serverWins'));
    await outbox.enqueue(request('stale-scan', 'append'));
    await outbox.enqueue(request('stale-bill', 'lastWriterWins'));
    await outbox.enqueue(request('table-seated', 'lastWriterWins'));
    await orchestrator.start();

    await orchestrator.syncNow();

    expect(reread).toEqual(['stale-price']);
    expect(wire.accepted).toEqual(['table-seated']);
  });

  it('surfaces a failed re-read without stopping the drain', async () => {
    const { outbox, wire, orchestrator } = await setUp(
      (entry) => (entry.entity === 'price' ? { ok: false, status: 409 } : { ok: true }),
      {
        onServerWins: () => {
          throw new Error('catalogue unreachable');
        },
      },
    );
    await outbox.enqueue(request('price', 'serverWins'));
    await outbox.enqueue(request('sale-A'));
    await orchestrator.start();

    await orchestrator.syncNow();

    expect(wire.accepted).toEqual(['sale-A']);
    expect(orchestrator.getState().lastError).toMatch(/catalogue unreachable/);
  });
});

describe('SyncOrchestrator, timestamps', () => {
  it("records the server's syncedAt from the answer, and the device's time only as deviceAckedAt", async () => {
    const { db, outbox, orchestrator } = await setUp((entry) =>
      entry.entity === 'case-1' ? { ok: true, syncedAt: '2026-11-03T08:00:00.000Z' } : { ok: true },
    );
    await outbox.enqueue(request('case-1'));
    await outbox.enqueue(request('sale-1'));
    await orchestrator.start();

    await orchestrator.syncNow();

    const [withServerTime, withoutServerTime] = rows(db);
    expect(withServerTime).toMatchObject({ synced_at: '2026-11-03T08:00:00.000Z' });
    expect(withoutServerTime).toMatchObject({ synced_at: null });
    expect(withServerTime?.device_acked_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    expect(withoutServerTime?.device_acked_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
    expect(orchestrator.getState().lastDeviceAckedAt).toBe(withoutServerTime?.device_acked_at);
  });
});
