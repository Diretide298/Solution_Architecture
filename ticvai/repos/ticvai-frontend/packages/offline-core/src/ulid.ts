/**
 * ULID: 48-bit timestamp + 80-bit randomness, Crockford base32.
 *
 * Used as the identifier for every outbox entry and every entity created
 * offline. Two reasons it is not a server-allocated id:
 *
 *   - offline devices must generate ids before the server has ever seen the
 *     record (31 Jul 2026 offline architecture)
 *   - the same value is the server-side idempotency key, so replaying the
 *     outbox after a crash is safe
 *
 * Must produce values matching the backend's `UlidGenerator`.
 */

const ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
const ENCODED_LENGTH = 26;

function randomBytes(count: number): Uint8Array {
  const bytes = new Uint8Array(count);

  const cryptoObj = (globalThis as { crypto?: Crypto }).crypto;
  if (cryptoObj?.getRandomValues) {
    cryptoObj.getRandomValues(bytes);
    return bytes;
  }

  throw new Error(
    'No CSPRNG available. ULIDs must not fall back to Math.random — collisions ' +
      'across devices would break outbox idempotency.',
  );
}

export function newUlid(timestamp: number = Date.now()): string {
  if (!Number.isFinite(timestamp) || timestamp < 0) {
    throw new RangeError(`Invalid timestamp: ${timestamp}`);
  }

  const bytes = new Uint8Array(16);

  let ms = Math.floor(timestamp);
  for (let i = 5; i >= 0; i--) {
    bytes[i] = ms & 0xff;
    ms = Math.floor(ms / 256);
  }

  bytes.set(randomBytes(10), 6);

  let output = '';
  let bitBuffer = 0;
  let bitCount = 0;

  for (const byte of bytes) {
    bitBuffer = (bitBuffer << 8) | byte;
    bitCount += 8;

    while (bitCount >= 5) {
      bitCount -= 5;
      output += ALPHABET[(bitBuffer >>> bitCount) & 0x1f];
    }
  }

  if (bitCount > 0) {
    output += ALPHABET[(bitBuffer << (5 - bitCount)) & 0x1f];
  }

  return output.slice(0, ENCODED_LENGTH);
}

export function isValidUlid(value: string): boolean {
  if (value.length !== ENCODED_LENGTH) return false;
  for (const char of value) {
    if (!ALPHABET.includes(char)) return false;
  }
  return true;
}

/** Extracts the embedded timestamp. Useful for ordering and for support triage. */
export function ulidTimestamp(value: string): number {
  if (!isValidUlid(value)) throw new Error(`Not a valid ULID: ${value}`);

  let ms = 0;
  for (let i = 0; i < 10; i++) {
    ms = ms * 32 + ALPHABET.indexOf(value[i]!);
  }
  return ms;
}
