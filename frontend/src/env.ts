import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

/**
 * Validated environment variables. Import `env` instead of reading `process.env` directly
 * so misconfiguration fails fast at startup. No `NEXT_PUBLIC_*` vars are defined here: the
 * backend is only ever called server-side (see design.md's session-cookie ownership decision),
 * so nothing about it needs to be exposed to the browser.
 */
export const env = createEnv({
  server: {
    API_URL: z.url().default("http://localhost:8000"),
    OPENAPI_SCHEMA_PATH: z.string().optional(),
  },
  client: {},
  experimental__runtimeEnv: {},
});
