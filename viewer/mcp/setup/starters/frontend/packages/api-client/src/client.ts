/**
 * The transport the generated client calls (SETUP-CLIENTS generates the operations from the
 * contracts; do not hand-write them). It applies the conventions every operation shares
 * (api-conventions 3 and 4, `contracts/shared/common.yaml`):
 *
 *   - errors arrive as `application/problem+json` and are thrown as `ApiError`
 *   - every mutating call carries an `Idempotency-Key`, a UUIDv7; where the body has a client
 *     UUIDv7 `id`, the key is that id (one key per write, never two that could disagree)
 *   - a write's `X-Consistency-Token` is returned, and a read that must see that write sends it back
 *   - ids are `format: uuid`; new ones are UUIDv7 (ADR-0056)
 *
 * Offline-capable writes in offline apps do not come here directly: they go through the
 * `offline-core` outbox, which calls this on drain with the entry's own id as the key.
 */

import { v7 as uuidv7 } from 'uuid';
import { ApiError, isProblem, type Problem } from './problem';

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface ApiClientOptions {
  /** The API root, e.g. `https://venue.example/api/v1`. */
  baseUrl: string;
  /** The session's bearer token; absent for public calls. */
  getAccessToken?: () => string | undefined | Promise<string | undefined>;
  /** Defaults to the global fetch. Injected in tests. */
  fetch?: typeof fetch;
}

export interface RequestOptions {
  method: HttpMethod;
  /** The path with its parameters already filled in, e.g. `/orders/0192...`. */
  path: string;
  query?: Record<string, string | number | boolean | undefined>;
  body?: unknown;
  /**
   * Mutating calls only. Pass the body's client-generated id where it has one, and the same value
   * again when retrying the same write. Left out, one is minted for this call.
   */
  idempotencyKey?: string;
  /** The `X-Consistency-Token` of a write this read must observe. */
  consistencyToken?: string;
  /** `If-Match` for a `serverWins` update: the ETag of the version being changed. */
  ifMatch?: string;
  signal?: AbortSignal;
}

export interface ApiResponse<T> {
  status: number;
  data: T;
  /** Set on a write: pass it to the next read that must see this write. */
  consistencyToken: string | undefined;
  etag: string | undefined;
}

/** A cursor-paged list (`Page` in common.yaml). Pass `nextCursor` back as `cursor`. */
export interface Page<T> {
  items: T[];
  nextCursor?: string;
  hasMore: boolean;
}

/** A new UUIDv7: an entity id minted on the client, or an Idempotency-Key. */
export function newIdempotencyKey(): string {
  return uuidv7();
}

const MUTATING: ReadonlySet<HttpMethod> = new Set<HttpMethod>(['POST', 'PUT', 'PATCH', 'DELETE']);

export interface ApiClient {
  request<T>(options: RequestOptions): Promise<ApiResponse<T>>;
}

export function createApiClient(options: ApiClientOptions): ApiClient {
  const doFetch = options.fetch ?? globalThis.fetch.bind(globalThis);
  const root = options.baseUrl.replace(/\/+$/, '');

  async function request<T>(req: RequestOptions): Promise<ApiResponse<T>> {
    const url = new URL(root + req.path);
    for (const [key, value] of Object.entries(req.query ?? {})) {
      if (value !== undefined) {
        url.searchParams.set(key, String(value));
      }
    }

    const headers = new Headers({ Accept: 'application/json, application/problem+json' });
    const token = await options.getAccessToken?.();
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
    if (MUTATING.has(req.method)) {
      headers.set('Idempotency-Key', req.idempotencyKey ?? newIdempotencyKey());
    }
    if (req.consistencyToken) {
      headers.set('X-Consistency-Token', req.consistencyToken);
    }
    if (req.ifMatch) {
      headers.set('If-Match', req.ifMatch);
    }
    const init: RequestInit = { method: req.method, headers };
    if (req.body !== undefined) {
      headers.set('Content-Type', 'application/json');
      init.body = JSON.stringify(req.body);
    }
    if (req.signal) {
      init.signal = req.signal;
    }

    const response = await doFetch(url.toString(), init);
    const text = await response.text();
    const parsed: unknown = text.length > 0 ? JSON.parse(text) : undefined;

    if (!response.ok) {
      throw new ApiError(toProblem(parsed, response), retryAfter(response));
    }

    return {
      status: response.status,
      data: parsed as T,
      consistencyToken: response.headers.get('X-Consistency-Token') ?? undefined,
      etag: response.headers.get('ETag') ?? undefined,
    };
  }

  return { request };
}

function toProblem(body: unknown, response: Response): Problem {
  if (isProblem(body)) {
    return body;
  }
  // Something between us and the API (a proxy, a gateway) answered without a problem body.
  return {
    type: 'about:blank',
    title: response.statusText || 'Request failed',
    status: response.status,
  };
}

function retryAfter(response: Response): number | undefined {
  const value = response.headers.get('Retry-After');
  if (value === null) {
    return undefined;
  }
  const seconds = Number(value);
  return Number.isFinite(seconds) && seconds >= 0 ? seconds : undefined;
}
