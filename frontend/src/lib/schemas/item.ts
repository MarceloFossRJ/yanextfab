import { z } from "zod";

export const itemFormSchema = z.object({
  title: z.string().min(1, "Title is required.").max(200),
  description: z.string().max(2000).optional().or(z.literal("")),
});

export type ItemFormInput = z.infer<typeof itemFormSchema>;
