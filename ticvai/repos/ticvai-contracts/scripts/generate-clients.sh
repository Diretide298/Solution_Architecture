#!/usr/bin/env bash
# Regenerates the three consumer clients from bundled specs.
set -euo pipefail

OUT_TS="dist/clients/typescript"
OUT_CS="dist/clients/csharp"
OUT_PY="dist/clients/python"
rm -rf dist/clients && mkdir -p "$OUT_TS" "$OUT_CS" "$OUT_PY"

for spec in dist/*.yaml; do
  name=$(basename "$spec" .yaml)

  npx --yes @hey-api/openapi-ts \
    --input "$spec" --output "${OUT_TS}/${name}" --client fetch

  npx --yes @openapitools/openapi-generator-cli generate \
    -i "$spec" -g csharp -o "${OUT_CS}/${name}" \
    --additional-properties=targetFramework=net8.0,library=httpclient,nullableReferenceTypes=true

  npx --yes @openapitools/openapi-generator-cli generate \
    -i "$spec" -g python-pydantic-v1 -o "${OUT_PY}/${name}"
done

echo "Generated clients for: $(ls dist/*.yaml | xargs -n1 basename | tr '\n' ' ')"
