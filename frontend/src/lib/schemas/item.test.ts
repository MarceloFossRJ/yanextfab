import { describe, expect, it } from "vitest";

import { itemFormSchema } from "./item";

describe("itemFormSchema", () => {
  it("accepts a valid title with no description", () => {
    const result = itemFormSchema.safeParse({ title: "Buy groceries" });
    expect(result.success).toBe(true);
  });

  it("accepts a valid title with a description", () => {
    const result = itemFormSchema.safeParse({ title: "Buy groceries", description: "Milk" });
    expect(result.success).toBe(true);
  });

  it("rejects an empty title", () => {
    const result = itemFormSchema.safeParse({ title: "" });
    expect(result.success).toBe(false);
  });

  it("rejects a missing title", () => {
    const result = itemFormSchema.safeParse({});
    expect(result.success).toBe(false);
  });

  it("rejects a title over 200 characters", () => {
    const result = itemFormSchema.safeParse({ title: "a".repeat(201) });
    expect(result.success).toBe(false);
  });
});
