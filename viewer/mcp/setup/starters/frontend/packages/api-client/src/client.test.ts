import { describe, expect, it } from 'vitest';
import { ApiError, createApiClient } from './index';

interface Captured {
  url: string;
  init: RequestInit;
}

function fakeFetch(status: number, body: unknown, headers: Record<string, string> = {}) {
  const calls: Captured[] = [];
  const impl = async (url: string | URL | Request, init?: RequestInit): Promise<Response> => {
    calls.push({ url: String(url), init: init ?? {} });
    const contentType = status >= 400 ? 'application/problem+json' : 'application/json';
    return new Response(body === undefined ? null : JSON.stringify(body), {
      status,
      headers: { 'Content-Type': contentType, ...headers },
    });
  };
  return { calls, fetch: impl as typeof fetch };
}

const uuidV7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

describe('createApiClient', () => {
  it('sends a UUIDv7 Idempotency-Key on a write and returns the consistency token', async () => {
    const { calls, fetch } = fakeFetch(201, { id: 'x' }, { 'X-Consistency-Token': '0/16B3748' });
    const client = createApiClient({ baseUrl: 'https://api.test/v1/', fetch });

    const response = await client.request<{ id: string }>({ method: 'POST', path: '/orders', body: {} });

    const key = new Headers(calls[0]?.init.headers).get('Idempotency-Key');
    expect(key).toMatch(uuidV7);
    expect(calls[0]?.url).toBe('https://api.test/v1/orders');
    expect(response.consistencyToken).toBe('0/16B3748');
  });

  it("uses the caller's key, so a retry of the same write carries the same one", async () => {
    const { calls, fetch } = fakeFetch(200, {});
    const client = createApiClient({ baseUrl: 'https://api.test', fetch });

    await client.request({ method: 'PUT', path: '/x', body: {}, idempotencyKey: '0192b3c4-0000-7000-8000-000000000001' });

    expect(new Headers(calls[0]?.init.headers).get('Idempotency-Key')).toBe('0192b3c4-0000-7000-8000-000000000001');
  });

  it('sends no Idempotency-Key on a read', async () => {
    const { calls, fetch } = fakeFetch(200, { items: [], hasMore: false });
    const client = createApiClient({ baseUrl: 'https://api.test', fetch });

    await client.request({ method: 'GET', path: '/orders', query: { pageSize: 50, cursor: undefined } });

    expect(new Headers(calls[0]?.init.headers).has('Idempotency-Key')).toBe(false);
    expect(calls[0]?.url).toBe('https://api.test/orders?pageSize=50');
  });

  it('throws the problem as an ApiError, keyed by its slug', async () => {
    const { fetch } = fakeFetch(409, {
      type: 'https://api.ticvai.com/problems/idempotency-conflict',
      title: 'Key reused',
      status: 409,
    });
    const client = createApiClient({ baseUrl: 'https://api.test', fetch });

    const error = await client.request({ method: 'POST', path: '/orders', body: {} }).catch((e: unknown) => e);

    expect(error).toBeInstanceOf(ApiError);
    expect((error as ApiError).slug).toBe('idempotency-conflict');
    expect((error as ApiError).status).toBe(409);
  });

  it('reads Retry-After on a 429', async () => {
    const { fetch } = fakeFetch(
      429,
      { type: 'https://api.ticvai.com/problems/rate-limited', title: 'Slow down', status: 429 },
      { 'Retry-After': '3' },
    );
    const client = createApiClient({ baseUrl: 'https://api.test', fetch });

    const error = (await client.request({ method: 'GET', path: '/x' }).catch((e: unknown) => e)) as ApiError;

    expect(error.retryAfterSeconds).toBe(3);
  });
});
