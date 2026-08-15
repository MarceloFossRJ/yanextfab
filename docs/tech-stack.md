# Tech Stack, Briefly

If a name below is new to you, here's the one-line version of what it's for:

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

See `openspec/changes/bootstrap-yanextfab/design.md` for the deeper reasoning behind these
choices (optional reading, not required to get started).
