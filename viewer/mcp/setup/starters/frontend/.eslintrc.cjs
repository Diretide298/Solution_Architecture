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
              { sourceTag: 'type:app', onlyDependOnLibsWithTags: ['type:package'] },
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
            ],
          },
        ],
        'no-restricted-imports': [
          'error',
          {
            patterns: [
              {
                group: ['**/permissions/compute*', '**/auth/resolve*'],
                message: 'Clients never compute permissions locally. Consume effectivePermissions from the session.',
              },
            ],
          },
        ],
      },
    },
  ],
};
