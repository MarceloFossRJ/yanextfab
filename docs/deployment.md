# Deployment

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
