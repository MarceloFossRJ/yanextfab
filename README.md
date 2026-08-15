# Yanextfab

Yet another Next.js and FastAPI boilerplate — a personal-first starter for projects that need a
TypeScript frontend, a Python backend, and heavy AI/agent tooling out of the box.

- **Frontend**: Next.js, React, Zod, Shadcn/ui, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy (async), Pydantic, LangGraph
- **Auth**: `fastapi-users`, with Next.js owning the session cookie
- **AI**: an example LangGraph agent streamed over SSE, backed by Anthropic via `init_chat_model`

See `openspec/changes/bootstrap-yanextfab/design.md` for the reasoning behind these choices.

## Getting started

```bash
cp .env.example .env   # set JWT_SECRET and (optionally) ANTHROPIC_API_KEY
make up                # docker compose up --build
```

That's the whole local setup: Postgres, the backend (migrations run automatically on
startup), the frontend, and Mailpit all come up together. Then:

- App: http://localhost:3000
- API docs: http://localhost:8000/docs
- Mailpit (dev email inbox — password reset emails land here): http://localhost:8025

See `make help`-equivalent targets in the root `Makefile` (`down`, `logs`, `migrate`, `lint`,
`test`, …) for the rest of the day-to-day commands.

### Enable pre-commit hooks

```bash
uv tool install pre-commit   # or: pipx install pre-commit
pre-commit install
```

This runs Ruff (lint + format) on the backend and ESLint + Prettier on the frontend before
every commit — the same checks CI runs on every PR (`.github/workflows/ci.yml`), just earlier.

## Configuration

All variables live in `.env` at the repo root (copy `.env.example` to start) for Docker
Compose, or in `backend/.env` / `frontend/.env.local` if running either app outside Docker —
see `backend/.env.example` and `frontend/.env.example`. Full list and defaults:
`backend/src/app/core/config.py` and `frontend/src/env.ts`.

| Variable | Where | Purpose |
| --- | --- | --- |
| `JWT_SECRET` | backend | Signs session/reset-password tokens. **Must** be changed before any real deployment — generate with `openssl rand -hex 32`. |
| `DATABASE_URL` | backend | Postgres connection string. Set by `docker-compose.yml` for the Compose path. |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_TLS` / `SMTP_SSL` | backend | Outgoing mail (password recovery). Defaults point at the Mailpit dev service (`mailpit:1025`, no auth). For production, point these at a real provider (SES, Postmark, Resend, …) — no vendor is hardcoded. |
| `SMTP_FROM` | backend | The "from" address on outgoing mail. |
| `ANTHROPIC_API_KEY` | backend | Required for the AI agent to actually call Claude. Without it, the chat example still works end-to-end but the LLM call fails (surfaced as a chat error message, not a crash — see `app/ai/router.py`). |
| `LLM_MODEL` | backend | `provider:model` string passed to LangChain's `init_chat_model`. Defaults to `anthropic:claude-sonnet-5`. **This is the one line to change to swap LLM providers** — the agent code itself (`app/ai/agent.py`) doesn't need to change. |
| `FRONTEND_URL` | backend | Used to build links in outgoing email (e.g. the password-reset URL) and for CORS. |
| `API_URL` | frontend | Server-only. Where the frontend reaches the backend. Never exposed to the browser — see `frontend/src/env.ts`. |
| `OPENAPI_SCHEMA_PATH` | frontend | Where the frontend watches for schema changes to regenerate its typed client (see below). Only relevant in dev. |

## Deployment

**Primary path — Docker Compose.** The same `docker-compose.yml` used for local development is
the primary deployment path: it's portable to any host that can run Docker Compose (or an
equivalent container orchestrator that accepts the same Dockerfiles), not tied to a specific
PaaS. Set real values for `JWT_SECRET`, `ANTHROPIC_API_KEY`, and the `SMTP_*` variables (see
`.env.example` and `backend/src/app/core/config.py`) for a production environment — the
in-repo defaults are dev-only.

**Secondary path — Vercel for the frontend only.** Next.js on Vercel is close to a one-click
deploy, so it's documented separately from the backend rather than folded into Compose:

1. Import the repo into Vercel with **Root Directory** set to `frontend/`.
2. Set the `API_URL` environment variable to your separately-hosted backend's URL (e.g.
   `https://api.yourdomain.com`). This is server-only — see `frontend/src/env.ts` — so it's
   never exposed to the browser.
3. Leave `OPENAPI_SCHEMA_PATH` unset in this environment: codegen is a dev/build-time step
   (`pnpm run gen:api-client`), not something that needs to run against a live schema file in
   production — the generated `frontend/src/lib/api/schema.d.ts` is already committed.
4. Vercel's default build (`next build`) and start commands work as-is; don't override them
   with `pnpm dev` — that's what runs the `chokidar-cli` watcher, which is dev-only.

The backend is deliberately *not* targeted at Vercel — it's a stateful FastAPI app (SSE
streaming, a persistent Postgres connection pool, a LangGraph checkpointer) that doesn't fit
a serverless function model. Any host that accepts a Dockerfile (Fly.io, Railway, Render, a
plain VM, …) works; point Vercel's `API_URL` at wherever you land it.

## API client codegen

The frontend never hand-writes fetch calls against the backend. Instead:

1. FastAPI serves its OpenAPI schema and, on every startup (including every `--reload` restart
   during local development), writes it to disk — see `backend/src/app/main.py`'s `lifespan`
   hook and `backend/scripts/export_openapi.py`.
2. The frontend's `pnpm dev` script runs a small `chokidar-cli` watcher
   (`pnpm run watch:api-client`) alongside `next dev` that watches that schema file and re-runs
   `pnpm run gen:api-client` whenever it changes — regenerating
   `frontend/src/lib/api/schema.d.ts` via `openapi-typescript`.
3. `frontend/src/lib/api/client.ts` wraps that generated schema with `openapi-fetch` into a
   single typed `apiClient`, used server-side only (Server Actions / Route Handlers — see
   `design.md`'s session-cookie-ownership decision for why the browser never calls the backend
   directly).

So: change a FastAPI route, save, and the typed client updates automatically — no manual
codegen step during day-to-day development.

**Regenerating manually** (e.g. outside Docker, or to check for drift):

```bash
cd backend && uv run python scripts/export_openapi.py openapi.json
cd ../frontend && OPENAPI_SCHEMA_PATH=../backend/openapi.json pnpm run gen:api-client
```

Or simply: `./scripts/check-api-client-drift.sh` — this is the same check CI runs on every PR;
it fails (and prints a diff) if the committed client doesn't match what regenerating it produces.
