import { env } from "@/env";
import { getSessionToken } from "@/lib/auth/session";

/**
 * Proxies the chat SSE stream to the backend, attaching the session token server-side.
 * The browser never sees the JWT or calls FastAPI directly — see design.md's
 * session-cookie-ownership decision.
 */
export async function POST(request: Request): Promise<Response> {
  const token = await getSessionToken();
  if (!token) {
    return new Response("Unauthorized", { status: 401 });
  }

  const body = await request.text();

  const backendResponse = await fetch(`${env.API_URL}/ai/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body,
  });

  if (!backendResponse.body) {
    return new Response("No response body", { status: 502 });
  }

  return new Response(backendResponse.body, {
    status: backendResponse.status,
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
