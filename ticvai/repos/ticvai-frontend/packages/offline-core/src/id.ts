/**
 * Ids: UUIDv7, the one id type (ADR-0056, 30 Sep 2026).
 *
 * Used as the identifier for every outbox entry and every entity created
 * offline. Two reasons it is not a server-allocated id:
 *
 *   - offline devices must generate ids before the server has ever seen the
 *     record (31 Jul 2026 offline architecture)
 *   - the same value is the server-side idempotency key, so replaying the
 *     outbox after a crash is safe
 *
 * The backend mints the same format with `Id.New()` (`Guid.CreateVersion7()`),
 * and the contracts type every id `format: uuid`. UUIDv7 is time-ordered, so
 * keys stay in insertion order in the server's indexes. Ids are opaque: the
 * app never reads a time out of one.
 */

import { v7 as uuidv7, validate, version } from 'uuid';

/** A new UUIDv7. Uses the platform CSPRNG; never falls back to Math.random. */
export function newId(): string {
  return uuidv7();
}

/**
 * True when `value` is a UUIDv7. Ids created before ADR-0056 may be other uuid
 * versions and are still valid ids: check an id received from the server with
 * `isUuid`, and use this only where a newly minted id is required.
 */
export function isVersion7Id(value: string): boolean {
  return validate(value) && version(value) === 7;
}

/** True when `value` is any uuid, the shape every id in the contracts has. */
export function isUuid(value: string): boolean {
  return validate(value);
}
