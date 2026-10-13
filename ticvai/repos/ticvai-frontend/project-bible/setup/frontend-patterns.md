# Frontend Patterns — TypeScript / React / React Native

Shared rules: [quality-gates](quality-gates.md).

## 4. TypeScript / React / React Native

### 4.1 Compiler

The TypeScript config sets `strict`, `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax` - in `tsconfig.base.json`
in the one-workspace starter, in the repository's own `tsconfig` in an app repository.

`any` is prohibited. Use `unknown` and narrow.

### 4.2 Enforced boundaries

ESLint blocks these - with `@nx/enforce-module-boundaries` in the one-workspace (Nx) starter, and
with the repository's own lint rules in an app repository (the frontend is one repository per app
since 13 October 2026; a rule its lint cannot express yet is still the rule, checked in review):

| Blocked | Why |
|---|---|
| Apps importing a SQLite driver directly | Everything goes through the one offline store (`offline-core`). Six sync engines is six divergent bug surfaces |
| Packages importing apps, where the repository has shared packages | Dependencies point one way |
| Local permission computation | Clients consume `effectivePermissions`. Client-side authz is a security hole and a divergence source |
| `localStorage` / `sessionStorage` in artefacts | Unsupported in the target runtime |

### 4.3 Style

```typescript
// Named exports. Default exports only where a framework demands one.
export function useShiftState(workstationId: string): ShiftState {
  // Hooks at the top, unconditional.
  const [state, setState] = useState<ShiftState>(initialShiftState);

  // Effects declare their dependencies honestly. No lying to the linter.
  useEffect(() => {
    // ...
  }, [workstationId]);

  return state;
}
```

| Rule | Detail |
|---|---|
| Function components, hooks only | No class components |
| Props typed with an interface, never inline | Reusable, documentable |
| No `React.FC` | Poor generics and children inference |
| Discriminated unions over optional-field soup | `{ status: 'offline' } \| { status: 'syncing'; pending: number }` |
| Errors surface to the user | A swallowed sync failure behind "all synced" is worse than an error |
| No business logic in components | Hooks and packages |

### 4.4 Offline

- **A write the contract marks `x-ticvai-offline-capable: true`, in an offline app** (the package's
  offline apps: venue-pos, venue-scanner, venue-staff-app, guest-app, kitchen-display; tagged
  `offline:yes` in the one-workspace starter), goes through the outbox of the one offline store
  (`offline-core`). No direct fetch on that path.
- **Every other write** — `offline-capable: false`, or any web app — calls the generated API client
  (`@ticvai/api-client`) directly and is disabled while offline, with the reason on screen. Queuing a write the server
  will not accept later is worse than refusing it now.
- Conflict policy is declared per entity at the call site. There is no global default.
- The offline indicator reflects real transport state, never an optimistic guess.

---

