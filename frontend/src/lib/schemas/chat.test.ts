import { describe, expect, it } from "vitest";

import { chatStreamEventSchema } from "./chat";

describe("chatStreamEventSchema", () => {
  it("accepts a token event", () => {
    const result = chatStreamEventSchema.safeParse({ type: "token", content: "hi" });
    expect(result.success).toBe(true);
  });

  it("accepts a done event", () => {
    const result = chatStreamEventSchema.safeParse({ type: "done" });
    expect(result.success).toBe(true);
  });

  it("accepts an error event", () => {
    const result = chatStreamEventSchema.safeParse({ type: "error", message: "boom" });
    expect(result.success).toBe(true);
  });

  it("rejects an unknown event type", () => {
    const result = chatStreamEventSchema.safeParse({ type: "tool_call", content: "x" });
    expect(result.success).toBe(false);
  });

  it("rejects a token event missing content", () => {
    const result = chatStreamEventSchema.safeParse({ type: "token" });
    expect(result.success).toBe(false);
  });

  it("rejects a non-object payload", () => {
    const result = chatStreamEventSchema.safeParse("not json");
    expect(result.success).toBe(false);
  });
});
