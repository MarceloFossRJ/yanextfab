"use client";

import { Plus } from "lucide-react";
import { useState } from "react";

import { ItemFormDialog } from "@/components/dashboard/item-form-dialog";
import { Button } from "@/components/ui/button";

export function NewItemButton() {
  const [open, setOpen] = useState(false);
  // Bumped on every open so ItemFormDialog remounts fresh each time (see its own comment on
  // why: React's "reset state with a key" pattern instead of a setState-in-effect).
  const [sessionId, setSessionId] = useState(0);

  return (
    <>
      <Button
        onClick={() => {
          setSessionId((id) => id + 1);
          setOpen(true);
        }}
      >
        <Plus />
        New item
      </Button>
      <ItemFormDialog key={sessionId} open={open} onOpenChange={setOpen} />
    </>
  );
}
