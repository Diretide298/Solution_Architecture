import { describe, expect, it } from 'vitest';
import { Outbox, type EnqueueRequest } from './outbox';
import { openMemoryDatabase, type MemoryDatabase } from './memory-sqlite.test-support';

function request(entity: string, overrides: Partial<EnqueueRequest> = {}): EnqueueRequest {
  return {
    entity,
    operation: 'create',
    endpoint: '/orders',
    method: 'POST',
    payload: { entity },
    conflictPolicy: 'append',
    venueId: 'venue-1',
    workstationId: 'till-1',
    ...overrides,
  };
}

function rows(db: MemoryDatabase): { entity: string; sequence: number; status: string }[] {
  return db.raw.prepare('SELECT entity, sequence, status FROM outbox ORDER BY sequence').all() as {
    entity: string;
    sequence: number;
    status: string;
  }[];
}

async function openOutbox(exclusiveTransactions = true): Promise<{ db: MemoryDatabase; outbox: Outbox }> {
  const db = await openMemoryDatabase({ exclusiveTransactions });
  const outbox = new Outbox(db);
  await outbox.initialise();
  return { db, outbox };
}

describe('Outbox.enqueue', () => {
  for (const exclusive of [true, false]) {
    const driver = exclusive ? 'an exclusive-transaction driver' : 'a driver whose transaction holds nothing off';

    it(`gives concurrent enqueues distinct sequences, increasing in call order, on ${driver}`, async () => {
      const { db, outbox } = await openOutbox(exclusive);
      const names = Array.from({ length: 12 }, (_, i) => `sale-${i + 1}`);

      const entries = await Promise.all(names.map((name) => outbox.enqueue(request(name))));

      const sequences = entries.map((entry) => entry.sequence);
      expect(new Set(sequences).size).toBe(names.length);
      expect(sequences).toEqual([...sequences].sort((a, b) => a - b));
      expect(rows(db).map((row) => row.entity)).toEqual(names);
      expect(rows(db).map((row) => row.sequence)).toEqual(sequences);
    });
  }

  it('allocates the sequence and inserts in one transaction: a failed insert leaves no gap', async () => {
    const { db, outbox } = await openOutbox();
    const first = await outbox.enqueue(request('sale-1', { id: '0190d0a0-0000-7000-8000-000000000001' }));

    await expect(
      outbox.enqueue(request('sale-1-again', { id: '0190d0a0-0000-7000-8000-000000000001' })),
    ).rejects.toThrow();
    const next = await outbox.enqueue(request('sale-2'));

    expect(next.sequence).toBe(first.sequence + 1);
    expect(rows(db).map((row) => row.entity)).toEqual(['sale-1', 'sale-2']);
  });

  it('refuses a second entry at a sequence another entry holds (UNIQUE(sequence))', async () => {
    const { db, outbox } = await openOutbox();
    const entry = await outbox.enqueue(request('sale-1'));

    expect(() =>
      db.raw
        .prepare(
          `INSERT INTO outbox (id, sequence, entity, operation, endpoint, method, payload,
             conflict_policy, status, recorded_at, attempts, venue_id, workstation_id)
           VALUES ('other', ?, 'x', 'create', '/x', 'POST', '{}', 'append', 'pending', 'now', 0, 'v', 'w')`,
        )
        .run(entry.sequence),
    ).toThrow(/UNIQUE/);
  });

  it('initialises idempotently, and adds device_acked_at to a table made before it', async () => {
    const db = await openMemoryDatabase();
    db.raw.exec(`CREATE TABLE outbox (
        id TEXT PRIMARY KEY, sequence INTEGER NOT NULL, entity TEXT NOT NULL, operation TEXT NOT NULL,
        endpoint TEXT NOT NULL, method TEXT NOT NULL, payload TEXT NOT NULL, conflict_policy TEXT NOT NULL,
        status TEXT NOT NULL, recorded_at TEXT NOT NULL, synced_at TEXT, attempts INTEGER NOT NULL DEFAULT 0,
        last_error TEXT, venue_id TEXT NOT NULL, workstation_id TEXT NOT NULL)`);
    const outbox = new Outbox(db);

    await outbox.initialise();
    await outbox.initialise();
    const entry = await outbox.enqueue(request('sale-1'));
    await outbox.markSynced(entry.id, null, '2026-11-03T10:00:00.000Z');

    const columns = (db.raw.prepare('PRAGMA table_info(outbox)').all() as { name: string }[]).map((c) => c.name);
    expect(columns).toContain('device_acked_at');
  });
});
