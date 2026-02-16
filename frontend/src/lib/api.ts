import { Persona, ChatMessage, Citation } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchPersonas(): Promise<Persona[]> {
  const res = await fetch(`${API_BASE}/api/personas`);
  if (!res.ok) throw new Error("Failed to fetch personas");
  const data = await res.json();
  return data.personas;
}

export async function streamChat(
  personaId: string,
  message: string,
  conversationHistory: ChatMessage[],
  onToken: (token: string) => void,
  onDone: () => void,
  onError: (error: string) => void,
  onSources?: (sources: Citation[]) => void
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      persona_id: personaId,
      message,
      conversation_history: conversationHistory,
    }),
  });

  if (!res.ok) {
    onError(`API error: ${res.status}`);
    return;
  }

  const reader = res.body?.getReader();
  if (!reader) {
    onError("No response body");
    return;
  }

  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data: ")) continue;

      const data = trimmed.slice(6);
      if (data === "[DONE]") {
        onDone();
        return;
      }

      try {
        const parsed = JSON.parse(data);
        if (parsed.error) {
          onError(parsed.error);
          return;
        }
        if (parsed.token) {
          onToken(parsed.token);
        }
        if (parsed.type === "sources" && parsed.sources && onSources) {
          onSources(parsed.sources);
        }
      } catch {
        // Skip malformed lines
      }
    }
  }

  onDone();
}
