# Project Structure

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
