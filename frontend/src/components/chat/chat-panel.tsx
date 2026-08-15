"use client";

import { useRef, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { chatStreamEventSchema } from "@/lib/schemas/chat";

type ChatMessage = { role: "user" | "assistant"; content: string };

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const conversationId = useRef<string | null>(null);
  if (conversationId.current === null) {
    conversationId.current = crypto.randomUUID();
  }

  function appendToLastAssistantMessage(text: string) {
    setMessages((prev) => {
      const next = [...prev];
      const last = next[next.length - 1];
      if (last?.role === "assistant") {
        next[next.length - 1] = { ...last, content: last.content + text };
      }
      return next;
    });
  }

  async function sendMessage(event: React.FormEvent) {
    event.preventDefault();
    const userMessage = input.trim();
    if (!userMessage || isStreaming) return;

    setInput("");
    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
      { role: "assistant", content: "" },
    ]);
    setIsStreaming(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId.current,
          message: userMessage,
        }),
      });

      if (!response.body) return;

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const frames = buffer.split("\n\n");
        buffer = frames.pop() ?? "";

        for (const frame of frames) {
          const line = frame.trim();
          if (!line.startsWith("data:")) continue;

          let parsed: unknown;
          try {
            parsed = JSON.parse(line.slice("data:".length).trim());
          } catch {
            continue;
          }

          // Validated before rendering — this is the one boundary the OpenAPI codegen
          // can't cover. A malformed event is dropped, not rendered.
          const result = chatStreamEventSchema.safeParse(parsed);
          if (!result.success) continue;

          const streamEvent = result.data;
          if (streamEvent.type === "token") {
            appendToLastAssistantMessage(streamEvent.content);
          } else if (streamEvent.type === "error") {
            appendToLastAssistantMessage(`\n\nError: ${streamEvent.message}`);
          }
        }
      }
    } finally {
      setIsStreaming(false);
    }
  }

  return (
    <div className="flex h-full flex-col gap-4">
      <div className="flex-1 space-y-3 overflow-y-auto">
        {messages.map((message, index) => (
          <div key={index} className={message.role === "user" ? "text-right" : "text-left"}>
            <span className="bg-muted inline-block rounded-lg px-3 py-2 text-sm">
              {message.content || "…"}
            </span>
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage} className="flex gap-2">
        <Input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask something…"
          disabled={isStreaming}
        />
        <Button type="submit" disabled={isStreaming || !input.trim()}>
          Send
        </Button>
      </form>
    </div>
  );
}
