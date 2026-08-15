# Yanextfab

Yet another Next.js and FastAPI boilerplate — a personal-first starter for projects that need a
TypeScript frontend, a Python backend, and heavy AI/agent tooling out of the box.

- **Frontend**: [Next.js](https://nextjs.org/) + React, [Zod](https://zod.dev/) for schema
  validation, [Shadcn/ui](https://ui.shadcn.com/) for components, [Tailwind CSS](https://tailwindcss.com/) for styling
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/) (async) for the database, [Pydantic](https://docs.pydantic.dev/) for data validation, [LangGraph](https://langchain-ai.github.io/langgraph/) for AI agents
- **Auth**: [`fastapi-users`](https://fastapi-users.github.io/fastapi-users/) on the backend, with Next.js owning the session cookie
- **AI**: an example LangGraph agent streamed over SSE, backed by Anthropic via `init_chat_model`

You don't need to already know all of these — see [Tech stack, briefly](#tech-stack-briefly)
below for a one-line explanation of each. See `openspec/changes/bootstrap-yanextfab/design.md`
for the deeper reasoning behind these choices (optional reading, not required to get started).

## Prerequisites

You have two options. Pick one — you don't need both.

**Option A — Docker only (recommended, least setup):**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- `git`

**Option B — running the apps natively (faster iteration, more setup):** everything in Option
A, plus:
- [Node.js 24+](https://nodejs.org/) and [pnpm](https://pnpm.io/installation) (frontend)
- [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) (backend)
- A local Postgres instance (or run just the `postgres` service from Docker Compose — see
  below)

`make` is used throughout this README as a shorthand, but it's optional — every `make <target>`
command is a one-liner defined in the root `Makefile`; if you don't have `make` installed, open
the `Makefile` and run the underlying command directly (e.g. `make up` is just
`docker compose up --build`).

**Windows**: use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) with Docker
Desktop's WSL2 backend. The repo's shell scripts (`docker-entrypoint.sh`,
`scripts/check-api-client-drift.sh`) and Makefile targets assume a Unix-like shell and aren't
tested on native Windows (PowerShell/cmd).

## Creating your own project from this template

1. On GitHub, click **"Use this template"** on the Yanextfab repo (or `git clone` it if you're
   not using GitHub) to get your own copy under a new name.
2. Rename the project. Nothing does this automatically — it's a handful of places where
   "Yanextfab"/"yanextfab" is hardcoded as boilerplate branding:
   - `frontend/package.json` — the `"name"` field (currently `"frontend"`, fine to leave as-is
     or rename)
   - `backend/pyproject.toml` — the `[project]` `name` field (currently `"backend"`)
   - `frontend/src/components/dashboard/app-sidebar.tsx` — the "Yanextfab" text shown in the
     dashboard sidebar
   - `frontend/src/app/register/page.tsx` — "Get started with Yanextfab." copy
   - `backend/src/app/main.py` — the FastAPI `title="Yanextfab API"`
   - `backend/src/app/core/mail.py` — the password-reset email subject line
   - `LICENSE` — the copyright holder name
   - This `README.md` — the title and description
3. Continue with **Getting started** below.

The `openspec/` directory is this template's own internal planning history (the proposal,
design doc, and task breakdown used to build Yanextfab itself) — it's not part of the running
app. Keep it if you want a written record of *why* things are built the way they are, or delete
the whole folder for your own project; nothing in `frontend/` or `backend/` depends on it.

## Getting started

```bash
cp .env.example .env
```

Open `.env` in a text editor and fill in:
- `JWT_SECRET` — a random secret used to sign session tokens. Generate one with
  `openssl rand -hex 32` (available by default on macOS/Linux; on Windows use WSL, or generate
  one at <https://generate-secret.vercel.app/32>) and paste it in. **Don't skip this** — the
  committed default is a well-known placeholder, not a real secret.
- `ANTHROPIC_API_KEY` — *optional.* Needed only to make the AI chat example actually respond.
  Get one at <https://console.anthropic.com/> (requires an account; Anthropic's API is
  pay-as-you-go, not free, but new accounts typically get a small trial credit). If you leave
  this blank, everything else in the app still works — the chat page will show an error message
  instead of a reply, rather than crashing.

Then bring the whole stack up:

```bash
make up   # or: docker compose up --build
```

This starts four containers together: Postgres, the backend (database migrations run
automatically on startup), the frontend, and Mailpit (a fake email inbox for testing the
password-reset flow — see below). The first run downloads base images and installs
dependencies, so it can take a few minutes; subsequent runs are much faster.

**How to tell it worked:** once the logs settle, open <http://localhost:3000> — you should land
on a login page. That confirms the frontend is up and can reach the backend.

- App: <http://localhost:3000>
- API docs (interactive, from FastAPI): <http://localhost:8000/docs>
- Mailpit (dev email inbox): <http://localhost:8025>

### Try it out

1. Go to <http://localhost:3000/register> and create an account with any email and an 8+
   character password — there's no email verification step, so any address works.
2. You'll land on the dashboard. Try the **Items** page (a small create/edit/delete example —
   proves the typed API path works end-to-end) and the **Chat** page (the AI agent example — it
   needs `ANTHROPIC_API_KEY` to actually reply, see above).
3. Try "Forgot password?" from the login page, then check <http://localhost:8025> — the reset
   email actually arrives there in dev, with a working reset link, instead of going to a real
   inbox.

### Other commands

All defined in the root `Makefile`:

| Command | What it does |
| --- | --- |
| `make down` | Stop and remove the containers |
| `make logs` | Tail logs from all services (useful for debugging a container that won't start) |
| `make restart` | Restart the containers without rebuilding |
| `make migrate` | Run database migrations manually (normally automatic on `make up`) |
| `make backend-shell` / `make frontend-shell` | Open a shell inside the running backend/frontend container |
| `make lint` / `make format` | Run linters / auto-format both apps |
| `make test` | Run both test suites (backend: pytest, frontend: vitest) |

### Troubleshooting

- **"Port already in use"**: something else on your machine is already using port 3000, 8000,
  8025, or 5433. Stop that process, or edit the port mappings in `docker-compose.yml`. (Postgres
  is deliberately exposed on host port **5433**, not the default 5432, specifically to avoid
  clashing with a Postgres install you might already have running locally — if you connect a
  database GUI tool, point it at 5433, not 5432.)
- **A container keeps restarting or exits immediately**: run `make logs` and look for the
  first error — it's almost always a missing/invalid `.env` value or Docker not having enough
  resources.
- **Docker isn't running at all**: make sure Docker Desktop is open and its whale icon shows
  "running" before `make up`.
- Still stuck: try `make down` then `make up` again for a clean restart.

## What's in the box

This is a full example app, not just empty scaffolding — the idea is you delete/replace the
example pieces as you build your real feature, rather than starting from nothing.

- **Auth** (`frontend/src/app/{login,register,forgot-password,reset-password}`,
  `backend/src/app/users.py`): working signup, login, logout, and password reset.
- **Dashboard shell** (`frontend/src/app/dashboard/layout.tsx`): a sidebar + protected-route
  wrapper — any page you add under `frontend/src/app/dashboard/` inherits it automatically.
- **CRUD example** (`frontend/src/app/dashboard/page.tsx`,
  `backend/src/app/{models,schemas,api}/item.py`): a minimal "items" resource showing the full
  typed path from a Postgres table to a form on the page. This is the one to copy when adding
  your own resources.
- **AI chat example** (`frontend/src/app/dashboard/chat`, `backend/src/app/ai/`): a LangGraph
  agent with one tool, streamed token-by-token over Server-Sent Events.

## Adding your own features

**Add a new backend endpoint and use it from the frontend:**
1. Add a route in `backend/src/app/api/` (copy `items.py` as a starting point) and register its
   router in `backend/src/app/main.py`.
2. Save. If you're running via `make up` (or `pnpm dev` locally), the frontend's typed client
   regenerates automatically within a second or two — no restart needed (see
   [API client codegen](#api-client-codegen) below for how this works, and what to check if it
   doesn't seem to be updating).
3. Call it from a Server Action or Route Handler in the frontend using
   `import { apiClient } from "@/lib/api/client"` — see `frontend/src/app/actions/items.ts` for
   a working example. You get autocomplete and type errors for the new endpoint immediately.

**Add a new frontend page:** create a folder under `frontend/src/app/` with a `page.tsx` (this
is standard [Next.js App Router](https://nextjs.org/docs/app/getting-started/layout-and-pages)
file-based routing). Put it under `frontend/src/app/dashboard/` if it should require login and
show the sidebar.

## Testing

- **Backend**: [pytest](https://docs.pytest.org/), via `cd backend && uv run pytest` (or
  `make test` for both suites). Tests live in `backend/tests/`; a real (disposable) Postgres
  database is required — see `backend/tests/conftest.py`, which creates and tears down its own
  test database automatically against whatever `DATABASE_URL` you have configured.
- **Frontend**: [Vitest](https://vitest.dev/), via `cd frontend && pnpm test`. Tests live next
  to the code they test as `*.test.ts` files (e.g. `frontend/src/lib/schemas/auth.test.ts`).

Both run automatically in CI on every pull request — see `.github/workflows/ci.yml`.

## Enable pre-commit hooks (optional, recommended)

```bash
uv tool install pre-commit   # or: pipx install pre-commit
pre-commit install
```

Requires `uv` (backend) and `pnpm` (frontend) to already be installed — see
[Prerequisites](#prerequisites) if you're only using Docker and don't have them yet.

This is optional — skipping it doesn't break anything locally. What it buys you: Ruff (lint +
format) on the backend and ESLint + Prettier on the frontend run automatically before every
`git commit`, catching the same issues CI would catch on the PR, just earlier and locally
instead of waiting for a CI run.

## Tech stack, briefly

If a name above is new to you, here's the one-line version of what it's for:

| Tool | What it's for |
| --- | --- |
| [Next.js](https://nextjs.org/) | The React framework running the frontend — pages, routing, and the server-side code that talks to the backend. |
| [Zod](https://zod.dev/) | Validates data at runtime (e.g. form input) and gives you matching TypeScript types for free. |
| [Shadcn/ui](https://ui.shadcn.com/) | Pre-built, customizable UI components (buttons, dialogs, forms, …) whose code lives directly in this repo (`frontend/src/components/ui/`), not in `node_modules`. |
| [Tailwind CSS](https://tailwindcss.com/) | Utility-class based styling — the `className="flex gap-2"` style attributes you'll see throughout. |
| [FastAPI](https://fastapi.tiangolo.com/) | The Python framework running the backend API. |
| [SQLAlchemy](https://www.sqlalchemy.org/) | Talks to the Postgres database from Python (the ORM). |
| [Pydantic](https://docs.pydantic.dev/) | Validates and serializes data on the backend — FastAPI uses it for request/response models. |
| [`fastapi-users`](https://fastapi-users.github.io/fastapi-users/) | Provides the registration/login/password-reset endpoints, so auth isn't hand-rolled. |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Builds the AI agent — manages its conversation state and lets it call tools. A "checkpointer" is just where that conversation state is saved (here, Postgres) so it survives a restart. |
| [Alembic](https://alembic.sqlalchemy.org/) | Manages database schema changes (migrations) for SQLAlchemy. |

## Configuration

All variables live in `.env` at the repo root (copy `.env.example` to start) for Docker
Compose, or in `backend/.env` / `frontend/.env.local` if running either app outside Docker —
see `backend/.env.example` and `frontend/.env.example`. Full list and defaults:
`backend/src/app/core/config.py` and `frontend/src/env.ts`.

| Variable | Where | Purpose |
| --- | --- | --- |
| `JWT_SECRET` | backend | Signs session/reset-password tokens. **Must** be changed before any real deployment — generate with `openssl rand -hex 32`. |
| `DATABASE_URL` | backend | Postgres connection string. Set by `docker-compose.yml` for the Compose path. |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `SMTP_TLS` / `SMTP_SSL` | backend | Outgoing mail (password recovery). Defaults point at the Mailpit dev service (`mailpit:1025`, no auth). For production, point these at a real provider — no vendor is hardcoded. For example, [Resend](https://resend.com/) gives you `SMTP_HOST=smtp.resend.com`, `SMTP_PORT=587`, `SMTP_USER=resend`, `SMTP_PASSWORD=<your API key>`, `SMTP_TLS=true`; most providers (Postmark, SES, Mailgun, …) work the same way — check their SMTP docs for the exact host/port. |
| `SMTP_FROM` | backend | The "from" address on outgoing mail. |
| `ANTHROPIC_API_KEY` | backend | Required for the AI agent to actually call Claude. Without it, the chat example still works end-to-end but the LLM call fails (surfaced as a chat error message, not a crash — see `app/ai/router.py`). |
| `LLM_MODEL` | backend | `provider:model` string passed to LangChain's `init_chat_model`. Defaults to `anthropic:claude-sonnet-5`. **This is the one line to change to swap LLM providers** — the agent code itself (`app/ai/agent.py`) doesn't need to change. |
| `FRONTEND_URL` | backend | Used to build links in outgoing email (e.g. the password-reset URL) and for CORS. |
| `API_URL` | frontend | Server-only. Where the frontend reaches the backend. Never exposed to the browser — see `frontend/src/env.ts`. |
| `OPENAPI_SCHEMA_PATH` | frontend | Where the frontend watches for schema changes to regenerate its typed client (see below). Only relevant in dev. |

## Deployment

*Skip this section until you're actually ready to put something in front of real users — it's
not needed to develop locally.*

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
Configuration above).

**Regenerating manually** (e.g. outside Docker, or to check for drift):

```bash
cd backend && uv run python scripts/export_openapi.py openapi.json
cd ../frontend && OPENAPI_SCHEMA_PATH=../backend/openapi.json pnpm run gen:api-client
```

Or simply: `./scripts/check-api-client-drift.sh` — this is the same check CI runs on every PR;
it fails (and prints a diff) if the committed client doesn't match what regenerating it produces.
