"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import type { z } from "zod";

import { resetPassword } from "@/app/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { resetPasswordSchema } from "@/lib/schemas/auth";

type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;

export function ResetPasswordForm({ token }: { token: string }) {
  const [serverError, setServerError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetPasswordInput>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { token },
  });

  async function onSubmit(data: ResetPasswordInput) {
    setServerError(null);
    const result = await resetPassword(data);
    if (result?.error) setServerError(result.error);
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <input type="hidden" {...register("token")} />
      <div className="space-y-2">
        <Label htmlFor="password">New password</Label>
        <Input
          id="password"
          type="password"
          autoComplete="new-password"
          {...register("password")}
        />
        {errors.password && <p className="text-destructive text-sm">{errors.password.message}</p>}
      </div>
      {serverError && <p className="text-destructive text-sm">{serverError}</p>}
      <Button type="submit" disabled={isSubmitting} className="w-full">
        {isSubmitting ? "Resetting…" : "Reset password"}
      </Button>
    </form>
  );
}
