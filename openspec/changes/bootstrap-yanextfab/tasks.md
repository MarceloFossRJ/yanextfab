## 1. Repository Scaffold

- [ ] 1.1 Replace `LICENSE` (AGPLv3) with the MIT license text
- [ ] 1.2 Create `frontend/` and `backend/` as sibling directories (no monorepo tool)
- [ ] 1.3 Initialize the frontend app (Next.js, React, TypeScript) with pnpm
- [ ] 1.4 Initialize the backend app (FastAPI project structure) with uv
- [ ] 1.5 Add root-level `docker-compose.yml` with placeholder services: `postgres`, `backend`, `frontend`, `mailpit`
- [ ] 1.6 Add a root `Makefile` (or npm scripts) for common commands (`up`, `down`, `logs`, etc.)

## 2. Backend Foundation

- [ ] 2.1 Configure async SQLAlchemy engine/session against the Postgres service
- [ ] 2.2 Add `pydantic-settings`-based configuration (env vars for DB, SMTP, LLM provider, JWT secret)
- [ ] 2.3 Set up Alembic (or equivalent) migrations
- [ ] 2.4 Confirm FastAPI serves `/openapi.json` and add a script that writes it to the Docker-shared volume location on change

## 3. Frontend Foundation

- [ ] 3.1 Install and configure Tailwind CSS
- [ ] 3.2 Install and configure Shadcn/ui
- [ ] 3.3 Install Zod; add `t3-env`-style validated environment variable schema
- [ ] 3.4 Install `openapi-typescript` + `openapi-fetch`; wire the codegen command to read the shared `openapi.json`
- [ ] 3.5 Install `chokidar-cli`; add a `watch:api-client` dev script that regenerates the client on `openapi.json` change

## 4. Authentication (spec: `authentication`)

- [ ] 4.1 Add `fastapi-users` with an async SQLAlchemy user model (email + hashed password)
- [ ] 4.2 Wire registration and login endpoints; confirm passwords are hashed, never stored plaintext
- [ ] 4.3 Add `fastapi-mail` and configure SMTP against Mailpit for dev
- [ ] 4.4 Wire fastapi-users' forgot-password/reset-password endpoints to send real emails via fastapi-mail; verify unregistered-email requests respond identically to registered ones
- [ ] 4.5 Leave OAuth hooks present in the fastapi-users config but inactive/commented, with a short doc note on enabling them per-project
- [ ] 4.6 Implement Next.js server actions/route handlers that call the backend server-to-server and set the httpOnly session cookie
- [ ] 4.7 Add Next.js middleware/route protection that rejects unauthenticated access to protected routes
- [ ] 4.8 Implement logout (clears the session cookie, invalidates the session)
- [ ] 4.9 Write tests covering registration, login, session persistence across reload, protected-route rejection, and the full password-recovery loop (request → email in Mailpit → reset → old password fails)

## 5. API Client Codegen (spec: `api-client-codegen`)

- [ ] 5.1 Verify generated types update correctly when a backend response schema changes (add/remove a field, regenerate, confirm type diff)
- [ ] 5.2 Add a CI step that regenerates the client from the backend's OpenAPI schema and fails the build if it differs from the committed client
- [ ] 5.3 Document the local dev workflow (`chokidar-cli` watcher) in the README

## 6. AI Agent (spec: `ai-agent`)

- [ ] 6.1 Add LangGraph, `langgraph-checkpoint-postgres`, and LangChain dependencies to the backend
- [ ] 6.2 Implement one example agent graph with one tool
- [ ] 6.3 Configure the agent's LLM call via `init_chat_model`, defaulting to Anthropic, provider swappable via config
- [ ] 6.4 Configure the Postgres-backed checkpointer for conversation state persistence
- [ ] 6.5 Implement a FastAPI SSE endpoint streaming agent responses
- [ ] 6.6 Implement the Next.js chat component consuming the SSE stream
- [ ] 6.7 Write hand-authored Zod schemas validating each streamed event shape on the client; reject/ignore malformed events
- [ ] 6.8 Write a test verifying a conversation resumes correctly from persisted state after a simulated backend restart

## 7. Dashboard (spec: `dashboard`)

- [ ] 7.1 Build the protected dashboard shell (sidebar nav, user menu, logout) gated behind authentication
- [ ] 7.2 Add the SQLAlchemy model, FastAPI routes, and migration for one example CRUD resource (e.g. "items")
- [ ] 7.3 Add the generated-client-backed create/list/update/delete calls on the frontend
- [ ] 7.4 Add the Zod-validated create/edit form using `react-hook-form` + `@hookform/resolvers/zod`
- [ ] 7.5 Add the chat page to dashboard navigation, linking to the AI agent capability
- [ ] 7.6 Write tests covering CRUD create/read/update/delete and client-side validation rejection

## 8. Deployment (spec: `deployment`)

- [ ] 8.1 Finalize `docker-compose.yml` so a fresh checkout boots frontend, backend, Postgres, and Mailpit with one command
- [ ] 8.2 Verify the stack runs unmodified on a second host (or a clean container environment) to confirm portability
- [ ] 8.3 Write the documented Vercel deployment path for the frontend, including how it points at a separately hosted backend

## 9. Quality Gates (spec: `quality-gates`)

- [ ] 9.1 Configure Ruff (lint + format) for the backend
- [ ] 9.2 Configure ESLint + Prettier for the frontend
- [ ] 9.3 Configure `pyright` (basic mode) for the backend
- [ ] 9.4 Set up pytest for the backend and vitest for the frontend
- [ ] 9.5 Add a single root `.pre-commit-config.yaml` with native Ruff hooks plus local hooks shelling out to `pnpm eslint`/`pnpm prettier`
- [ ] 9.6 Add a GitHub Actions workflow running on PR: pytest, vitest, pyright, and the API client drift-check
- [ ] 9.7 Verify a deliberately introduced lint violation is blocked locally by pre-commit and reported by CI

## 10. Documentation

- [ ] 10.1 Update `README.md` with setup instructions (`docker-compose up`, `pre-commit install`, env var requirements)
- [ ] 10.2 Document the production SMTP and LLM provider configuration points
- [ ] 10.3 Document the Vercel frontend deployment path
