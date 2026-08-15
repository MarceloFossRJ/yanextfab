# Yanextfab

Yet another Next.js and FastAPI boilerplate — a personal-first starter for projects that need a
TypeScript frontend, a Python backend, and heavy AI/agent tooling out of the box.

- **Frontend**: [Next.js](https://nextjs.org/) + React, [Zod](https://zod.dev/) for schema
  validation, [Shadcn/ui](https://ui.shadcn.com/) for components, [Tailwind CSS](https://tailwindcss.com/) for styling
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy](https://www.sqlalchemy.org/) (async) for the database, [Pydantic](https://docs.pydantic.dev/) for data validation, [LangGraph](https://langchain-ai.github.io/langgraph/) for AI agents
- **Auth**: [`fastapi-users`](https://fastapi-users.github.io/fastapi-users/) on the backend, with Next.js owning the session cookie
- **AI**: an example LangGraph agent streamed over SSE, backed by Anthropic via `init_chat_model`

You don't need to already know all of these — see [Tech Stack, Briefly](tech-stack.md) for a
one-line explanation of each.

New here? Start with [Getting Started](getting-started.md).
