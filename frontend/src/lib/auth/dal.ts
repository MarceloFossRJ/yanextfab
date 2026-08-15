import "server-only";

import { redirect } from "next/navigation";
import { cache } from "react";

import { apiClient } from "@/lib/api/client";

import { getSessionToken } from "./session";

/**
 * Data Access Layer: the one place that turns the session cookie into a verified user by
 * calling the backend (a "secure" check, per Next.js's auth guide) — not just reading the
 * cookie's presence. Cached per-request with React's cache() so repeated calls during a
 * single render don't repeat the network round trip.
 */
export const getCurrentUser = cache(async () => {
  const token = await getSessionToken();
  if (!token) return null;

  const { data, error } = await apiClient.GET("/users/me", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (error) return null;
  return data;
});

export async function requireUser() {
  const user = await getCurrentUser();
  if (!user) {
    // Not just /login: an invalid (e.g. expired) cookie must be deleted too, or proxy.ts's
    // optimistic check keeps bouncing the visitor back to /dashboard forever. See
    // /api/auth/clear-session's comment for the full loop this avoids.
    redirect("/api/auth/clear-session");
  }
  return user;
}
