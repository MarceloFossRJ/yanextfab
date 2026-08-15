import { redirect } from "next/navigation";

// The dashboard layout itself redirects to /login when unauthenticated, so this single
// redirect covers both the logged-in and logged-out landing experience.
export default function Home() {
  redirect("/dashboard");
}
