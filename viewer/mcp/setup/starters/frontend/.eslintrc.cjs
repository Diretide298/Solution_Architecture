module.exports = {
  root: true,
  plugins: ['@nx'],
  ignorePatterns: ['node_modules/', 'dist/', 'coverage/'],
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      extends: ['plugin:@nx/typescript'],
      rules: {
        '@nx/enforce-module-boundaries': [
          'error',
          {
            allow: [],
            depConstraints: [
              // Apps consume packages. Packages never consume apps.
              // Every project carries a constraint: a tag no constraint matches fails
              // the rule as soon as that project imports a library.
              { sourceTag: 'type:app', onlyDependOnLibsWithTags: ['type:package'] },
              { sourceTag: 'type:package', notDependOnLibsWithTags: ['type:app'] },
              // No app may bypass offline-core with its own sync or SQLite code.
              // offline-core is the single implementation - six copies is six
              // divergent bug surfaces.
              {
                sourceTag: 'type:app',
                bannedExternalImports: ['expo-sqlite', 'react-native-sqlite-storage', '@op-engineering/op-sqlite'],
              },
              // Design tokens are leaf. They depend on nothing.
              { sourceTag: 'scope:design-tokens', onlyDependOnLibsWithTags: [] },
              // api-client is generated from the contracts. It must not reach
              // into UI or offline concerns.
              { sourceTag: 'scope:api-client', onlyDependOnLibsWithTags: [] },
              // The UI kit is presentation: it renders from the design tokens and
              // reaches into neither the API nor offline concerns.
              { sourceTag: 'scope:ui', onlyDependOnLibsWithTags: ['scope:design-tokens'] },
              // offline-core is leaf. The app hands it a transport (SyncTransport);
              // it never imports api-client or the UI.
              { sourceTag: 'scope:offline-core', onlyDependOnLibsWithTags: [] },
            ],
          },
        ],
        'no-restricted-imports': [
          'error',
          {
            patterns: [
              {
                group: ['**/permissions/compute*', '**/auth/resolve*'],
                message:
                  'Clients never compute permissions (CR-367). Use effectivePermissions from the session for coarse ' +
                  'filtering only. For a node, look it up in Session.permissionsByScope by the entry of the deepest ' +
                  'listed path that contains the node; never union the entries of its ancestors, never apply a deny yourself.',
              },
            ],
          },
        ],
      },
    },
  ],
};
