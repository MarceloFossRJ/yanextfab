"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import type { z } from "zod";

import { createItem, updateItem } from "@/app/actions/items";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { itemFormSchema } from "@/lib/schemas/item";

type ItemInput = z.infer<typeof itemFormSchema>;

type ExistingItem = { id: string; title: string; description: string | null };

/**
 * Always externally controlled (open/onOpenChange) rather than owning its own
 * DialogTrigger — it's rendered both standalone (a plain "New item" button) and from
 * inside a dropdown menu item (editing), and Base UI's Menu.Item/Dialog.Trigger don't
 * compose cleanly via asChild nesting, so the parent owns open state in both cases.
 *
 * The parent should also give this a `key` that changes per "session" (e.g. the item id,
 * or a counter bumped on each open) — form/error state resets by remounting rather than
 * via a setState-in-effect, per React's guidance on resetting state with a key.
 */
export function ItemFormDialog({
  open,
  onOpenChange,
  item,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  item?: ExistingItem;
}) {
  const [serverError, setServerError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ItemInput>({
    resolver: zodResolver(itemFormSchema),
    defaultValues: { title: item?.title ?? "", description: item?.description ?? "" },
  });

  async function onSubmit(data: ItemInput) {
    setServerError(null);
    const result = item ? await updateItem(item.id, data) : await createItem(data);
    if (result?.error) {
      setServerError(result.error);
      return;
    }
    onOpenChange(false);
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{item ? "Edit item" : "New item"}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Title</Label>
            <Input id="title" {...register("title")} />
            {errors.title && <p className="text-destructive text-sm">{errors.title.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Input id="description" {...register("description")} />
            {errors.description && (
              <p className="text-destructive text-sm">{errors.description.message}</p>
            )}
          </div>
          {serverError && <p className="text-destructive text-sm">{serverError}</p>}
          <DialogFooter>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Saving…" : "Save"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
