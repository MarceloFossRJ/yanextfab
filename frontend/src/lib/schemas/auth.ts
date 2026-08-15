import { z } from "zod";

export const loginSchema = z.object({
  email: z.email("Please enter a valid email."),
  password: z.string().min(1, "Password is required."),
});

export const registerSchema = z.object({
  email: z.email("Please enter a valid email."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

export const forgotPasswordSchema = z.object({
  email: z.email("Please enter a valid email."),
});

export const resetPasswordSchema = z.object({
  token: z.string().min(1),
  password: z.string().min(8, "Password must be at least 8 characters."),
});
