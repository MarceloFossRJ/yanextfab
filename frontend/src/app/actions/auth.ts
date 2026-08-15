"use server";

import { redirect } from "next/navigation";

import { apiClient } from "@/lib/api/client";
import { createSession, deleteSession } from "@/lib/auth/session";
import {
  forgotPasswordSchema,
  loginSchema,
  registerSchema,
  resetPasswordSchema,
} from "@/lib/schemas/auth";

export type ActionState = { error?: string } | undefined;

const SESSION_MAX_AGE_SECONDS = 3600;

async function loginWithCredentials(email: string, password: string): Promise<ActionState> {
  const { data, error } = await apiClient.POST("/auth/jwt/login", {
    bodySerializer(body) {
      return new URLSearchParams(body as Record<string, string>).toString();
    },
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: {
      username: email,
      password,
      grant_type: "password",
      scope: "",
      client_id: null,
      client_secret: null,
    },
  });

  if (error || !data) {
    return { error: "Invalid email or password." };
  }

  await createSession(data.access_token, SESSION_MAX_AGE_SECONDS);
  return undefined;
}

// These actions take structured input (not FormData) because auth forms are validated
// client-side with react-hook-form + @hookform/resolvers/zod (see design.md's Zod-role
// decision), then submitted via handleSubmit rather than a bare <form action={...}>.
// Server-side re-validation still runs here, since Server Actions are public-facing
// endpoints regardless of how the client happens to call them.

export async function login(input: unknown): Promise<ActionState> {
  const parsed = loginSchema.safeParse(input);
  if (!parsed.success) {
    return { error: "Please enter a valid email and password." };
  }

  const result = await loginWithCredentials(parsed.data.email, parsed.data.password);
  if (result?.error) return result;

  redirect("/dashboard");
}

export async function registerUser(input: unknown): Promise<ActionState> {
  const parsed = registerSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { error } = await apiClient.POST("/auth/register", {
    body: {
      email: parsed.data.email,
      password: parsed.data.password,
      is_active: true,
      is_superuser: false,
      is_verified: false,
    },
  });

  if (error) {
    const detail = (error as { detail?: string }).detail;
    if (detail === "REGISTER_USER_ALREADY_EXISTS") {
      return { error: "An account with that email already exists." };
    }
    return { error: "Could not create your account. Please try again." };
  }

  const result = await loginWithCredentials(parsed.data.email, parsed.data.password);
  if (result?.error) return result;

  redirect("/dashboard");
}

export async function logout(): Promise<void> {
  await deleteSession();
  redirect("/login");
}

export async function forgotPassword(input: unknown): Promise<ActionState> {
  const parsed = forgotPasswordSchema.safeParse(input);
  if (!parsed.success) {
    return { error: "Please enter a valid email." };
  }

  // Always responds the same way regardless of whether the email is registered —
  // see specs/authentication/spec.md's "Recovery Request Confidentiality" requirement.
  await apiClient.POST("/auth/forgot-password", {
    body: { email: parsed.data.email },
  });

  return undefined;
}

export async function resetPassword(input: unknown): Promise<ActionState> {
  const parsed = resetPasswordSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input." };
  }

  const { error } = await apiClient.POST("/auth/reset-password", {
    body: { token: parsed.data.token, password: parsed.data.password },
  });

  if (error) {
    return { error: "This reset link is invalid or has expired. Request a new one." };
  }

  redirect("/login");
}
