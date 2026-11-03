#!/usr/bin/env bash
# Regenerates the three consumer clients from the bundled specs (make bundle writes dist/<folder>-<name>.yaml).
#
# r13 system review D-10 (CHG-R14J-003): the TypeScript clients were one folder per spec with no package.json, so
# `npm publish` in dist/clients/typescript had nothing to publish; C# targeted net8.0 (the backend is net10.0) and
# Python pydantic v1 (the AI runtime pins pydantic 2). Now the TypeScript clients are one package, @ticvai/api-client,
# versioned from the release tag, with one namespace per contract; C# targets net10.0 and Python uses the `python`
# generator (pydantic v2). openapi-generator-cli needs a Java runtime: the publish job's image has one.
set -euo pipefail

VERSION="${CLIENT_VERSION:-${CI_COMMIT_TAG:-v0.0.0-local}}"
VERSION="${VERSION#v}"
OUT_TS="dist/clients/typescript"
OUT_CS="dist/clients/csharp"
OUT_PY="dist/clients/python"
rm -rf dist/clients && mkdir -p "$OUT_TS/src" "$OUT_CS" "$OUT_PY"
command -v java >/dev/null || { echo "generate-clients: openapi-generator-cli needs a Java runtime (java is not on PATH)" >&2; exit 1; }

INDEX="$OUT_TS/src/index.ts"
: > "$INDEX"
for spec in dist/*.yaml; do
  name=$(basename "$spec" .yaml)
  # spine-identity -> spineIdentity: one namespace per contract in the one package
  ident=$(printf '%s' "$name" | awk -F'[-_.]' '{s = $1; for (i = 2; i <= NF; i++) s = s toupper(substr($i, 1, 1)) substr($i, 2); print s}')

  npx --yes @hey-api/openapi-ts \
    --input "$spec" --output "${OUT_TS}/src/${name}" --client fetch
  echo "export * as ${ident} from './${name}/index';" >> "$INDEX"

  npx --yes @openapitools/openapi-generator-cli generate \
    -i "$spec" -g csharp -o "${OUT_CS}/${name}" \
    --additional-properties=targetFramework=net10.0,library=httpclient,nullableReferenceTypes=true

  npx --yes @openapitools/openapi-generator-cli generate \
    -i "$spec" -g python -o "${OUT_PY}/${name}"
done

cat > "$OUT_TS/package.json" <<JSON
{
  "name": "@ticvai/api-client",
  "version": "${VERSION}",
  "description": "TICVAI API client, generated from ticvai-contracts at ${CI_COMMIT_TAG:-a local build}. Do not edit.",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"]
}
JSON
cat > "$OUT_TS/tsconfig.json" <<'JSON'
{
  "compilerOptions": {
    "target": "ES2022", "module": "ES2022", "moduleResolution": "Bundler", "lib": ["ES2022", "DOM"],
    "declaration": true, "outDir": "dist", "rootDir": "src", "strict": true, "skipLibCheck": true
  },
  "include": ["src"]
}
JSON
npx --yes -p typescript@5 tsc -p "$OUT_TS"

echo "Generated @ticvai/api-client ${VERSION} and the C# and Python clients for: $(ls dist/*.yaml | xargs -n1 basename | tr '\n' ' ')"
