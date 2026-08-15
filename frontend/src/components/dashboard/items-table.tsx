"use client";

import { MoreHorizontal } from "lucide-react";
import { useState, useTransition } from "react";

import { deleteItem } from "@/app/actions/items";
import { ItemFormDialog } from "@/components/dashboard/item-form-dialog";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type Item = { id: string; title: string; description: string | null };

export function ItemsTable({ items }: { items: Item[] }) {
  const [isPending, startTransition] = useTransition();
  const [editingItem, setEditingItem] = useState<Item | null>(null);

  if (items.length === 0) {
    return <p className="text-muted-foreground text-sm">No items yet. Create your first one.</p>;
  }

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Title</TableHead>
            <TableHead>Description</TableHead>
            <TableHead className="w-10" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.id}>
              <TableCell>{item.title}</TableCell>
              <TableCell className="text-muted-foreground">{item.description || "—"}</TableCell>
              <TableCell>
                <DropdownMenu>
                  <DropdownMenuTrigger
                    render={<Button variant="ghost" size="icon-sm" disabled={isPending} />}
                  >
                    <MoreHorizontal />
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => setEditingItem(item)}>Edit</DropdownMenuItem>
                    <DropdownMenuItem
                      variant="destructive"
                      onClick={() =>
                        startTransition(() => {
                          void deleteItem(item.id);
                        })
                      }
                    >
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <ItemFormDialog
        key={editingItem?.id ?? "edit-none"}
        open={editingItem !== null}
        onOpenChange={(open) => {
          if (!open) setEditingItem(null);
        }}
        item={editingItem ?? undefined}
      />
    </>
  );
}
