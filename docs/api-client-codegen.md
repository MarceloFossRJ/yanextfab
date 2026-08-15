# API Client Codegen

The frontend never hand-writes fetch calls against the backend. In plain terms: when you change
a FastAPI route and save, the frontend's TypeScript types for that route update automatically,
within a second or two, with no restart or manual command. Here's how, if you want to know:

1. FastAPI serves its OpenAPI schema and, on every startup (including every `--reload` restart
   during local development), writes it to disk — see `backend/src/app/main.py`'s `lifespan`
   hook and `backend/scripts/export_openapi.py`.
2. The frontend's `pnpm dev` script runs a small `chokidar-cli` watcher
   (`pnpm run watch:api-client`) alongside `next dev` that watches that schema file and re-runs
   `pnpm run gen:api-client` whenever it changes — regenerating
   `frontend/src/lib/api/schema.d.ts` via `openapi-typescript`.
3. `frontend/src/lib/api/client.ts` wraps that generated schema with `openapi-fetch` into a
   single typed `apiClient`. It's used **server-side only** — from Next.js Server Actions
   (functions marked `"use server"`, e.g. `frontend/src/app/actions/items.ts`) and Route
   Handlers (`frontend/src/app/api/*/route.ts`), never directly from browser-side code. This is
   deliberate: the browser never talks to the backend directly, so it never needs (or sees) the
   session token — see `design.md`'s session-cookie-ownership decision for the full reasoning.

**If the generated client doesn't seem to be updating:** check that the `api-client` process is
actually running (`make logs` should show a `[api-client]`-prefixed line watching
`/shared/openapi.json`); if you're running the frontend outside Docker, make sure
`OPENAPI_SCHEMA_PATH` points at wherever your local backend writes `openapi.json` (see
[Configuration](configuration.md)).

**Regenerating manually** (e.g. outside Docker, or to check for drift):

```bash
cd backend && uv run python scripts/export_openapi.py openapi.json
cd ../frontend && OPENAPI_SCHEMA_PATH=../backend/openapi.json pnpm run gen:api-client
```

Or simply: `./scripts/check-api-client-drift.sh` — this is the same check CI runs on every PR;
it fails (and prints a diff) if the committed client doesn't match what regenerating it produces.
