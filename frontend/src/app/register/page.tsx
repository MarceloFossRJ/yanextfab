import { AuthCard } from "@/components/auth/auth-card";
import { RegisterForm } from "@/components/auth/register-form";

export default function RegisterPage() {
  return (
    <AuthCard title="Create an account" description="Get started with Yanextfab.">
      <RegisterForm />
    </AuthCard>
  );
}
