## Context

See proposal.md for motivation. This design covers a from-scratch bootstrap of every capability listed there — there is no existing code or prior architecture to reconcile with. The constraints below come from an earlier requirements-gathering session with the project owner (four rounds of Q&A) and are treated as settled, not open for reconsideration here.

## Goals / Non-Goals

**Goals:**
- Establish one opinionated, working implementation of each capability (authentication, api-client-codegen, ai-agent, dashboard, deployment, quality-gates) that a future per-project fork can extend.
- Keep the stack slim: prefer the framework's own built-in mechanism over a bespoke one wherever both would satisfy a requirement (see the hot-reload decision below).
- Keep the two apps (frontend, backend) independently reasoned-about — no shared code, no monorepo build graph.

**Non-Goals:**
- Supporting multiple databases, multiple auth providers, or multiple deployment targets beyond the one primary + one documented-secondary path.
- A CLI scaffolder or any mechanism for pulling upstream template updates into a project generated from this template — this is a GitHub "template repository" only.
- Social/OAuth login, e2e testing (Playwright), or a monorepo build tool — explicitly deferred, not designed for extensibility toward them beyond leaving the obvious seams (e.g. fastapi-users' OAuth hooks present but inactive).

## Decisions

### Repository layout: plain sibling folders, no monorepo tool
`frontend/` and `backend/` are independent applications with no shared TypeScript/Python code. Turborepo/Nx exist to solve shared-package builds and cross-package task caching — neither applies here. Root-level Docker Compose and a Makefile provide the "run both together" ergonomics without a build-graph tool. Revisit only if a third app or a genuinely shared package appears.

### Package managers: pnpm (frontend), uv (backend)
Both are meaningfully faster than their predecessors (npm/yarn, pip/poetry) and are converging on being the default choice for new projects in each ecosystem as of 2026.

### Auth: fastapi-users + Next.js-owned session cookie
**Decision**: `fastapi-users` provides registration, login, and password-recovery token endpoints on the backend. FastAPI never sets a cookie — it issues a JWT to whoever calls it. Next.js server actions/route handlers call FastAPI server-to-server, then set the httpOnly session cookie themselves.

**Alternative considered**: FastAPI sets the cookie directly, with a shared reverse proxy (Caddy/nginx) putting both apps on the same origin to avoid CORS.

**Why the chosen approach**: it keeps FastAPI a pure, stateless JSON API — easier to reason about, test, and eventually scale or replace independently of the frontend. It avoids needing a reverse proxy in local dev (one less moving part in Docker Compose). This is the conventional pattern for a Next.js app sitting in front of a separate API, and it matches how most engineers coming from the Next.js ecosystem already expect session handling to work.

**Alternative considered for auth library**: hand-rolled JWT issuance + a raw `users` SQLAlchemy table. Rejected — `fastapi-users` gives password hashing, JWT handling, and the password-recovery token flow for free; hand-rolling those is where auth bugs live.

### Password recovery: fastapi-mail + Mailpit
`fastapi-users`' reset-password flow needs something to actually send the email. `fastapi-mail` is the natural FastAPI-native SMTP client. Mailpit runs as a Docker Compose service in dev only — it's an SMTP server with a web UI, so the full "forgot password → email arrives → reset link works" loop is testable locally without touching a real inbox or a paid provider. Production SMTP credentials are an unset, documented environment variable (`SMTP_HOST`, `SMTP_USER`, etc.) — no vendor is hardcoded, so swapping in SES/Postmark/Resend/etc. per project is a config change.

### API client codegen: openapi-typescript + openapi-fetch (not orval)
**Decision**: `openapi-typescript` generates types from FastAPI's OpenAPI schema; `openapi-fetch` is a thin, typed fetch wrapper around them.

**Alternative considered**: `orval`, which can additionally generate TanStack Query hooks and Zod schemas directly from the OpenAPI spec.

**Why the chosen approach**: the project owner explicitly chose the lighter tool. The trade-off is real and intentional — this combo does not produce runtime-validated Zod schemas, unlike orval. That gap is deliberately filled elsewhere (see Zod's role, below) rather than by pulling in orval's larger generation surface.

### Zod's role, given the codegen choice doesn't produce Zod schemas
Three concrete, load-bearing uses (not decorative):
1. **Form validation** — `react-hook-form` + `@hookform/resolvers/zod` on dashboard and auth forms.
2. **SSE payload validation** — the one API boundary OpenAPI/REST codegen structurally cannot cover, since streaming responses aren't representable in an OpenAPI schema. Hand-written Zod schemas validate each streamed agent event client-side before rendering.
3. **Environment variable validation** — `t3-env`-style Zod-validated env vars on the frontend, paired with `pydantic-settings` doing the equivalent on the backend.

### API client sync mechanism: one `chokidar-cli` watcher, not a Watchdog+Chokidar pair
**Decision**: the backend writes `openapi.json` to a location shared with the frontend via a Docker volume. A single `chokidar-cli` process on the frontend watches that file and re-runs the `openapi-typescript` codegen command when it changes.

**Alternative considered**: a Python `watchdog`-based watcher on the backend (regenerating `openapi.json` on source change) paired with a Chokidar-based watcher on the frontend.

**Why the chosen approach**: FastAPI's `--reload` (backed by `watchfiles`) already restarts the backend and serves an updated `/openapi.json` on every source change — a second backend-side watcher would duplicate that. Next.js's dev server already handles its own hot reload. The only actual gap is "frontend client is stale relative to backend schema," and that needs exactly one watcher on exactly one file. Two watcher libraries solving one problem is unnecessary surface area for a boilerplate whose explicit goal is to stay slim.

### AI agent: LangGraph, Postgres checkpointer, Anthropic default via `init_chat_model`
One example agent, one tool, streamed over SSE. State is checkpointed to Postgres (`langgraph-checkpoint-postgres`) rather than in-memory, so conversations survive a backend restart — consistent with Postgres already being the project's only supported database (no added infrastructure). The LLM call is routed through LangChain's `init_chat_model` rather than calling the Anthropic SDK directly, so switching providers is a configuration change, not a code change, while still defaulting to Anthropic.

### Dashboard scope: shell + one CRUD example + AI chat
The AI chat demo alone doesn't exercise the api-client-codegen or Zod-form-validation capabilities at all. One boring CRUD resource (e.g. "items") proves the full typed path — SQLAlchemy model → FastAPI route → generated client → Zod-validated form — independent of the AI path, which is the capability this boilerplate's headline feature ("end-to-end type safety") actually depends on being demonstrated.

### Deployment: Docker Compose primary, Vercel documented for frontend only
Docker Compose is the portable, self-hostable path and works for local dev and most PaaS targets that accept a Dockerfile. A documented (not automated) secondary path covers deploying the frontend to Vercel specifically, since Next.js-on-Vercel is close to a one-click deploy and likely the most common choice for future projects' frontends. The backend is not targeted at a specific PaaS beyond "accepts a Dockerfile."

### Quality gates: Ruff + ESLint/Prettier + pyright, single root pre-commit config
Ruff replaces both a Python linter and Black (it does both lint and format). ESLint (lint) is paired with Prettier (format) on the frontend, since ESLint alone doesn't format. `pyright` in basic mode closes the one asymmetry between the stacks: TypeScript gives the frontend compile-time type safety, but nothing previously caught backend type errors before runtime beyond Pydantic's runtime validation.

**Decision**: one root `.pre-commit-config.yaml` (the Python `pre-commit` framework) covers both ecosystems — native Ruff hooks, plus local hooks that shell out to `pnpm eslint` / `pnpm prettier` for the frontend.

**Alternative considered**: split tooling — `pre-commit` for the backend, `husky` + `lint-staged` for the frontend.

**Why the chosen approach**: one `pre-commit install` and one file contributors need to look at, even though the JS-ecosystem hooks technically shell out to `pnpm`. CI (GitHub Actions, on every PR) runs the same categories of checks — pytest, vitest, pyright, and the OpenAPI client drift-check — as a second enforcement point, not a different one.

### License: AGPLv3 → MIT
**BREAKING** relative to the repo's current state. AGPL is viral in a way that's a poor fit for a boilerplate: if a project built on top of this codebase is deployed as a network service, AGPL's terms arguably require that project's source to be released too — including client/commercial work built from this template. MIT is the de facto standard for this category of project (create-t3-app and comparable starters use it) and imposes no obligations on downstream projects.

## Risks / Trade-offs

- **[Risk] openapi-typescript+openapi-fetch doesn't validate responses at runtime, only types at compile time** → Mitigated by scoping Zod to the boundaries that actually need runtime validation (forms, SSE, env vars) rather than trying to make the REST client do something it isn't designed for.
- **[Risk] Next.js owning the session cookie means every authenticated request pays a server-to-server hop (Next.js → FastAPI) rather than the browser talking to FastAPI directly** → Accepted trade-off for the isolation and CORS-avoidance benefits; latency impact is negligible for a boilerplate's typical request volumes.
- **[Risk] A single `chokidar-cli` watcher is a new moving part in local dev that could silently stop running** → Mitigated by the CI drift-check, which is the actual correctness backstop; the watcher is a dev-convenience layer, not the source of truth.
- **[Risk] Mailpit and the SMTP-catcher pattern only prove the email loop works in dev, not with a real provider** → Accepted; production SMTP is documented but each downstream project must configure and verify its own provider.
- **[Risk] License change affects anyone who may have already cloned or relied on the AGPLv3 terms** → Low impact today since the repo has no prior releases or known external consumers; called out explicitly as **BREAKING** in the proposal regardless.
