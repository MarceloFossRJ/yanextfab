"use server";

import { revalidatePath } from "next/cache";

import { apiClient } from "@/lib/api/client";
import { getSessionToken } from "@/lib/auth/session";
import { itemFormSchema } from "@/lib/schemas/item";

type ActionState = { error?: string } | undefined;

async function authHeaders(): Promise<{ Authorization: string }> {
  const token = await getSessionToken();
  if (!token) {
    return { Authorization: "" };
  }
  return { Authorization: `Bearer ${token}` };
}

export async function createItem(input: unknown): Promise<ActionState> {
  const parsed = itemFormSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { error } = await apiClient.POST("/items", {
    headers: await authHeaders(),
    body: { title: parsed.data.title, description: parsed.data.description || null },
  });
  if (error) return { error: "Could not create item." };

  revalidatePath("/dashboard");
  return undefined;
}

export async function updateItem(itemId: string, input: unknown): Promise<ActionState> {
  const parsed = itemFormSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { error } = await apiClient.PATCH("/items/{item_id}", {
    params: { path: { item_id: itemId } },
    headers: await authHeaders(),
    body: { title: parsed.data.title, description: parsed.data.description || null },
  });
  if (error) return { error: "Could not update item." };

  revalidatePath("/dashboard");
  return undefined;
}

export async function deleteItem(itemId: string): Promise<ActionState> {
  const { error } = await apiClient.DELETE("/items/{item_id}", {
    params: { path: { item_id: itemId } },
    headers: await authHeaders(),
  });
  if (error) return { error: "Could not delete item." };

  revalidatePath("/dashboard");
  return undefined;
}
