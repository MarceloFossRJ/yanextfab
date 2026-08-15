import { AuthCard } from "@/components/auth/auth-card";
import { ResetPasswordForm } from "@/components/auth/reset-password-form";

export default async function ResetPasswordPage({
  searchParams,
}: {
  searchParams: Promise<{ token?: string }>;
}) {
  const { token } = await searchParams;

  return (
    <AuthCard title="Reset password" description="Choose a new password for your account.">
      {token ? (
        <ResetPasswordForm token={token} />
      ) : (
        <p className="text-destructive text-sm">
          This reset link is missing its token. Request a new one from the forgot password page.
        </p>
      )}
    </AuthCard>
  );
}
