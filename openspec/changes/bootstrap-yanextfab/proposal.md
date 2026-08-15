## Why

Yanextfab is meant to be a personal-first, reusable full-stack starter — TypeScript/Next.js frontend, Python/FastAPI backend, wired for heavy AI/agent workloads via LangGraph — so that new client and side projects can start from a working, typed, authenticated, deployable baseline instead of re-deciding the same dozen infrastructure questions each time. The repo currently has no application code, no chosen license (it ships AGPLv3, which is a poor fit for a boilerplate meant to seed commercial/client work), and no spec history. This change establishes the whole boilerplate in one pass so every subsequent per-project fork starts from the same settled foundation.

## What Changes

- Scaffold a two-app repo (`frontend/`, `backend/` as plain sibling folders, no monorepo tool) orchestrated by root-level Docker Compose, with Postgres as the only supported database.
- Add a complete, wired authentication system: `fastapi-users` (email+password) on the backend, with Next.js owning the httpOnly session cookie and proxying auth calls server-to-server. Password recovery is wired end-to-end via `fastapi-mail`, using Mailpit as the local dev SMTP catcher.
- Add generated, type-safe API client tooling: `openapi-typescript` + `openapi-fetch`, kept in sync with the backend via a single `chokidar-cli` watcher on `openapi.json`, backed by a CI drift-check.
- Add one example LangGraph AI agent (one tool) streamed over SSE to a Next.js chat component, with Postgres-backed checkpointing and Anthropic as the default LLM provider via `init_chat_model`.
- Add a protected dashboard shell plus one CRUD example resource that exercises the full typed path (SQLAlchemy → FastAPI → generated client → Zod-validated form), alongside the AI chat page.
- Add a documented deployment story: Docker Compose as the primary path, a documented secondary path for deploying the frontend to Vercel.
- Add quality gates shared across CI and local pre-commit: Ruff (backend lint+format), ESLint+Prettier (frontend lint+format), pyright (backend type-check), pytest, vitest, and the codegen drift-check — enforced locally via one root `.pre-commit-config.yaml` and in CI via GitHub Actions.
- **BREAKING**: Replace the repo's current AGPLv3 `LICENSE` with MIT.

## Capabilities

### New Capabilities
- `authentication`: fastapi-users-backed signup/login/session/password-recovery flow, with Next.js owning the session cookie.
- `api-client-codegen`: generated TypeScript API client kept in sync with the FastAPI OpenAPI schema, plus CI drift detection.
- `ai-agent`: example LangGraph agent streamed over SSE with persisted, checkpointed state.
- `dashboard`: protected shell, CRUD example resource, and AI chat page.
- `deployment`: Docker Compose primary deployment path plus documented Vercel path for the frontend.
- `quality-gates`: shared lint/format/type-check/test/drift-check enforcement across pre-commit and CI.

### Modified Capabilities
- None — this is the first change in the repo; no existing specs exist yet.

## Impact

- New `frontend/` (Next.js/React/Zod/Shadcn/Tailwind) and `backend/` (FastAPI/SQLAlchemy/Pydantic/LangGraph) applications, plus root-level Docker Compose, `.pre-commit-config.yaml`, and GitHub Actions workflows.
- New runtime dependencies: `fastapi-users`, `fastapi-mail`, `langgraph`, `langgraph-checkpoint-postgres`, `langchain` (for `init_chat_model`), `pydantic-settings`; frontend: `openapi-typescript`, `openapi-fetch`, `chokidar-cli`, `zod`, `react-hook-form`, `@hookform/resolvers`.
- New dev-only service: Mailpit (Docker Compose).
- License file replacement (AGPLv3 → MIT) at repo root — affects anyone who has already relied on the AGPLv3 terms, though the repo has no prior releases or external consumers yet.
