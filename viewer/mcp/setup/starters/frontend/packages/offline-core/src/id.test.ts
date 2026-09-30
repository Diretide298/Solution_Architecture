import { describe, expect, it } from 'vitest';
import { isUuid, isVersion7Id, newId } from './id';

describe('newId', () => {
  it('makes a lower-case UUIDv7', () => {
    const id = newId();
    expect(id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
    expect(isVersion7Id(id)).toBe(true);
    expect(isUuid(id)).toBe(true);
  });

  it('never repeats', () => {
    expect(newId()).not.toBe(newId());
  });

  it('sorts by time', async () => {
    const early = newId();
    await new Promise((resolve) => setTimeout(resolve, 2));
    const late = newId();
    expect(early < late).toBe(true);
  });
});

describe('isVersion7Id', () => {
  it('accepts a uuid of another version as a uuid but not as a new id', () => {
    const v4 = '3f2504e0-4f89-41d3-9a0c-0305e82c3301';
    expect(isUuid(v4)).toBe(true);
    expect(isVersion7Id(v4)).toBe(false);
  });

  it('refuses what is not a uuid', () => {
    expect(isUuid('01J8Z3K6QW0000000000000000')).toBe(false);
    expect(isVersion7Id('not-an-id')).toBe(false);
  });
});
