"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useState } from "react";
import { useForm } from "react-hook-form";
import type { z } from "zod";

import { forgotPassword } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { forgotPasswordSchema } from "@/lib/schemas/auth";

type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;

export function ForgotPasswordForm() {
  const [submitted, setSubmitted] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ForgotPasswordInput>({ resolver: zodResolver(forgotPasswordSchema) });

  async function onSubmit(data: ForgotPasswordInput) {
    await forgotPassword(data);
    // Always shown, regardless of whether the email is registered — see
    // specs/authentication/spec.md's "Recovery Request Confidentiality" requirement.
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <p className="text-muted-foreground text-sm">
        If an account exists for that email, we&apos;ve sent a link to reset your password.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" autoComplete="email" {...register("email")} />
        {errors.email && <p className="text-destructive text-sm">{errors.email.message}</p>}
      </div>
      <Button type="submit" disabled={isSubmitting} className="w-full">
        {isSubmitting ? "Sending…" : "Send reset link"}
      </Button>
      <div className="text-muted-foreground text-sm">
        <Link href="/login" className="hover:underline">
          Back to sign in
        </Link>
      </div>
    </form>
  );
}
