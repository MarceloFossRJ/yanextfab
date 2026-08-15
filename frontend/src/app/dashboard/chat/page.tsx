import { ChatPanel } from "@/components/chat/chat-panel";

// Auth is enforced by the /dashboard layout (requireUser()).
export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-3.5rem)] p-8">
      <ChatPanel />
    </div>
  );
}
