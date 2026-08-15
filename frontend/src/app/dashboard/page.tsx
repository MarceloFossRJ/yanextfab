import { ItemsTable } from "@/components/dashboard/items-table";
import { NewItemButton } from "@/components/dashboard/new-item-button";
import { apiClient } from "@/lib/api/client";
import { getSessionToken } from "@/lib/auth/session";

// Auth is enforced by the /dashboard layout (requireUser()).
export default async function DashboardPage() {
  const token = await getSessionToken();
  const { data } = await apiClient.GET("/items", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return (
    <div className="space-y-6 p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Items</h1>
        <NewItemButton />
      </div>
      <ItemsTable items={data ?? []} />
    </div>
  );
}
