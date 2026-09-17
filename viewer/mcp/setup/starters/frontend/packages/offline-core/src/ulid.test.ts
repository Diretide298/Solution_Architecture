import { describe, expect, it } from 'vitest';
import { isValidUlid, newUlid, ulidTimestamp } from './ulid';

describe('newUlid', () => {
  it('makes a valid 26-character id that keeps its timestamp', () => {
    const at = Date.UTC(2026, 8, 17, 9, 0, 0);
    const id = newUlid(at);
    expect(id).toHaveLength(26);
    expect(isValidUlid(id)).toBe(true);
    expect(ulidTimestamp(id)).toBe(at);
  });

  it('sorts by time', () => {
    const early = newUlid(1_000);
    const late = newUlid(2_000);
    expect(early < late).toBe(true);
  });

  it('refuses a negative timestamp', () => {
    expect(() => newUlid(-1)).toThrow(RangeError);
  });
});
