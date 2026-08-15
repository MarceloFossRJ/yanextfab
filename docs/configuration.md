# Configuration

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
| `OPENAPI_SCHEMA_PATH` | frontend | Where the frontend watches for schema changes to regenerate its typed client (see [API client codegen](api-client-codegen.md)). Only relevant in dev. |
