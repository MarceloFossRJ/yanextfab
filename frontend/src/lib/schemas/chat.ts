import { z } from "zod";

/**
 * Validates each SSE event streamed from /api/chat before it's rendered. This is the one
 * API boundary the OpenAPI-generated client can't cover — streaming responses aren't
 * representable in an OpenAPI schema — so it's hand-written. See design.md's Zod-role
 * decision.
 */
export const chatStreamEventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("token"), content: z.string() }),
  z.object({ type: z.literal("done") }),
  z.object({ type: z.literal("error"), message: z.string() }),
]);

export type ChatStreamEvent = z.infer<typeof chatStreamEventSchema>;
