/**
 * RFC 9457 problem details: the one error shape every operation returns
 * (`Problem` in `contracts/shared/common.yaml`, api-conventions 4).
 *
 * A client switches on the problem `type`, never on `status` or `detail`: one 409 can be a paid
 * order, a closed period or an expiring hold, and each has its own type.
 */

/** Every problem type URI is this plus a kebab-case slug. Compared, never fetched. */
export const PROBLEM_TYPE_BASE = 'https://api.ticvai.com/problems/';

/** The shared types in `common.yaml`. An operation may add its own; the slug stays a string. */
export type SharedProblemSlug =
  | 'validation'
  | 'unauthenticated'
  | 'session-superseded'
  | 'forbidden'
  | 'not-found'
  | 'idempotency-conflict'
  | 'concurrency-conflict'
  | 'rate-limited'
  | 'admission-required'
  | 'duplicate-code'
  | 'server-error';

/** One failing field of a `validation` problem; `code` names the rule that failed. */
export interface ProblemFieldError {
  field: string;
  code: string;
  message?: string;
}

export interface Problem {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  traceId?: string;
  errors?: ProblemFieldError[];
}

export function isProblem(value: unknown): value is Problem {
  if (typeof value !== 'object' || value === null) {
    return false;
  }
  const v = value as Record<string, unknown>;
  return typeof v['type'] === 'string' && typeof v['title'] === 'string' && typeof v['status'] === 'number';
}

/** The slug of a problem type URI (`https://api.ticvai.com/problems/not-found` → `not-found`). */
export function problemSlug(problem: Problem): string {
  return problem.type.startsWith(PROBLEM_TYPE_BASE) ? problem.type.slice(PROBLEM_TYPE_BASE.length) : problem.type;
}

/**
 * A call the server refused. Carries the problem as sent; `slug` is what to switch on.
 * `retryAfterSeconds` is set on a 429 (ADR-0064): an offline outbox treats it as "retry later",
 * never as a rejection.
 */
export class ApiError extends Error {
  override readonly name = 'ApiError';
  readonly problem: Problem;
  readonly retryAfterSeconds: number | undefined;

  constructor(problem: Problem, retryAfterSeconds?: number) {
    super(problem.detail ?? problem.title);
    this.problem = problem;
    this.retryAfterSeconds = retryAfterSeconds;
  }

  get status(): number {
    return this.problem.status;
  }

  get slug(): SharedProblemSlug | (string & {}) {
    return problemSlug(this.problem);
  }
}
