# Frontend Patterns — TypeScript / React / React Native

Shared rules: [quality-gates](quality-gates.md).

## 4. TypeScript / React / React Native

### 4.1 Compiler

`tsconfig.base.json` sets `strict`, `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`.

`any` is prohibited. Use `unknown` and narrow.

### 4.2 Enforced boundaries

ESLint `@nx/enforce-module-boundaries` blocks:

| Blocked | Why |
|---|---|
| Apps importing a SQLite driver directly | Everything goes through `offline-core`. Six sync engines is six divergent bug surfaces |
| Packages importing apps | Dependencies point one way |
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

- Every mutating call goes through the `offline-core` outbox. No direct fetch on a write path.
- Conflict policy is declared per entity at the call site. There is no global default.
- The offline indicator reflects real transport state, never an optimistic guess.

---

