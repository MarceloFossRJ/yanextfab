# Adding Your Own Features

**Add a new backend endpoint and use it from the frontend:**

1. Add a route in `backend/src/app/api/` (copy `items.py` as a starting point) and register its
   router in `backend/src/app/main.py`.
2. Save. If you're running via `make up` (or `pnpm dev` locally), the frontend's typed client
   regenerates automatically within a second or two — no restart needed (see
   [API client codegen](api-client-codegen.md) for how this works, and what to check if it
   doesn't seem to be updating).
3. Call it from a Server Action or Route Handler in the frontend using
   `import { apiClient } from "@/lib/api/client"` — see `frontend/src/app/actions/items.ts` for
   a working example. You get autocomplete and type errors for the new endpoint immediately.

**Add a new frontend page:** create a folder under `frontend/src/app/` with a `page.tsx` (this
is standard [Next.js App Router](https://nextjs.org/docs/app/getting-started/layout-and-pages)
file-based routing). Put it under `frontend/src/app/dashboard/` if it should require login and
show the sidebar.
