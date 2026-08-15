import createClient from "openapi-fetch";

import { env } from "@/env";

import type { paths } from "./schema";

/**
 * Server-only typed API client. The backend is never called directly from the browser —
 * Next.js server actions/route handlers own the session cookie and proxy to FastAPI
 * server-to-server. See design.md's auth session-cookie-ownership decision.
 */
export const apiClient = createClient<paths>({
  baseUrl: env.API_URL,
});
