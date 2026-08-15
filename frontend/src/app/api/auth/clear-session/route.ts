import { NextResponse } from "next/server";

import { deleteSession } from "@/lib/auth/session";

/**
 * Deletes an invalid/expired session cookie, then redirects to /login. Cookies can only be
 * mutated in a Server Action or Route Handler, not during a Server Component render — so
 * requireUser() redirects here (rather than deleting directly) when the secure check fails.
 * Without this, a stale cookie loops forever: proxy.ts's optimistic check keeps sending an
 * unauthenticated-looking /login visitor back to /dashboard because the cookie is still
 * present, even though it no longer validates against the backend.
 */
export async function GET(request: Request): Promise<Response> {
  await deleteSession();
  return NextResponse.redirect(new URL("/login", request.url));
}
