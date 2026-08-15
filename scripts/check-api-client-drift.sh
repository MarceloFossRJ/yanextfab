#!/usr/bin/env bash
# Regenerates the OpenAPI schema + typed frontend client and fails if the committed
# client differs from what regeneration produces. Run by CI (see .github/workflows/ci.yml)
# and usable locally: ./scripts/check-api-client-drift.sh
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

(cd backend && uv run python scripts/export_openapi.py openapi.json)
(cd frontend && OPENAPI_SCHEMA_PATH=../backend/openapi.json pnpm run gen:api-client)

if ! git diff --quiet -- frontend/src/lib/api/schema.d.ts; then
  echo "frontend/src/lib/api/schema.d.ts is out of date with the backend's OpenAPI schema."
  echo
  echo "Regenerate it locally with:"
  echo "  cd backend && uv run python scripts/export_openapi.py openapi.json"
  echo "  cd ../frontend && pnpm run gen:api-client"
  echo
  echo "Then commit the result. Diff:"
  git diff -- frontend/src/lib/api/schema.d.ts
  exit 1
fi

echo "API client is in sync with the backend schema."
